# Kasane {{VERSION}} — UI を作るためのルールと仕様

Kasane(かさね)は、Webサイトと Webアプリのためのデザインシステムです。
面を重ねて情報を区切り、アクセントの色を9色から選べます。

このファイルは、AI と人が UI を作るときの仕様書です。
**UI を作る・変更する前に、このファイルを最後まで読んでください。**
ここに書かれていないことは、「8. Kasane にない部品を作るとき」の手順で決めます。

ドキュメント: {{SITE}}/ ・ ソース: https://github.com/yamamotoxqx/design-system-kasane(MIT License)

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
<html lang="ja" data-accent="hidamari">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- 利用者が選んだ色を、描画の前に適用する(ちらつき防止) -->
  <script>
    try {
      var a = localStorage.getItem("kasane-accent");
      if (a) document.documentElement.dataset.accent = a;
    } catch (e) {}
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{FONTS}}/line-seed-jp.css">
  <link rel="stylesheet" href="{{BASE}}/kasane.min.css">
  <!-- メニュー、ダイアログ、タブ、色の保存(なくても表示はできる) -->
  <script src="{{BASE}}/kasane.js" defer></script>
</head>
```

| ファイル | 内容 |
|---|---|
| `{{BASE}}/kasane.css` | すべてのトークンと部品(読みやすい版) |
| `{{BASE}}/kasane.min.css` | 同じ内容の縮小版。本番ではこちら |
| `{{FONTS}}/line-seed-jp.css` | LINE Seed JP(400 / 700 / 800) |
| `{{BASE}}/tokens.json` | トークンの値(W3C Design Tokens 形式) |
| `{{BASE}}/kasane.js` | メニューの開け閉め、ダイアログ、タブ、色の選択と保存、色を変えたときの動き(なくても表示はできる) |

### kasane.js

`kasane.js` は、部品を動かす小さな JavaScript です(ほかのライブラリは要りません)。HTML に次の印を付けるだけで動きます。

| 印 | 動き |
|---|---|
| `.k-menu-btn[aria-controls]` | 押すとサイドバーをメニューとして開く。Esc キー、後ろの暗い所、`data-k-close` で閉じる |
| `[data-k-dialog="id"]` | 押すと、その `id` の `.k-scrim` を開く。`data-k-close` と Esc キーで閉じる |
| `.k-seg[role="tablist"]` | タブを押す・矢印キーで、パネルを切り替える |
| `.k-palette` | 選んだ色を適用して保存する。色は上から下へ塗り替わる |
| `[data-k-toast="文"]` | 押すとトーストを出す(`data-k-toast-type="ok"` などで種類) |
| `.k-account-btn[aria-controls]` | 押すとアカウントのパネル(`.k-account`)を右から開く |

JavaScript から色を変えるときは `Kasane.setAccent("ai")`、トーストは `Kasane.toast("保存しました", { type: "ok" })` を使います。自分で `data-accent` を書き換えると、塗り替えの動きが付きません。

### 色とテーマ

| 属性 | 値 | 省略したとき |
|---|---|---|
| `<html data-accent="…">` | `hidamari` `tachibana` `kobai` `fuji` `ai` `sora` `seiji` `moegi` `sumi` | `hidamari` |
| `<html data-theme="…">` | `light` `dark` | 端末の設定(`prefers-color-scheme`)に従う |

- `data-accent` には、デザイナーが決めた既定の色を書きます。利用者が色を変えられるようにする方法は「14. 製品に組み込むとき」にあります。
- ライトとダークは端末の設定に任せます。**製品にはライト・ダークの切り替えボタンを置きません。** `data-theme` は、画面を撮って確かめるときなどに使います。

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
| ひだまり | `hidamari` | 既定。明るい黄色 |
| 橘 | `tachibana` | 橙 |
| 紅梅 | `kobai` | ばら色 |
| 藤 | `fuji` | 紫 |
| 藍 | `ai` | 青 |
| 空 | `sora` | 水色 |
| 青磁 | `seiji` | 青緑 |
| 萌黄 | `moegi` | 黄緑 |
| 墨 | `sumi` | 色を持たない(黒とグレー) |

全パレットのライトとダークで、文字は4.5:1以上、入力の枠とフォーカスのリングは3:1以上のコントラストを満たしています。

**注意:** 明るいパレット(ひだまり、青磁、萌黄など)では、ライトのときに `--accent` の塗りと面の差が小さくなります。「選択中」「オン」を塗りの色だけで表さず、チェックの印、つまみの位置、文字の太さ、`--accent-soft` の面などを組み合わせてください。

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
| `--motion-recolor` | 600ms | 色を変えたときの塗り替え(`kasane.js`) |
| `--ease-out` | `cubic-bezier(.2, .7, .3, 1)` | 塗り替え以外のすべての動き |
| `--ease-in-out` | `cubic-bezier(.45, 0, .2, 1)` | 色の塗り替え |

- 動かすのは透明度と位置だけ。点滅や繰り返す動きは使いません。閉じるときは動かさずに消します。
- 色(パレット)を変えたときだけは、画面全体を上から下へ塗り替えます。`kasane.js` の `Kasane.setAccent()` が行うので、自分で動きを書きません。
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

### 日付、時刻、期間、単位、検索

```html
<!-- 日付と時刻: ブラウザーの入力欄をそのまま使う(date / time / datetime-local / month) -->
<label class="k-field">締め切り<input class="k-input" type="date" min="2026-11-25"></label>

