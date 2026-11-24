# v2 component pages: app layout and menu, table, empty and loading states, and the v1 → v2 migration page.
# Run inside build_site.py (exec), so page(), sec(), ex(), code(), icon() and CSS are in scope.

def _brand():
    return '<svg aria-hidden="true" viewBox="0 0 28 28"><rect x="2" y="8" width="18" height="18" rx="6" fill="var(--surface-3)"/><rect x="8" y="2" width="18" height="18" rx="6" fill="var(--accent)"/></svg>'

SHELL_SRC = '''<div class="k-app">
  <header class="k-header">
    <button class="k-menu-btn" type="button" aria-label="メニュー" aria-expanded="false" aria-controls="sidebar">
      %(menu)s
    </button>
    <a class="k-header-brand" href="/">%(brand)sかさね帳</a>
    <span class="k-header-space"></span>
    <button class="k-btn k-btn-quiet k-btn-icon" type="button" aria-label="お知らせ">%(bell)s</button>
  </header>
  <div class="k-drawer-scrim" hidden></div>
  <div class="k-layout">
    <nav class="k-sidebar" id="sidebar" aria-label="メイン">
      <div class="k-sidebar-head">
        <span class="k-header-brand">%(brand)sかさね帳</span>
        <button class="k-btn k-btn-quiet k-btn-icon" type="button" aria-label="メニューを閉じる" data-k-close>%(x)s</button>
      </div>
      <div class="k-nav">
        <a class="k-nav-link" href="/" aria-current="page">%(house)sきょう</a>
        <a class="k-nav-link" href="/tasks/">%(tasks)sやること<span class="k-badge k-badge-accent">3</span></a>
        <a class="k-nav-link" href="/calendar/">%(cal)s予定</a>
      </div>
      <div class="k-nav">
        <p class="k-nav-title">その他</p>
        <a class="k-nav-link" href="/settings/">%(settings)s設定</a>
      </div>
    </nav>
    <main class="k-main">
      <nav aria-label="パンくずリスト">
        <ol class="k-breadcrumb">
          <li><a href="/">ホーム</a></li>
          <li aria-current="page">きょう</li>
        </ol>
      </nav>
      <h1 class="k-title">きょう</h1>
      <ul class="k-list">
        <li class="k-list-item"><span class="k-list-item-main">実習の記録を出す</span><span class="k-list-item-sub">15:00</span></li>
        <li class="k-list-item"><span class="k-list-item-main">図書館の本を返す</span><span class="k-list-item-sub">17:00</span></li>
      </ul>
    </main>
  </div>
</div>''' % {'menu': icon('menu'), 'bell': icon('bell'), 'x': icon('x'), 'house': icon('house'), 'tasks': icon('list-checks'),
            'cal': icon('calendar'), 'settings': icon('settings'), 'brand': '<svg aria-hidden="true" viewBox="0 0 28 28">…</svg>'}

def _demo_shell(uid, cls):
    """The shell above as a live demo: landmarks become divs, the id is unique, the logo is drawn."""
    h = SHELL_SRC.replace('<svg aria-hidden="true" viewBox="0 0 28 28">…</svg>', _brand())
    h = h.replace('id="sidebar"', 'id="%s"' % uid).replace('aria-controls="sidebar"', 'aria-controls="%s"' % uid)
    for tag in ('header', 'main'):
        h = h.replace('<%s class=' % tag, '<div class=').replace('</%s>' % tag, '</div>')
    h = h.replace('<h1 class="k-title">きょう</h1>', '<p class="k-title ex-app-h">きょう</p>')
    h = re.sub(r'href="/[^"]*"', 'href="#navigation"', h)
    return '<div class="ex-app %s">%s</div>' % (cls, re.sub(r'\n\s*', '', h))

