---
id: 7
title: משולש אקראי על מעגל היחידה שמכיל את המרכז
level: senior
difficulty: medium
tags: [systemverilog, constraints, randomization, probability, math, python]
source: ""
added: 2026-10-15
---

## השאלה

צריך להגריל **שלוש נקודות על מעגל היחידה**, כך שהמשולש שהן יוצרות **יכיל את מרכז המעגל**
‏\( O = (0, 0) \).

??? interviewer "מה המראיין בודק"
    - **מגאומטריה לתנאי חישובי :** האם מצליחים לתרגם את "המשולש מכיל את המרכז" לתנאי פשוט
      על שלוש הזוויות בלבד, בלי קואורדינטות, כולל המקרה הגבולי שבו המרכז נמצא בדיוק על צלע.
    - **אילוצים ולא לולאת דחייה :** ב-SystemVerilog מתארים את התנאי ל-solver במקום להגריל
      ולבדוק, ויודעים מה `post_randomize()` עושה ולמה משתני `real` לא יכולים להיות `rand`.
    - **בודק עצמאי :** לבדוק את ה-generator בשיטה גאומטרית **אחרת**, ולא באותה נוסחה שבה
      הוא נבנה. זה היחס בין checker ל-generator בסביבת אימות.
    - **מקוד להסתברות :** לחשב את ההסתברות במודל הרציף, ולהבין מה משתנה כשהזוויות בדידות
      ומוגבלות למספרים שלמים.

---

### סעיף א – הגרלת המשולש

כתבו קוד שמחזיר שלוש נקודות כאלה :

- **ב-Python :** פונקציה שמחזירה שלוש נקודות \( (x, y) \).
- **ב-SystemVerilog :** class עם משתנים מסוג `rand` ו-constraints, כך שכל קריאה ל-`randomize()`
  תיתן משולש תקין. הזוויות יהיו מספרים שלמים במעלות, \( 0 \) עד \( 359 \).

??? tip "רמז 1"
    עבדו עם זוויות ולא עם קואורדינטות : נקודה על מעגל היחידה נקבעת על ידי זווית אחת
    \( \theta \), והנקודה עצמה היא \( (\cos\theta, \sin\theta) \).

