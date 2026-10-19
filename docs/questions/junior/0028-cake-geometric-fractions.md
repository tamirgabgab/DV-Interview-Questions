---
id: 28
title: חלוקת עוגה בסדרה הנדסית – מי מקבל הכי הרבה?
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
- **האדם ה-\( k \)** לוקח את השבר \( p_k = a\,q^{k-1} \) ממה שנשאר אחרי כל מי שלפניו.
  השברים עולים בסדרה הנדסית עם מנה \( q > 1 \).
- **הסוף:** אדם שהשבר שלו מגיע ל-1 או עובר אותו לוקח את כל מה שנשאר, והחלוקה נגמרת.

בשרטוט יש דוגמה עם \( a = 0.1 \) ו-\( q = 2 \). כל שורה היא העוגה ברגע שאדם אחד מגיע
אליה: השבר שהוא לוקח מוכפל משורה לשורה, אבל מה שנשאר לחתוך ממנו קטן. האדם החמישי היה
אמור לקחת \( 1.6 \), ולכן הוא לוקח את כל השארית. בפס התחתון כל הפרוסות במקומן:

<svg class="figure" viewBox="0 0 640 241" style="max-width:40rem" role="img" aria-label="חלוקת העוגה, שורה לכל אדם: כמה נשאר כשהוא מגיע והפרוסה שהוא חותך, ובסוף כל העוגה עם הפרוסות של כל 5 האנשים"><rect class="cake-gone" x="52" y="8" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="8" width="441.0" height="24"/><rect class="cake-slice" x="493.0" y="8" width="49.0" height="24"><title>אדם 1: p = 0.1, S = 0.1000</title></rect><text class="legend" x="40" y="25" text-anchor="end" style="font-size:17px">1</text><text class="tick" x="548.0" y="24" style="font-size:15px">p = 0.1</text><rect class="cake-gone" x="52" y="41" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="41" width="352.8" height="24"/><rect class="cake-slice2" x="404.8" y="41" width="88.2" height="24"><title>אדם 2: p = 0.2, S = 0.1800</title></rect><text class="legend" x="40" y="58" text-anchor="end" style="font-size:17px">2</text><text class="tick" x="499.0" y="57" style="font-size:15px">p = 0.2</text><rect class="cake-gone" x="52" y="74" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="74" width="211.7" height="24"/><rect class="cake-slice" x="263.7" y="74" width="141.1" height="24"><title>אדם 3: p = 0.4, S = 0.2880</title></rect><text class="legend" x="40" y="91" text-anchor="end" style="font-size:17px">3</text><text class="tick" x="410.8" y="90" style="font-size:15px">p = 0.4</text><rect class="cake-gone" x="52" y="107" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="107" width="42.3" height="24"/><rect class="cake-slice2" x="94.3" y="107" width="169.3" height="24"><title>אדם 4: p = 0.8, S = 0.3456</title></rect><text class="legend" x="40" y="124" text-anchor="end" style="font-size:17px">4</text><text class="tick" x="269.7" y="123" style="font-size:15px">p = 0.8</text><rect class="cake-gone" x="52" y="140" width="490" height="24" rx="3"/><rect class="cake-slice" x="52.0" y="140" width="42.3" height="24"><title>אדם 5: p = 1, S = 0.0864</title></rect><text class="legend" x="40" y="157" text-anchor="end" style="font-size:17px">5</text><text class="tick" x="100.3" y="156" style="font-size:15px">p = 1</text><rect class="cake-slice" x="493.0" y="191" width="49.0" height="24"/><text class="tick" x="517.5" y="233" text-anchor="middle" style="font-size:15px">1</text><rect class="cake-slice2" x="404.8" y="191" width="88.2" height="24"/><text class="tick" x="448.9" y="233" text-anchor="middle" style="font-size:15px">2</text><rect class="cake-slice" x="263.7" y="191" width="141.1" height="24"/><text class="tick" x="334.2" y="233" text-anchor="middle" style="font-size:15px">3</text><rect class="cake-slice2" x="94.3" y="191" width="169.3" height="24"/><text class="tick" x="179.0" y="233" text-anchor="middle" style="font-size:15px">4</text><rect class="cake-slice" x="52.0" y="191" width="42.3" height="24"/><text class="tick" x="73.2" y="233" text-anchor="middle" style="font-size:15px">5</text><rect class="cake-edge" x="52" y="191" width="490" height="24" rx="3"/></svg>

<span class="viz-legend"><span><i class="cake-slice"></i><i class="cake-slice2"></i>הפרוסה של האדם, בשני גוונים לסירוגין</span><span><i class="cake-rest"></i>נשאר לבאים אחריו</span><span><i class="cake-gone"></i>כבר נלקח</span></span>

מי מקבל את החלק הגדול ביותר של העוגה?

??? interviewer "מה המראיין בודק"
    - **מודל נכון:** להבחין בין שבר מהעוגה לשבר ממה שנשאר, ולכתוב את החלק של כל אדם בעזרת
      מה שנשאר לפניו.
    - **השוואה בין שכנים:** להשוות כל אדם לבא אחריו, ולראות שבסדרה הנדסית היחס יוצא פשוט
      מאוד.
    - **לוגריתמים:** לפתור אי-שוויון מעריכי ולעגל לכיוון הנכון.
    - **הוכחה ולא רק חישוב:** להראות שהחלקים עולים ואחר כך רק יורדים, ולא לשכוח את התיקו.

---

### סעיף א – הצבה מספרית

כאן \( a = 0.01 \) ו-\( q = 1.5 \), ולכן השברים הם \( 0.01, 0.015, 0.0225, \dots \), כל אחד גדול פי \( 1.5 \) מקודמו. מי מקבל את
החלק הגדול ביותר, וכמה הוא מקבל?

??? tip "רמז 1"
    שני כוחות מושכים לכיוונים הפוכים: השבר גדל, אבל מה שנשאר לחתוך ממנו קטן. סמנו ב-\( R_k \)
    את מה שנשאר לפני האדם ה-\( k \), וכתבו את החלק שלו \( S_k \) בעזרתו.

??? tip "רמז 2"
    השוו שני אנשים סמוכים: חשבו את היחס \( S_{k+1} / S_k \). עם \( p_{k+1} = q\,p_k \) כמעט
    הכול מצטמצם.

