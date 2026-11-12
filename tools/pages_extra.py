# Extra pages for the non-component sections. Executed inside build_site.py (uses page, sec, ex, dd, code, table, CSS, I_*).

I_PLUS, I_MENU, I_CHEV = icon('plus'), icon('menu'), icon('chevron-right')

# ---------------------------------------------------------------- はじめに
page('with-ai', 'Claude Code や Codex などの AI にUIを作ってもらうときに、Kasane のルールを守ってもらう方法です。ファイルを手元に置かなくても、URLを伝えるだけで使えます。',
  sec('AI に読ませるもの', '<p>AI には、このドキュメントサイトではなく、仕様書の <code>kasane.md</code> を読ませます。動きのあるページや大きなファイルは、AI がうまく読み取れないためです。仕様書には、ルールとその理由、全トークン、全部品の HTML、Kasane にない部品の作り方、作業後のチェックリストが入っています。</p>'
      + table(['ファイル', '内容'], [
          ['<code>' + BASE + '/kasane.md</code>', '仕様書(AI と人が読む)'],
          ['<code>' + BASE + '/kasane.min.css</code>', 'すべてのトークンと部品の CSS'],
          ['<code>' + BASE + '/tokens.json</code>', 'トークンの値(W3C Design Tokens 形式)'],
          ['<code>llms.txt</code>', 'AI に仕様書の場所を知らせる案内(サイトの一番上に置く)']]))
  + sec('Claude Code で使う', '<p>プロジェクトの <code>CLAUDE.md</code> に、次の内容を書きます。作業のたびに自動で読み込まれます。</p>'
      + code('Markdown', '## UI\n\nUIを作る・変更するときは、作業の前に次の仕様書を最後まで読み、そのルールに従うこと。\n' + BASE + '/kasane.md\n\nCSSは次を読み込む。\n' + BASE + '/kasane.min.css\n\n作業の最後に、仕様書の「作業の最後に確かめること」をすべて確かめること。')
      + '<p>URLを読むたびに許可を求められる場合は、配信先のドメインを Claude Code の設定で許可しておくと、聞かれなくなります。</p>')
  + sec('Codex で使う', '<p>プロジェクトの <code>AGENTS.md</code> に、上と同じ内容を書きます。Codex をネットにつながらない設定で使っているとURLを読めないので、その場合は <code>kasane.md</code> をリポジトリに置き、そのファイルを読むように書きます。</p>')
  + sec('ほかの AI で使う', '<p>チャットで使う場合は、<code>kasane.md</code> の内容を貼るか、ファイルとして添付します。プロジェクトの指示に入れておくと、毎回貼る必要がなくなります。</p>')
  + sec('自動でチェックする', '<p>AI は長い指示の一部を読み落とすことがあります。<code>kasane-lint</code> を入れると、ルールの多くを機械的に確かめられます。CSS は Stylelint、HTML は <code>kasane-check</code> が見ます。CSSと同じ配信先から入れられ、GitHub のアカウントは要りません。</p>'
      + code('bash', 'npm install --save-dev stylelint ' + LINT_URL)
      + '<p>プロジェクトに <code>.stylelintrc.json</code> を作ります。</p>'
      + code('JSON', '{\n  "extends": ["kasane-lint/stylelint"]\n}')
      + code('bash', 'npx stylelint "src/**/*.css"\nnpx kasane-check "src/**/*.html"')
      + '<p>同じパッケージに、画像を軽くして SSIM を確かめる <code>kasane-image</code> と、Lighthouse の最低点を確かめる <code>kasane-lighthouse</code> も入っています。使い方は <a href="#performance">パフォーマンス</a> にあります。</p>'
      + '<p>URLのファイル名には版の番号が入っています。ルールを更新するときは新しい番号のファイルを出すので、入れたものが勝手に変わることはありません。</p>'
      + '<p>AI に自分で直してもらうには、<code>CLAUDE.md</code> や <code>AGENTS.md</code> に次の1行を足します。</p>'
      + code('Markdown', '作業の最後に npx stylelint "src/**/*.css" と npx kasane-check "src/**/*.html" を実行し、出たものをすべて直すこと。\n画像は npx kasane-image で軽くしてから使うこと。\n画面ができたら npx kasane-lighthouse で評価し、最低点に届くまで直すこと。'))
  + sec('CSS のルール(Stylelint)', table(['ルール', '見つけるもの'], [
          ['<code>kasane/no-raw-color</code>', '色の直接指定(<code>#fff</code>、<code>rgb()</code>、色の名前など)'],
          ['<code>kasane/no-shadow</code>', '<code>box-shadow</code> などの影'],
          ['<code>kasane/border-only-on-inputs</code>', '入力の部品以外への枠線と区切り線'],
          ['<code>kasane/use-tokens</code>', '角丸、余白、文字の大きさ、動きの長さの直接指定(警告)'],
          ['<code>kasane/no-outline-none</code>', '<code>outline: none</code>'],
          ['<code>kasane/font-family-token</code>', 'トークン以外の書体の指定']])
      + '<p>自分で作った入力欄のクラスに枠を付けたいときは、設定で許可できます。</p>'
      + code('JSON', '{\n  "extends": ["kasane-lint/stylelint"],\n  "rules": {\n    "kasane/border-only-on-inputs": [true, { "inputSelectors": ["\\\\.app-search"] }]\n  }\n}'))
  + sec('HTML のルール(kasane-check)', table(['ルール', '見つけるもの'], [
          ['<code>kasane/one-primary</code>', '1つの画面に主ボタンが2つ以上ある'],
          ['<code>kasane/status-icon</code>', '成功・エラー・情報のバッジやエラー文にアイコンがない'],
          ['<code>kasane/inline-style</code>', '<code>style</code> 属性に色・影・枠線・書体が直接書かれている'],
          ['<code>kasane/icon-button-label</code>', '文字のないボタンやリンクに <code>aria-label</code> がない'],
          ['<code>kasane/form-label</code>', '入力欄にラベルがない'],
          ['<code>kasane/switch-structure</code>', 'スイッチの中に必要な要素がない'],
          ['<code>kasane/unknown-class</code>', 'Kasane にない <code>k-</code> のクラス(書き間違いや作り話)'],
          ['<code>kasane/lucide-icon</code>', 'Lucide に実在しないアイコン名、部品の中の Lucide 以外のアイコン'],
          ['<code>kasane/dialog-label</code>', 'ダイアログに名前がない'],
          ['<code>kasane/tab-aria</code>', 'タブに <code>aria-selected</code> か <code>aria-controls</code> がない'],
          ['<code>kasane/img-alt</code>', '画像に <code>alt</code> がない'],
          ['<code>kasane/img-size</code>', '画像に <code>width</code> と <code>height</code> がない'],
          ['<code>kasane/img-format</code>', 'JPEG・PNG・GIF をそのまま使っている']])
      + '<p>理由があってルールから外れる所には、<code>data-kasane-ignore</code> を付けると、その要素と中身を検査から外せます。ルール名を書くと、そのルールだけを外せます。</p>'
      + code('HTML', '<section data-kasane-ignore="one-primary">…</section>')
      + '<p>React などで HTML を JavaScript の中に書いている場合は、ビルドして書き出した HTML(<code>dist/**/*.html</code> など)を検査します。</p>'
      + '<p>機械で見つけられないこと(見た目のバランスや、文章の書き方など)は、仕様書のチェックリストと、画面を撮っての見直しで確かめます。</p>')
  + sec('画面を撮って確かめる', '<p>スクリーンショットを撮れる AI(Playwright やブラウザを操作できるもの)には、作った画面をライト・ダーク、パソコン・スマートフォンの幅で撮って見直すよう、仕様書で指示しています。文字の切れや重なり、読みにくい色の組み合わせ、部品の大きさのばらつきなど、ルールでは見つけにくい崩れを拾えます。撮れない環境では、撮れなかったことを報告するよう書いてあります。</p>'))

