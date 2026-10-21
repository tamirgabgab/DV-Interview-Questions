---
id: 6
title: רווח מקסימלי ממניה – לונג או שורט
level: junior
difficulty: medium
tags: [algorithms, python, systemverilog]
source: ""
added: 2026-10-15
---

## השאלה

נתון מערך `prices`, ובו `prices[i]` הוא מחיר המניה ביום \( i \). מותר לבצע **עסקה אחת**:
פעולה אחת ביום \( i \), ופעולה הפוכה ביום מאוחר יותר \( j > i \).

**כל זוג ימים שנותן את הרווח המקסימלי הוא תשובה נכונה.** אם אין עסקה שמרוויחה, מחזירים
רווח 0 ובלי ימים.

??? interviewer "מה המראיין בודק"
    - **מהפשוט ליעיל:** להתחיל מפתרון שבודק את כל הזוגות, ואז לזהות איזו עבודה חוזרת
      על עצמה ומיותרת.
    - **מה זוכרים בין יום ליום:** לנסח במדויק מה ידוע אחרי כל יום, ולמה זה מספיק כדי
      להחליט על היום הבא.
    - **מקרי קצה:** מערך ריק, יום אחד, מחירים שרק יורדים, ועסקה "באותו יום".
    - **הרחבה בלי לכתוב מחדש:** האם הטוויסט של סעיף ב משתלב בלולאה הקיימת, או דורש
      פתרון חדש.
    - **איך בודקים:** איך משווים את הפתרון היעיל לפתרון הפשוט על הרבה קלטים אקראיים.

---

### סעיף א – קנייה ואחר כך מכירה (לונג)

מצאו באיזה יום לקנות ובאיזה יום למכור כדי שהרווח \( prices[j] - prices[i] \) יהיה
מקסימלי.

??? tip "רמז 1"
    התחילו מהפתרון הפשוט: לבדוק כל זוג ימים \( i < j \). כמה זוגות כאלה יש, ואיזה חישוב
    חוזר על עצמו שוב ושוב?

