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
    איך מבודדים את האחד הנמוך ביותר של \( x \) בפעולה אחת?

??? tip "רמז 3"
    מה עושה ל-\( x \) החיבור של האחד הזה? אילו ביטים משתנים?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מוצאים את בלוק האחדות הנמוך ביותר. האחד העליון שלו עולה מקום אחד, ושאר האחדות של הבלוק
        יורדים לתחתית המילה. בנוסחה : ‏`r | (((x ^ r) >> 2) / c)`, כש-`c` הוא האחד הנמוך ו-`r = x + c`.
        אם החיבור גולש מעבר ל-\( w \) ביטים, אין מספר הבא.

    <!-- cost: זמן \( O(1) \) | זיכרון \( O(1) \) | חילוק אחד, ובחומרה הזזה -->

    #### הרעיון { .sol-idea }

    **איפה השינוי.** נכתוב \( x = a\,0\,\underbrace{1 \dots 1}_{m}\,\underbrace{0 \dots 0}_{t} \) : בלוק של
    \( m \) אחדות שמתחיל במקום \( t \), ומעליו אפס. מספר גדול יותר עם אותן אחדות חייב להדליק
    ביט שהיה כבוי, והנמוך ביותר שאפשר הוא האפס שמעל הבלוק, במקום \( t + m \). מדליקים אותו,
    ואת \( m - 1 \) האחדות הנותרים של הבלוק מניחים הכי נמוך שאפשר, בתחתית.

    **הנוסחה עושה את זה בחמישה צעדים.** על 92 ב-8 ביטים :

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
    4. **לתחתית :** צריך רק \( m - 1 \) מהם, בתחתית. ‏`>> 2` מזיז שני מקומות ימינה, והחילוק
       ב-\( c \) עוד \( t \). יחד זו הזזה ב-\( t + 2 \), שמפילה את שני האחדות הנמוכים מתחת לביט 0.
       ב-92 ‏(\( t = 2 \)) השורה של `>> 2` עוד מחזיקה ארבע אחדות, ורק החילוק מפיל שניים.
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
    - **לכן \( q \ge t + m \), והקטן ביותר הוא \( q = t + m \).** \( q \) קטן יותר נותן \( y \) קטן יותר : שני
      מועמדים שווים ל-\( x \) מעל ה-\( q \) הגדול מביניהם, ובביט הזה לבעל ה-\( q \) הגדול יש 1 ולשני 0,
      כמו ב-\( x \). הביט \( t + m \) כבוי ב-\( x \), ולכן אפשר. מעל \( q \) ‏\( y \) שווה ל-\( x \),
      ‏\( k - m \) אחדות. עם \( y_q \) יש \( k - m + 1 \), ונשארו \( m - 1 \) אחדות לביטים שמתחת
      ל-\( q \). המספר הקטן ביותר שם הוא כשהם בתחתית. זה בדיוק `r | s`.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(1) \) : חיבור אחד, XOR, הזזה וחילוק בחזקה של 2.
    - **בחומרה :** החילוק הוא הזזה ב-\( t \), והכול קומבינטורי, במחזור אחד (שאלת ההמשך השנייה).
      הנתיב הארוך עובר בשלושה שלבים בטור, כל אחד בעומק לוגריתמי ברוחב : בידוד האחד הנמוך
      (‏\( -x \) היא שרשרת carry), החיבור, וה-barrel shifter. ‏\( t \) מוכן מוקדם : \( c \) הוא one-hot,
      ולכן מספיק encoder בלי עדיפות, OR לכל ביט של \( t \), במקביל לחיבור.

    <!-- gen 2 -->

    <svg class="figure pn-dp" viewBox="0 0 560 228" direction="ltr" style="max-width:35rem" role="img" aria-label="תרשים המלבנים של next_same במחזור אחד : x &amp; −x מבודד את האחד הנמוך c, ‏encoder של one-hot נותן ממנו את t, המחבר נותן r = x + c ואת ה-carry העליון none, ‏XOR של x ו-r נותן את הבלוק והביט החדש, ‏barrel shifter מזיז אותו ב-t + 2, ו-OR עם r נותן את next. שלושה שלבים בטור : הבידוד, החיבור וההזזה"><defs><marker id="pn-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="pn-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs><g class="pn-blk pn-st1"><rect x="38" y="20" width="100" height="46" rx="5"/><text x="88" y="48" text-anchor="middle">x &amp; −x</text></g><g class="pn-blk"><rect x="176" y="20" width="124" height="46" rx="5"/><text x="238" y="48" text-anchor="middle">one-hot→t</text></g><g class="pn-blk pn-st2"><rect x="176" y="96" width="100" height="58" rx="5"/><text x="226" y="122" text-anchor="middle">+</text><text class="pn-sub" x="226" y="138" text-anchor="middle">w+1 bits</text></g><g class="pn-blk"><rect x="296" y="166" width="56" height="46" rx="5"/><text x="324" y="194" text-anchor="middle">XOR</text></g><g class="pn-blk pn-st3"><rect x="392" y="160" width="96" height="58" rx="5"/><text x="440" y="186" text-anchor="middle">&gt;&gt; t+2</text><text class="pn-sub" x="440" y="202" text-anchor="middle">barrel</text></g><g class="pn-blk"><rect x="504" y="96" width="44" height="58" rx="5"/><text x="526" y="130" text-anchor="middle">OR</text></g><path class="pn-wire" d="M6,110 L176,110" marker-end="url(#pn-hb)"/><text class="pn-wlab" x="6" y="102" text-anchor="start">x</text><path class="pn-wire" d="M20,43 L20,200"/><path class="pn-wire" d="M20,43 L38,43" marker-end="url(#pn-hb)"/><path class="pn-wire" d="M20,200 L296,200" marker-end="url(#pn-hb)"/><path class="pn-wire" d="M138,43 L176,43" marker-end="url(#pn-hb)"/><text class="pn-wlab" x="157" y="35" text-anchor="middle">c</text><path class="pn-wire" d="M157,43 L157,140 L176,140" marker-end="url(#pn-hb)"/><path class="pn-wire" d="M300,43 L440,43 L440,160" marker-end="url(#pn-hb)"/><text class="pn-wlab" x="370" y="35" text-anchor="middle">t</text><path class="pn-wire" d="M250,96 L250,72" marker-end="url(#pn-hb)"/><text class="pn-wlab" x="258" y="88" text-anchor="start">none</text><path class="pn-wire" d="M276,125 L504,125" marker-end="url(#pn-hb)"/><text class="pn-wlab" x="330" y="117" text-anchor="middle">r</text><path class="pn-wire" d="M284,125 L284,178 L296,178" marker-end="url(#pn-hb)"/><path class="pn-wire" d="M352,189 L392,189" marker-end="url(#pn-hb)"/><text class="pn-wlab" x="372" y="181" text-anchor="middle">x^r</text><path class="pn-wire" d="M488,189 L496,189 L496,145 L504,145" marker-end="url(#pn-hb)"/><text class="pn-wlab" x="496" y="214" text-anchor="middle">s</text><path class="pn-wire" d="M526,96 L526,64" marker-end="url(#pn-hb)"/><text class="pn-wlab" x="526" y="56" text-anchor="middle">next</text><circle class="pn-dot" cx="20" cy="110" r="3.5"/><circle class="pn-dot" cx="157" cy="43" r="3.5"/><circle class="pn-dot" cx="284" cy="125" r="3.5"/></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="pn-key-1"></i>שלב 1 : בידוד האחד הנמוך</span><span><i class="pn-key-2"></i>שלב 2 : החיבור</span><span><i class="pn-key-3"></i>שלב 3 : ההזזה</span><span><i class="pn-key-0"></i>שער אחד בעומק, או במקביל לחיבור</span></span>

    <!-- /gen -->

