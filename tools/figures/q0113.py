#!/usr/bin/env python3
"""Figures and tables of question 0113, the test that ends at time 0 (phases, objections
and the drain time).

    python tools/figures/fill.py 113        # put the blocks on the page

The model here is a timing model of the page's testbench, written from its description: a
10 ns clock that starts low (rising edges at 5, 15, 25, ... ns), a driver that holds reset
for two rising edges and then gives one item per cycle, monitors that sample at the falling
edge, and the DUT's latency of LAT cycles. tests/0113 runs the page's pyuvm code on
Verilator and checks every number here against the run: the end time, the items compared
and missing of every test, and the run that never ends.

blocks() returns, in page order: the log of SmokeTest, the log of ObjectionTest, the
timeline of the items against the drop of the objection, its legend, the table of drain
times, the log of the bounded run, and the table of the four runs.
"""

from __future__ import annotations

NB = " "
RLM = "‏"

PERIOD = 10          # ns
LAT = 4              # DUT latency in cycles
N = 8                # items per test
RESET_EDGES = 2      # rising edges with rst_n low
DRAIN_NS = 40        # the page's drain time
LIMIT_US = 100       # the page's global timeout
DRAINS = (0, 10, 20, 30, 40, 50)
SB = "uvm_test_top.env.sb"
HOLDER = "uvm_test_top.env.mon_out"
TIMEOUT_SRC = "cocotb.pipe"       # the logger of dut._log


def rise(k):
    """The time of rising edge k (k = 0, 1, 2, ...)."""
    return PERIOD // 2 + PERIOD * k


def taken(i):
    """The rising edge at which the DUT takes item i (after reset, one item per cycle)."""
    return rise(RESET_EDGES + i)


def seen_in(i):
    """The falling edge at which the input monitor sees item i (it is driven from the edge
    before the one that takes it)."""
    return taken(i) - PERIOD // 2


def seen_out(i):
    """The falling edge at which the output monitor sees item i: the valid bit walks
    through LAT flops, the first one written at the edge that takes the item."""
    return taken(i) + (LAT - 1) * PERIOD + PERIOD // 2


def last_taken():
    return taken(N - 1)


def run(test, drain=DRAIN_NS):
    """{end, sent, compared, missing, passed} of a test: "smoke" (no objection), "objection"
    (raise, start, drop), "drain" (the drop waits `drain` ns). The run ends at the drop,
    and check_phase counts what the monitors saw before it."""
    end = {"smoke": 0, "objection": last_taken(), "drain": last_taken() + drain}[test]
    sent = sum(seen_in(i) < end for i in range(N))
    seen = sum(seen_out(i) < end for i in range(N))
    return {"end": end, "sent": sent, "compared": seen, "missing": sent - seen, "passed": sent == seen}


def min_drain():
    """The drain must outlast the time from the drop to the last item at the output monitor."""
    return seen_out(N - 1) - last_taken()


def sb_lines(r):
    """The scoreboard's two lines of a run: (level, path, message)."""
    return [("INFO", SB, f"{r['end']} ns: {r['compared']} compared, 0 mismatches, {r['missing']} missing"),
            ("INFO", SB, "TEST PASSED") if r["passed"] else ("ERROR", SB, "TEST FAILED")]


def log(lines):
    return "```text\n" + "\n".join(f"{lvl:<8} [{who}] {msg}" for lvl, who, msg in lines) + "\n```"


def timeout_lines():
    """The bounded run (the colleague's monitor): run() of the page's fix stops it."""
    return [("CRITICAL", TIMEOUT_SRC, f"timeout at {LIMIT_US * 1000} ns"),
            ("", "", "Active objections:"),
            ("", "", f' raised by {HOLDER}, description=""')]


def timeout_log():
    rows = []
    for lvl, who, msg in timeout_lines():
        rows.append(f"{lvl:<8} [{who}] {msg}" if lvl else msg)
    return "```text\n" + "\n".join(rows) + "\n```"


# --- the timeline ------------------------------------------------------------------------

W, H = 400, 158
X0, X1 = 38, 392
T_MAX = 150
ROW_IN, ROW_OUT, BASE, TOP = 40, 92, 126, 14


def X(t):
    return X0 + t / T_MAX * (X1 - X0)


def item_box(t, y, k, cls):
    w = PERIOD / T_MAX * (X1 - X0) - 3
    return (f'<rect class="{cls}" x="{X(t) - w / 2:.1f}" y="{y - 12}" width="{w:.1f}" height="24" rx="3" '
            f'fill="none" stroke-width="2"/>'
            f'<text class="tick" x="{X(t):.1f}" y="{y + 5}" text-anchor="middle" style="font-size:14px">{k}</text>')


