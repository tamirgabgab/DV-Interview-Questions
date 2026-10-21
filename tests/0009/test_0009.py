import subprocess
import sys
import re
import random

import pytest

from extract_code import load_python

ns = load_python(9)
N, MAX_OPENS, Room = ns["N"], ns["MAX_OPENS"], ns["Room"]

# The example on the page: one cycle of 11, plus cycles of 3 and 2
EXAMPLE = [0, 7, 11, 15, 16, 13, 2, 12, 14, 4, 5, 6, 3, 1, 8, 9, 10]


def partitions(n, largest=None):
    largest = largest or n
    if n == 0:
        yield []
        return
    for k in range(min(n, largest), 0, -1):
        for rest in partitions(n - k, k):
            yield [k] + rest


def from_cycle_lengths(lengths, rng):
    """A random arrangement of the notes whose cycles have the given lengths."""
    boxes = list(range(1, N + 1))
    rng.shuffle(boxes)
    notes = [0] * (N + 1)
    for length in lengths:
        cycle, boxes = boxes[:length], boxes[length:]
        for i, box in enumerate(cycle):
            notes[box] = cycle[(i + 1) % length]
    return notes


def random_notes(rng):
    notes = list(range(1, N + 1))
    rng.shuffle(notes)
    return [0] + notes


def check_game(notes):
    room = Room(notes)
    ns["helper"](room)
    assert room.swaps_left >= ns["MAX_SWAPS"] - 1          # one swap at most
    for me in range(1, N + 1):
        assert ns["find_my_note"](room, me), (notes, me)
    assert ns["play"](notes)


def test_page_example():
    assert sorted(len(ns["cycle_from"](EXAMPLE, b)) for b in (1, 2, 8)) == [2, 3, 11]
    room = Room(EXAMPLE)
    ns["helper"](room)
    after = room._notes
    assert after[1] == 4 and after[9] == 7
    assert sorted(len(ns["cycle_from"](after, b)) for b in (1, 7, 2, 8)) == [2, 3, 5, 6]
    check_game(EXAMPLE)


def test_every_cycle_structure():
    rng = random.Random(9)
    structures = list(partitions(N))
    assert len(structures) == 231
    for lengths in structures:
        check_game(from_cycle_lengths(lengths, rng))


def test_random_arrangements():
    rng = random.Random(90)
    for _ in range(20000):
        check_game(random_notes(rng))


def test_without_helper_about_one_third_win():
    rng = random.Random(900)
    wins = 0
    for _ in range(20000):
        room = Room(random_notes(rng))
        wins += all(ns["find_my_note"](room, me) for me in range(1, N + 1))
    assert abs(wins / 20000 - 0.3371) < 0.015


def test_room_enforces_the_rules():
    room = Room(EXAMPLE)
    for _ in range(ns["MAX_SWAPS"]):
        room.swap(1, 2)
    with pytest.raises(AssertionError):
        room.swap(1, 2)                                    # a fifth swap
    room.enter()
    with pytest.raises(AssertionError):
        room.look_all()                                    # person 0 is gone
    for _ in range(MAX_OPENS):
        room.open_box(1)
    with pytest.raises(AssertionError):
        room.open_box(1)                                   # a ninth box
    room.enter()
    room.open_box(1)                                       # the next person starts fresh


def test_figures_up_to_date():
    # The SVG figures and the step-through figure on the page are the output of tools/figures/q0009.py
    from extract_code import ROOT, question_path
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0009.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(9).read_text(encoding="utf-8")
    generated = [l.strip() for l in out.splitlines() if l.strip().startswith("<svg class=\"figure\" viewBox=\"0 0 640")]
    page = re.findall(r'<svg class="figure" viewBox="0 0 640.*?</svg>', text)
    assert page == generated and len(page) == 2
    assert re.findall(r'<div class="stepper".*?</div></div>', text) == re.findall(r'<div class="stepper".*?</div></div>', out)


def test_explorer_matches_page_code():
    """The boxes explorer: its cycles, person 0's cut and the walks against the page's
    cycle_from, helper and find_my_note on the example and random arrangements; the two
    closed-form rates against the page's test value and a simulation."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(99)
    arrangements = [EXAMPLE] + [random_notes(rng) for _ in range(60)]
    arrangements += [from_cycle_lengths(lengths, rng) for lengths in ([16], [9, 7], [8, 8], [10, 3, 3], [1] * 16)]
    got = node_json(f"""
      const m = {explorer_require()};
      const arr = {json.dumps(arrangements)};
      const rnd = (() => {{ let a = 7; return () => {{ a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }}; }})();   // mulberry32: exact in doubles
      let wins = 0, randWins = 0;
      for (let r = 0; r < 4000; r++) {{ const notes = m.permShuffle(16, rnd); wins += m.permAllWin(notes, 8); randWins += m.permRandomPicks(notes, 8, rnd); }}
      console.log(JSON.stringify({{
        cycles: arr.map((a) => m.permCycles(a)),
        cut: arr.map((a) => m.permHelper(a, 8)),
        walks: arr.map((a) => {{ const c = m.permHelper(a, 8); const n = c ? m.permSwap(a, c[0], c[1]) : a;
          return Array.from({{length: 16}}, (_, i) => m.permWalk(n, i + 1, 8)); }}),
        before: arr.map((a) => Array.from({{length: 16}}, (_, i) => m.permWalk(a, i + 1, 8).found)),
        pStrat: m.permStrategyProb(16, 8), pRand: m.permRandomProb(16, 8), wins, randWins,
        small: [4, 6, 8].map((n) => [m.permStrategyProb(n, n / 2), m.permRandomProb(n, n / 2)]),
      }}));""")
    for notes, cycles, cut, walks, before in zip(arrangements, got["cycles"], got["cut"], got["walks"], got["before"]):
        seen = set()
        for c in cycles:
            assert c == ns["cycle_from"](notes, c[0]) and c[0] == min(c) and not seen & set(c)
            seen.update(c)
        assert seen == set(range(1, N + 1))
        room = Room(notes)
        ns["helper"](room)
        after = room._notes
        if cut is None:
            assert after == notes and room.swaps_left == ns["MAX_SWAPS"]
        else:
            assert room.swaps_left == ns["MAX_SWAPS"] - 1
            a, b = cut
            assert after == notes[:a] + [notes[b]] + notes[a + 1:b] + [notes[a]] + notes[b + 1:]
        for me, walk in enumerate(walks, start=1):
            assert walk["found"] == ns["find_my_note"](room, me)
            # the boxes opened, replayed on the page's Room
            replay = Room(after)
            replay.enter()
            opened, box = [], me
            for _ in range(MAX_OPENS):
                opened.append(box)
                note = replay.open_box(box)
                if note == me:
                    break
                box = note
            assert walk["opened"] == opened
        plain = Room(notes)
        assert before == [ns["find_my_note"](plain, me) for me in range(1, N + 1)]
    assert abs(got["pStrat"] - 0.3371) < 1e-4 and got["pRand"] == 2 ** -16
    assert abs(got["wins"] / 4000 - got["pStrat"]) < 0.05
    assert got["randWins"] <= 3                     # expected 0.06 of 4000 rounds
    # small N: 1 - sum 1/k over the long lengths, and (1/2)^n
    want = [[1 - (1 / 3 + 1 / 4), 2 ** -4], [1 - (1 / 4 + 1 / 5 + 1 / 6), 2 ** -6], [1 - sum(1 / k for k in range(5, 9)), 2 ** -8]]
    for (a, b), (c, d) in zip(got["small"], want):
        assert abs(a - c) < 1e-12 and b == d
