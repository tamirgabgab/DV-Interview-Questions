---
id: 83
title: כדי המים – למדוד 4 ליטר עם כד של 3 וכד של 5
level: student
difficulty: medium
kind: puzzle
tags: [logic-puzzles, bfs, number-theory, algorithms, python, systemverilog]
source: "חידה קלאסית; שלושת הכדים של 8, 5 ו-3 ליטר מיוחסים לטרטליה (המאה ה-16)"
added: 2026-11-05
---

## השאלה

יש שני כדים בלי שום סימון : כד **A** מחזיק בדיוק 3 ליטר, וכד **B** מחזיק בדיוק 5 ליטר. יש
ברז עם מים בלי הגבלה, וכיור. כל **צעד** הוא אחד משלושה :

- **מילוי :** ממלאים כד מהברז עד שהוא מלא.
- **ריקון :** שופכים את כל מה שבכד לכיור.
- **מזיגה :** מוזגים מכד אחד לשני, עד שהראשון ריק או שהשני מלא, מה שקורה קודם.

אין אפשרות לעצור באמצע מזיגה, כי אין על הכדים סימונים. המטרה : שבאחד הכדים יהיו
**בדיוק 4 ליטר**.

<!-- gen 0 -->

<svg class="figure wj-fig" viewBox="0 0 198 190" style="max-width:12.4rem" role="img" aria-label="שני כדים ריקים בלי סימונים : A מחזיק 3 ליטר ו-B מחזיק 5 ליטר"><line class="wj-lev" x1="12" x2="20" y1="122" y2="122"/><line class="wj-lev" x1="12" x2="20" y1="100" y2="100"/><path class="wj-jug" d="M12,78 L12,144 L76,144 L76,78"/><text class="wj-num" x="44.0" y="134" text-anchor="middle">0</text><text class="wj-name" x="44.0" y="164" text-anchor="middle">A</text><text class="wj-cap" x="44.0" y="182" text-anchor="middle" direction="rtl">3 ליטר</text><line class="wj-lev" x1="122" x2="130" y1="122" y2="122"/><line class="wj-lev" x1="122" x2="130" y1="100" y2="100"/><line class="wj-lev" x1="122" x2="130" y1="78" y2="78"/><line class="wj-lev" x1="122" x2="130" y1="56" y2="56"/><path class="wj-jug" d="M122,34 L122,144 L186,144 L186,34"/><text class="wj-num" x="154.0" y="134" text-anchor="middle">0</text><text class="wj-name" x="154.0" y="164" text-anchor="middle">B</text><text class="wj-cap" x="154.0" y="182" text-anchor="middle" direction="rtl">5 ליטר</text></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="wj-key-jug"></i>כד בלי סימונים, A של 3 ליטר ו-B של 5 ליטר</span><span><i class="wj-key-water"></i>מים, והמספר בתוך הכד הוא הכמות בליטרים</span></span>

<!-- /gen -->

