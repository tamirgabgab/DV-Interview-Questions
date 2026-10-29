---
id: 18
title: שני שעוני חול – מדידת D דקות מרגע 0
level: junior
difficulty: medium
kind: puzzle
tags: [algorithms, bfs, logic-puzzles, python, systemverilog]
source: ""
added: 2026-10-18
---

## השאלה

נתונים שני שעוני חול : שעון \( A \) שמודד \( A \) דקות ושעון \( B \) שמודד \( B \) דקות.
בכל רגע אפשר **להפוך** שעון (או את שניהם), גם באמצע הריצה שלו : החול שנשאר למעלה עובר
למטה, והחול שהיה למטה עובר למעלה וממשיך לרדת. אין שעון אחר, ואי אפשר לחלק חול.

צריך למדוד **בדיוק \( D \) דקות מרגע 0** : ברגע 0 מתחילים (שני השעונים עם כל החול למטה),
וברגע \( D \) איזשהו שעון חול צריך להיגמר בדיוק.

??? interviewer "מה המראיין בודק"
    - **היפוך באמצע הריצה :** האם המועמד רואה שהיפוך של שעון חצי-ריק שומר את כמות החול
      שכבר ירדה, ומשתמש בזה.
    - **מודל במקום ניחושים :** אחרי דוגמה אחת ביד, האם הוא מגדיר **מצב** של המערכת ומזהה
      שיש מספר קטן של פעולות אפשריות בכל רגע.
    - **מתי מחליטים :** האם הוא מבין שאין שעון אחר, ולכן ההחלטות מתקבלות רק ברגעים שבהם
      שעון נגמר.
    - **חיפוש בגרף :** האם הוא מחבר את הבעיה ל-BFS, ויודע להסביר למה החיפוש מסתיים ולמה
      הוא שלם.

---

### סעיף א – דוגמה : A = 7, B = 11, D = 15

מצאו רצף פעולות שמודד 15 דקות מרגע 0. הסבירו מתי הופכים כל שעון ולמה.

??? tip "רמז 1"
    שימו לב ש-\( 15 = 11 + 4 \). איך "מייצרים" 4 דקות עם שעונים של 7 ו-11?

