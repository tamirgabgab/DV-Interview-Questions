---
id: 29
title: שלושה מחוגים – כמה פעמים הם נפגשים ביממה?
level: junior
difficulty: medium
kind: puzzle
tags: [math, logic-puzzles]
source: ""
added: 2026-10-20
---

## השאלה

לשעון מחוגים יש שלושה מחוגים. כולם זזים ברציפות ובקצב קבוע, וגם מחוג השניות לא קופץ
משנייה לשנייה אלא מחליק :

- **מחוג השניות** מסיים סיבוב בדקה, כלומר ב-60 שניות.
- **מחוג הדקות** מסיים סיבוב בשעה, כלומר ב-3,600 שניות.
- **מחוג השעות** מסיים סיבוב ב-12 שעות, כלומר ב-43,200 שניות.

בשעה 00:00:00 שלושת המחוגים מצביעים על 12. **פגישה** היא רגע שבו שני מחוגים או יותר
מצביעים בדיוק לאותו כיוון.

??? interviewer "מה המראיין בודק"
    - **פירוק לזוגות :** לספור כל זוג מחוגים לחוד, ולא לנסות לעקוב אחרי שלושה בבת אחת.
    - **מהירות יחסית :** לראות שהמחוג המהיר "מקיף" את האיטי, ושמספר הפגישות הוא הפרש
      ההקפות.
    - **קצוות הקטע :** להחליט במפורש אם 00:00 נספר, ואם חצות של סוף היממה נספר.
    - **כפילויות :** לשים לב שרגע אחד יכול להיספר בכמה זוגות, ולהוכיח מתי זה קורה.

---

### סעיף א – כמה פגישות ביממה

כמה פעמים ביממה נפגשים לפחות שני מחוגים? היממה מתחילה ב-00:00:00 ונגמרת ב-23:59:59,
כולל. כך הרגע 00:00 נספר פעם אחת, וחצות של סוף היממה שייך כבר ליממה הבאה. רגע שבו
שלושת המחוגים נפגשים נספר פעם אחת.

??? tip "רמז 1"
    ספרו כל זוג מחוגים לחוד. כמה סיבובים מסיים כל מחוג ביממה?

??? tip "רמז 2"
    המחוג המהיר בזוג מקיף את האיטי. בכל פעם שהוא מרוויח עליו סיבוב שלם, הם נפגשים. כמה
    סיבובים הוא מרוויח ביממה?

??? tip "רמז 3"
    רגע שנספר בשני זוגות הוא רגע ששלושת המחוגים נפגשים בו. כמה רגעים כאלה יש ביממה?
    בדקו איפה מחוג השניות בכל פגישה של הדקות והשעות.

