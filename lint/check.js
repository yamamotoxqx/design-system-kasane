#!/usr/bin/env node
// kasane-check: checks HTML against the Kasane rules that Stylelint cannot see.
// Usage: kasane-check "src/**/*.html" [more files or folders] [--json]
import { parseDocument, DomUtils } from 'htmlparser2';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, resolve, sep } from 'node:path';

const data = (f) => JSON.parse(readFileSync(new URL(`./data/${f}`, import.meta.url), 'utf8'));
const K_CLASSES = new Set(data('classes.json'));
const LUCIDE = data('lucide.json');
const LUCIDE_NAMES = new Set(LUCIDE.names);

export const RULES = {
  'one-primary': '主ボタン(k-btn-primary)は1つの画面に1つまでです。ほかは k-btn か k-btn-quiet にしてください。',
  'status-icon': '状態(成功・エラー・情報)には、色だけでなくアイコンを添えてください(Lucide の check / circle-alert / info)。',
  'inline-style': 'style 属性に色・影・枠線・書体を直接書かないでください。トークンを使うクラスで指定します。',
  'icon-button-label': '文字のないボタン・リンクには aria-label で名前を付けてください。',
  'form-label': '入力欄にはラベルを付けてください(<label> で囲む、<label for> で結ぶ、または aria-label)。',
  'switch-structure': 'k-switch の中には <input type="checkbox"> と <span class="k-switch-track"> が必要です。',
  'unknown-class': 'Kasane にない k- のクラスです。書き間違いか、自分の部品なら k- 以外の名前にしてください。',
  'lucide-icon': 'アイコンは Lucide から取ってきて貼ってください(class="lucide lucide-名前" を残す)。',
  'dialog-label': 'role="dialog" には aria-labelledby(見出しの id)か aria-label が必要です。',
  'tab-aria': 'role="tab" には aria-selected と aria-controls が必要です。',
};

// ------------------------------------------------------------ helpers
const cls = (el) => (el.attribs && el.attribs.class ? el.attribs.class.split(/\s+/).filter(Boolean) : []);
const has = (el, c) => cls(el).includes(c);
const attr = (el, a) => (el.attribs ? el.attribs[a] : undefined);
const text = (el) => DomUtils.textContent(el).replace(/\s+/g, '').trim();
const find = (root, test) => DomUtils.findAll((e) => e.type === 'tag' && test(e), Array.isArray(root) ? root : [root]);
const ancestors = function* (el) { for (let p = el.parent; p; p = p.parent) if (p.type === 'tag') yield p; };
const ignored = (el, rule) => {
  for (const e of [el, ...ancestors(el)]) {
    const v = attr(e, 'data-kasane-ignore');
    if (v !== undefined && (v.trim() === '' || v.split(/[\s,]+/).includes(rule))) return true;
  }
  return false;
};

