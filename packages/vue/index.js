/* kasane-vue — Kasane components for Vue 3.5+.
   Every component renders the same HTML as kasane.md, so kasane.css styles it and kasane-check accepts it.
   No SFC, no build step: render functions only. app.use(Kasane) registers every component (KButton, KTextField…). */
import { defineComponent, h, ref, computed, watch, onMounted, onBeforeUnmount, useId, Fragment } from 'vue';
import {
  PALETTES, ICONS, getAccent, setAccent, onAccent, restoreAccent, recolor, toast,
  focusables, trapFocus, lockScroll
} from './core.js';

export { PALETTES, getAccent, setAccent, onAccent, restoreAccent, recolor, toast };

function cx() { return Array.prototype.filter.call(arguments, Boolean).join(' '); }
var STATUS_ICON = { ok: 'check', danger: 'circle-alert', info: 'info' };
var hasDOM = typeof document !== 'undefined';

/* ---------- Icon: the few Lucide icons Kasane needs itself. Use lucide-vue-next for the rest. ---------- */
export var KIcon = defineComponent({
  name: 'KIcon',
  props: { name: { type: String, required: true } },
  setup: function (props) {
    return function () {
      var d = ICONS[props.name];
      if (!d) return null;
      return h('svg', {
        xmlns: 'http://www.w3.org/2000/svg', width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none',
        stroke: 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round',
        class: 'lucide lucide-' + props.name, 'aria-hidden': 'true'
      }, d.map(function (c) { return h(c[0], c[1]); }));
    };
  }
});
function iconNode(icon) { return typeof icon === 'string' ? h(KIcon, { name: icon }) : icon || null; }
function slot(slots, name) { return slots[name] ? slots[name]() : null; }

/* ---------- Button ---------- */
export var KButton = defineComponent({
  name: 'KButton',
  props: { variant: String, size: String, icon: [String, Object], href: String, type: { type: String, default: 'button' } },
  setup: function (props, ctx) {
    return function () {
      var kids = slot(ctx.slots, 'default');
      var cls = cx('k-btn', props.variant && 'k-btn-' + props.variant, props.size && 'k-btn-' + props.size, props.icon && !kids && 'k-btn-icon');
      return props.href
        ? h('a', { class: cls, href: props.href }, [iconNode(props.icon), kids])
        : h('button', { class: cls, type: props.type }, [iconNode(props.icon), kids]);
    };
  }
});

