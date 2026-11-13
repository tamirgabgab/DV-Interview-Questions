---
id: 108
title: היפוך של k ביטים רצופים – כמה היפוכים עד שכל הביטים 1
level: junior
difficulty: medium
kind: code
tags: [algorithms, greedy, bitwise, python, systemverilog]
source: "LeetCode 995 (Minimum Number of K Consecutive Bit Flips) : סעיף א הוא השאלה, וסעיף ב מכליל ללוח"
added: 2026-11-13
---

## השאלה

נתון מערך של \( n \) ביטים, \( a \), וביט 0 הוא השמאלי. בצעד אחד בוחרים חלון של \( k \) ביטים
רצופים ומהפכים את כולם : כל 0 בחלון הופך ל-1, וכל 1 ל-0. מה המספר הקטן ביותר של צעדים שאחריו
כל הביטים 1? אם אין דרך כזו, מחזירים ‏−1.

**הדוגמה :** ב-<span dir="ltr">a = 00010110</span> עם \( k = 3 \) התשובה 3 : הופכים את החלונות
שמתחילים בביטים 0, 4 ו-5. ב-<span dir="ltr">a = 010</span> עם \( k = 1 \) התשובה 2, וב-<span dir="ltr">a = 110</span>
עם \( k = 2 \) התשובה ‏−1.

**ההקשר באימות :** רגיסטר של \( n \) ביטים שאפשר לכתוב אליו רק XOR עם מסכה של \( k \) אחדים
רצופים, בכל היסט. הבדיקה צריכה להביא אותו לכל האחדים בכמה שפחות כתיבות, או לדעת מראש שזה בלתי
אפשרי.

- **סעיף א – שורה של ביטים :** כתבו פתרון, הסבירו למה הוא נותן את המינימום, ושפרו אותו עד זמן
  \( O(n) \), ואם אפשר גם בזיכרון נוסף \( O(1) \).
- **סעיף ב – לוח של ביטים :** לוח של \( R \) שורות ו-\( C \) עמודות, וצעד מהפך ריבוע של
  \( k \times k \) תאים. מה משתנה?

??? interviewer "מה המראיין בודק"
    - **מה באמת שואלים :** האם המועמד שם לב למבנה של הבעיה לפני שהוא מחפש, או רץ ישר לחיפוש.
    - **סדר ופעמיים :** האם הוא שואל אם הסדר של הצעדים משנה, ומה קורה לחלון שהופכים פעמיים.
    - **הוכחה :** למה הפתרון נכון, ולא רק "זה נראה חמדן ועובד על הדוגמה".
    - **מ-\( O(nk) \) ל-\( O(n) \) :** האם הוא רואה שלא צריך להפוך את הביטים בפועל, ומה מספיק
      לזכור במקום.
    - **מקרי קצה :** חלון שלא נכנס בסוף המערך, ובלוח השורות והעמודות האחרונות.

---

### סעיף א – שורה של ביטים

??? tip "רמז 1"
    האם הסדר של הצעדים משנה את התוצאה? ומה קורה כשהופכים את אותו חלון פעמיים?

