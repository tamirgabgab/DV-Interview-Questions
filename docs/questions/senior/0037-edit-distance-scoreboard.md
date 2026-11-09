---
id: 37
title: מרחק עריכה בין שני זרמים – מה חסר, מה מיותר ומה שובש, עד d הבדלים, וחבילות שהתחלפו
level: senior
difficulty: medium
kind: code
tags: [algorithms, dynamic-programming, scoreboard, proof, python, systemverilog]
source: "שאלה קלאסית (Edit Distance, LeetCode 72) בהקשר של scoreboard שמשווה זרם צפוי לזרם בפועל; הרצועה של d הבדלים (Ukkonen) וההחלפה של שכנות (Damerau) הן ההכללות המקובלות שלה"
added: 2026-11-07
---

## השאלה

ה-scoreboard ציפה לזרם החבילות `ABCDEFGH`, וה-DUT שלח `ABDEYGHH`. כל אות היא חבילה. השוואה
של מקום מול מקום מוצאת חמש חבילות שונות מתוך שמונה, אבל באמת קרו רק שלושה דברים. **המרחק**
בין שני הזרמים הוא המספר הקטן ביותר של פעולות שהופכות את הזרם הצפוי לזרם בפועל, כשכל פעולה
היא אחת משלוש :

- **חבילה חסרה :** חבילה של הזרם הצפוי שלא הגיעה.
- **חבילה מיותרת :** חבילה שהגיעה ולא הייתה בזרם הצפוי.
- **חבילה ששובשה :** במקום חבילה אחת הגיעה חבילה אחרת.

ב-scoreboard שני הזרמים נאספים לשני תורים : ה-monitor שם בתור `actual` כל חבילה שה-DUT שלח,
וה-reference model שם בתור `expected` כל חבילה שציפה לה. השוואה בכל הגעה, ראש התור מול
החבילה שהגיעה, נתקעת בהבדל הראשון : מ-C והלאה כל חבילה נראית שגויה. לכן ההשוואה כאן רצה
בסוף הבדיקה, על שני התורים המלאים, וכותבת דוח :

<!-- gen 8 -->

<svg class="figure ed-fig ed-flow" viewBox="0 0 372 148" style="max-width:23.25rem" role="img" aria-label="הזרימה ב-scoreboard : ה-monitor שם את מה שה-DUT שלח, ABDEYGHH, בתור actual, ה-reference model שם את מה שציפה, ABCDEFGH, בתור expected, ובסוף הבדיקה diff משווה את שני התורים וכותב דוח"><defs><marker id="ed-flow-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ed-head" d="M0,0 L10,5 L0,10 Z"/></marker></defs><rect class="ed-blk" x="4" y="14" width="52" height="32" rx="5"/><text class="ed-blk-t" x="30" y="34" text-anchor="middle">DUT</text><path class="ed-arr" d="M56,30 L69,30" marker-end="url(#ed-flow-head)"/><rect class="ed-blk" x="70" y="14" width="66" height="32" rx="5"/><text class="ed-blk-t" x="103" y="34" text-anchor="middle">monitor</text><path class="ed-arr" d="M136,30 L149,30" marker-end="url(#ed-flow-head)"/><text class="ed-lab" x="206" y="14" text-anchor="middle">actual</text><rect class="ed-cell" x="150" y="20" width="14" height="20"/><text class="ed-pk" x="157" y="35" text-anchor="middle">A</text><rect class="ed-cell" x="164" y="20" width="14" height="20"/><text class="ed-pk" x="171" y="35" text-anchor="middle">B</text><rect class="ed-cell" x="178" y="20" width="14" height="20"/><text class="ed-pk" x="185" y="35" text-anchor="middle">D</text><rect class="ed-cell" x="192" y="20" width="14" height="20"/><text class="ed-pk" x="199" y="35" text-anchor="middle">E</text><rect class="ed-cell" x="206" y="20" width="14" height="20"/><text class="ed-pk" x="213" y="35" text-anchor="middle">Y</text><rect class="ed-cell" x="220" y="20" width="14" height="20"/><text class="ed-pk" x="227" y="35" text-anchor="middle">G</text><rect class="ed-cell" x="234" y="20" width="14" height="20"/><text class="ed-pk" x="241" y="35" text-anchor="middle">H</text><rect class="ed-cell" x="248" y="20" width="14" height="20"/><text class="ed-pk" x="255" y="35" text-anchor="middle">H</text><rect class="ed-blk" x="4" y="74" width="132" height="32" rx="5"/><text class="ed-blk-t" x="70" y="94" text-anchor="middle">reference model</text><path class="ed-arr" d="M136,90 L149,90" marker-end="url(#ed-flow-head)"/><text class="ed-lab" x="206" y="74" text-anchor="middle">expected</text><rect class="ed-cell" x="150" y="80" width="14" height="20"/><text class="ed-pk" x="157" y="95" text-anchor="middle">A</text><rect class="ed-cell" x="164" y="80" width="14" height="20"/><text class="ed-pk" x="171" y="95" text-anchor="middle">B</text><rect class="ed-cell" x="178" y="80" width="14" height="20"/><text class="ed-pk" x="185" y="95" text-anchor="middle">C</text><rect class="ed-cell" x="192" y="80" width="14" height="20"/><text class="ed-pk" x="199" y="95" text-anchor="middle">D</text><rect class="ed-cell" x="206" y="80" width="14" height="20"/><text class="ed-pk" x="213" y="95" text-anchor="middle">E</text><rect class="ed-cell" x="220" y="80" width="14" height="20"/><text class="ed-pk" x="227" y="95" text-anchor="middle">F</text><rect class="ed-cell" x="234" y="80" width="14" height="20"/><text class="ed-pk" x="241" y="95" text-anchor="middle">G</text><rect class="ed-cell" x="248" y="80" width="14" height="20"/><text class="ed-pk" x="255" y="95" text-anchor="middle">H</text><path class="ed-arr" d="M262,30 L273,30" marker-end="url(#ed-flow-head)"/><path class="ed-arr" d="M262,90 L273,90" marker-end="url(#ed-flow-head)"/><rect class="ed-blk" x="274" y="14" width="72" height="92" rx="5"/><text class="ed-blk-t" x="310" y="50" text-anchor="middle">diff at</text><text class="ed-blk-t" x="310" y="64" text-anchor="middle">the end</text><text class="ed-blk-t" x="310" y="78" text-anchor="middle">of the test</text><path class="ed-arr" d="M310,106 L310,125" marker-end="url(#ed-flow-head)"/><text class="ed-blk-t" x="310" y="141" text-anchor="middle">report</text></svg>

<!-- /gen -->

השאלה בארבעה סעיפים :

1. **המרחק :** פונקציה שמחשבת אותו, והמרחק בדוגמה.
2. **הדוח :** רשימת ההבדלים עצמם, ומה עושים כששני הסברים נותנים אותו מרחק.
3. **לכל היותר d הבדלים :** זרמים של מיליון חבילות שיש ביניהם מעט הבדלים.
4. **חבילות שהתחלפו :** שתי חבילות צמודות שהגיעו בסדר הפוך כפעולה אחת.

??? interviewer "מה המראיין בודק"
    - **למה לא מקום מול מקום :** חבילה אחת שחסרה מזיזה את כל מה שאחריה. האם המועמד רואה
      שצריך ליישר את שני הזרמים, ולא להשוות אותם.
    - **תכנות דינמי :** האם הוא מגיע לטבלה של קידומות ולשלושת המקרים של החבילה האחרונה,
      ויודע להוכיח שאין מקרה רביעי.
    - **מהמספר לדוח :** הליכה אחורה בטבלה, ומה המחיר שלה בזיכרון. והאם הוא שם לב ששני מסלולים
      באותו אורך מספרים סיפורים שונים.
    - **קנה מידה :** טבלה של \( 10^{12} \) תאים לא נכנסת לשום סימולציה. האם הוא מנצל את זה
      שההבדלים מעטים.
    - **הכללה :** הוספה של פעולה חדשה, החלפה של שכנות, ומה היא שוברת בהוכחה.

---

### סעיף א – המרחק

כתבו פונקציה שמחזירה את המרחק בין הזרם הצפוי `a`, באורך \( m \), לזרם בפועל `b`, באורך
\( n \), וחשבו אותו לדוגמה.

??? tip "רמז 1"
    מה יכול היה לקרות לחבילה האחרונה של הזרם הצפוי?

