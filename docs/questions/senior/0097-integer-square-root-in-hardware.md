---
id: 97
title: שורש ריבועי בחומרה, ביט אחרי ביט
level: senior
difficulty: hard
kind: design
tags: [digital-design, bitwise, algorithms, proof, python, systemverilog]
source: "השיטה הספרתית (digit-by-digit) לשורש, כמו בעט ונייר"
added: 2026-11-06
---

## השאלה

צריך מודול חומרה שמקבל \( n \) של 16 ביטים ומחזיר את השורש השלם שלו, \( r = \lfloor \sqrt{n} \rfloor \) :
המספר השלם הגדול ביותר שמקיים \( r^2 \le n \). אסור להשתמש במכפל ולא במחלק, כי מכפל של 16
ביטים יקר בשטח ובזמן. מותר רק חיבור, חיסור, השוואה והזזות.

השאלה בארבעה סעיפים : קודם \( n = 1000 \) ביד, אחר כך האלגוריתם בלי כפל עם הוכחה, אחר כך
מודול RTL והאימות שלו, ובסוף אותה שיטה לחילוק ולשורש שלישי.

??? interviewer "מה המראיין בודק"
    - **חיפוש ביט אחרי ביט :** האם המועמד רואה שאפשר לקבוע את השורש מהביט העליון לתחתון,
      כמו חיפוש בינארי, ושלשורש של 16 ביטים יש רק 8 ביטים.
    - **להיפטר מהכפל :** האם הוא מחליף את \( (r + b)^2 \) בשארית \( n - r^2 \) ובהפרש
      \( 2rb + b^2 \), ורואה שכשה-\( b \) הוא חזקה של 2 זה רק הזזות.
    - **הוכחה :** שמורת לולאה מסודרת, ולא "זה עובד בדוגמה".
    - **אימות :** בדיקה של כל 65,536 הקלטים, assertion על התוצאה, ומה עושים כשהקלט רחב מדי
      לבדיקה מלאה.

---

### סעיף א – השורש של 1000 ביד

חשבו את \( \lfloor \sqrt{1000} \rfloor \) ביט אחרי ביט, מהביט העליון של השורש לתחתון. בכל
שלב החליטו אם להדליק את הביט, וכתבו כמה נשאר מ-1000.

??? tip "רמז 1"
    כמה ביטים יש לשורש של מספר בן 16 ביטים? החליטו עליהם מהעליון למטה : ביט עליון שווה יותר
    מכל הביטים שמתחתיו יחד.

??? tip "רמז 2"
    ביט \( b = 2^k \) נשאר דלוק אם \( (r + b)^2 \le 1000 \), כש-\( r \) הוא מה שהוחלט עד עכשיו.
    במקום לחשב את \( (r + b)^2 \) מחדש, שמרו את מה שנשאר, \( n - r^2 \). כשמדליקים ביט
    \( b \), הריבוע גדל ב-\( (r + b)^2 - r^2 = 2rb + b^2 \).

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **‏31, ונשארים 39.** ביטים 7, 6 ו-5 גדולים מדי (\( 128^2 \), \( 64^2 \) ו-\( 32^2 \) כולם
        מעל 1000), וביטים 4 עד 0 כולם נכנסים : ‏\( 16 + 8 + 4 + 2 + 1 = 31 \), ו-\( 1000 - 31^2 = 1000 - 961 = 39 \).
        שמונה שלבים, אחד לכל ביט של השורש.

    <!-- cost: שלבים 8 | השורש 31 | השארית 39 -->

    #### הרעיון { .sol-idea }

    השורש קטן מ-256, אז יש לו 8 ביטים. בונים אותו מלמעלה : בכל שלב שואלים "אם אדליק את הביט
    הזה, האם הריבוע עדיין לא עובר את \( n \)?" אם כן, מדליקים. אם לא, משאירים כבוי. ביט
    עליון שדלוק שווה יותר מכל הביטים שמתחתיו יחד, ולכן ההחלטה עליו לא תלויה בהם. זה חיפוש
    בינארי על השורש, ביט אחד בכל שלב.

    כדי לא לחשב ריבוע בכל שלב, שומרים את **השארית** \( \mathit{rem} = n - r^2 \). להדליק את
    הביט \( b = 2^k \) מגדיל את הריבוע ב-\( (r + b)^2 - r^2 = 2rb + b^2 \), שאנחנו קוראים לו
    **הניסיון**. אם הניסיון לא גדול מהשארית, מדליקים את הביט ומחסירים אותו.

    <!-- gen 0 -->

    | ביט ‏k | הניסיון ‏2rb + b² | השארית לפני | ‏r אחרי, בבינארי |
    |:-:|:-:|:-:|:-:|
    | 7 | 16384 ✗ | 1000 | ‏<span dir="ltr">0 = <code>00000000</code></span> |
    | 6 | 4096 ✗ | 1000 | ‏<span dir="ltr">0 = <code>00000000</code></span> |
    | 5 | 1024 ✗ | 1000 | ‏<span dir="ltr">0 = <code>00000000</code></span> |
    | 4 | **256** ✓ | 1000 | ‏<span dir="ltr">16 = <code>00010000</code></span> |
    | 3 | **320** ✓ | 744 | ‏<span dir="ltr">24 = <code>00011000</code></span> |
    | 2 | **208** ✓ | 424 | ‏<span dir="ltr">28 = <code>00011100</code></span> |
    | 1 | **116** ✓ | 216 | ‏<span dir="ltr">30 = <code>00011110</code></span> |
    | 0 | **61** ✓ | 100 | ‏<span dir="ltr">31 = <code>00011111</code></span> |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **התחלה :** ‏\( r = 0 \), והשארית היא כל ה-1000.
    2. **ביט אחרי ביט, מ-7 עד 0 :** הניסיון הוא \( 2rb + b^2 \), עם \( b = 2^k \) ועם ה-\( r \) של עד עכשיו. כל עוד \( r = 0 \) הוא רק \( b^2 \).
    3. **ההחלטה :** ניסיון שלא גדול מהשארית נכנס : מדליקים את הביט ומחסירים אותו מהשארית. אחרת הביט נשאר כבוי והשארית לא משתנה.
    4. **בדיקה :** ‏\( 31^2 + 39 = 961 + 39 = 1000 \), ו-\( 32^2 = 1024 \) כבר גדול מ-1000.

    </div>

    #### למה זה נכון { .sol-proof }

    **אותה שיטה כמו בבית הספר.** השורש "בעט ונייר" בבסיס 10 מחלק את המספר לזוגות של ספרות,
    `10|00`, ומוצא ספרה אחת של השורש בכל זוג : בזוג `10` הספרה הגדולה שהריבוע שלה נכנס היא 3,
    ונשארת 1. מורידים את הזוג הבא ומקבלים 100. עכשיו מחפשים ספרה \( d \) כך
    ש-\( (2 \cdot 30 + d) \cdot d \le 100 \). הספרה 1 נותנת 61, והספרה 2 כבר נותנת 124. השורש 31, והשארית \( 100 - 61 = 39 \).
    הביטוי \( (2 \cdot 30 + d) \cdot d \) הוא בדיוק \( 2rb + b^2 \). בבסיס 2 יש רק שתי
    ספרות, ולכן במקום לחפש את \( d \) רק שואלים אם \( d = 1 \) נכנס.

    #### סיבוכיות { .sol-cost }

    שלב לכל ביט של השורש : 8 שלבים ל-\( n \) של 16 ביטים. בכל שלב השוואה אחת וחיסור אחד.

