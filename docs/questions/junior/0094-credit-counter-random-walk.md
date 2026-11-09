---
id: 94
title: מונה credits בהליכה אקראית – יתמלא או יתרוקן?
level: junior
difficulty: medium
kind: math
tags: [probability, protocols, proof, math, python, systemverilog]
source: "בעיית ההרס של המהמר (Gambler's ruin), מ-Pascal ו-Huygens; כאן במונה credits של פרוטוקול בחומרה"
added: 2026-11-06
---

## השאלה

בפרוטוקול עם credits (כמו ב-PCIe או ב-USB4) אצל השולח יש מונה של credits בין 0 ל-\( N \).
בכל מחזור שעון המקבל יכול להחזיר credit, והמונה עולה ב-1, או שהשולח צורך credit, והמונה
יורד ב-1. כשהמונה מגיע ל-\( N \) הוא **מלא**, וכשהוא מגיע ל-0 הוא **ריק** והשולח נעצר. בשני
המקרים הניסוי נגמר.

מתחילים עם \( k \) credits. בכל סעיף מחשבים שלושה מספרים : הסיכוי שהמונה **יתמלא** (יגיע
ל-\( N \) לפני 0), הסיכוי שהוא **יתרוקן** (יגיע ל-0 קודם), ומספר המחזורים **הממוצע** עד
שהוא נוגע באחד משני הקירות. הסעיפים מכלילים את המודל צעד אחרי צעד : קודם הוגן, אחר כך עם
הטיה, אחר כך עם מחזורים שבהם לא קורה כלום, ובסוף עם זמנים גאומטריים בין האירועים.

??? interviewer "מה המראיין בודק"
    - **משוואת הצעד הראשון :** האם המועמד מגדיר פונקציה של נקודת ההתחלה ומתנה על המחזור
      הראשון, במקום לנסות לספור מסלולים.
    - **תנאי שפה :** האם הוא רושם מה קורה על הקירות, ומבין שהם קובעים את הפתרון.
    - **פתרון נוסחת נסיגה :** פתרון מהצורה \( x^k \), פתרון פרטי לזמן, והמקרה המיוחד
      \( p = q \).
    - **רדוקציה :** האם הוא רואה שמחזורים בלי שינוי ושני תהליכים גאומטריים הם אותה הליכה,
      רק איטית יותר, ולא פותר הכול מחדש.
    - **בדיקה בסימולציה :** האם הוא יודע לבדוק נוסחה ב-Monte Carlo עם סובלנות סבירה, גם
      בבודק של SystemVerilog.

---

### סעיף א – הוגן, מ-3 עד 10

‏\( N = 10 \) ומתחילים עם \( k = 3 \). בכל מחזור המונה עולה ב-1 בהסתברות חצי ויורד ב-1
בהסתברות חצי. מה הסיכוי שיתמלא, מה הסיכוי שיתרוקן, וכמה מחזורים עוברים בממוצע עד שהוא
נוגע בקיר?

??? tip "רמז 1"
    סמנו ב-\( P(k) \) את הסיכוי להתמלא כשמתחילים מ-\( k \). אחרי מחזור אחד המונה ב-\( k + 1 \)
    או ב-\( k - 1 \). מה זה אומר על \( P(k) \)?

