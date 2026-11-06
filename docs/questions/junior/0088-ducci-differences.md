---
id: 88
title: הפרשים במעגל – מתי הכל מתאפס ומתי יש מחזור
level: junior
difficulty: medium
kind: math
tags: [logic-puzzles, sequences, number-theory, bitwise, proof, python, systemverilog]
source: "סדרת Ducci (המשחק של n מספרים), חידה קלאסית של אינווריאנטות"
added: 2026-11-06
---

## השאלה

ארבעה מספרים שלמים אי-שליליים יושבים על מעגל. בכל סיבוב מחליפים **כל** מספר בהפרש
המוחלט בינו לבין השכן שלו בכיוון השעון, כולם בבת אחת. למשל, מ-2, 6, 11 ו-4 (בכיוון
השעון) מקבלים 4, 5, 7 ו-2 : ההפרש של 2 ו-6, של 6 ו-11, של 11 ו-4, ושל 4 ו-2.

<!-- gen 0 -->

<svg class="figure du-fig" viewBox="0 0 300 236" style="max-width:18.8rem" role="img" aria-label="ארבעה מספרים על מעגל, בכיוון השעון מלמעלה : 2, 6, 11, 4. על כל צלע ההפרש בין שני המספרים שבקצותיה : 4, 5, 7, 2. אלה המספרים של הסיבוב הבא"><circle class="du-ring" cx="150" cy="116" r="84"/><line class="du-chord" x1="150" y1="32" x2="234" y2="116"/><rect class="du-diff-bg" x="177.0" y="62.0" width="30" height="24" rx="6"/><text class="du-diff" x="192.0" y="79.0" text-anchor="middle">4</text><line class="du-chord" x1="234" y1="116" x2="150" y2="200"/><rect class="du-diff-bg" x="177.0" y="146.0" width="30" height="24" rx="6"/><text class="du-diff" x="192.0" y="163.0" text-anchor="middle">5</text><line class="du-chord" x1="150" y1="200" x2="66" y2="116"/><rect class="du-diff-bg" x="93.0" y="146.0" width="30" height="24" rx="6"/><text class="du-diff" x="108.0" y="163.0" text-anchor="middle">7</text><line class="du-chord" x1="66" y1="116" x2="150" y2="32"/><rect class="du-diff-bg" x="93.0" y="62.0" width="30" height="24" rx="6"/><text class="du-diff" x="108.0" y="79.0" text-anchor="middle">2</text><circle class="du-node" cx="150" cy="32" r="20"/><text class="du-val" x="150" y="38" text-anchor="middle">2</text><circle class="du-node" cx="234" cy="116" r="20"/><text class="du-val" x="234" y="122" text-anchor="middle">6</text><circle class="du-node" cx="150" cy="200" r="20"/><text class="du-val" x="150" y="206" text-anchor="middle">11</text><circle class="du-node" cx="66" cy="116" r="20"/><text class="du-val" x="66" y="122" text-anchor="middle">4</text></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="du-key-node"></i>מספר על המעגל</span><span><i class="du-key-diff"></i>ההפרש בין שני שכנים : המספר שיחליף אותם בסיבוב הבא</span></span>

<!-- /gen -->

נסמן את המספרים \( x_1, \dots, x_n \). סיבוב מחליף את \( x_i \) ב-\( |x_i - x_{i+1}| \),
והשכן של \( x_n \) הוא \( x_1 \). מה קורה אחרי הרבה סיבובים, עם ארבעה מספרים ועם \( n \)
מספרים?

??? interviewer "מה המראיין בודק"
    - **מה לא משתנה ומה לא עולה :** האם המועמד מחפש כמות שלא גדלה (המקסימום), ומבין
      שהיא לבדה לא מספיקה, כי היא יכולה לעמוד במקום.
    - **מודולו 2 :** ההפרש המוחלט מודולו 2 הוא XOR. האם הוא רואה שזוגיות היא מערכת
      לינארית, והופך את החידה לחשבון על ביטים.
    - **אינדוקציה עם חלוקה :** כשהכל זוגי, אפשר לחלק ב-2 ולהמשיך באותו משחק. האם הוא
      יודע לסגור את ההוכחה באינדוקציה על המקסימום.
    - **כש-n משתנה :** האם הוא בודק את המקרה של שלושה מספרים, ומוצא דוגמה נגדית במקום
      להכליל מ-4.
    - **קוד :** סיבוב בלולאה אחת, וזיהוי מחזור עם מילון של המצבים שכבר נראו.

---

### סעיף א – ארבעה מספרים

1. הריצו את המשחק מ-2, 6, 11 ו-4. אחרי כמה סיבובים כל המספרים הם 0?
2. הוכיחו שמכל ארבעה מספרים שלמים אי-שליליים מגיעים תמיד לארבעה אפסים.
3. כתבו פונקציה לסיבוב אחד, ופונקציה שמחזירה כמה סיבובים עד שהכל 0.

??? tip "רמז 1"
    האם המספר הגדול ביותר יכול לגדול? האם זה מספיק כדי להוכיח שהמשחק נגמר?

