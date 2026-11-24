/*! Kasane v2 — small helpers for the menu drawer, dialogs, tabs and the palette. No dependencies.
   Load with <script src="https://kasane.y-n0.de/v2/kasane.js" defer></script>. Everything still shows without it. */
(function () {
  'use strict';
  var root = document.documentElement;
  var KEY_ACCENT = 'kasane-accent', KEY_THEME = 'kasane-theme';
  var PALETTES = ["hidamari", "tachibana", "kobai", "fuji", "ai", "sora", "seiji", "moegi", "sumi"];
  var reduce = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var all = function (sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- Recolouring: the new colours flow down from the top ---------- */
  var running = 0;
  function recolor(update) {
    if (!document.startViewTransition || reduce.matches || document.visibilityState !== 'visible') { update(); return; }
    running++;
    root.classList.add('k-recolor');
    var t = document.startViewTransition(update);
    var done = function () { if (--running === 0) root.classList.remove('k-recolor'); };
    t.finished.then(done, done);
  }

  function accent() { return root.dataset.accent || 'hidamari'; }
  function syncPalette(id) {
    all('.k-palette input[type="radio"]').forEach(function (r) { r.checked = r.value === id; });
  }
  function setAccent(id, opts) {
    if (id === 'yamabuki') id = 'hidamari';
    if (PALETTES.indexOf(id) < 0) return;
    opts = opts || {};
    if (opts.save !== false) store.set(KEY_ACCENT, id);
    if (id === accent()) { syncPalette(id); return; }
    var apply = function () { root.dataset.accent = id; syncPalette(id); };
    if (opts.animate === false) apply(); else recolor(apply);
    root.dispatchEvent(new CustomEvent('kasane:accent', { detail: { accent: id } }));
  }
  /* For screenshots and previews only: products follow the device setting (see kasane.md). */
  function setTheme(theme, opts) {
    opts = opts || {};
    if (theme !== 'light' && theme !== 'dark') theme = null;
    if (opts.save) store.set(KEY_THEME, theme);
    var apply = function () { if (theme) root.dataset.theme = theme; else delete root.dataset.theme; };
    if (opts.animate === false) apply(); else recolor(apply);
  }

  /* ---------- Focus helpers ---------- */
  var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
  function focusables(el) { return all(FOCUSABLE, el).filter(function (e) { return e.offsetWidth || e.offsetHeight || e.getClientRects().length; }); }
  function trap(e, box) {
    if (e.key !== 'Tab') return;
    var f = focusables(box); if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }
  var locks = 0;
  function lock(on) { locks += on ? 1 : -1; root.classList.toggle('k-scroll-lock', locks > 0); }

  /* ---------- Menu drawer: .k-menu-btn[aria-controls] opens .k-sidebar (under 900px) ---------- */
  var openDrawer = null;
  function scrimFor() {
    var s = document.querySelector('.k-drawer-scrim');
    if (!s) { s = document.createElement('div'); s.className = 'k-drawer-scrim'; s.hidden = true; document.body.appendChild(s); }
    return s;
  }
  function drawer(btn, open) {
    var side = document.getElementById(btn.getAttribute('aria-controls')); if (!side) return;
    var scrim = scrimFor();
    if (open) {
      side.setAttribute('data-open', '');
      scrim.hidden = false; btn.setAttribute('aria-expanded', 'true'); lock(true);
      openDrawer = { btn: btn, side: side };
      var f = side.querySelector('[aria-current="page"]') || focusables(side)[0]; if (f) f.focus();
    } else {
      side.removeAttribute('data-open');
      scrim.hidden = true; btn.setAttribute('aria-expanded', 'false'); lock(false);
      openDrawer = null;
      btn.focus();
    }
  }
  function closeDrawer() { if (openDrawer) drawer(openDrawer.btn, false); }
  var wide = window.matchMedia ? window.matchMedia('(min-width: 900px)') : null;
  if (wide) (wide.addEventListener ? wide.addEventListener('change', function (e) { if (e.matches) closeDrawer(); }) : wide.addListener(function (e) { if (e.matches) closeDrawer(); }));

  /* ---------- Dialog: [data-k-dialog="id"] opens the .k-scrim with that id ---------- */
  var dialogs = [];
  function openDialog(id, opener) {
    var scrim = document.getElementById(id); if (!scrim) return;
    scrim.hidden = false; lock(true);
    dialogs.push({ scrim: scrim, opener: opener || document.activeElement });
    var box = scrim.querySelector('.k-dialog') || scrim;
    var f = focusables(box)[0]; if (f) f.focus();
  }
  function closeDialog() {
    var d = dialogs.pop(); if (!d) return;
    d.scrim.hidden = true; lock(false);
    if (d.opener && d.opener.focus) d.opener.focus();
  }

  /* ---------- Tabs: .k-seg[role="tablist"] ---------- */
  function selectTab(tab, focus) {
    var list = tab.closest('[role="tablist"]');
    all('[role="tab"]', list).forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1;
      var panel = document.getElementById(t.getAttribute('aria-controls')); if (panel) panel.hidden = !on;
    });
    if (focus) tab.focus();
  }

  /* ---------- Events ---------- */
  document.addEventListener('click', function (e) {
    var t = e.target;
    var menu = t.closest('.k-menu-btn[aria-controls]');
    if (menu) { drawer(menu, menu.getAttribute('aria-expanded') !== 'true'); return; }
    if (openDrawer && (t.closest('.k-drawer-scrim') || t.closest('[data-k-close]') && openDrawer.side.contains(t))) { closeDrawer(); return; }
    if (openDrawer && t.closest('a[href]') && openDrawer.side.contains(t)) { closeDrawer(); return; }
    var opener = t.closest('[data-k-dialog]');
    if (opener) { openDialog(opener.getAttribute('data-k-dialog'), opener); return; }
    if (dialogs.length) {
      var top = dialogs[dialogs.length - 1].scrim;
      if (t === top || (t.closest('[data-k-close]') && top.contains(t))) { closeDialog(); return; }
    }
    var tab = t.closest('.k-seg[role="tablist"] [role="tab"]');
    if (tab) selectTab(tab, false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { if (dialogs.length) { closeDialog(); return; } if (openDrawer) { closeDrawer(); return; } }
    if (dialogs.length) trap(e, dialogs[dialogs.length - 1].scrim);
    else if (openDrawer) trap(e, openDrawer.side);
    var tab = e.target.closest && e.target.closest('.k-seg[role="tablist"] [role="tab"]');
    if (tab && /^(ArrowLeft|ArrowRight|Home|End)$/.test(e.key)) {
      var tabs = all('[role="tab"]', tab.closest('[role="tablist"]')), i = tabs.indexOf(tab);
      i = e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
      e.preventDefault(); selectTab(tabs[i], true);
    }
  });
  document.addEventListener('change', function (e) {
    var r = e.target;
    if (r.matches && r.matches('.k-palette input[type="radio"]') && r.checked) setAccent(r.value);
  });

  /* ---------- Start ---------- */
  function start() {
    if (root.dataset.accent === 'yamabuki') root.dataset.accent = 'hidamari';
    syncPalette(accent());
    all('.k-seg[role="tablist"]').forEach(function (list) {
      var sel = list.querySelector('[role="tab"][aria-selected="true"]') || list.querySelector('[role="tab"]');
      if (sel) selectTab(sel, false);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();

  window.Kasane = { setAccent: setAccent, setTheme: setTheme, recolor: recolor, openDialog: openDialog, closeDialog: closeDialog, closeDrawer: closeDrawer, palettes: PALETTES.slice() };
})();
