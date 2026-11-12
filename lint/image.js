#!/usr/bin/env node
// kasane-image: makes web-ready images and checks their quality with SSIM.
// For each input, width and format it searches for the lowest quality whose SSIM
// against the (resized) original is at or above the threshold.
//
//   kasane-image photo.jpg [more files] [--out public/img] [--widths 640,1280]
//                [--formats avif,webp] [--ssim 0.98] [--budget 100]
//   kasane-image --compare original.png compressed.avif
import { mkdirSync, existsSync, statSync, writeFileSync } from 'node:fs';
import { basename, extname, join } from 'node:path';

const DEFAULTS = { out: 'optimized', widths: [640, 1280, 1920], formats: ['avif', 'webp'], ssim: 0.99, budget: 100 };
export const SSIM_MIN = DEFAULTS.ssim;

async function deps() {
  try {
    const sharp = (await import('sharp')).default;
    const { ssim } = await import('ssim.js');
    return { sharp, ssim };
  } catch {
    console.error('kasane-image には sharp と ssim.js が必要です: npm install --save-dev sharp ssim.js');
    process.exit(2);
  }
}

/** Raw RGBA pixels of an image at an exact size. */
async function rgba(sharp, input, width, height) {
  const { data, info } = await sharp(input).resize(width, height, { fit: 'fill' }).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  return { data: new Uint8ClampedArray(data.buffer, data.byteOffset, data.length), width: info.width, height: info.height };
}

/** SSIM of `candidate` against `reference` (both buffers or paths), compared at the reference's size. */
export async function compare(reference, candidate) {
  const { sharp, ssim } = await deps();
  const meta = await sharp(reference).metadata();
  const a = await rgba(sharp, reference, meta.width, meta.height);
  const b = await rgba(sharp, candidate, meta.width, meta.height);
  return ssim(a, b).mssim;
}

const ENCODERS = {
  avif: (img, q) => img.avif({ quality: q, effort: 4 }),
  webp: (img, q) => img.webp({ quality: q, effort: 5 }),
  jpeg: (img, q) => img.jpeg({ quality: q, mozjpeg: true }),
};
// Used only when even quality 100 misses the threshold (very noisy images)
const LOSSLESS = {
  avif: (img) => img.avif({ lossless: true, effort: 4 }),
  webp: (img) => img.webp({ lossless: true, effort: 5 }),
  jpeg: (img) => img.jpeg({ quality: 100, mozjpeg: true }),
};

/** Lowest quality (by binary search) that meets the SSIM threshold. */
async function encodeBest(sharp, ssim, src, width, height, format, threshold) {
  const ref = await rgba(sharp, src, width, height);
  const refPng = await sharp(src).resize(width, height, { fit: 'fill' }).png().toBuffer();
  const tryQ = async (q) => {
    const buf = await ENCODERS[format](sharp(refPng), q).toBuffer();
    const out = await rgba(sharp, buf, width, height);
    return { q, buf, score: ssim(ref, out).mssim };
  };
  let lo = 30, hi = 100, best = await tryQ(hi);
  if (best.score < threshold) {
    const buf = await LOSSLESS[format](sharp(refPng)).toBuffer();
    const score = ssim(ref, await rgba(sharp, buf, width, height)).mssim;
    return { q: 'lossless', buf, score, ok: score >= threshold, lossless: true };
  }
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    const r = await tryQ(mid);
    if (r.score >= threshold) { best = r; hi = mid - 1; } else lo = mid + 1;
  }
  return { ...best, ok: true };
}

export async function optimize(files, opts = {}) {
  const o = { ...DEFAULTS, ...opts };
  const { sharp, ssim } = await deps();
  mkdirSync(o.out, { recursive: true });
  const results = [];
  for (const file of files) {
    const meta = await sharp(file).metadata();
    const name = basename(file, extname(file));
    let widths = o.widths.filter((w) => w <= meta.width);
    if (!widths.length) widths = [meta.width];
    const outputs = [];
    for (const w of widths) {
      const h = Math.round((meta.height * w) / meta.width);
      for (const f of o.formats) {
        const r = await encodeBest(sharp, ssim, file, w, h, f, o.ssim);
        const path = join(o.out, `${name}-${w}.${f === 'jpeg' ? 'jpg' : f}`);
        writeFileSync(path, r.buf);   // write the encoded bytes as they are (re-encoding would change the quality)
        outputs.push({ path, width: w, height: h, format: f, quality: r.q, lossless: !!r.lossless, ssim: r.score, kb: r.buf.length / 1024, ok: r.ok, overBudget: r.buf.length / 1024 > o.budget });
      }
    }
    results.push({ file, original: { width: meta.width, height: meta.height, kb: statSync(file).size / 1024 }, outputs });
  }
  return results;
}