<div class="selfcheck" data-answer="2872" data-show="2,872" data-hint="ספרו כל זוג מחוגים לחוד : בזוג, המהיר נפגש עם האיטי בכל סיבוב שהוא מרוויח עליו. רגע שבו שלושתם נפגשים נספר בשלושה זוגות." markdown>
כמה פעמים ביממה נפגשים לפחות שני מחוגים?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        בסך הכול 2,872 פגישות : 1,416 של השניות והדקות, 1,438 של השניות והשעות ו-22 של
        הדקות והשעות. מהסכום, 2,876, מורידים 4 : ב-00:00 וב-12:00 שלושת המחוגים נפגשים,
        וכל אחד מהרגעים האלה נספר בשלושת הזוגות במקום פעם אחת.

    #### הרעיון { .sol-idea }

    סופרים כל זוג לחוד. המחוג המהיר בזוג מקיף את האיטי, ובכל פעם שהוא מרוויח עליו סיבוב
    שלם הם נפגשים. לכן מספר הפגישות של זוג ביממה הוא ההפרש בין מספרי הסיבובים שלהם. אחר
    כך מחברים את שלושת הזוגות ומורידים את מה שנספר יותר מפעם אחת :

    <!-- gen 0 -->

    | הזוג | הקפות ביממה | פגישות ביממה | הזמן בין שתי פגישות |
    |---|---|---|---|
    | השניות והדקות | ‏1,440 ו-24 | ‏1,416 | ‏\( \tfrac{3{,}600}{59} \approx 61.02 \) שניות |
    | השניות והשעות | ‏1,440 ו-2 | ‏1,438 | ‏\( \tfrac{43{,}200}{719} \approx 60.08 \) שניות |
    | הדקות והשעות | ‏24 ו-2 | ‏22 | ‏\( \tfrac{43{,}200}{11} \approx 3927.27 \) שניות |

    <!-- /gen -->

    בשעון רואים את זה כך : הפגישה הראשונה של הדקות והשעות אחרי 00:00 היא ב-1:05:27.27.
    הנקודות הן 11 המקומות שבהם שני המחוגים האלה נפגשים, במרווחים שווים של \( \tfrac{1}{11} \)
    סיבוב. מחוג השניות רחוק מהם באותו רגע, ולכן זו פגישה של שניים בלבד :

    <!-- gen 1 -->

    <svg class="figure" viewBox="0 0 280 280" style="max-width:17rem" role="img" aria-label="שעון בשעה 1:05:27.27 : מחוג הדקות ומחוג השעות אחד על השני, ומחוג השניות במקום אחר. הנקודות הן 11 המקומות שבהם הדקות והשעות נפגשים"><circle class="clock-face" cx="140" cy="140" r="124"/><line class="clock-tick5" x1="140.0" y1="27.0" x2="140.0" y2="16.0"/><line class="clock-tick" x1="152.4" y1="21.7" x2="153.0" y2="16.7"/><line class="clock-tick" x1="164.7" y1="23.6" x2="165.8" y2="18.7"/><line class="clock-tick" x1="176.8" y1="26.8" x2="178.3" y2="22.1"/><line class="clock-tick" x1="188.4" y1="31.3" x2="190.4" y2="26.7"/><line class="clock-tick5" x1="196.5" y1="42.1" x2="202.0" y2="32.6"/><line class="clock-tick" x1="209.9" y1="43.7" x2="212.9" y2="39.7"/><line class="clock-tick" x1="219.6" y1="51.6" x2="223.0" y2="47.9"/><line class="clock-tick" x1="228.4" y1="60.4" x2="232.1" y2="57.0"/><line class="clock-tick" x1="236.3" y1="70.1" x2="240.3" y2="67.1"/><line class="clock-tick5" x1="237.9" y1="83.5" x2="247.4" y2="78.0"/><line class="clock-tick" x1="248.7" y1="91.6" x2="253.3" y2="89.6"/><line class="clock-tick" x1="253.2" y1="103.2" x2="257.9" y2="101.7"/><line class="clock-tick" x1="256.4" y1="115.3" x2="261.3" y2="114.2"/><line class="clock-tick" x1="258.3" y1="127.6" x2="263.3" y2="127.0"/><line class="clock-tick5" x1="253.0" y1="140.0" x2="264.0" y2="140.0"/><line class="clock-tick" x1="258.3" y1="152.4" x2="263.3" y2="153.0"/><line class="clock-tick" x1="256.4" y1="164.7" x2="261.3" y2="165.8"/><line class="clock-tick" x1="253.2" y1="176.8" x2="257.9" y2="178.3"/><line class="clock-tick" x1="248.7" y1="188.4" x2="253.3" y2="190.4"/><line class="clock-tick5" x1="237.9" y1="196.5" x2="247.4" y2="202.0"/><line class="clock-tick" x1="236.3" y1="209.9" x2="240.3" y2="212.9"/><line class="clock-tick" x1="228.4" y1="219.6" x2="232.1" y2="223.0"/><line class="clock-tick" x1="219.6" y1="228.4" x2="223.0" y2="232.1"/><line class="clock-tick" x1="209.9" y1="236.3" x2="212.9" y2="240.3"/><line class="clock-tick5" x1="196.5" y1="237.9" x2="202.0" y2="247.4"/><line class="clock-tick" x1="188.4" y1="248.7" x2="190.4" y2="253.3"/><line class="clock-tick" x1="176.8" y1="253.2" x2="178.3" y2="257.9"/><line class="clock-tick" x1="164.7" y1="256.4" x2="165.8" y2="261.3"/><line class="clock-tick" x1="152.4" y1="258.3" x2="153.0" y2="263.3"/><line class="clock-tick5" x1="140.0" y1="253.0" x2="140.0" y2="264.0"/><line class="clock-tick" x1="127.6" y1="258.3" x2="127.0" y2="263.3"/><line class="clock-tick" x1="115.3" y1="256.4" x2="114.2" y2="261.3"/><line class="clock-tick" x1="103.2" y1="253.2" x2="101.7" y2="257.9"/><line class="clock-tick" x1="91.6" y1="248.7" x2="89.6" y2="253.3"/><line class="clock-tick5" x1="83.5" y1="237.9" x2="78.0" y2="247.4"/><line class="clock-tick" x1="70.1" y1="236.3" x2="67.1" y2="240.3"/><line class="clock-tick" x1="60.4" y1="228.4" x2="57.0" y2="232.1"/><line class="clock-tick" x1="51.6" y1="219.6" x2="47.9" y2="223.0"/><line class="clock-tick" x1="43.7" y1="209.9" x2="39.7" y2="212.9"/><line class="clock-tick5" x1="42.1" y1="196.5" x2="32.6" y2="202.0"/><line class="clock-tick" x1="31.3" y1="188.4" x2="26.7" y2="190.4"/><line class="clock-tick" x1="26.8" y1="176.8" x2="22.1" y2="178.3"/><line class="clock-tick" x1="23.6" y1="164.7" x2="18.7" y2="165.8"/><line class="clock-tick" x1="21.7" y1="152.4" x2="16.7" y2="153.0"/><line class="clock-tick5" x1="27.0" y1="140.0" x2="16.0" y2="140.0"/><line class="clock-tick" x1="21.7" y1="127.6" x2="16.7" y2="127.0"/><line class="clock-tick" x1="23.6" y1="115.3" x2="18.7" y2="114.2"/><line class="clock-tick" x1="26.8" y1="103.2" x2="22.1" y2="101.7"/><line class="clock-tick" x1="31.3" y1="91.6" x2="26.7" y2="89.6"/><line class="clock-tick5" x1="42.1" y1="83.5" x2="32.6" y2="78.0"/><line class="clock-tick" x1="43.7" y1="70.1" x2="39.7" y2="67.1"/><line class="clock-tick" x1="51.6" y1="60.4" x2="47.9" y2="57.0"/><line class="clock-tick" x1="60.4" y1="51.6" x2="57.0" y2="47.9"/><line class="clock-tick" x1="70.1" y1="43.7" x2="67.1" y2="39.7"/><line class="clock-tick5" x1="83.5" y1="42.1" x2="78.0" y2="32.6"/><line class="clock-tick" x1="91.6" y1="31.3" x2="89.6" y2="26.7"/><line class="clock-tick" x1="103.2" y1="26.8" x2="101.7" y2="22.1"/><line class="clock-tick" x1="115.3" y1="23.6" x2="114.2" y2="18.7"/><line class="clock-tick" x1="127.6" y1="21.7" x2="127.0" y2="16.7"/><text class="legend" x="189.0" y="60.1" text-anchor="middle">1</text><text class="legend" x="224.9" y="96.0" text-anchor="middle">2</text><text class="legend" x="238.0" y="145.0" text-anchor="middle">3</text><text class="legend" x="224.9" y="194.0" text-anchor="middle">4</text><text class="legend" x="189.0" y="229.9" text-anchor="middle">5</text><text class="legend" x="140.0" y="243.0" text-anchor="middle">6</text><text class="legend" x="91.0" y="229.9" text-anchor="middle">7</text><text class="legend" x="55.1" y="194.0" text-anchor="middle">8</text><text class="legend" x="42.0" y="145.0" text-anchor="middle">9</text><text class="legend" x="55.1" y="96.0" text-anchor="middle">10</text><text class="legend" x="91.0" y="60.1" text-anchor="middle">11</text><text class="legend" x="140.0" y="47.0" text-anchor="middle">12</text><circle class="s2-dot" cx="140.0" cy="58.0" r="4.5"><title>0:00:00</title></circle><circle class="s2-dot" cx="184.3" cy="71.0" r="4.5"><title>1:05:27.27</title></circle><circle class="s2-dot" cx="214.6" cy="105.9" r="4.5"><title>2:10:54.55</title></circle><circle class="s2-dot" cx="221.2" cy="151.7" r="4.5"><title>3:16:21.82</title></circle><circle class="s2-dot" cx="202.0" cy="193.7" r="4.5"><title>4:21:49.09</title></circle><circle class="s2-dot" cx="163.1" cy="218.7" r="4.5"><title>5:27:16.36</title></circle><circle class="s2-dot" cx="116.9" cy="218.7" r="4.5"><title>6:32:43.64</title></circle><circle class="s2-dot" cx="78.0" cy="193.7" r="4.5"><title>7:38:10.91</title></circle><circle class="s2-dot" cx="58.8" cy="151.7" r="4.5"><title>8:43:38.18</title></circle><circle class="s2-dot" cx="65.4" cy="105.9" r="4.5"><title>9:49:05.45</title></circle><circle class="s2-dot" cx="95.7" cy="71.0" r="4.5"><title>10:54:32.73</title></circle><line class="ink-line" x1="140" y1="140" x2="173.5" y2="87.8" stroke-width="7" stroke-linecap="round"/><line class="s1-line" x1="140" y1="140" x2="191.9" y2="59.2" stroke-width="4.5" stroke-linecap="round"/><line class="s3-line" x1="140" y1="140" x2="170.4" y2="243.6" stroke-width="2" stroke-linecap="round"/><circle class="ink-dot" cx="140" cy="140" r="5"/></svg>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="ink"></i>מחוג השעות</span><span><i class="s1"></i>מחוג הדקות</span><span><i class="s3"></i>מחוג השניות</span><span><i class="s2"></i>המקומות שבהם הדקות והשעות נפגשים</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סיבובים ביממה :** ביממה יש 86,400 שניות. מחוג השניות מסיים בה 1,440 סיבובים,
       מחוג הדקות 24 ומחוג השעות 2 :

        \[
        \begin{aligned}
        n_s &= \frac{86{,}400}{60} = 1{,}440 \\
        n_m &= \frac{86{,}400}{3{,}600} = 24 \\
        n_h &= \frac{86{,}400}{43{,}200} = 2
        \end{aligned}
        \]

    2. **פגישות של זוג :** נניח שהמחוג המהיר מסיים \( n_i \) סיבובים ביממה והאיטי
       \( n_j \). הפער ביניהם, בסיבובים, גדל בקצב קבוע מ-0 עד \( n_i - n_j \). הם נפגשים
       בכל פעם שהפער הוא מספר שלם : 0 (ב-00:00), 1, 2, ועד \( n_i - n_j - 1 \). הפער
       \( n_i - n_j \) מגיע בדיוק בחצות של סוף היממה, שלא שייכת לה. לכן לזוג יש ביממה
       בדיוק \( n_i - n_j \) פגישות, כולל 00:00 :

        \[
        \begin{aligned}
        N_{sm} &= 1{,}440 - 24 = 1{,}416 \\
        N_{sh} &= 1{,}440 - 2 = 1{,}438 \\
        N_{mh} &= 24 - 2 = 22
        \end{aligned}
        \]

    3. **המרווח בין פגישות :** הפער גדל בקצב קבוע, ולכן הפגישות של זוג נמצאות במרווחים
       שווים : היממה חלקי מספר הפגישות. השניות והדקות נפגשים כל \( \tfrac{3{,}600}{59} \approx 61.02 \)
       שניות, והדקות והשעות כל שעה, 5 דקות ו-27.27 שניות. בגרף, הזווית של מחוג הדקות היא
       מסור עם 12 שיניים, הזווית של מחוג השעות היא קו אחד איטי, וכל חיתוך הוא פגישה :

        <!-- gen 3 -->

        <svg class="perf-chart" viewBox="0 0 480 260" style="max-width:36rem" role="img" aria-label="זווית מחוג הדקות ומחוג השעות לאורך 12 שעות : 12 נקודות מפגש, הראשונה והאחרונה עם מחוג השניות"><line class="grid" x1="46" x2="468" y1="226.0" y2="226.0"/><text class="tick" x="38" y="230.0" text-anchor="end">0°</text><line class="grid" x1="46" x2="468" y1="173.5" y2="173.5"/><text class="tick" x="38" y="177.5" text-anchor="end">90°</text><line class="grid" x1="46" x2="468" y1="121.0" y2="121.0"/><text class="tick" x="38" y="125.0" text-anchor="end">180°</text><line class="grid" x1="46" x2="468" y1="68.5" y2="68.5"/><text class="tick" x="38" y="72.5" text-anchor="end">270°</text><line class="grid" x1="46" x2="468" y1="16.0" y2="16.0"/><text class="tick" x="38" y="20.0" text-anchor="end">360°</text><line class="grid" x1="46.0" x2="46.0" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="46.0" y="244" text-anchor="middle">0</text><line class="grid" x1="81.2" x2="81.2" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="81.2" y="244" text-anchor="middle">1</text><line class="grid" x1="116.3" x2="116.3" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="116.3" y="244" text-anchor="middle">2</text><line class="grid" x1="151.5" x2="151.5" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="151.5" y="244" text-anchor="middle">3</text><line class="grid" x1="186.7" x2="186.7" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="186.7" y="244" text-anchor="middle">4</text><line class="grid" x1="221.8" x2="221.8" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="221.8" y="244" text-anchor="middle">5</text><line class="grid" x1="257.0" x2="257.0" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="257.0" y="244" text-anchor="middle">6</text><line class="grid" x1="292.2" x2="292.2" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="292.2" y="244" text-anchor="middle">7</text><line class="grid" x1="327.3" x2="327.3" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="327.3" y="244" text-anchor="middle">8</text><line class="grid" x1="362.5" x2="362.5" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="362.5" y="244" text-anchor="middle">9</text><line class="grid" x1="397.7" x2="397.7" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="397.7" y="244" text-anchor="middle">10</text><line class="grid" x1="432.8" x2="432.8" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="432.8" y="244" text-anchor="middle">11</text><line class="grid" x1="468.0" x2="468.0" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="468.0" y="244" text-anchor="middle">12</text><line class="s1-line" x1="46.0" y1="226.0" x2="81.2" y2="16.0" stroke-width="2"/><line class="s1-line" x1="81.2" y1="226.0" x2="116.3" y2="16.0" stroke-width="2"/><line class="s1-line" x1="116.3" y1="226.0" x2="151.5" y2="16.0" stroke-width="2"/><line class="s1-line" x1="151.5" y1="226.0" x2="186.7" y2="16.0" stroke-width="2"/><line class="s1-line" x1="186.7" y1="226.0" x2="221.8" y2="16.0" stroke-width="2"/><line class="s1-line" x1="221.8" y1="226.0" x2="257.0" y2="16.0" stroke-width="2"/><line class="s1-line" x1="257.0" y1="226.0" x2="292.2" y2="16.0" stroke-width="2"/><line class="s1-line" x1="292.2" y1="226.0" x2="327.3" y2="16.0" stroke-width="2"/><line class="s1-line" x1="327.3" y1="226.0" x2="362.5" y2="16.0" stroke-width="2"/><line class="s1-line" x1="362.5" y1="226.0" x2="397.7" y2="16.0" stroke-width="2"/><line class="s1-line" x1="397.7" y1="226.0" x2="432.8" y2="16.0" stroke-width="2"/><line class="s1-line" x1="432.8" y1="226.0" x2="468.0" y2="16.0" stroke-width="2"/><line class="ink-line" x1="46.0" y1="226.0" x2="468.0" y2="16.0" stroke-width="3"/><circle class="s3-dot" cx="46.0" cy="226.0" r="5.5"><title>0:00:00 – שלושתם</title></circle><circle class="s2-dot" cx="84.4" cy="206.9" r="4.5"><title>1:05:27.27</title></circle><circle class="s2-dot" cx="122.7" cy="187.8" r="4.5"><title>2:10:54.55</title></circle><circle class="s2-dot" cx="161.1" cy="168.7" r="4.5"><title>3:16:21.82</title></circle><circle class="s2-dot" cx="199.5" cy="149.6" r="4.5"><title>4:21:49.09</title></circle><circle class="s2-dot" cx="237.8" cy="130.5" r="4.5"><title>5:27:16.36</title></circle><circle class="s2-dot" cx="276.2" cy="111.5" r="4.5"><title>6:32:43.64</title></circle><circle class="s2-dot" cx="314.5" cy="92.4" r="4.5"><title>7:38:10.91</title></circle><circle class="s2-dot" cx="352.9" cy="73.3" r="4.5"><title>8:43:38.18</title></circle><circle class="s2-dot" cx="391.3" cy="54.2" r="4.5"><title>9:49:05.45</title></circle><circle class="s2-dot" cx="429.6" cy="35.1" r="4.5"><title>10:54:32.73</title></circle><circle class="s3-dot" cx="468.0" cy="16.0" r="5.5"><title>12:00:00 – שלושתם</title></circle><line class="axis" x1="46" x2="468" y1="226" y2="226"/></svg>

        <!-- /gen -->

        <!-- gen 4 -->

        <span class="viz-legend"><span><i class="ink"></i>מחוג השעות</span><span><i class="s1"></i>מחוג הדקות</span><span><i class="s2"></i>הדקות והשעות נפגשים</span><span><i class="s3"></i>שלושתם, גם עם מחוג השניות</span></span>

        <!-- /gen -->

        ב-12 שעות יש 12 חיתוכים, כולל 00:00 ו-12:00. ביממה כולה זה 22, כי 12:00 נספר
        פעם אחת ו-24:00 כבר לא שייך ליממה.

    4. **סכום הזוגות :** ‏\( 1{,}416 + 1{,}438 + 22 = 2{,}876 \). אבל זה מספר הפגישות של
       זוגות, ולא מספר הרגעים.

    5. **מה נספר פעמיים :** אם באותו רגע נפגשים שני זוגות שונים, למשל השניות עם הדקות
       והדקות עם השעות, אז שלושת המחוגים באותו מקום. רגע כזה נספר בשלושת הזוגות, ולכן
       מורידים 2 על כל אחד. ביממה יש שני רגעים כאלה בלבד : 00:00 ו-12:00 (בדיקה בהמשך,
       והוכחה כללית בסעיף ב).

    6. **התשובה :** ‏\( 2{,}876 - 2 \cdot 2 = 2{,}872 \).

    </div>

    #### למה זה נכון { .sol-proof }

    **שלושתם נפגשים רק ב-00:00 וב-12:00.** כל פגישה של שלושה היא גם פגישה של הדקות
    והשעות, וב-12 שעות יש רק 11 כאלה. מספיק לבדוק איפה מחוג השניות בכל אחת. על לוח של 60
    שנתות, הפגישה ה-\( k \) של הדקות והשעות היא בשנתה \( \tfrac{60k}{11} \), ומחוג השניות
    נמצא בשנתה של השניות בשעה :

    <!-- gen 9 -->

    | ‏\( k \) | השעה | הדקות והשעות על השנתה | מחוג השניות על השנתה |
    |---|---|---|---|
    | ‏0 | ‏0:00:00 | ‏0.00 | ‏0.00 (שלושתם) |
    | ‏1 | ‏1:05:27.27 | ‏5.45 | ‏27.27 |
    | ‏2 | ‏2:10:54.55 | ‏10.91 | ‏54.55 |
    | ‏3 | ‏3:16:21.82 | ‏16.36 | ‏21.82 |
    | ‏4 | ‏4:21:49.09 | ‏21.82 | ‏49.09 |
    | ‏5 | ‏5:27:16.36 | ‏27.27 | ‏16.36 |
    | ‏6 | ‏6:32:43.64 | ‏32.73 | ‏43.64 |
    | ‏7 | ‏7:38:10.91 | ‏38.18 | ‏10.91 |
    | ‏8 | ‏8:43:38.18 | ‏43.64 | ‏38.18 |
    | ‏9 | ‏9:49:05.45 | ‏49.09 | ‏5.45 |
    | ‏10 | ‏10:54:32.73 | ‏54.55 | ‏32.73 |
    | ‏11 | ‏12:00:00 | ‏0.00 | ‏0.00 (שלושתם) |

    <!-- /gen -->

    רק בשורה הראשונה ובאחרונה מחוג השניות באותה שנתה. ב-12 השעות שאחרי 12:00 הכול חוזר
    על עצמו, ולכן ביממה יש בדיוק שני רגעים של שלושה מחוגים.

    **מחוג השניות מקרוב.** כמעט בכל דקה מחוג השניות עובר גם את מחוג השעות וגם את מחוג
    הדקות, אבל ברגעים שונים. אחרי הדקה הראשונה, למשל, הוא פוגש את מחוג השעות אחרי 60.08 שניות,
    ואת מחוג הדקות רק אחרי 61.02 שניות. אלה שתי פגישות נפרדות, ולכן שני הזוגות נספרים לחוד :

    <!-- gen 5 -->

    <svg class="perf-chart" viewBox="0 0 480 260" style="max-width:36rem" role="img" aria-label="הזווית של שלושת המחוגים בין 0:00:59.8 ל-0:01:01.6 : מחוג השניות פוגש את מחוג השעות ב-60.08 שניות ואת מחוג הדקות ב-61.02 שניות"><line class="grid" x1="46" x2="468" y1="226.0" y2="226.0"/><text class="tick" x="38" y="230.0" text-anchor="end">0°</text><line class="grid" x1="46" x2="468" y1="184.0" y2="184.0"/><text class="tick" x="38" y="188.0" text-anchor="end">2°</text><line class="grid" x1="46" x2="468" y1="142.0" y2="142.0"/><text class="tick" x="38" y="146.0" text-anchor="end">4°</text><line class="grid" x1="46" x2="468" y1="100.0" y2="100.0"/><text class="tick" x="38" y="104.0" text-anchor="end">6°</text><line class="grid" x1="46" x2="468" y1="58.0" y2="58.0"/><text class="tick" x="38" y="62.0" text-anchor="end">8°</text><line class="grid" x1="46" x2="468" y1="16.0" y2="16.0"/><text class="tick" x="38" y="20.0" text-anchor="end">10°</text><line class="grid" x1="92.9" x2="92.9" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="92.9" y="244" text-anchor="middle">60</text><line class="grid" x1="210.1" x2="210.1" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="210.1" y="244" text-anchor="middle">60.5</text><line class="grid" x1="327.3" x2="327.3" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="327.3" y="244" text-anchor="middle">61</text><line class="grid" x1="444.6" x2="444.6" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="444.6" y="244" text-anchor="middle">61.5</text><line class="s3-line" x1="92.9" y1="226.0" x2="468.0" y2="24.4" stroke-width="2.5"/><line class="s1-line" x1="46.0" y1="100.4" x2="468.0" y2="96.6" stroke-width="3"/><line class="ink-line" x1="46.0" y1="215.5" x2="468.0" y2="215.2" stroke-width="3"/><circle class="s2-dot" cx="112.5" cy="215.5" r="5.5"><title>0:01:00.08 : השניות והשעות</title></circle><text class="legend" x="88.5" y="203.5" text-anchor="middle">60.08</text><circle class="s2-dot" cx="331.3" cy="97.9" r="5.5"><title>0:01:01.02 : השניות והדקות</title></circle><text class="legend" x="301.3" y="87.9" text-anchor="middle">61.02</text><line class="axis" x1="46" x2="468" y1="226" y2="226"/></svg>

    <!-- /gen -->

    <!-- gen 6 -->

    <span class="viz-legend"><span><i class="ink"></i>מחוג השעות</span><span><i class="s1"></i>מחוג הדקות</span><span><i class="s3"></i>מחוג השניות</span><span><i class="s2"></i>פגישה</span></span>

    <!-- /gen -->

    **דקה בלי פגישה.** מחוג השניות פוגש את מחוג הדקות כל 61.02 שניות, ולכן בכל דקה הפגישה
    מאחרת בעוד \( \tfrac{60}{59} \approx 1.017 \) שניות. בדקה 58 של השעה היא כבר בשנייה
    58.98, והפגישה הבאה היא בדיוק בשעה העגולה. בדקה 59 אין פגישה בכלל, ולכן בשעה יש 59
    פגישות כאלה, וביממה \( 59 \cdot 24 = 1{,}416 \). עם מחוג השעות הפגישה מאחרת רק ב-0.083
    שניות בכל דקה :

    <!-- gen 7 -->

    <svg class="perf-chart" viewBox="0 0 480 260" style="max-width:36rem" role="img" aria-label="בכל דקה בשעה הראשונה : באיזו שנייה מחוג השניות פוגש את מחוג הדקות ואת מחוג השעות. בדקה 59 אין פגישה עם מחוג הדקות"><line class="grid" x1="46" x2="468" y1="226.0" y2="226.0"/><text class="tick" x="38" y="230.0" text-anchor="end">0</text><line class="grid" x1="46" x2="468" y1="173.5" y2="173.5"/><text class="tick" x="38" y="177.5" text-anchor="end">15</text><line class="grid" x1="46" x2="468" y1="121.0" y2="121.0"/><text class="tick" x="38" y="125.0" text-anchor="end">30</text><line class="grid" x1="46" x2="468" y1="68.5" y2="68.5"/><text class="tick" x="38" y="72.5" text-anchor="end">45</text><line class="grid" x1="46" x2="468" y1="16.0" y2="16.0"/><text class="tick" x="38" y="20.0" text-anchor="end">60</text><line class="grid" x1="52.9" x2="52.9" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="52.9" y="244" text-anchor="middle">0</text><line class="grid" x1="122.1" x2="122.1" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="122.1" y="244" text-anchor="middle">10</text><line class="grid" x1="191.3" x2="191.3" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="191.3" y="244" text-anchor="middle">20</text><line class="grid" x1="260.5" x2="260.5" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="260.5" y="244" text-anchor="middle">30</text><line class="grid" x1="329.6" x2="329.6" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="329.6" y="244" text-anchor="middle">40</text><line class="grid" x1="398.8" x2="398.8" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="398.8" y="244" text-anchor="middle">50</text><line class="grid" x1="461.1" x2="461.1" y1="10" y2="226" stroke-dasharray="4 4"/><text class="tick" x="461.1" y="244" text-anchor="middle">59</text><circle class="ink-dot" cx="52.9" cy="226.0" r="3.2"><title>0:00:00 : השניות והשעות</title></circle><circle class="ink-dot" cx="59.8" cy="225.7" r="3.2"><title>0:01:00.08 : השניות והשעות</title></circle><circle class="ink-dot" cx="66.8" cy="225.4" r="3.2"><title>0:02:00.17 : השניות והשעות</title></circle><circle class="ink-dot" cx="73.7" cy="225.1" r="3.2"><title>0:03:00.25 : השניות והשעות</title></circle><circle class="ink-dot" cx="80.6" cy="224.8" r="3.2"><title>0:04:00.33 : השניות והשעות</title></circle><circle class="ink-dot" cx="87.5" cy="224.5" r="3.2"><title>0:05:00.42 : השניות והשעות</title></circle><circle class="ink-dot" cx="94.4" cy="224.2" r="3.2"><title>0:06:00.50 : השניות והשעות</title></circle><circle class="ink-dot" cx="101.3" cy="224.0" r="3.2"><title>0:07:00.58 : השניות והשעות</title></circle><circle class="ink-dot" cx="108.3" cy="223.7" r="3.2"><title>0:08:00.67 : השניות והשעות</title></circle><circle class="ink-dot" cx="115.2" cy="223.4" r="3.2"><title>0:09:00.75 : השניות והשעות</title></circle><circle class="ink-dot" cx="122.1" cy="223.1" r="3.2"><title>0:10:00.83 : השניות והשעות</title></circle><circle class="ink-dot" cx="129.0" cy="222.8" r="3.2"><title>0:11:00.92 : השניות והשעות</title></circle><circle class="ink-dot" cx="135.9" cy="222.5" r="3.2"><title>0:12:01.00 : השניות והשעות</title></circle><circle class="ink-dot" cx="142.9" cy="222.2" r="3.2"><title>0:13:01.08 : השניות והשעות</title></circle><circle class="ink-dot" cx="149.8" cy="221.9" r="3.2"><title>0:14:01.17 : השניות והשעות</title></circle><circle class="ink-dot" cx="156.7" cy="221.6" r="3.2"><title>0:15:01.25 : השניות והשעות</title></circle><circle class="ink-dot" cx="163.6" cy="221.3" r="3.2"><title>0:16:01.34 : השניות והשעות</title></circle><circle class="ink-dot" cx="170.5" cy="221.0" r="3.2"><title>0:17:01.42 : השניות והשעות</title></circle><circle class="ink-dot" cx="177.4" cy="220.7" r="3.2"><title>0:18:01.50 : השניות והשעות</title></circle><circle class="ink-dot" cx="184.4" cy="220.5" r="3.2"><title>0:19:01.59 : השניות והשעות</title></circle><circle class="ink-dot" cx="191.3" cy="220.2" r="3.2"><title>0:20:01.67 : השניות והשעות</title></circle><circle class="ink-dot" cx="198.2" cy="219.9" r="3.2"><title>0:21:01.75 : השניות והשעות</title></circle><circle class="ink-dot" cx="205.1" cy="219.6" r="3.2"><title>0:22:01.84 : השניות והשעות</title></circle><circle class="ink-dot" cx="212.0" cy="219.3" r="3.2"><title>0:23:01.92 : השניות והשעות</title></circle><circle class="ink-dot" cx="219.0" cy="219.0" r="3.2"><title>0:24:02.00 : השניות והשעות</title></circle><circle class="ink-dot" cx="225.9" cy="218.7" r="3.2"><title>0:25:02.09 : השניות והשעות</title></circle><circle class="ink-dot" cx="232.8" cy="218.4" r="3.2"><title>0:26:02.17 : השניות והשעות</title></circle><circle class="ink-dot" cx="239.7" cy="218.1" r="3.2"><title>0:27:02.25 : השניות והשעות</title></circle><circle class="ink-dot" cx="246.6" cy="217.8" r="3.2"><title>0:28:02.34 : השניות והשעות</title></circle><circle class="ink-dot" cx="253.5" cy="217.5" r="3.2"><title>0:29:02.42 : השניות והשעות</title></circle><circle class="ink-dot" cx="260.5" cy="217.2" r="3.2"><title>0:30:02.50 : השניות והשעות</title></circle><circle class="ink-dot" cx="267.4" cy="216.9" r="3.2"><title>0:31:02.59 : השניות והשעות</title></circle><circle class="ink-dot" cx="274.3" cy="216.7" r="3.2"><title>0:32:02.67 : השניות והשעות</title></circle><circle class="ink-dot" cx="281.2" cy="216.4" r="3.2"><title>0:33:02.75 : השניות והשעות</title></circle><circle class="ink-dot" cx="288.1" cy="216.1" r="3.2"><title>0:34:02.84 : השניות והשעות</title></circle><circle class="ink-dot" cx="295.0" cy="215.8" r="3.2"><title>0:35:02.92 : השניות והשעות</title></circle><circle class="ink-dot" cx="302.0" cy="215.5" r="3.2"><title>0:36:03.00 : השניות והשעות</title></circle><circle class="ink-dot" cx="308.9" cy="215.2" r="3.2"><title>0:37:03.09 : השניות והשעות</title></circle><circle class="ink-dot" cx="315.8" cy="214.9" r="3.2"><title>0:38:03.17 : השניות והשעות</title></circle><circle class="ink-dot" cx="322.7" cy="214.6" r="3.2"><title>0:39:03.25 : השניות והשעות</title></circle><circle class="ink-dot" cx="329.6" cy="214.3" r="3.2"><title>0:40:03.34 : השניות והשעות</title></circle><circle class="ink-dot" cx="336.6" cy="214.0" r="3.2"><title>0:41:03.42 : השניות והשעות</title></circle><circle class="ink-dot" cx="343.5" cy="213.7" r="3.2"><title>0:42:03.50 : השניות והשעות</title></circle><circle class="ink-dot" cx="350.4" cy="213.4" r="3.2"><title>0:43:03.59 : השניות והשעות</title></circle><circle class="ink-dot" cx="357.3" cy="213.1" r="3.2"><title>0:44:03.67 : השניות והשעות</title></circle><circle class="ink-dot" cx="364.2" cy="212.9" r="3.2"><title>0:45:03.76 : השניות והשעות</title></circle><circle class="ink-dot" cx="371.1" cy="212.6" r="3.2"><title>0:46:03.84 : השניות והשעות</title></circle><circle class="ink-dot" cx="378.1" cy="212.3" r="3.2"><title>0:47:03.92 : השניות והשעות</title></circle><circle class="ink-dot" cx="385.0" cy="212.0" r="3.2"><title>0:48:04.01 : השניות והשעות</title></circle><circle class="ink-dot" cx="391.9" cy="211.7" r="3.2"><title>0:49:04.09 : השניות והשעות</title></circle><circle class="ink-dot" cx="398.8" cy="211.4" r="3.2"><title>0:50:04.17 : השניות והשעות</title></circle><circle class="ink-dot" cx="405.7" cy="211.1" r="3.2"><title>0:51:04.26 : השניות והשעות</title></circle><circle class="ink-dot" cx="412.7" cy="210.8" r="3.2"><title>0:52:04.34 : השניות והשעות</title></circle><circle class="ink-dot" cx="419.6" cy="210.5" r="3.2"><title>0:53:04.42 : השניות והשעות</title></circle><circle class="ink-dot" cx="426.5" cy="210.2" r="3.2"><title>0:54:04.51 : השניות והשעות</title></circle><circle class="ink-dot" cx="433.4" cy="209.9" r="3.2"><title>0:55:04.59 : השניות והשעות</title></circle><circle class="ink-dot" cx="440.3" cy="209.6" r="3.2"><title>0:56:04.67 : השניות והשעות</title></circle><circle class="ink-dot" cx="447.2" cy="209.4" r="3.2"><title>0:57:04.76 : השניות והשעות</title></circle><circle class="ink-dot" cx="454.2" cy="209.1" r="3.2"><title>0:58:04.84 : השניות והשעות</title></circle><circle class="ink-dot" cx="461.1" cy="208.8" r="3.2"><title>0:59:04.92 : השניות והשעות</title></circle><circle class="s1-dot" cx="52.9" cy="226.0" r="3.2"><title>0:00:00 : השניות והדקות</title></circle><circle class="s1-dot" cx="59.8" cy="222.4" r="3.2"><title>0:01:01.02 : השניות והדקות</title></circle><circle class="s1-dot" cx="66.8" cy="218.9" r="3.2"><title>0:02:02.03 : השניות והדקות</title></circle><circle class="s1-dot" cx="73.7" cy="215.3" r="3.2"><title>0:03:03.05 : השניות והדקות</title></circle><circle class="s1-dot" cx="80.6" cy="211.8" r="3.2"><title>0:04:04.07 : השניות והדקות</title></circle><circle class="s1-dot" cx="87.5" cy="208.2" r="3.2"><title>0:05:05.08 : השניות והדקות</title></circle><circle class="s1-dot" cx="94.4" cy="204.6" r="3.2"><title>0:06:06.10 : השניות והדקות</title></circle><circle class="s1-dot" cx="101.3" cy="201.1" r="3.2"><title>0:07:07.12 : השניות והדקות</title></circle><circle class="s1-dot" cx="108.3" cy="197.5" r="3.2"><title>0:08:08.14 : השניות והדקות</title></circle><circle class="s1-dot" cx="115.2" cy="194.0" r="3.2"><title>0:09:09.15 : השניות והדקות</title></circle><circle class="s1-dot" cx="122.1" cy="190.4" r="3.2"><title>0:10:10.17 : השניות והדקות</title></circle><circle class="s1-dot" cx="129.0" cy="186.8" r="3.2"><title>0:11:11.19 : השניות והדקות</title></circle><circle class="s1-dot" cx="135.9" cy="183.3" r="3.2"><title>0:12:12.20 : השניות והדקות</title></circle><circle class="s1-dot" cx="142.9" cy="179.7" r="3.2"><title>0:13:13.22 : השניות והדקות</title></circle><circle class="s1-dot" cx="149.8" cy="176.2" r="3.2"><title>0:14:14.24 : השניות והדקות</title></circle><circle class="s1-dot" cx="156.7" cy="172.6" r="3.2"><title>0:15:15.25 : השניות והדקות</title></circle><circle class="s1-dot" cx="163.6" cy="169.1" r="3.2"><title>0:16:16.27 : השניות והדקות</title></circle><circle class="s1-dot" cx="170.5" cy="165.5" r="3.2"><title>0:17:17.29 : השניות והדקות</title></circle><circle class="s1-dot" cx="177.4" cy="161.9" r="3.2"><title>0:18:18.31 : השניות והדקות</title></circle><circle class="s1-dot" cx="184.4" cy="158.4" r="3.2"><title>0:19:19.32 : השניות והדקות</title></circle><circle class="s1-dot" cx="191.3" cy="154.8" r="3.2"><title>0:20:20.34 : השניות והדקות</title></circle><circle class="s1-dot" cx="198.2" cy="151.3" r="3.2"><title>0:21:21.36 : השניות והדקות</title></circle><circle class="s1-dot" cx="205.1" cy="147.7" r="3.2"><title>0:22:22.37 : השניות והדקות</title></circle><circle class="s1-dot" cx="212.0" cy="144.1" r="3.2"><title>0:23:23.39 : השניות והדקות</title></circle><circle class="s1-dot" cx="219.0" cy="140.6" r="3.2"><title>0:24:24.41 : השניות והדקות</title></circle><circle class="s1-dot" cx="225.9" cy="137.0" r="3.2"><title>0:25:25.42 : השניות והדקות</title></circle><circle class="s1-dot" cx="232.8" cy="133.5" r="3.2"><title>0:26:26.44 : השניות והדקות</title></circle><circle class="s1-dot" cx="239.7" cy="129.9" r="3.2"><title>0:27:27.46 : השניות והדקות</title></circle><circle class="s1-dot" cx="246.6" cy="126.3" r="3.2"><title>0:28:28.47 : השניות והדקות</title></circle><circle class="s1-dot" cx="253.5" cy="122.8" r="3.2"><title>0:29:29.49 : השניות והדקות</title></circle><circle class="s1-dot" cx="260.5" cy="119.2" r="3.2"><title>0:30:30.51 : השניות והדקות</title></circle><circle class="s1-dot" cx="267.4" cy="115.7" r="3.2"><title>0:31:31.53 : השניות והדקות</title></circle><circle class="s1-dot" cx="274.3" cy="112.1" r="3.2"><title>0:32:32.54 : השניות והדקות</title></circle><circle class="s1-dot" cx="281.2" cy="108.5" r="3.2"><title>0:33:33.56 : השניות והדקות</title></circle><circle class="s1-dot" cx="288.1" cy="105.0" r="3.2"><title>0:34:34.58 : השניות והדקות</title></circle><circle class="s1-dot" cx="295.0" cy="101.4" r="3.2"><title>0:35:35.59 : השניות והדקות</title></circle><circle class="s1-dot" cx="302.0" cy="97.9" r="3.2"><title>0:36:36.61 : השניות והדקות</title></circle><circle class="s1-dot" cx="308.9" cy="94.3" r="3.2"><title>0:37:37.63 : השניות והדקות</title></circle><circle class="s1-dot" cx="315.8" cy="90.7" r="3.2"><title>0:38:38.64 : השניות והדקות</title></circle><circle class="s1-dot" cx="322.7" cy="87.2" r="3.2"><title>0:39:39.66 : השניות והדקות</title></circle><circle class="s1-dot" cx="329.6" cy="83.6" r="3.2"><title>0:40:40.68 : השניות והדקות</title></circle><circle class="s1-dot" cx="336.6" cy="80.1" r="3.2"><title>0:41:41.69 : השניות והדקות</title></circle><circle class="s1-dot" cx="343.5" cy="76.5" r="3.2"><title>0:42:42.71 : השניות והדקות</title></circle><circle class="s1-dot" cx="350.4" cy="72.9" r="3.2"><title>0:43:43.73 : השניות והדקות</title></circle><circle class="s1-dot" cx="357.3" cy="69.4" r="3.2"><title>0:44:44.75 : השניות והדקות</title></circle><circle class="s1-dot" cx="364.2" cy="65.8" r="3.2"><title>0:45:45.76 : השניות והדקות</title></circle><circle class="s1-dot" cx="371.1" cy="62.3" r="3.2"><title>0:46:46.78 : השניות והדקות</title></circle><circle class="s1-dot" cx="378.1" cy="58.7" r="3.2"><title>0:47:47.80 : השניות והדקות</title></circle><circle class="s1-dot" cx="385.0" cy="55.2" r="3.2"><title>0:48:48.81 : השניות והדקות</title></circle><circle class="s1-dot" cx="391.9" cy="51.6" r="3.2"><title>0:49:49.83 : השניות והדקות</title></circle><circle class="s1-dot" cx="398.8" cy="48.0" r="3.2"><title>0:50:50.85 : השניות והדקות</title></circle><circle class="s1-dot" cx="405.7" cy="44.5" r="3.2"><title>0:51:51.86 : השניות והדקות</title></circle><circle class="s1-dot" cx="412.7" cy="40.9" r="3.2"><title>0:52:52.88 : השניות והדקות</title></circle><circle class="s1-dot" cx="419.6" cy="37.4" r="3.2"><title>0:53:53.90 : השניות והדקות</title></circle><circle class="s1-dot" cx="426.5" cy="33.8" r="3.2"><title>0:54:54.92 : השניות והדקות</title></circle><circle class="s1-dot" cx="433.4" cy="30.2" r="3.2"><title>0:55:55.93 : השניות והדקות</title></circle><circle class="s1-dot" cx="440.3" cy="26.7" r="3.2"><title>0:56:56.95 : השניות והדקות</title></circle><circle class="s1-dot" cx="447.2" cy="23.1" r="3.2"><title>0:57:57.97 : השניות והדקות</title></circle><circle class="s1-dot" cx="454.2" cy="19.6" r="3.2"><title>0:58:58.98 : השניות והדקות</title></circle><text class="legend" x="458.3" y="86.0" text-anchor="start" direction="rtl">בדקה 59 אין</text><line class="axis" x1="46" x2="468" y1="226" y2="226"/></svg>

    <!-- /gen -->

    <!-- gen 8 -->

    <span class="viz-legend"><span><i class="s1"></i>פגישה עם מחוג הדקות</span><span><i class="ink"></i>פגישה עם מחוג השעות</span></span>

    <!-- /gen -->

    **סוף היממה.** הפגישות האחרונות ביממה הן ב-23:58:58.98, של השניות והדקות, וב-23:58:59.92,
    של השניות והשעות. בדקה 23:59 אין אף פגישה, ולכן התשובה לא משתנה אם סופרים את 23:59 או
    לא.

    **בדיקה בדרך אחרת.** בתוך 12 שעות, בלי 00:00 ובלי 12:00, יש
    \( 707 + 718 + 10 = 1{,}435 \) פגישות, ואין בהן פגישה של שלושה. ביממה יש שני חלקים
    כאלה, ועוד שני הרגעים 00:00 ו-12:00 :
    \( 2 \cdot 1{,}435 + 2 = 2{,}872 \). אותה תשובה.

    **נסו בעצמכם.** גררו מחוג, הזיזו את פס היממה, הקלידו שעה או הפעילו את השעון. המונה סופר
    את הפגישות מ-00:00:00 ועד סוף השנייה שמוצגת, ושני מחוגים שנפגשים בשנייה הזו נצבעים
    בכתום. הכפתורים קופצים לפגישה הבאה או לקודמת, או לפגישה המשולשת הבאה, והסימון של
    הזוגות קובע אילו פגישות נחשבות לקפיצה. מתחת לפס היממה, פס זמן לכל זוג עם סימון בכל
    פגישה : רואים איפה הפגישות מתקבצות, ולחיצה על פס קופצת לפגישה הקרובה של אותו זוג :

    <div class="explorer" data-kind="clock" data-t="0"></div>

