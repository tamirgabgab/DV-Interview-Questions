---
id: 41
title: כמה טסטים אקראיים סוגרים כיסוי – אספן הקופונים
level: junior
difficulty: medium
kind: dv
tags: [probability, coverage, math, python, systemverilog]
source: "בעיית אספן הקופונים בלבוש DV; ההכללה דרך הטבעה בתהליך פואסון"
added: 2026-10-22
---

## השאלה

ב-covergroup יש **16 תאים** (bins), למשל 16 הערכים של שדה `opcode` ברוחב 4 ביטים. כל
טסט אקראי מגריל ערך אחד, בהסתברות שווה לכל תא, ללא תלות בטסטים הקודמים.

- **סעיף א :** כמה טסטים צריך **בממוצע** עד שכל 16 התאים כוסו לפחות פעם אחת? וכמה
  טסטים צריך כדי להיות **בטוחים ב-95%** שהכיסוי מלא? תנו נוסחה כללית ל-\( n \) תאים,
  ומספרים ל-\( n = 16 \) ול-\( n = 100 \).
- **סעיף ב :** התאים לא שווים : לתא \( i \) הסתברות \( p_i \) (יש opcode נדיר), והדרישה
  היא **לפחות \( k \) פגיעות** בכל תא (`at_least`). כתבו קוד שמחשב את התוחלת, ובדקו
  אותו בסימולציה.

??? interviewer "מה המראיין בודק"
    - **זיהוי הבעיה :** זו בעיית אספן הקופונים. האם המועמד רואה שהקושי הוא בתאים
      **האחרונים**, ולא בראשונים.
    - **תוחלת מול ביטחון :** "בממוצע 54" ו"ב-95% צריך 90" הם שני מספרים שונים, ובתכנון
      רגרסיה השני הוא שחשוב.
    - **מה קורה עם תא נדיר :** הבנה שתא אחד בהסתברות 1% מכתיב לבדו כ-100 טסטים, ולכן
      טסטים אקראיים טהורים הם דרך גרועה לסגור כיסוי של מקרים נדירים.
    - **כלים :** סכום של משתנים גיאומטריים, הכלה-הדחה, או הטריק של תהליך פואסון
      להכללה. לא חייבים את כולם, אבל צריך דרך אחת שמסתדרת עם \( p_i \) שונים.
    - **אימות :** האם המועמד מציע לבדוק את הנוסחה בסימולציה, כמו שבודקים מודל.

---

### סעיף א – ‏n תאים שווים

??? tip "רמז 1"
    חשבו על הטסטים בין פגיעה בתא חדש לפגיעה בתא חדש הבא. כשכבר כוסו \( i \) תאים, מה
    הסיכוי שהטסט הבא פוגע בתא שעוד לא כוסה?

??? tip "רמז 2"
    המתנה להצלחה בהסתברות \( q \) לוקחת בממוצע \( 1/q \) ניסיונות. סכמו את ההמתנות של
    כל התאים.

