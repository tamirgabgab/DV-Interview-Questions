---
id: 58
title: ה-tag שלא חזר – XOR, חלוקה לפי ביט וסכומי חזקות
level: senior
difficulty: hard
kind: dv
tags: [bitwise, methodology, math, systemverilog, python]
source: "שאלת ראיון נפוצה (missing number) בגרסה של בודק לתשובות עם tag"
added: 2026-10-27
---

## השאלה

רכיב DMA שולח בקשות קריאה עם `tag` של \( W \) ביטים. כל בקשה מקבלת תשובה עם אותו tag,
בסדר כלשהו, ואין שתי בקשות פתוחות עם אותו tag. בסוף הטסט כל tag שנשלח צריך לחזור **פעם
אחת בדיוק**. אתם כותבים בודק שיושב על הממשק, ורוצים לדעת מה השתבש **בלי טבלה של ביט לכל
tag** : הבודק רואה כל בקשה וכל תשובה פעם אחת, וזוכר רק כמה רגיסטרים.

- **סעיף א – אחד חסר :** תשובה אחת לא הגיעה. איך מוצאים את ה-tag שלה?
- **סעיף ב – שניים חסרים :** שתי תשובות לא הגיעו. איך מוצאים את שתיהן, ובכמה ביטים?
- **סעיף ג – חסר אחד וכפול אחד :** תשובה אחת לא הגיעה, ותשובה אחרת הגיעה פעמיים. למה
  הבודק של סעיף ב טועה כאן, ומה כן עובד?
- **סעיף ד – k חסרים :** איך מוצאים עד \( k \) תשובות חסרות, ובכמה זיכרון?

??? interviewer "מה המראיין בודק"
    - **מבנה במקום טבלה :** האם המועמד מחפש פעולה שבה כל tag "מבטל" את עצמו, במקום לזכור
      מי חזר.
    - **מה המצבר לא רואה :** האם הוא שואל מה קורה כשהכול תקין, כשחסר tag 0, וכשאותו מספר
      יכול לבוא משני תרחישים שונים.
    - **חומרה :** בכמה ביטים כל מצבר, ומה הבודק יודע רק בסוף ולא בזמן ההרצה.
    - **הכללה :** האם הוא מגיע מ-XOR לסכומים ולחזקות, ומבין מה כל אחד קונה.

---

### סעיף א – אחד חסר

??? tip "רמז 1"
    איזו פעולה מבטלת את עצמה כשמפעילים אותה פעמיים על אותו ערך?

??? tip "רמז 2"
    ‏\( t \oplus t = 0 \). מה יוצא אם עושים XOR לכל tag כשהוא נשלח, וגם כשהוא חוזר?

