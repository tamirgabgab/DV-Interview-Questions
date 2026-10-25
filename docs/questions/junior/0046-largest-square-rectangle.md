---
id: 46
title: הריבוע, המלבן והמשולש הגדולים ביותר של אחדות
level: junior
difficulty: medium
kind: code
tags: [algorithms, dynamic-programming, stack, python, systemverilog]
source: "שתי בעיות קלאסיות : תכנון דינמי לריבוע, והיסטוגרמה עם מחסנית למלבן. סעיף ג (המשולש) הוא תוספת של בעל האתר"
added: 2026-10-24
---

## השאלה

נתון מערך דו-ממדי `grid` בגודל \( m \times n \), שכל תא בו הוא `0` או `1`.

- **סעיף א :** מצא את **הריבוע** הגדול ביותר שכל התאים בו הם `1`.
- **סעיף ב :** מצא את **המלבן** בעל השטח הגדול ביותר שכל התאים בו הם `1`.
- **סעיף ג :** מצא את **המשולש ישר הזווית** בעל השטח הגדול ביותר שכל התאים בו הם `1`,
  כאשר שני הניצבים שווים באורכם ומקבילים לצירים : אחד לאורך עמודה ואחד לאורך שורה.

בסעיפים א ו-ב יש להחזיר את השטח ואת שתי הפינות שמגדירות את הצורה, ובסעיף ג את השטח
ואת שלושת הקודקודים :

=== "SystemVerilog"
    ```systemverilog title="shape_t"
    // The answer: the area, the top-left corner (r1, c1) and the bottom-right corner (r2, c2),
    // indices from 0; area 0 and every corner -1 when the grid has no 1.
    typedef struct { int area, r1, c1, r2, c2; } shape_t;

    // Part c: the area (the number of cells), the right angle (r0, c0), the end of the
    // leg along the column (r1, c1) and the end of the leg along the row (r2, c2);
    // area 0 and every vertex -1 when the grid has no 1.
    typedef struct { int area, r0, c0, r1, c1, r2, c2; } tri_t;

    // function automatic shape_t largest_square(bit grid[][]);      // to write
    // function automatic shape_t largest_rectangle(bit grid[][]);   // to write
    // function automatic tri_t largest_triangle(bit grid[][]);      // to write
    ```

=== "Python"
    ```python title="largest_square, largest_rectangle, largest_triangle"
    def largest_square(grid: list[list[int]]) -> tuple[int, tuple[int, int], tuple[int, int]]: ...
    def largest_rectangle(grid: list[list[int]]) -> tuple[int, tuple[int, int], tuple[int, int]]: ...
    def largest_triangle(grid: list[list[int]]) -> tuple[int, tuple[int, int], tuple[int, int], tuple[int, int]]: ...
    ```

הפלט הוא `(area, top_left, bottom_right)`, כאשר כל פינה היא `(row, col)` והאינדקסים
מתחילים מ-0. אם אין במערך אף `1`, מחזירים `(0, None, None)`. אם יש כמה תשובות באותו
שטח, מותר להחזיר כל אחת מהן. השטח נגזר מהפינות :

\[
\text{area} = (r_2 - r_1 + 1)\cdot(c_2 - c_1 + 1)
\]

בסעיף ג הפלט הוא `(area, corner, leg_col, leg_row)` : התא של הזווית הישרה, הקצה של
הניצב שלאורך העמודה והקצה של הניצב שלאורך השורה. הזווית הישרה יכולה להיות בכל אחד
מארבעת הכיוונים, והשטח הוא מספר התאים. למשל, שני המשולשים האלה הם בניצב 3 ובשטח 6 :

```text
1 0 0      0 0 1
1 1 0      0 1 1
1 1 1      1 1 1
```

התשובה לשמאלי היא `(6, (2, 0), (0, 0), (2, 2))`, ולימני `(6, (2, 2), (0, 2), (2, 0))`.
הצורה הזו, לעומת זאת, **אינה** משולש כזה, כי שתי הצלעות המשופעות שלה לא מקבילות לצירים :

```text
0 1 0
1 1 1
```

המשולש הגדול בה הוא בניצב 2 ובשטח 3, למשל `(3, (1, 1), (0, 1), (1, 0))`. בלי אף `1`
מחזירים `(0, None, None, None)`.

**דרישה :** פתרון בזמן \( O(m \cdot n) \) בכל הסעיפים.

