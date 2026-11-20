"""Question 0110, three bugs in RTL: every number of the page against the references of
tools/figures/q0110.py (the same traces tests/0110/tb.sv checks against Verilator, whose
inputs and want strings are compared here too), the Verilator messages the page quotes
against a real run of the page's modules, the claims about what lint finds, the generated
blocks, and the box's models (explorer/rtlbug.js) under Node against the same references."""

import json
import random
import re
import shutil
import subprocess
import sys

import pytest

from extract_code import ROOT, blocks, pick, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0110  # noqa: E402
from q0110 import A_C, B_C, D_A, D_B, EN_B, N  # noqa: E402

TB = (ROOT / "tests" / "0110" / "tb.sv").read_text(encoding="utf-8")


def norm(text):
    """Text as read: no RLM, a no-break space as a space, every run of white space one space."""
    return re.sub(r"\s+", " ", text.replace("‏", "").replace(" ", " "))


PAGE = norm(question_path(110).read_text(encoding="utf-8"))


def on_page(*phrases):
    for p in phrases:
        assert norm(p) in PAGE, p


def he(ks):
    """A Hebrew list of numbers: "2, 3 ו-5"."""
    ks = [str(k) for k in ks]
    return ks[0] if len(ks) == 1 else f"{', '.join(ks[:-1])} ו-{ks[-1]}"


# --- the testbench draws what the figures draw ------------------------------------------------

def test_testbench_inputs_and_want_strings():
    arrays = {m[1]: [int(v) for v in m[2].split(",")] for m in re.finditer(r"int (\w+)\[N\]\s*=\s*'\{([^}]*)\};", TB)}
    assert arrays == {"D_A": D_A, "EN_B": EN_B, "D_B": D_B, "A_C": A_C, "B_C": B_C}
    assert re.search(r"localparam int N = (\d+);", TB)[1] == str(N)
    strings = {m[1]: m[2] for m in re.finditer(r'string (WANT_\w+) = "([^"]*)";', TB)}
    lists = {m[1]: re.findall(r'"([01]+)"', m[2]) for m in re.finditer(r"string (WANT_\w+)\[3\] = '\{([^}]*)\};", TB)}
    want = q0110.want_strings()
    assert {**strings, **lists} == want
    # the waveforms on the page are drawn from the same traces
    for blocking in (True, False):
        tr = q0110.delay_trace(D_A, blocking)
        assert ["".join(str(r[i]) for r in tr) for i in range(3)] == want["WANT_A_BUG" if blocking else "WANT_A_FIX"]


def test_references_meet_or_miss_the_intent():
    bug, fix = q0110.delay_trace(D_A, True), q0110.delay_trace(D_A)
    assert [r[2] for r in fix] == q0110.delay_want(D_A)
    assert all(r[0] == r[1] == r[2] for r in bug)
    assert q0110.gate_trace(EN_B, D_B) == q0110.gate_want(EN_B, D_B)
    assert all(q0110.avg(a, b) == q0110.avg_want(a, b) for a, b in zip(A_C, B_C))
    assert q0110.lost_pairs() == (32640, {128})


# --- part a ----------------------------------------------------------------------------------

