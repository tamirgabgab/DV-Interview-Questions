---
id: 40
title: גלאי רצף 1011 עם חפיפה – מכונת מצבים
level: student
difficulty: easy
kind: design
tags: [digital-logic, fsm, systemverilog, python]
source: "שאלת ראיון קלאסית ל-RTL (HDLBits, Harris & Harris); ההכללה דרך האוטומט של KMP"
added: 2026-10-22
---

## השאלה

בכל מחזור שעון מגיע ביט אחד, `din`. תכננו מעגל שמוציא `found = 1` בכל מחזור שבו
**ארבעת הביטים האחרונים** הם `1011`, כולל חפיפה : בזרם `1011011` המוצא עולה פעמיים,
במחזור 4 ובמחזור 7, כי ה-`1` האחרון של הזיהוי הראשון הוא ה-`1` הראשון של הזיהוי השני.

ציירו את דיאגרמת המצבים, כתבו את המודול ב-SystemVerilog, והראו דיאגרמת תזמון על הזרם
שלמעלה.

??? interviewer "מה המראיין בודק"
    - **מה המצב מייצג :** האם המועמד מגדיר כל מצב כ"כמה מהתבנית כבר ראיתי", ולא כ"הביט
      האחרון".
    - **חפיפה :** כשביט שובר את ההתאמה, האם חוזרים להתחלה או למצב שמתאים לסיומת. זה
      ההבדל בין גלאי נכון לגלאי שמפספס.
    - **‏Mealy מול Moore :** באיזה מחזור המוצא עולה, וכמה מצבים צריך בכל אחת מהשיטות.
    - **איפוס ומוצא נקי :** מה המצב ההתחלתי, ומה קורה למוצא במחזור הראשון.
    - **הכללה :** האם יש דרך שיטתית לבנות את המכונה לכל תבנית, ולא רק בחשיבה ידנית.

---

### סעיף א – התבנית 1011

??? tip "רמז 1"
    המעגל צריך לזכור כמה מהתבנית כבר התאים : כלום, `1`, `10` או `101`. לפני שהתבנית
    נגמרת יש רק ארבע אפשרויות כאלה, ולכן ארבעה מצבים.

??? tip "רמז 2"
    כשמגיע ביט שלא מתאים, לא תמיד חוזרים להתחלה. אחרי `101` מגיע `0` : הביטים האחרונים
    הם `1010`, והם מסתיימים ב-`10`, שהוא התחלה של התבנית. לאיזה מצב עוברים?

