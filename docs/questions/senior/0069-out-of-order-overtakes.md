---
id: 69
title: עקיפות בזרם תשובות – כמה עקפו כל בקשה, כמה היא עקפה, וסך העקיפות
level: senior
difficulty: hard
kind: code
tags: [algorithms, sorting, protocols, python, systemverilog]
source: "סעיף א הוא Count of Smaller Numbers After Self (Google, Amazon), והסעיפים הבאים הם ההכללה שלו לזרם תשובות שלא לפי הסדר"
added: 2026-10-29
---

## השאלה

סביבת אימות שולחת \( n \) בקשות ל-DUT, בזו אחר זו, במספרים \( 0, 1, \dots, n - 1 \). ה-DUT
רשאי לענות שלא לפי הסדר (כמו completions ב-PCIe או תשובות ל-IDs שונים ב-AXI). המערך
`done` רושם לכל בקשה את הזמן שבו הגיעה התשובה שלה : ‏`done[i]` הוא זמן התשובה של
בקשה \( i \). בקשה \( j \) **עקפה** את בקשה \( i \) אם נשלחה אחריה (\( j > i \)) ונענתה
לפניה (\( \text{done}[j] < \text{done}[i] \)). שתי תשובות באותו זמן אינן עקיפה.

דוגמה : ‏`done = [5, 2, 6, 1]`. בקשה 3 נענתה ראשונה, ולכן עקפה את 0, את 1 ואת 2. בקשה 1
עקפה את 0. בסך הכול ארבע עקיפות.

**ההקשר באימות :** scoreboard של ממשק שעונה שלא לפי הסדר צריך לדעת לא רק *אם* התשובות
נכונות, אלא *כמה* ערבוב היה : בקשה שהרבה בקשות צעירות ממנה עקפו אותה היא בקשה
מורעבת (starvation), העקיפה הגדולה ביותר היא העומק שמאגר הסידור מחדש (reorder buffer)
חייב להחזיק, וסך העקיפות הוא מדד כיסוי : טסט שאף פעם לא ערבב תשובות לא בדק את
ה-scoreboard של שאלה [0050](0050-out-of-order-scoreboard.md). את שלושת המספרים האלה
מחשבים כאן מהטרייס, ובסוף גם תוך כדי הריצה.

- **סעיף א – כמה עקפו כל בקשה :** כתבו פונקציה שמחזירה לכל בקשה כמה בקשות מאוחרות
  ממנה נענו לפניה, \( \text{passed}[i] = |\{\, j > i : \text{done}[j] < \text{done}[i] \,\}| \),
  בזמן \( O(n \log n) \). בדוגמה : ‏<span dir="ltr">[2, 1, 1, 0]</span>.
- **סעיף ב – כמה כל בקשה עקפה :** ההיפך : לכל בקשה, כמה בקשות מוקדמות ממנה נענו אחריה,
  \( \text{overtook}[i] = |\{\, j < i : \text{done}[j] > \text{done}[i] \,\}| \). מה המשמעות
  של שני המערכים באימות, ומה הקשר בין הסכומים שלהם?
- **סעיף ג – סך העקיפות, ובזמן אמת :** כמה עקיפות היו בסך הכול, מה המספר אומר על הטסט,
  ואיך מדווחים על עקיפות **תוך כדי** הריצה, כשכל תשובה מגיעה, בלי לחכות לסוף?

??? interviewer "מה המראיין בודק"
    - **מזוגות לספירה :** האם המועמד רואה שהשאלה היא ספירת זוגות הפוכים, מתחיל מ-\( O(n^2) \)
      ויודע לאן לשפר. "כמה מהערכים שכבר ראיתי קטנים מהנוכחי" היא השאלה שחוזרת בכל סעיף.
    - **מבנה נתונים לספירת קידומת :** עץ Fenwick (או מיון-מיזוג). האם הוא מסביר *מה* כל תא
      שומר, ולא רק מצטט את שתי הלולאות.
    - **הפרטים הקטנים :** דחיסת ערכים לדרגות, אינדקסים מ-1, הטיפול בזמנים שווים, וסדר
      השאילתה והעדכון.
    - **ההכללה :** אותו עץ בכיוון ההפוך נותן את סעיף ב, ואותו עץ על אינדקסי השליחה נותן
      scoreboard שמדווח בזמן אמת. האם המועמד רואה שזה אותו כלי.
    - **המשמעות באימות :** הרעבה, עומק סידור מחדש, וכיסוי של ערבוב. מספר בלי משמעות הוא לא
      תוצאה.

---

### סעיף א – כמה בקשות עקפו כל בקשה

??? tip "רמז 1"
    הפתרון הישיר הוא שתי לולאות, \( O(n^2) \) : לכל \( i \), לספור את ה-\( j > i \) עם זמן קטן
    יותר. איזו ספירה חוזרת בכל צעד? "כמה מהזמנים שכבר ראיתי קטנים מהזמן הזה". אם הולכים
    מהסוף להתחלה, מה כבר "ראיתם" כשמגיעים ל-\( i \)?

??? tip "רמז 2"
    צריך מבנה שתומך בשתי פעולות ב-\( O(\log n) \) : "הוסף את הערך \( v \)" ו"כמה ערכים קטנים
    מ-\( v \) הוספו עד עכשיו". מערך של מונים לפי ערך עושה את הראשונה ב-\( O(1) \) ואת השנייה
    ב-\( O(n) \), ומערך של סכומי קידומת להיפך. מה באמצע?

