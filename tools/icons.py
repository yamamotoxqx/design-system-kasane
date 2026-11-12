#!/usr/bin/env python3
"""Make the site icons and the share image (npm run icons).

Writes into site/: favicon.svg, favicon.ico (16/32/48), apple-touch-icon.png (180),
icon-192.png, icon-512.png and og.png (1200x630). Not part of `npm run build`:
run it again only when the logo or the default palette changes.
Needs Python Playwright (with Chromium) and Pillow.
"""
import json, os, io
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, 'site')
NM = os.path.join(ROOT, 'node_modules')
PAL = json.load(open(os.path.join(HERE, '.out', 'palettes.json'), encoding='utf-8'))
P0 = PAL[0]                      # default palette (yamabuki)
L, D = P0['light'], P0['dark']
CHROME = os.environ.get('CHROME_PATH')

# The logo: a quiet square under an accent square, as in the site header.
def logo(back, front):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">'
            '<rect x="2" y="8" width="18" height="18" rx="6" fill="%s"/><rect x="8" y="2" width="18" height="18" rx="6" fill="%s"/></svg>' % (back, front))

FAVICON_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">'
               '<style>.b{fill:%s}.f{fill:%s}@media (prefers-color-scheme:dark){.b{fill:%s}.f{fill:%s}}</style>'
               '<rect class="b" x="2" y="8" width="18" height="18" rx="6"/><rect class="f" x="8" y="2" width="18" height="18" rx="6"/></svg>\n'
               % (L['--surface-3'], L['--accent'], D['--surface-3'], D['--accent']))

def font(path):
    return 'file://' + os.path.join(NM, path)

OG = '''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:T;font-weight:900;src:url(%(title)s) format("woff2")}
@font-face{font-family:B;font-weight:700;src:url(%(body)s) format("woff2")}
html,body{margin:0}
body{width:1200px;height:630px;background:%(bg)s;color:%(ink)s;font-family:B;box-sizing:border-box;position:relative;overflow:hidden}
.text{position:absolute;left:88px;top:150px;display:flex;flex-direction:column;gap:26px}
h1{font-family:T;font-weight:900;font-size:132px;line-height:1;margin:0}
p{font-size:34px;margin:0}
.sw{display:flex;gap:12px;margin-top:14px}
.sw i{width:40px;height:40px;border-radius:50%%;display:block}
.url{position:absolute;left:88px;bottom:56px;font-size:26px;color:%(muted)s}
.art{position:absolute;right:56px;top:115px;width:400px;height:400px}
</style></head><body>
<div class="text"><h1>Kasane</h1><p>面を重ねて区切り、<br>色を選べるデザインシステム</p><div class="sw">%(sw)s</div></div>
<div class="url">kasane.y-n0.de</div>
<div class="art">%(logo)s</div>
</body></html>'''

def main():
    os.makedirs(SITE, exist_ok=True)
    open(os.path.join(SITE, 'favicon.svg'), 'w', encoding='utf-8').write(FAVICON_SVG)
    with sync_playwright() as pw:
        b = pw.chromium.launch(**({'executable_path': CHROME} if CHROME else {}))
        pg = b.new_page()

        def shot(html_doc, w, h, transparent=False):
            pg.set_viewport_size({'width': w, 'height': h})
            tmp = os.path.join(HERE, '.out', '_icon.html')
            open(tmp, 'w', encoding='utf-8').write(html_doc)
            pg.goto('file://' + tmp)
            pg.evaluate("Promise.all([document.fonts.load('900 40px T'),document.fonts.load('700 20px B')]).then(()=>document.fonts.ready)")
            pg.wait_for_timeout(300)
            return Image.open(io.BytesIO(pg.screenshot(omit_background=transparent))).convert('RGBA')

        def square(size, pad, bg=None):
            body = 'margin:0;width:%dpx;height:%dpx;display:grid;place-items:center;%s' % (size, size, 'background:%s' % bg if bg else 'background:transparent')
            svg = logo(L['--surface-3'], L['--accent']).replace('<svg ', '<svg width="%d" height="%d" ' % (size - 2 * pad, size - 2 * pad))
            return shot('<html><body style="%s">%s</body></html>' % (body, svg), size, size, transparent=bg is None)

        # Browser tabs: transparent; home screens and app icons: on the page colour, with room for masks
        ico = square(48, 0)
        ico.save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
        square(180, 30, L['--bg']).convert('RGB').save(os.path.join(SITE, 'apple-touch-icon.png'), optimize=True)
        square(192, 38, L['--bg']).convert('RGB').save(os.path.join(SITE, 'icon-192.png'), optimize=True)
        square(512, 100, L['--bg']).convert('RGB').save(os.path.join(SITE, 'icon-512.png'), optimize=True)

        sw = ''.join('<i style="background:%s"></i>' % p['light']['--accent'] for p in PAL)
        og = OG % {'title': font('@fontsource/zen-maru-gothic/files/zen-maru-gothic-latin-900-normal.woff2'),
                   'body': font('line-seed-jp/woff2/LINESeedJP_OTF_Bd.woff2'),
                   'bg': L['--bg'], 'ink': L['--ink'], 'muted': L['--muted'], 'surface': L['--surface'], 'accent': L['--accent'],
                   'logo': logo(L['--surface-3'], L['--accent']), 'sw': sw}
        shot(og, 1200, 630).convert('RGB').save(os.path.join(SITE, 'og.png'), optimize=True)
        b.close()
    for f in ('favicon.svg', 'favicon.ico', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png', 'og.png'):
        print('site/%s %d bytes' % (f, os.path.getsize(os.path.join(SITE, f))))

if __name__ == '__main__':
    main()