??? tip "רמז 2"
    אם מחליטים למכור ביום \( j \), באיזה יום הכי כדאי היה לקנות? צריך לבדוק את כל הימים
    שלפניו, או שמספיק לזכור משהו אחד?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מעבר אחד על המערך: לכל יום בודקים את הרווח מול **המחיר הנמוך ביותר עד כה**, ורק
        אחר כך מעדכנים את המינימום. זמן **\( O(n) \)** וזיכרון \( O(1) \), במקום \( O(n^2) \)
        של בדיקת כל הזוגות.

    #### הרעיון { .sol-idea }

    אם מוכרים ביום \( j \), הקנייה הכי טובה היא במחיר **הנמוך ביותר עד אותו יום**. לכן לא
    צריך לבדוק את כל הזוגות: מספיק לזכור את המינימום עד כה ואת היום שבו הוא הופיע.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **לאתחל:** המינימום הוא מחיר היום הראשון, והרווח הטוב ביותר הוא 0 בלי ימים.
    2. **לכל יום, קודם לבדוק:** הרווח ממכירה היום הוא המחיר פחות המינימום של הימים
       **הקודמים**. אם הוא גדול מהטוב ביותר עד כה, שומרים אותו עם זוג הימים.
    3. **ורק אז לעדכן:** אם מחיר היום נמוך מהמינימום, הוא המינימום החדש, והיום הוא יום
       הקנייה המועמד הבא.
    4. **להחזיר:** את הרווח הטוב ביותר ואת זוג הימים שלו.

    </div>

    #### הקוד { .sol-code }

    **פתרון לא יעיל, \( O(n^2) \).** בודקים כל זוג ימים \( i < j \):

    === "SystemVerilog"
        ```systemverilog title="function max_long_brute" linenums="1" hl_lines="12 13"
        typedef struct {
          int    profit;
          string kind;      // "long", "short", or "" when no trade makes a profit
          int    open_i;    // day of the first trade  (-1 when there is no trade)
          int    close_i;   // day of the second trade (-1 when there is no trade)
        } trade_t;

        function automatic trade_t max_long_brute(int prices[$]);
          trade_t best = '{0, "", -1, -1};   // (1)!
          for (int i = 0; i < prices.size(); i++)
            for (int j = i + 1; j < prices.size(); j++)
              if (prices[j] - prices[i] > best.profit)   // (2)!
                best = '{prices[j] - prices[i], "long", i, j};
          return best;
        endfunction
        ```

        1. ‏"אין עסקה" מיוצג ברווח 0 ובימים `-1`. כל עסקה שנשמרת חייבת להיות טובה **ממש**
           מזה, ולכן עסקה ברווח 0 לא נחשבת.
        2. ההשוואה היא `>` ולא `>=`, ולכן מבין כמה זוגות עם אותו רווח נשמר הראשון לפי
           הסדר \( (i, j) \). הלולאה הפנימית מתחילה מ-`i + 1`, כך ש-\( j > i \) תמיד.

    === "Python"
        ```python title="max_long_brute" hl_lines="5 6"
        def max_long_brute(prices):
            best, buy, sell = 0, None, None   # (1)!
            for i in range(len(prices)):
                for j in range(i + 1, len(prices)):
                    if prices[j] - prices[i] > best:   # (2)!
                        best, buy, sell = prices[j] - prices[i], i, j
            return best, buy, sell
        ```

        1. ‏"אין עסקה" הוא רווח 0 ו-`None` לשני הימים.
        2. ההשוואה החדה שומרת את הזוג הראשון מבין זוגות עם אותו רווח.

    **פתרון יעיל, \( O(n) \).** עוברים על המערך פעם אחת, וזוכרים את המינימום עד כה ואת
    היום שבו הוא הופיע:

    === "SystemVerilog"
        ```systemverilog title="function max_long_fast" linenums="1" hl_lines="8 9"
        function automatic trade_t max_long_fast(int prices[$]);
          trade_t best = '{0, "", -1, -1};
          int     min_p, min_i;
          if (prices.size() == 0) return best;   // (1)!
          min_p = prices[0];                    // cheapest price seen so far
          min_i = 0;
          foreach (prices[i]) begin
            if (prices[i] - min_p > best.profit)  // sell today, bought at the cheapest day (2)
              best = '{prices[i] - min_p, "long", min_i, i};
            if (prices[i] < min_p) begin   // (3)!
              min_p = prices[i];
              min_i = i;
            end
          end
          return best;
        endfunction
        ```

        1. מערך ריק נבדק לפני הגישה ל-`prices[0]`. עם יום אחד הלולאה רצה פעם אחת, הרווח
           הוא 0, ומוחזר "אין עסקה".
        2. ביום הראשון `min_p` הוא מחיר היום עצמו, והרווח 0 לא נשמר. מהיום השני והלאה
           `min_p` הוא תמיד המינימום של הימים **הקודמים**, כי העדכון בא אחרי הבדיקה.
        3. העדכון אחרי הבדיקה. הוא ב-`<` ולא ב-`<=`, ולכן `min_i` נשאר היום **הראשון**
           שבו הופיע המחיר הנמוך.

    === "Python"
        ```python title="max_long_fast" hl_lines="7 8"
        def max_long_fast(prices):
            best, buy, sell = 0, None, None
            if not prices:
                return best, buy, sell
            min_p, min_i = prices[0], 0              # cheapest price seen so far
            for i, p in enumerate(prices):
                if p - min_p > best:                 # sell today, bought at the cheapest day (1)
                    best, buy, sell = p - min_p, min_i, i
                if p < min_p:   # (2)!
                    min_p, min_i = p, i
            return best, buy, sell
        ```

        1. הבדיקה מול המינימום של הימים הקודמים באה **לפני** העדכון, ולכן יום הקנייה
           תמיד מוקדם מיום המכירה.
        2. העדכון ב-`<` שומר את היום הראשון שבו הופיע המינימום.

    #### למה זה נכון { .sol-proof }

    לכל יום מכירה \( j \), הרווח הטוב ביותר האפשרי הוא \( prices[j] - \min_{i<j} prices[i] \):
    כל קנייה אחרת לפני \( j \) יקרה יותר או שווה. הלולאה בודקת בדיוק את הערך הזה לכל
    \( j \), ולכן המקסימום שלה הוא המקסימום על כל הזוגות.

    הסדר בתוך הלולאה חשוב: קודם בודקים את הרווח מול המינימום **של הימים הקודמים**, ורק
    אחר כך מעדכנים את המינימום. כך אף פעם לא "קונים ומוכרים" באותו יום.

    #### סיבוכיות { .sol-cost }

    הפתרון הלא יעיל בודק \( n(n-1)/2 \) זוגות, כלומר \( O(n^2) \). הפתרון היעיל עובר על
    המערך פעם אחת, \( O(n) \), עם שני משתנים נוספים בלבד, \( O(1) \) זיכרון. ההשוואה
    המלאה, כולל המספרים, בסעיף ב.

