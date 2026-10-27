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
- **סעיף ב – כל רצף :** כתבו קוד שמחשב את מספר ההטלות הממוצע לכל רצף של H ו-T,
  והסבירו את הנוסחה. כמה זה ל-`HHH`?
- **סעיף ג – מירוץ :** שני שחקנים מטילים אותו מטבע; אחד בוחר `HH` והשני `HT`, ומנצח
  מי שהרצף שלו מופיע קודם. מה הסיכוי של כל אחד? ומה קורה כשבוחרים רצפים באורך 3?

??? interviewer "מה המראיין בודק"
    - **מצבים במקום מקרים :** האם המועמד מגדיר מצב לפי "כמה מהרצף כבר נבנה", כמו בגלאי
      רצף בחומרה, וכותב משוואה לכל מצב.
    - **הבחנה בין "באותה הסתברות" ל"באותו זמן" :** ‏`HH` ו-`HT` מופיעים בכל מקום
      בהסתברות 1/4, ובכל זאת זמני ההמתנה שונים. האם הוא מסביר למה.
    - **הכללה :** האם הוא מגיע לנוסחה שתלויה רק בחפיפות של הרצף עם עצמו.
    - **אינטואיציה מטעה :** במירוץ, האם הוא נופל ל"הרצף עם התוחלת הקטנה מנצח".
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

### סעיף ב – כל רצף

כתבו קוד שמחשב את מספר ההטלות הממוצע לכל רצף, והסבירו את הנוסחה.

??? tip "רמז 1"
    בדקו את התוצאות של סעיף א מול החפיפות של הרצף עם עצמו : ל-`HT` אין חפיפה חוץ מהרצף
    כולו, ול-`HH` יש גם חפיפה באורך 1.

??? tip "רמז 2"
    דמיינו קזינו הוגן : לפני כל הטלה מגיע מהמר חדש עם שקל, ומהמר על האות הראשונה של
    הרצף; אם הוא זוכה, הוא מהמר על כל מה שיש לו על האות השנייה, וכן הלאה. כמה כסף יש
    למהמרים ברגע שהרצף מופיע?