??? tip "רמז 2"
    מתי המרכז נמצא **מחוץ** למשולש? חשבו על הקשתות שבין הנקודות לאורך המעגל.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ממיינים את שלוש הזוויות ומודדים את שלוש הקשתות שביניהן, כולל הקשת שחוזרת דרך 0°.
        **המרכז בתוך המשולש אם ורק אם כל אחת משלוש הקשתות קטנה מ-180°.** ב-Python מגרילים
        ודוחים עד שהתנאי מתקיים, וב-SystemVerilog התנאי הוא שלושה constraints וקריאה אחת
        ל-`randomize()`.

    #### הרעיון { .sol-idea }

    שלוש הנקודות מחלקות את המעגל לשלוש קשתות שסכומן \( 360° \). אם אחת מהן מגיעה לחצי מעגל,
    שלוש הנקודות יושבות בחצי מעגל אחד והמרכז נשאר בחוץ; אם כולן קטנות מחצי מעגל, המרכז
    בפנים. זה תנאי על הזוויות בלבד, ולכן קל לכתוב אותו גם כבדיקה בלולאה וגם כ-constraint.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מייצגים כל נקודה בזווית :** \( \theta_i \), והנקודה היא \( (\cos\theta_i, \sin\theta_i) \).
       כך "שלוש נקודות על המעגל" הופכות לשלושה מספרים.
    2. **מסדרים את הזוויות בסדר עולה :** ב-Python ממיינים אחרי ההגרלה, וב-SystemVerilog
       דורשים \( a_0 < a_1 < a_2 \) ישירות ב-constraint.
    3. **מחשבים שלוש קשתות :** \( a_1 - a_0 \), \( a_2 - a_1 \), והקשת שעוברת דרך 0°, שאורכה
       \( 360 - (a_2 - a_0) \).
    4. **דורשים שכל קשת קטנה מ-180° :** ב-Python מגרילים מחדש כשהתנאי נכשל, וב-SystemVerilog
       ה-solver מקיים אותו בקריאה אחת.
    5. **ממירים לנקודות ממשיות :** עם \( \cos \) ו-\( \sin \). ב-SystemVerilog זה קורה בתוך
       `post_randomize()`, כי משתני `real` לא יכולים להיות `rand`.
    6. **בודקים באופן עצמאי :** מכפלה וקטורית מול כל צלע, בשיטה שלא תלויה בתנאי הקשתות.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ב-SystemVerilog לא צריך לולאת דחייה : מתארים את התנאי כ-constraints, וה-solver מוצא
        פתרון שמקיים אותם בקריאה אחת ל-`randomize()`.

        ```systemverilog title="class circle_tri" linenums="1" hl_lines="24 25 26"
        class circle_tri;

          localparam int  FULL = 360;          // full circle, 1 degree resolution
          localparam int  HALF = FULL / 2;
          localparam real PI   = 3.14159265358979323846;

          rand int a[3];                       // angles in degrees
          real     x[3];
          real     y[3];

          constraint c_range {
            foreach (a[i]) a[i] inside {[0 : FULL - 1]};   // (1)!
          }

          // Strictly increasing => also guarantees the angles are all different
          constraint c_order {
            a[0] < a[1];
            a[1] < a[2];   // (2)!
          }

          // Differences between neighbouring points (including the wrap-around
          // arc from the last point back to the first) are smaller than half a circle
          constraint c_gaps {
            (a[1] - a[0])          < HALF;
            (a[2] - a[1])          < HALF;
            (FULL - (a[2] - a[0])) < HALF;   // (3)!
          }

          // Compute the real points with $cos / $sin
          function void post_randomize();   // (4)!
            real th;
            foreach (a[i]) begin
              th   = 2.0 * PI * real'(a[i]) / real'(FULL);   // (5)!
              x[i] = $cos(th);
              y[i] = $sin(th);
            end
          endfunction

          // Independent check using cross products: the center (0,0) must be on the
          // same side of all three edges.
          function bit center_inside();
            real s[3];
            int  j;
            for (int i = 0; i < 3; i++) begin
              j    = (i + 1) % 3;
              s[i] = (x[j] - x[i]) * (0.0 - y[i]) - (y[j] - y[i]) * (0.0 - x[i]);
            end
            return (s[0] > 0 && s[1] > 0 && s[2] > 0) ||   // (6)!
                   (s[0] < 0 && s[1] < 0 && s[2] < 0);
          endfunction

          function void print();
            foreach (a[i])
              $display("  P%0d: angle=%3d deg  (x=%8.5f, y=%8.5f)", i, a[i], x[i], y[i]);
            $display("  center inside triangle: %s", center_inside() ? "yes" : "NO");
          endfunction

        endclass
        ```

        1. הטווח נגמר ב-359 ולא ב-360 : הזווית 360° היא אותה נקודה כמו 0°. אם היו מרשים גם
           360, שתי זוויות "שונות" היו נותנות נקודה אחת והמשולש היה מנוון.
        2. אי-שוויון **חזק** ולא `<=`. הסדר העולה חוסך מיון ב-`post_randomize()`, מונע שתי
           נקודות זהות, ומבטל סימטריות : כל משולש מופיע פעם אחת ולא בשש תמורות. בזכות זה
           הספירה בסעיף ד היא בדיוק מספר הפתרונות של ה-solver.
        3. הקשת השלישית חוזרת מהנקודה האחרונה לראשונה **דרך 0°**, ולכן אורכה הוא ההשלמה
           ל-360. בלעדיה הזוויות 10°, 20°, 30° היו עוברות, אף שכולן בקשת של 20°.
        4. ‏`post_randomize()` נקראת אוטומטית אחרי כל `randomize()` **מוצלח**, ולא אחרי
           כישלון. כאן ממירים את הזוויות השלמות לנקודות ממשיות, כי לא ניתן להגריל `real`
           ישירות.
        5. מעלות לרדיאנים : \( 2\pi a_i / 360 \). ההמרות ל-`real` כתובות במפורש כדי שהקורא לא
           יצטרך לזכור את כללי ההרחבה של SystemVerilog לביטויים שמערבבים `int` ו-`real`.
        6. דורשים ששלושת הסימנים **שווים**, לא שהם חיוביים. בגלל `c_order` הנקודות מסודרות
           נגד כיוון השעון והסימן יוצא חיובי, אבל הבדיקה לא מניחה כיוון, ולכן היא נכונה גם
           על משולש שהגיע ממקור אחר.

        שימוש :

        ```systemverilog title="usage"
        circle_tri t = new();
        repeat (5) begin
          if (!t.randomize()) $fatal(1, "randomize() failed");
          t.print();
        end
        ```

        **למה כל חלק נמצא שם.**

        - **‏`c_order` :** מסדר את הזוויות בסדר עולה, ולכן אין צורך למיין. בנוסף זה מבטל
          סימטריות : כל משולש מופיע פעם אחת ולא בשש תמורות, והנקודות תמיד שונות זו מזו.
        - **‏`c_gaps` :** בדיוק התנאי מלמעלה. הקשת השלישית "עוברת דרך 0°", ולכן אורכה
          \( 360 - (a_2 - a_0) \).
        - **‏`post_randomize()` :** נקרא אוטומטית אחרי `randomize()` מוצלח, ומחשב את הנקודות
          הממשיות. משתנים מסוג `real` לא יכולים להיות `rand`, ולכן מגרילים זוויות שלמות
          וממירים אותן.
        - **‏`center_inside()` :** בדיקה **עצמאית**, בשיטה גאומטרית אחרת, שמוודאת שה-constraints
          נכונים. זה בדיוק התפקיד של checker מול generator.

    === "Python"
        מגרילים שלוש זוויות רציפות, ואם התנאי לא מתקיים מגרילים מחדש (rejection sampling).
        בנוסף, פונקציה עצמאית בודקת את התוצאה בעזרת מכפלה וקטורית (ראו "למה זה נכון") :

        ```python title="random_triangle_with_center" linenums="1" hl_lines="7 8"
        import math
        import random


        def contains_center(angles):
            a = sorted(angles)
            gaps = [a[1] - a[0], a[2] - a[1], 2 * math.pi - (a[2] - a[0])]  # (1)!
            return all(g < math.pi for g in gaps)  # (2)!


        def random_triangle_with_center():
            while True:
                angles = [random.uniform(0, 2 * math.pi) for _ in range(3)]
                if contains_center(angles):  # (3)!
                    return [(math.cos(t), math.sin(t)) for t in angles]


        # Independent check using cross products: the center (0, 0) must be on the
        # same side of all three edges.
        def center_inside(points):
            s = []
            for i in range(3):
                (x0, y0), (x1, y1) = points[i], points[(i + 1) % 3]
                s.append((x1 - x0) * (0.0 - y0) - (y1 - y0) * (0.0 - x0))
            return all(v > 0 for v in s) or all(v < 0 for v in s)  # (4)!


        print(random_triangle_with_center())
        ```

        1. הקשת השלישית סוגרת את המעגל מהזווית הגדולה ביותר חזרה לקטנה ביותר, ולכן אורכה הוא
           ההשלמה ל-\( 2\pi \). זו הקשת שקל לשכוח.
        2. אי-שוויון חזק : קשת של בדיוק \( \pi \) פירושה שהצלע שמולה היא קוטר והמרכז נמצא
           **על** הצלע, ולא בתוך המשולש.
        3. לולאת הדחייה : כל ניסיון בלתי תלוי בקודמיו, ולכן המשולשים שמתקבלים מתפלגים בדיוק
           כמו ההתפלגות המותנית "משולש אקראי שמכיל את המרכז".
        4. שלושת הסימנים שווים, בלי להניח כיוון : הפונקציה נכונה גם כשהנקודות לא ממוינות,
           ולכן היא בודק עצמאי אמיתי ל-`random_triangle_with_center`.

        לפי סעיף ג, רק \( \tfrac14 \) מההגרלות עוברות את התנאי, ולכן הלולאה מבצעת **בממוצע
        4 ניסיונות**.

    !!! note "איך נבדק הקוד"
        קוד ה-Python הורץ על 20,000 משולשים, וכולם עברו את בדיקת המכפלה הווקטורית. המחלקה
        ב-SystemVerilog רצה **כמו שהיא כתובה כאן** ב-Verilator עם ה-solver ‏z3, בכל
        עדכון של האתר : 500 קריאות ל-`randomize()`, כולן הצליחו וכולן עברו את
        `center_inside()`. בנוסף נבדק ש-`randomize() with` שמכריח קשת של 230° נכשל, ואחד עם
        שלוש קשתות קטנות מ-180° מצליח. בסימולטור מסחרי (VCS, Xcelium או Questa) הקוד רץ
        באותה צורה.

    #### למה זה נכון { .sol-proof }

    **התנאי : כל הקשתות קטנות מחצי מעגל.** ממיינים את שלוש הזוויות. שלוש הנקודות מחלקות את
    המעגל לשלוש קשתות, והסכום שלהן הוא \( 360° \). **המרכז נמצא בתוך המשולש אם ורק אם כל
    אחת משלוש הקשתות קטנה מ-\( 180° \).**

    - **אם קשת אחת גדולה מ-\( 180° \) :** שלוש הנקודות נמצאות כולן בחצי מעגל אחד, הצלע
      שמול הקשת הגדולה מפרידה בין המרכז לבין המשולש, ולכן המרכז בחוץ.
    - **אם קשת שווה בדיוק ל-\( 180° \) :** הצלע שמולה היא קוטר, והמרכז נמצא **על** הצלע.
      לכן התנאי הוא אי-שוויון חזק.
    - **אם כל הקשתות קטנות מ-\( 180° \) :** אף חצי מעגל לא מכיל את שלוש הנקודות, ולכן אף
      צלע לא מפרידה בין המרכז לקודקוד שמולה, והמרכז בפנים.

    <!-- gen 0 -->

    <svg class="figure" viewBox="0 0 640 330" role="img" aria-label="שתי דוגמאות : משולש שמכיל את מרכז המעגל ומשולש שלא מכיל אותו"><circle class="axis-c" cx="160" cy="150" r="100" fill="none"/><path class="s1-line" d="M265.2,111.7 A112,112 0 0 0 74.2,78.0" fill="none" stroke-width="3"/><text class="legend" x="181.9" y="29.9" text-anchor="middle">120°</text><path class="s1-line" d="M74.2,78.0 A112,112 0 0 0 121.7,255.2" fill="none" stroke-width="3"/><text class="legend" x="38.3" y="186.6" text-anchor="middle">110°</text><path class="s1-line" d="M121.7,255.2 A112,112 0 0 0 265.2,111.7" fill="none" stroke-width="3"/><text class="legend" x="249.1" y="243.1" text-anchor="middle">130°</text><polygon class="tri-ok" points="248.3,117.9 88.0,89.6 127.9,238.3"/><circle class="ink-dot" cx="248.3" cy="117.9" r="5"><title>20°</title></circle><circle class="ink-dot" cx="88.0" cy="89.6" r="5"><title>140°</title></circle><circle class="ink-dot" cx="127.9" cy="238.3" r="5"><title>250°</title></circle><circle class="center-dot" cx="160" cy="150" r="4"/><text class="tick" x="166" y="164">O</text><text class="legend" x="160" y="312" text-anchor="middle" direction="rtl">✓ מכיל את המרכז : כל הפערים קטנים מ-180°</text><circle class="axis-c" cx="480" cy="150" r="100" fill="none"/><path class="s1-line" d="M585.2,111.7 A112,112 0 0 0 518.3,44.8" fill="none" stroke-width="3"/><text class="legend" x="569.1" y="64.9" text-anchor="middle">50°</text><path class="s1-line" d="M518.3,44.8 A112,112 0 0 0 383.0,94.0" fill="none" stroke-width="3"/><text class="legend" x="436.9" y="35.6" text-anchor="middle">80°</text><path class="s2-line" d="M383.0,94.0 A112,112 0 1 0 585.2,111.7" fill="none" stroke-width="5"/><text class="legend" x="469.0" y="279.5" text-anchor="middle">230°</text><polygon class="tri-bad" points="568.3,117.9 512.1,61.7 398.6,103.0"/><circle class="ink-dot" cx="568.3" cy="117.9" r="5"><title>20°</title></circle><circle class="ink-dot" cx="512.1" cy="61.7" r="5"><title>70°</title></circle><circle class="ink-dot" cx="398.6" cy="103.0" r="5"><title>150°</title></circle><circle class="center-dot" cx="480" cy="150" r="4"/><text class="tick" x="486" y="164">O</text><text class="legend" x="480" y="312" text-anchor="middle" direction="rtl">✗ לא מכיל : יש פער של 230° > 180°</text></svg>

    <!-- /gen -->

    **הבדיקה הגאומטרית : מכפלה וקטורית.** עבור צלע מ-\( P_i \) ל-\( P_j \), הסימן של המכפלה
    הווקטורית

    \[
    \begin{aligned}
    s_i &= (P_j - P_i) \times (O - P_i) \\
        &= (x_j - x_i)(0 - y_i) - (y_j - y_i)(0 - x_i)
    \end{aligned}
    \]

    אומר אם \( O \) נמצא משמאל לצלע (חיובי) או מימין לה (שלילי). \( O \) בתוך המשולש אם
    ורק אם הוא באותו צד של **כל** שלוש הצלעות, כלומר שלושת הסימנים שווים. הבדיקה הזו
    עובדת בלי קשר לכיוון שבו הנקודות מסודרות, ולכן היא עצמאית מתנאי הקשתות : אם שתי
    השיטות מסכימות על עשרות אלפי משולשים, סביר שה-constraints נכונים.

    **נסו בעצמכם.** גררו את שלוש הנקודות על המעגל, או הקלידו לכל אחת זווית במעלות. המשולש
    ירוק כשהוא מכיל את המרכז, אדום כשלא, וענבר כשהמרכז נמצא בדיוק על צלע (או כששתי נקודות
    מתלכדות). ליד כל קשת כתוב הגודל שלה, והגדולה מודגשת. הכפתור "הפעלה" עובר בסדר עולה על
    כל 7,711,320 השלשות של זוויות שלמות **שונות** מ-0° עד 359°, ומונה כמה מהן מכילות את
    המרכז, כמה על צלע וכמה לא. בסוף הספירה : 1,911,720 מכילות, 64,440 על צלע ו-5,735,160
    לא, כלומר \( \tfrac{89}{359} \) של סעיף ד. הכפתור "1,000 הגרלות" מצייר היסטוגרמה של
    הקשת הגדולה ביותר במשולשים אקראיים : עמודה ירוקה היא משולש שמכיל (קשת מתחת ל-180°),
    העמודה הראשונה היא ה"שמנים", והעמודה המודגשת 170° עד 180° היא הכמעט מנוונים של
    שאלת הכיסוי. במקלדת : Tab ממקד נקודה, וחיצים מזיזים אותה במעלה אחת (עם Shift בעשר).

    <div class="explorer" data-kind="triangle" data-angles="20,140,250"></div>

    #### סיבוכיות { .sol-cost }

    | | ‏Python | ‏SystemVerilog |
    |-|--------|---------------|
    | עבודה להגרלה אחת | בממוצע 4 ניסיונות, כל אחד \( O(1) \) | קריאה אחת ל-`randomize()` |
    | מי מבטיח את התנאי | לולאת הדחייה | ה-solver, מתוך 1,911,720 פתרונות חוקיים (סעיף ד) |
    | הבדיקה העצמאית | ‏\( O(1) \) : שלוש מכפלות | ‏\( O(1) \) : שלוש מכפלות |

    לולאת הדחייה זולה כאן כי שיעור ההצלחה הוא \( \tfrac14 \). אם התנאי היה נדיר (למשל
    "כל הקשתות בין 119° ל-121°"), הדחייה הייתה מתייקרת מאוד, וה-solver של SystemVerilog היה
    נשאר באותו מחיר. זה היתרון המעשי של constraints.

