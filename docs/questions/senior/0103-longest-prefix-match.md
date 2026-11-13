---
id: 103
title: הקידומת הארוכה ביותר – טבלת ניתוב, עץ ביטים וחיפוש בצנרת
level: senior
difficulty: hard
kind: code
tags: [algorithms, bitwise, digital-design, protocols, python, systemverilog]
source: "חיפוש הקידומת הארוכה ביותר (longest prefix match) של נתבי IP, מאז CIDR (RFC 4632)"
added: 2026-11-13
---

## השאלה

בטבלת ניתוב כל שורה היא **קידומת** של כתובת, עם אורך, ו**קפיצה הבאה** : לאן לשלוח חבילה שהכתובת
שלה מתחילה בקידומת הזו. הכתובות הן של 32 ביטים, כתובות כארבעה מספרים של 8 ביטים, והאורך אומר
כמה ביטים עליונים של הקידומת נבדקים. לדוגמה :

| הקידומת | הקפיצה הבאה |
|---|:-:|
| ‏<span dir="ltr">10.0.0.0/8</span> | ‏A |
| ‏<span dir="ltr">10.1.0.0/16</span> | ‏B |
| ‏<span dir="ltr">10.1.2.0/24</span> | ‏C |
| ‏<span dir="ltr">172.16.0.0/12</span> | ‏E |
| ‏<span dir="ltr">0.0.0.0/0</span> | ‏D, ברירת המחדל |

לכתובת <span dir="ltr">10.1.2.3</span> מתאימות ארבע שורות : ‏/0, ‏/8, ‏/16 ו-/24. החוק הוא
**הקידומת הארוכה ביותר** (longest prefix match) : היא המדויקת ביותר, ולכן החבילה הולכת ל-C. בהינתן
טבלה וכתובת, החזירו את הקפיצה הבאה של הקידומת הארוכה ביותר שמתאימה לכתובת, או "אין" אם אף שורה
לא מתאימה.

**ההקשר באימות :** זה מודל הייחוס של כל נתב, וגם של מפענח הכתובות ב-NoC או ב-interconnect : מפת
כתובות עם אזורים חופפים, שבה האזור המדויק יותר גובר. ה-scoreboard שבודק את החומרה צריך את
התשובה הנכונה לכל כתובת, והחומרה עצמה צריכה למצוא אותה בכל שעון.

- **סעיף א – סריקה :** הדרך הישירה, שורה אחרי שורה.
- **סעיף ב – עץ ביטים :** חיפוש שלא תלוי במספר השורות, עם הוספה ומחיקה.
- **סעיף ג – כמה ביטים בכל צעד :** פחות צעדים, במחיר של זיכרון.
- **סעיף ד – בחומרה :** חיפוש אחד בכל שעון, בצנרת.

??? interviewer "מה המראיין בודק"
    - **ביטים ומסכות :** האם המועמד רואה כתובת כמספר של 32 ביטים, משווה רק את הביטים שמתחת
      למסכה, ושם לב למקרי הקצה של המסכה.
    - **מבנה נתונים :** האם הוא מגיע לבד לעץ שבו כל רמה היא ביט, ויודע מה לזכור בדרך למטה.
    - **זמן מול זיכרון :** כמה צעדים לחיפוש וכמה זיכרון, ואיך לסחור ביניהם.
    - **חומרה ואימות :** האם הוא יודע להפוך את החיפוש לצנרת, מה עובר בין השלבים, ואיך בודקים
      אותה מול מודל ייחוס, כולל המקרים שהבדיקות האקראיות מפספסות.

---

### סעיף א – סריקה של כל השורות

כתבו פונקציה שמקבלת את הטבלה וכתובת, ועוברת על כל השורות. מתי שורה מתאימה לכתובת, ואיך בוחרים
ביניהן? מה זמן החיפוש?

??? tip "רמז 1"
    שורה עם אורך \( k \) מתאימה כשה-\( k \) ביטים העליונים של הכתובת שווים ל-\( k \) הביטים
    העליונים של הקידומת. איזו מסכה בוחרת את הביטים האלה?

