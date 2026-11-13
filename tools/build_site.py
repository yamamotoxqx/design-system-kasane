import json, html, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
ROOT = os.path.join(HERE, '..')
OUT = os.path.join(HERE, '.out')
VERSION = 'v1'
# Where v1/ is served from (Cloudflare Workers, see wrangler.jsonc). Override with KASANE_BASE_URL if it moves.
BASE = os.environ.get('KASANE_BASE_URL', 'https://kasane.y-n0.de').rstrip('/') + '/' + VERSION
EMBED = '--embed' in sys.argv
LINT_VER = json.load(open(os.path.join(ROOT, 'lint', 'package.json'), encoding='utf-8'))['version']
LINT_URL = '%s/kasane-lint-%s.tgz' % (BASE, LINT_VER)   # single-file build (fonts and CSS inlined) for previews

esc = html.escape
PAL = json.load(open(os.path.join(OUT, 'palettes.json'), encoding='utf-8'))
PALETTES_CSS = open(os.path.join(OUT, 'kasane-palettes.css'), encoding='utf-8').read()

LUCIDE_DIR = os.path.join(ROOT, 'node_modules', 'lucide-static', 'icons')
LUCIDE_VER = json.load(open(os.path.join(ROOT, 'node_modules', 'lucide-static', 'package.json'), encoding='utf-8'))['version']
LUCIDE_URL = 'https://unpkg.com/lucide-static@%s/icons' % LUCIDE_VER
ICON_STROKE = '2.5'
def icon(name, cls=''):
    """Inline a Lucide icon as one line, with Kasane's stroke width and aria-hidden."""
    svg = open(os.path.join(LUCIDE_DIR, name + '.svg'), encoding='utf-8').read()
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
    svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip()
    head, body = svg.split('>', 1)                       # only strip size attributes from the <svg> tag itself
    svg = re.sub(r' (?:xmlns|width|height)="[^"]*"', '', head) + '>' + body
    svg = svg.replace('stroke-width="2"', 'stroke-width="%s"' % ICON_STROKE)
    svg = svg.replace('class="lucide ', 'class="%slucide ' % (cls + ' ' if cls else ''), 1)
    return svg.replace('<svg ', '<svg aria-hidden="true" ', 1)
I_OK, I_NG, I_WARN, I_INFO = icon('check'), icon('x'), icon('circle-alert'), icon('info')

# ---------------------------------------------------------------- component CSS (single source: used live and shown as sample code)
BASE_CSS = '''/* Kasane components
   Fonts: LINE Seed JP is served from fonts/line-seed-jp.css next to this file (weights 400, 700, 800).
   Zen Maru Gothic 900 and Inter come from Google Fonts:
   <link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"> */
:root {
  --font-body: "LINE Seed JP", "Hiragino Maru Gothic ProN", "Hiragino Sans", "Yu Gothic", Meiryo, sans-serif;
  --font-title: "Zen Maru Gothic", "LINE Seed JP", "Hiragino Maru Gothic ProN", sans-serif;  /* 900, titles only */
  --font-num: "Inter", "LINE Seed JP", system-ui, sans-serif;                                 /* with tabular-nums */
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --text-xs: 12px; --text-sm: 14px; --text-base: 16px; --text-lg: 18px; --text-xl: 24px; --text-2xl: 32px;
  --r-lg: 28px; --r-md: 18px; --r-sm: 14px; --r-full: 999px;
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-5: 24px; --space-6: 32px; --space-7: 56px;
}
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font-family: var(--font-body); font-weight: 400; font-size: var(--text-base); line-height: 1.8;
}
:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
.k-title { font-family: var(--font-title); font-weight: 900; line-height: 1.3; }
.k-num { font-family: var(--font-num); font-variant-numeric: tabular-nums; }
/* Icons are Lucide (https://lucide.dev), drawn at stroke-width 2.5 */
svg.lucide { flex: none; stroke-width: 2.5; }'''

CSS = {}
CSS['button'] = '''.k-btn {
  display: inline-flex; align-items: center; justify-content: center; gap: var(--space-2);
  min-height: 44px; padding: 0 var(--space-5); border: 0; border-radius: var(--r-full);
  background: var(--surface-2); color: var(--ink);
  font: inherit; font-weight: 700; font-size: 15px; cursor: pointer;
  transition: background-color var(--motion-fast), transform var(--motion-fast);
}
.k-btn:hover { background: var(--surface-3); }
.k-btn:active { transform: translateY(1px); }
.k-btn-primary, .k-btn-primary:hover { background: var(--accent); color: var(--on-accent); }
.k-btn-quiet { background: transparent; color: var(--muted); }
.k-btn-quiet:hover { background: var(--surface-2); color: var(--ink); }
.k-btn-danger, .k-btn-danger:hover { background: var(--danger-soft); color: var(--danger); }
.k-btn-sm { min-height: 36px; padding: 0 var(--space-4); font-size: var(--text-sm); }
.k-btn-lg { min-height: 54px; padding: 0 var(--space-6); font-size: 17px; }
.k-btn svg { width: 18px; height: 18px; flex: none; }
.k-btn-icon { width: 44px; padding: 0; }
.k-btn-icon svg { width: 22px; height: 22px; }
.k-btn[disabled] { opacity: .45; cursor: not-allowed; transform: none; }
@media (prefers-reduced-motion: reduce) { .k-btn { transition: none; } }'''

CSS['input'] = '''.k-field { display: flex; flex-direction: column; gap: 6px; font-weight: 700; font-size: var(--text-sm); }
.k-input {
  width: 100%; min-height: 46px; padding: 8px 14px;
  background: var(--surface); color: var(--ink);
  border: 2px solid var(--line); border-radius: var(--r-sm);
  font: inherit; font-weight: 400; font-size: var(--text-base);
}
.k-input::placeholder { color: var(--muted); }
.k-input:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; border-color: var(--ink); }
.k-input[aria-invalid="true"] { border-color: var(--danger); }
.k-hint { font-weight: 400; font-size: 13px; color: var(--muted); }
.k-error { display: flex; align-items: center; gap: 4px; font-size: 13px; color: var(--danger); }
.k-error svg { width: 16px; height: 16px; flex: none; }

.k-select { position: relative; }
.k-select select { appearance: none; -webkit-appearance: none; padding-right: 44px; cursor: pointer; }
.k-select::after {
  content: ""; position: absolute; right: 18px; top: 50%; width: 8px; height: 8px; pointer-events: none;
  border-right: 2.5px solid var(--muted); border-bottom: 2.5px solid var(--muted);
  transform: translateY(-70%) rotate(45deg);
}

.k-option { display: inline-flex; align-items: center; gap: 10px; min-height: 36px; cursor: pointer; }
.k-check {
  appearance: none; -webkit-appearance: none; flex: none; display: grid; place-items: center;
  width: 24px; height: 24px; margin: 0; cursor: pointer;
  background: var(--surface); border: 2px solid var(--line); border-radius: 8px;
}
.k-check:checked { background: var(--accent); border-color: var(--accent); }
.k-check:checked::after {
  content: ""; width: 11px; height: 6px; margin-top: -3px;
  border-left: 3px solid var(--on-accent); border-bottom: 3px solid var(--on-accent);
  transform: rotate(-45deg);
}

.k-radio {
  appearance: none; -webkit-appearance: none; flex: none;
  width: 24px; height: 24px; margin: 0; cursor: pointer;
  background: var(--surface); border: 2px solid var(--line); border-radius: 50%;
}
.k-radio:checked { border-color: var(--accent); background: radial-gradient(circle, var(--on-accent) 0 30%, var(--accent) 34%); }

.k-switch { display: inline-flex; align-items: center; gap: 10px; min-height: 36px; cursor: pointer; }
.k-switch input { position: absolute; opacity: 0; width: 1px; height: 1px; }
.k-switch-track { flex: none; position: relative; width: 50px; height: 30px; border-radius: var(--r-full); background: var(--line); transition: background-color var(--motion-fast); }
.k-switch-track::after {
  content: ""; position: absolute; left: 3px; top: 3px; width: 24px; height: 24px;
  border-radius: 50%; background: var(--surface); transition: transform var(--motion-fast);
}
.k-switch input:checked + .k-switch-track { background: var(--accent); }
.k-switch input:checked + .k-switch-track::after { transform: translateX(20px); background: var(--on-accent); }
.k-switch input:focus-visible + .k-switch-track { outline: 3px solid var(--focus); outline-offset: 3px; }
@media (prefers-reduced-motion: reduce) { .k-switch-track, .k-switch-track::after { transition: none; } }'''

CSS['card'] = '''.k-card {
  display: flex; flex-direction: column; gap: var(--space-3);
  background: var(--surface); border-radius: var(--r-lg); padding: var(--space-5);
}
.k-card-title { margin: 0; font-size: var(--text-lg); font-weight: 800; line-height: 1.5; }
.k-card-text { margin: 0; font-size: 15px; color: var(--muted); }
.k-list { display: flex; flex-direction: column; gap: 6px; margin: 0; padding: 0; list-style: none; }
.k-list-item {
  display: flex; align-items: center; gap: var(--space-3);
  background: var(--surface-2); border-radius: var(--r-md); padding: var(--space-3) var(--space-4);
}
.k-list-item-main { flex: 1; min-width: 0; font-weight: 700; }
.k-list-item-sub { font-size: 13px; color: var(--muted); }
.k-nest { background: var(--surface-2); border-radius: var(--r-md); padding: var(--space-4); }
.k-notice {
  display: flex; flex-direction: column; gap: var(--space-2);
  background: var(--surface-2); border-radius: var(--r-lg); padding: 22px;
}
.k-notice-title { margin: 0; font-size: var(--text-lg); font-weight: 800; line-height: 1.5; color: var(--notice-head); }'''

CSS['badge'] = '''.k-badge {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 2px 12px; border-radius: var(--r-full);
  background: var(--surface-3); color: var(--ink);
  font-size: 13px; font-weight: 700; line-height: 1.7;
}
.k-badge svg { width: 14px; height: 14px; flex: none; margin-left: -3px; }
.k-badge-accent { background: var(--accent-soft); color: var(--accent-ink); }
.k-badge-ok { background: var(--ok-soft); color: var(--ok); }
.k-badge-danger { background: var(--danger-soft); color: var(--danger); }
.k-badge-info { background: var(--info-soft); color: var(--info); }'''

