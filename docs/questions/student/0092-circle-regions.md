---
id: 92
title: נקודות על מעגל – לכמה חלקים מתחלק העיגול
level: student
difficulty: medium
kind: math
tags: [geometry, combinatorics, proof, logic-puzzles, python, systemverilog]
source: "בעיית העיגול של Moser, הדוגמה הקלאסית לדפוס שנשבר"
added: 2026-11-06
---

## השאלה

שמים \( n \) נקודות על מעגל, ומחברים כל זוג נקודות בקו ישר (מיתר). הקווים חותכים את
העיגול לחלקים. לכמה חלקים מתחלק העיגול? מניחים שהנקודות **במצב כללי** : אין שלושה קווים
שעוברים באותה נקודה בתוך העיגול.

עם נקודה אחת, שתיים, שלוש וארבע מקבלים 1, 2, 4 ו-8 חלקים :

<!-- gen 0 -->

<svg class="figure mc-fig mc-row" viewBox="0 0 518 146" style="max-width:32.4rem" role="img" aria-label="עיגולים עם נקודה אחת, שתיים, שלוש וארבע, וכל זוג נקודות מחובר בקו. מספר החלקים : 1, 2, 4 ו-8"><g transform="translate(402,0)"><path class="mc-reg mc-c0" d="M58.0,12.0A46,46 0 0 0 58.0,104.0A46,46 0 0 0 58.0,12.0Z"/><circle class="mc-ring" cx="58" cy="58" r="46"/><circle class="mc-pt" cx="58.0" cy="12.0" r="5.5"/></g><text class="mc-count" x="460.0" y="140" text-anchor="middle">n = 1 : 1</text><g transform="translate(268,0)"><path class="mc-reg mc-c0" d="M58.0,104.0A46,46 0 0 0 58.0,12.0L58.0,104.0Z"/><path class="mc-reg mc-c1" d="M58.0,12.0A46,46 0 0 0 58.0,104.0L58.0,12.0Z"/><circle class="mc-ring" cx="58" cy="58" r="46"/><line class="mc-chord" x1="58.0" y1="12.0" x2="58.0" y2="104.0"/><circle class="mc-pt" cx="58.0" cy="12.0" r="5.5"/><circle class="mc-pt" cx="58.0" cy="104.0" r="5.5"/></g><text class="mc-count" x="326.0" y="140" text-anchor="middle">n = 2 : 2</text><g transform="translate(134,0)"><path class="mc-reg mc-c0" d="M58.0,12.0L18.2,81.0L97.8,81.0L58.0,12.0Z"/><path class="mc-reg mc-c1" d="M97.8,81.0A46,46 0 0 0 58.0,12.0L97.8,81.0Z"/><path class="mc-reg mc-c2" d="M18.2,81.0A46,46 0 0 0 97.8,81.0L18.2,81.0Z"/><path class="mc-reg mc-c3" d="M58.0,12.0A46,46 0 0 0 18.2,81.0L58.0,12.0Z"/><circle class="mc-ring" cx="58" cy="58" r="46"/><line class="mc-chord" x1="58.0" y1="12.0" x2="18.2" y2="81.0"/><line class="mc-chord" x1="58.0" y1="12.0" x2="97.8" y2="81.0"/><line class="mc-chord" x1="18.2" y1="81.0" x2="97.8" y2="81.0"/><circle class="mc-pt" cx="58.0" cy="12.0" r="5.5"/><circle class="mc-pt" cx="18.2" cy="81.0" r="5.5"/><circle class="mc-pt" cx="97.8" cy="81.0" r="5.5"/></g><text class="mc-count" x="192.0" y="140" text-anchor="middle">n = 3 : 4</text><g transform="translate(0,0)"><path class="mc-reg mc-c0" d="M81.0,18.2L58.0,58.0L97.8,81.0L81.0,18.2Z"/><path class="mc-reg mc-c1" d="M58.0,58.0L35.0,97.8L97.8,81.0L58.0,58.0Z"/><path class="mc-reg mc-c2" d="M35.0,97.8L58.0,58.0L18.2,35.0L35.0,97.8Z"/><path class="mc-reg mc-c3" d="M81.0,18.2L18.2,35.0L58.0,58.0L81.0,18.2Z"/><path class="mc-reg mc-c4" d="M97.8,81.0A46,46 0 0 0 81.0,18.2L97.8,81.0Z"/><path class="mc-reg mc-c5" d="M35.0,97.8A46,46 0 0 0 97.8,81.0L35.0,97.8Z"/><path class="mc-reg mc-c0" d="M18.2,35.0A46,46 0 0 0 35.0,97.8L18.2,35.0Z"/><path class="mc-reg mc-c1" d="M81.0,18.2A46,46 0 0 0 18.2,35.0L81.0,18.2Z"/><circle class="mc-ring" cx="58" cy="58" r="46"/><line class="mc-chord" x1="81.0" y1="18.2" x2="18.2" y2="35.0"/><line class="mc-chord" x1="81.0" y1="18.2" x2="35.0" y2="97.8"/><line class="mc-chord" x1="81.0" y1="18.2" x2="97.8" y2="81.0"/><line class="mc-chord" x1="18.2" y1="35.0" x2="35.0" y2="97.8"/><line class="mc-chord" x1="18.2" y1="35.0" x2="97.8" y2="81.0"/><line class="mc-chord" x1="35.0" y1="97.8" x2="97.8" y2="81.0"/><circle class="mc-pt" cx="81.0" cy="18.2" r="5.5"/><circle class="mc-pt" cx="18.2" cy="35.0" r="5.5"/><circle class="mc-pt" cx="35.0" cy="97.8" r="5.5"/><circle class="mc-pt" cx="97.8" cy="81.0" r="5.5"/></g><text class="mc-count" x="58.0" y="140" text-anchor="middle">n = 4 : 8</text></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="mc-key-pt"></i>נקודה על המעגל</span><span><i class="mc-key-reg"></i>חלק של העיגול, כל חלק בצבע משלו</span></span>

<!-- /gen -->

??? interviewer "מה המראיין בודק"
    - **לא לסמוך על דפוס :** 1, 2, 4, 8 ו-16 מזמינים את הניחוש "חזקות של 2". האם המועמד
      בודק עוד מקרה לפני שהוא מכריז על נוסחה.
    - **ספירה בשני שלבים :** האם הוא מוצא מה כל קו **מוסיף**, במקום לספור חלקים בציור.
    - **מה קובע חיתוך :** שני קווים נחתכים בדיוק כשארבעת הקצוות שלהם מתחלפים לאורך המעגל.
      האם הוא רואה שכל ארבע נקודות נותנות נקודת חיתוך אחת בדיוק.
    - **נוסחת אוילר :** האם הוא יודע לספור קודקודים, צלעות ופאות בגרף מישורי, ולא שוכח
      את הקשתות ואת הפאה החיצונית.
    - **מה ההנחה נותנת :** מה קורה כששלושה קווים כן נפגשים, למשל במשושה משוכלל.

---

### סעיף א – חמש נקודות

1. לכמה חלקים מחלקים העיגול 10 הקווים בין 5 נקודות?
2. מה הנוסחה שהמספרים 1, 2, 4, 8 ו-16 מציעים?
3. כתבו פונקציה שמוסיפה את הקווים אחד אחד, וסופרת כמה חלקים כל קו מוסיף. הנקודות
   ממוספרות לפי הסדר על המעגל.

??? tip "רמז 1"
    מה קורה כשמוסיפים קו חדש? הוא עובר דרך כמה חלקים קיימים, וכל אחד מהם הוא חוצה לשניים.

