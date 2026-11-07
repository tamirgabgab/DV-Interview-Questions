---
id: 98
title: ספרת ביקורת בכרטיס אשראי – מה Luhn תופס ומה חומק
level: junior
difficulty: medium
kind: code
tags: [digits, number-theory, proof, constraints, python, systemverilog]
source: "האלגוריתם של H. P. Luhn מ-IBM (פטנט אמריקאי 2,950,048, 1960); ISBN-10 לפי ISO 2108"
added: 2026-11-07
---

## השאלה

המספר של כרטיס אשראי נגמר ב**ספרת ביקורת** : ספרה שלא נושאת מידע, ותפקידה לתפוס טעות
הקלדה לפני שהמספר נשלח לבנק. כמעט כל הכרטיסים משתמשים באלגוריתם של Luhn :

1. סופרים את המקומות מימין. הספרה הימנית ביותר, ספרת הביקורת, היא מקום 1.
2. כל ספרה במקום זוגי (2, 4, 6 ...) מכפילים ב-2. אם יצא מספר של שתי ספרות, מחסרים ממנו 9,
   וזה כמו לחבר את שתי הספרות שלו.
3. סוכמים את כל מה שיצא. המספר תקין אם הסכום מתחלק ב-10.

הסעיפים בודקים מספר ביד ומוכיחים אילו טעויות נתפסות, משווים לתעודת הזהות ול-ISBN של ספרים,
מוכיחים שאין שיטה של "סכום מודולו 10" שתופסת הכול, ובסוף בונים בודק וגירוי ב-SystemVerilog.
כל המספרים בשאלה הם מספרי בדיקה מפורסמים או מספרים מומצאים, לא של אדם אמיתי.

??? interviewer "מה המראיין בודק"
    - **ביצוע מדויק :** מאיזה צד סופרים, אילו מקומות מכפילים, ומה עושים עם 18.
    - **מה אומר "תופס" :** האם המועמד מנסח טעות כשינוי בסכום, ושואל מתי השינוי מתחלק ב-10.
    - **הוכחה במקום דוגמאות :** תמורה על הספרות לטעות בודדת, והפרש של שתי פונקציות להחלפה.
    - **למה 11 ולא 10 :** חשבון מודולו מספר ראשוני, ומה עולה ספרה עם 11 ערכים.
    - **הצד של DV :** בודק שמקבל ספרה בכל מחזור, גירוי באילוצים שמייצר מספרים תקינים
      ולא תקינים בכוונה, ובדיקה של כל הטעויות האפשריות מול מודל.

---

### סעיף א – בודקים כרטיס ביד

1. האם <span dir="ltr">4111 1111 1111 1111</span> (מספר הבדיקה של Visa) תקין? ומה עם
   <span dir="ltr">4111 1111 1111 1112</span>?
2. מה צריכה להיות הספרה האחרונה של <span dir="ltr">4111 1111 1111 111?</span>?
3. הוכיחו ש-Luhn תופס כל טעות בספרה אחת.
4. אילו החלפות של שתי ספרות שכנות הוא לא תופס?

??? tip "רמז 1"
    טעות משנה את הסכום. היא חומקת רק אם השינוי מתחלק ב-10. כמה יכולה ספרה אחת לשנות את
    הסכום, במקום רגיל ובמקום מוכפל?