CSS['tabs'] = '''.k-seg {
  position: relative; isolation: isolate;
  display: inline-grid; grid-auto-flow: column; grid-auto-columns: 1fr; gap: 2px;
  padding: 4px; border-radius: var(--r-full); background: var(--surface-2);
}
.k-seg button {
  min-height: 36px; padding: 6px var(--space-4); border: 0; border-radius: var(--r-full);
  background: transparent; color: var(--muted);
  font: inherit; font-weight: 700; font-size: var(--text-sm); cursor: pointer; white-space: nowrap;
  transition: color var(--motion-fast);
}
.k-seg button:hover { color: var(--ink); }
.k-seg button[aria-selected="true"], .k-seg button[aria-pressed="true"] { background: var(--surface); color: var(--ink); }

/* Sliding thumb: the selected background moves like a switch (up to 5 items, browsers with :has) */
@supports selector(:has(*)) {
  .k-seg { --n: 1; --i: 0; }
  .k-seg:has(> :nth-child(2):last-child) { --n: 2; }
  .k-seg:has(> :nth-child(3):last-child) { --n: 3; }
  .k-seg:has(> :nth-child(4):last-child) { --n: 4; }
  .k-seg:has(> :nth-child(5):last-child) { --n: 5; }
  .k-seg:has(> :nth-child(2)[aria-selected="true"], > :nth-child(2)[aria-pressed="true"]) { --i: 1; }
  .k-seg:has(> :nth-child(3)[aria-selected="true"], > :nth-child(3)[aria-pressed="true"]) { --i: 2; }
  .k-seg:has(> :nth-child(4)[aria-selected="true"], > :nth-child(4)[aria-pressed="true"]) { --i: 3; }
  .k-seg:has(> :nth-child(5)[aria-selected="true"], > :nth-child(5)[aria-pressed="true"]) { --i: 4; }
  .k-seg::before {
    content: ""; position: absolute; z-index: -1; top: 4px; bottom: 4px; left: 4px;
    width: calc((100% - 8px - (var(--n) - 1) * 2px) / var(--n));
    border-radius: var(--r-full); background: var(--surface);
    transform: translateX(calc(var(--i) * (100% + 2px)));
    transition: transform var(--motion-base) var(--ease-out);
    opacity: 0;
  }
  .k-seg:has(> [aria-selected="true"], > [aria-pressed="true"])::before { opacity: 1; }
  .k-seg button[aria-selected="true"], .k-seg button[aria-pressed="true"] { background: transparent; }
}
@media (prefers-reduced-motion: reduce) { .k-seg::before, .k-seg button { transition: none; } }'''

CSS['progress'] = '''.k-bar { height: 14px; border-radius: var(--r-full); background: var(--surface-2); overflow: hidden; }
.k-bar > i { display: block; height: 100%; border-radius: var(--r-full); background: var(--accent); }
.k-bar-head { display: flex; justify-content: space-between; font-size: var(--text-sm); font-weight: 700; }'''

CSS['dialog'] = '''.k-scrim {
  position: fixed; inset: 0; z-index: 10; display: grid; place-items: center; padding: var(--space-4);
  background: rgba(0, 0, 0, .5);
  animation: k-fade var(--motion-base);
}
.k-dialog {
  display: flex; flex-direction: column; gap: var(--space-3);
  width: 100%; max-width: 420px; padding: 28px;
  background: var(--surface); border-radius: var(--r-lg);
  animation: k-enter var(--motion-base) var(--ease-out);
}
.k-dialog-title { margin: 0; font-size: 20px; font-weight: 800; line-height: 1.5; }
.k-dialog-text { margin: 0; font-size: 15px; color: var(--muted); }
.k-dialog-actions { display: flex; justify-content: flex-end; flex-wrap: wrap; gap: var(--space-2); margin-top: var(--space-3); }
.k-toast {
  position: fixed; left: 50%; bottom: 24px; z-index: 11; transform: translateX(-50%);
  padding: 12px 22px; border-radius: var(--r-full);
  background: var(--ink); color: var(--bg); font-weight: 700; font-size: 15px;
}
@media (prefers-reduced-motion: reduce) { .k-scrim, .k-dialog { animation: none; } }'''

CSS['motion'] = '''/* Motion: short and quiet */
:root { --motion-fast: 150ms; --motion-base: 220ms; --motion-slow: 450ms; --ease-out: cubic-bezier(.2, .7, .3, 1); }
@keyframes k-enter { from { opacity: 0; transform: translateY(16px); } }
@keyframes k-fade { from { opacity: 0; } }
.k-enter { animation: k-enter var(--motion-slow) var(--ease-out); }
@media (prefers-reduced-motion: reduce) { .k-enter { animation: none; } }'''

def _palette_css():
    rules = ['''.k-palette { margin: 0; padding: 0; border: 0; min-width: 0; }
.k-palette legend { padding: 0; margin-bottom: var(--space-2); font-weight: 700; font-size: var(--text-sm); }
.k-palette-items { display: flex; flex-wrap: wrap; gap: var(--space-2); }
.k-palette-item {
  position: relative; display: inline-flex; align-items: center; gap: var(--space-2);
  min-height: 44px; padding: 0 var(--space-4) 0 var(--space-2); border-radius: var(--r-full);
  background: var(--surface-2); font-weight: 700; font-size: var(--text-sm); cursor: pointer;
}
.k-palette-item:hover { background: var(--surface-3); }
.k-palette-item input { position: absolute; opacity: 0; width: 1px; height: 1px; }
.k-palette-swatch { flex: none; display: grid; place-items: center; width: 28px; height: 28px; border-radius: 50%; background: var(--sw); }
.k-palette-item input:checked ~ .k-palette-swatch::after {
  content: ""; width: 11px; height: 6px; margin-top: -3px;
  border-left: 3px solid var(--sw-on); border-bottom: 3px solid var(--sw-on); transform: rotate(-45deg);
}
.k-palette-item:has(input:checked) { background: var(--accent-soft); color: var(--accent-ink); }
.k-palette-item input:focus-visible ~ .k-palette-swatch { outline: 3px solid var(--focus); outline-offset: 3px; }
/* Compact: swatches only, for a page footer. The name stays for screen readers. */
.k-palette-compact .k-palette-items { gap: var(--space-1); }
.k-palette-compact .k-palette-item, .k-palette-compact .k-palette-item:has(input:checked) { min-width: 44px; padding: 0; justify-content: center; background: transparent; }
.k-palette-compact .k-palette-name { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
/* Each swatch shows its own palette's accent (light / dark) */''']
    light = ''.join('.k-palette-swatch[data-swatch="%s"] { --sw: %s; --sw-on: %s; }\n' % (p['id'], p['light']['--accent'], p['light']['--on-accent']) for p in PAL)
    dark = ''.join('.k-palette-swatch[data-swatch="%s"] { --sw: %s; --sw-on: %s; }\n' % (p['id'], p['dark']['--accent'], p['dark']['--on-accent']) for p in PAL)
    rules.append(light.rstrip())
    rules.append('@media (prefers-color-scheme: dark) {\n' + dark.replace('.k-palette-swatch', ':root:not([data-theme="light"]) .k-palette-swatch').rstrip() + '\n}')
    rules.append(dark.replace('.k-palette-swatch', ':root[data-theme="dark"] .k-palette-swatch').rstrip())
    return '\n'.join(rules)
CSS['palette'] = _palette_css()

COMPONENTS_CSS = BASE_CSS + '\n\n/* Button */\n' + CSS['button'] + '\n\n/* Input, checkbox, switch */\n' + CSS['input'] + '\n\n/* Card and list */\n' + CSS['card'] + '\n\n/* Badge */\n' + CSS['badge'] + '\n\n/* Segmented control, tabs */\n' + CSS['tabs'] + '\n\n/* Progress bar */\n' + CSS['progress'] + '\n\n/* Dialog and toast */\n' + CSS['dialog'] + '\n\n/* Palette picker */\n' + CSS['palette'] + '\n\n' + CSS['motion'] + '\n'

# ---------------------------------------------------------------- distributable files
HEADER = '/*! Kasane %s — design tokens and components. Docs: index.html / kasane.md */\n' % VERSION
FULL_CSS = HEADER + '\n/* ================= Palettes (colour tokens) ================= */\n' + PALETTES_CSS + '\n/* ================= Shared tokens and components ================= */\n' + COMPONENTS_CSS
def minify(c):
    keep = HEADER.strip()
    c = re.sub(r'/\*.*?\*/', '', c, flags=re.S)
    c = re.sub(r'\s+', ' ', c)
    c = re.sub(r'\s*([{}:;,>])\s*', r'\1', c)
    c = c.replace(';}', '}')
    return keep + '\n' + c.strip() + '\n'
os.makedirs(os.path.join(ROOT, VERSION), exist_ok=True)
# @charset first: a page in another encoding (e.g. Shift_JIS) still reads the Japanese in this file correctly
CHARSET = '@charset "UTF-8";\n'
open(os.path.join(ROOT, VERSION, 'kasane.css'), 'w', encoding='utf-8').write(CHARSET + FULL_CSS)
open(os.path.join(ROOT, VERSION, 'kasane.min.css'), 'w', encoding='utf-8').write(CHARSET + minify(FULL_CSS))

# Data for the HTML check: Kasane class names and Lucide icon names
k_classes = sorted(set(re.findall(r'\.(k-[a-z0-9-]+)', FULL_CSS)))
json.dump(k_classes, open(os.path.join(ROOT, 'lint', 'data', 'classes.json'), 'w', encoding='utf-8'), indent=0)
lucide_names = sorted(f[:-4] for f in os.listdir(LUCIDE_DIR) if f.endswith('.svg'))
json.dump({'version': LUCIDE_VER, 'names': lucide_names}, open(os.path.join(ROOT, 'lint', 'data', 'lucide.json'), 'w', encoding='utf-8'), separators=(',', ':'))

# Design tokens in the W3C Design Tokens Community Group format
def tok(v, t='color'): return {'$type': t, '$value': v}
tokens = {'$description': 'Kasane %s design tokens' % VERSION, 'palette': {}, 'radius': {}, 'space': {}, 'fontSize': {}, 'fontFamily': {}, 'duration': {}}
for p in PAL:
    tokens['palette'][p['id']] = {'$description': '%s (%s)' % (p['name'], p['en']),
        'light': {k[2:]: tok(v) for k, v in p['light'].items()}, 'dark': {k[2:]: tok(v) for k, v in p['dark'].items()}}
