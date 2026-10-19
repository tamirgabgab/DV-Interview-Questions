#!/usr/bin/env python3
"""Figures and tables of question 0023 (PCIe endpoint reference model).

    python tools/figures/q0023.py > /tmp/q0023.html

Prints, in page order. Part a: the aligned read over the memory blocks (one or two
completions) and its legend; the cycle-by-cycle stepper of two interleaved reads and its
legend; the table of that run. Part b: the blocks an unaligned request touches and its
legend; the table of the block walk; the map of the four legal splits (and the illegal
128 + 128) and its legend; the table of the splits; the table of a run with an aligned and
an unaligned read. The runs come from the page's own Python code driven by a scripted
"random" source, so the figures show one fixed, hand-picked run; tests/0023 checks that the
page copies match.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_code import load_python  # noqa: E402
from stepper import stepper  # noqa: E402

ns = load_python(23)
MemWriteReq, MemReadReq = ns["MemWriteReq"], ns["MemReadReq"]
EndpointRefModel, UnalignedEndpointModel = ns["EndpointRefModel"], ns["UnalignedEndpointModel"]
RCB = ns["RCB"]

RLM = "‏"
BASE, SPAN = 0xFF80, 512          # address axis of the figures: 0xFF80 .. 0x10180
X0, X1 = 40, 600


class Script:
    """Stand-in for random.Random that returns prepared values in order, so a run of the
    page's model is fixed and hand-picked (coin flips, delays, and the index of the read
    chosen among the ready ones)."""

    def __init__(self, *values):
        self.values = list(values)

    def randint(self, a, b):
        v = self.values.pop(0)
        assert a <= v <= b, (a, v, b)
        return v

    def choice(self, seq):
        return seq[self.values.pop(0)]

    def done(self):
        assert not self.values, self.values


def x(addr):
    return X0 + (addr - BASE) * (X1 - X0) / SPAN


def grid(p, y_top, y_bot):
    for off in range(0, SPAN + 1, RCB):
        xx = x(BASE + off)
        p.append(f'<line class="cs-rcb" x1="{xx:.1f}" y1="{y_top}" x2="{xx:.1f}" y2="{y_bot}"/>')
        p.append(f'<text class="coord halo" x="{xx:.1f}" y="18" text-anchor="middle">0x{BASE + off:X}</text>')


def request_lines(p, start, end, y_top, y_bot):
    for a in (start, end):
        p.append(f'<line class="cs-req" x1="{x(a):.1f}" y1="{y_top}" x2="{x(a):.1f}" y2="{y_bot}"/>')


def box(p, cls, start, end, y, h, text, title=None, text_cls="cs-size"):
    a, b = x(start), x(end)
    t = f"<title>{title}</title>" if title else ""
    p.append(f'<rect class="{cls}" x="{a:.1f}" y="{y}" width="{b - a:.1f}" height="{h}" rx="3">{t}</rect>')
    if text:
        p.append(f'<text class="{text_cls}" x="{(a + b) / 2:.1f}" y="{y + h / 2 + 4.5:.1f}" '
                 f'text-anchor="middle">{text}</text>')


def legend(items):
    return ('<span class="viz-legend">' + "".join(f'<span><i class="{c}"></i>{t}</span>' for c, t in items)
            + "</span>")


# ------------------------------------------------------------------ part a: the aligned read

def aligned_svg():
    p = ['<svg class="figure cs-fig" viewBox="0 0 640 206" style="max-width:40rem" role="img" '
         'aria-label="קריאה מיושרת של 256 בתים מכתובת 0x10000: שני הבלוקים בזיכרון, ושתי התשובות '
         'החוקיות: Completion אחד של 256 בתים, או שניים של 128">']
    grid(p, 26, 174)
    request_lines(p, 0x10000, 0x10100, 30, 174)
    p.append('<text class="legend halo" x="44" y="46">memory after the write</text>')
    for key in (0x10000, 0x10080):
        box(p, "cs-blk", key, key + RCB, 52, 26, f"memory[0x{key:X}]", f"block 0x{key:X}: 128 bytes", "coord")
    p.append(f'<text class="tick" x="{x(0x10100 + RCB / 2):.1f}" y="69" text-anchor="middle">no entry</text>')
    p.append('<text class="legend halo" x="44" y="98">one completion</text>')
    box(p, "cs-one", 0x10000, 0x10100, 104, 26, "256 B · BC 256", "0x10000–0x100FF, byte count 256")
    p.append(f'<circle class="cs-can" cx="{x(0x10080):.1f}" cy="117" r="4.5">'
             '<title>0x10080: the only legal cut</title></circle>')
    p.append('<text class="legend halo" x="44" y="150">two completions</text>')
    box(p, "cs-first", 0x10000, 0x10080, 156, 26, "128 B · BC 256", "0x10000–0x1007F, byte count 256")
    box(p, "cs-last", 0x10080, 0x10100, 156, 26, "128 B · BC 128", "0x10080–0x100FF, byte count 128")
    p.append(f'<text class="legend halo" x="{x(0x10080):.1f}" y="198" text-anchor="middle">'
             'request: 256 B from 0x10000, RID 0x0200, tag 0x15</text>')
    p.append("</svg>")
    return "".join(p)


def aligned_legend():
    return legend([("cs-rcb", "גבול RCB"), ("cs-req", "תחילת הבקשה וסופה"),
                   ("cs-blk", "בלוק בזיכרון, המפתח הוא כתובת הבלוק"), ("cs-can", "נקודת החיתוך המותרת"),
                   ("cs-one", f"{RLM}Completion יחיד"), ("cs-first", "ראשון"), ("cs-last", "אחרון")])


# ------------------------------------------------------------------ part a: the interleaving run

NAMES = {0x15: "A", 0x16: "B", 0x22: "B"}


def run(model, script, reads, write_len=512):
    """Drive the page's model: one write, the reads in one cycle, then cycle by cycle until
    every completion went out. Returns the trace and the per-cycle snapshots."""
    m = model(script)
    m.process_write(MemWriteReq(0x10000, bytes(i & 0xFF for i in range(write_len))))
    for r in reads:
        m.process_read(r)
    sent, frames = [], []
    frames.append((0, snapshot(m), None, list(sent)))
    while m.pending_reads:
        m.tick()
        state = snapshot(m)
        cpl = m.get_next_completion()
        if cpl is not None:
            sent.append((m.current_cycle, cpl))
        frames.append((m.current_cycle, state, cpl, list(sent)))
        assert m.current_cycle < 50
    script.done()
    return sent, frames


def snapshot(m):
    """(name, ready_cycle, [(start, size, byte_count) of the completions still queued])."""
    return [(NAMES[p.cpls[0].tag], p.ready_cycle,
             [(c.start_address, len(c.data), c.byte_count) for c in p.cpls]) for p in m.pending_reads]


def frame_svg(cycle, state, sent, all_cpls):
    p = [f'<svg class="figure cs-fig" viewBox="0 0 640 236" style="max-width:40rem" role="img" '
         f'aria-label="מחזור {cycle}: תורי ההמתנה של שתי הקריאות וה-Completions שכבר נשלחו">']
    p.append(f'<text class="coord" x="8" y="22" font-weight="700">cycle {cycle}</text>')
    queued = {name: (ready, cpls) for name, ready, cpls in state}
    for row, name in enumerate(("A", "B")):
        y = 44 + row * 58
        cls = "cs-first" if name == "A" else "cs-last"
        ready, cpls = queued.get(name, (None, []))
        tag = 0x15 if name == "A" else 0x16
        p.append(f'<text class="coord" x="8" y="{y + 16}">{name} · tag 0x{tag:02X}</text>')
        if ready is None:
            status = "done"
        elif ready <= cycle:
            status = "ready"
            p.append(f'<circle class="cs-can" cx="14" cy="{y + 32}" r="4.5"/>')
        else:
            status = f"ready at {ready}"
        p.append(f'<text class="tick" x="{24 if status == "ready" else 8}" y="{y + 36}">{status}</text>')
        for i, (start, size, bc) in enumerate(all_cpls[name]):
            xx = 200 + i * 132
            pending = (start, size, bc) in cpls
            rect_cls = cls if pending else "st-done"
            p.append(f'<rect class="{rect_cls}" x="{xx}" y="{y}" width="120" height="40" rx="3"/>')
            p.append(f'<text class="cs-size" x="{xx + 60}" y="{y + 16}" text-anchor="middle">'
                     f'{size} B @ 0x{start:X}</text>')
            p.append(f'<text class="tick" x="{xx + 60}" y="{y + 32}" text-anchor="middle">BC {bc}</text>')
    p.append('<text class="coord" x="8" y="192">sent</text>')
    for i, (at, cpl) in enumerate(sent):
        name = NAMES[cpl.tag]
        cls = "cs-first" if name == "A" else "cs-last"
        xx = 70 + i * 110
        p.append(f'<rect class="{cls}" x="{xx}" y="170" width="100" height="40" rx="3"/>')
        p.append(f'<text class="cs-size" x="{xx + 50}" y="{186}" text-anchor="middle">cycle {at}</text>')
        p.append(f'<text class="tick" x="{xx + 50}" y="{202}" text-anchor="middle">'
                 f'{name}: 0x{cpl.start_address:X}</text>')
    if not sent:
        p.append('<text class="tick" x="70" y="195">nothing yet</text>')
    p.append("</svg>")
    return "".join(p)


def timeline_stepper():
    reads = [MemReadReq(0x10000, 256, 0x0200, 0x15), MemReadReq(0x10100, 256, 0x0200, 0x16)]
    # A: split (1), ready in 5; B: split (1), ready in 3; cycle 3: B then gap 3; cycle 5: A then
    # gap 1; cycle 6: both ready, pick B (index 1); cycle 7: A.
    script = Script(1, 5, 1, 3, 0, 3, 0, 1, 1, 0)
    sent, frames = run(EndpointRefModel, script, reads)
    all_cpls = {name: cpls for name, _, cpls in frames[0][1]}
    out = []
    for cycle, state, cpl, sent_so_far in frames:
        if cycle > 0 and cpl is None and cycle != 1:
            continue                                   # quiet cycles: show only the first
        svg = frame_svg(cycle, state, sent_so_far, all_cpls)
        ready = {name for name, r, _ in state if r <= cycle}
        if cycle == 0:
            cap = ("מחזור 0: שתי הקריאות הגיעו. כל אחת פוצלה ל-128 + 128 וקיבלה מחזור מוכנות אקראי: "
                   "A מוכנה ממחזור 5, ‏B ממחזור 3.")
        elif cpl is None:
            cap = f"מחזור {cycle}: אף קריאה לא מוכנה עדיין, ולכן אין Completion."
        else:
            name = NAMES[cpl.tag]
            left = next((len(c) for n, _, c in snapshot_after(state, name)), 0)
            both = " שתי הקריאות מוכנות, והבחירה ביניהן אקראית." if len(ready) == 2 else ""
            tail = (f" זה היה ה-Completion האחרון של {name}." if left == 1 else
                    f" ‏{name} ממתינה שוב, עם מחזור מוכנות חדש.")
            cap = (f"מחזור {cycle}:{both} נבחרה {name} ושלחה את ה-Completion הבא שלה: "
                   f"{len(cpl.data)} בתים מ-<span dir=\"ltr\">0x{cpl.start_address:X}</span>, "
                   f"Byte Count {cpl.byte_count}.{tail}")
        out.append((svg, cap))
    return stepper(out, "שתי קריאות ממתינות, מחזור אחרי מחזור"), sent


def snapshot_after(state, name):
    return [(n, r, c) for n, r, c in state if n == name]


def timeline_legend():
    return legend([("cs-first", f"{RLM}Completions של קריאה A"), ("cs-last", f"{RLM}Completions של קריאה B"),
                   ("st-done", "כבר נשלח"), ("cs-can", "קריאה שמחזור המוכנות שלה הגיע")])


def timeline_table(sent):
    rows = [f"| מחזור | קריאה | כתובת | גודל | {RLM}Byte Count |", "|---|---|---|---|---|"]
    for at, c in sent:
        rows.append(f"| {at} | {RLM}{NAMES[c.tag]} (Tag 0x{c.tag:02X}) | {RLM}`0x{c.start_address:X}` | "
                    f"{len(c.data)} | {c.byte_count} |")
    return "\n".join(rows)


# ------------------------------------------------------------------ part b: blocks and chunks

REQ_B = (0x10020, 256)


def chunks(address, length):
    out, done = [], 0
    while done < length:
        key, off = divmod(address + done, RCB)
        n = min(RCB - off, length - done)
        out.append((key * RCB, off, n))
        done += n
    return out


def chunks_svg():
    start, length = REQ_B
    end = start + length
    p = ['<svg class="figure cs-fig" viewBox="0 0 640 150" style="max-width:40rem" role="img" '
         'aria-label="בקשה של 256 בתים מכתובת 0x10020 נוגעת בשלושה בלוקים: 96 בתים אחרונים של 0x10000, '
         'כל 0x10080, ו-32 הבתים הראשונים של 0x10100; שני גבולות RCB בתוך הבקשה">']
    grid(p, 26, 124)
    for key in (0x10000, 0x10080, 0x10100):
        box(p, "cs-blk", key, key + RCB, 40, 30, "")
        p.append(f'<text class="coord halo" x="{x(key + RCB / 2):.1f}" y="88" text-anchor="middle">'
                 f'memory[0x{key:X}]</text>')
    box(p, "cs-keep", 0x10000, start, 41, 28, "32", "0x10000–0x1001F: 32 bytes kept as they were")
    box(p, "cs-keep", end, 0x10180, 41, 28, "96", "0x10120–0x1017F: 96 bytes kept as they were")
    for key, off, n in chunks(start, length):
        box(p, "cs-new", key + off, key + off + n, 41, 28, str(n), f"block 0x{key:X}, offset {off}, {n} bytes")
    request_lines(p, start, end, 30, 124)
    p.append(f'<line class="ink-line" x1="{x(start):.1f}" y1="106" x2="{x(end):.1f}" y2="106" stroke-width="1.6"/>')
    for b in (0x10080, 0x10100):
        p.append(f'<circle class="cs-can" cx="{x(b):.1f}" cy="106" r="4.5"><title>0x{b:X}: a legal cut</title></circle>')
    p.append(f'<text class="legend halo" x="{x(start + length / 2):.1f}" y="142" text-anchor="middle">'
             f'request: {length} B from 0x{start:X} (0x{start:X} … 0x{end - 1:X}), cuts allowed at 0x10080 and 0x10100</text>')
    p.append("</svg>")
    return "".join(p)


def chunks_legend():
    return legend([("cs-blk", "בלוק בזיכרון"), ("cs-new", "בתים שהבקשה נוגעת בהם"),
                   ("cs-keep", "בתים קיימים שנשמרים"), ("cs-can", "גבול RCB בתוך הבקשה"),
                   ("cs-req", "תחילת הבקשה וסופה")])


def chunks_table():
    start, length = REQ_B
    rows = ["| סיבוב | בלוק (המפתח) | היסט | בתים (n) | מכסה |", "|---|---|---|---|---|"]
    for i, (key, off, n) in enumerate(chunks(start, length), 1):
        rows.append(f"| {i} | {RLM}`0x{key:X}` | {off} | {n} | <span dir=\"ltr\">0x{key + off:X} … 0x{key + off + n - 1:X}</span> |")
    return "\n".join(rows)


# ------------------------------------------------------------------ part b: the splits

def splits():
    """The four legal splits of the example from the page's own create_fragments: one coin
    per interior boundary (0x10080, then 0x10100)."""
    start, length = REQ_B
    out = []
    for coins in ((0, 0), (1, 0), (0, 1), (1, 1)):
        s = Script(*coins)
        sizes = UnalignedEndpointModel(s).create_fragments(start, length)
        s.done()
        out.append(sizes)
    return out


def rows_of(sizes, start=REQ_B[0]):
    """(role, start, size, byte_count) per completion."""
    out, pos, left = [], start, sum(sizes)
    for i, size in enumerate(sizes):
        role = "one" if len(sizes) == 1 else "first" if i == 0 else "last" if i == len(sizes) - 1 else "mid"
        out.append((role, pos, size, left))
        pos += size
        left -= size
    return out


def splits_svg():
    start, length = REQ_B
    end = start + length
    all_splits = splits()
    row_h, top = 44, 34
    height = top + row_h * (len(all_splits) + 1) + 20
    p = [f'<svg class="figure cs-fig" viewBox="0 0 640 {height}" style="max-width:40rem" role="img" '
         'aria-label="ארבעת הפיצולים החוקיים של קריאה של 256 בתים מכתובת 0x10020, עם Byte Count של כל '
         'Completion, והפיצול הפסול 128 + 128 שחותך ב-0x100A0">']
    grid(p, 26, height - 22)
    request_lines(p, start, end, 30, height - 22)
    for r, sizes in enumerate(all_splits):
        y = top + r * row_h
        p.append(f'<text class="legend halo" x="44" y="{y + 26}">{" + ".join(map(str, sizes))}</text>')
        for role, pos, size, left in rows_of(sizes):
            box(p, f"cs-{role}", pos, pos + size, y + 10, 26, str(size),
                f"0x{pos:X}–0x{pos + size - 1:X}: {size} bytes, byte count {left}")
            p.append(f'<text class="tick" x="{x(pos + size / 2):.1f}" y="{y + 6}" text-anchor="middle">BC {left}</text>')
    y = top + len(all_splits) * row_h
    cut = start + 128
    p.append(f'<text class="legend halo" x="44" y="{y + 26}">128 + 128 ✕</text>')
    box(p, "cs-bad", start, cut, y + 10, 26, "128", "0x10020–0x1009F")
    box(p, "cs-bad", cut, end, y + 10, 26, "128", "0x100A0–0x1011F")
    p.append(f'<text class="cs-no halo" x="{x(cut):.1f}" y="{y + 6}" text-anchor="middle">cut at 0x{cut:X}: not a boundary</text>')
    p.append("</svg>")
    return "".join(p)


def splits_legend():
    return legend([("cs-one", f"{RLM}Completion יחיד"), ("cs-first", "ראשון: מכתובת הבקשה עד גבול"),
                   ("cs-mid", "אמצעי: מגבול לגבול"), ("cs-last", "אחרון: עד סוף הבקשה"),
                   ("cs-bad", "חיתוך שלא על גבול RCB")])


def splits_table():
    rows = [f"| פיצול | כתובות ההתחלה | גדלים | {RLM}Byte Count |", "|---|---|---|---|"]
    for sizes in splits():
        parts = rows_of(sizes)
        rows.append(f"| {RLM}{' + '.join(map(str, sizes))} | "
                    f"<span dir=\"ltr\">{', '.join(f'0x{pos:X}' for _, pos, _, _ in parts)}</span> | "
                    f"<span dir=\"ltr\">{', '.join(str(s) for _, _, s, _ in parts)}</span> | "
                    f"<span dir=\"ltr\">{', '.join(str(bc) for _, _, _, bc in parts)}</span> |")
    return "\n".join(rows)


# ------------------------------------------------------------------ part b: the run

def trace_table():
    reads = [MemReadReq(0x10000, 256, 0x0200, 0x15), MemReadReq(0x10020, 256, 0x0300, 0x22)]
    # A: split, ready in 4; B: both cuts, ready in 2; cycle 2: B, gap 3; cycle 4: A, gap 2;
    # cycle 5: B, gap 1; cycle 6: both ready, pick A (index 0); cycle 7: B.
    script = Script(1, 4, 1, 1, 2, 0, 3, 0, 2, 0, 1, 0, 0)
    sent, _ = run(UnalignedEndpointModel, script, reads)
    rows = [f"| מחזור | {RLM}Requester ID | {RLM}Tag | כתובת | גודל | {RLM}Byte Count | הבית הראשון והאחרון |",
            "|---|---|---|---|---|---|---|"]
    for at, c in sent:
        rows.append(f"| {at} | {RLM}`0x{c.requester_id:04X}` | {RLM}`0x{c.tag:02X}` | {RLM}`0x{c.start_address:X}` | "
                    f"{len(c.data)} | {c.byte_count} | <span dir=\"ltr\">0x{c.data[0]:02X} … 0x{c.data[-1]:02X}</span> |")
    return "\n".join(rows)


if __name__ == "__main__":
    print(aligned_svg(), "\n")
    print(aligned_legend(), "\n")
    stepper_html, sent_a = timeline_stepper()
    print(stepper_html, "\n")
    print(timeline_legend(), "\n")
    print(timeline_table(sent_a), "\n")
    print(chunks_svg(), "\n")
    print(chunks_legend(), "\n")
    print(chunks_table(), "\n")
    print(splits_svg(), "\n")
    print(splits_legend(), "\n")
    print(splits_table(), "\n")
    print(trace_table(), "\n")
