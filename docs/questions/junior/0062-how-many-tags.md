---
id: 62
title: כמה tags צריך – טרנזקציות חופפות, ומאגר אחד מול שניים
level: junior
difficulty: medium
kind: code
tags: [algorithms, sorting, protocols, python, systemverilog]
source: "Google ו-Meta (Meeting Rooms II), בלבוש של tags לטרנזקציות"
added: 2026-10-28
---

## השאלה

נתונה רשימה של טרנזקציות. לכל אחת זמן שליחה \( s_i \) וזמן תשובה \( e_i \), עם \( s_i < e_i \).
טרנזקציה פתוחה, מרגע השליחה ועד רגע התשובה, תופסת tag אחד, וברגע התשובה ה-tag משתחרר.
מה מספר ה-tags הקטן ביותר שמספיק כדי להריץ את כל הרשימה בלי לעכב אף שליחה?

דוגמה : לטרנזקציות 0 עד 30, ‏5 עד 10 ו-15 עד 20 מספיקים 2 tags.

**ההסכמה בזמנים שווים :** tag שמשתחרר ברגע \( t \) אפשר לתת לשליחה באותו \( t \). בראיון כדאי
לשאול את זה במפורש, כי בלי ההסכמה התשובה יכולה להיות גדולה באחד.

**ההקשר באימות :** מספר הטרנזקציות הפתוחות בו-זמנית (outstanding) קובע כמה tags או IDs
הסביבה צריכה, כמה כניסות ב-scoreboard מחכות לתשובה, ומה העומק של retry buffer. מטרייס של
הטרנזקציות אפשר לדעת את זה בדיוק.

- **סעיף א – מאגר אחד :** כתבו פונקציה שמחזירה את מספר ה-tags.
- **סעיף ב – שני מאגרים :** בפרוטוקול כמו AXI לקריאות ולכתיבות יש IDs נפרדים. כל טרנזקציה
  היא קריאה או כתיבה. כמה tags צריך כל מאגר, כמה צריך מאגר אחד משותף, ומה היחס ביניהם?

??? interviewer "מה המראיין בודק"
    - **מאירועים למונה :** האם המועמד רואה שכל טרנזקציה היא שני אירועים, ושהתשובה היא השיא של
      מונה, ולא מנסה לשבץ tags בפועל.
    - **המיון :** ‏\( O(n \log n) \), ומה קורה כששני אירועים נופלים על אותו רגע.
    - **ההכללה :** מאגר משותף אף פעם לא צריך יותר מסכום המאגרים הנפרדים, ולמה לפעמים הוא צריך
      פחות.
    - **הקשר לפרוטוקול :** outstanding transactions, מספר ה-IDs, עומק ה-scoreboard.

---

### סעיף א – מאגר אחד

??? tip "רמז 1"
    במקום לחשוב על טרנזקציות, חשבו על רגעים. בכל רגע, כמה טרנזקציות פתוחות? מה הקשר בין המספר
    הזה למספר ה-tags?

??? tip "רמז 2"
    המספר הפתוח משתנה רק בשליחה (עולה ב-1) ובתשובה (יורד ב-1). מיינו את כל האירועים לפי זמן
    ועברו עליהם עם מונה אחד.

