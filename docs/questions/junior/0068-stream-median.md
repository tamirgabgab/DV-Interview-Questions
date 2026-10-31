---
id: 68
title: החציון של זרם – שתי ערימות, אחוזון p, וחלון נע
level: junior
difficulty: medium
kind: code
tags: [algorithms, heap, python, systemverilog]
source: "שאלה קלאסית (Find Median from Data Stream, LeetCode 295); סעיף ב הוא ההכללה לאחוזון, וסעיף ג הוא Sliding Window Median (LeetCode 480) לאחוזון"
added: 2026-10-29
---

## השאלה

מספרים שלמים מגיעים אחד אחרי השני, בלי שידוע מראש כמה יהיו. אחרי כל מספר צריך לדווח על
**החציון** של כל מה שהגיע עד עכשיו : הערך האמצעי של המספרים הממוינים, ובמספר זוגי של ערכים
הממוצע של שני האמצעיים. בזרם <span dir="ltr">5 15 1 3 8 7 9 10 20 2</span> החציונים הם
<span dir="ltr">5 10 5 4 5 6 7 7.5 8 7.5</span> : אחרי <span dir="ltr">5 15</span> הממוצע 10,
אחרי <span dir="ltr">5 15 1</span> הערך האמצעי 5, וכן הלאה.

**ההקשר באימות :** מוניטור של זמני תגובה (latency) שמדווח תוך כדי הריצה על החציון ועל הזנב,
האחוזון ה-99, של הטרנזקציות שהסתיימו עד עכשיו, בלי לשמור את כולן ולמיין בסוף. הסימולציה
רצה שעות, ומדווחת כל אלף טרנזקציות; מיון של הכול בכל דיווח יהיה \( O(n \log n) \) לדיווח, ועם
מיליוני טרנזקציות זה כבר לא זניח. הגרסה של החלון הנע היא לוח המחוונים של "ה-\( W \)
הטרנזקציות האחרונות" : הזנב של הרגע, לא מתחילת הריצה.

- **סעיף א – החציון של זרם :** כתבו מחלקה `StreamMedian` עם `add(x)` ו-`median()`, כך
  שהכנסה עולה \( O(\log n) \) ושאילתה \( O(1) \).
- **סעיף ב – אחוזון p :** נתון שבר \( 0 \le p \le 1 \). אחרי כל מספר דווחו על **האחוזון**
  \( p \) של מה שהגיע : הערך במקום \( \lceil p \cdot n \rceil \) של הרשימה הממוינת (ספירה מ-1),
  ובמקום 1 כש-\( p = 0 \). כתבו `StreamQuantile(p)` עם `add(x)` ו-`quantile()`, באותה עלות.
- **סעיף ג – חלון נע :** אותו אחוזון, אבל רק על \( W \) המספרים האחרונים. ערך ישן יוצא
  מהחשבון בכל פעם שנכנס חדש. איך מוחקים מערימה?

??? interviewer "מה המראיין בודק"
    - **המבנה הנכון :** האם המועמד רואה שלא צריך את הכול ממוין, רק את הגבול בין "החצי
      הקטן" ל"חצי הגדול", ושהגבול הזה הוא ראש של ערימה.
    - **שמורות :** שני תנאים צריכים להתקיים אחרי כל הכנסה, על הסדר ועל הגדלים. האם המועמד
      מנסח אותם, ומראה למה כל צעד שומר עליהם.
    - **ההכללה :** מחציון לאחוזון כללי זה שינוי של גודל יעד אחד. האם המועמד מבין מה היה
      מיוחד ב"חצי".
    - **מחיקה ממבנה שלא תומך במחיקה :** בסעיף ג האינסטינקט למחוק מאמצע הערימה. האם
      המועמד מכיר מחיקה עצלה, ויודע מה היא עולה.

---

### סעיף א – החציון של זרם

??? tip "רמז 1"
    לא צריך לדעת את הסדר המלא של כל המספרים. מה צריך לדעת כדי לומר מה החציון של
    <span dir="ltr">1 3 5 7 8</span>, ומה משתנה בו כשנכנס 6? וכשנכנס 20?

??? tip "רמז 2"
    חלקו את המספרים לשני חצאים : הקטנים והגדולים. מהחצי הקטן צריך רק את **הגדול ביותר**, ומהחצי
    הגדול רק את **הקטן ביותר**. איזה מבנה נתונים נותן את הקיצוני בזמן קבוע ומכניס בזמן
    לוגריתמי?

