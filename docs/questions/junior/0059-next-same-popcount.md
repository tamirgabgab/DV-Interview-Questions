---
id: 59
title: המספר הבא עם אותו מספר של אחדות – Gosper, הקודם והמקום ברשימה
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
- **סעיף ג – המקום ברשימה :** כמה מספרים עם \( k \) אחדות קטנים מ-\( x \)? ובכיוון ההפוך :
  בהינתן \( m \) ו-\( k \), מה המספר עם \( k \) אחדות שיש בדיוק \( m \) כאלה קטנים ממנו? בלי
  לעבור עליהם אחד אחד.

לדוגמה, ב-8 ביטים \( 92 = 0101\,1100 \) והבא אחריו עם ארבע אחדות הוא \( 99 = 0110\,0011 \).

??? interviewer "מה המראיין בודק"
    - **לחשוב על הביטים :** האם המועמד רואה את המספר כבלוקים של אחדות ואפסים, ומבין איפה
      השינוי הקטן ביותר חייב לקרות.
    - **טריקים בסיסיים :** ‏`x & -x`, ה-carry של חיבור ו-XOR כדי לראות מה השתנה.
    - **סימטריה :** האם הוא מזהה שהקודם הוא "הבא" בעולם ההפוך, ולא כותב אלגוריתם חדש.
    - **ספירה במקום מעבר :** בסעיף ג, האם הוא סופר לפי הביט העליון ומגיע למקדמי בינום.
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

    #### למה זה נכון { .sol-proof }

    יהי \( y > x \) עם \( k \) אחדות, ו-\( q \) הביט העליון שבו הם שונים : ‏\( y_q = 1 \), ‏\( x_q = 0 \).

    - **‏\( q < t \) לא ייתכן :** כל האחדות של \( x \) נמצאות מעל \( q \), ושם \( y \) שווה ל-\( x \).
      עם האחד במקום \( q \) היו ל-\( y \) לפחות \( k + 1 \) אחדות.
    - **‏\( t \le q < t + m \) לא ייתכן :** שם \( x_q = 1 \).
    - **לכן \( q \ge t + m \), והקטן ביותר הוא \( q = t + m \).** מעל \( q \) ‏\( y \) שווה ל-\( x \),
      ‏\( k - m \) אחדות. עם \( y_q \) יש \( k - m + 1 \), ונשארו \( m - 1 \) אחדות לביטים שמתחת
      ל-\( q \). המספר הקטן ביותר שם הוא כשהם בתחתית. זה בדיוק `r | s`.

    **נסו בעצמכם.** בוחרים רוחב ומספר, ורואים את שלבי הנוסחה אחד אחרי השני. "הבא" ו"הקודם"
    עוברים ברשימה של כל המספרים עם אותו מספר של אחדות, והמקום ברשימה מתעדכן :

    <div class="explorer" data-kind="popnext" data-x="92" data-w="8"></div>

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

    | המקום של x | ‏x | ‏~x | המקום של ~x |
    |:-:|:-:|:-:|:-:|
    | ‏0 | ‏`00011` (3) | ‏`11100` (28) | ‏9 |
    | ‏1 | ‏`00101` (5) | ‏`11010` (26) | ‏8 |
    | ‏2 | ‏`00110` (6) | ‏`11001` (25) | ‏7 |
    | ‏3 | ‏`01001` (9) | ‏`10110` (22) | ‏6 |
    | ‏4 | ‏`01010` (10) | ‏`10101` (21) | ‏5 |
    | ‏5 | ‏`01100` (12) | ‏`10011` (19) | ‏4 |
    | ‏6 | ‏`10001` (17) | ‏`01110` (14) | ‏3 |
    | ‏7 | ‏`10010` (18) | ‏`01101` (13) | ‏2 |
    | ‏8 | ‏`10100` (20) | ‏`01011` (11) | ‏1 |
    | ‏9 | ‏`11000` (24) | ‏`00111` (7) | ‏0 |

    <!-- /gen -->

    **אותה פונקציה פעמיים.** הקודם של \( x \) הוא השכן שלו ברשימה למטה, כלומר השכן של \( \sim x \)
    ברשימה ההפוכה למעלה : ‏`next(~x)`, ועוד היפוך אחד כדי לחזור. על 99 ב-8 ביטים :

    <!-- gen 3 -->

    <div class="gs-scroll"><table class="gs-bits" dir="ltr" aria-label="הקודם של 99 דרך המשלים"><tbody><tr><th>x</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-val">99</td></tr><tr><th>~x</th><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">156</td></tr><tr><th>next(~x)</th><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-val">163</td></tr><tr><th>~next(~x)</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">92</td></tr></tbody></table></div>

    <!-- /gen -->

    #### הקוד { .sol-code }

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

    === "Python"
        ```python title="prev_same" linenums="1" hl_lines="4 5"
        def prev_same(x: int, w: int = 32) -> int:
            """The largest number below x with as many ones, in w bits; 0 when there is none."""
            mask = (1 << w) - 1
            y = next_same(~x & mask, w)      # (1)!
            return 0 if y == 0 else ~y & mask
        ```

        1. ב-Python ‏`~x` הוא \( -x - 1 \), מספר שלילי. המסכה מחזירה אותו לרוחב \( w \).

    #### למה זה נכון { .sol-proof }

    ‏\( f(y) = 2^w - 1 - y \) היא התאמה חד-חד-ערכית ויורדת בין המספרים עם \( k \) אחדות לאלה
    עם \( w - k \) אחדות ברוחב \( w \). לכן \( y \) הוא הגדול ביותר מתחת ל-\( x \) בקבוצה הראשונה
    בדיוק כש-\( f(y) \) הוא הקטן ביותר מעל \( f(x) \) בקבוצה השנייה, כלומר
    \( f(y) = \text{next}(f(x)) \).

    **הקודם הוא לא "הבא בכיוון השני" של אותה נוסחה.** ב-`next` הבלוק הנמוך זז למעלה ושאריתו
    יורדת לתחתית. ב-`prev` האחד שזז למטה הוא הנמוך ביותר שיש מתחתיו אפס, והאחדות שמתחתיו
    נצמדים אליו מלמטה, למקומות **הגבוהים** ביותר שמתחתיו. ההיפוך מתרגם אחד לשני.