??? tip "רמז 3"
    הזמנים יכולים להיות גדולים, אבל יש רק \( n \) מהם : החליפו כל זמן ב**דרגה** שלו, 1 לקטן
    ביותר, 2 לבא אחריו, וכן הלאה. ועל הדרגות : מערך שבו תא שומר סכום של **בלוק** של תאים,
    באורך שהוא חזקה של 2, כך שכל קידומת היא \( O(\log n) \) בלוקים (עץ Fenwick).

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ממירים כל זמן לדרגה שלו (1 לקטן ביותר). הולכים מהבקשה האחרונה לראשונה עם עץ
        Fenwick על הדרגות : לכל בקשה שואלים כמה דרגות **קטנות** מהדרגה שלה כבר בעץ (אלה
        בקשות מאוחרות שנענו לפניה), וזה \( \text{passed}[i] \), ואז מכניסים את הדרגה שלה.
        שאילתה ועדכון עולים \( O(\log n) \) כל אחד, ולכן \( O(n \log n) \) בסך הכול. בדוגמה :
        ‏<span dir="ltr">[2, 1, 1, 0]</span>. פתרון שני, באותו זמן : מיון-מיזוג שסופר תוך כדי
        המיזוג.

    <!-- cost: זמן \( O(n \log n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **מה סופרים.** נצייר את הבקשות בשורה העליונה לפי סדר השליחה ואת התשובות בשורה התחתונה
    לפי סדר ההגעה, וקו מכל בקשה לתשובה שלה. שני קווים חוצים זה את זה בדיוק כששתי
    הבקשות החליפו סדר, כלומר כשהמאוחרת עקפה את המוקדמת. ‏\( \text{passed}[i] \) הוא מספר
    הקווים של בקשות **מימין** ל-\( i \) (מאוחרות) שחוצים את הקו של \( i \) :

    <!-- gen 0 -->

    <svg class="figure ov-fig" viewBox="0 0 232 190" style="max-width:14.5rem" role="img" aria-label="הבקשות 0 עד 3 עם זמני התשובה 5 2 6 1, התשובות לפי סדר ההגעה, הקווים ביניהן, ו-passed של כל בקשה"><text class="tick" x="56" y="12" text-anchor="end">i</text><text class="ov-lab" x="56" y="39" text-anchor="end">done</text><text class="ov-lab" x="56" y="111" text-anchor="end">arrive</text><text class="tick" x="56" y="138" text-anchor="end">time</text><text class="ov-lab" x="56" y="171" text-anchor="end">passed</text><text class="tick" x="84" y="12" text-anchor="middle">0</text><text class="tick" x="124" y="12" text-anchor="middle">1</text><text class="tick" x="164" y="12" text-anchor="middle">2</text><text class="tick" x="204" y="12" text-anchor="middle">3</text><line class="ov-line is-cross" x1="84" y1="48" x2="164" y2="94"><title>request 0: sent in slot 0, answered at 5, slot 2 of the answers; its line is crossed 2 times: passed 2 + overtook 0</title></line><line class="ov-line is-cross" x1="124" y1="48" x2="124" y2="94"><title>request 1: sent in slot 1, answered at 2, slot 1 of the answers; its line is crossed 2 times: passed 1 + overtook 1</title></line><line class="ov-line is-cross" x1="164" y1="48" x2="204" y2="94"><title>request 2: sent in slot 2, answered at 6, slot 3 of the answers; its line is crossed 1 times: passed 1 + overtook 0</title></line><line class="ov-line is-cross" x1="204" y1="48" x2="84" y2="94"><title>request 3: sent in slot 3, answered at 1, slot 0 of the answers; its line is crossed 3 times: passed 0 + overtook 3</title></line><g class="ov-cell is-req"><title>request 0, answered at time 5</title><rect x="68" y="20" width="32" height="28" rx="4"/><text x="84" y="39" text-anchor="middle">5</text></g><g class="ov-cell is-req"><title>request 1, answered at time 2</title><rect x="108" y="20" width="32" height="28" rx="4"/><text x="124" y="39" text-anchor="middle">2</text></g><g class="ov-cell is-req"><title>request 2, answered at time 6</title><rect x="148" y="20" width="32" height="28" rx="4"/><text x="164" y="39" text-anchor="middle">6</text></g><g class="ov-cell is-req"><title>request 3, answered at time 1</title><rect x="188" y="20" width="32" height="28" rx="4"/><text x="204" y="39" text-anchor="middle">1</text></g><g class="ov-cell is-rsp"><title>answer slot 0: request 3, time 1</title><rect x="68" y="94" width="32" height="28" rx="4"/><text x="84" y="113" text-anchor="middle">3</text></g><text class="tick" x="84" y="138" text-anchor="middle">1</text><g class="ov-cell is-rsp"><title>answer slot 1: request 1, time 2</title><rect x="108" y="94" width="32" height="28" rx="4"/><text x="124" y="113" text-anchor="middle">1</text></g><text class="tick" x="124" y="138" text-anchor="middle">2</text><g class="ov-cell is-rsp"><title>answer slot 2: request 0, time 5</title><rect x="148" y="94" width="32" height="28" rx="4"/><text x="164" y="113" text-anchor="middle">0</text></g><text class="tick" x="164" y="138" text-anchor="middle">5</text><g class="ov-cell is-rsp"><title>answer slot 3: request 2, time 6</title><rect x="188" y="94" width="32" height="28" rx="4"/><text x="204" y="113" text-anchor="middle">2</text></g><text class="tick" x="204" y="138" text-anchor="middle">6</text><g class="ov-cnt"><title>passed[0] = 2</title><rect x="68" y="152" width="32" height="28" rx="4"/><text x="84" y="171" text-anchor="middle">2</text></g><g class="ov-cnt"><title>passed[1] = 1</title><rect x="108" y="152" width="32" height="28" rx="4"/><text x="124" y="171" text-anchor="middle">1</text></g><g class="ov-cnt"><title>passed[2] = 1</title><rect x="148" y="152" width="32" height="28" rx="4"/><text x="164" y="171" text-anchor="middle">1</text></g><g class="ov-cnt is-zero"><title>passed[3] = 0</title><rect x="188" y="152" width="32" height="28" rx="4"/><text x="204" y="171" text-anchor="middle">0</text></g></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="ov-key-req"></i>בקשה, לפי סדר השליחה, עם זמן התשובה</span><span><i class="ov-key-rsp"></i>תשובה, לפי סדר ההגעה, עם מספר הבקשה</span><span><i class="ov-key-cross"></i>קו שחוצה קו אחר : עקיפה</span><span><i class="ov-key-cnt"></i>הספירה של הבקשה</span></span>

    <!-- /gen -->

    **הלולאה הכפולה.** לכל \( i \) עוברים על כל \( j > i \) ובודקים \( \text{done}[j] < \text{done}[i] \).
    זה נכון, קל, ו-\( O(n^2) \) : על טרייס של מיליון תשובות זה חצי טריליון השוואות. בראיון
    אומרים את זה במשפט אחד, ועוברים לשפר.

    **מה חוזר על עצמו.** אם הולכים מהבקשה האחרונה לראשונה, אז כשמגיעים ל-\( i \) כבר
    "ראינו" בדיוק את הבקשות המאוחרות ממנה. השאלה בכל צעד היא אחת : **כמה מהזמנים שכבר
    ראינו קטנים מ-\( \text{done}[i] \)?** ואחרי התשובה מוסיפים את \( \text{done}[i] \) לנראים.
    צריך מבנה שעונה על "כמה קטנים מ-\( v \)" ומקבל "הוסף את \( v \)", שניהם מהר.

    **דחיסה לדרגות.** הזמנים יכולים להיות מספרים גדולים (מחזורי שעון, ננו-שניות), אבל יש
    רק \( n \) מהם. ממיינים את הערכים השונים ונותנים לכל ערך את ה**דרגה** שלו : 1 לקטן
    ביותר, 2 לבא אחריו, וכן הלאה עד \( m \le n \). "קטן מ-\( v \)" הופך ל"דרגה קטנה
    מדרגת \( v \)", ועכשיו המבנה צריך לכסות רק את \( 1 \dots m \). ערכים שווים מקבלים אותה דרגה,
    ולכן אינם נספרים זה כנגד זה : בדיוק ההסכמה ש"אותו זמן אינו עקיפה". בדוגמה הערכים
    <span dir="ltr">5 2 6 1</span> ממוינים הם <span dir="ltr">1 2 5 6</span>, ולכן הדרגות הן
    <span dir="ltr">3 2 4 1</span>.

    **מערך מונים, ולמה הוא לא מספיק.** מערך `cnt[1..m]` שבו `cnt[r]` סופר כמה פעמים נראתה
    הדרגה \( r \) : ההוספה היא \( O(1) \), אבל "כמה קטנים מ-\( r \)" הוא הסכום
    \( \text{cnt}[1] + \dots + \text{cnt}[r - 1] \), ‏\( O(n) \). מערך של סכומי קידומת הופך את
    זה : השאילתה \( O(1) \), אבל כל הוספה מעדכנת את כל הסכומים אחריה, \( O(n) \). צריך משהו
    באמצע.

    **עץ Fenwick (Binary Indexed Tree).** מערך `tree[1..m]` שבו התא \( i \) **לא** שומר ערך אחד
    אלא את הסכום של **הבלוק** של התאים שנגמר ב-\( i \), באורך \( \text{lowbit}(i) \) :
    הערך של הביט הדולק הנמוך ביותר של \( i \). כך `tree[6]` (‏\( 6 = 110_2 \), הביט הנמוך
    שווה 2) שומר את הסכום של התאים 5 ו-6, ו-`tree[8]` (‏\( 1000_2 \)) את הסכום של 1 עד 8.
    האיור מראה את הבלוקים ל-\( m = 8 \) : מעל כל תא הטווח שהוא מכסה, ומתחתיו \( i \)
    בבינארי. אורך הבלוק הוא תמיד הביט הנמוך, ובלוקים באותה שכבה אינם חופפים :

    <!-- gen 2 -->

    <svg class="figure ov-fig ov-fw" viewBox="0 0 392 142" style="max-width:24.5rem" role="img" aria-label="מערך Fenwick של 8 תאים : מעל כל תא הטווח שהוא מכסה, ומתחתיו האינדקס בבינארי"><text class="ov-lab" x="56" y="91" text-anchor="end">tree[i]</text><text class="tick" x="56" y="116" text-anchor="end">i</text><text class="tick" x="56" y="129" text-anchor="end">binary</text><g class="ov-bar"><title>tree[1] covers 1..1: 1 cell, the lowest set bit of 1</title><rect x="67" y="54" width="34" height="14" rx="3"/><text x="84" y="65" text-anchor="middle">1</text></g><g class="ov-tc"><title>tree[1]</title><rect x="68" y="72" width="32" height="28" rx="4"/><text x="84" y="91" text-anchor="middle"></text></g><text class="tick" x="84" y="116" text-anchor="middle">1</text><text class="ov-bin" x="84" y="129" text-anchor="middle">0001</text><g class="ov-bar"><title>tree[2] covers 1..2: 2 cells, the lowest set bit of 2</title><rect x="67" y="38" width="74" height="14" rx="3"/><text x="104" y="49" text-anchor="middle">1..2</text></g><g class="ov-tc"><title>tree[2]</title><rect x="108" y="72" width="32" height="28" rx="4"/><text x="124" y="91" text-anchor="middle"></text></g><text class="tick" x="124" y="116" text-anchor="middle">2</text><text class="ov-bin" x="124" y="129" text-anchor="middle">0010</text><g class="ov-bar"><title>tree[3] covers 3..3: 1 cell, the lowest set bit of 3</title><rect x="147" y="54" width="34" height="14" rx="3"/><text x="164" y="65" text-anchor="middle">3</text></g><g class="ov-tc"><title>tree[3]</title><rect x="148" y="72" width="32" height="28" rx="4"/><text x="164" y="91" text-anchor="middle"></text></g><text class="tick" x="164" y="116" text-anchor="middle">3</text><text class="ov-bin" x="164" y="129" text-anchor="middle">0011</text><g class="ov-bar"><title>tree[4] covers 1..4: 4 cells, the lowest set bit of 4</title><rect x="67" y="22" width="154" height="14" rx="3"/><text x="144" y="33" text-anchor="middle">1..4</text></g><g class="ov-tc"><title>tree[4]</title><rect x="188" y="72" width="32" height="28" rx="4"/><text x="204" y="91" text-anchor="middle"></text></g><text class="tick" x="204" y="116" text-anchor="middle">4</text><text class="ov-bin" x="204" y="129" text-anchor="middle">0100</text><g class="ov-bar"><title>tree[5] covers 5..5: 1 cell, the lowest set bit of 5</title><rect x="227" y="54" width="34" height="14" rx="3"/><text x="244" y="65" text-anchor="middle">5</text></g><g class="ov-tc"><title>tree[5]</title><rect x="228" y="72" width="32" height="28" rx="4"/><text x="244" y="91" text-anchor="middle"></text></g><text class="tick" x="244" y="116" text-anchor="middle">5</text><text class="ov-bin" x="244" y="129" text-anchor="middle">0101</text><g class="ov-bar"><title>tree[6] covers 5..6: 2 cells, the lowest set bit of 6</title><rect x="227" y="38" width="74" height="14" rx="3"/><text x="264" y="49" text-anchor="middle">5..6</text></g><g class="ov-tc"><title>tree[6]</title><rect x="268" y="72" width="32" height="28" rx="4"/><text x="284" y="91" text-anchor="middle"></text></g><text class="tick" x="284" y="116" text-anchor="middle">6</text><text class="ov-bin" x="284" y="129" text-anchor="middle">0110</text><g class="ov-bar"><title>tree[7] covers 7..7: 1 cell, the lowest set bit of 7</title><rect x="307" y="54" width="34" height="14" rx="3"/><text x="324" y="65" text-anchor="middle">7</text></g><g class="ov-tc"><title>tree[7]</title><rect x="308" y="72" width="32" height="28" rx="4"/><text x="324" y="91" text-anchor="middle"></text></g><text class="tick" x="324" y="116" text-anchor="middle">7</text><text class="ov-bin" x="324" y="129" text-anchor="middle">0111</text><g class="ov-bar"><title>tree[8] covers 1..8: 8 cells, the lowest set bit of 8</title><rect x="67" y="6" width="314" height="14" rx="3"/><text x="224" y="17" text-anchor="middle">1..8</text></g><g class="ov-tc"><title>tree[8]</title><rect x="348" y="72" width="32" height="28" rx="4"/><text x="364" y="91" text-anchor="middle"></text></g><text class="tick" x="364" y="116" text-anchor="middle">8</text><text class="ov-bin" x="364" y="129" text-anchor="middle">1000</text></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="ov-key-bar"></i>הטווח שהתא מכסה, באורך הביט הדולק הנמוך של i</span><span><i class="ov-key-q"></i>תאים שהשאילתה קוראת</span><span><i class="ov-key-u"></i>תאים שהעדכון מגדיל</span></span>

    <!-- /gen -->

    **הביט הנמוך ב-\( i \ \&\ {-i} \).** במשלים ל-2, ה-AND של \( i \) עם \( -i \) משאיר בדיוק את
    הביט הדולק הנמוך של \( i \) (ההסבר בשאלה [0060](../junior/0060-next-same-popcount.md)) :
    ‏\( 12 = 1100_2 \), ‏\( -12 = \dots 10100_2 \), ו-\( 12 \ \&\ {-12} = 100_2 = 4 \).

    **שאילתה, `prefix(i)` :** הסכום של התאים \( 1 \dots i \). קוראים את `tree[i]`, שמכסה את
    הבלוק \( (i - \text{lowbit}(i),\ i] \), ואז קופצים לתא שלפני הבלוק, \( i \gets i - \text{lowbit}(i) \),
    שהבלוק שלו נגמר בדיוק שם. הבלוקים שנקראים זרים ומכסים יחד את \( 1 \dots i \). כל קפיצה
    מכבה את הביט הדולק הנמוך של \( i \), ולכן יש לכל היותר כמספר הביטים, \( \lfloor \log_2 m \rfloor + 1 \).
    ‏\( \text{prefix}(7) \) קורא את `tree[7]` (התא 7), ‏`tree[6]` (‏5..6) ו-`tree[4]` (‏1..4).

    **עדכון, `add(i)` :** מוסיפים 1 לכל תא שהבלוק שלו מכיל את \( i \). הראשון הוא `tree[i]`
    עצמו. הבא הוא התא \( i + \text{lowbit}(i) \) : הבלוק שלו מתחיל לפני \( i \) ומסתיים אחריו,
    והוא התא הקרוב ביותר שכזה. לתא \( k \) שבין \( i \) ל-\( i + \text{lowbit}(i) \) יש ביט נמוך
    קטן מ-\( \text{lowbit}(i) \), ולכן הבלוק שלו, \( (k - \text{lowbit}(k),\ k] \), מתחיל מעל \( i \).
    גם כאן כל צעד מעלה את הביט הדולק הנמוך למקום גבוה יותר, ולכן לכל היותר
    \( \lfloor \log_2 m \rfloor + 1 \) צעדים. ‏\( \text{add}(3) \) מגדיל את `tree[3]`, ‏`tree[4]` ו-`tree[8]`.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **דרגות :** ממיינים את הערכים השונים של `done`, ובונים מילון ערך → דרגה (‏1 לקטן ביותר).
    2. **עץ ריק :** ‏`tree` של \( m \) אפסים, באינדקסים \( 1 \dots m \).
    3. **מהסוף להתחלה :** לכל \( i \) מ-\( n - 1 \) עד 0, בסדר הזה, כשהדרגה היא \( r \) :
    4. **שאילתה לפני העדכון :** ‏\( \text{passed}[i] = \text{prefix}(r - 1) \) : כמה דרגות קטנות
       מ-\( r \) כבר בעץ. אלה בדיוק הבקשות המאוחרות עם זמן קטן יותר.
    5. **עדכון :** ‏\( \text{add}(r) \) : מעכשיו בקשה \( i \) נספרת בשאילתות של הבקשות שלפניה.

    </div>

    על הדוגמה <span dir="ltr">5 2 6 1</span>, הדרגות <span dir="ltr">3 2 4 1</span> ו-\( m = 4 \).
    העץ כתוב כמערך <span dir="ltr">[tree[1], tree[2], tree[3], tree[4]]</span> :

    <!-- gen 4 -->

    | הצעד | הבקשה i | הזמן | הדרגה | השאילתה | התאים שנקראו | התוצאה | העדכון | העץ אחרי | ‏passed[i] |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏1 | ‏3 | ‏1 | ‏1 | ‏prefix(0) | אין | ‏0 | ‏<span dir="ltr">tree[1] → tree[2] → tree[4]</span> | ‏<span dir="ltr">[1, 1, 0, 1]</span> | **‏0** |
    | ‏2 | ‏2 | ‏6 | ‏4 | ‏prefix(3) | ‏<span dir="ltr">tree[3] → tree[2]</span> | ‏1 | ‏<span dir="ltr">tree[4]</span> | ‏<span dir="ltr">[1, 1, 0, 2]</span> | **‏1** |
    | ‏3 | ‏1 | ‏2 | ‏2 | ‏prefix(1) | ‏<span dir="ltr">tree[1]</span> | ‏1 | ‏<span dir="ltr">tree[2] → tree[4]</span> | ‏<span dir="ltr">[1, 2, 0, 3]</span> | **‏1** |
    | ‏4 | ‏0 | ‏5 | ‏3 | ‏prefix(2) | ‏<span dir="ltr">tree[2]</span> | ‏2 | ‏<span dir="ltr">tree[3] → tree[4]</span> | ‏<span dir="ltr">[1, 2, 1, 4]</span> | **‏2** |

    <!-- /gen -->

    בצעד 1 העץ ריק, ולכן \( \text{passed}[3] = 0 \), והדרגה 1 נכנסת לשלושת התאים שמכסים
    אותה : 1, 2 ו-4. בצעד 2 הדרגה 4 שואלת \( \text{prefix}(3) \) : ‏`tree[3]` הוא 0 ו-`tree[2]`
    (התאים 1..2) הוא 1, ולכן 1. בצעד האחרון הדרגה 3 שואלת \( \text{prefix}(2) \), וקוראת
    תא **אחד**, ‏`tree[2]`, שכבר מכיל את שתי הדרגות 1 ו-2 : זה החיסכון של העץ.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="class Fenwick, ranks, passed" linenums="1" hl_lines="12 18 33 34"
        class Fenwick:
            """A binary indexed tree over 1..n: add(i) counts one more at i, prefix(i) is the
            count at 1..i. Both walk O(log n) cells, moving by the lowest set bit i & -i."""

            def __init__(self, n: int):
                self.n = n
                self.tree = [0] * (n + 1)          # (1)!

            def add(self, i: int) -> None:
                while i <= self.n:
                    self.tree[i] += 1
                    i += i & -i                    # (2)!

            def prefix(self, i: int) -> int:
                s = 0
                while i > 0:
                    s += self.tree[i]
                    i -= i & -i                    # (3)!
                return s


        def ranks(done: list[int]) -> dict[int, int]:
            """Every value to its rank among the distinct values, 1 for the smallest."""
            return {v: r for r, v in enumerate(sorted(set(done)), start=1)}


        def passed(done: list[int]) -> list[int]:
            """passed[i]: how many later requests were answered before request i."""
            rk = ranks(done)
            ft = Fenwick(len(rk))
            out = [0] * len(done)
            for i in range(len(done) - 1, -1, -1):
                out[i] = ft.prefix(rk[done[i]] - 1)   # (4)!
                ft.add(rk[done[i]])
            return out
        ```

        1. ‏\( n + 1 \) תאים, כדי שהאינדקסים יהיו \( 1 \dots n \). התא 0 לא בשימוש.
        2. הביט הדולק הנמוך של \( i \). ב-Python המספרים אינם מוגבלים ברוחב, ובכל זאת `i & -i` נותן את הביט הנמוך, כי \( -i \) מתנהג כמשלים ל-2 אינסופי.
        3. החיסור מכבה את הביט הנמוך, וקופץ לתא שלפני הבלוק שנקרא.
        4. ‏`rk[done[i]] - 1` : דרגה קטנה ממש, ולכן זמן שווה אינו נספר.

    === "SystemVerilog"
        ```systemverilog title="class Fenwick, function passed" linenums="1" hl_lines="14 21 44 45"
        // a binary indexed tree over 1..n: add(i) counts one more at i, prefix(i) is the count
        // at 1..i; both walk O(log n) cells, moving by the lowest set bit i & -i
        class Fenwick;
          int n;
          int tree[];
          function new(int n);
            this.n = n;
            tree = new[n + 1];                   // (1)!
            foreach (tree[j]) tree[j] = 0;
          endfunction
          function void add(int i);
            while (i <= n) begin
              tree[i]++;
              i += i & -i;                       // (2)!
            end
          endfunction
          function int prefix(int i);
            int s = 0;
            while (i > 0) begin
              s += tree[i];
              i -= i & -i;                       // (3)!
            end
            return s;
          endfunction
        endclass

        // every value to its rank among the distinct values, 1 for the smallest
        function automatic void ranks(input int done[], output int rk[int]);
          int vals[$];
          foreach (done[i]) vals.push_back(done[i]);
          vals.sort();
          vals = vals.unique();
          foreach (vals[r]) rk[vals[r]] = r + 1;
        endfunction

        // passed[i]: how many later requests were answered before request i
        function automatic void passed(input int done[], output int out[]);
          int rk[int];
          Fenwick ft;
          ranks(done, rk);
          ft = new(rk.size());
          out = new[done.size()];
          for (int i = done.size() - 1; i >= 0; i--) begin
            out[i] = ft.prefix(rk[done[i]] - 1);   // (4)!
            ft.add(rk[done[i]]);
          end
        endfunction
        ```

        1. ‏\( n + 1 \) תאים כדי שהאינדקסים יהיו \( 1 \dots n \) : התא 0 לא בשימוש. עם אינדקס 0 הביט הנמוך הוא 0, והלולאות לא היו זזות.
        2. הביט הדולק הנמוך של \( i \). החיבור מעלה אותו, והתא הבא הוא הקרוב ביותר שהבלוק שלו מכיל את \( i \).
        3. החיסור מכבה אותו, וקופץ לתא שלפני הבלוק שנקרא.
        4. ‏`rk[done[i]] - 1` הוא "דרגה קטנה ממש", ולכן זמן שווה אינו נספר.

    **פתרון שני : מיון-מיזוג שסופר.** ממיינים את **האינדקסים** לפי הזמן שלהם במיון-מיזוג.
    במיזוג של שני חצאים ממוינים, כשמניחים אינדקס \( i \) מהחצי השמאלי, כל אינדקס מהחצי הימני
    שכבר הונח הוא בקשה מאוחרת יותר (הימני כולו אחרי השמאלי) עם זמן קטן יותר, כלומר
    עקיפה של \( i \) : מוסיפים את מספרם ל-\( \text{passed}[i] \). כל זוג נפגש במיזוג אחד
    בדיוק, ברמה שבה שני האינדקסים נפרדו לחצאים שונים, ולכן כל עקיפה נספרת פעם אחת. ערך
    שווה בחצי הימני לא נלקח לפני השמאלי (`<` ממש), ולכן אינו נספר :

    === "Python"
        ```python title="passed_merge" linenums="1" hl_lines="13 14"
        def passed_merge(done: list[int]) -> list[int]:
            """The same by merge sort: the indices sorted by their time; when an index of the
            left half is placed, every right-half index already placed was answered before it."""
            out = [0] * len(done)

            def sort(idx: list[int]) -> list[int]:
                if len(idx) <= 1:
                    return idx
                mid = len(idx) // 2
                left, right = sort(idx[:mid]), sort(idx[mid:])
                merged, j = [], 0
                for i in left:
                    while j < len(right) and done[right[j]] < done[i]:
                        merged.append(right[j])
                        j += 1
                    out[i] += j                    # (1)!
                    merged.append(i)
                merged.extend(right[j:])
                return merged

            sort(list(range(len(done))))
            return out
        ```

        1. ‏`j` אינדקסים מהחצי הימני כבר הונחו לפני \( i \) : כולם מאוחרים ממנו ונענו לפניו.

    === "SystemVerilog"
        ```systemverilog title="function passed_merge" linenums="1" hl_lines="13 14"
        typedef int idxq_t[$];

        // merge sort of the indices by their time; when an index of the left half is placed,
        // every right-half index already placed is a later request answered before it
        function automatic idxq_t sort_count(input int done[], idxq_t idx, ref int out[]);
          idxq_t left, right, merged;
          int mid = idx.size() / 2, j = 0;
          if (idx.size() <= 1) return idx;
          left = sort_count(done, idx[0:mid-1], out);
          right = sort_count(done, idx[mid:$], out);
          foreach (left[a]) begin
            while (j < right.size() && done[right[j]] < done[left[a]]) merged.push_back(right[j++]);
            out[left[a]] += j;                                                      // (1)!
            merged.push_back(left[a]);
          end
          while (j < right.size()) merged.push_back(right[j++]);
          return merged;
        endfunction

        function automatic void passed_merge(input int done[], output int out[]);
          idxq_t idx;
          out = new[done.size()];
          foreach (done[i]) begin out[i] = 0; idx.push_back(i); end
          void'(sort_count(done, idx, out));
        endfunction
        ```

        1. ‏`j` אינדקסים מהחצי הימני כבר הונחו לפני `left[a]` : כולם מאוחרים ממנו ונענו לפניו.

    **השוואה.** שניהם \( O(n \log n) \) זמן ו-\( O(n) \) זיכרון. מיון-מיזוג לא צריך דחיסה
    לדרגות ולא מבנה נוסף, אבל הוא רקורסיבי וסופר רק אחרי שכל הקלט ידוע : הוא מתאים לכל מה
    שמחשבים אחרי הטסט (גם את סעיף ב אפשר לספור באותו מיזוג), ולא לזרם. העץ קצר יותר לכתיבה,
    עובד **בזרם** (סעיף ג), ומשתנה רק בשאלה ששואלים אותו : אותו עץ נותן גם את סעיף ב. בראיון
    כדאי להכיר את שניהם ולנמק את הבחירה.

    #### למה זה נכון { .sol-proof }

    **שמורה.** לפני הצעד של \( i \), העץ מכיל בדיוק את הדרגות של הבקשות \( i + 1, \dots, n - 1 \),
    כל אחת פעם אחת. זה נכון בהתחלה (העץ ריק ואין בקשות אחרי \( n - 1 \)), והצעד של \( i \)
    מוסיף את הדרגה של \( i \) ולא נוגע באחרות.

    **השאילתה סופרת את הנכון.** ‏\( \text{prefix}(r - 1) \) הוא מספר הדרגות בעץ שקטנות ממש
    מ-\( r \). דרגה קטנה ממש פירושה ערך קטן ממש (הדרגות שומרות על הסדר, וערכים שווים חולקים
    דרגה), ולכן זה בדיוק \( |\{\, j > i : \text{done}[j] < \text{done}[i] \,\}| \). זמן שווה
    מקבל את הדרגה \( r \) עצמה, שמחוץ לטווח \( 1 \dots r - 1 \), ואינו נספר.

    **העץ עונה נכון.** בכל רגע `tree[i]` הוא מספר הדרגות שהוכנסו מהבלוק \( (i - \text{lowbit}(i),\ i] \),
    כי `add(r)` מגדיל בדיוק את התאים שהבלוק שלהם מכיל את \( r \) : הסדרה \( r, r + \text{lowbit}(r), \dots \)
    היא בדיוק התאים האלה, בסדר עולה. ו-`prefix(i)` קורא בלוקים זרים שמכסים את \( 1 \dots i \) :
    הבלוק של \( i \) נגמר ב-\( i \), הבא נגמר בדיוק לפניו, וכן הלאה עד 0. הסכום הוא מספר
    הדרגות ב-\( 1 \dots i \).

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n \log n) \) : המיון לדרגות \( O(n \log n) \), ואז \( n \) שאילתות ו-\( n \)
      עדכונים של \( O(\log m) \) כל אחד, עם \( m \le n \). עם זמנים שהם מספרים קטנים (עד \( T \),
      למשל מחזורי שעון בטסט קצר) אפשר לוותר על המיון ולעבוד על הזמנים עצמם ועוד 1, כי העץ
      מתחיל מ-1 וזמן 0 אפשרי : ‏\( O(n \log T) \).
    - **זיכרון :** ‏\( O(n) \) : העץ, המילון והפלט.
    - **מקרי קצה :** מערך ריק או של בקשה אחת : הכול אפסים. כל הזמנים שווים : הכול אפסים,
      כי הדרגה של כולם 1 ו-\( \text{prefix}(0) = 0 \). זמנים יורדים ממש : ‏\( \text{passed}[i] = n - 1 - i \),
      כולם עקפו את כולם.

    **נסו בעצמכם.** הקלידו `3 3 3 3` (או לחצו "שווים") : לעץ תא אחד, כל שאילתה היא `prefix(0)`
    שלא קוראת אף תא, והכול אפסים, כי זמן שווה אינו עקיפה. לחצו "הפוך" : ‏passed יוצא
    <span dir="ltr">[3, 2, 1, 0]</span> והסכום 6, כל הזוגות. הקלידו `8 7 6 5 4 3 2 1` ולחצו
    פעמיים על "הצעד הבא" : ‏`add(1)` מגדיל ארבעה תאים,
    <span dir="ltr">tree[1] → tree[2] → tree[4] → tree[8]</span>. מעבר לאיורים, התיבה מריצה את
    הקוד על קלט שלכם, גם עם זמנים שווים, ומדליקה את השורות שרצו בכל צעד :

    <div class="explorer" data-kind="overtakes" data-mode="a" data-done="5 2 6 1"></div>

---

### סעיף ב – כמה בקשות כל בקשה עקפה

??? tip "רמז 1"
    עכשיו לכל \( i \) סופרים את ה-\( j < i \) עם זמן **גדול** יותר. מאיזה כיוון כדאי ללכת,
    כדי שמה ש"כבר ראינו" יהיה בדיוק הבקשות המוקדמות?

??? tip "רמז 2"
    העץ עונה על "כמה קטנים או שווים ל-\( r \)". כמה **גדולים** מ-\( r \) יש בעץ? כמה בסך הכול
    הוכנסו, פחות התשובה הזו. שימו לב למספר שהוכנס עד עכשיו : הוא לא \( n \).

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        אותו עץ, מהבקשה הראשונה לאחרונה : כשמגיעים ל-\( i \) העץ מכיל את \( i \) הדרגות של
        הבקשות המוקדמות, ו-\( \text{prefix}(r) \) מהן קטנות או שוות ל-\( r \). השאר,
        \( \text{overtook}[i] = i - \text{prefix}(r) \), נענו אחריה : אותן היא עקפה. בדוגמה
        ‏<span dir="ltr">[0, 1, 0, 3]</span>, מול <span dir="ltr">[2, 1, 1, 0]</span> של סעיף א. שני
        הסכומים שווים (4), כי שניהם סופרים את אותם זוגות. ‏\( \text{passed}[i] \) מודד כמה
        בקשה \( i \) הורעבה, ו-\( \text{overtook}[i] \) כמה היא "דחפה".

    <!-- cost: זמן \( O(n \log n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **אותו כלי, הכיוון ההפוך.** בסעיף א הלכנו מהסוף, כדי שהעץ יחזיק את הבקשות המאוחרות.
    עכשיו רוצים את המוקדמות, ולכן הולכים מההתחלה : כשמגיעים ל-\( i \) העץ מחזיק בדיוק את
    \( i \) הדרגות של הבקשות \( 0 \dots i - 1 \).

    **לספור את הגדולים דרך הקטנים.** העץ עונה על שאלות קידומת : "כמה דרגות עד \( r \)". בקשה
    מוקדמת עקופה אם הזמן שלה **גדול** מ-\( \text{done}[i] \), כלומר הדרגה שלה גדולה ממש
    מ-\( r \). אלה כל מה שבעץ חוץ מהדרגות עד \( r \) :
    \( \text{overtook}[i] = i - \text{prefix}(r) \). שימו לב ל-\( i \) : זה מספר הדרגות שהוכנסו
    עד עכשיו, לא \( n \) ולא \( m \). ו-\( \text{prefix}(r) \), עם \( r \) ולא \( r - 1 \), כולל
    את הזמנים השווים, כך שהם **לא** נספרים כעקופים.

    **שני המערכים זה לצד זה.** על הדוגמה :

    <!-- gen 5 -->

    | הבקשה i | הזמן | ‏passed[i] | מי עקף אותה | ‏overtook[i] | את מי היא עקפה |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏0 | ‏5 | **‏2** | הבקשות ‏1, 3 | **‏0** | אף אחת |
    | ‏1 | ‏2 | **‏1** | הבקשה ‏3 | **‏1** | את ‏0 |
    | ‏2 | ‏6 | **‏1** | הבקשה ‏3 | **‏0** | אף אחת |
    | ‏3 | ‏1 | **‏0** | אף אחת | **‏3** | את ‏0, 1, 2 |
    | **סכום** | | **‏4** | | **‏4** | |

    <!-- /gen -->

    **המשמעות באימות.**

    - **‏\( \text{passed}[i] \) : כמה בקשה \( i \) הורעבה.** כל בקשה צעירה ממנה שנענתה לפניה היא
      פעם אחת שה-DUT העדיף מישהו אחר. ‏\( \max_i \text{passed}[i] \) הוא ההרעבה הגרועה ביותר
      בטסט, וגם **עומק הסידור מחדש** : מי שרוצה למסור את התשובות הלאה **לפי סדר השליחה**
      (reorder buffer) מחזיק, בזמן שהוא מחכה לתשובה של \( i \), את \( \text{passed}[i] \) התשובות
      הצעירות שכבר הגיעו (התשובה של \( i \) עצמה נמסרת מיד ואינה נספרת ; מאגר שרושם גם אותה
      צריך מקום אחד נוסף). זה גם החלון שבו scoreboard שמחפש תשובה "מהראש" צריך להסתכל.
      בשאלה [0050](0050-out-of-order-scoreboard.md) הסידור מחדש הוא רק **בין** IDs, ותוך כל
      ID התשובות בסדר : שם עומק התור של ID הוא מספר הבקשות הפתוחות שלו, וכאן מודדים את
      הערבוב עצמו.
    - **‏\( \text{overtook}[i] \) : כמה בקשה \( i \) הייתה "תוקפנית".** כמה בקשות ותיקות ממנה
      עדיין חיכו כשהיא נענתה. ‏\( \max_i \text{overtook}[i] \) הוא חסם תחתון למספר הבקשות הפתוחות
      בו-זמנית (outstanding) : ברגע שהתשובה של \( i \) הגיעה, \( \text{overtook}[i] \) בקשות
      ותיקות ממנה עוד היו פתוחות, ועוד היא עצמה.
    - **הסכום של כל אחד מהם** הוא מספר העקיפות בטסט : סעיף ג.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **דרגות ועץ ריק :** כמו בסעיף א.
    2. **מההתחלה לסוף :** לכל \( i \) מ-0 עד \( n - 1 \), כשהדרגה היא \( r \) :
    3. **שאילתה :** ‏\( \text{prefix}(r) \) : כמה מהבקשות המוקדמות נענו לא אחרי \( i \) (זמן קטן
       או שווה).
    4. **ההשלמה :** ‏\( \text{overtook}[i] = i - \text{prefix}(r) \), כי \( i \) דרגות הוכנסו.
    5. **עדכון :** ‏\( \text{add}(r) \).

    </div>

    על הדוגמה, מההתחלה :

    <!-- gen 6 -->

    | הצעד | הבקשה i | הזמן | הדרגה | כבר בעץ | השאילתה | התוצאה | ‏overtook[i] | העדכון | העץ אחרי |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏1 | ‏0 | ‏5 | ‏3 | ‏0 | ‏prefix(3) | ‏0 | **‏<span dir="ltr">0 − 0 = 0</span>** | ‏<span dir="ltr">tree[3] → tree[4]</span> | ‏<span dir="ltr">[0, 0, 1, 1]</span> |
    | ‏2 | ‏1 | ‏2 | ‏2 | ‏1 | ‏prefix(2) | ‏0 | **‏<span dir="ltr">1 − 0 = 1</span>** | ‏<span dir="ltr">tree[2] → tree[4]</span> | ‏<span dir="ltr">[0, 1, 1, 2]</span> |
    | ‏3 | ‏2 | ‏6 | ‏4 | ‏2 | ‏prefix(4) | ‏2 | **‏<span dir="ltr">2 − 2 = 0</span>** | ‏<span dir="ltr">tree[4]</span> | ‏<span dir="ltr">[0, 1, 1, 3]</span> |
    | ‏4 | ‏3 | ‏1 | ‏1 | ‏3 | ‏prefix(1) | ‏0 | **‏<span dir="ltr">3 − 0 = 3</span>** | ‏<span dir="ltr">tree[1] → tree[2] → tree[4]</span> | ‏<span dir="ltr">[1, 2, 1, 4]</span> |

    <!-- /gen -->

    בצעד 2 (בקשה 1, זמן 2, דרגה 2) בעץ דרגה אחת, 3, ו-\( \text{prefix}(2) = 0 \) : הבקשה
    היחידה שלפניה נענתה אחריה, ‏\( 1 - 0 = 1 \). בצעד האחרון (בקשה 3, דרגה 1) בעץ שלוש
    דרגות ו-\( \text{prefix}(1) = 0 \) : היא עקפה את שלושתן.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="overtook" linenums="1" hl_lines="7 8"
        def overtook(done: list[int]) -> list[int]:
            """overtook[i]: how many earlier requests were answered after request i."""
            rk = ranks(done)
            ft = Fenwick(len(rk))
            out = []
            for i, v in enumerate(done):
                out.append(i - ft.prefix(rk[v]))   # (1)!
                ft.add(rk[v])
            return out
        ```

        1. ‏`i` דרגות כבר בעץ, ‏`prefix(r)` מהן עד הדרגה \( r \) ועד בכלל. השאר, עם זמן גדול ממש, נענו אחרי \( i \).

    === "SystemVerilog"
        ```systemverilog title="function overtook" linenums="1" hl_lines="9 10"
        // overtook[i]: how many earlier requests were answered after request i
        function automatic void overtook(input int done[], output int out[]);
          int rk[int];
          Fenwick ft;
          ranks(done, rk);
          ft = new(rk.size());
          out = new[done.size()];
          foreach (done[i]) begin
            out[i] = i - ft.prefix(rk[done[i]]);   // (1)!
            ft.add(rk[done[i]]);
          end
        endfunction
        ```

        1. ‏`i` דרגות כבר בעץ (הבקשות 0 עד \( i - 1 \)), ‏`prefix(r)` מהן עד הדרגה \( r \) ועד בכלל. השאר נענו אחרי \( i \).

    #### למה זה נכון { .sol-proof }

    **השמורה :** לפני הצעד של \( i \) העץ מכיל בדיוק את הדרגות של \( 0, \dots, i - 1 \), כלומר
    \( i \) דרגות. ‏\( \text{prefix}(r) \) סופר מהן את אלה שהדרגה שלהן \( \le r \), כלומר
    \( \text{done}[j] \le \text{done}[i] \). ההשלמה, \( i - \text{prefix}(r) \), היא
    \( |\{\, j < i : \text{done}[j] > \text{done}[i] \,\}| \) : ההגדרה של \( \text{overtook}[i] \).

    **‏\( \sum_i \text{passed}[i] = \sum_i \text{overtook}[i] \).** נסתכל על קבוצת הזוגות
    \( P = \{\, (i, j) : i < j,\ \text{done}[j] < \text{done}[i] \,\} \), העקיפות. ‏\( \text{passed}[i] \)
    הוא מספר הזוגות ב-\( P \) שהרכיב הראשון שלהם \( i \), ו-\( \text{overtook}[j] \) מספר
    הזוגות שהרכיב השני שלהם \( j \). שני הסכומים סופרים את \( |P| \), כל זוג פעם אחת, פעם לפי
    הרכיב הראשון ופעם לפי השני. בדוגמה \( P = \{(0, 1), (0, 3), (1, 3), (2, 3)\} \), ושני הסכומים 4.

    **עומק הסידור מחדש.** מאגר שמוסר תשובות לפי סדר השליחה מחזיק בכל רגע תשובות שהגיעו
    ומחכות לבקשה \( h \) שבראש התור, הוותיקה ביותר שעוד לא נענתה. כולן נשלחו אחרי \( h \)
    ונענו לפניה, ולכן יש מהן לכל היותר \( \text{passed}[h] \) : התפוסה אף פעם לא עולה על
    המקסימום של \( \text{passed} \). מצד שני, רגע לפני שמגיעה התשובה של בקשה \( i \), כל
    \( \text{passed}[i] \) התשובות שעקפו אותה כבר במאגר, כי אף אחת מהן לא יכולה להימסר
    לפני \( i \). לכן התפוסה הגדולה ביותר היא בדיוק \( \max_i \text{passed}[i] \) (המבחן של השאלה
    מדמה את המאגר ובודק את השוויון).

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n \log n) \), כמו בסעיף א : אותו מיון, אותם \( 2n \) מעברים על העץ.
    - **זיכרון :** ‏\( O(n) \).
    - **שני המערכים יחד :** שני מעברים על אותן דרגות, אחד מהסוף (‏\( \text{passed} \)) ואחד
      מההתחלה (‏\( \text{overtook} \)) ; המיון לדרגות נעשה פעם אחת.

    **נסו בעצמכם.** הקלידו `3 3 1` : ‏overtook יוצא <span dir="ltr">[0, 0, 2]</span>. בקשה 1 לא
    עקפה את בקשה 0, שנענתה באותו זמן, כי השאילתה היא `prefix(r)` ולא `prefix(r - 1)`. לחצו
    "הפוך" : ‏<span dir="ltr">[0, 1, 2]</span>, והסכום 3 שווה לסכום של passed בתיבה של סעיף א על
    אותו קלט. התיבה מוסיפה לטבלה קלט שלכם ואת התאים שכל שאילתה קוראת :

    <div class="explorer" data-kind="overtakes" data-mode="b" data-done="5 2 6 1"></div>

