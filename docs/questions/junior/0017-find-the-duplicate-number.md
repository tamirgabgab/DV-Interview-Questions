---
id: 17
title: המספר הכפול – בלי לשנות את המערך ובלי זיכרון נוסף
level: junior
difficulty: medium
kind: code
tags: [algorithms, math, python, systemverilog]
source: "LeetCode 287 – Find the Duplicate Number"
added: 2026-10-18
---

## השאלה

נתון מערך `nums` של \( n + 1 \) מספרים שלמים, וכל אחד מהם בין 1 ל-\( n \). יש \( n + 1 \)
מספרים ורק \( n \) ערכים אפשריים, ולכן לפי **עקרון שובך היונים** לפחות ערך אחד מופיע
יותר מפעם אחת. כתבו פונקציה שמחזירה ערך כזה.

הדוגמה שתלווה את כל השאלה, עם \( n = 9 \) :

<div class="box-grid bg-10" dir="ltr"><span><small>0</small><b>3</b></span><span><small>1</small><b>9</b></span><span><small>2</small><b>5</b></span><span><small>3</small><b>6</b></span><span><small>4</small><b>7</b></span><span><small>5</small><b>8</b></span><span class="hl"><small>6</small><b>1</b></span><span class="hl"><small>7</small><b>1</b></span><span><small>8</small><b>2</b></span><span><small>9</small><b>4</b></span></div>

כאן הערך 1 מופיע פעמיים, באינדקסים 6 ו-7, וזו התשובה. ייתכן גם שערך כפול מופיע יותר
משתי פעמים, או שיש כמה ערכים כפולים. אז מספיק להחזיר אחד מהם.

??? interviewer "מה המראיין בודק"
    - **מהפשוט למוגבל :** להתחיל מפתרון נכון וברור, ואז להתאים אותו לאילוצים חדשים, ולא
      לקפוץ ישר לטריק.
    - **לנמק מחיר :** לכל פתרון לומר מה הוא עולה בזמן ובזיכרון, ואיזה אילוץ הוא שובר.
    - **עקרון שובך היונים :** להשתמש בו לא רק כדי לדעת שיש כפול, אלא גם כדי למצוא אותו.
    - **לראות גרף במערך :** לזהות שמערך שהערכים שלו הם אינדקסים הוא רשימה מקושרת, ושכפול
      הוא כניסה למעגל.
    - **הוכחה ולא שינון :** להסביר למה שלב 2 של Floyd נפגש בדיוק בכניסה למעגל.

---

### סעיף א – בלי הגבלות

כתבו פתרון נכון ופשוט. מותר לשנות את המערך או להשתמש בזיכרון נוסף. מה הסיבוכיות?

??? tip "רמז 1"
    אם המספרים היו ממוינים, איפה היה מופיע הכפול ביחס לעותק השני שלו?

??? tip "רמז 2"
    בלי מיון : עוברים על המערך פעם אחת וזוכרים אילו ערכים כבר ראינו. כל הערכים בין 1
    ל-\( n \), אז מספיק מערך של סימונים.

