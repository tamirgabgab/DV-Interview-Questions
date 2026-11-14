---
id: 10
title: סוגריים תקינים
level: student
difficulty: easy
kind: code
tags: [algorithms, stack, python, systemverilog]
source: "LeetCode 20 – Valid Parentheses"
added: 2026-10-16
---

## השאלה

נתונה מחרוזת `s` שמכילה רק את התווים `(`, `)`, `[`, `]`, `{` ו-`}`. כתבו פונקציה שבודקת
האם המחרוזת **תקינה**. מחרוזת תקינה אם :

- **אותו סוג :** כל סוגר פותח נסגר על ידי סוגר מאותו סוג.
- **הסדר הנכון :** הסוגר שנפתח אחרון נסגר ראשון (LIFO). אסור ש-`[` ייסגר לפני `(`
  שנפתח אחריו.
- **אין עודפים :** לכל סוגר סוגר יש סוגר פותח מתאים לפניו, וכל סוגר פותח נסגר עד סוף
  המחרוזת.

המחרוזת הריקה נחשבת תקינה.

| מחרוזת | תקינה? | הסבר |
|---|---|---|
| ‏`()` | ✓ | זוג אחד |
| ‏`()[]{}` | ✓ | שלושה זוגות, אחד אחרי השני |
| ‏`{[()]}` | ✓ | זוגות מקוננים, כל אחד נסגר בסדר ההפוך לפתיחה |
| ‏`([]{})` | ✓ | בתוך הסוגריים העגולים יש שני זוגות נפרדים |
| ‏`(]` | ✗ | הסוגר הסוגר מסוג אחר |
| ‏`([)]` | ✗ | הסדר לא נכון : `(` נסגר לפני `[` שנפתח אחריו |
| ‏`(((` | ✗ | סוגריים שלא נסגרו |
| ‏`())` | ✗ | סוגר סוגר שאין לו פותח |
| ‏`)(` | ✗ | יש אותו מספר של פותחים וסוגרים, אבל הסוגר מגיע לפני הפותח |

??? interviewer "מה המראיין בודק"
    - **מבנה הנתונים הנכון :** האם המועמד מזהה איזו תכונה בהגדרה של "תקינה" מכתיבה את
      מבנה הנתונים, ולא רק סופר תווים.
    - **שלושה מקרי כישלון :** סוג לא מתאים, סוגר סוגר שאין לו פותח, ופותחים שנשארו פתוחים
      בסוף. קל לשכוח את האחרון.
    - **קיצורי דרך :** בדיקת אורך אי-זוגי היא זולה, אבל לא מחליפה את הבדיקה המלאה. למשל
      `)(` באורך זוגי ולא תקינה.
    - **ניתוח הפתרון הפשוט :** לדעת להסביר למה הוא \( O(n^2) \) ולתת קלט שמראה את זה.
    - **מעבר יחיד :** בפתרון היעיל, לנמק למה כל תו נבדק פעם אחת בלבד.

---

### סעיף א – פתרון פשוט

כתבו פתרון פשוט, גם אם הוא לא יעיל, ונתחו את הסיבוכיות שלו.

??? tip "רמז 1"
    נסו להקטין את הבעיה : איזו פעולה על מחרוזת תקינה משאירה מחרוזת **קצרה יותר** שגם היא
    תקינה? אם חוזרים עליה מספיק פעמים, במה אמורים להישאר?

