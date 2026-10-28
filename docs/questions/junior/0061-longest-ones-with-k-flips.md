---
id: 61
title: הרצף הארוך ביותר של אחדות – עד k היפוכים, ואז כל ערך על ה-bus
level: junior
difficulty: medium
kind: code
tags: [algorithms, python, systemverilog]
source: "Meta (Max Consecutive Ones III), וההכללה של סעיף ב היא Longest Repeating Character Replacement"
added: 2026-10-28
---

## השאלה

נתון וקטור של \( n \) ביטים ומספר \( k \ge 0 \). מותר להפוך עד \( k \) אפסים לאחדות. מה האורך
של רצף האחדות הארוך ביותר שאפשר לקבל?

דוגמה : בווקטור <span dir="ltr">1 1 1 0 0 0 1 1 1 1 0</span> עם \( k = 2 \) התשובה היא 6. הופכים
את שני האפסים במקומות 4 ו-5 (סופרים מ-0), ומקבלים שישה אחדות רצופים במקומות 4 עד 9.

**ההקשר באימות :** אות `valid` שנדגם בכל מחזור. חלון שבו ה-`valid` דולק, כשמותר לסבול בתוכו
עד \( k \) מחזורים של stall, הוא בדיוק חלון עם לכל היותר \( k \) אפסים. מוניטור שמחפש את ה-burst
הארוך ביותר בטרייס עונה על השאלה הזו.

- **סעיף א – ביטים :** כתבו פונקציה שמחזירה את האורך, בזמן ליניארי ובזיכרון קבוע.
- **סעיף ב – כל ערך על ה-bus :** במקום ביטים, רצף של ערכים (למשל ה-opcode על bus בכל מחזור,
  או אותיות). מותר להחליף עד \( k \) ערכים. מה החלון הארוך ביותר שכולו ערך אחד?

??? interviewer "מה המראיין בודק"
    - **חלון במקום נקודת התחלה :** האם המועמד רואה שהתשובה היא קטע רציף, ומנסח מה מאפיין קטע
      חוקי (לכל היותר \( k \) אפסים) לפני שהוא כותב קוד.
    - **שני מצביעים שזזים רק קדימה :** למה הקצה השמאלי לא צריך לחזור אחורה. זה מה שנותן
      \( O(n) \) במקום \( O(n^2) \).
    - **ההכללה :** מה "האפסים בחלון" הופכים להיות כשיש יותר משני ערכים (אורך החלון פחות הערך
      הנפוץ ביותר בו).
    - **מקרי קצה :** ‏\( k = 0 \), ‏\( k \) גדול ממספר האפסים, וקטור ריק.

---

### סעיף א – ביטים, עד k היפוכים

??? tip "רמז 1"
    כל תשובה אפשרית היא קטע רציף של הווקטור. מה חייב להתקיים בקטע כדי שאפשר יהיה להפוך אותו
    לכולו אחדות?

??? tip "רמז 2"
    החזיקו קצה ימני וקצה שמאלי. הזיזו את הימני ביט אחרי ביט, וספרו כמה אפסים יש ביניהם. מתי
    צריך להזיז את השמאלי, ועד לאן?

