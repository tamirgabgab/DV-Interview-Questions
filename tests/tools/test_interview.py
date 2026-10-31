"""Interview mode and the quick jump (docs/javascripts/interview.js): the time target, the
series of the interview builder and the quick jump's matching, run under Node against
expectations computed here; and the question index the hook writes (questions.json)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from page_tests import node_json  # noqa: E402

LIB = json.dumps(str(ROOT / "docs" / "javascripts" / "interview.js"))

# a small index in the shape of questions.json's "qs"
QS = [
    ["0010", "סוגריים תקינים", "student", "easy", "code", ["מחסנית", "Python"], "questions/student/0010-x/", 2],
    ["0033", "עומק FIFO מקצבים ופרצים", "junior", "medium", "design", ["FIFO", "תכן דיגיטלי"], "questions/junior/0033-x/", 3],
    ["0034", "קוד Gray למצביעי FIFO אסינכרוני", "junior", "medium", "design", ["FIFO", "CDC"], "questions/junior/0034-x/", 4],
    ["0059", "מטבעות בשורה – לוקחים מהקצוות", "junior", "medium", "code", ["תכנות דינמי", "חידות היגיון"], "questions/junior/0059-x/", 5],
    ["0069", "עקיפות בזרם תשובות", "senior", "hard", "code", ["עץ פנוויק"], "questions/senior/0069-x/", 3],
    ["0031", "הגשר והפנס", "junior", "easy", "puzzle", ["חידות היגיון"], "questions/junior/0031-x/", 2],
]


def run(expr: str):
    return node_json(f"const I = require({LIB}); const QS = {json.dumps(QS, ensure_ascii=False)};"
                     f"process.stdout.write(JSON.stringify({expr}));")


def target(difficulty: str, parts: int) -> int:
    return {"easy": 10, "medium": 15, "hard": 25}[difficulty] + 3 * max(0, parts - 3)


def test_target_minutes():
    cases = [(d, p) for d in ("easy", "medium", "hard") for p in (0, 2, 3, 4, 7)]
    got = run("[" + ",".join(f"I.targetMinutes({json.dumps(d)}, {p})" for d, p in cases) + "]")
    assert got == [target(d, p) for d, p in cases]
    assert run('I.targetMinutes("unknown", "x")') == 15


def test_plan_fits_the_time_and_prefers_unsolved():
    for seed in range(1, 30):
        for minutes in (20, 40, 60):
            res = run(f'I.buildPlan(QS, {{level: "junior", minutes: {minutes}, kinds: ["code", "design", "puzzle"], solved: ["0031"], seed: {seed}}})')
            ids = [q[0] for q in res["plan"]]
            assert len(ids) == len(set(ids)) and ids
            assert all(q[2] == "junior" for q in res["plan"])
            used = sum(target(q[3], q[7]) for q in res["plan"])
            assert used == res["minutes"] and used <= minutes
            # the solved question comes only after every unsolved one that fits
            if "0031" in ids:
                left = minutes - used + target("easy", 2)
                assert all(q[0] in ids or target(q[3], q[7]) > left for q in QS if q[2] == "junior" and q[0] != "0031")
    # the same seed, the same series; the kinds filter applies
    a = run('I.buildPlan(QS, {level: "junior", minutes: 60, kinds: ["code", "design"], seed: 7})')
    b = run('I.buildPlan(QS, {level: "junior", minutes: 60, kinds: ["code", "design"], seed: 7})')
    assert a == b and all(q[4] in ("code", "design") for q in a["plan"])


def test_plan_never_empty_while_there_are_questions():
    res = run('I.buildPlan(QS, {level: "senior", minutes: 20, kinds: ["code"], seed: 3})')
    assert [q[0] for q in res["plan"]] == ["0069"] and res["minutes"] == 25
    assert run('I.buildPlan(QS, {level: "senior", minutes: 60, kinds: ["puzzle"], seed: 3})')["plan"] == []


def test_match():
    ids = lambda q: [r[0] for r in run(f"I.match(QS, {json.dumps(q, ensure_ascii=False)})")]  # noqa: E731
    assert ids("59") == ["0059"]                      # a number is an id, padded
    assert ids("0034")[0] == "0034"
    assert ids("3")[:1] == ["0033"] or "0033" in ids("3")
    assert ids("FIFO") == ["0033", "0034"]            # the title first, both match it
    assert ids("fifo") == ["0033", "0034"]
    assert ids("CDC") == ["0034"]                     # a topic name
    assert ids("חידות") == ["0031", "0059"]          # a topic word in two questions
    assert ids("מטבעות לוקחים") == ["0059"]           # every word, in any order
    assert ids("לוקחים-מהקצוות") == ["0059"]          # a dash is a space
    assert ids("") == [] and ids("   ") == []
    assert ids("שום דבר כזה") == []
    assert run("I.match(QS, 'FIFO', 1).length") == 1


def test_fmt():
    assert run("[I.fmt(0), I.fmt(59), I.fmt(61), I.fmt(3599), I.fmt(-4)]") == ["00:00", "00:59", "01:01", "59:59", "00:00"]


def test_part_heading_counts_parts():
    sys.path.insert(0, str(ROOT / "hooks"))
    import questions  # noqa: PLC0415
    body = (ROOT / "docs" / "questions" / "junior" / "0059-coins-in-a-row.md").read_text(encoding="utf-8")
    assert len(questions.PART_HEADING.findall(body)) == 5