??? tip "רמז 2"
    הסתכלו רק על הזוגיות. מה הזוגיות של \( |a - b| \) לפי הזוגיות של \( a \) ושל \( b \)?
    ומה קורה לזוגיות של ארבעה מספרים אחרי ארבעה סיבובים?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מ-2, 6, 11 ו-4 מגיעים לאפסים אחרי **6 סיבובים**. מכל התחלה : המקסימום אף פעם לא
        עולה, ואחרי **4 סיבובים כל המספרים זוגיים** (מודולו 2 סיבוב הוא XOR, ואחרי ארבעה
        סיבובים \( x_i \oplus x_{i+4} = 0 \)). ממספרים זוגיים המשחק הוא אותו משחק על
        החצאים, ולכן באינדוקציה על המקסימום מגיעים לאפסים.

    <!-- cost: זמן \( O(n) \) לסיבוב | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **המקסימום לא עולה.** אם \( 0 \le a, b \le M \) אז \( |a - b| \le M \). אבל הוא יכול
    לעמוד במקום : מ-2, 0, 2 ו-0 מקבלים 2, 2, 2 ו-2. לכן "יורד" לבד לא מוכיח שהמשחק נגמר.

    **זוגיות.** \( |a - b| \) זוגי בדיוק כש-\( a \) ו-\( b \) באותה זוגיות, כלומר מודולו 2
    ההפרש הוא \( a \oplus b \). סיבוב אחד נותן מודולו 2 את \( x_i \oplus x_{i+1} \). סיבוב
    שני נותן \( (x_i \oplus x_{i+1}) \oplus (x_{i+1} \oplus x_{i+2}) = x_i \oplus x_{i+2} \),
    כי \( x_{i+1} \) מופיע פעמיים ומתבטל. אותו חשבון שוב, על הצעדים של 2 : אחרי ארבעה
    סיבובים \( x_i \oplus x_{i+4} \). עם ארבעה מספרים על מעגל \( x_{i+4} = x_i \), ולכן
    הכל זוגי.

    **חלוקה ב-2.** אם כל המספרים זוגיים, \( |2a - 2b| = 2|a - b| \) : המשחק ממשיך בדיוק כמו
    המשחק על החצאים, כפול 2.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **לא עולה :** בכל סיבוב המקסימום \( M \) נשאר או יורד.
    2. **ארבעה סיבובים :** אחריהם כל המספרים זוגיים, והמקסימום עדיין לכל היותר \( M \).
    3. **חלוקה :** מכאן המשחק הוא פעמיים המשחק על החצאים, שהמקסימום שלו לכל היותר
       \( M/2 \).
    4. **אינדוקציה :** מקסימום 0 הוא ארבעה אפסים. כל ארבעה סיבובים חוצים את המקסימום,
       ולכן אחרי \( 4(\lfloor \log_2 M \rfloor + 1) \) סיבובים לכל היותר הכל 0.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="ducci_step" linenums="1" hl_lines="5 13"
        def ducci_step(v):
            """One round: every number becomes its distance from the next one around the
            circle (the last one's neighbour is the first)."""
            n = len(v)
            return [abs(v[i] - v[(i + 1) % n]) for i in range(n)]   # (1)!


        def steps_to_zero(v):
            """How many rounds until every number is 0. It always stops when there are 4
            numbers (part b: whenever n is a power of 2)."""
            steps = 0
            while any(v):
                v = ducci_step(v)                                   # (2)!
                steps += 1
            return steps
        ```

        1. כל המספרים מתעדכנים בבת אחת : הרשימה החדשה נבנית מהישנה, ולכן אין בעיה של
           סדר עדכון.
        2. אחרי ארבעה סיבובים הכל זוגי, ואחרי \( 4(\lfloor \log_2 M \rfloor + 1) \) הכל 0,
           ולכן הלולאה נגמרת.

    === "SystemVerilog"
        ```systemverilog title="function automatic void ducci_step" linenums="1" hl_lines="7 8"
        // One round on the circle: v[i] becomes |v[i] - v[i + 1]|, and the last one's
        // neighbour is the first. Updated in place: v[i + 1] is still the old value when
        // v[i] is computed, and the old v[0] is kept for the last one.
        function automatic void ducci_step(ref int v[$]);
          int n = v.size(), first = v[0], next;
          for (int i = 0; i < n; i++) begin
            next = (i == n - 1) ? first : v[i + 1];             // (1)!
            v[i] = (v[i] > next) ? v[i] - next : next - v[i];
          end
        endfunction

        // How many rounds until every number is 0.
        function automatic int steps_to_zero(int start[$]);
          int v[$];
          int steps = 0;
          bit nonzero = 1;
          v = start;
          while (nonzero) begin
            nonzero = 0;
            foreach (v[i]) if (v[i] != 0) nonzero = 1;
            if (nonzero) begin ducci_step(v); steps++; end
          end
          return steps;
        endfunction
        ```

        1. העדכון במקום : כש-\( i \) עולה, \( v[i+1] \) עוד לא עודכן. רק \( v[0] \)
           כבר עודכן כשמגיעים לאחרון, ולכן הערך הישן שלו נשמר ב-`first`.

    #### למה זה נכון { .sol-proof }

    **הריצה של 2, 6, 11 ו-4.** העמודה האחרונה היא כמה מארבעת המספרים אי-זוגיים. אחרי
    ארבעה סיבובים היא 0, כמו שההוכחה אומרת, ומשם המשחק הוא פעמיים המשחק של 1, 0, 1 ו-0 :

    <!-- gen 2 -->

    | סיבוב | מספר 1 | מספר 2 | מספר 3 | מספר 4 | הכי גדול | כמה אי-זוגיים |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | 0 | 2 | 6 | 11 | 4 | 11 | 1 |
    | 1 | 4 | 5 | 7 | 2 | 7 | 2 |
    | 2 | 1 | 2 | 5 | 2 | 5 | 2 |
    | 3 | 1 | 3 | 3 | 1 | 3 | 4 |
    | 4 | 2 | 0 | 2 | 0 | 2 | 0 |
    | 5 | 2 | 2 | 2 | 2 | 2 | 0 |
    | 6 | 0 | 0 | 0 | 0 | 0 | 0 |

    <!-- /gen -->

    **ההוכחה במלואה.** נסמן \( M \) את המקסימום בהתחלה. לפי הרעיון, אחרי 4 סיבובים כל
    המספרים זוגיים וקטנים או שווים ל-\( M \). נכתוב אותם \( 2y_1, \dots, 2y_4 \). מכיוון
    ש-\( |2a - 2b| = 2|a - b| \), כל סיבוב מכאן הוא פעמיים סיבוב על \( y \), שהמקסימום שלו
    לכל היותר \( \lfloor M/2 \rfloor \). באינדוקציה על \( M \), המשחק על \( y \) מגיע
    לאפסים, ולכן גם המשחק המקורי. כל ארבעה סיבובים חוצים את המקסימום, ולכן אחרי
    \( 4(\lfloor \log_2 M \rfloor + 1) \) סיבובים לכל היותר הכל 0. ל-2, 6, 11 ו-4,
    \( M = 11 \) והחסם הוא 16, והמשחק נגמר אחרי 6.

    **נסו בעצמכם.** המעגל מראה את המספרים, ועל כל צלע את ההפרש שיחליף אותם בסיבוב הבא.
    אפשר לבחור כמה מספרים, להקליד או להגריל, ולנסות את ההתחלות המוכנות. הגרף מתחת מראה את
    המקסימום בכל סיבוב : הוא אף פעם לא עולה.

    <div class="explorer" data-kind="ducci" data-v="2,6,11,4"></div>

    #### סיבוכיות { .sol-cost }

    סיבוב הוא \( O(n) \). עם \( n = 4 \) מספרים עד \( M \), יש לכל היותר
    \( 4(\lfloor \log_2 M \rfloor + 1) \) סיבובים, ולכן \( O(\log M) \) זמן בסך הכול.
    הזיכרון הוא \( O(n) \) לרשימה החדשה.

---

### סעיף ב – n שהוא חזקה של 2

עכשיו יש \( n \) מספרים על המעגל.

1. הוכיחו שכש-\( n \) הוא חזקה של 2 (1, 2, 4, 8, 16, ...) מגיעים תמיד לאפסים.
2. כתבו פונקציה שבודקת, בלי לנסות התחלות, אם כל התחלה של \( n \) מספרים מגיעה לאפסים.
   השתמשו בזוגיות : שמרו את הזוגיות של \( n \) המספרים כביטים של מספר שלם.

??? tip "רמז 1"
    בסעיף א, אחרי סיבוב אחד הזוגיות של \( x_i \) היא \( x_i \oplus x_{i+1} \), ואחרי שניים
    \( x_i \oplus x_{i+2} \). מה היא אחרי \( t \) סיבובים, באופן כללי?

??? tip "רמז 2"
    אחרי \( t \) סיבובים, \( x_{i+j} \) נכנס לזוגיות של \( x_i \) בדיוק כשהמקדם הבינומי
    \( \binom{t}{j} \) אי-זוגי, כמו במשולש פסקל מודולו 2. מה קורה בשורה \( t = 2^k \)?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        אחרי \( t \) סיבובים הזוגיות של \( x_i \) היא ה-XOR של \( x_{i+j} \) על כל \( j \)
        שבו \( \binom{t}{j} \) אי-זוגי. כש-\( t = n = 2^k \), המקדמים \( \binom{n}{j} \) זוגיים
        לכל \( 0 < j < n \), ונשאר \( x_i \oplus x_{i+n} = 0 \) : אחרי \( n \) סיבובים הכל
        זוגי. משם, כמו בסעיף א, חלוקה ב-2 ואינדוקציה על המקסימום : לכל היותר
        \( n(\lfloor \log_2 M \rfloor + 1) \) סיבובים. בקוד, מספיק לבדוק ש-1 אחד בין
        אפסים נעלם מודולו 2 אחרי \( n \) סיבובים.

    <!-- cost: זמן \( O(n) \) פעולות על מילה | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **זוגיות היא XOR, ו-XOR הוא חיבור.** מודולו 2, סיבוב מחליף את \( x_i \) ב-\( x_i \oplus x_{i+1} \).
    זו פעולה **לינארית** : הזוגיות אחרי סיבוב של סכום (ב-XOR) של שתי התחלות היא הסכום של
    הזוגיות שלהן. לכן מספיק להבין מה קורה ל-1 אחד בין אפסים, וכל התחלה היא XOR של כאלה.

    **משולש פסקל מודולו 2.** כמו בסעיף א, באינדוקציה על \( t \) : אחרי \( t \) סיבובים
    הזוגיות של \( x_i \) היא \( \bigoplus_j \binom{t}{j} x_{i+j} \), כי הצעד מחבר כל מקדם עם
    השכן שלו, בדיוק כמו הכלל של פסקל \( \binom{t+1}{j} = \binom{t}{j} + \binom{t}{j-1} \).
    בשורה \( t = 2^k \) כל המקדמים חוץ מהקצוות זוגיים, ולכן אחרי \( n = 2^k \) סיבובים
    נשאר \( x_i \oplus x_{i+n} \), ו-\( x_{i+n} = x_i \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מודולו 2 :** אחרי \( t \) סיבובים, \( x_i \mapsto \bigoplus_j \binom{t}{j} x_{i+j} \).
    2. **חזקה של 2 :** \( \binom{2^k}{j} \) זוגי לכל \( 0 < j < 2^k \), ולכן אחרי \( n \)
       סיבובים הכל זוגי.
    3. **חלוקה :** כמו בסעיף א, המשחק ממשיך כפעמיים המשחק על החצאים, והמקסימום נחצה.
    4. **הקוד :** הזוגיות כביטים של מספר שלם. סיבוב הוא XOR עם הסיבוב (rotate) של המילה
       בביט אחד. 1 אחד שנעלם אחרי \( n \) סיבובים מוכיח את זה לכל ההתחלות, בגלל
       הלינאריות.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="always_zero" linenums="1" hl_lines="4 13"
        def parity_step(b, n):
            """One round mod 2 on the parities of n numbers, kept as the bits of b (bit i is
            x_i mod 2): bit i becomes bit i XOR bit i + 1, around the circle."""
            rotated = (b >> 1) | ((b & 1) << (n - 1))           # (1)!
            return b ^ rotated


        def always_zero(n):
            """True if every start of n numbers reaches all zeros: n rounds must make a single
            odd number even (and by linearity every start)."""
            b = 1
            for _ in range(n):
                b = parity_step(b, n)                           # (2)!
            return b == 0
        ```

        1. הביט \( i \) של `rotated` הוא הביט \( i + 1 \) של `b`, והביט האחרון מקבל את הביט
           0 : השכן של \( x_n \) הוא \( x_1 \).
        2. אחרי \( n \) סיבובים הזוגיות של 1 אחד היא שורה \( n \) של משולש פסקל מודולו 2,
           מגולגלת על המעגל. היא 0 בדיוק כש-\( n \) חזקה של 2.

    === "SystemVerilog"
        ```systemverilog title="function automatic bit always_zero" linenums="1" hl_lines="5 13"
        // One round mod 2 on the parities of n numbers (n <= 64), kept as the bits of b:
        // bit i becomes bit i XOR bit i + 1, around the circle.
        function automatic longint unsigned parity_step(longint unsigned b, int n);
          longint unsigned rotated;
          rotated = (b >> 1) | ((b & 64'd1) << (n - 1));          // (1)!
          return b ^ rotated;
        endfunction

        // True if every start of n numbers reaches all zeros.
        function automatic bit always_zero(int n);
          longint unsigned b = 64'd1;
          for (int t = 0; t < n; t++)
            b = parity_step(b, n);
          return b == 0;
        endfunction
        ```

        1. אותו סיבוב (rotate) של \( n \) ביטים כמו ב-Python : הביט 0 עובר למקום
           \( n - 1 \). בחומרה זה רק חיווט ושער XOR לכל ביט.

    #### למה זה נכון { .sol-proof }

    **1 אחד בין אפסים.** כל שורה היא הזוגיות אחרי עוד סיבוב, ובמשבצת כהה מספר אי-זוגי.
    מימין, על 8 מספרים, השורות הן משולש פסקל מודולו 2, ובשורה 8 הכל זוגי. משמאל, על 6
    מספרים, המשולש מתגלגל סביב המעגל ואף שורה לא מתרוקנת :

    <!-- gen 3 -->

    <svg class="figure du-bits" viewBox="0 0 400 222" style="max-width:25.0rem" role="img" aria-label="הזוגיות של 1 בודד בין אפסים, סיבוב אחרי סיבוב. מימין 8 מספרים : אחרי 8 סיבובים הכל זוגי. משמאל 6 מספרים : אף פעם לא הכל זוגי"><text class="du-panel" x="302.0" y="30" text-anchor="middle">n = 8</text><text class="du-tick" x="222" y="52.2" text-anchor="end">0</text><rect class="du-zero" x="231" y="41" width="16" height="16" rx="2"/><rect class="du-zero" x="249" y="41" width="16" height="16" rx="2"/><rect class="du-zero" x="267" y="41" width="16" height="16" rx="2"/><rect class="du-zero" x="285" y="41" width="16" height="16" rx="2"/><rect class="du-zero" x="303" y="41" width="16" height="16" rx="2"/><rect class="du-zero" x="321" y="41" width="16" height="16" rx="2"/><rect class="du-zero" x="339" y="41" width="16" height="16" rx="2"/><rect class="du-one" x="357" y="41" width="16" height="16" rx="2"/><text class="du-tick" x="222" y="70.2" text-anchor="end">1</text><rect class="du-zero" x="231" y="59" width="16" height="16" rx="2"/><rect class="du-zero" x="249" y="59" width="16" height="16" rx="2"/><rect class="du-zero" x="267" y="59" width="16" height="16" rx="2"/><rect class="du-zero" x="285" y="59" width="16" height="16" rx="2"/><rect class="du-zero" x="303" y="59" width="16" height="16" rx="2"/><rect class="du-zero" x="321" y="59" width="16" height="16" rx="2"/><rect class="du-one" x="339" y="59" width="16" height="16" rx="2"/><rect class="du-one" x="357" y="59" width="16" height="16" rx="2"/><text class="du-tick" x="222" y="88.2" text-anchor="end">2</text><rect class="du-zero" x="231" y="77" width="16" height="16" rx="2"/><rect class="du-zero" x="249" y="77" width="16" height="16" rx="2"/><rect class="du-zero" x="267" y="77" width="16" height="16" rx="2"/><rect class="du-zero" x="285" y="77" width="16" height="16" rx="2"/><rect class="du-zero" x="303" y="77" width="16" height="16" rx="2"/><rect class="du-one" x="321" y="77" width="16" height="16" rx="2"/><rect class="du-zero" x="339" y="77" width="16" height="16" rx="2"/><rect class="du-one" x="357" y="77" width="16" height="16" rx="2"/><text class="du-tick" x="222" y="106.2" text-anchor="end">3</text><rect class="du-zero" x="231" y="95" width="16" height="16" rx="2"/><rect class="du-zero" x="249" y="95" width="16" height="16" rx="2"/><rect class="du-zero" x="267" y="95" width="16" height="16" rx="2"/><rect class="du-zero" x="285" y="95" width="16" height="16" rx="2"/><rect class="du-one" x="303" y="95" width="16" height="16" rx="2"/><rect class="du-one" x="321" y="95" width="16" height="16" rx="2"/><rect class="du-one" x="339" y="95" width="16" height="16" rx="2"/><rect class="du-one" x="357" y="95" width="16" height="16" rx="2"/><text class="du-tick" x="222" y="124.2" text-anchor="end">4</text><rect class="du-zero" x="231" y="113" width="16" height="16" rx="2"/><rect class="du-zero" x="249" y="113" width="16" height="16" rx="2"/><rect class="du-zero" x="267" y="113" width="16" height="16" rx="2"/><rect class="du-one" x="285" y="113" width="16" height="16" rx="2"/><rect class="du-zero" x="303" y="113" width="16" height="16" rx="2"/><rect class="du-zero" x="321" y="113" width="16" height="16" rx="2"/><rect class="du-zero" x="339" y="113" width="16" height="16" rx="2"/><rect class="du-one" x="357" y="113" width="16" height="16" rx="2"/><text class="du-tick" x="222" y="142.2" text-anchor="end">5</text><rect class="du-zero" x="231" y="131" width="16" height="16" rx="2"/><rect class="du-zero" x="249" y="131" width="16" height="16" rx="2"/><rect class="du-one" x="267" y="131" width="16" height="16" rx="2"/><rect class="du-one" x="285" y="131" width="16" height="16" rx="2"/><rect class="du-zero" x="303" y="131" width="16" height="16" rx="2"/><rect class="du-zero" x="321" y="131" width="16" height="16" rx="2"/><rect class="du-one" x="339" y="131" width="16" height="16" rx="2"/><rect class="du-one" x="357" y="131" width="16" height="16" rx="2"/><text class="du-tick" x="222" y="160.2" text-anchor="end">6</text><rect class="du-zero" x="231" y="149" width="16" height="16" rx="2"/><rect class="du-one" x="249" y="149" width="16" height="16" rx="2"/><rect class="du-zero" x="267" y="149" width="16" height="16" rx="2"/><rect class="du-one" x="285" y="149" width="16" height="16" rx="2"/><rect class="du-zero" x="303" y="149" width="16" height="16" rx="2"/><rect class="du-one" x="321" y="149" width="16" height="16" rx="2"/><rect class="du-zero" x="339" y="149" width="16" height="16" rx="2"/><rect class="du-one" x="357" y="149" width="16" height="16" rx="2"/><text class="du-tick" x="222" y="178.2" text-anchor="end">7</text><rect class="du-one" x="231" y="167" width="16" height="16" rx="2"/><rect class="du-one" x="249" y="167" width="16" height="16" rx="2"/><rect class="du-one" x="267" y="167" width="16" height="16" rx="2"/><rect class="du-one" x="285" y="167" width="16" height="16" rx="2"/><rect class="du-one" x="303" y="167" width="16" height="16" rx="2"/><rect class="du-one" x="321" y="167" width="16" height="16" rx="2"/><rect class="du-one" x="339" y="167" width="16" height="16" rx="2"/><rect class="du-one" x="357" y="167" width="16" height="16" rx="2"/><text class="du-tick" x="222" y="196.2" text-anchor="end">8</text><rect class="du-zero" x="231" y="185" width="16" height="16" rx="2"/><rect class="du-zero" x="249" y="185" width="16" height="16" rx="2"/><rect class="du-zero" x="267" y="185" width="16" height="16" rx="2"/><rect class="du-zero" x="285" y="185" width="16" height="16" rx="2"/><rect class="du-zero" x="303" y="185" width="16" height="16" rx="2"/><rect class="du-zero" x="321" y="185" width="16" height="16" rx="2"/><rect class="du-zero" x="339" y="185" width="16" height="16" rx="2"/><rect class="du-zero" x="357" y="185" width="16" height="16" rx="2"/><rect class="du-dead" x="229" y="184" width="146" height="18" rx="3"/><text class="du-panel" x="104.0" y="30" text-anchor="middle">n = 6</text><text class="du-tick" x="42" y="52.2" text-anchor="end">0</text><rect class="du-zero" x="51" y="41" width="16" height="16" rx="2"/><rect class="du-zero" x="69" y="41" width="16" height="16" rx="2"/><rect class="du-zero" x="87" y="41" width="16" height="16" rx="2"/><rect class="du-zero" x="105" y="41" width="16" height="16" rx="2"/><rect class="du-zero" x="123" y="41" width="16" height="16" rx="2"/><rect class="du-one" x="141" y="41" width="16" height="16" rx="2"/><text class="du-tick" x="42" y="70.2" text-anchor="end">1</text><rect class="du-zero" x="51" y="59" width="16" height="16" rx="2"/><rect class="du-zero" x="69" y="59" width="16" height="16" rx="2"/><rect class="du-zero" x="87" y="59" width="16" height="16" rx="2"/><rect class="du-zero" x="105" y="59" width="16" height="16" rx="2"/><rect class="du-one" x="123" y="59" width="16" height="16" rx="2"/><rect class="du-one" x="141" y="59" width="16" height="16" rx="2"/><text class="du-tick" x="42" y="88.2" text-anchor="end">2</text><rect class="du-zero" x="51" y="77" width="16" height="16" rx="2"/><rect class="du-zero" x="69" y="77" width="16" height="16" rx="2"/><rect class="du-zero" x="87" y="77" width="16" height="16" rx="2"/><rect class="du-one" x="105" y="77" width="16" height="16" rx="2"/><rect class="du-zero" x="123" y="77" width="16" height="16" rx="2"/><rect class="du-one" x="141" y="77" width="16" height="16" rx="2"/><text class="du-tick" x="42" y="106.2" text-anchor="end">3</text><rect class="du-zero" x="51" y="95" width="16" height="16" rx="2"/><rect class="du-zero" x="69" y="95" width="16" height="16" rx="2"/><rect class="du-one" x="87" y="95" width="16" height="16" rx="2"/><rect class="du-one" x="105" y="95" width="16" height="16" rx="2"/><rect class="du-one" x="123" y="95" width="16" height="16" rx="2"/><rect class="du-one" x="141" y="95" width="16" height="16" rx="2"/><text class="du-tick" x="42" y="124.2" text-anchor="end">4</text><rect class="du-zero" x="51" y="113" width="16" height="16" rx="2"/><rect class="du-one" x="69" y="113" width="16" height="16" rx="2"/><rect class="du-zero" x="87" y="113" width="16" height="16" rx="2"/><rect class="du-zero" x="105" y="113" width="16" height="16" rx="2"/><rect class="du-zero" x="123" y="113" width="16" height="16" rx="2"/><rect class="du-one" x="141" y="113" width="16" height="16" rx="2"/><text class="du-tick" x="42" y="142.2" text-anchor="end">5</text><rect class="du-one" x="51" y="131" width="16" height="16" rx="2"/><rect class="du-one" x="69" y="131" width="16" height="16" rx="2"/><rect class="du-zero" x="87" y="131" width="16" height="16" rx="2"/><rect class="du-zero" x="105" y="131" width="16" height="16" rx="2"/><rect class="du-one" x="123" y="131" width="16" height="16" rx="2"/><rect class="du-one" x="141" y="131" width="16" height="16" rx="2"/><text class="du-tick" x="42" y="160.2" text-anchor="end">6</text><rect class="du-zero" x="51" y="149" width="16" height="16" rx="2"/><rect class="du-one" x="69" y="149" width="16" height="16" rx="2"/><rect class="du-zero" x="87" y="149" width="16" height="16" rx="2"/><rect class="du-one" x="105" y="149" width="16" height="16" rx="2"/><rect class="du-zero" x="123" y="149" width="16" height="16" rx="2"/><rect class="du-zero" x="141" y="149" width="16" height="16" rx="2"/><text class="du-tick" x="42" y="178.2" text-anchor="end">7</text><rect class="du-one" x="51" y="167" width="16" height="16" rx="2"/><rect class="du-one" x="69" y="167" width="16" height="16" rx="2"/><rect class="du-one" x="87" y="167" width="16" height="16" rx="2"/><rect class="du-one" x="105" y="167" width="16" height="16" rx="2"/><rect class="du-zero" x="123" y="167" width="16" height="16" rx="2"/><rect class="du-zero" x="141" y="167" width="16" height="16" rx="2"/><text class="du-tick" x="42" y="196.2" text-anchor="end">8</text><rect class="du-zero" x="51" y="185" width="16" height="16" rx="2"/><rect class="du-zero" x="69" y="185" width="16" height="16" rx="2"/><rect class="du-zero" x="87" y="185" width="16" height="16" rx="2"/><rect class="du-one" x="105" y="185" width="16" height="16" rx="2"/><rect class="du-zero" x="123" y="185" width="16" height="16" rx="2"/><rect class="du-one" x="141" y="185" width="16" height="16" rx="2"/></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="du-key-one"></i>מספר אי-זוגי</span><span><i class="du-key-zero"></i>מספר זוגי</span><span><i class="du-key-dead"></i>שורה שכולה זוגית</span><span>בכל שורה הזוגיות אחרי עוד סיבוב, והמספר ליד השורה הוא מספר הסיבובים. מימין 8 מספרים, משמאל 6</span></span>

    <!-- /gen -->

    **למה \( \binom{2^k}{j} \) זוגי.** \( \binom{n}{j} = \frac{n}{j} \binom{n-1}{j-1} \). עם
    \( n = 2^k \) ו-\( 0 < j < n \), החזקה של 2 ב-\( j \) קטנה מ-\( 2^k \), ולכן
    \( \frac{2^k}{j} \binom{n-1}{j-1} \), שהוא מספר שלם, עדיין מתחלק ב-2. דרך אחרת :
    \( (1 + x)^2 = 1 + x^2 \) מודולו 2, ולכן \( (1 + x)^{2^k} = 1 + x^{2^k} \).

    **מספיק 1 אחד.** הזוגיות אחרי \( t \) סיבובים של XOR של התחלות היא ה-XOR של הזוגיות
    שלהן, ו-1 במקום אחר הוא אותו ציור מסובב. לכן אם 1 אחד נעלם אחרי \( n \) סיבובים, כל
    התחלה הופכת לזוגית אחרי \( n \) סיבובים.

    **הספירה.** כמו בסעיף א, כל \( n \) סיבובים חוצים את המקסימום : לכל היותר
    \( n(\lfloor \log_2 M \rfloor + 1) \) סיבובים. הטסט של השאלה בודק את החסם לכל התחלה
    עם ערכים קטנים, ל-\( n = 4 \) ול-\( n = 8 \).

    #### סיבוכיות { .sol-cost }

    הפונקציה `always_zero` עושה \( n \) סיבובים, כל אחד כמה פעולות על מילה : \( O(n) \) זמן ו-\( O(1) \)
    זיכרון, עד 64 מספרים במילה אחת. בדיקה של כל ההתחלות הייתה אינסופית.