??? tip "רמז 2"
    אם כל ערך הוא הממוצע של שני השכנים שלו, איך נראה הגרף? ולזמן : סמנו \( E(k) \), והוסיפו
    את המחזור שעבר.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **‏3/10.** הסיכוי להתמלא הוא \( P(3) = 3/10 \), הסיכוי להתרוקן \( 7/10 \), ובממוצע
        עוברים \( E(3) = 3 \cdot (10 - 3) = 21 \) מחזורים. באופן כללי \( P(k) = k/N \)
        ו-\( E(k) = k(N - k) \).

    <!-- cost: מתמלא 3/10 | מתרוקן 7/10 | מחזורים 21 -->

    #### הרעיון { .sol-idea }

    לא סופרים מסלולים. מגדירים \( P(k) \), הסיכוי להתמלא מ-\( k \), ומתנים על המחזור
    הראשון : בחצי מהמקרים ממשיכים מ-\( k + 1 \), ובחצי מ-\( k - 1 \). לכן כל ערך הוא הממוצע
    של שני השכנים שלו, והנקודות \( P(0), P(1), \dots, P(10) \) על קו ישר מ-0 ל-1. באותו אופן
    לזמן : \( E(k) \) הוא מחזור אחד ועוד הממוצע של השכנים, ולכן הגרף שלו פרבולה שיורדת ל-0
    בשני הקירות.

    <!-- gen 0 -->

    <div class="cw-fig"><svg class="perf-chart" viewBox="0 0 640 250" role="img" aria-label="שתי ריצות של המונה מ-3, עולה או יורד ב-1 בהסתברות חצי בכל מחזור. אחת מגיעה ל-10 אחרי 29 מחזורים, והשנייה ל-0 אחרי 11 מחזורים"><line class="grid" x1="46" x2="628" y1="214.0" y2="214.0"/><text class="tick" x="38" y="218.0" text-anchor="end">0</text><line class="grid" x1="46" x2="628" y1="174.4" y2="174.4"/><text class="tick" x="38" y="178.4" text-anchor="end">2</text><line class="grid" x1="46" x2="628" y1="134.8" y2="134.8"/><text class="tick" x="38" y="138.8" text-anchor="end">4</text><line class="grid" x1="46" x2="628" y1="95.2" y2="95.2"/><text class="tick" x="38" y="99.2" text-anchor="end">6</text><line class="grid" x1="46" x2="628" y1="55.6" y2="55.6"/><text class="tick" x="38" y="59.6" text-anchor="end">8</text><line class="grid" x1="46" x2="628" y1="16.0" y2="16.0"/><text class="tick" x="38" y="20.0" text-anchor="end">10</text><line class="s1-line" x1="46" x2="628" y1="16.0" y2="16.0" stroke-width="2" stroke-dasharray="6 4"/><text class="legend" x="52" y="10.0">N = 10</text><line class="s2-line" x1="46" x2="628" y1="214.0" y2="214.0" stroke-width="2" stroke-dasharray="6 4"/><polyline class="s1-line" points="46.0,154.6 66.1,134.8 86.1,154.6 106.2,174.4 126.3,154.6 146.3,134.8 166.4,115.0 186.5,134.8 206.6,154.6 226.6,134.8 246.7,115.0 266.8,134.8 286.8,115.0 306.9,134.8 327.0,115.0 347.0,95.2 367.1,115.0 387.2,95.2 407.2,115.0 427.3,134.8 447.4,115.0 467.4,95.2 487.5,115.0 507.6,134.8 527.7,115.0 547.7,95.2 567.8,75.4 587.9,55.6 607.9,35.8 628.0,16.0" fill="none" stroke-width="2.5"/><polyline class="s2-line" points="46.0,154.6 66.1,174.4 86.1,194.2 106.2,174.4 126.3,194.2 146.3,174.4 166.4,194.2 186.5,174.4 206.6,194.2 226.6,174.4 246.7,194.2 266.8,214.0" fill="none" stroke-width="2.5"/><circle class="ink-dot" cx="46.0" cy="154.6" r="4.5"></circle><text class="legend" x="68.0" y="158.6" text-anchor="middle">k = 3</text><circle class="s1-dot" cx="628.0" cy="16.0" r="4.5"></circle><circle class="s2-dot" cx="266.8" cy="214.0" r="4.5"></circle><text class="tick" x="46.0" y="232" text-anchor="middle">0</text><text class="tick" x="146.3" y="232" text-anchor="middle">5</text><text class="tick" x="246.7" y="232" text-anchor="middle">10</text><text class="tick" x="347.0" y="232" text-anchor="middle">15</text><text class="tick" x="447.4" y="232" text-anchor="middle">20</text><text class="tick" x="547.7" y="232" text-anchor="middle">25</text><line class="axis" x1="46" x2="628" y1="214" y2="214"/><text class="tick" x="38" y="232" text-anchor="end">t</text></svg></div>

    <span class="viz-legend"><span><i class="s1"></i><span>ריצה שהתמלאה, אחרי 29 מחזורים</span></span><span><i class="s2"></i><span>ריצה שהתרוקנה, אחרי 11 מחזורים</span></span><span><i class="ink"></i><span>ההתחלה, 3 credits</span></span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המשתנים :** \( P(k) \) הסיכוי להתמלא מ-\( k \), ו-\( E(k) \) מספר המחזורים הממוצע
       עד קיר.
    2. **הקירות :** \( P(0) = 0 \), \( P(10) = 1 \), ו-\( E(0) = E(10) = 0 \), כי שם הניסוי
       כבר נגמר.
    3. **הצעד הראשון :** לכל \( k \) מ-1 עד 9,
       \( P(k) = \tfrac12 P(k + 1) + \tfrac12 P(k - 1) \) ו-\( E(k) = 1 + \tfrac12 E(k + 1) + \tfrac12 E(k - 1) \).
    4. **הפתרון :** \( P(k) = k/10 \) ו-\( E(k) = k(10 - k) \). מ-3 : ‏\( 3/10 \), ‏\( 7/10 \)
       ו-21 מחזורים.

    </div>

    #### למה זה נכון { .sol-proof }

    **הניסוי נגמר.** מכל \( k \), עשרה מחזורים של עלייה ברצף מגיעים ל-10. לכן בכל קטע של
    עשרה מחזורים הניסוי נגמר בהסתברות לפחות \( 2^{-10} \), והסיכוי שהוא לא נגמר אחרי
    \( m \) קטעים קטן מ-\( (1 - 2^{-10})^m \), ששואף ל-0. מאותה סיבה גם הזמן הממוצע סופי.
    לכן \( P(k) \) ו-\( 1 - P(k) \) הם באמת הסיכויים להתמלא ולהתרוקן.

    **‏P קווי.** המשוואה \( P(k) = \tfrac12 P(k + 1) + \tfrac12 P(k - 1) \) שקולה ל-
    \( P(k + 1) - P(k) = P(k) - P(k - 1) \) : ההפרשים בין שכנים שווים, נניח \( d \). מ-0
    עד 10 יש עשרה הפרשים, ולכן \( 10d = P(10) - P(0) = 1 \), כלומר \( d = 1/10 \)
    ו-\( P(k) = k/10 \).

    **‏E פרבולה.** כאן המשוואה שקולה ל-
    \( E(k + 1) - E(k) = E(k) - E(k - 1) - 2 \) : כל הפרש קטן ב-2 מהקודם. אם ההפרש הראשון
    הוא \( E(1) - E(0) = c \), ההפרש ה-\( j \) הוא \( c - 2(j - 1) \). סכום עשרת ההפרשים
    הוא \( E(10) = 10c - 2 \cdot 45 = 0 \), ולכן \( c = 9 \), ו-
    \( E(k) = \sum_{j=1}^{k} \bigl(9 - 2(j - 1)\bigr) = 9k - k(k - 1) = k(10 - k) \).

    **דרך נוספת לראות את 3/10.** בכל מחזור המונה עולה או יורד ב-1 באותו סיכוי, ולכן הערך
    הממוצע שלו לא משתנה, גם בסוף : \( 3 = 10 \cdot P + 0 \cdot (1 - P) \), כלומר
    \( P = 3/10 \).

    <!-- gen 1 -->

    | ‏k | הסיכוי להתמלא | הסיכוי להתרוקן | מחזורים בממוצע |
    |:-:|:-:|:-:|:-:|
    | 1 | 1/10 | 9/10 | 9 |
    | 2 | 1/5 | 4/5 | 16 |
    | **3** | **3/10** | **7/10** | **21** |
    | 4 | 2/5 | 3/5 | 24 |
    | 5 | 1/2 | 1/2 | 25 |
    | 6 | 3/5 | 2/5 | 24 |
    | 7 | 7/10 | 3/10 | 21 |
    | 8 | 4/5 | 1/5 | 16 |
    | 9 | 9/10 | 1/10 | 9 |

    <!-- /gen -->

    **נסו בעצמכם.** "מחזור אחד" מזיז את המונה פעם אחת, "עד הקיר" מסיים את הריצה, ו-"100
    ריצות" מוסיף מאה ריצות לספירה. מימין הספירה מושווית לנוסחה, ובגרפים העקומות של
    \( P(k) \) ושל \( E(k) \) לכל נקודת התחלה :

    <div class="explorer" data-kind="creditwalk" data-mode="pq" data-a="0.5" data-n="10" data-k="3"></div>

    #### סיבוכיות { .sol-cost }

    החישוב ביד, בלי לולאות. בנוסחה \( P(k) = k/N \) ו-\( E(k) = k(N - k) \) לכל
    \( N \) ו-\( k \).

