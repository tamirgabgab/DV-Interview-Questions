---
id: 4
title: שלוש קופסאות עם תוויות שגויות
level: junior
difficulty: medium
tags: [logic-puzzles, algorithms, python, systemverilog]
source: ""
added: 2026-10-15
---

## השאלה

לפניכם שלוש קופסאות סגורות. באחת יש רק כדורים **אדומים**, באחרת רק כדורים **שחורים**,
ובשלישית יש **גם אדומים וגם שחורים**. על כל קופסה מודבקת תווית אחת: "אדום", "שחור"
ו"אדום ושחור".

<!-- gen 0 -->

<svg class="figure" viewBox="0 0 600 190" role="img" aria-label="שלוש קופסאות סגורות עם התוויות אדום, שחור, ואדום ושחור"><g text-anchor="middle"><g><polygon class="crate-top" points="20,50 50,20 200,20 170,50"/><polygon class="crate-side" points="170,50 200,20 200,120 170,150"/><rect class="crate-front" x="20" y="50" width="150" height="100"/><text class="crate-text" x="125" y="42" font-size="20">?</text><text class="crate-text" x="95" y="108" font-size="22">אדום</text><text class="tick" x="95" y="178" font-size="14" direction="rtl">קופסה 0</text></g><g><polygon class="crate-top" points="220,50 250,20 400,20 370,50"/><polygon class="crate-side" points="370,50 400,20 400,120 370,150"/><rect class="crate-front" x="220" y="50" width="150" height="100"/><text class="crate-text" x="325" y="42" font-size="20">?</text><text class="crate-text" x="295" y="108" font-size="22">שחור</text><text class="tick" x="295" y="178" font-size="14" direction="rtl">קופסה 1</text></g><g><polygon class="crate-top" points="420,50 450,20 600,20 570,50"/><polygon class="crate-side" points="570,50 600,20 600,120 570,150"/><rect class="crate-front" x="420" y="50" width="150" height="100"/><text class="crate-text" x="525" y="42" font-size="20">?</text><text class="crate-text" x="495" y="94" font-size="22">אדום</text><text class="crate-text" x="495" y="124" font-size="22">ושחור</text><text class="tick" x="495" y="178" font-size="14" direction="rtl">קופסה 2</text></g></g></svg>

<!-- /gen -->

**כל התוויות שגויות.** אי אפשר להציץ לתוך הקופסאות, אבל אפשר לבקש דגימה: מצביעים על
קופסה ומקבלים ממנה כדור אחד שנבחר באקראי.

??? interviewer "מה המראיין בודק"
    - **הבנה ולא ניחוש:** לנמק למה הבחירה של הקופסה שדוגמים ממנה היא היחידה שמבטיחה
      תשובה, ולא רק לנקוב במספר.
    - **רשימת המקרים:** לזהות כמה סידורים של תוכן בכלל אפשריים כשכל התוויות שגויות.
    - **מהחידה לקוד:** לתרגם נימוק מילולי לפונקציה נקייה, ולזהות שהתיקון הוא פעולה
      מוכרת על מערך.
    - **פרטים קטנים בקוד:** אינדקסים מעגליים, ומה `%` עושה למספר שלילי בכל שפה.

---

### סעיף א

מהו המספר **המינימלי** של דגימות שמבטיח שתוכלו לתקן את כל התוויות?

??? tip "רמז 1"
    על איזו קופסה אנחנו יודעים בוודאות שיש בה כדורים **מצבע אחד בלבד**?