FOOTER_SRC = '''<footer class="k-footer">
  <div class="k-footer-in">
    <nav class="k-footer-links" aria-label="このサイトについて">
      <a href="/about/">かさね帳について</a>
      <a href="/privacy/">プライバシー</a>
      <a href="/contact/">お問い合わせ</a>
    </nav>
%s
    <p class="k-footer-note">© 2026 かさね帳</p>
  </div>
</footer>''' % '\n'.join('    ' + l for l in palette_src(name='accent', compact=True, legend='テーマカラー').split('\n'))

FOOTER_DEMO = re.sub(r'\n\s*', '', FOOTER_SRC.replace('<footer class=', '<div class=').replace('</footer>', '</div>').replace('name="accent"', 'name="accent-footer"')
                     .replace('href="/about/"', 'href="#about"').replace('href="/privacy/"', 'href="#navigation"').replace('href="/contact/"', 'href="#navigation"'))

NAV_SRC = '<div class="k-nav">\n  <a class="k-nav-link" href="/" aria-current="page">%sきょう</a>\n  <a class="k-nav-link" href="/tasks/">%sやること<span class="k-badge k-badge-accent">3</span></a>\n  <a class="k-nav-link" href="/calendar/">%s予定</a>\n</div>' % (icon('house'), icon('list-checks'), icon('calendar'))

BREADCRUMB_SRC = '<nav aria-label="パンくずリスト">\n  <ol class="k-breadcrumb">\n    <li><a href="/">ホーム</a></li>\n    <li><a href="/settings/">設定</a></li>\n    <li aria-current="page">表示</li>\n  </ol>\n</nav>'

