---
id: 30
title: העכביש והזבוב – הדרך הקצרה ביותר על פני קופסה
level: junior
difficulty: medium
tags: [math, geometry, logic-puzzles]
source: ""
added: 2026-10-20
---

## השאלה

חדר בצורת תיבה : אורכו 30, רוחבו 12 וגובהו 12 (ביחידות כלשהן). על אחד מקירות הקצה יושב
עכביש, באמצע הרוחב, יחידה אחת מתחת לתקרה. על קיר הקצה שממול יושב זבוב, גם הוא באמצע
הרוחב, יחידה אחת מעל הרצפה. הזבוב לא זז. העכביש הולך רק על פני התיבה : על הקירות, על
התקרה ועל הרצפה, ולא דרך האוויר.

<!-- gen 0 -->

<svg class="figure" viewBox="0 0 530 266" style="max-width:36rem" role="img" aria-label="קופסה באורך 30, רוחב 12 וגובה 12 : העכביש על הקיר השמאלי, 11 מתחת לתקרה, והזבוב על הקיר הימני, 1 מעל הרצפה, שניהם באמצע הרוחב"><polygon class="box-end" points="50.0,236.0 110.5,175.5 110.5,31.5 50.0,92.0"><title>הקיר של העכביש (x = 0)</title></polygon><polygon class="box-face" points="50.0,92.0 410.0,92.0 470.5,31.5 110.5,31.5"><title>התקרה</title></polygon><polygon class="box-face" points="50.0,236.0 410.0,236.0 410.0,92.0 50.0,92.0"><title>הקיר הקרוב</title></polygon><polygon class="box-end" points="410.0,236.0 470.5,175.5 470.5,31.5 410.0,92.0" style="fill-opacity:0.25"><title>הקיר של הזבוב (x = 30)</title></polygon><line class="box-edge" x1="50.0" y1="236.0" x2="410.0" y2="236.0"/><line class="box-edge" x1="410.0" y1="236.0" x2="410.0" y2="92.0"/><line class="box-edge" x1="410.0" y1="92.0" x2="50.0" y2="92.0"/><line class="box-edge" x1="50.0" y1="92.0" x2="50.0" y2="236.0"/><line class="box-edge" x1="50.0" y1="92.0" x2="110.5" y2="31.5"/><line class="box-edge" x1="110.5" y1="31.5" x2="470.5" y2="31.5"/><line class="box-edge" x1="470.5" y1="31.5" x2="410.0" y2="92.0"/><line class="box-edge" x1="50.0" y1="236.0" x2="110.5" y2="175.5"/><line class="box-edge" x1="110.5" y1="175.5" x2="110.5" y2="31.5"/><line class="box-edge" x1="110.5" y1="175.5" x2="470.5" y2="175.5" stroke-dasharray="5 4"/><line class="box-edge" x1="470.5" y1="175.5" x2="410.0" y2="236.0" stroke-dasharray="5 4"/><line class="box-edge" x1="470.5" y1="175.5" x2="470.5" y2="31.5" stroke-dasharray="5 4"/><text class="legend" x="230.0" y="254.0" text-anchor="middle" style="font-size:14px">a = 30</text><text class="legend" x="434.0" y="169.0" text-anchor="middle" style="font-size:14px">h = 12</text><text class="legend" x="466.2" y="211.8" text-anchor="middle" style="font-size:14px">b = 12</text><line class="ink-line" x1="80.2" y1="73.8" x2="80.2" y2="61.8" stroke-width="1.2" stroke-dasharray="3 3"/><text class="legend" x="87.2" y="71.8" text-anchor="start" style="font-size:13px">1</text><line class="ink-line" x1="440.2" y1="193.8" x2="440.2" y2="205.8" stroke-width="1.2" stroke-dasharray="3 3"/><text class="legend" x="449.2" y="203.8" text-anchor="start" style="font-size:13px">1</text><circle class="s1-dot" cx="80.2" cy="73.8" r="6"><title>העכביש S = (0, 6, 11)</title></circle><text class="legend" x="91.2" y="90.8" text-anchor="start" style="font-size:18px">S</text><circle class="s2-dot" cx="440.2" cy="193.8" r="6"><title>הזבוב F = (30, 6, 1)</title></circle><text class="legend" x="429.2" y="184.8" text-anchor="end" style="font-size:18px">F</text><line class="axis-c" x1="50.0" y1="236.0" x2="134.0" y2="236.0"/><text class="legend" x="140.0" y="241.0" text-anchor="middle" style="font-size:14px" font-style="italic">x</text><line class="axis-c" x1="50.0" y1="236.0" x2="85.3" y2="200.7"/><text class="legend" x="91.3" y="205.7" text-anchor="middle" style="font-size:14px" font-style="italic">y</text><line class="axis-c" x1="50.0" y1="236.0" x2="50.0" y2="152.0"/><text class="legend" x="50.0" y="148.0" text-anchor="middle" style="font-size:14px" font-style="italic">z</text></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="s1"></i>העכביש S</span><span><i class="s2"></i>הזבוב F</span><span><i class="box-end"></i>קירות הקצה, x = 0 ו-x = a</span><span><i class="box-face"></i>הפאות הצדדיות</span></span>

<!-- /gen -->

נסמן את הצירים כמו באיור : \( x \) לאורך החדר, מ-0 עד \( a = 30 \), ‏\( y \) לרוחב, מ-0
עד \( b = 12 \), ו-\( z \) לגובה, מ-0 עד \( h = 12 \). שש הפאות נקראות כמו בממשק
שבהמשך : ‏`end0` הוא הקיר \( x = 0 \), ‏`enda` הוא הקיר \( x = a \), ‏`top` ו-`bottom` הן
התקרה והרצפה, ו-`side0` ו-`sideB` הם הקירות \( y = 0 \) ו-\( y = b \). העכביש נמצא
ב-\( S = (0, 6, 11) \) והזבוב ב-\( F = (30, 6, 1) \).

??? interviewer "מה המראיין בודק"
    - **לא להאמין לתשובה הראשונה :** המסלול "ישר מעל התקרה" נראה הכי קצר, והוא לא. הבדיקה
      היא אם המועמד מחפש חלופות אחרי שיש לו תשובה.
    - **פריסה :** להבין שמסלול על פני גוף הוא קו ישר כשפורסים את הפאות שהוא עובר דרכן
      למישור, ושפריסות שונות נותנות קווים שונים.
    - **שלמות :** לדעת להסביר למה מספיק לבדוק מספר סופי של פריסות, ולמה קו בפריסה
      הוא מסלול אמיתי רק אם הוא נשאר בתוך הפאות.
    - **מהרעיון לקוד :** לבחור ייצוג (הרצועה המחזורית) שהופך את החיפוש ללולאה קצרה
      וקריאה, ולא לסבך של מקרים.