<!-- 期間: 開始を選んだら、終了の min をその日にする -->
<fieldset class="k-range">
  <legend>期間</legend>
  <label class="k-field">開始日<input class="k-input" type="date"></label>
  <span class="k-range-sep" aria-hidden="true">〜</span>
  <label class="k-field">終了日<input class="k-input" type="date"></label>
</fieldset>

<!-- 単位(右)と検索のアイコン(左) -->
<label class="k-field">金額
  <span class="k-affix"><input class="k-input" type="number" inputmode="numeric"><span class="k-affix-end">円</span></span>
</label>
<label class="k-field">メモを探す
  <span class="k-affix"><span class="k-affix-start" aria-hidden="true"><svg …(search)></svg></span><input class="k-input" type="search"></span>
</label>
```

- **日付や時刻のために、自作のカレンダーや時刻の選択を作りません。** ブラウザーの入力欄なら、キーボードでも打てて、スマートフォンではいつもの選択画面が開き、読み上げにも対応しています。選べる範囲は `min` と `max` で決めます。
- 期間は幅480px未満で縦に並び、「〜」は隠れます。

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

<!-- 2択の切り替え(並び順など) -->
<div class="k-seg" role="group" aria-label="並び順">
  <button type="button" aria-pressed="true">新しい順</button>
  <button type="button" aria-pressed="false">古い順</button>
</div>
```

タブは、左右の矢印キーで移動できるようにします。選択中の背景は、つまみのように横へ動きます(項目は5つまで)。

### 色の選択

利用者がアクセントの色を選ぶ部品です。置く場所と保存の仕方は「14. 製品に組み込むとき」に従います。

```html
<fieldset class="k-palette">            <!-- 丸だけにするときは k-palette-compact を足す -->
  <legend>テーマカラー</legend>
  <div class="k-palette-items">
    <label class="k-palette-item">
      <input type="radio" name="accent" value="hidamari" checked>
      <span class="k-palette-swatch" data-swatch="hidamari"></span>
      <span class="k-palette-name">ひだまり</span>
    </label>
    <!-- 9色すべてを同じ形で並べる(value と data-swatch はパレットの名前、名前は「3. 色」の表) -->
  </div>
</fieldset>
```

- 中身はラジオボタンです。チェックの印と面の色で選択中を示し、矢印キーでも選べます。
- `.k-palette-compact` では名前が見えなくなりますが、読み上げ用に `.k-palette-name` は残してください。

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

<!-- トーストは .k-toasts の中に並べる(Kasane.toast() が作る) -->
<div class="k-toasts" aria-live="polite">
  <div class="k-toast"><svg …(check)></svg><span class="k-toast-text">保存しました</span></div>
  <div class="k-toast">
    <span class="k-toast-text">メモを削除しました</span>
    <button class="k-toast-action" type="button">元に戻す</button>
    <button class="k-toast-close" type="button" aria-label="閉じる"><svg …(x)></svg></button>
  </div>
