---
id: 56
title: חלוקה ב-3 בחלון של L ביטים – שרשור ל-LSB, שרשור ל-MSB ובכל בסיס
level: junior
difficulty: medium
kind: design
tags: [fsm, digital-logic, math, systemverilog, python]
source: "המשך של 0055 : אותה מכונה, אבל המספר הוא רק חלון של L הספרות האחרונות"
added: 2026-10-28
---

## השאלה

כמו ב-[שאלה 0055](0055-divisible-by-m-fsm.md), לרכיב נכנס ביט אחד בכל מחזור, `din`, והיציאה
`div` אומרת אם המספר מתחלק ב-3. ההבדל : המספר הוא לא כל מה שנקרא, אלא רק **חלון** של
‏\( L \) הביטים האחרונים. כשנכנס ביט חדש, הביט הוותיק ביותר יוצא מהחלון. אחרי reset החלון
מלא באפסים.

- **סעיף א – שרשור ל-LSB :** הביט החדש נכנס מימין, כביט הנמוך, והביט השמאלי יוצא. בחלון
  של 3 ביטים, ‏`011` ואחריו 1 הוא `111` ולא `0111`. תכננו את הרכיב. כמה מצבים צריך?
- **סעיף ב – שרשור ל-MSB :** הביט החדש נכנס משמאל, כביט הגבוה, והביט הימני יוצא. ‏`011`
  ואחריו 1 הוא `101` ולא `1011`.
- **סעיף ג – כל m וכל בסיס :** חלוקה ב-\( m \), כשבכל מחזור נכנסת ספרה בבסיס \( B \), חלון
  של \( L \) ספרות, וערך התחלתי כלשהו לחלון. כתבו מודול אחד עם פרמטרים לשני הכיוונים.

??? interviewer "מה המראיין בודק"
    - **מה השתנה :** האם המועמד רואה שהשארית לבדה כבר לא מספיקה, כי צריך לדעת מה יוצא
      מהחלון.
    - **עדכון במקום חישוב מחדש :** האם הוא מוצא שהשארית מתעדכנת בצעד קבוע, בלי לחשב את
      החלון כולו מודולו 3 בכל מחזור.
    - **מינימליות :** כמה זיכרון באמת צריך, והאם אפשר לעשות את זה בפחות מ-\( L \) ביטים.
    - **הכיוון השני :** מה ההבדל בין שני הכיוונים, ואיפה נדרש ש-\( B \) יהיה הפיך מודולו
      \( m \).

---

### סעיף א – שרשור ל-LSB

??? tip "רמז 1"
    ב-0055 המצב היה השארית, והביט החדש הפך את המספר ל-\( 2v + b \). מה קורה כאן לביט
    השמאלי של \( 2v + b \)?

??? tip "רמז 2"
    הביט שיוצא היה שווה \( 2^{L-1} \), ואחרי ההזזה הוא שווה \( 2^L \). כדי להוריד אותו
    מהשארית צריך לדעת מהו, ולכן צריך לזכור את החלון עצמו.

