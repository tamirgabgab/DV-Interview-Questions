---
id: 73
title: ערבוב מושלם של חפיסה – כמה ערבובים עד שהיא חוזרת, ושילוב במקום
level: junior
difficulty: medium
kind: code
tags: [permutations, number-theory, algorithms, python, systemverilog]
source: "חידת הקלפים של ה-faro shuffle, עם הכללה לכל גודל ושאלת קוד על שילוב במקום"
added: 2026-11-01
---

## השאלה

**ערבוב מושלם** (faro shuffle) : חוצים חפיסה בדיוק לשני חצאים, ומשלבים אותם קלף אחרי קלף.

- **‏out-shuffle :** הקלף העליון של החפיסה נשאר למעלה. מהחצי העליון \( t_0, t_1, \dots \) ומהתחתון
  \( b_0, b_1, \dots \) יוצא \( t_0, b_0, t_1, b_1, \dots \).
- **‏in-shuffle :** הקלף העליון יורד למקום השני : ‏\( b_0, t_0, b_1, t_1, \dots \).

שאלות :

- **סעיף א – 52 קלפים :** אחרי כמה out-shuffles חפיסה של 52 קלפים חוזרת לסדר המקורי? ואחרי כמה
  in-shuffles?
- **סעיף ב – כל גודל :** אותה שאלה לחפיסה של \( n \) קלפים, זוגי או אי-זוגי. כתבו נוסחה, והוכיחו
  שהחפיסה תמיד חוזרת.
- **סעיף ג – שילוב במקום :** כתבו קוד שהופך מערך \( [a_0, \dots, a_{m-1}, b_0, \dots, b_{m-1}] \)
  ל-\( [a_0, b_0, a_1, b_1, \dots] \), כלומר out-shuffle, בלי מערך עזר.

??? interviewer "מה המראיין בודק"
    - **נוסחה למקום :** האם המועמד כותב לאן הולך הקלף במקום \( p \), במקום לסמלץ.
    - **תורת המספרים :** האם הוא מזהה שזו הכפלה ב-2 מודולו מספר, ומבין למה היא תמיד חוזרת
      ל-1.
    - **מקרי קצה :** הקלף העליון והתחתון שלא זזים, ו-\( n \) אי-זוגי.
    - **במקום :** האם הוא משתמש בסיבוב של מערך (שאלה 0072) כאבן בניין, ויודע להעריך את המחיר.

---

### סעיף א – 52 קלפים

??? tip "רמז 1"
    מספרו את המקומות מ-0. לאן עובר הקלף במקום 1 ב-out-shuffle? ובמקום 2? ובמקום 26, הראשון
    בחצי התחתון?