def test_part_a_numbers():
    bug, fix, want = q0110.delay_trace(D_A, True), q0110.delay_trace(D_A), q0110.delay_want(D_A)
    rise_d, rise_want, rise_bug = D_A.index(1), want.index(1), [r[2] for r in bug].index(1)
    assert (rise_d, rise_want, rise_bug) == (1, 4, 2) and rise_want == rise_d + 3 and rise_bug == rise_d + 1
    on_page(f"הכניסה `d` עולה במחזור {rise_d}, ולכן `q3` היה צריך לעלות במחזור {rise_want}. הוא עולה כבר במחזור {rise_bug}")
    high_bug = [k for k, r in enumerate(bug) if r[2]]
    high_want = [k for k, v in enumerate(want) if v]
    assert high_bug == [2, 3, 5] and high_want == [4, 5, 7]
    on_page(f"`q3` גבוה במחזורים {he(high_bug)}, במקום {he(high_want)}")
    # the edge that opens cycle 2: d of cycle 1 is 1, every register 0; after it, with = all
    # three are 1, with <= only q1
    assert D_A[1] == 1 and bug[1] == fix[1] == (0, 0, 0)
    assert bug[2] == (1, 1, 1) and fix[2] == (1, 0, 0)
    on_page("נעקוב אחרי העלייה שפותחת את מחזור 2. לפניה `d = 1` (הערך של מחזור 1)",
            "במחזור 2 שלושתם 1", "ולכן במחזור 2 `q1` הוא 1, ו-`q2` ו-`q3` עדיין 0",
            "מכל מחזור \\( k \\ge 3 \\) `q3` הוא `d` של מחזור \\( k - 3 \\), ובמחזורים 0 עד 2 הוא עדיין 0")
    # the testbench runs the random cycles the page names, twice (parts a and b)
    assert TB.count("for (k = 0; k < 400; k++)") == 2
    on_page("הבדיקה מריצה 400 מחזורים אקראיים, ובכל אחד `q3` הוא `d` של שלושה מחזורים קודם")
    # the message of -Wall points at the three lines 9, 10, 11 of the module
    lines = pick(110, "systemverilog", "module delay3 (").splitlines()
    assert [lines[i - 1].strip() for i in (9, 10, 11)] == ["q1 = d;", "q2 = q1;", "q3 = q2;"]


# --- part b ----------------------------------------------------------------------------------

def test_part_b_numbers():
    bug, want = q0110.gate_trace(EN_B, D_B, False), q0110.gate_want(EN_B, D_B)
    assert bug[:3] == want[:3]
    wrong = [k for k in range(N) if bug[k] != want[k]]
    assert wrong == [3, 4, 6, 7]
    assert all(EN_B[k] == 0 for k in wrong)
    assert bug[3] == bug[4] == bug[2] == D_B[2] == 9 and want[3] == want[4] == 0
    assert bug[6] == bug[7] == bug[5] == D_B[5] == 6 and EN_B[2] == EN_B[5] == 1
    on_page("עד מחזור 2 הכול נכון. במחזורים 3 ו-4 `en` נמוך, אבל `y` נשאר 9 במקום 0, ובמחזורים 6 ו-7 הוא נשאר 6",
            "לכן `y` נשאר 9 ממחזור 2, ו-6 ממחזור 5",
            f"`y` שגוי במחזורים {he(wrong)}")
    assert EN_B[0] == 0 and bug[0] == 0
    assert EN_B[1] == EN_B[2] == 1 and (bug[1], bug[2]) == (5, 9)
    assert EN_B[3] == 0 and EN_B[4] == 0 and D_B[4] == 7 and bug[4] == 9
    assert EN_B[5] == 1 and bug[5] == 6
    on_page("במחזורים 1 ו-2 `en` גבוה, ו-`y` הוא `d` : קודם 5, ואז 9",
            "במחזור 4 `d` משתנה ל-7", "במחזור 5 `en` עולה ו-`y` הוא 6, ובמחזורים 6 ו-7 הוא נשאר 6")
    lines = pick(110, "systemverilog", "module en_gate (").splitlines()
    assert lines[5].strip() == "always_comb"          # line 6 of the LATCH message


# --- part c ----------------------------------------------------------------------------------

def test_part_c_numbers():
    a, b = A_C[2], B_C[2]
    assert (a, b, a + b) == (200, 100, 300) and q0110.avg(a, b, 8) == 22 and q0110.avg(a, b) == 150
    assert (a + b) - 256 == 44 == (a + b) % 256 and 44 >> 1 == 22
    on_page("במחזור 2, עם `a = 200` ו-`b = 100`, `avg` הוא 22 ולא 150",
            "\\( 300 - 256 = 44 \\), ו-`44 >> 1` הוא 22", "כמה ביטים צריך כדי לכתוב את 300?")
    assert (300).bit_length() == 9
    wrong = [k for k in range(N) if q0110.avg(A_C[k], B_C[k], 8) != q0110.avg_want(A_C[k], B_C[k])]
    assert wrong == [2, 4, 5, 6]
    assert all(q0110.avg_want(A_C[k], B_C[k]) - q0110.avg(A_C[k], B_C[k], 8) == 128 for k in wrong)
    assert all((A_C[k] + B_C[k] >= 256) == (k in wrong) for k in range(N))
    assert A_C[3] + B_C[3] == 255
    on_page(f"במחזורים {he(wrong)} `avg` קטן ב-128 בדיוק מהממוצע הנכון",
            "במחזור 3 הסכום 255, אין נשא, והתוצאה נכונה",
            "הנשא של `a + b` שווה 256, ואחרי ההזזה 128")
    assert 255 + 255 == 510 and (255 + 255) // 2 == 255
    wrong_pairs, diffs = q0110.lost_pairs()
    assert 256 * 256 == 65536 and wrong_pairs == 32640 and diffs == {128}
    assert sum(1 for x in range(256) for y in range(256) if x + y >= 256) == 32640
    on_page("\\( a + b \\le 510 \\)", "\\( \\lfloor (a + b) / 2 \\rfloor \\le 255 \\)",
            "הבדיקה עוברת על כל 65,536 הזוגות : התיקון נכון בכולם, והקוד המקורי שגוי ב-32,640 זוגות")
    lines = pick(110, "systemverilog", "module avg8_fixed").splitlines()
    assert lines[5].strip().startswith("assign avg = 8'(")   # line 6 of the WIDTHTRUNC message