---

### סעיף ג – סך העקיפות, אי-הסדר של הטסט, ודיווח בזמן אמת

??? tip "רמז 1"
    סך העקיפות הוא מספר הזוגות ההפוכים (inversions) של המערך. כמה הוא יכול להיות לכל
    היותר? מתי הוא 0?

??? tip "רמז 2"
    באיזה סדר התשובות מגיעות ל-scoreboard בזמן אמת, ומה כבר ממוין? מה שצריך לדעת כשמגיעה
    התשובה של בקשה \( i \) הוא כמה מהבקשות **שכבר נענו** נשלחו **אחריה**. מה "הערך" שמכניסים
    לעץ עכשיו, ומה הדרגה שלו?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        סך העקיפות הוא מספר ההיפוכים של `done` : הסכום של סעיף ב במעבר אחד, \( O(n \log n) \),
        או מיון-מיזוג. הוא 0 כשהתשובות בסדר ו-\( n(n - 1) / 2 \) כשהן הפוכות לגמרי, והחלוקה
        בו נותנת **אי-סדר** בין 0 ל-1 : מדד כיסוי ל"כמה הטסט ערבב". בדוגמה \( 4 / 6 \approx 0.67 \).
        בזמן אמת : התשובות מגיעות לפי סדר הזמן, ואינדקס השליחה הוא הדרגה בעצמו. עץ על
        \( 1 \dots n \) : כשמגיעה התשובה של \( i \), העקיפות שספגה הן "כמה כבר ענו" פחות
        \( \text{prefix}(i + 1) \), ואז \( \text{add}(i + 1) \). זה scoreboard שמדווח על כל עקיפה
        ברגע שהיא קורית.

    <!-- cost: זמן \( O(\log n) \) לתשובה | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **סך העקיפות.** לפי סעיף ב, \( \sum_i \text{overtook}[i] \) הוא מספר הזוגות ההפוכים
    (inversions) של `done`. אותו מעבר, עם מונה אחד במקום מערך. המספר הזה עונה על "כמה
    הטסט ערבב" : הוא 0 בדיוק כשהתשובות הגיעו לפי סדר השליחה (אין אף זוג הפוך), והוא
    \( \binom{n}{2} = n(n - 1) / 2 \) בדיוק כשכל זוג הפוך, כלומר התשובות הגיעו בסדר הפוך
    לגמרי. החלוקה ב-\( n(n - 1) / 2 \) נותנת **אי-סדר מנורמל** בין 0 ל-1, שאינו תלוי באורך
    הטסט. זה מדד כיסוי : coverpoint הוא ביטוי שלם, ולכן דוגמים אותו באחוזים שלמים, עם bins של
    0, של 1 עד 10, של 11 עד 30 וכן הלאה, ודורשים שטסטים של ערבוב יגיעו ל-bins הגבוהים. טסט
    שה-DUT ענה בו תמיד לפי הסדר נותן 0, ו-scoreboard של תשובות שלא לפי הסדר שעבר רק טסטים
    כאלה לא נבדק.

    **בזמן אמת : אינדקס השליחה הוא הדרגה.** עד עכשיו הסתכלנו על `done` אחרי הטסט. ב-scoreboard
    התשובות מגיעות **לפי סדר הזמן**, אחת אחרי השנייה, ועם כל תשובה מגיע ה-tag של הבקשה.
    ‏tags אמיתיים (AXI ID, ה-tag של PCIe) חוזרים על עצמם, ולכן ה-scoreboard רושם בשליחה לכל tag
    את מספר השליחה של הבקשה, ומתרגם את ה-tag של התשובה חזרה : ‏\( i \) כאן הוא תמיד מספר
    השליחה. עכשיו הזרם ממוין מעצמו, והערך שסופרים הוא אינדקס השליחה, שכבר נמצא
    ב-\( 0 \dots n - 1 \) : **לא צריך דחיסה**. העץ הוא על \( 1 \dots n \) (האינדקס ועוד 1), ומחזיק
    את הבקשות שכבר נענו. כשמגיעה התשובה של \( i \) : מספר הבקשות שכבר נענו ונשלחו **אחרי** \( i \)
    הוא "כמה נענו עד עכשיו" פחות \( \text{prefix}(i + 1) \) (אלה שנשלחו עד \( i \)). זה בדיוק
    \( \text{passed}[i] \), מדווח ברגע שהתשובה מגיעה, ולא בסוף. הסכום הרץ הוא סך העקיפות עד
    הרגע הזה, והחלוקה ב-\( k(k - 1) / 2 \) (‏\( k \) תשובות עד כה) או ב-\( n(n - 1) / 2 \) נותנת
    את אי-הסדר הרץ. בטסט שאינו נגמר העץ הוא חלון : בקשות שמספרן קטן מהבקשה הפתוחה הוותיקה
    ביותר כבר נענו כולן ונספרות גם ב-\( k \) וגם בכל \( \text{prefix} \), ולכן אפשר להוציא אותן
    משניהם ולמחזר את האינדקסים שלהן.

    **הזווית של החומרה.** העץ הוא מבנה בגודל קבוע : \( n \) מונים (תא שומר ספירה של בלוק שלם,
    עד \( \lfloor \log_2 n \rfloor + 1 \) ביטים), ושאילתה או עדכון נוגעים כל אחד
    ב-\( \lfloor \log_2 n \rfloor + 1 \) תאים לכל היותר, בכתובות שנקבעות מהביטים של \( i \). ב-RTL
    של מוניטור יש דרך פשוטה יותר : כל בקשה נענית פעם אחת, ולכן מספיק וקטור של \( n \) ביטים,
    ביט לבקשה שנענתה, ו-popcount של הביטים שמעל \( i \) : מחזור אחד, בלי לולאה ובלי עץ (הקוד,
    התרשים והטבלה לפי מחזורים בשאלת ההמשך הראשונה). העץ מתאים לתוכנה ולמודלים, שבהם
    \( n \) גדול ו-popcount של \( n \) ביטים אינו פעולה אחת.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סך העקיפות :** המעבר של סעיף ב עם מונה : ‏\( \text{total} \mathrel{+}= i - \text{prefix}(r) \).
    2. **אי-הסדר :** ‏\( \text{total} / \binom{n}{2} \), ‏0 בסדר מלא, 1 בסדר הפוך.
    3. **הזרם :** התשובות לפי סדר ההגעה, \( k = 0, 1, \dots \), כל אחת עם מספר הבקשה שלה \( i \).
       עץ על \( 1 \dots n \).
    4. **דיווח :** ‏\( \text{passed}[i] = k - \text{prefix}(i + 1) \) : כבר ענו \( k \), מהן
       \( \text{prefix}(i + 1) \) נשלחו עד \( i \) ועד בכלל, והשאר נשלחו אחריה ועקפו אותה.
    5. **עדכון :** ‏\( \text{add}(i + 1) \), והסכום הרץ גדל ב-\( \text{passed}[i] \).

    </div>

    על הדוגמה התשובות מגיעות בסדר <span dir="ltr">3, 1, 0, 2</span> (הזמנים <span dir="ltr">1, 2, 5, 6</span>),
    והעץ הוא על אינדקסי השליחה ועוד 1, כלומר <span dir="ltr">[tree[1], tree[2], tree[3], tree[4]]</span>
    עבור הבקשות 0 עד 3 :

    <!-- gen 7 -->

    | ההגעה k | הבקשה i | הזמן | כבר ענו | ‏prefix(i + 1) | עקיפות שספגה | הסכום הרץ | אי-הסדר | העץ אחרי |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏0 | ‏3 | ‏1 | ‏0 | ‏0 | **‏<span dir="ltr">0 − 0 = 0</span>** | ‏0 | ‏<span dir="ltr">0/6 ≈ 0.00</span> | ‏<span dir="ltr">[0, 0, 0, 1]</span> |
    | ‏1 | ‏1 | ‏2 | ‏1 | ‏0 | **‏<span dir="ltr">1 − 0 = 1</span>** | ‏1 | ‏<span dir="ltr">1/6 ≈ 0.17</span> | ‏<span dir="ltr">[0, 1, 0, 2]</span> |
    | ‏2 | ‏0 | ‏5 | ‏2 | ‏0 | **‏<span dir="ltr">2 − 0 = 2</span>** | ‏3 | ‏<span dir="ltr">3/6 ≈ 0.50</span> | ‏<span dir="ltr">[1, 2, 0, 3]</span> |
    | ‏3 | ‏2 | ‏6 | ‏3 | ‏2 | **‏<span dir="ltr">3 − 2 = 1</span>** | ‏4 | ‏<span dir="ltr">4/6 ≈ 0.67</span> | ‏<span dir="ltr">[1, 2, 1, 4]</span> |

    <!-- /gen -->

    כשמגיעה התשובה של בקשה 0 (השלישית), שתיים כבר ענו, ואף אחת מהן לא נשלחה עד 0
    (‏\( \text{prefix}(1) = 0 \)) : שתיהן עקפו אותה, וזה \( \text{passed}[0] = 2 \) של סעיף א,
    רק שעכשיו הוא ידוע ברגע ההגעה. הסכום הרץ מגיע ל-4, ואי-הסדר ל-\( 4 / 6 \).

    #### הקוד { .sol-code }

    === "Python"
        ```python title="inversions, disorder, arrival_order, live_overtakes" linenums="1" hl_lines="7 30 31"
        def inversions(done: list[int]) -> int:
            """The number of overtakes, every pair counted once: one pass of part b, summed."""
            rk = ranks(done)
            ft = Fenwick(len(rk))
            total = 0
            for i, v in enumerate(done):
                total += i - ft.prefix(rk[v])
                ft.add(rk[v])
            return total


        def disorder(done: list[int]) -> float:
            """The overtakes as a share of the n(n - 1) / 2 pairs: 0 in order, 1 fully reversed."""
            pairs = len(done) * (len(done) - 1) // 2
            return inversions(done) / pairs if pairs else 0.0


        def arrival_order(done: list[int]) -> list[int]:
            """The requests in the order their responses arrive (an equal time keeps the send order)."""
            return sorted(range(len(done)), key=lambda i: (done[i], i))


        def live_overtakes(order: list[int], n: int) -> list[int]:
            """The responses as they arrive: order[k] is the request answered k-th. For each
            arrival, how many later-sent requests were answered before it: a tree over the
            send indices 1..n, no compression, updated online."""
            ft = Fenwick(n)
            out = []
            for k, i in enumerate(order):
                out.append(k - ft.prefix(i + 1))   # (1)!
                ft.add(i + 1)                      # (2)!
            return out
        ```

        1. ‏`k` בקשות כבר נענו, ‏`prefix(i + 1)` מהן נשלחו עד \( i \) ועד בכלל. השאר נשלחו אחרי \( i \) ונענו לפניה : העקיפות שספגה.
        2. העדכון אחרי השאילתה, באינדקס \( i + 1 \) : העץ מתחיל מ-1.

    === "SystemVerilog"
        ```systemverilog title="function inversions, disorder, arrival_order, live_overtakes" linenums="1" hl_lines="8 24 33 34"
        // the number of overtakes, every pair counted once: one pass of part b, summed
        function automatic int inversions(input int done[]);
          int rk[int], total = 0;
          Fenwick ft;
          ranks(done, rk);
          ft = new(rk.size());
          foreach (done[i]) begin
            total += i - ft.prefix(rk[done[i]]);
            ft.add(rk[done[i]]);
          end
          return total;
        endfunction

        // the overtakes as a share of the n(n - 1) / 2 pairs: 0 in order, 1 fully reversed
        function automatic real disorder(input int done[]);
          int pairs = done.size() * (done.size() - 1) / 2;
          return pairs ? real'(inversions(done)) / pairs : 0.0;
        endfunction

        // the requests in the order their responses arrive (an equal time keeps the send order)
        function automatic void arrival_order(input int done[], output int order[$]);
          order = {};
          foreach (done[i]) order.push_back(i);
          order.sort(x) with ({done[x], x});                   // (1)!
        endfunction

        // the responses as they arrive: order[k] is the request answered k-th; for each
        // arrival, how many later-sent requests were answered before it (a tree over the
        // send indices 1..n, no compression, updated online)
        function automatic void live_overtakes(input int order[$], input int n, output int out[$]);
          Fenwick ft = new(n);
          out = {};
          foreach (order[k]) begin
            out.push_back(k - ft.prefix(order[k] + 1));        // (2)!
            ft.add(order[k] + 1);
          end
        endfunction
        ```

        1. המפתח הוא הזמן ואחריו האינדקס, כך שזמנים שווים נשארים בסדר השליחה ואינם נספרים כעקיפה. הזמנים אי-שליליים, ולכן השרשור ממוין נכון.
        2. ‏`k` בקשות כבר נענו, ‏`prefix(order[k] + 1)` מהן נשלחו עד הבקשה הזו ועד בכלל. השאר נשלחו אחריה ונענו לפניה.

    #### למה זה נכון { .sol-proof }

    **סך העקיפות.** לפי סעיף ב הסכום של \( \text{overtook} \) הוא \( |P| \), מספר הזוגות
    \( i < j \) עם \( \text{done}[j] < \text{done}[i] \). ‏\( P \) ריקה בדיוק כשהסדרה לא יורדת
    (אין שני איברים הפוכים), ו-\( P \) היא כל \( \binom{n}{2} \) הזוגות בדיוק כשהסדרה יורדת
    ממש. לכן אי-הסדר הוא 0 בסדר מלא, 1 בסדר הפוך מלא, ובין לבין מספר הזוגות שה-DUT הפך
    חלקי כל הזוגות.

    **הזרם.** כשמגיעה התשובה ה-\( k \) (מ-0), של בקשה \( i \), העץ מכיל בדיוק את \( k \)
    הבקשות שנענו לפניה, כי כל תשובה נכנסת לעץ אחרי השאילתה שלה. ‏\( \text{prefix}(i + 1) \)
    הוא מספרן שנשלחו ב-\( 0 \dots i \). השאר, \( k - \text{prefix}(i + 1) \), נשלחו אחרי \( i \)
    ונענו לפניה : זה \( \text{passed}[i] \) בדיוק, כי בקשה שנענתה לפני \( i \) בזרם היא בקשה
    עם זמן קטן יותר (ועם זמן שווה היא נמצאת לפניה בזרם רק אם נשלחה לפניה, ואז היא נספרת
    ב-\( \text{prefix} \) ולא כעקיפה). הסכום הרץ אחרי כל התשובות הוא \( \sum_i \text{passed}[i] = |P| \).

    **אין צורך במיון.** הדרגה של בקשה \( i \) בעץ היא \( i + 1 \) : אינדקסי השליחה כבר
    מספרים רצופים מ-0 ושונים זה מזה, ולכן המיפוי ערך → דרגה הוא הזזה ב-1 בלבד.

    #### סיבוכיות { .sol-cost }

    - **סך העקיפות מהטרייס :** ‏\( O(n \log n) \) זמן ו-\( O(n) \) זיכרון, כמו סעיף ב.
    - **בזמן אמת :** ‏\( O(\log n) \) לכל תשובה, בלי מיון ובלי דחיסה, ו-\( O(n) \) זיכרון שנקבע
      מראש : \( n \) מונים. ב-RTL : ‏\( n \) ביטים ו-popcount, מחזור אחד.
    - **הנירמול :** חילוק אחד בסוף, או בכל תשובה אם רוצים את אי-הסדר הרץ.

    **נסו בעצמכם.** לחצו "בסדר" : אי-הסדר 0.00, והמאגר (השורה buffer) ריק אחרי כל הגעה. לחצו
    "הפוך" : אי-הסדר 1.00, והמאגר מתמלא עד 3 ומתרוקן רק בתשובה האחרונה. ועל
    <span dir="ltr">5 2 6 1</span> : אחרי התשובה השלישית הסכום הרץ כבר 3 מתוך 4, והמאגר החזיק
    לכל היותר 2, המקסימום של passed. התיבה מוסיפה לטבלה את תפוסת המאגר אחרי כל הגעה :

    <div class="explorer" data-kind="overtakes" data-mode="c" data-done="5 2 6 1"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להישאר בלולאה הכפולה"
    ‏\( O(n^2) \) היא תשובה ראשונה טובה : נכונה, ומראה שהבנתם מה סופרים. המלכודת היא להישאר
    בה. על טרייס של \( 10^6 \) תשובות זה \( 5 \cdot 10^{11} \) השוואות : דקות ארוכות בקוד מקומפל
    ושעות רבות ב-Python, ולמראיין ברור שיש \( O(n \log n) \). אמרו "זו הגרסה הפשוטה, ועכשיו
    נשפר", ועברו לעץ או למיון-מיזוג.

