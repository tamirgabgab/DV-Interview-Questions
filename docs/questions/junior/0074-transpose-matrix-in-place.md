---
id: 74
title: שחלוף מטריצה במקום – סיבוב ב-90°, מטריצה לא ריבועית ובלי סימון
level: junior
difficulty: hard
kind: code
tags: [algorithms, permutations, matrices, python, systemverilog]
source: "שאלה מוכרת בראיונות קוד (rotate image, in-place transpose), עם ההכללה למטריצה לא ריבועית"
added: 2026-11-01
---

## השאלה

מטריצות שמורות בזיכרון **שורה אחרי שורה** (row-major) : המטריצה \( m \times n \) היא מערך אחד באורך
\( mn \), והאיבר \( (i, j) \) נמצא באינדקס \( i n + j \). הכול צריך לקרות **במקום**, בלי מערך עזר בגודל
המטריצה.

- **סעיף א – סיבוב תמונה :** סובבו תמונה \( n \times n \) ברבע סיבוב בכיוון השעון.
- **סעיף ב – שחלוף לא ריבועי :** מטריצה \( m \times n \) שמורה במערך באורך \( mn \). אחרי הפעולה המערך
  צריך להכיל את \( A^T \), מטריצה \( n \times m \), שורה אחרי שורה. מותר זיכרון של ביט אחד לכל איבר.
- **סעיף ג – בלי סימון :** אותו שחלוף, עם זיכרון נוסף \( O(1) \) בלבד.

לדוגמה, ‏\( 2 \times 3 \) עם השורות \( a\,b\,c \) ו-\( d\,e\,f \) שמורה כ-\( [a, b, c, d, e, f] \). השחלוף שלה, ‏\( 3 \times 2 \),
עם השורות \( a\,d \), ‏\( b\,e \) ו-\( c\,f \), שמור כ-\( [a, d, b, e, c, f] \).

??? interviewer "מה המראיין בודק"
    - **מיפוי אינדקסים :** האם המועמד כותב לאן עובר כל אינדקס, במקום לחשוב על שורות ועמודות.
    - **פירוק לפעולות פשוטות :** האם הוא רואה שסיבוב הוא שחלוף והיפוך.
    - **תמורות ומעגלים :** האם הוא מבין שבמטריצה לא ריבועית אין זוגות להחליף, אלא מעגלים ארוכים.
    - **זיכרון מול זמן :** מה עולה לוותר על הסימון, וכמה.
    - **מקרי קצה :** שורה אחת, עמודה אחת, ושני האיברים הקבועים בקצוות.

---

### סעיף א – סיבוב תמונה

??? tip "רמז 1"
    לאן עובר האיבר \( (i, j) \) ברבע סיבוב בכיוון השעון? כתבו את זה לתמונה \( 3 \times 3 \).