def test_try_it_paragraph():
    # part c: cycle 3 is 127 + 128 = 255, no carry; with b = 129 the sum is 256
    a = A_C[3]
    assert a + B_C[3] == 255 and q0110.avg(a, B_C[3], 8) == q0110.avg(a, B_C[3]) == 127
    assert a + 129 == 256 and q0110.avg(a, 129, 8) == 0 and q0110.avg(a, 129) == 128
    on_page("עברו למחזור 3 (הסכום 255, בלי נשא) ושנו את `b` ל-129 : הסכום 256, הנשא נדלק, ו-`avg` יורד ל-0 בקוד המקורי ועולה ל-128 בתיקון")
    # part a: at the edge into cycle 2, q2 = q1 reads the new 1 with =, the old 0 with <=
    assert D_A[1] == 1 and q0110.delay_trace(D_A, True)[1][0] == 0 == q0110.delay_trace(D_A)[1][0]
    on_page("עמדו על מחזור 2 והחליפו בין הבאג לתיקון : עם `=` השורה `q2 = q1` קוראת את ה-1 החדש, ועם `<=` את ה-0 הישן")
    # part b: en high in cycle 3 too
    en = EN_B[:3] + [1] + EN_B[4:]
    bug = q0110.gate_trace(en, D_B, False)
    assert EN_B[3] == 0 and bug[3] == D_B[3] == 12 and bug[4] == 12 and en[4] == 0
    on_page("לחצו על `en` במחזור 3 : `y` מקבל 12, ובמחזור 4 ה-latch כבר שומר את ה-12")


def test_traps_and_follow_ups():
    # (a + b) / 2 in 32 bits, and with 8'd2 back in 8 bits; the testbench runs both in SV
    assert (200 + 100) // 2 == 150 and ((200 + 100) % 256) // 2 == 22
    assert "8'((x + y8) / 2) != 8'd150" in TB and "8'((x + y8) / 8'd2) != 8'd22" in TB
    on_page("הביטוי `(a + b) / 2` נותן 150 עבור 200 ו-100", "מי שיכתוב `8'd2` במקום 2 יחזיר את הבאג, ויקבל שוב 22")
    # the swap: equal after one edge with =, swapped with <=
    assert "ra != rb" in TB and "sa != 4'd9 || sb != 4'd3" in TB
    # $display of an 8-bit sum, the comparisons, and the signedness of the follow-ups
    assert (200 + 100) % 256 == 44 and 200 + 100 > 255 and not ((200 + 100) % 256 > 255)
    assert '$sformatf("%0d", x + y8) != "44"' in TB and "x + y8 > 8'd255" in TB
    on_page("ההדפסה נותנת 44")
    assert (-1) % 256 == 255 and not (255 < 5)
    on_page("`s` נקרא כ-255, ו-255 לא קטן מ-5")
    for check in ("if (i < n) fail", "if (s8 < n) fail", "if (!(i < int'(n))) fail", "if (!(s8 < 5)) fail"):
        assert check in TB
    # the reversed lines: the testbench runs them against the fix, cycle by cycle
    assert "//@page reversed:" in TB and "qr3 !== a_fix.q3" in TB


# --- the Verilator messages ----------------------------------------------------------------------