??? interviewer "מה המראיין בודק"
    - **הגדרת תת-בעיה :** בסעיף א, לראות שכל ריבוע נגמר באיזשהו תא, ולהגדיר את התשובה
      לפי הפינה הימנית-התחתונה. מכאן נוסחת המעבר קצרה.
    - **רדוקציה :** בסעיף ב, לזהות שנוסחת הריבוע לא עובדת, ולהפוך כל שורה להיסטוגרמה.
      את "המלבן הגדול בהיסטוגרמה" כדאי לשאול קודם כבעיה עצמאית.
    - **פתרונות ביניים :** בסעיף ב, פתרון של \( O(m^2 \cdot n) \) (לבחור זוג שורות
      ולחפש רצף עמודות) מראה הבנה טובה. \( O(m \cdot n) \) עם מחסנית הוא הפתרון המלא.
    - **הבנה ולא זיכרון :** סעיף ג בודק אם המועמד מבין למה נוסחת סעיף א נכונה. במשולש
      מספיקים שני שכנים, וכל מה שנשאר הוא לטפל בארבעת הכיוונים בלי לשכפל את הקוד ארבע
      פעמים.
    - **רמה :** סעיף א מתאים לכל ראיון לג'וניור. סעיף ב קשה יותר, ומותר לתת בו את הרמז של
      ההיסטוגרמה. סעיף ג קצר אחרי סעיף א.

    ??? example "כלי בדיקה : השוואה לחיפוש מלא"
        הבודק מגריל 2,000 מערכים בגודל עד \( 7 \times 7 \), משווה את השטח לחיפוש מלא על
        כל המלבנים (בסעיף ג : על כל המשולשים), ובודק שהפינות או הקודקודים מגדירים צורה
        של אחדות בשטח הזה (ריבוע בסעיף א) :

        <!-- Fenced as py, not python: the run panel and load_python load the python blocks
        in page order, and the tester calls the solvers before the solutions define them.
        The page's test runs this block after the solutions. -->

        ```py title="brute, check"
        import random

        def brute(grid, square):
            m, n = len(grid), len(grid[0])
            best = 0
            for r1 in range(m):
                for r2 in range(r1, m):
                    for c1 in range(n):
                        for c2 in range(c1, n):
                            if square and r2 - r1 != c2 - c1:
                                continue
                            if all(grid[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)):
                                best = max(best, (r2 - r1 + 1) * (c2 - c1 + 1))
            return best


        def check(solver, square, trials=2000):
            for _ in range(trials):
                m, n = random.randint(1, 7), random.randint(1, 7)
                grid = [[int(random.random() < 0.7) for _ in range(n)] for _ in range(m)]
                area, tl, br = solver(grid)
                assert area == brute(grid, square)
                if area:
                    (r1, c1), (r2, c2) = tl, br
                    assert (r2 - r1 + 1) * (c2 - c1 + 1) == area
                    assert not square or r2 - r1 == c2 - c1
                    assert all(grid[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1))


        check(largest_square, square=True)
        check(largest_rectangle, square=False)


        def triangle(corner, k, dv, dh):
            r, c = corner                       # the legs go dv rows and dh columns away
            return [(r + dv * a, c + dh * b) for a in range(k) for b in range(k - a)]


        def brute_triangle(grid):
            m, n = len(grid), len(grid[0])
            best = 0
            for r in range(m):
                for c in range(n):
                    for dv in (-1, 1):
                        for dh in (-1, 1):
                            for k in range(1, min(m, n) + 1):
                                cells = triangle((r, c), k, dv, dh)
                                if all(0 <= a < m and 0 <= b < n and grid[a][b] for a, b in cells):
                                    best = max(best, k * (k + 1) // 2)
            return best


        for _ in range(2000):
            m, n = random.randint(1, 7), random.randint(1, 7)
            grid = [[int(random.random() < 0.7) for _ in range(n)] for _ in range(m)]
            area, corner, leg_col, leg_row = largest_triangle(grid)
            assert area == brute_triangle(grid)
            if area:
                (r, c), (r1, c1), (r2, c2) = corner, leg_col, leg_row
                k = abs(r1 - r) + 1
                assert c1 == c and r2 == r and abs(c2 - c) + 1 == k and k * (k + 1) // 2 == area
                dv, dh = (1 if r1 >= r else -1), (1 if c2 >= c else -1)
                assert all(grid[a][b] for a, b in triangle(corner, k, dv, dh))
        ```

---

### סעיף א – הריבוע הגדול ביותר

מצא את הריבוע הגדול ביותר שכולו `1`, בזמן \( O(m \cdot n) \).

??? tip "רמז 1"
    נניח שאתה יודע את התשובה לכל תא מעליך ומשמאלך. מה זה אומר על התא הנוכחי?

