# Rebuild v1/fonts/: LINE Seed JP (400 / 700 / 800) cut into a small number of unicode-range groups.
#
# Fontsource ships ~120 frequency-ordered slices per weight (372 @font-face rules in all). Parsing and
# matching that many faces costs a lot of main-thread time on phones, so this merges neighbouring slices
# into 18 groups per weight (54 faces). Frequent characters stay in small groups; rare ones share one group.
#
# Needs: npm install (line-seed-jp, @fontsource/line-seed-jp) and fonttools with brotli (pyftsubset).
# Run: npm run fonts
import os, re, shutil, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
NM = os.path.join(ROOT, 'node_modules')
SRC = {400: 'Rg', 700: 'Bd', 800: 'Eb'}
OUT = os.path.join(ROOT, 'v1', 'fonts')
# Groups of fontsource slice numbers (0 = rarest, 119 = most common) plus the named Latin-type slices.
GROUPS = ([('rare', range(0, 60))]
          + [('g%d' % a, range(a, a + 5)) for a in range(60, 95, 5)]
          + [('g%d' % a, range(a, b)) for a, b in ((95, 98), (98, 101), (101, 104), (104, 107), (107, 110), (110, 113), (113, 116), (116, 118), (118, 120))]
          + [('latin', ['latin', 'latin-ext', 'greek-ext', 'cyrillic'])])

def slices(weight):
    css = open(os.path.join(NM, '@fontsource', 'line-seed-jp', '%d.css' % weight), encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'/\* line-seed-jp-(?:\[(\d+)\]|([a-z-]+))-%d-normal \*/.*?unicode-range: ([^;]+);' % weight, css, re.S):
        out[m.group(1) or m.group(2)] = [r.strip() for r in m.group(3).split(',')]
    return out

def to_cps(ranges):
    cps = set()
    for r in ranges:
        r = r[2:]
        if '-' in r:
            a, b = r.split('-'); cps.update(range(int(a, 16), int(b, 16) + 1))
        else:
            cps.add(int(r, 16))
    return cps

def to_ranges(cps):
    cps = sorted(cps); out = []; i = 0
    while i < len(cps):
        j = i
        while j + 1 < len(cps) and cps[j + 1] == cps[j] + 1: j += 1
        out.append('U+%x' % cps[i] if i == j else 'U+%x-%x' % (cps[i], cps[j])); i = j + 1
    return ','.join(out)

def main():
    files = os.path.join(OUT, 'files')
    shutil.rmtree(files, ignore_errors=True); os.makedirs(files)
    faces = []
    with tempfile.TemporaryDirectory() as tmp:
        for weight, src in SRC.items():
            sl = slices(weight)
            for name, keys in GROUPS:
                cps = set()
                for k in keys:
                    cps |= to_cps(sl.get(str(k), []))
                if not cps: continue
                ulist = os.path.join(tmp, 'u.txt')
                open(ulist, 'w').write(','.join('%x' % c for c in sorted(cps)))
                fn = 'line-seed-jp-%d-%s.woff2' % (weight, name)
                subprocess.run(['pyftsubset', os.path.join(NM, 'line-seed-jp', 'woff2', 'LINESeedJP_OTF_%s.woff2' % src),
                                '--unicodes-file=' + ulist, '--flavor=woff2', '--no-hinting', '--desubroutinize',
                                '--output-file=' + os.path.join(files, fn)], check=True, capture_output=True)
                faces.append("@font-face{font-family:'LINE Seed JP';font-style:normal;font-display:swap;font-weight:%d;"
                             "src:url(./files/%s) format('woff2');unicode-range:%s}" % (weight, fn, to_ranges(cps)))
    head = ('/* LINE Seed JP (400 / 700 / 800), cut into %d unicode-range groups so browsers download only the groups a page uses.\n'
            '   Built by tools/fonts.py from line-seed-jp (and the slice order of @fontsource/line-seed-jp).\n'
            '   License: SIL Open Font License 1.1 (LICENSE-LINE-Seed-JP.txt). */\n' % len(faces))
    open(os.path.join(OUT, 'line-seed-jp.css'), 'w', encoding='utf-8').write(head + '\n'.join(faces) + '\n')
    total = sum(os.path.getsize(os.path.join(files, f)) for f in os.listdir(files))
    print('%d faces, %d files, %d KB' % (len(faces), len(os.listdir(files)), total // 1024))

if __name__ == '__main__':
    main()
