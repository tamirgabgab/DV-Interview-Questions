---
id: 66
title: מיזוג קטעים – קטעים חופפים, הגובה הכולל בכל נקודה, והשיא מול סף
level: junior
difficulty: medium
kind: code
tags: [algorithms, sorting, python, systemverilog]
source: "שאלה קלאסית (Merge Intervals), וההכללה לקטעים עם גובה היא של בעל האתר"
added: 2026-10-29
---

## השאלה

נתונה רשימה של **קטעים** על ציר המספרים. קטע נתון כזוג \( [s, e] \) עם \( s \le e \) : הוא מכיל
את כל הנקודות מ-\( s \) עד \( e \), כולל שתי הקצוות. שני קטעים **חופפים** אם יש נקודה שנמצאת
בשניהם. מזגו כל קבוצה של קטעים חופפים לקטע אחד, והחזירו את הקטעים שנשארו, ממוינים.

דוגמה : מהקטעים <span dir="ltr">[1, 3], [2, 6], [8, 10], [15, 18]</span> מתקבלים
<span dir="ltr">[1, 6], [8, 10], [15, 18]</span>, כי 2 נמצא גם ב-<span dir="ltr">[1, 3]</span>
וגם ב-<span dir="ltr">[2, 6]</span>.

**ההסכמה על הקצוות :** הקטעים סגורים, ולכן <span dir="ltr">[1, 4]</span> ו-<span dir="ltr">[4, 5]</span>
חופפים בנקודה 4 ומתמזגים ל-<span dir="ltr">[1, 5]</span>. בראיון כדאי לשאול את זה במפורש, כי
בחצאי קטעים (סעיף ב) אותם שני קטעים רק נוגעים זה בזה.

**ההקשר באימות :** מפת רגיסטרים או זיכרון היא רשימה של טווחי כתובות, ובדיקת התקינות שלה היא
מיזוג של קטעים (סעיף א) : טווחים שמתמזגים חופפים, כלומר שתי יחידות עונות לאותה כתובת, והמרווחים
בין הקטעים הממוזגים הם כתובות שאף יחידה לא עונה להן. כשכל טווח נושא משקל, למשל רוחב הפס
שכל master צורך בחלון הזמן שבו הוא פעיל, או ההספק של כל בלוק בזמן שהוא דולק, השאלה היא
מה הסכום בכל רגע ואיפה הוא חוצה את התקציב (סעיפים ב ו-ג). אותה סריקה נותנת מטרייס של
טרנזקציות את השיא של הבתים הממתינים לתשובה (outstanding bytes) : כל טרנזקציה היא קטע
מהבקשה עד התשובה, בגובה מספר הבתים שלה. זו ההכללה של שאלה [0062](0062-how-many-tags.md),
שבה הגובה של כל טרנזקציה הוא 1 והשיא הוא מספר ה-tags.

- **סעיף א – מיזוג :** כתבו פונקציה שמקבלת את הרשימה ומחזירה את הקטעים הממוזגים.
- **סעיף ב – גובה כולל :** כל קטע הוא עכשיו שלשה \( (s, e, h) \) : הוא מכסה את חצי הקטע
  \( [s, e) \), כלומר מ-\( s \) ועד \( e \) בלי \( e \) עצמו, עם גובה \( h \ge 1 \). הגובה הכולל
  בנקודה הוא סכום הגבהים של הקטעים שמכסים אותה. החזירו את **החתיכות** : הקטעים המקסימליים
  שבהם הגובה הכולל קבוע, כל אחת כשלשה \( (s, e, \text{total}) \), בלי החתיכות שבהן הגובה 0.
  דוגמה : מ-<span dir="ltr">(1, 7, 7)</span> ו-<span dir="ltr">(2, 6, 4)</span> מתקבלות
  <span dir="ltr">(1, 2, 7), (2, 6, 11), (6, 7, 7)</span>.
- **סעיף ג – השיא והסף :** מה הגובה הכולל הגדול ביותר, ואיפה הוא מתקבל? ואילו טווחים
  נמצאים בגובה כולל של לפחות סף \( T \) נתון?

??? interviewer "מה המראיין בודק"
    - **המיון קודם :** האם המועמד ממיין לפי ההתחלה, ורואה שאחרי המיון קטע יכול לחפוף רק
      לקטע הממוזג **האחרון**, ולא לקטע הקודם ברשימה המקורית.
    - **ההסכמה על הקצוות :** האם הוא שואל מה קורה לשני קטעים שנוגעים, ומתרגם את התשובה
      לסימן אחד בקוד, `<=` או `<`.
    - **מאירועים לסכום :** האם הוא מפרק כל קטע לשני אירועים, שומר סכום רץ, ויודע מה לעשות
      כששני אירועים נופלים על אותו מיקום.
    - **פלט קנוני :** חתיכות באורך אפס, חתיכות שכנות עם אותו גובה, ורווחים : האם הפלט שלו
      הוא רשימה אחת מוגדרת היטב שאפשר להשוות אליה במבחן.

---

### סעיף א – מיזוג קטעים חופפים

??? tip "רמז 1"
    לפני כל דבר אחר, מיינו את הקטעים לפי ההתחלה. אחרי המיון, אם קטע לא חופף לקטע הממוזג
    האחרון, האם הוא יכול לחפוף לקטע ממוזג מוקדם יותר?

??? tip "רמז 2"
    שמרו רשימת פלט. לכל קטע לפי הסדר : אם ההתחלה שלו אינה גדולה מהסוף של הקטע האחרון
    בפלט, הוא חופף לו, והסוף של האחרון הופך למקסימום של שני הסופים. אחרת הוא פותח קטע חדש.

