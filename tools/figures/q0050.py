#!/usr/bin/env python3
"""Figures and tables of question 0050 (a scoreboard for responses that may return out of
order across IDs and in order within an ID).

    python tools/figures/fill.py 50        # put the blocks on the page

The reference here is independent of the page code: three small checkers written from
their definitions (one queue per ID, one global FIFO, "any pending item of the same ID"),
each with the same end-of-test and timeout checks, and a set of short scenarios with the
truth of each (is the DUT's behaviour legal). blocks() returns, in page order: the figure
of the per-ID queues after a few events, its legend, and the table of the scenarios
against the three checkers. tests/0050 checks the page code against these and against
random legal and mutated traffic.
"""

TIMEOUT = 8
RLM = "‏"


# --- the checkers ------------------------------------------------------------------------

def check(events, kind, timeout=TIMEOUT):
    """The errors a checker reports on a list of events (t, op, id, data); op is "req",
    "rsp", "reset" or "end". kind: "per_id", "fifo" or "any"."""
    pend = []                 # (t, id, data) in arrival order
    errors = []

    def overdue(now):
        for t, i, d in pend:
            if now - t > timeout and (t, i, d, "late") not in seen:
                seen.add((t, i, d, "late"))
                errors.append(("timeout", i))

    seen = set()
    for t, op, i, d in events:
        overdue(t)
        if op == "req":
            pend.append((t, i, d))
        elif op == "reset":
            pend.clear()
        elif op == "end":
            errors += [("missing", i) for _, i, _ in pend]
        elif op == "rsp":
            if kind == "fifo":
                cand = pend[:1]
                if cand and cand[0][1] != i:
                    errors.append(("mismatch", i))
                    pend.pop(0)
                    continue
            elif kind == "per_id":
                cand = [p for p in pend if p[1] == i][:1]
            else:
                cand = [p for p in pend if p[1] == i and p[2] == d][:1] or [p for p in pend if p[1] == i][:1]
            if not cand:
                errors.append(("unexpected", i))
                continue
            pend.remove(cand[0])
            if cand[0][2] != d:
                errors.append(("mismatch", i))
    return errors


# The scenarios: (name in Hebrew, legal?, events). Data is what the reference model expects
# for a read (here a number per request).
SCENARIOS = [
    ("ערבוב חוקי בין IDs", True,
     [(0, "req", 0, 10), (1, "req", 1, 20), (2, "req", 0, 11), (3, "rsp", 1, 20), (4, "rsp", 0, 10), (5, "rsp", 0, 11), (6, "end", 0, 0)]),
    ("החלפת סדר בתוך ID", False,
     [(0, "req", 0, 10), (1, "req", 0, 11), (2, "rsp", 0, 11), (3, "rsp", 0, 10), (4, "end", 0, 0)]),
    ("נתון שגוי", False,
     [(0, "req", 0, 10), (1, "req", 1, 20), (2, "rsp", 1, 21), (3, "rsp", 0, 10), (4, "end", 0, 0)]),
    ("תשובה חסרה", False,
     [(0, "req", 0, 10), (1, "req", 1, 20), (2, "rsp", 1, 20), (3, "end", 0, 0)]),
    ("תשובה כפולה", False,
     [(0, "req", 0, 10), (1, "rsp", 0, 10), (2, "rsp", 0, 10), (3, "end", 0, 0)]),
    ("תשובה מאוחרת", False,
     [(0, "req", 0, 10), (12, "rsp", 0, 10), (13, "end", 0, 0)]),
    ("איפוס, ותשובה חדשה אחריו", True,
     [(0, "req", 0, 10), (1, "req", 1, 20), (2, "reset", 0, 0), (3, "req", 1, 21), (4, "rsp", 1, 21), (5, "end", 0, 0)]),
    ("תשובה ישנה אחרי איפוס", False,
     [(0, "req", 0, 10), (1, "reset", 0, 0), (2, "rsp", 0, 10), (3, "end", 0, 0)]),
]

