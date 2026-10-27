---
id: 52
title: HH מול HT – כמה הטלות מטבע עד שהרצף מופיע
level: senior
difficulty: medium
kind: math
tags: [probability, fsm, sequences, systemverilog, python]
source: "שאלת ראיון קלאסית בהסתברות; ההכללה של Conway ומשחק Penney"
added: 2026-10-27
---

## השאלה

מטילים מטבע הוגן שוב ושוב, ועוצרים ברגע שמופיעות שתי הטלות רצופות מסוימות.

- **סעיף א – ‏HH מול HT :** מה מספר ההטלות הממוצע עד שמופיע `HH` (שני "עץ" ברצף)? ומה
  הממוצע עד שמופיע `HT`? למה התשובות שונות, אם לשני הרצפים אותה הסתברות בכל מקום?
- **סעיף ב – כל רצף, ומטבע לא הוגן :** כתבו קוד שמחשב את מספר ההטלות הממוצע לכל רצף,
  והסבירו את הנוסחה. כמה זה ל-`HHH`? ומה משתנה כש-H יוצא בהסתברות \( q \)?
- **סעיף ג – מירוץ :** שני שחקנים מטילים אותו מטבע; אחד בוחר `HH` והשני `HT`, ומנצח
  מי שהרצף שלו מופיע קודם. מה הסיכוי של כל אחד? ומה קורה עם רצפים באורך 3, ועם שלושה
  שחקנים או יותר?
- **סעיף ד – ההתפלגות :** מצאו את הפונקציה היוצרת של מספר ההטלות, ומתוכה את השונות
  ואת ההסתברות לכל מספר הטלות.

??? interviewer "מה המראיין בודק"
    - **מצבים במקום מקרים :** האם המועמד מגדיר מצב לפי "כמה מהרצף כבר נבנה", כמו בגלאי
      רצף בחומרה, וכותב משוואה לכל מצב.
    - **הבחנה בין "באותה הסתברות" ל"באותו זמן" :** ‏`HH` ו-`HT` מופיעים בכל מקום
      בהסתברות 1/4, ובכל זאת זמני ההמתנה שונים. האם הוא מסביר למה.
    - **הכללה :** האם הוא מגיע לנוסחה שתלויה רק בחפיפות של הרצף עם עצמו, ושעובדת גם
      במטבע לא הוגן ובכל אלפבית.
    - **אינטואיציה מטעה :** במירוץ, האם הוא נופל ל"הרצף עם התוחלת הקטנה מנצח".
    - **מעבר לתוחלת :** האם הוא יודע להגיע להתפלגות כולה, ולמה השונות גדולה כל כך.
    - **הקשר ל-DV :** כמה זמן טסט אקראי צריך לרוץ עד שרצף מסוים מופיע ב-stimulus.

---

### סעיף א – ‏HH מול HT

מה מספר ההטלות הממוצע עד `HT`, ומה עד `HH`?

??? tip "רמז 1"
    הגדירו מצבים לפי מה שכבר נבנה : "כלום", "יש `H` בסוף", "הרצף הושלם". מכל מצב, ההטלה
    הבאה מובילה למצב אחר בהסתברות חצי.