<div class="selfcheck" data-answer="3" data-show="3 : אחרי המיון [1, 3], [2, 5], [6, 9], [9, 10], [12, 14] מתמזגים ל-[1, 5], [6, 10] ו-[12, 14]" data-hint="מיינו לפי ההתחלה. [9, 10] מתחיל בדיוק בסוף של [6, 9], ובקטעים סגורים זה חופף." markdown>
כמה קטעים נשארים אחרי המיזוג של <span dir="ltr">[2, 5], [1, 3], [6, 9], [9, 10], [12, 14]</span>?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ממיינים לפי ההתחלה ועוברים על הקטעים עם רשימת פלט. קטע שמתחיל בסוף של הקטע הממוזג
        האחרון או לפניו (`<=`) מאריך אותו : הסוף הופך למקסימום של שני הסופים. קטע שמתחיל
        אחרי הסוף פותח קטע חדש בפלט. בדוגמה : <span dir="ltr">[1, 6], [8, 10], [15, 18]</span>.

    <!-- cost: זמן \( O(n \log n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **מונחים.** קטע **סגור** \( [s, e] \) מכיל את שתי הקצוות שלו. שני קטעים \( [s_1, e_1] \)
    ו-\( [s_2, e_2] \) חופפים בדיוק כאשר \( s_1 \le e_2 \) וגם \( s_2 \le e_1 \) : כל אחד מתחיל
    לפני שהשני נגמר. קטעים שרק **נוגעים**, כמו <span dir="ltr">[1, 4]</span>
    ו-<span dir="ltr">[4, 5]</span>, חופפים בנקודה אחת, ולכן מתמזגים. **מיזוג** של קבוצת
    קטעים הוא הקטע מההתחלה הקטנה ביותר עד הסוף הגדול ביותר, וקבוצה נמזגת כשאפשר ללכת
    מכל קטע בה לכל קטע אחר דרך שרשרת של חפיפות.

    **למה למיין.** בלי סדר, כל קטע יכול לחפוף לכל קטע אחר, ובדיקה של כל הזוגות היא
    \( O(n^2) \). אחרי מיון לפי ההתחלה, הקטעים הממוזגים שנבנו עד עכשיו זרים זה לזה וממוינים,
    וכל קטע חדש מתחיל במקום שאינו קטן מכל ההתחלות שלפניו. לכן הוא יכול לחפוף רק לקטע
    הממוזג **האחרון** : אם הוא מתחיל אחרי הסוף של האחרון, הוא מתחיל גם אחרי הסוף של כל
    הקודמים לו. כך כל קטע נבדק מול קטע אחד בלבד.

    באיור, הקטעים של הדוגמה ממוינים לפי ההתחלה, ומתחת לציר התוצאה :

    <!-- gen 0 -->

    <svg class="figure iv-fig" viewBox="0 0 640 176" role="img" aria-label="ארבעה קטעים סגורים : [1, 3], [2, 6], [8, 10] ו-[15, 18], ומתחתם התוצאה הממוזגת [1, 6], [8, 10], [15, 18]"><line class="grid" x1="64" x2="64" y1="10" y2="116"/><text class="tick" x="64" y="130" text-anchor="middle">0</text><line class="grid" x1="126.222" x2="126.222" y1="10" y2="116"/><text class="tick" x="126.222" y="130" text-anchor="middle">2</text><line class="grid" x1="188.444" x2="188.444" y1="10" y2="116"/><text class="tick" x="188.444" y="130" text-anchor="middle">4</text><line class="grid" x1="250.667" x2="250.667" y1="10" y2="116"/><text class="tick" x="250.667" y="130" text-anchor="middle">6</text><line class="grid" x1="312.889" x2="312.889" y1="10" y2="116"/><text class="tick" x="312.889" y="130" text-anchor="middle">8</text><line class="grid" x1="375.111" x2="375.111" y1="10" y2="116"/><text class="tick" x="375.111" y="130" text-anchor="middle">10</text><line class="grid" x1="437.333" x2="437.333" y1="10" y2="116"/><text class="tick" x="437.333" y="130" text-anchor="middle">12</text><line class="grid" x1="499.556" x2="499.556" y1="10" y2="116"/><text class="tick" x="499.556" y="130" text-anchor="middle">14</text><line class="grid" x1="561.778" x2="561.778" y1="10" y2="116"/><text class="tick" x="561.778" y="130" text-anchor="middle">16</text><line class="grid" x1="624" x2="624" y1="10" y2="116"/><text class="tick" x="624" y="130" text-anchor="middle">18</text><text class="iv-name" x="56" y="27" text-anchor="end">1</text><rect class="iv-bar" x="95.1111" y="14" width="62.2222" height="16" rx="3"><title>[1, 3]</title></rect><text class="iv-name" x="56" y="51" text-anchor="end">2</text><rect class="iv-bar" x="126.222" y="38" width="124.444" height="16" rx="3"><title>[2, 6]</title></rect><text class="iv-name" x="56" y="75" text-anchor="end">3</text><rect class="iv-bar" x="312.889" y="62" width="62.2222" height="16" rx="3"><title>[8, 10]</title></rect><text class="iv-name" x="56" y="99" text-anchor="end">4</text><rect class="iv-bar" x="530.667" y="86" width="93.3333" height="16" rx="3"><title>[15, 18]</title></rect><line class="axis" x1="64" x2="624" y1="116" y2="116"/><text class="iv-name" x="56" y="163" text-anchor="end">merged</text><rect class="iv-merged" x="95.1111" y="150" width="155.556" height="16" rx="3"><title>merged: [1, 6]</title></rect><rect class="iv-merged" x="312.889" y="150" width="62.2222" height="16" rx="3"><title>merged: [8, 10]</title></rect><rect class="iv-merged" x="530.667" y="150" width="93.3333" height="16" rx="3"><title>merged: [15, 18]</title></rect></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="iv-key-bar"></i>קטע מהקלט, ממוין לפי ההתחלה</span><span><i class="iv-key-merged"></i>קטע ממוזג בפלט</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מיון :** לפי ההתחלה \( s \). רשימת הפלט מתחילה ריקה.
    2. **קטע שמאריך :** אם הפלט אינו ריק וההתחלה של הקטע הנוכחי אינה גדולה מהסוף של הקטע
       האחרון בפלט, \( s \le \text{end} \), הקטע חופף לו : הסוף של האחרון הופך
       ל-\( \max(\text{end}, e) \). אם \( e \) קטן יותר, הקטע כולו בפנים ודבר לא משתנה.
    3. **קטע חדש :** אחרת, \( s > \text{end} \), הקטע לא חופף לאף קטע בפלט ונוסף בסופו כמו
       שהוא.
    4. **התשובה :** רשימת הפלט, שהיא כבר ממוינת וזרה.

    </div>

    על הדוגמה, הקטעים כבר ממוינים :

    <!-- gen 2 -->

    | הקטע (ממוין) | הסוף של הקטע הממוזג האחרון | ההחלטה | הפלט אחרי הצעד |
    |:-:|:-:|:-:|:-:|
    | ‏<span dir="ltr">[1, 3]</span> | אין עדיין | אין קטע פתוח | ‏<span dir="ltr">[1, 3]</span> |
    | ‏<span dir="ltr">[2, 6]</span> | ‏3 | ‏<span dir="ltr">2 ≤ 3</span>, הסוף גדל ל-6 | ‏<span dir="ltr">[1, 6]</span> |
    | ‏<span dir="ltr">[8, 10]</span> | ‏6 | ‏<span dir="ltr">8 &gt; 6</span>, קטע חדש | ‏<span dir="ltr">[1, 6] [8, 10]</span> |
    | ‏<span dir="ltr">[15, 18]</span> | ‏10 | ‏<span dir="ltr">15 &gt; 10</span>, קטע חדש | ‏<span dir="ltr">[1, 6] [8, 10] [15, 18]</span> |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="merge" linenums="1" hl_lines="5 6 7"
        def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
            """Merge the closed intervals [start, end] that overlap or touch: sorted by start,
            an interval that starts at or before the end of the last merged one extends it."""
            out: list[list[int]] = []
            for s, e in sorted(intervals):                 # (1)!
                if out and s <= out[-1][1]:                # (2)!
                    out[-1][1] = max(out[-1][1], e)        # (3)!
                else:
                    out.append([s, e])
            return [(s, e) for s, e in out]
        ```

        1. ‏`sorted` ממיין זוגות לפי ההתחלה, ובהתחלה שווה לפי הסוף.
        2. ‏`out[-1]` הוא הקטע הממוזג האחרון. ‏`<=` ולא `<`, כי קטעים סגורים שנוגעים חופפים.
        3. הסוף הופך למקסימום של שני הסופים : קטע שכולו בפנים משאיר אותו כמו שהוא.

    === "SystemVerilog"
        ```systemverilog title="function merge" linenums="1" hl_lines="9 11 12"
        // merge the closed intervals [s, e] that overlap or touch: sorted by start, an interval
        // that starts at or before the end of the last merged one extends it
        typedef struct { int s; int e; } span_t;

        function automatic void merge(input span_t iv[], output span_t out[$]);
          span_t q[$];
          out = {};
          foreach (iv[i]) q.push_back(iv[i]);
          q.sort with (item.s);                                             // (1)!
          foreach (q[i]) begin
            if (out.size() > 0 && q[i].s <= out[$].e) begin                 // (2)!
              if (q[i].e > out[$].e) out[$].e = q[i].e;                     // (3)!
            end else out.push_back(q[i]);
          end
        endfunction
        ```

        1. מיון של התור לפי ההתחלה. שני קטעים עם אותה התחלה יכולים לבוא בכל סדר : השני מהם תמיד מאריך את הראשון.
        2. ‏`out[$]` הוא הקטע הממוזג האחרון. ‏`<=` ולא `<`, כי קטעים סגורים שנוגעים חופפים.
        3. הסוף גדל רק אם הקטע החדש נגמר אחרי האחרון. קטע שכולו בפנים לא משנה דבר.

    #### למה זה נכון { .sol-proof }

    **שמורה :** אחרי שעיברנו על הקטעים \( 0, \dots, i \) (בסדר הממוין), רשימת הפלט היא בדיוק
    המיזוג של הקטעים האלה : קטעים זרים, ממוינים, שכל אחד מהם הוא איחוד של קבוצה שנמזגת,
    וכל שני קטעים בפלט לא חופפים. באינדוקציה על \( i \) :

    - **חפיפה רק עם האחרון :** הקטע \( i \) מתחיל ב-\( s_i \), ו-\( s_i \ge s_j \) לכל
      \( j < i \). כל קטע בפלט פרט לאחרון נגמר לפני ההתחלה של האחרון, ולכן לפני \( s_i \) (כי
      האחרון מתחיל באחד מהקטעים \( j < i \), שמתחיל לפני \( s_i \)). לכן הקטע \( i \) יכול
      לחפוף רק לאחרון, ובדיוק כאשר \( s_i \le \text{end} \).
    - **הארכה :** אם הוא חופף, האיחוד של האחרון עם הקטע \( i \) הוא קטע אחד, מההתחלה של האחרון
      עד \( \max(\text{end}, e_i) \), והוא עדיין זר לקטעים שלפניו.
    - **קטע חדש :** אם \( s_i > \text{end} \), הקטע \( i \) זר לכל הפלט, ונוסף אחרון. הפלט נשאר
      ממוין, כי \( s_i \) גדול מהסוף של האחרון.

    בסוף הפלט הוא המיזוג של כל הקטעים. **הסופיות של הקודמים :** ברגע שקטע חדש נפתח, הקטע
    שלפניו לא ישתנה יותר, כי כל הקטעים הבאים מתחילים אחרי הסוף שלו. זו הסיבה שאפשר להדפיס
    את הפלט תוך כדי, בלי לשמור אותו.

    **קטעים שנוגעים, `<=` מול `<` :** עם `<=` שני קטעים סגורים שנוגעים, <span dir="ltr">[1, 4]</span>
    ו-<span dir="ltr">[4, 5]</span>, מתמזגים ל-<span dir="ltr">[1, 5]</span>. עם `<` הם נשארים
    שניים. שתי האפשרויות עקביות, וההסכמה בשאלה קובעת : כאן קטעים סגורים, ולכן `<=`. בחצאי
    קטעים \( [s, e) \) של סעיף ב הנקודה 4 שייכת רק לשני, ולכן שם הם רק נוגעים.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n \log n) \) למיון, ואחריו מעבר אחד, \( O(1) \) לקטע. כשההתחלות הן מספרים
      שלמים קטנים אפשר למיין במניין (counting sort) ולהגיע ל-\( O(n + T) \).
    - **זיכרון :** ‏\( O(n) \) לפלט (במקרה הגרוע אף זוג לא חופף). המיון במקום, ואז עוד \( O(1) \).

    **נסו בעצמכם.** כל צעד הוא קטע אחד לפי הסדר הממוין. השורה שמתחת לציר היא הפלט, והקטע
    שהצעד נגע בו מודגש :

    <div class="explorer" data-kind="intervals" data-mode="a" data-ivs="1-3 2-6 8-10 15-18"></div>

---

### סעיף ב – קטעים עם גובה, הגובה הכולל בכל נקודה

??? tip "רמז 1"
    כמו בשאלה 0062, הפכו כל קטע לשני **אירועים** : בהתחלה הגובה הכולל עולה ב-\( h \), ובסוף
    הוא יורד ב-\( h \). בין שני אירועים סמוכים הגובה הכולל לא משתנה. מה זה אומר על החתיכות?

??? tip "רמז 2"
    מיינו את האירועים לפי המיקום, ועברו עליהם עם סכום רץ. בכל מיקום חדש, לפני שמעדכנים את
    הסכום, החתיכה מהמיקום הקודם ועד כאן בגובה הסכום הנוכחי. מה עושים כשכמה אירועים נופלים
    על אותו מיקום? ומה עושים עם שתי חתיכות שכנות באותו גובה?

<div class="selfcheck" data-answer="3" data-show="3 : [0, 2) בגובה 2, [2, 6) בגובה 5 ו-[6, 8) בגובה 2. במיקום 4 הקטע הראשון נגמר והשלישי מתחיל, שניהם בגובה 2, ולכן הסכום לא משתנה" data-hint="האירועים : +2 ב-0, +3 ב-2, −2 ו-+2 ב-4, −3 ב-6, −2 ב-8. אחרי כל מיקום, מה הסכום? חתיכות שכנות באותו גובה הן חתיכה אחת." markdown>
כמה חתיכות יש לקטעים <span dir="ltr">(0, 4, 2), (2, 6, 3), (4, 8, 2)</span>?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        כל קטע נותן שני אירועים, \( +h \) במיקום \( s \) ו-\( -h \) במיקום \( e \). ממיינים את
        האירועים לפי מיקום ועוברים עליהם עם סכום רץ. בכל מיקום חדש, לפני האירועים שבו, פולטים
        את החתיכה מהמיקום הקודם ועד כאן בגובה הסכום הנוכחי (אם הוא אינו 0), ואם הגובה שלה
        שווה לגובה של החתיכה הקודמת היא מאריכה אותה. בדוגמה : <span dir="ltr">(1, 2, 7), (2, 6, 11), (6, 7, 7)</span>.

    <!-- cost: זמן \( O(n \log n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **מונחים.** **חצי קטע** \( [s, e) \) מכיל את \( s \) ואת כל הנקודות עד \( e \), אבל לא את
    \( e \) עצמו. כך \( [1, 4) \) ו-\( [4, 5) \) לא חולקים אף נקודה, וכל נקודה על הציר שייכת
    לכל היותר לאחד מהם : זו הסיבה שעובדים בחצאי קטעים כשמחברים גבהים. ה**גובה הכולל** בנקודה
    \( x \) הוא \( \sum h_i \) על כל הקטעים עם \( s_i \le x < e_i \). **חתיכה** היא חצי קטע מקסימלי
    שבו הגובה הכולל קבוע : מקסימלי, כלומר אי אפשר להאריך אותו לאף צד בלי שהגובה ישתנה.
    ההסכמה בפתרון : חתיכות בגובה 0 (רווחים) לא מדווחות, ושתי חתיכות שכנות באותו גובה הן
    חתיכה אחת. כך הפלט **קנוני** : לכל קלט יש בדיוק פלט אחד, ואפשר להשוות אליו במבחן.

    **אירועים.** הגובה הכולל משתנה רק בהתחלה של קטע (עולה ב-\( h \)) ובסוף שלו (יורד
    ב-\( h \)). לכן בין שני מיקומים סמוכים של אירועים הוא קבוע, וכל חתיכה היא איחוד של קטעים
    כאלה. סורקים את \( 2n \) האירועים לפי מיקום עם **סכום רץ** : בכל מיקום חדש, הסכום הנוכחי
    הוא הגובה בכל הדרך מהמיקום הקודם ועד כאן, ואז מחילים את כל האירועים של המיקום.

    באיור, שני הקטעים של הדוגמה עם הגובה שלהם, ומתחת לציר הגובה הכולל כבלוקים : בכל חתיכה
    הבלוק של כל קטע שמכסה אותה, והקו שמעל הוא הסכום :

    <!-- gen 3 -->

    <svg class="figure iv-fig" viewBox="0 0 640 218" role="img" aria-label="שני קטעים, [1, 7) בגובה 7 ו-[2, 6) בגובה 4, ומתחתם הגובה הכולל : 7 ב-[1, 2), 11 ב-[2, 6) ו-7 ב-[6, 7)"><line class="grid" x1="64" x2="64" y1="10" y2="68"/><text class="tick" x="64" y="82" text-anchor="middle">0</text><line class="grid" x1="140" x2="140" y1="10" y2="68"/><text class="tick" x="140" y="82" text-anchor="middle">1</text><line class="grid" x1="216" x2="216" y1="10" y2="68"/><text class="tick" x="216" y="82" text-anchor="middle">2</text><line class="grid" x1="292" x2="292" y1="10" y2="68"/><text class="tick" x="292" y="82" text-anchor="middle">3</text><line class="grid" x1="368" x2="368" y1="10" y2="68"/><text class="tick" x="368" y="82" text-anchor="middle">4</text><line class="grid" x1="444" x2="444" y1="10" y2="68"/><text class="tick" x="444" y="82" text-anchor="middle">5</text><line class="grid" x1="520" x2="520" y1="10" y2="68"/><text class="tick" x="520" y="82" text-anchor="middle">6</text><line class="grid" x1="596" x2="596" y1="10" y2="68"/><text class="tick" x="596" y="82" text-anchor="middle">7</text><text class="iv-name" x="56" y="27" text-anchor="end">1</text><rect class="iv-bar iv-c0" x="140" y="14" width="456" height="16" rx="3"><title>[1, 7) height 7</title></rect><text class="iv-h" x="602" y="27">h = 7</text><text class="iv-name" x="56" y="51" text-anchor="end">2</text><rect class="iv-bar iv-c1" x="216" y="38" width="304" height="16" rx="3"><title>[2, 6) height 4</title></rect><text class="iv-h" x="526" y="51">h = 4</text><line class="axis" x1="64" x2="596" y1="68" y2="68"/><text class="tick" x="56" y="212" text-anchor="end">0</text><text class="tick" x="56" y="192" text-anchor="end">2</text><text class="tick" x="56" y="172" text-anchor="end">4</text><text class="tick" x="56" y="152" text-anchor="end">6</text><text class="tick" x="56" y="132" text-anchor="end">8</text><text class="tick" x="56" y="112" text-anchor="end">10</text><rect class="iv-blk iv-c0" x="140" y="138" width="76" height="70"><title>[1, 2): interval 1 adds 7, total 7</title></rect><rect class="iv-blk iv-c0" x="216" y="138" width="304" height="70"><title>[2, 6): interval 1 adds 7, total 11</title></rect><rect class="iv-blk iv-c1" x="216" y="98" width="304" height="40"><title>[2, 6): interval 2 adds 4, total 11</title></rect><rect class="iv-blk iv-c0" x="520" y="138" width="76" height="70"><title>[6, 7): interval 1 adds 7, total 7</title></rect><path class="iv-line" d="M64,208 H140 V138 H216 H216 V98 H520 H520 V138 H596 V208"/><text class="iv-name" x="56" y="90" text-anchor="end">total</text></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="iv-key-blk"></i>הגובה של קטע אחד, בצבע שלו</span><span><i class="iv-key-line"></i>הגובה הכולל, סכום הבלוקים</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שני אירועים לקטע :** ‏\( (s, +h) \) ו-\( (e, -h) \).
    2. **מיון :** לפי המיקום. באותו מיקום הסדר לא משנה לפלט, כי שלב 3 פולט רק במיקום
       **חדש**, לפני שמחילים את כל האירועים של המיקום.
    3. **פולטים :** במיקום חדש \( p \), אם הסכום הנוכחי אינו 0, החתיכה \( [\text{prev}, p) \)
       בגובה הסכום. אם החתיכה הקודמת נגמרת ב-\( \text{prev} \) ובאותו גובה, מאריכים אותה
       ל-\( p \) במקום לפתוח חדשה.
    4. **מעדכנים :** הסכום עולה או יורד ב-\( h \) של האירוע, ו-\( \text{prev} \) הופך ל-\( p \).

    </div>

    על הדוגמה, מיקום אחרי מיקום :

    <!-- gen 5 -->

    | המיקום | האירועים | הסכום לפני | הסכום אחרי | החתיכה שנפלטת |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏1 | ‏<span dir="ltr">+7</span> (קטע 1) | ‏0 | ‏7 | אין |
    | ‏2 | ‏<span dir="ltr">+4</span> (קטע 2) | ‏7 | ‏11 | ‏<span dir="ltr">[1, 2)</span> בגובה **7** |
    | ‏6 | ‏<span dir="ltr">−4</span> (קטע 2) | ‏11 | ‏7 | ‏<span dir="ltr">[2, 6)</span> בגובה **11** |
    | ‏7 | ‏<span dir="ltr">−7</span> (קטע 1) | ‏7 | ‏0 | ‏<span dir="ltr">[6, 7)</span> בגובה **7** |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="skyline" linenums="1" hl_lines="5 9 11 14"
        def skyline(triples: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
            """The pieces (start, end, total) of constant total height, half-open; a gap of total 0
            is skipped and adjacent pieces of one total are joined. An event is +h at a start and
            -h at an end; before the events of a position, the piece up to it is emitted."""
            events = sorted((p, d) for s, e, h in triples for p, d in ((s, h), (e, -h)))   # (1)!
            out: list[list[int]] = []
            total, prev = 0, None
            for p, d in events:
                if prev is not None and p > prev and total != 0:          # (2)!
                    if out and out[-1][1] == prev and out[-1][2] == total:
                        out[-1][1] = p                                     # (3)!
                    else:
                        out.append([prev, p, total])
                total += d                                                 # (4)!
                prev = p
            return [(s, e, t) for s, e, t in out]
        ```

        1. זוגות \( (p, d) \) ממוינים לפי המיקום, ובמיקום שווה לפי \( d \) : הירידות לפני העליות.
        2. מיקום חדש וסכום שאינו 0 : יש חתיכה לפלוט. באירוע השני באותו מיקום `p == prev`, ואין פליטה כפולה.
        3. החתיכה הקודמת נגמרת כאן ובאותו גובה : מאריכים אותה במקום לפתוח חדשה.
        4. רק אחרי הפליטה הסכום משתנה.

    === "SystemVerilog"
        ```systemverilog title="function skyline" linenums="1" hl_lines="16 18 19 22"
        // the pieces [s, e) of constant total height: an event is +h at a start and -h at an end,
        // sorted by position; before the events of a position the piece up to it is emitted (a
        // total of 0 is a gap, and a piece of the same total as the last one extends it)
        typedef struct { int s; int e; int h; } piece_t;   // [s, e) with a height, or a total
        typedef struct { int p; int d; } ev_t;             // an event: the position and +h or -h

        function automatic void skyline(input piece_t iv[], output piece_t out[$]);
          ev_t ev[$];
          int total = 0, prev = 0;
          bit started = 0;
          out = {};
          foreach (iv[i]) begin
            ev.push_back('{iv[i].s, iv[i].h});
            ev.push_back('{iv[i].e, -iv[i].h});
          end
          ev.sort with (item.p);                                                    // (1)!
          foreach (ev[i]) begin
            if (started && ev[i].p > prev && total != 0) begin                       // (2)!
              if (out.size() > 0 && out[$].e == prev && out[$].h == total) out[$].e = ev[i].p;   // (3)!
              else out.push_back('{prev, ev[i].p, total});
            end
            total += ev[i].d;                                                        // (4)!
            prev = ev[i].p;
            started = 1;
          end
        endfunction
        ```

        1. מיון לפי המיקום בלבד. הסדר בין אירועים באותו מיקום לא משנה, כי הפליטה באה לפני כולם.
        2. מיקום חדש וסכום שאינו 0 : יש חתיכה לפלוט. באירוע השני באותו מיקום `ev[i].p == prev`, ואין פליטה כפולה.
        3. החתיכה הקודמת נגמרת כאן ובאותו גובה : מאריכים אותה. כך שני קטעים שנוגעים באותו גובה נותנים חתיכה אחת.
        4. רק אחרי הפליטה הסכום משתנה.

    #### למה זה נכון { .sol-proof }

    **קבוע בין אירועים :** יהיו \( p_1 < p_2 < \dots < p_m \) המיקומים השונים של האירועים. לכל
    \( x \) ב-\( [p_k, p_{k + 1}) \) אותם קטעים בדיוק מכסים את \( x \) : קטע \( [s_i, e_i) \)
    מכסה את \( x \) אם \( s_i \le x < e_i \), ו-\( s_i \) ו-\( e_i \) הם מיקומים של אירועים, ולכן
    התנאי לא משתנה בתוך \( [p_k, p_{k + 1}) \). מכאן שהגובה הכולל קבוע שם, ושווה לסכום
    הגבהים של הקטעים שהתחילו עד \( p_k \) ועוד לא נגמרו, שהוא בדיוק הסכום הרץ אחרי כל
    האירועים של \( p_k \).

    **החתיכות :** כל חתיכה היא איחוד של קטעים \( [p_k, p_{k + 1}) \) סמוכים באותו גובה, ואינה
    מכילה קטע כזה בגובה אחר. הסריקה פולטת כל \( [p_k, p_{k + 1}) \) שהגובה בו אינו 0, ומדביקה
    אותו לקודם כשהגבהים שווים והקודם נגמר ב-\( p_k \). לכן הפלט הוא בדיוק החתיכות
    המקסימליות בגובה שונה מ-0, כל אחת פעם אחת. לפני \( p_1 \) ואחרי \( p_m \) הגובה הוא 0.

    **אותו מיקום :** כל האירועים של \( p_k \) מוחלים לפני הפליטה הבאה, ולכן הסכום שנפלט
    עבור \( [p_k, p_{k + 1}) \) כולל את כולם, בכל סדר. הבדיקה `p > prev` היא מה שמונע פליטה
    של \( [p_k, p_k) \), חתיכה באורך אפס. בלעדיה, קטע שנגמר ואחר שמתחיל באותו מיקום נותנים
    חתיכה ריקה בגובה הסכום של שניהם אם \( +h \) מעובד ראשון, וגם הסדר "\( -h \) לפני \( +h \)"
    לא מציל : שני קטעים שמתחילים באותו מיקום נותנים חתיכה ריקה בגובה הראשון מהם. לכן
    הבדיקה היא על המיקום, לא על הסדר.

    **סעיף א הוא מקרה פרטי :** ניקח כל קטע סגור \( [s, e] \) של סעיף א כחצי קטע \( [s, e) \)
    בגובה 1. הגובה הכולל בנקודה הוא מספר הקטעים שמכסים אותה, והוא חיובי בדיוק בנקודות
    המכוסות. איחוד של חתיכות שכנות (שנוגעות זו בזו) בגובה חיובי כלשהו הוא קטע ממוזג של
    סעיף א : בדוגמה, <span dir="ltr">[1, 3), [2, 6), [8, 10), [15, 18)</span> בגובה 1 נותנים את
    החתיכות <span dir="ltr">[1, 2) 1, [2, 3) 2, [3, 6) 1, [8, 10) 1, [15, 18) 1</span>, ואיחוד
    השכנות הוא <span dir="ltr">[1, 6), [8, 10), [15, 18)</span>, הקצוות של סעיף א. גם קטעים
    שנוגעים מסתדרים : <span dir="ltr">[1, 4)</span> ו-<span dir="ltr">[4, 5)</span> הם שתי
    חתיכות שכנות בגובה 1, וההדבקה שלהן היא בדיוק המיזוג של `<=`. זה בדיוק מה ש-`above` של
    סעיף ג עושה עם \( T = 1 \), והמבחן בודק את זה על קלטים אקראיים.

    **מקרי קצה :** שני קטעים עם אותה התחלה נותנים שני אירועי \( +h \) באותו מיקום, והסכום
    קופץ בבת אחת. קטע מקונן, <span dir="ltr">(2, 6, 4)</span> בתוך <span dir="ltr">(1, 7, 7)</span>
    בדוגמה, נותן שלוש חתיכות : לפניו, בתוכו ואחריו. קטעים שנוגעים באותו גובה כולל, כמו
    <span dir="ltr">(0, 2, 3)</span> ו-<span dir="ltr">(2, 4, 3)</span>, הם חתיכה אחת
    <span dir="ltr">(0, 4, 3)</span>. בין שני קטעים זרים יש רווח בגובה 0, שלא מדווח. הגבהים
    חיוביים, ולכן הסכום הוא 0 בדיוק ברווחים. אם מרשים גבהים שליליים, הקוד עדיין רץ, אבל
    חתיכה שהגבהים בה מתקזזים ל-0 מדולגת כאילו הייתה רווח : צריך להחליט אם זה מה שרוצים.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n \log n) \) למיון של \( 2n \) אירועים, והסריקה ליניארית.
    - **זיכרון :** ‏\( O(n) \) לאירועים ולפלט, שיש בו לכל היותר \( 2n - 1 \) חתיכות.
    - **מערך הפרשים :** כשהמיקומים הם מספרים שלמים קטנים מ-\( L \), אפשר במקום המיון מערך
      \( \text{diff} \) באורך \( L + 1 \) : ‏\( \text{diff}[s] \mathrel{+}= h \),
      ‏\( \text{diff}[e] \mathrel{-}= h \), והסכום המצטבר שלו הוא הגובה בכל נקודה, ב-\( O(n + L) \).
      אותה סריקה, עם מערך במקום רשימת אירועים ממוינת.

    **נסו בעצמכם.** כל צעד הוא מיקום אחד של אירועים. הבלוקים נבנים משמאל לימין עם הסכום
    הרץ, והשורה שמתחת אומרת מה נפלט ולמה :

    <div class="explorer" data-kind="intervals" data-mode="b" data-ivs="1-7-7 2-6-4"></div>

