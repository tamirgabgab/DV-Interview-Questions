---
id: 81
title: N מלכות – ספירה בביטים, סימטריות ובנייה לכל N
level: junior
difficulty: medium
kind: code
tags: [recursion, bitwise, combinatorics, algorithms, python, systemverilog]
source: "חידה קלאסית (בצל, 1848); הבנייה המפורשת לכל N לפי N mod 6"
added: 2026-11-04
---

## השאלה

מציבים \( N \) מלכות על לוח שחמט של \( N \) על \( N \), כך שאף שתיים לא מאיימות זו על זו : לא
באותה שורה, לא באותה עמודה ולא באותו אלכסון. על לוח שחמט רגיל \( N = 8 \).

בכל הדף העמודה \( c \) היא הביט \( c \) של מסכה, והעמודה 0 מצוירת מימין, כמו הביט הנמוך של
מספר בינארי. כך כל שורה של הלוח עומדת מעל הביטים של המסכות שלה.

??? interviewer "מה המראיין בודק"
    - **‏backtracking נקי :** שורה אחרי שורה, מלכה אחת בכל שורה, וחזרה אחורה כשאין לאן. המראיין
      בודק שהמועמד לא מנסה את כל \( 64 \) המשבצות לכל מלכה.
    - **ביטים :** שלוש מסכות במקום לבדוק כל זוג מלכות, ו-`x & -x` לביט הנמוך. זה גם מה שנכתב
      בחומרה.
    - **שני האלכסונים :** הטעות הנפוצה היא לבדוק רק כיוון אחד.
    - **סימטריה :** לראות ש-92 פתרונות הם 12 פתרונות "באמת", ולהסביר למה \( 12 \cdot 8 \ne 92 \).
    - **מתמטיקה :** בנייה לכל \( N \) בלי חיפוש, והוכחה שהיא נכונה.

---

### סעיף א – כמה פתרונות יש ל-8 מלכות

כתבו פונקציה שסופרת את הפתרונות לכל \( N \), וחשבו כמה יש ל-\( N = 8 \). כמה עבודה החיפוש
עושה?

??? tip "רמז 1"
    בכל שורה יש בדיוק מלכה אחת. מציבים שורה אחרי שורה, ואם בשורה אין משבצת פנויה, חוזרים
    לשורה הקודמת ומנסים בה עמודה אחרת.

??? tip "רמז 2"
    איך יודעים מהר אילו עמודות פנויות בשורה הבאה? שלוש קבוצות : העמודות התפוסות, ושני כיווני
    האלכסון. כל קבוצה יכולה להיות מסכת ביטים.