/* ---------- Fields (v-model) ---------- */
var fieldProps = {
  label: String, hint: String, error: String, id: String,
  start: [String, Object], end: String, modelValue: [String, Number], fieldClass: String
};
function field(tag, extraProps, render) {
  return function (props, ctx) {
    var auto = useId();
    return function () {
      var id = props.id || auto;
      var hintId = props.hint ? id + '-hint' : null, errorId = props.error ? id + '-error' : null;
      var attrs = Object.assign({}, ctx.attrs, {
        id: id, class: cx('k-input', ctx.attrs.class),
        'aria-invalid': props.error ? 'true' : ctx.attrs['aria-invalid'],
        'aria-describedby': [hintId, errorId, ctx.attrs['aria-describedby']].filter(Boolean).join(' ') || undefined,
        value: props.modelValue,
        onInput: function (e) { ctx.emit('update:modelValue', e.target.value); }
      });
      var control = render(attrs, props, ctx);
      if (props.start || props.end) {
        control = h('span', { class: 'k-affix' }, [
          props.start ? h('span', { class: 'k-affix-start', 'aria-hidden': 'true' }, [iconNode(props.start)]) : null,
          control,
          props.end ? h('span', { class: 'k-affix-end' }, props.end) : null]);
      }
      return h('label', { class: cx('k-field', props.fieldClass) }, [
        props.label != null ? props.label : slot(ctx.slots, 'label'), control,
        props.hint ? h('span', { class: 'k-hint', id: hintId }, props.hint) : null,
        props.error ? h('span', { class: 'k-error', id: errorId }, [h(KIcon, { name: 'circle-alert' }), props.error]) : null]);
    };
  };
}
function fieldComponent(name, props, render) {
  return defineComponent({ name: name, inheritAttrs: false, props: Object.assign({}, fieldProps, props), emits: ['update:modelValue'], setup: field(name, props, render) });
}
/* <KTextField v-model="name" label="お名前" hint="…" error="…" start="search" end="円" type="number" /> */
export var KTextField = fieldComponent('KTextField', { type: { type: String, default: 'text' } }, function (a, p) {
  return h('input', Object.assign(a, { type: p.type }));
});
/* type: date (default), time, datetime-local, month, week */
export var KDateField = fieldComponent('KDateField', { type: { type: String, default: 'date' } }, function (a, p) {
  return h('input', Object.assign(a, { type: p.type }));
});
export var KSearchField = fieldComponent('KSearchField', { start: { type: [String, Object], default: 'search' } }, function (a) {
  return h('input', Object.assign(a, { type: 'search' }));
});
export var KTextArea = fieldComponent('KTextArea', { rows: { type: Number, default: 4 } }, function (a, p) {
  return h('textarea', Object.assign(a, { rows: p.rows }));
});
/* options: [{ value, label }] or <option> in the default slot */
export var KSelect = fieldComponent('KSelect', { options: Array }, function (a, p, ctx) {
  a.onInput = null;
  a.onChange = function (e) { ctx.emit('update:modelValue', e.target.value); };
  var opts = p.options ? p.options.map(function (o) { return h('option', { value: o.value, disabled: o.disabled }, o.label); }) : slot(ctx.slots, 'default');
  return h('span', { class: 'k-select' }, [h('select', a, opts)]);
});
/* <KDateRange legend="期間" start-label="開始日" end-label="終了日" v-model:start="from" v-model:end="to" /> */
export var KDateRange = defineComponent({
  name: 'KDateRange',
  props: { legend: String, startLabel: String, endLabel: String, start: String, end: String, type: { type: String, default: 'date' }, separator: { type: String, default: '〜' } },
  emits: ['update:start', 'update:end'],
  setup: function (props, ctx) {
    return function () {
      return h('fieldset', { class: 'k-range' }, [
        h('legend', null, props.legend),
        h(KDateField, { label: props.startLabel, type: props.type, modelValue: props.start, max: props.end || undefined, 'onUpdate:modelValue': function (v) { ctx.emit('update:start', v); } }),
        h('span', { class: 'k-range-sep', 'aria-hidden': 'true' }, props.separator),
        h(KDateField, { label: props.endLabel, type: props.type, modelValue: props.end, min: props.start || undefined, 'onUpdate:modelValue': function (v) { ctx.emit('update:end', v); } })]);
    };
  }
});

/* ---------- Checkbox, radio, switch ---------- */
/* <KCheckbox v-model="on" label="お知らせを受け取る" />  <KRadio v-model="density" value="loose" label="ゆったり" /> */
function optionComponent(name, kind) {
  return defineComponent({
    name: name, inheritAttrs: false,
    props: { label: String, modelValue: [Boolean, String, Number, Array], value: [String, Number] },
    emits: ['update:modelValue'],
    setup: function (props, ctx) {
      return function () {
        var radio = kind === 'radio';
        var checked = radio ? props.modelValue === props.value
          : Array.isArray(props.modelValue) ? props.modelValue.indexOf(props.value) >= 0 : !!props.modelValue;
        var input = h('input', Object.assign({}, ctx.attrs, {
          type: radio ? 'radio' : 'checkbox', class: kind === 'switch' ? undefined : radio ? 'k-radio' : 'k-check',
          value: props.value, checked: checked,
          onChange: function (e) {
            if (radio) ctx.emit('update:modelValue', props.value);
            else if (Array.isArray(props.modelValue)) {
              var list = props.modelValue.filter(function (v) { return v !== props.value; });
              if (e.target.checked) list.push(props.value);
              ctx.emit('update:modelValue', list);
            } else ctx.emit('update:modelValue', e.target.checked);
          }
        }));
        var text = props.label != null ? props.label : slot(ctx.slots, 'default');
        return kind === 'switch'
          ? h('label', { class: 'k-switch' }, [input, h('span', { class: 'k-switch-track', 'aria-hidden': 'true' }), text])
          : h('label', { class: 'k-option' }, [input, ' ', text]);
      };
    }
  });
}
export var KCheckbox = optionComponent('KCheckbox', 'check');
export var KRadio = optionComponent('KRadio', 'radio');
export var KSwitch = optionComponent('KSwitch', 'switch');

