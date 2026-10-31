#!/usr/bin/env python3
"""Type into every number and text field of every explorer box and check that it applies.

    mkdocs build --strict && python tools/check_inputs.py [site]

A value typed into a box's field is applied on Enter and when the field is left (core.js,
fields). This check opens every page with an explorer box at 1200 x 900 px, with every
collapsible block open, and for every visible, enabled, writable number or text field of
every box (the scrubber and other range inputs aside) it types a different valid value
the way a reader does: a mouse click into the field, select all, the keys one by one,
then Enter. The box must then differ from what it was before the typing somewhere other
than the field itself (a redraw, another control, a line that says why the value was
refused, or a seed taken); a box where nothing changed fails. The box is reset ("reset
everything") and the same field is tried with another value, left with Tab, and once
more through an input method: a composition ended by Enter, whose keydown is "Process"
and only its keyup Enter (Windows' text suggestions and the IMEs type this way). A try
that changes nothing at the box's first step is tried again at the end of its steps,
where it has an "end" button. A textarea is only tried with Tab (Enter is its new line),
and an editing aid (data-nolink: a guess, the operands or the brush of a button) only
with Enter, and is only a warning when nothing changed.

The value: for a number field, the current value plus or minus its step (1 when it has
none), or its min or max, kept within min and max and on the step; for a text field, the
current text with its last digit changed (0 and 1 swapped in a text of bits), or its parts
(split by commas, spaces or new lines, or its characters) in reverse order.

Needs Playwright, as tools/check_phone.py; --local-cdn, --offline, --route, --only and
--shard work as in tools/check_explorers.py.
"""

from __future__ import annotations

import argparse
import functools
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_explorers import BOXES, open_page, shard  # noqa: E402
from check_phone import local_cdn_routes, serve  # noqa: E402

WIDTH, HEIGHT = 1200, 900

FIELDS = "input[type=number], input[type=text], input:not([type]), textarea"

# Go to the end of box b's steps (its "end" button): a value that changes nothing at the
# first step (a new seed before any test ran) shows at the end, and the other way round.
ADVANCE = """(b) => {
  const box = document.querySelectorAll(".explorer")[b];
  const end = [...box.querySelectorAll("button.ex-end, button.ex-last")].find((el) => !el.disabled && el.getClientRects().length);
  if (end) end.click();
}"""

HAS_END = """(b) => !!document.querySelectorAll(".explorer")[b].querySelector("button.ex-end, button.ex-last")"""

# The fields of box b to try: [index, class, kind] of each visible, enabled, writable one.
LIST = """(b) => {
  const box = document.querySelectorAll(".explorer")[b];
  return [...box.querySelectorAll(%r)].map((el, i) => [i, el.className || el.tagName.toLowerCase(), el.type || "textarea",
    el.hasAttribute("data-nolink"), !el.disabled && !el.readOnly && !!el.getClientRects().length && !el.closest("[hidden], .fig-lightbox")])
    .filter((f) => f[4]).map((f) => f.slice(0, 4));
}""" % FIELDS

# What box b shows, the i-th field aside: its markup without the transient marks (a flash,
# the focus ring class, the reserved heights) and the values of its other controls.
SNAP = """([b, i]) => {
  const box = document.querySelectorAll(".explorer")[b];
  const field = box.querySelectorAll(%r)[i];
  const values = [...box.querySelectorAll("input, select, textarea")].filter((el) => el !== field)
    .map((el) => (el.type === "checkbox" || el.type === "radio" ? String(el.checked) : el.value));
  const copy = box.cloneNode(true);
  const twin = copy.querySelectorAll(%r)[i];
  if (twin) twin.remove();
  copy.querySelectorAll(".ex-guide, [hidden], [aria-hidden=true]").forEach((el) => el.remove());   // hidden text may be stale
  [copy, ...copy.querySelectorAll("*")].forEach((el) => {
    el.classList.remove("ex-changed", "focus-visible", "ex-guide-target");
    if (el.getAttribute("class") === "") el.removeAttribute("class");
    if (el.style) el.style.minHeight = "";
    if (el.getAttribute("style") === "") el.removeAttribute("style");
  });
  const html = copy.innerHTML;
  return JSON.stringify([html, values, box.dvqSeedAt || 0]);     // a seed taken counts (a box may draw nothing yet)
}""" % (FIELDS, FIELDS)