<div class="selfcheck" data-answer="5" data-show="5 : המקומות 5 עד 9, ‏1 0 1 1 1 עם האפס שבמקום 6 הפוך" data-hint="חפשו את הקטע הארוך ביותר שיש בו אפס אחד לכל היותר. הוא נגמר בשלושת האחדות שבסוף." markdown>
בווקטור <span dir="ltr">1 0 1 1 0 1 0 1 1 1</span> עם \( k = 1 \), מה האורך של הרצף הארוך ביותר?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        חלון נע עם שני מצביעים. הקצה הימני מתקדם ביט אחרי ביט, ומונה סופר את האפסים שבחלון.
        כשיש בחלון יותר מ-\( k \) אפסים, הקצה השמאלי מתקדם עד שנשארים \( k \). התשובה היא
        האורך הגדול ביותר שהחלון הגיע אליו : בדוגמה 6, המקומות 4 עד 9.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **קטע חוקי.** קטע של הווקטור אפשר להפוך לכולו אחדות בדיוק כשיש בו לכל היותר \( k \) אפסים.
    לכן השאלה היא : מהו הקטע הארוך ביותר עם לכל היותר \( k \) אפסים? בדוגמה :

    <!-- gen 0 -->

    <svg class="figure ok-fig" viewBox="0 0 390 92" style="max-width:24.375rem" role="img" aria-label="הווקטור 11100011110 : החלון הארוך ביותר עם לכל היותר 2 אפסים הוא באורך 6"><rect class="ok-win" x="140" y="17" width="212" height="44" rx="6"/><g class="ok-cell is-off"><title>place 0, value 1</title><rect x="10" y="22" width="30" height="34" rx="4"/><text x="25" y="45.0" text-anchor="middle">1</text></g><text class="tick" x="25" y="84" text-anchor="middle">0</text><g class="ok-cell is-off"><title>place 1, value 1</title><rect x="44" y="22" width="30" height="34" rx="4"/><text x="59" y="45.0" text-anchor="middle">1</text></g><text class="tick" x="59" y="84" text-anchor="middle">1</text><g class="ok-cell is-off"><title>place 2, value 1</title><rect x="78" y="22" width="30" height="34" rx="4"/><text x="93" y="45.0" text-anchor="middle">1</text></g><text class="tick" x="93" y="84" text-anchor="middle">2</text><g class="ok-cell is-off"><title>place 3, value 0</title><rect x="112" y="22" width="30" height="34" rx="4"/><text x="127" y="45.0" text-anchor="middle">0</text></g><text class="tick" x="127" y="84" text-anchor="middle">3</text><g class="ok-cell is-flip"><title>place 4, value 0</title><rect x="146" y="22" width="30" height="34" rx="4"/><text x="161" y="45.0" text-anchor="middle">0</text></g><text class="tick" x="161" y="84" text-anchor="middle">4</text><g class="ok-cell is-flip"><title>place 5, value 0</title><rect x="180" y="22" width="30" height="34" rx="4"/><text x="195" y="45.0" text-anchor="middle">0</text></g><text class="tick" x="195" y="84" text-anchor="middle">5</text><g class="ok-cell is-one"><title>place 6, value 1</title><rect x="214" y="22" width="30" height="34" rx="4"/><text x="229" y="45.0" text-anchor="middle">1</text></g><text class="tick" x="229" y="84" text-anchor="middle">6</text><g class="ok-cell is-one"><title>place 7, value 1</title><rect x="248" y="22" width="30" height="34" rx="4"/><text x="263" y="45.0" text-anchor="middle">1</text></g><text class="tick" x="263" y="84" text-anchor="middle">7</text><g class="ok-cell is-one"><title>place 8, value 1</title><rect x="282" y="22" width="30" height="34" rx="4"/><text x="297" y="45.0" text-anchor="middle">1</text></g><text class="tick" x="297" y="84" text-anchor="middle">8</text><g class="ok-cell is-one"><title>place 9, value 1</title><rect x="316" y="22" width="30" height="34" rx="4"/><text x="331" y="45.0" text-anchor="middle">1</text></g><text class="tick" x="331" y="84" text-anchor="middle">9</text><g class="ok-cell is-off"><title>place 10, value 0</title><rect x="350" y="22" width="30" height="34" rx="4"/><text x="365" y="45.0" text-anchor="middle">0</text></g><text class="tick" x="365" y="84" text-anchor="middle">10</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="ok-key-one"></i>כבר בערך הרצוי</span><span><i class="ok-key-flip"></i>אפס שהופך לאחד</span><span><i class="ok-key-win"></i>החלון הארוך ביותר</span></span>

    <!-- /gen -->

    **חלון נע.** במקום לבדוק כל קטע בנפרד, מחזיקים חלון אחד, \( [\text{left}, \text{right}] \), ומזיזים
    את הקצה הימני צעד אחרי צעד. מונה אחד סופר את האפסים שבחלון : כשביט 0 נכנס מימין המונה
    עולה, וכשביט 0 יוצא משמאל הוא יורד. ברגע שהמונה עובר את \( k \) החלון "ארוך מדי", ומקדמים
    את הקצה השמאלי עד שהוא חוזר להיות חוקי. בכל צעד האורך של החלון הוא מועמד לתשובה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הקצה הימני מתקדם :** הביט החדש נכנס לחלון. אם הוא 0, מונה האפסים גדל.
    2. **יותר מ-k אפסים :** מוציאים ביטים מהקצה השמאלי, אחד אחרי השני, עד שבחלון נשארים לכל
       היותר \( k \) אפסים. כל אפס שיוצא מוריד את המונה.
    3. **הטוב עד עכשיו :** האורך \( \text{right} - \text{left} + 1 \) נבדק מול הטוב עד עכשיו.
    4. **הסוף :** אחרי שהקצה הימני עבר את כל הווקטור, הטוב עד עכשיו הוא התשובה.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function longest_ones" linenums="1" hl_lines="6 7 11"
        // the longest run of ones after flipping at most k zeros: a sliding window over the
        // vector, zeros counts the zeros inside it
        function automatic int longest_ones(bit bits[], int k);
          int best = 0, left = 0, zeros = 0;
          foreach (bits[right]) begin
            if (!bits[right]) zeros++;                       // (1)!
            while (zeros > k) begin                          // (2)!
              if (!bits[left]) zeros--;
              left++;
            end
            if (right - left + 1 > best) best = right - left + 1;
          end
          return best;
        endfunction
        ```

        1. הביט החדש נכנס לחלון. רק אפס משנה את המונה.
        2. החלון ארוך מדי : הקצה השמאלי מתקדם עד שהמונה חוזר ל-\( k \). הוא לעולם לא חוזר אחורה.

    === "Python"
        ```python title="longest_ones" linenums="1" hl_lines="5 6 9"
        def longest_ones(bits: list[int], k: int) -> int:
            """The longest run of ones after flipping at most k zeros: a sliding window."""
            best = left = zeros = 0
            for right, b in enumerate(bits):
                zeros += b == 0                      # (1)!
                while zeros > k:                     # (2)!
                    zeros -= bits[left] == 0
                    left += 1
                best = max(best, right - left + 1)
            return best
        ```

        1. ‏`b == 0` הוא `True` או `False`, כלומר 1 או 0 בחיבור.
        2. החלון ארוך מדי : הקצה השמאלי מתקדם עד שהמונה חוזר ל-\( k \).

    #### למה זה נכון { .sol-proof }

    הצעדים על הדוגמה, \( k = 2 \) :

    <!-- gen 2 -->

    | הצעד | הביט שנכנס | אפסים בחלון | הקצה השמאלי | החלון | הטוב עד עכשיו |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏0 | ‏1 | ‏0 | ‏0 | ‏0..0 | **‏1** |
    | ‏1 | ‏1 | ‏0 | ‏0 | ‏0..1 | **‏2** |
    | ‏2 | ‏1 | ‏0 | ‏0 | ‏0..2 | **‏3** |
    | ‏3 | ‏0 | ‏1 | ‏0 | ‏0..3 | **‏4** |
    | ‏4 | ‏0 | ‏2 | ‏0 | ‏0..4 | **‏5** |
    | ‏5 | ‏0 | ‏2 | ‏4 (זז ‏4) | ‏4..5 | **‏5** |
    | ‏6 | ‏1 | ‏2 | ‏4 | ‏4..6 | **‏5** |
    | ‏7 | ‏1 | ‏2 | ‏4 | ‏4..7 | **‏5** |
    | ‏8 | ‏1 | ‏2 | ‏4 | ‏4..8 | **‏5** |
    | ‏9 | ‏1 | ‏2 | ‏4 | ‏4..9 | **‏6** |
    | ‏10 | ‏0 | ‏2 | ‏5 (זז ‏1) | ‏5..10 | **‏6** |

    <!-- /gen -->

    **שמורה :** אחרי הצעד של \( \text{right} \), החלון \( [\text{left}, \text{right}] \) חוקי (לכל היותר
    \( k \) אפסים), ו-\( \text{left} \) הוא **הקטן ביותר** שעבורו זה נכון. באינדוקציה : כל התחלה
    \( l \) קטנה מה-\( \text{left} \) של הצעד הקודם נתנה כבר יותר מ-\( k \) אפסים עד
    \( \text{right} - 1 \), ולכן גם עד \( \text{right} \). כלומר ההתחלה החוקית הקטנה ביותר לא קטנה
    מה-\( \text{left} \) הקודם, והלולאה מתקדמת ממנו ונעצרת בהתחלה החוקית הראשונה, שהיא הקטנה
    ביותר. לכן הקצה השמאלי לא צריך לחזור אחורה אף פעם.

    **ההשלמה :** כל קטע חוקי נגמר באיזשהו \( \text{right} \), ומתחיל ב-\( l \) שאינו קטן מההתחלה
    החוקית הקטנה ביותר של אותו \( \text{right} \). לכן האורך שלו אינו גדול מהאורך שהחלון רשם
    באותו צעד, והטוב עד עכשיו בסוף הוא האורך של הקטע החוקי הארוך ביותר. בדוגמה הוא נרשם
    בצעד 9 : החלון 4..9.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n) \). הקצה הימני זז \( n \) פעמים, והשמאלי לכל היותר \( n \) פעמים בסך הכול,
      כי הוא רק מתקדם.
    - **זיכרון :** ‏\( O(1) \), שלושה מספרים. הווקטור לא משתנה.

    **נסו בעצמכם.** הקצה הימני מתקדם תא אחד בכל צעד. התאים שבחלון מסומנים, האפסים שצריך להפוך
    בכתום, והחלון הטוב ביותר עד עכשיו מוקף :

    <div class="explorer" data-kind="onesk" data-mode="bits" data-bits="11100011110" data-k="2"></div>

---

### סעיף ב – כל ערך על ה-bus

??? tip "רמז 1"
    במקום "כמה אפסים יש בחלון", שאלו : כמה תאים בחלון **לא** שווים לערך הנפוץ ביותר בו? אלה
    התאים שצריך להחליף.

??? tip "רמז 2"
    שמרו מונה לכל ערך שבחלון. החלון חוקי כשהאורך שלו פחות המונה הגדול ביותר הוא לכל היותר
    \( k \).

<div class="selfcheck" data-answer="7" data-show="7 : המקומות 0 עד 6, ‏A B A A C A A, עם B ו-C שמוחלפים ב-A" data-hint="חפשו את החלון הארוך ביותר שיש בו לכל היותר שני תאים שאינם הערך הנפוץ בו." markdown>
על ה-bus עוברים הערכים <span dir="ltr">A B A A C A A B</span>, מחזור אחרי מחזור, ו-\( k = 2 \).
מה האורך של החלון הארוך ביותר שאפשר להפוך לערך אחד?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        אותו חלון נע, עם מונה לכל ערך שבחלון. החלון חוקי כשהאורך שלו פחות המונה של הערך הנפוץ
        ביותר בו הוא לכל היותר \( k \) : אלה בדיוק התאים שצריך להחליף. בדוגמה שבאיור, עם
        \( k = 2 \), התשובה היא 6 : המקומות 3 עד 8, שהופכים כולם ל-B.

    <!-- cost: זמן \( O(n \cdot |\Sigma|) \) | זיכרון \( O(|\Sigma|) \) -->

    #### הרעיון { .sol-idea }

    עם ביטים, "האפסים בחלון" הם האורך פחות מספר האחדות. עם כל ערך, התאים שצריך להחליף הם
    האורך פחות **המונה הגדול ביותר** : משאירים את הערך הנפוץ ביותר ומחליפים את כל השאר. לכן
    מחזיקים מונה לכל ערך שבחלון, ומצמצמים משמאל כל עוד האורך פחות המונה הגדול ביותר גדול
    מ-\( k \). הרצף <span dir="ltr">A A A B B C B A B A</span> עם \( k = 2 \) :

    <!-- gen 3 -->

    <svg class="figure ok-fig" viewBox="0 0 356 92" style="max-width:22.25rem" role="img" aria-label="הערכים A A A B B C B A B A על ה-bus : החלון הארוך ביותר של ערך אחד אחרי לכל היותר 2 החלפות הוא באורך 6"><rect class="ok-win" x="106" y="17" width="212" height="44" rx="6"/><g class="ok-cell is-off"><title>place 0, value A</title><rect x="10" y="22" width="30" height="34" rx="4"/><text x="25" y="45.0" text-anchor="middle">A</text></g><text class="tick" x="25" y="84" text-anchor="middle">0</text><g class="ok-cell is-off"><title>place 1, value A</title><rect x="44" y="22" width="30" height="34" rx="4"/><text x="59" y="45.0" text-anchor="middle">A</text></g><text class="tick" x="59" y="84" text-anchor="middle">1</text><g class="ok-cell is-off"><title>place 2, value A</title><rect x="78" y="22" width="30" height="34" rx="4"/><text x="93" y="45.0" text-anchor="middle">A</text></g><text class="tick" x="93" y="84" text-anchor="middle">2</text><g class="ok-cell is-one"><title>place 3, value B</title><rect x="112" y="22" width="30" height="34" rx="4"/><text x="127" y="45.0" text-anchor="middle">B</text></g><text class="tick" x="127" y="84" text-anchor="middle">3</text><g class="ok-cell is-one"><title>place 4, value B</title><rect x="146" y="22" width="30" height="34" rx="4"/><text x="161" y="45.0" text-anchor="middle">B</text></g><text class="tick" x="161" y="84" text-anchor="middle">4</text><g class="ok-cell is-flip"><title>place 5, value C</title><rect x="180" y="22" width="30" height="34" rx="4"/><text x="195" y="45.0" text-anchor="middle">C</text></g><text class="tick" x="195" y="84" text-anchor="middle">5</text><g class="ok-cell is-one"><title>place 6, value B</title><rect x="214" y="22" width="30" height="34" rx="4"/><text x="229" y="45.0" text-anchor="middle">B</text></g><text class="tick" x="229" y="84" text-anchor="middle">6</text><g class="ok-cell is-flip"><title>place 7, value A</title><rect x="248" y="22" width="30" height="34" rx="4"/><text x="263" y="45.0" text-anchor="middle">A</text></g><text class="tick" x="263" y="84" text-anchor="middle">7</text><g class="ok-cell is-one"><title>place 8, value B</title><rect x="282" y="22" width="30" height="34" rx="4"/><text x="297" y="45.0" text-anchor="middle">B</text></g><text class="tick" x="297" y="84" text-anchor="middle">8</text><g class="ok-cell is-off"><title>place 9, value A</title><rect x="316" y="22" width="30" height="34" rx="4"/><text x="331" y="45.0" text-anchor="middle">A</text></g><text class="tick" x="331" y="84" text-anchor="middle">9</text></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="ok-key-one"></i>כבר בערך הרצוי</span><span><i class="ok-key-flip"></i>ערך שמוחלף</span><span><i class="ok-key-win"></i>החלון הארוך ביותר</span></span>

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function longest_same" linenums="1" hl_lines="9 10 16"
        // the longest window that is one value after at most k replacements: s[i] is the value
        // on the bus in cycle i (a letter), count[] has a counter per value inside the window,
        // and most is the largest of them
        function automatic int longest_same(string s, int k);
          int count[byte], best = 0, left = 0, most = 0;
          for (int right = 0; right < s.len(); right++) begin
            count[s[right]]++;
            most = 0;
            foreach (count[v]) if (count[v] > most) most = count[v];   // (1)!
            while (right - left + 1 - most > k) begin                   // (2)!
              count[s[left]]--;
              left++;
              most = 0;
              foreach (count[v]) if (count[v] > most) most = count[v];
            end
            if (right - left + 1 > best) best = right - left + 1;
          end
          return best;
        endfunction
        ```

        1. המונה הגדול ביותר, על כל הערכים שבחלון. ‏`count` הוא מערך אסוציאטיבי שהמפתח שלו הוא הערך.
        2. התאים שצריך להחליף הם האורך פחות המונה הגדול ביותר. יותר מ-\( k \) : הקצה השמאלי מתקדם.

    === "Python"
        ```python title="longest_same" linenums="1" hl_lines="8 11"
        def longest_same(values, k: int) -> int:
            """The longest window that is one value after at most k replacements: a sliding
            window with a counter per value in it (values is a string or a list)."""
            count: dict = {}
            best = left = 0
            for right, v in enumerate(values):
                count[v] = count.get(v, 0) + 1
                while right - left + 1 - max(count.values()) > k:    # (1)!
                    count[values[left]] -= 1
                    left += 1
                best = max(best, right - left + 1)
            return best
        ```

        1. התאים שצריך להחליף הם האורך פחות המונה הגדול ביותר. יותר מ-\( k \) : הקצה השמאלי מתקדם.

    #### למה זה נכון { .sol-proof }

    אותה שמורה כמו בסעיף א, עם תנאי חוקיות אחר : חלון חוקי כשהאורך פחות המונה הגדול ביותר בו
    הוא לכל היותר \( k \). גם כאן הוצאת תא משמאל רק מקטינה את האורך, ולכן הקצה השמאלי הקטן
    ביותר שחוקי עבור \( \text{right} \) אינו קטן מזה של \( \text{right} - 1 \), והלולאה מוצאת אותו.
    עם שני ערכים, 0 ו-1, זה בדיוק סעיף א : המונה הגדול ביותר הוא של האחדות, וההפרש הוא
    האפסים.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n \cdot |\Sigma|) \), כש-\( |\Sigma| \) הוא מספר הערכים השונים : בכל צעד מחפשים
      את המונה הגדול ביותר. על bus עם כמה opcodes זה קבוע קטן. שאלת ההמשך מראה איך מגיעים
      ל-\( O(n) \) ממש.
    - **זיכרון :** ‏\( O(|\Sigma|) \), מונה לכל ערך.

    **נסו בעצמכם.** אותה תיבה, עם ערכים במקום ביטים. מתחת לרצף המונים של החלון והערך הנפוץ
    בו :

    <div class="explorer" data-kind="onesk" data-mode="values" data-values="AAABBCBABA" data-k="2"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להתחיל מחדש מכל נקודת התחלה"
    לכל התחלה להתקדם ימינה עד שנגמרים \( k \) האפסים זה נכון, אבל \( O(n^2) \). החלון הנע לא
    מתחיל מחדש : הקצה השמאלי ממשיך מהמקום שבו עצר, כי כל התחלה שכבר נפסלה נשארת פסולה.

