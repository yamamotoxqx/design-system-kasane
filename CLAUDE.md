# design-system-kasane

Kasane デザインシステム本体のリポジトリ。

- 配布するファイルは `v1/`(kasane.css、kasane.min.css、kasane.md、kasane.en.md、tokens.json、fonts/、配信時に kasane-lint の tgz)と、`site/`(ドキュメントサイト。ページごとの HTML、404.html、sitemap.xml、robots.txt、アイコン、共有用の画像)、ルートの `llms.txt`。`npm run dist` で `site/` の中身が配信先のルートになる。
- これらは `tools/` のソースから生成する。**生成されたファイルを直接編集しない。**
  - 色のパレット: `tools/core.cjs`(色の計算)、`tools/gen.cjs`(9色の定義)
  - 部品の CSS とドキュメントの各ページ: `tools/build_site.py`、`tools/pages_extra.py`
  - ドキュメントサイトの枠: `tools/site.tpl.html`。ページは1つずつ別のURL(`/color/` など)。リンクは `#color` と書けば、ビルドで `/color/` に変わる
  - アイコンと共有用の画像(`site/favicon.*`、`apple-touch-icon.png`、`icon-*.png`、`og.png`): `npm run icons`(`tools/icons.py`、Python の Playwright と Pillow が必要)。`npm run build` では作り直さない
  - AI 用の仕様書: `tools/kasane.md.tpl`(日本語)と `tools/kasane.en.md.tpl`(英語版)。**片方を変えたら、もう片方も同じように変える**(`npm test` で見出し・コード・表・クラス・トークンがそろっているかを確かめる)
- 変更したら `npm run build` → `npm test`。CI も同じことをして、生成物が古いと失敗する。
- 配信先は https://kasane.y-n0.de(Cloudflare Pages、`npm run dist` → `dist/`)。`main` に push すると配信も更新される。配信先を変えるときは `KASANE_BASE_URL=https://… npm run build`。
- 自動チェック `kasane-lint` は `lint/`(Stylelint のルール `plugin.js`、HTML のチェック `check.js`、画像の軽量化と SSIM `image.js`、Lighthouse の最低点 `lighthouse.js`)。`lint/data/` はビルドで生成。ルールを変えたら `lint/package.json` の `version` を上げる(配信ファイル名に版が入る)。
- `v1/fonts/` は `npm run fonts`(`tools/fonts.py`)で作る。LINE Seed JP を字の使われる頻度ごとに 18 グループ × 3 ウェイトに分けたもの(`@font-face` が多すぎるとスマートフォンで重くなるため)。`npm run build` では作り直さない。
- アイコンは Lucide(`lucide-static`、devDependency)。ドキュメントでは `icon('名前')` で埋め込む。
- ドキュメントサイト自身も Lighthouse の最低点(パフォーマンス 90、アクセシビリティ 100、ベストプラクティス 95、SEO 90)を満たすこと。`npm run dist && npm run lighthouse`(CI でも実行)。ページは `<head>` のスクリプトと CSS で最初から表示する(JavaScript で後から出さない)。
- 見た目が大きく変わる変更(トークン名やクラス名の変更・削除)は `v2/` として出し、`v1/` は残す。
- UI のルールは `v1/kasane.md` に従う。
