---
id: 89
title: מטבעות שאי אפשר להרכיב – 3 ו-5, כל זוג מטבעות, ו-6, 9 ו-20
level: junior
difficulty: medium
kind: math
tags: [number-theory, dijkstra, dynamic-programming, math, python, systemverilog]
source: "בעיית המטבעות של Frobenius; הנוסחה לשני מטבעות והספירה מופיעות אצל Sylvester (1884); 6, 9 ו-20 הן חידת ה-McNuggets הידועה"
added: 2026-11-06
---

## השאלה

בקופה יש רק מטבעות של 3 ושל 5, מכל סוג כמה שרוצים, ואין עודף. סכום \( n \) **אפשר
לשלם** אם יש מספרים שלמים \( x, y \ge 0 \) כך ש-\( n = 3x + 5y \). את 8 אפשר לשלם
(\( 3 + 5 \)), ואת 4 אי אפשר.

השאלה בשלושה סעיפים : קודם המטבעות 3 ו-5, אחר כך כל זוג מטבעות \( a \) ו-\( b \),
ובסוף שלושה מטבעות ויותר, עם קוד שמוצא את התשובה לכל רשימה של מטבעות.

??? interviewer "מה המראיין בודק"
    - **ניסוי מסודר :** האם המועמד כותב את הסכומים לפי הסדר ושם לב שאחרי רצף של סכומים
      שאפשר, הכול אפשר.
    - **ארגון לפי שארית :** האם הוא מסדר את הסכומים לפי השארית בחלוקה למטבע הקטן, ורואה
      שבכל עמודה מספיק לדעת מה הסכום הראשון שאפשר.
    - **הוכחה בשני הכיוונים :** לנוסחה של שני מטבעות צריך גם "את \( g \) אי אפשר" וגם "כל
      מה שגדול מ-\( g \) אפשר". האם הוא מזכיר מה קורה כשה-gcd גדול מ-1.
    - **מתמטיקה לאלגוריתם :** לשלושה מטבעות אין נוסחה. האם הוא הופך את התמונה של העמודות
      למסלולים קצרים על השאריות, ויודע להשוות את זה לריצה פשוטה על כל הסכומים.

---

### סעיף א – מטבעות של 3 ו-5

מהו הסכום הגדול ביותר שאי אפשר לשלם במטבעות של 3 ו-5? הוכיחו שכל סכום גדול ממנו אפשר.

??? tip "רמז 1"
    כתבו את הסכומים מ-0 עד 15, וסמנו כל סכום שאפשר לשלם.

