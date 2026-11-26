/* kasane-react — Kasane components for React 18 and 19.
   Every component renders the same HTML as kasane.md, so kasane.css styles it and kasane-check accepts it.
   No JSX, no build step: React.createElement only. */
import * as React from 'react';
import {
  PALETTES, ICONS, getAccent, setAccent, onAccent, restoreAccent, recolor, toast,
  FOCUSABLE, focusables, trapFocus, lockScroll
} from './core.js';

export { PALETTES, getAccent, setAccent, onAccent, restoreAccent, recolor, toast };

var h = React.createElement;
var Fragment = React.Fragment;
function cx() { return Array.prototype.filter.call(arguments, Boolean).join(' '); }
function omit(o, keys) { var r = {}; for (var k in o) if (keys.indexOf(k) < 0) r[k] = o[k]; return r; }
var STATUS_ICON = { ok: 'check', danger: 'circle-alert', info: 'info' };
var useIso = typeof window !== 'undefined' ? React.useLayoutEffect : React.useEffect;
function useLatest(v) { var r = React.useRef(v); useIso(function () { r.current = v; }); return r; }

/* ---------- Icon: the few Lucide icons Kasane needs itself. Use lucide-react for the rest. ---------- */
export function Icon(p) {
  var d = ICONS[p.name];
  if (!d) return null;
  return h('svg', {
    xmlns: 'http://www.w3.org/2000/svg', width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none',
    stroke: 'currentColor', strokeWidth: 2, strokeLinecap: 'round', strokeLinejoin: 'round',
    className: cx('lucide lucide-' + p.name, p.className), 'aria-hidden': 'true'
  }, d.map(function (c, i) { return h(c[0], Object.assign({ key: i }, c[1])); }));
}
function iconNode(icon) { return typeof icon === 'string' ? h(Icon, { name: icon }) : icon || null; }

/* ---------- Button ---------- */
export var Button = React.forwardRef(function Button(p, ref) {
  var tag = p.href ? 'a' : 'button';
  var props = omit(p, ['variant', 'size', 'icon', 'className', 'children']);
  props.ref = ref;
  props.className = cx('k-btn', p.variant && 'k-btn-' + p.variant, p.size && 'k-btn-' + p.size, p.icon && p.children == null && 'k-btn-icon', p.className);
  if (tag === 'button' && !props.type) props.type = 'button';
  return h(tag, props, iconNode(p.icon), p.children);
});

/* ---------- Fields ---------- */
var FIELD_KEYS = ['label', 'hint', 'error', 'start', 'end', 'fieldClassName', 'className', 'options', 'children'];
function useField(p) {
  var auto = React.useId();
  var id = p.id || auto;
  var hintId = p.hint ? id + '-hint' : null, errorId = p.error ? id + '-error' : null;
  return {
    id: id,
    control: function (extra) {
      return Object.assign(omit(p, FIELD_KEYS), extra, {
        id: id,
        className: cx('k-input', p.className),
        'aria-invalid': p.error ? 'true' : p['aria-invalid'],
        'aria-describedby': [hintId, errorId, p['aria-describedby']].filter(Boolean).join(' ') || undefined
      });
    },
    wrap: function (control) {
      if (p.start || p.end) {
        control = h('span', { className: 'k-affix' },
          p.start ? h('span', { className: 'k-affix-start', 'aria-hidden': 'true' }, iconNode(p.start)) : null,
          control,
          p.end ? h('span', { className: 'k-affix-end' }, p.end) : null);
      }
      return h('label', { className: cx('k-field', p.fieldClassName) }, p.label, control,
        p.hint ? h('span', { className: 'k-hint', id: hintId }, p.hint) : null,
        p.error ? h('span', { className: 'k-error', id: errorId }, h(Icon, { name: 'circle-alert' }), p.error) : null);
    }
  };
}
/* <TextField label="お名前" hint="…" error="…" start="search" end="円" type="number" /> */
export var TextField = React.forwardRef(function TextField(p, ref) {
  var f = useField(p);
  return f.wrap(h('input', f.control({ type: p.type || 'text', ref: ref })));
});
/* type: date (default), time, datetime-local, month, week */
export var DateField = React.forwardRef(function DateField(p, ref) {
  return h(TextField, Object.assign({}, p, { type: p.type || 'date', ref: ref }));
});
export var SearchField = React.forwardRef(function SearchField(p, ref) {
  return h(TextField, Object.assign({ start: 'search' }, p, { type: 'search', ref: ref }));
});
export var TextArea = React.forwardRef(function TextArea(p, ref) {
  var f = useField(p);
  return f.wrap(h('textarea', f.control({ rows: p.rows || 4, ref: ref })));
});
/* options: [{ value, label }] or <option> children */
export var Select = React.forwardRef(function Select(p, ref) {
  var f = useField(p);
  var opts = p.options ? p.options.map(function (o) { return h('option', { key: o.value, value: o.value, disabled: o.disabled }, o.label); }) : p.children;
  return f.wrap(h('span', { className: 'k-select' }, h('select', f.control({ ref: ref }), opts)));
});
/* <DateRange legend="期間" start={{ label: '開始日', value, onChange }} end={{ … }} /> */
export function DateRange(p) {
  var type = p.type || 'date';
  return h('fieldset', { className: cx('k-range', p.className) },
    h('legend', null, p.legend),
    h(DateField, Object.assign({ type: type, max: p.end && p.end.value || undefined }, p.start)),
    h('span', { className: 'k-range-sep', 'aria-hidden': 'true' }, p.separator || '〜'),
    h(DateField, Object.assign({ type: type, min: p.start && p.start.value || undefined }, p.end)));
}