---

### סעיף ג – המקום ברשימה

??? tip "רמז 1"
    כמה מספרים עם \( k \) אחדות יש מתחת ל-\( 2^p \), כלומר עם כל האחדות ב-\( p \) הביטים
    הנמוכים?

??? tip "רמז 2"
    נניח שהאחד העליון של \( x \) במקום \( p \). המספרים הקטנים מ-\( x \) עם \( k \) אחדות הם
    אלה שהאחד העליון שלהם מתחת ל-\( p \), ועוד אלה שהאחד העליון שלהם בדיוק ב-\( p \). כמה יש
    מהסוג הראשון, ומה נשאר לספור בסוג השני?

<div class="selfcheck" data-answer="24" data-show="24 : ‏C(2,1) + C(3,2) + C(4,3) + C(6,4) = 2 + 3 + 4 + 15" data-hint="האחדות של 92 = 0101 1100 במקומות 2, 3, 4 ו-6. סכמו את C(p, i) לכל אחד, כש-i הוא המספר הסידורי שלו מלמטה." markdown>
כמה מספרים עם ארבע אחדות קטנים מ-92?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        אם האחדות של \( x \) במקומות \( p_1 < p_2 < \dots < p_k \), אז מספר הקטנים ממנו הוא
        \( \sum_{i=1}^{k} \binom{p_i}{i} \). לכיוון ההפוך הולכים מ-\( i = k \) למטה : בוחרים את
        ה-\( p \) הגדול ביותר עם \( \binom{p}{i} \le m \), מדליקים את הביט \( p \), ומחסירים
        \( \binom{p}{i} \) מ-\( m \). ל-92 יש 24 קטנים ממנו, ול-99 יש 25, כמו שצריך לשכן הבא.

    <!-- cost: זמן \( O(w) \) חיבורים | זיכרון טבלה של \( \binom{p}{i} \), ‏\( O(w \cdot k) \) -->

    #### הרעיון { .sol-idea }

    **סופרים לפי הביט העליון.** המספרים עם \( k \) אחדות שכולן מתחת למקום \( p_k \) קטנים
    מ-\( x \), ויש \( \binom{p_k}{k} \) כאלה : בוחרים \( k \) מקומות מתוך \( p_k \). המספרים עם
    אחד במקום \( p_k \) קטנים מ-\( x \) בדיוק כשהחלק שמתחתיו, עם \( k - 1 \) אחדות, קטן מהחלק של
    \( x \) שמתחתיו. זו אותה שאלה עם \( k - 1 \) אחדות, ומכאן הסכום. ל-92 :

    <!-- gen 4 -->

    | ‏i (האחד ה-i מלמטה) | המקום שלו \( p_i \) | ‏\( \binom{p_i}{i} \) |
    |:-:|:-:|:-:|
    | ‏1 | ‏2 | ‏2 |
    | ‏2 | ‏3 | ‏3 |
    | ‏3 | ‏4 | ‏4 |
    | ‏4 | ‏6 | ‏15 |
    | **סך הכול** | | **‏24** |

    <!-- /gen -->

    **הכיוון ההפוך הוא חמדני.** המספרים שהאחד העליון שלהם בדיוק במקום \( p \) תופסים ברשימה את
    המקומות מ-\( \binom{p}{k} \) עד \( \binom{p+1}{k} - 1 \). לכן האחד העליון של המספר במקום \( m \)
    הוא ה-\( p \) הגדול ביותר עם \( \binom{p}{k} \le m \). מחסירים וממשיכים עם \( k - 1 \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **טבלה :** מקדמי הבינום \( \binom{p}{i} \) ל-\( p < w \) ו-\( i \le k \), מראש או במשולש פסקל.
    2. **המקום :** עוברים על הביטים מלמטה. לכל אחד, ה-\( i \)-י מלמטה במקום \( p \), מוסיפים
       \( \binom{p}{i} \).
    3. **המספר מהמקום :** מ-\( i = k \) עד 1 : ה-\( p \) הגדול ביותר עם \( \binom{p}{i} \le m \),
       מדליקים אותו ומחסירים.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="functions binom, rank_same, unrank_same" linenums="1" hl_lines="14 24 25 26"
        // C(n, k), exact at every step: after step t it is C(n - k + t, t)
        function automatic longint unsigned binom(int n, int k);
          longint unsigned b = 1;
          if (k < 0 || k > n) return 0;
          for (int t = 1; t <= k; t++) b = b * 64'(n - k + t) / 64'(t);
          return b;
        endfunction

        // how many numbers with as many ones as x are smaller than x
        function automatic longint unsigned rank_same(logic [31:0] x);
          longint unsigned r = 0;
          int i = 0;
          for (int p = 0; p < 32; p++)
            if (x[p]) begin i++; r += binom(p, i); end   // (1)!
          return r;
        endfunction

        // the number with k ones that has exactly m smaller numbers with k ones (m < C(32, k))
        function automatic logic [31:0] unrank_same(longint unsigned m, int k);
          logic [31:0] x = '0;
          int p;
          for (int i = k; i >= 1; i--) begin
            p = i - 1;
            while (binom(p + 1, i) <= m) p++;     // (2)!
            x[p] = 1'b1;
            m -= binom(p, i);
          end
          return x;
        endfunction
        ```

        1. ה-\( i \)-י מלמטה במקום \( p \) : יש \( \binom{p}{i} \) דרכים לשים \( i \) אחדות מתחתיו.
        2. ה-\( p \) הגדול ביותר עם \( \binom{p}{i} \le m \). הוא לפחות \( i - 1 \), כי \( \binom{i-1}{i} = 0 \).

    === "Python"
        ```python title="rank_same, unrank_same" linenums="1" hl_lines="10 21 23 24"
        from math import comb


        def rank_same(x: int) -> int:
            """How many numbers with as many ones as x are smaller than x."""
            r, i, p = 0, 0, 0
            while x:
                if x & 1:
                    i += 1
                    r += comb(p, i)          # (1)!
                x >>= 1
                p += 1
            return r


        def unrank_same(m: int, k: int) -> int:
            """The number with k ones that has exactly m smaller numbers with k ones."""
            x = 0
            for i in range(k, 0, -1):
                p = i - 1
                while comb(p + 1, i) <= m:   # (2)!
                    p += 1
                x |= 1 << p
                m -= comb(p, i)
            return x
        ```

        1. ה-\( i \)-י מלמטה במקום \( p \).
        2. המספרים שהאחד ה-\( i \) שלהם בדיוק ב-\( p \) הם במקומות \( \binom{p}{i} \) עד \( \binom{p+1}{i} - 1 \).

    #### למה זה נכון { .sol-proof }

    **המקום.** באינדוקציה על \( k \). המספרים עם \( k \) אחדות שקטנים מ-\( x \) מתחלקים לפי האחד
    העליון : מתחת ל-\( p_k \) יש \( \binom{p_k}{k} \). אם הוא בדיוק ב-\( p_k \), המספר קטן מ-\( x \)
    בדיוק כשהחלק שמתחת ל-\( p_k \) קטן מהחלק של \( x \), ולפי ההנחה יש
    \( \sum_{i<k} \binom{p_i}{i} \) כאלה.

    **הכיוון ההפוך.** החלק שמתחת ל-\( p_k \) הוא מספר עם \( k - 1 \) אחדות מתחת ל-\( 2^{p_k} \),
    ולכן המקום שלו קטן מ-\( \binom{p_k}{k-1} \). כלומר המקום של \( x \) נמצא בין \( \binom{p_k}{k} \)
    ל-\( \binom{p_k}{k} + \binom{p_k}{k-1} - 1 = \binom{p_k + 1}{k} - 1 \). הקטעים של \( p \) שונים לא
    חופפים, ולכן הבחירה החמדנית של \( p \) היא היחידה, וממשיכים עם \( k - 1 \).

    #### סיבוכיות { .sol-cost }

    - **הבא והקודם :** ‏\( O(1) \) : חיבור אחד, XOR, הזזה וחילוק בחזקה של 2. בחומרה החילוק הוא
      הזזה ב-\( t \), ‏\( t \) יוצא מ-priority encoder, והנתיב הארוך הוא ה-carry של החיבור.
    - **המקום :** ‏\( O(w) \) חיבורים, עם טבלה של \( \binom{p}{i} \).
    - **המספר מהמקום :** ‏\( O(w \cdot k) \) בגרסה שבקוד. אם מחפשים את \( p \) מלמעלה למטה, הוא
      רק יורד, ומספיקים \( O(w) \) צעדים.

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
    ל-\( 2^{w-2} \) : מ-\( 0100 \dots 0 \) ל-\( 1000 \dots 0 \).

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