??? tip "רמז 2"
    ‏\( (i, j) \to (j, n - 1 - i) \). אילו שתי פעולות פשוטות, כל אחת במקום, נותנות את זה?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **שחלוף, ואז היפוך של כל שורה.** השחלוף שולח \( (i, j) \) ל-\( (j, i) \), וההיפוך שולח \( (j, i) \)
        ל-\( (j, n - 1 - i) \), וזה בדיוק רבע סיבוב בכיוון השעון. שתי הפעולות הן החלפות, במקום, ב-\( O(n^2) \).

    <!-- cost: זמן \( O(n^2) \) | זיכרון \( O(1) \) | בערך n² החלפות -->

    #### הרעיון { .sol-idea }

    **לאן הולך כל איבר.** ברבע סיבוב בכיוון השעון, השורה העליונה נהיית העמודה הימנית : ‏\( (i, j) \to (j, n - 1 - i) \).
    במקום לבנות את זה ישירות, מפרקים לשתי פעולות שכל אחת מהן היא **זוגות** של החלפות :

    <!-- gen 0 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="תמונה 3 על 3 : המקורית, אחרי שחלוף (האלכסון לא זז), ואחרי היפוך של כל שורה, סיבוב של רבע סיבוב בכיוון השעון"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>0</td><td>1</td><td>2</td><td></td><td>0</td><td>1</td><td>2</td><td></td><td>0</td><td>1</td><td>2</td></tr><tr><th dir="rtl">שורה 0</th><td class="pm-c c1">a</td><td class="pm-c c1">b</td><td class="pm-c c1">c</td><td class="pm-c is-gap"></td><td class="pm-c c3">a</td><td class="pm-c c2">d</td><td class="pm-c c2">g</td><td class="pm-c is-gap"></td><td class="pm-c c1">g</td><td class="pm-c c1">d</td><td class="pm-c c1">a</td></tr><tr><th dir="rtl">שורה 1</th><td class="pm-c c1">d</td><td class="pm-c c1">e</td><td class="pm-c c1">f</td><td class="pm-c is-gap"></td><td class="pm-c c2">b</td><td class="pm-c c3">e</td><td class="pm-c c2">h</td><td class="pm-c is-gap"></td><td class="pm-c c1">h</td><td class="pm-c c1">e</td><td class="pm-c c1">b</td></tr><tr><th dir="rtl">שורה 2</th><td class="pm-c c1">g</td><td class="pm-c c1">h</td><td class="pm-c c1">i</td><td class="pm-c is-gap"></td><td class="pm-c c2">c</td><td class="pm-c c2">f</td><td class="pm-c c3">i</td><td class="pm-c is-gap"></td><td class="pm-c c1">i</td><td class="pm-c c1">f</td><td class="pm-c c1">c</td></tr></tbody></table></div>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שחלוף :** לכל \( i < j \), מחליפים את \( (i, j) \) ו-\( (j, i) \). האלכסון נשאר. ‏\( n(n-1)/2 \) החלפות.
    2. **היפוך של כל שורה :** מחליפים את \( (i, j) \) ו-\( (i, n - 1 - j) \). ‏\( n \lfloor n/2 \rfloor \) החלפות.
    3. **נגד כיוון השעון :** שחלוף, ואז היפוך של **סדר השורות** במקום היפוך של כל שורה : ‏\( (i, j) \to (n - 1 - j, i) \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="rotate90" linenums="1" hl_lines="6 8"
        def rotate90(a: list) -> None:
            """Rotate an n x n matrix (a list of rows) a quarter turn clockwise, in place."""
            n = len(a)
            for i in range(n):
                for j in range(i + 1, n):          # (1)!
                    a[i][j], a[j][i] = a[j][i], a[i][j]
            for row in a:
                row.reverse()
        ```

        1. רק מעל האלכסון. לולאה על כל \( j \) מחליפה כל זוג פעמיים, והמטריצה חוזרת למקומה.

    === "SystemVerilog"
        ```systemverilog title="function rotate90" linenums="1" hl_lines="6 11"
        // rotate an n x n matrix, stored row by row in a, a quarter turn clockwise
        function automatic void rotate90(ref int a[], input int n);
          int t;
          for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) begin
              t = a[i*n + j]; a[i*n + j] = a[j*n + i]; a[j*n + i] = t;
            end
          for (int i = 0; i < n; i++)
            for (int j = 0; j < n / 2; j++) begin
              t = a[i*n + j];
              a[i*n + j] = a[i*n + n - 1 - j];
              a[i*n + n - 1 - j] = t;
            end
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    השחלוף שולח את הערך שב-\( (i, j) \) ל-\( (j, i) \), וההיפוך של השורה \( j \) שולח אותו ל-\( (j, n - 1 - i) \).
    בדיקה על הפינות : ‏\( (0, 0) \to (0, n - 1) \), הפינה השמאלית העליונה עוברת לימנית העליונה, כמו ברבע
    סיבוב בכיוון השעון.

    **החלופה :** סיבוב "בשכבות", ארבעה איברים בכל פעם (‏\( (i,j) \to (j, n-1-i) \to \dots \)). הוא כותב
    פחות, אבל קל יותר לטעות בו באינדקסים :

    | השיטה | כמה כותבים | ב-\( n = 100 \) |
    |:-:|:-:|:-:|
    | שחלוף והיפוך | כ-\( n^2 \) החלפות, 3 השמות בכל אחת | ‏29,850 השמות |
    | שכבות | ‏5 השמות לכל 4 איברים, כ-\( 1.25 n^2 \) | ‏12,500 השמות |