??? tip "רמז 2"
    חשבו על ההפרש \( 11 - 7 = 4 \), ועל מה שקורה כשהופכים שעון **באמצע** הריצה שלו : כמה
    חול יש לו למטה באותו רגע?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        הופכים את שניהם ברגע 0, הופכים את \( A \) כשהוא נגמר (רגע 7), ושוב כש-\( B \) נגמר
        (רגע 11). ברגע 11 יש ב-\( A \) בדיוק 4 דקות של חול למטה, ההיפוך מעלה אותן, והוא
        נגמר ברגע \( 11 + 4 = 15 \).

    #### הרעיון { .sol-idea }

    היפוך של שעון באמצע הריצה **משמר את החלוקה** של החול ורק הופך את הכיוון. ברגע 11
    שעון \( A \) רץ 4 דקות מאז ההיפוך השני שלו, כלומר 4 דקות של חול כבר למטה. ההיפוך
    מחזיר אותן למעלה, וכך מקבלים "שעון של 4 דקות" שאין לנו.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **רגע 0 :** הופכים את שני השעונים.
    2. **רגע 7 :** שעון \( A \) נגמר. הופכים אותו מיד. בשעון \( B \) נשארו 4 דקות למעלה.
    3. **רגע 11 :** שעון \( B \) נגמר. בשעון \( A \) נשארו 3 דקות למעלה ו-4 למטה. הופכים את
       \( A \) : עכשיו 4 הדקות למעלה.
    4. **רגע 15 :** שעון \( A \) נגמר. עברו בדיוק \( 11 + 4 = 15 \) דקות.

    </div>

    #### למה זה נכון { .sol-proof }

    **אירוע אחרי אירוע.** לחצו "הבא" כדי לעקוב : משמאל מצב השעונים ברגע האירוע, מימין
    המצב אחרי הפעולה. המספר ליד כל שעון הוא כמות החול למעלה ולמטה, בדקות :

    <div class="stepper" role="group" aria-label="התוכנית למדידת 15 דקות עם שעוני חול של 7 ו-11 דקות, אירוע אחרי אירוע" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="רגע 0 : start"><text class="legend" x="10" y="33.0" font-weight="700">t = 0</text><text class="tick" x="10" y="51.0">start</text><clipPath id="hg1t"><polygon points="92,12 122,12 110.0,37.0 104.0,37.0"/></clipPath><clipPath id="hg1b"><polygon points="104.0,37.0 110.0,37.0 122,62 92,62"/></clipPath><rect class="sand-a" clip-path="url(#hg1b)" x="92" y="37.0" width="30" height="25.0"/><polygon class="glass" points="92,12 122,12 110.0,37.0 104.0,37.0"/><polygon class="glass" points="104.0,37.0 110.0,37.0 122,62 92,62"/><line class="frame" x1="88" y1="12" x2="126" y2="12"/><line class="frame" x1="88" y1="62" x2="126" y2="62"/><text class="tick" x="129" y="24">0</text><text class="tick" x="129" y="60">7</text><text class="legend" x="107.0" y="77" text-anchor="middle">A</text><clipPath id="hg2t"><polygon points="156,12 186,12 174.0,37.0 168.0,37.0"/></clipPath><clipPath id="hg2b"><polygon points="168.0,37.0 174.0,37.0 186,62 156,62"/></clipPath><rect class="sand-b" clip-path="url(#hg2b)" x="156" y="37.0" width="30" height="25.0"/><polygon class="glass" points="156,12 186,12 174.0,37.0 168.0,37.0"/><polygon class="glass" points="168.0,37.0 174.0,37.0 186,62 156,62"/><line class="frame" x1="152" y1="12" x2="190" y2="12"/><line class="frame" x1="152" y1="62" x2="190" y2="62"/><text class="tick" x="193" y="24">0</text><text class="tick" x="193" y="60">11</text><text class="legend" x="171.0" y="77" text-anchor="middle">B</text><line class="ink-line" x1="222" y1="37.0" x2="306" y2="37.0" stroke-width="1.5"/><polygon class="ink-fill" points="312,37.0 304,33.0 304,41.0"/><text class="legend" x="267" y="29.0" text-anchor="middle">flip A + B</text><clipPath id="hg3t"><polygon points="336,12 366,12 354.0,37.0 348.0,37.0"/></clipPath><clipPath id="hg3b"><polygon points="348.0,37.0 354.0,37.0 366,62 336,62"/></clipPath><rect class="sand-a" clip-path="url(#hg3t)" x="336" y="12.0" width="30" height="25.0"/><line class="stream-a" x1="351.0" y1="37.0" x2="351.0" y2="61.0"/><polygon class="glass" points="336,12 366,12 354.0,37.0 348.0,37.0"/><polygon class="glass" points="348.0,37.0 354.0,37.0 366,62 336,62"/><line class="frame" x1="332" y1="12" x2="370" y2="12"/><line class="frame" x1="332" y1="62" x2="370" y2="62"/><text class="tick" x="373" y="24">7</text><text class="tick" x="373" y="60">0</text><text class="legend" x="351.0" y="77" text-anchor="middle">A</text><clipPath id="hg4t"><polygon points="400,12 430,12 418.0,37.0 412.0,37.0"/></clipPath><clipPath id="hg4b"><polygon points="412.0,37.0 418.0,37.0 430,62 400,62"/></clipPath><rect class="sand-b" clip-path="url(#hg4t)" x="400" y="12.0" width="30" height="25.0"/><line class="stream-b" x1="415.0" y1="37.0" x2="415.0" y2="61.0"/><polygon class="glass" points="400,12 430,12 418.0,37.0 412.0,37.0"/><polygon class="glass" points="412.0,37.0 418.0,37.0 430,62 400,62"/><line class="frame" x1="396" y1="12" x2="434" y2="12"/><line class="frame" x1="396" y1="62" x2="434" y2="62"/><text class="tick" x="437" y="24">11</text><text class="tick" x="437" y="60">0</text><text class="legend" x="415.0" y="77" text-anchor="middle">B</text></svg><figcaption>רגע 0 : הופכים את שני השעונים. השעון הראשון שייגמר הוא A, בעוד 7 דקות.</figcaption></figure><figure class="stepper-frame"><svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="רגע 7 : A runs out"><text class="legend" x="10" y="33.0" font-weight="700">t = 7</text><text class="tick" x="10" y="51.0">A runs out</text><clipPath id="hg5t"><polygon points="92,12 122,12 110.0,37.0 104.0,37.0"/></clipPath><clipPath id="hg5b"><polygon points="104.0,37.0 110.0,37.0 122,62 92,62"/></clipPath><rect class="sand-a" clip-path="url(#hg5b)" x="92" y="37.0" width="30" height="25.0"/><polygon class="glass" points="92,12 122,12 110.0,37.0 104.0,37.0"/><polygon class="glass" points="104.0,37.0 110.0,37.0 122,62 92,62"/><line class="frame" x1="88" y1="12" x2="126" y2="12"/><line class="frame" x1="88" y1="62" x2="126" y2="62"/><text class="tick" x="129" y="24">0</text><text class="tick" x="129" y="60">7</text><text class="legend" x="107.0" y="77" text-anchor="middle">A</text><clipPath id="hg6t"><polygon points="156,12 186,12 174.0,37.0 168.0,37.0"/></clipPath><clipPath id="hg6b"><polygon points="168.0,37.0 174.0,37.0 186,62 156,62"/></clipPath><rect class="sand-b" clip-path="url(#hg6t)" x="156" y="27.9" width="30" height="9.1"/><line class="stream-b" x1="171.0" y1="37.0" x2="171.0" y2="45.1"/><rect class="sand-b" clip-path="url(#hg6b)" x="156" y="46.1" width="30" height="15.9"/><polygon class="glass" points="156,12 186,12 174.0,37.0 168.0,37.0"/><polygon class="glass" points="168.0,37.0 174.0,37.0 186,62 156,62"/><line class="frame" x1="152" y1="12" x2="190" y2="12"/><line class="frame" x1="152" y1="62" x2="190" y2="62"/><text class="tick" x="193" y="24">4</text><text class="tick" x="193" y="60">7</text><text class="legend" x="171.0" y="77" text-anchor="middle">B</text><line class="ink-line" x1="222" y1="37.0" x2="306" y2="37.0" stroke-width="1.5"/><polygon class="ink-fill" points="312,37.0 304,33.0 304,41.0"/><text class="legend" x="267" y="29.0" text-anchor="middle">flip A</text><clipPath id="hg7t"><polygon points="336,12 366,12 354.0,37.0 348.0,37.0"/></clipPath><clipPath id="hg7b"><polygon points="348.0,37.0 354.0,37.0 366,62 336,62"/></clipPath><rect class="sand-a" clip-path="url(#hg7t)" x="336" y="12.0" width="30" height="25.0"/><line class="stream-a" x1="351.0" y1="37.0" x2="351.0" y2="61.0"/><polygon class="glass" points="336,12 366,12 354.0,37.0 348.0,37.0"/><polygon class="glass" points="348.0,37.0 354.0,37.0 366,62 336,62"/><line class="frame" x1="332" y1="12" x2="370" y2="12"/><line class="frame" x1="332" y1="62" x2="370" y2="62"/><text class="tick" x="373" y="24">7</text><text class="tick" x="373" y="60">0</text><text class="legend" x="351.0" y="77" text-anchor="middle">A</text><clipPath id="hg8t"><polygon points="400,12 430,12 418.0,37.0 412.0,37.0"/></clipPath><clipPath id="hg8b"><polygon points="412.0,37.0 418.0,37.0 430,62 400,62"/></clipPath><rect class="sand-b" clip-path="url(#hg8t)" x="400" y="27.9" width="30" height="9.1"/><line class="stream-b" x1="415.0" y1="37.0" x2="415.0" y2="45.1"/><rect class="sand-b" clip-path="url(#hg8b)" x="400" y="46.1" width="30" height="15.9"/><polygon class="glass" points="400,12 430,12 418.0,37.0 412.0,37.0"/><polygon class="glass" points="412.0,37.0 418.0,37.0 430,62 400,62"/><line class="frame" x1="396" y1="12" x2="434" y2="12"/><line class="frame" x1="396" y1="62" x2="434" y2="62"/><text class="tick" x="437" y="24">4</text><text class="tick" x="437" y="60">7</text><text class="legend" x="415.0" y="77" text-anchor="middle">B</text></svg><figcaption>רגע 7 : שעון A נגמר והופכים אותו מיד. בשעון B נשארו 4 דקות למעלה, והוא ייגמר ראשון.</figcaption></figure><figure class="stepper-frame"><svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="רגע 11 : B runs out"><text class="legend" x="10" y="33.0" font-weight="700">t = 11</text><text class="tick" x="10" y="51.0">B runs out</text><clipPath id="hg9t"><polygon points="92,12 122,12 110.0,37.0 104.0,37.0"/></clipPath><clipPath id="hg9b"><polygon points="104.0,37.0 110.0,37.0 122,62 92,62"/></clipPath><rect class="sand-a" clip-path="url(#hg9t)" x="92" y="26.3" width="30" height="10.7"/><line class="stream-a" x1="107.0" y1="37.0" x2="107.0" y2="46.7"/><rect class="sand-a" clip-path="url(#hg9b)" x="92" y="47.7" width="30" height="14.3"/><polygon class="glass" points="92,12 122,12 110.0,37.0 104.0,37.0"/><polygon class="glass" points="104.0,37.0 110.0,37.0 122,62 92,62"/><line class="frame" x1="88" y1="12" x2="126" y2="12"/><line class="frame" x1="88" y1="62" x2="126" y2="62"/><text class="tick" x="129" y="24">3</text><text class="tick" x="129" y="60">4</text><text class="legend" x="107.0" y="77" text-anchor="middle">A</text><clipPath id="hg10t"><polygon points="156,12 186,12 174.0,37.0 168.0,37.0"/></clipPath><clipPath id="hg10b"><polygon points="168.0,37.0 174.0,37.0 186,62 156,62"/></clipPath><rect class="sand-b" clip-path="url(#hg10b)" x="156" y="37.0" width="30" height="25.0"/><polygon class="glass" points="156,12 186,12 174.0,37.0 168.0,37.0"/><polygon class="glass" points="168.0,37.0 174.0,37.0 186,62 156,62"/><line class="frame" x1="152" y1="12" x2="190" y2="12"/><line class="frame" x1="152" y1="62" x2="190" y2="62"/><text class="tick" x="193" y="24">0</text><text class="tick" x="193" y="60">11</text><text class="legend" x="171.0" y="77" text-anchor="middle">B</text><line class="ink-line" x1="222" y1="37.0" x2="306" y2="37.0" stroke-width="1.5"/><polygon class="ink-fill" points="312,37.0 304,33.0 304,41.0"/><text class="legend" x="267" y="29.0" text-anchor="middle">flip A</text><clipPath id="hg11t"><polygon points="336,12 366,12 354.0,37.0 348.0,37.0"/></clipPath><clipPath id="hg11b"><polygon points="348.0,37.0 354.0,37.0 366,62 336,62"/></clipPath><rect class="sand-a" clip-path="url(#hg11t)" x="336" y="22.7" width="30" height="14.3"/><line class="stream-a" x1="351.0" y1="37.0" x2="351.0" y2="50.3"/><rect class="sand-a" clip-path="url(#hg11b)" x="336" y="51.3" width="30" height="10.7"/><polygon class="glass" points="336,12 366,12 354.0,37.0 348.0,37.0"/><polygon class="glass" points="348.0,37.0 354.0,37.0 366,62 336,62"/><line class="frame" x1="332" y1="12" x2="370" y2="12"/><line class="frame" x1="332" y1="62" x2="370" y2="62"/><text class="tick" x="373" y="24">4</text><text class="tick" x="373" y="60">3</text><text class="legend" x="351.0" y="77" text-anchor="middle">A</text><clipPath id="hg12t"><polygon points="400,12 430,12 418.0,37.0 412.0,37.0"/></clipPath><clipPath id="hg12b"><polygon points="412.0,37.0 418.0,37.0 430,62 400,62"/></clipPath><rect class="sand-b" clip-path="url(#hg12b)" x="400" y="37.0" width="30" height="25.0"/><polygon class="glass" points="400,12 430,12 418.0,37.0 412.0,37.0"/><polygon class="glass" points="412.0,37.0 418.0,37.0 430,62 400,62"/><line class="frame" x1="396" y1="12" x2="434" y2="12"/><line class="frame" x1="396" y1="62" x2="434" y2="62"/><text class="tick" x="437" y="24">0</text><text class="tick" x="437" y="60">11</text><text class="legend" x="415.0" y="77" text-anchor="middle">B</text></svg><figcaption>רגע 11 : שעון B נגמר. בשעון A נשארו 3 דקות למעלה ו-4 למטה; ההיפוך מעלה את 4 הדקות.</figcaption></figure><figure class="stepper-frame"><svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="רגע 15 : A runs out"><text class="legend" x="10" y="33.0" font-weight="700">t = 15</text><text class="tick" x="10" y="51.0">A runs out</text><clipPath id="hg13t"><polygon points="92,12 122,12 110.0,37.0 104.0,37.0"/></clipPath><clipPath id="hg13b"><polygon points="104.0,37.0 110.0,37.0 122,62 92,62"/></clipPath><rect class="sand-a" clip-path="url(#hg13b)" x="92" y="37.0" width="30" height="25.0"/><polygon class="glass" points="92,12 122,12 110.0,37.0 104.0,37.0"/><polygon class="glass" points="104.0,37.0 110.0,37.0 122,62 92,62"/><line class="frame" x1="88" y1="12" x2="126" y2="12"/><line class="frame" x1="88" y1="62" x2="126" y2="62"/><text class="tick" x="129" y="24">0</text><text class="tick" x="129" y="60">7</text><text class="legend" x="107.0" y="77" text-anchor="middle">A</text><clipPath id="hg14t"><polygon points="156,12 186,12 174.0,37.0 168.0,37.0"/></clipPath><clipPath id="hg14b"><polygon points="168.0,37.0 174.0,37.0 186,62 156,62"/></clipPath><rect class="sand-b" clip-path="url(#hg14b)" x="156" y="37.0" width="30" height="25.0"/><polygon class="glass" points="156,12 186,12 174.0,37.0 168.0,37.0"/><polygon class="glass" points="168.0,37.0 174.0,37.0 186,62 156,62"/><line class="frame" x1="152" y1="12" x2="190" y2="12"/><line class="frame" x1="152" y1="62" x2="190" y2="62"/><text class="tick" x="193" y="24">0</text><text class="tick" x="193" y="60">11</text><text class="legend" x="171.0" y="77" text-anchor="middle">B</text><text class="legend" x="226" y="42.0" font-weight="700">✓ D = 15</text></svg><figcaption>רגע 15 : שעון A נגמר. עברו בדיוק 11 + 4 = 15 דקות מרגע 0.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="4"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    | הרגע | מה קרה | חול למעלה לפני (\( A \), \( B \)) | הפעולה | חול למעלה אחרי (\( A \), \( B \)) |
    |:-:|---|:-:|---|:-:|
    | 0 | התחלה | (0, 0) | הופכים את \( A \) ואת \( B \) | (7, 11) |
    | 7 | ‏\( A \) נגמר | (0, 4) | הופכים את \( A \) | (7, 4) |
    | 11 | ‏\( B \) נגמר | (3, 0) | הופכים את \( A \) | (4, 0) |
    | 15 | ‏\( A \) נגמר | (0, 0) | **סיימנו : 15 דקות** | |

    **למה לא כל \( D \) אפשרי?** מרגע 0 אפשר למדוד עם השעונים 7 ו-11 רק את
    \( 7, 11, 14, 15, 17, 18, 19, 20, 21, \ldots \). למשל, את \( D = 4 \) **אי אפשר** למדוד
    מרגע 0, למרות ש-\( 11 - 7 = 4 \) : הפרש בין שני רגעים הוא מדידה שמתחילה ברגע 7, לא
    ברגע 0. בשאלה [0019](../senior/0019-hourglass-measure-interval.md) מרשים גם מדידה כזו.