---

### סעיף ב – המספר הקודם

??? tip "רמז 1"
    מה קורה לסדר בין שני מספרים כשהופכים את כל הביטים שלהם?

??? tip "רמז 2"
    אם ל-\( x \) יש \( k \) אחדות ברוחב \( w \), כמה אחדות יש ל-\( \sim x \)?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏`prev(x) = ~next(~x)`, ברוחב \( w \). ההיפוך \( \sim x = 2^w - 1 - x \) הופך את הסדר ומעביר
        מספרים עם \( k \) אחדות למספרים עם \( w - k \) אחדות. לכן הגדול ביותר מתחת ל-\( x \) הוא
        ההיפוך של הקטן ביותר מעל \( \sim x \). בלי היפוך : מוצאים את האחד הנמוך ביותר שמתחתיו
        אפס, מורידים אותו מקום אחד, ומצמידים אליו מלמטה את כל האחדות שהיו מתחתיו.

    <!-- cost: זמן \( O(1) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **הסדר מתהפך.** אם \( y < x \) אז \( \sim y > \sim x \). ברוחב 5 ביטים, המספרים עם שתי אחדות
    לפי הסדר, ולידם ההיפוך שלהם. הרשימה של ההיפוכים יורדת, כלומר הרשימה של המספרים עם שלוש
    אחדות הפוכה :

    <!-- gen 4 -->

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

    <!-- gen 5 -->

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

    #### סיבוכיות { .sol-cost }

    - **זמן וזיכרון :** ‏\( O(1) \) : שני היפוכים וקריאה אחת ל-`next_same`. בחומרה זה אותו מעגל,
      עם שורה של NOT בכניסה ושורה ביציאה.

---

### סעיף ג – אותו מספר של אפסים

??? tip "רמז 1"
    בתוך אורך קבוע \( L \) (המספרים מ-\( 2^{L-1} \) עד \( 2^L - 1 \)), מה הקשר בין מספר האפסים
    למספר האחדות?

??? tip "רמז 2"
    מה קורה כשבאורך \( L \) כבר אין מספר הבא? מה המספר הקטן ביותר באורך \( L + 1 \) עם \( z \)
    אפסים?

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

    <!-- gen 6 -->

    | האורך | המספרים עם שלושה אפסים, לפי הסדר |
    |:-:|:-:|
    | ‏4 | ‏`1000` (8) |
    | ‏5 | ‏`10001` (17), ‏`10010` (18), ‏`10100` (20), ‏`11000` (24) |
    | ‏6 | ‏`100011` (35), ‏`100101` (37), ‏`100110` (38), ‏`101001` (41), ‏`101010` (42), ‏`101100` (44), ‏`110001` (49), ‏`110010` (50), ‏`110100` (52), ‏`111000` (56) |

    <!-- /gen -->

    **בתוך אורך זו אותה שאלה.** באורך \( L \) ביט \( L - 1 \) תמיד דולק, ומספר האפסים קובע את
    מספר האחדות. לכן `next_same(x, L)` נותן את הבא באותו אורך, אם יש כזה.

    **בסוף האורך קופצים.** ל-\( 120 = 1111000_2 \) אין מספר הבא באורך 7 : החיבור של סעיף א גולש מעבר
    ל-7 ביטים. המספר הבא הוא הקטן ביותר באורך 8 עם שלושה אפסים :

    <!-- gen 7 -->

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

    - **הבא והקודם עם אחדות :** ‏\( O(1) \), כמו בסעיפים א ו-ב.
    - **עם אפסים :** אותו דבר, ועוד האורך של \( x \) : בחומרה זה priority encoder מלמעלה, שמוצא את
      האחד העליון.

    **נסו בעצמכם.**

    - **ה-carry בעבודה :** עם 92 ברוחב 8, התקדמו בשלבים עד השורה `r = x + c` : בלוק שלוש האחדות
      (ביטים 2 עד 4) נעלם וביט 5 נדלק, והתוצאה 99. לחצו "הבא" שש פעמים : 99, 101, 102, 105, 106
      ו-108. בכל צעד האחד העליון של הבלוק הנמוך עולה מקום אחד, ושאר הבלוק יורד לתחתית.
    - **בלוק בראש :** עם 240 ‏(<span dir="ltr">11110000</span>) ברוחב 8, השורה של `r` גולשת לביט 8 : אין מספר
      הבא. עברו לרוחב 10 : הבא הוא 263 ‏(<span dir="ltr">100000111</span>).
    - **אפסים :** בחרו "אפסים" ו-120 : החיבור גולש מאורך 7, והשורה האחרונה קופצת ל-143, באורך 8. עם 9 והשלבים
      של "הקודם", ההיפוך נותן 6 ‏(<span dir="ltr">110</span>), קצר יותר, והתיבה קופצת ל-4 ‏(<span dir="ltr">100</span>).
      עם 8 : אין מספר קודם, כי 8 הוא הקטן ביותר עם שלושה אפסים.

    התיבה מוסיפה על הטבלאות כל מספר ורוחב, את הקודם צעד אחר צעד, ואת המקרים שבהם אין תשובה,
    כמו \( x = 0 \).

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
            מתחילים ב-`(1 << k) - 1` (עם \( k \ge 1 \)) וקוראים ל-`next_same` עד שהתוצאה היא 0 או עוברת
            את `1 << n`. בלי הבדיקה של 0 הלולאה לא נגמרת כש-\( n = w \) : אחרי הצירוף האחרון
            `next_same` מחזיר 0. יש בדיוק \( \binom{n}{k} \) צעדים, כל אחד \( O(1) \), לפי הסדר העולה.

            בחומרה זה רגיסטר `mask` אחד : ‏`mask <= next` בכל שעון, עם המעגל של שאלת ההמשך הבאה
            ברוחב \( n \), עד ש-`none` עולה. שלושה ערוצים מתוך חמישה, צירוף בכל שעון :

            <!-- gen 8 -->

            | מחזור | ‏mask | ‏c | ‏r | ‏next | ‏none |
            |:-:|:-:|:-:|:-:|:-:|:-:|
            | ‏0 | ‏00111 | ‏00001 | ‏001000 | ‏01011 | ‏0 |
            | ‏1 | ‏01011 | ‏00001 | ‏001100 | ‏01101 | ‏0 |
            | ‏2 | ‏01101 | ‏00001 | ‏001110 | ‏01110 | ‏0 |
            | ‏3 | ‏01110 | ‏00010 | ‏010000 | ‏10011 | ‏0 |
            | ‏4 | ‏10011 | ‏00001 | ‏010100 | ‏10101 | ‏0 |
            | ‏5 | ‏10101 | ‏00001 | ‏010110 | ‏10110 | ‏0 |
            | ‏6 | ‏10110 | ‏00010 | ‏011000 | ‏11001 | ‏0 |
            | ‏7 | ‏11001 | ‏00001 | ‏011010 | ‏11010 | ‏0 |
            | ‏8 | ‏11010 | ‏00010 | ‏011100 | ‏11100 | ‏0 |
            | ‏9 | ‏11100 | ‏00100 | ‏100000 | ‏00000 | ‏1 |

            <!-- /gen -->

    - **בחומרה, במחזור אחד ובלי חילוק :** איך?

        ??? fu-answer "תשובה"
            ‏\( s = (x \oplus r) \gg (t + 2) \), כש-\( t \) הוא מספר האפסים בתחתית של \( x \). ‏\( c \)
            הוא one-hot, ולכן \( t \) יוצא מ-encoder בלי עדיפות. הכול קומבינטורי : AND, חיבור, XOR,
            ‏barrel shifter ו-OR (התרשים בסיבוכיות של סעיף א).

            ```systemverilog title="module next_same_1c" linenums="1" hl_lines="12 14 15"
            // one clock, no divider: s = (x ^ r) >> (t + 2), t from an encoder of the one-hot c
            module next_same_1c #(parameter int W = 32) (
              input  logic [W-1:0] x,
              output logic [W-1:0] nxt,
              output logic         none          // no larger number with as many ones in W bits
            );
              localparam int TW = $clog2(W);
              logic [W-1:0]  c;
              logic [W:0]    r;
              logic [TW-1:0] t;
              always_comb begin
                c = x & -x;
                t = '0;
                for (int p = 0; p < W; p++) if (c[p]) t = t | TW'(p);   // (1)!
                r = {1'b0, x} + {1'b0, c};
                none = (x == '0) || r[W];
                nxt = none ? '0 : r[W-1:0] | ((x ^ r[W-1:0]) >> (t + 2));
              end
            endmodule
            ```

            1. ביט \( j \) של \( t \) הוא OR של הביטים של \( c \) שבמקום שלהם ביט \( j \) דולק. בלי עדיפות, כי רק ביט אחד של \( c \) דולק.

    - **אימות :** איך בודקים את `next_same_1c` בסימולציה?

        ??? fu-answer "תשובה"
            שלוש assertions שבודקות כל תשובה בלי מודל : ‏`next > x`, אותו מספר של אחדות, ו-`none` בדיוק
            כשבלוק האחדות הנמוך נוגע בביט העליון (או \( x = 0 \)). המינימליות נבדקת מול מודל ייחוס :
            חיפוש מלא ברוחב קטן (ב-12 ביטים, 4096 מספרים), ומספרים אקראיים ב-32. ה-covergroup דואג שהגירוי הגיע למקרי הקצה :
            ‏\( t = 0 \), \( t \) באמצע ובראש, בלוק של אחד בודד, בלוק בראש, וכל הביטים דולקים.

            ```systemverilog title="module next_same_sva" linenums="1" hl_lines="6 7 8"
            // bound to next_same_1c: the rules every answer keeps, and the cases a test must reach
            module next_same_sva #(parameter int W = 32) (
              input logic clk, input logic [W-1:0] x, nxt, input logic none
            );
              int fails = 0;
              a_above: assert property (@(posedge clk) !none |-> nxt > x) else fails++;
              a_ones:  assert property (@(posedge clk) !none |-> $countones(nxt) == $countones(x)) else fails++;
              a_none:  assert property (@(posedge clk) none == (x == '0 || &(x | (x - 1'b1)))) else fails++;   // (1)!

              covergroup cg @(posedge clk);
                cp_t:   coverpoint $clog2(x & -x) iff (x != '0) { bins zero = {0}; bins mid = {[1:W-2]}; bins top = {W-1}; }
                cp_m:   coverpoint ((x & ((x & -x) << 1)) == '0) iff (x != '0) { bins single = {1}; bins block = {0}; }
                cp_end: coverpoint none iff (x != '0) { bins next = {0}; bins at_top = {1}; }
                cp_all: coverpoint &x { bins all_ones = {1}; }
              endgroup
              cg cov = new();
            endmodule
            ```

            1. ‏`x | (x - 1)` מדליק את האפסים שמתחת לאחד הנמוך. כולו אחדות בדיוק כשמעל האחד הנמוך הכול דולק, כלומר הבלוק נוגע בראש.

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
