---
id: 76
title: פונקציה עולה עם f(f(n)) = 3n
level: junior
difficulty: medium
kind: math
tags: [math, number-theory, number-bases, proof]
source: ""
added: 2026-11-03
---

## השאלה

נתונה פונקציה \( f \) מהמספרים הטבעיים למספרים הטבעיים. הטבעיים כאן הם \( 1, 2, 3, \dots \),
בלי 0. ידוע עליה :

- **עולה ממש :** אם \( m < n \) אז \( f(m) < f(n) \).
- **התנאי :** לכל \( n \) מתקיים \( f(f(n)) = 3n \).

אין נוסחה ל-\( f \), רק שני התנאים האלה. מתברר שהם מספיקים כדי לחשב כל ערך שלה.

??? interviewer "מה המראיין בודק"
    - **להתחיל מהקטן :** לא לנחש נוסחה, אלא לבדוק מה התנאים מרשים בערך הראשון \( f(1) \).
    - **להשתמש בתנאי שוב ושוב :** כל ערך שמוצאים נותן ערך נוסף, וכך נבנית שרשרת של ערכים ידועים.
    - **לספור :** האם המועמד רואה ששני ערכים ידועים של פונקציה עולה ממש יכולים לקבוע את כל
      הערכים שביניהם.
    - **הוכחה מלאה :** להראות שהנוסחה הכללית היא היחידה, ולא רק שהיא עובדת.

---

### סעיף א – כמה זה f(14)

חשבו את \( f(14) \).

??? tip "רמז 1"
    מה יכול להיות \( f(1) \)? נסו \( f(1) = 1 \), ‏\( f(1) = 2 \) ו-\( f(1) \ge 3 \), ובדקו כל
    אפשרות מול שני התנאים.

??? tip "רמז 2"
    כש-\( f(1) \) ידוע, התנאי נותן ערך חדש : \( f(f(1)) = 3 \). המשיכו כך : כל ערך שמצאתם
    הוא נקודת התחלה לערך הבא. אילו מספרים מופיעים בשרשרת?