---

### סעיף ב – הרחבה : הנוסחה הכללית וההוכחה

**בונוס.** שני מחוגים מסיימים סיבוב בזמנים \( t_i < t_j \). מצאו את הזמן בין שתי פגישות
שלהם, ונוסחה למספר הפגישות בקטע זמן באורך \( L \) שמתחיל בפגישה : סגור, פתוח וחצי פתוח.
אחר כך הוכיחו ששלושת המחוגים של השעון נפגשים רק בכפולות של 12 שעות, והשתמשו בשתי
התוצאות כדי לקבל שוב את 2,872.

??? tip "רמז 1"
    מדדו זוויות בסיבובים. מחוג שמסיים סיבוב בזמן \( t_i \) נע במהירות \( 1 / t_i \)
    סיבובים ליחידת זמן. מתי הפער בין שני מחוגים הוא מספר שלם של סיבובים?

??? tip "רמז 2"
    הפגישות הן בזמנים \( 0, T, 2T, \dots \). כמה מספרים שלמים \( k \) מקיימים
    \( 0 \le kT \le L \)? ומה משתנה כשקצה של הקטע לא נכלל?

??? tip "רמז 3"
    בפגישה של שלושה, הזמן הוא גם כפולה של המרווח של השניות והדקות וגם כפולה של המרווח של
    הדקות והשעות. כתבו את זה כשוויון בין שני שברים עם מספרים שלמים \( a \) ו-\( b \).

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        הזמן בין פגישות הוא \( T_{ij} = \dfrac{t_i t_j}{t_j - t_i} \). בקטע \( 0 \le t < L \)
        יש \( \lceil L / T_{ij} \rceil \) פגישות, בקטע סגור \( \lfloor L / T_{ij} \rfloor + 1 \)
        ובקטע פתוח \( \lceil L / T_{ij} \rceil - 1 \). שלושת המחוגים נפגשים רק בזמנים
        \( t = 43{,}200\,c \), ולכן ביממה יש
        \( 1{,}416 + 1{,}438 + 22 - 2 \cdot 2 = 2{,}872 \) פגישות.

    #### הרעיון { .sol-idea }

    המיקום של מחוג, בסיבובים, הוא \( \theta_i(t) = t / t_i \). שני מחוגים נפגשים כשההפרש
    \( \theta_i - \theta_j \) הוא מספר שלם. ההפרש הזה לינארי בזמן, ולכן הוא עובר כל מספר שלם
    פעם אחת, במרווחים שווים. פגישה של שלושה היא שני תנאים כאלה בבת אחת, כלומר משוואה
    במספרים שלמים, והיא נפתרת בעזרת מחלק משותף.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מהירות יחסית :** המהירויות הן \( \omega_i = 1 / t_i \) ו-\( \omega_j = 1 / t_j \)
       סיבובים ליחידת זמן. המהיר מתרחק מהאיטי בקצב ההפרש :

        \[
        \omega_i - \omega_j = \frac{1}{t_i} - \frac{1}{t_j} = \frac{t_j - t_i}{t_i t_j}
        \tag{1}
        \]

    2. **זמני הפגישות :** הם נפגשים כשהמהיר הרוויח מספר שלם \( k \) של סיבובים, כלומר
       כש-\( t\,(\omega_i - \omega_j) = k \) :

        \[
        \begin{aligned}
        t &= k\,T_{ij} \\
        T_{ij} &= \frac{1}{\omega_i - \omega_j} = \frac{t_i t_j}{t_j - t_i}
        \end{aligned}
        \tag{2}
        \]

    3. **ספירה בקטע :** סופרים את השלמים \( k \ge 0 \) עם \( k T_{ij} \) בקטע. בקטע סגור
       \( k \le L / T_{ij} \). בקטע פתוח \( 1 \le k < L / T_{ij} \). בקטע חצי פתוח
       \( 0 \le k < L / T_{ij} \):

        \[
        \begin{aligned}
        N^{[0,L]} &= \left\lfloor \frac{L}{T_{ij}} \right\rfloor + 1 \\
        N^{(0,L)} &= \left\lceil \frac{L}{T_{ij}} \right\rceil - 1 \\
        N^{[0,L)} &= \left\lceil \frac{L}{T_{ij}} \right\rceil
        \end{aligned}
        \tag{3}
        \]

        המנה \( L / T_{ij} = L\,(\omega_i - \omega_j) \) היא הפרש הסיבובים של שני המחוגים
        בקטע, כמו בסעיף א. כשהיא מספר שלם, הקצה \( L \) הוא בעצמו פגישה, והמספרים הם
        \( L / T_{ij} + 1 \), \( L / T_{ij} - 1 \) ו-\( L / T_{ij} \).

    4. **מציבים בשעון :** בשניות, \( t_s = 60 \), \( t_m = 3{,}600 \) ו-\( t_h = 43{,}200 \) :

        \[
        \begin{aligned}
        T_{sm} &= \frac{60 \cdot 3{,}600}{3{,}540} = \frac{3{,}600}{59} \\
        T_{sh} &= \frac{60 \cdot 43{,}200}{43{,}140} = \frac{43{,}200}{719} \\
        T_{mh} &= \frac{3{,}600 \cdot 43{,}200}{39{,}600} = \frac{43{,}200}{11}
        \end{aligned}
        \]

        עם \( L = 43{,}200 \), כלומר 12 שעות, המנות הן 708, 719 ו-11, ונוסחה 3 נותנת :

        <!-- gen 10 -->

        | הקטע | השניות והדקות | השניות והשעות | הדקות והשעות |
        |---|---|---|---|
        | סגור, \( 0 \le t \le L \) | ‏709 | ‏720 | ‏12 |
        | פתוח, \( 0 < t < L \) | ‏707 | ‏718 | ‏10 |
        | חצי פתוח, \( 0 \le t < L \) | ‏708 | ‏719 | ‏11 |
        | יממה, \( 0 \le t < 2L \) | ‏1,416 | ‏1,438 | ‏22 |

        <!-- /gen -->

    5. **פגישה של שלושה :** אם השניות פוגשות את הדקות והדקות פוגשות את השעות באותו רגע,
       אז לפי נוסחה 2 יש שלמים \( a \) ו-\( b \) עם

        \[
        \begin{aligned}
        \frac{3{,}600\,a}{59} &= \frac{43{,}200\,b}{11} \\
        \frac{a}{59} &= \frac{12\,b}{11} \\
        11\,a &= 708\,b
        \end{aligned}
        \tag{4}
        \]

        ‏\( 708 = 2^2 \cdot 3 \cdot 59 \), ולכן \( \gcd(11, 708) = 1 \). מכאן ש-11 מחלק את
        \( b \) : ‏\( b = 11c \), ‏\( a = 708c \), והזמן הוא

        \[
        t = \frac{43{,}200 \cdot 11c}{11} = 43{,}200\,c
        \]

        כלומר רק כפולות של 12 שעות. ביממה אלה \( c = 0 \) ו-\( c = 1 \) : ‏00:00 ו-12:00.

    6. **הכלה והפרדה :** רגע שבו נפגשים שני מחוגים בדיוק שייך לזוג אחד, ורגע של שלושה
       שייך לשלושת הזוגות. אין רגע ששייך לשני זוגות בדיוק. לכן מספר הרגעים הוא

        \[
        N = N_{sm} + N_{sh} + N_{mh} - 2\,N_{smh}
        \]

    7. **התשובה :** ביממה, \( 0 \le t < 86{,}400 \), נוסחה 3 בקטע חצי פתוח נותנת 1,416,
       1,438 ו-22, ונוסחה 4 נותנת \( N_{smh} = 2 \) :

        \[
        N = 1{,}416 + 1{,}438 + 22 - 2 \cdot 2 = 2{,}872
        \]

        ובקטע הפתוח של 12 שעות אין פגישה של שלושה, ולכן
        \( N = 707 + 718 + 10 = 1{,}435 \), כמו בבדיקה של סעיף א.

    </div>

    #### למה זה נכון { .sol-proof }

    **אותה הוכחה, בדרך של סעיף א.** בפגישה ה-\( k \) של הדקות והשעות,
    \( t = \tfrac{43{,}200\,k}{11} \). מחוג הדקות ומחוג השעות נמצאים ב-\( \tfrac{k}{11} \)
    סיבוב, אחרי שמורידים סיבובים שלמים. מחוג השניות נמצא ב-

    \[
    \frac{t}{60} = \frac{720\,k}{11} = 65\,k + \frac{5\,k}{11}
    \]

    כלומר ב-\( \tfrac{5k}{11} \) סיבוב. הם באותו מקום כש-\( \tfrac{5k - k}{11} = \tfrac{4k}{11} \)
    הוא מספר שלם, כלומר כש-11 מחלק את \( k \). זה בדיוק 00:00 ו-12:00.

    **מקרי קצה של הנוסחה.** כש-\( t_j \to \infty \), המחוג האיטי עומד במקום,
    ו-\( T_{ij} \to t_i \) : המהיר פוגש אותו פעם בסיבוב. כש-\( t_j \to t_i \), המרווח שואף
    לאינסוף : שני מחוגים באותה מהירות לא נפגשים שוב, או שהם תמיד יחד.

    **לנסות בעצמכם.** בתיבה הבאה הקו הוא ההפרש \( \theta_i - \theta_j \) בסיבובים, והקווים
    המקווקווים הם המספרים השלמים, כך שכל חיתוך הוא פגישה. בוחרים זוג מחוגים, את האורך
    \( L \) ברבעים של \( T_{ij} \) ואת סוג הקטע, ונקודה מלאה היא פגישה שנספרת. כשהקצה
    \( L \) נופל על מספר שלם, שלוש הספירות של נוסחה 3 שונות, והן נבדלות רק בשני הקצוות.

    <div class="explorer" data-kind="gapline" data-pair="mh" data-r="3"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להכפיל את 12 השעות ב-2"
    בתוך 12 שעות, בלי הקצוות, יש 1,435 פגישות. מי שמכפיל ב-2 מקבל 2,870 ומפספס את 00:00
    ואת 12:00, שני רגעים שבהם שלושת המחוגים נפגשים. התשובה היא 2,872.