---

### סעיף ב – הטוויסט: מותר גם שורט

עכשיו מותר לבצע גם **שורט**: למכור את המניה ביום \( i \), ולקנות אותה בחזרה ביום מאוחר
יותר \( j > i \). הרווח בשורט הוא \( prices[i] - prices[j] \), כלומר מרוויחים כשהמחיר
יורד.

מצאו את העסקה הטובה ביותר מבין כל עסקאות הלונג וכל עסקאות השורט, והחזירו את הרווח, את
סוג העסקה ואת שני הימים.

**דוגמה:** עבור `{5, 8, 3, 9, 2, 6}`, הלונג הטוב ביותר מרוויח 6 (קונים ב-3, מוכרים ב-9),
אבל השורט הטוב ביותר מרוויח 7 (מוכרים ב-9 ביום 3, קונים בחזרה ב-2 ביום 4). התשובה היא
**שורט, רווח 7, ימים 3 ו-4**.

??? tip "רמז 1"
    כתבו את הרווח של שורט בין הימים \( i \) ו-\( j \) ליד הרווח של לונג באותם ימים. מה
    הקשר ביניהם, ואיך זה עוזר להשתמש שוב בפתרון של סעיף א?

??? tip "רמז 2"
    שורט הוא בדיוק "לונג הפוך": במקום המינימום עד כה, מה צריך לזכור?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        מריצים "שני סעיפי א" באותה לולאה: המינימום עד כה בשביל הלונג, **המקסימום עד כה**
        בשביל השורט, ובסוף מחזירים את הטוב מבין השניים. עבור הדוגמה: **שורט ברווח 7, ימים
        3 ו-4**. זמן \( O(n) \), זיכרון \( O(1) \).

    #### הרעיון { .sol-idea }

    רווח השורט בין \( i \) ל-\( j \) הוא בדיוק מינוס רווח הלונג באותם ימים. לכן אם בלונג
    הכי טוב לקנות בזול ביותר שהיה, בשורט הכי טוב למכור **ביקר ביותר** שהיה: במקום
    המינימום עד כה זוכרים את המקסימום עד כה, ושני החישובים חיים באותה לולאה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **לאתחל שני מועמדים:** לונג עם המינימום עד כה, ושורט עם המקסימום עד כה. שניהם
       מתחילים ממחיר היום הראשון, עם רווח 0.
    2. **לכל יום, לבדוק את שניהם:** מחיר היום פחות המינימום הוא רווח הלונג האפשרי היום,
       והמקסימום פחות מחיר היום הוא רווח השורט האפשרי היום. כל אחד מהם משווים לטוב ביותר
       מסוגו.
    3. **ורק אז לעדכן:** את המינימום ואת המקסימום לפי מחיר היום.
    4. **לבחור בסוף:** אם השורט הטוב יותר מהלונג מחזירים אותו; אחרת, אם הלונג חיובי,
       מחזירים אותו; אחרת "אין עסקה".

    </div>

    #### הקוד { .sol-code }

    **פתרון לא יעיל, \( O(n^2) \).** לכל זוג ימים \( i < j \) מחשבים גם את רווח הלונג וגם
    את רווח השורט:

    === "SystemVerilog"
        ```systemverilog title="function max_profit_brute" linenums="1" hl_lines="7 8"
        function automatic trade_t max_profit_brute(int prices[$]);
          trade_t best = '{0, "", -1, -1};
          int     long_profit, short_profit;

          for (int i = 0; i < prices.size(); i++)
            for (int j = i + 1; j < prices.size(); j++) begin
              long_profit  = prices[j] - prices[i];   // buy at i, sell at j
              short_profit = prices[i] - prices[j];   // sell at i, buy back at j (1)

              if (long_profit > best.profit)
                best = '{long_profit, "long", i, j};
              if (short_profit > best.profit)   // (2)!
                best = '{short_profit, "short", i, j};
            end

          return best;
        endfunction
        ```

        1. אותו זוג ימים, סימן הפוך: בדיוק אחד מהשניים חיובי (או שניהם אפס), ולכן בכל זוג
           רק עסקה אחת יכולה להשתפר.
        2. הלונג נבדק קודם, וההשוואה חדה. לכן כשללונג ולשורט יש אותו רווח מקסימלי, מוחזר
           הלונג, בדיוק כמו בפתרון היעיל.

    === "Python"
        ```python title="max_profit_brute" hl_lines="6 7"
        def max_profit_brute(prices):
            best, kind, first, second = 0, None, None, None

            for i in range(len(prices)):
                for j in range(i + 1, len(prices)):
                    long_profit = prices[j] - prices[i]     # buy at i, sell at j
                    short_profit = prices[i] - prices[j]    # sell at i, buy back at j (1)

                    if long_profit > best:
                        best, kind, first, second = long_profit, "long", i, j
                    if short_profit > best:   # (2)!
                        best, kind, first, second = short_profit, "short", i, j

            return best, kind, first, second
        ```

        1. אותו זוג ימים בסימן הפוך.
        2. ההשוואה החדה אחרי בדיקת הלונג: בתיקו בין לונג לשורט מוחזר הלונג.

    **פתרון יעיל, \( O(n) \).** מריצים "שני סעיפי א" במקביל, באותה לולאה:

    - **בשביל הלונג:** זוכרים את **המינימום עד כה**, כי הכי טוב לקנות בזול ביותר.
    - **בשביל השורט:** זוכרים את **המקסימום עד כה**, כי הכי טוב למכור ביקר ביותר.

    בסוף מחזירים את הטוב מבין השניים:

    === "SystemVerilog"
        ```systemverilog title="function max_profit_fast" linenums="1" hl_lines="13 19"
        function automatic trade_t max_profit_fast(int prices[$]);
          trade_t none = '{0, "", -1, -1};
          trade_t lng  = '{0, "long", -1, -1};
          trade_t sht  = '{0, "short", -1, -1};
          int     min_p, min_i;                 // cheapest price so far -> best day to open a long
          int     max_p, max_i;                 // highest price so far  -> best day to open a short

          if (prices.size() < 2) return none;   // (1)!
          min_p = prices[0];  min_i = 0;
          max_p = prices[0];  max_i = 0;

          foreach (prices[i]) begin
            if (prices[i] - min_p > lng.profit) begin
              lng.profit  = prices[i] - min_p;
              lng.open_i  = min_i;
              lng.close_i = i;
            end

            if (max_p - prices[i] > sht.profit) begin   // (2)!
              sht.profit  = max_p - prices[i];
              sht.open_i  = max_i;
              sht.close_i = i;
            end

            if (prices[i] < min_p) begin min_p = prices[i]; min_i = i; end   // (3)!
            if (prices[i] > max_p) begin max_p = prices[i]; max_i = i; end
          end

          if (sht.profit > lng.profit) return sht;   // (4)!
          if (lng.profit > 0)          return lng;
          return none;
        endfunction
        ```

        1. עסקה דורשת שני ימים שונים, ולכן עם פחות משני מחירים אין מה לבדוק. הבדיקה גם
           מגינה על הגישה ל-`prices[0]`.
        2. תמונת ראי של בדיקת הלונג: המקסימום של הימים **הקודמים** פחות מחיר היום. שני
           המועמדים נבדקים באותו יום, לפני כל עדכון.
        3. שני העדכונים אחרי שתי הבדיקות, בהשוואות חדות: `min_i` ו-`max_i` הם הימים
           **הראשונים** שבהם הופיעו הקיצונים.
        4. בחירה חדה: בתיקו בין שורט ללונג מוחזר הלונג, ואם גם הלונג ברווח 0 מוחזר "אין
           עסקה" עם ימים `-1`.

    === "Python"
        ```python title="max_profit_fast" linenums="1" hl_lines="12 16"
        def max_profit_fast(prices):
            if len(prices) < 2:   # (1)!
                return 0, None, None, None

            min_p, min_i = prices[0], 0     # cheapest price so far  -> best day to open a long
            max_p, max_i = prices[0], 0     # highest price so far   -> best day to open a short

            long_best, long_open, long_close = 0, None, None
            short_best, short_open, short_close = 0, None, None

            for i, p in enumerate(prices):
                if p - min_p > long_best:
                    long_best = p - min_p
                    long_open, long_close = min_i, i

                if max_p - p > short_best:   # (2)!
                    short_best = max_p - p
                    short_open, short_close = max_i, i

                if p < min_p:   # (3)!
                    min_p, min_i = p, i
                if p > max_p:
                    max_p, max_i = p, i

            if short_best > long_best:   # (4)!
                return short_best, "short", short_open, short_close
            if long_best > 0:
                return long_best, "long", long_open, long_close
            return 0, None, None, None
        ```

        1. עם פחות משני מחירים אין עסקה אפשרית.
        2. תמונת ראי של בדיקת הלונג, עם המקסימום של הימים הקודמים.
        3. העדכונים באים אחרי שתי הבדיקות, בהשוואות חדות.
        4. בתיקו מוחזר הלונג; לונג ברווח 0 הוא "אין עסקה".

    #### למה זה נכון { .sol-proof }

    **המחשה על הדוגמה.** הקו האפור הוא מחיר המניה. הקו הכחול הוא **המינימום עד כה**, שמשמש
    את הלונג, והקו הכתום הוא **המקסימום עד כה**, שמשמש את השורט. המקטעים המודגשים הם העסקה
    הטובה ביותר מכל סוג. מעבר עם העכבר על נקודה מציג את המחיר.

    <!-- gen 0 -->

    <span class="viz-legend"><span><i class="ink"></i>מחיר המניה</span><span><i class="s1"></i>המינימום עד כה (לונג)</span><span><i class="s2"></i>המקסימום עד כה (שורט)</span></span>

    <!-- /gen -->

    <!-- gen 1 -->

    <svg class="perf-chart" viewBox="0 0 640 300" role="img" aria-label="גרף מחירי המניה לפי יום, עם המינימום והמקסימום עד כה ועסקאות הלונג והשורט הטובות ביותר"><line class="grid" x1="44" x2="600" y1="260.0" y2="260.0"/><text class="tick" x="36" y="264.0" text-anchor="end">0</text><line class="grid" x1="44" x2="600" y1="212.0" y2="212.0"/><text class="tick" x="36" y="216.0" text-anchor="end">2</text><line class="grid" x1="44" x2="600" y1="164.0" y2="164.0"/><text class="tick" x="36" y="168.0" text-anchor="end">4</text><line class="grid" x1="44" x2="600" y1="116.0" y2="116.0"/><text class="tick" x="36" y="120.0" text-anchor="end">6</text><line class="grid" x1="44" x2="600" y1="68.0" y2="68.0"/><text class="tick" x="36" y="72.0" text-anchor="end">8</text><line class="grid" x1="44" x2="600" y1="20.0" y2="20.0"/><text class="tick" x="36" y="24.0" text-anchor="end">10</text><text class="tick" x="44.0" y="286" text-anchor="middle" direction="rtl">יום 0</text><text class="tick" x="155.2" y="286" text-anchor="middle" direction="rtl">יום 1</text><text class="tick" x="266.4" y="286" text-anchor="middle" direction="rtl">יום 2</text><text class="tick" x="377.6" y="286" text-anchor="middle" direction="rtl">יום 3</text><text class="tick" x="488.8" y="286" text-anchor="middle" direction="rtl">יום 4</text><text class="tick" x="600.0" y="286" text-anchor="middle" direction="rtl">יום 5</text><path class="s1-line" d="M44.0,140.0 H155.2 V140.0 H266.4 V188.0 H377.6 V188.0 H488.8 V212.0 H600.0 V212.0" fill="none" stroke-width="2"/><path class="s2-line" d="M44.0,140.0 H155.2 V68.0 H266.4 V68.0 H377.6 V44.0 H488.8 V44.0 H600.0 V44.0" fill="none" stroke-width="2"/><line class="s1-line" x1="266.4" y1="188.0" x2="377.6" y2="44.0" stroke-width="8" opacity="0.35"/><line class="s2-line" x1="377.6" y1="44.0" x2="488.8" y2="212.0" stroke-width="8" opacity="0.35"/><polyline class="ink-line" points="44.0,140.0 155.2,68.0 266.4,188.0 377.6,44.0 488.8,212.0 600.0,116.0" fill="none" stroke-width="2"/><circle class="ink-dot" cx="44.0" cy="140.0" r="5"><title>יום 0: מחיר 5</title></circle><text class="legend" x="44.0" y="160.0" text-anchor="middle" style="font-size:12px">5</text><circle class="ink-dot" cx="155.2" cy="68.0" r="5"><title>יום 1: מחיר 8</title></circle><text class="legend" x="155.2" y="57.0" text-anchor="middle" style="font-size:12px">8</text><circle class="ink-dot" cx="266.4" cy="188.0" r="5"><title>יום 2: מחיר 3</title></circle><text class="legend" x="266.4" y="208.0" text-anchor="middle" style="font-size:12px">3</text><circle class="ink-dot" cx="377.6" cy="44.0" r="5"><title>יום 3: מחיר 9</title></circle><text class="legend" x="377.6" y="33.0" text-anchor="middle" style="font-size:12px">9</text><circle class="ink-dot" cx="488.8" cy="212.0" r="5"><title>יום 4: מחיר 2</title></circle><text class="legend" x="488.8" y="232.0" text-anchor="middle" style="font-size:12px">2</text><circle class="ink-dot" cx="600.0" cy="116.0" r="5"><title>יום 5: מחיר 6</title></circle><text class="legend" x="600.0" y="105.0" text-anchor="middle" style="font-size:12px">6</text><text class="legend" x="310.0" y="120.8" text-anchor="end">long +6</text><text class="legend" x="445.2" y="120.8" text-anchor="start">short +7 ✓</text></svg>

    <!-- /gen -->

    **מעקב אחרי הלולאה.** בכל יום מחשבים את הרווח האפשרי מול המינימום והמקסימום של הימים
    **הקודמים**, ורק אחר כך מעדכנים אותם. ✅ מסמן שיפור:

    | יום | מחיר | לונג היום (מחיר פחות מינימום) | הלונג הטוב (ימים) | שורט היום (מקסימום פחות מחיר) | השורט הטוב (ימים) | מינימום אחרי היום | מקסימום אחרי היום |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | 0 | 5 | 0 | 0 | 0 | 0 | 5 (יום 0) | 5 (יום 0) |
    | 1 | 8 | 3 ✅ | 3 (0→1) | ‎-3 | 0 | 5 (יום 0) | 8 (יום 1) |
    | 2 | 3 | ‎-2 | 3 (0→1) | 5 ✅ | 5 (1→2) | 3 (יום 2) | 8 (יום 1) |
    | 3 | 9 | 6 ✅ | 6 (2→3) | ‎-1 | 5 (1→2) | 3 (יום 2) | 9 (יום 3) |
    | 4 | 2 | ‎-1 | 6 (2→3) | 7 ✅ | 7 (3→4) | 2 (יום 4) | 9 (יום 3) |
    | 5 | 6 | 4 | 6 (2→3) | 3 | 7 (3→4) | 2 (יום 4) | 9 (יום 3) |

    בסוף, השורט (7) גדול מהלונג (6), ולכן התשובה היא **שורט ברווח 7, ימים 3 ו-4**.

    #### סיבוכיות { .sol-cost }

    | | פתרון לא יעיל | פתרון יעיל |
    |-|---------------|------------|
    | זמן | ‏\( O(n^2) \): כל הזוגות | ‏\( O(n) \): מעבר אחד |
    | זיכרון נוסף | ‏\( O(1) \) | ‏\( O(1) \): ארבעה משתנים |
    | עבור מיליון ימים | כ-\( 5 \cdot 10^{11} \) זוגות | מיליון צעדים |

    הפתרון היעיל עושה לכל יום עבודה קבועה: שתי בדיקות ושני עדכונים, ולכן הזמן ליניארי
    גם כשמוסיפים את השורט.

    !!! note "הקשר ל-DV"
        זה בדיוק המבנה של **reference model** טוב: הפתרון הלא יעיל פשוט מספיק כדי שיהיה קל
        לסמוך עליו, והפתרון היעיל הוא "ה-DUT". מריצים את שניהם על הרבה קלטים אקראיים ומשווים
        את הרווח, וכך נבדקה גם הגרסה שבעמוד הזה.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: מקסימום פחות מינימום"
    הרווח של הלונג הוא **לא** המחיר הגבוה ביותר פחות הנמוך ביותר במערך: הקנייה חייבת
    לבוא **לפני** המכירה. עבור `{9, 1}` ההפרש הוא 8, אבל אין לונג שמרוויח (זה דווקא
    שורט מצוין). לכן זוכרים את המינימום **עד כה**, ולא את המינימום של כל המערך.