/* ---------- Checkbox, radio, switch ---------- */
function option(cls) {
  return React.forwardRef(function (p, ref) {
    var props = omit(p, ['label', 'children', 'className']);
    props.ref = ref;
    props.type = cls === 'k-radio' ? 'radio' : 'checkbox';
    props.className = cls;
    return h('label', { className: cx('k-option', p.className) }, h('input', props), ' ', p.label != null ? p.label : p.children);
  });
}
export var Checkbox = option('k-check');
export var Radio = option('k-radio');
export var Switch = React.forwardRef(function Switch(p, ref) {
  var props = omit(p, ['label', 'children', 'className']);
  props.ref = ref; props.type = 'checkbox';
  return h('label', { className: cx('k-switch', p.className) }, h('input', props),
    h('span', { className: 'k-switch-track', 'aria-hidden': 'true' }), p.label != null ? p.label : p.children);
});

/* ---------- Surfaces ---------- */
function rest(p, keys) { return omit(p, keys.concat(['className', 'children'])); }
export function Card(p) {
  var T = p.titleAs || 'h3';
  return h('div', Object.assign(rest(p, ['title', 'titleAs', 'text']), { className: cx('k-card', p.className) }),
    p.title != null ? h(T, { className: 'k-card-title' }, p.title) : null,
    p.text != null ? h('p', { className: 'k-card-text' }, p.text) : null,
    p.children);
}
export function Nest(p) { return h('div', Object.assign(rest(p, []), { className: cx('k-nest', p.className) }), p.children); }
export function Notice(p) {
  var T = p.titleAs || 'h3';
  return h('div', Object.assign(rest(p, ['title', 'titleAs']), { className: cx('k-notice', p.className) }),
    p.title != null ? h(T, { className: 'k-notice-title' }, p.title) : null, h('div', null, p.children));
}
export function List(p) { return h('ul', Object.assign(rest(p, []), { className: cx('k-list', p.className) }), p.children); }
export function ListItem(p) {
  return h('li', Object.assign(rest(p, ['main', 'sub']), { className: cx('k-list-item', p.className) }),
    h('span', { className: 'k-list-item-main' }, p.main), p.sub != null ? h('span', { className: 'k-list-item-sub' }, p.sub) : null, p.children);
}
/* tone: accent | ok | danger | info. ok, danger and info get their icon. */
export function Badge(p) {
  return h('span', Object.assign(rest(p, ['tone']), { className: cx('k-badge', p.tone && 'k-badge-' + p.tone, p.className) }),
    STATUS_ICON[p.tone] ? h(Icon, { name: STATUS_ICON[p.tone] }) : null, p.children);
}