??? tip "רמז 2"
    בנו את המסכה של \( k \) ביטים בכמה דרכים, ובדקו כל אחת ב-\( k = 0 \) וב-\( k = 32 \).

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שורה <span dir="ltr">(value, k)</span> מתאימה ל-addr כש-<span dir="ltr">(addr ^ value) & mask(k) == 0</span>,
        כש-mask(k) הוא \( k \) אחדות עליונות. עוברים על כל השורות ושומרים את המתאימה הארוכה ביותר :
        ‏\( O(N) \) לחיפוש. המלכודת היא /0 : המסכה שלו היא 0, וההזזה הרגילה שבונה אותה, הזזה ב-32, לא
        מוגדרת ב-C.

    <!-- cost: זמן \( O(N) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    הכתובת והקידומת הן מספרים של 32 ביטים, והמספר הראשון בכתובת הוא הבית העליון. ה-XOR שלהן
    מדליק בדיוק את הביטים שבהם הן שונות. אם אף אחד מהם לא נמצא ב-\( k \) הביטים העליונים, השורה
    מתאימה. מבין השורות המתאימות לוקחים את זו עם \( k \) הגדול ביותר. בדוגמה :

    <!-- gen 0 -->

    | הכתובת | השורות שמתאימות | הארוכה | הקפיצה הבאה |
    |---|---|:-:|:-:|
    | ‏<span dir="ltr">10.1.2.3</span> | ‏<span dir="ltr">/0, /8, /16, /24</span> | ‏/24 | ‏C |
    | ‏<span dir="ltr">10.1.3.4</span> | ‏<span dir="ltr">/0, /8, /16</span> | ‏/16 | ‏B |
    | ‏<span dir="ltr">10.200.0.1</span> | ‏<span dir="ltr">/0, /8</span> | ‏/8 | ‏A |
    | ‏<span dir="ltr">172.20.1.1</span> | ‏<span dir="ltr">/0, /12</span> | ‏/12 | ‏E |
    | ‏<span dir="ltr">172.32.0.1</span> | ‏<span dir="ltr">/0</span> | ‏/0 | ‏D |
    | ‏<span dir="ltr">8.8.8.8</span> | ‏<span dir="ltr">/0</span> | ‏/0 | ‏D |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הכתובת כמספר :** ‏<span dir="ltr">10.1.2.3</span> הוא
       <span dir="ltr">10 · 2²⁴ + 1 · 2¹⁶ + 2 · 2⁸ + 3</span>.
    2. **המסכה :** \( k \) אחדות עליונות, \( 2^{32} - 2^{32 - k} \). ב-\( k = 0 \) זה 0, וכל כתובת
       מתאימה. ב-\( k = 32 \) אלה 32 אחדות, וצריך שוויון מלא.
    3. **הסריקה :** לכל שורה, אם <span dir="ltr">(addr ^ value) & mask(k)</span> הוא 0 והאורך לא
       קטן מהטוב עד עכשיו, היא החדשה הטובה.
    4. **התשובה :** הקפיצה של הטובה, או "אין" כשאף שורה לא התאימה, וזה קורה רק בטבלה בלי /0.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="lpm_naive" linenums="1" hl_lines="11 17 24"
        def ip(text):
            """'10.1.2.3' -> a 32-bit number, the first number the high byte (big-endian)."""
            n = 0
            for part in text.split("."):
                n = n << 8 | int(part)                       # (1)!
            return n


        def mask(k, w=32):
            """The top k bits of a w-bit word set: mask(0) is 0, with no shift by w."""
            return ((1 << w) - 1) ^ ((1 << (w - k)) - 1)     # (2)!


        def route(text, hop, w=32):
            """'10.1.2.3/16' -> (10.1.0.0 as a number, 16, hop): the bits under the mask cleared."""
            addr, k = text.split("/")
            return ip(addr) & mask(int(k), w), int(k), hop   # (3)!


        def lpm_naive(routes, addr, w=32):
            """The hop of the longest prefix that matches addr; None when none does."""
            best, best_len = None, -1
            for value, k, hop in routes:
                if (addr ^ value) & mask(k, w) == 0 and k >= best_len:   # (4)!
                    best, best_len = hop, k
            return best
        ```

        1. כל מספר נכנס מתחת לקודמים : הראשון מגיע לבית העליון. זה סדר הביטים של הרשת (big-endian).
        2. ‏\( 2^w - 1 \) הן \( w \) אחדות, ו-\( 2^{w-k} - 1 \) הן \( w - k \) האחדות התחתונות.
           ה-XOR משאיר את \( k \) העליונות. ב-Python המספרים לא מוגבלים, ולכן ‏<span dir="ltr">1 << 32</span>
           הוא באמת \( 2^{32} \).
        3. הקידומת נשמרת עם אפסים מתחת למסכה : ‏<span dir="ltr">10.1.2.3/16</span> נשמרת כ-<span dir="ltr">10.1.0.0/16</span>.
           הסריקה לא צריכה את זה, כי המסכה מסתירה את הביטים האלה, אבל העצים של סעיפים ב ו-ג כן.
        4. ‏`>=` ולא `>` : שתי שורות מתאימות באותו אורך הן אותה קידומת, כתובה פעמיים. השורה המאוחרת
           גוברת, כמו בעץ, שבו הוספה שנייה מחליפה את הראשונה.

    === "SystemVerilog"
        ```systemverilog title="function automatic int lpm_naive" linenums="1" hl_lines="9 20"
        typedef struct {
          logic [31:0] value;            // the prefix, the bits under the mask 0
          int          len;              // 0 to w: 33 values for w = 32, more than 5 bits hold
          int          hop;              // the next hop
        } route_t;

        // The top k bits of a w-bit word set; in 64 bits, so that 1 << 32 is 2^32 and k = 0 gives 0
        function automatic logic [31:0] prefix_mask(int k, int w = 32);
          return 32'(((64'd1 << w) - 1) ^ ((64'd1 << (w - k)) - 1));   // (1)!
        endfunction

        function automatic route_t make_route(logic [31:0] value, int len, int hop, int w = 32);
          return '{value & prefix_mask(len, w), len, hop};
        endfunction

        // The hop of the longest prefix that matches addr; -1 when none does
        function automatic int lpm_naive(route_t routes[$], logic [31:0] addr, int w = 32);
          int best = -1, best_len = -1;
          foreach (routes[i])
            if (((addr ^ routes[i].value) & prefix_mask(routes[i].len, w)) == 0
                && routes[i].len >= best_len) begin
              best = routes[i].hop;
              best_len = routes[i].len;
            end
          return best;
        endfunction
        ```

        1. החשבון ב-64 ביטים, ולכן גם \( w - k = 32 \) לא מגיע לרוחב של המספר. ב-SystemVerilog הזזה
           ברוחב המספר או יותר מוגדרת ונותנת 0, אבל ב-C היא לא מוגדרת, ומעבד x86 לוקח רק את 5 הביטים
           התחתונים של ההזזה : ‏<span dir="ltr">~0u << 32</span> נשאר 32 אחדות, ו-/0 מתאים רק לכתובת 0.

    #### למה זה נכון { .sol-proof }

    **ההתאמה.** ‏<span dir="ltr">addr ^ value</span> מדליק את הביטים שבהם השתיים שונות, והמסכה
    משאירה מהם רק את \( k \) העליונים. התוצאה 0 בדיוק כשהן שוות בכל \( k \) הביטים העליונים, וזו
    ההגדרה של התאמה.

    **הבחירה.** הסריקה שומרת בכל רגע את השורה הארוכה ביותר מבין השורות שכבר נבדקו ומתאימות. בסוף
    נבדקו כולן. שתי שורות שונות לא יכולות להתאים באותו אורך, כי אז שתיהן שוות ל-\( k \) הביטים
    העליונים של הכתובת, ולכן זו לזו.

    #### סיבוכיות { .sol-cost }

    ‏\( N \) שורות, ובכל אחת XOR, AND והשוואה : \( O(N) \) לחיפוש, וזיכרון נוסף \( O(1) \). לנתב עם
    מיליון קידומות ומאות מיליוני חבילות בשנייה זה רחוק מלהספיק, אבל כמודל ייחוס זה בדיוק מה
    שצריך : קוד קצר שקל לראות שהוא נכון.

---

### סעיף ב – עץ ביטים

בנו מבנה נתונים שבו זמן החיפוש לא תלוי במספר השורות, אלא רק ברוחב הכתובת. תמכו גם בהוספה
ובמחיקה של שורה. כמה צעדים לוקח חיפוש, וכמה זיכרון?

??? tip "רמז 1"
    קראו את הכתובת ביט אחרי ביט מהעליון. כל קידומת היא דרך מהשורש : 0 שמאלה, 1 ימינה.

??? tip "רמז 2"
    בדרך למטה עוברים דרך כל הקידומות שמתאימות לכתובת, מהקצרה לארוכה. מה מספיק לזכור מהן?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **עץ ביטים** (binary trie) : רמה לכל ביט, וקידומת באורך \( k \) נשמרת בצומת בעומק \( k \).
        החיפוש יורד לפי ביטי הכתובת וזוכר את הקידומת האחרונה שעבר בדרך. הוא נעצר כשאין בן, או אחרי
        \( W = 32 \) ביטים. לכן חיפוש לוקח לכל היותר 32 צעדים, יהיו בטבלה כמה שורות שיהיו. הזיכרון
        הוא \( O(N \cdot W) \) צמתים במקרה הגרוע.

    <!-- cost: זמן \( O(W) \) | זיכרון \( O(N \cdot W) \) -->

    #### הרעיון { .sol-idea }

    כל הקידומות שמתאימות לכתובת הן התחלות שלה, ולכן הן נמצאות על דרך אחת בעץ : הדרך של
    הכתובת עצמה. החיפוש יורד בה וזוכר את הצומת האחרון שהחזיק קידומת. אין צורך לחזור למעלה : כל
    קידומת שנמצאה מאוחר יותר ארוכה יותר.

    באיור הטבלה בקטן, כתובות של 8 ביטים, והחיפוש של 185, הביטים <span dir="ltr">1011 1001</span>.
    הקידומות : ‏ε (הריקה, /0) אל D, ‏`1*` אל A, ‏`101*` אל B, ‏`10110*` אל C ו-`01*` אל E. החיפוש עובר ב-D,
    ב-A וב-B, יורד עוד צעד ל-1011, צומת בלי קידומת, ונעצר כי אין לו בן 1. התשובה היא B, האחרונה
    שנמצאה בדרך, ולא משהו מהצומת שבו החיפוש נעצר :

    <!-- gen 1 -->

    <svg class="figure lpm-trie" viewBox="0 0 190 286" style="max-width:11.875rem" direction="ltr" role="img" aria-label="עץ הביטים של הטבלה הקטנה, כתובות של 8 ביטים : הקידומות הריקה אל D, 1 אל A, 101 אל B, 10110 אל C, 01 אל E. החיפוש של 185, הביטים 10111001, עובר בצמתים השורש, 1, 10, 101, 1011 ונעצר, והתשובה B"><line class="lpm-edge" x1="84.0" y1="26.0" x2="40.0" y2="72.0"/><text class="lpm-bit" x="53.0" y="53.0" text-anchor="middle">0</text><line class="lpm-edge is-on" x1="84.0" y1="26.0" x2="128.0" y2="72.0"/><text class="lpm-bit" x="115.0" y="53.0" text-anchor="middle">1</text><line class="lpm-edge" x1="40.0" y1="72.0" x2="62.0" y2="118.0"/><text class="lpm-bit" x="60.0" y="99.0" text-anchor="middle">1</text><line class="lpm-edge is-on" x1="128.0" y1="72.0" x2="106.0" y2="118.0"/><text class="lpm-bit" x="108.0" y="99.0" text-anchor="middle">0</text><line class="lpm-edge is-on" x1="106.0" y1="118.0" x2="128.0" y2="164.0"/><text class="lpm-bit" x="126.0" y="145.0" text-anchor="middle">1</text><line class="lpm-edge is-on" x1="128.0" y1="164.0" x2="150.0" y2="210.0"/><text class="lpm-bit" x="148.0" y="191.0" text-anchor="middle">1</text><line class="lpm-edge" x1="150.0" y1="210.0" x2="128.0" y2="256.0"/><text class="lpm-bit" x="130.0" y="237.0" text-anchor="middle">0</text><line class="lpm-edge lpm-miss" x1="150.0" y1="210.0" x2="172.0" y2="243.0"/><text class="lpm-miss-t" x="172.0" y="260.0" text-anchor="middle">×</text><g class="lpm-node has-hop is-on"><circle cx="84.0" cy="26.0" r="13"/><text x="84.0" y="30.0" text-anchor="middle">D</text><title>השורש : הקידומת * אל D</title></g><g class="lpm-node no-hop"><circle cx="40.0" cy="72.0" r="13"/><title>0 : אין קידומת</title></g><g class="lpm-node has-hop is-on"><circle cx="128.0" cy="72.0" r="13"/><text x="128.0" y="76.0" text-anchor="middle">A</text><title>1 : הקידומת 1* אל A</title></g><g class="lpm-node has-hop"><circle cx="62.0" cy="118.0" r="13"/><text x="62.0" y="122.0" text-anchor="middle">E</text><title>01 : הקידומת 01* אל E</title></g><g class="lpm-node no-hop is-on"><circle cx="106.0" cy="118.0" r="13"/><title>10 : אין קידומת</title></g><g class="lpm-node has-hop is-on is-win"><circle cx="128.0" cy="164.0" r="13"/><text x="128.0" y="168.0" text-anchor="middle">B</text><title>101 : הקידומת 101* אל B</title></g><g class="lpm-node no-hop is-on"><circle cx="150.0" cy="210.0" r="13"/><title>1011 : אין קידומת</title></g><g class="lpm-node has-hop"><circle cx="128.0" cy="256.0" r="13"/><text x="128.0" y="260.0" text-anchor="middle">C</text><title>10110 : הקידומת 10110* אל C</title></g><text class="lpm-depth" x="6" y="30.0">0</text><text class="lpm-depth" x="6" y="76.0">1</text><text class="lpm-depth" x="6" y="122.0">2</text><text class="lpm-depth" x="6" y="168.0">3</text><text class="lpm-depth" x="6" y="214.0">4</text><text class="lpm-depth" x="6" y="260.0">5</text></svg>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="lpm-key-hop"></i>צומת שמחזיק קידומת</span><span><i class="lpm-key-nohop"></i>צומת בדרך, בלי קידומת</span><span><i class="lpm-key-on"></i>הדרך של החיפוש</span><span><i class="lpm-key-win"></i>הקידומת הארוכה שנמצאה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הוספה :** יורדים לפי \( k \) הביטים העליונים של הקידומת, יוצרים צומת שחסר, ובצומת
       בעומק \( k \) כותבים את הקפיצה. ‏/0 נכתבת בשורש.
    2. **חיפוש :** מתחילים בשורש, עם הקפיצה שלו כטובה עד עכשיו. בכל צעד יורדים לבן לפי הביט הבא
       של הכתובת. אם אין בן, עוצרים. אם לבן יש קפיצה, היא הטובה החדשה.
    3. **מחיקה :** יורדים לצומת של הקידומת ומוחקים ממנו את הקפיצה. אחר כך עולים בחזרה ומנתקים
       כל צומת שנשאר בלי קפיצה ובלי בנים. צומת שיש לו בן נשאר : קידומת ארוכה יותר עוברת דרכו.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="Trie" linenums="1" hl_lines="18 21 32 37 48"
        class Trie:
            """A binary trie of w-bit prefixes: a level a bit, the top bit first. A node is a
            list [child 0, child 1, hop], hop None when no prefix ends at it."""

            def __init__(self, w=32):
                self.w = w
                self.root = [None, None, None]
                self.nodes = 1

            def bit(self, value, i):
                return value >> (self.w - 1 - i) & 1                   # (1)!

            def insert(self, value, k, hop):
                node = self.root
                for i in range(k):                                     # (2)!
                    b = self.bit(value, i)
                    if node[b] is None:
                        node[b] = [None, None, None]
                        self.nodes += 1
                    node = node[b]
                node[2] = hop

            def delete(self, value, k):
                path = [self.root]
                for i in range(k):
                    nxt = path[-1][self.bit(value, i)]
                    if nxt is None:
                        return False
                    path.append(nxt)
                if path[-1][2] is None:
                    return False
                path[-1][2] = None
                for i in range(k, 0, -1):
                    node = path[i]
                    if node[0] is not None or node[1] is not None or node[2] is not None:
                        break                                          # (3)!
                    path[i - 1][self.bit(value, i - 1)] = None
                    self.nodes -= 1
                return True

            def lookup(self, addr):
                node, best = self.root, self.root[2]
                for i in range(self.w):
                    node = node[self.bit(addr, i)]
                    if node is None:
                        break
                    if node[2] is not None:
                        best = node[2]                                 # (4)!
                return best
        ```

        1. ביט 0 הוא העליון : ‏\( w - 1 \) מקומות מימין. כך הקידומת נקראת מההתחלה של הכתובת.
        2. רק \( k \) ביטים : הביטים שמתחת למסכה לא נקראים, ולכן גם קידומת שלא נורמלה נכנסת למקום הנכון.
        3. צומת עם בן או עם קפיצה נשאר, וגם כל הצמתים מעליו. בלי הבדיקה הזו, מחיקה של
           <span dir="ltr">10.0.0.0/8</span> הייתה מנתקת את <span dir="ltr">10.1.0.0/16</span> שמתחתיה.
        4. רק כאן משתנה התשובה. צומת בלי קפיצה, כמו 1011 באיור, משאיר את הטובה של הצומת שמעליו.

    === "SystemVerilog"
        ```systemverilog title="class trie" linenums="1" hl_lines="21 29 44 45 56"
        // A binary trie of w-bit prefixes in arrays: node i has the children c0[i] and c1[i]
        // (-1: none) and hop[i] (-1: no prefix ends at it); node 0 is the root
        class trie;
          int w, nodes;
          int c0[$], c1[$], hop[$];

          function new(int w = 32);
            this.w = w;
            c0.push_back(-1); c1.push_back(-1); hop.push_back(-1);
            nodes = 1;
          endfunction

          function int child(int n, bit b);
            return b ? c1[n] : c0[n];
          endfunction

          function void insert(logic [31:0] value, int k, int h);
            int n = 0;
            bit b;
            for (int i = 0; i < k; i++) begin
              b = value[w - 1 - i];
              if (child(n, b) < 0) begin
                c0.push_back(-1); c1.push_back(-1); hop.push_back(-1);
                if (b) c1[n] = c0.size() - 1; else c0[n] = c0.size() - 1;
                nodes++;
              end
              n = child(n, b);
            end
            hop[n] = h;
          endfunction

          function bit remove(logic [31:0] value, int k);
            int path[$] = '{0};
            int n;
            for (int i = 0; i < k; i++) begin
              n = child(path[i], value[w - 1 - i]);
              if (n < 0) return 0;
              path.push_back(n);
            end
            if (hop[path[k]] < 0) return 0;
            hop[path[k]] = -1;
            for (int i = k; i > 0; i--) begin
              n = path[i];
              if (c0[n] >= 0 || c1[n] >= 0 || hop[n] >= 0) break;
              if (value[w - i]) c1[path[i - 1]] = -1; else c0[path[i - 1]] = -1;   // (1)!
              nodes--;
            end
            return 1;
          endfunction

          function int lookup(logic [31:0] addr);
            int n = 0, best = hop[0];
            for (int i = 0; i < w; i++) begin
              n = child(n, addr[w - 1 - i]);
              if (n < 0) break;
              if (hop[n] >= 0) best = hop[n];
            end
            return best;
          endfunction
        endclass
        ```

        1. הצומת מנותק מאביו. המקום שלו במערכים נשאר, ורשימה של מקומות פנויים הייתה מחזירה אותו
           להוספה הבאה. ‏`nodes` סופר את הצמתים שבעץ.

    #### למה זה נכון { .sol-proof }

    **כל המתאימות על הדרך.** קידומת באורך \( k \) מתאימה לכתובת בדיוק כשהיא \( k \) הביטים הראשונים
    שלה, כלומר כשהצומת שלה הוא הצומת בעומק \( k \) על הדרך של הכתובת. לכן החיפוש פוגש את כל
    הקידומות המתאימות, ורק אותן, מהקצרה לארוכה.

    **העצירה.** אם לצומת בעומק \( i \) אין בן בכיוון של הביט הבא, אין בעץ אף קידומת שמתחילה
    ב-\( i + 1 \) הביטים הראשונים של הכתובת, ולכן אין קידומת מתאימה ארוכה יותר. הקידומת האחרונה
    שנמצאה היא הארוכה ביותר.

    **המחיקה.** צומת נחוץ אם הוא מחזיק קידומת או אם יש לו בן, כי אז קידומת כלשהי עוברת דרכו.
    המחיקה מנתקת רק צמתים שאינם נחוצים, מלמטה למעלה, ונעצרת בצומת הנחוץ הראשון. כל הצמתים מעליו
    נחוצים, כי הוא מתחתם.

    **נסו בעצמכם.** התיבה נפתחת על הטבלה של האיור והכתובת 185. צעדו ביט אחרי ביט : B נשאר הטוב
    ביותר גם כשהחיפוש יורד ל-1011, והטבלה מסמנת את שלוש השורות שמתאימות. כתבו 182 : החיפוש מגיע
    ל-10110 והתשובה C. אחר כך לחצו על "אין התאמה" : הכתובת 0 עוברת בשורש ובצומת 0, לא פוגשת אף קידומת, ואין תשובה. כתבו
    בטבלה <span dir="ltr">183/3</span> : השורה נשמרת כ-<span dir="ltr">160/3</span>, ‏`101*`. מעבר
    לאיור, התיבה מראה לכל צעד את הטוב עד עכשיו, ומשווה את התשובה לסריקה של סעיף א.

    <div class="explorer" data-kind="lpmtrie" data-addr="185"></div>

    #### סיבוכיות { .sol-cost }

    **זמן.** חיפוש, הוספה ומחיקה יורדים לכל היותר \( W \) רמות : \( O(W) \), ‏32 צעדים, בלי קשר
    ל-\( N \).

    **זיכרון.** כל קידומת מוסיפה לכל היותר \( W \) צמתים, ולכן יש לכל היותר \( N \cdot W + 1 \)
    צמתים. בטבלת הדוגמה של השאלה יש 37 צמתים לחמש קידומות : ‏/8, ‏/16 ו-/24 חולקות את הדרך של
    <span dir="ltr">10.1.2.0/24</span>, ‏24 צמתים, ו-<span dir="ltr">172.16.0.0/12</span> נפרדת כבר
    בביט הראשון, ‏12 צמתים, ועוד השורש. רוב הצמתים הם שרשרת עם בן אחד, וכל אחד מהם הוא צעד של
    חיפוש וקריאה מהזיכרון.

---

### סעיף ג – כמה ביטים בכל צעד

‏32 צעדים הם 32 קריאות מהזיכרון. קראו \( s \) ביטים בכל צעד במקום אחד : כל צומת הוא טבלה של
\( 2^s \) כניסות, והחיפוש לוקח \( W / s \) צעדים. מה עושים עם קידומת שהאורך שלה לא מתחלק
ב-\( s \)? כמה צעדים וכמה כניסות עולה כל \( s \) בטבלת הדוגמה?

??? tip "רמז 1"
    קידומת באורך 3 כשקוראים שני ביטים בכל צעד : לאילו כתובות של 4 ביטים היא מתאימה?

??? tip "רמז 2"
    שתי קידומות יכולות לבקש את אותה כניסה, למשל <span dir="ltr">1*</span> ו-<span dir="ltr">10*</span>
    בצעד של שני ביטים. מי צריכה לקבל אותה, ומה אם הארוכה נוספה לפני הקצרה?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        **הרחבה מבוקרת של קידומות** (controlled prefix expansion) : קידומת באורך \( k \) מורחבת לכפולה
        הבאה של \( s \), ומעתיקים אותה ל-\( 2^{s - k \bmod s} \) כניסות, או לכניסה אחת כש-\( k \) מתחלק
        ב-\( s \). ‏/0 ממלאת את כל \( 2^s \) הכניסות של השורש. כניסה שכבר מחזיקה קידומת מקורית ארוכה יותר לא נדרסת. החיפוש לוקח \( W / s \) צעדים,
        וכל צומת עולה \( 2^s \) כניסות. בטבלת הדוגמה \( s = 8 \) נותן 4 צעדים ו-1,024 כניסות, לעומת
        32 צעדים ו-70 כניסות של \( s = 1 \).

    <!-- cost: זמן \( O(W/s) \) | זיכרון \( 2^s \) לצומת -->

    #### הרעיון { .sol-idea }

    בצעד של \( s \) ביטים העץ יכול לבדוק רק אורכים שהם כפולות של \( s \). קידומת באורך אחר
    מוחלפת בכל ההמשכים שלה עד הכפולה הבאה : ‏`101*` עם \( s = 2 \) היא ‏`1010*` ו-`1011*`. אותה
    קבוצה של כתובות, ועכשיו באורך שהעץ יודע לבדוק. כשההרחבה של קידומת קצרה פוגשת כניסה של קידומת
    ארוכה יותר, הארוכה נשארת : היא הייתה מנצחת גם בסריקה. כך מתחלקת הטבלה הקטנה של סעיף ב בצעד
    של שני ביטים :

    <!-- gen 3 -->

    | הקידומת | האורך | מורחבת ל | הכניסות | נשארות לה |
    |---|:-:|:-:|---|---|
    | ‏<code>ε*</code> אל D | 0 | 2 | ‏<code>00</code>, <code>01</code>, <code>10</code>, <code>11</code> | ‏<code>00</code> |
    | ‏<code>1*</code> אל A | 1 | 2 | ‏<code>10</code>, <code>11</code> | ‏<code>10</code>, <code>11</code> |
    | ‏<code>101*</code> אל B | 3 | 4 | ‏<code>1010</code>, <code>1011</code> | ‏<code>1010</code>, <code>1011</code> |
    | ‏<code>10110*</code> אל C | 5 | 6 | ‏<code>101100</code>, <code>101101</code> | ‏<code>101100</code>, <code>101101</code> |
    | ‏<code>01*</code> אל E | 2 | 2 | ‏<code>01</code> | ‏<code>01</code> |

    <!-- /gen -->

    וכך עולה כל רוחב של צעד בטבלת הדוגמה של 32 ביטים. "כניסות בטבלאות" הן \( 2^s \) לכל צומת,
    ו"עם קפיצה" הן הכניסות שההרחבה מילאה :

    <!-- gen 4 -->

    | ביטים בצעד s | צעדים לחיפוש | צמתים | כניסות בטבלאות | כניסות עם קפיצה |
    |:-:|:-:|:-:|:-:|:-:|
    | 1 | 32 | 35 | 70 | 6 |
    | 2 | 16 | 17 | 68 | 8 |
    | 4 | 8 | 8 | 128 | 20 |
    | 8 | 4 | 4 | 1,024 | 274 |

    <!-- /gen -->

    ב-\( s = 1 \) יש 35 צמתים, ולא 37 כמו בסעיף ב : הקפיצה יושבת בכניסה של האב ולא בצומת משלה,
    ולכן לשני העלים אין צומת. ב-\( s = 8 \) השורש לבד הוא 256 כניסות, ו-255 מהן מחזיקות את D.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **האורך החדש :** ‏\( L = s \cdot \lceil k / s \rceil \), ולפחות \( s \).
    2. **הירידה :** יורדים \( L / s - 1 \) רמות לפי הביטים של הקידומת, ויוצרים צומת שחסר. לצומת
       חדש \( 2^s \) כניסות ריקות.
    3. **ההרחבה :** בצומת שהגענו אליו, \( 2^{L - k} \) כניסות רצופות מתחילות בכניסה של \( s \) הביטים
       האחרונים, עם אפסים מתחת לקידומת. כל אחת מקבלת את הקפיצה ואת \( k \), אלא אם יש בה כבר \( k \)
       גדול יותר.
    4. **החיפוש :** בכל רמה קוראים כניסה אחת לפי \( s \) ביטים של הכתובת. קפיצה בכניסה היא הטובה
       החדשה. אם אין לכניסה בן, עוצרים.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="MultiTrie" linenums="1" hl_lines="18 19 27 29 30"
        class MultiTrie:
            """A multibit trie: s bits a step, w / s levels. levels[d] holds the nodes of depth d
            one after another, 2^s entries each; an entry is [hop, its prefix length, child]."""

            def __init__(self, w=32, s=8):
                self.w, self.s = w, s
                self.levels = [[] for _ in range(w // s)]
                self.new_node(0)                                       # the root

            def new_node(self, d):
                self.levels[d] += [[None, -1, None] for _ in range(1 << self.s)]
                return (len(self.levels[d]) >> self.s) - 1

            def chunk(self, value, d):
                return value >> (self.w - (d + 1) * self.s) & ((1 << self.s) - 1)   # (1)!

            def insert(self, value, k, hop):
                value &= mask(k, self.w)                               # (2)!
                steps = max(1, -(-k // self.s))                        # (3)!
                n = 0
                for d in range(steps - 1):
                    e = self.levels[d][(n << self.s) + self.chunk(value, d)]
                    if e[2] is None:
                        e[2] = self.new_node(d + 1)
                    n = e[2]
                base = (n << self.s) + self.chunk(value, steps - 1)
                for j in range(1 << (steps * self.s - k)):             # (4)!
                    e = self.levels[steps - 1][base + j]
                    if k >= e[1]:                                      # (5)!
                        e[0], e[1] = hop, k

            def lookup(self, addr):
                n, best = 0, None
                for d in range(len(self.levels)):
                    hop, _, child = self.levels[d][(n << self.s) + self.chunk(addr, d)]
                    if hop is not None:
                        best = hop
                    if child is None:
                        break
                    n = child
                return best

            def entries(self):
                return sum(len(level) for level in self.levels)
        ```

        1. ‏\( s \) הביטים של רמה \( d \), מהעליונים : המספר של הכניסה בתוך הצומת.
        2. בלי הנרמול, ‏<span dir="ltr">10.1.2.3/16</span> עם \( s = 8 \) הייתה מתחילה את ההרחבה בכניסה 1
           של צומת <span dir="ltr">10.1</span>, כי הביטים 2 ו-3 נשארו בה, ומפספסת את רוב הכניסות.
        3. ‏\( \lceil k / s \rceil \) רמות, ולפחות אחת : ‏/0 נכתבת בשורש.
        4. ‏\( 2^{L - k} \) כניסות רצופות : הביטים שהקידומת לא קובעת עוברים על כל הערכים.
        5. כניסה ריקה מחזיקה אורך <span dir="ltr">−1</span>. אורך גדול יותר שכבר בכניסה נשאר, ולכן
           הסדר שבו נוספו השורות לא משנה. אורך שווה הוא אותה קידומת, והמאוחרת גוברת.

    === "SystemVerilog"
        ```systemverilog title="class mtrie" linenums="1" hl_lines="25 26 33 34 35 45"
        typedef struct { int hop, len, child; } mentry_t;   // -1: no hop, no prefix, no child

        // A multibit trie: s bits a step, w / s levels; lv[d] holds the nodes of depth d one
        // after another, f = 2^s entries each
        class mtrie;
          int w, s, f;
          mentry_t lv[32][$];

          function new(int w = 32, int s = 8);
            this.w = w; this.s = s; f = 1 << s;
            void'(new_node(0));
          endfunction

          function int new_node(int d);
            mentry_t e = '{-1, -1, -1};
            repeat (f) lv[d].push_back(e);
            return lv[d].size() / f - 1;
          endfunction

          function int chunk(logic [31:0] v, int d);
            return int'((v >> (w - (d + 1) * s)) & (f - 1));
          endfunction

          function void insert(logic [31:0] value, int k, int hop);
            int steps = k == 0 ? 1 : (k + s - 1) / s, n = 0, base;
            value &= prefix_mask(k, w);
            for (int d = 0; d < steps - 1; d++) begin
              base = n * f + chunk(value, d);
              if (lv[d][base].child < 0) lv[d][base].child = new_node(d + 1);
              n = lv[d][base].child;
            end
            base = n * f + chunk(value, steps - 1);
            for (int j = 0; j < (1 << (steps * s - k)); j++)
              if (k >= lv[steps - 1][base + j].len) begin
                lv[steps - 1][base + j].hop = hop;
                lv[steps - 1][base + j].len = k;
              end
          endfunction

          function int lookup(logic [31:0] addr);
            int n = 0, best = -1;
            mentry_t e;
            for (int d = 0; d < w / s; d++) begin
              e = lv[d][n * f + chunk(addr, d)];
              if (e.hop >= 0) best = e.hop;
              if (e.child < 0) break;
              n = e.child;
            end
            return best;
          endfunction

          function int entries();
            int sum = 0;
            foreach (lv[d]) sum += lv[d].size();
            return sum;
          endfunction
        endclass
        ```

    #### למה זה נכון { .sol-proof }

    **אותן כתובות.** קידומת \( p \) באורך \( k \) מתאימה לכתובת בדיוק כשאחת מ-\( 2^{L-k} \)
    ההרחבות שלה מתאימה לה : ההרחבות עוברות על כל הערכים של הביטים \( k \) עד \( L - 1 \), ולכן
    בדיוק אחת מהן שווה לכתובת בביטים האלה.

    **הארוכה נשארת.** כל כניסה בעץ מחזיקה, מבין הקידומות שהרחיבו אליה, את בעלת \( k \) הגדול ביותר,
    בכל סדר של הוספות, כי כל הוספה משווה את \( k \) שלה למה שכבר בכניסה. זו בדיוק הקידומת
    שהסריקה הייתה בוחרת מתוכן.

    **רמה אחרי רמה.** הכניסות בעומק \( d \) על הדרך של הכתובת מחזיקות קידומות שאורכן המקורי
    בין \( (d - 1)s + 1 \) ל-\( ds \), ו-/0 בשורש. לכן קפיצה בעומק גדול יותר תמיד באה מקידומת
    ארוכה יותר, והחיפוש יכול להחליף את הטובה בכל קפיצה שהוא פוגש, כמו בעץ הביטים.

    **נסו בעצמכם.** אותה תיבה, בצעד של שני ביטים. כל צומת הוא ארבע כניסות, וכניסה של קידומת
    שהורחבה מסומנת. בכתובת 185 : החיפוש קורא ‏`10`, ‏`11` ו-`10`, ונעצר בכניסה ריקה בלי בן, עם B. שנו
    בשורה של A את <span dir="ltr">128/1</span> ל-<span dir="ltr">128/2</span> : עכשיו השורה
    היא ‏`10*`, ו-A כבר לא מורחבת לכניסה ‏`11`, שנשארת עם D.

    <div class="explorer" data-kind="lpmtrie" data-addr="185" data-stride="2"></div>

    #### סיבוכיות { .sol-cost }

    **זמן.** חיפוש הוא \( W / s \) קריאות. הוספה יורדת באותו מספר רמות וכותבת עד \( 2^{s - 1} \)
    כניסות, או \( 2^s \) ל-/0.

    **זיכרון.** צומת עולה \( 2^s \) כניסות גם כשרק אחת מהן בשימוש. במקרה הגרוע כל קידומת יוצרת
    \( W / s \) צמתים משלה : \( O(N \cdot (W / s) \cdot 2^s) \). זה הסחר : ‏\( s \) גדול מקצר את
    החיפוש ומנפח את הזיכרון. נתבים אמיתיים בוחרים צעדים שונים לרמות שונות, למשל 16, 8 ו-8.

    **מחיקה.** כאן היא לא רק ניקוי של קפיצה : הכניסות של הקידומת שנמחקה צריכות לקבל את הקידומת
    הקצרה יותר שמכסה אותן, אם יש כזו. לכן שומרים לצד העץ את רשימת השורות המקוריות, ואת הכניסות של
    הקידומת שנמחקה כותבים מחדש מהקידומת הארוכה ביותר שעוד מכסה אותן.

---

### סעיף ד – חיפוש בחומרה, אחד בכל שעון

תכננו בחומרה את החיפוש של סעיף ג : כתובת חדשה נכנסת בכל שעון, וכל כתובת יוצאת עם הקפיצה שלה
אחרי מספר קבוע של שעונים. כתבו מודול RTL עם רוחב כתובת ורוחב צעד כפרמטרים, ותארו איך מאמתים
אותו.

??? tip "רמז 1"
    החיפוש של סעיף ג הוא \( W / s \) קריאות, אחת מכל רמה, וכל אחת תלויה בקודמת. איך עושים \( W / s \)
    קריאות בשעון אחד בלי לחכות?

??? tip "רמז 2"
    שימו כל רמה בזיכרון משלה, ושלב של צנרת לכל רמה. מה צריך לעבור מכל שלב לבא אחריו כדי שהוא
    יוכל להמשיך את החיפוש לבד?

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        **שלב לכל רמה, וזיכרון לכל שלב.** שלב \( d \) קורא כניסה אחת מהזיכרון של רמה \( d \), לפי
        הצומת שקיבל ו-\( s \) ביטים של הכתובת, ומעביר לשלב הבא ברגיסטרים את valid, הכתובת, הצומת
        הבא, האם עוד יורדים, והקפיצה הטובה עד עכשיו. כל שלב עובד על כתובת אחרת, ולכן נכנסת כתובת
        בכל שעון, וכל אחת יוצאת אחרי \( W / s \) שעונים. מאמתים מול הסריקה של סעיף א.

    <!-- cost: שלבים \( W/s \) | השהיה \( W/s \) שעונים | קצב 1 בשעון -->

    #### הרעיון { .sol-idea }

    בסעיף ג כל קריאה תלויה בקודמת, אבל רק בקודמת של **אותה** כתובת. אם לכל רמה יש זיכרון משלה,
    ‏\( W / s \) כתובות שונות יכולות לקרוא בו זמנית, כל אחת מרמה אחרת. כמו פס ייצור : כל שלב עושה
    צעד אחד של חיפוש ומעביר הלאה את כל מה שהשלב הבא צריך. ‏valid עובר עם הנתונים, ולכן שעון בלי
    כתובת הוא חור שעובר בצנרת ולא מבלבל אף שלב. הקפיצה הטובה עד עכשיו עוברת עם הכתובת, כמו ה-best
    של הקוד : אין צורך לחזור למעלה.

    <!-- gen 5 -->

    <svg class="figure lpm-pipe" viewBox="0 0 510 186" style="max-width:31.875rem" direction="ltr" role="img" aria-label="צנרת של 4 שלבים לכתובת של 8 ביטים, 2 ביטים בכל שלב : כל שלב קורא את הזיכרון של הרמה שלו, וברגיסטרים שלו עוברים לשלב הבא הכתובת, הצומת, הקפיצה הטובה עד עכשיו ו-valid"><rect class="lpm-stage" x="20" y="34" width="92" height="118" rx="6"/><text class="lpm-st-name" x="66.0" y="24" text-anchor="middle">stage 1</text><rect class="lpm-mem" x="30" y="46" width="72" height="40" rx="3"/><text class="lpm-mem-t" x="66.0" y="64" text-anchor="middle">level 0</text><text class="lpm-mem-s" x="66.0" y="79" text-anchor="middle">a[7:6]</text><rect class="lpm-reg" x="30" y="100" width="72" height="40" rx="3"/><text class="lpm-reg-t" x="66.0" y="117" text-anchor="middle">v a node</text><text class="lpm-reg-t" x="66.0" y="132" text-anchor="middle">go best</text><line class="lpm-wire" x1="66.0" y1="86" x2="66.0" y2="100"/><line class="lpm-wire lpm-arrow" x1="112" y1="120" x2="144" y2="120"/><path class="lpm-head" d="M144,120 l-7,-4 v8 z"/><rect class="lpm-stage" x="146" y="34" width="92" height="118" rx="6"/><text class="lpm-st-name" x="192.0" y="24" text-anchor="middle">stage 2</text><rect class="lpm-mem" x="156" y="46" width="72" height="40" rx="3"/><text class="lpm-mem-t" x="192.0" y="64" text-anchor="middle">level 1</text><text class="lpm-mem-s" x="192.0" y="79" text-anchor="middle">a[5:4]</text><rect class="lpm-reg" x="156" y="100" width="72" height="40" rx="3"/><text class="lpm-reg-t" x="192.0" y="117" text-anchor="middle">v a node</text><text class="lpm-reg-t" x="192.0" y="132" text-anchor="middle">go best</text><line class="lpm-wire" x1="192.0" y1="86" x2="192.0" y2="100"/><line class="lpm-wire lpm-arrow" x1="238" y1="120" x2="270" y2="120"/><path class="lpm-head" d="M270,120 l-7,-4 v8 z"/><rect class="lpm-stage" x="272" y="34" width="92" height="118" rx="6"/><text class="lpm-st-name" x="318.0" y="24" text-anchor="middle">stage 3</text><rect class="lpm-mem" x="282" y="46" width="72" height="40" rx="3"/><text class="lpm-mem-t" x="318.0" y="64" text-anchor="middle">level 2</text><text class="lpm-mem-s" x="318.0" y="79" text-anchor="middle">a[3:2]</text><rect class="lpm-reg" x="282" y="100" width="72" height="40" rx="3"/><text class="lpm-reg-t" x="318.0" y="117" text-anchor="middle">v a node</text><text class="lpm-reg-t" x="318.0" y="132" text-anchor="middle">go best</text><line class="lpm-wire" x1="318.0" y1="86" x2="318.0" y2="100"/><line class="lpm-wire lpm-arrow" x1="364" y1="120" x2="396" y2="120"/><path class="lpm-head" d="M396,120 l-7,-4 v8 z"/><rect class="lpm-stage" x="398" y="34" width="92" height="118" rx="6"/><text class="lpm-st-name" x="444.0" y="24" text-anchor="middle">stage 4</text><rect class="lpm-mem" x="408" y="46" width="72" height="40" rx="3"/><text class="lpm-mem-t" x="444.0" y="64" text-anchor="middle">level 3</text><text class="lpm-mem-s" x="444.0" y="79" text-anchor="middle">a[1:0]</text><rect class="lpm-reg" x="408" y="100" width="72" height="40" rx="3"/><text class="lpm-reg-t" x="444.0" y="117" text-anchor="middle">v a node</text><text class="lpm-reg-t" x="444.0" y="132" text-anchor="middle">go best</text><line class="lpm-wire" x1="444.0" y1="86" x2="444.0" y2="100"/><text class="lpm-io" x="20" y="176">in: valid, addr</text><text class="lpm-io" x="490" y="176" text-anchor="end">out: valid, hit, hop</text></svg>

    <!-- /gen -->

    כך עוברות בצנרת חמש כתובות של 8 ביטים, ‏\( s = 2 \), עם הטבלה הקטנה של סעיף ב. בכל תא הכתובת
    שבשלב והקפיצה הטובה עד עכשיו, ובשעון 3 לא נכנסה כתובת :

    <!-- gen 6 -->

    | שעון | נכנס | שלב 1 | שלב 2 | שלב 3 | שלב 4 |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | 1 | 185 | ‏<span dir="ltr">185 · A</span> | – | – | – |
    | 2 | 182 | ‏<span dir="ltr">182 · A</span> | ‏<span dir="ltr">185 · B</span> | – | – |
    | 3 | – | – | ‏<span dir="ltr">182 · B</span> | ‏<span dir="ltr">185 · B</span> | – |
    | 4 | 64 | ‏<span dir="ltr">64 · E</span> | – | ‏<span dir="ltr">182 · C</span> | **‏<span dir="ltr">185 · B</span>** |
    | 5 | 3 | ‏<span dir="ltr">3 · D</span> | ‏<span dir="ltr">64 · E</span> | – | **‏<span dir="ltr">182 · C</span>** |
    | 6 | – | – | ‏<span dir="ltr">3 · D</span> | ‏<span dir="ltr">64 · E</span> | – |
    | 7 | – | – | – | ‏<span dir="ltr">3 · D</span> | **‏<span dir="ltr">64 · E</span>** |
    | 8 | – | – | – | – | **‏<span dir="ltr">3 · D</span>** |

    <!-- /gen -->

    185 נכנסת בשעון 1 ויוצאת מהשלב הרביעי בסוף שעון 4 : ההשהיה היא 4 שעונים, שלב לכל רמה. כבר
    בשלב השלישי היא הפסיקה לרדת, כי לכניסה ‏`10` של הצומת 1011 אין בן, והשלב הרביעי רק מעביר
    אותה. 64 עוצרת כבר בשלב הראשון, עם E.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הזיכרונות :** רמה \( d \) בזיכרון משלה, \( N \) צמתים של \( 2^s \) כניסות. בכניסה :
       hop_ok והקפיצה, child_ok והבן, מספר הצומת ברמה הבאה. התוכנה ממלאת אותם דרך פתחת כתיבה, מתוך
       העץ של סעיף ג.
    2. **שלב \( d \) :** הכתובת של הכניסה היא הצומת שקיבל ואחריו \( s \) הביטים של הרמה. אם הוא
       עוד יורד והכניסה מחזיקה קפיצה, היא הטובה החדשה. הוא ממשיך לרדת רק אם יש לכניסה בן.
    3. **‏valid :** עובר שלב בכל שעון, עם איפוס. שאר הרגיסטרים בלי איפוס : בלי valid אף אחד לא
       מסתכל עליהם.
    4. **היציאה :** הרגיסטרים של השלב האחרון : out_valid, ‏out_hit, אם נמצאה קידומת, ו-out_hop.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="pipeline" linenums="1" hl_lines="13 14 15 16 19"
        def pipeline(t, inputs):
            """The pipeline of part d clock by clock, as the RTL: stage d reads level d of the
            MultiTrie t. inputs[c] is the address entering at clock c (None: no lookup). Per
            clock, the registers of every stage: None, or (address, best so far, walking)."""
            L, F = len(t.levels), 1 << t.s
            stages, trace = [None] * L, []
            for c in range(len(inputs) + L - 1):
                src = (inputs[c], 0, True, None) if c < len(inputs) and inputs[c] is not None else None
                new = []
                for d in range(L):
                    if src is not None:
                        addr, n, go, best = src
                        if go:                                           # (1)!
                            hop, _, child = t.levels[d][n * F + t.chunk(addr, d)]
                            best = best if hop is None else hop
                            go, n = child is not None, child if child is not None else 0
                        src = (addr, n, go, best)
                    new.append(src)
                    src = stages[d]                                      # (2)!
                stages = new
                trace.append([None if x is None else (x[0], x[3], x[2]) for x in stages])
            return trace
        ```

        1. שלב שכבר הפסיק לרדת רק מעביר את מה שקיבל. כך כל כתובת יוצאת אחרי אותו מספר שעונים,
           והסדר נשמר.
        2. השלב הבא מקבל את הרגיסטרים **הישנים** של השלב הזה, כמו בשעון של חומרה : כל השלבים
           מתעדכנים יחד.

    === "SystemVerilog"
        ```systemverilog title="module lpm_pipe" linenums="1" hl_lines="22 24 43 50 52 53"
        // The lookup in a pipeline: stage d holds level d of the multibit trie in its own memory
        // and reads it with s bits of the address; one lookup enters every clock, and each leaves
        // W / S clocks later with the best hop so far, carried down the pipe
        module lpm_pipe #(parameter int W = 8, S = 2, HW = 4, N = 8)   // address, stride, hop bits, nodes a level
          (input  logic                 clk, rst_n,
           input  logic                 in_valid,
           input  logic [W-1:0]         in_addr,
           input  logic                 wr_en,          // writes one entry of one level's memory
           input  int                   wr_level, wr_index,
           input  logic                 wr_hop_ok, wr_child_ok,
           input  logic [HW-1:0]        wr_hop,
           input  logic [$clog2(N)-1:0] wr_child,
           output logic                 out_valid, out_hit,
           output logic [HW-1:0]        out_hop);

          localparam int L = W / S, F = 1 << S, PW = $clog2(N);
          typedef struct packed {
            logic hop_ok; logic [HW-1:0] hop;                      // a prefix ends at this entry
            logic child_ok; logic [PW-1:0] child;                  // the node of the next level
          } entry_t;

          entry_t mem [L][N * F];                                  // (1)!
          always_ff @(posedge clk)
            if (wr_en) mem[wr_level][wr_index] <= {wr_hop_ok, wr_hop, wr_child_ok, wr_child};

          for (genvar d = 0; d < L; d++) begin : st
            logic          v, go, hit;                             // the registers of stage d
            logic [W-1:0]  a;
            logic [PW-1:0] p;
            logic [HW-1:0] hop;
            logic          iv, igo, ihit;                          // what enters stage d
            logic [W-1:0]  ia;
            logic [PW-1:0] ip;
            logic [HW-1:0] ihop;
            entry_t        e;

            if (d == 0) begin : first
              assign {iv, ia, ip, igo, ihit, ihop} = {in_valid, in_addr, PW'(0), 1'b1, 1'b0, HW'(0)};
            end else begin : next
              assign {iv, ia, ip, igo, ihit, ihop} = {st[d - 1].v, st[d - 1].a, st[d - 1].p,
                                                      st[d - 1].go, st[d - 1].hit, st[d - 1].hop};
            end
            assign e = mem[d][{ip, ia[W - 1 - d * S -: S]}];       // (2)!

            always_ff @(posedge clk or negedge rst_n)
              if (!rst_n) v <= 1'b0;
              else v <= iv;
            always_ff @(posedge clk) begin
              a   <= ia;
              go  <= igo && e.child_ok;
              p   <= e.child;
              hit <= ihit || (igo && e.hop_ok);
              hop <= igo && e.hop_ok ? e.hop : ihop;               // (3)!
            end
          end

          assign out_valid = st[L - 1].v;
          assign out_hit   = st[L - 1].hit;
          assign out_hop   = st[L - 1].hop;
        endmodule
        ```

        1. זיכרון לכל רמה, \( N \) צמתים של \( 2^S \) כניסות. כל שלב קורא רק מהזיכרון שלו, ולכן
           כל השלבים קוראים באותו שעון. כאן הקריאה צירופית. בזיכרון SRAM אמיתי הקריאה לוקחת שעון,
           והשלב נמשך שני שעונים, או שהכתובת שלו נשלחת כבר מהשלב הקודם.
        2. מספר הצומת ואחריו \( S \) הביטים של הרמה : זו בדיוק הכניסה \( p \cdot 2^S + \) chunk של
           הקוד ב-Python.
        3. הקפיצה הטובה עד עכשיו עוברת עם הכתובת. שלב שכבר לא יורד (`igo` הוא 0) מעביר אותה כמו
           שהיא.

    #### למה זה נכון { .sol-proof }

    **שלב הוא צעד.** בכל שעון שלב \( d \) מחשב מהרגיסטרים של שלב \( d - 1 \) בדיוק את הצעד ה-\( d \)
    של `lookup` בסעיף ג : אותה כניסה, אותו עדכון של הטובה, ואותה החלטה אם להמשיך. אחרי \( L \)
    שלבים הכתובת עברה את כל הצעדים, ולכן יוצאת עם התשובה של סעיף ג, שהיא התשובה של הסריקה.

    **בלי התנגשויות.** כל שלב קורא רק מהזיכרון של הרמה שלו ומחזיק כתובת אחת, ולכן \( L \) כתובות
    בצנרת לא מפריעות זו לזו. ‏valid שעובר עם הנתונים מסמן איזה שלב מחזיק כתובת אמיתית.

    **האימות.** הבודק בונה טבלאות אקראיות, ממלא מהן את הזיכרונות, ושולח כתובות אחת אחרי השנייה,
    עם חורים אקראיים. כל כתובת נכנסת לתור של ה-scoreboard עם התשובה של `lpm_naive`, וכל יציאה
    עם valid נבדקת מול ראש התור : ‏out_hit ו-out_hop מול התשובה, ושום יציאה לא חסרה או מיותרת.
    כתובות אקראיות כמעט אף פעם לא פוגעות בקידומת ארוכה, ולכן הבודק מוסיף כתובות מכוונות : הכתובת
    של כל קידומת, הכתובת שאחריה ושלפניה, וקידומות באורך \( W \). מוני כיסוי בודקים שהיו תשובות
    מ-/0, מקידומת באורך \( W \), מכתובת עם כמה קידומות מקוננות, ותשובות "אין" בטבלה בלי /0. אותו בודק
    מריץ \( s = 2 \) ו-\( s = 1 \) על 8 ביטים ו-\( s = 4 \) על 16 ביטים.

    #### סיבוכיות { .sol-cost }

    **‏8 ביטים, ‏\( s = 2 \) :** ארבעה שלבים, השהיה של 4 שעונים, וכתובת בכל שעון. בכל שלב זיכרון של
    \( 4N \) כניסות.

    **‏32 ביטים :** עם \( s = 8 \) ארבעה שלבים, ועם \( s = 4 \) שמונה. הקצב נשאר כתובת בשעון, וההשהיה
    היא מספר השלבים. הזיכרון של רמה \( d \) צריך לכל היותר \( \min(N, 2^{ds}) \) צמתים : השורש לבד
    ברמה 0, ובטבלה של מיליון קידומות רמה עמוקה מחזיקה מאות אלפי צמתים. לכן הרמה הראשונה היא לעתים
    טבלה אחת של \( 2^{16} \) או \( 2^{24} \) כניסות, ורק השאר עץ.

    **‏TCAM, הדרך האחרת :** זיכרון שבו כל שורה משווה את עצמה לכתובת, עם מסכה, באותו שעון. השורות
    ממוינות לפי אורך, והמקודד העדיפות (priority encoder) בוחר את המתאימה הראשונה. חיפוש בשעון אחד
    בלי צנרת, אבל כל שורה היא משווה, ולכן TCAM צורכת הרבה יותר הספק ושטח לביט מזיכרון רגיל.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : המסכה של /0"
    ‏`~0u << (32 - k)` ב-C נותן ב-\( k = 0 \) הזזה ב-32, שלא מוגדרת. מעבד x86 לוקח רק 5 ביטים של
    ההזזה, מזיז ב-0, ו-/0 מתאים רק לכתובת 0. ב-SystemVerilog ההזזה מוגדרת, אבל יש מלכודת אחרת :
    שדה אורך של 5 ביטים לא מחזיק 32, כי לאורך יש 33 ערכים, 0 עד 32. ‏`32 - k` בשדה של 5 ביטים
    הוא 0 ב-\( k = 0 \). צריך 6 ביטים, או בדיקה מפורשת של \( k = 0 \).

??? trap "מלכודת : קידומת שלא נורמלה"
    ‏<span dir="ltr">10.1.2.3/16</span> היא <span dir="ltr">10.1.0.0/16</span>. השוואה של
    <span dir="ltr">addr & mask == value</span> לא תתאים לה לעולם, כי ב-value נשארו ביטים מתחת
    למסכה, וההרחבה של סעיף ג תתחיל בכניסה הלא נכונה. מנרמלים כשמכניסים שורה לטבלה, או משווים
    עם XOR כמו בסעיף א.

??? trap "מלכודת : הארוכה נוספה קודם"
    בהרחבה של סעיף ג עם \( s = 8 \), אם <span dir="ltr">10.1.0.0/16</span> נוספה לפני <span dir="ltr">10.0.0.0/12</span>,
    ההרחבה של /12 עוברת על הכניסות של /16. בלי האורך המקורי בכל כניסה, השורה הקצרה דורסת את
    הארוכה, והתשובה תלויה בסדר שבו הטבלה נבנתה.

??? trap "מלכודת : מחיקה של צומת נחוץ"
    מחיקה של <span dir="ltr">10.0.0.0/8</span> מוחקת רק את הקפיצה מהצומת. אם מוחקים את הצומת עצמו,
    ‏<span dir="ltr">10.1.0.0/16</span> ו-<span dir="ltr">10.1.2.0/24</span> שמתחתיו נעלמות איתו.
    מנתקים רק צמתים בלי קפיצה ובלי בנים, מלמטה למעלה.

??? trap "מלכודת : סדר הבתים"
    ‏<span dir="ltr">10.1.2.3</span> הוא \( 10 \cdot 2^{24} + 1 \cdot 2^{16} + 2 \cdot 2^8 + 3 \) : המספר
    הראשון הוא הבית העליון, והביט הראשון של הקידומת הוא ביט 31. קריאה של ארבעת הבתים לתוך מספר
    במעבד little-endian הופכת את הסדר, וכל קידומת נבדקת על הבתים הלא נכונים.

??? followup "שאלות המשך"
    - **‏TCAM :** איך עושים את החיפוש בשעון אחד בלי עץ, ומה המחיר?

        ??? fu-answer "תשובה"
            כל שורה של ה-TCAM שומרת ערך ומסכה ומשווה את עצמה לכתובת, כולן באותו שעון. השורות
            ממוינות מהארוכה לקצרה, והמקודד העדיפות מחזיר את המתאימה הראשונה. המחיר : משווה לכל
            ביט, הספק גבוה בכל חיפוש, ושטח של פי כמה מ-SRAM. הוספה צריכה להזיז שורות כדי לשמור
            על הסדר.

    - **עדכון בזמן תנועה :** איך משנים את הטבלה בזמן שחיפושים עוברים בצנרת?

        ??? fu-answer "תשובה"
            בונים את השינוי בצמתים חדשים, שאף חיפוש עוד לא מגיע אליהם, וכותבים אחרון כניסה אחת
            ברמה העליונה שמחברת אותם. כל חיפוש רואה או את העץ הישן או את החדש. אחרי \( L \) שעונים
            אף חיפוש לא נמצא בצמתים הישנים, ומותר לשחרר אותם.

    - **‏IPv6 :** מה משתנה בכתובות של 128 ביטים?

        ??? fu-answer "תשובה"
            ‏\( W / s \) גדל פי 4 : ‏32 שלבים עם \( s = 4 \), או צעדים גדולים יותר ויותר זיכרון.
            בפועל הקידומות הן בעיקר עד /64, ולכן העץ עוצר מוקדם, והשלבים העמוקים כמעט ריקים.

    - **כמה קידומות לכל היותר :** מה מגביל את N בצנרת?

        ??? fu-answer "תשובה"
            הזיכרון של כל רמה : ‏\( N \) צמתים של \( 2^s \) כניסות. רמה \( d \) לא צריכה יותר
            מ-\( 2^{ds} \) צמתים, ולא יותר מאשר מספר הקידומות הארוכות מ-\( ds \) ביטים.
