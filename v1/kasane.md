# Kasane v1 — UI を作るためのルールと仕様

Kasane(かさね)は、Webサイトと Webアプリのためのデザインシステムです。
面を重ねて情報を区切り、アクセントの色を9色から選べます。

このファイルは、AI と人が UI を作るときの仕様書です。
**UI を作る・変更する前に、このファイルを最後まで読んでください。**
ここに書かれていないことは、「8. Kasane にない部品を作るとき」の手順で決めます。

ドキュメント: https://kasane.y-n0.de/ ・ ソース: https://github.com/yamamotoxqx/design-system-kasane(MIT License)

---

## 0. 優先順位

判断に迷ったら、上から順に優先します。

1. 利用者(依頼した人)の指示
2. 「2. 必ず守るルール」
3. この仕様書のほかの部分
4. あなた自身の判断

利用者の指示が Kasane のルールとぶつかるときは、指示に従ったうえで、どのルールから外れたかを一言伝えてください。

---

## 1. 読み込み方

```html
<!doctype html>
<html lang="ja" data-accent="yamabuki">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- 保存した色とテーマを、描画の前に適用する(ちらつき防止) -->
  <script>
    try {
      var a = localStorage.getItem("kasane-accent");
      var t = localStorage.getItem("kasane-theme");
      if (a) document.documentElement.dataset.accent = a;
      if (t) document.documentElement.dataset.theme = t;
    } catch (e) {}
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://kasane.y-n0.de/v1/fonts/line-seed-jp.css">
  <link rel="stylesheet" href="https://kasane.y-n0.de/v1/kasane.min.css">
</head>
```

| ファイル | 内容 |
|---|---|
| `https://kasane.y-n0.de/v1/kasane.css` | すべてのトークンと部品(読みやすい版) |
| `https://kasane.y-n0.de/v1/kasane.min.css` | 同じ内容の縮小版。本番ではこちら |
| `https://kasane.y-n0.de/v1/fonts/line-seed-jp.css` | LINE Seed JP(400 / 700 / 800) |
| `https://kasane.y-n0.de/v1/tokens.json` | トークンの値(W3C Design Tokens 形式) |

### 色とテーマの切り替え

| 属性 | 値 | 省略したとき |
|---|---|---|
| `<html data-accent="…">` | `yamabuki` `tachibana` `kobai` `fuji` `ai` `sora` `seiji` `moegi` `sumi` | `yamabuki` |
| `<html data-theme="…">` | `light` `dark` | 端末の設定(`prefers-color-scheme`)に従う |

テーマの切り替えは「ライト」「ダーク」の2択にします(「自動」は置きません)。初期状態は端末の設定に従います。

```js
const root = document.documentElement;
function isDark() {
  const t = root.dataset.theme;
  return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
}
function setTheme(theme) {            // "light" か "dark"
  root.dataset.theme = theme;
  try { localStorage.setItem("kasane-theme", theme); } catch (e) {}
}
function setAccent(id) {              // パレットの名前
  root.dataset.accent = id;
  try { localStorage.setItem("kasane-accent", id); } catch (e) {}
}
```

---

## 2. 必ず守るルール

理由も一緒に書いています。理由に反する書き方は、言い換えても禁止です。

1. **色は必ずトークン(`var(--…)`)で指定する。** `#fff`、`rgb()`、`hsl()`、`oklch()`、色の名前(`white` など)を書かない。
   理由: 色を直接書くと、パレットとテーマを切り替えても色が変わらず、読めなくなる。
2. **カード、リスト、パネル、ボタンに枠線と影を付けない。** `border`、`box-shadow`、`outline` で囲む、区切り線(`hr`、`border-top`)も同じ。区切りは面の色の差で作る。
   理由: Kasane の見た目の土台。線や影で区切ると、別のデザインシステムに見える。
3. **枠を持つのは入力の部品だけ。** 文字の入力欄、選択欄、チェックボックス、ラジオボタン。太さは2px、色は `--line`。
   理由: 「書き込める場所」だと一目で分かるようにするため。
4. **塗りと文字のトークンを使い分ける。** アクセントの塗りは `--accent`、その上の文字は `--on-accent`、アクセント色の文字やリンクは `--accent-ink`。`--accent` を文字の色に使わない。
   理由: 黄色や水色の `--accent` は、文字にすると読めない。
