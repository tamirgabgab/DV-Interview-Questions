---
id: 13
title: ממיינים ספרות ומחסרים – ארבע ספרות
level: junior
difficulty: medium
tags: [math, digits, sorting, number-bases, python, systemverilog]
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
    - **להכליל :** בבונוס, האם המועמד מעביר את ניתוח המקרים לבסיס כללי, ומבחין בין "יש
      נקודת שבת" לבין "כל המספרים מגיעים אליה".

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

    **כל זוג והמקרה שלו.** בתיבה הבאה לוחצים על משבצת של התרשים : מתחת מופיעים ההפרש,
    הספרות שלו לפי שלב 3 (הגדולה והקטנה מסומנות), המקרה של שלב 6 שחל עליו (או שלב 5
    בעמודה \( q = 0 \)), ושני התנאים של שלב 4. כשתנאי לא מתקיים, ההפרש שייך לזוג אחר, והחץ
    מוביל אליו. "לזוג הבא" הולך בעקבות החץ, וכל מסלול נגמר ב-6174, הזוג היחיד שמצביע על
    עצמו.

    <div class="explorer" data-kind="kappairs" data-p="9" data-q="5"></div>

    **נסו בעצמכם.** הקלידו מספר או הגרילו אחד : הטבלה מראה את המיון ואת החיסור, ואז
    מפעילים את אותו צעד על ההפרש שוב ושוב. חוץ ממספרים שכל הספרות שלהם שוות (שנופלים ל-0),
    כולם מגיעים ל-6174 ונעצרים שם, וההיסטוגרמה מראה אחרי כמה צעדים. המתג "החיסור במאונך"
    מראה את הצעד הראשון כמו בטבלה של סעיף ב : עמודה אחרי עמודה מהאחדות, עם הלווים, ליד
    הספרות ש-\( p \) ו-\( q \) צופים.

    <div class="explorer" data-kind="kaprekar" data-digits="4"></div>

    #### סיבוכיות { .sol-cost }

    הלולאה בודקת 10,000 מספרים, כל אחד ב-\( O(1) \), ולוקחת שבריר שנייה. לפי שלב 1 מספיק
    לבדוק רק 55 מועמדים. במבחן זו תשובה טובה כבדיקה, אבל בראיון מצפים גם להסבר : למה
    ההפרש תלוי רק ב-\( p \) ו-\( q \), ולמה רק אחד מהם עובד.

---

### סעיף ג – בונוס : ארבע ספרות בבסיס B { #base-b }

!!! note "להרחבה"
    הסעיף הזה ארוך מהקודמים. הוא מכליל את ההוכחה של סעיף ב לכל בסיס, ומראה למה 6174
    הוא מקרה פרטי של משפחה שלמה.

אותו תהליך, אבל המספר כתוב **בבסיס \( B \)** (\( 2 \le B \le 16 \) בתיבה), עם ארבע ספרות
ואפסים משלימים משמאל. ממיינים את הספרות מהגדול לקטן ומהקטן לגדול ומחסרים. לאילו בסיסים
\( B \) קיים מספר \( X \), שלא כל ספרותיו שוות, עם \( F(X) = X \), ומהו? בבסיס 10 התשובה
היא 6174. (בסעיף הזה \( B \) הוא הבסיס, ו-\( a \ge b \ge c \ge d \) הן הספרות הממוינות,
כמו בסעיף ב.)

??? tip "רמז 1"
    חזרו על שלב 1 של סעיף ב עם \( B \) במקום 10 : ההפרש הוא \( p(B^3 - 1) + q(B^2 - B) \),
    עם אותם \( p = a - d \) ו-\( q = b - c \). מהן הספרות שלו בבסיס \( B \)?

??? tip "רמז 2"
    כש-\( q \ge 1 \) הספרות הן \( (p,\ q - 1,\ B - q - 1,\ B - p) \). כדי שהמספר יחזור
    לעצמו, בארבע הספרות האלה הגדולה פחות הקטנה צריכה להיות \( p \), ושתי האמצעיות צריכות
    להיות רחוקות \( q \). בכמה דרכים אפשר לחלק ארבע ספרות לזוג "קיצוני" ולזוג "אמצעי"?