</div>
```

- ダイアログを開いたら最初のボタンにフォーカスを移し、Esc キーで閉じられるようにします。
- `kasane.js` を使うなら、`.k-scrim` に `id` と `hidden` を付け、開くボタンに `data-k-dialog="その id"`、閉じるボタンに `data-k-close` を付けます。
- トーストは `Kasane.toast("保存しました", { type: "ok" })` で出します(`type` は `ok` / `info` / `danger`)。操作を付けるときは `{ action: { label: "元に戻す", onClick } }`。
- トーストは自動で消えます。ふつうは5秒、操作が付くときは10秒。ポインターを重ねている間、フォーカスがある間、ページが裏にある間は止まります。失敗(`danger`)は自動で消さず、閉じるボタンを付けます。
- 並ぶのは3つまで(古いものから閉じる)。出るときだけ下から浮かび、閉じるときは動かしません。
- 同じ内容で重要性の低いトースト(`danger` でも操作付きでもないもの)は、新しく並べずに画面に出ているものへまとめます。「×2」のように回数を添え、時間を数え直します(`Kasane.toast()` が行う。`{ merge: false }` で止められる)。
- 大事な内容には使いません。入力の間違いはトーストではなく、入力欄の下(`.k-error`)に書きます。

### 画面の骨組み(ヘッダー、メニュー、サイドバー)

**ナビゲーションのある画面は、必ずこの形で作ります。** ヘッダー、メニュー、サイドバーを独自に作りません。

```html
<div class="k-app">
  <header class="k-header">
    <button class="k-menu-btn" type="button" aria-label="メニュー" aria-expanded="false" aria-controls="sidebar">
      <svg aria-hidden="true" class="lucide lucide-menu" …></svg>
    </button>
    <a class="k-header-brand" href="/">かさね帳</a>
    <span class="k-header-space"></span>
    <button class="k-btn k-btn-quiet k-btn-icon" type="button" aria-label="お知らせ"><svg aria-hidden="true" class="lucide lucide-bell" …></svg></button>
  </header>
  <div class="k-drawer-scrim" hidden></div>
  <div class="k-layout">
    <nav class="k-sidebar" id="sidebar" aria-label="メイン">
      <div class="k-sidebar-head">
        <span class="k-header-brand">かさね帳</span>
        <button class="k-btn k-btn-quiet k-btn-icon" type="button" aria-label="メニューを閉じる" data-k-close><svg aria-hidden="true" class="lucide lucide-x" …></svg></button>
      </div>
      <div class="k-nav">
        <a class="k-nav-link" href="/" aria-current="page"><svg aria-hidden="true" class="lucide lucide-house" …></svg>きょう</a>
        <a class="k-nav-link" href="/tasks/"><svg aria-hidden="true" class="lucide lucide-list-checks" …></svg>やること<span class="k-badge k-badge-accent">3</span></a>
      </div>
      <div class="k-nav">
        <p class="k-nav-title">その他</p>
        <a class="k-nav-link" href="/settings/"><svg aria-hidden="true" class="lucide lucide-settings" …></svg>設定</a>
      </div>
    </nav>
    <main class="k-main">
      <h1 class="k-title">きょう</h1>
      …
    </main>
  </div>
  <footer class="k-footer">…</footer>
</div>
```

- 幅900px以上: サイドバーは左に常に見えます。メニューのボタン(`.k-menu-btn`)は隠れます。
- 幅900px未満: サイドバーは左から出てくるメニュー(ドロワー)になり、ヘッダーの左端にメニューのボタンが出ます。
- メニューのボタンは左上に1つだけ。アイコンは Lucide の `menu`。`aria-controls` でサイドバーの `id` を指し、`aria-expanded` で開いているかを示します。
- メニューは開くときだけ220msで滑り込み、閉じるときはすぐに消します。Esc キー、後ろの暗い所(`.k-drawer-scrim`)、`data-k-close` のボタンで閉じます。開いたら選択中のリンクにフォーカスを移し、閉じたらメニューのボタンに戻します(`kasane.js` が行います)。
- **ドロップダウンのメニュー(ボタンの下に浮かぶメニュー)は作りません。** メニューはドロワー、確認はダイアログにします。
- 保存や送信など、その画面の主な操作をメニューの中にだけ置きません。
- 本文の面 `.k-main` は `--surface` です。中にはリスト、`.k-nest`、表など一段内側の部品を置きます。カードを並べるページでは `.k-main k-main-plain` にして、`.k-card` を背景の上に置きます。
- ページが5つ以下の小さなサイトでは、サイドバーの代わりにヘッダーにリンクを並べ(`<nav class="k-header-nav">` の中に `<a>`)、`.k-layout k-layout-single` で本文を1列にします。同じリンクを `.k-layout` の外の `.k-sidebar` にも書きます。`.k-layout` の外のサイドバーは、メニューを開いたときだけ表示されます。

### パンくずリスト

```html
<nav aria-label="パンくずリスト">
  <ol class="k-breadcrumb">
    <li><a href="/">ホーム</a></li>
    <li><a href="/settings/">設定</a></li>
    <li aria-current="page">表示</li>
  </ol>
