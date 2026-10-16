#!/usr/bin/env python3
"""Check the internal links of the built site.

    mkdocs build --strict && python tools/check_links.py [site]

Walks every HTML file under the site directory and checks that each internal link (href,
src, srcset, poster), including a #fragment, points at an existing file and, for a
fragment, at an element with that id. External links (http, https, mailto, ...) are not
fetched. Exit status 1 when anything is broken, so it can run in CI after the build.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ATTRS = {"href", "src", "poster", "data", "xlink:href"}
SKIP_SCHEMES = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:")


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, int]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is None:
                continue
            if name in ("id", "name") and tag != "meta":
                self.ids.add(value)
            elif name in ATTRS and tag != "base":
                self.links.append((value, self.getpos()[0]))
            elif name == "srcset":
                for part in value.split(","):
                    url = part.strip().split(" ")[0]
                    if url:
                        self.links.append((url, self.getpos()[0]))


def main(argv: list[str]) -> int:
    site = Path(argv[0] if argv else "site").resolve()
    if not site.is_dir():
        print(f"site directory not found: {site}")
        return 1

    pages: dict[Path, Collector] = {}
    for html in sorted(site.rglob("*.html")):
        c = Collector()
        c.feed(html.read_text(encoding="utf-8", errors="replace"))
        pages[html] = c

    def resolve(page: Path, url: str) -> Path | None:
        """The file an internal URL points at, or None for an external URL."""
        if url.lower().startswith(SKIP_SCHEMES) or url.startswith("//"):
            return None
        path = unquote(urlsplit(url).path)
        if not path:
            return page
        target = (site / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
        target = target.resolve()
        if target.is_dir():
            target = target / "index.html"
        return target

    broken: list[str] = []
    checked = 0
    for page, c in pages.items():
        rel = page.relative_to(site)
        for url, line in c.links:
            if url.startswith("#"):
                frag = unquote(url[1:])
                if frag and frag not in c.ids:
                    broken.append(f"{rel}:{line}: missing anchor #{frag}")
                checked += 1
                continue
            target = resolve(page, url)
            if target is None:
                continue
            checked += 1
            if not target.exists():
                broken.append(f"{rel}:{line}: missing file {url}")
                continue
            frag = unquote(urlsplit(url).fragment)
            if frag and target.suffix == ".html":
                ids = pages[target].ids if target in pages else set()
                if frag not in ids:
                    broken.append(f"{rel}:{line}: missing anchor {url}")

    for b in broken:
        print(b)
    print(f"{len(pages)} pages, {checked} internal links checked, {len(broken)} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