---

### סעיף ב – בלי כפל, ולמה זה נכון

1. הראו איך מחשבים את הניסיון \( 2rb + b^2 \) בלי כפל, רק בהזזות.
2. הוכיחו שהאלגוריתם מחזיר תמיד \( \lfloor \sqrt{n} \rfloor \).
3. כמה שלבים צריך לקלט של \( 2m \) ביטים, ולמה?
4. כתבו את האלגוריתם כפונקציה.

??? tip "רמז 1"
    ‏\( b = 2^k \). כמה זה \( 2 \cdot r \cdot 2^k \)? ו-\( (2^k)^2 \)?

??? tip "רמז 2"
    להוכחה : נסמנו ב-\( s \) את השורש האמיתי. איזה אי-שוויון בין \( r \) ל-\( s \) נשמר אחרי
    כל שלב?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        הניסיון הוא \( (r \ll (k + 1)) \mathbin{|} (1 \ll 2k) \) : הזזה של \( r \), ביט
        אחד, ו-OR. אחרי השלב של ביט \( k \) מתקיים \( r \le s < r + 2^k \), ובסוף, עם
        \( 2^0 = 1 \), יוצא \( r = s \). לקלט של \( 2m \) ביטים יש לשורש \( m \) ביטים, ולכן
        \( m \) שלבים.

    <!-- cost: זמן \( O(m) \) שלבים | חומרה מחסר אחד -->

    #### הרעיון { .sol-idea }

    כש-\( b = 2^k \), הכפל נעלם : \( 2rb = r \cdot 2^{k+1} \) הוא \( r \) מוזז שמאלה ב-\( k + 1 \),
    ו-\( b^2 = 2^{2k} \) הוא ביט אחד במקום \( 2k \). גאומטרית, הריבוע \( r^2 \) גדל לריבוע
    \( (r + b)^2 \), ומה שנוסף לו הוא שני מלבנים של \( r \) על \( b \) וריבוע קטן של \( b \) על \( b \) :

    <!-- gen 1 -->

    <div class="isq-figwrap"><svg class="figure isq-fig" viewBox="0 0 300 300" style="max-width:20rem" role="img" aria-label="השלב של ביט 3 בחישוב השורש של 1000, כשטחים : הריבוע r² = 16² = 256 כבר בפנים, ונוספים לו שני מלבנים של 16 על 8 וריבוע קטן של 8 על 8, יחד 320, בתוך הריבוע המקווקו שהצלע שלו √1000"><rect class="isq-sq-old" x="54" y="24" width="112.3" height="112.3"/><rect class="isq-sq-add" x="166.3" y="24" width="56.2" height="112.3"/><rect class="isq-sq-add" x="54" y="136.3" width="112.3" height="56.2"/><rect class="isq-sq-small" x="166.3" y="136.3" width="56.2" height="56.2"/><rect class="isq-sq-bound" x="54" y="24" width="222" height="222"/><text class="isq-lab" x="110.2" y="86.2" text-anchor="middle">r² = 256</text><text class="isq-lab" x="194.4" y="86.2" text-anchor="middle">128</text><text class="isq-lab" x="110.2" y="170.4" text-anchor="middle">128</text><text class="isq-lab" x="194.4" y="170.4" text-anchor="middle">64</text><text class="tick" x="110.2" y="210.5" text-anchor="middle">r = 16</text><text class="tick" x="194.4" y="210.5" text-anchor="middle">b = 8</text><text class="tick" x="46" y="85.2" text-anchor="end">16</text><text class="tick" x="46" y="169.4" text-anchor="end">8</text></svg></div>

    <span class="viz-legend"><span><i class="isq-key-old"></i><span>‏r² = 256, מה שכבר בפנים</span></span><span><i class="isq-key-add"></i><span>שני מלבנים ‏rb, יחד ‏2rb = 256</span></span><span><i class="isq-key-small"></i><span>‏b² = 64</span></span><span><i class="isq-key-bound"></i><span>הריבוע שהצלע שלו ‏√1000, השטח 1000</span></span></span>

    <!-- /gen -->

    ובחומרה מספיק OR במקום חיבור : הביטים הדלוקים של \( r \) כולם מעל ביט \( k \), כי עד
    עכשיו הוחלט רק על הביטים העליונים. אחרי ההזזה ב-\( k + 1 \) הם מעל ביט \( 2k + 1 \), והביט
    של \( b^2 \) נמצא ב-\( 2k \). אין להם ביט משותף, ולכן OR שווה לסכום. כך זה נראה בביט 3
    של 1000, כש-\( r = 16 \) :

    <!-- gen 2 -->

    <div class="gs-scroll" tabindex="0" role="region" aria-label="הניסיון בביט 3 כשהשורש עד עכשיו 16 : ‏r מוזז ב-4 הוא 256, ‏1 מוזז ב-6 הוא 64, ואין להם ביט משותף, ולכן OR נותן את הסכום 320"><table class="gs-bits isq-bits" dir="ltr" aria-label="הניסיון בביט 3 כשהשורש עד עכשיו 16 : ‏r מוזז ב-4 הוא 256, ‏1 מוזז ב-6 הוא 64, ואין להם ביט משותף, ולכן OR נותן את הסכום 320"><tbody><tr><th></th><td class="isq-ix">15</td><td class="isq-ix">14</td><td class="isq-ix">13</td><td class="isq-ix">12</td><td class="isq-ix">11</td><td class="isq-ix">10</td><td class="isq-ix">9</td><td class="isq-ix">8</td><td class="isq-ix">7</td><td class="isq-ix">6</td><td class="isq-ix">5</td><td class="isq-ix">4</td><td class="isq-ix">3</td><td class="isq-ix">2</td><td class="isq-ix">1</td><td class="isq-ix">0</td><td></td></tr><tr><th>r &lt;&lt; 4</th><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-one isq-r">1</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="isq-val">256</td></tr><tr><th>1 &lt;&lt; 6</th><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-one isq-b">1</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="isq-val">64</td></tr><tr><th>OR</th><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-one isq-t">1</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-one isq-t">1</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="gs-b isq-zero">0</td><td class="isq-val">320</td></tr></tbody></table></div>

    <span class="viz-legend"><span><i class="isq-key-r"></i><span>הביטים של ‏r = 16, מוזזים ב-4 (‏2rb)</span></span><span><i class="isq-key-b"></i><span>הביט 6 (‏b²)</span></span><span><i class="isq-key-t"></i><span>הניסיון 320</span></span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **התחלה :** ‏\( r = 0 \), ‏\( \mathit{rem} = n \). השמורה \( \mathit{rem} = n - r^2 \) נכונה.
    2. **לכל ביט \( k \), מלמעלה :** הניסיון \( t = (r \ll (k+1)) \mathbin{|} (1 \ll 2k) \).
    3. **ההחלטה :** אם \( t \le \mathit{rem} \), מחסירים \( \mathit{rem} \mathrel{-}= t \) ומדליקים את ביט \( k \) של \( r \). אחרת לא נוגעים בכלום.
    4. **סוף :** אחרי ביט 0, ‏\( r = \lfloor \sqrt{n} \rfloor \) ו-\( \mathit{rem} = n - r^2 \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="isqrt_bits" linenums="1" hl_lines="6 7"
        def isqrt_bits(n: int, width: int = 16) -> tuple[int, int]:
            """floor(sqrt(n)) of a width-bit n (width even), one result bit per step and no
            multiplication. Returns (r, n - r*r)."""
            r, rem = 0, n                                  # rem = n - r² all along
            for k in range(width // 2 - 1, -1, -1):       # (1)!
                trial = (r << (k + 1)) | (1 << (2 * k))    # (2)!
                if trial <= rem:                           # (r + b)² <= n
                    rem -= trial
                    r |= 1 << k
            return r, rem
        ```

        1. לשורש של מספר בן `width` ביטים יש `width // 2` ביטים, מהעליון לתחתון.
        2. ‏\( 2rb + b^2 \) עם \( b = 2^k \). ב-Python, כמו ב-SV, ההזזה חלשה מהחיבור : בלי
           הסוגריים `r << k + 1` הוא `r << (k + 1)`, אבל `a << 1 + b` הוא `a << (1 + b)`.

    === "SystemVerilog"
        ```systemverilog title="function automatic logic [7:0] isqrt16" linenums="1" hl_lines="8 9"
        // floor(sqrt(n)) of a 16-bit n: one result bit per loop step, no multiplier.
        function automatic logic [7:0] isqrt16(input logic [15:0] n);
          logic [15:0] rem, trial;
          logic [7:0]  r;
          rem = n;                                        // rem = n - r² all along
          r = '0;
          for (int k = 7; k >= 0; k--) begin
            trial = (16'(r) << (k + 1)) | (16'(1) << (2 * k));   // (1)!
            if (trial <= rem) begin
              rem -= trial;
              r[k] = 1'b1;
            end
          end
          return r;
        endfunction
        ```

        1. הניסיון תמיד נכנס ב-16 ביטים : הוא \( (r + b)^2 - r^2 \) עם \( r + b \le 255 \),
           ולכן קטן מ-\( 255^2 = 65025 \).

    #### למה זה נכון { .sol-proof }

    נסמן ב-\( s = \lfloor \sqrt{n} \rfloor \) את השורש האמיתי. **השמורה :** אחרי השלב של ביט
    \( k \) מתקיים

    \[ r \le s < r + 2^k, \qquad \mathit{rem} = n - r^2, \]

    וכל הביטים של \( r \) מתחת ל-\( k \) כבויים.

    - **לפני השלב הראשון,** עם \( r = 0 \) : ‏\( n < 2^{16} \), ולכן \( s < 2^8 = r + 2^8 \).
    - **צעד :** לפני ביט \( k \), עם \( b = 2^k \), ידוע ש-\( r \le s < r + 2b \). אם
      \( (r + b)^2 \le n \), כלומר הניסיון נכנס, אז \( s \ge r + b \), ולכן
      \( r + b \le s < (r + b) + b \) : מדליקים את הביט. אחרת \( (r + b)^2 > n \), ולכן
      \( s < r + b \), ו-\( r \le s < r + b \) : משאירים. בשני המקרים הטווח של \( s \)
      התקצר לחצי, והשארית עדיין \( n - r^2 \), כי מחסירים בדיוק את
      \( (r + b)^2 - r^2 \).
    - **סוף :** אחרי ביט 0, ‏\( r \le s < r + 1 \), ולכן \( r = s \).

    **כמה שלבים.** קלט של \( 2m \) ביטים קטן מ-\( 2^{2m} \), ולכן השורש קטן מ-\( 2^m \) : יש
    לו \( m \) ביטים, וכל שלב קובע אחד. לקלט באורך אי-זוגי מוסיפים ביט 0 מלמעלה.

    **נסו בעצמכם.** הקלידו 4095, לחצו "עד הסוף", ואחר כך הקלידו 4096. הפרש של 1 ב-\( n \) הופך
    את כל שמונת הביטים של השורש, מ-00111111 ל-01000000. ב-4096 התקדמו ביט אחרי ביט : בביט 6
    הניסיון ממלא בדיוק את הריבוע המקווקו של \( \sqrt{n} \), וכל ניסיון אחריו יוצא ממנו :

    <div class="explorer" data-kind="isqrt" data-n="1000"></div>

    #### סיבוכיות { .sol-cost }

    ‏\( m \) שלבים לקלט של \( 2m \) ביטים. בכל שלב הזזות (חיווט בלבד בחומרה), OR, השוואה
    וחיסור של \( 2m \) ביטים. במודול סדרתי זה מחסר אחד, השוואה ורגיסטרים, ובלי מכפל בכלל.

---

### סעיף ג – מודול RTL ואימות

1. כתבו מודול סדרתי `isqrt_seq` : ‏`start` טוען את \( n \), וביט אחד של השורש נקבע בכל שעון.
   כש-`busy` יורד, `done` עולה למחזור אחד, ו-`root` ו-`rem` מוכנים.
2. כתבו מודל ייחוס ב-Python שנותן את הרגיסטרים אחרי כל שעון.
3. איך מאמתים את המודול? מה בודקים כשהקלט הוא 16 ביטים, ומה כשהוא 32 ביטים?

??? tip "רמז 1"
    שלושה רגיסטרים מספיקים לחישוב : השורש, השארית ומונה הביט \( k \). הניסיון הוא צירופי,
    מחושב מהם.

??? tip "רמז 2"
    באימות לא צריך את האלגוריתם עצמו : התשובה נכונה אם ורק אם \( r^2 \le n < (r + 1)^2 \).
    בבודק מותר להשתמש בכפל.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏8 מחזורים אחרי `start` : ‏`root` ו-`rem` הם רגיסטרים, ובכל שעון נקבע ביט אחד. את
        16 הביטים בודקים במלואם, כל 65,536 הקלטים, מול מודל הייחוס, ו-assertion בודק
        \( r^2 \le n < (r + 1)^2 \) בכל `done`. ב-32 ביטים בודקים את שני הצדדים של כל
        "מדרגה", \( s^2 - 1 \) ו-\( s^2 \) לכל \( s \), את הערך המקסימלי, חזקות של 2 וקלטים
        אקראיים.

    <!-- cost: מחזורים 8 | קלטים בבדיקה המלאה 65,536 -->

    #### הרעיון { .sol-idea }

    המודול הוא הלולאה של סעיף ב, פרוסה על פני שעונים : כל איטרציה היא מחזור. מונה \( k \)
    יורד מ-7 ל-0, והניסיון מחושב בצירופי מ-`root` ומ-\( k \). כך זה נראה בחומרה :

    <!-- gen 3 -->

    <svg class="figure isq-fig isq-dp" viewBox="0 0 410 346" direction="ltr" style="max-width:25.625rem" role="img" aria-label="תרשים המלבנים של isqrt_seq : שלושה רגיסטרים, k של 3 ביטים, root של 8 ו-rem של 16. המזיז בוחר לפי k את הניסיון מתוך root. מחסר אחד מחשב rem פחות trial, וה-borrow שלו הוא ההשוואה : fits הוא ההפך של borrow. המפענח מדליק את root[k] כש-fits, והמרבב כותב ל-rem את n ב-load, את diff כש-fits, ואחרת את rem עצמו. הבקרה מחשבת load מ-start, מורידה את k ב-1 בכל מחזור של busy, ומעלה את done כש-k הוא 0"><defs><marker id="isq-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="isq-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs><g class="isq-blk isq-reg"><rect x="10" y="14" width="70" height="44" rx="5"/><text x="45" y="33" text-anchor="middle">k</text><text class="isq-sub" x="45" y="49" text-anchor="middle">3 bits</text></g><g class="isq-blk isq-reg"><rect x="118" y="14" width="130" height="44" rx="5"/><text x="183" y="33" text-anchor="middle">root</text><text class="isq-sub" x="183" y="49" text-anchor="middle">8 bits</text></g><g class="isq-blk isq-reg"><rect x="284" y="14" width="108" height="44" rx="5"/><text x="338" y="33" text-anchor="middle">rem</text><text class="isq-sub" x="338" y="49" text-anchor="middle">16 bits</text></g><g class="isq-blk isq-mux"><rect x="118" y="92" width="126" height="44" rx="5"/><text x="181" y="111" text-anchor="middle">trial</text><text class="isq-sub" x="181" y="127" text-anchor="middle">a mux on k</text></g><g class="isq-blk isq-stage"><rect x="284" y="92" width="108" height="44" rx="5"/><text x="338" y="111" text-anchor="middle">rem − trial</text><text class="isq-sub" x="338" y="127" text-anchor="middle">diff and borrow</text></g><g class="isq-blk isq-mux"><rect x="118" y="166" width="124" height="44" rx="5"/><text x="180" y="185" text-anchor="middle">decoder</text><text class="isq-sub" x="180" y="201" text-anchor="middle">root[k] ← 1</text></g><g class="isq-blk isq-ctl"><rect x="278" y="166" width="92" height="40" rx="5"/><text x="324" y="183" text-anchor="middle">fits</text><text class="isq-sub" x="324" y="199" text-anchor="middle">= !borrow</text></g><g class="isq-blk isq-ctl"><rect x="10" y="246" width="238" height="44" rx="5"/><text x="129" y="265" text-anchor="middle">control</text><text class="isq-sub" x="129" y="281" text-anchor="middle">load, busy, done, k ← k − 1</text></g><g class="isq-blk isq-mux"><rect x="284" y="246" width="108" height="44" rx="5"/><text x="338" y="265" text-anchor="middle">rem mux</text><text class="isq-sub" x="338" y="281" text-anchor="middle">n, diff or rem</text></g><path class="isq-wire" d="M28,58 L28,246" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="32" y="232" text-anchor="start">k</text><path class="isq-wire" d="M62,246 L62,58" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="66" y="232" text-anchor="start">k − 1</text><path class="isq-wire" d="M80,36 L92,36 L92,180 L118,180" marker-end="url(#isq-hb)"/><path class="isq-wire" d="M146,74 L146,92" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="152" y="84" text-anchor="start">k</text><path class="isq-wire" d="M183,58 L183,92" marker-end="url(#isq-hb)"/><path class="isq-wire" d="M244,114 L284,114" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="264" y="105" text-anchor="middle">trial</text><path class="isq-wire" d="M338,58 L338,92" marker-end="url(#isq-hb)"/><path class="isq-wire" d="M304,136 L304,166" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="299" y="155" text-anchor="end">borrow</text><path class="isq-wire" d="M278,194 L242,194" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="260" y="188" text-anchor="middle">fits</text><path class="isq-wire" d="M316,206 L316,246" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="312" y="232" text-anchor="end">fits</text><path class="isq-wire" d="M382,136 L382,246" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="378" y="232" text-anchor="end">diff</text><path class="isq-wire" d="M392,268 L401,268 L401,36 L392,36" marker-end="url(#isq-hb)"/><path class="isq-wire" d="M146,166 L146,150 L104,150 L104,66 L128,66 L128,58" marker-end="url(#isq-hb)"/><path class="isq-wire" d="M183,246 L183,210" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="187" y="232" text-anchor="start">load, busy</text><path class="isq-wire" d="M248,268 L284,268" marker-end="url(#isq-hb)"/><path class="isq-wire" d="M56,318 L56,290" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="56" y="332" text-anchor="middle">start</text><path class="isq-wire" d="M170,290 L170,318" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="170" y="332" text-anchor="middle">busy, done</text><path class="isq-wire" d="M338,318 L338,290" marker-end="url(#isq-hb)"/><text class="isq-wlab" x="338" y="332" text-anchor="middle">n</text></svg>

    <!-- /gen -->

    - **הרגיסטרים :** \( k \) של 3 ביטים, הביט שמחליטים עליו במחזור הזה. ‏`root` של 8 ביטים,
      השורש עד עכשיו. ‏`rem` של 16 ביטים, השארית \( n - \mathit{root}^2 \), שבהתחלה היא כל
      \( n \).
    - **המזיז :** מחשב את הניסיון \( (\mathit{root} \ll (k + 1)) \mathbin{|} (1 \ll 2k) \). אין
      בו חשבון : לכל ערך של \( k \) הניסיון הוא אותם ביטים של `root` במקום אחר, ועוד ביט אחד.
      לכן זה מרבב של 8 כניסות, שכל אחת מהן היא חיווט, והבורר שלו הוא \( k \).
    - **המחסר :** מחשב \( \mathit{diff} = \mathit{rem} - \mathit{trial} \) ב-17 ביטים. הביט
      העליון הוא ה-`borrow` : הוא 1 בדיוק כשהניסיון גדול מהשארית, והחיסור "לווה".
    - **המשווה הוא ה-borrow :** אין משווה נפרד. ‏\( \mathit{trial} \le \mathit{rem} \) אם ורק
      אם החיסור לא לווה, ולכן `fits = !borrow`. מחסר אחד נותן גם את ההחלטה וגם את השארית
      החדשה. בקוד כתובים `trial <= rem` ו-`rem - trial` בנפרד, וכדי לא לסמוך על הסינתזה שתאחד
      אותם אפשר לכתוב את המחסר במפורש, `{borrow, diff} = {1'b0, rem} - {1'b0, trial}`.
    - **המפענח :** הופך את \( k \) לאחד משמונה קווים, ובמחזור שבו `fits` דולק הוא מדליק את
      `root[k]`. ביט של `root` שנדלק לא נכבה עד החישוב הבא, ולכן לכל פליפ-פלופ של `root` יש
      אפשור משלו, ואין צורך בחיבור. ב-`load` הוא מאפס את כל `root`.
    - **המרבב של rem :** בוחר מה ייכתב ל-`rem` בסוף המחזור : \( n \) ב-`load`, ‏`diff`
      כש-`fits` דולק, ואחרת את `rem` עצמו.
    - **הבקרה :** ‏`load = start && !busy` טוען את \( n \), מאפס את `root`, כותב \( k = 7 \)
      ומדליק את `busy`. בכל מחזור של `busy` ‏\( k \) יורד ב-1, וב-\( k = 0 \) ‏`busy` יורד ו-`done`
      עולה למחזור אחד. ‏`busy` גם מאפשר את הכתיבה ל-`rem` ול-`root`, כך שהם לא זזים בין
      חישובים.

    כך עובר דרכו \( n = 1000 \). שורה בטבלה היא מחזור אחד בגל שמתחתיה, מעליית שעון אחת עד
    הבאה, והמספור שלהן אחד : במחזור 0 ‏`start` דולק, ו-`done` עולה במחזור 9. ‏`trial` ו-`fits`
    מחושבים בתוך המחזור, והעלייה שבסופו כותבת אותם, ולכן `root` ו-`rem` החדשים מופיעים רק בשורה
    הבאה :

    <!-- gen 4 -->

    | מחזור | ‏k | הניסיון ‏trial | נכנס? ‏fits | ‏root | ‏rem | ‏busy | ‏done |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | 0 | – | – | – | – | – | 0 | 0 |
    | 1 | 7 | 16384 | ✗ | 0 | 1000 | 1 | 0 |
    | 2 | 6 | 4096 | ✗ | 0 | 1000 | 1 | 0 |
    | 3 | 5 | 1024 | ✗ | 0 | 1000 | 1 | 0 |
    | 4 | 4 | **256** | ✓ | 0 | 1000 | 1 | 0 |
    | 5 | 3 | **320** | ✓ | 16 | 744 | 1 | 0 |
    | 6 | 2 | **208** | ✓ | 24 | 424 | 1 | 0 |
    | 7 | 1 | **116** | ✓ | 28 | 216 | 1 | 0 |
    | 8 | 0 | **61** | ✓ | 30 | 100 | 1 | 0 |
    | **9** | 0 | – | – | **31** | **39** | 0 | **1** |
    | 10 | 0 | – | – | 31 | 39 | 0 | 0 |

    <!-- /gen -->

    <!-- gen 5 -->

    ```wavedrom
    { signal: [
      { name: "clk",   wave: "p.........." },
      { name: "cycle", wave: "===========", data: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] },
      { name: "start", wave: "10........." },
      { name: "busy",  wave: "01.......0." },
      { name: "k",     wave: "x========..", data: ["7", "6", "5", "4", "3", "2", "1", "0"] },
      { name: "trial", wave: "x========x.", data: ["16384", "4096", "1024", "256", "320", "208", "116", "61"] },
      { name: "fits",  wave: "x0..1....x." },
      { name: "root",  wave: "x=...=====.", data: ["0", "16", "24", "28", "30", "31"] },
      { name: "rem",   wave: "x=...=====.", data: ["1000", "744", "424", "216", "100", "39"] },
      { name: "done",  wave: "0........10" }
    ]}
    ```

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מחזור 0, ‏`start` :** ‏`load` טוען `rem = n`, ‏`root = 0` ו-`k = 7`, ומדליק את `busy`.
    2. **מחזורים 1 עד 8, ‏`busy` :** אם הניסיון נכנס, מחסירים אותו ומדליקים את `root[k]`. בכל מקרה \( k \) יורד ב-1.
    3. **מחזור 9 :** אחרי ביט 0 ‏`busy` יורד, ו-`done` עולה למחזור אחד.
    4. **האימות :** כל הקלטים מול המודל, ו-assertion על התוצאה בכל `done`.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="isqrt_seq_model" linenums="1" hl_lines="7 8"
        import random


        def isqrt_seq_model(n: int) -> list[tuple[int, int, int, int, int]]:
            """The registers of isqrt_seq after the start clock and after every clock that
            follows, until done: (k, root, rem, busy, done)."""
            k, root, rem, busy, done = 7, 0, n, 1, 0
            trace = [(k, root, rem, busy, done)]
            while busy:
                trial = (root << (k + 1)) | (1 << (2 * k))
                if trial <= rem:
                    rem -= trial
                    root |= 1 << k
                if k == 0:
                    busy, done = 0, 1
                else:
                    k -= 1
                trace.append((k, root, rem, busy, done))
            return trace


        def corner_inputs(width: int = 32, randoms: int = 1000, seed: int = 1) -> list[int]:
            """Inputs for a width-bit isqrt when trying them all is too much."""
            top = (1 << width) - 1
            cases = {0, 1, top}                            # (1)!
            for s in range(1, 1 << (width // 2)):          # (2)!
                cases.update((s * s - 1, s * s))
            for i in range(width):                         # the powers of 2 and 2^i - 1
                cases.update((1 << i, (1 << i) - 1))
            rng = random.Random(seed)
            cases.update(rng.randrange(top + 1) for _ in range(randoms))
            return sorted(cases)
        ```

        1. ‏`top` הוא הקלט הגדול ביותר, והשורש שלו הוא הגדול ביותר : ב-32 ביטים
           \( 2^{16} - 1 = 65535 \), ונשארים \( 2^{17} - 2 \), השארית הגדולה האפשרית.
        2. השורש הוא פונקציית מדרגות : הוא קבוע בין \( s^2 \) ל-\( (s + 1)^2 - 1 \) ועולה
           ב-1 בדיוק ב-\( s^2 \). שני הצדדים של כל מדרגה, 131,070 קלטים, בודקים כל מקום
           שבו התשובה משתנה.

    === "SystemVerilog"
        ```systemverilog title="module isqrt_seq" linenums="1" hl_lines="13 22 23"
        // floor(sqrt(n)) of a 16-bit n, one result bit per clock: busy for 8 clocks after
        // start, then done for one clock with root and rem = n - root*root.
        module isqrt_seq (
          input  logic        clk, rst_n,
          input  logic        start,
          input  logic [15:0] n,
          output logic        busy, done,
          output logic [7:0]  root,
          output logic [15:0] rem
        );
          logic [2:0]  k;
          logic [15:0] trial;
          assign trial = (16'(root) << (k + 1)) | (16'(1) << (2 * k));   // (1)!

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin
              busy <= 1'b0; done <= 1'b0; root <= '0; rem <= '0; k <= '0;
            end else begin
              done <= 1'b0;
              if (start && !busy) begin
                rem <= n; root <= '0; k <= 3'd7; busy <= 1'b1;
              end else if (busy) begin
                if (trial <= rem) begin
                  rem <= rem - trial;
                  root[k] <= 1'b1;
                end
                if (k == 0) begin busy <= 1'b0; done <= 1'b1; end   // (2)!
                else k <= k - 1;
              end
            end
        endmodule

        // The checker: every finished root, whatever the algorithm inside.
        module isqrt_check (input logic clk, done, input logic [15:0] n,
                            input logic [7:0] root);
          logic [16:0] lo, hi;
          assign lo = root * root;                        // (3)!
          assign hi = (root + 1) * (root + 1);
          always @(posedge clk)
            if (done) assert (lo <= n && n < hi)
              else $error("isqrt(%0d) = %0d", n, root);
        endmodule
        ```

        1. ההזזות הן חיווט : בכל ערך של \( k \) הניסיון הוא אותם ביטים של `root` במקום
           אחר. בחומרה זה בורר לפי \( k \), ולא מכפל.
        2. ‏`start` בזמן `busy` לא מתחיל חישוב חדש : המודול מסיים את הנוכחי קודם. את \( n \)
           צריך להחזיק רק במחזור של `start`, כי הוא נטען ל-`rem`.
        3. בבודק מותר לכפול : הוא לא סינתזה, והוא לא יודע איך התשובה חושבה, רק מה היא חייבת
           לקיים. ‏`hi` צריך 17 ביטים, כי \( 256^2 = 65536 \).

    #### למה זה נכון { .sol-proof }

    **המודול הוא הפונקציה.** בכל מחזור של `busy` המודול עושה בדיוק איטרציה אחת של הלולאה
    של סעיף ב, עם אותו \( k \), ולכן אחרי 8 מחזורים \( \mathit{root} = \lfloor \sqrt{n} \rfloor \).
    הבדיקה המלאה משווה את `root` ואת `rem` למודל על כל 65,536 הקלטים, וה-assertion בודק את
    התכונה עצמה, בלי להסתמך על המודל.

    **למה 16 ביטים בודקים במלואם.** ‏65,536 קלטים כפול 9 מחזורים הם כחצי מיליון מחזורים,
    שניות בסימולציה. אין סיבה לדגום כשאפשר לבדוק הכול.

    **ב-32 ביטים** יש \( 2^{32} \) קלטים, יותר מדי. בודקים :

    - **את כל קצוות המדרגות :** \( s^2 - 1 \) ו-\( s^2 \) לכל \( s \) מ-1 עד 65535. שם
      התשובה משתנה, ושם טעות ב-off-by-one מתגלה.
    - **את הקצוות של הטווח :** 0, 1, והמקסימום \( 2^{32} - 1 \), שהשורש שלו 65535
      והשארית שלו הגדולה ביותר.
    - **חזקות של 2 ו-\( 2^i - 1 \) :** ביט אחד דלוק, וכל הביטים דלוקים, לבדיקת הנשאים במחסר.
    - **קלטים אקראיים :** לבאגים שתלויים בביטים באמצע, כמו רוחב שגוי של `rem`.

    **נסו בעצמכם.** התקדמו מחזור אחרי מחזור ועקבו אחרי `borrow` בטבלת האותות : כשהוא 1,
    ‏`fits` כבוי, ו-`root` ו-`rem` לא זזים. אחר כך לחצו על מקרה המלכודת 4096 : במחזור 2 הניסיון
    שווה בדיוק לשארית, והמחסר לא לווה, כי \( 4096 - 4096 = 0 \). משווה שבודק "קטן מ-" במקום
    "קטן או שווה" היה מחזיר 63 :

    <div class="explorer" data-kind="isqrthw" data-n="1000"></div>

    #### סיבוכיות { .sol-cost }

    ‏8 מחזורים לתוצאה, ואי אפשר להתחיל חדשה לפני שהקודמת נגמרה. בחומרה : שלושה רגיסטרים
    (3, 8 ו-16 ביטים), מחסר אחד של 17 ביטים שה-borrow שלו הוא גם ההשוואה, מרבב שמזיז את
    `root` לפי \( k \), מפענח של 3 ל-8 ומרבב לפני `rem`.

---

### סעיף ד – אותה שיטה לחילוק ולשורש שלישי

1. חלקו 1000 ב-7 באותה שיטה : ביט אחד של המנה בכל שלב, "האם זה נכנס, אז מחסירים".
2. חשבו את השורש השלישי של 1000 ביט אחרי ביט. מה הניסיון עכשיו, ואיך מחשבים אותו בלי כפל?
3. כתבו את שתי הפונקציות.

??? tip "רמז 1"
    בחילוק, להדליק את ביט \( k \) של המנה מוסיף \( d \cdot 2^k \) למכפלה \( q \cdot d \). כמה
    זה בהזזות?

??? tip "רמז 2"
    בשורש שלישי, \( (r + b)^3 - r^3 = 3r^2 b + 3r b^2 + b^3 \). כדי לא לכפול, שמרו גם את \( r^2 \)
    ברגיסטר, ועדכנו אותו כמו בסעיף ב. ו-\( 3x = (x \ll 1) + x \).

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        **‏\( 1000 = 142 \cdot 7 + 6 \)**, ו-**\( \sqrt[3]{1000} = 10 \)** בדיוק. בחילוק
        הניסיון הוא \( d \ll k \). בשורש השלישי הניסיון הוא
        \( ((3r^2) \ll k) + ((3r) \ll 2k) + (1 \ll 3k) \), עם \( r^2 \) שנשמר ברגיסטר ומתעדכן
        ב-\( 2rb + b^2 \), כמו השארית של סעיף ב. בשני המקרים אין מכפל.

    <!-- cost: חילוק 16 שלבים | שורש שלישי 8 שלבים ל-24 ביטים -->

    #### הרעיון { .sol-idea }

    בשלוש הבעיות מחפשים את המספר הגדול ביותר \( x \) כך ש-\( f(x) \le n \) :
    \( x^2 \le n \), ‏\( x \cdot d \le a \) ו-\( x^3 \le n \). בכל שלב שואלים אם להדליק את
    ביט \( k \), ושומרים את מה שנשאר, \( n - f(x) \). מה שמשתנה הוא רק **הניסיון**,
    \( f(x + b) - f(x) \) :

    | הבעיה | ‏\( f(x) \) | הניסיון \( f(x + b) - f(x) \) | בהזזות |
    |:-:|:-:|:-:|:-:|
    | שורש ריבועי | ‏\( x^2 \) | ‏\( 2xb + b^2 \) | ‏\( (x \ll (k+1)) \mathbin{|} (1 \ll 2k) \) |
    | חילוק ב-\( d \) | ‏\( x \cdot d \) | ‏\( d \cdot b \) | ‏\( d \ll k \) |
    | שורש שלישי | ‏\( x^3 \) | ‏\( 3x^2 b + 3x b^2 + b^3 \) | ‏\( (3x^2 \ll k) + (3x \ll 2k) + (1 \ll 3k) \) |

    **החילוק של 1000 ב-7.** המנה של 16 ביטים, מביט 15 למטה. ביטים 15 עד 8 גדולים מדי :
    ‏\( 7 \cdot 256 = 1792 > 1000 \).

    <!-- gen 6 -->

    | ביט ‏k | הניסיון ‏d · 2ᵏ | השארית לפני | ‏q אחרי |
    |:-:|:-:|:-:|:-:|
    | 15 עד 8 | 1792 ומעלה ✗ | 1000 | 0 |
    | 7 | **896** ✓ | 1000 | **128** |
    | 6 | 448 ✗ | 104 | 128 |
    | 5 | 224 ✗ | 104 | 128 |
    | 4 | 112 ✗ | 104 | 128 |
    | 3 | **56** ✓ | 104 | **136** |
    | 2 | **28** ✓ | 48 | **140** |
    | 1 | **14** ✓ | 20 | **142** |
    | 0 | 7 ✗ | 6 | 142 |

    <!-- /gen -->

    **השורש השלישי של 1000.** ‏\( 1000 < 2^{12} \), ולשורש השלישי של מספר בן 12 ביטים יש
    4 ביטים, 3 עד 0. ‏\( r^2 \) נשמר ברגיסטר ומתעדכן רק כשביט נדלק :

    <!-- gen 7 -->

    | ביט ‏k | הניסיון ‏3r²b + 3rb² + b³ | השארית לפני | ‏r, r² אחרי |
    |:-:|:-:|:-:|:-:|
    | 3 | **512** ✓ | 1000 | ‏<span dir="ltr">8, 64</span> |
    | 2 | 1216 ✗ | 488 | ‏<span dir="ltr">8, 64</span> |
    | 1 | **488** ✓ | 488 | ‏<span dir="ltr">10, 100</span> |
    | 0 | 331 ✗ | 0 | ‏<span dir="ltr">10, 100</span> |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **חילוק :** לכל \( k \) מ-15 למטה, אם \( d \ll k \le \mathit{rem} \), מחסירים ומדליקים את ביט \( k \) של \( q \).
    2. **שורש שלישי, הניסיון :** ‏\( 3r^2 = (r^2 \ll 1) + r^2 \) ו-\( 3r = (r \ll 1) + r \), ומזיזים כל אחד למקום שלו.
    3. **שורש שלישי, העדכון :** אם הניסיון נכנס, מחסירים אותו, מעדכנים \( r^2 \mathrel{+}= (r \ll (k+1)) + (1 \ll 2k) \) עם \( r \) הישן, ורק אז מדליקים את ביט \( k \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="divide_bits, icbrt_bits" linenums="1" hl_lines="5 18 19 20"
        def divide_bits(a: int, d: int, width: int = 16) -> tuple[int, int]:
            """a // d and a % d, one quotient bit per step: bit k is 1 when d·2^k still fits."""
            q, rem = 0, a
            for k in range(width - 1, -1, -1):
                trial = d << k                                 # (1)!
                if trial <= rem:
                    rem -= trial
                    q |= 1 << k
            return q, rem


        def icbrt_bits(n: int, width: int = 24) -> tuple[int, int]:
            """floor(cbrt(n)) of a width-bit n, one result bit per step and no multiplication.
            Returns (r, n - r**3)."""
            r, r2, rem = 0, 0, n                               # r2 = r² is kept in a register
            for k in range((width + 2) // 3 - 1, -1, -1):
                trial = ((((r2 << 1) + r2) << k)               # 3r²b
                         + (((r << 1) + r) << (2 * k))          # 3rb²
                         + (1 << (3 * k)))                      # b³
                if trial <= rem:
                    rem -= trial
                    r2 += (r << (k + 1)) + (1 << (2 * k))      # (2)!
                    r |= 1 << k
            return r, rem
        ```

        1. ‏\( d = 0 \) : הניסיון תמיד 0 ותמיד נכנס, ויוצא \( q = 2^{16} - 1 \) ו-\( \mathit{rem} = a \).
           זה גם מה ש-RISC-V מגדיר לחילוק באפס, אבל את המקרה צריך להגדיר במפרט.
        2. ‏\( (r + b)^2 = r^2 + 2rb + b^2 \), אותו ניסיון של סעיף ב, עם \( r \) **לפני**
           שהביט נדלק.

    === "SystemVerilog"
        ```systemverilog title="function automatic void divide16" linenums="1" hl_lines="7 23 24 25"
        // a / d and a % d of 16-bit numbers, one quotient bit per loop step, no divider.
        function automatic void divide16(input logic [15:0] a, d,
                                         output logic [15:0] q, rem);
          logic [31:0] left, trial;
          left = {16'd0, a};
          q = '0;
          for (int k = 15; k >= 0; k--) begin
            trial = {16'd0, d} << k;                      // d · 2^k
            if (trial <= left) begin
              left -= trial;
              q[k] = 1'b1;
            end
          end
          rem = left[15:0];
        endfunction

        // floor(cbrt(n)) of a 24-bit n: one result bit per loop step, r² kept, no multiplier.
        function automatic logic [7:0] icbrt24(input logic [23:0] n);
          logic [25:0] rem, trial, t1, t2, t3;
          logic [15:0] r2;
          logic [7:0]  r;
          rem = {2'b0, n}; r2 = '0; r = '0;
          for (int k = 7; k >= 0; k--) begin
            t1 = ((26'(r2) << 1) + 26'(r2)) << k;         // (1)!
            t2 = ((26'(r) << 1) + 26'(r)) << (2 * k);
            t3 = 26'(1) << (3 * k);
            trial = t1 + t2 + t3;
            if (trial <= rem) begin
              rem -= trial;
              r2 = r2 + (16'(r) << (k + 1)) + (16'(1) << (2 * k));
              r[k] = 1'b1;
            end
          end
          return r;
        endfunction
        ```

        1. כל איבר בשורה משלו, כי ב-SV ההזזה חלשה מהחיבור : `x << k + y` הוא
           `x << (k + y)`. כך שלושת האיברים \( 3r^2 b \), ‏\( 3r b^2 \) ו-\( b^3 \) נכתבים בלי
           טעות קדימות.

    #### למה זה נכון { .sol-proof }

    ההוכחה של סעיף ב עוברת כמעט מילה במילה, כי השתמשנו רק בשתי עובדות : \( f \) עולה, וכל
    השלבים שומרים \( \mathit{rem} = n - f(x) \). השמורה היא \( x \le s < x + 2^k \), כש-\( s \) הוא
    ה-\( x \) הגדול ביותר עם \( f(x) \le n \). אם \( f(x + b) \le n \), אז \( s \ge x + b \),
    ואחרת \( s < x + b \). בחילוק \( s = \lfloor a / d \rfloor \), ובשורש השלישי
    \( s = \lfloor \sqrt[3]{n} \rfloor \).

    **רוחב השורש השלישי.** לקלט של \( 3m \) ביטים יש לשורש השלישי \( m \) ביטים : 24 ביטים
    נותנים 8, ו-1000, שקטן מ-\( 2^{12} \), נותן 4. הניסיון \( (r + b)^3 - r^3 \) קטן מ-\( 255^3 < 2^{24} \).

    #### סיבוכיות { .sol-cost }

    חילוק של 16 ביטים : 16 שלבים, ביט מנה לכל שלב. שורש שלישי של 24 ביטים : 8 שלבים, עם
    שלוש הזזות, שלושה חיבורים, השוואה וחיסור בכל שלב, ורגיסטר נוסף ל-\( r^2 \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לסמוך על שורש בנקודה צפה"
    ‏`int(math.sqrt(n))` נראה נכון, אבל ל-\( n \) גדול הוא טועה :
    ‏`int(math.sqrt(9999999999999999))` נותן 100000000, והשורש השלם הוא 99999999. ‏`double`
    מעגל את \( n \) ל-\( 10^{16} \) עוד לפני השורש. בחומרה, ובכל קוד שצריך תשובה מדויקת,
    משתמשים בשיטה השלמה, או ב-`math.isqrt` של Python.

??? trap "מלכודת : קדימות של הזזה"
    ‏`r << k + 1` הוא `r << (k + 1)`, כי בשתי השפות החיבור קודם להזזה. זה עובד כאן במקרה,
    אבל `3 * r2 << k + t2` נשבר. כל איבר בסוגריים משלו.

??? trap "מלכודת : רוחב של רגיסטר"
    השארית צריכה את כל 16 הביטים של \( n \), וה-\( \mathit{hi} = (r + 1)^2 \) בבודק צריך 17 :
    ‏\( 256^2 = 65536 \). ‏`hi` של 16 ביטים הופך ל-0 כש-\( r = 255 \), וה-assertion נכשל
    על \( n = 65535 \) בלי שום באג במודול.

??? trap "מלכודת : לבדוק רק ריבועים מושלמים"
    על \( n = s^2 \) גם מודול שמעגל למעלה יענה נכון. הטעות של off-by-one מופיעה דווקא
    ב-\( s^2 - 1 \), ולכן בודקים את שני הצדדים של כל מדרגה.

??? followup "שאלות המשך"
    - **עיגול לקרוב :** איך מקבלים את השורש המעוגל לשלם הקרוב, בלי עוד שלב?

        ??? fu-answer "תשובה"
            אם \( \mathit{rem} > r \), מוסיפים 1. כי \( \sqrt{n} \ge r + \tfrac12 \) אם ורק אם
            \( n \ge r^2 + r + \tfrac14 \), ולשלמים זה \( n - r^2 \ge r + 1 \).

    - **תוצאה בכל מחזור :** איך מקבלים שורש בכל שעון ולא כל 8?

        ??? fu-answer "תשובה"
            פורסים את 8 השלבים ל-pipeline : כל שלב עם המחסר שלו ורגיסטרים בין השלבים. ‏latency
            של 8 מחזורים, תוצאה בכל מחזור, ופי 8 מחסרים בשטח.

    - **בלי השוואה :** אפשר להוריד את הבורר שבוחר בין `rem` ל-`rem - trial`?

        ??? fu-answer "תשובה"
            כן, בשיטה שלא משחזרת (non-restoring) : תמיד מחסירים. אם השארית יצאה שלילית, הביט
            0, ובשלב הבא מחברים במקום לחסר. הסימן של השארית קובע את הביט.

    - **ומה עם Newton?** למה לא \( x \leftarrow (x + n/x)/2 \)?

        ??? fu-answer "תשובה"
            ‏Newton מתכנס בכמה איטרציות בלבד, אבל כל איטרציה היא חילוק. בתוכנה עם מחלק מהיר
            זה משתלם. בחומרה בלי מחלק, החילוק עצמו הוא 16 שלבים, יותר מכל השיטה הזו.