page('updates', 'Kasane の変更の記録です。',
  sec('2026年11月', '<ul class="log">'
      '<li><time class="k-num">11.12</time><div><b>アクセシビリティとパフォーマンスのページを追加</b><span>画像を軽くして SSIM を確かめる kasane-image と、Lighthouse の最低点を確かめる kasane-lighthouse を加えました。</span></div></li>'
      '<li><time class="k-num">11.11</time><div><b>アイコンを Lucide に統一、HTML のチェックを追加</b><span>アイコンは Lucide だけを使う決まりにしました。kasane-check で、HTML の使い方も自動で確かめられます。</span></div></li>'
      '<li><time class="k-num">11.11</time><div><b>URLでの配信と自動チェックを用意</b><span>CSSを1本にまとめ、AI用の仕様書(kasane.md)と Stylelint のプラグインを加えました。</span></div></li>'
      '<li><time class="k-num">11.11</time><div><b>ドキュメントサイトを作成</b><span>はじめに、原則、スタイル、コンポーネントの4セクションで構成しました。初回に色を選ぶ画面と、ライト・ダークの切り替えがあります。</span></div></li>'
      '<li><time class="k-num">11.11</time><div><b>色以外は Hidamari を引き継ぐことに決定</b><span>書体(LINE Seed JP、Zen Maru Gothic、Inter)、角丸、部品を引き継ぎました。</span></div></li>'
      '<li><time class="k-num">11.11</time><div><b>アクセントは9色のパレットから選ぶ方式に決定</b><span>山吹、橘、紅梅、藤、藍、空、青磁、萌黄、墨。全色でコントラストの基準を検査しました。</span></div></li>'
      '<li><time class="k-num">11.10</time><div><b>名前を Kasane に決定</b><span>Hidamari とは切り離した、色を選べるデザインシステムとして始めました。</span></div></li></ul>'))