for k, v in (('lg', 28), ('md', 18), ('sm', 14), ('full', 999)): tokens['radius'][k] = tok('%dpx' % v, 'dimension')
for i, v in enumerate((4, 8, 12, 16, 24, 32, 56)): tokens['space'][str(i + 1)] = tok('%dpx' % v, 'dimension')
for k, v in (('xs', 12), ('sm', 14), ('base', 16), ('lg', 18), ('xl', 24), ('2xl', 32)): tokens['fontSize'][k] = tok('%dpx' % v, 'dimension')
tokens['fontFamily'] = {'body': tok(['LINE Seed JP', 'sans-serif'], 'fontFamily'), 'title': tok(['Zen Maru Gothic', 'sans-serif'], 'fontFamily'), 'num': tok(['Inter', 'sans-serif'], 'fontFamily')}
tokens['duration'] = {'fast': tok('150ms', 'duration'), 'base': tok('220ms', 'duration'), 'slow': tok('450ms', 'duration')}
json.dump(tokens, open(os.path.join(ROOT, VERSION, 'tokens.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# Rules and spec for AI tools and people
def spec(tpl):
    return open(tpl, encoding='utf-8').read().replace('{{BASE}}', BASE).replace('{{VERSION}}', VERSION).replace('{{LINT_URL}}', LINT_URL).replace('{{SITE}}', BASE.rsplit('/', 1)[0]).replace('{{LUCIDE_VER}}', LUCIDE_VER).replace('{{LUCIDE_URL}}', LUCIDE_URL)
md = spec('kasane.md.tpl')
open(os.path.join(ROOT, VERSION, 'kasane.md'), 'w', encoding='utf-8').write(md)
# English edition: same content, fewer tokens for AI tools
open(os.path.join(ROOT, VERSION, 'kasane.en.md'), 'w', encoding='utf-8').write(spec('kasane.en.md.tpl'))
open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8').write(
    '# Kasane\n\n> A design system for websites and web apps: surfaces are layered to separate content, and the accent colour is chosen from 9 palettes. '
    '面を重ねて区切り、アクセントの色を9色から選べるデザインシステム。\n\n'
    'Before building UI, read one of the specs below to the end. The English edition uses fewer tokens; both say the same thing.\n\n'
    '- [Kasane %s spec (English)](%s/kasane.en.md): rules, tokens, HTML for every component, end-of-work checklist\n'
    '- [Kasane %s 仕様書(日本語)](%s/kasane.md): 同じ内容の日本語版\n'
    '- [kasane.css](%s/kasane.css): all tokens and component CSS\n'
    '- [tokens.json](%s/tokens.json): token values (W3C Design Tokens format)\n'
    '- [Source](https://github.com/yamamotoxqx/design-system-kasane): GitHub repository (MIT License)\n' % (VERSION, BASE, VERSION, BASE, BASE, BASE))

# ---------------------------------------------------------------- helpers
CODE_FOLD = 14   # longer code starts folded, with a button to show all of it
def code(lang, src):
    src = src.strip('\n'); n = src.count('\n') + 1
    if n <= CODE_FOLD:
        return ('<div class="code"><div class="code-head"><span>%s</span><button class="copy" type="button">コピー</button></div>'
                '<pre><code>%s</code></pre></div>') % (lang, esc(src))
    return ('<div class="code long"><div class="code-head"><span>%s <small>%d行</small></span><button class="copy" type="button">コピー</button></div>'
            '<pre><code>%s</code></pre><button class="code-more" type="button" aria-expanded="false">すべて表示</button></div>') % (lang, n, esc(src))

def ex(src, stack=False):
    """Live demo + the same HTML as sample code."""
    return '<div class="ex"><div class="ex-demo%s">%s</div>%s</div>' % (' ex-stack' if stack else '', src, code('HTML', src))

def dd(do_html, do_text, dont_html, dont_text):
    return ('<div class="dd"><figure class="dd-item dd-do"><div class="dd-demo">%s</div><figcaption class="dd-cap"><span class="dd-label">%sDo</span>%s</figcaption></figure>'
            '<figure class="dd-item dd-dont"><div class="dd-demo">%s</div><figcaption class="dd-cap"><span class="dd-label">%sDon\'t</span>%s</figcaption></figure></div>') % (do_html, I_OK, do_text, dont_html, I_NG, dont_text)

def palette_src(name='accent', compact=False, legend='テーマカラー', selected='yamabuki'):
    """The colour picker as readable sample code, all 9 palettes."""
    items = ''.join('    <label class="k-palette-item">\n      <input type="radio" name="%s" value="%s"%s>\n      <span class="k-palette-swatch" data-swatch="%s"></span>\n      <span class="k-palette-name">%s</span>\n    </label>\n'
                    % (name, p['id'], ' checked' if p['id'] == selected else '', p['id'], p['name']) for p in PAL)
    return '<fieldset class="k-palette%s">\n  <legend>%s</legend>\n  <div class="k-palette-items">\n%s  </div>\n</fieldset>' % (' k-palette-compact' if compact else '', legend, items)

def palette_html(name='accent', compact=False, legend='テーマカラー', selected='yamabuki', ids=None):
    items = ''.join('<label class="k-palette-item"><input type="radio" name="%s" value="%s"%s><span class="k-palette-swatch" data-swatch="%s"></span><span class="k-palette-name">%s</span></label>'
                    % (name, p['id'], ' checked' if p['id'] == selected else '', p['id'], p['name']) for p in PAL if not ids or p['id'] in ids)
    return '<fieldset class="k-palette%s"><legend>%s</legend><div class="k-palette-items">%s</div></fieldset>' % (' k-palette-compact' if compact else '', legend, items)

def table_fixed(widths, head, rows):
    # fixed column widths: the table keeps its size while fonts load
    cols = '<colgroup>%s</colgroup>' % ''.join('<col style="width:%s">' % w for w in widths)
    return table(head, rows).replace('<table>', '<table class="fixed">' + cols, 1)

def table(head, rows):
    return '<div class="tbl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
        ''.join('<th>%s</th>' % h for h in head), ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in rows))

NAV = [
    ('intro', 'はじめに', [('about', 'Kasane とは'), ('start', '使い始める'), ('integrate', '組み込み方と使用例'), ('with-ai', 'AI と使う'), ('updates', '更新情報')]),
    ('principle', '原則', [('principles', 'デザイン原則'), ('accessibility', 'アクセシビリティ'), ('performance', 'パフォーマンス'), ('writing', '文章'), ('i18n', '多言語対応')]),
    ('style', 'スタイル', [('color', 'カラー'), ('typography', 'タイポグラフィ'), ('shape', '角丸と余白'), ('layout', 'レイアウト'), ('icons', 'アイコン'), ('motion', '動き')]),
    ('component', 'コンポーネント', [('button', 'ボタン'), ('input', '入力欄'), ('card', 'カードとリスト'), ('badge', 'バッジ'), ('tabs', 'タブ'), ('progress', '進捗バー'), ('dialog', 'ダイアログとトースト')]),
]
SEC_OF = {pid: label for _, label, pages in NAV for pid, _ in pages}
TITLE_OF = {pid: t for _, _, pages in NAV for pid, t in pages}

PAGES = []
TOCS = []
ART, TOC_OF, LEAD_OF = {}, {}, {}   # per page, for the one-file-per-URL site
FLAT = [(pid, t) for _, _, pages in NAV for pid, t in pages]
def page(pid, lead, body):
    # give every section an id, and build this page's on-this-page list and pager at build time
    n = [0]
    def add_id(m):
        n[0] += 1
        return m.group(0) if 'id=' in m.group(0) else '<section class="sec" id="%s-s%d">' % (pid, n[0])
    body = re.sub(r'<section class="sec"[^>]*>', add_id, body)
    toc = ''.join('<button type="button" data-scroll="%s">%s</button>' % (sid, re.sub(r'<[^>]+>', '', h2).strip())
                  for sid, h2 in re.findall(r'<section class="sec" id="([^"]+)"><h2>(.*?)</h2>', body))
    TOCS.append('<nav class="toc-page" data-page="%s" aria-label="このページの目次"><div class="toc-title">このページの内容</div>%s</nav>' % (pid, toc))
    TOC_OF[pid] = TOCS[-1]; LEAD_OF[pid] = lead
    i = [p for p, _ in FLAT].index(pid)
    pager = ''
    if i > 0: pager += '<a class="prev" href="#%s"><small>前のページ</small>%s</a>' % FLAT[i - 1]
    if i < len(FLAT) - 1: pager += '<a class="next" href="#%s"><small>次のページ</small>%s</a>' % FLAT[i + 1]
    PAGES.append('<article class="page" data-page="%s"><div class="page-head"><div class="crumbs">%s / %s</div><h1>%s</h1><p class="lead">%s</p></div>%s<nav class="pager" aria-label="前後のページ">%s</nav></article>'
                 % (pid, SEC_OF[pid], TITLE_OF[pid], TITLE_OF[pid], lead, body, pager))
    ART[pid] = PAGES[-1]

def sec(title, body):
    return '<section class="sec"><h2>%s</h2>%s</section>' % (title, body)

# ---------------------------------------------------------------- pages
def _lv(name, tok, inner=''):
    return ('<div class="lv" style="background:var(%s)"><div class="lv-h"><b>%s <code>%s</code></b><span class="lv-val" data-token="%s">%s</span></div>%s</div>'
            % (tok, name, tok[2:], tok, PAL[0]['light'][tok], inner))
def _chip(name, tok):
    return ('<div class="lv-chip"><i style="background:var(%s)"></i><b>%s <code>%s</code></b><span class="lv-val" data-token="%s">%s</span></div>'
            % (tok, name, tok[2:], tok, PAL[0]['light'][tok]))
LAYER_VIZ = ('<div class="layer-viz"><figure class="lv-panel"><figcaption>面の重なり</figcaption>'
             + _lv('背景', '--bg', _lv('カード', '--surface', _lv('中の面', '--surface-2', _lv('押したとき', '--surface-3'))))
             + '<p class="lv-note">ページ → カード → カードの中の行 → 押したとき、の順に一段ずつ変わります。</p></figure>'
             '<figure class="lv-panel"><figcaption>文字とアクセント</figcaption><div class="lv-chips">'
             + ''.join(_chip(n, t) for n, t in [('文字', '--ink'), ('補足', '--muted'), ('アクセント', '--accent'), ('アクセント文字', '--accent-ink'),
                                                ('アクセント薄', '--accent-soft'), ('入力欄の枠', '--line')])
             + '</div></figure></div>')

# "このサイトの構成" on the about page: same order as the sidebar and the footer (built from NAV)
SITEMAP_DESC = {
    'start': 'CSSの読み込みと、色の決め方',
    'integrate': '既定の色の決め方、利用者が色を変える場所、パレットごとの使用例',
    'with-ai': 'Claude Code などに Kasane のルールを渡す方法と、自動チェック',
    'updates': 'Kasane の変更の記録',
    'principle': '設計の考え方、アクセシビリティ、パフォーマンス、文章の書き方',
    'style': 'カラー、タイポグラフィ、角丸と余白、レイアウト、アイコン、動き',
    'component': '部品の見本とサンプルコード',
}
SITEMAP = [(p, t) for p, t in NAV[0][2] if p != 'about'] + [(ps[0][0], label) for _, label, ps in NAV[1:]]
SITEMAP_DESC.update({ps[0][0]: SITEMAP_DESC[sid] for sid, _, ps in NAV[1:]})