/* ---------- Surfaces ---------- */
export var KCard = defineComponent({
  name: 'KCard', props: { title: String, titleAs: { type: String, default: 'h3' }, text: String },
  setup: function (props, ctx) {
    return function () {
      return h('div', { class: 'k-card' }, [
        props.title != null ? h(props.titleAs, { class: 'k-card-title' }, props.title) : null,
        props.text != null ? h('p', { class: 'k-card-text' }, props.text) : null,
        slot(ctx.slots, 'default')]);
    };
  }
});
function simple(name, tag, cls) {
  return defineComponent({ name: name, setup: function (_, ctx) { return function () { return h(tag, { class: cls }, slot(ctx.slots, 'default')); }; } });
}
export var KNest = simple('KNest', 'div', 'k-nest');
export var KList = simple('KList', 'ul', 'k-list');
export var KNotice = defineComponent({
  name: 'KNotice', props: { title: String, titleAs: { type: String, default: 'h3' } },
  setup: function (props, ctx) {
    return function () {
      return h('div', { class: 'k-notice' }, [props.title != null ? h(props.titleAs, { class: 'k-notice-title' }, props.title) : null, h('div', null, slot(ctx.slots, 'default'))]);
    };
  }
});
export var KListItem = defineComponent({
  name: 'KListItem', props: { main: String, sub: String },
  setup: function (props, ctx) {
    return function () {
      return h('li', { class: 'k-list-item' }, [
        h('span', { class: 'k-list-item-main' }, props.main != null ? props.main : slot(ctx.slots, 'main')),
        props.sub != null ? h('span', { class: 'k-list-item-sub' }, props.sub) : null,
        slot(ctx.slots, 'default')]);
    };
  }
});
/* tone: accent | ok | danger | info. ok, danger and info get their icon. */
export var KBadge = defineComponent({
  name: 'KBadge', props: { tone: String },
  setup: function (props, ctx) {
    return function () {
      return h('span', { class: cx('k-badge', props.tone && 'k-badge-' + props.tone) }, [STATUS_ICON[props.tone] ? h(KIcon, { name: STATUS_ICON[props.tone] }) : null, slot(ctx.slots, 'default')]);
    };
  }
});