<div class="selfcheck" data-answer="2" data-show="2 : ברגע 10 הראשונה סוגרת לפני שהשנייה פותחת, ולכן אף פעם לא שלוש יחד" data-hint="בכל רגע ספרו כמה פתוחות. ברגע 10 תשובה ושליחה נופלות יחד, והתשובה קודמת." markdown>
לטרנזקציות 0 עד 10, ‏10 עד 20 ו-5 עד 15, כמה tags צריך?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מפרקים כל טרנזקציה לשני אירועים, שליחה שמוסיפה 1 ותשובה שמורידה 1. ממיינים את כל
        האירועים לפי זמן (תשובה לפני שליחה באותו זמן) ועוברים עליהם עם מונה. השיא של המונה הוא
        מספר ה-tags : בדוגמה 2.

    <!-- cost: זמן \( O(n \log n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **כמה פתוחות בכל רגע.** בכל רגע, כל טרנזקציה פתוחה מחזיקה tag, ולכן צריך לפחות כמספר
    הפתוחות ברגע העמוס ביותר. והשיא הזה גם מספיק : כשמגיעה שליחה יש tag פנוי, כי אחרת היו
    יותר פתוחות מהשיא. בדוגמה :

    <!-- gen 0 -->

    <svg class="figure tp-fig" viewBox="0 0 640 208" role="img" aria-label="שלוש טרנזקציות : 0 עד 30, 5 עד 10 ו-15 עד 20, ומתחתן כמה פתוחות בכל רגע, לכל היותר 2"><line class="grid" x1="64" x2="64" y1="10" y2="178"/><text class="tick" x="64" y="106" text-anchor="middle">0</text><line class="grid" x1="157.333" x2="157.333" y1="10" y2="178"/><text class="tick" x="157.333" y="106" text-anchor="middle">5</text><line class="grid" x1="250.667" x2="250.667" y1="10" y2="178"/><text class="tick" x="250.667" y="106" text-anchor="middle">10</text><line class="grid" x1="344" x2="344" y1="10" y2="178"/><text class="tick" x="344" y="106" text-anchor="middle">15</text><line class="grid" x1="437.333" x2="437.333" y1="10" y2="178"/><text class="tick" x="437.333" y="106" text-anchor="middle">20</text><line class="grid" x1="530.667" x2="530.667" y1="10" y2="178"/><text class="tick" x="530.667" y="106" text-anchor="middle">25</text><line class="grid" x1="624" x2="624" y1="10" y2="178"/><text class="tick" x="624" y="106" text-anchor="middle">30</text><text class="tp-name" x="56" y="27" text-anchor="end">T1</text><rect class="tp-bar" x="64" y="14" width="560" height="16" rx="3"><title>T1: 0–30</title></rect><text class="tp-name" x="56" y="51" text-anchor="end">T2</text><rect class="tp-bar" x="157.333" y="38" width="93.3333" height="16" rx="3"><title>T2: 5–10</title></rect><text class="tp-name" x="56" y="75" text-anchor="end">T3</text><rect class="tp-bar" x="344" y="62" width="93.3333" height="16" rx="3"><title>T3: 15–20</title></rect><line class="axis" x1="64" x2="624" y1="92" y2="92"/><text class="tick" x="56" y="182" text-anchor="end">0</text><text class="tick" x="56" y="160" text-anchor="end">1</text><text class="tick" x="56" y="138" text-anchor="end">2</text><line class="tp-max" x1="64" x2="624" y1="134" y2="134"/><path class="tp-count" d="M64,178 H64 V156 H157.333 V134 H250.667 V156 H344 V134 H437.333 V156 H624 V178 H624"/><text class="legend" x="624" y="127" text-anchor="end">max = 2</text><text class="tp-name" x="56" y="124" text-anchor="end">open</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="tp-key-bar"></i>טרנזקציה פתוחה, מהשליחה עד התשובה</span><span><i class="tp-key-count"></i>כמה פתוחות בכל רגע</span><span><i class="tp-key-max"></i>המקסימום, מספר ה-tags</span></span>

    <!-- /gen -->

    **אירועים במקום רגעים.** המספר הפתוח משתנה רק בשליחה ובתשובה. לכן מספיק להסתכל על
    \( 2n \) האירועים, ממוינים לפי זמן, ולהחזיק מונה אחד : שליחה מוסיפה 1, תשובה מורידה 1,
    והשיא של המונה הוא התשובה. באותו רגע תשובה באה לפני שליחה, כי ה-tag שהשתחרר כבר פנוי.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שני אירועים לטרנזקציה :** ‏\( (s_i, +1) \) ו-\( (e_i, -1) \).
    2. **מיון :** לפי הזמן, ובזמן שווה קודם \( -1 \) ואז \( +1 \).
    3. **סריקה :** מונה שמתחיל ב-0, ומתעדכן בכל אירוע. השיא נשמר.
    4. **התשובה :** השיא. בדוגמה המונה מגיע ל-2 ברגע 5 ושוב ברגע 15.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function tags_needed" linenums="1" hl_lines="6 9 11"
        // the most transactions open at once: every send and every response is one event,
        // sorted by time; 2t for a response and 2t + 1 for a send puts the response first
        function automatic int tags_needed(int sends[], int ends[]);
          int ev[$], open_now = 0, best = 0;
          foreach (sends[i]) begin
            ev.push_back(2 * sends[i] + 1);                  // (1)!
            ev.push_back(2 * ends[i]);
          end
          ev.sort();
          foreach (ev[i]) begin
            if (ev[i] % 2) open_now++; else open_now--;      // (2)!
            if (open_now > best) best = open_now;
          end
          return best;
        endfunction
        ```

        1. האירוע הוא מספר אחד : הזמן כפול 2, ועוד 1 לשליחה. כך מיון של מספרים ממיין לפי זמן, ובזמן שווה התשובה (זוגי) באה לפני השליחה (אי-זוגי).
        2. הביט הנמוך אומר מה האירוע : שליחה מעלה את המונה, תשובה מורידה.

    === "Python"
        ```python title="tags_needed" linenums="1" hl_lines="4 8"
        def tags_needed(txns: list[tuple[int, int]]) -> int:
            """The most transactions open at once: +1 at a send, -1 at a response, and a
            response before a send at the same time."""
            events = sorted((t, d) for s, e in txns for t, d in ((s, 1), (e, -1)))   # (1)!
            open_now = best = 0
            for _, d in events:
                open_now += d
                best = max(best, open_now)
            return best
        ```

        1. זוגות \( (t, d) \) ממוינים לפי הזמן, ובזמן שווה לפי \( d \) : ‏\( -1 \) לפני \( +1 \), כלומר התשובה לפני השליחה.

    #### למה זה נכון { .sol-proof }

    האירועים של הדוגמה :

    <!-- gen 2 -->

    | הזמן | האירוע | פתוחות אחריו | המקסימום עד עכשיו |
    |:-:|:-:|:-:|:-:|
    | ‏0 | שליחה, ‏+1 | ‏1 | **‏1** |
    | ‏5 | שליחה, ‏+1 | ‏2 | **‏2** |
    | ‏10 | תשובה, ‏−1 | ‏1 | **‏2** |
    | ‏15 | שליחה, ‏+1 | ‏2 | **‏2** |
    | ‏20 | תשובה, ‏−1 | ‏1 | **‏2** |
    | ‏30 | תשובה, ‏−1 | ‏0 | **‏2** |

    <!-- /gen -->

    **הכרחי :** ברגע שבו המונה בשיא \( M \), יש \( M \) טרנזקציות פתוחות, וכל אחת מחזיקה tag
    משלה. פחות מ-\( M \) tags לא מספיקים.

    **מספיק :** עם \( M \) tags, בכל שליחה מספר הפתוחות לפני השליחה הוא לכל היותר \( M - 1 \)
    (אחרת המונה היה עובר את \( M \) אחרי השליחה), ולכן יש tag פנוי. איזה tag פנוי לוקחים לא
    משנה למספר.

    **זמנים שווים :** המונה אחרי כל האירועים של רגע \( t \) זהה בכל סדר. הסדר משפיע רק על הערכים
    באמצע הרגע : אם שליחה נספרת לפני תשובה באותו \( t \), המונה עולה לרגע ב-1 מעבר למספר
    הפתוחות האמיתי, וכך נספר tag אחד יותר מדי. לכן התשובה קודמת.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n \log n) \) בגלל המיון של \( 2n \) אירועים. הסריקה עצמה ליניארית. כשהזמנים
      הם מספרי מחזור קטנים אפשר למיין במניין (counting sort) ולהגיע ל-\( O(n + T) \).
    - **זיכרון :** ‏\( O(n) \) לאירועים.

    **נסו בעצמכם.** כל צעד הוא אירוע אחד, לפי הסדר. הקו שמתחת לטרנזקציות הוא המונה, והקו המקווקו
    השיא עד עכשיו :

    <div class="explorer" data-kind="tagpool" data-mode="one" data-txns="0-30 5-10 15-20"></div>

---

### סעיף ב – שני מאגרים, קריאות וכתיבות

??? tip "רמז 1"
    הריצו את סעיף א שלוש פעמים : על הקריאות לבד, על הכתיבות לבד, ועל כולן יחד. איזה אי-שוויון
    מתקיים בין שלושת המספרים?

??? tip "רמז 2"
    שני השיאים לא חייבים להתרחש באותו רגע.

<div class="selfcheck" data-answer="2" data-show="2 : שני מאגרים צריכים 2 + 2, ומאגר משותף 2, כי הקריאות נגמרות לפני שהכתיבות מתחילות" data-hint="חשבו את השיא של הקריאות לבד, של הכתיבות לבד ושל כולן יחד. ההפרש בין הסכום לשיא המשותף הוא החיסכון." markdown>
קריאות 0 עד 10 ו-2 עד 12, כתיבות 20 עד 30 ו-22 עד 32. כמה tags חוסך מאגר משותף לעומת שני
מאגרים נפרדים?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        אם \( R \) הוא השיא של הקריאות לבד, \( W \) של הכתיבות לבד ו-\( S \) של כולן יחד, אז תמיד
        \( \max(R, W) \le S \le R + W \). שני מאגרים צריכים \( R + W \), מאגר משותף \( S \), והשוויון
        \( S = R + W \) מתקיים רק כשיש רגע שבו שני המאגרים בשיא בו-זמנית. סריקה אחת עם שני
        מונים נותנת את שלושת המספרים.

    <!-- cost: זמן \( O(n \log n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    אותה סריקה, עם מונה לקריאות ומונה לכתיבות. השיא של כל מונה הוא המאגר שלו, והשיא של
    **הסכום** הוא המאגר המשותף. הסכום בכל רגע אינו גדול מסכום השיאים, ולכן \( S \le R + W \),
    ושווה לו רק אם ברגע כלשהו שני המונים בשיא יחד. בדוגמה השיאים רחוקים זה מזה :

    <!-- gen 3 -->

    <svg class="figure tp-fig" viewBox="0 0 640 232" role="img" aria-label="שתי קריאות ב-0 עד 12 ושתי כתיבות ב-20 עד 32 : שני מאגרים צריכים 4 tags, מאגר משותף 2"><line class="grid" x1="64" x2="64" y1="10" y2="202"/><text class="tick" x="64" y="130" text-anchor="middle">0</text><line class="grid" x1="151.5" x2="151.5" y1="10" y2="202"/><text class="tick" x="151.5" y="130" text-anchor="middle">5</text><line class="grid" x1="239" x2="239" y1="10" y2="202"/><text class="tick" x="239" y="130" text-anchor="middle">10</text><line class="grid" x1="326.5" x2="326.5" y1="10" y2="202"/><text class="tick" x="326.5" y="130" text-anchor="middle">15</text><line class="grid" x1="414" x2="414" y1="10" y2="202"/><text class="tick" x="414" y="130" text-anchor="middle">20</text><line class="grid" x1="501.5" x2="501.5" y1="10" y2="202"/><text class="tick" x="501.5" y="130" text-anchor="middle">25</text><line class="grid" x1="589" x2="589" y1="10" y2="202"/><text class="tick" x="589" y="130" text-anchor="middle">30</text><text class="tp-name" x="56" y="27" text-anchor="end">R1</text><rect class="tp-bar is-r" x="64" y="14" width="175" height="16" rx="3"><title>R1: 0–10</title></rect><text class="tp-name" x="56" y="51" text-anchor="end">R2</text><rect class="tp-bar is-r" x="99" y="38" width="175" height="16" rx="3"><title>R2: 2–12</title></rect><text class="tp-name" x="56" y="75" text-anchor="end">W3</text><rect class="tp-bar is-w" x="414" y="62" width="175" height="16" rx="3"><title>W3: 20–30</title></rect><text class="tp-name" x="56" y="99" text-anchor="end">W4</text><rect class="tp-bar is-w" x="449" y="86" width="175" height="16" rx="3"><title>W4: 22–32</title></rect><line class="axis" x1="64" x2="624" y1="116" y2="116"/><text class="tick" x="56" y="206" text-anchor="end">0</text><text class="tick" x="56" y="184" text-anchor="end">1</text><text class="tick" x="56" y="162" text-anchor="end">2</text><line class="tp-max" x1="64" x2="624" y1="158" y2="158"/><path class="tp-count" d="M64,202 H64 V180 H99 V158 H239 V180 H274 V202 H414 V180 H449 V158 H589 V180 H624 V202 H624"/><text class="legend" x="624" y="151" text-anchor="end">max = 2</text><text class="tp-name" x="56" y="148" text-anchor="end">open</text></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="tp-key-r"></i>קריאה</span><span><i class="tp-key-w"></i>כתיבה</span><span><i class="tp-key-count"></i>כמה פתוחות יחד</span><span><i class="tp-key-max"></i>המקסימום של המאגר המשותף</span></span>

    <!-- /gen -->

    כאן \( R = 2 \), ‏\( W = 2 \), ‏\( S = 2 \) : שני מאגרים צריכים 4 tags ומאגר משותף 2. אם
    הכתיבות היו ב-3 עד 13 וב-5 עד 15, כל ארבע הטרנזקציות היו פתוחות ברגע 5, ו-\( S = 4 = R + W \).

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function pools" linenums="1" hl_lines="9 10 18"
        // one sweep with a counter per kind: the pool of the reads, the pool of the writes and
        // the shared pool that follows their sum; an event is 4t + 2 for a send (+0 for a
        // response) + 1 for a read, so at one time every response comes before every send
        function automatic void pools(int sends[], int ends[], bit is_read[],
                                      output int reads, output int writes, output int shared);
          int ev[$], open_r = 0, open_w = 0, d;
          reads = 0; writes = 0; shared = 0;
          foreach (sends[i]) begin
            ev.push_back(4 * sends[i] + 2 + is_read[i]);     // (1)!
            ev.push_back(4 * ends[i] + is_read[i]);
          end
          ev.sort();
          foreach (ev[i]) begin
            d = (ev[i] & 2) ? 1 : -1;
            if (ev[i] & 1) open_r += d; else open_w += d;
            if (open_r > reads) reads = open_r;
            if (open_w > writes) writes = open_w;
            if (open_r + open_w > shared) shared = open_r + open_w;   // (2)!
          end
        endfunction
        ```

        1. שני הביטים הנמוכים : ביט 1 לשליחה (אפס לתשובה), ביט 0 לקריאה. בזמן שווה כל התשובות, של שני הסוגים, באות לפני כל השליחות.
        2. המאגר המשותף עוקב אחרי הסכום של שני המונים.

    === "Python"
        ```python title="pools" linenums="1" hl_lines="4 10"
        def pools(txns: list[tuple[int, int, str]]) -> tuple[int, int, int]:
            """Tags for the reads alone, the writes alone and one shared pool, in one sweep: a
            counter per kind, and the shared pool follows their sum."""
            events = sorted((t, d, kind) for s, e, kind in txns for t, d in ((s, 1), (e, -1)))
            open_now = {"R": 0, "W": 0}
            best = {"R": 0, "W": 0, "shared": 0}
            for _, d, kind in events:
                open_now[kind] += d
                best[kind] = max(best[kind], open_now[kind])
                best["shared"] = max(best["shared"], open_now["R"] + open_now["W"])   # (1)!
            return best["R"], best["W"], best["shared"]
        ```

        1. המאגר המשותף עוקב אחרי הסכום של שני המונים. הסוג נמצא במקום השלישי של האירוע, אחרי \( d \), ולכן התשובות עדיין קודמות לשליחות.

    #### למה זה נכון { .sol-proof }

    **‏\( S \le R + W \) :** בכל רגע הפתוחות יחד הן הקריאות הפתוחות ועוד הכתיבות הפתוחות, לכל
    היותר \( R + W \). לכן גם השיא של הסכום אינו עולה על \( R + W \).

    **‏\( S \ge \max(R, W) \) :** ברגע שבו הקריאות בשיא יש לפחות \( R \) פתוחות יחד, וכך גם עם
    הכתיבות.

    **שוויון :** ‏\( S = R + W \) בדיוק כשיש רגע שבו \( R \) קריאות ו-\( W \) כתיבות פתוחות יחד.
    אחרת בכל רגע אחד המונים מתחת לשיאו, והסכום קטן מ-\( R + W \).

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n \log n) \), כמו סעיף א. סריקה אחת במקום שלוש.
    - **זיכרון :** ‏\( O(n) \).

    **נסו בעצמכם.** קריאות וכתיבות בצבעים שונים, ושלושת המונים בכל צעד :

    <div class="explorer" data-kind="tagpool" data-mode="two" data-txns="R0-10 R2-12 W20-30 W22-32"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : שליחה לפני תשובה באותו רגע"
    אם ממיינים את השליחה לפני התשובה באותו \( t \), המונה עולה לרגע מעבר למספר הפתוחות האמיתי.
    לטרנזקציות 0 עד 10 ו-10 עד 20 מקבלים 2 במקום 1. ההסכמה צריכה להיאמר בשאלה, והמיון צריך
    לכבד אותה.

