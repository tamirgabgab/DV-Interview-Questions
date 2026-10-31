---
id: 65
title: כמה איים – ארבעה כיוונים, שמונה כיוונים, וגודל כל אי
level: junior
difficulty: medium
kind: code
tags: [algorithms, bfs, python, systemverilog]
source: "שאלה קלאסית (Number of Islands, LeetCode 200); סעיף ג מכליל את Max Area of Island"
added: 2026-10-29
---

## השאלה

נתון לוח של \( m \) שורות ו-\( n \) עמודות, ובכל תא `'1'` (יבשה) או `'0'` (מים). שני תאי יבשה
הם **שכנים** אם אחד מהם נמצא בדיוק מעל, מתחת, משמאל או מימין לשני. **אי** הוא קבוצה של
תאי יבשה שאפשר להגיע מכל אחד מהם לכל אחד אחר דרך שכנים, ושאי אפשר להגדיל אותה : אף תא
יבשה מחוץ לקבוצה אינו שכן של תא בתוכה. מסביב ללוח יש רק מים. כמה איים יש בלוח?

דוגמה, לוח של 5 שורות ו-6 עמודות :

```text
1 1 0 0 0 0
1 1 0 0 1 1
0 0 0 0 1 0
0 0 0 1 0 0
0 0 0 1 0 0
```

התשובה היא 3 : הריבוע בפינה השמאלית העליונה, שלושת התאים בצד ימין, ושני התאים שבתחתית.

**ההקשר באימות :** בדיקת זיכרון (MBIST) מחזירה **מפת כשלים** : לוח של תאי הזיכרון, שורה
לכל כתובת ועמודה לכל ביט, ובו 1 בכל תא שנכשל. פגם פיזי אחד (קצר בין שתי ליניות, חלקיק
על הסיליקון) מופיע במפה כגוש של תאים צמודים, ולכן ספירת הגושים היא ספירת הפגמים, והגודל
של כל גוש אומר אם שורת חילוף אחת או עמודת חילוף אחת מספיקות לתקן אותו. מי שמנתח מפות כאלה,
ומי שכותב מודל ייחוס ל-DUT שמנתח אותן, כותב בדיוק את הפונקציה של השאלה הזו : סעיף א סופר
את הגושים, סעיף ב מתייחס גם לתאים שנוגעים בפינה (פגם לא מכבד את רשת הקואורדינטות), וסעיף ג
מחזיר את הגודל של כל גוש.

- **סעיף א – ארבעה כיוונים :** כתבו פונקציה שמחזירה את מספר האיים.
- **סעיף ב – שמונה כיוונים :** עכשיו גם תאים שנוגעים זה בזה בפינה (באלכסון) הם שכנים. מה
  משתנה באלגוריתם? כמה איים יש בלוח של הדוגמה?
- **סעיף ג – הגודל של כל אי :** החזירו רשימה של הגדלים של האיים, מהגדול לקטן. האורך של
  הרשימה הוא מספר האיים, וכל איבר הוא מספר התאים של אי אחד. בדוגמה : <span dir="ltr">[4, 3, 2]</span>.

??? interviewer "מה המראיין בודק"
    - **לראות גרף :** האם המועמד מזהה שהלוח הוא גרף (תא הוא צומת, שכנות היא קשת) ושאי הוא
      **רכיב קשירות**, ומשם מגיע לחיפוש לרוחב או לעומק, ולא לספירה ידנית של תבניות.
    - **סימון נכון :** מתי מסמנים תא כ"נראה", ולמה סימון מאוחר מדי מכניס תאים לתור פעמיים.
    - **ההכללה בטבלה :** האם השינוי משמונה כיוונים לארבעה הוא שורה אחת (טבלת הכיוונים), או
      שהקוד נכתב עם ארבעה תנאים ידניים שצריך לשכפל.
    - **עלות ומקרי קצה :** למה הזמן ליניארי בגודל הלוח, מה קורה בלוח ריק, בלוח שכולו יבשה,
      ובלוח גדול עם רקורסיה.

---

### סעיף א – ארבעה כיוונים

כתבו פונקציה שמקבלת את הלוח ומחזירה את מספר האיים.

??? tip "רמז 1"
    חשבו על הלוח כעל גרף : כל תא יבשה הוא צומת, ובין שני שכנים יש קשת. מה זה אי בשפה של
    גרפים, ואיזה אלגוריתם מוצא את כל הצמתים שמחוברים לצומת נתון?

??? tip "רמז 2"
    עוברים על הלוח שורה אחרי שורה. כשפוגשים תא יבשה שעוד לא סומן, זה אי חדש : סופרים אותו,
    ומסמנים את **כל** התאים של האי שלו, כדי שהסריקה לא תספור אותו שוב. איך מגיעים מתא אחד לכל
    האי שלו, בלי רקורסיה?