??? tip "רמז 3"
    היחס יוצא \( q(1 - p_k) \). מתי הוא גדול מ-1? פתרו את התנאי על \( p_k \), ואז מצאו את
    האדם הראשון שעובר את הסף, בעזרת לוגריתם.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        האדם העשירי, עם בערך \( 0.170 \) מהעוגה, כלומר 17%.

    #### הרעיון { .sol-idea }

    בהתחלה השבר גדל מהר יותר ממה שהעוגה נגמרת, ולכן כל אדם מקבל יותר מקודמו. אחר כך העוגה
    נגמרת מהר יותר, והחלקים קטנים. משווים כל אדם לבא אחריו: בסדרה הנדסית היחס ביניהם הוא
    פשוט \( q(1 - p_k) \), והאדם הבא מקבל יותר כל עוד \( p_k < 1 - \frac1q = \frac13 \).
    החלק הגדול ביותר הוא של **האדם הראשון שהשבר שלו מגיע לשליש**:

    <svg class="perf-chart" viewBox="0 0 640 250" role="img" aria-label="החלק של כל אדם. הגדול ביותר הוא של האדם ה-10, בערך 0.170 מהעוגה"><line class="grid" x1="46" x2="628" y1="216.0" y2="216.0"/><text class="tick" x="38" y="220.0" text-anchor="end">0.00</text><line class="grid" x1="46" x2="628" y1="167.5" y2="167.5"/><text class="tick" x="38" y="171.5" text-anchor="end">0.05</text><line class="grid" x1="46" x2="628" y1="119.0" y2="119.0"/><text class="tick" x="38" y="123.0" text-anchor="end">0.10</text><line class="grid" x1="46" x2="628" y1="70.5" y2="70.5"/><text class="tick" x="38" y="74.5" text-anchor="end">0.15</text><line class="grid" x1="46" x2="628" y1="22.0" y2="22.0"/><text class="tick" x="38" y="26.0" text-anchor="end">0.20</text><rect class="bar by-multiples" x="53.2" y="206.3" width="30.4" height="9.7" rx="2"><title>S(1) = 0.0100</title></rect><text class="tick" x="68.4" y="201.3" text-anchor="middle">0.010</text><text class="tick" x="68.4" y="234" text-anchor="middle">1</text><rect class="bar by-multiples" x="97.9" y="201.6" width="30.4" height="14.4" rx="2"><title>S(2) = 0.0149</title></rect><text class="tick" x="113.2" y="196.6" text-anchor="middle">0.015</text><text class="tick" x="113.2" y="234" text-anchor="middle">2</text><rect class="bar by-multiples" x="142.7" y="194.7" width="30.4" height="21.3" rx="2"><title>S(3) = 0.0219</title></rect><text class="tick" x="157.9" y="189.7" text-anchor="middle">0.022</text><text class="tick" x="157.9" y="234" text-anchor="middle">3</text><rect class="bar by-multiples" x="187.5" y="184.8" width="30.4" height="31.2" rx="2"><title>S(4) = 0.0322</title></rect><text class="tick" x="202.7" y="179.8" text-anchor="middle">0.032</text><text class="tick" x="202.7" y="234" text-anchor="middle">4</text><rect class="bar by-multiples" x="232.2" y="170.8" width="30.4" height="45.2" rx="2"><title>S(5) = 0.0466</title></rect><text class="tick" x="247.5" y="165.8" text-anchor="middle">0.047</text><text class="tick" x="247.5" y="234" text-anchor="middle">5</text><rect class="bar by-multiples" x="277.0" y="151.6" width="30.4" height="64.4" rx="2"><title>S(6) = 0.0664</title></rect><text class="tick" x="292.2" y="146.6" text-anchor="middle">0.066</text><text class="tick" x="292.2" y="234" text-anchor="middle">6</text><rect class="bar by-multiples" x="321.8" y="126.7" width="30.4" height="89.3" rx="2"><title>S(7) = 0.0920</title></rect><text class="tick" x="337.0" y="121.7" text-anchor="middle">0.092</text><text class="tick" x="337.0" y="234" text-anchor="middle">7</text><rect class="bar by-multiples" x="366.5" y="97.3" width="30.4" height="118.7" rx="2"><title>S(8) = 0.1223</title></rect><text class="tick" x="381.8" y="92.3" text-anchor="middle">0.122</text><text class="tick" x="381.8" y="234" text-anchor="middle">8</text><rect class="bar by-multiples" x="411.3" y="68.4" width="30.4" height="147.6" rx="2"><title>S(9) = 0.1521</title></rect><text class="tick" x="426.5" y="63.4" text-anchor="middle">0.152</text><text class="tick" x="426.5" y="234" text-anchor="middle">9</text><rect class="bar by-enum" x="456.1" y="51.4" width="30.4" height="164.6" rx="2"><title>S(10) = 0.1697</title></rect><text class="tick" x="471.3" y="46.4" text-anchor="middle">0.170</text><text class="tick" x="471.3" y="234" text-anchor="middle">10</text><rect class="bar by-multiples" x="500.9" y="64.0" width="30.4" height="152.0" rx="2"><title>S(11) = 0.1567</title></rect><text class="tick" x="516.1" y="59.0" text-anchor="middle">0.157</text><text class="tick" x="516.1" y="234" text-anchor="middle">11</text><rect class="bar by-multiples" x="545.6" y="119.5" width="30.4" height="96.5" rx="2"><title>S(12) = 0.0995</title></rect><text class="tick" x="560.8" y="114.5" text-anchor="middle">0.100</text><text class="tick" x="560.8" y="234" text-anchor="middle">12</text><rect class="bar by-multiples" x="590.4" y="200.9" width="30.4" height="15.1" rx="2"><title>S(13) = 0.0155</title></rect><text class="tick" x="605.6" y="195.9" text-anchor="middle">0.016</text><text class="tick" x="605.6" y="234" text-anchor="middle">13</text><line class="axis" x1="46" x2="628" y1="216" y2="216"/><text class="tick" x="38" y="234" text-anchor="end">k</text></svg>

    <span class="viz-legend"><span><i class="by-multiples"></i>‏\( S_k \), החלק של האדם ה-\( k \)</span><span><i class="by-enum"></i>החלק הגדול ביותר</span></span>

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סימונים:** ‏\( R_k \) הוא מה שנשאר מהעוגה לפני האדם ה-\( k \), עם \( R_1 = 1 \).
       האדם לוקח \( p_k \) ממנו, והשאר עובר הלאה:

        \[
        S_k = p_k R_k, \qquad R_{k+1} = (1 - p_k) R_k
        \]

    2. **היחס בין שכנים:** מה שנשאר מצטמצם, ועם \( p_{k+1} = q\,p_k \) מצטמצם גם השבר:

        \[
        \begin{aligned}
        \frac{S_{k+1}}{S_k} &= \frac{p_{k+1}(1 - p_k)}{p_k} \\
                            &= \frac{q\,p_k(1 - p_k)}{p_k} = q(1 - p_k)
        \end{aligned}
        \]

    3. **התנאי והסף:** האדם ה-\( k + 1 \) מקבל יותר בדיוק כשהיחס גדול מ-1:

        \[
        \begin{aligned}
        S_{k+1} > S_k &\iff q(1 - p_k) > 1 \\
                      &\iff p_k < 1 - \frac{1}{q} = \frac13
        \end{aligned}
        \]

    4. **מי עובר את הסף:** כופלים את שני האגפים ב-\( q / a \) ולוקחים לוגריתם:

        \[
        \begin{aligned}
                 & 0.01 \cdot 1.5^{k-1} \ge \tfrac13 \\
        \iff\quad & 1.5^{k} \ge 50 \\
        \iff\quad & k \ge \log_{1.5} 50 \approx 9.65
        \end{aligned}
        \]

        כי \( \frac{0.5}{0.01} = 50 \) ו-\( \log_{1.5} 50 = \frac{\ln 50}{\ln 1.5} \). לכן
        \( k = \lceil 9.65 \rceil = 10 \).

    5. **בדיקה ישירה:** ‏\( p_9 = 0.01 \cdot 1.5^8 \approx 0.256 < \tfrac13 \), ולכן
       \( S_{10} > S_9 \). ‏\( p_{10} = 0.01 \cdot 1.5^9 \approx 0.384 \ge \tfrac13 \), ולכן
       \( S_{11} < S_{10} \).

    6. **החלק שלו:** לפני האדם העשירי נשאר \( R_{10} \approx 0.4415 \), והוא לוקח ממנו
       \( 0.3844 \): ‏\( S_{10} \approx 0.3844 \cdot 0.4415 \approx 0.1697 \).

    </div>

    בגרף, כל עמוד הוא השבר של אדם אחד, והקו המקווקו הוא הסף \( \tfrac13 \). העמודים הכחולים
    מתחת לסף: אחרי כל אחד מהם בא אדם שמקבל יותר. הראשון שמגיע לסף הוא האדם העשירי:

    <svg class="perf-chart" viewBox="0 0 640 250" role="img" aria-label="השבר של כל אדם מול הסף T, בערך 0.333. הראשון שמגיע לסף הוא האדם ה-10"><line class="grid" x1="46" x2="628" y1="216.0" y2="216.0"/><text class="tick" x="38" y="220.0" text-anchor="end">0</text><line class="grid" x1="46" x2="628" y1="166.0" y2="166.0"/><text class="tick" x="38" y="170.0" text-anchor="end">0.25</text><line class="grid" x1="46" x2="628" y1="116.0" y2="116.0"/><text class="tick" x="38" y="120.0" text-anchor="end">0.5</text><line class="grid" x1="46" x2="628" y1="66.0" y2="66.0"/><text class="tick" x="38" y="70.0" text-anchor="end">0.75</text><line class="grid" x1="46" x2="628" y1="16.0" y2="16.0"/><text class="tick" x="38" y="20.0" text-anchor="end">1</text><line class="ink-line" x1="46" x2="628" y1="149.3" y2="149.3" stroke-width="1.5" stroke-dasharray="6 4"/><text class="legend" x="52" y="143.3">T ≈ 0.333</text><line class="s1-line" x1="68.4" x2="68.4" y1="216" y2="214.0" stroke-width="2"/><circle class="s1-dot" cx="68.4" cy="214.0" r="4.5"><title>p(1) = 0.0100</title></circle><text class="tick" x="68.4" y="234" text-anchor="middle">1</text><line class="s1-line" x1="113.2" x2="113.2" y1="216" y2="213.0" stroke-width="2"/><circle class="s1-dot" cx="113.2" cy="213.0" r="4.5"><title>p(2) = 0.0150</title></circle><text class="tick" x="113.2" y="234" text-anchor="middle">2</text><line class="s1-line" x1="157.9" x2="157.9" y1="216" y2="211.5" stroke-width="2"/><circle class="s1-dot" cx="157.9" cy="211.5" r="4.5"><title>p(3) = 0.0225</title></circle><text class="tick" x="157.9" y="234" text-anchor="middle">3</text><line class="s1-line" x1="202.7" x2="202.7" y1="216" y2="209.2" stroke-width="2"/><circle class="s1-dot" cx="202.7" cy="209.2" r="4.5"><title>p(4) = 0.0338</title></circle><text class="tick" x="202.7" y="234" text-anchor="middle">4</text><line class="s1-line" x1="247.5" x2="247.5" y1="216" y2="205.9" stroke-width="2"/><circle class="s1-dot" cx="247.5" cy="205.9" r="4.5"><title>p(5) = 0.0506</title></circle><text class="tick" x="247.5" y="234" text-anchor="middle">5</text><line class="s1-line" x1="292.2" x2="292.2" y1="216" y2="200.8" stroke-width="2"/><circle class="s1-dot" cx="292.2" cy="200.8" r="4.5"><title>p(6) = 0.0759</title></circle><text class="tick" x="292.2" y="234" text-anchor="middle">6</text><line class="s1-line" x1="337.0" x2="337.0" y1="216" y2="193.2" stroke-width="2"/><circle class="s1-dot" cx="337.0" cy="193.2" r="4.5"><title>p(7) = 0.1139</title></circle><text class="tick" x="337.0" y="234" text-anchor="middle">7</text><line class="s1-line" x1="381.8" x2="381.8" y1="216" y2="181.8" stroke-width="2"/><circle class="s1-dot" cx="381.8" cy="181.8" r="4.5"><title>p(8) = 0.1709</title></circle><text class="tick" x="381.8" y="234" text-anchor="middle">8</text><line class="s1-line" x1="426.5" x2="426.5" y1="216" y2="164.7" stroke-width="2"/><circle class="s1-dot" cx="426.5" cy="164.7" r="4.5"><title>p(9) = 0.2563</title></circle><text class="tick" x="426.5" y="234" text-anchor="middle">9</text><line class="s2-line" x1="471.3" x2="471.3" y1="216" y2="139.1" stroke-width="2"/><circle class="s2-dot" cx="471.3" cy="139.1" r="6"><title>p(10) = 0.3844</title></circle><text class="tick" x="471.3" y="234" text-anchor="middle">10</text><line class="ink-line" x1="516.1" x2="516.1" y1="216" y2="100.7" stroke-width="2"/><circle class="ink-dot" cx="516.1" cy="100.7" r="4.5"><title>p(11) = 0.5767</title></circle><text class="tick" x="516.1" y="234" text-anchor="middle">11</text><line class="ink-line" x1="560.8" x2="560.8" y1="216" y2="43.0" stroke-width="2"/><circle class="ink-dot" cx="560.8" cy="43.0" r="4.5"><title>p(12) = 0.8650</title></circle><text class="tick" x="560.8" y="234" text-anchor="middle">12</text><line class="ink-line" x1="605.6" x2="605.6" y1="216" y2="16.0" stroke-width="2"/><circle class="ink-dot" cx="605.6" cy="16.0" r="4.5"><title>p(13) = 1.0000</title></circle><text class="tick" x="605.6" y="234" text-anchor="middle">13</text><line class="axis" x1="46" x2="628" y1="216" y2="216"/><text class="tick" x="38" y="234" text-anchor="end">k</text></svg>

    <span class="viz-legend"><span><i class="s1"></i>מתחת לסף: הבא אחריו מקבל יותר</span><span><i class="s2"></i>הראשון שמגיע לסף: החלק הגדול ביותר</span><span><i class="ink"></i>מעל הסף</span><span><i class="ink-dash"></i>הסף \( T \)</span></span>

    #### למה זה נכון { .sol-proof }

    **היחס על גרף.** הנקודה ב-\( k \) היא היחס \( S_{k+1} / S_k = q(1 - p_k) \). הוא מתחיל
    קרוב ל-\( 1.5 \) ויורד, כי \( p_k \) גדל. כל עוד הנקודה מעל הקו \( y = 1 \), האדם הבא
    מקבל יותר. הנקודה הראשונה מתחת לקו היא אצל האדם העשירי:

    <svg class="perf-chart" viewBox="0 0 640 250" role="img" aria-label="היחס בין החלק של האדם הבא לחלק של האדם הנוכחי. הוא יורד מתחת ל-1 לראשונה אצל האדם ה-10"><line class="grid" x1="46" x2="628" y1="216.0" y2="216.0"/><text class="tick" x="38" y="220.0" text-anchor="end">0</text><line class="grid" x1="46" x2="628" y1="149.3" y2="149.3"/><text class="tick" x="38" y="153.3" text-anchor="end">0.5</text><line class="grid" x1="46" x2="628" y1="82.7" y2="82.7"/><text class="tick" x="38" y="86.7" text-anchor="end">1</text><line class="grid" x1="46" x2="628" y1="16.0" y2="16.0"/><text class="tick" x="38" y="20.0" text-anchor="end">1.5</text><line class="ink-line" x1="46" x2="628" y1="82.7" y2="82.7" stroke-width="1.5" stroke-dasharray="6 4"/><polyline class="s1-line" points="68.4,18.0 113.2,19.0 157.9,20.5 202.7,22.8 247.5,26.1 292.2,31.2 337.0,38.8 381.8,50.2 426.5,67.3 471.3,92.9 516.1,131.3 560.8,195.2" fill="none" stroke-width="1.5"/><circle class="s1-dot" cx="68.4" cy="18.0" r="4.5"><title>S(2) / S(1) = 1.485</title></circle><circle class="s1-dot" cx="113.2" cy="19.0" r="4.5"><title>S(3) / S(2) = 1.478</title></circle><circle class="s1-dot" cx="157.9" cy="20.5" r="4.5"><title>S(4) / S(3) = 1.466</title></circle><circle class="s1-dot" cx="202.7" cy="22.8" r="4.5"><title>S(5) / S(4) = 1.449</title></circle><circle class="s1-dot" cx="247.5" cy="26.1" r="4.5"><title>S(6) / S(5) = 1.424</title></circle><circle class="s1-dot" cx="292.2" cy="31.2" r="4.5"><title>S(7) / S(6) = 1.386</title></circle><circle class="s1-dot" cx="337.0" cy="38.8" r="4.5"><title>S(8) / S(7) = 1.329</title></circle><circle class="s1-dot" cx="381.8" cy="50.2" r="4.5"><title>S(9) / S(8) = 1.244</title></circle><circle class="s1-dot" cx="426.5" cy="67.3" r="4.5"><title>S(10) / S(9) = 1.116</title></circle><circle class="s2-dot" cx="471.3" cy="92.9" r="6"><title>S(11) / S(10) = 0.923</title></circle><circle class="s1-dot" cx="516.1" cy="131.3" r="4.5"><title>S(12) / S(11) = 0.635</title></circle><circle class="ink-dot" cx="560.8" cy="195.2" r="4.5"><title>S(13) / S(12) = 0.156</title></circle><text class="tick" x="68.4" y="234" text-anchor="middle">1</text><text class="tick" x="113.2" y="234" text-anchor="middle">2</text><text class="tick" x="157.9" y="234" text-anchor="middle">3</text><text class="tick" x="202.7" y="234" text-anchor="middle">4</text><text class="tick" x="247.5" y="234" text-anchor="middle">5</text><text class="tick" x="292.2" y="234" text-anchor="middle">6</text><text class="tick" x="337.0" y="234" text-anchor="middle">7</text><text class="tick" x="381.8" y="234" text-anchor="middle">8</text><text class="tick" x="426.5" y="234" text-anchor="middle">9</text><text class="tick" x="471.3" y="234" text-anchor="middle">10</text><text class="tick" x="516.1" y="234" text-anchor="middle">11</text><text class="tick" x="560.8" y="234" text-anchor="middle">12</text><line class="axis" x1="46" x2="628" y1="216" y2="216"/><text class="tick" x="38" y="234" text-anchor="end">k</text></svg>

    <span class="viz-legend"><span><i class="s1"></i>היחס \( S_{k+1} / S_k \)</span><span><i class="s2"></i>הפעם הראשונה מתחת ל-1</span><span><i class="ink"></i>היחס אל מי שלוקח את השארית</span><span><i class="ink-dash"></i>הקו \( y = 1 \)</span></span>

    **העוגה עצמה.** אותה חלוקה בשורות, עם הפרוסה של האדם העשירי מודגשת. תשעת האנשים
    הראשונים לוקחים יחד פחות מ-60% מהעוגה, ומשם השבר קופץ מהר:

    <svg class="figure" viewBox="0 0 640 505" style="max-width:40rem" role="img" aria-label="חלוקת העוגה, שורה לכל אדם: כמה נשאר כשהוא מגיע והפרוסה שהוא חותך, ובסוף כל העוגה עם הפרוסות של כל 13 האנשים"><rect class="cake-gone" x="52" y="8" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="8" width="485.1" height="24"/><rect class="cake-slice" x="537.1" y="8" width="4.9" height="24"><title>אדם 1: p = 0.01, S = 0.0100</title></rect><text class="legend" x="40" y="25" text-anchor="end" style="font-size:17px">1</text><text class="tick" x="548.0" y="24" style="font-size:15px">p = 0.01</text><rect class="cake-gone" x="52" y="41" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="41" width="477.8" height="24"/><rect class="cake-slice2" x="529.8" y="41" width="7.3" height="24"><title>אדם 2: p = 0.015, S = 0.0149</title></rect><text class="legend" x="40" y="58" text-anchor="end" style="font-size:17px">2</text><text class="tick" x="543.1" y="57" style="font-size:15px">p = 0.015</text><rect class="cake-gone" x="52" y="74" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="74" width="467.1" height="24"/><rect class="cake-slice" x="519.1" y="74" width="10.8" height="24"><title>אדם 3: p = 0.0225, S = 0.0219</title></rect><text class="legend" x="40" y="91" text-anchor="end" style="font-size:17px">3</text><text class="tick" x="535.8" y="90" style="font-size:15px">p = 0.0225</text><rect class="cake-gone" x="52" y="107" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="107" width="451.3" height="24"/><rect class="cake-slice2" x="503.3" y="107" width="15.8" height="24"><title>אדם 4: p = 0.0338, S = 0.0322</title></rect><text class="legend" x="40" y="124" text-anchor="end" style="font-size:17px">4</text><text class="tick" x="525.1" y="123" style="font-size:15px">p = 0.0338</text><rect class="cake-gone" x="52" y="140" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="140" width="428.5" height="24"/><rect class="cake-slice" x="480.5" y="140" width="22.8" height="24"><title>אדם 5: p = 0.0506, S = 0.0466</title></rect><text class="legend" x="40" y="157" text-anchor="end" style="font-size:17px">5</text><text class="tick" x="509.3" y="156" style="font-size:15px">p = 0.0506</text><rect class="cake-gone" x="52" y="173" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="173" width="395.9" height="24"/><rect class="cake-slice2" x="447.9" y="173" width="32.5" height="24"><title>אדם 6: p = 0.0759, S = 0.0664</title></rect><text class="legend" x="40" y="190" text-anchor="end" style="font-size:17px">6</text><text class="tick" x="486.5" y="189" style="font-size:15px">p = 0.0759</text><rect class="cake-gone" x="52" y="206" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="206" width="350.8" height="24"/><rect class="cake-slice" x="402.8" y="206" width="45.1" height="24"><title>אדם 7: p = 0.1139, S = 0.0920</title></rect><text class="legend" x="40" y="223" text-anchor="end" style="font-size:17px">7</text><text class="tick" x="453.9" y="222" style="font-size:15px">p = 0.1139</text><rect class="cake-gone" x="52" y="239" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="239" width="290.9" height="24"/><rect class="cake-slice2" x="342.9" y="239" width="59.9" height="24"><title>אדם 8: p = 0.1709, S = 0.1223</title></rect><text class="legend" x="40" y="256" text-anchor="end" style="font-size:17px">8</text><text class="tick" x="408.8" y="255" style="font-size:15px">p = 0.1709</text><rect class="cake-gone" x="52" y="272" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="272" width="216.3" height="24"/><rect class="cake-slice" x="268.3" y="272" width="74.6" height="24"><title>אדם 9: p = 0.2563, S = 0.1521</title></rect><text class="legend" x="40" y="289" text-anchor="end" style="font-size:17px">9</text><text class="tick" x="348.9" y="288" style="font-size:15px">p = 0.2563</text><rect class="cake-gone" x="52" y="305" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="305" width="133.2" height="24"/><rect class="cake-peak" x="185.2" y="305" width="83.2" height="24"><title>אדם 10: p = 0.3844, S = 0.1697</title></rect><text class="legend" x="40" y="322" text-anchor="end" style="font-size:17px">10</text><text class="tick" x="274.3" y="321" style="font-size:15px">p = 0.3844</text><rect class="cake-gone" x="52" y="338" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="338" width="56.4" height="24"/><rect class="cake-slice" x="108.4" y="338" width="76.8" height="24"><title>אדם 11: p = 0.5767, S = 0.1567</title></rect><text class="legend" x="40" y="355" text-anchor="end" style="font-size:17px">11</text><text class="tick" x="191.2" y="354" style="font-size:15px">p = 0.5767</text><rect class="cake-gone" x="52" y="371" width="490" height="24" rx="3"/><rect class="cake-rest" x="52" y="371" width="7.6" height="24"/><rect class="cake-slice2" x="59.6" y="371" width="48.8" height="24"><title>אדם 12: p = 0.865, S = 0.0995</title></rect><text class="legend" x="40" y="388" text-anchor="end" style="font-size:17px">12</text><text class="tick" x="114.4" y="387" style="font-size:15px">p = 0.865</text><rect class="cake-gone" x="52" y="404" width="490" height="24" rx="3"/><rect class="cake-slice" x="52.0" y="404" width="7.6" height="24"><title>אדם 13: p = 1, S = 0.0155</title></rect><text class="legend" x="40" y="421" text-anchor="end" style="font-size:17px">13</text><text class="tick" x="65.6" y="420" style="font-size:15px">p = 1</text><rect class="cake-slice" x="537.1" y="455" width="4.9" height="24"/><rect class="cake-slice2" x="529.8" y="455" width="7.3" height="24"/><rect class="cake-slice" x="519.1" y="455" width="10.8" height="24"/><rect class="cake-slice2" x="503.3" y="455" width="15.8" height="24"/><rect class="cake-slice" x="480.5" y="455" width="22.8" height="24"/><text class="tick" x="491.9" y="497" text-anchor="middle" style="font-size:15px">5</text><rect class="cake-slice2" x="447.9" y="455" width="32.5" height="24"/><text class="tick" x="464.2" y="497" text-anchor="middle" style="font-size:15px">6</text><rect class="cake-slice" x="402.8" y="455" width="45.1" height="24"/><text class="tick" x="425.4" y="497" text-anchor="middle" style="font-size:15px">7</text><rect class="cake-slice2" x="342.9" y="455" width="59.9" height="24"/><text class="tick" x="372.9" y="497" text-anchor="middle" style="font-size:15px">8</text><rect class="cake-slice" x="268.3" y="455" width="74.6" height="24"/><text class="tick" x="305.6" y="497" text-anchor="middle" style="font-size:15px">9</text><rect class="cake-peak" x="185.2" y="455" width="83.2" height="24"/><text class="tick" x="226.8" y="497" text-anchor="middle" style="font-size:15px">10</text><rect class="cake-slice" x="108.4" y="455" width="76.8" height="24"/><text class="tick" x="146.8" y="497" text-anchor="middle" style="font-size:15px">11</text><rect class="cake-slice2" x="59.6" y="455" width="48.8" height="24"/><text class="tick" x="84.0" y="497" text-anchor="middle" style="font-size:15px">12</text><rect class="cake-slice" x="52.0" y="455" width="7.6" height="24"/><rect class="cake-edge" x="52" y="455" width="490" height="24" rx="3"/></svg>

    <span class="viz-legend"><span><i class="cake-slice"></i><i class="cake-slice2"></i>הפרוסה של האדם, בשני גוונים לסירוגין</span><span><i class="cake-peak"></i>הפרוסה הגדולה ביותר</span><span><i class="cake-rest"></i>נשאר לבאים אחריו</span><span><i class="cake-gone"></i>כבר נלקח</span></span>

    **כל המספרים.** הטבלה מאשרת: החלקים עולים עד האדם העשירי ויורדים אחריו. האדם ה-13
    היה אמור לקחת \( 1.3 \) ממה שנשאר, ולכן הוא לוקח את כל השארית:

    | האדם \( k \) | השבר \( p_k \) | נשאר לפניו \( R_k \) | מקבל \( S_k \) |
    |---|---|---|---|
    | 1 | 0.01 | 1 | 0.0100 |
    | 2 | 0.015 | 0.9900 | 0.0149 |
    | 3 | 0.0225 | 0.9752 | 0.0219 |
    | 4 | 0.0338 | 0.9532 | 0.0322 |
    | 5 | 0.0506 | 0.9210 | 0.0466 |
    | 6 | 0.0759 | 0.8744 | 0.0664 |
    | 7 | 0.1139 | 0.8080 | 0.0920 |
    | 8 | 0.1709 | 0.7160 | 0.1223 |
    | 9 | 0.2563 | 0.5936 | 0.1521 |
    | **10** | **0.3844** | **0.4415** | **0.1697** |
    | 11 | 0.5767 | 0.2718 | 0.1567 |
    | 12 | 0.8650 | 0.1151 | 0.0995 |
    | 13 | 1, לוקח את השארית | 0.0155 | 0.0155 |

