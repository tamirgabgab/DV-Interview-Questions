---
id: 104
title: תחנות דלק על מעגל – מאיזו תחנה אפשר להשלים סיבוב
level: junior
difficulty: medium
kind: code
tags: [algorithms, greedy, python, systemverilog]
source: "LeetCode 134 (Gas Station), ולמת המעגל של Dvoretzky ו-Motzkin (1947)"
added: 2026-11-13
---

## השאלה

על כביש מעגלי יש \( n \ge 1 \) תחנות דלק, ממוספרות 0 עד \( n - 1 \) בכיוון הנסיעה. בתחנה
\( i \) מקבלים `gas[i]` ליטרים, והנסיעה ממנה לתחנה הבאה (מ-\( n - 1 \) חוזרים ל-0) עולה
`cost[i]` ליטרים. המכל מתחיל **ריק** ואין לו גבול. מאיזו תחנה אפשר להתחיל ולהשלים סיבוב שלם,
כלומר לחזור אליה בלי שהמכל יירד אף פעם מתחת ל-0? אם אין תחנה כזו, החזירו
<span dir="ltr">−1</span>.

**ההקשר באימות :** טבעת של צמתים ברשת על שבב (ring NoC) שעובדת עם credits. כל צומת נותן
לחבילה credits, וכל קפיצה לצומת הבא צורכת כמה מהם. מאיזה צומת חבילה יכולה להקיף את הטבעת בלי
להיתקע בהמתנה ל-credit? מודל הייחוס של בודק כזה צריך את התשובה, ובודק טוב צריך גם לדעת אם היא
יחידה.

**הדוגמה :** <span dir="ltr">gas = [1, 2, 3, 4, 5]</span> ו-<span dir="ltr">cost = [3, 4, 5, 1, 2]</span>.
מתחנה 3 המכל אחרי כל קטע הוא <span dir="ltr">3, 6, 4, 2, 0</span>, ולכן התשובה 3. ליד כל תחנה
הדלק שבה, ועל כל קטע המחיר שלו :

<!-- gen 0 -->

<svg class="figure gs-fig" viewBox="0 0 360 316" style="max-width:22.5rem" direction="ltr" role="img" aria-label="הדוגמה : חמש תחנות על מעגל, 0 עד 4 בכיוון השעון. הדלק בתחנות 1, 2, 3, 4, 5 והמחיר של הקטעים 3, 4, 5, 1, 2. תחנה 3 מסומנת : ממנה אפשר להשלים סיבוב"><g class="gs-leg"><title>leg 0 → 1: costs 3</title><path d="M201.8,56.3 A104,104 0 0 1 266.7,100.5" fill="none"/><path class="gs-head" d="M270.0,105.8 L269.8,96.6 L262.1,101.1 Z"/><text class="gs-cost" x="225.8" y="99.4" text-anchor="middle">−3</text></g><g class="gs-leg"><title>leg 1 → 2: costs 4</title><path d="M283.5,147.3 A104,104 0 0 1 261.5,222.7" fill="none"/><path class="gs-head" d="M257.4,227.4 L266.1,224.5 L259.4,218.5 Z"/><text class="gs-cost" x="254.2" y="186.6" text-anchor="middle">−4</text></g><g class="gs-leg"><title>leg 2 → 3: costs 5</title><path d="M222.1,253.1 A104,104 0 0 1 143.7,255.5" fill="none"/><path class="gs-head" d="M137.9,253.1 L143.4,260.5 L147.0,252.2 Z"/><text class="gs-cost" x="180.0" y="240.5" text-anchor="middle">−5</text></g><g class="gs-leg"><title>leg 3 → 4: costs 1</title><path d="M102.6,227.4 A104,104 0 0 1 76.1,153.6" fill="none"/><path class="gs-head" d="M76.5,147.3 L71.3,154.8 L80.2,155.8 Z"/><text class="gs-cost" x="105.8" y="186.6" text-anchor="middle">−1</text></g><g class="gs-leg"><title>leg 4 → 0: costs 2</title><path d="M90.0,105.8 A104,104 0 0 1 152.1,57.8" fill="none"/><path class="gs-head" d="M158.2,56.3 L149.4,53.6 L151.3,62.4 Z"/><text class="gs-cost" x="134.2" y="99.4" text-anchor="middle">−2</text></g><g class="gs-st"><title>station 0: gas 1</title><circle cx="180.0" cy="54.0" r="17"/><text class="gs-num" x="180.0" y="59.0" text-anchor="middle">0</text><text class="gs-gas" x="180.0" y="25.0" text-anchor="middle">+1</text></g><g class="gs-st"><title>station 1: gas 2</title><circle cx="278.9" cy="125.9" r="17"/><text class="gs-num" x="278.9" y="130.9" text-anchor="middle">1</text><text class="gs-gas" x="311.2" y="120.4" text-anchor="middle">+2</text></g><g class="gs-st"><title>station 2: gas 3</title><circle cx="241.1" cy="242.1" r="17"/><text class="gs-num" x="241.1" y="247.1" text-anchor="middle">2</text><text class="gs-gas" x="261.1" y="274.6" text-anchor="middle">+3</text></g><g class="gs-st is-good"><title>station 3: gas 4</title><circle cx="118.9" cy="242.1" r="17"/><text class="gs-num" x="118.9" y="247.1" text-anchor="middle">3</text><text class="gs-gas" x="98.9" y="274.6" text-anchor="middle">+4</text></g><g class="gs-st"><title>station 4: gas 5</title><circle cx="81.1" cy="125.9" r="17"/><text class="gs-num" x="81.1" y="130.9" text-anchor="middle">4</text><text class="gs-gas" x="48.8" y="120.4" text-anchor="middle">+5</text></g></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="gs-key-gas"></i>הדלק שמקבלים בתחנה (+)</span><span><i class="gs-key-cost"></i>המחיר של הקטע לתחנה הבאה (−)</span><span><i class="gs-key-good"></i>תחנה שממנה אפשר להשלים סיבוב</span></span>

<!-- /gen -->

- **סעיף א – לנסות כל תחנה :** פתרון ישיר, כמה הוא עולה, ואיזה תנאי פשוט חייב להתקיים כדי שתהיה
  תשובה בכלל?
- **סעיף ב – מעבר אחד :** מצאו תחנה בזמן \( O(n) \) ובזיכרון \( O(1) \), והוכיחו שכשהתנאי של
  סעיף א מתקיים, תמיד יש תחנה כזו.
- **סעיף ג – כמה תחנות טובות :** מתי בדיוק תחנה היא טובה, כמה כאלה יש, ואיך מוצאים את כולן
  ב-\( O(n) \)?

??? interviewer "מה המראיין בודק"
    - **מהסיפור למספרים :** האם המועמד רואה שבכל תחנה חשוב רק ההפרש בין הדלק למחיר, ושהמכל הוא
      סכום מצטבר של ההפרשים.
    - **תנאי הכרחי :** האם הוא שם לב לבדיקה הגלובלית לפני שהוא כותב לולאות.
    - **מ-\( O(n^2) \) ל-\( O(n) \) :** האם הוא יודע להסביר למה מותר לדלג על תחנות, ולא רק לזכור
      את הטריק.
    - **הוכחה :** למה התנאי ההכרחי גם מספיק, כלומר למה תמיד יש תשובה כשהוא מתקיים.
    - **מקרי קצה :** תחנה אחת, שוויון במינימום, ותשובה שאינה יחידה.