5. **状態は色だけで伝えない。** 成功・エラー・情報には、アイコンと文字を必ず添える。
   理由: 色の見え方は人と画面によって違う。
6. **書体は役割で分ける。** 基本は LINE Seed JP。ページのタイトルと章の見出しだけ `.k-title`(Zen Maru Gothic 900)。縦に並ぶ数字は `.k-num`(Inter の等幅数字)。
7. **角丸・余白・文字の大きさ・動きの長さは、トークンの値から選ぶ。** 新しい値を作らない。
8. **フォーカスのリングを消さない。** `outline: none` を書かない。押せる場所は高さ44px以上(小さいボタンでも36px)。
9. **主ボタン(`.k-btn-primary`)は、1つの画面に1つまで。**
10. **新しい部品は、既存のトークンと部品の組み合わせで作る。**
11. **アイコンは Lucide だけ。SVG は取ってきて貼る。**
    理由: 記憶から描いた形は崩れやすく、ほかのアイコン集と混ぜると線の雰囲気がそろわない。

---

## 3. 色

### トークン

値はパレットとテーマによって変わります。必ずトークンの名前で使ってください。

| トークン | 用途 | 使い方の例 |
|---|---|---|
| `--bg` | ページの背景 | `body` |
| `--surface` | カード、パネル、ダイアログ、入力欄の中 | `.k-card` |
| `--surface-2` | カードの中の面、リストの行、通常のボタン、タブの台 | `.k-list-item` |
| `--surface-3` | `--surface-2` の上でのホバー・押下 | `:hover` |
| `--ink` | 文字 | 本文、見出し |
| `--muted` | 補足の文字 | 説明文、日付、ラベルの補足 |
| `--line` | 入力の部品の枠、スイッチのオフ | `.k-input` |
| `--accent` | アクセントの塗り | 主ボタン、チェック、スイッチのオン、進捗バー |
| `--on-accent` | `--accent` の上の文字・印 | 主ボタンの文字 |
| `--accent-soft` | 薄いアクセントの面 | 選択中のナビ、注目のバッジ |
| `--accent-ink` | アクセント色の文字 | リンク、`--accent-soft` の上の文字 |
| `--focus` | フォーカスのリング | `:focus-visible` |
| `--notice-head` | お知らせの見出し | ライトでは文字色、ダークではアクセント色 |
| `--ok` / `--ok-soft` | 成功の文字 / 面 | 完了、保存しました |
| `--danger` / `--danger-soft` | エラー・削除の文字 / 面 | 削除ボタン、入力エラー |
| `--info` / `--info-soft` | 情報の文字 / 面 | 補足のお知らせ |

組み合わせは決まっています。この表にない組み合わせは使いません。

| 面 | その上に置ける文字 |
|---|---|
| `--bg` `--surface` `--surface-2` | `--ink` `--muted` `--accent-ink` |
| `--surface-3` | `--ink` |
| `--accent` | `--on-accent` |
| `--accent-soft` | `--accent-ink` |
| `--ok-soft` / `--danger-soft` / `--info-soft` | `--ok` / `--danger` / `--info` |

### パレット

| 名前 | `data-accent` | 印象 |
|---|---|---|
| 山吹 | `yamabuki` | 既定。明るい黄色 |
| 橘 | `tachibana` | 橙 |
| 紅梅 | `kobai` | ばら色 |
| 藤 | `fuji` | 紫 |
| 藍 | `ai` | 青 |
| 空 | `sora` | 水色 |
| 青磁 | `seiji` | 青緑 |
| 萌黄 | `moegi` | 黄緑 |
| 墨 | `sumi` | 色を持たない(黒とグレー) |

全パレットのライトとダークで、文字は4.5:1以上、入力の枠とフォーカスのリングは3:1以上のコントラストを満たしています。

**注意:** 明るいパレット(山吹、青磁、萌黄など)では、ライトのときに `--accent` の塗りと面の差が小さくなります。「選択中」「オン」を塗りの色だけで表さず、チェックの印、つまみの位置、文字の太さ、`--accent-soft` の面などを組み合わせてください。