page('navigation', '画面の骨組み(ヘッダー、メニュー、サイドバー、フッター)です。どの製品でも同じ形にすると、使う人が迷いません。',
  sec('画面の骨組み', '<p>上にヘッダー、左にサイドバー、右に本文の面を置きます。幅が900px未満になると、サイドバーは左から出てくるメニュー(ドロワー)に変わり、ヘッダーの左端にメニューのボタン(3本線)が出ます。下の見本は、このサイトを見ている画面の幅で形が変わります。</p><p>本文の面 <code>.k-main</code> は <code>--surface</code> なので、中には一段内側の部品(リスト、<code>.k-nest</code>、表)を置きます。カードを並べるページでは <code>.k-main-plain</code> を足して面をなくし、<code>.k-card</code> を背景の上に直接置きます。</p>'
      + '<div class="ex"><div class="ex-demo ex-frame">' + _demo_shell('demo-side-a', 'ex-app-wide') + '</div>' + code('HTML', SHELL_SRC) + '</div>')
  + sec('スマートフォンでは', '<p>スマートフォンの幅で見たときの形です。3本線のボタンを押すと、メニューが左から出てきます。</p>'
      + '<div class="ex"><div class="ex-demo ex-frame">' + _demo_shell('demo-side-b', 'ex-app-phone') + '</div></div>'
      + '<ul class="links">'
        '<li><b>3本線のボタンは左上に1つだけ</b><span>アイコンは Lucide の <code>menu</code>。<code>aria-controls</code> でサイドバーの id を指し、開いているかを <code>aria-expanded</code> で示します。</span></li>'
        '<li><b>メニューは左から出す</b><span>幅は画面の84%(最大320px)。後ろは暗くして、押すと閉じます。Esc キーと、中の「閉じる」ボタンでも閉じます。</span></li>'
        '<li><b>開くときだけ動かす</b><span>220msで滑り込み、閉じるときはすぐに消します。開いたら、選択中のリンクにフォーカスを移します。</span></li>'
        '<li><b>広い画面では3本線を出さない</b><span>900px以上ではサイドバーを常に見せます。メニューを隠すのは、場所が足りないときだけです。</span></li>'
        '<li><b>メニューの中にしかない操作を作らない</b><span>保存や送信など、その画面の主な操作は本文の中に置きます。</span></li></ul>')
  + sec('サイドバーのリンク', '<p>今いるページのリンクには <code>aria-current="page"</code> を付けます。背景が <code>--accent-soft</code> になります。リンクはアイコンと文字を組み合わせ、まとまりが2つ以上あるときは <code>.k-nav-title</code> で名前を付けます。件数は <code>.k-badge</code> で右端に出せます。</p>'
      + '<div class="ex"><div class="ex-demo ex-stack">' + NAV_SRC.replace('\n', '').replace('  <', '<').replace('href="/tasks/"', 'href="#navigation"').replace('href="/calendar/"', 'href="#navigation"').replace('href="/"', 'href="#navigation"') + '</div>' + code('HTML', NAV_SRC) + '</div>')
  + sec('ページが少ないサイト', '<p>ページが5つ以下の小さなサイトでは、サイドバーを置かず、ヘッダーにリンクを並べます(<code>.k-header-nav</code>)。本文は <code>.k-layout-single</code> で1列にします。幅が900px未満になるとヘッダーのリンクは隠れるので、同じリンクを <code>.k-sidebar</code> にも書いておきます。<code>.k-layout</code> の外に置いたサイドバーは、メニューを開いたときだけ表示されます。</p>'
      + code('HTML', '<header class="k-header">\n  <button class="k-menu-btn" type="button" aria-label="メニュー" aria-expanded="false" aria-controls="sidebar">…</button>\n  <a class="k-header-brand" href="/">かさね帳</a>\n  <nav class="k-header-nav" aria-label="メイン">\n    <a href="/" aria-current="page">ホーム</a>\n    <a href="/news/">お知らせ</a>\n    <a href="/about/">このサイトについて</a>\n  </nav>\n</header>\n<div class="k-drawer-scrim" hidden></div>\n<nav class="k-sidebar" id="sidebar" aria-label="メイン">\n  <div class="k-sidebar-head">…</div>\n  <div class="k-nav">\n    <a class="k-nav-link" href="/" aria-current="page">ホーム</a>\n    <a class="k-nav-link" href="/news/">お知らせ</a>\n    <a class="k-nav-link" href="/about/">このサイトについて</a>\n  </div>\n</nav>\n<div class="k-layout k-layout-single">\n  <main class="k-main">…</main>\n</div>'))
  + sec('パンくずリスト', '<p>階層が3段以上あるときに、本文の一番上に置きます。最後の項目は今いるページで、リンクにしません。</p>'
      + '<div class="ex"><div class="ex-demo">' + re.sub(r'href="/[^"]*"', 'href="#navigation"', BREADCRUMB_SRC.replace('\n', '')) + '</div>' + code('HTML', BREADCRUMB_SRC) + '</div>')
  + sec('フッター', '<p>ページの一番下に、サイトについてのリンクを置きます。設定ページのない製品では、色の選択(<code>.k-palette-compact</code>)もここに置きます。押すと、このサイトの色も変わります。</p>'
      + '<div class="ex"><div class="ex-demo ex-frame"><div class="ex-app ex-app-foot">' + FOOTER_DEMO + '</div></div>' + code('HTML', FOOTER_SRC) + '</div>')
  + sec('使い方', dd('<div class="mini-nav"><span class="mini-btn">' + icon('menu') + '</span><span class="mini-brand">かさね帳</span></div>',
                    'メニューは3本線のボタンから、左に出てくるドロワーで開きます。',
                    '<div class="mini-nav"><span class="mini-brand">かさね帳</span><span class="mini-drop"><span>きょう</span><span>やること</span><span>予定</span></span></div>',
                    'ボタンの下に浮かぶドロップダウンのメニューは使いません。影が要るうえ、小さな画面で押しにくくなります。'))
  + sec('JavaScript', '<p><code>kasane.js</code> を読み込むと、メニューの開け閉め、Esc キー、フォーカスの移動、背景のスクロールを止める処理が動きます。自分で書くときも、同じ動きにしてください。</p>'
      + code('HTML', '<script src="' + BASE + '/kasane.js" defer></script>'))
  + sec('CSS', code('CSS', CSS['layout'] + '\n\n' + CSS['nav'])))

