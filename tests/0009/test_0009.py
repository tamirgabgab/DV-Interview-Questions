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
