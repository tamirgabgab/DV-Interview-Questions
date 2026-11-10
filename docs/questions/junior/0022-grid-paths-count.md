---
id: 22
title: מסלולים בלוח – ימינה ולמטה, מכשולים, וגם למעלה
level: junior
difficulty: medium
kind: code
tags: [algorithms, combinatorics, dynamic-programming, proof, python, systemverilog]
source: "שאלה קלאסית (Unique Paths, LeetCode 62, ועם מכשולים LeetCode 63); סעיפים ג ו-ד מוסיפים צעד למעלה"
added: 2026-11-07
---

## השאלה

רובוט עומד בתא השמאלי העליון של לוח עם \( m \) שורות ו-\( n \) עמודות, וצריך להגיע לתא
הימני התחתון. בכל צעד הוא זז תא אחד. כמה מסלולים שונים יש לו? השאלה בארבעה סעיפים, וכל
סעיף משנה כלל אחד :

1. **ימינה ולמטה :** לוח ריק של 3 שורות ו-7 עמודות, ואחר כך כל לוח.
2. **מכשולים :** חלק מהתאים חסומים, ואסור לעבור בהם.
3. **גם למעלה :** מותר ימינה, למעלה ולמטה, אבל אסור לעבור באותו תא פעמיים. בלי הכלל הזה
   יש אינסוף מסלולים בכל לוח עם שתי שורות לפחות.
4. **גם למעלה, עם מכשולים :** שני הכללים יחד.

המספרים גדלים מהר, ולכן בכל סעיף מחזירים את המספר המדויק, וגם את השארית שלו בחלוקה
ל-\( 10^9 + 7 \), כמו ב-LeetCode.

??? interviewer "מה המראיין בודק"
    - **ספירה בלי למנות :** האם המועמד רואה שמסלול הוא רק סדר של צעדים, ומגיע לנוסחה ולא
      לחיפוש שעובר על כל המסלולים.
    - **תכנון דינמי :** כל תא הוא סכום של התאים שמהם מגיעים אליו. האם הוא מסביר למה אין
      ספירה כפולה, ולמה מכשול הוא פשוט 0.
    - **מה משתנה כשמוסיפים כיוון :** עם צעד למעלה כבר אין סדר פשוט בין התאים. האם הוא מוצא
      מה כן נשאר פשוט : בכל עמודה המסלול הוא קטע אנכי אחד.
    - **מספרים גדולים :** מתי 64 ביטים מספיקים, ואיך מחלקים מודולו ראשוני בלי פעולת חילוק.

---

### סעיף א – ימינה ולמטה בלבד

כמה מסלולים יש בלוח של 3 שורות ו-7 עמודות, כשכל צעד הוא ימינה או למטה? ומה התשובה ללוח
של \( m \) שורות ו-\( n \) עמודות? כתבו פונקציה שמחזירה את המספר המדויק, ופונקציה
שמחזירה אותו מודולו \( 10^9 + 7 \).

??? tip "רמז 1"
    כמה צעדים ימינה וכמה צעדים למטה יש בכל מסלול? האם המספרים האלה תלויים במסלול?

