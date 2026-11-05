---
id: 84
title: תת-הסדרה העולה הארוכה ביותר – DP, מערך tails וספירת כל ה-LIS
level: junior
difficulty: medium
kind: code
tags: [algorithms, dynamic-programming, binary-search, python, systemverilog]
source: "שאלת ראיון קלאסית; מערך tails הוא הצורה הקצרה של patience sorting"
added: 2026-11-05
---

## השאלה

נתון מערך של מספרים שלמים `a`. **תת-סדרה** מתקבלת ממנו כשמוחקים חלק מהאיברים ומשאירים את
השאר בסדר המקורי שלהם, ו**עולה** פירושו עולה ממש : כל איבר גדול מהקודם לו. מחפשים את האורך של
תת-הסדרה העולה הארוכה ביותר (Longest Increasing Subsequence, ‏LIS), ואת הסדרה עצמה.

למשל ב-`a = [10, 9, 2, 5, 3, 7, 101, 18]` האורך הוא 4, ו-`[2, 5, 7, 101]` היא אחת מתתי-הסדרות
האלה. האיברים לא חייבים להיות צמודים זה לזה.

??? interviewer "מה המראיין בודק"
    - **ניסוח מצב של DP :** הבחירה הנכונה היא "הסדרה הארוכה ביותר **שנגמרת** ב-`a[i]`". מצב כמו
      "הסדרה הארוכה ביותר בתחילית" לא מתקדם, כי הוא לא זוכר במה הסדרה נגמרת.
    - **שיפור מ-\( O(n^2) \) ל-\( O(n \log n) \) :** האם המועמד מכיר את מערך tails, ויודע להסביר
      למה הוא ממוין ולמה מותר לחפש בו חיפוש בינארי, ולא רק לשנן את הקוד.
    - **התשובה עצמה ולא רק האורך :** שחזור הסדרה עם מצביעים אחורה, והבנה ש-tails עצמו אינו
      תת-סדרה.
    - **עולה ממש מול לא יורדת :** ההבדל בין `bisect_left` ל-`bisect_right`, ומה קורה עם ערכים
      שווים.
    - **ספירה :** הרחבת ה-DP לזוג של אורך ומספר דרכים, בלי לספור פעמיים.

---

### סעיף א – DP בזמן ריבועי

כתבו פונקציה שמחזירה את האורך של ה-LIS ב-\( O(n^2) \), ושחזרו ממנה את תת-הסדרה עצמה. מה טבלת
ה-DP של הדוגמה?

??? tip "רמז 1"
    כל תת-סדרה עולה נגמרת באיבר כלשהו. מה האורך הגדול ביותר של תת-סדרה עולה שנגמרת **בדיוק**
    ב-`a[i]`?

??? tip "רמז 2"
    תת-סדרה כזו היא איבר יחיד, או תת-סדרה שנגמרת ב-`a[j]` עם \( j < i \) ו-`a[j] < a[i]`, ואחריה
    `a[i]`.

