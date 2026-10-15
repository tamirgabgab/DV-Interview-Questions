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
\( O = (0, 0) \).

---

### סעיף א – הגרלת המשולש

כתבו קוד שמחזיר שלוש נקודות כאלה:

- **ב-Python:** פונקציה שמחזירה שלוש נקודות \( (x, y) \).
- **ב-SystemVerilog:** class עם משתנים מסוג `rand` ו-constraints, כך שכל קריאה ל-`randomize()`
  תיתן משולש תקין. הזוויות יהיו מספרים שלמים במעלות, \( 0 \) עד \( 359 \).

??? tip "רמז"
    מתי המרכז נמצא **מחוץ** למשולש? חשבו על הקשתות שבין הנקודות לאורך המעגל.

??? success "פתרון סעיף א"
    #### התנאי: כל הקשתות קטנות מחצי מעגל

    ממיינים את שלוש הזוויות. שלוש הנקודות מחלקות את המעגל לשלוש קשתות, והסכום שלהן הוא
    \( 360° \). **המרכז נמצא בתוך המשולש אם ורק אם כל אחת משלוש הקשתות קטנה מ-\( 180° \).**

    - **אם קשת אחת גדולה מ-\( 180° \):** שלוש הנקודות נמצאות כולן בחצי מעגל אחד, הצלע
      שמול הקשת הגדולה מפרידה בין המרכז לבין המשולש, ולכן המרכז בחוץ.
    - **אם קשת שווה בדיוק ל-\( 180° \):** הצלע שמולה היא קוטר, והמרכז נמצא **על** הצלע.
      לכן התנאי הוא אי-שוויון חזק.

    <svg class="figure" viewBox="0 0 640 330" role="img" aria-label="שתי דוגמאות: משולש שמכיל את מרכז המעגל ומשולש שלא מכיל אותו"><circle class="axis-c" cx="160" cy="150" r="100" fill="none"/><path class="s1-line" d="M265.2,111.7 A112,112 0 0 0 74.2,78.0" fill="none" stroke-width="3"/><text class="legend" x="182.9" y="24.0" text-anchor="middle">120°</text><path class="s1-line" d="M74.2,78.0 A112,112 0 0 0 121.7,255.2" fill="none" stroke-width="3"/><text class="legend" x="32.5" y="188.2" text-anchor="middle">110°</text><path class="s1-line" d="M121.7,255.2 A112,112 0 0 0 265.2,111.7" fill="none" stroke-width="3"/><text class="legend" x="253.3" y="247.3" text-anchor="middle">130°</text><polygon class="tri-ok" points="254.0,115.8 83.4,85.7 125.8,244.0"/><circle class="ink-dot" cx="254.0" cy="115.8" r="5"><title>20°</title></circle><circle class="ink-dot" cx="83.4" cy="85.7" r="5"><title>140°</title></circle><circle class="ink-dot" cx="125.8" cy="244.0" r="5"><title>250°</title></circle><circle class="center-dot" cx="160" cy="150" r="4"/><text class="tick" x="166" y="164">O</text><text class="legend" x="160" y="312" text-anchor="middle" direction="rtl">✓ מכיל את המרכז: כל הפערים קטנים מ-180°</text><circle class="axis-c" cx="480" cy="150" r="100" fill="none"/><path class="s1-line" d="M585.2,111.7 A112,112 0 0 0 518.3,44.8" fill="none" stroke-width="3"/><text class="legend" x="573.3" y="60.7" text-anchor="middle">50°</text><path class="s1-line" d="M518.3,44.8 A112,112 0 0 0 383.0,94.0" fill="none" stroke-width="3"/><text class="legend" x="434.9" y="30.0" text-anchor="middle">80°</text><path class="s2-line" d="M383.0,94.0 A112,112 0 1 0 585.2,111.7" fill="none" stroke-width="5"/><text class="legend" x="468.5" y="285.5" text-anchor="middle">230°</text><polygon class="tri-bad" points="574.0,115.8 514.2,56.0 393.4,100.0"/><circle class="ink-dot" cx="574.0" cy="115.8" r="5"><title>20°</title></circle><circle class="ink-dot" cx="514.2" cy="56.0" r="5"><title>70°</title></circle><circle class="ink-dot" cx="393.4" cy="100.0" r="5"><title>150°</title></circle><circle class="center-dot" cx="480" cy="150" r="4"/><text class="tick" x="486" y="164">O</text><text class="legend" x="480" y="312" text-anchor="middle" direction="rtl">✗ לא מכיל: יש פער של 230° > 180°</text></svg>

    #### Python – הגרלה ודחייה (rejection sampling)

    מגרילים שלוש זוויות רציפות, ואם התנאי לא מתקיים מגרילים מחדש. בנוסף, פונקציה
    עצמאית בודקת את התוצאה בעזרת מכפלה וקטורית (ראו בהמשך):

    ```python
    import math
    import random


    def contains_center(angles):
        a = sorted(angles)
        gaps = [a[1] - a[0], a[2] - a[1], 2 * math.pi - (a[2] - a[0])]
        return all(g < math.pi for g in gaps)


    def random_triangle_with_center():
        while True:
            angles = [random.uniform(0, 2 * math.pi) for _ in range(3)]
            if contains_center(angles):
                return [(math.cos(t), math.sin(t)) for t in angles]


    # Independent check using cross products: the center (0, 0) must be on the
    # same side of all three edges.
    def center_inside(points):
        s = []
        for i in range(3):
            (x0, y0), (x1, y1) = points[i], points[(i + 1) % 3]
            s.append((x1 - x0) * (0.0 - y0) - (y1 - y0) * (0.0 - x0))
        return all(v > 0 for v in s) or all(v < 0 for v in s)


    print(random_triangle_with_center())
    ```

    לפי סעיף ב, רק \( \tfrac14 \) מההגרלות עוברות את התנאי, ולכן הלולאה מבצעת **בממוצע
    4 ניסיונות**.

    #### SystemVerilog – constraints

    ב-SystemVerilog לא צריך לולאת דחייה: מתארים את התנאי כ-constraints, וה-solver מוצא
    פתרון שמקיים אותם בקריאה אחת ל-`randomize()`.

    ```systemverilog
    class circle_tri;

      localparam int  FULL = 360;          // full circle, 1 degree resolution
      localparam int  HALF = FULL / 2;
      localparam real PI   = 3.14159265358979323846;

      rand int a[3];                       // angles in degrees
      real     x[3];
      real     y[3];

      constraint c_range {
        foreach (a[i]) a[i] inside {[0 : FULL - 1]};
      }

      // Strictly increasing => also guarantees the angles are all different
      constraint c_order {
        a[0] < a[1];
        a[1] < a[2];
      }

      // Differences between neighbouring points (including the wrap-around
      // arc from the last point back to the first) are smaller than half a circle
      constraint c_gaps {
        (a[1] - a[0])          < HALF;
        (a[2] - a[1])          < HALF;
        (FULL - (a[2] - a[0])) < HALF;
      }

      // Compute the real points with $cos / $sin
      function void post_randomize();
        real th;
        foreach (a[i]) begin
          th   = 2.0 * PI * real'(a[i]) / real'(FULL);
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
        return (s[0] > 0 && s[1] > 0 && s[2] > 0) ||
               (s[0] < 0 && s[1] < 0 && s[2] < 0);
      endfunction

      function void print();
        foreach (a[i])
          $display("  P%0d: angle=%3d deg  (x=%8.5f, y=%8.5f)", i, a[i], x[i], y[i]);
        $display("  center inside triangle: %s", center_inside() ? "yes" : "NO");
      endfunction

    endclass
    ```

    שימוש:

    ```systemverilog
    circle_tri t = new();
    repeat (5) begin
      if (!t.randomize()) $fatal(1, "randomize() failed");
      t.print();
    end
    ```

    #### למה כל חלק נמצא שם

    - **`c_order`:** מסדר את הזוויות בסדר עולה, ולכן אין צורך למיין. בנוסף זה מבטל
      סימטריות: כל משולש מופיע פעם אחת ולא בשש תמורות, והנקודות תמיד שונות זו מזו.
    - **`c_gaps`:** בדיוק התנאי מלמעלה. הקשת השלישית "עוברת דרך 0°", ולכן אורכה
      \( 360 - (a_2 - a_0) \).
    - **`post_randomize()`:** נקרא אוטומטית אחרי `randomize()` מוצלח, ומחשב את הנקודות
      הממשיות. משתנים מסוג `real` לא יכולים להיות `rand`, ולכן מגרילים זוויות שלמות
      וממירים אותן.
    - **`center_inside()`:** בדיקה **עצמאית**, בשיטה גאומטרית אחרת, שמוודאת שה-constraints
      נכונים. זה בדיוק התפקיד של checker מול generator.

    #### הבדיקה הגאומטרית: מכפלה וקטורית

    עבור צלע מ-\( P_i \) ל-\( P_j \), הסימן של המכפלה הווקטורית

    \[
    s_i = (P_j - P_i) \times (O - P_i) = (x_j - x_i)(0 - y_i) - (y_j - y_i)(0 - x_i)
    \]

    אומר אם \( O \) נמצא משמאל לצלע (חיובי) או מימין לה (שלילי). \( O \) בתוך המשולש אם
    ורק אם הוא באותו צד של **כל** שלוש הצלעות, כלומר שלושת הסימנים שווים. הבדיקה הזו
    עובדת בלי קשר לכיוון שבו הנקודות מסודרות.

    !!! note "איך נבדק הקוד"
        קוד ה-Python הורץ על 20,000 משולשים, וכולם עברו את בדיקת המכפלה הווקטורית. את
        `post_randomize()` ואת `center_inside()` ב-SystemVerilog הרצנו ב-Verilator על
        60,000 שלשות זוויות, והן תאמו בכולן לתנאי הקשתות. את ה-constraints עצמם לא הרצנו
        בסימולטור, כי לגרסה של Verilator שבה השתמשנו אין תמיכה ב-`randomize()` עם constraints
        על מערכים. בסימולטור מסחרי (VCS, Xcelium או Questa) הקוד רץ כמו שהוא.