---

### סעיף ב – האלגוריתם הכללי

כתבו פונקציה שמקבלת \( A \), \( B \) ו-\( D \) ומחזירה **תוכנית פעולה** : לכל רגע שבו
עושים משהו, איזה שעון הופכים. אם אי אפשר למדוד \( D \) מרגע 0, הפונקציה מחזירה "אין פתרון".

??? tip "רמז 1"
    באילו רגעים בכלל אפשר להחליט משהו, כשאין שעון אחר?

??? tip "רמז 2"
    מה **המצב** של המערכת ברגע כזה? כמה מספרים צריך כדי לתאר אותו, וכמה מצבים שונים יש
    בסך הכול?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        המצב הוא \( (t, a, b) \) : הזמן וכמות החול שלמעלה בכל שעון. מחליטים רק כששעון נגמר,
        ובכל החלטה יש ארבע אפשרויות (לא להפוך, \( A \), \( B \), שניהם). מריצים **BFS** מהמצב
        \( (0, 0, 0) \) עד שמוציאים מהתור מצב עם \( t = D \), וגוזמים מצבים שכבר נראו ומצבים
        שעוברים את \( D \).

    <!-- cost: זמן \( O((D + 1)(A + B + 1)) \) | זיכרון \( O((D + 1)(A + B + 1)) \) -->

    #### הרעיון { .sol-idea }

    **מחליטים רק כששעון נגמר.** אין לנו שעון אחר, ולכן הרגעים היחידים שאנחנו "מזהים" הם
    הרגעים שבהם שעון חול נגמר. בין שני רגעים כאלה אין מידע חדש, ואין אפשרות להפוך משהו
    "אחרי 2.5 דקות". לכן התוכנית היא רצף של **אירועים** : בכל אירוע מחליטים מה להפוך, ואז
    מחכים עד שהשעון הבא נגמר.

    **המצב.** ברגע אירוע מספיקים שלושה מספרים \( (t, a, b) \) : הזמן \( t \), כמות החול
    שלמעלה בשעון \( A \) (נסמן \( a \)) וכמות החול שלמעלה בשעון \( B \) (נסמן \( b \)).
    מכל מצב יוצאות **ארבע** אפשרויות : לא להפוך, להפוך את \( A \), להפוך את \( B \), או להפוך
    את שניהם. היפוך של שעון עם \( a \) דקות למעלה משאיר \( A - a \) דקות למעלה. אחרי ההחלטה
    מחכים \( w \) דקות, כאשר \( w \) הוא **המינימום** בין הכמויות החיוביות שלמעלה (השעון
    הראשון שנגמר), ומגיעים למצב :

    \[
    (t + w,\; \max(a' - w, 0),\; \max(b' - w, 0))
    \]

    אם אחרי ההחלטה שני השעונים ריקים למעלה, שום דבר לא יקרה לעולם : האפשרות הזאת נפסלת.
    אם \( t + w > D \), עברנו את \( D \) בלי שאף שעון נגמר בדיוק ברגע \( D \) : גם זה נפסל.

    <svg class="figure hourglass-fig" viewBox="0 0 640 300" role="img" aria-label="ארבע האפשרויות מהמצב t = 7, A = 0, B = 4"><text class="legend" x="320" y="16" text-anchor="middle" font-weight="700">t = 7</text><clipPath id="hg15t"><polygon points="270,26 300,26 288.0,51.0 282.0,51.0"/></clipPath><clipPath id="hg15b"><polygon points="282.0,51.0 288.0,51.0 300,76 270,76"/></clipPath><rect class="sand-a" clip-path="url(#hg15b)" x="270" y="51.0" width="30" height="25.0"/><polygon class="glass" points="270,26 300,26 288.0,51.0 282.0,51.0"/><polygon class="glass" points="282.0,51.0 288.0,51.0 300,76 270,76"/><line class="frame" x1="266" y1="26" x2="304" y2="26"/><line class="frame" x1="266" y1="76" x2="304" y2="76"/><text class="tick" x="307" y="38">0</text><text class="tick" x="307" y="74">7</text><text class="legend" x="285.0" y="91" text-anchor="middle">A</text><clipPath id="hg16t"><polygon points="334,26 364,26 352.0,51.0 346.0,51.0"/></clipPath><clipPath id="hg16b"><polygon points="346.0,51.0 352.0,51.0 364,76 334,76"/></clipPath><rect class="sand-b" clip-path="url(#hg16t)" x="334" y="41.9" width="30" height="9.1"/><line class="stream-b" x1="349.0" y1="51.0" x2="349.0" y2="59.1"/><rect class="sand-b" clip-path="url(#hg16b)" x="334" y="60.1" width="30" height="15.9"/><polygon class="glass" points="334,26 364,26 352.0,51.0 346.0,51.0"/><polygon class="glass" points="346.0,51.0 352.0,51.0 364,76 334,76"/><line class="frame" x1="330" y1="26" x2="368" y2="26"/><line class="frame" x1="330" y1="76" x2="368" y2="76"/><text class="tick" x="371" y="38">4</text><text class="tick" x="371" y="74">7</text><text class="legend" x="349.0" y="91" text-anchor="middle">B</text><g class="pruned"><line class="ink-line" x1="320" y1="104" x2="60" y2="150" stroke-width="1.2"/><text class="legend" x="60" y="170" text-anchor="middle">no flip</text><text class="tick" x="60" y="186" text-anchor="middle">wait 4 → t = 11</text><clipPath id="hg17t"><polygon points="8.0,196 38.0,196 26.0,221.0 20.0,221.0"/></clipPath><clipPath id="hg17b"><polygon points="20.0,221.0 26.0,221.0 38.0,246 8.0,246"/></clipPath><rect class="sand-a" clip-path="url(#hg17b)" x="8.0" y="221.0" width="30" height="25.0"/><polygon class="glass" points="8.0,196 38.0,196 26.0,221.0 20.0,221.0"/><polygon class="glass" points="20.0,221.0 26.0,221.0 38.0,246 8.0,246"/><line class="frame" x1="4.0" y1="196" x2="42.0" y2="196"/><line class="frame" x1="4.0" y1="246" x2="42.0" y2="246"/><text class="tick" x="45.0" y="208">0</text><text class="tick" x="45.0" y="244">7</text><text class="legend" x="23.0" y="261" text-anchor="middle">A</text><clipPath id="hg18t"><polygon points="72.0,196 102.0,196 90.0,221.0 84.0,221.0"/></clipPath><clipPath id="hg18b"><polygon points="84.0,221.0 90.0,221.0 102.0,246 72.0,246"/></clipPath><rect class="sand-b" clip-path="url(#hg18b)" x="72.0" y="221.0" width="30" height="25.0"/><polygon class="glass" points="72.0,196 102.0,196 90.0,221.0 84.0,221.0"/><polygon class="glass" points="84.0,221.0 90.0,221.0 102.0,246 72.0,246"/><line class="frame" x1="68.0" y1="196" x2="106.0" y2="196"/><line class="frame" x1="68.0" y1="246" x2="106.0" y2="246"/><text class="tick" x="109.0" y="208">0</text><text class="tick" x="109.0" y="244">11</text><text class="legend" x="87.0" y="261" text-anchor="middle">B</text><text class="tick" x="60" y="286" text-anchor="middle">seen ✗</text></g><g class="kept"><line class="ink-line" x1="320" y1="104" x2="220" y2="150" stroke-width="1.2"/><text class="legend" x="220" y="170" text-anchor="middle">flip A</text><text class="tick" x="220" y="186" text-anchor="middle">wait 4 → t = 11</text><clipPath id="hg19t"><polygon points="168.0,196 198.0,196 186.0,221.0 180.0,221.0"/></clipPath><clipPath id="hg19b"><polygon points="180.0,221.0 186.0,221.0 198.0,246 168.0,246"/></clipPath><rect class="sand-a" clip-path="url(#hg19t)" x="168.0" y="210.3" width="30" height="10.7"/><line class="stream-a" x1="183.0" y1="221.0" x2="183.0" y2="230.7"/><rect class="sand-a" clip-path="url(#hg19b)" x="168.0" y="231.7" width="30" height="14.3"/><polygon class="glass" points="168.0,196 198.0,196 186.0,221.0 180.0,221.0"/><polygon class="glass" points="180.0,221.0 186.0,221.0 198.0,246 168.0,246"/><line class="frame" x1="164.0" y1="196" x2="202.0" y2="196"/><line class="frame" x1="164.0" y1="246" x2="202.0" y2="246"/><text class="tick" x="205.0" y="208">3</text><text class="tick" x="205.0" y="244">4</text><text class="legend" x="183.0" y="261" text-anchor="middle">A</text><clipPath id="hg20t"><polygon points="232.0,196 262.0,196 250.0,221.0 244.0,221.0"/></clipPath><clipPath id="hg20b"><polygon points="244.0,221.0 250.0,221.0 262.0,246 232.0,246"/></clipPath><rect class="sand-b" clip-path="url(#hg20b)" x="232.0" y="221.0" width="30" height="25.0"/><polygon class="glass" points="232.0,196 262.0,196 250.0,221.0 244.0,221.0"/><polygon class="glass" points="244.0,221.0 250.0,221.0 262.0,246 232.0,246"/><line class="frame" x1="228.0" y1="196" x2="266.0" y2="196"/><line class="frame" x1="228.0" y1="246" x2="266.0" y2="246"/><text class="tick" x="269.0" y="208">0</text><text class="tick" x="269.0" y="244">11</text><text class="legend" x="247.0" y="261" text-anchor="middle">B</text><text class="tick" x="220" y="286" text-anchor="middle">new ✓</text></g><g class="pruned"><line class="ink-line" x1="320" y1="104" x2="380" y2="150" stroke-width="1.2"/><text class="legend" x="380" y="170" text-anchor="middle">flip B</text><text class="tick" x="380" y="186" text-anchor="middle">wait 7 → t = 14</text><clipPath id="hg21t"><polygon points="328.0,196 358.0,196 346.0,221.0 340.0,221.0"/></clipPath><clipPath id="hg21b"><polygon points="340.0,221.0 346.0,221.0 358.0,246 328.0,246"/></clipPath><rect class="sand-a" clip-path="url(#hg21b)" x="328.0" y="221.0" width="30" height="25.0"/><polygon class="glass" points="328.0,196 358.0,196 346.0,221.0 340.0,221.0"/><polygon class="glass" points="340.0,221.0 346.0,221.0 358.0,246 328.0,246"/><line class="frame" x1="324.0" y1="196" x2="362.0" y2="196"/><line class="frame" x1="324.0" y1="246" x2="362.0" y2="246"/><text class="tick" x="365.0" y="208">0</text><text class="tick" x="365.0" y="244">7</text><text class="legend" x="343.0" y="261" text-anchor="middle">A</text><clipPath id="hg22t"><polygon points="392.0,196 422.0,196 410.0,221.0 404.0,221.0"/></clipPath><clipPath id="hg22b"><polygon points="404.0,221.0 410.0,221.0 422.0,246 392.0,246"/></clipPath><rect class="sand-b" clip-path="url(#hg22b)" x="392.0" y="221.0" width="30" height="25.0"/><polygon class="glass" points="392.0,196 422.0,196 410.0,221.0 404.0,221.0"/><polygon class="glass" points="404.0,221.0 410.0,221.0 422.0,246 392.0,246"/><line class="frame" x1="388.0" y1="196" x2="426.0" y2="196"/><line class="frame" x1="388.0" y1="246" x2="426.0" y2="246"/><text class="tick" x="429.0" y="208">0</text><text class="tick" x="429.0" y="244">11</text><text class="legend" x="407.0" y="261" text-anchor="middle">B</text><text class="tick" x="380" y="286" text-anchor="middle">seen ✗</text></g><g class="pruned"><line class="ink-line" x1="320" y1="104" x2="540" y2="150" stroke-width="1.2"/><text class="legend" x="540" y="170" text-anchor="middle">flip A + B</text><text class="tick" x="540" y="186" text-anchor="middle">wait 7 → t = 14</text><clipPath id="hg23t"><polygon points="488.0,196 518.0,196 506.0,221.0 500.0,221.0"/></clipPath><clipPath id="hg23b"><polygon points="500.0,221.0 506.0,221.0 518.0,246 488.0,246"/></clipPath><rect class="sand-a" clip-path="url(#hg23b)" x="488.0" y="221.0" width="30" height="25.0"/><polygon class="glass" points="488.0,196 518.0,196 506.0,221.0 500.0,221.0"/><polygon class="glass" points="500.0,221.0 506.0,221.0 518.0,246 488.0,246"/><line class="frame" x1="484.0" y1="196" x2="522.0" y2="196"/><line class="frame" x1="484.0" y1="246" x2="522.0" y2="246"/><text class="tick" x="525.0" y="208">0</text><text class="tick" x="525.0" y="244">7</text><text class="legend" x="503.0" y="261" text-anchor="middle">A</text><clipPath id="hg24t"><polygon points="552.0,196 582.0,196 570.0,221.0 564.0,221.0"/></clipPath><clipPath id="hg24b"><polygon points="564.0,221.0 570.0,221.0 582.0,246 552.0,246"/></clipPath><rect class="sand-b" clip-path="url(#hg24b)" x="552.0" y="221.0" width="30" height="25.0"/><polygon class="glass" points="552.0,196 582.0,196 570.0,221.0 564.0,221.0"/><polygon class="glass" points="564.0,221.0 570.0,221.0 582.0,246 552.0,246"/><line class="frame" x1="548.0" y1="196" x2="586.0" y2="196"/><line class="frame" x1="548.0" y1="246" x2="586.0" y2="246"/><text class="tick" x="589.0" y="208">0</text><text class="tick" x="589.0" y="244">11</text><text class="legend" x="567.0" y="261" text-anchor="middle">B</text><text class="tick" x="540" y="286" text-anchor="middle">seen ✗</text></g></svg>

    באיור : מהמצב \( (7, 0, 4) \) יוצאים ארבעה מצבים. שלושה מהם כבר התגלו בדרך אחרת (למשל
    \( (11, 0, 0) \) מתקבל גם כשהופכים רק את \( B \) ברגע 0), ולכן נגזמים. רק
    \( (11, 3, 0) \) חדש, והוא זה שמוביל לפתרון.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **אתחול :** התור מכיל את \( (0, 0, 0) \) עם תוכנית ריקה, ו-`seen` מכיל אותו.
    2. **הוצאה מהתור :** מוציאים מצב. אם \( t = D \), התוכנית שלו היא התשובה.
    3. **ארבע אפשרויות :** לכל בחירה של היפוכים מחשבים את החול למעלה אחרי ההיפוך, את
       ההמתנה \( w \) ואת המצב הבא. פוסלים "שום דבר לא רץ" ו-\( t + w > D \).
    4. **גיזום והכנסה :** מצב שלא נראה נכנס לתור עם התוכנית הקודמת ועוד הפעולה הנוכחית
       ברגע \( t \).
    5. **סיום :** אם התור התרוקן, אי אפשר למדוד \( D \) מרגע 0.

    </div>

    #### הקוד { .sol-code }

    הפונקציה מחזירה את התוכנית כמיפוי מרגע לפעולה. ב-Python זה מילון `{0: 'AB', 7: 'A', 11: 'A'}`,
    וב-SystemVerilog מחרוזת `"0:AB 7:A 11:A"`. פעולה ריקה (`''` ב-Python, `-` ב-SystemVerilog)
    פירושה "לא להפוך כלום, רק לחכות לשעון הבא".

    === "Python"
        ```python title="solve" linenums="1" hl_lines="18 23 27"
        from collections import deque


        def solve(A, B, D):
            """Return {time: action} for a plan that ends exactly at D, or None."""
            # State: (time, sand on top of A, sand on top of B). At t=0 all sand is at the bottom.
            start = (0, 0, 0)
            queue = deque([(start, {})])
            seen = {start}

            while queue:
                (t, a, b), plan = queue.popleft()
                if t == D:
                    return plan

                for flip_a in (False, True):
                    for flip_b in (False, True):
                        a2 = A - a if flip_a else a   # (1)!
                        b2 = B - b if flip_b else b
                        running = [sand for sand in (a2, b2) if sand > 0]
                        if not running:
                            continue                # nothing flows, nothing will happen
                        wait = min(running)         # until the next hourglass runs out (2)
                        if t + wait > D:
                            continue                # would overshoot D

                        new_state = (t + wait, max(a2 - wait, 0), max(b2 - wait, 0))
                        if new_state not in seen:   # (3)!
                            seen.add(new_state)
                            action = ("A" if flip_a else "") + ("B" if flip_b else "")
                            queue.append((new_state, {**plan, t: action}))
            return None
        ```

        1. היפוך : החול שלמעלה הופך להיות \( A - a \). בלי היפוך הכמות נשארת.
        2. ההמתנה היא המינימום בין הכמויות **החיוביות** שלמעלה : שעון ריק למעלה לא משתתף.
        3. הגיזום : מצב שכבר נראה לא נכנס שוב. בלי זה החיפוש עדיין מסתיים (כי \( t \) גדל
           בכל צעד ונחסם על ידי \( D \)), אבל הוא אקספוננציאלי.

    === "SystemVerilog"
        ```systemverilog title="function measure_from_zero" linenums="1" hl_lines="27 30 32"
        typedef struct { int t; int a; int b; } hg_state_t;   // time, sand on top of A, sand on top of B

        // Returns 1 and fills `plan` (e.g. "0:AB 7:A 11:A") when D can be measured from time 0.
        // A token "t:X" means: at time t flip A, B, both (AB) or nothing (-), then wait.
        function automatic bit measure_from_zero(int A, int B, int D, output string plan);
          hg_state_t queue[$];
          string     plans[$];               // plan of each queued state, same order
          bit        seen[string];           // (1)!
          hg_state_t s, n;
          string     p, key, action;
          int        a2, b2, delay;          // (2)!

          s = '{0, 0, 0};                    // at t=0 all sand is at the bottom
          queue.push_back(s);
          plans.push_back("");
          seen["0,0,0"] = 1;

          while (queue.size() > 0) begin
            s = queue.pop_front();
            p = plans.pop_front();
            if (s.t == D) begin
              plan = p;
              return 1;
            end
            for (int flip_a = 0; flip_a <= 1; flip_a++)
              for (int flip_b = 0; flip_b <= 1; flip_b++) begin
                a2 = flip_a ? A - s.a : s.a;   // (3)!
                b2 = flip_b ? B - s.b : s.b;
                if (a2 == 0 && b2 == 0) continue;            // nothing flows, nothing will happen
                delay = (a2 == 0) ? b2 : (b2 == 0) ? a2 : (a2 < b2 ? a2 : b2);   // (4)!
                if (s.t + delay > D) continue;               // would overshoot D
                n = '{s.t + delay, (a2 > delay) ? a2 - delay : 0, (b2 > delay) ? b2 - delay : 0};
                key = $sformatf("%0d,%0d,%0d", n.t, n.a, n.b);
                if (!seen.exists(key)) begin
                  seen[key] = 1;
                  action = {flip_a ? "A" : "", flip_b ? "B" : ""};
                  if (action == "") action = "-";
                  queue.push_back(n);
                  plans.push_back({p, (p == "") ? "" : " ", $sformatf("%0d:%s", s.t, action)});
                end
              end
          end
          return 0;
        endfunction
        ```

        1. המצבים שכבר נראו נשמרים במערך אסוציאטיבי עם מפתח מחרוזת `"t,a,b"`, כי מפתח
           מסוג struct לא נתמך בכל הסימולטורים.
        2. המילה `wait` היא מילה שמורה ב-SystemVerilog (ההצהרה `wait(...)`), ולכן זמן
           ההמתנה נקרא כאן `delay`.
        3. היפוך : החול שלמעלה הופך להיות \( A - a \). בלי היפוך הכמות נשארת.
        4. ההמתנה היא המינימום בין הכמויות **החיוביות** שלמעלה : שעון ריק למעלה לא משתתף.

    #### למה זה נכון { .sol-proof }

    **החיפוש מסתיים ושלם.** מרחב המצבים **סופי** : \( 0 \le t \le D \), \( 0 \le a \le A \),
    \( 0 \le b \le B \). למעשה הוא קטן יותר : בכל אירוע לפחות שעון אחד בדיוק נגמר, ולכן
    \( a = 0 \) או \( b = 0 \), כלומר יש לכל היותר \( (D + 1)(A + B + 1) \) מצבים. BFS מבקר
    בכל מצב שאפשר להגיע אליו, ולכן אם קיימת תוכנית הוא מוצא אותה, ואם התור התרוקן אין
    תוכנית.

    **העץ עבור הדוגמה.** בכל צומת : הזמן והחול שלמעלה בשני השעונים. צמתים מקווקווים נגזמו
    (המצב כבר נראה, או שעוברים את \( D \)). הסדר שבו הקוד בודק את האפשרויות הוא : לא
    להפוך, \( B \), \( A \), שניהם.

    ```mermaid
    flowchart TD
        s0["t=0<br/>A=0, B=0"]
        s0 -- "B" --> s1["t=11<br/>A=0, B=0"]
        s0 -- "A" --> s2["t=7<br/>A=0, B=0"]
        s0 -- "AB" --> s3["t=7<br/>A=0, B=4"]
        s1 -- "A / B / AB" --> x1["> 15 ✗"]
        s2 -- "A" --> s4["t=14<br/>A=0, B=0"]
        s2 -- "AB" --> s5["t=14<br/>A=0, B=4"]
        s3 -- "wait / B / AB" --> x2["seen ✗"]
        s3 -- "A" --> s6["t=11<br/>A=3, B=0"]
        s4 -- "A / B / AB" --> x3["> 15 ✗"]
        s5 -- "any" --> x4["> 15 ✗"]
        s6 -- "wait" --> x5["seen ✗"]
        s6 -- "B" --> s7["t=14<br/>A=0, B=8"]
        s6 -- "A" --> s8["t=15<br/>A=0, B=0 ✓"]
        s6 -- "AB" --> s9["t=15<br/>A=0, B=7"]
        s7 -- "any" --> x6["> 15 ✗"]
        classDef pruned stroke-dasharray: 5 4,opacity:0.6;
        classDef found stroke:currentColor,stroke-width:3px;
        class x1,x2,x3,x4,x5,x6 pruned;
        class s8 found;
    ```

    **המעקב אחרי התור.** כל שורה היא הוצאה אחת מהתור :

    | # | המצב שיצא | התוכנית עד כאן | מצבים חדשים שנכנסים לתור |
    |:-:|:-:|---|---|
    | 1 | (0, 0, 0) | | (11, 0, 0) דרך \( B \); (7, 0, 0) דרך \( A \); (7, 0, 4) דרך \( AB \) |
    | 2 | (11, 0, 0) | 0 : \( B \) | אין : כל אפשרות עוברת את 15 |
    | 3 | (7, 0, 0) | 0 : \( A \) | (14, 0, 0) דרך \( A \); (14, 0, 4) דרך \( AB \) |
    | 4 | (7, 0, 4) | 0 : \( AB \) | (11, 3, 0) דרך \( A \); השאר כבר נראו |
    | 5 | (14, 0, 0) | 0 : \( A \), 7 : \( A \) | אין |
    | 6 | (14, 0, 4) | 0 : \( A \), 7 : \( AB \) | אין |
    | 7 | (11, 3, 0) | 0 : \( AB \), 7 : \( A \) | (14, 0, 8) דרך \( B \); **(15, 0, 0) דרך \( A \)**; (15, 0, 7) דרך \( AB \) |
    | 8 | (14, 0, 8) | 0 : \( AB \), 7 : \( A \), 11 : \( B \) | אין |
    | 9 | **(15, 0, 0)** | 0 : \( AB \), 7 : \( A \), 11 : \( A \) | ‏\( t = D \) : **מצאנו** |

    #### סיבוכיות { .sol-cost }

    - **זמן :** כל מצב נכנס לתור לכל היותר פעם אחת, ומכל מצב בודקים 4 אפשרויות, ולכן
      \( O\big((D + 1)(A + B + 1)\big) \). בדוגמה ה-BFS הוציא מהתור רק 9 מצבים.
    - **זיכרון :** אותו סדר גודל, ל-`seen` ולתור.
    - **איזו תוכנית מתקבלת :** BFS מוצא את התוכנית עם **מספר האירועים הקטן ביותר** (כל קשת
      בעץ היא אירוע אחד). זה לא בהכרח מספר ההיפוכים הקטן ביותר : כדי למזער היפוכים צריך
      לתת לכל קשת משקל, וזה כבר Dijkstra, כמו בשאלה
      [0019](../senior/0019-hourglass-measure-interval.md).

    **נסו בעצמכם.** בחרו שני שעונים ומטרה : ה-BFS רץ בדפדפן ומראה את התוכנית על ציר הזמן,
    עם האותיות של השעונים שהופכים בכל אירוע, ואת האירועים אחד אחד עם שני השעונים לפני
    הפעולה ואחריה. כשאי אפשר למדוד את \( D \) מרגע 0, הסיכום אומר אילו ערכים כן אפשר.
    שתי שאלות ההמשך גם כאן : שדה \( C \) מוסיף שעון שלישי (המצב גדל ל-\( (t, a, b, c) \),
    8 אפשרויות בכל אירוע), ובורר המטרה מחליף את "הכי מעט אירועים" ב"הכי מעט היפוכים",
    עם שורה שמשווה בין שתי המטרות. בשלב ההוכחה, בתחתית התיבה, "השליפה הבאה" מריץ את ה-BFS
    של העמוד מצב אחרי מצב : המצב שיוצא מהתור, ארבעת הילדים שלו (חדש, כבר נמצא או אחרי
    \( D \)), התור עצמו ועץ החיפוש, עד שהמטרה יוצאת מהתור :

    <div class="explorer" data-kind="hourglass" data-mode="zero" data-a="7" data-b="11" data-d="15"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לשכוח שאפשר להפוך שעון באמצע"
    מי שמתיר רק היפוך של שעון שנגמר יכול למדוד רק סכומים של ריצות שלמות, ולא ימצא את
    15 עם 7 ו-11. ההיפוך באמצע הריצה הוא הכלי שמייצר "שעונים" חדשים (4 דקות בדוגמה),
    וצריך להציע אותו בעצמכם.

