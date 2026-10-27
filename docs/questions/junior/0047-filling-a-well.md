---
id: 47
title: מילוי מים בבאר
level: junior
difficulty: hard
kind: code
tags: [algorithms, two-pointers, heap, dijkstra, python, systemverilog]
source: "שאלה נפוצה בראיונות קוד (לפי דיווחי מועמדים מ-Google, ‏Meta ו-Microsoft), LeetCode 42 ו-407"
added: 2026-10-25
---

## השאלה

יורד גשם על עמודים ברוחב 1 שעומדים זה לצד זה, והמים נאספים בבורות שביניהם. מים שמגיעים
לקצה נשפכים החוצה.

- **סעיף א :** נתון מערך `height` של \( n \) גבהים שלמים ואי-שליליים. כמה יחידות מים
  נשארות בין העמודים? בזמן \( O(n) \) ובזיכרון \( O(1) \).
- **סעיף ב :** נתונה מפת גבהים `height` בגודל \( m \times n \). המים זורמים לארבעת
  הכיוונים (לא באלכסון), ומתאי השפה הם נשפכים החוצה. כמה יחידות מים נשארות על המפה?

למשל, בשורה `[3, 0, 2, 0, 4]` נשארות 7 יחידות :

<!-- gen 0 -->

<svg class="figure" viewBox="0 0 232 210" style="max-width:14.5rem" role="img" aria-label="העמודים 3, 0, 2, 0, 4 : נשארות 7 יחידות מים"><rect class="fig-ground" x="8" y="144" width="40" height="40" rx="3"/><rect class="fig-ground" x="8" y="100" width="40" height="40" rx="3"/><rect class="fig-ground" x="8" y="56" width="40" height="40" rx="3"/><rect class="st-cell" x="8" y="12" width="40" height="40" rx="3"/><text class="st-text" x="28" y="204" text-anchor="middle">3</text><rect class="fig-water" x="52" y="144" width="40" height="40" rx="3"/><rect class="fig-water" x="52" y="100" width="40" height="40" rx="3"/><rect class="fig-water" x="52" y="56" width="40" height="40" rx="3"/><rect class="st-cell" x="52" y="12" width="40" height="40" rx="3"/><text class="st-text" x="72" y="204" text-anchor="middle">0</text><rect class="fig-ground" x="96" y="144" width="40" height="40" rx="3"/><rect class="fig-ground" x="96" y="100" width="40" height="40" rx="3"/><rect class="fig-water" x="96" y="56" width="40" height="40" rx="3"/><rect class="st-cell" x="96" y="12" width="40" height="40" rx="3"/><text class="st-text" x="116" y="204" text-anchor="middle">2</text><rect class="fig-water" x="140" y="144" width="40" height="40" rx="3"/><rect class="fig-water" x="140" y="100" width="40" height="40" rx="3"/><rect class="fig-water" x="140" y="56" width="40" height="40" rx="3"/><rect class="st-cell" x="140" y="12" width="40" height="40" rx="3"/><text class="st-text" x="160" y="204" text-anchor="middle">0</text><rect class="fig-ground" x="184" y="144" width="40" height="40" rx="3"/><rect class="fig-ground" x="184" y="100" width="40" height="40" rx="3"/><rect class="fig-ground" x="184" y="56" width="40" height="40" rx="3"/><rect class="fig-ground" x="184" y="12" width="40" height="40" rx="3"/><text class="st-text" x="204" y="204" text-anchor="middle">4</text></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="fig-key-ground"></i>עמוד</span><span><i class="fig-key-water"></i>מים שנשארים, 7 יחידות</span></span>

<!-- /gen -->

=== "SystemVerilog"
    ```systemverilog title="trap, trap_2d"
    // function automatic int trap(int height[]);        // to write
    // function automatic int trap_2d(int height[][]);   // to write
    ```

=== "Python"
    ```python title="trap, trap_2d"
    def trap(height: list[int]) -> int: ...
    def trap_2d(height: list[list[int]]) -> int: ...
    ```

