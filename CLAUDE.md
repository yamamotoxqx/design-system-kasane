# design-system-kasane

Kasane デザインシステム本体のリポジトリ。

- 配布するファイルは `v2/`(kasane.css、kasane.min.css、kasane.js、kasane.md、kasane.en.md、tokens.json、配信時に kasane-lint の tgz)と、`site/`(ドキュメントサイト。ページごとの HTML、404.html、sitemap.xml、robots.txt、アイコン、共有用の画像)、ルートの `llms.txt`。`npm run dist` で `site/` の中身が配信先のルートになる。
- これらは `tools/` のソースから生成する。**生成されたファイルを直接編集しない。**
  - 色のパレット: `tools/core.cjs`(色の計算)、`tools/gen.cjs`(9色の定義)
  - 部品の CSS とドキュメントの各ページ: `tools/build_site.py`、`tools/pages_extra.py`、`tools/pages_v2.py`(v2 で足した部品と移行のページ)
  - ドキュメントサイトの枠: `tools/site.tpl.html`。ページは1つずつ別のURL(`/color/` など)。リンクは `#color` と書けば、ビルドで `/color/` に変わる
  - アイコンと共有用の画像(`site/favicon.*`、`apple-touch-icon.png`、`icon-*.png`、`og.png`): `npm run icons`(`tools/icons.py`、Python の Playwright と Pillow が必要)。`npm run build` では作り直さない
  - 英語版のドキュメントサイト(`site/en/`): 日本語のページを描いたあと、`tools/i18n.py` が `tools/i18n/en.json` の訳で置き換える。**日本語の文章を変えたり足したりしたら、`en.json` に訳を足す**(足りないとビルドが止まり、`tools/.out/i18n-missing-en.json` に一覧が出る)。ビルドには Python の BeautifulSoup(`bs4`)が必要
  - AI 用の仕様書: `tools/kasane.md.tpl`(日本語)と `tools/kasane.en.md.tpl`(英語版)。**片方を変えたら、もう片方も同じように変える**(`npm test` で見出し・コード・表・クラス・トークンがそろっているかを確かめる)
- 変更したら `npm run build` → `npm test`。CI も同じことをして、生成物が古いと失敗する。
- 配信先は https://kasane.y-n0.de(Cloudflare Workers の静的アセット。設定は `wrangler.jsonc` で、Workers Builds が `npm run dist` → `dist/` を配信する。**配信するフォルダはこのファイルで固定する**。ないと Cloudflare が `site/` を選んで `v1/` が 404 になった)。`main` に push すると配信も更新される。配信先を変えるときは `KASANE_BASE_URL=https://… npm run build`。
- 自動チェック `kasane-lint` は `lint/`(Stylelint のルール `plugin.js`、HTML のチェック `check.js`、画像の軽量化と SSIM `image.js`、Lighthouse の最低点 `lighthouse.js`)。`lint/data/` はビルドで生成。ルールを変えたら `lint/package.json` の `version` を上げる(配信ファイル名に版が入る)。
- `v1/fonts/` は `npm run fonts`(`tools/fonts.py`)で作る。LINE Seed JP を字の使われる頻度ごとに 18 グループ × 3 ウェイトに分けたもの(`@font-face` が多すぎるとスマートフォンで重くなるため)。`npm run build` では作り直さない。
- アイコンは Lucide(`lucide-static`、devDependency)。ドキュメントでは `icon('名前')` で埋め込む。
- ドキュメントサイト自身も Lighthouse の最低点(パフォーマンス 90、アクセシビリティ 100、ベストプラクティス 95、SEO 90)を満たすこと。`npm run dist && npm run lighthouse`(CI でも実行)。ページは `<head>` のスクリプトと CSS で最初から表示する(JavaScript で後から出さない)。
- **`v1/` は凍結**: 出したときのまま残し、生成もしない(`v1/kasane-lint-1.2.0.tgz` も置いたまま)。書体 `v1/fonts/` だけは v1 と v2 で共通で使う(`build_site.py` の `FONT_DIR`)。
- 生成する版は `build_site.py` の `VERSION`(今は `v2`)。見た目が大きく変わる変更(トークン名やクラス名の変更・削除)は次の版(`v3/`)として出し、今の版は凍結して残す。
- `v2/kasane.js` は `tools/kasane.js` から作る(メニュー、ダイアログ、タブ、色の保存と上からの塗り替え)。ドキュメントサイトは読み込まず、`site.tpl.html` に同じ動きを持つ。
- 既定のパレットは `hidamari`(v1 の `yamabuki`)。v2 の CSS は `data-accent="yamabuki"` もひだまりとして表示する。
- UI のルールは `v2/kasane.md` に従う。
