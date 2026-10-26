---
id: 14
title: ריבועים ומלבנים אקראיים בלי חפיפה
level: junior
difficulty: medium
kind: dv
tags: [systemverilog, constraints, randomization, geometry, python]
source: ""
added: 2026-10-16
---

## השאלה

נתון grid של נקודות בגודל \( N \times M \) : הנקודות הן \( (x, y) \) עם \( 1 \le x \le N \)
ו-\( 1 \le y \le M \). על ה-grid מציירים צורות שהפינות שלהן נמצאות על נקודות של ה-grid.
כל צורה מתוארת על ידי שתי נקודות :

- **נקודת ההתחלה \( (x_1, y_1) \) :** הפינה השמאלית התחתונה.
- **נקודת הסוף \( (x_2, y_2) \) :** הפינה הימנית העליונה.

מהן מקבלים את הגודל : הרוחב הוא \( x_2 - x_1 \) והגובה הוא \( y_2 - y_1 \).

<svg class="figure" viewBox="0 0 330 250" style="max-width:30rem" role="img" aria-label="grid של 10 על 8 נקודות, ריבוע מ-(x1, y1) עד (x2, y2) ומלבן מ-(7, 2) עד (10, 6)"><line class="gp-line" x1="40" x2="40" y1="14" y2="224"/><line class="gp-line" x1="70" x2="70" y1="14" y2="224"/><line class="gp-line" x1="100" x2="100" y1="14" y2="224"/><line class="gp-line" x1="130" x2="130" y1="14" y2="224"/><line class="gp-line" x1="160" x2="160" y1="14" y2="224"/><line class="gp-line" x1="190" x2="190" y1="14" y2="224"/><line class="gp-line" x1="220" x2="220" y1="14" y2="224"/><line class="gp-line" x1="250" x2="250" y1="14" y2="224"/><line class="gp-line" x1="280" x2="280" y1="14" y2="224"/><line class="gp-line" x1="310" x2="310" y1="14" y2="224"/><line class="gp-line" x1="40" x2="310" y1="224" y2="224"/><line class="gp-line" x1="40" x2="310" y1="194" y2="194"/><line class="gp-line" x1="40" x2="310" y1="164" y2="164"/><line class="gp-line" x1="40" x2="310" y1="134" y2="134"/><line class="gp-line" x1="40" x2="310" y1="104" y2="104"/><line class="gp-line" x1="40" x2="310" y1="74" y2="74"/><line class="gp-line" x1="40" x2="310" y1="44" y2="44"/><line class="gp-line" x1="40" x2="310" y1="14" y2="14"/><circle class="gp-dot" cx="40" cy="224" r="1.8"/><circle class="gp-dot" cx="40" cy="194" r="1.8"/><circle class="gp-dot" cx="40" cy="164" r="1.8"/><circle class="gp-dot" cx="40" cy="134" r="1.8"/><circle class="gp-dot" cx="40" cy="104" r="1.8"/><circle class="gp-dot" cx="40" cy="74" r="1.8"/><circle class="gp-dot" cx="40" cy="44" r="1.8"/><circle class="gp-dot" cx="40" cy="14" r="1.8"/><circle class="gp-dot" cx="70" cy="224" r="1.8"/><circle class="gp-dot" cx="70" cy="194" r="1.8"/><circle class="gp-dot" cx="70" cy="164" r="1.8"/><circle class="gp-dot" cx="70" cy="134" r="1.8"/><circle class="gp-dot" cx="70" cy="104" r="1.8"/><circle class="gp-dot" cx="70" cy="74" r="1.8"/><circle class="gp-dot" cx="70" cy="44" r="1.8"/><circle class="gp-dot" cx="70" cy="14" r="1.8"/><circle class="gp-dot" cx="100" cy="224" r="1.8"/><circle class="gp-dot" cx="100" cy="194" r="1.8"/><circle class="gp-dot" cx="100" cy="164" r="1.8"/><circle class="gp-dot" cx="100" cy="134" r="1.8"/><circle class="gp-dot" cx="100" cy="104" r="1.8"/><circle class="gp-dot" cx="100" cy="74" r="1.8"/><circle class="gp-dot" cx="100" cy="44" r="1.8"/><circle class="gp-dot" cx="100" cy="14" r="1.8"/><circle class="gp-dot" cx="130" cy="224" r="1.8"/><circle class="gp-dot" cx="130" cy="194" r="1.8"/><circle class="gp-dot" cx="130" cy="164" r="1.8"/><circle class="gp-dot" cx="130" cy="134" r="1.8"/><circle class="gp-dot" cx="130" cy="104" r="1.8"/><circle class="gp-dot" cx="130" cy="74" r="1.8"/><circle class="gp-dot" cx="130" cy="44" r="1.8"/><circle class="gp-dot" cx="130" cy="14" r="1.8"/><circle class="gp-dot" cx="160" cy="224" r="1.8"/><circle class="gp-dot" cx="160" cy="194" r="1.8"/><circle class="gp-dot" cx="160" cy="164" r="1.8"/><circle class="gp-dot" cx="160" cy="134" r="1.8"/><circle class="gp-dot" cx="160" cy="104" r="1.8"/><circle class="gp-dot" cx="160" cy="74" r="1.8"/><circle class="gp-dot" cx="160" cy="44" r="1.8"/><circle class="gp-dot" cx="160" cy="14" r="1.8"/><circle class="gp-dot" cx="190" cy="224" r="1.8"/><circle class="gp-dot" cx="190" cy="194" r="1.8"/><circle class="gp-dot" cx="190" cy="164" r="1.8"/><circle class="gp-dot" cx="190" cy="134" r="1.8"/><circle class="gp-dot" cx="190" cy="104" r="1.8"/><circle class="gp-dot" cx="190" cy="74" r="1.8"/><circle class="gp-dot" cx="190" cy="44" r="1.8"/><circle class="gp-dot" cx="190" cy="14" r="1.8"/><circle class="gp-dot" cx="220" cy="224" r="1.8"/><circle class="gp-dot" cx="220" cy="194" r="1.8"/><circle class="gp-dot" cx="220" cy="164" r="1.8"/><circle class="gp-dot" cx="220" cy="134" r="1.8"/><circle class="gp-dot" cx="220" cy="104" r="1.8"/><circle class="gp-dot" cx="220" cy="74" r="1.8"/><circle class="gp-dot" cx="220" cy="44" r="1.8"/><circle class="gp-dot" cx="220" cy="14" r="1.8"/><circle class="gp-dot" cx="250" cy="224" r="1.8"/><circle class="gp-dot" cx="250" cy="194" r="1.8"/><circle class="gp-dot" cx="250" cy="164" r="1.8"/><circle class="gp-dot" cx="250" cy="134" r="1.8"/><circle class="gp-dot" cx="250" cy="104" r="1.8"/><circle class="gp-dot" cx="250" cy="74" r="1.8"/><circle class="gp-dot" cx="250" cy="44" r="1.8"/><circle class="gp-dot" cx="250" cy="14" r="1.8"/><circle class="gp-dot" cx="280" cy="224" r="1.8"/><circle class="gp-dot" cx="280" cy="194" r="1.8"/><circle class="gp-dot" cx="280" cy="164" r="1.8"/><circle class="gp-dot" cx="280" cy="134" r="1.8"/><circle class="gp-dot" cx="280" cy="104" r="1.8"/><circle class="gp-dot" cx="280" cy="74" r="1.8"/><circle class="gp-dot" cx="280" cy="44" r="1.8"/><circle class="gp-dot" cx="280" cy="14" r="1.8"/><circle class="gp-dot" cx="310" cy="224" r="1.8"/><circle class="gp-dot" cx="310" cy="194" r="1.8"/><circle class="gp-dot" cx="310" cy="164" r="1.8"/><circle class="gp-dot" cx="310" cy="134" r="1.8"/><circle class="gp-dot" cx="310" cy="104" r="1.8"/><circle class="gp-dot" cx="310" cy="74" r="1.8"/><circle class="gp-dot" cx="310" cy="44" r="1.8"/><circle class="gp-dot" cx="310" cy="14" r="1.8"/><text class="tick" x="40" y="242" text-anchor="middle">1</text><text class="tick" x="70" y="242" text-anchor="middle">2</text><text class="tick" x="100" y="242" text-anchor="middle">3</text><text class="tick" x="130" y="242" text-anchor="middle">4</text><text class="tick" x="160" y="242" text-anchor="middle">5</text><text class="tick" x="190" y="242" text-anchor="middle">6</text><text class="tick" x="220" y="242" text-anchor="middle">7</text><text class="tick" x="250" y="242" text-anchor="middle">8</text><text class="tick" x="280" y="242" text-anchor="middle">9</text><text class="tick" x="310" y="242" text-anchor="middle">10</text><text class="tick" x="30" y="228" text-anchor="end">1</text><text class="tick" x="30" y="198" text-anchor="end">2</text><text class="tick" x="30" y="168" text-anchor="end">3</text><text class="tick" x="30" y="138" text-anchor="end">4</text><text class="tick" x="30" y="108" text-anchor="end">5</text><text class="tick" x="30" y="78" text-anchor="end">6</text><text class="tick" x="30" y="48" text-anchor="end">7</text><text class="tick" x="30" y="18" text-anchor="end">8</text><rect class="shp-1" x="70" y="104" width="90" height="90"/><rect class="shp-2" x="220" y="74" width="90" height="120"/><circle class="ink-fill" cx="70" cy="194" r="4"/><text class="coord" x="76" y="212" text-anchor="start">(x1, y1)</text><circle class="ink-fill" cx="160" cy="104" r="4"/><text class="coord" x="154" y="96" text-anchor="end">(x2, y2)</text><circle class="ink-fill" cx="220" cy="194" r="4"/><text class="coord" x="226" y="212" text-anchor="start">(7, 2)</text><circle class="ink-fill" cx="310" cy="74" r="4"/><text class="coord" x="304" y="66" text-anchor="end">(10, 6)</text><text class="legend halo" x="115.0" y="154.0" text-anchor="middle" direction="rtl">ריבוע 3 על 3</text><text class="legend halo" x="265.0" y="124.0" text-anchor="middle" direction="rtl">מלבן</text><text class="legend halo" x="265.0" y="154.0" text-anchor="middle" direction="rtl">רוחב 3, גובה 4</text></svg>

המטרה : להגריל **מספר אקראי של צורות**, כך שאף שתי צורות **לא חופפות**, כלומר אין להן
שטח משותף. מותר שצורות יהיו **צמודות** : צלע משותפת, חלק מצלע או רק פינה משותפת.

בדוגמאות נשתמש ב-\( N = 10 \), ‏\( M = 8 \), ובמספר צורות בין 1 ל-6.

??? interviewer "מה המראיין בודק"
    - **לפרק לתנאים :** האם המועמד כותב קודם את כל התנאים על צורה **אחת** (איפה היא, מה
      הגודל שלה, מה הופך אותה לריבוע), ורק אחר כך את התנאי על **זוג** צורות.
    - **צמוד מול חופף :** ההבדל בין "צמודות" ל"חופפות" צריך להופיע בקוד כסימן אחד מדויק.
      מראיין טוב ישאל מה קורה כששתי צורות חולקות צלע.
    - **תנאי נכון לכל זוג :** האם בדיקת החפיפה נכונה לכל שני מלבנים, ולא רק לזוגות שנראים
      כמו בדוגמאות שעל הלוח.
    - **לבדוק את התוצאה :** ב-DV לא סומכים על `randomize()`. מצפים לבדוק את ערך ההחזרה
      שלו ולהריץ בודק שכתוב בנפרד מה-constraints.
    - **הכללה :** כמה מהפתרון צריך לשכתב כשעוברים מריבועים למלבנים, ואיזה מנגנון של השפה
      עושה את זה בלי להעתיק קוד.

---

### סעיף א – ריבועים

כתבו קוד ב-SystemVerilog או ב-Python שמגריל מספר אקראי של **ריבועים** על ה-grid, בלי
חפיפה ביניהם.

??? tip "רמז 1"
    כתבו קודם את כל התנאים על ריבוע **אחד** : איפה הוא יכול להיות ומה הופך אותו לריבוע.
    רק אחר כך עברו לתנאי על **זוג** ריבועים.