??? tip "רמז 3"
    הפלט במכונת Mealy תלוי במצב **ובביט** : במצב `101` עם `1` נכנס מוציאים 1. לאיזה מצב
    עוברים אחר כך, אם רוצים לזהות גם את ההתאמה החופפת?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ארבעה מצבים, לפי מה שנראה עד כה : `S0` (כלום), `S1` (`1`), `S2` (`10`) ו-`S3`
        (`101`). ‏`found = (state == S3) & din`, ואחרי זיהוי עוברים ל-`S1`, כי ה-`1`
        האחרון כבר יכול לפתוח התאמה חדשה. מ-`S3` עם `0` עוברים ל-`S2`, כי `1010` מסתיים
        ב-`10`.

    <!-- cost: פלופים 2 | השהיה שער אחד -->

    #### הרעיון { .sol-idea }

    המצב מקודד **כמה ביטים מהתחלת התבנית מסתיימים ברגע זה**. ברגע שמגיע ביט, שואלים
    שאלה אחת : מה הסיומת הארוכה ביותר של "מה שראיתי" שהיא תחילת התבנית? אם הביט מתאים,
    מתקדמים מצב אחד. אם לא, לא בהכרח חוזרים ל-`S0` : ייתכן שסיומת קצרה יותר עדיין
    מתאימה. זה בדיוק מה שנותן את החפיפה בלי שום מנגנון נוסף.

    המוצא הוא מסוג **Mealy** : הוא תלוי במצב ובביט הנוכחי, ולכן עולה **באותו מחזור** שבו
    הביט הרביעי מגיע. המכונה בשלבים, ליד הצעדים.

    #### השלבים { .sol-steps }

    <div class="steps-fig" data-fig-steps='["n0 n1 n2 n3", "e0-1-1 e1-0-2 e2-1-3", "e0-0-0 e1-1-1 e2-0-0 e3-0-2", "e3-1-1 n3 n1", "n0", "e0-1-1 n1>e1-0-2 n2>e2-1-3 n3>e3-1-1 n1>e1-0-2 n2>e2-1-3 n3>e3-1-1 n1"]' markdown>

    <div class="sf-fig" markdown>

    <!-- gen 0 -->

    <svg class="figure fs-fig" viewBox="0 0 660 240" style="max-width:41rem" role="img" aria-label="דיאגרמת המצבים של גלאי 1011 : 4 מצבים, הקשתות מסומנות בביט ובפלט"><defs><marker id="fs-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs><path class="fs-edge" data-fig="e0-0-0" d="M60.0,96 C36.0,48 104.0,48 80.0,94" marker-end="url(#fs-arrow)"/><line class="fs-edge" data-fig="e0-1-1" x1="96.0" y1="118" x2="215.3" y2="118" marker-end="url(#fs-arrow)"/><line class="fs-edge" data-fig="e1-0-2" x1="269.3" y1="118" x2="388.7" y2="118" marker-end="url(#fs-arrow)"/><path class="fs-edge" data-fig="e1-1-1" d="M233.3,96 C209.3,48 277.3,48 253.3,94" marker-end="url(#fs-arrow)"/><path class="fs-edge" data-fig="e2-0-0" d="M416.7,144 Q243.3,222 70.0,146" marker-end="url(#fs-arrow)"/><line class="fs-edge" data-fig="e2-1-3" x1="442.7" y1="118" x2="562.0" y2="118" marker-end="url(#fs-arrow)"/><path class="fs-edge" data-fig="e3-0-2" d="M590.0,144 Q503.3,200 416.7,146" marker-end="url(#fs-arrow)"/><path class="fs-edge is-found" data-fig="e3-1-1" d="M590.0,144 Q416.7,222 243.3,146" marker-end="url(#fs-arrow)"/><g class="fs-node is-start" data-fig="n0"><circle cx="70.0" cy="118" r="26"/><text x="70.0" y="123" text-anchor="middle">S0</text></g><text class="fs-meaning" data-fig="n0" x="70.0" y="160" text-anchor="middle">start</text><g class="fs-node" data-fig="n1"><circle cx="243.3" cy="118" r="26"/><text x="243.3" y="123" text-anchor="middle">S1</text></g><text class="fs-meaning" data-fig="n1" x="243.3" y="160" text-anchor="middle">1</text><g class="fs-node" data-fig="n2"><circle cx="416.7" cy="118" r="26"/><text x="416.7" y="123" text-anchor="middle">S2</text></g><text class="fs-meaning" data-fig="n2" x="416.7" y="160" text-anchor="middle">10</text><g class="fs-node" data-fig="n3"><circle cx="590.0" cy="118" r="26"/><text x="590.0" y="123" text-anchor="middle">S3</text></g><text class="fs-meaning" data-fig="n3" x="590.0" y="160" text-anchor="middle">101</text><text class="fs-label halo" data-fig="e0-0-0" x="70.0" y="60" text-anchor="middle">0</text><text class="fs-label halo" data-fig="e0-1-1" x="156.7" y="110" text-anchor="middle">1</text><text class="fs-label halo" data-fig="e1-0-2" x="330.0" y="110" text-anchor="middle">0</text><text class="fs-label halo" data-fig="e1-1-1" x="243.3" y="60" text-anchor="middle">1</text><text class="fs-label halo" data-fig="e2-0-0" x="243.3" y="199.0" text-anchor="middle">0</text><text class="fs-label halo" data-fig="e2-1-3" x="503.3" y="110" text-anchor="middle">1</text><text class="fs-label halo" data-fig="e3-0-2" x="503.3" y="188.0" text-anchor="middle">0</text><text class="fs-label is-found halo" data-fig="e3-1-1" x="416.7" y="199.0" text-anchor="middle">1 / 1</text><text class="legend" x="652" y="232" text-anchor="end">1011, Mealy</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="fs-key"></i>מעבר : הביט שמתקבל</span><span><i class="fs-key-found"></i>המעבר שמזהה : הביט / הפלט 1</span></span>

    <!-- /gen -->

    </div>

    <div class="steps" markdown>

    1. **המצבים :** ‏`S0` כלום, `S1` ראינו `1`, `S2` ראינו `10`, `S3` ראינו `101`.
    2. **התקדמות :** מ-`S0` עם `1` ל-`S1`, מ-`S1` עם `0` ל-`S2`, מ-`S2` עם `1` ל-`S3`.
    3. **נסיגה :** ‏`S0` עם `0` נשאר; `S1` עם `1` נשאר (`11` מסתיים ב-`1`); `S2` עם `0`
       חוזר ל-`S0` (`100` לא מסתיים בשום התחלה); `S3` עם `0` ל-`S2` (`1010` מסתיים ב-`10`).
    4. **זיהוי :** ‏`S3` עם `1` מוציא 1 ועובר ל-`S1`, כי `1011` מסתיים ב-`1`.
    5. **איפוס :** המצב ההתחלתי `S0`, והמוצא נמוך בו.
    6. **דוגמה :** ‏`1011011`. אחרי `101` המכונה ב-`S3`, וה-`1` הרביעי מזהה (הפלט 1) ומחזיר
       ל-`S1`. ‏`0` ו-`1` מביאים שוב ל-`S3`, וה-`1` האחרון מזהה שוב : שני זיהויים, והשני משתמש
       ב-`1` האחרון של הראשון.

    </div>

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="detect_1011" hl_lines="2 11 12"
        # the next state per state and bit: (on 0, on 1); in Sk the last k bits are the first k of 1011
        NEXT_1011 = {"S0": ("S0", "S1"), "S1": ("S2", "S1"), "S2": ("S0", "S3"), "S3": ("S2", "S1")}   # (1)!


        def detect_1011(bits: list[int]) -> tuple[list[str], list[int]]:
            """The Mealy machine on a bit stream: the state before each bit, and the output per bit."""
            state, states, out = "S0", [], []
            for b in bits:
                states.append(state)
                out.append(int(state == "S3" and b == 1))   # (2)!
                state = NEXT_1011[state][b]
            return states, out
        ```

        1. אותה טבלת מעברים כמו ב-`case` של המודול.
        2. הפלט של Mealy : המצב `S3` (ראינו `101`) והביט `1` ביחד.

    === "SystemVerilog"
        ```systemverilog title="module seq_detect_1011" linenums="1" hl_lines="8 16 17"
        module seq_detect_1011 (
          input  logic clk,
          input  logic rst_n,
          input  logic din,
          output logic found
        );
          typedef enum logic [1:0] {S0, S1, S2, S3} state_t;   // (1)!
          state_t state, next;

          always_comb begin
            next  = state;
            found = 1'b0;
            case (state)
              S0: next = din ? S1 : S0;
              S1: next = din ? S1 : S2;
              S2: next = din ? S3 : S0;
              S3: begin found = din; next = din ? S1 : S2; end   // (2)!
            endcase
          end

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) state <= S0;
            else        state <= next;
        endmodule
        ```

        1. אותם שמות כמו בגרף ובטבלאות : במצב `Sk` ‏k הביטים האחרונים הם k הראשונים של
           `1011` (‏`S2` ראה `10`, ‏`S3` ראה `101`). שני ביטים מספיקים לארבעה מצבים.
        2. הזיהוי : הפלט תלוי במצב ובביט (Mealy). עם `1` עוברים ל-`S1`, כי ה-`1` האחרון
           הוא גם ה-`1` הראשון של התאמה חופפת; עם `0` ל-`S2`, כי `1010` מסתיים ב-`10`.

    #### למה זה נכון { .sol-proof }

    **טבלת המעברים.** כל שורה היא מצב, וכל תא אומר לאן עוברים עם הביט הבא :

    <!-- gen 2 -->

    | המצב | מה נראה עד כה | הביט הבא 0 | הביט הבא 1 |
    |:-:|:-:|:-:|:-:|
    | ‏S0 | התחלה | ‏S0 | ‏S1 |
    | ‏S1 | ‏`1` | ‏S2 | ‏S1 |
    | ‏S2 | ‏`10` | ‏S0 | ‏S3 |
    | ‏S3 | ‏`101` | ‏S2 | ‏S1, **הפלט 1** |

    <!-- /gen -->

    **הזרם מהשאלה, ביט אחרי ביט.** אחרי הזיהוי הראשון במחזור 4 המכונה נמצאת ב-`S1`, ולכן
    `011` הבאים מספיקים לזיהוי השני במחזור 7 :

    <!-- gen 3 -->

    | מחזור | הביט | המצב לפני | המצב אחרי | הפלט |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏1 | ‏1 | ‏S0 | ‏S1 | ‏0 |
    | ‏2 | ‏0 | ‏S1 | ‏S2 | ‏0 |
    | ‏3 | ‏1 | ‏S2 | ‏S3 | ‏0 |
    | ‏4 | ‏1 | ‏S3 | ‏S1 | ‏**1** ✓ |
    | ‏5 | ‏0 | ‏S1 | ‏S2 | ‏0 |
    | ‏6 | ‏1 | ‏S2 | ‏S3 | ‏0 |
    | ‏7 | ‏1 | ‏S3 | ‏S1 | ‏**1** ✓ |

    <!-- /gen -->

    **המעגל.** המודול הוא שלושה בלוקים. לוגיקת המצב הבא (ה-`case` שב-`always_comb`)
    מחשבת את `next` מ-`state` ומ-`din`; רגיסטר המצב, שני פליפ-פלופים (ה-`always_ff`),
    שומר את `next` בכל עליית שעון; ולוגיקת המוצא מחשבת את `found`. ב-Mealy גם `din`
    נכנס ללוגיקת המוצא, ולכן יש מסלול צירופי מ-`din` ל-`found` בלי פליפ-פלופ באמצע :

    <!-- gen 6 -->

    <svg class="figure shw-fig shw-dp" viewBox="0 0 440 356" direction="ltr" style="max-width:27.5rem" role="img" aria-label="תרשים המלבנים של הגלאי : din נכנס ללוגיקת המצב הבא, שמחשבת את next משני ביטים. רגיסטר המצב, שני פליפ-פלופים על clk עם איפוס rst_n, שומר את next בעליית השעון, ו-state חוזר ללוגיקת המצב הבא ונכנס ללוגיקת המוצא. ב-Mealy גם din נכנס ישר ללוגיקת המוצא : found = (state == S3) & din, מסלול צירופי מ-din ל-found בלי פליפ-פלופ באמצע"><defs><marker id="shw-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="shw-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="shw-wlab" x="200" y="14" text-anchor="middle">din</text><path class="shw-wire" d="M200,20 L200,58" marker-end="url(#shw-hb)"/><path class="shw-wire shw-mealy" d="M200,38 L410,38 L410,285 L322,285" marker-end="url(#shw-hb)"/><circle class="shw-dot" cx="200" cy="38" r="3"/><text class="shw-wlab shw-mlab" x="404" y="160" text-anchor="end">Mealy</text><g class="shw-blk shw-logic"><rect x="80" y="60" width="240" height="50" rx="5"/><text x="200" y="82" text-anchor="middle">next-state logic</text><text class="shw-sub" x="200" y="99" text-anchor="middle">next = f(state, din)</text></g><path class="shw-wire" d="M200,110 L200,158" marker-end="url(#shw-hb)"/><text class="shw-wlab" x="208" y="140" text-anchor="start">next[1:0]</text><g class="shw-blk shw-reg"><rect x="110" y="160" width="180" height="50" rx="5"/><text x="200" y="182" text-anchor="middle">state register</text><text class="shw-sub" x="200" y="199" text-anchor="middle">2 D flip-flops</text></g><path class="shw-wire" d="M370,185 L292,185" marker-end="url(#shw-hb)"/><text class="shw-wlab" x="298" y="178" text-anchor="start">clk, rst_n</text><path class="shw-wire" d="M200,210 L200,258" marker-end="url(#shw-hb)"/><circle class="shw-dot" cx="200" cy="235" r="3"/><path class="shw-wire" d="M200,235 L40,235 L40,85 L78,85" marker-end="url(#shw-hb)"/><text class="shw-wlab" x="208" y="250" text-anchor="start">state[1:0]</text><g class="shw-blk shw-out"><rect x="80" y="260" width="240" height="50" rx="5"/><text x="200" y="282" text-anchor="middle">output logic</text><text class="shw-sub" x="200" y="299" text-anchor="middle">found = (state == S3) &amp; din</text></g><path class="shw-wire" d="M200,310 L200,343" marker-end="url(#shw-hb)"/><text class="shw-wlab" x="208" y="338" text-anchor="start">found</text></svg>

    <!-- /gen -->

    <!-- gen 7 -->

    <span class="viz-legend"><span><i class="shw-key-reg"></i>רגיסטר המצב : פליפ-פלופים</span><span><i class="shw-key-logic"></i>לוגיקה צירופית</span><span><i class="shw-key-mealy"></i>‏din → found : מסלול צירופי, רק ב-Mealy</span></span>

    <!-- /gen -->

    **דיאגרמת התזמון.** ‏`din` נדגם בעליית השעון, המצב מתעדכן אחריה, ו-`found` הוא
    צירופי : הוא עולה באותו מחזור שבו הביט הרביעי נמצא על הקו. השורה `found_moore` היא
    אותו גלאי ב-Moore, עם המצב החמישי `S4` של סעיף ב : הפלט שלו יוצא מהמצב בלבד, ולכן
    הוא עולה מחזור אחד אחרי `found`, במחזורים 5 ו-8. במחזור 8 לא מגיע ביט חדש (x),
    ו-`found_moore` עולה בו בכל זאת :

    ```wavedrom
    { signal: [
      { name: "clk",   wave: "p........" },
      { name: "din",   wave: "x101.01.x" },
      { name: "state", wave: "=========", data: ["S0", "S0", "S1", "S2", "S3", "S1", "S2", "S3", "S1"] },
      { name: "found", wave: "0...10.10" },
      { name: "found_moore", wave: "0....10.1" }
    ]}
    ```

    **נסו בעצמכם.** התיבה מריצה את המעגל שבתרשים שעון אחרי שעון. הקלידו `101011` : ב-`S3`
    מגיע `0`, המכונה עוברת ל-`S2` ולא ל-`S0`, ו-`found` עולה בשעון 6. עברו ל-Moore :
    ‏`found` עולה שעון אחד מאוחר יותר, ורגיסטר המצב צריך שלושה פליפ-פלופים. ב-`1011011`
    שימו לב לשעונים 4 ו-7 : ‏`din` הוא שמחליט על `found` באותו שעון. מעבר לתרשים ולדיאגרמת
    התזמון, התיבה מראה את הערך בכל חוט ובכל בלוק בשעון הנבחר, את הביטים של המצב שמתהפכים,
    וטבלה של כל האותות, עמודה לכל שעון :

    <div class="explorer" data-kind="seqhw" data-bits="1011011"></div>

    **למה החפיפה נכונה.** ב-`1011011` הזיהוי השני משתמש ב-`1` האחרון של הראשון. מי שחוזר
    ל-`S0` אחרי זיהוי יראה אחריו `011`, שאינם `1011`, ויפספס. המעבר ל-`S1` אומר בדיוק
    "ראיתי `1`", וזה כל מה שצריך לזכור.

    **למה לא יותר מצבים.** המצב הוא הסיומת הארוכה ביותר של הקלט שהיא תחילת התבנית. לפני
    זיהוי יש ארבע סיומות כאלה (באורך 0 עד 3), ואחרי זיהוי הסיומת `1011` עצמה שקולה
    ל-`1` לכל המשך אפשרי, ולכן לא צריך לה מצב משלה. זו הסיבה שמכונת Mealy מסתפקת
    בארבעה מצבים.

    #### סיבוכיות { .sol-cost }

    חומרה : שני פלופים למצב, וכמה שערים ללוגיקת המעבר והפלט. אין רגיסטר הזזה ואין
    משווה של ארבעה ביטים. הנתיב הצירופי מ-`din` ל-`found` הוא שער אחד, ולכן המוצא
    יכול להגיע ל"גליץ'" רגעי אם `din` לא יציב; מוצא רשום (Moore) פותר את זה במחיר
    מחזור אחד.

---

### סעיף ב – כל תבנית : הבנייה השיטתית, ‏Mealy מול Moore

כתבו קוד שבונה את המכונה **לכל תבנית** נתונה, כפרמטר, ומריץ אותה על זרם ביטים. כמה
מצבים צריך לתבנית באורך \( L \) ב-Mealy וב-Moore, ואיך מוצאים את מעברי הנסיגה בלי
לחשוב על כל מקרה בנפרד?

??? tip "רמז 1"
    מצב \( s \) פירושו "ה-\( s \) הביטים האחרונים הם ה-\( s \) הראשונים של התבנית". מה
    קורה כשהביט הבא לא מתאים לביט מספר \( s \) של התבנית?

??? tip "רמז 2"
    מורידים את הביט הראשון מהסיומת שהתאימה, ושואלים את אותה שאלה על סיומת קצרה יותר.
    זה בדיוק ה"כישלון" של KMP, ואפשר לחשב אותו מצב אחרי מצב.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        המצבים הם \( 0 \) עד \( L \) : "כמה מהתבנית מסתיים עכשיו". ‏\( next[s][b] = s + 1 \)
        אם \( b \) הוא הביט ה-\( s \) של התבנית, ואחרת \( next[fail(s)][b] \), כאשר
        \( fail(s) \) הוא המצב של הסיומת בלי הביט הראשון. ‏Moore צריך \( L + 1 \) מצבים
        (המצב \( L \) מוציא 1); Mealy מסתפק ב-\( L \), כי המצב \( L \) שקול ל-\( fail(L) \).

    <!-- cost: פלופים \( \lceil \log_2(L + 1) \rceil \) | בנייה \( O(L) \) | ריצה \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **המצב הוא סיומת.** אחרי כל ביט, המידע היחיד שמשפיע על העתיד הוא הסיומת הארוכה ביותר
    של הקלט שהיא תחילת התבנית. כל זיהוי עתידי מתחיל באחת מהסיומות של הקלט, וסיומת
    שאינה תחילת התבנית לא תוביל לזיהוי. לכן \( L + 1 \) מצבים מספיקים לכל תבנית.

    **הכישלון.** במצב \( s \) מגיע ביט \( b \) שלא מתאים. הסיומת שהתאימה היא
    \( P[0..s-1] \); מורידים ממנה את הביט הראשון ושואלים לאיזה מצב \( P[1..s-1] \) מביא.
    זה \( fail(s) \), ואז \( next[s][b] = next[fail(s)][b] \). את \( fail(s + 1) \)
    מחשבים מ-\( fail(s) \) באותה טבלה : \( fail(s + 1) = next[fail(s)][P[s]] \). כך
    הטבלה נבנית בשורה אחת של לולאה, בלי לחשוב על אף מקרה ביד : זה האוטומט של
    Knuth–Morris–Pratt.

    **הכישלון על 1011, שורה אחרי שורה.** כל שורה מחשבת את \( fail \) מהשורה הקודמת,
    והביט שלא מתאים הולך לאן שהולך מצב הכישלון עם אותו ביט. יוצא \( fail = 0, 0, 1, 1 \) :

    <!-- gen 8 -->

    | המצב | התאים | בלי הביט הראשון | ‏fail | איך מקבלים את fail | הביט שלא מתאים |
    |:-:|:-:|:-:|:-:|---|---|
    | ‏S1 | ‏`1` | ריק | ‏0 | התחלה : שום ביט | ‏`1 → next[0][1] = 1` |
    | ‏S2 | ‏`10` | ‏`0` | ‏0 | ‏`next[0][P[1]] = next[0][0]` | ‏`0 → next[0][0] = 0` |
    | ‏S3 | ‏`101` | ‏`01` | ‏1 | ‏`next[0][P[2]] = next[0][1]` | ‏`0 → next[1][0] = 2` |
    | ‏S4 | ‏`1011` | ‏`011` | ‏1 | ‏`next[1][P[3]] = next[1][1]` | שניהם, כמו ב-‏`S1` : `next[4] = next[1]` |

    <!-- /gen -->

    השורה של `S3` היא החפיפה של סעיף א : בלי הביט הראשון, `101` הופך ל-`01`, שמביא
    ל-`S1`, ו-`S1` עם `0` הולך ל-`S2`. לכן אחרי `1010` המכונה ב-`S2` ולא ב-`S0`.

    **‏Mealy מול Moore.** ב-Moore הפלט שייך למצב, ולכן צריך מצב \( L \) ("התבנית הסתיימה")
    שמוציא 1, והמוצא עולה **מחזור אחד אחרי** הביט האחרון. ב-Mealy הפלט שייך למעבר
    שנכנס למצב \( L \), ועוד באותו מחזור; ואחרי המעבר לא צריך את המצב \( L \) עצמו, כי
    המעברים ממנו זהים למעברים מ-\( fail(L) \). לכן Mealy חי עם \( L \) מצבים.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מצב 0 :** עם הביט הראשון של התבנית ל-1, אחרת נשאר ב-0.
    2. **מצב אחרי מצב :** ל-\( s = 1, \dots, L \), ולכל ביט : התקדמות אם מתאים, ואחרת
       \( next[fail][b] \).
    3. **הכישלון הבא :** ‏\( fail \leftarrow next[fail][P[s]] \), בלי לחשב סיומות ביד.
    4. **הריצה :** ב-Moore הפלט הוא \( state = L \); ב-Mealy הפלט הוא \( next = L \),
       והמצב החדש הוא \( fail(L) \) במקום \( L \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="fsm_table, run_fsm" linenums="1" hl_lines="6 8 10 17 22 23"
        def fsm_table(pattern: list[int]) -> list[list[int]]:
            """nxt[s][b] of the KMP automaton: state s means "the last s bits are the first s of the pattern"."""
            L = len(pattern)
            nxt = [[0, 0] for _ in range(L + 1)]
            nxt[0][pattern[0]] = 1
            fail = 0                                                        # (1)!
            for s in range(1, L + 1):
                for b in (0, 1):
                    nxt[s][b] = s + 1 if s < L and pattern[s] == b else nxt[fail][b]   # (2)!
                if s < L:
                    fail = nxt[fail][pattern[s]]                            # (3)!
            return nxt


        def run_fsm(pattern: list[int], bits: list[int], moore: bool = False) -> tuple[list[int], list[int]]:
            """The state before every bit and the output per bit; Mealy merges the full-match state into its equivalent."""
            L, nxt = len(pattern), fsm_table(pattern)
            rest = next(s for s in range(L) if nxt[s] == nxt[L])          # (4)!
            state, states, out = 0, [], []
            for b in bits:
                states.append(state)
                nstate = nxt[state][b]
                out.append(int(state == L) if moore else int(nstate == L))   # (5)!
                state = nstate if moore or nstate < L else rest
            return states, out
        ```

        1. ‏`fail` הוא מצב הכישלון של המצב הנוכחי.
        2. התקדמות על התאמה, ואחרת המעבר של מצב הכישלון עם אותו ביט.
        3. הכישלון של המצב הבא, מהטבלה שכבר קיימת.
        4. ‏Mealy : המצב ששקול למצב המלא, זה עם אותם שני מעברים. תמיד קיים, כי
           \( next[L] = next[fail(L)] \).
        5. ‏Moore מוציא מהמצב, מחזור אחרי הביט האחרון; Mealy מוציא על המעבר.

    === "SystemVerilog"
        ```systemverilog title="module seq_detect (any pattern)" linenums="1" hl_lines="15 19 20 38 43"
        module seq_detect #(
          parameter int L = 4,
          parameter bit [0:L-1] PATTERN = 4'b1011,   // PATTERN[0] arrives first
          parameter bit MOORE = 0
        ) (
          input  logic clk,
          input  logic rst_n,
          input  logic din,
          output logic found
        );
          // The KMP automaton: state s means "the last s bits are the first s of the pattern";
          // next_state(s, b) is s + 1 on a match, else the state of the same suffix without its first bit.
          function automatic int next_state(int s, bit b);
            int nxt[L + 1][2];
            int fail = 0;                                               // (1)!
            nxt[0][0] = 0; nxt[0][1] = 0; nxt[0][PATTERN[0]] = 1;
            for (int i = 1; i <= L; i++) begin
              for (int c = 0; c < 2; c++)
                nxt[i][c] = (i < L && PATTERN[i] == bit'(c)) ? i + 1 : nxt[fail][c];   // (2)!
              if (i < L) fail = nxt[fail][PATTERN[i]];                // (3)!
            end
            return nxt[s][b];
          endfunction

          // the Mealy machine merges the full-match state into the state with the same transitions
          function automatic int rest();
            for (int s = 0; s < L; s++)
              if (next_state(s, 1'b0) == next_state(L, 1'b0) && next_state(s, 1'b1) == next_state(L, 1'b1)) return s;
            return 0;
          endfunction

          localparam int W = $clog2(L + 1);
          logic [W-1:0] state;
          int nstate;

          always_comb begin
            nstate = next_state(int'(state), din);
            found  = MOORE ? (int'(state) == L) : (nstate == L);         // (4)!
          end

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) state <= '0;
            else        state <= W'((!MOORE && nstate == L) ? rest() : nstate);   // (5)!
        endmodule
        ```

        1. ‏`fail` הוא מצב הכישלון של המצב הנוכחי : לאן מביאה אותה סיומת בלי הביט הראשון.
        2. התקדמות על התאמה, ואחרת המעבר של מצב הכישלון עם אותו ביט.
        3. הכישלון של המצב הבא מחושב מהכישלון הנוכחי, בטבלה שכבר קיימת.
        4. ‏Moore : הפלט שייך למצב `L`; Mealy : הפלט שייך למעבר שנכנס אליו, באותו מחזור.
        5. ב-Mealy המצב `L` לא קיים : אחרי זיהוי עוברים למצב השקול לו. הפונקציה היא
           פונקציית קבועים (הפרמטרים ידועים), וכלי סינתזה מקפל אותה לטבלה קבועה.

    #### למה זה נכון { .sol-proof }

    **המצב מספיק.** נניח שהקלט עד עכשיו הוא \( x \), והמצב \( s \) הוא אורך הסיומת
    הארוכה ביותר של \( x \) שהיא תחילת התבנית. לכל המשך \( y \), התבנית מופיעה בסוף
    \( xy \) בדיוק אם היא מופיעה בסוף \( P[0..s-1]\,y \) : תחילת ההופעה היא סיומת של
    \( x \) שהיא תחילת התבנית, ולכן באורך \( s \) לכל היותר, כלומר בתוך \( P[0..s-1] \).
    לכן המצב קובע את כל העתיד, ואין צורך לזכור יותר.

    **נוסחת הנסיגה.** אם \( b = P[s] \), הסיומת החדשה היא \( P[0..s] \) ואורכה \( s + 1 \).
    אחרת, הסיומת הארוכה ביותר של \( P[0..s-1]\,b \) שהיא תחילת התבנית קצרה מ-\( s + 1 \),
    ולכן היא סיומת של \( P[1..s-1]\,b \); והמצב של \( P[1..s-1] \) הוא בדיוק
    \( fail(s) \). מכאן \( next[s][b] = next[fail(s)][b] \), והכישלון הבא מתקבל מאותה
    טבלה : \( fail(s + 1) = next[fail(s)][P[s]] \), כי \( P[1..s] = P[1..s-1]\,P[s] \).

    **הדוגמאות.** לכל תבנית, מספר המצבים, המצב שאליו המצב המלא "נופל" (הסיומת הארוכה
    ביותר של התבנית שהיא גם תחילתה), והמעברים :

    <!-- gen 5 -->

    | התבנית | המצבים | כישלון של המצב המלא | מעברים (מהמצב, בביט 0 / בביט 1) |
    |:-:|:-:|:-:|---|
    | ‏`1011` | ‏4 ‏(Mealy), 5 ‏(Moore) | ‏S1 | ‏S0 : 0 / 1; S1 : 2 / 1; S2 : 0 / 3; S3 : 2 / 4 |
    | ‏`0110` | ‏4 ‏(Mealy), 5 ‏(Moore) | ‏S1 | ‏S0 : 1 / 0; S1 : 1 / 2; S2 : 1 / 3; S3 : 4 / 0 |
    | ‏`1111` | ‏4 ‏(Mealy), 5 ‏(Moore) | ‏S3 | ‏S0 : 0 / 1; S1 : 0 / 2; S2 : 0 / 3; S3 : 0 / 4 |
    | ‏`10101` | ‏5 ‏(Mealy), 6 ‏(Moore) | ‏S3 | ‏S0 : 0 / 1; S1 : 2 / 1; S2 : 0 / 3; S3 : 4 / 1; S4 : 0 / 5 |
    | ‏`1101` | ‏4 ‏(Mealy), 5 ‏(Moore) | ‏S1 | ‏S0 : 0 / 1; S1 : 0 / 2; S2 : 3 / 2; S3 : 0 / 4 |

    <!-- /gen -->

    **‏Moore לעומת Mealy על 1011.** אותה טבלה עם מצב חמישי שמוציא 1. שימו לב שהשורה של
    `S4` זהה לשורה של `S1` : זה המצב שאליו Mealy "נופל" אחרי זיהוי :

    <!-- gen 4 -->

    | המצב | מה נראה עד כה | הפלט | הביט הבא 0 | הביט הבא 1 |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏S0 | התחלה | ‏0 | ‏S0 | ‏S1 |
    | ‏S1 | ‏`1` | ‏0 | ‏S2 | ‏S1 |
    | ‏S2 | ‏`10` | ‏0 | ‏S0 | ‏S3 |
    | ‏S3 | ‏`101` | ‏0 | ‏S2 | ‏S4 |
    | ‏S4 | ‏`1011` | ‏1 | ‏S2 | ‏S1 |

    <!-- /gen -->

    **נסו בעצמכם.** הזינו `1011011` (הכפתור בדוגמאות) וספרו את הזיהויים : שניים, במחזורים
    4 ו-7. עברו ל-Moore : ‏`found` זז מחזור אחד, ל-5, והמכונה עוצרת ב-`S4`, שיוציא את
    הזיהוי השני במחזור 8. אחר כך הקלידו את התבנית `1111`, לחצו על "ניקוי" והזינו `11111` : שני זיהויים,
    במחזורים 4 ו-5, כי אחרי זיהוי המכונה נשארת ב-`S3`. מעבר לטבלאות, התיבה בונה את המכונה
    לכל תבנית שתקלידו, ומראה בכל מצב למה כל מעבר הולך לאן שהוא הולך : התבנית מוזזת מתחת
    לקלט עד ההתאמה הארוכה ביותר :

    <div class="explorer" data-kind="seqdet" data-pattern="1011"></div>

    #### סיבוכיות { .sol-cost }

    - **מצבים :** ‏\( L + 1 \) ב-Moore, \( L \) ב-Mealy, כלומר \( \lceil \log_2(L + 1) \rceil \)
      פלופים. רגיסטר הזזה עם משווה היה דורש \( L \) פלופים ומשווה של \( L \) ביטים.
    - **בניית הטבלה :** ‏\( O(L) \) צעדים, וכל צעד עולה \( O(1) \). בחומרה הטבלה היא
      קבועה שמחושבת בזמן הסינתזה.
    - **ריצה :** ‏\( O(1) \) לכל ביט, מעבר אחד בטבלה.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לחזור להתחלה אחרי אי-התאמה"
    מי שכותב "אם הביט לא מתאים, `next = S0`" מפספס חפיפות : אחרי `101` מגיע `0`, והקלט
    `1010` מסתיים ב-`10`, שהוא כבר חצי תבנית. בזרם `101011` הגלאי הנכון מזהה במחזור 6,
    וגלאי כזה לא מזהה כלום.