??? tip "רמז 2"
    ‏\( p \to 2p \) בחצי העליון, ו-\( p \to 2p - 51 \) בתחתון : זה \( 2p \bmod 51 \). מתי \( 2^e \bmod 51 \)
    חוזר ל-1?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏**8 out-shuffles**, ו-**52 in-shuffles**. ב-out-shuffle הקלף במקום \( p \) עובר ל-\( 2p \bmod 51 \)
        (חוץ מהקלף התחתון, שלא זז), ולכן אחרי \( e \) ערבובים הוא ב-\( 2^e p \bmod 51 \). ‏\( 2^8 = 256 \equiv 1 \pmod{51} \),
        ו-8 הוא החזקה הקטנה ביותר. ב-in-shuffle המודולו הוא 53, ו-2 מגיע ל-1 רק בחזקה 52.

    #### הרעיון { .sol-idea }

    **לא מסמלצים, כותבים נוסחה.** נמספר את המקומות מ-0 (למעלה) עד 51. ב-out-shuffle הקלף ה-\( p \)
    של החצי העליון נוחת במקום \( 2p \), והקלף ה-\( j \) של החצי התחתון, שהיה במקום \( 26 + j \), נוחת
    במקום \( 2j + 1 \). שני המקרים הם אותה נוסחה :

    \[
    p \;\longmapsto\; 2p \bmod 51, \qquad 0 \le p \le 50,
    \]

    והקלף במקום 51 נשאר למטה. על 8 קלפים (מודולו 7) אפשר לראות את זה : המקומות מתחלקים למעגלים,
    וכל המעגלים חוזרים יחד אחרי 3 ערבובים.

    <!-- gen 0 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="שמונה קלפים בשלושה out-shuffles : בכל שורה הסדר מלמעלה, ואחרי שלושה ערבובים הסדר חוזר"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr><tr><th dir="rtl">לפני</th><td class="pm-c c1">0</td><td class="pm-c c2">1</td><td class="pm-c c2">2</td><td class="pm-c c3">3</td><td class="pm-c c2">4</td><td class="pm-c c3">5</td><td class="pm-c c3">6</td><td class="pm-c c4">7</td></tr><tr><th dir="rtl">אחרי 1</th><td class="pm-c c1">0</td><td class="pm-c c2">4</td><td class="pm-c c2">1</td><td class="pm-c c3">5</td><td class="pm-c c2">2</td><td class="pm-c c3">6</td><td class="pm-c c3">3</td><td class="pm-c c4">7</td></tr><tr><th dir="rtl">אחרי 2</th><td class="pm-c c1">0</td><td class="pm-c c2">2</td><td class="pm-c c2">4</td><td class="pm-c c3">6</td><td class="pm-c c2">1</td><td class="pm-c c3">3</td><td class="pm-c c3">5</td><td class="pm-c c4">7</td></tr><tr><th dir="rtl">אחרי 3</th><td class="pm-c c1">0</td><td class="pm-c c2">1</td><td class="pm-c c2">2</td><td class="pm-c c3">3</td><td class="pm-c c2">4</td><td class="pm-c c3">5</td><td class="pm-c c3">6</td><td class="pm-c c4">7</td></tr></tbody></table></div>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="pm-key-c1"></i>0 נשאר למעלה</span><span><i class="pm-key-c2"></i>‏1, 2, 4</span><span><i class="pm-key-c3"></i>‏3, 6, 5</span><span><i class="pm-key-c4"></i>‏7 נשאר למטה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏out-shuffle :** ‏\( p \to 2p \bmod 51 \). אחרי \( e \) ערבובים, \( p \to 2^e p \bmod 51 \).
    2. **מתי כולם חוזרים :** כש-\( 2^e p \equiv p \) לכל \( p \), ובפרט ל-\( p = 1 \) : ‏\( 2^e \equiv 1 \pmod{51} \).
    3. **החזקות של 2 מודולו 51 :** ‏2, 4, 8, 16, 32, 13, 26, 1. **‏\( e = 8 \).**
    4. **‏in-shuffle :** במספור מ-1, הקלף \( q \) עובר ל-\( 2q \bmod 53 \). ‏53 ראשוני, וההחזקות של 2
       עוברות על כל 52 השאריות לפני שחוזרות ל-1 : **‏\( e = 52 \)**.

    </div>

    #### למה זה נכון { .sol-proof }

    **‏out-shuffle.** הקלף במקום \( p < 26 \) הולך ל-\( 2p < 51 \). הקלף במקום \( p = 26 + j \) הולך ל-\( 2j + 1 \),
    ו-\( 2p = 52 + 2j = 51 + (2j + 1) \), כלומר \( 2p \bmod 51 = 2j + 1 \) (גם עבור \( j = 25 \) : ‏\( p = 51 \)
    הולך ל-51, ו-\( 102 \bmod 51 = 0 \). לכן מוציאים את 51 מהנוסחה, הוא תמיד בתחתית).

    **‏in-shuffle.** במספור מ-1, הקלף \( q \le 26 \) הולך למקום \( 2q \), והקלף \( q = 26 + j \) (‏\( j \ge 1 \))
    הולך ל-\( 2j - 1 = 2q - 53 \). שוב אותה נוסחה, \( 2q \bmod 53 \), הפעם בלי קלף קבוע.

    **למה 52.** אם \( 2^e \equiv 1 \pmod{53} \) אז \( e \) מחלק את 52, כלומר הוא 1, 2, 4, 13, 26 או 52.
    ‏\( 2^{13} = 8192 \equiv 30 \) ו-\( 2^{26} \equiv 30^2 = 900 \equiv -1 \), ולכן אף מחלק קטן לא מתאים.