<div class="selfcheck" data-answer="4" data-show="4" data-hint="XOR של 0 עד 7 הוא 0. עכשיו XOR של התשובות : 3, 0, 6, 1, 7, 2, 5." markdown>
נשלחו ה-tags 0 עד 7, וחזרו 3, 0, 6, 1, 7, 2, 5. איזה tag חסר?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        רגיסטר אחד של \( W \) ביטים : XOR של כל tag כשהוא נשלח וגם כשהוא חוזר. כל tag שחזר
        מתבטל, ובסוף נשאר בדיוק ה-tag החסר. צריך גם מונה של בקשות פתוחות, כי 0 ברגיסטר
        יכול להיות "הכול חזר" או "חסר tag 0".

    <!-- cost: זיכרון \( W + \log_2 n \) ביטים | עדכון \( O(1) \) לכל תשובה -->

    #### הרעיון { .sol-idea }

    ‏XOR הוא חיבור בלי נשא : הוא חילופי (הסדר לא משנה), ו-\( t \oplus t = 0 \). לכן אם
    עושים XOR לכל tag פעמיים, פעם בשליחה ופעם בחזרה, כל הזוגות מתבטלים, והתשובות יכולות
    לחזור בכל סדר. מה שנשאר ברגיסטר הוא ה-XOR של ה-tags **שעוד בחוץ**. אם בדיוק אחד בחוץ,
    זה הוא. בדוגמה :

    <!-- gen 0 -->

    | הצעד | ה-tag | בבינארי | ה-XOR עד עכשיו |
    |:-:|:-:|:-:|:-:|
    | נשלחו 0 עד 7 | | | ‏`000` = ‏0 |
    | ‏1 | ‏3 | ‏`011` | ‏`011` = ‏3 |
    | ‏2 | ‏0 | ‏`000` | ‏`011` = ‏3 |
    | ‏3 | ‏6 | ‏`110` | ‏`101` = ‏5 |
    | ‏4 | ‏1 | ‏`001` | ‏`100` = ‏4 |
    | ‏5 | ‏7 | ‏`111` | ‏`011` = ‏3 |
    | ‏6 | ‏2 | ‏`010` | ‏`001` = ‏1 |
    | ‏7 | ‏5 | ‏`101` | ‏`100` = ‏4 |

    <!-- /gen -->

    **מונה.** הרגיסטר לבד לא מבדיל בין "כולם חזרו" (0) לבין "חסר tag 0" (גם 0). מונה של
    בקשות פתוחות, \( +1 \) בשליחה ו-\( -1 \) בחזרה, אומר כמה חסרים, ורק אז יודעים איך לקרוא
    את ה-XOR.

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module tag_xor" linenums="1" hl_lines="14 15"
        // the XOR of the tags still out, and how many are out
        module tag_xor #(parameter int W = 8) (
          input  logic         clk, rst_n,
          input  logic         req_valid,
          input  logic [W-1:0] req_tag,
          input  logic         rsp_valid,
          input  logic [W-1:0] rsp_tag,
          output logic [W-1:0] missing,      // the tag, when out == 1
          output int           out
        );
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin missing <= '0; out <= 0; end
            else begin
              missing <= missing ^ (req_valid ? req_tag : '0) ^ (rsp_valid ? rsp_tag : '0);   // (1)!
              out     <= out + int'(req_valid) - int'(rsp_valid);
            end
        endmodule
        ```

        1. בקשה ותשובה באותו מחזור נכנסות שתיהן לאותו עדכון. ‏XOR חילופי, ולכן הסדר לא משנה.

    === "Python"
        ```python title="missing_one" linenums="1" hl_lines="5"
        def missing_one(sent: list[int], returned: list[int]) -> int:
            """One tag never came back: the XOR of every tag sent and every tag returned."""
            acc = 0
            for t in sent + returned:
                acc ^= t                      # (1)!
            return acc
        ```

        1. כל tag שחזר מופיע פעמיים ומתבטל. נשאר רק ה-tag שהופיע פעם אחת.

    #### למה זה נכון { .sol-proof }

    ‏XOR הוא חילופי וקיבוצי, ‏\( t \oplus t = 0 \) ו-\( t \oplus 0 = t \). לכן ה-XOR של כל
    הרצף שווה ל-XOR של ה-tags שמופיעים מספר אי-זוגי של פעמים. tag שחזר מופיע פעמיים, וה-tag
    החסר פעם אחת בלבד.

---

### סעיף ב – שניים חסרים

??? tip "רמז 1"
    עכשיו הרגיסטר מכיל \( x = a \oplus b \). מה אפשר ללמוד ממנו? ‏\( a \ne b \), ולכן יש ביט
    שבו \( x \) דולק. מה זה אומר על \( a \) ו-\( b \) בביט הזה?

??? tip "רמז 2"
    אם ידעתם מראש את הביט \( j \), הייתם עושים XOR נפרד רק ל-tags שהביט \( j \) שלהם 1. אבל
    את \( j \) יודעים רק בסוף. אז מה שומרים בזמן ההרצה?

<div class="selfcheck" data-answer="72" data-show="72 = 8 + 8 · 8" data-hint="רגיסטר x אחד של W ביטים, ועוד רגיסטר part[j] של W ביטים לכל אחד מ-W הביטים." markdown>
כמה ביטים של מצברים (בלי המונה) צריך הבודק של סעיף ב ל-tags של 8 ביטים?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        שומרים את \( x \), ה-XOR של הכול, ולכל ביט \( j \) גם `part[j]`, ה-XOR של ה-tags שהביט
        \( j \) שלהם 1. בסוף בוחרים ביט \( j \) שדולק ב-\( x \). ‏\( a \) ו-\( b \) נבדלים בו,
        ולכן `part[j]` מכיל רק אחד מהם : ‏\( a = \) `part[j]`, ‏\( b = x \oplus a \). סך הכול
        ‏\( W + W^2 \) ביטים, 72 ל-tags של 8 ביטים.

    <!-- cost: זיכרון \( W(W + 1) \) ביטים | עדכון \( O(W) \) לכל תשובה -->

    #### הרעיון { .sol-idea }

    **מה \( x \) אומר.** ‏\( x = a \oplus b \ne 0 \). בכל ביט שדולק ב-\( x \), בדיוק אחד מ-\( a \)
    ו-\( b \) דולק. לכן הביט הזה מחלק את כל ה-tags לשתי קבוצות, ובכל קבוצה יש **חסר אחד
    בדיוק**, וזה סעיף א פעמיים.

    **הבעיה בחומרה.** את הביט \( j \) יודעים רק בסוף, כשכבר אין את ה-tags. לכן שומרים את
    החלוקה **לכל** ביט מראש : ‏`part[j]` מקבל XOR של כל tag שהביט \( j \) שלו 1. בדוגמה נשלחו
    ‏0 עד 15, וחסרים 5 ו-12. ‏\( x = 5 \oplus 12 = 9 = 1001_2 \), והביט הנמוך שדולק בו הוא 0 :

    <!-- gen 1 -->

    | הביט j | ה-tags החסרים שהביט j שלהם 1 | ‏`part[j]` | ‏`x` בביט j |
    |:-:|:-:|:-:|:-:|
    | ‏0 | ‏5 | ‏`0101` = ‏5 | ‏1 |
    | ‏1 | ‏— | ‏`0000` = ‏0 | ‏0 |
    | ‏2 | ‏5, 12 | ‏`1001` = ‏9 | ‏0 |
    | ‏3 | ‏12 | ‏`1100` = ‏12 | ‏1 |

    <!-- /gen -->

    ‏`part[0] = 5`, ולכן החסרים הם 5 ו-\( 9 \oplus 5 = 12 \). גם ביט 3 היה עובד : ‏`part[3] = 12`.
    ביטים 1 ו-2 לא עוזרים, כי שני החסרים שווים בהם (‏`part[2]` הוא ה-XOR של שניהם).

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module tag_xor2" linenums="1" hl_lines="14 15 20 21"
        // two tags missing: the XOR of all, and per bit the XOR of the tags with that bit set
        module tag_xor2 #(parameter int W = 8) (
          input  logic         clk, rst_n,
          input  logic         req_valid,
          input  logic [W-1:0] req_tag,
          input  logic         rsp_valid,
          input  logic [W-1:0] rsp_tag,
          output logic [W-1:0] miss_a, miss_b   // when exactly two are out
        );
          logic [W-1:0] x, part [W];
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin x <= '0; foreach (part[j]) part[j] <= '0; end
            else begin
              x <= x ^ (req_valid ? req_tag : '0) ^ (rsp_valid ? rsp_tag : '0);
              foreach (part[j]) part[j] <= part[j] ^ (req_valid && req_tag[j] ? req_tag : '0)
                                                    ^ (rsp_valid && rsp_tag[j] ? rsp_tag : '0);   // (1)!
            end
          always_comb begin
            miss_a = '0;
            for (int j = W - 1; j >= 0; j--) if (x[j]) miss_a = part[j];   // (2)!
            miss_b = x ^ miss_a;
          end
        endmodule
        ```

        1. החלוקה לכל ביט נשמרת מראש, כי את הביט שיבדיל בין שני החסרים יודעים רק בסוף.
        2. כל ביט דולק ב-\( x \) מתאים. הלולאה יורדת, ולכן הביט הנמוך ביותר קובע.

    === "Python"
        ```python title="missing_two" linenums="1" hl_lines="7 8 9"
        def missing_two(sent: list[int], returned: list[int], width: int) -> list[int]:
            """Two tags never came back: split them by a bit where they differ."""
            x, part = 0, [0] * width
            for t in sent + returned:
                x ^= t
                for j in range(width):
                    if t >> j & 1: part[j] ^= t      # (1)!
            j = (x & -x).bit_length() - 1            # (2)!
            a = part[j]
            return sorted((a, x ^ a))
        ```

        1. ‏`part[j]` : ה-XOR של ה-tags שהביט \( j \) שלהם 1, שליחה וחזרה.
        2. הביט הנמוך ביותר שדולק ב-\( x = a \oplus b \) : שם \( a \) ו-\( b \) שונים.

    #### למה זה נכון { .sol-proof }

    לפי סעיף א, `part[j]` הוא ה-XOR של ה-tags **החסרים** שהביט \( j \) שלהם 1, כי כל השאר
    מתבטלים. אם \( x \) דולק בביט \( j \), אז בדיוק אחד מ-\( a, b \) דולק בו, ולכן `part[j]`
    הוא אותו אחד. השני הוא \( x \oplus a \).

    **בזול יותר.** גם סכום וסכום ריבועים מוצאים שני חסרים : ‏\( a + b \) ו-\( a^2 + b^2 \) נותנים
    משוואה ריבועית. ל-tags של 8 ביטים זה 38 ביטים במקום 72 (הטבלה בסעיף ד), אבל זה כבר
    מחבר וכופל ולא רק XOR.