# ---------------------------------------------------------------- 原則
page('writing', '画面の言葉も、デザインの一部です。やわらかく、短く、具体的に書きます。',
  sec('基本', '<ul class="links">'
      '<li><b>です・ます体で書く</b><span>親しみやすく、ていねいな印象にします。</span></li>'
      '<li><b>1文を短くする</b><span>1つの文には、1つのことだけを書きます。</span></li>'
      '<li><b>利用者が知っている言葉を使う</b><span>内部の用語や英語の略語を、そのまま出しません。</span></li>'
      '<li><b>絵文字を見出しの飾りにしない</b><span>見出しは言葉だけで伝えます。</span></li></ul>')
  + sec('ボタンの言葉', '<p>ボタンには、押すと何が起きるかを動詞で書きます。</p>'
      + dd('<div class="inline"><button class="k-btn k-btn-quiet" type="button">キャンセル</button><button class="k-btn k-btn-primary" type="button">予約を確定する</button></div>', '押した結果が、ボタンの言葉から分かります。',
           '<div class="inline"><button class="k-btn k-btn-quiet" type="button">いいえ</button><button class="k-btn k-btn-primary" type="button">OK</button></div>', '「OK」や「はい」だけでは、何が起きるのかが分かりません。'))
  + sec('エラーの言葉', '<p>何が起きたかと、どうすれば直るかを書きます。利用者を責める言い方は避けます。</p>'
      + dd('<span class="k-error" style="font-weight:700">%s「@」のあとにドメインを入力してください。</span>' % I_WARN, '直し方が具体的に分かります。',
           '<span class="k-error" style="font-weight:700">%s入力内容が不正です。</span>' % I_WARN, '何が問題で、どう直せばよいのかが分かりません。'))
  + sec('数字と日付', '<p>数字は半角で書き、単位との間は空けません。縦に並べるときは <code>.k-num</code> で桁をそろえます。日付は「11月5日(木)」のように、曜日を添えると予定を立てやすくなります。</p>'
      + ex('<span><span class="k-num">3</span>件の予定 ・ <span class="k-num">11</span>月<span class="k-num">5</span>日(木)まで</span>')))

# ---------------------------------------------------------------- スタイル
page('layout', '画面は、面を重ねて組み立てます。余白は部品の外側ではなく、並べる側で決めます。',
  sec('面の順番', '<p>ページの背景の上にカードを置き、カードの中のまとまりは中の面で作ります。同じ色の面を直接重ねないでください。</p>'
      + ex('<div class="k-card">\n  <h3 class="k-card-title">今週の予定</h3>\n  <ul class="k-list">\n    <li class="k-list-item"><span class="k-list-item-main">図書館の本を返す</span></li>\n    <li class="k-list-item"><span class="k-list-item-main">発表スライドの確認</span></li>\n  </ul>\n</div>', True)
      + table(['場所', '面', '角丸'], [['ページの背景', '<code>--bg</code>', 'なし'], ['カード、パネル', '<code>--surface</code>', '<code>--r-lg</code>'], ['中の面、リストの行', '<code>--surface-2</code>', '<code>--r-md</code>'], ['ホバー、押下', '<code>--surface-3</code>', '同じ']]))
  + sec('並べ方', '<p>部品どうしの間隔は、親の <code>gap</code> で決めます。部品に外側の余白(margin)を持たせないので、どこに置いても間隔がそろいます。</p>'
      + code('CSS', '.page  { display: flex; flex-direction: column; gap: var(--space-7); }  /* 章と章の間 */\n.cards { display: grid; gap: var(--space-4);\n         grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); }'))
  + sec('幅', table(['対象', '幅'], [['文章', '最大38em(全角で35〜40文字)'], ['本文の列', '最大1040px'], ['画面の左右の余白', '16px以上']]))
  + sec('画面の幅による切り替え', '<p>このサイトは、2つの幅で配置を変えています。カードの並びは、幅に応じて自動で折り返します。</p>'
      + table(['幅', '変わること'], [['1100px以下', '右の目次を隠す'], ['820px以下', '左のナビゲーションをメニューに入れ、1列にする']])
      + code('CSS', '.shell { display: grid; grid-template-columns: 248px minmax(0, 1fr) 216px; gap: var(--space-5); }\n@media (max-width: 1100px) { .shell { grid-template-columns: 248px minmax(0, 1fr); } }\n@media (max-width: 820px)  { .shell { grid-template-columns: minmax(0, 1fr); } }')))

ICONS = [('成功・チェック', 'check'), ('閉じる', 'x'), ('エラー・注意', 'circle-alert'), ('情報', 'info'), ('警告', 'triangle-alert'),
         ('追加', 'plus'), ('編集', 'pencil'), ('削除', 'trash-2'), ('検索', 'search'), ('設定', 'settings'),
         ('人', 'user'), ('人たち', 'users'), ('通知', 'bell'), ('予定', 'calendar'), ('メニュー', 'menu'),
         ('進む', 'chevron-right'), ('矢印', 'arrow-right'), ('外部リンク', 'external-link'), ('ログアウト', 'log-out'), ('コード', 'code')]
