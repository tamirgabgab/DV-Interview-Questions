---
id: 63
title: המקסימום בחלון נע – deque, החלון הארוך עם max − min ≤ limit, ובחומרה
level: junior
difficulty: medium
kind: code
tags: [algorithms, sliding-window, python, systemverilog]
source: "שאלה קלאסית (Sliding Window Maximum), וסעיף ב הוא Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit"
added: 2026-10-29
---

## השאלה

נתון מערך של \( n \) מספרים שלמים ומספר \( k \), עם \( 1 \le k \le n \). **חלון** בגודל \( k \) הוא
\( k \) ערכים רצופים של המערך, ויש \( n - k + 1 \) חלונות כאלה : זה שמתחיל במקום 0, זה שמתחיל
במקום 1, וכן הלאה. החזירו את המקסימום של כל חלון, לפי הסדר.

דוגמה : במערך <span dir="ltr">1 3 −1 −3 5 3 6 7</span> עם \( k = 3 \) החלונות הם
<span dir="ltr">[1 3 −1]</span>, ‏<span dir="ltr">[3 −1 −3]</span>, ‏<span dir="ltr">[−1 −3 5]</span>
וכן הלאה, והתשובה היא <span dir="ltr">3 3 5 5 6 7</span>.

**ההקשר באימות :** מוניטור שמדווח בכל מחזור על ה-latency הגבוה ביותר ב-\( k \) הטרנזקציות
האחרונות, או על התפוסה הגבוהה ביותר של תור ב-\( k \) המחזורים האחרונים (watermark נע במקום
שיא מתחילת הריצה), עונה בדיוק על השאלה הזו. וכשה-DUT עצמו מחשב מקסימום נע, ה-scoreboard
צריך מודל ייחוס שרץ בזמן ליניארי על טרייס של מיליוני מחזורים : זה סעיף א, וה-DUT הוא סעיף ג.

- **סעיף א – המקסימום של כל חלון :** כתבו פונקציה בזמן \( O(n) \), ולא \( O(n \cdot k) \).
- **סעיף ב – חלון באורך משתנה :** במקום \( k \) קבוע, נתון מספר \( \text{limit} \ge 0 \). מה
  האורך של הקטע הרציף הארוך ביותר שבו המקסימום פחות המינימום הוא לכל היותר
  \( \text{limit} \)?
- **סעיף ג – בחומרה :** דגימה אחת של \( W \) ביטים נכנסת בכל מחזור, ובכל מחזור צריך לצאת
  המקסימום של \( K \) הדגימות האחרונות. כמה אחסון צריך, כמה משווים, ואיך עושים את זה
  בעבודה קבועה בכל מחזור? כתבו את המודול.

??? interviewer "מה המראיין בודק"
    - **מה אפשר לשכוח :** האם המועמד שם לב שערך ישן שקטן מערך חדש לא יהיה מקסימום יותר
      לעולם, ולכן אפשר לזרוק אותו. זה הצעד שמוביל מ-\( O(n \cdot k) \) ל-\( O(n) \).
    - **ניתוח אמורטיזציה :** צעד אחד יכול להוציא הרבה ערכים, ובכל זאת כל הריצה ליניארית. למה?
    - **ההכללה :** חלון ששני הקצוות שלו זזים בקצב שונה, ושני מבנים, אחד למקסימום ואחד
      למינימום. הקשר לחלון הנע של שני מצביעים.
    - **מתוכנה לחומרה :** לולאת `while` שעושה כמות עבודה משתנה לא נכנסת למחזור אחד. האם
      המועמד מוצא מה אפשר לעשות במקביל, וכמה אחסון הוא באמת המינימום.

---

### סעיף א – המקסימום של כל חלון

??? tip "רמז 1"
    נניח שבחלון יש ערך 2 במקום 4, ועכשיו נכנס ערך 5 במקום 6. האם ה-2 יכול להיות המקסימום של
    חלון כלשהו מעכשיו והלאה?

??? tip "רמז 2"
    שמרו רק את המקומות של הערכים שעדיין "יש להם סיכוי", מהישן לחדש. מה אפשר לומר על הערכים
    שלהם? איפה נמצא המקסימום, ומאיפה מוציאים ערך שיצא מהחלון?