??? tip "רמז 2"
    מאילו תאים אפשר להגיע לתא \( (r, c) \) בצעד אחד? מה זה אומר על מספר המסלולים שנגמרים בו?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **‏28.** בכל מסלול יש בדיוק 2 צעדים למטה ו-6 צעדים ימינה, 8 צעדים בסך הכול, ומסלול
        נקבע לפי המקומות של שני הצעדים למטה מתוך השמונה : \( \binom{8}{2} = 28 \). בלוח
        כללי התשובה היא \( \binom{m+n-2}{m-1} \). אותו מספר יוצא מטבלה שבה כל תא הוא סכום
        של התא משמאלו והתא מעליו.

    <!-- cost: זמן \( O(mn) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    מסלול לא יכול לחזור אחורה, ולכן הוא יורד בדיוק \( m - 1 \) שורות וזז בדיוק \( n - 1 \)
    עמודות. מה שמבדיל בין שני מסלולים הוא רק **הסדר** של הצעדים. בלוח של 3 על 3 יש שני
    צעדים ימינה ושניים למטה, וששה סדרים שלהם :

    <!-- gen 0 -->

    <svg class="figure gx-fig lp-fig lp-small" viewBox="0 0 328 43" style="max-width:20.5rem" role="img" aria-label="ששת המסלולים של לוח 3 על 3 בצעדים ימינה ולמטה : בכל אחד שני צעדים ימינה ושני צעדים למטה, בסדר אחר"><g class="lp-one"><title>path 1: →→↓↓</title><rect class="lp-sq lp-end" x="2.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="15.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="28.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="2.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="15.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="28.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="2.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="15.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="28.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="8.5,8.5 21.5,8.5 34.5,8.5 34.5,21.5 34.5,34.5"/></g><g class="lp-one"><title>path 2: →↓→↓</title><rect class="lp-sq lp-end" x="53.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="66.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="79.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="53.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="66.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="79.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="53.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="66.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="79.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="59.5,8.5 72.5,8.5 72.5,21.5 85.5,21.5 85.5,34.5"/></g><g class="lp-one"><title>path 3: →↓↓→</title><rect class="lp-sq lp-end" x="104.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="117.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="130.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="104.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="117.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="130.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="104.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="117.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="130.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="110.5,8.5 123.5,8.5 123.5,21.5 123.5,34.5 136.5,34.5"/></g><g class="lp-one"><title>path 4: ↓→→↓</title><rect class="lp-sq lp-end" x="155.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="168.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="181.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="155.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="168.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="181.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="155.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="168.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="181.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="161.5,8.5 161.5,21.5 174.5,21.5 187.5,21.5 187.5,34.5"/></g><g class="lp-one"><title>path 5: ↓→↓→</title><rect class="lp-sq lp-end" x="206.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="219.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="232.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="206.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="219.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="232.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="206.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="219.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="232.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="212.5,8.5 212.5,21.5 225.5,21.5 225.5,34.5 238.5,34.5"/></g><g class="lp-one"><title>path 6: ↓↓→→</title><rect class="lp-sq lp-end" x="257.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="270.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="283.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="257.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="270.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="283.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="257.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="270.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="283.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="263.5,8.5 263.5,21.5 263.5,34.5 276.5,34.5 289.5,34.5"/></g></svg>

    <!-- /gen -->

    אפשר גם לספור תא אחרי תא. כמה מסלולים נגמרים בכל תא של הלוח של 3 על 7 :

    <!-- gen 1 -->

    <svg class="figure gx-fig lp-fig" viewBox="0 0 268 130" style="max-width:16.75rem" role="img" aria-label="לוח 3 על 7 : בכל תא מספר המסלולים מ-S שנגמרים בו, ימינה ולמטה. השורה העליונה והעמודה השמאלית הן 1, כל תא אחר הוא סכום של התא משמאלו והתא מעליו, ובתא T יש 28"><text class="tick" x="41" y="14" text-anchor="middle">0</text><text class="tick" x="75" y="14" text-anchor="middle">1</text><text class="tick" x="109" y="14" text-anchor="middle">2</text><text class="tick" x="143" y="14" text-anchor="middle">3</text><text class="tick" x="177" y="14" text-anchor="middle">4</text><text class="tick" x="211" y="14" text-anchor="middle">5</text><text class="tick" x="245" y="14" text-anchor="middle">6</text><text class="tick" x="17" y="43" text-anchor="end">0</text><text class="tick" x="17" y="77" text-anchor="end">1</text><text class="tick" x="17" y="111" text-anchor="end">2</text><g class="gx-cell is-open lp-h1"><title>cell (0, 0): 1 path ends here</title><rect x="25.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 1): 1 path ends here</title><rect x="59.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 2): 1 path ends here</title><rect x="93.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 3): 1 path ends here</title><rect x="127.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 4): 1 path ends here</title><rect x="161.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 5): 1 path ends here</title><rect x="195.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 6): 1 path ends here</title><rect x="229.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (1, 0): 1 path ends here</title><rect x="25.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (1, 1): 2 paths end here</title><rect x="59.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (1, 2): 3 paths end here</title><rect x="93.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (1, 3): 4 paths end here</title><rect x="127.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (1, 4): 5 paths end here</title><rect x="161.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h3"><title>cell (1, 5): 6 paths end here</title><rect x="195.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h3"><title>cell (1, 6): 7 paths end here</title><rect x="229.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (2, 0): 1 path ends here</title><rect x="25.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (2, 1): 3 paths end here</title><rect x="59.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h3"><title>cell (2, 2): 6 paths end here</title><rect x="93.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h3"><title>cell (2, 3): 10 paths end here</title><rect x="127.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (2, 4): 15 paths end here</title><rect x="161.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (2, 5): 21 paths end here</title><rect x="195.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (2, 6): 28 paths end here</title><rect x="229.5" y="91.5" width="31" height="31" rx="3"/></g><text class="gx-val" x="41" y="47" text-anchor="middle">1</text><text class="gx-tag" x="28" y="34">S</text><text class="gx-val" x="75" y="44" text-anchor="middle">1</text><text class="gx-val" x="109" y="44" text-anchor="middle">1</text><text class="gx-val" x="143" y="44" text-anchor="middle">1</text><text class="gx-val" x="177" y="44" text-anchor="middle">1</text><text class="gx-val" x="211" y="44" text-anchor="middle">1</text><text class="gx-val" x="245" y="44" text-anchor="middle">1</text><text class="gx-val" x="41" y="78" text-anchor="middle">1</text><text class="gx-val" x="75" y="78" text-anchor="middle">2</text><text class="gx-val" x="109" y="78" text-anchor="middle">3</text><text class="gx-val" x="143" y="78" text-anchor="middle">4</text><text class="gx-val" x="177" y="78" text-anchor="middle">5</text><text class="gx-val" x="211" y="78" text-anchor="middle">6</text><text class="gx-val" x="245" y="78" text-anchor="middle">7</text><text class="gx-val" x="41" y="112" text-anchor="middle">1</text><text class="gx-val" x="75" y="112" text-anchor="middle">3</text><text class="gx-val" x="109" y="112" text-anchor="middle">6</text><text class="gx-val" x="143" y="112" text-anchor="middle">10</text><text class="gx-val" x="177" y="112" text-anchor="middle">15</text><text class="gx-val" x="211" y="112" text-anchor="middle">21</text><text class="gx-val" x="245" y="115" text-anchor="middle">28</text><text class="gx-tag" x="232" y="102">T</text></svg>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="gx-key-s"></i>S ההתחלה, T היעד</span><span><i class="lp-key-lo"></i>מעט מסלולים</span><span><i class="lp-key-hi"></i>הרבה מסלולים</span><span><i class="gx-key is-wall"></i>מכשול</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ספירת הצעדים :** בכל מסלול יש \( m - 1 \) צעדים למטה ו-\( n - 1 \) צעדים ימינה,
       ‏\( m + n - 2 \) צעדים בסך הכול.
    2. **בחירה :** מסלול נקבע לפי המקומות של הצעדים למטה : בוחרים \( m - 1 \) מקומות מתוך
       \( m + n - 2 \). בלוח של 3 על 7 בוחרים 2 מתוך 8, ‏\( \frac{8 \cdot 7}{2} = 28 \).
    3. **הטבלה :** בשורה העליונה ובעמודה השמאלית יש מסלול אחד לכל תא. כל תא אחר הוא סכום של
       התא משמאלו והתא מעליו.
    4. **שורה אחת :** מספיק לשמור שורה אחת של \( n \) מספרים, ולעבור עליה משמאל לימין
       \( m - 1 \) פעמים : המספר שמשמאל כבר של השורה החדשה, והמספר במקום עוד של השורה
       שמעל.
    5. **מודולו :** ‏\( p = 10^9 + 7 \) ראשוני, ולכן במקום לחלק במכנה \( d \) כופלים
       ב-\( d^{p-2} \bmod p \), ההופכי שלו.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="paths_rd" linenums="1" hl_lines="9 17 27"
        from math import comb

        MOD = 10**9 + 7


        def paths_rd(m, n):
            """Right and down only, from the top-left cell to the bottom-right one: choose
            which m - 1 of the m + n - 2 steps go down."""
            return comb(m + n - 2, m - 1)                        # (1)!


        def paths_rd_dp(m, n):
            """The same count cell by cell, one row of n numbers at a time."""
            row = [1] * n                                        # (2)!
            for _ in range(m - 1):
                for c in range(1, n):
                    row[c] += row[c - 1]                         # (3)!
            return row[-1]


        def paths_rd_mod(m, n, p=MOD):
            """The count mod a prime p larger than m + n - 2."""
            k, top = m - 1, m + n - 2
            num = den = 1
            for i in range(1, k + 1):
                num, den = num * (top - k + i) % p, den * i % p
            return num * pow(den, p - 2, p) % p                  # (4)!
        ```

        1. ב-Python ‏`comb` מחזיר מספר מדויק בכל גודל. בלוח של 3 על 7 זה
           \( \binom{8}{2} = 28 \).
        2. השורה העליונה : לכל תא בה מגיעים בדרך אחת, ימינה כל הזמן.
        3. לפני השורה הזו `row[c]` הוא המספר של התא שמעל, ו-`row[c - 1]` כבר עודכן, והוא
           המספר של התא משמאל. הסכום הוא המספר של התא.
        4. ‏`pow(den, p - 2, p)` הוא ההופכי של המכנה מודולו \( p \), לפי המשפט הקטן של
           פרמה. המכנה הוא \( (m-1)! \), ו-\( p \) לא מחלק אותו כי \( p > m + n - 2 \).

    === "SystemVerilog"
        ```systemverilog title="function automatic longint unsigned paths_rd" linenums="1" hl_lines="8"
        // Right and down only: the same row of sums, in 64 bits. Every number of the row is at
        // most the answer, so it is exact while the answer is below 2^64.
        function automatic longint unsigned paths_rd(int m, int n);
          longint unsigned row[];
          row = new[n];
          foreach (row[c]) row[c] = 1;
          for (int r = 1; r < m; r++)
            for (int c = 1; c < n; c++) row[c] += row[c - 1];   // (1)!
          return row[n - 1];
        endfunction
        ```

        1. רק חיבורים, ואף מספר בשורה לא גדול מהתשובה. לכן אין גלישה לפני שהתשובה עצמה
           גולשת : לוח ריבועי עד 34 על 34, שבו התשובה היא בערך \( 7.2 \cdot 10^{18} \).
           בלוח של 35 על 35 היא כבר \( 2.8 \cdot 10^{19} \), יותר מ-\( 2^{64} \).

    #### למה זה נכון { .sol-proof }

    **הנוסחה.** ממסלול קוראים את קבוצת המקומות שבהם הוא יורד : \( m - 1 \) מקומות מתוך
    \( m + n - 2 \). להפך, מכל קבוצה כזו בונים מסלול שיורד בדיוק בה וזז ימינה בכל השאר. הוא
    נשאר בתוך הלוח, כי יש בו \( m - 1 \) צעדים למטה ו-\( n - 1 \) ימינה, ושני מסלולים שונים
    יורדים במקומות שונים. ההתאמה חד-חד-ערכית ועל, ולכן יש \( \binom{m+n-2}{m-1} \) מסלולים.

    **הטבלה.** הצעד האחרון של מסלול שנגמר בתא \( (r, c) \) בא מהתא משמאל או מהתא מלמעלה, ואף
    מסלול לא בא משניהם. לכן המסלולים לתא מתחלקים לשתי קבוצות זרות, והמספר הוא הסכום. זה
    המשולש של פסקל, מסובב : המספר בתא \( (r, c) \) הוא \( \binom{r+c}{r} \).

    **המודולו.** ‏\( \binom{m+n-2}{m-1} = \frac{\text{num}}{\text{den}} \), כש-num הוא מכפלה
    של \( m - 1 \) המספרים הגדולים עד \( m + n - 2 \) ו-den הוא \( (m-1)! \). כל הגורמים של
    den קטנים מ-\( p \), ו-\( p \) ראשוני, ולכן \( \text{den} \not\equiv 0 \). לפי המשפט
    הקטן של פרמה \( \text{den}^{p-1} \equiv 1 \pmod p \), ולכן \( \text{den}^{p-2} \) הוא
    ההופכי שלו, והמכפלה נותנת את השארית של התשובה.

    #### סיבוכיות { .sol-cost }

    הנוסחה : \( m - 1 \) כפלים, על מספרים שגדלים עד התשובה. הטבלה : \( (m-1)(n-1) \) חיבורים,
    זמן \( O(mn) \) וזיכרון של שורה אחת, \( O(n) \). המודולו : \( m - 1 \) כפלים ועוד חזקה,
    ‏\( O(m + \log p) \).

---

### סעיף ב – מכשולים

חלק מהתאים חסומים, ‏`grid[r][c] == 1`, ואסור לעבור בהם. כמה מסלולים ימינה ולמטה יש בלוח של
3 על 7 עם מכשולים בתאים \( (0, 5) \), \( (1, 1) \) ו-\( (2, 3) \)? כתבו פונקציה לכל לוח,
ומודול חומרה שמקבל שורה אחת של הלוח בכל מחזור שעון.

??? tip "רמז 1"
    האם הנוסחה של סעיף א עוד עובדת? ומה בטבלה של סעיף א נשאר נכון?

??? tip "רמז 2"
    כמה מסלולים נגמרים בתא חסום?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **‏9.** אותה טבלה של סעיף א, רק שבתא חסום כותבים 0 : אף מסלול לא נגמר בו, ולכן הוא
        לא מוסיף כלום לתאים שאחריו. הנוסחה כבר לא עובדת, כי היא סופרת גם מסלולים שעוברים
        במכשול. החומרה מחזיקה שורה אחת של מונים, ומעדכנת את כולה בשעון אחד לכל שורה של
        הלוח.

    <!-- cost: זמן \( O(mn) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    הטיעון של הטבלה לא השתמש בכך שהלוח ריק : לתא פנוי מגיעים משמאל או מלמעלה, ומסלול
    שנגמר בתא חסום לא קיים. לכן ממלאים את אותה טבלה, עם 0 בכל מכשול :

    <!-- gen 3 -->

    <svg class="figure gx-fig lp-fig" viewBox="0 0 268 130" style="max-width:16.75rem" role="img" aria-label="הלוח של סעיף ב : 3 על 7 עם שלושה מכשולים. בכל תא פנוי מספר המסלולים מ-S שנגמרים בו, ימינה ולמטה, ובתא T יש 9"><text class="tick" x="41" y="14" text-anchor="middle">0</text><text class="tick" x="75" y="14" text-anchor="middle">1</text><text class="tick" x="109" y="14" text-anchor="middle">2</text><text class="tick" x="143" y="14" text-anchor="middle">3</text><text class="tick" x="177" y="14" text-anchor="middle">4</text><text class="tick" x="211" y="14" text-anchor="middle">5</text><text class="tick" x="245" y="14" text-anchor="middle">6</text><text class="tick" x="17" y="43" text-anchor="end">0</text><text class="tick" x="17" y="77" text-anchor="end">1</text><text class="tick" x="17" y="111" text-anchor="end">2</text><g class="gx-cell is-open lp-h1"><title>cell (0, 0): 1 path ends here</title><rect x="25.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 1): 1 path ends here</title><rect x="59.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 2): 1 path ends here</title><rect x="93.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 3): 1 path ends here</title><rect x="127.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 4): 1 path ends here</title><rect x="161.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (0, 5): an obstacle</title><rect x="195.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h0"><title>cell (0, 6): 0 paths end here</title><rect x="229.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (1, 0): 1 path ends here</title><rect x="25.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 1): an obstacle</title><rect x="59.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (1, 2): 1 path ends here</title><rect x="93.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (1, 3): 2 paths end here</title><rect x="127.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (1, 4): 3 paths end here</title><rect x="161.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (1, 5): 3 paths end here</title><rect x="195.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (1, 6): 3 paths end here</title><rect x="229.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (2, 0): 1 path ends here</title><rect x="25.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (2, 1): 1 path ends here</title><rect x="59.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (2, 2): 2 paths end here</title><rect x="93.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 3): an obstacle</title><rect x="127.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (2, 4): 3 paths end here</title><rect x="161.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (2, 5): 6 paths end here</title><rect x="195.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (2, 6): 9 paths end here</title><rect x="229.5" y="91.5" width="31" height="31" rx="3"/></g><text class="gx-val" x="41" y="47" text-anchor="middle">1</text><text class="gx-tag" x="28" y="34">S</text><text class="gx-val" x="75" y="44" text-anchor="middle">1</text><text class="gx-val" x="109" y="44" text-anchor="middle">1</text><text class="gx-val" x="143" y="44" text-anchor="middle">1</text><text class="gx-val" x="177" y="44" text-anchor="middle">1</text><text class="gx-val" x="245" y="44" text-anchor="middle">0</text><text class="gx-val" x="41" y="78" text-anchor="middle">1</text><text class="gx-val" x="109" y="78" text-anchor="middle">1</text><text class="gx-val" x="143" y="78" text-anchor="middle">2</text><text class="gx-val" x="177" y="78" text-anchor="middle">3</text><text class="gx-val" x="211" y="78" text-anchor="middle">3</text><text class="gx-val" x="245" y="78" text-anchor="middle">3</text><text class="gx-val" x="41" y="112" text-anchor="middle">1</text><text class="gx-val" x="75" y="112" text-anchor="middle">1</text><text class="gx-val" x="109" y="112" text-anchor="middle">2</text><text class="gx-val" x="177" y="112" text-anchor="middle">3</text><text class="gx-val" x="211" y="112" text-anchor="middle">6</text><text class="gx-val" x="245" y="115" text-anchor="middle">9</text><text class="gx-tag" x="232" y="102">T</text></svg>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ההתחלה :** אם התא \( (0, 0) \) פנוי, יש בו מסלול אחד.
    2. **תא חסום :** 0.
    3. **תא פנוי :** הסכום של התא משמאלו והתא מעליו, כשתא מחוץ ללוח הוא 0.
    4. **התשובה :** המספר בתא הימני התחתון. אם הוא חסום, התשובה 0.
    5. **מודולו :** שארית אחרי כל חיבור. שתי שאריות מסתכמות לפחות מ-\( 2p \), ולכן מספיק
       להשוות ל-\( p \) ולחסר פעם אחת.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="paths_rd_blocked" linenums="1" hl_lines="9 11"
        def paths_rd_blocked(grid, p=None):
            """grid[r][c] == 1 is an obstacle. Right and down, from the top-left cell to the
            bottom-right one: the exact count, or the count mod p."""
            n = len(grid[0])
            row = [1] + [0] * (n - 1)                            # (1)!
            for cells in grid:
                for c in range(n):
                    if cells[c]:
                        row[c] = 0                               # (2)!
                    elif c:
                        row[c] += row[c - 1]
                    if p:
                        row[c] %= p
            return row[-1]
        ```

        1. השורה "שמעל" הלוח : מסלול אחד שנכנס לתא \( (0, 0) \), ההתחלה. כך השורה הראשונה
           מתמלאת באותו קוד כמו כל השאר.
        2. מכשול מאפס את המונה. מה שהיה בו, המספר של התא שמעליו, לא עובר הלאה.

    === "SystemVerilog"
        ```systemverilog title="module paths_rows" linenums="1" hl_lines="15 20 22"
        // Right and down with obstacles, one row of the board a clock. P = 0: the exact count in
        // W bits; P > 0: the count mod P.
        module paths_rows #(parameter int N = 7, W = 64, parameter longint unsigned P = 0) (
          input  logic         clk, rst_n,
          input  logic         valid,          // block holds a row this clock
          input  logic         first,          // the row is the board's first
          input  logic [N-1:0] block,          // bit c: the cell in column c is an obstacle
          output logic [W-1:0] count);         // the paths to the last cell of the rows so far

          logic [W-1:0] row [N];               // the paths that end at each cell of the last row
          logic [W-1:0] nxt [N];

          function automatic logic [W-1:0] add(logic [W-1:0] a, logic [W-1:0] b);
            logic [W:0] s = {1'b0, a} + {1'b0, b};
            if (P != 0 && s >= (W+1)'(P)) s -= (W+1)'(P);       // (1)!
            return s[W-1:0];
          endfunction

          always_comb begin
            nxt[0] = block[0] ? '0 : first ? W'(1) : row[0];
            for (int c = 1; c < N; c++)
              nxt[c] = block[c] ? '0 : add(first ? '0 : row[c], nxt[c - 1]);   // (2)!
          end

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) row <= '{default: '0};
            else if (valid) row <= nxt;

          assign count = row[N-1];
        endmodule
        ```

        1. שתי שאריות קטנות מ-\( P \), והסכום שלהן קטן מ-\( 2P \) : השוואה אחת וחיסור אחד
           מחזירים אותו לשארית, בלי פעולת חילוק.
        2. ‏`row[c]` הוא התא שמעל, ו-`nxt[c - 1]` התא משמאל באותה שורה, שחושב באותו שעון.
           כל השורה היא שרשרת של \( N - 1 \) מחברים, כמו ב-ripple carry, וזה הנתיב הקריטי :
           ב-\( N = 7 \) ו-\( W = 64 \) שישה מחברים של 64 ביטים בשעון אחד. בלוח רחב שמים
           רגיסטר באמצע השורה : החצי הימני של שורה מחושב בשעון שאחרי החצי השמאלי שלה, ביחד עם
           החצי השמאלי של השורה הבאה. עדיין נכנסת שורה בכל שעון, והתשובה מגיעה שעון אחד אחר כך.

    #### למה זה נכון { .sol-proof }

    **הטבלה.** נסמן ב-\( f(r, c) \) את מספר המסלולים מ-\( (0, 0) \) שנגמרים בתא \( (r, c) \).
    בתא חסום \( f = 0 \), כי מסלול לא נכנס אליו. בתא פנוי הצעד האחרון בא משמאל או מלמעלה,
    והקבוצות זרות, ולכן \( f(r, c) = f(r, c-1) + f(r-1, c) \), כשתא מחוץ ללוח נותן 0. אם
    אחד השכנים חסום, הוא מוסיף 0, וזה נכון : אף מסלול לא בא ממנו. באינדוקציה על \( r + c \)
    כל מספר בטבלה נכון.

    **הנוסחה נשברת.** ‏\( \binom{8}{2} = 28 \) סופרת את כל הסדרים של הצעדים, גם כאלה שעוברים
    במכשול. בלוח הזה 19 מתוך ה-28 עוברים באחד המכשולים לפחות, ונשארים 9.

    **החומרה.** בכל שעון `row` מחזיק את \( f \) של השורה הקודמת, ו-`nxt` מחשב את השורה החדשה
    משמאל לימין באותו סדר של הקוד ב-Python. ‏`first` מחליף את השורה שמעל בשורה של ההתחלה :
    1 בעמודה 0 ו-0 בכל השאר. אחרי השורה האחרונה `count` הוא \( f(m-1, n-1) \).

    בלוח של סעיף ב נכנסת שורה בכל שעון, ו-`first` הוא 1 בשורה 0. אחרי כל שעון `row` הוא
    השורה של הטבלה, עם 0 במכשול :

    <!-- gen 4 -->

    | שורה | בלוח | ‏`block` | ‏`row` אחרי השעון | ‏`count` |
    |:-:|:-:|:-:|:-:|:-:|
    | 0 | ‏<span dir="ltr">0000010</span> | ‏`7'b0100000` | ‏<span dir="ltr">[1, 1, 1, 1, 1, 0, 0]</span> | 0 |
    | 1 | ‏<span dir="ltr">0100000</span> | ‏`7'b0000010` | ‏<span dir="ltr">[1, 0, 1, 2, 3, 3, 3]</span> | 3 |
    | 2 | ‏<span dir="ltr">0001000</span> | ‏`7'b0001000` | ‏<span dir="ltr">[1, 1, 2, 0, 3, 6, 9]</span> | 9 |

    <!-- /gen -->

    **סדר הביטים.** ב-`block` הביט \( c \) הוא עמודה \( c \), וליטרל של SystemVerilog נכתב
    מהביט הגבוה. לכן השורה <span dir="ltr">0000010</span> של הלוח, עם מכשול בעמודה 5, נכנסת
    כ-`7'b0100000`, הפוכה. בבדיקה שבונה את `block` ממחרוזת של הלוח זו טעות נפוצה.

    **נסו בעצמכם.** הורידו את המכשול מ-\( (1, 1) \) : ‏T עולה מ-9 ל-15. בלי \( (0, 5) \)
    יש 12, ובלי \( (2, 3) \) יש 13. שימו מכשול ב-\( (0, 2) \) : ימינה ולמטה אין אף מסלול,
    ועם "ימינה, למעלה ולמטה" יש 8, כי המסלול עולה בחזרה בעמודה 2. ‏"ניקוי" ולוח של 10 על 10
    נותנים \( \binom{18}{9} = 48{,}620 \), ועם צעד למעלה \( 10^9 \). "שעון אחד" ממלא את
    הלוח שורה אחרי שורה, כמו `paths_rows` בטבלה למעלה. מעבר לאיורים, בקופסה יש כל לוח עד 10
    על 10, שני סוגי הצעדים על אותו לוח, ומסלול אקראי שלכל המסלולים יש בו אותו סיכוי :

    <div class="explorer" data-kind="latpaths" data-grid="0000010.0100000.0001000"></div>

    #### סיבוכיות { .sol-cost }

    כל תא נקרא פעם אחת : זמן \( O(mn) \), וזיכרון של שורה אחת, \( O(n) \). בחומרה \( m \)
    שעונים, ו-\( n \) מונים של \( W \) ביטים עם שרשרת של \( n - 1 \) מחברים בכל שעון.

