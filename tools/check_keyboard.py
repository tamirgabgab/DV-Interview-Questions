#!/usr/bin/env python3
"""A keyboard pass over the built site (S425): the tab order and the keys of the components.

    mkdocs build --strict && python tools/check_keyboard.py [site] [--only REGEX]

Serves the site locally and, on a few pages (the home page, the all-questions table, the
tags page, a study path and one question page with a box, a figure, a self-check and the
run panel), walks the whole page with Tab at 1200 px. Every stop must be visible, every
interactive stop must have a name (aria-label, a label, its text, a title) and must show a
focus ring (an outline or a shadow while :focus-visible), the first stop must be the skip
link, and the walk must end (no trap); the theme's own header, drawer, search and footer are
walked but not judged (axe covers them in the phone check). On the question page it then presses the keys of the
components: Enter opens a hint and toggles a fold of a box, the arrow keys step a focused
box, Enter on the enlarge button opens the lightbox and Escape closes it and gives the
focus back, a wrong self-check answer entered with Enter gets a message, Enter on "▶ להרצה"
opens the run panel, and "/" opens the search, typing finds a question and Escape closes
it. A failure in any of these fails the check. --offline, --route, --browser and --local-cdn
are the phone check's.
"""

from __future__ import annotations

import argparse
import functools
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_phone import local_cdn_routes, serve  # noqa: E402

WIDTH, HEIGHT = 1200, 900
MAX_STOPS = 900
DEFAULT_PAGES = r"^index\.html$|^all/|^tags/|^paths/coding/|0061-longest-ones"
QUESTION = r"0061-longest-ones"

# the focused element: where it is, whether it can be seen, its name, and its focus ring
DESCRIBE = """() => {
  const el = document.activeElement;
  if (!el || el === document.body || el === document.documentElement) return null;
  const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
  const clean = (s) => (s || "").replace(/\\s+/g, " ").trim();
  const visible = r.width > 0 && r.height > 0 && cs.visibility !== "hidden" && cs.display !== "none";
  let name = clean(el.getAttribute("aria-label"));
  const by = el.getAttribute("aria-labelledby");
  if (!name && by) name = clean(by.split(/\\s+/).map((id) => (document.getElementById(id) || {}).textContent || "").join(" "));
  if (!name && el.id) { const l = document.querySelector(`label[for="${CSS.escape(el.id)}"]`); if (l) name = clean(l.textContent); }
  if (!name && el.closest("label")) name = clean(el.closest("label").textContent);
  if (!name) name = clean(el.textContent) || clean(el.getAttribute("title")) || clean(el.getAttribute("placeholder")) || clean(el.getAttribute("alt"));
  if (!name) { const t = el.querySelector("img[alt], svg title"); if (t) name = clean(t.alt || t.textContent); }
  const ring = (cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) > 0) || cs.boxShadow !== "none";
  const cls = typeof el.className === "string" ? el.className.trim().split(/\\s+/).slice(0, 2).join(".") : "";
  window.__kbStops = window.__kbStops || new Map();
  if (!window.__kbStops.has(el)) window.__kbStops.set(el, window.__kbStops.size + 1);
  return { id: window.__kbStops.get(el), path: el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") + (cls ? "." + cls : ""), visible, name: name.slice(0, 40),
           focusVisible: el.matches(":focus-visible"), ring, theme: !!el.closest(".md-header, .md-search, .md-sidebar, .md-footer"),
           interactive: el.matches("a[href], button, input, select, textarea, summary, [role=button], [role=link]") };
}"""


def walk(page) -> tuple[int, list[str]]:
    """Tab through the page; the number of stops and the problems found."""
    problems: list[str] = []
    seen: set[int] = set()
    first = None
    stops = 0
    page.evaluate("() => { window.__kbStops = new Map(); document.activeElement && document.activeElement.blur(); window.scrollTo(0, 0); }")
    for _ in range(MAX_STOPS):
        page.keyboard.press("Tab")
        d = page.evaluate(DESCRIBE)
        if d is None:
            break                                   # back to the document: the walk is over
        if first is None:
            first = d
        elif d["id"] == first["id"]:
            break                                   # around the page once
        elif d["id"] in seen:
            problems.append(f"the focus comes back to {d['path']} \"{d['name']}\" before the walk is over (a trap?)")
            break
        stops += 1
        seen.add(d["id"])
        if d["theme"]:
            continue                                # the theme's own header, drawer and search (axe checks them)
        if not d["visible"]:
            problems.append(f"an invisible stop: {d['path']}")
        if d["interactive"] and not d["name"]:
            problems.append(f"no name: {d['path']}")
        if d["focusVisible"] and not d["ring"]:
            problems.append(f"no focus ring: {d['path']} \"{d['name']}\"")
    else:
        problems.append(f"the walk did not end in {MAX_STOPS} stops")
    if first is None:
        problems.append("nothing takes the focus")
    elif "md-skip" not in first["path"]:
        problems.append(f"the first stop is not the skip link: {first['path']}")
    return stops, list(dict.fromkeys(problems))