??? tip "רמז 2"
    הסתכלו על ביט 0. אילו חלונות מכסים אותו? ומה זה אומר על ההחלטה הראשונה שלכם?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        הסדר של ההיפוכים לא משנה, וחלון שהופכים פעמיים מתבטל, ולכן פתרון הוא קבוצה של נקודות
        התחלה. את ביט 0 מכסה רק החלון שמתחיל ב-0, ולכן ההחלטה עליו כפויה, וכך כל ביט אחריו : אם
        יש פתרון, הוא **יחיד**. סורקים משמאל לימין ופותחים חלון בכל ביט שנשאר 0, ו-0 שנשאר אחרי
        \( n - k \) אומר שאין פתרון. ה"מינימום" בשאלה מטעה : אין בין מה לבחור. במקום להפוך \( k \)
        ביטים, זוכרים רק את הזוגיות של החלונות הפתוחים, וזה \( O(n) \).

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **פתרון הוא קבוצה.** היפוך הוא XOR עם מסכה, ו-XOR חילופי : הסדר של הצעדים לא משנה את
    התוצאה. חלון שהופכים פעמיים חוזר למה שהיה, ולכן בפתרון הכי קצר אף חלון לא מופיע פעמיים.
    פתרון הוא רק קבוצה של נקודות התחלה, \( x_p = 1 \) כשהחלון שמתחיל ב-\( p \) נבחר, לכל
    \( p \) מ-0 עד \( n - k \).

    **הביט הראשון מחליט.** את ביט 0 מכסה חלון אחד בלבד, זה שמתחיל ב-0. אם \( a_0 = 0 \) חייבים
    לבחור אותו, ואם \( a_0 = 1 \) אסור. את ביט 1 מכסים החלונות שמתחילים ב-0 וב-1, וההחלטה על 0
    כבר נפלה, ולכן גם ההחלטה על 1 כפויה. בכל ביט \( i \) מכסים החלונות שמתחילים מ-\( i - k + 1 \)
    עד \( i \), וכולם כבר הוחלטו חוץ מזה שמתחיל ב-\( i \) :

    <!-- gen 0 -->

    <svg class="figure kf-cover" viewBox="0 0 278 198" style="max-width:17.38rem" direction="ltr" role="img" aria-label="שמונת הביטים של הדוגמה, ומתחתם 6 החלונות האפשריים, חלון לכל התחלה מ-0 עד 5. את ביט 4 מכסים החלונות שמתחילים ב-2, ב-3 וב-4. כשהסריקה מגיעה לביט 4 שני הראשונים כבר הוחלטו, והחלון שמתחיל ב-4 הוא היחיד שנשאר. בביטים 6 ו-7 לא מתחיל אף חלון"><rect class="kf-col" x="154" y="4" width="30" height="192" rx="3"/><rect class="kf-nostart" x="216" y="58" width="26" height="136" rx="3"/><rect class="kf-nostart" x="246" y="58" width="26" height="136" rx="3"/><text class="kf-idx" x="49" y="16" text-anchor="middle">0</text><rect class="kf-cell" x="36" y="22" width="26" height="26" rx="3"/><text class="kf-bit" x="49" y="40" text-anchor="middle">0</text><text class="kf-idx" x="79" y="16" text-anchor="middle">1</text><rect class="kf-cell" x="66" y="22" width="26" height="26" rx="3"/><text class="kf-bit" x="79" y="40" text-anchor="middle">0</text><text class="kf-idx" x="109" y="16" text-anchor="middle">2</text><rect class="kf-cell" x="96" y="22" width="26" height="26" rx="3"/><text class="kf-bit" x="109" y="40" text-anchor="middle">0</text><text class="kf-idx" x="139" y="16" text-anchor="middle">3</text><rect class="kf-cell kf-one" x="126" y="22" width="26" height="26" rx="3"/><text class="kf-bit" x="139" y="40" text-anchor="middle">1</text><text class="kf-idx" x="169" y="16" text-anchor="middle">4</text><rect class="kf-cell" x="156" y="22" width="26" height="26" rx="3"/><text class="kf-bit" x="169" y="40" text-anchor="middle">0</text><text class="kf-idx" x="199" y="16" text-anchor="middle">5</text><rect class="kf-cell kf-one" x="186" y="22" width="26" height="26" rx="3"/><text class="kf-bit" x="199" y="40" text-anchor="middle">1</text><text class="kf-idx" x="229" y="16" text-anchor="middle">6</text><rect class="kf-cell kf-one" x="216" y="22" width="26" height="26" rx="3"/><text class="kf-bit" x="229" y="40" text-anchor="middle">1</text><text class="kf-idx" x="259" y="16" text-anchor="middle">7</text><rect class="kf-cell" x="246" y="22" width="26" height="26" rx="3"/><text class="kf-bit" x="259" y="40" text-anchor="middle">0</text><text class="kf-lab" x="26" y="40" text-anchor="end">a</text><g class="kf-bar kf-other"><title>x0: does not cover bit 4</title><rect x="37" y="62" width="84" height="15" rx="4"/></g><text class="kf-lab" x="26" y="74" text-anchor="end">x0</text><g class="kf-bar kf-other"><title>x1: does not cover bit 4</title><rect x="67" y="84" width="84" height="15" rx="4"/></g><text class="kf-lab" x="26" y="96" text-anchor="end">x1</text><g class="kf-bar kf-old"><title>x2: decided before bit 4, covers it</title><rect x="97" y="106" width="84" height="15" rx="4"/></g><text class="kf-lab" x="26" y="118" text-anchor="end">x2</text><g class="kf-bar kf-old"><title>x3: decided before bit 4, covers it</title><rect x="127" y="128" width="84" height="15" rx="4"/></g><text class="kf-lab" x="26" y="140" text-anchor="end">x3</text><g class="kf-bar kf-new"><title>x4: the only window over bit 4 not decided yet</title><rect x="157" y="150" width="84" height="15" rx="4"/></g><text class="kf-lab" x="26" y="162" text-anchor="end">x4</text><g class="kf-bar kf-other"><title>x5: does not cover bit 4</title><rect x="187" y="172" width="84" height="15" rx="4"/></g><text class="kf-lab" x="26" y="184" text-anchor="end">x5</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="kf-key-old"></i>חלונות שכבר הוחלטו ומכסים את ביט 4</span><span><i class="kf-key-new"></i>החלון היחיד שעוד לא הוחלט : מתחיל ב-4</span><span><i class="kf-key-other"></i>חלון שלא מכסה את ביט 4</span><span><i class="kf-key-nostart"></i>שום חלון לא מתחיל כאן : רק בדיקה</span></span>

    <!-- /gen -->

    אין כאן בחירה בכלל : אם יש פתרון, הוא יחיד, והסריקה היא הדרך היחידה למצוא אותו. ה"מינימום"
    בשאלה הוא מסיח : כל פתרון נכון הוא אותו פתרון. על הדוגמה, בכל שורה מתחילים חלון בביט הראשון
    שעוד 0 :

    <!-- gen 2 -->

    | הצעד | הביטים | מה הפכנו |
    |:-:|:-:|:-:|
    | 0 | <span class="kf-w" dir="ltr"><span class="kf-b kf-first">0</span><span class="kf-b">0</span><span class="kf-b">0</span><span class="kf-b kf-one">1</span><span class="kf-b">0</span><span class="kf-b kf-one">1</span><span class="kf-b kf-one">1</span><span class="kf-b">0</span></span> | ‏– |
    | 1 | <span class="kf-w" dir="ltr"><span class="kf-b kf-one kf-flip">1</span><span class="kf-b kf-one kf-flip">1</span><span class="kf-b kf-one kf-flip">1</span><span class="kf-b kf-one">1</span><span class="kf-b kf-first">0</span><span class="kf-b kf-one">1</span><span class="kf-b kf-one">1</span><span class="kf-b">0</span></span> | החלון שמתחיל ב-0 |
    | 2 | <span class="kf-w" dir="ltr"><span class="kf-b kf-one">1</span><span class="kf-b kf-one">1</span><span class="kf-b kf-one">1</span><span class="kf-b kf-one">1</span><span class="kf-b kf-one kf-flip">1</span><span class="kf-b kf-flip kf-first">0</span><span class="kf-b kf-flip">0</span><span class="kf-b">0</span></span> | החלון שמתחיל ב-4 |
    | 3 | <span class="kf-w" dir="ltr"><span class="kf-b kf-one">1</span><span class="kf-b kf-one">1</span><span class="kf-b kf-one">1</span><span class="kf-b kf-one">1</span><span class="kf-b kf-one">1</span><span class="kf-b kf-one kf-flip">1</span><span class="kf-b kf-one kf-flip">1</span><span class="kf-b kf-one kf-flip">1</span></span> | החלון שמתחיל ב-5 |

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="kf-key-one"></i>ביט 1</span><span><i class="kf-key-first"></i>הביט הראשון שהוא 0 : החלון שמתחיל בו כפוי</span><span><i class="kf-key-flip"></i>שלושת הביטים שהצעד הפך</span></span>

    <!-- /gen -->

    **מתי אין פתרון.** חלון יכול להתחיל רק עד \( n - k \). ביט שאחרי \( n - k \) רק נבדק : כל
    החלונות שמכסים אותו כבר הוחלטו, ואם הוא נשאר 0 אין שום דרך לתקן אותו. ב-<span dir="ltr">a = 110</span>
    עם \( k = 2 \) הסריקה לא פותחת אף חלון, וביט 2, האחרון, נשאר 0.

    **מ-\( O(nk) \) ל-\( O(n) \).** הסריקה הישירה הופכת \( k \) ביטים בכל חלון. אבל כדי להחליט על
    ביט \( i \) צריך רק את הערך שלו עכשיו : \( a_i \) XOR הזוגיות של מספר החלונות הפתוחים מעליו.
    חלון שמתחיל ב-\( p \) פתוח מעל הביטים \( p \) עד \( p + k - 1 \), ונסגר כשמגיעים ל-\( p + k \).
    החלונות נפתחים לפי הסדר, ולכן נסגרים לפי אותו סדר : תור של נקודות ההתחלה מספיק. בכל ביט מוציאים
    מראש התור את החלון שנסגר, והזוגיות היא הזוגיות של גודל התור. על הדוגמה :

    <!-- gen 4 -->

    | ‏i | ‏a[i] | החלונות הפתוחים | הזוגיות | הביט עכשיו | מה עושים |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | 0 | 0 | אין | 0 | 0 | פותחים חלון ב-0 |
    | 1 | 0 | <span dir="ltr">[0]</span> | 1 | 1 | כלום |
    | 2 | 0 | <span dir="ltr">[0]</span> | 1 | 1 | כלום |
    | 3 | 1 | אין | 0 | 1 | כלום |
    | 4 | 0 | אין | 0 | 0 | פותחים חלון ב-4 |
    | 5 | 1 | <span dir="ltr">[4]</span> | 1 | 0 | פותחים חלון ב-5 |
    | 6 | 1 | <span dir="ltr">[4, 5]</span> | 0 | 1 | בדיקה : 1 |
    | 7 | 0 | <span dir="ltr">[5]</span> | 1 | 1 | בדיקה : 1 |

    <!-- /gen -->

    **בזיכרון \( O(1) \).** התור מחזיק עד \( k \) מספרים. במקומו אפשר לסמן את נקודת ההתחלה במערך
    עצמו : <span dir="ltr">a[i] += 2</span>. הביט המקורי נשאר ב-<span dir="ltr">a[i] & 1</span>, וכשהסריקה
    מגיעה ל-\( i + k \) היא רואה <span dir="ltr">a[i] >= 2</span> ויודעת שהחלון נסגר. בסוף מחזירים
    את המערך כמו שהיה, <span dir="ltr">a[i] &= 1</span>.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מתחילים :** תור ריק של חלונות פתוחים, ואפס היפוכים.
    2. **ביט \( i \), החלון שנסגר :** אם בראש התור חלון שהתחיל ב-\( i - k \), מוציאים אותו.
    3. **הביט עכשיו :** ‏\( a_i \) XOR הזוגיות של גודל התור. הוא 0 בדיוק כש-\( a_i \) שווה לזוגיות.
    4. **ביט 0 :** אם \( i + k > n \), אין פתרון. אחרת פותחים חלון ב-\( i \) : מכניסים את \( i \)
       לתור, ומוסיפים 1 להיפוכים.
    5. **הסוף :** מספר ההיפוכים, החלונות שהסריקה פתחה.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="min_flips" linenums="1" hl_lines="7 22 23 25 26 36 37 44"
        from collections import deque


        def min_flips_naive(a: list[int], k: int) -> int:
            """Scan left to right and flip the window at every bit that is still 0: O(nk)."""
            a = a[:]                                   # (1)!
            n, flips = len(a), 0
            for i in range(n):
                if a[i] == 0:
                    if i + k > n:                      # (2)!
                        return -1
                    for j in range(i, i + k):
                        a[j] ^= 1
                    flips += 1
            return flips


        def min_flips(a: list[int], k: int) -> int:
            """The same scan in O(n): only the parity of the windows open over bit i matters."""
            n, flips = len(a), 0
            starts = deque()                           # the windows open over bit i, at most k
            for i in range(n):
                if starts and starts[0] + k == i:      # (3)!
                    starts.popleft()
                if a[i] == len(starts) % 2:            # (4)!
                    if i + k > n:
                        return -1
                    starts.append(i)
                    flips += 1
            return flips


        def min_flips_inplace(a: list[int], k: int) -> int:
            """O(1) extra memory: a start is marked in the array itself and read again k bits later."""
            n, flips, odd = len(a), 0, 0
            for i in range(n):
                if i >= k and a[i - k] >= 2:           # (5)!
                    odd ^= 1
                if (a[i] & 1) == odd:
                    if i + k > n:
                        flips = -1
                        break
                    a[i] += 2
                    odd ^= 1
                    flips += 1
            for i in range(n):
                a[i] &= 1                              # (6)!
            return flips
        ```

        1. עובדים על עותק, כדי לא לשנות את המערך של מי שקרא לפונקציה.
        2. ביט 0 שאף חלון לא יכול להתחיל בו : חלון ב-\( i \) היה יוצא מהמערך.
        3. החלון שהתחיל ב-\( i - k \) מכסה עד \( i - 1 \), ולכן הוא כבר לא מעל ביט \( i \).
           הוא תמיד בראש התור, כי החלונות נכנסו לפי הסדר.
        4. הביט עכשיו הוא <span dir="ltr">a[i] ^ (len(starts) % 2)</span>, והוא 0 בדיוק כששני
           החלקים שווים.
        5. ‏<span dir="ltr">a[i - k] >= 2</span> רק אם חלון התחיל ב-\( i - k \), והוא נסגר עכשיו.
           ‏`odd` היא הזוגיות של החלונות הפתוחים, כמו גודל התור בגרסה הקודמת.
        6. מוחקים את הסימנים, והמערך חוזר בדיוק למה שהיה. גם כשאין פתרון, ולכן `break` ולא `return`.

    === "SystemVerilog"
        ```systemverilog title="function min_flips" linenums="1" hl_lines="17 18 34 35 41"
        // scan left to right and flip the window at every bit that is still 0: O(nk)
        function automatic int min_flips_naive(bit a[], int k);    // (1)!
          int n = a.size(), flips = 0;
          for (int i = 0; i < n; i++)
            if (a[i] == 0) begin
              if (i + k > n) return -1;
              for (int j = i; j < i + k; j++) a[j] = ~a[j];
              flips++;
            end
          return flips;
        endfunction

        // the same scan in O(n): only the parity of the windows open over bit i matters
        function automatic int min_flips(bit a[], int k);
          int n = a.size(), flips = 0;
          int starts[$];                                   // the windows open over bit i, at most k
          for (int i = 0; i < n; i++) begin
            if (starts.size() > 0 && starts[0] + k == i) void'(starts.pop_front());
            if (a[i] == starts.size() % 2) begin
              if (i + k > n) return -1;
              starts.push_back(i);
              flips++;
            end
          end
          return flips;
        endfunction

        // O(1) extra memory: a start is marked in the array itself and read again k bits later
        function automatic int min_flips_inplace(ref int a[], input int k);   // (2)!
          int n = a.size(), flips = 0;
          bit odd = 0;
          for (int i = 0; i < n; i++) begin
            if (i >= k && a[i - k] >= 2) odd = ~odd;
            if (a[i][0] == odd) begin
              if (i + k > n) begin flips = -1; break; end
              a[i] += 2;
              odd = ~odd;
              flips++;
            end
          end
          foreach (a[i]) a[i] &= 1;
          return flips;
        endfunction
        ```

        1. מערך דינמי שעובר כ-`input` מועתק, ולכן אפשר להפוך בו ביטים בלי לשנות את המערך של
           הקורא.
        2. כאן `ref` : הפונקציה עובדת על המערך של הקורא, בלי עותק, ומחזירה אותו כמו שהיה.
           ‏`int` ולא `bit`, כדי שיהיה מקום לסימן.

    #### למה זה נכון { .sol-proof }

    **מערכת משולשת.** נסמן \( x_p \in \{0, 1\} \) לכל \( p \) מ-0 עד \( n - k \). ביט \( i \)
    מסתיים 1 בדיוק כשמספר החלונות הנבחרים מעליו זוגי אם \( a_i = 1 \), ואי-זוגי אם \( a_i = 0 \) :

    \[
    \bigoplus_{p = \max(0,\, i - k + 1)}^{\min(i,\, n - k)} x_p = 1 \oplus a_i ,
    \qquad i = 0, \dots, n - 1 .
    \]

    במשוואה של ביט \( i \le n - k \) המשתנה עם האינדקס הגדול ביותר הוא \( x_i \), וכל השאר
    קודמים לו. לכן, לפי הסדר, כל משוואה קובעת משתנה חדש אחד בדיוק, והסריקה מחשבת אותו. במשוואות
    של \( i > n - k \) אין משתנה חדש : הן רק נבדקות. לכן יש לכל היותר פתרון אחד, והסריקה מוצאת
    אותו כשהוא קיים. מכאן גם כמה מערכים אפשר לתקן : כל אחת מ-\( 2^{n-k+1} \) הבחירות של
    \( x \) נותנת מערך אחר.

    **התור והסימון.** מעל ביט \( i \) פתוחים בדיוק החלונות שהתחילו מ-\( i - k + 1 \) עד \( i - 1 \).
    כל ביט מוציא מהתור לכל היותר חלון אחד, זה שהתחיל ב-\( i - k \), והוא בראש התור כי נקודות
    ההתחלה עולות. בסימון, <span dir="ltr">a[p] >= 2</span> בדיוק כשחלון התחיל ב-\( p \), והביט
    המקורי נשאר בביט הנמוך.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n) \) לתור ולסימון : כל ביט נכנס לתור ויוצא ממנו פעם אחת לכל היותר. הסריקה
      הישירה \( O(nk) \).
    - **זיכרון :** ‏\( O(k) \) לתור, \( O(1) \) עם הסימון, ו-\( O(n) \) לעותק בסריקה הישירה.

    **נסו בעצמכם.** התיבה נפתחת על <span dir="ltr">00010110</span> עם \( k = 3 \). לחצו "הצעד הבא"
    שש פעמים : בביט 0 נפתח חלון, בביטים 1 עד 3 לא, בביט 4 החלון של 0 כבר נסגר והביט 0, ובביט 5
    החלון של 4 פתוח ומהפך את ה-1, ולכן נפתח עוד חלון. "עד הסוף" נותן 3, בחלונות 0, 4 ו-5. אחר כך
    בחרו "‏110, k = 2" : הביט האחרון נשאר 0, והתשובה ‏−1. בתיבה אפשר ללחוץ על כל ביט, עד 20
    ביטים, ולראות איך ההחלטות שאחריו משתנות ולמה כל אחת מהן כפויה :

    <div class="explorer" data-kind="kflip" data-bits="00010110" data-k="3"></div>

---

### סעיף ב – לוח של ביטים

??? tip "רמז 1"
    אילו ריבועים מכסים את התא בפינה השמאלית העליונה, <span dir="ltr">(0, 0)</span>? ובאיזה סדר
    כדאי לעבור על התאים כדי שזה יקרה שוב ושוב?

??? tip "רמז 2"
    בסעיף א הספיקה הזוגיות של החלונות הפתוחים. איך יודעים בזמן קבוע כמה מהריבועים שכבר נבחרו
    מכסים תא, בלי לעבור עליהם? מה ריבוע אחד משנה במערך הפרשים דו-ממדי?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        אותה סריקה, שורה אחרי שורה ומשמאל לימין. את התא \( (r, c) \) מכסים הריבועים שהפינה
        השמאלית העליונה שלהם בריבוע \( k \times k \) שנגמר בו, וכולם כבר הוחלטו חוץ מזה שמתחיל
        בו : ההחלטה כפויה, והפתרון שוב יחיד. תא ב-\( k - 1 \) השורות או העמודות האחרונות, שאין
        ריבוע שמתחיל בו, רק נבדק. את הזוגיות של כל תא מקבלים בזמן קבוע ממערך הפרשים : ריבוע הופך
        ארבע פינות, וה-XOR המצטבר של הפינות הוא הזוגיות. הזמן \( O(RC) \).

    <!-- cost: זמן \( O(RC) \) | זיכרון \( O(RC) \) -->

    #### הרעיון { .sol-idea }

    **שוב, ההחלטה כפויה.** פתרון הוא קבוצה של פינות שמאליות עליונות, כמו בסעיף א. עוברים על
    התאים שורה אחרי שורה. ריבוע שמכסה את \( (r, c) \) מתחיל בשורה \( r' \le r \) ובעמודה
    \( c' \le c \), ולכן כל ריבוע כזה חוץ מ-\( (r, c) \) עצמו מתחיל בתא שהסריקה כבר עברה. אם
    התא 0 עכשיו, חייבים לפתוח בו ריבוע, ואם 1 אסור. תא שאחרי \( R - k \) בשורות או אחרי
    \( C - k \) בעמודות לא יכול לפתוח ריבוע, והוא רק נבדק :

    <!-- gen 5 -->

    <svg class="figure kf-grid" viewBox="0 0 300 110" style="max-width:23.44rem" direction="ltr" role="img" aria-label="לוח של 4 על 5 עם ריבועים של 2 על 2. משמאל הלוח בהתחלה, עם 4 הריבועים שהסריקה בוחרת, הפינה של כל אחד מסומנת. השורה האחרונה והעמודה האחרונה, שאין ריבוע שמתחיל בהן, מוצללות. מימין הלוח אחרי 4 ההיפוכים : כל התאים 1"><rect class="kf-cell kf-one" x="4" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="16" y="20" text-anchor="middle">1</text><rect class="kf-cell" x="30" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="42" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="56" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="68" y="20" text-anchor="middle">0</text><rect class="kf-cell kf-one" x="82" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="94" y="20" text-anchor="middle">1</text><rect class="kf-cell kf-one kf-band" x="108" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="120" y="20" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="4" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="16" y="46" text-anchor="middle">1</text><rect class="kf-cell" x="30" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="42" y="46" text-anchor="middle">0</text><rect class="kf-cell kf-one" x="56" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="68" y="46" text-anchor="middle">1</text><rect class="kf-cell" x="82" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="94" y="46" text-anchor="middle">0</text><rect class="kf-cell kf-one kf-band" x="108" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="120" y="46" text-anchor="middle">1</text><rect class="kf-cell" x="4" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="16" y="72" text-anchor="middle">0</text><rect class="kf-cell" x="30" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="42" y="72" text-anchor="middle">0</text><rect class="kf-cell" x="56" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="68" y="72" text-anchor="middle">0</text><rect class="kf-cell kf-one" x="82" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="94" y="72" text-anchor="middle">1</text><rect class="kf-cell kf-band" x="108" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="120" y="72" text-anchor="middle">0</text><rect class="kf-cell kf-band" x="4" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="16" y="98" text-anchor="middle">0</text><rect class="kf-cell kf-band" x="30" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="42" y="98" text-anchor="middle">0</text><rect class="kf-cell kf-one kf-band" x="56" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="68" y="98" text-anchor="middle">1</text><rect class="kf-cell kf-band" x="82" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="94" y="98" text-anchor="middle">0</text><rect class="kf-cell kf-band" x="108" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="120" y="98" text-anchor="middle">0</text><g class="kf-sq"><title>square from (0, 1)</title><rect x="32.5" y="6.5" width="45" height="45" rx="5"/><circle cx="37" cy="11" r="3"/></g><g class="kf-sq"><title>square from (1, 2)</title><rect x="58.5" y="32.5" width="45" height="45" rx="5"/><circle cx="63" cy="37" r="3"/></g><g class="kf-sq"><title>square from (2, 0)</title><rect x="6.5" y="58.5" width="45" height="45" rx="5"/><circle cx="11" cy="63" r="3"/></g><g class="kf-sq"><title>square from (2, 3)</title><rect x="84.5" y="58.5" width="45" height="45" rx="5"/><circle cx="89" cy="63" r="3"/></g><rect class="kf-cell kf-one" x="168" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="180" y="20" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="194" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="206" y="20" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="220" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="232" y="20" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="246" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="258" y="20" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="272" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="284" y="20" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="168" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="180" y="46" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="194" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="206" y="46" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="220" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="232" y="46" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="246" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="258" y="46" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="272" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="284" y="46" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="168" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="180" y="72" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="194" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="206" y="72" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="220" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="232" y="72" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="246" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="258" y="72" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="272" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="284" y="72" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="168" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="180" y="98" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="194" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="206" y="98" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="220" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="232" y="98" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="246" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="258" y="98" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="272" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="284" y="98" text-anchor="middle">1</text><path class="kf-arrow" d="M141.0,55 h16 m-5,-5 l5,5 l-5,5" fill="none"/></svg>

    <!-- /gen -->

    <!-- gen 6 -->

    <span class="viz-legend"><span><i class="kf-key-one"></i>תא 1</span><span><i class="kf-key-sqv"></i>ריבוע שהסריקה בוחרת, הנקודה בפינה שלו</span><span><i class="kf-key-band"></i>שורה או עמודה שאין ריבוע שמתחיל בה : רק בדיקה</span></span>

    <!-- /gen -->

    **ארבע פינות במקום \( k^2 \) תאים.** כמו בסעיף א, לא מהפכים את התאים בפועל. מחזיקים מערך
    הפרשים \( d \) : ריבוע שמתחיל ב-\( (r, c) \) הופך את \( d \) בארבע הפינות
    \( (r, c) \), \( (r, c + k) \), \( (r + k, c) \) ו-\( (r + k, c + k) \). ה-XOR של כל
    \( d \) מעל תא ומשמאלו הוא בדיוק הזוגיות של הריבועים שמכסים אותו : כל ריבוע תורם 1 בתוכו, ומחוצה
    לו הפינות שלו מתבטלות בזוגות. את ה-XOR המצטבר \( p \) מחשבים תא אחרי תא בזמן קבוע :

    \[
    p_{r,c} = d_{r,c} \oplus p_{r-1,c} \oplus p_{r,c-1} \oplus p_{r-1,c-1} .
    \]

    <!-- gen 7 -->

    <svg class="figure kf-grid kf-corners" viewBox="0 0 300 110" style="max-width:23.44rem" direction="ltr" role="img" aria-label="ריבוע של 2 על 2 שמתחיל בתא (1, 2). משמאל מערך ההפרשים d : ארבע פינות הופכות ל-1, בתאים (1, 2), (1, 4), (3, 2) ו-(3, 4). מימין ה-XOR המצטבר של d, מכל התאים שמעל ומשמאל : 1 בדיוק בארבעת התאים של הריבוע"><rect class="kf-cell" x="4" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="16" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="30" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="42" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="56" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="68" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="82" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="94" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="108" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="120" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="4" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="16" y="46" text-anchor="middle">0</text><rect class="kf-cell" x="30" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="42" y="46" text-anchor="middle">0</text><rect class="kf-cell kf-corner" x="56" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="68" y="46" text-anchor="middle">1</text><rect class="kf-cell" x="82" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="94" y="46" text-anchor="middle">0</text><rect class="kf-cell kf-corner" x="108" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="120" y="46" text-anchor="middle">1</text><rect class="kf-cell" x="4" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="16" y="72" text-anchor="middle">0</text><rect class="kf-cell" x="30" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="42" y="72" text-anchor="middle">0</text><rect class="kf-cell" x="56" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="68" y="72" text-anchor="middle">0</text><rect class="kf-cell" x="82" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="94" y="72" text-anchor="middle">0</text><rect class="kf-cell" x="108" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="120" y="72" text-anchor="middle">0</text><rect class="kf-cell" x="4" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="16" y="98" text-anchor="middle">0</text><rect class="kf-cell" x="30" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="42" y="98" text-anchor="middle">0</text><rect class="kf-cell kf-corner" x="56" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="68" y="98" text-anchor="middle">1</text><rect class="kf-cell" x="82" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="94" y="98" text-anchor="middle">0</text><rect class="kf-cell kf-corner" x="108" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="120" y="98" text-anchor="middle">1</text><rect class="kf-cell" x="168" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="180" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="194" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="206" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="220" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="232" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="246" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="258" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="272" y="4" width="24" height="24" rx="3"/><text class="kf-bit" x="284" y="20" text-anchor="middle">0</text><rect class="kf-cell" x="168" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="180" y="46" text-anchor="middle">0</text><rect class="kf-cell" x="194" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="206" y="46" text-anchor="middle">0</text><rect class="kf-cell kf-one" x="220" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="232" y="46" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="246" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="258" y="46" text-anchor="middle">1</text><rect class="kf-cell" x="272" y="30" width="24" height="24" rx="3"/><text class="kf-bit" x="284" y="46" text-anchor="middle">0</text><rect class="kf-cell" x="168" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="180" y="72" text-anchor="middle">0</text><rect class="kf-cell" x="194" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="206" y="72" text-anchor="middle">0</text><rect class="kf-cell kf-one" x="220" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="232" y="72" text-anchor="middle">1</text><rect class="kf-cell kf-one" x="246" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="258" y="72" text-anchor="middle">1</text><rect class="kf-cell" x="272" y="56" width="24" height="24" rx="3"/><text class="kf-bit" x="284" y="72" text-anchor="middle">0</text><rect class="kf-cell" x="168" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="180" y="98" text-anchor="middle">0</text><rect class="kf-cell" x="194" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="206" y="98" text-anchor="middle">0</text><rect class="kf-cell" x="220" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="232" y="98" text-anchor="middle">0</text><rect class="kf-cell" x="246" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="258" y="98" text-anchor="middle">0</text><rect class="kf-cell" x="272" y="82" width="24" height="24" rx="3"/><text class="kf-bit" x="284" y="98" text-anchor="middle">0</text><g class="kf-sq"><rect x="222.5" y="32.5" width="45" height="45" rx="5"/></g><path class="kf-arrow" d="M141.0,55 h16 m-5,-5 l5,5 l-5,5" fill="none"/></svg>

    <!-- /gen -->

    <!-- gen 8 -->

    <span class="viz-legend"><span><i class="kf-key-corner"></i>פינה שהריבוע הפך ב-d</span><span><i class="kf-key-one"></i>‏1 ב-XOR המצטבר : התא מתחת לריבוע</span></span>

    <!-- /gen -->

    שלוש מהפינות של ריבוע חדש נמצאות אחרי התא בסדר של הסריקה. הרביעית היא התא עצמו, שכבר נקרא,
    ולכן במקום לעדכן אותה ב-\( d \) מהפכים את \( p \) שלו.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מתחילים :** ‏\( d \) ו-\( p \) של אפסים, באורך שורה ועמודה נוספות.
    2. **תא \( (r, c) \), שורה אחרי שורה :** מחשבים את \( p_{r,c} \) מ-\( d \) ומשלושת השכנים
       שכבר חושבו.
    3. **התא עכשיו :** ‏\( g_{r,c} \) XOR \( p_{r,c} \). הוא 0 בדיוק כששניהם שווים.
    4. **תא 0 :** אם \( r + k > R \) או \( c + k > C \), אין פתרון. אחרת פותחים ריבוע : שלוש
       פינות ב-\( d \), ההיפוך של \( p_{r,c} \), ו-1 להיפוכים.
    5. **הסוף :** מספר הריבועים שהסריקה פתחה.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="min_flips_2d" linenums="1" hl_lines="23 24 25 30"
        def min_flips_2d_naive(g: list[list[int]], k: int) -> int:
            """Row by row, flip the k x k square at every cell that is still 0: O(RCk^2)."""
            g = [row[:] for row in g]
            R, C, flips = len(g), len(g[0]), 0
            for r in range(R):
                for c in range(C):
                    if g[r][c] == 0:
                        if r + k > R or c + k > C:
                            return -1
                        for rr in range(r, r + k):
                            for cc in range(c, c + k):
                                g[rr][cc] ^= 1
                        flips += 1
            return flips


        def min_flips_2d(g: list[list[int]], k: int) -> int:
            """The same scan in O(RC): the corners of the squares in d, their prefix XOR in p."""
            R, C, flips = len(g), len(g[0]), 0
            d = [[0] * (C + 1) for _ in range(R + 1)]   # the corners of the squares chosen
            p = [[0] * (C + 1) for _ in range(R + 1)]   # p[r + 1][c + 1]: the parity over (r, c)
            for r in range(R):
                for c in range(C):
                    p[r + 1][c + 1] = d[r][c] ^ p[r][c + 1] ^ p[r + 1][c] ^ p[r][c]   # (1)!
                    if g[r][c] == p[r + 1][c + 1]:
                        if r + k > R or c + k > C:      # (2)!
                            return -1
                        d[r][c + k] ^= 1
                        d[r + k][c] ^= 1
                        d[r + k][c + k] ^= 1
                        p[r + 1][c + 1] ^= 1            # (3)!
                        flips += 1
            return flips
        ```

        1. ‏`p` מוזז בשורה ובעמודה אחת, כדי שהשורה והעמודה הראשונות לא יצטרכו מקרה מיוחד.
        2. גם התאים שאין ריבוע שמתחיל בהם נבדקים כאן, כשהסריקה מגיעה אליהם : כל הריבועים שמכסים
           אותם כבר הוחלטו.
        3. הפינה \( (r, c) \) של הריבוע החדש : התא כבר נקרא, ולכן מעדכנים את הזוגיות שלו ולא
           את \( d \).

    === "SystemVerilog"
        ```systemverilog title="function min_flips_2d" linenums="1" hl_lines="23 24 25 26"
        // row by row, flip the k x k square at every cell that is still 0: O(RCk^2)
        function automatic int min_flips_2d_naive(bit g[][], int k);
          int R = g.size(), C = g[0].size(), flips = 0;
          for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
              if (g[r][c] == 0) begin
                if (r + k > R || c + k > C) return -1;
                for (int rr = r; rr < r + k; rr++)
                  for (int cc = c; cc < c + k; cc++) g[rr][cc] = ~g[rr][cc];
                flips++;
              end
          return flips;
        endfunction

        // the same scan in O(RC): the corners of the squares in d, their prefix XOR in p
        function automatic int min_flips_2d(bit g[][], int k);
          int R = g.size(), C = g[0].size(), flips = 0;
          bit d[][], p[][];                                // p[r + 1][c + 1]: the parity over (r, c)
          d = new[R + 1]; p = new[R + 1];
          foreach (d[r]) begin d[r] = new[C + 1]; p[r] = new[C + 1]; end
          for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++) begin
              p[r + 1][c + 1] = d[r][c] ^ p[r][c + 1] ^ p[r + 1][c] ^ p[r][c];
              if (g[r][c] == p[r + 1][c + 1]) begin
                if (r + k > R || c + k > C) return -1;
                d[r][c + k] ^= 1; d[r + k][c] ^= 1; d[r + k][c + k] ^= 1;
                p[r + 1][c + 1] ^= 1;                      // (1)!
                flips++;
              end
            end
          return flips;
        endfunction
        ```

        1. הפינה \( (r, c) \) של הריבוע החדש : התא כבר נקרא, ולכן מעדכנים את הזוגיות שלו.

    #### למה זה נכון { .sol-proof }

    **שוב מערכת משולשת.** משתנה \( x_{r,c} \) לכל פינה אפשרית, \( r \le R - k \) ו-\( c \le C - k \),
    ומשוואה לכל תא : ה-XOR של המשתנים של הריבועים שמכסים אותו שווה ל-\( 1 \oplus g_{r,c} \). בסדר
    של שורה אחרי שורה, במשוואה של תא שיכול לפתוח ריבוע המשתנה האחרון הוא שלו, ובמשוואה של תא שלא
    יכול אין משתנה חדש. לכן יש לכל היותר פתרון אחד, והסריקה מוצאת אותו. מכל \( 2^{RC} \) הלוחות
    אפשר לתקן רק \( 2^{(R-k+1)(C-k+1)} \) : בלוח של 4 על 5 עם \( k = 2 \), אחד מכל 256.

    **מערך ההפרשים.** ה-XOR של \( d \) על המלבן מ-\( (0, 0) \) עד \( (r, c) \) סופר כל פינה של
    ריבוע שבתוכו. בריבוע שמכסה את \( (r, c) \) רק הפינה \( (r', c') \) בתוך המלבן, ומכל ריבוע אחר
    בתוך המלבן שתי פינות או ארבע, או אף אחת. לכן ה-XOR הוא הזוגיות של הריבועים מעל התא. הנוסחה של
    \( p \) היא הכלה והדחה, כשחיבור וחיסור הם אותו XOR.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(RC) \) : מספר קבוע של פעולות לכל תא. הסריקה הישירה \( O(RCk^2) \).
    - **זיכרון :** ‏\( O(RC) \) ל-\( d \) ול-\( p \). אפשר להחזיק מ-\( p \) רק את השורה הקודמת,
      ומ-\( d \) רק את \( k + 1 \) השורות הבאות.

    **נסו בעצמכם.** התיבה נפתחת על הלוח של הדוגמה. לחצו "הצעד הבא" פעמיים : בתא
    <span dir="ltr">(0, 1)</span> נפתח הריבוע הראשון, ובצד מתהפכות שלוש פינות ב-\( d \). "עד הסוף" נותן
    ארבעה ריבועים, והשורה האחרונה והעמודה האחרונה רק נבדקות. בחרו "הפינה הפוכה" : הסריקה בוחרת
    את אותם ארבעה ריבועים, ובצעד האחרון, 20, התא <span dir="ltr">(3, 4)</span> נשאר 0. "הגרלה" נותנת
    לוח שאפשר לתקן. בתיבה רואים את \( d \) ואת \( p \) מתמלאים תא אחרי תא, בלוחות עד 8 על 8 :

    <div class="explorer" data-kind="kflip2" data-grid="10011.10101.00010.00100" data-k="2"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להפוך את הביטים בפועל"
    הסריקה הישירה הופכת \( k \) ביטים בכל חלון, וזה \( (n - k + 1) \cdot k \) פעולות במקרה הגרוע,
    כשכל החלונות נבחרים. עם \( n = 10^5 \) ו-\( k = n / 2 \) זה כ-\( 2.5 \cdot 10^9 \). הזוגיות של
    החלונות הפתוחים נותנת את אותה החלטה בפעולה אחת לביט.