??? tip "רמז 2"
    תהי \( E_s \) התוחלת של מספר ההטלות שנשארו ממצב \( s \). כל הטלה עולה 1, ולכן
    \( E_s = 1 + \tfrac12 E_{s'} + \tfrac12 E_{s''} \). מה ההבדל בין `HH` ל-`HT` כשאחרי
    `H` מגיעה ההטלה ה"לא נכונה"?

<div class="selfcheck" data-answer="6" data-show="6" data-hint="אחרי H, זנב מחזיר את HH להתחלה. כתבו E0 = 1 + E1/2 + E0/2 ו-E1 = 1 + E0/2, ופתרו." markdown>
מה מספר ההטלות הממוצע עד `HH`?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏`HT` : ‏4 הטלות בממוצע. ‏`HH` : ‏6 הטלות בממוצע. ההבדל הוא מה קורה אחרי `H` :
        ב-`HT`, הטלה "לא נכונה" (עוד `H`) משאירה אותנו עם `H` בסוף, כלומר באותו מצב. ב-`HH`,
        הטלה לא נכונה (`T`) מחזירה להתחלה ומוחקת את ההתקדמות.

    #### הרעיון { .sol-idea }

    המצב הוא **כמה מהרצף נמצא עכשיו בסוף ההטלות**, בדיוק כמו בגלאי רצף בחומרה
    ([שאלה 0040](../student/0040-sequence-detector-1011.md)). לשני הרצפים יש שלושה מצבים :
    התחלה, `H` בסוף, והרצף שלם. המעברים זהים חוץ ממעבר אחד :

    <!-- gen 0 -->

    <svg class="figure cp-fig" viewBox="0 0 660 300" style="max-width:41rem" role="img" aria-label="שרשראות המצבים של HH ושל HT : שלושה מצבים כל אחת, החצים מסומנים בהטלה"><defs><marker id="cp-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs><line class="fs-edge" x1="106" y1="92" x2="242" y2="92" marker-end="url(#cp-arrow)"/><text class="fs-label halo" x="175.0" y="84" text-anchor="middle">H</text><line class="fs-edge is-found" x1="296" y1="92" x2="432" y2="92" marker-end="url(#cp-arrow)"/><text class="fs-label is-found halo" x="365.0" y="84" text-anchor="middle">T</text><path class="fs-edge" d="M71,69 C50,28 110,28 89,68" marker-end="url(#cp-arrow)"/><text class="fs-label halo" x="80" y="38" text-anchor="middle">T</text><path class="fs-edge" d="M261,69 C240,28 300,28 279,68" marker-end="url(#cp-arrow)"/><text class="fs-label halo" x="270" y="38" text-anchor="middle">H</text><g class="fs-node is-start"><circle cx="80" cy="92" r="26"/><text x="80" y="96" text-anchor="middle" style="font-size:11px">start</text></g><g class="fs-node"><circle cx="270" cy="92" r="26"/><text x="270" y="96" text-anchor="middle">H</text></g><g class="fs-node is-out"><circle cx="460" cy="92" r="26"/><text x="460" y="96" text-anchor="middle">HT</text></g><text class="cp-exp" x="600" y="98" text-anchor="middle">E = 4</text><line class="fs-edge" x1="106" y1="222" x2="242" y2="222" marker-end="url(#cp-arrow)"/><text class="fs-label halo" x="175.0" y="214" text-anchor="middle">H</text><line class="fs-edge is-found" x1="296" y1="222" x2="432" y2="222" marker-end="url(#cp-arrow)"/><text class="fs-label is-found halo" x="365.0" y="214" text-anchor="middle">H</text><path class="fs-edge" d="M71,199 C50,158 110,158 89,198" marker-end="url(#cp-arrow)"/><text class="fs-label halo" x="80" y="168" text-anchor="middle">T</text><path class="fs-edge is-back" d="M270,248 Q175.0,292 80,250" marker-end="url(#cp-arrow)"/><text class="fs-label halo" x="175.0" y="284" text-anchor="middle">T</text><g class="fs-node is-start"><circle cx="80" cy="222" r="26"/><text x="80" y="226" text-anchor="middle" style="font-size:11px">start</text></g><g class="fs-node"><circle cx="270" cy="222" r="26"/><text x="270" y="226" text-anchor="middle">H</text></g><g class="fs-node is-out"><circle cx="460" cy="222" r="26"/><text x="460" y="226" text-anchor="middle">HH</text></g><text class="cp-exp" x="600" y="228" text-anchor="middle">E = 6</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="fs-key"></i>מעבר : ההטלה</span><span><i class="fs-key-found"></i>ההטלה שמשלימה את הרצף</span><span><i class="cp-key-back"></i>HH : זנב אחרי H מחזיר להתחלה</span></span>

    <!-- /gen -->

    ב-`HT`, אחרי `H` כל המשך טוב לנו : `T` מסיים, ו-`H` משאיר `H` בסוף. ב-`HH`, אחרי
    `H` ההטלה `T` שולחת להתחלה, ומשם צריך שוב לחכות ל-`H`. זה כל ההבדל.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏HT, ממצב `H` :** ‏\( E_1 = 1 + \tfrac12 \cdot 0 + \tfrac12 E_1 \), ולכן \( E_1 = 2 \).
    2. **‏HT, מההתחלה :** ‏\( E_0 = 1 + \tfrac12 E_1 + \tfrac12 E_0 \), ולכן
       \( E_0 = 2 + E_1 = 4 \).
    3. **‏HH, ממצב `H` :** ‏\( E_1 = 1 + \tfrac12 \cdot 0 + \tfrac12 E_0 \).
    4. **‏HH, מההתחלה :** ‏\( E_0 = 1 + \tfrac12 E_1 + \tfrac12 E_0 \), כלומר
       \( E_0 = 2 + E_1 = 3 + \tfrac12 E_0 \), ולכן \( E_0 = 6 \).

    </div>

    #### למה זה נכון { .sol-proof }

    **המצב מספיק.** ההטלות העתידיות לא תלויות בעבר, ומה שקובע אם ומתי הרצף יושלם הוא רק
    החלק של הרצף שכבר בסוף ההטלות. לכן התוחלת ממצב \( s \) מוגדרת היטב, ומקיימת את
    המשוואה "הטלה אחת ועוד התוחלת מהמצב הבא".

    **ההתפלגות.** לא רק התוחלת שונה. ההסתברות ש-`HT` מופיע לראשונה בהטלה \( t \) היא
    \( (t - 1) / 2^t \) : כל רצף של כמה `T`, אחר כך כמה `H` ואחר כך `T`. ל-`HH` היא
    \( F_{t-1} / 2^t \), כאשר \( F \) הם מספרי פיבונאצ'י, כי הרצפים שעוד לא הכילו `HH`
    נספרים כמו פיבונאצ'י. ל-`HH` יש זנב ארוך יותר :

    <!-- gen 2 -->

    <svg class="perf-chart" viewBox="0 0 640 250" role="img" aria-label="ההסתברות שהרצף מופיע לראשונה בהטלה t, ל-HT ול-HH : ל-HT שיא גבוה ב-2 ו-3 וזנב קצר, ל-HH זנב ארוך"><line class="grid" x1="46" x2="628" y1="216.0" y2="216.0"/><text class="tick" x="38" y="220.0" text-anchor="end">0</text><line class="grid" x1="46" x2="628" y1="149.3" y2="149.3"/><text class="tick" x="38" y="153.3" text-anchor="end">0.1</text><line class="grid" x1="46" x2="628" y1="82.7" y2="82.7"/><text class="tick" x="38" y="86.7" text-anchor="end">0.2</text><line class="grid" x1="46" x2="628" y1="16.0" y2="16.0"/><text class="tick" x="38" y="20.0" text-anchor="end">0.3</text><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="58.4" y="49.3" width="14.0" height="166.7" rx="2"><title>HT: P(T = 2) = 1/4</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="58.4" y="49.3" width="14.0" height="166.7" rx="2"><title>HH: P(T = 2) = 1/4</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="97.2" y="49.3" width="14.0" height="166.7" rx="2"><title>HT: P(T = 3) = 1/4</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="97.2" y="132.7" width="14.0" height="83.3" rx="2"><title>HH: P(T = 3) = 1/8</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="136.0" y="91.0" width="14.0" height="125.0" rx="2"><title>HT: P(T = 4) = 3/16</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="136.0" y="132.7" width="14.0" height="83.3" rx="2"><title>HH: P(T = 4) = 1/8</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="174.8" y="132.7" width="14.0" height="83.3" rx="2"><title>HT: P(T = 5) = 1/8</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="174.8" y="153.5" width="14.0" height="62.5" rx="2"><title>HH: P(T = 5) = 3/32</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="213.6" y="163.9" width="14.0" height="52.1" rx="2"><title>HT: P(T = 6) = 5/64</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="213.6" y="163.9" width="14.0" height="52.1" rx="2"><title>HH: P(T = 6) = 5/64</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="252.4" y="184.8" width="14.0" height="31.2" rx="2"><title>HT: P(T = 7) = 3/64</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="252.4" y="174.3" width="14.0" height="41.7" rx="2"><title>HH: P(T = 7) = 1/16</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="291.2" y="197.8" width="14.0" height="18.2" rx="2"><title>HT: P(T = 8) = 7/256</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="291.2" y="182.1" width="14.0" height="33.9" rx="2"><title>HH: P(T = 8) = 13/256</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="330.0" y="205.6" width="14.0" height="10.4" rx="2"><title>HT: P(T = 9) = 1/64</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="330.0" y="188.7" width="14.0" height="27.3" rx="2"><title>HH: P(T = 9) = 21/512</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="368.8" y="210.1" width="14.0" height="5.9" rx="2"><title>HT: P(T = 10) = 9/1024</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="368.8" y="193.9" width="14.0" height="22.1" rx="2"><title>HH: P(T = 10) = 17/512</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="407.6" y="212.7" width="14.0" height="3.3" rx="2"><title>HT: P(T = 11) = 5/1024</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="407.6" y="198.1" width="14.0" height="17.9" rx="2"><title>HH: P(T = 11) = 55/2048</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="446.4" y="214.2" width="14.0" height="1.8" rx="2"><title>HT: P(T = 12) = 11/4096</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="446.4" y="201.5" width="14.0" height="14.5" rx="2"><title>HH: P(T = 12) = 89/4096</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="485.2" y="215.0" width="14.0" height="1.0" rx="2"><title>HT: P(T = 13) = 3/2048</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="485.2" y="204.3" width="14.0" height="11.7" rx="2"><title>HH: P(T = 13) = 9/512</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="524.0" y="215.5" width="14.0" height="0.5" rx="2"><title>HT: P(T = 14) = 13/16384</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="524.0" y="206.5" width="14.0" height="9.5" rx="2"><title>HH: P(T = 14) = 233/16384</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="562.8" y="215.7" width="14.0" height="0.3" rx="2"><title>HT: P(T = 15) = 7/16384</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="562.8" y="208.3" width="14.0" height="7.7" rx="2"><title>HH: P(T = 15) = 377/32768</title></rect></g><g transform="translate(-7.4,0)"><rect class="bar by-multiples" x="601.6" y="215.8" width="14.0" height="0.2" rx="2"><title>HT: P(T = 16) = 15/65536</title></rect></g><g transform="translate(7.4,0)"><rect class="bar by-enum" x="601.6" y="209.8" width="14.0" height="6.2" rx="2"><title>HH: P(T = 16) = 305/32768</title></rect></g><text class="tick" x="65.4" y="234" text-anchor="middle">2</text><text class="tick" x="104.2" y="234" text-anchor="middle">3</text><text class="tick" x="143.0" y="234" text-anchor="middle">4</text><text class="tick" x="181.8" y="234" text-anchor="middle">5</text><text class="tick" x="220.6" y="234" text-anchor="middle">6</text><text class="tick" x="259.4" y="234" text-anchor="middle">7</text><text class="tick" x="298.2" y="234" text-anchor="middle">8</text><text class="tick" x="337.0" y="234" text-anchor="middle">9</text><text class="tick" x="375.8" y="234" text-anchor="middle">10</text><text class="tick" x="414.6" y="234" text-anchor="middle">11</text><text class="tick" x="453.4" y="234" text-anchor="middle">12</text><text class="tick" x="492.2" y="234" text-anchor="middle">13</text><text class="tick" x="531.0" y="234" text-anchor="middle">14</text><text class="tick" x="569.8" y="234" text-anchor="middle">15</text><text class="tick" x="608.6" y="234" text-anchor="middle">16</text><line class="axis" x1="46" x2="628" y1="216" y2="216"/><text class="tick" x="38" y="234" text-anchor="end">t</text></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="by-multiples"></i>HT : ‏(t − 1) / 2^t</span><span><i class="by-enum"></i>HH : ‏F(t − 1) / 2^t (פיבונאצ׳י)</span></span>

    <!-- /gen -->

    <!-- gen 4 -->

    | ההטלה t | ‏P(T = t) ל-HT | ‏P(T = t) ל-HH |
    |:-:|:-:|:-:|
    | ‏2 | ‏1/4 | ‏1/4 |
    | ‏3 | ‏1/4 | ‏1/8 |
    | ‏4 | ‏3/16 | ‏1/8 |
    | ‏5 | ‏1/8 | ‏3/32 |
    | ‏6 | ‏5/64 | ‏5/64 |
    | ‏7 | ‏3/64 | ‏1/16 |
    | ‏8 | ‏7/256 | ‏13/256 |

    <!-- /gen -->

    **למה "אותה הסתברות" לא נותנת "אותו זמן".** בכל זוג הטלות רצופות, `HH` ו-`HT`
    מופיעים בהסתברות 1/4, ולכן בטווח הארוך שניהם מופיעים באותה תדירות : פעם בארבע
    הטלות בממוצע. אבל `HH` מגיע **באשכולות** : ‏`HHH` מכיל שתי הופעות חופפות, ו-`HHHH`
    שלוש. כשההופעות מתקבצות, הרווחים ביניהן צריכים להיות ארוכים יותר כדי לשמור על אותה
    תדירות, וההמתנה להופעה הראשונה ארוכה יותר. ‏`HT` לא חופף לעצמו, ולכן ההופעות שלו
    מפוזרות באופן אחיד יותר.

---

### סעיף ב – כל רצף, ומטבע לא הוגן

כתבו קוד שמחשב את מספר ההטלות הממוצע לכל רצף, והסבירו את הנוסחה. מה משתנה כשהמטבע
לא הוגן, ו-H יוצא בהסתברות \( q \)?

??? tip "רמז 1"
    בדקו את התוצאות של סעיף א מול החפיפות של הרצף עם עצמו : ל-`HT` אין חפיפה חוץ מהרצף
    כולו, ול-`HH` יש גם חפיפה באורך 1.

??? tip "רמז 2"
    דמיינו קזינו הוגן : לפני כל הטלה מגיע מהמר חדש עם שקל, ומהמר על האות הראשונה של
    הרצף; אם הוא זוכה, הוא מהמר על כל מה שיש לו על האות השנייה, וכן הלאה. כמה כסף יש
    למהמרים ברגע שהרצף מופיע?

??? tip "רמז 3"
    בקזינו הוגן, הימור על אות שההסתברות שלה \( p \) מחזיר \( 1/p \) על כל שקל. במטבע
    הוגן זה פי 2, ובמטבע לא הוגן זה תלוי באות.

<div class="selfcheck" data-answer="14" data-show="14 = 2 + 4 + 8" data-hint="ל-HHH יש חפיפות עם עצמו באורכים 1, 2 ו-3. כל חפיפה באורך k תורמת 2 בחזקת k." markdown>
מה מספר ההטלות הממוצע עד `HHH`, במטבע הוגן?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏\( E[T] = \sum_k 1 / P(A_{1..k}) \) על כל אורך \( k \) שבו \( k \) האותיות האחרונות
        של הרצף \( A \) שוות ל-\( k \) הראשונות (כולל \( k = L \)), כאשר \( P(A_{1..k}) \) היא
        ההסתברות של \( k \) האותיות הראשונות. במטבע הוגן כל איבר הוא \( 2^k \) : ‏`HT` נותן 4,
        ‏`HH` נותן \( 2 + 4 = 6 \), ו-`HHH` נותן 14. עם \( P(H) = q \), ‏`HH` נותן
        \( 1/q + 1/q^2 \).

    <!-- cost: זמן \( O(L^2) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **קזינו הוגן.** לפני כל הטלה מגיע מהמר חדש עם שקל אחד, ומהמר על כך שההטלה הבאה
    היא האות הראשונה של הרצף. הקזינו הוגן : הימור על אות שההסתברות שלה \( p \) מחזיר
    \( 1/p \) על כל שקל. אם המהמר צודק, הוא מהמר על כל הסכום על האות השנייה, וכן הלאה.
    מהמר שטועה מפסיד הכול ויוצא, ומי שצדק \( k \) פעמים מחזיק \( 1 / P(A_{1..k}) \).

    **ברגע שהרצף מופיע** (הטלה \( T \)), הקזינו קיבל \( T \) שקלים, אחד מכל מהמר. מי
    שעדיין במשחק? המהמר שהתחיל לפני \( L \) הטלות והשלים את כל הרצף; וכל מהמר שהתחיל
    לפני \( k \) הטלות ושעד עכשיו צדק, כלומר כל \( k \) שבו \( k \) האותיות האחרונות של
    הרצף הן \( k \) הראשונות שלו. לכל אחד מהם \( 1 / P(A_{1..k}) \).

    **המשחק הוגן**, ולכן בממוצע הקזינו לא מרוויח ולא מפסיד : התוחלת של מה שקיבל שווה
    לתוחלת של מה ששילם. מה ששולם לא תלוי במזל, רק ברצף. לכן
    \( E[T] = \sum_{k \in \text{overlaps}} 1 / P(A_{1..k}) \).

    <!-- gen 5 -->

    | הרצף | חפיפות עם עצמו (אורכים) | התוחלת |
    |:-:|:-:|:-:|
    | ‏`HHH` | ‏1, 2, 3 | ‏2 + 4 + 8 = 14 |
    | ‏`HHT` | ‏3 | ‏8 = 8 |
    | ‏`HTH` | ‏1, 3 | ‏2 + 8 = 10 |
    | ‏`HTT` | ‏3 | ‏8 = 8 |
    | ‏`THH` | ‏3 | ‏8 = 8 |
    | ‏`THT` | ‏1, 3 | ‏2 + 8 = 10 |
    | ‏`TTH` | ‏3 | ‏8 = 8 |
    | ‏`TTT` | ‏1, 2, 3 | ‏2 + 4 + 8 = 14 |

    <!-- /gen -->

    **מטבע לא הוגן.** אותה נוסחה, עם ההסתברויות האמיתיות. מעניין שהסדר מתהפך : ככל ש-H
    שכיח יותר, `HH` מגיע מהר יותר מ-`HT`, כי ה-`T` הנדיר הוא שמעכב את `HT` :

    <!-- gen 6 -->

    | ההסתברות ל-H | ‏`HH` | ‏`HT` | ‏`TH` | ‏`TT` |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏1/2 | ‏6 | ‏4 | ‏4 | ‏6 |
    | ‏2/3 | ‏15/4 | ‏9/2 | ‏9/2 | ‏12 |
    | ‏3/4 | ‏28/9 | ‏16/3 | ‏16/3 | ‏20 |
    | ‏9/10 | ‏190/81 | ‏100/9 | ‏100/9 | ‏110 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **חפיפות :** לכל \( k = 1, \dots, L \) בודקים אם \( k \) האותיות האחרונות שוות
       ל-\( k \) הראשונות.
    2. **משקל :** כל חפיפה באורך \( k \) מוסיפה \( 1 / P(A_{1..k}) \), ההסתברות ההפוכה של
       התחילית באורך \( k \). החפיפה \( k = L \) תמיד קיימת ותורמת \( 1 / P(A) \).
    3. **אלפבית כלשהו :** הנוסחה לא תלויה בכך שיש שתי אותיות. בקובייה כל אות היא 1/6,
       וחפיפה באורך \( k \) תורמת \( 6^k \).

    </div>

    #### הקוד { .sol-code }

    הפונקציות מקבלות את ההסתברות של כל אות : ‏`{H: 1/2, T: 1/2}` למטבע הוגן,
    ‏`{H: q, T: 1 - q}` למטבע לא הוגן, או שש אותיות לקובייה.

    === "SystemVerilog"
        ```systemverilog title="prob, corr, expected_tosses" linenums="1" hl_lines="11 12"
        // the probability of the letters w[from .. to-1], p[c] the probability of the letter c
        function automatic real prob(string w, int from, int to, real p[byte]);
          real r = 1.0;
          for (int i = from; i < to; i++) r *= p[w[i]];
          return r;
        endfunction

        // Conway's correlation of a over b: 1 / P(the first k letters of b) for every k
        // for which the last k letters of a are the first k letters of b
        function automatic real corr(string a, string b, real p[byte]);
          real v = 0.0;
          for (int k = 1; k <= a.len() && k <= b.len(); k++)
            if (a.substr(a.len() - k, a.len() - 1) == b.substr(0, k - 1)) v += 1.0 / prob(b, 0, k, p);   // (1)!
          return v;
        endfunction

        // the expected number of tosses until the pattern first appears
        function automatic real expected_tosses(string w, real p[byte]);
          return corr(w, w, p);                                   // (2)!
        endfunction
        ```

        1. ‏`substr(i, j)` כולל את שני הקצוות : הסיומת באורך \( k \) של `a` מול התחילית באורך \( k \) של `b`.
        2. הרצף מול עצמו : כל חפיפה באורך \( k \) היא מהמר שעוד במשחק.

    === "Python"
        ```python title="prob, corr, expected_tosses" linenums="1" hl_lines="17 21"
        from fractions import Fraction

        FAIR = {"H": Fraction(1, 2), "T": Fraction(1, 2)}


        def prob(w: str, p: dict) -> Fraction:
            """The probability of the letters of w, p[c] the probability of the letter c."""
            r = Fraction(1)
            for c in w:
                r *= p[c]
            return r


        def corr(a: str, b: str, p: dict = FAIR) -> Fraction:
            """Conway's correlation: 1 / P(the first k letters of b) for every k for which
            the last k letters of a are the first k letters of b."""
            return sum((1 / prob(b[:k], p) for k in range(1, min(len(a), len(b)) + 1) if a[-k:] == b[:k]), Fraction(0))   # (1)!


        def expected_tosses(w: str, p: dict = FAIR) -> Fraction:
            return corr(w, w, p)   # (2)!
        ```

        1. ‏`a[-k:]` היא הסיומת באורך \( k \) ו-`b[:k]` התחילית באורך \( k \).
        2. הרצף מול עצמו : כל חפיפה באורך \( k \) היא מהמר שעוד במשחק.

    #### למה זה נכון { .sol-proof }

    **הקזינו הוגן לאורך כל המשחק.** הרווח הכולל של הקזינו אחרי \( t \) הטלות, \( M_t \),
    הוא מרטינגל : כל הימור הוגן, ולכן \( E[M_{t+1} \mid \text{past}] = M_t \). זמן העצירה
    \( T \) הוא בעל תוחלת סופית (בכל \( L \) הטלות יש סיכוי \( P(A) > 0 \) לרצף), והשינוי
    בכל צעד חסום, ולכן לפי משפט העצירה האופציונלית \( E[M_T] = M_0 = 0 \).

    **מה הקזינו קיבל ומה שילם.** עד \( T \) הגיעו \( T \) מהמרים, ולכן הקזינו קיבל
    \( T \). ברגע \( T \) הקזינו "חייב" למהמרים שעוד במשחק את מה שיש להם, ולפי הרעיון
    שלמעלה זה \( \sum_{k \in \text{overlaps}} 1/P(A_{1..k}) \), מספר קבוע. לכן
    \( 0 = E[M_T] = E[T] - \sum 1/P(A_{1..k}) \).

    **בדיקה מול סעיף א ומול שרשרת המצבים.** ‏`HT` : רק \( k = 2 \), ולכן 4. ‏`HH` :
    ‏\( k = 1, 2 \), ולכן 6. הטסטים של השאלה פותרים את שרשרת המצבים בשברים מדויקים לכל
    רצף עד אורך 8, במטבע הוגן, במטבעות לא הוגנים ובקובייה, ומשווים לנוסחה.

    #### סיבוכיות { .sol-cost }

    לכל \( k \) משווים שתי מחרוזות באורך \( k \), כלומר \( O(L^2) \) בסך הכול. אפשר
    \( O(L) \) עם פונקציית הכישלון של KMP : החפיפות של הרצף עם עצמו הן בדיוק השרשרת
    \( L, fail(L), fail(fail(L)), \dots \).

---

### סעיף ג – מירוץ בין כמה רצפים

אחד בוחר `HH` והשני `HT`, ומטילים עד שאחד הרצפים מופיע. מה הסיכוי של כל אחד? ואם יש
שלושה שחקנים או יותר, כל אחד עם רצף משלו?

??? tip "רמז 1"
    שניהם צריכים `H` קודם. מה קורה בהטלה שאחרי ה-`H` הראשון?

??? tip "רמז 2"
    לכלל : קבוצה של מהמרים לכל רצף. כל קבוצה נותנת משוואה של \( E[T] \) כפונקציה של
    הסיכויים לנצח, ויחד עם "הסיכויים מסתכמים ל-1" יש מספיק משוואות.

<div class="selfcheck" data-answer="1/2" data-show="1/2" data-hint="שני הרצפים מתחילים ב-H. אחרי ה-H הראשון, ההטלה הבאה מכריעה." markdown>
מה הסיכוי ש-`HT` מופיע לפני `HH`?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏`HH` מול `HT` : חצי לכל אחד, למרות ש-`HT` מופיע מהר יותר בממוצע. בכלל, עם רצפים
        \( A_1, \dots, A_m \) (אף אחד לא בתוך אחר) והסיכויים \( p_i \) לנצח :
        \( \sum_i p_i \cdot A_i A_j = E[T] \) לכל \( j \), ו-\( \sum_i p_i = 1 \), כאשר
        \( A_i A_j \) הוא `corr(A_i, A_j)`. שני שחקנים : ‏`THH` מנצח את `HHH` בסיכוי 7/8.
        שלושה : ‏`HHH`, ‏`HTH` ו-`THH` מנצחים ב-1/8, ‏5/12 ו-11/24, והמירוץ נמשך 16/3 בממוצע.

    <!-- cost: זמן \( O(m^2 L^2 + m^3) \) -->

    #### הרעיון { .sol-idea }

    **‏HH מול HT.** עד ה-`H` הראשון אף אחד לא מתקדם. מיד אחריו, `H` נותן `HH` ו-`T` נותן
    `HT`. חצי לכל אחד. התוחלת של `HT` קטנה יותר כי `HH` "מבזבז" זמן כשהוא נכשל, אבל
    במירוץ שניהם מתחילים יחד מאותו `H`, ואין למי לבזבז זמן.

    **הכלל.** לכל רצף \( A_j \) יש קבוצה של מהמרים שמהמרת עליו, כמו בסעיף ב. יהי \( p_i \)
    הסיכוי ש-\( A_i \) מופיע ראשון. כשהמירוץ נגמר ב-\( A_i \), הקבוצה של \( A_j \) מחזיקה
    בדיוק \( A_i A_j \) : המהמרים שהתחילו בסיומת של \( A_i \) שהיא תחילית של \( A_j \).
    כל קבוצה משחקת בקזינו הוגן ומשלמת שקל לכל הטלה, ולכן לכל \( j \) :

    \[
    E[T] = \sum_{i=1}^{m} p_i \cdot A_i A_j
    \]

    אלה \( m \) משוואות, ועם \( \sum_i p_i = 1 \) יש \( m + 1 \) משוואות ל-\( m + 1 \)
    הנעלמים \( p_1, \dots, p_m, E[T] \). לשני רצפים, חיסור שתי המשוואות נותן את הנוסחה של
    Conway : \( p_1 (AA - AB) = p_2 (BB - BA) \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מטריצה :** ‏\( m \times m \) של `corr(A_i, A_j)`.
    2. **משוואות :** לכל \( j \), \( \sum_i p_i \, \mathrm{corr}(A_i, A_j) - E = 0 \); ועוד
       \( \sum_i p_i = 1 \).
    3. **פתרון :** אלימינציה של גאוס על \( m + 1 \) משוואות.
    4. **תנאי :** אף רצף לא מופיע בתוך אחר, אחרת הרצף הפנימי תמיד מנצח (או משתתף בתיקו).

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="race" linenums="1" hl_lines="10 11 13 14"
        // the chance that each pattern appears first (win) and the expected length of the
        // race, from Conway's equations; no pattern inside another, at most 8 patterns
        function automatic real race(string pats[$], real p[byte], ref real win[$]);
          int  m = pats.size();
          real a[9][10];                                         // m + 1 equations, the last column is the right side
          real f, t;
          int  r;
          for (int j = 0; j <= m; j++) for (int i = 0; i <= m + 1; i++) a[j][i] = 0.0;
          for (int j = 0; j < m; j++) begin
            for (int i = 0; i < m; i++) a[j][i] = corr(pats[i], pats[j], p);   // (1)!
            a[j][m] = -1.0;                                      // - E[T]
          end
          for (int i = 0; i < m; i++) a[m][i] = 1.0;              // (2)!
          a[m][m + 1] = 1.0;
          for (int c = 0; c <= m; c++) begin                     // Gauss-Jordan with a pivot
            r = c;
            for (int i = c + 1; i <= m; i++) if (a[i][c] * a[i][c] > a[r][c] * a[r][c]) r = i;   // the largest |a|
            for (int i = 0; i <= m + 1; i++) begin t = a[c][i]; a[c][i] = a[r][i]; a[r][i] = t; end
            for (int i = 0; i <= m; i++)
              if (i != c) begin
                f = a[i][c] / a[c][c];
                for (int k = c; k <= m + 1; k++) a[i][k] -= f * a[c][k];
              end
          end
          win = {};
          for (int i = 0; i < m; i++) win.push_back(a[i][m + 1] / a[i][i]);
          return a[m][m + 1] / a[m][m];
        endfunction
        ```

        1. כשהמירוץ נגמר ב-\( A_i \), הקבוצה שמהמרת על \( A_j \) מחזיקה `corr(A_i, A_j)`.
        2. השורה האחרונה : הסיכויים מסתכמים ל-1.

    === "Python"
        ```python title="race" linenums="1" hl_lines="7 9"
        def race(pats: list[str], p: dict = FAIR) -> tuple[list[Fraction], Fraction]:
            """The chance that each pattern appears first, and the expected length of the race
            (Conway's equations; no pattern inside another)."""
            m = len(pats)
            rows = []
            for j in range(m):
                rows.append([corr(pats[i], pats[j], p) for i in range(m)] + [Fraction(-1), Fraction(0)])   # (1)!
            rows.append([Fraction(1)] * m + [Fraction(0), Fraction(1)])
            for c in range(m + 1):                                  # (2)!
                piv = next(i for i in range(c, m + 1) if rows[i][c] != 0)
                rows[c], rows[piv] = rows[piv], rows[c]
                for i in range(m + 1):
                    if i != c and rows[i][c] != 0:
                        f = rows[i][c] / rows[c][c]
                        rows[i] = [x - f * y for x, y in zip(rows[i], rows[c])]
            x = [rows[i][m + 1] / rows[i][i] for i in range(m + 1)]
            return x[:m], x[m]
        ```

        1. לכל \( j \) : ‏\( \sum_i p_i \cdot \mathrm{corr}(A_i, A_j) - E = 0 \).
        2. אלימינציה של גאוס-ז'ורדן בשברים מדויקים.

    #### למה זה נכון { .sol-proof }

    **‏HH מול HT במשוואות.** ‏\( AA = 6 \), ‏\( AB = 2 \) (ה-`H` האחרון של `HH` הוא תחילת
    `HT`), ‏\( BB = 4 \), ‏\( BA = 0 \). המשוואות : \( 6 p_1 + 0 p_2 = E \),
    \( 2 p_1 + 4 p_2 = E \), ‏\( p_1 + p_2 = 1 \). מכאן \( p_1 = p_2 = \frac12 \) ו-\( E = 3 \).

    **משחק Penney.** כשהיריב בוחר רצף באורך 3, תמיד יש רצף שמנצח אותו בסיכוי 2/3 לפחות.
    המתכון : לוקחים את שתי האותיות הראשונות של היריב, ומוסיפים לפניהן את ההפך של האות
    השנייה. ההסתברויות בטבלה חושבו בשרשרת מדויקת של שלוש ההטלות האחרונות, והן מסכימות
    עם המשוואות :

    <!-- gen 7 -->

    | היריב בוחר | התשובה הטובה ביותר | הסיכוי שהתשובה מופיעה קודם |
    |:-:|:-:|:-:|
    | ‏`HHH` | ‏`THH` | ‏7/8 |
    | ‏`HHT` | ‏`THH` | ‏3/4 |
    | ‏`HTH` | ‏`HHT` | ‏2/3 |
    | ‏`HTT` | ‏`HHT` | ‏2/3 |
    | ‏`THH` | ‏`TTH` | ‏2/3 |
    | ‏`THT` | ‏`TTH` | ‏2/3 |
    | ‏`TTH` | ‏`HTT` | ‏3/4 |
    | ‏`TTT` | ‏`HTT` | ‏7/8 |

    <!-- /gen -->

    היחס "מנצח את" לא טרנזיטיבי : ‏`THH` מנצח את `HHT`, ‏`TTH` מנצח את `THH`, ‏`HTT`
    מנצח את `TTH`, ו-`HHT` מנצח את `HTT`. מי שבוחר שני תמיד בעדיפות.

    **שלושה שחקנים.** הסיכוי לנצח לא נקבע לפי התוחלת של כל רצף לבד : ‏`HTH` (תוחלת 10)
    מנצח הרבה יותר מ-`HHH` (תוחלת 14), אבל `THH` (תוחלת 8) מנצח רק קצת יותר מ-`HTH` :

    <!-- gen 8 -->

    | הרצף | התוחלת לבד | הסיכוי לנצח במירוץ |
    |:-:|:-:|:-:|
    | ‏`HHH` | ‏14 | ‏1/8 |
    | ‏`HTH` | ‏10 | ‏5/12 |
    | ‏`THH` | ‏8 | ‏11/24 |
    | המירוץ כולו | ‏16/3 | ‏1 |

    <!-- /gen -->

    **נסו בעצמכם.** בוחרים מטבע הוגן, מטבע עם \( q \) או קובייה, מקלידים רצף (ואם רוצים,
    רצף יריב למירוץ), ומטילים ביד, באקראי או בהפעלה רציפה. גרף המצבים מראה איפה הרצף
    נמצא, והשורה מראה כמה הטלות עברו במשחק הנוכחי. ‏"1000 משחקים" מריץ אלף משחקים ומשווה
    את הממוצע ואת ההיסטוגרמה לחישוב המדויק :

    <div class="explorer" data-kind="coins" data-a="HH" data-b="HT"></div>

---

### סעיף ד – ההתפלגות כולה : פונקציה יוצרת

התוחלת היא מספר אחד. מהי ההתפלגות של \( T \) כולה? מצאו את הפונקציה היוצרת
\( G(z) = E[z^T] = \sum_t P(T = t) z^t \), ומתוכה את השונות ואת \( P(T = t) \) לכל \( t \).

??? tip "רמז 1"
    קחו רצף הטלות באורך \( n \) שעוד לא הכיל את \( A \), והוסיפו לו את \( A \) כולו. איפה
    יכולה להיגמר ההופעה **הראשונה** של \( A \) ברצף החדש?

??? tip "רמז 2"
    היא נגמרת בתוך ה-\( A \) שהוספתם, במרחק \( k \) מתחילתו, רק אם \( k \) הוא אורך של
    חפיפה. זה נותן משוואה בין \( P(T > n) \) לבין \( P(T = n + k) \).

<div class="selfcheck" data-answer="22" data-show="22" data-hint="מהפונקציה היוצרת : השונות היא G''(1) + G'(1) − G'(1)², או מהטבלה של התוחלת והשונות." markdown>
מה השונות של מספר ההטלות עד `HH`?
</div>

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        ‏\( G(z) = \dfrac{P(A) z^L}{P(A) z^L + (1 - z) C(z)} \), כאשר
        \( C(z) = \sum_{k \in \text{overlaps}} P(A_{k+1..L}) \, z^{L-k} \) הוא פולינום החפיפות
        (ההסתברות של מה שנשאר מ-\( A \) אחרי החפיפה). ממנו : \( E[T] = C(1)/P(A) \) כמו
        בסעיף ב, השונות \( G''(1) + G'(1) - G'(1)^2 \) (ל-`HH` : ‏22), ו-\( P(T = t) \) מנוסחת
        נסיגה אחת.

    <!-- cost: ההתפלגות עד t \( O(tL) \) | זיכרון \( O(t) \) -->

    #### הרעיון { .sol-idea }

    **להוסיף את הרצף.** קחו כל רצף הטלות באורך \( n \) שעוד לא הכיל את \( A \)
    (ההסתברות של כולם יחד היא \( P(T > n) \)), והוסיפו בסופו את \( A \). ברצף החדש \( A \)
    מופיע בוודאות, וההופעה **הראשונה** שלו נגמרת באחת מ-\( L \) העמדות של ה-\( A \)
    שהוספנו. אם היא נגמרת בעמדה \( k \) של ה-\( A \) הזה, אז \( k \) האותיות האחרונות
    של \( A \) הן \( k \) הראשונות שלו, כלומר \( k \) הוא אורך של חפיפה, ואחרי ההופעה
    הראשונה באות בדיוק האותיות \( A_{k+1..L} \).

    **המשוואה.** לכל \( n \ge 0 \) :

    \[
    P(T > n) \, P(A) = \sum_{k \in \text{overlaps}} P(T = n + k) \, P(A_{k+1..L})
    \]

    מכפילים ב-\( z^{n+L} \) ומסכמים על \( n \). בצד שמאל מתקבל \( P(A) z^L Q(z) \), כאשר
    \( Q(z) = \sum_n P(T > n) z^n = \frac{1 - G(z)}{1 - z} \); בצד ימין \( C(z) \, G(z) \).
    פותרים ל-\( G \) ומקבלים את הנוסחה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏C(z) :** לכל חפיפה באורך \( k \) מוסיפים \( P(A_{k+1..L}) z^{L-k} \). החפיפה
       \( k = L \) נותנת את האיבר הקבוע 1.
    2. **המכנה :** ‏\( D(z) = P(A) z^L + (1 - z) C(z) \), פולינום ממעלה \( L + 1 \) לכל
       היותר, עם \( D(0) = 1 \).
    3. **ההתפלגות :** מ-\( D(z) G(z) = P(A) z^L \) :
       \( g_t = P(A)[t = L] - \sum_{j \ge 1} d_j \, g_{t-j} \), כאשר \( g_t = P(T = t) \).
    4. **מומנטים :** ‏\( G'(1) \) ו-\( G''(1) \) מהנגזרות של המונה והמכנה ב-\( z = 1 \).

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="wait_dist" linenums="1" hl_lines="9 10 15 16"
        // P(T = t) for t = 0 .. n-1, from D(z) G(z) = P(w) z^L
        function automatic void wait_dist(string w, real p[byte], int n, ref real g[$]);
          int  L = w.len();
          real c[$], d[$], s;
          c = {}; repeat (L + 1) c.push_back(0.0);
          d = {}; repeat (L + 2) d.push_back(0.0);
          for (int k = 1; k <= L; k++)
            if (w.substr(L - k, L - 1) == w.substr(0, k - 1))
              c[L - k] += prob(w, k, L, p);                       // (1)!
          for (int i = 0; i <= L; i++) begin d[i] += c[i]; d[i + 1] -= c[i]; end
          d[L] += prob(w, 0, L, p);
          g = {};                                                 // (2)!
          for (int t = 0; t < n; t++) begin
            s = (t == L) ? prob(w, 0, L, p) : 0.0;
            for (int j = 1; j <= L + 1 && j <= t; j++) s -= d[j] * g[t - j];
            g.push_back(s / d[0]);                                // (3)!
          end
        endfunction
        ```

        1. האיבר של החפיפה באורך \( k \) ב-\( C(z) \) : מה שנשאר מ-\( A \), כפול \( z^{L-k} \).
        2. ‏\( D(z) = P(A) z^L + (1 - z) C(z) \) נבנה בשתי השורות שלמעלה.
        3. ‏\( d_0 = 1 \), אבל החלוקה משאירה את הקוד נכון גם בלי לסמוך על זה.

    === "Python"
        ```python title="generating, wait_dist, wait_moments" linenums="1" hl_lines="7 13 22 32 33"
        def generating(w: str, p: dict = FAIR) -> tuple[list[Fraction], list[Fraction]]:
            """G(z) = E[z^T] as (numerator, denominator), coefficients from z^0 up."""
            L, P = len(w), prob(w, p)
            c = [Fraction(0)] * (L + 1)
            for k in range(1, L + 1):
                if w[-k:] == w[:k]:
                    c[L - k] += prob(w[k:], p)                      # (1)!
            d = [Fraction(0)] * (L + 2)
            for i, ci in enumerate(c):
                d[i] += ci
                d[i + 1] -= ci
            d[L] += P
            return [Fraction(0)] * L + [P], d                       # (2)!


        def wait_dist(w: str, p: dict = FAIR, n: int = 20) -> list[Fraction]:
            """P(T = t) for t = 0 .. n-1."""
            num, d = generating(w, p)
            g = []
            for t in range(n):
                s = num[t] if t < len(num) else Fraction(0)
                s -= sum(d[j] * g[t - j] for j in range(1, min(len(d) - 1, t) + 1))
                g.append(s / d[0])
            return g


        def wait_moments(w: str, p: dict = FAIR) -> tuple[Fraction, Fraction]:
            """E[T] and Var(T) from G'(1) and G''(1)."""
            num, d = generating(w, p)
            at = lambda f, r: sum(c * prod_range(i, r) for i, c in enumerate(f))   # noqa: E731
            N, N1, N2, D, D1, D2 = at(num, 0), at(num, 1), at(num, 2), at(d, 0), at(d, 1), at(d, 2)
            g1 = (N1 * D - N * D1) / D ** 2                         # (3)!
            g2 = (N2 * D - N * D2) / D ** 2 - 2 * D1 * (N1 * D - N * D1) / D ** 3
            return g1, g2 + g1 - g1 ** 2


        def prod_range(i: int, r: int) -> int:
            """The r-th derivative of z^i at z = 1: i (i - 1) ... (i - r + 1)."""
            out = 1
            for j in range(r):
                out *= i - j
            return out
        ```

        1. האיבר של החפיפה באורך \( k \) : ההסתברות של מה שנשאר מ-\( A \), כפול \( z^{L-k} \).
        2. המונה \( P(A) z^L \), והמכנה \( P(A) z^L + (1 - z) C(z) \).
        3. נגזרת של מנה, ב-\( z = 1 \), שם \( G(1) = 1 \).

    #### למה זה נכון { .sol-proof }

    **המשוואה.** לכל רצף \( x \) באורך \( n \) בלי \( A \), ההופעה הראשונה של \( A \)
    ב-\( xA \) נגמרת בעמדה \( n + k \) עם \( 1 \le k \le L \). ההופעה הזו וה-\( A \) שהוספנו
    חופפות ב-\( k \) אותיות, ולכן \( k \) הוא אורך של חפיפה. להפך, לכל \( k \) כזה, המאורע
    "\( T = n + k \) ואחריו באות \( A_{k+1..L} \)" נותן בדיוק רצף מהצורה \( xA \). סוכמים
    על כל \( x \) ומקבלים את המשוואה של הרעיון.

    **הבדיקה ב-HH.** ‏\( P(A) = \frac14 \), ‏\( C(z) = 1 + \frac{z}{2} \), ולכן
    \( D(z) = 1 - \frac{z}{2} - \frac{z^2}{4} \) והנסיגה \( g_t = \frac12 g_{t-1} + \frac14 g_{t-2} \)
    (מ-\( g_2 = \frac14 \)), שזה בדיוק \( F_{t-1} / 2^t \) של סעיף א.

    **התוחלת והשונות.** ‏\( G'(1) = C(1)/P(A) \), אותה נוסחה כמו בסעיף ב. השונות גדלה מהר
    הרבה יותר מהתוחלת, וסטיית התקן קרובה לתוחלת : זמן ההמתנה מתנהג כמעט כמו התפלגות
    גאומטרית. הטבלה חושבה בשרשרת המצבים, בשברים מדויקים, והיא מסכימה עם הקוד :

    <!-- gen 9 -->

    | הרצף | התוחלת | השונות | סטיית התקן |
    |:-:|:-:|:-:|:-:|
    | ‏`HT` | ‏4 | ‏4 | ‏2.00 |
    | ‏`HH` | ‏6 | ‏22 | ‏4.69 |
    | ‏`HTH` | ‏10 | ‏58 | ‏7.62 |
    | ‏`HHH` | ‏14 | ‏142 | ‏11.92 |
    | ‏`HHHH` | ‏30 | ‏734 | ‏27.09 |

    <!-- /gen -->

    #### סיבוכיות { .sol-cost }

    בניית \( C(z) \) היא \( O(L^2) \). כל איבר של ההתפלגות עולה \( O(L) \), כי למכנה
    \( L + 2 \) מקדמים. המומנטים הם כמה סכומים על \( L + 2 \) מקדמים.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : ״לשני הרצפים אותה הסתברות, אז אותה תוחלת״"
    ההסתברות שזוג הטלות מסוים הוא `HH` שווה להסתברות שהוא `HT`, ולכן בטווח הארוך שניהם
    מופיעים באותה תדירות. זמן ההמתנה להופעה **הראשונה** תלוי בחפיפות : הופעות של `HH`
    מתקבצות, ולכן הרווחים לפניהן ארוכים יותר.

??? trap "מלכודת : ״התוחלת הקטנה מנצחת במירוץ״"
    ‏`HT` מגיע בממוצע אחרי 4 הטלות ו-`HH` אחרי 6, ובכל זאת במירוץ ביניהם הסיכוי חצי.
    ב-`HHH` מול `THH` ההבדל דרמטי : התוחלות 14 ו-8, אבל `THH` מנצח פי 7.

??? trap "מלכודת : לשכוח את מצב החפיפה במשוואות"
    מי שכותב ל-`HH` "אחרי `T` חוזרים להתחלה" צודק, אבל מי שכותב אותו דבר ל-`HT` ("אחרי
    `H` שלא מתאים חוזרים להתחלה") יקבל 6 במקום 4. ‏`HH` שאינו `HT` מסתיים ב-`H`, שהוא
    כבר תחילת הרצף, בדיוק כמו נסיגה בגלאי רצף.

??? trap "מלכודת : מירוץ שבו רצף אחד בתוך אחר"
    ‏`HT` מול `HHT` : כל הופעה של `HHT` מכילה `HT` שמסתיים באותו רגע, ולכן `HHT` לא יכול
    לנצח, והמשוואות של סעיף ג מתנוונות. בודקים את התנאי לפני שפותרים.

??? followup "שאלות המשך"
    - **קובייה :** כמה הטלות בממוצע עד `66`? ועד `12`?

        ??? fu-answer "תשובה"
            ל-`66` יש חפיפות באורכים 1 ו-2, ולכן \( 6 + 36 = 42 \). ל-`12` יש רק את הרצף כולו, ולכן
            36. אותה סיבה כמו `HH` מול `HT`.

    - **כיסוי בטסט אקראי :** ‏stimulus אקראי של ביטים הוגנים, ורוצים לראות `1011` לפחות
      פעם אחת. כמה מחזורים בממוצע?

        ??? fu-answer "תשובה"
            החפיפות של `1011` עם עצמו הן באורכים 1 ו-4, ולכן \( 2 + 16 = 18 \) מחזורים. ל-`1111`
            צריך \( 2 + 4 + 8 + 16 = 30 \).

    - **כמה רצפים ב-stimulus :** רוצים לראות גם `1011` וגם `0110`. כמה מחזורים עד שמופיע
      **אחד** מהם, ואיזה מופיע קודם?

        ??? fu-answer "תשובה"
            המירוץ של סעיף ג, ‏`race(["1011", "0110"])` : אחד מהם מופיע אחרי 73/6 ≈ 12.2 מחזורים
            בממוצע, ו-`1011` קודם בסיכוי 7/12. עד ששניהם מופיעים : \( \max + \min = T_A + T_B \), ולכן
            \( E[\max] = 18 + 18 - 73/6 = 143/6 \approx 23.8 \), גם כשהזמנים תלויים.

    - **הכי הרבה זמן :** איזה רצף באורך \( L \) מחכה הכי הרבה, ואיזה הכי מעט?

        ??? fu-answer "תשובה"
            הכי הרבה : רצף של אות אחת (`HHH...`), עם \( 2^{L+1} - 2 \). הכי מעט : רצף בלי חפיפות
            עצמיות (למשל `HH...HT`), עם \( 2^L \).