TABLE_SRC = '''<div class="k-table-wrap" role="region" aria-label="今月の支出" tabindex="0">
  <table class="k-table">
    <caption>今月の支出</caption>
    <thead>
      <tr><th scope="col">日付</th><th scope="col">内容</th><th scope="col" class="k-num">金額</th></tr>
    </thead>
    <tbody>
      <tr><td>11月3日(月)</td><td>教科書</td><td class="k-num">3,280円</td></tr>
      <tr><td>11月8日(土)</td><td>定期券</td><td class="k-num">12,400円</td></tr>
      <tr><td>11月12日(水)</td><td>文房具</td><td class="k-num">980円</td></tr>
    </tbody>
  </table>
</div>'''

page('table', '行と列で比べたい情報を並べる部品です。罫線は使わず、行を面にして隙間で分けます。',
  sec('表', '<p>見出しの行は小さく、薄い文字にします。本文の行は <code>--surface-2</code> の面にして、行どうしは4pxの隙間で分けます。金額や件数の列には <code>.k-num</code> を付けて、右にそろえます。</p>'
      + '<div class="ex"><div class="ex-demo ex-stack"><div class="k-card">' + TABLE_SRC.replace('\n', '').replace('  ', '') + '</div></div>' + code('HTML', TABLE_SRC) + '</div>')
  + sec('幅が足りないとき', '<p>表全体を <code>.k-table-wrap</code> で包むと、狭い画面では表だけが横にスクロールします。キーボードでもスクロールできるよう、<code>tabindex="0"</code> と <code>role="region"</code>、名前(<code>aria-label</code>)を付けます。列が2つか3つで、スマートフォンでよく見るものなら、表ではなく <a href="#card">リスト</a> にします。</p>')
  + sec('使い方', '<ul class="links">'
        '<li><b>罫線と縞模様を使わない</b><span>行の区切りは、面と隙間だけで作ります。</span></li>'
        '<li><b>見出しには <code>scope</code> を付ける</b><span>読み上げで、どの列の値かが分かります。</span></li>'
        '<li><b>並べ替えや選択を足すときは</b><span>見出しをボタンにして <code>aria-sort</code> を付けます。行の選択はチェックボックスで示し、色だけで示しません。</span></li></ul>')
  + sec('CSS', code('CSS', CSS['table'])))

EMPTY_SRC = '''<div class="k-empty">
  <div class="k-empty-icon">%s</div>
  <h3 class="k-empty-title">まだメモがありません</h3>
  <p class="k-empty-text">授業や実習で気づいたことを書きとめておくと、あとで見返せます。</p>
  <div class="k-empty-actions">
    <button class="k-btn k-btn-primary" type="button">%sメモを書く</button>
  </div>
</div>''' % (icon('inbox'), icon('file-plus'))

SKELETON_SRC = '''<div class="k-card" aria-busy="true">
  <span class="k-visually-hidden">読み込んでいます</span>
  <div class="k-skeleton" aria-hidden="true">
    <span class="k-skeleton-title"></span>
    <span class="k-skeleton-line"></span>
    <span class="k-skeleton-line"></span>
    <span class="k-skeleton-line k-skeleton-short"></span>
  </div>
</div>'''

page('empty', '表示するものがないときと、読み込んでいるあいだの部品です。何もない画面のままにしません。',
  sec('空の状態', '<p>リストや検索結果が空のときは、なぜ空なのかと、次にできることを伝えます。アイコンは内容に合ったものを Lucide から選びます。ボタンは1つにします。</p>'
      + ex(EMPTY_SRC, True))
  + sec('検索で見つからないとき', ex('<div class="k-empty">\n  <div class="k-empty-icon">%s</div>\n  <p class="k-empty-title">「ちょうせい」は見つかりませんでした</p>\n  <p class="k-empty-text">言葉を短くするか、ひらがなで探してみてください。</p>\n</div>' % icon('search'), True))
  + sec('読み込み中', '<p>読み込みに1秒以上かかるときは、内容の形をした灰色の面(スケルトン)を先に出します。光が流れるような繰り返す動きは使いません。読み込みが終わったら、まとめて中身に入れ替えます。</p>'
      + ex(SKELETON_SRC, True)
      + '<ul class="links">'
        '<li><b>1秒未満なら何も出さない</b><span>すぐ終わる読み込みでスケルトンを出すと、かえってちらつきます。</span></li>'
        '<li><b>読み上げにも伝える</b><span>まとまりに <code>aria-busy="true"</code> を付け、「読み込んでいます」を <code>.k-visually-hidden</code> で添えます。</span></li>'
        '<li><b>大きさを中身と同じにする</b><span>入れ替わったときに画面がずれないようにします。</span></li></ul>')
  + sec('CSS', code('CSS', CSS['empty'])))