---

### סעיף א – המרחק הקצר ביותר והמסלול

מהו המרחק הקצר ביותר שהעכביש צריך ללכת כדי להגיע לזבוב, ומהו המסלול? תארו את המסלול
בנקודות : איפה העכביש עוזב כל פאה ולאיזו פאה הוא עובר.

??? tip "רמז 1"
    מסלול על פני התיבה עובר דרך כמה פאות. פרסו את הפאות האלה למישור, כמו שפותחים קופסת
    קרטון : המסלול הופך לקו, והקו הקצר ביותר בין שתי נקודות במישור הוא ישר.

??? tip "רמז 2"
    המסלול שעולה לתקרה, חוצה אותה לאורכה ויורד לזבוב הוא באורך \( 1 + 30 + 11 = 42 \).
    נסו פריסות שעוברות דרך **יותר** פאות : הקו הישר עשוי להיות קצר יותר, גם אם הוא חוצה
    יותר קפלים.

??? tip "רמז 3"
    הצמידו את הקיר של העכביש לתקרה, את התקרה לאחד הקירות הארוכים, את הקיר הזה לרצפה, ואת
    הרצפה לקיר של הזבוב, במדרגות. בפריסה הזו \( S \) ו-\( F \) הם קודקודים של משולש
    ישר-זווית. מדדו את הניצבים.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        המרחק הקצר ביותר הוא **40**, ולא 42. המסלול עובר דרך חמש פאות : הקיר של העכביש,
        התקרה, אחד הקירות הארוכים, הרצפה והקיר של הזבוב. בפריסה הוא היתר של משולש
        ישר-זווית עם ניצבים 32 ו-24.

    #### הרעיון { .sol-idea }

    על פני גוף אין "קו ישר", אבל יש תחליף : בוחרים את סדר הפאות שהמסלול עובר דרכן, ופורסים
    אותן למישור סביב הצלעות המשותפות, כמו קרטון שפותחים. הפריסה שומרת אורכים, ולכן המסלול
    הקצר ביותר **בסדר פאות נתון** הוא קו ישר בפריסה, בתנאי שהקו באמת נשאר בתוך הפאות.
    נשאר לעבור על סדרי הפאות האפשריים, למדוד את הקו הישר בכל אחד, ולקחת את הקצר ביותר.
    ההפתעה : הקו הקצר ביותר עובר דרך חמש פאות, ולא דרך שלוש.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המסלול המתבקש, 42 :** העכביש עולה יחידה אחת לתקרה, חוצה את התקרה לאורכה, 30, ויורד
       11 אל הזבוב. בפריסה של שלוש הפאות האלה בשורה אחת זה קו ישר, ואורכו
       \( 1 + 30 + 11 = 42 \). אותו אורך בדיוק דרך הרצפה : ‏\( 11 + 30 + 1 \).

        <!-- gen 2 -->

        <svg class="figure" viewBox="0 0 542 182" style="max-width:36rem" role="img" aria-label="פריסה של הקיר של העכביש, התקרה והקיר של הזבוב בשורה אחת : קו ישר באורך 42"><rect class="box-end" x="28.0" y="34.0" width="108.0" height="108.0"><title>הקיר של העכביש</title></rect><text class="legend" x="35.0" y="54.0" text-anchor="start" style="font-size:16px">end0</text><rect class="box-face" x="136.0" y="34.0" width="270.0" height="108.0"><title>התקרה</title></rect><text class="legend" x="143.0" y="54.0" text-anchor="start" style="font-size:16px">top</text><rect class="box-end" x="406.0" y="34.0" width="108.0" height="108.0"><title>הקיר של הזבוב</title></rect><text class="legend" x="413.0" y="54.0" text-anchor="start" style="font-size:16px">enda</text><line class="box-path" x1="127.0" y1="88.0" x2="505.0" y2="88.0" stroke-width="3"/><circle class="s1-dot" cx="127.0" cy="88.0" r="5"></circle><text class="legend" x="127.0" y="77.0" text-anchor="middle" style="font-size:18px">S</text><circle class="s2-dot" cx="505.0" cy="88.0" r="5"></circle><text class="legend" x="505.0" y="77.0" text-anchor="middle" style="font-size:18px">F</text><text class="legend" x="316.0" y="78.0" text-anchor="middle" style="font-size:17px">1 + 30 + 11 = 42</text><text class="legend" x="136.0" y="159.0" text-anchor="middle" style="font-size:14px">x = 0</text><text class="legend" x="406.0" y="159.0" text-anchor="middle" style="font-size:14px">x = 30</text></svg>

        <!-- /gen -->

    2. **דרך קיר ארוך, 43.17 :** אפשר לעבור במקום זה דרך אחד הקירות הארוכים. בפריסה
       \( S \) ו-\( F \) נמצאים שניהם 6 מהקפל, אבל בגבהים 11 ו-1, ולכן
       \( \sqrt{42^2 + 10^2} \approx 43.17 \). ארוך יותר.

    3. **חמש פאות, 40 :** עכשיו פורסים במדרגות : הקיר של העכביש מוצמד לתקרה לאורך הצלע
       העליונה שלו, התקרה לקיר הרחוק, הקיר הרחוק לרצפה, והרצפה לקיר של הזבוב לאורך הצלע
       התחתונה שלו. בפריסה הזו \( S \) נמצא יחידה אחת משמאל לקצה התקרה, ו-\( F \) יחידה
       אחת מימין לקצה הרצפה. ההפרש האופקי הוא \( 1 + 30 + 1 = 32 \), וההפרש האנכי הוא
       הרוחב של הקיר הרחוק, 12, ועוד חצי רוחב של התקרה וחצי רוחב של הרצפה, ‏\( 6 + 6 \),
       ביחד 24 :

        \[
        \begin{aligned}
        d &= \sqrt{32^2 + 24^2} \\
          &= \sqrt{1{,}024 + 576} = \sqrt{1{,}600} = 40
        \end{aligned}
        \]

        <!-- gen 3 -->

        <svg class="figure" viewBox="0 0 542 362" style="max-width:36rem" role="img" aria-label="פריסה של חמש פאות במדרגות : הקיר של העכביש על התקרה, התקרה, הקיר הרחוק, הרצפה והקיר של הזבוב על הרצפה. הקו הישר הוא היתר של משולש ישר-זווית עם ניצבים 32 ו-24, ואורכו 40"><rect class="box-end" x="28.0" y="16.0" width="108.0" height="108.0"><title>הקיר של העכביש</title></rect><text class="legend" x="35.0" y="36.0" text-anchor="start" style="font-size:16px">end0</text><rect class="box-face" x="136.0" y="16.0" width="270.0" height="108.0"><title>התקרה</title></rect><text class="legend" x="143.0" y="36.0" text-anchor="start" style="font-size:16px">top</text><rect class="box-face" x="136.0" y="124.0" width="270.0" height="108.0"><title>הקיר הרחוק</title></rect><text class="legend" x="143.0" y="144.0" text-anchor="start" style="font-size:16px">sideB</text><rect class="box-face" x="136.0" y="232.0" width="270.0" height="108.0"><title>הרצפה</title></rect><text class="legend" x="143.0" y="252.0" text-anchor="start" style="font-size:16px">bottom</text><rect class="box-end" x="406.0" y="232.0" width="108.0" height="108.0"><title>הקיר של הזבוב</title></rect><text class="legend" x="413.0" y="252.0" text-anchor="start" style="font-size:16px">enda</text><line class="ink-line" x1="127.0" y1="70.0" x2="415.0" y2="70.0" stroke-width="1.2" stroke-dasharray="5 4"/><line class="ink-line" x1="415.0" y1="70.0" x2="415.0" y2="286.0" stroke-width="1.2" stroke-dasharray="5 4"/><text class="legend" x="271.0" y="62.0" text-anchor="middle" style="font-size:16px">Δx = 32</text><text class="legend" x="425.0" y="183.0" text-anchor="start" style="font-size:16px">Δp = 24</text><line class="box-path" x1="127.0" y1="70.0" x2="415.0" y2="286.0" stroke-width="3"/><circle class="ink-dot" cx="199.0" cy="124.0" r="3.5"><title>חוצה את הקפל בנקודה x = 7</title></circle><circle class="ink-dot" cx="343.0" cy="232.0" r="3.5"><title>חוצה את הקפל בנקודה x = 23</title></circle><circle class="s3-dot" cx="136.0" cy="76.8" r="4"><title>יוצא מהקיר של העכביש ב-y = 6.75</title></circle><circle class="s3-dot" cx="406.0" cy="279.2" r="4"><title>נכנס לקיר של הזבוב ב-y = 6.75</title></circle><circle class="s1-dot" cx="127.0" cy="70.0" r="5"></circle><text class="legend" x="127.0" y="58.0" text-anchor="middle" style="font-size:18px">S</text><circle class="s2-dot" cx="415.0" cy="286.0" r="5"></circle><text class="legend" x="429.0" y="292.0" text-anchor="middle" style="font-size:18px">F</text><text class="legend" x="235.0" y="206.0" text-anchor="middle" style="font-size:18px">d = 40</text><text class="legend" x="136.0" y="357.0" text-anchor="middle" style="font-size:14px">x = 0</text><text class="legend" x="406.0" y="357.0" text-anchor="middle" style="font-size:14px">x = 30</text></svg>

        <!-- /gen -->

        <!-- gen 4 -->

        <span class="viz-legend"><span><i class="box-path"></i>המסלול, קו ישר בפריסה</span><span><i class="s1"></i>העכביש S</span><span><i class="s2"></i>הזבוב F</span><span><i class="s3"></i>יציאה מקיר הקצה וכניסה אליו</span><span><i class="ink"></i>חציית קפל</span></span>

        <!-- /gen -->

    4. **האם הקו חוקי :** קו ישר בפריסה הוא מסלול אמיתי רק אם הוא חוצה את הפאות דרך
       הצלעות שלאורכן פרסנו. כאן הקו יוצא מהקיר של העכביש דרך הצלע העליונה, חוצה את
       הקפל בין התקרה לקיר הרחוק ב-\( x = 7 \), את הקפל בין הקיר הרחוק לרצפה ב-\( x = 23 \),
       ונכנס לקיר של הזבוב דרך הצלע התחתונה. כל הנקודות האלה בתוך הצלעות, ולכן המסלול
       קיים.

    5. **כל הפריסות :** מסלול מקיר אחד לקיר שממול עובר דרך פאה צדדית אחת, שתיים, שלוש או
       ארבע, בלי לחזור על פאה. יש 16 סדרים כאלה, ולכל אחד פריסה אחת וקו ישר אחד. בטבלה
       הניצבים של כל קו והאורך שלו. שני הקווים של 40 הם תמונת ראי זה של זה, דרך הקיר
       הרחוק או דרך הקיר הקרוב :

        <!-- gen 5 -->

        | הפאות שהמסלול עובר | ‏\( \Delta x \) | ‏\( \Delta p \) | האורך |
        |---|---|---|---|
        | ‏end0 → top → sideB → bottom → enda | ‏32 | ‏24 | ‏40 |
        | ‏end0 → top → side0 → bottom → enda | ‏32 | ‏24 | ‏40 |
        | ‏end0 → side0 → bottom → enda | ‏37 | ‏17 | ‏40.72 |
        | ‏end0 → sideB → bottom → enda | ‏37 | ‏17 | ‏40.72 |
        | ‏end0 → top → side0 → enda | ‏37 | ‏17 | ‏40.72 |
        | ‏end0 → top → sideB → enda | ‏37 | ‏17 | ‏40.72 |
        | ‏end0 → bottom → enda | ‏42 | ‏0 | ‏42 |
        | ‏end0 → top → enda | ‏42 | ‏0 | ‏42 |
        | ‏end0 → side0 → enda | ‏42 | ‏10 | ‏43.17 |
        | ‏end0 → sideB → enda | ‏42 | ‏10 | ‏43.17 |
        | ‏end0 → bottom → side0 → enda | ‏47 | ‏7 | ‏47.52 |
        | ‏end0 → bottom → sideB → enda | ‏47 | ‏7 | ‏47.52 |
        | ‏end0 → side0 → top → enda | ‏47 | ‏7 | ‏47.52 |
        | ‏end0 → sideB → top → enda | ‏47 | ‏7 | ‏47.52 |
        | ‏end0 → bottom → side0 → top → enda | ‏52 | ‏24 | ‏57.27 |
        | ‏end0 → bottom → sideB → top → enda | ‏52 | ‏24 | ‏57.27 |

        <!-- /gen -->

    6. **המסלול במרחב :** מחזירים את נקודות החצייה של הקו לפאות המקוריות. העכביש הולך על
       הקיר שלו מ-\( (0, 6, 11) \) לצלע התקרה ב-\( (0, 6.75, 12) \), חוצה את התקרה באלכסון
       עד הצלע עם הקיר הרחוק ב-\( (7, 12, 12) \), יורד על הקיר הרחוק באלכסון עד הרצפה
       ב-\( (23, 12, 0) \), חוצה את הרצפה עד הקיר של הזבוב ב-\( (30, 6.75, 0) \), ועולה אל
       \( (30, 6, 1) \). האורכים : ‏\( 1.25 + 8.75 + 20 + 8.75 + 1.25 = 40 \).

    </div>

    #### למה זה נכון { .sol-proof }

    **קו ישר בפריסה הוא המסלול הקצר ביותר בסדר הפאות שלו.** הפריסה מעתיקה כל פאה למישור
    בלי לשנות אורכים, ושתי פאות סמוכות נפרסות כך שהצלע המשותפת שלהן היא קטע אחד. לכן כל
    מסלול שעובר דרך הפאות בסדר הזה הופך בפריסה לעקומה באותו אורך, מ-\( S \) ל-\( F \), והקו
    הישר הוא הקצר מכולן. בכיוון ההפוך, קו ישר שנשאר בתוך הפאות הפרוסות מתקפל חזרה למסלול
    על פני התיבה באותו אורך.

    **מספיק לבדוק סדרים בלי חזרה.** אם מסלול חוזר לפאה שכבר ביקר בה, הקטע הישר בתוך
    הפאה בין שני הביקורים קצר יותר מהעיקוף, ולכן המסלול לא היה הקצר ביותר. גם ביקור חוזר
    בקיר של העכביש או של הזבוב מתקצר כך. נשארים 16 סדרים : פאה צדדית אחת (4), שתי פאות
    סמוכות (8), שלוש (8) או ארבע (8), ומהם רק 16 נותנים קו ישר שחוקי, כמו בטבלה. המינימום
    ביניהם, 40, הוא המינימום על פני כל המסלולים.

    **חסם תחתון.** המרחק הישר במרחב, דרך האוויר, הוא \( \sqrt{30^2 + 10^2} \approx 31.6 \).
    אף מסלול על פני התיבה לא יכול להיות קצר ממנו, ו-40 לא רחוק ממנו.

    **נסו בעצמכם.** הממשק הזה מראה את התיבה בתלת-ממד, את הפריסה ואת המסלול הקצר ביותר, ואפשר
    לגרור את העכביש ואת הזבוב לכל נקודה על פני התיבה ולשנות את המידות. הכפתור
    "Animate the box unfolding" מראה איך הפאות נפתחות למישור :

    <iframe class="tool-frame" src="../../../assets/spider-fly.html" title="Spider and fly: shortest path on a box" loading="lazy"></iframe>

    [‏לפתיחת הממשק בלשונית נפרדת](../../assets/spider-fly.html){ target="_blank" rel="noopener" }

