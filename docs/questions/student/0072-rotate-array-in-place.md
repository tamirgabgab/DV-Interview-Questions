---
id: 72
title: סיבוב מערך ב-k מקומות – במקום, בשלושה היפוכים או במעגלים
level: student
difficulty: medium
kind: code
tags: [algorithms, permutations, number-theory, python, systemverilog]
source: "שאלה קלאסית בראיונות קוד (rotate array), עם הרחבה ל-buffer מעגלי"
added: 2026-11-01
---

## השאלה

נתון מערך \( a \) באורך \( n \) ומספר \( k \ge 0 \). צריך **לסובב אותו שמאלה ב-\( k \) מקומות** : כל
איבר זז \( k \) מקומות שמאלה, ומי שיוצא מההתחלה נכנס בסוף. כלומר, אחרי הסיבוב
\( a[i] \) הוא מה שהיה ב-\( a[(i + k) \bmod n] \).

לדוגמה, ‏\( [1, 2, 3, 4, 5, 6, 7] \) עם \( k = 3 \) הופך ל-\( [4, 5, 6, 7, 1, 2, 3] \).

**התנאי :** במקום, כלומר עם זיכרון נוסף \( O(1) \) בלבד, בלי מערך עזר, ובזמן \( O(n) \).

- **סעיף א – שלושה היפוכים :** סובבו בעזרת היפוכים של קטעים בלבד, והוכיחו שזה נכון.
- **סעיף ב – מעגלים :** סובבו כך שכל איבר זז **פעם אחת** בלבד. כמה "מעגלים" יש, ולמה?
- **סעיף ג – buffer מעגלי :** ‏FIFO שמור בזיכרון של \( n \) כניסות, מלא, והאיבר הוותיק נמצא
  בכניסה ‏`head`. צריך לסדר אותו מחדש כך שהוותיק יהיה בכניסה 0. הזיכרון הוא single-port : קריאה
  אחת או כתיבה אחת בכל מחזור. כמה מחזורים לוקחת כל שיטה?

??? interviewer "מה המראיין בודק"
    - **במקום :** האם המועמד יודע לעבוד בלי מערך עזר, ומבין למה העתקה פשוטה דורסת ערכים.
    - **הוכחה קצרה :** האם הוא מסביר למה שלושת ההיפוכים נותנים סיבוב, ולא רק זוכר את הטריק.
    - **תורת המספרים :** האם הוא מוצא שמספר המעגלים הוא \( \gcd(n, k) \), ולא מניח שיש מעגל
      אחד.
    - **מקרי קצה :** ‏\( k = 0 \), ‏\( k \ge n \), ‏\( n = 0 \), וכיוון הסיבוב.
    - **חומרה :** האם הוא סופר גישות לזיכרון, ולא רק פעולות, כשהמחיר הוא מחזורים של SRAM.

---

### סעיף א – שלושה היפוכים

??? tip "רמז 1"
    כתבו את המערך כשני קטעים, \( A \) (‏\( k \) האיברים הראשונים) ו-\( B \) (השאר). הסיבוב הופך
    את \( AB \) ל-\( BA \). מה קורה ל-\( AB \) כשהופכים את כולו?