FEAT_SW = ''.join('<button class="feat-sw" type="button" data-accent-set="%s" aria-pressed="false" aria-label="%s" style="background:%s"></button>' % (p['id'], p['name'], p['light']['--accent']) for p in PAL)
FEAT_CHECKS = ''.join('<li>%s<span>%s</span><b class="k-num">%s</b></li>' % (I_OK, a_, b_) for a_, b_ in
                      [('CSS のルール(Stylelint)', '0件'), ('HTML のルール(kasane-check)', '0件'), ('画像の画質(SSIM)', '0.99以上'), ('Lighthouse', '最低点クリア')])
page('about', 'Kasane(かさね)は、Webサイトと Webアプリのためのデザインシステムです。面を重ねて情報を区切り、アクセントの色を9色から選べます。',
  sec('ひと目でわかる Kasane', '<p>Kasane の画面は、枠や影ではなく、面の色の差でできています。外側から背景、カード、中の面と、一段ずつ色が変わります。色は、いま表示しているパレットとテーマのものです。</p>' + LAYER_VIZ)
  + sec('特徴', '<div class="cards two">'
        '<div class="tile feat"><div class="feat-vis" aria-hidden="true"><div class="fv-card"><b>今週の予定</b><span class="fv-row">図書館の本を返す</span><span class="fv-row">資料を見直す</span></div></div>'
        '<h3>枠も影も使わない</h3><p>カードやリストは、面の色の差だけで区切ります。枠を持つのは入力欄だけです。</p></div>'
        '<div class="tile feat"><div class="feat-vis feat-sws" role="group" aria-label="アクセントの色">' + FEAT_SW + '</div>'
        '<h3>9色から選べる</h3><p>押すと、このサイトの色が変わります。どの色でも、文字の読みやすさは同じ基準を守ります。</p></div>'
        '<div class="tile feat"><div class="feat-vis feat-code" aria-hidden="true"><code>&lt;link rel="stylesheet"<br>&nbsp; href="…/v1/kasane.min.css"&gt;</code></div>'
        '<h3>CSSだけで使える</h3><p>トークンと部品は1つのCSSファイルで、URLから読み込めます。ビルドや JavaScript のライブラリは要りません。</p></div>'
        '<div class="tile feat"><div class="feat-vis"><ul class="feat-checks" aria-label="自動チェックの結果の例">' + FEAT_CHECKS + '</ul></div>'
        '<h3>AI だけでも品質を保てる</h3><p>自動チェックを充実させているので、AI だけでコーディングしても十分な品質を保てます。CSS と HTML のルール、画像の画質、Lighthouse の点数を機械で確かめ、見つかった問題は AI が自分で直します。<a href="#with-ai">AI と使う</a></p></div></div>')
  + sec('名前の由来', '<p>「かさね」には2つの意味があります。1つは、背景・カード・中の面と、面を重ねて画面を組み立てること。もう1つは、色の組み合わせを楽しむ「襲(かさね)の色目」です。パレットの名前も、山吹、藤、藍など日本の色の名前から取っています。</p>')
  + sec('このサイトの構成', '<ul class="site-map">' + ''.join(
        '<li><a href="#%s"><span class="sm-text"><b>%s</b><span>%s</span></span>%s</a></li>' % (pid, label, SITEMAP_DESC[pid], icon('chevron-right', 'go'))
        for pid, label in SITEMAP) + '</ul>'))

page('start', 'CSSを読み込み、<code>&lt;html&gt;</code> に色の名前を付けるだけで使えます。ファイルはURLで配信しているので、手元に置く必要はありません。',
  sec('1. CSSと書体を読み込む', '<p><code>kasane.css</code> に、色のトークン(9色)、書体・角丸・余白のトークン、部品のスタイルがすべて入っています。軽い縮小版の <code>kasane.min.css</code> もあります。</p>'
      + code('HTML', '<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">\n<link rel="stylesheet" href="' + BASE + '/fonts/line-seed-jp.css">\n<link rel="stylesheet" href="' + BASE + '/kasane.min.css">')
      + '<p>URLの <code>' + VERSION + '</code> は版の番号です。見た目が大きく変わる更新は新しい版として出すので、同じURLを使っている限り、見た目が急に変わることはありません。</p>')
  + sec('2. アクセントの色を選ぶ', '<p><code>data-accent</code> にパレットの名前を書きます。書かなければ山吹になります。使える名前は <a href="#color">カラー</a> のページにあります。</p>'
      + code('HTML', '<html lang="ja" data-accent="ai">'))
  + sec('3. ライトとダークは端末に任せる', '<p>何も指定しなければ、端末の設定(<code>prefers-color-scheme</code>)に従います。製品には、ライトとダークの切り替えボタンを置きません。利用者が変えられるのは色だけにします。</p>'
      + '<p><code>data-theme</code> に <code>light</code> か <code>dark</code> を書くと固定できますが、画面の確認やこのサイトの見本のためのものです。</p>')
  + sec('4. 利用者が色を変えられるようにする', '<p>色を変えられるようにするなら、設定ページか、ページ下部に色の選択を置きます。選んだ色は保存して、次に開いたとき <code>&lt;head&gt;</code> の先頭で、CSSより前に適用します。こうすると、別の色が一瞬見えるちらつきを防げます。置き方と見本は <a href="#integrate">組み込み方と使用例</a> にあります。</p>'
      + code('HTML', '<head>\n  <script>\n    try {\n      var a = localStorage.getItem("kasane-accent");\n      if (a) document.documentElement.dataset.accent = a;\n    } catch (e) {}\n  </script>\n  <link rel="stylesheet" href="' + BASE + '/kasane.min.css">\n</head>'))
  + sec('5. 部品を使う', '<p>部品はクラスを付けるだけで使えます。独自の部品を作るときは、色を直接書かずにトークンを参照します。</p>'
      + ex('<button class="k-btn k-btn-primary" type="button">保存する</button>\n<button class="k-btn" type="button">下書き</button>')
      + code('CSS', '.my-banner {\n  background: var(--accent-soft);\n  color: var(--accent-ink);\n  border-radius: var(--r-md);\n  padding: var(--space-4);\n}')))

PR = [('layers', '面を重ねて区切る', '枠線や影を使わず、面の色の差だけでまとまりを作ります。'),
      ('pcolor', '色は選べる、読みやすさは変えない', 'アクセントは9色から選べます。文字の読みやすさは全色で同じ基準を守ります。'),
      ('beyond', '色だけで伝えない', '状態や選択は、アイコン、文字、位置を組み合わせて伝えます。'),
      ('soft', 'やわらかく、はっきり', '角は丸く、押せる場所は大きく。操作できる場所が迷わず分かるようにします。'),
      ('type', '書体は役割で分ける', '基本は LINE Seed JP。例外はタイトルと、桁をそろえたい数字だけです。')]
page('principles', 'どの色を選んでも同じ使い心地になるように、5つの原則を決めています。',
  sec('5つの原則', '<div class="cards two">' + ''.join('<button class="tile tile-link" type="button" data-scroll="%s"><span class="num-tag">%d</span><h3>%s</h3><p>%s</p></button>' % (k, i + 1, t, d) for i, (k, t, d) in enumerate(PR)) + '</div>')
  + '<section class="sec" id="layers"><h2><span class="num-tag">1</span>面を重ねて区切る</h2><p>背景、カード、中の面と、内側に入るほど面の色を一段ずつ変えます。枠を持つのは入力欄だけです。入力欄は「書き込める場所」だと一目で分かる必要があるためです。</p>'
  + dd('<div class="k-card mini"><b>今週のやること</b><ul class="k-list"><li class="k-list-item">図書館の本を返す</li><li class="k-list-item">発表スライドの確認</li></ul></div>',
       'カードは <code>--surface</code>、中の行は <code>--surface-2</code> の面で区切ります。',
       '<div class="k-card mini" style="border:1px solid var(--line);box-shadow:0 6px 16px rgba(0,0,0,.18)"><b>今週のやること</b><div style="border-top:1px solid var(--line);padding-top:8px">図書館の本を返す</div><div style="border-top:1px solid var(--line);padding-top:8px">発表スライドの確認</div></div>',
       '枠線、影、区切り線でカードやリストを区切りません。') + '</section>'
  + '<section class="sec" id="pcolor"><h2><span class="num-tag">2</span>色は選べる、読みやすさは変えない</h2><p>色は必ずトークンで指定します。塗りには <code>--accent</code>、その上の文字には <code>--on-accent</code>、アクセント色の文字やリンクには <code>--accent-ink</code> を使います。こうすると、どのパレットでも文字は4.5:1以上のコントラストになります。</p>'
  + dd('<div class="stack"><button class="k-btn k-btn-primary" type="button">保存する</button><span class="a-ink">詳しく見る</span></div>', '塗りと文字で、別のトークンを使い分けます。',
       '<div class="stack"><span class="k-btn bad-on-accent" role="img" aria-label="悪い例: 読みにくい色の保存ボタン" data-label="保存する"></span><span class="bad-link" role="img" aria-label="悪い例: 読みにくい色のリンク" data-label="詳しく見る"></span></div>',
       '塗りの上の文字を白などに決め打ちしたり、塗り用の <code>--accent</code> を文字に使ったりしません。パレットやテーマによっては読めなくなります。') + '</section>'
  + '<section class="sec" id="beyond"><h2><span class="num-tag">3</span>色だけで伝えない</h2><p>成功は緑、エラーは赤で固定していますが、色の見え方は人や画面によって変わります。状態にはアイコンと文字を必ず添えます。チェックは印、スイッチはつまみの位置でも状態が分かるようにします。</p>'
  + dd('<div class="inline"><span class="k-badge k-badge-ok">%s保存しました</span><span class="k-badge k-badge-danger">%s送信できません</span></div>' % (I_OK, I_WARN), '色に加えて、アイコンと文字で状態を伝えます。',
       '<div class="inline" style="gap:20px"><span class="dot"><i style="background:var(--ok)"></i>田中さん</span><span class="dot"><i style="background:var(--danger)"></i>佐藤さん</span></div>',
       '色のついた丸だけで状態を表しません。何を意味するのかが伝わりません。') + '</section>'
  + '<section class="sec" id="soft"><h2><span class="num-tag">4</span>やわらかく、はっきり</h2><p>カードは28px、中の面は18px、入力欄は14pxの角丸にし、ボタンは丸薬型にします。押せる場所は高さ44px以上を基本にし、キーボードで操作したときはフォーカスのリングを必ず表示します。</p>'
  + dd('<button class="k-btn k-btn-primary" type="button">予約する</button>', '丸薬型で高さ44px。指でも押しやすい大きさです。',
       '<button class="k-btn k-btn-primary" type="button" style="min-height:24px;padding:0 8px;font-size:11px;border-radius:2px">予約する</button>',
       '小さく角ばったボタンにしません。<code>outline: none</code> でフォーカスのリングを消すのも避けます。') + '</section>'
  + '<section class="sec" id="type"><h2><span class="num-tag">5</span>書体は役割で分ける</h2><p>基本の書体は LINE Seed JP です。例外は2つだけで、ページのタイトルと章の見出しは Zen Maru Gothic の極太、桁をそろえたい数字は Inter の等幅数字にします。くわしくは <a href="#typography">タイポグラフィ</a> にあります。</p>'
  + dd('<div class="k-card mini"><b>今月の支出</b><div class="k-num" style="text-align:right;line-height:1.7">1,280<br>12,400<br>980</div></div>', '縦に並ぶ数字は <code>.k-num</code> で桁をそろえます。',
       '<div class="k-card mini"><b>今月の支出</b><div style="text-align:right;line-height:1.7">1,280<br>12,400<br>980</div></div>', '数字の列を基本の書体のままにしません。桁の位置がずれて比べにくくなります。') + '</section>')

