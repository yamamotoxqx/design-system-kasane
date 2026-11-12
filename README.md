# Kasane

面を重ねて区切り、アクセントの色を9色から選べる、Webサイトと Webアプリのためのデザインシステムです。

- 枠も影も使わず、面の色の差で区切ります(枠を持つのは入力の部品だけ)。
- アクセントは 山吹・橘・紅梅・藤・藍・空・青磁・萌黄・墨 の9色。全色のライトとダークで、文字のコントラスト 4.5:1 以上を検査しています。
- 書体は LINE Seed JP。タイトルだけ Zen Maru Gothic 900、並べる数字は Inter の等幅数字。

## 使い方

```html
<html lang="ja" data-accent="ai">
<head>
  <link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://kasane.y-n0.de/v1/fonts/line-seed-jp.css">
  <link rel="stylesheet" href="https://kasane.y-n0.de/v1/kasane.min.css">
</head>
<body>
  <button class="k-btn k-btn-primary" type="button">保存する</button>
</body>
</html>
```

- `data-accent`: パレットの名前(省略すると `yamabuki`)
- `data-theme`: `light` か `dark`(省略すると端末の設定。製品では指定せず、切り替えボタンも置かない)

くわしくは、ドキュメントサイト(https://kasane.y-n0.de/)と仕様書(https://kasane.y-n0.de/v1/kasane.md 、英語版 https://kasane.y-n0.de/v1/kasane.en.md)を見てください。製品への組み込み方(既定の色、利用者が色を変える場所)は、ドキュメントサイトの「組み込み方と使用例」にあります。

## AI に使ってもらう

プロジェクトの `CLAUDE.md`(Claude Code)や `AGENTS.md`(Codex)に、次のように書きます。

```markdown
## UI

UIを作る・変更するときは、作業の前に次の仕様書を最後まで読み、そのルールに従うこと。
https://kasane.y-n0.de/v1/kasane.en.md

CSSは次を読み込む。
https://kasane.y-n0.de/v1/kasane.min.css

作業の最後に、仕様書の「作業の最後に確かめること」をすべて確かめること。
```

## 自動チェック(kasane-lint)

CSS は Stylelint、HTML は `kasane-check` で、ルールを機械的に確かめます。

```bash
npm install --save-dev stylelint https://kasane.y-n0.de/v1/kasane-lint-1.2.0.tgz
```

```json
{ "extends": ["kasane-lint/stylelint"] }
```

```bash
npx stylelint "src/**/*.css"
npx kasane-check "src/**/*.html"
```

- CSS: 色の直接指定、影、入力の部品以外の枠線、トークン以外の角丸・余白・文字の大きさ・動きの長さ、`outline: none`、トークン以外の書体
- HTML: 主ボタンの数、状態のアイコン、`style` 属性の色、ラベル、スイッチの作り、Kasane にない `k-` クラス、Lucide に実在しないアイコン名、ダイアログやタブの属性

画像と表示速度も、同じパッケージで確かめられます。

```bash
npm install --save-dev sharp ssim.js lighthouse
npx kasane-image photo.jpg --out public/img        # AVIF / WebP に軽量化。SSIM 0.99 以上になる一番低い画質を自動で選ぶ
npx kasane-lighthouse http://localhost:3000/       # Lighthouse CLI で評価(モバイル・デスクトップ)
```

Lighthouse の最低点は、パフォーマンス 90、アクセシビリティ 100、ベストプラクティス 95、SEO 90 です。

ルールを変えたら `lint/package.json` の `version` を上げます。ファイル名に版が入るので、入れている側の内容が勝手に変わることはありません。

## アイコン

アイコンは [Lucide](https://lucide.dev/icons/)(ISC License)だけを使います。線の太さは 2.5。

## ファイル

| パス | 内容 |
|---|---|
| `v1/kasane.css` / `kasane.min.css` | すべてのトークンと部品 |
| `v1/kasane.md` | 仕様書(AI と人が読む) |
| `v1/kasane.en.md` | 仕様書の英語版(同じ内容。AI が読むときのトークンが少なく済む) |
| `v1/tokens.json` | トークンの値(W3C Design Tokens 形式) |
| `v1/fonts/` | LINE Seed JP(文字の範囲ごとに分割) |
| `index.html` | ドキュメントサイト |
| `llms.txt` | AI に仕様書の場所を知らせる案内 |
| `lint/` | `kasane-lint`(Stylelint のルール、`kasane-check`、`kasane-image`、`kasane-lighthouse`)。`npm run dist` で `v1/kasane-lint-<版>.tgz` として配信 |
| `tools/` | 上のファイルを生成するソース |

## 開発

```bash
npm install
npm run build   # tools/ から v1/ と index.html を生成
npm test        # Stylelint・kasane-check のルール、kasane-image、全パレットのコントラストを検査
npm run dist && npm run lighthouse   # ドキュメントサイトが Lighthouse の最低点を満たすか
```

配信は Cloudflare Pages(ビルドコマンド `npm run dist`、出力ディレクトリ `dist`)で、`main` に push すると更新されます。配信先を変えるときは `KASANE_BASE_URL=https://… npm run build` で作り直します。

## ライセンス

- Kasane 本体(CSS、仕様書、ドキュメント、Stylelint のプラグイン、生成スクリプト): MIT License(`LICENSE`)
- LINE Seed JP: SIL Open Font License 1.1(`v1/fonts/LICENSE-LINE-Seed-JP.txt`)
- Zen Maru Gothic と Inter は Google Fonts から読み込みます(どちらも SIL Open Font License 1.1)。