<div class="selfcheck" data-answer="6" data-show="6 : אחרי שישה ערכים הרשימה הממוינת היא 1 3 5 7 8 15, ושני האמצעיים הם 5 ו-7" data-hint="מיינו את ששת הערכים הראשונים. מספר הערכים זוגי, ולכן החציון הוא הממוצע של שני האמצעיים." markdown>
בזרם <span dir="ltr">5 15 1 3 8 7 9 10 20 2</span>, מה החציון אחרי ששת הערכים הראשונים?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שתי ערימות : `low`, ערימת **מקסימום** של החצי הקטן, ו-`high`, ערימת **מינימום** של החצי
        הגדול, עם \( |\text{low}| = |\text{high}| \) או \( |\text{low}| = |\text{high}| + 1 \). כל
        ערך ב-`low` קטן מכל ערך ב-`high` או שווה לו, ולכן החציון הוא הראש של `low` (במספר
        אי-זוגי) או הממוצע של שני הראשים. הכנסה : דוחפים ל-`low`, מעבירים את הראש של `low`
        ל-`high`, ואם `high` נעשתה גדולה יותר מחזירים את הראש שלה. שלוש פעולות ערימה,
        \( O(\log n) \).

    <!-- cost: הכנסה \( O(\log n) \) | שאילתה \( O(1) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **מונחים.** ‏**ערימה בינארית** (binary heap) היא מערך `a` שקוראים אותו כעץ : האיבר
    `a[k]` הוא ההורה של `a[2k + 1]` ושל `a[2k + 2]`, ולכן ההורה של `a[k]` הוא
    `a[(k − 1) / 2]`. **ערימת מינימום** מקיימת שכל איבר קטן משני ילדיו או שווה להם, ולכן
    `a[0]`, **הראש** (top), הוא המינימום של כל המערך. באיור, המערך <span dir="ltr">1 3 2 7 4 9 5</span>
    כעץ :

    <!-- gen 0 -->

    <svg class="figure th-fig" viewBox="0 0 320 224" style="max-width:20rem" role="img" aria-label="ערימת מינימום של 1 3 2 7 4 9 5 : המערך עם האינדקסים, ואותו מערך כעץ, כל איבר מעל שני ילדיו"><line class="th-edge" x1="160" y1="36" x2="84" y2="80"/><line class="th-edge" x1="160" y1="36" x2="236" y2="80"/><line class="th-edge" x1="84" y1="80" x2="46" y2="124"/><line class="th-edge" x1="84" y1="80" x2="122" y2="124"/><line class="th-edge" x1="236" y1="80" x2="198" y2="124"/><line class="th-edge" x1="236" y1="80" x2="274" y2="124"/><g class="th-node is-top"><title>a[0] = 1</title><circle cx="160" cy="36" r="14"/><text x="160" y="40" text-anchor="middle">1</text></g><text class="tick" x="176" y="26">0</text><g class="th-node"><title>a[1] = 3</title><circle cx="84" cy="80" r="14"/><text x="84" y="84" text-anchor="middle">3</text></g><text class="tick" x="100" y="70">1</text><g class="th-node"><title>a[2] = 2</title><circle cx="236" cy="80" r="14"/><text x="236" y="84" text-anchor="middle">2</text></g><text class="tick" x="252" y="70">2</text><g class="th-node"><title>a[3] = 7</title><circle cx="46" cy="124" r="14"/><text x="46" y="128" text-anchor="middle">7</text></g><text class="tick" x="62" y="114">3</text><g class="th-node"><title>a[4] = 4</title><circle cx="122" cy="124" r="14"/><text x="122" y="128" text-anchor="middle">4</text></g><text class="tick" x="138" y="114">4</text><g class="th-node"><title>a[5] = 9</title><circle cx="198" cy="124" r="14"/><text x="198" y="128" text-anchor="middle">9</text></g><text class="tick" x="214" y="114">5</text><g class="th-node"><title>a[6] = 5</title><circle cx="274" cy="124" r="14"/><text x="274" y="128" text-anchor="middle">5</text></g><text class="tick" x="290" y="114">6</text><text class="th-lab" x="28" y="194" text-anchor="end">a</text><g class="th-cell is-top"><title>a[0] = 1</title><rect x="36" y="172" width="32" height="28" rx="4"/><text x="52" y="189" text-anchor="middle">1</text></g><text class="tick" x="52" y="212" text-anchor="middle">0</text><g class="th-cell"><title>a[1] = 3</title><rect x="72" y="172" width="32" height="28" rx="4"/><text x="88" y="189" text-anchor="middle">3</text></g><text class="tick" x="88" y="212" text-anchor="middle">1</text><g class="th-cell"><title>a[2] = 2</title><rect x="108" y="172" width="32" height="28" rx="4"/><text x="124" y="189" text-anchor="middle">2</text></g><text class="tick" x="124" y="212" text-anchor="middle">2</text><g class="th-cell"><title>a[3] = 7</title><rect x="144" y="172" width="32" height="28" rx="4"/><text x="160" y="189" text-anchor="middle">7</text></g><text class="tick" x="160" y="212" text-anchor="middle">3</text><g class="th-cell"><title>a[4] = 4</title><rect x="180" y="172" width="32" height="28" rx="4"/><text x="196" y="189" text-anchor="middle">4</text></g><text class="tick" x="196" y="212" text-anchor="middle">4</text><g class="th-cell"><title>a[5] = 9</title><rect x="216" y="172" width="32" height="28" rx="4"/><text x="232" y="189" text-anchor="middle">9</text></g><text class="tick" x="232" y="212" text-anchor="middle">5</text><g class="th-cell"><title>a[6] = 5</title><rect x="252" y="172" width="32" height="28" rx="4"/><text x="268" y="189" text-anchor="middle">5</text></g><text class="tick" x="268" y="212" text-anchor="middle">6</text></svg>

    <!-- /gen -->

    שלוש פעולות : ‏**top** מחזירה את `a[0]`, ‏\( O(1) \). ‏**push** מוסיפה איבר בסוף המערך ומעלה
    אותו (מחליפה עם ההורה כל עוד הוא קטן ממנו), לכל היותר \( \lfloor \log_2 n \rfloor \)
    החלפות, כי זה הגובה של העץ. ‏**pop** מוציאה את הראש : האיבר האחרון עובר לראש ויורד (מוחלף
    עם הקטן מבין ילדיו כל עוד אחד מהם קטן ממנו), שוב \( O(\log n) \). **ערימת מקסימום** היא
    אותו דבר עם הסימן ההפוך, והראש הוא המקסימום. ב-Python המודול `heapq` הוא ערימת מינימום
    על רשימה רגילה; ערימת מקסימום מקבלים בדחיפה של **הערכים השליליים**, \( -x \), ואז הראש
    \( -a[0] \) הוא המקסימום. ב-SystemVerilog אין ערימה בספרייה : תור ממוין (`q.sort()` אחרי כל
    הכנסה) עולה \( O(n \log n) \) להכנסה, והכנסה למקום הנכון בתור ממוין \( O(n) \) בגלל ההזזה,
    ולכן בקוד שלמטה כתובה מחלקה `heap_t` של עשרים שורות, עם `push` ו-`pop` ב-\( O(\log n) \).

    **שתי ערימות.** את המספרים שהגיעו מחלקים לשני חצאים : `low`, הקטנים, ו-`high`, הגדולים.
    החציון יושב בדיוק על הגבול ביניהם : הוא הגדול ביותר ב-`low` או הקטן ביותר ב-`high`.
    לכן `low` היא ערימת **מקסימום** ו-`high` ערימת **מינימום**, ושני הראשים הם שני הערכים
    שמסביב לגבול. באיור, המצב אחרי כל הזרם של הדוגמה : ‏`high` מצוירת למעלה עם הראש שלה
    למטה, ‏`low` מצוירת למטה עם הראש שלה למעלה, כך ששני הראשים נפגשים על קו החציון :

    <!-- gen 1 -->

    <svg class="figure th-fig th-two" viewBox="0 0 320 300" style="max-width:20rem" role="img" aria-label="שתי הערימות אחרי כל הזרם 5 15 1 3 8 7 9 10 20 2 : high למעלה, low למטה, והחציון על הקו ביניהן"><line class="th-edge" x1="160" y1="106" x2="128" y2="66"/><line class="th-edge" x1="160" y1="106" x2="192" y2="66"/><line class="th-edge" x1="128" y1="66" x2="64" y2="26"/><line class="th-edge" x1="128" y1="66" x2="128" y2="26"/><g class="th-node is-top"><title>high[0]: value 8, arrival 4, the top</title><circle cx="160" cy="106" r="14"/><text x="160" y="110" text-anchor="middle">8</text></g><g class="th-node"><title>high[1]: value 9, arrival 6, in the heap</title><circle cx="128" cy="66" r="14"/><text x="128" y="70" text-anchor="middle">9</text></g><g class="th-node"><title>high[2]: value 15, arrival 1, in the heap</title><circle cx="192" cy="66" r="14"/><text x="192" y="70" text-anchor="middle">15</text></g><g class="th-node"><title>high[3]: value 20, arrival 8, in the heap</title><circle cx="64" cy="26" r="14"/><text x="64" y="30" text-anchor="middle">20</text></g><g class="th-node"><title>high[4]: value 10, arrival 7, in the heap</title><circle cx="128" cy="26" r="14"/><text x="128" y="30" text-anchor="middle">10</text></g><line class="th-edge" x1="160" y1="194" x2="128" y2="234"/><line class="th-edge" x1="160" y1="194" x2="192" y2="234"/><line class="th-edge" x1="128" y1="234" x2="64" y2="274"/><line class="th-edge" x1="128" y1="234" x2="128" y2="274"/><g class="th-node is-top"><title>low[0]: value 7, arrival 5, the top</title><circle cx="160" cy="194" r="14"/><text x="160" y="198" text-anchor="middle">7</text></g><g class="th-node"><title>low[1]: value 5, arrival 0, in the heap</title><circle cx="128" cy="234" r="14"/><text x="128" y="238" text-anchor="middle">5</text></g><g class="th-node"><title>low[2]: value 3, arrival 3, in the heap</title><circle cx="192" cy="234" r="14"/><text x="192" y="238" text-anchor="middle">3</text></g><g class="th-node"><title>low[3]: value 1, arrival 2, in the heap</title><circle cx="64" cy="274" r="14"/><text x="64" y="278" text-anchor="middle">1</text></g><g class="th-node"><title>low[4]: value 2, arrival 9, in the heap</title><circle cx="128" cy="274" r="14"/><text x="128" y="278" text-anchor="middle">2</text></g><line class="th-mid" x1="8" y1="150" x2="312" y2="150"/><text class="th-lab" x="10" y="142">high ↑ 5</text><text class="th-lab" x="10" y="166">low ↓ 5</text><rect class="th-ans-bg" x="100" y="139" width="120" height="22" rx="11"/><text class="th-ans" x="160" y="155" text-anchor="middle">median = 7.5</text></svg>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="th-key-in"></i>בערימה</span><span><i class="th-key-top"></i>הראש</span><span><i class="th-key-new"></i>הערך החדש</span><span><i class="th-key-moved"></i>עבר בצעד הזה</span><span><i class="th-key-dead"></i>יצא מהחלון, עוד בערימה</span></span>

    <!-- /gen -->

    **שתי שמורות.** אחרי כל הכנסה :

    - **הסדר :** כל ערך ב-`low` קטן מכל ערך ב-`high` או שווה לו. אז הראש של `low` הוא הגדול
      ב-\( |\text{low}| \) הערכים הקטנים ביותר, כלומר הערך במקום \( |\text{low}| \) של הרשימה
      הממוינת.
    - **הגדלים :** ‏\( |\text{low}| = |\text{high}| \) או \( |\text{low}| = |\text{high}| + 1 \). עם
      \( n \) ערכים, \( |\text{low}| = \lceil n / 2 \rceil \).

    יחד : במספר אי-זוגי של ערכים הראש של `low` הוא הערך במקום \( (n + 1) / 2 \), החציון. במספר
    זוגי הוא במקום \( n / 2 \), והראש של `high` במקום \( n / 2 + 1 \), ושני אלה הם האמצעיים.

    **לדחוף דרך `low`.** איך מכניסים ערך חדש \( x \) בלי לשבור את הסדר? הדרך הישירה היא להשוות
    את \( x \) לראשים ולבחור ערימה, עם כמה מקרים. הטריק שחוסך את המקרים : **תמיד** דוחפים את
    \( x \) ל-`low`, ומיד מעבירים את **הראש** של `low` ל-`high`. הראש הוא המקסימום של `low`
    אחרי ההכנסה, ולכן מה שעבר ל-`high` גדול מכל מה שנשאר ב-`low` או שווה לו, וקטן מכל מה
    שהיה ב-`high` (אם \( x \) עצמו עבר, הוא גדול מהראש הקודם של `low`, שהיה קטן מכל `high`;
    אם עבר הראש הקודם, הוא קטן מכל `high` מהשמורה). הסדר נשמר **בלי אף השוואה בקוד** : הערימה
    עושה את ההשוואות. אחרי המעבר `high` גדלה ב-1, ואם עכשיו היא גדולה מ-`low`, הראש של
    `high` חוזר ל-`low` : הוא המינימום של `high` וגדול מכל `low`, ולכן גם המעבר הזה שומר על
    הסדר. הגדלים חוזרים לשמורה.

    **הערה על ההגדרה.** יש מי שמגדירים את החציון במספר זוגי של ערכים כ**חציון התחתון**, הערך
    במקום \( n / 2 \), בלי ממוצע. אז התשובה היא תמיד הראש של `low`, וסעיף ב עם \( p = 1/2 \)
    נותן בדיוק אותה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **דוחפים ל-`low` :** הערך החדש \( x \) נכנס לערימת המקסימום. ב-Python נדחף \( -x \).
    2. **הראש של `low` עובר ל-`high` :** הוא המקסימום של `low` אחרי ההכנסה, ולכן הסדר נשמר.
    3. **איזון :** אם \( |\text{high}| > |\text{low}| \), הראש של `high` חוזר ל-`low`. אחרת
       אין צורך בשום דבר.
    4. **החציון :** אם \( |\text{low}| > |\text{high}| \), הראש של `low`. אחרת הממוצע של שני
       הראשים.

    </div>

    על הזרם <span dir="ltr">5 15 1 3 8 7 9 10 20 2</span>. בכל שורה הערך שעבר ל-`high` בצעד 2,
    הערך שחזר בצעד 3 (אם היה), ושתי הערימות אחרי הצעד, מהראש והלאה :

    <!-- gen 3 -->

    | ‏i | ‏x | עובר ל-high | חוזר ל-low | ‏low (הראש ראשון) | ‏high (הראש ראשון) | הגדלים | החציון |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏1 | ‏5 | ‏5 | ‏5 | ‏<span dir="ltr"><b>5</b></span> | ריקה | ‏1, 0 | **‏5** |
    | ‏2 | ‏15 | ‏15 | אין צורך | ‏<span dir="ltr"><b>5</b></span> | ‏<span dir="ltr"><b>15</b></span> | ‏1, 1 | **‏10** |
    | ‏3 | ‏1 | ‏5 | ‏5 | ‏<span dir="ltr"><b>5</b> 1</span> | ‏<span dir="ltr"><b>15</b></span> | ‏2, 1 | **‏5** |
    | ‏4 | ‏3 | ‏5 | אין צורך | ‏<span dir="ltr"><b>3</b> 1</span> | ‏<span dir="ltr"><b>5</b> 15</span> | ‏2, 2 | **‏4** |
    | ‏5 | ‏8 | ‏8 | ‏5 | ‏<span dir="ltr"><b>5</b> 3 1</span> | ‏<span dir="ltr"><b>8</b> 15</span> | ‏3, 2 | **‏5** |
    | ‏6 | ‏7 | ‏7 | אין צורך | ‏<span dir="ltr"><b>5</b> 3 1</span> | ‏<span dir="ltr"><b>7</b> 8 15</span> | ‏3, 3 | **‏6** |
    | ‏7 | ‏9 | ‏9 | ‏7 | ‏<span dir="ltr"><b>7</b> 5 3 1</span> | ‏<span dir="ltr"><b>8</b> 9 15</span> | ‏4, 3 | **‏7** |
    | ‏8 | ‏10 | ‏10 | אין צורך | ‏<span dir="ltr"><b>7</b> 5 3 1</span> | ‏<span dir="ltr"><b>8</b> 9 10 15</span> | ‏4, 4 | **‏7.5** |
    | ‏9 | ‏20 | ‏20 | ‏8 | ‏<span dir="ltr"><b>8</b> 7 5 3 1</span> | ‏<span dir="ltr"><b>9</b> 10 15 20</span> | ‏5, 4 | **‏8** |
    | ‏10 | ‏2 | ‏8 | אין צורך | ‏<span dir="ltr"><b>7</b> 5 3 2 1</span> | ‏<span dir="ltr"><b>8</b> 9 10 15 20</span> | ‏5, 5 | **‏7.5** |

    <!-- /gen -->

    בצעד 2 נכנס 15 : הוא נדחף ל-`low`, נעשה הראש שלה, ועובר ל-`high`. ‏`high` לא גדולה
    מ-`low`, ולכן שום דבר לא חוזר, והחציון הוא הממוצע של 5 ו-15. בצעד 3 נכנס 1 : הראש של
    `low` הוא עדיין 5, והוא עובר ל-`high`, שגדלה ל-2 מול 1, ולכן הראש של `high`, 5, חוזר.
    מה שעבר הלוך וחזור הוא ה-5 ולא ה-1 : הדחיפה דרך `low` מעבירה תמיד את המקסימום, וה-1
    נשאר במקומו. בצעד 9 נכנס 20, עובר ל-`high`, וחוזר 8 : החציון עלה מ-7.5 ל-8.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="class StreamMedian" linenums="1" hl_lines="14 15 16"
        from heapq import heappush, heappop


        class StreamMedian:
            """The median of every prefix of a stream: low is a max-heap of the smaller half
            (negated values, since heapq is a min-heap) and high a min-heap of the larger
            half, with len(low) == len(high) or len(low) == len(high) + 1."""

            def __init__(self):
                self.low: list[int] = []        # the smaller half, negated: -low[0] is its largest
                self.high: list[int] = []       # the larger half: high[0] is its smallest

            def add(self, x: int) -> None:
                heappush(self.low, -x)                          # (1)!
                heappush(self.high, -heappop(self.low))         # (2)!
                if len(self.high) > len(self.low):              # (3)!
                    heappush(self.low, -heappop(self.high))

            def median(self) -> float:
                if len(self.low) > len(self.high):
                    return -self.low[0]                         # (4)!
                return (-self.low[0] + self.high[0]) / 2


        def stream_medians(nums: list[int]) -> list[float]:
            """The median after every value."""
            sm = StreamMedian()
            out = []
            for x in nums:
                sm.add(x)
                out.append(sm.median())
            return out
        ```

        1. ‏`low` מחזיקה ערכים שליליים, ולכן הראש שלה, `low[0]`, הוא מינוס המקסימום.
        2. הדחיפה דרך `low` : הראש שלה יוצא (`heappop`), חוזר לסימן חיובי ונכנס ל-`high`.
        3. ‏`high` נעשתה גדולה יותר : הראש שלה חוזר ל-`low`, שוב עם הסימן ההפוך.
        4. מספר אי-זוגי של ערכים : החציון הוא הראש של `low`. שימו לב לסימן.

    === "SystemVerilog"
        ```systemverilog title="class heap_t, StreamMedian" linenums="1" hl_lines="41 42 43"
        // a value with its arrival number, so equal values are told apart (part c needs it)
        typedef struct { int v; int id; } item_t;

        // a binary heap in a queue: the smallest item on top, or the largest with is_max
        class heap_t;
          item_t a[$];
          bit is_max;
          function new(bit is_max = 0); this.is_max = is_max; endfunction
          function int size(); return a.size(); endfunction
          function item_t top(); return a[0]; endfunction
          function bit above(item_t x, item_t y);                  // x belongs above y
            if (x.v != y.v) return is_max ? x.v > y.v : x.v < y.v;
            return x.id < y.id;
          endfunction
          function void push(item_t x);                            // sift up          (1)
            int i = a.size();
            a.push_back(x);
            while (i > 0 && above(a[i], a[(i - 1) / 2])) begin
              a[i] = a[(i - 1) / 2]; a[(i - 1) / 2] = x; i = (i - 1) / 2;
            end
          endfunction
          function item_t pop();                                   // sift down        (2)
            item_t top = a[0], t;
            int i = 0, k;
            a[0] = a[$]; void'(a.pop_back());
            forever begin
              k = i;
              if (2 * i + 1 < a.size() && above(a[2 * i + 1], a[k])) k = 2 * i + 1;
              if (2 * i + 2 < a.size() && above(a[2 * i + 2], a[k])) k = 2 * i + 2;
              if (k == i) break;
              t = a[i]; a[i] = a[k]; a[k] = t; i = k;
            end
            return top;
          endfunction
        endclass

        class StreamMedian;
          heap_t low = new(1), high = new(0);   // the smaller half (max on top), the larger half
          int n = 0;
          function void add(int x);
            low.push('{x, n});                                     // (3)!
            high.push(low.pop());                                  // (4)!
            if (high.size() > low.size()) low.push(high.pop());    // (5)!
            n++;
          endfunction
          function real median();
            if (low.size() > high.size()) return low.top().v;
            return (real'(low.top().v) + high.top().v) / 2.0;
          endfunction
        endclass
        ```

        1. האיבר החדש בסוף המערך עולה : מוחלף עם ההורה `a[(i − 1) / 2]` כל עוד הוא שייך מעליו. לכל היותר הגובה של העץ.
        2. הראש יוצא, האחרון עובר לראש ויורד : מוחלף עם הילד שצריך להיות מעליו. ‏`forever` עם `break` נעצר כשאף ילד לא שייך מעליו.
        3. הערך עם מספר ההגעה שלו. בשני הסעיפים הראשונים המספר רק מכריע בין ערכים שווים.
        4. הדחיפה דרך `low` : הראש שלה, המקסימום של `low` אחרי ההכנסה, עובר ל-`high`. הסדר נשמר.
        5. ‏`high` נעשתה גדולה יותר : הראש שלה, המינימום של `high`, חוזר. הגדלים חוזרים לשמורה.

    #### למה זה נכון { .sol-proof }

    **שמורת הסדר** (כל `low` \( \le \) כל `high`) **באינדוקציה.** בהתחלה שתי הערימות ריקות.
    נניח שהיא מתקיימת לפני ההכנסה של \( x \), ויהי \( m' \) הראש של `low` לפניה. אחרי הדחיפה
    של \( x \), הראש \( m \) הוא המקסימום של `low` החדשה, והוא עובר ל-`high`. שני מקרים :

    - **‏\( m = x \) :** אז \( x \ge m' \), ומה שנשאר ב-`low` הוא בדיוק `low` הישנה, שקטנה מכל
      `high` הישנה (השמורה) וגם מ-\( x \) (כי \( x \ge m' \ge \) כל `low` הישנה). ‏`high` החדשה
      היא הישנה ועוד \( x \), ולכן כל `low` \( \le \) כל `high`.
    - **‏\( m = m' \) :** אז \( x \le m' \), ומה שנשאר ב-`low` הוא `low` הישנה בלי \( m' \) ועם
      \( x \), הכול \( \le m' \). ו-\( m' \le \) כל `high` הישנה לפי השמורה, ולכן כל `low`
      \( \le m' \le \) כל `high` החדשה.

    הערימה החליטה בעצמה איזה משני המקרים קרה : זה "בלי השוואה בקוד". המעבר חזרה מעביר את
    המינימום של `high`, שגדול מכל `low` או שווה לו (הוא היה ב-`high`) וקטן מכל `high` שנשאר.
    השמורה נשמרת.

    **שמורת הגדלים.** לפני ההכנסה \( |\text{low}| - |\text{high}| \in \{0, 1\} \). אחרי הדחיפה
    והמעבר, \( |\text{low}| \) לא השתנה ו-\( |\text{high}| \) גדל ב-1, ולכן ההפרש הוא \( -1 \) או
    \( 0 \). אם הוא \( -1 \), המעבר חזרה מביא אותו ל-\( 1 \). אחרי הצעד ההפרש שוב 0 או 1. מכאן
    \( |\text{low}| = \lceil n / 2 \rceil \), ולפי שמורת הסדר הראש של `low` הוא הערך במקום
    \( \lceil n / 2 \rceil \) של הרשימה הממוינת : החציון ב-\( n \) אי-זוגי, והאמצעי התחתון ב-\( n \)
    זוגי, כשהראש של `high` הוא האמצעי העליון.

    **ערכים שווים :** השמורה היא "קטן או שווה", ולכן כפילויות יכולות לשבת בשתי הערימות, והחציון
    נכון בכל מקרה : ב-<span dir="ltr">4 4 4 4</span> שני הראשים הם 4.

    #### סיבוכיות { .sol-cost }

    - **הכנסה :** ‏\( O(\log n) \). לכל היותר חמש פעולות ערימה : `push`, ‏`pop`, ‏`push`, ואולי
      עוד `pop` ו-`push`, כל אחת \( O(\log n) \) על ערימה של עד \( n \) איברים.
    - **שאילתה :** ‏\( O(1) \), שני ראשים.
    - **זיכרון :** ‏\( O(n) \). שומרים את כל הערכים, ואי אפשר אחרת : החציון המדויק של זרם דורש
      לזכור את הכול (ראו שאלות ההמשך על קירובים). לעומת מיון בכל שאילתה, \( O(n \log n) \)
      לשאילתה, או הכנסה למערך ממוין, \( O(n) \) להכנסה בגלל ההזזה.

    **נסו בעצמכם.** כל ערך הוא שלושה צעדים : הדחיפה ל-`low`, המעבר של הראש ל-`high`, והאיזון עם
    החציון. ‏`high` מצוירת למעלה עם הראש שלה למטה, ‏`low` מצוירת למטה עם הראש שלה למעלה, והקו
    ביניהן הוא החציון :

    <div class="explorer" data-kind="twoheaps" data-mode="a" data-nums="5 15 1 3 8 7 9 10 20 2"></div>

---

### סעיף ב – אחוזון p של זרם

??? tip "רמז 1"
    בסעיף א `low` מחזיקה בדיוק \( \lceil n / 2 \rceil \) ערכים, והראש שלה הוא הערך במקום
    \( \lceil n / 2 \rceil \) של הרשימה הממוינת. איזה גודל של `low` נותן את הערך במקום
    \( \lceil p \cdot n \rceil \)?

??? tip "רמז 2"
    אחרי כל הכנסה חשבו את גודל היעד של `low` מחדש. בכמה הוא יכול להשתנות בהכנסה אחת? מה
    זה אומר על מספר המעברים בין הערימות?

<div class="selfcheck" data-answer="15" data-show="15 : המקום ⌈0.9 · 10⌉ = 9 של 1 2 3 5 7 8 9 10 15 20, ולא 20" data-hint="מיינו את עשרת הערכים וחשבו את המקום ⌈p · n⌉. שימו לב שהוא לא 10." markdown>
בזרם <span dir="ltr">5 15 1 3 8 7 9 10 20 2</span>, מה האחוזון \( p = 0.9 \) אחרי כל עשרת
הערכים?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        אותן שתי ערימות, עם גודל יעד \( t = \lceil p \cdot n \rceil \) ל-`low` (ולפחות 1). אחרי
        הדחיפה דרך `low`, אם \( |\text{low}| < t \) הראש של `high` חוזר. האחוזון הוא תמיד הראש
        של `low`. היעד גדל בכל הכנסה ב-0 או ב-1, ולכן לכל היותר מעבר אחד חזרה, ו-\( O(\log n) \)
        להכנסה. בדוגמה עם \( p = 0.9 \) האחוזון הוא 15 אחרי עשרה ערכים, ועם \( p = 0.25 \) הוא 3.

    <!-- cost: הכנסה \( O(\log n) \) | שאילתה \( O(1) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **ההגדרה.** האחוזון \( p \) לפי **הדרגה הקרובה** (nearest rank) של \( n \) ערכים הוא הערך
    במקום \( r = \lceil p \cdot n \rceil \) של הרשימה הממוינת, ספירה מ-1, ובמקום 1 כש-\( p = 0 \).
    לכן \( p = 0 \) נותן את המינימום, \( p = 1 \) את המקסימום (\( r = n \)), ו-\( p = 1/2 \) את
    הערך במקום \( \lceil n / 2 \rceil \) : החציון ב-\( n \) אי-זוגי, ו**החציון התחתון** ב-\( n \)
    זוגי, לא הממוצע של סעיף א. עם \( p = 0.99 \) ו-\( n < 100 \) המקום הוא \( n \), כלומר המקסימום :
    "p99" מתחיל להיות שונה מהמקסימום רק ממאה ערכים. יש גם הגדרות עם **אינטרפולציה** בין שני
    ערכים שכנים (כמו בחציון של סעיף א) ; הדרגה הקרובה מחזירה תמיד ערך שבאמת נמדד, וזה מה
    שרוצים ממוניטור של latency.

    **אותו מבנה, יעד אחר.** בסעיף א הראש של `low` היה הערך במקום \( |\text{low}| \) של הרשימה
    הממוינת, בזכות שמורת הסדר. זה נכון לכל גודל של `low`, לא רק \( \lceil n / 2 \rceil \). אז
    נשמור על \( |\text{low}| = t \) עם \( t = \max(1, \lceil p \cdot n \rceil) \), והאחוזון הוא הראש
    של `low`, תמיד, בלי ממוצע.

    **היעד זז לאט.** כשנכנס ערך, \( n \) גדל ב-1 ו-\( t \) גדל ב-\( \lceil p (n + 1) \rceil - \lceil p n \rceil \),
    שהוא 0 או 1, כי \( p \le 1 \). אחרי הדחיפה דרך `low`, ‏\( |\text{low}| \) הוא עדיין היעד הישן, ולכן
    חסר לה לכל היותר ערך אחד, ואף פעם לא עודף : בדיקה אחת, `if` ולא `while`, ולכל היותר מעבר
    אחד חזרה מ-`high`.

    **חשבון שלם.** \( p \) ניתן כשבר \( \text{num} / \text{den} \) (למשל \( 9/10 \), או \( 99/100 \)),
    ו-\( \lceil p \cdot n \rceil = \lfloor (\text{num} \cdot n + \text{den} - 1) / \text{den} \rfloor \)
    בחלוקה שלמה. עם מספר עשרוני, `math.ceil(0.07 * 100)` הוא 8, כי \( 0.07 \cdot 100 \) בנקודה
    צפה הוא \( 7.000000000000001 \) : מקום אחד יותר מדי, בדיוק כשהמכפלה אמורה להיות שלמה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **דוחפים דרך `low` :** ‏\( x \) נכנס ל-`low`, והראש של `low` עובר ל-`high`, כמו בסעיף א.
       ‏\( |\text{low}| \) לא השתנה.
    2. **היעד :** ‏\( n \) גדל ב-1, ו-\( t = \max(1, \lceil p \cdot n \rceil) \) מחושב מחדש, בחשבון שלם.
    3. **השלמה :** אם \( |\text{low}| < t \), הראש של `high` חוזר ל-`low`. זה קורה לכל היותר פעם
       אחת.
    4. **האחוזון :** הראש של `low`.

    </div>

    על הזרם של סעיף א עם \( p = 9/10 \). בעמודה האחרונה הרשימה הממוינת, והמקום \( t \) מודגש.
    עד תשעה ערכים \( t = n \), ולכן `high` ריקה והאחוזון הוא המקסימום; בערך העשירי
    \( t = \lceil 9 \rceil = 9 \), ובפעם הראשונה ערך נשאר ב-`high` :

    <!-- gen 4 -->

    | ‏n | ‏x | היעד ⌈9n/10⌉ | חוזר ל-low | ‏low (הראש ראשון) | ‏high (הראש ראשון) | האחוזון | הרשימה הממוינת |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏1 | ‏5 | ‏1 | ‏5 | ‏<span dir="ltr"><b>5</b></span> | ריקה | **‏5** | ‏<span dir="ltr"><b>5</b></span> |
    | ‏2 | ‏15 | ‏2 | ‏15 | ‏<span dir="ltr"><b>15</b> 5</span> | ריקה | **‏15** | ‏<span dir="ltr">5 <b>15</b></span> |
    | ‏3 | ‏1 | ‏3 | ‏15 | ‏<span dir="ltr"><b>15</b> 5 1</span> | ריקה | **‏15** | ‏<span dir="ltr">1 5 <b>15</b></span> |
    | ‏4 | ‏3 | ‏4 | ‏15 | ‏<span dir="ltr"><b>15</b> 5 3 1</span> | ריקה | **‏15** | ‏<span dir="ltr">1 3 5 <b>15</b></span> |
    | ‏5 | ‏8 | ‏5 | ‏15 | ‏<span dir="ltr"><b>15</b> 8 5 3 1</span> | ריקה | **‏15** | ‏<span dir="ltr">1 3 5 8 <b>15</b></span> |
    | ‏6 | ‏7 | ‏6 | ‏15 | ‏<span dir="ltr"><b>15</b> 8 7 5 3 1</span> | ריקה | **‏15** | ‏<span dir="ltr">1 3 5 7 8 <b>15</b></span> |
    | ‏7 | ‏9 | ‏7 | ‏15 | ‏<span dir="ltr"><b>15</b> 9 8 7 5 3 1</span> | ריקה | **‏15** | ‏<span dir="ltr">1 3 5 7 8 9 <b>15</b></span> |
    | ‏8 | ‏10 | ‏8 | ‏15 | ‏<span dir="ltr"><b>15</b> 10 9 8 7 5 3 1</span> | ריקה | **‏15** | ‏<span dir="ltr">1 3 5 7 8 9 10 <b>15</b></span> |
    | ‏9 | ‏20 | ‏9 | ‏20 | ‏<span dir="ltr"><b>20</b> 15 10 9 8 7 5 3 1</span> | ריקה | **‏20** | ‏<span dir="ltr">1 3 5 7 8 9 10 15 <b>20</b></span> |
    | ‏10 | ‏2 | ‏9 | אין צורך | ‏<span dir="ltr"><b>15</b> 10 9 8 7 5 3 2 1</span> | ‏<span dir="ltr"><b>20</b></span> | **‏15** | ‏<span dir="ltr">1 2 3 5 7 8 9 10 <b>15</b> 20</span> |

    <!-- /gen -->

    ועם \( p = 1/4 \). היעד \( \lceil n / 4 \rceil \) גדל רק כל ארבעה ערכים, ובשאר ההכנסות שום
    דבר לא חוזר מ-`high` : הערך שנדחף דרך `low` מוצא את מקומו באחת הערימות, והראש של `low`
    נשאר הערך במקום \( t \) :

    <!-- gen 5 -->

    | ‏n | ‏x | היעד ⌈1n/4⌉ | חוזר ל-low | ‏low (הראש ראשון) | ‏high (הראש ראשון) | האחוזון | הרשימה הממוינת |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏1 | ‏5 | ‏1 | ‏5 | ‏<span dir="ltr"><b>5</b></span> | ריקה | **‏5** | ‏<span dir="ltr"><b>5</b></span> |
    | ‏2 | ‏15 | ‏1 | אין צורך | ‏<span dir="ltr"><b>5</b></span> | ‏<span dir="ltr"><b>15</b></span> | **‏5** | ‏<span dir="ltr"><b>5</b> 15</span> |
    | ‏3 | ‏1 | ‏1 | אין צורך | ‏<span dir="ltr"><b>1</b></span> | ‏<span dir="ltr"><b>5</b> 15</span> | **‏1** | ‏<span dir="ltr"><b>1</b> 5 15</span> |
    | ‏4 | ‏3 | ‏1 | אין צורך | ‏<span dir="ltr"><b>1</b></span> | ‏<span dir="ltr"><b>3</b> 5 15</span> | **‏1** | ‏<span dir="ltr"><b>1</b> 3 5 15</span> |
    | ‏5 | ‏8 | ‏2 | ‏3 | ‏<span dir="ltr"><b>3</b> 1</span> | ‏<span dir="ltr"><b>5</b> 8 15</span> | **‏3** | ‏<span dir="ltr">1 <b>3</b> 5 8 15</span> |
    | ‏6 | ‏7 | ‏2 | אין צורך | ‏<span dir="ltr"><b>3</b> 1</span> | ‏<span dir="ltr"><b>5</b> 7 8 15</span> | **‏3** | ‏<span dir="ltr">1 <b>3</b> 5 7 8 15</span> |
    | ‏7 | ‏9 | ‏2 | אין צורך | ‏<span dir="ltr"><b>3</b> 1</span> | ‏<span dir="ltr"><b>5</b> 7 8 9 15</span> | **‏3** | ‏<span dir="ltr">1 <b>3</b> 5 7 8 9 15</span> |
    | ‏8 | ‏10 | ‏2 | אין צורך | ‏<span dir="ltr"><b>3</b> 1</span> | ‏<span dir="ltr"><b>5</b> 7 8 9 10 15</span> | **‏3** | ‏<span dir="ltr">1 <b>3</b> 5 7 8 9 10 15</span> |
    | ‏9 | ‏20 | ‏3 | ‏5 | ‏<span dir="ltr"><b>5</b> 3 1</span> | ‏<span dir="ltr"><b>7</b> 8 9 10 15 20</span> | **‏5** | ‏<span dir="ltr">1 3 <b>5</b> 7 8 9 10 15 20</span> |
    | ‏10 | ‏2 | ‏3 | אין צורך | ‏<span dir="ltr"><b>3</b> 2 1</span> | ‏<span dir="ltr"><b>5</b> 7 8 9 10 15 20</span> | **‏3** | ‏<span dir="ltr">1 2 <b>3</b> 5 7 8 9 10 15 20</span> |

    <!-- /gen -->

    בהכנסה החמישית (8) היעד עולה מ-1 ל-2 : הראש של `low` (3) עובר ל-`high`, ומיד חוזר, כי
    \( |\text{low}| = 1 < 2 \). בהכנסה השישית (7) היעד נשאר 2, ‏7 עובר ל-`high` ונשאר שם : הראש
    של `low` עדיין 3, הערך השני בגודלו.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="class StreamQuantile" linenums="1" hl_lines="12 14 15"
        class StreamQuantile:
            """The p-quantile of every prefix, p = num / den, by the nearest rank: low holds
            the ceil(p n) smallest values (at least one), so the quantile is low's top."""

            def __init__(self, num: int, den: int):
                self.num, self.den, self.n = num, den, 0
                self.low: list[int] = []        # the ceil(p n) smallest values, negated
                self.high: list[int] = []       # the rest

            def add(self, x: int) -> None:
                heappush(self.low, -x)
                heappush(self.high, -heappop(self.low))         # (1)!
                self.n += 1
                target = max(1, -(-self.num * self.n // self.den))    # (2)!
                if len(self.low) < target:                      # (3)!
                    heappush(self.low, -heappop(self.high))

            def quantile(self) -> int:
                return -self.low[0]


        def stream_quantiles(nums: list[int], num: int, den: int) -> list[int]:
            """The p-quantile after every value."""
            sq = StreamQuantile(num, den)
            out = []
            for x in nums:
                sq.add(x)
                out.append(sq.quantile())
            return out
        ```

        1. הדחיפה דרך `low` של סעיף א. ‏`low` באותו גודל כמו לפני ההכנסה.
        2. ‏`-(-a // b)` הוא \( \lceil a / b \rceil \) בחשבון שלם : החלוקה השלמה של Python מעגלת כלפי מטה.
        3. היעד גדל לכל היותר ב-1, ולכן `if` מספיק : מעבר אחד חזרה, או כלום.

    === "SystemVerilog"
        ```systemverilog title="class StreamQuantile" linenums="1" hl_lines="8 10 12"
        class StreamQuantile;                   // the p-quantile, p = num / den, by the nearest rank
          heap_t low = new(1), high = new(0);   // low holds the ceil(p n) smallest values
          int num, den, n = 0;
          function new(int num, int den); this.num = num; this.den = den; endfunction
          function void add(int x);
            int target;
            low.push('{x, n});
            high.push(low.pop());                                  // (1)!
            n++;
            target = (num * n + den - 1) / den;                    // (2)!
            if (target < 1) target = 1;
            if (low.size() < target) low.push(high.pop());         // (3)!
          endfunction
          function int quantile(); return low.top().v; endfunction
        endclass
        ```

        1. הדחיפה דרך `low` של סעיף א. ‏`low` באותו גודל כמו לפני ההכנסה.
        2. ‏\( \lceil \text{num} \cdot n / \text{den} \rceil \) בחשבון שלם, בלי נקודה צפה.
        3. היעד גדל לכל היותר ב-1, ולכן `if` מספיק : מעבר אחד חזרה, או כלום.

    #### למה זה נכון { .sol-proof }

    **שמורת הסדר** נשמרת בדיוק כמו בסעיף א : הצעדים הם אותם צעדים, דחיפה דרך `low` ומעבר
    של ראש מ-`high` ל-`low`, ושניהם הוכחו שם בלי להסתמך על הגדלים.

    **שמורת הגודל** היא עכשיו \( |\text{low}| = t(n) = \max(1, \lceil p n \rceil) \). באינדוקציה :
    לפני ההכנסה \( |\text{low}| = t(n) \). אחרי הדחיפה והמעבר \( |\text{low}| = t(n) \) עדיין
    (אחד נכנס, אחד יצא). היעד החדש \( t(n + 1) \) מקיים \( t(n) \le t(n + 1) \le t(n) + 1 \) :
    הפונקציה \( \lceil p n \rceil \) לא יורדת, ועולה לכל היותר ב-1 כי
    \( p(n + 1) - pn = p \le 1 \) ושני תקרות של מספרים שהפרשם לכל היותר 1 נבדלות לכל היותר ב-1;
    ה-\( \max \) עם 1 לא משנה את זה. אם \( t(n + 1) = t(n) + 1 \), המעבר חזרה משלים את `low`;
    אחרת לא צריך כלום. גם \( |\text{high}| = n - t \ge 0 \) : כש-\( t = n \) (למשל \( p = 1 \))
    `high` ריקה אחרי המעבר חזרה, וכשחסר ל-`low`, ‏`high` לא ריקה, כי \( |\text{low}| < t \le n \).

    **האחוזון :** לפי שמורת הסדר הראש של `low` הוא הערך במקום \( |\text{low}| = \lceil p n \rceil \)
    של הרשימה הממוינת. זו ההגדרה.

    **מקרי הקצה :** ‏\( p = 0 \) נותן \( t = 1 \) תמיד, והראש של `low` הוא המינימום. ‏\( p = 1 \)
    נותן \( t = n \), ‏`high` ריקה והראש של `low` הוא המקסימום. ‏\( p = 1/2 \) נותן
    \( t = \lceil n / 2 \rceil \), בדיוק הגודל של `low` בסעיף א : אותן ערימות, ורק השאילתה שונה
    (הראש של `low` לבד, במקום הממוצע ב-\( n \) זוגי).

    #### סיבוכיות { .sol-cost }

    - **הכנסה :** ‏\( O(\log n) \), כמו בסעיף א : לכל היותר חמש פעולות ערימה.
    - **שאילתה :** ‏\( O(1) \). **זיכרון :** ‏\( O(n) \).
    - **הכללה :** כמה אחוזונים בבת אחת (p50, p90, p99) הם כמה מבנים כאלה, או מבנה אחד
      שמחזיק את הכול (שאלות ההמשך).

    **נסו בעצמכם.** אותה תיבה עם מחוון ל-\( p \). כל ערך הוא שלושה צעדים : הדחיפה ל-`low`,
    המעבר ל-`high`, וההשלמה ליעד עם האחוזון. שימו לב איך היעד זז ב-0 או ב-1 :

    <div class="explorer" data-kind="twoheaps" data-mode="b" data-nums="5 15 1 3 8 7 9 10 20 2" data-p="25"></div>

---

### סעיף ג – האחוזון בחלון של W הערכים האחרונים

??? tip "רמז 1"
    כשנכנס ערך חדש, הערך שנכנס לפני \( W \) צעדים צריך לצאת מהחשבון. באיזו ערימה הוא, ואיפה
    בתוכה? מה עולה למחוק איבר מאמצע ערימה?

??? tip "רמז 2"
    אל תמחקו. סמנו את הערך כ"מת" והשאירו אותו בערימה, אבל אל תספרו אותו בגודל. מתי בכל זאת
    חייבים לזרוק אותו באמת?

<div class="selfcheck" data-answer="9" data-show="9 : החלון האחרון הוא 9 10 20 2, ממוין 2 9 10 20, והמקום ⌈0.5 · 4⌉ = 2 הוא 9" data-hint="החלון האחרון הוא ארבעת הערכים האחרונים. מיינו אותם וקחו את המקום ⌈p · W⌉." markdown>
בזרם <span dir="ltr">5 15 1 3 8 7 9 10 20 2</span> עם \( W = 4 \) ו-\( p = 1/2 \), מה האחוזון
אחרי הערך האחרון?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        **מחיקה עצלה** (lazy deletion) : ערך שיצא מהחלון נשאר בערימה, מסומן כמת, ולא נספר.
        שומרים לכל ערימה את מספר הערכים **החיים** בה, ואת הערימה שבה כל ערך חי יושב. ראש מת
        נזרק לפני שקוראים את הראש. היעד הוא \( \lceil p \cdot m \rceil \) עם \( m = \min(n, W) \)
        הערכים החיים, ולכל היותר מעבר אחד בין הערימות בכל הכנסה. ערימה שבה יותר מתים מחיים
        נבנית מחדש מהחיים שלה. ‏\( O(\log W) \) להכנסה בממוצע, \( O(W) \) זיכרון. בדוגמה עם
        \( W = 4 \) ו-\( p = 1/2 \) האחוזון האחרון הוא 9.

    <!-- cost: הכנסה \( O(\log W) \) בממוצע | שאילתה \( O(1) \) | זיכרון \( O(W) \) -->

    #### הרעיון { .sol-idea }

    **מה חסר.** ערימה יודעת להוציא רק את הראש. הערך שיוצא מהחלון, זה שנכנס לפני \( W \) צעדים,
    יכול להיות בכל מקום בכל אחת מהערימות. למצוא אותו עולה \( O(W) \) (סריקה), ומחיקה מאמצע
    הערימה אפשרית רק אם יודעים את המקום שלו במערך, וגם אז דורשת תיקון של העץ. שני מבנים
    **ממוינים** שתומכים במחיקה (עצים מאוזנים, `multiset` ב-C++) פותרים את זה ישירות ב-\( O(\log W) \),
    אבל אין כאלה ב-Python וב-SystemVerilog. הפתרון עם ערימות :

    **מחיקה עצלה.** ערך שיצא מהחלון **נשאר** בערימה, ורק מסומן כמת. כל מה שצריך לדעת זה
    באיזו ערימה הוא חי, כדי להוריד את מספר **החיים** בה ב-1. לכן כל ערך נשמר עם מספר ההגעה
    שלו \( i \) (כך גם כפילויות נבדלות זו מזו), ומילון `side` מחזיק לכל ערך חי באיזו ערימה הוא.
    כשערך עובר בין הערימות, `side` שלו מתעדכן; כשהוא יוצא מהחלון, הרשומה שלו נמחקת : ערך
    שאין לו רשומה הוא מת. **הגדלים** של סעיף ב הם מעכשיו הגדלים החיים, `live`, ולא אורך
    המערך.

    **ניקוי הראש.** מת שיושב עמוק בערימה לא מפריע : הוא לא נספר, והשמורה של הסדר עדיין
    נכונה על כל האיברים, חיים ומתים, כי המעברים לא השתנו. מת מפריע רק כשהוא **בראש**, כי אז
    הראש אינו הערך החי הקיצוני. לכן לפני כל קריאה של ראש, לפני מעבר ולפני התשובה, זורקים את
    הראש כל עוד הוא מת (**prune**). כל מת נזרק פעם אחת לכל היותר, ולכן זה \( O(\log W) \) לכל
    ערך, בממוצע.

    **בנייה מחדש.** בלי שום דבר נוסף המתים יכולים להצטבר : בזרם עולה עם \( W = 2 \), הערכים
    הישנים ב-`low` לעולם לא מגיעים לראש (הראש הוא תמיד החדש), והערימה גדלה ל-\( O(n) \). לכן
    כשבערימה יש יותר מתים מחיים, בונים אותה מחדש מהחיים שלה, \( O(W) \). זה קורה רק אחרי
    לפחות \( \text{live} + 1 \) מחיקות מאז הבנייה הקודמת, ולכן העלות מתחלקת על המחיקות :
    \( O(1) \) לכל אחת, בממוצע. כל ערימה מחזיקה לכל היותר \( 2 \cdot \text{live} + 1 \) איברים,
    כלומר \( O(W) \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הערך הישן יוצא :** כשכבר יש \( W \) ערכים, הערך \( i - W \) מת : הרשומה שלו ב-`side`
       נמחקת, ומספר החיים בערימה שלו יורד ב-1. שום דבר לא זז בערימות.
    2. **דוחפים דרך `low` :** ‏\( x \) נכנס ל-`low` עם המספר \( i \) ונרשם בה, והראש **החי** של
       `low` (אחרי ניקוי) עובר ל-`high`. ‏`side` של מה שעבר מתעדכן.
    3. **היעד :** ‏\( m = \min(n, W) \) ערכים חיים, \( t = \max(1, \lceil p \cdot m \rceil) \). אם
       ל-`low` חסר ערך חי, הראש החי של `high` עובר אליה; אם יש לה עודף, הראש החי שלה עובר
       ל-`high`. לכל היותר מעבר אחד.
    4. **בנייה מחדש :** ערימה שבה יותר מתים מחיים נבנית מחדש מהחיים שלה.
    5. **האחוזון :** הראש החי של `low`, אחרי ניקוי.

    </div>

    על הזרם של סעיף א עם \( W = 4 \) ו-\( p = 1/2 \) (החציון התחתון של החלון, היעד
    \( \lceil 4 / 2 \rceil = 2 \) מהערך הרביעי). ערך מת כתוב מחוק :

    <!-- gen 6 -->

    | ‏i | ‏x | יוצא מהחלון | החלון | היעד | ‏low (הראש ראשון) | ‏high (הראש ראשון) | נזרקו / נבנתה מחדש | האחוזון |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏0 | ‏5 | אין | ‏<span dir="ltr">5</span> | ‏1 | ‏<span dir="ltr"><b>5</b></span> | ריקה | לא | **‏5** |
    | ‏1 | ‏15 | אין | ‏<span dir="ltr">5 15</span> | ‏1 | ‏<span dir="ltr"><b>5</b></span> | ‏<span dir="ltr"><b>15</b></span> | לא | **‏5** |
    | ‏2 | ‏1 | אין | ‏<span dir="ltr">5 15 1</span> | ‏2 | ‏<span dir="ltr"><b>5</b> 1</span> | ‏<span dir="ltr"><b>15</b></span> | לא | **‏5** |
    | ‏3 | ‏3 | אין | ‏<span dir="ltr">5 15 1 3</span> | ‏2 | ‏<span dir="ltr"><b>3</b> 1</span> | ‏<span dir="ltr"><b>5</b> 15</span> | לא | **‏3** |
    | ‏4 | ‏8 | ‏5 (מ-high) | ‏<span dir="ltr">15 1 3 8</span> | ‏2 | ‏<span dir="ltr"><b>3</b> 1</span> | ‏<span dir="ltr"><s>5</s> 8 15</span> | לא | **‏3** |
    | ‏5 | ‏7 | ‏15 (מ-high) | ‏<span dir="ltr">1 3 8 7</span> | ‏2 | ‏<span dir="ltr"><b>3</b> 1</span> | ‏<span dir="ltr"><s>5</s> 7 8 <s>15</s></span> | לא | **‏3** |
    | ‏6 | ‏9 | ‏1 (מ-low) | ‏<span dir="ltr">3 8 7 9</span> | ‏2 | ‏<span dir="ltr"><b>7</b> 3 <s>1</s></span> | ‏<span dir="ltr"><b>8</b> 9 <s>15</s></span> | נזרק מ-‏<span dir="ltr">high: 5</span> | **‏7** |
    | ‏7 | ‏10 | ‏3 (מ-low) | ‏<span dir="ltr">8 7 9 10</span> | ‏2 | ‏<span dir="ltr"><b>8</b> 7 <s>3</s> <s>1</s></span> | ‏<span dir="ltr"><b>9</b> 10 <s>15</s></span> | לא | **‏8** |
    | ‏8 | ‏20 | ‏8 (מ-low) | ‏<span dir="ltr">7 9 10 20</span> | ‏2 | ‏<span dir="ltr"><b>9</b> 7</span> | ‏<span dir="ltr"><b>10</b> <s>15</s> 20</span> | נבנתה מחדש : low | **‏9** |
    | ‏9 | ‏2 | ‏7 (מ-low) | ‏<span dir="ltr">9 10 20 2</span> | ‏2 | ‏<span dir="ltr"><b>9</b> <s>7</s> 2</span> | ‏<span dir="ltr"><b>10</b> <s>15</s> 20</span> | לא | **‏9** |

    <!-- /gen -->

    בצעד 4 נכנס 8 ויוצא 5, שחי ב-`high` : הוא נשאר שם, מחוק, ו-`high` סופרת 2 חיים. בצעד 6
    נכנס 9 ויוצא 1 מ-`low`, שנשארת עם חי אחד (3) ויעד 2 : הראש של `high` צריך לעבור, אבל הוא
    ה-5 המת, ולכן הוא נזרק קודם, ואז 7 עובר. בצעד 8 יוצא 8, השלישי שמת ב-`low` (אחרי 1 ו-3),
    מול שני חיים : ‏`low` נבנית מחדש, ונשארים בה רק 9 ו-7. ה-15 המת ב-`high` נשאר שם עד הסוף,
    כי הוא אף פעם לא מגיע לראש ו-`high` אף פעם לא מגיעה ליותר מתים מחיים.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="class WindowQuantile" linenums="1" hl_lines="18 37 39 42 46"
        from heapq import heapify


        class WindowQuantile:
            """The p-quantile of the last w values: the two heaps with lazy deletion. Every
            value carries its arrival number i; side[i] names the heap of a live value, and
            live counts the live values in each heap."""

            def __init__(self, w: int, num: int, den: int):
                self.w, self.num, self.den, self.n = w, num, den, 0
                self.heaps = {"low": [], "high": []}     # (-v, -i) in low, (v, i) in high
                self.side: dict[int, str] = {}
                self.live = {"low": 0, "high": 0}

            def _prune(self, s: str) -> None:
                """Dead values on top are thrown away."""
                h = self.heaps[s]
                while h and abs(h[0][1]) not in self.side:          # (1)!
                    heappop(h)

            def _move(self, src: str, dst: str) -> None:
                """The live top of src goes to dst."""
                self._prune(src)
                v, i = heappop(self.heaps[src])
                if src == "low":
                    v, i = -v, -i
                heappush(self.heaps[dst], (-v, -i) if dst == "low" else (v, i))
                self.side[i] = dst
                self.live[src] -= 1
                self.live[dst] += 1

            def add(self, x: int) -> None:
                i = self.n
                self.n += 1
                heappush(self.heaps["low"], (-x, -i))
                self.side[i], self.live["low"] = "low", self.live["low"] + 1
                self._move("low", "high")
                if i >= self.w:                                     # (2)!
                    self.live[self.side.pop(i - self.w)] -= 1
                m = min(self.n, self.w)
                target = max(1, -(-self.num * m // self.den))
                if self.live["low"] < target:                       # (3)!
                    self._move("high", "low")
                elif self.live["low"] > target:
                    self._move("low", "high")
                for s, h in self.heaps.items():                     # (4)!
                    if len(h) > 2 * self.live[s]:
                        h[:] = [e for e in h if abs(e[1]) in self.side]
                        heapify(h)

            def quantile(self) -> int:
                self._prune("low")
                return -self.heaps["low"][0][0]


        def window_quantiles(nums: list[int], w: int, num: int, den: int) -> list[int]:
            """The p-quantile of the last w values, after every value."""
            wq = WindowQuantile(w, num, den)
            out = []
            for x in nums:
                wq.add(x)
                out.append(wq.quantile())
            return out
        ```

        1. ב-`low` הזוג הוא \( (-v, -i) \), ולכן `abs` מחזיר את מספר ההגעה בשתי הערימות (לא את הערך, שיכול להיות שלילי). ערך בלי רשומה ב-`side` מת.
        2. הערך \( i - w \) יוצא מהחלון : הרשומה שלו נמחקת, והחיים בערימה שלו יורדים ב-1. שום דבר לא זז.
        3. היעד על החיים. כשהחלון מלא היציאה יכולה להשאיר ל-`low` חסר או עודף של ערך אחד.
        4. יותר מתים מחיים : הערימה נבנית מחדש מהחיים בלבד, \( O(W) \), לעיתים רחוקות.

    === "SystemVerilog"
        ```systemverilog title="class WindowQuantile" linenums="1" hl_lines="10 17 31 36 37"
        class WindowQuantile;                   // the p-quantile of the last w values, lazy deletion
          heap_t low = new(1), high = new(0);
          int w, num, den, n = 0;
          int side[int];                        // arrival -> 0 (low) or 1 (high), for every live value
          int live[2];                          // live values in low and in high
          function new(int w, int num, int den); this.w = w; this.num = num; this.den = den; endfunction
          function heap_t heap(int s); return s ? high : low; endfunction
          function void prune(int s);           // dead values on top are thrown away
            heap_t h = heap(s);
            while (h.size() > 0 && !side.exists(h.top().id)) void'(h.pop());   // (1)!
          endfunction
          function void move(int src, int dst); // the live top of src goes to dst
            item_t x;
            prune(src);
            x = heap(src).pop();
            heap(dst).push(x);
            side[x.id] = dst; live[src]--; live[dst]++;
          endfunction
          function void rebuild(int s);         // more dead than live: keep only the live values
            item_t keep[$];
            heap_t h = heap(s);
            if (h.size() <= 2 * live[s]) return;
            foreach (h.a[i]) if (side.exists(h.a[i].id)) keep.push_back(h.a[i]);
            h.a = {};
            foreach (keep[i]) h.push(keep[i]);
          endfunction
          function void add(int x);
            int m, target;
            low.push('{x, n}); side[n] = 0; live[0]++;
            move(0, 1);
            if (n >= w) begin live[side[n - w]]--; side.delete(n - w); end   // (2)!
            n++;
            m = n < w ? n : w;
            target = (num * m + den - 1) / den;
            if (target < 1) target = 1;
            if (live[0] < target) move(1, 0);                      // (3)!
            else if (live[0] > target) move(0, 1);
            rebuild(0); rebuild(1);
          endfunction
          function int quantile(); prune(0); return low.top().v; endfunction
        endclass
        ```

        1. ערך בלי רשומה ב-`side` מת. ראש מת נזרק, עד שהראש חי (או הערימה ריקה).
        2. הערך \( n - w \) יוצא מהחלון : החיים בערימה שלו יורדים ב-1, הרשומה נמחקת, ושום דבר לא זז.
        3. היעד על החיים. כשהחלון מלא, \( m = w \) קבוע, והיציאה יכולה להשאיר ל-`low` חסר או עודף של אחד.

    #### למה זה נכון { .sol-proof }

    **שמורת הסדר על כל האיברים.** המעברים הם אותם מעברים של סעיפים א ו-ב, ראש מערימה אחת
    לשנייה, רק שלפניהם נזרקים ראשים מתים. זריקה של ראש לא פוגעת בשמורה (היא על זוגות של
    איברים, ופחות איברים זה פחות זוגות). לכן כל איבר ב-`low`, חי או מת, קטן מכל איבר ב-`high` או
    שווה לו, ובפרט כל **חי** ב-`low` קטן מכל **חי** ב-`high`.

    **הספירה נכונה.** ‏`live[s]` סופר בדיוק את האיברים החיים בערימה \( s \) : הוא עולה כשערך נדחף או
    עובר אליה, יורד כשערך עובר ממנה או מת בה, ו-`side` אומר באיזו ערימה הערך חי ברגע שהוא
    מת. ערך שעבר בין הערימות ו-`side` שלו עודכן, נמצא פיזית רק בערימה החדשה, ולכן אין מצב
    שערך "חי" לפי `side` יושב בערימה אחרת.

    **הראש החי הוא הקיצוני.** אחרי ניקוי, הראש של `low` חי, והוא המקסימום של כל האיברים
    ב-`low`, ובפרט של החיים. לכן, עם \( |\text{live}_{\text{low}}| = t \) ושמורת הסדר על החיים,
    הוא הערך במקום \( t = \lceil p \cdot m \rceil \) בין \( m \) הערכים החיים, הערכים של החלון.

    **לכל היותר מעבר אחד.** לפני ההכנסה \( \text{live}_{\text{low}} = t(m) \). הדחיפה דרך `low` לא
    משנה אותה. כשהחלון לא מלא אין יציאה, \( m \) גדל ב-1 ו-\( t \) ב-0 או ב-1, כמו בסעיף ב.
    כשהחלון מלא, \( m = W \) ו-\( t \) קבוע, והיציאה מורידה את החיים של `low` ב-1 או ב-0 :
    חסר אחד, או בדיוק. בשני המקרים מעבר אחד לכל היותר, לכל כיוון. המעבר תמיד אפשרי : כשחסר
    ל-`low`, ל-`high` יש \( m - \text{live}_{\text{low}} > 0 \) חיים, וכשיש עודף, ל-`low` יש לפחות
    \( t + 1 \ge 2 \) חיים.

    **הבנייה מחדש** מסננת את המתים ובונה ערימה מהחיים : הסדר נשמר (אותם ערכים, פחות), הספירה
    לא משתנה (המתים לא נספרו), ואחריה אין בערימה מתים.

    #### סיבוכיות { .sol-cost }

    - **הכנסה :** ‏\( O(\log W) \) **בממוצע** (אמורטיזציה). בכל הכנסה עד חמש פעולות ערימה על ערימה של
      \( O(W) \) איברים. הניקוי זורק כל מת פעם אחת לכל היותר, \( O(\log W) \) לכל ערך שנכנס. הבנייה
      מחדש עולה \( O(W) \), אבל מתרחשת רק אחרי שלפחות \( \text{live} + 1 \) ערכים מתו מאז הקודמת,
      ולכן \( O(1) \) לכל מוות. צעד בודד יכול לעלות \( O(W) \), הממוצע לא.
    - **שאילתה :** ‏\( O(1) \) אחרי הניקוי (שהוא חלק מהאמורטיזציה).
    - **זיכרון :** ‏\( O(W) \) : כל ערימה לכל היותר \( 2 \cdot \text{live} + 1 \) איברים, והמילון
      `side` בגודל \( W \). בלי הבנייה מחדש הזיכרון היה \( O(n) \) במקרה הגרוע.
    - **החלופה :** שני עצים מאוזנים (או `multiset`), מחיקה אמיתית ב-\( O(\log W) \) במקרה הגרוע
      לכל צעד, בלי אמורטיזציה, ועם איטרטור לגבול במקום שני ראשים. כשיש כאלה בשפה זו תשובה טובה
      באותה מידה.

    **נסו בעצמכם.** החלון מסומן על הזרם, ערך שיצא מהחלון נשאר בערימה מחוק ואפור עד שהוא נזרק,
    והגדלים שמוצגים הם החיים :

    <div class="explorer" data-kind="twoheaps" data-mode="c" data-nums="5 15 1 3 8 7 9 10 20 2" data-w="4" data-p="50"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : למיין בכל שאילתה"
    ‏`sorted(values)[n // 2]` נכון, אבל \( O(n \log n) \) לכל שאילתה, ועם שאילתה אחרי כל הכנסה
    \( O(n^2 \log n) \) לכל הזרם. גם הכנסה למערך ממוין (`bisect.insort`) היא \( O(n) \) בגלל
    ההזזה. שתי הערימות נותנות \( O(\log n) \) להכנסה ו-\( O(1) \) לשאילתה, בלי לדעת כמה ערכים
    יגיעו.

??? trap "מלכודת : לשכוח את הסימן בערימת המקסימום"
    ‏`heapq` היא ערימת מינימום. מי שדוחף ל-`low` את \( x \) במקום \( -x \) מקבל בראש את
    **המינימום** של החצי הקטן, והחציון יוצא שגוי כבר בערך השלישי : ב-<span dir="ltr">5 15 1</span>
    הראש של `low` יהיה 1 במקום 5. כל כניסה ויציאה מ-`low` הופכת סימן, כולל הקריאה של הראש
    ב-`median`. ב-SystemVerilog, שבה הערימה כתובה ביד, הכיוון הוא דגל אחד במחלקה.

??? trap "מלכודת : לתת לגדלים להתרחק בשניים"
    מי שמכניס לפי השוואה עם הראשים ("אם \( x \) קטן מהראש של `low`, ל-`low`, אחרת ל-`high`")
    חייב לאזן אחרי **כל** הכנסה : שתי הכנסות רצופות לאותה ערימה בלי איזון נותנות הפרש 2, והראש
    כבר לא במקום \( \lceil n / 2 \rceil \). הדחיפה דרך `low` משאירה את הגדלים במקום, והאיזון הוא
    בדיקה אחת. הבדיקה הטובה : אחרי כל הכנסה \( |\text{low}| - |\text{high}| \in \{0, 1\} \), כטענה
    (assertion) בבדיקות.

??? trap "מלכודת : floor במקום ceil, ו-ceil בנקודה צפה"
    המקום של האחוזון הוא \( \lceil p \cdot n \rceil \). עם \( \lfloor p \cdot n \rfloor \) מקבלים
    מקום 0 ב-\( n \) קטן, ובמכפלה שלמה (\( p = 0.5 \), ‏\( n = 4 \)) אותו ערך, אבל ב-\( p = 0.9 \)
    ו-\( n = 5 \) את המקום 4 במקום 5. ו-`ceil` על מספר עשרוני טועה בדיוק כשהמכפלה שלמה :
    `math.ceil(0.07 * 100)` הוא 8. השבר \( \text{num} / \text{den} \) וחלוקה שלמה,
    \( \lfloor (\text{num} \cdot n + \text{den} - 1) / \text{den} \rfloor \), פותרים את שתי הבעיות.

??? trap "מלכודת : דרגה קרובה מול אינטרפולציה"
    יש כמה הגדרות לאחוזון : הדרגה הקרובה (כאן), אינטרפולציה ליניארית בין שני שכנים (ברירת
    המחדל של `numpy.percentile`), ועוד. על אותם נתונים הן נותנות מספרים שונים, ובמוניטור של
    latency צריך לומר במפורש איזו הגדרה מדווחים. בדוח הסופי מול מספר של `numpy` ההבדל ייראה
    כמו באג.

??? trap "מלכודת : למחוק מאמצע ערימה"
    בסעיף ג יש מי שמחפשים את הערך שיצא בערימה ומוחקים אותו מהמערך (`list.remove`) : זה
    \( O(W) \) לחיפוש, ואחרי המחיקה המערך כבר לא ערימה, וצריך `heapify`, שוב \( O(W) \). מחיקה
    עצלה משאירה את הערימה שלמה, ומשלמת רק כשהמת מגיע לראש.

??? followup "שאלות המשך"
    - **זיכרון קבוע :** הזרם ארוך ממה שנכנס לזיכרון. איך מקבלים חציון או אחוזון **מקורב**
      בזיכרון קבוע?

        ??? fu-answer "תשובה"
            היסטוגרמה עם תאים קבועים (למשל תא לכל 1 µs של latency, או תאים לוגריתמיים) : הכנסה
            \( O(1) \), והאחוזון הוא התא שבו הספירה המצטברת עוברת \( p \cdot n \), בדיוק של רוחב
            תא. או דגימת מאגר (reservoir sampling) של \( k \) ערכים אקראיים מהזרם, והאחוזון של
            המדגם, בשגיאה של \( O(1 / \sqrt{k}) \) בדרגה. ‏t-digest ו-KLL הם המבנים המקובלים לזה.

    - **ערכים שלמים קטנים :** הערכים הם שלמים מ-0 עד \( R \) (למשל latency במחזורים, עד 1000).
      אפשר אחוזון **מדויק** בלי ערימות?

        ??? fu-answer "תשובה"
            מערך ספירה `cnt[0..R]` : הכנסה \( O(1) \), ושאילתה סריקה של הספירות המצטברות עד
            \( \lceil p n \rceil \), ‏\( O(R) \). עם עץ Fenwick על אותן ספירות, הכנסה ושאילתה
            (חיפוש בינארי על הסכומים החלקיים) ב-\( O(\log R) \). מחיקה (החלון של סעיף ג) היא
            הורדה של 1, בחינם. כש-\( R \) קטן זה עדיף על הערימות גם בחומרה.

    - **כמה אחוזונים בבת אחת :** p50, p90 ו-p99 מאותו זרם.

        ??? fu-answer "תשובה"
            שלושה `StreamQuantile`, כל אחד שומר עותק של הכול, \( 3n \) זיכרון. או מבנה אחד :
            ארבע ערימות ברצף (הגבולות ב-50, 90 ו-99 אחוז) עם מעבר של ערך לאורך השרשרת, או עץ
            סדר-סטטיסטי (עץ מאוזן שכל צומת בו יודע את גודל תת-העץ שלו), שעונה על "הערך במקום
            \( r \)" לכל \( r \) ב-\( O(\log n) \). במערך ספירה (השאלה הקודמת) שלושתם הם שלוש
            סריקות.

    - **הממוצע והשונות בזרם :** למה הם קלים והחציון לא?

        ??? fu-answer "תשובה"
            הממוצע הוא מונה וסכום, שני מספרים, והשונות עם האלגוריתם של Welford עוד מספר אחד :
            \( \delta = x - \bar{x} \), ‏\( \bar{x} \mathrel{+}= \delta / n \), ‏\( M_2 \mathrel{+}= \delta (x - \bar{x}) \),
            והשונות \( M_2 / (n - 1) \), יציב נומרית. אלה **סטטיסטיקות ספיקות** : הערך הבא
            מעדכן אותן בלי הנתונים הישנים. החציון תלוי בכל ערך בנפרד (הוספת ערך גדול מזיזה
            אותו למקום הבא, ומי זה תלוי במה שיש), ולכן אין לו סיכום בגודל קבוע, רק קירובים.