??? tip "רמז 2"
    כתבו טבלה : לכל ספרה \( d \) מ-0 עד 9, מה היא מוסיפה במקום מוכפל, ומה ההפרש בין זה לבין
    \( d \) עצמה. בהחלפה של שכנות אחת מהן תמיד במקום מוכפל והשנייה לא.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **תקין.** הסכום של <span dir="ltr">4111 1111 1111 1111</span> הוא 30, ושל
        <span dir="ltr">...1112</span> הוא 31, לא תקין. הספרה החסרה היא 1. כל טעות בספרה
        אחת נתפסת, כי ההכפלה מעבירה את 0 עד 9 לעשר ספרות שונות. מכל 45 הזוגות של ספרות שונות,
        ההחלפה של שכנות חומקת רק בזוג אחד : <span dir="ltr">09 ↔ 90</span>.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    נסמן ב-\( D(d) \) את מה שספרה \( d \) מוסיפה במקום מוכפל : \( 2d \) כש-\( d \le 4 \),
    ו-\( 2d - 9 \) כש-\( d \ge 5 \). מימין לשמאל, המקומות 2, 4, 6 ... מוכפלים, ובמספר של 16
    ספרות אלה הספרות הראשונה, השלישית וכן הלאה משמאל :

    <!-- gen 0 -->

    <div class="lu-fig"><svg class="lu-strip" viewBox="0 0 356 70" role="img" aria-label="המספר 4111 1111 1111 1111: ספרה בכל עמודה, והעמודות המודגשות הן המקומות שמכפילים, כל ספרה שנייה מימין. השורה התחתונה היא מה שכל ספרה מוסיפה. הסכום 30, מתחלק ב-10, ולכן המספר תקין"><rect class="lu-cell lu-dbl" x="13" y="5" width="19" height="60" rx="3"/><rect class="lu-cell" x="34" y="5" width="19" height="60" rx="3"/><rect class="lu-cell lu-dbl" x="55" y="5" width="19" height="60" rx="3"/><rect class="lu-cell" x="76" y="5" width="19" height="60" rx="3"/><rect class="lu-cell lu-dbl" x="97" y="5" width="19" height="60" rx="3"/><rect class="lu-cell" x="118" y="5" width="19" height="60" rx="3"/><rect class="lu-cell lu-dbl" x="139" y="5" width="19" height="60" rx="3"/><rect class="lu-cell" x="160" y="5" width="19" height="60" rx="3"/><rect class="lu-cell lu-dbl" x="181" y="5" width="19" height="60" rx="3"/><rect class="lu-cell" x="202" y="5" width="19" height="60" rx="3"/><rect class="lu-cell lu-dbl" x="223" y="5" width="19" height="60" rx="3"/><rect class="lu-cell" x="244" y="5" width="19" height="60" rx="3"/><rect class="lu-cell lu-dbl" x="265" y="5" width="19" height="60" rx="3"/><rect class="lu-cell" x="286" y="5" width="19" height="60" rx="3"/><rect class="lu-cell lu-dbl" x="307" y="5" width="19" height="60" rx="3"/><rect class="lu-cell" x="328" y="5" width="19" height="60" rx="3"/><text class="lu-t" x="22.5" y="25.4" text-anchor="middle">4</text><text class="lu-t" x="43.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="64.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="85.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="106.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="127.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="148.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="169.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="190.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="211.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="232.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="253.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="274.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="295.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="316.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="337.5" y="25.4" text-anchor="middle">1</text><line class="lu-rule" x1="12" x2="348" y1="35" y2="35"/><text class="lu-t" x="22.5" y="55.4" text-anchor="middle">8</text><text class="lu-t" x="43.5" y="55.4" text-anchor="middle">1</text><text class="lu-t" x="64.5" y="55.4" text-anchor="middle">2</text><text class="lu-t" x="85.5" y="55.4" text-anchor="middle">1</text><text class="lu-t" x="106.5" y="55.4" text-anchor="middle">2</text><text class="lu-t" x="127.5" y="55.4" text-anchor="middle">1</text><text class="lu-t" x="148.5" y="55.4" text-anchor="middle">2</text><text class="lu-t" x="169.5" y="55.4" text-anchor="middle">1</text><text class="lu-t" x="190.5" y="55.4" text-anchor="middle">2</text><text class="lu-t" x="211.5" y="55.4" text-anchor="middle">1</text><text class="lu-t" x="232.5" y="55.4" text-anchor="middle">2</text><text class="lu-t" x="253.5" y="55.4" text-anchor="middle">1</text><text class="lu-t" x="274.5" y="55.4" text-anchor="middle">2</text><text class="lu-t" x="295.5" y="55.4" text-anchor="middle">1</text><text class="lu-t" x="316.5" y="55.4" text-anchor="middle">2</text><text class="lu-t" x="337.5" y="55.4" text-anchor="middle">1</text></svg></div>

    <span class="viz-legend"><span><i class="lu-key-dbl"></i><span>מקום שמכפילים</span></span><span><i class="lu-key-cell"></i><span>מקום שלא נוגעים בו</span></span></span>

    ‏<span dir="ltr">4·2 = 8</span> בעמודה הראשונה, ושבע פעמים <span dir="ltr">1·2 = 2</span>. שאר הספרות נכנסות כמו שהן : <span dir="ltr">8 + 7·2 + 8·1 = 30</span>.

    <!-- /gen -->

    טעות חומקת אם ורק אם היא משנה את הסכום בכפולה של 10. לכן שואלים לכל סוג של טעות מה
    בדיוק השינוי, ומתי הוא מתחלק ב-10.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הבדיקה :** ב-<span dir="ltr">4111 1111 1111 1111</span> שמונה מקומות מוכפלים : ה-4
       נותן 8 וכל 1 נותן 2. שמונת האחרים נותנים 1 כל אחד. סה"כ \( 8 + 7 \cdot 2 + 8 = 30 \),
       תקין. החלפת ה-1 האחרון ב-2 מוסיפה 1, ו-31 לא מתחלק ב-10.
    2. **ספרת הביקורת :** מחשבים את הסכום עם 0 במקומה. ב-<span dir="ltr">4111 1111 1111 1110</span>
       הוא 29, וחסר 1 עד 30. באופן כללי הספרה היא \( (10 - S \bmod 10) \bmod 10 \).
    3. **טעות במקום רגיל :** \( a \) הופכת ל-\( b \), והסכום משתנה ב-\( b - a \), בין
       \( -9 \) ל-9 ולא 0. נתפסת.
    4. **טעות במקום מוכפל :** השינוי \( D(b) - D(a) \). שתי הסדרות בטבלה שלמטה מראות
       ש-\( D \) מעבירה את 0 עד 9 לעשר ספרות שונות, אז גם כאן השינוי בין \( -9 \) ל-9 ולא 0.
    5. **החלפת שכנות :** \( a \) במקום מוכפל ו-\( b \) לידה. לפני ההחלפה הן מוסיפות
       \( D(a) + b \), אחרי \( D(b) + a \). ההחלפה חומקת אם ורק אם
       \( D(a) - a \equiv D(b) - b \pmod{10} \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="luhn" linenums="1" hl_lines="10 11 12 22"
        def luhn_sum(number):
            """The Luhn sum of a string of digits (spaces and dashes are skipped): from the
            right, the check digit is place 1, and the digits of the even places are doubled,
            minus 9 when that gives two digits."""
            digits = [int(c) for c in number if c.isdigit()]
            total = 0
            for place, d in enumerate(reversed(digits), start=1):
                if place % 2 == 0:
                    d *= 2
                    if d > 9:
                        d -= 9                       # (1)!
                total += d
            return total


        def luhn_valid(number):
            return luhn_sum(number) % 10 == 0


        def check_digit(partial):
            """The digit that completes partial to a valid number."""
            return (10 - luhn_sum(partial + "0") % 10) % 10      # (2)!


        def missed_swaps():
            """The pairs of different digits whose swap, in two neighbouring places, keeps the
            sum: D(a) - a = D(b) - b (mod 10)."""
            D = [2 * d - 9 if d > 4 else 2 * d for d in range(10)]
            return [(a, b) for a in range(10) for b in range(a + 1, 10)
                    if (D[a] - a) % 10 == (D[b] - b) % 10]   # (3)!
        ```

        1. ‏12 נותן 3, כמו 1 + 2. בטבלה שלמטה : \( D \) של 5 עד 9 היא 1, 3, 5, 7, 9.
        2. עם 0 במקום הספרה, הספרה שחסרה עד הכפולה הבאה של 10. ספרת הביקורת במקום 1, שלא
           מוכפל, ולכן היא נכנסת לסכום כמו שהיא.
        3. מחזירה <span dir="ltr">[(0, 9)]</span>.

    === "SystemVerilog"
        ```systemverilog title="function automatic bit luhn_ok" linenums="1" hl_lines="9 10 12"
        // Luhn: digits[0] is the leftmost digit and the last one the check digit (place 1)
        function automatic bit luhn_ok(byte unsigned digits[$]);
          int sum, n, d;
          sum = 0;
          n = digits.size();
          for (int place = 1; place <= n; place++) begin
            d = digits[n - place];                    // (1)!
            if (place % 2 == 0) begin
              d = 2 * d;
              if (d > 9) d -= 9;
            end
            sum += d;
          end
          return sum % 10 == 0;
        endfunction
        ```

        1. מימין לשמאל : המקום 1 הוא האיבר האחרון של התור.

    #### למה זה נכון { .sol-proof }

    <!-- gen 1 -->

    <div class="lu-fig"><svg class="lu-strip" viewBox="0 0 362 100" role="img" aria-label="שלוש שורות לכל ספרה d מ-0 עד 9: הספרה, מה שהיא מוסיפה במקום מוכפל, וההפרש בין השניים מודולו 10. השורה האמצעית היא כל הספרות מ-0 עד 9 בסדר אחר, ולכן כל טעות בספרה אחת נתפסת. בשורה התחתונה 0 מופיע פעמיים, אצל 0 ואצל 9, ולכן ההחלפה של 09 ו-90 חומקת"><rect class="lu-cell lu-hit" x="65" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="94" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="123" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="152" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="181" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="210" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="239" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="268" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="297" y="5" width="27" height="90" rx="3"/><rect class="lu-cell lu-hit" x="326" y="5" width="27" height="90" rx="3"/><text class="lu-lab" x="58" y="25.4" direction="ltr" text-anchor="end">d</text><text class="lu-t" x="78.5" y="25.4" text-anchor="middle">0</text><text class="lu-t" x="107.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="136.5" y="25.4" text-anchor="middle">2</text><text class="lu-t" x="165.5" y="25.4" text-anchor="middle">3</text><text class="lu-t" x="194.5" y="25.4" text-anchor="middle">4</text><text class="lu-t" x="223.5" y="25.4" text-anchor="middle">5</text><text class="lu-t" x="252.5" y="25.4" text-anchor="middle">6</text><text class="lu-t" x="281.5" y="25.4" text-anchor="middle">7</text><text class="lu-t" x="310.5" y="25.4" text-anchor="middle">8</text><text class="lu-t" x="339.5" y="25.4" text-anchor="middle">9</text><line class="lu-rule" x1="64" x2="354" y1="35" y2="35"/><text class="lu-lab" x="58" y="55.4" direction="ltr" text-anchor="end">D(d)</text><text class="lu-t" x="78.5" y="55.4" text-anchor="middle">0</text><text class="lu-t" x="107.5" y="55.4" text-anchor="middle">2</text><text class="lu-t" x="136.5" y="55.4" text-anchor="middle">4</text><text class="lu-t" x="165.5" y="55.4" text-anchor="middle">6</text><text class="lu-t" x="194.5" y="55.4" text-anchor="middle">8</text><text class="lu-t" x="223.5" y="55.4" text-anchor="middle">1</text><text class="lu-t" x="252.5" y="55.4" text-anchor="middle">3</text><text class="lu-t" x="281.5" y="55.4" text-anchor="middle">5</text><text class="lu-t" x="310.5" y="55.4" text-anchor="middle">7</text><text class="lu-t" x="339.5" y="55.4" text-anchor="middle">9</text><line class="lu-rule" x1="64" x2="354" y1="65" y2="65"/><text class="lu-lab" x="58" y="85.4" direction="ltr" text-anchor="end">D−d</text><text class="lu-t lu-sum" x="78.5" y="85.4" text-anchor="middle">0</text><text class="lu-t lu-sum" x="107.5" y="85.4" text-anchor="middle">1</text><text class="lu-t lu-sum" x="136.5" y="85.4" text-anchor="middle">2</text><text class="lu-t lu-sum" x="165.5" y="85.4" text-anchor="middle">3</text><text class="lu-t lu-sum" x="194.5" y="85.4" text-anchor="middle">4</text><text class="lu-t lu-sum" x="223.5" y="85.4" text-anchor="middle">6</text><text class="lu-t lu-sum" x="252.5" y="85.4" text-anchor="middle">7</text><text class="lu-t lu-sum" x="281.5" y="85.4" text-anchor="middle">8</text><text class="lu-t lu-sum" x="310.5" y="85.4" text-anchor="middle">9</text><text class="lu-t lu-sum" x="339.5" y="85.4" text-anchor="middle">0</text></svg></div>

    <span class="viz-legend"><span><i class="lu-key-hit"></i><span>אותו הפרש אצל {ltr("0")} ו-{ltr("9")}</span></span></span>

    <!-- /gen -->

    **טעות בספרה אחת.** בשורה האמצעית של הטבלה כל ספרה מ-0 עד 9 מופיעה פעם אחת :
    \( 0, 2, 4, 6, 8 \) מ-0 עד 4, ו-\( 1, 3, 5, 7, 9 \) מ-5 עד 9. לכן \( D(a) \ne D(b) \)
    כש-\( a \ne b \), וההפרש בין שתי ספרות שונות אף פעם לא מתחלק ב-10.

    **החלפת שכנות.** \( D(d) - d \) הוא \( d \) כש-\( d \le 4 \), ו-\( d - 9 \equiv d + 1 \)
    כש-\( d \ge 5 \). הערכים מודולו 10 הם \( 0, 1, 2, 3, 4, 6, 7, 8, 9, 0 \) : כולם שונים, חוץ
    מ-0 ו-9 ששניהם 0. לכן מבין 45 הזוגות, ההחלפה חומקת רק ב-<span dir="ltr">09 ↔ 90</span>,
    ובכל מקום במספר. למשל ב-<span dir="ltr">4111 1111 1110 9115</span> (תקין, סכום 40) החלפת
    ה-0 וה-9 נותנת <span dir="ltr">4111 1111 1119 0115</span>, גם הוא תקין.

    <div class="explorer" data-kind="luhn" data-number="4111111111111111" data-scheme="ean" data-map="swap"></div>

    #### סיבוכיות { .sol-cost }

    מעבר אחד על \( n \) הספרות, \( O(n) \), וזיכרון \( O(1) \) : הסכום מודולו 10 וביט של
    "המקום הבא מוכפל".

---

### סעיף ב – תעודת זהות ו-ISBN

1. מספר תעודת הזהות בישראל הוא 9 ספרות (משלימים ב-0 משמאל), והאחרונה היא ספרת ביקורת :
   כופלים את הספרות משמאל לסירוגין ב-1 וב-2, מכל מכפלה של שתי ספרות מחסרים 9, והסכום צריך
   להתחלק ב-10. בדקו את המספר המומצא <span dir="ltr">000000018</span>, והראו שזה בדיוק Luhn.
2. ב-ISBN-10 של ספר כופלים את 10 הספרות משמאל במשקלים 10, 9 ... 1, והסכום צריך להתחלק
   ב-11. ספרת ביקורת 10 נכתבת X. בדקו את <span dir="ltr">0-306-40615-2</span>.
3. הוכיחו ש-ISBN-10 תופס כל טעות בספרה אחת, וכל החלפה של שתי ספרות, גם לא שכנות.
4. למה ב-ISBN צריך את X?

??? tip "רמז 1"
    בתעודת הזהות 9 ספרות. איזה מקום מימין מקבל את המשקל 1 של הספרה הראשונה משמאל?

??? tip "רמז 2"
    ב-ISBN, טעות משנה את הסכום במכפלה של שני מספרים, שאף אחד מהם לא מתחלק ב-11. מה מיוחד
    במכפלה כזו כש-11 ראשוני?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **תקין, ותקין.** בתעודת הזהות המשקלים 1 ו-2 משמאל במספר של 9 ספרות נופלים בדיוק על
        המקומות הזוגיים מימין, כלומר זה Luhn : ב-<span dir="ltr">000000018</span> הסכום
        \( 1 \cdot 2 + 8 = 10 \). ב-ISBN הסכום 132, שהוא \( 12 \cdot 11 \). כל טעות בספרה
        אחת וכל החלפה של שתי ספרות משנות את הסכום במכפלה של שני גורמים שאינם מתחלקים ב-11,
        ולכן גם המכפלה לא מתחלקת. ה-X נחוץ כי ספרת הביקורת צריכה 11 ערכים, מ-0 עד 10.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **תעודת זהות.** במספר של 9 ספרות, הספרה הראשונה משמאל היא המקום 9 מימין, אי-זוגי, ולכן
    משקל 1. השנייה היא המקום 8, זוגי, ומשקל 2. וכן הלאה : המשקל 2 נופל על כל מקום זוגי מימין,
    כמו ב-Luhn. ההשלמה ב-0 משמאל לא משנה דבר, כי 0 מוסיף 0 בכל מקום.

    ‏**ISBN-10.** ב-<span dir="ltr">0-306-40615-2</span> המכפלות של הספרות במשקלים :

    <!-- gen 2 -->

    <div class="lu-fig"><svg class="lu-strip" viewBox="0 0 362 100" role="img" aria-label="ה-ISBN 0306406152: הספרות, המשקלים מ-10 עד 1 והמכפלות. הסכום 132, שהוא 12 כפול 11, ולכן המספר תקין"><rect class="lu-cell" x="65" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="94" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="123" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="152" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="181" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="210" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="239" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="268" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="297" y="5" width="27" height="90" rx="3"/><rect class="lu-cell" x="326" y="5" width="27" height="90" rx="3"/><text class="lu-lab" x="58" y="25.4" direction="rtl" text-anchor="start">ספרה</text><text class="lu-t" x="78.5" y="25.4" text-anchor="middle">0</text><text class="lu-t" x="107.5" y="25.4" text-anchor="middle">3</text><text class="lu-t" x="136.5" y="25.4" text-anchor="middle">0</text><text class="lu-t" x="165.5" y="25.4" text-anchor="middle">6</text><text class="lu-t" x="194.5" y="25.4" text-anchor="middle">4</text><text class="lu-t" x="223.5" y="25.4" text-anchor="middle">0</text><text class="lu-t" x="252.5" y="25.4" text-anchor="middle">6</text><text class="lu-t" x="281.5" y="25.4" text-anchor="middle">1</text><text class="lu-t" x="310.5" y="25.4" text-anchor="middle">5</text><text class="lu-t" x="339.5" y="25.4" text-anchor="middle">2</text><line class="lu-rule" x1="64" x2="354" y1="35" y2="35"/><text class="lu-lab" x="58" y="55.4" direction="rtl" text-anchor="start">משקל</text><text class="lu-t" x="78.5" y="55.4" text-anchor="middle">10</text><text class="lu-t" x="107.5" y="55.4" text-anchor="middle">9</text><text class="lu-t" x="136.5" y="55.4" text-anchor="middle">8</text><text class="lu-t" x="165.5" y="55.4" text-anchor="middle">7</text><text class="lu-t" x="194.5" y="55.4" text-anchor="middle">6</text><text class="lu-t" x="223.5" y="55.4" text-anchor="middle">5</text><text class="lu-t" x="252.5" y="55.4" text-anchor="middle">4</text><text class="lu-t" x="281.5" y="55.4" text-anchor="middle">3</text><text class="lu-t" x="310.5" y="55.4" text-anchor="middle">2</text><text class="lu-t" x="339.5" y="55.4" text-anchor="middle">1</text><line class="lu-rule" x1="64" x2="354" y1="65" y2="65"/><text class="lu-lab" x="58" y="85.4" direction="rtl" text-anchor="start">מכפלה</text><text class="lu-t lu-sum" x="78.5" y="85.4" text-anchor="middle">0</text><text class="lu-t lu-sum" x="107.5" y="85.4" text-anchor="middle">27</text><text class="lu-t lu-sum" x="136.5" y="85.4" text-anchor="middle">0</text><text class="lu-t lu-sum" x="165.5" y="85.4" text-anchor="middle">42</text><text class="lu-t lu-sum" x="194.5" y="85.4" text-anchor="middle">24</text><text class="lu-t lu-sum" x="223.5" y="85.4" text-anchor="middle">0</text><text class="lu-t lu-sum" x="252.5" y="85.4" text-anchor="middle">24</text><text class="lu-t lu-sum" x="281.5" y="85.4" text-anchor="middle">3</text><text class="lu-t lu-sum" x="310.5" y="85.4" text-anchor="middle">10</text><text class="lu-t lu-sum" x="339.5" y="85.4" text-anchor="middle">2</text></svg></div>

    ‏<span dir="ltr">0 + 27 + 0 + 42 + 24 + 0 + 24 + 3 + 10 + 2 = 132 = 12 · 11</span>.

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **תעודת זהות :** שבעה אפסים, אחר כך 1 במשקל 2 ו-8 במשקל 1 : \( 2 + 8 = 10 \), תקין.
       עם 9 בסוף הסכום 11, לא תקין.
    2. ‏**ISBN, הבדיקה :** \( \sum_{i=1}^{10} (11 - i)\, x_i = 132 = 12 \cdot 11 \), תקין.
    3. **טעות בספרה אחת :** ספרה במשקל \( w \) הופכת מ-\( a \) ל-\( b \). הסכום משתנה
       ב-\( w(b - a) \), כש-\( 1 \le w \le 10 \) ו-\( 1 \le |b - a| \le 10 \).
    4. **החלפה של שתי ספרות :** \( a \) במשקל \( w_i \) ו-\( b \) במשקל \( w_j \) מתחלפות.
       הסכום משתנה ב-\( (w_i - w_j)(b - a) \), כש-\( 1 \le |w_i - w_j| \le 9 \).
    5. **ה-X :** ספרת הביקורת היא במשקל 1, ולכן היא \( -\sum_{i=1}^{9} (11 - i)\,x_i \bmod 11 \),
       מספר מ-0 עד 10. כשיוצא 10 כותבים X, כמו ב-<span dir="ltr">0-8044-2957-X</span>.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="israeli_id_valid, isbn10_valid" linenums="1" hl_lines="10 21"
        def israeli_id_valid(id_number):
            """An Israeli ID number: 9 digits, padded with zeros on the left; weights 1, 2, 1,
            2 ... from the left, a two-digit product counted as the sum of its digits."""
            s = id_number.strip().zfill(9)
            if len(s) != 9 or not s.isdigit():
                return False
            total = 0
            for i, c in enumerate(s):
                p = int(c) * (1 if i % 2 == 0 else 2)
                total += p - 9 if p > 9 else p          # (1)!
            return total % 10 == 0


        def isbn10_valid(isbn):
            """ISBN-10: weights 10, 9 ... 1 from the left, the sum a multiple of 11; the
            check digit 10 is written X."""
            s = isbn.replace("-", "").replace(" ", "").upper()
            if len(s) != 10 or not s[:9].isdigit() or not (s[9].isdigit() or s[9] == "X"):
                return False
            values = [int(c) for c in s[:9]] + [10 if s[9] == "X" else int(s[9])]
            return sum((10 - i) * v for i, v in enumerate(values)) % 11 == 0   # (2)!
        ```

        1. ‏Luhn בדיוק : המשקל 2 על המקומות הזוגיים מימין. הבדיקות משוות אותה ל-`luhn_valid`
           על מספרים אקראיים.
        2. ‏`i = 0` היא הספרה השמאלית, במשקל 10.

    === "SystemVerilog"
        ```systemverilog title="function automatic bit isbn10_ok" linenums="1" hl_lines="6"
        // ISBN-10: v[0] is the leftmost digit and v[9] the check digit, 10 for an X
        function automatic bit isbn10_ok(byte unsigned v[10]);
          int sum;
          sum = 0;
          for (int i = 0; i < 10; i++)
            sum += (10 - i) * v[i];                   // (1)!
          return sum % 11 == 0;
        endfunction
        ```

        1. הסכום הגדול ביותר הוא \( 10 \cdot 55 = 550 \), הרבה פחות מהטווח של `int`.

    #### למה זה נכון { .sol-proof }

    **11 ראשוני.** אם ראשוני \( p \) מחלק מכפלה \( xy \), הוא מחלק את \( x \) או את \( y \).
    בטעות בספרה אחת \( x = w \) ו-\( y = b - a \), שניהם בין 1 ל-10 בערך מוחלט, ו-11 לא מחלק
    אף אחד מהם. בהחלפה \( x = w_i - w_j \) ו-\( y = b - a \), שוב שניהם בין 1 ל-10 בערך
    מוחלט. לכן השינוי אף פעם לא כפולה של 11, וכל טעות כזו נתפסת, גם בין ספרות רחוקות.

    **מה עולה הביטחון.** ספרה עשרונית אחת יכולה לקבל רק 10 ערכים, וספרת ביקורת מודולו 11
    צריכה 11. ה-X הוא המחיר : ISBN-13 החדש עבר למשקלים 1 ו-3 מודולו 10, כמו ברקוד, ושם
    החלפה של שתי שכנות שההפרש ביניהן 5 חומקת.

    #### סיבוכיות { .sol-cost }

    מעבר אחד על הספרות, \( O(n) \), וזיכרון \( O(1) \).

---

### סעיף ג – אין שיטה מושלמת מודולו 10

1. בשיטה של **סכום משוקלל מודולו 10**, כל מקום \( i \) כופל את הספרה שלו במשקל \( w_i \).
   הראו שאי אפשר לבחור משקלים שיתפסו גם כל טעות בספרה אחת וגם כל החלפה של שתי שכנות.
2. ‏Luhn אינו סכום משוקלל : במקום מוכפל הוא מחליף את הספרה לפי הטבלה \( D \). הראו שגם כל
   שיטה שבה כל מקום מעביר את הספרה דרך תמורה כלשהי של 0 עד 9 וסוכמים מודולו 10, מפספסת
   לפחות החלפה אחת של שכנות. מה זה אומר על Luhn?
3. איך ISBN-10 מצליח לתפוס את שני הסוגים?

??? tip "רמז 1"
    כדי לתפוס כל טעות בספרה אחת, איזה משקלים מותרים? נסו 2 ו-5, וחשבו על הפרש של 5 או של 2.

??? tip "רמז 2"
    לתמורות : אם \( g(d) \) עוברת על כל השאריות מ-0 עד 9, מה הסכום של \( g(0) + \dots + g(9) \)
    מודולו 10? וכמה הוא יוצא כש-\( g \) היא הפרש של שתי תמורות?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        **אין כזו.** לטעות בודדת כל משקל חייב להיות 1, 3, 7 או 9, ולהחלפה גם ההפרש בין
        משקלים שכנים חייב להיות כזה, אבל ההפרש של שני אי-זוגיים זוגי. ובתמורות : אילו
        ההפרש \( g \) בין שני מקומות שכנים היה עובר על כל השאריות, הסכום שלו היה
        \( 45 \equiv 5 \), אבל הסכום של הפרש של שתי תמורות הוא 0. לכן כל שיטה כזו מפספסת
        לפחות זוג אחד, ו-Luhn, שמפספס בדיוק אחד, הוא הטוב ביותר שאפשר. ISBN עובר למודולו 11,
        ומשלם ב-X.

    <!-- cost: זמן \( O(1) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    הטבלה משווה ארבע שיטות : כמה מ-90 הטעויות הבודדות (ספרה \( a \) שהפכה ל-\( b \)) וכמה
    מ-45 ההחלפות של שכנות כל אחת מפספסת. כל שיטה מודולו 10 נכשלת במשהו :

    <!-- gen 3 -->

    | השיטה | טעות בספרה אחת שחומקת | החלפת שכנות שחומקת |
    |---|---|---|
    | ‏Luhn : כפל ב-2 וסכום ספרות | אף אחת | ‏1 מתוך 45 : <span dir="ltr">09 ↔ 90</span> |
    | משקלים 1 ו-2, בלי סכום ספרות | ‏10 מתוך 90 (הפרש 5) | אף אחת |
    | ברקוד EAN-13, משקלים 1 ו-3 | אף אחת | ‏5 מתוך 45 (הפרש 5) |
    | ‏ISBN-10 : משקלים 10 עד 1, מודולו 11 | אף אחת | אף אחת |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **טעות בודדת :** השינוי \( w(b - a) \), ו-\( b - a \) עובר על כל המספרים מ-1 עד 9.
       אם \( w \) זוגי, \( w \cdot 5 \equiv 0 \). אם \( w \) מתחלק ב-5, \( w \cdot 2 \equiv 0 \).
       לכן \( w \in \{1, 3, 7, 9\} \), זרים ל-10.
    2. **החלפה :** השינוי \( (w_i - w_{i+1})(b - a) \). מאותה סיבה גם \( w_i - w_{i+1} \)
       צריך להיות זר ל-10.
    3. **הסתירה :** \( w_i \) ו-\( w_{i+1} \) שניהם אי-זוגיים, וההפרש שלהם זוגי. החלפה של
       שתי ספרות שההפרש ביניהן 5 חומקת, למשל 1 ו-6 בברקוד עם המשקלים 1 ו-3.
    4. **תמורות :** מקום \( i \) מוסיף \( \sigma_i(d) \). החלפת \( a \) ו-\( b \) בין \( i \)
       ל-\( i + 1 \) חומקת אם ורק אם \( g(a) = g(b) \), כש-\( g = \sigma_i - \sigma_{i+1} \)
       מודולו 10.
    5. **סכום של שאריות :** אילו \( g \) הייתה עוברת על כל השאריות,
       \( \sum_d g(d) \equiv 0 + 1 + \dots + 9 = 45 \equiv 5 \). אבל
       \( \sum_d g(d) = \sum_d \sigma_i(d) - \sum_d \sigma_{i+1}(d) = 45 - 45 = 0 \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="misses" linenums="1" hl_lines="7 8 9"
        def misses(odd, even, mod=10):
            """A scheme where a digit d adds odd(d) in the places 1, 3, 5 ... from the right and
            even(d) in the places 2, 4, 6 ..., summed mod `mod`: the single changes a -> b and
            the neighbour swaps {a, b} that keep the sum."""
            singles = [(a, b) for a in range(10) for b in range(10) if a != b
                       and ((odd(a) - odd(b)) % mod == 0 or (even(a) - even(b)) % mod == 0)]
            swaps = [(a, b) for a in range(10) for b in range(a + 1, 10)
                     if (odd(a) + even(b) - odd(b) - even(a)) % mod == 0]   # (1)!
            return singles, swaps


        def no_perfect_weights():
            """Every pair of neighbour weights mod 10 misses a single change or a swap."""
            return all(sum(map(len, misses(lambda d: w1 * d, lambda d: w2 * d))) > 0
                       for w1 in range(10) for w2 in range(10))         # (2)!
        ```

        1. ‏\( a \) במקום אי-זוגי ו-\( b \) לידה במקום זוגי, לפני ואחרי ההחלפה.
        2. מחזירה `True` : אף אחד מ-100 הזוגות של משקלים לא תופס הכול. הבדיקות מוסיפות
           חיפוש על כל התמורות, שלא מוצא \( \sigma \) שבה \( \sigma(d) - d \) עוברת על כל
           השאריות.

    #### למה זה נכון { .sol-proof }

    ‏**Luhn הוא הטוב ביותר מסוגו.** ב-Luhn \( \sigma_{\text{odd}}(d) = d \)
    ו-\( \sigma_{\text{even}} = D \), ו-\( g(d) = d - D(d) \) מקבלת את אותו ערך רק ב-0 וב-9. לפי
    הסעיף, כל שיטה מהסוג הזה מפספסת לפחות זוג אחד, ולכן אחד הוא המינימום.

    **למה זה לא עובד מודולו 10 ועובד מודולו 11.** הסתירה נשענת על כך ש-\( 45 \) אינו כפולה
    של 10. מודולו 11 \( 0 + 1 + \dots + 10 = 55 \equiv 0 \), ואין סתירה : \( g(d) = d \) עם
    המשקלים \( w \) ו-\( w + 1 \) עוברת על כל השאריות. באופן כללי, מודולו מספר אי-זוגי יש
    תמורה כזו, ומודולו מספר זוגי אין.

    **איך עוקפים בלי X.** ‏Verhoeff ו-Damm לא סוכמים בכלל : Verhoeff מחשב בחבורה שאינה
    חילופית, ו-Damm בטבלה של 10 על 10. שתיהן תופסות כל טעות בספרה אחת וכל החלפה של שכנות
    עם ספרת ביקורת עשרונית אחת. השאלות בסוף העמוד חוזרות לזה.

    <div class="explorer" data-kind="luhn" data-number="4111111111109115" data-scheme="w12" data-map="single"></div>

    #### סיבוכיות { .sol-cost }

    הבדיקה של שיטה עוברת על 90 טעויות בודדות ו-45 החלפות, \( O(1) \). החיפוש על כל זוגות
    המשקלים הוא 100 שיטות כאלה.

---

### סעיף ד – גירוי ובודק ב-SystemVerilog

בודק Luhn בחומרה מקבל ספרה אחת בכל מחזור שעון, מימין לשמאל, ומודיע בסוף אם המספר תקין.

1. כתבו את הבודק. כמה ביטים של מצב הוא צריך?
2. כתבו מחלקה שמגרילה מספרי כרטיס של 16 ספרות באילוצים, תקינים או לא תקינים לפי ביט
   `valid`.
3. איך בודקים שהבודק תופס בדיוק את מה שהמודל אומר?

??? tip "רמז 1"
    מה הבודק צריך לזכור בין ספרה לספרה? לא את כל הסכום.

??? tip "רמז 2"
    באילוצים קשה לכתוב "מכפילים, ואם יצא יותר מ-9 מחסרים 9" בתוך סכום. הוסיפו מערך עזר
    אקראי של מה שכל ספרה מוסיפה, עם אילוץ לכל איבר.

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        **חמישה ביטים.** הסכום מודולו 10 (4 ביטים) וביט שאומר אם המקום הבא מוכפל. כל ספרה
        מוסיפה \( d \) או \( D(d) \), והסכום נשאר קטן מ-10 בעזרת חיסור של 10. במחלקה, מערך
        עזר `c` מחזיק את מה שכל ספרה מוסיפה, ואילוץ על `c.sum()` מודולו 10 קובע אם המספר
        תקין. הבדיקה מריצה מספרים אקראיים, וכל טעות בספרה אחת וכל החלפה של שכנות במספרי
        דוגמה, ומשווה את הבודק למודל.

    <!-- cost: זמן \( O(n) \) מחזורים | זיכרון 5 ביטים -->

    #### הרעיון { .sol-idea }

    הבודק זוכר רק את מה שישפיע על התשובה : השארית של הסכום מודולו 10, ואם המקום הבא מוכפל.
    \( (s + x) \bmod 10 \) תלוי רק ב-\( s \bmod 10 \), ולכן אין צורך בסכום המלא. הגירוי
    מייצר גם מספרים לא תקינים בכוונה, ומעליהם טעויות שהמודל יודע מראש אם הן נתפסות.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המצב :** `sum` של 4 ביטים ו-`dbl` של ביט אחד. `start` מאפס את שניהם עם הספרה
       הראשונה, ספרת הביקורת.
    2. **ספרה :** מוסיפים `dbl ? D(digit) : digit`, ואם הסכום 10 או יותר מחסרים 10. הופכים
       את `dbl`.
    3. **סוף :** עם `last` הבודק מוציא, במחזור הבא, `done` ו-`ok = (sum == 0)`.
    4. **הגירוי :** `d[0]` היא ספרת הביקורת. `c[i]` שווה ל-`d[i]` במקום רגיל ול-\( D(d_i) \)
       במקום מוכפל, ו-`valid` קובע אם הסכום מתחלק ב-10.
    5. **הבדיקה :** לכל מספר שהוגרל, הבודק מסכים עם `luhn_ok`. בכל מספר דוגמה : כל 144 הטעויות
       הבודדות נתפסות, ובהחלפות של שכנות הבודק מסכים עם המודל, כולל ההחלפה של 0 ו-9 שחומקת.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="random_card, mutations" linenums="1" hl_lines="7 8 18 23"
        import random


        def random_card(valid, rng, n=16):
            """A random n-digit number whose Luhn sum ends in 0 (valid) or does not."""
            body = "".join(str(rng.randrange(10)) for _ in range(n - 1))
            c = check_digit(body)
            if not valid:
                c = (c + rng.randrange(1, 10)) % 10                 # (1)!
            return body + str(c)


        def mutations(number):
            """Every single-digit change and every swap of two different neighbours, as
            (kind, place from the left, the new number)."""
            out = []
            for i, ch in enumerate(number):
                for b in "0123456789":
                    if b != ch:
                        out.append(("single", i, number[:i] + b + number[i + 1:]))
            for i in range(len(number) - 1):
                if number[i] != number[i + 1]:
                    out.append(("swap", i, number[:i] + number[i + 1] + number[i] + number[i + 2:]))
            return out
        ```

        1. כל ספרה אחרת במקום 1 משנה את הסכום ב-1 עד 9, ולכן המספר לא תקין.

    === "SystemVerilog"
        ```systemverilog title="module luhn_checker" linenums="1" hl_lines="18 19 20"
        // Luhn in hardware: one digit a cycle, the check digit first (with start) and the
        // leftmost digit last (with last); done and ok come one cycle after last
        module luhn_checker (
          input  logic       clk, rst_n,
          input  logic       in_valid,      // a digit on `digit` this cycle
          input  logic       start,         // the first digit of a number, its check digit
          input  logic       last,          // the leftmost digit of the number
          input  logic [3:0] digit,
          output logic       done,
          output logic       ok);
          logic [3:0] sum;                  // the sum so far, mod 10
          logic       dbl;                  // the place of the next digit is doubled
          logic [3:0] s0;
          logic       d0;
          logic [4:0] add, total;
          always_comb begin
            s0 = start ? 4'd0 : sum;
            d0 = start ? 1'b0 : dbl;
            add = !d0 ? {1'b0, digit} : digit > 4 ? 5'(2 * digit - 9) : 5'(2 * digit);   // (1)!
            total = 5'(s0) + add;
            if (total >= 10) total = total - 10;                                      // (2)!
          end
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin
              sum <= '0; dbl <= 1'b0; done <= 1'b0; ok <= 1'b0;
            end else begin
              done <= in_valid && last;
              if (in_valid) begin
                sum <= total[3:0];
                dbl <= ~d0;
                if (last) ok <= (total == 0);
              end
            end
        endmodule
        ```

        1. ‏\( D \) בחומרה : הכפלה היא הזזה ב-1, והחיסור של 9 קורה רק מ-5 ומעלה.
        2. ‏\( s_0 \le 9 \) ו-\( \text{add} \le 9 \), אז הסכום עד 18, וחיסור אחד של 10 מספיק.

        ```systemverilog title="class luhn_gen" linenums="1" hl_lines="10 11 12 15 16"
        // Random 16-digit card numbers, valid or not as `valid` says; d[0] is the check
        // digit (place 1, the rightmost) and d[15] the leftmost digit
        class luhn_gen;
          rand bit [3:0] d[16];
          rand bit [4:0] c[16];             // what each digit adds to the sum
          rand bit       valid;
          constraint digits_c { foreach (d[i]) d[i] < 10; }
          constraint adds_c {
            foreach (d[i])
              if (i % 2 == 0) c[i] == d[i];                // (1)!
              else if (d[i] < 5) c[i] == 2 * d[i];
              else c[i] == 2 * d[i] - 9;
          }
          constraint sum_c {
            valid -> (c.sum() with (int'(item))) % 10 == 0;
            !valid -> (c.sum() with (int'(item))) % 10 != 0;   // (2)!
          }
        endclass
        ```

        1. ‏`i` מתחיל ב-0, ולכן המקום מימין הוא `i + 1` : `i` זוגי הוא מקום אי-זוגי, שלא מוכפל.
        2. ‏`int'(item)` לפני הסכום, אחרת הסכום מחושב ברוחב של 5 ביטים ונחתך.

    #### למה זה נכון { .sol-proof }

    **המצב מספיק.** אחרי \( k \) ספרות, `sum` הוא סכום Luhn של \( k \) הספרות הימניות מודולו
    10, ו-`dbl` הוא 1 אם ורק אם \( k \) אי-זוגי, כלומר המקום \( k + 1 \) זוגי. באינדוקציה :
    הספרה ה-\( (k+1) \) מוסיפה בדיוק את מה ש-Luhn מוסיף במקומה, והחיבור מודולו 10 שומר על
    השארית. אחרי הספרה האחרונה `sum` הוא הסכום מודולו 10, ו-`ok` נכון אם ורק אם הוא 0.

    **הגירוי נכון.** האילוצים על `c` הם בדיוק ההגדרה של Luhn, אז `c.sum()` הוא סכום Luhn של
    `d`, והאילוץ האחרון קובע את התשובה. הפותר בוחר מספר שמקיים את כולם, ולכן כל מספר
    עם `valid = 1` תקין וכל מספר עם `valid = 0` לא תקין. לפי התקן הפותר בוחר באחידות מבין
    כל הפתרונות, ורק עשירית מהם תקינים : לכל 15 ספרות יש ספרת ביקורת אחת. לכן הבדיקה קובעת
    את `valid` בכל קריאה, ב-`randomize() with`, ולא משאירה אותו להגרלה.

    **מה הבדיקה מכסה.** מספרים אקראיים בודקים את הנתיב הרגיל. הטעויות שנוצרות בכוונה בודקות
    בדיוק את המקרים שהשאלה עוסקת בהם, כולל ההחלפה היחידה שחומקת : ב-<span dir="ltr">4111 1111 1110 9115</span>
    הבודק חייב להגיד "תקין" גם אחרי ההחלפה של ה-0 וה-9, כי גם המודל אומר את זה.

    #### סיבוכיות { .sol-cost }

    מחזור אחד לספרה, 16 מחזורים לכרטיס ועוד אחד לתשובה. המצב 5 פליפ-פלופים, ובנתיב יש
    מחבר של 5 ביטים, השוואה ל-10 וטבלה של \( D \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לספור משמאל"
    ‏Luhn סופר מימין. במספר של 16 ספרות, ספירה משמאל מכפילה את המקומות הלא נכונים,
    ו-<span dir="ltr">4111 1111 1111 1111</span> נותן 27 ולא 30. במספר של 15 ספרות, כמו
    בכרטיסי American Express, הספרה הראשונה משמאל כבר לא מוכפלת.

??? trap "מלכודת : 18 נכנס כ-18"
    במקום מוכפל 9 נותן 18, ומחסרים 9 : 9. בלי החיסור 5 ו-0 במקום מוכפל נותנים 10 ו-0,
    שמודולו 10 שווים, וטעות בין 5 ל-0 חומקת. זו בדיוק השיטה של המשקלים 1 ו-2 בטבלה של סעיף ג.

??? trap "מלכודת : תקין זה לא אמיתי"
    ספרת הביקורת תופסת טעויות הקלדה, לא זיופים : כל מי שמכיר את האלגוריתם מייצר מספר "תקין"
    בשנייה, כמו בסעיף ד. בדיקת Luhn באתר רק חוסכת פנייה לבנק עם מספר שהוקלד לא נכון.

??? trap "מלכודת : הסכום ברוחב של 5 ביטים"
    ב-SystemVerilog, `c.sum()` בלי `with (int'(item))` מחושב ברוחב של האיברים, 5 ביטים. סכום
    של 16 ספרות מגיע עד 144, נחתך, והאילוץ מודולו 10 בודק מספר אחר.

??? followup "שאלות המשך"
    - **טעויות תאומות :** ‏<span dir="ltr">aa</span> שהופך ל-<span dir="ltr">bb</span>, כמו
      הקלדה של 22 במקום 55. אילו כאלה Luhn מפספס?

        ??? fu-answer "תשובה"
            הזוג מוסיף \( d + D(d) \), שהוא \( 3d \) כש-\( d \le 4 \) ו-\( 3d - 9 \) מ-5.
            מודולו 10 יש שלוש התנגשויות : <span dir="ltr">22 ↔ 55</span>,
            <span dir="ltr">33 ↔ 66</span> ו-<span dir="ltr">44 ↔ 77</span>.

    - **החלפה בקפיצה :** ‏<span dir="ltr">abc</span> שהופך ל-<span dir="ltr">cba</span>. כמה
      מהן Luhn תופס?

        ??? fu-answer "תשובה"
            אף אחת. \( a \) ו-\( c \) באותו סוג של מקום, שניהם מוכפלים או שניהם לא, אז
            ההחלפה ביניהן לא משנה את הסכום. ‏ISBN-10 תופס גם אותן.

    - **‏Damm :** איך ספרת ביקורת עשרונית אחת תופסת כל טעות בודדת וכל החלפה של שכנות?

        ??? fu-answer "תשובה"
            מחליפים את הסכום בטבלה \( T \) של 10 על 10 : \( s \leftarrow T[s][d] \) לכל ספרה,
            והמספר תקין אם \( s = 0 \). הטבלה בנויה כך שכל שורה וכל עמודה הן תמורה (טעות
            בודדת נתפסת), ו-\( T[T[s][a]][b] \ne T[T[s][b]][a] \) כש-\( a \ne b \) (החלפה
            נתפסת). זו לא חבורה חילופית, ולכן ההוכחה של סעיף ג לא חלה עליה.