??? tip "רמז 2"
    קשה לתאר ישירות מתי שני ריבועים חופפים. קל יותר לתאר מתי הם **לא** חופפים : איפה
    הריבוע השני יכול להיות ביחס לראשון?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מחלקה עם ארבעה constraints : כמות, בתוך ה-grid, רוחב שווה לגובה, ולכל זוג
        \( i < j \) התנאי **"‏\( j \) משמאל, מימין, מתחת או מעל \( i \)"** עם \( \le \), כדי
        שצורות צמודות יהיו מותרות. בודק נפרד מאמת את התוצאה עם אותם תנאים.

    <!-- cost: תנאים \( n(n-1)/2 \) | שלב \( O(196 \cdot n) \) -->

    #### הרעיון { .sol-idea }

    במקום לתאר מתי שתי צורות חופפות, מתארים מתי הן **לא** חופפות : \( j \) נמצאת כולה
    באחד מארבעת האזורים סביב \( i \). ארבעה תנאים פשוטים מחוברים ב-"או", והסימן \( \le \)
    הוא מה שמאפשר צלע או פינה משותפת.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **כמות :** מגרילים \( n \) בין 1 ל-MAX_SHAPES, וגודל כל ארבעת המערכים שווה ל-\( n \).
    2. **כל צורה בתוך ה-grid :** \( 1 \le x_1 < x_2 \le N \) ו-\( 1 \le y_1 < y_2 \le M \).
       האי-שוויון החזק נותן גם את הכיוון וגם צלע באורך 1 לפחות.
    3. **כל צורה ריבוע :** הרוחב שווה לגובה.
    4. **כל זוג בלי חפיפה :** לכל \( i < j \), הצורה \( j \) משמאל, מימין, מתחת או מעל
       \( i \), ב-"או".
    5. **בודק נפרד :** אחרי `randomize()` בודקים שהוא החזיר 1, ומריצים פונקציה שכתובה
       בנפרד ובודקת את אותם תנאים.

    </div>

    **כל התנאים בטבלה אחת.** נסמן את מספר הצורות ב-\( n \), ואת הצורה ה-\( i \)-ית
    ב-\( (x_1[i], y_1[i]) \) עד \( (x_2[i], y_2[i]) \).

    | התנאי | על מה | מה הוא אומר |
    |---|---|---|
    | כמות | כל הקבוצה | ‏\( 1 \le n \le \) MAX_SHAPES |
    | בתוך ה-grid | כל צורה | ‏\( 1 \le x_1 \), ‏\( x_2 \le N \), ‏\( 1 \le y_1 \), ‏\( y_2 \le M \) |
    | כיוון וגודל | כל צורה | ‏\( x_1 < x_2 \) ו-\( y_1 < y_2 \) : ההתחלה משמאל ולמטה מהסוף, והצלע לפחות 1 |
    | ריבוע | כל צורה | ‏\( x_2 - x_1 = y_2 - y_1 \) : הרוחב שווה לגובה |
    | בלי חפיפה | כל זוג \( i < j \) | אחד מארבעת המקרים בתרשים שבהמשך |

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="class square_set" linenums="1" hl_lines="31 32 33"
        class square_set;
          int N = 10, M = 8;             // grid points (1,1) .. (N,M)
          int MAX_SHAPES = 6;            // must fit: at most (N-1)*(M-1) unit squares

          rand int n;                          // how many shapes
          rand int x1[], y1[], x2[], y2[];     // shape i: start (x1,y1), end (x2,y2)

          // 1. How many shapes; the array sizes follow n
          constraint c_count {
            n inside {[1:MAX_SHAPES]};
            x1.size() == n;  y1.size() == n;  x2.size() == n;  y2.size() == n;   // (1)!
          }

          // 2. Every shape is on the grid, and its end is above and to the right of its start
          constraint c_on_grid {
            foreach (x1[i]) {
              x1[i] >= 1;  x2[i] <= N;  x1[i] < x2[i];   // (2)!
              y1[i] >= 1;  y2[i] <= M;  y1[i] < y2[i];
            }
          }

          // 3. Width equals height
          constraint c_square {
            foreach (x1[i]) x2[i] - x1[i] == y2[i] - y1[i];   // (3)!
          }

          // 4. No overlap: j is left of, right of, below or above i.
          //    "<=" (not "<") lets two shapes share an edge or a corner.
          constraint c_no_overlap {
            foreach (x1[i]) foreach (x1[j])
              if (i < j)   // (4)!
                x2[j] <= x1[i] || x2[i] <= x1[j] ||   // j left of i, or j right of i
                y2[j] <= y1[i] || y2[i] <= y1[j];     // j below i, or j above i
          }
        endclass
        ```

        1. ה-constraint על `size()` קובע את גודל המערכים הדינמיים. לפי התקן הגדלים נפתרים
           קודם, ורק אחר כך האיברים, ולכן ה-`foreach` בהמשך יודע על כמה צורות לעבור.
        2. ‏`x1[i] < x2[i]` עושה שתי עבודות : ההתחלה משמאל לסוף, והצלע באורך 1 לפחות. בלי
           זה היה אפשר לקבל "ריבוע" ברוחב 0 או צורה הפוכה.
        3. התנאי היחיד שמיוחד לריבועים. הוא יושב ב-constraint נפרד בכוונה, כדי שבסעיף ב
           אפשר יהיה להחליף או לכבות רק אותו.
        4. בלי `i < j` הלולאה הכפולה הייתה כוללת גם את \( i = j \), ושם אף אחד מארבעת
           המקרים לא מתקיים (צורה תמיד חופפת לעצמה), ולכן `randomize()` היה נכשל תמיד.
           עם התנאי כל זוג נבדק פעם אחת, \( n(n-1)/2 \) תנאים.

        כמה נקודות על הקוד :

        - **מערכים דינמיים :** ה-constraint על `size()` קובע את גודל המערכים. לפי התקן הגדלים
          נפתרים קודם, ורק אחר כך האיברים.
        - **‏`i < j` :** כל זוג נבדק פעם אחת, כלומר \( n(n-1)/2 \) תנאים. בלי התנאי הזה
          הלולאה הייתה כוללת גם את \( i = j \), ושם אף אחד מארבעת המקרים לא מתקיים (צורה
          תמיד חופפת לעצמה), ולכן `randomize()` היה נכשל תמיד.
        - **‏MAX_SHAPES :** חייב להיות אפשרי. ב-grid של \( N \times M \) נקודות נכנסים לכל היותר
          \( (N-1)(M-1) \) ריבועים, כולם בגודל 1.
        - **בלי סדר בין הצורות :** לא צריך להחליט מי ממוקמת ראשונה. ה-solver מוצא פתרון לכל
          התנאים יחד.

    === "Python"
        ```python title="random_shapes" linenums="1" hl_lines="8 26 27"
        import random


        def overlap(a, b):
            """Do shapes a and b share area? Sharing an edge or a corner is fine."""
            ax1, ay1, ax2, ay2 = a
            bx1, by1, bx2, by2 = b
            return ax1 < bx2 and bx1 < ax2 and ay1 < by2 and by1 < ay2   # (1)!


        def candidates(N, M, squares):
            """Every shape (x1, y1, x2, y2) that fits on the grid."""
            for x1 in range(1, N):
                for x2 in range(x1 + 1, N + 1):
                    for y1 in range(1, M):
                        for y2 in range(y1 + 1, M + 1):
                            if not squares or x2 - x1 == y2 - y1:   # (2)!
                                yield (x1, y1, x2, y2)


        def random_shapes(N, M, max_shapes, squares=True, rng=random):
            n = rng.randint(1, max_shapes)                  # how many shapes
            while True:                                     # retry until all n fit (3)
                shapes = []
                for _ in range(n):
                    free = [c for c in candidates(N, M, squares)
                            if not any(overlap(c, s) for s in shapes)]
                    if not free:
                        break                               # no room left: start over (4)
                    shapes.append(rng.choice(free))
                if len(shapes) == n:
                    return shapes
        ```

        1. זו צורת ה-"וגם" של תנאי החפיפה : חפיפה בציר \( x \) **וגם** בציר \( y \), עם
           \( < \) חזק. השלילה שלה היא בדיוק ארבעת המקרים עם \( \le \) שב-constraint.
        2. אותו תנאי "רוחב שווה לגובה", אבל כפרמטר : כך סעיף ב משתמש באותה פונקציה בלי
           להעתיק אותה.
        3. אין solver, ולכן אין הבטחה שכל \( n \) הצורות ייכנסו בניסיון הראשון. הלולאה
           החיצונית מנסה שוב עם אותו \( n \), כדי שההתפלגות של \( n \) לא תוטה לכמויות
           קטנות.
        4. כשלא נשאר מקום לצורה הבאה, לא מוותרים על צורה אחת אלא זורקים את כל הקבוצה.
           אחרת הקבוצות הצפופות היו מקבלות פחות צורות ממה שהוגרל.

        ב-Python אין solver, ולכן בונים את הקבוצה צורה אחרי צורה :

        - **מגרילים את \( n \).**
        - **בכל שלב :** עוברים על כל הצורות שנכנסות ל-grid (`candidates`), משאירים רק את אלה
          שלא חופפות לאף צורה שכבר נבחרה, ומגרילים אחת מהן.
        - **אם נתקעים :** כלומר לא נשאר מקום לצורה הבאה, מתחילים מחדש עם אותו \( n \).

        עם \( N = 10 \) ו-\( M = 8 \) יש 196 ריבועים אפשריים, ולכן הסריקה בכל שלב מהירה.

    **בודק : אותם תנאים כקוד רגיל.** ב-DV לא סומכים על `randomize()` בלי לבדוק : בודקים
    שהוא החזיר 1, ומריצים בודק שכתוב בנפרד מה-constraints. כאן הבודק משתמש בצורת ה-"וגם"
    של תנאי החפיפה :

    === "SystemVerilog"
        ```systemverilog title="function shapes_ok" linenums="1" hl_lines="9 10"
        // The same rules as plain code, for a scoreboard or post_randomize()
        function automatic bit shapes_ok(int N, int M, bit squares,
                                         int x1[], int y1[], int x2[], int y2[]);
          foreach (x1[i]) begin
            if (x1[i] < 1 || x2[i] > N || x1[i] >= x2[i]) return 0;     // on the grid
            if (y1[i] < 1 || y2[i] > M || y1[i] >= y2[i]) return 0;
            if (squares && x2[i] - x1[i] != y2[i] - y1[i]) return 0;   // a square
            for (int j = 0; j < i; j++)                                  // every earlier shape (1)
              if (x1[i] < x2[j] && x1[j] < x2[i] &&
                  y1[i] < y2[j] && y1[j] < y2[i]) return 0;              // overlap (2)
          end
          return 1;
        endfunction

        // Usage
        // square_set s = new();
        // if (!s.randomize()) $fatal(1, "randomize failed");
        // if (!shapes_ok(s.N, s.M, 1, s.x1, s.y1, s.x2, s.y2)) $error("illegal shapes");
        ```

        1. ‏`j < i` ולא `j != i` : כל זוג נבדק פעם אחת, בדיוק כמו `i < j` ב-constraint.
        2. הבודק כתוב בצורת ה-"וגם" ולא ב-"או" של ה-constraint. שתי צורות שונות של אותו
           תנאי הן בדיוק מה שרוצים מבודק בלתי תלוי : טעות בניסוח אחד לא תעבור בשני.

    === "Python"
        ```python title="shapes_ok"
        def shapes_ok(N, M, shapes, squares=True):
            for k, (x1, y1, x2, y2) in enumerate(shapes):
                if not (1 <= x1 < x2 <= N and 1 <= y1 < y2 <= M):     # on the grid
                    return False
                if squares and x2 - x1 != y2 - y1:                    # a square
                    return False
                if any(overlap(shapes[k], s) for s in shapes[:k]):    # every earlier shape (1)
                    return False
            return True
        ```

        1. ‏`shapes[:k]` הן רק הצורות שלפני \( k \), ולכן כל זוג נבדק פעם אחת. הבודק משתמש
           ב-`overlap`, צורת ה-"וגם" של התנאי.

    #### למה זה נכון { .sol-proof }

    **מה מותר ומה אסור.**

    <svg class="figure" viewBox="0 0 432 280" role="img" aria-label="זוגות של ריבועים : ארבעה מותרים ושניים אסורים"><line class="gp-line" x1="17" x2="17" y1="10" y2="98"/><line class="gp-line" x1="39" x2="39" y1="10" y2="98"/><line class="gp-line" x1="61" x2="61" y1="10" y2="98"/><line class="gp-line" x1="83" x2="83" y1="10" y2="98"/><line class="gp-line" x1="105" x2="105" y1="10" y2="98"/><line class="gp-line" x1="127" x2="127" y1="10" y2="98"/><line class="gp-line" x1="17" x2="127" y1="98" y2="98"/><line class="gp-line" x1="17" x2="127" y1="76" y2="76"/><line class="gp-line" x1="17" x2="127" y1="54" y2="54"/><line class="gp-line" x1="17" x2="127" y1="32" y2="32"/><line class="gp-line" x1="17" x2="127" y1="10" y2="10"/><circle class="gp-dot" cx="17" cy="98" r="1.8"/><circle class="gp-dot" cx="17" cy="76" r="1.8"/><circle class="gp-dot" cx="17" cy="54" r="1.8"/><circle class="gp-dot" cx="17" cy="32" r="1.8"/><circle class="gp-dot" cx="17" cy="10" r="1.8"/><circle class="gp-dot" cx="39" cy="98" r="1.8"/><circle class="gp-dot" cx="39" cy="76" r="1.8"/><circle class="gp-dot" cx="39" cy="54" r="1.8"/><circle class="gp-dot" cx="39" cy="32" r="1.8"/><circle class="gp-dot" cx="39" cy="10" r="1.8"/><circle class="gp-dot" cx="61" cy="98" r="1.8"/><circle class="gp-dot" cx="61" cy="76" r="1.8"/><circle class="gp-dot" cx="61" cy="54" r="1.8"/><circle class="gp-dot" cx="61" cy="32" r="1.8"/><circle class="gp-dot" cx="61" cy="10" r="1.8"/><circle class="gp-dot" cx="83" cy="98" r="1.8"/><circle class="gp-dot" cx="83" cy="76" r="1.8"/><circle class="gp-dot" cx="83" cy="54" r="1.8"/><circle class="gp-dot" cx="83" cy="32" r="1.8"/><circle class="gp-dot" cx="83" cy="10" r="1.8"/><circle class="gp-dot" cx="105" cy="98" r="1.8"/><circle class="gp-dot" cx="105" cy="76" r="1.8"/><circle class="gp-dot" cx="105" cy="54" r="1.8"/><circle class="gp-dot" cx="105" cy="32" r="1.8"/><circle class="gp-dot" cx="105" cy="10" r="1.8"/><circle class="gp-dot" cx="127" cy="98" r="1.8"/><circle class="gp-dot" cx="127" cy="76" r="1.8"/><circle class="gp-dot" cx="127" cy="54" r="1.8"/><circle class="gp-dot" cx="127" cy="32" r="1.8"/><circle class="gp-dot" cx="127" cy="10" r="1.8"/><rect class="shp-1" x="17" y="54" width="44" height="44"/><rect class="shp-2" x="83" y="32" width="44" height="44"/><text class="legend" x="72.0" y="120" text-anchor="middle" direction="rtl">✓ רחוקים</text><line class="gp-line" x1="161" x2="161" y1="10" y2="98"/><line class="gp-line" x1="183" x2="183" y1="10" y2="98"/><line class="gp-line" x1="205" x2="205" y1="10" y2="98"/><line class="gp-line" x1="227" x2="227" y1="10" y2="98"/><line class="gp-line" x1="249" x2="249" y1="10" y2="98"/><line class="gp-line" x1="271" x2="271" y1="10" y2="98"/><line class="gp-line" x1="161" x2="271" y1="98" y2="98"/><line class="gp-line" x1="161" x2="271" y1="76" y2="76"/><line class="gp-line" x1="161" x2="271" y1="54" y2="54"/><line class="gp-line" x1="161" x2="271" y1="32" y2="32"/><line class="gp-line" x1="161" x2="271" y1="10" y2="10"/><circle class="gp-dot" cx="161" cy="98" r="1.8"/><circle class="gp-dot" cx="161" cy="76" r="1.8"/><circle class="gp-dot" cx="161" cy="54" r="1.8"/><circle class="gp-dot" cx="161" cy="32" r="1.8"/><circle class="gp-dot" cx="161" cy="10" r="1.8"/><circle class="gp-dot" cx="183" cy="98" r="1.8"/><circle class="gp-dot" cx="183" cy="76" r="1.8"/><circle class="gp-dot" cx="183" cy="54" r="1.8"/><circle class="gp-dot" cx="183" cy="32" r="1.8"/><circle class="gp-dot" cx="183" cy="10" r="1.8"/><circle class="gp-dot" cx="205" cy="98" r="1.8"/><circle class="gp-dot" cx="205" cy="76" r="1.8"/><circle class="gp-dot" cx="205" cy="54" r="1.8"/><circle class="gp-dot" cx="205" cy="32" r="1.8"/><circle class="gp-dot" cx="205" cy="10" r="1.8"/><circle class="gp-dot" cx="227" cy="98" r="1.8"/><circle class="gp-dot" cx="227" cy="76" r="1.8"/><circle class="gp-dot" cx="227" cy="54" r="1.8"/><circle class="gp-dot" cx="227" cy="32" r="1.8"/><circle class="gp-dot" cx="227" cy="10" r="1.8"/><circle class="gp-dot" cx="249" cy="98" r="1.8"/><circle class="gp-dot" cx="249" cy="76" r="1.8"/><circle class="gp-dot" cx="249" cy="54" r="1.8"/><circle class="gp-dot" cx="249" cy="32" r="1.8"/><circle class="gp-dot" cx="249" cy="10" r="1.8"/><circle class="gp-dot" cx="271" cy="98" r="1.8"/><circle class="gp-dot" cx="271" cy="76" r="1.8"/><circle class="gp-dot" cx="271" cy="54" r="1.8"/><circle class="gp-dot" cx="271" cy="32" r="1.8"/><circle class="gp-dot" cx="271" cy="10" r="1.8"/><rect class="shp-1" x="161" y="54" width="44" height="44"/><rect class="shp-2" x="205" y="54" width="44" height="44"/><text class="legend" x="216.0" y="120" text-anchor="middle" direction="rtl">✓ צלע משותפת</text><line class="gp-line" x1="305" x2="305" y1="10" y2="98"/><line class="gp-line" x1="327" x2="327" y1="10" y2="98"/><line class="gp-line" x1="349" x2="349" y1="10" y2="98"/><line class="gp-line" x1="371" x2="371" y1="10" y2="98"/><line class="gp-line" x1="393" x2="393" y1="10" y2="98"/><line class="gp-line" x1="415" x2="415" y1="10" y2="98"/><line class="gp-line" x1="305" x2="415" y1="98" y2="98"/><line class="gp-line" x1="305" x2="415" y1="76" y2="76"/><line class="gp-line" x1="305" x2="415" y1="54" y2="54"/><line class="gp-line" x1="305" x2="415" y1="32" y2="32"/><line class="gp-line" x1="305" x2="415" y1="10" y2="10"/><circle class="gp-dot" cx="305" cy="98" r="1.8"/><circle class="gp-dot" cx="305" cy="76" r="1.8"/><circle class="gp-dot" cx="305" cy="54" r="1.8"/><circle class="gp-dot" cx="305" cy="32" r="1.8"/><circle class="gp-dot" cx="305" cy="10" r="1.8"/><circle class="gp-dot" cx="327" cy="98" r="1.8"/><circle class="gp-dot" cx="327" cy="76" r="1.8"/><circle class="gp-dot" cx="327" cy="54" r="1.8"/><circle class="gp-dot" cx="327" cy="32" r="1.8"/><circle class="gp-dot" cx="327" cy="10" r="1.8"/><circle class="gp-dot" cx="349" cy="98" r="1.8"/><circle class="gp-dot" cx="349" cy="76" r="1.8"/><circle class="gp-dot" cx="349" cy="54" r="1.8"/><circle class="gp-dot" cx="349" cy="32" r="1.8"/><circle class="gp-dot" cx="349" cy="10" r="1.8"/><circle class="gp-dot" cx="371" cy="98" r="1.8"/><circle class="gp-dot" cx="371" cy="76" r="1.8"/><circle class="gp-dot" cx="371" cy="54" r="1.8"/><circle class="gp-dot" cx="371" cy="32" r="1.8"/><circle class="gp-dot" cx="371" cy="10" r="1.8"/><circle class="gp-dot" cx="393" cy="98" r="1.8"/><circle class="gp-dot" cx="393" cy="76" r="1.8"/><circle class="gp-dot" cx="393" cy="54" r="1.8"/><circle class="gp-dot" cx="393" cy="32" r="1.8"/><circle class="gp-dot" cx="393" cy="10" r="1.8"/><circle class="gp-dot" cx="415" cy="98" r="1.8"/><circle class="gp-dot" cx="415" cy="76" r="1.8"/><circle class="gp-dot" cx="415" cy="54" r="1.8"/><circle class="gp-dot" cx="415" cy="32" r="1.8"/><circle class="gp-dot" cx="415" cy="10" r="1.8"/><rect class="shp-1" x="305" y="54" width="44" height="44"/><rect class="shp-2" x="349" y="10" width="66" height="66"/><text class="legend" x="360.0" y="120" text-anchor="middle" direction="rtl">✓ חלק מצלע</text><line class="gp-line" x1="17" x2="17" y1="150" y2="238"/><line class="gp-line" x1="39" x2="39" y1="150" y2="238"/><line class="gp-line" x1="61" x2="61" y1="150" y2="238"/><line class="gp-line" x1="83" x2="83" y1="150" y2="238"/><line class="gp-line" x1="105" x2="105" y1="150" y2="238"/><line class="gp-line" x1="127" x2="127" y1="150" y2="238"/><line class="gp-line" x1="17" x2="127" y1="238" y2="238"/><line class="gp-line" x1="17" x2="127" y1="216" y2="216"/><line class="gp-line" x1="17" x2="127" y1="194" y2="194"/><line class="gp-line" x1="17" x2="127" y1="172" y2="172"/><line class="gp-line" x1="17" x2="127" y1="150" y2="150"/><circle class="gp-dot" cx="17" cy="238" r="1.8"/><circle class="gp-dot" cx="17" cy="216" r="1.8"/><circle class="gp-dot" cx="17" cy="194" r="1.8"/><circle class="gp-dot" cx="17" cy="172" r="1.8"/><circle class="gp-dot" cx="17" cy="150" r="1.8"/><circle class="gp-dot" cx="39" cy="238" r="1.8"/><circle class="gp-dot" cx="39" cy="216" r="1.8"/><circle class="gp-dot" cx="39" cy="194" r="1.8"/><circle class="gp-dot" cx="39" cy="172" r="1.8"/><circle class="gp-dot" cx="39" cy="150" r="1.8"/><circle class="gp-dot" cx="61" cy="238" r="1.8"/><circle class="gp-dot" cx="61" cy="216" r="1.8"/><circle class="gp-dot" cx="61" cy="194" r="1.8"/><circle class="gp-dot" cx="61" cy="172" r="1.8"/><circle class="gp-dot" cx="61" cy="150" r="1.8"/><circle class="gp-dot" cx="83" cy="238" r="1.8"/><circle class="gp-dot" cx="83" cy="216" r="1.8"/><circle class="gp-dot" cx="83" cy="194" r="1.8"/><circle class="gp-dot" cx="83" cy="172" r="1.8"/><circle class="gp-dot" cx="83" cy="150" r="1.8"/><circle class="gp-dot" cx="105" cy="238" r="1.8"/><circle class="gp-dot" cx="105" cy="216" r="1.8"/><circle class="gp-dot" cx="105" cy="194" r="1.8"/><circle class="gp-dot" cx="105" cy="172" r="1.8"/><circle class="gp-dot" cx="105" cy="150" r="1.8"/><circle class="gp-dot" cx="127" cy="238" r="1.8"/><circle class="gp-dot" cx="127" cy="216" r="1.8"/><circle class="gp-dot" cx="127" cy="194" r="1.8"/><circle class="gp-dot" cx="127" cy="172" r="1.8"/><circle class="gp-dot" cx="127" cy="150" r="1.8"/><rect class="shp-1" x="17" y="194" width="44" height="44"/><rect class="shp-2" x="61" y="150" width="44" height="44"/><text class="legend" x="72.0" y="260" text-anchor="middle" direction="rtl">✓ פינה משותפת</text><line class="gp-line" x1="161" x2="161" y1="150" y2="238"/><line class="gp-line" x1="183" x2="183" y1="150" y2="238"/><line class="gp-line" x1="205" x2="205" y1="150" y2="238"/><line class="gp-line" x1="227" x2="227" y1="150" y2="238"/><line class="gp-line" x1="249" x2="249" y1="150" y2="238"/><line class="gp-line" x1="271" x2="271" y1="150" y2="238"/><line class="gp-line" x1="161" x2="271" y1="238" y2="238"/><line class="gp-line" x1="161" x2="271" y1="216" y2="216"/><line class="gp-line" x1="161" x2="271" y1="194" y2="194"/><line class="gp-line" x1="161" x2="271" y1="172" y2="172"/><line class="gp-line" x1="161" x2="271" y1="150" y2="150"/><circle class="gp-dot" cx="161" cy="238" r="1.8"/><circle class="gp-dot" cx="161" cy="216" r="1.8"/><circle class="gp-dot" cx="161" cy="194" r="1.8"/><circle class="gp-dot" cx="161" cy="172" r="1.8"/><circle class="gp-dot" cx="161" cy="150" r="1.8"/><circle class="gp-dot" cx="183" cy="238" r="1.8"/><circle class="gp-dot" cx="183" cy="216" r="1.8"/><circle class="gp-dot" cx="183" cy="194" r="1.8"/><circle class="gp-dot" cx="183" cy="172" r="1.8"/><circle class="gp-dot" cx="183" cy="150" r="1.8"/><circle class="gp-dot" cx="205" cy="238" r="1.8"/><circle class="gp-dot" cx="205" cy="216" r="1.8"/><circle class="gp-dot" cx="205" cy="194" r="1.8"/><circle class="gp-dot" cx="205" cy="172" r="1.8"/><circle class="gp-dot" cx="205" cy="150" r="1.8"/><circle class="gp-dot" cx="227" cy="238" r="1.8"/><circle class="gp-dot" cx="227" cy="216" r="1.8"/><circle class="gp-dot" cx="227" cy="194" r="1.8"/><circle class="gp-dot" cx="227" cy="172" r="1.8"/><circle class="gp-dot" cx="227" cy="150" r="1.8"/><circle class="gp-dot" cx="249" cy="238" r="1.8"/><circle class="gp-dot" cx="249" cy="216" r="1.8"/><circle class="gp-dot" cx="249" cy="194" r="1.8"/><circle class="gp-dot" cx="249" cy="172" r="1.8"/><circle class="gp-dot" cx="249" cy="150" r="1.8"/><circle class="gp-dot" cx="271" cy="238" r="1.8"/><circle class="gp-dot" cx="271" cy="216" r="1.8"/><circle class="gp-dot" cx="271" cy="194" r="1.8"/><circle class="gp-dot" cx="271" cy="172" r="1.8"/><circle class="gp-dot" cx="271" cy="150" r="1.8"/><rect class="shp-1" x="161" y="172" width="66" height="66"/><rect class="shp-2" x="205" y="172" width="44" height="44"/><rect class="shp-bad" x="205" y="172" width="22" height="44"/><text class="legend" x="216.0" y="260" text-anchor="middle" direction="rtl">✗ חפיפה</text><line class="gp-line" x1="305" x2="305" y1="150" y2="238"/><line class="gp-line" x1="327" x2="327" y1="150" y2="238"/><line class="gp-line" x1="349" x2="349" y1="150" y2="238"/><line class="gp-line" x1="371" x2="371" y1="150" y2="238"/><line class="gp-line" x1="393" x2="393" y1="150" y2="238"/><line class="gp-line" x1="415" x2="415" y1="150" y2="238"/><line class="gp-line" x1="305" x2="415" y1="238" y2="238"/><line class="gp-line" x1="305" x2="415" y1="216" y2="216"/><line class="gp-line" x1="305" x2="415" y1="194" y2="194"/><line class="gp-line" x1="305" x2="415" y1="172" y2="172"/><line class="gp-line" x1="305" x2="415" y1="150" y2="150"/><circle class="gp-dot" cx="305" cy="238" r="1.8"/><circle class="gp-dot" cx="305" cy="216" r="1.8"/><circle class="gp-dot" cx="305" cy="194" r="1.8"/><circle class="gp-dot" cx="305" cy="172" r="1.8"/><circle class="gp-dot" cx="305" cy="150" r="1.8"/><circle class="gp-dot" cx="327" cy="238" r="1.8"/><circle class="gp-dot" cx="327" cy="216" r="1.8"/><circle class="gp-dot" cx="327" cy="194" r="1.8"/><circle class="gp-dot" cx="327" cy="172" r="1.8"/><circle class="gp-dot" cx="327" cy="150" r="1.8"/><circle class="gp-dot" cx="349" cy="238" r="1.8"/><circle class="gp-dot" cx="349" cy="216" r="1.8"/><circle class="gp-dot" cx="349" cy="194" r="1.8"/><circle class="gp-dot" cx="349" cy="172" r="1.8"/><circle class="gp-dot" cx="349" cy="150" r="1.8"/><circle class="gp-dot" cx="371" cy="238" r="1.8"/><circle class="gp-dot" cx="371" cy="216" r="1.8"/><circle class="gp-dot" cx="371" cy="194" r="1.8"/><circle class="gp-dot" cx="371" cy="172" r="1.8"/><circle class="gp-dot" cx="371" cy="150" r="1.8"/><circle class="gp-dot" cx="393" cy="238" r="1.8"/><circle class="gp-dot" cx="393" cy="216" r="1.8"/><circle class="gp-dot" cx="393" cy="194" r="1.8"/><circle class="gp-dot" cx="393" cy="172" r="1.8"/><circle class="gp-dot" cx="393" cy="150" r="1.8"/><circle class="gp-dot" cx="415" cy="238" r="1.8"/><circle class="gp-dot" cx="415" cy="216" r="1.8"/><circle class="gp-dot" cx="415" cy="194" r="1.8"/><circle class="gp-dot" cx="415" cy="172" r="1.8"/><circle class="gp-dot" cx="415" cy="150" r="1.8"/><rect class="shp-1" x="305" y="150" width="88" height="88"/><rect class="shp-2" x="327" y="172" width="44" height="44"/><rect class="shp-bad" x="327" y="172" width="44" height="44"/><text class="legend" x="360.0" y="260" text-anchor="middle" direction="rtl">✗ אחד בתוך השני</text></svg>

    **נסו בעצמכם.** "עוד צורה" מגריל מועמד אקראי מבין כל הצורות שנכנסות ב-grid : מועמד
    שחופף צורה קיימת מהבהב באדום ונדחה, והראשון הפנוי נכנס בירוק. זו בדיוק בחירה אחידה
    מבין המועמדים הפנויים, כמו `rng.choice(free)` בדף. "הגרלה שלמה" מריץ את
    `random_shapes`, ומפת החום אחרי 500 הגרלות מראה איפה הצורות נוחתות ולמה רובן קטנות.
    המתג עובר למלבנים של סעיף ב. עם "ההטלות על הצירים", מועמד שנדחה מצויר עם ההטלות שלו ושל
    הצורה שהוא חופף : הן נפגשות גם על ציר \( x \) וגם על ציר \( y \). מתחת לתיבה שתי צורות
    להזזה, עם ארבעת המקרים של הדף שנדלקים ונכבים בזמן הגרירה.

    <div class="explorer" data-kind="shapes" data-n="10" data-m="8" data-max="6"></div>

    **מתי שני ריבועים לא חופפים.** שני ריבועים \( i \) ו-\( j \) לא חופפים אם ורק אם
    \( j \) נמצא **כולו** באחד מארבעת האזורים סביב \( i \) :

    <svg class="figure" viewBox="0 0 310 232" style="max-width:22rem" role="img" aria-label="ארבעת האזורים סביב ריבוע i : משמאל, מימין, מתחת ומעל"><line class="gp-line" x1="20" x2="20" y1="10" y2="220"/><line class="gp-line" x1="50" x2="50" y1="10" y2="220"/><line class="gp-line" x1="80" x2="80" y1="10" y2="220"/><line class="gp-line" x1="110" x2="110" y1="10" y2="220"/><line class="gp-line" x1="140" x2="140" y1="10" y2="220"/><line class="gp-line" x1="170" x2="170" y1="10" y2="220"/><line class="gp-line" x1="200" x2="200" y1="10" y2="220"/><line class="gp-line" x1="230" x2="230" y1="10" y2="220"/><line class="gp-line" x1="260" x2="260" y1="10" y2="220"/><line class="gp-line" x1="290" x2="290" y1="10" y2="220"/><line class="gp-line" x1="20" x2="290" y1="220" y2="220"/><line class="gp-line" x1="20" x2="290" y1="190" y2="190"/><line class="gp-line" x1="20" x2="290" y1="160" y2="160"/><line class="gp-line" x1="20" x2="290" y1="130" y2="130"/><line class="gp-line" x1="20" x2="290" y1="100" y2="100"/><line class="gp-line" x1="20" x2="290" y1="70" y2="70"/><line class="gp-line" x1="20" x2="290" y1="40" y2="40"/><line class="gp-line" x1="20" x2="290" y1="10" y2="10"/><circle class="gp-dot" cx="20" cy="220" r="1.8"/><circle class="gp-dot" cx="20" cy="190" r="1.8"/><circle class="gp-dot" cx="20" cy="160" r="1.8"/><circle class="gp-dot" cx="20" cy="130" r="1.8"/><circle class="gp-dot" cx="20" cy="100" r="1.8"/><circle class="gp-dot" cx="20" cy="70" r="1.8"/><circle class="gp-dot" cx="20" cy="40" r="1.8"/><circle class="gp-dot" cx="20" cy="10" r="1.8"/><circle class="gp-dot" cx="50" cy="220" r="1.8"/><circle class="gp-dot" cx="50" cy="190" r="1.8"/><circle class="gp-dot" cx="50" cy="160" r="1.8"/><circle class="gp-dot" cx="50" cy="130" r="1.8"/><circle class="gp-dot" cx="50" cy="100" r="1.8"/><circle class="gp-dot" cx="50" cy="70" r="1.8"/><circle class="gp-dot" cx="50" cy="40" r="1.8"/><circle class="gp-dot" cx="50" cy="10" r="1.8"/><circle class="gp-dot" cx="80" cy="220" r="1.8"/><circle class="gp-dot" cx="80" cy="190" r="1.8"/><circle class="gp-dot" cx="80" cy="160" r="1.8"/><circle class="gp-dot" cx="80" cy="130" r="1.8"/><circle class="gp-dot" cx="80" cy="100" r="1.8"/><circle class="gp-dot" cx="80" cy="70" r="1.8"/><circle class="gp-dot" cx="80" cy="40" r="1.8"/><circle class="gp-dot" cx="80" cy="10" r="1.8"/><circle class="gp-dot" cx="110" cy="220" r="1.8"/><circle class="gp-dot" cx="110" cy="190" r="1.8"/><circle class="gp-dot" cx="110" cy="160" r="1.8"/><circle class="gp-dot" cx="110" cy="130" r="1.8"/><circle class="gp-dot" cx="110" cy="100" r="1.8"/><circle class="gp-dot" cx="110" cy="70" r="1.8"/><circle class="gp-dot" cx="110" cy="40" r="1.8"/><circle class="gp-dot" cx="110" cy="10" r="1.8"/><circle class="gp-dot" cx="140" cy="220" r="1.8"/><circle class="gp-dot" cx="140" cy="190" r="1.8"/><circle class="gp-dot" cx="140" cy="160" r="1.8"/><circle class="gp-dot" cx="140" cy="130" r="1.8"/><circle class="gp-dot" cx="140" cy="100" r="1.8"/><circle class="gp-dot" cx="140" cy="70" r="1.8"/><circle class="gp-dot" cx="140" cy="40" r="1.8"/><circle class="gp-dot" cx="140" cy="10" r="1.8"/><circle class="gp-dot" cx="170" cy="220" r="1.8"/><circle class="gp-dot" cx="170" cy="190" r="1.8"/><circle class="gp-dot" cx="170" cy="160" r="1.8"/><circle class="gp-dot" cx="170" cy="130" r="1.8"/><circle class="gp-dot" cx="170" cy="100" r="1.8"/><circle class="gp-dot" cx="170" cy="70" r="1.8"/><circle class="gp-dot" cx="170" cy="40" r="1.8"/><circle class="gp-dot" cx="170" cy="10" r="1.8"/><circle class="gp-dot" cx="200" cy="220" r="1.8"/><circle class="gp-dot" cx="200" cy="190" r="1.8"/><circle class="gp-dot" cx="200" cy="160" r="1.8"/><circle class="gp-dot" cx="200" cy="130" r="1.8"/><circle class="gp-dot" cx="200" cy="100" r="1.8"/><circle class="gp-dot" cx="200" cy="70" r="1.8"/><circle class="gp-dot" cx="200" cy="40" r="1.8"/><circle class="gp-dot" cx="200" cy="10" r="1.8"/><circle class="gp-dot" cx="230" cy="220" r="1.8"/><circle class="gp-dot" cx="230" cy="190" r="1.8"/><circle class="gp-dot" cx="230" cy="160" r="1.8"/><circle class="gp-dot" cx="230" cy="130" r="1.8"/><circle class="gp-dot" cx="230" cy="100" r="1.8"/><circle class="gp-dot" cx="230" cy="70" r="1.8"/><circle class="gp-dot" cx="230" cy="40" r="1.8"/><circle class="gp-dot" cx="230" cy="10" r="1.8"/><circle class="gp-dot" cx="260" cy="220" r="1.8"/><circle class="gp-dot" cx="260" cy="190" r="1.8"/><circle class="gp-dot" cx="260" cy="160" r="1.8"/><circle class="gp-dot" cx="260" cy="130" r="1.8"/><circle class="gp-dot" cx="260" cy="100" r="1.8"/><circle class="gp-dot" cx="260" cy="70" r="1.8"/><circle class="gp-dot" cx="260" cy="40" r="1.8"/><circle class="gp-dot" cx="260" cy="10" r="1.8"/><circle class="gp-dot" cx="290" cy="220" r="1.8"/><circle class="gp-dot" cx="290" cy="190" r="1.8"/><circle class="gp-dot" cx="290" cy="160" r="1.8"/><circle class="gp-dot" cx="290" cy="130" r="1.8"/><circle class="gp-dot" cx="290" cy="100" r="1.8"/><circle class="gp-dot" cx="290" cy="70" r="1.8"/><circle class="gp-dot" cx="290" cy="40" r="1.8"/><circle class="gp-dot" cx="290" cy="10" r="1.8"/><rect class="sep-zone" x="20" y="10" width="90" height="210"/><rect class="sep-zone" x="200" y="10" width="90" height="210"/><rect class="sep-zone" x="20" y="160" width="270" height="60"/><rect class="sep-zone" x="20" y="10" width="270" height="60"/><line class="dash" x1="110" x2="110" y1="10" y2="220"/><line class="dash" x1="200" x2="200" y1="10" y2="220"/><line class="dash" x1="20" x2="290" y1="160" y2="160"/><line class="dash" x1="20" x2="290" y1="70" y2="70"/><rect class="shp-1" x="110" y="70" width="90" height="90"/><text class="shp-num" x="155.0" y="120.0" text-anchor="middle">i</text><text class="zone-label" x="65.0" y="120.0" text-anchor="middle" direction="rtl">משמאל</text><text class="zone-label" x="245.0" y="120.0" text-anchor="middle" direction="rtl">מימין</text><text class="zone-label" x="155.0" y="195.0" text-anchor="middle" direction="rtl">מתחת</text><text class="zone-label" x="155.0" y="45.0" text-anchor="middle" direction="rtl">מעל</text></svg>

    - **משמאל :** \( x_2[j] \le x_1[i] \).
    - **מימין :** \( x_2[i] \le x_1[j] \).
    - **מתחת :** \( y_2[j] \le y_1[i] \).
    - **מעל :** \( y_2[i] \le y_1[j] \).

    מספיק שאחד מהם מתקיים, ולכן מחברים אותם ב-"או". בפינות האזורים חופפים (למשל משמאל
    וגם מתחת), וזה בסדר.

    הסימן \( \le \) ולא \( < \) הוא מה שמאפשר צלע משותפת : כש-\( x_2[j] = x_1[i] \), הצלע
    הימנית של \( j \) היא בדיוק הצלע השמאלית של \( i \).

    אותו תנאי בצורה הפוכה : שני ריבועים **חופפים** אם ורק אם הם חופפים גם בציר \( x \) וגם
    בציר \( y \) :

    \[
    \begin{aligned}
             & x_1[i] < x_2[j] \;\wedge\; x_1[j] < x_2[i] \\
    \wedge\; & y_1[i] < y_2[j] \;\wedge\; y_1[j] < y_2[i]
    \end{aligned}
    \]

    זה בדיוק השלילה של ה-"או" (כלל דה-מורגן). ב-constraint נוח יותר להשתמש ב-"או", ובבודק
    נוח יותר להשתמש ב-"וגם".

    **דוגמאות להגרלות.** כל תמונה היא הגרלה אחת. שימו לב לריבועים צמודים, עם צלע או פינה
    משותפת :

    <svg class="figure" viewBox="0 0 714 198" role="img" aria-label="שלוש הגרלות של ריבועים בלי חפיפה"><line class="gp-line" x1="20" x2="20" y1="10" y2="164"/><line class="gp-line" x1="42" x2="42" y1="10" y2="164"/><line class="gp-line" x1="64" x2="64" y1="10" y2="164"/><line class="gp-line" x1="86" x2="86" y1="10" y2="164"/><line class="gp-line" x1="108" x2="108" y1="10" y2="164"/><line class="gp-line" x1="130" x2="130" y1="10" y2="164"/><line class="gp-line" x1="152" x2="152" y1="10" y2="164"/><line class="gp-line" x1="174" x2="174" y1="10" y2="164"/><line class="gp-line" x1="196" x2="196" y1="10" y2="164"/><line class="gp-line" x1="218" x2="218" y1="10" y2="164"/><line class="gp-line" x1="20" x2="218" y1="164" y2="164"/><line class="gp-line" x1="20" x2="218" y1="142" y2="142"/><line class="gp-line" x1="20" x2="218" y1="120" y2="120"/><line class="gp-line" x1="20" x2="218" y1="98" y2="98"/><line class="gp-line" x1="20" x2="218" y1="76" y2="76"/><line class="gp-line" x1="20" x2="218" y1="54" y2="54"/><line class="gp-line" x1="20" x2="218" y1="32" y2="32"/><line class="gp-line" x1="20" x2="218" y1="10" y2="10"/><circle class="gp-dot" cx="20" cy="164" r="1.8"/><circle class="gp-dot" cx="20" cy="142" r="1.8"/><circle class="gp-dot" cx="20" cy="120" r="1.8"/><circle class="gp-dot" cx="20" cy="98" r="1.8"/><circle class="gp-dot" cx="20" cy="76" r="1.8"/><circle class="gp-dot" cx="20" cy="54" r="1.8"/><circle class="gp-dot" cx="20" cy="32" r="1.8"/><circle class="gp-dot" cx="20" cy="10" r="1.8"/><circle class="gp-dot" cx="42" cy="164" r="1.8"/><circle class="gp-dot" cx="42" cy="142" r="1.8"/><circle class="gp-dot" cx="42" cy="120" r="1.8"/><circle class="gp-dot" cx="42" cy="98" r="1.8"/><circle class="gp-dot" cx="42" cy="76" r="1.8"/><circle class="gp-dot" cx="42" cy="54" r="1.8"/><circle class="gp-dot" cx="42" cy="32" r="1.8"/><circle class="gp-dot" cx="42" cy="10" r="1.8"/><circle class="gp-dot" cx="64" cy="164" r="1.8"/><circle class="gp-dot" cx="64" cy="142" r="1.8"/><circle class="gp-dot" cx="64" cy="120" r="1.8"/><circle class="gp-dot" cx="64" cy="98" r="1.8"/><circle class="gp-dot" cx="64" cy="76" r="1.8"/><circle class="gp-dot" cx="64" cy="54" r="1.8"/><circle class="gp-dot" cx="64" cy="32" r="1.8"/><circle class="gp-dot" cx="64" cy="10" r="1.8"/><circle class="gp-dot" cx="86" cy="164" r="1.8"/><circle class="gp-dot" cx="86" cy="142" r="1.8"/><circle class="gp-dot" cx="86" cy="120" r="1.8"/><circle class="gp-dot" cx="86" cy="98" r="1.8"/><circle class="gp-dot" cx="86" cy="76" r="1.8"/><circle class="gp-dot" cx="86" cy="54" r="1.8"/><circle class="gp-dot" cx="86" cy="32" r="1.8"/><circle class="gp-dot" cx="86" cy="10" r="1.8"/><circle class="gp-dot" cx="108" cy="164" r="1.8"/><circle class="gp-dot" cx="108" cy="142" r="1.8"/><circle class="gp-dot" cx="108" cy="120" r="1.8"/><circle class="gp-dot" cx="108" cy="98" r="1.8"/><circle class="gp-dot" cx="108" cy="76" r="1.8"/><circle class="gp-dot" cx="108" cy="54" r="1.8"/><circle class="gp-dot" cx="108" cy="32" r="1.8"/><circle class="gp-dot" cx="108" cy="10" r="1.8"/><circle class="gp-dot" cx="130" cy="164" r="1.8"/><circle class="gp-dot" cx="130" cy="142" r="1.8"/><circle class="gp-dot" cx="130" cy="120" r="1.8"/><circle class="gp-dot" cx="130" cy="98" r="1.8"/><circle class="gp-dot" cx="130" cy="76" r="1.8"/><circle class="gp-dot" cx="130" cy="54" r="1.8"/><circle class="gp-dot" cx="130" cy="32" r="1.8"/><circle class="gp-dot" cx="130" cy="10" r="1.8"/><circle class="gp-dot" cx="152" cy="164" r="1.8"/><circle class="gp-dot" cx="152" cy="142" r="1.8"/><circle class="gp-dot" cx="152" cy="120" r="1.8"/><circle class="gp-dot" cx="152" cy="98" r="1.8"/><circle class="gp-dot" cx="152" cy="76" r="1.8"/><circle class="gp-dot" cx="152" cy="54" r="1.8"/><circle class="gp-dot" cx="152" cy="32" r="1.8"/><circle class="gp-dot" cx="152" cy="10" r="1.8"/><circle class="gp-dot" cx="174" cy="164" r="1.8"/><circle class="gp-dot" cx="174" cy="142" r="1.8"/><circle class="gp-dot" cx="174" cy="120" r="1.8"/><circle class="gp-dot" cx="174" cy="98" r="1.8"/><circle class="gp-dot" cx="174" cy="76" r="1.8"/><circle class="gp-dot" cx="174" cy="54" r="1.8"/><circle class="gp-dot" cx="174" cy="32" r="1.8"/><circle class="gp-dot" cx="174" cy="10" r="1.8"/><circle class="gp-dot" cx="196" cy="164" r="1.8"/><circle class="gp-dot" cx="196" cy="142" r="1.8"/><circle class="gp-dot" cx="196" cy="120" r="1.8"/><circle class="gp-dot" cx="196" cy="98" r="1.8"/><circle class="gp-dot" cx="196" cy="76" r="1.8"/><circle class="gp-dot" cx="196" cy="54" r="1.8"/><circle class="gp-dot" cx="196" cy="32" r="1.8"/><circle class="gp-dot" cx="196" cy="10" r="1.8"/><circle class="gp-dot" cx="218" cy="164" r="1.8"/><circle class="gp-dot" cx="218" cy="142" r="1.8"/><circle class="gp-dot" cx="218" cy="120" r="1.8"/><circle class="gp-dot" cx="218" cy="98" r="1.8"/><circle class="gp-dot" cx="218" cy="76" r="1.8"/><circle class="gp-dot" cx="218" cy="54" r="1.8"/><circle class="gp-dot" cx="218" cy="32" r="1.8"/><circle class="gp-dot" cx="218" cy="10" r="1.8"/><rect class="shp-1" x="64" y="76" width="88" height="88"/><text class="shp-num" x="108.0" y="124.0" text-anchor="middle">1</text><rect class="shp-2" x="42" y="10" width="66" height="66"/><text class="shp-num" x="75.0" y="47.0" text-anchor="middle">2</text><rect class="shp-3" x="152" y="76" width="22" height="22"/><text class="shp-num" x="163.0" y="91.0" text-anchor="middle">3</text><text class="legend" x="119.0" y="186" text-anchor="middle" direction="rtl">הגרלה 1 : 3 ריבועים</text><line class="gp-line" x1="258" x2="258" y1="10" y2="164"/><line class="gp-line" x1="280" x2="280" y1="10" y2="164"/><line class="gp-line" x1="302" x2="302" y1="10" y2="164"/><line class="gp-line" x1="324" x2="324" y1="10" y2="164"/><line class="gp-line" x1="346" x2="346" y1="10" y2="164"/><line class="gp-line" x1="368" x2="368" y1="10" y2="164"/><line class="gp-line" x1="390" x2="390" y1="10" y2="164"/><line class="gp-line" x1="412" x2="412" y1="10" y2="164"/><line class="gp-line" x1="434" x2="434" y1="10" y2="164"/><line class="gp-line" x1="456" x2="456" y1="10" y2="164"/><line class="gp-line" x1="258" x2="456" y1="164" y2="164"/><line class="gp-line" x1="258" x2="456" y1="142" y2="142"/><line class="gp-line" x1="258" x2="456" y1="120" y2="120"/><line class="gp-line" x1="258" x2="456" y1="98" y2="98"/><line class="gp-line" x1="258" x2="456" y1="76" y2="76"/><line class="gp-line" x1="258" x2="456" y1="54" y2="54"/><line class="gp-line" x1="258" x2="456" y1="32" y2="32"/><line class="gp-line" x1="258" x2="456" y1="10" y2="10"/><circle class="gp-dot" cx="258" cy="164" r="1.8"/><circle class="gp-dot" cx="258" cy="142" r="1.8"/><circle class="gp-dot" cx="258" cy="120" r="1.8"/><circle class="gp-dot" cx="258" cy="98" r="1.8"/><circle class="gp-dot" cx="258" cy="76" r="1.8"/><circle class="gp-dot" cx="258" cy="54" r="1.8"/><circle class="gp-dot" cx="258" cy="32" r="1.8"/><circle class="gp-dot" cx="258" cy="10" r="1.8"/><circle class="gp-dot" cx="280" cy="164" r="1.8"/><circle class="gp-dot" cx="280" cy="142" r="1.8"/><circle class="gp-dot" cx="280" cy="120" r="1.8"/><circle class="gp-dot" cx="280" cy="98" r="1.8"/><circle class="gp-dot" cx="280" cy="76" r="1.8"/><circle class="gp-dot" cx="280" cy="54" r="1.8"/><circle class="gp-dot" cx="280" cy="32" r="1.8"/><circle class="gp-dot" cx="280" cy="10" r="1.8"/><circle class="gp-dot" cx="302" cy="164" r="1.8"/><circle class="gp-dot" cx="302" cy="142" r="1.8"/><circle class="gp-dot" cx="302" cy="120" r="1.8"/><circle class="gp-dot" cx="302" cy="98" r="1.8"/><circle class="gp-dot" cx="302" cy="76" r="1.8"/><circle class="gp-dot" cx="302" cy="54" r="1.8"/><circle class="gp-dot" cx="302" cy="32" r="1.8"/><circle class="gp-dot" cx="302" cy="10" r="1.8"/><circle class="gp-dot" cx="324" cy="164" r="1.8"/><circle class="gp-dot" cx="324" cy="142" r="1.8"/><circle class="gp-dot" cx="324" cy="120" r="1.8"/><circle class="gp-dot" cx="324" cy="98" r="1.8"/><circle class="gp-dot" cx="324" cy="76" r="1.8"/><circle class="gp-dot" cx="324" cy="54" r="1.8"/><circle class="gp-dot" cx="324" cy="32" r="1.8"/><circle class="gp-dot" cx="324" cy="10" r="1.8"/><circle class="gp-dot" cx="346" cy="164" r="1.8"/><circle class="gp-dot" cx="346" cy="142" r="1.8"/><circle class="gp-dot" cx="346" cy="120" r="1.8"/><circle class="gp-dot" cx="346" cy="98" r="1.8"/><circle class="gp-dot" cx="346" cy="76" r="1.8"/><circle class="gp-dot" cx="346" cy="54" r="1.8"/><circle class="gp-dot" cx="346" cy="32" r="1.8"/><circle class="gp-dot" cx="346" cy="10" r="1.8"/><circle class="gp-dot" cx="368" cy="164" r="1.8"/><circle class="gp-dot" cx="368" cy="142" r="1.8"/><circle class="gp-dot" cx="368" cy="120" r="1.8"/><circle class="gp-dot" cx="368" cy="98" r="1.8"/><circle class="gp-dot" cx="368" cy="76" r="1.8"/><circle class="gp-dot" cx="368" cy="54" r="1.8"/><circle class="gp-dot" cx="368" cy="32" r="1.8"/><circle class="gp-dot" cx="368" cy="10" r="1.8"/><circle class="gp-dot" cx="390" cy="164" r="1.8"/><circle class="gp-dot" cx="390" cy="142" r="1.8"/><circle class="gp-dot" cx="390" cy="120" r="1.8"/><circle class="gp-dot" cx="390" cy="98" r="1.8"/><circle class="gp-dot" cx="390" cy="76" r="1.8"/><circle class="gp-dot" cx="390" cy="54" r="1.8"/><circle class="gp-dot" cx="390" cy="32" r="1.8"/><circle class="gp-dot" cx="390" cy="10" r="1.8"/><circle class="gp-dot" cx="412" cy="164" r="1.8"/><circle class="gp-dot" cx="412" cy="142" r="1.8"/><circle class="gp-dot" cx="412" cy="120" r="1.8"/><circle class="gp-dot" cx="412" cy="98" r="1.8"/><circle class="gp-dot" cx="412" cy="76" r="1.8"/><circle class="gp-dot" cx="412" cy="54" r="1.8"/><circle class="gp-dot" cx="412" cy="32" r="1.8"/><circle class="gp-dot" cx="412" cy="10" r="1.8"/><circle class="gp-dot" cx="434" cy="164" r="1.8"/><circle class="gp-dot" cx="434" cy="142" r="1.8"/><circle class="gp-dot" cx="434" cy="120" r="1.8"/><circle class="gp-dot" cx="434" cy="98" r="1.8"/><circle class="gp-dot" cx="434" cy="76" r="1.8"/><circle class="gp-dot" cx="434" cy="54" r="1.8"/><circle class="gp-dot" cx="434" cy="32" r="1.8"/><circle class="gp-dot" cx="434" cy="10" r="1.8"/><circle class="gp-dot" cx="456" cy="164" r="1.8"/><circle class="gp-dot" cx="456" cy="142" r="1.8"/><circle class="gp-dot" cx="456" cy="120" r="1.8"/><circle class="gp-dot" cx="456" cy="98" r="1.8"/><circle class="gp-dot" cx="456" cy="76" r="1.8"/><circle class="gp-dot" cx="456" cy="54" r="1.8"/><circle class="gp-dot" cx="456" cy="32" r="1.8"/><circle class="gp-dot" cx="456" cy="10" r="1.8"/><rect class="shp-1" x="302" y="10" width="44" height="44"/><text class="shp-num" x="324.0" y="36.0" text-anchor="middle">1</text><rect class="shp-2" x="412" y="54" width="22" height="22"/><text class="shp-num" x="423.0" y="69.0" text-anchor="middle">2</text><rect class="shp-3" x="368" y="32" width="22" height="22"/><text class="shp-num" x="379.0" y="47.0" text-anchor="middle">3</text><rect class="shp-1" x="258" y="54" width="110" height="110"/><text class="shp-num" x="313.0" y="113.0" text-anchor="middle">4</text><text class="legend" x="357.0" y="186" text-anchor="middle" direction="rtl">הגרלה 2 : 4 ריבועים</text><line class="gp-line" x1="496" x2="496" y1="10" y2="164"/><line class="gp-line" x1="518" x2="518" y1="10" y2="164"/><line class="gp-line" x1="540" x2="540" y1="10" y2="164"/><line class="gp-line" x1="562" x2="562" y1="10" y2="164"/><line class="gp-line" x1="584" x2="584" y1="10" y2="164"/><line class="gp-line" x1="606" x2="606" y1="10" y2="164"/><line class="gp-line" x1="628" x2="628" y1="10" y2="164"/><line class="gp-line" x1="650" x2="650" y1="10" y2="164"/><line class="gp-line" x1="672" x2="672" y1="10" y2="164"/><line class="gp-line" x1="694" x2="694" y1="10" y2="164"/><line class="gp-line" x1="496" x2="694" y1="164" y2="164"/><line class="gp-line" x1="496" x2="694" y1="142" y2="142"/><line class="gp-line" x1="496" x2="694" y1="120" y2="120"/><line class="gp-line" x1="496" x2="694" y1="98" y2="98"/><line class="gp-line" x1="496" x2="694" y1="76" y2="76"/><line class="gp-line" x1="496" x2="694" y1="54" y2="54"/><line class="gp-line" x1="496" x2="694" y1="32" y2="32"/><line class="gp-line" x1="496" x2="694" y1="10" y2="10"/><circle class="gp-dot" cx="496" cy="164" r="1.8"/><circle class="gp-dot" cx="496" cy="142" r="1.8"/><circle class="gp-dot" cx="496" cy="120" r="1.8"/><circle class="gp-dot" cx="496" cy="98" r="1.8"/><circle class="gp-dot" cx="496" cy="76" r="1.8"/><circle class="gp-dot" cx="496" cy="54" r="1.8"/><circle class="gp-dot" cx="496" cy="32" r="1.8"/><circle class="gp-dot" cx="496" cy="10" r="1.8"/><circle class="gp-dot" cx="518" cy="164" r="1.8"/><circle class="gp-dot" cx="518" cy="142" r="1.8"/><circle class="gp-dot" cx="518" cy="120" r="1.8"/><circle class="gp-dot" cx="518" cy="98" r="1.8"/><circle class="gp-dot" cx="518" cy="76" r="1.8"/><circle class="gp-dot" cx="518" cy="54" r="1.8"/><circle class="gp-dot" cx="518" cy="32" r="1.8"/><circle class="gp-dot" cx="518" cy="10" r="1.8"/><circle class="gp-dot" cx="540" cy="164" r="1.8"/><circle class="gp-dot" cx="540" cy="142" r="1.8"/><circle class="gp-dot" cx="540" cy="120" r="1.8"/><circle class="gp-dot" cx="540" cy="98" r="1.8"/><circle class="gp-dot" cx="540" cy="76" r="1.8"/><circle class="gp-dot" cx="540" cy="54" r="1.8"/><circle class="gp-dot" cx="540" cy="32" r="1.8"/><circle class="gp-dot" cx="540" cy="10" r="1.8"/><circle class="gp-dot" cx="562" cy="164" r="1.8"/><circle class="gp-dot" cx="562" cy="142" r="1.8"/><circle class="gp-dot" cx="562" cy="120" r="1.8"/><circle class="gp-dot" cx="562" cy="98" r="1.8"/><circle class="gp-dot" cx="562" cy="76" r="1.8"/><circle class="gp-dot" cx="562" cy="54" r="1.8"/><circle class="gp-dot" cx="562" cy="32" r="1.8"/><circle class="gp-dot" cx="562" cy="10" r="1.8"/><circle class="gp-dot" cx="584" cy="164" r="1.8"/><circle class="gp-dot" cx="584" cy="142" r="1.8"/><circle class="gp-dot" cx="584" cy="120" r="1.8"/><circle class="gp-dot" cx="584" cy="98" r="1.8"/><circle class="gp-dot" cx="584" cy="76" r="1.8"/><circle class="gp-dot" cx="584" cy="54" r="1.8"/><circle class="gp-dot" cx="584" cy="32" r="1.8"/><circle class="gp-dot" cx="584" cy="10" r="1.8"/><circle class="gp-dot" cx="606" cy="164" r="1.8"/><circle class="gp-dot" cx="606" cy="142" r="1.8"/><circle class="gp-dot" cx="606" cy="120" r="1.8"/><circle class="gp-dot" cx="606" cy="98" r="1.8"/><circle class="gp-dot" cx="606" cy="76" r="1.8"/><circle class="gp-dot" cx="606" cy="54" r="1.8"/><circle class="gp-dot" cx="606" cy="32" r="1.8"/><circle class="gp-dot" cx="606" cy="10" r="1.8"/><circle class="gp-dot" cx="628" cy="164" r="1.8"/><circle class="gp-dot" cx="628" cy="142" r="1.8"/><circle class="gp-dot" cx="628" cy="120" r="1.8"/><circle class="gp-dot" cx="628" cy="98" r="1.8"/><circle class="gp-dot" cx="628" cy="76" r="1.8"/><circle class="gp-dot" cx="628" cy="54" r="1.8"/><circle class="gp-dot" cx="628" cy="32" r="1.8"/><circle class="gp-dot" cx="628" cy="10" r="1.8"/><circle class="gp-dot" cx="650" cy="164" r="1.8"/><circle class="gp-dot" cx="650" cy="142" r="1.8"/><circle class="gp-dot" cx="650" cy="120" r="1.8"/><circle class="gp-dot" cx="650" cy="98" r="1.8"/><circle class="gp-dot" cx="650" cy="76" r="1.8"/><circle class="gp-dot" cx="650" cy="54" r="1.8"/><circle class="gp-dot" cx="650" cy="32" r="1.8"/><circle class="gp-dot" cx="650" cy="10" r="1.8"/><circle class="gp-dot" cx="672" cy="164" r="1.8"/><circle class="gp-dot" cx="672" cy="142" r="1.8"/><circle class="gp-dot" cx="672" cy="120" r="1.8"/><circle class="gp-dot" cx="672" cy="98" r="1.8"/><circle class="gp-dot" cx="672" cy="76" r="1.8"/><circle class="gp-dot" cx="672" cy="54" r="1.8"/><circle class="gp-dot" cx="672" cy="32" r="1.8"/><circle class="gp-dot" cx="672" cy="10" r="1.8"/><circle class="gp-dot" cx="694" cy="164" r="1.8"/><circle class="gp-dot" cx="694" cy="142" r="1.8"/><circle class="gp-dot" cx="694" cy="120" r="1.8"/><circle class="gp-dot" cx="694" cy="98" r="1.8"/><circle class="gp-dot" cx="694" cy="76" r="1.8"/><circle class="gp-dot" cx="694" cy="54" r="1.8"/><circle class="gp-dot" cx="694" cy="32" r="1.8"/><circle class="gp-dot" cx="694" cy="10" r="1.8"/><rect class="shp-1" x="518" y="32" width="110" height="110"/><text class="shp-num" x="573.0" y="91.0" text-anchor="middle">1</text><rect class="shp-2" x="650" y="120" width="44" height="44"/><text class="shp-num" x="672.0" y="146.0" text-anchor="middle">2</text><rect class="shp-3" x="584" y="142" width="22" height="22"/><text class="shp-num" x="595.0" y="157.0" text-anchor="middle">3</text><rect class="shp-1" x="628" y="54" width="66" height="66"/><text class="shp-num" x="661.0" y="91.0" text-anchor="middle">4</text><rect class="shp-2" x="628" y="10" width="22" height="22"/><text class="shp-num" x="639.0" y="25.0" text-anchor="middle">5</text><rect class="shp-3" x="628" y="120" width="22" height="22"/><text class="shp-num" x="639.0" y="135.0" text-anchor="middle">6</text><text class="legend" x="595.0" y="186" text-anchor="middle" direction="rtl">הגרלה 3 : 6 ריבועים</text></svg>

    !!! note "איך נבדק הקוד"
        הקוד ב-Python נבדק על אלפי הגרלות, מול בדיקה בלתי תלויה שצובעת את המשבצות שכל צורה
        מכסה ומוודאת שאף משבצת לא נצבעת פעמיים. ב-Verilator, הבודק `shapes_ok` רץ בדיוק כמו
        שהוא כתוב כאן, והמחלקות רצות **כמו שהן בדף** ב-Verilator עם ה-solver ‏z3, בכל עדכון
        של האתר : `square_set`, אותה מחלקה עם `constraint_mode(0)`, והמחלקה היורשת `rect_set`
        נותנות רק קבוצות חוקיות בכל ההגרלות, עם כל הגדלים של `n`, עם צורות צמודות, ועם
        מלבנים שאינם ריבועים בשתי הגרסאות של סעיף ב. (גרסת השחרור 5.052 של Verilator
        השאירה חלק מהצורות של המחלקה היורשת לא מוגרלות; ב-CI רצה גרסת פיתוח מאוחרת יותר
        שבה זה תוקן.)

    #### סיבוכיות { .sol-cost }

    ב-SystemVerilog מספר התנאים של `c_no_overlap` הוא \( n(n-1)/2 \), כלומר גדל כמו
    \( n^2 \), ועם 6 צורות אלה 15 תנאים שה-solver פותר יחד. ב-Python כל שלב סורק את כל
    196 הריבועים האפשריים מול הצורות שכבר נבחרו, \( O(196 \cdot n) \) לשלב, ואם נתקעים
    מתחילים מחדש; ב-grid קטן וצפוף זה עלול לקרות כמה פעמים.

---

### סעיף ב – מלבנים

הכלילו את הפתרון ל**מלבנים** באורכים שונים. עדיין אסור שמלבנים יחפפו או יחתכו זה את זה,
ומותר שיהיו צמודים.

??? tip "רמז 1"
    איזה מהתנאים של סעיף א שייך רק לריבועים? האם צריך לגעת בשאר?

??? tip "רמז 2"
    בדקו את תנאי החפיפה על שני מלבנים שיוצרים צלב : האם יש פינה של אחד בתוך השני? ובכל
    זאת, האם הם חופפים?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        רק התנאי "רוחב שווה לגובה" יוצא : מחלקה יורשת `rect_set` עם constraint **ריק באותו
        שם**, או `c_square.constraint_mode(0)` על אובייקט קיים. **תנאי החפיפה נשאר בדיוק
        כמו שהוא**, כי הוא אף פעם לא השתמש בכך שהצורות הן ריבועים.

    <!-- cost: תנאים \( n(n-1)/2 \) | מועמדים 1,260 -->

    #### הרעיון { .sol-idea }

    כל שאר התנאים של סעיף א נשארים, כולל תנאי החפיפה. ב-SystemVerilog constraint במחלקה
    יורשת עם **אותו שם** מחליף את ה-constraint של מחלקת הבסיס, וזו הדרך להסיר תנאי אחד
    בלי להעתיק את המחלקה.

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="class rect_set"
        class rect_set extends square_set;
          // Same name as in square_set, so it replaces c_square: width and height are free
          constraint c_square { }   // (1)!
        endclass
        ```

        1. גוף ריק הוא constraint חוקי שלא דורש כלום. מכיוון שהשם זהה, הוא מסתיר את
           `c_square` של `square_set`, ושאר ה-constraints עוברים בירושה כמו שהם.

        ב-SystemVerilog, constraint במחלקה יורשת עם **אותו שם** מחליף את ה-constraint של
        מחלקת הבסיס. כל שאר התנאים עוברים בירושה. דרך אחרת היא לכבות את התנאי באובייקט של
        מחלקת הבסיס, בלי מחלקה חדשה :

        ```systemverilog title="constraint_mode"
        square_set s = new();
        s.c_square.constraint_mode(0);    // now s draws rectangles
        void'(s.randomize());
        ```

    === "Python"
        ```python title="random_rectangles"
        def random_rectangles(N, M, max_shapes, rng=random):
            return random_shapes(N, M, max_shapes, squares=False, rng=rng)
        ```

        הפרמטר `squares=False` מוריד את התנאי מ-`candidates`, ועכשיו יש 1,260 מלבנים
        אפשריים במקום 196 ריבועים.

    #### למה זה נכון { .sol-proof }

    **למה תנאי החפיפה נשאר נכון, ולמה בדיקה לפי פינות לא.** פתרון נפוץ אבל שגוי לבדיקת
    חפיפה : "שני מלבנים חופפים אם יש פינה של אחד בתוך השני". בשני מלבנים שיוצרים **צלב**
    אין אף פינה בתוך המלבן השני, והם עדיין חופפים :

    <svg class="figure" viewBox="0 0 496 252" role="img" aria-label="שני מלבנים בצורת צלב חופפים בלי שאף פינה נמצאת בתוך המלבן השני, ולידם חמישה מלבנים צמודים בלי חפיפה"><line class="gp-line" x1="46" x2="46" y1="10" y2="192"/><line class="gp-line" x1="72" x2="72" y1="10" y2="192"/><line class="gp-line" x1="98" x2="98" y1="10" y2="192"/><line class="gp-line" x1="124" x2="124" y1="10" y2="192"/><line class="gp-line" x1="150" x2="150" y1="10" y2="192"/><line class="gp-line" x1="176" x2="176" y1="10" y2="192"/><line class="gp-line" x1="202" x2="202" y1="10" y2="192"/><line class="gp-line" x1="228" x2="228" y1="10" y2="192"/><line class="gp-line" x1="254" x2="254" y1="10" y2="192"/><line class="gp-line" x1="46" x2="254" y1="192" y2="192"/><line class="gp-line" x1="46" x2="254" y1="166" y2="166"/><line class="gp-line" x1="46" x2="254" y1="140" y2="140"/><line class="gp-line" x1="46" x2="254" y1="114" y2="114"/><line class="gp-line" x1="46" x2="254" y1="88" y2="88"/><line class="gp-line" x1="46" x2="254" y1="62" y2="62"/><line class="gp-line" x1="46" x2="254" y1="36" y2="36"/><line class="gp-line" x1="46" x2="254" y1="10" y2="10"/><circle class="gp-dot" cx="46" cy="192" r="1.8"/><circle class="gp-dot" cx="46" cy="166" r="1.8"/><circle class="gp-dot" cx="46" cy="140" r="1.8"/><circle class="gp-dot" cx="46" cy="114" r="1.8"/><circle class="gp-dot" cx="46" cy="88" r="1.8"/><circle class="gp-dot" cx="46" cy="62" r="1.8"/><circle class="gp-dot" cx="46" cy="36" r="1.8"/><circle class="gp-dot" cx="46" cy="10" r="1.8"/><circle class="gp-dot" cx="72" cy="192" r="1.8"/><circle class="gp-dot" cx="72" cy="166" r="1.8"/><circle class="gp-dot" cx="72" cy="140" r="1.8"/><circle class="gp-dot" cx="72" cy="114" r="1.8"/><circle class="gp-dot" cx="72" cy="88" r="1.8"/><circle class="gp-dot" cx="72" cy="62" r="1.8"/><circle class="gp-dot" cx="72" cy="36" r="1.8"/><circle class="gp-dot" cx="72" cy="10" r="1.8"/><circle class="gp-dot" cx="98" cy="192" r="1.8"/><circle class="gp-dot" cx="98" cy="166" r="1.8"/><circle class="gp-dot" cx="98" cy="140" r="1.8"/><circle class="gp-dot" cx="98" cy="114" r="1.8"/><circle class="gp-dot" cx="98" cy="88" r="1.8"/><circle class="gp-dot" cx="98" cy="62" r="1.8"/><circle class="gp-dot" cx="98" cy="36" r="1.8"/><circle class="gp-dot" cx="98" cy="10" r="1.8"/><circle class="gp-dot" cx="124" cy="192" r="1.8"/><circle class="gp-dot" cx="124" cy="166" r="1.8"/><circle class="gp-dot" cx="124" cy="140" r="1.8"/><circle class="gp-dot" cx="124" cy="114" r="1.8"/><circle class="gp-dot" cx="124" cy="88" r="1.8"/><circle class="gp-dot" cx="124" cy="62" r="1.8"/><circle class="gp-dot" cx="124" cy="36" r="1.8"/><circle class="gp-dot" cx="124" cy="10" r="1.8"/><circle class="gp-dot" cx="150" cy="192" r="1.8"/><circle class="gp-dot" cx="150" cy="166" r="1.8"/><circle class="gp-dot" cx="150" cy="140" r="1.8"/><circle class="gp-dot" cx="150" cy="114" r="1.8"/><circle class="gp-dot" cx="150" cy="88" r="1.8"/><circle class="gp-dot" cx="150" cy="62" r="1.8"/><circle class="gp-dot" cx="150" cy="36" r="1.8"/><circle class="gp-dot" cx="150" cy="10" r="1.8"/><circle class="gp-dot" cx="176" cy="192" r="1.8"/><circle class="gp-dot" cx="176" cy="166" r="1.8"/><circle class="gp-dot" cx="176" cy="140" r="1.8"/><circle class="gp-dot" cx="176" cy="114" r="1.8"/><circle class="gp-dot" cx="176" cy="88" r="1.8"/><circle class="gp-dot" cx="176" cy="62" r="1.8"/><circle class="gp-dot" cx="176" cy="36" r="1.8"/><circle class="gp-dot" cx="176" cy="10" r="1.8"/><circle class="gp-dot" cx="202" cy="192" r="1.8"/><circle class="gp-dot" cx="202" cy="166" r="1.8"/><circle class="gp-dot" cx="202" cy="140" r="1.8"/><circle class="gp-dot" cx="202" cy="114" r="1.8"/><circle class="gp-dot" cx="202" cy="88" r="1.8"/><circle class="gp-dot" cx="202" cy="62" r="1.8"/><circle class="gp-dot" cx="202" cy="36" r="1.8"/><circle class="gp-dot" cx="202" cy="10" r="1.8"/><circle class="gp-dot" cx="228" cy="192" r="1.8"/><circle class="gp-dot" cx="228" cy="166" r="1.8"/><circle class="gp-dot" cx="228" cy="140" r="1.8"/><circle class="gp-dot" cx="228" cy="114" r="1.8"/><circle class="gp-dot" cx="228" cy="88" r="1.8"/><circle class="gp-dot" cx="228" cy="62" r="1.8"/><circle class="gp-dot" cx="228" cy="36" r="1.8"/><circle class="gp-dot" cx="228" cy="10" r="1.8"/><circle class="gp-dot" cx="254" cy="192" r="1.8"/><circle class="gp-dot" cx="254" cy="166" r="1.8"/><circle class="gp-dot" cx="254" cy="140" r="1.8"/><circle class="gp-dot" cx="254" cy="114" r="1.8"/><circle class="gp-dot" cx="254" cy="88" r="1.8"/><circle class="gp-dot" cx="254" cy="62" r="1.8"/><circle class="gp-dot" cx="254" cy="36" r="1.8"/><circle class="gp-dot" cx="254" cy="10" r="1.8"/><rect class="shp-1" x="46" y="62" width="208" height="52"/><rect class="shp-2" x="124" y="10" width="52" height="182"/><rect class="shp-bad" x="124" y="62" width="52" height="52"/><circle class="s1-fill" cx="46" cy="114" r="4"/><circle class="s1-fill" cx="46" cy="62" r="4"/><circle class="s1-fill" cx="254" cy="114" r="4"/><circle class="s1-fill" cx="254" cy="62" r="4"/><circle class="s3-fill" cx="124" cy="192" r="4"/><circle class="s3-fill" cx="124" cy="10" r="4"/><circle class="s3-fill" cx="176" cy="192" r="4"/><circle class="s3-fill" cx="176" cy="10" r="4"/><rect class="s1-fill" x="46" y="202" width="208" height="6" rx="3"/><rect class="s1-fill" x="12" y="62" width="6" height="52" rx="3"/><rect class="s3-fill" x="124" y="211" width="52" height="6" rx="3"/><rect class="s3-fill" x="21" y="10" width="6" height="182" rx="3"/><text class="legend" x="150.0" y="242" text-anchor="middle" direction="rtl">✗ צלב : אין פינה בפנים, ויש חפיפה</text><line class="gp-line" x1="324" x2="324" y1="10" y2="192"/><line class="gp-line" x1="350" x2="350" y1="10" y2="192"/><line class="gp-line" x1="376" x2="376" y1="10" y2="192"/><line class="gp-line" x1="402" x2="402" y1="10" y2="192"/><line class="gp-line" x1="428" x2="428" y1="10" y2="192"/><line class="gp-line" x1="454" x2="454" y1="10" y2="192"/><line class="gp-line" x1="480" x2="480" y1="10" y2="192"/><line class="gp-line" x1="324" x2="480" y1="192" y2="192"/><line class="gp-line" x1="324" x2="480" y1="166" y2="166"/><line class="gp-line" x1="324" x2="480" y1="140" y2="140"/><line class="gp-line" x1="324" x2="480" y1="114" y2="114"/><line class="gp-line" x1="324" x2="480" y1="88" y2="88"/><line class="gp-line" x1="324" x2="480" y1="62" y2="62"/><line class="gp-line" x1="324" x2="480" y1="36" y2="36"/><line class="gp-line" x1="324" x2="480" y1="10" y2="10"/><circle class="gp-dot" cx="324" cy="192" r="1.8"/><circle class="gp-dot" cx="324" cy="166" r="1.8"/><circle class="gp-dot" cx="324" cy="140" r="1.8"/><circle class="gp-dot" cx="324" cy="114" r="1.8"/><circle class="gp-dot" cx="324" cy="88" r="1.8"/><circle class="gp-dot" cx="324" cy="62" r="1.8"/><circle class="gp-dot" cx="324" cy="36" r="1.8"/><circle class="gp-dot" cx="324" cy="10" r="1.8"/><circle class="gp-dot" cx="350" cy="192" r="1.8"/><circle class="gp-dot" cx="350" cy="166" r="1.8"/><circle class="gp-dot" cx="350" cy="140" r="1.8"/><circle class="gp-dot" cx="350" cy="114" r="1.8"/><circle class="gp-dot" cx="350" cy="88" r="1.8"/><circle class="gp-dot" cx="350" cy="62" r="1.8"/><circle class="gp-dot" cx="350" cy="36" r="1.8"/><circle class="gp-dot" cx="350" cy="10" r="1.8"/><circle class="gp-dot" cx="376" cy="192" r="1.8"/><circle class="gp-dot" cx="376" cy="166" r="1.8"/><circle class="gp-dot" cx="376" cy="140" r="1.8"/><circle class="gp-dot" cx="376" cy="114" r="1.8"/><circle class="gp-dot" cx="376" cy="88" r="1.8"/><circle class="gp-dot" cx="376" cy="62" r="1.8"/><circle class="gp-dot" cx="376" cy="36" r="1.8"/><circle class="gp-dot" cx="376" cy="10" r="1.8"/><circle class="gp-dot" cx="402" cy="192" r="1.8"/><circle class="gp-dot" cx="402" cy="166" r="1.8"/><circle class="gp-dot" cx="402" cy="140" r="1.8"/><circle class="gp-dot" cx="402" cy="114" r="1.8"/><circle class="gp-dot" cx="402" cy="88" r="1.8"/><circle class="gp-dot" cx="402" cy="62" r="1.8"/><circle class="gp-dot" cx="402" cy="36" r="1.8"/><circle class="gp-dot" cx="402" cy="10" r="1.8"/><circle class="gp-dot" cx="428" cy="192" r="1.8"/><circle class="gp-dot" cx="428" cy="166" r="1.8"/><circle class="gp-dot" cx="428" cy="140" r="1.8"/><circle class="gp-dot" cx="428" cy="114" r="1.8"/><circle class="gp-dot" cx="428" cy="88" r="1.8"/><circle class="gp-dot" cx="428" cy="62" r="1.8"/><circle class="gp-dot" cx="428" cy="36" r="1.8"/><circle class="gp-dot" cx="428" cy="10" r="1.8"/><circle class="gp-dot" cx="454" cy="192" r="1.8"/><circle class="gp-dot" cx="454" cy="166" r="1.8"/><circle class="gp-dot" cx="454" cy="140" r="1.8"/><circle class="gp-dot" cx="454" cy="114" r="1.8"/><circle class="gp-dot" cx="454" cy="88" r="1.8"/><circle class="gp-dot" cx="454" cy="62" r="1.8"/><circle class="gp-dot" cx="454" cy="36" r="1.8"/><circle class="gp-dot" cx="454" cy="10" r="1.8"/><circle class="gp-dot" cx="480" cy="192" r="1.8"/><circle class="gp-dot" cx="480" cy="166" r="1.8"/><circle class="gp-dot" cx="480" cy="140" r="1.8"/><circle class="gp-dot" cx="480" cy="114" r="1.8"/><circle class="gp-dot" cx="480" cy="88" r="1.8"/><circle class="gp-dot" cx="480" cy="62" r="1.8"/><circle class="gp-dot" cx="480" cy="36" r="1.8"/><circle class="gp-dot" cx="480" cy="10" r="1.8"/><rect class="shp-1" x="324" y="140" width="78" height="52"/><text class="shp-num" x="363.0" y="170.0" text-anchor="middle">1</text><rect class="shp-2" x="402" y="62" width="78" height="130"/><text class="shp-num" x="441.0" y="131.0" text-anchor="middle">2</text><rect class="shp-3" x="324" y="10" width="52" height="130"/><text class="shp-num" x="350.0" y="79.0" text-anchor="middle">3</text><rect class="shp-1" x="376" y="10" width="104" height="52"/><text class="shp-num" x="428.0" y="40.0" text-anchor="middle">4</text><rect class="shp-2" x="376" y="62" width="26" height="78"/><text class="shp-num" x="389.0" y="105.0" text-anchor="middle">5</text><text class="legend" x="402.0" y="242" text-anchor="middle" direction="rtl">✓ מלבנים צמודים</text></svg>

    הפסים משמאל ומתחת ל-grid הם ההיטלים של שני המלבנים על הצירים. הנקודות הן הפינות,
    ואף אחת מהן לא נמצאת בתוך המלבן השני.

    התנאי עם ארבעת האזורים לא נופל במלכודת הזו : הוא בודק את ההיטלים על שני הצירים.
    בצלב ההיטלים חופפים גם על ציר \( x \) וגם על ציר \( y \), ולכן המלבנים חופפים.

    בשני ריבועים צלב לא יכול לקרות : הוא דורש שאחד יהיה רחב יותר מהשני והשני גבוה יותר
    מהראשון, וריבוע רחב יותר הוא גם גבוה יותר. לכן בסעיף א בדיקה לפי פינות במקרה עובדת,
    אבל רק התנאי על הצירים נכון לשני הסעיפים.

    **דוגמאות להגרלות.**

    <svg class="figure" viewBox="0 0 714 198" role="img" aria-label="שלוש הגרלות של מלבנים בלי חפיפה"><line class="gp-line" x1="20" x2="20" y1="10" y2="164"/><line class="gp-line" x1="42" x2="42" y1="10" y2="164"/><line class="gp-line" x1="64" x2="64" y1="10" y2="164"/><line class="gp-line" x1="86" x2="86" y1="10" y2="164"/><line class="gp-line" x1="108" x2="108" y1="10" y2="164"/><line class="gp-line" x1="130" x2="130" y1="10" y2="164"/><line class="gp-line" x1="152" x2="152" y1="10" y2="164"/><line class="gp-line" x1="174" x2="174" y1="10" y2="164"/><line class="gp-line" x1="196" x2="196" y1="10" y2="164"/><line class="gp-line" x1="218" x2="218" y1="10" y2="164"/><line class="gp-line" x1="20" x2="218" y1="164" y2="164"/><line class="gp-line" x1="20" x2="218" y1="142" y2="142"/><line class="gp-line" x1="20" x2="218" y1="120" y2="120"/><line class="gp-line" x1="20" x2="218" y1="98" y2="98"/><line class="gp-line" x1="20" x2="218" y1="76" y2="76"/><line class="gp-line" x1="20" x2="218" y1="54" y2="54"/><line class="gp-line" x1="20" x2="218" y1="32" y2="32"/><line class="gp-line" x1="20" x2="218" y1="10" y2="10"/><circle class="gp-dot" cx="20" cy="164" r="1.8"/><circle class="gp-dot" cx="20" cy="142" r="1.8"/><circle class="gp-dot" cx="20" cy="120" r="1.8"/><circle class="gp-dot" cx="20" cy="98" r="1.8"/><circle class="gp-dot" cx="20" cy="76" r="1.8"/><circle class="gp-dot" cx="20" cy="54" r="1.8"/><circle class="gp-dot" cx="20" cy="32" r="1.8"/><circle class="gp-dot" cx="20" cy="10" r="1.8"/><circle class="gp-dot" cx="42" cy="164" r="1.8"/><circle class="gp-dot" cx="42" cy="142" r="1.8"/><circle class="gp-dot" cx="42" cy="120" r="1.8"/><circle class="gp-dot" cx="42" cy="98" r="1.8"/><circle class="gp-dot" cx="42" cy="76" r="1.8"/><circle class="gp-dot" cx="42" cy="54" r="1.8"/><circle class="gp-dot" cx="42" cy="32" r="1.8"/><circle class="gp-dot" cx="42" cy="10" r="1.8"/><circle class="gp-dot" cx="64" cy="164" r="1.8"/><circle class="gp-dot" cx="64" cy="142" r="1.8"/><circle class="gp-dot" cx="64" cy="120" r="1.8"/><circle class="gp-dot" cx="64" cy="98" r="1.8"/><circle class="gp-dot" cx="64" cy="76" r="1.8"/><circle class="gp-dot" cx="64" cy="54" r="1.8"/><circle class="gp-dot" cx="64" cy="32" r="1.8"/><circle class="gp-dot" cx="64" cy="10" r="1.8"/><circle class="gp-dot" cx="86" cy="164" r="1.8"/><circle class="gp-dot" cx="86" cy="142" r="1.8"/><circle class="gp-dot" cx="86" cy="120" r="1.8"/><circle class="gp-dot" cx="86" cy="98" r="1.8"/><circle class="gp-dot" cx="86" cy="76" r="1.8"/><circle class="gp-dot" cx="86" cy="54" r="1.8"/><circle class="gp-dot" cx="86" cy="32" r="1.8"/><circle class="gp-dot" cx="86" cy="10" r="1.8"/><circle class="gp-dot" cx="108" cy="164" r="1.8"/><circle class="gp-dot" cx="108" cy="142" r="1.8"/><circle class="gp-dot" cx="108" cy="120" r="1.8"/><circle class="gp-dot" cx="108" cy="98" r="1.8"/><circle class="gp-dot" cx="108" cy="76" r="1.8"/><circle class="gp-dot" cx="108" cy="54" r="1.8"/><circle class="gp-dot" cx="108" cy="32" r="1.8"/><circle class="gp-dot" cx="108" cy="10" r="1.8"/><circle class="gp-dot" cx="130" cy="164" r="1.8"/><circle class="gp-dot" cx="130" cy="142" r="1.8"/><circle class="gp-dot" cx="130" cy="120" r="1.8"/><circle class="gp-dot" cx="130" cy="98" r="1.8"/><circle class="gp-dot" cx="130" cy="76" r="1.8"/><circle class="gp-dot" cx="130" cy="54" r="1.8"/><circle class="gp-dot" cx="130" cy="32" r="1.8"/><circle class="gp-dot" cx="130" cy="10" r="1.8"/><circle class="gp-dot" cx="152" cy="164" r="1.8"/><circle class="gp-dot" cx="152" cy="142" r="1.8"/><circle class="gp-dot" cx="152" cy="120" r="1.8"/><circle class="gp-dot" cx="152" cy="98" r="1.8"/><circle class="gp-dot" cx="152" cy="76" r="1.8"/><circle class="gp-dot" cx="152" cy="54" r="1.8"/><circle class="gp-dot" cx="152" cy="32" r="1.8"/><circle class="gp-dot" cx="152" cy="10" r="1.8"/><circle class="gp-dot" cx="174" cy="164" r="1.8"/><circle class="gp-dot" cx="174" cy="142" r="1.8"/><circle class="gp-dot" cx="174" cy="120" r="1.8"/><circle class="gp-dot" cx="174" cy="98" r="1.8"/><circle class="gp-dot" cx="174" cy="76" r="1.8"/><circle class="gp-dot" cx="174" cy="54" r="1.8"/><circle class="gp-dot" cx="174" cy="32" r="1.8"/><circle class="gp-dot" cx="174" cy="10" r="1.8"/><circle class="gp-dot" cx="196" cy="164" r="1.8"/><circle class="gp-dot" cx="196" cy="142" r="1.8"/><circle class="gp-dot" cx="196" cy="120" r="1.8"/><circle class="gp-dot" cx="196" cy="98" r="1.8"/><circle class="gp-dot" cx="196" cy="76" r="1.8"/><circle class="gp-dot" cx="196" cy="54" r="1.8"/><circle class="gp-dot" cx="196" cy="32" r="1.8"/><circle class="gp-dot" cx="196" cy="10" r="1.8"/><circle class="gp-dot" cx="218" cy="164" r="1.8"/><circle class="gp-dot" cx="218" cy="142" r="1.8"/><circle class="gp-dot" cx="218" cy="120" r="1.8"/><circle class="gp-dot" cx="218" cy="98" r="1.8"/><circle class="gp-dot" cx="218" cy="76" r="1.8"/><circle class="gp-dot" cx="218" cy="54" r="1.8"/><circle class="gp-dot" cx="218" cy="32" r="1.8"/><circle class="gp-dot" cx="218" cy="10" r="1.8"/><rect class="shp-1" x="108" y="98" width="110" height="44"/><text class="shp-num" x="163.0" y="124.0" text-anchor="middle">1</text><rect class="shp-2" x="86" y="32" width="132" height="66"/><text class="shp-num" x="152.0" y="69.0" text-anchor="middle">2</text><rect class="shp-3" x="42" y="32" width="44" height="88"/><text class="shp-num" x="64.0" y="80.0" text-anchor="middle">3</text><text class="legend" x="119.0" y="186" text-anchor="middle" direction="rtl">הגרלה 1 : 3 מלבנים</text><line class="gp-line" x1="258" x2="258" y1="10" y2="164"/><line class="gp-line" x1="280" x2="280" y1="10" y2="164"/><line class="gp-line" x1="302" x2="302" y1="10" y2="164"/><line class="gp-line" x1="324" x2="324" y1="10" y2="164"/><line class="gp-line" x1="346" x2="346" y1="10" y2="164"/><line class="gp-line" x1="368" x2="368" y1="10" y2="164"/><line class="gp-line" x1="390" x2="390" y1="10" y2="164"/><line class="gp-line" x1="412" x2="412" y1="10" y2="164"/><line class="gp-line" x1="434" x2="434" y1="10" y2="164"/><line class="gp-line" x1="456" x2="456" y1="10" y2="164"/><line class="gp-line" x1="258" x2="456" y1="164" y2="164"/><line class="gp-line" x1="258" x2="456" y1="142" y2="142"/><line class="gp-line" x1="258" x2="456" y1="120" y2="120"/><line class="gp-line" x1="258" x2="456" y1="98" y2="98"/><line class="gp-line" x1="258" x2="456" y1="76" y2="76"/><line class="gp-line" x1="258" x2="456" y1="54" y2="54"/><line class="gp-line" x1="258" x2="456" y1="32" y2="32"/><line class="gp-line" x1="258" x2="456" y1="10" y2="10"/><circle class="gp-dot" cx="258" cy="164" r="1.8"/><circle class="gp-dot" cx="258" cy="142" r="1.8"/><circle class="gp-dot" cx="258" cy="120" r="1.8"/><circle class="gp-dot" cx="258" cy="98" r="1.8"/><circle class="gp-dot" cx="258" cy="76" r="1.8"/><circle class="gp-dot" cx="258" cy="54" r="1.8"/><circle class="gp-dot" cx="258" cy="32" r="1.8"/><circle class="gp-dot" cx="258" cy="10" r="1.8"/><circle class="gp-dot" cx="280" cy="164" r="1.8"/><circle class="gp-dot" cx="280" cy="142" r="1.8"/><circle class="gp-dot" cx="280" cy="120" r="1.8"/><circle class="gp-dot" cx="280" cy="98" r="1.8"/><circle class="gp-dot" cx="280" cy="76" r="1.8"/><circle class="gp-dot" cx="280" cy="54" r="1.8"/><circle class="gp-dot" cx="280" cy="32" r="1.8"/><circle class="gp-dot" cx="280" cy="10" r="1.8"/><circle class="gp-dot" cx="302" cy="164" r="1.8"/><circle class="gp-dot" cx="302" cy="142" r="1.8"/><circle class="gp-dot" cx="302" cy="120" r="1.8"/><circle class="gp-dot" cx="302" cy="98" r="1.8"/><circle class="gp-dot" cx="302" cy="76" r="1.8"/><circle class="gp-dot" cx="302" cy="54" r="1.8"/><circle class="gp-dot" cx="302" cy="32" r="1.8"/><circle class="gp-dot" cx="302" cy="10" r="1.8"/><circle class="gp-dot" cx="324" cy="164" r="1.8"/><circle class="gp-dot" cx="324" cy="142" r="1.8"/><circle class="gp-dot" cx="324" cy="120" r="1.8"/><circle class="gp-dot" cx="324" cy="98" r="1.8"/><circle class="gp-dot" cx="324" cy="76" r="1.8"/><circle class="gp-dot" cx="324" cy="54" r="1.8"/><circle class="gp-dot" cx="324" cy="32" r="1.8"/><circle class="gp-dot" cx="324" cy="10" r="1.8"/><circle class="gp-dot" cx="346" cy="164" r="1.8"/><circle class="gp-dot" cx="346" cy="142" r="1.8"/><circle class="gp-dot" cx="346" cy="120" r="1.8"/><circle class="gp-dot" cx="346" cy="98" r="1.8"/><circle class="gp-dot" cx="346" cy="76" r="1.8"/><circle class="gp-dot" cx="346" cy="54" r="1.8"/><circle class="gp-dot" cx="346" cy="32" r="1.8"/><circle class="gp-dot" cx="346" cy="10" r="1.8"/><circle class="gp-dot" cx="368" cy="164" r="1.8"/><circle class="gp-dot" cx="368" cy="142" r="1.8"/><circle class="gp-dot" cx="368" cy="120" r="1.8"/><circle class="gp-dot" cx="368" cy="98" r="1.8"/><circle class="gp-dot" cx="368" cy="76" r="1.8"/><circle class="gp-dot" cx="368" cy="54" r="1.8"/><circle class="gp-dot" cx="368" cy="32" r="1.8"/><circle class="gp-dot" cx="368" cy="10" r="1.8"/><circle class="gp-dot" cx="390" cy="164" r="1.8"/><circle class="gp-dot" cx="390" cy="142" r="1.8"/><circle class="gp-dot" cx="390" cy="120" r="1.8"/><circle class="gp-dot" cx="390" cy="98" r="1.8"/><circle class="gp-dot" cx="390" cy="76" r="1.8"/><circle class="gp-dot" cx="390" cy="54" r="1.8"/><circle class="gp-dot" cx="390" cy="32" r="1.8"/><circle class="gp-dot" cx="390" cy="10" r="1.8"/><circle class="gp-dot" cx="412" cy="164" r="1.8"/><circle class="gp-dot" cx="412" cy="142" r="1.8"/><circle class="gp-dot" cx="412" cy="120" r="1.8"/><circle class="gp-dot" cx="412" cy="98" r="1.8"/><circle class="gp-dot" cx="412" cy="76" r="1.8"/><circle class="gp-dot" cx="412" cy="54" r="1.8"/><circle class="gp-dot" cx="412" cy="32" r="1.8"/><circle class="gp-dot" cx="412" cy="10" r="1.8"/><circle class="gp-dot" cx="434" cy="164" r="1.8"/><circle class="gp-dot" cx="434" cy="142" r="1.8"/><circle class="gp-dot" cx="434" cy="120" r="1.8"/><circle class="gp-dot" cx="434" cy="98" r="1.8"/><circle class="gp-dot" cx="434" cy="76" r="1.8"/><circle class="gp-dot" cx="434" cy="54" r="1.8"/><circle class="gp-dot" cx="434" cy="32" r="1.8"/><circle class="gp-dot" cx="434" cy="10" r="1.8"/><circle class="gp-dot" cx="456" cy="164" r="1.8"/><circle class="gp-dot" cx="456" cy="142" r="1.8"/><circle class="gp-dot" cx="456" cy="120" r="1.8"/><circle class="gp-dot" cx="456" cy="98" r="1.8"/><circle class="gp-dot" cx="456" cy="76" r="1.8"/><circle class="gp-dot" cx="456" cy="54" r="1.8"/><circle class="gp-dot" cx="456" cy="32" r="1.8"/><circle class="gp-dot" cx="456" cy="10" r="1.8"/><rect class="shp-1" x="390" y="10" width="44" height="44"/><text class="shp-num" x="412.0" y="36.0" text-anchor="middle">1</text><rect class="shp-2" x="390" y="54" width="44" height="110"/><text class="shp-num" x="412.0" y="113.0" text-anchor="middle">2</text><rect class="shp-3" x="324" y="142" width="66" height="22"/><text class="shp-num" x="357.0" y="157.0" text-anchor="middle">3</text><rect class="shp-1" x="280" y="76" width="88" height="44"/><text class="shp-num" x="324.0" y="102.0" text-anchor="middle">4</text><text class="legend" x="357.0" y="186" text-anchor="middle" direction="rtl">הגרלה 2 : 4 מלבנים</text><line class="gp-line" x1="496" x2="496" y1="10" y2="164"/><line class="gp-line" x1="518" x2="518" y1="10" y2="164"/><line class="gp-line" x1="540" x2="540" y1="10" y2="164"/><line class="gp-line" x1="562" x2="562" y1="10" y2="164"/><line class="gp-line" x1="584" x2="584" y1="10" y2="164"/><line class="gp-line" x1="606" x2="606" y1="10" y2="164"/><line class="gp-line" x1="628" x2="628" y1="10" y2="164"/><line class="gp-line" x1="650" x2="650" y1="10" y2="164"/><line class="gp-line" x1="672" x2="672" y1="10" y2="164"/><line class="gp-line" x1="694" x2="694" y1="10" y2="164"/><line class="gp-line" x1="496" x2="694" y1="164" y2="164"/><line class="gp-line" x1="496" x2="694" y1="142" y2="142"/><line class="gp-line" x1="496" x2="694" y1="120" y2="120"/><line class="gp-line" x1="496" x2="694" y1="98" y2="98"/><line class="gp-line" x1="496" x2="694" y1="76" y2="76"/><line class="gp-line" x1="496" x2="694" y1="54" y2="54"/><line class="gp-line" x1="496" x2="694" y1="32" y2="32"/><line class="gp-line" x1="496" x2="694" y1="10" y2="10"/><circle class="gp-dot" cx="496" cy="164" r="1.8"/><circle class="gp-dot" cx="496" cy="142" r="1.8"/><circle class="gp-dot" cx="496" cy="120" r="1.8"/><circle class="gp-dot" cx="496" cy="98" r="1.8"/><circle class="gp-dot" cx="496" cy="76" r="1.8"/><circle class="gp-dot" cx="496" cy="54" r="1.8"/><circle class="gp-dot" cx="496" cy="32" r="1.8"/><circle class="gp-dot" cx="496" cy="10" r="1.8"/><circle class="gp-dot" cx="518" cy="164" r="1.8"/><circle class="gp-dot" cx="518" cy="142" r="1.8"/><circle class="gp-dot" cx="518" cy="120" r="1.8"/><circle class="gp-dot" cx="518" cy="98" r="1.8"/><circle class="gp-dot" cx="518" cy="76" r="1.8"/><circle class="gp-dot" cx="518" cy="54" r="1.8"/><circle class="gp-dot" cx="518" cy="32" r="1.8"/><circle class="gp-dot" cx="518" cy="10" r="1.8"/><circle class="gp-dot" cx="540" cy="164" r="1.8"/><circle class="gp-dot" cx="540" cy="142" r="1.8"/><circle class="gp-dot" cx="540" cy="120" r="1.8"/><circle class="gp-dot" cx="540" cy="98" r="1.8"/><circle class="gp-dot" cx="540" cy="76" r="1.8"/><circle class="gp-dot" cx="540" cy="54" r="1.8"/><circle class="gp-dot" cx="540" cy="32" r="1.8"/><circle class="gp-dot" cx="540" cy="10" r="1.8"/><circle class="gp-dot" cx="562" cy="164" r="1.8"/><circle class="gp-dot" cx="562" cy="142" r="1.8"/><circle class="gp-dot" cx="562" cy="120" r="1.8"/><circle class="gp-dot" cx="562" cy="98" r="1.8"/><circle class="gp-dot" cx="562" cy="76" r="1.8"/><circle class="gp-dot" cx="562" cy="54" r="1.8"/><circle class="gp-dot" cx="562" cy="32" r="1.8"/><circle class="gp-dot" cx="562" cy="10" r="1.8"/><circle class="gp-dot" cx="584" cy="164" r="1.8"/><circle class="gp-dot" cx="584" cy="142" r="1.8"/><circle class="gp-dot" cx="584" cy="120" r="1.8"/><circle class="gp-dot" cx="584" cy="98" r="1.8"/><circle class="gp-dot" cx="584" cy="76" r="1.8"/><circle class="gp-dot" cx="584" cy="54" r="1.8"/><circle class="gp-dot" cx="584" cy="32" r="1.8"/><circle class="gp-dot" cx="584" cy="10" r="1.8"/><circle class="gp-dot" cx="606" cy="164" r="1.8"/><circle class="gp-dot" cx="606" cy="142" r="1.8"/><circle class="gp-dot" cx="606" cy="120" r="1.8"/><circle class="gp-dot" cx="606" cy="98" r="1.8"/><circle class="gp-dot" cx="606" cy="76" r="1.8"/><circle class="gp-dot" cx="606" cy="54" r="1.8"/><circle class="gp-dot" cx="606" cy="32" r="1.8"/><circle class="gp-dot" cx="606" cy="10" r="1.8"/><circle class="gp-dot" cx="628" cy="164" r="1.8"/><circle class="gp-dot" cx="628" cy="142" r="1.8"/><circle class="gp-dot" cx="628" cy="120" r="1.8"/><circle class="gp-dot" cx="628" cy="98" r="1.8"/><circle class="gp-dot" cx="628" cy="76" r="1.8"/><circle class="gp-dot" cx="628" cy="54" r="1.8"/><circle class="gp-dot" cx="628" cy="32" r="1.8"/><circle class="gp-dot" cx="628" cy="10" r="1.8"/><circle class="gp-dot" cx="650" cy="164" r="1.8"/><circle class="gp-dot" cx="650" cy="142" r="1.8"/><circle class="gp-dot" cx="650" cy="120" r="1.8"/><circle class="gp-dot" cx="650" cy="98" r="1.8"/><circle class="gp-dot" cx="650" cy="76" r="1.8"/><circle class="gp-dot" cx="650" cy="54" r="1.8"/><circle class="gp-dot" cx="650" cy="32" r="1.8"/><circle class="gp-dot" cx="650" cy="10" r="1.8"/><circle class="gp-dot" cx="672" cy="164" r="1.8"/><circle class="gp-dot" cx="672" cy="142" r="1.8"/><circle class="gp-dot" cx="672" cy="120" r="1.8"/><circle class="gp-dot" cx="672" cy="98" r="1.8"/><circle class="gp-dot" cx="672" cy="76" r="1.8"/><circle class="gp-dot" cx="672" cy="54" r="1.8"/><circle class="gp-dot" cx="672" cy="32" r="1.8"/><circle class="gp-dot" cx="672" cy="10" r="1.8"/><circle class="gp-dot" cx="694" cy="164" r="1.8"/><circle class="gp-dot" cx="694" cy="142" r="1.8"/><circle class="gp-dot" cx="694" cy="120" r="1.8"/><circle class="gp-dot" cx="694" cy="98" r="1.8"/><circle class="gp-dot" cx="694" cy="76" r="1.8"/><circle class="gp-dot" cx="694" cy="54" r="1.8"/><circle class="gp-dot" cx="694" cy="32" r="1.8"/><circle class="gp-dot" cx="694" cy="10" r="1.8"/><rect class="shp-1" x="496" y="54" width="88" height="110"/><text class="shp-num" x="540.0" y="113.0" text-anchor="middle">1</text><rect class="shp-2" x="628" y="76" width="66" height="88"/><text class="shp-num" x="661.0" y="124.0" text-anchor="middle">2</text><rect class="shp-3" x="650" y="32" width="22" height="44"/><text class="shp-num" x="661.0" y="58.0" text-anchor="middle">3</text><rect class="shp-1" x="584" y="32" width="66" height="22"/><text class="shp-num" x="617.0" y="47.0" text-anchor="middle">4</text><rect class="shp-2" x="496" y="10" width="176" height="22"/><text class="shp-num" x="584.0" y="25.0" text-anchor="middle">5</text><rect class="shp-3" x="584" y="142" width="44" height="22"/><text class="shp-num" x="606.0" y="157.0" text-anchor="middle">6</text><text class="legend" x="595.0" y="186" text-anchor="middle" direction="rtl">הגרלה 3 : 6 מלבנים</text></svg>

    #### סיבוכיות { .sol-cost }

    אותה סיבוכיות כמו בסעיף א : \( n(n-1)/2 \) תנאי זוגות ב-SystemVerilog. ב-Python מרחב
    המועמדים גדל מ-196 ל-1,260 צורות, ולכן כל שלב סורק פי 6 יותר, אבל עם 6 צורות לכל
    היותר זה עדיין מיידי.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : < במקום ≤"
    עם \( < \) בארבעת המקרים צורות צמודות נחשבות חופפות, וצלע משותפת או פינה משותפת
    נפסלות בניגוד לדרישה. הסימן \( \le \) בתנאי ה-"או" (ובהתאם \( < \) חזק בצורת ה-"וגם"
    של הבודק) הוא ההבדל בין "צמוד" ל"חופף".