/* ---------- Tabs and the two-way switch ---------- */
/* <KTabs label="説明" :tabs="[{ id: 'a', label: '概要' }, …]" v-model="tab"><template #a>…</template></KTabs> */
export var KTabs = defineComponent({
  name: 'KTabs', props: { label: String, tabs: { type: Array, required: true }, modelValue: String },
  emits: ['update:modelValue'],
  setup: function (props, ctx) {
    var base = useId();
    var inner = ref(props.tabs[0] && props.tabs[0].id);
    var value = computed(function () { return props.modelValue != null ? props.modelValue : inner.value; });
    var els = {};
    function select(id, focus) {
      inner.value = id; ctx.emit('update:modelValue', id);
      if (focus && els[id]) els[id].focus();
    }
    function onKey(e, i) {
      var n = props.tabs.length, j = null;
      if (e.key === 'ArrowRight') j = (i + 1) % n; else if (e.key === 'ArrowLeft') j = (i - 1 + n) % n;
      else if (e.key === 'Home') j = 0; else if (e.key === 'End') j = n - 1;
      if (j != null) { e.preventDefault(); select(props.tabs[j].id, true); }
    }
    return function () {
      return h(Fragment, null, [
        h('div', { class: 'k-seg', role: 'tablist', 'aria-label': props.label }, props.tabs.map(function (t, i) {
          var on = t.id === value.value;
          return h('button', {
            key: t.id, ref: function (el) { els[t.id] = el; }, type: 'button', role: 'tab',
            id: base + 'tab-' + t.id, 'aria-controls': base + 'panel-' + t.id, 'aria-selected': String(on), tabindex: on ? 0 : -1,
            onClick: function () { select(t.id); }, onKeydown: function (e) { onKey(e, i); }
          }, t.label);
        })),
        props.tabs.map(function (t) {
          return h('div', { key: t.id, class: 'k-nest', role: 'tabpanel', id: base + 'panel-' + t.id, 'aria-labelledby': base + 'tab-' + t.id, hidden: t.id !== value.value }, slot(ctx.slots, t.id));
        })]);
    };
  }
});
export var KSegmented = defineComponent({
  name: 'KSegmented', props: { label: String, options: { type: Array, required: true }, modelValue: [String, Number] },
  emits: ['update:modelValue'],
  setup: function (props, ctx) {
    return function () {
      return h('div', { class: 'k-seg', role: 'group', 'aria-label': props.label }, props.options.map(function (o) {
        return h('button', { key: o.value, type: 'button', 'aria-pressed': String(o.value === props.modelValue), onClick: function () { ctx.emit('update:modelValue', o.value); } }, o.label);
      }));
    };
  }
});

/* ---------- Progress ---------- */
export var KProgress = defineComponent({
  name: 'KProgress', props: { label: String, value: { type: Number, default: 0 }, max: { type: Number, default: 100 } },
  setup: function (props) {
    return function () {
      var pct = Math.round(Math.max(0, Math.min(1, props.value / props.max)) * 100);
      return h(Fragment, null, [
        h('div', { class: 'k-bar-head' }, [h('span', null, props.label), h('span', { class: 'k-num' }, pct + '%')]),
        h('div', { class: 'k-bar', role: 'progressbar', 'aria-label': props.label, 'aria-valuenow': pct, 'aria-valuemin': 0, 'aria-valuemax': 100 }, [h('i', { style: { width: pct + '%' } })])]);
    };
  }
});

/* ---------- Dialog ---------- */
/* <KDialog :open="open" title="このメモを削除しますか?" text="…" @close="open = false"><template #actions>…</template></KDialog> */
export var KDialog = defineComponent({
  name: 'KDialog', props: { open: Boolean, title: String, text: String },
  emits: ['close'],
  setup: function (props, ctx) {
    var titleId = useId();
    var box = ref(null);
    var opener = null;
    function key(e) { if (e.key === 'Escape') ctx.emit('close'); else trapFocus(e, box.value); }
    function start() {
      opener = document.activeElement;
      setTimeout(function () { var f = box.value && focusables(box.value)[0]; if (f) f.focus(); });
      lockScroll(true); document.addEventListener('keydown', key);
    }
    function stop() {
      document.removeEventListener('keydown', key); lockScroll(false);
      if (opener && opener.focus) opener.focus(); opener = null;
    }
    watch(function () { return props.open; }, function (v, old) { if (v && !old) start(); else if (!v && old) stop(); });
    onMounted(function () { if (props.open) start(); });
    onBeforeUnmount(function () { if (props.open) stop(); });
    return function () {
      if (!props.open) return null;
      return h('div', { class: 'k-scrim', onMousedown: function (e) { if (e.target === e.currentTarget) ctx.emit('close'); } }, [
        h('div', { ref: box, class: 'k-dialog', role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': titleId }, [
          h('h3', { class: 'k-dialog-title', id: titleId }, props.title),
          props.text != null ? h('p', { class: 'k-dialog-text' }, props.text) : null,
          slot(ctx.slots, 'default'),
          ctx.slots.actions ? h('div', { class: 'k-dialog-actions' }, ctx.slots.actions()) : null])]);
    };
  }
});