def press_keys(page) -> list[str]:
    """The keys of the components on a question page."""
    out: list[str] = []
    page.evaluate("async () => { if (window.dvqExplorers) await window.dvqExplorers.ready(); }")
    # a hint opens with Enter on its summary
    s = page.locator("details.tip > summary").first
    if s.count():
        s.focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(150)
        if not page.evaluate("() => document.querySelector('details.tip').open"):
            out.append("Enter on a hint's summary does not open it")
    # every solution open, for the components inside
    page.evaluate("() => document.querySelectorAll('details').forEach((d) => (d.open = true))")
    page.wait_for_timeout(300)
    # a box steps with the arrow keys
    box = page.locator(".explorer").first
    if box.count():
        box.scroll_into_view_if_needed()
        page.evaluate("async () => { if (window.dvqExplorers) await window.dvqExplorers.ready(); }")
        box.focus()
        before = box.locator(".ex-pos").first.text_content() if box.locator(".ex-pos").count() else ""
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(150)
        after = box.locator(".ex-pos").first.text_content() if box.locator(".ex-pos").count() else ""
        if before and before == after:
            out.append(f"the arrow key did not step the box ({before!r})")
        fold = box.locator(".ex-fold-btn").first
        if fold.count():
            fold.scroll_into_view_if_needed()
            was = fold.get_attribute("aria-expanded")
            fold.focus()
            page.keyboard.press("Enter")
            page.wait_for_timeout(150)
            if fold.get_attribute("aria-expanded") == was:
                out.append("Enter on a fold's button does not toggle it")
    # the enlarge button opens the lightbox; Escape closes it and gives the focus back
    btn = page.locator(".fig-enlarge").first
    if btn.count():
        btn.scroll_into_view_if_needed()
        btn.focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        if not page.locator(".fig-lightbox.is-open").count():
            out.append("Enter on the enlarge button does not open the lightbox")
        else:
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            if page.locator(".fig-lightbox.is-open").count():
                out.append("Escape does not close the lightbox")
            elif not page.evaluate("() => document.activeElement && document.activeElement.classList.contains('fig-enlarge')"):
                out.append("the focus does not come back to the enlarge button after the lightbox")
    # a self-check answers Enter
    field = page.locator(".selfcheck input").first
    if field.count():
        field.scroll_into_view_if_needed()
        field.focus()
        page.keyboard.type("987654")
        page.keyboard.press("Enter")
        page.wait_for_timeout(200)
        if not (page.locator(".selfcheck__msg").first.text_content() or "").strip():
            out.append("Enter in a self-check field gives no message")
    # the run panel opens from the code's button
    run = page.locator(".py-from-code").first
    if run.count():
        run.scroll_into_view_if_needed()
        run.focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(600)
        if not page.locator("details.py-runner[open]").count():
            out.append("Enter on the run button does not open the run panel")
    # the search: "/" opens it, typing finds a question, Escape closes it
    page.evaluate("() => { document.activeElement && document.activeElement.blur(); window.scrollTo(0, 0); }")
    page.keyboard.press("/")
    page.wait_for_timeout(200)
    if not page.evaluate("() => document.activeElement && document.activeElement.classList.contains('md-search__input')"):
        out.append("\"/\" does not focus the search")
    else:
        page.keyboard.type("0046")
        try:
            page.wait_for_selector(".md-search-result__item", timeout=10_000)
        except Exception:
            out.append("typing in the search finds nothing")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        if page.evaluate("() => document.activeElement && document.activeElement.classList.contains('md-search__input')"):
            out.append("Escape does not leave the search")
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("site", nargs="?", default="site")
    ap.add_argument("--only", default=DEFAULT_PAGES, help="check the pages whose path matches this regex")
    ap.add_argument("--browser", help="path to a Chromium executable")
    ap.add_argument("--offline", action="store_true", help="ignore errors of external scripts")
    ap.add_argument("--route", action="append", default=[], metavar="REGEX=FILE", help="serve requests matching REGEX from a local file")
    ap.add_argument("--local-cdn", action="store_true", help="--offline with the CDN copies of .cache/cdn (tools/dev_setup.sh)")
    args = ap.parse_args(argv)
    if args.local_cdn:
        args.offline = True
        args.route += local_cdn_routes()

    from playwright.sync_api import sync_playwright

    site = Path(args.site).resolve()
    if not site.is_dir():
        print(f"site directory not found: {site}")
        return 1
    pages = sorted(p.relative_to(site).as_posix() for p in site.rglob("index.html") if re.search(args.only, p.relative_to(site).as_posix()))
    server, base = serve(site)
    failures = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser) if args.browser else pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1, service_workers="block")
        for spec in args.route:
            pattern, file = spec.split("=", 1)
            ctx.route(re.compile(pattern), functools.partial(lambda file, route: route.fulfill(path=file), file))
        for rel in pages:
            page = ctx.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda e, errors=errors: errors.append(str(e)))
            try:
                page.goto(base + rel[: -len("index.html")], wait_until="networkidle", timeout=60_000)
            except Exception as e:
                errors.append(f"load: {e}")
            stops, problems = walk(page)
            keys = press_keys(page) if re.search(QUESTION, rel) else []
            if args.offline:
                errors = [e for e in errors if not re.search(r"https?://(?!127\.0\.0\.1)", e)]
            problems += keys + [f"script error: {e[:160]}" for e in errors]
            failures += bool(problems)
            print(f"{'FAIL' if problems else 'ok':4}  {rel[: -len('index.html')] or '/'}  {stops} tab stops{', the keys pressed' if keys == [] and re.search(QUESTION, rel) else ''}")
            for p in problems:
                print(f"        {p}")
            page.close()
        browser.close()
    server.shutdown()
    print(f"{len(pages)} pages walked with the keyboard at {WIDTH} px, {failures} with problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