---

### סעיף ב – כל גודל

??? tip "רמז 1"
    בסעיף א המודולו היה \( n - 1 \) ב-out ו-\( n + 1 \) ב-in. מה קורה כש-\( n \) אי-זוגי, והחצי העליון
    גדול מהתחתון בקלף אחד?

??? tip "רמז 2"
    למה תמיד קיימת חזקה \( e \) עם \( 2^e \equiv 1 \pmod M \)? חשבו על \( M \) אי-זוגי ועל עקרון שובך
    היונים בין החזקות של 2.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        כל ערבוב הוא \( p \to 2p \bmod M \), ולכן מספר הערבובים הוא **הסדר של 2 מודולו \( M \)** : החזקה
        הקטנה ביותר \( e \) עם \( 2^e \equiv 1 \pmod M \). ל-\( n \) זוגי, ‏\( M = n - 1 \) ב-out ו-\( M = n + 1 \)
        ב-in. ל-\( n \) אי-זוגי, ‏\( M = n \). ‏\( M \) תמיד אי-זוגי, ולכן החזקה קיימת, ו-\( e \le M - 1 \).

    <!-- cost: זמן \( O(M) \) לכל היותר | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **אותה נוסחה בכל הגדלים.** ב-\( n \) אי-זוגי החצי העליון גדול בקלף אחד, והקלף העליון נשאר
    למעלה. זה בדיוק out-shuffle של \( n + 1 \) קלפים בלי הקלף התחתון, שממילא לא זז : מודולו \( n \).
    כך יוצאת טבלה לכל גודל :

    <!-- gen 2 -->

    | ‏n | ‏out | ‏in |
    |:-:|:-:|:-:|
    | ‏8 | ‏3 (מודולו 7) | ‏6 (מודולו 9) |
    | ‏10 | ‏6 (מודולו 9) | ‏10 (מודולו 11) |
    | ‏16 | ‏4 (מודולו 15) | ‏8 (מודולו 17) |
    | ‏52 | ‏8 (מודולו 51) | ‏52 (מודולו 53) |
    | ‏64 | ‏6 (מודולו 63) | ‏12 (מודולו 65) |
    | ‏100 | ‏30 (מודולו 99) | ‏100 (מודולו 101) |
    | ‏7 (אי-זוגי) | ‏3 (מודולו 7) | — |
    | ‏51 (אי-זוגי) | ‏8 (מודולו 51) | — |

    <!-- /gen -->

    **‏\( n = 2^j \).** ב-out-shuffle, ‏\( 2^j \equiv 1 \pmod{2^j - 1} \), ולכן \( j \) ערבובים : 64 קלפים חוזרים
    אחרי 6. בכתיבה בינארית, ‏\( p \to 2p \bmod (2^j - 1) \) הוא **סיבוב של \( j \) הביטים** של \( p \) שמאלה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המודולו :** ‏\( M = n - 1 \) (out, ‏\( n \) זוגי), ‏\( M = n + 1 \) (in, ‏\( n \) זוגי), ‏\( M = n \) (‏\( n \) אי-זוגי).
    2. **מקרה קצה :** ‏\( M = 1 \) (שני קלפים, out) : הערבוב לא משנה כלום, ‏\( e = 1 \).
    3. **הסדר של 2 :** מכפילים ב-2 מודולו \( M \) עד שמגיעים ל-1, וסופרים.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="shuffles_to_return" linenums="1" hl_lines="4 8 10 11"
        def shuffles_to_return(n: int, kind: str = "out") -> int:
            """How many perfect shuffles bring a deck of n cards back to its order."""
            if n % 2:
                m = n                              # (1)!
            else:
                m = n - 1 if kind == "out" else n + 1
            if m == 1:
                return 1
            e, p = 1, 2 % m
            while p != 1:                          # (2)!
                p, e = 2 * p % m, e + 1
            return e
        ```

        1. ב-\( n \) אי-זוגי שני הסוגים מגיעים לאותה נוסחה, מודולו \( n \).
        2. ‏\( m \) אי-זוגי, ולכן הלולאה נעצרת אחרי \( m - 1 \) סיבובים לכל היותר.

    === "SystemVerilog"
        ```systemverilog title="function shuffles_to_return" linenums="1" hl_lines="5 7 8 10 11"
        // how many perfect shuffles bring a deck of n cards back; is_out = 1 for out-shuffles
        function automatic int shuffles_to_return(int n, bit is_out = 1);
          int m, e, p;
          if (n % 2 == 1) m = n;
          else if (is_out) m = n - 1;
          else m = n + 1;
          if (m == 1) return 1;
          e = 1;
          p = 2 % m;
          while (p != 1) begin
            p = (2 * p) % m;
            e++;
          end
          return e;
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **תמיד חוזרים.** ‏\( M \) אי-זוגי, ולכן 2 זר לו. בין החזקות \( 2^0, 2^1, \dots, 2^{M} \) יש \( M + 1 \)
    ערכים מודולו \( M \), ולכן שתיים שוות : ‏\( 2^a \equiv 2^b \) עם \( a < b \). אפשר לחלק ב-\( 2^a \), כי 2
    הפיך מודולו \( M \), ומקבלים \( 2^{b-a} \equiv 1 \).

    **החסם.** ‏\( 2^e \bmod M \) אף פעם לא 0, ולכן יש לכל היותר \( M - 1 \) ערכים לפני שחוזרים ל-1. לפי
    משפט אוילר, ‏\( e \) גם מחלק את \( \varphi(M) \). כש-\( M \) ראשוני ו-2 הוא שורש פרימיטיבי, ‏\( e = M - 1 \)
    הוא המקסימום : 52 in-shuffles ל-52 קלפים, 100 in-shuffles ל-100.