---

### סעיף ב – הכללה למצולע עם \( n \) קודקודים { data-toc-label="סעיף ב – הכללה למצולע עם n קודקודים" }

עכשיו מגרילים \( n \) נקודות על מעגל היחידה, \( 3 \le n \le 10 \), ומחברים אותן לפי הסדר
על המעגל למצולע. הכלילו את הקוד : \( n \) הוא פרמטר, הזוויות הן מערך באורך \( n \), והמצולע
חייב להכיל את המרכז.

??? tip "רמז 1"
    מה תפקיד הקשתות במשולש? האם משהו בטיעון השתמש בכך שיש בדיוק שלוש?

??? tip "רמז 2"
    הקשת שסוגרת את המעגל, מהנקודה האחרונה חזרה לראשונה דרך 0°, קיימת גם כאן. כמה קשתות יש
    בסך הכול, ומה התנאי על כל אחת?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **אותו תנאי בדיוק :** ממיינים את \( n \) הזוויות, מודדים את \( n \) הקשתות בין נקודות
        סמוכות (כולל הקשת שחוזרת דרך 0°), והמרכז בתוך המצולע אם ורק אם **כל** הקשתות
        קטנות מ-180°. הקוד זהה לקוד של המשולש, עם לולאה על מערך באורך \( n \) במקום שלוש
        שורות.

    #### הרעיון { .sol-idea }

    המצולע מכיל את המרכז אם ורק אם הקודקודים **לא** יושבים כולם בחצי מעגל אחד. חצי מעגל
    שמכיל את כל הקודקודים קיים בדיוק כשיש קשת ריקה של 180° ומעלה בין שני קודקודים סמוכים.
    לכן התנאי הוא על \( n \) הקשתות, ומספרן הוא הדבר היחיד שמשתנה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מייצגים כל קודקוד בזווית** \( \theta_i \), כמו בסעיף א.
    2. **ממיינים** את \( n \) הזוויות בסדר עולה : \( a_0 < a_1 < \dots < a_{n-1} \).
    3. **מודדים \( n \) קשתות :** \( a_{i+1} - a_i \) עבור \( i = 0, \ldots, n-2 \), והקשת
       הסוגרת \( 360 - (a_{n-1} - a_0) \).
    4. **התנאי :** כל הקשתות קטנות מ-180°. ב-SystemVerilog זה `foreach` אחד על הקשתות ועוד
       שורה לקשת הסוגרת; ב-Python זו לולאת דחייה על אותה בדיקה.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ‏`n` אינו `rand` : קובעים אותו לפני `randomize()`, והמערך `a` מקבל את הגודל שלו
        ב-constraint. כל שאר ה-constraints כתובים על `a[i]` ו-`a[i+1]`, ולכן הם נכונים לכל
        \( n \).

        ```systemverilog title="class circle_poly" linenums="1" hl_lines="17 18 19"
        class circle_poly;

          localparam int  FULL = 360;          // full circle, 1 degree resolution
          localparam int  HALF = FULL / 2;
          localparam real PI   = 3.14159265358979323846;

          int      n = 3;                      // vertices: set before randomize() (1)
          rand int a[];                        // angles in degrees, increasing
          real     x[];
          real     y[];

          constraint c_size  { a.size() == n; }   // (2)!
          constraint c_range { foreach (a[i]) a[i] inside {[0 : FULL - 1]}; }
          constraint c_order { foreach (a[i]) if (i > 0) a[i] > a[i - 1]; }   // (3)!

          // Every arc between neighbours, and the one that closes the circle, is
          // shorter than half a circle
          constraint c_gaps {
            foreach (a[i]) if (i > 0) a[i] - a[i - 1] < HALF;
            FULL - (a[n - 1] - a[0]) < HALF;   // (4)!
          }

          function void post_randomize();
            real th;
            x = new[n];
            y = new[n];
            foreach (a[i]) begin
              th   = 2.0 * PI * real'(a[i]) / real'(FULL);
              x[i] = $cos(th);
              y[i] = $sin(th);
            end
          endfunction

          // Independent check: the centre is on the same side of all n edges (5)
          function bit center_inside();
            bit pos = 1, neg = 1;
            real s;
            int  j;
            for (int i = 0; i < n; i++) begin
              j = (i + 1) % n;
              s = (x[j] - x[i]) * (0.0 - y[i]) - (y[j] - y[i]) * (0.0 - x[i]);
              if (s <= 0) pos = 0;
              if (s >= 0) neg = 0;
            end
            return pos || neg;
          endfunction

          function void print();
            foreach (a[i])
              $display("  P%0d: angle=%3d deg  (x=%8.5f, y=%8.5f)", i, a[i], x[i], y[i]);
            $display("  center inside polygon: %s", center_inside() ? "yes" : "NO");
          endfunction

        endclass
        ```

        1. ‏`n` הוא שדה רגיל : `randomize()` לא נוגע בו, והקורא קובע אותו לפני כל קריאה. כך
           אותו אובייקט מגריל משולש, מחומש או מעושר.
        2. גודל של מערך דינמי יכול להופיע ב-constraint, וה-solver מקצה אותו לפני שהוא פותר
           את התאים. בלי השורה הזו המערך היה נשאר ריק.
        3. ‏`foreach` עם תנאי על האינדקס במקום שתי שורות : הסדר העולה מבטיח גם זוויות שונות
           וגם שכל מצולע מופיע פעם אחת.
        4. הקשת הסוגרת היא עדיין שורה נפרדת, כי היא מחברת את התא האחרון לראשון. `a[n - 1]`
           חוקי ב-constraint כי `n` אינו `rand`.
        5. הסימן של \( s \) מספר אם המרכז משמאל לצלע או מימינה. במקום שלושה תנאים, שני
           דגלים : `pos` נשאר דלוק רק אם כל הסימנים חיוביים, `neg` רק אם כולם שליליים. סימן
           0 (המרכז על צלע) מכבה את שניהם.

        שימוש :

        ```systemverilog title="usage, part b"
        circle_poly p = new();
        for (int n = 3; n <= 10; n++) begin
          p.n = n;
          if (!p.randomize()) $fatal(1, "randomize() failed for n = %0d", n);
          p.print();
        end
        ```

    === "Python"
        אותה לולאת דחייה, עם `n` כפרמטר. הבדיקה העצמאית עוברת על \( n \) צלעות :

        ```python title="random_polygon_with_center" linenums="1" hl_lines="4 5"
        def contains_center_poly(angles):
            a = sorted(angles)
            n = len(a)
            gaps = [a[i + 1] - a[i] for i in range(n - 1)]   # (1)!
            gaps.append(2 * math.pi - (a[-1] - a[0]))       # the arc that closes the circle
            return all(g < math.pi for g in gaps)


        def random_polygon_with_center(n):
            while True:
                angles = [random.uniform(0, 2 * math.pi) for _ in range(n)]
                if contains_center_poly(angles):
                    return [(math.cos(t), math.sin(t)) for t in sorted(angles)]   # (2)!


        def center_inside_poly(points):
            s = []
            n = len(points)
            for i in range(n):
                (x0, y0), (x1, y1) = points[i], points[(i + 1) % n]
                s.append((x1 - x0) * (0.0 - y0) - (y1 - y0) * (0.0 - x0))
            return all(v > 0 for v in s) or all(v < 0 for v in s)


        print(random_polygon_with_center(5))
        ```

        1. ‏\( n - 1 \) קשתות בין שכנים ועוד הקשת הסוגרת : בדיוק \( n \) קשתות, כמו \( n \)
           צלעות במצולע.
        2. הנקודות מוחזרות **ממוינות** לפי הזווית, כי המצולע מוגדר לפי הסדר על המעגל.
           בלי המיון, `center_inside_poly` הייתה בודקת מצולע אחר, עם צלעות חוצות.

        לפי סעיף ג, ההסתברות שהגרלה אחת עוברת היא \( 1 - \tfrac{n}{2^{n-1}} \) : \( \tfrac14 \)
        למשולש, \( \tfrac12 \) למרובע, ו-\( \tfrac{247}{256} \approx 0.96 \) לעשר נקודות. ככל
        ש-\( n \) גדל, הלולאה כמעט לא דוחה.

    !!! note "איך נבדק הקוד"
        הפונקציות ב-Python רצו על 20,000 מצולעים לכל \( n \) בין 3 ל-10, וכולם עברו את
        בדיקת הצלעות; על זוויות אקראיות שתי השיטות הסכימו תמיד, גם כשמשווים לקוד המשולש של
        סעיף א עבור \( n = 3 \). המחלקה ב-SystemVerilog רצה **כמו שהיא כתובה כאן** ב-Verilator
        עם ה-solver ‏z3 : 200 קריאות ל-`randomize()` לכל \( n \), כולן הצליחו ועברו את
        `center_inside()`, ומצולע עם קשת של 200° נדחה.

    #### למה זה נכון { .sol-proof }

    **אותה הוכחה, עם \( n \) קשתות.** \( n \) הקודקודים מחלקים את המעגל ל-\( n \) קשתות
    שסכומן 360°. אם קשת אחת היא 180° לפחות, כל הקודקודים יושבים בחצי המעגל המשלים, והצלע
    שמול הקשת מפרידה בין המרכז למצולע (או שהמרכז עליה, בשוויון). אם כל הקשתות קטנות
    מ-180°, אף חצי מעגל לא מכיל את כל הקודקודים : לכל צלע, הקודקודים האחרים נמצאים בצד
    הרחוק שלה, ולכן המרכז באותו צד של כל הצלעות, כלומר בפנים.

    **למה המצולע קמור.** קודקודים על מעגל, מחוברים לפי הסדר, נותנים תמיד מצולע קמור, ולכן
    בדיקת "אותו צד של כל הצלעות" היא בדיקת הכלה תקפה. בלי המיון (קודקודים בסדר שרירותי)
    הצלעות היו חוצות זו את זו והבדיקה הייתה חסרת משמעות; זו הסיבה למיון ב-`c_order`
    וב-`random_polygon_with_center`.

    **נסו בעצמכם.** בחרו \( n \), גררו קודקודים או הקלידו זוויות, או הגרילו מצולע : ירוק
    כשהמרכז בפנים, אדום כשלא, ענבר כשהמרכז על צלע. ליד כל קשת כתוב גודלה והגדולה מודגשת.
    "1,000 הגרלות" סופר כמה מצולעים אקראיים מכילים את המרכז, ליד הנוסחה
    \( 1 - \tfrac{n}{2^{n-1}} \) של סעיף ג. גם כאן Tab ממקד קודקוד וחיצים מזיזים אותו.

    <div class="explorer" data-kind="polygon" data-n="5"></div>

    #### סיבוכיות { .sol-cost }

    | | ‏Python | ‏SystemVerilog |
    |-|--------|---------------|
    | עבודה להגרלה אחת | בממוצע \( 1 / (1 - n / 2^{n-1}) \) ניסיונות, כל אחד \( O(n \log n) \) בגלל המיון | קריאה אחת ל-`randomize()` עם \( 2n \) constraints |
    | הבדיקה העצמאית | ‏\( O(n) \) : \( n \) מכפלות | ‏\( O(n) \) : \( n \) מכפלות |

    ב-\( n = 3 \) הדחייה עולה 4 ניסיונות בממוצע; ב-\( n = 10 \) כמעט אחד. הכיוון ההפוך,
    "מצולע שלא מכיל את המרכז", היה הופך לנדיר ככל ש-\( n \) גדל, ושם היתרון של ה-solver
    היה מורגש.