<div class="selfcheck" data-answer="2" data-show="2" data-hint="החלון עובר 001, 011, 110 ואז 101. ‏101 בבינארי הוא 5, והשארית של 5 ב-3 היא 2." markdown>
חלון של 3 ביטים מתחיל ב-`000`, ונכנסים מימין הביטים 1, 1, 0, 1. מה השארית של החלון ב-3 בסוף?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שומרים את החלון ברגיסטר הזזה של \( L \) ביטים, ולידו את השארית \( r \) שלו. ביט
        \( b \) נכנס מימין, הביט \( out \) יוצא משמאל, ו-\( r' = (2r + b - 2^L \cdot out) \bmod 3 \).
        ‏`div` דולק כש-\( r = 0 \). כל מכונה צריכה לפחות \( L \) ביטים של זיכרון, ולכן רגיסטר
        ההזזה הוא לא בזבוז.

    <!-- cost: זיכרון \( L + 2 \) ביטים | עדכון קבוע לכל ביט | מצבים לפחות \( 2^{L-2} \) -->

    #### הרעיון { .sol-idea }

    **מה כבר לא מספיק.** ב-0055 המצב היה השארית. כאן, כשנכנס ביט, החלון הופך ל-\( 2w + b \)
    בלי הביט השמאלי, שעכשיו שווה \( 2^L \) :
    ‏\( w' = 2w + b - 2^L \cdot out \), כאשר \( out \) הוא הביט הגבוה של \( w \). את \( out \)
    אי אפשר לנחש מהשארית, ולכן צריך לזכור את החלון.

    **המכונה הישירה.** מצב לכל חלון : ‏\( 2^L \) מצבים, ומעבר לכל ביט. בחלון של שני ביטים
    יש ארבעה מצבים, ו-`00` ו-`11` (‏0 ו-3) מתחלקים :

    <!-- gen 0 -->

    <svg class="figure dv-fig" viewBox="0 0 360 272" style="max-width:24rem" role="img" aria-label="המכונה הישירה של חלון של 2 ביטים, ביט חדש נכנס כ-LSB : מצב לכל חלון, 00 ו-11 מתחלקים ב-3"><defs><marker id="wf-arrow-l2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs><path class="fs-edge" d="M165.6,54.8 C158,14 202,14 194.4,54.8" marker-end="url(#wf-arrow-l2)"><title>00 --0--> 00</title></path><text class="fs-label halo" x="180" y="18" text-anchor="middle">0</text><path class="fs-edge is-found" d="M202.4,82.7 Q246.2,99.8 262.6,141.8" marker-end="url(#wf-arrow-l2)"><title>00 --1--> 01</title></path><text class="fs-label halo is-found" x="247.1" y="102.2" text-anchor="middle">1</text><path class="fs-edge" d="M263.3,188.4 Q246.2,232.2 204.2,248.6" marker-end="url(#wf-arrow-l2)"><title>01 --0--> 10</title></path><text class="fs-label halo" x="247.8" y="237.1" text-anchor="middle">0</text><path class="fs-edge is-found" d="M250,175.7 Q180,206.5 111.8,176.5" marker-end="url(#wf-arrow-l2)"><title>01 --1--> 11</title></path><text class="fs-label halo is-found" x="180.5" y="206.3" text-anchor="middle">1</text><path class="fs-edge" d="M170.3,236 Q139.5,166 169.5,97.8" marker-end="url(#wf-arrow-l2)"><title>10 --0--> 00</title></path><text class="fs-label halo" x="143.7" y="170.5" text-anchor="middle">0</text><path class="fs-edge is-found" d="M188.7,235.6 Q205.8,191.8 247.8,175.4" marker-end="url(#wf-arrow-l2)"><title>10 --1--> 01</title></path><text class="fs-label halo is-found" x="204.2" y="194.9" text-anchor="middle">1</text><path class="fs-edge" d="M110.4,174.7 Q154.2,191.8 170.6,233.8" marker-end="url(#wf-arrow-l2)"><title>11 --0--> 10</title></path><text class="fs-label halo" x="155.1" y="194.2" text-anchor="middle">0</text><path class="fs-edge is-found" d="M68.8,180.4 C28,188 28,144 68.8,151.6" marker-end="url(#wf-arrow-l2)"><title>11 --1--> 11</title></path><text class="fs-label halo is-found" x="28" y="170" text-anchor="middle">1</text><g class="fs-node is-start"><circle cx="180" cy="74" r="24"/><circle cx="180" cy="74" r="19"/><text x="180" y="79" text-anchor="middle">00</text></g><g class="fs-node"><circle cx="272" cy="166" r="24"/><text x="272" y="171" text-anchor="middle">01</text></g><g class="fs-node"><circle cx="180" cy="258" r="24"/><text x="180" y="263" text-anchor="middle">10</text></g><g class="fs-node is-start"><circle cx="88" cy="166" r="24"/><circle cx="88" cy="166" r="19"/><text x="88" y="171" text-anchor="middle">11</text></g></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="fs-key"></i>הביט 0</span><span><i class="fs-key-found"></i>הביט 1</span><span><i class="dv-key-acc"></i>עיגול כפול : החלון מתחלק ב-3</span></span>

    <!-- /gen -->

    **בחומרה.** המכונה הישירה היא בדיוק רגיסטר הזזה של \( L \) ביטים. אפשר לחשב בכל מחזור
    את `w % 3` מכל הביטים, אבל זה עץ של לוגיקה שגדל עם \( L \). במקום זה שומרים גם את
    השארית, ומעדכנים אותה מהביט שנכנס ומהביט שיוצא בלבד :
    ‏\( r' = (2r + b - 2^L \cdot out) \bmod 3 \). ‏\( 2^L \bmod 3 \) הוא קבוע : 1 כש-\( L \)
    זוגי ו-2 כש-\( L \) אי-זוגי.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המצב :** החלון \( w \) (‏\( L \) ביטים) והשארית \( r = w \bmod 3 \) (שני ביטים). אחרי
       reset ‏\( w = 0 \) ו-\( r = 0 \).
    2. **ההזזה :** ‏\( out = w[L-1] \), ו-\( w' = \{w[L-2:0], b\} \).
    3. **השארית :** ‏\( r' = (2r + b - C \cdot out) \bmod 3 \), כאשר \( C = 2^L \bmod 3 \).
    4. **היציאה :** ‏`div = (r == 0)`.
    5. **דוגמה :** ‏\( L = 3 \), ‏\( C = 2 \), והביטים 1, 1, 0, 1 :

    </div>

    <!-- gen 2 -->

    | הביט שנכנס | הביט שיוצא | החלון | ‏\( r' = (2r + b - 2^L out) \bmod 3 \) | מתחלק |
    |:-:|:-:|:-:|:-:|:-:|
    | אחרי reset | אין | ‏`000` | ‏0 | ✓ |
    | ‏1 | ‏0 | ‏`001` | <span dir="ltr">(2·0 + 1 − 2·0) mod 3 = 1</span> | ✗ |
    | ‏1 | ‏0 | ‏`011` | <span dir="ltr">(2·1 + 1 − 2·0) mod 3 = 0</span> | ✓ |
    | ‏0 | ‏0 | ‏`110` | <span dir="ltr">(2·0 + 0 − 2·0) mod 3 = 0</span> | ✓ |
    | ‏1 | ‏1 | ‏`101` | <span dir="ltr">(2·0 + 1 − 2·1) mod 3 = 2</span> | ✗ |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="win3_lsb" linenums="1" hl_lines="8 9"
        def win3_lsb(bits: list[int], L: int, init: int = 0) -> list[bool]:
            """A window of the last L bits, each new bit entering as its LSB: after each bit,
            is the window divisible by 3?"""
            w, r, out = init, init % 3, []
            c = pow(2, L, 3)                           # what the bit that leaves weighs, mod 3
            for b in bits:
                top = w >> (L - 1)                     # the bit that leaves
                w = (w << 1 | b) & ((1 << L) - 1)
                r = (2 * r + b - c * top) % 3          # (1)!
                out.append(r == 0)
            return out
        ```

        1. השארית בלי לקרוא את החלון : מה שנכנס, פחות מה שיצא. ב-Python ‏`%` תמיד מחזיר 0 עד 2.

    === "SystemVerilog"
        ```systemverilog title="module win3_lsb" linenums="1" hl_lines="18 19"
        // a window of the last L bits, a new bit entering as its LSB: is the window divisible by 3?
        module win3_lsb #(
          parameter int L = 8,
          parameter logic [L-1:0] INIT = '0      // the window after reset
        ) (
          input  logic clk, rst_n,
          input  logic din,               // the next bit: the window's new lowest bit
          output logic div                // the window is divisible by 3
        );
          localparam int C = (L % 2 == 0) ? 1 : 2;   // 2^L mod 3: what the bit that leaves weighs
          logic [L-1:0] w;                // the window, w[L-1] the oldest bit
          logic [1:0]   r;                // w mod 3, kept without reading w
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin
              w <= INIT;
              r <= 2'(INIT % 3);
            end else begin
              w <= L'({w, din});                                 // (1)!
              r <= 2'((2 * r + din + 3 * C - C * w[L-1]) % 3);   // (2)!
            end
          assign div = (r == 2'd0);
        endmodule
        ```

        1. ‏`{w, din}` הוא \( L + 1 \) ביטים, וההמרה ל-\( L \) ביטים זורקת את הביט השמאלי, הביט שיוצא.
        2. ‏\( 2w + b - 2^L \cdot out \) מודולו 3. ‏\( 3C \) שומר את הביטוי חיובי, ואינו משנה את השארית.

    #### למה זה נכון { .sol-proof }

    **השארית נכונה.** באינדוקציה : אחרי reset ‏\( r = w \bmod 3 \). החלון החדש הוא
    \( w' = 2w + b - 2^L \cdot out \), ולכן \( w' \equiv 2r + b - C \cdot out \pmod 3 \) : זה \( r' \).

    **צריך לזכור כמעט את כל החלון.** קחו שני חלונות שנבדלים באחד מ-\( L - 2 \) הביטים
    הנמוכים, ונניח שהביט הנמוך ביותר שבו הם נבדלים הוא במקום \( i \). אחרי \( j = L - 1 - i \ge 2 \)
    ביטים נוספים, החלון הוא \( a \cdot 2^j + u \), כאשר \( a \) הם \( i + 1 \) הביטים
    הנמוכים של החלון הישן ו-\( u \) הביטים החדשים. ‏\( u \) יכול להיות כל שארית (‏\( 2^j \ge 4 \)),
    ולכן יש \( u \) שבו חלון אחד מתחלק והשני לא, אם השאריות של \( a \) שונות. והן שונות :
    הן נבדלות ב-\( 2^i \), שאינו מתחלק ב-3. לכן כל \( 2^{L-2} \) הצירופים של הביטים הנמוכים
    הם מצבים שונים.

    **כמה מצבים בדיוק.** הטבלה סופרת את המצבים של המכונה הקטנה ביותר : המכונה הישירה
    נבנתה ומוזערה. בכל שורה מ-\( L = 3 \) יש יותר מ-\( 2^{L-1} \) מצבים, ולכן כל מכונה צריכה לפחות
    \( L \) ביטים של זיכרון, בדיוק כמו רגיסטר ההזזה :

    <!-- gen 3 -->

    | ‏L | החלונות ‏\( 2^L \) | שרשור ל-LSB | שרשור ל-MSB | חסם תחתון ‏\( 2^{L-2} \) |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏1 | ‏2 | ‏2 | ‏2 | ‏1 |
    | ‏2 | ‏4 | ‏4 | ‏4 | ‏1 |
    | ‏3 | ‏8 | ‏7 | ‏7 | ‏2 |
    | ‏4 | ‏16 | ‏14 | ‏14 | ‏4 |
    | ‏5 | ‏32 | ‏27 | ‏27 | ‏8 |
    | ‏6 | ‏64 | ‏54 | ‏54 | ‏16 |
    | ‏7 | ‏128 | ‏107 | ‏107 | ‏32 |
    | ‏8 | ‏256 | ‏214 | ‏214 | ‏64 |

    <!-- /gen -->

---

### סעיף ב – שרשור ל-MSB

עכשיו הביט החדש נכנס משמאל, והביט הימני יוצא : ‏\( w' = 2^{L-1} b + \lfloor w / 2 \rfloor \).
מה צריך לשנות?

??? tip "רמז 1"
    כאן יוצא הביט הנמוך, \( out = w[0] \), והביט החדש שווה \( 2^{L-1} \). מה הקשר בין
    \( \lfloor w / 2 \rfloor \) לשארית של \( w \)?

??? tip "רמז 2"
    ‏\( \lfloor w / 2 \rfloor = (w - out) / 2 \), ומודולו 3 חילוק ב-2 הוא כפל ב-2, כי
    \( 2 \cdot 2 = 4 \equiv 1 \).

<div class="selfcheck" data-answer="6" data-show="6" data-hint="החלון עובר 100, 010, 101 ואז 110. ‏110 בבינארי הוא 6, וזה מתחלק ב-3." markdown>
חלון של 3 ביטים מתחיל ב-`000`, ונכנסים משמאל הביטים 1, 0, 1, 1. מה הערך של החלון בסוף?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        אותו רגיסטר הזזה בכיוון השני ואותה שארית. ‏\( out = w[0] \) יוצא, ו-
        ‏\( r' = (2(r - out) + 2^{L-1} b) \bmod 3 \), כי \( 2^{-1} \equiv 2 \pmod 3 \). אותו
        מספר מצבים כמו בסעיף א.

    <!-- cost: זיכרון \( L + 2 \) ביטים | עדכון קבוע לכל ביט | מצבים כמו בסעיף א -->

    #### הרעיון { .sol-idea }

    **הביט שיוצא.** ‏\( \lfloor w / 2 \rfloor = (w - out) / 2 \), כאשר \( out \) הוא הביט
    הנמוך. ‏\( w - out \) זוגי, ומודולו 3 חילוק ב-2 הוא כפל ב-\( 2^{-1} = 2 \). לכן
    \( \lfloor w / 2 \rfloor \equiv 2(r - out) \pmod 3 \).

    **הביט שנכנס.** הוא שווה \( 2^{L-1} \), ומודולו 3 זה קבוע : 1 כש-\( L \) אי-זוגי ו-2
    כש-\( L \) זוגי. יחד : ‏\( r' = (2(r - out) + T \cdot b) \bmod 3 \), כאשר \( T = 2^{L-1} \bmod 3 \).

    **כמה מצבים.** בטבלה של סעיף א, המספרים בשני הכיוונים שווים. ההוכחה היא אותה הוכחה
    במראה : הפעם הביטים הגבוהים קובעים את העתיד, וחילוק ב-\( 2^j \) מחליף את הכפל.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המצב :** החלון \( w \) והשארית \( r \), כמו בסעיף א.
    2. **ההזזה :** ‏\( out = w[0] \), ו-\( w' = \{b, w[L-1:1]\} \).
    3. **השארית :** ‏\( r' = (2(r - out) + T \cdot b) \bmod 3 \), ‏\( T = 2^{L-1} \bmod 3 \).
    4. **היציאה :** ‏`div = (r == 0)`.
    5. **דוגמה :** ‏\( L = 3 \), ‏\( T = 1 \), והביטים 1, 0, 1, 1 :

    </div>

    <!-- gen 4 -->

    | הביט שנכנס | הביט שיוצא | החלון | ‏\( r' = (2(r - out) + 2^{L-1} b) \bmod 3 \) | מתחלק |
    |:-:|:-:|:-:|:-:|:-:|
    | אחרי reset | אין | ‏`000` | ‏0 | ✓ |
    | ‏1 | ‏0 | ‏`100` | <span dir="ltr">(2·(0 − 0) + 1·1) mod 3 = 1</span> | ✗ |
    | ‏0 | ‏0 | ‏`010` | <span dir="ltr">(2·(1 − 0) + 1·0) mod 3 = 2</span> | ✗ |
    | ‏1 | ‏0 | ‏`101` | <span dir="ltr">(2·(2 − 0) + 1·1) mod 3 = 2</span> | ✗ |
    | ‏1 | ‏1 | ‏`110` | <span dir="ltr">(2·(2 − 1) + 1·1) mod 3 = 0</span> | ✓ |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="win3_msb" linenums="1" hl_lines="8 9"
        def win3_msb(bits: list[int], L: int, init: int = 0) -> list[bool]:
            """A window of the last L bits, each new bit entering as its MSB: after each bit,
            is the window divisible by 3?"""
            w, r, out = init, init % 3, []
            t = pow(2, L - 1, 3)                       # what the bit that enters weighs, mod 3
            for b in bits:
                low = w & 1                            # the bit that leaves
                w = b << (L - 1) | w >> 1
                r = (2 * (r - low) + t * b) % 3        # (1)!
                out.append(r == 0)
            return out
        ```

        1. ‏\( \lfloor w / 2 \rfloor = (w - low) / 2 \), ומודולו 3 חילוק ב-2 הוא כפל ב-2.

    === "SystemVerilog"
        ```systemverilog title="module win3_msb" linenums="1" hl_lines="18 19"
        // a window of the last L bits, a new bit entering as its MSB: is the window divisible by 3?
        module win3_msb #(
          parameter int L = 8,
          parameter logic [L-1:0] INIT = '0      // the window after reset
        ) (
          input  logic clk, rst_n,
          input  logic din,               // the next bit: the window's new highest bit
          output logic div                // the window is divisible by 3
        );
          localparam int T = (L % 2 == 1) ? 1 : 2;   // 2^(L-1) mod 3: what the bit that enters weighs
          logic [L-1:0] w;                // the window, w[0] the oldest bit
          logic [1:0]   r;                // w mod 3
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin
              w <= INIT;
              r <= 2'(INIT % 3);
            end else begin
              w <= L'({din, w} >> 1);                            // (1)!
              r <= 2'((2 * (r + 3 - w[0]) + T * din) % 3);       // (2)!
            end
          assign div = (r == 2'd0);
        endmodule
        ```

        1. ‏`{din, w} >> 1` שם את `din` במקום \( L - 1 \) וזורק את `w[0]`, הביט שיוצא.
        2. ‏\( (w - out) / 2 \equiv 2(r - out) \), כי \( 2^{-1} = 2 \) מודולו 3. ה-3 שומר את הביטוי חיובי.

    #### למה זה נכון { .sol-proof }

    **השארית נכונה.** ‏\( w' = 2^{L-1} b + (w - out) / 2 \). ‏\( 2 \cdot 2 \equiv 1 \pmod 3 \),
    ולכן \( (w - out) / 2 \equiv 2(w - out) \equiv 2(r - out) \), ו-\( w' \equiv r' \).

    **ההבדל מסעיף א.** בסעיף א לא חילקנו בכלום, ולכן הנוסחה עובדת לכל \( m \). כאן חילקנו
    ב-2, וזה עובד רק כש-2 הפיך מודולו \( m \), כלומר \( m \) אי-זוגי. זה חוזר בסעיף ג.

---

### סעיף ג – כל m, כל בסיס, כל L וחלון התחלתי

עכשיו בכל מחזור נכנסת ספרה \( d \) בבסיס \( B \), החלון הוא \( L \) ספרות, ואחרי reset
החלון הוא ערך \( INIT \) כלשהו. השאלה היא חלוקה ב-\( m \), כאשר בשרשור ל-MSB ‏\( m \)
ו-\( B \) זרים. מה המעברים, ואילו קבועים צריך?

??? tip "רמז 1"
    בשרשור ל-LSB : ‏\( w' = Bw + d - B^L \cdot out \). בשרשור ל-MSB :
    ‏\( w' = B^{L-1} d + (w - out) / B \).

??? tip "רמז 2"
    כל החזקות של \( B \) הן קבועים מודולו \( m \), וגם \( B^{-1} \) הוא קבוע. הם מחושבים
    פעם אחת, ב-elaboration.

<div class="selfcheck" data-answer="4" data-show="4" data-hint="10000 = 7 · 1428 + 4. ‏10 בחזקת 4 מודולו 7 : ‏10 ≡ 3, ‏3² = 9 ≡ 2, ‏2² = 4." markdown>
חלון של 4 ספרות עשרוניות, חלוקה ב-7, ספרה חדשה נכנסת כ-LSB. בכמה מכפילים את הספרה שיוצאת
לפני שמחסירים אותה? (מספר בין 0 ל-6.)
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        חלון של \( L \) ספרות ושארית \( r \). בשרשור ל-LSB :
        ‏\( r' = (Br + d - C_L \cdot out) \bmod m \), ‏\( C_L = B^L \bmod m \), לכל \( m \). בשרשור
        ל-MSB : ‏\( r' = ((r - out) \cdot B^{-1} + C_H \cdot d) \bmod m \),
        ‏\( C_H = B^{L-1} \bmod m \), כש-\( B \) ו-\( m \) זרים. אחרי reset ‏\( r = INIT \bmod m \).

    <!-- cost: זיכרון \( L \lceil \log_2 B \rceil + \lceil \log_2 m \rceil \) ביטים | עדכון כפל וחיבור אחד מודולו \( m \) -->

    #### הרעיון { .sol-idea }

    **שני הכיוונים.** סעיפים א ו-ב לא השתמשו בשום דבר מיוחד ל-3 או ל-2 : בשרשור ל-LSB
    הספרה שיוצאת מוכפלת ב-\( B^L \) ומוחסרת, ובשרשור ל-MSB מחסירים אותה ומחלקים ב-\( B \),
    כלומר כופלים ב-\( B^{-1} \). כל השאר קבועים מודולו \( m \) :

    <!-- gen 5 -->

    | הבסיס B | ‏L | ‏m | ‏\( B^L \bmod m \) (LSB) | ‏\( B^{L-1} \bmod m \) (MSB) | ‏\( B^{-1} \bmod m \) (MSB) |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏2 | ‏8 | ‏3 | ‏1 | ‏2 | ‏2 |
    | ‏2 | ‏8 | ‏7 | ‏4 | ‏2 | ‏4 |
    | ‏8 | ‏3 | ‏7 | ‏1 | ‏1 | ‏1 |
    | ‏16 | ‏2 | ‏5 | ‏1 | ‏1 | ‏1 |
    | ‏10 | ‏3 | ‏3 | ‏1 | ‏1 | ‏1 |
    | ‏10 | ‏4 | ‏7 | ‏4 | ‏6 | ‏5 |

    <!-- /gen -->

    **חלון התחלתי.** אחרי reset החלון הוא \( INIT \), והשארית היא \( INIT \bmod m \),
    שגם היא קבוע. מכאן אותם עדכונים.

    **‏k ביטים במחזור.** כמו ב-0055, ‏\( k \) ביטים יחד הם ספרה בבסיס \( 2^k \). החלון הוא
    \( L \) ספרות, כלומר \( kL \) ביטים, ורק הקבועים משתנים.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="win_div" linenums="1" hl_lines="13 17"
        def win_div(digits: list[int], m: int, base: int = 2, L: int = 8,
                    msb: bool = False, init: int = 0) -> list[bool]:
            """A window of the last L base-`base` digits, starting as init: after each digit, is
            the window divisible by m? msb=False: a digit enters as the lowest and the highest
            leaves; msb=True: it enters as the highest and the lowest leaves (gcd(base, m) = 1)."""
            cl, ch = pow(base, L, m), pow(base, L - 1, m)
            inv = pow(base, -1, m) if msb else 0
            w, r, out = init, init % m, []
            for d in digits:
                if msb:
                    low = w % base                     # the digit that leaves
                    w = d * base ** (L - 1) + w // base
                    r = ((r - low) * inv + ch * d) % m   # (1)!
                else:
                    top = w // base ** (L - 1)         # the digit that leaves
                    w = (w * base + d) % base ** L
                    r = (r * base + d - cl * top) % m    # (2)!
                out.append(r == 0)
            return out
        ```

        1. ‏\( \lfloor w / B \rfloor = (w - low) / B \), ומודולו \( m \) חילוק ב-\( B \) הוא כפל ב-\( B^{-1} \).
        2. הספרה שיוצאת שווה \( B^L \) אחרי ההזזה, ומודולו \( m \) זה \( C_L \).

    === "SystemVerilog"
        ```systemverilog title="module win_div" linenums="1" hl_lines="39 43"
        // divisible by M over a window of the last L base-B digits; MSB = 0: a digit enters as the
        // window's lowest digit and the highest leaves, MSB = 1: as its highest (gcd(B, M) = 1)
        module win_div #(
          parameter int     M    = 7,
          parameter int     B    = 10,
          parameter int     L    = 4,
          parameter bit     MSB  = 0,
          parameter longint INIT = 0      // the window's value after reset, below B**L
        ) (
          input  logic clk, rst_n,
          input  logic [$clog2(B)-1:0] d, // the next digit, 0 to B-1
          output logic div
        );
          localparam int W = $clog2(M), DW = $clog2(B);
          function automatic int pw(int e);               // B**e mod M
            int p = 1 % M;
            for (int i = 0; i < e; i++) p = p * B % M;
            return p;
          endfunction
          function automatic int inverse(int b, int m);   // b^-1 mod m
            for (int y = 0; y < m; y++) if (b * y % m == 1 % m) return y;
            return 0;
          endfunction
          function automatic logic [DW-1:0] digit(int i); // digit i of INIT, 0 the lowest
            longint v = INIT;
            for (int j = 0; j < i; j++) v = v / B;
            return DW'(v % B);
          endfunction
          localparam int CL = pw(L), CH = pw(L - 1), BINV = inverse(B % M, M);
          logic [DW-1:0] w [L];           // the window's digits, w[0] the lowest
          logic [W-1:0]  r;               // the window's value mod M
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin
              for (int i = 0; i < L; i++) w[i] <= digit(i);
              r <= W'(INIT % M);
            end else if (MSB) begin       // d enters at the top, w[0] leaves
              for (int i = 0; i < L - 1; i++) w[i] <= w[i + 1];
              w[L - 1] <= d;
              r <= W'(((r + M * B - w[0]) * BINV + d * CH) % M);   // (1)!
            end else begin                // d enters at the bottom, w[L-1] leaves
              for (int i = L - 1; i > 0; i--) w[i] <= w[i - 1];
              w[0] <= d;
              r <= W'((r * B + d + M * B - w[L - 1] * CL) % M);   // (2)!
            end
          assign div = (r == 0);
        endmodule
        ```

        1. ‏\( (w - out) \cdot B^{-1} + B^{L-1} d \). ‏\( M \cdot B \) הוא כפולה של \( M \) שגדולה מכל ספרה, ושומר את הביטוי חיובי.
        2. ‏\( Bw + d - B^L \cdot out \). ‏\( out \cdot C_L < B \cdot M \), ולכן גם כאן הביטוי חיובי.

    #### למה זה נכון { .sol-proof }

    **המעברים.** בשרשור ל-LSB : ‏\( w' = Bw + d - B^L \cdot out \equiv Br + d - C_L \cdot out \).
    בשרשור ל-MSB : ‏\( w - out \) מתחלק ב-\( B \), ו-\( B \) הפיך, ולכן
    \( (w - out) / B \equiv (r - out) B^{-1} \), ו-\( w' \equiv r' \). השארית מתחילה נכונה
    (‏\( INIT \bmod m \)) ונשארת נכונה בכל צעד.

    **למה צריך את החלון.** ‏\( out \) הוא ספרה של החלון, ואי אפשר לשחזר אותה מהשארית. גם
    בבסיס ובכל \( m \), ההוכחה של סעיף א מראה שכמעט כל החלון הוא מצב : החלון עצמו הוא
    הזיכרון, והשארית רק חוסכת את החישוב מחדש.

    **נסו בעצמכם.** בוחרים ברשימה איפה הספרה החדשה נכנסת, \( m \), בסיס, את אורך החלון ואת
    החלון אחרי reset, ומקלידים או משרשרים את הספרות שנכנסות. נתיב הנתונים מראה בכל צעד את
    הספרה שנכנסת, את זו שיוצאת ואת עדכון השארית. כשיש עד 16 חלונות מופיעה גם המכונה הישירה,
    עם מצב לכל חלון :

    <div class="explorer" data-kind="winfsm" data-m="3" data-base="2" data-len="3" data-init="000" data-num="1101"></div>

    #### סיבוכיות { .sol-cost }

    - **זיכרון :** ‏\( L \lceil \log_2 B \rceil \) ביטים לחלון ו-\( \lceil \log_2 m \rceil \) לשארית.
      החלון הכרחי, והשארית אפשר לחשב מהחלון.
    - **לוגיקה :** בכל מחזור כפל בקבוע וחיבור אחד מודולו \( m \), בלי קשר ל-\( L \). חישוב
      `w % m` מכל החלון הוא עץ בעומק \( O(\log L) \) ובגודל \( O(L) \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לשמור רק את השארית"
    זה עבד ב-0055 כי שום דבר לא יצא מהמספר. כאן הספרה שיוצאת משנה את השארית, ואי אפשר
    לדעת מהשארית מה היא. החלונות `011` ו-`110` הם 3 ו-6, שניהם מתחלקים, אבל אחרי הביט 0
    מימין הם `110` (6) ו-`100` (4).

??? trap "מלכודת : לשכוח את הביט שיוצא"
    ‏\( r' = (2r + b) \bmod 3 \) של 0055 נותן את השארית של המספר כולו, לא של החלון. ההבדל
    מתחיל ברגע שהחלון מתמלא והביט הראשון יוצא.

??? trap "מלכודת : חילוק ב-B כשהוא לא הפיך"
    בשרשור ל-MSB חילקנו ב-\( B \). ב-\( m \) זוגי עם ביטים, ‏\( 2^{-1} \bmod m \) לא קיים. אבל
    שרשור ל-LSB לא מחלק בכלום, ועובד לכל \( m \). ובשרשור ל-MSB עם \( m = 2^a \) מספיק לבדוק
    ש-\( a \) הביטים הנמוכים של החלון הם 0.

??? followup "שאלות המשך"
    - **השארית עצמה :** רוצים ביציאה את \( w \bmod m \), לא רק אם הוא 0. מה משתנה?

        ??? fu-answer "תשובה"
            כלום : \( r \) הוא השארית, בשני הכיוונים. זה ההבדל מ-0055, שבו מה-LSB המצב היה
            \( r \cdot B^{-k} \) והשארית עצמה דרשה לזכור גם את \( k \).

    - **בלי רגיסטר שארית :** מתי עדיף לחשב `w % 3` מהחלון בכל מחזור?

        ??? fu-answer "תשובה"
            כש-\( L \) קטן, או כשהחלון נטען לפעמים בבת אחת (load מקבילי). אז עץ קומבינטורי
            של שאריות חלקיות (סכום לסירוגין של זוגות ביטים, כי \( 2 \equiv -1 \)) חוסך את שני
            הביטים ואת הסנכרון שלהם עם החלון.

    - **חלון שמתמלא :** אין reset לאפסים, והחלון לא תקף עד שנכנסו \( L \) ביטים. מה מוסיפים?

        ??? fu-answer "תשובה"
            מונה עד \( L \) וביט valid. עד שהמונה מגיע ל-\( L \) היציאה לא תקפה, ומאותו רגע
            הרגיסטרים כבר מחזיקים חלון מלא, והעדכון רגיל.

    - **בדיקה :** איך מאמתים את המודול?

        ??? fu-answer "תשובה"
            מודל ייחוס ששומר את החלון כמספר (‏`longint` או Python) ומחשב \( w \bmod m \) מחדש
            בכל מחזור, ו-assertion ש-`div` שווה ל-\( w \bmod m = 0 \). רצפים אקראיים ארוכים,
            כמה ערכי \( INIT \), ושני הכיוונים, עם \( L = 1 \) ו-\( L \) גדול.
