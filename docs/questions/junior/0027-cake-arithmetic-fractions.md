---
id: 27
title: חלוקת עוגה בסדרה חשבונית – מי מקבל הכי הרבה?
level: junior
difficulty: medium
tags: [math, sequences]
source: ""
added: 2026-10-19
---

## השאלה

יש עוגה שלמה, בגודל 1. אנשים ניגשים אליה בתור, וכל אחד חותך לעצמו פרוסה **ממה שנשאר**
כשהגיע תורו:

- **האדם הראשון** לוקח את השבר \( p_1 = a \) מהעוגה.
- **האדם ה-\( k \)** לוקח את השבר \( p_k = a + (k - 1)d \) ממה שנשאר אחרי כל מי שלפניו.
  השברים עולים בסדרה חשבונית עם הפרש \( d > 0 \).
- **הסוף:** אדם שהשבר שלו מגיע ל-1 או עובר אותו לוקח את כל מה שנשאר, והחלוקה נגמרת.

בשרטוט יש דוגמה עם \( a = d = 0.2 \). כל שורה היא העוגה ברגע שאדם אחד מגיע אליה: השבר
שהוא לוקח גדל משורה לשורה, אבל מה שנשאר לחתוך ממנו קטן. בפס התחתון כל הפרוסות במקומן:

<svg class="figure" viewBox="0 0 640 241" style="max-width:40rem" role="img" aria-label="חלוקת העוגה, שורה לכל אדם: כמה נשאר כשהוא מגיע והפרוסה שהוא חותך, ובסוף כל העוגה עם הפרוסות של כל 5 האנשים"><rect class="cake-gone" x="52" y="8" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="8" width="392.0" height="24"/><rect class="cake-slice" x="444.0" y="8" width="98.0" height="24"><title>אדם 1: p = 0.2, S = 0.2000</title></rect><text class="legend" x="40" y="25" text-anchor="end" style="font-size:17px">1</text><text class="tick" x="548.0" y="24" style="font-size:15px">p = 0.2</text><rect class="cake-gone" x="52" y="41" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="41" width="235.2" height="24"/><rect class="cake-slice2" x="287.2" y="41" width="156.8" height="24"><title>אדם 2: p = 0.4, S = 0.3200</title></rect><text class="legend" x="40" y="58" text-anchor="end" style="font-size:17px">2</text><text class="tick" x="450.0" y="57" style="font-size:15px">p = 0.4</text><rect class="cake-gone" x="52" y="74" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="74" width="94.1" height="24"/><rect class="cake-slice" x="146.1" y="74" width="141.1" height="24"><title>אדם 3: p = 0.6, S = 0.2880</title></rect><text class="legend" x="40" y="91" text-anchor="end" style="font-size:17px">3</text><text class="tick" x="293.2" y="90" style="font-size:15px">p = 0.6</text><rect class="cake-gone" x="52" y="107" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="107" width="18.8" height="24"/><rect class="cake-slice2" x="70.8" y="107" width="75.3" height="24"><title>אדם 4: p = 0.8, S = 0.1536</title></rect><text class="legend" x="40" y="124" text-anchor="end" style="font-size:17px">4</text><text class="tick" x="152.1" y="123" style="font-size:15px">p = 0.8</text><rect class="cake-gone" x="52" y="140" width="490" height="24" rx="3"/><rect class="cake-slice" x="52.0" y="140" width="18.8" height="24"><title>אדם 5: p = 1, S = 0.0384</title></rect><text class="legend" x="40" y="157" text-anchor="end" style="font-size:17px">5</text><text class="tick" x="76.8" y="156" style="font-size:15px">p = 1</text><rect class="cake-slice" x="444.0" y="191" width="98.0" height="24"/><text class="tick" x="493.0" y="233" text-anchor="middle" style="font-size:15px">1</text><rect class="cake-slice2" x="287.2" y="191" width="156.8" height="24"/><text class="tick" x="365.6" y="233" text-anchor="middle" style="font-size:15px">2</text><rect class="cake-slice" x="146.1" y="191" width="141.1" height="24"/><text class="tick" x="216.6" y="233" text-anchor="middle" style="font-size:15px">3</text><rect class="cake-slice2" x="70.8" y="191" width="75.3" height="24"/><text class="tick" x="108.4" y="233" text-anchor="middle" style="font-size:15px">4</text><rect class="cake-slice" x="52.0" y="191" width="18.8" height="24"/><text class="tick" x="61.4" y="233" text-anchor="middle" style="font-size:15px">5</text><rect class="cake-edge" x="52" y="191" width="490" height="24" rx="3"/></svg>

<span class="viz-legend"><span><i class="cake-slice"></i><i class="cake-slice2"></i>הפרוסה של האדם, בשני גוונים לסירוגין</span><span><i class="cake-rest"></i>נשאר לבאים אחריו</span><span><i class="cake-gone"></i>כבר נלקח</span></span>

מי מקבל את החלק הגדול ביותר של העוגה?

??? interviewer "מה המראיין בודק"
    - **מודל נכון:** להבחין בין שבר מהעוגה לשבר ממה שנשאר, ולכתוב את החלק של כל אדם בעזרת
      מה שנשאר לפניו.
    - **השוואה בין שכנים:** במקום לחשב את כל החלקים, להשוות כל אדם לבא אחריו ולראות מה
      מצטמצם.
    - **מאי-שוויון לסף:** להפוך את התנאי למשוואה ריבועית אחת, ולמצוא ממנה סף.
    - **הוכחה ולא רק חישוב:** להראות שהחלקים עולים ואחר כך רק יורדים, ולא לשכוח את התיקו.

---

### סעיף א – הצבה מספרית

כאן \( a = 0.01 \) ו-\( d = 0.1 \), ולכן השברים הם \( 0.01, 0.11, 0.21, 0.31, \dots \). מי מקבל את החלק הגדול ביותר, וכמה הוא מקבל?

??? tip "רמז 1"
    שני כוחות מושכים לכיוונים הפוכים: השבר גדל, אבל מה שנשאר לחתוך ממנו קטן. סמנו ב-\( R_k \)
    את מה שנשאר לפני האדם ה-\( k \), וכתבו את החלק שלו \( S_k \) בעזרתו.

??? tip "רמז 2"
    השוו שני אנשים סמוכים: חשבו את היחס \( S_{k+1} / S_k \). כמעט הכול מצטמצם בו.

