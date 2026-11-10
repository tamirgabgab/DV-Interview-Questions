---
id: 82
title: משחק Nim – ה-XOR של הערימות, המשחק ההפוך ומספרי גרנדי
level: senior
difficulty: medium
kind: math
tags: [game-theory, bitwise, math, logic-puzzles, algorithms, systemverilog, python]
source: "משחק קלאסי; האסטרטגיה של בוטון (1901), ומשפט ספרג–גרנדי (1935, 1939)"
added: 2026-11-04
---

## השאלה

שני שחקנים משחקים בערימות של אסימונים. בכל תור השחקן בוחר ערימה אחת ולוקח ממנה כמה
אסימונים שהוא רוצה : לפחות אחד, ואפשר גם את כל הערימה. השחקנים מתחלפים, ושניהם משחקים
הכי טוב שאפשר.

- **סעיף א – האחרון שלוקח מנצח :** יש שלוש ערימות, של 3, 4 ו-5 אסימונים, ואתם מתחילים.
  האם אתם מנצחים, ובאיזה מהלך? ובאופן כללי : בכל מצב, איך יודעים מי מנצח, ומה המהלך המנצח?
- **סעיף ב – האחרון שלוקח מפסיד :** אותו משחק, אבל מי שלוקח את האסימון האחרון מפסיד. מה
  משתנה באסטרטגיה?
- **סעיף ג – לוקחים רק 1, 3 או 4 :** חוזרים לחוק של סעיף א, אבל מכל ערימה מותר לקחת רק 1,
  3 או 4 אסימונים בתור. מי מנצח ב-3, 4 ו-5 עכשיו, ואיך מחשבים כל מצב?

??? interviewer "מה המראיין בודק"
    - **מצב מנצח ומצב מפסיד :** האם המועמד מגדיר "מי שתורו מפסיד" כתכונה של מצב, ומבין
      שמספיק להראות שלוש תכונות : הסוף מפסיד, מכל מצב מפסיד כל מהלך יוצא ממנו, ומכל מצב
      אחר יש מהלך חזרה אליו.
    - **הבינארי :** האם הוא מגיע ל-XOR, ולא נתקע על הסכום או על הזוגיות.
    - **הוכחה ולא רק נוסחה :** שני הכיוונים, ולמה תמיד יש ערימה שאפשר להקטין לגודל הנכון.
    - **חוק אחר :** האם הוא מזהה מתי האסטרטגיה עוד עובדת עם תיקון קטן (סעיף ב), ומתי צריך
      כלי חדש (מספרי גרנדי, סעיף ג).
    - **קוד :** פונקציה שמחזירה מהלך מנצח במעבר אחד על הערימות, בלי חיפוש על כל המשחק.

---

### סעיף א – האחרון שלוקח מנצח

הערימות 3, 4 ו-5, ואתם מתחילים. האם אתם מנצחים, ובאיזה מהלך? ובאופן כללי, בכל מצב?

??? tip "רמז 1"
    התחילו ממצבים קטנים. שתי ערימות שוות : מי מנצח, ואיך? ושלוש ערימות של 1, 2 ו-3?