---

### סעיף ב – שחלוף לא ריבועי

??? tip "רמז 1"
    בריבוע, \( (i, j) \) ו-\( (j, i) \) מחליפים מקום. מה קורה במטריצה \( 2 \times 3 \)? כתבו לאן עובר כל אחד
    מששת האינדקסים.

??? tip "רמז 2"
    כתבו את המקום הישן \( k = i n + j \) ואת החדש \( k' = j m + i \). מה יוצא מ-\( k \cdot m \) מודולו
    \( mn - 1 \)?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        הערך באינדקס \( k \) עובר לאינדקס \( k m \bmod (mn - 1) \), חוץ מ-\( 0 \) ומ-\( mn - 1 \), שלא זזים. זו
        תמורה, ומבצעים אותה **מעגל אחרי מעגל** : לוקחים ערך "ביד", מניחים אותו במקום שלו ומרימים את
        מה שהיה שם, עד שחוזרים להתחלה. ביט "בוצע" לכל אינדקס מונע מעבר כפול על אותו מעגל.

    <!-- cost: זמן \( O(mn) \) | זיכרון ביט לכל איבר -->

    #### הרעיון { .sol-idea }

    **אין זוגות, יש מעגלים.** ב-\( 2 \times 3 \) הערך מאינדקס 1 עובר ל-2, משם ל-4, ל-3 ובחזרה ל-1 :

    <!-- gen 1 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="המטריצה 2 על 3 בזיכרון לפני השחלוף ואחריו, כל ערך צבוע לפי המעגל של המקום שלו"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr><tr><th dir="rtl">לפני</th><td class="pm-c c1">a</td><td class="pm-c c2">b</td><td class="pm-c c2">c</td><td class="pm-c c2">d</td><td class="pm-c c2">e</td><td class="pm-c c3">f</td></tr><tr><th dir="rtl">אחרי</th><td class="pm-c c1">a</td><td class="pm-c c2">d</td><td class="pm-c c2">b</td><td class="pm-c c2">e</td><td class="pm-c c2">c</td><td class="pm-c c3">f</td></tr></tbody></table></div>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="pm-key-c1"></i>‏0 לא זז</span><span><i class="pm-key-c2"></i>המעגל <span dir="ltr">1 → 2 → 4 → 3 → 1</span></span><span><i class="pm-key-c3"></i>‏5 לא זז</span></span>

    <!-- /gen -->

    ביד, צעד אחרי צעד : מרימים את `b` מאינדקס 1, וכל ערך שמונח מפנה את המקום לערך הבא. ארבע
    כתיבות, ואף ערך לא נדרס :

    <!-- gen 4 -->

    | הצעד | ביד | מניחים באינדקס | מרימים משם |
    |:-:|:-:|:-:|:-:|
    | ‏1 | ‏`b` | ‏2 | ‏`c` |
    | ‏2 | ‏`c` | ‏4 | ‏`e` |
    | ‏3 | ‏`e` | ‏3 | ‏`d` |
    | ‏4 | ‏`d` | ‏1 | כלום, המעגל נסגר |

    <!-- /gen -->

    ככל שהמטריצה גדלה, המעגלים מתארכים. ב-\( 3 \times 5 \) יש שני מעגלים באורך 6, ושלושה מקומות שלא זזים :

    <!-- gen 3 -->

    | המעגל | המקומות, לאן כל ערך עובר | האורך |
    |:-:|:-:|:-:|
    | ‏1 | ‏`0` | ‏1 |
    | ‏2 | ‏`1 → 3 → 9 → 13 → 11 → 5 → 1` | ‏6 |
    | ‏3 | ‏`2 → 6 → 4 → 12 → 8 → 10 → 2` | ‏6 |
    | ‏4 | ‏`7` | ‏1 |
    | ‏5 | ‏`14` | ‏1 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הנוסחה :** ‏\( k = i n + j \) עובר ל-\( k' = j m + i \), ו-\( k' = k m \bmod (mn - 1) \) לכל \( 0 < k < mn - 1 \).
    2. **התחלת מעגל :** לכל \( s \) מ-1 עד \( mn - 2 \) שעוד לא בוצע, מרימים את \( a[s] \) "ביד".
    3. **הנחה והרמה :** ‏\( k \leftarrow k m \bmod (mn - 1) \). מחליפים את מה שביד עם \( a[k] \), ומסמנים את \( k \).
    4. **סוף המעגל :** כש-\( k \) חוזר ל-\( s \), הערך האחרון מונח במקום שהתפנה בתחילת המעגל. ביד נשאר
       רק עותק של \( a[s] \) הישן, שכבר הונח בצעד הראשון, ואין מה לעשות בו.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="transpose" linenums="1" hl_lines="6 12 13 14"
        def transpose(a: list, m: int, n: int) -> None:
            """a holds an m x n matrix row by row; afterwards it holds the n x m transpose."""
            size = m * n
            if size <= 2:
                return
            done = [False] * size                  # (1)!
            for s in range(1, size - 1):
                if done[s]:
                    continue
                k, carry = s, a[s]
                while True:
                    k = k * m % (size - 1)         # (2)!
                    a[k], carry = carry, a[k]
                    done[k] = True
                    if k == s:
                        break
        ```

        1. ביט לכל איבר : ‏\( mn \) ביטים, הרבה פחות ממערך עזר של \( mn \) ערכים, אבל לא \( O(1) \).
        2. המקום שאליו הולך הערך שביד. ב-\( k = s \) המעגל נסגר.

    === "SystemVerilog"
        ```systemverilog title="function transpose" linenums="1" hl_lines="7 15 16 17"
        // a holds an m x n matrix row by row; afterwards it holds the n x m transpose
        function automatic void transpose(ref int a[], input int m, input int n);
          int size = m * n;
          int k, carry, t;
          bit done[];
          if (size <= 2) return;
          done = new[size];
          for (int s = 1; s < size - 1; s++) begin
            if (done[s]) continue;
            k = s;
            carry = a[s];
            forever begin
              k = (k * m) % (size - 1);         // (1)!
              t = a[k];
              a[k] = carry;
              carry = t;
              done[k] = 1;
              if (k == s) break;
            end
          end
        endfunction
        ```

        1. המכפלה `k * m` מחושבת ב-`int` של 32 ביט, וזה מספיק עד מטריצה ריבועית של
           <span dir="ltr">1290×1290</span>. למטריצה גדולה יותר מחשבים ב-`longint` (ראו את המלכודת על הגלישה).

    #### למה זה נכון { .sol-proof }

    **הנוסחה.** נכתוב \( k = i n + j \) ונכפיל ב-\( m \) : ‏\( k m = i \cdot mn + j m \). מודולו \( mn - 1 \), ‏\( mn \equiv 1 \), ולכן
    \( k m \equiv i + j m \). נשאר לבדוק ש-\( i + j m \) כבר קטן מהמודולוס : ‏\( i \le m - 1 \) ו-\( j \le n - 1 \), ולכן
    \( i + j m \le mn - 1 \), עם שוויון רק באיבר האחרון. לכן לכל \( k \ne mn - 1 \) זה בדיוק \( k' \). האינדקסים 0
    ו-\( mn - 1 \) הם האיבר הראשון והאחרון, ושם השחלוף לא מזיז כלום.

    **המעגלים.** ‏\( m \) זר ל-\( mn - 1 \) (כל מחלק משותף מחלק גם את \( m \cdot n - (mn - 1) = 1 \)), ולכן ההכפלה
    ב-\( m \) היא תמורה של \( 1, \dots, mn - 2 \). כל ערך מונח פעם אחת, והביט שלו מסומן, ולכן כל מעגל מבוצע
    בדיוק פעם אחת : ‏\( mn - 2 \) הנחות, אחת לכל אינדקס חוץ מהראשון ומהאחרון.

---

### סעיף ג – בלי סימון

??? tip "רמז 1"
    בלי ביט "בוצע", איך יודעים אם \( s \) שייך למעגל שכבר הוזז? מה מיוחד באינדקס הקטן ביותר של כל
    מעגל?

??? tip "רמז 2"
    מה אפשר לבדוק על \( s \) בהליכה אחת במעגל שלו, בלי לכתוב שום דבר למערך?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        מבצעים כל מעגל רק מה**מנהיג** שלו, האינדקס הקטן ביותר בו. לכל \( s \) הולכים במעגל : אם פוגשים
        אינדקס קטן מ-\( s \), המעגל כבר בוצע מהמנהיג שלו ומדלגים. אם חוזרים ל-\( s \), זה המנהיג, ומבצעים.
        זיכרון \( O(1) \). הזמן גדל : לכל היותר \( O((mn)^2) \), ובמדידה לא יותר מ-15 צעדי הליכה לכל איבר.

    <!-- cost: זמן \( O((mn)^2) \) לכל היותר | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **זיכרון בתמורה לזמן.** הביט של סעיף ב עונה על שאלה אחת : "האם המעגל של \( s \) כבר בוצע?". בלעדיו
    עונים עליה בהליכה. ההליכה עולה, אבל היא נעצרת מוקדם ברוב המקרים, ברגע שהיא פוגשת אינדקס קטן יותר.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **לכל \( s \) מ-1 עד \( mn - 2 \) :** מתחילים מ-\( k = s m \bmod (mn - 1) \).
    2. **הליכה :** כל עוד \( k > s \), ממשיכים : ‏\( k \leftarrow k m \bmod (mn - 1) \).
    3. **ההחלטה :** אם ההליכה נעצרה ב-\( k < s \), ‏\( s \) לא המנהיג, ומדלגים. אם ב-\( k = s \), זה המנהיג.
    4. **הביצוע :** כמו בסעיף ב, בלי הסימון.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="transpose_no_marks" linenums="1" hl_lines="7 8 9 10"
        def transpose_no_marks(a: list, m: int, n: int) -> None:
            """The transpose of transpose(), with O(1) extra memory: each cycle from its leader."""
            size = m * n
            if size <= 2:
                return
            for s in range(1, size - 1):
                k = s * m % (size - 1)
                while k > s:                       # (1)!
                    k = k * m % (size - 1)
                if k < s:
                    continue                       # (2)!
                k, carry = s, a[s]
                while True:
                    k = k * m % (size - 1)
                    a[k], carry = carry, a[k]
                    if k == s:
                        break
        ```

        1. ההליכה במעגל של \( s \). היא נגמרת, כי המעגל חוזר ל-\( s \).
        2. במעגל יש אינדקס קטן מ-\( s \), והוא כבר ביצע את המעגל.

    === "SystemVerilog"
        ```systemverilog title="function transpose_no_marks" linenums="1" hl_lines="7 8 9 10"
        // the transpose of transpose(), with O(1) extra memory: each cycle from its leader
        function automatic void transpose_no_marks(ref int a[], input int m, input int n);
          int size = m * n;
          int k, carry, t;
          if (size <= 2) return;
          for (int s = 1; s < size - 1; s++) begin
            k = (s * m) % (size - 1);
            while (k > s) k = (k * m) % (size - 1);
            if (k < s) continue;
            k = s;
            carry = a[s];
            forever begin
              k = (k * m) % (size - 1);
              t = a[k];
              a[k] = carry;
              carry = t;
              if (k == s) break;
            end
          end
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **כל מעגל מבוצע פעם אחת.** לכל מעגל יש מנהיג אחד בדיוק, האינדקס הקטן ביותר בו. ההליכה מ-\( s \)
    נעצרת ב-\( k = s \) רק אם אין במעגל אינדקס קטן מ-\( s \), כלומר רק מהמנהיג.

    **למה מותר לדלג באמצע הריצה.** ההליכה קוראת רק אינדקסים, לא ערכים. לכן מה שכבר הוזז במערך לא
    משנה אותה, והתשובה לשאלה "האם \( s \) מנהיג" זהה לפני הריצה, באמצעה ואחריה.

    **הזמן.** ההליכה מ-\( s \) עולה לכל היותר את אורך המעגל, ולכן \( O((mn)^2) \) הוא חסם עליון. לא הראינו
    מטריצה שמגיעה אליו : ההליכה נעצרת ברגע שהיא פוגשת אינדקס קטן מ-\( s \), ובדרך כלל זה קורה מהר. במדידה
    על כל המידות מ-<span dir="ltr">2×2</span> עד <span dir="ltr">120×120</span>, היחס הגדול ביותר הוא 14.9 צעדי הליכה לאיבר,
    ב-<span dir="ltr">98×78</span>. מספר ההנחות הוא \( mn - 2 \) עם סימון ובלעדיו, וההבדל הוא רק בעמודה האחרונה :

    <!-- gen 5 -->

    | המטריצה | ‏mn | מעגלים שזזים | מקומות שלא זזים | הנחות | צעדים בחיפוש המנהיגים |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏<span dir="ltr">2×3</span> | ‏6 | ‏1 | ‏2 | ‏4 | ‏9 |
    | ‏<span dir="ltr">3×5</span> | ‏15 | ‏2 | ‏3 | ‏13 | ‏33 |
    | ‏<span dir="ltr">8×12</span> | ‏96 | ‏10 | ‏2 | ‏94 | ‏285 |
    | ‏<span dir="ltr">64×48</span> | ‏3072 | ‏20 | ‏2 | ‏3070 | ‏20666 |
    | ‏<span dir="ltr">100×37</span> | ‏3700 | ‏516 | ‏10 | ‏3698 | ‏10244 |

    <!-- /gen -->

    **נסו בעצמכם.** התיבה מוסיפה לטבלאות את הסדר : הנחה אחרי הנחה, ובלי סימון גם את ההליכות
    שנכשלות ומדלגים עליהן.

    - השאירו <span dir="ltr">2×3</span> ולחצו "הצעד הבא" ארבע פעמים : 1 מונח באינדקס 2, אחריו 2 ב-4, 4 ב-3 ו-3 ב-1,
      והמעגל נסגר. זה כל השחלוף.
    - בחרו <span dir="ltr">4×4</span> : שישה מעגלים באורך 2, כל אחד נסגר אחרי שתי הנחות. אלה ההחלפות של סעיף א.
      עכשיו <span dir="ltr">2×7</span> : מעגל אחד באורך 12.
    - עברו ל"בלי סימון" ב-<span dir="ltr">3×5</span>. ההליכה מ-<span dir="ltr">s = 3</span> עוברת ב-9, 13, 11, 5 ונעצרת
      ב-1 : חמישה צעדים, ומדלגים. "עד הסוף" מראה אותן 13 הנחות ועוד 33 צעדי הליכה, וב-<span dir="ltr">6×8</span>
      יש 46 הנחות ו-160 צעדים.

    <div class="explorer" data-kind="transpose" data-m="2" data-n="3" data-method="marks"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לולאה על כל הזוגות"
    בריבוע, לולאה על כל \( i, j \) (ולא רק \( i < j \)) מחליפה כל זוג פעמיים, והמטריצה חוזרת. במטריצה
    לא ריבועית החלפות של \( (i, j) \) ו-\( (j, i) \) לא מוגדרות בכלל, כי הצורה משתנה.

??? trap "מלכודת : ‏mn − 1 והקצוות"
    הנוסחה \( k m \bmod (mn - 1) \) שולחת את \( mn - 1 \) ל-0, ולכן מריצים את הלולאה רק על \( 1, \dots, mn - 2 \).
    ובמטריצה של איבר אחד או שניים, ‏\( mn - 1 \le 1 \) : באיבר אחד מחלקים באפס, ובשניים כל אינדקס הולך
    ל-0. שם אין מה להזיז, ולכן הקוד חוזר מיד כש-`size <= 2`.

??? trap "מלכודת : גלישה ב-k · m"
    ‏\( k \cdot m \) מגיע כמעט ל-\( m^2 n \). ב-int של 32 ביט עם סימן, מטריצה ריבועית גולשת החל
    מ-<span dir="ltr">1291×1291</span>, כי \( 1291^3 > 2^{31} \). זה גם הגבול של קוד ה-SystemVerilog שבעמוד, שמחשב
    `k * m` ב-`int`. ב-SV וב-C כדאי לחשב ב-64 ביט, או להשתמש בצעד ההפוך (‏\( k \to k n \bmod (mn - 1) \))
    כשהוא קטן יותר.

??? followup "שאלות המשך"
    - **נגד כיוון השעון :** איך מסובבים רבע סיבוב נגד כיוון השעון? וחצי סיבוב?

        ??? fu-answer "תשובה"
            נגד : שחלוף ואז היפוך סדר השורות (או היפוך כל שורה ואז שחלוף). חצי סיבוב : היפוך של כל
            המערך השטוח, \( k \to n^2 - 1 - k \).

    - **הצעד ההפוך :** לאן הולכים בכיוון ההפוך של המעגל?

        ??? fu-answer "תשובה"
            ‏\( k \to k n \bmod (mn - 1) \), כי \( m n \equiv 1 \) : ההכפלה ב-\( n \) הופכת את ההכפלה ב-\( m \). אפשר
            לבצע את המעגל גם בכיוון הזה, עם "חור" במקום "יד".

    - **‏cache :** למה שחלוף פשוט (‏`b[j][i] = a[i][j]`) איטי במטריצות גדולות, ומה עוזר?

        ??? fu-answer "תשובה"
            הכתיבה קופצת בצעדים של \( m \), וכל גישה היא שורת cache אחרת. עוזר לשחלף בבלוקים של
            \( B \times B \) שנכנסים ל-cache, ואז לשחלף את הבלוקים.

    - **בחומרה :** ‏DMA צריך להפוך תמונה משורות לעמודות. איך עושים את זה בזרם, איבר אחד בכל מחזור?
      ואיך מאמתים?

        ??? fu-answer "תשובה"
            שני זיכרונות, כל אחד בגודל של תמונה שלמה (‏\( mn \) מילים), ב-ping-pong. את התמונה שנכנסת
            כותבים לאחד לפי הסדר, ובאותו זמן קוראים את הקודמת מהשני לפי עמודות, בכתובת \( i n + j \).
            מונה הקריאה מוסיף \( n \) בכל מחזור, ובסוף עמודה עובר ל-\( j + 1 \), בלי מכפל :

            <!-- gen 6 -->

            <svg class="figure tp-hw" viewBox="0 0 470 200" direction="ltr" style="max-width:29.375rem" role="img" aria-label="תרשים המלבנים של משחלף בזרם : מונה הכתיבה wr_addr סופר 0, 1, 2 וכותב את התמונה שנכנסת לזיכרון אחד, ומונה הקריאה rd_addr עובר על האינדקסים i·n + j, עמודה אחרי עמודה, וקורא את התמונה הקודמת מהזיכרון השני. ‏mux בוחר את הזיכרון שנקרא ומוציא את dout. בכל תמונה שני הזיכרונות מתחלפים בתפקידים"><defs><marker id="tp-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="tp-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs><g class="tp-blk"><rect x="10" y="16" width="130" height="52" rx="5"/><text x="75" y="39" text-anchor="middle">wr_addr</text><text class="tp-sub" x="75" y="57" text-anchor="middle">0, 1, 2, …</text></g><g class="tp-blk"><rect x="10" y="132" width="130" height="52" rx="5"/><text x="75" y="155" text-anchor="middle">rd_addr</text><text class="tp-sub" x="75" y="173" text-anchor="middle">i·n + j</text></g><g class="tp-blk"><rect x="200" y="16" width="110" height="52" rx="5"/><text x="255" y="39" text-anchor="middle">RAM A</text><text class="tp-sub" x="255" y="57" text-anchor="middle">mn</text></g><g class="tp-blk"><rect x="200" y="132" width="110" height="52" rx="5"/><text x="255" y="155" text-anchor="middle">RAM B</text><text class="tp-sub" x="255" y="173" text-anchor="middle">mn</text></g><g class="tp-blk"><rect x="368" y="74" width="54" height="52" rx="5"/><text x="395" y="105" text-anchor="middle">mux</text></g><path class="tp-wire" d="M140,34 L200,34" marker-end="url(#tp-hb)"/><path class="tp-wire" d="M140,166 L200,166" marker-end="url(#tp-hb)"/><path class="tp-wire" d="M310,42 L340,42 L340,88 L368,88" marker-end="url(#tp-hb)"/><path class="tp-wire" d="M310,158 L340,158 L340,112 L368,112" marker-end="url(#tp-hb)"/><path class="tp-wire" d="M422,100 L462,100" marker-end="url(#tp-hb)"/><path class="tp-wire tp-swap" d="M140,54 L200,146" marker-end="url(#tp-hb)"/><path class="tp-wire tp-swap" d="M140,146 L200,54" marker-end="url(#tp-hb)"/><text class="tp-wlab" x="170" y="26" text-anchor="middle">din</text><text class="tp-wlab" x="442" y="90" text-anchor="middle">dout</text></svg>

            <span class="viz-legend"><span><i class="tp-key-now"></i>התמונה הזו : כותבים ל-A וקוראים מ-B</span><span><i class="tp-key-swap"></i>התמונה הבאה : התפקידים מתחלפים</span></span>

            <!-- /gen -->

            בתמונה של <span dir="ltr">2×3</span>, האיברים `a` עד `f` כבר ב-B, והתמונה הבאה, `g` עד `l`, נכנסת ל-A :

            <!-- gen 7 -->

            | המחזור | ‏wr_addr, ל-A | ‏din | ‏rd_addr, מ-B | ‏dout |
            |:-:|:-:|:-:|:-:|:-:|
            | ‏6 | ‏0 | ‏`g` | ‏0 | ‏`a` |
            | ‏7 | ‏1 | ‏`h` | ‏3 | ‏`d` |
            | ‏8 | ‏2 | ‏`i` | ‏1 | ‏`b` |
            | ‏9 | ‏3 | ‏`j` | ‏4 | ‏`e` |
            | ‏10 | ‏4 | ‏`k` | ‏2 | ‏`c` |
            | ‏11 | ‏5 | ‏`l` | ‏5 | ‏`f` |

            <!-- /gen -->

            זיכרון סינכרוני מוציא את `dout` מחזור אחד אחרי הכתובת. **אימות :** המודל הוא ההגדרה, האיבר
            \( (i, j) \) יוצא במקום \( (j, i) \). הצורות שחייבים לכסות הן שורה אחת, עמודה אחת, ריבוע, ושתי
            תמונות רצופות, כדי לראות שהזיכרונות מתחלפים.