??? tip "רמז 2"
    הגדירו לכל תא את הצלע של הריבוע הגדול ביותר **שהפינה הימנית-התחתונה שלו** היא התא
    הזה. ריבוע בצלע \( k \) שנגמר בתא מכיל שלושה ריבועים בצלע \( k - 1 \). איפה הם
    נגמרים?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **תכנון דינמי :** הצלע של הריבוע שנגמר בתא היא המינימום של שלושה שכנים (למעלה,
        משמאל ובאלכסון) ועוד 1, או 0 בתא של 0. התשובה היא הצלע הגדולה ביותר, והפינות
        נגזרות ממנה ומהתא שבו היא נמצאה.

    <!-- cost: זמן \( O(m \cdot n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    נגדיר \( dp[i][j] \) : אורך הצלע של הריבוע הגדול ביותר שכולו 1, שהפינה
    הימנית-התחתונה שלו היא \( (i, j) \). הריבוע הגדול ביותר במערך נגמר באיזשהו תא, ולכן
    התשובה היא \( \max_{i,j} dp[i][j] \). בתא של 0 אין ריבוע, ו-\( dp[i][j] = 0 \). בתא
    של 1 :

    \[
    \begin{aligned}
    dp[i][j] = 1 + \min\bigl(&dp[i-1][j],\; dp[i][j-1],\\
    &dp[i-1][j-1]\bigr)
    \end{aligned}
    \]

    כאשר תאים מחוץ למערך נחשבים 0.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מעבר שורה אחרי שורה :** כל תא צריך את השכן מלמעלה, משמאל ובאלכסון, וכולם כבר
       חושבו כשעוברים על המערך משמאל לימין ומלמעלה למטה.
    2. **חיסכון בזיכרון :** כל תא צריך רק את השורה הקודמת ואת התא שמשמאלו, ולכן מספיק
       מערך אחד באורך \( n + 1 \) :
        - **‏`dp[j]` לפני העדכון :** התא מלמעלה.
        - **‏`dp[j - 1]` אחרי העדכון :** התא משמאל.
        - **התא שבאלכסון :** נשמר במשתנה `diag`, כי העדכון של `dp[j - 1]` מחק אותו.
    3. **מהצלע לפינות :** כשמוצאים צלע גדולה יותר \( k \) בתא \( (i, j) \), שומרים אותו
       כפינה הימנית-התחתונה. בסוף :

        \[
        \begin{aligned}
        \text{top_left} &= (i - k + 1,\; j - k + 1)\\
        \text{bottom_right} &= (i,\; j)\\
        \text{area} &= k^2
        \end{aligned}
        \]

    4. **דוגמה :**

        ```text
        grid:          dp:
        1 0 1 1 1      1 0 1 1 1
        1 1 1 1 1      1 1 1 2 2
        0 1 1 1 1      0 1 2 2 3
        1 1 1 1 0      1 1 2 3 0
        ```

        המקסימום הוא 3, לראשונה בתא \( (2, 4) \). התוצאה : `(9, (0, 2), (2, 4))`. יש גם
        ריבוע שני באותו גודל, מ-\( (1, 1) \) עד \( (3, 3) \), אבל הקוד שומר רק צלע
        **גדולה** יותר, ולכן מחזיר את הראשון.

    </div>

    **נסו בעצמכם.** התיבה מתחילה מהדוגמה. לחיצה על תא הופכת אותו, גרירה מסמנת מלבן
    שאפשר להפוך כולו ל-1 או ל-0, ו"מערך אקראי" ממלא מערך בגודל שבחרתם לפי הסיכוי ל-1.
    בשדה "הערכים" אפשר להדביק מערך שלם, וב"תצוגה" אפשר לבחור "התוצאה הסופית", שנשארת גם
    אחרי כל עריכה ומערך אקראי.
    כל צעד ממלא תא אחד ב-\( dp \) ומדגיש את שלושת השכנים שנקראו. הריבוע הטוב עד עכשיו
    מוקף בכתום, ובסוף הריבוע נצבע בירוק :

    <div class="explorer" data-kind="maxones" data-mode="square" data-grid="10111.11111.01111.11110"></div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="largest_square" linenums="1"
        function automatic int min3(int a, int b, int c);
          int m = a < b ? a : b;
          return m < c ? m : c;
        endfunction

        // Part a: dp[j + 1] is the side of the largest square of ones whose bottom-right
        // corner is column j of the current row.
        function automatic shape_t largest_square(bit grid[][]);
          int n, side = 0, ei, ej, top, diag, dp[];
          if (grid.size() == 0 || grid[0].size() == 0) return '{0, -1, -1, -1, -1};
          n = grid[0].size();
          dp = new[n + 1];                        // all 0: the row above the grid
          foreach (grid[i]) begin
            diag = 0;                             // dp of the cell up-left
            for (int j = 1; j <= n; j++) begin
              top = dp[j];
              if (grid[i][j - 1]) begin
                dp[j] = min3(top, dp[j - 1], diag) + 1;
                if (dp[j] > side) begin side = dp[j]; ei = i; ej = j - 1; end
              end else dp[j] = 0;
              diag = top;
            end
          end
          if (side == 0) return '{0, -1, -1, -1, -1};
          return '{side * side, ei - side + 1, ej - side + 1, ei, ej};
        endfunction
        ```

    === "Python"
        ```python title="largest_square" linenums="1"
        def largest_square(grid):
            if not grid or not grid[0]:
                return 0, None, None
            n = len(grid[0])
            dp = [0] * (n + 1)          # dp[j + 1] = the value for column j
            side, end = 0, None
            for i, row in enumerate(grid):
                diag = 0                # dp of the cell up-left
                for j in range(1, n + 1):
                    top = dp[j]
                    if row[j - 1] == 1:
                        dp[j] = min(top, dp[j - 1], diag) + 1
                        if dp[j] > side:
                            side, end = dp[j], (i, j - 1)
                    else:
                        dp[j] = 0
                    diag = top
            if side == 0:
                return 0, None, None
            r, c = end
            return side * side, (r - side + 1, c - side + 1), end
        ```

    #### למה זה נכון { .sol-proof }

    נניח ש-\( grid[i][j] = 1 \) ונסמן \( k = dp[i][j] \).

    - **הריבוע מוגבל על ידי כל שכן :** ריבוע בצלע \( k \) שנגמר ב-\( (i, j) \) מכיל
      שלושה ריבועים בצלע \( k - 1 \) : אחד שנגמר ב-\( (i - 1, j) \), אחד
      ב-\( (i, j - 1) \) ואחד ב-\( (i - 1, j - 1) \). לכן כל אחד משלושת השכנים לפחות
      \( k - 1 \).
    - **והמינימום מספיק :** אם שלושת השכנים לפחות \( t \), אז שלושת הריבועים בצלע \( t \)
      שנגמרים בהם, יחד עם התא \( (i, j) \), מכסים את כל הריבוע בצלע \( t + 1 \) שנגמר
      ב-\( (i, j) \).

    מכאן ש-\( k \) הוא בדיוק המינימום של השלושה ועוד 1. הקוד נבדק מול חיפוש מלא על כל
    המערכים עד \( 3 \times 3 \) ועל אלפי מערכים אקראיים עד \( 7 \times 7 \).

    #### סיבוכיות { .sol-cost }

    זמן \( O(m \cdot n) \) : כל תא נקרא פעם אחת ומחושב בשלוש השוואות. זיכרון \( O(n) \) :
    שורה אחת של \( dp \). זה אופטימלי, כי צריך לקרוא כל תא לפחות פעם אחת.

---

### סעיף ב – המלבן הגדול ביותר

מצא את המלבן בעל השטח הגדול ביותר שכולו `1`, בזמן \( O(m \cdot n) \).

??? tip "רמז 1"
    בעיה עצמאית קודם : נתונה היסטוגרמה, שורה של עמודות בגבהים שונים. איך מוצאים את
    המלבן הגדול ביותר שנכנס בה?

??? tip "רמז 2"
    לכל מלבן של אחדות יש שורה תחתונה. מה רואים אם סופרים, מעל כל תא בשורה הזו, כמה
    אחדות רצופות יש מעליו?

??? tip "רמז 3"
    במלבן הגדול בהיסטוגרמה, הגובה הוא הגובה של העמודה הנמוכה ביותר בו. איך מוצאים לכל
    עמודה את העמודה הנמוכה הראשונה משמאל ומימין, במעבר אחד?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **היסטוגרמה בכל שורה :** \( heights[j] \) סופר את ה-1 הרצופים בעמודה \( j \)
        שנגמרים בשורה הנוכחית. המלבן הגדול במערך הוא הגדול מבין המלבנים הגדולים
        בהיסטוגרמות של השורות, וכל היסטוגרמה נפתרת ב-\( O(n) \) עם מחסנית של עמודות
        בגבהים עולים.

    <!-- cost: זמן \( O(m \cdot n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **למה הפתרון של הריבוע לא עובד.** בריבוע מספיק מספר אחד לכל תא (הצלע), ושלושת
    השכנים קובעים אותו. במלבן יש שני ממדים בלתי תלויים : מלבן רחב ונמוך ומלבן צר וגבוה
    שנגמרים באותו תא לא ניתנים להשוואה. לכן צריך רעיון אחר.

    **כל שורה היא היסטוגרמה.** עבור כל שורה \( i \) נגדיר \( heights[j] \) : מספר ה-1
    הרצופים בעמודה \( j \) שנגמרים בשורה \( i \). בתא של 0 הגובה מתאפס, ובתא של 1 הוא
    גדל ב-1 מהשורה הקודמת. לכל מלבן של אחדות יש שורה תחתונה, ובהיסטוגרמה של השורה הזו
    הוא "עומד" על הבסיס, כלומר הוא מלבן בתוך ההיסטוגרמה. לכן המלבן הגדול במערך הוא
    המקסימום, על פני כל השורות, של המלבן הגדול בהיסטוגרמה של השורה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המלבן הגדול בהיסטוגרמה :** במלבן המקסימלי, הגובה שווה לגובה של העמודה הנמוכה
       ביותר בו. לכן מספיק לבדוק, **לכל עמודה**, את המלבן שגובהו בדיוק הגובה שלה
       ושמתרחב שמאלה וימינה עד העמודות הראשונות שנמוכות ממנה.
    2. **מחסנית בגבהים עולים :** את הגבולות האלה מוצאים במעבר אחד :
        - **גבול ימני :** כשמגיעה עמודה \( j \) נמוכה מהעמודה בראש המחסנית, \( j \) היא
          העמודה הנמוכה הראשונה מימין. מוציאים את העמודה מהמחסנית ומחשבים את המלבן שלה.
        - **גבול שמאלי :** העמודה שמתחתיה במחסנית היא הנמוכה הראשונה משמאל, כי כל מה
          שהיה ביניהן כבר יצא, כלומר היה גבוה יותר.
        - **סוף השורה :** מוסיפים עמודה דמיונית בגובה 0, כדי לרוקן את המחסנית.
    3. **מהמחסנית לפינות :** כשעמודה בגובה \( h \) יוצאת מהמחסנית בזמן שבודקים את
       העמודה \( j \), והעמודה שמתחתיה במחסנית היא \( p \) (או שהמחסנית ריקה) :

        \[
        \begin{aligned}
        \text{left} &= p + 1 \;\;(\text{or } 0)\\
        \text{area} &= h \cdot (j - \text{left})\\
        \text{top_left} &= (i - h + 1,\; \text{left})\\
        \text{bottom_right} &= (i,\; j - 1)
        \end{aligned}
        \]

    4. **דוגמה שבה מלבן מנצח ריבוע :**

        ```text
        grid:
        1 1 1 1 0
        1 1 1 1 1
        0 1 1 0 1
        ```

        | שורה | ‏heights | המלבן הטוב בשורה |
        |:-:|:-:|---|
        | ‏0 | ‏1 1 1 1 0 | שטח 4 |
        | ‏1 | ‏2 2 2 2 1 | **שטח 8** (גובה 2, עמודות 0-3) |
        | ‏2 | ‏0 3 3 0 2 | שטח 6 (גובה 3, עמודות 1-2) |

        התוצאה : `(8, (0, 0), (1, 3))`. הריבוע הגדול ביותר באותו מערך הוא רק
        \( 2 \times 2 \), בשטח 4.

    5. **מעקב אחרי המחסנית בשורה 1 :** ‏\( heights = [2, 2, 2, 2, 1] \).

        | ‏\( j \) | גובה \( j \) | מה קורה | מלבן שנבדק |
        |:-:|:-:|---|---|
        | ‏0 | ‏2 | דוחפים 0 | |
        | ‏1 | ‏2 | מוציאים 0 (לא נמוך יותר), דוחפים 1 | שטח 2 |
        | ‏2 | ‏2 | מוציאים 1, דוחפים 2 | שטח 4 |
        | ‏3 | ‏2 | מוציאים 2, דוחפים 3 | שטח 6 |
        | ‏4 | ‏1 | מוציאים 3 : גובה 2, עמודות 0-3 | **שטח 8** |
        | ‏5 | ‏0 (דמיוני) | מוציאים 4 : גובה 1, עמודות 0-4 | שטח 5 |

    </div>

    **נסו בעצמכם.** אותה תיבה, במצב מלבן ועם הדוגמה של הסעיף. צעד הוא עדכון של שורה,
    דחיפה למחסנית או הוצאה ממנה. לצד המערך מתמלאת טבלת \( heights \), שורה אחרי שורה,
    והעמודות שבמחסנית מסומנות בפס. המלבן שנבדק מקווקו, הטוב עד עכשיו מוקף בכתום, ובסוף
    המלבן נצבע בירוק :

    <div class="explorer" data-kind="maxones" data-mode="rect" data-grid="11110.11111.01101"></div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="largest_rectangle" linenums="1"
        // Part b: every row as a histogram of the ones that end in it, and the largest
        // rectangle of each histogram by a stack of columns with increasing heights.
        function automatic shape_t largest_rectangle(bit grid[][]);
          shape_t best = '{0, -1, -1, -1, -1};
          int n, h, height, left, area, heights[], stack[$];
          if (grid.size() == 0 || grid[0].size() == 0) return best;
          n = grid[0].size();
          heights = new[n];
          foreach (grid[i]) begin
            for (int j = 0; j < n; j++) heights[j] = grid[i][j] ? heights[j] + 1 : 0;
            stack.delete();                                  // column indices with increasing heights
            for (int j = 0; j <= n; j++) begin
              h = j < n ? heights[j] : 0;                    // a zero at the end empties the stack
              while (stack.size() > 0 && heights[stack[$]] >= h) begin
                height = heights[stack.pop_back()];
                left = stack.size() > 0 ? stack[$] + 1 : 0;
                area = height * (j - left);
                if (area > best.area) best = '{area, i - height + 1, left, i, j - 1};
              end
              stack.push_back(j);
            end
          end
          return best;
        endfunction
        ```

    === "Python"
        ```python title="largest_rectangle" linenums="1"
        def largest_rectangle(grid):
            if not grid or not grid[0]:
                return 0, None, None
            n = len(grid[0])
            heights = [0] * n
            best, top_left, bottom_right = 0, None, None
            for i, row in enumerate(grid):
                for j in range(n):
                    heights[j] = heights[j] + 1 if row[j] == 1 else 0
                stack = []                           # column indices with increasing heights
                for j in range(n + 1):
                    h = heights[j] if j < n else 0   # a zero at the end empties the stack
                    while stack and heights[stack[-1]] >= h:
                        height = heights[stack.pop()]
                        left = stack[-1] + 1 if stack else 0
                        area = height * (j - left)
                        if area > best:
                            best = area
                            top_left, bottom_right = (i - height + 1, left), (i, j - 1)
                    stack.append(j)
            return best, top_left, bottom_right
        ```

    #### למה זה נכון { .sol-proof }

    **כל מלבן נבדק או נשלט.** קחו מלבן מקסימלי, והעמודה הנמוכה ביותר בו בשורה התחתונה
    שלו (הימנית מביניהן, אם יש כמה). כשהעמודה הזו יוצאת מהמחסנית, הגבול הימני הוא
    העמודה הנמוכה הראשונה מימינה, והגבול השמאלי הוא העמודה הנמוכה ממנה הראשונה משמאלה.
    המלבן שנבדק הוא לפחות המלבן המקסימלי, ולכן הקוד מוצא את השטח הנכון.

    **הערה על `>=` :** כשמוציאים גם עמודות בגובה שווה, המלבן של העמודה שיוצאת ראשונה קצר
    מדי, אבל העמודה האחרונה באותו גובה מחשבת את הרוחב המלא. לכן התשובה נשארת נכונה.

    הקוד נבדק מול חיפוש מלא על כל המערכים עד \( 3 \times 3 \) ועל אלפי מערכים אקראיים
    עד \( 7 \times 7 \), ובכל מקרה הפינות מגדירות מלבן של אחדות בשטח שהוחזר.

    #### סיבוכיות { .sol-cost }

    זמן \( O(m \cdot n) \) : כל שורה מעדכנת \( n \) גבהים ומריצה מחסנית, וכל עמודה נכנסת
    למחסנית ויוצאת ממנה פעם אחת, ולכן \( O(n) \) לשורה. זיכרון \( O(n) \) : הגבהים
    והמחסנית.

---

### סעיף ג – המשולש הגדול ביותר

מצא את המשולש ישר הזווית בעל השטח הגדול ביותר שכולו `1`, עם ניצבים שווים ומקבילים
לצירים, בזמן \( O(m \cdot n) \).

??? tip "רמז 1"
    התחילו מכיוון אחד : הזווית הישרה למטה מימין, ושני הניצבים יוצאים ממנה למעלה ושמאלה.
    במה המשולש הזה דומה לריבוע של סעיף א, ובמה הוא שונה ממנו?

??? tip "רמז 2"
    משולש בניצב \( k \) שהזווית הישרה שלו בתא \( (i, j) \) מכיל שני משולשים בניצב
    \( k - 1 \) באותו כיוון. איפה הזוויות הישרות שלהם? ואיזה מבין שלושת השכנים של סעיף
    א כבר לא נחוץ?

??? tip "רמז 3"
    ארבעת הכיוונים הם אותה בעיה, רק שהמעבר על המערך מתחיל מצד אחר. איך מריצים את אותו
    מעבר ארבע פעמים בלי לכתוב אותו ארבע פעמים?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        **תכנון דינמי עם שני שכנים :** לכל כיוון, הניצב של המשולש שהזווית הישרה שלו בתא
        הוא המינימום של שני שכנים, אחד לאורך כל ניצב, ועוד 1. מריצים ארבעה מעברים, אחד
        לכל כיוון, וכל מעבר עובר על השורות ועל העמודות כך שהשכנים כבר חושבו. משולש בניצב
        \( k \) מכיל \( k(k + 1)/2 \) תאים.

    <!-- cost: זמן \( O(m \cdot n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    נקבע כיוון : הניצבים יוצאים מהזווית הישרה לכיוון \( d_v \) בעמודה (למעלה \( -1 \)
    או למטה \( +1 \)) ולכיוון \( d_h \) בשורה (שמאלה \( -1 \) או ימינה \( +1 \)). המשולש
    בניצב \( k \) שהזווית הישרה שלו ב-\( (i, j) \) הוא התאים

    \[
    \begin{aligned}
    &(i + d_v \cdot a,\; j + d_h \cdot b)\\
    &a, b \ge 0,\;\; a + b \le k - 1
    \end{aligned}
    \]

    כלומר שורה של \( k \) תאים לאורך ניצב אחד, לידה שורה של \( k - 1 \) תאים, וכן הלאה עד
    תא אחד בקצה של הניצב השני. בסך הכול \( k(k + 1)/2 \) תאים. נגדיר \( dp[i][j] \) : הניצב
    של המשולש הגדול ביותר בכיוון הזה שהזווית הישרה שלו ב-\( (i, j) \). בתא של 0 הוא 0, ובתא
    של 1 :

    \[
    dp[i][j] = 1 + \min\bigl(dp[i + d_v][j],\; dp[i][j + d_h]\bigr)
    \]

    כאשר תאים מחוץ למערך נחשבים 0. זו הנוסחה של סעיף א **בלי השכן שבאלכסון** : בריבוע
    השכן הזה שומר על הפינה שמול הזווית, ובמשולש אין פינה כזו.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ארבעה מעברים :** מעבר לכל זוג \( (d_v, d_h) \). השכנים צריכים להיות מחושבים לפני
       התא, ולכן המעבר מתחיל מהצד שאליו פונים הניצבים :
        - **השורות :** כשהניצב עולה, מלמעלה למטה. כשהוא יורד, מלמטה למעלה.
        - **העמודות :** כשהניצב פונה שמאלה, משמאל לימין. כשהוא פונה ימינה, מימין לשמאל.
    2. **שורה אחת בזיכרון :** מספיק מערך אחד באורך \( n \), שמתאפס בתחילת כל מעבר :
        - **‏`dp[j]` לפני העדכון :** התא בשורה הקודמת של המעבר, כלומר השכן לאורך העמודה.
        - **‏`prev` :** התא שחושב רגע לפני כן באותה שורה, כלומר השכן לאורך השורה.
        - **אין `diag` :** בניגוד לסעיף א, אף אחד לא צריך את הערך הישן של התא.
    3. **מהניצב לקודקודים :** כשמוצאים ניצב גדול יותר \( k \) בתא \( (i, j) \) :

        \[
        \begin{aligned}
        \text{corner} &= (i,\; j)\\
        \text{leg_col} &= (i + d_v (k - 1),\; j)\\
        \text{leg_row} &= (i,\; j + d_h (k - 1))\\
        \text{area} &= k(k + 1)/2
        \end{aligned}
        \]

    4. **דוגמה :** המעבר שבו הניצבים יוצאים למעלה וימינה (\( d_v = -1 \), \( d_h = +1 \)),
       שורות מלמעלה למטה ועמודות מימין לשמאל :

        ```text
        grid:            dp:
        1 0 0 0 0 0 1    1 0 0 0 0 0 1
        1 1 0 0 0 1 1    2 1 0 0 0 1 1
        1 1 1 0 1 1 1    3 2 1 0 1 2 1
        1 1 1 1 0 1 0    4 3 2 1 0 1 0
        0 1 0 1 1 1 1    0 1 0 2 1 2 1
        ```

        המקסימום הוא 4, בתא \( (3, 0) \), והתוצאה היא `(10, (3, 0), (0, 0), (3, 3))`. בצד
        ימין יש משולש בניצב 3 שהזווית הישרה שלו ב-\( (2, 6) \) והניצבים שלו יוצאים
        למעלה ושמאלה, בשטח 6. בשורות 3 ו-4, בעמודות 4 עד 6, יש את הצורה `0 1 0` מעל
        `1 1 1`, והיא נותנת רק ניצב 2. באותו מערך הריבוע הגדול הוא \( 2 \times 2 \) והמלבן
        הגדול בשטח 6 : משולש הוא לא מלבן, ולכן השטח שלו יכול לעבור את המלבן הגדול.

    </div>

    **נסו בעצמכם.** אותה תיבה, במצב משולש ועם הדוגמה של הסעיף. כל צעד ממלא תא אחד ב-\( dp \)
    של הכיוון הנוכחי ומדגיש את שני השכנים שנקראו, והריצה עוברת על ארבעת הכיוונים אחד
    אחרי השני ("הכיוון הבא" קופץ ביניהם). המשולש הטוב עד עכשיו מוקף בכתום, ובסוף המשולש
    נצבע בירוק :

    <div class="explorer" data-kind="maxones" data-mode="tri" data-grid="1000001.1100011.1110111.1111010.0101111"></div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="largest_triangle" linenums="1"
        // Part c: a pass for each direction of the legs; dp[j] is the leg of the largest
        // triangle of ones whose right angle is column j of the current row.
        function automatic tri_t largest_triangle(bit grid[][]);
          tri_t best = '{0, -1, -1, -1, -1, -1, -1};
          int m, n, i, j, side = 0, prev, dp[];
          if (grid.size() == 0 || grid[0].size() == 0) return best;
          m = grid.size();
          n = grid[0].size();
          for (int dv = -1; dv <= 1; dv += 2)            // the legs go up (-1) or down (+1)
            for (int dh = -1; dh <= 1; dh += 2) begin    // and left (-1) or right (+1)
              dp = new[n];                               // all 0
              for (int s = 0; s < m; s++) begin
                i = dv < 0 ? s : m - 1 - s;              // the rows the legs point to first
                prev = 0;                                // dp of the neighbour along the row
                for (int t = 0; t < n; t++) begin
                  j = dh < 0 ? t : n - 1 - t;
                  dp[j] = grid[i][j] ? (dp[j] < prev ? dp[j] : prev) + 1 : 0;
                  if (dp[j] > side) begin
                    side = dp[j];
                    best = '{side * (side + 1) / 2, i, j, i + dv * (side - 1), j, i, j + dh * (side - 1)};
                  end
                  prev = dp[j];
                end
              end
            end
          return best;
        endfunction
        ```

    === "Python"
        ```python title="largest_triangle" linenums="1"
        def largest_triangle(grid):
            if not grid or not grid[0]:
                return 0, None, None, None
            m, n = len(grid), len(grid[0])
            side, corner, legs = 0, None, None
            for dv, dh in ((-1, -1), (-1, 1), (1, -1), (1, 1)):   # the legs: up or down, left or right
                rows = range(m) if dv < 0 else range(m - 1, -1, -1)   # the rows the legs point to first
                cols = range(n) if dh < 0 else range(n - 1, -1, -1)
                dp = [0] * n            # dp[j] = the leg for column j of the current row
                for i in rows:
                    prev = 0            # dp of the neighbour along the row
                    for j in cols:
                        dp[j] = min(dp[j], prev) + 1 if grid[i][j] == 1 else 0
                        if dp[j] > side:
                            side, corner = dp[j], (i, j)
                            legs = (i + dv * (side - 1), j), (i, j + dh * (side - 1))
                        prev = dp[j]
            if side == 0:
                return 0, None, None, None
            return side * (side + 1) // 2, corner, *legs
        ```

    #### למה זה נכון { .sol-proof }

    נניח ש-\( grid[i][j] = 1 \), ונסמן \( k = dp[i][j] \) בכיוון \( (d_v, d_h) \).

    - **המשולש מוגבל על ידי שני השכנים :** המשולש בניצב \( k \) מכיל שני משולשים בניצב
      \( k - 1 \) באותו כיוון : התאים עם \( a \ge 1 \) הם המשולש שהזווית הישרה שלו
      ב-\( (i + d_v, j) \), והתאים עם \( b \ge 1 \) הם המשולש שהזווית הישרה שלו
      ב-\( (i, j + d_h) \). לכן כל אחד משני השכנים לפחות \( k - 1 \).
    - **והמינימום מספיק :** אם שני השכנים לפחות \( t \), שני המשולשים בניצב \( t \)
      שלהם מכסים את כל התאים של המשולש בניצב \( t + 1 \), חוץ מהתא היחיד שבו
      \( a = b = 0 \), שהוא \( (i, j) \) עצמו.
    - **כל משולש נבדק :** לכל משולש יש זווית ישרה וכיוון אחד, והמעבר של הכיוון הזה מחשב
      את \( dp \) בתא של הזווית.

    הקוד נבדק מול חיפוש מלא על כל המערכים עד \( 3 \times 3 \) ועל אלפי מערכים אקראיים עד
    \( 8 \times 8 \), ובכל מקרה שלושת הקודקודים מגדירים משולש של אחדות בשטח שהוחזר.

    #### סיבוכיות { .sol-cost }

    זמן \( O(m \cdot n) \) : ארבעה מעברים, וכל אחד קורא כל תא פעם אחת ומשווה שני מספרים.
    זיכרון \( O(n) \) : שורה אחת של \( dp \), שמתאפסת בין המעברים. זה אופטימלי, כי צריך
    לקרוא כל תא לפחות פעם אחת.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להתאים את נוסחת הריבוע למלבן"
    טעות נפוצה בסעיף ב היא לשמור לכל תא רוחב וגובה מקסימליים ולכפול אותם. זה לא עובד,
    כי הרוחב הטוב והגובה הטוב לא בהכרח שייכים לאותו מלבן. במערך `0 1` מעל `1 1`, מעל
    התא \( (1, 1) \) יש עמודה בגובה 2 ומשמאלו שורה ברוחב 2, אבל אין מלבן
    \( 2 \times 2 \) של אחדות : התא \( (0, 0) \) הוא 0, והתשובה היא 2.

??? trap "מלכודת : העמודה הדמיונית בסוף השורה"
    בלי העמודה בגובה 0 בסוף, העמודות שנשארות במחסנית לא יוצאות ממנה, והמלבנים שמגיעים
    עד הקצה הימני לא נבדקים. במערך של שורה אחת `1 1 1` הקוד היה מחזיר 0.

??? trap "מלכודת : מקרי קצה"
    מערך ריק, מערך בלי אף `1` (התשובה `(0, None, None)`), שורה אחת או עמודה אחת. בשורה
    אחת הריבוע הגדול הוא \( 1 \times 1 \), והמלבן הוא הרצף הארוך ביותר של אחדות.
    המשולש בשורה אחת הוא תא בודד, בשטח 1.

??? trap "מלכודת : שלושה שכנים במשולש"
    מי שמעתיק את נוסחת סעיף א כמו שהיא, עם השכן שבאלכסון, מקבל ריבוע ולא משולש. במשולש
    השמאלי מהשאלה (`1 0 0` מעל `1 1 0` מעל `1 1 1`), בכיוון שבו הניצבים יוצאים למעלה
    וימינה, השכן שבאלכסון של \( (2, 0) \) הוא \( (1, 1) \). שם הניצב הוא 1 בלבד,
    כי \( (0, 1) \) הוא 0, ולכן הנוסחה עם שלושה שכנים נותנת בזווית ניצב 2 במקום 3, ושטח 3
    במקום 6.

??? trap "מלכודת : סדר המעבר"
    בכיוון שבו הניצב פונה ימינה, השכן לאורך השורה הוא \( (i, j + 1) \). מעבר רגיל משמאל
    לימין קורא אותו לפני שחושב, כלומר את הערך של השורה הקודמת, והתשובה יוצאת שגויה. לכן
    כל מעבר מתחיל מהצד שאליו פונים הניצבים.

??? followup "שאלות המשך"
    - **כל התשובות :** איך מחזירים את כל הריבועים או המלבנים בשטח המקסימלי? בריבוע, כל
      תא עם \( dp[i][j] \) שווה למקסימום הוא פינה של ריבוע כזה. התיבה מציינת כמה יש, בכל אחת משלוש הצורות.
    - **קובייה :** הכללה למערך תלת-ממדי. נוסחת הריבוע הופכת למינימום של 7 שכנים ועוד 1.
    - **פתרון ביניים :** פתרון \( O(m^2 \cdot n) \) לסעיף ב : לכל זוג שורות, העמודות
      שכולן 1 בין שתי השורות, והרצף הארוך ביותר שלהן.
    - **פירמידה :** הצורה `0 1 0` מעל `1 1 1`, שסעיף ג לא סופר, היא משולש שווה-שוקיים
      שהבסיס שלו בשורה. פירמידה בגובה \( h \) שמרכז הבסיס שלה ב-\( (i, j) \) היא פירמידה
      בגובה \( h - 1 \) שמרכז הבסיס שלה ב-\( (i - 1, j) \), ומתחתיה שורה של
      \( 2h - 1 \) אחדות. לכן \( P[i][j] = \min(P[i-1][j] + 1,\; L[i][j],\; R[i][j]) \),
      כאשר \( L \) ו-\( R \) סופרים את ה-1 הרצופים שמשמאל לתא ומימינו, כולל התא עצמו. השטח
      הוא \( h^2 \).