??? interviewer "מה המראיין בודק"
    - **פירוק לעמודות :** לראות שאפשר לחשב כל עמודה בנפרד. בבור שלם קשה להתמקד, ועמודה
      אחת תלויה רק בשני קירות.
    - **פתרונות ביניים :** \( O(n^2) \) (לכל עמודה מחפשים את הקירות), ואחריו \( O(n) \) עם
      שני מערכים. שני המצביעים הם השיפור בזיכרון, ושם המראיין מבקש נימוק ולא רק קוד.
    - **הכללה :** בסעיף ב, לראות שהנוסחה של השורה כבר לא נכונה, כי המים בורחים במסלול
      מפותל, ולהגיע לרעיון של "הצפה מבחוץ" עם ערימה. זה Dijkstra בתחפושת.
    - **רמה :** סעיף א מתאים לג'וניור. סעיף ב הוא שאלה קשה גם לסניור, ומותר לתת בו את
      הרמז על השפה.

---

### סעיף א – מים בשורה

כמה מים נשארים בין העמודים, בזמן \( O(n) \) ובזיכרון \( O(1) \)?

??? tip "רמז 1"
    אל תחשבו על בורות שלמים. כמה מים נשארים **מעל עמודה אחת**, ומה קובע את זה?

??? tip "רמז 2"
    המים מעל עמודה עולים עד הנמוך מבין שני קירות : הגבוה ביותר משמאלה והגבוה ביותר
    מימינה. איך יודעים את הנמוך מביניהם בלי לשמור את כל המקסימומים?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **שני מצביעים :** מעל עמודה נשארים \( \min(\text{maxL}, \text{maxR}) - h \).
        מתחילים משני הקצוות ובכל צעד מזיזים את הצד הנמוך יותר : בצד הזה הקיר הנמוך הוא
        המקסימום של הצד עצמו, ולכן אפשר לחשב את העמודה מיד.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    המים מעל עמודה \( i \) עולים עד הקיר הגבוה ביותר משמאלה, ועד הקיר הגבוה ביותר
    מימינה, כל אחד כולל העמודה עצמה. מעל הנמוך מבין השניים הם נשפכים לצד שלו :

    \[
    \begin{aligned}
    \text{water}[i] = \min\bigl(&\text{maxL}[i],\; \text{maxR}[i]\bigr)\\
    &- \text{height}[i]
    \end{aligned}
    \]

    התשובה היא סכום המים על כל העמודות. פתרון ראשון שומר את \( \text{maxL} \) ואת
    \( \text{maxR} \) בשני מערכים. הפתרון המלא מוותר עליהם : הוא צריך רק את **הנמוך**
    מבין השניים, ואותו אפשר לדעת בלי לדעת את השני.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שני מערכים :** \( \text{maxL} \) במעבר משמאל לימין, \( \text{maxR} \) במעבר מימין
       לשמאל, ומעבר שלישי שסוכם. בדוגמה מהשאלה :

        | ‏i | ‏0 | ‏1 | ‏2 | ‏3 | ‏4 |
        |---|:-:|:-:|:-:|:-:|:-:|
        | גובה | ‏3 | ‏0 | ‏2 | ‏0 | ‏4 |
        | ‏maxL | ‏3 | ‏3 | ‏3 | ‏3 | ‏4 |
        | ‏maxR | ‏4 | ‏4 | ‏4 | ‏4 | ‏4 |
        | מים | ‏0 | ‏3 | ‏1 | ‏3 | ‏0 |

        הסכום הוא 7. הזמן \( O(n) \), אבל הזיכרון \( O(n) \).

    2. **שני מצביעים :** `l` מתחיל בקצה השמאלי ו-`r` בקצה הימני, וכל אחד זוכר את המקסימום
       שראה בצד שלו (`left_max`, `right_max`).
    3. **מזיזים את הצד הנמוך :** אם `height[l] < height[r]`, מעדכנים את `left_max`,
       מוסיפים `left_max - height[l]` ומזיזים את `l` ימינה. אחרת, אותו דבר מימין.
    4. **מעקב על הדוגמה :**

        | צעד | ‏l | ‏r | ההשוואה | ‏left_max | מים | סך הכול |
        |:-:|:-:|:-:|---|:-:|:-:|:-:|
        | ‏1 | ‏0 | ‏4 | ‏3 < 4, שמאל | ‏3 | ‏0 | ‏0 |
        | ‏2 | ‏1 | ‏4 | ‏0 < 4, שמאל | ‏3 | ‏3 | ‏3 |
        | ‏3 | ‏2 | ‏4 | ‏2 < 4, שמאל | ‏3 | ‏1 | ‏4 |
        | ‏4 | ‏3 | ‏4 | ‏0 < 4, שמאל | ‏3 | ‏3 | ‏7 |

        המצביעים נפגשים בעמודה 4, הגבוהה ביותר, ומעליה אין מים. התשובה 7.

    </div>

    **נסו בעצמכם.** לחיצה על משבצת בעמודה קובעת את הגובה שלה, גרירה מסמנת כמה עמודות
    לערך אחד או ל-<bdi dir="ltr">+1</bdi> ו-<bdi dir="ltr">−1</bdi>, ובשדה "הערכים" אפשר להדביק מערך שלם. כל צעד מזיז מצביע אחד,
    ומתחת לעמודים מופיעים \( \text{maxL} \), \( \text{maxR} \) והמים של כל עמודה.
    ב"תצוגה" אפשר לבחור "התוצאה הסופית", ואז כל עריכה ומערך אקראי מראים מיד את המים :

    <div class="explorer" data-kind="rainwater" data-mode="row" data-heights="0,1,0,2,1,0,1,3,2,1,2,1"></div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="trap" linenums="1"
        // Part a: two pointers; the lower side's own maximum is the lower wall of its column.
        function automatic int trap(int height[]);
          int l = 0, r = height.size() - 1, left_max = 0, right_max = 0, water = 0;
          while (l < r) begin
            if (height[l] < height[r]) begin
              if (height[l] > left_max) left_max = height[l];
              water += left_max - height[l];
              l++;
            end else begin
              if (height[r] > right_max) right_max = height[r];
              water += right_max - height[r];
              r--;
            end
          end
          return water;
        endfunction
        ```

    === "Python"
        ```python title="trap" linenums="1"
        def trap(height):
            l, r = 0, len(height) - 1
            left_max = right_max = water = 0
            while l < r:
                if height[l] < height[r]:
                    left_max = max(left_max, height[l])
                    water += left_max - height[l]
                    l += 1
                else:
                    right_max = max(right_max, height[r])
                    water += right_max - height[r]
                    r -= 1
            return water
        ```

    #### למה זה נכון { .sol-proof }

    **הטענה :** כשמזיזים את `l` (כי `height[l] < height[r]`), אז
    \( \text{left_max} \le \text{maxR}[l] \), ולכן המים בעמודה הם בדיוק
    \( \text{left_max} - \text{height}[l] \).

    - **‏`left_max` הוא \( \text{maxL}[l] \) :** הוא המקסימום של כל העמודות עד \( l \).
    - **הוא לא גבוה מהקיר הימני :** \( \text{left_max} \) הוא הגובה של עמודה כלשהי
      \( k \le l \). כשהמצביע השמאלי עמד עליה, הוא זז ממנה, כלומר הייתה מולה עמודה ימנית
      גבוהה ממנה או שווה לה, ועמודה כזו עדיין נמצאת מימין ל-\( l \) (המצביע הימני רק זז
      שמאלה, ולא עבר את \( l \)). או ש-\( k = l \), ואז \( \text{height}[r] \) גבוה יותר.
      בשני המקרים \( \text{maxR}[l] \ge \text{left_max} \).

    המקרה של הזזת `r` סימטרי. הקוד נבדק מול הנוסחה על כל המערכים באורך עד 7 בגבהים 0 עד
    3, ועל אלפי מערכים אקראיים.

    #### סיבוכיות { .sol-cost }

    זמן \( O(n) \) : כל צעד מזיז מצביע אחד, ויש \( n - 1 \) צעדים. זיכרון \( O(1) \) :
    שני מצביעים, שני מקסימומים וסכום.

---

### סעיף ב – מים במפה

כמה מים נשארים על מפת גבהים דו-ממדית, כשהמים זורמים לארבעת הכיוונים?

??? tip "רמז 1"
    נסו את הנוסחה של סעיף א עם ארבעה קירות (למעלה, למטה, שמאלה וימינה) על המפה מתחת.
    למה היא נותנת יותר מדי?

    ```text
    3 3 3 3 3
    3 1 1 1 3
    3 1 5 1 3
    3 1 1 1 2
    3 3 3 3 3
    ```

??? tip "רמז 2"
    מתאי השפה המים נשפכים החוצה, ולכן הם "הקיר" הראשון. מאיזה תא בשפה המים יברחו קודם?

??? tip "רמז 3"
    בשני המצביעים של סעיף א תמיד התקדמנו מהקיר הנמוך. במפה יש גבול שלם במקום שני קצוות.
    איזה מבנה נתונים מוצא בכל פעם את התא הנמוך ביותר בגבול?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **הצפה מבחוץ עם ערימת מינימום :** מכניסים את כל תאי השפה לערימה. בכל צעד מוציאים
        את התא הנמוך ביותר בגבול, וכל שכן שעוד לא ביקרנו בו מתמלא עד הגובה שלו ונכנס
        לערימה בגובה **פני המים** שלו, כלומר \( \max(\text{level}, h) \).

    <!-- cost: זמן \( O(mn \log mn) \) | זיכרון \( O(mn) \) -->

    #### הרעיון { .sol-idea }

    **למה הנוסחה של סעיף א נכשלת.** בשורה, מים יכולים לברוח רק שמאלה או ימינה. במפה
    הם בורחים **במסלול מפותל**, דרך תאים שלא נמצאים באותה שורה או עמודה. במפה של הרמז,
    לכל תא של 1 יש קיר בגובה 3 בכל אחד מארבעת הכיוונים הישרים, והנוסחה נותנת 13. אבל
    מעל גובה 2 המים זורמים בין האחדות עד התא בגובה 2 בשפה הימנית, ונשפכים דרכו.
    התשובה הנכונה היא 8.

    **הצפה מבחוץ.** את מה שנבדק שומרים כ"אזור" שגבולו בערימה, וכל תא בגבול שמור עם גובה
    פני המים שלו. התא הנמוך ביותר בגבול הוא הנקודה שדרכה המים בורחים מכל מה שבפנים.
    שכן שלו שעוד לא נבדק מתמלא **בדיוק** עד הגובה הזה :

    - **לא יותר :** מעליו המים בורחים דרך התא הנמוך, ומשם החוצה.
    - **לא פחות :** כל שאר הגבול גבוה לפחות כמוהו, כי הוצאנו את המינימום, ולכן השכן מוקף
      קירות בגובה הזה לפחות.

    זה אותו רעיון כמו בסעיף א, "תמיד מתקדמים מהקיר הנמוך", וגם אותו מבנה כמו האלגוריתם
    של Dijkstra : המרחק הוא הגובה המקסימלי במסלול הטוב ביותר החוצה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **השפה :** כל תאי השפה נכנסים לערימה בגובה שלהם ומסומנים כ"נבדקו". הם לא מחזיקים
       מים.
    2. **הוצאת המינימום :** מוציאים את \( (\text{level}, i, j) \), התא הנמוך ביותר בגבול.
    3. **מילוי השכנים :** לכל שכן \( (a, b) \) שעוד לא נבדק :
        - **מים :** מוסיפים \( \max(0,\; \text{level} - h[a][b]) \).
        - **לערימה :** בגובה \( \max(\text{level},\; h[a][b]) \). שכן שהתמלא נכנס בגובה פני
          המים, לא בגובה הקרקע, כי המים מעליו הם עכשיו חלק מהקיר.
    4. **דוגמה :** המפה של הרמז. בשפה יש 16 תאים, כולם בגובה 3 חוץ מ-\( (3, 4) \) בגובה 2,
       ולכן הוא יוצא ראשון. בטבלה רק ההוצאות שהגיעו לתא חדש :

        | צעד | יצא | ‏level | השכן | גובה | מים |
        |:-:|:-:|:-:|:-:|:-:|:-:|
        | ‏1 | ‏(3, 4) | ‏2 | ‏(3, 3) | ‏1 | ‏1 |
        | ‏2 | ‏(3, 3) | ‏2 | ‏(2, 3) | ‏1 | ‏1 |
        | ‏3 | ‏(3, 3) | ‏2 | ‏(3, 2) | ‏1 | ‏1 |
        | ‏4 | ‏(2, 3) | ‏2 | ‏(1, 3) | ‏1 | ‏1 |
        | ‏5 | ‏(2, 3) | ‏2 | ‏(2, 2) | ‏5 | ‏0 |
        | ‏6 | ‏(1, 3) | ‏2 | ‏(1, 2) | ‏1 | ‏1 |
        | ‏7 | ‏(1, 2) | ‏2 | ‏(1, 1) | ‏1 | ‏1 |
        | ‏8 | ‏(1, 1) | ‏2 | ‏(2, 1) | ‏1 | ‏1 |
        | ‏9 | ‏(2, 1) | ‏2 | ‏(3, 1) | ‏1 | ‏1 |

        כל המים נכנסים דרך "הדליפה" בגובה 2, ותאי השפה בגובה 3 יוצאים רק אחריה. המים
        מתחלקים כך, וסכומם 8 :

        ```text
        0 0 0 0 0
        0 1 1 1 0
        0 1 0 1 0
        0 1 1 1 0
        0 0 0 0 0
        ```

    </div>

    **נסו בעצמכם.** לחיצה על תא מסמנת אותו וגרירה מסמנת מלבן. מספר שמקלידים נכנס לכל
    התאים המסומנים, לחיצה כפולה פותחת עריכה של תא, ובשדה "הערכים" אפשר להדביק מפה שלמה
    (גבהים 0 עד 20). כל צעד מוציא תא אחד מהערימה : הגבול שבערימה מוקף בכתום, התא שיצא
    ממוסגר, והמים נצבעים בכחול לפי העומק. לצד המפה מופיעה הערימה, מהנמוך לגבוה, וב"תצוגה"
    אפשר לעבור ישר לתוצאה הסופית :

    <div class="explorer" data-kind="rainwater" data-mode="map" data-map="3,3,3,3,3.3,1,1,1,3.3,1,5,1,3.3,1,1,1,2.3,3,3,3,3"></div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="min_heap, trap_2d" linenums="1"
        // Part b: a cell of the boundary, by the level of its water surface.
        typedef struct { int level, r, c; } cell_t;

        class min_heap;                          // a binary heap on level
          cell_t a[$];
          function int size(); return a.size(); endfunction
          function void push(cell_t x);
            int i = a.size();
            a.push_back(x);
            while (i > 0 && a[(i - 1) / 2].level > a[i].level) begin
              a[i] = a[(i - 1) / 2];
              a[(i - 1) / 2] = x;
              i = (i - 1) / 2;
            end
          endfunction
          function cell_t pop();
            cell_t top = a[0], t;
            int i = 0, k;
            a[0] = a[a.size() - 1];
            void'(a.pop_back());
            forever begin                        // sift down
              k = i;
              if (2 * i + 1 < a.size() && a[2 * i + 1].level < a[k].level) k = 2 * i + 1;
              if (2 * i + 2 < a.size() && a[2 * i + 2].level < a[k].level) k = 2 * i + 2;
              if (k == i) break;
              t = a[i]; a[i] = a[k]; a[k] = t;
              i = k;
            end
            return top;
          endfunction
        endclass

        function automatic int trap_2d(int height[][]);
          min_heap heap = new();
          bit seen[][];
          int m = height.size(), n, water = 0, a, b;
          cell_t cur;
          int dr[4] = '{1, -1, 0, 0}, dc[4] = '{0, 0, 1, -1};
          if (m == 0 || height[0].size() == 0) return 0;
          n = height[0].size();
          seen = new[m];
          foreach (seen[i]) seen[i] = new[n];
          foreach (height[i, j])                 // the border spills out: the first wall
            if (i == 0 || i == m - 1 || j == 0 || j == n - 1) begin
              heap.push('{height[i][j], i, j});
              seen[i][j] = 1;
            end
          while (heap.size() > 0) begin
            cur = heap.pop();                    // the lowest point of the wall
            for (int d = 0; d < 4; d++) begin
              a = cur.r + dr[d];
              b = cur.c + dc[d];
              if (a < 0 || a >= m || b < 0 || b >= n || seen[a][b]) continue;
              seen[a][b] = 1;
              if (cur.level > height[a][b]) begin
                water += cur.level - height[a][b];
                heap.push('{cur.level, a, b});   // its water surface is the new wall
              end else heap.push('{height[a][b], a, b});
            end
          end
          return water;
        endfunction
        ```

    === "Python"
        ```python title="trap_2d" linenums="1"
        import heapq

        def trap_2d(height):
            if not height or not height[0]:
                return 0
            m, n = len(height), len(height[0])
            seen = [[False] * n for _ in range(m)]
            heap = []                                # (water level, row, col) of the boundary
            for i in range(m):
                for j in range(n):
                    if i in (0, m - 1) or j in (0, n - 1):   # the border spills out
                        heapq.heappush(heap, (height[i][j], i, j))
                        seen[i][j] = True
            water = 0
            while heap:
                level, i, j = heapq.heappop(heap)    # the lowest point of the wall
                for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    if 0 <= a < m and 0 <= b < n and not seen[a][b]:
                        seen[a][b] = True
                        water += max(0, level - height[a][b])
                        heapq.heappush(heap, (max(level, height[a][b]), a, b))   # the new wall
            return water
        ```

    #### למה זה נכון { .sol-proof }

    נגדיר את **גובה הבריחה** של תא : מבין כל המסלולים מהתא אל מחוץ למפה, המסלול שבו
    הגובה המקסימלי הוא הקטן ביותר, והמקסימום הזה. המים מעל התא עולים בדיוק עד גובה
    הבריחה שלו, כי מעליו יש להם דרך החוצה ומתחתיו כל דרך חסומה. התשובה היא סכום
    \( \text{escape}(i, j) - h[i][j] \) על כל התאים.

    - **הערימה יוצאת בסדר עולה :** כל תא נכנס לערימה בגובה שלא קטן מהגובה של התא שיצא
      והכניס אותו, ולכן הגבהים שיוצאים מהערימה לא יורדים לעולם.
    - **הגובה שנקבע לשכן הוא גובה הבריחה שלו :** \( \max(\text{level}, h) \) הוא הגובה
      המקסימלי במסלול דרך התא שיצא, ולכן הוא לא נמוך מגובה הבריחה. ואין מסלול טוב ממנו :
      כל מסלול החוצה עובר דרך הגבול של האזור שנבדק, וכל הגבול נמצא בערימה בגובה
      \( \text{level} \) לפחות.

    כמו ב-Dijkstra, "המרחק" הוא גובה הבריחה, ותא שיצא מהערימה כבר סופי. הקוד נבדק מול
    חישוב ישיר של גובה הבריחה, בלי ערימה (מעדכנים כל תא לפי השכנים שלו עד שאין שינוי), על
    אלפי מפות אקראיות עד \( 7 \times 7 \).

    #### סיבוכיות { .sol-cost }

    זמן \( O(mn \log mn) \) : כל תא נכנס לערימה ויוצא ממנה פעם אחת, וכל פעולה בערימה
    עולה \( O(\log mn) \). זיכרון \( O(mn) \) : הערימה ומערך הביקורים.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להזיז את המצביע הגבוה"
    אם מזיזים את הצד הגבוה, המים של העמודה מחושבים לפי המקסימום של הצד שלה, אבל הקיר
    בצד השני יכול להיות נמוך יותר, והמים נשפכים דרכו. במערך
    `[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]` הגרסה הזו מחזירה 14 במקום 6.