page('icons', 'アイコンは Lucide を使います。線で描かれた、角の丸いアイコン集です。文字を補うもので、アイコンだけで意味を伝えることは避けます。',
  sec('使うアイコン集', '<p><a href="https://lucide.dev/icons/">Lucide</a>(ISC ライセンス)から選びます。ほかのアイコン集と混ぜたり、自分で描いたりしません。いまの版は <code>' + LUCIDE_VER + '</code> です。</p>'
      + table(['決まり', '内容'], [
          ['線の太さ', '<code>2.5</code>(Lucide の標準の2より少し太く。<code>kasane.css</code> が自動で 2.5 にします)'],
          ['色', '<code>currentColor</code>(まわりの文字と同じ色)'],
          ['塗り', 'しない(線のアイコンだけ)'],
          ['クラス', 'Lucide の <code>class="lucide lucide-名前"</code> を消さない(自動チェックで使います)']]))
  + sec('よく使うアイコン', '<p>名前で探して、<code>lucide.dev</code> からコピーするか、次の場所から SVG を取ってきて貼ります。</p>'
      '<div class="icon-grid">' + ''.join('<div>%s<small>%s</small><code>%s</code></div>' % (icon(n), l, n) for l, n in ICONS) + '</div>'
      + code('bash', 'curl ' + LUCIDE_URL + '/user-plus.svg'))
  + sec('状態のアイコン', '<p>状態を表すときは、次のアイコンを使います。</p>'
      + table(['状態', 'アイコン', '名前'], [['成功', I_OK, '<code>check</code>'], ['エラー', I_WARN, '<code>circle-alert</code>'], ['情報', I_INFO, '<code>info</code>'], ['閉じる', I_NG, '<code>x</code>']]))
  + sec('大きさ', table(['場所', '大きさ'], [['バッジの中', '14px'], ['エラーの文の前', '16px'], ['ボタンの中', '18px'], ['アイコンだけのボタン', '22px']])
      + '<p>Kasane の部品の中に置けば、大きさは CSS で自動的に決まります。</p>')
  + sec('ボタンの中で使う', ex('<button class="k-btn k-btn-primary" type="button">%s予定を追加</button>' % I_PLUS))
  + sec('アイコンだけのボタン', '<p>文字がないボタンには、<code>aria-label</code> で名前を付けます。</p>'
      + ex('<button class="k-btn k-btn-icon" type="button" aria-label="メニューを開く">%s</button>' % I_MENU)
      + dd('<span class="k-badge k-badge-ok">%s完了</span>' % I_OK, 'アイコンに文字を添えます。',
           '<span class="k-badge k-badge-ok" style="padding:4px 8px">%s</span>' % I_OK.replace('<svg ', '<svg style="margin:0" ', 1), 'アイコンだけで状態を表しません。'))
  + sec('AI に頼むとき', '<p>AI はアイコンの形を記憶から描いてしまうことがあります。仕様書では「名前を決めて、SVG は必ず取ってきて貼る」と指示しています。自動チェックでは、Lucide に実在しない名前を見つけられます。</p>'))

