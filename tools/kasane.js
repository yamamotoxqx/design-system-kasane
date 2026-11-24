/*! Kasane {{VERSION}} — the menu drawer, dialogs, tabs, the palette and toasts. No dependencies.
   Load with <script src="{{BASE}}/kasane.js" defer></script>. Everything still shows without it. */
(function () {
  'use strict';
/*@@CORE@@*/
  var root = document.documentElement;
  var all = function (sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); };
  function syncPalette(id) { all('.k-palette input[type="radio"]').forEach(function (r) { r.checked = r.value === id; }); }
  onAccent(syncPalette);

  /* For screenshots and previews only: products follow the device setting (see kasane.md). */
  function setTheme(theme, opts) {
    opts = opts || {};
    if (theme !== 'light' && theme !== 'dark') theme = null;
    if (opts.save) { try { if (theme) localStorage.setItem('kasane-theme', theme); else localStorage.removeItem('kasane-theme'); } catch (e) {} }
    var apply = function () { if (theme) root.dataset.theme = theme; else delete root.dataset.theme; };
    if (opts.animate === false) apply(); else recolor(apply);
  }

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
      scrim.hidden = false; btn.setAttribute('aria-expanded', 'true'); lockScroll(true);
      openDrawer = { btn: btn, side: side };
      var f = side.querySelector('[aria-current="page"]') || focusables(side)[0]; if (f) f.focus();
    } else {
      side.removeAttribute('data-open');
      scrim.hidden = true; btn.setAttribute('aria-expanded', 'false'); lockScroll(false);
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
    scrim.hidden = false; lockScroll(true);
    dialogs.push({ scrim: scrim, opener: opener || document.activeElement });
    var box = scrim.querySelector('.k-dialog') || scrim;
    var f = focusables(box)[0]; if (f) f.focus();
  }
  function closeDialog() {
    var d = dialogs.pop(); if (!d) return;
    d.scrim.hidden = true; lockScroll(false);
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
    var toaster = t.closest('[data-k-toast]');
    if (toaster) { toast(toaster.getAttribute('data-k-toast'), { type: toaster.getAttribute('data-k-toast-type') || undefined }); return; }
    var tab = t.closest('.k-seg[role="tablist"] [role="tab"]');
    if (tab) selectTab(tab, false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { if (dialogs.length) { closeDialog(); return; } if (openDrawer) { closeDrawer(); return; } }
    if (dialogs.length) trapFocus(e, dialogs[dialogs.length - 1].scrim);
    else if (openDrawer) trapFocus(e, openDrawer.side);
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
    restoreAccent();
    syncPalette(getAccent());
    toastRegion();
    all('.k-seg[role="tablist"]').forEach(function (list) {
      var sel = list.querySelector('[role="tab"][aria-selected="true"]') || list.querySelector('[role="tab"]');
      if (sel) selectTab(sel, false);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();

  window.Kasane = {
    setAccent: setAccent, getAccent: getAccent, onAccent: onAccent, setTheme: setTheme, recolor: recolor, toast: toast,
    openDialog: openDialog, closeDialog: closeDialog, closeDrawer: closeDrawer,
    palettes: PALETTES.map(function (p) { return p.id; })
  };
})();
