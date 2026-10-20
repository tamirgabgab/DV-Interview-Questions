---
id: 19
title: שני שעוני חול – מדידת D דקות בין שני רגעים
level: senior
difficulty: hard
tags: [algorithms, dijkstra, bfs, logic-puzzles, python, systemverilog]
source: ""
added: 2026-10-18
---

## השאלה

כמו בשאלה [0018](../junior/0018-hourglass-measure-from-zero.md): שני שעוני חול של \( A \)
ו-\( B \) דקות, ובכל רגע אפשר להפוך כל אחד מהם, גם באמצע הריצה. ההבדל: המדידה **לא חייבת
להתחיל ברגע 0**. מותר להכריז "מתחילים למדוד" ברגע \( t_1 \) שבו שעון נגמר, ולסיים ברגע
‏\( t_2 \) שבו שעון נגמר, כך ש-\( t_2 - t_1 = D \).

מבין כל התוכניות האפשריות מחפשים את זו שבה המדידה **מסתיימת הכי מוקדם** (\( t_2 \) מינימלי),
כי זה הזמן הכולל שמי שמודד צריך לחכות.

??? interviewer "מה המראיין בודק"
    - **הפרש בין שני רגעים:** האם המועמד מזהה שמדידה היא הפרש בין שני אירועים באותה
      ריצה, ולא בהכרח סכום מרגע 0.
    - **מה משתנה לעומת 0018:** האם הוא רואה שהזמן עבר מהמטרה אל המחיר, ושהקשתות כבר לא
      שוות, ולכן BFS לא מספיק.
    - **בחירת המצב:** מה נכנס למצב ומה יוצא ממנו כדי שהחיפוש יסתיים ועדיין ימצא את
      המינימום.
    - **‏Dijkstra בפועל:** תור עדיפויות, קשת במחיר 0, רשומות ישנות, ואיך משחזרים את
      התוכנית.

---

### סעיף א – דוגמה: A = 7, B = 11, D = 1

מצאו איך למדוד **דקה אחת** עם שעוני חול של 7 ו-11 דקות. מתי המדידה מתחילה, מתי היא
מסתיימת, ומה עושים בדרך?

??? tip "רמז 1"
    מרגע 0 אי אפשר: השעון הראשון נגמר רק ברגע 7. חפשו שני רגעים שבהם שעונים נגמרים,
    **באותה ריצה**, בהפרש של דקה.

