---
id: 106
title: המספר שמופיע פעם אחת – כשכל השאר מופיעים שלוש פעמים
level: junior
difficulty: medium
kind: code
tags: [algorithms, bitwise, python, systemverilog]
source: "LeetCode 136 ו-137 (Single Number, Single Number II) כסולם : סעיף א הוא 136, סעיף ב הוא 137, וסעיף ג מכליל"
added: 2026-11-13
---

## השאלה

נתון מערך של מספרים שלמים של 32 ביט, עם סימן. כל מספר מופיע בו **שלוש פעמים**, חוץ ממספר אחד
שמופיע **פעם אחת**. מצאו אותו בזמן \( O(n) \) ובזיכרון \( O(1) \) : בלי מילון, בלי מיון ובלי מערך
עזר שגדל עם הקלט.

**ההקשר באימות :** מסלול עם יתירות משולשת (triple redundancy) : כל טרנזקציה אמורה להגיע לבודק
שלוש פעמים, פעם מכל עותק של המסלול. טרנזקציה אחת הגיעה רק פעם אחת. הבודק רואה זרם ארוך של
טרנזקציות, אין לו זיכרון לשמור את כולן, ויש לו רק כמה רגיסטרים. איזו טרנזקציה זו?

**הדוגמאות :** ב-<span dir="ltr">[2, 2, 3, 2]</span> התשובה 3, וב-<span dir="ltr">[0, 1, 0, 1, 0, 1, 99]</span>
התשובה 99.

- **סעיף א – כל השאר פעמיים :** החימום. כל מספר מופיע פעמיים, חוץ מאחד. איך מוצאים אותו בלי
  זיכרון, ולמה זה עובד?
- **סעיף ב – כל השאר שלוש פעמים :** השאלה עצמה. למה הפתרון של סעיף א לא עובד, ומה עובד במקומו?
- **סעיף ג – הכללה :** כל השאר מופיעים \( k \) פעמים, והמיוחד \( p \) פעמים, כש-\( p \) לא
  מתחלק ב-\( k \). ומה אם המיוחד מופיע פעמיים, והשאר שלוש פעמים?

??? interviewer "מה המראיין בודק"
    - **למה XOR עובד :** האם המועמד מבין מה ה-XOR עושה בכל ביט, ולא רק זוכר את הטריק.
    - **פירוק לביטים :** האם הוא רואה שכל ביט הוא בעיה נפרדת, ושמותר לספור בכל ביט לבד.
    - **מכונת מצבים :** האם הוא יודע לגזור את הקוד מטבלת מצבים, ולהסביר כל פעולה בו.
    - **מקרי קצה :** מספרים שליליים, ובפייתון מספרים שאין להם רוחב קבוע.
    - **הכללה :** האם הוא מגיע לכל \( k \), ויודע כמה רגיסטרים זה עולה.

---

### סעיף א – כל השאר פעמיים

??? tip "רמז 1"
    מה יוצא כשעושים XOR למספר עם עצמו? ומה כשעושים XOR עם 0?

??? tip "רמז 2"
    הסתכלו על ביט אחד בכל המספרים, עמודה אחת של אפסים ואחדים. מה ה-XOR של העמודה אומר על מספר
    האחדים בה?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ה-XOR של כל המספרים. כל זוג מתבטל, כי \( a \oplus a = 0 \), הסדר לא משנה, ומה שנשאר הוא
        המספר הבודד. ב-<span dir="ltr">[4, 1, 2, 1, 2]</span> התשובה 4.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **‏XOR הוא חיבור מודולו 2 בכל ביט.** בכל ביט, ה-XOR של כל המספרים הוא 1 בדיוק כשמספר האחדים
    בעמודה של הביט הזה אי-זוגי. מספר שמופיע פעמיים מוסיף לכל עמודה 0 או 2 אחדים, מספר זוגי. לכן
    הזוגיות של כל עמודה היא הביט של המספר הבודד, וה-XOR של הכול הוא המספר עצמו. על הדוגמה, בשלושה
    ביטים :

    <!-- gen 0 -->

    | הצעד | המספר | בבינארי | ה-XOR עד עכשיו | בעשרוני |
    |:-:|:-:|:-:|:-:|:-:|
    | 1 | 4 | ‏`100` | ‏`100` | 4 |
    | 2 | 1 | ‏`001` | ‏`101` | 5 |
    | 3 | 2 | ‏`010` | ‏`111` | 7 |
    | 4 | 1 | ‏`001` | ‏`110` | 6 |
    | 5 | 2 | ‏`010` | ‏`100` | 4 |

    <!-- /gen -->

    אחרי 4 ו-1 הרגיסטר מחזיק את שניהם, ואחרי ה-1 השני רק את 4 ו-2. כל ערך נכנס ויוצא, וה-XOR
    זוכר רק את מי שנכנס מספר אי-זוגי של פעמים.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מתחילים :** רגיסטר אחד, 0.
    2. **כל מספר :** עושים לו XOR לתוך הרגיסטר.
    3. **הסוף :** הרגיסטר הוא המספר הבודד.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="single_twice"
        def single_twice(nums: list[int]) -> int:
            """Every number appears twice but one, which appears once: the XOR of all of them."""
            acc = 0
            for x in nums:
                acc ^= x                               # (1)!
            return acc
        ```

        1. גם מספר שלילי עובד כמו שהוא : XOR פועל על כל ביט לבד, גם על הביטים של הסימן.

    === "SystemVerilog"
        ```systemverilog title="function single_twice"
        // every number appears twice but one, which appears once: the XOR of all of them
        function automatic int single_twice(int nums[]);
          int acc = 0;
          foreach (nums[i]) acc ^= nums[i];
          return acc;
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    ‏XOR חילופי וקיבוצי, \( x \oplus x = 0 \) ו-\( x \oplus 0 = x \). לכן אפשר לסדר מחדש את כל
    המספרים כך שכל זוג שווה יעמוד יחד, כל זוג נותן 0, ונשאר המספר שאין לו זוג. אותו טריק מוצא
    tag שלא חזר בבודד של [שאלה 0058](../senior/0058-missing-tags.md), כשכל tag נכנס פעם בשליחה
    ופעם בחזרה.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n) \), פעולה אחת לכל מספר.
    - **זיכרון :** ‏\( O(1) \) : רגיסטר אחד.