??? trap "מלכודת : רגיסטר הזזה שמתחיל מאפסים"
    החלופה "רגיסטר הזזה של 4 ביטים ומשווה ל-1011" נכונה, אבל אחרי איפוס הרגיסטר מלא
    אפסים : לתבנית `0000` הוא "יזהה" מיד, בלי שהגיע אף ביט. צריך מונה של ארבעה מחזורים
    או ביט תקפות. למכונת המצבים אין את הבעיה הזו, כי `S0` אומר "לא ראיתי כלום".

??? trap "מלכודת : לבלבל בין מחזור הפלט של Mealy ל-Moore"
    ב-Mealy ‏`found` עולה במחזור שבו הביט הרביעי על הקו; ב-Moore מחזור אחד אחריו. בדיקה
    שמצפה לאחד ומקבלת את השני תיכשל "באחד", וזו טעות תזמון קלאסית בטסטבנצ'ים.

??? trap "מלכודת : פלט צירופי שמגיע מ-din"
    ב-Mealy ‏`found` תלוי ישירות ב-`din`. אם `din` מגיע מדומיין אחר או עם גליץ'ים, גם
    `found` ירעד. רושמים את המוצא (ומקבלים Moore), או מוודאים ש-`din` סינכרוני ויציב.

??? followup "שאלות המשך"
    - **בלי חפיפה :** אחרי זיהוי חוזרים ל-`S0`. אילו שורות בטבלה משתנות, וכמה פעמים
      עולה המוצא על `1011011`?

        ??? fu-answer "תשובה"
            רק המעבר שמזהה משתנה : `S3` עם `1` עובר ל-`S0` במקום ל-`S1`. ב-`1011011` המוצא עולה
            פעם אחת, במחזור 4, כי ה-`1` האחרון של הזיהוי כבר לא פותח התאמה חדשה.

    - **שתי תבניות בבת אחת :** ‏`found_a` ל-`1011` ו-`found_b` ל-`0110` מאותו זרם. כמה
      מצבים צריך למכונה אחת שעושה את שניהם?

        ??? fu-answer "תשובה"
            מכפלת המכונות : המצב הוא זוג של מצבים, אחד לכל תבנית. ב-Moore יש לכל היותר
            \( 5 \cdot 5 \) זוגות, ובפועל רק 9 מהם ישיגים מ-\( (0, 0) \) : זה בדיוק מספר
            הצמתים של אוטומט אהו–קורסיק על שתי התבניות (כל ההתחלות של `1011` ושל `0110`,
            כולל הריקה). ב-Mealy כל מצב מלא מתמזג במצב השקול לו, ולכן מספיקים 7 מתוך
            \( 4 \cdot 4 \) : שני הזוגות עם מצב מלא, \( (4, 3) \) ו-\( (2, 4) \), נעלמים.

    - **אות תקפות :** ‏`din` תקף רק כש-`valid = 1`. איפה נכנס `valid` בקוד?

        ??? fu-answer "תשובה"
            כ-enable על הפלופ של המצב, כך שבמחזור לא תקף המצב לא זז, ו-`found` מסונן
            ב-`valid` כדי שלא יעלה על ביט לא תקף.

    - **בתים במקום ביטים :** אותה בנייה על אלפבית של 256 ערכים. מה גודל הטבלה, ואיך
      מצמצמים אותה?

        ??? fu-answer "תשובה"
            טבלה מלאה היא \( (L + 1) \cdot 256 \) כניסות. מצמצמים אותה ל-\( L + 1 \) כניסות של
            כישלון ומחשבים את המעבר בלולאה על \( fail \), כמו ב-KMP המקורי.

    - **סדר הביטים :** התבנית מגיעה LSB תחילה. מה משתנה?

        ??? fu-answer "תשובה"
            מחפשים את התבנית בסדר ההגעה, כלומר `1101`, ובונים לה מכונה באותה שיטה. בקוד הכללי
            משתנה רק הסדר שבו קוראים את `PATTERN`, אבל טבלת המעברים עצמה שונה מזו של `1011`.