# A new value for the i-th field of box b (the `nth` alternative), scrolled to the middle
# of the screen; returns [value, x, y] of its centre, or null when no value was found.
PICK = """([b, i, nth]) => {
  const box = document.querySelectorAll(".explorer")[b];
  const el = box.querySelectorAll(%r)[i];
  if (!el) return null;
  el.scrollIntoView({ block: "center", behavior: "instant" });
  const cur = el.value;
  let options = [];
  if (el.type === "number") {
    const num = (s) => (s === "" || s == null ? null : Number(s));
    const min = num(el.getAttribute("min")), max = num(el.getAttribute("max"));
    const stepAttr = el.getAttribute("step");
    const step = !stepAttr || stepAttr === "any" ? 1 : Number(stepAttr);
    const base = min !== null ? min : 0;
    const digits = (String(step).split(".")[1] || "").length;
    const v = cur.trim() === "" || !Number.isFinite(Number(cur)) ? (min !== null ? min : 1) : Number(cur);
    const cands = [v + step, v - step, v + 2 * step, v - 2 * step, min, max, (min !== null && max !== null) ? base + Math.round((max - base) / 2 / step) * step : null];
    options = cands.filter((c) => c !== null && Number.isFinite(c))
      .map((c) => Number(c.toFixed(Math.max(digits, 0))))
      .filter((c) => (min === null || c >= min - 1e-9) && (max === null || c <= max + 1e-9))
      .filter((c) => !stepAttr || stepAttr === "any" || Math.abs((c - base) / step - Math.round((c - base) / step)) < 1e-6)
      .filter((c) => Math.abs(c - v) > 1e-9)
      .map((c) => String(c));
  } else {
    const parts = cur.split(/(\\s*[,;\\n]\\s*|\\s+)/);
    const tokens = parts.filter((_, k) => k %% 2 === 0), seps = parts.filter((_, k) => k %% 2 === 1);
    const rev = tokens.length > 1 ? tokens.slice().reverse().map((t, k) => t + (seps[k] || "")).join("") : [...cur].reverse().join("");
    // the last digit changed: 0 and 1 swap in a text of bits, any other digit goes up by one
    const bits = /^[01\\s,;]*$/.test(cur);
    const digit = cur.replace(/(\\d)(\\D*)$/, (_, d, rest) => `${bits ? 1 - Number(d) : (Number(d) + 1) %% 10}${rest}`);
    options = [digit, rev].filter((t) => t && t !== cur);
  }
  options = [...new Set(options)];
  if (!options.length) return null;
  const r = el.getBoundingClientRect();
  return [options[Math.min(nth, options.length - 1)], r.left + Math.min(r.width / 2, 30), r.top + r.height / 2];
}""" % FIELDS

RESET = """(b) => {
  const box = document.querySelectorAll(".explorer")[b];
  const play = box.querySelector(".ex-play");
  if (play && play.textContent.trim() === "עצירה") play.click();
  const btn = box.querySelector(".ex-reset-all");
  if (btn) btn.click();
  box.querySelectorAll(".is-folded > .ex-proof-title .ex-fold-btn, .is-folded > .ex-fold-title .ex-fold-btn").forEach((f) => f.click());
}"""

FOCUSED = """([b, i]) => document.activeElement === document.querySelectorAll(".explorer")[b].querySelectorAll(%r)[i]""" % FIELDS


def type_in(page, cdp, value: str, leave: str) -> None:
    """Type value into the focused field and leave it: "Enter", "Tab", or "ime", an input
    method's composition ended by Enter (the keydown is the input method's "Process", only
    the keyup is Enter: Windows' text suggestions and the IMEs do this)."""
    page.keyboard.press("ControlOrMeta+A")
    if leave != "ime":
        page.keyboard.type(value, delay=15)
        page.wait_for_timeout(80)
        page.keyboard.press(leave)
        return
    for k in range(len(value)):
        cdp.send("Input.dispatchKeyEvent", {"type": "rawKeyDown", "key": "Process", "windowsVirtualKeyCode": 229})
        cdp.send("Input.imeSetComposition", {"text": value[: k + 1], "selectionStart": k + 1, "selectionEnd": k + 1})
        cdp.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": value[k], "windowsVirtualKeyCode": ord(value[k].upper())})
    page.wait_for_timeout(80)
    cdp.send("Input.dispatchKeyEvent", {"type": "rawKeyDown", "key": "Process", "code": "Enter", "windowsVirtualKeyCode": 229})
    cdp.send("Input.insertText", {"text": value})
    cdp.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})


def settled(page, b: int, i: int) -> str:
    """The snapshot of box b once it stopped changing (an "end" that plays to its end, a
    flash), for up to two seconds."""
    snap = page.evaluate(SNAP, [b, i])
    for _ in range(20):
        page.wait_for_timeout(100)
        again = page.evaluate(SNAP, [b, i])
        if again == snap:
            break
        snap = again
    return snap


