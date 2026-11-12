// npm run lighthouse: serve dist/ locally and check the docs site against Kasane's Lighthouse minimums.
// Run `npm run dist` first. Set CHROME_PATH if Chrome is not found.
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';
import { audit, MIN } from '../lint/lighthouse.js';

const root = fileURLToPath(new URL('../dist/', import.meta.url));
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.md': 'text/markdown; charset=utf-8', '.txt': 'text/plain; charset=utf-8', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' };
const server = createServer(async (req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.endsWith('/')) p += 'index.html';
  try {
    const body = await readFile(join(root, normalize(p).replace(/^(\.\.[/\\])+/, '')));
    res.writeHead(200, { 'content-type': TYPES[extname(p)] || 'application/octet-stream', 'cache-control': 'max-age=3600' });
    res.end(body);
  } catch { res.writeHead(404); res.end('not found'); }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}/`;
const pages = ['', 'principles/', 'color/', 'input/', 'performance/', 'integrate/'];
let ok = true;
try {
  const results = await audit(pages.map((p) => base + p), { presets: ['mobile', 'desktop'], runs: Number(process.env.LH_RUNS || 1) });
  for (const r of results) {
    const line = Object.entries(r.scores).map(([k, v]) => `${k} ${v}${v < MIN[k] ? '✖' : ''}`).join('  ');
    console.log(`${r.pass ? '✓' : '✖'} ${r.url.replace(base, '/')} (${r.preset})  ${line}`);
    for (const [c, list] of Object.entries(r.failing)) for (const a of list) console.log(`    ${c}: ${a.title} ${a.value}`);
    ok &&= r.pass;
  }
} catch (e) { console.error(e.message); ok = false; }
server.close();
process.exit(ok ? 0 : 1);
