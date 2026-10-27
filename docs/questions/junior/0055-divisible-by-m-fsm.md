---
id: 55
title: מכונת מצבים לחלוקה ב-3 – ביטים מה-MSB, מה-LSB ובכל בסיס
level: junior
difficulty: medium
kind: design
tags: [fsm, digital-logic, math, systemverilog, python]
source: "שאלת ראיון נפוצה בתכנון לוגי (divisible-by-3 FSM); הכיוון מה-LSB וההכללה לבסיס ול-k ביטים"
added: 2026-10-27
---

## השאלה

לרכיב נכנס ביט אחד בכל מחזור שעון, `din`. אחרי כל ביט, היציאה `div` צריכה לומר אם המספר
שנקרא **עד עכשיו** מתחלק ב-3. אין מקום לשמור את המספר עצמו : הוא יכול להיות ארוך כרצונכם.

- **סעיף א – מה-MSB :** הביט החדש הוא הביט הנמוך של המספר. הביטים 1, 1, 0 הם המספרים 1,
  3 ו-6, ולכן `div` הוא 0, 1, 1. תכננו מכונת מצבים. כמה מצבים צריך?
- **סעיף ב – מה-LSB :** הביט החדש הוא הביט **הגבוה** של המספר. הביטים 0, 1, 1 הם המספרים
  0, 2 ו-6. כמה מצבים צריך עכשיו?
- **סעיף ג – כל m וכל בסיס :** חלוקה ב-\( m \) אי-זוגי, כשבכל מחזור נכנסת ספרה בבסיס
  \( B \), למשל \( k \) ביטים יחד (בסיס \( 2^k \)) או ספרה עשרונית. כתבו מודול אחד עם
  פרמטרים לשני הכיוונים.

??? interviewer "מה המראיין בודק"
    - **מה זוכרים :** האם המועמד מבין שאת המספר אי אפשר לשמור, ומחפש את המידע הקטן ביותר
      שמספיק כדי לענות גם בעתיד.
    - **אינדוקציה :** האם הוא כותב את המעבר מתוך מה שביט חדש עושה למספר, ומוכיח שהמצב
      נשאר נכון.
    - **הכיוון השני :** האם הוא עוצר ב"צריך גם את המיקום", או בודק אם המיקום באמת נחוץ.
    - **מינימליות :** איך יודעים שאין מכונה קטנה יותר, ומה זה אומר על שני מצבים שמתנהגים
      אותו דבר.
    - **חומרה :** כמה ביטים יש לרגיסטר, ומה קורה ללוגיקה כשנכנסים כמה ביטים במחזור.

---

### סעיף א – הביטים מגיעים מה-MSB

??? tip "רמז 1"
    מה ביט חדש עושה למספר? אם המספר עד עכשיו הוא \( v \), אחרי הביט \( b \) הוא \( 2v + b \).

??? tip "רמז 2"
    כדי לדעת את השארית של \( 2v + b \) ב-3, מספיק לדעת את השארית של \( v \).

