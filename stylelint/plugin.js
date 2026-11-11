// Kasane Stylelint rules. Each rule checks one of the "必ず守るルール" in v1/kasane.md.
import stylelint from 'stylelint';

const { createPlugin, utils: { report, ruleMessages, validateOptions } } = stylelint;
const NS = 'kasane';

// Remove url(...) and quoted strings so data URIs and content text are not inspected.
const clean = (v) => v.replace(/url\([^)]*\)/gi, '').replace(/"[^"]*"|'[^']*'/g, '');
const isCustomProp = (prop) => prop.startsWith('--');

/** Make a rule that inspects declarations. check(decl, options) returns a message key or null. */
function declRule(name, messages, check, { allowOptions = false } = {}) {
  const ruleName = `${NS}/${name}`;
  const msgs = ruleMessages(ruleName, messages);
  const rule = (primary, secondary) => (root, result) => {
    const ok = validateOptions(result, ruleName, { actual: primary, possible: [true] },
      ...(allowOptions ? [{ actual: secondary, possible: () => true, optional: true }] : []));
    if (!ok) return;
    root.walkDecls((decl) => {
      const hit = check(decl, secondary || {});
      if (hit) report({ ruleName, result, node: decl, message: typeof msgs[hit] === 'function' ? msgs[hit](decl.prop, decl.value) : msgs[hit], word: decl.value });
    });
  };
  rule.ruleName = ruleName;
  rule.messages = msgs;
  rule.meta = { url: 'https://github.com/yamamotoxqx/design-system-kasane/blob/main/v1/kasane.md' };
  return createPlugin(ruleName, rule);
}

// ------------------------------------------------------------ no-raw-color
const NAMED = new Set('aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray lightslategrey lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive olivedrab orange orangered orchid palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue slateblue slategray slategrey snow springgreen steelblue tan teal thistle tomato turquoise violet wheat white whitesmoke yellow yellowgreen'.split(' '));
const COLOR_FN = /\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(/i;
const HEX = /(^|[\s,(])#[0-9a-f]{3,8}\b/i;
const COLOR_PROPS = /color|background|border|outline|fill|stroke|shadow|caret|accent|text-decoration|column-rule/i;

export const noRawColor = declRule('no-raw-color', {
  raw: (prop, value) => `色を直接書かずに、トークン(var(--surface) など)を使ってください: "${prop}: ${value}"`,
}, (decl) => {
  const v = clean(decl.value);
  if (HEX.test(v) || COLOR_FN.test(v)) return 'raw';
  if (isCustomProp(decl.prop) || COLOR_PROPS.test(decl.prop)) {
    const words = v.toLowerCase().split(/[\s,()/]+/);
    if (words.some((w) => NAMED.has(w))) return 'raw';
  }
  return null;
});

// ------------------------------------------------------------ no-shadow
export const noShadow = declRule('no-shadow', {
  shadow: (prop) => `影(${prop})は使いません。面の色の差で区切ってください。`,
}, (decl) => {
  const p = decl.prop.toLowerCase(), v = decl.value.trim().toLowerCase();
  if ((p === 'box-shadow' || p === 'text-shadow') && v !== 'none') return 'shadow';
  if (p === 'filter' && v.includes('drop-shadow')) return 'shadow';
  return null;
});

// ------------------------------------------------------------ border-only-on-inputs
const DEFAULT_INPUTS = ['input', 'select', 'textarea', '\\[contenteditable', '\\.k-input', '\\.k-check', '\\.k-radio'];
const BORDER_PROP = /^border(?:-(?:top|right|bottom|left|block|inline|block-start|block-end|inline-start|inline-end))?(?:-(?:width|style|color))?$/i;
const NO_BORDER = /^(?:none|0|0px|hidden|transparent|inherit|initial|unset|revert)$/i;

export const borderOnlyOnInputs = declRule('border-only-on-inputs', {
  border: (prop) => `枠線(${prop})を付けられるのは入力の部品だけです。カードやリストは面の色の差で区切ってください。`,
  outline: () => 'outline で枠を描くのは、フォーカスのリング(:focus / :focus-visible)だけにしてください。',
}, (decl, opts) => {
  const p = decl.prop.toLowerCase();
  const sel = decl.parent && decl.parent.selector ? decl.parent.selector : '';
  if (BORDER_PROP.test(p)) {
    if (NO_BORDER.test(decl.value.trim())) return null;
    const allowed = new RegExp((opts.inputSelectors || []).concat(DEFAULT_INPUTS).join('|'), 'i');
    // every selector in the list must be an input-like selector
    const parts = sel.split(',').map((s) => s.trim()).filter(Boolean);
    if (parts.length && parts.every((s) => allowed.test(s))) return null;
    return 'border';
  }
  if (p === 'outline' && !NO_BORDER.test(decl.value.trim()) && !/:focus/.test(sel)) return 'outline';
  return null;
}, { allowOptions: true });

// ------------------------------------------------------------ use-tokens
const LEN = /(^|[\s(,])-?\d*\.?\d+(px|rem|em|pt)\b/i;
const TIME = /(^|[\s,])\d*\.?\d+m?s\b/i;
const SPACE_PROPS = /^(?:padding|margin|gap|row-gap|column-gap|inset)(?:-.+)?$/i;

export const useTokens = declRule('use-tokens', {
  radius: () => '角丸は var(--r-lg) / var(--r-md) / var(--r-sm) / var(--r-full) か 50% を使ってください。',
  space: () => '余白は var(--space-1) 〜 var(--space-7) から選んでください。',
  size: () => '文字の大きさは var(--text-xs) 〜 var(--text-2xl) から選んでください。',
  time: () => '動きの長さは var(--motion-fast) / var(--motion-base) / var(--motion-slow) から選んでください。',
}, (decl) => {
  if (isCustomProp(decl.prop)) return null;
  const p = decl.prop.toLowerCase(), v = clean(decl.value).replace(/var\([^)]*\)/g, '');
  if (/^border(?:-[a-z]+)*-radius$/.test(p) && LEN.test(v)) return 'radius';
  if (SPACE_PROPS.test(p) && LEN.test(v)) return 'space';
  if (p === 'font-size' && LEN.test(v)) return 'size';
  if (/^(?:transition|animation)(?:-duration|-delay)?$/.test(p) && TIME.test(v)) return 'time';
  return null;
});

// ------------------------------------------------------------ no-outline-none
export const noOutlineNone = declRule('no-outline-none', {
  none: () => 'フォーカスのリングを消さないでください(outline: none は禁止)。',
}, (decl) => (decl.prop.toLowerCase() === 'outline' && /^(?:none|0|0px)$/i.test(decl.value.trim()) ? 'none' : null));

// ------------------------------------------------------------ font-family-token
export const fontFamilyToken = declRule('font-family-token', {
  font: () => '書体は var(--font-body) / var(--font-title) / var(--font-num) / var(--font-mono) で指定してください。',
}, (decl) => {
  const p = decl.prop.toLowerCase();
  if (p !== 'font-family' && p !== 'font') return null;
  const v = decl.value.trim();
  if (/var\(--font-/.test(v) || /^(?:inherit|initial|unset|revert)$/i.test(v)) return null;
  if (p === 'font' && /^(?:inherit|initial|unset|revert)$/i.test(v)) return null;
  return 'font';
});

export default [noRawColor, noShadow, borderOnlyOnInputs, useTokens, noOutlineNone, fontFamilyToken];