<div class="selfcheck" data-answer="14" data-show="14 = 2 + 4 + 8" data-hint="ל-HHH יש חפיפות עם עצמו באורכים 1, 2 ו-3. כל חפיפה באורך k תורמת 2 בחזקת k." markdown>
מה מספר ההטלות הממוצע עד `HHH`?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏\( E[T] = \sum_k 2^k \) על כל אורך \( k \) שבו \( k \) האותיות האחרונות של הרצף שוות
        ל-\( k \) הראשונות (כולל \( k = L \)). ‏`HT` : ‏\( 4 \). ‏`HH` : ‏\( 2 + 4 = 6 \). ‏`HHH` :
        ‏\( 2 + 4 + 8 = 14 \). הנוסחה נובעת מטיעון המהמרים בקזינו הוגן.

    <!-- cost: זמן \( O(L^2) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **קזינו הוגן.** לפני כל הטלה מגיע מהמר חדש עם שקל אחד, ומהמר על כך שההטלה הבאה
    היא האות הראשונה של הרצף. אם הוא צודק יש לו 2, והוא מהמר על כל הסכום על האות
    השנייה; אם הוא צודק שוב יש לו 4, וכן הלאה. מהמר שטועה מפסיד הכול ויוצא, ומהמר
    שהשלים את כל הרצף מסיים עם \( 2^L \).

    **ברגע שהרצף מופיע** (הטלה \( T \)), הקזינו קיבל \( T \) שקלים, אחד מכל מהמר. מי
    שעדיין במשחק? המהמר שהתחיל לפני \( L \) הטלות והשלים את כל הרצף, עם \( 2^L \); וכל
    מהמר שהתחיל לפני \( k \) הטלות ושעד עכשיו צדק, כלומר כל \( k \) שבו \( k \) האותיות
    האחרונות של הרצף הן \( k \) הראשונות שלו. לכל אחד מהם \( 2^k \).

    **המשחק הוגן**, ולכן בממוצע הקזינו לא מרוויח ולא מפסיד : התוחלת של מה שקיבל שווה
    לתוחלת של מה ששילם. מה ששולם לא תלוי במזל, רק ברצף. לכן
    \( E[T] = \sum_{k \in \text{overlaps}} 2^k \).

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

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **חפיפות :** לכל \( k = 1, \dots, L \) בודקים אם \( k \) האותיות האחרונות שוות
       ל-\( k \) הראשונות.
    2. **סכום :** כל חפיפה באורך \( k \) מוסיפה \( 2^k \). החפיפה \( k = L \) תמיד קיימת
       ותורמת \( 2^L \).
    3. **מטבע לא הוגן :** במקום \( 2^k \) מוסיפים \( 1 / P(\text{prefix}_k) \), ההסתברות
       של \( k \) האותיות הראשונות.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="corr, expected_tosses" linenums="1" hl_lines="5 6"
        // Conway's correlation of a over b: the sum of 2^k over every k for which
        // the last k letters of a are the first k letters of b
        function automatic longint corr(string a, string b);
          longint v = 0;
          for (int k = 1; k <= a.len() && k <= b.len(); k++)
            if (a.substr(a.len() - k, a.len() - 1) == b.substr(0, k - 1)) v += longint'(1) << k;   // (1)!
          return v;
        endfunction

        // the expected number of fair tosses until the pattern first appears
        function automatic longint expected_tosses(string p);
          return corr(p, p);                                  // (2)!
        endfunction
        ```

        1. ‏`substr(i, j)` כולל את שני הקצוות : הסיומת באורך \( k \) של `a` מול התחילית באורך \( k \) של `b`.
        2. הרצף מול עצמו : כל חפיפה באורך \( k \) היא מהמר שעוד במשחק עם \( 2^k \).

    === "Python"
        ```python title="corr, expected_tosses" hl_lines="4 9"
        def corr(a: str, b: str) -> int:
            """Conway's correlation: the sum of 2**k over every k for which the last k
            letters of a are the first k letters of b."""
            return sum(2 ** k for k in range(1, min(len(a), len(b)) + 1) if a[-k:] == b[:k])   # (1)!


        def expected_tosses(p: str) -> int:
            """The expected number of fair tosses until p first appears."""
            return corr(p, p)   # (2)!
        ```

        1. ‏`a[-k:]` היא הסיומת באורך \( k \) ו-`b[:k]` התחילית באורך \( k \).
        2. הרצף מול עצמו : כל חפיפה באורך \( k \) היא מהמר שעוד במשחק עם \( 2^k \).

    #### למה זה נכון { .sol-proof }

    **הקזינו הוגן לאורך כל המשחק.** הרווח הכולל של הקזינו אחרי \( t \) הטלות, \( M_t \),
    הוא מרטינגל : כל הימור הוגן, ולכן \( E[M_{t+1} \mid \text{past}] = M_t \). זמן העצירה
    \( T \) הוא בעל תוחלת סופית (בכל \( L \) הטלות יש סיכוי \( 2^{-L} \) לרצף), והשינוי
    בכל צעד חסום, ולכן לפי משפט העצירה האופציונלית \( E[M_T] = M_0 = 0 \).

    **מה הקזינו קיבל ומה שילם.** עד \( T \) הגיעו \( T \) מהמרים, ולכן הקזינו קיבל
    \( T \). ברגע \( T \) הקזינו "חייב" למהמרים שעוד במשחק את מה שיש להם, ולפי הרעיון
    שלמעלה זה \( \sum_{k \in \text{overlaps}} 2^k \), מספר קבוע. לכן
    \( 0 = E[M_T] = E[T] - \sum 2^k \).

    **בדיקה מול סעיף א.** ‏`HT` : רק \( k = 2 \), ולכן 4. ‏`HH` : ‏\( k = 1, 2 \), ולכן 6.
    הנוסחה מסכימה עם פתרון המשוואות, וגם עם פתרון מדויק של שרשרת המצבים בטסטים של השאלה
    לכל הרצפים עד אורך 8.

    #### סיבוכיות { .sol-cost }

    לכל \( k \) משווים שתי מחרוזות באורך \( k \), כלומר \( O(L^2) \) בסך הכול. אפשר
    \( O(L) \) עם פונקציית הכישלון של KMP : החפיפות של הרצף עם עצמו הן בדיוק השרשרת
    \( L, fail(L), fail(fail(L)), \dots \).

---

### סעיף ג – מירוץ בין שני רצפים

אחד בוחר `HH` והשני `HT`, ומטילים עד שאחד הרצפים מופיע. מה הסיכוי של כל אחד?

??? tip "רמז 1"
    שניהם צריכים `H` קודם. מה קורה בהטלה שאחרי ה-`H` הראשון?

??? tip "רמז 2"
    לכלל : שתי קבוצות של מהמרים, אחת מהמרת על כל רצף. כל קבוצה נותנת משוואה של \( E[T] \)
    כפונקציה של \( p \), הסיכוי שהרצף הראשון מנצח.

<div class="selfcheck" data-answer="1/2" data-show="1/2" data-hint="שני הרצפים מתחילים ב-H. אחרי ה-H הראשון, ההטלה הבאה מכריעה." markdown>
מה הסיכוי ש-`HT` מופיע לפני `HH`?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        חצי לכל אחד, למרות ש-`HT` מופיע מהר יותר בממוצע : אחרי ה-`H` הראשון, ההטלה הבאה
        מכריעה. בכלל, \( P(A \text{ first}) = \frac{BB - BA}{(AA - AB) + (BB - BA)} \), כאשר
        \( XY \) הוא `corr(X, Y)`. ברצפים באורך 3 לכל בחירה יש תשובה שמנצחת אותה :
        ‏`THH` מנצח את `HHH` בסיכוי 7/8.

    <!-- cost: זמן \( O(L^2) \) -->

    #### הרעיון { .sol-idea }

    **‏HH מול HT.** עד ה-`H` הראשון אף אחד לא מתקדם. מיד אחריו, `H` נותן `HH` ו-`T` נותן
    `HT`. חצי לכל אחד. התוחלת של `HT` קטנה יותר כי `HH` "מבזבז" זמן כשהוא נכשל, אבל
    במירוץ שניהם מתחילים יחד מאותו `H`, ואין למי לבזבז זמן.

    **הכלל.** קבוצה אחת של מהמרים מהמרת על \( A \) וקבוצה שנייה על \( B \), כמו בסעיף ב.
    יהי \( p \) הסיכוי ש-\( A \) מופיע קודם. כשהמשחק נגמר ב-\( A \), למהמרים על \( A \)
    יש \( AA \), ולמהמרים על \( B \) יש \( AB \) (סיומות של \( A \) שהן תחיליות של \( B \)).
    כשהוא נגמר ב-\( B \), יש להם \( BA \) ו-\( BB \). כל קבוצה משחקת בקזינו הוגן, ולכן :

    \[
    \begin{aligned}
    E[T] &= p \cdot AA + (1 - p) \cdot BA \\
    E[T] &= p \cdot AB + (1 - p) \cdot BB
    \end{aligned}
    \]

    משווים ומקבלים \( p (AA - AB) = (1 - p)(BB - BA) \).

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="p_first" hl_lines="3 4"
        // the chance that pattern a appears before pattern b (neither inside the other)
        function automatic real p_first(string a, string b);
          longint wa = corr(b, b) - corr(b, a);                   // (1)!
          longint wb = corr(a, a) - corr(a, b);
          return real'(wa) / real'(wa + wb);
        endfunction
        ```

        1. היחס בין הסיכויים של \( A \) ל-\( B \) הוא \( (BB - BA) : (AA - AB) \), הנוסחה של Conway.

    === "Python"
        ```python title="p_first" hl_lines="5"
        from fractions import Fraction


        def p_first(a: str, b: str) -> Fraction:
            wa, wb = corr(b, b) - corr(b, a), corr(a, a) - corr(a, b)   # (1)!
            return Fraction(wa, wa + wb)
        ```

        1. היחס בין הסיכויים של \( A \) ל-\( B \) הוא \( (BB - BA) : (AA - AB) \), הנוסחה של Conway.

    #### למה זה נכון { .sol-proof }

    **‏HH מול HT בנוסחה.** ‏\( AA = 6 \), ‏\( AB = 2 \) (ה-`H` האחרון של `HH` הוא תחילת
    `HT`), ‏\( BB = 4 \), ‏\( BA = 0 \). לכן \( p = \frac{4 - 0}{(6 - 2) + (4 - 0)} = \frac12 \).

    **משחק Penney.** כשהיריב בוחר רצף באורך 3, תמיד יש רצף שמנצח אותו בסיכוי 2/3 לפחות.
    המתכון : לוקחים את שתי האותיות הראשונות של היריב, ומוסיפים לפניהן את ההפך של האות
    השנייה. ההסתברויות בטבלה חושבו בשרשרת מדויקת של שלוש ההטלות האחרונות, והן מסכימות
    עם הנוסחה :

    <!-- gen 6 -->

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

    **נסו בעצמכם.** מקלידים רצף (ואם רוצים, רצף יריב למירוץ), ומטילים ביד, באקראי או
    בהפעלה רציפה. הגרף מראה את המצב של כל רצף, והשורה מראה כמה הטלות עברו במשחק הנוכחי.
    ‏"1000 משחקים" מריץ אלף משחקים ומשווה את הממוצע ואת ההיסטוגרמה לחישוב המדויק :

    <div class="explorer" data-kind="coins" data-a="HH" data-b="HT"></div>

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

??? followup "שאלות המשך"
    - **מטבע לא הוגן :** ההסתברות ל-`H` היא \( q \). מה התוחלת עד `HH`?

        ??? fu-answer "תשובה"
            ‏\( \frac{1}{q} + \frac{1}{q^2} \) : במקום \( 2^k \), כל חפיפה תורמת אחד חלקי ההסתברות של
            התחילית שלה. עם \( q = 1/2 \) זה \( 2 + 4 = 6 \).

    - **כיסוי בטסט אקראי :** ‏stimulus אקראי של ביטים הוגנים, ורוצים לראות `1011` לפחות
      פעם אחת. כמה מחזורים בממוצע?

        ??? fu-answer "תשובה"
            החפיפות של `1011` עם עצמו הן באורכים 1 ו-4, ולכן \( 2 + 16 = 18 \) מחזורים. ל-`1111`
            צריך \( 2 + 4 + 8 + 16 = 30 \).

    - **הסטייה :** מה השונות של מספר ההטלות עד `HT`?

        ??? fu-answer "תשובה"
            ‏\( T \) הוא סכום של שתי המתנות גאומטריות עם \( p = 1/2 \) (ל-`H` ואחריו ל-`T`), ולכן
            השונות \( 2 + 2 = 4 \). ל-`HH` השונות 22.

    - **הכי הרבה זמן :** איזה רצף באורך \( L \) מחכה הכי הרבה, ואיזה הכי מעט?

        ??? fu-answer "תשובה"
            הכי הרבה : רצף של אות אחת (`HHH...`), עם \( 2^{L+1} - 2 \). הכי מעט : רצף בלי חפיפות
            עצמיות (למשל `HH...HT`), עם \( 2^L \).