??? tip "רמז 3"
    כדי לשחזר את הסדרה, זכרו לכל \( i \) את ה-\( j \) שנתן לו את האורך שלו.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏`dp[i]` הוא האורך של תת-הסדרה העולה הארוכה ביותר שנגמרת ב-`a[i]` :
        ‏\( dp[i] = 1 + \max \{ dp[j] : j < i,\ a[j] < a[i] \} \), או 1 אם אין \( j \) כזה. התשובה
        היא המקסימום של `dp`, ולא `dp[n - 1]`. בדוגמה `dp = [1, 1, 1, 2, 2, 3, 4, 4]`, האורך 4,
        והשחזור לאחור מ-101 נותן `[2, 5, 7, 101]`.

    <!-- cost: זמן \( O(n^2) \), ‏28 השוואות ל-8 איברים | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    מסתכלים על האיבר האחרון של תת-הסדרה. אם היא נגמרת ב-`a[i]`, מה שלפניו הוא תת-סדרה עולה
    שנגמרת באיבר קטן יותר ומוקדם יותר, וכדאי לקחת את הארוכה מביניהן. מתחת לכל איבר כתוב
    `dp[i]`, וקשת מחברת אותו לאיבר `prev[i]` שלפניו בסדרה הארוכה שנגמרת בו :

    <!-- gen 0 -->

    <svg class="figure lis-fig" viewBox="0 0 384 136" style="max-width:24.0rem" role="img" aria-label="סעיף א : המערך 10 9 2 5 3 7 101 18. מתחת לכל איבר dp, האורך של תת-הסדרה העולה הארוכה ביותר שנגמרת בו : 1 1 1 2 2 3 4 4. קשת מכל איבר לאיבר prev שלפניו. האורך 4, והסדרה 2 5 7 101 מודגשת"><path class="lis-link" d="M148,50 Q190,14 232,50"/><path class="lis-link" d="M274,50 Q316,14 358,50"/><path class="lis-link is-chain" d="M148,50 Q169,26 190,50"/><path class="lis-link is-chain" d="M190,50 Q232,14 274,50"/><path class="lis-link is-chain" d="M274,50 Q295,26 316,50"/><text class="lis-idx" x="64" y="14" text-anchor="middle">0</text><rect class="st-cell" x="46" y="52" width="36" height="36" rx="3"/><text class="st-text" x="64" y="75" text-anchor="middle">10</text><text class="lis-idx" x="106" y="14" text-anchor="middle">1</text><rect class="st-cell" x="88" y="52" width="36" height="36" rx="3"/><text class="st-text" x="106" y="75" text-anchor="middle">9</text><text class="lis-idx" x="148" y="14" text-anchor="middle">2</text><rect class="fig-one" x="130" y="52" width="36" height="36" rx="3"/><text class="st-text" x="148" y="75" text-anchor="middle">2</text><text class="lis-idx" x="190" y="14" text-anchor="middle">3</text><rect class="fig-one" x="172" y="52" width="36" height="36" rx="3"/><text class="st-text" x="190" y="75" text-anchor="middle">5</text><text class="lis-idx" x="232" y="14" text-anchor="middle">4</text><rect class="st-cell" x="214" y="52" width="36" height="36" rx="3"/><text class="st-text" x="232" y="75" text-anchor="middle">3</text><text class="lis-idx" x="274" y="14" text-anchor="middle">5</text><rect class="fig-one" x="256" y="52" width="36" height="36" rx="3"/><text class="st-text" x="274" y="75" text-anchor="middle">7</text><text class="lis-idx" x="316" y="14" text-anchor="middle">6</text><rect class="fig-one" x="298" y="52" width="36" height="36" rx="3"/><text class="st-text" x="316" y="75" text-anchor="middle">101</text><text class="lis-idx" x="358" y="14" text-anchor="middle">7</text><rect class="st-cell" x="340" y="52" width="36" height="36" rx="3"/><text class="st-text" x="358" y="75" text-anchor="middle">18</text><text class="lis-lab" x="36" y="75" text-anchor="end">a</text><text class="lis-lab" x="36" y="120" text-anchor="end">dp</text><rect class="lis-val" x="46" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="64" y="119" text-anchor="middle">1</text><rect class="lis-val" x="88" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="106" y="119" text-anchor="middle">1</text><rect class="lis-val is-lit" x="130" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="148" y="119" text-anchor="middle">1</text><rect class="lis-val is-lit" x="172" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="190" y="119" text-anchor="middle">2</text><rect class="lis-val" x="214" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="232" y="119" text-anchor="middle">2</text><rect class="lis-val is-lit" x="256" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="274" y="119" text-anchor="middle">3</text><rect class="lis-val is-lit" x="298" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="316" y="119" text-anchor="middle">4</text><rect class="lis-val" x="340" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="358" y="119" text-anchor="middle">4</text></svg>

    <span class="viz-legend"><span><i class="fc-key-sorted"></i>תת-סדרה עולה ארוכה ביותר</span><span><i class="lis-key-chain"></i>הקשת מ-<code>prev[i]</code> ל-<code>i</code> שלה</span><span><i class="lis-key-link"></i>קשת <code>prev</code> של איבר אחר</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **התחלה :** `dp[i] = 1` ו-`prev[i] = -1` לכל \( i \) : כל איבר לבדו הוא תת-סדרה עולה.

    2. **מעבר על הקודמים :** לכל \( i \), לכל \( j < i \) עם `a[j] < a[i]`, אפשר להוסיף את `a[i]`
       אחרי הסדרה שנגמרת ב-`a[j]`. אם `dp[j] + 1 > dp[i]`, מעדכנים `dp[i] = dp[j] + 1` ו-`prev[i] = j`.

    3. **האורך :** המקסימום של `dp`. הסדרה הארוכה לא חייבת להיגמר באיבר האחרון : בדוגמה
       `[3, 4, 1]` האיבר האחרון נותן `dp = 1`, והתשובה 2.

    4. **השחזור :** מתחילים באינדקס שבו `dp` מקסימלי, הולכים לאחור לפי `prev` עד \( -1 \), והופכים
       את הסדר.

    </div>

    בתיבה כל צעד הוא השוואה אחת של `a[j]` עם `a[i]`. מתחת למערך שורת `len`, שהיא `dp`, ושורת
    `cnt` של סעיף ג :

    <div class="explorer" data-kind="lis" data-mode="dp" data-nums="10 9 2 5 3 7 101 18"></div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="lis_dp" linenums="1" hl_lines="7 8"
        def lis_dp(a: list[int]) -> tuple[int, list[int], list[int]]:
            """Part a: dp[i] is the length of the longest increasing subsequence that ends at a[i],
            prev[i] the index before a[i] on it (-1 at its start). Returns (the length, dp, prev)."""
            dp, prev = [1] * len(a), [-1] * len(a)
            for i in range(len(a)):
                for j in range(i):
                    if a[j] < a[i] and dp[j] + 1 > dp[i]:   # (1)!
                        dp[i], prev[i] = dp[j] + 1, j
            return max(dp, default=0), dp, prev             # (2)!


        def lis_from_dp(a: list[int], dp: list[int], prev: list[int]) -> list[int]:
            """One LIS itself: from an index with the largest dp, back along prev."""
            out, i = [], dp.index(max(dp)) if dp else -1   # (3)!
            while i >= 0:
                out.append(a[i])
                i = prev[i]
            return out[::-1]
        ```

        1. ‏`a[j] < a[i]` : עולה ממש. ‏`>` ולא `>=` : כשיש כמה \( j \) עם אותו אורך, נשאר הראשון.
        2. המקסימום על כל המערך, לא `dp[-1]`.
        3. ‏`dp.index` מחזיר את האינדקס הראשון עם האורך המקסימלי.

    === "SystemVerilog"
        ```systemverilog title="function lis_dp" linenums="1" hl_lines="9"
        // Part a: dp[i] and prev[i] as in the Python; returns the length of the LIS.
        function automatic int lis_dp(int a[$], ref int dp[$], ref int prev[$]);
          int best = 0;
          dp.delete();
          prev.delete();
          foreach (a[i]) begin
            dp.push_back(1);
            prev.push_back(-1);
            for (int j = 0; j < i; j++)
              if (a[j] < a[i] && dp[j] + 1 > dp[i]) begin   // (1)!
                dp[i] = dp[j] + 1;
                prev[i] = j;
              end
            if (dp[i] > best) best = dp[i];                  // (2)!
          end
          return best;
        endfunction

        // One LIS itself, from the first index with the largest dp back along prev.
        function automatic void lis_from_dp(int a[$], int dp[$], int prev[$], ref int out[$]);
          int best = 0, i = -1;
          foreach (dp[k]) if (dp[k] > best) begin best = dp[k]; i = k; end
          out.delete();
          while (i >= 0) begin
            out.push_front(a[i]);
            i = prev[i];
          end
        endfunction
        ```

        1. אותו תנאי כמו ב-Python : עולה ממש, ועדכון רק כשהאורך גדל.
        2. המקסימום נאסף תוך כדי, כי `dp[i]` כבר סופי כשהלולאה הפנימית נגמרת.

    #### למה זה נכון { .sol-proof }

    **הנוסחה.** תת-סדרה עולה שנגמרת ב-`a[i]` היא `a[i]` לבדו, או תת-סדרה עולה שנגמרת באיבר
    `a[j]` עם \( j < i \) ו-`a[j] < a[i]`, ואחריה `a[i]`. במקרה השני האורך הוא אחד יותר מהאורך של
    החלק שלפני `a[i]`, והחלק הזה ארוך לכל היותר `dp[j]`. לכן `dp[i]` הוא בדיוק 1 ועוד המקסימום של
    `dp[j]` על ה-\( j \)-ים המתאימים. הלולאה מחשבת את `dp` לפי סדר האינדקסים, ולכן כש-`a[i]` מחושב,
    כל `dp[j]` עם \( j < i \) כבר סופי.

    **השחזור.** `prev[i]` הוא ה-\( j \) שנתן את `dp[i]`, כך ש-`dp[prev[i]] = dp[i] - 1`. ההליכה
    לאחור יורדת באורך באחד בכל צעד, ובכל צעד הערך קטן יותר, ולכן היא עוברת על `dp[i]` איברים
    שיוצרים תת-סדרה עולה.

    #### סיבוכיות { .sol-cost }

    זמן \( O(n^2) \) : הלולאה הפנימית עושה \( 0 + 1 + \dots + (n - 1) = n(n - 1)/2 \) השוואות, ‏28
    ל-8 איברים. זיכרון \( O(n) \) לשני המערכים.

---

### סעיף ב – ‏n log n עם מערך tails { #tails }

שפרו את הזמן ל-\( O(n \log n) \). החזירו גם כאן תת-סדרה עולה ארוכה ביותר, לא רק את האורך.

??? tip "רמז 1"
    לכל אורך \( L \), זכרו רק את הערך הקטן ביותר שבו יכולה להיגמר תת-סדרה עולה באורך \( L \). למה
    הקטן ביותר?

??? tip "רמז 2"
    המערך הזה, `tails`, ממוין. כשמגיע איבר חדש \( x \), איזה תא שלו משתנה, ואיך מוצאים אותו?

??? tip "רמז 3"
    ‏`tails` עצמו אינו תת-סדרה. כדי לשחזר, זכרו לכל איבר את האיבר שלפניו : האיבר שגמר את האורך
    הקצר ממנו באחד, ברגע שהוא נכנס.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏`tails[k]` הוא הערך הקטן ביותר שבו נגמרת תת-סדרה עולה באורך \( k + 1 \) מבין האיברים
        שנקראו. המערך עולה ממש, ולכן לכל \( x \) מוצאים בחיפוש בינארי את ה-\( k \) הראשון עם
        `tails[k] >= x` : אם אין כזה, \( x \) מאריך את המערך, ואחרת הוא מחליף את `tails[k]`. האורך של
        `tails` בסוף הוא אורך ה-LIS. בדוגמה `tails = [2, 3, 7, 18]`, ושחזור לפי `parent` נותן
        `[2, 3, 7, 18]`.

    <!-- cost: זמן \( O(n \log n) \), ‏10 השוואות בדוגמה | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    בסעיף א כל איבר הסתכל על כל הקודמים. אבל מכל הסדרות באורך \( L \), רק אחת מעניינת : זו
    שנגמרת בערך הקטן ביותר, כי כל איבר שמאריך סדרה אחרת באורך \( L \) מאריך גם אותה. כך מספיק
    לזכור ערך אחד לכל אורך. הנה `tails` אחרי כל איבר של הדוגמה :

    <!-- gen 1 -->

    <svg class="figure lis-fig" viewBox="0 0 402 340" style="max-width:25.1rem" role="img" aria-label="סעיף ב : מערך tails אחרי כל איבר של 10 9 2 5 3 7 101 18. x = 10 : מאריך במקום 0, tails = 10; x = 9 : מחליף את 10 במקום 0, tails = 9; x = 2 : מחליף את 9 במקום 0, tails = 2; x = 5 : מאריך במקום 1, tails = 2 5; x = 3 : מחליף את 5 במקום 1, tails = 2 3; x = 7 : מאריך במקום 2, tails = 2 3 7; x = 101 : מאריך במקום 3, tails = 2 3 7 101; x = 18 : מחליף את 101 במקום 3, tails = 2 3 7 18"><text class="lis-idx" x="122" y="14" text-anchor="middle">0</text><text class="lis-idx" x="164" y="14" text-anchor="middle">1</text><text class="lis-idx" x="206" y="14" text-anchor="middle">2</text><text class="lis-idx" x="248" y="14" text-anchor="middle">3</text><text class="lis-lab" x="94" y="14" text-anchor="end">k</text><text class="lis-lab" x="94" y="47" text-anchor="end">x = 10</text><rect class="lis-cell is-new" x="104" y="24" width="36" height="32" rx="3"/><text class="lis-num" x="122" y="45" text-anchor="middle">10</text><text class="lis-side" x="276" y="45">k = 0, append</text><text class="lis-lab" x="94" y="87" text-anchor="end">x = 9</text><rect class="lis-cell is-rep" x="104" y="64" width="36" height="32" rx="3"/><text class="lis-num" x="122" y="85" text-anchor="middle">9</text><text class="lis-side" x="276" y="85">k = 0, 10 → 9</text><text class="lis-lab" x="94" y="127" text-anchor="end">x = 2</text><rect class="lis-cell is-rep" x="104" y="104" width="36" height="32" rx="3"/><text class="lis-num" x="122" y="125" text-anchor="middle">2</text><text class="lis-side" x="276" y="125">k = 0, 9 → 2</text><text class="lis-lab" x="94" y="167" text-anchor="end">x = 5</text><rect class="lis-cell" x="104" y="144" width="36" height="32" rx="3"/><text class="lis-num" x="122" y="165" text-anchor="middle">2</text><rect class="lis-cell is-new" x="146" y="144" width="36" height="32" rx="3"/><text class="lis-num" x="164" y="165" text-anchor="middle">5</text><text class="lis-side" x="276" y="165">k = 1, append</text><text class="lis-lab" x="94" y="207" text-anchor="end">x = 3</text><rect class="lis-cell" x="104" y="184" width="36" height="32" rx="3"/><text class="lis-num" x="122" y="205" text-anchor="middle">2</text><rect class="lis-cell is-rep" x="146" y="184" width="36" height="32" rx="3"/><text class="lis-num" x="164" y="205" text-anchor="middle">3</text><text class="lis-side" x="276" y="205">k = 1, 5 → 3</text><text class="lis-lab" x="94" y="247" text-anchor="end">x = 7</text><rect class="lis-cell" x="104" y="224" width="36" height="32" rx="3"/><text class="lis-num" x="122" y="245" text-anchor="middle">2</text><rect class="lis-cell" x="146" y="224" width="36" height="32" rx="3"/><text class="lis-num" x="164" y="245" text-anchor="middle">3</text><rect class="lis-cell is-new" x="188" y="224" width="36" height="32" rx="3"/><text class="lis-num" x="206" y="245" text-anchor="middle">7</text><text class="lis-side" x="276" y="245">k = 2, append</text><text class="lis-lab" x="94" y="287" text-anchor="end">x = 101</text><rect class="lis-cell" x="104" y="264" width="36" height="32" rx="3"/><text class="lis-num" x="122" y="285" text-anchor="middle">2</text><rect class="lis-cell" x="146" y="264" width="36" height="32" rx="3"/><text class="lis-num" x="164" y="285" text-anchor="middle">3</text><rect class="lis-cell" x="188" y="264" width="36" height="32" rx="3"/><text class="lis-num" x="206" y="285" text-anchor="middle">7</text><rect class="lis-cell is-new" x="230" y="264" width="36" height="32" rx="3"/><text class="lis-num" x="248" y="285" text-anchor="middle">101</text><text class="lis-side" x="276" y="285">k = 3, append</text><text class="lis-lab" x="94" y="327" text-anchor="end">x = 18</text><rect class="lis-cell" x="104" y="304" width="36" height="32" rx="3"/><text class="lis-num" x="122" y="325" text-anchor="middle">2</text><rect class="lis-cell" x="146" y="304" width="36" height="32" rx="3"/><text class="lis-num" x="164" y="325" text-anchor="middle">3</text><rect class="lis-cell" x="188" y="304" width="36" height="32" rx="3"/><text class="lis-num" x="206" y="325" text-anchor="middle">7</text><rect class="lis-cell is-rep" x="230" y="304" width="36" height="32" rx="3"/><text class="lis-num" x="248" y="325" text-anchor="middle">18</text><text class="lis-side" x="276" y="325">k = 3, 101 → 18</text></svg>

    <span class="viz-legend"><span><i class="lis-key-new"></i>\( x \) מאריך את <code>tails</code></span><span><i class="fc-key-chg"></i>\( x \) מחליף ערך גדול ממנו או שווה לו</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **חיפוש בינארי :** לכל \( x \) מחפשים את ה-\( k \) הראשון עם `tails[k] >= x`, בין `lo = 0`
       ל-`hi = len(tails)`. אם `tails[mid] < x`, ה-\( k \) מימין ל-`mid` (‏`lo = mid + 1`), ואחרת
       הוא `mid` או משמאל לו (‏`hi = mid`). זה `bisect_left`.

    2. **הארכה או החלפה :** אם \( k \) הוא האורך של `tails`, כל הערכים קטנים מ-\( x \), והוא מאריך
       את הסדרה הארוכה ביותר : `tails.append(x)`. אחרת `tails[k] = x` : סדרה באורך \( k + 1 \)
       שנגמרת ב-\( x \), שהוא קטן מהערך הקודם או שווה לו.

    3. **המצביע אחורה :** `tail_at[k]` הוא האינדקס במערך של הערך `tails[k]`. האיבר שלפני \( x \) הוא
       `parent[i] = tail_at[k - 1]`, הסוף של סדרה באורך \( k \) ברגע הזה, או \( -1 \) כש-\( k = 0 \).

    4. **השחזור :** מתחילים ב-`tail_at[-1]`, הסוף של הסדרה הארוכה, והולכים לאחור לפי `parent`.

    </div>

    השחזור בדוגמה : `parent` של כל איבר, והשרשרת אחורה מ-`tail_at[3] = 7`, האינדקס של 18 :

    <!-- gen 2 -->

    <svg class="figure lis-fig" viewBox="0 0 402 136" style="max-width:25.1rem" role="img" aria-label="סעיף ב, השחזור : parent של כל איבר, – – – 2 2 4 5 5. מהאיבר האחרון שנכנס לסוף tails, האינדקס 7, אחורה לפי parent : 2 3 7 18"><g transform="translate(18 0)"><path class="lis-link" d="M148,50 Q169,26 190,50"/><path class="lis-link" d="M274,50 Q295,26 316,50"/><path class="lis-link is-chain" d="M148,50 Q190,14 232,50"/><path class="lis-link is-chain" d="M232,50 Q253,26 274,50"/><path class="lis-link is-chain" d="M274,50 Q316,14 358,50"/><text class="lis-idx" x="64" y="14" text-anchor="middle">0</text><rect class="st-cell" x="46" y="52" width="36" height="36" rx="3"/><text class="st-text" x="64" y="75" text-anchor="middle">10</text><text class="lis-idx" x="106" y="14" text-anchor="middle">1</text><rect class="st-cell" x="88" y="52" width="36" height="36" rx="3"/><text class="st-text" x="106" y="75" text-anchor="middle">9</text><text class="lis-idx" x="148" y="14" text-anchor="middle">2</text><rect class="fig-one" x="130" y="52" width="36" height="36" rx="3"/><text class="st-text" x="148" y="75" text-anchor="middle">2</text><text class="lis-idx" x="190" y="14" text-anchor="middle">3</text><rect class="st-cell" x="172" y="52" width="36" height="36" rx="3"/><text class="st-text" x="190" y="75" text-anchor="middle">5</text><text class="lis-idx" x="232" y="14" text-anchor="middle">4</text><rect class="fig-one" x="214" y="52" width="36" height="36" rx="3"/><text class="st-text" x="232" y="75" text-anchor="middle">3</text><text class="lis-idx" x="274" y="14" text-anchor="middle">5</text><rect class="fig-one" x="256" y="52" width="36" height="36" rx="3"/><text class="st-text" x="274" y="75" text-anchor="middle">7</text><text class="lis-idx" x="316" y="14" text-anchor="middle">6</text><rect class="st-cell" x="298" y="52" width="36" height="36" rx="3"/><text class="st-text" x="316" y="75" text-anchor="middle">101</text><text class="lis-idx" x="358" y="14" text-anchor="middle">7</text><rect class="fig-one" x="340" y="52" width="36" height="36" rx="3"/><text class="st-text" x="358" y="75" text-anchor="middle">18</text><text class="lis-lab" x="36" y="75" text-anchor="end">a</text><text class="lis-lab" x="36" y="120" text-anchor="end">parent</text><rect class="lis-val" x="46" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="64" y="119" text-anchor="middle">–</text><rect class="lis-val" x="88" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="106" y="119" text-anchor="middle">–</text><rect class="lis-val is-lit" x="130" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="148" y="119" text-anchor="middle">–</text><rect class="lis-val" x="172" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="190" y="119" text-anchor="middle">2</text><rect class="lis-val is-lit" x="214" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="232" y="119" text-anchor="middle">2</text><rect class="lis-val is-lit" x="256" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="274" y="119" text-anchor="middle">4</text><rect class="lis-val" x="298" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="316" y="119" text-anchor="middle">5</text><rect class="lis-val is-lit" x="340" y="100" width="36" height="28" rx="3"/><text class="lis-num" x="358" y="119" text-anchor="middle">5</text></g></svg>

    <span class="viz-legend"><span><i class="fc-key-sorted"></i>הסדרה שהשחזור מחזיר</span><span><i class="lis-key-chain"></i>הקשת מ-<code>parent[i]</code> ל-<code>i</code> שלה</span><span><i class="lis-key-link"></i>קשת <code>parent</code> של איבר אחר</span><span>הסימן – הוא \( -1 \)</span></span>

    <!-- /gen -->

    בתיבה כל צעד הוא השוואה אחת של החיפוש הבינארי, או הכנסה של \( x \) ל-`tails`. מעל המערך
    הקשתות של `parent` :

    <div class="explorer" data-kind="lis" data-mode="tails" data-nums="10 9 2 5 3 7 101 18"></div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="lis" linenums="1" hl_lines="7 8 9 10 11 12 19"
        def lis(a: list[int]) -> list[int]:
            """Part b: one longest strictly increasing subsequence of a, in O(n log n)."""
            tails, tail_at = [], []          # (1)!
            parent = [-1] * len(a)
            for i, x in enumerate(a):
                lo, hi = 0, len(tails)
                while lo < hi:               # (2)!
                    mid = (lo + hi) // 2
                    if tails[mid] < x:
                        lo = mid + 1
                    else:
                        hi = mid
                if lo == len(tails):         # (3)!
                    tails.append(x)
                    tail_at.append(i)
                else:
                    tails[lo] = x
                    tail_at[lo] = i
                parent[i] = tail_at[lo - 1] if lo else -1   # (4)!
            out, i = [], tail_at[-1] if tail_at else -1
            while i >= 0:                    # (5)!
                out.append(a[i])
                i = parent[i]
            return out[::-1]
        ```

        1. ‏`tails[k]` : הסוף הקטן ביותר של סדרה עולה באורך \( k + 1 \). ‏`tail_at[k]` : האינדקס שלו ב-`a`.
        2. החיפוש הבינארי של `bisect_left(tails, x)`, כתוב במפורש כמו בתיבה.
        3. ‏\( x \) גדול מכל `tails` : הסדרה הארוכה ביותר גדלה באחד.
        4. האיבר שלפני \( x \) : הסוף של סדרה באורך \( k \) ברגע הזה. הוא קטן מ-\( x \) ומוקדם ממנו.
        5. מהסוף של הסדרה הארוכה, אחורה לפי `parent`, ובסוף הפיכה.

    === "SystemVerilog"
        ```systemverilog title="function lis" linenums="1" hl_lines="7 8 9 10 11"
        // Part b: one longest strictly increasing subsequence of a, in O(n log n).
        function automatic void lis(int a[$], ref int out[$]);
          int tails[$], tail_at[$], parent[$];
          int lo, hi, mid, k;
          foreach (a[i]) begin
            lo = 0;
            hi = tails.size();
            while (lo < hi) begin                       // (1)!
              mid = (lo + hi) / 2;
              if (tails[mid] < a[i]) lo = mid + 1;
              else hi = mid;
            end
            if (lo == tails.size()) begin
              tails.push_back(a[i]);
              tail_at.push_back(i);
            end else begin
              tails[lo] = a[i];
              tail_at[lo] = i;
            end
            parent.push_back(lo > 0 ? tail_at[lo - 1] : -1);
          end
          out.delete();
          k = tail_at.size() > 0 ? tail_at[tail_at.size() - 1] : -1;
          while (k >= 0) begin                          // (2)!
            out.push_front(a[k]);
            k = parent[k];
          end
        endfunction
        ```

        1. החיפוש הבינארי, כמו ב-Python : ה-\( k \) הראשון עם `tails[k] >= a[i]`.
        2. ‏`push_front` במקום הפיכה בסוף.

    #### למה זה נכון { .sol-proof }

    **האינווריאנטה.** אחרי כל איבר, לכל \( k \) קטן מהאורך של `tails`, ‏`tails[k]` הוא הערך הקטן
    ביותר שבו נגמרת תת-סדרה עולה באורך \( k + 1 \) מבין האיברים שנקראו, ואין תת-סדרה עולה ארוכה
    מהאורך של `tails`.

    **‏tails עולה ממש.** קחו את הסדרה באורך \( k + 2 \) שנגמרת ב-`tails[k + 1]`. האיבר שלפני הסוף
    שלה גומר סדרה באורך \( k + 1 \), והוא קטן מ-`tails[k + 1]`. לכן `tails[k]`, המינימום על כל
    הסדרות באורך \( k + 1 \), קטן מ-`tails[k + 1]`. כך המערך ממוין, והחיפוש הבינארי מותר.

    **הצעד.** נניח שהאינווריאנטה נכונה לפני \( x \), ו-\( k \) הוא ה-\( k \) הראשון עם
    `tails[k] >= x`. ‏\( x \) יכול לגמור סדרה באורך \( L + 1 \) רק אם יש לפניו סדרה באורך \( L \)
    שנגמרת בערך קטן ממנו, כלומר רק אם `tails[L - 1] < x`. זה נכון בדיוק ל-\( L \le k \). לכל
    \( L < k \) הסוף \( x \) גדול מ-`tails[L]`, ולכן לא משנה את המינימום. ל-\( L = k \) הסוף \( x \)
    קטן מ-`tails[k]` או שווה לו, ולכן הוא המינימום החדש, או, כש-\( k \) הוא האורך של `tails`, אורך
    חדש. ל-\( L > k \) אין סדרה כזו שנגמרת ב-\( x \).

    **השחזור.** כש-\( x \) נכנס למקום \( k \), ‏`parent[i] = tail_at[k - 1]` הוא אינדקס מוקדם יותר
    עם ערך קטן מ-\( x \), שגומר סדרה באורך \( k \) שהשחזור שלה כבר נכון. באינדוקציה, ההליכה לאחור
    מכל איבר שנכנס למקום \( k \) נותנת סדרה עולה באורך \( k + 1 \).

    #### סיבוכיות { .sol-cost }

    זמן \( O(n \log n) \) : לכל איבר חיפוש בינארי במערך של לכל היותר \( n \) ערכים. בדוגמה 10
    השוואות במקום 28. זיכרון \( O(n) \) ל-`tails`, ‏`tail_at` ו-`parent`.