??? tip "רמז 2"
    נסמן ב-\( d[i][j] \) את המרחק בין \( i \) החבילות הראשונות של `a` ל-\( j \) החבילות
    הראשונות של `b`. מהו \( d[i][0] \)? ומהו \( d[0][j] \)?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **‏3 :** ‏C חסרה, F שובשה ל-Y, ו-H מיותרת. מחשבים טבלה של קידומות : ‏\( d[i][0] = i \)
        ו-\( d[0][j] = j \), ובכל תא המינימום של שלוש אפשרויות : התא שמעליו ועוד 1, התא שמשמאלו
        ועוד 1, והתא באלכסון ועוד 0 או 1, לפי אם \( a_i = b_j \). המרחק הוא התא בפינה,
        \( d[m][n] \).

    <!-- cost: זמן \( O(m \cdot n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    במקום להשוות חבילה מול חבילה, בונים טבלה : שורה לכל קידומת של הזרם הצפוי, ועמודה לכל
    קידומת של הזרם בפועל. בכל תא נמצא המרחק בין שתי הקידומות. צעד למטה הוא חבילה חסרה, צעד
    ימינה הוא חבילה מיותרת, וצעד באלכסון הוא אותה חבילה (0) או חבילה ששובשה (1). המרחק הוא
    המסלול הזול ביותר מהפינה העליונה לפינה התחתונה :

    <!-- gen 0 -->

    <svg class="figure ed-fig" viewBox="0 0 324 294" style="max-width:20.25rem" role="img" aria-label="טבלת המרחקים של ABCDEFGH מול ABDEYGHH : הזרם הצפוי בשורות, הזרם בפועל בעמודות, ובפינה 3. המסלול מהפינה : C חסרה, F שובשה ל-Y, ו-H מיותרת"><text class="ed-idx" x="69" y="18" text-anchor="middle">0</text><text class="ed-idx" x="95" y="18" text-anchor="middle">1</text><text class="ed-pk" x="95" y="46" text-anchor="middle">A</text><text class="ed-idx" x="121" y="18" text-anchor="middle">2</text><text class="ed-pk" x="121" y="46" text-anchor="middle">B</text><text class="ed-idx" x="147" y="18" text-anchor="middle">3</text><text class="ed-pk" x="147" y="46" text-anchor="middle">D</text><text class="ed-idx" x="173" y="18" text-anchor="middle">4</text><text class="ed-pk" x="173" y="46" text-anchor="middle">E</text><text class="ed-idx" x="199" y="18" text-anchor="middle">5</text><text class="ed-pk" x="199" y="46" text-anchor="middle">Y</text><text class="ed-idx" x="225" y="18" text-anchor="middle">6</text><text class="ed-pk" x="225" y="46" text-anchor="middle">G</text><text class="ed-idx" x="251" y="18" text-anchor="middle">7</text><text class="ed-pk" x="251" y="46" text-anchor="middle">H</text><text class="ed-idx" x="277" y="18" text-anchor="middle">8</text><text class="ed-pk" x="277" y="46" text-anchor="middle">H</text><text class="ed-idx" x="13" y="73" text-anchor="middle">0</text><text class="ed-idx" x="13" y="99" text-anchor="middle">1</text><text class="ed-pk" x="41" y="99" text-anchor="middle">A</text><text class="ed-idx" x="13" y="125" text-anchor="middle">2</text><text class="ed-pk" x="41" y="125" text-anchor="middle">B</text><text class="ed-idx" x="13" y="151" text-anchor="middle">3</text><text class="ed-pk" x="41" y="151" text-anchor="middle">C</text><text class="ed-idx" x="13" y="177" text-anchor="middle">4</text><text class="ed-pk" x="41" y="177" text-anchor="middle">D</text><text class="ed-idx" x="13" y="203" text-anchor="middle">5</text><text class="ed-pk" x="41" y="203" text-anchor="middle">E</text><text class="ed-idx" x="13" y="229" text-anchor="middle">6</text><text class="ed-pk" x="41" y="229" text-anchor="middle">F</text><text class="ed-idx" x="13" y="255" text-anchor="middle">7</text><text class="ed-pk" x="41" y="255" text-anchor="middle">G</text><text class="ed-idx" x="13" y="281" text-anchor="middle">8</text><text class="ed-pk" x="41" y="281" text-anchor="middle">H</text><rect class="ed-cell ed-same" x="56" y="56" width="26" height="26"/><text class="ed-v" x="69" y="73" text-anchor="middle">0</text><rect class="ed-cell" x="82" y="56" width="26" height="26"/><text class="ed-v" x="95" y="73" text-anchor="middle">1</text><rect class="ed-cell" x="108" y="56" width="26" height="26"/><text class="ed-v" x="121" y="73" text-anchor="middle">2</text><rect class="ed-cell" x="134" y="56" width="26" height="26"/><text class="ed-v" x="147" y="73" text-anchor="middle">3</text><rect class="ed-cell" x="160" y="56" width="26" height="26"/><text class="ed-v" x="173" y="73" text-anchor="middle">4</text><rect class="ed-cell" x="186" y="56" width="26" height="26"/><text class="ed-v" x="199" y="73" text-anchor="middle">5</text><rect class="ed-cell" x="212" y="56" width="26" height="26"/><text class="ed-v" x="225" y="73" text-anchor="middle">6</text><rect class="ed-cell" x="238" y="56" width="26" height="26"/><text class="ed-v" x="251" y="73" text-anchor="middle">7</text><rect class="ed-cell" x="264" y="56" width="26" height="26"/><text class="ed-v" x="277" y="73" text-anchor="middle">8</text><rect class="ed-cell" x="56" y="82" width="26" height="26"/><text class="ed-v" x="69" y="99" text-anchor="middle">1</text><rect class="ed-cell ed-same" x="82" y="82" width="26" height="26"/><text class="ed-v" x="95" y="99" text-anchor="middle">0</text><rect class="ed-cell" x="108" y="82" width="26" height="26"/><text class="ed-v" x="121" y="99" text-anchor="middle">1</text><rect class="ed-cell" x="134" y="82" width="26" height="26"/><text class="ed-v" x="147" y="99" text-anchor="middle">2</text><rect class="ed-cell" x="160" y="82" width="26" height="26"/><text class="ed-v" x="173" y="99" text-anchor="middle">3</text><rect class="ed-cell" x="186" y="82" width="26" height="26"/><text class="ed-v" x="199" y="99" text-anchor="middle">4</text><rect class="ed-cell" x="212" y="82" width="26" height="26"/><text class="ed-v" x="225" y="99" text-anchor="middle">5</text><rect class="ed-cell" x="238" y="82" width="26" height="26"/><text class="ed-v" x="251" y="99" text-anchor="middle">6</text><rect class="ed-cell" x="264" y="82" width="26" height="26"/><text class="ed-v" x="277" y="99" text-anchor="middle">7</text><rect class="ed-cell" x="56" y="108" width="26" height="26"/><text class="ed-v" x="69" y="125" text-anchor="middle">2</text><rect class="ed-cell" x="82" y="108" width="26" height="26"/><text class="ed-v" x="95" y="125" text-anchor="middle">1</text><rect class="ed-cell ed-same" x="108" y="108" width="26" height="26"/><text class="ed-v" x="121" y="125" text-anchor="middle">0</text><rect class="ed-cell" x="134" y="108" width="26" height="26"/><text class="ed-v" x="147" y="125" text-anchor="middle">1</text><rect class="ed-cell" x="160" y="108" width="26" height="26"/><text class="ed-v" x="173" y="125" text-anchor="middle">2</text><rect class="ed-cell" x="186" y="108" width="26" height="26"/><text class="ed-v" x="199" y="125" text-anchor="middle">3</text><rect class="ed-cell" x="212" y="108" width="26" height="26"/><text class="ed-v" x="225" y="125" text-anchor="middle">4</text><rect class="ed-cell" x="238" y="108" width="26" height="26"/><text class="ed-v" x="251" y="125" text-anchor="middle">5</text><rect class="ed-cell" x="264" y="108" width="26" height="26"/><text class="ed-v" x="277" y="125" text-anchor="middle">6</text><rect class="ed-cell" x="56" y="134" width="26" height="26"/><text class="ed-v" x="69" y="151" text-anchor="middle">3</text><rect class="ed-cell" x="82" y="134" width="26" height="26"/><text class="ed-v" x="95" y="151" text-anchor="middle">2</text><rect class="ed-cell ed-miss" x="108" y="134" width="26" height="26"/><text class="ed-v" x="121" y="151" text-anchor="middle">1</text><rect class="ed-cell" x="134" y="134" width="26" height="26"/><text class="ed-v" x="147" y="151" text-anchor="middle">1</text><rect class="ed-cell" x="160" y="134" width="26" height="26"/><text class="ed-v" x="173" y="151" text-anchor="middle">2</text><rect class="ed-cell" x="186" y="134" width="26" height="26"/><text class="ed-v" x="199" y="151" text-anchor="middle">3</text><rect class="ed-cell" x="212" y="134" width="26" height="26"/><text class="ed-v" x="225" y="151" text-anchor="middle">4</text><rect class="ed-cell" x="238" y="134" width="26" height="26"/><text class="ed-v" x="251" y="151" text-anchor="middle">5</text><rect class="ed-cell" x="264" y="134" width="26" height="26"/><text class="ed-v" x="277" y="151" text-anchor="middle">6</text><rect class="ed-cell" x="56" y="160" width="26" height="26"/><text class="ed-v" x="69" y="177" text-anchor="middle">4</text><rect class="ed-cell" x="82" y="160" width="26" height="26"/><text class="ed-v" x="95" y="177" text-anchor="middle">3</text><rect class="ed-cell" x="108" y="160" width="26" height="26"/><text class="ed-v" x="121" y="177" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="134" y="160" width="26" height="26"/><text class="ed-v" x="147" y="177" text-anchor="middle">1</text><rect class="ed-cell" x="160" y="160" width="26" height="26"/><text class="ed-v" x="173" y="177" text-anchor="middle">2</text><rect class="ed-cell" x="186" y="160" width="26" height="26"/><text class="ed-v" x="199" y="177" text-anchor="middle">3</text><rect class="ed-cell" x="212" y="160" width="26" height="26"/><text class="ed-v" x="225" y="177" text-anchor="middle">4</text><rect class="ed-cell" x="238" y="160" width="26" height="26"/><text class="ed-v" x="251" y="177" text-anchor="middle">5</text><rect class="ed-cell" x="264" y="160" width="26" height="26"/><text class="ed-v" x="277" y="177" text-anchor="middle">6</text><rect class="ed-cell" x="56" y="186" width="26" height="26"/><text class="ed-v" x="69" y="203" text-anchor="middle">5</text><rect class="ed-cell" x="82" y="186" width="26" height="26"/><text class="ed-v" x="95" y="203" text-anchor="middle">4</text><rect class="ed-cell" x="108" y="186" width="26" height="26"/><text class="ed-v" x="121" y="203" text-anchor="middle">3</text><rect class="ed-cell" x="134" y="186" width="26" height="26"/><text class="ed-v" x="147" y="203" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="160" y="186" width="26" height="26"/><text class="ed-v" x="173" y="203" text-anchor="middle">1</text><rect class="ed-cell" x="186" y="186" width="26" height="26"/><text class="ed-v" x="199" y="203" text-anchor="middle">2</text><rect class="ed-cell" x="212" y="186" width="26" height="26"/><text class="ed-v" x="225" y="203" text-anchor="middle">3</text><rect class="ed-cell" x="238" y="186" width="26" height="26"/><text class="ed-v" x="251" y="203" text-anchor="middle">4</text><rect class="ed-cell" x="264" y="186" width="26" height="26"/><text class="ed-v" x="277" y="203" text-anchor="middle">5</text><rect class="ed-cell" x="56" y="212" width="26" height="26"/><text class="ed-v" x="69" y="229" text-anchor="middle">6</text><rect class="ed-cell" x="82" y="212" width="26" height="26"/><text class="ed-v" x="95" y="229" text-anchor="middle">5</text><rect class="ed-cell" x="108" y="212" width="26" height="26"/><text class="ed-v" x="121" y="229" text-anchor="middle">4</text><rect class="ed-cell" x="134" y="212" width="26" height="26"/><text class="ed-v" x="147" y="229" text-anchor="middle">3</text><rect class="ed-cell" x="160" y="212" width="26" height="26"/><text class="ed-v" x="173" y="229" text-anchor="middle">2</text><rect class="ed-cell ed-chg" x="186" y="212" width="26" height="26"/><text class="ed-v" x="199" y="229" text-anchor="middle">2</text><rect class="ed-cell" x="212" y="212" width="26" height="26"/><text class="ed-v" x="225" y="229" text-anchor="middle">3</text><rect class="ed-cell" x="238" y="212" width="26" height="26"/><text class="ed-v" x="251" y="229" text-anchor="middle">4</text><rect class="ed-cell" x="264" y="212" width="26" height="26"/><text class="ed-v" x="277" y="229" text-anchor="middle">5</text><rect class="ed-cell" x="56" y="238" width="26" height="26"/><text class="ed-v" x="69" y="255" text-anchor="middle">7</text><rect class="ed-cell" x="82" y="238" width="26" height="26"/><text class="ed-v" x="95" y="255" text-anchor="middle">6</text><rect class="ed-cell" x="108" y="238" width="26" height="26"/><text class="ed-v" x="121" y="255" text-anchor="middle">5</text><rect class="ed-cell" x="134" y="238" width="26" height="26"/><text class="ed-v" x="147" y="255" text-anchor="middle">4</text><rect class="ed-cell" x="160" y="238" width="26" height="26"/><text class="ed-v" x="173" y="255" text-anchor="middle">3</text><rect class="ed-cell" x="186" y="238" width="26" height="26"/><text class="ed-v" x="199" y="255" text-anchor="middle">3</text><rect class="ed-cell ed-same" x="212" y="238" width="26" height="26"/><text class="ed-v" x="225" y="255" text-anchor="middle">2</text><rect class="ed-cell ed-extra" x="238" y="238" width="26" height="26"/><text class="ed-v" x="251" y="255" text-anchor="middle">3</text><rect class="ed-cell" x="264" y="238" width="26" height="26"/><text class="ed-v" x="277" y="255" text-anchor="middle">4</text><rect class="ed-cell" x="56" y="264" width="26" height="26"/><text class="ed-v" x="69" y="281" text-anchor="middle">8</text><rect class="ed-cell" x="82" y="264" width="26" height="26"/><text class="ed-v" x="95" y="281" text-anchor="middle">7</text><rect class="ed-cell" x="108" y="264" width="26" height="26"/><text class="ed-v" x="121" y="281" text-anchor="middle">6</text><rect class="ed-cell" x="134" y="264" width="26" height="26"/><text class="ed-v" x="147" y="281" text-anchor="middle">5</text><rect class="ed-cell" x="160" y="264" width="26" height="26"/><text class="ed-v" x="173" y="281" text-anchor="middle">4</text><rect class="ed-cell" x="186" y="264" width="26" height="26"/><text class="ed-v" x="199" y="281" text-anchor="middle">4</text><rect class="ed-cell" x="212" y="264" width="26" height="26"/><text class="ed-v" x="225" y="281" text-anchor="middle">3</text><rect class="ed-cell" x="238" y="264" width="26" height="26"/><text class="ed-v" x="251" y="281" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="264" y="264" width="26" height="26"/><text class="ed-v" x="277" y="281" text-anchor="middle">3</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="ed-key-same"></i>אותה חבילה</span><span><i class="ed-key-miss"></i>חסרה, צעד למטה</span><span><i class="ed-key-extra"></i>מיותרת, צעד ימינה</span><span><i class="ed-key-chg"></i>שובשה, צעד באלכסון</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **השורה והעמודה של 0 :** ‏\( d[0][j] = j \), כי כל \( j \) החבילות מיותרות.
       ‏\( d[i][0] = i \), כי כל \( i \) החבילות חסרות.
    2. **כל תא :** המינימום של שלוש אפשרויות. ‏\( a_i \) חסרה, ‏\( b_j \) מיותרת, או שהן
       מתאימות זו לזו : ‏0 אם הן אותה חבילה ו-1 אם \( a_i \) שובשה ל-\( b_j \).
    3. **התשובה :** ‏\( d[m][n] \). בדוגמה 3.
    4. **זיכרון :** כל שורה תלויה רק בשורה שמעליה, ולכן מספיקות שתי שורות.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="edit_distance" linenums="1" hl_lines="9 10 11"
        def edit_distance(a, b):
            """The fewest edits from the expected stream a to the actual stream b: a packet
            missing, a packet extra, or a packet changed. Every packet is one character."""
            prev = list(range(len(b) + 1))                       # (1)!
            for i in range(1, len(a) + 1):
                cur = [i] + [0] * len(b)
                for j in range(1, len(b) + 1):
                    cur[j] = min(
                        prev[j] + 1,                             # a[i - 1] is missing
                        cur[j - 1] + 1,                          # b[j - 1] is extra
                        prev[j - 1] + (a[i - 1] != b[j - 1]))    # (2)!
                prev = cur
            return prev[-1]
        ```

        1. השורה של 0 : ‏\( d[0][j] = j \), ו-`cur[0] = i` הוא \( d[i][0] \).
        2. אותה חבילה עולה 0, וחבילה ששובשה עולה 1.

    === "SystemVerilog"
        ```systemverilog title="function automatic int edit_distance" linenums="1" hl_lines="11 12 13"
        // The fewest edits from the expected stream a to the actual stream b: a packet missing,
        // a packet extra, or a packet changed. Every packet is one character.
        function automatic int edit_distance(string a, string b);
          int prev[], cur[];
          prev = new[b.len() + 1];
          cur = new[b.len() + 1];
          foreach (prev[j]) prev[j] = j;
          for (int i = 1; i <= a.len(); i++) begin
            cur[0] = i;
            for (int j = 1; j <= b.len(); j++) begin
              cur[j] = prev[j - 1] + int'(a[i - 1] != b[j - 1]);
              if (prev[j] + 1 < cur[j]) cur[j] = prev[j] + 1;
              if (cur[j - 1] + 1 < cur[j]) cur[j] = cur[j - 1] + 1;
            end
            prev = cur;
          end
          return prev[b.len()];
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **יישור.** רצף של פעולות שהופך את \( a_1 \ldots a_i \) ל-\( b_1 \ldots b_j \) אפשר לכתוב
    כיישור : שתי שורות, הצפוי מעל בפועל, כשבכל עמודה זוג חבילות או חבילה מול חור. העלות היא
    מספר העמודות שאינן אותה חבילה מול אותה חבילה.

    **שלושה מקרים.** בעמודה האחרונה של יישור יש \( a_i \) מול חור (חסרה), חור מול \( b_j \)
    (מיותרת), או \( a_i \) מול \( b_j \). אין מקרה אחר, כי העמודה האחרונה מכילה את החבילה
    האחרונה של לפחות אחד הזרמים. אם מורידים אותה, נשאר יישור של קידומות קצרות יותר, בעלות
    שקטנה ב-1, ב-1, או ב-\( [a_i \ne b_j] \). לכן \( d[i][j] \) הוא לפחות המינימום של שלוש
    האפשרויות. ולהפך : לכל אחת מהן יש יישור בעלות הזו, ולכן \( d[i][j] \) הוא בדיוק המינימום.
    באינדוקציה על \( i + j \) כל הטבלה נכונה.

    **הדוגמה.** בפינה של הטבלה 3, ואי אפשר פחות. ב-`a` יש C ו-F שאין ב-`b`, וב-`b` יש Y
    ו-H שנייה שאין ב-`a`. כל פעולה מוציאה לכל היותר חבילה אחת ומכניסה לכל היותר חבילה אחת,
    ולכן צריך לפחות שתי פעולות. שתיים מספיקות רק אם שתיהן שיבושים במקום, של C ושל F, אבל
    שתי האפשרויות נותנות `ABYDEHGH` ו-`ABHDEYGH`, ולא `ABDEYGHH`.

    **נסו בעצמכם.** לפני כל "התא הבא" נחשו מאיזה שכן יגיע המינימום, והתיבה תראה. הכפתורים
    של המלכודות טוענים את המקרים שבסוף העמוד : לחצו על "השורה של 0" ‏(`AB` מול `XAB`), ונחשו
    מה היה בפינה אילו השורה של 0 הייתה אפסים :

    <div class="explorer" data-kind="editdist" data-a="ABCDEFGH" data-b="ABDEYGHH"></div>

    #### סיבוכיות { .sol-cost }

    ‏\( m \cdot n \) תאים, כל אחד בזמן קבוע : זמן \( O(m \cdot n) \), וזיכרון של שתי שורות,
    ‏\( O(n) \). לשני זרמים של מיליון חבילות זה \( 10^{12} \) תאים, ולכן סעיף ג.

---

### סעיף ב – הדוח, מה חסר, מה מיותר ומה שובש

המספר 3 לא מספיק למהנדס האימות. כתבו פונקציה שמחזירה את רשימת ההבדלים לפי הסדר. ומה עושים
כששני הסברים שונים נותנים אותו מרחק? בדקו עם `ABCDEF` מול `ABDXEF`.

??? tip "רמז 1"
    מאיזה שכן הגיע המינימום של התא שבפינה?

??? tip "רמז 2"
    בתא שבו שתי אפשרויות נותנות אותו מינימום, שתיהן נכונות. מה כל אחת מהן מספרת?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **הולכים אחורה מהפינה.** בכל תא עוברים לשכן שממנו הגיע המינימום : למעלה היא חבילה
        חסרה, שמאלה מיותרת, ובאלכסון אותה חבילה או חבילה ששובשה. כל שורה בדוח נושאת גם את
        המקום שלה. בדוגמה של סעיף א הדוח הוא C חסרה (מקום 3 בצפוי), F שובשה ל-Y (מקום 6 בצפוי
        ו-5 בפועל) ו-H מיותרת, זו שבמקום 7 בפועל. כשיש שוויון, הכלל קובע את הסיפור : ב-`ABCDEF`
        מול `ABDXEF` המרחק 2 הוא גם "C חסרה ו-X מיותרת" וגם "C שובשה ל-D ו-D שובשה ל-X". שני
        שיבושים שנותנים בדיוק את החבילות הבאות בזרם הם צירוף מקרים, ולכן ה-scoreboard מעדיף
        חבילה חסרה ומיותרת.

    <!-- cost: זמן \( O(m \cdot n) \) | זיכרון \( O(m \cdot n) \) -->

    #### הרעיון { .sol-idea }

    הערך של כל תא הגיע מאחד משלושת השכנים שלו. אם זוכרים את כל הטבלה, אפשר ללכת אחורה
    מהפינה ולקרוא את המסלול. כל צעד במסלול שאינו אותה חבילה הוא שורה בדוח, והתא \( (i, j) \)
    שבו הצעד נגמר הוא המקום שלה : ‏\( i \) חבילות של הזרם הצפוי ו-\( j \) של הזרם בפועל. ב-`ABDEYGHH`
    יש שתי H, והמקום אומר איזו מהן מיותרת : זו שבמקום 7. ב-scoreboard המקום הוא המספר של
    הטרנזקציה, ואיתו מוצאים אותה בלוג וב-waveform.

    בתא שבו שני שכנים נותנים את המינימום, שני המסלולים זולים באותה מידה, וצריך כלל. שני
    שיבושים שכל אחד מהם נותן בדיוק את החבילה הבאה בזרם הם צירוף מקרים. חבילה אחת שחסרה,
    ואחריה חבילה אחת מיותרת, מסבירות אותו דבר בלי צירוף מקרים. לכן כשיש שוויון,
    ה-scoreboard מעדיף חסרה ומיותרת על פני שיבוש :

    <!-- gen 2 -->

    | הכלל בשוויון | הדוח | המרחק |
    |---|---|:-:|
    | קודם חסרה ומיותרת | חסרה C, מיותרת X | 2 |
    | קודם שיבוש | שובשה C ל-D, שובשה D ל-X | 2 |

    <!-- /gen -->

    שני המסלולים בטבלה, באותו מחיר :

    <!-- gen 3 -->

    <svg class="figure ed-fig" viewBox="0 0 272 242" style="max-width:17rem" role="img" aria-label="טבלת המרחקים של ABCDEF מול ABDXEF, ובפינה 2. שני מסלולים באותו אורך : C חסרה ו-X מיותרת, או C שובשה ל-D ו-D שובשה ל-X"><text class="ed-idx" x="69" y="18" text-anchor="middle">0</text><text class="ed-idx" x="95" y="18" text-anchor="middle">1</text><text class="ed-pk" x="95" y="46" text-anchor="middle">A</text><text class="ed-idx" x="121" y="18" text-anchor="middle">2</text><text class="ed-pk" x="121" y="46" text-anchor="middle">B</text><text class="ed-idx" x="147" y="18" text-anchor="middle">3</text><text class="ed-pk" x="147" y="46" text-anchor="middle">D</text><text class="ed-idx" x="173" y="18" text-anchor="middle">4</text><text class="ed-pk" x="173" y="46" text-anchor="middle">X</text><text class="ed-idx" x="199" y="18" text-anchor="middle">5</text><text class="ed-pk" x="199" y="46" text-anchor="middle">E</text><text class="ed-idx" x="225" y="18" text-anchor="middle">6</text><text class="ed-pk" x="225" y="46" text-anchor="middle">F</text><text class="ed-idx" x="13" y="73" text-anchor="middle">0</text><text class="ed-idx" x="13" y="99" text-anchor="middle">1</text><text class="ed-pk" x="41" y="99" text-anchor="middle">A</text><text class="ed-idx" x="13" y="125" text-anchor="middle">2</text><text class="ed-pk" x="41" y="125" text-anchor="middle">B</text><text class="ed-idx" x="13" y="151" text-anchor="middle">3</text><text class="ed-pk" x="41" y="151" text-anchor="middle">C</text><text class="ed-idx" x="13" y="177" text-anchor="middle">4</text><text class="ed-pk" x="41" y="177" text-anchor="middle">D</text><text class="ed-idx" x="13" y="203" text-anchor="middle">5</text><text class="ed-pk" x="41" y="203" text-anchor="middle">E</text><text class="ed-idx" x="13" y="229" text-anchor="middle">6</text><text class="ed-pk" x="41" y="229" text-anchor="middle">F</text><rect class="ed-cell ed-same" x="56" y="56" width="26" height="26"/><text class="ed-v" x="69" y="73" text-anchor="middle">0</text><rect class="ed-cell" x="82" y="56" width="26" height="26"/><text class="ed-v" x="95" y="73" text-anchor="middle">1</text><rect class="ed-cell" x="108" y="56" width="26" height="26"/><text class="ed-v" x="121" y="73" text-anchor="middle">2</text><rect class="ed-cell" x="134" y="56" width="26" height="26"/><text class="ed-v" x="147" y="73" text-anchor="middle">3</text><rect class="ed-cell" x="160" y="56" width="26" height="26"/><text class="ed-v" x="173" y="73" text-anchor="middle">4</text><rect class="ed-cell" x="186" y="56" width="26" height="26"/><text class="ed-v" x="199" y="73" text-anchor="middle">5</text><rect class="ed-cell" x="212" y="56" width="26" height="26"/><text class="ed-v" x="225" y="73" text-anchor="middle">6</text><rect class="ed-cell" x="56" y="82" width="26" height="26"/><text class="ed-v" x="69" y="99" text-anchor="middle">1</text><rect class="ed-cell ed-same" x="82" y="82" width="26" height="26"/><text class="ed-v" x="95" y="99" text-anchor="middle">0</text><rect class="ed-cell" x="108" y="82" width="26" height="26"/><text class="ed-v" x="121" y="99" text-anchor="middle">1</text><rect class="ed-cell" x="134" y="82" width="26" height="26"/><text class="ed-v" x="147" y="99" text-anchor="middle">2</text><rect class="ed-cell" x="160" y="82" width="26" height="26"/><text class="ed-v" x="173" y="99" text-anchor="middle">3</text><rect class="ed-cell" x="186" y="82" width="26" height="26"/><text class="ed-v" x="199" y="99" text-anchor="middle">4</text><rect class="ed-cell" x="212" y="82" width="26" height="26"/><text class="ed-v" x="225" y="99" text-anchor="middle">5</text><rect class="ed-cell" x="56" y="108" width="26" height="26"/><text class="ed-v" x="69" y="125" text-anchor="middle">2</text><rect class="ed-cell" x="82" y="108" width="26" height="26"/><text class="ed-v" x="95" y="125" text-anchor="middle">1</text><rect class="ed-cell ed-same" x="108" y="108" width="26" height="26"/><text class="ed-v" x="121" y="125" text-anchor="middle">0</text><rect class="ed-cell" x="134" y="108" width="26" height="26"/><text class="ed-v" x="147" y="125" text-anchor="middle">1</text><rect class="ed-cell" x="160" y="108" width="26" height="26"/><text class="ed-v" x="173" y="125" text-anchor="middle">2</text><rect class="ed-cell" x="186" y="108" width="26" height="26"/><text class="ed-v" x="199" y="125" text-anchor="middle">3</text><rect class="ed-cell" x="212" y="108" width="26" height="26"/><text class="ed-v" x="225" y="125" text-anchor="middle">4</text><rect class="ed-cell" x="56" y="134" width="26" height="26"/><text class="ed-v" x="69" y="151" text-anchor="middle">3</text><rect class="ed-cell" x="82" y="134" width="26" height="26"/><text class="ed-v" x="95" y="151" text-anchor="middle">2</text><rect class="ed-cell ed-miss" x="108" y="134" width="26" height="26"/><text class="ed-v" x="121" y="151" text-anchor="middle">1</text><rect class="ed-cell" x="134" y="134" width="26" height="26"/><text class="ed-v" x="147" y="151" text-anchor="middle">1</text><rect class="ed-cell" x="160" y="134" width="26" height="26"/><text class="ed-v" x="173" y="151" text-anchor="middle">2</text><rect class="ed-cell" x="186" y="134" width="26" height="26"/><text class="ed-v" x="199" y="151" text-anchor="middle">3</text><rect class="ed-cell" x="212" y="134" width="26" height="26"/><text class="ed-v" x="225" y="151" text-anchor="middle">4</text><rect class="ed-cell" x="56" y="160" width="26" height="26"/><text class="ed-v" x="69" y="177" text-anchor="middle">4</text><rect class="ed-cell" x="82" y="160" width="26" height="26"/><text class="ed-v" x="95" y="177" text-anchor="middle">3</text><rect class="ed-cell" x="108" y="160" width="26" height="26"/><text class="ed-v" x="121" y="177" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="134" y="160" width="26" height="26"/><text class="ed-v" x="147" y="177" text-anchor="middle">1</text><rect class="ed-cell ed-extra" x="160" y="160" width="26" height="26"/><text class="ed-v" x="173" y="177" text-anchor="middle">2</text><rect class="ed-cell" x="186" y="160" width="26" height="26"/><text class="ed-v" x="199" y="177" text-anchor="middle">3</text><rect class="ed-cell" x="212" y="160" width="26" height="26"/><text class="ed-v" x="225" y="177" text-anchor="middle">4</text><rect class="ed-cell" x="56" y="186" width="26" height="26"/><text class="ed-v" x="69" y="203" text-anchor="middle">5</text><rect class="ed-cell" x="82" y="186" width="26" height="26"/><text class="ed-v" x="95" y="203" text-anchor="middle">4</text><rect class="ed-cell" x="108" y="186" width="26" height="26"/><text class="ed-v" x="121" y="203" text-anchor="middle">3</text><rect class="ed-cell" x="134" y="186" width="26" height="26"/><text class="ed-v" x="147" y="203" text-anchor="middle">2</text><rect class="ed-cell" x="160" y="186" width="26" height="26"/><text class="ed-v" x="173" y="203" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="186" y="186" width="26" height="26"/><text class="ed-v" x="199" y="203" text-anchor="middle">2</text><rect class="ed-cell" x="212" y="186" width="26" height="26"/><text class="ed-v" x="225" y="203" text-anchor="middle">3</text><rect class="ed-cell" x="56" y="212" width="26" height="26"/><text class="ed-v" x="69" y="229" text-anchor="middle">6</text><rect class="ed-cell" x="82" y="212" width="26" height="26"/><text class="ed-v" x="95" y="229" text-anchor="middle">5</text><rect class="ed-cell" x="108" y="212" width="26" height="26"/><text class="ed-v" x="121" y="229" text-anchor="middle">4</text><rect class="ed-cell" x="134" y="212" width="26" height="26"/><text class="ed-v" x="147" y="229" text-anchor="middle">3</text><rect class="ed-cell" x="160" y="212" width="26" height="26"/><text class="ed-v" x="173" y="229" text-anchor="middle">3</text><rect class="ed-cell" x="186" y="212" width="26" height="26"/><text class="ed-v" x="199" y="229" text-anchor="middle">3</text><rect class="ed-cell ed-same" x="212" y="212" width="26" height="26"/><text class="ed-v" x="225" y="229" text-anchor="middle">2</text><polyline class="ed-other" points="69,69 95,95 121,121 147,147 173,173 199,199 225,225"/></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="ed-key-same"></i>אותה חבילה</span><span><i class="ed-key-miss"></i>חסרה, צעד למטה</span><span><i class="ed-key-extra"></i>מיותרת, צעד ימינה</span><span><i class="ed-key-chg"></i>שובשה, צעד באלכסון</span><span><i class="ed-key-other"></i>המסלול כשמעדיפים שיבוש</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הטבלה המלאה :** הפעם שומרים את כל הטבלה, ולא רק שתי שורות.
    2. **מהפינה :** מתחילים ב-\( (m, n) \).
    3. **אותה חבילה :** אם \( a_i = b_j \), עוברים באלכסון, בלי שורה בדוח.
    4. **אחרת :** עוברים לשכן הראשון, לפי סדר הכלל, שהערך שלו קטן ב-1, וכותבים בדוח מה
       הצעד אומר, ואת התא \( (i, j) \) שבו הוא נגמר.
    5. **הסוף :** ב-\( (0, 0) \). הופכים את הסדר של הדוח, כי הלכנו מהסוף להתחלה.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="diff" linenums="1" hl_lines="17 18 19 20"
        def diff(a, b, prefer="gaps"):
            """The report: every difference in stream order as (kind, expected, actual, i, j),
            i and j the packets of a and of b read up to the line. At a tie "gaps" says missing
            or extra before changed, "changed" the other way."""
            d = [[i + j if i == 0 or j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
            for i in range(1, len(a) + 1):
                for j in range(1, len(b) + 1):
                    d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
            moves = [("missing", 1, 0), ("extra", 0, 1), ("changed", 1, 1)]
            if prefer == "changed":
                moves = moves[2:] + moves[:2]
            i, j, out = len(a), len(b), []
            while i or j:
                if i and j and a[i - 1] == b[j - 1]:
                    i, j = i - 1, j - 1                          # (1)!
                    continue
                for kind, di, dj in moves:
                    if i >= di and j >= dj and d[i][j] == d[i - di][j - dj] + 1:
                        break                                    # (2)!
                out.append((kind, a[i - 1] if di else None, b[j - 1] if dj else None, i, j))  # (3)!
                i, j = i - di, j - dj
            return out[::-1]
        ```

        1. כשהחבילות שוות, האלכסון תמיד נותן את המינימום (ההוכחה למטה), ולכן אין צורך לבדוק.
        2. הערך של התא הוא המינימום של שלוש האפשרויות, ולכן לפחות אחת מהן מתאימה. הסדר של
           `moves` הוא הכלל לשוויון.
        3. המקום של השורה : חבילה חסרה היא `a[i - 1]`, אחרי \( j \) חבילות בפועל, וחבילה מיותרת
           היא `b[j - 1]`, אחרי \( i \) חבילות צפויות.

    === "SystemVerilog"
        ```systemverilog title="function automatic lines_t diff" linenums="1" hl_lines="27 28 29 30 31 32 33"
        typedef string lines_t[$];

        // The report: every difference in stream order, at its cell (i, j). prefer_changed: at
        // a tie a changed packet before a missing or an extra one.
        function automatic lines_t diff(string a, string b, bit prefer_changed);
          int d[][];
          int i = a.len(), j = b.len();
          bit chg, miss, ext;
          lines_t out;
          d = new[a.len() + 1];
          foreach (d[r]) begin
            d[r] = new[b.len() + 1];
            foreach (d[r][c]) d[r][c] = (r == 0 || c == 0) ? r + c : 0;
          end
          for (int r = 1; r <= a.len(); r++)
            for (int c = 1; c <= b.len(); c++) begin
              d[r][c] = d[r - 1][c - 1] + int'(a[r - 1] != b[c - 1]);
              if (d[r - 1][c] + 1 < d[r][c]) d[r][c] = d[r - 1][c] + 1;
              if (d[r][c - 1] + 1 < d[r][c]) d[r][c] = d[r][c - 1] + 1;
            end
          while (i > 0 || j > 0) begin
            chg  = i > 0 && j > 0 && d[i][j] == d[i - 1][j - 1] + 1;
            miss = i > 0 && d[i][j] == d[i - 1][j] + 1;
            ext  = j > 0 && d[i][j] == d[i][j - 1] + 1;
            if (i > 0 && j > 0 && a[i - 1] == b[j - 1]) begin
              i--; j--;
            end else if (chg && (prefer_changed || !(miss || ext))) begin
              out.push_front($sformatf("%c changed to %c at (%0d, %0d)", a[i - 1], b[j - 1], i, j));
              i--; j--;
            end else if (miss) begin
              out.push_front($sformatf("%c missing at (%0d, %0d)", a[i - 1], i, j)); i--;
            end else begin
              out.push_front($sformatf("%c extra at (%0d, %0d)", b[j - 1], i, j)); j--;
            end
          end
          return out;
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **שכנים קרובים.** שני תאים שכנים בטבלה שונים לכל היותר ב-1 : מ-\( (i-1, j) \) מגיעים
    ל-\( (i, j) \) בפעולה אחת, ולהפך, יישור של \( (i, j) \) בלי \( a_i \) הוא יישור
    של \( (i-1, j) \) שזול לכל היותר ב-1 יותר.

    **אותה חבילה.** אם \( a_i = b_j \), אז \( d[i-1][j] + 1 \ge d[i-1][j-1] \) ו-\( d[i][j-1] + 1
    \ge d[i-1][j-1] \), לפי השכנים הקרובים. לכן המינימום הוא \( d[i-1][j-1] \), והאלכסון תמיד
    נכון.

    **הדוח.** בכל צעד שאינו אותה חבילה הערך יורד ב-1 בדיוק, ובאותה חבילה הוא לא משתנה.
    לכן מספר השורות בדוח הוא \( d[m][n] \). והצעדים, לפי הסדר, בונים את `b` מ-`a` : זה היישור
    של סעיף א, עמודה אחרי עמודה.

    **השוויון.** בתא שבו שני שכנים נותנים את המינימום, כל אחד מהם מתחיל מסלול זול ביותר.
    המרחק לא תלוי בבחירה, אבל הדוח כן. בדוגמה, בתא \( (4, 4) \), ‏D מול X, גם השכן משמאל וגם
    השכן באלכסון שווים 1. משמאל ממשיכים ל-"X מיותרת" ול-"C חסרה", ובאלכסון ל-"D שובשה ל-X"
    ול-"C שובשה ל-D".

    **נסו בעצמכם.** החליפו את הכלל לשוויון, ומצאו בטבלה את התא שבו שני המסלולים נפרדים. מה
    המקום של כל שורה בדוח, בכל אחד מהכללים?

    <div class="explorer" data-kind="editdist" data-a="ABCDEF" data-b="ABDXEF"></div>

    #### סיבוכיות { .sol-cost }

    בניית הטבלה כמו בסעיף א, \( O(m \cdot n) \), וההליכה אחורה היא \( O(m + n) \) צעדים. הפעם
    צריך את כל הטבלה, \( O(m \cdot n) \) זיכרון, כי ההליכה אחורה קוראת שורות ישנות.

---

### סעיף ג – לכל היותר d הבדלים

זרם של מיליון חבילות לא נכנס לטבלה של \( 10^{12} \) תאים. אבל ב-scoreboard ההבדלים מעטים.
כתבו פונקציה שמחזירה את המרחק אם הוא לכל היותר \( d \), ואחרת אומרת שהוא גדול מ-\( d \),
בזמן \( O(m \cdot d) \).

??? tip "רמז 1"
    מה הערך הקטן ביותר שיכול להיות בתא \( (i, j) \)?

??? tip "רמז 2"
    אם המרחק לכל היותר \( d \), כמה רחוק מהאלכסון הראשי יכול המסלול להגיע?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        **רק \( 2d + 1 \) אלכסונים.** ‏\( d[i][j] \ge |i - j| \), ולכן מסלול שעולה לכל היותר
        \( d \) לא יוצא מהרצועה \( |i - j| \le d \). מחשבים רק את התאים שבה, ותא מחוץ לה
        נחשב לגדול מ-\( d \). אם \( |m - n| > d \) עונים מיד, ואם כל התאים של שורה כבר גדולים
        מ-\( d \) עוצרים.

    <!-- cost: זמן \( O(m \cdot d) \) | זיכרון \( O(d) \) -->

    #### הרעיון { .sol-idea }

    ההפרש בין האורכים של שתי קידומות הוא מספר חבילות שחייבות להיות חסרות או מיותרות, ולכן
    \( d[i][j] \ge |i - j| \). לאורך המסלול הזול ביותר הערכים לא יורדים, כי כל צעד בו מוסיף 0
    (אותה חבילה) או 1 (פעולה). לכן אם בפינה יש לכל היותר \( d \), כל תא במסלול שווה לכל היותר
    \( d \), ורחוק מהאלכסון לכל היותר \( d \). עם \( d = 2 \) מחשבים רק חמישה אלכסונים :

    <!-- gen 5 -->

    <svg class="figure ed-fig" viewBox="0 0 428 398" style="max-width:26.75rem" role="img" aria-label="טבלת המרחקים של ABCDEFGHIJKL מול ABCEFGHIXJKL עם d = 2 : רק חמשת האלכסונים שסביב האלכסון הראשי מחושבים, ובפינה 2"><text class="ed-idx" x="69" y="18" text-anchor="middle">0</text><text class="ed-idx" x="95" y="18" text-anchor="middle">1</text><text class="ed-pk" x="95" y="46" text-anchor="middle">A</text><text class="ed-idx" x="121" y="18" text-anchor="middle">2</text><text class="ed-pk" x="121" y="46" text-anchor="middle">B</text><text class="ed-idx" x="147" y="18" text-anchor="middle">3</text><text class="ed-pk" x="147" y="46" text-anchor="middle">C</text><text class="ed-idx" x="173" y="18" text-anchor="middle">4</text><text class="ed-pk" x="173" y="46" text-anchor="middle">E</text><text class="ed-idx" x="199" y="18" text-anchor="middle">5</text><text class="ed-pk" x="199" y="46" text-anchor="middle">F</text><text class="ed-idx" x="225" y="18" text-anchor="middle">6</text><text class="ed-pk" x="225" y="46" text-anchor="middle">G</text><text class="ed-idx" x="251" y="18" text-anchor="middle">7</text><text class="ed-pk" x="251" y="46" text-anchor="middle">H</text><text class="ed-idx" x="277" y="18" text-anchor="middle">8</text><text class="ed-pk" x="277" y="46" text-anchor="middle">I</text><text class="ed-idx" x="303" y="18" text-anchor="middle">9</text><text class="ed-pk" x="303" y="46" text-anchor="middle">X</text><text class="ed-idx" x="329" y="18" text-anchor="middle">10</text><text class="ed-pk" x="329" y="46" text-anchor="middle">J</text><text class="ed-idx" x="355" y="18" text-anchor="middle">11</text><text class="ed-pk" x="355" y="46" text-anchor="middle">K</text><text class="ed-idx" x="381" y="18" text-anchor="middle">12</text><text class="ed-pk" x="381" y="46" text-anchor="middle">L</text><text class="ed-idx" x="13" y="73" text-anchor="middle">0</text><text class="ed-idx" x="13" y="99" text-anchor="middle">1</text><text class="ed-pk" x="41" y="99" text-anchor="middle">A</text><text class="ed-idx" x="13" y="125" text-anchor="middle">2</text><text class="ed-pk" x="41" y="125" text-anchor="middle">B</text><text class="ed-idx" x="13" y="151" text-anchor="middle">3</text><text class="ed-pk" x="41" y="151" text-anchor="middle">C</text><text class="ed-idx" x="13" y="177" text-anchor="middle">4</text><text class="ed-pk" x="41" y="177" text-anchor="middle">D</text><text class="ed-idx" x="13" y="203" text-anchor="middle">5</text><text class="ed-pk" x="41" y="203" text-anchor="middle">E</text><text class="ed-idx" x="13" y="229" text-anchor="middle">6</text><text class="ed-pk" x="41" y="229" text-anchor="middle">F</text><text class="ed-idx" x="13" y="255" text-anchor="middle">7</text><text class="ed-pk" x="41" y="255" text-anchor="middle">G</text><text class="ed-idx" x="13" y="281" text-anchor="middle">8</text><text class="ed-pk" x="41" y="281" text-anchor="middle">H</text><text class="ed-idx" x="13" y="307" text-anchor="middle">9</text><text class="ed-pk" x="41" y="307" text-anchor="middle">I</text><text class="ed-idx" x="13" y="333" text-anchor="middle">10</text><text class="ed-pk" x="41" y="333" text-anchor="middle">J</text><text class="ed-idx" x="13" y="359" text-anchor="middle">11</text><text class="ed-pk" x="41" y="359" text-anchor="middle">K</text><text class="ed-idx" x="13" y="385" text-anchor="middle">12</text><text class="ed-pk" x="41" y="385" text-anchor="middle">L</text><rect class="ed-cell ed-same" x="56" y="56" width="26" height="26"/><text class="ed-v" x="69" y="73" text-anchor="middle">0</text><rect class="ed-cell" x="82" y="56" width="26" height="26"/><text class="ed-v" x="95" y="73" text-anchor="middle">1</text><rect class="ed-cell" x="108" y="56" width="26" height="26"/><text class="ed-v" x="121" y="73" text-anchor="middle">2</text><rect class="ed-cell ed-out" x="134" y="56" width="26" height="26"/><rect class="ed-cell ed-out" x="160" y="56" width="26" height="26"/><rect class="ed-cell ed-out" x="186" y="56" width="26" height="26"/><rect class="ed-cell ed-out" x="212" y="56" width="26" height="26"/><rect class="ed-cell ed-out" x="238" y="56" width="26" height="26"/><rect class="ed-cell ed-out" x="264" y="56" width="26" height="26"/><rect class="ed-cell ed-out" x="290" y="56" width="26" height="26"/><rect class="ed-cell ed-out" x="316" y="56" width="26" height="26"/><rect class="ed-cell ed-out" x="342" y="56" width="26" height="26"/><rect class="ed-cell ed-out" x="368" y="56" width="26" height="26"/><rect class="ed-cell" x="56" y="82" width="26" height="26"/><text class="ed-v" x="69" y="99" text-anchor="middle">1</text><rect class="ed-cell ed-same" x="82" y="82" width="26" height="26"/><text class="ed-v" x="95" y="99" text-anchor="middle">0</text><rect class="ed-cell" x="108" y="82" width="26" height="26"/><text class="ed-v" x="121" y="99" text-anchor="middle">1</text><rect class="ed-cell" x="134" y="82" width="26" height="26"/><text class="ed-v" x="147" y="99" text-anchor="middle">2</text><rect class="ed-cell ed-out" x="160" y="82" width="26" height="26"/><rect class="ed-cell ed-out" x="186" y="82" width="26" height="26"/><rect class="ed-cell ed-out" x="212" y="82" width="26" height="26"/><rect class="ed-cell ed-out" x="238" y="82" width="26" height="26"/><rect class="ed-cell ed-out" x="264" y="82" width="26" height="26"/><rect class="ed-cell ed-out" x="290" y="82" width="26" height="26"/><rect class="ed-cell ed-out" x="316" y="82" width="26" height="26"/><rect class="ed-cell ed-out" x="342" y="82" width="26" height="26"/><rect class="ed-cell ed-out" x="368" y="82" width="26" height="26"/><rect class="ed-cell" x="56" y="108" width="26" height="26"/><text class="ed-v" x="69" y="125" text-anchor="middle">2</text><rect class="ed-cell" x="82" y="108" width="26" height="26"/><text class="ed-v" x="95" y="125" text-anchor="middle">1</text><rect class="ed-cell ed-same" x="108" y="108" width="26" height="26"/><text class="ed-v" x="121" y="125" text-anchor="middle">0</text><rect class="ed-cell" x="134" y="108" width="26" height="26"/><text class="ed-v" x="147" y="125" text-anchor="middle">1</text><rect class="ed-cell" x="160" y="108" width="26" height="26"/><text class="ed-v" x="173" y="125" text-anchor="middle">2</text><rect class="ed-cell ed-out" x="186" y="108" width="26" height="26"/><rect class="ed-cell ed-out" x="212" y="108" width="26" height="26"/><rect class="ed-cell ed-out" x="238" y="108" width="26" height="26"/><rect class="ed-cell ed-out" x="264" y="108" width="26" height="26"/><rect class="ed-cell ed-out" x="290" y="108" width="26" height="26"/><rect class="ed-cell ed-out" x="316" y="108" width="26" height="26"/><rect class="ed-cell ed-out" x="342" y="108" width="26" height="26"/><rect class="ed-cell ed-out" x="368" y="108" width="26" height="26"/><rect class="ed-cell ed-out" x="56" y="134" width="26" height="26"/><rect class="ed-cell" x="82" y="134" width="26" height="26"/><text class="ed-v" x="95" y="151" text-anchor="middle">2</text><rect class="ed-cell" x="108" y="134" width="26" height="26"/><text class="ed-v" x="121" y="151" text-anchor="middle">1</text><rect class="ed-cell ed-same" x="134" y="134" width="26" height="26"/><text class="ed-v" x="147" y="151" text-anchor="middle">0</text><rect class="ed-cell" x="160" y="134" width="26" height="26"/><text class="ed-v" x="173" y="151" text-anchor="middle">1</text><rect class="ed-cell" x="186" y="134" width="26" height="26"/><text class="ed-v" x="199" y="151" text-anchor="middle">2</text><rect class="ed-cell ed-out" x="212" y="134" width="26" height="26"/><rect class="ed-cell ed-out" x="238" y="134" width="26" height="26"/><rect class="ed-cell ed-out" x="264" y="134" width="26" height="26"/><rect class="ed-cell ed-out" x="290" y="134" width="26" height="26"/><rect class="ed-cell ed-out" x="316" y="134" width="26" height="26"/><rect class="ed-cell ed-out" x="342" y="134" width="26" height="26"/><rect class="ed-cell ed-out" x="368" y="134" width="26" height="26"/><rect class="ed-cell ed-out" x="56" y="160" width="26" height="26"/><rect class="ed-cell ed-out" x="82" y="160" width="26" height="26"/><rect class="ed-cell" x="108" y="160" width="26" height="26"/><text class="ed-v" x="121" y="177" text-anchor="middle">2</text><rect class="ed-cell ed-miss" x="134" y="160" width="26" height="26"/><text class="ed-v" x="147" y="177" text-anchor="middle">1</text><rect class="ed-cell" x="160" y="160" width="26" height="26"/><text class="ed-v" x="173" y="177" text-anchor="middle">1</text><rect class="ed-cell" x="186" y="160" width="26" height="26"/><text class="ed-v" x="199" y="177" text-anchor="middle">2</text><rect class="ed-cell" x="212" y="160" width="26" height="26"/><text class="ed-v" x="225" y="177" text-anchor="middle">3</text><rect class="ed-cell ed-out" x="238" y="160" width="26" height="26"/><rect class="ed-cell ed-out" x="264" y="160" width="26" height="26"/><rect class="ed-cell ed-out" x="290" y="160" width="26" height="26"/><rect class="ed-cell ed-out" x="316" y="160" width="26" height="26"/><rect class="ed-cell ed-out" x="342" y="160" width="26" height="26"/><rect class="ed-cell ed-out" x="368" y="160" width="26" height="26"/><rect class="ed-cell ed-out" x="56" y="186" width="26" height="26"/><rect class="ed-cell ed-out" x="82" y="186" width="26" height="26"/><rect class="ed-cell ed-out" x="108" y="186" width="26" height="26"/><rect class="ed-cell" x="134" y="186" width="26" height="26"/><text class="ed-v" x="147" y="203" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="160" y="186" width="26" height="26"/><text class="ed-v" x="173" y="203" text-anchor="middle">1</text><rect class="ed-cell" x="186" y="186" width="26" height="26"/><text class="ed-v" x="199" y="203" text-anchor="middle">2</text><rect class="ed-cell" x="212" y="186" width="26" height="26"/><text class="ed-v" x="225" y="203" text-anchor="middle">3</text><rect class="ed-cell" x="238" y="186" width="26" height="26"/><text class="ed-v" x="251" y="203" text-anchor="middle">4</text><rect class="ed-cell ed-out" x="264" y="186" width="26" height="26"/><rect class="ed-cell ed-out" x="290" y="186" width="26" height="26"/><rect class="ed-cell ed-out" x="316" y="186" width="26" height="26"/><rect class="ed-cell ed-out" x="342" y="186" width="26" height="26"/><rect class="ed-cell ed-out" x="368" y="186" width="26" height="26"/><rect class="ed-cell ed-out" x="56" y="212" width="26" height="26"/><rect class="ed-cell ed-out" x="82" y="212" width="26" height="26"/><rect class="ed-cell ed-out" x="108" y="212" width="26" height="26"/><rect class="ed-cell ed-out" x="134" y="212" width="26" height="26"/><rect class="ed-cell" x="160" y="212" width="26" height="26"/><text class="ed-v" x="173" y="229" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="186" y="212" width="26" height="26"/><text class="ed-v" x="199" y="229" text-anchor="middle">1</text><rect class="ed-cell" x="212" y="212" width="26" height="26"/><text class="ed-v" x="225" y="229" text-anchor="middle">2</text><rect class="ed-cell" x="238" y="212" width="26" height="26"/><text class="ed-v" x="251" y="229" text-anchor="middle">3</text><rect class="ed-cell" x="264" y="212" width="26" height="26"/><text class="ed-v" x="277" y="229" text-anchor="middle">4</text><rect class="ed-cell ed-out" x="290" y="212" width="26" height="26"/><rect class="ed-cell ed-out" x="316" y="212" width="26" height="26"/><rect class="ed-cell ed-out" x="342" y="212" width="26" height="26"/><rect class="ed-cell ed-out" x="368" y="212" width="26" height="26"/><rect class="ed-cell ed-out" x="56" y="238" width="26" height="26"/><rect class="ed-cell ed-out" x="82" y="238" width="26" height="26"/><rect class="ed-cell ed-out" x="108" y="238" width="26" height="26"/><rect class="ed-cell ed-out" x="134" y="238" width="26" height="26"/><rect class="ed-cell ed-out" x="160" y="238" width="26" height="26"/><rect class="ed-cell" x="186" y="238" width="26" height="26"/><text class="ed-v" x="199" y="255" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="212" y="238" width="26" height="26"/><text class="ed-v" x="225" y="255" text-anchor="middle">1</text><rect class="ed-cell" x="238" y="238" width="26" height="26"/><text class="ed-v" x="251" y="255" text-anchor="middle">2</text><rect class="ed-cell" x="264" y="238" width="26" height="26"/><text class="ed-v" x="277" y="255" text-anchor="middle">3</text><rect class="ed-cell" x="290" y="238" width="26" height="26"/><text class="ed-v" x="303" y="255" text-anchor="middle">4</text><rect class="ed-cell ed-out" x="316" y="238" width="26" height="26"/><rect class="ed-cell ed-out" x="342" y="238" width="26" height="26"/><rect class="ed-cell ed-out" x="368" y="238" width="26" height="26"/><rect class="ed-cell ed-out" x="56" y="264" width="26" height="26"/><rect class="ed-cell ed-out" x="82" y="264" width="26" height="26"/><rect class="ed-cell ed-out" x="108" y="264" width="26" height="26"/><rect class="ed-cell ed-out" x="134" y="264" width="26" height="26"/><rect class="ed-cell ed-out" x="160" y="264" width="26" height="26"/><rect class="ed-cell ed-out" x="186" y="264" width="26" height="26"/><rect class="ed-cell" x="212" y="264" width="26" height="26"/><text class="ed-v" x="225" y="281" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="238" y="264" width="26" height="26"/><text class="ed-v" x="251" y="281" text-anchor="middle">1</text><rect class="ed-cell" x="264" y="264" width="26" height="26"/><text class="ed-v" x="277" y="281" text-anchor="middle">2</text><rect class="ed-cell" x="290" y="264" width="26" height="26"/><text class="ed-v" x="303" y="281" text-anchor="middle">3</text><rect class="ed-cell" x="316" y="264" width="26" height="26"/><text class="ed-v" x="329" y="281" text-anchor="middle">4</text><rect class="ed-cell ed-out" x="342" y="264" width="26" height="26"/><rect class="ed-cell ed-out" x="368" y="264" width="26" height="26"/><rect class="ed-cell ed-out" x="56" y="290" width="26" height="26"/><rect class="ed-cell ed-out" x="82" y="290" width="26" height="26"/><rect class="ed-cell ed-out" x="108" y="290" width="26" height="26"/><rect class="ed-cell ed-out" x="134" y="290" width="26" height="26"/><rect class="ed-cell ed-out" x="160" y="290" width="26" height="26"/><rect class="ed-cell ed-out" x="186" y="290" width="26" height="26"/><rect class="ed-cell ed-out" x="212" y="290" width="26" height="26"/><rect class="ed-cell" x="238" y="290" width="26" height="26"/><text class="ed-v" x="251" y="307" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="264" y="290" width="26" height="26"/><text class="ed-v" x="277" y="307" text-anchor="middle">1</text><rect class="ed-cell ed-extra" x="290" y="290" width="26" height="26"/><text class="ed-v" x="303" y="307" text-anchor="middle">2</text><rect class="ed-cell" x="316" y="290" width="26" height="26"/><text class="ed-v" x="329" y="307" text-anchor="middle">3</text><rect class="ed-cell" x="342" y="290" width="26" height="26"/><text class="ed-v" x="355" y="307" text-anchor="middle">4</text><rect class="ed-cell ed-out" x="368" y="290" width="26" height="26"/><rect class="ed-cell ed-out" x="56" y="316" width="26" height="26"/><rect class="ed-cell ed-out" x="82" y="316" width="26" height="26"/><rect class="ed-cell ed-out" x="108" y="316" width="26" height="26"/><rect class="ed-cell ed-out" x="134" y="316" width="26" height="26"/><rect class="ed-cell ed-out" x="160" y="316" width="26" height="26"/><rect class="ed-cell ed-out" x="186" y="316" width="26" height="26"/><rect class="ed-cell ed-out" x="212" y="316" width="26" height="26"/><rect class="ed-cell ed-out" x="238" y="316" width="26" height="26"/><rect class="ed-cell" x="264" y="316" width="26" height="26"/><text class="ed-v" x="277" y="333" text-anchor="middle">2</text><rect class="ed-cell" x="290" y="316" width="26" height="26"/><text class="ed-v" x="303" y="333" text-anchor="middle">2</text><rect class="ed-cell ed-same" x="316" y="316" width="26" height="26"/><text class="ed-v" x="329" y="333" text-anchor="middle">2</text><rect class="ed-cell" x="342" y="316" width="26" height="26"/><text class="ed-v" x="355" y="333" text-anchor="middle">3</text><rect class="ed-cell" x="368" y="316" width="26" height="26"/><text class="ed-v" x="381" y="333" text-anchor="middle">4</text><rect class="ed-cell ed-out" x="56" y="342" width="26" height="26"/><rect class="ed-cell ed-out" x="82" y="342" width="26" height="26"/><rect class="ed-cell ed-out" x="108" y="342" width="26" height="26"/><rect class="ed-cell ed-out" x="134" y="342" width="26" height="26"/><rect class="ed-cell ed-out" x="160" y="342" width="26" height="26"/><rect class="ed-cell ed-out" x="186" y="342" width="26" height="26"/><rect class="ed-cell ed-out" x="212" y="342" width="26" height="26"/><rect class="ed-cell ed-out" x="238" y="342" width="26" height="26"/><rect class="ed-cell ed-out" x="264" y="342" width="26" height="26"/><rect class="ed-cell" x="290" y="342" width="26" height="26"/><text class="ed-v" x="303" y="359" text-anchor="middle">3</text><rect class="ed-cell" x="316" y="342" width="26" height="26"/><text class="ed-v" x="329" y="359" text-anchor="middle">3</text><rect class="ed-cell ed-same" x="342" y="342" width="26" height="26"/><text class="ed-v" x="355" y="359" text-anchor="middle">2</text><rect class="ed-cell" x="368" y="342" width="26" height="26"/><text class="ed-v" x="381" y="359" text-anchor="middle">3</text><rect class="ed-cell ed-out" x="56" y="368" width="26" height="26"/><rect class="ed-cell ed-out" x="82" y="368" width="26" height="26"/><rect class="ed-cell ed-out" x="108" y="368" width="26" height="26"/><rect class="ed-cell ed-out" x="134" y="368" width="26" height="26"/><rect class="ed-cell ed-out" x="160" y="368" width="26" height="26"/><rect class="ed-cell ed-out" x="186" y="368" width="26" height="26"/><rect class="ed-cell ed-out" x="212" y="368" width="26" height="26"/><rect class="ed-cell ed-out" x="238" y="368" width="26" height="26"/><rect class="ed-cell ed-out" x="264" y="368" width="26" height="26"/><rect class="ed-cell ed-out" x="290" y="368" width="26" height="26"/><rect class="ed-cell" x="316" y="368" width="26" height="26"/><text class="ed-v" x="329" y="385" text-anchor="middle">4</text><rect class="ed-cell" x="342" y="368" width="26" height="26"/><text class="ed-v" x="355" y="385" text-anchor="middle">3</text><rect class="ed-cell ed-same" x="368" y="368" width="26" height="26"/><text class="ed-v" x="381" y="385" text-anchor="middle">2</text></svg>

    <!-- /gen -->

    החיסכון גדל עם הזרם :

    <!-- gen 6 -->

    | הזרמים | הסף d | תאים בטבלה המלאה | תאים ברצועה |
    |---|:-:|:-:|:-:|
    | שני זרמים של 12 חבילות | 2 | 144 | 54 |
    | שני זרמים של 1,000 חבילות | 3 | 1,000,000 | 6,988 |
    | שני זרמים של 1,000,000 חבילות | 10 | 1,000,000,000,000 | 20,999,890 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **האורכים :** אם \( |m - n| > d \), המרחק גדול מ-\( d \). אין צורך לחשב.
    2. **שורה אחרי שורה :** בשורה \( i \) מחשבים רק את \( j \) מ-\( i - d \) עד \( i + d \).
       שכן מחוץ לרצועה נחשב ל-\( d + 1 \).
    3. **עצירה מוקדמת :** המסלול הזול ביותר עובר בכל שורה. אם כל התאים של השורה גדולים מ-\( d \),
       המרחק גדול מ-\( d \).
    4. **התשובה :** התא \( (m, n) \), אם הוא לכל היותר \( d \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="edit_distance_within" linenums="1" hl_lines="11 15 16 17 18"
        def edit_distance_within(a, b, d):
            """The distance when it is at most d, else None: only the cells with |i - j| <= d,
            a cell outside them counts as d + 1."""
            m, n = len(a), len(b)
            if abs(m - n) > d:
                return None
            big = d + 1
            prev = {j: j for j in range(0, min(n, d) + 1)}
            for i in range(1, m + 1):
                cur = {}
                for j in range(max(0, i - d), min(n, i + d) + 1):
                    if j == 0:
                        cur[j] = i
                        continue
                    cur[j] = min(prev.get(j, big) + 1, cur.get(j - 1, big) + 1,
                                 prev.get(j - 1, big) + (a[i - 1] != b[j - 1]))   # (1)!
                if min(cur.values()) > d:
                    return None                                  # (2)!
                prev = cur
            return prev[n] if prev[n] <= d else None
        ```

        1. הנוסחה של סעיף א. ‏`get(..., big)` הוא שכן מחוץ לרצועה.
        2. המסלול הזול ביותר עובר בשורה הזו, והערכים לאורכו לא יורדים : כל צעד מוסיף 0 או 1.

    === "SystemVerilog"
        ```systemverilog title="function automatic int edit_distance_within" linenums="1" hl_lines="18 19 20 26"
        // The distance when it is at most d, else -1: only the cells with |i - j| <= d, cell
        // (i, j) at k = j - i + d of its row, a cell outside the band counted as d + 1
        function automatic int edit_distance_within(string a, string b, int d);
          int m = a.len(), n = b.len(), big = d + 1;
          int prev[], cur[];
          int j, v, best;
          if (m - n > d || n - m > d) return -1;
          prev = new[2 * d + 1];
          cur = new[2 * d + 1];
          for (int k = 0; k <= 2 * d; k++) prev[k] = (k >= d && k - d <= n) ? k - d : big;
          for (int i = 1; i <= m; i++) begin
            best = big;
            for (int k = 0; k <= 2 * d; k++) begin
              j = i + k - d;
              if (j < 0 || j > n) v = big;
              else if (j == 0) v = i;
              else begin
                v = prev[k] + int'(a[i - 1] != b[j - 1]);                    // (i - 1, j - 1)
                if (k < 2 * d && prev[k + 1] + 1 < v) v = prev[k + 1] + 1;  // (i - 1, j)
                if (k > 0 && cur[k - 1] + 1 < v) v = cur[k - 1] + 1;        // (i, j - 1)
                if (v > big) v = big;
              end
              cur[k] = v;
              if (v < best) best = v;
            end
            if (best > d) return -1;
            prev = cur;
          end
          return prev[n - m + d] <= d ? prev[n - m + d] : -1;
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **חסם מלמטה.** ביישור של \( a_1 \ldots a_i \) ו-\( b_1 \ldots b_j \), כל עמודה עם זוג
    חבילות לוקחת אחת מכל צד. אם \( i > j \), לפחות \( i - j \) חבילות של `a` נשארות מול חור.
    לכן \( d[i][j] \ge |i - j| \).

    **המסלול נשאר ברצועה.** כל צעד במסלול הזול ביותר מוסיף לערך 0 או 1, ולכן הערכים לאורכו
    לא יורדים, ובפינה יש \( d[m][n] \).
    אם \( d[m][n] \le d \), כל תא במסלול מקיים \( |i - j| \le d[i][j] \le d \).

    **מה הקוד מחשב.** תא ברצועה מחושב מהשכנים שלו ברצועה בלבד, ולכן הערך שלו הוא המחיר של
    המסלול הזול ביותר שכולו ברצועה. זה לפחות הערך האמיתי, וכשהמרחק לכל היותר \( d \) המסלול
    הזול ביותר כולו ברצועה, ולכן הערך שווה בדיוק. כשהמרחק גדול מ-\( d \), גם הערך המחושב גדול
    מ-\( d \), והקוד עונה נכון שהמרחק גדול מ-\( d \).

    **העצירה המוקדמת.** המסלול הזול ביותר מ-\( (0, 0) \) ל-\( (m, n) \) עובר בכל שורה, והערכים
    לאורכו לא יורדים. אם המרחק לכל היותר \( d \), התא שלו בשורה הזו נמצא ברצועה ושווה לכל היותר
    \( d \). לכן אם כל השורה גדולה מ-\( d \), גם המרחק.

    #### סיבוכיות { .sol-cost }

    ‏\( 2d + 1 \) תאים בכל אחת מ-\( m \) השורות : זמן \( O(m \cdot d) \), וזיכרון של שתי שורות
    של הרצועה, \( O(d) \). כשלא יודעים את \( d \) מראש מתחילים ב-\( d = 1 \) ומכפילים פי 2
    עד שיש תשובה : הזמן הכולל הוא \( O(m \cdot D) \), כש-\( D \) המרחק האמיתי.

    ב-scoreboard של מיליון חבילות, עד סוף הבדיקה הזיכרון מחזיק את שני התורים : מיליון חבילות
    בכל אחד, או מזהה של 8 בתים לכל חבילה, ‏8 MB לתור. המרחק לבדו צריך עוד שתי שורות של
    הרצועה. לדוח שומרים את הרצועה כולה, כי ההליכה אחורה של סעיף ב לא יוצאת ממנה : עם
    \( d = 10 \) זה כ-21 מיליון תאים, בית לכל תא (הערכים עד \( d + 1 \)), כ-21 MB במקום
    \( 10^{12} \).

---

### סעיף ד – שתי חבילות שהתחלפו

שתי תשובות שהגיעו בסדר הפוך : `ABCDEFGH` מול `ABDCEFHG`. בסעיפים הקודמים כל זוג כזה עולה 2.
הוסיפו פעולה רביעית, החלפה של שתי חבילות צמודות במחיר 1, ותקנו את הנוסחה.

??? tip "רמז 1"
    כמה תאים אחורה בטבלה לוקחת החלפה של שתי חבילות?

??? tip "רמז 2"
    מתי מותר להשתמש בה? השוו את שתי החבילות האחרונות של כל קידומת.

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        **‏2 במקום 4.** לנוסחה נוסף איבר רביעי, \( d[i-2][j-2] + 1 \), כש-\( a_i = b_{j-1} \)
        ו-\( a_{i-1} = b_j \) : שתי החבילות האחרונות של `a` הן שתי האחרונות של `b` בסדר
        הפוך. ‏CD התחלפו ל-DC, ו-GH התחלפו ל-HG.

    <!-- cost: זמן \( O(m \cdot n) \) | זיכרון \( O(m \cdot n) \) -->

    #### הרעיון { .sol-idea }

    החלפה של שתי חבילות צמודות היא צעד של שתי שורות ושתי עמודות באלכסון, בבת אחת. מותר
    לעשות אותו רק כשהזוג האחרון של כל קידומת הוא אותו זוג בסדר הפוך. חבילה שזזה רחוק, כמו
    ב-`ABCD` מול `BCDA`, היא לא החלפה של שכנות, ונשארת חסרה ומיותרת :

    <!-- gen 7 -->

    | הצפוי מול בפועל | בלי החלפה | עם החלפה של שכנות | הדוח עם החלפה |
    |---|:-:|:-:|---|
    | ‏`ABCDEFGH` מול `ABDCEFHG` | 4 | 2 | התחלפו <span dir="ltr">CD</span> ל-<span dir="ltr">DC</span>, התחלפו <span dir="ltr">GH</span> ל-<span dir="ltr">HG</span> |
    | ‏`ABCDEF` מול `ABDCEF` | 2 | 1 | התחלפו <span dir="ltr">CD</span> ל-<span dir="ltr">DC</span> |
    | ‏`ABCD` מול `BCDA` | 2 | 2 | חסרה A, מיותרת A |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **כמו בסעיף א :** אותה שורה ואותה עמודה של 0, ואותן שלוש אפשרויות.
    2. **האפשרות הרביעית :** אם \( i, j \ge 2 \), ‏\( a_i = b_{j-1} \) ו-\( a_{i-1} = b_j \), גם
       \( d[i-2][j-2] + 1 \).
    3. **התשובה :** ‏\( d[m][n] \). הצעד החדש חוזר שתי שורות אחורה, ולכן שומרים שלוש שורות, או את כל הטבלה.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="edit_distance_swaps" linenums="1" hl_lines="8 9"
        def edit_distance_swaps(a, b):
            """The distance when two neighbouring packets that came in the opposite order count
            as one edit (each packet edited at most once)."""
            d = [[i + j if i == 0 or j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
            for i in range(1, len(a) + 1):
                for j in range(1, len(b) + 1):
                    d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
                    if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                        d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)    # (1)!
            return d[len(a)][len(b)]
        ```

        1. שתי החבילות האחרונות של `a` הן שתי האחרונות של `b` בסדר הפוך : החלפה אחת, ושתי
           שורות ושתי עמודות אחורה.

    === "SystemVerilog"
        ```systemverilog title="function automatic int edit_distance_swaps" linenums="1" hl_lines="15 16"
        // The distance when two neighbouring packets that came in the opposite order count as
        // one edit (each packet edited at most once)
        function automatic int edit_distance_swaps(string a, string b);
          int d[][];
          d = new[a.len() + 1];
          foreach (d[r]) begin
            d[r] = new[b.len() + 1];
            foreach (d[r][c]) d[r][c] = (r == 0 || c == 0) ? r + c : 0;
          end
          for (int i = 1; i <= a.len(); i++)
            for (int j = 1; j <= b.len(); j++) begin
              d[i][j] = d[i - 1][j - 1] + int'(a[i - 1] != b[j - 1]);
              if (d[i - 1][j] + 1 < d[i][j]) d[i][j] = d[i - 1][j] + 1;
              if (d[i][j - 1] + 1 < d[i][j]) d[i][j] = d[i][j - 1] + 1;
              if (i > 1 && j > 1 && a[i - 1] == b[j - 2] && a[i - 2] == b[j - 1] &&
                  d[i - 2][j - 2] + 1 < d[i][j]) d[i][j] = d[i - 2][j - 2] + 1;
            end
          return d[a.len()][b.len()];
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **ארבעה מקרים.** כאן כל חבילה משתתפת לכל היותר בפעולה אחת. אז בסוף של יישור יש עמודה של
    סעיף א, או החלפה : \( a_{i-1} a_i \) מול \( b_{j-1} b_j \) בסדר הפוך. אם מורידים את ההחלפה,
    נשאר יישור של \( (i-2, j-2) \) בעלות שקטנה ב-1. זה האיבר הרביעי, וההוכחה של סעיף א עובדת
    עם ארבעה מקרים במקום שלושה.

    **הדוגמה.** ‏`ABCDEFGH` מול `ABDCEFHG` : בלי החלפה כל זוג עולה 2, למשל C חסרה ו-C
    מיותרת, ובסך הכול 4. עם החלפה, ‏\( d[4][4] = d[2][2] + 1 = 1 \) ו-\( d[8][8] = d[6][6] + 1 = 2 \).

    **נסו בעצמכם.** כבו את "גם החלפה של שכנות" ובדקו איך כל החלפה נהיית חסרה ומיותרת. אחר כך
    לחצו על המלכודת "CA מול ABC" : הטבלה נותנת 3, אבל יש דרך בשתי פעולות. מצאו אותה. ומה
    קורה ב"חבילה שזזה רחוק"?

    <div class="explorer" data-kind="editdist" data-a="ABCDEFGH" data-b="ABDCEFHG" data-swap="1"></div>

    #### סיבוכיות { .sol-cost }

    עדיין \( O(1) \) לכל תא : זמן \( O(m \cdot n) \). המרחק לבדו צריך שלוש שורות, \( O(n) \)
    זיכרון. הקוד כאן שומר את כל הטבלה, \( O(m \cdot n) \), כדי שאפשר יהיה לבנות ממנה דוח כמו
    בסעיף ב.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : השוואה של מקום מול מקום"
    ‏`ABCDEFGH` מול `ABDEYGHH` נותן חמש חבילות שונות מתוך שמונה, כי C שחסרה מזיזה את כל מה
    שאחריה. דוח כזה מטביע את מהנדס האימות בהבדלים שלא קרו. המרחק הוא 3, ושלוש שורות בדוח.

??? trap "מלכודת : השורה והעמודה של 0"
    אם מאתחלים אותן ל-0 במקום \( j \) ו-\( i \), חבילות מיותרות בתחילת הזרם לא עולות כלום.
    ‏`AB` מול `XAB` יוצא 0 במקום 1, ו-`ABC` מול זרם ריק יוצא 0 במקום 3.

??? trap "מלכודת : דוח משתי שורות"
    הקוד של סעיף א שומר שתי שורות, וזה מספיק למרחק. אבל ההליכה אחורה של סעיף ב צריכה את כל
    הטבלה. מי שמקצר את הזיכרון ואחר כך מנסה לבנות דוח, מגלה שהשורות שהוא צריך כבר נמחקו.

??? trap "מלכודת : החלפה של שכנות היא לא כל מה ש-Damerau מאפשר"
    סעיף ד סופר כל חבילה לכל היותר בפעולה אחת. ‏`CA` מול `ABC` יוצא שם 3, אבל בשתי פעולות
    אפשר : להחליף ל-`AC` ואז להכניס B באמצע. הגרסה שמאפשרת לערוך שוב זוג שהתחלף צריכה טבלה
    עם עוד מידע, על המקום האחרון של כל חבילה.

??? followup "שאלות המשך"
    - **בלי שיבוש :** אם יש רק חבילות חסרות ומיותרות, מה המרחק?

        ??? fu-answer "תשובה"
            ‏\( m + n - 2 \cdot \text{LCS} \), כש-LCS הוא האורך של תת-הסדרה המשותפת הארוכה ביותר.
            בדוגמה של סעיף א תת-הסדרה היא `ABDEGH`, באורך 6, והמרחק \( 8 + 8 - 12 = 4 \) : השיבוש
            של F ל-Y עולה כאן 2.

    - **דוח בזיכרון קטן :** איך בונים את הדוח של סעיף ב בזיכרון \( O(n) \)?

        ??? fu-answer "תשובה"
            האלגוריתם של Hirschberg. מחשבים את השורה האמצעית מלמעלה ואת אותה שורה מלמטה, ושתיהן
            יחד מראות איפה המסלול חוצה אותה. אחר כך פותרים כל חצי בנפרד. הזמן נשאר
            \( O(m \cdot n) \), פי 2 בערך.

    - **מחירים שונים :** חבילה חסרה חמורה יותר מחבילה מיותרת. מה משתנה?

        ??? fu-answer "תשובה"
            רק המחירים בנוסחה : \( d[i-1][j] + c_{\text{miss}} \), \( d[i][j-1] + c_{\text{extra}} \),
            ושיבוש ב-\( c_{\text{chg}} \). השורה והעמודה של 0 הן סכומים של המחירים. ההוכחה לא
            משתנה.

    - **חבילה שזזה רחוק :** ‏`ABCD` מול `BCDA` עולה 2 גם עם החלפה של שכנות. מה ה-scoreboard
      צריך לעשות כשתשובות מגיעות שלא לפי הסדר?

        ??? fu-answer "תשובה"
            להפסיק להשוות לפי הסדר. אם לכל תשובה יש מזהה, מתאימים לפי המזהה, תור לכל מזהה, כמו
            ב-[שאלה 0050](0050-out-of-order-scoreboard.md). מרחק העריכה מתאים לזרם שאמור להגיע
            לפי הסדר.

    - **בחומרה :** איך מחשבים את הטבלה מהר יותר מתא בכל שעון?

        ??? fu-answer "תשובה"
            כל התאים על אנטי-אלכסון אחד, \( i + j = k \), תלויים רק באנטי-אלכסונים \( k - 1 \)
            ו-\( k - 2 \). מערך סיסטולי של \( n \) יחידות מחשב אנטי-אלכסון שלם בכל שעון, וכל
            הטבלה נגמרת אחרי \( m + n - 1 \) שעונים.