page('motion', '動きは短く、控えめにします。画面が変わったことに気づけて、操作を待たせない長さにします。',
  sec('動きの役割', '<p>Kasane の動きには、3つの役割があります。飾りのための動きは使いません。</p>'
      + table(['役割', '例', '長さ'], [
          ['現れたことを伝える', 'ページの切り替え、カードの表示', '<code>--motion-slow</code>'],
          ['開いた・閉じたことを伝える', 'ダイアログ、メニュー', '<code>--motion-base</code>'],
          ['操作に反応する', 'ボタンを押す、スイッチを切り替える', '<code>--motion-fast</code>']]))
  + sec('トークン', table(['トークン', '値', '使う場所'], [
        ['<code>--motion-fast</code>', '150ms', 'ボタンの色と押し込み、スイッチ'],
        ['<code>--motion-base</code>', '220ms', 'ダイアログ、メニューの開閉'],
        ['<code>--motion-slow</code>', '450ms', 'ページの切り替え、部品が現れるとき'],
        ['<code>--ease-out</code>', 'cubic-bezier(.2, .7, .3, 1)', 'すばやく始まり、ゆっくり止まる']]))
  + sec('現れる', '<p>ページや部品が現れるときは、16px下から浮かび上がらせます。<code>.k-enter</code> を付けるだけで使えます。</p>'
      '<div class="ex"><div class="ex-demo ex-stack"><div class="k-card k-enter" id="motion-demo"><h3 class="k-card-title">今週のおしらせ</h3><p class="k-card-text">金曜日は、図書館が17時に閉まります。</p></div><button class="k-btn" type="button" data-replay="motion-demo" style="align-self:center;width:auto">もう一度動かす</button></div>'
      + code('HTML', '<div class="k-card k-enter">...</div>') + '</div>')
  + sec('ページを切り替える', '<p>このサイトのページ切り替えも、同じ動きです。前のページは動かさずに消し、次のページだけを浮かび上がらせます。両方を動かすと、切り替えのたびに待つ時間が長くなるためです。</p>'
      + code('CSS', '.page:not([hidden]) { animation: k-enter var(--motion-slow) var(--ease-out); }\n@media (prefers-reduced-motion: reduce) { .page:not([hidden]) { animation: none; } }')
      + code('JavaScript', '// hidden を付け外しすると、表示のたびに動きが最初から再生されます\nfunction showPage(id) {\n  document.querySelectorAll(".page").forEach((p) => { p.hidden = p.dataset.page !== id; });\n  window.scrollTo(0, 0);\n}'))
  + sec('開く・閉じる', '<p>ダイアログは、背景をふわっと暗くし、本体を下から浮かび上がらせます。閉じるときは動かさず、すぐに消します。</p>'
      '<div class="ex"><div class="ex-demo"><button class="k-btn" type="button" data-open-demo>ダイアログを開く</button></div>'
      + code('CSS', '.k-scrim  { animation: k-fade var(--motion-base); }\n.k-dialog { animation: k-enter var(--motion-base) var(--ease-out); }') + '</div>'
      '<div class="k-scrim" id="demo-dialog" hidden><div class="k-dialog" role="dialog" aria-modal="true" aria-labelledby="demo-dialog-title"><h3 class="k-dialog-title" id="demo-dialog-title">このメモを削除しますか?</h3><p class="k-dialog-text">これは動きの見本です。どちらを押しても、何も削除されません。</p><div class="k-dialog-actions"><button class="k-btn k-btn-quiet" type="button" data-close-demo>キャンセル</button><button class="k-btn k-btn-danger" type="button" data-close-demo>削除する</button></div></div></div>')
  + sec('操作に反応する', '<p>ボタンは、押すと1pxだけ沈みます。スイッチは、つまみが150msで動きます。タブや2択の切り替えでは、選択中の背景が220msで横へ動きます。押した瞬間に反応が返ることを優先して、短くしています。</p>'
      + ex('<button class="k-btn k-btn-primary" type="button">押してみる</button>\n<label class="k-switch">\n  <input type="checkbox" checked>\n  <span class="k-switch-track" aria-hidden="true"></span>\n  切り替えてみる\n</label>\n<div class="k-seg" role="group" aria-label="表示">\n  <button type="button" aria-pressed="true" data-seg-demo>週</button>\n  <button type="button" aria-pressed="false" data-seg-demo>月</button>\n  <button type="button" aria-pressed="false" data-seg-demo>年</button>\n</div>')
      + code('CSS', '.k-btn { transition: background-color var(--motion-fast), transform var(--motion-fast); }\n.k-btn:active { transform: translateY(1px); }\n.k-switch-track::after { transition: transform var(--motion-fast); }'))
  + sec('動きを減らす設定', '<p>端末で「視差効果を減らす」が有効なときは、すべての動きを止めます。動きがなくても、内容と状態はすべて分かるようにします。</p>'
      + code('CSS', '@media (prefers-reduced-motion: reduce) {\n  .k-enter, .k-scrim, .k-dialog { animation: none; }\n  .k-btn, .k-switch-track, .k-switch-track::after { transition: none; }\n}'))
  + sec('使い方', dd('<div class="k-card mini k-enter" id="dd-motion"><b>保存しました</b><span style="color:var(--muted)">一度だけ、静かに現れます。</span></div>', '動かすのは透明度と位置だけにして、一度で止めます。',
                    '<div class="k-card mini bad-motion"><b>保存しました</b><span style="color:var(--muted)">ずっと揺れ続けます。</span></div>', '点滅や、揺れ続ける動きは使いません。読むじゃまになります。')
      + '<ul class="links">'
      '<li><b>450msより長くしない</b><span>長い動きは、操作のたびに待たされる感じになります。</span></li>'
      '<li><b>消えるときは動かさない</b><span>閉じる操作は、すぐに終わらせます。</span></li></ul>')
  + sec('CSS', code('CSS', CSS['motion'])))

# ---------------------------------------------------------------- 原則: アクセシビリティ / パフォーマンス
LH_MIN = [('パフォーマンス', 'performance', 90), ('アクセシビリティ', 'accessibility', 100), ('ベストプラクティス', 'best-practices', 95), ('SEO', 'seo', 90)]
REF_SPINDLE_A11Y = '<a href="https://spindle.ameba.design/principles/accessibility/">Spindle(Ameba)のアクセシビリティ</a>'
REF_SPINDLE_PERF = '<a href="https://spindle.ameba.design/principles/performance/">Spindle(Ameba)のパフォーマンス</a>'