---

### סעיף ב – קוד : העכביש על `end0`, הזבוב על `enda`

כתבו פונקציה שמקבלת את המידות \( a, b, h \), את מקום העכביש \( (0, y_0, z_0) \) על הקיר
`end0` ואת מקום הזבוב \( (a, y_1, z_1) \) על הקיר `enda`, ומחזירה את המרחק הקצר ביותר
ואת הנקודה שבה העכביש עוזב את הקיר שלו : הנקודה על אחת מארבע הצלעות של `end0` שאליה הוא
הולך בקו ישר. הקוד צריך להיות קריא, ועדיף בלי טיפול נפרד בכל אחת מ-16 הפריסות.

??? tip "רמז 1"
    ארבע הפאות הצדדיות עוטפות את התיבה כמו חישוק. פרסו אותן לרצועה אחת לאורך \( x \) :
    רצפה, קיר רחוק, תקרה, קיר קרוב, ושוב רצפה. קואורדינטה אחת, \( p \), עוברת סביב ההיקף,
    והיא מחזורית עם מחזור \( 2(b + h) \).

??? tip "רמז 2"
    הקיר של העכביש מתקפל על הרצועה סביב אחת מארבע הצלעות שלו. בכל קיפול העכביש נוחת
    במקום אחר במישור : במרחק שלו מאותה צלע, שמאלה מ-\( x = 0 \), ובגובה \( p \) של
    הנקודה הקרובה אליו על הצלע. ארבע דמויות לעכביש, ארבע לזבוב.