??? trap "מלכודת : חיפוש על המצבים"
    ‏BFS על כל המערכים האפשריים, כשכל צעד הוא חלון, מוצא את המסלול הקצר ביותר, אבל יש
    \( 2^n \) מצבים : עם \( n = 40 \) זה יותר מ-\( 10^{12} \). ובכלל אין מה לחפש : לכל מערך יש פתרון
    אחד או אף אחד.

??? trap "מלכודת : חלון שיוצא מהמערך"
    חלון יכול להתחיל רק עד \( n - k \). פתרון שמהפך בסוף "מה שנשאר מהחלון" מתקן כל מערך, גם כזה
    שאין לו פתרון : ב-<span dir="ltr">a = 110</span> עם \( k = 2 \) הוא מחזיר 1 במקום ‏−1.

??? trap "מלכודת : לחפש פתרון קצר יותר"
    הסריקה נראית כמו אלגוריתם חמדן, ומי שחושב שחמדן "בדרך כלל" טוב ינסה לשפר אותה, או להוכיח
    שהיא אופטימלית בטיעון של החלפה. אבל אין פתרון אחר להשוות אליו : הפתרון יחיד, וכל שיטה נכונה,
    מהירה או איטית, מוצאת בדיוק את אותם חלונות.

??? trap "מלכודת : לשכוח את השורות והעמודות האחרונות"
    בלוח, תא שאין ריבוע שמתחיל בו לא פותח ריבוע, אבל עדיין צריך לבדוק שהוא 1. בלוח של סעיף ב,
    עם 1 בפינה הימנית התחתונה במקום 0, הסריקה בוחרת את אותם ארבעה ריבועים, והפינה נשארת 0. פתרון
    שבודק רק את התאים שפותחים ריבוע מחזיר 4 במקום ‏−1.