---

### סעיף ג – שילוב במקום

??? tip "רמז 1"
    חלקו כל חצי לשניים : ‏\( A_1 A_2 B_1 B_2 \). מה צריך לעשות כדי לקבל \( A_1 B_1 \, A_2 B_2 \)?

??? tip "רמז 2"
    להחליף את \( A_2 \) ו-\( B_1 \) זה **סיבוב** של הקטע \( A_2 B_1 \), כמו בשאלה 0072. ואחרי זה יש שתי
    בעיות של חצי הגודל.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        הפרד ומשול : כותבים \( A = A_1 A_2 \), ‏\( B = B_1 B_2 \) (חצאים), ומסובבים את \( A_2 B_1 \) ל-\( B_1 A_2 \)
        בשלושה היפוכים. עכשיו יש \( A_1 B_1 \) ו-\( A_2 B_2 \), שתי בעיות בחצי הגודל. כל רמה עולה
        \( O(n) \), ויש \( \log_2 n \) רמות : ‏\( O(n \log n) \) זמן ו-\( O(1) \) זיכרון, עם מחסנית של קטעים
        (או \( O(\log n) \) ברקורסיה).

    <!-- cost: זמן \( O(n \log n) \) | זיכרון \( O(\log n) \) למחסנית -->

    #### הרעיון { .sol-idea }

    **סיבוב במקום הוא כלי.** כשהקטעים לא בסדר הנכון, מחליפים שני קטעים סמוכים בסיבוב, בלי זיכרון
    נוסף. על \( m = 4 \) :

    <!-- gen 3 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="השילוב במקום של a0 עד a3 ו-b0 עד b3 : בכל רמה מסובבים את הקטעים הממוסגרים"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr><tr><th dir="rtl">לפני</th><td class="pm-c c1">a0</td><td class="pm-c c1">a1</td><td class="pm-c c1">a2</td><td class="pm-c c1">a3</td><td class="pm-c c2">b0</td><td class="pm-c c2">b1</td><td class="pm-c c2">b2</td><td class="pm-c c2">b3</td></tr><tr><th dir="rtl">רמה 1</th><td class="pm-c c1">a0</td><td class="pm-c c1">a1</td><td class="pm-c c2 is-hl">b0</td><td class="pm-c c2 is-hl">b1</td><td class="pm-c c1 is-hl">a2</td><td class="pm-c c1 is-hl">a3</td><td class="pm-c c2">b2</td><td class="pm-c c2">b3</td></tr><tr><th dir="rtl">רמה 2</th><td class="pm-c c1">a0</td><td class="pm-c c2 is-hl">b0</td><td class="pm-c c1 is-hl">a1</td><td class="pm-c c2">b1</td><td class="pm-c c1">a2</td><td class="pm-c c2 is-hl">b2</td><td class="pm-c c1 is-hl">a3</td><td class="pm-c c2">b3</td></tr></tbody></table></div>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **קטע ראשון :** כל המערך, \( 2m \) איברים, \( m \) מכל צד.
    2. **החלוקה :** ‏\( h = \lfloor m/2 \rfloor \), ‏\( A_1 \) ו-\( B_1 \) באורך \( h \), ‏\( A_2 \) ו-\( B_2 \) באורך \( m - h \).
    3. **הסיבוב :** הקטע \( A_2 B_1 \) (מ-\( h \) עד \( m + h \)) מסתובב שמאלה ב-\( m - h \), ונהיה \( B_1 A_2 \).
    4. **שני תת-קטעים :** ‏\( A_1 B_1 \) עם \( h \) מכל צד, ו-\( A_2 B_2 \) עם \( m - h \) מכל צד. קטע עם
       \( m \le 1 \) כבר משולב.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="interleave" linenums="1" hl_lines="10 11 12 23 24"
        def reverse_range(a: list, lo: int, hi: int) -> None:
            hi -= 1
            while lo < hi:
                a[lo], a[hi] = a[hi], a[lo]
                lo, hi = lo + 1, hi - 1


        def rotate_left(a: list, lo: int, hi: int, k: int) -> None:
            """Rotate a[lo:hi] left by k places (0 <= k <= hi - lo), by three reversals."""
            reverse_range(a, lo, lo + k)
            reverse_range(a, lo + k, hi)
            reverse_range(a, lo, hi)


        def interleave(a: list) -> None:
            """[a0..a(m-1), b0..b(m-1)] -> [a0, b0, a1, b1, ...] in place (an out-shuffle)."""
            stack = [(0, len(a) // 2)]               # (1)!
            while stack:
                lo, m = stack.pop()
                if m <= 1:
                    continue
                h = m // 2
                rotate_left(a, lo + h, lo + m + h, m - h)   # (2)!
                stack += [(lo, h), (lo + 2 * h, m - h)]
        ```

        1. קטע הוא \( (lo, m) \) : ‏\( 2m \) איברים מ-\( lo \), ‏\( m \) מכל צד. הקטעים בלתי תלויים, אז הסדר במחסנית לא משנה.
        2. ‏\( A_2 B_1 \to B_1 A_2 \). אחרי זה \( a[lo : lo + 2h] \) הוא \( A_1 B_1 \).

    === "SystemVerilog"
        ```systemverilog title="function interleave" linenums="1" hl_lines="12 13 14 28 29 30"
        function automatic void reverse_range(ref int a[], input int lo, input int hi);
          int t;
          hi--;
          while (lo < hi) begin
            t = a[lo]; a[lo] = a[hi]; a[hi] = t;
            lo++; hi--;
          end
        endfunction

        // rotate a[lo .. hi-1] left by k places (0 <= k <= hi - lo), by three reversals
        function automatic void rotate_left(ref int a[], input int lo, input int hi, input int k);
          reverse_range(a, lo, lo + k);
          reverse_range(a, lo + k, hi);
          reverse_range(a, lo, hi);
        endfunction

        // [a0..a(m-1), b0..b(m-1)] -> [a0, b0, a1, b1, ...] in place (an out-shuffle)
        function automatic void interleave(ref int a[]);
          int lo_q[$], m_q[$];
          int lo, m, h;
          lo_q.push_back(0);
          m_q.push_back(a.size() / 2);
          while (lo_q.size() > 0) begin
            lo = lo_q.pop_back();
            m = m_q.pop_back();
            if (m <= 1) continue;
            h = m / 2;
            rotate_left(a, lo + h, lo + m + h, m - h);
            lo_q.push_back(lo);          m_q.push_back(h);
            lo_q.push_back(lo + 2 * h);  m_q.push_back(m - h);
          end
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **נכונות, באינדוקציה על \( m \).** אחרי הסיבוב, החצי \( a[lo : lo + 2h] \) הוא \( A_1 B_1 \), שהשילוב שלו הוא
    \( a_0 b_0 \dots a_{h-1} b_{h-1} \), והחצי השני הוא \( A_2 B_2 \), שהשילוב שלו ממשיך מ-\( a_h b_h \). שני
    השילובים זה אחר זה הם בדיוק השילוב של כל הקטע.

    **המחיר.** הסיבוב של קטע באורך \( m \) עולה בערך \( m \) החלפות. בכל רמה הקטעים המסובבים זרים, וסכום
    האורכים שלהם הוא לכל היותר \( m \le n/2 \). יש \( \lceil \log_2 m \rceil \) רמות, ולכן \( O(n \log n) \).

    **ב-\( O(n) \) ?** אפשר, עם "מנהיגי מעגלים" : כשמספר האיברים הוא \( 3^k - 1 \), המעגלים של
    \( q \to 2q \bmod (n + 1) \) מתחילים בדיוק ב-\( 1, 3, 9, \dots, 3^{k-1} \), כי 2 הוא שורש פרימיטיבי מודולו
    \( 3^k \) (Jain, 2004). לאורך אחר מסובבים קודם קטע באורך \( 3^k - 1 \) לתחילת המערך, ופותרים את השאר
    באותה דרך. מסובך לראיון, אבל טוב לדעת שקיים.

    **נסו בעצמכם.** בוחרים מספר קלפים וסוג ערבוב, ומערבבים. הקלפים צבועים לפי המעגל של המקום שלהם,
    והמונה מראה מתי החפיסה חוזרת :

    <div class="explorer" data-kind="faro" data-n="8" data-shuffle="out"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לספור מ-1 או מ-0"
    הנוסחה של out-shuffle היא \( 2p \bmod (n - 1) \) כשסופרים מ-0, והנוסחה של in-shuffle היא \( 2q \bmod (n + 1) \)
    כשסופרים מ-1. בבסיס הלא נכון הנוסחה לא מתאימה לאף קלף מחוץ לחצי העליון.

??? trap "מלכודת : המודולו 1"
    ב-out-shuffle של שני קלפים \( M = 1 \), והלולאה "עד ש-\( p = 1 \)" לא נעצרת, כי \( 2 \bmod 1 = 0 \).
    הערבוב לא משנה כלום, והתשובה היא 1.

??? trap "מלכודת : לסמלץ עד שחוזרים"
    סימולציה עולה \( O(n) \) לכל ערבוב, ובחפיסה של 100 קלפים עם in-shuffle צריך 100 ערבובים. הנוסחה עולה
    \( O(M) \) הכפלות של מספרים קטנים, ולא דורשת חפיסה בכלל.

??? followup "שאלות המשך"
    - **הקלף העליון למקום \( p \) :** איך מעבירים את הקלף העליון למקום \( p \) (מ-0) בערבובים מושלמים בלבד?

        ??? fu-answer "תשובה"
            כותבים את \( p \) בבינארית ועוברים מהביט העליון : 1 הוא in-shuffle (‏\( x \to 2x + 1 \)), ו-0 הוא
            out-shuffle (‏\( x \to 2x \)). זה הטריק של Alex Elmsley.

    - **שילוב של \( k \) ערימות :** מחלקים ל-\( k \) ערימות שוות ומשלבים. כמה ערבובים?

        ??? fu-answer "תשובה"
            אותו רעיון : ‏\( p \to kp \bmod (n - 1) \), ולכן הסדר של \( k \) מודולו \( n - 1 \), כש-\( k \) זר ל-\( n - 1 \).

    - **המקום של קלף אחרי \( e \) ערבובים :** בלי לסמלץ?

        ??? fu-answer "תשובה"
            ‏\( 2^e p \bmod M \), עם חזקה מהירה (ריבוע וכפל) : ‏\( O(\log e) \) הכפלות.

    - **‏\( n = 2^j \) בחומרה :** מה זה out-shuffle על הכתובות?

        ??? fu-answer "תשובה"
            סיבוב של ביטי הכתובת שמאלה (perfect shuffle network). ‏\( j \) סיבובים מחזירים כל כתובת למקומה.