---

### סעיף ב – כל השאר שלוש פעמים

??? tip "רמז 1"
    נסו את ה-XOR של סעיף א על <span dir="ltr">[2, 2, 3, 2]</span>. מה יוצא, ולמה?

??? tip "רמז 2"
    בסעיף א כל ביט היה מונה מודולו 2. איזה מונה צריך עכשיו בכל ביט, כמה ביטים של זיכרון הוא צריך,
    ואיך מעדכנים את כל המונים יחד?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        בכל ביט סופרים את האחדים **מודולו 3**, ומה שנשאר הוא הביט של המספר הבודד. ספירה ישירה של
        32 עמודות עולה \( O(32n) \). קצר יותר : מונה מודולו 3 לכל ביט, ששני הביטים שלו שמורים
        בשני רגיסטרים, `ones` ו-`twos`, לכל 32 הביטים יחד. לכל מספר \( x \) מעדכנים קודם
        <span dir="ltr">`ones = (ones ^ x) & ~twos`</span> ואחר כך
        <span dir="ltr">`twos = (twos ^ x) & ~ones`</span>, ובסוף `ones` הוא המספר. ב-<span dir="ltr">[2, 2, 3, 2]</span> :
        3.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **למה XOR לא מספיק.** ‏XOR סופר מודולו 2. מספר שמופיע שלוש פעמים מוסיף לכל עמודה 0 או 3
    אחדים, ו-3 אי-זוגי, ולכן הוא לא מתבטל. ב-<span dir="ltr">[2, 2, 3, 2]</span> ה-XOR הוא 1, ה-XOR
    של 2 ו-3 : כל ערך נשאר פעם אחת.

    **סופרים מודולו 3.** בכל ביט, מספר האחדים בעמודה הוא 3 כפול מספר הערכים המשולשים שיש להם 1
    בביט הזה, ועוד הביט של המספר הבודד. מודולו 3 נשאר רק הביט של הבודד. הפתרון הישיר עובר על
    המערך 32 פעמים, פעם לכל ביט, וסופר. זה \( O(32n) \), עדיין לינארי, בזיכרון קבוע.

    **מונה מודולו 3 בכל ביט.** במקום 32 מעברים, נחזיק לכל ביט את הספירה שלו מודולו 3 תוך כדי
    מעבר אחד : 0, 1 או 2, שני ביטים של זיכרון. את הביט הנמוך של כל 32 המונים נשים ברגיסטר אחד,
    `ones`, ואת הביט הגבוה ב-`twos`. ביט במצב 00 (‏twos ואז ones) סופר 0, במצב 01 סופר 1, ובמצב
    10 סופר 2. ביט 1 במספר שנכנס מקדם את המונה, וביט 0 משאיר אותו :

    <!-- gen 1 -->

    <svg class="figure m3-fsm" viewBox="0 0 380 252" style="max-width:23.75rem" direction="ltr" role="img" aria-label="המונה של ביט אחד : שלושה מצבים, 00, 01 ו-10, לספירה 0, 1 ו-2 מודולו 3. ביט 1 במספר שנכנס מעביר למצב הבא, 10 חוזר ל-00, וביט 0 משאיר במקום. למצב 11 לא מגיעים"><g class="m3-arc"><title>a 1: 0 → 1</title><path d="M94.3,145.9 Q118.5,104.9 154.1,92.5" fill="none"/><path class="m3-head" d="M162.6,89.5 L155.8,97.2 L152.5,87.8 Z"/><text class="m3-lab" x="118.5" y="109.9" text-anchor="middle">1</text></g><g class="m3-arc"><title>a 1: 1 → 2</title><path d="M216.4,89.2 Q261.5,104.9 280.6,137.3" fill="none"/><path class="m3-head" d="M285.2,145.0 L276.3,139.8 L285.0,134.8 Z"/><text class="m3-lab" x="261.5" y="109.9" text-anchor="middle">1</text></g><g class="m3-arc"><title>a 1: 2 → 0</title><path d="M280.2,189.8 Q190.0,280.0 106.9,196.9" fill="none"/><path class="m3-head" d="M100.5,190.5 L110.4,193.3 L103.3,200.4 Z"/><text class="m3-lab" x="190.0" y="243.0" text-anchor="middle">1</text></g><g class="m3-loop"><title>a 0: stays at 0</title><path d="M55.4,183.4 C28.8,217.7 28.8,122.3 49.1,148.9" fill="none"/><path class="m3-head" d="M54.6,156.1 L45.1,152.0 L53.1,145.9 Z"/><text class="m3-lab" x="11.4" y="175.0" text-anchor="middle">0</text></g><g class="m3-loop"><title>a 0: stays at 1</title><path d="M176.6,55.4 C142.3,28.8 237.7,28.8 211.1,49.1" fill="none"/><path class="m3-head" d="M203.9,54.6 L208.0,45.1 L214.1,53.1 Z"/><text class="m3-lab" x="190.0" y="16.4" text-anchor="middle">0</text></g><g class="m3-loop"><title>a 0: stays at 2</title><path d="M324.6,156.6 C351.2,122.3 351.2,217.7 330.9,191.1" fill="none"/><path class="m3-head" d="M325.4,183.9 L334.9,188.0 L326.9,194.1 Z"/><text class="m3-lab" x="368.6" y="175.0" text-anchor="middle">0</text></g><g class="m3-node m3-n0"><title>twos 0, ones 0: count 0 mod 3</title><circle cx="80" cy="170" r="28"/><text class="m3-code" x="80" y="171" text-anchor="middle">00</text><text class="m3-cnt" x="80" y="187" text-anchor="middle">≡0</text></g><g class="m3-node m3-n1"><title>twos 0, ones 1: count 1 mod 3</title><circle cx="190" cy="80" r="28"/><text class="m3-code" x="190" y="81" text-anchor="middle">01</text><text class="m3-cnt" x="190" y="97" text-anchor="middle">≡1</text></g><g class="m3-node m3-n2"><title>twos 1, ones 0: count 2 mod 3</title><circle cx="300" cy="170" r="28"/><text class="m3-code" x="300" y="171" text-anchor="middle">10</text><text class="m3-cnt" x="300" y="187" text-anchor="middle">≡2</text></g><g class="m3-node m3-n3"><title>twos 1, ones 1: never reached</title><circle cx="190" cy="152" r="20"/><text class="m3-code" x="190" y="157" text-anchor="middle">11</text></g></svg>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="m3-key-n0"></i>המצב 00 : הספירה של הביט היא 0, מודולו 3</span><span><i class="m3-key-n1"></i>המצב 01 : ‏1 ב-ones, הספירה 1</span><span><i class="m3-key-n2"></i>המצב 10 : ‏1 ב-twos, הספירה 2</span><span><i class="m3-key-one"></i>ביט 1 במספר שנכנס : למצב הבא</span><span><i class="m3-key-zero"></i>ביט 0 : נשארים</span><span><i class="m3-key-n3"></i>המצב 11 : לא מגיעים אליו</span></span>

    <!-- /gen -->

    **גוזרים את שתי השורות.** כל 32 המונים צריכים לזוז יחד, בפעולות על מילה שלמה. נתחיל ממה שעשינו
    בסעיף א, להפוך כל רגיסטר לפי \( x \), ונבדוק איפה זה טועה. בטבלה כל מצב וכל ביט של \( x \),
    המצב הבא, וליד כל רגיסטר ה-XOR שלו עם \( x \) מול הערך שהוא צריך לקבל :

    <!-- gen 3 -->

    | המצב twos ones | ‏x | המצב הבא | ‏`ones ^ x` | הערך החדש של ones | ‏`twos ^ x` | הערך החדש של twos |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | 00 | 0 | 00 | 0 | 0 | 0 | 0 |
    | 00 | 1 | 01 | 1 | 1 | **1** | 0 |
    | 01 | 0 | 01 | 1 | 1 | 0 | 0 |
    | 01 | 1 | 10 | 0 | 0 | 1 | 1 |
    | 10 | 0 | 10 | 0 | 0 | 1 | 1 |
    | 10 | 1 | 00 | **1** | 0 | 0 | 0 |

    <!-- /gen -->

    ב-ones ה-XOR טועה רק בשורה האחרונה (מודגש) : מ-10 עם 1 חוזרים ל-00, ו-ones צריך להישאר 0.
    זו השורה היחידה עם `twos = 1` שבה ה-XOR נותן 1, כי במצב 10 ‏ones אף פעם לא נדלק. לכן מסכים
    אותו ב-`~twos`, וזו השורה הראשונה : <span dir="ltr">`ones = (ones ^ x) & ~twos`</span>.

    ב-twos ה-XOR טועה רק בשורה השנייה : מ-00 עם 1 עוברים ל-01, ו-twos צריך להישאר 0. בשורה הזו
    ones **החדש** הוא 1, ובכל שורה שבה twos החדש צריך להיות 1 (01 עם 1, ו-10 עם 0) ones החדש הוא
    0. לכן מסכים ב-`~ones` אחרי שהוא כבר עודכן, וזו השורה השנייה :
    <span dir="ltr">`twos = (twos ^ x) & ~ones`</span>. עם ones הישן זה לא עובד : ב-01 עם 1 ‏ones
    הישן הוא 1, והמסכה הייתה מוחקת את ה-1 ש-twos צריך לקבל.

    על הדוגמה, בארבעה ביטים. בכל שורה המספר שנכנס, שני הרגיסטרים אחריו, והספירה של כל ביט :

    <!-- gen 4 -->

    <div class="m3-tracewrap" tabindex="0" role="region" aria-label="ones ו-twos אחרי כל מספר של הדוגמה"><table class="m3-trace"><thead><tr><th>הצעד</th><th>המספר x</th><th>ones</th><th>twos</th><th>הספירה של כל ביט, מודולו 3</th></tr></thead><tbody><tr><td>0</td><td>–</td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span></span></td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span></span></td><td><span class="m3-w" dir="ltr"><span class="m3-b m3-st0">0</span><span class="m3-b m3-st0">0</span><span class="m3-b m3-st0">0</span><span class="m3-b m3-st0">0</span></span></td></tr><tr><td>1</td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-x">1</span><span class="m3-b">0</span></span> <span class="m3-v">2</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-one">1</span><span class="m3-b">0</span></span> <span class="m3-v">2</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span></span> <span class="m3-v">0</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b m3-st0">0</span><span class="m3-b m3-st0">0</span><span class="m3-b m3-st1">1</span><span class="m3-b m3-st0">0</span></span></td></tr><tr><td>2</td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-x">1</span><span class="m3-b">0</span></span> <span class="m3-v">2</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span></span> <span class="m3-v">0</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-two">1</span><span class="m3-b">0</span></span> <span class="m3-v">2</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b m3-st0">0</span><span class="m3-b m3-st0">0</span><span class="m3-b m3-st2">2</span><span class="m3-b m3-st0">0</span></span></td></tr><tr><td>3</td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-x">1</span><span class="m3-b m3-x">1</span></span> <span class="m3-v">3</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-one">1</span></span> <span class="m3-v">1</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span></span> <span class="m3-v">0</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b m3-st0">0</span><span class="m3-b m3-st0">0</span><span class="m3-b m3-st0">0</span><span class="m3-b m3-st1">1</span></span></td></tr><tr><td>4</td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-x">1</span><span class="m3-b">0</span></span> <span class="m3-v">2</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-one">1</span><span class="m3-b m3-one">1</span></span> <span class="m3-v">3</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span></span> <span class="m3-v">0</span></td><td><span class="m3-w" dir="ltr"><span class="m3-b m3-st0">0</span><span class="m3-b m3-st0">0</span><span class="m3-b m3-st1">1</span><span class="m3-b m3-st1">1</span></span></td></tr></tbody></table></div>

    <!-- /gen -->

    <!-- gen 5 -->

    <span class="viz-legend"><span><i class="m3-key-x"></i>ביט 1 במספר שנכנס</span><span><i class="m3-key-n1"></i>ביט 1 ב-ones : הספירה שלו 1</span><span><i class="m3-key-n2"></i>ביט 1 ב-twos : הספירה שלו 2</span></span>

    <!-- /gen -->

    ביט 1 סופר 1, 2, 0 ושוב 1 : שלושת ה-2 מתבטלים, וה-3 משאיר בו 1. ביט 0 נדלק רק ב-3. בסוף
    `twos = 0` ו-`ones` הוא <span dir="ltr">0011 = 3</span>.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מתחילים :** שני רגיסטרים, `ones` ו-`twos`, שניהם 0 : כל ביט במצב 00.
    2. **מעדכנים את ones :** ‏<span dir="ltr">`ones = (ones ^ x) & ~twos`</span>.
    3. **מעדכנים את twos :** עם ones החדש, <span dir="ltr">`twos = (twos ^ x) & ~ones`</span>.
    4. **הסוף :** ביט שהספירה שלו 1 נמצא ב-ones, ולכן `ones` הוא המספר הבודד.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="single_thrice" linenums="1" hl_lines="7 10 17 18"
        def single_thrice_count(nums: list[int]) -> int:
            """Every number three times but one: the ones of every bit counted modulo 3 (32-bit numbers)."""
            res = 0
            for b in range(32):
                cnt = 0
                for x in nums:
                    cnt += (x >> b) & 1                # (1)!
                if cnt % 3:
                    res |= 1 << b
            return res - (1 << 32) if res >> 31 else res   # (2)!


        def single_thrice(nums: list[int]) -> int:
            """Every number three times but one: a counter modulo 3 in every bit, in two words."""
            ones, twos = 0, 0
            for x in nums:
                ones = (ones ^ x) & ~twos              # (3)!
                twos = (twos ^ x) & ~ones              # (4)!
            return ones
        ```

        1. במספר שלילי, ‏`>>` בפייתון ממלא באחדים מלמעלה, ולכן ביט 31 הוא ביט הסימן של המספר
           ב-32 ביט.
        2. ‏`res` נבנה מ-32 ביטים כמספר בלי סימן. כשביט 31 דלוק, התשובה שלילית (ראו המלכודת).
        3. מתהפך לפי \( x \), חוץ מביטים במצב 10, שם ones נשאר 0.
        4. עם ones **החדש**. הסדר של שתי השורות הוא חלק מהפתרון (ראו המלכודת).

    === "SystemVerilog"
        ```systemverilog title="function single_thrice" linenums="1" hl_lines="6 16 17"
        // every number three times but one: the ones of every bit counted modulo 3
        function automatic int single_thrice_count(int nums[]);
          int res = 0, cnt;
          for (int b = 0; b < 32; b++) begin
            cnt = 0;
            foreach (nums[i]) cnt += nums[i][b];
            if (cnt % 3 != 0) res[b] = 1'b1;
          end
          return res;                                       // (1)!
        endfunction

        // every number three times but one: a counter modulo 3 in every bit, in two words
        function automatic int single_thrice(int nums[]);
          int ones = 0, twos = 0;
          foreach (nums[i]) begin
            ones = (ones ^ nums[i]) & ~twos;
            twos = (twos ^ nums[i]) & ~ones;
          end
          return ones;
        endfunction
        ```

        1. ‏`int` הוא 32 ביט עם סימן, ולכן ביט 31 דלוק נותן מספר שלילי בלי שום המרה.

    #### למה זה נכון { .sol-proof }

    **הספירה :** בכל ביט \( b \), מספר האחדים הוא \( 3m_b + s_b \), כש-\( m_b \) מספר הערכים
    המשולשים עם 1 בביט \( b \) ו-\( s_b \) הביט של הבודד. מודולו 3 זה \( s_b \).

    **המונה :** באינדוקציה על המספרים, אחרי כל מספר המצב של כל ביט, ‏twos ואז ones, הוא הספירה שלו
    מודולו 3 בקידוד 00, 01, 10. בהתחלה כולם 00, והטבלה מראה ששתי השורות נותנות את המצב הבא בכל
    שש השורות. כל ביט של המילה הוא מונה נפרד, כי `^`, `&` ו-`~` לא מערבבים ביטים. בסוף כל ביט
    במצב 00 או 01 לפי \( s_b \), ולכן `twos = 0` ו-`ones` הוא הבודד.

    **מספרים שליליים :** ב-SystemVerilog ‏`int` הוא 32 ביט במשלים ל-2, ואין מה לעשות. בפייתון
    למספר אין רוחב : ‏<span dir="ltr">−4</span> הוא <span dir="ltr">…11100</span>, עם אחדים בלי סוף
    משמאל, ו-`^`, `&` ו-`~` פועלים על הייצוג הזה ביט אחרי ביט. כל ביט מעל 31 רואה את ביט הסימן של
    כל מספר, ולכן כל הביטים האלה סופרים בדיוק את אותו דבר, ומסיימים במצב של ביט הסימן של הבודד.
    ‏`single_thrice` מחזירה מספר שלילי נכון בלי שום מסכה : ב-<span dir="ltr">[−2, −2, 1, 1, −3, 1, −3, −3, −4, −2]</span>
    היא מחזירה <span dir="ltr">−4</span>. רק `single_thrice_count`, שעוברת על 32 ביטים ובונה מהם
    מספר, צריכה להפוך את ביט 31 לסימן.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n) \) : ארבע פעולות על מילה לכל מספר. הספירה הישירה \( O(32n) \).
    - **זיכרון :** ‏\( O(1) \) : שני רגיסטרים, ובספירה הישירה מונה אחד.

    **נסו בעצמכם.** התיבה נפתחת על <span dir="ltr">[2, 2, 3, 2]</span>, עם ביט 1 בתרשים. לחצו
    "הצעד הבא" ארבע פעמים : ביט 1 עובר 01, 10, 00 ושוב 01, ובסוף <span dir="ltr">ones = 3</span>.
    בחרו "עם שליליים" ו"עד הסוף" : כל שמונת הביטים מסכימים עם הספירה, ו-<span dir="ltr">ones = −4</span>.
    לבסוף בחרו בשדה הסדר "twos ואז ones" : הספירה של כל ביט נכונה, אבל ביט שסופר 1 יושב ב-twos,
    המצב שלו אדום, ו-ones יוצא 0. בתיבה אפשר לכתוב כל מערך של עד 16 מספרים, ולראות את כל הביטים
    יחד מול הספירה האמיתית שלהם :

    <div class="explorer" data-kind="thrice" data-nums="2.2.3.2" data-order="good"></div>

---

### סעיף ג – הכללה

??? tip "רמז 1"
    אם המיוחד מופיע \( p \) פעמים, מה הספירה של ביט שלו מודולו \( k \)? מתי היא 0?

??? tip "רמז 2"
    בסעיף ב המונה של כל ביט היה שני ביטים, ברגיסטר לכל ביט של המונה. כמה רגיסטרים צריך למונה
    מודולו \( k \), ואיך מוסיפים 1 לכל המונים יחד?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        בכל ביט סופרים מודולו \( k \). הספירה היא \( p \bmod k \) בביטים של המיוחד ו-0 בכל השאר,
        ולכן כש-\( p \) לא מתחלק ב-\( k \) הביטים שהספירה שלהם לא 0 הם המיוחד. המונים נשמרים
        ב-\( \lceil \log_2 k \rceil \) רגיסטרים, רגיסטר לכל ביט של המונה, והתשובה היא ה-OR שלהם.
        כש-\( k = 3 \) ו-\( p = 2 \) המיוחד מסיים ב-twos ו-`ones = 0`, ולכן מחזירים
        <span dir="ltr">`ones | twos`</span> : ב-<span dir="ltr">[5, 5, 7, 7, 7]</span> ‏twos הוא 5.

    <!-- cost: זמן \( O(n \log k) \) | זיכרון \( O(\log k) \) -->

    #### הרעיון { .sol-idea }

    **מה הספירה מגלה.** בכל ביט, הספירה היא \( k \) כפול משהו, ועוד \( p \) אם למיוחד יש 1
    בביט הזה. מודולו \( k \) נשאר \( p \bmod k \), או 0. כש-\( p \) לא מתחלק ב-\( k \), ‏\( p \bmod k \ne 0 \),
    והביטים שהספירה שלהם לא 0 הם בדיוק הביטים של המיוחד. כש-\( p \) כן מתחלק ב-\( k \), המיוחד
    מתבטל כמו כל השאר, ואין דרך לגלות אותו כך.

    **פעמיים בין שלשות.** עם \( k = 3 \) ו-\( p = 2 \) כל ביט של המיוחד מסיים בספירה 2, כלומר
    ב-twos : ‏ones מסיים 0, ו-twos הוא המספר. <span dir="ltr">`ones | twos`</span> מכסה את שני
    המקרים, \( p = 1 \) ו-\( p = 2 \), בלי לדעת מראש מה \( p \). בבודק של המסלול המשולש זה
    המקרה שבו עותק אחד מתוך שלושה אבד, והטרנזקציה הגיעה פעמיים.

    **מונה בחתכים (bit-sliced).** למונה מודולו \( k \) צריך \( m = \lceil \log_2 k \rceil \)
    ביטים. נחזיק \( m \) רגיסטרים : ‏`c[j]` הוא ביט \( j \) של המונים של כל הביטים. הוספת \( x \)
    לכל המונים היא מחבר עם שארית שעוברת מביט לביט (ripple carry), כשהשארית הראשונה היא \( x \)
    עצמו : ביט \( j \) מקבל XOR עם השארית, והשארית הבאה היא ה-AND שלהם. אחר כך מאפסים את המונים
    שהגיעו ל-\( k \) : מסכה של הביטים שבהם כל `c[j]` שווה לביט \( j \) של \( k \). עם \( k = 2 \)
    זה רגיסטר אחד וה-XOR של סעיף א. עם \( k = 3 \) זה שני רגיסטרים, באותו קידוד של ones ו-twos
    בדיוק, רק בפעולות אחרות. עם \( k = 4 \) המונה חוזר מ-3 ל-0 בעצמו, והאיפוס לא משנה דבר.

    **דוגמה עם \( k = 5 \).** ב-<span dir="ltr">[7, −1, 6, 7, −1, 7, 6, −1, 7, −1, 7, −1]</span>
    ‏7 ו-<span dir="ltr">−1</span> מופיעים חמש פעמים, ו-6 פעמיים, ולכן צריך שלושה רגיסטרים. בביט 0
    יש אחד מכל 7 ומכל <span dir="ltr">−1</span>, עשרה אחדים. בביטים 1 ו-2 יש גם את שני ה-6, שנים
    עשר. מביט 3 ומעלה רק ה-<span dir="ltr">−1</span>, חמישה. מודולו 5 נשארים ביטים 1 ו-2 עם 2, ‏\( p \) :

    <!-- gen 6 -->

    <div class="m3-tracewrap" tabindex="0" role="region" aria-label="המונים של הדוגמה עם k = 5, ביט לכל עמודה"><table class="m3-lanes"><tbody><tr><th>הספירה מודולו 5</th><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-nz">2</span><span class="m3-b m3-nz">2</span><span class="m3-b">0</span></span></td><td></td></tr><tr><th>‏c[2]</th><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span></span></td><td class="m3-v">0</td></tr><tr><th>‏c[1]</th><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-one">1</span><span class="m3-b m3-one">1</span><span class="m3-b">0</span></span></td><td class="m3-v">6</td></tr><tr><th>‏c[0]</th><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span></span></td><td class="m3-v">0</td></tr><tr class="m3-or"><th>ה-OR של המילים</th><td><span class="m3-w" dir="ltr"><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b">0</span><span class="m3-b m3-x">1</span><span class="m3-b m3-x">1</span><span class="m3-b">0</span></span></td><td class="m3-v">6</td></tr></tbody></table></div>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **כמה רגיסטרים :** ‏\( m = \lceil \log_2 k \rceil \), כולם 0.
    2. **מוסיפים את \( x \) :** השארית מתחילה ב-\( x \). לכל \( j \), ‏`c[j]` מקבל XOR עם השארית,
       והשארית הבאה היא ה-AND שלהם.
    3. **מאפסים את מי שהגיע ל-\( k \) :** המסכה היא ה-AND על כל \( j \) של `c[j]` כשביט \( j \)
       של \( k \) הוא 1, ושל `~c[j]` כשהוא 0. כל רגיסטר מקבל AND עם ההיפוך של המסכה.
    4. **התשובה :** ה-OR של כל הרגיסטרים.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="single_mod_k" linenums="1" hl_lines="7 18 21 26"
        def single_thrice_any(nums: list[int]) -> int:
            """Every number three times but one, which appears once or twice."""
            ones, twos = 0, 0
            for x in nums:
                ones = (ones ^ x) & ~twos
                twos = (twos ^ x) & ~ones
            return ones | twos                         # (1)!


        def single_mod_k(nums: list[int], k: int) -> int:
            """Every number k times but one, which appears p times, p not a multiple of k (k >= 2):
            a counter modulo k in every bit, its bits in ceil(log2 k) words."""
            m = (k - 1).bit_length()                   # (2)!
            c = [0] * m                                # c[j]: bit j of every bit's counter
            for x in nums:
                carry = x
                for j in range(m):
                    c[j], carry = c[j] ^ carry, c[j] & carry
                full = ~0
                for j in range(m):                     # (3)!
                    full &= c[j] if (k >> j) & 1 else ~c[j]
                for j in range(m):
                    c[j] &= ~full
            res = 0
            for w in c:
                res |= w                               # (4)!
            return res
        ```

        1. ‏\( p = 1 \) משאיר את המיוחד ב-ones, ו-\( p = 2 \) ב-twos. הרגיסטר השני תמיד 0.
        2. ‏\( \lceil \log_2 k \rceil \) : ‏3 ל-\( k = 5 \), ‏2 ל-\( k = 3 \) ול-\( k = 4 \), ‏1 ל-\( k = 2 \).
        3. ‏`full` הוא 1 בביטים שהמונה שלהם הגיע ל-\( k \). המונה לא עובר את \( k \) : לפני
           ההוספה הוא לכל היותר \( k - 1 \).
        4. ביט שהמונה שלו לא 0 הוא ביט של המיוחד, ולא חשוב איזה ביט של המונה דלוק.

    === "SystemVerilog"
        ```systemverilog title="function single_mod_k" linenums="1" hl_lines="8 22 26 29"
        // every number three times but one, which appears once or twice
        function automatic int single_thrice_any(int nums[]);
          int ones = 0, twos = 0;
          foreach (nums[i]) begin
            ones = (ones ^ nums[i]) & ~twos;
            twos = (twos ^ nums[i]) & ~ones;
          end
          return ones | twos;
        endfunction

        // every number k times but one, which appears p times, p not a multiple of k (k >= 2):
        // a counter modulo k in every bit, its bits in $clog2(k) words
        function automatic int single_mod_k(int nums[], int k);
          int m, carry, nxt, full, res = 0;
          int c[];
          m = $clog2(k);
          c = new[m];                                       // (1)!
          foreach (nums[i]) begin
            carry = nums[i];
            for (int j = 0; j < m; j++) begin
              nxt = c[j] & carry;
              c[j] ^= carry;
              carry = nxt;
            end
            full = -1;
            for (int j = 0; j < m; j++) full &= k[j] ? c[j] : ~c[j];
            for (int j = 0; j < m; j++) c[j] &= ~full;
          end
          foreach (c[j]) res |= c[j];
          return res;
        endfunction
        ```

        1. ‏`new[m]` מאתחל את כל הרגיסטרים ל-0.

    #### למה זה נכון { .sol-proof }

    **המונים :** באינדוקציה, אחרי כל מספר כל ביט מחזיק את הספירה שלו מודולו \( k \) בבינארי,
    בביטים \( j \) של `c[j]`. לפני ההוספה המונה לכל היותר \( k - 1 \), ההוספה נותנת לכל היותר
    \( k \le 2^m \), והאיפוס מחזיר \( k \) ל-0. כש-\( k = 2^m \) הערך \( k \) לא נכנס ב-\( m \) ביטים,
    והמונה חוזר ל-0 בעצמו. המסכה אז מסמנת מונים שהם 0, ואיפוס של 0 לא משנה אותם.

    **התשובה :** ביט שהספירה שלו לא 0 מודולו \( k \) הוא ביט של המיוחד, כפי שראינו, וה-OR של
    הרגיסטרים הוא 1 בדיוק בביטים האלה. מספרים שליליים בפייתון עובדים מאותה סיבה כמו בסעיף ב : כל
    הביטים מעל 31 סופרים את אותו דבר.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n \log k) \) : לכל מספר כ-\( 3m \) פעולות על מילה.
    - **זיכרון :** ‏\( O(\log k) \) : ‏\( m \) רגיסטרים, שלושה ל-\( k = 5 \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : XOR לבד"
    ה-XOR של סעיף א סופר מודולו 2, ומספר שמופיע שלוש פעמים לא מתבטל. מה שיוצא הוא ה-XOR של כל
    הערכים **השונים**, כל אחד פעם אחת : ב-<span dir="ltr">[2, 2, 3, 2]</span> יוצא 1, ה-XOR של 2
    ו-3, וב-<span dir="ltr">[0, 1, 0, 1, 0, 1, 99]</span> יוצא 98, ה-XOR של 0, 1 ו-99. רק כשכל
    הערכים המשולשים מתבטלים ביניהם במקרה, ה-XOR נותן את התשובה, ואז זה מזל.

??? trap "מלכודת : הסדר של שתי השורות"
    השורה של twos משתמשת ב-ones **החדש**. אם מחליפים את הסדר, ‏twos קודם, המונה רץ אחורה :
    00, 10, 01, 00. כל ביט עדיין סופר מודולו 3, אבל ביט שסופר 1 נמצא ב-twos, ו-ones יוצא 0 :
    ב-<span dir="ltr">[2, 2, 3, 2]</span> ‏`ones = 0` ו-`twos = 3`. אם מחשבים את שתיהן מהערכים
    הישנים, יחד, אחרי המספר הראשון <span dir="ltr">ones = twos = 2</span> : ביט 1 במצב 11, שאין לו
    משמעות, ובסוף שניהם 0.

??? trap "מלכודת : הסימן בפייתון"
    ‏`single_thrice_count` בונה את התשובה מ-32 ביטים, ובלי השורה האחרונה היא מחזירה מספר בלי סימן :
    בדוגמה עם השליליים <span dir="ltr">4294967292 = −4 + 2^32</span> ולא <span dir="ltr">−4</span>.
    אותו דבר קורה למי ש"מתקן" את `single_thrice` עם <span dir="ltr">`& 0xFFFFFFFF`</span> : בפייתון
    שתי השורות עובדות על מספרים שליליים כמו שהן, והמסכה רק מקלקלת.

??? trap "מלכודת : מילון"
    ספירה של כל ערך במילון (`Counter`) מוצאת את התשובה במעבר אחד, אבל המילון מחזיק את כל הערכים
    השונים, כשליש מהמערך : זיכרון \( O(n) \), לא \( O(1) \). בבודד של המסלול המשולש זה טבלה בגודל
    של כל הטרנזקציות שעוברות.

??? trap "מלכודת : מיון"
    אחרי מיון כל ערך יושב בשלשה, ומספיק לבדוק כל שלשה. אבל המיון הוא \( O(n \log n) \), לא
    \( O(n) \), והוא משנה את המערך או מעתיק אותו, ואז הזיכרון \( O(n) \).

??? followup "שאלות המשך"
    - **בחומרה :** בודק שמקבל מילה של 32 ביט בכל שעון. איך נראה המימוש של `single_thrice`, וכמה
      הוא עולה?

        ??? fu-answer "תשובה"
            מונה מודולו 3 של שני ביטים לכל ביט של המילה : 64 flip-flops, ‏ones ו-twos. בכל ביט שני
            XOR ושני AND עם היפוך, מילה אחת בכל שעון. אפשר גם בלי השרשרת מ-ones החדש ל-twos : בכל ביט
            ones הבא הוא <span dir="ltr">x ? ~ones & ~twos : ones</span> ו-twos הבא הוא
            <span dir="ltr">x ? ones : twos</span>, שניהם מהערכים הישנים. בסוף, ones הוא הבודד.

    - **שני בודדים, השאר פעמיים :** שני מספרים מופיעים פעם אחת, וכל השאר פעמיים. איך מוצאים את
      שניהם בזיכרון \( O(1) \)?

        ??? fu-answer "תשובה"
            ה-XOR של הכול הוא <span dir="ltr">a ^ b</span>, ולא 0, כי \( a \ne b \). בוחרים ביט דלוק
            בו, למשל הנמוך, <span dir="ltr">d & −d</span>, ועושים XOR נפרד למספרים שהביט הזה דלוק בהם
            ולאלה שלא : \( a \) ו-\( b \) נופלים בקבוצות שונות, וכל זוג נופל כולו באותה קבוצה. זו החלוקה
            לפי ביט של [שאלה 0058](../senior/0058-missing-tags.md).

    - **האם הקלט עומד בכלל :** הפונקציה מחזירה מספר גם כשהכלל לא מתקיים. איך בודקים את התשובה?

        ??? fu-answer "תשובה"
            מעבר שני שסופר כמה פעמים התשובה מופיעה : אם לא פעם אחת, הכלל הופר. ב-<span dir="ltr">[2, 3, 2, 5, 2]</span>
            ‏`single_thrice` מחזירה 6, שלא מופיע בכלל. אבל זו בדיקה חלקית : ב-<span dir="ltr">[1, 4, 4]</span>
            היא מחזירה 1, שמופיע פעם אחת, אף ש-4 מופיע פעמיים. בדיקה מלאה צריכה זיכרון.