??? trap "מלכודת : לשכוח את i < j"
    בלי `i < j` בלולאה הכפולה כל צורה נבדקת גם מול עצמה, ושם אף אחד מארבעת המקרים לא
    מתקיים. התוצאה היא `randomize()` שנכשל **תמיד**, ומי שלא בודק את ערך ההחזרה שלו מקבל
    מערכים לא מאותחלים בלי שום הודעה.

??? trap "מלכודת : בדיקה לפי פינות"
    "שני מלבנים חופפים אם יש פינה של אחד בתוך השני" נכון לריבועים ולא למלבנים : בצלב אין
    אף פינה בתוך המלבן השני, והם חופפים. הבדיקה הנכונה היא על ההיטלים בשני הצירים, כמו
    בתרשים של סעיף ב.

??? followup "שאלות המשך"
    - **מרווח בין צורות :** כל שתי צורות חייבות להיות במרחק של לפחות \( G \). מה משנים
      ב-constraint?

        ??? fu-answer "תשובה"
            מוסיפים \( G \) לכל אחד מארבעת המקרים, למשל \( x_2[j] + G \le x_1[i] \). עם \( G = 1 \)
            צורות כבר לא יכולות להיות צמודות.

    - **כמה שטח מכוסה :** דרשו שהצורות יכסו לפחות חצי מה-grid. מה צריך להוסיף?

        ??? fu-answer "תשובה"
            צריך את השטח של כל צורה ואת הסכום שלהם, למשל מערך rand עם
            `area[i] == (x2[i] - x1[i]) * (y2[i] - y1[i])` ו-`2 * area.sum() >= (N - 1) * (M - 1)`
            (או `sum() with`). אין חפיפה, ולכן סכום השטחים הוא בדיוק השטח המכוסה.

    - **התפלגות :** האם כל הקבוצות החוקיות יוצאות באותה הסתברות?

        ??? fu-answer "תשובה"
            לא בהכרח. ה-solver מנסה להגריל באחידות על כל הפתרונות, אבל הבנייה צעד אחרי צעד
            ב-Python לא אחידה : ריבוע ענק שנבחר ראשון משאיר מעט מקום לאחרים, ולכן קבוצה עם
            צורה גדולה יוצאת בהסתברות גבוהה יותר מקבוצה של צורות קטנות.

    - **הרבה צורות :** מה קורה ל-solver כשמבקשים הרבה צורות?

        ??? fu-answer "תשובה"
            מספר התנאים גדל כמו \( n^2 \), וה-solver נהיה איטי. חלופה : מחזיקים מפה של משבצות
            תפוסות וממקמים צורה אחרי צורה, כמו בפתרון ב-Python.

    - **שלושה ממדים :** קופסאות במקום מלבנים. מה קורה לתנאי של אי החפיפה?

        ??? fu-answer "תשובה"
            התנאי נשאר אותו רעיון עם שישה מקרים, שניים לכל ציר : \( j \) משמאל, מימין, מתחת,
            מעל, לפני או אחרי \( i \), מחוברים ב-"או".
