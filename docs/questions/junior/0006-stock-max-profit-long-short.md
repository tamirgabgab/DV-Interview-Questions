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

---

### סעיף א – קנייה ואחר כך מכירה (לונג)

מצאו באיזה יום לקנות ובאיזה יום למכור כדי שהרווח \( prices[j] - prices[i] \) יהיה
מקסימלי.

??? tip "רמז"
    אם מחליטים למכור ביום \( j \), באיזה יום הכי כדאי היה לקנות? צריך לבדוק את כל הימים
    שלפניו, או שמספיק לזכור משהו אחד?

??? success "פתרון סעיף א"
    #### פתרון לא יעיל – \( O(n^2) \)

    בודקים כל זוג ימים \( i < j \):

    === "SystemVerilog"
        ```systemverilog
        typedef struct {
          int    profit;
          string kind;      // "long", "short", or "" when no trade makes a profit
          int    open_i;    // day of the first trade  (-1 when there is no trade)
          int    close_i;   // day of the second trade (-1 when there is no trade)
        } trade_t;

        function automatic trade_t max_long_brute(int prices[$]);
          trade_t best = '{0, "", -1, -1};
          for (int i = 0; i < prices.size(); i++)
            for (int j = i + 1; j < prices.size(); j++)
              if (prices[j] - prices[i] > best.profit)
                best = '{prices[j] - prices[i], "long", i, j};
          return best;
        endfunction
        ```

    === "Python"
        ```python
        def max_long_brute(prices):
            best, buy, sell = 0, None, None
            for i in range(len(prices)):
                for j in range(i + 1, len(prices)):
                    if prices[j] - prices[i] > best:
                        best, buy, sell = prices[j] - prices[i], i, j
            return best, buy, sell
        ```

    #### פתרון יעיל – \( O(n) \)

    אם מוכרים ביום \( j \), הקנייה הכי טובה היא במחיר **הנמוך ביותר עד אותו יום**. לכן
    עוברים על המערך פעם אחת, וזוכרים את המינימום עד כה ואת היום שבו הוא הופיע:

    === "SystemVerilog"
        ```systemverilog
        function automatic trade_t max_long_fast(int prices[$]);
          trade_t best = '{0, "", -1, -1};
          int     min_p, min_i;
          if (prices.size() == 0) return best;
          min_p = prices[0];                    // cheapest price seen so far
          min_i = 0;
          foreach (prices[i]) begin
            if (prices[i] - min_p > best.profit)  // sell today, bought at the cheapest day
              best = '{prices[i] - min_p, "long", min_i, i};
            if (prices[i] < min_p) begin
              min_p = prices[i];
              min_i = i;
            end
          end
          return best;
        endfunction
        ```

    === "Python"
        ```python
        def max_long_fast(prices):
            best, buy, sell = 0, None, None
            if not prices:
                return best, buy, sell
            min_p, min_i = prices[0], 0              # cheapest price seen so far
            for i, p in enumerate(prices):
                if p - min_p > best:                 # sell today, bought at the cheapest day
                    best, buy, sell = p - min_p, min_i, i
                if p < min_p:
                    min_p, min_i = p, i
            return best, buy, sell
        ```

    הסדר בתוך הלולאה חשוב: קודם בודקים את הרווח מול המינימום **של הימים הקודמים**, ורק
    אחר כך מעדכנים את המינימום. כך אף פעם לא "קונים ומוכרים" באותו יום.

---

### סעיף ב – הטוויסט: מותר גם שורט

עכשיו מותר לבצע גם **שורט**: למכור את המניה ביום \( i \), ולקנות אותה בחזרה ביום
\( j > i \). הרווח בשורט הוא \( prices[i] - prices[j] \), כלומר מרוויחים כשהמחיר יורד.

מצאו את העסקה הטובה ביותר מבין כל עסקאות הלונג וכל עסקאות השורט, והחזירו את הרווח, את
סוג העסקה ואת שני הימים.

**דוגמה:** עבור `{5, 8, 3, 9, 2, 6}`, הלונג הטוב ביותר מרוויח 6 (קונים ב-3, מוכרים ב-9),
אבל השורט הטוב ביותר מרוויח 7 (מוכרים ב-9 ביום 3, קונים בחזרה ב-2 ביום 4). התשובה היא
**שורט, רווח 7, ימים 3 ו-4**.

