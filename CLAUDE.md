# design-system-kasane

Kasane デザインシステム本体のリポジトリ。

- 配布するファイルは `v1/`(kasane.css、kasane.min.css、kasane.md、tokens.json、fonts/)と、ルートの `index.html`(ドキュメントサイト)、`llms.txt`。
- これらは `tools/` のソースから生成する。**生成されたファイルを直接編集しない。**
  - 色のパレット: `tools/core.cjs`(色の計算)、`tools/gen.cjs`(9色の定義)
  - 部品の CSS とドキュメントの各ページ: `tools/build_site.py`、`tools/pages_extra.py`
  - ドキュメントサイトの枠: `tools/site.tpl.html`
  - AI 用の仕様書: `tools/kasane.md.tpl`
- 変更したら `npm run build` → `npm test`。CI も同じことをして、生成物が古いと失敗する。
- 配信先が決まったら `KASANE_BASE_URL=https://… npm run build` で URL を埋め込む。
- 見た目が大きく変わる変更(トークン名やクラス名の変更・削除)は `v2/` として出し、`v1/` は残す。
- UI のルールは `v1/kasane.md` に従う。
