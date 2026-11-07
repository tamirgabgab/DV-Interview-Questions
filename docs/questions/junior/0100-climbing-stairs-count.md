---
id: 100
title: כמה דרכים לעלות במדרגות – קפיצות מקבוצה, מדרגות שבורות, בלי סדר ובדיוק t קפיצות
level: junior
difficulty: medium
kind: code
tags: [algorithms, combinatorics, dynamic-programming, sequences, proof, python, systemverilog]
source: "שאלה קלאסית (Climbing Stairs, LeetCode 70); ההכללות לקבוצת קפיצות, למדרגות שבורות ולספירה בלי סדר מופיעות בגרסאות רבות שלה (Coin Change II, LeetCode 518)"
added: 2026-11-07
---

## השאלה

עולים בגרם מדרגות מהקרקע, מדרגה 0, עד מדרגה \( n \). בכל קפיצה עולים מספר מדרגות מתוך
קבוצה קבועה \( S \). כמה דרכים שונות יש להגיע בדיוק למדרגה \( n \)? השאלה בארבעה סעיפים :

1. **הבסיס :** ‏\( S = \{1, 2\} \) ו-\( n = 10 \), ואחר כך כל קבוצה \( S \).
2. **מדרגות שבורות :** על חלק מהמדרגות אסור לנחות.
3. **בלי סדר :** ‏\( 1 + 2 \) ו-\( 2 + 1 \) נחשבות לדרך אחת. מה משתנה בקוד?
4. **בדיוק t קפיצות :** כמה דרכים מגיעות ל-\( n \) בדיוק ב-\( t \) קפיצות?

בכל סעיף כותבים קוד שסופר את מספר הדרכים, בלי לעבור על הדרכים עצמן.

??? interviewer "מה המראיין בודק"
    - **נוסחת נסיגה :** האם המועמד שואל "מאיפה הגעתי למדרגה הזו" ומגיע לסכום, ולא מנסה
      למנות את כל הדרכים.
    - **למה אין ספירה כפולה :** הקפיצה האחרונה מחלקת את הדרכים לקבוצות זרות. האם הוא יודע
      להסביר את זה, ולא רק לכתוב את הסכום.
    - **הסדר של הלולאות :** כשהסדר לא חשוב, אותו קוד עם שתי הלולאות מוחלפות נותן תשובה אחרת.
      האם הוא מבין למה כל סדר של הלולאות סופר משהו אחר.
    - **זיכרון וחומרה :** מספיק לזכור את \( \max S \) הערכים האחרונים. האם הוא רואה שזה רגיסטר
      הזזה, מדרגה אחת בכל שעון.

---

### סעיף א – קפיצות של 1 ושל 2, ואחר כך כל קבוצה

כמה דרכים יש להגיע למדרגה 10 בקפיצות של מדרגה אחת או שתיים? כתבו פונקציה שמקבלת \( n \)
וקבוצה \( S \) של גדלי קפיצה, ומחזירה את מספר הדרכים. כאן הסדר חשוב : \( 1 + 2 \) ו-\( 2 + 1 \)
הן שתי דרכים.

??? tip "רמז 1"
    מה הייתה הקפיצה האחרונה של דרך שמגיעה למדרגה 10? מאילו מדרגות אפשר להגיע אליה?