<div class="selfcheck" data-answer="2" data-show="2" data-hint="השארית עוברת 1, 2, 2 ואז 2 · 2 + 1 = 5, כלומר 2. ובדיקה : 1011 בבינארי הוא 11." markdown>
המכונה מקבלת את הביטים 1, 0, 1, 1 מה-MSB. באיזה מצב (איזו שארית) היא נמצאת בסוף?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שלושה מצבים : השארית \( r \) של המספר עד עכשיו. ביט \( b \) מעביר את \( r \)
        ל-\( (2r + b) \bmod 3 \), ו-`div` דולק כש-\( r = 0 \). מתחילים ב-\( r = 0 \).

    #### הרעיון { .sol-idea }

    המספר גדל בלי סוף, אבל השארית שלו ב-3 היא רק אחד משלושה ערכים, והיא כל מה שצריך :
    כשנכנס ביט, המספר הופך ל-\( 2v + b \), והשארית שלו נקבעת לפי השארית של \( v \)
    לבד. לכן המצב הוא השארית, ויש שלושה מצבים :

    <!-- gen 0 -->

    <svg class="figure dv-fig" viewBox="0 0 360 272" style="max-width:24rem" role="img" aria-label="מכונת המצבים של 3 מה-MSB : שלושה מצבים, השארית של המספר עד עכשיו"><defs><marker id="dv-arrow-m3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs><path class="fs-edge" d="M165.6,54.8 C158,14 202,14 194.4,54.8" marker-end="url(#dv-arrow-m3)"><title>0 --0--> 0</title></path><text class="fs-label halo" x="180" y="18" text-anchor="middle">0</text><path class="fs-edge is-found" d="M199.4,88.2 Q250.2,125.5 256.8,186.2" marker-end="url(#dv-arrow-m3)"><title>0 --1--> 1</title></path><text class="fs-label halo is-found" x="248.7" y="129.8" text-anchor="middle">1</text><path class="fs-edge" d="M237.7,221.7 Q180,247.1 124.1,222.5" marker-end="url(#dv-arrow-m3)"><title>1 --0--> 2</title></path><text class="fs-label halo" x="180.5" y="249.6" text-anchor="middle">0</text><path class="fs-edge is-found" d="M240.3,197.8 Q189.5,160.5 182.8,99.8" marker-end="url(#dv-arrow-m3)"><title>1 --1--> 0</title></path><text class="fs-label halo is-found" x="191" y="164.2" text-anchor="middle">1</text><path class="fs-edge" d="M122.3,202.3 Q180,176.9 235.9,201.5" marker-end="url(#dv-arrow-m3)"><title>2 --0--> 1</title></path><text class="fs-label halo" x="179.5" y="182.4" text-anchor="middle">0</text><path class="fs-edge is-found" d="M90.9,234.1 C59.4,261.1 37.4,222.9 76.5,209.1" marker-end="url(#dv-arrow-m3)"><title>2 --1--> 2</title></path><text class="fs-label halo is-found" x="48.4" y="246" text-anchor="middle">1</text><g class="fs-node is-start"><circle cx="180" cy="74" r="24"/><circle cx="180" cy="74" r="19"/><text x="180" y="79" text-anchor="middle">r=0</text></g><g class="fs-node"><circle cx="259.7" cy="212" r="24"/><text x="259.7" y="217" text-anchor="middle">r=1</text></g><g class="fs-node"><circle cx="100.3" cy="212" r="24"/><text x="100.3" y="217" text-anchor="middle">r=2</text></g></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="fs-key"></i>הביט 0</span><span><i class="fs-key-found"></i>הביט 1</span><span><i class="dv-key-acc"></i>עיגול כפול : המספר מתחלק (ומשם מתחילים)</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המצב :** ‏\( r = v \bmod 3 \), שני ביטים ברגיסטר. אחרי reset ‏\( r = 0 \) (עוד לא נקרא
       ביט, והמספר הוא 0).
    2. **המעבר :** ‏\( r' = (2r + b) \bmod 3 \). שישה מעברים בסך הכול, בטבלה למטה.
    3. **היציאה :** ‏`div = (r == 0)`. היא תלויה רק במצב, כלומר מכונת Moore.

    </div>

    <!-- gen 2 -->

    | המצב (השארית) | הביט | ‏\( 2r + b \) | המצב הבא |
    |:-:|:-:|:-:|:-:|
    | ‏0 | ‏0 | ‏0 | ‏0 |
    | ‏0 | ‏1 | ‏1 | ‏1 |
    | ‏1 | ‏0 | ‏2 | ‏2 |
    | ‏1 | ‏1 | ‏3 | ‏0 |
    | ‏2 | ‏0 | ‏4 | ‏1 |
    | ‏2 | ‏1 | ‏5 | ‏2 |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module div3_msb" linenums="1" hl_lines="10 11"
        // bits MSB first: the state is the remainder of the number read so far
        module div3_msb (
          input  logic clk, rst_n,
          input  logic din,               // the next bit: the number's new lowest bit
          output logic div                // the number read so far is divisible by 3
        );
          logic [1:0] r;
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) r <= 2'd0;
            else        r <= 2'((2 * r + din) % 3);   // (1)!
          assign div = (r == 2'd0);
        endmodule
        ```

        1. ‏\( 2r + b \) הוא לכל היותר 5, והסינתזה הופכת את הביטוי לטבלה של שש שורות.

    === "Python"
        ```python title="div3_msb" linenums="1" hl_lines="5"
        def div3_msb(bits: list[int]) -> list[bool]:
            """After each bit (MSB first): is the number read so far divisible by 3?"""
            r, out = 0, []
            for b in bits:
                r = (2 * r + b) % 3                    # (1)!
                out.append(r == 0)
            return out
        ```

        1. המספר הופך ל-\( 2v + b \), והשארית שלו תלויה רק בשארית של \( v \).

    #### למה זה נכון { .sol-proof }

    **המצב הוא השארית.** באינדוקציה : בהתחלה \( v = 0 \) ו-\( r = 0 \). אם \( r \equiv v \),
    אז \( 2r + b \equiv 2v + b \pmod 3 \), ולכן אחרי הביט \( r' \) הוא השארית של המספר
    החדש. היציאה דולקת בדיוק כשהשארית 0.

    **פחות משלושה אי אפשר.** כל שני מצבים צריכים להיות שונים : המספר 0 מתחלק, 1 ו-2 לא,
    ולכן 0 שונה משניהם כבר עכשיו. ‏1 ו-2 נבדלים אחרי הביט 1 : ‏\( 2 \cdot 1 + 1 = 3 \)
    מתחלק, ו-\( 2 \cdot 2 + 1 = 5 \) לא.

---

### סעיף ב – הביטים מגיעים מה-LSB

עכשיו הביט ה-\( k \) (מ-0) שנכנס הוא הביט שערכו \( 2^k \). המספר \( 6 = 110_2 \) מגיע
כ-0, 1, 1. כמה מצבים צריך?

??? tip "רמז 1"
    הביט החדש מוסיף \( b \cdot 2^k \). ב-3, ‏\( 2^k \) הוא 1, 2, 1, 2, ..., ולכן נראה שצריך
    לזכור גם את השארית וגם אם \( k \) זוגי. זה 6 מצבים. האם כולם באמת שונים?

??? tip "רמז 2"
    במקום השארית \( r \) שמרו את \( x = r \cdot 2^{-k} \bmod 3 \) (ב-3 ‏\( 2^{-1} = 2 \),
    כי \( 2 \cdot 2 = 4 \equiv 1 \)). מה ביט חדש עושה ל-\( x \)? ומתי \( r = 0 \)?

<div class="selfcheck" data-answer="3" data-show="3" data-hint="המכונה הנאיבית שומרת שארית וזוגיות : 6 מצבים. אבל שני מצבים עם אותו x = r · 2^-k מתנהגים אותו דבר על כל ביט שיבוא." markdown>
כמה מצבים יש למכונה הקטנה ביותר שבודקת חלוקה ב-3 כשהביטים מגיעים מה-LSB?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        גם כאן שלושה מצבים. שומרים \( x = r \cdot 2^{-k} \bmod 3 \), ‏ביט \( b \) מעביר אותו
        ל-\( 2(x + b) \bmod 3 \), ו-`div` דולק כש-\( x = 0 \). המכונה הנאיבית של 6 מצבים
        (שארית וזוגיות) מתמזגת לשלושה.

    #### הרעיון { .sol-idea }

    **הניסיון הראשון.** ביט חדש מוסיף \( b \cdot 2^k \), ו-\( 2^k \bmod 3 \) מתחלף בין 1
    ל-2. לכן שומרים את השארית ואת זוגיות \( k \) : שישה מצבים. זה עובד, אבל לא צריך את
    כולם.

    **מה באמת קובע את העתיד.** אחרי \( k \) ביטים, כל ביט שיבוא מוסיף כפולה של \( 2^k \).
    לכן המספר כולו יהיה \( v + 2^k w \), כאשר \( w \) הוא המספר שהביטים הבאים יבנו. הוא
    מתחלק ב-3 אם ורק אם \( v \cdot 2^{-k} + w \equiv 0 \) : כפל ב-\( 2^{-k} \) לא משנה
    חלוקה ב-3, כי 2 הפיך מודולו 3. לכן העתיד תלוי רק ב-\( x = v \cdot 2^{-k} \bmod 3 \),
    ושני מצבים נאיביים עם אותו \( x \) הם אותו מצב :

    <!-- gen 3 -->

    | השארית r | הביטים עד עכשיו k | המשקל של הביט הבא ‏\( 2^k \bmod 3 \) | ‏\( x = r \cdot 2^{-k} \bmod 3 \) |
    |:-:|:-:|:-:|:-:|
    | ‏0 | זוגי | ‏1 | ‏0 |
    | ‏0 | אי-זוגי | ‏2 | ‏0 |
    | ‏1 | זוגי | ‏1 | ‏1 |
    | ‏1 | אי-זוגי | ‏2 | ‏2 |
    | ‏2 | זוגי | ‏1 | ‏2 |
    | ‏2 | אי-זוגי | ‏2 | ‏1 |

    <!-- /gen -->

    **המעבר.** ‏\( x' = (v + b \cdot 2^k) \cdot 2^{-(k+1)} = (x + b) \cdot 2^{-1} \), כלומר
    ‏\( x' = 2(x + b) \bmod 3 \). המיקום \( k \) נעלם מהנוסחה, ולכן אין צורך לזכור אותו :

    <!-- gen 4 -->

    <svg class="figure dv-fig" viewBox="0 0 360 272" style="max-width:24rem" role="img" aria-label="מכונת המצבים של 3 מה-LSB : שלושה מצבים, x הוא השארית כפול 2 בחזקת מינוס k"><defs><marker id="dv-arrow-l3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs><path class="fs-edge" d="M165.6,54.8 C158,14 202,14 194.4,54.8" marker-end="url(#dv-arrow-l3)"><title>0 --0--> 0</title></path><text class="fs-label halo" x="180" y="18" text-anchor="middle">0</text><path class="fs-edge is-found" d="M177.4,97.9 Q170.5,160.5 121.3,196.6" marker-end="url(#dv-arrow-l3)"><title>0 --1--> 2</title></path><text class="fs-label halo is-found" x="169.5" y="163.4" text-anchor="middle">1</text><path class="fs-edge" d="M237.7,221.7 Q180,247.1 124.1,222.5" marker-end="url(#dv-arrow-l3)"><title>1 --0--> 2</title></path><text class="fs-label halo" x="180.5" y="249.6" text-anchor="middle">0</text><path class="fs-edge is-found" d="M283.5,209.1 C322.6,222.9 300.6,261.1 269.1,234.1" marker-end="url(#dv-arrow-l3)"><title>1 --1--> 1</title></path><text class="fs-label halo is-found" x="311.6" y="246" text-anchor="middle">1</text><path class="fs-edge" d="M122.3,202.3 Q180,176.9 235.9,201.5" marker-end="url(#dv-arrow-l3)"><title>2 --0--> 1</title></path><text class="fs-label halo" x="179.5" y="182.4" text-anchor="middle">0</text><path class="fs-edge is-found" d="M102.9,188.1 Q109.8,125.5 159,89.4" marker-end="url(#dv-arrow-l3)"><title>2 --1--> 0</title></path><text class="fs-label halo is-found" x="110.9" y="130.6" text-anchor="middle">1</text><g class="fs-node is-start"><circle cx="180" cy="74" r="24"/><circle cx="180" cy="74" r="19"/><text x="180" y="79" text-anchor="middle">x=0</text></g><g class="fs-node"><circle cx="259.7" cy="212" r="24"/><text x="259.7" y="217" text-anchor="middle">x=1</text></g><g class="fs-node"><circle cx="100.3" cy="212" r="24"/><text x="100.3" y="217" text-anchor="middle">x=2</text></g></svg>

    <!-- /gen -->

    **הפתעה.** זו בדיוק המכונה של סעיף א, עם 1 ו-2 בתפקידים הפוכים. הסיבה : ‏\( 2 \equiv -1
    \pmod 3 \), ולכן היפוך סדר הביטים רק מחליף את סימן השארית, ו-0 נשאר 0. ב-5 זה כבר לא
    כך : לשני הכיוונים יש חמישה מצבים, אבל המכונות שונות.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המצב :** ‏\( x = v \cdot 2^{-k} \bmod 3 \), שני ביטים. השארית עצמה היא
       \( x \cdot 2^k \bmod 3 \), אבל לא צריך אותה.
    2. **המעבר :** ‏\( x' = 2(x + b) \bmod 3 \).
    3. **היציאה :** ‏`div = (x == 0)`, כי \( v \equiv 0 \) אם ורק אם \( x \equiv 0 \).
    4. **דוגמה :** ‏6 מגיע כ-0, 1, 1. ‏\( x \) עובר 0, 2, 0 (‏\( 2 \cdot 0 = 0 \), ‏\( 2 \cdot 1 = 2 \),
       ‏\( 2 \cdot 3 = 6 \equiv 0 \)), ולכן `div` הוא 1, 0, 1 : המספרים 0, 2 ו-6.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module div3_lsb" linenums="1" hl_lines="10 11"
        // bits LSB first: the state is x = remainder * 2^-k mod 3 (k bits read so far)
        module div3_lsb (
          input  logic clk, rst_n,
          input  logic din,               // the next bit: the number's new highest bit
          output logic div                // the number read so far is divisible by 3
        );
          logic [1:0] x;
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) x <= 2'd0;
            else        x <= 2'((2 * (x + din)) % 3);   // (1)!
          assign div = (x == 2'd0);
        endmodule
        ```

        1. ‏\( x' = (x + b) \cdot 2^{-1} \), ומודולו 3 ‏\( 2^{-1} = 2 \). המיקום \( k \) לא מופיע.

    === "Python"
        ```python title="div3_lsb" linenums="1" hl_lines="5"
        def div3_lsb(bits: list[int]) -> list[bool]:
            """After each bit (LSB first): is the number read so far divisible by 3?"""
            x, out = 0, []                             # x = remainder * 2^-k mod 3
            for b in bits:
                x = 2 * (x + b) % 3                    # (1)!
                out.append(x == 0)
            return out
        ```

        1. ‏\( x' = (x + b) \cdot 2^{-1} \bmod 3 \), ו-\( 2^{-1} = 2 \).

    #### למה זה נכון { .sol-proof }

    **המצב נכון.** באינדוקציה : בהתחלה \( v = 0 \), ‏\( k = 0 \) ו-\( x = 0 \). אם
    \( x \equiv v \cdot 2^{-k} \), אחרי הביט \( b \) המספר הוא \( v + b \cdot 2^k \), ו-
    ‏\( (v + b \cdot 2^k) \cdot 2^{-(k+1)} \equiv (x + b) \cdot 2^{-1} = x' \).

    **היציאה נכונה.** ‏\( 2^k \) הפיך מודולו 3, ולכן \( v \equiv 0 \) אם ורק אם
    \( x = v \cdot 2^{-k} \equiv 0 \).

    **פחות משלושה אי אפשר.** אחרי \( k \) ביטים, הביטים הבאים יכולים לבנות כל \( w \), ולכן
    שני ערכים שונים של \( x \) נבדלים : יש \( w \) שבו \( x + w \equiv 0 \) והשני לא.

---

### סעיף ג – כל m, כל בסיס, ו-k ביטים במחזור

עכשיו בכל מחזור נכנסת ספרה \( d \) בבסיס \( B \), והשאלה היא חלוקה ב-\( m \), כאשר
\( m \) ו-\( B \) זרים (למשל \( m \) אי-זוגי ו-\( B = 2^k \)). כמה מצבים צריך בכל כיוון,
ומה המעברים?

??? tip "רמז 1"
    מה-MSB ספרה חדשה הופכת את המספר ל-\( Bv + d \). מה-LSB היא מוסיפה \( d \cdot B^k \).

??? tip "רמז 2"
    ‏\( B \) הפיך מודולו \( m \) כשהם זרים. העתיקו את הטריק של סעיף ב עם \( B^{-1} \).

<div class="selfcheck" data-answer="5" data-show="5" data-hint="מה-LSB המעבר הוא x' = (x + d) · B^-1. מחפשים y שבו 10y משאיר שארית 1 ב-7 : ‏10 · 5 = 50 = 7 · 7 + 1." markdown>
מכונה מה-LSB בודקת חלוקה ב-7 של מספר עשרוני, ספרה במחזור. בכמה כופלים את \( x + d \)?
(התשובה היא מספר בין 0 ל-6.)
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏\( m \) מצבים בשני הכיוונים. מה-MSB : ‏\( r' = (Br + d) \bmod m \). מה-LSB :
        ‏\( x' = (x + d) \cdot B^{-1} \bmod m \). ‏\( k \) ביטים במחזור הם ספרה בבסיס \( 2^k \) :
        אותם \( m \) מצבים, רק המכפילים משתנים.

    <!-- cost: מצבים \( m \) | רגיסטר \( \lceil \log_2 m \rceil \) ביטים | לוגיקה טבלה של \( m \times B \) -->

    #### הרעיון { .sol-idea }

    **שני הכיוונים.** סעיפים א ו-ב לא השתמשו בשום דבר מיוחד ל-3 או ל-2, חוץ מכך ש-2
    הפיך מודולו 3. לכן אותו דבר עובד לכל \( m \) ו-\( B \) זרים : מה-MSB המצב הוא
    השארית, ומה-LSB המצב הוא \( x = v \cdot B^{-k} \bmod m \).

    **‏k ביטים במחזור.** ‏\( k \) ביטים שנכנסים יחד הם ספרה אחת בבסיס \( 2^k \), ולכן זה אותו
    מקרה עם \( B = 2^k \). מספר המצבים לא משתנה, רק המכפילים : ‏\( B \bmod m \) מה-MSB
    ו-\( B^{-1} \bmod m \) מה-LSB. בטבלה, בכל תא המכפיל מה-MSB ואחריו המכפיל מה-LSB :

    <!-- gen 6 -->

    | ‏k ביטים במחזור | הבסיס ‏\( B = 2^k \) | ‏m = 3 | ‏m = 5 | ‏m = 7 |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏1 | ‏2 | ‏2, 2 | ‏2, 3 | ‏2, 4 |
    | ‏2 | ‏4 | ‏1, 1 | ‏4, 4 | ‏4, 2 |
    | ‏3 | ‏8 | ‏2, 2 | ‏3, 2 | ‏1, 1 |
    | ‏4 | ‏16 | ‏1, 1 | ‏1, 1 | ‏2, 4 |

    <!-- /gen -->

    כשהמכפיל הוא 1, המכונה רק מחברת את הספרות מודולו \( m \), באותו אופן בשני הכיוונים.
    זה הכלל המוכר "מספר מתחלק ב-3 אם סכום הספרות שלו מתחלק ב-3" : ‏\( 10 \equiv 1 \pmod 3 \).
    ב-3 עם שני ביטים במחזור (‏\( 4 \equiv 1 \)), וב-7 עם שלושה (‏\( 8 \equiv 1 \)), זה אותו כלל
    בבסיס 4 ובבסיס 8.

    **כמה מצבים בכל כיוון.** הטבלה סופרת, לכל \( m \) עד 16 וביט במחזור, את המצבים של
    המכונה הקטנה ביותר : המכונות הנאיביות נבנו מההגדרה ומוזערו. ב-\( m \) אי-זוגי שני
    הכיוונים צריכים \( m \) בדיוק, והמכונה הנאיבית מה-LSB גדולה פי אורך המחזור של
    \( 2^k \bmod m \). ב-\( m \) זוגי מספיק פחות, וזו שאלת המשך :

    <!-- gen 5 -->

    | ‏m | מה-MSB | מה-LSB | המכונה הנאיבית מה-LSB |
    |:-:|:-:|:-:|:-:|
    | ‏2 | ‏2 | ‏3 | ‏3 |
    | ‏3 | ‏3 | ‏3 | ‏6 |
    | ‏4 | ‏3 | ‏4 | ‏7 |
    | ‏5 | ‏5 | ‏5 | ‏20 |
    | ‏6 | ‏4 | ‏5 | ‏13 |
    | ‏7 | ‏7 | ‏7 | ‏21 |
    | ‏8 | ‏4 | ‏5 | ‏15 |
    | ‏9 | ‏9 | ‏9 | ‏54 |
    | ‏10 | ‏6 | ‏7 | ‏41 |
    | ‏11 | ‏11 | ‏11 | ‏110 |
    | ‏12 | ‏5 | ‏6 | ‏27 |
    | ‏13 | ‏13 | ‏13 | ‏156 |
    | ‏14 | ‏8 | ‏9 | ‏43 |
    | ‏15 | ‏15 | ‏15 | ‏60 |
    | ‏16 | ‏5 | ‏6 | ‏31 |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module div_fsm" linenums="1" hl_lines="16 20 21"
        // divisible by M, one base-B digit a cycle, from the MSB or from the LSB (gcd(B, M) = 1)
        module div_fsm #(
          parameter int M   = 7,
          parameter int B   = 8,          // 2**k for k bits a cycle
          parameter bit LSB = 1           // 1: the digits arrive lowest first
        ) (
          input  logic clk, rst_n,
          input  logic [$clog2(B)-1:0] d, // the next digit, 0 to B-1
          output logic div
        );
          localparam int W = $clog2(M);
          function automatic int inverse(int b, int m);   // b^-1 mod m
            for (int y = 0; y < m; y++) if (b * y % m == 1 % m) return y;
            return 0;                                     // (1)!
          endfunction
          localparam int BINV = inverse(B % M, M);
          logic [W-1:0] s;                // MSB: the remainder; LSB: x = remainder * B^-k
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n)   s <= '0;
            else if (LSB) s <= W'((s + d) * BINV % M);   // (2)!
            else          s <= W'((s * B + d) % M);
          assign div = (s == 0);
        endmodule
        ```

        1. לא קורה כש-\( B \) ו-\( M \) זרים. ‏`inverse` רץ בזמן ה-elaboration, ו-`BINV` הוא קבוע.
        2. אותו כלל של סעיף ב : ‏\( x' = (x + d) \cdot B^{-1} \).

    === "Python"
        ```python title="div_fsm" linenums="1" hl_lines="4 7"
        def div_fsm(digits: list[int], m: int, base: int = 2, lsb: bool = False) -> list[bool]:
            """After each digit: is the number read so far divisible by m? (gcd(base, m) = 1)
            From the MSB the state is the remainder; from the LSB it is remainder * base^-k."""
            inv = pow(base, -1, m)                     # (1)!
            s, out = 0, []
            for d in digits:
                s = (s + d) * inv % m if lsb else (s * base + d) % m
                out.append(s == 0)
            return out
        ```

        1. ‏\( B^{-1} \bmod m \). ‏`pow` מעלה שגיאה כש-\( B \) ו-\( m \) לא זרים.

    #### למה זה נכון { .sol-proof }

    **המעברים.** מה-MSB : ‏\( r \equiv v \) גורר \( Br + d \equiv Bv + d \). מה-LSB :
    ‏\( (v + d B^k) B^{-(k+1)} \equiv (x + d) B^{-1} \). בשני המקרים היציאה דולקת כשהמצב 0,
    כי \( B^k \) הפיך מודולו \( m \).

    **פחות מ-\( m \) אי אפשר.** קחו שני מצבים שונים \( s \ne s' \). מה-LSB, הספרות הבאות
    יכולות לבנות כל \( w \), ויש \( w \) שבו \( s + w \equiv 0 \) אבל \( s' + w \not\equiv 0 \).
    מה-MSB, ‏\( \ell \) ספרות נוספות נותנות \( B^\ell s + w \). בוחרים \( \ell \) עם
    \( B^\ell \ge m \), כך ש-\( w \) יכול להיות כל שארית, ו-\( B^\ell (s - s') \not\equiv 0 \) כי
    \( B \) הפיך. כל שני מצבים נבדלים, ולכן צריך את כל \( m \).

    **נסו בעצמכם.** אותן ספרות נכנסות לשתי המכונות, לזו מה-MSB מהספרה הגבוהה ולזו מה-LSB
    מהנמוכה. כל מכונה רואה מספר אחר בדרך, אבל בסוף שתיהן עונות על אותו מספר. בוחרים
    \( m \), בסיס ומספר, או מוסיפים ספרות בכפתורים :

    <div class="explorer" data-kind="divfsm" data-m="3" data-base="2" data-num="1011"></div>

    #### סיבוכיות { .sol-cost }

    - **מצבים :** ‏\( m \), כלומר רגיסטר של \( \lceil \log_2 m \rceil \) ביטים, בלי קשר לאורך המספר.
    - **לוגיקה :** טבלת מעברים של \( m \times B \) שורות. ‏\( k \) ביטים במחזור מגדילים את הטבלה
      פי \( 2^{k-1} \) לעומת ביט אחד, אבל המסלול הקריטי הוא חיפוש אחד בטבלה, ולא \( k \) צעדים בשרשרת.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לשמור את המספר"
    רגיסטר שמחזיק את המספר כולו ובודק `% 3` עובד רק עד שהוא מתמלא. השאלה היא בדיוק מה
    **מספיק** לזכור, והתשובה היא שני ביטים, לכל אורך.

??? trap "מלכודת : 'מה-LSB צריך גם את המיקום'"
    שישה מצבים (שארית וזוגיות) הם מכונה נכונה, אבל לא הקטנה ביותר. המיקום נחוץ רק כדי
    לדעת את השארית עצמה, וכדי לענות "מתחלק או לא" מספיק \( x = r \cdot 2^{-k} \).

??? trap "מלכודת : בסיס ו-m לא זרים"
    בבסיס 10 ‏\( 10^{-1} \bmod 5 \) לא קיים, והנוסחה מה-LSB לא עובדת. אבל חלוקה ב-5 בבסיס
    10 תלויה רק בספרה האחרונה, ולכן מה-MSB מספיקים שני מצבים ומה-LSB שלושה (הספרה
    הראשונה שנקראה, ואז הכרעה קבועה).

??? followup "שאלות המשך"
    - **‏m זוגי :** כמה מצבים צריך לחלוקה ב-6 או ב-12, ביט במחזור?

        ??? fu-answer "תשובה"
            כש-\( m = 2^a m' \) עם \( m' \) אי-זוגי : מה-MSB ‏\( m' + a \) מצבים, ומה-LSB ‏\( m' + a + 1 \)
            (‏\( a \) הביטים הראשונים חייבים להיות 0, ומצב "נכשל" אחד). ל-6 : ‏4 ו-5, ל-12 : ‏5 ו-6, כמו בטבלה.

    - **לא רק כן או לא :** רוצים את השארית עצמה ביציאה. מה משתנה?

        ??? fu-answer "תשובה"
            מה-MSB כלום : המצב הוא השארית. מה-LSB השארית היא \( x \cdot 2^k \), ולכן צריך גם את
            \( k \) מודולו אורך המחזור, והמכונה הנאיבית (6 מצבים ל-3) היא כבר הקטנה ביותר.

    - **הכלל של 11 :** איך זה קשור לכלל "ההפרש בין סכום הספרות במקומות הזוגיים והאי-זוגיים"?

        ??? fu-answer "תשובה"
            ‏\( 10 \equiv -1 \pmod{11} \), בדיוק כמו \( 2 \equiv -1 \pmod 3 \) בסעיף ב. לכן הכפל
            בבסיס הוא החלפת סימן, והשארית היא סכום הספרות לסירוגין.

    - **בדיקה :** איך מאמתים את המודול?

        ??? fu-answer "תשובה"
            מודל ייחוס שסוכם את המספר כולו (‏`longint` או Python עם מספרים גדולים), ובכל מחזור
            assertion ש-`div` שווה ל-\( v \bmod m = 0 \). הרצה על כל הרצפים עד אורך 12, ועל רצפים
            אקראיים ארוכים, בשני הכיוונים.
