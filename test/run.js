// npm test: (1) the Stylelint rules catch what they should, (2) every palette meets the contrast rules.
import stylelint from 'stylelint';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const here = (p) => fileURLToPath(new URL(p, import.meta.url));
const config = (await import('../lint/stylelint.js')).default;
let failed = 0;
const fail = (msg) => { failed++; console.error('  ✗ ' + msg); };
const pass = (msg) => console.log('  ✓ ' + msg);

// ---------------------------------------------------------------- 1. lint rules
console.log('Stylelint rules');
const lint = async (file) => (await stylelint.lint({ files: here(file), config, configBasedir: here('../') })).results[0].warnings;

const good = await lint('fixtures/good.css');
if (good.length) good.forEach((w) => fail(`good.css:${w.line} ${w.rule} — ${w.text}`)); else pass('good.css has no reports');

const bad = await lint('fixtures/bad.css');
const lines = readFileSync(here('fixtures/bad.css'), 'utf8').split('\n');
lines.forEach((text, i) => {
  const m = text.match(/expect (\S+)/);
  if (!m) return;
  const hit = bad.some((w) => w.line === i + 1 && w.rule === m[1]);
  hit ? pass(`bad.css:${i + 1} ${m[1]}`) : fail(`bad.css:${i + 1} expected ${m[1]}`);
});

// ---------------------------------------------------------------- 2. HTML check
console.log('\nHTML check (kasane-check)');
const { checkHtml } = await import('../lint/check.js');
const goodHtml = checkHtml(readFileSync(here('fixtures/good.html'), 'utf8'));
if (goodHtml.length) goodHtml.forEach((w) => fail(`good.html:${w.line} ${w.rule} — ${w.text}`)); else pass('good.html has no reports');
const badSrc = readFileSync(here('fixtures/bad.html'), 'utf8');
const badHtml = checkHtml(badSrc);
badSrc.split('\n').forEach((text, i) => {
  const m = text.match(/expect (\S+) -->/);
  if (!m) return;
  badHtml.some((w) => w.line === i + 1 && w.rule === m[1]) ? pass(`bad.html:${i + 1} ${m[1]}`) : fail(`bad.html:${i + 1} expected ${m[1]}`);
});
const expected = (badSrc.match(/expect /g) || []).length;
if (badHtml.length !== expected) fail(`bad.html: ${badHtml.length} reports, expected ${expected}: ` + badHtml.map((w) => w.line + ' ' + w.rule).join(', '));

// ---------------------------------------------------------------- 3. image optimisation
console.log('\nImage optimisation (kasane-image)');
{
  const { optimize, compare, SSIM_MIN } = await import('../lint/image.js');
  const sharp = (await import('sharp')).default;
  const { mkdtempSync } = await import('node:fs');
  const { tmpdir } = await import('node:os');
  const { join } = await import('node:path');
  const dir = mkdtempSync(join(tmpdir(), 'kasane-img-'));
  // a test picture: smooth gradient with a few shapes and some noise
  const W = 800, H = 500, px = Buffer.alloc(W * H * 3);
  let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = (y * W + x) * 3, ring = Math.hypot(x - 300, y - 250) < 120 ? 60 : 0;
    px[i] = 90 + (120 * x) / W + ring + rnd() * 10; px[i + 1] = 70 + (140 * y) / H + rnd() * 10; px[i + 2] = 180 - (80 * x) / W - ring + rnd() * 10;
  }
  const src = join(dir, 'sample.png');
  await sharp(px, { raw: { width: W, height: H, channels: 3 } }).png().toFile(src);
  const [r] = await optimize([src], { out: join(dir, 'out'), widths: [400, 800], formats: ['avif', 'webp'] });
  const srcKb = r.original.kb;
  for (const o of r.outputs) {
    const label = `${o.width}px ${o.format}: q=${o.quality}${o.lossless ? '' : ''} SSIM ${o.ssim.toFixed(4)} ${o.kb.toFixed(1)} KB`;
    o.ok && o.ssim >= SSIM_MIN && o.kb < srcKb ? pass(label) : fail(label + ' (expected SSIM >= ' + SSIM_MIN + ' and smaller than the source)');
  }
  const s = await compare(src, r.outputs.find((o) => o.width === 800).path);
  s >= SSIM_MIN ? pass(`--compare: SSIM ${s.toFixed(4)}`) : fail(`--compare: SSIM ${s.toFixed(4)}`);
}

