#!/usr/bin/env python3
"""Check generated HTML links, assets and internal heading anchors offline."""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id'):
            self.ids.add(data['id'])
        for key in ('href', 'src'):
            if data.get(key):
                self.links.append(data[key])


def check(root):
    root = Path(root).resolve()
    pages = {}
    for file in root.rglob('*.html'):
        parsed = Page()
        parsed.feed(file.read_text(encoding='utf-8'))
        pages[file] = parsed
    errors = []
    count = 0
    for file, page in pages.items():
        for link in page.links:
            parts = urlsplit(link)
            if parts.scheme or link.startswith('//'):
                continue
            count += 1
            raw = unquote(parts.path)
            target = (root / raw.lstrip('/')) if raw.startswith('/') else (file.parent / raw)
            if not raw:
                target = file
            if target.is_dir() or raw.endswith('/'):
                target = target / 'index.html'
            target = target.resolve()
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f'{file.relative_to(root)}: missing {link}')
            elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
                errors.append(f'{file.relative_to(root)}: missing anchor {link}')
    if not pages:
        errors.append('No generated HTML pages')
    if errors:
        raise ValueError('\n'.join(errors))
    print(f'Checked {len(pages)} HTML pages and {count} internal links/assets.')


if __name__ == '__main__':
    try:
        check(sys.argv[1] if len(sys.argv) > 1 else 'public')
    except ValueError as exc:
        sys.exit(str(exc))