??? tip "רמז 3"
    בשרשרת מופיעים \( f(9) \) ו-\( f(18) \). מה אפשר לומר על הערכים של \( f \) בין 9
    ל-18?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏\( f(14) = 23 \). ‏\( f(1) = 2 \) הוא הערך היחיד האפשרי, ממנו השרשרת נותנת
        \( f(9) = 18 \) ו-\( f(18) = 27 \), ובין שני אלה \( f \) עולה בדיוק ב-1 בכל צעד.

    #### הרעיון { .sol-idea }

    שני ערכים ידועים של \( f \) לא מספיקים בדרך כלל כדי לדעת מה קורה ביניהם. כאן הם מספיקים :
    כשהעלייה הכוללת שווה למספר הצעדים, כל צעד עולה בדיוק ב-1.

    <!-- gen 0 -->

    <svg class="figure" viewBox="0 0 640 168" style="max-width:40rem" role="img" aria-label="סעיף א : המספרים 9 עד 18 למעלה, והערכים 18 עד 27 למטה. הקצוות ידועים מהשרשרת, תשעה צעדים ועלייה של תשע, ולכן כל n עולה ל-n + 9, ו-14 עולה ל-23"><text class="legend" x="62" y="40" text-anchor="end" style="font-size:17px">n</text><text class="legend" x="62" y="142" text-anchor="end" style="font-size:17px">f(n)</text><line class="s1-line" x1="92" y1="48" x2="92" y2="116" stroke-width="3"/><circle class="s1-dot" cx="92" cy="34" r="6"><title>n = 9</title></circle><circle class="s1-dot" cx="92" cy="136" r="6"><title>f(9) = 18</title></circle><text class="tick" x="92" y="21" text-anchor="middle" style="font-size:16px">9</text><text class="tick" x="92" y="162" text-anchor="middle" style="font-size:16px">18</text><line class="ink-line" x1="146" y1="48" x2="146" y2="116" stroke-width="1.4"/><circle class="ink-dot" cx="146" cy="34" r="4.5"><title>n = 10</title></circle><circle class="ink-dot" cx="146" cy="136" r="4.5"><title>f(10) = 19</title></circle><text class="tick" x="146" y="21" text-anchor="middle" style="font-size:16px">10</text><text class="tick" x="146" y="162" text-anchor="middle" style="font-size:16px">19</text><line class="ink-line" x1="200" y1="48" x2="200" y2="116" stroke-width="1.4"/><circle class="ink-dot" cx="200" cy="34" r="4.5"><title>n = 11</title></circle><circle class="ink-dot" cx="200" cy="136" r="4.5"><title>f(11) = 20</title></circle><text class="tick" x="200" y="21" text-anchor="middle" style="font-size:16px">11</text><text class="tick" x="200" y="162" text-anchor="middle" style="font-size:16px">20</text><line class="ink-line" x1="254" y1="48" x2="254" y2="116" stroke-width="1.4"/><circle class="ink-dot" cx="254" cy="34" r="4.5"><title>n = 12</title></circle><circle class="ink-dot" cx="254" cy="136" r="4.5"><title>f(12) = 21</title></circle><text class="tick" x="254" y="21" text-anchor="middle" style="font-size:16px">12</text><text class="tick" x="254" y="162" text-anchor="middle" style="font-size:16px">21</text><line class="ink-line" x1="308" y1="48" x2="308" y2="116" stroke-width="1.4"/><circle class="ink-dot" cx="308" cy="34" r="4.5"><title>n = 13</title></circle><circle class="ink-dot" cx="308" cy="136" r="4.5"><title>f(13) = 22</title></circle><text class="tick" x="308" y="21" text-anchor="middle" style="font-size:16px">13</text><text class="tick" x="308" y="162" text-anchor="middle" style="font-size:16px">22</text><line class="s2-line" x1="362" y1="48" x2="362" y2="116" stroke-width="3"/><circle class="s2-dot" cx="362" cy="34" r="6"><title>n = 14</title></circle><circle class="s2-dot" cx="362" cy="136" r="6"><title>f(14) = 23</title></circle><text class="tick" x="362" y="21" text-anchor="middle" style="font-size:16px">14</text><text class="tick" x="362" y="162" text-anchor="middle" style="font-size:16px">23</text><line class="ink-line" x1="416" y1="48" x2="416" y2="116" stroke-width="1.4"/><circle class="ink-dot" cx="416" cy="34" r="4.5"><title>n = 15</title></circle><circle class="ink-dot" cx="416" cy="136" r="4.5"><title>f(15) = 24</title></circle><text class="tick" x="416" y="21" text-anchor="middle" style="font-size:16px">15</text><text class="tick" x="416" y="162" text-anchor="middle" style="font-size:16px">24</text><line class="ink-line" x1="470" y1="48" x2="470" y2="116" stroke-width="1.4"/><circle class="ink-dot" cx="470" cy="34" r="4.5"><title>n = 16</title></circle><circle class="ink-dot" cx="470" cy="136" r="4.5"><title>f(16) = 25</title></circle><text class="tick" x="470" y="21" text-anchor="middle" style="font-size:16px">16</text><text class="tick" x="470" y="162" text-anchor="middle" style="font-size:16px">25</text><line class="ink-line" x1="524" y1="48" x2="524" y2="116" stroke-width="1.4"/><circle class="ink-dot" cx="524" cy="34" r="4.5"><title>n = 17</title></circle><circle class="ink-dot" cx="524" cy="136" r="4.5"><title>f(17) = 26</title></circle><text class="tick" x="524" y="21" text-anchor="middle" style="font-size:16px">17</text><text class="tick" x="524" y="162" text-anchor="middle" style="font-size:16px">26</text><line class="s1-line" x1="578" y1="48" x2="578" y2="116" stroke-width="3"/><circle class="s1-dot" cx="578" cy="34" r="6"><title>n = 18</title></circle><circle class="s1-dot" cx="578" cy="136" r="6"><title>f(18) = 27</title></circle><text class="tick" x="578" y="21" text-anchor="middle" style="font-size:16px">18</text><text class="tick" x="578" y="162" text-anchor="middle" style="font-size:16px">27</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="s1"></i>ידוע מהשרשרת : ‏\( f(9) = 18 \), ‏\( f(18) = 27 \)</span><span><i class="ink"></i>נקבע בספירה : כל צעד עולה ב-1</span><span><i class="s2"></i>‏\( f(14) = 23 \)</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הערך הראשון :** אם \( f(1) = 1 \), אז \( f(f(1)) = f(1) = 1 \), ולא 3. אם
       \( f(1) = a \ge 3 \), אז מהתנאי \( f(a) = 3 \). אבל \( a > 1 \) ו-\( f \) עולה ממש,
       ולכן \( f(a) > f(1) = a \ge 3 \), סתירה. נשאר רק \( f(1) = 2 \).

    2. **השרשרת :** מכאן כל ערך נותן את הבא, כי \( f(f(m)) = 3m \) :

        \[
        \begin{aligned}
        f(2) &= f(f(1)) = 3 \cdot 1 = 3 \\
        f(3) &= f(f(2)) = 3 \cdot 2 = 6 \\
        f(6) &= f(f(3)) = 3 \cdot 3 = 9 \\
        f(9) &= f(f(6)) = 3 \cdot 6 = 18 \\
        f(18) &= f(f(9)) = 3 \cdot 9 = 27
        \end{aligned}
        \]

    3. **ספירת מקומות :** מ-9 עד 18 יש 9 צעדים, והערכים עולים מ-18 ל-27, כלומר ב-9 :

        \[
        18 = f(9) < f(10) < \dots < f(18) = 27
        \]

        כל אחת מתשע העליות היא לפחות 1, והסכום שלהן הוא 9. לכן כל עלייה היא בדיוק 1,
        ו-\( f(9 + j) = 18 + j \) לכל \( 0 \le j \le 9 \).

    4. **התשובה :** ‏\( 14 = 9 + 5 \), ולכן \( f(14) = 18 + 5 = 23 \).

    5. **בדיקה :** ‏\( f(9) = 18 < f(14) = 23 < f(18) = 27 \), כמו שפונקציה עולה דורשת. מהתנאי
       \( f(23) = f(f(14)) = 3 \cdot 14 = 42 \), וגם זה מתאים : \( 18 < 23 < 27 \), ולכן
       \( f(23) \) צריך להיות בין \( f(18) = 27 \) ל-\( f(27) = f(f(18)) = 54 \).

    </div>

    #### למה זה נכון { .sol-proof }

    **למה הספירה עובדת.** ‏\( f \) מקבלת רק ערכים שלמים, ולכן "עולה ממש" פירושו
    \( f(n + 1) \ge f(n) + 1 \). אם אחת העליות בין 9 ל-18 הייתה 2 או יותר, הסכום של כל
    התשע היה לפחות 10, ו-\( f(18) \) היה לפחות 28. אבל \( f(18) = 27 \).

    **אותו טיעון קודם, בקטן.** בין \( f(3) = 6 \) ל-\( f(6) = 9 \) יש שלושה צעדים ועלייה
    של שלוש, ולכן \( f(4) = 7 \) ו-\( f(5) = 8 \). בסעיף ב זה הופך לכלל לכל הקטעים.