---

### סעיף א – לנסות כל תחנה

??? tip "רמז 1"
    מה קורה למכל בתחנה אחת ובקטע שאחריה? האם חשוב כמה דלק יש בתחנה, או רק משהו אחר?

??? tip "רמז 2"
    כמה דלק יש במכל אחרי סיבוב שלם, מכל תחנה שמתחילים בה?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מנסים כל תחנה \( s \) : מתחילים עם מכל ריק, ובכל תחנה מוסיפים את הדלק ומורידים את מחיר
        הקטע, עד שהמכל יורד מתחת ל-0 או שהסיבוב נגמר. זה \( O(n^2) \). תנאי הכרחי : אחרי סיבוב
        שלם במכל יש בדיוק \( S = \sum \mathrm{gas} - \sum \mathrm{cost} \), ולכן אם \( S < 0 \) אין
        תשובה. בדוגמה \( S = 0 \), ורק תחנה 3 מצליחה.

    <!-- cost: זמן \( O(n^2) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **רק ההפרש חשוב.** בתחנה \( i \) המכל עולה ב-`gas[i]` ומיד יורד ב-`cost[i]`, ולכן כל מה שחשוב
    הוא ההפרש \( d_i = \mathrm{gas}[i] - \mathrm{cost}[i] \). בדוגמה
    <span dir="ltr">d = [−2, −2, −2, 3, 3]</span>. מי שמתחיל ב-\( s \) עם מכל ריק, המכל שלו אחרי
    הקטע שיוצא מהתחנה ה-\( k \) בדרך הוא סכום ההפרשים מ-\( s \) עד שם, והוא צריך להיות לפחות 0
    אחרי כל אחד מ-\( n \) הקטעים.

    **תנאי הכרחי.** אחרי סיבוב שלם עברנו בכל תחנה פעם אחת, ולכן במכל יש
    \( S = d_0 + d_1 + \dots + d_{n-1} \), מאיזו תחנה שלא התחלנו. אם \( S < 0 \), הקטע האחרון
    של כל סיבוב נגמר מתחת ל-0, ואין תשובה. בסעיף ב נראה שהתנאי הזה גם מספיק.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **תחנת התחלה :** לכל \( s \) מ-0 עד \( n - 1 \), המכל 0.
    2. **קטע אחרי קטע :** בתחנה \( i = (s + k) \bmod n \) מוסיפים \( d_i \) למכל.
    3. **נתקעים :** אם המכל ירד מתחת ל-0, עוברים לתחנת ההתחלה הבאה.
    4. **הצלחה :** אם עברו \( n \) קטעים, מחזירים את \( s \). אם אף תחנה לא הצליחה,
       <span dir="ltr">−1</span>.

    </div>

    על הדוגמה. בכל שורה תחנת התחלה והמכל אחרי כל קטע, עד שהוא יורד מתחת ל-0 (מודגש) :

    <!-- gen 2 -->

    | התחנה ההתחלתית | קטע 1 | קטע 2 | קטע 3 | קטע 4 | קטע 5 | התוצאה |
    |:-:|:-:|:-:|:-:|:-:|:-:|---|
    | 0 | ‏**<span dir="ltr">−2</span>** | – | – | – | – | נתקעים בקטע <span dir="ltr">0 → 1</span> |
    | 1 | ‏**<span dir="ltr">−2</span>** | – | – | – | – | נתקעים בקטע <span dir="ltr">1 → 2</span> |
    | 2 | ‏**<span dir="ltr">−2</span>** | – | – | – | – | נתקעים בקטע <span dir="ltr">2 → 3</span> |
    | 3 | 3 | 6 | 4 | 2 | 0 | סיבוב שלם |
    | 4 | 3 | 1 | ‏**<span dir="ltr">−1</span>** | – | – | נתקעים בקטע <span dir="ltr">1 → 2</span> |

    <!-- /gen -->

    החיפוש עוצר בתחנה 3 אחרי 8 קטעים. שימו לב לתחנה 4 : היא מתחילה טוב, עם 3 ליטרים, אבל נתקעת
    באותו קטע כמו תחנה 1, כי היא צריכה לעבור דרך תחנות 0, 1 ו-2.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="start_naive" linenums="1" hl_lines="6 10"
        def start_naive(gas: list[int], cost: list[int]) -> int:
            """The first station from which a full lap never runs dry, or -1: every start is driven."""
            n = len(gas)
            for s in range(n):
                tank, k = 0, 0
                while k < n and tank >= 0:             # (1)!
                    i = (s + k) % n
                    tank += gas[i] - cost[i]
                    k += 1
                if tank >= 0:                          # (2)!
                    return s
            return -1
        ```

        1. הלולאה נעצרת כשהמכל ירד מתחת ל-0, או אחרי \( n \) קטעים. ‏\( i \) הוא המקום במעגל, ולכן
           ה-`% n`.
        2. אם הלולאה נגמרה והמכל לא שלילי, עברו כל \( n \) הקטעים : המכל לא ירד מתחת ל-0 אף פעם,
           כי הלולאה הייתה עוצרת.

    === "SystemVerilog"
        ```systemverilog title="function start_naive" linenums="1" hl_lines="8 13"
        // the first station from which a full lap never runs dry, or -1: every start is driven
        function automatic int start_naive(int gas[], int cost[]);
          int n, tank, k, i;
          n = gas.size();
          for (int s = 0; s < n; s++) begin
            tank = 0;
            k = 0;
            while (k < n && tank >= 0) begin                 // (1)!
              i = (s + k) % n;
              tank += gas[i] - cost[i];
              k++;
            end
            if (tank >= 0) return s;
          end
          return -1;
        endfunction
        ```

        1. תנאי הלולאה עוצר אותה כשהמכל שלילי, בלי `break`, כמו ב-Python.

    #### למה זה נכון { .sol-proof }

    המכל אחרי \( k \) קטעים מ-\( s \) הוא בדיוק סכום \( d \) על התחנות שעברנו, והקוד בודק אותו
    אחרי כל קטע. תחנה מוחזרת רק אם כל \( n \) הערכים לא שליליים, וכל תחנה נבדקת לפי הסדר, ולכן
    מוחזרת התחנה הטובה הראשונה, או <span dir="ltr">−1</span> אם אין.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n^2) \) במקרה הגרוע. ב-<span dir="ltr">d = [1, 1, 1, −4, 4]</span>, וכך
      לכל \( n \) עם \( n - 2 \) אחדים, <span dir="ltr">−(n − 1)</span> ו-\( n - 1 \), כל תחנה לפני
      האחרונה נוסעת עד תחנה \( n - 2 \) ונתקעת שם, והחיפוש נוסע \( n(n+1)/2 \) קטעים, 15 עבור
      \( n = 5 \), אף ש-\( S \ge 0 \).
    - **זיכרון :** ‏\( O(1) \).
    - **הבדיקה הזולה :** אפשר לחשב את \( S \) קודם, ב-\( O(n) \), ולהחזיר
      <span dir="ltr">−1</span> מיד כשהוא שלילי. זה לא משנה את המקרה הגרוע.

---

### סעיף ב – מעבר אחד

??? tip "רמז 1"
    נניח שהתחלתם ב-\( s \) ונתקעתם לראשונה בקטע שיוצא מ-\( j \). מה אפשר להגיד על תחנה \( t \)
    שנמצאת בין \( s \) ל-\( j \)? כמה דלק היה לכם כשהגעתם אליה?

??? tip "רמז 2"
    ציירו את הסכום המצטבר של \( d \) מתחנה 0 לאורך הסיבוב, גם כשהוא שלילי. איך נראה המכל
    ממקום התחלה אחר על אותו ציור?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        מעבר אחד : צוברים את המכל מתחנת ההתחלה הנוכחית, וכשהוא יורד מתחת ל-0 בקטע שיוצא מ-\( j \),
        מתחילים מחדש מ-\( j + 1 \) עם מכל ריק. בסוף, אם \( S \ge 0 \) תחנת ההתחלה האחרונה היא
        התשובה, ואחרת <span dir="ltr">−1</span>. זו בדיוק התחנה שלפניה הסכום המצטבר הכי נמוך,
        ולכן כש-\( S \ge 0 \) תמיד יש תשובה. בדוגמה : 3.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **מדלגים על תחנות.** נניח שמ-\( s \) נתקעים לראשונה בקטע שיוצא מ-\( j \). כל תחנה \( t \)
    בין \( s \) ל-\( j \) הגענו אליה מ-\( s \) עם מכל של 0 או יותר. מי שמתחיל ב-\( t \) מתחיל
    עם 0, כלומר עם פחות או אותו דבר, ומשם נוסע באותם קטעים. לכן בכל נקודה עד \( j \) יש לו לכל
    היותר מה שהיה למי שהתחיל ב-\( s \), והוא נתקע בקטע של \( j \) או לפניו. אף תחנה מ-\( s \)
    עד \( j \) לא טובה, ואפשר להמשיך ישר מ-\( j + 1 \) עם מכל ריק. כל תחנה נבדקת פעם אחת : מעבר
    אחד על המערך.

    **הרמות.** נגדיר \( P_0 = 0 \) ו-\( P_k = d_0 + \dots + d_{k-1} \) : המכל כשמגיעים לתחנה
    \( k \) מתחנה 0, אילו מותר היה למכל לרדת מתחת ל-0. ‏\( P_n = S \). מי שמתחיל ב-\( s \) מגיע
    לתחנה \( k > s \) עם \( P_k - P_s \), ואחרי שהוא עובר את תחנה 0 עם \( S + P_k - P_s \). כלומר
    המכל הוא **הגובה של הרמה מעל הרמה של תחנת ההתחלה**. בציור הרמות של הדוגמה לאורך שני
    סיבובים, כשבסיבוב השני כל רמה גבוהה ב-\( S \) :

    <!-- gen 3 -->

    <svg class="perf-chart gs-chart" viewBox="0 0 640 232" role="img" aria-label="הרמות של הדוגמה לאורך שני סיבובים : 0, −2, −4, −6, −3, 0 ושוב. הנמוכה, −6, לפני תחנה 3. הסיבוב מתחנה 3 מוצלל, וכל הרמות בו לפחות −6"><rect class="gs-win" x="207.8" y="16" width="303.7" height="180" rx="4"/><line class="grid" x1="40" x2="626" y1="196.0" y2="196.0"/><text class="tick" x="32" y="200.0" text-anchor="end">−7</text><line class="grid" x1="40" x2="626" y1="174.2" y2="174.2"/><text class="tick" x="32" y="178.2" text-anchor="end">−6</text><line class="grid" x1="40" x2="626" y1="152.5" y2="152.5"/><text class="tick" x="32" y="156.5" text-anchor="end">−5</text><line class="grid" x1="40" x2="626" y1="130.8" y2="130.8"/><text class="tick" x="32" y="134.8" text-anchor="end">−4</text><line class="grid" x1="40" x2="626" y1="109.0" y2="109.0"/><text class="tick" x="32" y="113.0" text-anchor="end">−3</text><line class="grid" x1="40" x2="626" y1="87.2" y2="87.2"/><text class="tick" x="32" y="91.2" text-anchor="end">−2</text><line class="grid" x1="40" x2="626" y1="65.5" y2="65.5"/><text class="tick" x="32" y="69.5" text-anchor="end">−1</text><line class="grid" x1="40" x2="626" y1="43.8" y2="43.8"/><text class="tick" x="32" y="47.8" text-anchor="end">0</text><line class="grid" x1="40" x2="626" y1="22.0" y2="22.0"/><text class="tick" x="32" y="26.0" text-anchor="end">1</text><line class="gs-lap" x1="333.0" x2="333.0" y1="14" y2="196"/><line class="gs-low" x1="40" x2="626" y1="174.2" y2="174.2"/><polyline class="gs-line" points="66.6,43.8 119.9,87.2 173.2,130.8 226.5,174.2 279.7,109.0 333.0,43.8 386.3,87.2 439.5,130.8 492.8,174.2 546.1,109.0 599.4,43.8" fill="none" stroke-width="2"/><circle class="gs-pt" cx="66.6" cy="43.8" r="4"><title>P0 = 0, station 0</title></circle><text class="gs-val" x="66.6" y="34.8" text-anchor="middle">0</text><text class="tick" x="66.6" y="214" text-anchor="middle">0</text><circle class="gs-pt" cx="119.9" cy="87.2" r="4"><title>P1 = −2, station 1</title></circle><text class="gs-val" x="119.9" y="78.2" text-anchor="middle">−2</text><text class="tick" x="119.9" y="214" text-anchor="middle">1</text><circle class="gs-pt" cx="173.2" cy="130.8" r="4"><title>P2 = −4, station 2</title></circle><text class="gs-val" x="173.2" y="121.8" text-anchor="middle">−4</text><text class="tick" x="173.2" y="214" text-anchor="middle">2</text><circle class="gs-pt is-good is-min" cx="226.5" cy="174.2" r="5.5"><title>P3 = −6, station 3</title></circle><text class="gs-val" x="226.5" y="165.2" text-anchor="middle">−6</text><text class="tick" x="226.5" y="214" text-anchor="middle">3</text><circle class="gs-pt" cx="279.7" cy="109.0" r="4"><title>P4 = −3, station 4</title></circle><text class="gs-val" x="279.7" y="100.0" text-anchor="middle">−3</text><text class="tick" x="279.7" y="214" text-anchor="middle">4</text><circle class="gs-pt" cx="333.0" cy="43.8" r="4"><title>P5 = 0, station 0</title></circle><text class="gs-val" x="333.0" y="34.8" text-anchor="middle">0</text><text class="tick" x="333.0" y="214" text-anchor="middle">0</text><circle class="gs-pt" cx="386.3" cy="87.2" r="4"><title>P6 = −2, station 1</title></circle><text class="gs-val" x="386.3" y="78.2" text-anchor="middle">−2</text><text class="tick" x="386.3" y="214" text-anchor="middle">1</text><circle class="gs-pt" cx="439.5" cy="130.8" r="4"><title>P7 = −4, station 2</title></circle><text class="gs-val" x="439.5" y="121.8" text-anchor="middle">−4</text><text class="tick" x="439.5" y="214" text-anchor="middle">2</text><circle class="gs-pt" cx="492.8" cy="174.2" r="4"><title>P8 = −6, station 3</title></circle><text class="gs-val" x="492.8" y="165.2" text-anchor="middle">−6</text><text class="tick" x="492.8" y="214" text-anchor="middle">3</text><circle class="gs-pt" cx="546.1" cy="109.0" r="4"><title>P9 = −3, station 4</title></circle><text class="gs-val" x="546.1" y="100.0" text-anchor="middle">−3</text><text class="tick" x="546.1" y="214" text-anchor="middle">4</text><circle class="gs-pt" cx="599.4" cy="43.8" r="4"><title>P10 = 0, station 0</title></circle><text class="gs-val" x="599.4" y="34.8" text-anchor="middle">0</text><text class="tick" x="599.4" y="214" text-anchor="middle">0</text><line class="axis" x1="40" x2="626" y1="196" y2="196"/></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="gs-key-line"></i>הרמה \( P_k \) : סכום ה-\( d \) עד התחנה, מתחנה 0</span><span><i class="gs-key-low"></i>הרמה הנמוכה בסיבוב הראשון</span><span><i class="gs-key-good"></i>תחנה שממנה אפשר להשלים סיבוב</span><span><i class="gs-key-win"></i>הסיבוב מתחנה 3 : המכל הוא הגובה מעל הרמה שלה</span><span><i class="gs-key-lap"></i>תחילת הסיבוב השני : כל רמה גבוהה ב-\( S \)</span></span>

    <!-- /gen -->

    **למה תמיד יש תשובה.** מתחילים בתחנה \( s \) שהרמה שלה \( P_s \) הכי נמוכה מבין
    \( P_0, \dots, P_{n-1} \). עד סוף הסיבוב הראשון המכל הוא \( P_k - P_s \ge 0 \), כי \( P_s \)
    המינימום. אחרי תחנה 0 הוא \( S + P_k - P_s \ge P_k - P_s \ge 0 \), כי \( S \ge 0 \). בדוגמה
    הרמה הנמוכה היא <span dir="ltr">−6</span>, לפני תחנה 3, והמכל מ-3 הוא הגובה מעל הקו :
    <span dir="ltr">3, 6, 4, 2, 0</span>.

    **שני פתרונות, אותה תשובה.** אפשר לחפש ישר את המינימום של הרמות : לצבור את \( P \), לזכור את
    הרמה הנמוכה עד כה ואת התחנה שאחריה, ולעדכן רק כשרמה חדשה **נמוכה ממש** מהקודמת. המעבר האחד
    עושה את אותו הדבר בלי לקרוא לזה כך : המכל שלו תמיד שווה לרמה הנוכחית פחות הרמה הנמוכה עד כה.
    כשהמכל יורד מתחת ל-0, הרמה ירדה מתחת לנמוכה, ושני הפתרונות זזים יחד לתחנה הבאה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מתחילים :** ההתחלה 0, המכל 0, הסכום הכולל 0.
    2. **תחנה \( i \) :** מוסיפים \( d_i \) למכל ולסכום הכולל.
    3. **נתקעים :** אם המכל שלילי, ההתחלה זזה ל-\( i + 1 \) והמכל חוזר ל-0.
    4. **הסוף :** אם הסכום הכולל \( S \ge 0 \) מחזירים את ההתחלה, ואחרת
       <span dir="ltr">−1</span>.

    </div>

    על הדוגמה. בכל שורה תחנה, המכל מההתחלה הנוכחית אחרי הקטע שלה, וליד זה הרמה והרמה הנמוכה עד
    כה. בשורה 3 המכל הוא \( -3 - (-6) = 3 \), ובשורה 4 \( 0 - (-6) = 6 \) :

    <!-- gen 5 -->

    | התחנה \( i \) | ‏\( d_i \) | המכל מההתחלה הנוכחית | ההתחלה | הרמה \( P_{i+1} \) | הרמה הנמוכה עד כה |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | 0 | ‏<span dir="ltr">−2</span> | ‏**<span dir="ltr">−2</span>**, מתחילים מחדש | 1 | ‏<span dir="ltr">−2</span> | ‏<span dir="ltr">−2</span> |
    | 1 | ‏<span dir="ltr">−2</span> | ‏**<span dir="ltr">−2</span>**, מתחילים מחדש | 2 | ‏<span dir="ltr">−4</span> | ‏<span dir="ltr">−4</span> |
    | 2 | ‏<span dir="ltr">−2</span> | ‏**<span dir="ltr">−2</span>**, מתחילים מחדש | 3 | ‏<span dir="ltr">−6</span> | ‏<span dir="ltr">−6</span> |
    | 3 | 3 | 3 | 3 | ‏<span dir="ltr">−3</span> | ‏<span dir="ltr">−6</span> |
    | 4 | 3 | 6 | 3 | 0 | ‏<span dir="ltr">−6</span> |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="start_one_pass" linenums="1" hl_lines="9 19"
        def start_one_pass(gas: list[int], cost: list[int]) -> int:
            """The first station from which a full lap never runs dry, or -1: one pass, O(1) memory."""
            start, tank, total = 0, 0, 0
            for i in range(len(gas)):
                d = gas[i] - cost[i]
                tank += d
                total += d
                if tank < 0:                           # (1)!
                    start, tank = i + 1, 0
            return start if total >= 0 else -1         # (2)!


        def start_at_min(gas: list[int], cost: list[int]) -> int:
            """The station whose level P_s, the sum of d before it, is the lowest (the first of
            several), or -1: the same station as start_one_pass."""
            level, low, at = 0, 0, 0
            for i in range(len(gas)):
                level += gas[i] - cost[i]              # (3)!
                if level < low:
                    low, at = level, i + 1
            return at if level >= 0 else -1
        ```

        1. נתקעים בקטע שיוצא מ-\( i \) : אף תחנה מ-`start` עד \( i \) לא טובה. ההתחלה הבאה
           \( i + 1 \), ולא \( i \) (ראו המלכודת).
        2. בלי הבדיקה של הסכום הכולל, הקוד מחזיר תחנה גם כשאין תשובה (ראו המלכודת).
        3. ‏`level` הוא \( P_{i+1} \), הרמה לפני התחנה הבאה. ‏`<` ולא `<=` : כך נבחר המינימום
           הראשון, וגם `at` לא מגיע אף פעם ל-\( n \) כשיש תשובה.

    === "SystemVerilog"
        ```systemverilog title="function start_one_pass" linenums="1" hl_lines="9 24"
        // the first station from which a full lap never runs dry, or -1: one pass, O(1) memory
        function automatic int start_one_pass(int gas[], int cost[]);
          int start = 0, tank = 0, total = 0, d;
          foreach (gas[i]) begin
            d = gas[i] - cost[i];
            tank += d;
            total += d;
            if (tank < 0) begin                              // (1)!
              start = i + 1;
              tank = 0;
            end
          end
          return total >= 0 ? start : -1;
        endfunction

        // the station whose level P_s, the sum of d before it, is the lowest (the first of
        // several), or -1: the same station as start_one_pass
        function automatic int start_at_min(int gas[], int cost[]);
          int level = 0, low = 0, at = 0;
          foreach (gas[i]) begin
            level += gas[i] - cost[i];
            if (level < low) begin                           // (2)!
              low = level;
              at = i + 1;
            end
          end
          return level >= 0 ? at : -1;
        endfunction
        ```

        1. ההתחלה זזה מעבר לתחנה שבה נתקענו.
        2. מינימום חדש רק כשהרמה נמוכה ממש, כמו ב-Python.

    #### למה זה נכון { .sol-proof }

    **הדילוג :** תהי \( t \) תחנה בין \( s \) ל-\( j \), כשמ-\( s \) המכל לא שלילי עד הקטע של
    \( j \) ושלילי בו. המכל מ-\( s \) אחרי כל קטע מ-\( t \) והלאה שווה למכל מ-\( t \) ועוד המכל
    שהיה כשהגענו ל-\( t \), שהוא לפחות 0. לכן המכל מ-\( t \) בקטע של \( j \) לכל היותר המכל
    מ-\( s \) שם, שלילי. אף תחנה מ-\( s \) עד \( j \) לא טובה, ובפרט לא תחנה לפני ההתחלה
    האחרונה.

    **ההתחלה האחרונה טובה כש-\( S \ge 0 \) :** המכל במעבר שווה ל-\( P_{i+1} \) פחות הרמה הנמוכה
    עד כה (שכוללת את \( P_0 = 0 \)), באינדוקציה : הוא מתאפס בדיוק כשהרמה יורדת ממש מתחת לנמוכה.
    לכן ההתחלה האחרונה היא התחנה שאחרי המקום הראשון שבו הרמה הנמוכה ביותר מתקבלת, ולפי הציור
    הסיבוב ממנה לא יורד מתחת ל-0. זה גם מראה ששני הפתרונות מחזירים אותה תחנה.

    **זו התחנה הטובה הראשונה :** כל תחנה לפניה מתחילה ברמה גבוהה ממש מהמינימום, והמינימום
    מגיע אחריה באותו סיבוב, ולכן היא נתקעת. סעיף א מחזיר אותה תחנה.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n) \), מעבר אחד.
    - **זיכרון :** ‏\( O(1) \) : שלושה מונים.
    - **מול סעיף א :** אותה תשובה, תמיד. החיסכון הוא הדילוג : תחנה שכבר נבדקה כחלק מסיבוב
      שנכשל לא נבדקת שוב.

    **נסו בעצמכם.** התיבה נפתחת על הדוגמה מתחנה 3. לחצו "עד הסוף" : על הטבעת המכל עובר
    <span dir="ltr">3, 6, 4, 2, 0</span>, ובגרף הוא הגובה מעל הרמה של תחנה 3. לחצו על תחנה 4
    ואחר כך "עד הסוף" : המכל יורד ל-<span dir="ltr">−1</span> בקטע <span dir="ltr">1 → 2</span>,
    והנקודה בגרף יורדת מתחת לרמה שהתחלתם בה. לבסוף בחרו "אין פתרון" : כל תחנה נתקעת, והסכום
    <span dir="ltr">−1</span>. בתיבה אפשר לכתוב כל טבעת עד 10 תחנות ולנסוע מכל תחנה קטע אחרי
    קטע :

    <div class="explorer" data-kind="gasring" data-gas="1.2.3.4.5" data-cost="3.4.5.1.2" data-start="3"></div>

