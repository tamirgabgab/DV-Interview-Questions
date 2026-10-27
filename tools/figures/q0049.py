#!/usr/bin/env python3
"""Figures and tables of question 0049 (the architecture of a UVM testbench: the
components, the connections, and the path of one transaction).

    python tools/figures/fill.py 49        # put the blocks on the page

LAYOUT holds every component of the drawing (an id, its label, its box and whether it
is a container), ARROWS the connections between them (TLM ports, the virtual interface,
the pins), and PATH the stages of one transaction from the sequence to the scoreboard.
The explorer (docs/javascripts/explorer/uvmarch.js) draws the same layout; tests/0049
checks that both agree and that every stage of the path follows an arrow. blocks()
returns, in page order: the architecture figure, its legend, the table of the
connections and the table of the phases.
"""

RLM = "‏"
W, H = 680, 520

# id: (label, x, y, w, h, container?)
LAYOUT = {
    "top":         ("tb_top",            8,   8, 664, 504, True),
    "test":        ("test",             18,  30, 644, 326, True),
    "sequence":    ("sequence",        120,  40, 110,  30, False),
    "env":         ("env",              28,  80, 624, 266, True),
    "agent_in":    ("agent (active)",   38, 104, 252, 232, True),
    "sequencer":   ("sequencer",        48, 132, 112,  44, False),
    "driver":      ("driver",           48, 240, 100,  44, False),
    "monitor_in":  ("monitor",         170, 240, 110,  44, False),
    "scoreboard":  ("scoreboard",      304, 132, 150,  64, False),
    "coverage":    ("coverage",        304, 240, 150,  44, False),
    "agent_out":   ("agent (passive)", 470, 104, 172, 232, True),
    "monitor_out": ("monitor",         500, 240, 110,  44, False),
    "vif_in":      ("interface in",     48, 384, 232,  36, False),
    "dut":         ("DUT",             300, 376, 150, 120, False),
    "vif_out":     ("interface out",   470, 384, 172,  36, False),
}

# (from, to, kind): kind is "tlm" (a TLM port) or "pin" (signals through the interface)
ARROWS = [
    ("sequence", "sequencer", "tlm"),
    ("sequencer", "driver", "tlm"),
    ("driver", "vif_in", "pin"),
    ("vif_in", "dut", "pin"),
    ("vif_in", "monitor_in", "pin"),
    ("dut", "vif_out", "pin"),
    ("vif_out", "monitor_out", "pin"),
    ("monitor_in", "scoreboard", "tlm"),
    ("monitor_in", "coverage", "tlm"),
    ("monitor_out", "scoreboard", "tlm"),
]

# the path of one transaction, as the arrows it takes in order: down to the pins, the input
# monitor's copy to the scoreboard (the expected side), through the DUT, and the output
PATH = [("sequence", "sequencer"), ("sequencer", "driver"), ("driver", "vif_in"), ("vif_in", "monitor_in"),
        ("monitor_in", "scoreboard"), ("vif_in", "dut"), ("dut", "vif_out"), ("vif_out", "monitor_out"),
        ("monitor_out", "scoreboard")]


def center(c):
    _, x, y, w, h, _ = LAYOUT[c]
    return x + w / 2, y + h / 2


def edge_point(c, toward):
    """Where the line from the centre of c toward a point leaves the box of c."""
    _, x, y, w, h, _ = LAYOUT[c]
    cx, cy = center(c)
    dx, dy = toward[0] - cx, toward[1] - cy
    if dx == 0 and dy == 0:
        return cx, cy
    sx = (w / 2) / abs(dx) if dx else float("inf")
    sy = (h / 2) / abs(dy) if dy else float("inf")
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


def arrow_line(a, b):
    """The arrow from a to b between the box edges (straight)."""
    pa, pb = edge_point(a, center(b)), edge_point(b, center(a))
    return pa, pb


def figure():
    s = (f'<svg class="figure uv-fig" viewBox="0 0 {W} {H}" style="max-width:42rem" role="img" '
         'aria-label="סביבת UVM : test, env, שני agents, scoreboard ו-coverage מעל ה-DUT, עם ה-interfaces ביניהם">'
         '<defs><marker id="uv-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>')
    for c, (label, x, y, w, h, cont) in LAYOUT.items():
        if cont:
            s += (f'<g class="uv-box is-cont uv-{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
                  f'<text x="{x + 8}" y="{y + 17}">{label}</text></g>')
    for a, b, kind in ARROWS:
        (x1, y1), (x2, y2) = arrow_line(a, b)
        s += f'<line class="uv-arrow uv-{kind}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" marker-end="url(#uv-arrow)"/>'
    for c, (label, x, y, w, h, cont) in LAYOUT.items():
        if not cont:
            cx, cy = center(c)
            s += (f'<g class="uv-box uv-{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>'
                  f'<text x="{cx:.1f}" y="{cy + 5:.1f}" text-anchor="middle">{label}</text></g>')
    return s + "</svg>"


def legend():
    return ('<span class="viz-legend"><span><i class="uv-key-tlm"></i>חיבור TLM : טרנזקציות</span>'
            '<span><i class="uv-key-pin"></i>אותות דרך ה-interface</span></span>')


CONNECTIONS = [
    ("sequence → sequencer", "‏`start_item` / `finish_item`", "ה-sequence מבקש תור, מקבל אישור, ממלא את הפריט ושולח אותו"),
    ("sequencer → driver", "‏`seq_item_port` ← `seq_item_export`", "ה-driver מושך פריט ב-`get_next_item` ומחזיר `item_done`"),
    ("driver → interface", "‏virtual interface", "ה-driver משנה אותות לפי הפרוטוקול"),
    ("interface → monitor", "‏virtual interface", "המוניטור רק דוגם אותות, ובונה מהם טרנזקציה"),
    ("monitor → scoreboard / coverage", "‏`uvm_analysis_port` ← `uvm_analysis_imp`", "‏`write()` לכל המנויים, בלי לחכות"),
    ("config_db → driver / monitor", "‏`uvm_config_db#(virtual ...)::get`", "ה-top שם את ה-interface, והרכיבים לוקחים אותו ב-`build_phase`"),
]


def connections_table():
    rows = ["| החיבור | המנגנון | מה עובר בו |", "|---|---|---|"]
    rows += [f"| {RLM}{a} | {b} | {c} |" for a, b, c in CONNECTIONS]
    return "\n".join(rows)


PHASES = [
    ("‏`build_phase`", "מלמעלה למטה", "יצירת הרכיבים (`type_id::create`) ולקיחת הגדרות מ-`config_db`"),
    ("‏`connect_phase`", "מלמטה למעלה", "חיבור ה-ports : ‏driver ל-sequencer, מוניטורים ל-scoreboard"),
    ("‏`end_of_elaboration_phase`", "מלמטה למעלה", "הדפסת הטופולוגיה, בדיקות שהכול מחובר"),
    ("‏`run_phase`", "במקביל, זמן סימולציה", "ה-test מרים objection, מריץ sequences ומוריד objection"),
    ("‏`extract` / `check` / `report`", "מלמטה למעלה", "בדיקות סוף : תורים ריקים ב-scoreboard, סיכום שגיאות"),
]


def phases_table():
    rows = ["| השלב | הסדר | מה קורה בו |", "|---|:-:|---|"]
    rows += [f"| {a} | {b} | {c} |" for a, b, c in PHASES]
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [figure(), legend(), connections_table(), phases_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