</nav>
```

階層が3段以上あるときに、本文の一番上に置きます。最後の項目は今いるページで、リンクにしません。

### フッター

```html
<footer class="k-footer">
  <div class="k-footer-in">
    <nav class="k-footer-links" aria-label="このサイトについて">
      <a href="/about/">かさね帳について</a>
      <a href="/privacy/">プライバシー</a>
    </nav>
    <fieldset class="k-palette k-palette-compact">…</fieldset>
    <p class="k-footer-note">© 2026 かさね帳</p>
  </div>
</footer>
```

設定ページのない製品では、色の選択(`.k-palette-compact`)をフッターに置きます。

### アカウント

ログインのある製品は、ヘッダーの右端にアバターのボタンを1つ置き、押すと右からアカウントのパネルを出します。

```html
<!-- ヘッダーの右端 -->
<button class="k-account-btn" type="button" aria-label="アカウント: 青木 ゆい" aria-expanded="false" aria-controls="account">
  <span class="k-avatar" aria-hidden="true">青</span>
</button>

<div class="k-drawer-scrim" hidden></div>
<div class="k-account" id="account" role="dialog" aria-modal="true" aria-label="アカウント">
  <div class="k-account-head">
    <span class="k-avatar k-avatar-lg" aria-hidden="true">青</span>
    <div>
      <p class="k-account-name">青木 ゆい</p>
      <p class="k-account-email">yui.aoki@example.com</p>
    </div>
    <button class="k-btn k-btn-quiet k-btn-icon" type="button" aria-label="閉じる" data-k-close><svg …(x)></svg></button>
  </div>
  <a class="k-btn" href="/account/">アカウントを管理</a>
  <p class="k-account-title">ほかのアカウント</p>
  <ul class="k-account-list">
    <li><button class="k-account-item" type="button"><span class="k-avatar" aria-hidden="true">サ</span><span><span class="k-account-name">サークルの共用</span><span class="k-account-email">circle@example.com</span></span></button></li>
  </ul>
  <div class="k-account-actions">
    <button class="k-btn k-btn-quiet" type="button"><svg …(user-plus)></svg>アカウントを追加</button>
    <button class="k-btn k-btn-quiet" type="button"><svg …(log-out)></svg>ログアウト</button>
  </div>
  <nav class="k-account-links" aria-label="規約"><a href="/privacy/">プライバシー</a><a href="/terms/">利用規約</a></nav>
</div>

<!-- ログインしていないとき: アバターの代わりに -->
<a class="k-btn" href="/login/">ログイン</a>
```

- **アバターの下に浮かぶメニューは作りません。** パネルは画面の幅にかかわらず右から出ます(開くときだけ220msで滑り込み、閉じるときはすぐ消える)。Esc キー、後ろの暗い所、`data-k-close` で閉じます(`kasane.js` が行う)。
- 中身の順番は固定: 今のアカウント(大きいアバター、名前、メールアドレス)→「アカウントを管理」→ ほかのアカウント(2つ以上のときだけ。押すと切り替えて読み込み直す)→「アカウントを追加」「ログアウト」→ 規約のリンク。
- アバターは写真か、名前の最初の1文字。ボタンの `aria-label` に名前を書き、アバターは読み上げない(`alt=""` か `aria-hidden`)。
- メールアドレスは省略せず、長ければ折り返します。名前に敬称を付けません。
- ログアウトは赤くせず、確認もしません(書きかけの内容が消えるときだけ確認する)。切り替えやログアウトをトーストで知らせません。
- ログインしていないときの「ログイン」はふつうのボタン(主ボタンにしない)。

### 表

```html
<div class="k-table-wrap" role="region" aria-label="今月の支出" tabindex="0">
  <table class="k-table">
    <caption>今月の支出</caption>
    <thead>
      <tr><th scope="col">日付</th><th scope="col">内容</th><th scope="col" class="k-num">金額</th></tr>
    </thead>
    <tbody>
      <tr><td>11月3日(月)</td><td>教科書</td><td class="k-num">3,280円</td></tr>
    </tbody>
  </table>