<div class="selfcheck" data-answer="4" data-show="4 : אחד מהראש (המקום 1, שיצא מהחלון) ושלושה מהזנב (המקומות 2, 3 ו-4, כולם קטנים מ-10)" data-hint="לפני הצעד האחרון ה-deque מחזיק את המקומות 1 עד 4. בדקו קודם את הראש, ואז כמה ערכים בזנב קטנים מ-10." markdown>
במערך <span dir="ltr">9 8 7 6 5 10</span> עם \( k = 4 \), כמה מקומות יוצאים מה-deque, מהראש ומהזנב יחד,
בצעד של המקום האחרון (\( i = 5 \), הערך 10)?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שומרים deque של **מקומות** (אינדקסים) שהערכים שלהם יורדים מהראש לזנב. בכל צעד : אם הראש
        יצא מהחלון מוציאים אותו, מוציאים מהזנב כל ערך שאינו גדול מהערך החדש, ומכניסים את המקום
        החדש לזנב. הראש הוא המקסימום של החלון. כל מקום נכנס ויוצא פעם אחת, ולכן הזמן \( O(n) \).
        בדוגמה : <span dir="ltr">3 3 5 5 6 7</span>.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(k) \) -->

    #### הרעיון { .sol-idea }

    **מונחים.** ‏**deque** (קיצור של double-ended queue) הוא תור ששני הקצוות שלו פתוחים :
    אפשר להכניס ולהוציא גם בראש (front) וגם בזנב (back), כל פעולה ב-\( O(1) \). ב-Python זה
    `collections.deque`, וב-SystemVerilog תור `int q[$]` עם `push_back`, ‏`pop_back` ו-`pop_front`.
    בפתרון נשמור ב-deque **מקומות** במערך, לא ערכים, כי צריך לדעת מתי ערך יוצא מהחלון.

    **ערך נשלט.** נניח שבמקום \( j \) יש ערך, ובמקום מאוחר יותר \( i > j \) יש ערך גדול ממנו או
    שווה לו. מרגע ש-\( i \) נכנס, כל חלון שמכיל את \( j \) מכיל גם את \( i \), כי \( i \) יוצא
    מהחלון רק אחרי \( j \). לכן הערך שב-\( j \) לא יהיה מקסימום שהערך שב-\( i \) לא מכסה, ואפשר
    לשכוח אותו ברגע ש-\( i \) נכנס. נשארים רק מועמדים : מקומות שהערך שלהם **גדול** מכל ערך שבא
    אחריהם בחלון. מהישן לחדש, הערכים של המועמדים יורדים, ולכן הישן ביותר הוא הגדול ביותר : הוא
    המקסימום של החלון. deque כזה, שהערכים בו מסודרים, נקרא **deque מונוטוני**.

    באיור, שורה לכל מקום \( i \) של הדוגמה : החלון של \( k = 3 \) הערכים האחרונים מוקף, המקומות
    שב-deque צבועים, הראש מודגש, והמקומות שיצאו באותו צעד מחוקים. בשורה של \( i = 4 \) הערך 5
    נכנס ומוציא שלושה מקומות בבת אחת :

    <!-- gen 0 -->

    <svg class="figure sm-fig" viewBox="0 0 386 324" style="max-width:24.125rem" role="img" aria-label="המערך 1 3 −1 −3 5 3 6 7 עם k = 3 : ה-deque אחרי כל אינדקס, והמקסימום של כל חלון"><text class="tick" x="75" y="14" text-anchor="middle">0</text><text class="tick" x="109" y="14" text-anchor="middle">1</text><text class="tick" x="143" y="14" text-anchor="middle">2</text><text class="tick" x="177" y="14" text-anchor="middle">3</text><text class="tick" x="211" y="14" text-anchor="middle">4</text><text class="tick" x="245" y="14" text-anchor="middle">5</text><text class="tick" x="279" y="14" text-anchor="middle">6</text><text class="tick" x="313" y="14" text-anchor="middle">7</text><text class="tick" x="50" y="14" text-anchor="end">index</text><text class="tick" x="358" y="14" text-anchor="middle">max</text><text class="sm-lab" x="50" y="49" text-anchor="end">i = 0</text><rect class="sm-win" x="59" y="29" width="32" height="30" rx="5"/><g class="sm-cell is-front"><title>i = 0: place 0, value 1, the front of the deque</title><rect x="61" y="32" width="28" height="24" rx="4"/><text x="75" y="49" text-anchor="middle">1</text></g><g class="sm-cell is-wait"><title>i = 0: place 1, value 3, not read yet</title><rect x="95" y="32" width="28" height="24" rx="4"/><text x="109" y="49" text-anchor="middle">3</text></g><g class="sm-cell is-wait"><title>i = 0: place 2, value -1, not read yet</title><rect x="129" y="32" width="28" height="24" rx="4"/><text x="143" y="49" text-anchor="middle">−1</text></g><g class="sm-cell is-wait"><title>i = 0: place 3, value -3, not read yet</title><rect x="163" y="32" width="28" height="24" rx="4"/><text x="177" y="49" text-anchor="middle">−3</text></g><g class="sm-cell is-wait"><title>i = 0: place 4, value 5, not read yet</title><rect x="197" y="32" width="28" height="24" rx="4"/><text x="211" y="49" text-anchor="middle">5</text></g><g class="sm-cell is-wait"><title>i = 0: place 5, value 3, not read yet</title><rect x="231" y="32" width="28" height="24" rx="4"/><text x="245" y="49" text-anchor="middle">3</text></g><g class="sm-cell is-wait"><title>i = 0: place 6, value 6, not read yet</title><rect x="265" y="32" width="28" height="24" rx="4"/><text x="279" y="49" text-anchor="middle">6</text></g><g class="sm-cell is-wait"><title>i = 0: place 7, value 7, not read yet</title><rect x="299" y="32" width="28" height="24" rx="4"/><text x="313" y="49" text-anchor="middle">7</text></g><text class="sm-out" x="358" y="49" text-anchor="middle">–</text><text class="sm-lab" x="50" y="85" text-anchor="end">i = 1</text><rect class="sm-win" x="59" y="65" width="66" height="30" rx="5"/><g class="sm-cell is-pop"><title>i = 1: place 0, value 1, left the deque at this index</title><rect x="61" y="68" width="28" height="24" rx="4"/><text x="75" y="85" text-anchor="middle">1</text></g><line class="sm-strike" x1="64" y1="89" x2="86" y2="71"/><g class="sm-cell is-front"><title>i = 1: place 1, value 3, the front of the deque</title><rect x="95" y="68" width="28" height="24" rx="4"/><text x="109" y="85" text-anchor="middle">3</text></g><g class="sm-cell is-wait"><title>i = 1: place 2, value -1, not read yet</title><rect x="129" y="68" width="28" height="24" rx="4"/><text x="143" y="85" text-anchor="middle">−1</text></g><g class="sm-cell is-wait"><title>i = 1: place 3, value -3, not read yet</title><rect x="163" y="68" width="28" height="24" rx="4"/><text x="177" y="85" text-anchor="middle">−3</text></g><g class="sm-cell is-wait"><title>i = 1: place 4, value 5, not read yet</title><rect x="197" y="68" width="28" height="24" rx="4"/><text x="211" y="85" text-anchor="middle">5</text></g><g class="sm-cell is-wait"><title>i = 1: place 5, value 3, not read yet</title><rect x="231" y="68" width="28" height="24" rx="4"/><text x="245" y="85" text-anchor="middle">3</text></g><g class="sm-cell is-wait"><title>i = 1: place 6, value 6, not read yet</title><rect x="265" y="68" width="28" height="24" rx="4"/><text x="279" y="85" text-anchor="middle">6</text></g><g class="sm-cell is-wait"><title>i = 1: place 7, value 7, not read yet</title><rect x="299" y="68" width="28" height="24" rx="4"/><text x="313" y="85" text-anchor="middle">7</text></g><text class="sm-out" x="358" y="85" text-anchor="middle">–</text><text class="sm-lab" x="50" y="121" text-anchor="end">i = 2</text><rect class="sm-win" x="59" y="101" width="100" height="30" rx="5"/><g class="sm-cell is-off"><title>i = 2: place 0, value 1, not in the deque</title><rect x="61" y="104" width="28" height="24" rx="4"/><text x="75" y="121" text-anchor="middle">1</text></g><g class="sm-cell is-front"><title>i = 2: place 1, value 3, the front of the deque</title><rect x="95" y="104" width="28" height="24" rx="4"/><text x="109" y="121" text-anchor="middle">3</text></g><g class="sm-cell is-in"><title>i = 2: place 2, value -1, in the deque</title><rect x="129" y="104" width="28" height="24" rx="4"/><text x="143" y="121" text-anchor="middle">−1</text></g><g class="sm-cell is-wait"><title>i = 2: place 3, value -3, not read yet</title><rect x="163" y="104" width="28" height="24" rx="4"/><text x="177" y="121" text-anchor="middle">−3</text></g><g class="sm-cell is-wait"><title>i = 2: place 4, value 5, not read yet</title><rect x="197" y="104" width="28" height="24" rx="4"/><text x="211" y="121" text-anchor="middle">5</text></g><g class="sm-cell is-wait"><title>i = 2: place 5, value 3, not read yet</title><rect x="231" y="104" width="28" height="24" rx="4"/><text x="245" y="121" text-anchor="middle">3</text></g><g class="sm-cell is-wait"><title>i = 2: place 6, value 6, not read yet</title><rect x="265" y="104" width="28" height="24" rx="4"/><text x="279" y="121" text-anchor="middle">6</text></g><g class="sm-cell is-wait"><title>i = 2: place 7, value 7, not read yet</title><rect x="299" y="104" width="28" height="24" rx="4"/><text x="313" y="121" text-anchor="middle">7</text></g><text class="sm-out is-val" x="358" y="121" text-anchor="middle">3</text><text class="sm-lab" x="50" y="157" text-anchor="end">i = 3</text><rect class="sm-win" x="93" y="137" width="100" height="30" rx="5"/><g class="sm-cell is-off"><title>i = 3: place 0, value 1, not in the deque</title><rect x="61" y="140" width="28" height="24" rx="4"/><text x="75" y="157" text-anchor="middle">1</text></g><g class="sm-cell is-front"><title>i = 3: place 1, value 3, the front of the deque</title><rect x="95" y="140" width="28" height="24" rx="4"/><text x="109" y="157" text-anchor="middle">3</text></g><g class="sm-cell is-in"><title>i = 3: place 2, value -1, in the deque</title><rect x="129" y="140" width="28" height="24" rx="4"/><text x="143" y="157" text-anchor="middle">−1</text></g><g class="sm-cell is-in"><title>i = 3: place 3, value -3, in the deque</title><rect x="163" y="140" width="28" height="24" rx="4"/><text x="177" y="157" text-anchor="middle">−3</text></g><g class="sm-cell is-wait"><title>i = 3: place 4, value 5, not read yet</title><rect x="197" y="140" width="28" height="24" rx="4"/><text x="211" y="157" text-anchor="middle">5</text></g><g class="sm-cell is-wait"><title>i = 3: place 5, value 3, not read yet</title><rect x="231" y="140" width="28" height="24" rx="4"/><text x="245" y="157" text-anchor="middle">3</text></g><g class="sm-cell is-wait"><title>i = 3: place 6, value 6, not read yet</title><rect x="265" y="140" width="28" height="24" rx="4"/><text x="279" y="157" text-anchor="middle">6</text></g><g class="sm-cell is-wait"><title>i = 3: place 7, value 7, not read yet</title><rect x="299" y="140" width="28" height="24" rx="4"/><text x="313" y="157" text-anchor="middle">7</text></g><text class="sm-out is-val" x="358" y="157" text-anchor="middle">3</text><text class="sm-lab" x="50" y="193" text-anchor="end">i = 4</text><rect class="sm-win" x="127" y="173" width="100" height="30" rx="5"/><g class="sm-cell is-off"><title>i = 4: place 0, value 1, not in the deque</title><rect x="61" y="176" width="28" height="24" rx="4"/><text x="75" y="193" text-anchor="middle">1</text></g><g class="sm-cell is-pop"><title>i = 4: place 1, value 3, left the deque at this index</title><rect x="95" y="176" width="28" height="24" rx="4"/><text x="109" y="193" text-anchor="middle">3</text></g><line class="sm-strike" x1="98" y1="197" x2="120" y2="179"/><g class="sm-cell is-pop"><title>i = 4: place 2, value -1, left the deque at this index</title><rect x="129" y="176" width="28" height="24" rx="4"/><text x="143" y="193" text-anchor="middle">−1</text></g><line class="sm-strike" x1="132" y1="197" x2="154" y2="179"/><g class="sm-cell is-pop"><title>i = 4: place 3, value -3, left the deque at this index</title><rect x="163" y="176" width="28" height="24" rx="4"/><text x="177" y="193" text-anchor="middle">−3</text></g><line class="sm-strike" x1="166" y1="197" x2="188" y2="179"/><g class="sm-cell is-front"><title>i = 4: place 4, value 5, the front of the deque</title><rect x="197" y="176" width="28" height="24" rx="4"/><text x="211" y="193" text-anchor="middle">5</text></g><g class="sm-cell is-wait"><title>i = 4: place 5, value 3, not read yet</title><rect x="231" y="176" width="28" height="24" rx="4"/><text x="245" y="193" text-anchor="middle">3</text></g><g class="sm-cell is-wait"><title>i = 4: place 6, value 6, not read yet</title><rect x="265" y="176" width="28" height="24" rx="4"/><text x="279" y="193" text-anchor="middle">6</text></g><g class="sm-cell is-wait"><title>i = 4: place 7, value 7, not read yet</title><rect x="299" y="176" width="28" height="24" rx="4"/><text x="313" y="193" text-anchor="middle">7</text></g><text class="sm-out is-val" x="358" y="193" text-anchor="middle">5</text><text class="sm-lab" x="50" y="229" text-anchor="end">i = 5</text><rect class="sm-win" x="161" y="209" width="100" height="30" rx="5"/><g class="sm-cell is-off"><title>i = 5: place 0, value 1, not in the deque</title><rect x="61" y="212" width="28" height="24" rx="4"/><text x="75" y="229" text-anchor="middle">1</text></g><g class="sm-cell is-off"><title>i = 5: place 1, value 3, not in the deque</title><rect x="95" y="212" width="28" height="24" rx="4"/><text x="109" y="229" text-anchor="middle">3</text></g><g class="sm-cell is-off"><title>i = 5: place 2, value -1, not in the deque</title><rect x="129" y="212" width="28" height="24" rx="4"/><text x="143" y="229" text-anchor="middle">−1</text></g><g class="sm-cell is-off"><title>i = 5: place 3, value -3, not in the deque</title><rect x="163" y="212" width="28" height="24" rx="4"/><text x="177" y="229" text-anchor="middle">−3</text></g><g class="sm-cell is-front"><title>i = 5: place 4, value 5, the front of the deque</title><rect x="197" y="212" width="28" height="24" rx="4"/><text x="211" y="229" text-anchor="middle">5</text></g><g class="sm-cell is-in"><title>i = 5: place 5, value 3, in the deque</title><rect x="231" y="212" width="28" height="24" rx="4"/><text x="245" y="229" text-anchor="middle">3</text></g><g class="sm-cell is-wait"><title>i = 5: place 6, value 6, not read yet</title><rect x="265" y="212" width="28" height="24" rx="4"/><text x="279" y="229" text-anchor="middle">6</text></g><g class="sm-cell is-wait"><title>i = 5: place 7, value 7, not read yet</title><rect x="299" y="212" width="28" height="24" rx="4"/><text x="313" y="229" text-anchor="middle">7</text></g><text class="sm-out is-val" x="358" y="229" text-anchor="middle">5</text><text class="sm-lab" x="50" y="265" text-anchor="end">i = 6</text><rect class="sm-win" x="195" y="245" width="100" height="30" rx="5"/><g class="sm-cell is-off"><title>i = 6: place 0, value 1, not in the deque</title><rect x="61" y="248" width="28" height="24" rx="4"/><text x="75" y="265" text-anchor="middle">1</text></g><g class="sm-cell is-off"><title>i = 6: place 1, value 3, not in the deque</title><rect x="95" y="248" width="28" height="24" rx="4"/><text x="109" y="265" text-anchor="middle">3</text></g><g class="sm-cell is-off"><title>i = 6: place 2, value -1, not in the deque</title><rect x="129" y="248" width="28" height="24" rx="4"/><text x="143" y="265" text-anchor="middle">−1</text></g><g class="sm-cell is-off"><title>i = 6: place 3, value -3, not in the deque</title><rect x="163" y="248" width="28" height="24" rx="4"/><text x="177" y="265" text-anchor="middle">−3</text></g><g class="sm-cell is-pop"><title>i = 6: place 4, value 5, left the deque at this index</title><rect x="197" y="248" width="28" height="24" rx="4"/><text x="211" y="265" text-anchor="middle">5</text></g><line class="sm-strike" x1="200" y1="269" x2="222" y2="251"/><g class="sm-cell is-pop"><title>i = 6: place 5, value 3, left the deque at this index</title><rect x="231" y="248" width="28" height="24" rx="4"/><text x="245" y="265" text-anchor="middle">3</text></g><line class="sm-strike" x1="234" y1="269" x2="256" y2="251"/><g class="sm-cell is-front"><title>i = 6: place 6, value 6, the front of the deque</title><rect x="265" y="248" width="28" height="24" rx="4"/><text x="279" y="265" text-anchor="middle">6</text></g><g class="sm-cell is-wait"><title>i = 6: place 7, value 7, not read yet</title><rect x="299" y="248" width="28" height="24" rx="4"/><text x="313" y="265" text-anchor="middle">7</text></g><text class="sm-out is-val" x="358" y="265" text-anchor="middle">6</text><text class="sm-lab" x="50" y="301" text-anchor="end">i = 7</text><rect class="sm-win" x="229" y="281" width="100" height="30" rx="5"/><g class="sm-cell is-off"><title>i = 7: place 0, value 1, not in the deque</title><rect x="61" y="284" width="28" height="24" rx="4"/><text x="75" y="301" text-anchor="middle">1</text></g><g class="sm-cell is-off"><title>i = 7: place 1, value 3, not in the deque</title><rect x="95" y="284" width="28" height="24" rx="4"/><text x="109" y="301" text-anchor="middle">3</text></g><g class="sm-cell is-off"><title>i = 7: place 2, value -1, not in the deque</title><rect x="129" y="284" width="28" height="24" rx="4"/><text x="143" y="301" text-anchor="middle">−1</text></g><g class="sm-cell is-off"><title>i = 7: place 3, value -3, not in the deque</title><rect x="163" y="284" width="28" height="24" rx="4"/><text x="177" y="301" text-anchor="middle">−3</text></g><g class="sm-cell is-off"><title>i = 7: place 4, value 5, not in the deque</title><rect x="197" y="284" width="28" height="24" rx="4"/><text x="211" y="301" text-anchor="middle">5</text></g><g class="sm-cell is-off"><title>i = 7: place 5, value 3, not in the deque</title><rect x="231" y="284" width="28" height="24" rx="4"/><text x="245" y="301" text-anchor="middle">3</text></g><g class="sm-cell is-pop"><title>i = 7: place 6, value 6, left the deque at this index</title><rect x="265" y="284" width="28" height="24" rx="4"/><text x="279" y="301" text-anchor="middle">6</text></g><line class="sm-strike" x1="268" y1="305" x2="290" y2="287"/><g class="sm-cell is-front"><title>i = 7: place 7, value 7, the front of the deque</title><rect x="299" y="284" width="28" height="24" rx="4"/><text x="313" y="301" text-anchor="middle">7</text></g><text class="sm-out is-val" x="358" y="301" text-anchor="middle">7</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="sm-key-win"></i>החלון של k הערכים האחרונים</span><span><i class="sm-key-in"></i>אינדקס ב-deque</span><span><i class="sm-key-front"></i>הראש של ה-deque, המקסימום</span><span><i class="sm-key-pop"></i>יצא מה-deque באינדקס הזה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הראש יצא מהחלון :** החלון שנגמר ב-\( i \) מתחיל ב-\( i - k + 1 \). אם המקום שבראש הוא
       \( i - k \), הוא כבר מחוץ לחלון, ומוציאים אותו מהראש. בכל צעד יוצא כך מקום אחד לכל היותר.
    2. **מנקים את הזנב :** כל עוד הערך של המקום שבזנב קטן מהערך החדש \( x \) או שווה לו, מוציאים
       אותו מהזנב. הוא נשלט על ידי \( x \).
    3. **מכניסים :** את \( i \) לזנב. הערכים ב-deque עדיין יורדים מהראש לזנב.
    4. **הפלט :** מ-\( i = k - 1 \) והלאה (מהחלון המלא הראשון), הערך של הראש הוא המקסימום של
       החלון שנגמר ב-\( i \).

    </div>

    על הדוגמה, \( k = 3 \). ב-deque כל ערך כתוב עם המקום שלו מתחתיו, מהראש (משמאל) לזנב :

    <!-- gen 2 -->

    | ‏i | הערך | יצא מהראש | יצאו מהזנב | ה-deque אחרי הצעד | המקסימום |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏0 | ‏1 | אין | אין | ‏<span dir="ltr">1<sub>0</sub></span> | עוד אין חלון |
    | ‏1 | ‏3 | אין | ‏<span dir="ltr">1<sub>0</sub></span> | ‏<span dir="ltr">3<sub>1</sub></span> | עוד אין חלון |
    | ‏2 | ‏<span dir="ltr">−1</span> | אין | אין | ‏<span dir="ltr">3<sub>1</sub> −1<sub>2</sub></span> | **‏3** |
    | ‏3 | ‏<span dir="ltr">−3</span> | אין | אין | ‏<span dir="ltr">3<sub>1</sub> −1<sub>2</sub> −3<sub>3</sub></span> | **‏3** |
    | ‏4 | ‏5 | ‏3<sub>1</sub> | ‏<span dir="ltr">−3<sub>3</sub> −1<sub>2</sub></span> | ‏<span dir="ltr">5<sub>4</sub></span> | **‏5** |
    | ‏5 | ‏3 | אין | אין | ‏<span dir="ltr">5<sub>4</sub> 3<sub>5</sub></span> | **‏5** |
    | ‏6 | ‏6 | אין | ‏<span dir="ltr">3<sub>5</sub> 5<sub>4</sub></span> | ‏<span dir="ltr">6<sub>6</sub></span> | **‏6** |
    | ‏7 | ‏7 | אין | ‏<span dir="ltr">6<sub>6</sub></span> | ‏<span dir="ltr">7<sub>7</sub></span> | **‏7** |

    <!-- /gen -->

    בצעד \( i = 1 \) הערך 3 מוציא את ה-1 שלפניו. בצעד \( i = 3 \) ה-deque מחזיק שלושה מקומות,
    כגודל החלון, כי הערכים <span dir="ltr">3 −1 −3</span> יורדים. בצעד \( i = 4 \) הראש, המקום 1,
    יוצא מהחלון, ואז הערך 5 מוציא מהזנב את <span dir="ltr">−3</span> ואת <span dir="ltr">−1</span>.
    מכאן והלאה ה-deque קצר : 6 ו-7 גדולים מכל מה שלפניהם.

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function window_max" linenums="1" hl_lines="7 8 10"
        // the maximum of every window of k values: q is a deque of indices, front first, whose
        // values decrease from the front to the back
        function automatic void window_max(input int nums[], input int k, output int out[$]);
          int q[$];
          out = {};
          foreach (nums[i]) begin
            if (q.size() > 0 && q[0] == i - k) void'(q.pop_front());               // (1)!
            while (q.size() > 0 && nums[q[$]] <= nums[i]) void'(q.pop_back());     // (2)!
            q.push_back(i);
            if (i >= k - 1) out.push_back(nums[q[0]]);                             // (3)!
          end
        endfunction
        ```

        1. ‏`q[0]` הוא הראש. רק המקום \( i - k \) יכול לצאת מהחלון בצעד הזה, ולכן `if` ולא `while`.
        2. ‏`q[$]` הוא הזנב. ערך שאינו גדול מהחדש לא יהיה מקסימום יותר.
        3. החלון המלא הראשון נגמר ב-\( k - 1 \). מאז, בכל צעד יוצא ערך אחד.

    === "Python"
        ```python title="window_max" linenums="1" hl_lines="10 12 16"
        from collections import deque


        def window_max(nums: list[int], k: int) -> list[int]:
            """The maximum of every window of k values: q holds indices, and their values
            decrease from the front of the deque to its back."""
            q: deque[int] = deque()
            out = []
            for i, x in enumerate(nums):
                if q and q[0] == i - k:            # (1)!
                    q.popleft()
                while q and nums[q[-1]] <= x:      # (2)!
                    q.pop()
                q.append(i)
                if i >= k - 1:
                    out.append(nums[q[0]])         # (3)!
            return out
        ```

        1. ‏`q[0]` הוא הראש. רק המקום \( i - k \) יכול לצאת מהחלון בצעד הזה.
        2. ‏`q[-1]` הוא הזנב. ערך שאינו גדול מ-\( x \) לא יהיה מקסימום יותר.
        3. מהחלון המלא הראשון והלאה, הראש הוא המקסימום.

    #### למה זה נכון { .sol-proof }

    **שמורה :** אחרי הצעד של \( i \), ה-deque מחזיק, לפי הסדר, בדיוק את המקומות \( j \) של החלון
    \( [i - k + 1, i] \) שהערך שלהם גדול מכל ערך שבא אחריהם עד \( i \). באינדוקציה על \( i \) :

    - **הראש :** החלון זז במקום אחד, ולכן רק \( i - k \) יוצא ממנו. אם הוא ב-deque, הוא בראש,
      כי הוא הישן ביותר. שלב 1 מוציא אותו.
    - **הזנב :** המקומות שהערך שלהם אינו גדול מ-\( x \) מפסיקים לקיים את התנאי, וכל השאר ממשיכים
      לקיים אותו. הערכים ב-deque יורדים, ולכן הנפסלים הם בדיוק רצף בסוף, ושלב 2 מוציא אותם
      ועוצר בראשון שגדול מ-\( x \).
    - **החדש :** אחרי \( i \) אין אף ערך, ולכן \( i \) מקיים את התנאי ונכנס בשלב 3.

    **הראש הוא המקסימום :** יהי \( M \) המקסימום של החלון, ו-\( j^* \) המקום האחרון שבו הוא מופיע.
    כל ערך אחרי \( j^* \) קטן מ-\( M \), ולכן \( j^* \) ב-deque, ואין לפניו ב-deque אף מקום, כי ערך
    שגדול מ-\( M \) לא קיים בחלון. לכן \( j^* \) בראש.

    **ערכים שווים, `<=` מול `<` :** הקוד מוציא מהזנב גם ערך **שווה** לחדש (`<=`). אם מוציאים רק
    ערך קטן ממנו (`<`), שני הערכים השווים נשארים, ה-deque יורד ולא יורד ממש, והראש הוא המופע
    **הראשון** של המקסימום. גם זה נכון, כי ההוצאה מהראש היא לפי מקום. ההבדל הוא באורך : עם
    `<=` ה-deque יורד ממש ולכן קצר יותר. במערך של ערכים שווים, <span dir="ltr">2 2 2 2 2</span>
    עם \( k = 3 \), ‏`<=` משאיר מקום אחד ו-`<` מגיע לשלושה.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n) \). צעד אחד יכול להוציא הרבה (בצעד \( i = 4 \) של הדוגמה שלושה), אבל כל
      מקום נכנס ל-deque פעם אחת ויוצא לכל היותר פעם אחת. לכן בכל הריצה יש לכל היותר \( 2n \)
      פעולות על ה-deque, כלומר \( O(1) \) בממוצע לצעד. זה ניתוח **אמורטיזציה** : המחיר של צעד
      יקר משולם על ידי הצעדים שהכניסו את מה שהוא הוציא.
    - **זיכרון :** ‏\( O(k) \) ל-deque : הוא מחזיק רק מקומות מהחלון, ומגיע ל-\( k \) במערך יורד. עוד
      \( n - k + 1 \) ערכים לפלט.
    - **מקרי קצה :** ‏\( k = 1 \) מחזיר את המערך עצמו, ו-\( k = n \) מחזיר ערך אחד, המקסימום של הכול.

    **נסו בעצמכם.** כל צעד הוא פעולה אחת על ה-deque : הוצאה מהראש, הוצאה מהזנב, או הכנסה עם
    הפלט. המספר שמתחת לסופר את הפעולות, ומראה שהן לכל היותר \( 2n \) :

    <div class="explorer" data-kind="slidemax" data-mode="a" data-nums="1 3 -1 -3 5 3 6 7" data-k="3"></div>

---

### סעיף ב – חלון באורך משתנה, max − min ≤ limit

??? tip "רמז 1"
    זה חלון נע של שני מצביעים, כמו בשאלה [0061](0061-longest-ones-with-k-flips.md) : הקצה הימני
    מתקדם תא אחרי תא, והשמאלי מתקדם כל עוד החלון לא חוקי. מה צריך לדעת על החלון כדי לבדוק אם
    הוא חוקי?

??? tip "רמז 2"
    צריך את המקסימום **ואת** המינימום של החלון, בזמן שני הקצוות זזים. שני deques כמו בסעיף א,
    אחד שהערכים בו יורדים ואחד שהערכים בו עולים. מה משתנה בהוצאה מהראש כשהקצה השמאלי קופץ?

<div class="selfcheck" data-answer="5" data-show="5 : המקומות 1 עד 5, ‏5 6 7 8 10 לא, כי 10 − 5 = 5. החלון הוא 6 7 8 10 6, המקומות 2 עד 6, עם 10 − 6 = 4" data-hint="חלון שמכיל את 10 לא יכול להכיל ערך קטן מ-6. חפשו את הקטע הארוך ביותר סביב ה-10 שכל הערכים בו לפחות 6." markdown>
במערך <span dir="ltr">1 5 6 7 8 10 6 5 6</span> עם \( \text{limit} = 4 \), מה האורך של הקטע
הארוך ביותר שבו המקסימום פחות המינימום הוא לכל היותר 4?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        חלון נע \( [\text{left}, \text{right}] \) עם שני deques : ‏`hi` (ערכים יורדים, בראש המקסימום)
        ו-`lo` (ערכים עולים, בראש המינימום). הקצה הימני מתקדם ונכנס לשניהם כמו בסעיף א. כל עוד
        המקסימום פחות המינימום גדול מ-\( \text{limit} \), הקצה השמאלי מתקדם, ומקום שבראש deque
        ושווה ל-\( \text{left} \) יוצא ממנו. התשובה היא החלון הארוך ביותר שנרשם : בדוגמה 4.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **חלון חוקי.** קטע \( [\text{left}, \text{right}] \) חוקי אם המקסימום שלו פחות המינימום שלו
    הוא לכל היותר \( \text{limit} \). כמו בשאלה 0061, מחפשים את הקטע החוקי הארוך ביותר בחלון נע :
    הקצה הימני \( \text{right} \) מתקדם תא אחרי תא, והקצה השמאלי \( \text{left} \) מתקדם רק כשהחלון
    לא חוקי. ב-0061 מונה אחד הספיק כדי לדעת אם החלון חוקי. כאן צריך את המקסימום ואת המינימום של
    חלון ששני הקצוות שלו זזים, כלומר שני deques מונוטוניים של סעיף א :

    - **‏`hi` :** מקומות שהערכים שלהם **יורדים** מהראש לזנב. בראש המקסימום של החלון.
    - **‏`lo` :** מקומות שהערכים שלהם **עולים** מהראש לזנב. בראש המינימום של החלון.

    ההבדל היחיד מסעיף א הוא בהוצאה מהראש. שם החלון זז במקום אחד בדיוק בכל צעד. כאן הקצה השמאלי
    יכול לעמוד כמה צעדים ואז לקפוץ כמה מקומות. לכן בודקים את הראש בכל התקדמות של
    \( \text{left} \) : אם הראש הוא \( \text{left} \) עצמו, הוא יוצא מהחלון יחד איתו.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הקצה הימני מתקדם :** הערך החדש \( x = \text{nums}[\text{right}] \). מוציאים מהזנב של `hi`
       כל ערך קטן מ-\( x \) או שווה לו, ומהזנב של `lo` כל ערך גדול מ-\( x \) או שווה לו. אחר כך
       \( \text{right} \) נכנס לזנב של שניהם.
    2. **החלון לא חוקי :** כל עוד \( \text{nums}[\text{hi}[0]] - \text{nums}[\text{lo}[0]] > \text{limit} \),
       הקצה השמאלי מתקדם במקום אחד. לפני ההתקדמות, אם הראש של `hi` או של `lo` הוא
       \( \text{left} \), הוא יוצא מהראש.
    3. **הטוב עד עכשיו :** החלון חוקי, והאורך \( \text{right} - \text{left} + 1 \) נבדק מול הטוב עד
       עכשיו.
    4. **הסוף :** אחרי שהקצה הימני עבר את כל המערך, הטוב עד עכשיו הוא התשובה.

    </div>

    על הדוגמה <span dir="ltr">10 1 2 4 7 2</span> עם \( \text{limit} = 5 \). ה-deques אחרי כל
    צעד, ערך עם המקום שלו מתחתיו, מהראש לזנב :

    <!-- gen 3 -->

    | ‏right | הערך | ‏hi (המקסימום) | ‏lo (המינימום) | ‏left | החלון | ‏max − min | הטוב עד עכשיו |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏0 | ‏10 | ‏<span dir="ltr">10<sub>0</sub></span> | ‏<span dir="ltr">10<sub>0</sub></span> | ‏0 | ‏0..0 | ‏0 | **‏1** |
    | ‏1 | ‏1 | ‏<span dir="ltr">1<sub>1</sub></span> | ‏<span dir="ltr">1<sub>1</sub></span> | ‏1 (זז ‏1) | ‏1..1 | ‏<span dir="ltr">9 → 0</span> | **‏1** |
    | ‏2 | ‏2 | ‏<span dir="ltr">2<sub>2</sub></span> | ‏<span dir="ltr">1<sub>1</sub> 2<sub>2</sub></span> | ‏1 | ‏1..2 | ‏1 | **‏2** |
    | ‏3 | ‏4 | ‏<span dir="ltr">4<sub>3</sub></span> | ‏<span dir="ltr">1<sub>1</sub> 2<sub>2</sub> 4<sub>3</sub></span> | ‏1 | ‏1..3 | ‏3 | **‏3** |
    | ‏4 | ‏7 | ‏<span dir="ltr">7<sub>4</sub></span> | ‏<span dir="ltr">2<sub>2</sub> 4<sub>3</sub> 7<sub>4</sub></span> | ‏2 (זז ‏1) | ‏2..4 | ‏<span dir="ltr">6 → 5</span> | **‏3** |
    | ‏5 | ‏2 | ‏<span dir="ltr">7<sub>4</sub> 2<sub>5</sub></span> | ‏<span dir="ltr">2<sub>5</sub></span> | ‏2 | ‏2..5 | ‏5 | **‏4** |

    <!-- /gen -->

    בצעד 1 נכנס 1 : המקסימום 10 והמינימום 1, הפרש 9. הקצה השמאלי עובר את המקום 0, וה-10 יוצא
    מהראש של `hi`. בצעד 4 נכנס 7 : החלון 1..4 הוא <span dir="ltr">1 2 4 7</span>, הפרש 6, והקצה
    השמאלי עובר את המקום 1 (ה-1 יוצא מהראש של `lo`). החלון 2..4 עם הפרש 5 חוקי. בצעד 5 נכנס 2,
    ‏`lo` מוציא את ה-2 הישן (שווה לחדש), והחלון 2..5, <span dir="ltr">2 4 7 2</span>, באורך 4.

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function longest_within" linenums="1" hl_lines="7 10 15"
        // the longest window whose max - min is at most limit: hi keeps the window's maximum at
        // its front (values decreasing), lo its minimum (values increasing)
        function automatic int longest_within(int nums[], int limit);
          int hi[$], lo[$], left = 0, best = 0;
          foreach (nums[right]) begin
            while (hi.size() > 0 && nums[hi[$]] <= nums[right]) void'(hi.pop_back());
            while (lo.size() > 0 && nums[lo[$]] >= nums[right]) void'(lo.pop_back());   // (1)!
            hi.push_back(right);
            lo.push_back(right);
            while (nums[hi[0]] - nums[lo[0]] > limit) begin                          // (2)!
              if (hi[0] == left) void'(hi.pop_front());
              if (lo[0] == left) void'(lo.pop_front());
              left++;
            end
            if (right - left + 1 > best) best = right - left + 1;
          end
          return best;
        endfunction
        ```

        1. המינימום : אותו ניקוי עם הסימן ההפוך. ב-`lo` הערכים עולים מהראש לזנב.
        2. החלון לא חוקי : הקצה השמאלי מתקדם, ומקום שבראש ושווה ל-`left` יוצא. הלולאה נעצרת, כי חלון של תא אחד חוקי.

    === "Python"
        ```python title="longest_within" linenums="1" hl_lines="13 17 23"
        from collections import deque


        def longest_within(nums: list[int], limit: int) -> int:
            """The longest window whose max - min is at most limit: hi keeps the window's
            maximum at its front (values decreasing), lo its minimum (values increasing)."""
            hi: deque[int] = deque()
            lo: deque[int] = deque()
            best = left = 0
            for right, x in enumerate(nums):
                while hi and nums[hi[-1]] <= x:
                    hi.pop()
                while lo and nums[lo[-1]] >= x:              # (1)!
                    lo.pop()
                hi.append(right)
                lo.append(right)
                while nums[hi[0]] - nums[lo[0]] > limit:     # (2)!
                    if hi[0] == left:
                        hi.popleft()
                    if lo[0] == left:
                        lo.popleft()
                    left += 1
                best = max(best, right - left + 1)
            return best
        ```

        1. המינימום : אותו ניקוי עם הסימן ההפוך. ב-`lo` הערכים עולים מהראש לזנב.
        2. החלון לא חוקי : הקצה השמאלי מתקדם, ומקום שבראש ושווה ל-`left` יוצא.

    #### למה זה נכון { .sol-proof }

    **ה-deques :** אותה שמורה כמו בסעיף א, על החלון \( [\text{left}, \text{right}] \) : ‏`hi` מחזיק
    את המקומות שהערך שלהם גדול מכל ערך אחריהם בחלון, ו-`lo` את אלה שהערך שלהם קטן מכל ערך
    אחריהם. כשהקצה הימני מתקדם, הניקוי של הזנב וההכנסה שומרים עליה בדיוק כמו בסעיף א. כשהקצה
    השמאלי מתקדם במקום אחד, רק \( \text{left} \) יוצא מהחלון, ואם הוא ב-deque הוא בראש. לכן הראש
    של `hi` הוא תמיד המקסימום של החלון, והראש של `lo` המינימום.

    **הקצה השמאלי לא חוזר אחורה :** אם \( [l, r] \) לא חוקי, גם \( [l, r + 1] \) לא חוקי : ערך נוסף
    יכול רק להגדיל את המקסימום ולהקטין את המינימום, ולכן ההפרש לא קטן. מכאן שההתחלה החוקית
    הקטנה ביותר עבור \( r + 1 \) אינה קטנה מזו של \( r \), והלולאה, שמתקדמת מ-\( \text{left} \) של
    הצעד הקודם, נעצרת בדיוק בה. חלון של תא אחד חוקי (הפרש 0), ולכן הלולאה תמיד נעצרת. בכל צעד
    החלון הוא החלון החוקי הארוך ביותר שנגמר ב-\( \text{right} \), והטוב מכולם הוא התשובה.

    **‏\( \text{limit} = 0 \) :** חלון חוקי הוא חלון שכל הערכים בו שווים, והתשובה היא הרצף הארוך
    ביותר של ערך אחד. ב-<span dir="ltr">4 2 2 2 4 4 2 2</span> זה 3. ועוד דוגמה :
    ב-<span dir="ltr">8 2 4 7</span> עם \( \text{limit} = 4 \) התשובה 2 (‏<span dir="ltr">2 4</span> או
    <span dir="ltr">4 7</span>).

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n) \). הקצה הימני זז \( n \) פעמים והשמאלי לכל היותר \( n \) פעמים, וכל מקום נכנס
      לכל deque פעם אחת ויוצא לכל היותר פעם אחת.
    - **זיכרון :** ‏\( O(n) \) במקרה הגרוע : החלון יכול להיות כל המערך, וב-deque יש עד כאורך החלון.

    **נסו בעצמכם.** אותה תיבה, עם שני ה-deques ושני הקצוות. כל צעד הוא פעולה אחת : הוצאה מזנב,
    הכנסה, או התקדמות של הקצה השמאלי :

    <div class="explorer" data-kind="slidemax" data-mode="b" data-nums="10 1 2 4 7 2" data-limit="5"></div>