??? tip "רמז 2"
    נסמנו ב-\( w(i) \) את מספר הדרכים להגיע למדרגה \( i \). כמה דרכים יש להגיע ל-0?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **‏89.** כל דרך למדרגה \( i \) מסתיימת בקפיצה של \( s \in S \), ולפניה היא דרך למדרגה
        \( i - s \). לכן \( w(i) = \sum_{s \in S} w(i - s) \), עם \( w(0) = 1 \) ו-\( w \) של
        מדרגה שלילית 0. עם \( S = \{1, 2\} \) זו סדרת Fibonacci : 1, 1, 2, 3, 5, 8 ועד
        \( w(10) = 89 \).

    <!-- cost: זמן \( O(n \cdot |S|) \) | זיכרון \( O(\max S) \) -->

    #### הרעיון { .sol-idea }

    במקום לשאול איך מתחילים, שואלים איך **מסיימים**. דרך שמגיעה למדרגה 10 נחתה לפני הקפיצה
    האחרונה על מדרגה 9 או על מדרגה 8. לכן מספר הדרכים ל-10 הוא סכום הדרכים ל-9 ול-8 :

    <!-- gen 0 -->

    <svg class="figure sw-fig" viewBox="0 0 372 174" style="max-width:23.25rem" role="img" aria-label="גרם מדרגות 0 עד 10 עם קפיצות של 1 ושל 2 : על כל מדרגה מספר הדרכים להגיע אליה, 1, 1, 2, 3, 5 ועד 89 במדרגה 10. חיצים מהמדרגות 9 ו-8 אל מדרגה 10"><g class="sw-stair"><title>stair 0: 1 way</title><rect x="6" y="130" width="28" height="26" rx="2"/></g><text class="tick" x="20" y="169" text-anchor="middle">0</text><text class="sw-val" x="20" y="145" text-anchor="middle">1</text><g class="sw-stair"><title>stair 1: 1 way</title><rect x="36" y="121" width="28" height="35" rx="2"/></g><text class="tick" x="50" y="169" text-anchor="middle">1</text><text class="sw-val" x="50" y="136" text-anchor="middle">1</text><g class="sw-stair"><title>stair 2: 2 ways</title><rect x="66" y="112" width="28" height="44" rx="2"/></g><text class="tick" x="80" y="169" text-anchor="middle">2</text><text class="sw-val" x="80" y="127" text-anchor="middle">2</text><g class="sw-stair"><title>stair 3: 3 ways</title><rect x="96" y="103" width="28" height="53" rx="2"/></g><text class="tick" x="110" y="169" text-anchor="middle">3</text><text class="sw-val" x="110" y="118" text-anchor="middle">3</text><g class="sw-stair"><title>stair 4: 5 ways</title><rect x="126" y="94" width="28" height="62" rx="2"/></g><text class="tick" x="140" y="169" text-anchor="middle">4</text><text class="sw-val" x="140" y="109" text-anchor="middle">5</text><g class="sw-stair"><title>stair 5: 8 ways</title><rect x="156" y="85" width="28" height="71" rx="2"/></g><text class="tick" x="170" y="169" text-anchor="middle">5</text><text class="sw-val" x="170" y="100" text-anchor="middle">8</text><g class="sw-stair"><title>stair 6: 13 ways</title><rect x="186" y="76" width="28" height="80" rx="2"/></g><text class="tick" x="200" y="169" text-anchor="middle">6</text><text class="sw-val" x="200" y="91" text-anchor="middle">13</text><g class="sw-stair"><title>stair 7: 21 ways</title><rect x="216" y="67" width="28" height="89" rx="2"/></g><text class="tick" x="230" y="169" text-anchor="middle">7</text><text class="sw-val" x="230" y="82" text-anchor="middle">21</text><g class="sw-stair sw-from"><title>stair 8: 34 ways</title><rect x="246" y="58" width="28" height="98" rx="2"/></g><text class="tick" x="260" y="169" text-anchor="middle">8</text><text class="sw-val" x="260" y="73" text-anchor="middle">34</text><g class="sw-stair sw-from"><title>stair 9: 55 ways</title><rect x="276" y="49" width="28" height="107" rx="2"/></g><text class="tick" x="290" y="169" text-anchor="middle">9</text><text class="sw-val" x="290" y="64" text-anchor="middle">55</text><g class="sw-stair sw-focus"><title>stair 10: 89 ways</title><rect x="306" y="40" width="28" height="116" rx="2"/></g><text class="tick" x="320" y="169" text-anchor="middle">10</text><text class="sw-val" x="320" y="55" text-anchor="middle">89</text><path class="sw-arc" d="M290,45 Q305,14 320,36" marker-end="url(#sw-head)"/><path class="sw-arc" d="M260,54 Q290,6 320,36" marker-end="url(#sw-head)"/><defs><marker id="sw-head" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path class="sw-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="sw-key"></i>מדרגה, ומעליה מספר הדרכים להגיע אליה</span><span><i class="sw-key-focus"></i>המדרגה האחרונה</span><span><i class="sw-key-from"></i>המדרגות שקופצים מהן אליה</span></span>

    <!-- /gen -->

    אותו רעיון עובד לכל קבוצת קפיצות. כך נראות הטבלאות של כמה קבוצות :

    <!-- gen 2 -->

    | הקפיצות S | הנוסחה | הדרכים למדרגות 0 עד 10 | למדרגה 10 |
    |---|---|---|:-:|
    | ‏<span dir="ltr">{1, 2}</span> | ‏<span dir="ltr">w(i) = w(i−1) + w(i−2)</span> | ‏<span dir="ltr">1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89</span> | 89 |
    | ‏<span dir="ltr">{1, 2, 3}</span> | ‏<span dir="ltr">w(i) = w(i−1) + w(i−2) + w(i−3)</span> | ‏<span dir="ltr">1, 1, 2, 4, 7, 13, 24, 44, 81, 149, 274</span> | 274 |
    | ‏<span dir="ltr">{1, 3, 5}</span> | ‏<span dir="ltr">w(i) = w(i−1) + w(i−3) + w(i−5)</span> | ‏<span dir="ltr">1, 1, 1, 2, 3, 5, 8, 12, 19, 30, 47</span> | 47 |
    | ‏<span dir="ltr">{2, 3}</span> | ‏<span dir="ltr">w(i) = w(i−2) + w(i−3)</span> | ‏<span dir="ltr">1, 0, 1, 1, 1, 2, 2, 3, 4, 5, 7</span> | 7 |
    | ‏<span dir="ltr">{1, 2, 3, 4, 5, 6}</span> | ‏<span dir="ltr">w(i) = w(i−1) + w(i−2) + w(i−3) + w(i−4) + w(i−5) + w(i−6)</span> | ‏<span dir="ltr">1, 1, 2, 4, 8, 16, 32, 63, 125, 248, 492</span> | 492 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הקרקע :** ‏\( w(0) = 1 \). יש דרך אחת להיות על הקרקע : לא לקפוץ בכלל.
    2. **מדרגה אחרי מדרגה :** לכל \( i \) מ-1 עד \( n \), ‏\( w(i) \) הוא סכום של \( w(i - s) \)
       על כל \( s \in S \) שלא גדול מ-\( i \).
    3. **התשובה :** ‏\( w(n) \). עם \( S = \{1, 2\} \) :
       ‏<span dir="ltr">w(10) = w(9) + w(8) = 55 + 34 = 89</span>.
    4. **זיכרון :** ‏\( w(i) \) תלוי רק ב-\( \max S \) הערכים שלפניו, ולכן מספיק חלון שלהם.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="count_ways" linenums="1" hl_lines="4 6"
        def count_ways(n, steps):
            """The climbs from stair 0 to stair n when every jump is a number of stairs from
            steps. The order of the jumps matters: 1 + 2 and 2 + 1 are two climbs."""
            ways = [1] + [0] * n                                 # (1)!
            for i in range(1, n + 1):
                ways[i] = sum(ways[i - s] for s in steps if s <= i)   # (2)!
            return ways[n]


        def list_ways(n, steps):
            """Every climb itself, for a small n: a first jump, then every climb of the rest."""
            if n == 0:
                return [[]]
            return [[s] + rest for s in sorted(steps) if s <= n for rest in list_ways(n - s, steps)]
        ```

        1. ‏`ways[0] = 1` : הדרך הריקה. בלי זה כל הטבלה יוצאת 0.
        2. כל \( s \) הוא הקפיצה האחרונה האפשרית. דרכים עם קפיצה אחרונה שונה הן דרכים שונות,
           ולכן מחברים.

    === "SystemVerilog"
        ```systemverilog title="function automatic longint unsigned count_ways" linenums="1" hl_lines="9"
        // The climbs from stair 0 to stair n, every jump a number of stairs from steps (each at
        // least 1), in 64 bits
        function automatic longint unsigned count_ways(int n, int steps[$]);
          longint unsigned ways[];
          ways = new[n + 1];
          ways[0] = 1;
          for (int i = 1; i <= n; i++) begin
            ways[i] = 0;
            foreach (steps[k]) if (steps[k] <= i) ways[i] += ways[i - steps[k]];
          end
          return ways[n];
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **הנסיגה.** כל דרך למדרגה \( i \ge 1 \) מסתיימת בקפיצה אחת, בגודל \( s \in S \). אם
    מורידים אותה, נשארת דרך למדרגה \( i - s \), ולהפך : כל דרך למדרגה \( i - s \) ואחריה קפיצה
    של \( s \) היא דרך ל-\( i \). זו התאמה חד-חד-ערכית ועל בין הדרכים ל-\( i \) שמסתיימות
    ב-\( s \) לבין הדרכים ל-\( i - s \). הקבוצות של \( s \) שונים זרות, כי לכל דרך קפיצה אחרונה
    אחת, ולכן \( w(i) = \sum_{s \in S,\ s \le i} w(i - s) \). באינדוקציה על \( i \) כל ערך בטבלה
    נכון.

    **סדרת Fibonacci.** עם \( S = \{1, 2\} \) הנסיגה היא \( w(i) = w(i-1) + w(i-2) \), עם
    \( w(0) = w(1) = 1 \). זו סדרת Fibonacci מוזזת באחד : \( w(n) = F_{n+1} \), ו-\( F_{11} = 89 \).

    **נסו בעצמכם.** בחרו גדלי קפיצה ומספר מדרגות. על כל מדרגה מופיע מספר הדרכים להגיע אליה.
    לחצו על מדרגה כדי לראות מאילו מדרגות קופצים אליה, ואיך הסכום שלהן נותן את המספר שלה :

    <div class="explorer" data-kind="stairs" data-n="10" data-steps="1.2"></div>

    #### סיבוכיות { .sol-cost }

    לכל מדרגה \( |S| \) חיבורים : זמן \( O(n \cdot |S|) \). הטבלה כולה היא \( O(n) \) זיכרון, אבל
    מספיק חלון של \( \max S \) ערכים. ‏`list_ways` עוברת על כל הדרכים, ומספר הדרכים גדל
    מעריכית, \( F_{n+1} \approx 1.618^{n} \) עם \( S = \{1, 2\} \). לכן היא רק לבדיקה של \( n \)
    קטן.