</div>
```

- 行は `--surface-2` の面で、行どうしは隙間で分けます。罫線と縞模様は使いません。`--surface` の上(カードや `.k-main` の中)に置きます。
- 金額や件数の列は `.k-num`(右にそろう)。見出しには `scope` を付けます。
- 狭い画面では `.k-table-wrap` の中だけが横にスクロールします。列が2つか3つなら、表ではなく `.k-list` にします。

### 空の状態

```html
<div class="k-empty">
  <div class="k-empty-icon"><svg aria-hidden="true" class="lucide lucide-inbox" …></svg></div>
  <h3 class="k-empty-title">まだメモがありません</h3>
  <p class="k-empty-text">授業や実習で気づいたことを書きとめておくと、あとで見返せます。</p>
  <div class="k-empty-actions">
    <button class="k-btn k-btn-primary" type="button">メモを書く</button>
  </div>
</div>
```

リストや検索結果が空のときに、何もない画面のままにしません。なぜ空なのかと、次にできることを書きます。ボタンは1つまで。

### 読み込み中

```html
<div class="k-card" aria-busy="true">
  <span class="k-visually-hidden">読み込んでいます</span>
  <div class="k-skeleton" aria-hidden="true">
    <span class="k-skeleton-title"></span>
    <span class="k-skeleton-line"></span>
    <span class="k-skeleton-line k-skeleton-short"></span>
  </div>
</div>
```

- 読み込みに1秒以上かかるときだけ出します。形と大きさは中身に合わせます(`.k-skeleton-block` は画像、`.k-skeleton-circle` はアイコン)。
- 光が流れる動きやくるくる回るアイコンは使いません。終わったら、まとめて中身に入れ替えます。

### 現れる動き

```html
<div class="k-card k-enter">…</div>
```

### アイコン

アイコンは **Lucide**({{LUCIDE_VER}})だけを使います。ほかのアイコン集と混ぜたり、自分で描いたりしません。

- **SVG は記憶から描かず、必ず取ってきて貼る。** 名前を決めたら `{{LUCIDE_URL}}/<名前>.svg` から取得します(一覧: https://lucide.dev/icons/)。
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

タグ、カレンダー、グラフなど、ここにない部品が必要になったら、次の順で決めます。

1. **既存の部品で代わりにならないか考える。** たとえば「選べるタグ」は `.k-badge` と `.k-seg` の組み合わせで作れます。
2. **面を決める。** どの面の上に置くかを決め、その一段内側の面を使います(「4. 面の重なり」)。
3. **トークンだけで書く。** 色、角丸、余白、文字の大きさ、動きは、すべて既存のトークンから選びます。
4. **区切りは面と隙間で作る。** 枠線、影、区切り線は使いません。
5. **クラス名は `k-` を付けない。** `k-` は Kasane 本体の部品のためにとっておきます。自分のプロジェクトの名前などを付けてください。

例: 選べるタグ

```css
.app-tag { display: inline-flex; align-items: center; min-height: 36px; padding: 0 var(--space-4);
           border: 0; border-radius: var(--r-full); background: var(--surface-2); color: var(--ink);
           font: inherit; font-size: var(--text-sm); font-weight: 700; cursor: pointer; }
.app-tag:hover { background: var(--surface-3); }
.app-tag[aria-pressed="true"] { background: var(--accent-soft); color: var(--accent-ink); }
```

例: カレンダーの日付

```css
.app-day { display: grid; place-items: center; width: 44px; height: 44px; border-radius: 50%;
           font-family: var(--font-num); font-variant-numeric: tabular-nums; font-weight: 700; }