# accessibility and performance pages live in pages_extra.py

pal_btns = ''.join('<button class="pal" type="button" data-accent-set="%s" aria-pressed="false"><i style="background:linear-gradient(135deg,%s 50%%,%s 50%%)"></i><b>%s</b><small>%s</small></button>' % (p['id'], p['light']['--accent'], p['dark']['--accent'], p['name'], p['id']) for p in PAL)
TOKENS = [('--bg', 'ページの背景'), ('--surface', 'カード、パネル'), ('--surface-2', '中の面、リストの行、通常のボタン'), ('--surface-3', 'ホバー、押下'),
          ('--ink', '文字'), ('--muted', '補足の文字'), ('--line', '入力欄の枠、スイッチのオフ'),
          ('--accent', 'アクセントの塗り(主ボタン、チェック、スイッチのオン)'), ('--on-accent', 'アクセントの塗りの上の文字'),
          ('--accent-soft', '薄いアクセントの面'), ('--accent-ink', 'アクセント色の文字、リンク'), ('--focus', 'フォーカスのリング'),
          ('--ok', '成功の文字'), ('--ok-soft', '成功の面'), ('--danger', 'エラー・削除の文字'), ('--danger-soft', 'エラー・削除の面'),
          ('--info', '情報の文字'), ('--info-soft', '情報の面')]
page('color', '色はすべてトークンで指定します。アクセントは9色のパレットから選べて、ライトとダークの値はパレットごとに決まっています。',
  sec('パレット', '<p>押すと、このサイト全体の色が切り替わります。<code>data-accent</code> には、下の英字の名前を書きます。</p><div class="pals">' + pal_btns + '</div>'
      + code('HTML', '<html data-accent="yamabuki">').replace('&quot;yamabuki&quot;', '&quot;<span data-accent-code>yamabuki</span>&quot;'))
  + sec('面の重なり', '<p>Kasane は枠や影を使わず、面の色の差で区切ります。内側に入るほど、面の色を一段ずつ変えます。下の値は、いま表示しているパレットとテーマのものです。</p>' + LAYER_VIZ)
  + sec('トークンの一覧', '<p>値は、いま表示しているパレットとテーマのものです。</p>'
      + table_fixed(['32%', '43%', '25%'], ['トークン', '用途', 'いまの値'], [['<code>%s</code>' % k, d, '<span class="sw"><i style="background:var(%s)"></i><span data-token="%s">%s</span></span>' % (k, k, PAL[0]['light'][k])] for k, d in TOKENS]))
  + sec('アクセントの使い分け', '<p>アクセントには、塗り用と文字用の2つのトークンがあります。黄色や水色のような明るい色は、そのまま文字にすると読めないためです。</p>'
      + code('CSS', '.button-primary { background: var(--accent); color: var(--on-accent); }\n.link           { color: var(--accent-ink); }\n.highlight      { background: var(--accent-soft); color: var(--accent-ink); }'))
  + sec('状態の色', '<p>成功は緑、エラーは赤、情報は落ち着いた青灰色で、どのパレットでも同じです。文字の色は、対応する <code>-soft</code> の面に重ねて使い、アイコンを必ず添えます。</p>'
      + ex('<span class="k-badge k-badge-ok">%s成功</span>\n<span class="k-badge k-badge-danger">%sエラー</span>\n<span class="k-badge k-badge-info">%s情報</span>' % (I_OK, I_WARN, I_INFO))))

page('typography', '書体は役割で使い分けます。基本は LINE Seed JP で、例外はタイトルと、桁をそろえたい数字だけです。',
  sec('書体', table(['役割', '書体', 'トークン'], [
        ['基本(本文、見出し、ボタン)', 'LINE Seed JP 400 / 700 / 800', '<code>--font-body</code>'],
        ['タイトル(ページのタイトルと章の見出し)', 'Zen Maru Gothic 900', '<code>--font-title</code>、<code>.k-title</code>'],
        ['数字(金額、件数、日付を並べる所)', 'Inter + tabular-nums', '<code>--font-num</code>、<code>.k-num</code>']])
      + '<p>LINE Seed JP は Kasane と一緒に配信しています。文字の範囲ごとに細かく分けてあるので、ページで使う文字の分だけが読み込まれます。Zen Maru Gothic と Inter は Google Fonts から読み込みます。</p>'
      + code('HTML', '<link rel="stylesheet" href="' + BASE + '/fonts/line-seed-jp.css">\n<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')
      + '<p>3つの書体はどれも SIL Open Font License 1.1 で公開されています。</p>')
  + sec('文字の大きさ', '<div class="type-list">'
      '<div class="type-row"><code>--text-2xl</code><span class="k-title" style="font-size:32px">ページのタイトル</span><small>32px / Zen Maru Gothic 900</small></div>'
      '<div class="type-row"><code>--text-xl</code><span class="k-title" style="font-size:24px">章の見出し</span><small>24px / Zen Maru Gothic 900</small></div>'
      '<div class="type-row"><code>--text-lg</code><span style="font-size:18px;font-weight:800;line-height:1.5">カードの見出し</span><small>18px / 800</small></div>'
      '<div class="type-row"><code>--text-base</code><span style="font-size:16px">本文の文字はこの大きさです。</span><small>16px / 400</small></div>'
      '<div class="type-row"><code>--text-sm</code><span style="font-size:14px">ラベルや補足に使います。</span><small>14px / 400・700</small></div>'
      '<div class="type-row"><code>--text-xs</code><span style="font-size:12px">注釈や日付に使います。</span><small>12px / 400</small></div></div>')
  + sec('タイトルの使い方', dd('<div class="stack" style="align-items:flex-start"><span class="k-title" style="font-size:24px">今週のおしらせ</span><span style="font-size:14px">図書館は金曜日、17時に閉まります。</span></div>', 'Zen Maru Gothic はタイトルだけに使います。',
        '<div class="stack" style="align-items:flex-start"><span class="k-title" style="font-size:24px">今週のおしらせ</span><span class="k-title" style="font-size:14px">図書館は金曜日、17時に閉まります。</span></div>', '本文やカードの中の見出しには使いません。極太の文字が続くと読みにくくなります。'))
  + sec('行間と行の長さ', '<p>本文の行間は 1.8、タイトルは 1.3 です。長い文章は、1行が全角35〜40文字に収まる幅にします。</p>'
      + code('CSS', 'body { line-height: 1.8; }\n.k-title { line-height: 1.3; }\n.prose { max-width: 38em; }'))
  + sec('数字', '<p>金額や件数を縦に並べるときは、Inter の等幅数字にして桁をそろえます。</p>'
      '<div class="numcmp"><div><small>LINE Seed JP</small><span>1,111.00</span><span>8,888.00</span><span>10,000.01</span></div><div class="k-num"><small>Inter + tabular-nums</small><span>1,111.00</span><span>8,888.00</span><span>10,000.01</span></div></div>'
      + ex('<span class="k-num">12,480</span> 円')))

page('shape', '角を大きく丸め、余白を決まった段階から選ぶことで、やわらかく整った印象にします。',
  sec('角丸', '<p>外側の面ほど大きく、内側の面ほど小さくします。</p>'
      '<div class="radii"><div><i style="border-radius:28px"></i><code>--r-lg</code><small>28px カード、パネル</small></div><div><i style="border-radius:18px"></i><code>--r-md</code><small>18px 中の面、リストの行</small></div><div><i style="border-radius:14px"></i><code>--r-sm</code><small>14px 入力欄</small></div><div><i style="border-radius:999px"></i><code>--r-full</code><small>ボタン、バッジ</small></div></div>')
  + sec('余白', '<p>余白は7段階から選びます。部品の中は小さく、章の間は大きく取ります。</p>'
      '<div class="spaces">' + ''.join('<div><code>--space-%d</code><i style="width:%dpx"></i><small>%dpx %s</small></div>' % (i + 1, v, v, d) for i, (v, d) in enumerate([(4, 'アイコンと文字の間'), (8, 'ボタンどうしの間'), (12, 'リストの行の内側'), (16, '中の面の内側'), (24, 'カードの内側'), (32, 'カードどうしの間'), (56, '章と章の間')])) + '</div>')
  + sec('押せる場所の大きさ', '<p>ボタンは高さ44px、小さいボタンは36px、入力欄は46pxです。</p>')
  + sec('サンプルコード', code('CSS', '.panel {\n  background: var(--surface);\n  border-radius: var(--r-lg);\n  padding: var(--space-5);\n}\n.panel > * + * { margin-top: var(--space-3); }')))

page('button', '操作のきっかけになる部品です。丸薬型で、枠線はありません。',
  sec('種類', '<p>主な操作は <code>.k-btn-primary</code>、取り消しなど控えめな操作は <code>.k-btn-quiet</code>、削除は <code>.k-btn-danger</code> を使います。</p>'
      + ex('<button class="k-btn k-btn-primary" type="button">保存する</button>\n<button class="k-btn" type="button">下書きにする</button>\n<button class="k-btn k-btn-quiet" type="button">キャンセル</button>\n<button class="k-btn k-btn-danger" type="button">削除する</button>'))
  + sec('大きさと無効', ex('<button class="k-btn k-btn-primary k-btn-sm" type="button">小さいボタン</button>\n<button class="k-btn k-btn-primary" type="button">標準のボタン</button>\n<button class="k-btn k-btn-primary k-btn-lg" type="button">大きいボタン</button>\n<button class="k-btn" type="button" disabled>使えません</button>'))
  + sec('使い方', dd('<div class="inline"><button class="k-btn k-btn-quiet" type="button">キャンセル</button><button class="k-btn k-btn-primary" type="button">保存する</button></div>', '主ボタンは1つの画面に1つまでにします。',
                    '<div class="inline"><button class="k-btn k-btn-primary" type="button">キャンセル</button><button class="k-btn k-btn-primary" type="button">保存する</button></div>', '主ボタンを並べません。どちらが主な操作か分からなくなります。'))
  + sec('CSS', code('CSS', CSS['button'])))

