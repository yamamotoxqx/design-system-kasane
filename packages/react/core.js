/* Kasane v2 core: palettes, the colour (with the top-down recolour), toasts and focus helpers.
   Shared by kasane.js, kasane-react and kasane-vue. Safe to import on the server (no DOM work until called). */
export var PALETTES = [{"id": "hidamari", "name": "ひだまり", "en": "Hidamari"}, {"id": "tachibana", "name": "橘", "en": "Tachibana"}, {"id": "kobai", "name": "紅梅", "en": "Kobai"}, {"id": "fuji", "name": "藤", "en": "Fuji"}, {"id": "ai", "name": "藍", "en": "Ai"}, {"id": "sora", "name": "空", "en": "Sora"}, {"id": "seiji", "name": "青磁", "en": "Seiji"}, {"id": "moegi", "name": "萌黄", "en": "Moegi"}, {"id": "sumi", "name": "墨", "en": "Sumi"}];
export var ICONS = {"check": [["path", {"d": "M20 6 9 17l-5-5"}]], "circle-alert": [["circle", {"cx": "12", "cy": "12", "r": "10"}], ["line", {"x1": "12", "x2": "12", "y1": "8", "y2": "12"}], ["line", {"x1": "12", "x2": "12.01", "y1": "16", "y2": "16"}]], "info": [["circle", {"cx": "12", "cy": "12", "r": "10"}], ["path", {"d": "M12 16v-4"}], ["path", {"d": "M12 8h.01"}]], "x": [["path", {"d": "M18 6 6 18"}], ["path", {"d": "m6 6 12 12"}]], "menu": [["path", {"d": "M4 5h16"}], ["path", {"d": "M4 12h16"}], ["path", {"d": "M4 19h16"}]], "search": [["path", {"d": "m21 21-4.34-4.34"}], ["circle", {"cx": "11", "cy": "11", "r": "8"}]], "user-plus": [["path", {"d": "M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"}], ["circle", {"cx": "9", "cy": "7", "r": "4"}], ["line", {"x1": "19", "x2": "19", "y1": "8", "y2": "14"}], ["line", {"x1": "22", "x2": "16", "y1": "11", "y2": "11"}]], "log-out": [["path", {"d": "m16 17 5-5-5-5"}], ["path", {"d": "M21 12H9"}], ["path", {"d": "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"}]]};

