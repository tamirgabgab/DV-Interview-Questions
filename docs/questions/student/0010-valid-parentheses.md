---
id: 10
title: סוגריים תקינים
level: student
difficulty: easy
tags: [algorithms, stack, python, systemverilog]
source: "LeetCode 20 – Valid Parentheses"
added: 2026-10-16
---

## השאלה

נתונה מחרוזת `s` שמכילה רק את התווים `(`, `)`, `[`, `]`, `{` ו-`}`. כתבו פונקציה שבודקת
האם המחרוזת **תקינה**. מחרוזת תקינה אם:

- **אותו סוג:** כל סוגר פותח נסגר על ידי סוגר מאותו סוג.
- **הסדר הנכון:** הסוגר שנפתח אחרון נסגר ראשון (LIFO). אסור ש-`[` ייסגר לפני `(`
  שנפתח אחריו.
- **אין עודפים:** לכל סוגר סוגר יש סוגר פותח מתאים לפניו, וכל סוגר פותח נסגר עד סוף
  המחרוזת.

המחרוזת הריקה נחשבת תקינה.

| מחרוזת | תקינה? | הסבר |
|---|---|---|
| `()` | ✓ | זוג אחד |
| `()[]{}` | ✓ | שלושה זוגות, אחד אחרי השני |
| `{[()]}` | ✓ | זוגות מקוננים, כל אחד נסגר בסדר ההפוך לפתיחה |
| `([]{})` | ✓ | בתוך הסוגריים העגולים יש שני זוגות נפרדים |
| `(]` | ✗ | הסוגר הסוגר מסוג אחר |
| `([)]` | ✗ | הסדר לא נכון: `(` נסגר לפני `[` שנפתח אחריו |
| `(((` | ✗ | סוגריים שלא נסגרו |
| `())` | ✗ | סוגר סוגר שאין לו פותח |
| `)(` | ✗ | יש אותו מספר של פותחים וסוגרים, אבל הסוגר מגיע לפני הפותח |

---

### סעיף א – פתרון פשוט

כתבו פתרון פשוט, גם אם הוא לא יעיל, ונתחו את הסיבוכיות שלו.

??? tip "רמז"
    במחרוזת תקינה תמיד יש לפחות זוג אחד **צמוד**, כמו `()` או `[]`. מה קורה למחרוזת אם
    מוחקים אותו?

??? success "פתרון סעיף א"
    #### הרעיון: למחוק זוגות צמודים עד שאין יותר

    במחרוזת תקינה ולא ריקה, הסוגר הפותח **האחרון** לפני הסוגר הסוגר הראשון חייב להיות
    צמוד אליו ומאותו סוג. לכן תמיד יש זוג צמוד, ומחיקה שלו משאירה מחרוזת שתקינה אם ורק
    אם המקורית תקינה. מוחקים זוגות צמודים שוב ושוב: אם בסוף נשארת מחרוזת ריקה, המחרוזת
    תקינה. אם נתקעים עם מחרוזת שאין בה אף זוג צמוד, היא לא תקינה.

    === "SystemVerilog"
        ```systemverilog
        // Remove every non-overlapping occurrence of `pair`, scanning left to right
        // (the same as Python's str.replace(pair, ""))
        function automatic string remove_pair(string s, string pair);
          string out = "";
          int    i   = 0;
          while (i < s.len()) begin
            if (i + 1 < s.len() && s.substr(i, i + 1) == pair) begin
              i += 2;                             // skip the adjacent pair
            end else begin
              out = {out, s.substr(i, i)};
              i++;
            end
          end
          return out;
        endfunction

        function automatic bit is_valid_brute(string s);
          string prev;
          do begin
            prev = s;
            s = remove_pair(s, "()");
            s = remove_pair(s, "[]");
            s = remove_pair(s, "{}");
          end while (s != prev);                  // stop when a pass removed nothing
          return s == "";
        endfunction
        ```

    === "Python"
        ```python
        def isValid_brute(s: str) -> bool:
            while "()" in s or "[]" in s or "{}" in s:
                s = s.replace("()", "").replace("[]", "").replace("{}", "")
            return s == ""
        ```

    #### דוגמה

    עבור `(((())))` כל מעבר מוחק רק את הזוג הפנימי, ולכן צריך 4 מעברים:

    | מעבר | לפני | אחרי |
    |---|---|---|
    | 1 | `(((())))` | `((()))` |
    | 2 | `((()))` | `(())` |
    | 3 | `(())` | `()` |
    | 4 | `()` | (ריקה) ✓ |

    עבור `([)]` אין אף זוג צמוד, ולכן הלולאה נעצרת מיד והמחרוזת לא תקינה.

    #### סיבוכיות

    - **זמן:** כל מעבר עובר על כל המחרוזת, כלומר \( O(n) \). כל מעבר מוחק לפחות זוג אחד,
      ולכן יש עד \( n/2 \) מעברים. בסך הכול \( O(n^2) \).
    - **המקרה הגרוע:** סוגריים מקוננים מאותו סוג, \( k \) פעמים `(` ואחריהן \( k \) פעמים
      `)`. כל מעבר מוריד רק זוג אחד.
    - **זיכרון:** \( O(n) \), כי כל `replace` בונה מחרוזת חדשה.