---

### סעיף ג – כל n אחר

עכשיו \( n \) **אינו** חזקה של 2, למשל 3, 5, 6 או 7.

1. מצאו התחלה של שלושה מספרים שלא מגיעה לאפסים לעולם, והוכיחו שלכל \( n \) כזה יש
   התחלה כזו.
2. הסבירו למה כל התחלה נכנסת בסוף **למחזור**.
3. כתבו פונקציה שמחזירה אחרי כמה סיבובים נכנסים למחזור, ומה האורך שלו.

??? tip "רמז 1"
    נסו את 1, 2 ו-3. ומה קורה ל-0, 0 ו-1? מספרים שהם רק 0 ו-1 נשארים 0 ו-1, והסיבוב עליהם
    הוא XOR.

??? tip "רמז 2"
    עם 0 ו-1, מאיזה מצב מגיעים לאפסים? רק ממצב שכולו 1. ומאיזה מצב מגיעים ל"כולו 1" על
    מעגל באורך אי-זוגי?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        מ-0, 0 ו-1 מקבלים 0, 1 ו-1, ואז 1, 0 ו-1, ואז 1, 1 ו-0, ושוב 0, 1 ו-1 : מחזור באורך 3. באופן
        כללי, עם \( n = 2^k m \) ו-\( m \) אי-זוגי, \( m \ge 3 \), ההתחלה עם 1 בכל מקום
        \( m \)-י ואפסים בשאר לא מגיעה לאפסים לעולם. וכל התחלה נכנסת למחזור : המקסימום לא
        עולה, ולכן יש מספר סופי של מצבים. בקוד, מילון של המצבים שכבר נראו נותן את הצעד שבו
        המחזור מתחיל ואת האורך שלו.

    <!-- cost: זמן \( O(n(T + L)) \) | זיכרון \( O(n(T + L)) \) -->

    #### הרעיון { .sol-idea }

    **רק 0 ו-1.** אם כל המספרים 0 או 1, ההפרשים שוב 0 או 1, וההפרש הוא בדיוק XOR. לאפסים
    מגיעים רק ממצב שבו כל השכנים שווים, כלומר מאפסים או ממצב שכולו 1. ל"כולו 1" מגיעים רק
    ממצב שבו כל שני שכנים **שונים**, כלומר 0 ו-1 לסירוגין, וזה בלתי אפשרי על מעגל באורך
    אי-זוגי. לכן על מעגל אי-זוגי, כל התחלה של 0 ו-1 שאינה אפסים ואינה כולה 1 לא מגיעה
    לאפסים לעולם.

    **כל n שאינו חזקה של 2.** נכתוב \( n = 2^k m \) עם \( m \) אי-זוגי ו-\( m \ge 3 \).
    התחלה שחוזרת על עצמה כל \( m \) מקומות נשארת כזו אחרי סיבוב, והמשחק עליה הוא בדיוק
    המשחק על \( m \) מספרים, \( 2^k \) פעמים. ההתחלה עם 1 בכל מקום \( m \)-י היא 1 אחד בין
    אפסים במשחק של \( m \), ולכן גם היא לא מגיעה לאפסים.

    **מחזור.** המקסימום לא עולה, ולכן כל המצבים הם \( n \) מספרים בין 0 ל-\( M \) : לכל
    היותר \( (M + 1)^n \) מצבים. אחרי מספיק סיבובים מצב חוזר, ומשם הכל חוזר.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **דוגמה :** 0, 0 ו-1 נכנסים למחזור של שלושה מצבים : 0, 1 ו-1, ואז 1, 0 ו-1, ואז 1, 1 ו-0.
    2. **מעגל אי-זוגי :** לאפסים מגיעים רק דרך "כולו 1", ול"כולו 1" רק ממצב לסירוגין, שאין
       על מעגל אי-זוגי.
    3. **כל n :** \( n = 2^k m \), והתחלה עם מחזוריות \( m \) משחקת כמו המשחק על \( m \).
    4. **מחזור :** מספר סופי של מצבים. הקוד שומר מילון ממצב לצעד שבו נראה לראשונה.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="ducci_orbit" linenums="1" hl_lines="5 9"
        def ducci_orbit(v):
            """(tail, period): the rounds before the numbers enter a cycle, and the cycle's
            length. All zeros is a cycle of length 1."""
            n = len(v)
            seen = {}                                               # (1)!
            v, t = tuple(v), 0
            while v not in seen:
                seen[v] = t
                v = tuple(abs(v[i] - v[(i + 1) % n]) for i in range(n))
                t += 1
            return seen[v], t - seen[v]                             # (2)!
        ```

        1. מילון ממצב לסיבוב שבו נראה לראשונה. המצב הוא tuple, כי רשימה לא יכולה להיות
           מפתח.
        2. המצב הראשון שחוזר הוא תחילת המחזור. הוא נראה בסיבוב `seen[v]`, והוא חוזר
           בסיבוב `t`.

    === "SystemVerilog"
        ```systemverilog title="function automatic int ducci_orbit" linenums="1" hl_lines="9 14"
        // The length of the cycle the numbers enter, and in tail the rounds before it. All
        // zeros is a cycle of length 1.
        function automatic int ducci_orbit(int start[$], output int tail);
          int seen[string];
          int v[$];
          string key;
          int t = 0;
          v = start;
          while (1) begin
            key = "";
            foreach (v[i]) key = {key, $sformatf("%0d,", v[i])};   // (1)!
            if (seen.exists(key)) break;
            seen[key] = t;
            ducci_step(v);
            t++;
          end
          tail = seen[key];
          return t - tail;
        endfunction
        ```

        1. המפתח של המילון הוא המצב כמחרוזת, "0,1,1,". מערך אסוציאטיבי עם מפתח
           `string` הוא המילון של SystemVerilog.

    #### למה זה נכון { .sol-proof }

    **1, 2 ו-3.** שני סיבובים עד שנכנסים למחזור, ושלושה במחזור :

    <!-- gen 5 -->

    | סיבוב | מספר 1 | מספר 2 | מספר 3 | הערה |
    |:-:|:-:|:-:|:-:|---|
    | 0 | 1 | 2 | 3 | התחלה |
    | 1 | 1 | 1 | 2 |  |
    | 2 | 0 | 1 | 1 | נכנסים למחזור |
    | 3 | 1 | 0 | 1 |  |
    | 4 | 1 | 1 | 0 |  |
    | 5 | 0 | 1 | 1 | חוזר למצב של סיבוב 2 |

    <!-- /gen -->

    **אורכי המחזורים.** כל מחזור שהמשחק נכנס אליו מורכב מאפסים וממספר אחד \( c \) בלבד
    (משפט של Burmester, ‏Forcade ו-Jacobs משנת 1978), ולכן הוא \( c \) כפול מחזור של 0
    ו-1. האורכים שלו הם אורכי המחזורים של המשחק על 0 ו-1, והקוד מוצא את כולם מ-\( 2^n \)
    ההתחלות של 0 ו-1. הטסט של השאלה בודק גם את המשפט, בכל ההתחלות עם ערכים קטנים עד
    \( n = 10 \) :

    <!-- gen 6 -->

    | ‏n | חזקה של 2 | אורכי המחזורים, חוץ מהאפסים | ההתחלה של 1 אחד ואפסים |
    |:-:|:-:|---|---|
    | 3 | לא | 3 | מחזור באורך 3 |
    | 4 | כן | אין, תמיד מגיעים לאפסים | מגיעים לאפסים |
    | 5 | לא | 15 | מחזור באורך 15 |
    | 6 | לא | 3 ו-6 | מחזור באורך 6 |
    | 7 | לא | 7 | מחזור באורך 7 |
    | 8 | כן | אין, תמיד מגיעים לאפסים | מגיעים לאפסים |
    | 9 | לא | 3 ו-63 | מחזור באורך 63 |
    | 10 | לא | 15 ו-30 | מחזור באורך 30 |

    <!-- /gen -->

    **נסו בעצמכם.** אותה תיבה, עם 1, 2, 3, 4 ו-5 : המשחק נכנס למחזור באורך 15, והתיבה
    מסמנת את הסיבוב שבו המחזור מתחיל :

    <div class="explorer" data-kind="ducci" data-v="1,2,3,4,5"></div>

    #### סיבוכיות { .sol-cost }

    יש \( T \) סיבובים עד המחזור ו-\( L \) במחזור, כל אחד \( O(n) \), ועוד \( O(n) \) למפתח
    של המילון : \( O(n(T + L)) \) זמן וזיכרון. \( T + L \) לכל היותר \( (M + 1)^n \), אבל
    בפועל קטן בהרבה : ל-1 עד 5 זה 17.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : המקסימום יורד, אז זה נגמר"
    המקסימום לא עולה, אבל הוא לא חייב לרדת : 2, 0, 2 ו-0 הופכים ל-2, 2, 2 ו-2. ועם שלושה
    מספרים, 1, 2 ו-3 נכנסים למחזור שהמקסימום שלו נשאר 1 לנצח. צריך את הזוגיות כדי להוכיח
    ירידה של ממש, וכש-\( n \) אינו חזקה של 2 אין ירידה כזו.

??? trap "מלכודת : להכליל מארבעה"
    ארבעה מספרים תמיד מתאפסים, ולכן קל להניח ש"זה עובד לכל \( n \)". הניסיון הראשון עם
    שלושה מספרים, 1, 2 ו-3, כבר מראה שלא. המבנה הוא החזקה של 2, לא הזוגיות של \( n \) :
    גם 6 ו-10 מגיעים למחזורים.

??? trap "מלכודת : עדכון במקום בלי עותק"
    אם מעדכנים את \( v[i] \) במקום ואז משתמשים בו לחישוב של \( v[i-1] \), או מעדכנים את
    האחרון לפי \( v[0] \) החדש, מקבלים משחק אחר. ב-Python בונים רשימה חדשה, וב-SV שומרים
    את \( v[0] \) הישן לפני הלולאה.

??? followup "שאלות המשך"
    - **כמה סיבובים :** האם יש חסם על מספר הסיבובים לארבעה מספרים, בלי תלות במקסימום?

        ??? fu-answer "תשובה"
            לא. התחלות שנבנות ממספרי טריבונאצ'י לוקחות כל פעם יותר : 0, 7, 20 ו-44 לוקחים
            13 סיבובים, ו-0, 1705, 4841 ו-10609 לוקחים 25. החסם של סעיף א,
            \( 4(\lfloor \log_2 M \rfloor + 1) \), גדל עם \( M \).

    - **מספרים ממשיים :** האם ארבעה מספרים **ממשיים** תמיד מגיעים לאפסים?

        ??? fu-answer "תשובה"
            לא. עם \( q \approx 1.839 \), השורש של \( q^3 = q^2 + q + 1 \), ההתחלה
            \( 1, q, q^2, q^3 \) שומרת על הצורה שלה אחרי כל סיבוב, רק מוקטנת, ולכן לא מגיעה
            לאפס לעולם. ההוכחה של סעיף א השתמשה בזוגיות, שקיימת רק בשלמים.

    - **זיכרון קבוע :** איך מזהים את המחזור בלי מילון?

        ??? fu-answer "תשובה"
            השפן והצב של Floyd : שני מצבים, אחד מתקדם סיבוב אחד והשני שניים, עד שהם
            נפגשים. אחר כך מוצאים את תחילת המחזור ואת האורך שלו, ב-\( O(n) \) זיכרון במקום
            \( O(n(T + L)) \).

    - **החשבון של המחזורים :** למה ל-5 מספרים המחזור באורך 15?

        ??? fu-answer "תשובה"
            על 0 ו-1 הסיבוב הוא כפל ב-\( (1 + x) \) בפולינומים מודולו \( x^n - 1 \) מעל
            GF(2). ל-5 מספרים, 2 מודולו 5 חוזר אחרי 4 צעדים, והמחזור מחלק את \( 2^4 - 1 = 15 \).
            בפועל הוא 15. הטבלה של סעיף ג מחושבת בקוד.
