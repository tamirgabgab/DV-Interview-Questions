---
id: 13
title: ממיינים ספרות ומחסרים – ארבע ספרות
level: junior
difficulty: medium
tags: [math, digits, sorting, python, systemverilog]
source: "Kaprekar's routine (4 digits)"
added: 2026-10-16
---

## השאלה

!!! info "גרסה קשה יותר של שאלה 0012"
    זו אותה שאלה כמו [ממיינים ספרות ומחסרים](../student/0012-sort-digits-and-subtract.md),
    אבל עם ארבע ספרות במקום שלוש. הקוד כמעט זהה, וההוכחה מסובכת יותר.

נתון מספר שלם `x` בין 0 ל-9999. כותבים אותו **בדיוק עם 4 ספרות**, ומשלימים אפסים משמאל
לפי הצורך : 95 נכתב 0095, ו-7 נכתב 0007. מהספרות האלה בונים שני מספרים :

- **מהגדול לקטן :** הספרות ממוינות בסדר יורד.
- **מהקטן לגדול :** הספרות ממוינות בסדר עולה.

מחסרים את הקטן מהגדול. אם ההפרש יוצא בדיוק `x`, המספר `x` נקרא **מיוחד**.

| המספר `x` | מהגדול לקטן | מהקטן לגדול | ההפרש | מיוחד? |
|---|---|---|---|---|
| 3524 | 5432 | 2345 | 3087 | ✗ |
| 95 | 9500 | 0059 | 9441 | ✗ |
| 1000 | 1000 | 0001 | 0999 | ✗ |
| 7777 | 7777 | 7777 | 0 | ✗ |
| 0 | 0000 | 0000 | 0 | ✓ |

??? interviewer "מה המראיין בודק"
    - **אפסים משלימים :** האם זוכרים ש-95 הוא 0095. בלי זה ההפרש הוא \( 95 - 59 \) במקום
      \( 9500 - 0059 \), וכל התוצאה משתבשת.
    - **מיון של ארבעה ערכים :** אפשר ב-`sort` של השפה, אבל בשאלה על חומרה מצפים לרשת
      השוואות קבועה. כמה משווים צריך, ובכמה שכבות?
    - **לצמצם את החיפוש :** האם באמת צריך לבדוק את כל 10,000 המספרים, או שההוכחה מצמצמת
      את המועמדים לקומץ שאפשר לעבור עליו ביד?
    - **ספרות של הפרש :** איך מוצאים את הספרות של ההפרש בלי לנחש, מתוך הספרות של המספר
      המקורי בלבד.
    - **ניתוח מקרים מסודר :** להסביר למה המקרים מכסים הכול, ולא רק לנסות דוגמאות עד
      שמשהו עובד.

---

### סעיף א – לבדוק מספר אחד

כתבו פונקציה שמקבלת את `x` ומחזירה 1 אם הוא מיוחד, ו-0 אחרת.

??? tip "רמז 1"
    כמו בשלוש ספרות : מפרקים בעזרת חלוקה ושארית ב-10, ממיינים, ובונים את שני המספרים מאותן
    ספרות בשני סדרים הפוכים.