---

### סעיף ג – גם למעלה

עכשיו מותר לזוז ימינה, למעלה או למטה, אבל אסור לעבור באותו תא פעמיים. כמה מסלולים יש
בלוח הריק של 3 על 7? ובלוח של \( m \) שורות ו-\( n \) עמודות? למה בלי הכלל של "לא פעמיים"
אין תשובה?

??? tip "רמז 1"
    אין צעד שמאלה. מה זה אומר על הסדר שבו המסלול עובר בעמודות?

??? tip "רמז 2"
    בתוך עמודה אחת, האם המסלול יכול לרדת ואחר כך לעלות? ואם לא, מה קובע את מה שהוא עושה
    בעמודה?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        **‏\( 3^6 = 729 \).** בלי צעד שמאלה המסלול עובר בעמודות לפי הסדר, ובכל עמודה הוא קטע
        אנכי אחד : לרדת ואחר כך לעלות היה מחזיר אותו לתא שכבר עבר בו. לכן מסלול נקבע לפי
        השורה שבה הוא יוצא מכל עמודה חוץ מהאחרונה, ובכל אחת יש \( m \) אפשרויות :
        \( m^{n-1} \). בלוח של 10 על 10 זה \( 10^9 \), לעומת 48,620 ימינה ולמטה.

    <!-- cost: זמן \( O(\log n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    במקום לשאול איך המסלול זז, שואלים איפה הוא **עוזב** כל עמודה. בלוח של 3 על 3 יש שלוש
    שורות יציאה לעמודה 0 ושלוש לעמודה 1, ובעמודה האחרונה יורדים ל-T. אלה תשעת המסלולים :

    <!-- gen 5 -->

    <svg class="figure gx-fig lp-fig lp-small" viewBox="0 0 277 94" style="max-width:17.3125rem" role="img" aria-label="תשעת המסלולים של לוח 3 על 3 כשמותר גם למעלה, בלי לחזור לתא : בכל עמודה המסלול הוא קטע אנכי אחד, ובשתי העמודות הראשונות בוחרים את שורת היציאה"><g class="lp-one"><title>path 1: →→↓↓</title><rect class="lp-sq lp-end" x="2.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="15.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="28.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="2.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="15.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="28.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="2.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="15.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="28.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="8.5,8.5 21.5,8.5 34.5,8.5 34.5,21.5 34.5,34.5"/></g><g class="lp-one"><title>path 2: →↓→↓</title><rect class="lp-sq lp-end" x="53.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="66.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="79.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="53.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="66.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="79.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="53.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="66.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="79.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="59.5,8.5 72.5,8.5 72.5,21.5 85.5,21.5 85.5,34.5"/></g><g class="lp-one"><title>path 3: →↓↓→</title><rect class="lp-sq lp-end" x="104.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="117.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="130.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="104.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="117.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="130.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="104.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="117.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="130.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="110.5,8.5 123.5,8.5 123.5,21.5 123.5,34.5 136.5,34.5"/></g><g class="lp-one"><title>path 4: ↓→→↓</title><rect class="lp-sq lp-end" x="155.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="168.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="181.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="155.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="168.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="181.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="155.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="168.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="181.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="161.5,8.5 161.5,21.5 174.5,21.5 187.5,21.5 187.5,34.5"/></g><g class="lp-one"><title>path 5: ↓→↓→</title><rect class="lp-sq lp-end" x="206.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="219.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="232.75" y="2.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="206.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="219.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="232.75" y="15.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="206.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="219.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="232.75" y="28.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="212.5,8.5 212.5,21.5 225.5,21.5 225.5,34.5 238.5,34.5"/></g><g class="lp-one"><title>path 6: ↓→↑→↓↓</title><rect class="lp-sq lp-end" x="2.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="15.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="28.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="2.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="15.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="28.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="2.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="15.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="28.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="8.5,59.5 8.5,72.5 21.5,72.5 21.5,59.5 34.5,59.5 34.5,72.5 34.5,85.5"/></g><g class="lp-one"><title>path 7: ↓↓→→</title><rect class="lp-sq lp-end" x="53.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="66.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="79.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="53.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="66.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="79.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="53.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="66.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="79.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="59.5,59.5 59.5,72.5 59.5,85.5 72.5,85.5 85.5,85.5"/></g><g class="lp-one"><title>path 8: ↓↓→↑→↓</title><rect class="lp-sq lp-end" x="104.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="117.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="130.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="104.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="117.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="130.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="104.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="117.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="130.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="110.5,59.5 110.5,72.5 110.5,85.5 123.5,85.5 123.5,72.5 136.5,72.5 136.5,85.5"/></g><g class="lp-one"><title>path 9: ↓↓→↑↑→↓↓</title><rect class="lp-sq lp-end" x="155.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="168.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="181.75" y="53.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="155.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="168.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="181.75" y="66.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="155.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq" x="168.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><rect class="lp-sq lp-end" x="181.75" y="79.75" width="11.5" height="11.5" rx="1.5"/><polyline class="lp-line" points="161.5,59.5 161.5,72.5 161.5,85.5 174.5,85.5 174.5,72.5 174.5,59.5 187.5,59.5 187.5,72.5 187.5,85.5"/></g></svg>

    <!-- /gen -->

    כך גדלים שני המספרים. העמודה האחרונה של הטבלה, "גם שמאלה", סופרת את המסלולים שמותר בהם
    גם צעד שמאלה, בלי לחזור לתא. אותם ספרנו בחיפוש מלא :

    <!-- gen 6 -->

    | הלוח | ימינה ולמטה | ימינה, למעלה ולמטה | גם שמאלה |
    |---|:-:|:-:|:-:|
    | ‏<span dir="ltr">2 × 2</span> | 2 | 2 | 2 |
    | ‏<span dir="ltr">3 × 3</span> | 6 | 9 | 12 |
    | ‏<span dir="ltr">3 × 7</span> | 28 | 729 | 1,369 |
    | ‏<span dir="ltr">4 × 4</span> | 20 | 64 | 184 |
    | ‏<span dir="ltr">5 × 5</span> | 70 | 625 | 8,512 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **עמודות לפי הסדר :** אין צעד שמאלה, ולכן מסלול שעזב עמודה לא חוזר אליה.
    2. **קטע אנכי :** בתוך עמודה המסלול זז רק למעלה או למטה. אם הוא מחליף כיוון, הצעד הבא
       מחזיר אותו לתא שהוא בא ממנו. לכן בכל עמודה הוא קטע אנכי אחד, מהשורה שבה נכנס לשורה
       שבה יוצא.
    3. **שורת יציאה :** בכל עמודה חוץ מהאחרונה בוחרים את השורה שממנה זזים ימינה, \( m \)
       אפשרויות. בעמודה האחרונה אין בחירה : יורדים ל-T.
    4. **ספירה :** ‏\( n - 1 \) בחירות של \( m \) אפשרויות, \( m^{n-1} \).
    5. **מודולו :** חזקה בריבועים חוזרים, כ-\( 2 \log_2 n \) כפלים.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="paths_rud" linenums="1" hl_lines="4 8 25"
        def paths_rud(m, n):
            """Right, up and down, never a cell twice: an exit row in every column but the
            last one."""
            return m ** (n - 1)


        def paths_rud_mod(m, n, p=MOD):
            return pow(m, n - 1, p)                              # (1)!


        def count_walks(grid, moves):
            """Every path by brute force: depth first, never a cell twice. moves is a list of
            (dr, dc), e.g. [(0, 1), (1, 0), (-1, 0)] for right, down and up."""
            m, n = len(grid), len(grid[0])
            seen = {(0, 0)}

            def go(r, c):
                if (r, c) == (m - 1, n - 1):
                    return 1
                total = 0
                for dr, dc in moves:
                    a, b = r + dr, c + dc
                    if 0 <= a < m and 0 <= b < n and not grid[a][b] and (a, b) not in seen:
                        seen.add((a, b))
                        total += go(a, b)                        # (2)!
                        seen.remove((a, b))
                return total

            return 0 if grid[0][0] else go(0, 0)
        ```

        1. ‏`pow` עם שלושה ארגומנטים מחשב בריבועים חוזרים, ומחזיר תשובה גם ל-\( n = 10^{18} \).
        2. החיפוש עובר על כל מסלול, ולכן הוא טוב רק ללוחות קטנים. הוא כאן כדי לבדוק את
           הנוסחאות, וכדי לספור כשמותר גם שמאלה ואין נוסחה.

    === "SystemVerilog"
        ```systemverilog title="function automatic longint unsigned pow_mod" linenums="1" hl_lines="7 8"
        // m^(n-1) mod p by squaring. With p below 2^31 every product is below 2^62.
        function automatic longint unsigned pow_mod(longint unsigned b, longint unsigned e,
                                                    longint unsigned p);
          longint unsigned r = 1 % p;
          b = b % p;
          while (e > 0) begin
            if (e[0]) r = r * b % p;                           // (1)!
            b = b * b % p;
            e = e >> 1;
          end
          return r;
        endfunction

        function automatic longint unsigned paths_rud_mod(longint unsigned m, longint unsigned n);
          return pow_mod(m, n - 1, 64'd1000000007);
        endfunction
        ```

        1. הביטים של המעריך מהנמוך לגבוה : \( b \) עובר על \( m, m^2, m^4, \dots \), וכל ביט
           1 כופל את התוצאה בחזקה שלו.

    #### למה זה נכון { .sol-proof }

    **ההתאמה.** ממסלול קוראים את שורות היציאה \( b_0, \dots, b_{n-2} \) של העמודות 0 עד
    \( n - 2 \). להפך, מכל רשימה כזו בונים מסלול : בעמודה 0 משורה 0 אל \( b_0 \), צעד ימינה,
    בעמודה 1 מ-\( b_0 \) אל \( b_1 \), וכן הלאה, ובעמודה האחרונה מ-\( b_{n-2} \) אל
    \( m - 1 \). המסלול חוקי : בכל עמודה הוא זז בכיוון אחד, ולכן לא חוזר לתא, ולעמודה שעזב
    הוא לא חוזר. ולפי השלב השני כל מסלול נראה כך, כלומר נקבע מהרשימה שלו. ההתאמה חד-חד-ערכית
    ועל, ויש \( m^{n-1} \) רשימות.

    **בלי "לא פעמיים".** אם מותר לחזור לתא, מסלול יכול לעלות ולרדת באותה עמודה כמה פעמים
    שירצה, ויש אינסוף מסלולים. זה דורש שתי שורות לפחות : בלוח של שורה אחת אין צעד למעלה או
    למטה, ויש בו מסלול אחד.

    **ושמאלה?** עם ארבעה כיוונים, בלי לחזור לתא, יש מספר סופי של מסלולים, אבל מסלול יכול לחזור
    לעמודה שכבר עזב, וההתאמה לשורות יציאה נשברת. לספירה הזו אין נוסחה ידועה. בטבלה היא נספרה
    בחיפוש מלא, והיא גדלה מהר יותר מכל השאר.

    #### סיבוכיות { .sol-cost }

    הנוסחה : חזקה אחת, \( O(\log n) \) כפלים במודולו וזיכרון \( O(1) \). המספר המדויק הוא בן
    \( (n - 1) \log_2 m \) ביטים בערך, ובלוח של 10 על 10 הוא כבר צריך 30 ביטים.

---

### סעיף ד – גם למעלה, עם מכשולים

אותו כלל של סעיף ג, ימינה, למעלה ולמטה בלי לחזור לתא, בלוח עם מכשולים. כמה מסלולים יש
בלוח של סעיף ב? ובלוח "זיגזג", שבו עמודה 1 פתוחה רק בשורה התחתונה ועמודה 3 רק בשורה
העליונה? כתבו פונקציה לכל לוח, ומודול חומרה שמקבל עמודה אחת של הלוח בכל מחזור שעון.

??? tip "רמז 1"
    מה מהטיעון של סעיף ג נשאר נכון כשיש מכשולים? המסלול עדיין עובר בעמודות לפי הסדר.

??? tip "רמז 2"
    מכשולים מחלקים עמודה לקטעים רציפים של תאים פנויים. מאיזו שורה של העמודה אפשר להגיע
    לאיזו?

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        **‏32, ובזיגזג 9.** המסלול עדיין עובר בעמודות לפי הסדר, ובכל עמודה הוא קטע אנכי, אבל
        רק בתוך קטע רציף של תאים פנויים. לכן עוברים עמודה אחרי עמודה : מספר המסלולים שנגמרים
        בתא הוא סכום המסלולים שנכנסו לעמודה בכל השורות של הקטע שלו. בזיגזג אין אף מסלול
        ימינה ולמטה, כי צריך לעלות בעמודה 2 משורה 2 לשורה 0.

    <!-- cost: זמן \( O(mn) \) | זיכרון \( O(m) \) -->

    #### הרעיון { .sol-idea }

    עכשיו סופרים לפי עמודות ולא לפי תאים. בכל עמודה, מכל שורה שנכנסים בה אפשר להגיע בדרך
    אחת לכל תא של אותו קטע פנוי, ולשום תא אחר. בלוח של סעיף ב :

    <!-- gen 7 -->

    <svg class="figure gx-fig lp-fig" viewBox="0 0 268 130" style="max-width:16.75rem" role="img" aria-label="אותו לוח של סעיף ב כשמותר גם למעלה : בכל תא פנוי מספר המסלולים מ-S שנגמרים בו, ובתא T יש 32"><text class="tick" x="41" y="14" text-anchor="middle">0</text><text class="tick" x="75" y="14" text-anchor="middle">1</text><text class="tick" x="109" y="14" text-anchor="middle">2</text><text class="tick" x="143" y="14" text-anchor="middle">3</text><text class="tick" x="177" y="14" text-anchor="middle">4</text><text class="tick" x="211" y="14" text-anchor="middle">5</text><text class="tick" x="245" y="14" text-anchor="middle">6</text><text class="tick" x="17" y="43" text-anchor="end">0</text><text class="tick" x="17" y="77" text-anchor="end">1</text><text class="tick" x="17" y="111" text-anchor="end">2</text><g class="gx-cell is-open lp-h1"><title>cell (0, 0): 1 path ends here</title><rect x="25.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 1): 1 path ends here</title><rect x="59.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 2): 2 paths end here</title><rect x="93.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (0, 3): 4 paths end here</title><rect x="127.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h3"><title>cell (0, 4): 8 paths end here</title><rect x="161.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (0, 5): an obstacle</title><rect x="195.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (0, 6): 32 paths end here</title><rect x="229.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (1, 0): 1 path ends here</title><rect x="25.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 1): an obstacle</title><rect x="59.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (1, 2): 2 paths end here</title><rect x="93.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (1, 3): 4 paths end here</title><rect x="127.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h3"><title>cell (1, 4): 8 paths end here</title><rect x="161.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (1, 5): 16 paths end here</title><rect x="195.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (1, 6): 32 paths end here</title><rect x="229.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (2, 0): 1 path ends here</title><rect x="25.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (2, 1): 1 path ends here</title><rect x="59.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (2, 2): 2 paths end here</title><rect x="93.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 3): an obstacle</title><rect x="127.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h3"><title>cell (2, 4): 8 paths end here</title><rect x="161.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (2, 5): 16 paths end here</title><rect x="195.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (2, 6): 32 paths end here</title><rect x="229.5" y="91.5" width="31" height="31" rx="3"/></g><text class="gx-val" x="41" y="47" text-anchor="middle">1</text><text class="gx-tag" x="28" y="34">S</text><text class="gx-val" x="75" y="44" text-anchor="middle">1</text><text class="gx-val" x="109" y="44" text-anchor="middle">2</text><text class="gx-val" x="143" y="44" text-anchor="middle">4</text><text class="gx-val" x="177" y="44" text-anchor="middle">8</text><text class="gx-val" x="245" y="44" text-anchor="middle">32</text><text class="gx-val" x="41" y="78" text-anchor="middle">1</text><text class="gx-val" x="109" y="78" text-anchor="middle">2</text><text class="gx-val" x="143" y="78" text-anchor="middle">4</text><text class="gx-val" x="177" y="78" text-anchor="middle">8</text><text class="gx-val" x="211" y="78" text-anchor="middle">16</text><text class="gx-val" x="245" y="78" text-anchor="middle">32</text><text class="gx-val" x="41" y="112" text-anchor="middle">1</text><text class="gx-val" x="75" y="112" text-anchor="middle">1</text><text class="gx-val" x="109" y="112" text-anchor="middle">2</text><text class="gx-val" x="177" y="112" text-anchor="middle">8</text><text class="gx-val" x="211" y="112" text-anchor="middle">16</text><text class="gx-val" x="245" y="115" text-anchor="middle">32</text><text class="gx-tag" x="232" y="102">T</text></svg>

    <!-- /gen -->

    בזיגזג אין מסלול ימינה ולמטה בכלל. עם צעד למעלה המסלול חייב לרדת בעמודה 0, לעבור למטה
    בעמודה 1, לעלות בעמודה 2 ולעבור למעלה בעמודה 3. בעמודות 4 ו-5 הוא בוחר שוב שורת
    יציאה :

    <!-- gen 8 -->

    <svg class="figure gx-fig lp-fig" viewBox="0 0 268 130" style="max-width:16.75rem" role="img" aria-label="לוח הזיגזג : עמודה 1 פתוחה רק למטה ועמודה 3 רק למעלה. בצעדים ימינה ולמטה אין אף מסלול, וכשמותר גם למעלה יש 9. בכל תא מספר המסלולים שנגמרים בו, ומסלול אחד מסומן"><text class="tick" x="41" y="14" text-anchor="middle">0</text><text class="tick" x="75" y="14" text-anchor="middle">1</text><text class="tick" x="109" y="14" text-anchor="middle">2</text><text class="tick" x="143" y="14" text-anchor="middle">3</text><text class="tick" x="177" y="14" text-anchor="middle">4</text><text class="tick" x="211" y="14" text-anchor="middle">5</text><text class="tick" x="245" y="14" text-anchor="middle">6</text><text class="tick" x="17" y="43" text-anchor="end">0</text><text class="tick" x="17" y="77" text-anchor="end">1</text><text class="tick" x="17" y="111" text-anchor="end">2</text><g class="gx-cell is-open lp-h1"><title>cell (0, 0): 1 path ends here</title><rect x="25.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (0, 1): an obstacle</title><rect x="59.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 2): 1 path ends here</title><rect x="93.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 3): 1 path ends here</title><rect x="127.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (0, 4): 1 path ends here</title><rect x="161.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (0, 5): 3 paths end here</title><rect x="195.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (0, 6): 9 paths end here</title><rect x="229.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (1, 0): 1 path ends here</title><rect x="25.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 1): an obstacle</title><rect x="59.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (1, 2): 1 path ends here</title><rect x="93.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 3): an obstacle</title><rect x="127.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (1, 4): 1 path ends here</title><rect x="161.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (1, 5): 3 paths end here</title><rect x="195.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (1, 6): 9 paths end here</title><rect x="229.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (2, 0): 1 path ends here</title><rect x="25.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (2, 1): 1 path ends here</title><rect x="59.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (2, 2): 1 path ends here</title><rect x="93.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 3): an obstacle</title><rect x="127.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h1"><title>cell (2, 4): 1 path ends here</title><rect x="161.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h2"><title>cell (2, 5): 3 paths end here</title><rect x="195.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open lp-h4"><title>cell (2, 6): 9 paths end here</title><rect x="229.5" y="91.5" width="31" height="31" rx="3"/></g><polyline class="gx-path" points="41,39 41,73 41,107 75,107 109,107 109,73 109,39 143,39 177,39 211,39 245,39 245,73 245,107"><title>a path: ↓↓→→↑↑→→→→↓↓</title></polyline><text class="gx-val" x="41" y="47" text-anchor="middle">1</text><text class="gx-tag" x="28" y="34">S</text><text class="gx-val" x="109" y="44" text-anchor="middle">1</text><text class="gx-val" x="143" y="44" text-anchor="middle">1</text><text class="gx-val" x="177" y="44" text-anchor="middle">1</text><text class="gx-val" x="211" y="44" text-anchor="middle">3</text><text class="gx-val" x="245" y="44" text-anchor="middle">9</text><text class="gx-val" x="41" y="78" text-anchor="middle">1</text><text class="gx-val" x="109" y="78" text-anchor="middle">1</text><text class="gx-val" x="177" y="78" text-anchor="middle">1</text><text class="gx-val" x="211" y="78" text-anchor="middle">3</text><text class="gx-val" x="245" y="78" text-anchor="middle">9</text><text class="gx-val" x="41" y="112" text-anchor="middle">1</text><text class="gx-val" x="75" y="112" text-anchor="middle">1</text><text class="gx-val" x="109" y="112" text-anchor="middle">1</text><text class="gx-val" x="177" y="112" text-anchor="middle">1</text><text class="gx-val" x="211" y="112" text-anchor="middle">3</text><text class="gx-val" x="245" y="115" text-anchor="middle">9</text><text class="gx-tag" x="232" y="102">T</text></svg>

    <!-- /gen -->

    <!-- gen 9 -->

    <span class="viz-legend"><span><i class="gx-key-s"></i>S ההתחלה, T היעד</span><span><i class="lp-key-lo"></i>מעט מסלולים</span><span><i class="lp-key-hi"></i>הרבה מסלולים</span><span><i class="gx-key is-wall"></i>מכשול</span><span><i class="gx-key-path"></i>מסלול אחד</span></span>

    <!-- /gen -->

    עמודה אחרי עמודה, בווקטורים לפי השורות 0, 1 ו-2 מלמעלה למטה, ו-# הוא מכשול. זו גם
    הטבלה של `paths_cols`, עמודה בכל שעון : ב-`block` הביט \( r \) הוא שורה \( r \), האוגר
    `out` מקבל את המסלולים שנגמרים בכל תא של העמודה (0 במכשול), ו-`count` הוא התא התחתון :

    <!-- gen 10 -->

    | עמודה | ‏`block` | נכנסים בכל שורה | המסלולים שנגמרים בכל תא | ‏`count` | למה |
    |:-:|:-:|:-:|:-:|:-:|---|
    | 0 | ‏`3'b000` | ‏<span dir="ltr">[1, 0, 0]</span> | ‏<span dir="ltr">[1, 1, 1]</span> | 1 | ההתחלה בשורה 0, וכל העמודה קטע אחד |
    | 1 | ‏`3'b011` | ‏<span dir="ltr">[#, #, 1]</span> | ‏<span dir="ltr">[#, #, 1]</span> | 1 | רק שורה 2 פנויה |
    | 2 | ‏`3'b000` | ‏<span dir="ltr">[0, 0, 1]</span> | ‏<span dir="ltr">[1, 1, 1]</span> | 1 | קטע אחד : כל תא מקבל 1, גם שורה 0 |
    | 3 | ‏`3'b110` | ‏<span dir="ltr">[1, #, #]</span> | ‏<span dir="ltr">[1, #, #]</span> | 0 | רק שורה 0 פנויה |
    | 4 | ‏`3'b000` | ‏<span dir="ltr">[1, 0, 0]</span> | ‏<span dir="ltr">[1, 1, 1]</span> | 1 | קטע אחד : <span dir="ltr">1 + 0 + 0</span> |
    | 5 | ‏`3'b000` | ‏<span dir="ltr">[1, 1, 1]</span> | ‏<span dir="ltr">[3, 3, 3]</span> | 3 | קטע אחד : <span dir="ltr">1 + 1 + 1</span> |
    | 6 | ‏`3'b000` | ‏<span dir="ltr">[3, 3, 3]</span> | ‏<span dir="ltr">[9, 9, 9]</span> | 9 | קטע אחד : <span dir="ltr">3 + 3 + 3</span> |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **כניסה :** לעמודה \( c \) נכנסים בשורה \( r \) מהתא \( (r, c - 1) \), ולעמודה 0 רק
       בשורה 0, ההתחלה. לתא חסום לא נכנסים.
    2. **קטעים :** מחלקים את העמודה לקטעים רציפים של תאים פנויים.
    3. **סכום לקטע :** לכל קטע מחברים את הכניסות שלו. זה המספר של כל תא בקטע, כי מכל שורת
       כניסה יש דרך אנכית אחת לכל אחד מהם.
    4. **הלאה :** המספרים של העמודה הם הכניסות של העמודה הבאה.
    5. **התשובה :** המספר בתא הימני התחתון.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="paths_rud_blocked" linenums="1" hl_lines="8 18"
        def paths_rud_blocked(grid, p=None):
            """Right, up and down with obstacles, never a cell twice, a column at a time: a path
            enters a column at some row, walks up or down inside its run of free cells, and
            leaves it at another row."""
            m, n = len(grid), len(grid[0])
            out = [1] + [0] * (m - 1)                            # (1)!
            for c in range(n):
                enter = [0 if grid[r][c] else out[r] for r in range(m)]
                out = [0] * m
                r = 0
                while r < m:
                    if grid[r][c]:
                        r += 1
                        continue
                    s = r
                    while r < m and not grid[r][c]:
                        r += 1
                    total = sum(enter[s:r])                      # (2)!
                    if p:
                        total %= p
                    out[s:r] = [total] * (r - s)
            return out[m - 1]
        ```

        1. העמודה "שמשמאל" ללוח : מסלול אחד שנכנס לעמודה 0 בשורה 0, ההתחלה.
        2. הקטע הוא השורות \( s \) עד \( r - 1 \). כל מסלול שנכנס באחת מהן יכול להיגמר בכל
           אחת מהן, בדרך אחת.

    === "SystemVerilog"
        ```systemverilog title="module paths_cols" linenums="1" hl_lines="23 26"
        // Right, up and down with obstacles, never a cell twice, one column of the board a clock.
        // P = 0: the exact count in W bits; P > 0: the count mod P.
        module paths_cols #(parameter int M = 3, W = 64, parameter longint unsigned P = 0) (
          input  logic         clk, rst_n,
          input  logic         valid,          // block holds a column this clock
          input  logic         first,          // the column is the board's first
          input  logic [M-1:0] block,          // bit r: the cell in row r is an obstacle
          output logic [W-1:0] count);         // the paths to the bottom cell of the last column

          logic [W-1:0] out [M];               // the paths that end at each cell of the last column
          logic [W-1:0] down [M];              // what entered the run at this row or above it
          logic [W-1:0] run [M];               // what entered the whole run of this row

          function automatic logic [W-1:0] add(logic [W-1:0] a, logic [W-1:0] b);
            logic [W:0] s = {1'b0, a} + {1'b0, b};
            if (P != 0 && s >= (W+1)'(P)) s -= (W+1)'(P);
            return s[W-1:0];
          endfunction

          always_comb begin
            down[0] = block[0] ? '0 : first ? W'(1) : out[0];
            for (int r = 1; r < M; r++)
              down[r] = block[r] ? '0 : add(down[r - 1], first ? '0 : out[r]);   // (1)!
            run[M-1] = down[M-1];
            for (int r = M - 2; r >= 0; r--)
              run[r] = block[r] ? '0 : block[r + 1] ? down[r] : run[r + 1];     // (2)!
          end

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) out <= '{default: '0};
            else if (valid) out <= run;

          assign count = out[M-1];
        endmodule
        ```

        1. שרשרת מלמעלה למטה : סכום הכניסות של הקטע עד השורה הזו. מכשול מאפס אותה, וכך הקטע
           הבא מתחיל מ-0.
        2. שרשרת מלמטה למעלה : התא התחתון של קטע מחזיק את הסכום של כל הקטע, וכל תא מעליו
           באותו קטע מעתיק אותו.

    #### למה זה נכון { .sol-proof }

    **קטע אחד.** כמו בסעיף ג, המסלול עובר בעמודות לפי הסדר, ובכל עמודה הוא קטע אנכי אחד. הקטע
    הזה לא עובר במכשול, ולכן שורת הכניסה ושורת היציאה באותו קטע של תאים פנויים. להפך, בין כל
    שתי שורות באותו קטע יש דרך אנכית אחת בדיוק.

    **הספירה.** נסמן ב-\( f(r, c) \) את מספר המסלולים מ-S שנגמרים בתא הפנוי \( (r, c) \). מסלול
    כזה נכנס לעמודה \( c \) בשורה \( a \) של אותו קטע, ולפני כן הוא מסלול שנגמר בתא
    \( (a, c - 1) \). לכן \( f(r, c) = \sum_a f(a, c - 1) \), על השורות \( a \) של הקטע שבהן
    התא \( (a, c) \) פנוי, ואין ספירה כפולה, כי לכל מסלול שורת כניסה אחת. הסכום זהה לכל התאים
    של הקטע. בלוח ריק כל עמודה היא קטע אחד, וכל עמודה כופלת ב-\( m \) : זו הנוסחה של סעיף ג.

    **החומרה.** ‏`down[r]` הוא סכום הכניסות מתחילת הקטע ועד השורה \( r \), ו-`run[r]` הוא
    `down` של התא התחתון בקטע, כלומר הסכום של כל הקטע. אלה בדיוק \( f \) של העמודה, והם
    נכנסים ל-`out` לעמודה הבאה.

    **נסו בעצמכם.** הקופסה פותחת את לוח הזיגזג, עם צעד למעלה. פתחו את \( (1, 3) \) : עמודה 3
    הופכת לקטע אחד של שני תאים, ו-T עולה מ-9 ל-36. בלוח של העמוד, חסמו את \( (1, 5) \) :
    עמודה 5 מתפצלת לשני קטעים של תא אחד, כל קטע מעביר רק את מה שנכנס אליו, ו-T יורד מ-9
    ל-2. החליפו ל"ימינה ולמטה" : אין אף מסלול. "שעון אחד" ממלא את הלוח עמודה אחרי עמודה,
    כמו `paths_cols` בטבלה למעלה :

    <div class="explorer" data-kind="latpaths" data-dirs="rud" data-grid="0100000.0101000.0001000"></div>

    #### סיבוכיות { .sol-cost }

    כל תא נקרא פעמיים, בכניסה ובסכום של הקטע : זמן \( O(mn) \), וזיכרון של עמודה אחת,
    \( O(m) \). בחומרה \( n \) שעונים, עם שתי שרשראות של \( m \) תאים בכל שעון.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : הנוסחה כשיש מכשולים"
    ‏\( \binom{m+n-2}{m-1} \) סופרת את כל הסדרים של הצעדים, גם את אלה שעוברים במכשול, ולכן עם
    מכשולים היא רק חסם עליון. צריך את הטבלה, או לחסר את המסלולים שעוברים במכשולים בהכלה
    והדחה, כמו בשאלת ההמשך הראשונה.

??? trap "מלכודת : כפל לפני חילוק ב-64 ביטים"
    הנוסחה בלולאה, \( r \leftarrow r \cdot (\text{top} - k + i) / i \), נותנת בכל צעד מספר
    שלם, אבל המכפלה גולשת לפני החילוק. בלוח של 33 על 33 התשובה, בערך \( 1.8 \cdot 10^{18} \),
    נכנסת ב-64 ביטים, והלולאה כבר נותנת תשובה שגויה, וכך גם ב-34 על 34. הטבלה של סעיף א רק
    מחברת, ואף מספר בה לא גדול מהתשובה.

??? trap "מלכודת : זיכרון לפי תא כשיש צעד למעלה"
    בסעיפים א ו-ב אפשר לכתוב רקורסיה עם זיכרון : \( f(r, c) = f(r, c-1) + f(r-1, c) \). עם צעד
    למעלה הניסיון הטבעי, \( f(r, c) = f(r, c-1) + f(r-1, c) + f(r+1, c) \), מעגלי : התא תלוי
    בשכן מתחתיו, שתלוי בו. ובאמת, מה שמותר אחרי תא תלוי באילו תאים כבר עברו. לכן סופרים
    לפי עמודה ולפי קטע, ולא לפי תא.

??? trap "מלכודת : לספור בחיפוש מלא"
    ‏`count_walks` עוברת על כל מסלול. בלוח של 10 על 10 עם צעד למעלה יש \( 10^9 \) מסלולים,
    ובלוח של 16 על 16 יותר מ-\( 10^{18} \). חיפוש מלא טוב רק לבדיקה של לוחות קטנים.

??? followup "שאלות המשך"
    - **לוח ענק עם מעט מכשולים :** לוח של \( 10^5 \) על \( 10^5 \), ימינה ולמטה, עם 20
      מכשולים. הטבלה גדולה מדי. איך סופרים?

        ??? fu-answer "תשובה"
            הכלה והדחה. ממיינים את המכשולים לפי \( r + c \), ולכל מכשול \( i \) סופרים את
            המסלולים שמגיעים אליו בלי לעבור במכשול קודם : כל המסלולים אליו, פחות
            \( g_j \cdot \binom{\Delta r + \Delta c}{\Delta r} \) לכל מכשול \( j \) שלמעלה
            ומשמאל לו, כש-\( \Delta r \) ו-\( \Delta c \) הם ההפרשים ביניהם. באותה דרך סופרים
            את T. אלה \( O(k^2) \) מקדמים בינומיים, עם עצרות מודולו \( p \) שמחושבות מראש.

    - **התחלה ויעד בכל מקום :** עם צעד למעלה, מהתא \( (r_0, c_0) \) לתא \( (r_1, c_1) \)
      כש-\( c_1 > c_0 \), בלוח ריק. כמה מסלולים יש?

        ??? fu-answer "תשובה"
            ‏\( m^{c_1 - c_0} \), בלי קשר לשורות : שורת יציאה בכל עמודה מ-\( c_0 \) עד
            \( c_1 - 1 \), ובעמודה \( c_1 \) הולכים ליעד. המסלול לא יוצא מהעמודות שבין
            השתיים, כי אין צעד שמאלה.

    - **מסלול אקראי :** איך מגרילים מסלול, כך שלכל המסלולים יש אותו סיכוי?

        ??? fu-answer "תשובה"
            מהסוף להתחלה, עם הטבלה : מהתא \( (r, c) \) חוזרים לתא משמאל בהסתברות
            \( f(r, c-1) / f(r, c) \), ולמעלה בשאר. ההסתברות של מסלול היא מכפלה שמצטמצמת
            ל-\( 1 / f(m-1, n-1) \). עם צעד למעלה הולכים מהסוף עמודה אחרי עמודה : בעמודה
            שבה המסלול נגמר בשורה \( r \) בוחרים את שורת הכניסה \( a \) מהקטע של \( r \),
            בהסתברות של הכניסה בשורה \( a \) מתוך סכום הכניסות של הקטע, ועוברים בעמודה מ-\( a \)
            ל-\( r \). כך עושה הכפתור "מסלול אקראי" בקופסה, בשני סוגי הצעדים.

    - **אימות של `paths_rows` :** מה בודקים במודול, ואילו מקרי קצה הבדיקה האקראית חייבת לפגוש?

        ??? fu-answer "תשובה"
            מודל ייחוס, הטבלה של Python, ב-scoreboard שמשווה את `count` אחרי כל שורה, על
            לוחות אקראיים ועל הלוחות של העמוד. ליד המודול, טענות שתמיד נכונות ונקודות כיסוי
            למקרי הקצה :

            ```systemverilog title="module paths_rows_check" linenums="1"
            // Bound next to paths_rows: what always holds, and the corners a random test must reach.
            module paths_rows_check #(parameter int N = 7, W = 64) (
              input logic         clk, rst_n, valid, first,
              input logic [N-1:0] block,
              input logic [W-1:0] count);
              // no row this clock: the count holds
              a_hold: assert property (@(posedge clk) disable iff (!rst_n) !valid |=> $stable(count));
              // a fully blocked row ends every path
              a_wall: assert property (@(posedge clk) disable iff (!rst_n) valid && &block |=> count == '0);
              c_s_blocked: cover property (@(posedge clk) valid && first && block[0]);
              c_t_blocked: cover property (@(posedge clk) valid && block[N-1]);
              c_wall:      cover property (@(posedge clk) valid && &block);
            endmodule
            ```

            ועם \( P > 0 \) גם נקודת כיסוי בתוך `add`, לסכום שעובר את \( P \) ומחסרים ממנו.

    - **גם שמאלה :** כמה מסלולים יש עם ארבעה כיוונים, בלי לחזור לתא?

        ??? fu-answer "תשובה"
            אין נוסחה ידועה. בלוחות ריבועיים של 1 עד 5 יש 1, 2, 12, 184 ו-8,512. סופרים
            בחיפוש עם חזרה לאחור, או בשיטות שעוברות עמודה אחרי עמודה עם כל הדרכים שבהן
            המסלול חוצה אותה, וזה גדל מהר מאוד.
