#!/usr/bin/env python3
"""Figures of question 0018 (two hourglasses, measure D from time 0).

    python tools/figures/q0018.py > /tmp/q0018.html

Prints, in page order: the step-through figure of the plan for A = 7, B = 11, D = 15 (one
frame per event) and the four-way branching from the state t = 7, A = 0, B = 4. Paste them
into the page; tests/0018 checks that the page copies match.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hourglass import branches, event_frame  # noqa: E402
from stepper import stepper  # noqa: E402

A, B = 7, 11

# (t, what happened, (a, b) on arrival, action, (a, b) after, caption)
PLAN = [
    (0, "start", (0, 0), "flip A + B", (7, 11),
     "רגע 0: הופכים את שני השעונים. השעון הראשון שייגמר הוא A, בעוד 7 דקות."),
    (7, "A runs out", (0, 4), "flip A", (7, 4),
     "רגע 7: שעון A נגמר והופכים אותו מיד. בשעון B נשארו 4 דקות למעלה, והוא ייגמר ראשון."),
    (11, "B runs out", (3, 0), "flip A", (4, 0),
     "רגע 11: שעון B נגמר. בשעון A נשארו 3 דקות למעלה ו-4 למטה; ההיפוך מעלה את 4 הדקות."),
    (15, "A runs out", (0, 0), "✓ D = 15", None,
     "רגע 15: שעון A נגמר. עברו בדיוק 11 + 4 = 15 דקות מרגע 0."),
]


def main() -> None:
    frames = [(event_frame(A, B, t, event, before, action, after, f"רגע {t}: {event}"), caption)
              for t, event, before, action, after, caption in PLAN]
    print(stepper(frames, "התוכנית למדידת 15 דקות עם שעוני חול של 7 ו-11 דקות, אירוע אחרי אירוע"))
    print()
    print(branches(A, B, 7, 0, 4, [
        ("no flip", 4, (11, 0, 0), "seen ✗", "pruned"),
        ("flip A", 4, (11, 3, 0), "new ✓", "kept"),
        ("flip B", 7, (14, 0, 0), "seen ✗", "pruned"),
        ("flip A + B", 7, (14, 0, 0), "seen ✗", "pruned"),
    ], "ארבע האפשרויות מהמצב t = 7, A = 0, B = 4"))


if __name__ == "__main__":
    main()