??? tip "רמז 2"
    כתבו את כל הסידורים של התוכן שבהם אף תווית לא נכונה. כמה כאלה יש, ובמה הם נבדלים?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מספיקה **דגימה אחת**, מהקופסה שעליה כתוב "אדום ושחור".

    #### הרעיון { .sol-idea }

    התווית על הקופסה "אדום ושחור" שגויה, ולכן היא **לא** מעורבת: יש בה רק אדומים או רק
    שחורים. כדור אחד מספיק כדי לדעת איזה מהשניים, ומשם שאר התוויות נקבעות בכוח.

    #### למה זה נכון { .sol-proof }

    מכיוון שכל שלוש התוויות שגויות, יש רק **שני סידורים אפשריים** של התוכן:

    | התווית על הקופסה | אדום | שחור | אדום ושחור |
    |------------------|------|------|------------|
    | תוכן אפשרי, סידור 1 | שחור | אדום ושחור | **אדום** |
    | תוכן אפשרי, סידור 2 | אדום ושחור | אדום | **שחור** |

    בעמודה של "אדום ושחור" שני הסידורים נבדלים בצבע אחד וברור, ולכן כדור אחד מכריע בין
    הסידורים:

    ```mermaid
    flowchart TD
        D["שולפים כדור אחד מהקופסה<br/>שהתווית שלה: אדום ושחור"] --> Q{"איזה צבע יצא?"}
        Q -- "אדום" --> A["הקופסה הזו: אדום<br/>התווית אדום: שחור<br/>התווית שחור: אדום ושחור"]
        Q -- "שחור" --> B["הקופסה הזו: שחור<br/>התווית שחור: אדום<br/>התווית אדום: אדום ושחור"]
    ```

    **הכלל:** אם יצא כדור בצבע \( c \), הקופסה המעורבת-לכאורה היא \( c \). הקופסה
    שהתווית שלה \( c \) לא יכולה להכיל \( c \) (התווית שגויה) וגם לא את התערובת (כי
    התערובת היא בקופסה השלישית), ולכן היא מכילה את **הצבע השני**. הקופסה האחרונה מכילה את
    התערובת.

    **למה דגימה מקופסה אחרת לא מספיקה?** נניח ששולפים מהקופסה שעליה כתוב "אדום" ומקבלים כדור שחור. לפי הטבלה, ייתכן שהיא
    "שחור" (סידור 1) וייתכן שהיא "אדום ושחור" (סידור 2), ואין דרך להכריע. לכן אין הבטחה
    שדגימה אחת תספיק, וזה אותו מצב גם בקופסה "שחור".

---

### סעיף ב

כתבו פונקציה שמקבלת מערך `labels` בגודל 3 של מחרוזות: התוויות של קופסאות 0, 1 ו-2,
**בסדר כלשהו**. ערכי התוויות הם `"RED"`, `"BLACK"` ו-`"MIXED"`. הפונקציה צריכה להחזיר את
התוויות הנכונות.

לרשותכם API נתון, `draw(i)`, ששולף כדור אקראי מקופסה `i` ומחזיר `"RED"` או `"BLACK"`.

=== "SystemVerilog"
    ```systemverilog
    typedef string labels_t[3];

    // Provided API: draws one random ball from box i and returns "RED" or "BLACK".
    function automatic string draw(int i);
    ```

=== "Python"
    ```python
    # Provided API: draws one random ball from box i and returns "RED" or "BLACK".
    def draw(i): ...
    ```