NAMES = {"timeout": "timeout", "missing": "חסרה", "unexpected": "לא צפויה", "mismatch": "אי-התאמה"}


def verdict(errors, legal):
    if not errors:
        return "✓ עבר" if legal else "✗ פספס באג"
    what = ", ".join(dict.fromkeys(NAMES[e] for e, _ in errors))
    return f"✓ תפס ({what})" if not legal else f"✗ אזעקת שווא ({what})"


# --- blocks ------------------------------------------------------------------------------

def queues_figure():
    """The per-ID queues after the requests 0:A, 1:B, 0:C, 2:D, 1:E and the response of B."""
    reqs = [(0, "A"), (1, "B"), (0, "C"), (2, "D"), (1, "E")]
    W, H = 640, 250
    s = (f'<svg class="figure sb-fig" viewBox="0 0 {W} {H}" style="max-width:40rem" role="img" '
         'aria-label="תור לכל ID : הבקשות נכנסות לסוף התור של ה-ID שלהן, ותשובה נבדקת מול ראש התור של אותו ID">')
    # the stream of requests on top, oldest on the right
    s += f'<text class="legend" x="{W - 10}" y="22" text-anchor="end" direction="rtl">בקשות, לפי סדר ההגעה</text>'
    for k, (i, name) in enumerate(reqs):
        x = W - 70 - k * 70
        done = name == "B"
        s += (f'<g class="sb-item sb-id{i}{" is-done" if done else ""}"><rect x="{x - 26}" y="34" width="52" height="30" rx="5"/>'
              f'<text x="{x}" y="54" text-anchor="middle">{i}:{name}</text></g>')
    # the queues
    for i in range(3):
        y = 108 + i * 46
        s += f'<text class="sb-qname" x="{W - 20}" y="{y + 20}" text-anchor="end">ID {i}</text>'
        s += f'<line class="sb-rail" x1="{W - 90}" y1="{y + 15}" x2="{W - 400}" y2="{y + 15}"/>'
        items = [n for j, n in reqs if j == i and n != "B"]
        for k, name in enumerate(items):
            x = W - 120 - k * 64
            head = k == 0
            s += (f'<g class="sb-item sb-id{i}{" is-head" if head else ""}"><rect x="{x - 26}" y="{y}" width="52" height="30" rx="5"/>'
                  f'<text x="{x}" y="{y + 20}" text-anchor="middle">{name}</text></g>')
        if not items:
            s += f'<text class="tick" x="{W - 120}" y="{y + 20}" text-anchor="middle">(empty)</text>'
    # the response that just arrived
    s += ('<g class="sb-item sb-id1 is-rsp"><rect x="40" y="154" width="120" height="30" rx="5"/>'
          '<text x="100" y="174" text-anchor="middle">rsp 1:B ✓</text></g>'
          '<path class="sb-arrow" d="M160,169 L220,169" marker-end="url(#sb-arrow)"/>'
          '<defs><marker id="sb-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>')
    s += f'<text class="legend" x="100" y="206" text-anchor="middle">popped from the head of queue 1</text>'
    return s + "</svg>"


def legend():
    return ('<span class="viz-legend"><span><i class="sb-key-head"></i>ראש התור : התשובה הבאה של ה-ID הזה</span>'
            '<span><i class="sb-key-done"></i>בקשה שכבר נענתה</span></span>')


def scenario_table():
    rows = ["| התרחיש | ה-DUT תקין? | תור לכל ID | תור אחד לכולם | חיפוש בכל התור של ה-ID |", "|---|:-:|:-:|:-:|:-:|"]
    for name, legal, ev in SCENARIOS:
        cells = [verdict(check(ev, k), legal) for k in ("per_id", "fifo", "any")]
        rows.append(f"| {name} | {'כן' if legal else 'לא'} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [queues_figure(), legend(), scenario_table()]


if __name__ == "__main__":
    for name, legal, ev in SCENARIOS:
        print(name, legal, [check(ev, k) for k in ("per_id", "fifo", "any")])
    print("\n\n".join(blocks()))