??? followup "שאלות המשך"
    - **מלבן במקום ריבוע :** צעד מהפך מלבן של \( a \times b \), \( a \) שורות ו-\( b \) עמודות.
      מה משתנה?

        ??? fu-answer "תשובה"
            כמעט כלום : התא \( (r, c) \) מכריע את המלבן שמתחיל בו, אם \( r + a \le R \) ו-\( c + b \le C \),
            והפינות ב-\( d \) הן \( (r, c + b) \), \( (r + a, c) \) ו-\( (r + a, c + b) \). שאר התאים רק
            נבדקים, והפתרון שוב יחיד.

    - **מערך מעגלי :** הביט האחרון צמוד לביט 0, וחלון יכול להתחיל בכל אחד מ-\( n \) הביטים
      ולהסתובב מהסוף להתחלה. האם הסריקה עדיין עובדת?

        ??? fu-answer "תשובה"
            לא : כל ביט מכוסה ב-\( k \) חלונות, ושום החלטה לא כפויה. מההפרש בין שני ביטים שכנים,
            \( x_p \oplus x_{p-k} = a_p \oplus a_{p-1} \), ולכן המשתנים מתחלקים ל-\( g = \gcd(n, k) \)
            מעגלים של \( p \to p + k \), כל אחד נקבע מביט אחד. אם יש פתרון, יש \( 2^g \) כש-\( k / g \)
            זוגי ו-\( 2^{g-1} \) כשהוא אי-זוגי. המינימום : בכל מעגל הצד הזול, וכש-\( k / g \) אי-זוגי
            מספר המעגלים שהפכנו חייב להיות זוגי, ואם לא, מחליפים את המעגל עם ההפרש הקטן. זו מערכת
            מעל GF(2), כמו ב-[שאלה 0087](../senior/0087-lights-out.md).

    - **בחומרה :** הביטים מגיעים אחד בכל שעון. מה צריך לזכור כדי להחליט על כל ביט כשהוא מגיע?

        ??? fu-answer "תשובה"
            רגיסטר הזזה של \( k - 1 \) ההחלטות האחרונות : הזוגיות היא ה-XOR שלו, או flop אחד שמתהפך
            עם ההחלטה שנכנסת ועם זו שיוצאת. ההחלטה היא <span dir="ltr">~(bit ^ parity)</span>, מונה סופר
            אותן, ו-0 ב-\( k - 1 \) הביטים האחרונים מסמן שאין פתרון.

    - **כמה מערכים אפשר לתקן :** מכל \( 2^n \) המערכים של \( n \) ביטים, כמה אפשר להביא לכל האחדים?

        ??? fu-answer "תשובה"
            בדיוק \( 2^{n-k+1} \), כל אחד בדרך אחת : כל בחירה של חלונות נותנת מערך אחר. מערך אקראי
            ניתן לתיקון בהסתברות \( 2^{-(k-1)} \). עם \( n = 8 \) ו-\( k = 3 \) זה 64 מתוך 256.
