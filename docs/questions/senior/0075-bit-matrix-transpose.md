---
id: 75
title: שחלוף מטריצת ביטים 8×8 במילה של 64 ביט – שלוש החלפות, הכללה ו-RTL
level: senior
difficulty: medium
kind: code
tags: [bitwise, matrices, digital-design, python, systemverilog]
source: "טריק ביטים מוכר (Hacker's Delight, ‏delta swap), עם הכללה ל-32×32 ומודול חומרה"
added: 2026-11-01
---

## השאלה

מילה \( x \) של 64 ביט מחזיקה מטריצת ביטים \( 8 \times 8 \) : **הבית \( r \) הוא השורה \( r \)**, והביט \( c \) שלו
הוא העמודה \( c \). כלומר האיבר \( (r, c) \) הוא הביט \( 8r + c \) של \( x \). כך שמורים, למשל, לוח שחמט
(bitboard), או שמונה ערוצים של 8 ביט שצריך לפרק לפי ביטים.

**השחלוף** שולח את הביט \( 8r + c \) לביט \( 8c + r \).

- **סעיף א – לולאה :** כתבו את השחלוף בלולאה. כמה ביטים לא זזים?
- **סעיף ב – שלוש פעולות :** כתבו אותו בשלוש פעולות של מסכה והזזה בלבד, בלי לולאה, והוכיחו.
- **סעיף ג – הכללה :** איך זה נראה למטריצה \( N \times N \), ‏\( N = 2^L \)? ולמטריצה \( 32 \times 32 \) שהשורות שלה
  הן מערך של 32 מילים של 32 ביט?
- **סעיף ד – RTL :** כתבו מודול חומרה שמשחלף מטריצה \( N \times N \). כמה שערים הוא צריך?

??? interviewer "מה המראיין בודק"
    - **אינדקסים כביטים :** האם המועמד רואה ש-\( 8r + c \) הוא שלושה ביטים של \( r \) ושלושה של \( c \),
      ושהשחלוף מחליף ביניהם.
    - **הפרד ומשול :** האם הוא מגיע לשחלוף בבלוקים, ומבין למה שלושה שלבים מספיקים.
    - **‏delta swap :** האם הוא יודע להחליף הרבה זוגות ביטים בבת אחת עם XOR, מסכה והזזה.
    - **חומרה מול תוכנה :** האם הוא מבין שבחומרה שחלוף קבוע הוא חיווט בלבד, ושהטריק נחוץ רק בתוכנה,
      או כשהנתונים מגיעים בזרם.

---

### סעיף א – לולאה

??? tip "רמז 1"
    לכל \( r \) ו-\( c \), קוראים את הביט \( 8r + c \) וכותבים אותו לביט \( 8c + r \) של מילה חדשה.