??? tip "רמז 2"
    השאלה היחידה היא איך ממיינים ארבעה ערכים בלי לולאה. נסו קודם למיין שני זוגות בנפרד :
    מה אפשר לומר על שני המנצחים ועל שני המפסידים?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מפרקים לארבע ספרות (האפסים המשלימים מתקבלים לבד), ממיינים אותן ברשת של **חמש
        השוואות**, בונים מהן את הגדול ואת הקטן, ומחזירים 1 אם ההפרש שווה ל-`x`.

    #### הרעיון { .sol-idea }

    בדיוק כמו בשלוש ספרות : שני המספרים בנויים מאותן ארבע ספרות, ולכן מספיק למיין פעם
    אחת. ההבדל היחיד הוא רשת המיון, שצריכה חמש השוואות במקום שלוש.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **לפרק :** הספרות הן `x / 1000`, `(x / 100) % 10`, `(x / 10) % 10` ו-`x % 10`.
       האפסים המשלימים מתקבלים לבד : עבור 95 יוצא 0, 0, 9, 5.
    2. **למיין :** את ארבע הספרות בסדר יורד, \( a \ge b \ge c \ge d \).
    3. **להרכיב :** הגדול הוא \( 1000a + 100b + 10c + d \) והקטן הוא
       \( 1000d + 100c + 10b + a \).
    4. **להשוות :** את ההפרש ל-`x`.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function is_special_4" linenums="1" hl_lines="8 9 10"
        function automatic bit is_special_4(int x);
          int a = x / 1000, b = (x / 100) % 10, c = (x / 10) % 10, d = x % 10;   // (1)!
          int largest, smallest;

          // Sorting network for 4 values, descending: a >= b >= c >= d
          if (a < b) {a, b} = {b, a};     // two separate pairs (2)
          if (c < d) {c, d} = {d, c};
          if (a < c) {a, c} = {c, a};     // a = largest of all four (3)
          if (b < d) {b, d} = {d, b};     // d = smallest of all four (4)
          if (b < c) {b, c} = {c, b};     // order the middle two (5)

          largest  = 1000 * a + 100 * b + 10 * c + d;
          smallest = 1000 * d + 100 * c + 10 * b + a;   // (6)!
          return largest - smallest == x;
        endfunction
        ```

        1. חלוקה שלמה ושארית מפרקות את `x` לספרות. עבור `x = 95` מתקבל `a = 0`, `b = 0`,
           `c = 9`, `d = 5`, בדיוק כמו 0095. לא צריך טיפול מיוחד במספרים קטנים.
        2. שתי ההשוואות הראשונות ממיינות את הזוג `a`, `b` ואת הזוג `c`, `d` בנפרד. הן
           בלתי תלויות, ולכן בחומרה הן באותה שכבה.
        3. השוואה בין שני המנצחים : הגדול מביניהם גדול מכל הארבעה, ועובר ל-`a`.
        4. השוואה בין שני המפסידים : הקטן מביניהם קטן מכל הארבעה, ועובר ל-`d`. גם היא
           בלתי תלויה בקודמת, ולכן השלישית והרביעית הן שכבה אחת.
        5. אחרי ארבע השוואות רק `b` ו-`c` עוד לא מסודרות זו מול זו. ההשוואה החמישית סוגרת
           את הרשת, ואי אפשר למיין ארבעה ערכים בפחות מחמש השוואות.
        6. אותן ספרות בסדר הפוך. בניגוד לשלוש ספרות, כאן אין ספרה שנשארת במקומה : גם
           `b` ו-`c` מתחלפות, וזה מה שמסבך את ההוכחה בסעיף ב.

        חמש השוואות מספיקות כדי למיין ארבעה ערכים :

        - **שתי השוואות ראשונות :** ממיינות את הזוג `a`, `b` ואת הזוג `c`, `d` בנפרד.
        - **השוואה שלישית :** בין שני המנצחים. המנצח הוא הגדול מכולם ועובר ל-`a`.
        - **השוואה רביעית :** בין שני המפסידים. המפסיד הוא הקטן מכולם ועובר ל-`d`.
        - **השוואה חמישית :** מסדרת את שני הערכים שנשארו באמצע.

        בחומרה זה מעגל צירופי של חמישה משווים בשלוש שכבות : את שתי ההשוואות הראשונות אפשר
        לעשות במקביל, וגם את השלישית והרביעית.

    === "Python"
        ```python title="is_special_4"
        def is_special_4(x: int) -> int:
            digits = sorted(f"{x:04d}")              # four digits, leading zeros included (1)
            smallest = int("".join(digits))           # ascending order
            largest = int("".join(reversed(digits)))  # descending order (2)
            return int(largest - smallest == x)
        ```

        1. ‏`f"{x:04d}"` מרפדת באפסים משמאל לארבע ספרות, ו-`sorted` על המחרוזת מחזירה
           רשימה של תווים בסדר עולה. מיון של ספרות כתווים זהה למיון שלהן כמספרים, כי כולן
           באותו אורך.
        2. ‏`reversed` הופכת את הסדר העולה ליורד, בלי מיון שני.

    #### סיבוכיות { .sol-cost }

    ‏\( O(1) \) : תמיד ארבע ספרות, חמש השוואות ושני מספרים להרכיב.

---

### סעיף ב – לבדוק את כל המספרים

מריצים את הפונקציה על כל המספרים מ-0 עד 9999, ושומרים במערך את אלה שהיא מחזירה עבורם 1.
מה יכיל המערך בסוף? הוכיחו.

??? tip "רמז 1"
    כתבו את ההפרש בעזרת הספרות הממוינות \( a \ge b \ge c \ge d \). הפעם ספרות האמצע לא
    מתבטלות, אבל ההפרש עדיין תלוי רק בשני מספרים. באילו? כמה הפרשים שונים יכולים לצאת?

??? tip "רמז 2"
    כדי לדעת מה הספרות של ההפרש, עשו את החיסור במאונך, כמו בבית הספר, עמודה אחרי עמודה
    עם "לווה". באילו עמודות תמיד צריך ללוות?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        המערך יכיל שני מספרים בלבד : **0 ו-6174**.

    #### הרעיון { .sol-idea }

    ההפרש תלוי רק בשני מספרים : המרחק \( p \) בין הספרה הגדולה לקטנה, והמרחק \( q \) בין
    שתי האמצעיות. לכן יש רק 55 הפרשים אפשריים, חיסור במאונך נותן את הספרות של כל אחד
    מהם, וניתוח מקרים משאיר רק את 0 ואת 6174.

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function find_special_4"
        function automatic void find_special_4(ref int special[$]);
          special.delete();   // (1)!
          for (int x = 0; x <= 9999; x++)
            if (is_special_4(x)) special.push_back(x);
        endfunction
        ```

        1. התור מגיע מהקורא (`ref`), ולכן מרוקנים אותו קודם : אחרת קריאה שנייה הייתה
           מוסיפה את התוצאות פעם נוספת.

    === "Python"
        ```python title="find_special_4"
        def find_special_4() -> list[int]:
            return [x for x in range(10000) if is_special_4(x)]
        ```

    בדיקה : הספרות של 6174 ממוינות הן 7, 6, 4, 1, ו-\( 7641 - 1467 = 6174 \).

    #### למה זה נכון { .sol-proof }

    <div class="steps" markdown>

    1. **ההפרש תלוי רק בשני מספרים.** נסמן את הספרות הממוינות \( a \ge b \ge c \ge d \).
       אז :

        \[
        \begin{aligned}
               & 1000a + 100b + 10c + d \\
        -\;    & (1000d + 100c + 10b + a) \\
        =\;    & 999(a - d) + 90(b - c)
        \end{aligned}
        \]

        נסמן :

        - **‏\( p = a - d \) :** המרחק בין הספרה הגדולה לקטנה.
        - **‏\( q = b - c \) :** המרחק בין שתי הספרות האמצעיות.

        ההפרש הוא \( 999p + 90q \). בשלוש ספרות הספרה האמצעית התבטלה, וכאן נשארים שני
        פרמטרים, ולכן ההוכחה ארוכה יותר. מכיוון ש-\( b \) ו-\( c \) נמצאות בין \( a \)
        ל-\( d \), מתקיים \( 0 \le q \le p \le 9 \). כלומר יש רק **55 הפרשים אפשריים**,
        ואם `x` מיוחד, הוא חייב להיות אחד מהם.

    2. **המקרה \( p = 0 \).** כל הספרות שוות וההפרש הוא 0. המספר היחיד מהצורה הזו
       שההפרש שלו שווה לו הוא 0 עצמו. למשל 7777 נותן הפרש 0, ולא 7777. מעכשיו
       \( p \ge 1 \).

    3. **הספרות של ההפרש.** מחסרים במאונך את \( \overline{dcba} \) מ-\( \overline{abcd} \),
       מהאחדות אל האלפים :

        | עמודה | החישוב | לווים? | הספרה שיוצאת |
        |---|---|---|---|
        | אחדות | ‏\( d - a = -p \), שלילי כי \( p \ge 1 \) | תמיד | ‏\( 10 - p \) |
        | עשרות | ‏\( c - b - 1 = -q - 1 \), תמיד שלילי | תמיד | ‏\( 9 - q \) |
        | מאות | ‏\( b - c - 1 = q - 1 \) | רק כש-\( q = 0 \) | ‏\( q - 1 \), או 9 כש-\( q = 0 \) |
        | אלפים | ‏\( a - d \) פחות הלווה מהמאות | אף פעם | ‏\( p \), או \( p - 1 \) כש-\( q = 0 \) |

        כלומר, מהאלפים לאחדות :

        - **כש-\( q \ge 1 \) :** הספרות של ההפרש הן \( p,\ q - 1,\ 9 - q,\ 10 - p \).
        - **כש-\( q = 0 \) :** הספרות של ההפרש הן \( p - 1,\ 9,\ 9,\ 10 - p \).

        דוגמה : עבור 0095 הספרות הממוינות הן 9, 5, 0, 0, ולכן \( p = 9 \) ו-\( q = 5 \).
        לפי הנוסחה הספרות הן 9, 4, 4, 1, וזה בדיוק \( 9500 - 0059 = 9441 \).

    4. **מה צריך להתקיים.** אם `x` מיוחד, `x` שווה להפרש, ולכן יש לו בדיוק את הספרות של
       ההפרש. אבל \( p \) ו-\( q \) חושבו מהספרות של `x`. לכן, כשממיינים את ארבע הספרות
       של ההפרש :

        - **תנאי א :** הגדולה פחות הקטנה שווה בדיוק \( p \).
        - **תנאי ב :** שתי האמצעיות רחוקות זו מזו בדיוק \( q \).

        נבדוק מתי זה קורה.

    5. **המקרה \( q = 0 \) לא אפשרי.** בהפרש יש שתי ספרות 9, ולכן \( a = b = 9 \). כיוון
       ש-\( q = b - c = 0 \), גם \( c = 9 \), כלומר יש שלוש ספרות 9. לכן אחת מהספרות
       \( p - 1 \) ו-\( 10 - p \) היא 9 :

        - **‏\( p - 1 = 9 \) :** אז \( p = 10 \), וזו לא ספרה.
        - **‏\( 10 - p = 9 \) :** אז \( p = 1 \), והספרות הן 0, 9, 9, 9. המרחק בין הגדולה
          לקטנה הוא 9 ולא 1, ותנאי א לא מתקיים.

    6. **המקרה \( q \ge 1 \).** הספרות של ההפרש הן \( p,\ q - 1,\ 9 - q,\ 10 - p \). כיוון
       ש-\( q \le p \), מתקיים \( q - 1 < p \), ולכן :

        - **‏\( q - 1 \)** אף פעם לא הספרה הגדולה ביותר, כי \( p \) גדולה ממנה.
        - **‏\( p \)** אף פעם לא הספרה הקטנה ביותר, כי \( q - 1 \) קטנה ממנה.

        נשארו 3 אפשרויות לספרה הגדולה, \( \{\, p,\ 9 - q,\ 10 - p \,\} \), ו-3 לספרה
        הקטנה, \( \{\, q - 1,\ 9 - q,\ 10 - p \,\} \). בלי המקרים שבהם אותה ספרה היא גם
        הגדולה וגם הקטנה, נשארים **7 מקרים**. בכל מקרה כותבים את תנאי א, ובודקים את תנאי ב
        על שתי הספרות שנשארו באמצע :

        - **מקרה 1, הגדולה \( p \) והקטנה \( q - 1 \) :** תנאי א נותן \( p - (q - 1) = p \),
          כלומר \( q = 1 \). באמצע נשארות \( 9 - q = 8 \) ו-\( 10 - p \). אבל \( p \) היא
          הגדולה, ולכן \( p \ge 8 \) ו-\( 10 - p \le 2 \). המרחק בין שתי האמצעיות הוא לפחות
          6, ולא \( q = 1 \). ✗
        - **מקרה 2, הגדולה \( p \) והקטנה \( 9 - q \) :** תנאי א נותן \( q = 9 \), ולכן גם
          \( p = 9 \). הספרות הן 9, 8, 0, 1, ושתי האמצעיות (8 ו-1) רחוקות 7 ולא 9. ✗
        - **מקרה 3, הגדולה \( p \) והקטנה \( 10 - p \) :** תנאי א נותן \( 2p - 10 = p \),
          כלומר \( p = 10 \), וזו לא ספרה. ✗
        - **מקרה 4, הגדולה \( 9 - q \) והקטנה \( q - 1 \) :** תנאי א נותן \( 10 - 2q = p \).
          באמצע נשארות \( p \) ו-\( 10 - p \), שהמרחק ביניהן \( |2p - 10| = |10 - 4q| \).
          תנאי ב דורש \( |10 - 4q| = q \), כלומר \( q = 2 \) (האפשרות השנייה,
          \( q = 10/3 \), לא שלמה). אז \( p = 6 \), והספרות הן 6, 1, 7, 4. ממוינות :
          7, 6, 4, 1. הגדולה היא באמת \( 9 - q = 7 \), הקטנה \( q - 1 = 1 \),
          ‏\( 7 - 1 = 6 = p \) ו-\( 6 - 4 = 2 = q \). ✓
        - **מקרה 5, הגדולה \( 9 - q \) והקטנה \( 10 - p \) :** תנאי א נותן
          \( p - 1 - q = p \), כלומר \( q = -1 \). ✗
        - **מקרה 6, הגדולה \( 10 - p \) והקטנה \( q - 1 \) :** תנאי א נותן
          \( 11 - p - q = p \), כלומר \( q = 11 - 2p \). באמצע נשארות \( p \)
          ו-\( 9 - q = 2p - 2 \), שהמרחק ביניהן \( |p - 2| \). תנאי ב דורש
          \( |p - 2| = 11 - 2p \) : או \( p = 13/3 \), שלא שלם, או \( p = 9 \), ואז
          \( q = -7 \). ✗
        - **מקרה 7, הגדולה \( 10 - p \) והקטנה \( 9 - q \) :** תנאי א נותן \( q = 2p - 1 \).
          יחד עם \( q \le p \) יוצא \( p = q = 1 \), והספרות הן 1, 0, 8, 9. הקטנה היא 0
          ולא \( 9 - q = 8 \). ✗

    7. **המסקנה.** רק מקרה 4 עובד, עם \( p = 6 \) ו-\( q = 2 \). ההפרש הוא
       \( 999 \cdot 6 + 90 \cdot 2 = 5994 + 180 = 6174 \). יחד עם 0 משלב 2, אלה שני
       המספרים המיוחדים היחידים. ∎

    </div>

    **כל 55 המועמדים בתרשים אחד.** כל משבצת היא הפרש \( 999p + 90q \) אחד. העמודה
    \( q = 0 \) (בכחול) נפסלה בשלב 5, ומבין כל השאר רק 6174 (בכתום) חוזר לעצמו. המועמד
    ה-55 הוא 0, כש-\( p = 0 \).

    <svg class="figure" viewBox="0 0 518 266" role="img" aria-label="כל 54 ההפרשים האפשריים 999p + 90q, ורק 6174 חוזר לעצמו"><text class="tick" x="75.0" y="17" text-anchor="middle">q = 0</text><text class="tick" x="121.0" y="17" text-anchor="middle">q = 1</text><text class="tick" x="167.0" y="17" text-anchor="middle">q = 2</text><text class="tick" x="213.0" y="17" text-anchor="middle">q = 3</text><text class="tick" x="259.0" y="17" text-anchor="middle">q = 4</text><text class="tick" x="305.0" y="17" text-anchor="middle">q = 5</text><text class="tick" x="351.0" y="17" text-anchor="middle">q = 6</text><text class="tick" x="397.0" y="17" text-anchor="middle">q = 7</text><text class="tick" x="443.0" y="17" text-anchor="middle">q = 8</text><text class="tick" x="489.0" y="17" text-anchor="middle">q = 9</text><text class="tick" x="44" y="44.0" text-anchor="end">p = 1</text><rect class="box-node" x="52" y="26" width="46" height="26"/><rect class="cell-s1" x="52" y="26" width="46" height="26"/><text class="box-num" x="75.0" y="44.0" text-anchor="middle">0999</text><rect class="box-node" x="98" y="26" width="46" height="26"/><text class="box-num" x="121.0" y="44.0" text-anchor="middle">1089</text><text class="tick" x="44" y="70.0" text-anchor="end">p = 2</text><rect class="box-node" x="52" y="52" width="46" height="26"/><rect class="cell-s1" x="52" y="52" width="46" height="26"/><text class="box-num" x="75.0" y="70.0" text-anchor="middle">1998</text><rect class="box-node" x="98" y="52" width="46" height="26"/><text class="box-num" x="121.0" y="70.0" text-anchor="middle">2088</text><rect class="box-node" x="144" y="52" width="46" height="26"/><text class="box-num" x="167.0" y="70.0" text-anchor="middle">2178</text><text class="tick" x="44" y="96.0" text-anchor="end">p = 3</text><rect class="box-node" x="52" y="78" width="46" height="26"/><rect class="cell-s1" x="52" y="78" width="46" height="26"/><text class="box-num" x="75.0" y="96.0" text-anchor="middle">2997</text><rect class="box-node" x="98" y="78" width="46" height="26"/><text class="box-num" x="121.0" y="96.0" text-anchor="middle">3087</text><rect class="box-node" x="144" y="78" width="46" height="26"/><text class="box-num" x="167.0" y="96.0" text-anchor="middle">3177</text><rect class="box-node" x="190" y="78" width="46" height="26"/><text class="box-num" x="213.0" y="96.0" text-anchor="middle">3267</text><text class="tick" x="44" y="122.0" text-anchor="end">p = 4</text><rect class="box-node" x="52" y="104" width="46" height="26"/><rect class="cell-s1" x="52" y="104" width="46" height="26"/><text class="box-num" x="75.0" y="122.0" text-anchor="middle">3996</text><rect class="box-node" x="98" y="104" width="46" height="26"/><text class="box-num" x="121.0" y="122.0" text-anchor="middle">4086</text><rect class="box-node" x="144" y="104" width="46" height="26"/><text class="box-num" x="167.0" y="122.0" text-anchor="middle">4176</text><rect class="box-node" x="190" y="104" width="46" height="26"/><text class="box-num" x="213.0" y="122.0" text-anchor="middle">4266</text><rect class="box-node" x="236" y="104" width="46" height="26"/><text class="box-num" x="259.0" y="122.0" text-anchor="middle">4356</text><text class="tick" x="44" y="148.0" text-anchor="end">p = 5</text><rect class="box-node" x="52" y="130" width="46" height="26"/><rect class="cell-s1" x="52" y="130" width="46" height="26"/><text class="box-num" x="75.0" y="148.0" text-anchor="middle">4995</text><rect class="box-node" x="98" y="130" width="46" height="26"/><text class="box-num" x="121.0" y="148.0" text-anchor="middle">5085</text><rect class="box-node" x="144" y="130" width="46" height="26"/><text class="box-num" x="167.0" y="148.0" text-anchor="middle">5175</text><rect class="box-node" x="190" y="130" width="46" height="26"/><text class="box-num" x="213.0" y="148.0" text-anchor="middle">5265</text><rect class="box-node" x="236" y="130" width="46" height="26"/><text class="box-num" x="259.0" y="148.0" text-anchor="middle">5355</text><rect class="box-node" x="282" y="130" width="46" height="26"/><text class="box-num" x="305.0" y="148.0" text-anchor="middle">5445</text><text class="tick" x="44" y="174.0" text-anchor="end">p = 6</text><rect class="box-node" x="52" y="156" width="46" height="26"/><rect class="cell-s1" x="52" y="156" width="46" height="26"/><text class="box-num" x="75.0" y="174.0" text-anchor="middle">5994</text><rect class="box-node" x="98" y="156" width="46" height="26"/><text class="box-num" x="121.0" y="174.0" text-anchor="middle">6084</text><rect class="box-node" x="144" y="156" width="46" height="26"/><rect class="cell-s2" x="144" y="156" width="46" height="26"/><text class="box-num" x="167.0" y="174.0" text-anchor="middle">6174</text><rect class="box-node" x="190" y="156" width="46" height="26"/><text class="box-num" x="213.0" y="174.0" text-anchor="middle">6264</text><rect class="box-node" x="236" y="156" width="46" height="26"/><text class="box-num" x="259.0" y="174.0" text-anchor="middle">6354</text><rect class="box-node" x="282" y="156" width="46" height="26"/><text class="box-num" x="305.0" y="174.0" text-anchor="middle">6444</text><rect class="box-node" x="328" y="156" width="46" height="26"/><text class="box-num" x="351.0" y="174.0" text-anchor="middle">6534</text><text class="tick" x="44" y="200.0" text-anchor="end">p = 7</text><rect class="box-node" x="52" y="182" width="46" height="26"/><rect class="cell-s1" x="52" y="182" width="46" height="26"/><text class="box-num" x="75.0" y="200.0" text-anchor="middle">6993</text><rect class="box-node" x="98" y="182" width="46" height="26"/><text class="box-num" x="121.0" y="200.0" text-anchor="middle">7083</text><rect class="box-node" x="144" y="182" width="46" height="26"/><text class="box-num" x="167.0" y="200.0" text-anchor="middle">7173</text><rect class="box-node" x="190" y="182" width="46" height="26"/><text class="box-num" x="213.0" y="200.0" text-anchor="middle">7263</text><rect class="box-node" x="236" y="182" width="46" height="26"/><text class="box-num" x="259.0" y="200.0" text-anchor="middle">7353</text><rect class="box-node" x="282" y="182" width="46" height="26"/><text class="box-num" x="305.0" y="200.0" text-anchor="middle">7443</text><rect class="box-node" x="328" y="182" width="46" height="26"/><text class="box-num" x="351.0" y="200.0" text-anchor="middle">7533</text><rect class="box-node" x="374" y="182" width="46" height="26"/><text class="box-num" x="397.0" y="200.0" text-anchor="middle">7623</text><text class="tick" x="44" y="226.0" text-anchor="end">p = 8</text><rect class="box-node" x="52" y="208" width="46" height="26"/><rect class="cell-s1" x="52" y="208" width="46" height="26"/><text class="box-num" x="75.0" y="226.0" text-anchor="middle">7992</text><rect class="box-node" x="98" y="208" width="46" height="26"/><text class="box-num" x="121.0" y="226.0" text-anchor="middle">8082</text><rect class="box-node" x="144" y="208" width="46" height="26"/><text class="box-num" x="167.0" y="226.0" text-anchor="middle">8172</text><rect class="box-node" x="190" y="208" width="46" height="26"/><text class="box-num" x="213.0" y="226.0" text-anchor="middle">8262</text><rect class="box-node" x="236" y="208" width="46" height="26"/><text class="box-num" x="259.0" y="226.0" text-anchor="middle">8352</text><rect class="box-node" x="282" y="208" width="46" height="26"/><text class="box-num" x="305.0" y="226.0" text-anchor="middle">8442</text><rect class="box-node" x="328" y="208" width="46" height="26"/><text class="box-num" x="351.0" y="226.0" text-anchor="middle">8532</text><rect class="box-node" x="374" y="208" width="46" height="26"/><text class="box-num" x="397.0" y="226.0" text-anchor="middle">8622</text><rect class="box-node" x="420" y="208" width="46" height="26"/><text class="box-num" x="443.0" y="226.0" text-anchor="middle">8712</text><text class="tick" x="44" y="252.0" text-anchor="end">p = 9</text><rect class="box-node" x="52" y="234" width="46" height="26"/><rect class="cell-s1" x="52" y="234" width="46" height="26"/><text class="box-num" x="75.0" y="252.0" text-anchor="middle">8991</text><rect class="box-node" x="98" y="234" width="46" height="26"/><text class="box-num" x="121.0" y="252.0" text-anchor="middle">9081</text><rect class="box-node" x="144" y="234" width="46" height="26"/><text class="box-num" x="167.0" y="252.0" text-anchor="middle">9171</text><rect class="box-node" x="190" y="234" width="46" height="26"/><text class="box-num" x="213.0" y="252.0" text-anchor="middle">9261</text><rect class="box-node" x="236" y="234" width="46" height="26"/><text class="box-num" x="259.0" y="252.0" text-anchor="middle">9351</text><rect class="box-node" x="282" y="234" width="46" height="26"/><text class="box-num" x="305.0" y="252.0" text-anchor="middle">9441</text><rect class="box-node" x="328" y="234" width="46" height="26"/><text class="box-num" x="351.0" y="252.0" text-anchor="middle">9531</text><rect class="box-node" x="374" y="234" width="46" height="26"/><text class="box-num" x="397.0" y="252.0" text-anchor="middle">9621</text><rect class="box-node" x="420" y="234" width="46" height="26"/><text class="box-num" x="443.0" y="252.0" text-anchor="middle">9711</text><rect class="box-node" x="466" y="234" width="46" height="26"/><text class="box-num" x="489.0" y="252.0" text-anchor="middle">9801</text></svg>

    **נסו בעצמכם.** הקלידו מספר או הגרילו אחד : הטבלה מראה את המיון ואת החיסור, ואז
    מפעילים את אותו צעד על ההפרש שוב ושוב. חוץ ממספרים שכל הספרות שלהם שוות (שנופלים ל-0),
    כולם מגיעים ל-6174 ונעצרים שם, וההיסטוגרמה מראה אחרי כמה צעדים.

    <div class="explorer" data-kind="kaprekar" data-digits="4"></div>

    #### סיבוכיות { .sol-cost }

    הלולאה בודקת 10,000 מספרים, כל אחד ב-\( O(1) \), ולוקחת שבריר שנייה. לפי שלב 1 מספיק
    לבדוק רק 55 מועמדים. במבחן זו תשובה טובה כבדיקה, אבל בראיון מצפים גם להסבר : למה
    ההפרש תלוי רק ב-\( p \) ו-\( q \), ולמה רק אחד מהם עובד.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : אפסים משלימים"
    הפתרון הנפוץ ביותר שנכשל הוא מיון של הספרות **בלי** לרפד באפסים. אז 95 הופך ל-"95"
    ו-"59", ההפרש הוא 36 במקום 9441, וגם ההוכחה של סעיף ב משתנה. מספר בן פחות מארבע
    ספרות הוא עדיין מספר בן ארבע ספרות בשאלה הזו.