??? tip "רמז 2"
    אם אפשר לשלם את \( n \), אפשר גם את \( n + 3 \). כמה סכומים רצופים שאפשר לשלם מספיקים
    כדי שכל סכום גדול יותר יהיה אפשרי?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **‏7.** אי אפשר לשלם רק 1, 2, 4 ו-7. אחר כך \( 8 = 3 + 5 \), \( 9 = 3 + 3 + 3 \)
        ו-\( 10 = 5 + 5 \) הם שלושה סכומים רצופים שאפשר, ומכל אחד מהם מוסיפים מטבעות של 3
        ומקבלים את כל הסכומים הגדולים יותר.

    <!-- cost: סכומים שאי אפשר 4 | הגדול 7 -->

    #### הרעיון { .sol-idea }

    אם אפשר לשלם את \( n \), מוסיפים עוד מטבע של 3 ומשלמים את \( n + 3 \). לכן ברגע שיש
    **שלושה** סכומים רצופים שאפשר לשלם, כל סכום גדול יותר הוא אחד מהם ועוד כמה מטבעות של 3.
    נשאר למצוא את הרצף הראשון כזה, ולוודא שהסכום שלפניו באמת אי אפשר.

    <!-- gen 0 -->

    <div class="gs-scroll" tabindex="0" role="region" aria-label="הסכומים מ-0 עד 14 במטבעות של 3 ו-5 : אי אפשר לשלם 1, 2, 4 ו-7, ואת 8, 9 ו-10 אפשר, ומהם כל סכום גדול יותר"><table class="gs-bits fb-tab fb-line" dir="ltr" aria-label="הסכומים מ-0 עד 14 במטבעות של 3 ו-5 : אי אפשר לשלם 1, 2, 4 ו-7, ואת 8, 9 ו-10 אפשר, ומהם כל סכום גדול יותר"><tbody><tr><th></th><td class="fb-ix">0</td><td class="fb-ix">1</td><td class="fb-ix">2</td><td class="fb-ix">3</td><td class="fb-ix">4</td><td class="fb-ix">5</td><td class="fb-ix">6</td><td class="fb-ix">7</td><td class="fb-ix">8</td><td class="fb-ix">9</td></tr><tr><th>0</th><td class="gs-b fb-ok">0</td><td class="gs-b fb-no">1</td><td class="gs-b fb-no">2</td><td class="gs-b fb-ok">3</td><td class="gs-b fb-no">4</td><td class="gs-b fb-ok">5</td><td class="gs-b fb-ok">6</td><td class="gs-b fb-no fb-g">7</td><td class="gs-b fb-ok fb-run">8</td><td class="gs-b fb-ok fb-run">9</td></tr><tr><th>10</th><td class="gs-b fb-ok fb-run">10</td><td class="gs-b fb-ok">11</td><td class="gs-b fb-ok">12</td><td class="gs-b fb-ok">13</td><td class="gs-b fb-ok">14</td><td class="gs-b fb-pad"></td><td class="gs-b fb-pad"></td><td class="gs-b fb-pad"></td><td class="gs-b fb-pad"></td><td class="gs-b fb-pad"></td></tr></tbody></table></div>

    <span class="viz-legend"><span><i class="fb-key-ok"></i><span>אפשר לשלם</span></span><span><i class="fb-key-no"></i><span>אי אפשר לשלם</span></span><span><i class="fb-key-g"></i><span>הסכום הגדול ביותר שאי אפשר, 7</span></span><span><i class="fb-key-run"></i><span>3 סכומים ברצף שאפשר, ומכאן הכול אפשר</span></span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הסכומים הקטנים :** ‏0 אפשר (בלי מטבעות), 3 ו-5 אפשר, 6 = 3 + 3. את 1, 2 ו-4 אי
       אפשר, כי הם קטנים מ-5 ולא מתחלקים ב-3.
    2. **הרצף :** ‏8, 9 ו-10 אפשר. מכאן כל סכום גדול יותר הוא אחד מהם ועוד מטבעות של 3.
    3. **הסכום שלפני הרצף :** ‏7. במטבעות של 5 אפשר להשתמש 0 או 1 פעמים, ונשאר 7 או 2, ואף
       אחד מהם לא מתחלק ב-3. לכן את 7 אי אפשר לשלם.

    </div>

    #### למה זה נכון { .sol-proof }

    **לפי שארית.** מסדרים את הסכומים בשלוש עמודות לפי השארית שלהם בחלוקה ל-3. בתוך עמודה
    הסכומים קופצים ב-3, ולכן ברגע שסכום אחד בעמודה אפשרי, כל מה שמתחתיו אפשרי. כל עמודה
    מתחילה בסכום הראשון שלה שאפשר לשלם :

    - **שארית 0 :** ‏0, בלי מטבעות.
    - **שארית 2 :** ‏5, מטבע אחד של 5.
    - **שארית 1 :** ‏10, שני מטבעות של 5. במטבע אחד של 5 נשארת שארית 2, ובלי מטבעות של 5
      נשארת שארית 0.

    <!-- gen 1 -->

    <div class="gs-scroll" tabindex="0" role="region" aria-label="הסכומים לפי השארית שלהם בחלוקה ל-3 : בעמודה של 0 הכול אפשר, בעמודה של 1 הראשון שאפשר הוא 10, ובעמודה של 2 הראשון הוא 5"><table class="gs-bits fb-tab fb-res" dir="ltr" aria-label="הסכומים לפי השארית שלהם בחלוקה ל-3 : בעמודה של 0 הכול אפשר, בעמודה של 1 הראשון שאפשר הוא 10, ובעמודה של 2 הראשון הוא 5"><tbody><tr><th>r</th><td class="fb-ix">0</td><td class="fb-ix">1</td><td class="fb-ix">2</td></tr><tr><th></th><td class="gs-b fb-ok fb-first">0</td><td class="gs-b fb-no">1</td><td class="gs-b fb-no">2</td></tr><tr><th></th><td class="gs-b fb-ok">3</td><td class="gs-b fb-no">4</td><td class="gs-b fb-ok fb-first">5</td></tr><tr><th></th><td class="gs-b fb-ok">6</td><td class="gs-b fb-no fb-g">7</td><td class="gs-b fb-ok">8</td></tr><tr><th></th><td class="gs-b fb-ok">9</td><td class="gs-b fb-ok fb-first">10</td><td class="gs-b fb-ok">11</td></tr><tr><th></th><td class="gs-b fb-ok">12</td><td class="gs-b fb-ok">13</td><td class="gs-b fb-ok">14</td></tr></tbody></table></div>

    <span class="viz-legend"><span><i class="fb-key-first"></i><span>הסכום הראשון שאפשר בעמודה, וכל מה שמתחתיו אפשר (מוסיפים 3)</span></span><span><i class="fb-key-no"></i><span>אי אפשר לשלם</span></span><span><i class="fb-key-g"></i><span>הסכום הגדול ביותר שאי אפשר</span></span></span>

    <!-- /gen -->

    הסכום הראשון האחרון הוא 10, בעמודה של שארית 1. כל מה שמעליו בעמודה אי אפשר, והגדול
    שבהם הוא \( 10 - 3 = 7 \). בשתי העמודות האחרות הכול אפשרי כבר מ-5 ומטה. לכן 7 הוא
    הסכום הגדול ביותר שאי אפשר לשלם, וארבעת הסכומים שאי אפשר הם 1, 2, 4 ו-7.

    #### סיבוכיות { .sol-cost }

    מספיק לבדוק 11 סכומים, מ-0 עד 10, ביד.

---

### סעיף ב – שני מטבעות כלליים

עכשיו המטבעות הם \( a \) ו-\( b \), בלי מחלק משותף (\( \gcd(a, b) = 1 \)).

