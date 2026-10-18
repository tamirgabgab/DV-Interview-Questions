#!/usr/bin/env python3
"""Figure of question 0019 (two hourglasses, measure D between two moments).

    python tools/figures/q0019.py > /tmp/q0019.html

Prints the step-through figure of the plan for A = 7, B = 11, D = 1 (one frame per event;
the frames inside the measurement window are framed). Paste it into the page; tests/0019
checks that the page copy matches.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hourglass import event_frame  # noqa: E402
from stepper import stepper  # noqa: E402

A, B = 7, 11

# (t, what happened, (a, b) on arrival, action, (a, b) after, caption)
PLAN = [
    (0, "start", (0, 0), "flip A + B", (7, 11),
     "רגע 0: הופכים את שני השעונים."),
    (7, "A runs out", (0, 4), "flip A", (7, 4),
     "רגע 7: שעון A נגמר והופכים אותו. ריצה שנייה של A מתחילה."),
    (11, "B runs out", (3, 0), "flip B", (3, 11),
     "רגע 11: שעון B נגמר והופכים אותו. ריצה שנייה של B מתחילה; ב-A נשארו 3 דקות."),
    (14, "A runs out", (0, 8), "flip A", (7, 8),
     "רגע 14: שעון A נגמר והופכים אותו. ריצה שלישית של A מתחילה; ב-B נשארו 8 דקות."),
    (21, "A runs out", (0, 1), "START", (0, 1),
     "רגע 21: שעון A נגמר בפעם השלישית. ב-B נשארה בדיוק דקה אחת למעלה: מתחילים למדוד, לא הופכים כלום."),
    (22, "B runs out", (0, 0), "STOP ✓ 22 − 21 = 1", None,
     "רגע 22: שעון B נגמר בפעם השנייה. מסיימים: נמדדה דקה אחת."),
]


def main() -> None:
    frames = [(event_frame(A, B, t, event, before, action, after, f"רגע {t}: {event}", measuring=t >= 21), caption)
              for t, event, before, action, after, caption in PLAN]
    print(stepper(frames, "התוכנית למדידת דקה אחת עם שעוני חול של 7 ו-11 דקות: המדידה מרגע 21 עד רגע 22"))


if __name__ == "__main__":
    main()