page('input', '文字の入力欄、チェックボックス、スイッチ、色の選択です。Kasane で枠線を持つのは、この入力の部品だけです。',
  sec('文字の入力欄', ex('<label class="k-field">お名前\n  <input class="k-input" type="text" placeholder="例:山田 花子">\n  <span class="k-hint">本名でなくてもかまいません。</span>\n</label>', True))
  + sec('エラー', '<p>枠を赤くするだけでなく、何が問題で、どう直せばよいかを文で伝えます。</p>'
        + ex('<label class="k-field">メールアドレス\n  <input class="k-input" type="email" value="hanako@" aria-invalid="true" aria-describedby="mail-error">\n  <span class="k-error" id="mail-error">%s「@」のあとにドメインを入力してください。</span>\n</label>' % I_WARN, True))
  + sec('選択欄', ex('<label class="k-field">場所\n  <span class="k-select">\n    <select class="k-input">\n      <option>東京</option>\n      <option>大阪</option>\n      <option>福岡</option>\n    </select>\n  </span>\n</label>', True))
  + sec('チェックボックス', ex('<label class="k-option"><input class="k-check" type="checkbox" checked> お知らせを受け取る</label>\n<label class="k-option"><input class="k-check" type="checkbox"> 週のまとめを受け取る</label>'))
  + sec('ラジオボタン', ex('<label class="k-option"><input class="k-radio" type="radio" name="density" checked> ゆったり</label>\n<label class="k-option"><input class="k-radio" type="radio" name="density"> ふつう</label>\n<label class="k-option"><input class="k-radio" type="radio" name="density"> コンパクト</label>'))
  + sec('スイッチ', '<p>すぐに反映される設定に使います。オンとオフは、つまみの位置でも分かります。</p>'
        + ex('<label class="k-switch">\n  <input type="checkbox" checked>\n  <span class="k-switch-track" aria-hidden="true"></span>\n  自動で保存する\n</label>'))
  + sec('色の選択', '<p>利用者がアクセントの色を選ぶための部品です。中身はラジオボタンなので、キーボードの矢印キーでも選べます。色の丸だけを並べる <code>.k-palette-compact</code> もあります。置き場所と保存の仕方は <a href="#integrate">組み込み方と使用例</a> にあります。押すと、このサイトの色も変わります。</p>'
        + '<div class="ex"><div class="ex-demo ex-stack"><div class="wide">' + palette_html(name='accent-input') + '</div></div>'
        + code('HTML', palette_src()) + '</div>'
        + '<p>色の丸だけを並べるときは、<code>k-palette</code> に <code>k-palette-compact</code> を足します。名前は見えなくなりますが、読み上げのために <code>k-palette-name</code> は残します。</p>')
  + sec('CSS', code('CSS', CSS['input'] + '\n\n' + CSS['palette'])))

page('card', '情報のまとまりを作る面です。枠線も影も使わず、面の色で区切ります。',
  sec('カード', ex('<div class="k-card">\n  <h3 class="k-card-title">今週のおしらせ</h3>\n  <p class="k-card-text">金曜日は、図書館が17時に閉まります。</p>\n  <div><button class="k-btn" type="button">詳しく見る</button></div>\n</div>', True))
  + sec('リスト', '<p>行は <code>--surface-2</code> の面にして、行どうしは6pxの隙間で分けます。区切り線は使いません。</p>'
        + ex('<div class="k-card">\n  <h3 class="k-card-title">やること</h3>\n  <ul class="k-list">\n    <li class="k-list-item"><span class="k-list-item-main">図書館の本を返す</span><span class="k-list-item-sub">11月5日まで</span></li>\n    <li class="k-list-item"><span class="k-list-item-main">発表スライドの確認</span><span class="k-list-item-sub">11月8日まで</span></li>\n  </ul>\n</div>', True))
  + sec('中の面', '<p>カードの中に小さなまとまりを作るときは、<code>.k-nest</code> で面を一段変えます。</p>'
        + ex('<div class="k-card">\n  <h3 class="k-card-title">設定</h3>\n  <div class="k-nest">通知は、毎朝8時にまとめて届きます。</div>\n</div>', True))
  + sec('お知らせ', '<p>お知らせの見出しは、ライトでは文字色、ダークではアクセントの色になります。</p>'
        + ex('<div class="k-notice">\n  <h3 class="k-notice-title">お知らせ</h3>\n  <div>今週のまとめは、日曜の夜に届きます。</div>\n</div>', True))
  + sec('CSS', code('CSS', CSS['card'])))

page('badge', '状態や分類を短い言葉で示す部品です。',
  sec('種類', '<p>状態を表すバッジには、アイコンを必ず添えます。</p>'
      + ex('<span class="k-badge">下書き</span>\n<span class="k-badge k-badge-accent">注目</span>\n<span class="k-badge k-badge-ok">%s完了</span>\n<span class="k-badge k-badge-danger">%sエラー</span>\n<span class="k-badge k-badge-info">%s情報</span>' % (I_OK, I_WARN, I_INFO)))
  + sec('リストの中で使う', ex('<ul class="k-list" style="width:100%%;max-width:420px">\n  <li class="k-list-item"><span class="k-list-item-main">レポートの提出</span><span class="k-badge k-badge-ok">%s完了</span></li>\n  <li class="k-list-item"><span class="k-list-item-main">発表スライド</span><span class="k-badge k-badge-accent">もうすぐ</span></li>\n</ul>' % I_OK, True))
  + sec('CSS', code('CSS', CSS['badge'])))

page('tabs', '同じ場所で表示を切り替える部品です。選択中の項目だけ、面の色を変えます。',
  sec('タブ', '<p><code>.k-seg</code> は <code>--surface</code> の面の上に置きます。選ぶと、選択中の背景がスイッチのつまみのように横へ動きます(項目は5つまで)。</p>'
      + ex('<div class="k-card">\n  <div><div class="k-seg" role="tablist" aria-label="説明">\n    <button type="button" role="tab" id="tab-a" aria-controls="panel-a" aria-selected="true">概要</button>\n    <button type="button" role="tab" id="tab-b" aria-controls="panel-b" aria-selected="false" tabindex="-1">使い方</button>\n  </div></div>\n  <div class="k-nest" role="tabpanel" id="panel-a" aria-labelledby="tab-a">Kasane は、色を選べるデザインシステムです。</div>\n  <div class="k-nest" role="tabpanel" id="panel-b" aria-labelledby="tab-b" hidden>CSSを読み込み、部品のクラスを付けて使います。</div>\n</div>', True)
      + code('JavaScript', 'document.querySelectorAll(\'[role="tablist"]\').forEach((list) => {\n  const tabs = [...list.querySelectorAll(\'[role="tab"]\')];\n  const select = (tab) => tabs.forEach((t) => {\n    const on = t === tab;\n    t.setAttribute("aria-selected", String(on));\n    t.tabIndex = on ? 0 : -1;\n    document.getElementById(t.getAttribute("aria-controls")).hidden = !on;\n  });\n  tabs.forEach((tab, i) => {\n    tab.addEventListener("click", () => select(tab));\n    tab.addEventListener("keydown", (e) => {\n      const d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;\n      if (!d) return;\n      const next = tabs[(i + d + tabs.length) % tabs.length];\n      select(next); next.focus();\n    });\n  });\n});'))
  + sec('2つから選ぶ切り替え', '<p>表示の切り替えなど、選択肢が少ないときにも使えます。このときは <code>aria-pressed</code> で選択中を示します。</p>'
      + ex('<div class="k-card"><div class="k-seg" role="group" aria-label="並び順">\n  <button type="button" aria-pressed="true">新しい順</button>\n  <button type="button" aria-pressed="false">古い順</button>\n</div></div>'))
  + sec('CSS', code('CSS', CSS['tabs'])))

page('progress', '作業がどこまで進んだかを示す部品です。',
  sec('進捗バー', '<p>バーの長さだけでなく、数字でも進み具合を伝えます。数字は <code>.k-num</code> にします。</p>'
      + ex('<div class="k-card">\n  <div class="k-bar-head"><span>部品</span><span class="k-num">72%</span></div>\n  <div class="k-bar" role="progressbar" aria-label="部品" aria-valuenow="72" aria-valuemin="0" aria-valuemax="100"><i style="width:72%"></i></div>\n</div>', True))
  + sec('CSS', code('CSS', CSS['progress'])))

page('dialog', '確認が必要な操作と、操作の結果を伝える部品です。',
  sec('ダイアログ', '<p>取り消しのボタンは枠も背景もない <code>.k-btn-quiet</code> にして左に、実行するボタンは右に置きます。</p>'
      + ex('<div class="k-dialog" role="dialog" aria-modal="true" aria-labelledby="dialog-title">\n  <h3 class="k-dialog-title" id="dialog-title">このメモを削除しますか?</h3>\n  <p class="k-dialog-text">削除すると元に戻せません。</p>\n  <div class="k-dialog-actions">\n    <button class="k-btn k-btn-quiet" type="button">キャンセル</button>\n    <button class="k-btn k-btn-danger" type="button">削除する</button>\n  </div>\n</div>', True)
      + '<p>実際に使うときは、全体を <code>.k-scrim</code> で包んで画面の中央に重ねます。開いたら最初のボタンにフォーカスを移し、Esc キーで閉じられるようにします。</p>'
      + code('HTML', '<div class="k-scrim">\n  <div class="k-dialog" role="dialog" aria-modal="true" aria-labelledby="dialog-title">\n    ...\n  </div>\n</div>'))
  + sec('トースト', '<p>操作の結果を、画面の下に短く表示します。数秒で消えるので、大事な内容には使いません。</p>'
      + ex('<div class="k-toast" role="status">保存しました</div>'))
  + sec('CSS', code('CSS', CSS['dialog'])))

exec(open('pages_extra.py', encoding='utf-8').read())

