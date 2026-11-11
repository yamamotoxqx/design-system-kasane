# Extra pages for the non-component sections. Executed inside build_site.py (uses page, sec, ex, dd, code, table, CSS, I_*).

I_PLUS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'
I_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
I_CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'

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
  + sec('自動でチェックする', '<p>AI は長い指示の一部を読み落とすことがあります。Stylelint のプラグインを入れると、色の直接指定、影、入力の部品以外の枠線、トークン以外の角丸や余白などを、機械的に見つけられます。</p>'
      + '<p>ルールは、CSSと同じ配信先からパッケージとして入れられます。GitHub のアカウントや認証は要りません。</p>'
      + code('bash', 'npm install --save-dev stylelint ' + LINT_URL)
      + '<p>プロジェクトに <code>.stylelintrc.json</code> を作ります。</p>'
      + code('JSON', '{\n  "extends": ["stylelint-config-kasane"]\n}')
      + code('bash', 'npx stylelint "src/**/*.css"')
      + '<p>URLのファイル名には版の番号が入っています。ルールを更新するときは新しい番号のファイルを出すので、入れたものが勝手に変わることはありません。</p>'
      + '<p>AI に自分で直してもらうには、<code>CLAUDE.md</code> や <code>AGENTS.md</code> に次の1行を足します。</p>'
      + code('Markdown', 'CSSを変更したら、作業の最後に npx stylelint "src/**/*.css" を実行し、出たものをすべて直すこと。')
      + table(['ルール', '見つけるもの'], [
          ['<code>kasane/no-raw-color</code>', '色の直接指定(<code>#fff</code>、<code>rgb()</code>、色の名前など)'],
          ['<code>kasane/no-shadow</code>', '<code>box-shadow</code> などの影'],
          ['<code>kasane/border-only-on-inputs</code>', '入力の部品以外への枠線と区切り線'],
          ['<code>kasane/use-tokens</code>', '角丸、余白、文字の大きさ、動きの長さの直接指定(警告)'],
          ['<code>kasane/no-outline-none</code>', '<code>outline: none</code>'],
          ['<code>kasane/font-family-token</code>', 'トークン以外の書体の指定']])
      + '<p>自分で作った入力欄のクラスに枠を付けたいときは、設定で許可できます。</p>'
      + code('JSON', '{\n  "extends": ["stylelint-config-kasane"],\n  "rules": {\n    "kasane/border-only-on-inputs": [true, { "inputSelectors": ["\\\\.app-search"] }]\n  }\n}')
      + '<p>機械で見つけられないこと(主ボタンが1つか、状態にアイコンがあるか、など)は、仕様書のチェックリストで確かめます。</p>'))

page('updates', 'Kasane の変更の記録です。',
  sec('2026年11月', '<ul class="log">'
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

ICONS = [('チェック', I_OK), ('閉じる', I_NG), ('注意', I_WARN), ('情報', I_INFO), ('追加', I_PLUS), ('メニュー', I_MENU), ('進む', I_CHEV)]
page('icons', 'アイコンは、角の丸い線で描きます。文字を補うもので、アイコンだけで意味を伝えることは避けます。',
  sec('描き方', '<p>24pxの枠に、太さ3の線で描きます。線の端と角は丸くします。色は <code>currentColor</code> にして、まわりの文字と同じ色にします。</p>'
      '<div class="icon-grid">' + ''.join('<div>%s<small>%s</small></div>' % (svg, name) for name, svg in ICONS) + '</div>'
      + code('HTML', I_OK))
  + sec('大きさ', table(['場所', '大きさ'], [['バッジの中', '14px'], ['ボタンの中', '18px'], ['アイコンだけのボタン', '22px']]))
  + sec('ボタンの中で使う', ex('<button class="k-btn k-btn-primary" type="button">%s予定を追加</button>' % I_PLUS))
  + sec('アイコンだけのボタン', '<p>文字がないボタンには、<code>aria-label</code> で名前を付けます。</p>'
      + ex('<button class="k-btn k-btn-icon" type="button" aria-label="メニューを開く">%s</button>' % I_MENU)
      + dd('<span class="k-badge k-badge-ok">%s完了</span>' % I_OK, 'アイコンに文字を添えます。',
           '<span class="k-badge k-badge-ok" style="padding:4px 8px">%s</span>' % I_OK.replace('<svg ', '<svg style="margin:0" '), 'アイコンだけで状態を表しません。')))

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