??? trap "מלכודת : לספור כמה חופפות לכל טרנזקציה"
    הטרנזקציה 0 עד 30 חופפת לשתי האחרות, אבל שלושתן אף פעם לא פתוחות יחד. "הכי הרבה חפיפות
    של טרנזקציה אחת ועוד 1" נותן 3 במקום 2. סופרים פתוחות ברגע, לא זוגות חופפים.

??? trap "מלכודת : לשבץ tags בפועל כדי לספור"
    לחפש tag פנוי לכל שליחה ולזכור מתי הוא משתחרר עובד, אבל זה \( O(n \cdot \text{tags}) \) או ערימה,
    והרבה קוד בשביל מספר אחד. השיא של המונה הוא אותו מספר, בלי שיבוץ.

??? followup "שאלות המשך"
    - **איזה tag לכל טרנזקציה :** איך משבצים בפועל, בלי לחרוג מהמספר שחישבנו?

        ??? fu-answer "תשובה"
            שומרים ערימת מינימום של \( (e_i, \text{tag}) \) לטרנזקציות הפתוחות ורשימה של tags
            פנויים. בכל שליחה מוציאים קודם מהערימה את כל מי ש-\( e \le s \) ומחזירים את ה-tags
            שלהן לרשימה, ואז לוקחים tag פנוי. הרשימה אף פעם לא מתרוקנת, לפי ההוכחה של סעיף א.

    - **רק T tags :** מה אם יש פחות tags מהשיא? איך מחשבים מתי כל שליחה יוצאת בפועל?

        ??? fu-answer "תשובה"
            שליחה שאין לה tag מחכה עד שהתשובה הקרובה ביותר משחררת אחד, ונדחית בהתאם, כולל זמן
            התשובה שלה. ערימת מינימום של זמני השחרור נותנת את זה ב-\( O(n \log n) \), וסכום הדחיות
            הוא מחיר המאגר הקטן.

    - **טרנזקציה שתופסת w tags :** burst של \( w \) beats תופס \( w \) קרדיטים. מה משתנה?

        ??? fu-answer "תשובה"
            אותה סריקה, עם \( +w_i \) בשליחה ו-\( -w_i \) בתשובה במקום \( \pm 1 \). השיא של המונה
            הוא מספר הקרדיטים, ואותה הסכמה על זמנים שווים.