??? tip "רמז 2"
    היפוך של \( AB \) הוא \( B^R A^R \) : הקטעים מחליפים מקום, אבל כל אחד הפוך. איך מתקנים את זה?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        הופכים את \( k \) הראשונים, הופכים את השאר, ואז הופכים את כל המערך :
        ‏\( (A^R B^R)^R = B A \). כל היפוך הוא החלפות מהקצוות פנימה, ולכן הזיכרון הנוסף הוא משתנה
        אחד, והזמן הוא בערך \( n \) החלפות.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) | בערך n החלפות -->

    #### הרעיון { .sol-idea }

    **למה לא להעתיק.** הלולאה `a[i] = a[i + k]` דורסת את \( k \) הראשונים לפני שהם מגיעים
    לסוף. בלי מערך עזר צריך פעולה שלא מאבדת אף ערך, והחלפה (swap) היא כזו.

    **היפוך הוא כמעט סיבוב.** אם המערך הוא \( A B \), היפוך של כולו נותן \( B^R A^R \) : הקטעים כבר
    בסדר הנכון, רק שכל אחד מהם הפוך. לכן הופכים כל קטע **מראש**, וההיפוך האחרון מיישר אותם.
    על \( [1, \dots, 7] \) עם \( k = 3 \) :

    <!-- gen 0 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="שלושת ההיפוכים על 1 עד 7 עם k = 3 : בכל שורה המערך אחרי ההיפוך, והקטע שהתהפך ממוסגר"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td></tr><tr><th dir="rtl">לפני</th><td class="pm-c c1">1</td><td class="pm-c c1">2</td><td class="pm-c c1">3</td><td class="pm-c c2">4</td><td class="pm-c c2">5</td><td class="pm-c c2">6</td><td class="pm-c c2">7</td></tr><tr><th dir="rtl">היפוך של A</th><td class="pm-c is-hl">3</td><td class="pm-c is-hl">2</td><td class="pm-c is-hl">1</td><td class="pm-c c2">4</td><td class="pm-c c2">5</td><td class="pm-c c2">6</td><td class="pm-c c2">7</td></tr><tr><th dir="rtl">היפוך של B</th><td class="pm-c c1">3</td><td class="pm-c c1">2</td><td class="pm-c c1">1</td><td class="pm-c is-hl">7</td><td class="pm-c is-hl">6</td><td class="pm-c is-hl">5</td><td class="pm-c is-hl">4</td></tr><tr><th dir="rtl">היפוך של הכול</th><td class="pm-c is-hl">4</td><td class="pm-c is-hl">5</td><td class="pm-c is-hl">6</td><td class="pm-c is-hl">7</td><td class="pm-c is-hl">1</td><td class="pm-c is-hl">2</td><td class="pm-c is-hl">3</td></tr></tbody></table></div>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מנרמלים :** ‏\( k \leftarrow k \bmod n \). סיבוב ב-\( n \) מחזיר את המערך למקומו. אם יצא 0,
       אין מה לעשות.
    2. **היפוך של \( A \) :** האיברים \( 0 \) עד \( k - 1 \).
    3. **היפוך של \( B \) :** האיברים \( k \) עד \( n - 1 \).
    4. **היפוך של הכול :** ‏\( (A^R B^R)^R = (B^R)^R (A^R)^R = B A \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="reverse_range, rotate_reversals" linenums="1" hl_lines="11 12 13"
        def reverse_range(a: list, lo: int, hi: int) -> None:
            """Reverse a[lo:hi] in place, swapping from both ends inward."""
            hi -= 1
            while lo < hi:
                a[lo], a[hi] = a[hi], a[lo]
                lo, hi = lo + 1, hi - 1


        def rotate_reversals(a: list, k: int) -> None:
            """Rotate a left by k places in place: a[i] becomes the old a[(i + k) % n]."""
            n = len(a)
            if n == 0 or k % n == 0:
                return
            k %= n                                 # (1)!
            reverse_range(a, 0, k)
            reverse_range(a, k, n)
            reverse_range(a, 0, n)
        ```

        1. ‏\( k \ge n \) מותר : סיבוב ב-\( n \) לא משנה כלום. ב-Python ‏`%` נותן גם ל-\( k \) שלילי
           ערך בין 0 ל-\( n - 1 \), כלומר סיבוב ימינה.

    === "SystemVerilog"
        ```systemverilog title="function reverse_range, rotate_reversals" linenums="1" hl_lines="16 17 18"
        // reverse a[lo .. hi-1] in place, swapping from both ends inward
        function automatic void reverse_range(ref int a[], input int lo, input int hi);
          int t;
          hi--;
          while (lo < hi) begin
            t = a[lo]; a[lo] = a[hi]; a[hi] = t;
            lo++; hi--;
          end
        endfunction

        // rotate a left by k >= 0 places in place: a[i] becomes the old a[(i + k) % n]
        function automatic void rotate_reversals(ref int a[], input int k);
          int n = a.size();
          if (n == 0 || k % n == 0) return;
          k = k % n;
          reverse_range(a, 0, k);
          reverse_range(a, k, n);
          reverse_range(a, 0, n);
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    היפוך של קטע באורך \( L \) שולח את המקום \( j \) בקטע למקום \( L - 1 - j \). נעקוב אחרי איבר
    אחד :

    - **איבר מ-\( A \), במקום \( i < k \) :** אחרי ההיפוך הראשון הוא במקום \( k - 1 - i \), ואחרי
      ההיפוך של הכול במקום \( n - 1 - (k - 1 - i) = n - k + i \). זה בדיוק \( i - k \bmod n \).
    - **איבר מ-\( B \), במקום \( i \ge k \) :** אחרי ההיפוך השני הוא במקום \( k + (n - 1 - i) \), ואחרי
      ההיפוך של הכול במקום \( n - 1 - k - (n - 1 - i) = i - k \).

    כלומר כל איבר זז \( k \) מקומות שמאלה, מעגלית. **המחיר :** ‏\( \lfloor k/2 \rfloor + \lfloor (n-k)/2 \rfloor + \lfloor n/2 \rfloor \)
    החלפות, בערך \( n \). כל איבר זז פעמיים.

---

### סעיף ב – מעגלים

??? tip "רמז 1"
    האיבר שיגיע למקום 0 נמצא עכשיו במקום \( k \). מי יגיע למקום \( k \)? ולמקום שאחריו?

??? tip "רמז 2"
    המסלול \( 0, k, 2k, \dots \) (מודולו \( n \)) חוזר ל-0. אחרי כמה צעדים? ומה עם המקומות שהוא
    לא עבר בהם?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        שומרים את \( a[s] \) בצד, ומושכים לאורך המעגל : ‏\( a[s] \leftarrow a[s + k] \leftarrow a[s + 2k] \dots \),
        עד שחוזרים ל-\( s \), ושם כותבים את מה ששמרנו. יש **\( g = \gcd(n, k) \) מעגלים**, כל אחד באורך
        \( n / g \), והם מתחילים ב-\( s = 0, 1, \dots, g - 1 \). כל איבר נקרא פעם אחת ונכתב פעם אחת.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) | השמות n ועוד gcd -->

    #### הרעיון { .sol-idea }

    **סיבוב הוא תמורה.** המקום \( i \) מקבל את הערך מ-\( i + k \). אם מתחילים ממקום \( s \) והולכים
    כל פעם \( k \) קדימה, מגיעים בסוף בחזרה ל-\( s \) : זה **מעגל** של התמורה. בתוך מעגל מזיזים כל
    איבר צעד אחד, עם משתנה זמני אחד בלבד.

    **יכול להיות יותר ממעגל אחד.** עם \( n = 12 \) ו-\( k = 8 \), המעגל שמתחיל ב-0 עובר רק ב-0, 8 ו-4.
    המקומות מתחלקים לארבעה מעגלים :

    <!-- gen 1 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="המעגלים של n = 12 ו-k = 8 : לכל אינדקס, מספר המעגל שלו"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td><td>11</td></tr><tr><th dir="rtl">המעגל</th><td class="pm-c c1">1</td><td class="pm-c c2">2</td><td class="pm-c c3">3</td><td class="pm-c c4">4</td><td class="pm-c c1">1</td><td class="pm-c c2">2</td><td class="pm-c c3">3</td><td class="pm-c c4">4</td><td class="pm-c c1">1</td><td class="pm-c c2">2</td><td class="pm-c c3">3</td><td class="pm-c c4">4</td></tr></tbody></table></div>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="pm-key-c1"></i>מעגל 1</span><span><i class="pm-key-c2"></i>מעגל 2</span><span><i class="pm-key-c3"></i>מעגל 3</span><span><i class="pm-key-c4"></i>מעגל 4</span></span>

    <!-- /gen -->

    <!-- gen 3 -->

    | המעגל | ההעברות | האורך |
    |:-:|:-:|:-:|
    | ‏1 | ‏`a[0] ← a[8] ← a[4] ← tmp` | ‏3 |
    | ‏2 | ‏`a[1] ← a[9] ← a[5] ← tmp` | ‏3 |
    | ‏3 | ‏`a[2] ← a[10] ← a[6] ← tmp` | ‏3 |
    | ‏4 | ‏`a[3] ← a[11] ← a[7] ← tmp` | ‏3 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מנרמלים :** ‏\( k \leftarrow k \bmod n \). אם יצא 0, אין מה לעשות.
    2. **מספר המעגלים :** ‏\( g = \gcd(n, k) \), באלגוריתם של אוקלידס.
    3. **לכל מעגל, \( s = 0 \) עד \( g - 1 \) :** שומרים \( \mathit{tmp} = a[s] \), ומ-\( i = s \) מושכים
       \( a[i] \leftarrow a[i + k] \) (מודולו \( n \)) ומתקדמים, עד שהמקום הבא הוא שוב \( s \).
    4. **סוגרים את המעגל :** במקום האחרון כותבים את \( \mathit{tmp} \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="rotate_cycles" linenums="1" hl_lines="10 15 16 19"
        from math import gcd


        def rotate_cycles(a: list, k: int) -> None:
            """Rotate a left by k places, moving every entry once along the cycles."""
            n = len(a)
            if n == 0 or k % n == 0:
                return
            k %= n
            for s in range(gcd(n, k)):             # (1)!
                tmp, i = a[s], s
                while True:
                    j = i + k
                    if j >= n:
                        j -= n                     # (2)!
                    if j == s:
                        break
                    a[i], i = a[j], j
                a[i] = tmp
        ```

        1. כל מעגל מכיל בדיוק מקום אחד מבין \( 0, \dots, g - 1 \), ולכן אלה ההתחלות.
        2. ‏\( i < n \) ו-\( k < n \), ולכן חיסור אחד מספיק במקום `%`. בחומרה זה חיבור והשוואה.

    === "SystemVerilog"
        ```systemverilog title="function gcd_of, rotate_cycles" linenums="1" hl_lines="14 18 19 21"
        function automatic int gcd_of(int x, int y);
          int t;
          while (y != 0) begin t = x % y; x = y; y = t; end
          return x;
        endfunction

        // rotate a left by k >= 0 places, moving every entry once along the cycles
        function automatic void rotate_cycles(ref int a[], input int k);
          int n = a.size();
          int g, i, j, tmp;
          if (n == 0 || k % n == 0) return;
          k = k % n;
          g = gcd_of(n, k);
          for (int s = 0; s < g; s++) begin
            tmp = a[s];
            i = s;
            forever begin
              j = i + k;
              if (j >= n) j -= n;
              if (j == s) break;
              a[i] = a[j];
              i = j;
            end
            a[i] = tmp;
          end
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **אורך המעגל.** מ-\( s \) מגיעים אחרי \( t \) צעדים ל-\( s + tk \bmod n \). חוזרים ל-\( s \) כש-\( n \)
    מחלק את \( tk \), והקטן ביותר כזה הוא \( t = n / g \) : נכתוב \( n = g n' \), ‏\( k = g k' \), עם \( n' \) ו-\( k' \)
    זרים, ואז \( n' \mid t k' \) גורר \( n' \mid t \).

    **מספר המעגלים.** יש \( n \) מקומות, וכל מעגל באורך \( n / g \), ולכן יש \( g \) מעגלים. כל צעד מוסיף
    \( k \), שמתחלק ב-\( g \), ולכן כל המקומות במעגל נותנים אותה שארית בחלוקה ב-\( g \). כך כל אחד
    מ-\( 0, \dots, g - 1 \) נמצא במעגל אחר, והם בדיוק ההתחלות.

    **המחיר.** כל מקום נכתב פעם אחת : ‏\( n - g \) השמות לאורך המעגלים, ועוד \( g \) השמות של \( \mathit{tmp} \).
    אם \( \gcd(n, k) = 1 \) (למשל \( n \) ראשוני) יש מעגל אחד שעובר בכל המערך.

---

### סעיף ג – buffer מעגלי

??? tip "רמז 1"
    הסידור מחדש הוא סיבוב שמאלה ב-`head`. מה עולה החלפה אחת, כשכל קריאה וכל כתיבה הן מחזור?

??? tip "רמז 2"
    בשיטת המעגלים, כמה פעמים קוראים כל כניסה, וכמה פעמים כותבים אותה? ‏`tmp` יכול לשבת ברגיסטר.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        זה סיבוב שמאלה ב-`head`. בשיטת המעגלים כל כניסה נקראת פעם אחת ונכתבת פעם אחת : **\( 2n \)
        מחזורים**. שלושת ההיפוכים קוראים וכותבים כל כניסה בערך פעמיים, כי החלפה היא שתי קריאות
        ושתי כתיבות : בערך **\( 4n \) מחזורים**, בדיוק \( 4 \) כפול מספר ההחלפות של סעיף א.

    <!-- cost: זמן \( 2n \) מחזורים | זיכרון רגיסטר אחד -->

    #### הרעיון { .sol-idea }

    **מה שחשוב הוא גישות.** בתוכנה החלפה והשמה עולות בערך אותו דבר. מול זיכרון single-port כל
    קריאה וכל כתיבה הן מחזור, ולכן סופרים גישות לזיכרון. במעגלים, הערך ב-`tmp` ובכל "יד" נמצא
    ברגיסטר, וכל כניסה עוברת פעם אחת בלבד.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="Ram, linearize" linenums="1" hl_lines="21 23 24"
        from math import gcd


        class Ram:
            """A single-port memory: one read or one write per cycle."""
            def __init__(self, data):
                self.mem, self.cycles = list(data), 0
            def read(self, i):
                self.cycles += 1
                return self.mem[i]
            def write(self, i, v):
                self.cycles += 1
                self.mem[i] = v


        def linearize(ram: Ram, head: int) -> None:
            """Move the oldest entry (at head) to entry 0, the cycles way."""
            n = len(ram.mem)
            if head % n == 0:
                return
            for s in range(gcd(n, head)):
                tmp, i = ram.read(s), s          # (1)!
                while (j := (i + head) % n) != s:
                    ram.write(i, ram.read(j))
                    i = j
                ram.write(i, tmp)
        ```

        1. כל כניסה נקראת פעם אחת : ההתחלה כאן, וכל השאר כשמושכים מהן. כל כניסה נכתבת פעם
           אחת. סה"כ \( 2n \) מחזורים.

    === "SystemVerilog"
        ```systemverilog title="class Ram, function linearize" linenums="1" hl_lines="21 22 24"
        class Ram;                             // a single-port memory: one access per cycle
          int mem[];
          int cycles;
          function new(int data[]);
            mem = data;
            cycles = 0;
          endfunction
          function int read(int i);
            cycles++;
            return mem[i];
          endfunction
          function void write(int i, int v);
            cycles++;
            mem[i] = v;
          endfunction
        endclass

        // move the oldest entry (at head) to entry 0, the cycles way
        function automatic void linearize(Ram ram, int head);
          int n = ram.mem.size();
          int tmp, i, j;
          if (head % n == 0) return;
          for (int s = 0; s < gcd_of(n, head); s++) begin
            tmp = ram.read(s);
            i = s;
            forever begin
              j = (i + head) % n;
              if (j == s) break;
              ram.write(i, ram.read(j));
              i = j;
            end
            ram.write(i, tmp);
          end
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **מעגלים.** כל מעגל באורך \( L \) עולה \( L \) קריאות ו-\( L \) כתיבות, ואורכי המעגלים מסתכמים
    ב-\( n \) : ‏\( 2n \) בדיוק.

    **היפוכים.** כל החלפה קוראת שתי כניסות וכותבת שתיים, ולכן \( 4 \left( \lfloor h/2 \rfloor + \lfloor (n-h)/2 \rfloor + \lfloor n/2 \rfloor \right) \),
    כש-\( h \) הוא `head`. זה בערך \( 4n \) :

    <!-- gen 4 -->

    | ‏n | ‏head | שלושה היפוכים | מעגלים |
    |:-:|:-:|:-:|:-:|
    | ‏8 | ‏3 | ‏28 | ‏16 |
    | ‏8 | ‏4 | ‏32 | ‏16 |
    | ‏12 | ‏5 | ‏44 | ‏24 |
    | ‏1024 | ‏300 | ‏4096 | ‏2048 |

    <!-- /gen -->

    **אבל.** ההיפוכים ניגשים לזיכרון ברצף, משני הקצוות, והמעגלים קופצים בצעדים של \( k \). מול
    cache או DRAM, שבהם גישה רציפה זולה, ההיפוכים יכולים לנצח למרות שהם ניגשים יותר. מול SRAM
    פשוט, המעגלים מנצחים.

    **נסו בעצמכם.** בוחרים \( n \), ‏\( k \) ושיטה, ומתקדמים צעד אחרי צעד : בהיפוכים כל צעד הוא
    החלפה, ובמעגלים כל צעד הוא השמה אחת, והתאים צבועים לפי המעגל שלהם.

    <div class="explorer" data-kind="rotatek" data-n="7" data-k="3" data-method="rev"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : מעגל אחד"
    הלולאה "שומרים את \( a[0] \) ומושכים עד שחוזרים ל-0" נכונה רק כש-\( \gcd(n, k) = 1 \). עם
    \( n = 12 \), ‏\( k = 8 \) היא מזיזה רק את 0, 8 ו-4, ומשאירה תשעה מקומות במקום.

??? trap "מלכודת : ‏k גדול מ-n, ו-k = 0"
    בלי \( k \bmod n \) ההיפוך הראשון יוצא מהמערך. ‏\( k = 0 \) או \( k = n \) לא צריכים לעשות כלום.
    בלי בדיקה, ההיפוכים עושים \( n \) החלפות מיותרות, וב-SV ‏\( k \bmod 0 \) על מערך ריק הוא חילוק
    באפס.

??? trap "מלכודת : הכיוון"
    סיבוב שמאלה ב-\( k \) הוא סיבוב ימינה ב-\( n - k \). ההיפוכים ההפוכים, קודם הכול ואז שני
    הקטעים, מסובבים ימינה. כדאי לבדוק על דוגמה קטנה לפני שכותבים.

??? followup "שאלות המשך"
    - **סיבוב ימינה :** איך מסובבים ימינה ב-\( k \) עם אותן פונקציות?

        ??? fu-answer "תשובה"
            סיבוב שמאלה ב-\( n - k \). או בהיפוכים : קודם את הכול, ואז את \( k \) הראשונים ואת השאר.

    - **רשימה מקושרת :** איך מסובבים רשימה מקושרת ב-\( k \)?

        ??? fu-answer "תשובה"
            לא מזיזים ערכים : מוצאים את הצומת ה-\( k \), מחברים את הזנב לראש וחותכים אחרי הצומת
            ה-\( k - 1 \). זמן \( O(n) \), בלי שום העתקה.

    - **בחומרה, וקטור ביטים :** איך מסובבים וקטור של \( n \) ביטים ב-\( k \) במחזור אחד?

        ??? fu-answer "תשובה"
            ‏barrel shifter : ‏\( \log_2 n \) שלבים של mux, שלב \( j \) מסובב ב-\( 2^j \) לפי ביט \( j \) של
            \( k \). ל-\( k \) קבוע זה רק חיווט, בלי שערים.

    - **בלי gcd :** איך מוצאים את המעגלים בלי לחשב \( \gcd \)?

        ??? fu-answer "תשובה"
            סופרים כמה השמות עשינו, ומתחילים מעגל חדש ב-\( s + 1 \) עד שהגענו ל-\( n \). זה עובד
            כי המעגלים מתחילים בדיוק ב-\( 0, \dots, g - 1 \).