const COLOR_FN = /\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(/i;
const HEX = /(^|[\s,(:])#[0-9a-f]{3,8}\b/i;
const NAMED = /(?:^|[\s:,])(?:white|black|red|green|blue|yellow|orange|purple|pink|gray|grey|silver|navy|teal|gold|brown|cyan|magenta|lime|maroon|olive)(?:$|[\s;,!])/i;

function checkStyle(el, style) {
  const decls = style.split(';').map((d) => d.trim()).filter(Boolean);
  for (const d of decls) {
    const i = d.indexOf(':');
    if (i < 0) continue;
    const prop = d.slice(0, i).trim().toLowerCase();
    const val = d.slice(i + 1).replace(/url\([^)]*\)/gi, '').trim();
    if (HEX.test(' ' + val) || COLOR_FN.test(val)) return `"${d}"`;
    if (/color|background|fill|stroke/.test(prop) && NAMED.test(' ' + val + ' ')) return `"${d}"`;
    if (/shadow/.test(prop) && !/^none$/i.test(val)) return `"${d}"`;
    if (/^border(?:-(?:top|right|bottom|left))?(?:-(?:width|style|color))?$/.test(prop) && !/^(?:none|0|0px)$/i.test(val)
        && !['input', 'select', 'textarea'].includes(el.name)) return `"${d}"`;
    if (prop === 'font-family' && !/var\(--font-/.test(val)) return `"${d}"`;
  }
  return null;
}

// ------------------------------------------------------------ check one document
export function checkHtml(src) {
  const doc = parseDocument(src, { withStartIndices: true, lowerCaseAttributeNames: true });
  const lineStarts = [0];
  for (let i = 0; i < src.length; i++) if (src[i] === '\n') lineStarts.push(i + 1);
  const pos = (idx) => {
    let lo = 0, hi = lineStarts.length - 1;
    while (lo < hi) { const m = (lo + hi + 1) >> 1; if (lineStarts[m] <= idx) lo = m; else hi = m - 1; }
    return { line: lo + 1, column: idx - lineStarts[lo] + 1 };
  };
  const out = [];
  const report = (rule, el, extra) => {
    if (ignored(el, rule)) return;
    out.push({ rule: `kasane/${rule}`, ...pos(el.startIndex ?? 0), text: RULES[rule] + (extra ? ` ${extra}` : '') });
  };
  const all = find(doc.children, () => true);
  const labelFor = new Set(all.filter((e) => e.name === 'label' && attr(e, 'for')).map((e) => attr(e, 'for')));

  // one-primary
  all.filter((e) => has(e, 'k-btn-primary')).slice(1).forEach((e) => report('one-primary', e));

  for (const el of all) {
    const c = cls(el);
    // status-icon
    if (c.some((x) => ['k-badge-ok', 'k-badge-danger', 'k-badge-info', 'k-error'].includes(x)) && !find(el.children, (e) => e.name === 'svg').length) report('status-icon', el);
    // inline-style
    const st = attr(el, 'style');
    if (st) { const bad = checkStyle(el, st); if (bad) report('inline-style', el, bad); }
    // icon-button-label
    if ((el.name === 'button' || (el.name === 'a' && attr(el, 'href') !== undefined)) && !text(el)
        && !attr(el, 'aria-label') && !attr(el, 'aria-labelledby') && !attr(el, 'title')) report('icon-button-label', el);
    // form-label
    const type = (attr(el, 'type') || 'text').toLowerCase();
    if ((el.name === 'input' && !['hidden', 'submit', 'button', 'reset', 'image'].includes(type)) || el.name === 'select' || el.name === 'textarea') {
      const ok = attr(el, 'aria-label') || attr(el, 'aria-labelledby') || attr(el, 'title')
        || [...ancestors(el)].some((a) => a.name === 'label') || (attr(el, 'id') && labelFor.has(attr(el, 'id')));
      if (!ok) report('form-label', el);
    }
    // switch-structure
    if (c.includes('k-switch')) {
      const inp = find(el.children, (e) => e.name === 'input' && (attr(e, 'type') || '').toLowerCase() === 'checkbox');
      const track = find(el.children, (e) => has(e, 'k-switch-track'));
      if (!inp.length || !track.length) report('switch-structure', el);
    }
    // unknown-class
    const unknown = c.filter((x) => x.startsWith('k-') && !K_CLASSES.has(x));
    if (unknown.length) report('unknown-class', el, unknown.map((x) => `"${x}"`).join(' '));
    // lucide-icon
    if (el.name === 'svg') {
      const names = c.filter((x) => x.startsWith('lucide-')).map((x) => x.slice(7));
      const bad = names.filter((n) => !LUCIDE_NAMES.has(n));
      if (bad.length) report('lucide-icon', el, `Lucide ${LUCIDE.version} に "${bad.join('", "')}" はありません。`);
      else if (!c.includes('lucide') && [...ancestors(el)].some((a) => cls(a).some((x) => ['k-btn', 'k-badge', 'k-error'].includes(x)))) report('lucide-icon', el);
    }
    // dialog-label
    if (attr(el, 'role') === 'dialog' && !attr(el, 'aria-labelledby') && !attr(el, 'aria-label')) report('dialog-label', el);
    // tab-aria
    if (attr(el, 'role') === 'tab' && (attr(el, 'aria-selected') === undefined || attr(el, 'aria-controls') === undefined)) report('tab-aria', el);
  }
  return out.sort((a, b) => a.line - b.line || a.column - b.column);
}

// ------------------------------------------------------------ files
function globToRegex(pattern) {
  let re = '';
  for (let i = 0; i < pattern.length; i++) {
    const ch = pattern[i];
    if (ch === '*') {
      if (pattern[i + 1] === '*') { re += '(?:.*/)?'; i += pattern[i + 2] === '/' ? 2 : 1; } else re += '[^/]*';
    } else if (ch === '?') re += '[^/]';
    else if (ch === '{') { const end = pattern.indexOf('}', i); re += '(?:' + pattern.slice(i + 1, end).split(',').map((s) => s.replace(/[.+^$()|[\]\\]/g, '\\$&')).join('|') + ')'; i = end; }
    else re += ch.replace(/[.+^$()|[\]\\]/g, '\\$&');
  }
  return new RegExp('^' + re + '$');
}
function walk(dir, acc = []) {
  for (const n of readdirSync(dir)) {
    if (n === 'node_modules' || n.startsWith('.')) continue;
    const p = join(dir, n);
    statSync(p).isDirectory() ? walk(p, acc) : acc.push(p);
  }
  return acc;
}
export function expand(args) {
  const files = new Set();
  for (const a of args) {
    if (existsSync(a) && statSync(a).isDirectory()) { walk(a).filter((f) => /\.html?$/i.test(f)).forEach((f) => files.add(f)); continue; }
    if (existsSync(a)) { files.add(a); continue; }
    const base = a.split(/[*?{]/)[0].replace(/[^/]*$/, '') || '.';
    if (!existsSync(base)) continue;
    const re = globToRegex(a.replace(/^\.\//, ''));
    walk(base).map((f) => relative('.', f).split(sep).join('/')).filter((f) => re.test(f)).forEach((f) => files.add(f));
  }
  return [...files];
}

// ------------------------------------------------------------ CLI
const isMain = process.argv[1] && resolve(process.argv[1]).replace(/\.js$/, '') === resolve(new URL(import.meta.url).pathname).replace(/\.js$/, '')
  || /kasane-check$/.test(process.argv[1] || '');
if (isMain) {
  const args = process.argv.slice(2);
  const json = args.includes('--json');
  const targets = args.filter((a) => !a.startsWith('--'));
  if (!targets.length) {
    console.log('使い方: kasane-check "src/**/*.html" [--json]\n\nルール:\n' + Object.entries(RULES).map(([k, v]) => `  kasane/${k}\n    ${v}`).join('\n'));
    process.exit(0);
  }
  const files = expand(targets);
  if (!files.length) { console.error('HTML のファイルが見つかりません: ' + targets.join(' ')); process.exit(2); }
  const results = files.map((f) => ({ file: f, warnings: checkHtml(readFileSync(f, 'utf8')) }));
  const total = results.reduce((n, r) => n + r.warnings.length, 0);
  if (json) console.log(JSON.stringify(results, null, 2));
  else {
    for (const r of results) {
      if (!r.warnings.length) continue;
      console.log('\n' + r.file);
      for (const w of r.warnings) console.log(`  ${String(w.line).padStart(4)}:${String(w.column).padEnd(4)} ✖  ${w.text}  ${w.rule}`);
    }
    console.log(total ? `\n✖ ${total} 件(${files.length} ファイル)` : `✓ 問題は見つかりませんでした(${files.length} ファイル)`);
  }
  process.exit(total ? 1 : 0);
}