.app-day:hover { background: var(--surface-2); }
.app-day[aria-current="date"] { background: var(--accent); color: var(--on-accent); }
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
| メニューを自作する、ボタンの下にドロップダウンで出す | `.k-menu-btn` と `.k-sidebar`(左から出るメニュー) |
| `<table>` に罫線や縞模様 | `.k-table` |
| 読み込み中に回るアイコン、光るスケルトン | `.k-skeleton`(動かない) |
| `root.dataset.accent = "ai"` で色を変える | `Kasane.setAccent("ai")`(塗り替えの動きが付く) |
| 日付を選ぶカレンダーを自作する | `<input class="k-input" type="date">` |
| アバターの下にアカウントのメニューを浮かせる | `.k-account-btn` と `.k-account`(右から出るパネル) |
| トーストを `setTimeout` で自作する | `Kasane.toast()`(止める・閉じる・読み上げまで入っている) |
| React や Vue で `.k-` の HTML を手で組む | `kasane-react` / `kasane-vue` の部品 |

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
- [ ] ライト・ダークの切り替えボタンを置いていない。最初に色を選ばせる画面を出していない
- [ ] 幅375pxで横スクロールが出ない
- [ ] ナビゲーションは `.k-header` `.k-sidebar` `.k-nav` で作り、幅900px未満でメニューのボタンから開いて Esc キーで閉じる
- [ ] 画像は `kasane-image` で軽くした(AVIF / WebP、SSIM 0.99 以上、`width` `height` `alt` あり)
- [ ] `kasane-lighthouse` で最低点を満たした(パフォーマンス 90、アクセシビリティ 100、ベストプラクティス 95、SEO 90)

### 画面を撮って確かめる(できる場合)

スクリーンショットを撮れる道具(Playwright、ブラウザの操作など)が使えるなら、作った画面を実際に撮って見直してください。

撮る組み合わせ:

| 幅 | テーマ | パレット |
|---|---|---|
| 1280px | ライト | ひだまり(`hidamari`) |
| 1280px | ダーク | ひだまり(`hidamari`) |
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
const cases = [[1280, "light", "hidamari"], [1280, "dark", "hidamari"], [375, "light", "ai"], [375, "dark", "sumi"]];
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
npm install --save-dev stylelint {{LINT_URL}}
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
| `kasane/menu-button` | `k-menu-btn` か `k-account-btn` に `aria-controls` か `aria-expanded` がない |
| `kasane/img-alt` | `<img>` に `alt` がない(飾りの画像は `alt=""`) |
| `kasane/img-size` | `<img>` に `width` と `height` がない |
| `kasane/img-format` | JPEG・PNG・GIF をそのまま使っている(`<picture>` で AVIF / WebP を出していない) |

理由があってルールから外れる所には `data-kasane-ignore="ルール名"`(空なら全ルール)を付けると、その要素と中身を検査から外せます。外した理由を作業の報告で伝えてください。

---

## 13. 画像とパフォーマンス

表示が速く、読み込み中に画面がずれない状態を目指します。

### Lighthouse の最低点

作った画面は Lighthouse CLI で評価し、**モバイルとデスクトップの両方で**次の点数を下回らないようにします。

| 項目 | 最低点 |
|---|---|
| パフォーマンス | 90 |
| アクセシビリティ | 100 |
| ベストプラクティス | 95 |
| SEO | 90 |

```bash
npm install --save-dev lighthouse
npx kasane-lighthouse http://localhost:3000/ http://localhost:3000/users   # --runs 3 で揺れを抑える
```

届かない項目があると、点数を下げている原因が表示されます。最低点に届くまで直してください。Chrome が見つからないときは `CHROME_PATH` を指定します。目標の指標は LCP 2.5 秒以内、INP 200 ミリ秒以内、CLS 0.1 以下です。

### 画像

画像はそのまま置かず、**必ず `kasane-image` で軽くしてから**使います。

| 決まり | 内容 |
|---|---|
| 形式 | 写真・イラストは AVIF と WebP。アイコン・ロゴは SVG。動く画像は GIF ではなく動画 |
| 大きさ | 表示する大きさの2倍まで。幅の種類は3つまで |
| 画質 | 元の画像との SSIM 0.99 以上(`kasane-image` が自動で確かめる)。最後は目でも確かめる |
| 容量 | 1枚 100 KB を超えたら、幅を小さくできないか見直す |
| 属性 | `width` `height` `alt` を必ず書く。画面の外の画像は `loading="lazy"`、最初に見える大きな画像は `fetchpriority="high"` |

```bash
npm install --save-dev sharp ssim.js
npx kasane-image photo.jpg --out public/img --widths 640,1280     # 書き出しと SSIM の確認、<picture> を表示
npx kasane-image --compare original.png public/img/photo.avif     # SSIM だけを確かめる
```

`kasane-image` は幅ごと・形式ごとに、SSIM が 0.99 以上になる一番低い画質を選び、そのまま貼れる `<picture>` を表示します。

### そのほか