??? interviewer "מה המראיין בודק"
    - **ניסוי מסודר :** האם המועמד רואה שמזיגה היא כלי מדידה ("מה שנשאר ב-B אחרי שמילאנו
      את A"), במקום לנחש צעדים.
    - **מינימליות :** האם הוא יודע להסביר למה אין דרך קצרה יותר, ולא רק להראות דרך אחת.
    - **הכללה :** מתי אפשר בכלל. האם הוא מגיע ל-gcd, ומוכיח את שני הכיוונים, גם "רק
      כפולות" וגם "כל הכפולות".
    - **מרחב מצבים :** האם הוא מתאר מצב כזוג כמויות, רואה גרף, ובוחר BFS למסלול הקצר.

---

### סעיף א – 4 ליטר

איך מגיעים ל-4 ליטר באחד הכדים? כמה צעדים צריך לכל הפחות?

??? tip "רמז 1"
    איזו כמות חדשה, לא 3 ולא 5, אפשר לייצר בשני צעדים?

??? tip "רמז 2"
    מילוי של B ומזיגה ממנו ל-A משאירים 2 ליטר ב-B. אם ה-2 האלה היו ב-A, כמה מקום היה
    נשאר בו?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שישה צעדים : ממלאים את B, מוזגים ממנו ל-A (ב-B נשארים 2), מרוקנים את A, מוזגים את
        ה-2 ל-A, ממלאים שוב את B, ומשלימים ממנו את A, שחסר בו ליטר אחד. ב-B נשארים 4.
        מי שמתחיל במילוי A מגיע ל-4 רק אחרי שמונה צעדים, ופחות משישה אי אפשר.

    <!-- cost: צעדים 6 | מצבים 16 -->

    #### הרעיון { .sol-idea }

    המזיגה היא כלי המדידה היחיד. מזיגה של B מלא לתוך A ריק משאירה ב-B בדיוק
    ‏\( 5 - 3 = 2 \) ליטר. כשה-2 האלה עוברים ל-A, נשאר ב-A מקום לליטר אחד בדיוק, ולכן
    מזיגה של B מלא לתוך A מוציאה מ-B ליטר אחד, ונשארים בו \( 5 - 1 = 4 \). בחשבון : מילאנו
    את B פעמיים ושפכנו את A פעמיים, \( 2 \cdot 5 - 2 \cdot 3 = 4 \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מילוי B :** ב-B יש 5.
    2. **מזיגה מ-B ל-A :** ‏A מתמלא ב-3, וב-B נשארים 2.
    3. **ריקון A :** ‏A ריק, וב-B עדיין 2.
    4. **מזיגה מ-B ל-A :** ה-2 עוברים ל-A, ו-B ריק.
    5. **מילוי B :** ב-B יש 5, וב-A יש 2.
    6. **מזיגה מ-B ל-A :** ב-A יש מקום לליטר אחד בלבד. הוא מתמלא, וב-B נשארים 4.

    </div>

    #### למה זה נכון { .sol-proof }

    **צעד אחרי צעד.** לחצו "הבא" כדי לעקוב אחרי הכמות בכל כד :

    <!-- gen 2 -->

    <div class="stepper" role="group" aria-label="ששת הצעדים שמביאים 4 ליטר לכד B, צעד אחרי צעד" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure wj-fig" viewBox="0 0 198 190" style="max-width:12.4rem" role="img" aria-label="התחלה"><line class="wj-lev" x1="12" x2="20" y1="122" y2="122"/><line class="wj-lev" x1="12" x2="20" y1="100" y2="100"/><path class="wj-jug" d="M12,78 L12,144 L76,144 L76,78"/><text class="wj-num" x="44.0" y="134" text-anchor="middle">0</text><text class="wj-name" x="44.0" y="164" text-anchor="middle">A</text><text class="wj-cap" x="44.0" y="182" text-anchor="middle" direction="rtl">3 ליטר</text><line class="wj-lev" x1="122" x2="130" y1="122" y2="122"/><line class="wj-lev" x1="122" x2="130" y1="100" y2="100"/><line class="wj-lev" x1="122" x2="130" y1="78" y2="78"/><line class="wj-lev" x1="122" x2="130" y1="56" y2="56"/><path class="wj-jug" d="M122,34 L122,144 L186,144 L186,34"/><text class="wj-num" x="154.0" y="134" text-anchor="middle">0</text><text class="wj-name" x="154.0" y="164" text-anchor="middle">B</text><text class="wj-cap" x="154.0" y="182" text-anchor="middle" direction="rtl">5 ליטר</text></svg><figcaption>התחלה : שני הכדים ריקים.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 198 190" style="max-width:12.4rem" role="img" aria-label="צעד 1"><line class="wj-lev" x1="12" x2="20" y1="122" y2="122"/><line class="wj-lev" x1="12" x2="20" y1="100" y2="100"/><path class="wj-jug" d="M12,78 L12,144 L76,144 L76,78"/><text class="wj-num" x="44.0" y="134" text-anchor="middle">0</text><text class="wj-name" x="44.0" y="164" text-anchor="middle">A</text><text class="wj-cap" x="44.0" y="182" text-anchor="middle" direction="rtl">3 ליטר</text><rect class="wj-water" x="125" y="34" width="58" height="110"/><line class="wj-lev" x1="122" x2="130" y1="122" y2="122"/><line class="wj-lev" x1="122" x2="130" y1="100" y2="100"/><line class="wj-lev" x1="122" x2="130" y1="78" y2="78"/><line class="wj-lev" x1="122" x2="130" y1="56" y2="56"/><path class="wj-jug wj-chg" d="M122,34 L122,144 L186,144 L186,34"/><text class="wj-num" x="154.0" y="94.0" text-anchor="middle">5</text><text class="wj-name" x="154.0" y="164" text-anchor="middle">B</text><text class="wj-cap" x="154.0" y="182" text-anchor="middle" direction="rtl">5 ליטר</text></svg><figcaption>צעד 1 : ממלאים את B מהברז. ב-A יש 0, וב-B יש 5.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 198 190" style="max-width:12.4rem" role="img" aria-label="צעד 2"><rect class="wj-water" x="15" y="78" width="58" height="66"/><line class="wj-lev" x1="12" x2="20" y1="122" y2="122"/><line class="wj-lev" x1="12" x2="20" y1="100" y2="100"/><path class="wj-jug wj-chg" d="M12,78 L12,144 L76,144 L76,78"/><text class="wj-num" x="44.0" y="116.0" text-anchor="middle">3</text><text class="wj-name" x="44.0" y="164" text-anchor="middle">A</text><text class="wj-cap" x="44.0" y="182" text-anchor="middle" direction="rtl">3 ליטר</text><rect class="wj-water" x="125" y="100" width="58" height="44"/><line class="wj-lev" x1="122" x2="130" y1="122" y2="122"/><line class="wj-lev" x1="122" x2="130" y1="100" y2="100"/><line class="wj-lev" x1="122" x2="130" y1="78" y2="78"/><line class="wj-lev" x1="122" x2="130" y1="56" y2="56"/><path class="wj-jug wj-chg" d="M122,34 L122,144 L186,144 L186,34"/><text class="wj-num" x="154.0" y="127.0" text-anchor="middle">2</text><text class="wj-name" x="154.0" y="164" text-anchor="middle">B</text><text class="wj-cap" x="154.0" y="182" text-anchor="middle" direction="rtl">5 ליטר</text><path class="wj-arrow" d="M154.0,30 Q99.0,6 52.0,68"/><polygon class="wj-head" points="47.0,61 57.0,61 52.0,70"/></svg><figcaption>צעד 2 : מוזגים מ-B ל-A, עד ש-A מלא. ב-A יש 3, וב-B יש 2.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 198 190" style="max-width:12.4rem" role="img" aria-label="צעד 3"><line class="wj-lev" x1="12" x2="20" y1="122" y2="122"/><line class="wj-lev" x1="12" x2="20" y1="100" y2="100"/><path class="wj-jug wj-chg" d="M12,78 L12,144 L76,144 L76,78"/><text class="wj-num" x="44.0" y="134" text-anchor="middle">0</text><text class="wj-name" x="44.0" y="164" text-anchor="middle">A</text><text class="wj-cap" x="44.0" y="182" text-anchor="middle" direction="rtl">3 ליטר</text><rect class="wj-water" x="125" y="100" width="58" height="44"/><line class="wj-lev" x1="122" x2="130" y1="122" y2="122"/><line class="wj-lev" x1="122" x2="130" y1="100" y2="100"/><line class="wj-lev" x1="122" x2="130" y1="78" y2="78"/><line class="wj-lev" x1="122" x2="130" y1="56" y2="56"/><path class="wj-jug" d="M122,34 L122,144 L186,144 L186,34"/><text class="wj-num" x="154.0" y="127.0" text-anchor="middle">2</text><text class="wj-name" x="154.0" y="164" text-anchor="middle">B</text><text class="wj-cap" x="154.0" y="182" text-anchor="middle" direction="rtl">5 ליטר</text></svg><figcaption>צעד 3 : שופכים את A לכיור. ב-A יש 0, וב-B יש 2.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 198 190" style="max-width:12.4rem" role="img" aria-label="צעד 4"><rect class="wj-water" x="15" y="100" width="58" height="44"/><line class="wj-lev" x1="12" x2="20" y1="122" y2="122"/><line class="wj-lev" x1="12" x2="20" y1="100" y2="100"/><path class="wj-jug wj-chg" d="M12,78 L12,144 L76,144 L76,78"/><text class="wj-num" x="44.0" y="127.0" text-anchor="middle">2</text><text class="wj-name" x="44.0" y="164" text-anchor="middle">A</text><text class="wj-cap" x="44.0" y="182" text-anchor="middle" direction="rtl">3 ליטר</text><line class="wj-lev" x1="122" x2="130" y1="122" y2="122"/><line class="wj-lev" x1="122" x2="130" y1="100" y2="100"/><line class="wj-lev" x1="122" x2="130" y1="78" y2="78"/><line class="wj-lev" x1="122" x2="130" y1="56" y2="56"/><path class="wj-jug wj-chg" d="M122,34 L122,144 L186,144 L186,34"/><text class="wj-num" x="154.0" y="134" text-anchor="middle">0</text><text class="wj-name" x="154.0" y="164" text-anchor="middle">B</text><text class="wj-cap" x="154.0" y="182" text-anchor="middle" direction="rtl">5 ליטר</text><path class="wj-arrow" d="M154.0,30 Q99.0,6 52.0,68"/><polygon class="wj-head" points="47.0,61 57.0,61 52.0,70"/></svg><figcaption>צעד 4 : מוזגים מ-B ל-A, עד ש-B ריק. ב-A יש 2, וב-B יש 0.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 198 190" style="max-width:12.4rem" role="img" aria-label="צעד 5"><rect class="wj-water" x="15" y="100" width="58" height="44"/><line class="wj-lev" x1="12" x2="20" y1="122" y2="122"/><line class="wj-lev" x1="12" x2="20" y1="100" y2="100"/><path class="wj-jug" d="M12,78 L12,144 L76,144 L76,78"/><text class="wj-num" x="44.0" y="127.0" text-anchor="middle">2</text><text class="wj-name" x="44.0" y="164" text-anchor="middle">A</text><text class="wj-cap" x="44.0" y="182" text-anchor="middle" direction="rtl">3 ליטר</text><rect class="wj-water" x="125" y="34" width="58" height="110"/><line class="wj-lev" x1="122" x2="130" y1="122" y2="122"/><line class="wj-lev" x1="122" x2="130" y1="100" y2="100"/><line class="wj-lev" x1="122" x2="130" y1="78" y2="78"/><line class="wj-lev" x1="122" x2="130" y1="56" y2="56"/><path class="wj-jug wj-chg" d="M122,34 L122,144 L186,144 L186,34"/><text class="wj-num" x="154.0" y="94.0" text-anchor="middle">5</text><text class="wj-name" x="154.0" y="164" text-anchor="middle">B</text><text class="wj-cap" x="154.0" y="182" text-anchor="middle" direction="rtl">5 ליטר</text></svg><figcaption>צעד 5 : ממלאים את B מהברז. ב-A יש 2, וב-B יש 5.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 198 190" style="max-width:12.4rem" role="img" aria-label="צעד 6"><rect class="wj-water" x="15" y="78" width="58" height="66"/><line class="wj-lev" x1="12" x2="20" y1="122" y2="122"/><line class="wj-lev" x1="12" x2="20" y1="100" y2="100"/><path class="wj-jug wj-chg" d="M12,78 L12,144 L76,144 L76,78"/><text class="wj-num" x="44.0" y="116.0" text-anchor="middle">3</text><text class="wj-name" x="44.0" y="164" text-anchor="middle">A</text><text class="wj-cap" x="44.0" y="182" text-anchor="middle" direction="rtl">3 ליטר</text><rect class="wj-water" x="125" y="56" width="58" height="88"/><line class="wj-lev" x1="122" x2="130" y1="122" y2="122"/><line class="wj-lev" x1="122" x2="130" y1="100" y2="100"/><line class="wj-lev" x1="122" x2="130" y1="78" y2="78"/><line class="wj-lev" x1="122" x2="130" y1="56" y2="56"/><path class="wj-jug wj-chg" d="M122,34 L122,144 L186,144 L186,34"/><text class="wj-num" x="154.0" y="105.0" text-anchor="middle">4</text><text class="wj-name" x="154.0" y="164" text-anchor="middle">B</text><text class="wj-cap" x="154.0" y="182" text-anchor="middle" direction="rtl">5 ליטר</text><path class="wj-arrow" d="M154.0,30 Q99.0,6 52.0,68"/><polygon class="wj-head" points="47.0,61 57.0,61 52.0,70"/></svg><figcaption>צעד 6 : מוזגים מ-B ל-A, עד ש-A מלא. ב-A יש 3, וב-B יש 4. <strong>ב-B יש 4 ליטר.</strong></figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="7"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <!-- /gen -->

    <!-- gen 3 -->

    | צעד | הפעולה | ‏B | ‏A |
    |:-:|---|:-:|:-:|
    | 1 | מילוי B | 5 | 0 |
    | 2 | מזיגה מ-B ל-A | 2 | 3 |
    | 3 | ריקון A | 2 | 0 |
    | 4 | מזיגה מ-B ל-A | 0 | 2 |
    | 5 | מילוי B | 5 | 2 |
    | 6 | מזיגה מ-B ל-A | 4 | 3 |

    <!-- /gen -->

    **הדרך השנייה.** מי שמתחיל במילוי A וממשיך לשפוך את A לתוך B, כל פעם ש-B מתמלא
    מרוקנים אותו, מגיע ל-4 בתוך B, אבל רק אחרי שמונה צעדים. כאן מילאנו את A שלוש פעמים
    ושפכנו את B פעם אחת : \( 3 \cdot 3 - 5 = 4 \).

    <!-- gen 4 -->

    | צעד | הפעולה | ‏B | ‏A |
    |:-:|---|:-:|:-:|
    | 1 | מילוי A | 0 | 3 |
    | 2 | מזיגה מ-A ל-B | 3 | 0 |
    | 3 | מילוי A | 3 | 3 |
    | 4 | מזיגה מ-A ל-B | 5 | 1 |
    | 5 | ריקון B | 0 | 1 |
    | 6 | מזיגה מ-A ל-B | 1 | 0 |
    | 7 | מילוי A | 1 | 3 |
    | 8 | מזיגה מ-A ל-B | 4 | 0 |

    <!-- /gen -->

    **למה לא פחות משישה.** חיפוש לרוחב (BFS) רושם את כל המצבים שמגיעים אליהם בצעד אחד, אחר
    כך את המצבים החדשים שמגיעים אליהם בשני צעדים, וכן הלאה. כל זוג בטבלה הוא הכמות ב-A
    והכמות ב-B, משמאל לימין כמו בציור :

    <!-- gen 5 -->

    | צעדים | מצבים חדשים, כזוגות <span dir="ltr">(A, B)</span> | כמה |
    |:-:|---|:-:|
    | 0 | ‏<span dir="ltr">(0, 0)</span> | 1 |
    | 1 | ‏<span dir="ltr">(3, 0), (0, 5)</span> | 2 |
    | 2 | ‏<span dir="ltr">(3, 5), (0, 3), (3, 2)</span> | 3 |
    | 3 | ‏<span dir="ltr">(3, 3), (0, 2)</span> | 2 |
    | 4 | ‏<span dir="ltr">(1, 5), (2, 0)</span> | 2 |
    | 5 | ‏<span dir="ltr">(1, 0), (2, 5)</span> | 2 |
    | 6 | ‏<span dir="ltr">(0, 1), <strong>(3, 4)</strong></span> | 2 |
    | 7 | ‏<span dir="ltr">(3, 1), <strong>(0, 4)</strong></span> | 2 |

    <!-- /gen -->

    יש 16 מצבים בסך הכול, ואחרי שבעה צעדים אין מצב חדש (סעיף ב מסביר למה רק הם). מצב עם 4
    ליטר מופיע לראשונה בשורה 6, ולכן חמישה צעדים לא מספיקים. יש רק מסלול אחד של שישה
    צעדים אליו : זה שלמעלה.

    #### סיבוכיות { .sol-cost }

    שישה צעדים, ומרחב של 16 מצבים נגישים בלבד : מספיק קטן כדי לעבור על כולו ביד, כמו
    בטבלה שלמעלה.

---

### סעיף ב – כל a, b ו-T

עכשיו הכדים מחזיקים \( a \) ו-\( b \) ליטר, והמטרה היא \( T \) ליטר באחד מהם.

1. מתי אפשר בכלל? הוכיחו.
2. כתבו פונקציה שמחזירה את רשימת הצעדים הקצרה ביותר, או שאין דרך.

??? tip "רמז 1"
    נניח ש-\( a = 4 \) ו-\( b = 6 \). אילו כמויות יכולות בכלל להופיע בכד? מה המשותף לכל
    הצעדים?

??? tip "רמז 2"
    תארו מצב כזוג \( (x, y) \), הכמויות ב-A וב-B. מכל מצב יש לכל היותר שישה צעדים, וכל
    צעד עולה אחד. איזה חיפוש מוצא את המסלול הקצר?

??? tip "רמז 3"
    לכיוון השני של ההוכחה : ממלאים רק את A, שופכים אותו לתוך B, ומרוקנים את B כשהוא מלא.
    מה יש ב-B אחרי שמזגנו בסך הכול \( k \) כדים של A, כל עוד B לא יצא מלא בדיוק?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        אפשר אם ורק אם \( T \le \max(a, b) \) ו-\( T \) מתחלק ב-\( \gcd(a, b) \). כל צעד
        משאיר בכל כד כפולה של \( \gcd \), ולהפך, מילוי חוזר של A ושפיכה לתוך B מייצרים
        ב-B כל כפולה של \( \gcd \). את הדרך הקצרה מוצא **BFS** על הזוגות \( (x, y) \), עם
        שישה צעדים מכל זוג.

    <!-- cost: זמן \( O(ab) \) | זיכרון \( O(ab) \) -->

    #### הרעיון { .sol-idea }

    **המצב.** הזוג \( (x, y) \) : כמה יש ב-A וכמה ב-B. ההתחלה \( (0, 0) \), ויש לכל
    היותר \( (a + 1)(b + 1) \) זוגות. כל צעד מעביר מזוג לזוג, ולכן התוכנית היא מסלול
    בגרף, והתוכנית הקצרה היא המסלול הקצר. כל הקשתות שוות, ולכן BFS.

    **מה מגיעים אליו.** אחרי כל צעד אחד הכדים ריק או מלא : מילוי וריקון קובעים כד אחד,
    ומזיגה נגמרת כשהראשון ריק או שהשני מלא. לכן כל המצבים הנגישים יושבים על שפת הרשת. ב-3
    ו-5 יש \( (3 + 1) \cdot (5 + 1) = 24 \) זוגות, ומהם 16 על השפה. כולם נגישים, 16 מתוך
    24, ו-8 המצבים שבפנים לא נגישים לעולם :

    <!-- gen 6 -->

    <svg class="perf-chart" viewBox="0 0 244 244" style="max-width:15.2rem" role="img" aria-label="מרחב המצבים של שני הכדים : A לרוחב מ-0 עד 3, B לגובה מ-0 עד 5. 16 מצבים נגישים, כולם על השפה, ו-8 המצבים שבפנים לא נגישים. המסלול של 6 צעדים והמסלול של 8 צעדים מסומנים"><line class="grid" x1="67.5" x2="67.5" y1="6" y2="212"/><text class="tick" x="67.5" y="230" text-anchor="middle">0</text><line class="grid" x1="114.5" x2="114.5" y1="6" y2="212"/><text class="tick" x="114.5" y="230" text-anchor="middle">1</text><line class="grid" x1="161.5" x2="161.5" y1="6" y2="212"/><text class="tick" x="161.5" y="230" text-anchor="middle">2</text><line class="grid" x1="208.5" x2="208.5" y1="6" y2="212"/><text class="tick" x="208.5" y="230" text-anchor="middle">3</text><line class="grid" x1="44" x2="232" y1="195.3" y2="195.3"/><text class="tick" x="36" y="199.3" text-anchor="end">0</text><line class="grid" x1="44" x2="232" y1="162.0" y2="162.0"/><text class="tick" x="36" y="166.0" text-anchor="end">1</text><line class="grid" x1="44" x2="232" y1="128.7" y2="128.7"/><text class="tick" x="36" y="132.7" text-anchor="end">2</text><line class="grid" x1="44" x2="232" y1="95.3" y2="95.3"/><text class="tick" x="36" y="99.3" text-anchor="end">3</text><line class="grid" x1="44" x2="232" y1="62.0" y2="62.0"/><text class="tick" x="36" y="66.0" text-anchor="end">4</text><line class="grid" x1="44" x2="232" y1="28.7" y2="28.7"/><text class="tick" x="36" y="32.7" text-anchor="end">5</text><line class="axis" x1="44" x2="232" y1="212" y2="212"/><text class="tick" x="232.0" y="242.0" text-anchor="end">A</text><text class="tick" x="34.0" y="22.0" text-anchor="end">B</text><polyline class="wj-route is-alt" points="67.5,195.3 208.5,195.3 67.5,95.3 208.5,95.3 114.5,28.7 114.5,195.3 67.5,162.0 208.5,162.0 67.5,62.0" fill="none" stroke-width="2.5" stroke-dasharray="6 5"/><polyline class="wj-route" points="67.5,195.3 67.5,28.7 208.5,128.7 67.5,128.7 161.5,195.3 161.5,28.7 208.5,62.0" fill="none" stroke-width="3"/><circle class="wj-reach" cx="67.5" cy="195.3" r="6.5"><title>A = 0, B = 0</title></circle><circle class="wj-reach" cx="67.5" cy="162.0" r="6.5"><title>A = 0, B = 1</title></circle><circle class="wj-reach" cx="67.5" cy="128.7" r="6.5"><title>A = 0, B = 2</title></circle><circle class="wj-reach" cx="67.5" cy="95.3" r="6.5"><title>A = 0, B = 3</title></circle><circle class="wj-goal" cx="67.5" cy="62.0" r="6.5"><title>A = 0, B = 4</title></circle><circle class="wj-reach" cx="67.5" cy="28.7" r="6.5"><title>A = 0, B = 5</title></circle><circle class="wj-reach" cx="114.5" cy="195.3" r="6.5"><title>A = 1, B = 0</title></circle><circle class="wj-never" cx="114.5" cy="162.0" r="4.5"><title>A = 1, B = 1 : לא מגיעים</title></circle><circle class="wj-never" cx="114.5" cy="128.7" r="4.5"><title>A = 1, B = 2 : לא מגיעים</title></circle><circle class="wj-never" cx="114.5" cy="95.3" r="4.5"><title>A = 1, B = 3 : לא מגיעים</title></circle><circle class="wj-never" cx="114.5" cy="62.0" r="4.5"><title>A = 1, B = 4 : לא מגיעים</title></circle><circle class="wj-reach" cx="114.5" cy="28.7" r="6.5"><title>A = 1, B = 5</title></circle><circle class="wj-reach" cx="161.5" cy="195.3" r="6.5"><title>A = 2, B = 0</title></circle><circle class="wj-never" cx="161.5" cy="162.0" r="4.5"><title>A = 2, B = 1 : לא מגיעים</title></circle><circle class="wj-never" cx="161.5" cy="128.7" r="4.5"><title>A = 2, B = 2 : לא מגיעים</title></circle><circle class="wj-never" cx="161.5" cy="95.3" r="4.5"><title>A = 2, B = 3 : לא מגיעים</title></circle><circle class="wj-never" cx="161.5" cy="62.0" r="4.5"><title>A = 2, B = 4 : לא מגיעים</title></circle><circle class="wj-reach" cx="161.5" cy="28.7" r="6.5"><title>A = 2, B = 5</title></circle><circle class="wj-reach" cx="208.5" cy="195.3" r="6.5"><title>A = 3, B = 0</title></circle><circle class="wj-reach" cx="208.5" cy="162.0" r="6.5"><title>A = 3, B = 1</title></circle><circle class="wj-reach" cx="208.5" cy="128.7" r="6.5"><title>A = 3, B = 2</title></circle><circle class="wj-reach" cx="208.5" cy="95.3" r="6.5"><title>A = 3, B = 3</title></circle><circle class="wj-goal" cx="208.5" cy="62.0" r="6.5"><title>A = 3, B = 4</title></circle><circle class="wj-reach" cx="208.5" cy="28.7" r="6.5"><title>A = 3, B = 5</title></circle></svg>

    <!-- /gen -->

    <!-- gen 7 -->

    <span class="viz-legend"><span><i class="wj-key-reach"></i>מצב שמגיעים אליו</span><span><i class="wj-key-goal"></i>מצב עם 4 ליטר</span><span><i class="wj-key-never"></i>מצב שלא מגיעים אליו לעולם</span><span><i class="wj-key-best"></i>6 הצעדים, מתחילים במילוי B</span><span><i class="wj-key-alt"></i>8 הצעדים, מתחילים במילוי A</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **בדיקה מראש, לא חובה :** אם \( T > \max(a, b) \) או ש-\( T \) לא מתחלק
       ב-\( \gcd(a, b) \), אין דרך, ו-`can_measure` עונה על זה בלי חיפוש. `jugs_shortest`
       לא קוראת לה : החיפוש עובר על כל המצבים הנגישים, לא מוצא, ומחזיר `None`.
    2. **תור והורים :** מכניסים את \( (0, 0) \) לתור, ורושמים שאין לו הורה.
    3. **הוצאה :** מוציאים זוג. אם באחד הכדים יש \( T \), סיימנו.
    4. **הרחבה :** מחשבים את ששת הצעדים : מילוי A או B, ריקון A או B, ומזיגה לכל כיוון.
       צעד שלא משנה כלום נזרק (ממצב נגיש נשארים לכל היותר ארבעה). כל זוג חדש מקבל הורה
       ואת שם הצעד, ונכנס לתור.
    5. **שחזור :** מהזוג שנמצא הולכים אחורה לפי ההורים, ואז הופכים את הסדר.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="jugs_shortest" linenums="1" hl_lines="7 13 30 38"
        from collections import deque
        from math import gcd


        def can_measure(a, b, t):
            """t litres in one of the jugs: no more than the bigger jug, and a multiple of gcd(a, b)."""
            return 0 <= t <= max(a, b) and t % gcd(a, b) == 0


        def jug_steps(a, b, x, y):
            """Every state one step from (x, y), with its step: fill, empty, or pour until the
            first jug is empty or the second is full."""
            ab = min(x, b - y)                                   # (1)!
            ba = min(y, a - x)
            for step, nxt in ((("fill", "A"), (a, y)), (("fill", "B"), (x, b)),
                              (("empty", "A"), (0, y)), (("empty", "B"), (x, 0)),
                              (("pour", "A", "B"), (x - ab, y + ab)),
                              (("pour", "B", "A"), (x + ba, y - ba))):
                if nxt != (x, y):
                    yield step, nxt


        def jugs_shortest(a, b, t):
            """The fewest steps from two empty jugs to t litres in one of them:
            [(step, x, y), ...] with the contents after each step, or None."""
            parent = {(0, 0): None}
            queue = deque([(0, 0)])
            while queue:
                s = queue.popleft()
                if t in s:                                       # (2)!
                    plan = []
                    while parent[s] is not None:
                        prev, step = parent[s]
                        plan.append((step, *s))
                        s = prev
                    return plan[::-1]
                for step, nxt in jug_steps(a, b, *s):
                    if nxt not in parent:                        # (3)!
                        parent[nxt] = (s, step)
                        queue.append(nxt)
            return None
        ```

        1. כמה עובר במזיגה : כל מה שיש ב-A, או המקום שנשאר ב-B, הקטן מביניהם.
        2. ‏BFS מוציא את הזוגות לפי מרחק עולה מההתחלה, ולכן הזוג הראשון עם \( T \) הוא הקרוב
           ביותר.
        3. זוג שכבר נראה, נראה במרחק קטן או שווה. אין טעם להכניס אותו שוב.

    === "SystemVerilog"
        ```systemverilog title="function automatic int jugs_shortest" linenums="1" hl_lines="13 26 27 30"
        // The fewest steps from two empty jugs to t litres in one of them, or -1. plan lists the
        // steps, e.g. "fill B, pour B A, empty A, pour B A, fill B, pour B A".
        function automatic int jugs_shortest(int a, int b, int t, output string plan);
          int parent[int], depth[int];              // keyed by x * (b + 1) + y
          string took[int];
          int queue[$];
          int s, x, y, nx, ny, d, key;
          string name;
          plan = "";
          depth[0] = 0; parent[0] = -1;
          queue.push_back(0);
          while (queue.size() > 0) begin
            s = queue.pop_front();                 // (1)!
            x = s / (b + 1); y = s % (b + 1);
            if (x == t || y == t) begin
              for (int c = s; parent[c] >= 0; c = parent[c])
                plan = (plan == "") ? took[c] : {took[c], ", ", plan};
              return depth[s];
            end
            for (int k = 0; k < 6; k++) begin
              case (k)
                0: begin nx = a; ny = y; name = "fill A"; end
                1: begin nx = x; ny = b; name = "fill B"; end
                2: begin nx = 0; ny = y; name = "empty A"; end
                3: begin nx = x; ny = 0; name = "empty B"; end
                4: begin d = (x < b - y) ? x : b - y; nx = x - d; ny = y + d; name = "pour A B"; end
                default: begin d = (y < a - x) ? y : a - x; nx = x + d; ny = y - d; name = "pour B A"; end
              endcase
              key = nx * (b + 1) + ny;             // (2)!
              if (key == s || depth.exists(key)) continue;
              depth[key] = depth[s] + 1; parent[key] = s; took[key] = name;
              queue.push_back(key);
            end
          end
          return -1;
        endfunction
        ```

        1. התור מחזיק מפתחות : זוג \( (x, y) \) נשמר כמספר אחד, \( x \cdot (b + 1) + y \).
        2. אותם ששה צעדים ובאותו סדר כמו ב-Python, ולכן גם אותה תוכנית.

    #### למה זה נכון { .sol-proof }

    **רק כפולות של gcd.** נסמן \( g = \gcd(a, b) \). בהתחלה בשני הכדים יש 0. מילוי משאיר
    בכד \( a \) או \( b \), וריקון משאיר 0, וכולם כפולות של \( g \). מזיגה לא משנה את הסכום
    \( x + y \), ואחריה אחד הכדים ריק (והשני מחזיק את הסכום) או מלא (והשני מחזיק את הסכום
    פחות \( a \) או \( b \)). לכן אם לפני הצעד שני הכדים היו כפולות של \( g \), גם אחריו.
    בנוסף, אין כד שמחזיק יותר מ-\( \max(a, b) \). לכן \( T \) חייב להיות כפולה של \( g \),
    ולא יותר מהכד הגדול.

    **כל הכפולות.** נניח \( a \le b \). ממלאים רק את A, שופכים אותו לתוך B, ומרוקנים את B
    בכל פעם שהוא מתמלא. אחרי שמזגנו בסך הכול \( k \) כדים של A, לכל \( k < b/g \), ב-B יש
    \( k \cdot a \bmod b \) (מה שלא נשפך לכיור). ל-\( k \) גדול יותר זה כבר לא תמיד נכון : ב-3
    ו-5, אחרי חמישה כדים B מלא, 5 ולא 0. כש-\( k \) עובר על \( 0, 1, \dots, b/g - 1 \), השארית
    \( k \cdot a \bmod b \) עוברת על **כל** הכפולות של \( g \) שקטנות מ-\( b \) : אם שתיים היו
    שוות, \( b \) היה מחלק את \( (k_1 - k_2) \cdot a \), כלומר \( b/g \) מחלק את \( k_1 - k_2 \),
    וזה בלתי אפשרי כש-\( |k_1 - k_2| < b/g \). את \( T = b \) מקבלים במילוי אחד. זה הכיוון
    השני של הזהות של Bézout : כל כפולה של \( g \) היא \( u \cdot a - v \cdot b \). הבנייה
    גם נותנת את המקדמים : \( u = k \) הוא מספר המילויים של A, ו-\( v \) הוא מספר הריקונים של
    B. בדרך השנייה של סעיף א, \( u = 3 \) ו-\( v = 1 \).

    **הקצר ביותר.** ‏BFS מבקר בזוגות לפי מרחק עולה מ-\( (0, 0) \), ולכן הזוג הראשון שבו יש
    \( T \) נמצא דרך מסלול באורך מינימלי. הטבלה בודקת את כל זה על כמה דוגמאות :

    <!-- gen 8 -->

    | ‏a | ‏b | ‏T | ‏gcd | אפשר? | הכי מעט צעדים | למה |
    |:-:|:-:|:-:|:-:|:-:|:-:|---|
    | 3 | 5 | 4 | 1 | כן | 6 | כפולה של 1, ולא יותר מ-5 |
    | 3 | 5 | 1 | 1 | כן | 4 | כפולה של 1, ולא יותר מ-5 |
    | 3 | 5 | 2 | 1 | כן | 2 | כפולה של 1, ולא יותר מ-5 |
    | 4 | 6 | 2 | 2 | כן | 2 | כפולה של 2, ולא יותר מ-6 |
    | 4 | 6 | 3 | 2 | לא | ‏– | לא כפולה של 2 |
    | 6 | 10 | 8 | 2 | כן | 6 | כפולה של 2, ולא יותר מ-10 |
    | 7 | 11 | 6 | 1 | כן | 10 | כפולה של 1, ולא יותר מ-11 |
    | 3 | 5 | 7 | 1 | לא | ‏– | יותר מהכד הגדול, 5 |

    <!-- /gen -->

    **נסו בעצמכם.** שלוש משימות :

    - **שתי הדרכים :** פתרו ביד את 3, 5 ו-4 ליטר, פעם במילוי B תחילה (6 צעדים) ופעם במילוי
      A תחילה (8). על הרשת אלה שני קווים שונים לאורך השפה.
    - **כשאי אפשר :** קבעו \( a = 4 \), \( b = 6 \) ו-\( T = 3 \). רק 10 מתוך 35 הזוגות
      נגישים, בכולם הכמויות זוגיות, והתיבה אומרת למה אי אפשר. עם \( T = 2 \) מספיקים שני
      צעדים.
    - **מרחב גדול יותר :** קבעו \( a = 7 \), \( b = 11 \) ו-\( T = 6 \), ולחצו "הדרך
      הקצרה" : 10 צעדים, ו-36 מתוך 96 הזוגות נגישים. עם \( a = b = 5 \) נגישים רק 4.

    מה שאין באיורים : הסימון "מרחק BFS" כותב בכל מצב נגיש בכמה צעדים מגיעים אליו, לכל
    \( a \) ו-\( b \). ב-3 ו-5 אלה המספרים של הטבלה בסעיף א.

    <div class="explorer" data-kind="jugs" data-a="3" data-b="5" data-t="4"></div>

    #### סיבוכיות { .sol-cost }

    לכל היותר \( (a + 1)(b + 1) \) זוגות. בפועל נגישים רק מצבי השפה שבהם שתי הכמויות
    כפולות של \( g = \gcd(a, b) \), ומספרם בדיוק \( 2(a + b)/g \) : ב-3 ו-5,
    \( 2 \cdot 8 / 1 = 16 \). מכל זוג לכל היותר שישה צעדים, ולכן הזמן והזיכרון \( O(ab) \)
    בחסם הפשוט, ו-\( O(a + b) \) בפועל.

---

### סעיף ג – שלושה כדים, בלי ברז

הפעם אין ברז ואין כיור. יש שלושה כדים של 8, 5 ו-3 ליטר. הכד של 8 מלא, ושני האחרים ריקים.
מותר רק למזוג מכד לכד, ושוב עד שהראשון ריק או שהשני מלא. איך מחלקים את 8 הליטרים
לשני חצאים של 4, בכד של 8 ובכד של 5? כמה מזיגות צריך לכל הפחות?

??? tip "רמז 1"
    כמות המים הכוללת לא משתנה. כמה מספרים צריך כדי לתאר מצב?

??? tip "רמז 2"
    כמה מצבים בכלל נגישים? ציירו אותם על רשת, כמו בסעיף ב.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        שבע מזיגות : מ-8 ל-5, מ-5 ל-3, מ-3 ל-8, מ-5 ל-3, מ-8 ל-5, מ-5 ל-3 ומ-3 ל-8. בסוף
        יש 4 בכד של 8 ו-4 בכד של 5. מי שמתחיל במזיגה מ-8 ל-3 צריך שמונה, ופחות משבע אי
        אפשר.

    <!-- cost: מזיגות 7 | מצבים 16 -->

    #### הרעיון { .sol-idea }

    **שני מספרים מספיקים.** הסכום תמיד 8, ולכן הכמויות בכד של 5 ובכד של 3 קובעות את המצב.
    יש 24 זוגות כאלה, ושוב רק מצבי השפה נגישים, 16 מתוך 24. הסיבה כמו בסעיף ב : כל מזיגה
    משאירה כד אחד ריק או מלא. אם זה הכד של 5 או של 3, המצב על השפה. אם זה הכד של 8 : כשהוא
    מלא שני האחרים ריקים, וכשהוא ריק שניהם מלאים, ושני המצבים האלה הם פינות של הרשת.

    **אותו חיפוש.** מכל מצב יש לכל היותר שש מזיגות, אחת לכל זוג סדור של כדים. BFS מהמצב
    שבו הכד של 8 מלא מוצא את המסלול הקצר למצב שבו בכד של 8 ובכד של 5 יש 4.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מ-8 ל-5 :** נשארים <span dir="ltr">3, 5, 0</span> (משמאל לימין כמו בציור : הכדים
       של 8, 5 ו-3).
    2. **מ-5 ל-3 :** נשארים <span dir="ltr">3, 2, 3</span>.
    3. **מ-3 ל-8 :** נשארים <span dir="ltr">6, 2, 0</span>.
    4. **מ-5 ל-3 :** נשארים <span dir="ltr">6, 0, 2</span>.
    5. **מ-8 ל-5 :** נשארים <span dir="ltr">1, 5, 2</span>.
    6. **מ-5 ל-3 :** הכד של 3 צריך רק ליטר אחד, ונשארים <span dir="ltr">1, 4, 3</span>.
    7. **מ-3 ל-8 :** נשארים <span dir="ltr">4, 4, 0</span>.

    </div>

    <!-- gen 9 -->

    <div class="stepper" role="group" aria-label="שבע המזיגות שמחלקות 8 ליטר לשני חצאים של 4, מזיגה אחרי מזיגה" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure wj-fig" viewBox="0 0 308 200" style="max-width:19.2rem" role="img" aria-label="התחלה"><rect class="wj-water" x="15" y="34" width="58" height="120"/><line class="wj-lev" x1="12" x2="20" y1="139" y2="139"/><line class="wj-lev" x1="12" x2="20" y1="124" y2="124"/><line class="wj-lev" x1="12" x2="20" y1="109" y2="109"/><line class="wj-lev" x1="12" x2="20" y1="94" y2="94"/><line class="wj-lev" x1="12" x2="20" y1="79" y2="79"/><line class="wj-lev" x1="12" x2="20" y1="64" y2="64"/><line class="wj-lev" x1="12" x2="20" y1="49" y2="49"/><path class="wj-jug" d="M12,34 L12,154 L76,154 L76,34"/><text class="wj-num" x="44.0" y="99.0" text-anchor="middle">8</text><text class="wj-cap" x="44.0" y="176" text-anchor="middle" direction="rtl">8 ליטר</text><line class="wj-lev" x1="122" x2="130" y1="139" y2="139"/><line class="wj-lev" x1="122" x2="130" y1="124" y2="124"/><line class="wj-lev" x1="122" x2="130" y1="109" y2="109"/><line class="wj-lev" x1="122" x2="130" y1="94" y2="94"/><path class="wj-jug" d="M122,79 L122,154 L186,154 L186,79"/><text class="wj-num" x="154.0" y="144" text-anchor="middle">0</text><text class="wj-cap" x="154.0" y="176" text-anchor="middle" direction="rtl">5 ליטר</text><line class="wj-lev" x1="232" x2="240" y1="139" y2="139"/><line class="wj-lev" x1="232" x2="240" y1="124" y2="124"/><path class="wj-jug" d="M232,109 L232,154 L296,154 L296,109"/><text class="wj-num" x="264.0" y="144" text-anchor="middle">0</text><text class="wj-cap" x="264.0" y="176" text-anchor="middle" direction="rtl">3 ליטר</text></svg><figcaption>התחלה : הכד של 8 מלא, ושני האחרים ריקים.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 308 200" style="max-width:19.2rem" role="img" aria-label="צעד 1"><rect class="wj-water" x="15" y="109" width="58" height="45"/><line class="wj-lev" x1="12" x2="20" y1="139" y2="139"/><line class="wj-lev" x1="12" x2="20" y1="124" y2="124"/><line class="wj-lev" x1="12" x2="20" y1="109" y2="109"/><line class="wj-lev" x1="12" x2="20" y1="94" y2="94"/><line class="wj-lev" x1="12" x2="20" y1="79" y2="79"/><line class="wj-lev" x1="12" x2="20" y1="64" y2="64"/><line class="wj-lev" x1="12" x2="20" y1="49" y2="49"/><path class="wj-jug wj-chg" d="M12,34 L12,154 L76,154 L76,34"/><text class="wj-num" x="44.0" y="136.5" text-anchor="middle">3</text><text class="wj-cap" x="44.0" y="176" text-anchor="middle" direction="rtl">8 ליטר</text><rect class="wj-water" x="125" y="79" width="58" height="75"/><line class="wj-lev" x1="122" x2="130" y1="139" y2="139"/><line class="wj-lev" x1="122" x2="130" y1="124" y2="124"/><line class="wj-lev" x1="122" x2="130" y1="109" y2="109"/><line class="wj-lev" x1="122" x2="130" y1="94" y2="94"/><path class="wj-jug wj-chg" d="M122,79 L122,154 L186,154 L186,79"/><text class="wj-num" x="154.0" y="121.5" text-anchor="middle">5</text><text class="wj-cap" x="154.0" y="176" text-anchor="middle" direction="rtl">5 ליטר</text><line class="wj-lev" x1="232" x2="240" y1="139" y2="139"/><line class="wj-lev" x1="232" x2="240" y1="124" y2="124"/><path class="wj-jug" d="M232,109 L232,154 L296,154 L296,109"/><text class="wj-num" x="264.0" y="144" text-anchor="middle">0</text><text class="wj-cap" x="264.0" y="176" text-anchor="middle" direction="rtl">3 ליטר</text><path class="wj-arrow" d="M44.0,30 Q99.0,6 146.0,69"/><polygon class="wj-head" points="141.0,62 151.0,62 146.0,71"/></svg><figcaption>מזיגה 1 : מוזגים מהכד של 8 לכד של 5, עד שהכד של 5 מלא. בכדים של 8, 5 ו-3 : 3, 5 ו-0.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 308 200" style="max-width:19.2rem" role="img" aria-label="צעד 2"><rect class="wj-water" x="15" y="109" width="58" height="45"/><line class="wj-lev" x1="12" x2="20" y1="139" y2="139"/><line class="wj-lev" x1="12" x2="20" y1="124" y2="124"/><line class="wj-lev" x1="12" x2="20" y1="109" y2="109"/><line class="wj-lev" x1="12" x2="20" y1="94" y2="94"/><line class="wj-lev" x1="12" x2="20" y1="79" y2="79"/><line class="wj-lev" x1="12" x2="20" y1="64" y2="64"/><line class="wj-lev" x1="12" x2="20" y1="49" y2="49"/><path class="wj-jug" d="M12,34 L12,154 L76,154 L76,34"/><text class="wj-num" x="44.0" y="136.5" text-anchor="middle">3</text><text class="wj-cap" x="44.0" y="176" text-anchor="middle" direction="rtl">8 ליטר</text><rect class="wj-water" x="125" y="124" width="58" height="30"/><line class="wj-lev" x1="122" x2="130" y1="139" y2="139"/><line class="wj-lev" x1="122" x2="130" y1="124" y2="124"/><line class="wj-lev" x1="122" x2="130" y1="109" y2="109"/><line class="wj-lev" x1="122" x2="130" y1="94" y2="94"/><path class="wj-jug wj-chg" d="M122,79 L122,154 L186,154 L186,79"/><text class="wj-num" x="154.0" y="144.0" text-anchor="middle">2</text><text class="wj-cap" x="154.0" y="176" text-anchor="middle" direction="rtl">5 ליטר</text><rect class="wj-water" x="235" y="109" width="58" height="45"/><line class="wj-lev" x1="232" x2="240" y1="139" y2="139"/><line class="wj-lev" x1="232" x2="240" y1="124" y2="124"/><path class="wj-jug wj-chg" d="M232,109 L232,154 L296,154 L296,109"/><text class="wj-num" x="264.0" y="136.5" text-anchor="middle">3</text><text class="wj-cap" x="264.0" y="176" text-anchor="middle" direction="rtl">3 ליטר</text><path class="wj-arrow" d="M154.0,75 Q209.0,6 256.0,99"/><polygon class="wj-head" points="251.0,92 261.0,92 256.0,101"/></svg><figcaption>מזיגה 2 : מוזגים מהכד של 5 לכד של 3, עד שהכד של 3 מלא. בכדים של 8, 5 ו-3 : 3, 2 ו-3.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 308 200" style="max-width:19.2rem" role="img" aria-label="צעד 3"><rect class="wj-water" x="15" y="64" width="58" height="90"/><line class="wj-lev" x1="12" x2="20" y1="139" y2="139"/><line class="wj-lev" x1="12" x2="20" y1="124" y2="124"/><line class="wj-lev" x1="12" x2="20" y1="109" y2="109"/><line class="wj-lev" x1="12" x2="20" y1="94" y2="94"/><line class="wj-lev" x1="12" x2="20" y1="79" y2="79"/><line class="wj-lev" x1="12" x2="20" y1="64" y2="64"/><line class="wj-lev" x1="12" x2="20" y1="49" y2="49"/><path class="wj-jug wj-chg" d="M12,34 L12,154 L76,154 L76,34"/><text class="wj-num" x="44.0" y="114.0" text-anchor="middle">6</text><text class="wj-cap" x="44.0" y="176" text-anchor="middle" direction="rtl">8 ליטר</text><rect class="wj-water" x="125" y="124" width="58" height="30"/><line class="wj-lev" x1="122" x2="130" y1="139" y2="139"/><line class="wj-lev" x1="122" x2="130" y1="124" y2="124"/><line class="wj-lev" x1="122" x2="130" y1="109" y2="109"/><line class="wj-lev" x1="122" x2="130" y1="94" y2="94"/><path class="wj-jug" d="M122,79 L122,154 L186,154 L186,79"/><text class="wj-num" x="154.0" y="144.0" text-anchor="middle">2</text><text class="wj-cap" x="154.0" y="176" text-anchor="middle" direction="rtl">5 ליטר</text><line class="wj-lev" x1="232" x2="240" y1="139" y2="139"/><line class="wj-lev" x1="232" x2="240" y1="124" y2="124"/><path class="wj-jug wj-chg" d="M232,109 L232,154 L296,154 L296,109"/><text class="wj-num" x="264.0" y="144" text-anchor="middle">0</text><text class="wj-cap" x="264.0" y="176" text-anchor="middle" direction="rtl">3 ליטר</text><path class="wj-arrow" d="M264.0,105 Q154.0,6 52.0,24"/><polygon class="wj-head" points="47.0,17 57.0,17 52.0,26"/></svg><figcaption>מזיגה 3 : מוזגים מהכד של 3 לכד של 8, עד שהכד של 3 ריק. בכדים של 8, 5 ו-3 : 6, 2 ו-0.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 308 200" style="max-width:19.2rem" role="img" aria-label="צעד 4"><rect class="wj-water" x="15" y="64" width="58" height="90"/><line class="wj-lev" x1="12" x2="20" y1="139" y2="139"/><line class="wj-lev" x1="12" x2="20" y1="124" y2="124"/><line class="wj-lev" x1="12" x2="20" y1="109" y2="109"/><line class="wj-lev" x1="12" x2="20" y1="94" y2="94"/><line class="wj-lev" x1="12" x2="20" y1="79" y2="79"/><line class="wj-lev" x1="12" x2="20" y1="64" y2="64"/><line class="wj-lev" x1="12" x2="20" y1="49" y2="49"/><path class="wj-jug" d="M12,34 L12,154 L76,154 L76,34"/><text class="wj-num" x="44.0" y="114.0" text-anchor="middle">6</text><text class="wj-cap" x="44.0" y="176" text-anchor="middle" direction="rtl">8 ליטר</text><line class="wj-lev" x1="122" x2="130" y1="139" y2="139"/><line class="wj-lev" x1="122" x2="130" y1="124" y2="124"/><line class="wj-lev" x1="122" x2="130" y1="109" y2="109"/><line class="wj-lev" x1="122" x2="130" y1="94" y2="94"/><path class="wj-jug wj-chg" d="M122,79 L122,154 L186,154 L186,79"/><text class="wj-num" x="154.0" y="144" text-anchor="middle">0</text><text class="wj-cap" x="154.0" y="176" text-anchor="middle" direction="rtl">5 ליטר</text><rect class="wj-water" x="235" y="124" width="58" height="30"/><line class="wj-lev" x1="232" x2="240" y1="139" y2="139"/><line class="wj-lev" x1="232" x2="240" y1="124" y2="124"/><path class="wj-jug wj-chg" d="M232,109 L232,154 L296,154 L296,109"/><text class="wj-num" x="264.0" y="144.0" text-anchor="middle">2</text><text class="wj-cap" x="264.0" y="176" text-anchor="middle" direction="rtl">3 ליטר</text><path class="wj-arrow" d="M154.0,75 Q209.0,6 256.0,99"/><polygon class="wj-head" points="251.0,92 261.0,92 256.0,101"/></svg><figcaption>מזיגה 4 : מוזגים מהכד של 5 לכד של 3, עד שהכד של 5 ריק. בכדים של 8, 5 ו-3 : 6, 0 ו-2.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 308 200" style="max-width:19.2rem" role="img" aria-label="צעד 5"><rect class="wj-water" x="15" y="139" width="58" height="15"/><line class="wj-lev" x1="12" x2="20" y1="139" y2="139"/><line class="wj-lev" x1="12" x2="20" y1="124" y2="124"/><line class="wj-lev" x1="12" x2="20" y1="109" y2="109"/><line class="wj-lev" x1="12" x2="20" y1="94" y2="94"/><line class="wj-lev" x1="12" x2="20" y1="79" y2="79"/><line class="wj-lev" x1="12" x2="20" y1="64" y2="64"/><line class="wj-lev" x1="12" x2="20" y1="49" y2="49"/><path class="wj-jug wj-chg" d="M12,34 L12,154 L76,154 L76,34"/><text class="wj-num" x="44.0" y="151.5" text-anchor="middle">1</text><text class="wj-cap" x="44.0" y="176" text-anchor="middle" direction="rtl">8 ליטר</text><rect class="wj-water" x="125" y="79" width="58" height="75"/><line class="wj-lev" x1="122" x2="130" y1="139" y2="139"/><line class="wj-lev" x1="122" x2="130" y1="124" y2="124"/><line class="wj-lev" x1="122" x2="130" y1="109" y2="109"/><line class="wj-lev" x1="122" x2="130" y1="94" y2="94"/><path class="wj-jug wj-chg" d="M122,79 L122,154 L186,154 L186,79"/><text class="wj-num" x="154.0" y="121.5" text-anchor="middle">5</text><text class="wj-cap" x="154.0" y="176" text-anchor="middle" direction="rtl">5 ליטר</text><rect class="wj-water" x="235" y="124" width="58" height="30"/><line class="wj-lev" x1="232" x2="240" y1="139" y2="139"/><line class="wj-lev" x1="232" x2="240" y1="124" y2="124"/><path class="wj-jug" d="M232,109 L232,154 L296,154 L296,109"/><text class="wj-num" x="264.0" y="144.0" text-anchor="middle">2</text><text class="wj-cap" x="264.0" y="176" text-anchor="middle" direction="rtl">3 ליטר</text><path class="wj-arrow" d="M44.0,30 Q99.0,6 146.0,69"/><polygon class="wj-head" points="141.0,62 151.0,62 146.0,71"/></svg><figcaption>מזיגה 5 : מוזגים מהכד של 8 לכד של 5, עד שהכד של 5 מלא. בכדים של 8, 5 ו-3 : 1, 5 ו-2.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 308 200" style="max-width:19.2rem" role="img" aria-label="צעד 6"><rect class="wj-water" x="15" y="139" width="58" height="15"/><line class="wj-lev" x1="12" x2="20" y1="139" y2="139"/><line class="wj-lev" x1="12" x2="20" y1="124" y2="124"/><line class="wj-lev" x1="12" x2="20" y1="109" y2="109"/><line class="wj-lev" x1="12" x2="20" y1="94" y2="94"/><line class="wj-lev" x1="12" x2="20" y1="79" y2="79"/><line class="wj-lev" x1="12" x2="20" y1="64" y2="64"/><line class="wj-lev" x1="12" x2="20" y1="49" y2="49"/><path class="wj-jug" d="M12,34 L12,154 L76,154 L76,34"/><text class="wj-num" x="44.0" y="151.5" text-anchor="middle">1</text><text class="wj-cap" x="44.0" y="176" text-anchor="middle" direction="rtl">8 ליטר</text><rect class="wj-water" x="125" y="94" width="58" height="60"/><line class="wj-lev" x1="122" x2="130" y1="139" y2="139"/><line class="wj-lev" x1="122" x2="130" y1="124" y2="124"/><line class="wj-lev" x1="122" x2="130" y1="109" y2="109"/><line class="wj-lev" x1="122" x2="130" y1="94" y2="94"/><path class="wj-jug wj-chg" d="M122,79 L122,154 L186,154 L186,79"/><text class="wj-num" x="154.0" y="129.0" text-anchor="middle">4</text><text class="wj-cap" x="154.0" y="176" text-anchor="middle" direction="rtl">5 ליטר</text><rect class="wj-water" x="235" y="109" width="58" height="45"/><line class="wj-lev" x1="232" x2="240" y1="139" y2="139"/><line class="wj-lev" x1="232" x2="240" y1="124" y2="124"/><path class="wj-jug wj-chg" d="M232,109 L232,154 L296,154 L296,109"/><text class="wj-num" x="264.0" y="136.5" text-anchor="middle">3</text><text class="wj-cap" x="264.0" y="176" text-anchor="middle" direction="rtl">3 ליטר</text><path class="wj-arrow" d="M154.0,75 Q209.0,6 256.0,99"/><polygon class="wj-head" points="251.0,92 261.0,92 256.0,101"/></svg><figcaption>מזיגה 6 : מוזגים מהכד של 5 לכד של 3, עד שהכד של 3 מלא. בכדים של 8, 5 ו-3 : 1, 4 ו-3.</figcaption></figure><figure class="stepper-frame"><svg class="figure wj-fig" viewBox="0 0 308 200" style="max-width:19.2rem" role="img" aria-label="צעד 7"><rect class="wj-water" x="15" y="94" width="58" height="60"/><line class="wj-lev" x1="12" x2="20" y1="139" y2="139"/><line class="wj-lev" x1="12" x2="20" y1="124" y2="124"/><line class="wj-lev" x1="12" x2="20" y1="109" y2="109"/><line class="wj-lev" x1="12" x2="20" y1="94" y2="94"/><line class="wj-lev" x1="12" x2="20" y1="79" y2="79"/><line class="wj-lev" x1="12" x2="20" y1="64" y2="64"/><line class="wj-lev" x1="12" x2="20" y1="49" y2="49"/><path class="wj-jug wj-chg" d="M12,34 L12,154 L76,154 L76,34"/><text class="wj-num" x="44.0" y="129.0" text-anchor="middle">4</text><text class="wj-cap" x="44.0" y="176" text-anchor="middle" direction="rtl">8 ליטר</text><rect class="wj-water" x="125" y="94" width="58" height="60"/><line class="wj-lev" x1="122" x2="130" y1="139" y2="139"/><line class="wj-lev" x1="122" x2="130" y1="124" y2="124"/><line class="wj-lev" x1="122" x2="130" y1="109" y2="109"/><line class="wj-lev" x1="122" x2="130" y1="94" y2="94"/><path class="wj-jug" d="M122,79 L122,154 L186,154 L186,79"/><text class="wj-num" x="154.0" y="129.0" text-anchor="middle">4</text><text class="wj-cap" x="154.0" y="176" text-anchor="middle" direction="rtl">5 ליטר</text><line class="wj-lev" x1="232" x2="240" y1="139" y2="139"/><line class="wj-lev" x1="232" x2="240" y1="124" y2="124"/><path class="wj-jug wj-chg" d="M232,109 L232,154 L296,154 L296,109"/><text class="wj-num" x="264.0" y="144" text-anchor="middle">0</text><text class="wj-cap" x="264.0" y="176" text-anchor="middle" direction="rtl">3 ליטר</text><path class="wj-arrow" d="M264.0,105 Q154.0,6 52.0,24"/><polygon class="wj-head" points="47.0,17 57.0,17 52.0,26"/></svg><figcaption>מזיגה 7 : מוזגים מהכד של 3 לכד של 8, עד שהכד של 3 ריק. בכדים של 8, 5 ו-3 : 4, 4 ו-0. <strong>שני חצאים של 4 ליטר.</strong></figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="8"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <!-- /gen -->

    <!-- gen 10 -->

    | מזיגה | מ- | ל- | הכד של 3 | הכד של 5 | הכד של 8 |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | 1 | 8 | 5 | 0 | 5 | 3 |
    | 2 | 5 | 3 | 3 | 2 | 3 |
    | 3 | 3 | 8 | 0 | 2 | 6 |
    | 4 | 5 | 3 | 2 | 0 | 6 |
    | 5 | 8 | 5 | 2 | 5 | 1 |
    | 6 | 5 | 3 | 3 | 4 | 1 |
    | 7 | 3 | 8 | 0 | 4 | 4 |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="split_shortest" linenums="1" hl_lines="17 18 24"
        def split_shortest(caps, start, goal):
            """Pours only, no tap: the fewest pours from start to goal,
            [(i, j, state), ...] (jug i into jug j, the contents after it), or None."""
            parent = {start: None}
            queue = deque([start])
            while queue:
                s = queue.popleft()
                if s == goal:
                    plan = []
                    while parent[s] is not None:
                        prev, i, j = parent[s]
                        plan.append((i, j, s))
                        s = prev
                    return plan[::-1]
                for i in range(len(caps)):
                    for j in range(len(caps)):
                        d = min(s[i], caps[j] - s[j])            # (1)!
                        if i == j or d == 0:
                            continue
                        nxt = list(s)
                        nxt[i] -= d
                        nxt[j] += d
                        nxt = tuple(nxt)
                        if nxt not in parent:
                            parent[nxt] = (s, i, j)
                            queue.append(nxt)
            return None
        ```

        1. כמו בסעיף ב : כל מה שיש בכד i, או המקום שנשאר בכד j. מזיגה שלא מעבירה כלום לא
           נחשבת.

    === "SystemVerilog"
        ```systemverilog title="function automatic int split_shortest" linenums="1" hl_lines="8 25 26 29"
        // Pours only: the fewest pours from start to goal with three jugs, or -1. plan lists
        // the pours by capacity, e.g. "8>5, 5>3, 3>8".
        function automatic int split_shortest(int caps[3], int start[3], int goal[3], output string plan);
          int parent[int], depth[int], from_i[int], to_j[int];
          int queue[$];
          int s[3], n[3], key, cur, d, goal_key;
          plan = "";
          key = (start[0] * (caps[1] + 1) + start[1]) * (caps[2] + 1) + start[2];   // (1)!
          goal_key = (goal[0] * (caps[1] + 1) + goal[1]) * (caps[2] + 1) + goal[2];
          depth[key] = 0; parent[key] = -1;
          queue.push_back(key);
          while (queue.size() > 0) begin
            cur = queue.pop_front();
            if (cur == goal_key) begin
              for (int c = cur; parent[c] >= 0; c = parent[c])
                plan = (plan == "") ? $sformatf("%0d>%0d", caps[from_i[c]], caps[to_j[c]])
                                    : {$sformatf("%0d>%0d", caps[from_i[c]], caps[to_j[c]]), ", ", plan};
              return depth[cur];
            end
            s[2] = cur % (caps[2] + 1);
            s[1] = (cur / (caps[2] + 1)) % (caps[1] + 1);
            s[0] = cur / ((caps[2] + 1) * (caps[1] + 1));
            for (int i = 0; i < 3; i++)
              for (int j = 0; j < 3; j++) begin
                d = (s[i] < caps[j] - s[j]) ? s[i] : caps[j] - s[j];
                if (i == j || d == 0) continue;
                n = s; n[i] -= d; n[j] += d;
                key = (n[0] * (caps[1] + 1) + n[1]) * (caps[2] + 1) + n[2];
                if (depth.exists(key)) continue;
                depth[key] = depth[cur] + 1; parent[key] = cur; from_i[key] = i; to_j[key] = j;
                queue.push_back(key);
              end
          end
          return -1;
        endfunction
        ```

        1. מצב של שלושה כדים נשמר כמספר אחד, כמו מספר בבסיס מעורב : ספרה לכל כד.

    #### למה זה נכון { .sol-proof }

    **אותו גרף, אותו BFS.** כל מזיגה היא קשת בין שני מצבים, וכל הקשתות שוות, ולכן BFS מוצא
    מסלול באורך מינימלי. הוא מגיע לחלוקה רק במזיגה השביעית, ויש בדיוק מסלול אחד באורך
    שבע. הרשת מראה את המצבים הנגישים, לפי הכד של 5 לרוחב והכד של 3 לגובה, ואת שתי
    הדרכים :

    <!-- gen 11 -->

    <svg class="perf-chart" viewBox="0 0 336 176" style="max-width:21.0rem" role="img" aria-label="מרחב המצבים של שלושת הכדים לפי הכד של 5 לרוחב והכד של 3 לגובה, והכד של 8 מחזיק את השאר. 16 מצבים נגישים, כולם על השפה. המסלול של 7 מזיגות והמסלול של 8 מזיגות מסומנים"><line class="grid" x1="67.3" x2="67.3" y1="6" y2="144"/><text class="tick" x="67.3" y="162" text-anchor="middle">0</text><line class="grid" x1="114.0" x2="114.0" y1="6" y2="144"/><text class="tick" x="114.0" y="162" text-anchor="middle">1</text><line class="grid" x1="160.7" x2="160.7" y1="6" y2="144"/><text class="tick" x="160.7" y="162" text-anchor="middle">2</text><line class="grid" x1="207.3" x2="207.3" y1="6" y2="144"/><text class="tick" x="207.3" y="162" text-anchor="middle">3</text><line class="grid" x1="254.0" x2="254.0" y1="6" y2="144"/><text class="tick" x="254.0" y="162" text-anchor="middle">4</text><line class="grid" x1="300.7" x2="300.7" y1="6" y2="144"/><text class="tick" x="300.7" y="162" text-anchor="middle">5</text><line class="grid" x1="44" x2="324" y1="127.5" y2="127.5"/><text class="tick" x="36" y="131.5" text-anchor="end">0</text><line class="grid" x1="44" x2="324" y1="94.5" y2="94.5"/><text class="tick" x="36" y="98.5" text-anchor="end">1</text><line class="grid" x1="44" x2="324" y1="61.5" y2="61.5"/><text class="tick" x="36" y="65.5" text-anchor="end">2</text><line class="grid" x1="44" x2="324" y1="28.5" y2="28.5"/><text class="tick" x="36" y="32.5" text-anchor="end">3</text><line class="axis" x1="44" x2="324" y1="144" y2="144"/><text class="tick" x="324.0" y="174.0" text-anchor="end">5</text><text class="tick" x="34.0" y="22.0" text-anchor="end">3</text><polyline class="wj-route is-alt" points="67.3,127.5 67.3,28.5 207.3,127.5 207.3,28.5 300.7,94.5 67.3,94.5 114.0,127.5 114.0,28.5 254.0,127.5" fill="none" stroke-width="2.5" stroke-dasharray="6 5"/><polyline class="wj-route" points="67.3,127.5 300.7,127.5 160.7,28.5 160.7,127.5 67.3,61.5 300.7,61.5 254.0,28.5 254.0,127.5" fill="none" stroke-width="3"/><circle class="wj-reach" cx="67.3" cy="127.5" r="6.5"><title>5 = 0, 3 = 0</title></circle><circle class="wj-reach" cx="67.3" cy="94.5" r="6.5"><title>5 = 0, 3 = 1</title></circle><circle class="wj-reach" cx="67.3" cy="61.5" r="6.5"><title>5 = 0, 3 = 2</title></circle><circle class="wj-reach" cx="67.3" cy="28.5" r="6.5"><title>5 = 0, 3 = 3</title></circle><circle class="wj-reach" cx="114.0" cy="127.5" r="6.5"><title>5 = 1, 3 = 0</title></circle><circle class="wj-never" cx="114.0" cy="94.5" r="4.5"><title>5 = 1, 3 = 1 : לא מגיעים</title></circle><circle class="wj-never" cx="114.0" cy="61.5" r="4.5"><title>5 = 1, 3 = 2 : לא מגיעים</title></circle><circle class="wj-reach" cx="114.0" cy="28.5" r="6.5"><title>5 = 1, 3 = 3</title></circle><circle class="wj-reach" cx="160.7" cy="127.5" r="6.5"><title>5 = 2, 3 = 0</title></circle><circle class="wj-never" cx="160.7" cy="94.5" r="4.5"><title>5 = 2, 3 = 1 : לא מגיעים</title></circle><circle class="wj-never" cx="160.7" cy="61.5" r="4.5"><title>5 = 2, 3 = 2 : לא מגיעים</title></circle><circle class="wj-reach" cx="160.7" cy="28.5" r="6.5"><title>5 = 2, 3 = 3</title></circle><circle class="wj-reach" cx="207.3" cy="127.5" r="6.5"><title>5 = 3, 3 = 0</title></circle><circle class="wj-never" cx="207.3" cy="94.5" r="4.5"><title>5 = 3, 3 = 1 : לא מגיעים</title></circle><circle class="wj-never" cx="207.3" cy="61.5" r="4.5"><title>5 = 3, 3 = 2 : לא מגיעים</title></circle><circle class="wj-reach" cx="207.3" cy="28.5" r="6.5"><title>5 = 3, 3 = 3</title></circle><circle class="wj-goal" cx="254.0" cy="127.5" r="6.5"><title>5 = 4, 3 = 0</title></circle><circle class="wj-never" cx="254.0" cy="94.5" r="4.5"><title>5 = 4, 3 = 1 : לא מגיעים</title></circle><circle class="wj-never" cx="254.0" cy="61.5" r="4.5"><title>5 = 4, 3 = 2 : לא מגיעים</title></circle><circle class="wj-reach" cx="254.0" cy="28.5" r="6.5"><title>5 = 4, 3 = 3</title></circle><circle class="wj-reach" cx="300.7" cy="127.5" r="6.5"><title>5 = 5, 3 = 0</title></circle><circle class="wj-reach" cx="300.7" cy="94.5" r="6.5"><title>5 = 5, 3 = 1</title></circle><circle class="wj-reach" cx="300.7" cy="61.5" r="6.5"><title>5 = 5, 3 = 2</title></circle><circle class="wj-reach" cx="300.7" cy="28.5" r="6.5"><title>5 = 5, 3 = 3</title></circle></svg>

    <!-- /gen -->

    <!-- gen 12 -->

    <span class="viz-legend"><span><i class="wj-key-reach"></i>מצב שמגיעים אליו</span><span><i class="wj-key-goal"></i>החלוקה : 4 ו-4</span><span><i class="wj-key-never"></i>מצב שלא מגיעים אליו</span><span><i class="wj-key-best"></i>7 המזיגות, מתחילים מ-8 ל-5</span><span><i class="wj-key-alt"></i>8 המזיגות, מתחילים מ-8 ל-3</span></span>

    <!-- /gen -->

    **נסו בעצמכם.** שתי משימות. התחילו ב-<span dir="ltr">8 → 3</span> במקום
    ב-<span dir="ltr">8 → 5</span> והגיעו לחלוקה : שמונה מזיגות במקום שבע. אחר כך נסו להגיע
    למצב שבפנים הרשת, למשל 2 בכד של 5 ו-1 בכד של 3 : אי אפשר. מה שאין באיורים : כאן אפשר
    לטעות ולבטל, ו"מרחק BFS" מראה שהחלוקה היא אחד משני המצבים הרחוקים ביותר מההתחלה, 7
    מזיגות.

    <div class="explorer" data-kind="jugs3" data-caps="8,5,3" data-goal="4,4,0"></div>

    #### סיבוכיות { .sol-cost }

    שבע מזיגות, במרחב של 16 מצבים שמכל אחד מהם לכל היותר שש מזיגות. עם \( n \) כדים
    בקיבולות \( c_1, \dots, c_n \) יש לכל היותר \( \prod (c_i + 1) \) מצבים, ומכל מצב לכל
    היותר \( n(n - 1) \) מזיגות.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : gcd בלבד"
    ‏\( \gcd(3, 5) = 1 \) מחלק כל מספר, אבל 7 ליטר אי אפשר למדוד בכד אחד : אף כד לא מחזיק
    יותר מ-5. התנאי המלא הוא גם כפולה של \( \gcd \) וגם לא יותר מהכד הגדול.

??? trap "מלכודת : DFS במקום BFS"
    חיפוש לעומק מוצא דרך, אבל לא בהכרח את הקצרה. ב-3 ו-5, חיפוש לעומק שמנסה את הצעדים
    בסדר של הקוד ממלא את A, ממלא את B ומרוקן את A, ורק אז עושה את חמשת הצעדים האחרונים של
    הדרך הקצרה. הוא עוצר ב-4 אחרי שמונה צעדים, שניים מהם מיותרים (וזו לא "הדרך השנייה" של
    סעיף א). רק BFS, שעובר על המצבים לפי מרחק, מבטיח את המינימום.

??? trap "מלכודת : לעצור באמצע מזיגה"
    "מוזגים 4 ליטר מ-B" הוא לא צעד : אין על הכדים סימונים, ומזיגה נגמרת רק כשהכד שמוזגים
    ממנו ריק או שהכד השני מלא. בגלל זה כל המצבים הנגישים על שפת הרשת.

??? followup "שאלות המשך"
    - **4 ליטר בשני הכדים יחד :** מה משתנה אם המטרה היא \( T \) ליטר בסך הכול, A ו-B ביחד?

        ??? fu-answer "תשובה"
            עכשיו אפשר כל כפולה של \( \gcd(a, b) \) עד \( a + b \). למשל 7 ליטר ב-3 ו-5 :
            חמשת הצעדים הראשונים של סעיף א משאירים 2 ב-A ו-5 ב-B, ופחות מחמישה אי אפשר.

    - **בלי BFS :** האם אפשר לחשב את מספר הצעדים המינימלי בנוסחה?

        ??? fu-answer "תשובה"
            כן, בלי נוסחה סגורה אבל בלי חיפוש. יש שתי שיטות של "מזיגה חוזרת" : ממלאים רק
            את A ושופכים ל-B, או ממלאים רק את B ושופכים ל-A. מריצים את שתיהן ולוקחים את
            הקצרה, ב-\( O(a + b) \). ב-3 ו-5 אלה 8 ו-6 צעדים. הסיבה : כל המצבים הנגישים, חוץ
            מההתחלה, יושבים על מעגל אחד לאורך השפה, ושתי השיטות הולכות סביבו בשני
            הכיוונים. זו לא הוכחה מלאה : הטסט של השאלה משווה את התוצאה ל-BFS לכל
            \( a, b \le 40 \).

    - **איך בודקים את `jugs_shortest`?** איזה מודל ייחוס לא חוזר על אותו BFS?

        ??? fu-answer "תשובה"
            שלוש בדיקות שלא תלויות באלגוריתם שנבדק. **קיום :** יש תוכנית אם ורק אם כלל
            ה-gcd (`can_measure`) אומר שאפשר. **חוקיות :** בודק שמריץ את התוכנית מ-\( (0, 0) \),
            צעד אחרי צעד, ומוודא שכל צעד חוקי, שהכמויות שהפונקציה מדווחת נכונות, ושבסוף יש
            \( T \) באחד הכדים. **מינימום :** השוואה של האורך לקצרה משתי "המזיגות החוזרות"
            של השאלה הקודמת. מקרי הקצה שחייבים לכסות : \( \gcd > 1 \), ‏\( T \) גדול משני
            הכדים, \( T = 0 \) ו-\( a = b \).

    - **ארבעה כדים, או שלושה עם ברז :** מה משתנה בקוד?

        ??? fu-answer "תשובה"
            רק רשימת הצעדים. המצב הוא וקטור של כמויות, ומכל מצב יש מילוי וריקון לכל כד
            (אם יש ברז) ומזיגה לכל זוג סדור. BFS נשאר אותו BFS.