??? trap "מלכודת : לחבר את שלושת הזוגות"
    הסכום 2,876 סופר כל אחד מהרגעים 00:00 ו-12:00 שלוש פעמים, פעם בכל זוג. השאלה שואלת
    על רגעים, ולכן מורידים 2 על כל אחד מהם.

??? trap "מלכודת : פגישה של הדקות והשעות בכל שעה"
    הדקות והשעות נפגשים כל שעה, 5 דקות ו-27 שניות, ולא כל שעה עגולה. לכן יש 22 פגישות
    ביממה ולא 24 : בין 11:00 ל-12:00 אין פגישה, והבאה היא ב-12:00 עצמה.

??? trap "מלכודת : מחוג השניות פוגש את שניהם יחד"
    מחוג השניות עובר את מחוג השעות ואת מחוג הדקות כמעט באותו זמן, אבל לא באותו רגע. אחרי
    הדקה הראשונה ההפרש כמעט שנייה, ובמקום הצפוף ביותר ביממה הוא רק
    \( \tfrac{3{,}600}{42{,}421} \approx 0.085 \) שניות, אבל אף פעם לא אפס, חוץ מ-00:00
    ומ-12:00. אלה שתי פגישות נפרדות, ושתיהן נספרות.

??? trap "מלכודת : לספור גם את חצות של סוף היממה"
    הרגע 24:00 הוא 00:00 של היממה הבאה. מי שסופר גם אותו מקבל 2,873, ומי שסופר יום אחרי
    יום יספור כל חצות פעמיים.