??? success "פתרון 1 – פשוט וישיר"
    !!! answer "תשובה בקצרה"
        דוגמים מהקופסה שהתווית שלה `"MIXED"`, ואז שלושה מעברים על המערך ממלאים מערך
        תוויות חדש לפי הכלל של סעיף א.

    #### הרעיון { .sol-idea }

    מתרגמים את פתרון סעיף א לקוד כמעט מילה במילה, ובונים מערך תוויות **חדש**.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **לולאה** שמוצאת את הקופסה `k` שהתווית שלה `"MIXED"`, ושולפים ממנה כדור.
    2. **תנאי `if`** קובע מה הצבע השני (`other`), והקופסה `k` מקבלת את צבע הכדור.
    3. **לולאה שנייה** מוצאת את הקופסה שהתווית שלה היא צבע הכדור, ומסמנת אותה בצבע השני.
    4. **לולאה שלישית** מוצאת את הקופסה שהתווית שלה היא הצבע השני, ומסמנת אותה `"MIXED"`.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function fix_labels_simple" linenums="1" hl_lines="9 14"
        function automatic labels_t fix_labels_simple(labels_t labels);
          labels_t fixed;
          int      k;
          string   ball, other;

          // 1. Find the box labelled MIXED and draw one ball from it.
          foreach (labels[i])
            if (labels[i] == "MIXED") k = i;
          ball = draw(k);   // (1)!

          // 2. That box really holds only `ball`-coloured balls.
          if (ball == "RED") other = "BLACK";
          else               other = "RED";
          fixed[k] = ball;   // (2)!

          // 3. The box labelled `ball` cannot hold `ball` -> it holds `other`.
          foreach (labels[i])
            if (labels[i] == ball) fixed[i] = other;   // (3)!

          // 4. The box labelled `other` holds the mix.
          foreach (labels[i])
            if (labels[i] == other) fixed[i] = "MIXED";

          return fixed;
        endfunction
        ```

        1. הדגימה היחידה בכל הפונקציה. היא מהקופסה `k`, שתוויתה `"MIXED"`, כי רק עליה ידוע
           בוודאות שיש בה צבע אחד.
        2. ‏`fixed` הוא מערך חדש, ולכן אפשר למלא אותו לפי הכלל בלי לחשוש לדרוס תווית
           שעוד צריך לקרוא מ-`labels`.
        3. הקופסה שתוויתה כצבע הכדור לא יכולה להכיל את הצבע הזה (התווית שגויה) ולא את
           התערובת (היא ב-`k`), ולכן נשאר לה הצבע השני.

    === "Python"
        ```python title="fix_labels_simple" linenums="1" hl_lines="8 13"
        def fix_labels_simple(labels):
            fixed = ["", "", ""]

            # 1. Find the box labelled MIXED and draw one ball from it.
            for i in range(3):
                if labels[i] == "MIXED":
                    k = i
            ball = draw(k)   # (1)!

            # 2. That box really holds only `ball`-coloured balls.
            if ball == "RED":
                other = "BLACK"
            else:
                other = "RED"
            fixed[k] = ball   # (2)!

            # 3. The box labelled `ball` cannot hold `ball` -> it holds `other`.
            for i in range(3):
                if labels[i] == ball:
                    fixed[i] = other

            # 4. The box labelled `other` holds the mix.
            for i in range(3):
                if labels[i] == other:
                    fixed[i] = "MIXED"

            return fixed
        ```

        1. הדגימה היחידה בכל הפונקציה, מהקופסה שתוויתה `"MIXED"`. ב-Python אפשר לקצר
           ל-`k = labels.index("MIXED")`.
        2. ‏`fixed` הוא מערך חדש, ולכן הכלל ממולא בלי לדרוס תוויות שעוד צריך לקרוא.

    #### סיבוכיות { .sol-cost }

    הפתרון נכון וקל לקריאה, אבל הוא עובר על המערך שלוש פעמים ומחזיק מערך נוסף. עם שלוש
    קופסאות זה \( O(1) \), אבל הוא לא מנצל את המבנה של הבעיה.

??? success "פתרון 2 – אופטימלי: שתי החלפות במקום"
    !!! answer "תשובה בקצרה"
        התיקון הוא **סיבוב** של שלוש התוויות, ולכן אחרי הדגימה מספיקות **שתי החלפות
        במקום**, בלי מערך נוסף ובלי חיפושים נוספים.

    #### הרעיון { .sol-idea }

    אחרי שמוצאים את `k` ושולפים כדור, לא צריך לחפש שוב. שתי הקופסאות האחרות הן
    \( (k+1) \bmod 3 \) ו-\( (k-1) \bmod 3 \), ובדיקה אחת אומרת איזו מהן נושאת את התווית של
    צבע הכדור:

    - **‏`same`:** הקופסה שהתווית שלה שווה לצבע הכדור.
    - **‏`other`:** הקופסה שהתווית שלה היא הצבע השני.

    לפי הכלל מסעיף א, שלוש התוויות פשוט **מסתובבות** בין הקופסאות:

    ```mermaid
    flowchart LR
        S["same<br/>התווית: צבע הכדור"] -- "צבע הכדור עובר ל-k" --> K["k<br/>התווית: MIXED"]
        K -- "MIXED עובר ל-other" --> O["other<br/>התווית: הצבע השני"]
        O -- "הצבע השני עובר ל-same" --> S
    ```

    סיבוב של שלושה איברים (מחזור באורך 3) שווה בדיוק ל**שתי החלפות**.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מוצאים את `k`** (התווית `"MIXED"`) ושולפים ממנה כדור.
    2. **מזהים את `same` ואת `other`** בבדיקה אחת על שתי הקופסאות האחרות.
    3. **החלפה בין `k` ל-`same`:** קופסה `k` מקבלת את צבע הכדור, ו-`same` מקבלת זמנית את
       `"MIXED"`.
    4. **החלפה בין `same` ל-`other`:** `same` מקבלת את הצבע השני, ו-`other` מקבלת את
       `"MIXED"`.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function fix_labels" hl_lines="15 16"
        function automatic void fix_labels(ref labels_t labels);
          int    k, n1, n2, same, other;
          string ball, tmp;

          foreach (labels[i])
            if (labels[i] == "MIXED") k = i;
          ball = draw(k);                       // the true colour of box k

          n1    = (k + 1) % 3;                  // the two other boxes
          n2    = (k + 2) % 3;                  // (k + 2) % 3 == (k - 1) mod 3 (1)
          same  = (labels[n1] == ball) ? n1 : n2;   // (2)!
          other = (same == n1) ? n2 : n1;

          // Rotate the three labels with two swaps.
          tmp = labels[k];    labels[k]    = labels[same];  labels[same]  = tmp;   // (3)!
          tmp = labels[same]; labels[same] = labels[other]; labels[other] = tmp;
        endfunction
        ```

        1. ‏`(k + 2) % 3` במקום `(k - 1) % 3`: ב-SystemVerilog, כמו ב-C, `%` שומר על הסימן
           של המחולק, ולכן עבור `k = 0` היה מתקבל `-1`, אינדקס לא חוקי. חיבור 2 שקול לחיסור
           1 מודולו 3 ונשאר חיובי.
        2. בדיקה אחת במקום לולאה: מבין שתי הקופסאות האחרות, זו שתוויתה כצבע הכדור היא
           `same`, והשנייה היא `other`.
        3. ההחלפה דרך `tmp` היא הדרך של SystemVerilog להחליף שני איברים במערך. אחרי
           ההחלפה הראשונה `k` כבר נכונה, ואחרי השנייה גם `same` ו-`other`.

    === "Python"
        ```python title="fix_labels" hl_lines="10 11"
        def fix_labels(labels):
            k = labels.index("MIXED")
            ball = draw(k)                      # the true colour of box k

            n1, n2 = (k + 1) % 3, (k + 2) % 3   # the two other boxes (1)
            same = n1 if labels[n1] == ball else n2
            other = n2 if same == n1 else n1

            # Rotate the three labels with two swaps.
            labels[k], labels[same] = labels[same], labels[k]   # (2)!
            labels[same], labels[other] = labels[other], labels[same]
            return labels
        ```

        1. ב-Python דווקא `(k - 1) % 3` היה נותן 2 עבור `k = 0`, אבל הקוד נשמר זהה לגרסת
           ה-SystemVerilog כדי שאותו נימוק יעבוד בשתי השפות.
        2. החלפה ב-Python היא השמה מרובה, בלי משתנה עזר. שתי ההחלפות יחד הן סיבוב של
           שלוש התוויות.

    #### למה זה נכון { .sol-proof }

    **דוגמת הרצה.** נניח שהקלט הוא `{"RED", "BLACK", "MIXED"}`, והתוכן האמיתי הוא סידור 1 מסעיף א.
    לכן \( k = 2 \), והכדור שנשלף אדום. השכנים הם `n1 = 0` ו-`n2 = 1`. בקופסה 0 התווית
    `"RED"`, ולכן `same = 0` ו-`other = 1`:

    | שלב | התוויות |
    |-----|---------|
    | התחלה | <span class="arr"><span>RED</span><span>BLACK</span><span class="hl">MIXED</span></span> |
    | החלפה 1, בין `k=2` ל-`same=0` | <span class="arr"><span class="hl">MIXED</span><span>BLACK</span><span class="hl">RED</span></span> |
    | החלפה 2, בין `same=0` ל-`other=1` | <span class="arr"><span class="hl">BLACK</span><span class="hl">MIXED</span><span>RED</span></span> |

    התוצאה `{"BLACK", "MIXED", "RED"}` תואמת בדיוק לסידור 1.

    #### סיבוכיות { .sol-cost }

    | | פתרון 1 | פתרון 2 |
    |-|---------|---------|
    | מעברים על המערך | שלושה | אחד (למציאת `k`) |
    | זיכרון נוסף | מערך חדש | שני אינדקסים |
    | פעולות על התוויות | שלוש השמות למערך החדש | בדיוק שתי החלפות במקום |
    | דגימות | אחת | אחת |

    כשיש רק 3 קופסאות שני הפתרונות הם \( O(1) \). בראיון היתרון של פתרון 2 הוא בעיקר
    הזיהוי שמדובר ב**סיבוב** של התוויות, כלומר תמורה מחזורית, ושכל סיבוב כזה מתבצע בשתי
    החלפות.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: מודולו של מספר שלילי"
    ב-SystemVerilog וב-C הביטוי `(k - 1) % 3` נותן `-1` כש-`k = 0`, וגישה למערך באינדקס
    הזה היא באג שקט. ב-Python אותו ביטוי נותן 2. כשכותבים אינדקס מעגלי, מוסיפים את
    הגודל פחות אחת (`k + 2`) או בודקים את הסימן במפורש.

??? trap "מלכודת: לדגום מהקופסה הלא נכונה"
    דגימה מהקופסה "אדום" או "שחור" נראית טבעית, אבל כדור אחד משם לא מכריע בין שני
    הסידורים האפשריים. רק הקופסה שתוויתה "אדום ושחור" ידועה מראש כחד-צבעית.

??? followup "שאלות המשך"
    - **חלק מהתוויות שגויות:** מה קורה אם רק **חלק** מהתוויות שגויות? אז דגימה אחת כבר לא
      מספיקה בכל המקרים. נסו למצוא דוגמה.
    - **בשפה מתמטית:** שני הסידורים האפשריים הם שתי התמורות בלי נקודת שבת (derangements)
      של שלושה איברים. כמה תמורות כאלה יש לארבעה איברים?
    - **ארבע קופסאות:** עם ארבע קופסאות וארבעה סוגי תוכן, האם עדיין מספיקה דגימה אחת?