def lint(tmp_path, name, code, wall=False):
    path = tmp_path / f"{name}.sv"
    path.write_text(code, encoding="utf-8")
    run = subprocess.run(["verilator", "--lint-only", *(["-Wall"] if wall else []), f"{name}.sv"],
                         cwd=tmp_path, capture_output=True, text=True)
    return run.returncode, run.stdout + run.stderr


def quoted(word):
    """The page's text block that quotes a warning, its lines."""
    found = [b for b in blocks(110, "text") if f"%Warning-{word}:" in b]
    assert len(found) == 1, word
    return found[0].rstrip("\n").splitlines()


def test_verilator_messages(tmp_path):
    if not shutil.which("verilator"):
        pytest.skip("verilator is not installed")
    mod = lambda marker: pick(110, "systemverilog", marker)  # noqa: E731

    def same(lines, out):
        got = [line.rstrip() for line in out.splitlines()]
        for line in lines:
            assert line.rstrip() in got, (line, out)

    # part a: silent by default, BLKSEQ on lines 9, 10 and 11 with -Wall; the page quotes line 9
    rc, out = lint(tmp_path, "delay3", mod("module delay3 ("))
    assert rc == 0 and "%Warning" not in out
    rc, out = lint(tmp_path, "delay3", mod("module delay3 ("), wall=True)
    same(quoted("BLKSEQ"), out)
    assert [int(m) for m in re.findall(r"%Warning-BLKSEQ: delay3\.sv:(\d+):", out)] == [9, 10, 11]
    # part b: LATCH without -Wall
    rc, out = lint(tmp_path, "en_gate", mod("module en_gate ("))
    same(quoted("LATCH"), out)
    assert out.count("%Warning") == 1
    # part c: nothing, even with -Wall; without its cast the fix gets WIDTHTRUNC
    rc, out = lint(tmp_path, "avg8", mod("module avg8 ("), wall=True)
    assert rc == 0 and "%Warning" not in out
    fixed = mod("module avg8_fixed")
    nocast = re.sub(r"8'\((\(\{1'b0, a\} \+ b\) >> 1)\)", r"\1", fixed)
    assert nocast != fixed
    rc, out = lint(tmp_path, "avg8_fixed", nocast)
    same(quoted("WIDTHTRUNC"), out)
    # the fixes are clean, also with -Wall
    for marker, name in (("module delay3_fixed", "delay3_fixed"), ("module en_gate_fixed", "en_gate_fixed"),
                         ("module avg8_fixed", "avg8_fixed")):
        rc, out = lint(tmp_path, name, mod(marker), wall=True)
        assert rc == 0 and "%Warning" not in out, (name, out)
    # the trap: the reversed lines are silent by default, BLKSEQ with -Wall
    reversed_lines = mod("reversed:")
    shell = ("module rev (\n  input  logic clk,\n  input  logic d,\n  output logic q3\n);\n  logic q1, q2;\n"
             + reversed_lines + "endmodule\n")
    rc, out = lint(tmp_path, "rev", shell)
    assert rc == 0 and "%Warning" not in out
    rc, out = lint(tmp_path, "rev", shell, wall=True)
    assert out.count("%Warning-BLKSEQ") == 3
    # the follow-ups: a case without default gives CASEINCOMPLETE with an example and LATCH;
    # a + b > 8'd255 gives CMPCONST, without -Wall
    case = ("module dec (\n  input  logic [1:0] s,\n  output logic [3:0] y\n);\n  always_comb\n    case (s)\n"
            "      2'd0: y = 4'd1;\n      2'd1: y = 4'd2;\n      2'd2: y = 4'd4;\n    endcase\nendmodule\n")
    rc, out = lint(tmp_path, "dec", case)
    assert "%Warning-CASEINCOMPLETE" in out and "example pattern 0x3" in out and "%Warning-LATCH" in out
    cmp = "module cmp (\n  input  logic [7:0] a,\n  input  logic [7:0] b,\n  output logic big\n);\n  assign big = a + b > 8'd255;\nendmodule\n"
    rc, out = lint(tmp_path, "cmp", cmp)
    assert "%Warning-CMPCONST" in out and "Comparison is constant due to limited range" in out
    on_page('Verilator מזהיר CMPCONST, "Comparison is constant due to limited range"',
            "Verilator מזהיר CASEINCOMPLETE, עם דוגמה לערך חסר, וגם LATCH")


