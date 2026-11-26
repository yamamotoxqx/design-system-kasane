// kasane-react and kasane-vue: every component renders on the server, and the HTML passes kasane-check
// with only the classes kasane.css defines.
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import * as React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { createSSRApp, h } from 'vue';
import { renderToString } from 'vue/server-renderer';
import { checkHtml } from '../lint/check.js';

const here = (p) => fileURLToPath(new URL(p, import.meta.url));
const css = readFileSync(here('../v2/kasane.css'), 'utf8');
const known = new Set([...css.matchAll(/\.(k-[a-z0-9-]+)/g)].map((m) => m[1]));

function verify(name, html, fail, pass, expect) {
  const issues = checkHtml('<!doctype html><html lang="ja"><body>' + html + '</body></html>');
  const unknown = [...html.matchAll(/class="([^"]*)"/g)].flatMap((m) => m[1].split(/\s+/)).filter((c) => c.startsWith('k-') && !known.has(c));
  const missing = (expect || []).filter((c) => !html.includes(c));
  if (issues.length || unknown.length || missing.length) {
    fail(`${name}: ${issues.map((i) => i.rule + ' ' + (i.message || '')).join('; ')} ${unknown.length ? 'unknown ' + unknown.join(',') : ''} ${missing.length ? 'missing ' + missing.join(',') : ''}`);
  } else pass(name);
}