---

### סעיף ב – הנוסחה הכללית

מצאו את \( f(n) \) לכל \( n \), והוכיחו שזו הפונקציה היחידה שמקיימת את שני התנאים.

??? tip "רמז 1"
    בשרשרת של סעיף א הופיעו 1, 2, 3, 6, 9, 18, 27. נחשו מה זה \( f(3^k) \) ומה זה
    \( f(2 \cdot 3^k) \), והוכיחו באינדוקציה.

??? tip "רמז 2"
    בין \( 3^k \) ל-\( 2 \cdot 3^k \) : אותה ספירה כמו בסעיף א. כמה צעדים, ובכמה \( f \)
    עולה?

??? tip "רמז 3"
    מספר \( n \) בין \( 2 \cdot 3^k \) ל-\( 3^{k+1} \) הוא ערך של \( f \) על החצי הראשון של
    אותו קטע : \( n = f(m) \). מה זה אומר על \( f(n) = f(f(m)) \)?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        לכל \( n \) יש \( k \ge 0 \) עם \( 3^k \le n \le 3^{k+1} \), ואז
        \( f(n) = n + 3^k \) כש-\( n \le 2 \cdot 3^k \), ו-\( f(n) = 3n - 3^{k+1} \)
        כש-\( n \ge 2 \cdot 3^k \). בבסיס 3 : ספרה מובילה 1 הופכת ל-2, וספרה מובילה 2 הופכת
        ל-1 עם 0 נוסף בסוף.

    #### הרעיון { .sol-idea }

    השרשרת של סעיף א נותנת "עוגנים" : הערכים ב-\( 3^k \) וב-\( 2 \cdot 3^k \). בחצי הראשון
    של כל קטע הספירה של סעיף א עובדת, ו-\( f \) עולה בשיפוע 1. בחצי השני הספירה כבר לא
    מספיקה, אבל כל מספר שם הוא ערך של \( f \) מהחצי הראשון, והתנאי \( f(f(m)) = 3m \) נותן
    שיפוע 3. הגרף מתחלף בין שני השיפועים, ונשאר בין \( 1.5n \) ל-\( 2n \), משני צדי הקו
    \( \sqrt{3}\,n \) :

    <!-- gen 2 -->

    <svg class="perf-chart" viewBox="0 0 640 300" style="max-width:40rem" role="img" aria-label="סעיף ב : הגרף של f עד 27. מ-3 בחזקת k עד פעמיים 3 בחזקת k הגרף עולה בשיפוע 1, ומשם עד 3 בחזקת k + 1 בשיפוע 3; העוגנים מסומנים, והקו המקווקו הוא שורש 3 כפול n"><line class="grid" x1="46" x2="628" y1="262.0" y2="262.0"/><text class="tick" x="38" y="266.0" text-anchor="end">0</text><line class="grid" x1="46" x2="628" y1="220.7" y2="220.7"/><text class="tick" x="38" y="224.7" text-anchor="end">9</text><line class="grid" x1="46" x2="628" y1="179.3" y2="179.3"/><text class="tick" x="38" y="183.3" text-anchor="end">18</text><line class="grid" x1="46" x2="628" y1="138.0" y2="138.0"/><text class="tick" x="38" y="142.0" text-anchor="end">27</text><line class="grid" x1="46" x2="628" y1="96.7" y2="96.7"/><text class="tick" x="38" y="100.7" text-anchor="end">36</text><line class="grid" x1="46" x2="628" y1="55.3" y2="55.3"/><text class="tick" x="38" y="59.3" text-anchor="end">45</text><line class="grid" x1="46" x2="628" y1="14.0" y2="14.0"/><text class="tick" x="38" y="18.0" text-anchor="end">54</text><line class="grid" x1="67.1" x2="67.1" y1="8" y2="262" stroke-dasharray="4 4"/><text class="tick" x="67.1" y="280" text-anchor="middle">1</text><line class="grid" x1="88.2" x2="88.2" y1="8" y2="262" stroke-dasharray="4 4"/><text class="tick" x="88.2" y="280" text-anchor="middle">2</text><line class="grid" x1="109.3" x2="109.3" y1="8" y2="262" stroke-dasharray="4 4"/><text class="tick" x="109.3" y="280" text-anchor="middle">3</text><line class="grid" x1="172.5" x2="172.5" y1="8" y2="262" stroke-dasharray="4 4"/><text class="tick" x="172.5" y="280" text-anchor="middle">6</text><line class="grid" x1="235.8" x2="235.8" y1="8" y2="262" stroke-dasharray="4 4"/><text class="tick" x="235.8" y="280" text-anchor="middle">9</text><line class="grid" x1="425.6" x2="425.6" y1="8" y2="262" stroke-dasharray="4 4"/><text class="tick" x="425.6" y="280" text-anchor="middle">18</text><line class="grid" x1="615.3" x2="615.3" y1="8" y2="262" stroke-dasharray="4 4"/><text class="tick" x="615.3" y="280" text-anchor="middle">27</text><line class="axis" x1="46" x2="628" y1="262" y2="262"/><polyline class="ink-line" points="46.0,262.0 628.0,42.5" fill="none" stroke-width="1.5" stroke-dasharray="6 4"/><line class="s1-line" x1="67.1" y1="252.8" x2="88.2" y2="248.2" stroke-width="2.5"/><line class="s3-line" x1="88.2" y1="248.2" x2="109.3" y2="234.4" stroke-width="2.5"/><line class="s1-line" x1="109.3" y1="234.4" x2="172.5" y2="220.7" stroke-width="2.5"/><line class="s3-line" x1="172.5" y1="220.7" x2="235.8" y2="179.3" stroke-width="2.5"/><line class="s1-line" x1="235.8" y1="179.3" x2="425.6" y2="138.0" stroke-width="2.5"/><line class="s3-line" x1="425.6" y1="138.0" x2="615.3" y2="14.0" stroke-width="2.5"/><circle class="s1-dot" cx="130.3" cy="229.9" r="3.2"><title>f(4) = 7</title></circle><circle class="s1-dot" cx="151.4" cy="225.3" r="3.2"><title>f(5) = 8</title></circle><circle class="s3-dot" cx="193.6" cy="206.9" r="3.2"><title>f(7) = 12</title></circle><circle class="s3-dot" cx="214.7" cy="193.1" r="3.2"><title>f(8) = 15</title></circle><circle class="s1-dot" cx="256.9" cy="174.7" r="3.2"><title>f(10) = 19</title></circle><circle class="s1-dot" cx="278.0" cy="170.1" r="3.2"><title>f(11) = 20</title></circle><circle class="s1-dot" cx="299.0" cy="165.6" r="3.2"><title>f(12) = 21</title></circle><circle class="s1-dot" cx="320.1" cy="161.0" r="3.2"><title>f(13) = 22</title></circle><circle class="s1-dot" cx="341.2" cy="156.4" r="3.2"><title>f(14) = 23</title></circle><circle class="s1-dot" cx="362.3" cy="151.8" r="3.2"><title>f(15) = 24</title></circle><circle class="s1-dot" cx="383.4" cy="147.2" r="3.2"><title>f(16) = 25</title></circle><circle class="s1-dot" cx="404.5" cy="142.6" r="3.2"><title>f(17) = 26</title></circle><circle class="s3-dot" cx="446.7" cy="124.2" r="3.2"><title>f(19) = 30</title></circle><circle class="s3-dot" cx="467.7" cy="110.4" r="3.2"><title>f(20) = 33</title></circle><circle class="s3-dot" cx="488.8" cy="96.7" r="3.2"><title>f(21) = 36</title></circle><circle class="s3-dot" cx="509.9" cy="82.9" r="3.2"><title>f(22) = 39</title></circle><circle class="s3-dot" cx="531.0" cy="69.1" r="3.2"><title>f(23) = 42</title></circle><circle class="s3-dot" cx="552.1" cy="55.3" r="3.2"><title>f(24) = 45</title></circle><circle class="s3-dot" cx="573.2" cy="41.6" r="3.2"><title>f(25) = 48</title></circle><circle class="s3-dot" cx="594.3" cy="27.8" r="3.2"><title>f(26) = 51</title></circle><circle class="s2-dot" cx="67.1" cy="252.8" r="5"><title>f(1) = 2</title></circle><circle class="s2-dot" cx="88.2" cy="248.2" r="5"><title>f(2) = 3</title></circle><circle class="s2-dot" cx="109.3" cy="234.4" r="5"><title>f(3) = 6</title></circle><circle class="s2-dot" cx="172.5" cy="220.7" r="5"><title>f(6) = 9</title></circle><circle class="s2-dot" cx="235.8" cy="179.3" r="5"><title>f(9) = 18</title></circle><circle class="s2-dot" cx="425.6" cy="138.0" r="5"><title>f(18) = 27</title></circle><circle class="s2-dot" cx="615.3" cy="14.0" r="5"><title>f(27) = 54</title></circle><text class="legend" x="569.0" y="48.6" text-anchor="end">√3 · n</text></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="s1"></i>‏\( 3^k \le n \le 2 \cdot 3^k \) : שיפוע 1</span><span><i class="by-bfs"></i>‏\( 2 \cdot 3^k \le n \le 3^{k+1} \) : שיפוע 3</span><span><i class="s2"></i>העוגנים \( 3^k \) ו-\( 2 \cdot 3^k \)</span><span><i class="ink-dash"></i>‏\( \sqrt{3}\,n \), להשוואה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **העוגנים :** לכל \( k \ge 0 \) :

        \[
        f(3^k) = 2 \cdot 3^k, \qquad f(2 \cdot 3^k) = 3^{k+1}
        \]

        באינדוקציה על \( k \). עבור \( k = 0 \) זה \( f(1) = 2 \) ו-\( f(2) = 3 \) מסעיף א.
        אם \( f(3^k) = 2 \cdot 3^k \), אז \( f(2 \cdot 3^k) = f(f(3^k)) = 3^{k+1} \),
        ו-\( f(3^{k+1}) = f(f(2 \cdot 3^k)) = 2 \cdot 3^{k+1} \).

    2. **החצי הראשון :** מ-\( 3^k \) עד \( 2 \cdot 3^k \) יש \( 3^k \) צעדים, והערכים עולים
       מ-\( 2 \cdot 3^k \) ל-\( 3^{k+1} \), כלומר ב-\( 3^k \). כמו בסעיף א, כל צעד עולה
       בדיוק ב-1 :

        \[
        f(n) = n + 3^k, \qquad 3^k \le n \le 2 \cdot 3^k
        \]

    3. **החצי השני :** אם \( 2 \cdot 3^k \le n \le 3^{k+1} \), אז \( m = n - 3^k \) נמצא
       בחצי הראשון, ולפי הצעד הקודם \( f(m) = m + 3^k = n \). לכן :

        \[
        \begin{aligned}
        f(n) &= f(f(m)) = 3m \\
             &= 3n - 3^{k+1}
        \end{aligned}
        \]

    4. **כל \( n \) מכוסה :** כל \( n \ge 1 \) נמצא בקטע \( [3^k, 3^{k+1}] \) של \( k \)
       כלשהו. בנקודות המעבר, \( 2 \cdot 3^k \) בין החצאים ו-\( 3^{k+1} \) בין הקטעים, שתי
       הנוסחאות נותנות את אותו ערך, ולכן לא משנה באיזו משתמשים.

    5. **בדיקה מול סעיף א :** ‏\( 9 \le 14 \le 18 \), כלומר \( k = 2 \) והחצי הראשון :
       \( f(14) = 14 + 9 = 23 \).

    </div>

    #### למה זה נכון { .sol-proof }

    **יחידות.** כל צעד למעלה נבע משני התנאים בלבד : \( f(1) = 2 \) נכפה, העוגנים נכפו
    באינדוקציה, החצי הראשון בספירה והחצי השני מהתנאי. לכן אין פונקציה אחרת שמקיימת אותם.

    **קיום.** צריך גם לבדוק שהנוסחה באמת מקיימת את התנאים, ולא רק שהיא היחידה האפשרית :

    - **בחצי הראשון :** ‏\( f \) שולחת את \( [3^k, 2 \cdot 3^k] \) על \( [2 \cdot 3^k, 3^{k+1}] \),
      החצי השני של אותו קטע. לכן

        \[
        \begin{aligned}
        f(f(n)) &= 3(n + 3^k) - 3^{k+1} \\
                &= 3n
        \end{aligned}
        \]

    - **בחצי השני :** ‏\( f \) שולחת את \( [2 \cdot 3^k, 3^{k+1}] \) על
      \( [3^{k+1}, 2 \cdot 3^{k+1}] \), החצי הראשון של הקטע הבא. לכן

        \[
        \begin{aligned}
        f(f(n)) &= (3n - 3^{k+1}) + 3^{k+1} \\
                &= 3n
        \end{aligned}
        \]

    - **עולה ממש :** בכל חצי השיפוע הוא 1 או 3, ובנקודות המעבר שתי הנוסחאות שוות, ולכן
      \( f \) עולה בכל צעד.

    **בבסיס 3.** מספר עם \( k + 1 \) ספרות בבסיס 3 נמצא בין \( 3^k \) ל-\( 3^{k+1} \). הספרה
    המובילה שלו היא 1 בדיוק כש-\( 3^k \le n < 2 \cdot 3^k \), כלומר \( n = 3^k + r \) עם
    \( r < 3^k \). אז
    \( f(n) = 2 \cdot 3^k + r \) : אותן ספרות, והמובילה הופכת ל-2. בחצי השני
    \( n = 2 \cdot 3^k + r \), ואז \( f(n) = 3(3^k + r) \) : המובילה הופכת ל-1, וכפל ב-3
    מוסיף 0 בסוף. פעמיים הכלל נותן את \( n \) עם 0 בסוף, כלומר \( 3n \) :

    <!-- gen 4 -->

    | ‏\( n \) | בבסיס 3 | הספרה המובילה | ‏\( f(n) \) בבסיס 3 | ‏\( f(n) \) |
    |---|---|---|---|---|
    | 5 | <span dir="ltr">12</span> | 1 הופכת ל-2 | <span dir="ltr">22</span> | 8 |
    | 7 | <span dir="ltr">21</span> | 2 הופכת ל-1, ו-0 בסוף | <span dir="ltr">110</span> | 12 |
    | 14 | <span dir="ltr">112</span> | 1 הופכת ל-2 | <span dir="ltr">212</span> | 23 |
    | 23 | <span dir="ltr">212</span> | 2 הופכת ל-1, ו-0 בסוף | <span dir="ltr">1120</span> | 42 |
    | 2027 | <span dir="ltr">2210002</span> | 2 הופכת ל-1, ו-0 בסוף | <span dir="ltr">12100020</span> | 3894 |

    <!-- /gen -->

    נסו בתיבה : מ-\( n = 14 \) לחצו ארבע פעמים "הבא בשרשרת". השרשרת היא
    <span dir="ltr">14 → 23 → 42 → 69 → 126</span>, ובבסיס 3
    <span dir="ltr">112, 212, 1120, 2120, 11200</span> : הספרה המובילה מתחלפת בין 1 ל-2, ובכל
    צעד שני נוסף 0. הקלידו 17 ולחצו פעמיים "n + 1" : הערכים הם 26, 27 ו-30, כי ב-18, אמצע
    הקטע, השיפוע עובר מ-1 ל-3. ב-26, 27 ו-28 הערכים הם 51, 54 ו-55 : ב-27 מתחיל קטע חדש,
    השיפוע חוזר ל-1, ובבסיס 3 נוספת ספרה. ב-60 וב-61 הערכים הם 99 ו-102, ו-100 ו-101
    מדולגים, כמו בשאלת ההמשך. מעבר לטבלה, בתיבה יש כל \( n \) עד 999,999,999, והחישוב של כל
    ערך מהעוגנים :

    <div class="explorer" data-kind="ffn" data-n="14"></div>

