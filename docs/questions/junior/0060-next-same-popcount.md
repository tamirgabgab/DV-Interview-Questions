---
id: 60
title: המספר הבא עם אותו מספר של אחדות – Gosper, הקודם, ואפסים
level: junior
difficulty: medium
kind: code
tags: [bitwise, combinatorics, algorithms, systemverilog, python]
source: "טריק ביטים קלאסי (Gosper's hack, ‏HAKMEM 175), שאלה מוכרת בראיונות"
added: 2026-10-27
---

## השאלה

נתון מספר שלם חיובי \( x \) ברוחב \( w \) ביטים, ובו \( k \) ביטים דולקים (אחדות).

- **סעיף א – הבא :** מצאו את המספר **הקטן ביותר שגדול מ-\( x \)** ויש בו בדיוק \( k \) אחדות,
  בכמה פעולות על ביטים, בלי לולאה.
- **סעיף ב – הקודם :** מצאו את המספר **הגדול ביותר שקטן מ-\( x \)** עם \( k \) אחדות.
- **סעיף ג – אפסים :** אותה שאלה, אבל סופרים **אפסים**, רק מהאחד העליון ומטה. אפסים מובילים
  לא נספרים, כי הם לא משנים את הערך, ואין רוחב קבוע. מה המספר הבא אחרי \( x \) עם אותו מספר
  של אפסים, ומה הקודם?

לדוגמה, ב-8 ביטים \( 92 = 0101\,1100 \) והבא אחריו עם ארבע אחדות הוא \( 99 = 0110\,0011 \).

??? interviewer "מה המראיין בודק"
    - **לחשוב על הביטים :** האם המועמד רואה את המספר כבלוקים של אחדות ואפסים, ומבין איפה
      השינוי הקטן ביותר חייב לקרות.
    - **טריקים בסיסיים :** ‏`x & -x`, ה-carry של חיבור ו-XOR כדי לראות מה השתנה.
    - **סימטריה :** האם הוא מזהה שהקודם הוא "הבא" בעולם ההפוך, ולא כותב אלגוריתם חדש.
    - **אורך משתנה :** בסעיף ג, האם הוא מבין שעם אפסים האורך של המספר הוא חלק מהתנאי, ושבתוך
      אורך קבוע זו אותה שאלה של סעיפים א ו-ב.
    - **מקרי קצה :** ‏\( x = 0 \), בלוק האחדות בראש המילה, ורוחב המילה.

---

### סעיף א – המספר הבא

??? tip "רמז 1"
    כדי לגדול כמה שפחות, השינוי צריך להיות נמוך ככל האפשר. איזה אחד אפשר להזיז שמאלה הכי
    נמוך?

??? tip "רמז 2"
    מצאו את בלוק האחדות הנמוך ביותר. מה קורה כשמוסיפים ל-\( x \) את האחד הנמוך ביותר שלו,
    ‏`x & -x`?

??? tip "רמז 3"
    אחרי החיבור יש אחד חדש מעל הבלוק, והבלוק כולו נעלם. כמה אחדות חסרים עכשיו, ואיפה הכי זול
    לשים אותם?