page('migrate', 'v1 は今のURLのまま残しています。v2 に移るときに変えるところをまとめました。',
  sec('v1 はそのまま使えます', '<p><code>/v1/</code> のファイル(<code>kasane.css</code>、<code>kasane.md</code>、書体、<code>kasane-lint</code>)は、出したときのまま残しています。今 v1 を読み込んでいるページは、何もしなくても見た目が変わりません。</p>')
  + sec('URLを変える', '<p><code>v1</code> を <code>v2</code> に変えます。書体は v1 と v2 で同じファイルを使うので、そのままです。</p>'
      + code('HTML', '<link rel="stylesheet" href="' + ORIGIN + '/v1/fonts/line-seed-jp.css">\n<link rel="stylesheet" href="' + BASE + '/kasane.min.css">\n<script src="' + BASE + '/kasane.js" defer></script>'))
  + sec('変わったこと', table(['', 'v1', 'v2'], [
        ['既定のパレット', '<code>yamabuki</code>(山吹)', '<code>hidamari</code>(ひだまり)。<code>yamabuki</code> と書いても、ひだまりとして表示します'],
        ['画面の骨組み', 'なし(各自で作る)', '<code>.k-header</code> <code>.k-menu-btn</code> <code>.k-sidebar</code> <code>.k-nav</code> <code>.k-footer</code> など'],
        ['表、空の状態、読み込み中', 'なし', '<code>.k-table</code> <code>.k-empty</code> <code>.k-skeleton</code>'],
        ['パンくずリスト', 'なし', '<code>.k-breadcrumb</code>'],
        ['JavaScript', 'なし', '<code>kasane.js</code>(メニュー、ダイアログ、タブ、色の保存)'],
        ['色を変えたとき', 'すぐに切り替わる', '上から下へ、塗り替えるように切り替わる'],
        ['自動チェック', '<code>kasane-lint</code> 1.2', '<code>kasane-lint</code> 2.0(メニューのボタンを確かめるルールを追加)']]))
  + sec('保存した色', '<p>利用者が v1 で山吹を選んで保存していた場合、<code>localStorage</code> には <code>yamabuki</code> が残っています。v2 の CSS はこの名前もひだまりとして表示し、<code>kasane.js</code> は読み込んだときに <code>hidamari</code> へ書き換えます。<code>kasane.js</code> を使わない場合は、<code>&lt;head&gt;</code> のスクリプトで書き換えます。</p>'
      + code('HTML', '<script>\n  try {\n    var a = localStorage.getItem("kasane-accent");\n    if (a === "yamabuki") { a = "hidamari"; localStorage.setItem("kasane-accent", a); }\n    if (a) document.documentElement.dataset.accent = a;\n  } catch (e) {}\n</script>'))
  + sec('AI に頼むとき', '<p>AI に移行を頼むときは、次のように伝えます。</p>'
      + code('テキスト', 'Kasane を v1 から v2 に更新してください。\n仕様書: ' + BASE + '/kasane.md\n- 読み込むURLの v1 を v2 にする(書体の /v1/fonts/ はそのまま)\n- data-accent の yamabuki を hidamari にする\n- 自作のヘッダー、メニュー、表、空の状態があれば、v2 の部品に置き換える\n- 最後に kasane-lint 2.0 で確かめる')))