---

### סעיף ג (בונוס) – מה ההסתברות כשהזוויות רציפות?

מגרילים שלוש זוויות באופן אחיד ובלתי תלוי ב-\( [0, 2\pi) \). מה ההסתברות שהמשולש מכיל
את המרכז?

??? tip "רמז 1"
    חשבו על המאורע המשלים : לפי סעיף א, מתי המרכז **בחוץ**? לפעמים קל יותר לחשב את
    ההסתברות של "לא" מאשר של "כן".

??? tip "רמז 2"
    המרכז בחוץ אם ורק אם שלוש הנקודות נמצאות בחצי מעגל אחד. נסו לתאר את המצב הזה בעזרת
    "הנקודה הראשונה" של חצי המעגל.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ההסתברות היא **\( \tfrac14 \)** : המרכז בחוץ בהסתברות \( 3 \cdot \tfrac14 = \tfrac34 \),
        כי לכל אחת משלוש הנקודות יש סיכוי \( \tfrac14 \) להיות "הראשונה" של חצי מעגל שמכיל
        את שתי האחרות.

    #### הרעיון { .sol-idea }

    סופרים את המאורע המשלים. כששלוש הנקודות בחצי מעגל אחד, בדיוק אחת מהן היא "הראשונה"
    (נגד כיוון השעון) של חצי המעגל הזה, ולכן המאורע "המרכז בחוץ" מתפרק לשלושה מאורעות זרים
    וקלים לחישוב.

    #### למה זה נכון { .sol-proof }

    לפי סעיף א, המרכז **בחוץ** אם ורק אם יש קשת של \( 180° \) לפחות, כלומר שלוש הנקודות
    נמצאות בחצי מעגל אחד. במקרה כזה בדיוק אחת הנקודות היא "הראשונה" בחצי המעגל : שתי
    הנקודות האחרות נמצאות בחצי המעגל שמתחיל בה נגד כיוון השעון.

    <!-- gen 1 -->

    <svg class="figure" viewBox="0 0 360 300" style="max-width:22rem" role="img" aria-label="חצי המעגל שמתחיל בנקודה P1 נגד כיוון השעון"><path class="half-fill" d="M180,140 L86.0,174.2 A100,100 0 0 0 274.0,105.8 Z"/><circle class="axis-c" cx="180" cy="140" r="100" fill="none"/><line class="axis-c" x1="86.0" y1="174.2" x2="274.0" y2="105.8"/><circle class="ink-dot" cx="86.0" cy="174.2" r="5"/><text class="legend" x="67.2" y="185.0" text-anchor="middle">P1</text><circle class="ink-dot" cx="162.6" cy="238.5" r="5"/><text class="legend" x="159.2" y="262.2" text-anchor="middle">P2</text><circle class="ink-dot" cx="266.6" cy="190.0" r="5"/><text class="legend" x="283.9" y="204.0" text-anchor="middle">P3</text><circle class="center-dot" cx="180" cy="140" r="4"/><text class="tick" x="180" y="288" text-anchor="middle" direction="rtl">P2 ו-P3 נפלו בחצי המעגל שמתחיל ב-P1, ולכן המרכז בחוץ</text></svg>

    <!-- /gen -->

    <div class="steps" markdown>

    1. **מגדירים את המאורעות.** \( A_i \) : "שתי הנקודות האחרות נמצאות בחצי המעגל שמתחיל
       ב-\( P_i \) נגד כיוון השעון".
    2. **ההסתברות של כל מאורע.** כל אחת משתי הנקודות האחרות נופלת בחצי המעגל הזה בהסתברות
       \( \tfrac12 \), ובאופן בלתי תלוי. לכן \( \Pr[A_i] = \tfrac12 \cdot \tfrac12 = \tfrac14 \).
    3. **המאורעות זרים.** שתי נקודות לא יכולות להיות שתיהן "הראשונה" : אם \( P_j \) בחצי
       המעגל שמתחיל ב-\( P_i \), אז \( P_i \) לא בחצי המעגל שמתחיל ב-\( P_j \). שוויון מדויק
       של זוויות קורה בהסתברות 0.
    4. **מחברים.** נסמן ב-\( O \in \triangle \) את המאורע "המרכז בתוך המשולש". לכן :

        \[
        \begin{aligned}
        \Pr[O \notin \triangle] &= \Pr[A_1] + \Pr[A_2] + \Pr[A_3] \\
                                &= 3 \cdot \tfrac14 = \tfrac34 \\
        \Pr[O \in \triangle]    &= 1 - \tfrac34 = \tfrac14
        \end{aligned}
        \]

    </div>

    סימולציה של 400,000 הגרלות ב-Python נתנה 0.2501.

    **הכללה :** עבור \( n \) נקודות, ההסתברות שכולן בחצי מעגל אחד היא \( \tfrac{n}{2^{n-1}} \) :
    אותו טיעון בדיוק, עם \( n \) מאורעות זרים שההסתברות של כל אחד היא \( (\tfrac12)^{n-1} \).
    עבור \( n = 3 \) מתקבל \( \tfrac34 \), כמו למעלה.