??? tip "רמז 2"
    ביט לא זז כש-\( 8r + c = 8c + r \). מתי זה קורה?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        לולאה כפולה על \( r \) ו-\( c \) : אם הביט \( 8r + c \) דולק, מדליקים את \( 8c + r \) במילה חדשה. 64 איטרציות,
        כל אחת כמה פעולות. **8 ביטים** לא זזים, האלכסון \( r = c \).

    <!-- cost: זמן 64 איטרציות | זיכרון מילה אחת -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="transpose8_loop" linenums="1" hl_lines="6 7"
        def transpose8_loop(x: int) -> int:
            """Transpose the 8 x 8 bit matrix in x: bit 8r + c (row r = byte r) goes to bit 8c + r."""
            y = 0
            for r in range(8):
                for c in range(8):
                    if x >> (8 * r + c) & 1:
                        y |= 1 << (8 * c + r)
            return y
        ```

    === "SystemVerilog"
        ```systemverilog title="function transpose8_loop" linenums="1" hl_lines="6"
        // transpose the 8 x 8 bit matrix in x: bit 8r + c (row r = byte r) goes to bit 8c + r
        function automatic logic [63:0] transpose8_loop(logic [63:0] x);
          logic [63:0] y = '0;
          for (int r = 0; r < 8; r++)
            for (int c = 0; c < 8; c++)
              y[8*c + r] = x[8*r + c];
          return y;
        endfunction
        ```

---

### סעיף ב – שלוש פעולות

??? tip "רמז 1"
    שחלוף של מטריצת בלוקים \( \begin{pmatrix} A & B \\ C & D \end{pmatrix} \) הוא \( \begin{pmatrix} A^T & C^T \\ B^T & D^T \end{pmatrix} \).
    מה אפשר לעשות קודם, ומה אחר כך?

??? tip "רמז 2"
    איך מחליפים בפעולה אחת את כל הביטים \( p \) שבמסכה \( M \) עם הביטים \( p + s \)? חשבו על
    \( t = ((x \gg s) \oplus x) \,\&\, M \).

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        שלוש פעולות delta swap, כל אחת מחליפה 16 זוגות של ביטים : ‏**הזזה 7** עם המסכה `0x00AA00AA00AA00AA`
        (משחלפת כל בלוק \( 2 \times 2 \)), ‏**הזזה 14** עם `0x0000CCCC0000CCCC` (מחליפה בלוקים של \( 2 \times 2 \)),
        ו-**הזזה 28** עם `0x00000000F0F0F0F0` (מחליפה בלוקים של \( 4 \times 4 \)). כל אחת היא שש פעולות של
        ביטים, ובסך הכול 18 במקום 64 איטרציות.

    <!-- cost: זמן 18 פעולות | זיכרון מילה אחת -->

    #### הרעיון { .sol-idea }

    **האינדקס הוא שישה ביטים.** ‏\( 8r + c \) הוא \( r_2 r_1 r_0 \, c_2 c_1 c_0 \) בבינארית, והשחלוף מחליף את שלושת
    הביטים של \( r \) עם שלושת הביטים של \( c \). כל שלב מחליף **זוג אחד** : ‏\( r_i \) עם \( c_i \). השלב מזיז את
    האיבר עם \( r_i = 0 \), ‏\( c_i = 1 \) אל האיבר עם \( r_i = 1 \), ‏\( c_i = 0 \), ושאר הביטים של האינדקס לא משתנים.
    המרחק ביניהם הוא \( 8 \cdot 2^i - 2^i = 7 \cdot 2^i \) : ‏7, ‏14 ו-28.

    **‏delta swap.** ‏\( t = ((x \gg s) \oplus x) \,\&\, M \) מסמן בכל ביט \( p \) של \( M \) אם הביטים \( p \) ו-\( p + s \) שונים.
    ‏\( x \oplus t \oplus (t \ll s) \) הופך בדיוק את הזוגות השונים, וזו החלפה. על המטריצה, בכל תא שם האיבר שבו :

    <!-- gen 0 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="המטריצה לפני, ואחרי השלב הראשון (הזזה 7) : בכל תא שם האיבר שבו, שורה ואז עמודה, והאיברים שזזו ממוסגרים"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td></td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr><tr><th dir="rtl">בית 0</th><td class="pm-c c3">00</td><td class="pm-c">01</td><td class="pm-c">02</td><td class="pm-c">03</td><td class="pm-c">04</td><td class="pm-c">05</td><td class="pm-c">06</td><td class="pm-c">07</td><td class="pm-c is-gap"></td><td class="pm-c c3">00</td><td class="pm-c c1 is-hl">10</td><td class="pm-c">02</td><td class="pm-c c1 is-hl">12</td><td class="pm-c">04</td><td class="pm-c c1 is-hl">14</td><td class="pm-c">06</td><td class="pm-c c1 is-hl">16</td></tr><tr><th dir="rtl">בית 1</th><td class="pm-c">10</td><td class="pm-c c3">11</td><td class="pm-c">12</td><td class="pm-c">13</td><td class="pm-c">14</td><td class="pm-c">15</td><td class="pm-c">16</td><td class="pm-c">17</td><td class="pm-c is-gap"></td><td class="pm-c c1 is-hl">01</td><td class="pm-c c3">11</td><td class="pm-c c1 is-hl">03</td><td class="pm-c">13</td><td class="pm-c c1 is-hl">05</td><td class="pm-c">15</td><td class="pm-c c1 is-hl">07</td><td class="pm-c">17</td></tr><tr><th dir="rtl">בית 2</th><td class="pm-c">20</td><td class="pm-c">21</td><td class="pm-c c3">22</td><td class="pm-c">23</td><td class="pm-c">24</td><td class="pm-c">25</td><td class="pm-c">26</td><td class="pm-c">27</td><td class="pm-c is-gap"></td><td class="pm-c">20</td><td class="pm-c c1 is-hl">30</td><td class="pm-c c3">22</td><td class="pm-c c1 is-hl">32</td><td class="pm-c">24</td><td class="pm-c c1 is-hl">34</td><td class="pm-c">26</td><td class="pm-c c1 is-hl">36</td></tr><tr><th dir="rtl">בית 3</th><td class="pm-c">30</td><td class="pm-c">31</td><td class="pm-c">32</td><td class="pm-c c3">33</td><td class="pm-c">34</td><td class="pm-c">35</td><td class="pm-c">36</td><td class="pm-c">37</td><td class="pm-c is-gap"></td><td class="pm-c c1 is-hl">21</td><td class="pm-c">31</td><td class="pm-c c1 is-hl">23</td><td class="pm-c c3">33</td><td class="pm-c c1 is-hl">25</td><td class="pm-c">35</td><td class="pm-c c1 is-hl">27</td><td class="pm-c">37</td></tr><tr><th dir="rtl">בית 4</th><td class="pm-c">40</td><td class="pm-c">41</td><td class="pm-c">42</td><td class="pm-c">43</td><td class="pm-c c3">44</td><td class="pm-c">45</td><td class="pm-c">46</td><td class="pm-c">47</td><td class="pm-c is-gap"></td><td class="pm-c">40</td><td class="pm-c c1 is-hl">50</td><td class="pm-c">42</td><td class="pm-c c1 is-hl">52</td><td class="pm-c c3">44</td><td class="pm-c c1 is-hl">54</td><td class="pm-c">46</td><td class="pm-c c1 is-hl">56</td></tr><tr><th dir="rtl">בית 5</th><td class="pm-c">50</td><td class="pm-c">51</td><td class="pm-c">52</td><td class="pm-c">53</td><td class="pm-c">54</td><td class="pm-c c3">55</td><td class="pm-c">56</td><td class="pm-c">57</td><td class="pm-c is-gap"></td><td class="pm-c c1 is-hl">41</td><td class="pm-c">51</td><td class="pm-c c1 is-hl">43</td><td class="pm-c">53</td><td class="pm-c c1 is-hl">45</td><td class="pm-c c3">55</td><td class="pm-c c1 is-hl">47</td><td class="pm-c">57</td></tr><tr><th dir="rtl">בית 6</th><td class="pm-c">60</td><td class="pm-c">61</td><td class="pm-c">62</td><td class="pm-c">63</td><td class="pm-c">64</td><td class="pm-c">65</td><td class="pm-c c3">66</td><td class="pm-c">67</td><td class="pm-c is-gap"></td><td class="pm-c">60</td><td class="pm-c c1 is-hl">70</td><td class="pm-c">62</td><td class="pm-c c1 is-hl">72</td><td class="pm-c">64</td><td class="pm-c c1 is-hl">74</td><td class="pm-c c3">66</td><td class="pm-c c1 is-hl">76</td></tr><tr><th dir="rtl">בית 7</th><td class="pm-c">70</td><td class="pm-c">71</td><td class="pm-c">72</td><td class="pm-c">73</td><td class="pm-c">74</td><td class="pm-c">75</td><td class="pm-c">76</td><td class="pm-c c3">77</td><td class="pm-c is-gap"></td><td class="pm-c c1 is-hl">61</td><td class="pm-c">71</td><td class="pm-c c1 is-hl">63</td><td class="pm-c">73</td><td class="pm-c c1 is-hl">65</td><td class="pm-c">75</td><td class="pm-c c1 is-hl">67</td><td class="pm-c c3">77</td></tr></tbody></table></div>

    <!-- /gen -->

    <!-- gen 1 -->

    <div class="pm-scroll" tabindex="0" role="region" aria-label="אחרי השלב השני (הזזה 14), ואחרי השלישי (הזזה 28) : זה השחלוף"><table class="pm-cells" dir="ltr"><tbody><tr class="pm-head"><th></th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td></td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr><tr><th dir="rtl">בית 0</th><td class="pm-c c3">00</td><td class="pm-c">10</td><td class="pm-c">20</td><td class="pm-c">30</td><td class="pm-c">04</td><td class="pm-c">14</td><td class="pm-c">24</td><td class="pm-c">34</td><td class="pm-c is-gap"></td><td class="pm-c c3">00</td><td class="pm-c">10</td><td class="pm-c">20</td><td class="pm-c">30</td><td class="pm-c c1 is-hl">40</td><td class="pm-c c1 is-hl">50</td><td class="pm-c c1 is-hl">60</td><td class="pm-c c1 is-hl">70</td></tr><tr><th dir="rtl">בית 1</th><td class="pm-c">01</td><td class="pm-c c3">11</td><td class="pm-c">21</td><td class="pm-c">31</td><td class="pm-c">05</td><td class="pm-c">15</td><td class="pm-c">25</td><td class="pm-c">35</td><td class="pm-c is-gap"></td><td class="pm-c">01</td><td class="pm-c c3">11</td><td class="pm-c">21</td><td class="pm-c">31</td><td class="pm-c c1 is-hl">41</td><td class="pm-c c1 is-hl">51</td><td class="pm-c c1 is-hl">61</td><td class="pm-c c1 is-hl">71</td></tr><tr><th dir="rtl">בית 2</th><td class="pm-c">02</td><td class="pm-c">12</td><td class="pm-c c3">22</td><td class="pm-c">32</td><td class="pm-c">06</td><td class="pm-c">16</td><td class="pm-c">26</td><td class="pm-c">36</td><td class="pm-c is-gap"></td><td class="pm-c">02</td><td class="pm-c">12</td><td class="pm-c c3">22</td><td class="pm-c">32</td><td class="pm-c c1 is-hl">42</td><td class="pm-c c1 is-hl">52</td><td class="pm-c c1 is-hl">62</td><td class="pm-c c1 is-hl">72</td></tr><tr><th dir="rtl">בית 3</th><td class="pm-c">03</td><td class="pm-c">13</td><td class="pm-c">23</td><td class="pm-c c3">33</td><td class="pm-c">07</td><td class="pm-c">17</td><td class="pm-c">27</td><td class="pm-c">37</td><td class="pm-c is-gap"></td><td class="pm-c">03</td><td class="pm-c">13</td><td class="pm-c">23</td><td class="pm-c c3">33</td><td class="pm-c c1 is-hl">43</td><td class="pm-c c1 is-hl">53</td><td class="pm-c c1 is-hl">63</td><td class="pm-c c1 is-hl">73</td></tr><tr><th dir="rtl">בית 4</th><td class="pm-c">40</td><td class="pm-c">50</td><td class="pm-c">60</td><td class="pm-c">70</td><td class="pm-c c3">44</td><td class="pm-c">54</td><td class="pm-c">64</td><td class="pm-c">74</td><td class="pm-c is-gap"></td><td class="pm-c c1 is-hl">04</td><td class="pm-c c1 is-hl">14</td><td class="pm-c c1 is-hl">24</td><td class="pm-c c1 is-hl">34</td><td class="pm-c c3">44</td><td class="pm-c">54</td><td class="pm-c">64</td><td class="pm-c">74</td></tr><tr><th dir="rtl">בית 5</th><td class="pm-c">41</td><td class="pm-c">51</td><td class="pm-c">61</td><td class="pm-c">71</td><td class="pm-c">45</td><td class="pm-c c3">55</td><td class="pm-c">65</td><td class="pm-c">75</td><td class="pm-c is-gap"></td><td class="pm-c c1 is-hl">05</td><td class="pm-c c1 is-hl">15</td><td class="pm-c c1 is-hl">25</td><td class="pm-c c1 is-hl">35</td><td class="pm-c">45</td><td class="pm-c c3">55</td><td class="pm-c">65</td><td class="pm-c">75</td></tr><tr><th dir="rtl">בית 6</th><td class="pm-c">42</td><td class="pm-c">52</td><td class="pm-c">62</td><td class="pm-c">72</td><td class="pm-c">46</td><td class="pm-c">56</td><td class="pm-c c3">66</td><td class="pm-c">76</td><td class="pm-c is-gap"></td><td class="pm-c c1 is-hl">06</td><td class="pm-c c1 is-hl">16</td><td class="pm-c c1 is-hl">26</td><td class="pm-c c1 is-hl">36</td><td class="pm-c">46</td><td class="pm-c">56</td><td class="pm-c c3">66</td><td class="pm-c">76</td></tr><tr><th dir="rtl">בית 7</th><td class="pm-c">43</td><td class="pm-c">53</td><td class="pm-c">63</td><td class="pm-c">73</td><td class="pm-c">47</td><td class="pm-c">57</td><td class="pm-c">67</td><td class="pm-c c3">77</td><td class="pm-c is-gap"></td><td class="pm-c c1 is-hl">07</td><td class="pm-c c1 is-hl">17</td><td class="pm-c c1 is-hl">27</td><td class="pm-c c1 is-hl">37</td><td class="pm-c">47</td><td class="pm-c">57</td><td class="pm-c">67</td><td class="pm-c c3">77</td></tr></tbody></table></div>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **השלב הראשון :** בתוך כל בלוק \( 2 \times 2 \), מחליפים את הפינה הימנית העליונה עם השמאלית התחתונה.
    2. **השלב השני :** בתוך כל בלוק \( 4 \times 4 \), מחליפים את בלוק ה-\( 2 \times 2 \) הימני העליון עם השמאלי התחתון.
    3. **השלב השלישי :** מחליפים את בלוק ה-\( 4 \times 4 \) הימני העליון עם השמאלי התחתון.

    </div>

    <!-- gen 2 -->

    | השלב | מה מחליפים | ההזזה | המסכה | זוגות |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏1 | בתוך כל בלוק 2×2 | ‏7 | ‏`0x00AA00AA00AA00AA` | ‏16 |
    | ‏2 | בלוקים 2×2 בתוך כל 4×4 | ‏14 | ‏`0x0000CCCC0000CCCC` | ‏16 |
    | ‏3 | בלוקים 4×4 | ‏28 | ‏`0x00000000F0F0F0F0` | ‏16 |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="delta_swap, transpose8" linenums="1" hl_lines="3 4 8 9 10"
        def delta_swap(x: int, mask: int, s: int) -> int:
            """Swap every bit p of mask with bit p + s."""
            t = ((x >> s) ^ x) & mask              # (1)!
            return x ^ t ^ (t << s)


        def transpose8(x: int) -> int:
            x = delta_swap(x, 0x00AA00AA00AA00AA, 7)    # inside each 2 x 2 block
            x = delta_swap(x, 0x0000CCCC0000CCCC, 14)   # 2 x 2 blocks inside each 4 x 4
            x = delta_swap(x, 0x00000000F0F0F0F0, 28)   # the 4 x 4 blocks
            return x
        ```

        1. ביט \( p \) של \( t \) דולק כש-\( p \) במסכה והביטים \( p \) ו-\( p + s \) שונים. רק אז צריך להחליף.

    === "SystemVerilog"
        ```systemverilog title="function delta_swap, transpose8" linenums="1" hl_lines="4 5 10 11 12"
        // swap every bit p of mask with bit p + s
        function automatic logic [63:0] delta_swap(logic [63:0] x, logic [63:0] mask, int s);
          logic [63:0] t;
          t = ((x >> s) ^ x) & mask;
          return x ^ t ^ (t << s);
        endfunction

        function automatic logic [63:0] transpose8(logic [63:0] x);
          logic [63:0] y;
          y = delta_swap(x, 64'h00AA00AA00AA00AA, 7);    // inside each 2 x 2 block
          y = delta_swap(y, 64'h0000CCCC0000CCCC, 14);   // 2 x 2 blocks inside each 4 x 4
          y = delta_swap(y, 64'h00000000F0F0F0F0, 28);   // the 4 x 4 blocks
          return y;
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **ה-delta swap מחליף.** נסתכל על זוג \( p \in M \), ‏\( q = p + s \), ונסמן \( t_p = x_p \oplus x_q \). ‏\( t \) דולק רק
    בביטים של \( M \), ו-\( t \ll s \) רק בביטים \( M + s \), ושתי הקבוצות זרות : ביט במסכה הוא תמיד "הנמוך" בזוג
    (‏\( r_i = 0 \), ‏\( c_i = 1 \)) ואף פעם לא ה"גבוה". לכן הביט \( p \) נהיה \( x_p \oplus t_p = x_q \), הביט \( q \) נהיה
    \( x_q \oplus t_p = x_p \), וכל ביט שלא בזוג נשאר.

    **שלושה שלבים.** כל שלב מחליף את \( r_i \) ו-\( c_i \) של כל אינדקס ומשאיר את שאר הביטים. ההחלפות של זוגות
    שונים לא תלויות זו בזו, ולכן אחרי שלושתן \( r \) ו-\( c \) התחלפו לגמרי : ‏\( 8r + c \to 8c + r \). מאותה סיבה
    **הסדר של השלבים לא משנה**.

---

### סעיף ג – הכללה

??? tip "רמז 1"
    ב-\( N \times N \) עם \( N = 2^L \), לאינדקס יש \( L \) ביטים של שורה ו-\( L \) של עמודה. כמה שלבים, ומה
    ההזזה של כל אחד?

??? tip "רמז 2"
    כשכל שורה היא מילה נפרדת, השלב \( j \) מחליף ביטים בין המילה \( r \) למילה \( r + j \). איזה ביטים?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏\( L = \log_2 N \) שלבים. **במילה אחת** של \( N^2 \) ביטים, השלב \( i \) הוא delta swap עם הזזה \( (N - 1) 2^i \) ומסכה
        של הביטים עם \( r_i = 0 \), ‏\( c_i = 1 \). **במערך של \( N \) מילים**, השלב \( j = 2^i \) מחליף בכל זוג מילים
        \( r \), ‏\( r + j \) (עם \( r_j = 0 \)) את הביטים \( c \) עם \( c_j = 1 \) במילה \( r \) עם הביטים \( c - j \) במילה \( r + j \).
        ל-\( 32 \times 32 \) זה \( 5 \cdot 16 = 80 \) פעולות, במקום 1024 ביטים אחד אחד.

    <!-- cost: זמן \( \tfrac{N}{2} \log_2 N \) פעולות | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **אותו רעיון, יותר שלבים.** במילה אחת :

    <!-- gen 3 -->

    | ‏N | ביטים | השלבים, הזזה ומסכה |
    |:-:|:-:|:-:|
    | ‏2 | ‏4 | ‏`1: 0x2` |
    | ‏4 | ‏16 | ‏`3: 0x0A0A · 6: 0x00CC` |
    | ‏8 | ‏64 | ‏`7: 0x00AA00AA00AA00AA · 14: 0x0000CCCC0000CCCC · 28: 0x00000000F0F0F0F0` |

    <!-- /gen -->

    **שורה היא מילה.** כש-\( N = 32 \) המטריצה לא נכנסת במילה, אבל השלב \( j \) מחליף איבר \( (r, c) \) עם
    \( (r + j, c - j) \) : בין שתי מילים. ‏\( t = ((a[r] \gg j) \oplus a[r + j]) \,\&\, M_j \) עם \( M_j \) של הביטים עם
    \( c_j = 0 \), ואז \( a[r + j] \mathrel{\oplus}= t \) ו-\( a[r] \mathrel{\oplus}= t \ll j \) :

    <!-- gen 4 -->

    | ‏j | המסכה | זוגות של מילים |
    |:-:|:-:|:-:|
    | ‏16 | ‏`0x0000FFFF` | ‏16 |
    | ‏8 | ‏`0x00FF00FF` | ‏16 |
    | ‏4 | ‏`0x0F0F0F0F` | ‏16 |
    | ‏2 | ‏`0x33333333` | ‏16 |
    | ‏1 | ‏`0x55555555` | ‏16 |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="transpose32" linenums="1" hl_lines="7 8 9 11"
        def transpose32(a: list) -> None:
            """a[r] holds row r of a 32 x 32 bit matrix (bit c = column c); transpose it in place."""
            j, mask = 16, 0x0000FFFF
            while j:
                for r in range(32):
                    if r & j == 0:                     # (1)!
                        t = ((a[r] >> j) ^ a[r + j]) & mask
                        a[r + j] ^= t
                        a[r] ^= t << j
                j >>= 1
                mask ^= mask << j                      # (2)!
        ```

        1. ‏\( r \) עם הביט \( j \) כבוי, בזוג עם \( r + j \).
        2. ‏`0x0000FFFF` → ‏`0x00FF00FF` → ‏`0x0F0F0F0F` → ‏`0x33333333` → ‏`0x55555555` : הביטים \( c \) עם \( c_j = 0 \).

    === "SystemVerilog"
        ```systemverilog title="function transpose32" linenums="1" hl_lines="7 8 9 11"
        // a[r] holds row r of a 32 x 32 bit matrix (bit c = column c); transpose it in place
        function automatic void transpose32(ref logic [31:0] a[32]);
          logic [31:0] mask = 32'h0000FFFF, t;
          for (int j = 16; j > 0; j >>= 1) begin
            for (int r = 0; r < 32; r++)
              if ((r & j) == 0) begin
                t = ((a[r] >> j) ^ a[r + j]) & mask;
                a[r + j] ^= t;
                a[r] ^= t << j;
              end
            mask ^= mask << (j >> 1);
          end
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **במילה אחת.** האיבר \( (r, c) \) הוא הביט \( N r + c \). מ-\( (r, c) \) עם \( r_i = 0 \), ‏\( c_i = 1 \) ל-\( (r + 2^i, c - 2^i) \)
    המרחק הוא \( N 2^i - 2^i = (N - 1) 2^i \), אותו מרחק לכל הזוגות, ולכן delta swap אחד מבצע את כולם. ‏\( L \)
    שלבים מחליפים את כל \( L \) הזוגות \( r_i \leftrightarrow c_i \), כמו בסעיף ב.

    **במערך.** בשלב \( j \) הביט \( c \) (עם \( c_j = 1 \)) של \( a[r] \) עובר ב-\( a[r] \gg j \) למקום \( c - j \), שבו \( c_j = 0 \) :
    \( t \) הוא ההפרש בין שני האיברים של כל זוג, וה-XOR עם \( t \) בשתי המילים מחליף אותם. כל מילה עם \( r_j = 0 \)
    בזוג אחד, ולכן \( N/2 \) פעולות בכל שלב.

---

### סעיף ד – RTL

??? tip "רמז 1"
    בחומרה, מה זה "להזיז ביט ממקום \( 8r + c \) למקום \( 8c + r \)" כשהמקומות קבועים?

??? tip "רמז 2"
    ‏`assign` בתוך `generate`. ומה משתנה אם השורות מגיעות אחת בכל מחזור?

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        **אפס שערים** : שחלוף קבוע הוא רק חיווט, ‏`assign out[N*c + r] = in[N*r + c]` בתוך `generate`. כל
        הטריקים של סעיפים ב ו-ג נחוצים בתוכנה, שבה יש רק פעולות על מילים שלמות. בחומרה הבעיה האמיתית
        היא כשהמטריצה מגיעה **בזרם**, שורה בכל מחזור : אז צריך לשמור את כל \( N \) השורות לפני שאפשר להוציא
        עמודה, כלומר \( N^2 \) ביטים של זיכרון, ו-latency של \( N \) מחזורים.

    <!-- cost: שערים 0 | חוטים N² -->

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module bit_transpose" linenums="1" hl_lines="8"
        // an N x N bit matrix, row r in bits [N*r +: N], transposed: wires only
        module bit_transpose #(parameter int N = 8) (
          input  logic [N*N-1:0] in,
          output logic [N*N-1:0] out
        );
          for (genvar r = 0; r < N; r++) begin : g_row
            for (genvar c = 0; c < N; c++) begin : g_col
              assign out[N*c + r] = in[N*r + c];   // (1)!
            end
          end
        endmodule
        ```

        1. הסינתזה לא מייצרת כאן אף תא : ‏\( N^2 \) חוטים מוצלבים. ב-\( N = 32 \) זה 1024 חוטים, ובמימוש פיזי
           ההצלבה עצמה (routing) היא המחיר.

    #### למה זה נכון { .sol-proof }

    כל ביט של `out` מחובר לביט אחד בדיוק של `in`, לפי הנוסחה של השחלוף. ה-testbench של השאלה משווה את
    המודול, ב-\( N = 8 \) וב-\( N = 4 \), לפונקציות של סעיפים א ו-ב על אלפי מילים אקראיות.

    **נסו בעצמכם.** לוחצים על ביטים כדי לצייר, ומעבירים את המטריצה בשלושת השלבים : בכל שלב הזוגות
    שמתחלפים מסומנים, והמילה, המסכה וההזזה כתובות מתחת :

    <div class="explorer" data-kind="bitmatrix" data-pattern="F"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : איזה ביט הוא העמודה 0"
    יש שתי מוסכמות : ביט 0 של הבית הוא העמודה השמאלית או הימנית, והבית 0 הוא השורה העליונה או התחתונה.
    השחלוף על האלכסון הראשי במוסכמה אחת הוא שחלוף על האלכסון המשני באחרת, והמסכות משתנות. כותבים
    את המוסכמה לפני המסכות.