??? success "פתרון 1 – מיון"
    !!! answer "תשובה בקצרה"
        ממיינים עותק של המערך. אחרי המיון העותקים של ערך כפול צמודים, ולכן מספיק להשוות כל
        איבר לקודם לו. זמן \( O(n \log n) \), וזיכרון \( O(n) \) לעותק.

    <!-- cost: זמן \( O(n \log n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    מיון מקבץ ערכים שווים יחד. לכן במערך ממוין יש כפול אם ורק אם יש שני איברים **סמוכים**
    ששווים זה לזה, ואת זה בודקים במעבר אחד.

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function find_duplicate_sort" linenums="1" hl_lines="2 5"
        function automatic int find_duplicate_sort(const ref int nums[]);   // (1)!
          int s[] = nums;   // (2)!
          s.sort();
          for (int i = 1; i < s.size(); i++)
            if (s[i] == s[i - 1]) return s[i];   // equal neighbours: a duplicate
          return -1;                             // never reached for a valid input
        endfunction
        ```

        1. ‏`const ref` מעביר את המערך בלי להעתיק אותו, ומבטיח שהפונקציה לא משנה אותו : כתיבה
           ל-`nums` היא שגיאת קומפילציה. כל ארבעת הפתרונות מקבלים את הקלט כך.
        2. ‏`s.sort()` ממיין במקום. בגלל `const ref` אי אפשר למיין את `nums` עצמו, ולכן ממיינים
           עותק, וזה הזיכרון הנוסף של \( O(n) \).

    === "Python"
        ```python title="find_duplicate_sort" linenums="1" hl_lines="2 4"
        def find_duplicate_sort(nums: list[int]) -> int:
            s = sorted(nums)   # (1)!
            for i in range(1, len(s)):
                if s[i] == s[i - 1]:   # equal neighbours: a duplicate
                    return s[i]
            return -1   # never reached for a valid input
        ```

        1. ‏`sorted` מחזיר רשימה חדשה ולא נוגע ב-`nums`. ‏`nums.sort()` היה ממיין במקום, בלי
           זיכרון נוסף, אבל משנה את הקלט של מי שקרא לפונקציה.

    #### סיבוכיות { .sol-cost }

    - **זמן :** \( O(n \log n) \) למיון, ועוד \( O(n) \) למעבר.
    - **זיכרון :** \( O(n) \) לעותק. מיון במקום חוסך את העותק, אבל משנה את המערך.

??? success "פתרון 2 – טבלת סימונים"
    !!! answer "תשובה בקצרה"
        מערך `seen` של \( n + 1 \) ביטים. עוברים על `nums` : אם `seen[v]` כבר דלוק, \( v \) הוא
        הכפול. אחרת מדליקים אותו. זמן \( O(n) \), זיכרון \( O(n) \).

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    הערכים הם בין 1 ל-\( n \), ולכן אפשר להשתמש בהם ישירות כאינדקסים לטבלה. הערך הראשון
    שמגיע למשבצת שכבר מסומנת הוא כפול.

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function find_duplicate_seen" linenums="1" hl_lines="4"
        function automatic int find_duplicate_seen(const ref int nums[]);
          bit seen[] = new[nums.size()];   // (1)!
          foreach (nums[i]) begin
            if (seen[nums[i]]) return nums[i];   // the second time we meet this value
            seen[nums[i]] = 1;
          end
          return -1;
        endfunction
        ```

        1. ‏\( n + 1 \) משבצות, באינדקסים 0 עד \( n \), בדיוק כמו גודל הקלט. ערך תמיד בין 1
           ל-\( n \), ולכן `seen[0]` לא בשימוש וכל גישה חוקית.

    === "Python"
        ```python title="find_duplicate_seen" linenums="1" hl_lines="4"
        def find_duplicate_seen(nums: list[int]) -> int:
            seen = [False] * len(nums)   # (1)!
            for v in nums:
                if seen[v]:              # the second time we meet this value
                    return v
                seen[v] = True
            return -1
        ```

        1. אפשר גם `set()`, אבל רשימה באורך \( n + 1 \) מראה שהזיכרון הוא בדיוק ביט, או בית,
           לכל ערך אפשרי.

    #### סיבוכיות { .sol-cost }

    - **זמן :** \( O(n) \), מעבר אחד.
    - **זיכרון :** \( O(n) \) לטבלה. זה הפתרון הכי מהיר, אבל הוא שובר את האילוץ של סעיף ב.

---

### סעיף ב – בלי לשנות את המערך ובזיכרון קבוע { #o1 }

עכשיו אסור לשנות את `nums` ואסור להקצות זיכרון שתלוי ב-\( n \). מותרים רק כמה משתנים. מצאו
פתרון שמהיר יותר מ-\( O(n^2) \), ואז פתרון בזמן \( O(n) \).

??? tip "רמז 1"
    בחרו ערך \( mid \) וספרו כמה מספרים במערך הם לכל היותר \( mid \). מה עקרון שובך היונים
    אומר אם התוצאה גדולה מ-\( mid \)?

??? tip "רמז 2"
    עכשיו לפתרון ב-\( O(n) \) : חשבו על כל אינדקס \( i \) כעל צומת עם חץ אל `nums[i]`. מה
    המשמעות של שני חצים שנכנסים לאותו צומת?

??? tip "רמז 3"
    מתחילים מאינדקס 0 והולכים לפי החצים. ההליכה חייבת להיכנס למעגל. איך מוצאים את הכניסה
    למעגל עם שני מצביעים בלבד?

??? success "פתרון 3 – חיפוש בינארי על הערכים"
    !!! answer "תשובה בקצרה"
        מחפשים בינארית על **הערכים** ולא על האינדקסים. אם יותר מ-\( mid \) מספרים הם לכל
        היותר \( mid \), יש כפול בין 1 ל-\( mid \). אחרת הוא בין \( mid + 1 \) ל-\( n \). זמן
        \( O(n \log n) \), זיכרון \( O(1) \).

    <!-- cost: זמן \( O(n \log n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    עקרון שובך היונים עובד גם על חלק מהטווח : אם יותר מ-\( mid \) מספרים נופלים בתוך \( mid \)
    הערכים \( 1, \ldots, mid \), שניים מהם שווים. ספירה אחת על כל המערך אומרת לאיזה חצי של
    הטווח ללכת, וכל צעד חוצה את הטווח.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הטווח :** \( lo = 1 \), ‏\( hi = n \).
    2. **ספירה :** \( mid \) הוא אמצע הטווח. סופרים כמה מספרים במערך הם לכל היותר \( mid \).
    3. **החלטה :** אם הספירה גדולה מ-\( mid \), הכפול בחצי התחתון, ו-\( hi = mid \). אחרת הוא
       בחצי העליון, ו-\( lo = mid + 1 \).
    4. **סוף :** כשהטווח הוא ערך אחד, זה הכפול.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function find_duplicate_binary" linenums="1" hl_lines="7 8"
        function automatic int find_duplicate_binary(const ref int nums[]);
          int lo = 1, hi = nums.size() - 1, mid, count;   // the answer is a value in lo..hi
          while (lo < hi) begin
            mid = (lo + hi) / 2;
            count = 0;
            foreach (nums[i]) if (nums[i] <= mid) count++;
            if (count > mid) hi = mid;   // (1)!
            else             lo = mid + 1;
          end
          return lo;
        endfunction
        ```

        1. יותר מ-\( mid \) מספרים בתוך \( mid \) ערכים : לפי עקרון שובך היונים יש כפול בין 1
           ל-\( mid \). חשוב : סופרים את **כל** המספרים שקטנים או שווים ל-\( mid \), ולא רק
           את אלה שבטווח \( lo..mid \).

    === "Python"
        ```python title="find_duplicate_binary" linenums="1" hl_lines="5 6"
        def find_duplicate_binary(nums: list[int]) -> int:
            lo, hi = 1, len(nums) - 1          # the answer is a value in lo..hi
            while lo < hi:
                mid = (lo + hi) // 2
                count = sum(1 for v in nums if v <= mid)   # (1)!
                if count > mid:
                    hi = mid
                else:
                    lo = mid + 1
            return lo
        ```

        1. ביטוי generator שסופר בלי לבנות רשימה, ולכן הזיכרון נשאר \( O(1) \).

    #### למה זה נכון { .sol-proof }

    **שמורה.** לאורך כל הלולאה מתקיימים שני דברים :

    - **מתחת לטווח אין עודף :** לכל היותר \( lo - 1 \) מספרים הם לכל היותר \( lo - 1 \).
    - **עד סוף הטווח יש עודף :** יותר מ-\( hi \) מספרים הם לכל היותר \( hi \).

    בהתחלה אין אף מספר שהוא לכל היותר 0, וכל \( n + 1 \) המספרים הם לכל היותר \( n \),
    ולכן השמורה מתקיימת. כל צעד שומר על אחד משני החלקים ומעדכן את הקצה השני. בסוף
    \( lo = hi \), ולכן לכל היותר \( lo - 1 \) מספרים קטנים מ-\( lo \), אבל יותר מ-\( lo \)
    מספרים הם לכל היותר \( lo \). כלומר הערך \( lo \) מופיע לפחות פעמיים.

    **על הדוגמה :**

    | הטווח | ‏\( mid \) | כמה \( \le mid \) | הכפול נמצא |
    |---|---|---|---|
    | 1 עד 9 | 5 | 6 | ‏\( 6 > 5 \) : בין 1 ל-5 |
    | 1 עד 5 | 3 | 4 | ‏\( 4 > 3 \) : בין 1 ל-3 |
    | 1 עד 3 | 2 | 3 | ‏\( 3 > 2 \) : בין 1 ל-2 |
    | 1 עד 2 | 1 | 2 | ‏\( 2 > 1 \) : הוא 1 |
    | 1 עד 1 | | | **1** |

    **נסו בעצמכם.** התיבה מריצה את החיפוש צעד אחרי צעד על אותה דוגמה. בכל צעד מודגשים במערך
    המספרים שלכל היותר \( mid \), והתרשים מראה לכל ערך \( v \) כמה מספרים הם לכל היותר
    \( v \), מול הקו \( y = v \) : עמודה מעל הקו היא עודף. הטווח \( lo \) עד \( hi \) מצטמצם כך
    שלפניו אין עודף ובסופו יש, והשורה האחרונה בודקת את השמורה בכל צעד. כשנשאר ערך אחד,
    העמודה שלו מעל הקו והעמודה שלפניו לא, ולכן הוא מופיע לפחות פעמיים.

    <div class="explorer" data-kind="dupbin" data-nmax="12"></div>

    #### סיבוכיות { .sol-cost }

    - **זמן :** \( O(n \log n) \). יש \( \log_2 n \) צעדים, וכל צעד סופר את כל המערך.
    - **זיכרון :** \( O(1) \) : ארבעה משתנים.

??? success "פתרון 4 – מעגל במערך : האלגוריתם של Floyd"
    !!! answer "תשובה בקצרה"
        רואים במערך גרף שבו כל אינדקס \( i \) מצביע על `nums[i]`. ההליכה מאינדקס 0 נכנסת
        למעגל, **ונקודת הכניסה למעגל היא הערך הכפול**. מוצאים אותה עם צב וארנב : שלב 1 עד
        שהם נפגשים, ושלב 2 מ-0 ומנקודת המפגש, צעד אחד בכל פעם. זמן \( O(n) \), זיכרון
        \( O(1) \).

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    כל אינדקס הוא צומת, ומכל צומת יוצא חץ אחד אל `nums[i]`. אף ערך אינו 0, ולכן אף חץ לא
    נכנס לצומת 0, ומשם מתחילים. ההליכה מ-0 לא יכולה להימשך לנצח בלי לחזור על צומת, ולכן
    היא נכנסת למעגל. לצומת הכניסה נכנסים **שני** חצים : אחד מהזנב שהוביל אליו, ואחד מהמעגל
    עצמו. שני חצים שנכנסים לצומת \( v \) הם שני אינדקסים שונים שהערך בשניהם \( v \), כלומר
    \( v \) כפול.

    בדוגמה : הזנב הוא 0, 3 ו-6, המעגל הוא 1, 9, 4 ו-7, ושני החצים הכתומים נכנסים ל-1. המעגל 2,
    5 ו-8 בצד לא מחובר להליכה מ-0, ולכן הוא לא משנה כלום :

    <svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו : זנב, מעגל, ומעגל נפרד"><defs><marker id="q17a-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q17a-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="59.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17a-ink)"><title>nums[0] = 3</title></line><line class="ink-line" x1="293.4" y1="76.6" x2="334.4" y2="35.6" stroke-width="2.2" marker-end="url(#q17a-ink)"><title>nums[1] = 9</title></line><g class="st-faded"><line class="ink-line" x1="100.5" y1="206.5" x2="86.4" y2="230.9" stroke-width="2.2" marker-end="url(#q17a-ink)"><title>nums[2] = 5</title></line></g><line class="ink-line" x1="139.0" y1="90.0" x2="178.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17a-ink)"><title>nums[3] = 6</title></line><line class="ink-line" x1="406.6" y1="103.4" x2="365.6" y2="144.4" stroke-width="2.2" marker-end="url(#q17a-ink)"><title>nums[4] = 7</title></line><g class="st-faded"><line class="ink-line" x1="94.4" y1="250.0" x2="122.6" y2="250.0" stroke-width="2.2" marker-end="url(#q17a-ink)"><title>nums[5] = 8</title></line></g><line class="s2-line" x1="219.0" y1="90.0" x2="258.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17a-s2)"><title>nums[6] = 1</title></line><line class="s2-line" x1="336.6" y1="146.6" x2="295.6" y2="105.6" stroke-width="2.2" marker-end="url(#q17a-s2)"><title>nums[7] = 1</title></line><g class="st-faded"><line class="ink-line" x1="135.1" y1="233.5" x2="121.0" y2="209.1" stroke-width="2.2" marker-end="url(#q17a-ink)"><title>nums[8] = 2</title></line></g><line class="ink-line" x1="363.4" y1="33.4" x2="404.4" y2="74.4" stroke-width="2.2" marker-end="url(#q17a-ink)"><title>nums[9] = 4</title></line><g><circle class="st-cell" cx="40.0" cy="90.0" r="17"/><text class="st-text" x="40.0" y="95.0" text-anchor="middle">0</text></g><g><circle class="st-cell" cx="120.0" cy="90.0" r="17"/><text class="st-text" x="120.0" y="95.0" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="200.0" cy="90.0" r="17"/><text class="st-text" x="200.0" y="95.0" text-anchor="middle">6</text></g><g><circle class="st-ok" cx="280.0" cy="90.0" r="17"/><text class="st-text" x="280.0" y="95.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="350.0" cy="20.0" r="17"/><text class="st-text" x="350.0" y="25.0" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="420.0" cy="90.0" r="17"/><text class="st-text" x="420.0" y="95.0" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="350.0" cy="160.0" r="17"/><text class="st-text" x="350.0" y="165.0" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-cell" cx="110.0" cy="190.0" r="17"/><text class="st-text" x="110.0" y="195.0" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-cell" cx="75.4" cy="250.0" r="17"/><text class="st-text" x="75.4" y="255.0" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-cell" cx="144.6" cy="250.0" r="17"/><text class="st-text" x="144.6" y="255.0" text-anchor="middle">8</text></g></svg>

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **התחלה :** הצב והארנב באינדקס 0.
    2. **שלב 1, מפגש :** בכל צעד הצב עושה צעד אחד, `slow = nums[slow]`, והארנב שני צעדים.
       ממשיכים עד שהם באותו צומת. זה קורה בתוך המעגל.
    3. **שלב 2, כניסה :** מחזירים את הצב ל-0, משאירים את הארנב בנקודת המפגש, ומעכשיו שניהם
       עושים צעד אחד בכל פעם.
    4. **התשובה :** הצומת שבו הם נפגשים הוא הכניסה למעגל, כלומר הערך הכפול.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function find_duplicate_floyd" linenums="1" hl_lines="5 9 10"
        function automatic int find_duplicate_floyd(const ref int nums[]);
          int slow = 0, fast = 0;
          do begin                     // phase 1: meet inside the cycle
            slow = nums[slow];
            fast = nums[nums[fast]];   // (1)!
          end while (slow != fast);
          slow = 0;   // (2)!
          while (slow != fast) begin
            slow = nums[slow];
            fast = nums[fast];
          end
          return slow;                 // the entry of the cycle = the duplicate value
        endfunction
        ```

        1. הארנב עושה שני צעדים בכל איטרציה. ‏`do ... while` ולא `while` : בהתחלה שניהם ב-0,
           ולולאת `while` רגילה לא הייתה נכנסת בכלל.
        2. שלב 2 : הצב חוזר להתחלה, הארנב נשאר בנקודת המפגש, ומעכשיו שניהם צועדים צעד אחד. הם
           נפגשים בדיוק בכניסה למעגל, וההוכחה למטה.

    === "Python"
        ```python title="find_duplicate_floyd" linenums="1" hl_lines="5 10 11"
        def find_duplicate_floyd(nums: list[int]) -> int:
            slow = fast = 0
            while True:                   # phase 1: meet inside the cycle (1)
                slow = nums[slow]
                fast = nums[nums[fast]]   # two steps
                if slow == fast:
                    break
            slow = 0                      # phase 2: back to the start, one step each
            while slow != fast:
                slow = nums[slow]
                fast = nums[fast]
            return slow                   # the entry of the cycle = the duplicate value
        ```

        1. ל-Python אין `do ... while`, ולכן `while True` עם `break` אחרי הצעד : גם כאן הצעד
           הראשון קורה לפני הבדיקה, כי בהתחלה שניהם ב-0.

    #### למה זה נכון { .sol-proof }

    **צעד אחרי צעד.** לחצו "הבא" כדי לעקוב אחרי שני השלבים על הדוגמה :

    <span class="viz-legend"><span><i class="fl-slow"></i>הצב : צעד אחד בכל פעם</span><span><i class="fl-fast"></i>הארנב : שני צעדים בכל פעם</span><span><i class="s3"></i>הכניסה למעגל, הערך הכפול</span></span>

    <div class="stepper" role="group" aria-label="האלגוריתם של Floyd על הדוגמה : שלב המפגש ושלב הכניסה למעגל" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו : זנב, מעגל, ומעגל נפרד"><defs><marker id="q17s0-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q17s0-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="59.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s0-ink)"><title>nums[0] = 3</title></line><line class="ink-line" x1="293.4" y1="76.6" x2="334.4" y2="35.6" stroke-width="2.2" marker-end="url(#q17s0-ink)"><title>nums[1] = 9</title></line><g class="st-faded"><line class="ink-line" x1="100.5" y1="206.5" x2="86.4" y2="230.9" stroke-width="2.2" marker-end="url(#q17s0-ink)"><title>nums[2] = 5</title></line></g><line class="ink-line" x1="139.0" y1="90.0" x2="178.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s0-ink)"><title>nums[3] = 6</title></line><line class="ink-line" x1="406.6" y1="103.4" x2="365.6" y2="144.4" stroke-width="2.2" marker-end="url(#q17s0-ink)"><title>nums[4] = 7</title></line><g class="st-faded"><line class="ink-line" x1="94.4" y1="250.0" x2="122.6" y2="250.0" stroke-width="2.2" marker-end="url(#q17s0-ink)"><title>nums[5] = 8</title></line></g><line class="ink-line" x1="219.0" y1="90.0" x2="258.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s0-ink)"><title>nums[6] = 1</title></line><line class="ink-line" x1="336.6" y1="146.6" x2="295.6" y2="105.6" stroke-width="2.2" marker-end="url(#q17s0-ink)"><title>nums[7] = 1</title></line><g class="st-faded"><line class="ink-line" x1="135.1" y1="233.5" x2="121.0" y2="209.1" stroke-width="2.2" marker-end="url(#q17s0-ink)"><title>nums[8] = 2</title></line></g><line class="ink-line" x1="363.4" y1="33.4" x2="404.4" y2="74.4" stroke-width="2.2" marker-end="url(#q17s0-ink)"><title>nums[9] = 4</title></line><g><circle class="st-cell" cx="40.0" cy="90.0" r="17"/><text class="st-text" x="40.0" y="95.0" text-anchor="middle">0</text></g><g><circle class="st-cell" cx="120.0" cy="90.0" r="17"/><text class="st-text" x="120.0" y="95.0" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="200.0" cy="90.0" r="17"/><text class="st-text" x="200.0" y="95.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="280.0" cy="90.0" r="17"/><text class="st-text" x="280.0" y="95.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="350.0" cy="20.0" r="17"/><text class="st-text" x="350.0" y="25.0" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="420.0" cy="90.0" r="17"/><text class="st-text" x="420.0" y="95.0" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="350.0" cy="160.0" r="17"/><text class="st-text" x="350.0" y="165.0" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-cell" cx="110.0" cy="190.0" r="17"/><text class="st-text" x="110.0" y="195.0" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-cell" cx="75.4" cy="250.0" r="17"/><text class="st-text" x="75.4" y="255.0" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-cell" cx="144.6" cy="250.0" r="17"/><text class="st-text" x="144.6" y="255.0" text-anchor="middle">8</text></g><circle class="fl-slow" cx="40.0" cy="90.0" r="22"/><circle class="fl-fast" cx="40.0" cy="90.0" r="27"/></svg><figcaption>שלב 1 : הצב והארנב מתחילים באינדקס 0, שאף ערך לא מצביע עליו.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו : זנב, מעגל, ומעגל נפרד"><defs><marker id="q17s1-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q17s1-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="59.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s1-ink)"><title>nums[0] = 3</title></line><line class="ink-line" x1="293.4" y1="76.6" x2="334.4" y2="35.6" stroke-width="2.2" marker-end="url(#q17s1-ink)"><title>nums[1] = 9</title></line><g class="st-faded"><line class="ink-line" x1="100.5" y1="206.5" x2="86.4" y2="230.9" stroke-width="2.2" marker-end="url(#q17s1-ink)"><title>nums[2] = 5</title></line></g><line class="ink-line" x1="139.0" y1="90.0" x2="178.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s1-ink)"><title>nums[3] = 6</title></line><line class="ink-line" x1="406.6" y1="103.4" x2="365.6" y2="144.4" stroke-width="2.2" marker-end="url(#q17s1-ink)"><title>nums[4] = 7</title></line><g class="st-faded"><line class="ink-line" x1="94.4" y1="250.0" x2="122.6" y2="250.0" stroke-width="2.2" marker-end="url(#q17s1-ink)"><title>nums[5] = 8</title></line></g><line class="ink-line" x1="219.0" y1="90.0" x2="258.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s1-ink)"><title>nums[6] = 1</title></line><line class="ink-line" x1="336.6" y1="146.6" x2="295.6" y2="105.6" stroke-width="2.2" marker-end="url(#q17s1-ink)"><title>nums[7] = 1</title></line><g class="st-faded"><line class="ink-line" x1="135.1" y1="233.5" x2="121.0" y2="209.1" stroke-width="2.2" marker-end="url(#q17s1-ink)"><title>nums[8] = 2</title></line></g><line class="ink-line" x1="363.4" y1="33.4" x2="404.4" y2="74.4" stroke-width="2.2" marker-end="url(#q17s1-ink)"><title>nums[9] = 4</title></line><g><circle class="st-cell" cx="40.0" cy="90.0" r="17"/><text class="st-text" x="40.0" y="95.0" text-anchor="middle">0</text></g><g><circle class="st-cell" cx="120.0" cy="90.0" r="17"/><text class="st-text" x="120.0" y="95.0" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="200.0" cy="90.0" r="17"/><text class="st-text" x="200.0" y="95.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="280.0" cy="90.0" r="17"/><text class="st-text" x="280.0" y="95.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="350.0" cy="20.0" r="17"/><text class="st-text" x="350.0" y="25.0" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="420.0" cy="90.0" r="17"/><text class="st-text" x="420.0" y="95.0" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="350.0" cy="160.0" r="17"/><text class="st-text" x="350.0" y="165.0" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-cell" cx="110.0" cy="190.0" r="17"/><text class="st-text" x="110.0" y="195.0" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-cell" cx="75.4" cy="250.0" r="17"/><text class="st-text" x="75.4" y="255.0" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-cell" cx="144.6" cy="250.0" r="17"/><text class="st-text" x="144.6" y="255.0" text-anchor="middle">8</text></g><circle class="fl-slow" cx="120.0" cy="90.0" r="22"/><circle class="fl-fast" cx="200.0" cy="90.0" r="27"/></svg><figcaption>שלב 1, איטרציה 1 : הצב מתקדם צעד אחד ל-3, והארנב שני צעדים ל-6.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו : זנב, מעגל, ומעגל נפרד"><defs><marker id="q17s2-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q17s2-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="59.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s2-ink)"><title>nums[0] = 3</title></line><line class="ink-line" x1="293.4" y1="76.6" x2="334.4" y2="35.6" stroke-width="2.2" marker-end="url(#q17s2-ink)"><title>nums[1] = 9</title></line><g class="st-faded"><line class="ink-line" x1="100.5" y1="206.5" x2="86.4" y2="230.9" stroke-width="2.2" marker-end="url(#q17s2-ink)"><title>nums[2] = 5</title></line></g><line class="ink-line" x1="139.0" y1="90.0" x2="178.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s2-ink)"><title>nums[3] = 6</title></line><line class="ink-line" x1="406.6" y1="103.4" x2="365.6" y2="144.4" stroke-width="2.2" marker-end="url(#q17s2-ink)"><title>nums[4] = 7</title></line><g class="st-faded"><line class="ink-line" x1="94.4" y1="250.0" x2="122.6" y2="250.0" stroke-width="2.2" marker-end="url(#q17s2-ink)"><title>nums[5] = 8</title></line></g><line class="ink-line" x1="219.0" y1="90.0" x2="258.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s2-ink)"><title>nums[6] = 1</title></line><line class="ink-line" x1="336.6" y1="146.6" x2="295.6" y2="105.6" stroke-width="2.2" marker-end="url(#q17s2-ink)"><title>nums[7] = 1</title></line><g class="st-faded"><line class="ink-line" x1="135.1" y1="233.5" x2="121.0" y2="209.1" stroke-width="2.2" marker-end="url(#q17s2-ink)"><title>nums[8] = 2</title></line></g><line class="ink-line" x1="363.4" y1="33.4" x2="404.4" y2="74.4" stroke-width="2.2" marker-end="url(#q17s2-ink)"><title>nums[9] = 4</title></line><g><circle class="st-cell" cx="40.0" cy="90.0" r="17"/><text class="st-text" x="40.0" y="95.0" text-anchor="middle">0</text></g><g><circle class="st-cell" cx="120.0" cy="90.0" r="17"/><text class="st-text" x="120.0" y="95.0" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="200.0" cy="90.0" r="17"/><text class="st-text" x="200.0" y="95.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="280.0" cy="90.0" r="17"/><text class="st-text" x="280.0" y="95.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="350.0" cy="20.0" r="17"/><text class="st-text" x="350.0" y="25.0" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="420.0" cy="90.0" r="17"/><text class="st-text" x="420.0" y="95.0" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="350.0" cy="160.0" r="17"/><text class="st-text" x="350.0" y="165.0" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-cell" cx="110.0" cy="190.0" r="17"/><text class="st-text" x="110.0" y="195.0" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-cell" cx="75.4" cy="250.0" r="17"/><text class="st-text" x="75.4" y="255.0" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-cell" cx="144.6" cy="250.0" r="17"/><text class="st-text" x="144.6" y="255.0" text-anchor="middle">8</text></g><circle class="fl-slow" cx="200.0" cy="90.0" r="22"/><circle class="fl-fast" cx="350.0" cy="20.0" r="27"/></svg><figcaption>שלב 1, איטרציה 2 : הצב מתקדם צעד אחד ל-6, והארנב שני צעדים ל-9.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו : זנב, מעגל, ומעגל נפרד"><defs><marker id="q17s3-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q17s3-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="59.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s3-ink)"><title>nums[0] = 3</title></line><line class="ink-line" x1="293.4" y1="76.6" x2="334.4" y2="35.6" stroke-width="2.2" marker-end="url(#q17s3-ink)"><title>nums[1] = 9</title></line><g class="st-faded"><line class="ink-line" x1="100.5" y1="206.5" x2="86.4" y2="230.9" stroke-width="2.2" marker-end="url(#q17s3-ink)"><title>nums[2] = 5</title></line></g><line class="ink-line" x1="139.0" y1="90.0" x2="178.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s3-ink)"><title>nums[3] = 6</title></line><line class="ink-line" x1="406.6" y1="103.4" x2="365.6" y2="144.4" stroke-width="2.2" marker-end="url(#q17s3-ink)"><title>nums[4] = 7</title></line><g class="st-faded"><line class="ink-line" x1="94.4" y1="250.0" x2="122.6" y2="250.0" stroke-width="2.2" marker-end="url(#q17s3-ink)"><title>nums[5] = 8</title></line></g><line class="ink-line" x1="219.0" y1="90.0" x2="258.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s3-ink)"><title>nums[6] = 1</title></line><line class="ink-line" x1="336.6" y1="146.6" x2="295.6" y2="105.6" stroke-width="2.2" marker-end="url(#q17s3-ink)"><title>nums[7] = 1</title></line><g class="st-faded"><line class="ink-line" x1="135.1" y1="233.5" x2="121.0" y2="209.1" stroke-width="2.2" marker-end="url(#q17s3-ink)"><title>nums[8] = 2</title></line></g><line class="ink-line" x1="363.4" y1="33.4" x2="404.4" y2="74.4" stroke-width="2.2" marker-end="url(#q17s3-ink)"><title>nums[9] = 4</title></line><g><circle class="st-cell" cx="40.0" cy="90.0" r="17"/><text class="st-text" x="40.0" y="95.0" text-anchor="middle">0</text></g><g><circle class="st-cell" cx="120.0" cy="90.0" r="17"/><text class="st-text" x="120.0" y="95.0" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="200.0" cy="90.0" r="17"/><text class="st-text" x="200.0" y="95.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="280.0" cy="90.0" r="17"/><text class="st-text" x="280.0" y="95.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="350.0" cy="20.0" r="17"/><text class="st-text" x="350.0" y="25.0" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="420.0" cy="90.0" r="17"/><text class="st-text" x="420.0" y="95.0" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="350.0" cy="160.0" r="17"/><text class="st-text" x="350.0" y="165.0" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-cell" cx="110.0" cy="190.0" r="17"/><text class="st-text" x="110.0" y="195.0" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-cell" cx="75.4" cy="250.0" r="17"/><text class="st-text" x="75.4" y="255.0" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-cell" cx="144.6" cy="250.0" r="17"/><text class="st-text" x="144.6" y="255.0" text-anchor="middle">8</text></g><circle class="fl-slow" cx="280.0" cy="90.0" r="22"/><circle class="fl-fast" cx="350.0" cy="160.0" r="27"/></svg><figcaption>שלב 1, איטרציה 3 : הצב מתקדם צעד אחד ל-1, והארנב שני צעדים ל-7.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו : זנב, מעגל, ומעגל נפרד"><defs><marker id="q17s4-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q17s4-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="59.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s4-ink)"><title>nums[0] = 3</title></line><line class="ink-line" x1="293.4" y1="76.6" x2="334.4" y2="35.6" stroke-width="2.2" marker-end="url(#q17s4-ink)"><title>nums[1] = 9</title></line><g class="st-faded"><line class="ink-line" x1="100.5" y1="206.5" x2="86.4" y2="230.9" stroke-width="2.2" marker-end="url(#q17s4-ink)"><title>nums[2] = 5</title></line></g><line class="ink-line" x1="139.0" y1="90.0" x2="178.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s4-ink)"><title>nums[3] = 6</title></line><line class="ink-line" x1="406.6" y1="103.4" x2="365.6" y2="144.4" stroke-width="2.2" marker-end="url(#q17s4-ink)"><title>nums[4] = 7</title></line><g class="st-faded"><line class="ink-line" x1="94.4" y1="250.0" x2="122.6" y2="250.0" stroke-width="2.2" marker-end="url(#q17s4-ink)"><title>nums[5] = 8</title></line></g><line class="ink-line" x1="219.0" y1="90.0" x2="258.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s4-ink)"><title>nums[6] = 1</title></line><line class="ink-line" x1="336.6" y1="146.6" x2="295.6" y2="105.6" stroke-width="2.2" marker-end="url(#q17s4-ink)"><title>nums[7] = 1</title></line><g class="st-faded"><line class="ink-line" x1="135.1" y1="233.5" x2="121.0" y2="209.1" stroke-width="2.2" marker-end="url(#q17s4-ink)"><title>nums[8] = 2</title></line></g><line class="ink-line" x1="363.4" y1="33.4" x2="404.4" y2="74.4" stroke-width="2.2" marker-end="url(#q17s4-ink)"><title>nums[9] = 4</title></line><g><circle class="st-cell" cx="40.0" cy="90.0" r="17"/><text class="st-text" x="40.0" y="95.0" text-anchor="middle">0</text></g><g><circle class="st-cell" cx="120.0" cy="90.0" r="17"/><text class="st-text" x="120.0" y="95.0" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="200.0" cy="90.0" r="17"/><text class="st-text" x="200.0" y="95.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="280.0" cy="90.0" r="17"/><text class="st-text" x="280.0" y="95.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="350.0" cy="20.0" r="17"/><text class="st-text" x="350.0" y="25.0" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="420.0" cy="90.0" r="17"/><text class="st-text" x="420.0" y="95.0" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="350.0" cy="160.0" r="17"/><text class="st-text" x="350.0" y="165.0" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-cell" cx="110.0" cy="190.0" r="17"/><text class="st-text" x="110.0" y="195.0" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-cell" cx="75.4" cy="250.0" r="17"/><text class="st-text" x="75.4" y="255.0" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-cell" cx="144.6" cy="250.0" r="17"/><text class="st-text" x="144.6" y="255.0" text-anchor="middle">8</text></g><circle class="fl-slow" cx="350.0" cy="20.0" r="22"/><circle class="fl-fast" cx="350.0" cy="20.0" r="27"/></svg><figcaption>שלב 1, איטרציה 4 : שניהם ב-9. נפגשו בתוך המעגל, ומספר האיטרציות 4 הוא כפולה של אורך המעגל.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו : זנב, מעגל, ומעגל נפרד"><defs><marker id="q17s5-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q17s5-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="59.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s5-ink)"><title>nums[0] = 3</title></line><line class="ink-line" x1="293.4" y1="76.6" x2="334.4" y2="35.6" stroke-width="2.2" marker-end="url(#q17s5-ink)"><title>nums[1] = 9</title></line><g class="st-faded"><line class="ink-line" x1="100.5" y1="206.5" x2="86.4" y2="230.9" stroke-width="2.2" marker-end="url(#q17s5-ink)"><title>nums[2] = 5</title></line></g><line class="ink-line" x1="139.0" y1="90.0" x2="178.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s5-ink)"><title>nums[3] = 6</title></line><line class="ink-line" x1="406.6" y1="103.4" x2="365.6" y2="144.4" stroke-width="2.2" marker-end="url(#q17s5-ink)"><title>nums[4] = 7</title></line><g class="st-faded"><line class="ink-line" x1="94.4" y1="250.0" x2="122.6" y2="250.0" stroke-width="2.2" marker-end="url(#q17s5-ink)"><title>nums[5] = 8</title></line></g><line class="ink-line" x1="219.0" y1="90.0" x2="258.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s5-ink)"><title>nums[6] = 1</title></line><line class="ink-line" x1="336.6" y1="146.6" x2="295.6" y2="105.6" stroke-width="2.2" marker-end="url(#q17s5-ink)"><title>nums[7] = 1</title></line><g class="st-faded"><line class="ink-line" x1="135.1" y1="233.5" x2="121.0" y2="209.1" stroke-width="2.2" marker-end="url(#q17s5-ink)"><title>nums[8] = 2</title></line></g><line class="ink-line" x1="363.4" y1="33.4" x2="404.4" y2="74.4" stroke-width="2.2" marker-end="url(#q17s5-ink)"><title>nums[9] = 4</title></line><g><circle class="st-cell" cx="40.0" cy="90.0" r="17"/><text class="st-text" x="40.0" y="95.0" text-anchor="middle">0</text></g><g><circle class="st-cell" cx="120.0" cy="90.0" r="17"/><text class="st-text" x="120.0" y="95.0" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="200.0" cy="90.0" r="17"/><text class="st-text" x="200.0" y="95.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="280.0" cy="90.0" r="17"/><text class="st-text" x="280.0" y="95.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="350.0" cy="20.0" r="17"/><text class="st-text" x="350.0" y="25.0" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="420.0" cy="90.0" r="17"/><text class="st-text" x="420.0" y="95.0" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="350.0" cy="160.0" r="17"/><text class="st-text" x="350.0" y="165.0" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-cell" cx="110.0" cy="190.0" r="17"/><text class="st-text" x="110.0" y="195.0" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-cell" cx="75.4" cy="250.0" r="17"/><text class="st-text" x="75.4" y="255.0" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-cell" cx="144.6" cy="250.0" r="17"/><text class="st-text" x="144.6" y="255.0" text-anchor="middle">8</text></g><circle class="fl-slow" cx="40.0" cy="90.0" r="22"/><circle class="fl-fast" cx="350.0" cy="20.0" r="27"/></svg><figcaption>שלב 2 : מחזירים את הצב ל-0. הארנב נשאר בנקודת המפגש 9, ומעכשיו שניהם צועדים צעד אחד.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו : זנב, מעגל, ומעגל נפרד"><defs><marker id="q17s6-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q17s6-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="59.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s6-ink)"><title>nums[0] = 3</title></line><line class="ink-line" x1="293.4" y1="76.6" x2="334.4" y2="35.6" stroke-width="2.2" marker-end="url(#q17s6-ink)"><title>nums[1] = 9</title></line><g class="st-faded"><line class="ink-line" x1="100.5" y1="206.5" x2="86.4" y2="230.9" stroke-width="2.2" marker-end="url(#q17s6-ink)"><title>nums[2] = 5</title></line></g><line class="ink-line" x1="139.0" y1="90.0" x2="178.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s6-ink)"><title>nums[3] = 6</title></line><line class="ink-line" x1="406.6" y1="103.4" x2="365.6" y2="144.4" stroke-width="2.2" marker-end="url(#q17s6-ink)"><title>nums[4] = 7</title></line><g class="st-faded"><line class="ink-line" x1="94.4" y1="250.0" x2="122.6" y2="250.0" stroke-width="2.2" marker-end="url(#q17s6-ink)"><title>nums[5] = 8</title></line></g><line class="ink-line" x1="219.0" y1="90.0" x2="258.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s6-ink)"><title>nums[6] = 1</title></line><line class="ink-line" x1="336.6" y1="146.6" x2="295.6" y2="105.6" stroke-width="2.2" marker-end="url(#q17s6-ink)"><title>nums[7] = 1</title></line><g class="st-faded"><line class="ink-line" x1="135.1" y1="233.5" x2="121.0" y2="209.1" stroke-width="2.2" marker-end="url(#q17s6-ink)"><title>nums[8] = 2</title></line></g><line class="ink-line" x1="363.4" y1="33.4" x2="404.4" y2="74.4" stroke-width="2.2" marker-end="url(#q17s6-ink)"><title>nums[9] = 4</title></line><g><circle class="st-cell" cx="40.0" cy="90.0" r="17"/><text class="st-text" x="40.0" y="95.0" text-anchor="middle">0</text></g><g><circle class="st-cell" cx="120.0" cy="90.0" r="17"/><text class="st-text" x="120.0" y="95.0" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="200.0" cy="90.0" r="17"/><text class="st-text" x="200.0" y="95.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="280.0" cy="90.0" r="17"/><text class="st-text" x="280.0" y="95.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="350.0" cy="20.0" r="17"/><text class="st-text" x="350.0" y="25.0" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="420.0" cy="90.0" r="17"/><text class="st-text" x="420.0" y="95.0" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="350.0" cy="160.0" r="17"/><text class="st-text" x="350.0" y="165.0" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-cell" cx="110.0" cy="190.0" r="17"/><text class="st-text" x="110.0" y="195.0" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-cell" cx="75.4" cy="250.0" r="17"/><text class="st-text" x="75.4" y="255.0" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-cell" cx="144.6" cy="250.0" r="17"/><text class="st-text" x="144.6" y="255.0" text-anchor="middle">8</text></g><circle class="fl-slow" cx="120.0" cy="90.0" r="22"/><circle class="fl-fast" cx="420.0" cy="90.0" r="27"/></svg><figcaption>שלב 2, איטרציה 1 : הצב ב-3, הארנב ב-4.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו : זנב, מעגל, ומעגל נפרד"><defs><marker id="q17s7-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q17s7-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="59.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s7-ink)"><title>nums[0] = 3</title></line><line class="ink-line" x1="293.4" y1="76.6" x2="334.4" y2="35.6" stroke-width="2.2" marker-end="url(#q17s7-ink)"><title>nums[1] = 9</title></line><g class="st-faded"><line class="ink-line" x1="100.5" y1="206.5" x2="86.4" y2="230.9" stroke-width="2.2" marker-end="url(#q17s7-ink)"><title>nums[2] = 5</title></line></g><line class="ink-line" x1="139.0" y1="90.0" x2="178.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s7-ink)"><title>nums[3] = 6</title></line><line class="ink-line" x1="406.6" y1="103.4" x2="365.6" y2="144.4" stroke-width="2.2" marker-end="url(#q17s7-ink)"><title>nums[4] = 7</title></line><g class="st-faded"><line class="ink-line" x1="94.4" y1="250.0" x2="122.6" y2="250.0" stroke-width="2.2" marker-end="url(#q17s7-ink)"><title>nums[5] = 8</title></line></g><line class="ink-line" x1="219.0" y1="90.0" x2="258.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s7-ink)"><title>nums[6] = 1</title></line><line class="ink-line" x1="336.6" y1="146.6" x2="295.6" y2="105.6" stroke-width="2.2" marker-end="url(#q17s7-ink)"><title>nums[7] = 1</title></line><g class="st-faded"><line class="ink-line" x1="135.1" y1="233.5" x2="121.0" y2="209.1" stroke-width="2.2" marker-end="url(#q17s7-ink)"><title>nums[8] = 2</title></line></g><line class="ink-line" x1="363.4" y1="33.4" x2="404.4" y2="74.4" stroke-width="2.2" marker-end="url(#q17s7-ink)"><title>nums[9] = 4</title></line><g><circle class="st-cell" cx="40.0" cy="90.0" r="17"/><text class="st-text" x="40.0" y="95.0" text-anchor="middle">0</text></g><g><circle class="st-cell" cx="120.0" cy="90.0" r="17"/><text class="st-text" x="120.0" y="95.0" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="200.0" cy="90.0" r="17"/><text class="st-text" x="200.0" y="95.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="280.0" cy="90.0" r="17"/><text class="st-text" x="280.0" y="95.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="350.0" cy="20.0" r="17"/><text class="st-text" x="350.0" y="25.0" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="420.0" cy="90.0" r="17"/><text class="st-text" x="420.0" y="95.0" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="350.0" cy="160.0" r="17"/><text class="st-text" x="350.0" y="165.0" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-cell" cx="110.0" cy="190.0" r="17"/><text class="st-text" x="110.0" y="195.0" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-cell" cx="75.4" cy="250.0" r="17"/><text class="st-text" x="75.4" y="255.0" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-cell" cx="144.6" cy="250.0" r="17"/><text class="st-text" x="144.6" y="255.0" text-anchor="middle">8</text></g><circle class="fl-slow" cx="200.0" cy="90.0" r="22"/><circle class="fl-fast" cx="350.0" cy="160.0" r="27"/></svg><figcaption>שלב 2, איטרציה 2 : הצב ב-6, הארנב ב-7.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו : זנב, מעגל, ומעגל נפרד"><defs><marker id="q17s8-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q17s8-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="59.0" y1="90.0" x2="98.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s8-ink)"><title>nums[0] = 3</title></line><line class="ink-line" x1="293.4" y1="76.6" x2="334.4" y2="35.6" stroke-width="2.2" marker-end="url(#q17s8-ink)"><title>nums[1] = 9</title></line><g class="st-faded"><line class="ink-line" x1="100.5" y1="206.5" x2="86.4" y2="230.9" stroke-width="2.2" marker-end="url(#q17s8-ink)"><title>nums[2] = 5</title></line></g><line class="ink-line" x1="139.0" y1="90.0" x2="178.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s8-ink)"><title>nums[3] = 6</title></line><line class="ink-line" x1="406.6" y1="103.4" x2="365.6" y2="144.4" stroke-width="2.2" marker-end="url(#q17s8-ink)"><title>nums[4] = 7</title></line><g class="st-faded"><line class="ink-line" x1="94.4" y1="250.0" x2="122.6" y2="250.0" stroke-width="2.2" marker-end="url(#q17s8-ink)"><title>nums[5] = 8</title></line></g><line class="s2-line" x1="219.0" y1="90.0" x2="258.0" y2="90.0" stroke-width="2.2" marker-end="url(#q17s8-s2)"><title>nums[6] = 1</title></line><line class="s2-line" x1="336.6" y1="146.6" x2="295.6" y2="105.6" stroke-width="2.2" marker-end="url(#q17s8-s2)"><title>nums[7] = 1</title></line><g class="st-faded"><line class="ink-line" x1="135.1" y1="233.5" x2="121.0" y2="209.1" stroke-width="2.2" marker-end="url(#q17s8-ink)"><title>nums[8] = 2</title></line></g><line class="ink-line" x1="363.4" y1="33.4" x2="404.4" y2="74.4" stroke-width="2.2" marker-end="url(#q17s8-ink)"><title>nums[9] = 4</title></line><g><circle class="st-cell" cx="40.0" cy="90.0" r="17"/><text class="st-text" x="40.0" y="95.0" text-anchor="middle">0</text></g><g><circle class="st-cell" cx="120.0" cy="90.0" r="17"/><text class="st-text" x="120.0" y="95.0" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="200.0" cy="90.0" r="17"/><text class="st-text" x="200.0" y="95.0" text-anchor="middle">6</text></g><g><circle class="st-ok" cx="280.0" cy="90.0" r="17"/><text class="st-text" x="280.0" y="95.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="350.0" cy="20.0" r="17"/><text class="st-text" x="350.0" y="25.0" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="420.0" cy="90.0" r="17"/><text class="st-text" x="420.0" y="95.0" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="350.0" cy="160.0" r="17"/><text class="st-text" x="350.0" y="165.0" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-cell" cx="110.0" cy="190.0" r="17"/><text class="st-text" x="110.0" y="195.0" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-cell" cx="75.4" cy="250.0" r="17"/><text class="st-text" x="75.4" y="255.0" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-cell" cx="144.6" cy="250.0" r="17"/><text class="st-text" x="144.6" y="255.0" text-anchor="middle">8</text></g><circle class="fl-slow" cx="280.0" cy="90.0" r="22"/><circle class="fl-fast" cx="280.0" cy="90.0" r="27"/></svg><figcaption>שלב 2, איטרציה 3 : שניהם ב-1, הכניסה למעגל. שני חצים נכנסים אליה, מאינדקס 6 ומאינדקס 7, ולכן 1 הוא הערך הכפול.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="9"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    **נסו בעצמכם.** הגרילו מערך או הקלידו אחד (\( n + 1 \) מספרים בין 1 ל-\( n \)) : התיבה
    מציירת אותו כגרף של זנב ומעגל, ומריצה את הצב והארנב צעד אחרי צעד דרך שני השלבים. בסוף
    החצים שנכנסים לכניסה למעגל נצבעים בכתום, והם בדיוק האינדקסים שמחזיקים את הערך הכפול.
    "העתקת קישור" נותן קישור שפותח את התיבה עם אותו מערך באותו צעד.

    <div class="explorer" data-kind="floyd" data-nmax="12"></div>

    **ההוכחה.** נסמן ב-\( x_t \) את הצומת אחרי \( t \) צעדים מ-0, ב-\( \mu \) את אורך הזנב
    (מספר הצעדים עד הכניסה למעגל), וב-\( \lambda \) את אורך המעגל. בדוגמה
    \( \mu = 3 \) ו-\( \lambda = 4 \).

    - **שלב 1 נגמר :** אחרי \( t \) צעדים הצב ב-\( x_t \) והארנב ב-\( x_{2t} \). כש-\( t \ge \mu \)
      שניהם במעגל, והמרחק ביניהם לאורך המעגל קטן ב-1 בכל צעד. לכן הם נפגשים לכל היותר
      אחרי \( \mu + \lambda \) צעדים.
    - **מה ידוע בנקודת המפגש :** \( x_t = x_{2t} \) כשהשניים במעגל, ולכן ההפרש \( 2t - t = t \)
      הוא כפולה של \( \lambda \). בדוגמה \( t = 4 \).
    - **שלב 2 :** אחרי \( \mu \) צעדים נוספים הצב ב-\( x_\mu \), הכניסה. הארנב ב-\( x_{t + \mu} \),
      שהוא \( x_\mu \) ועוד \( t \) צעדים, כלומר מספר שלם של סיבובים, ולכן גם הוא בכניסה.
    - **ולא לפני :** לפני \( \mu \) צעדים הצב עדיין בזנב, והארנב כל הזמן במעגל, ולכן הם לא
      יכולים להיפגש מוקדם יותר. המפגש הראשון הוא בדיוק בכניסה.

    #### סיבוכיות { .sol-cost }

    - **זמן :** \( O(n) \). שלב 1 לוקח לכל היותר \( \mu + \lambda \le n + 1 \) צעדים, ושלב 2
      לוקח \( \mu \) צעדים.
    - **זיכרון :** \( O(1) \) : שני מצביעים.

    **ארבעת הפתרונות :**

    | פתרון | זמן | זיכרון נוסף | משנה את המערך? |
    |---|---|---|---|
    | מיון של עותק | ‏\( O(n \log n) \) | ‏\( O(n) \) | לא, ובמיון במקום : כן |
    | טבלת סימונים | ‏\( O(n) \) | ‏\( O(n) \) | לא |
    | חיפוש בינארי על הערכים | ‏\( O(n \log n) \) | ‏\( O(1) \) | לא |
    | ‏Floyd | ‏\( O(n) \) | ‏\( O(1) \) | לא |

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : XOR או סכום"
    טריק מוכר הוא לחשב את סכום המערך פחות \( 1 + 2 + \cdots + n \), או XOR של הכל. זה עובד
    רק כשהערך הכפול מופיע **בדיוק פעמיים** וכל שאר הערכים מופיעים פעם אחת. בשאלה הזו ערך
    יכול להופיע שלוש פעמים, ואז ערכים אחרים חסרים, והטריק נותן תשובה שגויה. למשל, במערך
    ‏`[2, 2, 2, 1]` עם \( n = 3 \) הסכום הוא 7, ‏\( 1 + 2 + 3 = 6 \), וההפרש 1 אינו הכפול.

??? trap "מלכודת : להתחיל את Floyd מהמקום הלא נכון"
    מתחילים מאינדקס 0 כי אף חץ לא נכנס אליו, ולכן הוא בוודאות בזנב ולא בתוך מעגל. אם
    מתחילים מצומת שנמצא בתוך מעגל, למשל מאינדקס 2 בדוגמה, אין זנב ואין כניסה, ושלב 2 מחזיר
    צומת שאינו בהכרח כפול.

??? trap "מלכודת : חיפוש בינארי על האינדקסים"
    המערך לא ממוין, ולכן חיפוש בינארי על המקומות בו לא אומר כלום. החיפוש הוא על **טווח
    הערכים** 1 עד \( n \), ובכל צעד סופרים את כל המערך מחדש.

??? followup "שאלות המשך"
    - **הקשר לשאלה 0009 :** שם כל קופסה מצביעה על הפתק שבה, והתמורה מתפרקת למעגלים בלי
      זנבות. מה שונה כאן, ולמה דווקא הכפול יוצר זנב?
    - **רשימה מקושרת :** בהינתן ראש של רשימה מקושרת, איך יודעים אם יש בה מעגל, ואיך מוצאים
      את אורכו? (אותו צב וארנב.)
    - **כל הכפולים :** אם מותר לשנות את המערך, אפשר למצוא את **כל** הכפולים בזמן \( O(n) \)
      ובזיכרון \( O(1) \), על ידי היפוך סימן במקום `abs(v)`. איך?
    - **בחומרה :** זרם של \( n + 1 \) ערכים מגיע ערך אחד בכל מחזור שעון, ואסור לשמור אותו.
      כמה ביטים של זיכרון צריך כדי למצוא כפול, ואם מותר לקרוא את הזרם כמה פעמים?