??? tip "רמז 3"
    כתבו את התנאי "היחס גדול מ-1" כאי-שוויון על \( p_k \) בלבד, בעזרת \( p_{k+1} = p_k + d \).
    יוצאת משוואה ריבועית, והשורש החיובי שלה הוא סף.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        האדם הרביעי, עם בערך \( 0.216 \) מהעוגה, כלומר 21.6%.

    #### הרעיון { .sol-idea }

    בהתחלה השבר גדל מהר יותר ממה שהעוגה נגמרת, ולכן כל אדם מקבל יותר מקודמו. אחר כך העוגה
    נגמרת מהר יותר, והחלקים קטנים. כדי למצוא את נקודת המפנה משווים כל אדם לבא אחריו: האדם
    הבא מקבל יותר בדיוק כשהשבר הנוכחי \( p_k \) קטן מסף \( T \). החלק הגדול ביותר הוא של
    **האדם הראשון שהשבר שלו מגיע לסף**:

    <svg class="perf-chart" viewBox="0 0 640 250" role="img" aria-label="החלק של כל אדם. הגדול ביותר הוא של האדם ה-4, בערך 0.216 מהעוגה"><line class="grid" x1="46" x2="628" y1="216.0" y2="216.0"/><text class="tick" x="38" y="220.0" text-anchor="end">0.00</text><line class="grid" x1="46" x2="628" y1="177.2" y2="177.2"/><text class="tick" x="38" y="181.2" text-anchor="end">0.05</text><line class="grid" x1="46" x2="628" y1="138.4" y2="138.4"/><text class="tick" x="38" y="142.4" text-anchor="end">0.10</text><line class="grid" x1="46" x2="628" y1="99.6" y2="99.6"/><text class="tick" x="38" y="103.6" text-anchor="end">0.15</text><line class="grid" x1="46" x2="628" y1="60.8" y2="60.8"/><text class="tick" x="38" y="64.8" text-anchor="end">0.20</text><line class="grid" x1="46" x2="628" y1="22.0" y2="22.0"/><text class="tick" x="38" y="26.0" text-anchor="end">0.25</text><rect class="bar by-multiples" x="54.5" y="208.2" width="36.0" height="7.8" rx="2"><title>S(1) = 0.0100</title></rect><text class="tick" x="72.5" y="203.2" text-anchor="middle">0.010</text><text class="tick" x="72.5" y="234" text-anchor="middle">1</text><rect class="bar by-multiples" x="107.4" y="131.5" width="36.0" height="84.5" rx="2"><title>S(2) = 0.1089</title></rect><text class="tick" x="125.4" y="126.5" text-anchor="middle">0.109</text><text class="tick" x="125.4" y="234" text-anchor="middle">2</text><rect class="bar by-multiples" x="160.3" y="72.4" width="36.0" height="143.6" rx="2"><title>S(3) = 0.1850</title></rect><text class="tick" x="178.3" y="67.4" text-anchor="middle">0.185</text><text class="tick" x="178.3" y="234" text-anchor="middle">3</text><rect class="bar by-enum" x="213.2" y="48.6" width="36.0" height="167.4" rx="2"><title>S(4) = 0.2158</title></rect><text class="tick" x="231.2" y="43.6" text-anchor="middle">0.216</text><text class="tick" x="231.2" y="234" text-anchor="middle">4</text><rect class="bar by-multiples" x="266.1" y="63.2" width="36.0" height="152.8" rx="2"><title>S(5) = 0.1969</title></rect><text class="tick" x="284.1" y="58.2" text-anchor="middle">0.197</text><text class="tick" x="284.1" y="234" text-anchor="middle">5</text><rect class="bar by-multiples" x="319.0" y="103.9" width="36.0" height="112.1" rx="2"><title>S(6) = 0.1445</title></rect><text class="tick" x="337.0" y="98.9" text-anchor="middle">0.145</text><text class="tick" x="337.0" y="234" text-anchor="middle">6</text><rect class="bar by-multiples" x="371.9" y="150.3" width="36.0" height="65.7" rx="2"><title>S(7) = 0.0847</title></rect><text class="tick" x="389.9" y="145.3" text-anchor="middle">0.085</text><text class="tick" x="389.9" y="234" text-anchor="middle">7</text><rect class="bar by-multiples" x="424.8" y="186.2" width="36.0" height="29.8" rx="2"><title>S(8) = 0.0384</title></rect><text class="tick" x="442.8" y="181.2" text-anchor="middle">0.038</text><text class="tick" x="442.8" y="234" text-anchor="middle">8</text><rect class="bar by-multiples" x="477.7" y="206.1" width="36.0" height="9.9" rx="2"><title>S(9) = 0.0127</title></rect><text class="tick" x="495.7" y="201.1" text-anchor="middle">0.013</text><text class="tick" x="495.7" y="234" text-anchor="middle">9</text><rect class="bar by-multiples" x="530.6" y="213.9" width="36.0" height="2.1" rx="2"><title>S(10) = 0.0027</title></rect><text class="tick" x="548.6" y="208.9" text-anchor="middle">0.003</text><text class="tick" x="548.6" y="234" text-anchor="middle">10</text><rect class="bar by-multiples" x="583.6" y="215.8" width="36.0" height="0.2" rx="2"><title>S(11) = 0.0003</title></rect><text class="tick" x="601.5" y="210.8" text-anchor="middle">0.000</text><text class="tick" x="601.5" y="234" text-anchor="middle">11</text><line class="axis" x1="46" x2="628" y1="216" y2="216"/><text class="tick" x="38" y="234" text-anchor="end">k</text></svg>

    <span class="viz-legend"><span><i class="by-multiples"></i>‏\( S_k \), החלק של האדם ה-\( k \)</span><span><i class="by-enum"></i>החלק הגדול ביותר</span></span>

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סימונים:** ‏\( R_k \) הוא מה שנשאר מהעוגה לפני האדם ה-\( k \), עם \( R_1 = 1 \).
       האדם לוקח \( p_k \) ממנו, והשאר עובר הלאה:

        \[
        S_k = p_k R_k, \qquad R_{k+1} = (1 - p_k) R_k
        \]

    2. **היחס בין שכנים:** מה שנשאר מצטמצם, ונשארים רק השברים:

        \[
        \begin{aligned}
        \frac{S_{k+1}}{S_k} &= \frac{p_{k+1} R_{k+1}}{p_k R_k} \\
                            &= \frac{p_{k+1}(1 - p_k)}{p_k}
        \end{aligned}
        \]

        האדם ה-\( k + 1 \) מקבל יותר מהאדם ה-\( k \) בדיוק כשהיחס גדול מ-1.

    3. **מציבים \( p_{k+1} = p_k + d \):** ופותחים סוגריים:

        \[
        \begin{aligned}
        S_{k+1} > S_k &\iff (p_k + d)(1 - p_k) > p_k \\
                      &\iff p_k + d - p_k^2 - d\,p_k > p_k \\
                      &\iff p_k^2 + d\,p_k - d < 0
        \end{aligned}
        \]

    4. **הסף:** השורש החיובי של \( p^2 + 0.1p - 0.1 = 0 \) הוא

        \[
        \begin{aligned}
        T &= \frac{-0.1 + \sqrt{0.01 + 0.4}}{2} \\
          &= \frac{\sqrt{0.41} - 0.1}{2} \approx 0.2702
        \end{aligned}
        \]

        כל עוד \( p_k < T \) החלקים גדלים, ומהרגע ש-\( p_k \ge T \) הם קטנים.

    5. **מי עובר את הסף:** ‏\( p_3 = 0.21 < T \), ולכן \( S_4 > S_3 \). ‏\( p_4 = 0.31 \ge T \),
       ולכן \( S_5 < S_4 \). בנוסחה של סעיף ב:
       \( k = \left\lceil \frac{T - a}{d} \right\rceil + 1 = \lceil 2.60 \rceil + 1 = 4 \).

    6. **החלק שלו:** לפני האדם הרביעי נשאר \( R_4 = 0.99 \cdot 0.89 \cdot 0.79 \approx 0.6961 \),
       והוא לוקח ממנו \( 0.31 \):
       \( S_4 = 0.31 \cdot 0.6961 \approx 0.2158 \).

    </div>

    בגרף, כל עמוד הוא השבר של אדם אחד, והקו המקווקו הוא הסף. העמודים הכחולים מתחת לסף: אחרי
    כל אחד מהם בא אדם שמקבל יותר. הראשון שמגיע לסף הוא האדם הרביעי:

    <svg class="perf-chart" viewBox="0 0 640 250" role="img" aria-label="השבר של כל אדם מול הסף T, בערך 0.270. הראשון שמגיע לסף הוא האדם ה-4"><line class="grid" x1="46" x2="628" y1="216.0" y2="216.0"/><text class="tick" x="38" y="220.0" text-anchor="end">0</text><line class="grid" x1="46" x2="628" y1="166.0" y2="166.0"/><text class="tick" x="38" y="170.0" text-anchor="end">0.25</text><line class="grid" x1="46" x2="628" y1="116.0" y2="116.0"/><text class="tick" x="38" y="120.0" text-anchor="end">0.5</text><line class="grid" x1="46" x2="628" y1="66.0" y2="66.0"/><text class="tick" x="38" y="70.0" text-anchor="end">0.75</text><line class="grid" x1="46" x2="628" y1="16.0" y2="16.0"/><text class="tick" x="38" y="20.0" text-anchor="end">1</text><line class="ink-line" x1="46" x2="628" y1="162.0" y2="162.0" stroke-width="1.5" stroke-dasharray="6 4"/><text class="legend" x="52" y="156.0">T ≈ 0.270</text><line class="s1-line" x1="72.5" x2="72.5" y1="216" y2="214.0" stroke-width="2"/><circle class="s1-dot" cx="72.5" cy="214.0" r="4.5"><title>p(1) = 0.0100</title></circle><text class="tick" x="72.5" y="234" text-anchor="middle">1</text><line class="s1-line" x1="125.4" x2="125.4" y1="216" y2="194.0" stroke-width="2"/><circle class="s1-dot" cx="125.4" cy="194.0" r="4.5"><title>p(2) = 0.1100</title></circle><text class="tick" x="125.4" y="234" text-anchor="middle">2</text><line class="s1-line" x1="178.3" x2="178.3" y1="216" y2="174.0" stroke-width="2"/><circle class="s1-dot" cx="178.3" cy="174.0" r="4.5"><title>p(3) = 0.2100</title></circle><text class="tick" x="178.3" y="234" text-anchor="middle">3</text><line class="s2-line" x1="231.2" x2="231.2" y1="216" y2="154.0" stroke-width="2"/><circle class="s2-dot" cx="231.2" cy="154.0" r="6"><title>p(4) = 0.3100</title></circle><text class="tick" x="231.2" y="234" text-anchor="middle">4</text><line class="ink-line" x1="284.1" x2="284.1" y1="216" y2="134.0" stroke-width="2"/><circle class="ink-dot" cx="284.1" cy="134.0" r="4.5"><title>p(5) = 0.4100</title></circle><text class="tick" x="284.1" y="234" text-anchor="middle">5</text><line class="ink-line" x1="337.0" x2="337.0" y1="216" y2="114.0" stroke-width="2"/><circle class="ink-dot" cx="337.0" cy="114.0" r="4.5"><title>p(6) = 0.5100</title></circle><text class="tick" x="337.0" y="234" text-anchor="middle">6</text><line class="ink-line" x1="389.9" x2="389.9" y1="216" y2="94.0" stroke-width="2"/><circle class="ink-dot" cx="389.9" cy="94.0" r="4.5"><title>p(7) = 0.6100</title></circle><text class="tick" x="389.9" y="234" text-anchor="middle">7</text><line class="ink-line" x1="442.8" x2="442.8" y1="216" y2="74.0" stroke-width="2"/><circle class="ink-dot" cx="442.8" cy="74.0" r="4.5"><title>p(8) = 0.7100</title></circle><text class="tick" x="442.8" y="234" text-anchor="middle">8</text><line class="ink-line" x1="495.7" x2="495.7" y1="216" y2="54.0" stroke-width="2"/><circle class="ink-dot" cx="495.7" cy="54.0" r="4.5"><title>p(9) = 0.8100</title></circle><text class="tick" x="495.7" y="234" text-anchor="middle">9</text><line class="ink-line" x1="548.6" x2="548.6" y1="216" y2="34.0" stroke-width="2"/><circle class="ink-dot" cx="548.6" cy="34.0" r="4.5"><title>p(10) = 0.9100</title></circle><text class="tick" x="548.6" y="234" text-anchor="middle">10</text><line class="ink-line" x1="601.5" x2="601.5" y1="216" y2="16.0" stroke-width="2"/><circle class="ink-dot" cx="601.5" cy="16.0" r="4.5"><title>p(11) = 1.0000</title></circle><text class="tick" x="601.5" y="234" text-anchor="middle">11</text><line class="axis" x1="46" x2="628" y1="216" y2="216"/><text class="tick" x="38" y="234" text-anchor="end">k</text></svg>

    <span class="viz-legend"><span><i class="s1"></i>מתחת לסף: הבא אחריו מקבל יותר</span><span><i class="s2"></i>הראשון שמגיע לסף: החלק הגדול ביותר</span><span><i class="ink"></i>מעל הסף</span><span><i class="ink-dash"></i>הסף \( T \)</span></span>

    #### למה זה נכון { .sol-proof }

    **היחס על גרף.** כאן הנקודה ב-\( k \) היא היחס \( S_{k+1} / S_k \), בסולם לוגריתמי כי
    הוא מתחיל ב-10.89. כל עוד הנקודה מעל הקו \( y = 1 \), האדם הבא מקבל יותר. הנקודה
    הראשונה מתחת לקו היא אצל האדם הרביעי, ומשם כל הנקודות מתחת לקו:

    <svg class="perf-chart" viewBox="0 0 640 250" role="img" aria-label="היחס בין החלק של האדם הבא לחלק של האדם הנוכחי. הוא יורד מתחת ל-1 לראשונה אצל האדם ה-4"><line class="grid" x1="46" x2="628" y1="192.9" y2="192.9"/><text class="tick" x="38" y="196.9" text-anchor="end">0.1</text><line class="grid" x1="46" x2="628" y1="169.7" y2="169.7"/><text class="tick" x="38" y="173.7" text-anchor="end">0.2</text><line class="grid" x1="46" x2="628" y1="139.1" y2="139.1"/><text class="tick" x="38" y="143.1" text-anchor="end">0.5</text><line class="grid" x1="46" x2="628" y1="116.0" y2="116.0"/><text class="tick" x="38" y="120.0" text-anchor="end">1</text><line class="grid" x1="46" x2="628" y1="92.9" y2="92.9"/><text class="tick" x="38" y="96.9" text-anchor="end">2</text><line class="grid" x1="46" x2="628" y1="62.3" y2="62.3"/><text class="tick" x="38" y="66.3" text-anchor="end">5</text><line class="grid" x1="46" x2="628" y1="39.1" y2="39.1"/><text class="tick" x="38" y="43.1" text-anchor="end">10</text><line class="ink-line" x1="46" x2="628" y1="116.0" y2="116.0" stroke-width="1.5" stroke-dasharray="6 4"/><polyline class="s1-line" points="72.5,36.3 125.4,98.3 178.3,110.9 231.2,119.1 284.1,126.3 337.0,133.8 389.9,142.4 442.8,152.9 495.7,167.6 548.6,193.2" fill="none" stroke-width="1.5"/><circle class="s1-dot" cx="72.5" cy="36.3" r="4.5"><title>S(2) / S(1) = 10.890</title></circle><circle class="s1-dot" cx="125.4" cy="98.3" r="4.5"><title>S(3) / S(2) = 1.699</title></circle><circle class="s1-dot" cx="178.3" cy="110.9" r="4.5"><title>S(4) / S(3) = 1.166</title></circle><circle class="s2-dot" cx="231.2" cy="119.1" r="6"><title>S(5) / S(4) = 0.913</title></circle><circle class="s1-dot" cx="284.1" cy="126.3" r="4.5"><title>S(6) / S(5) = 0.734</title></circle><circle class="s1-dot" cx="337.0" cy="133.8" r="4.5"><title>S(7) / S(6) = 0.586</title></circle><circle class="s1-dot" cx="389.9" cy="142.4" r="4.5"><title>S(8) / S(7) = 0.454</title></circle><circle class="s1-dot" cx="442.8" cy="152.9" r="4.5"><title>S(9) / S(8) = 0.331</title></circle><circle class="s1-dot" cx="495.7" cy="167.6" r="4.5"><title>S(10) / S(9) = 0.213</title></circle><circle class="ink-dot" cx="548.6" cy="193.2" r="4.5"><title>S(11) / S(10) = 0.099</title></circle><text class="tick" x="72.5" y="234" text-anchor="middle">1</text><text class="tick" x="125.4" y="234" text-anchor="middle">2</text><text class="tick" x="178.3" y="234" text-anchor="middle">3</text><text class="tick" x="231.2" y="234" text-anchor="middle">4</text><text class="tick" x="284.1" y="234" text-anchor="middle">5</text><text class="tick" x="337.0" y="234" text-anchor="middle">6</text><text class="tick" x="389.9" y="234" text-anchor="middle">7</text><text class="tick" x="442.8" y="234" text-anchor="middle">8</text><text class="tick" x="495.7" y="234" text-anchor="middle">9</text><text class="tick" x="548.6" y="234" text-anchor="middle">10</text><line class="axis" x1="46" x2="628" y1="216" y2="216"/><text class="tick" x="38" y="234" text-anchor="end">k</text></svg>

    <span class="viz-legend"><span><i class="s1"></i>היחס \( S_{k+1} / S_k \)</span><span><i class="s2"></i>הפעם הראשונה מתחת ל-1</span><span><i class="ink"></i>היחס אל מי שלוקח את השארית</span><span><i class="ink-dash"></i>הקו \( y = 1 \)</span></span>

    **העוגה עצמה.** אותה חלוקה בשורות, עם הפרוסה של האדם הרביעי מודגשת. בשורות העליונות
    הפרוסות דקות כי השבר קטן, ובתחתונות הן דקות כי כמעט לא נשאר כלום:

    <svg class="figure" viewBox="0 0 640 439" style="max-width:40rem" role="img" aria-label="חלוקת העוגה, שורה לכל אדם: כמה נשאר כשהוא מגיע והפרוסה שהוא חותך, ובסוף כל העוגה עם הפרוסות של כל 11 האנשים"><rect class="cake-gone" x="52" y="8" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="8" width="485.1" height="24"/><rect class="cake-slice" x="537.1" y="8" width="4.9" height="24"><title>אדם 1: p = 0.01, S = 0.0100</title></rect><text class="legend" x="40" y="25" text-anchor="end" style="font-size:17px">1</text><text class="tick" x="548.0" y="24" style="font-size:15px">p = 0.01</text><rect class="cake-gone" x="52" y="41" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="41" width="431.7" height="24"/><rect class="cake-slice2" x="483.7" y="41" width="53.4" height="24"><title>אדם 2: p = 0.11, S = 0.1089</title></rect><text class="legend" x="40" y="58" text-anchor="end" style="font-size:17px">2</text><text class="tick" x="543.1" y="57" style="font-size:15px">p = 0.11</text><rect class="cake-gone" x="52" y="74" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="74" width="341.1" height="24"/><rect class="cake-slice" x="393.1" y="74" width="90.7" height="24"><title>אדם 3: p = 0.21, S = 0.1850</title></rect><text class="legend" x="40" y="91" text-anchor="end" style="font-size:17px">3</text><text class="tick" x="489.7" y="90" style="font-size:15px">p = 0.21</text><rect class="cake-gone" x="52" y="107" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="107" width="235.3" height="24"/><rect class="cake-peak" x="287.3" y="107" width="105.7" height="24"><title>אדם 4: p = 0.31, S = 0.2158</title></rect><text class="legend" x="40" y="124" text-anchor="end" style="font-size:17px">4</text><text class="tick" x="399.1" y="123" style="font-size:15px">p = 0.31</text><rect class="cake-gone" x="52" y="140" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="140" width="138.9" height="24"/><rect class="cake-slice" x="190.9" y="140" width="96.5" height="24"><title>אדם 5: p = 0.41, S = 0.1969</title></rect><text class="legend" x="40" y="157" text-anchor="end" style="font-size:17px">5</text><text class="tick" x="293.3" y="156" style="font-size:15px">p = 0.41</text><rect class="cake-gone" x="52" y="173" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="173" width="68.0" height="24"/><rect class="cake-slice2" x="120.0" y="173" width="70.8" height="24"><title>אדם 6: p = 0.51, S = 0.1445</title></rect><text class="legend" x="40" y="190" text-anchor="end" style="font-size:17px">6</text><text class="tick" x="196.9" y="189" style="font-size:15px">p = 0.51</text><rect class="cake-gone" x="52" y="206" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="206" width="26.5" height="24"/><rect class="cake-slice" x="78.5" y="206" width="41.5" height="24"><title>אדם 7: p = 0.61, S = 0.0847</title></rect><text class="legend" x="40" y="223" text-anchor="end" style="font-size:17px">7</text><text class="tick" x="126.0" y="222" style="font-size:15px">p = 0.61</text><rect class="cake-gone" x="52" y="239" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="239" width="7.7" height="24"/><rect class="cake-slice2" x="59.7" y="239" width="18.8" height="24"><title>אדם 8: p = 0.71, S = 0.0384</title></rect><text class="legend" x="40" y="256" text-anchor="end" style="font-size:17px">8</text><text class="tick" x="84.5" y="255" style="font-size:15px">p = 0.71</text><rect class="cake-gone" x="52" y="272" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="272" width="1.5" height="24"/><rect class="cake-slice" x="53.5" y="272" width="6.2" height="24"><title>אדם 9: p = 0.81, S = 0.0127</title></rect><text class="legend" x="40" y="289" text-anchor="end" style="font-size:17px">9</text><text class="tick" x="65.7" y="288" style="font-size:15px">p = 0.81</text><rect class="cake-gone" x="52" y="305" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="305" width="0.1" height="24"/><rect class="cake-slice2" x="52.1" y="305" width="1.3" height="24"><title>אדם 10: p = 0.91, S = 0.0027</title></rect><text class="legend" x="40" y="322" text-anchor="end" style="font-size:17px">10</text><text class="tick" x="59.5" y="321" style="font-size:15px">p = 0.91</text><rect class="cake-gone" x="52" y="338" width="490" height="24" rx="3"/><rect class="cake-slice" x="52.0" y="338" width="0.6" height="24"><title>אדם 11: p = 1, S = 0.0003</title></rect><text class="legend" x="40" y="355" text-anchor="end" style="font-size:17px">11</text><text class="tick" x="58.1" y="354" style="font-size:15px">p = 1</text><rect class="cake-slice" x="537.1" y="389" width="4.9" height="24"/><rect class="cake-slice2" x="483.7" y="389" width="53.4" height="24"/><text class="tick" x="510.4" y="431" text-anchor="middle" style="font-size:15px">2</text><rect class="cake-slice" x="393.1" y="389" width="90.7" height="24"/><text class="tick" x="438.4" y="431" text-anchor="middle" style="font-size:15px">3</text><rect class="cake-peak" x="287.3" y="389" width="105.7" height="24"/><text class="tick" x="340.2" y="431" text-anchor="middle" style="font-size:15px">4</text><rect class="cake-slice" x="190.9" y="389" width="96.5" height="24"/><text class="tick" x="239.1" y="431" text-anchor="middle" style="font-size:15px">5</text><rect class="cake-slice2" x="120.0" y="389" width="70.8" height="24"/><text class="tick" x="155.4" y="431" text-anchor="middle" style="font-size:15px">6</text><rect class="cake-slice" x="78.5" y="389" width="41.5" height="24"/><text class="tick" x="99.3" y="431" text-anchor="middle" style="font-size:15px">7</text><rect class="cake-slice2" x="59.7" y="389" width="18.8" height="24"/><text class="tick" x="69.1" y="431" text-anchor="middle" style="font-size:15px">8</text><rect class="cake-slice" x="53.5" y="389" width="6.2" height="24"/><rect class="cake-slice2" x="52.1" y="389" width="1.3" height="24"/><rect class="cake-slice" x="52.0" y="389" width="0.6" height="24"/><rect class="cake-edge" x="52" y="389" width="490" height="24" rx="3"/></svg>

    <span class="viz-legend"><span><i class="cake-slice"></i><i class="cake-slice2"></i>הפרוסה של האדם, בשני גוונים לסירוגין</span><span><i class="cake-peak"></i>הפרוסה הגדולה ביותר</span><span><i class="cake-rest"></i>נשאר לבאים אחריו</span><span><i class="cake-gone"></i>כבר נלקח</span></span>

    **כל המספרים.** הטבלה מאשרת: החלקים עולים עד האדם הרביעי ויורדים אחריו. האדם האחרון
    לוקח את כל השארית, שהיא כמעט אפס:

    | האדם \( k \) | השבר \( p_k \) | נשאר לפניו \( R_k \) | מקבל \( S_k \) |
    |---|---|---|---|
    | 1 | 0.01 | 1 | 0.0100 |
    | 2 | 0.11 | 0.9900 | 0.1089 |
    | 3 | 0.21 | 0.8811 | 0.1850 |
    | **4** | **0.31** | **0.6961** | **0.2158** |
    | 5 | 0.41 | 0.4803 | 0.1969 |
    | 6 | 0.51 | 0.2834 | 0.1445 |
    | 7 | 0.61 | 0.1389 | 0.0847 |
    | 8 | 0.71 | 0.0542 | 0.0384 |
    | 9 | 0.81 | 0.0157 | 0.0127 |
    | 10 | 0.91 | 0.0030 | 0.0027 |
    | 11 | 1, לוקח את השארית | 0.0003 | 0.0003 |