---

## 4. 面の重なり

```
--bg(ページ)
└ --surface(カード、角丸 --r-lg)
   └ --surface-2(中の面、リストの行、角丸 --r-md)
      └ --surface-3(ホバー・押下)
```

- 内側に入るほど、面を一段ずつ変えます。同じ色の面を直接重ねません。
- ダイアログは `--surface`。背景は半透明の黒(`.k-scrim`)。
- ページの背景の上に直接 `--surface-2` を置かず、間に `--surface` を挟みます。

---

## 5. 書体と文字

| 役割 | 書体 | 指定 |
|---|---|---|
| 基本(本文、見出し、ボタン) | LINE Seed JP 400 / 700 / 800 | `--font-body`(`body` に設定済み) |
| ページのタイトル、章の見出し | Zen Maru Gothic 900 | `.k-title` / `--font-title` |
| 縦に並ぶ数字(金額、件数、日付、統計) | Inter + `tabular-nums` | `.k-num` / `--font-num` |

| トークン | 大きさ | 使う場所 | 太さ |
|---|---|---|---|
| `--text-2xl` | 32px | ページのタイトル | `.k-title` |
| `--text-xl` | 24px | 章の見出し | `.k-title` |
| `--text-lg` | 18px | カードの見出し | 800 |
| `--text-base` | 16px | 本文 | 400 |
| `--text-sm` | 14px | ラベル、補足 | 400 / 700 |
| `--text-xs` | 12px | 注釈、日付 | 400 |

- 本文の行間は1.8、タイトルは1.3。長い文章は `max-width: 38em`。
- `.k-title` をカードの中の見出しや本文に使いません。

---

## 6. 角丸・余白・大きさ・動き

| 角丸 | 値 | 使う場所 |
|---|---|---|
| `--r-lg` | 28px | カード、パネル、ダイアログ、お知らせ |
| `--r-md` | 18px | 中の面、リストの行 |
| `--r-sm` | 14px | 入力欄 |
| `--r-full` | 999px | ボタン、バッジ、タブ、スイッチ、進捗バー |

円(アイコンの丸など)は `50%` を使えます。

| 余白 | 値 | 使う場所 |
|---|---|---|
| `--space-1` | 4px | アイコンと文字の間 |
| `--space-2` | 8px | ボタンどうしの間 |
| `--space-3` | 12px | リストの行の内側、カードの中の要素の間 |
| `--space-4` | 16px | 中の面の内側、カードどうしの間 |
| `--space-5` | 24px | カードの内側 |
| `--space-6` | 32px | 大きなまとまりの間 |
| `--space-7` | 56px | 章と章の間 |

- 部品どうしの間隔は、親要素の `gap` で決めます。部品に外側の `margin` を持たせません。
- 押せる場所の高さ: ボタン44px、小さいボタン36px、大きいボタン54px、入力欄46px。
- 画面の左右の余白は16px以上。幅400px前後のスマートフォンで1列に並び替わるようにします。

| 動き | 値 | 使う場所 |
|---|---|---|
| `--motion-fast` | 150ms | ボタンの色と押し込み、スイッチ |
| `--motion-base` | 220ms | ダイアログ、メニューの開閉 |
| `--motion-slow` | 450ms | ページの切り替え、部品が現れるとき(`.k-enter`) |
| `--ease-out` | `cubic-bezier(.2, .7, .3, 1)` | すべての動き |

- 動かすのは透明度と位置だけ。点滅や繰り返す動きは使いません。閉じるときは動かさずに消します。
- `@media (prefers-reduced-motion: reduce)` では動きを止めます。

---

## 7. 部品

クラスは `k-` で始まります。ここにある HTML をそのまま使ってください。

### ボタン