??? tip "רמז 2"
    במחרוזת תקינה תמיד יש לפחות זוג אחד **צמוד**, כמו `()` או `[]`. מה קורה למחרוזת אם
    מוחקים אותו?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מוחקים זוגות צמודים `()`, `[]`, `{}` שוב ושוב, עד שמעבר שלם לא משנה כלום.
        **המחרוזת תקינה אם ורק אם נשארת מחרוזת ריקה.** הזמן הוא \( O(n^2) \).

    <!-- cost: זמן \( O(n^2) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    במחרוזת תקינה ולא ריקה תמיד יש זוג צמוד, ומחיקה שלו משאירה מחרוזת שתקינה אם ורק
    אם המקורית תקינה. לכן מוחקים זוגות צמודים שוב ושוב : אם בסוף נשארת מחרוזת ריקה,
    המחרוזת תקינה. אם נתקעים עם מחרוזת שאין בה אף זוג צמוד, היא לא תקינה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מעבר :** מוחקים מהמחרוזת את כל המופעים של `()`, אחר כך של `[]`, ואחר כך של `{}`.
    2. **לחזור :** כל עוד המעבר האחרון שינה את המחרוזת, עושים מעבר נוסף (מחיקה יכולה
       ליצור זוג צמוד חדש, למשל `(())` הופך ל-`()`).
    3. **להכריע :** אם נשארה מחרוזת ריקה היא תקינה, אחרת לא.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="isValid_brute" hl_lines="2 3"
        def isValid_brute(s: str) -> bool:
            while "()" in s or "[]" in s or "{}" in s:   # (1)!
                s = s.replace("()", "").replace("[]", "").replace("{}", "")   # (2)!
            return s == ""
        ```

        1. תנאי הלולאה הוא "יש עוד זוג צמוד למחוק", ולא "המחרוזת לא ריקה" : על `([)]` הלולאה
           לא נכנסת בכלל, ובלי זה היא הייתה אינסופית.
        2. ‏`replace` מוחק את כל המופעים הלא חופפים במעבר אחד, אבל זוג חדש שנוצר מהמחיקה
           (למשל `()` מתוך `(())`) מטופל רק במעבר הבא.

    === "SystemVerilog"
        ```systemverilog title="functions remove_pair and is_valid_brute" linenums="1" hl_lines="24 25"
        // Remove every non-overlapping occurrence of `pair`, scanning left to right
        // (the same as Python's str.replace(pair, ""))
        function automatic string remove_pair(string s, string pair);
          string out = "";
          int    i   = 0;
          while (i < s.len()) begin
            if (i + 1 < s.len() && s.substr(i, i + 1) == pair) begin   // (1)!
              i += 2;                             // skip the adjacent pair (2)
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
          end while (s != prev);                  // stop when a pass removed nothing (3)
          return s == "";   // (4)!
        endfunction
        ```

        1. ‏`substr(i, i + 1)` ב-SystemVerilog מקבל אינדקס התחלה **ואינדקס סוף כולל**, ולכן
           זה שני תווים (לא כמו `s[i:i+1]` ב-Python). הבדיקה `i + 1 < s.len()` מונעת גישה
           מעבר לסוף המחרוזת בתו האחרון.
        2. אחרי שמוחקים זוג מדלגים על שני התווים ולא ממשיכים מהתו השני שלו, כדי שהמופעים
           לא יחפפו. זה בדיוק מה ש-`str.replace` עושה, ולכן שתי הגרסאות מתנהגות אותו דבר.
        3. התנאי לעצירה הוא "מעבר שלם לא שינה כלום", ולא "המחרוזת ריקה" : מחרוזת לא תקינה
           כמו `([)]` לעולם לא תתרוקן, ובלי התנאי הזה הלולאה הייתה אינסופית.
        4. מחרוזת שנשארו בה תווים היא לא תקינה, גם אם היא קצרה : למשל `(` או `)(`.

    #### למה זה נכון { .sol-proof }

    במחרוזת תקינה ולא ריקה, הסוגר הפותח **האחרון** לפני הסוגר הסוגר הראשון חייב להיות
    צמוד אליו ומאותו סוג : בין שניהם אין סוגר פותח (הוא האחרון) ואין סוגר סוגר (ההוא
    הראשון), ולפי כלל LIFO הסוגר הסוגר הראשון סוגר את הפותח האחרון. לכן תמיד יש זוג
    צמוד, ומחיקה שלו משאירה מחרוזת שתקינה אם ורק אם המקורית תקינה. ומכאן גם הכיוון ההפוך,
    בניסוח השקול : מחרוזת לא ריקה **בלי** אף זוג צמוד אינה תקינה, כי לכל מחרוזת תקינה ולא
    ריקה יש זוג כזה. זה מכסה גם מחרוזות בלי אף סוגר סוגר, כמו `(((`.

    **דוגמה.** עבור `(((())))` כל מעבר מוחק רק את הזוג הפנימי, ולכן צריך 4 מעברים :

    | מעבר | לפני | אחרי |
    |---|---|---|
    | 1 | ‏`(((())))` | ‏`((()))` |
    | 2 | ‏`((()))` | ‏`(())` |
    | 3 | ‏`(())` | ‏`()` |
    | 4 | ‏`()` | (ריקה) ✓ |

    עבור `([)]` אין אף זוג צמוד, ולכן הלולאה נעצרת מיד והמחרוזת לא תקינה.

    #### סיבוכיות { .sol-cost }

    - **זמן :** כל מעבר עובר על כל המחרוזת, כלומר \( O(n) \). כל מעבר מוחק לפחות זוג אחד,
      ולכן יש עד \( n/2 \) מעברים. בסך הכול \( O(n^2) \).
    - **המקרה הגרוע :** סוגריים מקוננים מאותו סוג, \( k \) פעמים `(` ואחריהן \( k \) פעמים
      `)`. כל מעבר מוריד רק זוג אחד.
    - **זיכרון :** \( O(n) \), כי כל `replace` בונה מחרוזת חדשה.

---

### סעיף ב – פתרון יעיל

כתבו פתרון שעובר על המחרוזת **פעם אחת**.

??? tip "רמז 1"
    עוברים תו-תו משמאל לימין. מה המידע המינימלי שצריך לזכור על מה שכבר נקרא, כדי
    להחליט אם הסוגר הסוגר הבא חוקי? האם צריך לזכור את כל המחרוזת, או רק חלק ממנה?

??? tip "רמז 2"
    כשמגיע סוגר סוגר, רק סוגר פותח אחד יכול להתאים לו : האחרון שנפתח ועוד לא נסגר. איזה
    מבנה נתונים נותן תמיד את האיבר האחרון שנכנס?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **מחסנית (stack) :** סוגר פותח נדחף, סוגר סוגר חייב להתאים לראש המחסנית ומוציא
        אותו, ובסוף המחסנית חייבת להיות ריקה. מעבר אחד, \( O(n) \).

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    "האחרון שנפתח נסגר ראשון" זו בדיוק ההגדרה של מחסנית. כשמגיע סוגר סוגר, היחיד שיכול
    להתאים לו הוא הפותח האחרון שעדיין לא נסגר, כלומר ראש המחסנית, ולכן לא צריך לזכור
    שום דבר מעבר לפותחים הפתוחים.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סוגר פותח :** דוחפים אותו למחסנית.
    2. **סוגר סוגר :** בראש המחסנית חייב להיות הפותח מאותו סוג. אם המחסנית ריקה, או
       שבראשה סוג אחר, המחרוזת לא תקינה. אחרת מוציאים את הפותח מהמחסנית.
    3. **בסוף :** המחרוזת תקינה רק אם המחסנית ריקה, כלומר כל הפותחים נסגרו.

    </div>

    **קיצור דרך, לא חובה.** מחרוזת באורך אי-זוגי אף פעם לא תקינה, כי סוגריים באים בזוגות.
    הקוד בודק את זה לפני הלולאה וחוסך אותה, אבל הבדיקה לא מחליפה את שלושת הצעדים :
    `)(` באורך זוגי ולא תקינה.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="isValid" linenums="1" hl_lines="10 16"
        def isValid(s: str) -> bool:
            if len(s) % 2 == 1:          # odd length -> can never be valid
                return False

            pairs = {")": "(", "]": "[", "}": "{"}   # (1)!
            stack = []

            for ch in s:
                if ch in pairs:                              # closing bracket
                    if not stack or stack[-1] != pairs[ch]:  # empty or mismatch (2)
                        return False
                    stack.pop()
                else:                                        # opening bracket
                    stack.append(ch)

            return not stack             # valid only if every opener was closed (3)
        ```

        1. מילון מסוגר סוגר לפותח שלו עושה שתי עבודות : `ch in pairs` מזהה שזה סוגר סוגר,
           ו-`pairs[ch]` נותן את הפותח שצריך להיות בראש המחסנית.
        2. ‏`not stack` נבדק ראשון, ולכן `stack[-1]` לא ניגש לרשימה ריקה.
        3. רשימה ריקה היא `False`, ולכן `not stack` הוא בדיוק "כל הפותחים נסגרו". בלי השורה
           הזו `(((` הייתה עוברת.

    === "SystemVerilog"
        ```systemverilog title="function is_valid" linenums="1" hl_lines="15 22"
        function automatic bit is_valid(string s);
          byte stack[$] = {};   // (1)!
          byte want;                              // the opener that matches s[i]
          if (s.len() % 2 == 1) return 0;         // odd length -> can never be valid (2)

          for (int i = 0; i < s.len(); i++) begin
            case (s[i])
              ")":     want = "(";
              "]":     want = "[";
              "}":     want = "{";
              default: want = 0;                  // s[i] is an opening bracket
            endcase

            if (want != 0) begin                  // closing bracket
              if (stack.size() == 0 || stack[$] != want) return 0;   // empty or mismatch (3)
              void'(stack.pop_back());   // (4)!
            end else begin                        // opening bracket
              stack.push_back(s[i]);
            end
          end

          return stack.size() == 0;               // valid only if every opener was closed (5)
        endfunction
        ```

        1. תור (queue) משמש כמחסנית : `push_back` דוחף, `pop_back` מוציא, ו-`stack[$]` הוא
           האיבר האחרון, כלומר ראש המחסנית.
        2. קיצור דרך זול לפני הלולאה. הוא לא מחליף את הבדיקה המלאה : `)(` באורך זוגי ועדיין
           לא תקינה.
        3. שני מקרי כישלון בתנאי אחד. הסדר חשוב : בודקים קודם שהמחסנית לא ריקה, ורק אז
           ניגשים ל-`stack[$]`, כי `||` מפסיק לחשב אחרי תנאי ראשון שמתקיים.
        4. ‏`pop_back` מחזיר את האיבר שהוצא, ולא צריך אותו כאן. העטיפה ב-`void'()` אומרת
           במפורש שהערך נזרק, ומונעת אזהרה של הכלים.
        5. מקרה הכישלון השלישי, שקל לשכוח : `(((` עובר את כל הלולאה בלי תקלה, ורק כאן
           מתגלה שנשארו פותחים בלי סוגרים.

    #### למה זה נכון { .sol-proof }

    **האינווריאנט של הלולאה.** אחרי כל תו, המחסנית מכילה בדיוק את הפותחים שעוד לא נסגרו, מהישן
    לחדש. סוגר סוגר יכול לסגור רק את החדש שבהם (כלל LIFO), ולכן השוואה לראש המחסנית
    בודקת את כל שלושת התנאים : סוג תואם (ראש המחסנית מאותו סוג), סדר נכון (סוגרים רק את
    האחרון שנפתח) ואין עודפים (מחסנית ריקה כשמגיע סוגר, או מחסנית לא ריקה בסוף).

    **המחסנית צעד אחרי צעד.** לחצו "הבא" כדי לעקוב אחרי המחסנית תו אחרי תו, קודם על
    מחרוזת תקינה ואז על מחרוזת שנכשלת בגלל סדר הסגירה :

    <!-- gen 0 -->

    <div class="stepper" role="group" aria-label="המחסנית תו אחרי תו על {[()]}" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure" viewBox="0 0 442 190" style="max-width:28rem" role="img" aria-label="מצב המחסנית"><rect class="st-cell" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">{</text><rect class="st-cell" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><rect class="st-cell" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">(</text><rect class="st-cell" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">)</text><rect class="st-cell" x="200" y="36" width="40" height="40" rx="5"/><text class="st-text" x="220.0" y="63" text-anchor="middle">]</text><rect class="st-cell" x="246" y="36" width="40" height="40" rx="5"/><text class="st-text" x="266.0" y="63" text-anchor="middle">}</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="394" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="366" x2="422" y1="176" y2="176" stroke-width="2"/><text class="st-small" x="394" y="162" text-anchor="middle">empty</text></svg><figcaption>לפני הקריאה : המחרוזת שבאיור, והמחסנית ריקה.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 442 190" style="max-width:28rem" role="img" aria-label="מצב המחסנית"><rect class="st-cur" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">{</text><path class="s2-fill" d="M29.0,92 L43.0,92 L36.0,82 z"/><rect class="st-cell" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><rect class="st-cell" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">(</text><rect class="st-cell" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">)</text><rect class="st-cell" x="200" y="36" width="40" height="40" rx="5"/><text class="st-text" x="220.0" y="63" text-anchor="middle">]</text><rect class="st-cell" x="246" y="36" width="40" height="40" rx="5"/><text class="st-text" x="266.0" y="63" text-anchor="middle">}</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="394" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="366" x2="422" y1="176" y2="176" stroke-width="2"/><rect class="st-top" x="372" y="138" width="44" height="34" rx="5"/><text class="st-text" x="394" y="162" text-anchor="middle">{</text></svg><figcaption>תו 1 הוא פותח מסולסל, ולכן נדחף למחסנית.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 442 190" style="max-width:28rem" role="img" aria-label="מצב המחסנית"><rect class="st-done" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">{</text><rect class="st-cur" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><path class="s2-fill" d="M75.0,92 L89.0,92 L82.0,82 z"/><rect class="st-cell" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">(</text><rect class="st-cell" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">)</text><rect class="st-cell" x="200" y="36" width="40" height="40" rx="5"/><text class="st-text" x="220.0" y="63" text-anchor="middle">]</text><rect class="st-cell" x="246" y="36" width="40" height="40" rx="5"/><text class="st-text" x="266.0" y="63" text-anchor="middle">}</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="394" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="366" x2="422" y1="176" y2="176" stroke-width="2"/><rect class="st-stack" x="372" y="138" width="44" height="34" rx="5"/><text class="st-text" x="394" y="162" text-anchor="middle">{</text><rect class="st-top" x="372" y="100" width="44" height="34" rx="5"/><text class="st-text" x="394" y="124" text-anchor="middle">[</text></svg><figcaption>תו 2 הוא פותח מרובע, ולכן נדחף למחסנית.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 442 190" style="max-width:28rem" role="img" aria-label="מצב המחסנית"><rect class="st-done" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">{</text><rect class="st-done" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><rect class="st-cur" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">(</text><path class="s2-fill" d="M121.0,92 L135.0,92 L128.0,82 z"/><rect class="st-cell" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">)</text><rect class="st-cell" x="200" y="36" width="40" height="40" rx="5"/><text class="st-text" x="220.0" y="63" text-anchor="middle">]</text><rect class="st-cell" x="246" y="36" width="40" height="40" rx="5"/><text class="st-text" x="266.0" y="63" text-anchor="middle">}</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="394" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="366" x2="422" y1="176" y2="176" stroke-width="2"/><rect class="st-stack" x="372" y="138" width="44" height="34" rx="5"/><text class="st-text" x="394" y="162" text-anchor="middle">{</text><rect class="st-stack" x="372" y="100" width="44" height="34" rx="5"/><text class="st-text" x="394" y="124" text-anchor="middle">[</text><rect class="st-top" x="372" y="62" width="44" height="34" rx="5"/><text class="st-text" x="394" y="86" text-anchor="middle">(</text></svg><figcaption>תו 3 הוא פותח עגול, ולכן נדחף למחסנית.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 442 190" style="max-width:28rem" role="img" aria-label="מצב המחסנית"><rect class="st-done" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">{</text><rect class="st-done" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><rect class="st-done" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">(</text><rect class="st-cur" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">)</text><path class="s2-fill" d="M167.0,92 L181.0,92 L174.0,82 z"/><rect class="st-cell" x="200" y="36" width="40" height="40" rx="5"/><text class="st-text" x="220.0" y="63" text-anchor="middle">]</text><rect class="st-cell" x="246" y="36" width="40" height="40" rx="5"/><text class="st-text" x="266.0" y="63" text-anchor="middle">}</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="394" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="366" x2="422" y1="176" y2="176" stroke-width="2"/><rect class="st-stack" x="372" y="138" width="44" height="34" rx="5"/><text class="st-text" x="394" y="162" text-anchor="middle">{</text><rect class="st-top" x="372" y="100" width="44" height="34" rx="5"/><text class="st-text" x="394" y="124" text-anchor="middle">[</text></svg><figcaption>תו 4 הוא סוגר עגול. בראש המחסנית פותח עגול, מתאים, ולכן הוא מוצא מהמחסנית.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 442 190" style="max-width:28rem" role="img" aria-label="מצב המחסנית"><rect class="st-done" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">{</text><rect class="st-done" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><rect class="st-done" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">(</text><rect class="st-done" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">)</text><rect class="st-cur" x="200" y="36" width="40" height="40" rx="5"/><text class="st-text" x="220.0" y="63" text-anchor="middle">]</text><path class="s2-fill" d="M213.0,92 L227.0,92 L220.0,82 z"/><rect class="st-cell" x="246" y="36" width="40" height="40" rx="5"/><text class="st-text" x="266.0" y="63" text-anchor="middle">}</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="394" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="366" x2="422" y1="176" y2="176" stroke-width="2"/><rect class="st-top" x="372" y="138" width="44" height="34" rx="5"/><text class="st-text" x="394" y="162" text-anchor="middle">{</text></svg><figcaption>תו 5 הוא סוגר מרובע. בראש המחסנית פותח מרובע, מתאים, ולכן הוא מוצא מהמחסנית.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 442 190" style="max-width:28rem" role="img" aria-label="מצב המחסנית"><rect class="st-done" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">{</text><rect class="st-done" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><rect class="st-done" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">(</text><rect class="st-done" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">)</text><rect class="st-done" x="200" y="36" width="40" height="40" rx="5"/><text class="st-text" x="220.0" y="63" text-anchor="middle">]</text><rect class="st-cur" x="246" y="36" width="40" height="40" rx="5"/><text class="st-text" x="266.0" y="63" text-anchor="middle">}</text><path class="s2-fill" d="M259.0,92 L273.0,92 L266.0,82 z"/><text class="st-small" x="16" y="24">input</text><text class="st-small" x="394" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="366" x2="422" y1="176" y2="176" stroke-width="2"/><text class="st-small" x="394" y="162" text-anchor="middle">empty</text></svg><figcaption>תו 6 הוא סוגר מסולסל. בראש המחסנית פותח מסולסל, מתאים, ולכן הוא מוצא מהמחסנית.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 442 190" style="max-width:28rem" role="img" aria-label="מצב המחסנית"><rect class="st-done" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">{</text><rect class="st-done" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><rect class="st-done" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">(</text><rect class="st-done" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">)</text><rect class="st-done" x="200" y="36" width="40" height="40" rx="5"/><text class="st-text" x="220.0" y="63" text-anchor="middle">]</text><rect class="st-done" x="246" y="36" width="40" height="40" rx="5"/><text class="st-text" x="266.0" y="63" text-anchor="middle">}</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="394" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="366" x2="422" y1="176" y2="176" stroke-width="2"/><text class="st-small" x="394" y="162" text-anchor="middle">empty</text></svg><figcaption>סוף המחרוזת והמחסנית ריקה : כל פותח נסגר, המחרוזת תקינה ✓</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="8"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <!-- /gen -->

    <!-- gen 1 -->

    <div class="stepper" role="group" aria-label="המחסנית תו אחרי תו על ([)]" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure" viewBox="0 0 360 190" style="max-width:22rem" role="img" aria-label="מצב המחסנית"><rect class="st-cell" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">(</text><rect class="st-cell" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><rect class="st-cell" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">)</text><rect class="st-cell" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">]</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="312" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="284" x2="340" y1="176" y2="176" stroke-width="2"/><text class="st-small" x="312" y="162" text-anchor="middle">empty</text></svg><figcaption>לפני הקריאה : המחרוזת שבאיור, והמחסנית ריקה.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 360 190" style="max-width:22rem" role="img" aria-label="מצב המחסנית"><rect class="st-cur" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">(</text><path class="s2-fill" d="M29.0,92 L43.0,92 L36.0,82 z"/><rect class="st-cell" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><rect class="st-cell" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">)</text><rect class="st-cell" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">]</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="312" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="284" x2="340" y1="176" y2="176" stroke-width="2"/><rect class="st-top" x="290" y="138" width="44" height="34" rx="5"/><text class="st-text" x="312" y="162" text-anchor="middle">(</text></svg><figcaption>תו 1 הוא פותח עגול, ולכן נדחף למחסנית.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 360 190" style="max-width:22rem" role="img" aria-label="מצב המחסנית"><rect class="st-done" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">(</text><rect class="st-cur" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><path class="s2-fill" d="M75.0,92 L89.0,92 L82.0,82 z"/><rect class="st-cell" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">)</text><rect class="st-cell" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">]</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="312" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="284" x2="340" y1="176" y2="176" stroke-width="2"/><rect class="st-stack" x="290" y="138" width="44" height="34" rx="5"/><text class="st-text" x="312" y="162" text-anchor="middle">(</text><rect class="st-top" x="290" y="100" width="44" height="34" rx="5"/><text class="st-text" x="312" y="124" text-anchor="middle">[</text></svg><figcaption>תו 2 הוא פותח מרובע, ולכן נדחף למחסנית.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 360 190" style="max-width:22rem" role="img" aria-label="מצב המחסנית"><rect class="st-done" x="16" y="36" width="40" height="40" rx="5"/><text class="st-text" x="36.0" y="63" text-anchor="middle">(</text><rect class="st-done" x="62" y="36" width="40" height="40" rx="5"/><text class="st-text" x="82.0" y="63" text-anchor="middle">[</text><rect class="st-bad" x="108" y="36" width="40" height="40" rx="5"/><text class="st-text" x="128.0" y="63" text-anchor="middle">)</text><path class="s2-fill" d="M121.0,92 L135.0,92 L128.0,82 z"/><rect class="st-cell" x="154" y="36" width="40" height="40" rx="5"/><text class="st-text" x="174.0" y="63" text-anchor="middle">]</text><text class="st-small" x="16" y="24">input</text><text class="st-small" x="312" y="24" text-anchor="middle">stack</text><line class="ink-line" x1="284" x2="340" y1="176" y2="176" stroke-width="2"/><rect class="st-stack" x="290" y="138" width="44" height="34" rx="5"/><text class="st-text" x="312" y="162" text-anchor="middle">(</text><rect class="st-bad" x="290" y="100" width="44" height="34" rx="5"/><text class="st-text" x="312" y="124" text-anchor="middle">[</text></svg><figcaption>תו 3 הוא סוגר עגול, אבל בראש המחסנית פותח מרובע ולא פותח עגול. סדר הסגירה שגוי : המחרוזת לא תקינה ✗</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="4"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <!-- /gen -->

    **נסו בעצמכם.** התיבה מוסיפה על האיורים מחרוזות משלכם ומקרי מלכודת, עם גרף העומק
    והמעברים של סעיף א על אותה מחרוזת. הקלידו מחרוזת אחת לכל סיבת כישלון : סוג לא מתאים,
    סוגר בלי פותח, ופותחים שנשארו בסוף, ונחשו באיזה תו כל אחת תיכשל לפני שאתם מריצים.
    ואחת רביעית : מחרוזת באורך זוגי שבכל זאת נכשלת.

    <div class="explorer" data-kind="brackets" data-s="{[()]}"></div>

    #### סיבוכיות { .sol-cost }

    - **זמן :** \( O(n) \). כל תו נדחף או נבדק פעם אחת, וכל פעולה על המחסנית היא \( O(1) \).
    - **זיכרון :** \( O(n) \) במקרה הגרוע, למשל `((((((` שבה כל התווים נדחפים.

    **כמה זה משנה?** על הקלט הגרוע של הפתרון הפשוט, \( n/2 \) פעמים `(` ואחריהן \( n/2 \)
    פעמים `)`, הפתרון הפשוט עושה \( n/2 \) מעברים, וכל מעבר קורא את כל מה שנשאר מהמחרוזת.
    המחסנית קוראת כל תו פעם אחת :

    <!-- gen 2 -->

    | אורך \( n \) | מעברים בפתרון הפשוט | תווים שנקראו : פשוט | תווים שנקראו : מחסנית | פי כמה |
    |---|---|---|---|---|
    | 10 | 5 | 30 | 10 | 3 |
    | 100 | 50 | 2,550 | 100 | 25 |
    | 1,000 | 500 | 250,500 | 1,000 | 250 |
    | 10,000 | 5,000 | 25,005,000 | 10,000 | 2,500 |
    | 100,000 | 50,000 | 2,500,050,000 | 100,000 | 25,000 |

    <!-- /gen -->

    במדידה ב-Python, על מחרוזת של 100,000 תווים, הפתרון הפשוט לוקח כמה שניות והמחסנית כמה
    אלפיות שנייה, כלומר היא מהירה פי כמה אלפים (המספרים המדויקים תלויים במחשב). הפער קטן
    מפי 25,000 של הטבלה, כי `replace` רץ בקוד מהודר וקורא כל תו מהר יותר מהלולאה של המחסנית ב-Python.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לספור במקום לזכור"
    פתרון מפתה הוא לספור פותחים וסוגרים ולבדוק שהמונים שווים. זה מפספס את הסדר (`)(`
    עובר) ואת הסוג (`(]` עובר אם סופרים את כל הסוגריים יחד, ו-`([)]` עובר גם עם מונה
    לכל סוג). צריך לזכור **אילו** פותחים פתוחים ובאיזה סדר, וזה בדיוק מה שהמחסנית עושה.

??? trap "מלכודת : לשכוח את הבדיקה בסוף"
    מחרוזת כמו `(((` או `{[` עוברת את כל הלולאה בלי אף כישלון, כי אין בה סוגר סוגר. רק
    הבדיקה שהמחסנית ריקה בסוף תופסת אותה. גם בפתרון הפשוט המקבילה היא לבדוק שנשארה
    מחרוזת ריקה, ולא רק שהלולאה נעצרה.

??? followup "שאלות המשך"
    - **רק סוג אחד של סוגריים :** האם צריך מחסנית?

        ??? fu-answer "תשובה"
            לא, מספיק מונה. מוסיפים 1 על `(`, מורידים 1 על `)`, והמחרוזת תקינה אם המונה אף פעם
            לא שלילי ובסוף הוא 0. זיכרון \( O(1) \).

    - **בחומרה :** איך בודקים זרם של תווים, תו אחד בכל מחזור שעון?

        ??? fu-answer "תשובה"
            עם סוג אחד, אותו מונה הוא FSM פשוט. עם כמה סוגים צריך זיכרון LIFO, 2 ביט לכל רמה,
            בעומק של הקינון המקסימלי (לכל היותר \( n/2 \)). ב-overflow אי אפשר להמשיך לבדוק,
            ולכן מעלים דגל שגיאה במקום לענות "תקינה".

    - **הסוגריים התקינים הארוכים ביותר :** מצאו את אורך תת-המחרוזת התקינה הארוכה ביותר
      (LeetCode 32).

        ??? fu-answer "תשובה"
            מחסנית של **אינדקסים** עם \( -1 \) בתחתית : `(` דוחף את האינדקס, `)` מוציא, ואם
            המחסנית התרוקנה דוחפים את האינדקס של ה-`)` כתחתית חדשה; אחרת האורך הוא \( i \) פחות
            הראש. ‏\( O(n) \); למשל עבור `)()())` התשובה 4.