---

### סעיף ב – הטיה : p ו-q

עכשיו המונה עולה ב-1 בהסתברות \( p \) ויורד ב-1 בהסתברות \( q = 1 - p \), עם
\( p \ne q \).

1. מצאו נוסחה לסיכוי להתמלא, \( P(k) \), ולסיכוי להתרוקן.
2. מצאו נוסחה ל-\( E(k) \).
3. חשבו עבור \( p = 0.6 \), \( k = 3 \) ו-\( N = 10 \).
4. כתבו פונקציה שמחזירה את שלושת המספרים, והראו שהיא נותנת את סעיף א כש-\( p = q \).

??? tip "רמז 1"
    המשוואה היא \( P(k) = pP(k + 1) + qP(k - 1) \). נסו פתרון מהצורה \( x^k \). מה צריך
    לקיים \( x \)?

??? tip "רמז 2"
    ל-\( E(k) = 1 + pE(k + 1) + qE(k - 1) \) נחשו פתרון פרטי \( ck \), ואז הוסיפו את
    הפתרון של המשוואה בלי ה-1 והתאימו לקירות.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        עם \( \rho = q/p \) :
        \( P(k) = \dfrac{1 - \rho^k}{1 - \rho^N} \), הסיכוי להתרוקן \( 1 - P(k) \),
        ו-\( E(k) = \dfrac{k - N \cdot P(k)}{q - p} \). ב-\( p = 0.6 \) מ-3 : הסיכוי להתמלא
        \( 41553/58025 \approx 0.716 \), להתרוקן \( \approx 0.284 \), ובממוצע
        \( 48291/2321 \approx 20.81 \) מחזורים.

    <!-- cost: זמן \( O(\log N) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    אותה משוואת צעד ראשון, עם \( p \) ו-\( q \) במקום חצי. מציבים \( x^k \) ב-
    \( P(k) = pP(k + 1) + qP(k - 1) \) ומקבלים \( px^2 - x + q = 0 \), כלומר
    \( (x - 1)(px - q) = 0 \) : השורשים הם 1 ו-\( \rho = q/p \). כל פתרון הוא
    \( A + B\rho^k \), והקירות קובעים את \( A \) ואת \( B \). הטיה קטנה עושה הבדל גדול :
    ב-\( p = 0.6 \) הסיכוי להתמלא מ-3 קופץ מ-0.3 ל-0.716.

    <!-- gen 2 -->

    | ‏p | ‏q | הסיכוי להתמלא | הסיכוי להתרוקן | מחזורים בממוצע |
    |:-:|:-:|:-:|:-:|:-:|
    | 0.40 | 0.60 | 0.042 | 0.958 | 12.90 |
    | 0.45 | 0.55 | 0.128 | 0.872 | 17.17 |
    | 0.50 | 0.50 | 0.300 | 0.700 | 21.00 |
    | 0.55 | 0.45 | 0.523 | 0.477 | 22.25 |
    | **0.60** | **0.40** | **0.716** | **0.284** | **20.81** |
    | 0.70 | 0.30 | 0.921 | 0.079 | 15.54 |

    <!-- /gen -->

    <!-- gen 3 -->

    <div class="cw-fig"><svg class="perf-chart" viewBox="0 0 640 250" role="img" aria-label="הסיכוי להתמלא מכל נקודת התחלה k, מ-0 עד 10, בשלוש הסתברויות לעלות : 0.4, 0.5 ו-0.6. בחצי זה קו ישר, ובהטיה הקו מתעקם למעלה או למטה"><line class="grid" x1="46" x2="628" y1="214.0" y2="214.0"/><text class="tick" x="38" y="218.0" text-anchor="end">0</text><line class="grid" x1="46" x2="628" y1="164.5" y2="164.5"/><text class="tick" x="38" y="168.5" text-anchor="end">0.25</text><line class="grid" x1="46" x2="628" y1="115.0" y2="115.0"/><text class="tick" x="38" y="119.0" text-anchor="end">0.5</text><line class="grid" x1="46" x2="628" y1="65.5" y2="65.5"/><text class="tick" x="38" y="69.5" text-anchor="end">0.75</text><line class="grid" x1="46" x2="628" y1="16.0" y2="16.0"/><text class="tick" x="38" y="20.0" text-anchor="end">1</text><polyline class="s2-line" points="46.0,214.0 104.2,212.3 162.4,209.6 220.6,205.7 278.8,199.8 337.0,191.0 395.2,177.7 453.4,157.8 511.6,127.9 569.8,83.2 628.0,16.0" fill="none" stroke-width="2.5"/><circle class="s2-dot" cx="46.0" cy="214.0" r="3.5"></circle><circle class="s2-dot" cx="104.2" cy="212.3" r="3.5"></circle><circle class="s2-dot" cx="162.4" cy="209.6" r="3.5"></circle><circle class="s2-dot" cx="220.6" cy="205.7" r="3.5"></circle><circle class="s2-dot" cx="278.8" cy="199.8" r="3.5"></circle><circle class="s2-dot" cx="337.0" cy="191.0" r="3.5"></circle><circle class="s2-dot" cx="395.2" cy="177.7" r="3.5"></circle><circle class="s2-dot" cx="453.4" cy="157.8" r="3.5"></circle><circle class="s2-dot" cx="511.6" cy="127.9" r="3.5"></circle><circle class="s2-dot" cx="569.8" cy="83.2" r="3.5"></circle><circle class="s2-dot" cx="628.0" cy="16.0" r="3.5"></circle><polyline class="ink-line" points="46.0,214.0 104.2,194.2 162.4,174.4 220.6,154.6 278.8,134.8 337.0,115.0 395.2,95.2 453.4,75.4 511.6,55.6 569.8,35.8 628.0,16.0" fill="none" stroke-width="2.5"/><circle class="ink-dot" cx="46.0" cy="214.0" r="3.5"></circle><circle class="ink-dot" cx="104.2" cy="194.2" r="3.5"></circle><circle class="ink-dot" cx="162.4" cy="174.4" r="3.5"></circle><circle class="ink-dot" cx="220.6" cy="154.6" r="3.5"></circle><circle class="ink-dot" cx="278.8" cy="134.8" r="3.5"></circle><circle class="ink-dot" cx="337.0" cy="115.0" r="3.5"></circle><circle class="ink-dot" cx="395.2" cy="95.2" r="3.5"></circle><circle class="ink-dot" cx="453.4" cy="75.4" r="3.5"></circle><circle class="ink-dot" cx="511.6" cy="55.6" r="3.5"></circle><circle class="ink-dot" cx="569.8" cy="35.8" r="3.5"></circle><circle class="ink-dot" cx="628.0" cy="16.0" r="3.5"></circle><polyline class="s1-line" points="46.0,214.0 104.2,146.8 162.4,102.1 220.6,72.2 278.8,52.3 337.0,39.0 395.2,30.2 453.4,24.3 511.6,20.4 569.8,17.7 628.0,16.0" fill="none" stroke-width="2.5"/><circle class="s1-dot" cx="46.0" cy="214.0" r="3.5"></circle><circle class="s1-dot" cx="104.2" cy="146.8" r="3.5"></circle><circle class="s1-dot" cx="162.4" cy="102.1" r="3.5"></circle><circle class="s1-dot" cx="220.6" cy="72.2" r="3.5"></circle><circle class="s1-dot" cx="278.8" cy="52.3" r="3.5"></circle><circle class="s1-dot" cx="337.0" cy="39.0" r="3.5"></circle><circle class="s1-dot" cx="395.2" cy="30.2" r="3.5"></circle><circle class="s1-dot" cx="453.4" cy="24.3" r="3.5"></circle><circle class="s1-dot" cx="511.6" cy="20.4" r="3.5"></circle><circle class="s1-dot" cx="569.8" cy="17.7" r="3.5"></circle><circle class="s1-dot" cx="628.0" cy="16.0" r="3.5"></circle><line class="ink-line" x1="220.6" x2="220.6" y1="12" y2="214" stroke-width="1" stroke-dasharray="3 3"/><text class="tick" x="46.0" y="232" text-anchor="middle">0</text><text class="tick" x="104.2" y="232" text-anchor="middle">1</text><text class="tick" x="162.4" y="232" text-anchor="middle">2</text><text class="tick" x="220.6" y="232" text-anchor="middle">3</text><text class="tick" x="278.8" y="232" text-anchor="middle">4</text><text class="tick" x="337.0" y="232" text-anchor="middle">5</text><text class="tick" x="395.2" y="232" text-anchor="middle">6</text><text class="tick" x="453.4" y="232" text-anchor="middle">7</text><text class="tick" x="511.6" y="232" text-anchor="middle">8</text><text class="tick" x="569.8" y="232" text-anchor="middle">9</text><text class="tick" x="628.0" y="232" text-anchor="middle">10</text><line class="axis" x1="46" x2="628" y1="214" y2="214"/><text class="tick" x="38" y="232" text-anchor="end">k</text></svg></div>

    <span class="viz-legend"><span><i class="s1"></i><span>‏p = 0.6</span></span><span><i class="ink"></i><span>‏p = 0.5, הקו הישר k/N</span></span><span><i class="s2"></i><span>‏p = 0.4</span></span><span><i class="ink-dash"></i><span>ההתחלה k = 3</span></span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הקירות :** \( k = 0 \) ו-\( k = N \) מחזירים את התשובה מיד.
    2. **ההסתברויות בתזוזה :** \( a = p/(p + q) \) ו-\( b = q/(p + q) \). כאן \( q = 1 - p \),
       ולכן \( a = p \) ו-\( b = q \). בסעיף ג אותה פונקציה תטפל גם במחזורים בלי שינוי.
    3. **הוגן :** כש-\( a = b \), \( P = k/N \) ו-\( k(N - k) \) תזוזות.
    4. **מוטה :** \( \rho = b/a \), \( P = (1 - \rho^k)/(1 - \rho^N) \), ו-
       \( (k - N P)/(b - a) \) תזוזות.
    5. **הזמן :** מספר התזוזות חלקי \( p + q \), כאן 1.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="walk_odds" linenums="1" hl_lines="20 21 22"
        from fractions import Fraction


        def walk_odds(k, N, p, q):
            """The counter at k between the walls 0 and N moves +1 with probability p and -1 with
            q in a cycle, and stays with r = 1 - p - q. Returns (P(full: N first), P(empty: 0
            first), the expected cycles until a wall), exact when p and q are fractions."""
            p, q = Fraction(p), Fraction(q)
            s = p + q                                   # the chance of a move in a cycle
            if s == 0:
                raise ValueError("the counter never moves")
            if k <= 0:
                return Fraction(0), Fraction(1), Fraction(0)
            if k >= N:
                return Fraction(1), Fraction(0), Fraction(0)
            a, b = p / s, q / s                         # (1)!
            if a == b:
                full, moves = Fraction(k, N), Fraction(k * (N - k))      # (2)!
            elif a == 0:
                full, moves = Fraction(0), Fraction(k)
            else:
                rho = b / a
                full = (1 - rho ** k) / (1 - rho ** N)                    # (3)!
                moves = (k - N * full) / (b - a)                          # (4)!
            return full, 1 - full, moves / s                              # (5)!
        ```

        1. ההסתברות לעלות ולרדת **בתנאי** שהמונה זז. בסעיף הזה \( p + q = 1 \), ולכן זה
           אותו דבר.
        2. סעיף א. בלי הענף הזה הנוסחה המוטה מחלקת 0 ב-0.
        3. ‏\( A + B\rho^k \) עם \( P(0) = 0 \) ו-\( P(N) = 1 \).
        4. הפתרון הפרטי \( k/(b - a) \) ועוד \( A + B\rho^k \) שמתאפס בקירות.
        5. כל תזוזה לוקחת בממוצע \( 1/(p + q) \) מחזורים. כאן \( p + q = 1 \).

    === "SystemVerilog"
        ```systemverilog title="function automatic real p_full" linenums="1" hl_lines="11 12 23"
        // P(full: the counter reaches n before 0) from k, when it moves +1 with p and -1 with q
        // in a cycle and stays with 1 - p - q
        function automatic real p_full(int k, int n, real p, real q);
          real a, b, rho;
          if (k <= 0) return 0.0;
          if (k >= n) return 1.0;
          a = p / (p + q);                            // (1)!
          b = q / (p + q);
          if (a == b) return real'(k) / n;            // (2)!
          if (a == 0.0) return 0.0;
          rho = b / a;
          return (1.0 - rho ** k) / (1.0 - rho ** n);
        endfunction

        // the expected cycles until the counter reaches 0 or n
        function automatic real mean_cycles(int k, int n, real p, real q);
          real a, b, moves;
          if (k <= 0 || k >= n) return 0.0;
          a = p / (p + q);
          b = q / (p + q);
          if (a == b) moves = real'(k) * (n - k);
          else if (a == 0.0) moves = k;
          else moves = (k - n * p_full(k, n, p, q)) / (b - a);
          return moves / (p + q);                     // (3)!
        endfunction
        ```

        1. ההסתברויות בתנאי שהמונה זז, כמו ב-Python.
        2. ‏`real'(k) / n` ולא `k / n`, שהוא חילוק של שלמים ונותן 0.
        3. מספר התזוזות חלקי הסיכוי לזוז במחזור.

    #### למה זה נכון { .sol-proof }

    **הסיכוי להתמלא.** הפתרון הכללי של \( P(k) = pP(k + 1) + qP(k - 1) \) הוא
    \( A + B\rho^k \) (שני שורשים שונים, כי \( \rho \ne 1 \)). מ-\( P(0) = 0 \) :
    ‏\( B = -A \). מ-\( P(N) = 1 \) : ‏\( A(1 - \rho^N) = 1 \). לכן
    \( P(k) = (1 - \rho^k)/(1 - \rho^N) \). אין פתרון אחר : \( P(1) \) קובע את כל השאר
    דרך \( P(k + 1) = \bigl(P(k) - qP(k - 1)\bigr)/p \), ו-\( P(N) = 1 \) קובע את \( P(1) \).

    **הזמן.** \( E(k) = 1 + pE(k + 1) + qE(k - 1) \). הפתרון הפרטי \( k/(q - p) \) מקיים
    אותה : ‏\( p\tfrac{k + 1}{q - p} + q\tfrac{k - 1}{q - p} + 1 = \tfrac{k + p - q}{q - p} + 1
    = \tfrac{k}{q - p} \). מוסיפים \( A + B\rho^k \) ומתאימים לקירות :
    \( E(0) = 0 \) נותן \( B = -A \), ו-\( E(N) = 0 \) נותן
    \( E(k) = \dfrac{k}{q - p} - \dfrac{N}{q - p} \cdot \dfrac{1 - \rho^k}{1 - \rho^N}
    = \dfrac{k - N \cdot P(k)}{q - p} \).

    **המקרה ההוגן כגבול.** אם כותבים \( 1 - \rho^k = (1 - \rho)(1 + \rho + \dots + \rho^{k-1}) \),
    מקבלים \( P(k) = \dfrac{1 + \rho + \dots + \rho^{k-1}}{1 + \rho + \dots + \rho^{N-1}} \),
    וכש-\( \rho \to 1 \) זה \( k/N \). באותו אופן \( E(k) \to k(N - k) \). הנוסחה רציפה,
    אבל בקוד צריך ענף נפרד ל-\( a = b \), אחרת יש חילוק 0 ב-0.

    **מה רואים בטבלה.** הזמן הממוצע הארוך ביותר מ-3 הוא לא בהוגן : ב-\( p = 0.55 \) הוא
    22.25 מחזורים. הטיה קלה כלפי הקיר הרחוק מאריכה את הדרך, והטיה חזקה מקצרת אותה.

    #### סיבוכיות { .sol-cost }

    שתי חזקות, \( O(\log N) \) כפלים כל אחת, וזיכרון \( O(1) \). בשברים מדויקים גם גודל
    המספרים גדל עם \( N \).

---

### סעיף ג – מחזורים בלי שינוי : p, q ו-r

בכל מחזור המונה עולה ב-1 בהסתברות \( p \), יורד ב-1 בהסתברות \( q \), ונשאר בהסתברות
\( r = 1 - p - q \) (במחזור הזה לא הוחזר ולא נצרך credit).

1. הראו שהסיכוי להתמלא תלוי רק ב-\( p/(p + q) \), ושווה לזה של סעיף ב עם
   \( p' = p/(p + q) \).
2. הראו שהזמן הממוצע הוא הזמן של סעיף ב חלקי \( p + q \).
3. חשבו עבור \( p = 0.3 \), \( q = 0.2 \), \( r = 0.5 \), מ-3 עם \( N = 10 \).
4. כתבו פונקציה שפותרת את משוואות הצעד הראשון ישירות, בלי הנוסחה, ובדקו שהיא מסכימה.

??? tip "רמז 1"
    הסתכלו רק על המחזורים שבהם המונה זז. בתנאי שהוא זז, מה הסיכוי שהוא עולה?

??? tip "רמז 2"
    במשוואה \( E(k) = 1 + pE(k + 1) + rE(k) + qE(k - 1) \) העבירו את \( rE(k) \) לצד השני
    וחלקו ב-\( p + q \).

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        הסיכוי להתמלא הוא של סעיף ב עם \( p' = p/(p + q) \), והזמן הממוצע הוא הזמן של סעיף ב
        חלקי \( p + q \). ב-\( 0.3, 0.2, 0.5 \) : ‏\( p' = 0.6 \), אותו סיכוי של 0.716,
        והזמן \( 20.81 / 0.5 = 96582/2321 \approx 41.61 \) מחזורים.

    <!-- cost: זמן \( O(N) \) | זיכרון \( O(N) \) -->

    #### הרעיון { .sol-idea }

    מחזור שבו המונה נשאר לא משנה לאן הוא יגיע, רק מתי. אם מסתכלים רק על המחזורים שבהם הוא
    זז, כל תזוזה היא עלייה בהסתברות \( p/(p + q) \), בלי קשר למה שהיה קודם : זו בדיוק
    ההליכה של סעיף ב. בין תזוזה לתזוזה מחכים זמן גאומטרי עם ממוצע \( 1/(p + q) \), ולכן
    הזמן הממוצע מוכפל ב-\( 1/(p + q) \). בטבלה, שורות עם אותו \( p/(p + q) \) נותנות אותו
    סיכוי, והזמן גדל ככל ש-\( r \) גדל :

    <!-- gen 4 -->

    | ‏p | ‏q | ‏r | ‏p/(p + q) | הסיכוי להתמלא | מחזורים בממוצע |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | 0.60 | 0.40 | 0 | 0.60 | 0.716 | 20.81 |
    | **0.30** | **0.20** | **0.50** | **0.60** | **0.716** | **41.61** |
    | 0.12 | 0.08 | 0.80 | 0.60 | 0.716 | 104.03 |
    | 0.25 | 0.25 | 0.50 | 0.50 | 0.300 | 42.00 |
    | 0.10 | 0.10 | 0.80 | 0.50 | 0.300 | 105.00 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המשוואות :** \( P(k) = pP(k + 1) + rP(k) + qP(k - 1) \), ובזמן אותו דבר עם 1 נוסף.
    2. **ההרצה למעלה :** \( P(k + 1) = \bigl((p + q)P(k) - qP(k - 1)\bigr)/p \). מתחילים
       מ-\( P(0) = 0 \) ו-\( P(1) = x \) לא ידוע, וכל \( P(k) \) יוצא \( x \cdot u_k \).
    3. **הזמן :** \( E(0) = 0 \) ו-\( E(1) = y \), וכל \( E(k) \) יוצא \( y \cdot u_k + v_k \).
    4. **הקיר העליון :** \( P(N) = 1 \) נותן \( x = 1/u_N \), ו-\( E(N) = 0 \) נותן
       \( y = -v_N/u_N \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="by_recurrence" linenums="1" hl_lines="13 14 15 16"
        from fractions import Fraction


        def by_recurrence(N, p, q):
            """P(full) and the expected cycles from every start 0..N, from the first-step
            equations P(k) = p P(k+1) + r P(k) + q P(k-1) and E(k) = 1 + p E(k+1) + r E(k)
            + q E(k-1), without the closed form (p > 0): run the equations up from P(0) = 0,
            P(1) = x and E(0) = 0, E(1) = y, and fit x and y to the wall at N."""
            p, q = Fraction(p), Fraction(q)
            s = p + q
            u = [Fraction(0), Fraction(1)]              # P(k) = x * u[k]
            v = [Fraction(0), Fraction(0)]              # E(k) = y * u[k] + v[k]
            for k in range(1, N):
                u.append((s * u[k] - q * u[k - 1]) / p)                   # (1)!
                v.append((s * v[k] - q * v[k - 1] - 1) / p)               # (2)!
            x, y = 1 / u[N], -v[N] / u[N]                                 # (3)!
            return [x * u[k] for k in range(N + 1)], [y * u[k] + v[k] for k in range(N + 1)]
        ```

        1. מ-\( P(k) = pP(k + 1) + rP(k) + qP(k - 1) \) : מעבירים את \( rP(k) \), ו-
           \( p + q = 1 - r \).
        2. אותו דבר לזמן, עם ה-1 של המחזור.
        3. ‏\( P(N) = x \cdot u_N = 1 \) ו-\( E(N) = y \cdot u_N + v_N = 0 \).

    === "SystemVerilog"
        ```systemverilog title="function automatic void by_recurrence" linenums="1" hl_lines="13 14"
        // P(full) and the expected cycles from k, from the first-step equations without the
        // closed form (p > 0): P = x * u and E = y * u + v, run up from k = 0 and 1
        function automatic void by_recurrence(int k, int n, real p, real q,
                                              output real full, output real cycles);
          real u[], v[];
          real s, x, y;
          s = p + q;
          u = new[n + 1];
          v = new[n + 1];
          u[0] = 0.0; u[1] = 1.0;
          v[0] = 0.0; v[1] = 0.0;
          for (int j = 1; j < n; j++) begin
            u[j + 1] = (s * u[j] - q * u[j - 1]) / p;           // (1)!
            v[j + 1] = (s * v[j] - q * v[j - 1] - 1.0) / p;
          end
          x = 1.0 / u[n];
          y = -v[n] / u[n];
          full = x * u[k];
          cycles = y * u[k] + v[k];
        endfunction
        ```

        1. אותה הרצה של Python, במספרים ממשיים.

    #### למה זה נכון { .sol-proof }

    **הסיכוי.** מעבירים את \( rP(k) \) לצד השני :
    \( (1 - r)P(k) = pP(k + 1) + qP(k - 1) \), וכי \( 1 - r = p + q \), מחלקים ב-\( p + q \) :
    \( P(k) = p'P(k + 1) + q'P(k - 1) \) עם \( p' = p/(p + q) \) ו-\( q' = q/(p + q) \).
    זו המשוואה של סעיף ב עם אותם קירות, ולפתרון שלה רק \( p' \) חשוב.

    **הזמן.** \( (p + q)E(k) = 1 + pE(k + 1) + qE(k - 1) \). נסמן \( F(k) = (p + q)E(k) \),
    ואז \( F(k) = 1 + p'F(k + 1) + q'F(k - 1) \) עם \( F(0) = F(N) = 0 \) : ‏\( F \) הוא
    הזמן של סעיף ב עם \( p' \), ולכן \( E(k) = F(k)/(p + q) \).

    **ההרצה למעלה.** המשוואות לינאריות, והן קובעות את \( P(k + 1) \) מ-\( P(k) \)
    ומ-\( P(k - 1) \) כש-\( p > 0 \). לכן כל הפתרונות עם \( P(0) = 0 \) הם כפולות של
    \( u \), ו-\( u_N > 0 \) (כל \( u_k \) לפני \( N \) חיובי). כך `by_recurrence` מקבלת
    את אותם מספרים של `walk_odds`, בלי לנחש פתרון.

    #### סיבוכיות { .sol-cost }

    לולאה אחת על \( N \) ערכים : זמן \( O(N) \) וזיכרון \( O(N) \), והיא מחזירה את התשובה
    לכל נקודת התחלה בבת אחת.

---

### סעיף ד – זמנים גאומטריים : λ1 ו-λ2

המקבל מחזיר credit אחרי זמן **גאומטרי** עם פרמטר \( \lambda_1 \) : הסיכוי שההחזרה הבאה
תגיע בעוד בדיוק \( t \) מחזורים הוא \( \lambda_1 (1 - \lambda_1)^{t-1} \) (זו ההתפלגות
המעריכית הבדידה). השולח צורך credit אחרי זמן גאומטרי עם פרמטר \( \lambda_2 \), בלי תלות
בהחזרות. כשהחזרה וצריכה קורות באותו מחזור, המונה לא משתנה.

1. הראו שזה המודל של סעיף ג, ומצאו את \( p \), \( q \) ו-\( r \) לפי \( \lambda_1 \)
   ו-\( \lambda_2 \).
2. חשבו עבור \( \lambda_1 = 1/2 \) ו-\( \lambda_2 = 1/4 \), מ-3 עם \( N = 10 \).
3. מה קורה כש-\( \lambda_1 = \lambda_2 \)?
4. כתבו מונה credits בחומרה, ובדקו את הנוסחה בסימולציה.

??? tip "רמז 1"
    בהינתן שההחזרה עוד לא הגיעה עד עכשיו, מה הסיכוי שהיא תגיע במחזור הבא? האם זה תלוי
    בכמה זמן כבר חיכינו?

??? tip "רמז 2"
    בכל מחזור יש ארבע אפשרויות : החזרה בלבד, צריכה בלבד, שתיהן, אף אחת. מה כל אחת עושה
    למונה?

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        ‏\( p = \lambda_1 (1 - \lambda_2) \), \( q = \lambda_2 (1 - \lambda_1) \) ו-
        \( r = 1 - p - q \), ומכאן סעיף ג. ב-\( \lambda_1 = 1/2 \), \( \lambda_2 = 1/4 \) :
        ‏\( p = 3/8 \), \( q = 1/8 \), הסיכוי להתמלא \( 28431/29524 \approx 0.963 \),
        להתרוקן \( \approx 0.037 \), ובממוצע \( 195738/7381 \approx 26.52 \) מחזורים. כש-
        \( \lambda_1 = \lambda_2 = \lambda \) ההליכה הוגנת : \( P(k) = k/N \) ו-
        \( E(k) = k(N - k)/\bigl(2\lambda(1 - \lambda)\bigr) \).

    <!-- cost: זמן \( O(\log N) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    להתפלגות גאומטרית אין זיכרון : לא משנה כמה זמן כבר חיכינו, הסיכוי שההחזרה תגיע במחזור
    הבא הוא תמיד \( \lambda_1 \). לכן בכל מחזור יש החזרה בהסתברות \( \lambda_1 \) וצריכה
    בהסתברות \( \lambda_2 \), בלי קשר לעבר ובלי קשר זו לזו. המונה עולה כשיש החזרה בלי
    צריכה, יורד כשיש צריכה בלי החזרה, ונשאר בשני המקרים האחרים. זה בדיוק סעיף ג.

    <!-- gen 5 -->

    | ‏λ1 | ‏λ2 | ‏p | ‏q | ‏r | הסיכוי להתמלא | מחזורים בממוצע |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | **0.50** | **0.25** | **0.375** | **0.125** | **0.500** | **0.963** | **26.52** |
    | 0.40 | 0.50 | 0.200 | 0.300 | 0.500 | 0.042 | 25.81 |
    | 0.50 | 0.50 | 0.250 | 0.250 | 0.500 | 0.300 | 42.00 |
    | 0.10 | 0.10 | 0.090 | 0.090 | 0.820 | 0.300 | 116.67 |
    | 0.90 | 0.80 | 0.180 | 0.080 | 0.740 | 0.912 | 61.25 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ההמרה :** \( p = \lambda_1 (1 - \lambda_2) \) ו-\( q = \lambda_2 (1 - \lambda_1) \).
    2. **היחס :** \( \rho = q/p = \dfrac{\lambda_2 (1 - \lambda_1)}{\lambda_1 (1 - \lambda_2)} \),
       קטן מ-1 בדיוק כש-\( \lambda_1 > \lambda_2 \), כשה-credits חוזרים מהר יותר משהם נצרכים.
    3. **הנוסחה :** `walk_odds(k, N, p, q)` מסעיף ב, שמטפלת גם ב-\( r \).
    4. **הבדיקה :** סימולציה מחזור אחרי מחזור, ומונה credits בחומרה עם גירוי אקראי.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="simulate" linenums="1" hl_lines="20 21 22"
        import random


        def rates_to_steps(l1, l2):
            """Geometric waits: a credit comes back with probability l1 in a cycle and one is used
            with l2, independently. Returns (p, q) of the walk: up only, down only."""
            return l1 * (1 - l2), l2 * (1 - l1)


        def simulate(k, N, l1, l2, runs, seed=1):
            """Monte Carlo of the counter cycle by cycle: (share full, share empty, mean cycles)."""
            rnd = random.Random(seed)
            full = cycles = 0
            for _ in range(runs):
                c, t = k, 0
                while 0 < c < N:
                    back = rnd.random() < l1                # (1)!
                    used = rnd.random() < l2
                    c += back - used                        # (2)!
                    t += 1
                full += c == N
                cycles += t
            return full / runs, 1 - full / runs, cycles / runs
        ```

        1. שני אירועים בלתי תלויים בכל מחזור, כי לגאומטרית אין זיכרון.
        2. החזרה וצריכה באותו מחזור מבטלות זו את זו.

    === "SystemVerilog"
        ```systemverilog title="module credit_counter" linenums="1" hl_lines="14 15"
        // A credit counter between 0 (empty: the sender stalls) and N (full). After reset it
        // holds start; in a cycle a credit may come back (ret) and one may be used (take).
        module credit_counter #(parameter int N = 10) (
          input  logic                       clk, rst_n,
          input  logic [$clog2(N + 1) - 1:0] start,
          input  logic                       ret, take,
          output logic [$clog2(N + 1) - 1:0] count,
          output logic                       full, empty
        );
          assign full = count == N;
          assign empty = count == 0;
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) count <= start;
            else if (!full && !empty)                   // (1)!
              count <= count + ret - take;              // (2)!
        endmodule
        ```

        1. על הקירות הניסוי נגמר, והמונה לא זז עוד.
        2. ‏`ret` ו-`take` יחד : פלוס 1 ומינוס 1, בלי שינוי. בין הקירות אין גלישה.

    #### למה זה נכון { .sol-proof }

    **אין זיכרון.** אם \( T \) גאומטרי עם \( \lambda \), אז
    \( \Pr(T > t) = (1 - \lambda)^t \), ולכן
    \( \Pr(T = t + 1 \mid T > t) = \dfrac{\lambda (1 - \lambda)^t}{(1 - \lambda)^t} = \lambda \),
    בלי תלות ב-\( t \). אחרי כל החזרה מתחיל זמן המתנה חדש מאותה התפלגות, ולכן בכל מחזור,
    מה שלא קרה קודם, יש החזרה בהסתברות \( \lambda_1 \).

    **ארבע האפשרויות.** ההחזרות והצריכות בלתי תלויות, ולכן במחזור :
    החזרה בלבד \( \lambda_1 (1 - \lambda_2) = p \), צריכה בלבד
    \( \lambda_2 (1 - \lambda_1) = q \), ושתיהן או אף אחת
    \( \lambda_1 \lambda_2 + (1 - \lambda_1)(1 - \lambda_2) = r \). מכאן כל המספרים באים
    מסעיף ג.

    **כש-λ1 = λ2.** אז \( p = q = \lambda (1 - \lambda) \) : ההליכה הוגנת, הסיכוי להתמלא
    \( k/N \) כמו בסעיף א, והזמן \( k(N - k) \) חלקי \( p + q = 2\lambda(1 - \lambda) \).
    ב-\( \lambda = 1/2 \) זה \( 21/0.5 = 42 \) מחזורים.

    **הבדיקה בחומרה.** הבודק מאפס את `credit_counter` עם 3, מגריל בכל מחזור את `ret`
    ב-\( \lambda_1 \) ואת `take` ב-\( \lambda_2 \) עם `$urandom`, וסופר מחזורים עד `full`
    או `empty`. על אלפי ריצות השבר של `full` והזמן הממוצע קרובים לנוסחה בתוך ארבע סטיות
    תקן. בתיבה בוחרים \( \lambda_1 \) ו-\( \lambda_2 \) ומריצים :

    <div class="explorer" data-kind="creditwalk" data-mode="rates" data-a="0.5" data-b="0.25" data-n="10" data-k="3"></div>

    #### סיבוכיות { .sol-cost }

    הנוסחה \( O(\log N) \). סימולציה של \( R \) ריצות לוקחת \( R \cdot E(k) \) מחזורים
    בממוצע, והשגיאה שלה קטנה כמו \( 1/\sqrt{R} \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : חצי-חצי מכל מקום"
    ההליכה הוגנת, אבל מ-3 עם \( N = 10 \) הסיכוי להתמלא הוא 0.3 ולא חצי. מה שהוגן הוא
    הערך הממוצע של המונה, ולכן הסיכוי הוא המרחק היחסי מהקיר : \( k/N \).

??? trap "מלכודת : p = λ1 ו-q = λ2"
    השוואה ישירה שוכחת את המחזורים שבהם יש גם החזרה וגם צריכה. ב-\( \lambda_1 = 0.9 \)
    ו-\( \lambda_2 = 0.8 \) היא נותנת \( p + q = 1.7 \), שאינו הסתברות. הנכון :
    \( p = 0.18 \), \( q = 0.08 \) ו-\( r = 0.74 \).

??? trap "מלכודת : הנוסחה המוטה ב-p = q"
    ‏\( (1 - \rho^k)/(1 - \rho^N) \) ב-\( \rho = 1 \) היא 0 חלקי 0. הקוד בודק \( a = b \)
    לפני הנוסחה. במספרים ממשיים, \( p \) קרוב מאוד לחצי נותן ביטול של ספרות, ועדיף שם הצורה
    של הסכומים \( (1 + \rho + \dots + \rho^{k-1})/(1 + \dots + \rho^{N-1}) \).

??? trap "מלכודת : גלישה ב-ρ^N"
    כש-\( p < q \) ו-\( N \) גדול, \( \rho^N \) עובר את הטווח של `real`. מחלקים את המונה
    והמכנה ב-\( \rho^N \) : \( P(k) = (\rho^{-N} - \rho^{k-N})/(\rho^{-N} - 1) \), ושם כל
    החזקות קטנות מ-1.

??? followup "שאלות המשך"
    - **בלי קיר עליון :** מה קורה כש-\( N \to \infty \)?

        ??? fu-answer "תשובה"
            אם \( p \le q \), המונה מתרוקן בהסתברות 1. אם \( p > q \), \( \rho < 1 \),
            ו-\( \rho^N \to 0 \) : הסיכוי לא להתרוקן לעולם הוא \( 1 - (q/p)^k \). מ-3
            ב-\( p = 0.6 \) : \( 1 - (2/3)^3 = 19/27 \approx 0.70 \).

    - **קיר שמחזיר :** אם ב-\( N \) המונה פשוט נשאר (credit נוסף הולך לאיבוד), כמה מחזורים
      בממוצע עד שהוא מתרוקן, בהליכה ההוגנת?

        ??? fu-answer "תשובה"
            ‏\( E(k) = k(2N + 1 - k) \). ב-\( N \) המשוואה היא
            \( E(N) = 1 + \tfrac12 E(N) + \tfrac12 E(N - 1) \), ולכן ההפרש האחרון הוא 2,
            וכל הפרש לפניו גדול ב-2. מ-3 עם \( N = 10 \) : ‏54 מחזורים.

    - **התפלגות הזמן :** מה הסיכוי שבסעיף א הניסוי נגמר בתוך 21 מחזורים, הזמן הממוצע?

        ??? fu-answer "תשובה"
            בערך 0.65. מחשבים בתכנות דינמי על (מחזור, מצב) : מתחילים עם הסתברות 1 ב-3,
            מעבירים חצי לכל שכן בכל מחזור, וסוכמים את מה שהגיע לקירות. הזמן מוטה ימינה :
            רוב הריצות קצרות מהממוצע, ומעט ריצות ארוכות מושכות אותו למעלה.