/* ---------- Colour ---------- */
/* const { accent, setAccent } = useAccent(); setAccent('ai') repaints from the top and saves the choice. */
export function useAccent() {
  var accent = ref('hidamari');
  var stop = function () {};
  onMounted(function () { accent.value = getAccent(); stop = onAccent(function (a) { accent.value = a; }); });
  onBeforeUnmount(function () { stop(); });
  return { accent: accent, setAccent: setAccent };
}
export var KPalette = defineComponent({
  name: 'KPalette', props: { legend: String, compact: Boolean, name: { type: String, default: 'accent' }, lang: String },
  setup: function (props) {
    var a = useAccent();
    return function () {
      var en = props.lang === 'en';
      return h('fieldset', { class: cx('k-palette', props.compact && 'k-palette-compact') }, [
        h('legend', null, props.legend || (en ? 'Theme colour' : 'テーマカラー')),
        h('div', { class: 'k-palette-items' }, PALETTES.map(function (c) {
          return h('label', { key: c.id, class: 'k-palette-item' }, [
            h('input', { type: 'radio', name: props.name, value: c.id, checked: a.accent.value === c.id, onChange: function () { setAccent(c.id); } }),
            h('span', { class: 'k-palette-swatch', 'data-swatch': c.id }),
            h('span', { class: 'k-palette-name' }, en ? c.en : c.name)]);
        }))]);
    };
  }
});

/* ---------- Page frame ---------- */
/* <KAppShell brand="かさね帳"><template #sidebar>…</template> … <template #footer>…</template></KAppShell>
   Slots: logo, actions, header-nav, sidebar, default (main), footer. */