page('accessibility', '誰でも、どんな状況でも、迷わず読めて、操作できる状態を目指します。色を選べる Kasane では、どの色を選んでも同じように使えることが土台です。',
  sec('目指すこと', '<p>使いにくさは、障害のある人だけのものではありません。年齢を重ねたとき、けがをしたとき、眼鏡を忘れたとき、外の光が強いとき、片手がふさがっているとき。状況が変わると、誰でも同じ画面が使いにくくなります。</p>'
      '<p>アクセシビリティを高めると、そうした状況でも使えるようになり、ふだんの使いやすさも上がります。全員にとって完ぺきな形は作れなくても、別の見せ方や操作の手段を用意すれば、使える人は確実に増えます。</p>')
  + sec('4つの使いにくさ', '<p>どんな使いにくさがあるかを知ることが、最初の一歩です。Kasane の部品は、次の点に気をつけて作っています。</p>'
      + table(['使いにくさ', 'たとえば', 'Kasane で気をつけていること'], [
          ['見えにくい', '文字がぼやける、外の光で画面が読めない、色の区別がつきにくい、画面が見えない',
           '全パレットで文字のコントラスト 4.5:1 以上。色だけで伝えない。拡大しても崩れない。スクリーンリーダーで読める'],
          ['聞こえにくい', '音を出せない場所にいる、耳が聞こえにくい', '音だけで知らせない。動画には字幕を付ける'],
          ['操作しにくい', '手がふるえる、片手しか使えない、マウスを使えない', '押せる場所は高さ44px以上。キーボードだけで操作できる。複雑な操作に頼らない'],
          ['わかりにくい', '長い文が読みにくい、アイコンの意味がわからない、動きに気を取られる', '短くやさしい文。アイコンに文字を添える。動きは控えめで、止められる']]))
  + sec('基準', '<p>WCAG 2.2 の AA を目安にします。Kasane の部品と仕様書は、このうち見た目と部品の作りで守れるものを、あらかじめ満たすように作っています。</p>')
  + sec('コントラスト', '<p>9色すべてで、ライトとダークの両方がこの基準を満たすことを、パレットを作るときに自動で検査しています。</p>'
      + table(['対象', '使うトークン', '基準'], [
          ['本文の文字', '<code>--ink</code>、<code>--muted</code>', '面に対して 4.5:1 以上'],
          ['主ボタンの上の文字', '<code>--on-accent</code>', '<code>--accent</code> に対して 4.5:1 以上'],
          ['アクセント色の文字・リンク', '<code>--accent-ink</code>', '面と <code>--accent-soft</code> に対して 4.5:1 以上'],
          ['状態の文字', '<code>--ok</code>、<code>--danger</code>、<code>--info</code>', '対応する <code>-soft</code> の面に対して 4.5:1 以上'],
          ['入力欄の枠、スイッチのオフ', '<code>--line</code>', '<code>--surface</code> に対して 3:1 以上'],
          ['フォーカスのリング', '<code>--focus</code>', '面に対して 3:1 以上']]))
  + sec('色だけで伝えない', '<p>山吹や青磁など明るいパレットでは、ライトのときに <code>--accent</code> の塗りと面の差が 3:1 に届きません。「選ばれている」「オンになっている」を塗りの色だけで伝えず、チェックの印、スイッチのつまみの位置、文字などを組み合わせます。</p>'
      + dd('<label class="k-switch"><input type="checkbox" checked id="a11y-sw1"><span class="k-switch-track" aria-hidden="true"></span>通知 オン</label>', 'つまみの位置と文字でも、オンだと分かります。',
           '<div class="inline"><span style="width:44px;height:24px;border-radius:999px;background:var(--accent);display:block"></span><span style="width:44px;height:24px;border-radius:999px;background:var(--surface-3);display:block"></span></div>', '色の違いだけでオンとオフを表しません。'))
  + sec('キーボードとフォーカス', '<p>操作できる部品はすべて、Tab キーで移動でき、Enter やスペースで操作できるようにします。フォーカスが当たったときは <code>--focus</code> の3pxのリングを表示し、消しません。マウスを乗せたときだけ見える情報は、フォーカスしたときにも見せます。</p>'
      + code('CSS', ':focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }'))
  + sec('スクリーンリーダー', '<ul class="links">'
      '<li><b>入力欄にはラベル</b><span><code>&lt;label&gt;</code> で囲むか、<code>for</code> で結びます。</span></li>'
      '<li><b>文字のないボタンには名前</b><span>アイコンだけのボタンには <code>aria-label</code> を付けます。</span></li>'
      '<li><b>画像には説明</b><span><code>alt</code> に内容を書きます。飾りの画像は <code>alt=""</code> にします。</span></li>'
      '<li><b>あとから出る知らせは読み上げる</b><span>トーストには <code>role="status"</code> を付けます。</span></li>'
      '<li><b>見出しは順番どおりに</b><span>h1、h2、h3 の順に使い、段を飛ばしません。</span></li></ul>')
  + sec('押せる場所の大きさ', '<p>ボタンや選択肢は、高さ44px以上を基本にします。小さいボタン(<code>.k-btn-sm</code>)でも36pxです。押せる場所どうしは、間を8px以上あけます。</p>')
  + sec('動きを減らす設定', '<p>端末で「視差効果を減らす」が有効なときは、Kasane の動きはすべて止まります。動きがなくても、内容と状態はすべて分かるようにします。</p>'
      + code('CSS', '@media (prefers-reduced-motion: reduce) {\n  .k-enter, .k-dialog { animation: none; }\n}'))
  + sec('確かめ方', '<p>自動の検査と、人の目と手による確認を組み合わせます。</p>'
      + table(['確かめること', '方法'], [
          ['部品の使い方(ラベル、名前、画像の説明など)', '<code>npx kasane-check "src/**/*.html"</code>'],
          ['自動で見つけられる問題の全体', '<code>npx kasane-lighthouse URL</code> でアクセシビリティ 100 点'],
          ['キーボードだけで最後まで操作できるか', 'マウスを使わずに、Tab と Enter で一通り操作する'],
          ['拡大しても崩れないか', 'ブラウザで 200% に拡大して見る'],
          ['読み上げで内容が伝わるか', 'VoiceOver(Mac・iPhone)や NVDA(Windows)で一度読み上げる']])
      + '<p>自動の検査で見つかるのは、問題の一部だけです。最後は実際に操作して確かめます。</p>')
  + sec('参考にしたもの', '<ul class="links">'
      '<li>' + REF_SPINDLE_A11Y + '<span>目指す状態と、4つの使いにくさの考え方</span></li>'
      '<li><a href="https://www.w3.org/TR/WCAG22/">WCAG 2.2</a><span>Web のアクセシビリティの国際的な基準</span></li></ul>'))