??? tip "רמז 2"
    כתבו את הערימות בבינארי, זו מעל זו. מה משותף לשתי ערימות שוות ול-1, 2, 3, בכל עמודה של
    ביטים?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מנצחים : לוקחים 2 מהערימה של 3, ומשאירים 1, 4 ו-5. הכלל : מי שתורו מפסיד בדיוק כשה-XOR
        של כל הערימות הוא 0. כאן \( 3 \oplus 4 \oplus 5 = 2 \), ולכן מי שמתחיל מנצח. המהלך
        המנצח מקטין ערימה \( h \) ל-\( h \oplus x \), כש-\( x \) הוא ה-XOR, ובוחרים ערימה שיש לה
        את הביט הגבוה של \( x \). ב-3, 4, 5 רק לערימה של 3 יש אותו, ולכן זה המהלך המנצח היחיד.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **מצב מפסיד.** נקרא למצב מפסיד אם מי שתורו מפסיד בו, כשהיריב משחק נכון. השולחן הריק
    הוא מצב מפסיד : מי שתורו כבר הפסיד, כי היריב לקח את האסימון האחרון. מצב הוא מנצח אם יש
    ממנו מהלך למצב מפסיד, ומפסיד אם כל המהלכים ממנו מובילים למצבים מנצחים.

    **ה-XOR.** הטענה : מצב מפסיד בדיוק כשה-XOR של הערימות הוא 0, כלומר כשבכל עמודה של ביטים
    יש מספר זוגי של אחדות. בשתי ערימות שוות כל עמודה מכילה שני ביטים שווים, וב-1, 2, 3
    (‏01, 10, 11) כל עמודה מכילה שתי אחדות. ב-3, 4, 5 עמודת ה-2 מכילה אחד בודד, ולכן ה-XOR
    הוא 2. כדי לאפס אותו צריך להפוך את הביט הזה בערימה שיש לה אותו, ורק ל-3 יש :

    <!-- gen 0 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="סעיף א : הערימות 3, 4 ו-5 בבינארי ושורת ה-XOR שלהן, 010 = 2. הביט הגבוה של ה-XOR הוא ביט ה-2, ורק לערימה 3 יש אותו"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>4</td><td>2</td><td>1</td><td class="pm-val"></td></tr><tr><th dir="rtl">ערימה 3</th><td class="pm-c">0</td><td class="pm-c c2 is-hl">1</td><td class="pm-c c1">1</td><td class="pm-val">= 3</td></tr><tr><th dir="rtl">ערימה 4</th><td class="pm-c c1">1</td><td class="pm-c is-hl">0</td><td class="pm-c">0</td><td class="pm-val">= 4</td></tr><tr><th dir="rtl">ערימה 5</th><td class="pm-c c1">1</td><td class="pm-c is-hl">0</td><td class="pm-c c1">1</td><td class="pm-val">= 5</td></tr><tr><th dir="rtl">‏XOR</th><td class="pm-c">0</td><td class="pm-c c1 is-hl">1</td><td class="pm-c">0</td><td class="pm-val">= 2</td></tr></tbody></table></div>

    <!-- /gen -->

    אחרי שלוקחים 2 מהערימה של 3, נשארים 1, 4 ו-5, וה-XOR שלהם 0 :

    <!-- gen 1 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="סעיף א : אחרי המהלך, הערימות 1, 4 ו-5, וה-XOR שלהן 000 = 0"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>4</td><td>2</td><td>1</td><td class="pm-val"></td></tr><tr><th dir="rtl">ערימה 1</th><td class="pm-c">0</td><td class="pm-c">0</td><td class="pm-c c1">1</td><td class="pm-val">= 1</td></tr><tr><th dir="rtl">ערימה 4</th><td class="pm-c c1">1</td><td class="pm-c">0</td><td class="pm-c">0</td><td class="pm-val">= 4</td></tr><tr><th dir="rtl">ערימה 5</th><td class="pm-c c1">1</td><td class="pm-c">0</td><td class="pm-c c1">1</td><td class="pm-val">= 5</td></tr><tr><th dir="rtl">‏XOR</th><td class="pm-c c3">0</td><td class="pm-c c3">0</td><td class="pm-c c3">0</td><td class="pm-val">= 0</td></tr></tbody></table></div>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="pm-key-c1"></i>ביט 1 בערימה</span><span><i class="pm-key-hl"></i>העמודה של הביט הגבוה של ה-XOR</span><span><i class="pm-key-c2"></i>הערימה שיש לה את הביט הזה : ממנה לוקחים</span><span><i class="pm-key-c3"></i>‏XOR = 0 : מי שתורו מפסיד</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ה-XOR :** מחשבים \( x = h_1 \oplus h_2 \oplus \dots \oplus h_n \).
    2. **‏x = 0 :** אין מהלך מנצח. כל מהלך משאיר ליריב מצב מנצח, ונשאר לקוות שהוא יטעה.
    3. **הביט הגבוה :** אם \( x \ne 0 \), מוצאים את הביט הגבוה של \( x \) וערימה \( h \) שיש לה
       את הביט הזה.
    4. **המהלך :** מקטינים את \( h \) ל-\( h \oplus x \). זה פחות מ-\( h \), כי הביט הגבוה של
       \( x \) נכבה ב-\( h \) והביטים מעליו לא משתנים, וה-XOR החדש הוא
       \( x \oplus h \oplus (h \oplus x) = 0 \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="nim_move" linenums="1" hl_lines="8 12 13"
        from functools import reduce
        from operator import xor


        def nim_move(heaps: list[int]):
            """Normal Nim (the last to take wins): a winning move (heap index, new size),
            or None when the player to move loses against best play."""
            x = reduce(xor, heaps, 0)      # (1)!
            if x == 0:
                return None                # (2)!
            for i, h in enumerate(heaps):
                if h ^ x < h:              # (3)!
                    return i, h ^ x
            return None
        ```

        1. ה-XOR של כל הערימות, במעבר אחד.
        2. מצב מפסיד : כל מהלך משנה ערימה אחת, ולכן משנה את ה-XOR לערך שאינו 0.
        3. ‏`h ^ x < h` בדיוק כשלערימה יש את הביט הגבוה של \( x \). תמיד יש ערימה כזו, כי הביט
           הזה הגיע ל-\( x \) מאחת הערימות.

    === "SystemVerilog"
        ```systemverilog title="nim_move" linenums="1" hl_lines="6 7 9 10 11"
        // normal Nim (the last to take wins): a winning move, heap idx down to new_size;
        // returns 0 when the player to move loses against best play
        function automatic bit nim_move(int heaps[$], output int idx, output int new_size);
          int x;
          x = 0;
          foreach (heaps[i]) x ^= heaps[i];          // (1)!
          if (x == 0) return 0;                      // (2)!
          foreach (heaps[i])
            if ((heaps[i] ^ x) < heaps[i]) begin     // (3)!
              idx = i;
              new_size = heaps[i] ^ x;
              return 1;
            end
          return 0;
        endfunction
        ```

        1. ה-XOR של כל הערימות. בחומרה זה עץ של שערי XOR, בתרשים שלמטה.
        2. מצב מפסיד : אין מהלך מנצח.
        3. הערימה הראשונה שיש לה את הביט הגבוה של \( x \).

    **בחומרה.** אותו כלל הוא גם מעגל צירופי, בלי שעון. עץ XOR מחשב את \( x \), גלאי האחד
    המוביל משאיר ממנו רק את הביט הגבוה (`top`), ‏AND של כל ערימה עם `top` אומר אם היא
    מועמדת, מקודד עדיפות בוחר את המועמדת הראשונה, ומרבב עם XOR נותן את הגודל החדש.
    ל-\( n \) ערימות של \( w \) ביטים העומק הוא \( O(\log n + \log w) \) רמות של שערים :

    <!-- gen 3 -->

    <svg class="figure nm-fig nm-dp" viewBox="0 0 400 440" direction="ltr" style="max-width:25rem" role="img" aria-label="תרשים המלבנים של nim_move_hw, מעגל צירופי בלי שעון : עץ XOR מחשב את x מכל הערימות. גלאי האחד המוביל מוציא את top, עם ביט דלוק אחד במקום הביט הגבוה של x. לכל ערימה, AND עם top ואחריו OR של הביטים אומר אם היא מועמדת, ו-valid הוא OR של המועמדות. מקודד עדיפות בוחר את המועמדת הראשונה, idx, ומרבב בוחר את heap[idx], וה-XOR שלו עם x הוא new_size"><defs><marker id="nm-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="nm-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs><g class="nm-blk nm-tree"><rect x="50" y="40" width="270" height="46" rx="5"/><text x="185" y="60" text-anchor="middle">XOR tree</text><text class="nm-sub" x="185" y="76" text-anchor="middle">x = heap[0] ^ ... ^ heap[n-1]</text></g><g class="nm-blk nm-logic"><rect x="50" y="116" width="270" height="46" rx="5"/><text x="185" y="136" text-anchor="middle">leading one</text><text class="nm-sub" x="185" y="152" text-anchor="middle">top = the highest 1 of x</text></g><g class="nm-blk nm-logic"><rect x="50" y="192" width="270" height="46" rx="5"/><text x="185" y="212" text-anchor="middle">candidates</text><text class="nm-sub" x="185" y="228" text-anchor="middle">cand[i] = |(heap[i] &amp; top)</text></g><g class="nm-blk nm-logic"><rect x="50" y="268" width="270" height="46" rx="5"/><text x="185" y="288" text-anchor="middle">priority encoder</text><text class="nm-sub" x="185" y="304" text-anchor="middle">idx = the first 1 of cand</text></g><g class="nm-blk nm-out"><rect x="50" y="344" width="270" height="46" rx="5"/><text x="185" y="364" text-anchor="middle">mux + XOR</text><text class="nm-sub" x="185" y="380" text-anchor="middle">new_size = heap[idx] ^ x</text></g><path class="nm-wire" d="M185,4 L185,40" marker-end="url(#nm-hb)"/><text class="nm-wlab" x="179" y="16" text-anchor="end">heap[0..n-1]</text><path class="nm-wire" d="M185,22 L350,22 L350,215 L320,215" marker-end="url(#nm-hb)"/><path class="nm-wire" d="M350,215 L350,367 L320,367" marker-end="url(#nm-hb)"/><text class="nm-wlab" x="355" y="335" text-anchor="start">heap</text><path class="nm-wire" d="M185,86 L185,116" marker-end="url(#nm-hb)"/><text class="nm-wlab" x="191" y="106" text-anchor="start">x</text><path class="nm-wire" d="M185,100 L22,100 L22,367 L50,367" marker-end="url(#nm-hb)"/><text class="nm-wlab" x="28" y="300" text-anchor="start">x</text><path class="nm-wire" d="M185,162 L185,192" marker-end="url(#nm-hb)"/><text class="nm-wlab" x="191" y="182" text-anchor="start">top</text><path class="nm-wire" d="M185,238 L185,268" marker-end="url(#nm-hb)"/><text class="nm-wlab" x="191" y="258" text-anchor="start">cand</text><path class="nm-wire" d="M185,314 L185,344" marker-end="url(#nm-hb)"/><text class="nm-wlab" x="191" y="334" text-anchor="start">idx</text><path class="nm-wire" d="M320,291 L396,291" marker-end="url(#nm-hb)"/><text class="nm-wlab" x="394" y="284" text-anchor="end">valid</text><path class="nm-wire" d="M185,390 L185,420" marker-end="url(#nm-hb)"/><text class="nm-wlab" x="191" y="414" text-anchor="start">new_size</text><circle class="nm-dot" cx="185" cy="22" r="3"/><circle class="nm-dot" cx="350" cy="215" r="3"/><circle class="nm-dot" cx="185" cy="100" r="3"/></svg>

    <!-- /gen -->

    ```systemverilog title="module nim_move_hw" linenums="1" hl_lines="13 15 16 19 20"
    // nim_move without a clock: N heaps of W bits (N >= 2); valid = 0 when the player to
    // move loses, otherwise heap idx goes down to new_size
    module nim_move_hw #(parameter int N = 3, parameter int W = 3) (
      input  logic [N-1:0][W-1:0]  heap,
      output logic                 valid,
      output logic [$clog2(N)-1:0] idx,
      output logic [W-1:0]         new_size
    );
      logic [W-1:0] x, top;
      logic [N-1:0] cand;
      always_comb begin
        x = '0;
        for (int i = 0; i < N; i++) x ^= heap[i];                  // (1)!
        top = '0;
        for (int b = 0; b < W; b++) if (x[b]) top = W'(1) << b;    // (2)!
        for (int i = 0; i < N; i++) cand[i] = |(heap[i] & top);    // (3)!
        valid = |cand;
        idx = '0;
        for (int i = N - 1; i >= 0; i--) if (cand[i]) idx = i;     // (4)!
        new_size = heap[idx] ^ x;                                  // (5)!
      end
    endmodule
    ```

    1. עץ XOR : הסינתזה בונה מהלולאה \( \lceil \log_2 n \rceil \) רמות של שערים לכל ביט.
    2. גלאי האחד המוביל : הביט הדלוק האחרון בלולאה הוא הגבוה, ו-`top` דלוק רק בו.
    3. המועמדות, הערימות שיש להן את הביט הגבוה של \( x \). ‏`valid` הוא OR שלהן, והוא 1
       בדיוק כש-\( x \ne 0 \).
    4. מקודד עדיפות : המועמדת הראשונה, כמו בלולאה של הפונקציה.
    5. מרבב שבוחר את `heap[idx]`, ו-XOR עם \( x \) : התנאי \( h \oplus x < h \) של הפונקציה
       כבר מובטח, כי למועמדת יש את הביט הגבוה.

    **האימות.** ה-assertions הן שני הכיוונים של ההוכחה שלמטה : כש-`valid` דולק, המהלך חוקי
    וה-XOR אחריו 0, וכש-`valid` כבוי, ה-XOR כבר 0. הכיסוי סופר מצבים מפסידים ואת מספר
    הערימות המועמדות :

    ```systemverilog title="module nim_move_check" linenums="1" hl_lines="16 18 19 20 21 23"
    // the checks of nim_move_hw, sampled on a clock of the testbench: a move is legal and
    // leaves XOR 0, and valid = 0 only on XOR 0; covered: a lost position, k candidates
    module nim_move_check #(parameter int N = 3, parameter int W = 3) (
      input logic                 clk,
      input logic [N-1:0][W-1:0]  heap,
      input logic                 valid,
      input logic [$clog2(N)-1:0] idx,
      input logic [W-1:0]         new_size
    );
      logic [W-1:0] x;
      int ncand, fails = 0, lost = 0, hits[N + 1];
      always_comb begin
        x = '0;
        for (int i = 0; i < N; i++) x ^= heap[i];
        ncand = 0;
        for (int i = 0; i < N; i++) if ((heap[i] ^ x) < heap[i]) ncand++;    // (1)!
      end
      a_move: assert property (@(posedge clk) valid |-> idx < N && new_size < heap[idx] &&
                                              (x ^ heap[idx] ^ new_size) == 0) else fails++;
      a_lost: assert property (@(posedge clk) !valid |-> x == 0) else fails++;
      c_lost: cover property (@(posedge clk) x == 0) lost++;
      for (genvar k = 1; k <= N; k += 2) begin : g_cand                 // (2)!
        c_cand: cover property (@(posedge clk) ncand == k) hits[k]++;
      end
    endmodule
    ```

    1. מספר המהלכים המנצחים לפי התנאי של הפונקציה, ולא לפי המימוש שנבדק.
    2. בעמודה של הביט הגבוה של \( x \) יש מספר אי-זוגי של אחדות, ולכן רק מספר אי-זוגי של
       מועמדות אפשרי : בשלוש ערימות, 1 או 3.

    הטסט של השאלה מריץ את שניהם ב-Verilator על כל 512 המצבים של שלוש ערימות של 3 ביטים, מצב
    בכל מחזור, ומשווה לפתרון בכוח של המשחק. אף assertion לא נופלת, הכיסוי רואה את 64 המצבים
    המפסידים ואת שני הסוגים של מועמדות, ועותק עם באג, שבו מועמדת היא כל ערימה עם ביט משותף
    ל-\( x \), מפיל את `a_move`. ברוחב גדול יותר עוברים על מצבים אקראיים עד שהכיסוי מלא, או
    מוכיחים ב-formal מול `nim_move`.

    #### למה זה נכון { .sol-proof }

    נקרא \( P \) לקבוצת המצבים שה-XOR שלהם 0. מספיקות שלוש תכונות :

    1. **הסוף ב-P :** השולחן הריק הוא XOR של אפסים, ומי שתורו בו הפסיד.
    2. **מ-P יוצאים :** מהלך משנה ערימה אחת מ-\( h \) ל-\( h' \ne h \), ולכן ה-XOR החדש הוא
       \( 0 \oplus h \oplus h' \ne 0 \). כל מהלך ממצב ב-\( P \) מוביל למצב מחוץ ל-\( P \).
    3. **ל-P חוזרים :** אם \( x \ne 0 \), נסמן ב-\( k \) את הביט הגבוה שלו. יש ערימה \( h \) עם
       ביט \( k \) דלוק, כי ה-XOR בעמודה \( k \) הוא 1. ב-\( h \oplus x \) הביט \( k \) כבוי,
       והביטים שמעליו שווים לאלה של \( h \), ולכן \( h \oplus x < h \) : זה מהלך חוקי, וה-XOR
       אחריו הוא 0.

    מי שמשאיר ליריב מצב ב-\( P \) ממשיך לעשות זאת בכל תור, לפי תכונה 3, והיריב לא יכול לברוח,
    לפי תכונה 2. בכל תור יורד לפחות אסימון אחד, ולכן המשחק נגמר, והשולחן הריק מגיע ליריב.
    באינדוקציה על מספר האסימונים : מצב מפסיד בדיוק כשהוא ב-\( P \).

    **כמה מהלכים מנצחים יש?** בדיוק כמספר הערימות שיש להן את הביט הגבוה של \( x \), כי רק בהן
    \( h \oplus x < h \). ב-3, 4, 5 יש אחת כזו. בטבלה עוד מצבים, וב-5, 6, 7, 8 המהלך היחיד הוא
    דווקא מהערימה הגדולה :

    <!-- gen 4 -->

    | הערימות | ‏XOR | מי שתורו | המהלכים המנצחים |
    |:-:|:-:|:-:|:-:|
    | <span dir="ltr">(3, 4, 5)</span> | <span dir="ltr">2 = 0010</span> | מנצח | <span dir="ltr">3 → 1</span> |
    | <span dir="ltr">(1, 2, 3)</span> | <span dir="ltr">0 = 0000</span> | מפסיד | אין |
    | <span dir="ltr">(1, 1, 2)</span> | <span dir="ltr">2 = 0010</span> | מנצח | <span dir="ltr">2 → 0</span> |
    | <span dir="ltr">(2, 5, 6)</span> | <span dir="ltr">1 = 0001</span> | מנצח | <span dir="ltr">5 → 4</span> |
    | <span dir="ltr">(7, 9, 12)</span> | <span dir="ltr">2 = 0010</span> | מנצח | <span dir="ltr">7 → 5</span> |
    | <span dir="ltr">(5, 6, 7, 8)</span> | <span dir="ltr">12 = 1100</span> | מנצח | <span dir="ltr">8 → 4</span> |

    <!-- /gen -->

    **נסו בעצמכם.** משחקים נגד המחשב, שעונה תמיד במהלך המנצח כשיש כזה. קחו 3 מהערימה של 5
    (<span dir="ltr">5 → 2</span>) : המחשב עונה <span dir="ltr">4 → 1</span>, משאיר 3, 1, 2,
    ושורת ה-XOR חוזרת ל-000. בטלו ושחקו <span dir="ltr">3 → 1</span> : עכשיו אתם אלה שמשאירים
    000 אחרי כל תור. הקלידו 1, 2, 3 : אין לכם מהלך מנצח, אבל אם המחשב מתחיל הוא לוקח אסימון
    אחד מהערימה הגדולה, ואתם מנצחים. ובשביל שאלת ההמשך הראשונה, הקלידו 3, 5, 6, 7 וספרו את
    הערימות המסומנות בעמודה של הביט 4. מעבר לטבלאות, הלוח מראה את תשובות המחשב ואת ה-XOR
    אחרי כל מהלך, ומאפשר לבטל מהלך :

    <div class="explorer" data-kind="nim" data-heaps="3,4,5" data-rule="normal"></div>

    #### סיבוכיות { .sol-cost }

    מעבר אחד לחישוב ה-XOR ומעבר אחד למציאת הערימה : \( O(n) \) ל-\( n \) ערימות, וזיכרון קבוע.
    בלי הכלל, חיפוש על כל המצבים עולה \( \prod (h_i + 1) \) מצבים.

---

### סעיף ב – האחרון שלוקח מפסיד

אותו משחק, אבל מי שלוקח את האסימון האחרון מפסיד. מה משתנה?

??? tip "רמז 1"
    באמצע המשחק, כשיש עוד כמה ערימות גדולות, האם מישהו בכלל שם לב לחוק החדש?

??? tip "רמז 2"
    חשבו על הסוף, כשכל הערימות הן 1. מי מנצח עם שלוש ערימות של 1, ומי עם שתיים? ומה צריך
    לקרות במהלך שמשאיר רק ערימות של 1?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        משחקים בדיוק כמו בסעיף א, עד המהלך שמשאיר רק ערימות של 0 ו-1. במהלך הזה משאירים מספר
        אי-זוגי של ערימות של 1, ולא זוגי. מי שתורו מפסיד בדיוק כשיש ערימה גדולה מ-1 וה-XOR
        הוא 0, או כשכל הערימות 0 או 1 ומספר הערימות של 1 אי-זוגי. ב-3, 4, 5 המהלך המנצח לא
        משתנה : לוקחים 2 מהערימה של 3.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **הסוף הפוך.** כשכל הערימות הן 1, כל מהלך לוקח ערימה שלמה, והשחקנים פשוט מתחלפים. עם
    מספר אי-זוגי של ערימות, מי שתורו לוקח את האחרונה ומפסיד. זה ההפך מסעיף א, ששם מספר
    אי-זוגי של ערימות של 1 הוא XOR של 1, מצב מנצח.

    **האמצע זהה.** כל עוד יש לפחות שתי ערימות גדולות מ-1, מהלך אחד לא יכול להשאיר רק ערימות
    של 1, והמשחק נראה בדיוק כמו בסעיף א. ההבדל מופיע רק ברגע שנשארת ערימה אחת גדולה מ-1 : מי
    שתורו מקטין אותה ל-0 או ל-1, לפי מה שמשאיר מספר אי-זוגי של ערימות של 1. בסוף של 1, 1, 4
    המהלך של סעיף א מפסיד :

    <!-- gen 5 -->

    | המהלך מ-<span dir="ltr">(1, 1, 4)</span> | המצב שנשאר | ‏XOR | כשהאחרון מנצח | כשהאחרון מפסיד |
    |:-:|:-:|:-:|:-:|:-:|
    | הורדה ל-0, כמו ב-Nim רגיל : <span dir="ltr">4 → 0</span> | <span dir="ltr">(1, 1, 0)</span> | ‏0 | היריב מפסיד | היריב מנצח |
    | הורדה ל-1 : <span dir="ltr">4 → 1</span> | <span dir="ltr">(1, 1, 1)</span> | ‏1 | היריב מנצח | היריב מפסיד |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ערימות גדולות :** סופרים כמה ערימות גדולות מ-1, וכמה ערימות של 1.
    2. **שתיים או יותר :** משחקים את המהלך של סעיף א, שמאפס את ה-XOR. אם ה-XOR כבר 0, אין
       מהלך מנצח.
    3. **אחת בדיוק :** מקטינים אותה ל-1 אם מספר הערימות של 1 זוגי, ול-0 אם הוא אי-זוגי. כך
       נשאר מספר אי-זוגי של ערימות של 1, ותמיד יש מהלך מנצח.
    4. **אף אחת :** לוקחים ערימה של 1. המצב מנצח בדיוק כשמספר הערימות של 1 זוגי וגדול מ-0.

    </div>

    #### הקוד { .sol-code }

    הפונקציה משתמשת ב-`nim_move` של סעיף א, ומקבלת מצב עם אסימון אחד לפחות.

    === "Python"
        ```python title="misere_move" linenums="1" hl_lines="6 7 9 10"
        def misere_move(heaps: list[int]):
            """Misère Nim (the last to take loses), at least one token on the table: a winning
            move (heap index, new size), or None when the player to move loses."""
            big = [i for i, h in enumerate(heaps) if h > 1]
            ones = sum(1 for h in heaps if h == 1)
            if len(big) == 1:                             # (1)!
                return big[0], 1 if ones % 2 == 0 else 0
            if not big:                                   # (2)!
                return (heaps.index(1), 0) if ones % 2 == 0 else None
            return nim_move(heaps)                        # (3)!
        ```

        1. הערימה הגדולה האחרונה : משאירים ממנה 0 או 1, כך שמספר הערימות של 1 יהיה אי-זוגי.
        2. רק ערימות של 0 ו-1 : מי שתורו מנצח כשמספר הערימות של 1 זוגי.
        3. שתי ערימות גדולות או יותר : בדיוק כמו בסעיף א.

    === "SystemVerilog"
        ```systemverilog title="misere_move" linenums="1" hl_lines="10 11 12 15 16 21"
        // misère Nim (the last to take loses), at least one token on the table: a winning
        // move, heap idx down to new_size; returns 0 when the player to move loses
        function automatic bit misere_move(int heaps[$], output int idx, output int new_size);
          int big, last_big, ones, first_one;
          big = 0; ones = 0; first_one = -1; last_big = -1;
          foreach (heaps[i]) begin
            if (heaps[i] > 1) begin big++; last_big = i; end
            if (heaps[i] == 1) begin ones++; if (first_one < 0) first_one = i; end
          end
          if (big == 1) begin                        // (1)!
            idx = last_big;
            new_size = (ones % 2 == 0) ? 1 : 0;
            return 1;
          end
          if (big == 0) begin                        // (2)!
            if (ones % 2 == 1) return 0;
            idx = first_one;
            new_size = 0;
            return 1;
          end
          return nim_move(heaps, idx, new_size);     // (3)!
        endfunction
        ```

        1. הערימה הגדולה האחרונה : משאירים 0 או 1, כך שיישאר מספר אי-זוגי של ערימות של 1.
        2. רק ערימות של 0 ו-1 : מספר אי-זוגי של ערימות של 1 הוא מצב מפסיד.
        3. שתי ערימות גדולות או יותר : המהלך של סעיף א.

    #### למה זה נכון { .sol-proof }

    נקרא \( L \) לקבוצת המצבים משני הסוגים : (א) יש ערימה גדולה מ-1 וה-XOR הוא 0; (ב) כל
    הערימות 0 או 1, ומספר הערימות של 1 אי-זוגי. השולחן הריק אינו ב-\( L \) : מי שתורו בו
    ניצח, כי היריב לקח את האחרון. ושוב מספיק להראות שתי תכונות.

    **מ-L יוצאים.** ממצב מסוג (ב), כל מהלך לוקח ערימה של 1, ומשאיר מספר זוגי שלהן : מחוץ
    ל-\( L \). ממצב מסוג (א), כל מהלך הופך את ה-XOR ללא-0, כמו בסעיף א. אם נשארה ערימה גדולה
    מ-1, המצב מחוץ ל-\( L \). ואם לא נשארה, אז לפני המהלך הייתה ערימה גדולה אחת בדיוק, אבל
    אז ה-XOR לא היה יכול להיות 0 : לערימה הזו יש ביט של 2 או יותר, ולאף ערימה אחרת אין.

    **ל-L חוזרים.** עם שתי ערימות גדולות או יותר וה-XOR לא 0, המהלך של סעיף א מאפס את
    ה-XOR, ומשנה ערימה אחת בלבד, ולכן נשארת ערימה גדולה : סוג (א). עם ערימה גדולה אחת,
    מקטינים אותה ל-0 או ל-1 ומקבלים סוג (ב). ובלי ערימות גדולות, עם מספר זוגי של ערימות של
    1, לוקחים אחת : סוג (ב).

    המשחק נגמר, ולכן מי שתמיד מחזיר את היריב ל-\( L \) מנצח : היריב לא מגיע לשולחן הריק
    בתורו, אלא לוקח את האסימון האחרון בעצמו.

    **נסו בעצמכם.** אותו משחק, עם החוק ההפוך. הקלידו 1, 1, 4 ושחקו <span dir="ltr">4 → 0</span>,
    כמו ב-Nim רגיל : המחשב לוקח ערימה של 1, ואתם נאלצים לקחת את האחרון. בטלו ושחקו
    <span dir="ltr">4 → 1</span> : עכשיו המחשב הוא שנאלץ. בערימות של העמוד, 1, 1, 4, 6, ה-XOR הוא
    2 ומי שמתחיל מנצח. מעבר לטבלה של \( (1, 1, 4) \), הלוח מסביר את הרגע שבו נשארת ערימה אחת
    גדולה מ-1, ומקווקו את שורת ה-XOR כשכל הערימות 0 או 1, כי שם היא כבר לא קובעת :

    <div class="explorer" data-kind="nim" data-heaps="1,1,4,6" data-rule="misere"></div>

    #### סיבוכיות { .sol-cost }

    מעבר אחד לספירה, ובמקרה הכללי המהלך של סעיף א : \( O(n) \) זמן וזיכרון קבוע.

---

### סעיף ג – לוקחים רק 1, 3 או 4

חוזרים לחוק של סעיף א, אבל מכל ערימה מותר לקחת רק 1, 3 או 4 אסימונים. מי מנצח ב-3, 4, 5,
ואיך מחשבים כל מצב?

??? tip "רמז 1"
    התחילו מערימה אחת. מערימה של \( n \) אפשר לעבור ל-\( n - 1 \), ‏\( n - 3 \) ו-\( n - 4 \).
    אילו גדלים מפסידים?

??? tip "רמז 2"
    ערימה כאן היא לא ערימת Nim רגילה, אבל אולי היא מתנהגת בדיוק כמו ערימת Nim בגודל אחר.
    באיזה גודל?

??? tip "רמז 3"
    ערימת Nim בגודל \( v \) יכולה לעבור לכל גודל קטן מ-\( v \), ולא ל-\( v \) עצמו. תנו לכל
    \( n \) ערך \( v \), כך שמ-\( n \) אפשר להגיע למצבים עם כל ערך קטן מ-\( v \), ולא למצב עם
    \( v \) עצמו.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        לכל גודל \( n \) מחשבים את מספר גרנדי \( g(n) \) : הערך הקטן ביותר שאינו בין מספרי
        גרנדי של המצבים שאפשר לעבור אליהם (mex). עבור 1, 3, 4 יוצא 0, 1, 0, 1, 2, 3, 2, שחוזר
        במחזור 7. ערימה של \( n \) מתנהגת כמו ערימת Nim בגודל \( g(n) \), ולכן מי שתורו מפסיד
        בדיוק כשה-XOR של מספרי גרנדי הוא 0. ב-3, 4, 5 : \( 1 \oplus 2 \oplus 3 = 0 \), ולכן
        הפעם מי שמתחיל מפסיד, אף ש-\( 3 \oplus 4 \oplus 5 = 2 \).

    <!-- cost: טבלה \( O(H \cdot |S|) \) | מהלך \( O(n \cdot |S|) \) | זיכרון \( O(H) \) -->

    #### הרעיון { .sol-idea }

    **ה-mex.** נגדיר \( g(0) = 0 \), ולכל \( n \) :

    \[
    g(n) = \operatorname{mex} \{\, g(n - m) \mid m \in \{1, 3, 4\},\ m \le n \,\}
    \]

    כש-mex של קבוצה הוא המספר הטבעי הקטן ביותר שאינו בה. מהגדרה, מערימה עם \( g(n) = v \)
    אפשר לעבור למצבים עם כל ערך קטן מ-\( v \), ואי אפשר לעבור למצב עם \( v \) עצמו, בדיוק כמו
    בערימת Nim בגודל \( v \). לפעמים אפשר לעבור גם לערך גדול מ-\( v \). זה לא מציל מצב מפסיד
    (תכונה 2 בהוכחה), אבל לפעמים זה מהלך מנצח בעצמו : ב-5, 6, 7 גם <span dir="ltr">6 → 5</span>,
    מ-\( g = 2 \) ל-\( g = 3 \), מנצח.

    **החישוב.** \( g(1) = \operatorname{mex}\{0\} = 1 \), ‏\( g(2) = \operatorname{mex}\{1\} = 0 \),
    ‏\( g(3) = \operatorname{mex}\{0, 0\} = 1 \), ‏\( g(4) = \operatorname{mex}\{1, 1, 0\} = 2 \),
    ‏\( g(5) = \operatorname{mex}\{2, 0, 1\} = 3 \), ‏\( g(6) = \operatorname{mex}\{3, 1, 0\} = 2 \),
    ו-\( g(7) = \operatorname{mex}\{2, 2, 1\} = 0 \). כל ערך תלוי רק בארבעת הערכים שלפניו,
    וארבעת הערכים ב-7 עד 10 שווים לאלה ב-0 עד 3. לכן מכאן הסדרה חוזרת על עצמה, במחזור 7 :

    <!-- gen 6 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="סעיף ג : מספרי גרנדי של המשחק שבו לוקחים 1, 3 או 4, מ-n = 0 עד 13 : 0, 1, 0, 1, 2, 3, 2 ושוב 0, 1, 0, 1, 2, 3, 2. ארבעת הערכים ב-7 עד 10 שווים לאלה ב-0 עד 3, ולכן הסדרה מחזורית במחזור 7"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td><td>11</td><td>12</td><td>13</td></tr><tr><th dir="rtl">‏g(n)</th><td class="pm-c c1">0</td><td class="pm-c c1">1</td><td class="pm-c c1">0</td><td class="pm-c c1">1</td><td class="pm-c c1">2</td><td class="pm-c c1">3</td><td class="pm-c c1">2</td><td class="pm-c c4 is-hl">0</td><td class="pm-c c4 is-hl">1</td><td class="pm-c c4 is-hl">0</td><td class="pm-c c4 is-hl">1</td><td class="pm-c c4">2</td><td class="pm-c c4">3</td><td class="pm-c c4">2</td></tr></tbody></table></div>

    <!-- /gen -->

    <!-- gen 7 -->

    <span class="viz-legend"><span><i class="pm-key-c1"></i>המחזור הראשון, n = 0 עד 6</span><span><i class="pm-key-c4"></i>המחזור השני, n = 7 עד 13</span><span><i class="pm-key-hl"></i>ארבעה ערכים שחוזרים : מכאן הסדרה חוזרת</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הטבלה :** מחשבים \( g(0), g(1), \dots \) עד הערימה הגדולה, לפי ה-mex.
    2. **ה-XOR :** \( x = g(h_1) \oplus g(h_2) \oplus \dots \oplus g(h_n) \).
    3. **‏x = 0 :** מי שתורו מפסיד.
    4. **המהלך :** אחרת, כמו בסעיף א, בוחרים ערימה \( h \) עם הביט הגבוה של \( x \), והיעד הוא
       \( t = g(h) \oplus x < g(h) \). מבין \( h - 1 \), ‏\( h - 3 \) ו-\( h - 4 \) יש אחד עם
       \( g = t \), לפי ההגדרה של mex.

    </div>

    הטבלה משווה את ה-XOR של מספרי גרנדי ל-XOR של הגדלים, עם כל המהלכים המנצחים. ב-5, 6, 7
    וב-10, 11, 6 יש שלושה, וחלקם מעלים את \( g \) של הערימה :

    <!-- gen 8 -->

    | הערימות | מספרי גרנדי | ‏XOR של גרנדי | מי שתורו | המהלכים המנצחים | ‏XOR של הגדלים |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | <span dir="ltr">(3, 4, 5)</span> | <span dir="ltr">1, 2, 3</span> | ‏0 | מפסיד | אין | ‏2 |
    | <span dir="ltr">(5, 6, 7)</span> | <span dir="ltr">3, 2, 0</span> | ‏1 | מנצח | <span dir="ltr">5 → 4; 6 → 5; 7 → 3</span> | ‏4 |
    | <span dir="ltr">(10, 11, 6)</span> | <span dir="ltr">1, 2, 2</span> | ‏1 | מנצח | <span dir="ltr">10 → 9; 10 → 7; 6 → 5</span> | ‏7 |
    | <span dir="ltr">(2, 9, 16)</span> | <span dir="ltr">0, 0, 0</span> | ‏0 | מפסיד | אין | ‏27 |

    <!-- /gen -->

    #### הקוד { .sol-code }

    הפונקציה `subtraction_move` משתמשת בכלל של סעיף א, על מספרי גרנדי במקום על הגדלים.

    === "Python"
        ```python title="grundy, subtraction_move" linenums="1" hl_lines="5 6 14 19"
        def grundy(n: int, moves=(1, 3, 4)) -> list[int]:
            """The Grundy numbers g[0..n] of one heap when a move takes one of `moves`."""
            g = [0] * (n + 1)
            for k in range(1, n + 1):
                seen = {g[k - m] for m in moves if m <= k}
                g[k] = min(set(range(len(seen) + 1)) - seen)   # (1)!
            return g


        def subtraction_move(heaps: list[int], moves=(1, 3, 4)):
            """A winning move (heap index, new size) when a move takes one of `moves` from a
            heap, or None when the player to move loses."""
            g = grundy(max(heaps), moves)
            x = reduce(xor, (g[h] for h in heaps), 0)               # (2)!
            if x == 0:
                return None
            for i, h in enumerate(heaps):
                for m in moves:
                    if m <= h and g[h - m] == g[h] ^ x:             # (3)!
                        return i, h - m
            return None
        ```

        1. ה-mex : הערך הקטן ביותר שאינו ב-`seen`. הוא לכל היותר `len(seen)`.
        2. ה-XOR של מספרי גרנדי, ולא של הגדלים.
        3. מעבירים ערימה אחת לערך \( g(h) \oplus x \), כמו ב-\( h \oplus x \) של סעיף א. בודקים כל
           ערימה וכל מהלך, ולכן גם מהלך שמעלה את \( g \), כמו <span dir="ltr">6 → 5</span> ב-5, 6, 7,
           נמצא.

    === "SystemVerilog"
        ```systemverilog title="grundy_table, grundy, subtraction_move" linenums="1" hl_lines="7 8 25 26 30"
        // the Grundy numbers g[0..n] of one heap when a move takes one of `moves`
        function automatic void grundy_table(int n, int moves[$], output int g[]);
          bit seen[];
          g = new[n + 1];                               // all 0
          for (int k = 1; k <= n; k++) begin
            seen = new[moves.size() + 1];               // (1)!
            foreach (moves[j]) if (moves[j] <= k) seen[g[k - moves[j]]] = 1;
            while (seen[g[k]]) g[k]++;                  // (2)!
          end
        endfunction

        // the Grundy number of a heap of n tokens
        function automatic int grundy(int n, int moves[$]);
          int g[];
          grundy_table(n, moves, g);
          return g[n];
        endfunction

        // a winning move, heap idx down to new_size, when a move takes one of `moves` from a
        // heap; returns 0 when the player to move loses
        function automatic bit subtraction_move(int heaps[$], int moves[$], output int idx, output int new_size);
          int g[], hmax, x;
          hmax = 0; x = 0;
          foreach (heaps[i]) if (heaps[i] > hmax) hmax = heaps[i];
          grundy_table(hmax, moves, g);                 // (3)!
          foreach (heaps[i]) x ^= g[heaps[i]];          // (4)!
          if (x == 0) return 0;
          foreach (heaps[i])
            foreach (moves[j])
              if (moves[j] <= heaps[i] && g[heaps[i] - moves[j]] == (g[heaps[i]] ^ x)) begin   // (5)!
                idx = i;
                new_size = heaps[i] - moves[j];
                return 1;
              end
          return 0;
        endfunction
        ```

        1. ה-mex של \( |S| \) ערכים הוא לכל היותר \( |S| \), ולכן מספיק מערך של \( |S| + 1 \).
        2. ה-mex : מתחילים מ-0 ועולים עד הערך הראשון שלא נראה.
        3. הטבלה נבנית פעם אחת, עד הערימה הגדולה : \( O(H \cdot |S|) \).
        4. ה-XOR של מספרי גרנדי. בחומרה, לגדלים קטנים, ‏\( g \) הוא טבלה קבועה, או \( n \bmod 7 \)
           וטבלה של 7 ערכים.
        5. כל ערימה וכל מהלך, כמו בפייתון : \( O(n \cdot |S|) \) קריאות מהטבלה.

    #### למה זה נכון { .sol-proof }

    נקרא \( x \) ל-XOR של מספרי גרנדי. הטענה : מצב מפסיד בדיוק כש-\( x = 0 \). שלוש התכונות
    של סעיף א :

    1. **הסוף :** השולחן הריק, כל הערימות 0, ו-\( g(0) = 0 \), ולכן \( x = 0 \).
    2. **מ-x = 0 יוצאים :** מהלך משנה ערימה אחת מ-\( h \) ל-\( h' \), ו-\( g(h') \ne g(h) \),
       כי \( g(h) \) הוא בדיוק ערך שאי אפשר לעבור אליו. לכן \( x \) משתנה לערך שאינו 0. זה
       נכון גם כש-\( g(h') > g(h) \), למשל מ-7, שה-\( g \) שלו 0, עוברים ל-6, שה-\( g \) שלו 2.
    3. **ל-x = 0 חוזרים :** אם \( x \ne 0 \), בוחרים \( h \) עם הביט הגבוה של \( x \), והיעד
       \( t = g(h) \oplus x \) קטן מ-\( g(h) \). כל ערך קטן מ-\( g(h) \) ניתן להשגה, אחרת ה-mex
       היה קטן יותר, ולכן יש מהלך מ-\( h \) ל-\( h' \) עם \( g(h') = t \), ואחריו \( x = 0 \).

    ושוב, המשחק נגמר, ולכן מי שתורו ב-\( x = 0 \) מפסיד.

    **המשפט הכללי.** אותה הוכחה עובדת לכל משחק "הוגן", שבו לשני השחקנים אותם מהלכים, המשחק
    תמיד נגמר, ומי שלא יכול לזוז מפסיד. לכל מצב יש מספר גרנדי, ה-mex של המצבים שאפשר להגיע
    אליהם, והוא מתנהג בדיוק כמו ערימת Nim בגודל הזה. וסכום של משחקים, שבו בכל תור משחקים
    באחד מהם, מתנהג כמו ה-XOR של המספרים. זה משפט ספרג–גרנדי, ו-Nim הוא המקרה שבו
    \( g(n) = n \).

    **נסו בעצמכם.** אותו משחק, עם 1, 3 או 4 בלבד, ומתחת ללוח מספרי גרנדי של הערימות בבינארי.
    ב-5, 6, 7 קחו 1 מהערימה של 6 : ה-\( g \) שלה עולה מ-2 ל-3, ובכל זאת ה-XOR יורד ל-0 והמחשב
    מפסיד. הקלידו 7 לבד : כל שלושת המהלכים שלכם, ל-6, ל-4 ול-3, משאירים למחשב מצב מנצח. וב-3,
    4, 5 תנו למחשב להתחיל : הוא מפסיד, אף שה-XOR של הגדלים 2. מעבר לטבלה, ‏"הצגת המהלך המנצח"
    מונה את כל המהלכים המנצחים, גם את אלה שמעלים את \( g \) :

    <div class="explorer" data-kind="nim" data-heaps="5,6,7" data-rule="sub"></div>

    #### סיבוכיות { .sol-cost }

    הטבלה עד הערימה הגדולה \( H \) עולה \( O(H \cdot |S|) \) זמן ו-\( O(H) \) זיכרון. אחריה, מהלך
    הוא \( O(n \cdot |S|) \). כאן, בזכות המחזור, \( g(n) = g(n \bmod 7) \) והטבלה קבועה בגודלה.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : הסכום או הזוגיות במקום XOR"
    ‏"סכום זוגי מפסיד" נשמע סביר, אבל ב-1, 1, 2 הסכום 4 ומי שתורו מנצח : לוקח את ה-2 ומשאיר
    1, 1. וב-1, 2, 3 הסכום 6 והוא מפסיד. מה שקובע הוא הזוגיות של כל עמודת ביטים לחוד, וזה
    בדיוק ה-XOR.

??? trap "מלכודת : לוקחים מהערימה הגדולה"
    ב-3, 4, 5 המהלך המנצח היחיד הוא מהערימה הקטנה : \( 5 \oplus 2 = 7 \) ו-\( 4 \oplus 2 = 6 \),
    שניהם גדולים מהערימה, ולכן אי אפשר להגיע אליהם. רק ערימה שיש לה את הביט הגבוה של ה-XOR
    מתאימה, ולפעמים זו הקטנה.

??? trap "מלכודת : במשחק ההפוך משחקים כרגיל עד הסוף"
    ב-1, 1, 4, כשהאחרון מפסיד, המהלך של סעיף א מוריד את 4 ל-0 ומשאיר 1, 1. היריב לוקח אחד,
    ואתם נאלצים לקחת את האחרון ומפסידים. המהלך הנכון מוריד את 4 ל-1, ומשאיר שלוש ערימות של 1.

??? trap "מלכודת : XOR של הגדלים בסעיף ג"
    ב-3, 4, 5 עם 1, 3 או 4 בלבד, ה-XOR של הגדלים הוא 2 והוא "אומר" שמי שמתחיל מנצח. אבל
    מספרי גרנדי הם 1, 2, 3, ה-XOR שלהם 0, ומי שמתחיל מפסיד. הגדלים נכונים בכל מצב רק כשמותר
    לקחת כל כמות, כי אז \( g(n) = n \).

??? trap "מלכודת : המקסימום במקום ה-mex"
    ‏\( g(7) = \operatorname{mex}\{2, 2, 1\} = 0 \), אבל "המקסימום ועוד 1" נותן 3. ערימה של 7 היא
    מצב מפסיד : כל המהלכים ממנה, ל-6, ל-4 ול-3, מובילים למצבים מנצחים. עם המקסימום, כל
    הערכים רק עולים, ושום ערימה גדולה לא נראית מפסידה.

??? followup "שאלות המשך"
    - **כמה מהלכים מנצחים?** ב-3, 5, 6, 7 של Nim רגיל, כמה מהלכים מנצחים יש?

        ??? fu-answer "תשובה"
            ה-XOR הוא 7, והביט הגבוה שלו 4. לשלוש ערימות יש אותו, 5, 6 ו-7, ולכן יש שלושה
            מהלכים מנצחים : <span dir="ltr">5 → 2</span>, <span dir="ltr">6 → 1</span>
            ו-<span dir="ltr">7 → 0</span>. ל-3 אין את הביט, ו-\( 3 \oplus 7 = 4 > 3 \).

    - **ערימה אחת, לוקחים 1 עד k :** מתי מי שתורו מפסיד?

        ??? fu-answer "תשובה"
            בדיוק כש-\( n \) מתחלק ב-\( k + 1 \) : מכל מהלך של היריב, \( t \), עונים ב-\( k + 1 - t \).
            מספר גרנדי הוא \( g(n) = n \bmod (k + 1) \), ולכן כמה ערימות כאלה הן XOR של השאריות.

    - **‏Nim על מדרגות :** מטבעות על מדרגות 1 עד \( k \). מהלך מוריד כמה מטבעות שרוצים
      ממדרגה אחת למדרגה שמתחתיה, ומהמדרגה הראשונה הם יורדים לרצפה. מי מנצח?

        ??? fu-answer "תשובה"
            מי שתורו מפסיד בדיוק כשה-XOR של המדרגות האי-זוגיות הוא 0. המדרגות האי-זוגיות הן
            ערימות Nim. אם היריב מוריד מטבעות ממדרגה זוגית לאי-זוגית, מורידים אותם עוד מדרגה,
            וה-XOR חוזר לקדמותו.

    - **‏Nim עם פיצול :** מהלך הוא לקחת מערימה, או לפצל ערימה לשתי ערימות לא ריקות. מה מספרי
      גרנדי?

        ??? fu-answer "תשובה"
            ה-mex כולל גם את \( g(a) \oplus g(n - a) \) של כל פיצול. יוצא 0, 1, 2, 4, 3, 5, 6, 8,
            7, ... : ‏\( g(n) = n \) כש-\( n \bmod 4 \) הוא 1 או 2, ו-3 ו-4 מתחלפים בכל רביעייה :
            \( g(4k + 3) = 4k + 4 \) ו-\( g(4k + 4) = 4k + 3 \).