export var KAppShell = defineComponent({
  name: 'KAppShell',
  props: { brand: String, brandHref: { type: String, default: '/' }, single: Boolean, plain: Boolean, lang: String, menuLabel: String, closeLabel: String, navLabel: String },
  setup: function (props, ctx) {
    var sideId = useId();
    var open = ref(false), btn = ref(null), side = ref(null);
    var wide = null;
    function key(e) { if (e.key === 'Escape') open.value = false; else trapFocus(e, side.value); }
    function change(e) { if (e.matches) open.value = false; }
    watch(open, function (v) {
      if (v) {
        setTimeout(function () { var f = side.value && (side.value.querySelector('[aria-current="page"]') || focusables(side.value)[0]); if (f) f.focus(); });
        lockScroll(true); document.addEventListener('keydown', key);
        wide = window.matchMedia('(min-width: 900px)'); wide.addEventListener('change', change);
      } else {
        lockScroll(false); document.removeEventListener('keydown', key);
        if (wide) wide.removeEventListener('change', change);
        if (btn.value) btn.value.focus();
      }
    });
    onBeforeUnmount(function () { if (open.value) { lockScroll(false); document.removeEventListener('keydown', key); } });
    return function () {
      var en = props.lang === 'en';
      var navLabel = props.navLabel || (en ? 'Main' : 'メイン');
      var hasSide = !!ctx.slots.sidebar;
      var brand = [slot(ctx.slots, 'logo'), props.brand];
      var sidebar = hasSide ? h('nav', {
        ref: side, class: 'k-sidebar', id: sideId, 'aria-label': navLabel, 'data-open': open.value ? '' : undefined,
        onClick: function (e) { if (e.target.closest && e.target.closest('a[href]')) open.value = false; }
      }, [
        h('div', { class: 'k-sidebar-head' }, [
          h('span', { class: 'k-header-brand' }, brand),
          h('button', { class: 'k-btn k-btn-quiet k-btn-icon', type: 'button', 'aria-label': props.closeLabel || (en ? 'Close menu' : 'メニューを閉じる'), 'data-k-close': '', onClick: function () { open.value = false; } }, [h(KIcon, { name: 'x' })])]),
        ctx.slots.sidebar()]) : null;
      return h('div', { class: 'k-app' }, [
        h('header', { class: 'k-header' }, [
          hasSide ? h('button', {
            ref: btn, class: 'k-menu-btn', type: 'button', 'aria-label': props.menuLabel || (en ? 'Menu' : 'メニュー'),
            'aria-expanded': String(open.value), 'aria-controls': sideId, onClick: function () { open.value = !open.value; }
          }, [h(KIcon, { name: 'menu' })]) : null,
          h('a', { class: 'k-header-brand', href: props.brandHref }, brand),
          ctx.slots['header-nav'] ? h('nav', { class: 'k-header-nav', 'aria-label': navLabel }, ctx.slots['header-nav']()) : null,
          h('span', { class: 'k-header-space' }),
          slot(ctx.slots, 'actions')]),
        hasSide ? h('div', { class: 'k-drawer-scrim', hidden: !open.value, onClick: function () { open.value = false; } }) : null,
        props.single ? sidebar : null,
        h('div', { class: cx('k-layout', props.single && 'k-layout-single') }, [
          props.single ? null : sidebar,
          h('main', { class: cx('k-main', props.plain && 'k-main-plain') }, slot(ctx.slots, 'default'))]),
        slot(ctx.slots, 'footer')]);
    };
  }
});
export var KNavGroup = defineComponent({
  name: 'KNavGroup', props: { title: String },
  setup: function (props, ctx) {
    return function () { return h('div', { class: 'k-nav' }, [props.title != null ? h('p', { class: 'k-nav-title' }, props.title) : null, slot(ctx.slots, 'default')]); };
  }
});
/* as: a router link component (RouterLink, NuxtLink…); current: this page */
export var KNavLink = defineComponent({
  name: 'KNavLink', inheritAttrs: false,
  props: { as: [String, Object], current: Boolean, icon: [String, Object], badge: [String, Number] },
  setup: function (props, ctx) {
    return function () {
      var attrs = Object.assign({}, ctx.attrs, { class: cx('k-nav-link', ctx.attrs.class), 'aria-current': props.current ? 'page' : undefined });
      var kids = function () { return [iconNode(props.icon), slot(ctx.slots, 'default'), props.badge != null ? h(KBadge, { tone: 'accent' }, function () { return String(props.badge); }) : null]; };
      return typeof (props.as || 'a') === 'string' ? h(props.as || 'a', attrs, kids()) : h(props.as, attrs, { default: kids });
    };
  }
});
/* items: [{ label, href }]; the last one is the current page */
export var KBreadcrumb = defineComponent({
  name: 'KBreadcrumb', props: { items: { type: Array, required: true }, label: String, lang: String },
  setup: function (props) {
    return function () {
      var n = props.items.length;
      return h('nav', { 'aria-label': props.label || (props.lang === 'en' ? 'Breadcrumb' : 'パンくずリスト') }, [
        h('ol', { class: 'k-breadcrumb' }, props.items.map(function (it, i) {
          return i === n - 1 ? h('li', { key: i, 'aria-current': 'page' }, it.label) : h('li', { key: i }, [h('a', { href: it.href }, it.label)]);
        }))]);
    };
  }
});
export var KFooter = defineComponent({
  name: 'KFooter', props: { links: Array, linksLabel: String, palette: Boolean, note: String, lang: String },
  setup: function (props, ctx) {
    return function () {
      return h('footer', { class: 'k-footer' }, [h('div', { class: 'k-footer-in' }, [
        props.links ? h('nav', { class: 'k-footer-links', 'aria-label': props.linksLabel || (props.lang === 'en' ? 'About this site' : 'このサイトについて') },
          props.links.map(function (l, i) { return h('a', { key: i, href: l.href }, l.label); })) : null,
        props.palette ? h(KPalette, { compact: true, name: 'accent-footer', lang: props.lang }) : null,
        slot(ctx.slots, 'default'),
        props.note != null ? h('p', { class: 'k-footer-note' }, props.note) : null])]);
    };
  }
});

