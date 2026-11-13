"""Translate the rendered Japanese docs pages into another language.

The pages are written once, in Japanese (build_site.py, pages_extra.py). For the
English site, the build renders each page and swaps every piece of Japanese text
for its entry in tools/i18n/<lang>.json:

- a "unit" is a run of text and inline tags (<a>, <code>, <b>, …) inside one
  block, keyed by its HTML with whitespace collapsed. The translation is HTML too,
  so links and code stay where the sentence needs them.
- inside <pre>, each line with Japanese is a unit (code comments, sample text).
- attributes such as aria-label, alt, title, placeholder and meta content.

Elements with data-i18n-skip are left as they are. Missing entries are reported,
so the English site never silently shows Japanese.
"""
import re
from bs4 import BeautifulSoup, NavigableString, Tag, Comment

JP = re.compile(r'[぀-ヿ㐀-鿿！-｠]')
INLINE = {'a', 'code', 'b', 'strong', 'em', 'kbd', 'br', 'time', 'q', 'abbr', 'mark', 'sub', 'sup', 'u', 's'}
SKIP = {'script', 'style', 'svg', 'noscript'}
ATTRS = ('aria-label', 'alt', 'title', 'placeholder', 'content', 'data-label', 'aria-roledescription', 'value')


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def _is_inline_run_member(node):
    """Text, or an inline element whose whole subtree is inline."""
    if isinstance(node, Comment):
        return False
    if isinstance(node, NavigableString):
        return True
    if not isinstance(node, Tag) or node.has_attr('data-i18n-skip'):
        return False
    # a plain <span>, a number (<span class="k-num">) or a word in another language (<span lang>) inside a sentence is part of it
    plain_span = node.name == 'span' and (not node.attrs or node.get('class') == ['k-num'] or list(node.attrs) == ['lang'])
    if node.name not in INLINE and not plain_span:
        return False
    return all(_is_inline_run_member(c) for c in node.children)


class Translator:
    def __init__(self, table):
        self.table = table
        self.missing = {}

    def lookup(self, key):
        if key in self.table and self.table[key] is not None:
            return self.table[key]
        self.missing[key] = None
        return None

    # -- runs of text + inline tags
    def _runs(self, el):
        for run in self._raw_runs(el):
            solid = [n for n in run if not (isinstance(n, NavigableString) and not n.strip())]
            # a run that is one element (a link, a bold label): key it by its content, not its markup
            if len(solid) == 1 and isinstance(solid[0], Tag) and solid[0].name not in ('br', 'code'):
                yield from self._runs(solid[0])
            else:
                yield run

    def _raw_runs(self, el):
        run = []
        for c in list(el.children):
            if _is_inline_run_member(c):
                # two inline elements side by side (links in a menu, buttons in a row) are separate texts
                if isinstance(c, Tag) and run:
                    prev = [n for n in run if not (isinstance(n, NavigableString) and not n.strip())]
                    if prev and isinstance(prev[-1], Tag):
                        yield run
                        run = []
                run.append(c)
                continue
            if run:
                yield run
            run = []
            if isinstance(c, Tag) and c.name not in SKIP and not c.has_attr('data-i18n-skip'):
                if c.name == 'pre':
                    self._pre(c)
                else:
                    yield from self._runs(c)
        if run:
            yield run

    def _pre(self, pre):
        for s in list(pre.find_all(string=True)):
            if not JP.search(s):
                continue
            out = []
            for line in s.split('\n'):
                if JP.search(line):
                    lead = line[:len(line) - len(line.lstrip())]
                    t = self.lookup(line.strip())
                    out.append(lead + t if t is not None else line)
                else:
                    out.append(line)
            s.replace_with(NavigableString('\n'.join(out)))

    def _apply_run(self, run):
        src = ''.join(str(n) for n in run)
        if not JP.search(src):
            return
        key = norm(src)
        t = self.lookup(key)
        if t is None:
            return
        lead = src[:len(src) - len(src.lstrip())]
        tail = src[len(src.rstrip()):]
        frag = BeautifulSoup(lead + t + tail, 'html.parser')
        first = run[0]
        for n in list(frag.contents):
            first.insert_before(n)
        for n in run:
            n.extract()

    def translate(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        for el in soup.find_all(True):
            if el.has_attr('data-i18n-skip') or el.find_parent(attrs={'data-i18n-skip': True}):
                continue
            for a in ATTRS:
                v = el.get(a)
                if isinstance(v, str) and JP.search(v):
                    t = self.lookup(norm(v))
                    if t is not None:
                        el[a] = t
        root = soup.html or soup
        for run in list(self._runs(root)):
            self._apply_run(run)
        return str(soup)