---

### סעיף ד (בונוס) – ומה אם הזוויות בדידות?

עכשיו הזוויות הן מספרים שלמים, כמו במחלקה של SystemVerilog :

1. **רזולוציה של מעלה :** בוחרים באקראי שלוש זוויות **שונות** מתוך \( 0, 1, \ldots, 359 \),
   וכל שלשה אפשרית באותה הסתברות. מה ההסתברות שהמשולש מכיל את המרכז?
2. **רזולוציה כללית :** אותה שאלה עם \( M \) נקודות במרווחים שווים על המעגל.

??? tip "רמז 1"
    במקום הסתברות, ספרו משולשים : כמה שלשות של נקודות יש בסך הכול, וכמה מהן "רעות"? נסו
    קודם על \( M = 4 \) ו-\( M = 5 \) ביד.

??? tip "רמז 2"
    כמו בסעיף ג, ספרו את המשולשים **הרעים** לפי "הנקודה הראשונה" שלהם. שימו לב למקרה
    שבו \( M \) זוגי : אז יש נקודות שנמצאות בדיוק זו מול זו.

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        ברזולוציה של מעלה ההסתברות היא **\( P(360) = \tfrac{89}{359} \approx 0.2479 \)**. באופן
        כללי \( P(M) = \tfrac{M+1}{4(M-2)} \) כש-\( M \) אי-זוגי ו-\( P(M) = \tfrac{M-4}{4(M-1)} \)
        כש-\( M \) זוגי, ושני המקרים מתכנסים ל-\( \tfrac14 \).

    #### הרעיון { .sol-idea }

    אותה ספירה כמו בסעיף ג, אבל בדידה : מחלקים את מספר המשולשים הטובים ב-\( \binom{M}{3} \).
    משולש רע נספר לפי "הנקודה הראשונה" שלו, ומספר הנקודות שמותר לשתי האחרות לתפוס אחריה הוא
    \( \lfloor M/2 \rfloor \). ההבדל בין \( M \) זוגי לאי-זוגי נובע מהקוטר : כש-\( M \) זוגי יש
    נקודות שנמצאות בדיוק זו מול זו, ומשולש עם קוטר כצלע נחשב רע.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סופרים את כל המשולשים :** \( \binom{M}{3} \). מודדים קשתות ב"צעדים" בין נקודות סמוכות,
       ושלוש הקשתות מסתכמות ל-\( M \) צעדים.
    2. **מגדירים משולש רע :** משולש שיש בו קשת של \( \tfrac{M}{2} \) צעדים לפחות (המרכז בחוץ
       או על צלע). קשת כזו יכולה להיות רק אחת, כי שתיים היו מסתכמות לפחות ב-\( M \) והקשת
       השלישית הייתה 0.
    3. **סופרים את הרעים לפי הנקודה הראשונה :** נסמן ב-\( p \) את הנקודה שאחרי הקשת הגדולה.
       שתי הנקודות האחרות נמצאות בתוך \( \lfloor M/2 \rfloor \) הנקודות שאחרי \( p \), ויש
       \( M \) אפשרויות ל-\( p \). לכן :

        \[
        \begin{aligned}
        \#\text{good} &= \binom{M}{3} - M \binom{\lfloor M/2 \rfloor}{2} \\
        P(M)          &= 1 - \frac{M \binom{\lfloor M/2 \rfloor}{2}}{\binom{M}{3}}
        \end{aligned}
        \]

    4. **מפשטים לפי הזוגיות של \( M \) :**

        \[
        P(M) =
        \begin{cases}
        \dfrac{M+1}{4(M-2)} & M \equiv 1 \pmod 2 \\[2ex]
        \dfrac{M-4}{4(M-1)} & M \equiv 0 \pmod 2
        \end{cases}
        \]

    5. **מציבים \( M = 360 \) :**

        \[
        P(360) = \frac{1{,}911{,}720}{7{,}711{,}320} = \frac{89}{359} \approx 0.24791
        \]

    </div>

    #### למה זה נכון { .sol-proof }

    **הקשר למחלקה של SystemVerilog.** \( 1{,}911{,}720 \) הוא גם **מספר הפתרונות החוקיים**
    של ה-constraints במחלקה, כלומר מספר המשולשים השונים שה-solver יכול להחזיר : `c_order` דואג
    שכל שלשה נספרת פעם אחת, ו-`c_gaps` הוא בדיוק התנאי "אין קשת של 180 צעדים". לפי התקן,
    ה-solver בוחר בהתפלגות אחידה מבין הפתרונות החוקיים, ולכן כל אחד מהמשולשים האלה מתקבל
    באותה הסתברות.

    **איך \( P(M) \) מתכנס ל-\( \tfrac14 \).** שתי הסדרות, הזוגית והאי-זוגית, מתקרבות
    ל-\( \tfrac14 \) משני הצדדים :

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="s1"></i>M אי-זוגי</span><span><i class="s2"></i>M זוגי</span></span>

    <!-- /gen -->

    <!-- gen 3 -->

    <svg class="perf-chart" viewBox="0 0 640 300" role="img" aria-label="ההסתברות שהמשולש מכיל את המרכז כפונקציה של M"><line class="grid" x1="48" x2="600" y1="260.0" y2="260.0"/><text class="tick" x="40" y="264.0" text-anchor="end">0.0</text><line class="grid" x1="48" x2="600" y1="211.2" y2="211.2"/><text class="tick" x="40" y="215.2" text-anchor="end">0.1</text><line class="grid" x1="48" x2="600" y1="162.4" y2="162.4"/><text class="tick" x="40" y="166.4" text-anchor="end">0.2</text><line class="grid" x1="48" x2="600" y1="113.6" y2="113.6"/><text class="tick" x="40" y="117.6" text-anchor="end">0.3</text><line class="grid" x1="48" x2="600" y1="64.8" y2="64.8"/><text class="tick" x="40" y="68.8" text-anchor="end">0.4</text><line class="grid" x1="48" x2="600" y1="16.0" y2="16.0"/><text class="tick" x="40" y="20.0" text-anchor="end">0.5</text><line class="axis" x1="48" x2="600" y1="138.0" y2="138.0" stroke-width="1" stroke-dasharray="none"/><text class="legend" x="54" y="132.0">¼</text><text class="tick" x="48.0" y="278" text-anchor="middle">M = 4</text><text class="tick" x="109.3" y="278" text-anchor="middle">M = 8</text><text class="tick" x="170.7" y="278" text-anchor="middle">M = 12</text><text class="tick" x="232.0" y="278" text-anchor="middle">M = 16</text><text class="tick" x="293.3" y="278" text-anchor="middle">M = 20</text><text class="tick" x="354.7" y="278" text-anchor="middle">M = 24</text><text class="tick" x="416.0" y="278" text-anchor="middle">M = 28</text><text class="tick" x="477.3" y="278" text-anchor="middle">M = 32</text><text class="tick" x="538.7" y="278" text-anchor="middle">M = 36</text><text class="tick" x="600.0" y="278" text-anchor="middle">M = 40</text><polyline class="s1-line" points="63.3,16.0 94.0,64.8 124.7,85.7 155.3,97.3 186.0,104.7 216.7,109.8 247.3,113.6 278.0,116.5 308.7,118.7 339.3,120.6 370.0,122.1 400.7,123.4 431.3,124.4 462.0,125.4 492.7,126.2 523.3,126.9 554.0,127.5 584.7,128.1" fill="none" stroke-width="2"/><circle class="s1-dot" cx="63.3" cy="16.0" r="4"><title>M = 5: P = 0.5000</title></circle><circle class="s1-dot" cx="94.0" cy="64.8" r="4"><title>M = 7: P = 0.4000</title></circle><circle class="s1-dot" cx="124.7" cy="85.7" r="4"><title>M = 9: P = 0.3571</title></circle><circle class="s1-dot" cx="155.3" cy="97.3" r="4"><title>M = 11: P = 0.3333</title></circle><circle class="s1-dot" cx="186.0" cy="104.7" r="4"><title>M = 13: P = 0.3182</title></circle><circle class="s1-dot" cx="216.7" cy="109.8" r="4"><title>M = 15: P = 0.3077</title></circle><circle class="s1-dot" cx="247.3" cy="113.6" r="4"><title>M = 17: P = 0.3000</title></circle><circle class="s1-dot" cx="278.0" cy="116.5" r="4"><title>M = 19: P = 0.2941</title></circle><circle class="s1-dot" cx="308.7" cy="118.7" r="4"><title>M = 21: P = 0.2895</title></circle><circle class="s1-dot" cx="339.3" cy="120.6" r="4"><title>M = 23: P = 0.2857</title></circle><circle class="s1-dot" cx="370.0" cy="122.1" r="4"><title>M = 25: P = 0.2826</title></circle><circle class="s1-dot" cx="400.7" cy="123.4" r="4"><title>M = 27: P = 0.2800</title></circle><circle class="s1-dot" cx="431.3" cy="124.4" r="4"><title>M = 29: P = 0.2778</title></circle><circle class="s1-dot" cx="462.0" cy="125.4" r="4"><title>M = 31: P = 0.2759</title></circle><circle class="s1-dot" cx="492.7" cy="126.2" r="4"><title>M = 33: P = 0.2742</title></circle><circle class="s1-dot" cx="523.3" cy="126.9" r="4"><title>M = 35: P = 0.2727</title></circle><circle class="s1-dot" cx="554.0" cy="127.5" r="4"><title>M = 37: P = 0.2714</title></circle><circle class="s1-dot" cx="584.7" cy="128.1" r="4"><title>M = 39: P = 0.2703</title></circle><polyline class="s2-line" points="48.0,260.0 78.7,211.2 109.3,190.3 140.0,178.7 170.7,171.3 201.3,166.2 232.0,162.4 262.7,159.5 293.3,157.3 324.0,155.4 354.7,153.9 385.3,152.6 416.0,151.6 446.7,150.6 477.3,149.8 508.0,149.1 538.7,148.5 569.3,147.9 600.0,147.4" fill="none" stroke-width="2"/><circle class="s2-dot" cx="48.0" cy="260.0" r="4"><title>M = 4: P = 0.0000</title></circle><circle class="s2-dot" cx="78.7" cy="211.2" r="4"><title>M = 6: P = 0.1000</title></circle><circle class="s2-dot" cx="109.3" cy="190.3" r="4"><title>M = 8: P = 0.1429</title></circle><circle class="s2-dot" cx="140.0" cy="178.7" r="4"><title>M = 10: P = 0.1667</title></circle><circle class="s2-dot" cx="170.7" cy="171.3" r="4"><title>M = 12: P = 0.1818</title></circle><circle class="s2-dot" cx="201.3" cy="166.2" r="4"><title>M = 14: P = 0.1923</title></circle><circle class="s2-dot" cx="232.0" cy="162.4" r="4"><title>M = 16: P = 0.2000</title></circle><circle class="s2-dot" cx="262.7" cy="159.5" r="4"><title>M = 18: P = 0.2059</title></circle><circle class="s2-dot" cx="293.3" cy="157.3" r="4"><title>M = 20: P = 0.2105</title></circle><circle class="s2-dot" cx="324.0" cy="155.4" r="4"><title>M = 22: P = 0.2143</title></circle><circle class="s2-dot" cx="354.7" cy="153.9" r="4"><title>M = 24: P = 0.2174</title></circle><circle class="s2-dot" cx="385.3" cy="152.6" r="4"><title>M = 26: P = 0.2200</title></circle><circle class="s2-dot" cx="416.0" cy="151.6" r="4"><title>M = 28: P = 0.2222</title></circle><circle class="s2-dot" cx="446.7" cy="150.6" r="4"><title>M = 30: P = 0.2241</title></circle><circle class="s2-dot" cx="477.3" cy="149.8" r="4"><title>M = 32: P = 0.2258</title></circle><circle class="s2-dot" cx="508.0" cy="149.1" r="4"><title>M = 34: P = 0.2273</title></circle><circle class="s2-dot" cx="538.7" cy="148.5" r="4"><title>M = 36: P = 0.2286</title></circle><circle class="s2-dot" cx="569.3" cy="147.9" r="4"><title>M = 38: P = 0.2297</title></circle><circle class="s2-dot" cx="600.0" cy="147.4" r="4"><title>M = 40: P = 0.2308</title></circle></svg>

    <!-- /gen -->

    | ‏\( M \) | משולשים טובים | כל המשולשים | ‏\( P(M) \) |
    |:-:|:-:|:-:|:-:|
    | 3 | 1 | 1 | 1 |
    | 4 | 0 | 4 | 0 |
    | 5 | 5 | 10 | 0.5 |
    | 6 | 2 | 20 | 0.1 |
    | 12 | 40 | 220 | 0.1818 |
    | 13 | 91 | 286 | 0.3182 |
    | 360 | 1,911,720 | 7,711,320 | 0.24791 |
    | 361 | 1,960,230 | 7,775,940 | 0.25209 |
    | ‏\( \infty \) | | | ‏\( \tfrac14 \) |

    - **כש-\( M \) זוגי :** ההסתברות **קטנה** מ-\( \tfrac14 \). יש נקודות שנמצאות בדיוק זו מול
      זו, וכל משולש שיש לו קוטר כצלע נחשב "רע", כי המרכז נמצא על הצלע. המקרה הקיצוני
      הוא \( M = 4 \) : כל שלושה קודקודים של ריבוע יוצרים משולש ישר-זווית, והמרכז נמצא על
      היתר.
    - **כש-\( M \) אי-זוגי :** ההסתברות **גדולה** מ-\( \tfrac14 \). המקרה הקיצוני הוא
      \( M = 3 \) : יש משולש אחד בלבד, משולש שווה-צלעות, והוא מכיל את המרכז.
    - **כש-\( M \to \infty \) :** שני המקרים מתכנסים לתשובה הרציפה \( \tfrac14 \).

    **בדיקה :** עבור כל \( M \) מ-3 עד 40 ספרנו ישירות את השלשות שכל הקשתות שלהן קצרות מחצי
    מעגל, והמספר שווה לנוסחה \( \binom{M}{3} - M \binom{\lfloor M/2 \rfloor}{2} \).

    !!! note "ואם מגרילים כל זווית בנפרד?"
        אם מגרילים שלוש זוויות **בלתי תלויות** מתוך \( 0..359 \), ייתכן ששתיים מהן יצאו זהות,
        ואז המשולש מנוון. במקרה הזה ההסתברות היא
        \( \frac{6 \cdot \#\text{good}}{M^3} \approx 0.24585 \) עבור \( M = 360 \) : כל משולש טוב
        מתקבל ב-6 סדרים שונים מתוך \( M^3 \) הגרלות.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לשכוח את הקשת שעוברת דרך 0°"
    אחרי המיון קל לבדוק רק את שני ההפרשים \( a_1 - a_0 \) ו-\( a_2 - a_1 \). הקשת השלישית,
    מהנקודה האחרונה חזרה לראשונה דרך 0°, היא \( 360 - (a_2 - a_0) \), ובלעדיה הזוויות
    10°, 20°, 30° "עוברות" אף שכל המשולש יושב בקשת של 20°. זו הסיבה שב-`c_gaps` יש שלוש
    שורות ולא שתיים.

??? trap "מלכודת : קוטר נחשב בפנים"
    כתיבה של `<= 180` במקום `< 180` מכניסה משולשים שבהם צלע אחת היא קוטר והמרכז נמצא **על**
    הצלע, לא בתוכה. ברציף זה מאורע בהסתברות 0, אבל בבדיד, שבו המחלקה עובדת, יש
    \( 180 \cdot 358 \) שלשות כאלה, והבדיקה העצמאית `center_inside()` הייתה נכשלת עליהן.

??? trap "מלכודת : להגריל קואורדינטות במקום זוויות"
    ב-SystemVerilog משתני `real` לא יכולים להיות `rand`, ולכן אי אפשר להגריל \( (x, y) \)
    ישירות. גם אם היה אפשר, הגרלה אחידה של \( x \) ואחר כך חישוב \( y \) לא נותנת פיזור
    אחיד על המעגל. הגרלת זווית שלמה והמרה ב-`post_randomize()` פותרת את שתי הבעיות.

??? followup "שאלות המשך"
    - **ההסתברות הבדידה למצולע :** בסעיף ד נספרו המשולשים. כמה מבין \( \binom{360}{n} \)
      המצולעים עם קודקודים במעלות שלמות מכילים את המרכז? (רמז : אותה ספירה של "הקבוצות
      הרעות" לפי הקודקוד הראשון של חצי המעגל, עם \( \binom{180}{n-1} \) במקום \( \binom{180}{2} \);
      תיבת המצולע מראה את השבר המדויק.)
    - **התפלגות ב-SystemVerilog :** איך מוסיפים constraint שגורם למשולשים "שמנים", שבהם
      כל הקשתות קרובות ל-\( 120° \), להופיע יותר? למשל בעזרת `dist` על אורך הקשתות.
    - **כיסוי (coverage) :** איזה covergroup הייתם כותבים כדי לוודא שהגרלתם גם משולשים עם
      קשת של \( 179° \), כלומר כמעט מנוונים?