---

### סעיף ב – המקרה הכללי

עבור \( a > 0 \) ו-\( 1 < q \le 2 \) כלשהם, מצאו נוסחה לאדם שמקבל את החלק הגדול ביותר.
הוכיחו שיש פסגה אחת: החלקים עולים עד אדם מסוים, ואחריו רק יורדים. מתי יש תיקו?

ההנחה \( q \le 2 \) אומרת שהשבר לכל היותר מוכפל בין שני אנשים סמוכים. כש-\( q > 2 \)
התשובה תלויה גם ב-\( a \), ונחזור לזה בשאלות ההמשך.

??? tip "רמז 1"
    היחס \( q(1 - p_k) \) מסעיף א לא תלוי במספרים. מה קורה לו כש-\( k \) גדל?

??? tip "רמז 2"
    מצאו את הסף כפונקציה של \( q \), ואז פתרו \( a\,q^{k-1} \ge T \) עם לוגריתם בבסיס \( q \).

??? tip "רמז 3"
    אל תשכחו את האדם האחרון: השבר שלו נחתך ל-1. בדקו שהחיתוך לא משנה את התשובה כש-\( q \le 2 \).

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        הסף הוא \( T = 1 - \dfrac{1}{q} \), והחלק הגדול ביותר הוא של האדם הראשון שהשבר שלו
        מגיע לסף:
        \( k = \max\left(1,\ \left\lceil \log_q \frac{q - 1}{a} \right\rceil\right) \).
        אם \( q^k = \frac{q - 1}{a} \) בדיוק, יש תיקו בינו לבין האדם שאחריו.

    #### הרעיון { .sol-idea }

    היחס בין שכנים הוא \( q(1 - p_k) \). כש-\( q > 1 \) השברים עולים, ולכן היחס רק יורד.
    ברגע שהוא יורד מתחת ל-1 הוא נשאר שם: החלקים עולים, ומאז רק יורדים. זו פסגה אחת, והיא
    אצל האדם הראשון שהשבר שלו מגיע לסף \( 1 - 1/q \), הנקודה שבה הקו \( q(1 - p) \) חוצה
    את 1.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **היחס:** כמו בסעיף א, לכל מי שאינו האחרון,

        \[
        \frac{S_{k+1}}{S_k} = q(1 - p_k)
        \]

    2. **פסגה אחת:** ‏\( p_k \) עולה עם \( k \), ולכן \( q(1 - p_k) \) יורד. כל עוד הוא
       גדול מ-1 החלקים גדלים. מהאדם הראשון שבו הוא 1 או פחות, הוא נשאר כזה, והחלקים רק
       קטנים. אם הוא שווה ל-1 בדיוק, אז \( S_{k+1} = S_k \): תיקו.

    3. **הסף:** ‏\( q(1 - p) = 1 \) בדיוק כש-\( p = T = 1 - \frac1q = \frac{q - 1}{q} \).
       הוא תמיד בין 0 ל-1, וכש-\( q \le 2 \) גם \( T \le \tfrac12 \).

    4. **האדם האחרון:** האדם \( L \) שלוקח את השארית מקבל את השבר 1 ולא \( q\,p_{L-1} \),
       ולכן היחס אליו הוא \( \frac{1 - p_{L-1}}{p_{L-1}} \). אם \( p_{L-1} < T \le \tfrac12 \),
       היחס הזה גדול מ-1, כמו שהתנאי אומר. אם \( p_{L-1} \ge T \), היחס קטן מהיחס בלי
       החיתוך, שכבר קטן מ-1 או שווה לו. בשני המקרים התשובה לא משתנה. גם התיקו נשאר: אם
       \( p_{L-1} = T \), אז \( q\,p_{L-1} = q - 1 \le 1 \), ולכן השבר של האחרון הוא בדיוק 1,
       בלי חיתוך.

    5. **מי עובר את הסף:** כופלים ב-\( q / a \) ולוקחים לוגריתם בבסיס \( q > 1 \):

        \[
        \begin{aligned}
        a\,q^{k-1} \ge \frac{q - 1}{q} &\iff q^k \ge \frac{q - 1}{a} \\
                                       &\iff k \ge \log_q \frac{q - 1}{a}
        \end{aligned}
        \]

    6. **הנוסחה:** ה-\( k \) הקטן ביותר שמקיים את זה הוא

        \[
        \begin{aligned}
        k &= \max\left(1,\ \left\lceil \log_q \frac{q - 1}{a} \right\rceil\right) \\
          &= \max\left(1,\ \left\lceil \frac{\ln \frac{q - 1}{a}}{\ln q} \right\rceil\right)
        \end{aligned}
        \]

        אם \( a \ge 1 - \frac1q \), האדם הראשון מקבל הכי הרבה. אם \( q^k = \frac{q - 1}{a} \)
        בדיוק, האדם ה-\( k \) והאדם ה-\( k + 1 \) מקבלים חלק שווה.

    </div>

    #### למה זה נכון { .sol-proof }

    **הסף בגרף.** כל קו הוא \( y = q(1 - p) \): הוא מתחיל ב-\( q \) כש-\( p = 0 \) ויורד
    ל-0 כש-\( p = 1 \). הוא חוצה את הקו \( y = 1 \) בדיוק ב-\( p = 1 - 1/q \): שליש עבור
    \( q = 1.5 \), וחצי עבור \( q = 2 \). על הקו של \( q = 1.5 \) מסומנים השברים של האנשים
    בסעיף א: תשעה מעל הקו, והעשירי הוא הראשון מתחתיו:

    <svg class="perf-chart" viewBox="0 0 640 260" role="img" aria-label="הקווים q כפול 1 פחות p מול הקו y = 1. הם נחתכים ב-p = 1 פחות 1 חלקי q: שליש עבור q = 1.5, וחצי עבור q = 2"><line class="grid" x1="46" x2="626" y1="226.0" y2="226.0"/><text class="tick" x="38" y="230.0" text-anchor="end">0</text><line class="grid" x1="46" x2="626" y1="175.5" y2="175.5"/><text class="tick" x="38" y="179.5" text-anchor="end">0.5</text><line class="grid" x1="46" x2="626" y1="125.0" y2="125.0"/><text class="tick" x="38" y="129.0" text-anchor="end">1</text><line class="grid" x1="46" x2="626" y1="74.6" y2="74.6"/><text class="tick" x="38" y="78.6" text-anchor="end">1.5</text><line class="grid" x1="46" x2="626" y1="24.1" y2="24.1"/><text class="tick" x="38" y="28.1" text-anchor="end">2</text><text class="tick" x="46.0" y="244" text-anchor="middle">0</text><text class="tick" x="191.0" y="244" text-anchor="middle">0.25</text><text class="tick" x="336.0" y="244" text-anchor="middle">0.5</text><text class="tick" x="481.0" y="244" text-anchor="middle">0.75</text><line class="ink-line" x1="46" x2="626" y1="125.0" y2="125.0" stroke-width="1.5" stroke-dasharray="6 4"/><line class="s1-line" x1="46.0" y1="74.6" x2="626.0" y2="226.0" stroke-width="2.5"/><text class="legend" x="54.0" y="68.6">q = 1.5</text><line class="ink-line" x1="239.3" x2="239.3" y1="125.0" y2="226" stroke-width="1" stroke-dasharray="3 3"/><circle class="ink-dot" cx="239.3" cy="125.0" r="3.5"/><text class="legend" x="245.3" y="220">1/3</text><line class="s3-line" x1="46.0" y1="24.1" x2="626.0" y2="226.0" stroke-width="2.5"/><text class="legend" x="54.0" y="18.1">q = 2</text><line class="ink-line" x1="336.0" x2="336.0" y1="125.0" y2="226" stroke-width="1" stroke-dasharray="3 3"/><circle class="ink-dot" cx="336.0" cy="125.0" r="3.5"/><text class="legend" x="342.0" y="220">1/2</text><circle class="s1-dot" cx="51.8" cy="76.1" r="4"><title>p(1) = 0.0100</title></circle><circle class="s1-dot" cx="54.7" cy="76.8" r="4"><title>p(2) = 0.0150</title></circle><circle class="s1-dot" cx="59.0" cy="78.0" r="4"><title>p(3) = 0.0225</title></circle><circle class="s1-dot" cx="65.6" cy="79.7" r="4"><title>p(4) = 0.0338</title></circle><circle class="s1-dot" cx="75.4" cy="82.2" r="4"><title>p(5) = 0.0506</title></circle><circle class="s1-dot" cx="90.0" cy="86.1" r="4"><title>p(6) = 0.0759</title></circle><circle class="s1-dot" cx="112.1" cy="91.8" r="4"><title>p(7) = 0.1139</title></circle><circle class="s1-dot" cx="145.1" cy="100.4" r="4"><title>p(8) = 0.1709</title></circle><circle class="s1-dot" cx="194.6" cy="113.4" r="4"><title>p(9) = 0.2563</title></circle><circle class="s2-dot" cx="269.0" cy="132.8" r="6"><title>p(10) = 0.3844</title></circle><circle class="ink-dot" cx="380.5" cy="161.9" r="4"><title>p(11) = 0.5767</title></circle><circle class="ink-dot" cx="547.7" cy="205.6" r="4"><title>p(12) = 0.8650</title></circle><line class="axis" x1="46" x2="626" y1="226" y2="226"/><text class="tick" x="626" y="244" text-anchor="end">p</text></svg>

    <span class="viz-legend"><span><i class="s1"></i>‏\( y = 1.5\,(1 - p) \)</span><span><i class="s3"></i>‏\( y = 2\,(1 - p) \)</span><span><i class="ink-dash"></i>הקו \( y = 1 \)</span><span><i class="s2"></i>האדם ה-10: הראשון מתחת לקו</span><span><i class="ink"></i>אחריו, גם הם מתחת לקו</span></span>

    **‏\( q \) אחרים.** עם \( a = 0.01 \), ככל ש-\( q \) קרוב יותר ל-1, הפסגה מגיעה מאוחר
    יותר והיא נמוכה ושטוחה יותר:

    | ‏\( q \) | הסף \( 1 - 1/q \) | ‏\( \log_q \frac{q - 1}{a} \) | המקבל הגדול | חלקו |
    |---|---|---|---|---|
    | ‏2 | ‏0.500 | ‏6.64 | האדם ה-7 | ‏0.313 |
    | ‏1.5 | ‏0.333 | ‏9.65 | האדם ה-10 | ‏0.170 |
    | ‏1.1 | ‏0.091 | ‏24.16 | האדם ה-25 | ‏0.040 |

    **תיקו.** עם \( a = 0.25 \) ו-\( q = 2 \): ‏\( \frac{q - 1}{a} = 4 = 2^2 \), ולכן
    \( k = 2 \) עם תיקו. אכן \( p_2 = 0.5 = T \), והאדם השני והשלישי מקבלים כל אחד \( 0.375 \).

    **נסו בעצמכם.** הזיזו את \( a \) ואת \( q \), וראו איך הפסגה זזה. הנוסחה והעמודות
    מסכימות בכל התחום:

    <div class="cake-explorer" data-kind="geo" data-a="0.01" data-step="1.5"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: האחרון מקבל הכי הרבה"
    לאדם האחרון יש השבר הגדול ביותר, הוא לוקח את כל מה שנשאר. אבל בסעיף א נשאר לו רק
    \( 0.0155 \) מהעוגה, פחות מעשירית מהחלק של האדם העשירי.