# --- the generated blocks and the box -----------------------------------------------------------

def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(110)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(110)
    cases = [(D_A, EN_B, D_B, A_C, B_C)]
    for _ in range(200):
        cases.append(([rng.randint(0, 1) for _ in range(N)], [rng.randint(0, 1) for _ in range(N)],
                      [rng.randint(0, 15) for _ in range(N)], [rng.randint(0, 255) for _ in range(N)],
                      [rng.randint(0, 255) for _ in range(N)]))
    script = (f"const m = {explorer_require()};"
              f"console.log(JSON.stringify({{page: m.rbPage, out: {json.dumps(cases)}.map(([dA, enB, dB, aC, bC]) => ["
              "m.rbDelay(dA, true), m.rbDelay(dA), m.rbDelayWant(dA),"
              f"Array.from({{length: {N - 1}}}, (_, i) => [m.rbEdge(dA, i + 1, true), m.rbEdge(dA, i + 1)]),"
              "m.rbGate(enB, dB, false), m.rbGate(enB, dB), m.rbGateWant(enB, dB), enB.map((_, k) => m.rbHeld(enB, k)),"
              "aC.map((a, k) => [m.rbAvg(a, bC[k], 8), m.rbAvg(a, bC[k]), m.rbAvgWant(a, bC[k]), m.rbSum(a, bC[k])]),"
              "m.rbDecode(m.rbEncode({dA, enB, dB, aC, bC, k: 5}))])}));")
    got = node_json(script)
    assert got["page"] == {"dA": D_A, "enB": EN_B, "dB": D_B, "aC": A_C, "bC": B_C}
    for (dA, enB, dB, aC, bC), (bug, fix, want, edges, gbug, gfix, gwant, held, avgs, back) in zip(cases, got["out"]):
        tb, tf = q0110.delay_trace(dA, True), q0110.delay_trace(dA)
        assert [tuple(r) for r in bug] == tb and [tuple(r) for r in fix] == tf and want == q0110.delay_want(dA)
        for k, (eb, ef) in enumerate(edges, start=1):
            x = dA[k - 1]
            # per line: the right-hand side before the edge, what the line reads (and writes)
            assert eb == [[x, x], [tb[k - 1][0], x], [tb[k - 1][1], x]] and [r[1] for r in eb] == list(tb[k])
            assert ef == [[x, x], [tf[k - 1][0], tf[k - 1][0]], [tf[k - 1][1], tf[k - 1][1]]] and [r[1] for r in ef] == list(tf[k])
        assert gbug == q0110.gate_trace(enB, dB, False) and gfix == q0110.gate_trace(enB, dB) and gwant == q0110.gate_want(enB, dB)
        for k, j in enumerate(held):
            assert gbug[k] == (dB[j] if j >= 0 else 0) and (j == -1 or (enB[j] and not any(enB[j + 1:k + 1])))
        for (a, b), (b8, b9, w, s) in zip(zip(aC, bC), avgs):
            assert (b8, b9, w) == (q0110.avg(a, b, 8), q0110.avg(a, b), q0110.avg_want(a, b))
            assert s == {"sum": a + b, "carry": (a + b) >> 8, "sum8": (a + b) % 256, "bug": b8, "fix": b9}
        assert back == {"dA": dA, "enB": enB, "dB": dB, "aC": aC, "bC": bC, "k": 5}
    bad = node_json(f"const m = {explorer_require()};"
                    "console.log(JSON.stringify(['', '0110100_01100100_3.5.9.12.7.6.10.1_1.1.1.1.1.1.1.1_1.1.1.1.1.1.1.1_0',"
                    " '01101000_01100100_3.5.9.12.7.6.10.16_1.1.1.1.1.1.1.1_1.1.1.1.1.1.1.1_0',"
                    " '01101000_01100100_3.5.9.12.7.6.10.1_1.1.1.1.1.1.1.256_1.1.1.1.1.1.1.1_0',"
                    " '01101000_01100100_3.5.9.12.7.6.10.1_1.1.1.1.1.1.1.1_1.1.1.1.1.1.1.1_8'].map((t) => m.rbDecode(t))));")
    assert bad == [None] * 5