- フォントの CSS は表示を止めないように読み込む: `<link rel="stylesheet" href="{{FONTS}}/line-seed-jp.css" media="print" onload="this.media='all'">`(`<noscript>` に通常の `<link>` も置く)
- 読み込み中・0件・失敗のときも同じ大きさの場所を使い、あとから上に部品を差し込まない
- 本番では `kasane.min.css` を使う。JavaScript には `defer` を付ける

---

## 14. 製品に組み込むとき

Kasane は、色をデザイナーが決めることも、利用者が変えることもできます。組み込むときは、次の2つを最初に決めます。依頼に書かれていなければ、既定の色はひだまり、利用者は色を変えられない、として作り、そのことを報告で伝えます。

| 決めること | やり方 |
|---|---|
| 既定の色 | `<html data-accent="…">` に書く |
| 利用者が色を変えられるか | 変えられるなら、設定ページかページ下部に色の選択(`.k-palette`)を置く |

### 既定の色の選び方

| こんなとき | パレット |
|---|---|
| ブランドの色がある | その色相に一番近いパレット |
| 信頼感、落ち着き(予約、金融、医療など) | `ai` `sora` |
| 明るさ、親しみやすさ(学習、暮らしなど) | `hidamari` `tachibana` `moegi` |
| やさしさ、交流(コミュニティなど) | `kobai` `fuji` |
| 情報に集中してほしい(業務の画面、管理画面) | `sumi` |

### 色の選択を置く場所

| 製品 | 置く場所 | 部品 |
|---|---|---|
| 設定ページがある | 設定ページの「表示」などのまとまりの中 | `.k-palette`(名前も見せる) |
| 設定ページがない | ページ下部(フッター) | `.k-palette.k-palette-compact` |

- 開いたらすぐ既定の色で表示します。最初に色を選ばせる画面やダイアログを出しません。
- 色の選択は1か所だけに置きます。ヘッダーやすべての画面に置きません。
- ライト・ダークの切り替えは置きません(端末の設定に従う)。

### 選んだ色を保存する

`<head>` には「1. 読み込み方」のスクリプトを置きます。`kasane.js` を読み込んでいれば、`.k-palette` を置くだけで、選んだ色の適用、保存、塗り替えの動きまで動きます。`kasane.js` を使わないときは、次の JavaScript をつなぎます。

```js
const root = document.documentElement;
const current = root.dataset.accent || "hidamari";
document.querySelectorAll('.k-palette input[name="accent"]').forEach((radio) => {
  radio.checked = radio.value === current;
  radio.addEventListener("change", () => {
    root.dataset.accent = radio.value;
    try { localStorage.setItem("kasane-accent", radio.value); } catch (e) {}
  });
});
```

ログインのある製品では、選んだ色を利用者の設定としてサーバーにも保存し、HTML を返すときに `data-accent` へ書き込むと、別の端末でも同じ色になります。

色を変えたことや保存したことは、トースト(「色を変更しました」「保存しました」など)で知らせません。画面が塗り替わるだけで伝わります。

---

## 15. 多言語に対応するとき

1つの製品を複数の言語で出すときは、次のとおりにします。依頼に言語が書かれていなければ、1つの言語だけで作ります。

| 決めること | 決まり |
|---|---|
| `<html lang>` | ページの言語を書く。別の言語の言葉には、その要素に `lang` を付ける |
| URL | 既定の言語はそのまま(`/pricing/`)、ほかの言語は先頭に言語の記号(`/en/pricing/`)。各ページに `hreflang` でほかの言語の同じページを示す |
| 言語の切り替え | ヘッダーの右側かページ下部の1か所。同じページの別の言語版へ移る。ブラウザの言語設定で勝手に移さない |
| 言語の名前 | その言語で書く(「English」「日本語」)。`lang` を付ける。国旗は使わない |
| 文章 | コードに直接書かず翻訳ファイルから読む。文をつなぎ合わせない。画像に文字を入れない |
| 幅 | ボタンやラベルに固定の幅を付けない。一番長い言語でも画面を撮って確かめる |
| 書体 | LINE Seed JP は日本語とラテン文字用。ほかの文字は `:root:lang(ko) { --font-body: … }` のように、その言語のときだけ足す |
| 数字と日付 | `Intl.DateTimeFormat` / `Intl.NumberFormat` にページの言語を渡す。縦に並べるときは `.k-num` |
| 右から左の言語 | まだ確かめていない。必要なら左右反転で崩れないかを確かめ、報告する |