export async function testPackages(fail, pass) {
  const R = await import('../packages/react/index.js');
  const e = React.createElement;
  const rows = [{ d: '11月3日', item: '教科書', yen: '3,280円' }];
  const cols = [{ key: 'd', label: '日付' }, { key: 'item', label: '内容' }, { key: 'yen', label: '金額', numeric: true }];
  const react = {
    Button: [e(R.Button, { variant: 'primary', icon: 'check' }, '保存する'), ['k-btn k-btn-primary', 'lucide-check', 'type="button"']],
    IconButton: [e(R.Button, { variant: 'quiet', icon: 'x', 'aria-label': '閉じる' }), ['k-btn-icon']],
    TextField: [e(R.TextField, { label: 'メール', hint: 'h', error: 'e', type: 'email', defaultValue: '' }), ['aria-invalid="true"', 'aria-describedby=']],
    DateField: [e(R.DateField, { label: '日付', defaultValue: '2026-11-25' }), ['type="date"']],
    DateRange: [e(R.DateRange, { legend: '期間', start: { label: '開始日' }, end: { label: '終了日' } }), ['k-range', 'k-range-sep']],
    NumberUnit: [e(R.TextField, { label: '金額', type: 'number', end: '円' }), ['k-affix-end']],
    SearchField: [e(R.SearchField, { label: '検索' }), ['k-affix-start', 'lucide-search', 'type="search"']],
    TextArea: [e(R.TextArea, { label: 'メモ' }), ['<textarea']],
    Select: [e(R.Select, { label: '場所', options: [{ value: 'tokyo', label: '東京' }] }), ['k-select']],
    Options: [e(React.Fragment, null, e(R.Checkbox, { label: 'a', defaultChecked: true }), e(R.Radio, { label: 'b', name: 'r' }), e(R.Switch, { label: 'c' })), ['k-check', 'k-radio', 'k-switch-track']],
    Card: [e(R.Card, { title: 't', text: 'x' }, e(R.List, null, e(R.ListItem, { main: 'm', sub: 's' })), e(R.Nest, null, 'n')), ['k-card-title', 'k-list-item-sub', 'k-nest']],
    Notice: [e(R.Notice, { title: 'お知らせ' }, 'x'), ['k-notice-title']],
    Badge: [e(React.Fragment, null, e(R.Badge, { tone: 'ok' }, '完了'), e(R.Badge, { tone: 'danger' }, 'エラー')), ['lucide-check', 'lucide-circle-alert']],
    Tabs: [e(R.Card, null, e(R.Tabs, { label: '説明', tabs: [{ id: 'a', label: '概要', content: 'A' }, { id: 'b', label: '使い方', content: 'B' }] })), ['role="tablist"', 'aria-selected="true"', 'hidden']],
    Segmented: [e(R.Card, null, e(R.Segmented, { label: '並び順', options: [{ value: 'n', label: '新' }, { value: 'o', label: '古' }], value: 'n' })), ['aria-pressed="true"']],
    Progress: [e(R.Progress, { label: '部品', value: 72 }), ['aria-valuenow="72"', 'width:72%']],
    Dialog: [e(R.Dialog, { open: true, title: '削除しますか?', text: 'x', actions: e(R.Button, { variant: 'danger' }, '削除する') }), ['k-scrim', 'aria-modal="true"', 'k-dialog-actions']],
    Palette: [e(R.Palette, { compact: true }), ['k-palette-compact', 'data-swatch="hidamari"', 'checked']],
    AppShell: [e(R.AppShell, { brand: 'かさね帳', sidebar: e(R.NavGroup, { title: 'その他' }, e(R.NavLink, { href: '/', current: true, badge: 3 }, 'きょう')), footer: e(R.Footer, { links: [{ href: '/a/', label: 'a' }], palette: true, note: '©' }) },
      e(R.Breadcrumb, { items: [{ href: '/', label: 'ホーム' }, { label: 'きょう' }] })), ['k-menu-btn', 'aria-controls=', 'aria-expanded="false"', 'k-drawer-scrim', 'aria-current="page"', 'k-breadcrumb', 'k-footer-in']],
    Table: [e(R.Card, null, e(R.Table, { caption: '今月の支出', columns: cols, rows })), ['k-table-wrap', 'scope="col"', 'k-num']],
    Empty: [e(R.Empty, { icon: 'info', title: 'まだありません', text: 'x' }, e(R.Button, { variant: 'primary' }, '書く')), ['k-empty-actions']],
    Skeleton: [e(R.Skeleton, { lines: 3 }), ['aria-busy="true"', 'k-skeleton-short', 'k-visually-hidden']],
    Avatar: [e(React.Fragment, null, e(R.Avatar, { name: '青木 ゆい' }), e(R.Avatar, { name: 'a', size: 'lg', src: '/a.webp' })), ['>青<', 'k-avatar-lg', 'alt=""']],
    Account: [e(R.Account, { user: { name: '青木 ゆい', email: 'yui@example.com' }, accounts: [{ name: 'サークル', email: 'c@example.com' }], manageHref: '/account/', onAdd() {}, onLogout() {}, links: [{ href: '/privacy/', label: 'プライバシー' }] }),
      ['k-account-btn', 'aria-controls=', 'aria-expanded="false"', 'role="dialog"', 'k-account-item', 'lucide-log-out', 'k-account-links']],
    SignIn: [e(R.Account, { user: null, loginHref: '/login/' }), ['href="/login/"', 'ログイン']]
  };
  for (const [name, [el, expect]] of Object.entries(react)) verify('react ' + name, renderToStaticMarkup(el), fail, pass, expect);

  const V = await import('../packages/vue/index.js');
  const vue = {
    KButton: [() => h(V.KButton, { variant: 'primary', icon: 'check' }, () => '保存する'), ['k-btn k-btn-primary', 'lucide-check']],
    KTextField: [() => h(V.KTextField, { label: 'メール', hint: 'h', error: 'e', type: 'email', modelValue: 'a' }), ['aria-invalid="true"', 'value="a"']],
    KDateField: [() => h(V.KDateField, { label: '日付', modelValue: '2026-11-25' }), ['type="date"']],
    KDateRange: [() => h(V.KDateRange, { legend: '期間', startLabel: '開始日', endLabel: '終了日', start: '2026-11-01' }), ['k-range', 'min="2026-11-01"']],
    KSearchField: [() => h(V.KSearchField, { label: '検索' }), ['k-affix-start', 'type="search"']],
    KNumber: [() => h(V.KTextField, { label: '金額', type: 'number', end: '円' }), ['k-affix-end']],
    KTextArea: [() => h(V.KTextArea, { label: 'メモ' }), ['<textarea']],
    KSelect: [() => h(V.KSelect, { label: '場所', options: [{ value: 'tokyo', label: '東京' }], modelValue: 'tokyo' }), ['k-select']],
    Options: [() => [h(V.KCheckbox, { label: 'a', modelValue: true }), h(V.KRadio, { label: 'b', value: 'x', modelValue: 'x', name: 'r' }), h(V.KSwitch, { label: 'c' })], ['k-check', 'k-radio', 'k-switch-track', 'checked']],
    KCard: [() => h(V.KCard, { title: 't', text: 'x' }, () => [h(V.KList, null, () => h(V.KListItem, { main: 'm', sub: 's' })), h(V.KNest, null, () => 'n')]), ['k-card-title', 'k-list-item-sub', 'k-nest']],
    KNotice: [() => h(V.KNotice, { title: 'お知らせ' }, () => 'x'), ['k-notice-title']],
    KBadge: [() => h(V.KBadge, { tone: 'info' }, () => '情報'), ['lucide-info']],
    KTabs: [() => h(V.KCard, null, () => h(V.KTabs, { label: '説明', tabs: [{ id: 'a', label: '概要' }, { id: 'b', label: '使い方' }] }, { a: () => 'A', b: () => 'B' })), ['role="tablist"', 'aria-selected="true"', 'hidden']],
    KSegmented: [() => h(V.KCard, null, () => h(V.KSegmented, { label: '並び順', options: [{ value: 'n', label: '新' }], modelValue: 'n' })), ['aria-pressed="true"']],
    KProgress: [() => h(V.KProgress, { label: '部品', value: 72 }), ['aria-valuenow="72"', 'width:72%']],
    KDialog: [() => h(V.KDialog, { open: true, title: '削除しますか?' }, { actions: () => h(V.KButton, { variant: 'danger' }, () => '削除する') }), ['k-scrim', 'aria-modal="true"', 'k-dialog-actions']],
    KPalette: [() => h(V.KPalette, { compact: true }), ['k-palette-compact', 'data-swatch="hidamari"']],
    KAppShell: [() => h(V.KAppShell, { brand: 'かさね帳' }, {
      sidebar: () => h(V.KNavGroup, { title: 'その他' }, () => h(V.KNavLink, { href: '/', current: true, badge: 3 }, () => 'きょう')),
      default: () => h(V.KBreadcrumb, { items: [{ href: '/', label: 'ホーム' }, { label: 'きょう' }] }),
      footer: () => h(V.KFooter, { links: [{ href: '/a/', label: 'a' }], palette: true, note: '©' })
    }), ['k-menu-btn', 'aria-expanded="false"', 'k-drawer-scrim', 'aria-current="page"', 'k-breadcrumb', 'k-footer-in']],
    KTable: [() => h(V.KCard, null, () => h(V.KTable, { caption: '今月の支出', columns: cols, rows })), ['k-table-wrap', 'scope="col"', 'k-num']],
    KEmpty: [() => h(V.KEmpty, { title: 'まだありません', text: 'x' }, () => h(V.KButton, { variant: 'primary' }, () => '書く')), ['k-empty-actions']],
    KSkeleton: [() => h(V.KSkeleton, { lines: 2 }), ['aria-busy="true"', 'k-skeleton-short']],
    KAvatar: [() => h(V.KAvatar, { name: 'yui', size: 'sm' }), ['>Y<', 'k-avatar-sm']],
    KAccount: [() => h(V.KAccount, { user: { name: '青木 ゆい', email: 'yui@example.com' }, accounts: [{ name: 'サークル' }], manageHref: '/account/', links: [{ href: '/terms/', label: '利用規約' }] }),
      ['k-account-btn', 'aria-expanded="false"', 'role="dialog"', 'k-account-item', 'lucide-user-plus']],
    KSignIn: [() => h(V.KAccount, { loginHref: '/login/' }), ['href="/login/"']]
  };
  for (const [name, [render, expect]] of Object.entries(vue)) {
    const html = (await renderToString(createSSRApp({ render }))).replace(/<!--\[-->|<!--\]-->|<!---->/g, '');
    verify('vue ' + name, html, fail, pass, expect);
  }
  // the install function registers every component
  const app = createSSRApp({ render: () => null });
  app.use(V.default);
  Object.keys(V).filter((k) => /^K[A-Z]/.test(k)).forEach((k) => { if (!app.component(k)) fail('vue install misses ' + k); });
}
