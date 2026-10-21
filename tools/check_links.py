#!/usr/bin/env python3
"""Check the internal links of the built site.

    mkdocs build --strict && python tools/check_links.py [site]

Walks every HTML file under the site directory and checks that each internal link (href,
src, srcset, poster), including a #fragment, points at an existing file and, for a
fragment, at an element with that id. Absolute links under the site's own path (the 404
page uses them, from site_url) are resolved against the site root. External links (http,
https, mailto, ...) are not fetched unless --external is given: then every distinct
http(s) URL is requested once (HEAD, then GET), with a browser-like User-Agent and a
timeout; 404s, 5xx and connection failures are broken, while 403 / 429 answers (sites that
refuse robots) are listed as warnings only. Exit status 1 when anything is broken, so it
can run in CI after the build; the weekly workflow runs the external check.
"""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/124.0 Safari/537.36 dv-interview-questions-link-check")
BLOCKED = {401, 403, 429, 999}      # answers that mean "no robots", not "gone"

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


def fetch(url: str, timeout: float = 20.0) -> tuple[str, int | None, str]:
    """(url, status or None, note) after a HEAD request, retried as GET when HEAD is refused."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as res:
                return url, res.status, ""
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 404, 405, 429, 500, 501):
                continue
            return url, e.code, e.reason if isinstance(e.reason, str) else ""
        except Exception as e:   # DNS, TLS, timeout, reset
            if method == "HEAD":
                continue
            return url, None, type(e).__name__ + (f": {e}" if str(e) else "")
    return url, None, "no answer"


def check_external(pages: dict[Path, "Collector"], site: Path, workers: int = 8) -> int:
    """Request every distinct external URL once; print the broken ones and the blocked ones."""
    where: dict[str, str] = {}
    for page, c in pages.items():
        for url, line in c.links:
            if url.lower().startswith(("http:", "https:")) or url.startswith("//"):
                full = "https:" + url if url.startswith("//") else url
                where.setdefault(full.split("#")[0], f"{page.relative_to(site)}:{line}")
    broken, blocked = [], []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for url, status, note in pool.map(fetch, sorted(where)):
            if status is not None and status < 400:
                continue
            line = f"{where[url]}: {status or 'error'} {note} {url}".replace("  ", " ")
            (blocked if status in BLOCKED else broken).append(line)
    for b in broken:
        print(b)
    for b in blocked:
        print(f"warn blocked: {b}")
    print(f"{len(where)} external links checked, {len(broken)} broken, {len(blocked)} refused the robot")
    return len(broken)


def site_prefix(site: Path) -> str:
    """The path of site_url ("/DV-Interview-Questions/"), from the canonical link of the home page."""
    index = site / "index.html"
    if index.exists():
        m = re.search(r'<link rel="canonical" href="([^"]+)"', index.read_text(encoding="utf-8", errors="replace"))
        if m:
            path = urlsplit(m.group(1)).path
            return path if path.endswith("/") else path + "/"
    return "/"


def main(argv: list[str]) -> int:
    external = "--external" in argv
    argv = [a for a in argv if a != "--external"]
    site = Path(argv[0] if argv else "site").resolve()
    if not site.is_dir():
        print(f"site directory not found: {site}")
        return 1
    prefix = site_prefix(site)

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
        if prefix != "/" and path.startswith(prefix):
            path = "/" + path[len(prefix):]
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
    bad = len(broken)
    if external:
        bad += check_external(pages, site)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