??? trap "מלכודת : זמנים שווים נספרים כעקיפה"
    בסעיף א שאילתה של \( \text{prefix}(r) \) במקום \( \text{prefix}(r - 1) \) סופרת גם בקשות
    מאוחרות עם **אותו** זמן, ובסעיף ב \( i - \text{prefix}(r - 1) \) סופרת מוקדמות עם אותו
    זמן. בדחיסה, ערכים שווים חייבים לקבל **אותה** דרגה : מילון על הערכים השונים
    (‏`sorted(set(done))`), ולא "המקום של כל בקשה ברשימה הממוינת של כל \( n \) הזמנים", שנותן
    לשני זמנים שווים דרגות שונות, ואז אחד מהם "קטן" מהשני ונספר. במיזוג ההשוואה היא `<`
    ממש. בודקים על מערך שכולו אותו ערך : התשובה חייבת להיות אפסים.

??? trap "מלכודת : אינדקס 0 בעץ, ו-`i & -i`"
    עץ Fenwick עובד מ-1 : עם \( i = 0 \) הביט הנמוך הוא 0, ‏`i += i & -i` לא זז, והלולאה
    אינסופית (או `prefix(0)` חוזר מיד, שזה בסדר, אבל `add(0)` לא). לכן המערך באורך \( m + 1 \)
    והדרגות מתחילות מ-1, ובסעיף ג מכניסים \( i + 1 \) ולא \( i \). ב-SystemVerilog `i & -i`
    על `int` עובד כצפוי (משלים ל-2 ב-32 ביט), וגם על טיפוס לא חתום, כמו `logic [31:0]`,
    יוצא אותו ביט. ההבדל בין הטיפוסים הוא בהשוואות של הלולאות כשמערבבים חתום ולא חתום :
    השאירו את האינדקס ואת \( n \) באותו טיפוס, `int` כמו בקוד.