---

### סעיף ג – חסר אחד וכפול אחד

??? tip "רמז 1"
    נניח שחסר \( a \) ו-\( d \) חזר פעמיים. מה יש ב-\( x \)? ומה אומר המונה?

??? tip "רמז 2"
    ‏XOR מאבד את הסימן : הוא לא יודע אם tag "חסר" או "עודף". סכום יודע. נסו את ההפרש בין
    הסכום של מה שנשלח לסכום של מה שחזר, וגם עם ריבועים.

<div class="selfcheck" data-answer="7" data-show="7 (והכפול 3)" data-hint="‏a − d = 4 ו-a² − d² = 40. חלקו : a + d = 40 / 4 = 10." markdown>
נשלחו 0 עד 9. הסכום של מה שנשלח פחות מה שחזר הוא 4, וההפרש בסכומי הריבועים הוא 40. איזה tag חסר?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏XOR נותן \( a \oplus d \), בדיוק כמו "שניים חסרים", והמונה אומר שאף אחד לא בחוץ. הבודק של
        סעיף ב יכריז בטעות על שני חסרים. במקום זה שומרים \( s = a - d \) ו-\( q = a^2 - d^2 \)
        (שליחה פחות חזרה). אז \( a + d = q / s \), ומכאן \( a \) ו-\( d \).

    <!-- cost: זיכרון כ-\( 5W \) ביטים | עדכון כפל אחד לכל תשובה -->

    #### הרעיון { .sol-idea }

    **למה XOR נכשל.** ‏XOR סופר מופעים מודולו 2 : ה-tag החסר הופיע פעם אחת, והכפול שלוש
    פעמים. שניהם אי-זוגיים, ולכן \( x = a \oplus d \), וזה נראה בדיוק כמו שני חסרים. בדוגמה
    החסר 7, הכפול 3, ו-\( x = 4 \). הבודק של סעיף א, שמסתכל רק על \( x \), היה אומר "חסר 4" :
    tag שחזר כרגיל.

    **סכומים זוכרים סימן.** הסכום של מה שנשלח פחות מה שחזר הוא \( a - d \) : החסר נספר עם \( + \),
    הכפול עם \( - \). שני נעלמים צריכים שתי משוואות, והשנייה היא אותו דבר עם ריבועים :

    <!-- gen 2 -->

    | המצבר | נשלחו | חזרו | ההפרש | מה זה |
    |:-:|:-:|:-:|:-:|---|
    | ‏`s` : סכום | ‏45 | ‏41 | ‏4 | ‏\( a - d \) |
    | ‏`q` : סכום ריבועים | ‏285 | ‏245 | ‏40 | ‏\( a^2 - d^2 \) |
    | ‏XOR | | | ‏4 | ‏\( a \oplus d \), כמו שני חסרים |
    | מונה | ‏10 | ‏10 | ‏0 | אף אחד לא "בחוץ" |

    <!-- /gen -->

    ‏\( a^2 - d^2 = (a - d)(a + d) \), ולכן \( a + d = 40 / 4 = 10 \), ‏\( a = (10 + 4)/2 = 7 \)
    ו-\( d = 3 \).

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module tag_sums" linenums="1" hl_lines="14 15 18 19 20"
        // one tag missing (a) and one returned twice (d): s = a - d, q = a^2 - d^2
        module tag_sums #(parameter int W = 8) (
          input  logic         clk, rst_n,
          input  logic         req_valid,
          input  logic [W-1:0] req_tag,
          input  logic         rsp_valid,
          input  logic [W-1:0] rsp_tag,
          output logic [W-1:0] miss, dup
        );
          longint s, q, total;
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin s <= 0; q <= 0; end
            else begin
              s <= s + (req_valid ? req_tag : 0) - (rsp_valid ? rsp_tag : 0);                       // (1)!
              q <= q + (req_valid ? req_tag * req_tag : 0) - (rsp_valid ? rsp_tag * rsp_tag : 0);
            end
          always_comb begin
            total = (s != 0) ? q / s : 0;    // a + d
            miss  = W'((total + s) / 2);     // (2)!
            dup   = W'((total - s) / 2);
          end
        endmodule
        ```

        1. ‏`longint` : הסכומים רחבים מ-\( W \) ועם סימן. ההקשר של 64 ביט מרחיב את `req_tag` לפני הכפל.
        2. ‏\( a = ((a + d) + (a - d)) / 2 \). החילוק מתאים לבודק בסוף הטסט, לא לנתיב קריטי.

    === "Python"
        ```python title="missing_and_dup" linenums="1" hl_lines="3 4 5"
        def missing_and_dup(sent: list[int], returned: list[int]) -> tuple[int, int]:
            """One tag missing (a) and one returned twice (d): s = a - d and q = a^2 - d^2."""
            s = sum(sent) - sum(returned)
            q = sum(t * t for t in sent) - sum(t * t for t in returned)
            total = q // s                                # (1)!
            return (total + s) // 2, (total - s) // 2
        ```

        1. ‏\( a^2 - d^2 = (a - d)(a + d) \), ולכן \( a + d = q / s \), והחילוק מדויק.

    #### למה זה נכון { .sol-proof }

    כל tag שחזר פעם אחת מתבטל בשני הסכומים. ה-tag החסר נשאר עם \( +a \) ו-\( +a^2 \), והכפול
    חזר פעם נוספת, עם \( -d \) ו-\( -d^2 \). ‏\( a \ne d \), ולכן \( s \ne 0 \) והחילוק מוגדר.

---

### סעיף ד – k חסרים

??? tip "רמז 1"
    בסעיף ג שני נעלמים דרשו שתי משוואות, סכום וסכום ריבועים. כמה משוואות צריך ל-\( k \)
    נעלמים?

??? tip "רמז 2"
    ‏\( p_i = \sum a_m^i \) עבור \( i = 1, \dots, k \). מהם בונים את הפולינום ששורשיו הם החסרים,
    בעזרת זהויות ניוטון.

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        שומרים \( k \) סכומי חזקות, \( p_i = \sum_{\text{sent}} t^i - \sum_{\text{returned}} t^i \),
        שהם סכומי החזקות של החסרים. זהויות ניוטון הופכות אותם למקדמים של
        \( \prod (z - a_m) \), ובסוף מציבים כל tag ובודקים מי שורש. הזיכרון גדל כמו \( k^2 W \),
        ולא כמו מספר ה-tags.

    <!-- cost: זיכרון \( O(k^2 W) \) ביטים | עדכון \( O(k) \) | פענוח \( O(n k) \) -->

    #### הרעיון { .sol-idea }

    סכומי החזקות \( p_1, \dots, p_k \) של \( k \) מספרים קובעים אותם : הם קובעים את
    הפולינומים הסימטריים האלמנטריים \( e_1, \dots, e_k \), שהם המקדמים של הפולינום שהשורשים
    שלו הם המספרים. הקשר הוא זהויות ניוטון :

    \[
    i \, e_i = \sum_{j=1}^{i} (-1)^{j-1} e_{i-j} \, p_j, \qquad e_0 = 1
    \]

    וההמשך הוא \( \prod_m (z - a_m) = z^k - e_1 z^{k-1} + e_2 z^{k-2} - \dots \). בסוף
    הטסט מציבים כל tag אפשרי : השורשים הם החסרים.

    **כמה זה עולה.** ‏\( p_i \) גדל עד בערך \( n^{i+1} \), כלומר \( (i + 1) W \) ביטים. לכל השיטות,
    ל-tags של 8 ביטים :

    <!-- gen 3 -->

    | השיטה | מה היא מוצאת | הרגיסטרים | ביטים ל-tags של 8 ביטים |
    |---|---|---|:-:|
    | ‏XOR | חסר אחד | ‏`x` | ‏8 |
    | ‏XOR לפי ביט | שני חסרים | ‏`x` ו-`part[0..W-1]` | ‏72 |
    | סכום וסכום ריבועים | חסר אחד וכפול אחד | ‏`s` ו-`q`, עם סימן | ‏40 |
    | סכומי חזקות עד 2 | עד 2 חסרים | ‏\( p_1, \dots, p_{2} \) | ‏38 |
    | סכומי חזקות עד 3 | עד 3 חסרים | ‏\( p_1, \dots, p_{3} \) | ‏68 |
    | סכומי חזקות עד 4 | עד 4 חסרים | ‏\( p_1, \dots, p_{4} \) | ‏106 |
    | טבלה של ביט לכל tag | הכול | ‏256 ביטים | ‏256 |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function missing_k" linenums="1" hl_lines="8 13 14 20"
        // up to k tags missing: power sums, Newton's identities, then the roots among 0..n-1
        function automatic void missing_k(int sent[$], int returned[$], int k, int n, ref int miss[$]);
          longint p[], e[], v;
          p = new[k + 1]; e = new[k + 1];
          for (int i = 1; i <= k; i++) begin
            p[i] = 0;
            foreach (sent[m])     p[i] += longint'(sent[m]) ** i;
            foreach (returned[m]) p[i] -= longint'(returned[m]) ** i;   // (1)!
          end
          e[0] = 1;
          for (int i = 1; i <= k; i++) begin
            e[i] = 0;
            for (int j = 1; j <= i; j++) e[i] += ((j % 2) ? 1 : -1) * e[i - j] * p[j];
            e[i] /= i;                                                   // (2)!
          end
          miss = {};
          for (int z = 0; z < n; z++) begin
            v = 0;
            for (int i = 0; i <= k; i++) v = v * z + ((i % 2) ? -e[i] : e[i]);
            if (v == 0) miss.push_back(z);                               // (3)!
          end
        endfunction
        ```

        1. ‏\( p_i \) של החסרים : כל tag שחזר מתבטל.
        2. זהות ניוטון. החילוק ב-\( i \) תמיד מדויק.
        3. ‏הורנר על \( z^k - e_1 z^{k-1} + e_2 z^{k-2} - \dots \) : שורש הוא tag חסר. עם פחות מ-\( k \) חסרים, ‏\( e_i \) העליונים 0 והשורש 0 נוסף. לכן משתמשים במונה כדי לדעת את \( k \).

    === "Python"
        ```python title="missing_k" linenums="1" hl_lines="4 7 9"
        def missing_k(sent: list[int], returned: list[int], k: int, n: int) -> list[int]:
            """Exactly k tags missing: power sums of the missing set, Newton's identities,
            then the roots of prod(z - a) among the tags 0..n-1."""
            p = [sum(t ** i for t in sent) - sum(t ** i for t in returned) for i in range(k + 1)]
            e = [1] + [0] * k
            for i in range(1, k + 1):
                e[i] = sum((-1) ** (j - 1) * e[i - j] * p[j] for j in range(1, i + 1)) // i   # (1)!
            poly = lambda z: sum((-1) ** i * e[i] * z ** (k - i) for i in range(k + 1))
            return [z for z in range(n) if poly(z) == 0]
        ```

        1. זהויות ניוטון : ‏\( i \, e_i = \sum_j (-1)^{j-1} e_{i-j} p_j \).

    #### למה זה נכון { .sol-proof }

    **סכומי החזקות של החסרים.** כמו קודם, כל tag שחזר מתבטל בכל \( p_i \).

    **מהם לחסרים.** זהויות ניוטון נכונות לכל \( k \) מספרים, ולכן ה-\( e_i \) שיוצאים הם
    המקדמים של \( \prod_m (z - a_m) \). פולינום ממעלה \( k \) שאינו אפס מתאפס רק בשורשים שלו,
    והם בדיוק החסרים.

    **נסו בעצמכם.** בוחרים כמה tags, ולוחצים על tag כדי שלא יחזור או שיחזור פעמיים, או
    בוחרים תרחיש מוכן. התשובות חוזרות בסדר אקראי, והמצברים מתעדכנים. בסוף רואים מה כל שיטה
    מוצאת, ואיפה היא טועה. במצב "חידה" התיבה מסתירה את התקלה, ואתם מוצאים אותה מהמצברים :

    <div class="explorer" data-kind="tagcheck" data-n="16" data-case="two"></div>

    #### סיבוכיות { .sol-cost }

    - **זיכרון :** ‏\( W \) ביטים לחסר אחד, ‏\( W(W+1) \) לשניים ב-XOR, וכ-\( k^2 W / 2 \) לסכומי
      חזקות עד \( k \), במקום \( 2^W \) לטבלה.
    - **עדכון :** ‏\( O(1) \) עד \( O(k) \) לכל תשובה, בלי תלות במספר ה-tags.
    - **פענוח :** בסעיף ד מציבים כל tag, ‏\( O(n k) \), פעם אחת בסוף הטסט.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לסמוך על 0"
    רגיסטר XOR שמכיל 0 בסוף לא אומר שהכול חזר : אולי חסר tag 0, ואולי חסרים שלושה tags שה-XOR שלהם
    0 (למשל 1, 2 ו-3). המונה של הבקשות הפתוחות הוא חלק מהבודק, לא תוספת.