```html
<button class="k-btn k-btn-primary" type="button">保存する</button>   <!-- 主な操作。1画面に1つ -->
<button class="k-btn" type="button">下書きにする</button>              <!-- 通常 -->
<button class="k-btn k-btn-quiet" type="button">キャンセル</button>    <!-- 取り消し。枠も背景もなし -->
<button class="k-btn k-btn-danger" type="button">削除する</button>     <!-- 削除 -->

<button class="k-btn k-btn-sm" type="button">小さい</button>           <!-- 36px -->
<button class="k-btn k-btn-lg k-btn-primary" type="button">大きい</button> <!-- 54px -->
<button class="k-btn" type="button" disabled>使えません</button>

<!-- アイコン付き(アイコンは 18px、文字の前) -->
<button class="k-btn k-btn-primary" type="button"><svg …(plus)></svg>予定を追加</button>
<!-- アイコンだけ(aria-label 必須) -->
<button class="k-btn k-btn-icon" type="button" aria-label="メニューを開く"><svg …(menu)></svg></button>
```

- 並べるときは、取り消しを左、実行を右に置きます。
- ボタンの言葉は、押すと何が起きるかを動詞で書きます(「OK」「はい」は使わない)。
- リンクをボタンの見た目にするときは `<a class="k-btn">` を使えます。

### 入力欄

```html
<label class="k-field">お名前
  <input class="k-input" type="text" placeholder="例:山田 花子">
  <span class="k-hint">本名でなくてもかまいません。</span>
</label>

<!-- エラー: 枠を赤くし、何が問題でどう直すかを書く -->
<label class="k-field">メールアドレス
  <input class="k-input" type="email" aria-invalid="true" aria-describedby="mail-error">
  <span class="k-error" id="mail-error"><svg …(circle-alert)></svg>「@」のあとにドメインを入力してください。</span>
</label>

<!-- 複数行 -->
<label class="k-field">メモ<textarea class="k-input" rows="4"></textarea></label>

<!-- 選択欄 -->
<label class="k-field">場所
  <span class="k-select"><select class="k-input"><option>東京</option><option>大阪</option></select></span>
</label>
```

### チェックボックス、ラジオボタン、スイッチ

```html
<label class="k-option"><input class="k-check" type="checkbox" checked> お知らせを受け取る</label>
<label class="k-option"><input class="k-radio" type="radio" name="density" checked> ゆったり</label>

<!-- スイッチ: すぐ反映される設定に使う。span.k-switch-track は必須 -->
<label class="k-switch">
  <input type="checkbox" checked>
  <span class="k-switch-track" aria-hidden="true"></span>
  自動で保存する
</label>
```

### カード、リスト、中の面、お知らせ

```html
<div class="k-card">
  <h3 class="k-card-title">今週のやること</h3>
  <p class="k-card-text">金曜日は、図書館が17時に閉まります。</p>
  <ul class="k-list">
    <li class="k-list-item"><span class="k-list-item-main">図書館の本を返す</span><span class="k-list-item-sub">11月5日まで</span></li>
    <li class="k-list-item"><span class="k-list-item-main">発表スライドの確認</span><span class="k-list-item-sub">11月8日まで</span></li>
  </ul>
  <div class="k-nest">通知は、毎朝8時にまとめて届きます。</div>
</div>

<div class="k-notice">
  <h3 class="k-notice-title">お知らせ</h3>
  <div>今週のまとめは、日曜の夜に届きます。</div>
</div>
```

- リストの行どうしは6pxの隙間で分けます(`.k-list` に設定済み)。区切り線は使いません。

### バッジ

```html
<span class="k-badge">下書き</span>
<span class="k-badge k-badge-accent">注目</span>
<span class="k-badge k-badge-ok"><svg …(check)></svg>完了</span>
<span class="k-badge k-badge-danger"><svg …(circle-alert)></svg>エラー</span>
<span class="k-badge k-badge-info"><svg …(info)></svg>情報</span>
```

### タブ、2択の切り替え

```html
<!-- タブ(.k-seg は --surface の上に置く) -->
<div class="k-seg" role="tablist" aria-label="説明">
  <button type="button" role="tab" id="tab-a" aria-controls="panel-a" aria-selected="true">概要</button>
  <button type="button" role="tab" id="tab-b" aria-controls="panel-b" aria-selected="false" tabindex="-1">使い方</button>
</div>
<div class="k-nest" role="tabpanel" id="panel-a" aria-labelledby="tab-a">…</div>
<div class="k-nest" role="tabpanel" id="panel-b" aria-labelledby="tab-b" hidden>…</div>

<!-- 2択の切り替え(テーマの切り替えなど) -->
<div class="k-seg" role="group" aria-label="テーマ">
  <button type="button" aria-pressed="true">ライト</button>
  <button type="button" aria-pressed="false">ダーク</button>
</div>
```