??? trap "מלכודת : לעדכן לפני ששואלים"
    אם מכניסים את הדרגה של \( i \) ואז שואלים, בסעיף ב \( \text{prefix}(r) \) כולל את \( i \)
    עצמה ו-\( i - \text{prefix}(r) \) יוצא קטן ב-1 (ואפילו שלילי כשהיא לבדה), ובסעיף ג
    \( k - \text{prefix}(i + 1) \) גם כן. בסעיף א עם \( r - 1 \) הסדר לא משנה, וזה בדיוק מה
    שמסתיר את הבאג עד שעוברים לסעיף ב. הכלל : קודם שואלים על מה שכבר בעץ, אחר כך מצטרפים.

??? trap "מלכודת : בסעיף ב להשלים ל-n במקום למספר שהוכנס"
    ‏\( \text{overtook}[i] = n - \text{prefix}(r) \) סופר גם את כל הבקשות **המאוחרות**, שעוד לא
    בעץ בכלל. מה שמשלימים ממנו הוא מספר הדרגות שהוכנסו עד עכשיו, \( i \), ולא \( n \) ולא
    \( m \). (אם רוצים בכל זאת עץ "מלא", מכניסים קודם את כולן, הולכים **מהסוף להתחלה**
    ומוציאים כל בקשה, בעדכון של \( -1 \), לפני השאילתה שלה : אותה תוצאה, יותר עבודה, ועדכון
    שהעץ שבעמוד לא תומך בו.)