??? tip "רמז 3"
    כשיורדים שורה, איום באלכסון זז בעמודה אחת : מסכה אחת זזה ביט שמאלה (`<< 1`) והשנייה ביט
    ימינה (`>> 1`). ‏`x & -x` הוא הביט הנמוך של \( x \).

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        יש 92 פתרונות. מציבים שורה אחרי שורה עם שלוש מסכות : `cols` לעמודות התפוסות, ו-`left`
        ו-`right` לשני האלכסונים. העמודות הפנויות הן `full & ~(cols | left | right)`, ובכל שורה
        מנסים אותן מהביט הנמוך. ל-8 מלכות החיפוש מציב רק 2,056 מלכות.

    <!-- cost: זמן \( O(N!) \) במקרה הגרוע, 2,056 הצבות ל-8 | זיכרון \( O(N) \) -->

    #### הרעיון { .sol-idea }

    מלכה אחת בכל שורה, ולכן מספיק לבחור עמודה לכל שורה. בשורה \( r \) לא כל עמודה מותרת : מלכה
    בשורה \( r' < r \) ובעמודה \( c' \) מאיימת בשורה \( r \) על העמודה \( c' \), ועל העמודות
    \( c' \pm (r - r') \) באלכסונים. שלוש מסכות זוכרות את כל האיומים האלה לשורה הבאה. הנה הלוח
    אחרי שלוש מלכות, והמסכות של שורה 3 :

    <!-- gen 0 -->

    <svg class="figure nq-board" viewBox="0 0 378 378" style="max-width:22rem" role="img" aria-label="סעיף א : לוח של 8 על 8, העמודה 0 מימין. מלכות בשורה 0 בעמודה 0, בשורה 1 בעמודה 4 ובשורה 2 בעמודה 7. בשורה 3 מאוימות העמודות 0, 2, 3, 4, 6 ו-7, ופנויות רק העמודות 1 ו-5"><rect class="nq-sq" x="309" y="24" width="44" height="44"/><rect class="nq-sq is-dark" x="265" y="24" width="44" height="44"/><rect class="nq-sq" x="221" y="24" width="44" height="44"/><rect class="nq-sq is-dark" x="177" y="24" width="44" height="44"/><rect class="nq-sq" x="133" y="24" width="44" height="44"/><rect class="nq-sq is-dark" x="89" y="24" width="44" height="44"/><rect class="nq-sq" x="45" y="24" width="44" height="44"/><rect class="nq-sq is-dark" x="1" y="24" width="44" height="44"/><rect class="nq-sq is-dark" x="309" y="68" width="44" height="44"/><rect class="nq-sq" x="265" y="68" width="44" height="44"/><rect class="nq-sq is-dark" x="221" y="68" width="44" height="44"/><rect class="nq-sq" x="177" y="68" width="44" height="44"/><rect class="nq-sq is-dark" x="133" y="68" width="44" height="44"/><rect class="nq-sq" x="89" y="68" width="44" height="44"/><rect class="nq-sq is-dark" x="45" y="68" width="44" height="44"/><rect class="nq-sq" x="1" y="68" width="44" height="44"/><rect class="nq-sq" x="309" y="112" width="44" height="44"/><rect class="nq-sq is-dark" x="265" y="112" width="44" height="44"/><rect class="nq-sq" x="221" y="112" width="44" height="44"/><rect class="nq-sq is-dark" x="177" y="112" width="44" height="44"/><rect class="nq-sq" x="133" y="112" width="44" height="44"/><rect class="nq-sq is-dark" x="89" y="112" width="44" height="44"/><rect class="nq-sq" x="45" y="112" width="44" height="44"/><rect class="nq-sq is-dark" x="1" y="112" width="44" height="44"/><rect class="nq-sq is-dark is-hit" x="309" y="156" width="44" height="44"/><rect class="nq-sq is-free" x="265" y="156" width="44" height="44"/><rect class="nq-sq is-dark is-hit" x="221" y="156" width="44" height="44"/><rect class="nq-sq is-hit" x="177" y="156" width="44" height="44"/><rect class="nq-sq is-dark is-hit" x="133" y="156" width="44" height="44"/><rect class="nq-sq is-free" x="89" y="156" width="44" height="44"/><rect class="nq-sq is-dark is-hit" x="45" y="156" width="44" height="44"/><rect class="nq-sq is-hit" x="1" y="156" width="44" height="44"/><rect class="nq-sq" x="309" y="200" width="44" height="44"/><rect class="nq-sq is-dark" x="265" y="200" width="44" height="44"/><rect class="nq-sq" x="221" y="200" width="44" height="44"/><rect class="nq-sq is-dark" x="177" y="200" width="44" height="44"/><rect class="nq-sq" x="133" y="200" width="44" height="44"/><rect class="nq-sq is-dark" x="89" y="200" width="44" height="44"/><rect class="nq-sq" x="45" y="200" width="44" height="44"/><rect class="nq-sq is-dark" x="1" y="200" width="44" height="44"/><rect class="nq-sq is-dark" x="309" y="244" width="44" height="44"/><rect class="nq-sq" x="265" y="244" width="44" height="44"/><rect class="nq-sq is-dark" x="221" y="244" width="44" height="44"/><rect class="nq-sq" x="177" y="244" width="44" height="44"/><rect class="nq-sq is-dark" x="133" y="244" width="44" height="44"/><rect class="nq-sq" x="89" y="244" width="44" height="44"/><rect class="nq-sq is-dark" x="45" y="244" width="44" height="44"/><rect class="nq-sq" x="1" y="244" width="44" height="44"/><rect class="nq-sq" x="309" y="288" width="44" height="44"/><rect class="nq-sq is-dark" x="265" y="288" width="44" height="44"/><rect class="nq-sq" x="221" y="288" width="44" height="44"/><rect class="nq-sq is-dark" x="177" y="288" width="44" height="44"/><rect class="nq-sq" x="133" y="288" width="44" height="44"/><rect class="nq-sq is-dark" x="89" y="288" width="44" height="44"/><rect class="nq-sq" x="45" y="288" width="44" height="44"/><rect class="nq-sq is-dark" x="1" y="288" width="44" height="44"/><rect class="nq-sq is-dark" x="309" y="332" width="44" height="44"/><rect class="nq-sq" x="265" y="332" width="44" height="44"/><rect class="nq-sq is-dark" x="221" y="332" width="44" height="44"/><rect class="nq-sq" x="177" y="332" width="44" height="44"/><rect class="nq-sq is-dark" x="133" y="332" width="44" height="44"/><rect class="nq-sq" x="89" y="332" width="44" height="44"/><rect class="nq-sq is-dark" x="45" y="332" width="44" height="44"/><rect class="nq-sq" x="1" y="332" width="44" height="44"/><rect class="nq-frame" x="1" y="24" width="352" height="352"/><text class="nq-lab" x="331.0" y="17" text-anchor="middle">0</text><text class="nq-lab" x="287.0" y="17" text-anchor="middle">1</text><text class="nq-lab" x="243.0" y="17" text-anchor="middle">2</text><text class="nq-lab" x="199.0" y="17" text-anchor="middle">3</text><text class="nq-lab" x="155.0" y="17" text-anchor="middle">4</text><text class="nq-lab" x="111.0" y="17" text-anchor="middle">5</text><text class="nq-lab" x="67.0" y="17" text-anchor="middle">6</text><text class="nq-lab" x="23.0" y="17" text-anchor="middle">7</text><text class="nq-lab" x="358" y="51.0">0</text><text class="nq-lab" x="358" y="95.0">1</text><text class="nq-lab" x="358" y="139.0">2</text><text class="nq-lab" x="358" y="183.0">3</text><text class="nq-lab" x="358" y="227.0">4</text><text class="nq-lab" x="358" y="271.0">5</text><text class="nq-lab" x="358" y="315.0">6</text><text class="nq-lab" x="358" y="359.0">7</text><g class="nq-q"><polygon points="317.8,53.9 315.2,36.3 324.4,46.0 331.0,31.9 337.6,46.0 346.8,36.3 344.2,53.9"/><rect x="317.8" y="54.8" width="26.4" height="4.8" rx="1.3"/></g><g class="nq-q"><polygon points="141.8,97.9 139.2,80.3 148.4,90.0 155.0,75.9 161.6,90.0 170.8,80.3 168.2,97.9"/><rect x="141.8" y="98.8" width="26.4" height="4.8" rx="1.3"/></g><g class="nq-q"><polygon points="9.8,141.9 7.2,124.3 16.4,134.0 23.0,119.9 29.6,134.0 38.8,124.3 36.2,141.9"/><rect x="9.8" y="142.8" width="26.4" height="4.8" rx="1.3"/></g></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <div class="gs-scroll" tabindex="0" role="region" aria-label="המסכות של שורה 3 בבינארי"><table class="gs-bits nq-masks" dir="ltr" aria-label="המסכות של שורה 3, ביט 7 משמאל וביט 0 מימין"><tbody><tr class="nq-bitno"><th>bit</th><th>7</th><th>6</th><th>5</th><th>4</th><th>3</th><th>2</th><th>1</th><th>0</th><td></td></tr><tr><th>cols</th><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-val">= 145</td></tr><tr><th>left</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">= 72</td></tr><tr><th>right</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-val">= 68</td></tr><tr><th>free</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one is-free">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one is-free">1</td><td class="gs-b">0</td><td class="gs-val">= 34</td></tr></tbody></table></div>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="nq-key-hit"></i>מאוימת בשורה הבאה</span><span><i class="nq-key-free"></i>פנויה : ביט 1 ב-free</span><span><i class="gs-key-one"></i>ביט 1 במסכה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שלוש מסכות :** `cols` הן העמודות התפוסות. `left` הן העמודות שמאוימות באלכסון שיורד
       שמאלה, והעמודה שלו גדלה ב-1 בכל שורה. `right` הן העמודות שמאוימות באלכסון שיורד ימינה,
       והעמודה שלו קטנה ב-1 בכל שורה.

    2. **העמודות הפנויות :** `free = full & ~(cols | left | right)`, כש-`full` הוא \( N \) אחדות.
       בשורה 3 של הדוגמה `free = 00100010`, כלומר העמודות 1 ו-5.

    3. **הביט הנמוך :** `bit = free & -free`. במשלים ל-2, `-free` הופך את כל הביטים שמעל הביט
       הנמוך, ולכן ה-AND משאיר רק אותו. אחר כך `free ^= bit` מוחק אותו מהרשימה.

    4. **שורה למטה :** מניחים את המלכה ויורדים שורה עם `cols | bit`, עם `(left | bit) << 1` ועם
       `(right | bit) >> 1`. ההזזה מעבירה כל איום אלכסוני לעמודה שלו בשורה הבאה. ביט שזז
       מעבר לעמודה \( N - 1 \) נחתך ב-`& full`, וביט שזז ימינה מעמודה 0 נופל לבד.

    5. **פתרון או חזרה :** כש-`cols == full`, הונחו \( N \) מלכות וזה פתרון. כש-`free` מתרוקן,
       הפונקציה חוזרת, והשורה הקודמת ממשיכה לביט הפנוי הבא שלה.

    </div>

    בתיבה בוחרים \( N \). כל צעד הוא מלכה אחת שהחיפוש מציב, ומתחת ללוח המסכות של השורה הבאה,
    כל ביט מתחת לעמודה שלו :

    <div class="explorer" data-kind="nqueens" data-n="8"></div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="count_queens" linenums="1" hl_lines="9 11 13"
        def count_queens(n: int, first: int = -1) -> int:
            """The solutions of n queens; first: the columns allowed in row 0 (all by default)."""
            full = (1 << n) - 1

            def place(cols: int, left: int, right: int, allowed: int) -> int:
                if cols == full:                              # (1)!
                    return 1
                count = 0
                free = allowed & ~(cols | left | right)       # (2)!
                while free:
                    bit = free & -free                        # (3)!
                    free ^= bit
                    count += place(cols | bit, ((left | bit) << 1) & full, (right | bit) >> 1, full)  # (4)!
                return count

            return place(0, 0, 0, full & first)
        ```

        1. ‏\( N \) אחדות ב-`cols` : הונחו \( N \) מלכות, מלכה בכל שורה.
        2. ‏`allowed` הוא `full`, חוץ מבשורה 0, שבה סעיף ב מגביל אותו לחצי מהעמודות.
        3. הביט הנמוך של `free` : העמודה הפנויה הקטנה.
        4. השורה הבאה : העמודה תפוסה, ושני האיומים האלכסוניים זזים עמודה, כל אחד לכיוון שלו.

    === "SystemVerilog"
        ```systemverilog title="count_queens" linenums="1" hl_lines="10 14 21 22 23"
        // The solutions of n queens (n <= 31); first: the columns allowed in row 0 (all by default).
        function automatic int count_queens(int n, int first = -1);
          int unsigned full = (32'd1 << n) - 1;
          int unsigned cols[32], left[32], right[32], free[32];   // (1)!
          int unsigned low;
          int row = 0, count = 0;
          cols[0] = 0; left[0] = 0; right[0] = 0;
          free[0] = full & first;
          while (row >= 0) begin
            if (free[row] == 0) begin                             // (2)!
              row--;
              continue;
            end
            low = free[row] & -free[row];                         // (3)!
            free[row] ^= low;
            if (row == n - 1) begin                               // (4)!
              count++;
              continue;
            end
            cols[row + 1] = cols[row] | low;
            left[row + 1] = ((left[row] | low) << 1) & full;
            right[row + 1] = (right[row] | low) >> 1;
            free[row + 1] = full & ~(cols[row + 1] | left[row + 1] | right[row + 1]);
            row++;
          end
          return count;
        endfunction
        ```

        1. בלי רקורסיה : מחסנית של מסכות, שורה לכל רמה, כמו שבונים את זה בחומרה.
        2. בשורה הזו אין עוד עמודה לנסות : חוזרים לשורה הקודמת. כשגם שורה 0 מתרוקנת, `row` הוא \( -1 \) והחיפוש נגמר.
        3. הביט הנמוך של `free`. ‏`bit` הוא מילה שמורה ב-SystemVerilog, ולכן השם `low`.
        4. מלכה בשורה האחרונה היא פתרון, ולא צריך לרדת עוד שורה.

    #### למה זה נכון { .sol-proof }

    **המסכות מדויקות.** מלכה בשורה \( r \) ובעמודה \( c \) מאיימת בשורה \( r + d \) על שלוש
    עמודות : \( c \), ‏\( c + d \) ו-\( c - d \). ב-`cols` הביט \( c \) נשאר תמיד. ב-`left` הביט
    \( c \) זז \( d \) פעמים שמאלה ומגיע ל-\( c + d \), וב-`right` הוא זז \( d \) פעמים ימינה ומגיע
    ל-\( c - d \). ביט שיוצא מהלוח מייצג משבצת שלא קיימת, ולכן מותר לחתוך אותו. כך `free` הוא
    בדיוק קבוצת העמודות שאף מלכה מלמעלה לא מאיימת עליהן.

    **כל פתרון נמצא פעם אחת.** פתרון הוא בחירה של עמודה לכל שורה. החיפוש עובר על כל הבחירות של
    שורה 0 שלא מאוימות, ולכל אחת על כל הבחירות של שורה 1 שלא מאוימות, וכן הלאה. כל פתרון הוא
    מסלול אחד בעץ הזה, ומסלול שנתקע לא נספר.

    #### סיבוכיות { .sol-cost }

    החיפוש חוסך המון לעומת ניסיון של כל האפשרויות, אבל הוא עדיין מעריכי :

    <!-- gen 3 -->

    | ‏\( N \) | פתרונות | מלכות שהחיפוש מציב | ‏\( N! \) | ‏\( N^N \) |
    |:-:|:-:|:-:|:-:|:-:|
    | 4 | 2 | 16 | 24 | 256 |
    | 5 | 10 | 53 | 120 | 3,125 |
    | 6 | 4 | 152 | 720 | 46,656 |
    | 7 | 40 | 551 | 5,040 | 823,543 |
    | 8 | 92 | 2,056 | 40,320 | 16,777,216 |
    | 9 | 352 | 8,393 | 362,880 | 387,420,489 |
    | 10 | 724 | 35,538 | 3,628,800 | 10,000,000,000 |
    | 11 | 2,680 | 166,925 | 39,916,800 | 285,311,670,611 |
    | 12 | 14,200 | 856,188 | 479,001,600 | 8,916,100,448,256 |

    <!-- /gen -->

    כל הצבה עולה כמה פעולות על מילה אחת, והזיכרון הוא \( O(N) \) : עומק הרקורסיה, או המחסנית של
    ה-SystemVerilog. המקרה הגרוע חסום ב-\( N! \), כי בשורה \( r \) נשארות לכל היותר \( N - r \)
    עמודות. בפועל מספר ההצבות גדל פי 4 עד 5 בכל פעם ש-\( N \) גדל ב-1.

---

### סעיף ב – כמה פתרונות שונים באמת { #symmetry }

פתרון שמסובבים אותו או משקפים אותו הוא שוב פתרון. אם סופרים פתרונות כאלה כפתרון אחד, כמה
פתרונות שונים יש ל-8 מלכות? ואיך משתמשים בסימטריה כדי לחסוך בספירה של סעיף א?

??? tip "רמז 1"
    ללוח ריבועי יש 8 סימטריות : ארבעה סיבובים, אחד מהם "בלי שינוי", וארבעה שיקופים. כל אחת
    מעבירה פתרון לפתרון.

??? tip "רמז 2"
    אם כל פתרון היה הולך ל-8 פתרונות שונים, 92 היה מתחלק ב-8. הוא לא מתחלק. מה זה אומר על אחד
    הפתרונות?

??? tip "רמז 3"
    שיקוף ימין-שמאל מעביר את המלכה של שורה 0 מהחצי הימני של השורה לחצי השמאלי. כמה פתרונות
    יש עם מלכה בחצי הימני של שורה 0?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        יש 12 פתרונות שונים : ל-11 מהם יש 8 תמונות שונות, ולאחד יש רק 4, כי חצי סיבוב לא משנה
        אותו. \( 11 \cdot 8 + 4 = 92 \). כדי לחסוך בספירה, מגבילים את המלכה של שורה 0 לחצי
        מהעמודות ומכפילים ב-2. כש-\( N \) אי-זוגי, את העמודה האמצעית סופרים בנפרד.

    <!-- cost: זמן כמחצית מסעיף א | זיכרון \( O(N) \) -->

    #### הרעיון { .sol-idea }

    מקבצים את הפתרונות למחלקות : שני פתרונות באותה מחלקה אם סימטריה אחת מעבירה את הראשון לשני.
    מכל מחלקה מציירים את התמונה הקטנה ביותר שלה, כרשימת עמודות לפי השורות :

    <!-- gen 4 -->

    <svg class="figure nq-classes" viewBox="0 0 766 284" style="max-width:40rem" role="img" aria-label="סעיף ב : 12 הפתרונות השונים של 8 מלכות, כל אחד בתמונה הקטנה ביותר שלו. לאחד עשר מהם יש 8 תמונות שונות, ולאחד, המסומן, רק 4 : הוא לא משתנה בחצי סיבוב"><rect class="nq-sq" x="100" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="86" y="2" width="14" height="14"/><rect class="nq-sq" x="72" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="58" y="2" width="14" height="14"/><rect class="nq-sq" x="44" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="30" y="2" width="14" height="14"/><rect class="nq-sq" x="16" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="2" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="100" y="16" width="14" height="14"/><rect class="nq-sq" x="86" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="72" y="16" width="14" height="14"/><rect class="nq-sq" x="58" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="44" y="16" width="14" height="14"/><rect class="nq-sq" x="30" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="16" y="16" width="14" height="14"/><rect class="nq-sq" x="2" y="16" width="14" height="14"/><rect class="nq-sq" x="100" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="86" y="30" width="14" height="14"/><rect class="nq-sq" x="72" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="58" y="30" width="14" height="14"/><rect class="nq-sq" x="44" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="30" y="30" width="14" height="14"/><rect class="nq-sq" x="16" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="2" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="100" y="44" width="14" height="14"/><rect class="nq-sq" x="86" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="72" y="44" width="14" height="14"/><rect class="nq-sq" x="58" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="44" y="44" width="14" height="14"/><rect class="nq-sq" x="30" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="16" y="44" width="14" height="14"/><rect class="nq-sq" x="2" y="44" width="14" height="14"/><rect class="nq-sq" x="100" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="86" y="58" width="14" height="14"/><rect class="nq-sq" x="72" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="58" y="58" width="14" height="14"/><rect class="nq-sq" x="44" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="30" y="58" width="14" height="14"/><rect class="nq-sq" x="16" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="2" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="100" y="72" width="14" height="14"/><rect class="nq-sq" x="86" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="72" y="72" width="14" height="14"/><rect class="nq-sq" x="58" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="44" y="72" width="14" height="14"/><rect class="nq-sq" x="30" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="16" y="72" width="14" height="14"/><rect class="nq-sq" x="2" y="72" width="14" height="14"/><rect class="nq-sq" x="100" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="86" y="86" width="14" height="14"/><rect class="nq-sq" x="72" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="58" y="86" width="14" height="14"/><rect class="nq-sq" x="44" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="30" y="86" width="14" height="14"/><rect class="nq-sq" x="16" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="2" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="100" y="100" width="14" height="14"/><rect class="nq-sq" x="86" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="72" y="100" width="14" height="14"/><rect class="nq-sq" x="58" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="44" y="100" width="14" height="14"/><rect class="nq-sq" x="30" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="16" y="100" width="14" height="14"/><rect class="nq-sq" x="2" y="100" width="14" height="14"/><rect class="nq-frame" x="2" y="2" width="112" height="112"/><circle class="nq-dot" cx="107.0" cy="9.0" r="4.5"/><circle class="nq-dot" cx="51.0" cy="23.0" r="4.5"/><circle class="nq-dot" cx="9.0" cy="37.0" r="4.5"/><circle class="nq-dot" cx="37.0" cy="51.0" r="4.5"/><circle class="nq-dot" cx="79.0" cy="65.0" r="4.5"/><circle class="nq-dot" cx="23.0" cy="79.0" r="4.5"/><circle class="nq-dot" cx="93.0" cy="93.0" r="4.5"/><circle class="nq-dot" cx="65.0" cy="107.0" r="4.5"/><text class="nq-lab" x="58.0" y="130" text-anchor="middle">×8</text><rect class="nq-sq" x="230" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="216" y="2" width="14" height="14"/><rect class="nq-sq" x="202" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="188" y="2" width="14" height="14"/><rect class="nq-sq" x="174" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="160" y="2" width="14" height="14"/><rect class="nq-sq" x="146" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="132" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="230" y="16" width="14" height="14"/><rect class="nq-sq" x="216" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="202" y="16" width="14" height="14"/><rect class="nq-sq" x="188" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="174" y="16" width="14" height="14"/><rect class="nq-sq" x="160" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="146" y="16" width="14" height="14"/><rect class="nq-sq" x="132" y="16" width="14" height="14"/><rect class="nq-sq" x="230" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="216" y="30" width="14" height="14"/><rect class="nq-sq" x="202" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="188" y="30" width="14" height="14"/><rect class="nq-sq" x="174" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="160" y="30" width="14" height="14"/><rect class="nq-sq" x="146" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="132" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="230" y="44" width="14" height="14"/><rect class="nq-sq" x="216" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="202" y="44" width="14" height="14"/><rect class="nq-sq" x="188" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="174" y="44" width="14" height="14"/><rect class="nq-sq" x="160" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="146" y="44" width="14" height="14"/><rect class="nq-sq" x="132" y="44" width="14" height="14"/><rect class="nq-sq" x="230" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="216" y="58" width="14" height="14"/><rect class="nq-sq" x="202" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="188" y="58" width="14" height="14"/><rect class="nq-sq" x="174" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="160" y="58" width="14" height="14"/><rect class="nq-sq" x="146" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="132" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="230" y="72" width="14" height="14"/><rect class="nq-sq" x="216" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="202" y="72" width="14" height="14"/><rect class="nq-sq" x="188" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="174" y="72" width="14" height="14"/><rect class="nq-sq" x="160" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="146" y="72" width="14" height="14"/><rect class="nq-sq" x="132" y="72" width="14" height="14"/><rect class="nq-sq" x="230" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="216" y="86" width="14" height="14"/><rect class="nq-sq" x="202" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="188" y="86" width="14" height="14"/><rect class="nq-sq" x="174" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="160" y="86" width="14" height="14"/><rect class="nq-sq" x="146" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="132" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="230" y="100" width="14" height="14"/><rect class="nq-sq" x="216" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="202" y="100" width="14" height="14"/><rect class="nq-sq" x="188" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="174" y="100" width="14" height="14"/><rect class="nq-sq" x="160" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="146" y="100" width="14" height="14"/><rect class="nq-sq" x="132" y="100" width="14" height="14"/><rect class="nq-frame" x="132" y="2" width="112" height="112"/><circle class="nq-dot" cx="237.0" cy="9.0" r="4.5"/><circle class="nq-dot" cx="167.0" cy="23.0" r="4.5"/><circle class="nq-dot" cx="139.0" cy="37.0" r="4.5"/><circle class="nq-dot" cx="209.0" cy="51.0" r="4.5"/><circle class="nq-dot" cx="153.0" cy="65.0" r="4.5"/><circle class="nq-dot" cx="195.0" cy="79.0" r="4.5"/><circle class="nq-dot" cx="223.0" cy="93.0" r="4.5"/><circle class="nq-dot" cx="181.0" cy="107.0" r="4.5"/><text class="nq-lab" x="188.0" y="130" text-anchor="middle">×8</text><rect class="nq-sq" x="360" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="346" y="2" width="14" height="14"/><rect class="nq-sq" x="332" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="318" y="2" width="14" height="14"/><rect class="nq-sq" x="304" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="290" y="2" width="14" height="14"/><rect class="nq-sq" x="276" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="262" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="360" y="16" width="14" height="14"/><rect class="nq-sq" x="346" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="332" y="16" width="14" height="14"/><rect class="nq-sq" x="318" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="304" y="16" width="14" height="14"/><rect class="nq-sq" x="290" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="276" y="16" width="14" height="14"/><rect class="nq-sq" x="262" y="16" width="14" height="14"/><rect class="nq-sq" x="360" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="346" y="30" width="14" height="14"/><rect class="nq-sq" x="332" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="318" y="30" width="14" height="14"/><rect class="nq-sq" x="304" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="290" y="30" width="14" height="14"/><rect class="nq-sq" x="276" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="262" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="360" y="44" width="14" height="14"/><rect class="nq-sq" x="346" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="332" y="44" width="14" height="14"/><rect class="nq-sq" x="318" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="304" y="44" width="14" height="14"/><rect class="nq-sq" x="290" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="276" y="44" width="14" height="14"/><rect class="nq-sq" x="262" y="44" width="14" height="14"/><rect class="nq-sq" x="360" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="346" y="58" width="14" height="14"/><rect class="nq-sq" x="332" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="318" y="58" width="14" height="14"/><rect class="nq-sq" x="304" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="290" y="58" width="14" height="14"/><rect class="nq-sq" x="276" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="262" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="360" y="72" width="14" height="14"/><rect class="nq-sq" x="346" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="332" y="72" width="14" height="14"/><rect class="nq-sq" x="318" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="304" y="72" width="14" height="14"/><rect class="nq-sq" x="290" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="276" y="72" width="14" height="14"/><rect class="nq-sq" x="262" y="72" width="14" height="14"/><rect class="nq-sq" x="360" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="346" y="86" width="14" height="14"/><rect class="nq-sq" x="332" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="318" y="86" width="14" height="14"/><rect class="nq-sq" x="304" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="290" y="86" width="14" height="14"/><rect class="nq-sq" x="276" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="262" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="360" y="100" width="14" height="14"/><rect class="nq-sq" x="346" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="332" y="100" width="14" height="14"/><rect class="nq-sq" x="318" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="304" y="100" width="14" height="14"/><rect class="nq-sq" x="290" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="276" y="100" width="14" height="14"/><rect class="nq-sq" x="262" y="100" width="14" height="14"/><rect class="nq-frame" x="262" y="2" width="112" height="112"/><circle class="nq-dot" cx="353.0" cy="9.0" r="4.5"/><circle class="nq-dot" cx="325.0" cy="23.0" r="4.5"/><circle class="nq-dot" cx="297.0" cy="37.0" r="4.5"/><circle class="nq-dot" cx="269.0" cy="51.0" r="4.5"/><circle class="nq-dot" cx="339.0" cy="65.0" r="4.5"/><circle class="nq-dot" cx="367.0" cy="79.0" r="4.5"/><circle class="nq-dot" cx="283.0" cy="93.0" r="4.5"/><circle class="nq-dot" cx="311.0" cy="107.0" r="4.5"/><text class="nq-lab" x="318.0" y="130" text-anchor="middle">×8</text><rect class="nq-sq" x="490" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="476" y="2" width="14" height="14"/><rect class="nq-sq" x="462" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="448" y="2" width="14" height="14"/><rect class="nq-sq" x="434" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="420" y="2" width="14" height="14"/><rect class="nq-sq" x="406" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="392" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="490" y="16" width="14" height="14"/><rect class="nq-sq" x="476" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="462" y="16" width="14" height="14"/><rect class="nq-sq" x="448" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="434" y="16" width="14" height="14"/><rect class="nq-sq" x="420" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="406" y="16" width="14" height="14"/><rect class="nq-sq" x="392" y="16" width="14" height="14"/><rect class="nq-sq" x="490" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="476" y="30" width="14" height="14"/><rect class="nq-sq" x="462" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="448" y="30" width="14" height="14"/><rect class="nq-sq" x="434" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="420" y="30" width="14" height="14"/><rect class="nq-sq" x="406" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="392" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="490" y="44" width="14" height="14"/><rect class="nq-sq" x="476" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="462" y="44" width="14" height="14"/><rect class="nq-sq" x="448" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="434" y="44" width="14" height="14"/><rect class="nq-sq" x="420" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="406" y="44" width="14" height="14"/><rect class="nq-sq" x="392" y="44" width="14" height="14"/><rect class="nq-sq" x="490" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="476" y="58" width="14" height="14"/><rect class="nq-sq" x="462" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="448" y="58" width="14" height="14"/><rect class="nq-sq" x="434" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="420" y="58" width="14" height="14"/><rect class="nq-sq" x="406" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="392" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="490" y="72" width="14" height="14"/><rect class="nq-sq" x="476" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="462" y="72" width="14" height="14"/><rect class="nq-sq" x="448" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="434" y="72" width="14" height="14"/><rect class="nq-sq" x="420" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="406" y="72" width="14" height="14"/><rect class="nq-sq" x="392" y="72" width="14" height="14"/><rect class="nq-sq" x="490" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="476" y="86" width="14" height="14"/><rect class="nq-sq" x="462" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="448" y="86" width="14" height="14"/><rect class="nq-sq" x="434" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="420" y="86" width="14" height="14"/><rect class="nq-sq" x="406" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="392" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="490" y="100" width="14" height="14"/><rect class="nq-sq" x="476" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="462" y="100" width="14" height="14"/><rect class="nq-sq" x="448" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="434" y="100" width="14" height="14"/><rect class="nq-sq" x="420" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="406" y="100" width="14" height="14"/><rect class="nq-sq" x="392" y="100" width="14" height="14"/><rect class="nq-frame" x="392" y="2" width="112" height="112"/><circle class="nq-dot" cx="483.0" cy="9.0" r="4.5"/><circle class="nq-dot" cx="441.0" cy="23.0" r="4.5"/><circle class="nq-dot" cx="413.0" cy="37.0" r="4.5"/><circle class="nq-dot" cx="497.0" cy="51.0" r="4.5"/><circle class="nq-dot" cx="469.0" cy="65.0" r="4.5"/><circle class="nq-dot" cx="399.0" cy="79.0" r="4.5"/><circle class="nq-dot" cx="427.0" cy="93.0" r="4.5"/><circle class="nq-dot" cx="455.0" cy="107.0" r="4.5"/><text class="nq-lab" x="448.0" y="130" text-anchor="middle">×8</text><rect class="nq-sq" x="620" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="606" y="2" width="14" height="14"/><rect class="nq-sq" x="592" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="578" y="2" width="14" height="14"/><rect class="nq-sq" x="564" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="550" y="2" width="14" height="14"/><rect class="nq-sq" x="536" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="522" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="620" y="16" width="14" height="14"/><rect class="nq-sq" x="606" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="592" y="16" width="14" height="14"/><rect class="nq-sq" x="578" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="564" y="16" width="14" height="14"/><rect class="nq-sq" x="550" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="536" y="16" width="14" height="14"/><rect class="nq-sq" x="522" y="16" width="14" height="14"/><rect class="nq-sq" x="620" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="606" y="30" width="14" height="14"/><rect class="nq-sq" x="592" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="578" y="30" width="14" height="14"/><rect class="nq-sq" x="564" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="550" y="30" width="14" height="14"/><rect class="nq-sq" x="536" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="522" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="620" y="44" width="14" height="14"/><rect class="nq-sq" x="606" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="592" y="44" width="14" height="14"/><rect class="nq-sq" x="578" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="564" y="44" width="14" height="14"/><rect class="nq-sq" x="550" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="536" y="44" width="14" height="14"/><rect class="nq-sq" x="522" y="44" width="14" height="14"/><rect class="nq-sq" x="620" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="606" y="58" width="14" height="14"/><rect class="nq-sq" x="592" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="578" y="58" width="14" height="14"/><rect class="nq-sq" x="564" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="550" y="58" width="14" height="14"/><rect class="nq-sq" x="536" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="522" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="620" y="72" width="14" height="14"/><rect class="nq-sq" x="606" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="592" y="72" width="14" height="14"/><rect class="nq-sq" x="578" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="564" y="72" width="14" height="14"/><rect class="nq-sq" x="550" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="536" y="72" width="14" height="14"/><rect class="nq-sq" x="522" y="72" width="14" height="14"/><rect class="nq-sq" x="620" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="606" y="86" width="14" height="14"/><rect class="nq-sq" x="592" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="578" y="86" width="14" height="14"/><rect class="nq-sq" x="564" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="550" y="86" width="14" height="14"/><rect class="nq-sq" x="536" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="522" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="620" y="100" width="14" height="14"/><rect class="nq-sq" x="606" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="592" y="100" width="14" height="14"/><rect class="nq-sq" x="578" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="564" y="100" width="14" height="14"/><rect class="nq-sq" x="550" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="536" y="100" width="14" height="14"/><rect class="nq-sq" x="522" y="100" width="14" height="14"/><rect class="nq-frame" x="522" y="2" width="112" height="112"/><circle class="nq-dot" cx="613.0" cy="9.0" r="4.5"/><circle class="nq-dot" cx="571.0" cy="23.0" r="4.5"/><circle class="nq-dot" cx="543.0" cy="37.0" r="4.5"/><circle class="nq-dot" cx="585.0" cy="51.0" r="4.5"/><circle class="nq-dot" cx="627.0" cy="65.0" r="4.5"/><circle class="nq-dot" cx="529.0" cy="79.0" r="4.5"/><circle class="nq-dot" cx="557.0" cy="93.0" r="4.5"/><circle class="nq-dot" cx="599.0" cy="107.0" r="4.5"/><text class="nq-lab" x="578.0" y="130" text-anchor="middle">×8</text><rect class="nq-sq" x="750" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="736" y="2" width="14" height="14"/><rect class="nq-sq" x="722" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="708" y="2" width="14" height="14"/><rect class="nq-sq" x="694" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="680" y="2" width="14" height="14"/><rect class="nq-sq" x="666" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="652" y="2" width="14" height="14"/><rect class="nq-sq is-dark" x="750" y="16" width="14" height="14"/><rect class="nq-sq" x="736" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="722" y="16" width="14" height="14"/><rect class="nq-sq" x="708" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="694" y="16" width="14" height="14"/><rect class="nq-sq" x="680" y="16" width="14" height="14"/><rect class="nq-sq is-dark" x="666" y="16" width="14" height="14"/><rect class="nq-sq" x="652" y="16" width="14" height="14"/><rect class="nq-sq" x="750" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="736" y="30" width="14" height="14"/><rect class="nq-sq" x="722" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="708" y="30" width="14" height="14"/><rect class="nq-sq" x="694" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="680" y="30" width="14" height="14"/><rect class="nq-sq" x="666" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="652" y="30" width="14" height="14"/><rect class="nq-sq is-dark" x="750" y="44" width="14" height="14"/><rect class="nq-sq" x="736" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="722" y="44" width="14" height="14"/><rect class="nq-sq" x="708" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="694" y="44" width="14" height="14"/><rect class="nq-sq" x="680" y="44" width="14" height="14"/><rect class="nq-sq is-dark" x="666" y="44" width="14" height="14"/><rect class="nq-sq" x="652" y="44" width="14" height="14"/><rect class="nq-sq" x="750" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="736" y="58" width="14" height="14"/><rect class="nq-sq" x="722" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="708" y="58" width="14" height="14"/><rect class="nq-sq" x="694" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="680" y="58" width="14" height="14"/><rect class="nq-sq" x="666" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="652" y="58" width="14" height="14"/><rect class="nq-sq is-dark" x="750" y="72" width="14" height="14"/><rect class="nq-sq" x="736" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="722" y="72" width="14" height="14"/><rect class="nq-sq" x="708" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="694" y="72" width="14" height="14"/><rect class="nq-sq" x="680" y="72" width="14" height="14"/><rect class="nq-sq is-dark" x="666" y="72" width="14" height="14"/><rect class="nq-sq" x="652" y="72" width="14" height="14"/><rect class="nq-sq" x="750" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="736" y="86" width="14" height="14"/><rect class="nq-sq" x="722" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="708" y="86" width="14" height="14"/><rect class="nq-sq" x="694" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="680" y="86" width="14" height="14"/><rect class="nq-sq" x="666" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="652" y="86" width="14" height="14"/><rect class="nq-sq is-dark" x="750" y="100" width="14" height="14"/><rect class="nq-sq" x="736" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="722" y="100" width="14" height="14"/><rect class="nq-sq" x="708" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="694" y="100" width="14" height="14"/><rect class="nq-sq" x="680" y="100" width="14" height="14"/><rect class="nq-sq is-dark" x="666" y="100" width="14" height="14"/><rect class="nq-sq" x="652" y="100" width="14" height="14"/><rect class="nq-frame" x="652" y="2" width="112" height="112"/><circle class="nq-dot" cx="743.0" cy="9.0" r="4.5"/><circle class="nq-dot" cx="687.0" cy="23.0" r="4.5"/><circle class="nq-dot" cx="757.0" cy="37.0" r="4.5"/><circle class="nq-dot" cx="673.0" cy="51.0" r="4.5"/><circle class="nq-dot" cx="715.0" cy="65.0" r="4.5"/><circle class="nq-dot" cx="659.0" cy="79.0" r="4.5"/><circle class="nq-dot" cx="729.0" cy="93.0" r="4.5"/><circle class="nq-dot" cx="701.0" cy="107.0" r="4.5"/><text class="nq-lab" x="708.0" y="130" text-anchor="middle">×8</text><rect class="nq-sq" x="100" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="86" y="148" width="14" height="14"/><rect class="nq-sq" x="72" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="58" y="148" width="14" height="14"/><rect class="nq-sq" x="44" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="30" y="148" width="14" height="14"/><rect class="nq-sq" x="16" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="2" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="100" y="162" width="14" height="14"/><rect class="nq-sq" x="86" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="72" y="162" width="14" height="14"/><rect class="nq-sq" x="58" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="44" y="162" width="14" height="14"/><rect class="nq-sq" x="30" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="16" y="162" width="14" height="14"/><rect class="nq-sq" x="2" y="162" width="14" height="14"/><rect class="nq-sq" x="100" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="86" y="176" width="14" height="14"/><rect class="nq-sq" x="72" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="58" y="176" width="14" height="14"/><rect class="nq-sq" x="44" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="30" y="176" width="14" height="14"/><rect class="nq-sq" x="16" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="2" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="100" y="190" width="14" height="14"/><rect class="nq-sq" x="86" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="72" y="190" width="14" height="14"/><rect class="nq-sq" x="58" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="44" y="190" width="14" height="14"/><rect class="nq-sq" x="30" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="16" y="190" width="14" height="14"/><rect class="nq-sq" x="2" y="190" width="14" height="14"/><rect class="nq-sq" x="100" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="86" y="204" width="14" height="14"/><rect class="nq-sq" x="72" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="58" y="204" width="14" height="14"/><rect class="nq-sq" x="44" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="30" y="204" width="14" height="14"/><rect class="nq-sq" x="16" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="2" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="100" y="218" width="14" height="14"/><rect class="nq-sq" x="86" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="72" y="218" width="14" height="14"/><rect class="nq-sq" x="58" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="44" y="218" width="14" height="14"/><rect class="nq-sq" x="30" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="16" y="218" width="14" height="14"/><rect class="nq-sq" x="2" y="218" width="14" height="14"/><rect class="nq-sq" x="100" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="86" y="232" width="14" height="14"/><rect class="nq-sq" x="72" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="58" y="232" width="14" height="14"/><rect class="nq-sq" x="44" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="30" y="232" width="14" height="14"/><rect class="nq-sq" x="16" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="2" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="100" y="246" width="14" height="14"/><rect class="nq-sq" x="86" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="72" y="246" width="14" height="14"/><rect class="nq-sq" x="58" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="44" y="246" width="14" height="14"/><rect class="nq-sq" x="30" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="16" y="246" width="14" height="14"/><rect class="nq-sq" x="2" y="246" width="14" height="14"/><rect class="nq-frame" x="2" y="148" width="112" height="112"/><circle class="nq-dot" cx="93.0" cy="155.0" r="4.5"/><circle class="nq-dot" cx="37.0" cy="169.0" r="4.5"/><circle class="nq-dot" cx="9.0" cy="183.0" r="4.5"/><circle class="nq-dot" cx="79.0" cy="197.0" r="4.5"/><circle class="nq-dot" cx="107.0" cy="211.0" r="4.5"/><circle class="nq-dot" cx="65.0" cy="225.0" r="4.5"/><circle class="nq-dot" cx="23.0" cy="239.0" r="4.5"/><circle class="nq-dot" cx="51.0" cy="253.0" r="4.5"/><text class="nq-lab" x="58.0" y="276" text-anchor="middle">×8</text><rect class="nq-sq" x="230" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="216" y="148" width="14" height="14"/><rect class="nq-sq" x="202" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="188" y="148" width="14" height="14"/><rect class="nq-sq" x="174" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="160" y="148" width="14" height="14"/><rect class="nq-sq" x="146" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="132" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="230" y="162" width="14" height="14"/><rect class="nq-sq" x="216" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="202" y="162" width="14" height="14"/><rect class="nq-sq" x="188" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="174" y="162" width="14" height="14"/><rect class="nq-sq" x="160" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="146" y="162" width="14" height="14"/><rect class="nq-sq" x="132" y="162" width="14" height="14"/><rect class="nq-sq" x="230" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="216" y="176" width="14" height="14"/><rect class="nq-sq" x="202" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="188" y="176" width="14" height="14"/><rect class="nq-sq" x="174" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="160" y="176" width="14" height="14"/><rect class="nq-sq" x="146" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="132" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="230" y="190" width="14" height="14"/><rect class="nq-sq" x="216" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="202" y="190" width="14" height="14"/><rect class="nq-sq" x="188" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="174" y="190" width="14" height="14"/><rect class="nq-sq" x="160" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="146" y="190" width="14" height="14"/><rect class="nq-sq" x="132" y="190" width="14" height="14"/><rect class="nq-sq" x="230" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="216" y="204" width="14" height="14"/><rect class="nq-sq" x="202" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="188" y="204" width="14" height="14"/><rect class="nq-sq" x="174" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="160" y="204" width="14" height="14"/><rect class="nq-sq" x="146" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="132" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="230" y="218" width="14" height="14"/><rect class="nq-sq" x="216" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="202" y="218" width="14" height="14"/><rect class="nq-sq" x="188" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="174" y="218" width="14" height="14"/><rect class="nq-sq" x="160" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="146" y="218" width="14" height="14"/><rect class="nq-sq" x="132" y="218" width="14" height="14"/><rect class="nq-sq" x="230" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="216" y="232" width="14" height="14"/><rect class="nq-sq" x="202" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="188" y="232" width="14" height="14"/><rect class="nq-sq" x="174" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="160" y="232" width="14" height="14"/><rect class="nq-sq" x="146" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="132" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="230" y="246" width="14" height="14"/><rect class="nq-sq" x="216" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="202" y="246" width="14" height="14"/><rect class="nq-sq" x="188" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="174" y="246" width="14" height="14"/><rect class="nq-sq" x="160" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="146" y="246" width="14" height="14"/><rect class="nq-sq" x="132" y="246" width="14" height="14"/><rect class="nq-frame" x="132" y="148" width="112" height="112"/><circle class="nq-dot" cx="223.0" cy="155.0" r="4.5"/><circle class="nq-dot" cx="153.0" cy="169.0" r="4.5"/><circle class="nq-dot" cx="209.0" cy="183.0" r="4.5"/><circle class="nq-dot" cx="167.0" cy="197.0" r="4.5"/><circle class="nq-dot" cx="139.0" cy="211.0" r="4.5"/><circle class="nq-dot" cx="181.0" cy="225.0" r="4.5"/><circle class="nq-dot" cx="237.0" cy="239.0" r="4.5"/><circle class="nq-dot" cx="195.0" cy="253.0" r="4.5"/><text class="nq-lab" x="188.0" y="276" text-anchor="middle">×8</text><rect class="nq-sq" x="360" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="346" y="148" width="14" height="14"/><rect class="nq-sq" x="332" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="318" y="148" width="14" height="14"/><rect class="nq-sq" x="304" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="290" y="148" width="14" height="14"/><rect class="nq-sq" x="276" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="262" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="360" y="162" width="14" height="14"/><rect class="nq-sq" x="346" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="332" y="162" width="14" height="14"/><rect class="nq-sq" x="318" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="304" y="162" width="14" height="14"/><rect class="nq-sq" x="290" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="276" y="162" width="14" height="14"/><rect class="nq-sq" x="262" y="162" width="14" height="14"/><rect class="nq-sq" x="360" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="346" y="176" width="14" height="14"/><rect class="nq-sq" x="332" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="318" y="176" width="14" height="14"/><rect class="nq-sq" x="304" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="290" y="176" width="14" height="14"/><rect class="nq-sq" x="276" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="262" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="360" y="190" width="14" height="14"/><rect class="nq-sq" x="346" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="332" y="190" width="14" height="14"/><rect class="nq-sq" x="318" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="304" y="190" width="14" height="14"/><rect class="nq-sq" x="290" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="276" y="190" width="14" height="14"/><rect class="nq-sq" x="262" y="190" width="14" height="14"/><rect class="nq-sq" x="360" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="346" y="204" width="14" height="14"/><rect class="nq-sq" x="332" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="318" y="204" width="14" height="14"/><rect class="nq-sq" x="304" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="290" y="204" width="14" height="14"/><rect class="nq-sq" x="276" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="262" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="360" y="218" width="14" height="14"/><rect class="nq-sq" x="346" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="332" y="218" width="14" height="14"/><rect class="nq-sq" x="318" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="304" y="218" width="14" height="14"/><rect class="nq-sq" x="290" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="276" y="218" width="14" height="14"/><rect class="nq-sq" x="262" y="218" width="14" height="14"/><rect class="nq-sq" x="360" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="346" y="232" width="14" height="14"/><rect class="nq-sq" x="332" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="318" y="232" width="14" height="14"/><rect class="nq-sq" x="304" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="290" y="232" width="14" height="14"/><rect class="nq-sq" x="276" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="262" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="360" y="246" width="14" height="14"/><rect class="nq-sq" x="346" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="332" y="246" width="14" height="14"/><rect class="nq-sq" x="318" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="304" y="246" width="14" height="14"/><rect class="nq-sq" x="290" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="276" y="246" width="14" height="14"/><rect class="nq-sq" x="262" y="246" width="14" height="14"/><rect class="nq-frame" x="262" y="148" width="112" height="112"/><circle class="nq-dot" cx="353.0" cy="155.0" r="4.5"/><circle class="nq-dot" cx="283.0" cy="169.0" r="4.5"/><circle class="nq-dot" cx="311.0" cy="183.0" r="4.5"/><circle class="nq-dot" cx="269.0" cy="197.0" r="4.5"/><circle class="nq-dot" cx="367.0" cy="211.0" r="4.5"/><circle class="nq-dot" cx="325.0" cy="225.0" r="4.5"/><circle class="nq-dot" cx="297.0" cy="239.0" r="4.5"/><circle class="nq-dot" cx="339.0" cy="253.0" r="4.5"/><text class="nq-lab" x="318.0" y="276" text-anchor="middle">×8</text><rect class="nq-sq" x="490" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="476" y="148" width="14" height="14"/><rect class="nq-sq" x="462" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="448" y="148" width="14" height="14"/><rect class="nq-sq" x="434" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="420" y="148" width="14" height="14"/><rect class="nq-sq" x="406" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="392" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="490" y="162" width="14" height="14"/><rect class="nq-sq" x="476" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="462" y="162" width="14" height="14"/><rect class="nq-sq" x="448" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="434" y="162" width="14" height="14"/><rect class="nq-sq" x="420" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="406" y="162" width="14" height="14"/><rect class="nq-sq" x="392" y="162" width="14" height="14"/><rect class="nq-sq" x="490" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="476" y="176" width="14" height="14"/><rect class="nq-sq" x="462" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="448" y="176" width="14" height="14"/><rect class="nq-sq" x="434" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="420" y="176" width="14" height="14"/><rect class="nq-sq" x="406" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="392" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="490" y="190" width="14" height="14"/><rect class="nq-sq" x="476" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="462" y="190" width="14" height="14"/><rect class="nq-sq" x="448" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="434" y="190" width="14" height="14"/><rect class="nq-sq" x="420" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="406" y="190" width="14" height="14"/><rect class="nq-sq" x="392" y="190" width="14" height="14"/><rect class="nq-sq" x="490" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="476" y="204" width="14" height="14"/><rect class="nq-sq" x="462" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="448" y="204" width="14" height="14"/><rect class="nq-sq" x="434" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="420" y="204" width="14" height="14"/><rect class="nq-sq" x="406" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="392" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="490" y="218" width="14" height="14"/><rect class="nq-sq" x="476" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="462" y="218" width="14" height="14"/><rect class="nq-sq" x="448" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="434" y="218" width="14" height="14"/><rect class="nq-sq" x="420" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="406" y="218" width="14" height="14"/><rect class="nq-sq" x="392" y="218" width="14" height="14"/><rect class="nq-sq" x="490" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="476" y="232" width="14" height="14"/><rect class="nq-sq" x="462" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="448" y="232" width="14" height="14"/><rect class="nq-sq" x="434" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="420" y="232" width="14" height="14"/><rect class="nq-sq" x="406" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="392" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="490" y="246" width="14" height="14"/><rect class="nq-sq" x="476" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="462" y="246" width="14" height="14"/><rect class="nq-sq" x="448" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="434" y="246" width="14" height="14"/><rect class="nq-sq" x="420" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="406" y="246" width="14" height="14"/><rect class="nq-sq" x="392" y="246" width="14" height="14"/><rect class="nq-frame is-sym" x="392" y="148" width="112" height="112"/><circle class="nq-dot" cx="469.0" cy="155.0" r="4.5"/><circle class="nq-dot" cx="441.0" cy="169.0" r="4.5"/><circle class="nq-dot" cx="483.0" cy="183.0" r="4.5"/><circle class="nq-dot" cx="399.0" cy="197.0" r="4.5"/><circle class="nq-dot" cx="497.0" cy="211.0" r="4.5"/><circle class="nq-dot" cx="413.0" cy="225.0" r="4.5"/><circle class="nq-dot" cx="455.0" cy="239.0" r="4.5"/><circle class="nq-dot" cx="427.0" cy="253.0" r="4.5"/><text class="nq-lab" x="448.0" y="276" text-anchor="middle">×4</text><rect class="nq-sq" x="620" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="606" y="148" width="14" height="14"/><rect class="nq-sq" x="592" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="578" y="148" width="14" height="14"/><rect class="nq-sq" x="564" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="550" y="148" width="14" height="14"/><rect class="nq-sq" x="536" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="522" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="620" y="162" width="14" height="14"/><rect class="nq-sq" x="606" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="592" y="162" width="14" height="14"/><rect class="nq-sq" x="578" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="564" y="162" width="14" height="14"/><rect class="nq-sq" x="550" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="536" y="162" width="14" height="14"/><rect class="nq-sq" x="522" y="162" width="14" height="14"/><rect class="nq-sq" x="620" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="606" y="176" width="14" height="14"/><rect class="nq-sq" x="592" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="578" y="176" width="14" height="14"/><rect class="nq-sq" x="564" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="550" y="176" width="14" height="14"/><rect class="nq-sq" x="536" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="522" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="620" y="190" width="14" height="14"/><rect class="nq-sq" x="606" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="592" y="190" width="14" height="14"/><rect class="nq-sq" x="578" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="564" y="190" width="14" height="14"/><rect class="nq-sq" x="550" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="536" y="190" width="14" height="14"/><rect class="nq-sq" x="522" y="190" width="14" height="14"/><rect class="nq-sq" x="620" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="606" y="204" width="14" height="14"/><rect class="nq-sq" x="592" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="578" y="204" width="14" height="14"/><rect class="nq-sq" x="564" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="550" y="204" width="14" height="14"/><rect class="nq-sq" x="536" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="522" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="620" y="218" width="14" height="14"/><rect class="nq-sq" x="606" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="592" y="218" width="14" height="14"/><rect class="nq-sq" x="578" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="564" y="218" width="14" height="14"/><rect class="nq-sq" x="550" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="536" y="218" width="14" height="14"/><rect class="nq-sq" x="522" y="218" width="14" height="14"/><rect class="nq-sq" x="620" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="606" y="232" width="14" height="14"/><rect class="nq-sq" x="592" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="578" y="232" width="14" height="14"/><rect class="nq-sq" x="564" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="550" y="232" width="14" height="14"/><rect class="nq-sq" x="536" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="522" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="620" y="246" width="14" height="14"/><rect class="nq-sq" x="606" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="592" y="246" width="14" height="14"/><rect class="nq-sq" x="578" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="564" y="246" width="14" height="14"/><rect class="nq-sq" x="550" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="536" y="246" width="14" height="14"/><rect class="nq-sq" x="522" y="246" width="14" height="14"/><rect class="nq-frame" x="522" y="148" width="112" height="112"/><circle class="nq-dot" cx="599.0" cy="155.0" r="4.5"/><circle class="nq-dot" cx="571.0" cy="169.0" r="4.5"/><circle class="nq-dot" cx="529.0" cy="183.0" r="4.5"/><circle class="nq-dot" cx="585.0" cy="197.0" r="4.5"/><circle class="nq-dot" cx="627.0" cy="211.0" r="4.5"/><circle class="nq-dot" cx="543.0" cy="225.0" r="4.5"/><circle class="nq-dot" cx="613.0" cy="239.0" r="4.5"/><circle class="nq-dot" cx="557.0" cy="253.0" r="4.5"/><text class="nq-lab" x="578.0" y="276" text-anchor="middle">×8</text><rect class="nq-sq" x="750" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="736" y="148" width="14" height="14"/><rect class="nq-sq" x="722" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="708" y="148" width="14" height="14"/><rect class="nq-sq" x="694" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="680" y="148" width="14" height="14"/><rect class="nq-sq" x="666" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="652" y="148" width="14" height="14"/><rect class="nq-sq is-dark" x="750" y="162" width="14" height="14"/><rect class="nq-sq" x="736" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="722" y="162" width="14" height="14"/><rect class="nq-sq" x="708" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="694" y="162" width="14" height="14"/><rect class="nq-sq" x="680" y="162" width="14" height="14"/><rect class="nq-sq is-dark" x="666" y="162" width="14" height="14"/><rect class="nq-sq" x="652" y="162" width="14" height="14"/><rect class="nq-sq" x="750" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="736" y="176" width="14" height="14"/><rect class="nq-sq" x="722" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="708" y="176" width="14" height="14"/><rect class="nq-sq" x="694" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="680" y="176" width="14" height="14"/><rect class="nq-sq" x="666" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="652" y="176" width="14" height="14"/><rect class="nq-sq is-dark" x="750" y="190" width="14" height="14"/><rect class="nq-sq" x="736" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="722" y="190" width="14" height="14"/><rect class="nq-sq" x="708" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="694" y="190" width="14" height="14"/><rect class="nq-sq" x="680" y="190" width="14" height="14"/><rect class="nq-sq is-dark" x="666" y="190" width="14" height="14"/><rect class="nq-sq" x="652" y="190" width="14" height="14"/><rect class="nq-sq" x="750" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="736" y="204" width="14" height="14"/><rect class="nq-sq" x="722" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="708" y="204" width="14" height="14"/><rect class="nq-sq" x="694" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="680" y="204" width="14" height="14"/><rect class="nq-sq" x="666" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="652" y="204" width="14" height="14"/><rect class="nq-sq is-dark" x="750" y="218" width="14" height="14"/><rect class="nq-sq" x="736" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="722" y="218" width="14" height="14"/><rect class="nq-sq" x="708" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="694" y="218" width="14" height="14"/><rect class="nq-sq" x="680" y="218" width="14" height="14"/><rect class="nq-sq is-dark" x="666" y="218" width="14" height="14"/><rect class="nq-sq" x="652" y="218" width="14" height="14"/><rect class="nq-sq" x="750" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="736" y="232" width="14" height="14"/><rect class="nq-sq" x="722" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="708" y="232" width="14" height="14"/><rect class="nq-sq" x="694" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="680" y="232" width="14" height="14"/><rect class="nq-sq" x="666" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="652" y="232" width="14" height="14"/><rect class="nq-sq is-dark" x="750" y="246" width="14" height="14"/><rect class="nq-sq" x="736" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="722" y="246" width="14" height="14"/><rect class="nq-sq" x="708" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="694" y="246" width="14" height="14"/><rect class="nq-sq" x="680" y="246" width="14" height="14"/><rect class="nq-sq is-dark" x="666" y="246" width="14" height="14"/><rect class="nq-sq" x="652" y="246" width="14" height="14"/><rect class="nq-frame" x="652" y="148" width="112" height="112"/><circle class="nq-dot" cx="729.0" cy="155.0" r="4.5"/><circle class="nq-dot" cx="687.0" cy="169.0" r="4.5"/><circle class="nq-dot" cx="743.0" cy="183.0" r="4.5"/><circle class="nq-dot" cx="701.0" cy="197.0" r="4.5"/><circle class="nq-dot" cx="659.0" cy="211.0" r="4.5"/><circle class="nq-dot" cx="757.0" cy="225.0" r="4.5"/><circle class="nq-dot" cx="673.0" cy="239.0" r="4.5"/><circle class="nq-dot" cx="715.0" cy="253.0" r="4.5"/><text class="nq-lab" x="708.0" y="276" text-anchor="middle">×8</text></svg>

    <!-- /gen -->

    <!-- gen 5 -->

    <span class="viz-legend"><span><i class="nq-key-dot"></i>מלכה</span><span><i class="nq-key-sym"></i>הפתרון שחצי סיבוב לא משנה</span><span>‏×8 או ×4 : כמה פתרונות שונים יש במחלקה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שתי פעולות :** רבע סיבוב מעביר מלכה מ-\( (r, c) \) ל-\( (c, N - 1 - r) \), ושיקוף ימין-שמאל
       מעביר אותה ל-\( (r, N - 1 - c) \). ארבעה סיבובים, וכל אחד עם שיקוף או בלעדיו, הם כל 8
       הסימטריות.

    2. **נציג אחד :** הנציג של מחלקה הוא התמונה הקטנה ביותר שלה, כרשימת עמודות. מספר הפתרונות
       השונים הוא מספר הנציגים השונים.

    3. **למה 4 ולא 8 :** אם חצי סיבוב לא משנה פתרון, אז שתי סימטריות שונות בחצי סיבוב נותנות
       אותה תמונה, ויש רק \( 8 / 2 = 4 \) תמונות שונות.

    4. **ספירה בלי לראות את המחלקות (Burnside) :** סופרים לכל סימטריה כמה פתרונות היא לא משנה,
       ומחלקים את הסכום ב-8 :

        <!-- gen 6 -->

        | הסימטריה | פתרונות שהיא לא משנה |
        |:-:|:-:|
        | בלי שינוי | 92 |
        | רבע סיבוב | 0 |
        | חצי סיבוב | 4 |
        | שלושה רבעי סיבוב | 0 |
        | שיקוף ימין-שמאל | 0 |
        | שיקוף באלכסון | 0 |
        | שיקוף למעלה-למטה | 0 |
        | שיקוף באלכסון השני | 0 |
        | **הסכום** | **96** |

        <!-- /gen -->

        ‏\( 96 / 8 = 12 \). כל מחלקה של 8 תורמת לסכום 8, דרך "בלי שינוי" בלבד. המחלקה של 4
        תורמת 4 דרך "בלי שינוי" ועוד 4 דרך חצי סיבוב, כלומר 8 גם היא.

    5. **לחסוך בספירה :** שיקוף ימין-שמאל מעביר פתרון שבו המלכה של שורה 0 בעמודה \( c < N/2 \)
       לפתרון שבו היא בעמודה \( N - 1 - c \ge N/2 \), ולהפך. לכן סופרים רק עם שורה 0 בחצי
       הימני של הלוח ומכפילים ב-2. ‏8 מלכות : \( 2 \cdot 46 = 92 \). כש-\( N \) אי-זוגי, השיקוף
       משאיר את העמודה האמצעית במקומה, ולכן אותה סופרים בנפרד, בלי להכפיל.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="solutions, images, distinct, count_half" linenums="1" hl_lines="23 32 37 42 44"
        def solutions(n: int):
            """Every solution, p[r] = the column of the queen in row r, in the order of the search."""
            full = (1 << n) - 1

            def place(row: int, cols: int, left: int, right: int, p: list[int]):
                if row == n:
                    yield tuple(p)
                    return
                free = full & ~(cols | left | right)
                while free:
                    bit = free & -free
                    free ^= bit
                    yield from place(row + 1, cols | bit, ((left | bit) << 1) & full, (right | bit) >> 1,
                                     p + [bit.bit_length() - 1])

            yield from place(0, 0, 0, 0, [])


        def rotate(p: tuple[int, ...]) -> tuple[int, ...]:
            """A quarter turn: the queen (r, c) goes to (c, n - 1 - r)."""
            q = [0] * len(p)
            for r, c in enumerate(p):
                q[c] = len(p) - 1 - r
            return tuple(q)


        def images(p: tuple[int, ...]) -> list[tuple[int, ...]]:
            """The 8 images of p: four turns, and each one mirrored left to right."""
            turns = [p]
            for _ in range(3):
                turns.append(rotate(turns[-1]))
            return turns + [tuple(len(p) - 1 - c for c in q) for q in turns]   # (1)!


        def distinct(n: int) -> int:
            """The solutions up to rotation and reflection: one smallest image per class."""
            return len({min(images(p)) for p in solutions(n)})                 # (2)!


        def count_half(n: int) -> int:
            """count_queens with row 0 limited to the half of the columns (and the middle one)."""
            count = 2 * count_queens(n, (1 << (n // 2)) - 1)                    # (3)!
            if n % 2:
                count += count_queens(n, 1 << (n // 2))                         # (4)!
            return count
        ```

        1. השיקוף \( (r, c) \to (r, N - 1 - c) \) של כל אחד מארבעת הסיבובים.
        2. התמונה הקטנה ביותר היא הנציג של המחלקה, ושני פתרונות באותה מחלקה נותנים אותו נציג.
        3. העמודות \( 0 \) עד \( N/2 - 1 \) של שורה 0. כל פתרון כזה והשיקוף שלו נספרים יחד.
        4. ‏\( N \) אי-זוגי : העמודה האמצעית. השיקוף שלה הוא היא עצמה, ולכן בלי להכפיל.

    === "SystemVerilog"
        ```systemverilog title="count_half, canonical, distinct" linenums="1" hl_lines="3 4 26 30 49"
        // count_queens with row 0 limited to the half of the columns (and the middle one).
        function automatic int count_half(int n);
          int count = 2 * count_queens(n, (1 << (n / 2)) - 1);      // (1)!
          if (n % 2) count += count_queens(n, 1 << (n / 2));
          return count;
        endfunction

        // The smallest of the 8 images of p (p[r]: the column of row r), 4 bits a row (n <= 16).
        function automatic longint unsigned canonical(int n, int p[16]);
          longint unsigned best = '1, key;
          int q[16];
          int c, r2, c2;
          for (int t = 0; t < 8; t++) begin                         // (2)!
            for (int r = 0; r < n; r++) begin
              c = p[r];
              case (t)
                0: begin r2 = r;         c2 = c;         end
                1: begin r2 = c;         c2 = n - 1 - r; end
                2: begin r2 = n - 1 - r; c2 = n - 1 - c; end
                3: begin r2 = n - 1 - c; c2 = r;         end
                4: begin r2 = r;         c2 = n - 1 - c; end
                5: begin r2 = c;         c2 = r;         end
                6: begin r2 = n - 1 - r; c2 = c;         end
                default: begin r2 = n - 1 - c; c2 = n - 1 - r; end
              endcase
              q[r2] = c2;
            end
            key = 0;
            for (int r = 0; r < n; r++) key |= longint'(q[r]) << (4 * r);
            if (key < best) best = key;
          end
          return best;
        endfunction

        // The solutions up to rotation and reflection (n <= 16): one smallest image per class.
        function automatic int distinct(int n);
          int unsigned full = (32'd1 << n) - 1;
          int unsigned cols[16], left[16], right[16], free[16];
          int unsigned low;
          int p[16];
          bit seen[longint unsigned];                               // (3)!
          int row = 0;
          cols[0] = 0; left[0] = 0; right[0] = 0; free[0] = full;
          while (row >= 0) begin
            if (free[row] == 0) begin row--; continue; end
            low = free[row] & -free[row];
            free[row] ^= low;
            p[row] = $clog2(low);
            if (row == n - 1) begin seen[canonical(n, p)] = 1; continue; end
            cols[row + 1] = cols[row] | low;
            left[row + 1] = ((left[row] | low) << 1) & full;
            right[row + 1] = (right[row] | low) >> 1;
            free[row + 1] = full & ~(cols[row + 1] | left[row + 1] | right[row + 1]);
            row++;
          end
          return seen.num();
        endfunction
        ```

        1. העמודות \( 0 \) עד \( N/2 - 1 \) של שורה 0, פעמיים. כש-\( N \) אי-זוגי, העמודה האמצעית פעם אחת.
        2. שמונה הסימטריות כמפות של \( (r, c) \) : ארבעה סיבובים, ואחריהם ארבעה שיקופים.
        3. מערך אסוציאטיבי לפי הנציג : כל מחלקה נכנסת פעם אחת, ו-`num()` סופר אותן.

    #### למה זה נכון { .sol-proof }

    **שיקופים לא משאירים אף פתרון.** שיקוף ימין-שמאל משאיר כל מלכה בשורה שלה, ולכן פתרון שלא
    משתנה צריך \( c = N - 1 - c \) בכל שורה, כלומר את כל המלכות בעמודה אחת. אותו דבר עם שיקוף
    למעלה-למטה ושורה אחת. שיקוף באלכסון מעביר את \( (r, c) \) ל-\( (c, r) \). אם \( r \ne c \),
    שתי המלכות האלה על אותו אלכסון שני (\( r + c \) שווה), ולכן כל המלכות על האלכסון הראשי,
    וזה בלתי אפשרי כש-\( N > 1 \). השיקוף באלכסון השני דומה.

    **הנוסחה של Burnside.** אם סופרים זוגות של סימטריה ופתרון שהיא לא משנה, כל מחלקה של \( k \)
    תמונות נותנת בדיוק \( 8 \) זוגות : לכל אחת מ-\( k \) התמונות יש \( 8/k \) סימטריות שלא משנות
    אותה. לכן מספר המחלקות הוא סכום הזוגות חלקי 8.

    #### סיבוכיות { .sol-cost }

    ‏`count_half` מציב כמחצית מהמלכות של `count_queens`. ‏`distinct` עובר על כל הפתרונות, ולכל אחד
    בונה 8 תמונות בזמן \( O(N) \) : ‏\( O(8N) \) לפתרון, מעבר לחיפוש עצמו.

---

### סעיף ג – פתרון לכל N בלי חיפוש { #construction }

תנו נוסחה שנותנת פתרון לכל \( N \ge 4 \) בלי שום חיפוש, והוכיחו שהיא נכונה. למה ל-\( N = 2 \)
ול-\( N = 3 \) אין פתרון בכלל?

??? tip "רמז 1"
    בסעיף הזה השורות והעמודות ממוספרות מ-1. נסו קפיצות של פרש : בשורה 1 העמודה 2, בשורה 2 העמודה
    4, בשורה 3 העמודה 6, וכן הלאה.

??? tip "רמז 2"
    שתי מלכות על קו ששיפועו 2 אף פעם לא באותו אלכסון. אחרי העמודות הזוגיות, מה עם האי-זוגיות?

??? tip "רמז 3"
    הבעיה היחידה היא מלכה מהחצי הזוגי מול מלכה מהחצי האי-זוגי. כתבו את התנאי לאלכסון משותף,
    ובדקו מתי יש לו פתרון.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        כש-\( N \bmod 6 \) אינו 2 או 3 : קודם העמודות הזוגיות \( 2, 4, 6, \dots \), ואחריהן
        האי-זוגיות \( 1, 3, 5, \dots \). כש-\( N \bmod 6 = 2 \), החצי האי-זוגי הוא
        \( 3, 1, 7, 9, \dots, N - 1, 5 \). כש-\( N \bmod 6 = 3 \), הזוגי הוא
        \( 4, 6, \dots, N - 1, 2 \) והאי-זוגי \( 5, 7, \dots, N, 1, 3 \). ל-2 ול-3 אין פתרון, כי
        כל משבצת של המלכה האמצעית מאיימת על כל מה שנשאר.

    <!-- cost: זמן \( O(N) \) | זיכרון \( O(N) \) -->

    #### הרעיון { .sol-idea }

    בחצי הראשון של השורות המלכות בעמודות הזוגיות, כל שורה שתי עמודות הלאה, ובחצי השני בעמודות
    האי-זוגיות. בתוך כל חצי המלכות על קו ששיפועו 2, ולכן אף שתיים לא באותו אלכסון. הנה \( N = 10 \) :

    <!-- gen 7 -->

    <svg class="figure nq-board" viewBox="0 0 386 386" style="max-width:22rem" role="img" aria-label="סעיף ג : הבנייה ל-N = 10. בשורות 1 עד 5 המלכות בעמודות הזוגיות 2, 4, 6, 8, 10, ובשורות 6 עד 10 בעמודות האי-זוגיות 1, 3, 5, 7, 9. בכל חצי המלכות על קו ששיפועו 2, ולכן אף שתיים לא באותו אלכסון"><rect class="nq-sq" x="325" y="24" width="36" height="36"/><rect class="nq-sq is-dark is-even" x="289" y="24" width="36" height="36"/><rect class="nq-sq" x="253" y="24" width="36" height="36"/><rect class="nq-sq is-dark" x="217" y="24" width="36" height="36"/><rect class="nq-sq" x="181" y="24" width="36" height="36"/><rect class="nq-sq is-dark" x="145" y="24" width="36" height="36"/><rect class="nq-sq" x="109" y="24" width="36" height="36"/><rect class="nq-sq is-dark" x="73" y="24" width="36" height="36"/><rect class="nq-sq" x="37" y="24" width="36" height="36"/><rect class="nq-sq is-dark" x="1" y="24" width="36" height="36"/><rect class="nq-sq is-dark" x="325" y="60" width="36" height="36"/><rect class="nq-sq" x="289" y="60" width="36" height="36"/><rect class="nq-sq is-dark" x="253" y="60" width="36" height="36"/><rect class="nq-sq is-even" x="217" y="60" width="36" height="36"/><rect class="nq-sq is-dark" x="181" y="60" width="36" height="36"/><rect class="nq-sq" x="145" y="60" width="36" height="36"/><rect class="nq-sq is-dark" x="109" y="60" width="36" height="36"/><rect class="nq-sq" x="73" y="60" width="36" height="36"/><rect class="nq-sq is-dark" x="37" y="60" width="36" height="36"/><rect class="nq-sq" x="1" y="60" width="36" height="36"/><rect class="nq-sq" x="325" y="96" width="36" height="36"/><rect class="nq-sq is-dark" x="289" y="96" width="36" height="36"/><rect class="nq-sq" x="253" y="96" width="36" height="36"/><rect class="nq-sq is-dark" x="217" y="96" width="36" height="36"/><rect class="nq-sq" x="181" y="96" width="36" height="36"/><rect class="nq-sq is-dark is-even" x="145" y="96" width="36" height="36"/><rect class="nq-sq" x="109" y="96" width="36" height="36"/><rect class="nq-sq is-dark" x="73" y="96" width="36" height="36"/><rect class="nq-sq" x="37" y="96" width="36" height="36"/><rect class="nq-sq is-dark" x="1" y="96" width="36" height="36"/><rect class="nq-sq is-dark" x="325" y="132" width="36" height="36"/><rect class="nq-sq" x="289" y="132" width="36" height="36"/><rect class="nq-sq is-dark" x="253" y="132" width="36" height="36"/><rect class="nq-sq" x="217" y="132" width="36" height="36"/><rect class="nq-sq is-dark" x="181" y="132" width="36" height="36"/><rect class="nq-sq" x="145" y="132" width="36" height="36"/><rect class="nq-sq is-dark" x="109" y="132" width="36" height="36"/><rect class="nq-sq is-even" x="73" y="132" width="36" height="36"/><rect class="nq-sq is-dark" x="37" y="132" width="36" height="36"/><rect class="nq-sq" x="1" y="132" width="36" height="36"/><rect class="nq-sq" x="325" y="168" width="36" height="36"/><rect class="nq-sq is-dark" x="289" y="168" width="36" height="36"/><rect class="nq-sq" x="253" y="168" width="36" height="36"/><rect class="nq-sq is-dark" x="217" y="168" width="36" height="36"/><rect class="nq-sq" x="181" y="168" width="36" height="36"/><rect class="nq-sq is-dark" x="145" y="168" width="36" height="36"/><rect class="nq-sq" x="109" y="168" width="36" height="36"/><rect class="nq-sq is-dark" x="73" y="168" width="36" height="36"/><rect class="nq-sq" x="37" y="168" width="36" height="36"/><rect class="nq-sq is-dark is-even" x="1" y="168" width="36" height="36"/><rect class="nq-sq is-dark is-odd" x="325" y="204" width="36" height="36"/><rect class="nq-sq" x="289" y="204" width="36" height="36"/><rect class="nq-sq is-dark" x="253" y="204" width="36" height="36"/><rect class="nq-sq" x="217" y="204" width="36" height="36"/><rect class="nq-sq is-dark" x="181" y="204" width="36" height="36"/><rect class="nq-sq" x="145" y="204" width="36" height="36"/><rect class="nq-sq is-dark" x="109" y="204" width="36" height="36"/><rect class="nq-sq" x="73" y="204" width="36" height="36"/><rect class="nq-sq is-dark" x="37" y="204" width="36" height="36"/><rect class="nq-sq" x="1" y="204" width="36" height="36"/><rect class="nq-sq" x="325" y="240" width="36" height="36"/><rect class="nq-sq is-dark" x="289" y="240" width="36" height="36"/><rect class="nq-sq is-odd" x="253" y="240" width="36" height="36"/><rect class="nq-sq is-dark" x="217" y="240" width="36" height="36"/><rect class="nq-sq" x="181" y="240" width="36" height="36"/><rect class="nq-sq is-dark" x="145" y="240" width="36" height="36"/><rect class="nq-sq" x="109" y="240" width="36" height="36"/><rect class="nq-sq is-dark" x="73" y="240" width="36" height="36"/><rect class="nq-sq" x="37" y="240" width="36" height="36"/><rect class="nq-sq is-dark" x="1" y="240" width="36" height="36"/><rect class="nq-sq is-dark" x="325" y="276" width="36" height="36"/><rect class="nq-sq" x="289" y="276" width="36" height="36"/><rect class="nq-sq is-dark" x="253" y="276" width="36" height="36"/><rect class="nq-sq" x="217" y="276" width="36" height="36"/><rect class="nq-sq is-dark is-odd" x="181" y="276" width="36" height="36"/><rect class="nq-sq" x="145" y="276" width="36" height="36"/><rect class="nq-sq is-dark" x="109" y="276" width="36" height="36"/><rect class="nq-sq" x="73" y="276" width="36" height="36"/><rect class="nq-sq is-dark" x="37" y="276" width="36" height="36"/><rect class="nq-sq" x="1" y="276" width="36" height="36"/><rect class="nq-sq" x="325" y="312" width="36" height="36"/><rect class="nq-sq is-dark" x="289" y="312" width="36" height="36"/><rect class="nq-sq" x="253" y="312" width="36" height="36"/><rect class="nq-sq is-dark" x="217" y="312" width="36" height="36"/><rect class="nq-sq" x="181" y="312" width="36" height="36"/><rect class="nq-sq is-dark" x="145" y="312" width="36" height="36"/><rect class="nq-sq is-odd" x="109" y="312" width="36" height="36"/><rect class="nq-sq is-dark" x="73" y="312" width="36" height="36"/><rect class="nq-sq" x="37" y="312" width="36" height="36"/><rect class="nq-sq is-dark" x="1" y="312" width="36" height="36"/><rect class="nq-sq is-dark" x="325" y="348" width="36" height="36"/><rect class="nq-sq" x="289" y="348" width="36" height="36"/><rect class="nq-sq is-dark" x="253" y="348" width="36" height="36"/><rect class="nq-sq" x="217" y="348" width="36" height="36"/><rect class="nq-sq is-dark" x="181" y="348" width="36" height="36"/><rect class="nq-sq" x="145" y="348" width="36" height="36"/><rect class="nq-sq is-dark" x="109" y="348" width="36" height="36"/><rect class="nq-sq" x="73" y="348" width="36" height="36"/><rect class="nq-sq is-dark is-odd" x="37" y="348" width="36" height="36"/><rect class="nq-sq" x="1" y="348" width="36" height="36"/><rect class="nq-frame" x="1" y="24" width="360" height="360"/><text class="nq-lab" x="343.0" y="17" text-anchor="middle">1</text><text class="nq-lab" x="307.0" y="17" text-anchor="middle">2</text><text class="nq-lab" x="271.0" y="17" text-anchor="middle">3</text><text class="nq-lab" x="235.0" y="17" text-anchor="middle">4</text><text class="nq-lab" x="199.0" y="17" text-anchor="middle">5</text><text class="nq-lab" x="163.0" y="17" text-anchor="middle">6</text><text class="nq-lab" x="127.0" y="17" text-anchor="middle">7</text><text class="nq-lab" x="91.0" y="17" text-anchor="middle">8</text><text class="nq-lab" x="55.0" y="17" text-anchor="middle">9</text><text class="nq-lab" x="19.0" y="17" text-anchor="middle">10</text><text class="nq-lab" x="366" y="47.0">1</text><text class="nq-lab" x="366" y="83.0">2</text><text class="nq-lab" x="366" y="119.0">3</text><text class="nq-lab" x="366" y="155.0">4</text><text class="nq-lab" x="366" y="191.0">5</text><text class="nq-lab" x="366" y="227.0">6</text><text class="nq-lab" x="366" y="263.0">7</text><text class="nq-lab" x="366" y="299.0">8</text><text class="nq-lab" x="366" y="335.0">9</text><text class="nq-lab" x="366" y="371.0">10</text><g class="nq-q"><polygon points="296.2,48.5 294.0,34.1 301.6,42.0 307.0,30.5 312.4,42.0 320.0,34.1 317.8,48.5"/><rect x="296.2" y="49.2" width="21.6" height="4.0" rx="1.1"/></g><g class="nq-q"><polygon points="224.2,84.5 222.0,70.1 229.6,78.0 235.0,66.5 240.4,78.0 248.0,70.1 245.8,84.5"/><rect x="224.2" y="85.2" width="21.6" height="4.0" rx="1.1"/></g><g class="nq-q"><polygon points="152.2,120.5 150.0,106.1 157.6,114.0 163.0,102.5 168.4,114.0 176.0,106.1 173.8,120.5"/><rect x="152.2" y="121.2" width="21.6" height="4.0" rx="1.1"/></g><g class="nq-q"><polygon points="80.2,156.5 78.0,142.1 85.6,150.0 91.0,138.5 96.4,150.0 104.0,142.1 101.8,156.5"/><rect x="80.2" y="157.2" width="21.6" height="4.0" rx="1.1"/></g><g class="nq-q"><polygon points="8.2,192.5 6.0,178.1 13.6,186.0 19.0,174.5 24.4,186.0 32.0,178.1 29.8,192.5"/><rect x="8.2" y="193.2" width="21.6" height="4.0" rx="1.1"/></g><g class="nq-q"><polygon points="332.2,228.5 330.0,214.1 337.6,222.0 343.0,210.5 348.4,222.0 356.0,214.1 353.8,228.5"/><rect x="332.2" y="229.2" width="21.6" height="4.0" rx="1.1"/></g><g class="nq-q"><polygon points="260.2,264.5 258.0,250.1 265.6,258.0 271.0,246.5 276.4,258.0 284.0,250.1 281.8,264.5"/><rect x="260.2" y="265.2" width="21.6" height="4.0" rx="1.1"/></g><g class="nq-q"><polygon points="188.2,300.5 186.0,286.1 193.6,294.0 199.0,282.5 204.4,294.0 212.0,286.1 209.8,300.5"/><rect x="188.2" y="301.2" width="21.6" height="4.0" rx="1.1"/></g><g class="nq-q"><polygon points="116.2,336.5 114.0,322.1 121.6,330.0 127.0,318.5 132.4,330.0 140.0,322.1 137.8,336.5"/><rect x="116.2" y="337.2" width="21.6" height="4.0" rx="1.1"/></g><g class="nq-q"><polygon points="44.2,372.5 42.0,358.1 49.6,366.0 55.0,354.5 60.4,366.0 68.0,358.1 65.8,372.5"/><rect x="44.2" y="373.2" width="21.6" height="4.0" rx="1.1"/></g></svg>

    <!-- /gen -->

    <!-- gen 8 -->

    <span class="viz-legend"><span><i class="nq-key-even"></i>שורות 1 עד 5 : העמודות הזוגיות</span><span><i class="nq-key-odd"></i>שורות 6 עד 10 : העמודות האי-זוגיות</span><span>העמודה 1 מימין</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שני חצאים :** ‏\( m = \lfloor N/2 \rfloor \). בשורה \( i \le m \) המלכה בעמודה \( 2i \),
       ובשורה \( m + j \) המלכה בעמודה \( 2j - 1 \).

    2. **‏\( N \bmod 6 = 2 \) :** בחצי האי-זוגי מחליפים את 1 ו-3, ומעבירים את 5 לסוף.

    3. **‏\( N \bmod 6 = 3 \) :** בחצי הזוגי מעבירים את 2 לסוף, ובחצי האי-זוגי מעבירים את 1 ו-3
       לסוף.

    4. **הטבלה :** העמודה של המלכה בכל שורה, ל-\( N \) מ-4 עד 12 :

        <!-- gen 9 -->

        | ‏\( N \) | ‏\( N \bmod 6 \) | העמודה של המלכה בשורות 1 עד \( N \) |
        |:-:|:-:|:-:|
        | 4 | 4 | <span dir="ltr">2, 4, 1, 3</span> |
        | 5 | 5 | <span dir="ltr">2, 4, 1, 3, 5</span> |
        | 6 | 0 | <span dir="ltr">2, 4, 6, 1, 3, 5</span> |
        | 7 | 1 | <span dir="ltr">2, 4, 6, 1, 3, 5, 7</span> |
        | 8 | 2 | <span dir="ltr">2, 4, 6, 8, 3, 1, 7, 5</span> |
        | 9 | 3 | <span dir="ltr">4, 6, 8, 2, 5, 7, 9, 1, 3</span> |
        | 10 | 4 | <span dir="ltr">2, 4, 6, 8, 10, 1, 3, 5, 7, 9</span> |
        | 11 | 5 | <span dir="ltr">2, 4, 6, 8, 10, 1, 3, 5, 7, 9, 11</span> |
        | 12 | 0 | <span dir="ltr">2, 4, 6, 8, 10, 12, 1, 3, 5, 7, 9, 11</span> |

        <!-- /gen -->

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="construct" linenums="1" hl_lines="5 6 7 8 9"
        def construct(n: int) -> list[int]:
            """A solution for n >= 4 without search: the column (from 1) of the queen in rows 1 .. n."""
            evens = list(range(2, n + 1, 2))
            odds = list(range(1, n + 1, 2))
            if n % 6 == 2:                                                    # (1)!
                odds = [3, 1] + [c for c in odds if c not in (1, 3, 5)] + [5]
            elif n % 6 == 3:                                                  # (2)!
                evens = [c for c in evens if c != 2] + [2]
                odds = [c for c in odds if c not in (1, 3)] + [1, 3]
            return evens + odds
        ```

        1. ‏1 ו-3 מתחלפים, ו-5 עובר לסוף החצי האי-זוגי.
        2. ‏2 עובר לסוף החצי הזוגי, ו-1 ו-3 לסוף החצי האי-זוגי.

    === "SystemVerilog"
        ```systemverilog title="construct" linenums="1" hl_lines="4 12"
        // A solution for n >= 4 without search: col[i] is the column (from 1) of the queen in row i + 1.
        function automatic void construct(int n, output int col[64]);
          int k = 0;
          if (n % 6 == 3) begin                                     // (1)!
            for (int c = 4; c <= n; c += 2) col[k++] = c;
            col[k++] = 2;
            for (int c = 5; c <= n; c += 2) col[k++] = c;
            col[k++] = 1;
            col[k++] = 3;
          end else begin
            for (int c = 2; c <= n; c += 2) col[k++] = c;
            if (n % 6 == 2) begin                                   // (2)!
              col[k++] = 3;
              col[k++] = 1;
              for (int c = 7; c <= n; c += 2) col[k++] = c;
              col[k++] = 5;
            end else
              for (int c = 1; c <= n; c += 2) col[k++] = c;
          end
        endfunction
        ```

        1. ‏2 עובר לסוף החצי הזוגי, ו-1 ו-3 לסוף החצי האי-זוגי.
        2. ‏1 ו-3 מתחלפים, ו-5 עובר לסוף החצי האי-זוגי.

    #### למה זה נכון { .sol-proof }

    **עמודות.** כל עמודה מ-1 עד \( N \) מופיעה פעם אחת : הזוגיות בחצי אחד והאי-זוגיות בשני.

    **בתוך חצי.** שתי מלכות זוגיות בשורות \( i < i' \) נמצאות בעמודות \( 2i \) ו-\( 2i' \).
    ההפרש בעמודות הוא \( 2(i' - i) \), פעמיים ההפרש בשורות, ולכן הן לא באותו אלכסון. כך גם
    בחצי האי-זוגי.

    **בין החצאים.** מלכה \( (i, 2i) \) ומלכה \( (m + j, 2j - 1) \) באותו אלכסון אם ההפרש בשורות
    שווה להפרש בעמודות, בערך מוחלט :

    \[
    \begin{aligned}
    m + j - i &= 2j - 1 - 2i \\
              &\Longrightarrow\; j = m + i + 1 \\
    m + j - i &= -(2j - 1 - 2i) \\
              &\Longrightarrow\; 3(i - j) = m - 1
    \end{aligned}
    \]

    במקרה הראשון \( j > m + 1 \), יותר מכל מספר העמודות האי-זוגיות, ולכן אין זוג כזה. המקרה
    השני דורש ש-\( m - 1 \) יתחלק ב-3, כלומר \( m \equiv 1 \pmod 3 \). כש-\( m = \lfloor N/2 \rfloor \),
    זה קורה בדיוק כש-\( N \bmod 6 \) הוא 2 או 3. בכל \( N \) אחר אין אף זוג שמאיים, והרשימה פתרון.

    **התיקונים.** כש-\( N \bmod 6 \) הוא 2 או 3, הרשימה הפשוטה נכשלת. למשל ב-\( N = 8 \) המלכות
    \( (2, 4) \) ו-\( (5, 1) \) באותו אלכסון. התיקונים של שלבים 2 ו-3 מזיזים כמה מלכות לסוף
    החצי שלהן, הרחק מהזוגות האלה, ובודקים אותם באותה דרך. הבדיקה של השאלה מריצה את הבנייה לכל
    \( N \) מ-4 עד 1,000.

    **‏2 ו-3.** ב-\( N = 2 \) כל שתי משבצות בשורות שונות ובעמודות שונות נמצאות באלכסון. ב-\( N = 3 \)
    המלכה של השורה האמצעית לא יכולה להיות במרכז, שמאיים על כל הלוח. אם היא בעמודה של צד, היא
    מאיימת על שתי המשבצות הקרובות לה בשורה העליונה ובשורה התחתונה, ובכל שורה כזו נשארת רק המשבצת
    בצד השני. שתי המשבצות האלה באותה עמודה.

    #### סיבוכיות { .sol-cost }

    ‏\( O(N) \) זמן וזיכרון : רשימה אחת של \( N \) עמודות, בלי שום חיפוש. ל-\( N = 1{,}000{,}000 \)
    זה מיידי, ואילו החיפוש של סעיף א כבר ב-\( N = 30 \) לא מסתיים בזמן סביר.

---

### נסו בעצמכם { #place }

מציבים מלכות בעצמכם, והתיבה אומרת אם אפשר להשלים אותן לפתרון. היא מתחילה משלוש המלכות של
סעיף א :

<div class="explorer" data-kind="nqplace" data-n="8" data-queens="0.0_1.4_2.7"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : רק אלכסון אחד"
    בדיקה של `r1 - r2 == c1 - c2` בלבד מפספסת את האלכסון השני, שבו `r1 - r2 == c2 - c1`. עם
    בדיקה כזו ל-8 מלכות יוצאים 2,113 "פתרונות" ולא 92. הבדיקה הנכונה היא
    `abs(r1 - r2) == abs(c1 - c2)`, ובמסכות אלה `left` ו-`right`.

??? trap "מלכודת : free בלי & full"
    ב-Python `~x` הוא מספר שלילי, עם אינסוף אחדות משמאל. בלי `& full`, ‏`free` אף פעם לא מתרוקן
    והלולאה לא נגמרת. בשפה עם רוחב קבוע, כמו SystemVerilog, ‏`1 << N` צריך \( N + 1 \) ביטים,
    ולכן במילה של 32 ביטים הקוד מוגבל ל-\( N \le 31 \). ביט ש-`<< 1` מוציא מהמילה לא חסר : הוא
    ממילא מחוץ ללוח.

??? trap "מלכודת : לספור פתרון מסובב כפתרון אחר"
    אם השאלה היא "כמה פתרונות שונים", התשובה 12, לא 92. ואם מחלקים את 92 ב-8 יוצא \( 11.5 \) :
    המחלקה של 4 היא הסיבה.

??? trap "מלכודת : לנסות את כל המשבצות לכל מלכה"
    לבחור 8 משבצות מתוך 64 זה \( \binom{64}{8} \approx 4.4 \cdot 10^9 \) אפשרויות. מלכה אחת בכל
    שורה מורידה את זה ל-\( 8^8 \approx 1.7 \cdot 10^7 \), עמודה שונה בכל שורה ל-\( 8! = 40{,}320 \),
    והחזרה המוקדמת אחורה ל-2,056 הצבות בלבד.

??? followup "שאלות המשך"
    - **הספירה לכל N :** מה מספר הפתרונות ל-\( N \) מ-1 עד 12?

        ??? fu-answer "תשובה"
            ‏1, 0, 0, 2, 10, 4, 40, 92, 352, 724, 2,680, 14,200. ל-6 יש פחות פתרונות מאשר ל-5, ואין
            נוסחה סגורה : הספירה ידועה רק בחיפוש, עד \( N = 27 \) בערך.

    - **על טורוס :** מה קורה כשהאלכסונים ממשיכים מעבר לקצה לצד השני?

        ??? fu-answer "תשובה"
            יש פתרון בדיוק כש-\( N \) זר ל-6 (פוליה). למשל המלכה של שורה \( r \) בעמודה
            \( 2r \bmod N \). ל-5 יש 10 פתרונות כאלה ול-7 יש 28, ול-4, ל-6, ל-8 ול-9 אין אף אחד.

    - **צריחים ורצים :** כמה צריחים אפשר לשים בלי איומים, ובכמה דרכים? וכמה רצים לכל היותר?

        ??? fu-answer "תשובה"
            ‏\( N \) צריחים, ב-\( N! \) דרכים : כל שורה ועמודה פעם אחת, בלי אלכסונים. רצים : עד
            \( 2N - 2 \), כי יש \( 2N - 1 \) אלכסונים בכל כיוון, ושני האלכסונים הקצרים בפינות
            הנגדיות לא יכולים להיות מלאים שניהם.

    - **הפתרון הראשון :** איך מוצאים פתרון אחד, בלי לספור את כולם?

        ??? fu-answer "תשובה"
            אותו חיפוש, שעוצר בפתרון הראשון. ל-8 מלכות הוא מגיע אחרי 113 הצבות בלבד. לכל \( N \)
            גדול עדיף סעיף ג.