??? tip "רמז 3"
    רק חלוקה אחת נותנת משפחה שלמה של פתרונות : \( p = 3q \) ו-\( B = 5q \). מה זה אומר
    על הבסיס?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏**חוץ משני חריגים, נקודת שבת קיימת אם ורק אם \( B \) מתחלק ב-5**, ואז היא יחידה.
        עם \( B = 5k \) הספרות הן \( (3k,\ k - 1,\ 4k - 1,\ 2k) \) והערך הוא
        \( B(B - 1)(3B^2 + 4B + 3) / 5 \) : בבסיס 10 (‏\( k = 2 \)) זה 6174. החריגים הם 0111
        ו-1001 בבסיס 2, ו-3021 בבסיס 4. בכל בסיס אחר אין נקודת שבת, והתהליך נכנס למחזורים.

    #### הרעיון { .sol-idea }

    **שני פרמטרים.** עם הספרות הממוינות \( a \ge b \ge c \ge d \), \( p = a - d \)
    ו-\( q = b - c \), כך ש-\( 0 \le q \le p \le B - 1 \) :

    \[
    \begin{aligned}
    F &= (a B^3 + b B^2 + c B + d) \\
      &\quad - (d B^3 + c B^2 + b B + a) \\
      &= p \, (B^3 - 1) + q \, (B^2 - B).
    \end{aligned}
    \]

    בבסיס 10 זה בדיוק \( 999p + 90q \) של סעיף ב. אם \( p = 0 \) כל הספרות שוות ו-\( F = 0 \),
    ולכן מעכשיו \( p \ge 1 \).

    **הספרות של F.** כמו בחיסור במאונך של סעיף ב, עם \( B \) במקום 10 :

    - **כש-\( q = 0 \) :** הספרות הן \( (p - 1,\ B - 1,\ B - 1,\ B - p) \).
    - **כש-\( q \ge 1 \) :** הספרות הן \( (p,\ q - 1,\ B - q - 1,\ B - p) \).

    כי בפריסה לפי חזקות של \( B \) :

    \[
    \begin{aligned}
    p (B^3 - 1) &= (p - 1) B^3 + (B - 1) B^2 \\
                &\quad + (B - 1) B + (B - p), \\
    F           &= p B^3 + (q - 1) B^2 \\
                &\quad + (B - q - 1) B + (B - p) \quad (q \ge 1).
    \end{aligned}
    \]

    בשני המקרים כל המקדמים בין 0 ל-\( B - 1 \), והייצוג בבסיס \( B \) יחיד, ולכן אלה בדיוק
    הספרות. כמו בשלוש ספרות, ההפרש תלוי רק בזוג \( (p, q) \), ולכן כל התהליך הוא מפה על
    הזוגות.

    **התנאי.** ‏\( F(X) = X \) אם ורק אם \( X \) שווה לערך של הזוג שלו, כלומר לספרות של
    \( F \) יש אותו זוג : **הגדולה פחות הקטנה היא \( p \)**, ו**ההפרש בין שתי האמצעיות הוא
    \( q \)**. זה מה שבודקים בכל המקרים.

    **התוצאה :**

    <!-- gen 0 -->

    | הבסיס B | נקודת השבת בבסיס B | הערך העשרוני |
    |:-:|:-:|:-:|
    | ‏2 | ‏0111 ו-1001 | ‏7 ו-9 |
    | ‏4 | ‏3021 | ‏201 |
    | ‏**B = 5k** | ‏**(3k, k − 1, 4k − 1, 2k)** | ‏**B(B − 1)(3B² + 4B + 3) / 5** |
    | כל בסיס אחר | אין | — |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הצורה :** \( F = p (B^3 - 1) + q (B^2 - B) \).
    2. **הספרות :** \( (p - 1, B - 1, B - 1, B - p) \) או \( (p, q - 1, B - q - 1, B - p) \).
    3. **התנאי :** בספרות של \( F \) הגדולה פחות הקטנה היא \( p \), והאמצעיות רחוקות \( q \).
    4. **המקרה \( q = 0 \) :** רק בסיס 2.
    5. **המקרה \( q \ge 1 \) :** שלוש דרכים לחלק את ארבע הספרות לשני זוגות; רק אחת נותנת
       משפחה, \( B = 5q \), ועוד שני חריגים בבסיסים 2 ו-4.
    6. **קיום אינו התכנסות.** בבסיס 15 נקודת השבת 92B6 קיימת, אבל 1234 לא מגיע אליה : הוא
       נכנס למחזור באורך 4 (‏30DC, D852, B2B4, 9676). ה-\( (p, q) \) של 9676 הוא שוב (3, 1),
       בדיוק כמו של 1234, ולכן הצעד הבא חוזר ל-30DC :

        <!-- gen 2 -->

        | צעד | ‏X בבסיס 15 | מהגדול לקטן | מהקטן לגדול | ‏(p, q) | ההפרש |
        |:-:|:-:|:-:|:-:|:-:|:-:|
        | ‏1 | ‏1234 | ‏4321 | ‏1234 | ‏(3, 1) | ‏**30DC** |
        | ‏2 | ‏30DC | ‏DC30 | ‏03CD | ‏(13, 9) | ‏**D852** |
        | ‏3 | ‏D852 | ‏D852 | ‏258D | ‏(11, 3) | ‏**B2B4** |
        | ‏4 | ‏B2B4 | ‏BB42 | ‏24BB | ‏(9, 7) | ‏**9676** |
        | ‏5 | ‏9676 | ‏9766 | ‏6679 | ‏(3, 1) | ‏**30DC** |

        <!-- /gen -->

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="kaprekar4_step_b, kaprekar4_fixed_b" hl_lines="3 4 5 6 7 8 15 16"
        // One step in base B: four digits (leading zeros kept), sorted descending minus ascending.
        function automatic int kaprekar4_step_b(int x, int B);
          int a = x / (B * B * B), b = (x / (B * B)) % B, c = (x / B) % B, d = x % B;   // (1)!
          if (a < b) {a, b} = {b, a};     // the same sorting network as in part a
          if (c < d) {c, d} = {d, c};
          if (a < c) {a, c} = {c, a};
          if (b < d) {b, d} = {d, b};
          if (b < c) {b, c} = {c, b};
          return (a * B * B * B + b * B * B + c * B + d) - (d * B * B * B + c * B * B + b * B + a);   // (2)!
        endfunction

        // The fixed points with two different digits, by the theorem: returns how many, in x1 and x2.
        function automatic int kaprekar4_fixed_b(int B, output int x1, output int x2);
          x1 = 0; x2 = 0;
          if (B == 2) begin x1 = 7; x2 = 9; return 2; end                                 // (3)!
          if (B == 4) begin x1 = 201; return 1; end
          if (B % 5 == 0) begin x1 = B * (B - 1) * (3 * B * B + 4 * B + 3) / 5; return 1; end   // (4)!
          return 0;
        endfunction
        ```

        1. אותו פירוק כמו בסעיף א, עם \( B \) במקום 10. ב-SystemVerilog שמות רגישים לאותיות,
           ולכן `B` (הבסיס) ו-`b` (הספרה השנייה) הם שני משתנים שונים.
        2. הגדול פחות הקטן; לפי ההוכחה זה \( p (B^3 - 1) + q (B^2 - B) \).
        3. החריגים : 0111 ו-1001 בבסיס 2 (7 ו-9), ו-3021 בבסיס 4 (201).
        4. המשפחה \( B = 5k \) : הספרות \( (3k, k - 1, 4k - 1, 2k) \). המכפלה מתחלקת ב-5 כי
           \( B \) מתחלק.

    === "Python"
        ```python title="kaprekar4_step_b, kaprekar4_fixed_b, kaprekar4_orbit_b"
        def kaprekar4_step_b(x: int, B: int) -> int:
            """One step in base B: four digits (leading zeros kept), sorted descending minus ascending."""
            a, b, c, d = sorted((x // B**3, x // B**2 % B, x // B % B, x % B), reverse=True)
            return (a * B**3 + b * B**2 + c * B + d) - (d * B**3 + c * B**2 + b * B + a)


        def kaprekar4_fixed_b(B: int) -> list[int]:
            """The fixed points with two different digits, by the theorem."""
            out = [7, 9] if B == 2 else [201] if B == 4 else []          # 0111, 1001; 3021 (1)
            if B % 5 == 0:
                out.append(B * (B - 1) * (3 * B * B + 4 * B + 3) // 5)  # (3k, k-1, 4k-1, 2k) (2)
            return out


        def kaprekar4_orbit_b(x: int, B: int) -> tuple[list[int], int]:
            """The values from x until one repeats, and the index where the cycle starts."""
            values = [x]
            while (y := kaprekar4_step_b(values[-1], B)) not in values:
                values.append(y)
            return values, values.index(y)                                # (3)!
        ```

        1. החריגים של הבסיסים 2 ו-4.
        2. המשפחה \( B = 5k \).
        3. אורך המחזור הוא `len(values) - start`; נקודת שבת היא מחזור באורך 1. בבסיס אי-מתחלק
           ב-5 (חוץ מ-2 ו-4) הלולאה תמיד מסתיימת במחזור ארוך מ-1.

    #### למה זה נכון { .sol-proof }

    **המקרה \( q = 0 \).** הספרות הן \( \{p - 1,\ B - 1,\ B - 1,\ B - p\} \). שתי האמצעיות
    צריכות להיות שוות, ולכן עוד ספרה שווה ל-\( B - 1 \) :

    - **‏\( p - 1 = B - 1 \) :** ‏\( p = B \), בלתי אפשרי.
    - **‏\( B - p = B - 1 \) :** ‏\( p = 1 \). אז הקטנה היא \( p - 1 = 0 \), והתנאי
      \( (B - 1) - 0 = p = 1 \) נותן \( B = 2 \) : **0111 בבסיס 2**.

    **המקרה \( q \ge 1 \).** נקרא לארבע הספרות של \( F \) :

    \[
    \alpha = p, \quad \beta = B - p, \quad \gamma = q - 1, \quad \delta = B - q - 1.
    \]

    צריך לחלק אותן לזוג **קיצוני** (הגדולה והקטנה, עם הפרש \( p \)) ולזוג **אמצעי** (עם
    הפרש \( q \)). יש בדיוק שלוש דרכים לחלק ארבעה איברים לשני זוגות, ולזוג הקיצוני יש
    תמיד את ההפרש הגדול מבין השניים.

    **חלוקה א : \( \{\alpha, \beta\} \) ו-\( \{\gamma, \delta\} \).** ההפרשים הם \( |2p - B| \)
    ו-\( |2q - B| \).

    - **‏\( \{\alpha, \beta\} \) קיצוני :** ‏\( |2p - B| = p \) נותן \( B = 3p \), ו-\( |2q - B| = q \)
      נותן \( B = 3q \), ולכן \( p = q \). אבל אז \( \gamma = p - 1 < \alpha \), כלומר \( \alpha \)
      אינו הקטנה. ✗
    - **‏\( \{\gamma, \delta\} \) קיצוני :** ‏\( |2q - B| = p \) ו-\( |2p - B| = q \).
      - ‏\( B - 2q = p \) ו-\( B - 2p = q \) : ‏\( p = q \), ואז \( \delta = 2p - 1 < \beta = 2p \),
        כלומר \( \delta \) אינו הגדולה. ✗
      - ‏\( 2q - B = p \) : ‏\( 2q = B + p \), אבל \( 2q \le 2p \), ולכן \( B \le p \). ✗
      - ‏\( B - 2q = p \) ו-\( 2p - B = q \) : **‏\( p = 3q \) ו-\( B = 5q \)**. ✓

    עם \( k = q \) : ‏\( \alpha = 3k \), ‏\( \beta = 2k \), ‏\( \gamma = k - 1 \), ‏\( \delta = 4k - 1 \).
    הזוג הקיצוני \( \{k - 1, 4k - 1\} \) הוא באמת הקטנה והגדולה, עם הפרש \( 3k = p \), והזוג
    האמצעי \( \{2k, 3k\} \) רחוק \( k = q \). זו **המשפחה \( B = 5k \)**. הספרות של \( X \) הן
    \( (p,\ q - 1,\ B - q - 1,\ B - p) \), כלומר \( (3k,\ k - 1,\ 4k - 1,\ 2k) \).

    **חלוקה ב : \( \{\alpha, \gamma\} \) ו-\( \{\beta, \delta\} \).** ההפרשים הם
    \( p - q + 1 \) ו-\( |p - q - 1| \).

    - **‏\( \{\alpha, \gamma\} \) קיצוני :** ‏\( p - q + 1 = p \) נותן \( q = 1 \), ואז
      \( |p - 2| = 1 \), כלומר \( p = 3 \) או \( p = 1 \).
      - ‏\( p = 3 \) : הספרות \( \{3,\ B - 3,\ 0,\ B - 2\} \). כדי ש-3 תהיה הגדולה צריך
        \( B - 2 \le 3 \), ומ-\( p \le B - 1 \) נובע \( B \ge 4 \). בבסיס 4 זה **3021**, ובבסיס 5
        זה 3032, שכבר במשפחה (‏\( k = 1 \)).
      - ‏\( p = 1 \) : הספרות \( \{1,\ B - 1,\ 0,\ B - 2\} \). כדי ש-1 תהיה הגדולה צריך
        \( B = 2 \) : **1001 בבסיס 2**.
    - **‏\( \{\beta, \delta\} \) קיצוני :** ‏\( |p - q - 1| = p \). האפשרות \( p - q - 1 = p \) נותנת
      \( q = -1 \); האפשרות \( q + 1 - p = p \) נותנת \( q = 2p - 1 \), ועם \( q \le p \) יוצא
      \( p = q = 1 \) ו-\( B = 2 \), שוב 1001.

    **חלוקה ג : \( \{\alpha, \delta\} \) ו-\( \{\beta, \gamma\} \).** נסמן \( t = B - p - q \). ההפרשים
    הם \( |1 - t| \) ו-\( |t + 1| \).

    - **‏\( t = 0 \) :** שני ההפרשים 1, ולכן \( p = q = 1 \) ו-\( B = 2 \). שוב 1001.
    - **‏\( t \ge 1 \) :** ההפרשים \( t - 1 \) ו-\( t + 1 \), ולכן \( q = t - 1 \), ‏\( p = t + 1 \)
      ו-\( B = p + q + t = 3t \). הזוג הקיצוני צריך להיות \( \{\beta, \gamma\} = \{2t - 1,\ t - 2\} \),
      אבל \( \delta = 2t > 2t - 1 \). ✗
    - **‏\( t \le -1 \) :** ההפרשים \( |t| + 1 \) ו-\( |t| - 1 \), ולכן \( p = |t| + 1 \),
      ‏\( q = |t| - 1 \) ו-\( B = p + q + t = |t| \), כלומר \( p = B + 1 \). ✗

    כל החלוקות נבדקו, ולכן הפתרונות הם בדיוק 0111 ו-1001 (בסיס 2), 3021 (בסיס 4) והמשפחה
    \( B = 5k \). ∎

    **הערך במשפחה.** בדרך ההפרשים, עם \( p = 3k \) ו-\( q = k \) :

    \[
    \begin{aligned}
    X &= 3k (B^3 - 1) + k (B^2 - B) \\
      &= k (B - 1)(3B^2 + 4B + 3) \\
      &= \frac{B (B - 1)(3B^2 + 4B + 3)}{5},
    \end{aligned}
    \]

    או בהצבה של \( B = 5k \) בספרות :

    \[
    \begin{aligned}
    X &= 375k^4 + 25k^3 - 5k^2 - 3k \\
      &= k (5k - 1)(75k^2 + 20k + 3).
    \end{aligned}
    \]

    בבסיס 10 : ‏\( 2 \cdot 9 \cdot 343 = 6174 \) ✓ :

    <!-- gen 1 -->

    | ‏B | ‏k | הספרות | בבסיס B | הערך העשרוני |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏5 | ‏1 | ‏(3, 0, 3, 2) | ‏**3032** | ‏392 |
    | ‏10 | ‏2 | ‏(6, 1, 7, 4) | ‏**6174** | ‏6,174 |
    | ‏15 | ‏3 | ‏(9, 2, 11, 6) | ‏**92B6** | ‏30,996 |
    | ‏20 | ‏4 | ‏(12, 3, 15, 8) | ‏**C3F8** | ‏97,508 |
    | ‏25 | ‏5 | ‏(15, 4, 19, 10) | ‏**F4JA** | ‏237,360 |
    | ‏30 | ‏6 | ‏(18, 5, 23, 12) | ‏**I5NC** | ‏491,202 |
    | ‏35 | ‏7 | ‏(21, 6, 27, 14) | ‏**L6RE** | ‏908,684 |
    | ‏40 | ‏8 | ‏(24, 7, 31, 16) | ‏— | ‏1,548,456 |
    | ‏45 | ‏9 | ‏(27, 8, 35, 18) | ‏— | ‏2,478,168 |
    | ‏50 | ‏10 | ‏(30, 9, 39, 20) | ‏— | ‏3,774,470 |

    <!-- /gen -->

    **קיום אינו התכנסות.** בבסיסים 5 ו-10 כל מספר שלא כל ספרותיו שוות מגיע לנקודת השבת.
    בבסיס 15 נקודת השבת קיימת, אבל רק 2,160 מתוך 50,610 מספרים מגיעים אליה, והשאר נכנסים
    לשישה מחזורים. בבסיסים בלי נקודת שבת כל המספרים נכנסים למחזורים. הטבלה מריצה את כל
    \( B^4 \) המספרים של כל בסיס :

    <!-- gen 3 -->

    | ‏B | נקודות שבת | מחזורים : האורך (כמה מספרים מגיעים) | מגיעים לנקודת שבת |
    |:-:|:-:|---|:-:|
    | ‏2 | ‏0111, 1001 | ‏— | ‏14 מתוך 14 |
    | ‏3 | ‏— | ‏2 (78) | ‏0 מתוך 78 |
    | ‏4 | ‏3021 | ‏2 (168) | ‏84 מתוך 252 |
    | ‏5 | ‏3032 | ‏— | ‏620 מתוך 620 |
    | ‏6 | ‏— | ‏6 (1,290) | ‏0 מתוך 1,290 |
    | ‏7 | ‏— | ‏3 (2,394) | ‏0 מתוך 2,394 |
    | ‏8 | ‏— | ‏5 (2,768), 3 (1,320) | ‏0 מתוך 4,088 |
    | ‏9 | ‏— | ‏3 (3,308), 3 (3,244) | ‏0 מתוך 6,552 |
    | ‏10 | ‏6174 | ‏— | ‏9,990 מתוך 9,990 |
    | ‏11 | ‏— | ‏5 (7,522), 5 (7,108) | ‏0 מתוך 14,630 |
    | ‏12 | ‏— | ‏6 (16,012), 3 (4,712) | ‏0 מתוך 20,724 |
    | ‏13 | ‏— | ‏6 (11,706), 6 (11,340), 3 (5,502) | ‏0 מתוך 28,548 |
    | ‏14 | ‏— | ‏3 (38,402) | ‏0 מתוך 38,402 |
    | ‏15 | ‏92B6 | ‏4 (10,052), 4 (9,640), 4 (9,538), 4 (9,490), 2 (5,170), 2 (4,560) | ‏2,160 מתוך 50,610 |
    | ‏16 | ‏— | ‏6 (31,536), 4 (14,928), 3 (12,528), 2 (6,528) | ‏0 מתוך 65,520 |

    <!-- /gen -->

    **המפה של הזוגות.** כי \( F \) תלוי רק ב-\( (p, q) \), אפשר לצייר את כל התהליך על משולש
    הזוגות \( 0 \le q \le p \le B - 1 \) : כל משבצת צבועה לפי היעד של הערך שלה. בבסיס 15 רוב
    המשבצות נכנסות למחזורים, ורק חלק קטן מגיע ל-(9, 3) של 92B6. המסלול של 1234 עובר בארבע
    משבצות וחוזר ל-(3, 1) :

    <!-- gen 4 -->

    <svg class="figure kq-map" viewBox="0 0 442 342" style="max-width:28rem" role="img" aria-label="המפה של הזוגות (p, q) בבסיס 15 : כל משבצת צבועה לפי היעד של הערך שלה, והמסלול של 1234"><text class="kq-tick" x="57" y="18" text-anchor="middle">0</text><text class="kq-tick" x="83" y="18" text-anchor="middle">1</text><text class="kq-tick" x="109" y="18" text-anchor="middle">2</text><text class="kq-tick" x="135" y="18" text-anchor="middle">3</text><text class="kq-tick" x="161" y="18" text-anchor="middle">4</text><text class="kq-tick" x="187" y="18" text-anchor="middle">5</text><text class="kq-tick" x="213" y="18" text-anchor="middle">6</text><text class="kq-tick" x="239" y="18" text-anchor="middle">7</text><text class="kq-tick" x="265" y="18" text-anchor="middle">8</text><text class="kq-tick" x="291" y="18" text-anchor="middle">9</text><text class="kq-tick" x="317" y="18" text-anchor="middle">10</text><text class="kq-tick" x="343" y="18" text-anchor="middle">11</text><text class="kq-tick" x="369" y="18" text-anchor="middle">12</text><text class="kq-tick" x="395" y="18" text-anchor="middle">13</text><text class="kq-tick" x="421" y="18" text-anchor="middle">14</text><text class="kq-tick" x="14" y="18">p \ q</text><text class="kq-tick" x="38" y="41" text-anchor="end">1</text><rect class="kq-cell to-cycle" x="45" y="27" width="24" height="20" rx="3"><title>(p, q) = (1, 0) : 0EEE</title></rect><rect class="kq-cell to-cycle" x="71" y="27" width="24" height="20" rx="3"><title>(p, q) = (1, 1) : 10DE</title></rect><text class="kq-tick" x="38" y="63" text-anchor="end">2</text><rect class="kq-cell to-cycle" x="45" y="49" width="24" height="20" rx="3"><title>(p, q) = (2, 0) : 1EED</title></rect><rect class="kq-cell to-cycle" x="71" y="49" width="24" height="20" rx="3"><title>(p, q) = (2, 1) : 20DD</title></rect><rect class="kq-cell to-cycle" x="97" y="49" width="24" height="20" rx="3"><title>(p, q) = (2, 2) : 21CD</title></rect><text class="kq-tick" x="38" y="85" text-anchor="end">3</text><rect class="kq-cell to-cycle" x="45" y="71" width="24" height="20" rx="3"><title>(p, q) = (3, 0) : 2EEC</title></rect><rect class="kq-cell is-cycle" x="71" y="71" width="24" height="20" rx="3"><title>(p, q) = (3, 1) : 30DC</title></rect><rect class="kq-cell to-cycle" x="97" y="71" width="24" height="20" rx="3"><title>(p, q) = (3, 2) : 31CC</title></rect><rect class="kq-cell to-cycle" x="123" y="71" width="24" height="20" rx="3"><title>(p, q) = (3, 3) : 32BC</title></rect><text class="kq-tick" x="38" y="107" text-anchor="end">4</text><rect class="kq-cell to-cycle" x="45" y="93" width="24" height="20" rx="3"><title>(p, q) = (4, 0) : 3EEB</title></rect><rect class="kq-cell to-cycle" x="71" y="93" width="24" height="20" rx="3"><title>(p, q) = (4, 1) : 40DB</title></rect><rect class="kq-cell to-cycle" x="97" y="93" width="24" height="20" rx="3"><title>(p, q) = (4, 2) : 41CB</title></rect><rect class="kq-cell to-cycle" x="123" y="93" width="24" height="20" rx="3"><title>(p, q) = (4, 3) : 42BB</title></rect><rect class="kq-cell to-cycle" x="149" y="93" width="24" height="20" rx="3"><title>(p, q) = (4, 4) : 43AB</title></rect><text class="kq-tick" x="38" y="129" text-anchor="end">5</text><rect class="kq-cell to-cycle" x="45" y="115" width="24" height="20" rx="3"><title>(p, q) = (5, 0) : 4EEA</title></rect><rect class="kq-cell is-cycle" x="71" y="115" width="24" height="20" rx="3"><title>(p, q) = (5, 1) : 50DA</title></rect><rect class="kq-cell to-cycle" x="97" y="115" width="24" height="20" rx="3"><title>(p, q) = (5, 2) : 51CA</title></rect><rect class="kq-cell is-cycle" x="123" y="115" width="24" height="20" rx="3"><title>(p, q) = (5, 3) : 52BA</title></rect><rect class="kq-cell to-cycle" x="149" y="115" width="24" height="20" rx="3"><title>(p, q) = (5, 4) : 53AA</title></rect><rect class="kq-cell to-cycle" x="175" y="115" width="24" height="20" rx="3"><title>(p, q) = (5, 5) : 549A</title></rect><text class="kq-tick" x="38" y="151" text-anchor="end">6</text><rect class="kq-cell to-cycle" x="45" y="137" width="24" height="20" rx="3"><title>(p, q) = (6, 0) : 5EE9</title></rect><rect class="kq-cell to-cycle" x="71" y="137" width="24" height="20" rx="3"><title>(p, q) = (6, 1) : 60D9</title></rect><rect class="kq-cell to-cycle" x="97" y="137" width="24" height="20" rx="3"><title>(p, q) = (6, 2) : 61C9</title></rect><rect class="kq-cell to-fixed" x="123" y="137" width="24" height="20" rx="3"><title>(p, q) = (6, 3) : 62B9</title></rect><rect class="kq-cell to-cycle" x="149" y="137" width="24" height="20" rx="3"><title>(p, q) = (6, 4) : 63A9</title></rect><rect class="kq-cell to-cycle" x="175" y="137" width="24" height="20" rx="3"><title>(p, q) = (6, 5) : 6499</title></rect><rect class="kq-cell to-cycle" x="201" y="137" width="24" height="20" rx="3"><title>(p, q) = (6, 6) : 6589</title></rect><text class="kq-tick" x="38" y="173" text-anchor="end">7</text><rect class="kq-cell to-cycle" x="45" y="159" width="24" height="20" rx="3"><title>(p, q) = (7, 0) : 6EE8</title></rect><rect class="kq-cell is-cycle" x="71" y="159" width="24" height="20" rx="3"><title>(p, q) = (7, 1) : 70D8</title></rect><rect class="kq-cell to-cycle" x="97" y="159" width="24" height="20" rx="3"><title>(p, q) = (7, 2) : 71C8</title></rect><rect class="kq-cell is-cycle" x="123" y="159" width="24" height="20" rx="3"><title>(p, q) = (7, 3) : 72B8</title></rect><rect class="kq-cell to-cycle" x="149" y="159" width="24" height="20" rx="3"><title>(p, q) = (7, 4) : 73A8</title></rect><rect class="kq-cell is-cycle" x="175" y="159" width="24" height="20" rx="3"><title>(p, q) = (7, 5) : 7498</title></rect><rect class="kq-cell to-cycle" x="201" y="159" width="24" height="20" rx="3"><title>(p, q) = (7, 6) : 7588</title></rect><rect class="kq-cell to-cycle" x="227" y="159" width="24" height="20" rx="3"><title>(p, q) = (7, 7) : 7678</title></rect><text class="kq-tick" x="38" y="195" text-anchor="end">8</text><rect class="kq-cell to-cycle" x="45" y="181" width="24" height="20" rx="3"><title>(p, q) = (8, 0) : 7EE7</title></rect><rect class="kq-cell to-cycle" x="71" y="181" width="24" height="20" rx="3"><title>(p, q) = (8, 1) : 80D7</title></rect><rect class="kq-cell to-cycle" x="97" y="181" width="24" height="20" rx="3"><title>(p, q) = (8, 2) : 81C7</title></rect><rect class="kq-cell to-cycle" x="123" y="181" width="24" height="20" rx="3"><title>(p, q) = (8, 3) : 82B7</title></rect><rect class="kq-cell to-cycle" x="149" y="181" width="24" height="20" rx="3"><title>(p, q) = (8, 4) : 83A7</title></rect><rect class="kq-cell to-cycle" x="175" y="181" width="24" height="20" rx="3"><title>(p, q) = (8, 5) : 8497</title></rect><rect class="kq-cell to-cycle" x="201" y="181" width="24" height="20" rx="3"><title>(p, q) = (8, 6) : 8587</title></rect><rect class="kq-cell to-cycle" x="227" y="181" width="24" height="20" rx="3"><title>(p, q) = (8, 7) : 8677</title></rect><rect class="kq-cell to-cycle" x="253" y="181" width="24" height="20" rx="3"><title>(p, q) = (8, 8) : 8767</title></rect><text class="kq-tick" x="38" y="217" text-anchor="end">9</text><rect class="kq-cell to-cycle" x="45" y="203" width="24" height="20" rx="3"><title>(p, q) = (9, 0) : 8EE6</title></rect><rect class="kq-cell is-cycle" x="71" y="203" width="24" height="20" rx="3"><title>(p, q) = (9, 1) : 90D6</title></rect><rect class="kq-cell to-cycle" x="97" y="203" width="24" height="20" rx="3"><title>(p, q) = (9, 2) : 91C6</title></rect><rect class="kq-cell is-fixed" x="123" y="203" width="24" height="20" rx="3"><title>(p, q) = (9, 3) : 92B6</title></rect><rect class="kq-cell to-cycle" x="149" y="203" width="24" height="20" rx="3"><title>(p, q) = (9, 4) : 93A6</title></rect><rect class="kq-cell is-cycle" x="175" y="203" width="24" height="20" rx="3"><title>(p, q) = (9, 5) : 9496</title></rect><rect class="kq-cell to-cycle" x="201" y="203" width="24" height="20" rx="3"><title>(p, q) = (9, 6) : 9586</title></rect><rect class="kq-cell is-cycle" x="227" y="203" width="24" height="20" rx="3"><title>(p, q) = (9, 7) : 9676</title></rect><rect class="kq-cell to-cycle" x="253" y="203" width="24" height="20" rx="3"><title>(p, q) = (9, 8) : 9766</title></rect><rect class="kq-cell to-cycle" x="279" y="203" width="24" height="20" rx="3"><title>(p, q) = (9, 9) : 9856</title></rect><text class="kq-tick" x="38" y="239" text-anchor="end">10</text><rect class="kq-cell to-cycle" x="45" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 0) : 9EE5</title></rect><rect class="kq-cell to-cycle" x="71" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 1) : A0D5</title></rect><rect class="kq-cell to-cycle" x="97" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 2) : A1C5</title></rect><rect class="kq-cell to-cycle" x="123" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 3) : A2B5</title></rect><rect class="kq-cell to-cycle" x="149" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 4) : A3A5</title></rect><rect class="kq-cell to-cycle" x="175" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 5) : A495</title></rect><rect class="kq-cell to-cycle" x="201" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 6) : A585</title></rect><rect class="kq-cell to-cycle" x="227" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 7) : A675</title></rect><rect class="kq-cell to-cycle" x="253" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 8) : A765</title></rect><rect class="kq-cell to-cycle" x="279" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 9) : A855</title></rect><rect class="kq-cell to-cycle" x="305" y="225" width="24" height="20" rx="3"><title>(p, q) = (10, 10) : A945</title></rect><text class="kq-tick" x="38" y="261" text-anchor="end">11</text><rect class="kq-cell to-cycle" x="45" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 0) : AEE4</title></rect><rect class="kq-cell is-cycle" x="71" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 1) : B0D4</title></rect><rect class="kq-cell to-cycle" x="97" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 2) : B1C4</title></rect><rect class="kq-cell is-cycle" x="123" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 3) : B2B4</title></rect><rect class="kq-cell to-cycle" x="149" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 4) : B3A4</title></rect><rect class="kq-cell is-cycle" x="175" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 5) : B494</title></rect><rect class="kq-cell to-cycle" x="201" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 6) : B584</title></rect><rect class="kq-cell is-cycle" x="227" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 7) : B674</title></rect><rect class="kq-cell to-cycle" x="253" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 8) : B764</title></rect><rect class="kq-cell is-cycle" x="279" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 9) : B854</title></rect><rect class="kq-cell to-cycle" x="305" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 10) : B944</title></rect><rect class="kq-cell to-cycle" x="331" y="247" width="24" height="20" rx="3"><title>(p, q) = (11, 11) : BA34</title></rect><text class="kq-tick" x="38" y="283" text-anchor="end">12</text><rect class="kq-cell to-cycle" x="45" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 0) : BEE3</title></rect><rect class="kq-cell to-cycle" x="71" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 1) : C0D3</title></rect><rect class="kq-cell to-cycle" x="97" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 2) : C1C3</title></rect><rect class="kq-cell to-cycle" x="123" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 3) : C2B3</title></rect><rect class="kq-cell to-cycle" x="149" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 4) : C3A3</title></rect><rect class="kq-cell to-cycle" x="175" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 5) : C493</title></rect><rect class="kq-cell to-fixed" x="201" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 6) : C583</title></rect><rect class="kq-cell to-cycle" x="227" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 7) : C673</title></rect><rect class="kq-cell to-cycle" x="253" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 8) : C763</title></rect><rect class="kq-cell to-fixed" x="279" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 9) : C853</title></rect><rect class="kq-cell to-cycle" x="305" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 10) : C943</title></rect><rect class="kq-cell to-cycle" x="331" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 11) : CA33</title></rect><rect class="kq-cell to-cycle" x="357" y="269" width="24" height="20" rx="3"><title>(p, q) = (12, 12) : CB23</title></rect><text class="kq-tick" x="38" y="305" text-anchor="end">13</text><rect class="kq-cell to-cycle" x="45" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 0) : CEE2</title></rect><rect class="kq-cell is-cycle" x="71" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 1) : D0D2</title></rect><rect class="kq-cell to-cycle" x="97" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 2) : D1C2</title></rect><rect class="kq-cell is-cycle" x="123" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 3) : D2B2</title></rect><rect class="kq-cell to-cycle" x="149" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 4) : D3A2</title></rect><rect class="kq-cell is-cycle" x="175" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 5) : D492</title></rect><rect class="kq-cell to-cycle" x="201" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 6) : D582</title></rect><rect class="kq-cell is-cycle" x="227" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 7) : D672</title></rect><rect class="kq-cell to-cycle" x="253" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 8) : D762</title></rect><rect class="kq-cell is-cycle" x="279" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 9) : D852</title></rect><rect class="kq-cell to-cycle" x="305" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 10) : D942</title></rect><rect class="kq-cell is-cycle" x="331" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 11) : DA32</title></rect><rect class="kq-cell to-cycle" x="357" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 12) : DB22</title></rect><rect class="kq-cell to-cycle" x="383" y="291" width="24" height="20" rx="3"><title>(p, q) = (13, 13) : DC12</title></rect><text class="kq-tick" x="38" y="327" text-anchor="end">14</text><rect class="kq-cell to-cycle" x="45" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 0) : DEE1</title></rect><rect class="kq-cell to-cycle" x="71" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 1) : E0D1</title></rect><rect class="kq-cell to-cycle" x="97" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 2) : E1C1</title></rect><rect class="kq-cell to-cycle" x="123" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 3) : E2B1</title></rect><rect class="kq-cell to-cycle" x="149" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 4) : E3A1</title></rect><rect class="kq-cell to-cycle" x="175" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 5) : E491</title></rect><rect class="kq-cell to-cycle" x="201" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 6) : E581</title></rect><rect class="kq-cell to-cycle" x="227" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 7) : E671</title></rect><rect class="kq-cell to-cycle" x="253" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 8) : E761</title></rect><rect class="kq-cell to-cycle" x="279" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 9) : E851</title></rect><rect class="kq-cell to-cycle" x="305" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 10) : E941</title></rect><rect class="kq-cell to-cycle" x="331" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 11) : EA31</title></rect><rect class="kq-cell to-cycle" x="357" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 12) : EB21</title></rect><rect class="kq-cell to-cycle" x="383" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 13) : EC11</title></rect><rect class="kq-cell to-cycle" x="409" y="313" width="24" height="20" rx="3"><title>(p, q) = (14, 14) : ED01</title></rect><line class="kq-path" x1="83.0" y1="81.0" x2="291.0" y2="301.0"/><circle class="kq-head" cx="291.0" cy="301.0" r="3.5"/><line class="kq-path" x1="291.0" y1="301.0" x2="135.0" y2="257.0"/><circle class="kq-head" cx="135.0" cy="257.0" r="3.5"/><line class="kq-path" x1="135.0" y1="257.0" x2="239.0" y2="213.0"/><circle class="kq-head" cx="239.0" cy="213.0" r="3.5"/><line class="kq-path" x1="239.0" y1="213.0" x2="83.0" y2="81.0"/><circle class="kq-head" cx="83.0" cy="81.0" r="3.5"/><line class="kq-path" x1="83.0" y1="81.0" x2="291.0" y2="301.0"/><circle class="kq-head" cx="291.0" cy="301.0" r="3.5"/><circle class="kq-start" cx="83.0" cy="81.0" r="7"/></svg>

    <!-- /gen -->

    <!-- gen 5 -->

    <span class="viz-legend"><span><i class="kq-key-fixed"></i>נקודת השבת 92B6 : ‏(p, q) = (9, 3)</span><span><i class="kq-key-cycle"></i>זוגות שעל מחזור</span><span><i class="kq-key-tofixed"></i>מגיעים לנקודת השבת</span><span><i class="kq-key-tocycle"></i>נכנסים למחזור</span><span><i class="kq-key-path"></i>המסלול של 1234 (העיגול : ההתחלה)</span></span>

    <!-- /gen -->

    **השוואה לשלוש ספרות.** בשלוש ספרות התהליך תלוי בפרמטר אחד, ותנאי השבת \( b = 2d \)
    מחייב בסיס זוגי (שאלה 0012, סעיף ג). בארבע ספרות יש שני פרמטרים, ותנאי השבת הוא המערכת
    \( p = 3q \), \( B = 5q \), ולכן הבסיס חייב להתחלק ב-5.

    **אימות.** הבדיקות של השאלה מוצאות בחיפוש ממצה את כל נקודות השבת בכל בסיס מ-2 עד 60
    (על הזוגות \( (p, q) \), מספיק כי כל נקודת שבת היא ערך של זוג), ומריצות כל מספר בבסיסים
    2 עד 16.

    **נסו בעצמכם.** בוחרים בסיס ומקלידים ארבע ספרות : הטבלה מראה את המיון והחיסור צעד אחרי
    צעד עד שערך חוזר, השורה מתחת מסבירה את \( p \), \( q \), את הספרות של \( F \) ואם הגענו
    לנקודת שבת או למחזור, המפה מראה את המסלול על הזוגות, והטבלה שמתחת אומרת לאן מגיעים כל
    המספרים של הבסיס :

    <div class="explorer" data-kind="kap4base" data-b="15" data-x="1234"></div>

    #### סיבוכיות { .sol-cost }

    צעד הוא \( O(1) \). המסלול נעצר אחרי לכל היותר מספר הזוגות, \( B(B + 1) / 2 \) צעדים,
    כי הערך תלוי רק בזוג. החיפוש של נקודות השבת עובר על \( O(B^2) \) זוגות במקום על \( B^4 \)
    מספרים, ולכן גם בסיס 300 מיידי.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : אפסים משלימים"
    הפתרון הנפוץ ביותר שנכשל הוא מיון של הספרות **בלי** לרפד באפסים. אז 95 הופך ל-"95"
    ו-"59", ההפרש הוא 36 במקום 9441, וגם ההוכחה של סעיף ב משתנה. מספר בן פחות מארבע
    ספרות הוא עדיין מספר בן ארבע ספרות בשאלה הזו.

??? trap "מלכודת : להעתיק את ההוכחה של שלוש ספרות"
    בשלוש ספרות ספרת האמצע מתבטלת וההפרש הוא כפולה של 99. מי שמניח שגם כאן האמצע
    מתבטל מקבל "כפולה של 999" ומפספס את האיבר \( 90q \) : גם \( b \) וגם \( c \)
    מחליפות מקום בין שני המספרים, ולכן נשארים שני פרמטרים ולא אחד.

??? trap "מלכודת : נקודת שבת אינה מבטיחה התכנסות"
    בבסיס 10 כל מספר מגיע ל-6174, ומפתה להסיק שבכל בסיס עם נקודת שבת זה כך. בבסיס 15
    נקודת השבת 92B6 קיימת, אבל רק כ-4% מהמספרים מגיעים אליה, והשאר נכנסים למחזורים. לולאה
    "עד שהערך לא משתנה" בבסיס 15 תיתקע על רוב הקלטים.

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