??? trap "מלכודת: כמה זוגות ימים עם אותו רווח"
    כשיש כמה עסקאות עם אותו רווח מקסימלי, שתי הפונקציות עשויות להחזיר **זוג ימים שונה**,
    אבל תמיד את **אותו רווח**. הפונקציה הלא יעילה מחזירה את הזוג הראשון לפי הסדר
    \( (i, j) \). הפונקציה היעילה נצמדת למינימום או למקסימום **הראשונים** שהופיעו, כי
    העדכון מתבצע רק כשיש ערך קטן או גדול **ממש**. אם ללונג ולשורט יש אותו רווח, היא מעדיפה
    לונג. לכן בבדיקה אוטומטית משווים את הרווח, ובודקים שהימים שהוחזרו באמת נותנים אותו.

??? followup "שאלות המשך"
    - **הרבה עסקאות:** אם מותר לבצע כמה עסקאות לונג שאינן חופפות, סוכמים את כל העליות בין
      יום ליום, ב-\( O(n) \).
    - **בדיוק \( k \) עסקאות:** פותרים בתכנות דינמי, ב-\( O(nk) \).
    - **עמלה על כל עסקה:** מוסיפים את העמלה לתנאי, ואם הרווח אחרי העמלה לא חיובי לא
      מבצעים עסקה.