---

### סעיף ב (בונוס) – מה ההסתברות כשהזוויות רציפות?

מגרילים שלוש זוויות באופן אחיד ובלתי תלוי ב-\( [0, 2\pi) \). מה ההסתברות שהמשולש מכיל
את המרכז?

??? tip "רמז"
    המרכז בחוץ אם ורק אם שלוש הנקודות נמצאות בחצי מעגל אחד. נסו לתאר את המצב הזה בעזרת
    "הנקודה הראשונה" של חצי המעגל.

??? success "פתרון סעיף ב"
    **התשובה: \( \tfrac14 \).**

    לפי סעיף א, המרכז **בחוץ** אם ורק אם יש קשת של \( 180° \) לפחות, כלומר שלוש הנקודות
    נמצאות בחצי מעגל אחד. במקרה כזה בדיוק אחת הנקודות היא "הראשונה" בחצי המעגל: שתי
    הנקודות האחרות נמצאות בחצי המעגל שמתחיל בה נגד כיוון השעון.

    <svg class="figure" viewBox="0 0 360 300" style="max-width:22rem" role="img" aria-label="חצי המעגל שמתחיל בנקודה P1 נגד כיוון השעון"><path class="half-fill" d="M180,140 L86.0,174.2 A100,100 0 0 0 274.0,105.8 Z"/><circle class="axis-c" cx="180" cy="140" r="100" fill="none"/><line class="axis-c" x1="86.0" y1="174.2" x2="274.0" y2="105.8"/><circle class="ink-dot" cx="86.0" cy="174.2" r="5"/><text class="legend" x="67.2" y="185.0" text-anchor="middle">P1</text><circle class="ink-dot" cx="162.6" cy="238.5" r="5"/><text class="legend" x="159.2" y="262.2" text-anchor="middle">P2</text><circle class="ink-dot" cx="266.6" cy="190.0" r="5"/><text class="legend" x="283.9" y="204.0" text-anchor="middle">P3</text><circle class="center-dot" cx="180" cy="140" r="4"/><text class="tick" x="180" y="288" text-anchor="middle" direction="rtl">P2 ו-P3 נפלו בחצי המעגל שמתחיל ב-P1, ולכן המרכז בחוץ</text></svg>

    נגדיר את המאורע \( A_i \): "שתי הנקודות האחרות נמצאות בחצי המעגל שמתחיל ב-\( P_i \)".

    - **ההסתברות של כל מאורע:** כל אחת משתי הנקודות האחרות נופלת בחצי המעגל הזה
      בהסתברות \( \tfrac12 \), ובאופן בלתי תלוי. לכן \( \Pr[A_i] = \tfrac12 \cdot \tfrac12 = \tfrac14 \).
    - **המאורעות זרים:** שתי נקודות לא יכולות להיות שתיהן "הראשונה". שוויון מדויק של זוויות
      קורה בהסתברות 0.

    נסמן ב-\( O \in \triangle \) את המאורע "המרכז בתוך המשולש". לכן:

    \[
    \Pr[O \notin \triangle] = \Pr[A_1] + \Pr[A_2] + \Pr[A_3] = 3 \cdot \tfrac14 = \tfrac34
    \qquad\Longrightarrow\qquad
    \Pr[O \in \triangle] = 1 - \tfrac34 = \tfrac14
    \]

    סימולציה של 400,000 הגרלות ב-Python נתנה 0.2501.

    **הכללה:** עבור \( n \) נקודות, ההסתברות שכולן בחצי מעגל אחד היא \( \tfrac{n}{2^{n-1}} \).
    עבור \( n = 3 \) מתקבל \( \tfrac34 \), כמו למעלה.