---

### סעיף ג – כמה תתי-סדרות עולות ארוכות ביותר יש { #count }

כתבו פונקציה שסופרת כמה תתי-סדרות עולות באורך המקסימלי יש במערך. שתי תתי-סדרות שונות אם הן
משתמשות באינדקסים שונים, גם כשהערכים שלהן שווים. למשל ב-`[1, 3, 5, 4, 7]` יש שתיים : `[1, 3, 5, 7]`
ו-`[1, 3, 4, 7]`.

??? tip "רמז 1"
    לצד `dp[i]`, האורך, שמרו `cnt[i]` : כמה תתי-סדרות עולות באורך `dp[i]` נגמרות ב-`a[i]`.

??? tip "רמז 2"
    ‏\( j \) עם `a[j] < a[i]` ו-`dp[j] + 1 > dp[i]` נותן אורך חדש, ואז `cnt[i] = cnt[j]`. מה קורה
    כש-`dp[j] + 1 == dp[i]`?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        זוג של אורך ומספר לכל \( i \) : ‏\( j \) שנותן אורך גדול יותר מחליף את הזוג ל-
        `(dp[j] + 1, cnt[j])`, ו-\( j \) שנותן אותו אורך מוסיף `cnt[j]` למספר. התשובה היא הסכום של
        `cnt[i]` על כל ה-\( i \) שבהם `dp[i]` מקסימלי. ב-`[1, 3, 5, 4, 7]` זה 2, ובדוגמה של סעיף א
        זה 4.

    <!-- cost: זמן \( O(n^2) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    כל תת-סדרה באורך המקסימלי שנגמרת ב-`a[i]` נוצרת מתת-סדרה באורך המקסימלי שנגמרת באיבר
    הקודם בה, ואחריה `a[i]`. לכן המספר ב-\( i \) הוא סכום המספרים ב-\( j \)-ים שנותנים את האורך
    המקסימלי, ורק בהם. הנה הזוגות של `[1, 3, 5, 4, 7]` :

    <!-- gen 3 -->

    <div class="gs-scroll" tabindex="0" role="region" aria-label="סעיף ג, המערך 1 3 5 4 7 : לכל אינדקס האורך length ומספר הסדרות count. האורך המקסימלי 4, והסכום של count בעמודות שלו הוא 2"><table class="gs-bits lis-tab" dir="ltr" aria-label="סעיף ג, המערך 1 3 5 4 7 : לכל אינדקס האורך length ומספר הסדרות count. האורך המקסימלי 4, והסכום של count בעמודות שלו הוא 2"><tbody><tr class="lis-ix"><th>i</th><td class="gs-b">0</td><td class="gs-b">1</td><td class="gs-b">2</td><td class="gs-b">3</td><td class="gs-b is-one">4</td></tr><tr><th>a[i]</th><td class="gs-b">1</td><td class="gs-b">3</td><td class="gs-b">5</td><td class="gs-b">4</td><td class="gs-b is-one">7</td></tr><tr><th>length</th><td class="gs-b">1</td><td class="gs-b">2</td><td class="gs-b">3</td><td class="gs-b">3</td><td class="gs-b is-one">4</td></tr><tr><th>count</th><td class="gs-b">1</td><td class="gs-b">1</td><td class="gs-b">1</td><td class="gs-b">1</td><td class="gs-b is-one">2</td></tr></tbody></table></div>

    <span class="viz-legend"><span><i class="gs-key-one"></i>אורך מקסימלי, 4 : הסכום של <code>count</code> בעמודות האלה הוא 2</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **התחלה :** `length[i] = 1` ו-`count[i] = 1` : האיבר לבדו.

    2. **אורך חדש :** ‏\( j < i \) עם `a[j] < a[i]` ו-`length[j] + 1 > length[i]` : כל הסדרות הקודמות
       קצרות יותר, ולכן `length[i] = length[j] + 1` ו-`count[i] = count[j]`.

    3. **אותו אורך :** `length[j] + 1 == length[i]` : עוד `count[j]` סדרות באותו אורך,
       ‏`count[i] += count[j]`.

    4. **הסכום :** האורך המקסימלי \( L \) הוא המקסימום של `length`, והתשובה היא סכום `count[i]` על
       ה-\( i \)-ים עם `length[i] = L`. ב-`[1, 3, 5, 4, 7]` רק `a[4] = 7` גומר סדרה באורך 4, ושם
       `count = 1 + 1 = 2`.

    </div>

    בתיבה שורת `cnt` היא `count`. אותה תיבה כמו בסעיף א, על המערך של הסעיף :

    <div class="explorer" data-kind="lis" data-mode="dp" data-nums="1 3 5 4 7"></div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="count_lis" linenums="1" hl_lines="7 9"
        def count_lis(a: list[int]) -> int:
            """Part c: how many strictly increasing subsequences of the largest length a has."""
            length, count = [1] * len(a), [1] * len(a)
            for i in range(len(a)):
                for j in range(i):
                    if a[j] < a[i]:
                        if length[j] + 1 > length[i]:      # (1)!
                            length[i], count[i] = length[j] + 1, count[j]
                        elif length[j] + 1 == length[i]:  # (2)!
                            count[i] += count[j]
            best = max(length, default=0)
            return sum(c for n, c in zip(length, count) if n == best)
        ```

        1. אורך חדש : כל מה שנספר עד עכשיו קצר יותר, והמספר מתחיל מחדש מ-`count[j]`.
        2. אותו אורך דרך \( j \) אחר : עוד `count[j]` סדרות, כולן שונות מהקודמות באיבר שלפני `a[i]`.

    === "SystemVerilog"
        ```systemverilog title="function count_lis" linenums="1" hl_lines="11 14"
        // Part c: how many strictly increasing subsequences of the largest length a has.
        function automatic longint count_lis(int a[$]);
          int length[$];
          longint count[$];
          int best = 0;
          longint total = 0;
          foreach (a[i]) begin
            length.push_back(1);
            count.push_back(1);
            for (int j = 0; j < i; j++)
              if (a[j] < a[i]) begin
                if (length[j] + 1 > length[i]) begin      // (1)!
                  length[i] = length[j] + 1;
                  count[i] = count[j];
                end else if (length[j] + 1 == length[i])  // (2)!
                  count[i] += count[j];
              end
            if (length[i] > best) best = length[i];
          end
          foreach (a[i]) if (length[i] == best) total += count[i];
          return total;
        endfunction
        ```

        1. אורך חדש : המספר מתחיל מחדש.
        2. אותו אורך : המספרים מצטברים. ‏`longint`, כי המספר יכול לגדול כמו \( 2^{n/2} \).

    #### למה זה נכון { .sol-proof }

    נראה באינדוקציה ש-`count[i]` הוא מספר תתי-הסדרות העולות באורך `length[i]` שנגמרות ב-`a[i]`.
    סדרה כזו עם יותר מאיבר אחד מורכבת מסדרה שנגמרת באיבר \( j < i \) עם `a[j] < a[i]`, ואחריה
    `a[i]`. החלק הזה הוא סדרה עולה באורך `length[i] - 1` שנגמרת ב-`a[j]`, ולכן
    `length[j] >= length[i] - 1`. מצד שני `length[j] <= length[i] - 1`, אחרת `a[i]` היה מאריך סדרה
    ארוכה יותר. לכן `length[j] = length[i] - 1`, והחלק הוא אחת מ-`count[j]` הסדרות שנספרו ב-\( j \).
    הסדרות נחלקות לפי ה-\( j \) שלפני `a[i]` : ב-\( j \) מסוים יש בדיוק `count[j]` מהן, ומ-\( j \)-ים
    שונים הן שונות. זה בדיוק הסכום שהקוד צובר : הענף "אורך חדש" מאפס את הסכום כשמתגלה אורך
    גדול יותר, והענף "אותו אורך" מוסיף. בסוף, כל תת-סדרה באורך המקסימלי נגמרת באיבר אחד, ולכן
    הסכום על ה-\( i \)-ים עם האורך המקסימלי סופר כל אחת פעם אחת.

    בדוגמה של סעיף א ארבע תתי-סדרות באורך 4 : שתיים נגמרות ב-101 ושתיים ב-18.

    <!-- gen 4 -->

    <div class="gs-scroll" tabindex="0" role="region" aria-label="סעיף ג, הדוגמה של סעיף א : לכל אינדקס האורך length ומספר הסדרות count. האורך המקסימלי 4, והסכום של count בעמודות שלו הוא 4"><table class="gs-bits lis-tab" dir="ltr" aria-label="סעיף ג, הדוגמה של סעיף א : לכל אינדקס האורך length ומספר הסדרות count. האורך המקסימלי 4, והסכום של count בעמודות שלו הוא 4"><tbody><tr class="lis-ix"><th>i</th><td class="gs-b">0</td><td class="gs-b">1</td><td class="gs-b">2</td><td class="gs-b">3</td><td class="gs-b">4</td><td class="gs-b">5</td><td class="gs-b is-one">6</td><td class="gs-b is-one">7</td></tr><tr><th>a[i]</th><td class="gs-b">10</td><td class="gs-b">9</td><td class="gs-b">2</td><td class="gs-b">5</td><td class="gs-b">3</td><td class="gs-b">7</td><td class="gs-b is-one">101</td><td class="gs-b is-one">18</td></tr><tr><th>length</th><td class="gs-b">1</td><td class="gs-b">1</td><td class="gs-b">1</td><td class="gs-b">2</td><td class="gs-b">2</td><td class="gs-b">3</td><td class="gs-b is-one">4</td><td class="gs-b is-one">4</td></tr><tr><th>count</th><td class="gs-b">1</td><td class="gs-b">1</td><td class="gs-b">1</td><td class="gs-b">1</td><td class="gs-b">1</td><td class="gs-b">2</td><td class="gs-b is-one">2</td><td class="gs-b is-one">2</td></tr></tbody></table></div>

    <span class="viz-legend"><span><i class="gs-key-one"></i>אורך מקסימלי, 4 : הסכום של <code>count</code> בעמודות האלה הוא 4</span></span>

    <!-- /gen -->

    #### סיבוכיות { .sol-cost }

    זמן \( O(n^2) \), כמו בסעיף א, וזיכרון \( O(n) \). המספר עצמו יכול להיות אקספוננציאלי :
    במערך `[2, 1, 4, 3, 6, 5, …]` של \( n \) איברים יש \( 2^{n/2} \) תתי-סדרות ארוכות ביותר.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : tails הוא לא ה-LIS"
    ב-`[3, 4, 5, 1]` בסוף `tails = [1, 4, 5]`, אבל 1 בא **אחרי** 5 במערך, ולכן זו לא תת-סדרה. האורך
    של `tails` נכון, ו-`[3, 4, 5]` היא התשובה. כדי להחזיר את הסדרה צריך את `parent` של סעיף ב.

??? trap "מלכודת : bisect_right"
    עם `bisect_right` ערך שווה לא מחליף את עצמו אלא נכנס אחריו, וזה סופר תתי-סדרות **לא יורדות**.
    ב-`[2, 2, 2]` התשובה של עולה ממש היא 1, ועם `bisect_right` יוצא 3.

??? trap "מלכודת : dp[n - 1] במקום המקסימום"
    ‏`dp[n - 1]` הוא האורך של הסדרה שנגמרת באיבר האחרון. ב-`[3, 4, 1]` הוא 1, והתשובה 2.

??? trap "מלכודת : חמדן מההתחלה"
    לקחת כל איבר שגדול מהאחרון שנלקח לא עובד : ב-`[10, 1, 2, 3]` זה נותן `[10]`, והתשובה
    `[1, 2, 3]`. גם להתחיל מכל איבר בנפרד לא עוזר : ב-`[1, 5, 2, 3]` החמדן מ-1 לוקח את 5 ונתקע.

??? followup "שאלות המשך"
    - **לא יורדת :** איך משנים את סעיף ב כך שגם ערכים שווים מותרים?

        ??? fu-answer "תשובה"
            מחפשים את ה-\( k \) הראשון עם `tails[k] > x`, כלומר `bisect_right`, ובחיפוש
            `if tails[mid] <= x: lo = mid + 1`. ב-`[2, 2, 2]` זה נותן 3.

    - **ערימות של פסיאנס :** מחלקים קלפים לערימות, וכל קלף נכנס לערימה השמאלית ביותר שהקלף
      העליון שלה גדול ממנו או שווה לו, או לערימה חדשה. כמה ערימות יהיו?

        ??? fu-answer "תשובה"
            כאורך ה-LIS : הקלפים העליונים הם בדיוק `tails`. כל ערימה היא תת-סדרה לא עולה, ולכן זה גם
            המספר הקטן ביותר של תתי-סדרות לא עולות שמכסות את המערך (Dilworth).

    - **מעטפות בתוך מעטפות :** לכל מעטפה רוחב וגובה, ומעטפה נכנסת לאחרת כששני הממדים קטנים
      ממש. כמה מעטפות אפשר לשים זו בתוך זו?

        ??? fu-answer "תשובה"
            ממיינים לפי רוחב עולה, וברוחב שווה לפי גובה **יורד**, ואז LIS עולה ממש על הגבהים. הסדר
            היורד מונע לקחת שתי מעטפות באותו רוחב.

    - **ספירה ב-\( O(n \log n) \) :** איך מאיצים את סעיף ג?

        ??? fu-answer "תשובה"
            עץ Fenwick על הערכים אחרי דחיסה, שבכל תא זוג של אורך ומספר. לכל `a[i]` שואלים את
            הזוג הטוב ביותר על הערכים הקטנים ממנו ב-\( O(\log n) \), עם אותו כלל איחוד כמו בסעיף
            ג, ומעדכנים את התא של `a[i]`.

    - **ארדש-סקרש :** למה בכל סדרה של \( n^2 + 1 \) מספרים שונים יש תת-סדרה מונוטונית באורך
      \( n + 1 \)?

        ??? fu-answer "תשובה"
            אם ה-LIS קצר מ-\( n + 1 \), יש לכל היותר \( n \) ערימות של פסיאנס, ולכן באחת מהן לפחות
            \( n + 1 \) קלפים : תת-סדרה יורדת באורך \( n + 1 \).