??? tip "רמז 3"
    ל"95%" צריך את ההתפלגות ולא רק את התוחלת. אפשר לעקוב אחרי מספר התאים שכוסו, טסט
    אחרי טסט : בכל טסט המספר נשאר או עולה באחד, בהסתברויות ידועות.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        התוחלת היא \( n H_n = n\left(1 + \tfrac12 + \dots + \tfrac1n\right) \approx n \ln n + 0.58\,n \) :
        ‏**54.1 טסטים ל-16 תאים** ו-**518.7 ל-100**. כדי להיות בטוחים ב-95% צריך הרבה יותר :
        ‏**90 טסטים ל-16 תאים** ו-**754 ל-100**, בערך \( n \ln n + 3n \).

    <!-- cost: תוחלת \( O(n) \) | התפלגות \( O(n t) \) | סימולציה \( O(T) \) -->

    #### הרעיון { .sol-idea }

    מפרקים את הדרך לכיסוי מלא לשלבים : "מ-\( i \) תאים מכוסים ל-\( i + 1 \)". בשלב הזה
    כל טסט פוגע בתא חדש בהסתברות \( (n - i) / n \), ולכן ההמתנה היא משתנה גיאומטרי עם
    תוחלת \( n / (n - i) \). התוחלת של הסכום היא סכום התוחלות, גם אם השלבים תלויים זה
    בזה :

    \[
    \begin{aligned}
    E[T] &= \sum_{i=0}^{n-1} \frac{n}{n - i} \\
         &= n \left( \frac{1}{n} + \frac{1}{n-1} + \dots + 1 \right) = n H_n
    \end{aligned}
    \]

    התא הראשון עולה טסט אחד, והאחרון עולה בממוצע \( n \) טסטים : חצי מהזמן הולך על
    שני התאים האחרונים. זו הסיבה שכיסוי "כמעט מלא" מגיע מהר, והשלמה ל-100% איטית.

    **ל-95% צריך את ההתפלגות.** עוקבים אחרי \( c \), מספר התאים שכבר כוסו : אחרי כל טסט
    \( c \) נשאר (בהסתברות \( c/n \)) או עולה באחד (בהסתברות \( (n - c)/n \)). זו שרשרת
    מרקוב עם \( n + 1 \) מצבים, ומגלגלים אותה טסט אחרי טסט עד שההסתברות של \( c = n \)
    עוברת 0.95.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הפירוק :** ‏\( T = T_0 + T_1 + \dots + T_{n-1} \), כאשר \( T_i \) הוא מספר הטסטים
       מהפגיעה ה-\( i \) בתא חדש עד הפגיעה הבאה.
    2. **כל שלב :** ‏\( T_i \) גיאומטרי עם הצלחה \( (n - i)/n \), ולכן \( E[T_i] = n/(n - i) \).
    3. **הסכום :** ‏\( E[T] = n H_n \). ל-16 תאים : ‏\( 16 \cdot 3.381 = 54.1 \).
    4. **ההתפלגות :** מגלגלים את השרשרת על \( c \) ומוצאים את \( t \) הראשון שבו
       \( P(c = n) \ge 0.95 \) : ‏90 ל-16 תאים.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="expected_uniform, cover_curve, tests_for" linenums="1" hl_lines="7 13 14 15 16"
        localparam int MAXB = 1024;      // bins

        // n H_n: the expected number of tests until every one of n equal bins is hit.
        function automatic real expected_uniform(int n);
          real e = 0.0;
          for (int i = 0; i < n; i++) e += real'(n) / real'(n - i);   // (1)!
          return e;
        endfunction

        // One more test: the distribution of the number of covered bins (prob[c], c = 0..n).
        function automatic void cover_step(int n, ref real prob[MAXB + 1]);
          real nxt[MAXB + 1];
          for (int c = 0; c <= n; c++)
            nxt[c] = prob[c] * real'(c) / real'(n) + (c > 0 ? prob[c - 1] * real'(n - c + 1) / real'(n) : 0.0);   // (2)!
          for (int c = 0; c <= n; c++) prob[c] = nxt[c];
        endfunction

        // P(all n bins covered within t tests) for t = 0..tmax.
        function automatic void cover_curve(int n, int tmax, output real curve[MAXB]);
          real prob[MAXB + 1];
          foreach (prob[c]) prob[c] = (c == 0) ? 1.0 : 0.0;
          for (int t = 0; t <= tmax; t++) begin
            curve[t] = prob[n];
            cover_step(n, prob);
          end
        endfunction

        // The fewest tests that cover all n bins with probability at least q.
        function automatic int tests_for(int n, real q);
          real prob[MAXB + 1];
          int t = 0;
          foreach (prob[c]) prob[c] = (c == 0) ? 1.0 : 0.0;
          while (prob[n] < q) begin cover_step(n, prob); t++; end   // (3)!
          return t;
        endfunction
        ```

        1. ההמתנה לתא חדש כשכבר כוסו \( i \) : ‏\( n / (n - i) \) טסטים בממוצע.
        2. בכל טסט \( c \) נשאר (פגיעה בתא שכבר כוסה) או עולה באחד (תא חדש).
        3. מגלגלים את השרשרת עד שההסתברות לכיסוי מלא עוברת את \( q \).

    === "Python"
        ```python title="expected_uniform, cover_curve, tests_for" linenums="1" hl_lines="3 8 21"
        def expected_uniform(n: int) -> float:
            """n H_n: the expected number of tests until every one of n equal bins is hit."""
            return sum(n / (n - i) for i in range(n))                         # (1)!


        def cover_step(prob: list[float], n: int) -> list[float]:
            """One more test: the distribution of the number of covered bins (prob[c], c = 0..n)."""
            return [prob[c] * c / n + (prob[c - 1] * (n - c + 1) / n if c else 0.0) for c in range(n + 1)]   # (2)!


        def cover_curve(n: int, tmax: int) -> list[float]:
            """P(all n bins covered within t tests) for t = 0..tmax."""
            prob, out = [1.0] + [0.0] * n, []
            for _ in range(tmax + 1):
                out.append(prob[n])
                prob = cover_step(prob, n)
            return out


        def tests_for(n: int, q: float) -> int:
            """The fewest tests that cover all n bins with probability at least q."""
            prob, t = [1.0] + [0.0] * n, 0
            while prob[n] < q:                                                # (3)!
                prob, t = cover_step(prob, n), t + 1
            return t
        ```

        1. ההמתנה לתא חדש כשכבר כוסו \( i \) : ‏\( n / (n - i) \) טסטים בממוצע.
        2. בכל טסט \( c \) נשאר (פגיעה בתא שכבר כוסה) או עולה באחד (תא חדש).
        3. מגלגלים את השרשרת עד שההסתברות לכיסוי מלא עוברת את \( q \).

    #### למה זה נכון { .sol-proof }

    **ההמתנות של 16 התאים.** הטבלה מראה למה הסוף יקר : התא האחרון לבדו עולה 16 טסטים
    בממוצע, כמו 12 התאים הראשונים ביחד בערך :

    <!-- gen 0 -->

    | ‏bins שכבר כוסו | הסיכוי שטסט פוגע בחדש | טסטים בממוצע עד הפגיעה הבאה |
    |:-:|:-:|:-:|
    | ‏0 | ‏16/16 | ‏1.00 |
    | ‏1 | ‏15/16 | ‏1.07 |
    | ‏2 | ‏14/16 | ‏1.14 |
    | ‏4 | ‏12/16 | ‏1.33 |
    | ‏8 | ‏8/16 | ‏2.00 |
    | ‏12 | ‏4/16 | ‏4.00 |
    | ‏14 | ‏2/16 | ‏8.00 |
    | ‏15 | ‏1/16 | ‏16.00 |
    | **סך הכול** | | ‏**54.1** |

    <!-- /gen -->

    **לנסות בעצמכם.** בתיבה הבאה ״הטסט הבא״ מגריל טסטים אחד אחרי השני. הסרט מחלק אותם
    לשלבים, מ-\( i \) תאים מכוסים ל-\( i + 1 \), והעמודות משוות את ההמתנה של כל שלב
    לתוחלת \( n/(n - i) \). ״ממוצע של 500 ריצות״ מראה שהממוצעים יושבים על התוחלות, ושהשלבים
    האחרונים לוקחים את רוב הטסטים.

    <div class="explorer" data-kind="stages" data-n="16" data-seed="37"></div>

    **תוחלת, חציון ו-95%.** אותם חישובים לכמה גדלים. שימו לב שהיחס בין "95%" ל-\( n \)
    גדל עם \( n \), כי \( n \ln n \) גדל מהר מ-\( n \) :

    <!-- gen 1 -->

    | ‏bins | התוחלת ‏n·H_n | חציון | ‏95% | ‏99% | ‏95% לעומת n |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏4 | ‏8.3 | ‏7 | ‏16 | ‏21 | ‏×4.0 |
    | ‏8 | ‏21.7 | ‏20 | ‏38 | ‏51 | ‏×4.8 |
    | ‏16 | ‏54.1 | ‏51 | ‏90 | ‏115 | ‏×5.6 |
    | ‏32 | ‏129.9 | ‏123 | ‏203 | ‏255 | ‏×6.3 |
    | ‏64 | ‏303.6 | ‏290 | ‏453 | ‏557 | ‏×7.1 |
    | ‏100 | ‏518.7 | ‏497 | ‏754 | ‏916 | ‏×7.5 |

    <!-- /gen -->

    **העקומה ל-16 תאים.** ההסתברות לכיסוי מלא אחרי \( t \) טסטים. היא עולה בחדות סביב
    התוחלת, אבל הזנב ארוך : מ-50% ל-95% צריך כמעט פי שניים טסטים :

    <!-- gen 2 -->

    <svg class="perf-chart" viewBox="0 0 640 250" role="img" aria-label="הסיכוי שכל 16 ה-bins כוסו אחרי t טסטים, עם החציון 51, התוחלת 54.1 והטסט ה-90 שבו מגיעים ל-95%"><line class="grid" x1="46" x2="628" y1="216.0" y2="216.0"/><text class="tick" x="38" y="220.0" text-anchor="end">0</text><line class="grid" x1="46" x2="628" y1="166.0" y2="166.0"/><text class="tick" x="38" y="170.0" text-anchor="end">0.25</text><line class="grid" x1="46" x2="628" y1="116.0" y2="116.0"/><text class="tick" x="38" y="120.0" text-anchor="end">0.5</text><line class="grid" x1="46" x2="628" y1="66.0" y2="66.0"/><text class="tick" x="38" y="70.0" text-anchor="end">0.75</text><line class="grid" x1="46" x2="628" y1="16.0" y2="16.0"/><text class="tick" x="38" y="20.0" text-anchor="end">1</text><line class="grid" x1="46.0" x2="46.0" y1="10" y2="216" stroke-dasharray="4 4"/><text class="tick" x="46.0" y="234" text-anchor="middle">0</text><line class="grid" x1="161.5" x2="161.5" y1="10" y2="216" stroke-dasharray="4 4"/><text class="tick" x="161.5" y="234" text-anchor="middle">25</text><line class="grid" x1="277.0" x2="277.0" y1="10" y2="216" stroke-dasharray="4 4"/><text class="tick" x="277.0" y="234" text-anchor="middle">50</text><line class="grid" x1="392.4" x2="392.4" y1="10" y2="216" stroke-dasharray="4 4"/><text class="tick" x="392.4" y="234" text-anchor="middle">75</text><line class="grid" x1="507.9" x2="507.9" y1="10" y2="216" stroke-dasharray="4 4"/><text class="tick" x="507.9" y="234" text-anchor="middle">100</text><line class="grid" x1="623.4" x2="623.4" y1="10" y2="216" stroke-dasharray="4 4"/><text class="tick" x="623.4" y="234" text-anchor="middle">125</text><line class="ink-line" x1="46" x2="628" y1="26.0" y2="26.0" stroke-width="1.5" stroke-dasharray="6 4"/><text class="legend" x="624" y="20.0" text-anchor="end">95%</text><line class="grid" x1="46" x2="628" y1="116.0" y2="116.0" stroke-width="1" stroke-dasharray="6 4"/><text class="legend" x="624" y="110.0" text-anchor="end">50%</text><polyline class="s1-line" points="46.0,216.0 50.6,216.0 55.2,216.0 59.9,216.0 64.5,216.0 69.1,216.0 73.7,216.0 78.3,216.0 83.0,216.0 87.6,216.0 92.2,216.0 96.8,216.0 101.4,216.0 106.0,216.0 110.7,216.0 115.3,216.0 119.9,216.0 124.5,216.0 129.1,216.0 133.8,216.0 138.4,215.9 143.0,215.8 147.6,215.6 152.2,215.4 156.9,214.9 161.5,214.3 166.1,213.4 170.7,212.2 175.3,210.7 180.0,208.9 184.6,206.7 189.2,204.2 193.8,201.3 198.4,198.1 203.0,194.5 207.7,190.6 212.3,186.4 216.9,181.9 221.5,177.3 226.1,172.4 230.8,167.4 235.4,162.3 240.0,157.1 244.6,151.9 249.2,146.6 253.9,141.3 258.5,136.1 263.1,131.0 267.7,125.9 272.3,120.9 277.0,116.0 281.6,111.2 286.2,106.6 290.8,102.1 295.4,97.8 300.0,93.6 304.7,89.6 309.3,85.7 313.9,82.0 318.5,78.5 323.1,75.1 327.8,71.8 332.4,68.7 337.0,65.8 341.6,63.0 346.2,60.3 350.9,57.8 355.5,55.4 360.1,53.1 364.7,50.9 369.3,48.9 374.0,47.0 378.6,45.1 383.2,43.4 387.8,41.8 392.4,40.2 397.0,38.8 401.7,37.4 406.3,36.1 410.9,34.9 415.5,33.8 420.1,32.7 424.8,31.7 429.4,30.7 434.0,29.8 438.6,29.0 443.2,28.2 447.9,27.4 452.5,26.7 457.1,26.1 461.7,25.5 466.3,24.9 471.0,24.3 475.6,23.8 480.2,23.3 484.8,22.9 489.4,22.5 494.0,22.1 498.7,21.7 503.3,21.3 507.9,21.0 512.5,20.7 517.1,20.4 521.8,20.1 526.4,19.9 531.0,19.6 535.6,19.4 540.2,19.2 544.9,19.0 549.5,18.8 554.1,18.6 558.7,18.5 563.3,18.3 568.0,18.2 572.6,18.0 577.2,17.9 581.8,17.8 586.4,17.7 591.0,17.6 595.7,17.5 600.3,17.4 604.9,17.3 609.5,17.2 614.1,17.1 618.8,17.1 623.4,17.0 628.0,16.9" fill="none" stroke-width="2"/><line class="ink-line" x1="281.6" x2="281.6" y1="116.0" y2="216" stroke-width="1" stroke-dasharray="3 3"/><text class="legend" x="287.6" y="210">חציון 51</text><line class="ink-line" x1="295.9" x2="295.9" y1="97.8" y2="216" stroke-width="1" stroke-dasharray="3 3"/><text class="legend" x="301.9" y="210">תוחלת 54.1</text><line class="ink-line" x1="461.7" x2="461.7" y1="26.0" y2="216" stroke-width="1" stroke-dasharray="3 3"/><text class="legend" x="467.7" y="210">95% : 90</text><line class="axis" x1="46" x2="628" y1="216" y2="216"/><text class="tick" x="38" y="234" text-anchor="end">טסטים</text></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="by-multiples"></i>‏P(כל 16 ה-bins כוסו אחרי t טסטים)</span><span><i class="ink"></i>החציון, התוחלת והטסט שבו מגיעים ל-95%</span></span>

    <!-- /gen -->

    **הנוסחה הסגורה לזנב.** בהכלה-הדחה על "אילו תאים עדיין ריקים" :

    \[
    P(T > t) = \sum_{j=1}^{n} (-1)^{j+1} \binom{n}{j} \left(1 - \frac{j}{n}\right)^{t}
    \]

    היא נכונה, אבל לא נוחה למחשב : ב-\( n = 100 \) האיברים ענקיים ומתקזזים, והטעות
    הנומרית בולעת את התשובה. השרשרת על \( c \) נותנת אותם מספרים בלי התקזזות, ובדיקות
    השאלה משוות ביניהן ב-\( n \) קטן עם שברים מדויקים.

    **הקירוב.** ‏\( H_n \approx \ln n + 0.5772 \), ולכן \( E[T] \approx n \ln n + 0.58 n \).
    לזנב : ‏\( P(T > t) \approx n e^{-t/n} \) (האיבר הראשון של הסכום), ומכאן "95%" ב-
    \( t \approx n \ln(20 n) \) : ל-16 תאים 92, קרוב ל-90 המדויק.

    #### סיבוכיות { .sol-cost }

    התוחלת ב-\( O(n) \). ההתפלגות עד \( t \) טסטים ב-\( O(n t) \) : ל-100 תאים ו-95%
    זה \( 100 \times 754 \), מיידי. סימולציה של ריצה אחת : ‏\( O(T) \) עם \( T \approx n \ln n \).

---

### סעיף ב – תאים לא שווים, ולפחות k פגיעות

לתא \( i \) הסתברות \( p_i \) (למשל 16 תאים, אחד מהם בהסתברות 0.01 והשאר שווים), והכיסוי
דורש לפחות \( k \) פגיעות בכל תא. כתבו פונקציה שמחשבת את תוחלת מספר הטסטים, ופונקציה
שמדמה ריצה אחת, כדי להשוות.

??? tip "רמז 1"
    הפירוק לשלבים כבר לא עובד : ההסתברות לפגוע ב"תא חדש" תלויה **באילו** תאים נשארו, לא
    רק בכמה.

??? tip "רמז 2"
    טריק : במקום לספור טסטים, דמיינו שהטסטים מגיעים בזמן רציף, כתהליך פואסון בקצב 1.
    אז הפגיעות בכל תא הן תהליך פואסון משלו, בקצב \( p_i \), **בלתי תלוי** בתאים האחרים.

??? tip "רמז 3"
    עם אי-תלות, "כולם כוסו עד זמן \( t \)" הוא מכפלה, ו-\( E[T] = \int_0^\infty P(T > t)\,dt \).
    נשאר להסביר למה תוחלת הזמן הרציף שווה לתוחלת מספר הטסטים.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        \[
        E[T] = \int_0^\infty \left( 1 - \prod_{i=1}^{n} P\big(\mathrm{Poisson}(p_i t) \ge k\big) \right) dt
        \]
        ול-\( k = 1 \) יש צורה סגורה, \( E[T] = \sum_{S \ne \emptyset} (-1)^{|S|+1} / p(S) \)
        על כל תת-הקבוצות של התאים. לארבעה תאים עם \( 0.1, 0.2, 0.3, 0.4 \) : ‏12.36; ל-16
        תאים עם אחד נדיר ב-0.01 : ‏111.8, כמעט כפליים מ-54.1 של התאים השווים.

    <!-- cost: אינטגרל \( O(n k \cdot t_{\max} / h) \) | נוסחה \( O(2^n \cdot n) \) | סימולציה \( O(T) \) -->

    #### הרעיון { .sol-idea }

    **הטבעה בזמן רציף.** נניח שהטסטים מגיעים ברגעים אקראיים, כתהליך פואסון בקצב 1 : בין
    טסט לטסט עובר זמן אקספוננציאלי עם תוחלת 1. כל טסט "מתפצל" לתא \( i \) בהסתברות
    \( p_i \), ולכן הפגיעות בתא \( i \) הן תהליך פואסון בקצב \( p_i \), **ובלתי תלויות**
    בפגיעות בתאים האחרים (תכונת הפיצול של פואסון). מספר הפגיעות בתא \( i \) עד זמן
    \( t \) הוא \( \mathrm{Poisson}(p_i t) \).

    **כיסוי מלא.** בזמן \( t \) כל התאים כוסו אם לכל אחד יש \( k \) פגיעות לפחות, ובזכות
    אי-התלות זו מכפלה :
    \( P(\tau \le t) = \prod_i P(\mathrm{Poisson}(p_i t) \ge k) \), כאשר \( \tau \) הוא
    הזמן הרציף של הכיסוי. התוחלת של משתנה אי-שלילי היא אינטגרל הזנב, ומכאן הנוסחה.

    **מזמן רציף למספר טסטים.** ‏\( \tau \) הוא רגע הגעתו של הטסט ה-\( T \), כלומר סכום
    של \( T \) זמני המתנה אקספוננציאליים עם תוחלת 1. ‏\( T \) נקבע רק לפי **אילו** תאים
    הטסטים פגעו, ולא לפי **מתי** הגיעו, ולכן \( T \) בלתי תלוי בזמני ההמתנה, וזהות ואלד
    נותנת \( E[\tau] = E[T] \cdot 1 \). תוחלת הזמן הרציף היא בדיוק תוחלת מספר הטסטים.

    **‏k = 1.** ‏\( P(\mathrm{Poisson}(p_i t) \ge 1) = 1 - e^{-p_i t} \), פותחים את
    המכפלה, וכל איבר \( \int_0^\infty e^{-p(S) t} dt = 1/p(S) \) : זו הכלה-הדחה על
    תת-הקבוצות. לתאים שווים הסכום מצטמצם ל-\( n H_n \) של סעיף א.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ההסתברויות :** ‏\( p_i \) מהמשקלים של התאים, מנורמלים לסכום 1.
    2. **הזנב :** לכל \( t \), ‏\( 1 - \prod_i P(\mathrm{Poisson}(p_i t) \ge k) \), עם
       \( P(\ge k) = 1 - e^{-\lambda}\sum_{j<k} \lambda^j / j! \).
    3. **האינטגרל :** כלל סימפסון בצעדים קבועים, עד שהזנב נעלם.
    4. **‏k = 1 בנפרד :** הסכום על \( 2^n - 1 \) תת-הקבוצות, כבדיקה של האינטגרל.
    5. **סימולציה :** מגרילים טסט אחרי טסט לפי \( p \) עד שלכל תא יש \( k \) פגיעות,
       וממצעים על הרבה ריצות.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="expected_tests, expected_k1, simulate_tests" linenums="1" hl_lines="9 10 19 20 21 22 33 44 45 46"
        localparam int MAXN = 32;        // bins with their own probability

        // P(Poisson(lam) >= k).
        function automatic real poisson_at_least(real lam, int k);
          real term = $exp(-lam), below = 0.0;
          for (int j = 0; j < k; j++) begin below += term; term *= lam / real'(j + 1); end
          return 1.0 - below;
        endfunction

        // 1 - prod_i P(Poisson(p_i t) >= k): some bin still short of k hits at time t.
        function automatic real uncovered(real p[MAXN], int n, int k, real t);
          real prod = 1.0;
          for (int i = 0; i < n; i++) prod *= poisson_at_least(p[i] * t, k);
          return 1.0 - prod;
        endfunction

        // E[tests] until every bin has at least k hits: the integral of uncovered(t), Simpson's rule.
        function automatic real expected_tests(real p[MAXN], int n, int k);
          real h = 0.02, total = 0.0, t = 0.0, a, m, b;
          forever begin
            a = uncovered(p, n, k, t); m = uncovered(p, n, k, t + h / 2); b = uncovered(p, n, k, t + h);
            total += h * (a + 4.0 * m + b) / 6.0;                        // (1)!
            t += h;
            if (t > 1.0 && b < 1e-12) return total;
          end
        endfunction

        // k = 1 in closed form: over the non-empty subsets, (-1)^(|S|+1) / p(S).
        function automatic real expected_k1(real p[MAXN], int n);
          real total = 0.0, s;
          for (int mask = 1; mask < (1 << n); mask++) begin
            s = 0.0;
            for (int i = 0; i < n; i++) if (mask[i]) s += p[i];
            total += ($countones(mask) % 2 ? 1.0 : -1.0) / s;             // (2)!
          end
          return total;
        endfunction

        // One run: tests drawn by p until every bin has k hits; returns the number of tests.
        function automatic int simulate_tests(real p[MAXN], int n, int k);
          int hits[MAXN], left = n, t = 0, i;
          real r;
          foreach (hits[j]) hits[j] = 0;
          while (left > 0) begin
            r = real'($urandom) / 4294967296.0;                           // (3)!
            i = 0;
            while (i < n - 1 && r >= p[i]) begin r -= p[i]; i++; end
            hits[i]++; t++;
            if (hits[i] == k) left--;
          end
          return t;
        endfunction
        ```

        1. כלל סימפסון על קטע באורך \( h \) : ‏\( h (a + 4m + b) / 6 \).
        2. הסימן לפי גודל תת-הקבוצה : חיובי לאי-זוגי, שלילי לזוגי.
        3. ‏`$urandom` ל-\( [0, 1) \), והתא נבחר לפי ההסתברויות המצטברות.

    === "Python"
        ```python title="expected_tests, expected_k1, simulate_tests" linenums="1" hl_lines="20 21 22 31 32 40 41"
        import math


        def poisson_at_least(lam: float, k: int) -> float:
            """P(Poisson(lam) >= k)."""
            term, below = math.exp(-lam), 0.0
            for j in range(k):
                below += term
                term *= lam / (j + 1)
            return 1.0 - below


        def expected_tests(p: list[float], k: int, h: float = 0.02) -> float:
            """E[tests] until every bin i (probability p[i]) has at least k hits: the integral over t
            of 1 - prod_i P(Poisson(p_i t) >= k), by Simpson's rule until the integrand vanishes."""
            def uncovered(t):
                prod = 1.0
                for pi in p:
                    prod *= poisson_at_least(pi * t, k)
                return 1.0 - prod
            total, t = 0.0, 0.0
            while True:
                a, m, b = uncovered(t), uncovered(t + h / 2), uncovered(t + h)
                total += h * (a + 4 * m + b) / 6                                # (1)!
                t += h
                if t > 1 and b < 1e-12:
                    return total


        def expected_k1(p: list[float]) -> float:
            """k = 1 in closed form: over the non-empty subsets, (-1)^(|S|+1) / p(S)."""
            total = 0.0
            for mask in range(1, 1 << len(p)):
                s = sum(pi for i, pi in enumerate(p) if mask >> i & 1)
                total += (1 if bin(mask).count("1") % 2 else -1) / s           # (2)!
            return total


        def simulate_tests(p: list[float], k: int, rng) -> int:
            """One run: tests drawn by p until every bin has k hits; the number of tests."""
            hits, left, t = [0] * len(p), len(p), 0
            while left:
                r, i = rng.random(), 0                                           # (3)!
                while i < len(p) - 1 and r >= p[i]:
                    r, i = r - p[i], i + 1
                hits[i] += 1
                t += 1
                if hits[i] == k:
                    left -= 1
            return t
        ```

        1. כלל סימפסון על קטע באורך \( h \) : ‏\( h (a + 4m + b) / 6 \).
        2. הסימן לפי גודל תת-הקבוצה : חיובי לאי-זוגי, שלילי לזוגי.
        3. מספר אקראי ב-\( [0, 1) \), והתא נבחר לפי ההסתברויות המצטברות.

    #### למה זה נכון { .sol-proof }

    **הפיצול של פואסון.** בתהליך פואסון בקצב 1, כל נקודה מסומנת בתא \( i \) בהסתברות
    \( p_i \) ללא תלות בשאר. הנקודות המסומנות \( i \) הן תהליך פואסון בקצב \( p_i \), ותהליכים
    של תאים שונים בלתי תלויים. לכן \( N_i(t) \sim \mathrm{Poisson}(p_i t) \), ו-
    \( P(\text{all covered by } t) = \prod_i P(N_i(t) \ge k) \).

    **מזמן לטסטים.** ‏\( \tau = X_1 + \dots + X_T \), עם \( X_j \) אקספוננציאליים בתוחלת 1
    ו-\( T \) מספר הטסטים עד הכיסוי. המאורע \( \{T \ge j\} \) נקבע לפי התאים של
    \( j - 1 \) הטסטים הראשונים, שבלתי תלויים ב-\( X_j \). זהות ואלד :
    \( E[\tau] = E[T]\,E[X] = E[T] \). ואז \( E[T] = E[\tau] \), והתוחלת של \( \tau \) היא
    אינטגרל הזנב :

    \[
    \begin{aligned}
    E[T] &= \int_0^\infty P(\tau > t)\,dt \\
         &= \int_0^\infty \Big(1 - \prod_i P\big(N_i(t) \ge k\big)\Big)\,dt
    \end{aligned}
    \]

    **‏k = 1 והכלה-הדחה.** פותחים את המכפלה :

    \[
    1 - \prod_i \left(1 - e^{-p_i t}\right) = \sum_{S \ne \emptyset} (-1)^{|S|+1} e^{-p(S)\,t}
    \]

    ואינטגרל של כל איבר הוא \( 1 / p(S) \). עם \( p_i = 1/n \) מקבלים
    \( \sum_j (-1)^{j+1} \binom{n}{j} \frac{n}{j} = n H_n \), בהתאם לסעיף א.

    **הדוגמאות.** האינטגרל, הנוסחה הסגורה כשיש, והבדיקות של השאלה מריצות גם את
    הסימולציה ומוודאות שהממוצע נופל בתוך השגיאה הסטטיסטית :

    <!-- gen 4 -->

    | המקרה | ‏k | התוחלת (האינטגרל) | הנוסחה הסגורה ל-k = 1 |
    |---|:-:|:-:|:-:|
    | ארבעה bins שווים | ‏1 | ‏8.33 | ‏8.33 |
    | ארבעה bins, 0.1 / 0.2 / 0.3 / 0.4 | ‏1 | ‏12.36 | ‏12.36 |
    | ארבעה bins שווים, לפחות 2 פגיעות | ‏2 | ‏14.19 | — |
    | ארבעה bins, 0.1 / 0.2 / 0.3 / 0.4, לפחות 3 | ‏3 | ‏32.16 | — |
    | ‏16 bins שווים | ‏1 | ‏54.09 | ‏54.09 = 16·H₁₆ |
    | ‏16 bins : אחד נדיר (0.01), השאר שווים | ‏1 | ‏111.79 | ‏111.79 |
    | ‏16 bins שווים, לפחות 4 פגיעות | ‏4 | ‏132.00 | — |

    <!-- /gen -->

    התא הנדיר מכתיב הכול : 15 תאים שווים נסגרים בכ-50 טסטים, והתא של 1% לבדו דורש
    בממוצע 100, ולכן התוחלת קופצת ל-111.8. דרישה של 4 פגיעות בכל אחד מ-16 התאים
    השווים עולה 132 טסטים, ולא \( 4 \times 54 \) : הפגיעות ה"מיותרות" בתאים שכבר
    כוסו נספרות גם כן.

    **נסו בעצמכם.** בוחרים מספר תאים, משקל לכל תא (ההסתברויות הן המשקלים מנורמלים)
    ו-`at_least`. "הטסט הבא" ו"הפעלה" ממלאים את התאים טסט אחרי טסט עד הכיסוי, ו"1,000
    ריצות" מציירות היסטוגרמה של מספר הטסטים, עם הממוצע וה-95% לעומת התוחלת המחושבת :

    <div class="explorer" data-kind="coverage" data-n="4" data-weights="1 2 3 4" data-k="1"></div>

    #### סיבוכיות { .sol-cost }

    - **האינטגרל :** ‏\( O(n k \cdot t_{\max} / h) \), כאשר \( t_{\max} \) הוא הזמן שבו הזנב
      נעלם, בערך \( n \ln n \) עד כמה מאות. ל-16 תאים זה אלפי צעדים, מיידי.
    - **הנוסחה הסגורה :** ‏\( O(2^n \cdot n) \), מעשית עד כ-20 תאים.
    - **סימולציה :** ‏\( O(T) \) לריצה, ו-1,000 ריצות נותנות ממוצע עם שגיאה של כ-\( \sigma / 30 \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : 'n טסטים מספיקים ל-n תאים'"
    אחרי \( n \) טסטים אקראיים מכוסים בממוצע רק \( n(1 - 1/e) \approx 63\% \) מהתאים.
    כיסוי מלא עולה \( n \ln n \), ובביטחון של 95% בערך \( n \ln(20n) \) : ל-100 תאים,
    754 טסטים, לא 100.

??? trap "מלכודת : תוחלת במקום אחוזון"
    "בממוצע 54 טסטים" לא אומר ש-54 טסטים מספיקים : ב-54 טסטים הסיכוי לכיסוי מלא הוא
    רק כ-59%. תכנון רגרסיה עובד עם אחוזון (95% או 99%), והוא כמעט פי שניים מהתוחלת.

??? trap "מלכודת : לחשב את הזנב בהכלה-הדחה ב-n גדול"
    הסכום המתחלף נכון מתמטית, אבל ב-\( n = 100 \) האיברים הם בגודל \( 10^{29} \)
    ומתקזזים לאחד שבר קטן. בנקודה צפה התשובה יוצאת זבל. השרשרת על מספר התאים
    המכוסים לא מתקזזת.

??? trap "מלכודת : להכפיל ב-k"
    ‏`at_least = 4` לא מכפיל את התוחלת ב-4 : הפגיעות בתאים שכבר השלימו נספרות ממילא.
    ל-16 תאים שווים התוחלת היא 132, ולא 216. בכיוון השני, אין גם דרך קצרה : צריך את
    האינטגרל או סימולציה.

??? followup "שאלות המשך"
    - **הטיה במקום אקראיות :** איך מכסים את התא הנדיר בלי 100 טסטים? ‏(constraint
      עם `dist` שמעלה את ההסתברות שלו, או טסט ייעודי; זה כל הרעיון של coverage-driven.)
    - **הזנב במקרה הכללי :** לא רק התוחלת, אלא "כמה טסטים ל-95%" עם \( p_i \) שונים. ‏(אין
      שרשרת פשוטה; סימולציה, או חסם מההכלה-הדחה כש-\( n \) קטן.)
    - **כמה טסטים כדי להגיע ל-90% מהתאים :** לא כיסוי מלא. ‏(‏\( n (H_n - H_{n/10}) \), שמתקרב ל-\( n \ln 10 \approx 2.3n \); ל-16
      תאים 30 טסטים לעומת 54.)
    - **‏cross coverage :** ‏\( 16 \times 16 \) תאים של שני שדות בלתי תלויים. ‏(אותה בעיה
      עם \( n = 256 \) : בערך 1,568 טסטים בממוצע, ו-2,176 ל-95%.)
    - **טסטים לא בלתי תלויים :** כל טסט מגריל 10 ערכים ברצף. מה משתנה בתוחלת? ‏(סופרים
      ערכים ולא טסטים; מספר הטסטים הוא עשירית, מעוגל למעלה.)