function pictureSnippet(r, formats) {
  const by = (f) => r.outputs.filter((x) => x.format === f);
  const largest = r.outputs[r.outputs.length - 1];
  const srcset = (f) => by(f).map((x) => `${x.path} ${x.width}w`).join(', ');
  const fallback = by(formats[formats.length - 1]);
  const mid = fallback[Math.floor((fallback.length - 1) / 2)] || largest;
  return ['<picture>',
    ...formats.slice(0, -1).map((f) => `  <source type="image/${f}" srcset="${srcset(f)}" sizes="100vw">`),
    `  <img src="${mid.path}" srcset="${srcset(formats[formats.length - 1])}" sizes="100vw"`,
    `       width="${largest.width}" height="${largest.height}" alt="(画像の内容を書く)" loading="lazy" decoding="async">`,
    '</picture>'].join('\n');
}

// ------------------------------------------------------------ CLI
const isMain = /kasane-image$|image\.js$/.test(process.argv[1] || '');
if (isMain) {
  const argv = process.argv.slice(2);
  const opt = (k) => { const i = argv.indexOf(k); return i >= 0 ? argv.splice(i, 2)[1] : undefined; };
  if (argv.includes('--compare')) {
    argv.splice(argv.indexOf('--compare'), 1);
    const th = Number(opt('--ssim') || DEFAULTS.ssim);
    const [a, b] = argv;
    if (!a || !b) { console.error('使い方: kasane-image --compare 元の画像 軽量化した画像 [--ssim 0.98]'); process.exit(2); }
    const s = await compare(a, b);
    console.log(`SSIM ${s.toFixed(4)}  ${s >= th ? '✓' : '✖'} 基準 ${th}`);
    process.exit(s >= th ? 0 : 1);
  }
  const o = {};
  const out = opt('--out'); if (out) o.out = out;
  const widths = opt('--widths'); if (widths) o.widths = widths.split(',').map(Number);
  const formats = opt('--formats'); if (formats) o.formats = formats.split(',');
  const th = opt('--ssim'); if (th) o.ssim = Number(th);
  const budget = opt('--budget'); if (budget) o.budget = Number(budget);
  const files = argv.filter((a) => !a.startsWith('--') && existsSync(a));
  if (!files.length) {
    console.log(`使い方: kasane-image 画像… [--out ${DEFAULTS.out}] [--widths ${DEFAULTS.widths}] [--formats ${DEFAULTS.formats}] [--ssim ${DEFAULTS.ssim}] [--budget ${DEFAULTS.budget}]
       kasane-image --compare 元の画像 軽量化した画像

幅ごと・形式ごとに、SSIM が基準(既定 ${DEFAULTS.ssim})以上になる一番低い品質を自動で選んで書き出します。`);
    process.exit(files.length ? 0 : (argv.length ? 2 : 0));
  }
  const fm = o.formats || DEFAULTS.formats;
  const results = await optimize(files, o);
  let bad = 0;
  for (const r of results) {
    console.log(`\n${r.file}  (${r.original.width}×${r.original.height}, ${r.original.kb.toFixed(0)} KB)`);
    for (const x of r.outputs) {
      const mark = !x.ok ? '✖' : x.overBudget ? '⚠' : '✓';
      if (!x.ok) bad++;
      console.log(`  ${mark} ${x.path.padEnd(40)} q=${String(x.quality).padStart(3)}  SSIM ${x.ssim.toFixed(4)}  ${x.kb.toFixed(1).padStart(7)} KB${x.overBudget ? `  (目安 ${o.budget || DEFAULTS.budget} KB を超えています。幅を小さくできないか確かめてください)` : ''}${x.lossless ? '  (画質を落とすと基準に届かないため可逆圧縮にしました)' : ''}${!x.ok ? '  (可逆圧縮でも SSIM の基準に届きません)' : ''}`);
    }
    console.log('\n' + pictureSnippet(r, fm));
  }
  console.log(bad ? `\n✖ ${bad} 件が SSIM の基準に届きませんでした` : '\n✓ すべて SSIM の基準を満たしています。最後に目でも確かめてください。');
  process.exit(bad ? 1 : 0);
}