??? tip "רמז 2"
    חשבו על כפולות של 7 ושל 11. איזה זוג כפולות נבדל בדקה אחת?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        נותנים ל-\( A \) לרוץ שלוש פעמים ברצף (נגמר ברגע 21) ול-\( B \) פעמיים ברצף (נגמר
        ברגע 22), שניהם מרגע 0. מתחילים למדוד ברגע 21 ומסיימים ברגע 22:
        \( 1 = 2 \cdot 11 - 3 \cdot 7 \).

    #### הרעיון { .sol-idea }

    שעון שהופכים מיד בכל פעם שהוא נגמר, נגמר בכפולות של אורכו: \( A \) ברגעים 7, 14, 21
    ו-\( B \) ברגעים 11, 22. שני הרצפים האלה קורים **באותה ריצה**, ולכן כל הפרש בין רגע
    מהרצף האחד לרגע מהרצף השני הוא מדידה אפשרית. השוויון \( 2 \cdot 11 - 3 \cdot 7 = 1 \)
    נותן את הדקה: מרגע 21 (\( A \) נגמר בפעם השלישית) עד רגע 22 (\( B \) נגמר בפעם השנייה).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **רגע 0:** הופכים את שני השעונים.
    2. **רגע 7:** שעון \( A \) נגמר, הופכים אותו.
    3. **רגע 11:** שעון \( B \) נגמר, הופכים אותו.
    4. **רגע 14:** שעון \( A \) נגמר, הופכים אותו.
    5. **רגע 21:** שעון \( A \) נגמר. ב-\( B \) נשארה בדיוק דקה למעלה: **מתחילים למדוד**, לא
       הופכים כלום.
    6. **רגע 22:** שעון \( B \) נגמר: **מסיימים**. נמדדה דקה אחת.

    </div>

    #### למה זה נכון { .sol-proof }

    **אירוע אחרי אירוע.** לחצו "הבא" כדי לעקוב. שני האירועים האחרונים, חלון המדידה,
    מסומנים במסגרת:

    <div class="stepper" role="group" aria-label="התוכנית למדידת דקה אחת עם שעוני חול של 7 ו-11 דקות: המדידה מרגע 21 עד רגע 22" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="רגע 0: start"><text class="legend" x="10" y="33.0" font-weight="700">t = 0</text><text class="tick" x="10" y="51.0">start</text><clipPath id="hg1t"><polygon points="92,12 122,12 110.0,37.0 104.0,37.0"/></clipPath><clipPath id="hg1b"><polygon points="104.0,37.0 110.0,37.0 122,62 92,62"/></clipPath><rect class="sand-a" clip-path="url(#hg1b)" x="92" y="37.0" width="30" height="25.0"/><polygon class="glass" points="92,12 122,12 110.0,37.0 104.0,37.0"/><polygon class="glass" points="104.0,37.0 110.0,37.0 122,62 92,62"/><line class="frame" x1="88" y1="12" x2="126" y2="12"/><line class="frame" x1="88" y1="62" x2="126" y2="62"/><text class="tick" x="129" y="24">0</text><text class="tick" x="129" y="60">7</text><text class="legend" x="107.0" y="77" text-anchor="middle">A</text><clipPath id="hg2t"><polygon points="156,12 186,12 174.0,37.0 168.0,37.0"/></clipPath><clipPath id="hg2b"><polygon points="168.0,37.0 174.0,37.0 186,62 156,62"/></clipPath><rect class="sand-b" clip-path="url(#hg2b)" x="156" y="37.0" width="30" height="25.0"/><polygon class="glass" points="156,12 186,12 174.0,37.0 168.0,37.0"/><polygon class="glass" points="168.0,37.0 174.0,37.0 186,62 156,62"/><line class="frame" x1="152" y1="12" x2="190" y2="12"/><line class="frame" x1="152" y1="62" x2="190" y2="62"/><text class="tick" x="193" y="24">0</text><text class="tick" x="193" y="60">11</text><text class="legend" x="171.0" y="77" text-anchor="middle">B</text><line class="ink-line" x1="222" y1="37.0" x2="306" y2="37.0" stroke-width="1.5"/><polygon class="ink-fill" points="312,37.0 304,33.0 304,41.0"/><text class="legend" x="267" y="29.0" text-anchor="middle">flip A + B</text><clipPath id="hg3t"><polygon points="336,12 366,12 354.0,37.0 348.0,37.0"/></clipPath><clipPath id="hg3b"><polygon points="348.0,37.0 354.0,37.0 366,62 336,62"/></clipPath><rect class="sand-a" clip-path="url(#hg3t)" x="336" y="12.0" width="30" height="25.0"/><line class="stream-a" x1="351.0" y1="37.0" x2="351.0" y2="61.0"/><polygon class="glass" points="336,12 366,12 354.0,37.0 348.0,37.0"/><polygon class="glass" points="348.0,37.0 354.0,37.0 366,62 336,62"/><line class="frame" x1="332" y1="12" x2="370" y2="12"/><line class="frame" x1="332" y1="62" x2="370" y2="62"/><text class="tick" x="373" y="24">7</text><text class="tick" x="373" y="60">0</text><text class="legend" x="351.0" y="77" text-anchor="middle">A</text><clipPath id="hg4t"><polygon points="400,12 430,12 418.0,37.0 412.0,37.0"/></clipPath><clipPath id="hg4b"><polygon points="412.0,37.0 418.0,37.0 430,62 400,62"/></clipPath><rect class="sand-b" clip-path="url(#hg4t)" x="400" y="12.0" width="30" height="25.0"/><line class="stream-b" x1="415.0" y1="37.0" x2="415.0" y2="61.0"/><polygon class="glass" points="400,12 430,12 418.0,37.0 412.0,37.0"/><polygon class="glass" points="412.0,37.0 418.0,37.0 430,62 400,62"/><line class="frame" x1="396" y1="12" x2="434" y2="12"/><line class="frame" x1="396" y1="62" x2="434" y2="62"/><text class="tick" x="437" y="24">11</text><text class="tick" x="437" y="60">0</text><text class="legend" x="415.0" y="77" text-anchor="middle">B</text></svg><figcaption>רגע 0: הופכים את שני השעונים.</figcaption></figure><figure class="stepper-frame"><svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="רגע 7: A runs out"><text class="legend" x="10" y="33.0" font-weight="700">t = 7</text><text class="tick" x="10" y="51.0">A runs out</text><clipPath id="hg5t"><polygon points="92,12 122,12 110.0,37.0 104.0,37.0"/></clipPath><clipPath id="hg5b"><polygon points="104.0,37.0 110.0,37.0 122,62 92,62"/></clipPath><rect class="sand-a" clip-path="url(#hg5b)" x="92" y="37.0" width="30" height="25.0"/><polygon class="glass" points="92,12 122,12 110.0,37.0 104.0,37.0"/><polygon class="glass" points="104.0,37.0 110.0,37.0 122,62 92,62"/><line class="frame" x1="88" y1="12" x2="126" y2="12"/><line class="frame" x1="88" y1="62" x2="126" y2="62"/><text class="tick" x="129" y="24">0</text><text class="tick" x="129" y="60">7</text><text class="legend" x="107.0" y="77" text-anchor="middle">A</text><clipPath id="hg6t"><polygon points="156,12 186,12 174.0,37.0 168.0,37.0"/></clipPath><clipPath id="hg6b"><polygon points="168.0,37.0 174.0,37.0 186,62 156,62"/></clipPath><rect class="sand-b" clip-path="url(#hg6t)" x="156" y="27.9" width="30" height="9.1"/><line class="stream-b" x1="171.0" y1="37.0" x2="171.0" y2="45.1"/><rect class="sand-b" clip-path="url(#hg6b)" x="156" y="46.1" width="30" height="15.9"/><polygon class="glass" points="156,12 186,12 174.0,37.0 168.0,37.0"/><polygon class="glass" points="168.0,37.0 174.0,37.0 186,62 156,62"/><line class="frame" x1="152" y1="12" x2="190" y2="12"/><line class="frame" x1="152" y1="62" x2="190" y2="62"/><text class="tick" x="193" y="24">4</text><text class="tick" x="193" y="60">7</text><text class="legend" x="171.0" y="77" text-anchor="middle">B</text><line class="ink-line" x1="222" y1="37.0" x2="306" y2="37.0" stroke-width="1.5"/><polygon class="ink-fill" points="312,37.0 304,33.0 304,41.0"/><text class="legend" x="267" y="29.0" text-anchor="middle">flip A</text><clipPath id="hg7t"><polygon points="336,12 366,12 354.0,37.0 348.0,37.0"/></clipPath><clipPath id="hg7b"><polygon points="348.0,37.0 354.0,37.0 366,62 336,62"/></clipPath><rect class="sand-a" clip-path="url(#hg7t)" x="336" y="12.0" width="30" height="25.0"/><line class="stream-a" x1="351.0" y1="37.0" x2="351.0" y2="61.0"/><polygon class="glass" points="336,12 366,12 354.0,37.0 348.0,37.0"/><polygon class="glass" points="348.0,37.0 354.0,37.0 366,62 336,62"/><line class="frame" x1="332" y1="12" x2="370" y2="12"/><line class="frame" x1="332" y1="62" x2="370" y2="62"/><text class="tick" x="373" y="24">7</text><text class="tick" x="373" y="60">0</text><text class="legend" x="351.0" y="77" text-anchor="middle">A</text><clipPath id="hg8t"><polygon points="400,12 430,12 418.0,37.0 412.0,37.0"/></clipPath><clipPath id="hg8b"><polygon points="412.0,37.0 418.0,37.0 430,62 400,62"/></clipPath><rect class="sand-b" clip-path="url(#hg8t)" x="400" y="27.9" width="30" height="9.1"/><line class="stream-b" x1="415.0" y1="37.0" x2="415.0" y2="45.1"/><rect class="sand-b" clip-path="url(#hg8b)" x="400" y="46.1" width="30" height="15.9"/><polygon class="glass" points="400,12 430,12 418.0,37.0 412.0,37.0"/><polygon class="glass" points="412.0,37.0 418.0,37.0 430,62 400,62"/><line class="frame" x1="396" y1="12" x2="434" y2="12"/><line class="frame" x1="396" y1="62" x2="434" y2="62"/><text class="tick" x="437" y="24">4</text><text class="tick" x="437" y="60">7</text><text class="legend" x="415.0" y="77" text-anchor="middle">B</text></svg><figcaption>רגע 7: שעון A נגמר והופכים אותו. ריצה שנייה של A מתחילה.</figcaption></figure><figure class="stepper-frame"><svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="רגע 11: B runs out"><text class="legend" x="10" y="33.0" font-weight="700">t = 11</text><text class="tick" x="10" y="51.0">B runs out</text><clipPath id="hg9t"><polygon points="92,12 122,12 110.0,37.0 104.0,37.0"/></clipPath><clipPath id="hg9b"><polygon points="104.0,37.0 110.0,37.0 122,62 92,62"/></clipPath><rect class="sand-a" clip-path="url(#hg9t)" x="92" y="26.3" width="30" height="10.7"/><line class="stream-a" x1="107.0" y1="37.0" x2="107.0" y2="46.7"/><rect class="sand-a" clip-path="url(#hg9b)" x="92" y="47.7" width="30" height="14.3"/><polygon class="glass" points="92,12 122,12 110.0,37.0 104.0,37.0"/><polygon class="glass" points="104.0,37.0 110.0,37.0 122,62 92,62"/><line class="frame" x1="88" y1="12" x2="126" y2="12"/><line class="frame" x1="88" y1="62" x2="126" y2="62"/><text class="tick" x="129" y="24">3</text><text class="tick" x="129" y="60">4</text><text class="legend" x="107.0" y="77" text-anchor="middle">A</text><clipPath id="hg10t"><polygon points="156,12 186,12 174.0,37.0 168.0,37.0"/></clipPath><clipPath id="hg10b"><polygon points="168.0,37.0 174.0,37.0 186,62 156,62"/></clipPath><rect class="sand-b" clip-path="url(#hg10b)" x="156" y="37.0" width="30" height="25.0"/><polygon class="glass" points="156,12 186,12 174.0,37.0 168.0,37.0"/><polygon class="glass" points="168.0,37.0 174.0,37.0 186,62 156,62"/><line class="frame" x1="152" y1="12" x2="190" y2="12"/><line class="frame" x1="152" y1="62" x2="190" y2="62"/><text class="tick" x="193" y="24">0</text><text class="tick" x="193" y="60">11</text><text class="legend" x="171.0" y="77" text-anchor="middle">B</text><line class="ink-line" x1="222" y1="37.0" x2="306" y2="37.0" stroke-width="1.5"/><polygon class="ink-fill" points="312,37.0 304,33.0 304,41.0"/><text class="legend" x="267" y="29.0" text-anchor="middle">flip B</text><clipPath id="hg11t"><polygon points="336,12 366,12 354.0,37.0 348.0,37.0"/></clipPath><clipPath id="hg11b"><polygon points="348.0,37.0 354.0,37.0 366,62 336,62"/></clipPath><rect class="sand-a" clip-path="url(#hg11t)" x="336" y="26.3" width="30" height="10.7"/><line class="stream-a" x1="351.0" y1="37.0" x2="351.0" y2="46.7"/><rect class="sand-a" clip-path="url(#hg11b)" x="336" y="47.7" width="30" height="14.3"/><polygon class="glass" points="336,12 366,12 354.0,37.0 348.0,37.0"/><polygon class="glass" points="348.0,37.0 354.0,37.0 366,62 336,62"/><line class="frame" x1="332" y1="12" x2="370" y2="12"/><line class="frame" x1="332" y1="62" x2="370" y2="62"/><text class="tick" x="373" y="24">3</text><text class="tick" x="373" y="60">4</text><text class="legend" x="351.0" y="77" text-anchor="middle">A</text><clipPath id="hg12t"><polygon points="400,12 430,12 418.0,37.0 412.0,37.0"/></clipPath><clipPath id="hg12b"><polygon points="412.0,37.0 418.0,37.0 430,62 400,62"/></clipPath><rect class="sand-b" clip-path="url(#hg12t)" x="400" y="12.0" width="30" height="25.0"/><line class="stream-b" x1="415.0" y1="37.0" x2="415.0" y2="61.0"/><polygon class="glass" points="400,12 430,12 418.0,37.0 412.0,37.0"/><polygon class="glass" points="412.0,37.0 418.0,37.0 430,62 400,62"/><line class="frame" x1="396" y1="12" x2="434" y2="12"/><line class="frame" x1="396" y1="62" x2="434" y2="62"/><text class="tick" x="437" y="24">11</text><text class="tick" x="437" y="60">0</text><text class="legend" x="415.0" y="77" text-anchor="middle">B</text></svg><figcaption>רגע 11: שעון B נגמר והופכים אותו. ריצה שנייה של B מתחילה; ב-A נשארו 3 דקות.</figcaption></figure><figure class="stepper-frame"><svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="רגע 14: A runs out"><text class="legend" x="10" y="33.0" font-weight="700">t = 14</text><text class="tick" x="10" y="51.0">A runs out</text><clipPath id="hg13t"><polygon points="92,12 122,12 110.0,37.0 104.0,37.0"/></clipPath><clipPath id="hg13b"><polygon points="104.0,37.0 110.0,37.0 122,62 92,62"/></clipPath><rect class="sand-a" clip-path="url(#hg13b)" x="92" y="37.0" width="30" height="25.0"/><polygon class="glass" points="92,12 122,12 110.0,37.0 104.0,37.0"/><polygon class="glass" points="104.0,37.0 110.0,37.0 122,62 92,62"/><line class="frame" x1="88" y1="12" x2="126" y2="12"/><line class="frame" x1="88" y1="62" x2="126" y2="62"/><text class="tick" x="129" y="24">0</text><text class="tick" x="129" y="60">7</text><text class="legend" x="107.0" y="77" text-anchor="middle">A</text><clipPath id="hg14t"><polygon points="156,12 186,12 174.0,37.0 168.0,37.0"/></clipPath><clipPath id="hg14b"><polygon points="168.0,37.0 174.0,37.0 186,62 156,62"/></clipPath><rect class="sand-b" clip-path="url(#hg14t)" x="156" y="18.8" width="30" height="18.2"/><line class="stream-b" x1="171.0" y1="37.0" x2="171.0" y2="54.2"/><rect class="sand-b" clip-path="url(#hg14b)" x="156" y="55.2" width="30" height="6.8"/><polygon class="glass" points="156,12 186,12 174.0,37.0 168.0,37.0"/><polygon class="glass" points="168.0,37.0 174.0,37.0 186,62 156,62"/><line class="frame" x1="152" y1="12" x2="190" y2="12"/><line class="frame" x1="152" y1="62" x2="190" y2="62"/><text class="tick" x="193" y="24">8</text><text class="tick" x="193" y="60">3</text><text class="legend" x="171.0" y="77" text-anchor="middle">B</text><line class="ink-line" x1="222" y1="37.0" x2="306" y2="37.0" stroke-width="1.5"/><polygon class="ink-fill" points="312,37.0 304,33.0 304,41.0"/><text class="legend" x="267" y="29.0" text-anchor="middle">flip A</text><clipPath id="hg15t"><polygon points="336,12 366,12 354.0,37.0 348.0,37.0"/></clipPath><clipPath id="hg15b"><polygon points="348.0,37.0 354.0,37.0 366,62 336,62"/></clipPath><rect class="sand-a" clip-path="url(#hg15t)" x="336" y="12.0" width="30" height="25.0"/><line class="stream-a" x1="351.0" y1="37.0" x2="351.0" y2="61.0"/><polygon class="glass" points="336,12 366,12 354.0,37.0 348.0,37.0"/><polygon class="glass" points="348.0,37.0 354.0,37.0 366,62 336,62"/><line class="frame" x1="332" y1="12" x2="370" y2="12"/><line class="frame" x1="332" y1="62" x2="370" y2="62"/><text class="tick" x="373" y="24">7</text><text class="tick" x="373" y="60">0</text><text class="legend" x="351.0" y="77" text-anchor="middle">A</text><clipPath id="hg16t"><polygon points="400,12 430,12 418.0,37.0 412.0,37.0"/></clipPath><clipPath id="hg16b"><polygon points="412.0,37.0 418.0,37.0 430,62 400,62"/></clipPath><rect class="sand-b" clip-path="url(#hg16t)" x="400" y="18.8" width="30" height="18.2"/><line class="stream-b" x1="415.0" y1="37.0" x2="415.0" y2="54.2"/><rect class="sand-b" clip-path="url(#hg16b)" x="400" y="55.2" width="30" height="6.8"/><polygon class="glass" points="400,12 430,12 418.0,37.0 412.0,37.0"/><polygon class="glass" points="412.0,37.0 418.0,37.0 430,62 400,62"/><line class="frame" x1="396" y1="12" x2="434" y2="12"/><line class="frame" x1="396" y1="62" x2="434" y2="62"/><text class="tick" x="437" y="24">8</text><text class="tick" x="437" y="60">3</text><text class="legend" x="415.0" y="77" text-anchor="middle">B</text></svg><figcaption>רגע 14: שעון A נגמר והופכים אותו. ריצה שלישית של A מתחילה; ב-B נשארו 8 דקות.</figcaption></figure><figure class="stepper-frame"><svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="רגע 21: A runs out"><rect class="measure" x="2" y="2" width="456" height="88" rx="6"/><text class="legend" x="10" y="33.0" font-weight="700">t = 21</text><text class="tick" x="10" y="51.0">A runs out</text><clipPath id="hg17t"><polygon points="92,12 122,12 110.0,37.0 104.0,37.0"/></clipPath><clipPath id="hg17b"><polygon points="104.0,37.0 110.0,37.0 122,62 92,62"/></clipPath><rect class="sand-a" clip-path="url(#hg17b)" x="92" y="37.0" width="30" height="25.0"/><polygon class="glass" points="92,12 122,12 110.0,37.0 104.0,37.0"/><polygon class="glass" points="104.0,37.0 110.0,37.0 122,62 92,62"/><line class="frame" x1="88" y1="12" x2="126" y2="12"/><line class="frame" x1="88" y1="62" x2="126" y2="62"/><text class="tick" x="129" y="24">0</text><text class="tick" x="129" y="60">7</text><text class="legend" x="107.0" y="77" text-anchor="middle">A</text><clipPath id="hg18t"><polygon points="156,12 186,12 174.0,37.0 168.0,37.0"/></clipPath><clipPath id="hg18b"><polygon points="168.0,37.0 174.0,37.0 186,62 156,62"/></clipPath><rect class="sand-b" clip-path="url(#hg18t)" x="156" y="34.7" width="30" height="2.3"/><line class="stream-b" x1="171.0" y1="37.0" x2="171.0" y2="38.3"/><rect class="sand-b" clip-path="url(#hg18b)" x="156" y="39.3" width="30" height="22.7"/><polygon class="glass" points="156,12 186,12 174.0,37.0 168.0,37.0"/><polygon class="glass" points="168.0,37.0 174.0,37.0 186,62 156,62"/><line class="frame" x1="152" y1="12" x2="190" y2="12"/><line class="frame" x1="152" y1="62" x2="190" y2="62"/><text class="tick" x="193" y="24">1</text><text class="tick" x="193" y="60">10</text><text class="legend" x="171.0" y="77" text-anchor="middle">B</text><line class="ink-line" x1="222" y1="37.0" x2="306" y2="37.0" stroke-width="1.5"/><polygon class="ink-fill" points="312,37.0 304,33.0 304,41.0"/><text class="legend" x="267" y="29.0" text-anchor="middle">START</text><clipPath id="hg19t"><polygon points="336,12 366,12 354.0,37.0 348.0,37.0"/></clipPath><clipPath id="hg19b"><polygon points="348.0,37.0 354.0,37.0 366,62 336,62"/></clipPath><rect class="sand-a" clip-path="url(#hg19b)" x="336" y="37.0" width="30" height="25.0"/><polygon class="glass" points="336,12 366,12 354.0,37.0 348.0,37.0"/><polygon class="glass" points="348.0,37.0 354.0,37.0 366,62 336,62"/><line class="frame" x1="332" y1="12" x2="370" y2="12"/><line class="frame" x1="332" y1="62" x2="370" y2="62"/><text class="tick" x="373" y="24">0</text><text class="tick" x="373" y="60">7</text><text class="legend" x="351.0" y="77" text-anchor="middle">A</text><clipPath id="hg20t"><polygon points="400,12 430,12 418.0,37.0 412.0,37.0"/></clipPath><clipPath id="hg20b"><polygon points="412.0,37.0 418.0,37.0 430,62 400,62"/></clipPath><rect class="sand-b" clip-path="url(#hg20t)" x="400" y="34.7" width="30" height="2.3"/><line class="stream-b" x1="415.0" y1="37.0" x2="415.0" y2="38.3"/><rect class="sand-b" clip-path="url(#hg20b)" x="400" y="39.3" width="30" height="22.7"/><polygon class="glass" points="400,12 430,12 418.0,37.0 412.0,37.0"/><polygon class="glass" points="412.0,37.0 418.0,37.0 430,62 400,62"/><line class="frame" x1="396" y1="12" x2="434" y2="12"/><line class="frame" x1="396" y1="62" x2="434" y2="62"/><text class="tick" x="437" y="24">1</text><text class="tick" x="437" y="60">10</text><text class="legend" x="415.0" y="77" text-anchor="middle">B</text></svg><figcaption>רגע 21: שעון A נגמר בפעם השלישית. ב-B נשארה בדיוק דקה אחת למעלה: מתחילים למדוד, לא הופכים כלום.</figcaption></figure><figure class="stepper-frame"><svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="רגע 22: B runs out"><rect class="measure" x="2" y="2" width="456" height="88" rx="6"/><text class="legend" x="10" y="33.0" font-weight="700">t = 22</text><text class="tick" x="10" y="51.0">B runs out</text><clipPath id="hg21t"><polygon points="92,12 122,12 110.0,37.0 104.0,37.0"/></clipPath><clipPath id="hg21b"><polygon points="104.0,37.0 110.0,37.0 122,62 92,62"/></clipPath><rect class="sand-a" clip-path="url(#hg21b)" x="92" y="37.0" width="30" height="25.0"/><polygon class="glass" points="92,12 122,12 110.0,37.0 104.0,37.0"/><polygon class="glass" points="104.0,37.0 110.0,37.0 122,62 92,62"/><line class="frame" x1="88" y1="12" x2="126" y2="12"/><line class="frame" x1="88" y1="62" x2="126" y2="62"/><text class="tick" x="129" y="24">0</text><text class="tick" x="129" y="60">7</text><text class="legend" x="107.0" y="77" text-anchor="middle">A</text><clipPath id="hg22t"><polygon points="156,12 186,12 174.0,37.0 168.0,37.0"/></clipPath><clipPath id="hg22b"><polygon points="168.0,37.0 174.0,37.0 186,62 156,62"/></clipPath><rect class="sand-b" clip-path="url(#hg22b)" x="156" y="37.0" width="30" height="25.0"/><polygon class="glass" points="156,12 186,12 174.0,37.0 168.0,37.0"/><polygon class="glass" points="168.0,37.0 174.0,37.0 186,62 156,62"/><line class="frame" x1="152" y1="12" x2="190" y2="12"/><line class="frame" x1="152" y1="62" x2="190" y2="62"/><text class="tick" x="193" y="24">0</text><text class="tick" x="193" y="60">11</text><text class="legend" x="171.0" y="77" text-anchor="middle">B</text><text class="legend" x="226" y="42.0" font-weight="700">STOP ✓ 22 − 21 = 1</text></svg><figcaption>רגע 22: שעון B נגמר בפעם השנייה. מסיימים: נמדדה דקה אחת.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="6"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    | הרגע | מה קרה | חול למעלה לפני (\( A \), \( B \)) | הפעולה | חול למעלה אחרי (\( A \), \( B \)) |
    |:-:|---|:-:|---|:-:|
    | 0 | התחלה | (0, 0) | הופכים את \( A \) ואת \( B \) | (7, 11) |
    | 7 | ‏\( A \) נגמר | (0, 4) | הופכים את \( A \) | (7, 4) |
    | 11 | ‏\( B \) נגמר | (3, 0) | הופכים את \( B \) | (3, 11) |
    | 14 | ‏\( A \) נגמר | (0, 8) | הופכים את \( A \) | (7, 8) |
    | 21 | ‏\( A \) נגמר | (0, 1) | **מתחילים למדוד**, לא הופכים כלום | (0, 1) |
    | 22 | ‏\( B \) נגמר | (0, 0) | **מסיימים: \( 22 - 21 = 1 \)** | |

    **למה זו המדידה שמסתיימת הכי מוקדם?** הרגעים שבהם שעון יכול להיגמר לפני 22 הם
    \( 7, 11, 14, 15, 17, 18, 19, 20, 21 \). יש בהם זוגות בהפרש 1, למשל 14 ו-15, אבל הם לא
    שייכים לאותה ריצה: ברגע 11 (\( B \) נגמר) נשארו ב-\( A \) שלוש דקות; אם **לא** הופכים
    אותו הוא נגמר ברגע 14, ואם **כן** הופכים אותו הוא נגמר ברגע 15. אי אפשר לקבל את שניהם.
    הדרך השיטתית לבדוק את כל הזוגות היא האלגוריתם של סעיף ב, והוא מאשר ש-22 הוא המינימום.

    **הכללה.** אם \( \gcd(A, B) = 1 \), לפי משפט בזו (Bézout) קיימים \( x, y \ge 0 \) כך
    ש-\( D = xB - yA \). מריצים את \( B \) \( x \) פעמים ברצף ואת \( A \) \( y \) פעמים ברצף,
    שניהם מרגע 0, ומודדים מהרגע \( yA \) עד הרגע \( xB \). כלומר **כל** \( D \) ניתן למדידה
    כמרווח, אבל לא בהכרח מוקדם: \( D = 1 \) דורש לחכות 22 דקות.