---

### סעיף ב – מדרגות שבורות

חלק מהמדרגות שבורות, ואסור לנחות עליהן. כמה דרכים יש להגיע למדרגה 10 בקפיצות של 1 ושל 2,
כשמדרגה 5 שבורה? ומה קורה כששתי מדרגות צמודות שבורות? כתבו פונקציה לכל קבוצת מדרגות
שבורות, ומודול חומרה שמקבל מדרגה אחת בכל מחזור שעון.

??? tip "רמז 1"
    כמה דרכים יש לנחות על מדרגה שבורה?

??? tip "רמז 2"
    עם \( S = \{1, 2\} \), איך אפשר לעבור את מדרגה 5 בלי לנחות עליה?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **‏25.** אותה טבלה, ובמדרגה שבורה כותבים 0 : אף דרך לא נוחתת עליה, ולכן היא לא מוסיפה
        כלום למדרגות שמעליה. עם \( S = \{1, 2\} \) מדרגה 5 נעברת רק בקפיצה מ-4 ל-6, ולכן
        \( w(10) = w(4) \cdot w'(4) = 5 \cdot 5 = 25 \), כש-\( w'(4) \) הוא הדרכים מ-6 ל-10. שתי
        מדרגות שבורות צמודות חוסמות הכול : 0 דרכים.

    <!-- cost: זמן \( O(n \cdot |S|) \) | זיכרון \( O(\max S) \) -->

    #### הרעיון { .sol-idea }

    הטיעון של סעיף א לא תלוי בכך שכל המדרגות שלמות : הדרכים ל-\( i \) עדיין מתחלקות לפי
    הקפיצה האחרונה. מדרגה שבורה היא מדרגה שמספר הדרכים אליה 0 :

    <!-- gen 3 -->

    <svg class="figure sw-fig" viewBox="0 0 372 174" style="max-width:23.25rem" role="img" aria-label="אותו גרם מדרגות כשמדרגה 5 שבורה : עליה 0, מדרגה 6 מקבלת רק ממדרגה 4, ובמדרגה 10 יש 25 דרכים"><g class="sw-stair"><title>stair 0: 1 way</title><rect x="6" y="130" width="28" height="26" rx="2"/></g><text class="tick" x="20" y="169" text-anchor="middle">0</text><text class="sw-val" x="20" y="145" text-anchor="middle">1</text><g class="sw-stair"><title>stair 1: 1 way</title><rect x="36" y="121" width="28" height="35" rx="2"/></g><text class="tick" x="50" y="169" text-anchor="middle">1</text><text class="sw-val" x="50" y="136" text-anchor="middle">1</text><g class="sw-stair"><title>stair 2: 2 ways</title><rect x="66" y="112" width="28" height="44" rx="2"/></g><text class="tick" x="80" y="169" text-anchor="middle">2</text><text class="sw-val" x="80" y="127" text-anchor="middle">2</text><g class="sw-stair"><title>stair 3: 3 ways</title><rect x="96" y="103" width="28" height="53" rx="2"/></g><text class="tick" x="110" y="169" text-anchor="middle">3</text><text class="sw-val" x="110" y="118" text-anchor="middle">3</text><g class="sw-stair sw-from"><title>stair 4: 5 ways</title><rect x="126" y="94" width="28" height="62" rx="2"/></g><text class="tick" x="140" y="169" text-anchor="middle">4</text><text class="sw-val" x="140" y="109" text-anchor="middle">5</text><g class="sw-stair sw-broken"><title>stair 5: broken</title><rect x="156" y="85" width="28" height="71" rx="2"/></g><text class="tick" x="170" y="169" text-anchor="middle">5</text><path class="sw-x" d="M163,90 l14,14 M177,90 l-14,14"/><g class="sw-stair sw-focus"><title>stair 6: 5 ways</title><rect x="186" y="76" width="28" height="80" rx="2"/></g><text class="tick" x="200" y="169" text-anchor="middle">6</text><text class="sw-val" x="200" y="91" text-anchor="middle">5</text><g class="sw-stair"><title>stair 7: 5 ways</title><rect x="216" y="67" width="28" height="89" rx="2"/></g><text class="tick" x="230" y="169" text-anchor="middle">7</text><text class="sw-val" x="230" y="82" text-anchor="middle">5</text><g class="sw-stair"><title>stair 8: 10 ways</title><rect x="246" y="58" width="28" height="98" rx="2"/></g><text class="tick" x="260" y="169" text-anchor="middle">8</text><text class="sw-val" x="260" y="73" text-anchor="middle">10</text><g class="sw-stair"><title>stair 9: 15 ways</title><rect x="276" y="49" width="28" height="107" rx="2"/></g><text class="tick" x="290" y="169" text-anchor="middle">9</text><text class="sw-val" x="290" y="64" text-anchor="middle">15</text><g class="sw-stair"><title>stair 10: 25 ways</title><rect x="306" y="40" width="28" height="116" rx="2"/></g><text class="tick" x="320" y="169" text-anchor="middle">10</text><text class="sw-val" x="320" y="55" text-anchor="middle">25</text><path class="sw-arc" d="M140,90 Q170,42 200,72" marker-end="url(#sw-head)"/><defs><marker id="sw-head" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path class="sw-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="sw-key"></i>מדרגה, ומעליה מספר הדרכים להגיע אליה</span><span><i class="sw-key-focus"></i>המדרגה האחרונה</span><span><i class="sw-key-from"></i>המדרגות שקופצים מהן אליה</span><span><i class="sw-key-broken"></i>מדרגה שבורה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הקרקע :** ‏\( w(0) = 1 \), כמו קודם.
    2. **מדרגה שבורה :** ‏\( w(i) = 0 \).
    3. **מדרגה שלמה :** הסכום של סעיף א. מדרגה שבורה מתחת לה מוסיפה 0.
    4. **התשובה :** ‏\( w(n) \). אם \( n \) עצמה שבורה, אין דרך.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="count_ways_broken" linenums="1" hl_lines="6 7"
        def count_ways_broken(n, steps, broken=()):
            """The same count when no climb may land on a broken stair."""
            bad = set(broken)
            ways = [1] + [0] * n
            for i in range(1, n + 1):
                if i not in bad:                                 # (1)!
                    ways[i] = sum(ways[i - s] for s in steps if s <= i)
            return ways[n]
        ```

        1. מדרגה שבורה נשארת 0, ולכן כל סכום שעובר דרכה מקבל ממנה 0.

    === "SystemVerilog"
        ```systemverilog title="module stairs_ways" linenums="1" hl_lines="16 25 26"
        // One stair a clock: ways is the number of climbs to it, from the K stairs below it.
        // steps[s] = 1: a jump of s stairs is allowed (s from 1 to K).
        module stairs_ways #(parameter int K = 6, W = 64) (
          input  logic         clk, rst_n,
          input  logic         start,          // stair 0, the ground: one climb, the empty one
          input  logic         valid,          // the next stair, this clock
          input  logic         broken,         // that stair is broken
          input  logic [K:1]   steps,
          output logic [W-1:0] ways);          // the climbs to the last stair

          logic [W-1:0] below [1:K];           // below[s]: the climbs to the stair s below the next one
          logic [W-1:0] sum;

          always_comb begin
            sum = '0;
            for (int s = 1; s <= K; s++) if (steps[s]) sum += below[s];   // (1)!
          end

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin
              below <= '{default: '0}; ways <= '0;
            end else if (start) begin
              below <= '{default: '0}; below[1] <= W'(1); ways <= W'(1);
            end else if (valid) begin
              for (int s = K; s > 1; s--) below[s] <= below[s - 1];        // (2)!
              below[1] <= broken ? '0 : sum;
              ways <= broken ? '0 : sum;
            end
        endmodule
        ```

        1. הסכום של סעיף א : ‏`below[s]` הוא \( w(i - s) \) של המדרגה הבאה \( i \), ו-`steps`
           בוחר אילו מהם נכנסים.
        2. רגיסטר הזזה של \( K \) ערכים : אחרי המדרגה \( i \), ‏`below[1]` הוא \( w(i) \),
           ‏`below[2]` הוא \( w(i - 1) \) וכן הלאה. מדרגה שבורה נכנסת אליו כ-0.

    #### למה זה נכון { .sol-proof }

    **הטבלה.** דרך לא נוחתת על מדרגה שבורה, ולכן \( w(i) = 0 \) למדרגה שבורה. למדרגה שלמה
    ההוכחה של סעיף א עובדת כמו שהיא : הקפיצה האחרונה באה ממדרגה \( i - s \), והדרכים אליה
    כבר לא נוחתות על מדרגה שבורה. אם \( i - s \) שבורה, היא מוסיפה 0, וזה נכון.

    **מכפלה.** עם \( S = \{1, 2\} \) ומדרגה \( b \) שבורה, כל דרך עוברת את \( b \) בקפיצה
    מ-\( b - 1 \) ל-\( b + 1 \). לכן דרך היא זוג : דרך מ-0 ל-\( b - 1 \), ודרך מ-\( b + 1 \)
    ל-\( n \). מ-0 ל-4 יש 5 דרכים, ומ-6 ל-10, שוב 4 מדרגות, 5 דרכים : \( 5 \cdot 5 = 25 \).
    אם גם \( b + 1 \) שבורה, אין קפיצה שעוברת שתיהן, ו-\( w(n) = 0 \).

    **החומרה.** אחרי `start` הרגיסטר מחזיק \( w(0) = 1 \) ב-`below[1]`, ואפסים מתחת לקרקע.
    בכל שעון עם `valid` המודול מחשב את \( w(i) \) מהחלון ומכניס אותו לראש החלון. זה בדיוק
    הקוד של Python, עם חלון של \( K \) ערכים במקום טבלה.

    **נסו בעצמכם.** לחצו על מדרגה ואז על "שבירה" כדי לשבור אותה או לתקן אותה. מדרגה שבורה
    מוסיפה 0 לכל מדרגה שקופצים אליה ממנה :

    <div class="explorer" data-kind="stairs" data-n="10" data-steps="1.2" data-broken="5" data-pick="6"></div>

    #### סיבוכיות { .sol-cost }

    כמו בסעיף א : זמן \( O(n \cdot |S|) \) וזיכרון \( O(\max S) \). בחומרה \( n \) שעונים,
    ‏\( K \) רגיסטרים ו-\( K - 1 \) מחברים.

---

### סעיף ג – בלי סדר

עכשיו \( 1 + 2 \) ו-\( 2 + 1 \) הן אותה דרך : חשוב רק כמה קפיצות יש מכל גודל. כמה דרכים
יש להגיע למדרגה 10 עם \( S = \{1, 2\} \)? ועם \( S = \{1, 2, 3\} \)? הראו שמספיק להחליף את
הסדר של שתי הלולאות בקוד.

??? tip "רמז 1"
    עם \( S = \{1, 2\} \), דרך בלי סדר נקבעת לפי מספר הקפיצות של 2. כמה אפשרויות יש לו?

??? tip "רמז 2"
    אם מחליטים שכל הקפיצות של 1 באות לפני כל הקפיצות של 2, לכל דרך בלי סדר יש סדר אחד
    בלבד. איך כותבים טבלה שסופרת רק סדרים כאלה?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        **‏6, ועם {1, 2, 3} ‏14.** עם \( S = \{1, 2\} \) מספר הקפיצות של 2 הוא 0 עד 5, וכל
        אחד קובע דרך. בקוד מחליפים את הלולאות : הלולאה החיצונית עוברת על גדלי הקפיצה, והפנימית
        על המדרגות. כך כל דרך נספרת פעם אחת, בסדר שבו הקפיצות ממוינות מהקטנה לגדולה. הסדר
        הרגיל של הלולאות סופר את כל הסדרים, 89 ו-274.

    <!-- cost: זמן \( O(n \cdot |S|) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    עם \( S = \{1, 2\} \) קל לראות את ההבדל. כל דרך בלי סדר נקבעת לפי מספר הקפיצות של 2,
    ‏\( k \), ומספר הסדרים שלה הוא מספר הדרכים לבחור איפה הן, \( \binom{10-k}{k} \) :

    <!-- gen 5 -->

    | קפיצות של 2 | קפיצות של 1 | קפיצות בסך הכול, t | סדרים שונים | בלי סדר |
    |:-:|:-:|:-:|:-:|:-:|
    | 0 | 10 | 10 | ‏<span dir="ltr">C(10, 0) = 1</span> | 1 |
    | 1 | 8 | 9 | ‏<span dir="ltr">C(9, 1) = 9</span> | 1 |
    | 2 | 6 | 8 | ‏<span dir="ltr">C(8, 2) = 28</span> | 1 |
    | 3 | 4 | 7 | ‏<span dir="ltr">C(7, 3) = 35</span> | 1 |
    | 4 | 2 | 6 | ‏<span dir="ltr">C(6, 4) = 15</span> | 1 |
    | 5 | 0 | 5 | ‏<span dir="ltr">C(5, 5) = 1</span> | 1 |
    | **סך הכול** | | | **89** | **6** |

    <!-- /gen -->

    כדי לספור כל דרך פעם אחת, סופרים רק את הסדר שבו הקפיצות ממוינות מהקטנה לגדולה. זה מה
    שהטבלה עושה כשהלולאה החיצונית עוברת על גדלי הקפיצה. עם \( S = \{1, 2, 3\} \) ו-6 מדרגות :

    <!-- gen 6 -->

    | אחרי הלולאה של | הטבלה, מדרגות 0 עד 6 | מה נספר |
    |---|---|---|
    | 1 | ‏<span dir="ltr">1, 1, 1, 1, 1, 1, 1</span> | רק קפיצות של 1 : דרך אחת לכל מדרגה |
    | 2 | ‏<span dir="ltr">1, 1, 2, 2, 3, 3, 4</span> | קפיצות של 1 ושל 2, כל ה-2 אחרי כל ה-1 |
    | 3 | ‏<span dir="ltr">1, 1, 2, 3, 4, 5, 7</span> | גם קפיצות של 3, אחרי כל השאר |
    | בסדר הרגיל | ‏<span dir="ltr">1, 1, 2, 4, 7, 13, 24</span> | כל הסדרים |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הקרקע :** ‏\( w(0) = 1 \), וכל השאר 0.
    2. **גודל אחרי גודל :** לכל \( s \in S \), מהקטן לגדול, ולכל מדרגה \( i \) מ-\( s \)
       עד \( n \) : ‏\( w(i) \mathrel{+}= w(i - s) \).
    3. **מה הטבלה מחזיקה :** אחרי הגודל \( s \), ‏\( w(i) \) הוא מספר הדרכים למדרגה \( i \)
       בקפיצות שכולן לכל היותר \( s \), כשהסדר לא חשוב.
    4. **התשובה :** ‏\( w(n) \) אחרי הגודל האחרון.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="count_multisets" linenums="1" hl_lines="5 6 7"
        def count_multisets(n, steps):
            """The order does not matter: only how many jumps of each size. 1 + 2 and 2 + 1 are
            one way."""
            ways = [1] + [0] * n
            for s in sorted(set(steps)):                         # (1)!
                for i in range(s, n + 1):
                    ways[i] += ways[i - s]                       # (2)!
            return ways[n]
        ```

        1. הלולאה החיצונית על גדלי הקפיצה. בסעיף א היא הייתה על המדרגות.
        2. ‏`ways[i - s]` כבר כולל את הקפיצות של \( s \) שנספרו בסיבוב הזה, ולכן אפשר לקפוץ
           \( s \) כמה פעמים שרוצים. הוא לא כולל קפיצות גדולות מ-\( s \), כי עוד לא הגענו
           אליהן : הן תמיד יבואו אחרונות.

    === "SystemVerilog"
        ```systemverilog title="function automatic longint unsigned count_multisets" linenums="1" hl_lines="7 8"
        // The order does not matter: the loops of count_ways swapped (steps without repeats)
        function automatic longint unsigned count_multisets(int n, int steps[$]);
          longint unsigned ways[];
          ways = new[n + 1];
          foreach (ways[i]) ways[i] = 0;
          ways[0] = 1;
          foreach (steps[k])
            for (int i = steps[k]; i <= n; i++) ways[i] += ways[i - steps[k]];
          return ways[n];
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **נציג אחד לכל דרך.** דרך בלי סדר היא אוסף של קפיצות, ולכל אוסף יש סדר אחד בדיוק שבו
    הקפיצות לא יורדות : כל ה-1 קודם, אחר כך כל ה-2, וכן הלאה. לכן מספר הדרכים בלי סדר שווה
    למספר הסדרים הממוינים.

    **הטבלה סופרת סדרים ממוינים.** נסמן ב-\( w_s(i) \) את מספר הסדרים הממוינים למדרגה \( i \)
    שכל הקפיצות בהם לכל היותר \( s \). סדר כזה נגמר בקפיצה של \( s \), או שאין בו קפיצה של
    \( s \) בכלל. במקרה הראשון, בלי הקפיצה האחרונה הוא סדר ממוין ל-\( i - s \) עם קפיצות עד
    \( s \). במקרה השני הוא סדר עם קפיצות קטנות מ-\( s \). לכן
    \( w_s(i) = w_{s'}(i) + w_s(i - s) \), כש-\( s' \) הגודל הקודם. זה בדיוק מה שהלולאה הפנימית
    עושה : לפני השורה `ways[i]` הוא \( w_{s'}(i) \), ו-`ways[i - s]` כבר עודכן ל-\( w_s(i - s) \).

    **‏{1, 2} ו-{1, 2, 3}.** עם \( S = \{1, 2\} \), \( k \) קפיצות של 2 ו-\( 10 - 2k \) של 1
    לכל \( k \) מ-0 עד 5 : ‏6 דרכים. סכום הסדרים שלהן, \( \sum_k \binom{10-k}{k} = 89 \), הוא
    התשובה של סעיף א. עם \( S = \{1, 2, 3\} \) הטבלה נותנת 14 דרכים, לעומת 274 סדרים.

    #### סיבוכיות { .sol-cost }

    ‏\( |S| \) מעברים על הטבלה : זמן \( O(n \cdot |S|) \). כאן צריך את כל הטבלה, \( O(n) \),
    כי כל מעבר קורא את הערכים של המעבר הקודם בכל המדרגות.

---

### סעיף ד – בדיוק t קפיצות

כמה דרכים מגיעות למדרגה 10 בקפיצות של 1 ושל 2 בדיוק ב-7 קפיצות? כתבו פונקציה לכל \( S \)
ו-\( t \), והוכיחו נוסחה סגורה ל-\( S = \{1, 2\} \).

??? tip "רמז 1"
    עם \( S = \{1, 2\} \) ו-7 קפיצות שמגיעות ל-10, כמה מהן הן קפיצות של 2?

??? tip "רמז 2"
    לכל \( S \) : מה הייתה הקפיצה האחרונה, ובכמה קפיצות הגיעו למדרגה שלפניה?

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        **‏35.** ב-7 קפיצות שמגיעות ל-10 יש בדיוק 3 קפיצות של 2 ו-4 של 1, ובוחרים איפה ה-2 :
        ‏\( \binom{7}{3} = 35 \). באופן כללי \( \binom{t}{n - t} \) ל-\( S = \{1, 2\} \). לכל
        \( S \) שומרים שורה לכל מספר קפיצות : \( w_t(i) = \sum_{s \in S} w_{t-1}(i - s) \).

    <!-- cost: זמן \( O(t \cdot n \cdot |S|) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    עכשיו המצב הוא לא רק המדרגה, אלא גם מספר הקפיצות עד אליה. הקפיצה האחרונה עדיין מחלקת את
    הדרכים, אבל הדרך שלפניה עשתה קפיצה אחת פחות. בטבלה, שורה לכל \( t \) ועמודה לכל מדרגה,
    עם \( S = \{1, 2\} \) :

    <!-- gen 7 -->

    | הקפיצות t | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | 0 | 1 | · | · | · | · | · | · |
    | 1 | · | 1 | 1 | · | · | · | · |
    | 2 | · | · | 1 | 2 | 1 | · | · |
    | 3 | · | · | · | 1 | 3 | 3 | 1 |
    | 4 | · | · | · | · | 1 | 4 | 6 |
    | 5 | · | · | · | · | · | 1 | 5 |
    | 6 | · | · | · | · | · | · | 1 |

    <!-- /gen -->

    כל מספר הוא סכום של שני המספרים בשורה שמעליו, אחד ושניים משמאל. זה המשולש של פסקל, מוזז :
    בשורה \( t \) ובעמודה \( i \) נמצא \( \binom{t}{i - t} \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שורה 0 :** ‏\( w_0(0) = 1 \), וכל השאר 0 : בלי קפיצות נשארים על הקרקע.
    2. **שורה אחרי שורה :** ‏\( w_t(i) = \sum_{s \in S,\ s \le i} w_{t-1}(i - s) \).
    3. **התשובה :** ‏\( w_t(n) \). מספיק לשמור את השורה הקודמת.
    4. **בדיקה :** סכום כל השורות בעמודה \( n \) הוא התשובה של סעיף א.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="count_ways_exact" linenums="1" hl_lines="5"
        def count_ways_exact(n, steps, t):
            """The climbs of n stairs in exactly t jumps: row j holds every stair in j jumps."""
            row = [1] + [0] * n
            for _ in range(t):
                row = [sum(row[i - s] for s in steps if s <= i) for i in range(n + 1)]   # (1)!
            return row[n]
        ```

        1. השורה החדשה נבנית כולה מהשורה הקודמת. אם מעדכנים במקום, כמו בסעיף א, ערך שכבר
           עודכן נקרא שוב, וקפיצה נספרת פעמיים באותה שורה.

    === "SystemVerilog"
        ```systemverilog title="function automatic longint unsigned count_ways_exact" linenums="1" hl_lines="11"
        // The climbs of n stairs in exactly t jumps, a row of stairs per number of jumps
        function automatic longint unsigned count_ways_exact(int n, int steps[$], int t);
          longint unsigned row[], nxt[];
          row = new[n + 1];
          nxt = new[n + 1];
          foreach (row[i]) row[i] = 0;
          row[0] = 1;
          repeat (t) begin
            foreach (nxt[i]) begin
              nxt[i] = 0;
              foreach (steps[k]) if (steps[k] <= i) nxt[i] += row[i - steps[k]];
            end
            row = nxt;
          end
          return row[n];
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **הטבלה.** דרך ל-\( i \) ב-\( t \) קפיצות מסתיימת בקפיצה \( s \), ולפניה דרך ל-\( i - s \)
    ב-\( t - 1 \) קפיצות. ההתאמה חד-חד-ערכית ועל, והקבוצות של \( s \) שונים זרות, כמו בסעיף א.
    באינדוקציה על \( t \) כל שורה נכונה.

    **הנוסחה ל-{1, 2}.** אם בדרך יש \( a \) קפיצות של 1 ו-\( b \) של 2, אז \( a + b = t \)
    ו-\( a + 2b = n \), ולכן \( b = n - t \) ו-\( a = 2t - n \). הדרך נקבעת לפי המקומות של
    הקפיצות של 2 מתוך \( t \) : ‏\( \binom{t}{n-t} \). עם \( n = 10 \) ו-\( t = 7 \) זה
    \( \binom{7}{3} = 35 \). אם \( t < n/2 \) או \( t > n \) אין אף דרך.

    **הקשר לסעיפים הקודמים.** כל דרך עושה מספר כלשהו של קפיצות, ולכן
    \( \sum_t \binom{t}{n-t} = 89 \), התשובה של סעיף א. ומספר ה-\( t \) האפשריים, 6, הוא
    התשובה של סעיף ג : עם \( S = \{1, 2\} \) מספר הקפיצות קובע את האוסף.

    #### סיבוכיות { .sol-cost }

    ‏\( t \) שורות, \( n \cdot |S| \) חיבורים בכל אחת : זמן \( O(t \cdot n \cdot |S|) \),
    וזיכרון של שתי שורות, \( O(n) \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : רקורסיה בלי זיכרון"
    ‏`f(n) = f(n - 1) + f(n - 2)` כרקורסיה פשוטה מחשבת את אותם ערכים שוב ושוב, ומספר
    הקריאות גדל כמו התשובה עצמה, \( F_{n+1} \). ל-\( n = 50 \) זה יותר מ-\( 10^{10} \) קריאות.
    הטבלה, או רקורסיה עם זיכרון, מחשבת כל ערך פעם אחת.

??? trap "מלכודת : w(0) = 0"
    ‏"אין קפיצות, אז אין דרכים" נשמע הגיוני, אבל אז כל הטבלה יוצאת 0. הקרקע היא דרך אחת, הדרך
    הריקה, ועליה נבנות כל השאר.

??? trap "מלכודת : הסדר של הלולאות"
    אותן שתי שורות של קוד, עם הלולאות מוחלפות, סופרות דבר אחר : המדרגות בחוץ סופרות סדרים
    (סעיף א), וגדלי הקפיצה בחוץ סופרים אוספים (סעיף ג). עם \( S = \{1, 2, 3\} \) ו-\( n = 10 \)
    זה 274 מול 14. לפני שכותבים, שואלים אם 1 + 2 ו-2 + 1 הן אותה דרך.

??? trap "מלכודת : גלישה"
    ‏\( F_{n+1} \) גדל פי 1.618 בכל מדרגה. ב-64 ביטים בלי סימן התשובה עם \( S = \{1, 2\} \)
    נכנסת עד \( n = 92 \), ‏\( F_{93} \approx 1.2 \cdot 10^{19} \). אחרי זה צריך מספרים גדולים, או
    שארית, כמו ב-LeetCode.

??? followup "שאלות המשך"
    - **המדרגה הבאה בזיכרון קבוע :** כתבו את סעיף א עם שלושה משתנים בלבד, ל-\( S = \{1, 2\} \).

        ??? fu-answer "תשובה"
            ‏`a, b = 1, 1` הם \( w(i-1) \) ו-\( w(i) \), ובכל צעד `a, b = b, a + b`. אחרי
            \( n - 1 \) צעדים \( b = w(n) \). ל-\( S \) כללי : חלון מעגלי של \( \max S \) ערכים.

    - **עלות לכל מדרגה :** לכל מדרגה יש עלות, ומשלמים על כל מדרגה שנוחתים עליה. מה העלות
      הקטנה ביותר להגיע ל-\( n \)?

        ??? fu-answer "תשובה"
            אותה טבלה, עם מינימום במקום סכום : \( c(i) = \text{cost}(i) + \min_s c(i - s) \).
            הקפיצה האחרונה עדיין מחלקת את הדרכים, ומהטובה בכל קבוצה בוחרים את הטובה ביותר.

    - **מטבעות :** כמה דרכים יש לשלם 10 שקלים במטבעות של 1, 2 ו-5?

        ??? fu-answer "תשובה"
            זה סעיף ג : סכום בלי סדר, ‏\( S = \{1, 2, 5\} \) ו-\( n = 10 \), ויש 10 דרכים. אם
            הסדר שבו משלמים חשוב, זה סעיף א, ויש 128.