<div class="selfcheck" data-answer="5" data-show="5 : אף שני תאי יבשה אינם שכנים, ולכן כל אחד מהם הוא אי" data-hint="שכנים הם רק למעלה, למטה, משמאל ומימין. האם התא האמצעי שכן של אחת הפינות?" markdown>
בלוח <span dir="ltr">101 / 010 / 101</span> (שלוש שורות, יבשה בארבע הפינות ובאמצע), כמה איים יש
עם ארבעה כיוונים?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **מילוי בהצפה** (flood fill). סורקים את הלוח שורה אחרי שורה, ומחזיקים לוח `seen` של
        התאים שכבר סומנו. כל תא יבשה שלא סומן הוא אי חדש : מגדילים את המונה ומציפים ממנו את
        כל האי בעזרת תור (BFS) : מוציאים תא, ומכניסים כל שכן שהוא יבשה ועוד לא סומן, ומסמנים
        אותו **ברגע הכניסה**. כל תא יבשה נכנס לתור פעם אחת בדיוק, ולכן הזמן \( O(mn) \).
        בדוגמה : 3.

    <!-- cost: זמן \( O(mn) \) | זיכרון \( O(mn) \) -->

    #### הרעיון { .sol-idea }

    **מונחים.** ‏**שכן** של תא הוא אחד מארבעת התאים שנוגעים בו בצלע : למעלה, למטה, משמאל
    ומימין. בשפה של גרפים הלוח הוא גרף שהצמתים שלו הם תאי היבשה, ובין שני שכנים יש קשת. **אי**
    הוא בדיוק **רכיב קשירות** של הגרף הזה : קבוצה של צמתים שבין כל שניים מהם יש מסלול, ושלא
    מחוברת לשום צומת מחוצה לה. לכן "כמה איים" היא "כמה רכיבי קשירות", שאלה שיש לה אלגוריתם
    סטנדרטי : חיפוש מכל צומת שעוד לא ביקרו בו.

    **ההצפה.** מתא יבשה אחד מגיעים לכל האי שלו כמו מים שנשפכים : מהתא לשכניו, משכניו לשכניהם,
    עד שאין לאן. מממשים את זה עם **תור** (BFS, חיפוש לרוחב) : מכניסים את התא הראשון, ואז בכל
    צעד מוציאים תא מראש התור ומכניסים לזנב כל שכן שלו שהוא יבשה ועוד לא נראה. אפשר גם עם
    מחסנית במקום תור (DFS, חיפוש לעומק), ואז הסדר אחר אבל התוצאה זהה.

    **הסימון.** לוח `seen` באותו גודל אומר לכל תא אם כבר הגיעו אליו. תא מסומן ברגע שהוא
    **נכנס** לתור, לא כשהוא יוצא ממנו. ככה אותו תא לא יכול להיכנס פעמיים משני שכנים שונים.
    אפשר במקום זה "להטביע" את התא (לכתוב בו `'0'`), אבל אז הלוח של הקורא נהרס, ולכן כאן
    הלוח נשאר כפי שהתקבל.

    **הספירה.** הסריקה החיצונית עוברת על כל התאים לפי הסדר. תא יבשה שהסריקה פוגשת כשהוא עוד לא
    מסומן לא שייך לאף אי שכבר הוצף (אחרת היה מסומן), ולכן הוא אי חדש : המונה גדל ב-1, וההצפה
    ממנו מסמנת את כל האי, כך שהסריקה תדלג על שאר התאים שלו. בלוח של הדוגמה שלושה איים :

    <!-- gen 0 -->

    <svg class="figure il-fig" viewBox="0 0 248 208" style="max-width:15.5rem" role="img" aria-label="הלוח 5 על 6 של הדוגמה : שלושה איים עם ארבעה כיוונים, כל אי בצבע שלו והמספר שלו בתא"><text class="tick" x="44" y="14" text-anchor="middle">0</text><text class="tick" x="80" y="14" text-anchor="middle">1</text><text class="tick" x="116" y="14" text-anchor="middle">2</text><text class="tick" x="152" y="14" text-anchor="middle">3</text><text class="tick" x="188" y="14" text-anchor="middle">4</text><text class="tick" x="224" y="14" text-anchor="middle">5</text><text class="tick" x="18" y="44" text-anchor="end">0</text><text class="tick" x="18" y="80" text-anchor="end">1</text><text class="tick" x="18" y="116" text-anchor="end">2</text><text class="tick" x="18" y="152" text-anchor="end">3</text><text class="tick" x="18" y="188" text-anchor="end">4</text><g class="il-cell is-land il-i1"><title>cell (0, 0): land, island 1 of 4 cells</title><rect x="28" y="24" width="32" height="32" rx="4"/><text x="44" y="45" text-anchor="middle">1</text></g><g class="il-cell is-land il-i1"><title>cell (0, 1): land, island 1 of 4 cells</title><rect x="64" y="24" width="32" height="32" rx="4"/><text x="80" y="45" text-anchor="middle">1</text></g><g class="il-cell is-water"><title>cell (0, 2): water</title><rect x="100" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 3): water</title><rect x="136" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 4): water</title><rect x="172" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 5): water</title><rect x="208" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i1"><title>cell (1, 0): land, island 1 of 4 cells</title><rect x="28" y="60" width="32" height="32" rx="4"/><text x="44" y="81" text-anchor="middle">1</text></g><g class="il-cell is-land il-i1"><title>cell (1, 1): land, island 1 of 4 cells</title><rect x="64" y="60" width="32" height="32" rx="4"/><text x="80" y="81" text-anchor="middle">1</text></g><g class="il-cell is-water"><title>cell (1, 2): water</title><rect x="100" y="60" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (1, 3): water</title><rect x="136" y="60" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i2"><title>cell (1, 4): land, island 2 of 3 cells</title><rect x="172" y="60" width="32" height="32" rx="4"/><text x="188" y="81" text-anchor="middle">2</text></g><g class="il-cell is-land il-i2"><title>cell (1, 5): land, island 2 of 3 cells</title><rect x="208" y="60" width="32" height="32" rx="4"/><text x="224" y="81" text-anchor="middle">2</text></g><g class="il-cell is-water"><title>cell (2, 0): water</title><rect x="28" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 1): water</title><rect x="64" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 2): water</title><rect x="100" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 3): water</title><rect x="136" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i2"><title>cell (2, 4): land, island 2 of 3 cells</title><rect x="172" y="96" width="32" height="32" rx="4"/><text x="188" y="117" text-anchor="middle">2</text></g><g class="il-cell is-water"><title>cell (2, 5): water</title><rect x="208" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 0): water</title><rect x="28" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 1): water</title><rect x="64" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 2): water</title><rect x="100" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i3"><title>cell (3, 3): land, island 3 of 2 cells</title><rect x="136" y="132" width="32" height="32" rx="4"/><text x="152" y="153" text-anchor="middle">3</text></g><g class="il-cell is-water"><title>cell (3, 4): water</title><rect x="172" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 5): water</title><rect x="208" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 0): water</title><rect x="28" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 1): water</title><rect x="64" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 2): water</title><rect x="100" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i3"><title>cell (4, 3): land, island 3 of 2 cells</title><rect x="136" y="168" width="32" height="32" rx="4"/><text x="152" y="189" text-anchor="middle">3</text></g><g class="il-cell is-water"><title>cell (4, 4): water</title><rect x="172" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 5): water</title><rect x="208" y="168" width="32" height="32" rx="4"/></g></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="il-key il-i1"></i>אי 1</span><span><i class="il-key il-i2"></i>אי 2</span><span><i class="il-key il-i3"></i>אי 3</span><span><i class="il-key is-water"></i>מים</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הסריקה :** עוברים על התאים שורה אחרי שורה, ובכל שורה משמאל לימין. תא של מים או תא
       שכבר סומן : ממשיכים הלאה.
    2. **אי חדש :** תא יבשה שלא סומן. ‏\( \text{count} \leftarrow \text{count} + 1 \), מסמנים אותו ומכניסים
       אותו לתור.
    3. **ההצפה :** כל עוד התור לא ריק, מוציאים תא מראשו ובודקים את ארבעת השכנים שלו : שכן
       בתוך הלוח, שהוא יבשה ועוד לא סומן, מסומן ונכנס לזנב התור. שכן מחוץ ללוח, מים, או תא
       שכבר סומן : לא עושים כלום.
    4. **האי נגמר :** התור התרוקן. כל התאים של האי מסומנים, וחוזרים לסריקה מהמקום שבו עצרה.
    5. **הסוף :** הסריקה עברה את כל הלוח, ו-\( \text{count} \) הוא מספר האיים.

    </div>

    על הדוגמה, צעד אחרי צעד. תא נכתב כ-(שורה, עמודה), והשכנים נבדקים בסדר קבוע : למעלה, למטה,
    שמאלה, ימינה :

    <!-- gen 2 -->

    | הצעד | מה קרה | התא | השכנים שנבדקו | התור אחרי הצעד | איים | הגודל |
    |:-:|:--|:-:|:--|:--|:-:|:-:|
    | ‏1 | הסריקה פגשה יבשה שלא סומנה : **אי חדש 1**, התא מסומן ונכנס לתור | ‏<span dir="ltr">(0,0)</span> | — | ‏<span dir="ltr">(0,0)</span> | ‏1 | ‏0 |
    | ‏2 | התא יוצא מהתור, הגודל גדל ב-1 | ‏<span dir="ltr">(0,0)</span> | למעלה מחוץ ללוח; למטה <span dir="ltr">(1, 0)</span> **מסומן ונכנס לתור**; שמאלה מחוץ ללוח; ימינה <span dir="ltr">(0, 1)</span> **מסומן ונכנס לתור** | ‏<span dir="ltr">(1,0) (0,1)</span> | ‏1 | ‏1 |
    | ‏3 | התא יוצא מהתור, הגודל גדל ב-1 | ‏<span dir="ltr">(1,0)</span> | למעלה <span dir="ltr">(0, 0)</span> כבר סומן; למטה <span dir="ltr">(2, 0)</span> מים; שמאלה מחוץ ללוח; ימינה <span dir="ltr">(1, 1)</span> **מסומן ונכנס לתור** | ‏<span dir="ltr">(0,1) (1,1)</span> | ‏1 | ‏2 |
    | ‏4 | התא יוצא מהתור, הגודל גדל ב-1 | ‏<span dir="ltr">(0,1)</span> | למעלה מחוץ ללוח; למטה <span dir="ltr">(1, 1)</span> כבר סומן; שמאלה <span dir="ltr">(0, 0)</span> כבר סומן; ימינה <span dir="ltr">(0, 2)</span> מים | ‏<span dir="ltr">(1,1)</span> | ‏1 | ‏3 |
    | ‏5 | התא יוצא מהתור, הגודל גדל ב-1 | ‏<span dir="ltr">(1,1)</span> | למעלה <span dir="ltr">(0, 1)</span> כבר סומן; למטה <span dir="ltr">(2, 1)</span> מים; שמאלה <span dir="ltr">(1, 0)</span> כבר סומן; ימינה <span dir="ltr">(1, 2)</span> מים | ‏ריק | ‏1 | ‏4 |
    | ‏6 | הסריקה עברה 9 תאים של מים או תאים שכבר סומנו, ופגשה יבשה שלא סומנה : **אי חדש 2**, התא מסומן ונכנס לתור | ‏<span dir="ltr">(1,4)</span> | — | ‏<span dir="ltr">(1,4)</span> | ‏2 | ‏0 |
    | ‏7 | התא יוצא מהתור, הגודל גדל ב-1 | ‏<span dir="ltr">(1,4)</span> | למעלה <span dir="ltr">(0, 4)</span> מים; למטה <span dir="ltr">(2, 4)</span> **מסומן ונכנס לתור**; שמאלה <span dir="ltr">(1, 3)</span> מים; ימינה <span dir="ltr">(1, 5)</span> **מסומן ונכנס לתור** | ‏<span dir="ltr">(2,4) (1,5)</span> | ‏2 | ‏1 |
    | ‏8 | התא יוצא מהתור, הגודל גדל ב-1 | ‏<span dir="ltr">(2,4)</span> | למעלה <span dir="ltr">(1, 4)</span> כבר סומן; למטה <span dir="ltr">(3, 4)</span> מים; שמאלה <span dir="ltr">(2, 3)</span> מים; ימינה <span dir="ltr">(2, 5)</span> מים | ‏<span dir="ltr">(1,5)</span> | ‏2 | ‏2 |
    | ‏9 | התא יוצא מהתור, הגודל גדל ב-1 | ‏<span dir="ltr">(1,5)</span> | למעלה <span dir="ltr">(0, 5)</span> מים; למטה <span dir="ltr">(2, 5)</span> מים; שמאלה <span dir="ltr">(1, 4)</span> כבר סומן; ימינה מחוץ ללוח | ‏ריק | ‏2 | ‏3 |
    | ‏10 | הסריקה עברה 10 תאים של מים או תאים שכבר סומנו, ופגשה יבשה שלא סומנה : **אי חדש 3**, התא מסומן ונכנס לתור | ‏<span dir="ltr">(3,3)</span> | — | ‏<span dir="ltr">(3,3)</span> | ‏3 | ‏0 |
    | ‏11 | התא יוצא מהתור, הגודל גדל ב-1 | ‏<span dir="ltr">(3,3)</span> | למעלה <span dir="ltr">(2, 3)</span> מים; למטה <span dir="ltr">(4, 3)</span> **מסומן ונכנס לתור**; שמאלה <span dir="ltr">(3, 2)</span> מים; ימינה <span dir="ltr">(3, 4)</span> מים | ‏<span dir="ltr">(4,3)</span> | ‏3 | ‏1 |
    | ‏12 | התא יוצא מהתור, הגודל גדל ב-1 | ‏<span dir="ltr">(4,3)</span> | למעלה <span dir="ltr">(3, 3)</span> כבר סומן; למטה מחוץ ללוח; שמאלה <span dir="ltr">(4, 2)</span> מים; ימינה <span dir="ltr">(4, 4)</span> מים | ‏ריק | ‏3 | ‏2 |
    | ‏13 | הסריקה עברה את 8 התאים האחרונים (מים או מסומנים) ונגמרה | — | — | ‏ריק | ‏3 | — |

    <!-- /gen -->

    בצעד 2 התא <span dir="ltr">(0, 0)</span> יוצא, ושני שכניו ביבשה נכנסים. בצעד 4 כל ארבעת
    השכנים של <span dir="ltr">(0, 1)</span> כבר מסומנים, מים, או מחוץ ללוח, ולכן שום תא לא
    נכנס. אחרי צעד 5 התור ריק, האי הראשון שלם עם 4 תאים, והסריקה ממשיכה מ-<span dir="ltr">(1, 2)</span> :
    היא עוברת 9 תאים (מים, ותאי האי שכבר סומנו) עד <span dir="ltr">(1, 4)</span>, האי השני. בסך
    הכול 9 הוצאות מהתור, אחת לכל תא יבשה.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="count_islands" linenums="1" hl_lines="10 19 33"
        from collections import deque

        DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]        # up, down, left, right


        def flood(grid: list[str], seen: list[list[bool]], r: int, c: int, dirs=DIRS4) -> int:
            """BFS from the land cell (r, c): marks every land cell of its island in seen, each
            when it is pushed, and returns the island's size."""
            m, n = len(grid), len(grid[0])
            seen[r][c] = True                              # (1)!
            q = deque([(r, c)])
            size = 0
            while q:
                i, j = q.popleft()
                size += 1
                for di, dj in dirs:
                    a, b = i + di, j + dj
                    if 0 <= a < m and 0 <= b < n and grid[a][b] == "1" and not seen[a][b]:   # (2)!
                        seen[a][b] = True
                        q.append((a, b))
            return size


        def count_islands(grid: list[str]) -> int:
            """The number of islands: every land cell the scan meets before any flood reached it
            starts a new island."""
            m, n = len(grid), len(grid[0]) if grid else 0
            seen = [[False] * n for _ in range(m)]
            count = 0
            for r in range(m):
                for c in range(n):
                    if grid[r][c] == "1" and not seen[r][c]:
                        count += 1                         # (3)!
                        flood(grid, seen, r, c)
            return count
        ```

        1. הסימון ברגע הכניסה לתור, גם של התא הראשון. ‏`seen` הוא רשימה של רשימות, ולכן
           הסימונים נשארים אצל הקורא.
        2. הבדיקה `0 <= a < m` נחוצה גם ב-Python : בלעדיה `grid[-1]` הוא השורה **האחרונה**,
           בלי שגיאה, והאיים "מתחברים" דרך הקצה.
        3. תא יבשה שהסריקה פוגשת לפני שאיזו הצפה הגיעה אליו : אי חדש. את הגודל שההצפה
           מחזירה סעיף ג ינצל.

    === "SystemVerilog"
        ```systemverilog title="function count_islands" linenums="1" hl_lines="10 18 36"
        typedef struct { int r, c; } cell_t;
        localparam int DR4[4] = '{-1, 1, 0, 0};             // up, down, left, right
        localparam int DC4[4] = '{0, 0, -1, 1};

        // BFS from the land cell (r, c): marks every land cell of its island in seen, each
        // when it is pushed, and returns the island's size
        function automatic int flood(string grid[], ref bit seen[][], input int r, int c, int dr[], int dc[]);
          int m = grid.size(), n = grid[0].len(), size = 0;
          cell_t q[$], cur;
          seen[r][c] = 1;                                                              // (1)!
          q.push_back('{r, c});
          while (q.size() > 0) begin
            cur = q.pop_front();
            size++;
            foreach (dr[k]) begin
              int a = cur.r + dr[k], b = cur.c + dc[k];
              if (a >= 0 && a < m && b >= 0 && b < n && grid[a].getc(b) == "1" && !seen[a][b]) begin   // (2)!
                seen[a][b] = 1;
                q.push_back('{a, b});
              end
            end
          end
          return size;
        endfunction

        // the number of islands: every land cell the scan meets before any flood reached it
        // starts a new island
        function automatic int count_islands(string grid[]);
          int m = grid.size(), n = m > 0 ? grid[0].len() : 0, count = 0;
          bit seen[][];
          seen = new[m];
          foreach (seen[i]) seen[i] = new[n];
          for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
              if (grid[r].getc(c) == "1" && !seen[r][c]) begin
                count++;                                                               // (3)!
                void'(flood(grid, seen, r, c, DR4, DC4));
              end
          return count;
        endfunction
        ```

        1. הסימון ברגע הכניסה לתור, גם של התא הראשון. ‏`seen` עובר ב-`ref`, כך שהסימונים
           נשארים אצל הקורא ומונעים ספירה כפולה.
        2. הסדר של התנאים חשוב : קודם בודקים שהשכן בתוך הלוח, ורק אז ניגשים ל-`grid[a]`.
           ‏`getc(b)` הוא התו ה-`b` של שורה `a`.
        3. תא יבשה שהסריקה פוגשת לפני שאיזו הצפה הגיעה אליו : אי חדש. ההצפה מסמנת את שאר
           האי, ואת הגודל שהיא מחזירה סעיף ג ינצל.

    #### למה זה נכון { .sol-proof }

    **ההצפה מסמנת בדיוק את האי.** נסמן ב-\( I \) את האי של תא ההתחלה \( s \). שתי הכלות :

    - **רק את האי :** כל תא שנכנס לתור הוא יבשה ושכן של תא שכבר בתור. באינדוקציה על סדר הכניסה,
      מכל תא כזה יש מסלול של שכנים ביבשה עד \( s \), ולכן הוא ב-\( I \).
    - **את כל האי :** נניח שתא \( t \in I \) לא סומן. יש מסלול של שכנים ביבשה מ-\( s \) ל-\( t \);
      יהי \( u \) התא הראשון עליו שלא סומן, ו-\( v \) התא שלפניו, שכן סומן. ‏\( v \) נכנס לתור, ולכן
      גם יצא ממנו (ההצפה נגמרת רק כשהתור ריק), ובאותו רגע \( u \), שכן שלו, יבשה ולא מסומן,
      נכנס וסומן. סתירה.

    **כל תא יבשה נכנס לתור פעם אחת בדיוק.** לכל היותר פעם אחת, כי תא מסומן ברגע הכניסה, ותא
    מסומן לא נכנס שוב. לפחות פעם אחת, כי הסריקה החיצונית מגיעה לכל תא : אם הוא עדיין לא מסומן
    הוא מתחיל הצפה ונכנס, ואם הוא מסומן הוא כבר נכנס קודם.

    **המונה הוא מספר האיים.** המונה גדל פעם אחת לכל הצפה. כל הצפה מסמנת אי שלם, ואי שסומן לא
    מתחיל הצפה שנייה (כל התאים שלו מסומנים). ולכל אי יש הצפה : התא הראשון שלו בסדר הסריקה
    אינו מסומן כשהסריקה מגיעה אליו, כי הצפות קודמות סימנו רק איים אחרים. לכן הצפות ואיים
    מתאימים אחד לאחד.

    **מקרי קצה :** לוח ריק או לוח שכולו מים נותנים 0 : אף תא לא מתחיל הצפה. לוח שכולו יבשה הוא
    אי אחד של \( mn \) תאים. שורה אחת או עמודה אחת : האיים הם הרצפים של `1`.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(mn) \). הסריקה החיצונית עוברת כל תא פעם אחת; בתוך ההצפות כל תא יבשה יוצא
      מהתור פעם אחת ובודק ארבעה שכנים, כלומר לכל היותר \( 4mn \) בדיקות של שכנים בסך הכול,
      בלי קשר למספר האיים או לצורתם.
    - **זיכרון :** ‏\( O(mn) \) ללוח `seen` (ביט לכל תא). התור מחזיק רק את **החזית** של ההצפה :
      בלוח 20 × 20 שכולו יבשה הוא מגיע ל-20 תאים לכל היותר, ואילו מחסנית של DFS מגיעה
      ל-191 ורקורסיה לעומק 400 (כל הלוח). במקרה הגרוע גם התור הוא \( O(mn) \).

    **נסו בעצמכם.** לחיצה על תא הופכת אותו ממים ליבשה ובחזרה, ו"לוח אקראי" מגריל לוח חדש. כל
    צעד הוא תא אחד : אי חדש שנכנס לתור, או תא שיוצא ממנו ושכניו נבדקים. התור מצויר ליד הלוח,
    התא הנוכחי מוקף, וכל אי מקבל צבע ומספר :

    <div class="explorer" data-kind="islands" data-mode="a" data-grid="110000.110011.000010.000100.000100"></div>

---

### סעיף ב – שמונה כיוונים

עכשיו גם תאים שנוגעים זה בזה רק בפינה (באלכסון) הם שכנים : לכל תא עד שמונה שכנים. מה משתנה
באלגוריתם, וכמה איים יש בלוח של הדוגמה?

??? tip "רמז 1"
    מה בקוד של סעיף א יודע שיש בדיוק ארבעה שכנים? אם זו רשימה, מה צריך להוסיף לה?

??? tip "רמז 2"
    בלוח של הדוגמה חפשו שני איים שנוגעים זה בזה בפינה בלבד. ואחרי שפתרתם : בקו אלכסוני של
    יבשה, האם המים משני צדדיו מופרדים?

<div class="selfcheck" data-answer="1" data-show="1 : התא האמצעי נוגע בכל ארבע הפינות באלכסון, ולכן חמשת התאים הם אי אחד" data-hint="עכשיו גם נגיעה בפינה מחברת. באילו תאים נוגע התא האמצעי?" markdown>
באותו לוח <span dir="ltr">101 / 010 / 101</span>, כמה איים יש עם שמונה כיוונים?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        אותו אלגוריתם בדיוק. הדבר היחיד שמשתנה הוא **טבלת הכיוונים** : שמונה זוגות של
        \( (\Delta r, \Delta c) \) במקום ארבעה, והלולאה על השכנים עוברת עליהם. הקוד של ההצפה
        לא יודע כמה שכנים יש לתא. בדוגמה שני האיים של ימין ושל התחתית נוגעים בפינה, ולכן יש
        **2** איים.

    <!-- cost: זמן \( O(mn) \) | זיכרון \( O(mn) \) -->

    #### הרעיון { .sol-idea }

    **טבלת הכיוונים.** בסעיף א השכנים של \( (i, j) \) הם \( (i + \Delta r, j + \Delta c) \) לכל זוג
    בטבלה <span dir="ltr">(−1, 0), (1, 0), (0, −1), (0, 1)</span>. שכנות של שמונה כיוונים
    מוסיפה את ארבע הפינות <span dir="ltr">(−1, −1), (−1, 1), (1, −1), (1, 1)</span>. ההצפה,
    הסימון, הסריקה וההוכחה לא משתנים, כי כולם מדברים על "שכן" ולא על "למעלה" או "ימינה" :
    הגרף קיבל קשתות נוספות, והאלגוריתם למציאת רכיבי קשירות נשאר אותו אלגוריתם. זה בדיוק
    למה כותבים את השכנים כטבלה ולא כארבעה תנאים.

    **מה משתנה בדוגמה.** התא <span dir="ltr">(2, 4)</span> של האי הימני והתא
    <span dir="ltr">(3, 3)</span> של האי התחתון נוגעים בפינה. עם ארבעה כיוונים הם שני איים;
    עם שמונה הם אי אחד של 5 תאים, ובלוח נשארים שני איים :

    <!-- gen 3 -->

    <svg class="figure il-fig" viewBox="0 0 248 208" style="max-width:15.5rem" role="img" aria-label="אותו לוח עם שמונה כיוונים : שני איים, הפינה בין (2, 4) ל-(3, 3) מחברת"><text class="tick" x="44" y="14" text-anchor="middle">0</text><text class="tick" x="80" y="14" text-anchor="middle">1</text><text class="tick" x="116" y="14" text-anchor="middle">2</text><text class="tick" x="152" y="14" text-anchor="middle">3</text><text class="tick" x="188" y="14" text-anchor="middle">4</text><text class="tick" x="224" y="14" text-anchor="middle">5</text><text class="tick" x="18" y="44" text-anchor="end">0</text><text class="tick" x="18" y="80" text-anchor="end">1</text><text class="tick" x="18" y="116" text-anchor="end">2</text><text class="tick" x="18" y="152" text-anchor="end">3</text><text class="tick" x="18" y="188" text-anchor="end">4</text><g class="il-cell is-land il-i1"><title>cell (0, 0): land, island 1 of 4 cells</title><rect x="28" y="24" width="32" height="32" rx="4"/><text x="44" y="45" text-anchor="middle">1</text></g><g class="il-cell is-land il-i1"><title>cell (0, 1): land, island 1 of 4 cells</title><rect x="64" y="24" width="32" height="32" rx="4"/><text x="80" y="45" text-anchor="middle">1</text></g><g class="il-cell is-water"><title>cell (0, 2): water</title><rect x="100" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 3): water</title><rect x="136" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 4): water</title><rect x="172" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 5): water</title><rect x="208" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i1"><title>cell (1, 0): land, island 1 of 4 cells</title><rect x="28" y="60" width="32" height="32" rx="4"/><text x="44" y="81" text-anchor="middle">1</text></g><g class="il-cell is-land il-i1"><title>cell (1, 1): land, island 1 of 4 cells</title><rect x="64" y="60" width="32" height="32" rx="4"/><text x="80" y="81" text-anchor="middle">1</text></g><g class="il-cell is-water"><title>cell (1, 2): water</title><rect x="100" y="60" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (1, 3): water</title><rect x="136" y="60" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i2"><title>cell (1, 4): land, island 2 of 5 cells</title><rect x="172" y="60" width="32" height="32" rx="4"/><text x="188" y="81" text-anchor="middle">2</text></g><g class="il-cell is-land il-i2"><title>cell (1, 5): land, island 2 of 5 cells</title><rect x="208" y="60" width="32" height="32" rx="4"/><text x="224" y="81" text-anchor="middle">2</text></g><g class="il-cell is-water"><title>cell (2, 0): water</title><rect x="28" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 1): water</title><rect x="64" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 2): water</title><rect x="100" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 3): water</title><rect x="136" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i2"><title>cell (2, 4): land, island 2 of 5 cells</title><rect x="172" y="96" width="32" height="32" rx="4"/><text x="188" y="117" text-anchor="middle">2</text></g><g class="il-cell is-water"><title>cell (2, 5): water</title><rect x="208" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 0): water</title><rect x="28" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 1): water</title><rect x="64" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 2): water</title><rect x="100" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i2"><title>cell (3, 3): land, island 2 of 5 cells</title><rect x="136" y="132" width="32" height="32" rx="4"/><text x="152" y="153" text-anchor="middle">2</text></g><g class="il-cell is-water"><title>cell (3, 4): water</title><rect x="172" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 5): water</title><rect x="208" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 0): water</title><rect x="28" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 1): water</title><rect x="64" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 2): water</title><rect x="100" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i2"><title>cell (4, 3): land, island 2 of 5 cells</title><rect x="136" y="168" width="32" height="32" rx="4"/><text x="152" y="189" text-anchor="middle">2</text></g><g class="il-cell is-water"><title>cell (4, 4): water</title><rect x="172" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 5): water</title><rect x="208" y="168" width="32" height="32" rx="4"/></g><line class="il-link" x1="44" y1="40" x2="80" y2="76"><title>a corner link: (0, 0) and (1, 1)</title></line><line class="il-link" x1="80" y1="40" x2="44" y2="76"><title>a corner link: (0, 1) and (1, 0)</title></line><line class="il-link" x1="224" y1="76" x2="188" y2="112"><title>a corner link: (1, 5) and (2, 4)</title></line><line class="il-link" x1="188" y1="112" x2="152" y2="148"><title>a corner link: (2, 4) and (3, 3)</title></line></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="il-key il-i1"></i>אי 1</span><span><i class="il-key il-i2"></i>אי 2</span><span><i class="il-key il-i3"></i>אי 3</span><span><i class="il-key is-water"></i>מים</span><span><i class="il-key-link"></i>חיבור דרך פינה (שמונה כיוונים בלבד)</span></span>

    <!-- /gen -->

    **הפרדוקס של הפינות.** על נייר, קו סגור של יבשה מפריד בין המים שבתוכו למים שבחוץ. על לוח
    של תאים זה כבר לא בטוח. קו אלכסוני של יבשה הוא אי אחד בשמונה כיוונים, אבל שני תאי מים
    משני צדדיו נוגעים זה בזה בפינה **באותה** פינה שדרכה היבשה מחוברת. אם גם המים "מחוברים
    בשמונה כיוונים", הקו לא מפריד כלום; ואם המים מחוברים בארבעה כיוונים בלבד, הקו מפריד, אבל
    אז בארבעה כיוונים הוא עצמו ארבעה איים נפרדים :

    <!-- gen 5 -->

    <svg class="figure il-fig" viewBox="0 0 176 172" style="max-width:11rem" role="img" aria-label="קו אלכסוני של יבשה על לוח 4 על 4 : עם שמונה כיוונים הוא אי אחד, והמים משני הצדדים גם הם מחוברים דרך אותן פינות"><text class="tick" x="44" y="14" text-anchor="middle">0</text><text class="tick" x="80" y="14" text-anchor="middle">1</text><text class="tick" x="116" y="14" text-anchor="middle">2</text><text class="tick" x="152" y="14" text-anchor="middle">3</text><text class="tick" x="18" y="44" text-anchor="end">0</text><text class="tick" x="18" y="80" text-anchor="end">1</text><text class="tick" x="18" y="116" text-anchor="end">2</text><text class="tick" x="18" y="152" text-anchor="end">3</text><g class="il-cell is-water"><title>cell (0, 0): water</title><rect x="28" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 1): water</title><rect x="64" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 2): water</title><rect x="100" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i1"><title>cell (0, 3): land, island 1 of 4 cells</title><rect x="136" y="24" width="32" height="32" rx="4"/><text x="152" y="45" text-anchor="middle">1</text></g><g class="il-cell is-water"><title>cell (1, 0): water</title><rect x="28" y="60" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (1, 1): water</title><rect x="64" y="60" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i1"><title>cell (1, 2): land, island 1 of 4 cells</title><rect x="100" y="60" width="32" height="32" rx="4"/><text x="116" y="81" text-anchor="middle">1</text></g><g class="il-cell is-water"><title>cell (1, 3): water</title><rect x="136" y="60" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 0): water</title><rect x="28" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i1"><title>cell (2, 1): land, island 1 of 4 cells</title><rect x="64" y="96" width="32" height="32" rx="4"/><text x="80" y="117" text-anchor="middle">1</text></g><g class="il-cell is-water"><title>cell (2, 2): water</title><rect x="100" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 3): water</title><rect x="136" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i1"><title>cell (3, 0): land, island 1 of 4 cells</title><rect x="28" y="132" width="32" height="32" rx="4"/><text x="44" y="153" text-anchor="middle">1</text></g><g class="il-cell is-water"><title>cell (3, 1): water</title><rect x="64" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 2): water</title><rect x="100" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 3): water</title><rect x="136" y="132" width="32" height="32" rx="4"/></g><line class="il-link" x1="152" y1="40" x2="116" y2="76"><title>a corner link: (0, 3) and (1, 2)</title></line><line class="il-link" x1="116" y1="76" x2="80" y2="112"><title>a corner link: (1, 2) and (2, 1)</title></line><line class="il-link" x1="80" y1="112" x2="44" y2="148"><title>a corner link: (2, 1) and (3, 0)</title></line></svg>

    <!-- /gen -->

    <!-- gen 6 -->

    | השכנות | איים של יבשה | חלקים של מים | מה זה אומר |
    |:--|:-:|:-:|:--|
    | ארבעה כיוונים | ‏4 | ‏2 | ארבעה תאים בודדים, והמים משני צידי האלכסון מופרדים |
    | שמונה כיוונים | ‏1 | ‏1 | אי אחד, אבל גם המים חוצים את האלכסון דרך אותן פינות : הקו לא מפריד |

    <!-- /gen -->

    לכן בעיבוד תמונה בוחרים שכנות **שונה** ליבשה ולמים : שמונה כיוונים לרקע הקדמי וארבעה לרקע
    האחורי (או להפך). ככה קו סגור תמיד מפריד, וקו שאינו סגור אף פעם לא. השאלה הזו שואלת רק
    על היבשה, ולכן לא נתקלים בפרדוקס; אבל מי שסופר גם "אגמים" (חורים של מים בתוך אי) חייב
    להחליט.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הטבלה :** ‏\( \text{DIRS8} \) היא \( \text{DIRS4} \) ועוד ארבע הפינות. אותם שמות, רק
       ארוכים פי שניים.
    2. **אותה הצפה :** ‏`flood` של סעיף א מקבלת את הטבלה כפרמטר, ולכן אותה פונקציה בדיוק
       מציפה עם שמונה שכנים.
    3. **אותה סריקה :** תא יבשה שלא סומן : אי חדש, והצפה ממנו.
    4. **בדוגמה :** ההצפה של <span dir="ltr">(1, 4)</span> מגיעה דרך <span dir="ltr">(2, 4)</span>
       אל <span dir="ltr">(3, 3)</span> באלכסון, וממנו ל-<span dir="ltr">(4, 3)</span>. כשהסריקה
       מגיעה ל-<span dir="ltr">(3, 3)</span> הוא כבר מסומן. ‏\( \text{count} = 2 \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="count_islands8" linenums="1" hl_lines="1 14"
        DIRS8 = DIRS4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]      # and the four corners


        def count_islands8(grid: list[str]) -> int:
            """The number of islands when a corner also joins: the same scan, the flood with
            eight directions."""
            m, n = len(grid), len(grid[0]) if grid else 0
            seen = [[False] * n for _ in range(m)]
            count = 0
            for r in range(m):
                for c in range(n):
                    if grid[r][c] == "1" and not seen[r][c]:
                        count += 1
                        flood(grid, seen, r, c, DIRS8)   # (1)!
            return count
        ```

        1. ההבדל היחיד מסעיף א : הטבלה של שמונה כיוונים. ‏`flood` עצמה לא משתנה.

    === "SystemVerilog"
        ```systemverilog title="function count_islands8" linenums="1" hl_lines="1 2 15"
        localparam int DR8[8] = '{-1, 1, 0, 0, -1, -1, 1, 1};   // the four of part a, then the corners
        localparam int DC8[8] = '{0, 0, -1, 1, -1, 1, -1, 1};

        // the number of islands when a corner also joins: the same scan, the flood with eight
        // directions
        function automatic int count_islands8(string grid[]);
          int m = grid.size(), n = m > 0 ? grid[0].len() : 0, count = 0;
          bit seen[][];
          seen = new[m];
          foreach (seen[i]) seen[i] = new[n];
          for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
              if (grid[r].getc(c) == "1" && !seen[r][c]) begin
                count++;
                void'(flood(grid, seen, r, c, DR8, DC8));                              // (1)!
              end
          return count;
        endfunction
        ```

        1. ההבדל היחיד מסעיף א : הטבלה של שמונה כיוונים. ‏`flood` עצמה לא משתנה.

    #### למה זה נכון { .sol-proof }

    ההוכחה של סעיף א לא הזכירה את מספר השכנים ולא את הכיוונים שלהם, רק שלושה דברים : "שכן" הוא
    יחס סימטרי (אם \( u \) שכן של \( v \) אז \( v \) שכן של \( u \)), ההצפה בודקת את **כל** השכנים
    של תא שיוצא מהתור, והסריקה מגיעה לכל תא. שמונה כיוונים מקיימים את שלושתם : הטבלה סימטרית
    (לכל \( (\Delta r, \Delta c) \) יש בה גם \( (-\Delta r, -\Delta c) \)), והלולאה עוברת על כולה. לכן
    ההצפה מסמנת בדיוק את רכיב הקשירות בגרף החדש, וכל תא נכנס פעם אחת.

    **איים רק מתאחדים.** כל קשת של ארבעה כיוונים היא גם קשת של שמונה, ולכן כל אי של סעיף א
    מוכל באי אחד של סעיף ב. מכאן שמספר האיים לא גדל, וסכום הגדלים (מספר תאי היבשה) נשאר.
    בלוח <span dir="ltr">101 / 010 / 101</span> חמישה איים הופכים לאחד.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(mn) \), עם לכל היותר \( 8mn \) בדיקות של שכנים במקום \( 4mn \).
    - **זיכרון :** ‏\( O(mn) \), כמו בסעיף א.

    **נסו בעצמכם.** אותה תיבה, עם מתג בין ארבעה לשמונה כיוונים. התיבה מתחילה בשמונה : הפינה
    בין <span dir="ltr">(2, 4)</span> ל-<span dir="ltr">(3, 3)</span> מחברת את שני האיים. עברו
    לארבעה וחזרה, או ציירו קו אלכסוני :

    <div class="explorer" data-kind="islands" data-mode="b" data-grid="110000.110011.000010.000100.000100"></div>

---

### סעיף ג – הגודל של כל אי

החזירו רשימה של הגדלים של האיים, מהגדול לקטן : האורך שלה הוא מספר האיים, וכל איבר הוא מספר
התאים של אי אחד.

??? tip "רמז 1"
    ההצפה עוברת על כל תא של האי בדיוק פעם אחת. איפה בקוד אפשר לספור אותם?

??? tip "רמז 2"
    כל הצפה מחזירה מספר אחד. אוספים את המספרים לרשימה, ורק **בסוף** ממיינים. האי הגדול
    ביותר הוא האיבר הראשון.

<div class="selfcheck" data-answer="5" data-show="5 : האי של הצד הימני והשורה התחתונה, (0, 3) (1, 3) (2, 3) (2, 2) (2, 1); האי השני הוא שלושת התאים של הפינה השמאלית העליונה" data-hint="עקבו אחרי עמודה 3 מלמעלה למטה, ואז שמאלה לאורך השורה התחתונה." markdown>
בלוח <span dir="ltr">1101 / 1001 / 0111</span> (שלוש שורות של ארבעה תאים) עם ארבעה כיוונים, מה
הגודל של האי הגדול ביותר?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ההצפה כבר עוברת על כל תא של האי פעם אחת, ולכן היא סופרת אותם תוך כדי : `size` גדל ב-1
        בכל הוצאה מהתור, וההצפה מחזירה אותו. במקום מונה אוספים רשימה של הגדלים, ובסוף ממיינים
        בסדר יורד. בדוגמה <span dir="ltr">[4, 3, 2]</span> עם ארבעה כיוונים ו-<span dir="ltr">[5, 4]</span>
        עם שמונה. הגודל המקסימלי (Max Area of Island) הוא פשוט האיבר הראשון.

    <!-- cost: זמן \( O(mn + k \log k) \) | זיכרון \( O(mn) \) -->

    #### הרעיון { .sol-idea }

    **הספירה בתוך ההצפה.** כל תא של האי יוצא מהתור פעם אחת בדיוק (ההוכחה של סעיף א), ולכן
    מונה שגדל ב-1 בכל הוצאה הוא בדיוק הגודל של האי כשהתור מתרוקן. זה מה ש-`flood` של סעיף א
    כבר מחזירה; בסעיף א זרקנו את הערך, וכאן שומרים אותו.

    **הרשימה והמיון.** הסריקה מוצאת את האיים בסדר של התא הראשון שלהם, לא לפי גודל. לכן אוספים
    את הגדלים לרשימה כמו שהם, ובסוף ממיינים פעם אחת בסדר יורד. למיין "תוך כדי" (למשל להכניס
    כל גודל למקום הנכון ברשימה) נכון גם כן אבל יקר יותר, ולמיין בסדר עולה מחזיר רשימה הפוכה
    ממה שביקשו. האורך של הרשימה הוא מספר האיים של סעיף א, וסכום האיברים הוא מספר תאי היבשה
    בלוח, שתי בדיקות קלות לקוד.

    <!-- gen 7 -->

    <svg class="figure il-fig" viewBox="0 0 248 208" style="max-width:15.5rem" role="img" aria-label="הלוח של הדוגמה, הגודל של האי כתוב בכל תא שלו"><text class="tick" x="44" y="14" text-anchor="middle">0</text><text class="tick" x="80" y="14" text-anchor="middle">1</text><text class="tick" x="116" y="14" text-anchor="middle">2</text><text class="tick" x="152" y="14" text-anchor="middle">3</text><text class="tick" x="188" y="14" text-anchor="middle">4</text><text class="tick" x="224" y="14" text-anchor="middle">5</text><text class="tick" x="18" y="44" text-anchor="end">0</text><text class="tick" x="18" y="80" text-anchor="end">1</text><text class="tick" x="18" y="116" text-anchor="end">2</text><text class="tick" x="18" y="152" text-anchor="end">3</text><text class="tick" x="18" y="188" text-anchor="end">4</text><g class="il-cell is-land il-i1"><title>cell (0, 0): land, island 1 of 4 cells</title><rect x="28" y="24" width="32" height="32" rx="4"/><text x="44" y="45" text-anchor="middle">4</text></g><g class="il-cell is-land il-i1"><title>cell (0, 1): land, island 1 of 4 cells</title><rect x="64" y="24" width="32" height="32" rx="4"/><text x="80" y="45" text-anchor="middle">4</text></g><g class="il-cell is-water"><title>cell (0, 2): water</title><rect x="100" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 3): water</title><rect x="136" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 4): water</title><rect x="172" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (0, 5): water</title><rect x="208" y="24" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i1"><title>cell (1, 0): land, island 1 of 4 cells</title><rect x="28" y="60" width="32" height="32" rx="4"/><text x="44" y="81" text-anchor="middle">4</text></g><g class="il-cell is-land il-i1"><title>cell (1, 1): land, island 1 of 4 cells</title><rect x="64" y="60" width="32" height="32" rx="4"/><text x="80" y="81" text-anchor="middle">4</text></g><g class="il-cell is-water"><title>cell (1, 2): water</title><rect x="100" y="60" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (1, 3): water</title><rect x="136" y="60" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i2"><title>cell (1, 4): land, island 2 of 3 cells</title><rect x="172" y="60" width="32" height="32" rx="4"/><text x="188" y="81" text-anchor="middle">3</text></g><g class="il-cell is-land il-i2"><title>cell (1, 5): land, island 2 of 3 cells</title><rect x="208" y="60" width="32" height="32" rx="4"/><text x="224" y="81" text-anchor="middle">3</text></g><g class="il-cell is-water"><title>cell (2, 0): water</title><rect x="28" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 1): water</title><rect x="64" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 2): water</title><rect x="100" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (2, 3): water</title><rect x="136" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i2"><title>cell (2, 4): land, island 2 of 3 cells</title><rect x="172" y="96" width="32" height="32" rx="4"/><text x="188" y="117" text-anchor="middle">3</text></g><g class="il-cell is-water"><title>cell (2, 5): water</title><rect x="208" y="96" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 0): water</title><rect x="28" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 1): water</title><rect x="64" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 2): water</title><rect x="100" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i3"><title>cell (3, 3): land, island 3 of 2 cells</title><rect x="136" y="132" width="32" height="32" rx="4"/><text x="152" y="153" text-anchor="middle">2</text></g><g class="il-cell is-water"><title>cell (3, 4): water</title><rect x="172" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (3, 5): water</title><rect x="208" y="132" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 0): water</title><rect x="28" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 1): water</title><rect x="64" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 2): water</title><rect x="100" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-land il-i3"><title>cell (4, 3): land, island 3 of 2 cells</title><rect x="136" y="168" width="32" height="32" rx="4"/><text x="152" y="189" text-anchor="middle">2</text></g><g class="il-cell is-water"><title>cell (4, 4): water</title><rect x="172" y="168" width="32" height="32" rx="4"/></g><g class="il-cell is-water"><title>cell (4, 5): water</title><rect x="208" y="168" width="32" height="32" rx="4"/></g></svg>

    <!-- /gen -->

    <!-- gen 8 -->

    <span class="viz-legend"><span><i class="il-key il-i1"></i>יבשה, צבע לכל אי, הגודל כתוב בתא</span><span><i class="il-key is-water"></i>מים</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הסריקה :** כמו בסעיף א, עם טבלת הכיוונים של הסעיף שבוחרים (ארבעה או שמונה).
    2. **ההצפה סופרת :** בכל הוצאה מהתור \( \text{size} \leftarrow \text{size} + 1 \). כשהתור ריק,
       ההצפה מחזירה את \( \text{size} \).
    3. **הרשימה :** הגודל שחזר נכנס לסוף הרשימה. בדוגמה : 4, אחר כך 3, אחר כך 2.
    4. **המיון :** בסוף ממיינים בסדר יורד. בדוגמה הרשימה כבר ממוינת; בלוח אחר (אי קטן שמופיע
       לפני גדול) המיון משנה את הסדר.

    </div>

    האיים של הדוגמה, התאים שלהם והגדלים, בשתי השכנויות :

    <!-- gen 9 -->

    | השכנות | האי | התאים | הגודל | הרשימה הממוינת |
    |:--|:-:|:--|:-:|:--|
    | ארבעה כיוונים | ‏1 | ‏<span dir="ltr">(0,0) (0,1) (1,0) (1,1)</span> | ‏4 | ‏<span dir="ltr">[4, 3, 2]</span> |
    | ‏— | ‏2 | ‏<span dir="ltr">(1,4) (1,5) (2,4)</span> | ‏3 | ‏— |
    | ‏— | ‏3 | ‏<span dir="ltr">(3,3) (4,3)</span> | ‏2 | ‏— |
    | שמונה כיוונים | ‏1 | ‏<span dir="ltr">(0,0) (0,1) (1,0) (1,1)</span> | ‏4 | ‏<span dir="ltr">[5, 4]</span> |
    | ‏— | ‏2 | ‏<span dir="ltr">(1,4) (1,5) (2,4) (3,3) (4,3)</span> | ‏5 | ‏— |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="island_sizes" linenums="1" hl_lines="11 12"
        def island_sizes(grid: list[str], diag: bool = False) -> list[int]:
            """The size of every island, largest first; diag=True joins across corners too. The
            length of the list is the number of islands, and its sum the number of land cells."""
            m, n = len(grid), len(grid[0]) if grid else 0
            dirs = DIRS8 if diag else DIRS4
            seen = [[False] * n for _ in range(m)]
            sizes = []
            for r in range(m):
                for c in range(n):
                    if grid[r][c] == "1" and not seen[r][c]:
                        sizes.append(flood(grid, seen, r, c, dirs))   # (1)!
            return sorted(sizes, reverse=True)                         # (2)!
        ```

        1. אותה סריקה, רק שהגודל שההצפה מחזירה נשמר ברשימה.
        2. מיון אחד בסוף, בסדר יורד. ‏`len(sizes)` הוא מספר האיים, ו-`sum(sizes)` מספר תאי
           היבשה.

    === "SystemVerilog"
        ```systemverilog title="function island_sizes" linenums="1" hl_lines="12 13"
        // the size of every island, largest first; diag joins across corners too. The length of
        // the queue is the number of islands, and its sum the number of land cells
        function automatic void island_sizes(string grid[], bit diag, output int sizes[$]);
          int m = grid.size(), n = m > 0 ? grid[0].len() : 0;
          bit seen[][];
          sizes = {};
          seen = new[m];
          foreach (seen[i]) seen[i] = new[n];
          for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
              if (grid[r].getc(c) == "1" && !seen[r][c])
                sizes.push_back(diag ? flood(grid, seen, r, c, DR8, DC8) : flood(grid, seen, r, c, DR4, DC4));   // (1)!
          sizes.rsort();                                                                 // (2)!
        endfunction
        ```

        1. אותה סריקה, רק שהגודל שההצפה מחזירה נשמר בתור של התוצאות.
        2. ‏`rsort` ממיין תור בסדר יורד. ‏`sizes.size()` הוא מספר האיים, ו-`sizes.sum()` מספר תאי
           היבשה.

    #### למה זה נכון { .sol-proof }

    **הגודל נכון.** לפי סעיף א, ההצפה מתא \( s \) מוציאה מהתור כל תא של האי של \( s \) פעם אחת
    בדיוק, ואף תא אחר. המונה גדל פעם אחת בכל הוצאה, ולכן הוא מספר התאים של האי.

    **הרשימה שלמה.** הצפות ואיים מתאימים אחד לאחד (סעיף א), ולכן ברשימה יש בדיוק איבר אחד לכל
    אי. האיים זרים זה לזה ומכסים את כל היבשה (כל תא יבשה שייך לאי אחד בדיוק : לרכיב הקשירות
    שלו), ולכן סכום הגדלים הוא מספר תאי היבשה. בדוגמה \( 4 + 3 + 2 = 9 \) וגם \( 5 + 4 = 9 \).

    **המיון בסוף מספיק.** המיון לא משנה את האיברים, רק את הסדר, והרשימה הממוינת היא תוצאה
    שלא תלויה בסדר הסריקה. לכן שתי פונקציות שמוצאות את האיים בסדר שונה (BFS, DFS, או
    union-find של שאלת ההמשך הראשונה) מחזירות אותה רשימה.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(mn) \) להצפות, ועוד \( O(k \log k) \) למיון \( k \) גדלים. יש לכל היותר
      \( \lceil mn / 2 \rceil \) איים (לוח שחמט), ולכן במקרה הגרוע \( O(mn \log(mn)) \). מי שרוצה
      ליניארי ממש ממיין בספירה : הגדלים הם מספרים שלמים בין 1 ל-\( mn \).
    - **זיכרון :** ‏\( O(mn) \) ל-`seen`, ועוד \( O(k) \) לרשימה.

    **נסו בעצמכם.** אותה תיבה : הגודל של כל אי כתוב בתאים שלו וגדל עם ההצפה, ומתחת ללוח
    הרשימה הממוינת, שמתעדכנת כשאי נגמר :

    <div class="explorer" data-kind="islands" data-mode="c" data-grid="110000.110011.000010.000100.000100"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : רקורסיה על לוח גדול"
    ‏DFS רקורסיבי (`dfs(r, c)` שקוראת לעצמה על כל שכן) הוא הפתרון הקצר ביותר, ונופל על לוח
    גדול : בלוח \( 1000 \times 1000 \) שכולו יבשה עומק הרקורסיה מגיע למיליון, כי המסלול
    מתפתל דרך כל הלוח (על 20 × 20 העומק הוא 400, כל התאים). ב-Python הגבול הוא 1,000
    קריאות ומתקבל `RecursionError`; ב-C נגמר המחסנית של התהליך. תור או מחסנית מפורשת, כמו
    בקוד, לא מוגבלים כך, ועם תור (BFS) הזיכרון הוא רק החזית של ההצפה.

??? trap "מלכודת : לסמן תא כשהוא יוצא מהתור ולא כשהוא נכנס"
    אם בודקים `seen` רק ביציאה מהתור, תא יכול להיכנס פעמיים, משני שכנים שונים, לפני שאחד
    העותקים יוצא ומסמן אותו. התוצאה עדיין נכונה (העותק השני נזרק), אבל התור מתנפח : בלוח
    20 × 20 שכולו יבשה 761 הכנסות במקום 400, ובשמונה כיוונים יותר. בקוד התא מסומן בשורה שבה
    הוא נכנס לתור, ולכן מספר ההכנסות שווה בדיוק למספר תאי היבשה.

??? trap "מלכודת : לשכוח את גבולות הלוח"
    שכן של תא בשורה 0 הוא בשורה \( -1 \). ב-SystemVerilog קריאה מחוץ למערך מחזירה 0 או X בלי
    להפיל את הריצה, וב-Python `grid[-1]` הוא פשוט השורה **האחרונה** : איים בשורה הראשונה
    ובשורה האחרונה מתאחדים בשקט, בלי שום שגיאה. הבדיקה `0 <= a < m and 0 <= b < n` באה
    **לפני** הגישה ללוח, בגלל סדר הערכה משמאל לימין.

??? trap "מלכודת : לספור אלכסונים בסעיף א, או לשכוח אותם בסעיף ב"
    מי שכותב את השכנים כארבעה תנאים מפורשים מתקשה לעבור בין הסעיפים ושוכח כיוון. בלוח של
    הדוגמה ארבעה כיוונים נותנים 3 ושמונה נותנים 2 : בדיקה אחת מגלה טעות. טבלת כיוונים אחת,
    שמועברת להצפה כפרמטר, היא ההבדל היחיד בין הסעיפים.

??? trap "מלכודת : למיין לפני שאספו, או בסדר הלא נכון"
    למיין את הרשימה אחרי כל אי חדש נותן \( O(k^2 \log k) \) במקום מיון אחד; ו-`sort()` בלי
    `reverse=True` (או `sort` במקום `rsort` ב-SystemVerilog) מחזיר מהקטן לגדול, בדיוק הפוך
    ממה שביקשו, וטסט שבודק רק את האורך ואת הסכום לא יתפוס את זה. בודקים גם את האיבר
    הראשון מול האי הגדול ביותר.

??? followup "שאלות המשך"
    - **איים שנוספים תא אחרי תא (LC 305) :** הלוח מתחיל כולו מים, ובכל צעד תא אחד הופך
      ליבשה. איך מחזירים את מספר האיים אחרי כל צעד, בלי לסרוק את כל הלוח מחדש?

        ??? fu-answer "תשובה"
            עם **union-find** (מבנה של קבוצות זרות עם `find` ו-`union`). תא חדש הוא קבוצה חדשה
            והמונה גדל ב-1; לכל שכן שלו ביבשה שהשורש שלו שונה, מאחדים והמונה קטן ב-1. כל צעד
            עולה כמעט \( O(1) \) (דחיסת מסלולים ואיחוד לפי גודל), במקום \( O(mn) \) לסריקה מחדש.
            על הדוגמה, הוספת התאים בסדר הסריקה נותנת את המונים
            <span dir="ltr">1, 1, 1, 1, 2, 2, 2, 3, 3</span>.

    - **ההיקף של אי (LC 463) :** אורך החוף של אי יחיד, כשכל צלע של תא היא יחידה אחת.

        ??? fu-answer "תשובה"
            כל תא תורם 4 צלעות, וכל זוג תאים שכנים (בצלע) חולק צלע אחת שלא נספרת, פעמיים : ‏\( 4 \cdot \text{cells} - 2 \cdot \text{shared} \).
            אפשר גם לספור תוך כדי ההצפה : לכל תא שיוצא מהתור, כל שכן שהוא מים או מחוץ ללוח
            הוא צלע של חוף. בדוגמה האי של 4 תאים (ריבוע) : ‏\( 16 - 2 \cdot 4 = 8 \), והאי של 3
            תאים (צורת L) : ‏\( 12 - 2 \cdot 2 = 8 \) גם כן.

    - **כמה צורות שונות של איים (LC 694) :** שני איים נחשבים זהים אם הזזה בלבד (בלי סיבוב או
      שיקוף) מעבירה אחד לשני.

        ??? fu-answer "תשובה"
            נותנים לכל אי **ייצוג קנוני** : אוסף התאים שלו ביחס לתא הראשון שלו בסדר הסריקה
            (מחסירים ממנו את השורה והעמודה של התא הראשון), או רצף הצעדים של ההצפה בסדר קבוע.
            שתי צורות זהות נותנות אותו ייצוג. שמים את הייצוגים בקבוצה (set), וגודל הקבוצה הוא
            התשובה. בדוגמה שלוש צורות שונות : ריבוע, L ומקל.

    - **לוח תלת-ממדי :** הלוח הוא \( m \times n \times p \) תאים (למשל שכבות של תמונה רפואית, או
      שכבות מתכת בפריסה). מה משתנה?

        ??? fu-answer "תשובה"
            רק טבלת הכיוונים ומספר הקואורדינטות : שישה שכנים בצלעות (\( \pm 1 \) בכל ציר), או 26
            עם הפינות והמקצועות. ההצפה, הסימון והסריקה זהים, והזמן \( O(mnp) \). זה בדיוק היתרון
            של לכתוב את השכנים כטבלה.