??? trap "מלכודת : להעתיק את ההוכחה של שלוש ספרות"
    בשלוש ספרות ספרת האמצע מתבטלת וההפרש הוא כפולה של 99. מי שמניח שגם כאן האמצע
    מתבטל מקבל "כפולה של 999" ומפספס את האיבר \( 90q \) : גם \( b \) וגם \( c \)
    מחליפות מקום בין שני המספרים, ולכן נשארים שני פרמטרים ולא אחד.

??? followup "שאלות המשך"
    - **לחזור על התהליך :** מתחילים ממספר שלא כל הספרות שלו שוות, ומפעילים שוב ושוב את
      "ממיינים ומחסרים" על התוצאה. תמיד מגיעים ל-6174, שנקרא הקבוע של Kaprekar, ולכל
      היותר אחרי 7 צעדים. למשל <span dir="ltr">3524 → 3087 → 8352 → 6174</span>, ו-95 צריך את כל 7 הצעדים :
      <span dir="ltr">0095 → 9441 → 7992 → 7173 → 6354 → 3087 → 8352 → 6174</span>.
    - **כמה צעדים לכל מספר :**

        | צעדים | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
        |---|---|---|---|---|---|---|---|---|
        | מספרים | 1 | 383 | 576 | 2,400 | 1,272 | 1,518 | 1,656 | 2,184 |

        ‏10 המספרים שכל הספרות שלהם שוות (0000 עד 9999) מגיעים ל-0 ולא נספרו.
    - **חמש ספרות :** רק 0 מיוחד. כל מספר אחר נכנס בסוף למעגל ולא נעצר.
    - **שש ספרות :** יש שני מספרים מיוחדים, 549945 ו-631764.
    - **בחומרה :** כתבו מודול צירופי שמקבל 4 ספרות BCD ומוציא את ההפרש. כמה שכבות של
      משווים יש בנתיב הארוך ביותר?