??? trap "מלכודת : להפוך את הביטים באמת"
    אין צורך לשנות את הווקטור. סופרים אפסים בחלון, ולא "משתמשים בהיפוכים". ווקטור ששונה
    בפועל מקלקל את הבדיקה של החלונות הבאים, שצריכים את הערכים המקוריים.

??? trap "מלכודת : המונה הגדול ביותר מול 'הערך שבחרנו מראש'"
    בסעיף ב אין ערך מטרה : הערך הנפוץ ביותר **בחלון** הוא שנשאר, והוא יכול להתחלף מחלון
    לחלון. לקבוע מראש "מחפשים A" פותר שאלה אחרת, ומפספס את החלון של B בדוגמה.

??? followup "שאלות המשך"
    - **איפה החלון :** איך מחזירים גם את המקום של הרצף, ולא רק את האורך?

        ??? fu-answer "תשובה"
            כשהטוב עד עכשיו משתפר, שומרים גם את \( \text{left} \) של אותו צעד. התשובה היא
            \( [\text{left}, \text{left} + \text{best} - 1] \), בלי עבודה נוספת.

    - **סעיף ב ב-O(n) ממש :** אפשר להימנע מהחיפוש של המונה הגדול ביותר בכל צעד?

        ??? fu-answer "תשובה"
            כן, בטריק : מחזיקים את המונה הגדול ביותר שנראה **אי פעם**, ולא מצמצמים את החלון אלא
            מזיזים אותו (שמאל וימין יחד) כשהוא לא חוקי. החלון אף פעם לא מתקצר, ולכן האורך שלו
            בסוף הוא התשובה : הוא גדל רק כשמונה כלשהו עובר את השיא הקודם, ואז החלון חוקי באמת.
            ‏\( O(n) \) זמן, אבל ההוכחה עדינה יותר, וכדאי להסביר אותה בראיון.

    - **ללא טרייס שלם :** המוניטור רואה ביט אחד בכל מחזור. אפשר לענות "מה הטוב עד עכשיו" אחרי
      כל ביט?

        ??? fu-answer "תשובה"
            האלגוריתם כבר עובד כך : כל צעד משתמש רק בביט החדש ובביטים שבחלון. מספיק לשמור את
            החלון (או את המקומות של האפסים שבו, לכל היותר \( k + 1 \)), והתשובה מתעדכנת בכל מחזור
            בזמן אמורטיזציה \( O(1) \).