---

### סעיף ג – כמה זה f(2027)

חשבו את \( f(2027) \).

??? tip "רמז 1"
    מצאו את \( k \) שבשבילו \( 3^k \le 2027 \le 3^{k+1} \).

??? tip "רמז 2"
    באיזה חצי של הקטע נמצא 2027? השוו אותו ל-\( 2 \cdot 3^k \).

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏\( f(2027) = 3894 \). המספר נמצא בחצי השני של הקטע \( [729, 2187] \), ולכן
        \( f(2027) = 3 \cdot 2027 - 2187 \).

    #### הרעיון { .sol-idea }

    מספיק לדעת באיזה קטע ובאיזה חצי שלו נמצא 2027, ולהציב בנוסחה של סעיף ב.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הקטע :** ‏\( 3^6 = 729 \) ו-\( 3^7 = 2187 \), ולכן \( 729 \le 2027 \le 2187 \)
       ו-\( k = 6 \).

    2. **החצי :** ‏\( 2 \cdot 3^6 = 1458 \le 2027 \), כלומר החצי השני.

    3. **הנוסחה :**

        \[
        \begin{aligned}
        f(2027) &= 3 \cdot 2027 - 3^7 \\
                &= 6081 - 2187 = 3894
        \end{aligned}
        \]

    4. **בדיקה :** ‏3894 נמצא בחצי הראשון של \( [2187, 6561] \), כי
       \( 2187 \le 3894 \le 4374 \). לכן \( f(3894) = 3894 + 2187 = 6081 = 3 \cdot 2027 \).

    5. **בבסיס 3 :** ‏<span dir="ltr">2027 = 2210002</span> בבסיס 3, ספרה מובילה 2. היא
       הופכת ל-1 ו-0 נוסף בסוף : <span dir="ltr">12100020</span>, שהוא 3894.

    </div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לנחש f(n) = √3 · n"
    היחס \( f(n) / n \) נשאר בין 1.5 ל-2, משני צדי \( \sqrt{3} \approx 1.73 \), ולכן קל לנחש
    פונקציה ליניארית \( f(n) = cn \) עם \( c^2 = 3 \). אבל \( \sqrt{3}\,n \) לא שלם, ואף
    פונקציה ליניארית עם \( c^2 = 3 \) לא מחזירה טבעיים. הפתרון האמיתי מתחלף בין שיפוע 1
    לשיפוע 3.

