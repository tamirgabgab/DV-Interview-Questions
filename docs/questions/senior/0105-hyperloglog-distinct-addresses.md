---
id: 105
title: כמה כתובות שונות עברו באפיק – HyperLogLog בפחות מקילובייט
level: senior
difficulty: hard
kind: code
tags: [probability, algorithms, bitwise, digital-design, python, systemverilog]
source: "HyperLogLog של Flajolet, Fusy, Gandouet ו-Meunier (2007), עם המערבל של splitmix64"
added: 2026-11-13
---

## השאלה

מוניטור על אפיק רואה מיליוני טרנזקציות בכל ריצה, וצריך לדווח **כמה כתובות שונות** היו בהן. זה
מדד של כיסוי מרחב הכתובות : האם הבדיקה באמת מפזרת כתובות, או חוזרת שוב ושוב על אותן שורות.
למוניטור, בחומרה או בבודק שרץ לצד הסימולציה, אין זיכרון לשמור את הכתובות עצמן. הציעו שיטה
שמעריכה את המספר בדיוק של אחוזים בודדים, בפחות מקילובייט, ושמתעדכנת בקצב של טרנזקציה בכל שעון.

הכתובות הן של 64 ביטים, וכתובת שחוזרת נספרת פעם אחת.

- **סעיף א – ספירה מדויקת :** הדרך הישירה, וכמה זיכרון היא צריכה.
- **סעיף ב – רגיסטר אחד :** מספר קטן אחד שגדל עם מספר הכתובות השונות.
- **סעיף ג – HyperLogLog :** הרבה רגיסטרים קטנים, והממוצע הנכון שלהם.
- **סעיף ד – בחומרה :** יחידה שמעדכנת את הרגיסטרים בכל שעון, בצנרת.

??? interviewer "מה המראיין בודק"
    - **זיכרון מול דיוק :** האם המועמד מבין מה עולה תשובה מדויקת, ומוכן להחליף אותה באומדן
      עם שגיאה ידועה.
    - **הסתברות :** האם הוא יודע לחשב סיכוי של רצף ביטים, ולהסיק ממנו גודל.
    - **ממוצעים ושגיאה :** איך מקטינים את הרעש של הרבה אומדנים, ואיזה ממוצע לא נגרר אחרי ערך
      קיצוני אחד.
    - **חומרה ואימות :** צנרת שקוראת, משנה וכותבת את אותו זיכרון, ואיך בודקים רכיב שהתשובה שלו
      היא אומדן.

---

### סעיף א – ספירה מדויקת

כתבו פונקציה שמקבלת רצף של כתובות ומחזירה כמה כתובות שונות יש בו. כמה זיכרון היא צריכה כשיש
בו מיליון כתובות שונות?

??? tip "רמז 1"
    כשמגיעה כתובת, איך יודעים אם היא כבר הופיעה?