??? trap "מלכודת : הזזה של ערך עם סימן"
    ב-C, ‏`>>` על `int64_t` שלילי משכפל את ביט הסימן, והמסכות כבר לא בודדות את מה שצריך. עובדים
    ב-`uint64_t`. ב-Python אין רוחב, אבל המסכה ממילא חותכת.

??? trap "מלכודת : הסדר של הפעולות בתוך delta swap"
    ‏`x ^= t; x ^= t << s` נכון, אבל `x ^= t << s` לפני חישוב \( t \) מ-\( x \) המקורי לא. \( t \) נלקח מ-\( x \) לפני
    כל שינוי.

??? followup "שאלות המשך"
    - **סיבוב ב-90° :** איך מסובבים את המטריצה ב-90° בכיוון השעון באותה מילה?

        ??? fu-answer "תשובה"
            שחלוף ואז היפוך של כל שורה, כלומר היפוך הביטים בתוך כל בית. או היפוך סדר הבתים (byte swap) ואז
            שחלוף, כמו בשאלה 0074.

    - **שיקוף :** איך משקפים את המטריצה אנכית ואופקית?

        ??? fu-answer "תשובה"
            אנכי : היפוך סדר הבתים, ‏`bswap`. אופקי : היפוך הביטים בתוך כל בית, בשלושה delta swaps עם הזזות 1, 2 ו-4.

    - **בזרם :** שורה של 8 ביטים נכנסת בכל מחזור, ורוצים להוציא עמודה בכל מחזור. כמה זיכרון, ומה ה-latency?

        ??? fu-answer "תשובה"
            ‏64 ביטים של רגיסטרים ו-8 מחזורים, או שני בנקים (ping-pong) כדי לקבל מטריצה חדשה בכל 8 מחזורים
            בלי הפסקה.

    - **מטריצה מלבנית :** ‏\( 8 \times 4 \) בתוך 32 ביט?

        ??? fu-answer "תשובה"
            שחלוף לא ריבועי של ביטים הוא תמורה עם מעגלים, כמו בשאלה 0074. אפשר לרפד לריבוע \( 8 \times 8 \),
            לשחלף ולדחוס, או לתאר את התמורה כרשת של delta swaps (רשת Beneš).