??? tip "רמז 3"
    קו ישר מדמות של העכביש לדמות של הזבוב הוא מסלול חוקי אם הוא חוצה את \( x = 0 \) בתוך
    הצלע שקיפלנו סביבה, ואת \( x = a \) בתוך הצלע של הזבוב. אל תשכחו שהזבוב יכול להיות גם
    מחזור אחד למעלה או למטה ברצועה.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        פורסים את הפאות הצדדיות לרצועה מחזורית, מציבים בה ארבע דמויות לעכביש וארבע לזבוב,
        ובודקים \( 4 \cdot 4 \cdot 3 = 48 \) קווים ישרים, עם הזזה של מחזור אחד למעלה ולמטה.
        לכל קו שתי בדיקות : שהוא חוצה את \( x = 0 \) בתוך צלע היציאה ואת \( x = a \) בתוך
        צלע הכניסה. הקו החוקי הקצר ביותר הוא התשובה, ונקודת החצייה שלו עם \( x = 0 \) היא
        נקודת היציאה. ‏\( O(1) \), בלי רקורסיה ובלי טיפול נפרד בפריסות.

    <!-- cost: זמן \( O(1) \) | קווים 48 -->

    #### הרעיון { .sol-idea }

    במקום 16 פריסות שונות, פריסה אחת שמכילה את כולן. ארבע הפאות הצדדיות נפרסות לרצועה
    \( 0 \le x \le a \), עם קואורדינטת היקף \( p \) שמתחילה ברצפה ועוברת לקיר הרחוק,
    לתקרה ולקיר הקרוב. הרצועה מחזורית : ‏\( p \) ו-\( p + 2(b + h) \) הם אותה נקודה. קיר
    קצה שמתקפל על הרצועה סביב צלע מסוימת מוסיף לרצועה מלבן, והעכביש או הזבוב מקבלים בו
    דמות. בחירה של צלע לעכביש, צלע לזבוב והזזה מחזורית לזבוב היא בדיוק בחירה של פריסה,
    והקו הישר בין שתי הדמויות הוא הקו של אותה פריסה :

    <!-- gen 6 -->

    <svg class="figure" viewBox="0 0 477 554" style="max-width:40rem" role="img" aria-label="הרצועה המחזורית של ארבע הפאות הצדדיות, עם ארבע הדמויות של העכביש משמאל וארבע הדמויות של הזבוב מימין, חלקן גם מחזור אחד למעלה ולמטה. הקו הישר הקצר ביותר שיוצא דרך צלע נכונה הוא המסלול"><rect class="box-copy" x="130.8" y="445.6" width="216.0" height="86.4"><title>הקיר הקרוב (עותק מחזורי)</title></rect><rect class="box-face" x="130.8" y="359.2" width="216.0" height="86.4"><title>הרצפה</title></rect><text class="legend" x="137.8" y="377.2" text-anchor="start" style="font-size:14px">bottom</text><rect class="box-face" x="130.8" y="272.8" width="216.0" height="86.4"><title>הקיר הרחוק</title></rect><text class="legend" x="137.8" y="290.8" text-anchor="start" style="font-size:14px">sideB</text><rect class="box-face" x="130.8" y="186.4" width="216.0" height="86.4"><title>התקרה</title></rect><text class="legend" x="137.8" y="204.4" text-anchor="start" style="font-size:14px">top</text><rect class="box-face" x="130.8" y="100.0" width="216.0" height="86.4"><title>הקיר הקרוב</title></rect><text class="legend" x="137.8" y="118.0" text-anchor="start" style="font-size:14px">side0</text><rect class="box-copy" x="130.8" y="13.6" width="216.0" height="86.4"><title>הרצפה (עותק מחזורי)</title></rect><line class="axis-c" x1="130.8" y1="532.0" x2="130.8" y2="13.6" stroke-width="1.5"/><line class="axis-c" x1="346.8" y1="532.0" x2="346.8" y2="13.6" stroke-width="1.5"/><line class="ink-line" x1="30.0" y1="445.6" x2="447.6" y2="445.6" stroke-width="1" stroke-dasharray="4 3"/><line class="ink-line" x1="30.0" y1="100.0" x2="447.6" y2="100.0" stroke-width="1" stroke-dasharray="4 3"/><text class="legend" x="375.6" y="441.6" text-anchor="start" style="font-size:11px">p = 0</text><text class="legend" x="375.6" y="96.0" text-anchor="start" style="font-size:11px">p = 48</text><circle class="ink-dot" cx="51.6" cy="402.4" r="3.5"><title>S דרך הרצפה : x = −11, p = 6</title></circle><text class="legend" x="43.6" y="406.4" text-anchor="end" style="font-size:12px">bottom</text><circle class="ink-dot" cx="87.6" cy="280.0" r="3.5"><title>S דרך הקיר הרחוק : x = −6, p = 23</title></circle><text class="legend" x="79.6" y="284.0" text-anchor="end" style="font-size:12px">sideB</text><circle class="s1-dot" cx="123.6" cy="229.6" r="5"><title>S דרך התקרה : x = −1, p = 30</title></circle><text class="legend" x="115.6" y="233.6" text-anchor="end" style="font-size:12px">top</text><circle class="ink-dot" cx="87.6" cy="179.2" r="3.5"><title>S דרך הקיר הקרוב : x = −6, p = 37</title></circle><text class="legend" x="79.6" y="183.2" text-anchor="end" style="font-size:12px">side0</text><circle class="s2-dot" cx="354.0" cy="402.4" r="5"><title>F דרך הרצפה, k = 0 : x = 31, p = 6</title></circle><text class="legend" x="362.0" y="406.4" text-anchor="start" style="font-size:12px">bottom</text><circle class="ink-dot" cx="354.0" cy="56.8" r="3.5"><title>F דרך הרצפה, k = 1 : x = 31, p = 54</title></circle><text class="legend" x="362.0" y="60.8" text-anchor="start" style="font-size:12px">bottom, k = +1</text><circle class="ink-dot" cx="390.0" cy="352.0" r="3.5"><title>F דרך הקיר הרחוק, k = 0 : x = 36, p = 13</title></circle><text class="legend" x="398.0" y="356.0" text-anchor="start" style="font-size:12px">sideB</text><circle class="ink-dot" cx="426.0" cy="229.6" r="3.5"><title>F דרך התקרה, k = 0 : x = 41, p = 30</title></circle><text class="legend" x="434.0" y="233.6" text-anchor="start" style="font-size:12px">top</text><circle class="ink-dot" cx="390.0" cy="452.8" r="3.5"><title>F דרך הקיר הקרוב, k = -1 : x = 36, p = -1</title></circle><text class="legend" x="398.0" y="456.8" text-anchor="start" style="font-size:12px">side0, k = -1</text><circle class="ink-dot" cx="390.0" cy="107.2" r="3.5"><title>F דרך הקיר הקרוב, k = 0 : x = 36, p = 47</title></circle><text class="legend" x="398.0" y="111.2" text-anchor="start" style="font-size:12px">side0</text><line class="s3-line" x1="130.8" y1="272.8" x2="130.8" y2="186.4" stroke-width="5"/><line class="s3-line" x1="346.8" y1="445.6" x2="346.8" y2="359.2" stroke-width="5"/><line class="box-path" x1="123.6" y1="229.6" x2="354.0" y2="402.4" stroke-width="3"/><circle class="s3-dot" cx="130.8" cy="235.0" r="4"><title>נקודת היציאה : p = 29.25</title></circle><circle class="s3-dot" cx="346.8" cy="397.0" r="4"><title>נקודת הכניסה : p = 6.75</title></circle><text class="legend" x="208.8" y="340.0" text-anchor="middle" style="font-size:17px">d = 40</text><text class="legend" x="130.8" y="548.0" text-anchor="middle" style="font-size:13px">x = 0</text><text class="legend" x="346.8" y="548.0" text-anchor="middle" style="font-size:13px">x = 30</text><text class="legend" x="16.0" y="272.8" text-anchor="middle" style="font-size:15px">p</text></svg>

    <!-- /gen -->

    <!-- gen 7 -->

    <span class="viz-legend"><span><i class="s1"></i>הדמות הנבחרת של S</span><span><i class="s2"></i>הדמות הנבחרת של F</span><span><i class="ink"></i>שאר הדמויות</span><span><i class="s3"></i>צלעות היציאה והכניסה, והנקודות עליהן</span><span><i class="box-path"></i>המסלול הקצר ביותר</span><span><i class="box-copy"></i>עותק מחזורי של הרצועה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **קואורדינטת ההיקף :** על הרצפה \( p = y \), על הקיר הרחוק \( p = b + z \), על
       התקרה \( p = b + h + (b - y) \), ועל הקיר הקרוב \( p = 2b + h + (h - z) \). המחזור הוא
       \( P = 2(b + h) \). כל פאה צדדית היא פס אופקי ברצועה, וצלע של קיר קצה היא קטע
       אנכי : הצלע התחתונה של `end0` היא \( x = 0 \) עם \( 0 \le p \le b \), וכך הלאה.

    2. **ארבע דמויות לכל נקודה :** כשמקפלים את `end0` סביב הצלע \( e \), העכביש נוחת
       ב-\( x = -d_e \), כש-\( d_e \) הוא המרחק שלו מהצלע בתוך הקיר, וב-\( p \) של הנקודה
       הקרובה אליו על הצלע. הזבוב נוחת ב-\( x = a + d_e \). לנקודות של השאלה :

        <!-- gen 8 -->

        | הנקודה | הצלע | המרחק לצלע | ‏\( x \) של הדמות | ‏\( p \) של הדמות | טווח ה-\( p \) של הצלע |
        |---|---|---|---|---|---|
        | ‏S | ‏bottom | ‏11 | ‏−11 | ‏6 | ‏0 עד 12 |
        | ‏S | ‏sideB | ‏6 | ‏−6 | ‏23 | ‏12 עד 24 |
        | ‏S | ‏top | ‏1 | ‏−1 | ‏30 | ‏24 עד 36 |
        | ‏S | ‏side0 | ‏6 | ‏−6 | ‏37 | ‏36 עד 48 |
        | ‏F | ‏bottom | ‏1 | ‏31 | ‏6 | ‏0 עד 12 |
        | ‏F | ‏sideB | ‏6 | ‏36 | ‏13 | ‏12 עד 24 |
        | ‏F | ‏top | ‏11 | ‏41 | ‏30 | ‏24 עד 36 |
        | ‏F | ‏side0 | ‏6 | ‏36 | ‏47 | ‏36 עד 48 |

        <!-- /gen -->

    3. **הקו :** לדמות \( (x_s, p_s) \) של העכביש ולדמות \( (x_f, p_f + kP) \) של הזבוב,
       עם \( k \in \{-1, 0, 1\} \), ההפרשים הם \( \Delta x = x_f - x_s \) ו-\( \Delta p = p_f + kP - p_s \),
       והאורך הוא \( \sqrt{\Delta x^2 + \Delta p^2} \).

    4. **שתי בדיקות :** הקו חוצה את \( x = 0 \) ב-\( p_{\text{exit}} = p_s + \Delta p \cdot d_s / \Delta x \),
       ואת \( x = a \) ב-\( p_{\text{enter}} = p_s + \Delta p \cdot (d_s + a) / \Delta x \).
       הקו חוקי אם \( p_{\text{exit}} \) בתוך טווח ה-\( p \) של צלע העכביש, ו-\( p_{\text{enter}} \)
       בתוך הטווח של צלע הזבוב, מוזז ב-\( kP \). בין \( x = 0 \) ל-\( x = a \) הקו נמצא
       ברצועה, וכל \( p \) שם חוקי. בתוך הקירות המקופלים הקו חוקי כי המלבן קמור ושני
       הקצוות שלו בתוכו.

    5. **המינימום :** מבין 48 הקווים לוקחים את החוקי הקצר ביותר. נקודת היציאה היא
       \( p_{\text{exit}} \) על צלע העכביש, מתורגמת חזרה ל-\( (y, z) \) : על הצלע התחתונה
       \( (p, 0) \), על צלע הקיר הרחוק \( (b, p - b) \), על הצלע העליונה \( (b - (p - b - h), h) \),
       ועל צלע הקיר הקרוב \( (0, h - (p - 2b - h)) \).

    6. **הנקודות של השאלה :** הדמות של \( S \) דרך התקרה היא \( (-1, 30) \), הדמות של
       \( F \) דרך הרצפה היא \( (31, 6) \), ‏\( k = 0 \). ‏\( \Delta x = 32 \), ‏\( \Delta p = -24 \),
       האורך 40. ‏\( p_{\text{exit}} = 30 - 24 \cdot 1 / 32 = 29.25 \), בתוך \( [24, 36] \), ועל
       הצלע העליונה זה \( y = 12 - (29.25 - 24) = 6.75 \) : נקודת היציאה היא \( (0, 6.75, 12) \).
       ‏\( p_{\text{enter}} = 30 - 24 \cdot 31 / 32 = 6.75 \), בתוך \( [0, 12] \).

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="shortest_path" linenums="1" hl_lines="44 45 46 47 48 49 50 51"
        localparam real EPS = 1e-9;   // a line through a corner still counts as inside

        typedef struct {
          int  hinge;     // 0 bottom, 1 sideB, 2 top, 3 side0: the edge the point leaves through
          real gap;      // the distance from the point to that edge, inside the end face
          real p;         // the perimeter coordinate of the foot of the perpendicular on the edge
          real lo, hi;    // the edge itself, as a range of the perimeter coordinate
        } image_t;

        // The image of the point (y, z) of an end face when the face is folded flat on edge e.
        function automatic image_t edge_image(int e, real y, real z, real b, real h);
          image_t img;
          img.hinge = e;
          case (e)
            0:       begin img.gap = z;     img.p = y;                   img.lo = 0.0;     img.hi = b;         end  // (1)!
            1:       begin img.gap = b - y; img.p = b + z;               img.lo = b;       img.hi = b + h;     end
            2:       begin img.gap = h - z; img.p = b + h + (b - y);     img.lo = b + h;   img.hi = 2*b + h;   end
            default: begin img.gap = y;     img.p = 2*b + h + (h - z);   img.lo = 2*b + h; img.hi = 2*(b + h); end
          endcase
          return img;
        endfunction

        // The point (y, z) of an end face at perimeter coordinate p of its edge e.
        function automatic void edge_point(int e, real p, real b, real h, output real y, output real z);
          case (e)
            0:       begin y = p;               z = 0.0;                 end
            1:       begin y = b;               z = p - b;               end
            2:       begin y = b - (p - b - h); z = h;                   end
            default: begin y = 0.0;             z = h - (p - 2*b - h);   end
          endcase
        endfunction

        // The shortest surface distance from the spider (0, y0, z0) to the fly (a, y1, z1).
        // (0, exit_y, exit_z) is the point where the spider leaves its wall.
        function automatic real shortest_path(real a, real b, real h, real y0, real z0, real y1, real z1,
                                              output real exit_y, output real exit_z);
          real period = 2.0 * (b + h);
          real best = -1.0, best_p = 0.0;
          int  best_edge = 0;
          for (int es = 0; es < 4; es++) begin
            image_t s = edge_image(es, y0, z0, b, h);
            for (int ef = 0; ef < 4; ef++) begin
              image_t f = edge_image(ef, y1, z1, b, h);
              for (int k = -1; k <= 1; k++) begin                     // (2)!
                real dx = s.gap + a + f.gap;                        // from x = -s.gap to x = a + f.gap
                real dp = f.p + k * period - s.p;
                real p_exit  = s.p + dp * s.gap / dx;                // where the line crosses x = 0
                real p_enter = s.p + dp * (s.gap + a) / dx;          // where it crosses x = a
                real d;
                if (p_exit < s.lo - EPS || p_exit > s.hi + EPS) continue;                            // (3)!
                if (p_enter < f.lo + k * period - EPS || p_enter > f.hi + k * period + EPS) continue;
                d = $sqrt(dx * dx + dp * dp);
                if (best < 0.0 || d < best) begin                     // (4)!
                  best = d; best_edge = es; best_p = p_exit;
                end
              end
            end
          end
          edge_point(best_edge, best_p, b, h, exit_y, exit_z);
          return best;
        endfunction
        ```

        1. ארבע הצלעות של קיר קצה, בסדר הרצועה : רצפה, קיר רחוק, תקרה, קיר קרוב. לכל אחת
           המרחק של הנקודה ממנה, ה-\( p \) של הנקודה הקרובה ביותר עליה, והטווח של הצלע עצמה.
           אותה פונקציה משמשת לעכביש ולזבוב, כי שני הקירות חופפים.
        2. ‏\( k \) מזיז את דמות הזבוב מחזור אחד למטה, משאיר אותה במקום, או מזיז מחזור אחד
           למעלה. הזזה גדולה יותר היא הקפה שלמה סביב התיבה, ואף פעם לא קצרה יותר.
        3. שתי הבדיקות של שלב 4 : הקו חייב לצאת מהקיר דרך הצלע שקיפלנו סביבה, ולהיכנס לקיר
           של הזבוב דרך הצלע שלו. ‏`continue` מדלג על קו שאינו מסלול אמיתי.
        4. ‏`best < 0.0` מסמן שעוד אין מועמד. תמיד יש לפחות קו חוקי אחד, כי הקו דרך התקרה או
           דרך הרצפה בלי הזזה תמיד חוקי.

    === "Python"
        ```python title="shortest_path" linenums="1" hl_lines="28 29 30 31 32 33 34 35 36"
        from math import hypot

        EPS = 1e-9   # a line through a corner still counts as inside


        def edge_images(y, z, b, h):
            """The four images of a point (y, z) of an end face, one per edge it can leave
            through: (edge, distance to the edge, p of the foot on the edge, p-range of the edge)."""
            return [("bottom", z,     y,                   0,         b),          # (1)!
                    ("sideB",  b - y, b + z,               b,         b + h),
                    ("top",    h - z, b + h + (b - y),     b + h,     2 * b + h),
                    ("side0",  y,     2 * b + h + (h - z), 2 * b + h, 2 * (b + h))]


        def edge_point(edge, p, b, h):
            """The point (y, z) of an end face at perimeter coordinate p of its edge."""
            return {"bottom": (p, 0.0), "sideB": (b, p - b), "top": (b - (p - b - h), h),
                    "side0": (0.0, h - (p - 2 * b - h))}[edge]


        def shortest_path(a, b, h, y0, z0, y1, z1):
            """The shortest surface distance from the spider (0, y0, z0) to the fly (a, y1, z1),
            and the point (0, y, z) where the spider leaves its wall."""
            period = 2 * (b + h)
            best = None
            for s_edge, ds, ps, s_lo, s_hi in edge_images(y0, z0, b, h):
                for f_edge, df, pf, f_lo, f_hi in edge_images(y1, z1, b, h):
                    for k in (-1, 0, 1):                        # the fly one turn down, here, one turn up (2)
                        dx = ds + a + df                        # from x = -ds to x = a + df
                        dp = pf + k * period - ps
                        p_exit = ps + dp * ds / dx              # where the line crosses x = 0
                        p_enter = ps + dp * (ds + a) / dx       # where it crosses x = a
                        if not (s_lo - EPS <= p_exit <= s_hi + EPS):
                            continue                            # leaves the wall through another edge (3)
                        if not (f_lo + k * period - EPS <= p_enter <= f_hi + k * period + EPS):
                            continue                            # enters the fly's wall through another edge
                        d = hypot(dx, dp)
                        if best is None or d < best[0]:         # (4)!
                            best = (d, s_edge, p_exit)
            d, edge, p = best
            y, z = edge_point(edge, p, b, h)
            return d, (0.0, y, z)
        ```

        1. ארבע הצלעות של קיר קצה, בסדר הרצועה : רצפה, קיר רחוק, תקרה, קיר קרוב. לכל אחת
           המרחק של הנקודה ממנה, ה-\( p \) של הנקודה הקרובה ביותר עליה, והטווח של הצלע עצמה.
           אותה פונקציה משמשת לעכביש ולזבוב, כי שני הקירות חופפים.
        2. ‏\( k \) מזיז את דמות הזבוב מחזור אחד למטה, משאיר אותה במקום, או מזיז מחזור אחד
           למעלה. הזזה גדולה יותר היא הקפה שלמה סביב התיבה, ואף פעם לא קצרה יותר.
        3. שתי הבדיקות של שלב 4 : הקו חייב לצאת מהקיר דרך הצלע שקיפלנו סביבה, ולהיכנס לקיר
           של הזבוב דרך הצלע שלו. ‏`continue` מדלג על קו שאינו מסלול אמיתי.
        4. תמיד יש לפחות קו חוקי אחד, כי הקו דרך התקרה או דרך הרצפה בלי הזזה תמיד חוקי,
           ולכן `best` לא נשאר `None`.

    #### למה זה נכון { .sol-proof }

    **כל פריסה היא קו ברצועה.** סדר פאות מ-`end0` ל-`enda` עובר דרך פאות צדדיות
    סמוכות, וברצועה הן פסים סמוכים : או בכיוון \( p \) עולה או בכיוון \( p \) יורד, אולי
    דרך הקפל המחזורי בין \( p = P \) ל-\( p = 0 \). הצלע שדרכה המסלול יוצא מ-`end0` היא
    צלע הקיפול של העכביש, והצלע שדרכה הוא נכנס ל-`enda` היא צלע הקיפול של הזבוב. ההזזה
    \( k \) בוחרת אם הקו מגיע לזבוב בכיוון \( p \) עולה או יורד. לכן כל אחד מ-16 הקווים של
    סעיף א מופיע בין 48 הקווים, ובטבלה של סעיף א הם מופיעים עם אותם ניצבים.

    **קו חוקי הוא מסלול אמיתי.** בתוך הרצועה כל נקודה היא נקודה על פאה צדדית, ולכן קטע
    הקו בין \( x = 0 \) ל-\( x = a \) הוא מסלול על הפאות הצדדיות באותו אורך. הקטע מהדמות
    של העכביש עד \( x = 0 \) נמצא בתוך המלבן של הקיר המקופל, כי שני הקצוות שלו בתוכו : הדמות,
    ונקודת היציאה שנבדקה. אותו דבר בצד הזבוב. קיפול חזרה נותן מסלול באורך הקו.

    **בדיקה מול כוח גס.** הבדיקות של השאלה משוות את הפונקציה, על אלפי תיבות ונקודות
    אקראיות, למימוש שעובר על כל סדרי הפאות ופורס כל אחד בנפרד, כמו הפותר שבממשק. המרחקים
    זהים, וגם נקודת היציאה.

    #### סיבוכיות { .sol-cost }

    ‏\( O(1) \) : ‏48 קווים, ולכל קו שורש אחד ושתי השוואות. אין רקורסיה, אין רשימת פאות ואין
    מטריצות סיבוב. שני המערכים של ארבע הדמויות הם כל הזיכרון.

    **נסו בעצמכם.** גררו את העכביש ואת הזבוב על שני הקירות, או שנו את מידות התיבה, והרצועה
    מצטיירת מחדש : שמונה הדמויות, הקווים החוקיים, הקצר ביותר בכתום ונקודת היציאה על הצלע
    שלה. בבחירה "כל 48" רואים גם את הקווים שנפסלו, כי הם חוצים את \( x = 0 \) או את
    \( x = a \) מחוץ לצלע שלהם. הטבלה שמתחת מפרקת את המסלול לקטעים, פאה אחרי פאה :

    <div class="explorer" data-kind="strip" data-a="30" data-b="12" data-h="12" data-y0="6" data-z0="11" data-y1="6" data-z1="1"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : 42 נראה ברור"
    המסלול מעל התקרה או מתחת לרצפה הוא 42, והוא נראה הכי ישיר. אבל המסלול הקצר ביותר
    עובר דרך חמש פאות ואורכו 40. קפלים לא עולים כלום : רק האורך בפריסה קובע.

??? trap "מלכודת : המרחק במרחב"
    ‏\( \sqrt{30^2 + 10^2} \approx 31.6 \) הוא המרחק דרך האוויר. הוא חסם תחתון לכל מסלול על פני
    התיבה, אבל אי-אפשר ללכת אותו. התשובה חייבת להיות מסלול על הפאות.

??? trap "מלכודת : קו ישר שיוצא מהפאות"
    לא כל קו ישר בפריסה הוא מסלול. אם הקו חוצה את \( x = 0 \) מחוץ לצלע שקיפלנו סביבה,
    הוא "עובר דרך האוויר" ליד פינת הקיר. מי שלא בודק את זה מקבל מרחקים קצרים מדי. בקוד
    אלה שתי הבדיקות שמדלגות על קו.

??? trap "מלכודת : לשכוח את ההזזה המחזורית"
    ברצועה הזבוב מופיע גם מחזור אחד למעלה ולמטה. בלי \( k \) הקוד מפספס חצי מהמסלולים,
    למשל את המסלול של 40 דרך הקיר הקרוב, ובנקודות אחרות גם את המסלול הקצר ביותר.

??? trap "מלכודת : השוואה מדויקת של ממשיים"
    קו שחוצה בדיוק בפינה של צלע, או נקודה שיושבת בדיוק על צלע, נותנים שוויון בין ממשיים.
    בלי \( \varepsilon \) קטן הבדיקה עלולה לפסול מסלול חוקי בגלל שגיאת עיגול.

??? followup "שאלות המשך"
    - **הזבוב זז :** אם הזבוב נמצא באמצע הקיר שלו, ‏\( (30, 6, 6) \), מה המסלול הקצר ביותר?
      ‏(דרך התקרה בלבד : ‏\( \sqrt{37^2 + 0} = 37 \)‏, כי \( 1 + 30 + 6 \).)
    - **קובייה :** בקובייה \( 1 \times 1 \times 1 \), עכביש באמצע פאה אחת וזבוב באמצע הפאה
      שממול. ‏(2, דרך פאה אחת בלבד; כאן המסלול הפשוט הוא הקצר ביותר.)
    - **מתי חמש פאות מנצחות :** עם \( a = 30 \) ו-\( b = h = 12 \), עבור אילו גבהים \( z_0 \)
      של העכביש ו-\( z_1 \) של הזבוב, שניהם באמצע הרוחב, המסלול דרך חמש פאות קצר מהמסלול
      דרך התקרה? הריצו את הקוד על רשת של נקודות.
    - **שתי הנקודות על פאות צדדיות :** הרחיבו את הקוד למקרה שהעכביש והזבוב על פאות
      כלשהן. ‏(הפותר שבממשק עושה את זה בעזרת מעבר על סדרי פאות ופריסה של כל סדר.)
    - **הוכחה שהמסלול ישר בכל פאה :** הראו שמסלול קצר ביותר הוא קו ישר בתוך כל פאה, ושהוא
      לא עובר דרך קודקוד של התיבה.