??? tip "רמז"
    שורט הוא בדיוק "לונג הפוך": במקום המינימום עד כה, מה צריך לזכור?

??? success "פתרון סעיף ב"
    #### פתרון לא יעיל – \( O(n^2) \)

    לכל זוג ימים \( i < j \) מחשבים גם את רווח הלונג וגם את רווח השורט:

    === "SystemVerilog"
        ```systemverilog
        function automatic trade_t max_profit_brute(int prices[$]);
          trade_t best = '{0, "", -1, -1};
          int     long_profit, short_profit;

          for (int i = 0; i < prices.size(); i++)
            for (int j = i + 1; j < prices.size(); j++) begin
              long_profit  = prices[j] - prices[i];   // buy at i, sell at j
              short_profit = prices[i] - prices[j];   // sell at i, buy back at j

              if (long_profit > best.profit)
                best = '{long_profit, "long", i, j};
              if (short_profit > best.profit)
                best = '{short_profit, "short", i, j};
            end

          return best;
        endfunction
        ```

    === "Python"
        ```python
        def max_profit_brute(prices):
            best, kind, first, second = 0, None, None, None

            for i in range(len(prices)):
                for j in range(i + 1, len(prices)):
                    long_profit = prices[j] - prices[i]     # buy at i, sell at j
                    short_profit = prices[i] - prices[j]    # sell at i, buy back at j

                    if long_profit > best:
                        best, kind, first, second = long_profit, "long", i, j
                    if short_profit > best:
                        best, kind, first, second = short_profit, "short", i, j

            return best, kind, first, second
        ```

    #### פתרון יעיל – \( O(n) \)

    מריצים "שני סעיפי א" במקביל, באותה לולאה:

    - **בשביל הלונג:** זוכרים את **המינימום עד כה**, כי הכי טוב לקנות בזול ביותר.
    - **בשביל השורט:** זוכרים את **המקסימום עד כה**, כי הכי טוב למכור ביקר ביותר.

    בסוף מחזירים את הטוב מבין השניים:

    === "SystemVerilog"
        ```systemverilog
        function automatic trade_t max_profit_fast(int prices[$]);
          trade_t none = '{0, "", -1, -1};
          trade_t lng  = '{0, "long", -1, -1};
          trade_t sht  = '{0, "short", -1, -1};
          int     min_p, min_i;                 // cheapest price so far -> best day to open a long
          int     max_p, max_i;                 // highest price so far  -> best day to open a short

          if (prices.size() < 2) return none;
          min_p = prices[0];  min_i = 0;
          max_p = prices[0];  max_i = 0;

          foreach (prices[i]) begin
            if (prices[i] - min_p > lng.profit) begin
              lng.profit  = prices[i] - min_p;
              lng.open_i  = min_i;
              lng.close_i = i;
            end

            if (max_p - prices[i] > sht.profit) begin
              sht.profit  = max_p - prices[i];
              sht.open_i  = max_i;
              sht.close_i = i;
            end

            if (prices[i] < min_p) begin min_p = prices[i]; min_i = i; end
            if (prices[i] > max_p) begin max_p = prices[i]; max_i = i; end
          end

          if (sht.profit > lng.profit) return sht;
          if (lng.profit > 0)          return lng;
          return none;
        endfunction
        ```

    === "Python"
        ```python
        def max_profit_fast(prices):
            if len(prices) < 2:
                return 0, None, None, None

            min_p, min_i = prices[0], 0     # cheapest price so far  -> best day to open a long
            max_p, max_i = prices[0], 0     # highest price so far   -> best day to open a short

            long_best, long_open, long_close = 0, None, None
            short_best, short_open, short_close = 0, None, None

            for i, p in enumerate(prices):
                if p - min_p > long_best:
                    long_best = p - min_p
                    long_open, long_close = min_i, i

                if max_p - p > short_best:
                    short_best = max_p - p
                    short_open, short_close = max_i, i

                if p < min_p:
                    min_p, min_i = p, i
                if p > max_p:
                    max_p, max_i = p, i

            if short_best > long_best:
                return short_best, "short", short_open, short_close
            if long_best > 0:
                return long_best, "long", long_open, long_close
            return 0, None, None, None
        ```

    #### המחשה על הדוגמה

    הקו האפור הוא מחיר המניה. הקו הכחול הוא **המינימום עד כה**, שמשמש את הלונג, והקו
    הכתום הוא **המקסימום עד כה**, שמשמש את השורט. המקטעים המודגשים הם העסקה הטובה ביותר
    מכל סוג. מעבר עם העכבר על נקודה מציג את המחיר.

    <span class="viz-legend"><span><i class="ink"></i>מחיר המניה</span><span><i class="s1"></i>המינימום עד כה (לונג)</span><span><i class="s2"></i>המקסימום עד כה (שורט)</span></span>

    <svg class="perf-chart" viewBox="0 0 640 300" role="img" aria-label="גרף מחירי המניה לפי יום, עם המינימום והמקסימום עד כה ועסקאות הלונג והשורט הטובות ביותר"><line class="grid" x1="44" x2="600" y1="260.0" y2="260.0"/><text class="tick" x="36" y="264.0" text-anchor="end">0</text><line class="grid" x1="44" x2="600" y1="212.0" y2="212.0"/><text class="tick" x="36" y="216.0" text-anchor="end">2</text><line class="grid" x1="44" x2="600" y1="164.0" y2="164.0"/><text class="tick" x="36" y="168.0" text-anchor="end">4</text><line class="grid" x1="44" x2="600" y1="116.0" y2="116.0"/><text class="tick" x="36" y="120.0" text-anchor="end">6</text><line class="grid" x1="44" x2="600" y1="68.0" y2="68.0"/><text class="tick" x="36" y="72.0" text-anchor="end">8</text><line class="grid" x1="44" x2="600" y1="20.0" y2="20.0"/><text class="tick" x="36" y="24.0" text-anchor="end">10</text><text class="tick" x="44.0" y="286" text-anchor="middle" direction="rtl">יום 0</text><text class="tick" x="155.2" y="286" text-anchor="middle" direction="rtl">יום 1</text><text class="tick" x="266.4" y="286" text-anchor="middle" direction="rtl">יום 2</text><text class="tick" x="377.6" y="286" text-anchor="middle" direction="rtl">יום 3</text><text class="tick" x="488.8" y="286" text-anchor="middle" direction="rtl">יום 4</text><text class="tick" x="600.0" y="286" text-anchor="middle" direction="rtl">יום 5</text><path class="s1-line" d="M44.0,140.0 H155.2 V140.0 H266.4 V188.0 H377.6 V188.0 H488.8 V212.0 H600.0 V212.0" fill="none" stroke-width="2"/><path class="s2-line" d="M44.0,140.0 H155.2 V68.0 H266.4 V68.0 H377.6 V44.0 H488.8 V44.0 H600.0 V44.0" fill="none" stroke-width="2"/><line class="s1-line" x1="266.4" y1="188.0" x2="377.6" y2="44.0" stroke-width="8" opacity="0.35"/><line class="s2-line" x1="377.6" y1="44.0" x2="488.8" y2="212.0" stroke-width="8" opacity="0.35"/><path class="ink-line" d="M44.0,140.0 L155.2,68.0 L266.4,188.0 L377.6,44.0 L488.8,212.0 L600.0,116.0" fill="none" stroke-width="2"/><circle class="ink-dot" cx="44.0" cy="140.0" r="5"><title>יום 0: מחיר 5</title></circle><text class="tick" x="44.0" y="160.0" text-anchor="middle">5</text><circle class="ink-dot" cx="155.2" cy="68.0" r="5"><title>יום 1: מחיר 8</title></circle><text class="tick" x="155.2" y="57.0" text-anchor="middle">8</text><circle class="ink-dot" cx="266.4" cy="188.0" r="5"><title>יום 2: מחיר 3</title></circle><text class="tick" x="266.4" y="208.0" text-anchor="middle">3</text><circle class="ink-dot" cx="377.6" cy="44.0" r="5"><title>יום 3: מחיר 9</title></circle><text class="tick" x="377.6" y="33.0" text-anchor="middle">9</text><circle class="ink-dot" cx="488.8" cy="212.0" r="5"><title>יום 4: מחיר 2</title></circle><text class="tick" x="488.8" y="232.0" text-anchor="middle">2</text><circle class="ink-dot" cx="600.0" cy="116.0" r="5"><title>יום 5: מחיר 6</title></circle><text class="tick" x="600.0" y="105.0" text-anchor="middle">6</text><text class="legend" x="310.0" y="120.0" text-anchor="end">long +6</text><text class="legend" x="445.2" y="120.0" text-anchor="start">short +7 ✓</text></svg>

    #### מעקב אחרי הלולאה

    בכל יום מחשבים את הרווח האפשרי מול המינימום והמקסימום של הימים **הקודמים**, ורק אחר
    כך מעדכנים אותם. ✅ מסמן שיפור:

    | יום | מחיר | לונג היום (מחיר פחות מינימום) | הלונג הטוב (ימים) | שורט היום (מקסימום פחות מחיר) | השורט הטוב (ימים) | מינימום אחרי היום | מקסימום אחרי היום |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | 0 | 5 | 0 | 0 | 0 | 0 | 5 (יום 0) | 5 (יום 0) |
    | 1 | 8 | 3 ✅ | 3 (0→1) | ‎-3 | 0 | 5 (יום 0) | 8 (יום 1) |
    | 2 | 3 | ‎-2 | 3 (0→1) | 5 ✅ | 5 (1→2) | 3 (יום 2) | 8 (יום 1) |
    | 3 | 9 | 6 ✅ | 6 (2→3) | ‎-1 | 5 (1→2) | 3 (יום 2) | 9 (יום 3) |
    | 4 | 2 | ‎-1 | 6 (2→3) | 7 ✅ | 7 (3→4) | 2 (יום 4) | 9 (יום 3) |
    | 5 | 6 | 4 | 6 (2→3) | 3 | 7 (3→4) | 2 (יום 4) | 9 (יום 3) |

    בסוף, השורט (7) גדול מהלונג (6), ולכן התשובה היא **שורט ברווח 7, ימים 3 ו-4**.

    #### השוואה

    | | פתרון לא יעיל | פתרון יעיל |
    |-|---------------|------------|
    | זמן | \( O(n^2) \): כל הזוגות | \( O(n) \): מעבר אחד |
    | זיכרון נוסף | \( O(1) \) | \( O(1) \): ארבעה משתנים |
    | עבור מיליון ימים | כ-\( 5 \cdot 10^{11} \) זוגות | מיליון צעדים |