??? trap "מלכודת : להפוך 'אחרי 3 דקות'"
    תוכנית שאומרת "להפוך את \( B \) שלוש דקות אחרי ההתחלה" לא ניתנת לביצוע : אין לנו איך
    לדעת מתי עברו שלוש דקות. כל פעולה חייבת להיות צמודה לאירוע, ולכן המודל מחליט רק
    כששעון נגמר.

??? trap "מלכודת : לוותר על 'לא להפוך כלום'"
    כשמודדים מרגע 0 האפשרות "רק לחכות" נראית מיותרת, ובכל המקרים שהבדיקות האוטומטיות
    מריצות (\( A, B \le 11 \), \( D < 25 \)) התוכנית שנמצאת אכן לא כוללת המתנה בלבד, כי המצב
    שמגיעים אליו בהמתנה מתגלה גם בדרך אחרת. בשאלה 0019 היא הכרחית : ברגע 21 מחכים בלי
    להפוך כלום. עדיף לכלול אותה תמיד ולתת ל-`seen` לגזום.

??? followup "שאלות המשך"
    - **שלושה שעונים :** מה משתנה?

        ??? fu-answer "תשובה"
            המצב גדל ל-\( (t, a, b, c) \), ויש 8 אפשרויות היפוך בכל אירוע. ההמתנה היא המינימום
            בין הכמויות החיוביות שלמעלה בשלושת השעונים, והשאר אותו BFS.

    - **אילו \( D \) בכלל אפשריים?**

        ??? fu-answer "תשובה"
            רק כפולות של \( \gcd(A, B) \), כי כל רגע של אירוע הוא צירוף שלם של \( A \) ו-\( B \),
            ולא כולן : עם 7 ו-11 אי אפשר למדוד מרגע 0 את 1 עד 6, 8 עד 10, 12, 13 ו-16. מ-17
            והלאה כל \( D \) אפשרי.

    - **מדידה שלא מתחילה ברגע 0 :** איך משתנים המצב והאלגוריתם? זו שאלה
      [0019](../senior/0019-hourglass-measure-interval.md).

        ??? fu-answer "תשובה"
            הזמן עובר מהמצב אל המחיר : המצב הוא \( (a, b, m) \), כש-\( m \) הוא כמה נמדד (<span dir="ltr">−1</span>
            לפני ההתחלה), ונוספת קשת "מתחילים למדוד" במחיר 0. במקום BFS מריצים Dijkstra לפי
            הזמן, כדי למצוא את המדידה שמסתיימת הכי מוקדם.

    - **מספר היפוכים מינימלי :** איך משנים את החיפוש כך שימזער היפוכים ולא אירועים?

        ??? fu-answer "תשובה"
            נותנים לכל קשת משקל השווה למספר השעונים שהופכים בה (0, 1 או 2), ומריצים Dijkstra
            על אותם מצבים \( (t, a, b) \). הזמן נשאר במצב, כי הוא חלק מהמטרה \( t = D \).