??? tip "רמז 2"
    מה חייב להישאר בזיכרון בסוף הרצף, כדי שהתשובה לכתובת הבאה תהיה נכונה?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שומרים את הכתובות שהופיעו בטבלת גיבוב (hash set) ומחזירים את הגודל שלה : זמן קבוע בממוצע
        לכל טרנזקציה, אבל זיכרון שגדל עם מספר הכתובות השונות \( n \). מיליון כתובות של 8 בתים הן
        8,000,000 בתים, כ-8 MB, עוד לפני התקורה של הטבלה. אי אפשר הרבה פחות : כל שיטה מדויקת צריכה
        כ-5.7 MB למיליון כתובות.

    <!-- cost: זמן \( O(1) \) לטרנזקציה | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    כתובת חדשה מגדילה את הספירה, וכתובת שכבר הופיעה לא. כדי להבדיל ביניהן צריך לזכור את כל
    הכתובות שהופיעו, ולשאול מהר אם כתובת נמצאת ביניהן. טבלת גיבוב עונה על זה בזמן קבוע בממוצע. מיון
    של כל הכתובות וספירה של הערכים השונים נותן אותה תשובה, ב-\( O(N \log N) \) ובאותו זיכרון.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="distinct_exact"
        def distinct_exact(stream):
            seen = set()                       # every address seen, once
            for a in stream:
                seen.add(a)
            return len(seen)
        ```

    === "SystemVerilog"
        ```systemverilog title="function automatic int distinct_exact"
        function automatic int distinct_exact(logic [63:0] stream[$]);
          bit seen[logic [63:0]];              // (1)!
          foreach (stream[i]) seen[stream[i]] = 1;
          return seen.num();
        endfunction
        ```

        1. מערך אסוציאטיבי : יש בו רק המפתחות שנכתבו, ולכן הוא תופס זיכרון לכל כתובת שהופיעה, לא
           לכל \( 2^{64} \) הכתובות.

    #### למה זה נכון { .sol-proof }

    **הספירה.** כל כתובת נכנסת לטבלה, וכתובת שכבר בה לא נוספת שוב. בסוף יש בטבלה בדיוק הכתובות
    השונות, כל אחת פעם אחת.

    **אי אפשר בפחות.** נניח ששיטה מדויקת עברה על רצף של \( n \) כתובות שונות. אם תגיע עכשיו כתובת
    \( x \), הספירה תגדל בדיוק כש-\( x \) לא הייתה ברצף. לכן מהזיכרון של השיטה אפשר לשחזר את כל
    הקבוצה : שתי קבוצות שונות חייבות להשאיר זיכרון שונה. יש \( \binom{2^{64}}{n} \) קבוצות כאלה,
    והזיכרון צריך לפחות \( \log_2 \binom{2^{64}}{n} \) ביטים. למיליון כתובות זה כ-45.5 מיליון ביטים,
    כ-5.7 MB.

    #### סיבוכיות { .sol-cost }

    זמן קבוע בממוצע לכל טרנזקציה, וזיכרון של 8 בתים לכל כתובת שונה, ועוד התקורה של הטבלה. למוניטור
    בחומרה זה זיכרון בגודל של כל הכתובות שהבדיקה נגעה בהן, ולבודק בסימולציה זה זיכרון שגדל בלי
    גבול עם אורך הריצה.

---

### סעיף ב – רגיסטר אחד

נניח שיש פונקציית גיבוב (hash) שהופכת כל כתובת ל-64 ביטים שנראים אקראיים, ותמיד לאותם ביטים
לאותה כתובת. **הדרגה** של hash היא מספר האפסים המובילים שלו ועוד 1, כלומר המקום של ה-1
הראשון. מה הסיכוי שהדרגה היא בדיוק \( k \)? שמרו מספר אחד בלבד, \( R \) : המקסימום של הדרגה על
כל הכתובות. איך מעריכים ממנו את מספר הכתובות השונות, למה כתובות שחוזרות לא משנות אותו, וכמה
האומדן מדויק?

??? tip "רמז 1"
    כל ביט של ה-hash הוא כמו הטלה של מטבע הוגן. בכמה כתובות שונות צריך לעבור, בערך, כדי לראות
    hash שמתחיל ב-10 אפסים?

??? tip "רמז 2"
    כתובת שחוזרת נותנת את אותו hash בדיוק. מה זה עושה למקסימום? ומה ההסתברות שהמקסימום של
    \( n \) דרגות קטן מ-\( k \)?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        הדרגה היא \( k \) בהסתברות \( 2^{-k} \) : ‏\( k - 1 \) אפסים ואחריהם 1. לכן היא לפחות \( k \)
        בהסתברות \( 2^{-(k-1)} \), ומבין \( n \) כתובות שונות המקסימום \( R \) קרוב ל-\( \log_2 n \).
        האומדן הוא \( 2^R \), ומספיק לו בית אחד. כתובת שחוזרת נותנת את אותה דרגה ולא משנה את
        המקסימום. אבל האומדן רועש : הוא תמיד חזקה של 2, ולאלף כתובות הוא פי 8 או יותר מהאמת
        ב-21.7% מהמקרים.

    <!-- cost: זמן \( O(1) \) לטרנזקציה | זיכרון בית אחד -->

    #### הרעיון { .sol-idea }

    ה-hash הוא 64 הטלות של מטבע. hash שמתחיל ב-\( k - 1 \) אפסים נדיר : אחד מכל \( 2^{k-1} \).
    אם ראינו hash כזה, כנראה עברו בערך \( 2^{k-1} \) כתובות שונות או יותר. המקסימום של הדרגה
    שומר בדיוק את הרצף הנדיר ביותר שנראה עד עכשיו. למשל, ה-hash של הכתובת 877,363,008 מתחיל בשלושה
    אפסים, והדרגה שלו 4 :

    <!-- gen 0 -->

    <svg class="figure hll-hash" viewBox="0 0 355 134" style="max-width:22.188rem" direction="ltr" role="img" aria-label="64 הביטים של ה-hash של הכתובת 877363008, בארבע שורות של 16, הביט העליון ראשון. 3 אפסים מובילים ואחריהם 1 : הדרגה 4"><rect class="hll-bit is-zero" x="30" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-zero" x="38.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-zero" x="49" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-zero" x="57.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-zero" x="68" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-zero" x="76.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-one" x="87" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-one" x="95.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="111" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="119.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="130" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="138.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="149" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="157.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="168" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="176.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="192" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="200.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="211" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="219.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="230" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="238.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="249" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="257.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="273" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="281.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="292" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="300.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="311" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="319.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="330" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="338.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="30" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="38.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="49" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="57.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="68" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="76.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="87" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="95.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="111" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="119.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="130" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="138.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="149" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="157.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="168" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="176.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="192" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="200.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="211" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="219.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="230" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="238.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="249" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="257.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="273" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="281.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="292" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="300.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="311" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="319.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="330" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="338.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="30" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="38.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="49" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="57.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="68" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="76.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="87" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="95.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="111" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="119.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="130" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="138.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="149" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="157.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="168" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="176.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="192" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="200.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="211" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="219.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="230" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="238.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="249" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="257.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="273" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="281.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="292" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="300.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="311" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="319.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="330" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="338.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="30" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="38.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="49" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="57.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="68" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="76.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="87" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="95.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="111" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="119.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="130" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="138.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="149" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="157.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="168" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="176.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="192" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="200.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="211" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="219.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="230" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="238.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="249" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="257.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="273" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="281.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="292" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="300.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="311" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="319.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="330" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="338.5" y="121.0" text-anchor="middle">1</text><text class="hll-bitno" x="25" y="24.0" text-anchor="end">63</text><text class="hll-bitno" x="25" y="56.0" text-anchor="end">47</text><text class="hll-bitno" x="25" y="88.0" text-anchor="end">31</text><text class="hll-bitno" x="25" y="120.0" text-anchor="end">15</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="hll-key-zero"></i>האפסים המובילים</span><span><i class="hll-key-one"></i>ה-1 הראשון : הדרגה</span></span>

    <!-- /gen -->

    כך מתנהג הרגיסטר האחד על רצפים של כתובות שונות שגדלים פי 10 בכל שורה :

    <!-- gen 2 -->

    | כתובות שונות | רגיסטר אחד R | האומדן 2<sup>R</sup> | פי |
    |:-:|:-:|:-:|:-:|
    | 10 | 5 | 32 | ‏<span dir="ltr">3.20</span> |
    | 100 | 7 | 128 | ‏<span dir="ltr">1.28</span> |
    | 1,000 | 10 | 1,024 | ‏<span dir="ltr">1.02</span> |
    | 10,000 | 13 | 8,192 | ‏<span dir="ltr">0.82</span> |
    | 100,000 | 20 | 1,048,576 | ‏<span dir="ltr">10.49</span> |
    | 1,000,000 | 20 | 1,048,576 | ‏<span dir="ltr">1.05</span> |

    <!-- /gen -->

    האומדן קופץ בחזקות של 2, ומ-100,000 עד 1,000,000 הוא לא זז בכלל. הוא תלוי ב-hash אחד, הנדיר
    ביותר שנראה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ה-hash :** ‏mix64, המערבל שבסוף splitmix64 : הוספה של קבוע, ושני סבבים של XOR עם הזזה
       ואחריו כפל. כל ביט של הכתובת משפיע על כל ביטי התוצאה.
    2. **הדרגה :** מספר האפסים המובילים ועוד 1, ו-65 ל-hash שהוא 0.
    3. **העדכון :** ‏\( R \leftarrow \max(R, \text{rank}) \) בכל טרנזקציה.
    4. **האומדן :** ‏\( 2^R \), כשמבקשים אותו.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="one_register" linenums="1" hl_lines="7 8 14 20"
        MASK64 = (1 << 64) - 1


        def mix64(x):
            """splitmix64's finalizer: a 64-bit address -> 64 bits that look random."""
            x = (x + 0x9E3779B97F4A7C15) & MASK64
            x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9 & MASK64    # (1)!
            x = (x ^ (x >> 27)) * 0x94D049BB133111EB & MASK64
            return x ^ (x >> 31)


        def rank(w, width):
            """The leading zeros of a width-bit number, plus 1: width + 1 when it is 0."""
            return width - w.bit_length() + 1                     # (2)!


        def one_register(stream):
            r = 0
            for a in stream:
                r = max(r, rank(mix64(a), 64))
            return r                                              # the estimate is 2 ** r
        ```

        1. ה-XOR עם הזזה מוריד ביטים עליונים לתחתונים, והכפל מעלה כל ביט לכל הביטים שמעליו. אחרי
           שני סבבים, שינוי של ביט אחד בכתובת הופך בערך חצי מביטי התוצאה.
        2. ‏`bit_length` הוא המקום של ה-1 העליון, ולכן \( \text{width} - \) ‏`bit_length` הם האפסים
           שמעליו.

    === "SystemVerilog"
        ```systemverilog title="function automatic logic [63:0] mix64" linenums="1" hl_lines="4 5 12 19"
        // splitmix64's finalizer: a 64-bit address -> 64 bits that look random
        function automatic logic [63:0] mix64(logic [63:0] x);
          x = x + 64'h9E37_79B9_7F4A_7C15;
          x = (x ^ (x >> 30)) * 64'hBF58_476D_1CE4_E5B9;           // (1)!
          x = (x ^ (x >> 27)) * 64'h94D0_49BB_1331_11EB;
          return x ^ (x >> 31);
        endfunction

        // The leading zeros of the low `width` bits of w, plus 1 (width + 1 when they are all 0)
        function automatic int rank(logic [63:0] w, int width);
          for (int i = width - 1; i >= 0; i--)
            if (w[i]) return width - i;
          return width + 1;
        endfunction

        function automatic int one_register(logic [63:0] stream[$]);
          int r = 0, k;
          foreach (stream[i]) begin
            k = rank(mix64(stream[i]), 64);
            if (k > r) r = k;
          end
          return r;                                                  // the estimate: 2 ** r
        endfunction
        ```

        1. ב-SystemVerilog החשבון ב-64 ביטים לא חורג מהרוחב : הכפל נחתך ל-64 הביטים התחתונים, כמו
           ה-`& MASK64` של Python. בחומרה זה מכפל של 64 על 64 ביטים, ולכן בצנרת של סעיף ד הוא
           יכול להתפרס על כמה שלבים.

    #### למה זה נכון { .sol-proof }

    **הסיכוי.** הדרגה לפחות \( k \) כש-\( k - 1 \) הביטים הראשונים הם 0 : הסתברות \( 2^{-(k-1)} \).
    ל-\( n \) כתובות שונות יש \( n \) ערכי hash בלתי תלויים, ולכן

    \[ P(R < k) = \left(1 - 2^{-(k-1)}\right)^n \approx e^{-n / 2^{k-1}}. \]

    כש-\( 2^{k-1} \) הרבה קטן מ-\( n \) זה כמעט 0, וכשהוא הרבה גדול מ-\( n \) זה כמעט 1. המעבר
    הוא סביב \( 2^{k-1} \approx n \), ולכן \( 2^R \) קרוב ל-\( n \) עד פקטור קבוע.

    **כפילויות.** כתובת שחוזרת נותנת את אותו hash, ולכן את אותה דרגה, והמקסימום לא משתנה. \( R \)
    תלוי רק בקבוצת הכתובות, לא בסדר שלהן ולא בכמה פעמים כל אחת הופיעה.

    **הרעש.** מהנוסחה, \( P(R = k) = (1 - 2^{-k})^n - (1 - 2^{-(k-1)})^n \). לאלף כתובות שונות :

    <!-- gen 3 -->

    | האומדן 2<sup>R</sup> | פי | ההסתברות |
    |:-:|:-:|:-:|
    | עד 256 | ‏<span dir="ltr">≤ 0.26</span> | ‏<span dir="ltr">2.0%</span> |
    | 512 | ‏<span dir="ltr">0.51</span> | ‏<span dir="ltr">12.2%</span> |
    | 1,024 | ‏<span dir="ltr">1.02</span> | ‏<span dir="ltr">23.5%</span> |
    | 2,048 | ‏<span dir="ltr">2.05</span> | ‏<span dir="ltr">23.7%</span> |
    | 4,096 | ‏<span dir="ltr">4.10</span> | ‏<span dir="ltr">17.0%</span> |
    | 8,192 | ‏<span dir="ltr">8.19</span> | ‏<span dir="ltr">10.2%</span> |
    | 16,384 ומעלה | ‏<span dir="ltr">≥ 16.38</span> | ‏<span dir="ltr">11.5%</span> |

    <!-- /gen -->

    רק כרבע מהמקרים נותנים את 1,024, החזקה הקרובה, ו-21.7% נותנים פי 8 או יותר. הזנב העליון ארוך,
    כי hash אחד עם הרבה אפסים מספיק כדי להקפיץ את \( R \).

    #### סיבוכיות { .sol-cost }

    ‏hash אחד, ספירה של אפסים מובילים והשוואה לכל טרנזקציה. הרגיסטר מחזיק דרגה עד 65, ולכן בית
    אחד מספיק. הוא סופר עד \( 2^{64} \) כתובות, אבל השגיאה שלו היא פקטור, לא אחוזים.