---

### סעיף ב – האלגוריתם הכללי

כתבו פונקציה שמקבלת \( A \), \( B \) ו-\( D \) ומחזירה את רגע ההתחלה \( t_1 \) ואת תוכנית
הפעולה של המדידה **שמסתיימת הכי מוקדם**, או "אין פתרון".

??? tip "רמז 1"
    בשאלה 0018 כל קשת בגרף הייתה "שווה": חיפשנו מצב עם \( t = D \), ולא היה אכפת לנו כמה
    אירועים עברנו בדרך. מה המחיר של קשת עכשיו, ומה בדיוק אנחנו ממזערים?

??? tip "רמז 2"
    אם הזמן הוא המחיר, הוא לא יכול להישאר חלק מהמצב. מה צריך להיכנס למצב במקומו כדי לדעת
    מתי המדידה הסתיימה?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        המצב הוא \( (a, b, m) \): החול שלמעלה בשני השעונים וכמה דקות **נמדדו עד עכשיו**
        (\( m = -1 \) לפני ההתחלה). הזמן \( t \) הוא המחיר של המסלול. מריצים **Dijkstra**: קשת
        "מתחילים למדוד" במחיר 0, וארבע קשתות היפוך במחיר ההמתנה. המצב הראשון שיוצא מהתור
        עם \( m = D \) הוא המדידה שמסתיימת הכי מוקדם.

    #### הרעיון { .sol-idea }

    **למה BFS כבר לא מספיק.** עכשיו הזמן \( t \) הוא **המחיר** שרוצים למזער, ולא חלק
    מהמטרה. בין שני אירועים עוברות \( w \) דקות, ו-\( w \) משתנה מקשת לקשת (4 דקות כאן, 7
    שם). BFS מוצא את המסלול עם מספר הקשתות הקטן ביותר, אבל זה לא המסלול הקצר בזמן: שלוש
    קשתות של 3 דקות קצרות מקשת אחת של 11. מסלול קצר ביותר בגרף עם משקלים חיוביים הוא
    בדיוק הבעיה שפותר **Dijkstra**.

    **המצב החדש.** שלשה \( (a, b, m) \): כמות החול שלמעלה בשעון \( A \), כמות החול שלמעלה
    בשעון \( B \), וכמה דקות נמדדו עד עכשיו (\( m \)), עם \( m = -1 \) כל עוד המדידה לא
    התחילה. הזמן \( t \) **לא** חלק מהמצב: הוא המרחק מהמצב ההתחלתי, וזה מה ש-Dijkstra
    מחשב. אילו היינו מכניסים את \( t \) למצב, כל מצב היה נראה "חדש", החיפוש לא היה גוזם
    כלום, והוא לא היה מסתיים (כי \( t \) לא חסום).

    **הקשתות מכל מצב:**

    - **"מתחילים למדוד"** (רק כש-\( m = -1 \)): מעבר ל-\( (a, b, 0) \) במחיר 0. ההחלטה
      מתקבלת ברגע אירוע, בלי להפוך כלום, ולכן היא לא לוקחת זמן.
    - **ארבע אפשרויות ההיפוך** כמו בשאלה 0018: מחכים \( w \) דקות (עד השעון הבא), והמחיר
      הוא \( w \). אם המדידה כבר התחילה, \( m \) גדל ב-\( w \); אם \( m + w > D \) הקשת נפסלת,
      כי עברנו את \( D \) בלי ששעון נגמר בדיוק.

    המטרה: המצב הראשון שיוצא מהתור עם \( m = D \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **אתחול:** תור עדיפויות לפי \( t \) עם המצב \( (0, 0, -1) \) במחיר 0, ומילון `best`
       עם המחיר הטוב ביותר שידוע לכל מצב.
    2. **הוצאה:** מוציאים את הרשומה עם \( t \) הקטן ביותר. אם היא ישנה (יש ל-`best` מחיר
       קטן יותר) מדלגים. אם \( m = D \), מחזירים את רגע ההתחלה ואת התוכנית.
    3. **קשתות:** בונים את האפשרויות: "מתחילים למדוד" כש-\( m = -1 \), וארבע אפשרויות
       ההיפוך עם ההמתנה שלהן; פוסלים \( m + w > D \).
    4. **שחרור (relax):** אפשרות שמגיעה למצב בזמן קטן מ-`best` מעדכנת את `best` ונכנסת
       לתור.
    5. **סיום:** אם התור התרוקן, אין מדידה כזו (למשל כש-\( D \) לא כפולה של \( \gcd(A, B) \)).

    </div>

    #### הקוד { .sol-code }

    התוכנית מוחזרת כמו בשאלה 0018 (מיפוי מרגע לפעולה), ובנוסף מוחזר רגע ההתחלה. בדוגמה:
    התחלה ב-21 והתוכנית `{0: 'AB', 7: 'A', 11: 'B', 14: 'A', 21: ''}`, כאשר הפעולה הריקה ב-21
    היא "לא להפוך, רק לחכות". ב-SystemVerilog: `"0:AB 7:A 11:B 14:A 21:-"`.

    === "SystemVerilog"
        ```systemverilog title="function measure_interval" linenums="1" hl_lines="27 35 47 58"
        // One entry of the priority queue: the state (a, b, measured) plus the path that reached it.
        typedef struct {
          int    t;          // time so far (the path cost Dijkstra minimizes)
          int    a;          // sand on top of A
          int    b;          // sand on top of B
          int    measured;   // minutes measured so far, -1 = measurement not started yet
          int    start;      // time the measurement started, -1 = not started
          string plan;       // "0:AB 7:A ..." (A, B, AB = flip, - = just wait)
        } hg_entry_t;

        // Returns 1 and fills `start` and `plan` for the measurement of D that ends earliest.
        function automatic bit measure_interval(int A, int B, int D, output int start, output string plan);
          hg_entry_t queue[$];               // (1)!
          hg_entry_t options[$];
          int        best[string];           // earliest known time per state, keyed "a,b,measured"
          hg_entry_t e, n;
          string     key, action;
          int        a2, b2, delay, m2, pos;

          e = '{0, 0, 0, -1, -1, ""};
          best["0,0,-1"] = 0;
          queue.push_back(e);

          while (queue.size() > 0) begin
            e = queue.pop_front();
            key = $sformatf("%0d,%0d,%0d", e.a, e.b, e.measured);
            if (e.t > best[key]) continue;                   // (2)!
            if (e.measured == D) begin
              start = e.start;
              plan  = e.plan;
              return 1;
            end

            options.delete();
            if (e.measured == -1) begin                      // (3)!
              n = e;
              n.measured = 0;
              n.start    = e.t;
              options.push_back(n);
            end
            for (int flip_a = 0; flip_a <= 1; flip_a++)
              for (int flip_b = 0; flip_b <= 1; flip_b++) begin
                a2 = flip_a ? A - e.a : e.a;
                b2 = flip_b ? B - e.b : e.b;
                if (a2 == 0 && b2 == 0) continue;            // nothing flows, nothing will happen
                delay = (a2 == 0) ? b2 : (b2 == 0) ? a2 : (a2 < b2 ? a2 : b2);   // next to run out
                m2 = (e.measured == -1) ? -1 : e.measured + delay;   // (4)!
                if (m2 > D) continue;                        // would overshoot D
                action = {flip_a ? "A" : "", flip_b ? "B" : ""};
                if (action == "") action = "-";
                n = '{e.t + delay, (a2 > delay) ? a2 - delay : 0, (b2 > delay) ? b2 - delay : 0,
                      m2, e.start, {e.plan, (e.plan == "") ? "" : " ", $sformatf("%0d:%s", e.t, action)}};
                options.push_back(n);
              end

            foreach (options[i]) begin
              key = $sformatf("%0d,%0d,%0d", options[i].a, options[i].b, options[i].measured);
              if (!best.exists(key) || options[i].t < best[key]) begin   // (5)!
                best[key] = options[i].t;
                pos = queue.size();                          // sorted insert, after entries with the same t
                for (int j = 0; j < queue.size(); j++)
                  if (queue[j].t > options[i].t) begin pos = j; break; end
                queue.insert(pos, options[i]);
              end
            end
          end
          return 0;
        endfunction
        ```

        1. אין ערימה (heap) מובנית ב-SystemVerilog, ולכן התור נשמר **ממוין** לפי \( t \): כל
           רשומה חדשה נכנסת אחרי כל הרשומות עם \( t \) קטן או שווה (`queue.insert` בשורה 63),
           ו-`pop_front` נותן תמיד את הקטנה ביותר. ההכנסה היא \( O(n) \), וזה מספיק למרחב
           מצבים של כמה מאות צמתים.
        2. רשומה ישנה: המצב כבר הושג בזמן קטן יותר, ולכן הרשומה הזאת לא מעניינת. כך לא
           צריך לחפש ולמחוק רשומות בתוך התור.
        3. הקשת "מתחילים למדוד": אותו מצב פיזי, \( m \) הופך ל-0, ורגע ההתחלה נשמר. המחיר
           0, ולכן \( t \) לא משתנה.
        4. ‏\( m \) גדל בזמן ההמתנה רק אחרי שהמדידה התחילה. אם עוברים את \( D \), הקשת נפסלת.
        5. השחרור (relax) של Dijkstra: רק מצב שמושג בזמן קטן יותר נכנס לתור.

    === "Python"
        ```python title="solve" linenums="1" hl_lines="15 22 33 41"
        import heapq
        from itertools import count


        def solve(A, B, D):
            """Return (start, plan) for the measurement that ends earliest, or None."""
            # State: (sand on top of A, sand on top of B, minutes measured; -1 = not started yet)
            first = (0, 0, -1)
            best = {first: 0}
            tie = count()  # tie-breaker so the queue never compares dicts (1)
            queue = [(0, next(tie), first, None, {})]

            while queue:
                t, _, state, start, plan = heapq.heappop(queue)
                if t > best[state]:
                    continue                        # stale entry, a faster way here was found (2)
                a, b, measured = state
                if measured == D:
                    return start, plan

                options = []                        # (new state, new time, start, plan)
                if measured == -1:                  # start measuring right now (takes no time) (3)
                    options.append(((a, b, 0), t, t, plan))

                for flip_a in (False, True):
                    for flip_b in (False, True):
                        a2 = A - a if flip_a else a
                        b2 = B - b if flip_b else b
                        running = [sand for sand in (a2, b2) if sand > 0]
                        if not running:
                            continue                # nothing flows, nothing will happen
                        wait = min(running)         # until the next hourglass runs out
                        m2 = -1 if measured == -1 else measured + wait   # (4)!
                        if m2 > D:
                            continue                # would overshoot D
                        action = ("A" if flip_a else "") + ("B" if flip_b else "")
                        new_state = (max(a2 - wait, 0), max(b2 - wait, 0), m2)
                        options.append((new_state, t + wait, start, {**plan, t: action}))

                for new_state, new_t, new_start, new_plan in options:
                    if new_state not in best or new_t < best[new_state]:   # (5)!
                        best[new_state] = new_t
                        heapq.heappush(queue, (new_t, next(tie), new_state, new_start, new_plan))
            return None
        ```

        1. הערימה משווה tuples איבר-איבר. כששני \( t \) שווים היא הייתה מגיעה להשוואה של
           מילונים, שלא מוגדרת. המונה `count()` באיבר השני מונע את זה, וגם שומר על סדר FIFO
           בין שוויונות.
        2. רשומה ישנה: המצב כבר הושג בזמן קטן יותר. הבדיקה זורקת אותה בלי לחפש בתוך
           הערימה.
        3. הקשת "מתחילים למדוד": אותו מצב פיזי, \( m \) הופך ל-0, ורגע ההתחלה נשמר. המחיר
           0, ולכן \( t \) לא משתנה.
        4. ‏\( m \) גדל בזמן ההמתנה רק אחרי שהמדידה התחילה.
        5. השחרור (relax) של Dijkstra: רק מצב שמושג בזמן קטן יותר נכנס לערימה.

    #### למה זה נכון { .sol-proof }

    **‏Dijkstra מחזיר את המינימום.** כל הקשתות במחיר \( \ge 0 \), ולכן Dijkstra מוציא את
    המצבים לפי סדר עולה של הזמן המינימלי להגיע אליהם. המצב הראשון שיוצא עם \( m = D \)
    הוא לכן זה שמושג בזמן הקטן ביותר, כלומר המדידה שמסתיימת הכי מוקדם. **החיפוש מסתיים**
    כי מרחב המצבים סופי: \( (A + 1)(B + 1)(D + 2) \) לכל היותר, ובפועל הרבה פחות, כי בכל
    אירוע \( a = 0 \) או \( b = 0 \).

    **המעקב עבור הדוגמה.** כל שורה היא הוצאה אחת מהתור (המצב עם \( t \) הקטן ביותר). "לא
    משתפר" פירושו שהמצב כבר נמצא בזמן קטן או שווה, ולכן לא נכנס שוב לתור:

    | # | ‏\( t \) | המצב \( (a, b, m) \) | התחלה | מה נכנס לתור |
    |:-:|:-:|:-:|:-:|---|
    | 1 | 0 | (0, 0, −1) | | (0, 0, 0) ב-0 דרך "התחלה"; (0, 4, −1) ב-7 דרך \( AB \). ‏\( A \) לבד או \( B \) לבד מחזירים ל-(0, 0, −1), לא משתפר |
    | 2 | 0 | (0, 0, 0) | 0 | אין: כל המתנה נותנת \( m \ge 7 > 1 \) |
    | 3 | 7 | (0, 4, −1) | | (0, 4, 0) ב-7; (3, 0, −1) ב-11 דרך \( A \) |
    | 4 | 7 | (0, 4, 0) | 7 | אין |
    | 5 | 11 | (3, 0, −1) | | (3, 0, 0) ב-11; (0, 8, −1) ב-14 דרך \( B \); (0, 7, −1) ב-15 דרך \( AB \) |
    | 6 | 11 | (3, 0, 0) | 11 | אין |
    | 7 | 14 | (0, 8, −1) | | (0, 8, 0) ב-14; (0, 1, −1) ב-21 דרך \( A \); (4, 0, −1) ב-17 דרך \( AB \) |
    | 8 | 14 | (0, 8, 0) | 14 | אין |
    | 9 | 15 | (0, 7, −1) | | (0, 7, 0) ב-15; (3, 0, −1) ב-19 לא משתפר (כבר ב-11) |
    | 10 | 15 | (0, 7, 0) | 15 | אין |
    | 11 | 17 | (4, 0, −1) | | (4, 0, 0) ב-17; השאר לא משתפר |
    | 12 | 17 | (4, 0, 0) | 17 | אין |
    | 13 | 21 | (0, 1, −1) | | (0, 1, 0) ב-21; (6, 0, −1) ב-22 דרך \( A \); (0, 3, −1) ב-28 דרך \( AB \) |
    | 14 | 21 | (0, 1, 0) | 21 | **(0, 0, 1) ב-22 דרך המתנה**; (6, 0, 1) ב-22 דרך \( A \) |
    | 15 | 22 | (6, 0, −1) | | (6, 0, 0) ב-22; (0, 5, −1) ב-28; (0, 10, −1) ב-23 |
    | 16 | 22 | **(0, 0, 1)** | 21 | ‏\( m = D \): **מצאנו**. התחלה ב-21, סיום ב-22 |

    שימו לב לשורות 2, 4, 6, 8, 10, 12: בכל אירוע האלגוריתם "מנסה" להתחיל למדוד, ומגלה שאף
    שעון לא נגמר בדיוק דקה אחרי. רק ברגע 21, כשב-\( B \) נשארה בדיוק דקה למעלה, ההתחלה
    מצליחה.

    **המסלול שנמצא**, עם הענפים הצדדיים העיקריים (על כל קשת: הפעולה ומחיר הזמן שלה):

    ```mermaid
    flowchart TD
        s0["t=0<br/>(0, 0, −1)"]
        s0 -- "AB, +7" --> s1["t=7<br/>(0, 4, −1)"]
        s0 -. "start, +0" .-> d0["(0, 0, 0)<br/>dead end"]
        s1 -- "A, +4" --> s2["t=11<br/>(3, 0, −1)"]
        s1 -. "start, +0" .-> d1["(0, 4, 0)<br/>dead end"]
        s2 -- "B, +3" --> s3["t=14<br/>(0, 8, −1)"]
        s2 -- "AB, +4" --> p1["t=15<br/>(0, 7, −1)"]
        s2 -. "start, +0" .-> d2["(3, 0, 0)<br/>dead end"]
        s3 -- "A, +7" --> s4["t=21<br/>(0, 1, −1)"]
        s3 -- "AB, +3" --> p2["t=17<br/>(4, 0, −1)"]
        s3 -. "start, +0" .-> d3["(0, 8, 0)<br/>dead end"]
        s4 -- "start, +0" --> s5["t=21<br/>(0, 1, 0)"]
        s5 -- "wait, +1" --> s6["t=22<br/>(0, 0, 1) ✓"]
        classDef pruned stroke-dasharray: 5 4,opacity:0.6;
        classDef found stroke:#1baf7a,stroke-width:3px;
        class p1,p2,d0,d1,d2,d3 pruned;
        class s6 found;
    ```

    #### סיבוכיות { .sol-cost }

    - **זמן:** עם \( S \) מצבים וערימה, \( O(S \log S) \). בפועל \( S \le (A + B + 1)(D + 2) \),
      כי בכל אירוע אחד השעונים ריק למעלה. בדוגמה ה-Dijkstra הוציא מהתור 16 מצבים.
    - **ב-SystemVerilog:** ההכנסה הממוינת היא \( O(S) \) לרשומה, כלומר \( O(S^2) \) בסך הכול.
      לערכים של ראיון זה שקוף.
    - **זיכרון:** \( O(S) \) ל-`best` ולתור.

    **נסו בעצמכם.** בחרו שני שעונים ומטרה: ה-Dijkstra רץ בדפדפן ומראה את המדידה שמסתיימת
    הכי מוקדם על ציר הזמן, עם חלון המדידה במסגרת, ואת האירועים אחד אחד עם שני השעונים.
    נסו \( D = 4 \), שמרגע 0 אי אפשר למדוד אבל כמרווח כן, ו-\( A = 4, B = 6, D = 3 \),
    שאין לו פתרון:

    <div class="explorer" data-kind="hourglass" data-mode="interval" data-a="7" data-b="11" data-d="1"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: להשאיר את הזמן בתוך המצב"
    עם \( t \) במצב, כל מצב נראה חדש, `best` לא גוזם כלום, והחיפוש לא מסתיים, כי \( t \)
    לא חסום. הזמן הוא המחיר של המסלול, ו-\( m \) (כמה נמדד) הוא מה שמחליף אותו במצב
    ומבטיח שהמרחב סופי.

??? trap "מלכודת: לפתור עם ה-BFS של 0018 מכל מצב"
    אפשר להריץ את ה-BFS מכל מצב שניתן להגיע אליו ולקחת את המינימום. זה נכון, אבל
    \( O(S^2) \), ו-Dijkstra עושה את זה במעבר אחד. בראיון כדאי להזכיר את הפתרון הזה כצעד
    ביניים, ואז לשפר.

??? trap "מלכודת: להתחיל למדוד 'בין אירועים'"
    "מתחילים למדוד" היא החלטה בגרף, עם מחיר 0, שאפשר לקבל רק ברגע אירוע. מי שמתחיל למדוד
    ברגע שרירותי לא יודע מתי התחיל. גם הסיום חייב להיות אירוע: לכן \( m + w > D \) נפסל,
    ולא מעוגל.

??? followup "שאלות המשך"
    - **מספר היפוכים מינימלי:** איך ממזערים את מספר ההיפוכים במקום את הזמן? (אותו
      Dijkstra עם משקל 1 לכל שעון שהופכים ו-0 להמתנה.)
    - **קיום לכל \( D \):** איך מוכיחים שעם \( \gcd(A, B) = 1 \) כל \( D \) ניתן למדידה?
      (משפט בזו, כמו בסעיף א.)
    - **שלושה שעונים:** מה המצב ומה מספר האפשרויות?
    - **‏BFS לעומת Dijkstra:** למה BFS הוא מקרה פרטי של Dijkstra, ומתי מותר להחליף
      Dijkstra ב-BFS בלי לפגוע בתוצאה?