## נקודות חשובות ושאלות המשך

??? note "כמה זוגות ימים עם אותו רווח"
    כשיש כמה עסקאות עם אותו רווח מקסימלי, שתי הפונקציות עשויות להחזיר **זוג ימים שונה**,
    אבל תמיד את **אותו רווח**. הפונקציה הלא יעילה מחזירה את הזוג הראשון לפי הסדר
    \( (i, j) \). הפונקציה היעילה נצמדת למינימום או למקסימום **הראשונים** שהופיעו, כי
    העדכון מתבצע רק כשיש ערך קטן או גדול **ממש**. אם ללונג ולשורט יש אותו רווח, היא מעדיפה
    לונג. לכן בבדיקה אוטומטית משווים את הרווח, ובודקים שהימים שהוחזרו באמת נותנים אותו.

??? note "הקשר ל-DV"
    זה בדיוק המבנה של **reference model** טוב: הפתרון הלא יעיל פשוט מספיק כדי שיהיה קל
    לסמוך עליו, והפתרון היעיל הוא "ה-DUT". מריצים את שניהם על הרבה קלטים אקראיים ומשווים
    את הרווח, וכך נבדקה גם הגרסה שבעמוד הזה.

??? note "שאלות המשך"
    - **הרבה עסקאות:** אם מותר לבצע כמה עסקאות לונג שאינן חופפות, סוכמים את כל העליות בין
      יום ליום, ב-\( O(n) \).
    - **בדיוק \( k \) עסקאות:** פותרים בתכנות דינמי, ב-\( O(nk) \).
    - **עמלה על כל עסקה:** מוסיפים את העמלה לתנאי, ואם הרווח אחרי העמלה לא חיובי לא
      מבצעים עסקה.
