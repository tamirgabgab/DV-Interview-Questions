---
id: 0                    # next free running number (unique across all levels)
title: כותרת השאלה
level: student           # student | junior | senior | staff  (must match the folder)
difficulty: easy         # easy | medium | hard
tags: [digital-logic]    # topic tags, see README.md
source: ""               # optional: company / interview round
added: YYYY-MM-DD
---

## השאלה

ניסוח מלא וברור של השאלה, כולל כל ההנחות והאילוצים.
(For multi-part questions use "### סעיף א", "### סעיף ב", ... each followed by its own
collapsed solution.)

??? tip "רמז"
    כיוון לפתרון בלי לחשוף אותו.

## הפתרון

??? success "פתרון"
    הסבר שלב אחר שלב. דיאגרמות (Mermaid), דיאגרמות תזמון (WaveDrom), נוסחאות (\( LaTeX \))
    לפי הצורך.

    Code is always given in both languages, as linked tabs:

    === "SystemVerilog"
        ```systemverilog
        // ...
        ```

    === "Python"
        ```python
        # ...
        ```

## נקודות חשובות ושאלות המשך

??? note "נקודות חשובות"
    - מה המראיין באמת בודק.
    - טעויות נפוצות.
    - שאלות המשך צפויות.

<!--
If the question has code, also add tests/<id>/ (copy a similar question's folder):
  test_<id>.py  pytest tests of the page's Python blocks (load_python(<id>))
  tb.sv         Verilator testbench; pulls page code with //@page <text>
  demo.py       starting code of the in-browser "run" panel
Then run: python tools/run_tests.py <id>
-->