// ---------------------------------------------------------------- 4. contrast
console.log('\nPalette contrast (v1/tokens.json)');
const tokens = JSON.parse(readFileSync(here('../v1/tokens.json'), 'utf8'));
const lin = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const lum = (hex) => { const n = [1, 3, 5].map((i) => lin(parseInt(hex.substr(i, 2), 16) / 255)); return 0.2126 * n[0] + 0.7152 * n[1] + 0.0722 * n[2]; };
const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
// [text, background(s), minimum]
const RULES = [
  ['ink', ['bg', 'surface', 'surface-2', 'surface-3'], 4.5],
  ['muted', ['bg', 'surface', 'surface-2'], 4.5],
  ['accent-ink', ['bg', 'surface', 'surface-2', 'accent-soft'], 4.5],
  ['on-accent', ['accent'], 4.5],
  ['ok', ['ok-soft'], 4.5], ['danger', ['danger-soft'], 4.5], ['info', ['info-soft'], 4.5],
  ['line', ['surface'], 3],
  ['focus', ['bg', 'surface', 'surface-2'], 3],
];
for (const [id, pal] of Object.entries(tokens.palette)) {
  for (const theme of ['light', 'dark']) {
    const t = pal[theme];
    let worst = Infinity;
    for (const [fg, bgs, min] of RULES) for (const bg of bgs) {
      const r = ratio(t[fg].$value, t[bg].$value);
      worst = Math.min(worst, r / min);
      if (r < min) fail(`${id} ${theme}: ${fg} on ${bg} = ${r.toFixed(2)}:1 (needs ${min}:1)`);
    }
    if (worst >= 1) pass(`${id} ${theme}`);
  }
}

// ---------------------------------------------------------------- 5. ja / en specs say the same thing
console.log('\nSpecs (v1/kasane.md, v1/kasane.en.md)');
const shape = (file) => {
  const t = readFileSync(here('../v1/' + file), 'utf8');
  const fences = t.match(/^```\w*$/gm) || [];
  return {
    headings: (t.match(/^#{1,3} /gm) || []).join(''),
    sections: (t.match(/^## (\d+)\./gm) || []).join(','),
    code: fences.filter((_, i) => i % 2 === 0).join(','),
    tables: (t.match(/^\|---/gm) || []).length,
    classes: [...new Set(t.match(/\bk-[a-z0-9-]+/g) || [])].sort().join(' '),
    tokens: [...new Set(t.match(/--[a-z][a-z0-9-]*/g) || [])].sort().join(' '),
  };
};
const ja = shape('kasane.md'), en = shape('kasane.en.md');
for (const k of Object.keys(ja)) (ja[k] === en[k] ? pass : fail)(`same ${k}` + (ja[k] === en[k] ? '' : `\n      ja: ${ja[k]}\n      en: ${en[k]}`));

// ---------------------------------------------------------------- 6. docs links go to real URLs
console.log('\nDocs site links');
{
  const walk = (d) => readdirSync(d).flatMap((f) => { const p = d + '/' + f; return statSync(p).isDirectory() ? walk(p) : p.endsWith('.html') ? [p] : []; });
  const bad = walk(here('../site')).flatMap((f) => (readFileSync(f, 'utf8').match(/href="#[^"]*"/g) || []).map((m) => f.split('/site/')[1] + ' ' + m));
  (bad.length ? fail : pass)('no #name links left (every page link is a /name/ URL)' + (bad.length ? '\n      ' + bad.slice(0, 5).join('\n      ') : ''));
}

console.log(failed ? `\n${failed} check(s) failed` : '\nAll checks passed');
process.exit(failed ? 1 : 0);