??? trap "מלכודת: שבר מהעוגה או שבר ממה שנשאר"
    אם כל אחד היה לוקח \( p_k \) **מהעוגה כולה**, החלק שלו היה פשוט \( p_k \), והחלק הגדול
    היה של מי שהשבר שלו הכי גדול, כל עוד נשארה עוגה. כאן השבר הוא ממה שנשאר, ולכן החלק הוא
    \( p_k R_k \), ושני הגורמים זזים בכיוונים הפוכים.

??? trap "מלכודת: לשכוח את התיקו"
    כש-\( q^k = \frac{q - 1}{a} \) בדיוק, הלוגריתם יוצא מספר שלם, והיחס \( q(1 - p_k) \) שווה
    ל-1. שני אנשים מקבלים את אותו חלק, כמו בדוגמה \( a = 0.25 \), \( q = 2 \).

??? trap "מלכודת: הלוגריתם הלא נכון"
    הסף הוא \( 1 - 1/q \) ולא 1. מי שפותר \( a\,q^{k-1} \ge 1 \) מוצא את האדם **האחרון**,
    זה שלוקח את השארית: ‏\( \lceil \log_{1.5} 100 \rceil + 1 = 13 \) במקום 10.

??? trap "מלכודת: עיגול של לוגריתם"
    ‏\( \log_{1.5} 50 \approx 9.65 \), ולכן מעגלים **למעלה** ל-10. אבל כשהתשובה המדויקת היא
    מספר שלם, זה מקרה התיקו, ומחשבון שמחזיר \( 7.0000001 \) במקום 7 יעגל למעלה ל-8. כשהלוגריתם
    קרוב למספר שלם, בודקים ישירות את \( q^k \) מול \( \frac{q - 1}{a} \).

??? followup "שאלות המשך"
    - **‏\( q \le 1 \):** מה קורה כשהשברים לא עולים? ‏(‏\( q(1 - p_k) < 1 \) תמיד, כי
      \( p_k > 0 \), ולכן האדם הראשון מקבל הכי הרבה.)
    - **‏\( q > 2 \):** נסו \( a = 0.6 \) ו-\( q = 3 \). הנוסחה נותנת את האדם השני, אבל הוא
      מקבל \( 0.4 \) והראשון \( 0.6 \). מה השתבש, ולמה זה קורה רק לחלק מערכי \( a \)?
    - **פסגה שטוחה:** הראו שכש-\( q \to 1 \) ההפרש בין החלק הגדול לחלקים של שכניו הולך
      ל-0. כמה אנשים מקבלים לפחות 90% מהחלק הגדול כש-\( q = 1.1 \)?
    - **כמה אנשים בסך הכול:** הראו שמספר האנשים הוא \( \left\lceil \log_q \frac1a \right\rceil + 1 \),
      ובדקו שבסעיף א יוצא 13.
    - **סדרה חשבונית:** מה משתנה כשהשברים עולים ב-\( d \) בכל פעם? זו
      [שאלה 0027](0027-cake-arithmetic-fractions.md).