page('performance', '表示が速く、動きが安定していて、思わぬ動きがない状態を目指します。読みたいものがすぐに見えて、触ったらすぐに反応することは、それだけで使いやすさです。',
  sec('目指す状態', '<ul class="links">'
      '<li><b>すぐに見える</b><span>読みたい内容や大事な部品が、できるだけ早く表示される。</span></li>'
      '<li><b>すぐに反応する</b><span>スクロールやタップに、遅れずに応える。</span></li>'
      '<li><b>ずれない</b><span>読み込みの途中で、部品が動いたり消えたりしない。</span></li></ul>')
  + sec('Lighthouse の最低点', '<p>作った画面は、Lighthouse で評価します。モバイルとデスクトップの両方で、次の点数を下回らないことが条件です。</p>'
      + table(['項目', '最低点'], [[l, '<span class="k-num">%d</span> 点以上' % v] for l, _, v in LH_MIN])
      + '<p><code>kasane-lighthouse</code> は Lighthouse CLI を実行して、最低点に届かない項目と、点数を下げている原因を表示します。</p>'
      + code('bash', 'npm install --save-dev lighthouse\nnpx kasane-lighthouse http://localhost:3000/ http://localhost:3000/users')
      + code('text', 'http://localhost:3000/  (モバイル)\n  ✓ パフォーマンス　　　  96  (最低 90)\n  ✓ アクセシビリティ　　 100  (最低 100)\n  ✓ ベストプラクティス　  96  (最低 95)\n  ✓ SEO　　　　　　　 100  (最低 90)')
      + '<p>点数は通信やパソコンの状態で少し揺れます。揺れが気になるときは <code>--runs 3</code> で3回測り、真ん中の結果を使います。Chrome が見つからないときは、<code>CHROME_PATH</code> に場所を指定します。</p>')
  + sec('目標の指標', '<p>Lighthouse の点数のもとになる指標のうち、特に次の3つを目標にします。</p>'
      + table(['指標', '意味', '目標'], [
          ['LCP', 'いちばん大きな内容が表示されるまでの時間', '<span class="k-num">2.5</span> 秒以内'],
          ['INP', '操作してから画面が反応するまでの時間', '<span class="k-num">200</span> ミリ秒以内'],
          ['CLS', '読み込み中に画面がずれた量', '<span class="k-num">0.1</span> 以下']]))
  + sec('画像', '<p>画像は、ページの重さの大部分を占めます。そのまま置かず、必ず軽くしてから使います。</p>'
      + table(['決まり', '内容'], [
          ['形式', '写真やイラストは AVIF と WebP。アイコンやロゴは SVG。動く画像は GIF ではなく動画'],
          ['大きさ', '表示する大きさの2倍まで。幅の種類は3つ(大・中・小)までにする'],
          ['画質', '元の画像との SSIM が <span class="k-num">0.99</span> 以上。最後は目でも確かめる'],
          ['容量', '1枚 <span class="k-num">100</span> KB を超えたら、幅を小さくできないか見直す'],
          ['ずれを防ぐ', '<code>width</code> と <code>height</code> を必ず書く'],
          ['読み込み', '画面の外の画像は <code>loading="lazy"</code>。最初に見える大きな画像は <code>fetchpriority="high"</code>']]))
  + sec('画像を軽くする', '<p><code>kasane-image</code> は、幅ごと・形式ごとに画像を書き出し、元の画像との SSIM が基準以上になる一番低い画質を自動で選びます。そのまま貼れる <code>&lt;picture&gt;</code> も表示します。</p>'
      + code('bash', 'npm install --save-dev sharp ssim.js\nnpx kasane-image photo.jpg --out public/img --widths 640,1280')
      + code('text', 'photo.jpg  (2400×1600, 1820 KB)\n  ✓ public/img/photo-640.avif     q=46  SSIM 0.9903     28.4 KB\n  ✓ public/img/photo-640.webp     q=71  SSIM 0.9901     41.2 KB\n  ✓ public/img/photo-1280.avif    q=42  SSIM 0.9905     79.0 KB\n  ✓ public/img/photo-1280.webp    q=68  SSIM 0.9900    112.6 KB  (目安 100 KB を超えています…)')
      + code('HTML', '<picture>\n  <source type="image/avif" srcset="img/photo-640.avif 640w, img/photo-1280.avif 1280w" sizes="100vw">\n  <img src="img/photo-640.webp" srcset="img/photo-640.webp 640w, img/photo-1280.webp 1280w" sizes="100vw"\n       width="1280" height="853" alt="夕方の公園" loading="lazy" decoding="async">\n</picture>')
      + '<p>ほかの道具で軽くした画像は、<code>--compare</code> で SSIM だけを確かめられます。<code>kasane-check</code> は、JPEG や PNG をそのまま使っている所や、<code>alt</code>、<code>width</code>、<code>height</code> がない画像を見つけます。</p>'
      + code('bash', 'npx kasane-image --compare original.png public/img/photo.avif')
      + dd('<div class="stack" style="font-size:14px"><span class="k-num">photo-1280.avif</span><span class="k-badge k-badge-ok">' + I_OK + '79 KB ・ SSIM 0.990</span></div>', '軽くしたうえで、画質を数字で確かめます。',
           '<div class="stack" style="font-size:14px"><span class="k-num">IMG_2041.PNG</span><span class="k-badge k-badge-danger">' + I_WARN + '4.8 MB ・ 未処理</span></div>', '撮った写真をそのまま置きません。'))
  + sec('フォント', '<p>LINE Seed JP は、文字の範囲ごとに細かく分けて配信しているので、ページで使う文字の分だけが読み込まれます。フォントの CSS は表示を止めないように読み込み、読み込みが終わるまではいつもの書体で表示します。</p>'
      + code('HTML', '<link rel="stylesheet" href="' + BASE + '/fonts/line-seed-jp.css" media="print" onload="this.media=\'all\'">\n<noscript><link rel="stylesheet" href="' + BASE + '/fonts/line-seed-jp.css"></noscript>'))
  + sec('画面のずれを防ぐ', '<ul class="links">'
      '<li><b>大きさを先に決める</b><span>画像や埋め込みには <code>width</code> と <code>height</code> を書き、読み込む前から場所を空けておきます。</span></li>'
      '<li><b>読み込み中も同じ大きさ</b><span>読み込み中、0件、失敗したときも、同じ大きさの場所を使います。</span></li>'
      '<li><b>あとから差し込まない</b><span>読み込みが終わってから、上に部品を足しません。ログインの状態で部品を消さず、同じ大きさで入れ替えます。</span></li></ul>')
  + sec('CSS と JavaScript', '<ul class="links">'
      '<li><b>縮小版を使う</b><span>本番では <code>kasane.min.css</code>(約 21 KB)を読み込みます。</span></li>'
      '<li><b>表示を止めない</b><span>JavaScript には <code>defer</code> を付けます。大きなライブラリは、本当に必要なときだけ使います。</span></li>'
      '<li><b>長い処理を分ける</b><span>重い処理は細かく分けて、操作への反応を止めないようにします。</span></li></ul>')
  + sec('確かめ方', '<p>作業の最後に、次の3つを実行します。CI に入れておくと、遅くなった変更をすぐに見つけられます。</p>'
      + code('bash', 'npx kasane-image --compare original.png public/img/photo.avif   # 画像の画質\nnpx kasane-check "dist/**/*.html"                               # 画像の属性と形式\nnpx kasane-lighthouse http://localhost:3000/                     # 最低点'))
  + sec('参考にしたもの', '<ul class="links">'
      '<li>' + REF_SPINDLE_PERF + '<span>目指す状態、画像やレイアウトのずれのチェックリスト</span></li>'
      '<li><a href="https://web.dev/articles/vitals">Web Vitals</a><span>LCP、INP、CLS の考え方と目標</span></li>'
      '<li><a href="https://developer.chrome.com/docs/lighthouse/overview">Lighthouse</a><span>評価に使う道具</span></li></ul>'))
