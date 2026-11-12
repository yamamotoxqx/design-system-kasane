#!/usr/bin/env node
// kasane-lighthouse: runs the Lighthouse CLI and fails when a score is below Kasane's minimums.
//
//   kasane-lighthouse http://localhost:3000/ [more URLs] [--preset mobile|desktop|both] [--runs 3]
//                     [--min performance=90,accessibility=100,best-practices=95,seo=90] [--json]
//
// Needs the lighthouse package (npm install --save-dev lighthouse) and Chrome.
// Set CHROME_PATH if Chrome is not found automatically.
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import { join } from 'node:path';

export const MIN = { performance: 90, accessibility: 100, 'best-practices': 95, seo: 90 };
const LABEL = { performance: 'パフォーマンス', accessibility: 'アクセシビリティ', 'best-practices': 'ベストプラクティス', seo: 'SEO' };
const CATS = Object.keys(MIN);

function lighthouseBin() {
  for (const base of [join(process.cwd(), 'noop.js'), import.meta.url]) {
    try { return createRequire(base).resolve('lighthouse/cli/index.js'); } catch { /* try next */ }
  }
  return null;
}

function runOnce(bin, url, preset) {
  const args = [bin, url, '--output=json', '--output-path=stdout', '--quiet',
    `--only-categories=${CATS.join(',')}`, '--chrome-flags=--headless=new --no-sandbox --disable-gpu'];
  if (preset === 'desktop') args.push('--preset=desktop');
  return new Promise((resolve, reject) => {
    const p = spawn(process.execPath, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '', err = '';
    p.stdout.on('data', (d) => { out += d; });
    p.stderr.on('data', (d) => { err += d; });
    p.on('close', (code) => {
      if (code !== 0) return reject(new Error(`Lighthouse が失敗しました(${url}, ${preset}):\n${err.trim().split('\n').slice(-5).join('\n')}`));
      try { resolve(JSON.parse(out)); } catch { reject(new Error('Lighthouse の結果を読めませんでした')); }
    });
  });
}

// Chrome sometimes fails to start on CI machines; try again a couple of times before giving up.
async function withRetry(fn, tries = 3) {
  for (let i = 1; ; i++) {
    try { return await fn(); } catch (e) {
      if (i >= tries || !/debugging port|ECONNREFUSED|Chrome|launch/i.test(e.message)) throw e;
      await new Promise((r) => setTimeout(r, 2000 * i));
    }
  }
}

const median = (xs) => { const s = [...xs].sort((a, b) => a - b); return s[Math.floor(s.length / 2)]; };

/** Run Lighthouse for each URL and preset. Returns results with scores (0-100) and failing audits. */
export async function audit(urls, { presets = ['mobile', 'desktop'], runs = 1, min = MIN } = {}) {
  const bin = lighthouseBin();
  if (!bin) throw new Error('lighthouse が見つかりません: npm install --save-dev lighthouse');
  const results = [];
  for (const url of urls) {
    for (const preset of presets) {
      const reports = [];
      for (let i = 0; i < runs; i++) reports.push(await withRetry(() => runOnce(bin, url, preset)));
      // use the run with the median performance score; other categories rarely vary
      const perf = reports.map((r) => r.categories.performance.score);
      const lhr = reports[perf.indexOf(median(perf))];
      const scores = Object.fromEntries(CATS.map((c) => [c, Math.round((lhr.categories[c].score ?? 0) * 100)]));
      const failing = {};
      for (const c of CATS) {
        if (scores[c] >= min[c]) continue;
        failing[c] = lhr.categories[c].auditRefs
          .filter((ref) => ref.weight > 0)
          .map((ref) => lhr.audits[ref.id])
          .filter((a) => a && a.score !== null && a.score < 0.9)
          .sort((a, b) => a.score - b.score)
          .slice(0, 6)
          .map((a) => ({ id: a.id, title: a.title, value: a.displayValue || '' }));
      }
      results.push({ url, preset, scores, failing, pass: CATS.every((c) => scores[c] >= min[c]) });
    }
  }
  return results;
}

// ------------------------------------------------------------ CLI
const isMain = /kasane-lighthouse$|lighthouse\.js$/.test(process.argv[1] || '');
if (isMain) {
  const argv = process.argv.slice(2);
  const opt = (k) => { const i = argv.indexOf(k); return i >= 0 ? argv.splice(i, 2)[1] : undefined; };
  const json = argv.includes('--json'); if (json) argv.splice(argv.indexOf('--json'), 1);
  const preset = opt('--preset') || 'both';
  const runs = Number(opt('--runs') || 1);
  const min = { ...MIN };
  const m = opt('--min');
  if (m) for (const kv of m.split(',')) { const [k, v] = kv.split('='); if (k in min) min[k] = Number(v); }
  const urls = argv.filter((a) => /^https?:\/\//.test(a));
  if (!urls.length) {
    console.log(`使い方: kasane-lighthouse URL… [--preset mobile|desktop|both] [--runs 3] [--min performance=90,...] [--json]

Kasane の最低点:
${CATS.map((c) => `  ${LABEL[c].padEnd(10, '　')} ${MIN[c]} 点以上`).join('\n')}

lighthouse(npm install --save-dev lighthouse)と Chrome が必要です。`);
    process.exit(0);
  }
  try {
    const presets = preset === 'both' ? ['mobile', 'desktop'] : [preset];
    const results = await audit(urls, { presets, runs, min });
    if (json) console.log(JSON.stringify({ min, results }, null, 2));
    else {
      for (const r of results) {
        console.log(`\n${r.url}  (${r.preset === 'mobile' ? 'モバイル' : 'デスクトップ'})`);
        for (const c of CATS) console.log(`  ${r.scores[c] >= min[c] ? '✓' : '✖'} ${LABEL[c].padEnd(10, '　')} ${String(r.scores[c]).padStart(3)}  (最低 ${min[c]})`);
        for (const [c, list] of Object.entries(r.failing)) {
          if (!list.length) continue;
          console.log(`    ${LABEL[c]}を下げている項目:`);
          for (const a of list) console.log(`      - ${a.title}${a.value ? `(${a.value})` : ''}  [${a.id}]`);
        }
      }
      const failed = results.filter((r) => !r.pass).length;
      console.log(failed ? `\n✖ ${failed} 件が最低点に届きませんでした` : '\n✓ すべて最低点を満たしています');
    }
    process.exit(results.every((r) => r.pass) ? 0 : 1);
  } catch (e) {
    console.error(e.message);
    process.exit(2);
  }
}