---

### סעיף ג – HyperLogLog

חלקו את הכתובות ל-\( m = 2^p \) קבוצות לפי \( p \) הביטים הראשונים של ה-hash, ושמרו לכל קבוצה
רגיסטר כמו של סעיף ב, מהדרגה של הביטים שנשארו. איך משלבים את \( m \) הרגיסטרים לאומדן אחד? מה
עושים כשיש מעט כתובות ורגיסטרים נשארים ריקים? כמה רגיסטרים צריך לשגיאה של כ-3%, וכמה זיכרון
הם תופסים? ואיך מאחדים את הספירות של שני מוניטורים?

??? tip "רמז 1"
    כל רגיסטר רואה בערך \( n / m \) כתובות, ו-\( 2^{R_j} \) מעריך את המספר הזה. למה ממוצע רגיל
    של \( m \) האומדנים האלה עדיין רגיש לרגיסטר אחד שהתמזל?

??? tip "רמז 2"
    רגיסטר ריק פירושו שאף כתובת לא נפלה בו. כמה רגיסטרים ריקים מצפים לראות אחרי \( n \) כתובות?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏\( p \) הביטים הראשונים בוחרים רגיסטר \( j \), ו-\( R_j \) שומר את הדרגה המקסימלית של
        \( 64 - p \) הביטים האחרים. האומדן הוא \( \alpha_m m^2 / \sum_j 2^{-R_j} \), עם
        \( \alpha_m = 0.7213 / (1 + 1.079 / m) \) : ממוצע **הרמוני** של \( 2^{R_j} \), שלא נגרר אחרי
        רגיסטר אחד גבוה. כשהאומדן עד \( 2.5m \) ויש \( V \) רגיסטרים ריקים, מחליפים אותו
        ב-\( m \ln(m / V) \). השגיאה התקנית היא בערך \( 1.04 / \sqrt{m} \) : ‏1,024 רגיסטרים של 6 ביטים,
        768 בתים, נותנים 3.25%. האיחוד של שני מוניטורים הוא המקסימום של כל זוג רגיסטרים.

    <!-- cost: זמן \( O(1) \) לטרנזקציה | זיכרון \( 6m \) ביטים | שגיאה \( 1.04/\sqrt{m} \) -->

    #### הרעיון { .sol-idea }

    רגיסטר אחד רועש מדי, ולכן מחלקים את הכתובות ל-\( m \) קבוצות בלי לשמור אותן : ה-hash עצמו
    בוחר קבוצה. אותו hash של הכתובת 877,363,008, עכשיו עם \( p = 4 \) : ארבעת הביטים הראשונים,
    ‏0001, הם רגיסטר 1, והדרגה נספרת רק מהביטים שאחריהם.

    <!-- gen 4 -->

    <svg class="figure hll-hash" viewBox="0 0 355 134" style="max-width:22.188rem" direction="ltr" role="img" aria-label="64 הביטים של ה-hash של הכתובת 877363008, בארבע שורות של 16, הביט העליון ראשון. הביטים 4 הראשונים, 0001, בוחרים את רגיסטר 1, ואחריהם 3 אפסים ו-1 : הדרגה 4"><rect class="hll-bit is-idx" x="30" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-idx" x="38.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-idx" x="49" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-idx" x="57.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-idx" x="68" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-idx" x="76.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-idx" x="87" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-idx" x="95.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-zero" x="111" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-zero" x="119.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-zero" x="130" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-zero" x="138.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-zero" x="149" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-zero" x="157.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-one" x="168" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-one" x="176.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="192" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="200.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="211" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="219.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="230" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="238.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="249" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="257.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="273" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="281.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="292" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="300.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="311" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="319.5" y="25.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="330" y="8" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="338.5" y="25.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="30" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="38.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="49" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="57.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="68" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="76.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="87" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="95.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="111" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="119.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="130" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="138.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="149" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="157.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="168" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="176.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="192" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="200.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="211" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="219.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="230" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="238.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="249" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="257.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="273" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="281.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="292" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="300.5" y="57.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="311" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="319.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="330" y="40" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="338.5" y="57.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="30" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="38.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="49" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="57.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="68" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="76.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="87" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="95.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="111" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="119.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="130" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="138.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="149" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="157.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="168" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="176.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="192" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="200.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="211" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="219.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="230" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="238.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="249" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="257.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="273" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="281.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="292" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="300.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="311" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="319.5" y="89.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="330" y="72" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="338.5" y="89.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="30" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="38.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="49" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="57.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="68" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="76.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="87" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="95.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="111" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="119.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="130" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="138.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="149" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="157.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="168" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="176.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="192" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="200.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="211" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="219.5" y="121.0" text-anchor="middle">1</text><rect class="hll-bit is-rest" x="230" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="238.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="249" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="257.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="273" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="281.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="292" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="300.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="311" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="319.5" y="121.0" text-anchor="middle">0</text><rect class="hll-bit is-rest" x="330" y="104" width="17" height="24" rx="2"/><text class="hll-bit-t is-rest" x="338.5" y="121.0" text-anchor="middle">1</text><text class="hll-bitno" x="25" y="24.0" text-anchor="end">63</text><text class="hll-bitno" x="25" y="56.0" text-anchor="end">47</text><text class="hll-bitno" x="25" y="88.0" text-anchor="end">31</text><text class="hll-bitno" x="25" y="120.0" text-anchor="end">15</text></svg>

    <!-- /gen -->

    <!-- gen 5 -->

    <span class="viz-legend"><span><i class="hll-key-idx"></i>הביטים שבוחרים את הרגיסטר</span><span><i class="hll-key-zero"></i>האפסים המובילים</span><span><i class="hll-key-one"></i>ה-1 הראשון : הדרגה</span></span>

    <!-- /gen -->

    כל רגיסטר הוא רגיסטר של סעיף ב על כ-\( n / m \) כתובות, ו-\( 2^{R_j} \) מעריך את המספר הזה. אבל
    האומדנים האלה נוטים לערכים גבוהים מאוד : כמו בטבלה של סעיף ב, אחד מתוך כמה רגיסטרים מראה פי 8
    ויותר. ממוצע רגיל של \( 2^{R_j} \) הולך אחרי הרגיסטר הגבוה ביותר. הממוצע ההרמוני,
    \( m / \sum_j 2^{-R_j} \), הולך אחרי הרוב : רגיסטר גבוה תורם לסכום מספר קרוב ל-0, כמעט כלום. כפול
    \( m \) קבוצות, ועם תיקון של הטיה \( \alpha_m \), זה האומדן.

    כך נראים 16 הרגיסטרים אחרי 50 כתובות שונות, וכך מחושב האומדן שלהם :

    <!-- gen 6 -->

    <svg class="figure hll-regs" viewBox="0 0 356 122" style="max-width:22.250rem" direction="ltr" role="img" aria-label="16 הרגיסטרים אחרי 50 הכתובות הראשונות של הזרם האקראי, לפי הסדר : 2, 4, 3, 1, 2, 4, 2, 3, 1, 4, 2, 4, 2, 3, 4, 2. 0 ריקים"><g class="hll-reg hll-c3"><rect x="4" y="4" width="40" height="40" rx="3"/><text x="24.0" y="30.0" text-anchor="middle">2</text><title>רגיסטר 0 : 2</title></g><text class="hll-regno" x="24.0" y="57" text-anchor="middle">0</text><g class="hll-reg hll-c6"><rect x="48" y="4" width="40" height="40" rx="3"/><text x="68.0" y="30.0" text-anchor="middle">4</text><title>רגיסטר 1 : 4</title></g><text class="hll-regno" x="68.0" y="57" text-anchor="middle">1</text><g class="hll-reg hll-c5"><rect x="92" y="4" width="40" height="40" rx="3"/><text x="112.0" y="30.0" text-anchor="middle">3</text><title>רגיסטר 2 : 3</title></g><text class="hll-regno" x="112.0" y="57" text-anchor="middle">2</text><g class="hll-reg hll-c2"><rect x="136" y="4" width="40" height="40" rx="3"/><text x="156.0" y="30.0" text-anchor="middle">1</text><title>רגיסטר 3 : 1</title></g><text class="hll-regno" x="156.0" y="57" text-anchor="middle">3</text><g class="hll-reg hll-c3"><rect x="180" y="4" width="40" height="40" rx="3"/><text x="200.0" y="30.0" text-anchor="middle">2</text><title>רגיסטר 4 : 2</title></g><text class="hll-regno" x="200.0" y="57" text-anchor="middle">4</text><g class="hll-reg hll-c6"><rect x="224" y="4" width="40" height="40" rx="3"/><text x="244.0" y="30.0" text-anchor="middle">4</text><title>רגיסטר 5 : 4</title></g><text class="hll-regno" x="244.0" y="57" text-anchor="middle">5</text><g class="hll-reg hll-c3"><rect x="268" y="4" width="40" height="40" rx="3"/><text x="288.0" y="30.0" text-anchor="middle">2</text><title>רגיסטר 6 : 2</title></g><text class="hll-regno" x="288.0" y="57" text-anchor="middle">6</text><g class="hll-reg hll-c5"><rect x="312" y="4" width="40" height="40" rx="3"/><text x="332.0" y="30.0" text-anchor="middle">3</text><title>רגיסטר 7 : 3</title></g><text class="hll-regno" x="332.0" y="57" text-anchor="middle">7</text><g class="hll-reg hll-c2"><rect x="4" y="62" width="40" height="40" rx="3"/><text x="24.0" y="88.0" text-anchor="middle">1</text><title>רגיסטר 8 : 1</title></g><text class="hll-regno" x="24.0" y="115" text-anchor="middle">8</text><g class="hll-reg hll-c6"><rect x="48" y="62" width="40" height="40" rx="3"/><text x="68.0" y="88.0" text-anchor="middle">4</text><title>רגיסטר 9 : 4</title></g><text class="hll-regno" x="68.0" y="115" text-anchor="middle">9</text><g class="hll-reg hll-c3"><rect x="92" y="62" width="40" height="40" rx="3"/><text x="112.0" y="88.0" text-anchor="middle">2</text><title>רגיסטר 10 : 2</title></g><text class="hll-regno" x="112.0" y="115" text-anchor="middle">10</text><g class="hll-reg hll-c6"><rect x="136" y="62" width="40" height="40" rx="3"/><text x="156.0" y="88.0" text-anchor="middle">4</text><title>רגיסטר 11 : 4</title></g><text class="hll-regno" x="156.0" y="115" text-anchor="middle">11</text><g class="hll-reg hll-c3"><rect x="180" y="62" width="40" height="40" rx="3"/><text x="200.0" y="88.0" text-anchor="middle">2</text><title>רגיסטר 12 : 2</title></g><text class="hll-regno" x="200.0" y="115" text-anchor="middle">12</text><g class="hll-reg hll-c5"><rect x="224" y="62" width="40" height="40" rx="3"/><text x="244.0" y="88.0" text-anchor="middle">3</text><title>רגיסטר 13 : 3</title></g><text class="hll-regno" x="244.0" y="115" text-anchor="middle">13</text><g class="hll-reg hll-c6"><rect x="268" y="62" width="40" height="40" rx="3"/><text x="288.0" y="88.0" text-anchor="middle">4</text><title>רגיסטר 14 : 4</title></g><text class="hll-regno" x="288.0" y="115" text-anchor="middle">14</text><g class="hll-reg hll-c3"><rect x="312" y="62" width="40" height="40" rx="3"/><text x="332.0" y="88.0" text-anchor="middle">2</text><title>רגיסטר 15 : 2</title></g><text class="hll-regno" x="332.0" y="115" text-anchor="middle">15</text></svg>

    <!-- /gen -->

    <!-- gen 7 -->

    | הגודל | הערך |
    |---|:-:|
    | הסכום <span dir="ltr">Σ 2<sup>−R[j]</sup></span> | ‏<span dir="ltr">3.1875</span> |
    | הקבוע ‏α<sub>16</sub> | ‏<span dir="ltr">0.6757</span> |
    | האומדן <span dir="ltr">α m² / Σ</span> | ‏<span dir="ltr">54.3</span> |
    | רגיסטרים ריקים V | 0 |
    | הסף של התיקון <span dir="ltr">2.5 m</span> | ‏<span dir="ltr">40</span> |

    <!-- /gen -->

    האומדן 54.3 גבוה מ-\( 2.5m = 40 \) ואין רגיסטר ריק, ולכן התיקון לא נכנס. מול 50 האמיתיות זו
    שגיאה של 8.5%, בתוך השגיאה התקנית של 16 רגיסטרים, 26%.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הפיצול :** ‏\( j \) הוא \( p \) הביטים העליונים של ה-hash, ו-\( w \) הם \( 64 - p \) הביטים
       האחרים.
    2. **העדכון :** ‏\( R_j \leftarrow \max(R_j, \text{rank}(w)) \), דרגה על רוחב \( 64 - p \).
    3. **האומדן :** ‏\( E = \alpha_m m^2 / \sum_j 2^{-R_j} \).
    4. **טווח קטן :** אם \( E \le 2.5m \) ויש \( V > 0 \) רגיסטרים ריקים, האומדן הוא \( m \ln(m / V) \).
    5. **איחוד :** שני מוניטורים עם אותו \( p \) ואותו hash מתאחדים ברגיסטר המקסימלי בכל מקום.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="HLL" linenums="1" hl_lines="13 14 15 20 23 27"
        import math


        class HLL:
            """HyperLogLog with m = 2^p registers, each the max rank of the addresses it got."""

            def __init__(self, p):
                self.p, self.m = p, 1 << p
                self.regs = [0] * self.m

            def add(self, a):
                h = mix64(a)
                j = h >> (64 - self.p)                               # (1)!
                w = h & ((1 << (64 - self.p)) - 1)
                self.regs[j] = max(self.regs[j], rank(w, 64 - self.p))

            def estimate(self):
                m = self.m
                alpha = 0.7213 / (1 + 1.079 / m)                     # (2)!
                e = alpha * m * m / sum(2.0 ** -r for r in self.regs)
                zeros = self.regs.count(0)
                if e <= 2.5 * m and zeros > 0:
                    return m * math.log(m / zeros)                   # (3)!
                return e

            def merge(self, other):
                self.regs = [max(a, b) for a, b in zip(self.regs, other.regs)]   # (4)!
        ```

        1. הביטים העליונים בוחרים רגיסטר, והתחתונים נותנים דרגה. אסור שאותם ביטים ישמשו לשניהם :
           ראו את המלכודות.
        2. הקבוע של המאמר ל-\( m \ge 128 \). ל-16, ל-32 ול-64 המאמר נותן 0.673, ‏0.697 ו-0.709, והנוסחה
           רחוקה מהם פחות מחצי אחוז.
        3. ספירה ליניארית (linear counting) : ממספר הרגיסטרים שאף כתובת לא הגיעה אליהם.
        4. המקסימום לא תלוי בסדר ולא בכפילויות, ולכן האיחוד יוצא בדיוק כמו מוניטור אחד שראה את שני
           הזרמים.

    === "SystemVerilog"
        ```systemverilog title="class hll" linenums="1" hl_lines="14 15 16 26 27 32"
        // HyperLogLog with m = 2^p registers, each the max rank of the addresses it got
        class hll;
          int p, m;
          byte unsigned regs[];

          function new(int p);
            this.p = p;
            m = 1 << p;
            regs = new[m];                                // every register 0
          endfunction

          function void add(logic [63:0] a);
            logic [63:0] h = mix64(a);
            int j = int'(h >> (64 - p));                  // the top p bits: the register
            int r = rank(h, 64 - p);                      // the other 64 - p bits: the rank
            if (r > regs[j]) regs[j] = byte'(r);
          endfunction

          function real estimate();
            real alpha = 0.7213 / (1 + 1.079 / m), sum = 0, e;
            int zeros = 0;
            foreach (regs[j]) begin
              sum += 2.0 ** (-real'(regs[j]));
              if (regs[j] == 0) zeros++;
            end
            e = alpha * m * m / sum;
            if (e <= 2.5 * m && zeros > 0) return m * $ln(real'(m) / zeros);
            return e;
          endfunction

          function void merge(hll other);
            foreach (regs[j]) if (other.regs[j] > regs[j]) regs[j] = other.regs[j];
          endfunction
        endclass
        ```

    #### למה זה נכון { .sol-proof }

    **כפילויות, סדר ואיחוד.** כל רגיסטר הוא מקסימום, ומקסימום לא משתנה כשמוסיפים ערך שכבר היה ולא
    תלוי בסדר. לכן הרגיסטרים תלויים רק בקבוצת הכתובות. ‏15,000 טרנזקציות על 5,000 כתובות שונות
    נותנות את האומדן 5,115, בדיוק כמו 5,000 הכתובות לבד. מוניטור אחד ראה את הכתובות 1 עד 60,000
    של הזרם האקראי, ומוניטור אחר את 30,001 עד 90,000. האומדנים שלהם 62,702 ו-63,234, והאיחוד, במקסימום
    של כל זוג רגיסטרים, נותן 96,382 מול 90,000 כתובות שונות. הרגיסטרים של האיחוד זהים לאלה של מוניטור
    שראה את שני הזרמים.

    **הממוצע ההרמוני.** ב-200 הריצות של הטבלה למטה, האומדן עם ממוצע רגיל,
    \( \alpha_m m \cdot \frac{1}{m} \sum_j 2^{R_j} \), טועה בממוצע ריבועי ב-2,729% עם 1,024 רגיסטרים,
    וריצה אחת נותנת יותר מפי 300 מהאמת. עם הממוצע ההרמוני השגיאה היא 2.92%.

    **הטווח הקטן.** כתובת נופלת לכל רגיסטר בהסתברות \( 1/m \), ולכן אחרי \( n \) כתובות כל רגיסטר
    ריק בהסתברות \( (1 - 1/m)^n \approx e^{-n/m} \). מספר הרגיסטרים הריקים \( V \) הוא בערך
    \( m e^{-n/m} \), ומכאן \( n \approx m \ln(m / V) \). הנוסחה ההרמונית מניחה שכל רגיסטר ראה הרבה
    כתובות, ובלי אף כתובת היא נותנת \( \alpha_m m \), כ-738 ל-1,024 רגיסטרים. על 100 כתובות שונות
    היא נותנת 784, והספירה הליניארית, עם 930 רגיסטרים ריקים, 98.6.

    **השגיאה.** השגיאה התקנית היחסית היא בערך \( 1.04 / \sqrt{m} \) (המאמר של HyperLogLog). על
    הזרם האקראי, עם 1,024 רגיסטרים :

    <!-- gen 8 -->

    | כתובות שונות | האומדן, 1,024 רגיסטרים | השגיאה | רגיסטר אחד |
    |:-:|:-:|:-:|:-:|
    | 10 | 10 | ‏<span dir="ltr">+0.5%</span> | 32 |
    | 100 | 99 | ‏<span dir="ltr">−1.4%</span> | 128 |
    | 1,000 | 1,026 | ‏<span dir="ltr">+2.6%</span> | 1,024 |
    | 10,000 | 10,353 | ‏<span dir="ltr">+3.5%</span> | 8,192 |
    | 100,000 | 106,786 | ‏<span dir="ltr">+6.8%</span> | 1,048,576 |
    | 1,000,000 | 992,011 | ‏<span dir="ltr">−0.8%</span> | 1,048,576 |

    <!-- /gen -->

    ב-100,000 השגיאה 6.8%, יותר מפעמיים השגיאה התקנית. ריצה אחת יכולה ליפול שם, ולכן את השגיאה
    בודקים על הרבה ריצות. ‏200 ריצות של 5,000 כתובות שונות, כל ריצה על כתובות אחרות :

    <!-- gen 9 -->

    | רגיסטרים m | הזיכרון | ‏1.04/√m | השגיאה שנמדדה | מחוץ ל-2σ |
    |:-:|:-:|:-:|:-:|:-:|
    | 16 | 12 בתים | ‏<span dir="ltr">26.00%</span> | ‏<span dir="ltr">28.34%</span> | 14 מתוך 200 |
    | 64 | 48 בתים | ‏<span dir="ltr">13.00%</span> | ‏<span dir="ltr">12.21%</span> | 5 מתוך 200 |
    | 256 | 192 בתים | ‏<span dir="ltr">6.50%</span> | ‏<span dir="ltr">6.77%</span> | 10 מתוך 200 |
    | 1,024 | 768 בתים | ‏<span dir="ltr">3.25%</span> | ‏<span dir="ltr">2.92%</span> | 6 מתוך 200 |

    <!-- /gen -->

    השגיאה שנמדדה קרובה ל-\( 1.04 / \sqrt{m} \) בכל \( m \), ויורדת פי 2 כש-\( m \) גדל פי 4. העמודה
    האחרונה סופרת ריצות עם שגיאה של יותר מפעמיים השגיאה התקנית : בהתפלגות נורמלית מצפים לכ-5%,
    כלומר כ-10 מתוך 200.

    **נסו בעצמכם.** התיבה מעבירה זרם של 20,000 טרנזקציות ועוצרת אחרי 10, 15, 20, 30 ... ובכל עצירה
    מראה את הרגיסטרים ואת השגיאה של האומדן. נסו את הזרם האקראי עם 16 רגיסטרים ואחר כך עם 1,024 :
    הפס האפור סביב השגיאה 0 מצטמצם מ-26% ל-3.25%, והנקודות הכתומות של הרגיסטר האחד קופצות הרחק
    מחוצה לו. אחר כך בחרו כתובות רציפות ו-hash שהוא הכתובת עצמה : כל הכתובות נופלות לרגיסטר אחד,
    והאומדן נשאר 1. מעבר לטבלאות, התיבה מראה איך הרגיסטרים מתמלאים, ומתי האומדן עובר מספירה
    ליניארית לנוסחה ההרמונית.

    <div class="explorer" data-kind="hll" data-stream="rand" data-hash="mix" data-m="64"></div>

    #### סיבוכיות { .sol-cost }

    **זמן.** לכל טרנזקציה hash אחד, ספירה של אפסים מובילים ומקסימום : \( O(1) \). האומדן עובר על
    \( m \) הרגיסטרים בזמן \( O(m) \), ורק כשמבקשים אותו.

    **זיכרון.** עם hash של 64 ביטים ו-\( p = 10 \) הדרגה היא עד \( 64 - 10 + 1 = 55 \), ו-6 ביטים
    מחזיקים אותה. ‏1,024 רגיסטרים הם 6,144 ביטים, 768 בתים, לשגיאה של 3.25%. כל הכפלה של הדיוק
    עולה פי 4 רגיסטרים.

    **הטווח.** הרגיסטרים לא גדלים עם \( n \) : אותם 768 בתים סופרים 100 כתובות או \( 10^{12} \).
    הדרגה גדלה רק כמו \( \log_2 \log_2 n \) ביטים, ומכאן השם.

---

### סעיף ד – בחומרה

תכננו יחידת RTL שמקבלת כתובת בכל שעון ומעדכנת את הרגיסטרים של סעיף ג. הרגיסטרים יושבים
ב-RAM עם קריאה סינכרונית : הערך יוצא שעון אחרי שהכתובת נשלחה. את האומדן עצמו מחשבת התוכנה מהרגיסטרים
בסוף הריצה. מה קורה כששתי כתובות רצופות נופלות באותו רגיסטר? ואיך מאמתים יחידה שכל התפקיד שלה
הוא לתת אומדן?

??? tip "רמז 1"
    חלקו את העבודה לשלבים : hash, פיצול וספירה של אפסים, קריאה של הרגיסטר, מקסימום וכתיבה. באיזה
    שעון כל כתובת קוראת את הרגיסטר שלה, ובאיזה שעון היא כותבת אותו?

??? tip "רמז 2"
    כתובת B נכנסת שעון אחד אחרי A, ושתיהן הולכות לאותו רגיסטר. B קוראת את הרגיסטר באותו שעון שבו A
    כותבת אותו. איזה ערך היא מקבלת, ומה היא כותבת שעון אחר כך?

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        שלושה שלבים : שלב 1 מחשב את ה-hash, שלב 2 מפצל אותו, סופר אפסים ושולח את הקריאה, ושלב 3
        לוקח את המקסימום וכותב. כתובת שנכנסת שעון אחרי כתובת לאותו רגיסטר קוראת את הערך **לפני**
        הכתיבה של הקודמת, וכותבת מעליה : העדכון של הקודמת הולך לאיבוד. התיקון הוא **קידום**
        (forwarding) : שלב 3 משווה את הרגיסטר שלו לכתיבה של השעון הקודם, ואם הם שווים לוקח את הערך
        שנכתב. מאמתים את הרגיסטרים ביט אחרי ביט מול מודל הייחוס, ואת האומדן רק סטטיסטית.

    <!-- cost: שלבים 3 | קצב כתובת בשעון | זיכרון \( 6 \cdot 2^P \) ביטים -->

    #### הרעיון { .sol-idea }

    כל כתובת עוברת hash, פיצול, קריאה, מקסימום וכתיבה. בצנרת כל שלב עובד על כתובת אחרת, ולכן
    נכנסת כתובת בכל שעון. הקושי הוא שהקריאה והכתיבה של אותו רגיסטר רחוקות שעון אחד : כתובת קוראת
    בסוף שלב 2 וכותבת בסוף שלב 3. אם הכתובת שלפניה הלכה לאותו רגיסטר, הכתיבה שלה קורית בדיוק
    באותו שעון שבו הכתובת הזו קוראת, ובקריאה הסינכרונית יוצא הערך הישן. רגיסטרים של "הכתיבה
    האחרונה", הרגיסטר והערך, מתקנים את זה : שלב 3 משתמש בהם במקום בערך שנקרא, כשהרגיסטר זהה.

    <!-- gen 10 -->

    <svg class="figure hll-pipe" viewBox="0 0 508 240" style="max-width:31.750rem" direction="ltr" role="img" aria-label="יחידת העדכון בשלושה שלבים : שלב 1 מחשב את ה-hash, שלב 2 מפצל אותו לרגיסטר ולדרגה וקורא את הרגיסטר, שלב 3 לוקח את המקסימום וכותב. דרך הקידום מחזירה את הכתיבה של השעון הקודם לבורר של שלב 3"><rect class="hll-stage" x="14" y="26" width="104" height="112" rx="5"/><text class="hll-st-name" x="66.0" y="18" text-anchor="middle">stage 1</text><rect class="hll-stage" x="150" y="26" width="150" height="112" rx="5"/><text class="hll-st-name" x="225.0" y="18" text-anchor="middle">stage 2</text><rect class="hll-stage" x="332" y="26" width="162" height="112" rx="5"/><text class="hll-st-name" x="413.0" y="18" text-anchor="middle">stage 3</text><text class="hll-io" x="14" y="160" text-anchor="start">in: valid, addr</text><rect class="hll-op" x="26" y="42" width="80" height="34" rx="5"/><text class="hll-pt" x="66" y="64" text-anchor="middle">mix64</text><rect class="hll-reg" x="26" y="92" width="80" height="34" rx="5"/><text class="hll-pt" x="66" y="114" text-anchor="middle">v1  h1</text><line class="hll-wire" x1="66" y1="76" x2="66" y2="92"/><line class="hll-wire" x1="106" y1="109" x2="160" y2="109"/><path class="hll-head" d="M160,109 l-7,-4 v8 z"/><rect class="hll-op" x="162" y="42" width="126" height="34" rx="5"/><text class="hll-pt" x="225" y="57" text-anchor="middle">j = h[63:64-P]</text><text class="hll-pt" x="225" y="71" text-anchor="middle">r = clz + 1</text><rect class="hll-reg" x="162" y="92" width="126" height="34" rx="5"/><text class="hll-pt" x="225" y="114" text-anchor="middle">v2 j2 r2 q2</text><line class="hll-wire" x1="225" y1="76" x2="225" y2="92"/><line class="hll-wire" x1="288" y1="109" x2="344" y2="109"/><path class="hll-head" d="M344,109 l-7,-4 v8 z"/><rect class="hll-op" x="346" y="42" width="72" height="34" rx="5"/><text class="hll-pt" x="382" y="57" text-anchor="middle">old =</text><text class="hll-pt" x="382" y="71" text-anchor="middle">q2 / wq</text><rect class="hll-op" x="428" y="42" width="54" height="34" rx="5"/><text class="hll-pt" x="455" y="64" text-anchor="middle">max</text><line class="hll-wire" x1="418" y1="59" x2="428" y2="59"/><path class="hll-head" d="M428,59 l-7,-4 v8 z"/><rect class="hll-fwd" x="346" y="92" width="136" height="34" rx="5"/><text class="hll-pt" x="414" y="106" text-anchor="middle">wv wj wq</text><text class="hll-pt-s" x="414" y="120" text-anchor="middle">previous write</text><line class="hll-wire hll-fwd-w" x1="382" y1="92" x2="382" y2="76"/><path class="hll-head hll-fwd-h" d="M382,77 l-4,7 h8 z"/><rect class="hll-ram" x="162" y="180" width="320" height="36" rx="5"/><text class="hll-pt" x="322" y="203" text-anchor="middle">regs [M] : 6 bits each</text><line class="hll-wire" x1="225" y1="180" x2="225" y2="128"/><path class="hll-head" d="M225,128 l-4,7 h8 z"/><text class="hll-pt-s" x="231" y="160" text-anchor="start">read j1</text><line class="hll-wire hll-dim" x1="455" y1="76" x2="455" y2="92"/><path class="hll-wire" d="M482,59 h8 v135 h-8" fill="none"/><path class="hll-head" d="M482,194 l-7,-4 v8 z"/><text class="hll-pt-s" x="490" y="230" text-anchor="end">write regs[j2]</text></svg>

    <!-- /gen -->

    כך עוברות ביחידה, עם 16 רגיסטרים, שלוש כתובות שכולן נופלות ברגיסטר 12 : ‏A ‏(1,984) בדרגה 4, ‏B
    ‏(1,280) בדרגה 1 שעון אחריה, ו-C ‏(1,472) בדרגה 2 שני שעונים אחרי B. בכל שורה מה שכל שלב עושה
    באותו שעון, ‏q הוא הערך שנקרא, ו-R הוא הרגיסטר אחרי סוף השעון. הערך המודגש הגיע בקידום :

    <!-- gen 11 -->

    | שעון | שלב 1 | שלב 2 | שלב 3 | ‏R[12] | ‏R[12] בלי קידום |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | 1 | ‏A | – | – | 0 | 0 |
    | 2 | ‏B | ‏<span dir="ltr">A: r=4, q=0</span> | – | 0 | 0 |
    | 3 | – | ‏<span dir="ltr">B: r=1, q=0</span> | ‏<span dir="ltr">A: max(0, 4)</span> | 4 | 4 |
    | 4 | ‏C | – | ‏<span dir="ltr">B: max(<b>4</b>, 1)</span> | 4 | 1 |
    | 5 | – | ‏<span dir="ltr">C: r=2, q=4</span> | – | 4 | 1 |
    | 6 | – | – | ‏<span dir="ltr">C: max(4, 2)</span> | 4 | 2 |

    <!-- /gen -->

    בשעון 3 ‏A כותבת 4, ובאותו שעון B קוראת ומקבלת 0. בשעון 4 הקידום מחליף את ה-0 ב-4, ו-B
    כותבת \( \max(4, 1) = 4 \). בלי הקידום B כותבת 1, והעדכון של A אבד. C קוראת שני שעונים אחרי B,
    אחרי הכתיבה, ולא צריכה קידום : בלעדיו היא רק ממשיכה מה-1 השגוי ומשאירה 2 במקום 4.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שלב 1 :** ‏h1 מקבל את \( \text{mix64} \) של הכתובת, ו-v1 את valid.
    2. **שלב 2 :** ‏j2 הוא \( P \) הביטים העליונים של h1, ‏r2 הדרגה של השאר, ו-q2 הערך של
       <span dir="ltr">regs[j]</span>, נקרא באותו שעון.
    3. **שלב 3 :** ‏old הוא q2, או wq כשבשעון הקודם נכתב אותו רגיסטר. ‏nv הוא
       <span dir="ltr">max(old, r2)</span>, נכתב ל-<span dir="ltr">regs[j2]</span>, ונשמר ב-wj
       וב-wq לשעון הבא.
    4. **ניקוי :** אחרי reset היחידה מאפסת רגיסטר אחד בכל שעון, ו-busy דולק עד שכולם 0.
    5. **הקריאה של התוכנה :** פתח קריאה נפרד, rd_idx ו-rd_val. התוכנה קוראת את \( 2^P \) הרגיסטרים
       בסוף הריצה ומחשבת את האומדן של סעיף ג.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="pipeline" linenums="1" hl_lines="13 18 20 21"
        def pipeline(inputs, p, forward=True):
            """The update unit of part d clock by clock, as the RTL. inputs[c] is the address
            entering at clock c (None: none). Stage 1 hashes, stage 2 splits the hash and reads
            the register, stage 3 writes the max. Returns the registers."""
            width = 64 - p
            regs = [0] * (1 << p)
            h1 = s2 = wr = None             # stage 1's hash, stage 2's (j, r, q), last clock's write
            for c in range(len(inputs) + 2):
                a = inputs[c] if c < len(inputs) else None
                new_wr = None
                if s2 is not None:                                       # stage 3
                    j, r, q = s2
                    old = wr[1] if forward and wr is not None and wr[0] == j else q   # (1)!
                    new_wr = (j, max(old, r))
                new_s2 = None
                if h1 is not None:                                       # stage 2
                    j = h1 >> width
                    new_s2 = (j, rank(h1 & ((1 << width) - 1), width), regs[j])     # (2)!
                if new_wr is not None:
                    regs[new_wr[0]] = new_wr[1]                          # the write at the clock edge
                h1, s2, wr = (None if a is None else mix64(a)), new_s2, new_wr   # (3)!
            return regs
        ```

        1. הקידום : אם בשעון הקודם נכתב אותו רגיסטר, הערך שנכתב חדש יותר ממה שנקרא.
        2. הקריאה לפני הכתיבה של אותו שעון : זה מה שקורה ב-RAM עם קריאה סינכרונית, כשהקריאה והכתיבה
           לאותה כתובת באותה עליית שעון.
        3. כל השלבים מתעדכנים יחד בסוף השעון, כמו רגיסטרים בחומרה.

    === "SystemVerilog"
        ```systemverilog title="module hll_update" linenums="1" hl_lines="22 23 38 41 42"
        // The register update of HyperLogLog, one address a clock, in three stages: 1 hashes,
        // 2 splits the hash, counts and reads the register, 3 writes the max back. The registers
        // are a RAM with a synchronous read; the software reads them on rd_idx / rd_val
        module hll_update #(parameter int P = 10, parameter bit FORWARD = 1)   // (1)!
          (input  logic         clk, rst_n,
           input  logic         in_valid,
           input  logic [63:0]  in_addr,
           input  logic [P-1:0] rd_idx,
           output logic [5:0]   rd_val,
           output logic         busy);          // clearing the registers after reset, one a clock

          localparam int M = 1 << P;
          logic [5:0]   regs [M];
          logic [P:0]   clr;                    // the register being cleared; M: done
          logic         v1, v2, wv;             // stages 1 and 2 hold an address; a write last clock
          logic [63:0]  h1;                     // stage 1: the hash
          logic [P-1:0] j2, wj;                 // stage 2: the register, its rank and its value as
          logic [5:0]   r2, q2, wq;             // read; wj, wq: the write of the last clock
          logic [5:0]   old, nv;

          assign busy = !clr[P];
          assign old  = FORWARD && wv && wj == j2 ? wq : q2;
          assign nv   = r2 > old ? r2 : old;

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin
              clr <= '0;
              {v1, v2, wv} <= '0;
            end else begin
              if (busy) clr <= clr + 1'b1;
              {v1, v2, wv} <= {in_valid && !busy, v1, v2};
            end

          always_ff @(posedge clk) begin
            h1 <= mix64(in_addr);                                 // stage 1
            j2 <= h1[63 -: P];                                    // stage 2
            r2 <= 6'(rank(h1, 64 - P));
            q2 <= regs[h1[63 -: P]];                              // (2)!
            wj <= j2;                                             // stage 3
            wq <= nv;
            if (busy) regs[clr[P-1:0]] <= '0;
            else if (v2) regs[j2] <= nv;
          end

          assign rd_val = regs[rd_idx];
        endmodule
        ```

        1. ‏`FORWARD = 0` היא היחידה של המלכודת, בלי הקידום. היא נשארת בקוד כדי שהבודק יראה שהוא
           תופס אותה : מוטציה שהבודק לא תופס היא בודק חלש.
        2. הקריאה הסינכרונית : q2 מקבל את <span dir="ltr">regs[j]</span> כמו שהיה לפני עליית השעון,
           גם כשבאותה עלייה נכתב אותו רגיסטר בשורה 42.

    #### למה זה נכון { .sol-proof }

    **אותם עדכונים, באותו סדר.** הכתובות עוברות את השלבים לפי הסדר, ולכן העדכונים של כל רגיסטר
    נכתבים בשלב 3 בסדר שבו הכתובות נכנסו. מספיק להראות שכל עדכון מתחיל מהערך של הרגיסטר אחרי כל
    העדכונים שלפניו. עדכון שנמצא בשלב 3 בשעון \( t \) קרא בסוף שעון \( t - 1 \). הוא ראה כל כתיבה עד
    סוף שעון \( t - 2 \), וחסרה לו רק הכתיבה של סוף שעון \( t - 1 \), של העדכון שהיה בשלב 3 בשעון
    הקודם. בדיוק את הכתיבה הזו מביא הקידום, כשהיא לאותו רגיסטר. לכן הרגיסטרים בסוף הם בדיוק אלה של
    סעיף ג, והאומדן שהתוכנה מחשבת מהם זהה.

    **האימות של הרגיסטרים.** בהינתן ה-hash, היחידה דטרמיניסטית לגמרי, ולכן אין סיבה להשוות אותה
    לאומדן. הבודק מזין את אותן כתובות ליחידה ולמחלקה hll של סעיף ג, ובסוף קורא את כל הרגיסטרים
    ומשווה אותם ביט אחרי ביט. כתובות אקראיות כמעט לא נופלות באותו רגיסטר שעון אחרי שעון, ולכן
    הבודק מוסיף זרמים מכוונים : שתי כתובות של אותו רגיסטר, הגבוהה קודם, במרחק של 1, 2, 3 ו-4 שעונים,
    עם חורים או עם כתובות של רגיסטרים אחרים ביניהן, ושרשראות של שלוש. מוני כיסוי בודקים שהיה מרחק 1
    שבו הקידום שינה את התוצאה, ומרחקים 2 ו-3. אותו בודק מריץ גם את `FORWARD = 0`, וחייב להיכשל.

    **האימות של האומדן.** את האומדן אסור להשוות למספר האמיתי בטולרנס הדוק בריצה אחת : בטבלה של סעיף ג
    ריצה תקינה לגמרי נותנת 6.8%. בודקים אותו סטטיסטית, על הרבה ריצות עם זרעים קבועים : שהשגיאה
    הריבועית הממוצעת קרובה ל-\( 1.04 / \sqrt{m} \), ושמספר הריצות מחוץ לשתי סטיות תקן קרוב ל-5%. כך
    בנויות הבדיקות של העמוד הזה.

    #### סיבוכיות { .sol-cost }

    **קצב והשהיה.** כתובת בכל שעון, והרגיסטר שלה מעודכן שלושה שעונים אחרי שנכנסה. ה-mix64 הוא שני
    כפלים של 64 ביטים. בשבב אמיתי הם מתפרסים על כמה שלבים לפני שלב 2, אבל זה לא משנה את הסכנה : היא
    רק בין הקריאה לכתיבה.

    **זיכרון.** ‏\( 2^P \) רגיסטרים של 6 ביטים, ועוד רגיסטרים לשלושה שלבים, לכתיבה האחרונה ולמונה
    הניקוי. עם \( P = 10 \) זה RAM של 768 בתים.

    **קריאה של RAM שלוקחת יותר.** אם הקריאה לוקחת שני שעונים, יש שתי כתיבות שהקריאה לא ראתה, וצריך
    לקדם משתיהן, את החדשה קודם. אפשרות אחרת היא לעצור את הצנרת כששתי כתובות לאותו רגיסטר קרובות מדי,
    במחיר של קצב.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : hash חלש"
    הכתובת עצמה כ-hash : ‏\( p \) הביטים העליונים של כתובות רציפות זהים, וכולן נופלות לרגיסטר אחד.
    בתיבה, 20,000 כתובות רציפות עם hash שהוא הכתובת נותנות אומדן של 1. גם hash שמערבב רק את הביטים
    התחתונים נכשל כך. ה-hash צריך שכל ביט של הכתובת ישפיע על כל ביטי התוצאה, כמו ה-mix64.

??? trap "מלכודת : ממוצע רגיל"
    ממוצע רגיל של \( 2^{R_j} \) הולך אחרי הרגיסטר הגבוה ביותר, ורגיסטר אחד שראה hash עם 20 אפסים
    מספיק כדי לנפח את האומדן פי מאות. עם 1,024 רגיסטרים השגיאה שלו היא 2,729%, ושל הממוצע
    ההרמוני 2.92%.

??? trap "מלכודת : בלי תיקון לטווח הקטן"
    בלי אף כתובת הנוסחה ההרמונית נותנת \( \alpha_m m \), ועל 100 כתובות שונות עם 1,024 רגיסטרים היא
    נותנת 784. כשהאומדן עד \( 2.5m \) ויש רגיסטרים ריקים, הספירה הליניארית \( m \ln(m/V) \) נותנת
    98.6.

??? trap "מלכודת : קריאה, שינוי וכתיבה בצנרת"
    שתי כתובות רצופות לאותו רגיסטר : השנייה קוראת לפני שהראשונה כתבה, ודורסת אותה. ברוב הזמן
    זה לא קורה, ולכן בדיקות אקראיות עם הרבה רגיסטרים כמעט לא רואות את זה. צריך קידום או עצירה,
    ובדיקה מכוונת לכל מרחק.

??? trap "מלכודת : אותם ביטים לרגיסטר ולדרגה"
    אם הדרגה נספרת על כל ה-hash, כולל \( p \) הביטים שבחרו את הרגיסטר, רגיסטר שהביט העליון שלו 1
    מקבל תמיד דרגה 1, ורק רגיסטר 0 יכול לראות דרגה של יותר מ-\( p \). הרגיסטרים כבר לא בלתי תלויים
    בבחירה, והאומדן יוצא נמוך בהרבה. בתיבה, "אותם ביטים" על 20,000 כתובות נותן 552 עם 256 רגיסטרים.

??? trap "מלכודת : להשוות אומדן לאמת בריצה אחת"
    בדיקה ש-\( |E - n| / n < 3\% \) בכל ריצה תיכשל בכשליש מהריצות, גם כשהכל תקין. בודקים את הרגיסטרים
    מול מודל ייחוס בדיוק, ואת האומדן סטטיסטית על הרבה ריצות.

??? followup "שאלות המשך"
    - **הרבה מוניטורים ורגרסיה :** כמה כתובות שונות נגעה כל הרגרסיה, על פני מאות בדיקות?

        ??? fu-answer "תשובה"
            כל בדיקה שומרת את 768 הבתים של הרגיסטרים שלה, והאיחוד הוא המקסימום של כל רגיסטר על כל
            הבדיקות. זה מדויק כמו מוניטור אחד שראה את כל הרגרסיה. החיתוך של שתיים יוצא מהכלה והדחה,
            ‏\( |A| + |B| - |A \cup B| \), אבל רועש הרבה יותר.

    - **‏Bloom filter או ספירה ליניארית :** למה לא אחד מהם לבד?

        ??? fu-answer "תשובה"
            ‏Bloom filter עונה אם כתובת כבר הופיעה, ולכן סופר, אבל צריך כ-9.6 ביטים לכל כתובת
            ל-1% טעויות : מיליון כתובות הן כ-1.2 MB. ספירה ליניארית לבד, מפת ביטים של \( m \) ביטים,
            מדויקת רק כל עוד \( n \) לא גדול בהרבה מ-\( m \) : למיליון כתובות בשגיאה של 3.25% היא צריכה
            כ-109 אלף ביטים, כ-13.6 KB, ועם מספר גדול בהרבה ממה שתוכננה לו היא מתמלאת ולא סופרת.

    - **‏hash של 32 ביטים :** מה משתנה?

        ??? fu-answer "תשובה"
            כשהמספר מתקרב ל-\( 2^{32} \), ערכי hash של כתובות שונות מתנגשים, והאומדן נמוך מדי. המאמר
            המקורי מתקן מעל \( 2^{32}/30 \) ל-\( -2^{32} \ln(1 - E/2^{32}) \). עם 64 ביטים אין צורך,
            ו-6 ביטים לרגיסטר עדיין מספיקים.

    - **מחיקה :** אפשר להוציא כתובת מהספירה?

        ??? fu-answer "תשובה"
            לא. המקסימום לא זוכר מי הביא אותו, והרגיסטר לא יודע אם כתובת אחרת הייתה מביאה את אותה
            דרגה. מחלונות זמן משתמשים בכמה מערכים לפי זמן, או ברגיסטרים ששומרים גם מתי הדרגה נראתה.