??? trap "מלכודת : להתחיל מ-f(1) = 1"
    פונקציה עולה ממש על הטבעיים מקיימת \( f(n) \ge n \), וקל להניח ש-\( f(1) = 1 \). אבל אז
    \( f(f(1)) = 1 \ne 3 \). הנקודה הראשונה היא להוכיח ש-\( f(1) = 2 \), ולא להניח אותה.

??? trap "מלכודת : לספור גם בחצי השני"
    בחצי השני, מ-\( 2 \cdot 3^k \) עד \( 3^{k+1} \), הערכים עולים ב-\( 3 \cdot 3^k \)
    ב-\( 3^k \) צעדים בלבד. ספירה לבדה לא קובעת איך העלייה מתחלקת בין הצעדים. כאן צריך את
    התנאי : כל \( n \) בחצי הזה הוא \( f(m) \), ולכן \( f(n) = 3m \).

??? trap "מלכודת : לספור בלי שני העוגנים"
    הטיעון של סעיף א עובד רק כשידועים שני הקצוות, \( f(3^k) = 2 \cdot 3^k \)
    ו-\( f(2 \cdot 3^k) = 3^{k+1} \). ערך אחד ידוע ושיפוע "סביר" אינם הוכחה. לכן קודם מוכיחים
    את העוגנים באינדוקציה, ורק אז סופרים.

