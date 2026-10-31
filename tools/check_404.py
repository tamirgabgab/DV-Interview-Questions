#!/usr/bin/env python3
"""Check the 404 page of the built site as GitHub Pages serves it (S424).

    mkdocs build --strict && python tools/check_404.py [site]

The page (overrides/404.html) links its styles and scripts by the site's absolute path
(/DV-Interview-Questions/...), so it cannot be opened from a plain local server. This check
serves the site under that path (read from site_url in mkdocs.yml, or --prefix) and answers
every missing address with 404.html and the status 404, as Pages does. It then opens a
missing page, a missing address that holds a question's id, and one that holds a question's
slug, at 390 and at 1200 px, and fails when: the answer is not the custom page, a style or a
script of the page (its own, not the theme's repository facts) did not load, a script threw, the page scrolls sideways, the guess
("אולי חיפשת את שאלה 0046") is missing or points elsewhere, the level links point outside
the site's path, "שאלה אקראית" does not open a question, or "חיפוש באתר" does not focus the
search; and an old address of a renumbered question (dvq_renumbered in mkdocs.yml) must
go to its new page. --axe PATH (or --local-cdn) runs axe-core on the page as check_phone.py does;
--offline, --route and --browser are the phone check's.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import re
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_phone import AXE, CDN_DIR, INSPECT, local_cdn_routes  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WIDTHS = (390, 1200)
HEIGHT = 844
GUESS_ID = "0046"


def site_prefix() -> str:
    """The path of site_url in mkdocs.yml, with its slashes ("/DV-Interview-Questions/")."""
    m = re.search(r"^site_url:\s*(\S+)", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"), re.M)
    path = re.sub(r"^https?://[^/]+", "", m.group(1)) if m else "/"
    return "/" + path.strip("/") + "/" if path.strip("/") else "/"


class PagesHandler(http.server.SimpleHTTPRequestHandler):
    """The site under its prefix; every other address gets 404.html with the status 404."""
    prefix = "/"
    site = Path("site")

    def log_message(self, *args):
        pass

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        rel = path[len(self.prefix):] if path.startswith(self.prefix) else None
        target = self.site / rel if rel is not None else None
        if target is not None and target.is_dir():
            target = target / "index.html"
        if target is None or not target.is_file() or ".." in rel:
            body = (self.site / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.path = "/" + rel
        super().do_GET()


def serve_under(site: Path, prefix: str):
    handler = functools.partial(PagesHandler, directory=str(site))
    PagesHandler.prefix, PagesHandler.site = prefix, site
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("site", nargs="?", default="site")
    ap.add_argument("--prefix", help="the site's path on its host (default: from site_url in mkdocs.yml)")
    ap.add_argument("--browser", help="path to a Chromium executable")
    ap.add_argument("--offline", action="store_true", help="ignore errors of external scripts")
    ap.add_argument("--route", action="append", default=[], metavar="REGEX=FILE", help="serve requests matching REGEX from a local file")
    ap.add_argument("--axe", metavar="AXE_MIN_JS", help="run axe-core from this file; a serious or critical violation fails")
    ap.add_argument("--local-cdn", action="store_true", help="--offline with the CDN copies of .cache/cdn, axe-core included")
    args = ap.parse_args(argv)
    if args.local_cdn:
        args.offline = True
        args.route += local_cdn_routes()
        if not args.axe and (CDN_DIR / "axe-core" / "axe.min.js").is_file():
            args.axe = str(CDN_DIR / "axe-core" / "axe.min.js")

    from playwright.sync_api import sync_playwright

    site = Path(args.site).resolve()
    if not (site / "404.html").is_file():
        print(f"no 404.html in {site}")
        return 1
    prefix = args.prefix or site_prefix()
    server, origin = serve_under(site, prefix)
    questions = {m.group(1): m.group(2) for m in re.finditer(r'href="[^"]*?(questions/\w+/(\d{4})-[\w-]+/)"', (site / "all" / "index.html").read_text(encoding="utf-8"))}
    questions = {qid: path for path, qid in questions.items()}
    guess_path = questions.get(GUESS_ID)
    if not guess_path:
        print(f"question {GUESS_ID} is not on the all-questions page")
        return 1
    slug = guess_path.split("/")[2][5:]
    m = re.search(r"^  dvq_renumbered:\n((?:    \"\d{4}\": \"\d{4}\"\n)+)", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"), re.M)
    renumbered = dict(re.findall(r'"(\d{4})": "(\d{4})"', m.group(1))) if m else {}
    cases = [("a missing page", f"{prefix}no-such-page/", None),
             ("a missing address with an id", f"{prefix}questions/{GUESS_ID}/", guess_path),
             ("a missing address with a slug", f"{prefix}questions/senior/{slug}/", guess_path)]

    problems = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser) if args.browser else pw.chromium.launch()
        for width in WIDTHS:
            ctx = browser.new_context(viewport={"width": width, "height": HEIGHT}, device_scale_factor=1, service_workers="block")
            for spec in args.route:
                pattern, file = spec.split("=", 1)
                ctx.route(re.compile(pattern), functools.partial(lambda file, route: route.fulfill(path=file), file))
            for name, path, guess in cases:
                page = ctx.new_page()
                errors: list[str] = []
                failed: list[str] = []
                page.on("pageerror", lambda e, errors=errors: errors.append(str(e)))
                # the page's own assets only: the theme's repository facts come from api.github.com,
                # which answers 403 to a runner, and a blocked CDN is --offline's business
                page.on("response", lambda r, failed=failed: failed.append(f"{r.status} {r.url}")
                        if r.status >= 400 and r.request.resource_type != "document" and r.url.startswith(origin) else None)
                page.on("requestfailed", lambda r, failed=failed: failed.append(f"failed {r.url}") if r.url.startswith(origin) else None)
                try:
                    resp = page.goto(origin + path, wait_until="networkidle", timeout=60_000)
                    status = resp.status if resp else 0
                except Exception as e:
                    errors.append(f"load: {e}")
                    status = 0
                if args.offline:
                    errors = [e for e in errors if not re.search(r"https?://(?!127\.0\.0\.1)", e)]
                found: list[str] = []
                if status != 404:
                    found.append(f"status {status}, not 404")
                if not page.locator(".not-found h1").count():
                    found.append("not the custom page")
                info = page.evaluate(INSPECT, width)
                if info["scrollWidth"] > width + 1:
                    found.append(f"{info['scrollWidth']} px wide: " + "; ".join(info["wide"]))
                found += [f"script error: {e[:160]}" for e in errors]
                found += [f"did not load: {f[:160]}" for f in failed]
                guess_el = page.locator(".nf-guess")
                if guess:
                    href = page.evaluate("() => { const a = document.querySelector('.nf-guess a'); return a ? a.getAttribute('href') : null; }")
                    if not guess_el.is_visible() or not href or not href.endswith(guess):
                        found.append(f"the guess is missing or wrong: {href}")
                elif guess_el.is_visible():
                    found.append("a guess where there is nothing to guess")
                levels = page.evaluate("() => [...document.querySelectorAll('.nf-levels a')].map((a) => a.getAttribute('href'))")
                if not levels or any(not h.startswith(prefix + "questions/") for h in levels):
                    found.append(f"level links outside the site's path: {levels}")
                if args.axe:
                    page.add_script_tag(path=args.axe)
                    for v in page.evaluate(AXE):
                        found.append(f"axe {v['impact']} {v['id']} x{v['count']}: {v['help']} ({v['first']})")
                # the two buttons: the search focused, a random question opened
                page.locator(".nf-search").click()
                page.wait_for_timeout(300)
                if not page.evaluate("() => document.activeElement && document.activeElement.classList.contains('md-search__input')"):
                    found.append("the search button did not focus the search")
                page.keyboard.press("Escape")
                page.locator(".nf-random").click()
                try:
                    page.wait_for_url(re.compile(re.escape(origin + prefix) + r"questions/\w+/\d{4}-"), timeout=10_000)
                except Exception:
                    found.append(f"the random question did not open a question: {page.url}")
                problems += bool(found)
                print(f"{'FAIL' if found else 'ok':4}  {name} at {width} px  {path}")
                for f in found:
                    print(f"        {f}")
                page.close()
            # a question moved to a new number (dvq_renumbered in mkdocs.yml): its old address
            # goes straight to the new page, with the anchor
            for old_id, new_id in renumbered.items():
                new_path = questions.get(new_id)
                if not new_path:
                    continue
                level, slug = new_path.split("/")[1], new_path.split("/")[2][5:]
                page = ctx.new_page()
                old = f"{prefix}questions/{level}/{old_id}-{slug}/#x"
                try:
                    page.goto(origin + old, wait_until="networkidle", timeout=60_000)
                    page.wait_for_url(re.compile(re.escape(origin + prefix + new_path) + "#x$"), timeout=10_000)
                    print(f"ok    a renumbered question at {width} px  {old} -> {new_path}")
                except Exception:
                    problems += 1
                    print(f"FAIL  a renumbered question at {width} px  {old}: at {page.url}, not {new_path}")
                page.close()
                break                                # one moved question is enough
            ctx.close()
        browser.close()
    server.shutdown()
    print(f"{len(cases) * len(WIDTHS)} views of the 404 page under {prefix}, {problems} with problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