HOME = ('<article class="page home" data-page="home"><div class="hero"><div class="hero-art" aria-hidden="true"><i></i><i></i><i></i></div>'
        '<h1>Kasane</h1><p class="lead">面を重ねて区切り、色を選べるデザインシステム。</p><p class="hero-ai">AI で UI を作るときは、<a href="' + BASE + '/kasane.md">仕様書(kasane.md)</a>を読ませてください。</p>'
        '<div class="inline start"><a class="k-btn k-btn-primary" href="#start">使い始める</a><button class="k-btn" type="button" data-open-chooser>色を選び直す</button></div></div>'
        '<div class="cards two">'
        '<a class="tile tile-link" href="#about"><h2 class="tile-h">はじめに</h2><p>Kasane の概要、使い始め方、AI との使い方。</p></a>'
        '<a class="tile tile-link" href="#principles"><h2 class="tile-h">原則</h2><p>設計の考え方、アクセシビリティ、パフォーマンス、文章の書き方。</p></a>'
        '<a class="tile tile-link" href="#color"><h2 class="tile-h">スタイル</h2><p>カラー、タイポグラフィ、レイアウト、アイコン、動き。</p></a>'
        '<a class="tile tile-link" href="#button">\n<h2 class="tile-h">コンポーネント</h2><p>部品の見本とサンプルコード。</p></a></div></article>')

sidebar = ''.join('<div class="nav-group" data-sec="%s"><div class="nav-title">%s</div>%s</div>' % (sid, label, ''.join('<a class="nav-link" href="#%s">%s</a>' % (pid, t) for pid, t in pages)) for sid, label, pages in NAV)
topnav = ''.join('<a href="#%s" data-sec="%s">%s</a>' % (pages[0][0], sid, label) for sid, label, pages in NAV)
footer_cols = ''.join('<div class="f-col"><div class="f-title">%s</div>%s</div>' % (label, ''.join('<a href="#%s">%s</a>' % (pid, t) for pid, t in pages)) for _, label, pages in NAV)
chooser_btns = ''.join('<button class="pal" type="button" data-accent-set="%s" aria-pressed="false"><i style="background:linear-gradient(135deg,%s 50%%,%s 50%%)"></i><b>%s</b><small>%s</small></button>' % (p['id'], p['light']['--accent'], p['dark']['--accent'], p['name'], p['en']) for p in PAL)
nav_json = json.dumps([{'id': sid, 'label': label, 'pages': [list(p) for p in pages]} for sid, label, pages in NAV], ensure_ascii=False)

# Docs-only: for the Don't example, the text colour that reads worst on each palette's accent
# (white on light accents, near-black on dark ones), so the example follows the selected palette.
def _lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def _cr(a, b):
    x, y = _lum(a), _lum(b); return (max(x, y) + .05) / (min(x, y) + .05)
def _bad(acc): return min(('#ffffff', '#1a1a1a'), key=lambda c: _cr(c, acc))
DOCS_EXTRA = ''
# Docs only: .demo-scope[data-accent] carries one palette's tokens, so several palettes can sit on one page.
_ORDER = ['--bg', '--surface', '--surface-2', '--surface-3', '--ink', '--muted', '--line', '--accent', '--accent-soft', '--accent-ink', '--on-accent', '--focus', '--notice-head', '--ok', '--ok-soft', '--danger', '--danger-soft', '--info', '--info-soft']
for p in PAL:
    sel = '.demo-scope[data-accent="%s"]' % p['id']
    lt = ';'.join('%s:%s' % (k, p['light'][k]) for k in _ORDER)
    dk = ';'.join('%s:%s' % (k, p['dark'][k]) for k in _ORDER)
    DOCS_EXTRA += '%s{%s}@media (prefers-color-scheme:dark){html:not([data-theme="light"]) %s{%s}}html[data-theme="dark"] %s{%s}\n' % (sel, lt, sel, dk, sel, dk)
for p in PAL:
    sel = ':root[data-accent="%s"]' % p['id']
    first = p['id'] == PAL[0]['id']
    l, d = _bad(p['light']['--accent']), _bad(p['dark']['--accent'])
    DOCS_EXTRA += '%s%s{--bad-on-accent:%s}\n' % (sel, ',:root:not([data-accent])' if first else '', l)
    DOCS_EXTRA += '@media (prefers-color-scheme:dark){%s:not([data-theme="light"])%s{--bad-on-accent:%s}}\n' % (sel, ',:root:not([data-accent]):not([data-theme="light"])' if first else '', d)
    DOCS_EXTRA += '%s[data-theme="dark"]%s{--bad-on-accent:%s}\n' % (sel, ',:root:not([data-accent])[data-theme="dark"]' if first else '', d)
DOCS_EXTRA += '.bad-on-accent,.bad-on-accent:hover{background:var(--accent);color:var(--bad-on-accent);cursor:default}.bad-on-accent::after{content:attr(data-label)}.bad-link{color:var(--accent);font-weight:700;text-decoration:underline;text-underline-offset:3px}.bad-link::after{content:attr(data-label)}\n'

# Point AI tools at the plain-text spec: <head> links and a footer column.
SITE = BASE.rsplit('/', 1)[0]
footer_cols += ('<div class="f-col"><div class="f-title">AI 向け</div><a href="%s/kasane.md">仕様書(kasane.md)</a><a href="%s/kasane.en.md">英語版(kasane.en.md)</a>'
                '<a href="%s/llms.txt">llms.txt</a><a href="%s/tokens.json">tokens.json</a></div>' % (BASE, BASE, SITE, BASE))

# Routing without JavaScript at first paint: a tiny script in <head> sets html[data-page] and
# html[data-sec] from the hash, and these rules show the right page, sidebar group and TOC.
PAGE_SEC = {'home': ''}
for sid, _, pages in NAV:
    for pid, _ in pages: PAGE_SEC[pid] = sid
ROUTE_CSS = ''.join('html[data-page="%s"] .page[data-page="%s"],html[data-page="%s"] .toc-page[data-page="%s"]{display:flex}' % (p, p, p, p) for p in PAGE_SEC)
ROUTE_CSS += ''.join('html[data-sec="%s"] .nav-group[data-sec="%s"]{display:flex}' % (s, s) for s, _, _ in NAV)
DOCS_EXTRA = ROUTE_CSS + '\n' + DOCS_EXTRA

# ---------------------------------------------------------------- SEO
SITE_NAME = 'Kasane'
HOME_TITLE = 'Kasane — 色を選べるデザインシステム'
HOME_DESC = ('Kasane(かさね)は、面を重ねて情報を区切り、アクセントの色を9色から選べる、Webサイトと Webアプリのためのデザインシステムです。'
             'CSS、部品の見本とサンプルコード、AI 用の仕様書、自動チェックを公開しています。')
def plain(h):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()
LANGS = ('ja', 'en')   # ja at /, en at /en/
def path_of(pid, lang='ja'):
    return ('' if lang == 'ja' else '/' + lang) + ('/' if pid == 'home' else '/%s/' % pid)
def url_of(pid, lang='ja'):
    return SITE + path_of(pid, lang)