/* ---------- Tabs and the two-way switch ---------- */
/* <Tabs label="説明" tabs={[{ id: 'a', label: '概要', content: … }]} value? onChange? /> */
export function Tabs(p) {
  var base = React.useId();
  var st = React.useState(p.defaultValue != null ? p.defaultValue : p.tabs[0] && p.tabs[0].id);
  var value = p.value != null ? p.value : st[0];
  var refs = React.useRef({});
  function select(id, focus) {
    if (p.value == null) st[1](id);
    if (p.onChange) p.onChange(id);
    if (focus && refs.current[id]) refs.current[id].focus();
  }
  function onKey(e, i) {
    var n = p.tabs.length, j = null;
    if (e.key === 'ArrowRight') j = (i + 1) % n; else if (e.key === 'ArrowLeft') j = (i - 1 + n) % n;
    else if (e.key === 'Home') j = 0; else if (e.key === 'End') j = n - 1;
    if (j != null) { e.preventDefault(); select(p.tabs[j].id, true); }
  }
  return h(Fragment, null,
    h('div', { className: cx('k-seg', p.className), role: 'tablist', 'aria-label': p.label },
      p.tabs.map(function (t, i) {
        var on = t.id === value;
        return h('button', {
          key: t.id, ref: function (el) { refs.current[t.id] = el; }, type: 'button', role: 'tab',
          id: base + 'tab-' + t.id, 'aria-controls': base + 'panel-' + t.id, 'aria-selected': String(on), tabIndex: on ? 0 : -1,
          onClick: function () { select(t.id); }, onKeyDown: function (e) { onKey(e, i); }
        }, t.label);
      })),
    p.tabs.map(function (t) {
      return h('div', { key: t.id, className: 'k-nest', role: 'tabpanel', id: base + 'panel-' + t.id, 'aria-labelledby': base + 'tab-' + t.id, hidden: t.id !== value }, t.content);
    }));
}
/* <Segmented label="並び順" options={[{ value: 'new', label: '新しい順' }, …]} value onChange /> */
export function Segmented(p) {
  return h('div', { className: cx('k-seg', p.className), role: 'group', 'aria-label': p.label },
    p.options.map(function (o) {
      return h('button', { key: o.value, type: 'button', 'aria-pressed': String(o.value === p.value), onClick: function () { if (p.onChange) p.onChange(o.value); } }, o.label);
    }));
}

/* ---------- Progress ---------- */
export function Progress(p) {
  var max = p.max || 100, pct = Math.round(Math.max(0, Math.min(1, (p.value || 0) / max)) * 100);
  return h(Fragment, null,
    h('div', { className: 'k-bar-head' }, h('span', null, p.label), h('span', { className: 'k-num' }, pct + '%')),
    h('div', { className: 'k-bar', role: 'progressbar', 'aria-label': p.label, 'aria-valuenow': pct, 'aria-valuemin': 0, 'aria-valuemax': 100 },
      h('i', { style: { width: pct + '%' } })));
}