---

### סעיף ג – בחומרה, המקסימום של K הדגימות האחרונות בכל מחזור

??? tip "רמז 1"
    בכל צעד של סעיף א לולאת ה-`while` מוציאה מספר משתנה של ערכים, מאפס ועד \( k - 1 \). בחומרה
    כל מחזור עושה כמות עבודה קבועה. אפשר לדעת **בבת אחת** אילו ערכים הלולאה הייתה מוציאה?

??? tip "רמז 2"
    הערכים ב-deque יורדים. לכן אלה שאינם גדולים מהדגימה החדשה הם רצף בסוף. השוו את הדגימה עם
    **כל** הכניסות במקביל, ומצאו איפה הרצף מתחיל. ובמקום מקום במערך, שמרו לכל כניסה את הגיל
    שלה.

<div class="selfcheck" data-answer="3" data-show="3 : ה-5 וה-3 קטנים מ-6 ויוצאים בהשוואה, וה-7 מגיע לגיל 3 = K ויוצא מהחלון" data-hint="לפני המחזור הכניסות הן 7 (גיל 2), ‏5 (גיל 1) ו-3 (גיל 0). אילו מהן אינן גדולות מ-6, ומה קורה לגיל של הראש?" markdown>
בזרם <span dir="ltr">9 7 5 3 6 2 8 1</span> עם \( K = 3 \), כמה כניסות יוצאות מהמבנה במחזור 4,
כשהדגימה 6 נכנסת?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏\( K \) כניסות, כל אחת ערך של \( W \) ביטים, גיל וביט valid, מהישנה לחדשה. בכל מחזור \( K \)
        משווים בודקים במקביל איזו כניסה גדולה מהדגימה החדשה \( x \). התוצאה היא רצף של אחדות
        ואחריו אפסים, ומקודד עדיפות מוצא את האפס הראשון \( p \) : שם נכתבת \( x \), והכניסות שאחריה
        מתבטלות. הראש יוצא כשהגיל שלו מגיע ל-\( K \), והמקסימום הוא הראש. עבודה קבועה בכל מחזור,
        ו-\( K \) כניסות הן גם המינימום במקרה הגרוע.

    <!-- cost: משווים \( K \) | פלופים \( O(K \cdot W) \) | השהיה \( O(\log W + \log K) \) -->

    #### הרעיון { .sol-idea }

    **מה אי אפשר להעתיק.** בכל צעד של סעיף א הלולאה מוציאה מהזנב מספר משתנה של ערכים. מעגל
    שמבצע לולאה כזו צריך מספר משתנה של מחזורים, או שרשרת של \( K \) השוואות אחת אחרי השנייה
    באותו מחזור, שהיא ארוכה מאוד. אבל אפשר לחשב את **התוצאה** של הלולאה בלי לולאה.

    **הכניסות.** המבנה מחזיק \( K \) כניסות, \( 0 \) עד \( K - 1 \), שהן ה-deque של סעיף א : כניסה 0
    היא הראש (הישנה והגדולה), ואחריה כניסות חדשות וקטנות יותר. לכל כניסה שלושה שדות :

    - **‏`val` :** הערך, \( W \) ביטים.
    - **‏`age` :** הגיל, כמה מחזורים עברו מאז שהדגימה נכנסה. הוא מחליף את "המקום במערך" של סעיף א :
      דגימה בחלון של \( K \) האחרונות אם הגיל שלה הוא לכל היותר \( K - 1 \).
    - **‏`vld` :** האם הכניסה בשימוש. הכניסות בשימוש הן תמיד רצף מההתחלה.

    **השוואה במקביל.** הלולאה של סעיף א מוציאה את כל הערכים שאינם גדולים מ-\( x \). הערכים בכניסות
    יורדים, ולכן הכניסות שנשארות הן רצף מההתחלה. מחשבים לכל כניסה, במקביל,
    \( \text{keep}[j] = \text{vld}[j] \land \text{val}[j] > x \), ומקבלים מסכה של אחדות ואחריהם אפסים
    (מסכת **מדחום**, thermometer). ‏**מקודד עדיפות** (priority encoder) מוצא את האפס הראשון,
    \( p \) : שם נכתבת \( x \), והכניסות שאחריה מתבטלות. זה בדיוק מה שהלולאה הייתה עושה, במחזור אחד.

    **הוצאה מהראש לפי גיל.** בכל מחזור הגיל של כל כניסה שנשארה עולה ב-1. כשהגיל של כניסה 0
    מגיע ל-\( K \), היא מחוץ לחלון, וכל הכניסות זזות מקום אחד לכיוון הראש. רק הראש יכול להגיע
    לגיל הזה, כי הגילים יורדים מהראש לזנב, ולכן במחזור יוצאת כך כניסה אחת לכל היותר.

    **כמה כניסות.** ‏\( K \) מספיקות, כי ה-deque של סעיף א אף פעם לא ארוך מהחלון. וזה גם המינימום :
    אחרי \( K \) דגימות יורדות ממש, \( a_1 > a_2 > \dots > a_K \), ודגימות קטנות מכולן, המוצא של
    המחזורים הבאים הוא \( a_1, a_2, \dots, a_K \) בזה אחר זה. לכן המצב אחרי \( a_K \) חייב לקבוע את
    כל \( K \) הערכים. יש \( \binom{2^W}{K} \) סדרות יורדות כאלה, וכדי להבדיל ביניהן צריך לפחות
    \( \log_2 \binom{2^W}{K} \ge K (W - \log_2 K) \) ביטים, כמעט \( K \) ערכים שלמים.

    המודול עם \( K = 3 \) : הכניסות, משווה לכל כניסה מול האפיק של \( x \), מקודד העדיפות, והלוגיקה
    של המצב הבא שנכנסת לרגיסטרים בעליית השעון :

    <!-- gen 4 -->

    <svg class="figure sm-fig sm-diag" viewBox="0 0 400 270" style="max-width:25rem" role="img" aria-label="המודול עם K = 3 : שלוש כניסות, משווה לכל כניסה מול הדגימה החדשה x, מקודד עדיפות שמוצא את המקום של x, ולוגיקת המצב הבא"><text class="sm-lab" x="90" y="14" text-anchor="middle">max_out = val[0]</text><line class="sm-wire" x1="90" y1="40" x2="90" y2="22"/><path class="sm-head" d="M86,27 L94,27 L90,20 Z"/><rect class="sm-reg" x="48.0" y="40" width="84" height="40" rx="4"><title>entry 0: a value and its age</title></rect><text class="sm-lab" x="90" y="56" text-anchor="middle">val[0]</text><text class="sm-lab" x="90" y="72" text-anchor="middle">age[0]</text><line class="sm-wire" x1="74" y1="80" x2="74" y2="114"/><path class="sm-head" d="M70,111 L78,111 L74,118 Z"/><line class="sm-wire" x1="106" y1="100" x2="106" y2="114"/><path class="sm-head" d="M102,111 L110,111 L106,118 Z"/><circle class="sm-tap" cx="106" cy="100" r="3"/><rect class="sm-cmpbox" x="54.0" y="118" width="72" height="26" rx="13"><title>comparator 0</title></rect><text class="sm-lab" x="90" y="135" text-anchor="middle">val[0] &gt; x</text><line class="sm-wire" x1="90" y1="144" x2="90" y2="172"/><path class="sm-head" d="M86,169 L94,169 L90,176 Z"/><text class="tick" x="95" y="162">keep[0]</text><rect class="sm-reg" x="148.0" y="40" width="84" height="40" rx="4"><title>entry 1: a value and its age</title></rect><text class="sm-lab" x="190" y="56" text-anchor="middle">val[1]</text><text class="sm-lab" x="190" y="72" text-anchor="middle">age[1]</text><line class="sm-wire" x1="174" y1="80" x2="174" y2="114"/><path class="sm-head" d="M170,111 L178,111 L174,118 Z"/><line class="sm-wire" x1="206" y1="100" x2="206" y2="114"/><path class="sm-head" d="M202,111 L210,111 L206,118 Z"/><circle class="sm-tap" cx="206" cy="100" r="3"/><rect class="sm-cmpbox" x="154.0" y="118" width="72" height="26" rx="13"><title>comparator 1</title></rect><text class="sm-lab" x="190" y="135" text-anchor="middle">val[1] &gt; x</text><line class="sm-wire" x1="190" y1="144" x2="190" y2="172"/><path class="sm-head" d="M186,169 L194,169 L190,176 Z"/><text class="tick" x="195" y="162">keep[1]</text><rect class="sm-reg" x="248.0" y="40" width="84" height="40" rx="4"><title>entry 2: a value and its age</title></rect><text class="sm-lab" x="290" y="56" text-anchor="middle">val[2]</text><text class="sm-lab" x="290" y="72" text-anchor="middle">age[2]</text><line class="sm-wire" x1="274" y1="80" x2="274" y2="114"/><path class="sm-head" d="M270,111 L278,111 L274,118 Z"/><line class="sm-wire" x1="306" y1="100" x2="306" y2="114"/><path class="sm-head" d="M302,111 L310,111 L306,118 Z"/><circle class="sm-tap" cx="306" cy="100" r="3"/><rect class="sm-cmpbox" x="254.0" y="118" width="72" height="26" rx="13"><title>comparator 2</title></rect><text class="sm-lab" x="290" y="135" text-anchor="middle">val[2] &gt; x</text><line class="sm-wire" x1="290" y1="144" x2="290" y2="172"/><path class="sm-head" d="M286,169 L294,169 L290,176 Z"/><text class="tick" x="295" y="162">keep[2]</text><line class="sm-bus" x1="60" y1="100" x2="386" y2="100"/><text class="sm-lab" x="388" y="94" text-anchor="end">x</text><rect class="sm-enc" x="30" y="176" width="360" height="28" rx="4"/><text class="sm-lab" x="210" y="194" text-anchor="middle">priority encoder: p = the first 0 of keep</text><line class="sm-wire" x1="190.0" y1="204" x2="190.0" y2="218"/><path class="sm-head" d="M186.0,215 L194.0,215 L190.0,222 Z"/><rect class="sm-enc" x="30" y="222" width="360" height="40" rx="4"/><text class="sm-lab" x="210" y="238" text-anchor="middle">next: j &lt; p kept (age + 1), slot p ← x</text><text class="sm-lab" x="210" y="254" text-anchor="middle">age[0] = K: shift to the front</text><path class="sm-wire" d="M30,242 H14 V60 H40.0"/><path class="sm-head" d="M41.0,56 L41.0,64 L48.0,60 Z"/><text class="tick" x="18" y="152" text-anchor="start">clk</text></svg>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **השוואה :** ‏\( K \) משווים בבת אחת, \( \text{keep}[j] = \text{vld}[j] \land \text{val}[j] > x \).
       המסכה היא אחדות ואחריהם אפסים.
    2. **המקום של x :** מקודד העדיפות נותן את \( p \), האפס הראשון של המסכה, או \( p = K \) אם כל
       הכניסות נשארות.
    3. **המצב הבא :** כניסה \( j < p \) נשארת והגיל שלה עולה ב-1. כניסה \( p \) מקבלת את \( x \) עם גיל 0.
       הכניסות שאחרי \( p \) מתבטלות.
    4. **יציאה לפי גיל :** אם הגיל של כניסה 0 הגיע ל-\( K \), כל הכניסות זוזות מקום אחד לכיוון הראש.
       כש-\( p = K \) זה תמיד קורה, ולכן מקום נוסף נחוץ רק בתוך הלוגיקה, לא ברגיסטרים.
    5. **המוצא :** אחרי עליית השעון, המוצא `max_out` הוא `val[0]`, הערך של הראש.

    </div>

    על הזרם <span dir="ltr">9 7 5 3 6 2 8 1</span> עם \( K = 3 \). כל כניסה כתובה כערך עם הגיל שלה
    מתחתיו, מכניסה 0 (משמאל), והמסכה `keep` מכניסה 0 :

    <!-- gen 5 -->

    | המחזור | ‏x | הכניסות לפני | ‏keep | המקום של x | יוצא בגיל K | הכניסות אחרי | ‏max_out |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏0 | ‏9 | ‏ריק | ‏<span dir="ltr">000</span> | ‏0 | אין | ‏<span dir="ltr">9<sub>0</sub></span> | **‏9** |
    | ‏1 | ‏7 | ‏<span dir="ltr">9<sub>0</sub></span> | ‏<span dir="ltr">100</span> | ‏1 | אין | ‏<span dir="ltr">9<sub>1</sub> 7<sub>0</sub></span> | **‏9** |
    | ‏2 | ‏5 | ‏<span dir="ltr">9<sub>1</sub> 7<sub>0</sub></span> | ‏<span dir="ltr">110</span> | ‏2 | אין | ‏<span dir="ltr">9<sub>2</sub> 7<sub>1</sub> 5<sub>0</sub></span> | **‏9** |
    | ‏3 | ‏3 | ‏<span dir="ltr">9<sub>2</sub> 7<sub>1</sub> 5<sub>0</sub></span> | ‏<span dir="ltr">111</span> | ‏3 | ‏9 | ‏<span dir="ltr">7<sub>2</sub> 5<sub>1</sub> 3<sub>0</sub></span> | **‏7** |
    | ‏4 | ‏6 | ‏<span dir="ltr">7<sub>2</sub> 5<sub>1</sub> 3<sub>0</sub></span> | ‏<span dir="ltr">100</span> | ‏1 | ‏7 | ‏<span dir="ltr">6<sub>0</sub></span> | **‏6** |
    | ‏5 | ‏2 | ‏<span dir="ltr">6<sub>0</sub></span> | ‏<span dir="ltr">100</span> | ‏1 | אין | ‏<span dir="ltr">6<sub>1</sub> 2<sub>0</sub></span> | **‏6** |
    | ‏6 | ‏8 | ‏<span dir="ltr">6<sub>1</sub> 2<sub>0</sub></span> | ‏<span dir="ltr">000</span> | ‏0 | אין | ‏<span dir="ltr">8<sub>0</sub></span> | **‏8** |
    | ‏7 | ‏1 | ‏<span dir="ltr">8<sub>0</sub></span> | ‏<span dir="ltr">100</span> | ‏1 | אין | ‏<span dir="ltr">8<sub>1</sub> 1<sub>0</sub></span> | **‏8** |

    <!-- /gen -->

    במחזור 3 כל שלוש הכניסות גדולות מ-3, המסכה `111` ו-\( p = 3 \) : ה-3 נכתב למקום הנוסף, וה-9, שמגיע
    לגיל 3, יוצא. במחזור 4 המסכה `100` : ה-6 נכתב לכניסה 1 ומבטל את ה-5 ואת ה-3 בבת אחת, וה-7
    יוצא לפי גיל, כך שנשאר רק ה-6. בסעיף א זה היה צעד עם שתי הוצאות מהזנב ואחת מהראש.

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module win_max" linenums="1" hl_lines="23 29 35 43"
        // the maximum of the last K samples, every cycle: K entries, front first, whose values
        // decrease from the front to the back (the deque of part a), each with its age
        module win_max #(
          parameter int K = 3,
          parameter int W = 8
        ) (
          input  logic         clk,
          input  logic         rst_n,
          input  logic [W-1:0] x,            // a new sample every cycle
          output logic [W-1:0] max_out       // the maximum of the last K samples
        );
          localparam int AW = $clog2(K + 1);
          logic [W-1:0]  val  [K];           // the entries, front first
          logic [AW-1:0] age  [K];           // cycles since the entry's sample came in
          logic [K-1:0]  vld;
          logic [K-1:0]  keep;               // val[j] > x: ones, then zeros
          logic [K:0]    kp;                 // keep[j - 1], and 1 for j = 0
          logic [W-1:0]  nval [K+1];         // the entries after x is written, one spare slot
          logic [AW-1:0] nage [K+1];
          logic [K:0]    nvld;
          logic          drop;               // the front reached age K
          always_comb begin
            for (int j = 0; j < K; j++) keep[j] = vld[j] && val[j] > x;           // (1)!
            kp = {keep, 1'b1};
            for (int j = 0; j < K; j++) begin
              if (keep[j]) begin                                                 // kept, one cycle older
                nval[j] = val[j]; nage[j] = age[j] + 1'b1; nvld[j] = 1'b1;
              end else if (kp[j]) begin
                nval[j] = x;      nage[j] = '0;            nvld[j] = 1'b1;       // (2)!
              end else begin
                nval[j] = '0;     nage[j] = '0;            nvld[j] = 1'b0;
              end
            end
            nval[K] = x; nage[K] = '0; nvld[K] = keep[K-1];                     // all K kept
            drop = nvld[0] && nage[0] == AW'(K);                                // (3)!
          end
          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin
              vld <= '0;
              for (int j = 0; j < K; j++) begin val[j] <= '0; age[j] <= '0; end
            end else begin
              for (int j = 0; j < K; j++) begin
                val[j] <= drop ? nval[j + 1] : nval[j];                          // (4)!
                age[j] <= drop ? nage[j + 1] : nage[j];
                vld[j] <= drop ? nvld[j + 1] : nvld[j];
              end
            end
          assign max_out = val[0];
        endmodule
        ```

        1. ‏\( K \) משווים של \( W \) ביטים, כולם באותו מחזור. ‏`keep` היא המסכה, אחדות ואחריהם אפסים.
        2. ‏`kp[j] && !keep[j]` הוא האפס הראשון של המסכה : היציאה של מקודד העדיפות, one-hot. שם נכתבת \( x \).
        3. הראש נשאר והגיע לגיל \( K \) : הוא כבר מחוץ לחלון. רק הראש יכול להגיע לגיל הזה.
        4. ההזזה לכיוון הראש : מרבב אחד לכל כניסה, בין המקום שלה למקום שאחריה.

    === "Python"
        ```python title="class WinMax" linenums="1" hl_lines="12 18 22"
        class WinMax:
            """The module win_max cycle by cycle: k entries, front first, each a value, its age
            and a valid bit; clock(x) is one rising edge and returns max_out after it."""

            def __init__(self, k: int):
                self.k = k
                self.slots = [(0, 0, False)] * k               # (value, age, valid)

            def clock(self, x: int) -> int:
                k, slots = self.k, self.slots
                # k comparators at once: the entries larger than x, ones then zeros
                keep = [ok and v > x for v, _, ok in slots]     # (1)!
                nxt = []
                for j, (v, age, ok) in enumerate(slots):
                    if keep[j]:
                        nxt.append((v, age + 1, True))          # kept, one cycle older
                    elif j == 0 or keep[j - 1]:
                        nxt.append((x, 0, True))                # (2)!
                    else:
                        nxt.append((0, 0, False))
                nxt.append((x, 0, keep[-1]))                    # all k kept: the spare slot
                drop = nxt[0][2] and nxt[0][1] == k             # (3)!
                self.slots = nxt[1:] if drop else nxt[:k]
                return self.slots[0][0]


        def win_max_run(samples: list[int], k: int) -> list[int]:
            """max_out after every sample, one sample a cycle."""
            hw = WinMax(k)
            return [hw.clock(x) for x in samples]
        ```

        1. המשווים של המודול. ‏`keep` היא המסכה, אחדות ואחריהם אפסים.
        2. האפס הראשון של המסכה, היציאה של מקודד העדיפות : שם נכתבת \( x \) עם גיל 0.
        3. הראש נשאר והגיע לגיל \( k \) : כל הכניסות זזות מקום אחד לכיוון הראש.

    #### למה זה נכון { .sol-proof }

    **הכניסות הן ה-deque של סעיף א.** נקרא לדגימה של המחזור \( t \) "המקום \( t \)". הטענה : אחרי
    המחזור \( t \), הכניסות בשימוש הן, לפי הסדר, ה-deque של סעיף א אחרי הצעד \( i = t \), וכניסה
    שהערך שלה מהמקום \( j \) מחזיקה גיל \( t - j \). באינדוקציה, עם השמורה של סעיף א :

    - **השוואה והמקום של x :** הערכים בכניסות יורדים, ולכן המסכה היא אחדות ואחריהם אפסים, והכניסות
      שמתבטלות הן בדיוק אלה שהלולאה של סעיף א הייתה מוציאה מהזנב. \( x \) נכתבת אחריהן, כמו
      `push_back`.
    - **יציאה לפי גיל :** בסעיף א הראש יוצא כשהמקום שלו הוא \( i - k \), כלומר כשהגיל שלו אחרי המחזור
      הוא \( K \). אם \( x \) גדולה ממנו, הוא מתבטל כבר בהשוואה. אחרת הוא נשאר, הגיל שלו מגיע ל-\( K \),
      והמודול מוציא אותו. אותה תוצאה, אף שהסדר הפוך מסעיף א.
    - **אין גלישה :** ‏\( p = K \) רק כשכל \( K \) הכניסות נשארות. הגילים שלהן שונים זה מזה ולכל היותר
      \( K - 1 \), ולכן הם בדיוק \( 0, \dots, K - 1 \), והראש מגיע לגיל \( K \) ויוצא. המקום הנוסף \( K \)
      חוזר למקום \( K - 1 \).

    לכן \( \text{val}[0] \), הראש, הוא המקסימום של \( K \) הדגימות האחרונות, לפי סעיף א.

    #### סיבוכיות { .sol-cost }

    - **אחסון :** ‏\( K \) כניסות של \( W + \lceil \log_2 (K + 1) \rceil + 1 \) ביטים. לפי החסם שלמעלה
      אי אפשר הרבה פחות.
    - **לוגיקה :** ‏\( K \) משווים של \( W \) ביטים, זיהוי של האפס הראשון במסכה (\( K \) שערי AND, כי
      המסכה היא מדחום), ושני מרבבים לכל כניסה.
    - **השהיה :** משווה (\( O(\log W) \)), ואחריו המקודד והמרבבים (\( O(\log K) \)), בלי קשר לכמה
      כניסות מתבטלות. ההשוואה עם הדרך הישירה : אוגר הזזה של \( K \) הדגימות ועץ של \( K - 1 \) משווים
      דורשים אותו אחסון, אבל \( \lceil \log_2 K \rceil \) משווים בשרשרת, או צנרת עם השהיה של כמה
      מחזורים.

    **נסו בעצמכם.** כל מחזור הוא שני צעדים : ההשוואה (המסכה, המקום של \( x \) והכניסה שמגיעה לגיל
    \( K \)) ועליית השעון (המצב החדש והמוצא) :

    <div class="explorer" data-kind="slidemax" data-mode="c" data-nums="9 7 5 3 6 2 8 1" data-k="3"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להוציא מהראש לפי ערך ולא לפי מקום"
    יש מי ששומרים ב-deque ערכים, ומוציאים את הראש כשהוא שווה לערך שיוצא מהחלון,
    \( \text{nums}[i - k] \). עם ערכים שווים זה שובר את הקוד : ב-<span dir="ltr">5 5 1</span> עם
    \( k = 2 \), ה-5 השני מוציא את הראשון מהזנב (`<=`), ובצעד הבא ה-5 שיוצא מהחלון "נמצא" בראש
    ומוציא את ה-5 שעדיין בחלון. מתקבל <span dir="ltr">5 1</span> במקום <span dir="ltr">5 5</span>.
    שומרים מקומות, ואז אין שאלה מי יוצא.

??? trap "מלכודת : ‏`<=` מול `<` כשיש ערכים שווים"
    עם מקומות שני הסימנים נכונים : `<=` נותן deque שיורד ממש וקצר יותר, ו-`<` שומר עותקים של
    ערך שווה. הטעות היא לערבב : לשמור ערכים ולהוציא את השווים (המלכודת הקודמת), או בסעיף ב
    להעתיק את הניקוי של `hi` אל `lo` בלי להפוך את הסימן, ואז גם `lo` מחזיק מקסימום. בודקים על מערך של ערכים שווים, ועל
    מערך יורד ועולה.

??? trap "מלכודת : לחשב את המקסימום של כל חלון מחדש"
    ‏`max(nums[i:i + k])` לכל חלון נכון, אבל \( O(n \cdot k) \) : עם \( n = 10^6 \) ו-\( k = 10^3 \) זה
    מיליארד השוואות. ה-deque עושה לכל היותר \( 2n \) פעולות, בלי קשר ל-\( k \).

??? trap "מלכודת : בסעיף ב להזיז את left צעד אחד ולא בלולאה"
    עם `if` במקום `while` הקצה השמאלי זז לכל היותר מקום אחד בכל צעד, והחלון יכול להישאר לא
    חוקי. ב-<span dir="ltr">1 2 3 10</span> עם \( \text{limit} = 2 \), בצעד 3 החלון צריך לקפוץ
    ל-3..3, ועם `if` הוא נשאר 1..3, ‏<span dir="ltr">2 3 10</span> עם הפרש 8. במקרה,
    האורך שנרשם בסוף עדיין נכון (זה הטריק של "חלון שלא מתקצר" משאלה 0061), אבל כל דבר אחר
    שקוראים מהחלון שגוי : המקום שלו, ההפרש שלו, ומוניטור שמדווח על חלון לא חוקי. ההוכחה של
    הקוד היא על `while`.

??? trap "מלכודת : בסעיף ג להניח שהלולאה של ה-deque היא מחזור אחד"
    ‏`while` בתוך `always_comb` לא מסונתז, ו-`for` של \( K \) איטרציות עם `break` נפרש לשרשרת של
    \( K \) השוואות בטור באותו מחזור. ההבחנה שהופכת את זה למעגל היא שהכניסות שמתבטלות הן רצף
    בסוף, ולכן אפשר להשוות את כולן במקביל ולמצוא את הגבול במקודד עדיפות.

??? followup "שאלות המשך"
    - **המקסימום והמינימום יחד :** איך מחזירים בכל חלון גם את המינימום, בתוכנה ובחומרה?

        ??? fu-answer "תשובה"
            שני deques, כמו בסעיף ב : אחד שהערכים בו יורדים ואחד שהם עולים, בזמן \( O(n) \). בחומרה
            שני מבנים של \( K \) כניסות, עם \( 2K \) משווים, ו-max − min הוא חיסור אחד של שני הראשים.

    - **בלי deque, ‏van Herk / Gil-Werman :** אפשר מקסימום של כל חלון במספר קבוע של השוואות לכל
      ערך, בלי קשר ל-\( k \) ובלי לולאה משתנה?

        ??? fu-answer "תשובה"
            כן. מחלקים לבלוקים של \( k \), ומחשבים בכל בלוק מקסימום מתחילתו (prefix) ומקסימום עד סופו
            (suffix). חלון שמתחיל ב-\( i \) חוצה לכל היותר שני בלוקים, והמקסימום שלו הוא
            \( \max(\text{suffix}[i], \text{prefix}[i + k - 1]) \). בערך שלוש השוואות לכל ערך, ובחומרה מעט
            משווים, במחיר של אחסון של שני בלוקים והשהיה של בלוק.

    - **הסכום או הממוצע של החלון :** מה משתנה, ולמה המקסימום קשה יותר?

        ??? fu-answer "תשובה"
            סכום נע הוא מונה אחד : מוסיפים את הערך שנכנס ומחסירים את הערך שיוצא (צריך לזכור את \( k \)
            הערכים, באוגר הזזה או ב-FIFO). למקסימום אין פעולה הפוכה : כשהערך שיוצא הוא המקסימום, אי
            אפשר "להחסיר" אותו ולקבל את הבא. לכן צריך את המועמדים, ה-deque.

    - **חלון דו-ממדי :** המקסימום של כל ריבוע \( k \times k \) בתמונה או במטריצה בגודל \( n \times m \).

        ??? fu-answer "תשובה"
            קודם המקסימום הנע בגודל \( k \) על כל שורה, ואחר כך על כל עמודה של התוצאה. המקסימום של
            ריבוע הוא המקסימום של המקסימומים של השורות שלו. הזמן \( O(n \cdot m) \), בלי קשר ל-\( k \).