var hasDOM = typeof document !== 'undefined';
var KEY_ACCENT = 'kasane-accent';
var store = {
  get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set: function (k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
};
function isPalette(id) { for (var i = 0; i < PALETTES.length; i++) if (PALETTES[i].id === id) return true; return false; }
function reduced() { return hasDOM && window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
function lang() { return hasDOM && /^en/.test(document.documentElement.lang || '') ? 'en' : 'ja'; }

/* ---------- Icons (Lucide, ISC) as SVG text, for DOM made outside a framework ---------- */
export function iconSvg(name) {
  var d = ICONS[name]; if (!d) return '';
  return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-' + name + '" aria-hidden="true">'
    + d.map(function (c) { return '<' + c[0] + Object.keys(c[1]).map(function (k) { return ' ' + k + '="' + c[1][k] + '"'; }).join('') + '/>'; }).join('') + '</svg>';
}

/* ---------- Colour ---------- */
export function getAccent() {
  if (!hasDOM) return 'hidamari';
  var a = document.documentElement.dataset.accent;
  return a && a !== 'yamabuki' ? a : 'hidamari';
}
var running = 0;
/* Run update() so that the new colours flow down from the top (View Transitions). */
export function recolor(update) {
  if (!hasDOM || !document.startViewTransition || reduced() || document.visibilityState !== 'visible') { update(); return; }
  var root = document.documentElement;
  running++; root.classList.add('k-recolor');
  var done = function () { if (--running === 0) root.classList.remove('k-recolor'); };
  document.startViewTransition(update).finished.then(done, done);
}
export function setAccent(id, opts) {
  if (id === 'yamabuki') id = 'hidamari';
  if (!hasDOM || !isPalette(id)) return;
  opts = opts || {};
  var root = document.documentElement;
  if (opts.save !== false) store.set(KEY_ACCENT, id);
  if (root.dataset.accent === id) return;
  var apply = function () {
    root.dataset.accent = id;
    root.dispatchEvent(new CustomEvent('kasane:accent', { detail: { accent: id } }));
  };
  if (opts.animate === false) apply(); else recolor(apply);
}
/* Call fn(accent) whenever the colour changes. Returns a function that stops listening. */
export function onAccent(fn) {
  if (!hasDOM) return function () {};
  var h = function (e) { fn(e.detail.accent); };
  document.documentElement.addEventListener('kasane:accent', h);
  return function () { document.documentElement.removeEventListener('kasane:accent', h); };
}
/* Apply the saved colour (v1's "yamabuki" becomes "hidamari"). The <head> script normally does this first. */
export function restoreAccent() {
  if (!hasDOM) return;
  var a = store.get(KEY_ACCENT);
  if (a === 'yamabuki') { a = 'hidamari'; store.set(KEY_ACCENT, a); }
  if (a && isPalette(a)) document.documentElement.dataset.accent = a;
  else if (document.documentElement.dataset.accent === 'yamabuki') document.documentElement.dataset.accent = 'hidamari';
}

/* ---------- Focus and scroll ---------- */
export var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
export function focusables(el) {
  return Array.prototype.slice.call(el.querySelectorAll(FOCUSABLE)).filter(function (e) { return e.offsetWidth || e.offsetHeight || e.getClientRects().length; });
}
/* Keep Tab inside box (for dialogs and the open menu). */
export function trapFocus(e, box) {
  if (e.key !== 'Tab' || !box) return;
  var f = focusables(box); if (!f.length) return;
  var first = f[0], last = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
}
var locks = 0;
export function lockScroll(on) {
  if (!hasDOM) return;
  locks = Math.max(0, locks + (on ? 1 : -1));
  document.documentElement.classList.toggle('k-scroll-lock', locks > 0);
}

/* ---------- Toasts: shown at the bottom, closed by themselves ----------
   toast('保存しました', { type: 'ok' })                  ok | info | danger, or nothing
   toast('削除しました', { action: { label: '元に戻す', onClick: undo } })
   Plain toasts close after 5 s, toasts with an action after 10 s. Errors (danger) stay until closed.
   The same message again (not danger, no action) is merged into the toast on screen as "×2"; { merge: false } turns this off.
   The timer stops while the pointer is on the toast, while it has focus, and while the page is hidden. */
var TOAST_MAX = 3;
export function toastRegion() {
  if (!hasDOM || !document.body) return null;
  var r = document.querySelector('.k-toasts');
  if (!r) { r = document.createElement('div'); r.className = 'k-toasts'; r.setAttribute('aria-live', 'polite'); document.body.appendChild(r); }
  return r;
}
export function toast(message, opts) {
  var region = toastRegion();
  if (!region) return { close: function () {} };
  opts = opts || {};
  var type = opts.type, en = lang() === 'en';
  /* The same low-importance toast again (not danger, no action): merge into the one on screen,
     show the count and start its timer over, so a burst of saves does not pile up. */
  var key = (type || '') + '|' + message, mergeable = type !== 'danger' && !opts.action && opts.merge !== false;
  if (mergeable) {
    for (var n = region.firstChild; n; n = n.nextSibling) if (n.kasaneKey === key && n.kasaneRepeat) return n.kasaneRepeat();
  }
  var count = 1;
  var el = document.createElement('div');
  el.className = 'k-toast';
  if (type === 'danger') el.setAttribute('role', 'alert');
  var icon = { ok: 'check', danger: 'circle-alert', info: 'info' }[type];
  if (icon) el.insertAdjacentHTML('beforeend', iconSvg(icon));
  var text = document.createElement('span');
  text.className = 'k-toast-text'; text.textContent = message; el.appendChild(text);
  var closed = false, timer = null, left, started;
  function close() {
    if (closed) return; closed = true; clearTimeout(timer);
    document.removeEventListener('visibilitychange', vis);
    var hadFocus = el.contains(document.activeElement);
    if (el.parentNode) el.parentNode.removeChild(el);
    if (hadFocus && opts.returnFocus && opts.returnFocus.focus) opts.returnFocus.focus();
    if (opts.onClose) opts.onClose();
  }
  if (opts.action) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'k-toast-action'; b.textContent = opts.action.label;
    b.addEventListener('click', function () { if (opts.action.onClick) opts.action.onClick(); close(); });
    el.appendChild(b);
  }
  var duration = opts.duration != null ? opts.duration : type === 'danger' ? 0 : opts.action ? 10000 : 5000;
  if (duration === 0 || opts.action || opts.closable) {
    var c = document.createElement('button');
    c.type = 'button'; c.className = 'k-toast-close';
    c.setAttribute('aria-label', opts.closeLabel || (en ? 'Close' : '閉じる'));
    c.innerHTML = iconSvg('x');
    c.addEventListener('click', close);
    el.appendChild(c);
  }
  function run() { if (closed || !duration || timer) return; started = Date.now(); timer = setTimeout(close, left); }
  function pause() { if (!timer) return; clearTimeout(timer); timer = null; left -= Date.now() - started; }
  function vis() { if (document.visibilityState === 'hidden') pause(); else if (!hovered && !focused) run(); }
  var hovered = false, focused = false;
  left = duration;
  el.addEventListener('mouseenter', function () { hovered = true; pause(); });
  el.addEventListener('mouseleave', function () { hovered = false; if (!focused) run(); });
  el.addEventListener('focusin', function () { focused = true; pause(); });
  el.addEventListener('focusout', function (e) { if (!el.contains(e.relatedTarget)) { focused = false; if (!hovered) run(); } });
  document.addEventListener('visibilitychange', vis);
  el.kasaneClose = close;
  if (mergeable) {
    el.kasaneKey = key;
    el.kasaneRepeat = function () {
      count++;
      text.textContent = message + ' ×' + count;
      left = duration;
      if (timer) { clearTimeout(timer); timer = null; }
      if (!hovered && !focused && document.visibilityState !== 'hidden') run();
      return { close: close };
    };
  }
  region.appendChild(el);
  while (region.children.length > TOAST_MAX) {
    var f = region.firstChild;
    if (f.kasaneClose) f.kasaneClose(); else region.removeChild(f);
  }
  if (document.visibilityState !== 'hidden') run();
  return { close: close };
}