??? followup "שאלות המשך"
    - **שבוע :** כמה פגישות יש בשבוע?

        ??? fu-answer "תשובה"
            בדיוק \( 7 \cdot 2{,}872 = 20{,}104 \), כי כל יממה מתחילה ב-00:00 ונגמרת לפני החצות
            הבאה, ולכן אף פגישה לא נספרת פעמיים.

    - **לוח של 24 שעות :** מה התשובה אם מחוג השעות מסיים סיבוב ביממה?

        ??? fu-answer "תשובה"
            בסך הכול 2,876 : השניות מקיפות את השעות \( 1{,}440 - 1 = 1{,}439 \) פעמים,
            הדקות \( 24 - 1 = 23 \) פעמים, והשניות את הדקות 1,416 פעמים כמו קודם. שלושתם נפגשים
            רק ב-00:00, ולכן \( 1{,}416 + 1{,}439 + 23 - 2 = 2{,}876 \).

    - **מחוגים מנוגדים :** כמה פעמים ביממה מחוג הדקות ומחוג השעות על קו ישר, בכיוונים
      הפוכים?

        ??? fu-answer "תשובה"
            בדיוק 22 : ההפרש ביניהם גדל ב-22 סיבובים ביממה, והם מנוגדים כשהוא חצי סיבוב, סיבוב
            וחצי, וכן הלאה עד 21.5 סיבובים.

    - **זווית ישרה :** כמה פעמים ביממה יש זווית של 90 מעלות בין מחוג הדקות למחוג השעות?

        ??? fu-answer "תשובה"
            בדיוק 44 : בכל אחד מ-22 הסיבובים שההפרש מרוויח, הוא עובר פעם ברבע סיבוב ופעם בשלושה
            רבעים.

    - **מחוג שניות שקופץ :** אם מחוג השניות קופץ פעם בשנייה, ופגישה היא רק כששני המחוגים
      מצביעים לאותו כיוון ממש, כמה פגישות יש?

        ??? fu-answer "תשובה"
            בסך הכול 44 : השניות והדקות נפגשות רק בשעות עגולות (24), השניות והשעות רק ב-00:00
            וב-12:00, ונשארות 22 הפגישות של הדקות והשעות. הרגעים 00:00 ו-12:00 נמצאים בשלוש
            הקבוצות, ולכן \( 24 + 2 + 22 - 2 \cdot 2 = 44 \).