タブは、左右の矢印キーで移動できるようにします。選択中の背景は、つまみのように横へ動きます(項目は5つまで)。

### 進捗バー

```html
<div class="k-bar-head"><span>部品</span><span class="k-num">72%</span></div>
<div class="k-bar" role="progressbar" aria-label="部品" aria-valuenow="72" aria-valuemin="0" aria-valuemax="100"><i style="width:72%"></i></div>
```

数字でも進み具合を示します。`style="width:…"` は、この部品で唯一使ってよいインラインのスタイルです。

### ダイアログ、トースト

```html
<div class="k-scrim">
  <div class="k-dialog" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
    <h3 class="k-dialog-title" id="dialog-title">このメモを削除しますか?</h3>
    <p class="k-dialog-text">削除すると元に戻せません。</p>
    <div class="k-dialog-actions">
      <button class="k-btn k-btn-quiet" type="button">キャンセル</button>
      <button class="k-btn k-btn-danger" type="button">削除する</button>
    </div>
  </div>
</div>

<div class="k-toast" role="status">保存しました</div>
```

- ダイアログを開いたら最初のボタンにフォーカスを移し、Esc キーで閉じられるようにします。
- トーストは数秒で消します。大事な内容には使いません。

### 現れる動き

```html
<div class="k-card k-enter">…</div>
```

### アイコン

アイコンは **Lucide**(1.71.0)だけを使います。ほかのアイコン集と混ぜたり、自分で描いたりしません。