/* ---------- Table, empty state, loading ---------- */
/* columns: [{ key, label, numeric }]; rows: objects. A slot named after a column key renders its cells ({ row }). */
export var KTable = defineComponent({
  name: 'KTable', props: { caption: String, label: String, columns: { type: Array, required: true }, rows: { type: Array, required: true }, rowKey: String },
  setup: function (props, ctx) {
    return function () {
      return h('div', { class: 'k-table-wrap', role: 'region', 'aria-label': props.label || props.caption, tabindex: 0 }, [
        h('table', { class: 'k-table' }, [
          props.caption != null ? h('caption', null, props.caption) : null,
          h('thead', null, [h('tr', null, props.columns.map(function (c) { return h('th', { key: c.key, scope: 'col', class: c.numeric ? 'k-num' : undefined }, c.label); }))]),
          h('tbody', null, props.rows.map(function (r, i) {
            return h('tr', { key: props.rowKey ? r[props.rowKey] : i }, props.columns.map(function (c) {
              return h('td', { key: c.key, class: c.numeric ? 'k-num' : undefined }, ctx.slots[c.key] ? ctx.slots[c.key]({ row: r }) : String(r[c.key] != null ? r[c.key] : ''));
            }));
          }))])]);
    };
  }
});
export var KEmpty = defineComponent({
  name: 'KEmpty', props: { icon: { type: [String, Object], default: 'info' }, title: String, titleAs: { type: String, default: 'h3' }, text: String },
  setup: function (props, ctx) {
    return function () {
      return h('div', { class: 'k-empty' }, [
        h('div', { class: 'k-empty-icon' }, [slot(ctx.slots, 'icon') || iconNode(props.icon)]),
        h(props.titleAs, { class: 'k-empty-title' }, props.title),
        props.text != null ? h('p', { class: 'k-empty-text' }, props.text) : null,
        ctx.slots.default ? h('div', { class: 'k-empty-actions' }, ctx.slots.default()) : null]);
    };
  }
});
export var KSkeleton = defineComponent({
  name: 'KSkeleton', props: { lines: { type: Number, default: 3 }, title: { type: Boolean, default: true }, card: { type: Boolean, default: true }, label: String, lang: String },
  setup: function (props) {
    return function () {
      var out = [];
      if (props.title) out.push(h('span', { class: 'k-skeleton-title' }));
      for (var i = 0; i < props.lines; i++) out.push(h('span', { class: cx('k-skeleton-line', i === props.lines - 1 && props.lines > 1 && 'k-skeleton-short') }));
      return h('div', { class: props.card ? 'k-card' : undefined, 'aria-busy': 'true' }, [
        h('span', { class: 'k-visually-hidden' }, props.label || (props.lang === 'en' ? 'Loading' : '読み込んでいます')),
        h('div', { class: 'k-skeleton', 'aria-hidden': 'true' }, out)]);
    };
  }
});

/* ---------- Toasts ---------- */
/* const show = useToast(); show('保存しました', { type: 'ok' }). Same as toast() from the core. */
export function useToast() { return toast; }

var ALL = {
  KIcon: KIcon, KButton: KButton, KTextField: KTextField, KDateField: KDateField, KSearchField: KSearchField, KTextArea: KTextArea,
  KSelect: KSelect, KDateRange: KDateRange, KCheckbox: KCheckbox, KRadio: KRadio, KSwitch: KSwitch, KCard: KCard, KNest: KNest,
  KNotice: KNotice, KList: KList, KListItem: KListItem, KBadge: KBadge, KTabs: KTabs, KSegmented: KSegmented, KProgress: KProgress,
  KDialog: KDialog, KPalette: KPalette, KAppShell: KAppShell, KNavGroup: KNavGroup, KNavLink: KNavLink, KBreadcrumb: KBreadcrumb,
  KFooter: KFooter, KTable: KTable, KEmpty: KEmpty, KSkeleton: KSkeleton
};
/* app.use(Kasane) */
export default {
  install: function (app) {
    for (var k in ALL) app.component(k, ALL[k]);
    if (hasDOM) restoreAccent();
  }
};
