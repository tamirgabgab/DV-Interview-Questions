---
id: 0                    # next free running number (unique across all levels)
title: כותרת השאלה
level: student           # student | junior | senior  (must match the folder)
difficulty: easy         # easy | medium | hard
kind: puzzle             # puzzle | code | design | math | dv  (one; see CONTRIBUTING.md)
tags: [digital-logic]    # topic tags, see CONTRIBUTING.md
source: ""               # optional: company / interview round
added: YYYY-MM-DD
---

## השאלה

ניסוח מלא וברור של השאלה, כולל כל ההנחות והאילוצים. (No `#` heading here: the title
comes from the front matter and the hook renders the header card.)

??? interviewer "מה המראיין בודק"
    - **נקודה 1 :** what the interviewer is really testing, without revealing the answer.
    - **נקודה 2 :** ...

---

### סעיף א – שם הסעיף

(For multi-part questions use "### סעיף א", "### סעיף ב", ... each followed by its own
hints and collapsed solution. A single-part question skips the part heading.)

??? tip "רמז 1"
    רמז קל, כיוון כללי. (Hint 2 is shown only after hint 1 was opened.)

??? tip "רמז 2"
    רמז חזק יותר.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שורה אחת עם התוצאה הסופית.

    <!-- Cost chips under the short answer, required when the solution has a complexity block:
    a Hebrew label word and a value per chip, chips separated by " | ". -->

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    פסקה או שתיים : מה הרעיון המרכזי.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שם הצעד :** מה עושים.
    2. **שם הצעד :** מה עושים.

    </div>

    #### הקוד { .sol-code }

    <!-- Code is always given in both languages, as linked tabs. Non-trivial blocks get code
    annotations: a `// (1)!` / `# (1)!` marker at the end of a line and a numbered list
    right after the block. Use `title=` on every block, `linenums="1"` on long blocks and
    `hl_lines=` for the key lines. -->

    === "SystemVerilog"
        ```systemverilog title="function my_function" hl_lines="2"
        function automatic int my_function(int x);
          return x + 1;   // (1)!
        endfunction
        ```

        1. הסבר בעברית לשורה הזו.

    === "Python"
        ```python title="my_function"
        def my_function(x: int) -> int:
            return x + 1   # (1)!
        ```

        1. הסבר בעברית לשורה הזו.

    #### למה זה נכון { .sol-proof }

    הוכחה, טבלת מעקב או נימוק. דיאגרמות (Mermaid), דיאגרמות תזמון (WaveDrom), נוסחאות
    (\( LaTeX \)) לפי הצורך.

    #### סיבוכיות { .sol-cost }

    זמן וזיכרון, ולמה.

    (Keep the block order; drop blocks that do not apply, e.g. a puzzle has no code block.)

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : שם המלכודת"
    טעות נפוצה ואיך נמנעים ממנה.

??? followup "שאלות המשך"
    - **שאלה 1 :** ...
    - **שאלה 2 :** ...

<!--
If the question has code, also add tests/<id>/ (copy a similar question's folder):
  test_<id>.py  pytest tests of the page's Python blocks (load_python(<id>))
  tb.sv         Verilator testbench; pulls page code with //@page <text>
  demo.py       starting code of the in-browser "run" panel
Then run: python tools/run_tests.py <id>
-->