def try_field(page, cdp, b: int, i: int, nth: int, leave: str, advance: bool = False) -> str | None:
    """Type the nth new value into field i of box b and leave it with `leave`, at the end
    of the box's steps when `advance`. Returns a problem, or None when the box changed."""
    if advance:
        page.evaluate(ADVANCE, b)
        page.wait_for_timeout(50)
    pick = page.evaluate(PICK, [b, i, nth])
    if not pick:
        return None
    value, x, y = pick
    before = settled(page, b, i) if advance else page.evaluate(SNAP, [b, i])
    page.mouse.click(x, y)
    page.wait_for_timeout(80)
    if not page.evaluate(FOCUSED, [b, i]):
        return f"a click does not focus the field (to type {value!r})"
    type_in(page, cdp, value, leave)
    page.wait_for_timeout(350)
    if page.evaluate(SNAP, [b, i]) == before:
        how = {"Enter": "pressed Enter", "Tab": "left the field with Tab", "ime": "pressed Enter to end an input method's composition"}[leave]
        return f"typed {value!r} and {how}: nothing in the box changed"
    return None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("site", nargs="?", default="site")
    ap.add_argument("--browser", help="path to a Chromium executable")
    ap.add_argument("--offline", action="store_true", help="ignore errors of external scripts")
    ap.add_argument("--route", action="append", default=[], metavar="REGEX=FILE",
                    help="serve requests matching REGEX from a local file")
    ap.add_argument("--only", help="check only pages whose path matches this regex")
    ap.add_argument("--local-cdn", action="store_true",
                    help="--offline with the CDN copies of .cache/cdn (tools/dev_setup.sh)")
    ap.add_argument("--shard", metavar="K/N", help="check only the K-th of N parts of the pages (1 <= K <= N)")
    args = ap.parse_args(argv)
    if args.local_cdn:
        args.offline = True
        args.route += local_cdn_routes()

    from playwright.sync_api import sync_playwright

    site = Path(args.site).resolve()
    if not site.is_dir():
        print(f"site directory not found: {site}")
        return 1
    counts = {p.relative_to(site).as_posix(): p.read_text(encoding="utf-8").count('class="explorer"')
              for p in site.rglob("index.html")}
    pages = sorted(p for p, n in counts.items() if n)
    if args.only:
        pages = [p for p in pages if re.search(args.only, p)]
    if args.shard:
        pages = shard(pages, counts, args.shard)
        if pages is None:
            print(f"--shard takes K/N with 1 <= K <= N, not {args.shard}")
            return 1
    server, base = serve(site)

    external = re.compile(r"https?://(?!127\.0\.0\.1)")
    failures = fields_total = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser) if args.browser else pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1,
                                  service_workers="block", reduced_motion="no-preference")
        for spec in args.route:
            pattern, file = spec.split("=", 1)
            ctx.route(re.compile(pattern), functools.partial(lambda file, route: route.fulfill(path=file), file))
        for rel in pages:
            url = base + rel[: -len("index.html")]
            errors: list[str] = []
            page = open_page(ctx, url, errors)
            cdp = ctx.new_cdp_session(page)
            n_boxes = page.evaluate(BOXES)
            problems: list[str] = []
            notes: list[str] = []
            fields = 0
            for b in range(n_boxes):
                kind = page.evaluate("(b) => document.querySelectorAll('.explorer')[b].dataset.kind", b)
                for i, cls, typ, aid in page.evaluate(LIST, b):
                    fields += 1
                    name = f"{kind} {b}, {typ} field {i} ({cls.strip()[:40]})"
                    # a textarea keeps Enter for its new lines: it applies when it is left; an
                    # editing aid (data-nolink: a guess, a value for a button) acts on Enter only
                    if typ == "textarea":
                        tries = ((1, "Tab"),)
                    elif aid:
                        tries = ((0, "Enter"),)
                    else:
                        tries = ((0, "Enter"), (1, "Tab"), (0, "ime"))
                    for nth, leave in tries:
                        found = try_field(page, cdp, b, i, nth, leave)
                        page.evaluate(RESET, b)
                        page.wait_for_timeout(100)
                        if found and page.evaluate(HAS_END, b):    # the start may not show the value
                            found = try_field(page, cdp, b, i, nth, leave, advance=True)
                            page.evaluate(RESET, b)
                            page.wait_for_timeout(100)
                        if found and aid:
                            notes.append(f"{name}: {found} (an editing aid: a warning)")
                        elif found:
                            problems.append(f"{name}: {found}")
            problems += [f"script error: {e[:200]}" for e in errors if not (args.offline and external.search(e))]
            page.close()
            failures += bool(problems)
            fields_total += fields
            print(f"{'FAIL' if problems else 'ok':4}  {rel[: -len('index.html')]}  {n_boxes} boxes, {fields} fields")
            for p in problems:
                print(f"        {p}")
            for n in notes:
                print(f"        warn {n}")
        browser.close()
    server.shutdown()
    print(f"{len(pages)} pages, {fields_total} fields, {failures} pages with problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