```html
<html lang="ja">
<head>
  <link rel="canonical" href="https://example.com/pricing/">
  <link rel="alternate" hreflang="ja" href="https://example.com/pricing/">
  <link rel="alternate" hreflang="en" href="https://example.com/en/pricing/">
  <link rel="alternate" hreflang="x-default" href="https://example.com/pricing/">
</head>
<!-- 言語の切り替え(アイコンは Lucide の languages を取得して貼る) -->
<a class="k-btn k-btn-quiet" href="/en/pricing/" hreflang="en" lang="en"><svg …(languages)></svg>English</a>
```

---

## 16. React と Vue

React と Vue では、`.k-` の HTML を手で組まず、部品のパッケージを使います。出てくる HTML はこの仕様書と同じです。

```bash
npm install {{BASE}}/kasane-react-{{PKG_VERSION}}.tgz   # React 18 以上
npm install {{BASE}}/kasane-vue-{{PKG_VERSION}}.tgz     # Vue 3.5 以上
```

```jsx
import { AppShell, NavGroup, NavLink, DateField, Button, toast } from "kasane-react";
import "kasane-react/kasane.css";

<AppShell brand="かさね帳" sidebar={<NavGroup><NavLink href="/" current>きょう</NavLink></NavGroup>}>
  <DateField label="締め切り" value={due} onChange={(e) => setDue(e.target.value)} />
  <Button variant="primary" onClick={() => toast("保存しました", { type: "ok" })}>保存する</Button>
</AppShell>
```

```vue
<KAppShell brand="かさね帳">
  <template #sidebar><KNavGroup><KNavLink href="/" current>きょう</KNavLink></KNavGroup></template>
  <KDateField v-model="due" label="締め切り" />
  <KButton variant="primary" @click="toast('保存しました', { type: 'ok' })">保存する</KButton>
</KAppShell>
```

| React | Vue | HTML |
|---|---|---|
| `Button` | `KButton` | `.k-btn` |
| `TextField` `DateField` `SearchField` `TextArea` `Select` | `KTextField` `KDateField` `KSearchField` `KTextArea` `KSelect` | `.k-field` `.k-input` |
| `DateRange` | `KDateRange` | `.k-range` |
| `Checkbox` `Radio` `Switch` | `KCheckbox` `KRadio` `KSwitch` | `.k-check` `.k-radio` `.k-switch` |
| `Card` `Nest` `Notice` `List` `ListItem` | `KCard` `KNest` `KNotice` `KList` `KListItem` | `.k-card` `.k-nest` `.k-notice` `.k-list` |
| `Badge` | `KBadge` | `.k-badge` |
| `Tabs` `Segmented` | `KTabs` `KSegmented` | `.k-seg` |
| `Progress` | `KProgress` | `.k-bar` |
| `Dialog` | `KDialog` | `.k-dialog` |
| `toast()` | `toast()` | `.k-toast` |
| `Palette` `useAccent()` | `KPalette` `useAccent()` | `.k-palette` |
| `AppShell` `NavGroup` `NavLink` `Breadcrumb` `Footer` | `KAppShell` `KNavGroup` `KNavLink` `KBreadcrumb` `KFooter` | `.k-app` `.k-sidebar` `.k-nav` `.k-breadcrumb` `.k-footer` |
| `Table` | `KTable` | `.k-table` |
| `Empty` `Skeleton` | `KEmpty` `KSkeleton` | `.k-empty` `.k-skeleton` |
| `Avatar` `Account` | `KAvatar` `KAccount` | `.k-avatar` `.k-account` |

- 入力欄に `label` `hint` `error` を渡すと、`aria-describedby` と `aria-invalid` が付きます。React は `value` と `onChange`、Vue は `v-model` で使います。
- アイコンは `lucide-react` / `lucide-vue-next` の部品を `icon` に渡します。`check` `circle-alert` `info` `x` `menu` `search` `user-plus` `log-out` は名前でも書けます。
- ルーターのリンクは、`NavLink` / `KNavLink` の `as` に `Link`(Next.js)や `RouterLink`(Vue Router)を渡します。
- 書体の読み込みと、選んだ色を表示の前に当てる `<head>` のスクリプトは「1. 読み込み方」のとおりに書きます。
- ないものを作るときは「8. Kasane にない部品を作るとき」に従います。