BG = {m: PAL[0][m]['--bg'] for m in ('light', 'dark')}   # default palette, for the browser UI colour
def seo(pid, title, desc, robots=None, lang='ja', tr=lambda s: s):
    a = html.escape
    tags = ['<meta name="description" content="%s">' % a(desc)]
    if robots:
        tags.append('<meta name="robots" content="%s">' % robots)
    else:
        tags += ['<link rel="canonical" href="%s">' % url_of(pid, lang)]
        tags += ['<link rel="alternate" hreflang="%s" href="%s">' % (l, url_of(pid, l)) for l in LANGS]
        tags += ['<link rel="alternate" hreflang="x-default" href="%s">' % url_of(pid),
                 '<meta property="og:type" content="%s">' % ('website' if pid == 'home' else 'article'),
                 '<meta property="og:site_name" content="%s">' % SITE_NAME,
                 '<meta property="og:title" content="%s">' % a(title),
                 '<meta property="og:description" content="%s">' % a(desc),
                 '<meta property="og:url" content="%s">' % url_of(pid, lang),
                 '<meta property="og:image" content="%s/og.png">' % SITE,
                 '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
                 '<meta property="og:image:alt" content="Kasane — 面を重ねて区切り、色を選べるデザインシステム">',
                 '<meta property="og:locale" content="%s">' % ('ja_JP' if lang == 'ja' else 'en_US'),
                 '<meta name="twitter:card" content="summary_large_image">']
        if pid == 'home':
            ld = {'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NAME, 'alternateName': 'かさね', 'url': url_of('home', lang),
                  'description': tr(desc), 'inLanguage': lang}
        else:
            sid = PAGE_SEC[pid]; first = [p for s_, _, ps in NAV if s_ == sid for p, _ in ps][0]
            ld = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': SITE_NAME, 'item': url_of('home', lang)},
                {'@type': 'ListItem', 'position': 2, 'name': tr(SEC_OF[pid]), 'item': url_of(first, lang)},
                {'@type': 'ListItem', 'position': 3, 'name': tr(TITLE_OF[pid]), 'item': url_of(pid, lang)}]}
        tags.append('<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False).replace('</', '<\\/'))
    tags += ['<meta name="theme-color" media="(prefers-color-scheme: light)" content="%s">' % BG['light'],
             '<meta name="theme-color" media="(prefers-color-scheme: dark)" content="%s">' % BG['dark'],
             '<link rel="icon" href="/favicon.ico" sizes="32x32">',
             '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
             '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
             '<link rel="manifest" href="/site.webmanifest">',
             '<link rel="alternate" type="text/markdown" title="Kasane 仕様書" href="%s/kasane.md">' % BASE,
             '<link rel="alternate" type="text/markdown" hreflang="en" title="Kasane spec (English)" href="%s/kasane.en.md">' % BASE]
    return '\n'.join(tags)

T = open('site.tpl.html', encoding='utf-8').read()
T = re.sub(r'<!--@@ICON:([a-z0-9-]+)@@-->', lambda m: icon(m.group(1)), T)
T = T.replace('/* Log, icon grid */', DOCS_EXTRA + '\n/* Log, icon grid */', 1)
T = (T.replace('<!--@@SIDEBAR@@-->', sidebar).replace('<!--@@TOPNAV@@-->', topnav)
      .replace('<!--@@FOOTER@@-->', footer_cols).replace('<!--@@CHOOSER@@-->', chooser_btns).replace('/*@@NAV@@*/', nav_json)
      .replace('/*@@PAGESEC@@*/', json.dumps(PAGE_SEC)))

NOT_FOUND = ('<article class="page" data-page="home"><div class="page-head"><h1>ページが見つかりません</h1>'
             '<p class="lead">URLが変わったか、ページがなくなった可能性があります。</p></div>'
             '<div class="inline start"><a class="k-btn k-btn-primary" href="/">トップページへ</a><a class="k-btn" href="/start/">使い始める</a></div></article>')

def write(path, out):
    assert '@@' not in out, path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(out)

if EMBED:
    # Single file for previews: every page in one document, routed by #name; CSS and a subset of LINE Seed JP inlined.
    import subprocess, base64
    out = (T.replace('<!--@@PAGES@@-->', HOME + ''.join(PAGES)).replace('<!--@@TOC@@-->', ''.join(TOCS))
            .replace('@@TITLE@@', HOME_TITLE).replace('<!--@@SEO@@-->', seo('home', HOME_TITLE, HOME_DESC))
            .replace('/*@@ROUTE@@*/', "(function(d){var h=location.hash.slice(1);if(!(h in KASANE_PAGES))h='home';d.dataset.page=h;d.dataset.sec=KASANE_PAGES[h];})(document.documentElement);"))
    src = os.environ.get('LINE_SEED_SRC', '/home/claude/hidamari/fonts/node_modules/line-seed-jp/woff2')
    out = out.replace('<!--@@HEADLINKS@@-->', '').replace('<!--@@LANG@@-->', '').replace(
        '<!--@@LANGDEMO@@-->', '<a class="k-btn k-btn-quiet" href="%s/en/i18n/" hreflang="en" lang="en">%sEnglish</a>' % (SITE, icon('languages'))).replace('/*@@PALETTES@@*/', PALETTES_CSS).replace('/*@@COMPONENTS@@*/', COMPONENTS_CSS)
    chars = (set(out) | set(chr(c) for c in range(0x20, 0x7f))) - {'\n', '\t'}
    open(os.path.join(OUT, 'chars.txt'), 'w', encoding='utf-8').write(''.join(sorted(chars)))
    faces = []
    for fn, w in (('Rg', 400), ('Bd', 700), ('Eb', 800)):
        dst = os.path.join(OUT, 'sub_%s.woff2' % fn)
        subprocess.run(['pyftsubset', os.path.join(src, 'LINESeedJP_OTF_%s.woff2' % fn), '--text-file=' + os.path.join(OUT, 'chars.txt'),
                        '--flavor=woff2', '--output-file=' + dst, '--layout-features=*'], check=True, capture_output=True)
        faces.append("@font-face{font-family:'LINE Seed JP';font-weight:%d;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}"
                     % (w, base64.b64encode(open(dst, 'rb').read()).decode()))
    out = out.replace('/*@@FONTS@@*/', '\n'.join(faces))
    write(os.path.join(OUT, 'docs-embedded.html'), out)
    print('wrote tools/.out/docs-embedded.html', len(out), 'bytes;', len(PAGES) + 1, 'pages')
else:
    # The docs site: one HTML file per URL (/, /color/, …) so every page can be found and shared on its own.
    # It uses the same files it documents.
    SITE_DIR = os.path.join(ROOT, 'site')
    import shutil
    # The translated pages need BeautifulSoup. Where it is missing (e.g. a deploy machine that only rebuilds),
    # keep the committed site/en/ as it is; CI has it and checks that site/ is up to date.
    try:
        import bs4  # noqa: F401
        BUILD_LANGS = LANGS
    except ImportError:
        BUILD_LANGS = ('ja',)
        print('i18n: BeautifulSoup (bs4) is not installed; keeping the existing translated pages')
    for d in os.listdir(SITE_DIR) if os.path.isdir(SITE_DIR) else []:
        if d in LANGS and d not in BUILD_LANGS: continue
        if os.path.isfile(os.path.join(SITE_DIR, d, 'index.html')): shutil.rmtree(os.path.join(SITE_DIR, d))
    head_links = ('<link rel="preload" href="/%s/fonts/line-seed-jp.css" as="style">\n<link rel="stylesheet" href="/%s/fonts/line-seed-jp.css" media="print" onload="this.media=\'all\'">\n'
                  '<noscript><link rel="stylesheet" href="/%s/fonts/line-seed-jp.css"></noscript>\n<link rel="stylesheet" href="/%s/kasane.css">' % (VERSION, VERSION, VERSION, VERSION))
    ids = set(PAGE_SEC)
    sys.path.insert(0, HERE)
    if BUILD_LANGS != ('ja',):
        from i18n import Translator
    TABLES = {l: json.load(open(os.path.join(HERE, 'i18n', l + '.json'), encoding='utf-8')) for l in BUILD_LANGS if l != 'ja'}
    TR = {l: Translator(t) for l, t in TABLES.items()}
    def tr_text(lang):
        return (lambda s_: s_) if lang == 'ja' else (lambda s_: TR[lang].lookup(re.sub(r'\s+', ' ', s_).strip()) or s_)
    JS_STRINGS = ['メニューを開く', 'メニューを閉じる', 'コピー', 'コピーしました', 'コピーできませんでした', 'すべて表示', 'たたむ']
    def links(h, lang):   # #name → /name/ (or /en/name/)
        return re.sub(r'href="#([a-z0-9-]+)"', lambda m: 'href="%s"' % path_of(m.group(1), lang) if m.group(1) in ids else m.group(0), h)
    def lang_switch(pid, lang, cls='lang-link', label_tag='span'):
        other = 'en' if lang == 'ja' else 'ja'
        label = 'English' if other == 'en' else '日本語'
        return ('<a class="%s" href="%s" hreflang="%s" lang="%s" data-lang-switch data-i18n-skip>%s<%s>%s</%s></a>'
                % (cls, path_of(pid, other), other, other, icon('languages'), label_tag, label, label_tag))
    # English pages are almost all Latin text. The font CSS loads without blocking, so the first paint would use
    # another font and the text would reflow when LINE Seed JP arrives (layout shift). Declare the three Latin
    # groups inline and preload them, so English text is drawn in LINE Seed JP from the start.
    _fcss = open(os.path.join(ROOT, VERSION, 'fonts', 'line-seed-jp.css'), encoding='utf-8').read()
    LATIN_FACES = [m.group(0) for m in re.finditer(r"@font-face\{[^}]*files/line-seed-jp-\d+-latin\.woff2[^}]*\}", _fcss)]
    assert len(LATIN_FACES) == 3, 'expected the 400/700/800 Latin groups in line-seed-jp.css'
    LATIN_HEAD = (''.join('<link rel="preload" href="/%s/fonts/files/%s" as="font" type="font/woff2" crossorigin>\n'
                          % (VERSION, re.search(r'files/([^)]+)\)', f).group(1)) for f in LATIN_FACES)
                  + '<style>' + ''.join(f.replace('font-display:swap', 'font-display:block').replace('url(./files/', 'url(/%s/fonts/files/' % VERSION) for f in LATIN_FACES) + '</style>\n')
    def render(pid, article, toc, title, desc, robots=None, lang='ja'):
        route = "window.KASANE_PAGE='%s';document.documentElement.dataset.page='%s';document.documentElement.dataset.sec='%s';" % (pid, pid, PAGE_SEC[pid])
        if lang != 'ja':
            route += 'window.KASANE_T=%s;' % json.dumps({k: TR[lang].lookup(k) or k for k in JS_STRINGS}, ensure_ascii=False)
        if pid == 'home' and not robots:   # old links (/#color) still work
            route += "(function(h){if(h&&h!=='home'&&h in KASANE_PAGES)location.replace('%s'+h+'/');})(location.hash.slice(1));" % path_of('home', lang)
        out = (T.replace('<!--@@PAGES@@-->', article).replace('<!--@@TOC@@-->', toc).replace('@@TITLE@@', html.escape(title))
                .replace('<!--@@SEO@@-->', seo(pid, title, desc, robots, lang, tr_text(lang))).replace('/*@@ROUTE@@*/', route)
                .replace('<!--@@LANG@@-->', lang_switch(pid, lang))
                .replace('<!--@@LANGDEMO@@-->', lang_switch(pid, lang, 'k-btn k-btn-quiet', 'span'))
                .replace('<!--@@HEADLINKS@@-->', (LATIN_HEAD if lang != 'ja' else '') + head_links).replace('/*@@PALETTES@@*/', '').replace('/*@@COMPONENTS@@*/', '').replace('/*@@FONTS@@*/', ''))
        out = links(out, lang)
        if lang != 'ja':
            out = TR[lang].translate(out).replace('<html lang="ja"', '<html lang="%s"' % lang, 1)
            if not out.lower().startswith('<!doctype'):
                out = '<!DOCTYPE html>\n' + out
        return out
    for lang in BUILD_LANGS:
        base = SITE_DIR if lang == 'ja' else os.path.join(SITE_DIR, lang)
        write(os.path.join(base, 'index.html'), render('home', HOME, '', HOME_TITLE, HOME_DESC, lang=lang))
        for pid, _ in FLAT:
            write(os.path.join(base, pid, 'index.html'), render(pid, ART[pid], TOC_OF[pid], '%s | Kasane デザインシステム' % TITLE_OF[pid], plain(LEAD_OF[pid]), lang=lang))
        write(os.path.join(base, '404.html'), render('home', NOT_FOUND, '', 'ページが見つかりません | Kasane', 'お探しのページは見つかりませんでした。', robots='noindex', lang=lang))
    # Every Japanese text on the English pages needs an entry in tools/i18n/<lang>.json
    for lang, t in TR.items():
        miss = sorted(t.missing)
        open(os.path.join(OUT, 'i18n-missing-%s.json' % lang), 'w', encoding='utf-8').write(json.dumps({k: '' for k in miss}, ensure_ascii=False, indent=1))
        if miss:
            print('i18n: %d %s text(s) have no translation (see tools/.out/i18n-missing-%s.json)' % (len(miss), lang, lang))
            if not os.environ.get('KASANE_I18N_LAX'):
                sys.exit(1)
    write(os.path.join(SITE_DIR, 'sitemap.xml'), '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + ''.join('  <url><loc>%s</loc></url>\n' % url_of(p, l) for l in LANGS for p in ['home'] + [p for p, _ in FLAT]) + '</urlset>\n')
    write(os.path.join(SITE_DIR, 'robots.txt'), 'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE)
    write(os.path.join(SITE_DIR, 'site.webmanifest'), json.dumps({
        'name': 'Kasane デザインシステム', 'short_name': 'Kasane', 'lang': 'ja', 'start_url': '/', 'display': 'browser',
        'background_color': BG['light'], 'theme_color': BG['light'],
        'icons': [{'src': '/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': '/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                  {'src': '/icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]}, ensure_ascii=False, indent=2) + '\n')
    print('wrote site/:', len(FLAT) + 1, 'pages ×', len(LANGS), 'languages, 404.html, sitemap.xml, robots.txt, site.webmanifest')