??? followup "שאלות המשך"
    - **מתי \( f(n) = 2n \) :** לאילו \( n \)?

        ??? fu-answer "תשובה"
            רק בחזקות של 3. בחצי הראשון \( n + 3^k = 2n \) נותן \( n = 3^k \), ובחצי השני
            \( 3n - 3^{k+1} = 2n \) נותן \( n = 3^{k+1} \).

    - **ערך של \( f \) :** האם 100 הוא \( f(m) \) של \( m \) כלשהו?

        ??? fu-answer "תשובה"
            לא. ‏\( 81 \le 100 \le 162 \), והערכים בקטע הזה באים מהחצי השני של הקטע
            הקודם : \( f(m) = 3m - 81 \), תמיד כפולה של 3. ‏100 לא מתחלק ב-3.

    - **פי 2 במקום פי 3 :** האם יש פונקציה עולה ממש עם \( f(f(n)) = 2n \)?

        ??? fu-answer "תשובה"
            לא. ‏\( f(1) = 1 \) נותן 1 ולא 2. ‏\( f(1) = 2 \) נותן \( f(2) = 2 \), אבל
            \( f(2) > f(1) = 2 \). ו-\( f(1) = a \ge 3 \) נותן \( f(a) = 2 \), אבל
            \( f(a) > f(1) \ge 3 \).

    - **עם 0 :** מה משתנה אם הטבעיים מתחילים ב-0?

        ??? fu-answer "תשובה"
            רק \( f(0) = 0 \) נוסף. אם \( f(0) = a > 0 \), אז \( f(a) = 0 \), אבל
            \( f(a) > f(0) = a > 0 \). משם הכול כמו קודם : \( f(1) > f(0) = 0 \), וההוכחה ש-\( f(1) = 2 \) עובדת כמו שהיא.