---

### סעיף ב – המקרה הכללי

עבור \( a > 0 \) ו-\( 0 < d \le \tfrac12 \) כלשהם, מצאו נוסחה לאדם שמקבל את החלק הגדול
ביותר. הוכיחו שיש פסגה אחת: החלקים עולים עד אדם מסוים, ואחריו רק יורדים. מתי יש תיקו?

ההנחה \( d \le \tfrac12 \) אומרת שהשבר לא קופץ ביותר מחצי בין שני אנשים סמוכים. נחזור
למקרה החריג בשאלות ההמשך.

??? tip "רמז 1"
    התנאי משלב 3 של סעיף א לא השתמש במספרים עד הסוף. כתבו אותו עם \( d \) כללי, והעבירו
    אגפים כך שבצד אחד יהיה רק \( p_k \).

??? tip "רמז 2"
    התנאי הוא \( \dfrac{p_k^2}{1 - p_k} < d \). מה קורה לאגף שמאל כש-\( p_k \) גדל, ומה זה אומר
    על האנשים שאחרי הפעם הראשונה שהתנאי נכשל?

??? tip "רמז 3"
    אל תשכחו את האדם האחרון: השבר שלו נחתך ל-1. בדקו שהחיתוך לא משנה את התשובה כש-\( d \le \tfrac12 \).

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        הסף הוא \( T = \dfrac{\sqrt{d^2 + 4d} - d}{2} \), והחלק הגדול ביותר הוא של האדם הראשון
        שהשבר שלו מגיע לסף:
        \( k = \max\left(1,\ \left\lceil \frac{T - a}{d} \right\rceil + 1\right) \).
        אם \( a + (k - 1)d = T \) בדיוק, יש תיקו בינו לבין האדם שאחריו.

    #### הרעיון { .sol-idea }

    התנאי "האדם הבא מקבל יותר" שקול ל-\( f(p_k) < d \), כש-\( f(p) = \dfrac{p^2}{1 - p} \).
    הפונקציה \( f \) עולה, והשברים \( p_k \) עולים, ולכן גם \( f(p_k) \) עולה עם \( k \).
    ברגע שהתנאי נכשל הוא נכשל לתמיד: החלקים עולים, ומאז רק יורדים. זו פסגה אחת, והיא אצל
    האדם הראשון שהשבר שלו מגיע לסף \( T \), הנקודה שבה \( f(T) = d \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **התנאי הכללי:** אותו פיתוח כמו בסעיף א, עם \( d \) כללי. מחלקים ב-\( 1 - p_k > 0 \),
       שהוא חיובי לכל מי שאינו האחרון:

        \[
        \begin{aligned}
        S_{k+1} > S_k &\iff d(1 - p_k) > p_k^2 \\
                      &\iff f(p_k) = \frac{p_k^2}{1 - p_k} < d
        \end{aligned}
        \]

    2. **הפונקציה עולה:** בתחום \( 0 < p < 1 \) המונה \( p^2 \) גדל והמכנה \( 1 - p \) קטן,
       ושניהם חיוביים. לכן \( f \) עולה. בנגזרת:
       \( f'(p) = \dfrac{p(2 - p)}{(1 - p)^2} > 0 \).

    3. **פסגה אחת:** השברים \( p_k \) עולים עם \( k \), ולכן גם \( f(p_k) \) עולה. כל עוד
       \( f(p_k) < d \) החלקים גדלים. מהאדם הראשון שבו \( f(p_k) \ge d \), התנאי לא חוזר
       להתקיים, והחלקים רק קטנים. אם \( f(p_k) = d \) בדיוק, אז \( S_{k+1} = S_k \): תיקו.

    4. **הסף:** ‏\( f(p) = d \) היא המשוואה \( p^2 + dp - d = 0 \), והשורש החיובי שלה הוא

        \[
        T = \frac{\sqrt{d^2 + 4d} - d}{2}
        \]

        הוא תמיד בין 0 ל-1: ב-\( p = 0 \) אגף שמאל הוא \( -d < 0 \), וב-\( p = 1 \) הוא
        \( 1 > 0 \). כש-\( d \le \tfrac12 \) גם \( T \le \tfrac12 \), כי ב-\( p = \tfrac12 \)
        אגף שמאל הוא \( \tfrac14 - \tfrac{d}{2} \ge 0 \).

    5. **האדם האחרון:** האדם \( L \) שלוקח את השארית מקבל את השבר 1 ולא \( p_{L-1} + d \),
       ולכן היחס אליו הוא \( \frac{1 - p_{L-1}}{p_{L-1}} \). אם \( p_{L-1} < T \le \tfrac12 \),
       היחס הזה גדול מ-1, כמו שהתנאי אומר. אם \( p_{L-1} \ge T \), היחס קטן מהיחס בלי
       החיתוך, שכבר קטן מ-1 או שווה לו. בשני המקרים התשובה לא משתנה. גם התיקו נשאר: אם
       \( p_{L-1} = T \le \tfrac12 \), אז \( p_{L-1} + d \le 1 \), ולכן השבר של האחרון הוא
       בדיוק 1, בלי חיתוך.

    6. **הנוסחה:** מחפשים את ה-\( k \) הקטן ביותר שבו \( a + (k - 1)d \ge T \), כלומר
       \( k - 1 \ge \frac{T - a}{d} \):

        \[
        k = \max\left(1,\ \left\lceil \frac{T - a}{d} \right\rceil + 1\right)
        \]

        אם \( a \ge T \), האדם הראשון מקבל הכי הרבה. אם \( a + (k - 1)d = T \) בדיוק, האדם
        ה-\( k \) והאדם ה-\( k + 1 \) מקבלים חלק שווה.

    </div>

    #### למה זה נכון { .sol-proof }

    **הסף בגרף.** העקומה היא \( f(p) \), והקו המקווקו הוא \( y = d \) עבור \( d = 0.1 \)
    של סעיף א. הם נחתכים ב-\( T \approx 0.270 \). על העקומה מסומנים השברים של האנשים
    הראשונים: שלושה מתחת לקו, והרביעי הוא הראשון מעליו:

    <svg class="perf-chart" viewBox="0 0 640 260" role="img" aria-label="הפונקציה p בריבוע חלקי 1 פחות p, מול הקו בגובה d = 0.1. הם נחתכים ב-T, בערך 0.270"><line class="grid" x1="46" x2="626" y1="226.0" y2="226.0"/><text class="tick" x="38" y="230.0" text-anchor="end">0</text><line class="grid" x1="46" x2="626" y1="190.7" y2="190.7"/><text class="tick" x="38" y="194.7" text-anchor="end">0.1</text><line class="grid" x1="46" x2="626" y1="155.3" y2="155.3"/><text class="tick" x="38" y="159.3" text-anchor="end">0.2</text><line class="grid" x1="46" x2="626" y1="120.0" y2="120.0"/><text class="tick" x="38" y="124.0" text-anchor="end">0.3</text><line class="grid" x1="46" x2="626" y1="84.7" y2="84.7"/><text class="tick" x="38" y="88.7" text-anchor="end">0.4</text><line class="grid" x1="46" x2="626" y1="49.3" y2="49.3"/><text class="tick" x="38" y="53.3" text-anchor="end">0.5</text><line class="grid" x1="46" x2="626" y1="14.0" y2="14.0"/><text class="tick" x="38" y="18.0" text-anchor="end">0.6</text><text class="tick" x="46.0" y="244" text-anchor="middle">0</text><text class="tick" x="128.9" y="244" text-anchor="middle">0.1</text><text class="tick" x="211.7" y="244" text-anchor="middle">0.2</text><text class="tick" x="294.6" y="244" text-anchor="middle">0.3</text><text class="tick" x="377.4" y="244" text-anchor="middle">0.4</text><text class="tick" x="460.3" y="244" text-anchor="middle">0.5</text><text class="tick" x="543.1" y="244" text-anchor="middle">0.6</text><polyline class="s1-line" points="46.0,226.0 50.1,226.0 54.3,226.0 58.4,225.9 62.6,225.9 66.7,225.8 70.9,225.7 75.0,225.6 79.1,225.4 83.3,225.3 87.4,225.1 91.6,224.9 95.7,224.6 99.9,224.4 104.0,224.1 108.1,223.9 112.3,223.5 116.4,223.2 120.6,222.9 124.7,222.5 128.9,222.1 133.0,221.6 137.1,221.2 141.3,220.7 145.4,220.2 149.6,219.7 153.7,219.1 157.9,218.6 162.0,217.9 166.1,217.3 170.3,216.6 174.4,216.0 178.6,215.2 182.7,214.5 186.9,213.7 191.0,212.9 195.1,212.0 199.3,211.2 203.4,210.3 207.6,209.3 211.7,208.3 215.9,207.3 220.0,206.3 224.1,205.2 228.3,204.1 232.4,202.9 236.6,201.7 240.7,200.5 244.9,199.2 249.0,197.9 253.1,196.6 257.3,195.2 261.4,193.7 265.6,192.2 269.7,190.7 273.9,189.1 278.0,187.5 282.1,185.9 286.3,184.1 290.4,182.4 294.6,180.6 298.7,178.7 302.9,176.8 307.0,174.8 311.1,172.8 315.3,170.7 319.4,168.6 323.6,166.4 327.7,164.1 331.9,161.8 336.0,159.4 340.1,157.0 344.3,154.4 348.4,151.9 352.6,149.2 356.7,146.5 360.9,143.7 365.0,140.8 369.1,137.9 373.3,134.9 377.4,131.8 381.6,128.6 385.7,125.3 389.9,122.0 394.0,118.5 398.1,115.0 402.3,111.4 406.4,107.7 410.6,103.8 414.7,99.9 418.9,95.9 423.0,91.8 427.1,87.5 431.3,83.2 435.4,78.7 439.6,74.2 443.7,69.4 447.9,64.6 452.0,59.7 456.1,54.6 460.3,49.3 464.4,44.0 468.6,38.4 472.7,32.8 476.9,27.0 481.0,21.0 485.1,14.8" fill="none" stroke-width="2.5"/><line class="ink-line" x1="46" x2="626" y1="190.7" y2="190.7" stroke-width="1.5" stroke-dasharray="6 4"/><text class="legend" x="622" y="184.7" text-anchor="end">y = d = 0.1</text><line class="ink-line" x1="269.8" x2="269.8" y1="190.7" y2="226" stroke-width="1" stroke-dasharray="3 3"/><text class="legend" x="275.8" y="220">T ≈ 0.270</text><circle class="s1-dot" cx="54.3" cy="226.0" r="4.5"><title>p(1) = 0.0100</title></circle><text class="tick" x="54.3" y="217.0" text-anchor="middle">1</text><circle class="s1-dot" cx="137.1" cy="221.2" r="4.5"><title>p(2) = 0.1100</title></circle><text class="tick" x="137.1" y="212.2" text-anchor="middle">2</text><circle class="s1-dot" cx="220.0" cy="206.3" r="4.5"><title>p(3) = 0.2100</title></circle><text class="tick" x="220.0" y="197.3" text-anchor="middle">3</text><circle class="s2-dot" cx="302.9" cy="176.8" r="6"><title>p(4) = 0.3100</title></circle><text class="tick" x="302.9" y="167.8" text-anchor="middle">4</text><circle class="ink-dot" cx="385.7" cy="125.3" r="4.5"><title>p(5) = 0.4100</title></circle><text class="tick" x="385.7" y="116.3" text-anchor="middle">5</text><circle class="ink-dot" cx="468.6" cy="38.4" r="4.5"><title>p(6) = 0.5100</title></circle><text class="tick" x="468.6" y="29.4" text-anchor="middle">6</text><circle class="ink-dot" cx="269.8" cy="190.7" r="3.5"/><line class="axis" x1="46" x2="626" y1="226" y2="226"/><text class="tick" x="626" y="244" text-anchor="end">p</text></svg>

    <span class="viz-legend"><span><i class="s1"></i>‏\( f(p) = p^2 / (1 - p) \)</span><span><i class="ink-dash"></i>הקו \( y = d \)</span><span><i class="s2"></i>האדם ה-4: הראשון מעל הקו</span><span><i class="ink"></i>אחריו, גם הם מעל הקו</span></span>

    **מקרה פרטי: \( a = d \).** אז \( p_k = kd \), ומציבים בתנאי \( p_k^2 + d\,p_k - d \ge 0 \):

    \[
    k^2 d^2 + k d^2 - d \ge 0 \iff k(k + 1) \ge \frac{1}{d}
    \]

    כלומר האדם הראשון שעבורו \( k(k + 1) \ge 1/d \), ובנוסחה סגורה
    \( k = \left\lceil \frac{\sqrt{1 + 4/d} - 1}{2} \right\rceil \). כש-\( d \) קטן,
    \( k \approx 1/\sqrt{d} \). עוד דוגמאות. בעמודה האחרונה, כש-\( a = d \), הבדיקה \( k(k + 1) \ge 1/d \) של האדם הגדול:

    | הפרמטרים | הסף \( T \) | המקבל הגדול | הערה |
    |---|---|---|---|
    | ‏\( a = 0.01,\ d = 0.1 \) | ‏0.270 | האדם ה-4 | סעיף א |
    | ‏\( a = d = 0.1 \) | ‏0.270 | האדם ה-3 | ‏\( 12 \ge 10 \) |
    | ‏\( a = d = 0.01 \) | ‏0.095 | האדם ה-10 | ‏\( 110 \ge 100 \) |
    | ‏\( a = d = 1/12 \) | ‏0.250 | תיקו בין ה-3 ל-4 | ‏\( 12 = 12 \) |

    **נסו בעצמכם.** הזיזו את \( a \) ואת \( d \), וראו איך הפסגה זזה. הנוסחה והעמודות
    מסכימות בכל התחום:

    <div class="explorer" data-kind="cake-arith" data-a="0.01" data-step="0.1"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: האחרון מקבל הכי הרבה"
    לאדם האחרון יש השבר הגדול ביותר, הוא לוקח את כל מה שנשאר. אבל בסעיף א נשאר לו רק
    \( 0.0003 \) מהעוגה. שבר גדול של כמעט כלום הוא כמעט כלום.

??? trap "מלכודת: שבר מהעוגה או שבר ממה שנשאר"
    אם כל אחד היה לוקח \( p_k \) **מהעוגה כולה**, החלק שלו היה פשוט \( p_k \), והחלק הגדול
    היה של מי שהשבר שלו הכי גדול, כל עוד נשארה עוגה. כאן השבר הוא ממה שנשאר, ולכן החלק הוא
    \( p_k R_k \), ושני הגורמים זזים בכיוונים הפוכים.

??? trap "מלכודת: לשכוח את התיקו"
    כש-\( p_k = T \) בדיוק, היחס \( S_{k+1} / S_k \) שווה ל-1, ושני אנשים מקבלים את אותו
    חלק. למשל עם \( a = d = 1/12 \): ‏\( p_3 = 1/4 = T \), והאדם השלישי והרביעי מקבלים כל
    אחד \( 0.191 \). התשובה "האדם השלישי" לבד חסרה.

??? trap "מלכודת: טעות של אחד באינדקס"
    התנאי \( p_k < T \) משווה את האדם ה-\( k \) לאדם **שאחריו**. לכן הפסגה היא אצל האדם
    הראשון שהשבר **שלו** מגיע לסף, ולא אצל האחרון שמתחתיו. בסעיף א: ‏\( p_3 < T \le p_4 \),
    והתשובה היא 4 ולא 3.

??? trap "מלכודת: לעגל את הסף מוקדם מדי"
    כשהשבר קרוב לסף, \( T \approx 0.27 \) לא מספיק כדי להחליט. מחשבים בדיוק, או בודקים
    את הסימן של \( p_k^2 + d\,p_k - d \) ישירות, בלי שורשים.

??? followup "שאלות המשך"
    - **‏\( a = d \) קטן מאוד:** מי מקבל הכי הרבה כש-\( a = d = 0.0001 \)? ‏(האדם ה-100, כי
      \( 99 \cdot 100 < 10{,}000 \le 100 \cdot 101 \).)
    - **הסף בקצוות:** מה קורה ל-\( T \) כש-\( d \to 0 \) וכש-\( d \to \infty \)? למה הוא תמיד
      קטן מ-1? ‏(‏\( T \approx \sqrt{d} \) כש-\( d \) קטן, ו-\( T \to 1 \) כש-\( d \) גדל.)
    - **קפיצה של יותר מחצי:** נסו \( a = 0.55 \) ו-\( d = 0.8 \). הנוסחה נותנת את האדם השני,
      אבל הוא מקבל \( 0.45 \) והראשון \( 0.55 \). מה השתבש, ואיך מתקנים את הנוסחה?
    - **שברים שלא עולים:** מה קורה כש-\( d \le 0 \)? ‏(האדם הראשון מקבל הכי הרבה, כי גם השבר
      וגם מה שנשאר רק קטנים או נשארים.)
    - **כמה אנשים בסך הכול:** הראו שמספר האנשים הוא \( \left\lceil \frac{1 - a}{d} \right\rceil + 1 \),
      ובדקו שבסעיף א יוצא 11.
    - **סדרה הנדסית:** מה משתנה כשהשברים עולים פי \( q \) בכל פעם? זו
      [שאלה 0028](0028-cake-geometric-fractions.md).