??? tip "רמז 2"
    קו שחוצה \( k \) קווים קודמים נחתך ל-\( k + 1 \) קטעים, וכל קטע מחלק חלק אחד לשניים.
    ומתי שני קווים נחתכים? הסתכלו על הסדר של ארבעת הקצוות שלהם על המעגל.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **16 חלקים.** קו שחוצה \( k \) קווים קודמים מוסיף \( k + 1 \) חלקים. עם 5 נקודות
        עשרת הקווים מוסיפים 15, ועם החלק ההתחלתי יש 16. המספרים 1, 2, 4, 8 ו-16 מציעים
        \( 2^{n-1} \), אבל זה רק ניחוש, וסעיף ב מראה שהוא נשבר.

    <!-- cost: זמן \( O(n^4) \) | זיכרון \( O(n^2) \) -->

    #### הרעיון { .sol-idea }

    במקום לספור חלקים בציור, **סופרים מה כל קו מוסיף.** מתחילים מעיגול שלם, חלק אחד,
    ומוסיפים את הקווים אחד אחד. קו חדש שחוצה \( k \) קווים קודמים נחתך ב-\( k \) נקודות ל-\( k + 1 \)
    קטעים. כל קטע עובר בתוך חלק אחד וחוצה אותו לשניים, ולכן הקו מוסיף בדיוק \( k + 1 \)
    חלקים.

    **מתי שני קווים נחתכים.** הקו בין הנקודות \( a \) ו-\( b \) מחלק את המעגל לשתי קשתות.
    הקו בין \( c \) ל-\( d \) חותך אותו בתוך העיגול בדיוק כש-\( c \) ו-\( d \) נמצאות על קשתות
    **שונות**, כלומר כשארבעת הקצוות מתחלפים לאורך המעגל. עם מספור לפי הסדר על המעגל
    ו-\( a < b \), זה אומר שבדיוק אחד מ-\( c \) ו-\( d \) נמצא בין \( a \) ל-\( b \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מספור :** הנקודות 1 עד \( n \) לפי הסדר על המעגל.
    2. **קו אחר קו :** לכל קו, סופרים כמה מהקווים שכבר צוירו הוא חוצה, בבדיקת ההתחלפות.
    3. **חיבור :** מתחילים מ-1, ומוסיפים \( k + 1 \) לכל קו.
    4. **חמש נקודות :** הקווים מוסיפים 15, ויוצא 16.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="regions_by_chords" linenums="1" hl_lines="5 15"
        def crosses(a, b, c, d):
            """Points numbered in order around the circle, a < b and c < d: do the chords
            (a, b) and (c, d) cross inside the disc? Exactly when one end of the second chord
            lies strictly between a and b and the other does not."""
            return len({a, b, c, d}) == 4 and (a < c < b) != (a < d < b)   # (1)!


        def regions_by_chords(n):
            """The regions of the disc, adding the chords one at a time: a chord that crosses
            k chords drawn before it is cut into k + 1 pieces, and each piece splits a region."""
            drawn, regions = [], 1
            for a in range(n):
                for b in range(a + 1, n):
                    k = sum(crosses(a, b, c, d) for c, d in drawn)
                    regions += k + 1                                       # (2)!
                    drawn.append((a, b))
            return regions
        ```

        1. שני הקצוות של הקו השני על אותה קשת (שניהם בין \( a \) ל-\( b \), או שניהם מחוץ)
           פירושם שהוא לא חוצה. קו שחולק קצה עם הראשון נפגש איתו רק על המעגל, ולא נספר.
        2. נקודות החיתוך, \( k \) במספר, חותכות את הקו ל-\( k + 1 \) קטעים, וכל קטע מוסיף חלק.

    === "SystemVerilog"
        ```systemverilog title="function automatic int regions_by_chords" linenums="1" hl_lines="5 17"
        // Points numbered in order around the circle, a < b and c < d: do the chords (a, b)
        // and (c, d) cross inside the disc?
        function automatic bit crosses(int a, int b, int c, int d);
          bit c_in = (a < c) && (c < b), d_in = (a < d) && (d < b);
          return (a != c) && (a != d) && (b != c) && (b != d) && (c_in != d_in);   // (1)!
        endfunction

        // The regions of the disc, adding the chords (a, b), a < b, one at a time.
        function automatic int regions_by_chords(int n);
          int da[$], db[$];                          // the chords drawn so far
          int regions = 1, k;
          for (int a = 0; a < n; a++)
            for (int b = a + 1; b < n; b++) begin
              k = 0;
              foreach (da[i]) if (crosses(a, b, da[i], db[i])) k++;
              da.push_back(a); db.push_back(b);
              regions += k + 1;                      // (2)!
            end
          return regions;
        endfunction
        ```

        1. אותו תנאי כמו ב-Python : ארבעה קצוות שונים, ובדיוק אחד מקצות הקו השני בין
           \( a \) ל-\( b \).
        2. ‏\( k \) חיתוכים, \( k + 1 \) קטעים, \( k + 1 \) חלקים חדשים.

    #### למה זה נכון { .sol-proof }

    **כל קו מוסיף \( k + 1 \).** במצב כללי, \( k \) נקודות החיתוך של הקו החדש עם הקווים
    הקודמים שונות זו מזו, ואף אחת מהן אינה נקודת חיתוך ישנה (אחרת שלושה קווים היו נפגשים
    בה). לכן הן מחלקות את הקו ל-\( k + 1 \) קטעים, וכל קטע עובר מצד לצד של חלק קיים אחד,
    בלי לפגוש קו אחר בדרך, ומחלק אותו לשני חלקים. החלקים שהקו לא עובר בהם לא משתנים.

    **חמש נקודות.** בציור, חמש נקודות במצולע משוכלל (במחומש אין שלושה קווים שנפגשים
    בנקודה אחת), וכל אחד מ-16 החלקים ממוספר :

    <!-- gen 2 -->

    <svg class="figure mc-fig" viewBox="0 0 272 272" style="max-width:17.0rem" role="img" aria-label="חמש נקודות על מעגל וכל עשרת הקווים ביניהן. העיגול מתחלק ל-16 חלקים, ממוספרים 1 עד 16 : מחומש באמצע, חמישה משולשים סביבו, עוד חמישה ליד הצלעות, וחמש קשתות"><path class="mc-reg mc-c0" d="M111.3,102.0L96.0,149.0L136.0,178.0L176.0,149.0L160.7,102.0L111.3,102.0Z"/><path class="mc-reg mc-c1" d="M136.0,26.0L111.3,102.0L160.7,102.0L136.0,26.0Z"/><path class="mc-reg mc-c2" d="M160.7,102.0L176.0,149.0L240.6,102.0L160.7,102.0Z"/><path class="mc-reg mc-c3" d="M200.7,225.0L176.0,149.0L136.0,178.0L200.7,225.0Z"/><path class="mc-reg mc-c4" d="M96.0,149.0L71.3,225.0L136.0,178.0L96.0,149.0Z"/><path class="mc-reg mc-c5" d="M96.0,149.0L111.3,102.0L31.4,102.0L96.0,149.0Z"/><path class="mc-reg mc-c0" d="M136.0,26.0L160.7,102.0L240.6,102.0L136.0,26.0Z"/><path class="mc-reg mc-c1" d="M176.0,149.0L200.7,225.0L240.6,102.0L176.0,149.0Z"/><path class="mc-reg mc-c2" d="M200.7,225.0L136.0,178.0L71.3,225.0L200.7,225.0Z"/><path class="mc-reg mc-c3" d="M71.3,225.0L96.0,149.0L31.4,102.0L71.3,225.0Z"/><path class="mc-reg mc-c4" d="M136.0,26.0L31.4,102.0L111.3,102.0L136.0,26.0Z"/><path class="mc-reg mc-c5" d="M240.6,102.0A110,110 0 0 0 136.0,26.0L240.6,102.0Z"/><path class="mc-reg mc-c0" d="M200.7,225.0A110,110 0 0 0 240.6,102.0L200.7,225.0Z"/><path class="mc-reg mc-c1" d="M71.3,225.0A110,110 0 0 0 200.7,225.0L71.3,225.0Z"/><path class="mc-reg mc-c2" d="M31.4,102.0A110,110 0 0 0 71.3,225.0L31.4,102.0Z"/><path class="mc-reg mc-c3" d="M136.0,26.0A110,110 0 0 0 31.4,102.0L136.0,26.0Z"/><circle class="mc-ring" cx="136" cy="136" r="110"/><line class="mc-chord" x1="136.0" y1="26.0" x2="31.4" y2="102.0"/><line class="mc-chord" x1="136.0" y1="26.0" x2="71.3" y2="225.0"/><line class="mc-chord" x1="136.0" y1="26.0" x2="200.7" y2="225.0"/><line class="mc-chord" x1="136.0" y1="26.0" x2="240.6" y2="102.0"/><line class="mc-chord" x1="31.4" y1="102.0" x2="71.3" y2="225.0"/><line class="mc-chord" x1="31.4" y1="102.0" x2="200.7" y2="225.0"/><line class="mc-chord" x1="31.4" y1="102.0" x2="240.6" y2="102.0"/><line class="mc-chord" x1="71.3" y1="225.0" x2="200.7" y2="225.0"/><line class="mc-chord" x1="71.3" y1="225.0" x2="240.6" y2="102.0"/><line class="mc-chord" x1="200.7" y1="225.0" x2="240.6" y2="102.0"/><text class="mc-num" x="136.0" y="140.0" text-anchor="middle">1</text><text class="mc-num" x="136.0" y="80.7" text-anchor="middle">2</text><text class="mc-num" x="192.4" y="121.7" text-anchor="middle">3</text><text class="mc-num" x="170.9" y="188.0" text-anchor="middle">4</text><text class="mc-num" x="101.1" y="188.0" text-anchor="middle">5</text><text class="mc-num" x="79.6" y="121.7" text-anchor="middle">6</text><text class="mc-num" x="179.1" y="80.7" text-anchor="middle">7</text><text class="mc-num" x="205.7" y="162.7" text-anchor="middle">8</text><text class="mc-num" x="136.0" y="213.3" text-anchor="middle">9</text><text class="mc-num" x="66.3" y="162.7" text-anchor="middle">10</text><text class="mc-num" x="92.9" y="80.7" text-anchor="middle">11</text><text class="mc-num" x="195.9" y="57.5" text-anchor="middle">12</text><text class="mc-num" x="233.0" y="171.5" text-anchor="middle">13</text><text class="mc-num" x="136.0" y="242.0" text-anchor="middle">14</text><text class="mc-num" x="39.0" y="171.5" text-anchor="middle">15</text><text class="mc-num" x="76.1" y="57.5" text-anchor="middle">16</text><circle class="mc-pt" cx="136.0" cy="26.0" r="5.5"/><text class="mc-plab" x="136.0" y="15.0" text-anchor="middle">1</text><circle class="mc-pt" cx="31.4" cy="102.0" r="5.5"/><text class="mc-plab" x="17.1" y="101.4" text-anchor="middle">2</text><circle class="mc-pt" cx="71.3" cy="225.0" r="5.5"/><text class="mc-plab" x="62.5" y="241.1" text-anchor="middle">3</text><circle class="mc-pt" cx="200.7" cy="225.0" r="5.5"/><text class="mc-plab" x="209.5" y="241.1" text-anchor="middle">4</text><circle class="mc-pt" cx="240.6" cy="102.0" r="5.5"/><text class="mc-plab" x="254.9" y="101.4" text-anchor="middle">5</text></svg>

    <!-- /gen -->

    **קו אחר קו.** הקווים לפי הסדר, כמה קווים קודמים כל אחד חוצה, וכמה חלקים הוא מוסיף :

    <!-- gen 3 -->

    | הקו | חוצה קווים קודמים | חלקים שהוא מוסיף | חלקים אחריו |
    |:-:|:-:|:-:|:-:|
    | 1 ו-2 | 0 | 1 | 2 |
    | 1 ו-3 | 0 | 1 | 3 |
    | 1 ו-4 | 0 | 1 | 4 |
    | 1 ו-5 | 0 | 1 | 5 |
    | 2 ו-3 | 0 | 1 | 6 |
    | 2 ו-4 | 1 | 2 | 8 |
    | 2 ו-5 | 2 | 3 | 11 |
    | 3 ו-4 | 0 | 1 | 12 |
    | 3 ו-5 | 2 | 3 | 15 |
    | 4 ו-5 | 0 | 1 | 16 |

    <!-- /gen -->

    **נסו בעצמכם.** לחצו "הקו הבא" עד הקו בין 2 ל-5 : הוא פוגש שני קווים, מוסיף 3, ויש 11
    חלקים, כמו בשורה שלו בטבלה. עברו ל-6 נקודות : הקו בין 3 ל-6 פוגש ארבעה קווים ומוסיף 5,
    ובסוף יש 31 חלקים, לא 32. ועם 5 נקודות, גררו את נקודה 3 אל בין נקודות 4 ו-5 : עכשיו
    חלק מהקווים מוסיפים מספר אחר, אבל אחרי כל הקווים יש שוב 16. על הטבלה התיבה מוסיפה כל מספר של נקודות וכל
    מיקום שלהן :

    <div class="explorer" data-kind="circlecut" data-n="5" data-angles="90 162 234 306 18" data-show="steps"></div>

    #### סיבוכיות { .sol-cost }

    יש \( \binom{n}{2} \) קווים, וכל אחד נבדק מול כל הקווים שלפניו : \( O(n^4) \) בדיקות
    של זמן קבוע. הזיכרון הוא רשימת הקווים, \( O(n^2) \). סעיף ב נותן נוסחה בזמן קבוע.

---

### סעיף ב – שש נקודות והנוסחה הכללית

1. לכמה חלקים מתחלק העיגול עם 6 נקודות? האם הניחוש של סעיף א עומד?
2. הוכיחו שעם \( n \) נקודות במצב כללי מספר החלקים הוא
   \( \binom{n}{4} + \binom{n}{2} + 1 \). תנו שתי הוכחות : אחת בספירת הקווים של סעיף א,
   ואחת בנוסחת אוילר לגרפים מישוריים.
3. כתבו את הנוסחה כפונקציה.

??? tip "רמז 1"
    לפי סעיף א, כל קו מוסיף \( k + 1 \). סכמו את זה על כל הקווים. מה סופר הסכום של
    ה-\( k \)?

??? tip "רמז 2"
    כמה נקודות על המעגל קובעות נקודת חיתוך אחת? ולהפך, כמה נקודות חיתוך קובעות ארבע
    נקודות על המעגל?

??? tip "רמז 3"
    לנוסחת אוילר, \( V - E + F = 2 \) : הקודקודים הם הנקודות על המעגל ונקודות החיתוך. הצלעות
    הן הקשתות של המעגל והקטעים של הקווים. אל תשכחו שאחת הפאות היא מחוץ לעיגול.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **31 חלקים, לא 32.** הדפוס של חזקות 2 נשבר כבר ב-6. באופן כללי מספר החלקים הוא
        \( \binom{n}{4} + \binom{n}{2} + 1 \) : 1 לעיגול, 1 לכל קו ו-1 לכל נקודת חיתוך, וכל
        ארבע נקודות על המעגל קובעות נקודת חיתוך אחת בדיוק. נוסחת אוילר נותנת את אותו
        מספר.

    <!-- cost: זמן \( O(1) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    לפי סעיף א, החלקים הם 1, ועוד 1 לכל קו, ועוד 1 לכל נקודת חיתוך. וכל ארבע נקודות על
    המעגל קובעות נקודת חיתוך אחת בדיוק, של שני האלכסונים של המרובע שהן יוצרות, ולכן יש
    \( \binom{n}{2} \) קווים ו-\( \binom{n}{4} \) נקודות חיתוך.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שש נקודות :** \( \binom{6}{4} + \binom{6}{2} + 1 = 15 + 15 + 1 = 31 \).
    2. **הוכחה ראשונה :** 1 ועוד \( k + 1 \) לכל קו, וכל ארבע נקודות נותנות חיתוך אחד.
    3. **הוכחה שנייה :** אוילר על הגרף של הנקודות, החיתוכים, הקשתות והקטעים.
    4. **הקוד :** נוסחה בשורה אחת, ובדיקה שהספירה של אוילר נותנת אותו מספר.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="regions" linenums="1" hl_lines="7 15"
        from math import comb


        def regions(n):
            """The regions of the disc cut by all the chords between n points on a circle, no
            three chords through one point inside."""
            return comb(n, 4) + comb(n, 2) + 1          # (1)!


        def euler_regions(n):
            """The same count by Euler's formula V - E + F = 2 on the planar graph of the
            points, the crossings, the arcs and the pieces of the chords."""
            V = n + comb(n, 4)                          # n points and one crossing per 4 points
            E = n + comb(n, 2) + 2 * comb(n, 4)         # n arcs; every crossing cuts 2 chords
            return E - V + 1                            # (2)!
        ```

        1. 1 לעיגול השלם, 1 לכל אחד מ-\( \binom{n}{2} \) הקווים, ו-1 לכל אחת מ-\( \binom{n}{4} \)
           נקודות החיתוך.
        2. אוילר נותן \( F = E - V + 2 \) פאות, ואחת מהן היא מחוץ לעיגול. לכן החלקים הם
           \( E - V + 1 \).

    === "SystemVerilog"
        ```systemverilog title="function automatic longint regions" linenums="1" hl_lines="11 18"
        // C(n, k) without overflow for the sizes here: multiply and divide in turn.
        function automatic longint comb(int n, int k);
          longint r = 1;
          if (k < 0 || k > n) return 0;
          for (int i = 0; i < k; i++) r = r * (n - i) / (i + 1);
          return r;
        endfunction

        // The regions of the disc, n points in general position.
        function automatic longint regions(int n);
          return comb(n, 4) + comb(n, 2) + 1;               // (1)!
        endfunction

        // The same by Euler: V - E + F = 2, one face outside the disc.
        function automatic longint euler_regions(int n);
          longint v = n + comb(n, 4);
          longint e = n + comb(n, 2) + 2 * comb(n, 4);
          return e - v + 1;                                 // (2)!
        endfunction
        ```

        1. המכפלה \( r \cdot (n - i) \) מתחלקת תמיד ב-\( i + 1 \), כי אחרי \( i + 1 \) צעדים
           \( r \) הוא \( \binom{n}{i+1} \). לכן החילוק השלם מדויק.
        2. אותו חשבון כמו ב-Python : הפאות של אוילר בלי הפאה החיצונית.

    #### למה זה נכון { .sol-proof }

    **שש נקודות.** בציור, שש נקודות במצב כללי : 15 קווים, 15 נקודות חיתוך, ו-31 חלקים :

    <!-- gen 4 -->

    <svg class="figure mc-fig" viewBox="0 0 272 272" style="max-width:17.0rem" role="img" aria-label="שש נקודות במצב כללי וכל חמישה-עשר הקווים ביניהן. 15 נקודות חיתוך, ו-31 חלקים, לא 32"><path class="mc-reg mc-c0" d="M141.3,148.4L142.2,123.0L119.6,134.8L141.3,148.4Z"/><path class="mc-reg mc-c1" d="M142.2,123.0L141.3,148.4L178.4,171.5L196.5,138.1L180.5,103.1L142.2,123.0Z"/><path class="mc-reg mc-c2" d="M139.8,191.0L141.3,148.4L119.6,134.8L81.8,154.5L101.5,186.6L139.8,191.0Z"/><path class="mc-reg mc-c3" d="M105.2,82.0L83.3,112.1L119.6,134.8L142.2,123.0L143.7,80.7L105.2,82.0Z"/><path class="mc-reg mc-c4" d="M141.3,148.4L139.8,191.0L166.2,194.0L178.4,171.5L141.3,148.4Z"/><path class="mc-reg mc-c5" d="M143.7,80.7L142.2,123.0L180.5,103.1L169.9,79.8L143.7,80.7Z"/><path class="mc-reg mc-c0" d="M83.3,112.1L68.4,132.6L81.8,154.5L119.6,134.8L83.3,112.1Z"/><path class="mc-reg mc-c2" d="M180.5,103.1L196.5,138.1L229.3,77.7L180.5,103.1Z"/><path class="mc-reg mc-c2" d="M225.0,200.7L196.5,138.1L178.4,171.5L225.0,200.7Z"/><path class="mc-reg mc-c3" d="M137.9,246.0L139.8,191.0L101.5,186.6L137.9,246.0Z"/><path class="mc-reg mc-c4" d="M145.6,26.4L105.2,82.0L143.7,80.7L145.6,26.4Z"/><path class="mc-reg mc-c5" d="M101.5,186.6L81.8,154.5L34.7,179.0L101.5,186.6Z"/><path class="mc-reg mc-c0" d="M83.3,112.1L105.2,82.0L38.9,84.4L83.3,112.1Z"/><path class="mc-reg mc-c1" d="M139.8,191.0L137.9,246.0L166.2,194.0L139.8,191.0Z"/><path class="mc-reg mc-c3" d="M225.0,200.7L178.4,171.5L166.2,194.0L225.0,200.7Z"/><path class="mc-reg mc-c3" d="M169.9,79.8L180.5,103.1L229.3,77.7L169.9,79.8Z"/><path class="mc-reg mc-c0" d="M145.6,26.4L143.7,80.7L169.9,79.8L145.6,26.4Z"/><path class="mc-reg mc-c1" d="M68.4,132.6L34.7,179.0L81.8,154.5L68.4,132.6Z"/><path class="mc-reg mc-c1" d="M68.4,132.6L83.3,112.1L38.9,84.4L68.4,132.6Z"/><path class="mc-reg mc-c1" d="M196.5,138.1L225.0,200.7L229.3,77.7L196.5,138.1Z"/><path class="mc-reg mc-c2" d="M137.9,246.0L101.5,186.6L34.7,179.0L137.9,246.0Z"/><path class="mc-reg mc-c3" d="M145.6,26.4L38.9,84.4L105.2,82.0L145.6,26.4Z"/><path class="mc-reg mc-c4" d="M225.0,200.7L166.2,194.0L137.9,246.0L225.0,200.7Z"/><path class="mc-reg mc-c5" d="M145.6,26.4L169.9,79.8L229.3,77.7L145.6,26.4Z"/><path class="mc-reg mc-c0" d="M34.7,179.0L68.4,132.6L38.9,84.4L34.7,179.0Z"/><path class="mc-reg mc-c2" d="M225.0,200.7A110,110 0 0 0 229.3,77.7L225.0,200.7Z"/><path class="mc-reg mc-c3" d="M34.7,179.0A110,110 0 0 0 137.9,246.0L34.7,179.0Z"/><path class="mc-reg mc-c4" d="M145.6,26.4A110,110 0 0 0 38.9,84.4L145.6,26.4Z"/><path class="mc-reg mc-c4" d="M229.3,77.7A110,110 0 0 0 145.6,26.4L229.3,77.7Z"/><path class="mc-reg mc-c5" d="M137.9,246.0A110,110 0 0 0 225.0,200.7L137.9,246.0Z"/><path class="mc-reg mc-c1" d="M38.9,84.4A110,110 0 0 0 34.7,179.0L38.9,84.4Z"/><circle class="mc-ring" cx="136" cy="136" r="110"/><line class="mc-chord" x1="145.6" y1="26.4" x2="38.9" y2="84.4"/><line class="mc-chord" x1="145.6" y1="26.4" x2="34.7" y2="179.0"/><line class="mc-chord" x1="145.6" y1="26.4" x2="137.9" y2="246.0"/><line class="mc-chord" x1="145.6" y1="26.4" x2="225.0" y2="200.7"/><line class="mc-chord" x1="145.6" y1="26.4" x2="229.3" y2="77.7"/><line class="mc-chord" x1="38.9" y1="84.4" x2="34.7" y2="179.0"/><line class="mc-chord" x1="38.9" y1="84.4" x2="137.9" y2="246.0"/><line class="mc-chord" x1="38.9" y1="84.4" x2="225.0" y2="200.7"/><line class="mc-chord" x1="38.9" y1="84.4" x2="229.3" y2="77.7"/><line class="mc-chord" x1="34.7" y1="179.0" x2="137.9" y2="246.0"/><line class="mc-chord" x1="34.7" y1="179.0" x2="225.0" y2="200.7"/><line class="mc-chord" x1="34.7" y1="179.0" x2="229.3" y2="77.7"/><line class="mc-chord" x1="137.9" y1="246.0" x2="225.0" y2="200.7"/><line class="mc-chord" x1="137.9" y1="246.0" x2="229.3" y2="77.7"/><line class="mc-chord" x1="225.0" y1="200.7" x2="229.3" y2="77.7"/><circle class="mc-pt" cx="145.6" cy="26.4" r="5.5"/><text class="mc-plab" x="146.9" y="15.5" text-anchor="middle">1</text><circle class="mc-pt" cx="38.9" cy="84.4" r="5.5"/><text class="mc-plab" x="25.6" y="81.3" text-anchor="middle">2</text><circle class="mc-pt" cx="34.7" cy="179.0" r="5.5"/><text class="mc-plab" x="20.9" y="188.8" text-anchor="middle">3</text><circle class="mc-pt" cx="137.9" cy="246.0" r="5.5"/><text class="mc-plab" x="138.2" y="265.0" text-anchor="middle">4</text><circle class="mc-pt" cx="225.0" cy="200.7" r="5.5"/><text class="mc-plab" x="237.1" y="213.5" text-anchor="middle">5</text><circle class="mc-pt" cx="229.3" cy="77.7" r="5.5"/><text class="mc-plab" x="242.0" y="73.8" text-anchor="middle">6</text></svg>

    <!-- /gen -->

    **הוכחה ראשונה, קו אחר קו.** לפי סעיף א, כל קו מוסיף 1 ועוד מספר הקווים הקודמים
    שהוא חוצה. נסכם על כל הקווים :

    \[
    \begin{aligned}
    \text{regions} &= 1 + \sum_{\text{chords}} (k + 1) \\
                   &= 1 + \binom{n}{2} + \sum_{\text{chords}} k .
    \end{aligned}
    \]

    כל זוג קווים שנחתכים נספר בסכום של ה-\( k \) פעם אחת בדיוק, כשהשני מביניהם מצויר.
    לכן \( \sum k \) הוא מספר נקודות החיתוך, ובמצב כללי כל נקודת חיתוך היא זוג אחד. זוג
    קווים נחתך בדיוק כשיש להם ארבעה קצוות שונים שמתחלפים לאורך המעגל. ולכל ארבע נקודות
    יש בדיוק זיווג אחד כזה מבין שלושת הזיווגים, שני האלכסונים של המרובע. לכן יש
    \( \binom{n}{4} \) נקודות חיתוך, והחלקים הם \( \binom{n}{4} + \binom{n}{2} + 1 \).

    **הוכחה שנייה, נוסחת אוילר.** הגרף המישורי הוא הנקודות על המעגל, נקודות החיתוך,
    הקשתות של המעגל בין נקודות סמוכות, והקטעים של הקווים בין נקודות חיתוך סמוכות. הוא
    קשיר, כי המעגל מחבר את כל הנקודות. ב-\( n = 1 \) הקשת היחידה היא לולאה, וב-\( n = 2 \)
    יש שתי צלעות בין אותן שתי נקודות, ונוסחת אוילר נכונה גם לגרף כזה.

    - **קודקודים :** \( V = n + \binom{n}{4} \), הנקודות ונקודות החיתוך.
    - **צלעות :** \( n \) קשתות. קו שחוצה \( k \) קווים הוא \( k + 1 \) קטעים, והסכום על
      כל הקווים הוא \( \binom{n}{2} + 2\binom{n}{4} \), כי כל נקודת חיתוך נמצאת על שני
      קווים. לכן \( E = n + \binom{n}{2} + 2\binom{n}{4} \).
    - **פאות :** \( F = E - V + 2 \), ואחת מהן היא כל מה שמחוץ לעיגול. לכן

    \[
    \begin{aligned}
    \text{regions} &= E - V + 1 \\
                   &= \binom{n}{2} + \binom{n}{4} + 1 .
    \end{aligned}
    \]

    **הספירה לכל n.** הטבלה סופרת קודקודים וצלעות ל-\( n \) עד 10, ומשווה לחזקות של 2.
    עד 5 הן שוות, ומשם הן נפרדות :

    <!-- gen 5 -->

    | ‏n | נקודות על המעגל | נקודות חיתוך | קודקודים V | צלעות E | חלקים E − V + 1 | 2 בחזקת n − 1 |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | 1 | 1 | 0 | 1 | 1 | 1 | 1 |
    | 2 | 2 | 0 | 2 | 3 | 2 | 2 |
    | 3 | 3 | 0 | 3 | 6 | 4 | 4 |
    | 4 | 4 | 1 | 5 | 12 | 8 | 8 |
    | 5 | 5 | 5 | 10 | 25 | 16 | 16 |
    | 6 | 6 | 15 | 21 | 51 | 31 | 32 |
    | 7 | 7 | 35 | 42 | 98 | 57 | 64 |
    | 8 | 8 | 70 | 78 | 176 | 99 | 128 |
    | 9 | 9 | 126 | 135 | 297 | 163 | 256 |
    | 10 | 10 | 210 | 220 | 475 | 256 | 512 |

    <!-- /gen -->

    <!-- gen 6 -->

    <svg class="perf-chart mc-chart" viewBox="0 0 640 250" role="img" aria-label="מספר החלקים לפי n, מול 2 בחזקת n פחות 1 : עד n = 5 הם שווים, ומ-6 החלקים מפגרים : 31 מול 32, 57 מול 64, 256 מול 512"><line class="grid" x1="46" x2="628" y1="210.0" y2="210.0"/><text class="tick" x="38" y="214.0" text-anchor="end">0</text><line class="grid" x1="46" x2="628" y1="162.2" y2="162.2"/><text class="tick" x="38" y="166.2" text-anchor="end">128</text><line class="grid" x1="46" x2="628" y1="114.5" y2="114.5"/><text class="tick" x="38" y="118.5" text-anchor="end">256</text><line class="grid" x1="46" x2="628" y1="66.7" y2="66.7"/><text class="tick" x="38" y="70.7" text-anchor="end">384</text><line class="grid" x1="46" x2="628" y1="19.0" y2="19.0"/><text class="tick" x="38" y="23.0" text-anchor="end">512</text><rect class="mc-bar-pow" x="54.1" y="209.6" width="19.8" height="0.4" rx="2"/><rect class="mc-bar-reg" x="76.3" y="209.6" width="19.8" height="0.4" rx="2"/><rect class="mc-bar-pow" x="112.3" y="209.3" width="19.8" height="0.7" rx="2"/><rect class="mc-bar-reg" x="134.5" y="209.3" width="19.8" height="0.7" rx="2"/><rect class="mc-bar-pow" x="170.5" y="208.5" width="19.8" height="1.5" rx="2"/><rect class="mc-bar-reg" x="192.7" y="208.5" width="19.8" height="1.5" rx="2"/><rect class="mc-bar-pow" x="228.7" y="207.0" width="19.8" height="3.0" rx="2"/><rect class="mc-bar-reg" x="250.9" y="207.0" width="19.8" height="3.0" rx="2"/><rect class="mc-bar-pow" x="286.9" y="204.0" width="19.8" height="6.0" rx="2"/><rect class="mc-bar-reg" x="309.1" y="204.0" width="19.8" height="6.0" rx="2"/><rect class="mc-bar-pow" x="345.1" y="198.1" width="19.8" height="11.9" rx="2"/><rect class="mc-bar-reg" x="367.3" y="198.4" width="19.8" height="11.6" rx="2"/><text class="tick" x="377.2" y="193.4" text-anchor="middle">31</text><rect class="mc-bar-pow" x="403.3" y="186.1" width="19.8" height="23.9" rx="2"/><rect class="mc-bar-reg" x="425.5" y="188.7" width="19.8" height="21.3" rx="2"/><text class="tick" x="435.4" y="183.7" text-anchor="middle">57</text><rect class="mc-bar-pow" x="461.5" y="162.2" width="19.8" height="47.8" rx="2"/><rect class="mc-bar-reg" x="483.7" y="173.1" width="19.8" height="36.9" rx="2"/><text class="tick" x="493.6" y="168.1" text-anchor="middle">99</text><rect class="mc-bar-pow" x="519.7" y="114.5" width="19.8" height="95.5" rx="2"/><rect class="mc-bar-reg" x="541.9" y="149.2" width="19.8" height="60.8" rx="2"/><text class="tick" x="551.8" y="144.2" text-anchor="middle">163</text><rect class="mc-bar-pow" x="577.9" y="19.0" width="19.8" height="191.0" rx="2"/><rect class="mc-bar-reg" x="600.1" y="114.5" width="19.8" height="95.5" rx="2"/><text class="tick" x="610.0" y="109.5" text-anchor="middle">256</text><text class="tick" x="75.1" y="228" text-anchor="middle">1</text><text class="tick" x="133.3" y="228" text-anchor="middle">2</text><text class="tick" x="191.5" y="228" text-anchor="middle">3</text><text class="tick" x="249.7" y="228" text-anchor="middle">4</text><text class="tick" x="307.9" y="228" text-anchor="middle">5</text><text class="tick" x="366.1" y="228" text-anchor="middle">6</text><text class="tick" x="424.3" y="228" text-anchor="middle">7</text><text class="tick" x="482.5" y="228" text-anchor="middle">8</text><text class="tick" x="540.7" y="228" text-anchor="middle">9</text><text class="tick" x="598.9" y="228" text-anchor="middle">10</text><line class="axis" x1="46" x2="628" y1="210" y2="210"/><text class="tick" x="38" y="228" text-anchor="end">n</text></svg>

    <!-- /gen -->

    <!-- gen 7 -->

    <span class="viz-legend"><span><i class="mc-key-reg2"></i>מספר החלקים</span><span><i class="mc-key-pow"></i>2 בחזקת n − 1, הדפוס של 1, 2, 4, 8, 16</span></span>

    <!-- /gen -->

    **למה זה נשבר.** \( \binom{n}{4} + \binom{n}{2} + 1 \) הוא פולינום ממעלה 4, וחזקות של 2
    גדלות מהר יותר מכל פולינום. ההתאמה עד 5 אינה מקרה : לפי הבינום של ניוטון,
    \( 2^{n-1} = \sum_{j} \binom{n-1}{j} \), ובזהות פסקל אותו סכום עד \( j = 4 \) הוא
    \( \binom{n}{4} + \binom{n}{2} + 1 \) בדיוק. לכן שני המספרים שווים כל עוד
    \( n - 1 \le 4 \).

    **נסו בעצמכם.** כאן שש נקודות במצב כללי, ו-31 חלקים. הפכו שלושה קווים לקטרים : לחצו על
    נקודה 4 והזיזו אותה בחיצים 6 מעלות אחורה, מ-271 ל-265, מול נקודה 1. את נקודה 5 הזיזו 8
    מעלות קדימה, מ-324 ל-332, ואת נקודה 6 תשע מעלות אחורה, מ-32 ל-23. כל לחיצה על חץ היא
    מעלה אחת : ימינה או למעלה קדימה, שמאלה או למטה אחורה. שלושת הקטרים נפגשים במרכז, ויש
    13 נקודות חיתוך ו-30 חלקים. על הציורים התיבה מוסיפה ספירה מתוך הגאומטריה לכל מיקום
    שתגררו :

    <div class="explorer" data-kind="circlecut" data-n="6" data-angles="85 152 203 271 324 32"></div>

    #### סיבוכיות { .sol-cost }

    שלושה מקדמים בינומיים, כל אחד בכמה כפלים : \( O(1) \) זמן וזיכרון. בסעיף א הספירה
    הייתה \( O(n^4) \).

---

### סעיף ג – מתוך הקואורדינטות

הנקודות כבר לא בהכרח במצב כללי.

1. כתבו פונקציה שמקבלת את הזוויות של הנקודות על המעגל (במעלות), ומחזירה את מספר
   החלקים מתוך הגאומטריה עצמה, גם כששלושה קווים או יותר נפגשים באותה נקודה.
2. לכמה חלקים מתחלק העיגול כשהנקודות הן קודקודים של משושה משוכלל? ומה ההפרש מהנוסחה
   כשבנקודה אחת נפגשים \( m \) קווים?

??? tip "רמז 1"
    בהוכחה של אוילר לא השתמשנו בכך שנקודת חיתוך היא של שני קווים בדיוק. ספרו את
    הקודקודים ואת הצלעות כמו שהם, עם נקודות חיתוך שונות בלבד.

??? tip "רמז 2"
    במחשב, שתי נקודות חיתוך "זהות" יוצאות שונות בספרה האחרונה. אחדו נקודות
    קרובות מאוד לנקודה אחת. ובמשושה משוכלל, היכן נפגשים שלושה קווים?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        מחשבים את כל נקודות החיתוך, מאחדים נקודות קרובות, וסופרים
        \( V = n + P \) ו-\( E = n + \sum_c (p_c + 1) \), כש-\( P \) מספר נקודות החיתוך
        השונות ו-\( p_c \) מספר נקודות החיתוך על הקו \( c \). החלקים הם \( E - V + 1 \).
        במשושה משוכלל שלושת הקטרים נפגשים במרכז, ויש **30 חלקים** ולא 31. בנקודה שבה נפגשים
        \( m \) קווים הולכים לאיבוד \( \binom{m-1}{2} \) חלקים.

    <!-- cost: זמן \( O(n^4 P) \) | זיכרון \( O(n^2 + P) \) -->

    #### הרעיון { .sol-idea }

    **אוילר עובד תמיד.** בהוכחה השנייה של סעיף ב ספרנו קודקודים וצלעות. אותה ספירה נכונה
    גם כשבנקודה אחת עוברים יותר משני קווים : הנקודה היא קודקוד אחד, וכל קו שעובר בה נחתך
    בה פעם אחת. לכן

    \[ \text{regions} = E - V + 1 = 1 + \binom{n}{2} + \sum_c p_c - P . \]

    במצב כללי כל נקודה נמצאת על שני קווים, \( \sum_c p_c = 2P \), וחוזרים לנוסחה.

    **נקודה עם \( m \) קווים.** במצב כללי, \( m \) קווים היו נחתכים ב-\( \binom{m}{2} \)
    נקודות, וכל אחת תורמת 1 ל-\( \sum p_c - P \). כשכולם עוברים בנקודה אחת, היא תורמת
    \( m - 1 \). ההפרש הוא \( \binom{m}{2} - (m - 1) = \binom{m-1}{2} \). במשושה, \( m = 3 \)
    במרכז, וחסר חלק אחד : 30.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **נקודות :** \( (\cos\theta, \sin\theta) \) לכל זווית.
    2. **חיתוכים :** לכל זוג קווים עם ארבעה קצוות שונים, נקודת החיתוך אם היא בתוך שני
       הקטעים.
    3. **איחוד :** מעגלים את הקואורדינטות של כל נקודת חיתוך ל-7 ספרות אחרי הנקודה, ונקודות
       שיוצאות זהות הן נקודה אחת. ב-SystemVerilog בודקים במקום זה מרחק קטן
       מ-\( 10^{-7} \).
    4. **אוילר :** \( V \) ו-\( E \) כמו בסעיף ב, והחלקים \( E - V + 1 \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="count_regions" linenums="1" hl_lines="13 30"
        import itertools
        import math


        def crossing(p, q, r, s):
            """The point where segment pq crosses segment rs strictly inside both, or None."""
            den = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0])
            if abs(den) < 1e-12:
                return None
            t = ((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / den
            u = ((r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])) / den
            if 1e-9 < t < 1 - 1e-9 and 1e-9 < u < 1 - 1e-9:
                return (round(p[0] + t * (q[0] - p[0]), 7), round(p[1] + t * (q[1] - p[1]), 7))  # (1)!
            return None


        def count_regions(angles):
            """The regions of the disc cut by the chords between points at the given angles
            (degrees, every point once), in any position: Euler's formula on the planar graph."""
            pts = [(math.cos(math.radians(t)), math.sin(math.radians(t))) for t in angles]
            n = len(pts)
            on = {c: set() for c in itertools.combinations(range(n), 2)}   # crossings on each chord
            for (a, b), (c, d) in itertools.combinations(on, 2):
                x = crossing(pts[a], pts[b], pts[c], pts[d])
                if x:
                    on[(a, b)].add(x)
                    on[(c, d)].add(x)
            inner = set().union(*on.values())                            # the distinct crossings
            V = n + len(inner)
            E = n + sum(len(s) + 1 for s in on.values())                 # (2)!
            return E - V + 1 if n else 1
        ```

        1. העיגול ל-7 ספרות הוא האיחוד : שלושה קווים שנפגשים במרכז נותנים שלוש נקודות
           שנבדלות רק בספרה ה-16, והן נהיות נקודה אחת בקבוצה. עיגול אינו בדיוק בדיקת
           מרחק : שתי נקודות כמעט זהות משני צדי גבול של עיגול, כמו 0.12345674999999999
           ו-0.12345675, יוצאות 0.1234567 ו-0.1234568. בדוגמאות כאן זה לא קורה, ובדיקת
           המרחק של SystemVerilog סוגרת גם את המקרה הזה.
        2. ‏\( n \) קשתות, וקו שעוברות בו \( p \) נקודות חיתוך שונות הוא \( p + 1 \) קטעים.

    === "SystemVerilog"
        ```systemverilog title="function automatic int count_regions" linenums="1" hl_lines="25 36"
        // The regions of the disc cut by the chords between points at the given angles
        // (degrees, every point once), in any position: Euler's formula on the planar graph.
        function automatic int count_regions(real ang[$]);
          real px[$], py[$], ix[$], iy[$];      // the points; the distinct crossings
          int ca[$], cb[$];                      // the chords
          int n = ang.size(), pieces = 0;
          for (int i = 0; i < n; i++) begin
            px.push_back($cos(ang[i] * 3.14159265358979 / 180.0));
            py.push_back($sin(ang[i] * 3.14159265358979 / 180.0));
          end
          for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) begin ca.push_back(a); cb.push_back(b); end
          foreach (ca[i]) begin
            real hx[$], hy[$];                   // the crossings on chord i
            foreach (ca[j]) begin
              real den, t, u, x, y;
              bit seen = 0;
              if (j == i || ca[j] == ca[i] || ca[j] == cb[i] || cb[j] == ca[i] || cb[j] == cb[i]) continue;
              den = (px[cb[i]] - px[ca[i]]) * (py[cb[j]] - py[ca[j]]) - (py[cb[i]] - py[ca[i]]) * (px[cb[j]] - px[ca[j]]);
              if (den < 1e-12 && den > -1e-12) continue;
              t = ((px[ca[j]] - px[ca[i]]) * (py[cb[j]] - py[ca[j]]) - (py[ca[j]] - py[ca[i]]) * (px[cb[j]] - px[ca[j]])) / den;
              u = ((px[ca[j]] - px[ca[i]]) * (py[cb[i]] - py[ca[i]]) - (py[ca[j]] - py[ca[i]]) * (px[cb[i]] - px[ca[i]])) / den;
              if (!(t > 1e-9 && t < 1 - 1e-9 && u > 1e-9 && u < 1 - 1e-9)) continue;
              x = px[ca[i]] + t * (px[cb[i]] - px[ca[i]]);
              y = py[ca[i]] + t * (py[cb[i]] - py[ca[i]]);
              foreach (hx[k]) if ((hx[k] - x) ** 2 + (hy[k] - y) ** 2 < 1e-14) seen = 1;   // (1)!
              if (!seen) begin hx.push_back(x); hy.push_back(y); end
            end
            pieces += hx.size() + 1;
            foreach (hx[k]) begin
              bit seen = 0;
              foreach (ix[m]) if ((ix[m] - hx[k]) ** 2 + (iy[m] - hy[k]) ** 2 < 1e-14) seen = 1;
              if (!seen) begin ix.push_back(hx[k]); iy.push_back(hy[k]); end
            end
          end
          if (n == 0) return 1;
          return (n + pieces) - (n + ix.size()) + 1;   // (2)!
        endfunction
        ```

        1. האיחוד : נקודה במרחק קטן מ-\( 10^{-7} \) מנקודה שכבר נמצאה על אותו קו היא אותה
           נקודה.
        2. ‏\( E - V + 1 \), עם \( E = n + \) הקטעים ו-\( V = n + \) נקודות החיתוך השונות.

    #### למה זה נכון { .sol-proof }

    **המשושה המשוכלל.** שלושת הקטרים נפגשים במרכז (מסומן בעיגול). במקום שלוש נקודות
    חיתוך יש שם אחת, ולכן יש 13 נקודות חיתוך ו-30 חלקים :

    <!-- gen 8 -->

    <svg class="figure mc-fig" viewBox="0 0 272 272" style="max-width:17.0rem" role="img" aria-label="משושה משוכלל וכל הקווים בין קודקודיו. שלושת הקטרים נפגשים במרכז, ולכן יש רק 13 נקודות חיתוך ו-30 חלקים במקום 31"><path class="mc-reg mc-c0" d="M136.0,81.0L136.0,136.0L183.6,108.5L167.8,81.0L136.0,81.0Z"/><path class="mc-reg mc-c1" d="M199.5,136.0L183.6,108.5L136.0,136.0L183.6,163.5L199.5,136.0Z"/><path class="mc-reg mc-c2" d="M136.0,136.0L136.0,191.0L167.8,191.0L183.6,163.5L136.0,136.0Z"/><path class="mc-reg mc-c3" d="M136.0,191.0L136.0,136.0L88.4,163.5L104.2,191.0L136.0,191.0Z"/><path class="mc-reg mc-c4" d="M88.4,108.5L72.5,136.0L88.4,163.5L136.0,136.0L88.4,108.5Z"/><path class="mc-reg mc-c5" d="M104.2,81.0L88.4,108.5L136.0,136.0L136.0,81.0L104.2,81.0Z"/><path class="mc-reg mc-c1" d="M136.0,26.0L136.0,81.0L167.8,81.0L136.0,26.0Z"/><path class="mc-reg mc-c1" d="M167.8,81.0L183.6,108.5L231.3,81.0L167.8,81.0Z"/><path class="mc-reg mc-c2" d="M183.6,108.5L199.5,136.0L231.3,81.0L183.6,108.5Z"/><path class="mc-reg mc-c3" d="M231.3,191.0L199.5,136.0L183.6,163.5L231.3,191.0Z"/><path class="mc-reg mc-c4" d="M231.3,191.0L183.6,163.5L167.8,191.0L231.3,191.0Z"/><path class="mc-reg mc-c5" d="M136.0,191.0L136.0,246.0L167.8,191.0L136.0,191.0Z"/><path class="mc-reg mc-c0" d="M136.0,246.0L136.0,191.0L104.2,191.0L136.0,246.0Z"/><path class="mc-reg mc-c1" d="M104.2,191.0L88.4,163.5L40.7,191.0L104.2,191.0Z"/><path class="mc-reg mc-c2" d="M72.5,136.0L40.7,191.0L88.4,163.5L72.5,136.0Z"/><path class="mc-reg mc-c3" d="M72.5,136.0L88.4,108.5L40.7,81.0L72.5,136.0Z"/><path class="mc-reg mc-c4" d="M88.4,108.5L104.2,81.0L40.7,81.0L88.4,108.5Z"/><path class="mc-reg mc-c0" d="M136.0,26.0L104.2,81.0L136.0,81.0L136.0,26.0Z"/><path class="mc-reg mc-c0" d="M136.0,26.0L167.8,81.0L231.3,81.0L136.0,26.0Z"/><path class="mc-reg mc-c1" d="M199.5,136.0L231.3,191.0L231.3,81.0L199.5,136.0Z"/><path class="mc-reg mc-c2" d="M231.3,191.0L167.8,191.0L136.0,246.0L231.3,191.0Z"/><path class="mc-reg mc-c3" d="M136.0,246.0L104.2,191.0L40.7,191.0L136.0,246.0Z"/><path class="mc-reg mc-c4" d="M40.7,191.0L72.5,136.0L40.7,81.0L40.7,191.0Z"/><path class="mc-reg mc-c5" d="M136.0,26.0L40.7,81.0L104.2,81.0L136.0,26.0Z"/><path class="mc-reg mc-c1" d="M231.3,81.0A110,110 0 0 0 136.0,26.0L231.3,81.0Z"/><path class="mc-reg mc-c2" d="M231.3,191.0A110,110 0 0 0 231.3,81.0L231.3,191.0Z"/><path class="mc-reg mc-c3" d="M136.0,246.0A110,110 0 0 0 231.3,191.0L136.0,246.0Z"/><path class="mc-reg mc-c4" d="M40.7,191.0A110,110 0 0 0 136.0,246.0L40.7,191.0Z"/><path class="mc-reg mc-c5" d="M40.7,81.0A110,110 0 0 0 40.7,191.0L40.7,81.0Z"/><path class="mc-reg mc-c0" d="M136.0,26.0A110,110 0 0 0 40.7,81.0L136.0,26.0Z"/><circle class="mc-ring" cx="136" cy="136" r="110"/><line class="mc-chord" x1="136.0" y1="26.0" x2="40.7" y2="81.0"/><line class="mc-chord" x1="136.0" y1="26.0" x2="40.7" y2="191.0"/><line class="mc-chord" x1="136.0" y1="26.0" x2="136.0" y2="246.0"/><line class="mc-chord" x1="136.0" y1="26.0" x2="231.3" y2="191.0"/><line class="mc-chord" x1="136.0" y1="26.0" x2="231.3" y2="81.0"/><line class="mc-chord" x1="40.7" y1="81.0" x2="40.7" y2="191.0"/><line class="mc-chord" x1="40.7" y1="81.0" x2="136.0" y2="246.0"/><line class="mc-chord" x1="40.7" y1="81.0" x2="231.3" y2="191.0"/><line class="mc-chord" x1="40.7" y1="81.0" x2="231.3" y2="81.0"/><line class="mc-chord" x1="40.7" y1="191.0" x2="136.0" y2="246.0"/><line class="mc-chord" x1="40.7" y1="191.0" x2="231.3" y2="191.0"/><line class="mc-chord" x1="40.7" y1="191.0" x2="231.3" y2="81.0"/><line class="mc-chord" x1="136.0" y1="246.0" x2="231.3" y2="191.0"/><line class="mc-chord" x1="136.0" y1="246.0" x2="231.3" y2="81.0"/><line class="mc-chord" x1="231.3" y1="191.0" x2="231.3" y2="81.0"/><circle class="mc-triple" cx="136.0" cy="136.0" r="7"/><circle class="mc-pt" cx="136.0" cy="26.0" r="5.5"/><text class="mc-plab" x="136.0" y="15.0" text-anchor="middle">1</text><circle class="mc-pt" cx="40.7" cy="81.0" r="5.5"/><text class="mc-plab" x="27.7" y="77.5" text-anchor="middle">2</text><circle class="mc-pt" cx="40.7" cy="191.0" r="5.5"/><text class="mc-plab" x="27.7" y="202.5" text-anchor="middle">3</text><circle class="mc-pt" cx="136.0" cy="246.0" r="5.5"/><text class="mc-plab" x="136.0" y="265.0" text-anchor="middle">4</text><circle class="mc-pt" cx="231.3" cy="191.0" r="5.5"/><text class="mc-plab" x="244.3" y="202.5" text-anchor="middle">5</text><circle class="mc-pt" cx="231.3" cy="81.0" r="5.5"/><text class="mc-plab" x="244.3" y="77.5" text-anchor="middle">6</text></svg>

    <!-- /gen -->

    <!-- gen 9 -->

    <span class="viz-legend"><span><i class="mc-key-triple"></i>נקודה שבה שלושה קווים נפגשים</span></span>

    <!-- /gen -->

    **מצולעים משוכללים.** הטבלה מחושבת בקוד. במצולע עם מספר זוגי של קודקודים, מ-6 ומעלה,
    כל הקטרים נפגשים במרכז, ומ-8 יש גם נקודות אחרות שבהן נפגשים שלושה קווים. במספר אי-זוגי אין אף נקודה כזו,
    והמספר שווה לנוסחה (משפט של Poonen ו-Rubinstein משנת 1998, והטבלה בודקת עד 12) :

    <!-- gen 10 -->

    | ‏n | נקודות במצב כללי | מצולע משוכלל | ההפרש |
    |:-:|:-:|:-:|:-:|
    | 3 | 4 | 4 | 0 |
    | 4 | 8 | 8 | 0 |
    | 5 | 16 | 16 | 0 |
    | 6 | 31 | 30 | 1 |
    | 7 | 57 | 57 | 0 |
    | 8 | 99 | 88 | 11 |
    | 9 | 163 | 163 | 0 |
    | 10 | 256 | 230 | 26 |
    | 11 | 386 | 386 | 0 |
    | 12 | 562 | 456 | 106 |

    <!-- /gen -->

    **נסו בעצמכם.** כאן משושה משוכלל, והנקודה שבמרכז מסומנת. בחרו 7 נקודות : 57 חלקים,
    כמו בנוסחה, ואין נקודה מסומנת. בחרו 8 : ‏88 חלקים מול 99, ותשע נקודות מסומנות, שמונה
    של שלושה קווים והמרכז, שבו נפגשים ארבעה. חזרו ל-6 ובחרו "קו אחר קו" : הקו בין 3 ל-6
    מוסיף 4 ולא 5, כי הוא פוגש את הקו בין 1 ל-4 ואת הקו בין 2 ל-5 באותה נקודה. ולבסוף
    בחרו שוב "כולם", עברו ל"חופשי, גוררים" והזיזו קודקוד אחד מעלה אחת בחץ : המרכז מתפרק
    לשלוש נקודות, ויש 31 חלקים. על הטבלה התיבה מוסיפה את המקום של כל נקודה כזו בציור :

    <div class="explorer" data-kind="circlecut" data-n="6" data-where="regular"></div>

    #### סיבוכיות { .sol-cost }

    יש \( O(n^2) \) קווים ו-\( O(n^4) \) זוגות של קווים. לכל חיתוך בודקים אם הוא כבר
    נמצא, מול \( P \) הנקודות השונות : \( O(n^4 P) \) זמן, ו-\( O(n^2 + P) \) זיכרון.
    תמיד \( P \le \binom{n}{4} \) : כל נקודת חיתוך באה לפחות מרביעייה אחת של נקודות (שני
    קווים שנחתכים בה), וכל רביעייה נותנת נקודת חיתוך אחת בלבד. עם טבלת גיבוב (hash) על הקואורדינטות המעוגלות, כמו
    הקבוצה ב-Python, הזמן יורד ל-\( O(n^4) \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : 1, 2, 4, 8, 16, אז 32"
    חמשת המקרים הראשונים מתאימים ל-\( 2^{n-1} \), ומשם זה נשבר : 31, 57, 99. דפוס הוא
    השערה, לא הוכחה. הספירה של מה שכל קו מוסיף נותנת את התשובה הנכונה מההתחלה.

??? trap "מלכודת : לספור כל זוג קווים כחיתוך"
    יש \( \binom{\binom{n}{2}}{2} \) זוגות של קווים, אבל רובם לא נחתכים בתוך העיגול : קווים
    עם קצה משותף נפגשים רק על המעגל, וקווים שהקצוות שלהם לא מתחלפים לא נפגשים בכלל. רק
    זיווג אחד מכל ארבע נקודות נחתך, ולכן החיתוכים הם \( \binom{n}{4} \).

??? trap "מלכודת : אוילר בלי הקשתות או עם הפאה החיצונית"
    בלי הקשתות של המעגל, החלקים שליד המעגל לא סגורים והגרף לא נותן אותם. ונוסחת אוילר
    סופרת גם את הפאה שמחוץ לעיגול. החלקים הם \( E - V + 1 \), לא \( E - V + 2 \).

??? trap "מלכודת : להשוות נקודות חיתוך בשוויון מדויק"
    במשושה משוכלל שלושת החיתוכים במרכז יוצאים במחשב כנקודות שנבדלות ב-\( 10^{-16} \).
    בשוויון מדויק הן שלוש נקודות, והתוצאה היא 31 במקום 30. צריך לאחד נקודות קרובות.

??? followup "שאלות המשך"
    - **ישרים במישור :** לכמה חלקים מחלקים \( n \) ישרים את המישור, כששום שניים לא מקבילים
      ושום שלושה לא נפגשים?

        ??? fu-answer "תשובה"
            ‏\( \binom{n}{2} + n + 1 \). אותו טיעון : כל ישר חדש נחתך ב-\( k \) נקודות
            ל-\( k + 1 \) חלקים, וכאן כל זוג ישרים נחתך.

    - **קצב הגדילה :** מי גדל מהר יותר, מספר החלקים או \( 2^{n-1} \)?

        ??? fu-answer "תשובה"
            ‏\( 2^{n-1} \). מספר החלקים הוא בערך \( n^4/24 \), פולינום, וב-\( n = 10 \) הוא כבר
            256 מול 512. היחס ביניהם שואף ל-0.

    - **מצולע משוכלל :** האם יש נוסחה למספר החלקים במצולע משוכלל?

        ??? fu-answer "תשובה"
            יש, אבל מסובכת. Poonen ו-Rubinstein (1998) נתנו נוסחה שיש בה איברים שתלויים
            בהתחלקות של \( n \) ב-6, ב-12, ב-18 ובעוד מספרים, עד 210. כש-\( n \) אי-זוגי אין
            נקודות שבהן נפגשים שלושה קווים, והנוסחה של השאלה נכונה.