??? trap "מלכודת : 'שני חסרים' שהם בעצם כפול"
    ‏XOR סופר מודולו 2, ולכן tag שחזר פעמיים נראה כמו tag שלא חזר. בודק שמכריז "חסרים a
    ו-b" בלי לבדוק את המונה יחפש באג במקום הלא נכון.

??? trap "מלכודת : סכומים ברוחב של tag"
    סכום של 256 tags של 8 ביטים לא נכנס ב-8 ביטים, וסכום ריבועים לא נכנס ב-16. גלישה מודולו
    \( 2^w \) שוברת את החילוק של סעיף ג. בודקים את רוחב המצבר מול הערך הגדול ביותר.

??? followup "שאלות המשך"
    - **‏tags שחוזרים לשימוש :** אחרי שתשובה חוזרת, ה-tag שלה נשלח שוב. האם המצברים עדיין
      עובדים?

        ??? fu-answer "תשובה"
            כן : כל שליחה וכל חזרה נכנסות למצבר, ולכן בכל רגע הוא מתאר את ה-tags שבחוץ עכשיו, גם
            אם כל tag נשלח פעמים רבות. כך בדיוק עובדים המודולים של סעיפים א עד ג.

    - **מתי לדווח :** הבודק יודע מה חסר רק בסוף. איך מגלים tag שלא חוזר כבר באמצע הטסט?

        ??? fu-answer "תשובה"
            צריך זמן : מונה גיל לכל tag פתוח (וזו שוב טבלה), או timeout על הבקשה הוותיקה ביותר אם
            התשובות חוזרות בסדר. המצברים הם בדיקה זולה של סוף הטסט, לא תחליף לבדיקת זמן.

    - **‏tag שחזר עם נתונים שגויים :** האם המצברים יגלו את זה?

        ??? fu-answer "תשובה"
            לא, הם רואים רק tags. לנתונים צריך scoreboard, או לפחות XOR או CRC של (tag, נתונים) בשני
            הצדדים, שמגלה שינוי אבל לא אומר איפה.