---

### סעיף ג – כמה תחנות טובות

??? tip "רמז 1"
    בציור של סעיף ב, המכל מ-\( s \) הוא הגובה מעל \( P_s \). מה צריך להתקיים לגבי כל הרמות
    שהסיבוב מ-\( s \) עובר בהן?

??? tip "רמז 2"
    הפרידו בין \( S = 0 \) ל-\( S > 0 \). כש-\( S = 0 \) הסיבוב השני הוא העתק של הראשון. ומה
    משתנה כשהוא גבוה יותר?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        תחנה \( s \) טובה בדיוק כש-\( S \ge 0 \), ‏\( P_s \le P_k \) לכל רמה \( k \) אחריה
        בסיבוב, ו-\( P_s \le P_k + S \) לכל \( k \) לפניה. כש-\( S = 0 \) אלה בדיוק התחנות שהרמה
        שלהן היא המינימום, וכמה פעמים שהמינימום מתקבל, כך יש תחנות טובות (למת המעגל). כש-\( S > 0 \)
        יכולות להיות יותר. את כולן מוצאים ב-\( O(n) \) : המינימום של הרמות מכל מקום עד הסוף,
        ומינימום רץ מההתחלה.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **התנאי המדויק.** מ-\( s \) מגיעים לתחנה \( k > s \) עם \( P_k - P_s \), ואחרי תחנה 0
    לתחנה \( k \le s \) עם \( S + P_k - P_s \). המכל לא שלילי לאורך כל הסיבוב בדיוק כש :

    \[
    \begin{aligned}
    P_s &\le P_k \quad \text{for } s < k \le n, \\
    P_s &\le P_k + S \quad \text{for } 0 \le k \le s .
    \end{aligned}
    \]

    השורה השנייה עם \( k = s \) היא \( S \ge 0 \). על הציור של שני הסיבובים, שבו
    \( P_{n+k} = P_k + S \) : תחנה טובה כשהרמה שלה היא המינימום של כל \( n + 1 \) הרמות מ-\( s \)
    עד \( s + n \).

    **כש-\( S = 0 \).** הסיבוב השני הוא העתק של הראשון, וכל חלון של \( n + 1 \) רמות עובר בכולן.
    לכן תחנה טובה בדיוק כש-\( P_s \) הוא המינימום של כל הרמות, ומספר התחנות הטובות הוא מספר
    הפעמים שהמינימום מתקבל בין \( P_0, \dots, P_{n-1} \). זו **למת המעגל**, שמאחורי הספירה של
    מספרי קטלן : לסדרה של \( m + 1 \) פעמים \( +1 \) ו-\( m \) פעמים \( -1 \) יש בדיוק סיבוב אחד
    שכל הסכומים החלקיים שלו חיוביים, ולכן מתוך \( \binom{2m+1}{m} \) הסדרות בדיוק
    \( \frac{1}{2m+1}\binom{2m+1}{m} \) הן כאלה. בטבעת <span dir="ltr">gas = [3, 1, 2, 1, 2, 2, 1]</span>,
    <span dir="ltr">cost = [1, 3, 1, 2, 2, 1, 2]</span> הסכום 0, והמינימום 0 מתקבל ארבע פעמים, לפני
    התחנות 0, 2, 4 ו-5 :

    <!-- gen 6 -->

    <svg class="perf-chart gs-chart" viewBox="0 0 640 232" role="img" aria-label="הרמות של הטבעת עם הסכום 0 : 0, 2, 0, 1, 0, 0, 1 ובסוף שוב 0. הרמה הנמוכה, 0, מתקבלת לפני התחנות 0, 2, 4 ו-5, ואלה ארבע התחנות הטובות"><line class="grid" x1="40" x2="626" y1="196.0" y2="196.0"/><text class="tick" x="32" y="200.0" text-anchor="end">−1</text><line class="grid" x1="40" x2="626" y1="152.5" y2="152.5"/><text class="tick" x="32" y="156.5" text-anchor="end">0</text><line class="grid" x1="40" x2="626" y1="109.0" y2="109.0"/><text class="tick" x="32" y="113.0" text-anchor="end">1</text><line class="grid" x1="40" x2="626" y1="65.5" y2="65.5"/><text class="tick" x="32" y="69.5" text-anchor="end">2</text><line class="grid" x1="40" x2="626" y1="22.0" y2="22.0"/><text class="tick" x="32" y="26.0" text-anchor="end">3</text><line class="gs-low" x1="40" x2="626" y1="152.5" y2="152.5"/><polyline class="gs-line" points="76.6,152.5 149.9,65.5 223.1,152.5 296.4,109.0 369.6,152.5 442.9,152.5 516.1,109.0 589.4,152.5" fill="none" stroke-width="2"/><circle class="gs-pt is-good is-min" cx="76.6" cy="152.5" r="5.5"><title>P0 = 0, station 0</title></circle><text class="gs-val" x="76.6" y="143.5" text-anchor="middle">0</text><text class="tick" x="76.6" y="214" text-anchor="middle">0</text><circle class="gs-pt" cx="149.9" cy="65.5" r="4"><title>P1 = 2, station 1</title></circle><text class="gs-val" x="149.9" y="56.5" text-anchor="middle">2</text><text class="tick" x="149.9" y="214" text-anchor="middle">1</text><circle class="gs-pt is-good is-min" cx="223.1" cy="152.5" r="5.5"><title>P2 = 0, station 2</title></circle><text class="gs-val" x="223.1" y="143.5" text-anchor="middle">0</text><text class="tick" x="223.1" y="214" text-anchor="middle">2</text><circle class="gs-pt" cx="296.4" cy="109.0" r="4"><title>P3 = 1, station 3</title></circle><text class="gs-val" x="296.4" y="100.0" text-anchor="middle">1</text><text class="tick" x="296.4" y="214" text-anchor="middle">3</text><circle class="gs-pt is-good is-min" cx="369.6" cy="152.5" r="5.5"><title>P4 = 0, station 4</title></circle><text class="gs-val" x="369.6" y="143.5" text-anchor="middle">0</text><text class="tick" x="369.6" y="214" text-anchor="middle">4</text><circle class="gs-pt is-good is-min" cx="442.9" cy="152.5" r="5.5"><title>P5 = 0, station 5</title></circle><text class="gs-val" x="442.9" y="143.5" text-anchor="middle">0</text><text class="tick" x="442.9" y="214" text-anchor="middle">5</text><circle class="gs-pt" cx="516.1" cy="109.0" r="4"><title>P6 = 1, station 6</title></circle><text class="gs-val" x="516.1" y="100.0" text-anchor="middle">1</text><text class="tick" x="516.1" y="214" text-anchor="middle">6</text><circle class="gs-pt" cx="589.4" cy="152.5" r="4"><title>P7 = 0, station 0</title></circle><text class="gs-val" x="589.4" y="143.5" text-anchor="middle">0</text><text class="tick" x="589.4" y="214" text-anchor="middle">0</text><line class="axis" x1="40" x2="626" y1="196" y2="196"/></svg>

    <!-- /gen -->

    **כש-\( S > 0 \).** הסיבוב השני גבוה יותר, ולכן לרמות שלפני \( s \) מותר להיות נמוכות
    מ-\( P_s \), עד \( S \). כל תחנה שעל המינימום עדיין טובה, אבל יכולות להיות עוד, והתחנה
    שהמעבר האחד מחזיר היא רק הראשונה. ב-<span dir="ltr">gas = [1, 3, 2, 3, 4]</span>,
    <span dir="ltr">cost = [2, 1, 3, 2, 2]</span> הסכום 3, הרמה הנמוכה <span dir="ltr">−1</span>
    רק לפני תחנה 1, אבל גם 3 ו-4 טובות :

    <!-- gen 7 -->

    <svg class="perf-chart gs-chart" viewBox="0 0 640 232" role="img" aria-label="הרמות של הטבעת עם הסכום 3 לאורך שני סיבובים : 0, −1, 1, 0, 1, ובסיבוב השני כל אחת גבוהה ב-3. הרמה הנמוכה רק לפני תחנה 1, אבל גם 3 ו-4 טובות : מכל אחת מהן הסיבוב לא יורד מתחת לרמה שלה"><line class="grid" x1="40" x2="626" y1="196.0" y2="196.0"/><text class="tick" x="32" y="200.0" text-anchor="end">−2</text><line class="grid" x1="40" x2="626" y1="157.3" y2="157.3"/><text class="tick" x="32" y="161.3" text-anchor="end">0</text><line class="grid" x1="40" x2="626" y1="118.7" y2="118.7"/><text class="tick" x="32" y="122.7" text-anchor="end">2</text><line class="grid" x1="40" x2="626" y1="80.0" y2="80.0"/><text class="tick" x="32" y="84.0" text-anchor="end">4</text><line class="grid" x1="40" x2="626" y1="41.3" y2="41.3"/><text class="tick" x="32" y="45.3" text-anchor="end">6</text><line class="gs-lap" x1="333.0" x2="333.0" y1="14" y2="196"/><line class="gs-low" x1="40" x2="626" y1="176.7" y2="176.7"/><line class="gs-floor" x1="119.9" x2="386.3" y1="176.7" y2="176.7"/><line class="gs-floor" x1="226.5" x2="492.8" y1="157.3" y2="157.3"/><line class="gs-floor" x1="279.7" x2="546.1" y1="138.0" y2="138.0"/><polyline class="gs-line" points="66.6,157.3 119.9,176.7 173.2,138.0 226.5,157.3 279.7,138.0 333.0,99.3 386.3,118.7 439.5,80.0 492.8,99.3 546.1,80.0 599.4,41.3" fill="none" stroke-width="2"/><circle class="gs-pt" cx="66.6" cy="157.3" r="4"><title>P0 = 0, station 0</title></circle><text class="gs-val" x="66.6" y="148.3" text-anchor="middle">0</text><text class="tick" x="66.6" y="214" text-anchor="middle">0</text><circle class="gs-pt is-good is-min" cx="119.9" cy="176.7" r="5.5"><title>P1 = −1, station 1</title></circle><text class="gs-val" x="119.9" y="167.7" text-anchor="middle">−1</text><text class="tick" x="119.9" y="214" text-anchor="middle">1</text><circle class="gs-pt" cx="173.2" cy="138.0" r="4"><title>P2 = 1, station 2</title></circle><text class="gs-val" x="173.2" y="129.0" text-anchor="middle">1</text><text class="tick" x="173.2" y="214" text-anchor="middle">2</text><circle class="gs-pt is-good" cx="226.5" cy="157.3" r="5.5"><title>P3 = 0, station 3</title></circle><text class="gs-val" x="226.5" y="148.3" text-anchor="middle">0</text><text class="tick" x="226.5" y="214" text-anchor="middle">3</text><circle class="gs-pt is-good" cx="279.7" cy="138.0" r="5.5"><title>P4 = 1, station 4</title></circle><text class="gs-val" x="279.7" y="129.0" text-anchor="middle">1</text><text class="tick" x="279.7" y="214" text-anchor="middle">4</text><circle class="gs-pt" cx="333.0" cy="99.3" r="4"><title>P5 = 3, station 0</title></circle><text class="gs-val" x="333.0" y="90.3" text-anchor="middle">3</text><text class="tick" x="333.0" y="214" text-anchor="middle">0</text><circle class="gs-pt" cx="386.3" cy="118.7" r="4"><title>P6 = 2, station 1</title></circle><text class="gs-val" x="386.3" y="109.7" text-anchor="middle">2</text><text class="tick" x="386.3" y="214" text-anchor="middle">1</text><circle class="gs-pt" cx="439.5" cy="80.0" r="4"><title>P7 = 4, station 2</title></circle><text class="gs-val" x="439.5" y="71.0" text-anchor="middle">4</text><text class="tick" x="439.5" y="214" text-anchor="middle">2</text><circle class="gs-pt" cx="492.8" cy="99.3" r="4"><title>P8 = 3, station 3</title></circle><text class="gs-val" x="492.8" y="90.3" text-anchor="middle">3</text><text class="tick" x="492.8" y="214" text-anchor="middle">3</text><circle class="gs-pt" cx="546.1" cy="80.0" r="4"><title>P9 = 4, station 4</title></circle><text class="gs-val" x="546.1" y="71.0" text-anchor="middle">4</text><text class="tick" x="546.1" y="214" text-anchor="middle">4</text><circle class="gs-pt" cx="599.4" cy="41.3" r="4"><title>P10 = 6, station 0</title></circle><text class="gs-val" x="599.4" y="32.3" text-anchor="middle">6</text><text class="tick" x="599.4" y="214" text-anchor="middle">0</text><line class="axis" x1="40" x2="626" y1="196" y2="196"/></svg>

    <!-- /gen -->

    <!-- gen 8 -->

    <span class="viz-legend"><span><i class="gs-key-line"></i>הרמה \( P_k \) : סכום ה-\( d \) עד התחנה, מתחנה 0</span><span><i class="gs-key-low"></i>הרמה הנמוכה בסיבוב הראשון</span><span><i class="gs-key-good"></i>תחנה שממנה אפשר להשלים סיבוב</span><span><i class="gs-key-floor"></i>הרמה של תחנה טובה, לאורך הסיבוב ממנה</span><span><i class="gs-key-lap"></i>תחילת הסיבוב השני : כל רמה גבוהה ב-\( S \)</span></span>

    <!-- /gen -->

    <!-- gen 9 -->

    | התחנה \( s \) | ‏\( P_s \) | הנמוכה אחריה בסיבוב | הנמוכה לפניה, ועוד \( S \) | המכל בסיבוב ממנה | טובה? |
    |:-:|:-:|:-:|:-:|---|:-:|
    | 0 | 0 | ‏<span dir="ltr">−1</span> | אין | ‏<span dir="ltr">−1</span>, נתקעים | לא |
    | 1 | ‏<span dir="ltr">−1</span> | 0 | ‏<span dir="ltr">0 + 3 = 3</span> | ‏<span dir="ltr">2, 1, 2, 4, 3</span> | כן |
    | 2 | 1 | 0 | ‏<span dir="ltr">−1 + 3 = 2</span> | ‏<span dir="ltr">−1</span>, נתקעים | לא |
    | 3 | 0 | 1 | ‏<span dir="ltr">−1 + 3 = 2</span> | ‏<span dir="ltr">1, 3, 2, 4, 3</span> | כן |
    | 4 | 1 | 3 | ‏<span dir="ltr">−1 + 3 = 2</span> | ‏<span dir="ltr">2, 1, 3, 2, 3</span> | כן |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הרמות :** ‏\( P_0 = 0 \) ו-\( P_{k+1} = P_k + d_k \). אם \( S = P_n < 0 \), אין תחנות טובות.
    2. **המינימום מהסוף :** ‏\( \mathrm{after}[k] = \min(P_k, \dots, P_n) \), במעבר אחד מהסוף להתחלה.
    3. **המינימום מההתחלה :** במעבר קדימה שומרים את \( \min(P_0, \dots, P_s) \).
    4. **הבדיקה :** ‏\( s \) טובה כש-\( P_s \le \mathrm{after}[s+1] \) וגם
       \( P_s \le \min(P_0, \dots, P_s) + S \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="good_starts" linenums="1" hl_lines="12 16"
        def good_starts(gas: list[int], cost: list[int]) -> list[int]:
            """Every station from which a full lap never runs dry, in O(n) time."""
            n = len(gas)
            p = [0] * (n + 1)                          # p[k]: the level before station k
            for i in range(n):
                p[i + 1] = p[i] + gas[i] - cost[i]
            total = p[n]
            if total < 0:
                return []
            after = p[:]                               # (1)!
            for k in range(n - 1, -1, -1):
                after[k] = min(p[k], after[k + 1])
            starts, low = [], p[0]
            for s in range(n):
                low = min(low, p[s])                   # (2)!
                if p[s] <= after[s + 1] and p[s] <= low + total:
                    starts.append(s)
            return starts
        ```

        1. ‏`after[k]` הוא המינימום של \( P_k, \dots, P_n \). הרמות שהסיבוב מ-\( s \) עובר בהן לפני
           תחנה 0 הן \( P_{s+1}, \dots, P_n \).
        2. ‏`low` כולל גם את \( P_s \) עצמה, וזה לא משנה את התנאי : \( P_s \le P_s + S \) כש-\( S \ge 0 \).

    === "SystemVerilog"
        ```systemverilog title="function good_starts" linenums="1" hl_lines="11 15"
        // every station from which a full lap never runs dry, in O(n) time
        function automatic void good_starts(int gas[], int cost[], output int starts[$]);
          int n, p[], after[], low;
          n = gas.size();
          p = new[n + 1];                                    // (1)!
          after = new[n + 1];
          starts.delete();
          for (int i = 0; i < n; i++) p[i + 1] = p[i] + gas[i] - cost[i];
          if (p[n] < 0) return;
          after[n] = p[n];
          for (int k = n - 1; k >= 0; k--) after[k] = p[k] < after[k + 1] ? p[k] : after[k + 1];
          low = p[0];
          for (int s = 0; s < n; s++) begin
            if (p[s] < low) low = p[s];
            if (p[s] <= after[s + 1] && p[s] <= low + p[n]) starts.push_back(s);
          end
        endfunction
        ```

        1. ‏`new[n + 1]` מאתחל ל-0, ובפרט \( P_0 = 0 \).

    #### למה זה נכון { .sol-proof }

    **התנאי :** המכל מ-\( s \) כשמגיעים לתחנה \( k \) בסיבוב הראשון הוא \( P_k - P_s \), ואחרי
    תחנה 0 \( S + P_k - P_s \) ; התנאי אומר בדיוק שכל הערכים האלה לפחות 0. הקוד מחשב את שני
    המינימומים לכל \( s \) ובודק אותם.

    **כש-\( S = 0 \) :** השורה השנייה היא \( P_s \le P_k \) לכל \( k \le s \), ויחד עם הראשונה
    \( P_s \) קטנה או שווה לכל הרמות. ההפך ברור, ולכן התחנות הטובות הן בדיוק אלה שעל המינימום.

    **כש-\( S > 0 \) :** תחנה \( s \) על המינימום מקיימת את השורה הראשונה, ואת השנייה
    כי \( P_s \le P_k < P_k + S \). התחנה 3 של הדוגמה האחרונה מראה שההפך לא נכון : \( P_3 = 0 \),
    אבל לפניה \( P_1 = -1 \), ו-<span dir="ltr">−1 + 3 = 2 ≥ 0</span>.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n) \) : שלושה מעברים.
    - **זיכרון :** ‏\( O(n) \) לרמות ולמינימום מהסוף. אפשר גם ב-\( O(1) \) (ראו שאלות ההמשך).
    - **מספר התחנות הטובות :** מ-0 ועד \( n \). כש-\( S = 0 \) הוא מספר המינימומים, וכש-\( S > 0 \)
      לפחות זה.

    **נסו בעצמכם.** התיבה נפתחת על הטבעת עם הסכום 3. התחנות 1, 3 ו-4 ירוקות, אבל רק לפני 1 יש
    את הרמה הנמוכה. לחצו על 3 ו"עד הסוף" : הנקודות בגרף לא יורדות מתחת לרמה של 3. אחר כך בחרו
    "סכום 0, ארבע תחנות" : ארבע הירוקות הן בדיוק ארבע הרמות הנמוכות. לבסוף שנו בשדה הדלק את 1
    של תחנה 0 ל-2 : הסכום עולה ל-4, ותחנה 0 נעשית טובה גם היא. התיבה בודקת כל טבעת שתכתבו מול
    הנסיעה עצמה מכל תחנה :

    <div class="explorer" data-kind="gasring" data-gas="1.3.2.3.4" data-cost="2.1.3.2.2" data-start="3"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להתחיל מחדש מ-j במקום מ-j + 1"
    נתקעים בקטע שיוצא מ-\( j \), ולכן גם \( j \) עצמה לא טובה. קוד שכותב `start = i` מחזיר
    בדוגמה את תחנה 2 : המכל אחרי שלוש התחנות הראשונות מתאפס, ההתחלה נשארת 2, ומשם המכל רק עולה.
    אבל מתחנה 2 המכל אחרי הקטע הראשון הוא <span dir="ltr">−2</span>.

??? trap "מלכודת : להחזיר תחנה בלי לבדוק את הסכום"
    המעבר האחד בלי הבדיקה \( S \ge 0 \) מחזיר תמיד תחנה. ב-<span dir="ltr">gas = [2, 3, 4]</span>,
    <span dir="ltr">cost = [3, 4, 3]</span> הוא מחזיר 2, ומשם המכל <span dir="ltr">1, 0, −1</span> :
    הסכום \( S = -1 \), ואין תשובה. הדילוג מוכיח רק שתחנות **לפני** ההתחלה האחרונה לא טובות. שהיא עצמה
    טובה נובע רק מ-\( S \ge 0 \).

??? trap "מלכודת : להניח שהתשובה יחידה"
    ‏LeetCode מבטיח שיש לכל היותר תשובה אחת, אבל בטבעת עם הסכום 0 של סעיף ג יש ארבע : 0, 2, 4 ו-5.
    מודל ייחוס שמשווה את התשובה של התכן לתחנה אחת, למשל זו שהמעבר האחד מחזיר, נכשל על תכן נכון
    שבוחר אחרת. בודק נכון נוסע מהתחנה שהתכן החזיר ובודק שהמכל לא יורד מתחת ל-0, או משווה לרשימה
    של סעיף ג. וכשהתכן מחזיר <span dir="ltr">−1</span>, בודקים ש-\( S < 0 \).

??? trap "מלכודת : שוויון במינימום ותחנה עם d = 0"
    בתחנה עם \( d_i = 0 \) המכל לא משתנה, ואם הוא היה 0, הוא נשאר 0. קוד שמתחיל מחדש כשהמכל
    "‏\( \le 0 \)" ולא כש-"‏\( < 0 \)" מדלג על תחנות טובות, ובסוף המערך יכול לצאת ממנו : ב-<span dir="ltr">gas = [1, 0]</span>,
    <span dir="ltr">cost = [0, 1]</span> המכל אחרי שתי התחנות 0, והקוד מחזיר 2, שאינה תחנה. כך
    גם חיפוש מינימום עם `<=` : הוא בוחר את המינימום האחרון, וכאן \( P_2 = 0 = P_0 \) והוא מחזיר 2.
    הבדיקה הנכונה היא "נמוך ממש".

??? trap "מלכודת : תחנה אחת"
    עם \( n = 1 \) הסיבוב הוא קטע אחד, מתחנה 0 חזרה אליה, והתשובה 0 בדיוק כש-`gas[0] >= cost[0]`.
    קוד שנוסע בלולאה כמו `while j != s` מהתחנה שאחרי ההתחלה, ומחליט שהסיבוב הצליח כי חזר ל-\( s \),
    לא נכנס ללולאה בכלל : התחנה שאחרי 0 היא 0. הוא מחזיר 0 גם ל-<span dir="ltr">gas = [1]</span>,
    <span dir="ltr">cost = [2]</span>, וכל הפונקציות בעמוד מחזירות שם <span dir="ltr">−1</span>.
    אותו קוד טועה גם כשהמכל יורד מתחת ל-0 בדיוק בקטע האחרון : בטבעת שאין לה פתרון של המלכודת
    הקודמת הוא מחזיר 2. ההחלטה צריכה להיות לפי המכל אחרי כל קטע, גם האחרון, ולא לפי המקום.

??? followup "שאלות המשך"
    - **בחומרה :** איך נראה מודול שמקבל בכל שעון זוג \( (\mathrm{gas}, \mathrm{cost}) \) של תחנה
      אחת, ובסוף מוציא את התחנה או <span dir="ltr">−1</span>?

        ??? fu-answer "תשובה"
            זה `start_at_min` כזרם : רגיסטר של הסכום המצטבר, רגיסטר של המינימום ורגיסטר של
            המקום שלו, ומונה של התחנות. בכל שעון מחסר נותן \( d \), מחבר מוסיף אותו לסכום,
            ומשווה בודק אם הסכום החדש נמוך ממש מהמינימום ; אם כן, המינימום והמקום (המונה ועוד 1)
            נכתבים. בסוף, הסימן של הסכום בוחר בין המקום ל-<span dir="ltr">−1</span>. שני מחברים
            ומשווה, ושום זיכרון של התחנות.

    - **כל התחנות בזיכרון \( O(1) \) :** אפשר למצוא את כל התחנות הטובות בלי מערכים?

        ??? fu-answer "תשובה"
            כן, בשני מעברים. הראשון מוצא את \( S \), את המינימום \( m \) של \( P_0, \dots, P_{n-1} \)
            ואת המקום הראשון שלו \( a \). תחנה לפני \( a \) לא טובה, ומ-\( a \) והלאה המינימום
            שלפני כל תחנה הוא \( m \). המעבר השני הולך מהסוף אחורה עד \( a \), שומר את המינימום
            של הרמות שאחרי, ובודק \( P_s \le \) המינימום הזה וגם \( P_s \le m + S \).

    - **שני כיוונים :** ומה אם מותר לנסוע גם נגד הכיוון, כשהקטע מ-\( i \) ל-\( i - 1 \) עולה
      `cost[i - 1]`?

        ??? fu-answer "תשובה"
            נגד הכיוון זו אותה בעיה על טבעת אחרת : בתחנה \( i \) ההפרש הוא
            \( \mathrm{gas}[i] - \mathrm{cost}[i-1] \), והסדר הפוך. מריצים את המעבר האחד פעם לכל
            כיוון, עדיין \( O(n) \). התנאי ההכרחי זהה בשני הכיוונים : אותו \( S \).

    - **בדיקה של תשובה :** התכן מחזיר תחנה. איך בודקים אותה ב-\( O(n) \) בלי לחשב את כל
      התחנות הטובות?

        ??? fu-answer "תשובה"
            נוסעים ממנה סיבוב אחד ובודקים שהמכל לא יורד מתחת ל-0. אם התכן החזיר
            <span dir="ltr">−1</span>, מספיק לבדוק ש-\( S < 0 \), כי לפי סעיף ב \( S \ge 0 \)
            אומר שיש תשובה.