<div class="selfcheck" data-answer="99" data-show="99 : ‏0110 0011" data-hint="הבלוק הנמוך ב-0101 1100 הוא שלוש האחדות במקומות 2 עד 4. האחד העליון שלו עולה למקום 5, ושני האחרים יורדים לתחתית." markdown>
מה המספר הבא אחרי 92 עם ארבע אחדות?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מוצאים את בלוק האחדות הנמוך ביותר. האחד העליון שלו עולה מקום אחד, ושאר האחדות של הבלוק
        יורדים לתחתית המילה. בנוסחה : ‏`c = x & -x`, ‏`r = x + c`, והתשובה היא
        ‏`r | (((x ^ r) >> 2) / c)`. אם החיבור גולש מעבר ל-\( w \) ביטים, אין מספר הבא.

    <!-- cost: זמן \( O(1) \) | זיכרון \( O(1) \) | חילוק אחד, ובחומרה הזזה -->

    #### הרעיון { .sol-idea }

    **איפה השינוי.** נכתוב \( x = a\,0\,\underbrace{1 \dots 1}_{m}\,\underbrace{0 \dots 0}_{t} \) : בלוק של
    \( m \) אחדות שמתחיל במקום \( t \), ומעליו אפס. מספר גדול יותר עם אותן אחדות חייב להדליק
    ביט שהיה כבוי, והנמוך ביותר שאפשר הוא האפס שמעל הבלוק, במקום \( t + m \). מדליקים אותו,
    ואת \( m - 1 \) האחדות הנותרים של הבלוק מניחים הכי נמוך שאפשר, בתחתית.

    **הנוסחה עושה את זה בארבעה צעדים.** על 92 ב-8 ביטים :

    <!-- gen 0 -->

    <div class="gs-scroll"><table class="gs-bits" dir="ltr" aria-label="השלבים של הנוסחה על 92 ב-8 ביטים"><tbody><tr><th>x</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">92</td></tr><tr><th>c = x &amp; −x</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one is-mark">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">4</td></tr><tr><th>r = x + c</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">96</td></tr><tr><th>x ^ r</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">60</td></tr><tr><th>(x ^ r) &gt;&gt; 2</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-val">15</td></tr><tr><th>s = … / c</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-val">3</td></tr><tr><th>r | s</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-val">99</td></tr></tbody></table></div>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="gs-key-one"></i>ביט דולק</span><span><i class="gs-key-mark"></i>הביטים שהשלב עוסק בהם</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **האחד הנמוך :** ‏`c = x & -x`. ‏\( -x = \sim x + 1 \) הופך את כל הביטים שמעל האחד
       הנמוך, ולכן ה-AND משאיר רק אותו : ‏\( c = 2^t \).
    2. **ה-carry :** ‏`r = x + c`. החיבור רץ לאורך הבלוק, מכבה את כולו ומדליק את הביט
       \( t + m \) שמעליו. מעל זה \( r \) שווה ל-\( x \).
    3. **מה השתנה :** ‏`x ^ r` הוא בדיוק \( m + 1 \) אחדות, במקומות \( t \) עד \( t + m \) : הבלוק
       והביט החדש.
    4. **לתחתית :** צריך רק \( m - 1 \) מהם, בתחתית. ‏`>> 2` מוריד שניים, והחילוק ב-\( c \) מזיז
       ימינה עוד \( t \) מקומות.
    5. **מחברים :** ‏`r | s` : החלק העליון והביט החדש מ-\( r \), והאחדות שירדו מ-\( s \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="next_same" linenums="1" hl_lines="5 6 9"
        def next_same(x: int, w: int = 32) -> int:
            """The smallest number above x with as many ones, in w bits; 0 when there is none."""
            if x == 0:
                return 0
            c = x & -x                       # the lowest one
            r = x + c                        # the carry clears the lowest block
            if r >> w:
                return 0                     # the block was at the top
            return r | (((x ^ r) >> 2) // c)  # (1)!
        ```

        1. ב-Python ‏`//` קודם ל-`>>`, ולכן כל הסוגריים. בלעדיהם ‏`(x ^ r) >> 2 // c` מזיז ב-\( 2 / c \).

    === "SystemVerilog"
        ```systemverilog title="function next_same" linenums="1" hl_lines="6 7 9 10"
        // the smallest number above x with as many ones; 0 when there is none in 32 bits
        function automatic logic [31:0] next_same(logic [31:0] x);
          logic [31:0] c, s;
          logic [32:0] r;
          if (x == 0) return '0;
          c = x & -x;                              // (1)!
          r = {1'b0, x} + {1'b0, c};               // (2)!
          if (r[32]) return '0;                    // (3)!
          s = ((x ^ r[31:0]) >> 2) / c;
          return r[31:0] | s;
        endfunction
        ```

        1. האחד הנמוך ביותר, \( c = 2^t \).
        2. ה-carry מכבה את הבלוק הנמוך ומדליק את הביט שמעליו. הביט ה-33 תופס גלישה.
        3. הבלוק היה בראש המילה : אין מספר גדול יותר עם אותן אחדות ב-32 ביטים.

    #### למה זה נכון { .sol-proof }

    יהי \( y > x \) עם \( k \) אחדות, ו-\( q \) הביט העליון שבו הם שונים : ‏\( y_q = 1 \), ‏\( x_q = 0 \).

    - **‏\( q < t \) לא ייתכן :** כל האחדות של \( x \) נמצאות מעל \( q \), ושם \( y \) שווה ל-\( x \).
      עם האחד במקום \( q \) היו ל-\( y \) לפחות \( k + 1 \) אחדות.
    - **‏\( t \le q < t + m \) לא ייתכן :** שם \( x_q = 1 \).
    - **לכן \( q \ge t + m \), והקטן ביותר הוא \( q = t + m \).** מעל \( q \) ‏\( y \) שווה ל-\( x \),
      ‏\( k - m \) אחדות. עם \( y_q \) יש \( k - m + 1 \), ונשארו \( m - 1 \) אחדות לביטים שמתחת
      ל-\( q \). המספר הקטן ביותר שם הוא כשהם בתחתית. זה בדיוק `r | s`.

---

### סעיף ב – המספר הקודם

??? tip "רמז 1"
    מה קורה לסדר בין שני מספרים כשהופכים את כל הביטים שלהם?

??? tip "רמז 2"
    אם ל-\( x \) יש \( k \) אחדות ברוחב \( w \), כמה אחדות יש ל-\( \sim x \)?

<div class="selfcheck" data-answer="80" data-show="80 : ‏0101 0000" data-hint="ל-96 = 0110 0000 יש שתי אחדות. האחד הנמוך שמתחתיו יש אפס יורד מקום אחד." markdown>
מה המספר הקודם ל-96 עם שתי אחדות?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏`prev(x) = ~next(~x)`, ברוחב \( w \). ההיפוך \( \sim x = 2^w - 1 - x \) הופך את הסדר ומעביר
        מספרים עם \( k \) אחדות למספרים עם \( w - k \) אחדות. לכן הגדול ביותר מתחת ל-\( x \) הוא
        ההיפוך של הקטן ביותר מעל \( \sim x \). בלי היפוך : מוצאים את האחד הנמוך ביותר שמתחתיו
        אפס, מורידים אותו מקום אחד, ומצמידים אליו מלמטה את כל האחדות שהיו מתחתיו.

    #### הרעיון { .sol-idea }

    **הסדר מתהפך.** אם \( y < x \) אז \( \sim y > \sim x \). ברוחב 5 ביטים, המספרים עם שתי אחדות
    לפי הסדר, ולידם ההיפוך שלהם. הרשימה של ההיפוכים יורדת, כלומר הרשימה של המספרים עם שלוש
    אחדות הפוכה :

    <!-- gen 2 -->

    | ‏x, עולה | ‏~x, יורד |
    |:-:|:-:|
    | ‏`00011` (3) | ‏`11100` (28) |
    | ‏`00101` (5) | ‏`11010` (26) |
    | ‏`00110` (6) | ‏`11001` (25) |
    | ‏`01001` (9) | ‏`10110` (22) |
    | ‏`01010` (10) | ‏`10101` (21) |
    | ‏`01100` (12) | ‏`10011` (19) |
    | ‏`10001` (17) | ‏`01110` (14) |
    | ‏`10010` (18) | ‏`01101` (13) |
    | ‏`10100` (20) | ‏`01011` (11) |
    | ‏`11000` (24) | ‏`00111` (7) |

    <!-- /gen -->

    **אותה פונקציה פעמיים.** הקודם של \( x \) הוא השכן שלו ברשימה למטה, כלומר השכן של \( \sim x \)
    ברשימה ההפוכה למעלה : ‏`next(~x)`, ועוד היפוך אחד כדי לחזור. על 99 ב-8 ביטים :

    <!-- gen 3 -->

    <div class="gs-scroll"><table class="gs-bits" dir="ltr" aria-label="הקודם של 99 דרך המשלים"><tbody><tr><th>x</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-val">99</td></tr><tr><th>~x</th><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">156</td></tr><tr><th>next(~x)</th><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-val">163</td></tr><tr><th>~next(~x)</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">92</td></tr></tbody></table></div>

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="prev_same" linenums="1" hl_lines="4 5"
        def prev_same(x: int, w: int = 32) -> int:
            """The largest number below x with as many ones, in w bits; 0 when there is none."""
            mask = (1 << w) - 1
            y = next_same(~x & mask, w)      # (1)!
            return 0 if y == 0 else ~y & mask
        ```

        1. ב-Python ‏`~x` הוא \( -x - 1 \), מספר שלילי. המסכה מחזירה אותו לרוחב \( w \).

    === "SystemVerilog"
        ```systemverilog title="function prev_same" linenums="1" hl_lines="4 5"
        // the largest number below x with as many ones; 0 when there is none
        function automatic logic [31:0] prev_same(logic [31:0] x);
          logic [31:0] y;
          y = next_same(~x);                       // (1)!
          return (y == 0) ? '0 : ~y;
        endfunction
        ```

        1. ‏`~x` הוא ברוחב 32 ביטים בדיוק, כמו המשתנה. אם אין הבא ל-\( \sim x \), אין קודם ל-\( x \).

    #### למה זה נכון { .sol-proof }

    ‏\( f(y) = 2^w - 1 - y \) היא התאמה חד-חד-ערכית ויורדת בין המספרים עם \( k \) אחדות לאלה
    עם \( w - k \) אחדות ברוחב \( w \). לכן \( y \) הוא הגדול ביותר מתחת ל-\( x \) בקבוצה הראשונה
    בדיוק כש-\( f(y) \) הוא הקטן ביותר מעל \( f(x) \) בקבוצה השנייה, כלומר
    \( f(y) = \text{next}(f(x)) \).

    **הקודם הוא לא "הבא בכיוון השני" של אותה נוסחה.** ב-`next` הבלוק הנמוך זז למעלה ושאריתו
    יורדת לתחתית. ב-`prev` האחד שזז למטה הוא הנמוך ביותר שיש מתחתיו אפס, והאחדות שמתחתיו
    נצמדים אליו מלמטה, למקומות **הגבוהים** ביותר שמתחתיו. ההיפוך מתרגם אחד לשני.

---

### סעיף ג – אותו מספר של אפסים

??? tip "רמז 1"
    בתוך אורך קבוע \( L \) (המספרים מ-\( 2^{L-1} \) עד \( 2^L - 1 \)), מה הקשר בין מספר האפסים
    למספר האחדות?

??? tip "רמז 2"
    מה קורה כשבאורך \( L \) כבר אין מספר הבא? מה המספר הקטן ביותר באורך \( L + 1 \) עם \( z \)
    אפסים?

<div class="selfcheck" data-answer="143" data-show="143 : ‏10001111" data-hint="ל-120 = 1111000 יש שלושה אפסים, והוא האחרון באורך 7 עם שלושה אפסים. באורך 8 : אחד בראש, שלושה אפסים, וארבע אחדות בתחתית." markdown>
מה המספר הבא אחרי 120 עם שלושה אפסים?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        באורך קבוע \( L \), ‏\( z \) אפסים הם \( L - z \) אחדות, ולכן בתוך האורך הבא והקודם הם בדיוק
        סעיפים א ו-ב ברוחב \( L \). כשהאורך נגמר, עוברים אורך. הבא הוא הקטן ביותר באורך \( L + 1 \) :
        ‏1, אחריו \( z \) אפסים ו-\( L - z \) אחדות, כלומר \( 2^L + 2^{L-z} - 1 \). הקודם הוא הגדול ביותר
        באורך \( L - 1 \) : ‏\( L - 1 - z \) אחדות ואחריהן \( z \) אפסים. אם אין בו מקום לאחד
        (\( L - 1 - z < 1 \)), אין קודם.

    <!-- cost: זמן \( O(1) \) ועוד האורך של x | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **למה אפסים שונים מאחדות.** אפס מוביל לא משנה את הערך, ולכן לא סופרים אותו. עם ביט 1 זה לא
    משנה כלום : אפשר להוסיף אפסים מובילים בלי לשנות את מספר האחדות, והמספר גדל בחופשיות בתוך
    המילה. עם ביט 0 **האורך** של המספר הוא חלק מהתנאי. כל מספר באורך \( L + 1 \) גדול מכל מספר
    באורך \( L \), ולכן הרשימה של המספרים עם \( z \) אפסים עוברת על האורכים לפי הסדר :

    <!-- gen 4 -->

    | האורך | המספרים עם שלושה אפסים, לפי הסדר |
    |:-:|:-:|
    | ‏4 | ‏`1000` (8) |
    | ‏5 | ‏`10001` (17), ‏`10010` (18), ‏`10100` (20), ‏`11000` (24) |
    | ‏6 | ‏`100011` (35), ‏`100101` (37), ‏`100110` (38), ‏`101001` (41), ‏`101010` (42), ‏`101100` (44), ‏`110001` (49), ‏`110010` (50), ‏`110100` (52), ‏`111000` (56) |

    <!-- /gen -->

    **בתוך אורך זו אותה שאלה.** באורך \( L \) ביט \( L - 1 \) תמיד דולק, ומספר האפסים קובע את
    מספר האחדות. לכן `next_same(x, L)` נותן את הבא באותו אורך, אם יש כזה.

    **בסוף האורך קופצים.** ל-120 = 1111000 אין מספר הבא באורך 7 : החיבור של סעיף א גולש מעבר
    ל-7 ביטים. המספר הבא הוא הקטן ביותר באורך 8 עם שלושה אפסים :

    <!-- gen 5 -->

    <div class="gs-scroll"><table class="gs-bits" dir="ltr" aria-label="הבא אחרי 120 עם שלושה אפסים"><tbody><tr><th>x</th><td class="gs-b">0</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">120</td></tr><tr><th>c = x &amp; −x</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one is-mark">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">8</td></tr><tr><th>r = x + c</th><td class="gs-b is-one is-mark">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">128</td></tr><tr><th>1 0…0 1…1</th><td class="gs-b is-one is-mark">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-b is-one is-mark">1</td><td class="gs-val">143</td></tr></tbody></table></div>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **האורך :** ‏\( L \), המקום של האחד העליון ועוד 1, ו-\( z = L - \text{popcount}(x) \).
    2. **הבא :** ‏`next_same(x, L)`. אם הוא קיים, זו התשובה. אם לא, ‏\( 2^L + 2^{L-z} - 1 \).
    3. **הקודם :** ‏`prev_same(x, L)`. אם הביט \( L - 1 \) שלו דולק, הוא באותו אורך וזו התשובה.
       אם לא, ‏\( (2^{L-1-z} - 1) \cdot 2^z \), כשיש מקום לאחד אחד לפחות.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="next_zeros, prev_zeros" linenums="1" hl_lines="5 6 13 14 15"
        def next_zeros(x: int) -> int:
            """The smallest number above x (x >= 1) with as many zeros below its top one."""
            length = x.bit_length()
            z = length - bin(x).count("1")
            y = next_same(x, length)          # (1)!
            return y if y else (1 << length) | ((1 << (length - z)) - 1)


        def prev_zeros(x: int) -> int:
            """The largest number below x with as many zeros below its top one; 0 when there is none."""
            length = x.bit_length()
            z = length - bin(x).count("1")
            y = prev_same(x, length)
            if y >> (length - 1):            # (2)!
                return y
            return ((1 << (length - 1 - z)) - 1) << z if length - 1 - z >= 1 else 0
        ```

        1. ברוחב האורך של \( x \) : ‏0 אומר שהאורך נגמר.
        2. הביט העליון של האורך דולק : אותו אורך, ולכן אותם אפסים.

    === "SystemVerilog"
        ```systemverilog title="functions next_zeros, prev_zeros" linenums="1" hl_lines="9 11 21 23"
        // the smallest number above x (x >= 1) with as many zeros below its top one;
        // 0 when it would not fit in 32 bits
        function automatic logic [31:0] next_zeros(logic [31:0] x);
          int L = 0, z;
          logic [31:0] y;
          for (int p = 0; p < 32; p++) if (x[p]) L = p + 1;
          z = L - $countones(x);
          y = next_same(x);
          if (y != 0 && 64'(y) < (64'd1 << L)) return y;    // (1)!
          if (L == 32) return '0;
          return 32'((64'd1 << L) | ((64'd1 << (L - z)) - 1));
        endfunction

        // the largest number below x with as many zeros below its top one; 0 when there is none
        function automatic logic [31:0] prev_zeros(logic [31:0] x);
          int L = 0, z;
          logic [31:0] y;
          for (int p = 0; p < 32; p++) if (x[p]) L = p + 1;
          z = L - $countones(x);
          y = prev_same(x);
          if (L > 0 && y[L - 1]) return y;                  // (2)!
          if (L - 1 - z < 1) return '0;
          return 32'(((64'd1 << (L - 1 - z)) - 1) << z);
        endfunction
        ```

        1. ‏`next_same` ברוחב 32 מוצא את הבא עם אותן אחדות. אם הוא עדיין באורך \( L \), יש לו גם אותם אפסים.
        2. הקודם עם אותן אחדות קטן מ-\( x \), ולכן לא ארוך ממנו. אם הביט העליון של האורך דולק, הוא באותו אורך.

    #### למה זה נכון { .sol-proof }

    **הסדר הוא קודם לפי אורך.** כל מספר באורך \( L \) קטן מכל מספר באורך \( L + 1 \). לכן הבא
    אחרי \( x \) עם \( z \) אפסים הוא באורך \( L \) אם יש שם כזה, ואחרת הקטן ביותר באורך \( L + 1 \).

    **בתוך אורך.** באורך \( L \) יש \( L \) ביטים בלי אפסים מובילים, ולכן \( z \) אפסים הם בדיוק
    \( L - z \) אחדות, וסעיפים א ו-ב נותנים את השכנים.

    **בין אורכים.** באורך \( L + 1 \) הביט העליון דולק, ונשארים \( L \) ביטים עם \( z \) אפסים
    ו-\( L - z \) אחדות. הקטן ביותר שם הוא עם האחדות בתחתית : ‏\( 2^L + 2^{L-z} - 1 \). באורך
    \( L - 1 \) יש \( L - 1 - z \) אחדות, והגדול ביותר הוא עם כולן למעלה. אם \( L - 1 - z < 1 \),
    אין אחד לביט העליון, ולכן אין מספר קודם. המספר הקטן ביותר עם \( z \) אפסים הוא \( 2^z \).

    #### סיבוכיות { .sol-cost }

    - **הבא והקודם עם אחדות :** ‏\( O(1) \) : חיבור אחד, XOR, הזזה וחילוק בחזקה של 2. בחומרה
      החילוק הוא הזזה ב-\( t \), ‏\( t \) יוצא מ-priority encoder, והנתיב הארוך הוא ה-carry של
      החיבור.
    - **עם אפסים :** אותו דבר, ועוד האורך של \( x \) : עוד priority encoder, מלמעלה.

    **נסו בעצמכם.** בוחרים את הביט שסופרים, רוחב ומספר, ורואים את שלבי הנוסחה אחד אחרי השני,
    למספר הבא או לקודם. עם ביט 0 האפסים המובילים מסומנים בקו מקווקו, ולא נספרים :

    <div class="explorer" data-kind="popnext" data-x="92" data-w="8"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : ‏x = 0 ובלוק בראש המילה"
    ב-\( x = 0 \) אין אחד נמוך, ‏\( c = 0 \), והחילוק הוא חילוק באפס. כשהבלוק הנמוך הוא גם
    העליון ונוגע בראש המילה (11100000), החיבור גולש, ובלי בדיקה מקבלים מספר קטן או מספר רחב
    מדי. שני המקרים מחזירים "אין".

??? trap "מלכודת : ‏~x בפייתון"
    ב-Python למספרים אין רוחב, ו-`~x` הוא \( -x - 1 \), שלילי. בלי `& mask` ההיפוך לא נותן
    מספר עם \( w - k \) אחדות, והתשובה של `prev_same` שגויה.

??? trap "מלכודת : לחפש מספר אחרי מספר"
    ‏`while popcount(y) != k: y += 1` נכון, אבל איטי. מ-\( 0111\,1111\,0000\,0000 \) (32512) הוא
    עובר 319 מספרים עד \( 1000\,0000\,0011\,1111 \) (32831), והמרחק בין שכנים מגיע
    ל-\( 2^{w-2} \) : מ-\( 0100 \dots 0 \) ל-\( 1000 \dots 0 \).

??? followup "שאלות המשך"
    - **כל הקבוצות בגודל \( k \) :** איך עוברים על כל הבחירות של \( k \) ערוצים מתוך \( n \),
      למשל כדי לכסות כל צירוף של ערוצים פעילים?

        ??? fu-answer "תשובה"
            מתחילים ב-`(1 << k) - 1` וקוראים ל-`next_same` עד שהתוצאה עוברת את `1 << n`. יש
            בדיוק \( \binom{n}{k} \) צעדים, כל אחד \( O(1) \), לפי הסדר העולה.

    - **בחומרה, במחזור אחד ובלי חילוק :** איך?

        ??? fu-answer "תשובה"
            ‏\( s = (x \oplus r) \gg (t + 2) \), כש-\( t \) הוא מספר האפסים בתחתית של \( x \),
            מ-priority encoder. הכול קומבינטורי : AND, חיבור, XOR, ‏barrel shifter ו-OR.

    - **כל תתי-המסכות :** איך עוברים על כל המספרים שהאחדות שלהם בתוך מסכה \( M \)?

        ??? fu-answer "תשובה"
            ‏`s = (s - 1) & M`, מ-\( s = M \) עד 0. החיסור מכבה את האחד הנמוך של \( s \) ומדליק את
            כל מה שמתחתיו, וה-AND משאיר רק את מה שבמסכה. על כל המסכות יחד זה \( 3^n \) צעדים.

    - **הבא, רק בביטים מותרים :** הבא עם אותו מספר של אחדות, כשמותר להדליק רק ביטים של מסכה
      \( M \)?

        ??? fu-answer "תשובה"
            דוחסים את הביטים של \( M \) למספר רציף (`pext`), מפעילים את `next_same` ברוחב
            \( \text{popcount}(M) \), ומפזרים חזרה (`pdep`). הסדר נשמר, כי הדחיסה שומרת על
            הסדר בין הביטים.