??? followup "שאלות המשך"
    - **המוניטור ב-RTL :** כתבו את המוניטור של סעיף ג כמודול, עם וקטור של ביטים במקום העץ.
      מה בודקים בו, ומה אוספים ממנו לכיסוי?

        ??? fu-answer "תשובה"
            ביט לכל בקשה שנענתה, `answered`. כשמגיעה התשובה של הבקשה `rsp_seq`, הביטים הדולקים
            שמעליה הם הבקשות שנשלחו אחריה וכבר נענו : הזזה ימינה ב-`rsp_seq + 1` משאירה רק
            אותם, ו-popcount סופר אותם. באותו מחזור הביט שלה נדלק, המקסימום והסכום מתעדכנים :

            <!-- gen 8 -->

            <svg class="figure ov-dp" viewBox="0 0 560 244" direction="ltr" style="max-width:35rem" role="img" aria-label="תרשים המלבנים של המוניטור : הטבלה seq_of_tag הופכת את ה-tag של התשובה למספר השליחה rsp_seq, הווקטור answered מוזז ימינה ב-seq + 1 כך שנשארים הביטים שמעל הבקשה, ‏popcount סופר אותם ונותן את passed, ובאותו מחזור הביט rsp_seq של answered נדלק, max_passed שומר את המקסימום ו-total את הסכום"><defs><marker id="ov-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="ov-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs><g class="ov-blk"><rect x="86" y="20" width="116" height="44" rx="5"/><text x="144" y="39" text-anchor="middle">seq_of_tag</text><text class="ov-sub" x="144" y="56" text-anchor="middle">[rsp_tag]</text></g><g class="ov-blk ov-st1"><rect x="290" y="20" width="100" height="44" rx="5"/><text x="340" y="39" text-anchor="middle">&gt;&gt; seq+1</text><text class="ov-sub" x="340" y="56" text-anchor="middle">bits above</text></g><g class="ov-blk ov-st1"><rect x="418" y="20" width="110" height="44" rx="5"/><text x="473" y="47" text-anchor="middle">popcount</text></g><g class="ov-blk ov-st2"><rect x="280" y="110" width="120" height="44" rx="5"/><text x="340" y="129" text-anchor="middle">answered</text><text class="ov-sub" x="340" y="146" text-anchor="middle">N bits</text></g><g class="ov-blk"><rect x="418" y="110" width="110" height="44" rx="5"/><text x="473" y="129" text-anchor="middle">max_passed</text><text class="ov-sub" x="473" y="146" text-anchor="middle">max</text></g><g class="ov-blk"><rect x="418" y="190" width="110" height="44" rx="5"/><text x="473" y="209" text-anchor="middle">total</text><text class="ov-sub" x="473" y="226" text-anchor="middle">+= passed</text></g><path class="ov-wire" d="M6,42 L86,42" marker-end="url(#ov-hb)"/><text class="ov-wlab" x="8" y="34" text-anchor="start">rsp_tag</text><path class="ov-wire" d="M202,42 L290,42" marker-end="url(#ov-hb)"/><text class="ov-wlab" x="210" y="34" text-anchor="start">rsp_seq</text><path class="ov-wire" d="M246,42 L246,132 L280,132" marker-end="url(#ov-hb)"/><text class="ov-wlab" x="238" y="128" text-anchor="end">set bit</text><path class="ov-wire" d="M340,110 L340,64" marker-end="url(#ov-hb)"/><path class="ov-wire" d="M390,42 L418,42" marker-end="url(#ov-hb)"/><path class="ov-wire" d="M528,42 L556,42" marker-end="url(#ov-hb)"/><text class="ov-wlab" x="556" y="14" text-anchor="end">passed</text><path class="ov-wire" d="M542,42 L542,212 L528,212" marker-end="url(#ov-hb)"/><path class="ov-wire" d="M542,132 L528,132" marker-end="url(#ov-hb)"/><circle class="ov-dot" cx="246" cy="42" r="3.5"/><circle class="ov-dot" cx="542" cy="42" r="3.5"/><circle class="ov-dot" cx="542" cy="132" r="3.5"/></svg>

            <!-- /gen -->

            <!-- gen 9 -->

            <span class="viz-legend"><span><i class="ov-key-q"></i>השאילתה : הביטים שמעל הבקשה, וספירתם</span><span><i class="ov-key-u"></i>העדכון : הביט של הבקשה נדלק</span><span><i class="ov-key-req"></i>הטבלה מ-tag למספר השליחה, המקסימום והסכום</span></span>

            <!-- /gen -->

            ```systemverilog title="module ooo_monitor" linenums="1" hl_lines="11 16"
            // the monitor of part c in RTL: a bit per answered request instead of the tree; one
            // response a clock, rsp_seq is the send number of the request (looked up from its tag)
            module ooo_monitor #(parameter int N = 16, parameter int MAX_REORDER = N - 1) (
              input  logic                 clk, rst_n, rsp_valid,
              input  logic [$clog2(N)-1:0] rsp_seq,
              output logic [$clog2(N):0]   passed,       // with rsp_valid: the overtakes this response took
              output logic [$clog2(N):0]   max_passed,
              output logic [31:0]          total
            );
              logic [N-1:0] answered;
              assign passed = ($clog2(N) + 1)'($countones(answered >> (32'(rsp_seq) + 1)));   // (1)!
              always_ff @(posedge clk or negedge rst_n)
                if (!rst_n) begin
                  answered <= '0; max_passed <= '0; total <= '0;
                end else if (rsp_valid) begin
                  answered[rsp_seq] <= 1'b1;                                               // (2)!
                  if (passed > max_passed) max_passed <= passed;
                  total <= total + 32'(passed);
                end

              int fails = 0;
              a_once:  assert property (@(posedge clk) disable iff (!rst_n) rsp_valid |-> !answered[rsp_seq]) else fails++;
              a_depth: assert property (@(posedge clk) disable iff (!rst_n) rsp_valid |-> int'(passed) <= MAX_REORDER) else fails++;   // (3)!

              covergroup cg @(posedge clk);
                cp_passed: coverpoint passed iff (rst_n && rsp_valid) { bins none = {0}; bins one = {1}; bins few = {[2:3]}; bins many = {[4:$]}; }
                cp_disorder: coverpoint 100 * total / (N * (N - 1) / 2) iff (rst_n && (&answered)) {   // (4)!
                  bins in_order = {0}; bins low = {[1:10]}; bins mid = {[11:30]}; bins high = {[31:100]};
                }
              endgroup
              cg cov = new();
            endmodule
            ```

            1. הביטים של הבקשות שנשלחו אחרי `rsp_seq`, נספרים במחזור אחד. זו השאילתה, לפני העדכון : ‏`answered` עוד בלי הביט של התשובה הזו.
            2. העדכון, בקצה השעון. תשובה אחת במחזור ; עם כמה תשובות באותו מחזור סופרים את כולן מול אותו `answered`, ורק אז מדליקים את כל הביטים שלהן.
            3. הרעבה : תשובה שיותר מ-`MAX_REORDER` בקשות צעירות עקפו אותה. זה גם העומק שמאגר הסידור מחדש של ה-DUT הובטח לו.
            4. אי-הסדר באחוזים שלמים, נדגם כשכל הבקשות נענו. ערך ממשי אינו coverpoint.

            על הדוגמה (הזמנים הם מספרי המחזור, `answered` כתוב עם הביט של בקשה 3 משמאל) :

            <!-- gen 10 -->

            | מחזור | ‏rsp_seq | ‏answered לפני | הביטים שמעל | ‏passed | ‏answered אחרי | ‏max_passed | ‏total |
            |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
            | ‏1 | ‏3 | ‏`0000` | ‏`0000` | **‏0** | ‏`1000` | ‏0 | ‏0 |
            | ‏2 | ‏1 | ‏`1000` | ‏`1000` | **‏1** | ‏`1010` | ‏1 | ‏1 |
            | ‏5 | ‏0 | ‏`1010` | ‏`1010` | **‏2** | ‏`1011` | ‏2 | ‏3 |
            | ‏6 | ‏2 | ‏`1011` | ‏`1000` | **‏1** | ‏`1111` | ‏2 | ‏4 |

            <!-- /gen -->

            במחזורים 3 ו-4 אין תשובה (`rsp_valid` הוא 0) ושום דבר לא משתנה. במחזור 5 מגיעה
            התשובה של בקשה 0, ומעליה דולקים הביטים של 1 ושל 3 : ‏`passed` הוא 2, כמו בסעיף א.
            ‏`a_once` תופסת תשובה שנייה לאותה בקשה (או תרגום שגוי של tag), ו-`cp_passed` דורש
            שהטסט הגיע גם לתשובה שלא נעקפה וגם לתשובה שנעקפה ארבע פעמים ויותר.

    - **השרשרת הארוכה ביותר של תשובות בסדר :** מהו המספר הגדול ביותר של בקשות שנענו
      **לפי סדר השליחה** שלהן, ואיך מחשבים אותו ב-\( O(n \log n) \)?

        ??? fu-answer "תשובה"
            זו תת-הסדרה **הלא-יורדת** הארוכה ביותר של `done` (זמן שווה אינו עקיפה, ולכן שתי
            תשובות מאותו מחזור הן בסדר). מחזיקים מערך `tails` שבו `tails[L]` הוא הזמן הקטן
            ביותר שמסיים שרשרת באורך \( L + 1 \) ; לכל זמן מוצאים בחיפוש בינארי את המקום הראשון
            ש**גדול** ממנו (`bisect_right`) ומחליפים (או מאריכים). ‏`tails` לא יורד, ולכן
            \( O(\log n) \) לאיבר. בדוגמה <span dir="ltr">5 2 6 1</span> התשובה 2 (‏<span dir="ltr">2 6</span>
            או <span dir="ltr">5 6</span>), ועל <span dir="ltr">3 3 3</span> היא 3, לא 1. ‏\( n \) פחות
            האורך הזה הוא כמה בקשות לפחות "יצאו מהתור".

    - **כמה החלפות מסדרות את התשובות :** נתון סדר ההגעה כתמורה של \( 0 \dots n - 1 \). מהו
      מספר ההחלפות (swap של שני איברים) הקטן ביותר שמחזיר אותו לסדר השליחה?

        ??? fu-answer "תשובה"
            ‏\( n \) פחות מספר המעגלים של התמורה, כמו בשאלה [0009](../junior/0009-boxes-cycles-helper.md) :
            החלפה אחת מפרקת מעגל אחד לשניים, ולכן צריך לפחות (אורך − 1) החלפות למעגל, וזה
            מספיק. בדוגמה סדר ההגעה <span dir="ltr">3 1 0 2</span> הוא המעגל \( 0 \to 3 \to 2 \to 0 \)
            והנקודה הקבועה 1 : שני מעגלים, \( 4 - 2 = 2 \) החלפות. שימו לב שזה מדד אחר מסך
            העקיפות (שם 4) : ההיפוכים סופרים החלפות של **שכנים**.

    - **מרחק העקיפה הגדול ביותר :** מהו ה-\( j - i \) הגדול ביותר בין בקשה לבקשה שעקפה אותה,
      ואיך מוצאים אותו בזמן ליניארי?

        ??? fu-answer "תשובה"
            צריך \( i \) קטן עם זמן גדול ו-\( j \) גדול עם זמן קטן. מחשבים מינימום-סיפא
            \( \text{suf}[j] = \min(\text{done}[j], \dots, \text{done}[n - 1]) \) ועוברים עם שני
            מצביעים : אם \( \text{suf}[j] < \text{done}[i] \) יש עקיפה במרחק \( j - i \) לפחות
            (מישהו מ-\( j \) והלאה), מקדמים \( j \) ; אחרת אף \( j' \ge j \) לא עוקף את \( i \),
            ומקדמים \( i \). ‏\( O(n) \). בדוגמה 3 : בקשה 3 עקפה את בקשה 0.

    - **זמנים שאינם שונים :** ה-DUT עונה על כמה בקשות באותו מחזור. מה משתנה בכל סעיף?

        ??? fu-answer "תשובה"
            בטרייס : הדרגות של ערכים שווים שוות, \( r - 1 \) בסעיף א ו-\( r \) בסעיף ב, וזהו :
            אותו מחזור אינו עקיפה. בזרם : צריך להחליט באיזה סדר התשובות של אותו מחזור
            "מגיעות" ; אם המוניטור מעביר אותן לפי סדר השליחה (או שואל על כולן, עם אותו \( k \),
            ורק אז מעדכן את כולן), אותו מחזור אינו נספר. לעדכן את כולן ורק אז לשאול נותן
            ספירה שגויה. אם מגדירים אחרת, למשל "אותו מחזור הוא חצי עקיפה", סופרים את השווים
            בנפרד : ‏\( \text{prefix}(r) - \text{prefix}(r - 1) \).