??? trap "מלכודת : הנוסחה של השורה על המפה"
    המינימום של ארבעת הקירות הישרים (למעלה, למטה, משמאל ומימין) מתעלם ממסלולים
    מפותלים. במפה של סעיף ב הוא נותן 13 במקום 8, כי המים בורחים דרך התא בגובה 2 בשפה.

??? trap "מלכודת : לדחוף לערימה את גובה הקרקע"
    שכן שהתמלא צריך להיכנס לערימה בגובה פני המים, \( \max(\text{level}, h) \). מי
    שדוחף את \( h \) עצמו גורם לשכנים שלו "לברוח" דרך תא שבעצם מלא מים. במפה של סעיף ב
    הגרסה הזו מחזירה 1 במקום 8.

??? trap "מלכודת : מקרי קצה"
    מערך ריק או באורך 1 או 2 : אין מים. מפה עם שורה אחת או שתיים, או עמודה אחת או שתיים :
    כל התאים בשפה, ואין מים. עמודים בגובה שווה לאורך כל השורה : אין מים.

??? followup "שאלות המשך"
    - **שמונה כיוונים :** אם המים זורמים גם באלכסון, מה משתנה?

        ??? fu-answer "תשובה"
            רק רשימת השכנים, ל-8. ההצפה מבחוץ עם הערימה נשארת נכונה, כי היא לא תלויה בצורת
            השכנות.

    - **גבהים קטנים :** הגבהים שלמים עד \( H \). אפשר לוותר על הערימה?

        ??? fu-answer "תשובה"
            כן : מחליפים אותה ב-\( H + 1 \) תורים, אחד לכל גובה. פני המים שמוציאים לא יורדים, ולכן
            עוברים על התורים פעם אחת, בזמן \( O(mn + H) \). זה גם מימוש נוח בחומרה.

    - **איפה המים :** איך מחזירים את עומק המים בכל תא, ולא רק את הסכום?

        ??? fu-answer "תשובה"
            שומרים במטריצה את המים של כל שכן, \( \max(\text{level}, h) - h \), במקום לסכום אותם.
            התיבה של סעיף ב מציגה את המטריצה הזו.