1. הוכיחו שהסכום הגדול ביותר שאי אפשר לשלם הוא \( g = ab - a - b \).
2. כמה סכומים אי אפשר לשלם בסך הכול?
3. מה קורה כש-\( \gcd(a, b) > 1 \)?
4. כתבו פונקציה שמחזירה את \( g \) ואת מספר הסכומים שאי אפשר.

??? tip "רמז 1"
    סדרו את הסכומים בעמודות לפי השארית בחלוקה ל-\( a \), כמו בסעיף א. באיזו עמודה נמצא
    \( k \cdot b \), לכל \( k \) מ-0 עד \( a - 1 \)?

??? tip "רמז 2"
    לספירה : השוו בין \( n \) לבין \( g - n \). האם אפשר לשלם את שניהם? האם יכול להיות שאי
    אפשר לשלם אף אחד מהם?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏\( g = ab - a - b \), ובדיוק \( (a - 1)(b - 1)/2 \) סכומים אי אפשר לשלם : חצי
        מהסכומים מ-0 עד \( g \), כי לכל \( n \) בטווח הזה בדיוק אחד מ-\( n \) ו-\( g - n \)
        אפשרי. ב-3 ו-5 : ‏\( g = 7 \) וארבעה סכומים. כש-\( \gcd(a, b) = d > 1 \) אפשר לשלם
        רק כפולות של \( d \), ולכן יש אינסוף סכומים שאי אפשר, ואין גדול ביותר.

    <!-- cost: זמן \( O(1) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    בעמודה של שארית \( r \) בחלוקה ל-\( a \), הסכום הראשון שאפשר לשלם הוא כפולה של \( b \).
    הכפולות \( 0, b, 2b, \dots, (a - 1)b \) נופלות כל אחת בעמודה אחרת, כי \( a \) ו-\( b \)
    זרים, ולכן הן ראשי העמודות. הראש הגבוה ביותר הוא \( (a - 1)b \), והסכום שמעליו באותה
    עמודה, \( (a - 1)b - a = ab - a - b \), הוא הגדול ביותר שאי אפשר. בטבלה המספרים באים
    מספירה ישירה של כל הסכומים, ובכל שורה עם gcd 1 הם שווים לנוסחאות. למשל ב-7 ו-11 :
    \( 7 \cdot 11 - 7 - 11 = 59 \), ו-\( 6 \cdot 10 / 2 = 30 \).

    <!-- gen 2 -->

    | המטבעות | הגדול שאי אפשר | כמה סכומים אי אפשר |
    |:-:|:-:|:-:|
    | ‏<span dir="ltr">3, 5</span> | 7 | 4 |
    | ‏<span dir="ltr">4, 7</span> | 17 | 9 |
    | ‏<span dir="ltr">5, 8</span> | 27 | 14 |
    | ‏<span dir="ltr">2, 9</span> | 7 | 4 |
    | ‏<span dir="ltr">7, 11</span> | 59 | 30 |
    | ‏<span dir="ltr">6, 9</span> | אין, ה-gcd הוא 3 | אינסוף |
    | ‏<span dir="ltr">4, 10</span> | אין, ה-gcd הוא 2 | אינסוף |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **בדיקת gcd :** אם \( \gcd(a, b) > 1 \), אין סכום גדול ביותר, ומחזירים "אין".
    2. **הנוסחה :** \( g = ab - a - b \).
    3. **הספירה :** \( (a - 1)(b - 1)/2 \) סכומים שאי אפשר לשלם.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="two_coins" linenums="1" hl_lines="9 14"
        from math import gcd


        def two_coins(a, b):
            """(the largest amount coins of a and b cannot pay, how many amounts they cannot pay),
            or None when gcd(a, b) > 1: then only multiples of the gcd, and no largest."""
            if gcd(a, b) != 1:
                return None                                       # (1)!
            return a * b - a - b, (a - 1) * (b - 1) // 2          # (2)!


        def can_pay_two(n, a, b):
            """Is n = x·a + y·b with x, y >= 0? Enough to try y = 0 .. a - 1."""
            return any(n - y * b >= 0 and (n - y * b) % a == 0 for y in range(a))   # (3)!
        ```

        1. כל סכום שמשלמים הוא כפולה של \( \gcd(a, b) \). סכום שאינו כפולה, אי אפשר לשלם
           לעולם, ויש אינסוף כאלה.
        2. ‏\( (a - 1)(b - 1) \) תמיד זוגי : כש-\( a \) ו-\( b \) זרים, לפחות אחד מהם אי-זוגי.
        3. אם \( y \ge a \), אפשר להחליף \( a \) מטבעות של \( b \) ב-\( b \) מטבעות של
           \( a \). לכן מספיק לנסות \( y \) מ-0 עד \( a - 1 \).

    === "SystemVerilog"
        ```systemverilog title="function automatic bit two_coins" linenums="1" hl_lines="9 10"
        function automatic int gcd2(int a, int b);
          return b == 0 ? a : gcd2(b, a % b);
        endfunction

        // g: the largest amount coins of a and b cannot pay, count: how many amounts they cannot
        // pay. Returns 0 when gcd(a, b) > 1: then only multiples of the gcd, and no largest.
        function automatic bit two_coins(int a, int b, output int g, output int count);
          if (gcd2(a, b) != 1) return 0;          // (1)!
          g = a * b - a - b;
          count = (a - 1) * (b - 1) / 2;
          return 1;
        endfunction

        // Is n = x·a + y·b with x, y >= 0? Enough to try y = 0 .. a - 1.
        function automatic bit can_pay_two(int n, int a, int b);
          for (int y = 0; y < a; y++)
            if (n - y * b >= 0 && (n - y * b) % a == 0) return 1;
          return 0;
        endfunction
        ```

        1. ‏SystemVerilog לא מחזיר "אין". הפונקציה מחזירה ביט, והתוצאות יוצאות בפרמטרים.

    #### למה זה נכון { .sol-proof }

    **את \( g \) אי אפשר לשלם.** נניח ש-\( ab - a - b = xa + yb \) עם \( x, y \ge 0 \). אז
    \( ab = (x + 1)a + (y + 1)b \). הצד השמאלי מתחלק ב-\( a \), ולכן \( a \) מחלק את
    \( (y + 1)b \), וכי \( a \) ו-\( b \) זרים, \( a \) מחלק את \( y + 1 \) : כלומר
    \( y + 1 \ge a \). באותו אופן \( x + 1 \ge b \). אבל אז
    \( (x + 1)a + (y + 1)b \ge ba + ab = 2ab \), גדול מ-\( ab \). סתירה.

    **כל סכום גדול מ-\( g \) אפשר.** הכפולות \( kb \) עבור \( k = 0, 1, \dots, a - 1 \)
    נותנות שאריות שונות בחלוקה ל-\( a \) : אם \( k_1 b \) ו-\( k_2 b \) נותנות אותה שארית,
    \( a \) מחלק את \( (k_1 - k_2) b \), ולכן את \( k_1 - k_2 \), שהוא קטן מ-\( a \) בערך
    מוחלט, כלומר \( k_1 = k_2 \). יש \( a \) כפולות ו-\( a \) שאריות, ולכן בכל עמודה יש
    כפולה אחת, וכל סכום בעמודה שגדול ממנה או שווה לה הוא \( kb \) ועוד מטבעות של \( a \).
    הכפולה הגדולה היא \( (a - 1)b \), ולכן כל סכום שגדול מ-\( (a - 1)b - a = g \) אפשרי.

    **הספירה.** כל מספר שלם \( n \) אפשר לכתוב בדרך אחת בדיוק כ-\( n = xa + yb \) עם
    \( 0 \le x \le b - 1 \) ו-\( y \) שלם כלשהו (אולי שלילי), ו-\( n \) אפשר לשלם אם ורק אם
    \( y \ge 0 \). עכשיו
    \( g - n = (b - 1 - x)a + (-1 - y)b \), וגם כאן \( 0 \le b - 1 - x \le b - 1 \). לכן
    את \( g - n \) אפשר לשלם אם ורק אם \( -1 - y \ge 0 \), כלומר \( y < 0 \). בכל זוג
    \( n \) ו-\( g - n \) בדיוק אחד אפשרי, ולכן בדיוק חצי מ-\( g + 1 \) הסכומים מ-0 עד
    \( g \) אי אפשר : ‏\( (g + 1)/2 = (a - 1)(b - 1)/2 \). כך זה נראה ב-4 ו-7, עם \( g = 17 \) :

    <!-- gen 3 -->

    <div class="gs-scroll" tabindex="0" role="region" aria-label="מטבעות של 4 ו-7, הסכום הגדול שאי אפשר 17. בכל עמודה זוג שמסתכם ל-17, ובכל זוג בדיוק אחד אפשר לשלם"><table class="gs-bits fb-tab fb-sym" dir="ltr" aria-label="מטבעות של 4 ו-7, הסכום הגדול שאי אפשר 17. בכל עמודה זוג שמסתכם ל-17, ובכל זוג בדיוק אחד אפשר לשלם"><tbody><tr><th>n</th><td class="gs-b fb-ok">0</td><td class="gs-b fb-no">1</td><td class="gs-b fb-no">2</td><td class="gs-b fb-no">3</td><td class="gs-b fb-ok">4</td><td class="gs-b fb-no">5</td><td class="gs-b fb-no">6</td><td class="gs-b fb-ok">7</td><td class="gs-b fb-ok">8</td></tr><tr><th>17 − n</th><td class="gs-b fb-no">17</td><td class="gs-b fb-ok">16</td><td class="gs-b fb-ok">15</td><td class="gs-b fb-ok">14</td><td class="gs-b fb-no">13</td><td class="gs-b fb-ok">12</td><td class="gs-b fb-ok">11</td><td class="gs-b fb-no">10</td><td class="gs-b fb-no">9</td></tr></tbody></table></div>

    <span class="viz-legend"><span><i class="fb-key-ok"></i><span>אפשר לשלם</span></span><span><i class="fb-key-no"></i><span>אי אפשר לשלם</span></span></span>

    <!-- /gen -->

    **כש-\( \gcd(a, b) = d > 1 \).** כל סכום שמשלמים הוא \( xa + yb \), כפולה של \( d \). אף
    סכום שאינו כפולה של \( d \) אי אפשר לשלם, ויש אינסוף כאלה. בין הכפולות של \( d \)
    השאלה חוזרת למטבעות \( a/d \) ו-\( b/d \).

    **נסו בעצמכם.** הקלידו מטבעות, ושני עד ארבעה ערכים. כל סכום צבוע לפי אם אפשר לשלם אותו,
    הסכום הגדול שאי אפשר ממוסגר, ומיד אחריו מסומן הרצף של סכומים שאפשר, באורך המטבע הקטן :

    <div class="explorer" data-kind="frobenius" data-mode="line" data-coins="4,7"></div>

    #### סיבוכיות { .sol-cost }

    הנוסחה היא \( O(1) \). הבדיקה של סכום אחד ב-`can_pay_two` היא \( O(a) \).

---

### סעיף ג – שלושה מטבעות ויותר

עכשיו המטבעות הם 6, 9 ו-20. מהו הסכום הגדול ביותר שאי אפשר לשלם? כתבו פונקציה שמקבלת כל
רשימה של מטבעות ומחזירה את הסכום הזה, והשוו אותה לריצה פשוטה על כל הסכומים לפי הסדר.

??? tip "רמז 1"
    סדרו את הסכומים בשש עמודות לפי השארית בחלוקה ל-6, המטבע הקטן. מה צריך לדעת על כל עמודה?

??? tip "רמז 2"
    מטבע של \( c \) מעביר מעמודה \( r \) לעמודה \( (r + c) \bmod 6 \), ועולה \( c \). מה
    מחפשים בגרף שבו העמודות הן הצמתים?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        **‏43.** לשלושה מטבעות ויותר אין נוסחה. מחשבים לכל שארית \( r \) בחלוקה למטבע
        הקטן \( a \) את הסכום הקטן ביותר שאפשר לשלם, \( \mathrm{dist}[r] \), בעזרת Dijkstra
        על \( a \) השאריות. סכום \( n \) אפשר לשלם אם ורק אם
        \( n \ge \mathrm{dist}[n \bmod a] \), והגדול שאי אפשר הוא
        \( \max \mathrm{dist} - a \). ב-6, 9 ו-20 הסכומים הקטנים הם 0, 49, 20, 9, 40 ו-29,
        ו-\( 49 - 6 = 43 \).

    <!-- cost: זמן \( O(k \cdot a \log a) \) | זיכרון \( O(a) \) -->

    #### הרעיון { .sol-idea }

    זו אותה תמונה של סעיף א, עם שש עמודות. בכל עמודה מספיק לדעת את הסכום הראשון שאפשר
    לשלם, וכל מה שמתחתיו אפשרי. את הראשים כבר אי אפשר לקבל מכפולות של מטבע אחד : ‏49 בעמודה
    של שארית 1 הוא \( 20 + 20 + 9 \). מוצאים אותם כמסלולים קצרים : כל עמודה היא צומת,
    מטבע \( c \) הוא קשת מ-\( r \) ל-\( (r + c) \bmod a \) במחיר \( c \), והסכום הראשון
    בעמודה הוא המרחק אליה מעמודה 0.

    <!-- gen 4 -->

    <div class="gs-scroll" tabindex="0" role="region" aria-label="הסכומים במטבעות של 6, 9 ו-20 לפי השארית בחלוקה ל-6. הסכומים הראשונים שאפשר בכל עמודה : 0, 49, 20, 9, 40 ו-29. הגדול מהם 49, ולכן 43 הוא הגדול שאי אפשר"><table class="gs-bits fb-tab fb-res" dir="ltr" aria-label="הסכומים במטבעות של 6, 9 ו-20 לפי השארית בחלוקה ל-6. הסכומים הראשונים שאפשר בכל עמודה : 0, 49, 20, 9, 40 ו-29. הגדול מהם 49, ולכן 43 הוא הגדול שאי אפשר"><tbody><tr><th>r</th><td class="fb-ix">0</td><td class="fb-ix">1</td><td class="fb-ix">2</td><td class="fb-ix">3</td><td class="fb-ix">4</td><td class="fb-ix">5</td></tr><tr><th></th><td class="gs-b fb-ok fb-first">0</td><td class="gs-b fb-no">1</td><td class="gs-b fb-no">2</td><td class="gs-b fb-no">3</td><td class="gs-b fb-no">4</td><td class="gs-b fb-no">5</td></tr><tr><th></th><td class="gs-b fb-ok">6</td><td class="gs-b fb-no">7</td><td class="gs-b fb-no">8</td><td class="gs-b fb-ok fb-first">9</td><td class="gs-b fb-no">10</td><td class="gs-b fb-no">11</td></tr><tr><th></th><td class="gs-b fb-ok">12</td><td class="gs-b fb-no">13</td><td class="gs-b fb-no">14</td><td class="gs-b fb-ok">15</td><td class="gs-b fb-no">16</td><td class="gs-b fb-no">17</td></tr><tr><th></th><td class="gs-b fb-ok">18</td><td class="gs-b fb-no">19</td><td class="gs-b fb-ok fb-first">20</td><td class="gs-b fb-ok">21</td><td class="gs-b fb-no">22</td><td class="gs-b fb-no">23</td></tr><tr><th></th><td class="gs-b fb-ok">24</td><td class="gs-b fb-no">25</td><td class="gs-b fb-ok">26</td><td class="gs-b fb-ok">27</td><td class="gs-b fb-no">28</td><td class="gs-b fb-ok fb-first">29</td></tr><tr><th></th><td class="gs-b fb-ok">30</td><td class="gs-b fb-no">31</td><td class="gs-b fb-ok">32</td><td class="gs-b fb-ok">33</td><td class="gs-b fb-no">34</td><td class="gs-b fb-ok">35</td></tr><tr><th></th><td class="gs-b fb-ok">36</td><td class="gs-b fb-no">37</td><td class="gs-b fb-ok">38</td><td class="gs-b fb-ok">39</td><td class="gs-b fb-ok fb-first">40</td><td class="gs-b fb-ok">41</td></tr><tr><th></th><td class="gs-b fb-ok">42</td><td class="gs-b fb-no fb-g">43</td><td class="gs-b fb-ok">44</td><td class="gs-b fb-ok">45</td><td class="gs-b fb-ok">46</td><td class="gs-b fb-ok">47</td></tr><tr><th></th><td class="gs-b fb-ok">48</td><td class="gs-b fb-ok fb-first">49</td><td class="gs-b fb-ok">50</td><td class="gs-b fb-ok">51</td><td class="gs-b fb-ok">52</td><td class="gs-b fb-ok">53</td></tr></tbody></table></div>

    <span class="viz-legend"><span><i class="fb-key-first"></i><span>הסכום הראשון שאפשר בעמודה, וכל מה שמתחתיו אפשר (מוסיפים 6)</span></span><span><i class="fb-key-no"></i><span>אי אפשר לשלם</span></span><span><i class="fb-key-g"></i><span>הסכום הגדול ביותר שאי אפשר</span></span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **בדיקת gcd :** אם ה-gcd של כל המטבעות גדול מ-1, אין סכום גדול ביותר.
    2. **התחלה :** \( a \) הוא המטבע הקטן. \( \mathrm{dist}[0] = 0 \), ושאר השאריות
       אינסוף.
    3. **‏Dijkstra :** מוציאים מהתור את השארית עם המרחק הקטן. לכל מטבע \( c \) מנסים לשפר
       את השארית \( (r + c) \bmod a \) למרחק \( \mathrm{dist}[r] + c \).
    4. **התשובה :** \( g = \max_r \mathrm{dist}[r] - a \), הסכום שמעל הראש הגבוה ביותר.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="frobenius" linenums="1" hl_lines="17 18 26 34 43"
        import heapq
        from functools import reduce
        from math import gcd, inf


        def smallest_payable(coins):
            """dist[r]: the smallest amount the coins can pay with remainder r mod a = min(coins).
            Dijkstra on the a remainders: a coin c leads from r to (r + c) % a and costs c."""
            a = min(coins)
            dist = [0] + [inf] * (a - 1)
            heap = [(0, 0)]
            while heap:
                d, r = heapq.heappop(heap)
                if d > dist[r]:
                    continue                                      # (1)!
                for c in coins:
                    nr = (r + c) % a
                    if d + c < dist[nr]:
                        dist[nr] = d + c
                        heapq.heappush(heap, (d + c, nr))
            return dist


        def can_pay(n, coins):
            """n can be paid iff it is at least the smallest payable amount of its remainder."""
            return n >= smallest_payable(coins)[n % min(coins)]


        def frobenius(coins):
            """The largest amount the coins cannot pay; None when gcd(coins) > 1 (no largest),
            -1 when every amount can be paid (a coin of 1)."""
            if reduce(gcd, coins) != 1:
                return None
            return max(smallest_payable(coins)) - min(coins)      # (2)!


        def frobenius_dp(coins):
            """The same by trying amounts 1, 2, 3, ... until min(coins) payable amounts in a row."""
            if reduce(gcd, coins) != 1:
                return None
            a = min(coins)
            ok, run, n = [True], 1, 0
            while run < a:                                        # (3)!
                n += 1
                ok.append(any(c <= n and ok[n - c] for c in coins))
                run = run + 1 if ok[n] else 0
            return n - a
        ```

        1. רשומה ישנה בתור : השארית כבר נסגרה במרחק קטן יותר.
        2. הסכום שמעל הראש הגבוה ביותר, באותה עמודה, הוא הגדול שאי אפשר לשלם.
        3. ‏\( a \) סכומים רצופים שאפשר : מכאן כל סכום הוא אחד מהם ועוד מטבעות של \( a \).
           הסכום שלפני הרצף הוא התשובה.

    === "SystemVerilog"
        ```systemverilog title="function automatic bit frobenius" linenums="1" hl_lines="17 22 23 26"
        // g: the largest amount the coins cannot pay (-1 when every amount can be paid).
        // Returns 0 when the gcd of the coins is more than 1: then there is no largest.
        // best[r]: the smallest payable amount with remainder r mod a = the smallest coin
        // (dist is a keyword of SystemVerilog).
        function automatic bit frobenius(int coins[$], output int g);
          int a = coins[0], r, worst = 0;
          int best[$];
          bit done[$];
          foreach (coins[k]) if (coins[k] < a) a = coins[k];
          for (int i = 0; i < a; i++) begin
            best.push_back(i == 0 ? 0 : -1);           // -1: not reached yet
            done.push_back(0);
          end
          for (int step = 0; step < a; step++) begin
            r = -1;                                    // (1)!
            for (int i = 0; i < a; i++)
              if (!done[i] && best[i] >= 0 && (r < 0 || best[i] < best[r])) r = i;
            if (r < 0) return 0;                       // (2)!
            done[r] = 1;
            if (best[r] > worst) worst = best[r];
            foreach (coins[k]) begin
              int nr = (r + coins[k]) % a, nd = best[r] + coins[k];
              if (best[nr] < 0 || nd < best[nr]) best[nr] = nd;
            end
          end
          g = worst - a;
          return 1;
        endfunction

        // The same by trying amounts 1, 2, 3, ... until min(coins) payable amounts in a row.
        function automatic bit frobenius_dp(int coins[$], output int g);
          int a = coins[0], d = 0, run = 1, n = 0;
          bit ok[$];
          foreach (coins[k]) begin
            if (coins[k] < a) a = coins[k];
            d = gcd2(d, coins[k]);
          end
          if (d != 1) return 0;
          ok.push_back(1);
          while (run < a) begin
            bit p = 0;
            n++;
            foreach (coins[k]) if (coins[k] <= n && ok[n - coins[k]]) p = 1;
            ok.push_back(p);
            run = p ? run + 1 : 0;
          end
          g = n - a;
          return 1;
        endfunction
        ```

        1. בלי תור עדיפויות : בכל סבב סורקים את \( a \) השאריות ובוחרים את הקרובה שעוד לא
           נסגרה. זה \( O(a^2) \), ומספיק כש-\( a \) קטן.
        2. אין שארית פתוחה שהגענו אליה : יש שאריות שאף פעם לא מגיעים אליהן, וזה קורה רק
           כשה-gcd גדול מ-1.

    #### למה זה נכון { .sol-proof }

    **סכום אפשרי בדיוק מהראש של העמודה ומטה.** אם אפשר לשלם את \( n \), אפשר גם את
    \( n + a \). להפך, אם אפשר לשלם את \( n \), הוא באותה עמודה של הראש
    \( \mathrm{dist}[n \bmod a] \), ולכן לא קטן ממנו, כי הראש הוא הקטן ביותר בעמודה שאפשר.
    לכן את \( n \) אפשר לשלם אם ורק אם \( n \ge \mathrm{dist}[n \bmod a] \).

    **הראשים הם מסלולים קצרים.** כל סכום שמשלמים הוא סדרה של מטבעות, ואם מוסיפים אותם אחד
    אחד מ-0, עוברים מעמודה לעמודה : מטבע \( c \) מוביל מ-\( r \) ל-\( (r + c) \bmod a \)
    ומוסיף \( c \). לכן הסכום הקטן ביותר בעמודה \( r \) הוא אורך המסלול הקצר ביותר מ-0
    ל-\( r \), ו-Dijkstra מוצא אותו, כי כל המחירים חיוביים. מטבע של \( a \) הוא לולאה
    שחוזרת לאותה עמודה, ולא משפר אף מסלול. כך Dijkstra סוגר את השאריות של 6, 9 ו-20, לפי
    הסדר :

    <!-- gen 5 -->

    | הסדר | השארית | הראש של העמודה | איך מגיעים אליו |
    |:-:|:-:|:-:|---|
    | 1 | 0 | 0 | ההתחלה, בלי מטבעות |
    | 2 | 3 | 9 | הראש 0 של שארית 0, ועוד מטבע של 9 |
    | 3 | 2 | 20 | הראש 0 של שארית 0, ועוד מטבע של 20 |
    | 4 | 5 | 29 | הראש 9 של שארית 3, ועוד מטבע של 20 |
    | 5 | 4 | 40 | הראש 20 של שארית 2, ועוד מטבע של 20 |
    | 6 | 1 | 49 | הראש 29 של שארית 5, ועוד מטבע של 20 |

    <!-- /gen -->

    **התשובה.** בעמודה עם הראש הגבוה, \( \mathrm{dist}[r] = 49 \), הסכום שמעל הראש,
    \( 49 - 6 = 43 \), אי אפשר. בכל העמודות האחרות הראשים נמוכים יותר, ולכן כל סכום גדול
    מ-43 אפשרי. בסך הכול יש 22 סכומים שאי אפשר לשלם, מ-1 עד 43.

    **הריצה הפשוטה.** ‏`frobenius_dp` בודק את הסכומים לפי הסדר. ברגע שיש \( a \) סכומים
    רצופים שאפשר, כל סכום גדול יותר הוא אחד מהם ועוד מטבעות של \( a \), ולכן הסכום שלפני
    הרצף הוא התשובה. היא עוצרת רק כשה-gcd הוא 1, ולכן הבדיקה שלו באה קודם.

    **נסו בעצמכם.** בתיבה הראשונה Dijkstra סוגר עמודה אחרי עמודה. בכל צעד מתגלה הראש של
    עמודה, וכל מה שמתחתיו נצבע. בתיבה השנייה מקלידים סכום, ורואים איך לשלם אותו, או למה אי
    אפשר :

    <div class="explorer" data-kind="frobenius" data-mode="residues" data-coins="6,9,20"></div>

    <div class="explorer" data-kind="frobenius" data-mode="pay" data-coins="6,9,20" data-n="43"></div>

    #### סיבוכיות { .sol-cost }

    עם \( k \) מטבעות ו-\( a \) המטבע הקטן, Dijkstra מטפל ב-\( a \) צמתים ו-\( k \cdot a \)
    קשתות : \( O(k \cdot a \log a) \) זמן ו-\( O(a) \) זיכרון. הריצה הפשוטה בודקת כל סכום
    עד \( g + a \), כל אחד עם \( k \) מטבעות : \( O(k \cdot g) \), ו-\( g \) גדל בערך כמו
    המכפלה של שני מטבעות. ההבדל גדל עם המטבעות :

    <!-- gen 6 -->

    | המטבעות | הגדול שאי אפשר | סכומים שהריצה הפשוטה בודקת | שאריות ש-Dijkstra מסדר |
    |:-:|:-:|:-:|:-:|
    | ‏<span dir="ltr">3, 5</span> | 7 | 10 | 3 |
    | ‏<span dir="ltr">6, 9, 20</span> | 43 | 49 | 6 |
    | ‏<span dir="ltr">5, 7, 9</span> | 13 | 18 | 5 |
    | ‏<span dir="ltr">31, 37, 41</span> | 293 | 324 | 31 |
    | ‏<span dir="ltr">101, 103, 107</span> | 3,533 | 3,634 | 101 |

    <!-- /gen -->

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לשכוח את ה-gcd"
    במטבעות של 4 ו-6 אי אפשר לשלם אף סכום אי-זוגי, ויש אינסוף כאלה. הנוסחה
    \( ab - a - b \) נותנת כאן 14, שדווקא **אפשר** לשלם (\( 4 + 4 + 6 \)). בלי הבדיקה,
    `frobenius_dp` רצה לנצח.

??? trap "מלכודת : רצף קצר מדי"
    ב-6, 9 ו-20 הסכומים 38, 39, 40, 41 ו-42 אפשריים, חמישה ברצף, ואת 43 אי אפשר. רצף מוכיח
    שהכול אפשרי רק כשהוא באורך המטבע הקטן, כאן 6.

??? trap "מלכודת : לשלם בחמדנות"
    "קודם כמה שיותר מהמטבע הגדול" לא עובד : את 24 במטבעות של 6, 9 ו-20 החמדן מתחיל ב-20,
    נשאר עם 4 ונתקע, אבל \( 24 = 6 + 6 + 6 + 6 \). הבדיקה הנכונה היא
    \( n \ge \mathrm{dist}[n \bmod a] \), והמטבעות באים מהמסלול של Dijkstra.

??? trap "מלכודת : להמציא נוסחה לשלושה מטבעות"
    ההכללה הטבעית, \( abc - a - b - c \), נותנת ב-6, 9 ו-20 את 1045, והתשובה היא 43. הוכח
    שאין נוסחה פולינומית לשלושה מטבעות, ולכן צריך אלגוריתם.

??? followup "שאלות המשך"
    - **עוד מטבע :** מה הסכום הגדול שאי אפשר במטבעות של 4, 6, 9 ו-20?

        ??? fu-answer "תשובה"
            ‏11. עכשיו המטבע הקטן הוא 4, והראשים של ארבע העמודות הם 0, 9, 6 ו-15.
            \( 15 - 4 = 11 \).

    - **כמה דרכים :** בכמה דרכים אפשר לשלם 60 במטבעות של 6, 9 ו-20, כשהסדר לא משנה?

        ??? fu-answer "תשובה"
            חמש. ‏DP של בעיית העודף : עוברים על המטבעות אחד אחד, ולכל סכום \( n \) מוסיפים
            את מספר הדרכים של \( n - c \). המעבר על המטבעות בלולאה החיצונית סופר כל קבוצה
            פעם אחת, בלי סדר.

    - **הכי מעט מטבעות :** איך משלמים סכום במספר המטבעות הקטן ביותר?

        ??? fu-answer "תשובה"
            ‏DP על הסכומים : \( \mathrm{best}[n] = 1 + \min_c \mathrm{best}[n - c] \). גם כאן
            החמדן נכשל, למשל ב-24.

    - **מטבעות רבים :** האם הבעיה קלה כשמספר המטבעות גדל?

        ??? fu-answer "תשובה"
            לא. כשמספר המטבעות הוא חלק מהקלט, הבעיה NP-קשה. למספר קבוע של מטבעות יש
            אלגוריתם פולינומי, והשיטה של העמודות כאן היא \( O(k \cdot a \log a) \), טובה
            כשהמטבע הקטן קטן.