/* ---------- Dialog ---------- */
/* <Dialog open onClose title="このメモを削除しますか?" text="削除すると元に戻せません。" actions={<>…</>} /> */
export function Dialog(p) {
  var titleId = React.useId();
  var box = React.useRef(null);
  var onClose = useLatest(p.onClose);
  React.useEffect(function () {
    if (!p.open) return;
    var opener = document.activeElement;
    var f = box.current && focusables(box.current)[0]; if (f) f.focus();
    lockScroll(true);
    function key(e) { if (e.key === 'Escape') { if (onClose.current) onClose.current(); } else trapFocus(e, box.current); }
    document.addEventListener('keydown', key);
    return function () {
      document.removeEventListener('keydown', key); lockScroll(false);
      if (opener && opener.focus) opener.focus();
    };
  }, [p.open]);
  if (!p.open) return null;
  return h('div', { className: 'k-scrim', onMouseDown: function (e) { if (e.target === e.currentTarget && onClose.current) onClose.current(); } },
    h('div', { ref: box, className: cx('k-dialog', p.className), role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': titleId },
      h('h3', { className: 'k-dialog-title', id: titleId }, p.title),
      p.text != null ? h('p', { className: 'k-dialog-text' }, p.text) : null,
      p.children,
      p.actions ? h('div', { className: 'k-dialog-actions' }, p.actions) : null));
}

/* ---------- Colour ---------- */
/* const [accent, setAccent] = useAccent(); setAccent('ai') repaints from the top and saves the choice. */
export function useAccent() {
  var st = React.useState('hidamari');
  React.useEffect(function () { st[1](getAccent()); return onAccent(st[1]); }, []);
  return [st[0], setAccent];
}
export function Palette(p) {
  var a = useAccent();
  var name = p.name || 'accent', en = p.lang === 'en';
  return h('fieldset', { className: cx('k-palette', p.compact && 'k-palette-compact', p.className) },
    h('legend', null, p.legend || (en ? 'Theme colour' : 'テーマカラー')),
    h('div', { className: 'k-palette-items' }, PALETTES.map(function (c) {
      return h('label', { key: c.id, className: 'k-palette-item' },
        h('input', { type: 'radio', name: name, value: c.id, checked: a[0] === c.id, onChange: function () { a[1](c.id); } }),
        h('span', { className: 'k-palette-swatch', 'data-swatch': c.id }),
        h('span', { className: 'k-palette-name' }, en ? c.en : c.name));
    })));
}

/* ---------- Page frame: header, menu button, sidebar (a drawer under 900px), main, footer ---------- */
/* <AppShell brand="かさね帳" logo={<Logo />} actions={…} sidebar={<NavGroup>…</NavGroup>} footer={<Footer … />}>…</AppShell> */
export function AppShell(p) {
  var sideId = React.useId();
  var st = React.useState(false), open = st[0], setOpen = st[1];
  var btn = React.useRef(null), side = React.useRef(null), wasOpen = React.useRef(false);
  var en = p.lang === 'en';
  var navLabel = p.navLabel || (en ? 'Main' : 'メイン');
  React.useEffect(function () {
    if (!open) { if (wasOpen.current && btn.current) btn.current.focus(); wasOpen.current = false; return; }
    wasOpen.current = true;
    var f = side.current && (side.current.querySelector('[aria-current="page"]') || focusables(side.current)[0]); if (f) f.focus();
    lockScroll(true);
    function key(e) { if (e.key === 'Escape') setOpen(false); else trapFocus(e, side.current); }
    var wide = window.matchMedia('(min-width: 900px)');
    function change(e) { if (e.matches) setOpen(false); }
    document.addEventListener('keydown', key);
    wide.addEventListener('change', change);
    return function () { document.removeEventListener('keydown', key); wide.removeEventListener('change', change); lockScroll(false); };
  }, [open]);
  var hasSide = p.sidebar != null;
  var sidebar = hasSide ? h('nav', {
    ref: side, className: 'k-sidebar', id: sideId, 'aria-label': navLabel, 'data-open': open ? '' : undefined,
    onClick: function (e) { if (e.target.closest && e.target.closest('a[href]')) setOpen(false); }
  },
    h('div', { className: 'k-sidebar-head' },
      h('span', { className: 'k-header-brand' }, p.logo, p.brand),
      h(Button, { variant: 'quiet', icon: 'x', 'aria-label': p.closeLabel || (en ? 'Close menu' : 'メニューを閉じる'), 'data-k-close': '', onClick: function () { setOpen(false); } })),
    p.sidebar) : null;
  return h('div', { className: cx('k-app', p.className) },
    h('header', { className: 'k-header' },
      hasSide ? h('button', {
        ref: btn, className: 'k-menu-btn', type: 'button', 'aria-label': p.menuLabel || (en ? 'Menu' : 'メニュー'),
        'aria-expanded': String(open), 'aria-controls': sideId, onClick: function () { setOpen(!open); }
      }, h(Icon, { name: 'menu' })) : null,
      h(p.brandAs || 'a', { className: 'k-header-brand', href: p.brandHref || '/' }, p.logo, p.brand),
      p.headerNav ? h('nav', { className: 'k-header-nav', 'aria-label': navLabel }, p.headerNav) : null,
      h('span', { className: 'k-header-space' }),
      p.actions),
    hasSide ? h('div', { className: 'k-drawer-scrim', hidden: !open, onClick: function () { setOpen(false); } }) : null,
    p.single ? sidebar : null,
    h('div', { className: cx('k-layout', p.single && 'k-layout-single') },
      p.single ? null : sidebar,
      h('main', { className: cx('k-main', p.plain && 'k-main-plain') }, p.children)),
    p.footer);
}
export function NavGroup(p) {
  return h('div', { className: cx('k-nav', p.className) }, p.title != null ? h('p', { className: 'k-nav-title' }, p.title) : null, p.children);
}
/* as: a router link component (Next.js Link, React Router NavLink…). current: this page. */
export function NavLink(p) {
  var props = rest(p, ['as', 'current', 'icon', 'badge']);
  props.className = cx('k-nav-link', p.className);
  props['aria-current'] = p.current ? 'page' : undefined;
  return h(p.as || 'a', props, iconNode(p.icon), p.children, p.badge != null ? h(Badge, { tone: 'accent' }, p.badge) : null);
}
/* items: [{ label, href }]; the last one is the current page */
export function Breadcrumb(p) {
  var n = p.items.length;
  return h('nav', { 'aria-label': p.label || (p.lang === 'en' ? 'Breadcrumb' : 'パンくずリスト') },
    h('ol', { className: 'k-breadcrumb' }, p.items.map(function (it, i) {
      return i === n - 1 ? h('li', { key: i, 'aria-current': 'page' }, it.label)
        : h('li', { key: i }, h(p.linkAs || 'a', { href: it.href }, it.label));
    })));
}
export function Footer(p) {
  return h('footer', { className: cx('k-footer', p.className) },
    h('div', { className: 'k-footer-in' },
      p.links ? h('nav', { className: 'k-footer-links', 'aria-label': p.linksLabel || (p.lang === 'en' ? 'About this site' : 'このサイトについて') },
        p.links.map(function (l, i) { return h(p.linkAs || 'a', { key: i, href: l.href }, l.label); })) : null,
      p.palette ? h(Palette, { compact: true, name: 'accent-footer', lang: p.lang }) : null,
      p.children,
      p.note != null ? h('p', { className: 'k-footer-note' }, p.note) : null));
}

/* ---------- Avatar and account ---------- */
var AVATAR_PX = { sm: 28, lg: 64 };
function initial(name) { var t = (name || '').trim(); return t ? Array.from(t)[0].toUpperCase() : '?'; }
/* <Avatar name="青木 ゆい" src? size="sm | lg" />. It is not read aloud: name the button that holds it. */
export function Avatar(p) {
  var cls = cx('k-avatar', p.size && 'k-avatar-' + p.size, p.className), px = AVATAR_PX[p.size] || 36;
  return p.src ? h('img', { className: cls, src: p.src, alt: '', width: px, height: px })
    : h('span', { className: cls, 'aria-hidden': 'true' }, initial(p.name));
}
/* <Account user={{ name, email, image }} accounts={[…]} manageHref="/account/" onSwitch onAdd onLogout links={[…]} />
   Put it at the right end of the header (AppShell's actions). Without user it shows the sign-in button. */
export function Account(p) {
  var id = React.useId();
  var st = React.useState(false), open = st[0], setOpen = st[1];
  var btn = React.useRef(null), panel = React.useRef(null), wasOpen = React.useRef(false);
  var en = p.lang === 'en';
  React.useEffect(function () {
    if (!open) { if (wasOpen.current && btn.current) btn.current.focus(); wasOpen.current = false; return; }
    wasOpen.current = true;
    var f = panel.current && focusables(panel.current)[0]; if (f) f.focus();
    lockScroll(true);
    function key(e) { if (e.key === 'Escape') setOpen(false); else trapFocus(e, panel.current); }
    document.addEventListener('keydown', key);
    return function () { document.removeEventListener('keydown', key); lockScroll(false); };
  }, [open]);
  if (!p.user) {
    return p.loginHref ? h(Button, { href: p.loginHref }, en ? 'Sign in' : 'ログイン')
      : h(Button, { onClick: p.onLogin }, en ? 'Sign in' : 'ログイン');
  }
  var u = p.user, others = p.accounts || [];
  function close() { setOpen(false); }
  return h(Fragment, null,
    h('button', {
      ref: btn, className: 'k-account-btn', type: 'button', 'aria-label': (en ? 'Account: ' : 'アカウント: ') + u.name,
      'aria-expanded': String(open), 'aria-controls': id, onClick: function () { setOpen(!open); }
    }, h(Avatar, { name: u.name, src: u.image })),
    h('div', { className: 'k-drawer-scrim', hidden: !open, onClick: close }),
    h('div', { ref: panel, className: 'k-account', id: id, role: 'dialog', 'aria-modal': 'true', 'aria-label': en ? 'Account' : 'アカウント', 'data-open': open ? '' : undefined },
      h('div', { className: 'k-account-head' },
        h(Avatar, { name: u.name, src: u.image, size: 'lg' }),
        h('div', null, h('p', { className: 'k-account-name' }, u.name), u.email ? h('p', { className: 'k-account-email' }, u.email) : null),
        h(Button, { variant: 'quiet', icon: 'x', 'aria-label': en ? 'Close' : '閉じる', 'data-k-close': '', onClick: close })),
      p.manageHref ? h(Button, { href: p.manageHref }, en ? 'Manage account' : 'アカウントを管理') : null,
      others.length ? h('p', { className: 'k-account-title' }, en ? 'Other accounts' : 'ほかのアカウント') : null,
      others.length ? h('ul', { className: 'k-account-list' }, others.map(function (a, i) {
        return h('li', { key: a.email || i }, h('button', { className: 'k-account-item', type: 'button', onClick: function () { close(); if (p.onSwitch) p.onSwitch(a); } },
          h(Avatar, { name: a.name, src: a.image }),
          h('span', null, h('span', { className: 'k-account-name' }, a.name), a.email ? h('span', { className: 'k-account-email' }, a.email) : null)));
      })) : null,
      p.onAdd || p.onLogout ? h('div', { className: 'k-account-actions' },
        p.onAdd ? h(Button, { variant: 'quiet', icon: 'user-plus', onClick: function () { close(); p.onAdd(); } }, en ? 'Add account' : 'アカウントを追加') : null,
        p.onLogout ? h(Button, { variant: 'quiet', icon: 'log-out', onClick: function () { close(); p.onLogout(); } }, en ? 'Sign out' : 'ログアウト') : null) : null,
      p.links ? h('nav', { className: 'k-account-links', 'aria-label': en ? 'Legal' : '規約' }, p.links.map(function (l, i) { return h('a', { key: i, href: l.href }, l.label); })) : null));
}

/* ---------- Table, empty state, loading ---------- */
/* columns: [{ key, label, numeric }]; rows: objects (render(row) for custom cells) */
export function Table(p) {
  return h('div', { className: 'k-table-wrap', role: 'region', 'aria-label': p.label || p.caption, tabIndex: 0 },
    h('table', { className: cx('k-table', p.className) },
      p.caption != null ? h('caption', null, p.caption) : null,
      h('thead', null, h('tr', null, p.columns.map(function (c) {
        return h('th', { key: c.key, scope: 'col', className: c.numeric ? 'k-num' : undefined }, c.label);
      }))),
      h('tbody', null, p.rows.map(function (r, i) {
        return h('tr', { key: p.rowKey ? r[p.rowKey] : i }, p.columns.map(function (c) {
          return h('td', { key: c.key, className: c.numeric ? 'k-num' : undefined }, c.render ? c.render(r) : r[c.key]);
        }));
      }))));
}
export function Empty(p) {
  var T = p.titleAs || 'h3';
  return h('div', { className: cx('k-empty', p.className) },
    h('div', { className: 'k-empty-icon' }, iconNode(p.icon || 'info')),
    h(T, { className: 'k-empty-title' }, p.title),
    p.text != null ? h('p', { className: 'k-empty-text' }, p.text) : null,
    p.children ? h('div', { className: 'k-empty-actions' }, p.children) : null);
}
export function Skeleton(p) {
  var lines = p.lines || 3, out = [];
  if (p.title !== false) out.push(h('span', { key: 't', className: 'k-skeleton-title' }));
  for (var i = 0; i < lines; i++) out.push(h('span', { key: i, className: cx('k-skeleton-line', i === lines - 1 && lines > 1 && 'k-skeleton-short') }));
  return h('div', { className: cx(p.card === false ? null : 'k-card', p.className), 'aria-busy': 'true' },
    h('span', { className: 'k-visually-hidden' }, p.label || (p.lang === 'en' ? 'Loading' : '読み込んでいます')),
    h('div', { className: 'k-skeleton', 'aria-hidden': 'true' }, out));
}

/* ---------- Toasts ---------- */
/* const show = useToast(); show('保存しました', { type: 'ok' }). Same as toast() from the core. */
export function useToast() { return toast; }