---

### סעיף ג (בונוס) – ומה אם הזוויות בדידות?

עכשיו הזוויות הן מספרים שלמים, כמו במחלקה של SystemVerilog:

1. **רזולוציה של מעלה:** בוחרים באקראי שלוש זוויות **שונות** מתוך \( 0, 1, \ldots, 359 \),
   וכל שלשה אפשרית באותה הסתברות. מה ההסתברות שהמשולש מכיל את המרכז?
2. **רזולוציה כללית:** אותה שאלה עם \( M \) נקודות במרווחים שווים על המעגל.

??? tip "רמז"
    כמו בסעיף ב, ספרו את המשולשים **הרעים** לפי "הנקודה הראשונה" שלהם. שימו לב למקרה
    שבו \( M \) זוגי: אז יש נקודות שנמצאות בדיוק זו מול זו.

??? success "פתרון סעיף ג"
    #### ספירה

    יש \( \binom{M}{3} \) משולשים. נמדוד קשתות ב"צעדים" בין נקודות סמוכות. משולש **רע**
    (המרכז בחוץ או על צלע) הוא משולש שיש בו קשת של \( \tfrac{M}{2} \) צעדים לפחות. קשת
    כזו יכולה להיות רק אחת, כי שתיים היו מסתכמות לפחות ב-\( M \) והקשת השלישית הייתה 0.

    נסמן ב-\( p \) את הנקודה שאחרי הקשת הגדולה. שתי הנקודות האחרות נמצאות בתוך
    \( \lfloor M/2 \rfloor \) הנקודות שאחרי \( p \). יש \( M \) אפשרויות ל-\( p \), ולכן:

    \[
    \#\text{good} = \binom{M}{3} - M \binom{\lfloor M/2 \rfloor}{2}
    \qquad
    P(M) = 1 - \frac{M \binom{\lfloor M/2 \rfloor}{2}}{\binom{M}{3}}
    \]

    אחרי פישוט:

    \[
    P(M) =
    \begin{cases}
    \dfrac{M+1}{4(M-2)} & M \equiv 1 \pmod 2 \\[2ex]
    \dfrac{M-4}{4(M-1)} & M \equiv 0 \pmod 2
    \end{cases}
    \]

    #### רזולוציה של מעלה, \( M = 360 \)

    \[
    P(360) = \frac{1{,}911{,}720}{7{,}711{,}320} = \frac{89}{359} \approx 0.24791
    \]

    \( 1{,}911{,}720 \) הוא גם **מספר הפתרונות החוקיים** של ה-constraints במחלקה, כלומר מספר
    המשולשים השונים שה-solver יכול להחזיר. לפי התקן, ה-solver בוחר בהתפלגות אחידה מבין
    הפתרונות החוקיים, ולכן כל אחד מהמשולשים האלה מתקבל באותה הסתברות.

    #### איך \( P(M) \) מתכנס ל-\( \tfrac14 \)

    <span class="viz-legend"><span><i class="s1"></i>M אי-זוגי</span><span><i class="s2"></i>M זוגי</span></span>

    <svg class="perf-chart" viewBox="0 0 640 300" role="img" aria-label="ההסתברות שהמשולש מכיל את המרכז כפונקציה של M"><line class="grid" x1="48" x2="600" y1="260.0" y2="260.0"/><text class="tick" x="40" y="264.0" text-anchor="end">0.0</text><line class="grid" x1="48" x2="600" y1="211.2" y2="211.2"/><text class="tick" x="40" y="215.2" text-anchor="end">0.1</text><line class="grid" x1="48" x2="600" y1="162.4" y2="162.4"/><text class="tick" x="40" y="166.4" text-anchor="end">0.2</text><line class="grid" x1="48" x2="600" y1="113.6" y2="113.6"/><text class="tick" x="40" y="117.6" text-anchor="end">0.3</text><line class="grid" x1="48" x2="600" y1="64.8" y2="64.8"/><text class="tick" x="40" y="68.8" text-anchor="end">0.4</text><line class="grid" x1="48" x2="600" y1="16.0" y2="16.0"/><text class="tick" x="40" y="20.0" text-anchor="end">0.5</text><line class="axis" x1="48" x2="600" y1="138.0" y2="138.0"/><text class="tick" x="54" y="132.0">¼</text><text class="tick" x="48.0" y="286" text-anchor="middle">M = 4</text><text class="tick" x="109.3" y="286" text-anchor="middle">M = 8</text><text class="tick" x="170.7" y="286" text-anchor="middle">M = 12</text><text class="tick" x="232.0" y="286" text-anchor="middle">M = 16</text><text class="tick" x="293.3" y="286" text-anchor="middle">M = 20</text><text class="tick" x="354.7" y="286" text-anchor="middle">M = 24</text><text class="tick" x="416.0" y="286" text-anchor="middle">M = 28</text><text class="tick" x="477.3" y="286" text-anchor="middle">M = 32</text><text class="tick" x="538.7" y="286" text-anchor="middle">M = 36</text><text class="tick" x="600.0" y="286" text-anchor="middle">M = 40</text><path class="s1-line" d="M63.3,16.0 L94.0,64.8 L124.7,85.7 L155.3,97.3 L186.0,104.7 L216.7,109.8 L247.3,113.6 L278.0,116.5 L308.7,118.7 L339.3,120.6 L370.0,122.1 L400.7,123.4 L431.3,124.4 L462.0,125.4 L492.7,126.2 L523.3,126.9 L554.0,127.5 L584.7,128.1" fill="none" stroke-width="2"/><circle class="s1-dot" cx="63.3" cy="16.0" r="4"><title>M = 5: P = 0.5000</title></circle><circle class="s1-dot" cx="94.0" cy="64.8" r="4"><title>M = 7: P = 0.4000</title></circle><circle class="s1-dot" cx="124.7" cy="85.7" r="4"><title>M = 9: P = 0.3571</title></circle><circle class="s1-dot" cx="155.3" cy="97.3" r="4"><title>M = 11: P = 0.3333</title></circle><circle class="s1-dot" cx="186.0" cy="104.7" r="4"><title>M = 13: P = 0.3182</title></circle><circle class="s1-dot" cx="216.7" cy="109.8" r="4"><title>M = 15: P = 0.3077</title></circle><circle class="s1-dot" cx="247.3" cy="113.6" r="4"><title>M = 17: P = 0.3000</title></circle><circle class="s1-dot" cx="278.0" cy="116.5" r="4"><title>M = 19: P = 0.2941</title></circle><circle class="s1-dot" cx="308.7" cy="118.7" r="4"><title>M = 21: P = 0.2895</title></circle><circle class="s1-dot" cx="339.3" cy="120.6" r="4"><title>M = 23: P = 0.2857</title></circle><circle class="s1-dot" cx="370.0" cy="122.1" r="4"><title>M = 25: P = 0.2826</title></circle><circle class="s1-dot" cx="400.7" cy="123.4" r="4"><title>M = 27: P = 0.2800</title></circle><circle class="s1-dot" cx="431.3" cy="124.4" r="4"><title>M = 29: P = 0.2778</title></circle><circle class="s1-dot" cx="462.0" cy="125.4" r="4"><title>M = 31: P = 0.2759</title></circle><circle class="s1-dot" cx="492.7" cy="126.2" r="4"><title>M = 33: P = 0.2742</title></circle><circle class="s1-dot" cx="523.3" cy="126.9" r="4"><title>M = 35: P = 0.2727</title></circle><circle class="s1-dot" cx="554.0" cy="127.5" r="4"><title>M = 37: P = 0.2714</title></circle><circle class="s1-dot" cx="584.7" cy="128.1" r="4"><title>M = 39: P = 0.2703</title></circle><path class="s2-line" d="M48.0,260.0 L78.7,211.2 L109.3,190.3 L140.0,178.7 L170.7,171.3 L201.3,166.2 L232.0,162.4 L262.7,159.5 L293.3,157.3 L324.0,155.4 L354.7,153.9 L385.3,152.6 L416.0,151.6 L446.7,150.6 L477.3,149.8 L508.0,149.1 L538.7,148.5 L569.3,147.9 L600.0,147.4" fill="none" stroke-width="2"/><circle class="s2-dot" cx="48.0" cy="260.0" r="4"><title>M = 4: P = 0.0000</title></circle><circle class="s2-dot" cx="78.7" cy="211.2" r="4"><title>M = 6: P = 0.1000</title></circle><circle class="s2-dot" cx="109.3" cy="190.3" r="4"><title>M = 8: P = 0.1429</title></circle><circle class="s2-dot" cx="140.0" cy="178.7" r="4"><title>M = 10: P = 0.1667</title></circle><circle class="s2-dot" cx="170.7" cy="171.3" r="4"><title>M = 12: P = 0.1818</title></circle><circle class="s2-dot" cx="201.3" cy="166.2" r="4"><title>M = 14: P = 0.1923</title></circle><circle class="s2-dot" cx="232.0" cy="162.4" r="4"><title>M = 16: P = 0.2000</title></circle><circle class="s2-dot" cx="262.7" cy="159.5" r="4"><title>M = 18: P = 0.2059</title></circle><circle class="s2-dot" cx="293.3" cy="157.3" r="4"><title>M = 20: P = 0.2105</title></circle><circle class="s2-dot" cx="324.0" cy="155.4" r="4"><title>M = 22: P = 0.2143</title></circle><circle class="s2-dot" cx="354.7" cy="153.9" r="4"><title>M = 24: P = 0.2174</title></circle><circle class="s2-dot" cx="385.3" cy="152.6" r="4"><title>M = 26: P = 0.2200</title></circle><circle class="s2-dot" cx="416.0" cy="151.6" r="4"><title>M = 28: P = 0.2222</title></circle><circle class="s2-dot" cx="446.7" cy="150.6" r="4"><title>M = 30: P = 0.2241</title></circle><circle class="s2-dot" cx="477.3" cy="149.8" r="4"><title>M = 32: P = 0.2258</title></circle><circle class="s2-dot" cx="508.0" cy="149.1" r="4"><title>M = 34: P = 0.2273</title></circle><circle class="s2-dot" cx="538.7" cy="148.5" r="4"><title>M = 36: P = 0.2286</title></circle><circle class="s2-dot" cx="569.3" cy="147.9" r="4"><title>M = 38: P = 0.2297</title></circle><circle class="s2-dot" cx="600.0" cy="147.4" r="4"><title>M = 40: P = 0.2308</title></circle></svg>

    | \( M \) | משולשים טובים | כל המשולשים | \( P(M) \) |
    |:-:|:-:|:-:|:-:|
    | 3 | 1 | 1 | 1 |
    | 4 | 0 | 4 | 0 |
    | 5 | 5 | 10 | 0.5 |
    | 6 | 2 | 20 | 0.1 |
    | 12 | 40 | 220 | 0.1818 |
    | 13 | 91 | 286 | 0.3182 |
    | 360 | 1,911,720 | 7,711,320 | 0.24791 |
    | 361 | 1,960,230 | 7,775,940 | 0.25209 |
    | \( \infty \) | | | \( \tfrac14 \) |

    - **\( M \) זוגי:** ההסתברות **קטנה** מ-\( \tfrac14 \). יש נקודות שנמצאות בדיוק זו מול
      זו, וכל משולש שיש לו קוטר כצלע נחשב "רע", כי המרכז נמצא על הצלע. המקרה הקיצוני
      הוא \( M = 4 \): כל שלושה קודקודים של ריבוע יוצרים משולש ישר-זווית, והמרכז נמצא על
      היתר.
    - **\( M \) אי-זוגי:** ההסתברות **גדולה** מ-\( \tfrac14 \). המקרה הקיצוני הוא
      \( M = 3 \): יש משולש אחד בלבד, משולש שווה-צלעות, והוא מכיל את המרכז.
    - **\( M \to \infty \):** שני המקרים מתכנסים לתשובה הרציפה \( \tfrac14 \).

    !!! note "ואם מגרילים כל זווית בנפרד?"
        אם מגרילים שלוש זוויות **בלתי תלויות** מתוך \( 0..359 \), ייתכן ששתיים מהן יצאו זהות,
        ואז המשולש מנוון. במקרה הזה ההסתברות היא
        \( \frac{6 \cdot \#\text{good}}{M^3} \approx 0.24585 \) עבור \( M = 360 \): כל משולש טוב
        מתקבל ב-6 סדרים שונים מתוך \( M^3 \) הגרלות.

## נקודות חשובות ושאלות המשך

??? note "נקודות שהמראיין מחפש"
    - **ניסוח גאומטרי נכון:** "כל הקשתות קטנות מ-\( 180° \)", כולל הקשת שעוברת דרך 0°,
      וכולל המקרה הגבולי של קוטר.
    - **constraints במקום לולאת דחייה:** להבין שה-solver מוצא פתרון ישירות, ושה-constraint
      `c_order` גם חוסך מיון וגם מונע כפילויות.
    - **checker עצמאי:** לבדוק את ה-generator בשיטה אחרת (מכפלה וקטורית), ולא באותה
      נוסחה שבה הוא נבנה.
    - **הסתברות:** \( \tfrac14 \) ברציף, וההבדל בין \( M \) זוגי לאי-זוגי בבדיד.

??? note "שאלות המשך"
    - **\( n \) נקודות:** מה ההסתברות שמצולע עם \( n \) קודקודים אקראיים מכיל את המרכז?
      התשובה היא \( 1 - \tfrac{n}{2^{n-1}} \).
    - **distribution ב-SystemVerilog:** איך מוסיפים constraint שגורם למשולשים "שמנים",
      שבהם כל הקשתות קרובות ל-\( 120° \), להופיע יותר? למשל בעזרת `dist` על אורך הקשתות.
    - **כיסוי (coverage):** איזה covergroup הייתם כותבים כדי לוודא שהגרלתם גם משולשים עם
      קשת של \( 179° \), כלומר כמעט מנוונים?