---

### סעיף ג – השיא, ואיפה הגובה לפחות T

??? tip "רמז 1"
    החתיכות של סעיף ב כבר מכסות את כל הציר בגובה קבוע לכל חתיכה. מעבר אחד עליהן מספיק.

??? tip "רמז 2"
    שתי חתיכות שכנות ששתיהן מעל הסף הן טווח אחד. מה התנאי להדבקה, ומתי השיא "מתפרש" על כמה
    חתיכות?

<div class="selfcheck" data-answer="6" data-show="6 : ב-[2, 3) שלושת הקטעים הראשונים מכסים יחד, 2 + 3 + 1" data-hint="כתבו את האירועים לפי המיקום וחשבו את הסכום אחרי כל אחד. איפה שלושה קטעים חופפים?" markdown>
לקטעים <span dir="ltr">(0, 4, 2), (1, 3, 3), (2, 6, 1), (5, 8, 4)</span>, מה הגובה הכולל הגדול
ביותר?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        מעבר אחד על החתיכות של סעיף ב. הטווחים בגובה לפחות \( T \) : חתיכה שהגובה שלה
        \( \ge T \) מצטרפת לטווח הקודם אם הוא נגמר בדיוק בהתחלה שלה, ואחרת פותחת טווח חדש.
        השיא הוא הגובה הגדול ביותר, והטווחים שלו הם אותה פונקציה עם \( T \) שווה לשיא.
        בדוגמה : שיא 6 ב-<span dir="ltr">[2, 3)</span>, ובסף \( T = 4 \) הטווחים
        <span dir="ltr">[1, 3)</span> ו-<span dir="ltr">[5, 8)</span>.

    <!-- cost: זמן \( O(n) \) אחרי סעיף ב | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    החתיכות של סעיף ב הן תיאור מלא של הגובה הכולל : בכל חתיכה הוא קבוע, ובין החתיכות הוא 0.
    לכן כל שאלה על הגובה היא מעבר אחד על הרשימה. **השיא** הוא הגובה הגדול ביותר ברשימה,
    ו**איפה** הוא מתקבל הן החתיכות בגובה הזה. **הטווחים מעל סף** \( T \ge 1 \) הם איחוד
    החתיכות בגובה \( \ge T \) : שתי חתיכות כאלה שנוגעות זו בזו (הקודמת נגמרת בדיוק בהתחלה
    של הבאה) הן טווח אחד, גם אם הגובה שלהן שונה. רווח בגובה 0 לעולם אינו מגיע לסף, ולכן
    חתיכות משני צדי רווח נשארות שני טווחים.

    זה בדיוק הפתרון של שאלה [0062](0062-how-many-tags.md) : שם הגובה של כל טרנזקציה הוא 1,
    הגובה הכולל הוא מספר הטרנזקציות הפתוחות, והשיא הוא מספר ה-tags. ובשאלה
    [0033](0033-fifo-depth-from-rates.md) התפוסה של ה-FIFO היא סכום רץ של כתיבות פחות
    קריאות, והעומק הנדרש הוא השיא שלה : אותה סריקה, אירוע אחרי אירוע.

    באיור, ארבעה קטעים עם גבהים, הגובה הכולל שלהם, הסף \( T = 4 \) והשיא :

    <!-- gen 6 -->

    <svg class="figure iv-fig" viewBox="0 0 640 276" role="img" aria-label="ארבעה קטעים עם גבהים, הגובה הכולל שלהם, הסף T = 4 והשיא 6 ב-[2, 3)"><line class="grid" x1="64" x2="64" y1="10" y2="116"/><text class="tick" x="64" y="130" text-anchor="middle">0</text><line class="grid" x1="130.5" x2="130.5" y1="10" y2="116"/><text class="tick" x="130.5" y="130" text-anchor="middle">1</text><line class="grid" x1="197" x2="197" y1="10" y2="116"/><text class="tick" x="197" y="130" text-anchor="middle">2</text><line class="grid" x1="263.5" x2="263.5" y1="10" y2="116"/><text class="tick" x="263.5" y="130" text-anchor="middle">3</text><line class="grid" x1="330" x2="330" y1="10" y2="116"/><text class="tick" x="330" y="130" text-anchor="middle">4</text><line class="grid" x1="396.5" x2="396.5" y1="10" y2="116"/><text class="tick" x="396.5" y="130" text-anchor="middle">5</text><line class="grid" x1="463" x2="463" y1="10" y2="116"/><text class="tick" x="463" y="130" text-anchor="middle">6</text><line class="grid" x1="529.5" x2="529.5" y1="10" y2="116"/><text class="tick" x="529.5" y="130" text-anchor="middle">7</text><line class="grid" x1="596" x2="596" y1="10" y2="116"/><text class="tick" x="596" y="130" text-anchor="middle">8</text><text class="iv-name" x="56" y="27" text-anchor="end">1</text><rect class="iv-bar iv-c0" x="64" y="14" width="266" height="16" rx="3"><title>[0, 4) height 2</title></rect><text class="iv-h" x="336" y="27">h = 2</text><text class="iv-name" x="56" y="51" text-anchor="end">2</text><rect class="iv-bar iv-c1" x="130.5" y="38" width="133" height="16" rx="3"><title>[1, 3) height 3</title></rect><text class="iv-h" x="269.5" y="51">h = 3</text><text class="iv-name" x="56" y="75" text-anchor="end">3</text><rect class="iv-bar iv-c2" x="197" y="62" width="266" height="16" rx="3"><title>[2, 6) height 1</title></rect><text class="iv-h" x="469" y="75">h = 1</text><text class="iv-name" x="56" y="99" text-anchor="end">4</text><rect class="iv-bar iv-c3" x="396.5" y="86" width="199.5" height="16" rx="3"><title>[5, 8) height 4</title></rect><text class="iv-h" x="602" y="99">h = 4</text><line class="axis" x1="64" x2="596" y1="116" y2="116"/><text class="tick" x="56" y="270" text-anchor="end">0</text><text class="tick" x="56" y="250" text-anchor="end">1</text><text class="tick" x="56" y="230" text-anchor="end">2</text><text class="tick" x="56" y="210" text-anchor="end">3</text><text class="tick" x="56" y="190" text-anchor="end">4</text><text class="tick" x="56" y="170" text-anchor="end">5</text><text class="tick" x="56" y="150" text-anchor="end">6</text><rect class="iv-blk iv-c0" x="64" y="226" width="66.5" height="40"><title>[0, 1): interval 1 adds 2, total 2</title></rect><rect class="iv-blk iv-c0" x="130.5" y="226" width="66.5" height="40"><title>[1, 2): interval 1 adds 2, total 5</title></rect><rect class="iv-blk iv-c1" x="130.5" y="166" width="66.5" height="60"><title>[1, 2): interval 2 adds 3, total 5</title></rect><rect class="iv-blk iv-c0" x="197" y="226" width="66.5" height="40"><title>[2, 3): interval 1 adds 2, total 6</title></rect><rect class="iv-blk iv-c1" x="197" y="166" width="66.5" height="60"><title>[2, 3): interval 2 adds 3, total 6</title></rect><rect class="iv-blk iv-c2" x="197" y="146" width="66.5" height="20"><title>[2, 3): interval 3 adds 1, total 6</title></rect><rect class="iv-blk iv-c0" x="263.5" y="226" width="66.5" height="40"><title>[3, 4): interval 1 adds 2, total 3</title></rect><rect class="iv-blk iv-c2" x="263.5" y="206" width="66.5" height="20"><title>[3, 4): interval 3 adds 1, total 3</title></rect><rect class="iv-blk iv-c2" x="330" y="246" width="66.5" height="20"><title>[4, 5): interval 3 adds 1, total 1</title></rect><rect class="iv-blk iv-c2" x="396.5" y="246" width="66.5" height="20"><title>[5, 6): interval 3 adds 1, total 5</title></rect><rect class="iv-blk iv-c3" x="396.5" y="166" width="66.5" height="80"><title>[5, 6): interval 4 adds 4, total 5</title></rect><rect class="iv-blk iv-c3" x="463" y="186" width="133" height="80"><title>[6, 8): interval 4 adds 4, total 4</title></rect><path class="iv-line" d="M64,266 H64 V226 H130.5 H130.5 V166 H197 H197 V146 H263.5 H263.5 V206 H330 H330 V246 H396.5 H396.5 V166 H463 H463 V186 H596 V266"/><line class="iv-thr" x1="64" x2="596" y1="186" y2="186"/><text class="legend" x="600" y="190">T = 4</text><line class="iv-peak" x1="64" x2="596" y1="146" y2="146"/><text class="legend" x="600" y="150">max</text><text class="iv-name" x="56" y="138" text-anchor="end">total</text></svg>

    <!-- /gen -->

    <!-- gen 7 -->

    <span class="viz-legend"><span><i class="iv-key-line"></i>הגובה הכולל</span><span><i class="iv-key-thr"></i>הסף T</span><span><i class="iv-key-peak"></i>השיא</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **החתיכות :** מריצים את סעיף ב ומקבלים את הרשימה, ממוינת לפי ההתחלה.
    2. **הסף :** לכל חתיכה בגובה \( \ge T \) : אם הטווח האחרון שנמצא נגמר בדיוק בהתחלה שלה,
       הסוף שלו הופך לסוף שלה. אחרת היא טווח חדש. חתיכה מתחת לסף מדולגת, ושוברת את הרצף.
    3. **השיא :** הגובה הגדול ביותר ברשימה, ואז אותו מעבר עם \( T \) שווה לשיא נותן את
       הטווחים שבהם הוא מתקבל.

    </div>

    על הדוגמה עם \( T = 4 \) :

    <!-- gen 8 -->

    | החתיכה | הגובה | לפחות 4? | הטווחים עד עכשיו | השיא עד עכשיו |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏<span dir="ltr">[0, 1)</span> | ‏2 | לא | אין | **‏2** ב-<span dir="ltr">[0, 1)</span> |
    | ‏<span dir="ltr">[1, 2)</span> | ‏5 | כן, טווח חדש | ‏<span dir="ltr">[1, 2)</span> | **‏5** ב-<span dir="ltr">[1, 2)</span> |
    | ‏<span dir="ltr">[2, 3)</span> | ‏6 | כן, מצטרפת לטווח הקודם | ‏<span dir="ltr">[1, 3)</span> | **‏6** ב-<span dir="ltr">[2, 3)</span> |
    | ‏<span dir="ltr">[3, 4)</span> | ‏3 | לא | ‏<span dir="ltr">[1, 3)</span> | **‏6** ב-<span dir="ltr">[2, 3)</span> |
    | ‏<span dir="ltr">[4, 5)</span> | ‏1 | לא | ‏<span dir="ltr">[1, 3)</span> | **‏6** ב-<span dir="ltr">[2, 3)</span> |
    | ‏<span dir="ltr">[5, 6)</span> | ‏5 | כן, טווח חדש | ‏<span dir="ltr">[1, 3) [5, 6)</span> | **‏6** ב-<span dir="ltr">[2, 3)</span> |
    | ‏<span dir="ltr">[6, 8)</span> | ‏4 | כן, מצטרפת לטווח הקודם | ‏<span dir="ltr">[1, 3) [5, 8)</span> | **‏6** ב-<span dir="ltr">[2, 3)</span> |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="above" linenums="1" hl_lines="5 7 17"
        def above(pieces: list[tuple[int, int, int]], t: int) -> list[tuple[int, int]]:
            """The ranges [start, end) where the total is at least t (t >= 1), adjacent ones joined."""
            out: list[list[int]] = []
            for s, e, total in pieces:
                if total >= t:                                  # (1)!
                    if out and out[-1][1] == s:
                        out[-1][1] = e                          # (2)!
                    else:
                        out.append([s, e])
            return [(s, e) for s, e in out]


        def peak(pieces: list[tuple[int, int, int]]) -> tuple[int, list[tuple[int, int]]]:
            """The largest total and the ranges where it holds; (0, []) without pieces."""
            if not pieces:
                return 0, []
            top = max(total for _, _, total in pieces)          # (3)!
            return top, above(pieces, top)
        ```

        1. החתיכה מגיעה לסף.
        2. הטווח האחרון נגמר בדיוק בהתחלה של החתיכה : מדביקים, גם כשהגבהים שונים.
        3. השיא הוא המקסימום של הגבהים, והטווחים שלו הם `above` עם הסף שווה לשיא.

    === "SystemVerilog"
        ```systemverilog title="function above" linenums="1" hl_lines="6 7 15"
        // the ranges where the total is at least t (adjacent pieces joined), and the peak: the
        // largest total with the ranges that hold it
        function automatic void above(input piece_t pieces[$], input int t, output span_t out[$]);
          out = {};
          foreach (pieces[j]) begin
            if (pieces[j].h >= t) begin                                            // (1)!
              if (out.size() > 0 && out[$].e == pieces[j].s) out[$].e = pieces[j].e;   // (2)!
              else out.push_back('{pieces[j].s, pieces[j].e});
            end
          end
        endfunction

        function automatic int peak(input piece_t pieces[$], output span_t where[$]);
          int top = 0;
          foreach (pieces[j]) if (pieces[j].h > top) top = pieces[j].h;          // (3)!
          above(pieces, top, where);
          return top;
        endfunction
        ```

        1. החתיכה מגיעה לסף. ‏`span_t` של סעיף א משמש כאן לטווח \( [s, e) \).
        2. הטווח האחרון נגמר בדיוק בהתחלה של החתיכה : מדביקים, גם כשהגבהים שונים.
        3. השיא הוא המקסימום של הגבהים, וברשימה ריקה 0 : ‏`above` עם \( T = 0 \) על רשימה ריקה מחזיר רשימה ריקה.

    #### למה זה נכון { .sol-proof }

    **הסף :** נקודה \( x \) היא בגובה \( \ge T \) בדיוק אם היא בחתיכה בגובה כזה (ברווח הגובה
    0, ו-\( T \ge 1 \)). לכן קבוצת הנקודות המבוקשת היא איחוד החתיכות האלה. שתי חתיכות
    ברשימה שנוגעות זו בזו הן רצופות ברשימה (כי הרשימה ממוינת וזרה), ולכן בדיקת ההדבקה מול
    הטווח האחרון בלבד מספיקה, בדיוק כמו בסעיף א : הטווחים שנבנים הם רכיבי הקשירות של
    האיחוד.

    **השיא :** הגובה הכולל מקבל ערכים רק בחתיכות (וב-0 ברווחים), ולכן המקסימום שלו הוא
    המקסימום של הרשימה, והמקומות שבהם הוא מתקבל הם החתיכות בגובה הזה, שהן בדיוק הטווחים של
    `above` עם \( T \) שווה לשיא. אם שתי חתיכות שכנות שתיהן בשיא, הן לא היו נפרדות בסעיף ב,
    ולכן כל טווח של השיא הוא חתיכה אחת.

    **הקשר ל-0062 :** עם גובה 1 לכל טרנזקציה, השיא של סעיף ג הוא מספר ה-tags, וההסכמה
    "תשובה לפני שליחה באותו רגע" של 0062 היא בדיוק חצאי הקטעים \( [s, e) \) : ברגע \( e \)
    הטרנזקציה כבר לא פתוחה.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n) \) על רשימת החתיכות (לכל היותר \( 2n - 1 \)), אחרי \( O(n \log n) \) של
      סעיף ב. השיא והטווחים שלו הם שני מעברים, ואפשר גם באחד.
    - **זיכרון :** ‏\( O(n) \) לטווחים.

    **נסו בעצמכם.** הגובה הכולל כקו, הסף \( T \) בסליידר, והשיא מקווקו. כל צעד הוא חתיכה אחת :
    מעל הסף או לא, מצטרפת לטווח או פותחת חדש :

    <div class="explorer" data-kind="intervals" data-mode="c" data-ivs="0-4-2 1-3-3 2-6-1 5-8-4" data-t="4"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לשכוח למיין"
    בלי מיון, <span dir="ltr">[8, 10], [1, 3], [2, 6]</span> נותנים <span dir="ltr">[8, 10]</span>
    בלבד : ‏<span dir="ltr">1 ≤ 10</span> ו-<span dir="ltr">2 ≤ 10</span>, ולכן שני הקטעים
    "נבלעים" בקטע שאינו חופף להם כלל, והסוף 10 לא גדל. המיון הוא מה שמבטיח שחפיפה אפשרית
    רק עם הקטע הממוזג האחרון, ושהתנאי \( s \le \text{end} \) באמת אומר חפיפה.

??? trap "מלכודת : להשוות לקטע הקודם בקלט ולא לקטע הממוזג האחרון"
    ב-<span dir="ltr">[1, 10], [2, 3], [4, 5]</span> הקטע <span dir="ltr">[4, 5]</span> לא חופף
    ל-<span dir="ltr">[2, 3]</span>, אבל הוא בתוך <span dir="ltr">[1, 10]</span>. ההשוואה היא תמיד
    מול הסוף של **הפלט** האחרון, שכבר מחזיק את המקסימום של כל הסופים עד כאן.

??? trap "מלכודת : קטעים סגורים מול חצאי קטעים, וקטעים שנוגעים"
    ‏<span dir="ltr">[1, 4]</span> ו-<span dir="ltr">[4, 5]</span> מתמזגים בקטעים סגורים (`<=`) ולא
    בחצאי קטעים (`<`). הסימן בקוד הוא ההסכמה של השאלה. בסעיף ב אותה שאלה חוזרת כסדר של
    האירועים באותו מיקום : מי שפולט אחרי כל אירוע חייב לשים \( -h \) לפני \( +h \), ועדיין נופל
    על שני קטעים שמתחילים יחד. הפתרון בעמוד פולט רק במיקום חדש, לפני כל האירועים שלו, ואז
    הסדר לא משנה.

??? trap "מלכודת : לפלוט חתיכה באורך אפס"
    בלי הבדיקה `p > prev`, שני אירועים באותו מיקום נותנים חתיכה \( [p, p) \), ריקה, בגובה
    שבין שני האירועים. ב-<span dir="ltr">(0, 4, 2)</span> ו-<span dir="ltr">(4, 8, 2)</span> הייתה
    מופיעה <span dir="ltr">(4, 4, 4)</span> כש-\( +h \) מעובד ראשון, וב-<span dir="ltr">(0, 4, 1)</span>
    ו-<span dir="ltr">(0, 4, 2)</span>, שמתחילים יחד, <span dir="ltr">(0, 0, 1)</span> בכל סדר. חתיכה
    היא תמיד באורך חיובי.

??? trap "מלכודת : להשאיר שתי חתיכות שכנות באותו גובה"
    כשקטע נגמר ואחר באותו גובה מתחיל באותו מיקום, הסכום לא משתנה, אבל סריקה תמימה פולטת
    שתי חתיכות : <span dir="ltr">(0, 2, 3)</span> ו-<span dir="ltr">(2, 4, 3)</span> במקום
    <span dir="ltr">(0, 4, 3)</span>. שתי הצורות מתארות את אותו גובה, אבל רק אחת מהן קנונית,
    והמבחן משווה רשימות. הפתרון מדביק, ואומר זאת בהגדרה של חתיכה (מקסימלית).

??? trap "מלכודת : לספור חפיפות של זוגות במקום את הגובה בנקודה"
    "כמה קטעים חופפים לקטע הזה ועוד אחד" אינו השיא : ב-<span dir="ltr">(0, 30, 1), (5, 10, 1), (15, 20, 1)</span>
    הקטע הראשון חופף לשניים, אבל הגובה הכולל אף פעם אינו 3. סופרים בנקודה, בסריקה.

??? followup "שאלות המשך"
    - **הכנסה של קטע אחד (LC 57) :** נתונה רשימה ממוזגת וממוינת וקטע חדש. איך מכניסים אותו
      ב-\( O(n) \) בלי למיין מחדש?

        ??? fu-answer "תשובה"
            מעבר אחד : מעתיקים את הקטעים שנגמרים לפני ההתחלה של החדש, ממזגים לתוך החדש כל קטע
            שחופף לו (ההתחלה הופכת למינימום והסוף למקסימום), ואז מעתיקים את השאר. הקטעים החופפים
            הם רצף אחד ברשימה, כי היא ממוינת וזרה.

    - **החיתוך של שתי רשימות (LC 986) :** שתי רשימות ממוזגות וממוינות. אילו קטעים נמצאים
      בשתיהן?

        ??? fu-answer "תשובה"
            שני מצביעים, \( i \) ו-\( j \). החיתוך של הזוג הנוכחי הוא
            \( [\max(s_i, s_j), \min(e_i, e_j)] \), ונפלט אם ההתחלה אינה גדולה מהסוף. מקדמים את
            המצביע של הקטע שנגמר קודם, כי הוא לא יכול לחתוך אף קטע נוסף. זמן \( O(n + m) \).

    - **האורך המכוסה הכולל :** כמה מהציר מכוסה לפחות על ידי קטע אחד?

        ??? fu-answer "תשובה"
            סכום האורכים של הקטעים הממוזגים של סעיף א (או של החתיכות של סעיף ב, בלי הגובה).
            הפלט הממוזג זר, ולכן אין ספירה כפולה. אותה סריקה עם צבירה במקום רשימה, ב-\( O(1) \)
            זיכרון נוסף.

    - **מספר הנקודות שדוקרות את כל הקטעים :** מה המספר הקטן ביותר של נקודות כך שכל קטע
      מכיל לפחות אחת מהן?

        ??? fu-answer "תשובה"
            חמדני לפי הסוף : ממיינים לפי \( e \), שמים נקודה בסוף של הקטע הראשון, ומדלגים על כל
            קטע שמכיל אותה (\( s \le \) הנקודה). הקטע הבא שלא מכיל אותה מקבל נקודה בסוף שלו. כל
            נקודה "מוצדקת" על ידי קטע שאף נקודה קודמת לא דוקרת, ולכן המספר מינימלי. זמן
            \( O(n \log n) \).