def timeline():
    drop, end = last_taken(), last_taken() + DRAIN_NS
    s = [f'<svg class="perf-chart q113-timeline" viewBox="0 0 {W} {H}" style="max-width:34rem" role="img" '
         f'aria-label="{N} items: taken by the DUT at {taken(0)} to {drop} ns, seen at the output at '
         f'{seen_out(0)} to {seen_out(N - 1)} ns; the objection drops at {drop} ns, the drain ends at {end} ns">']
    s.append(f'<rect class="hist-near" x="{X(drop):.1f}" y="{TOP}" width="{X(end) - X(drop):.1f}" height="{BASE - TOP}"/>')
    for t in range(0, T_MAX + 1, 50):
        last = t == T_MAX
        s.append(f'<text class="tick" x="{X(t):.1f}" y="{BASE + 18}" text-anchor="{"end" if last else "middle"}" '
                 f'style="font-size:14px">{t}{" ns" if last else ""}</text>')
    s.append(f'<line class="axis" x1="{X0}" x2="{X1}" y1="{BASE}" y2="{BASE}"/>')
    for name, y in (("in", ROW_IN), ("out", ROW_OUT)):
        s.append(f'<text class="tick" x="{X0 - 6}" y="{y + 5}" text-anchor="end" style="font-size:14px">{name}</text>')
    for i in range(N):
        s.append(item_box(seen_in(i), ROW_IN, i, "ink-line"))
        s.append(item_box(seen_out(i), ROW_OUT, i, "s1-line" if seen_out(i) < drop else "s2-line"))
    s.append(f'<line class="ink-line" x1="{X(drop):.1f}" x2="{X(drop):.1f}" y1="{TOP}" y2="{BASE}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    s.append(f'<line class="ink-line" x1="{X(end):.1f}" x2="{X(end):.1f}" y1="{TOP}" y2="{BASE}" stroke-width="1.5"/>')
    for t in (drop, end):
        s.append(f'<text class="tick" x="{X(t):.1f}" y="{TOP - 2}" text-anchor="middle" style="font-size:13px">{t}</text>')
    return "".join(s) + "</svg>"


def legend():
    drop, end = last_taken(), last_taken() + DRAIN_NS
    return ('<span class="viz-legend">'
            f'<span><i class="s1"></i>פריט שיצא לפני {drop} ns{NB}: נבדק בשתי הריצות</span>'
            f'<span><i class="s2"></i>פריט שעוד היה בצינור{NB}: נבדק רק עם drain</span>'
            f'<span><i class="ink-dash"></i>הורדת ה-objection בלי drain, ב-{drop} ns</span>'
            f'<span><i class="ink"></i>סוף הריצה עם drain של {DRAIN_NS} ns, ב-{end} ns</span>'
            '</span>')


def drain_table():
    rows = ["| ה-drain | סוף הריצה | נבדקו | חסרים | התוצאה |", "|:-:|:-:|:-:|:-:|:-:|"]
    for d in DRAINS:
        r = run("drain", d)
        verdict = "עובר" if r["passed"] else "נכשל"
        rows.append(f"| {d} ns | {r['end']} ns | {r['compared']} | {r['missing']} | {verdict} |")
    return "\n".join(rows)


def runs_table():
    rows = ["| הריצה | סוף הריצה | נבדקו | חסרים | מה ה-scoreboard אומר |", "|:--|:-:|:-:|:-:|:--|"]
    names = {"smoke": "‏`SmokeTest`, בלי objection", "objection": "‏`ObjectionTest`, בלי drain",
             "drain": f"‏`DrainTest`, ‏drain של {DRAIN_NS} ns"}
    for test in ("smoke", "objection", "drain"):
        r = run(test)
        say = "עובר" + (f"{NB}: לא נבדק כלום" if r["compared"] == 0 else "") if r["passed"] else "נכשל"
        rows.append(f"| {names[test]} | {r['end']} ns | {r['compared']} | {r['missing']} | {say} |")
    rows.append(f"| ‏`DrainTest` עם המוניטור של העמית | אין סוף{NB}: נעצר ב-{LIMIT_US} µs | — | — | לא מגיע ל-`check_phase` |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [log(sb_lines(run("smoke"))), log(sb_lines(run("objection"))), timeline(), legend(),
            drain_table(), timeout_log(), runs_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