---

### סעיף ב – פתרון יעיל

כתבו פתרון שעובר על המחרוזת **פעם אחת**.

??? tip "רמז"
    כשמגיע סוגר סוגר, רק סוגר פותח אחד יכול להתאים לו: האחרון שנפתח ועוד לא נסגר. איזה
    מבנה נתונים נותן תמיד את האיבר האחרון שנכנס?

??? success "פתרון סעיף ב"
    #### הרעיון: מחסנית (stack)

    עוברים על התווים משמאל לימין:

    - **סוגר פותח:** דוחפים אותו למחסנית.
    - **סוגר סוגר:** בראש המחסנית חייב להיות הפותח מאותו סוג. אם המחסנית ריקה, או שבראשה
      סוג אחר, המחרוזת לא תקינה. אחרת מוציאים את הפותח מהמחסנית.
    - **בסוף:** המחרוזת תקינה רק אם המחסנית ריקה, כלומר כל הפותחים נסגרו.

    בדיקה מקדימה: מחרוזת באורך אי-זוגי אף פעם לא תקינה, כי סוגריים באים בזוגות.

    === "SystemVerilog"
        ```systemverilog
        function automatic bit is_valid(string s);
          byte stack[$] = {};
          byte want;                              // the opener that matches s[i]
          if (s.len() % 2 == 1) return 0;         // odd length -> can never be valid

          for (int i = 0; i < s.len(); i++) begin
            case (s[i])
              ")":     want = "(";
              "]":     want = "[";
              "}":     want = "{";
              default: want = 0;                  // s[i] is an opening bracket
            endcase

            if (want != 0) begin                  // closing bracket
              if (stack.size() == 0 || stack[$] != want) return 0;   // empty or mismatch
              void'(stack.pop_back());
            end else begin                        // opening bracket
              stack.push_back(s[i]);
            end
          end

          return stack.size() == 0;               // valid only if every opener was closed
        endfunction
        ```

    === "Python"
        ```python
        def isValid(s: str) -> bool:
            if len(s) % 2 == 1:          # odd length -> can never be valid
                return False

            pairs = {")": "(", "]": "[", "}": "{"}
            stack = []

            for ch in s:
                if ch in pairs:                              # closing bracket
                    if not stack or stack[-1] != pairs[ch]:  # empty or mismatch
                        return False
                    stack.pop()
                else:                                        # opening bracket
                    stack.append(ch)

            return not stack             # valid only if every opener was closed
        ```

    #### דוגמה: המחסנית אחרי כל תו

    עבור `{[()]}`:

    | תו | פעולה | המחסנית |
    |---|---|---|
    | `{` | דחיפה | <span class="arr"><span>{</span></span> |
    | `[` | דחיפה | <span class="arr"><span>{</span><span>[</span></span> |
    | `(` | דחיפה | <span class="arr"><span>{</span><span>[</span><span class="hl">(</span></span> |
    | `)` | בראש `(`, מתאים, הוצאה | <span class="arr"><span>{</span><span>[</span></span> |
    | `]` | בראש `[`, מתאים, הוצאה | <span class="arr"><span>{</span></span> |
    | `}` | בראש `{`, מתאים, הוצאה | (ריקה) ✓ |

    עבור `([)]`:

    | תו | פעולה | המחסנית |
    |---|---|---|
    | `(` | דחיפה | <span class="arr"><span>(</span></span> |
    | `[` | דחיפה | <span class="arr"><span>(</span><span class="hl">[</span></span> |
    | `)` | בראש `[`, לא מתאים ל-`(` | לא תקינה ✗ |

    #### סיבוכיות

    - **זמן:** \( O(n) \). כל תו נדחף או נבדק פעם אחת, וכל פעולה על המחסנית היא \( O(1) \).
    - **זיכרון:** \( O(n) \) במקרה הגרוע, למשל `((((((` שבה כל התווים נדחפים.

    #### כמה זה משנה?

    על הקלט הגרוע של הפתרון הפשוט, \( n/2 \) פעמים `(` ואחריהן \( n/2 \) פעמים `)`, הפתרון
    הפשוט עושה \( n/2 \) מעברים, וכל מעבר קורא את כל מה שנשאר מהמחרוזת. המחסנית קוראת כל תו
    פעם אחת:

    | אורך \( n \) | מעברים בפתרון הפשוט | תווים שנקראו: פשוט | תווים שנקראו: מחסנית | פי כמה |
    |---|---|---|---|---|
    | 10 | 5 | 30 | 10 | 3 |
    | 100 | 50 | 2,550 | 100 | 25 |
    | 1,000 | 500 | 250,500 | 1,000 | 250 |
    | 10,000 | 5,000 | 25,005,000 | 10,000 | 2,500 |
    | 100,000 | 50,000 | 2,500,050,000 | 100,000 | 25,000 |

    <span class="viz-legend"><span><i class="by-enum"></i>פתרון פשוט: מחיקת זוגות</span><span><i class="by-multiples"></i>פתרון יעיל: מחסנית</span></span>

    <svg class="perf-chart" viewBox="0 0 640 280" role="img" aria-label="מספר התווים שכל פתרון קורא, בסקאלה לוגריתמית"><line class="grid" x1="64" x2="630" y1="240.0" y2="240.0"/><text class="tick" x="56" y="244.0" text-anchor="end">10<tspan dy="-5" font-size="9">0</tspan></text><line class="grid" x1="64" x2="630" y1="217.6" y2="217.6"/><text class="tick" x="56" y="221.6" text-anchor="end">10<tspan dy="-5" font-size="9">1</tspan></text><line class="grid" x1="64" x2="630" y1="195.2" y2="195.2"/><text class="tick" x="56" y="199.2" text-anchor="end">10<tspan dy="-5" font-size="9">2</tspan></text><line class="grid" x1="64" x2="630" y1="172.8" y2="172.8"/><text class="tick" x="56" y="176.8" text-anchor="end">10<tspan dy="-5" font-size="9">3</tspan></text><line class="grid" x1="64" x2="630" y1="150.4" y2="150.4"/><text class="tick" x="56" y="154.4" text-anchor="end">10<tspan dy="-5" font-size="9">4</tspan></text><line class="grid" x1="64" x2="630" y1="128.0" y2="128.0"/><text class="tick" x="56" y="132.0" text-anchor="end">10<tspan dy="-5" font-size="9">5</tspan></text><line class="grid" x1="64" x2="630" y1="105.6" y2="105.6"/><text class="tick" x="56" y="109.6" text-anchor="end">10<tspan dy="-5" font-size="9">6</tspan></text><line class="grid" x1="64" x2="630" y1="83.2" y2="83.2"/><text class="tick" x="56" y="87.2" text-anchor="end">10<tspan dy="-5" font-size="9">7</tspan></text><line class="grid" x1="64" x2="630" y1="60.8" y2="60.8"/><text class="tick" x="56" y="64.8" text-anchor="end">10<tspan dy="-5" font-size="9">8</tspan></text><line class="grid" x1="64" x2="630" y1="38.4" y2="38.4"/><text class="tick" x="56" y="42.4" text-anchor="end">10<tspan dy="-5" font-size="9">9</tspan></text><line class="grid" x1="64" x2="630" y1="16.0" y2="16.0"/><text class="tick" x="56" y="20.0" text-anchor="end">10<tspan dy="-5" font-size="9">10</tspan></text><rect class="bar by-enum" x="86.6" y="206.9" width="34.0" height="33.1"><title>n = 10: pair removal reads 30</title></rect><rect class="bar by-multiples" x="120.6" y="217.6" width="34.0" height="22.4"><title>n = 10: stack reads 10</title></rect><text class="tick" x="120.6" y="258" text-anchor="middle">n = 10</text><rect class="bar by-enum" x="199.8" y="163.7" width="34.0" height="76.3"><title>n = 100: pair removal reads 2,550</title></rect><rect class="bar by-multiples" x="233.8" y="195.2" width="34.0" height="44.8"><title>n = 100: stack reads 100</title></rect><text class="tick" x="233.8" y="258" text-anchor="middle">n = 100</text><rect class="bar by-enum" x="313.0" y="119.1" width="34.0" height="120.9"><title>n = 1,000: pair removal reads 250,500</title></rect><rect class="bar by-multiples" x="347.0" y="172.8" width="34.0" height="67.2"><title>n = 1,000: stack reads 1,000</title></rect><text class="tick" x="347.0" y="258" text-anchor="middle">n = 1,000</text><rect class="bar by-enum" x="426.2" y="74.3" width="34.0" height="165.7"><title>n = 10,000: pair removal reads 25,005,000</title></rect><rect class="bar by-multiples" x="460.2" y="150.4" width="34.0" height="89.6"><title>n = 10,000: stack reads 10,000</title></rect><text class="tick" x="460.2" y="258" text-anchor="middle">n = 10,000</text><rect class="bar by-enum" x="539.4" y="29.5" width="34.0" height="210.5"><title>n = 100,000: pair removal reads 2,500,050,000</title></rect><rect class="bar by-multiples" x="573.4" y="128.0" width="34.0" height="112.0"><title>n = 100,000: stack reads 100,000</title></rect><text class="tick" x="573.4" y="258" text-anchor="middle">n = 100,000</text><line class="axis" x1="64" x2="630" y1="240" y2="240"/></svg>

    במדידה ב-Python, על מחרוזת של 100,000 תווים, הפתרון הפשוט לקח כ-7 שניות, והמחסנית
    פחות מ-10 מילישניות.

## נקודות חשובות ושאלות המשך

??? note "נקודות שהמראיין מחפש"
    - **לזהות LIFO:** "האחרון שנפתח נסגר ראשון" זו בדיוק ההגדרה של מחסנית.
    - **שלושה מקרי כישלון:** סוג לא מתאים, סוגר סוגר כשהמחסנית ריקה, ומחסנית לא ריקה
      בסוף. קל לשכוח את האחרון.
    - **בדיקת אורך אי-זוגי:** קיצור דרך זול, אבל לא מחליף את הבדיקה המלאה. למשל `)(`
      באורך זוגי ולא תקינה.
    - **ניתוח הפתרון הפשוט:** לדעת להסביר למה הוא \( O(n^2) \) ולתת קלט שמראה את זה.

??? note "שאלות המשך"
    - **רק סוג אחד של סוגריים:** אפשר בלי מחסנית, עם מונה בלבד. מוסיפים 1 על `(`, מורידים 1
      על `)`, והמחרוזת תקינה אם המונה אף פעם לא שלילי ובסוף הוא 0. זיכרון \( O(1) \).
    - **בחומרה:** אותו מונה הוא FSM פשוט שבודק זרם של תווים, תו אחד בכל מחזור שעון. עם כמה
      סוגים צריך זיכרון LIFO, ואז שואלים מה העומק המקסימלי ומה קורה ב-overflow.
    - **הסוגריים התקינים הארוכים ביותר:** מצאו את אורך תת-המחרוזת התקינה הארוכה ביותר
      (LeetCode 32).