- **SVG は記憶から描かず、必ず取ってきて貼る。** 名前を決めたら `https://unpkg.com/lucide-static@1.71.0/icons/<名前>.svg` から取得します(一覧: https://lucide.dev/icons/)。
- 取ってきた SVG の `class="lucide lucide-<名前>"` は消さない。自動チェックで、実在する名前かを確かめます。
- `width` `height` `xmlns` は消してかまいません。`aria-hidden="true"` を付けます。
- 線の太さは `kasane.css` が 2.5 にします。色は `currentColor`(まわりの文字と同じ色)。塗りつぶしのアイコンは使いません。
- 文字と一緒に使います。アイコンだけのボタンには `aria-label` を付けます。

| 用途 | 名前 |
|---|---|
| 成功・チェック | `check` |
| エラー・注意 | `circle-alert` |
| 情報 | `info` |
| 閉じる | `x` |
| 追加 / 編集 / 削除 | `plus` / `pencil` / `trash-2` |
| 検索 / 設定 / 通知 | `search` / `settings` / `bell` |
| 人 / 人たち | `user` / `users` |
| メニュー / 進む | `menu` / `chevron-right` |

大きさは置く場所で決まります(バッジの中 14px、エラーの文 16px、ボタンの中 18px、アイコンだけのボタン 22px)。Kasane の部品の中に置けば自動です。

```html
<svg aria-hidden="true" class="lucide lucide-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
```

---

## 8. Kasane にない部品を作るとき

表、タグ、ナビゲーション、カレンダーなど、ここにない部品が必要になったら、次の順で決めます。

1. **既存の部品で代わりにならないか考える。** たとえば「選べるタグ」は `.k-badge` と `.k-seg` の組み合わせで作れます。
2. **面を決める。** どの面の上に置くかを決め、その一段内側の面を使います(「4. 面の重なり」)。
3. **トークンだけで書く。** 色、角丸、余白、文字の大きさ、動きは、すべて既存のトークンから選びます。
4. **区切りは面と隙間で作る。** 枠線、影、区切り線は使いません。
5. **クラス名は `k-` を付けない。** `k-` は Kasane 本体の部品のためにとっておきます。自分のプロジェクトの名前などを付けてください。

例: 表

```css
.app-table { width: 100%; border-collapse: separate; border-spacing: 0 var(--space-1); }
.app-table th { text-align: left; font-size: var(--text-xs); color: var(--muted); padding: 0 var(--space-3); }
.app-table td { background: var(--surface-2); padding: var(--space-2) var(--space-3); }
.app-table td:first-child { border-radius: var(--r-md) 0 0 var(--r-md); }
.app-table td:last-child  { border-radius: 0 var(--r-md) var(--r-md) 0; }
.app-table .amount { font-family: var(--font-num); font-variant-numeric: tabular-nums; text-align: right; }
```

例: サイドのナビゲーション

```css
.app-nav a { display: flex; align-items: center; min-height: 40px; padding: 0 var(--space-3);
             border-radius: var(--r-sm); color: var(--ink); text-decoration: none; font-weight: 700; }
.app-nav a:hover { background: var(--surface-2); }
.app-nav a[aria-current="page"] { background: var(--accent-soft); color: var(--accent-ink); }
```

---

## 9. 文章

- です・ます体で、1文を短く書きます。1つの文には1つのことだけ。
- 利用者が知っている言葉を使います。内部の用語や英語の略語をそのまま出しません。
- ボタンは「押すと何が起きるか」を動詞で書きます。「予約を確定する」。「OK」「はい」は使いません。
- エラーは「何が起きたか」と「どうすれば直るか」を書きます。利用者を責める言い方をしません。
- 数字は半角。日付は「11月5日(木)」のように曜日を添えます。
- 絵文字を見出しの飾りにしません。

---

## 10. よくある間違い

| してしまいがちなこと | 正しくは |
|---|---|
| `background: #ffffff;` | `background: var(--surface);` |
| `color: var(--accent);`(リンク) | `color: var(--accent-ink);` |
| `.card { border: 1px solid #ddd; }` | 枠を消し、`background: var(--surface);` |
| `.card { box-shadow: 0 2px 8px rgba(0,0,0,.1); }` | 影を消し、面の色で区切る |
| `.list li + li { border-top: 1px solid var(--line); }` | `.k-list`(行を面にして隙間で分ける) |
| `border-radius: 8px;` | `border-radius: var(--r-md);` など |
| `padding: 20px;` | `padding: var(--space-5);` など |
| `font-family: sans-serif;` | 指定しない(`body` に設定済み)か `var(--font-body)` |
| 金額の列がそのまま | `.k-num` を付ける |
| `<span style="color:green">●</span> 完了` | `<span class="k-badge k-badge-ok"><svg …(check)></svg>完了</span>` |
| アイコンの SVG を記憶から描く | Lucide から取ってきて貼る |
| `button:focus { outline: none; }` | 書かない |
| 主ボタンを2つ並べる | 片方を `.k-btn` か `.k-btn-quiet` にする |
| 黄色のボタンに白い文字 | `color: var(--on-accent);` |

---

## 11. 作業の最後に確かめること

UI を作ったら、渡す前に次をすべて確かめてください。

- [ ] 色の値(`#`、`rgb(`、`hsl(`、`oklch(`、色の名前)を書いていない
- [ ] 入力の部品以外に `border`、`box-shadow`、区切り線がない
- [ ] `--accent` を文字の色に使っていない。`--accent` の上の文字は `--on-accent`
- [ ] 角丸、余白、文字の大きさ、動きの長さがトークンの値になっている
- [ ] 状態(成功・エラー・情報)にアイコンと文字がある
- [ ] アイコンはすべて Lucide から取ってきたもの(`class="lucide lucide-…"` が付いている)
- [ ] 主ボタンが1画面に1つまで
- [ ] `.k-title` はページのタイトルと章の見出しだけ。縦に並ぶ数字に `.k-num`
- [ ] `outline: none` がない。押せる場所が高さ44px以上
- [ ] `data-theme="dark"` と `data-accent` を変えても読める
- [ ] 幅375pxで横スクロールが出ない

### 画面を撮って確かめる(できる場合)

スクリーンショットを撮れる道具(Playwright、ブラウザの操作など)が使えるなら、作った画面を実際に撮って見直してください。

撮る組み合わせ:

| 幅 | テーマ | パレット |
|---|---|---|
| 1280px | ライト | 山吹(`yamabuki`) |
| 1280px | ダーク | 山吹(`yamabuki`) |
| 375px | ライト | 藍(`ai`) |
| 375px | ダーク | 墨(`sumi`) |

見るところ:

- [ ] 文字が切れたり、重なったり、はみ出したりしていない
- [ ] 横スクロールが出ていない
- [ ] どの組み合わせでも文字とボタンが読める(明るい黄色の上の白い文字、などがない)
- [ ] カードやリストの区切りが、面の色の差で見分けられる
- [ ] 同じ種類の部品の大きさ、余白、角丸がそろっている
- [ ] 主ボタンが目立ち、取り消しのボタンが控えめになっている
- [ ] 空の状態、長い名前、件数が多いときにも崩れない(データを差し替えて撮る)

崩れを見つけたら直して、もう一度撮ります。撮れない環境のときは、撮れなかったことを作業の報告で伝えてください。

Playwright で撮る例:

```js
// npx playwright install chromium  のあと  node shot.mjs
import { chromium } from "playwright";
const url = "http://localhost:3000/users";   // 作った画面
const cases = [[1280, "light", "yamabuki"], [1280, "dark", "yamabuki"], [375, "light", "ai"], [375, "dark", "sumi"]];
const browser = await chromium.launch();
for (const [width, theme, accent] of cases) {
  const page = await browser.newPage({ viewport: { width, height: 900 } });
  await page.goto(url);
  await page.evaluate(([t, a]) => { document.documentElement.dataset.theme = t; document.documentElement.dataset.accent = a; }, [theme, accent]);
  await page.waitForTimeout(500);
  await page.screenshot({ path: `shot-${width}-${theme}-${accent}.png`, fullPage: true });
}
await browser.close();
```

---

## 12. 自動チェック

`kasane-lint` で、ルールの多くを機械的に確かめられます。CSS は Stylelint、HTML は `kasane-check` が見ます。

```bash
npm install --save-dev stylelint https://kasane.y-n0.de/v1/kasane-lint-1.0.0.tgz
```

```json
// .stylelintrc.json
{ "extends": ["kasane-lint/stylelint"] }
```

```bash
npx stylelint "src/**/*.css"
npx kasane-check "src/**/*.html"
```

**作業の最後に、2つのコマンドを実行し、出たものをすべて直してください**(`kasane-lint` が入っているプロジェクトの場合)。React などで HTML を JavaScript の中に書いている場合は、ビルドして書き出した HTML を `kasane-check` に渡します。

### CSS のルール(Stylelint)

| ルール | 見つけるもの |
|---|---|
| `kasane/no-raw-color` | 色の直接指定(`#…`、`rgb()`、`hsl()`、`oklch()`、色の名前) |
| `kasane/no-shadow` | `box-shadow` |
| `kasane/border-only-on-inputs` | 入力の部品以外への `border` と、区切り線 |
| `kasane/use-tokens` | 角丸、余白、文字の大きさ、動きの長さの直接指定(警告) |
| `kasane/no-outline-none` | `outline: none` / `outline: 0` |
| `kasane/font-family-token` | トークン以外の `font-family` |

### HTML のルール(kasane-check)

| ルール | 見つけるもの |
|---|---|
| `kasane/one-primary` | 1つのファイルに主ボタン(`k-btn-primary`)が2つ以上 |
| `kasane/status-icon` | `k-badge-ok` `k-badge-danger` `k-badge-info` `k-error` にアイコン(`<svg>`)がない |
| `kasane/inline-style` | `style` 属性の色・影・枠線・書体 |
| `kasane/icon-button-label` | 文字のないボタン・リンクに `aria-label` がない |
| `kasane/form-label` | 入力欄にラベルがない |
| `kasane/switch-structure` | `k-switch` の中に `input[type=checkbox]` と `k-switch-track` がない |
| `kasane/unknown-class` | Kasane にない `k-` のクラス |
| `kasane/lucide-icon` | Lucide に実在しないアイコン名、部品の中の Lucide 以外のアイコン |
| `kasane/dialog-label` | `role="dialog"` に名前がない |
| `kasane/tab-aria` | `role="tab"` に `aria-selected` か `aria-controls` がない |

理由があってルールから外れる所には `data-kasane-ignore="ルール名"`(空なら全ルール)を付けると、その要素と中身を検査から外せます。外した理由を作業の報告で伝えてください。
