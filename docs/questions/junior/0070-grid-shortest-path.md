---
id: 70
title: המסלול הקצר ביותר בלוח – BFS, שבירת עד k קירות, ועלות כניסה לכל תא
level: junior
difficulty: medium
kind: code
tags: [algorithms, bfs, dijkstra, python, systemverilog]
source: "שאלה קלאסית (Shortest Path in Binary Matrix, LeetCode 1091); סעיף ב הוא LeetCode 1293, וסעיף ג מכליל ל-Dijkstra על לוח"
added: 2026-10-29
---

## השאלה

נתון לוח של \( R \) שורות ו-\( C \) עמודות. כל תא הוא `0` (פתוח) או `1` (קיר), ובלוח יש תא
התחלה \( S \) ותא יעד \( T \), שניהם פתוחים. תא נכתב כ-(שורה, עמודה), והשורה 0 היא העליונה.
**צעד** הוא מעבר מתא לתא שכן. **כמה צעדים יש במסלול הקצר ביותר מ-\( S \) ל-\( T \)?** אם אין
מסלול, החזירו <span dir="ltr">−1</span>.

בכל הסעיפים יש מתג של **ארבעה או שמונה כיוונים**. ארבעה כיוונים : למעלה, למטה, שמאלה וימינה,
וזה המקרה העיקרי. שמונה כיוונים : גם ארבעת האלכסונים, וצעד באלכסון הוא צעד אחד כמו כל צעד אחר.
**הכלל של האלכסון :** אסור לעבור באלכסון בין שני קירות שנוגעים זה בזה בפינה. כלומר, צעד מ-\( (r, c) \)
ל-\( (r + 1, c + 1) \) אסור כששני התאים שהוא חולף על פניהם, \( (r, c + 1) \) ו-\( (r + 1, c) \), הם
קירות ; אם רק אחד מהם קיר, הצעד מותר. הכלל האחר, שמתיר גם את המעבר הזה, הוא שאלת המשך.

הדוגמה של סעיפים א ו-ב, לוח של 7 שורות ו-9 עמודות, \( S = (3, 0) \) ו-\( T = (3, 8) \) :

```text
0 0 1 0 1 0 0 0 0
0 0 1 0 0 1 0 1 0
0 0 1 0 1 0 0 1 0
S 0 1 0 0 1 0 1 T
0 0 1 0 1 0 0 1 0
0 0 1 0 0 1 0 1 0
0 0 0 0 0 0 0 1 0
```

שלושה קירות עומדים בדרך : עמודה 2 פתוחה רק למטה, קיר זיגזג בעמודות 4 ו-5 פתוח רק למטה,
ועמודה 7 פתוחה רק למעלה. התשובה עם ארבעה כיוונים היא 20, ועם שמונה 15.

**ההקשר באימות :** ב-NoC בצורת רשת (mesh) כל תא הוא נתב, וקיר הוא נתב כבוי או אזור שהחבילות
לא עוברות בו. מודל הייחוס של סביבת האימות צריך לדעת כמה hops לפחות יש בין שני נתבים, כדי לבדוק
את ה-latency של כל חבילה ולתפוס ניתוב שמבזבז צעדים ; ובבדיקת routing עם תקלות הוא צריך לדעת
אם יעד בכלל ניתן להשגה, ולהחזיר <span dir="ltr">−1</span> כשלא. רשת עם קישורים אלכסוניים היא
המתג של שמונה הכיוונים.

- **סעיף א – הלוח הקלאסי :** מצאו את מספר הצעדים במסלול הקצר ביותר, או <span dir="ltr">−1</span>,
  והחזירו גם את המסלול עצמו, תא אחרי תא.
- **סעיף ב – מותר לשבור עד \( k \) קירות :** אפשר להיכנס לתא של קיר, אבל כל כניסה כזו "שוברת" אותו
  ומנצלת אחת מ-\( k \) שבירות. מה המסלול הקצר ביותר עכשיו? (LeetCode 1293.) בדוגמה עם
  \( k = 1 \) התשובה 14.
- **סעיף ג – עלות כניסה לכל תא :** אין יותר `0` ו-`1`. בכל תא עלות כניסה מ-1 עד 9, כמו שטח :
  כביש 1, בוץ 5, הר 9, ו-`#` הוא קיר. העלות של מסלול היא סכום העלויות של התאים **שנכנסים**
  אליהם, ולכן העלות של \( S \) עצמו לא משולמת והעלות של \( T \) כן. מצאו את העלות הקטנה ביותר.

??? interviewer "מה המראיין בודק"
    - **מהלוח לגרף :** האם המועמד רואה שתא הוא צומת וצעד הוא קשת, ושמסלול קצר בגרף בלי משקלים
      הוא BFS, ולא חיפוש לעומק או ניסיון של כל המסלולים.
    - **למה BFS נכון :** האם הוא יודע להסביר שהתאים יוצאים מהתור לפי המרחק, ולא רק "ככה עושים".
    - **המצב הנכון :** בסעיף ב, האם הוא מבין שהתא לבדו אינו מספיק כדי לתאר איפה החיפוש נמצא,
      ומה בדיוק צריך להוסיף למצב.
    - **מתי BFS לא מספיק :** בסעיף ג, האם הוא מזהה שעלויות שונות דורשות תור עדיפויות, ויודע מה
      משתנה בהוכחה.
    - **פרטים :** גבולות הלוח, הכלל של האלכסון, מתי מסמנים תא, וההבדל בין "צעדים" ל"עלות".

---

### סעיף א – הלוח הקלאסי : BFS

??? tip "רמז 1"
    חשבו על כל תא פתוח כעל צומת, ועל כל צעד כעל קשת. איזה חיפוש מוצא קודם את כל התאים במרחק 1,
    אחר כך את כל התאים במרחק 2, וכן הלאה?

??? tip "רמז 2"
    תור (FIFO) : מכניסים את \( S \) עם המרחק 0. בכל פעם מוציאים תא, ולכל שכן פתוח שעוד אין לו
    מרחק כותבים את המרחק של התא ועוד 1, ומכניסים אותו לזנב התור. כדי לבנות את המסלול עצמו,
    רושמים לכל תא **מאיזה תא** הגיעו אליו.

<div class="selfcheck" data-answer="9" data-show="9 : מ-(3, 0) למעלה ל-(2, 0), ימינה לאורך שורה 2 עד (2, 3), למעלה דרך (1, 3) ל-(0, 3), ושמאלה לאורך שורה 0 עד (0, 0)" data-hint="שורה 1 חסומה חוץ מהעמודה האחרונה, ולכן צריך לעבור אותה בעמודה 3. ספרו את הצעדים בשורה 2, בעמודה 3 ובשורה 0." markdown>
בלוח <span dir="ltr">0000 / 1110 / 0000 / 0111</span> (ארבע שורות, השורה העליונה ראשונה), עם
ארבעה כיוונים, \( S = (3, 0) \) ו-\( T = (0, 0) \). כמה צעדים במסלול הקצר ביותר?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏**BFS** מ-\( S \) על התאים הפתוחים : תור של תאים, וכל תא מקבל את המרחק שלו, המרחק של
        התא שממנו הגיעו ועוד 1, בפעם הראשונה שמגיעים אליו, ואת ה**הורה** שלו, התא שממנו הגיעו.
        כש-\( T \) יוצא מהתור המרחק שלו הוא התשובה, והמסלול נבנה מהסוף להתחלה דרך ההורים. בדוגמה :
        20 צעדים עם ארבעה כיוונים, 15 עם שמונה.

    <!-- cost: זמן \( O(RC) \) | זיכרון \( O(RC) \) -->

    #### הרעיון { .sol-idea }

    **מונחים.** ‏**שכן** של תא הוא תא שאפשר להגיע אליו בצעד אחד : אחד מארבעת התאים שנוגעים בו
    בצלע, ועם שמונה כיוונים גם אחד מארבעת התאים שנוגעים בו בפינה (כל עוד הצעד אינו עובר בין שני
    קירות). **המרחק** של תא הוא מספר הצעדים במסלול הקצר ביותר מ-\( S \) אליו. בשפה של גרפים, הלוח
    הוא גרף שהצמתים שלו הם התאים הפתוחים, ובין שני שכנים יש קשת ; לכל הקשתות אותו "מחיר", צעד
    אחד. **גרף בלי משקלים** כזה הוא בדיוק המקרה של BFS.

    **‏BFS (breadth-first search, חיפוש לרוחב).** מבקרים בתאים **בשכבות** לפי המרחק : קודם \( S \)
    (מרחק 0), אחר כך כל התאים במרחק 1, אחר כך במרחק 2, וכן הלאה, כמו גל שמתפשט מ-\( S \). הכלי
    הוא **תור** (queue, FIFO : מה שנכנס ראשון יוצא ראשון). מכניסים את \( S \), ובלולאה מוציאים את
    התא שבראש התור ובודקים את השכנים שלו : שכן פתוח שעוד אין לו מרחק מקבל את המרחק של התא ועוד 1
    ונכנס לזנב התור. שכן שכבר יש לו מרחק לא נוגעים בו, כי הגיעו אליו מוקדם יותר או באותו מרחק.
    מערך `dist` של מרחקים, עם <span dir="ltr">−1</span> לתא שעוד לא הגיעו אליו, הוא גם הסימון של
    "כבר ראינו את התא", כמו `seen` בהצפה של [0065](0065-number-of-islands.md).

    **למה BFS ולא חיפוש לעומק.** חיפוש לעומק (DFS) הולך עד הסוף בכיוון אחד, ולכן הפעם הראשונה
    שהוא מגיע לתא היא לא בהכרח הדרך הקצרה ; כדי למצוא את הקצר ביותר הוא היה צריך לנסות את כל
    המסלולים, ומספרם מעריכי. ‏BFS מגיע לכל תא **קודם** בדרך הקצרה ביותר, ולכן מספיק לבקר בכל תא
    פעם אחת.

    **המסלול עצמו.** המרחק לבדו לא אומר איך הולכים. לכן כשתא מקבל מרחק רושמים גם את ה**הורה** שלו,
    התא שממנו הגיעו, במערך `parent`. ההורים יוצרים עץ שהשורש שלו \( S \) (**עץ ה-BFS**), ובו
    הדרך מכל תא לשורש היא מסלול קצר ביותר. בסוף הולכים מ-\( T \) להורה שלו, להורה של ההורה, וכן
    הלאה עד \( S \), והופכים את הרשימה.

    הדוגמה עם ארבעה כיוונים. בכל תא המרחק שלו מ-\( S \), והמסלול שנבנה מההורים. המסלול יורד לפתח
    של עמודה 2, ממשיך בשורה התחתונה מתחת לקיר הזיגזג, עולה בעמודה 6 עד השורה העליונה, עובר את
    עמודה 7 בפתח שלה, ויורד ל-\( T \) :

    <!-- gen 0 -->

    <svg class="figure gx-fig" viewBox="0 0 336 266" style="max-width:21rem" role="img" aria-label="הדוגמה : לוח 7 על 9 עם שלושה קירות, ההתחלה S משמאל והיעד T מימין ; בכל תא המרחק שלו מ-S ב-BFS של ארבעה כיוונים, והמסלול הקצר מסומן"><text class="tick" x="41" y="14" text-anchor="middle">0</text><text class="tick" x="75" y="14" text-anchor="middle">1</text><text class="tick" x="109" y="14" text-anchor="middle">2</text><text class="tick" x="143" y="14" text-anchor="middle">3</text><text class="tick" x="177" y="14" text-anchor="middle">4</text><text class="tick" x="211" y="14" text-anchor="middle">5</text><text class="tick" x="245" y="14" text-anchor="middle">6</text><text class="tick" x="279" y="14" text-anchor="middle">7</text><text class="tick" x="313" y="14" text-anchor="middle">8</text><text class="tick" x="17" y="43" text-anchor="end">0</text><text class="tick" x="17" y="77" text-anchor="end">1</text><text class="tick" x="17" y="111" text-anchor="end">2</text><text class="tick" x="17" y="145" text-anchor="end">3</text><text class="tick" x="17" y="179" text-anchor="end">4</text><text class="tick" x="17" y="213" text-anchor="end">5</text><text class="tick" x="17" y="247" text-anchor="end">6</text><g class="gx-cell is-open is-seen"><title>cell (0, 0): open, distance 3</title><rect x="25.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 1): open, distance 4</title><rect x="59.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (0, 2): wall</title><rect x="93.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 3): open, distance 12</title><rect x="127.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (0, 4): wall</title><rect x="161.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 5): open, distance 16</title><rect x="195.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 6): open, distance 15</title><rect x="229.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 7): open, distance 16</title><rect x="263.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 8): open, distance 17</title><rect x="297.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 0): open, distance 2</title><rect x="25.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 1): open, distance 3</title><rect x="59.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 2): wall</title><rect x="93.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 3): open, distance 11</title><rect x="127.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 4): open, distance 12</title><rect x="161.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 5): wall</title><rect x="195.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 6): open, distance 14</title><rect x="229.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 7): wall</title><rect x="263.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 8): open, distance 18</title><rect x="297.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 0): open, distance 1</title><rect x="25.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 1): open, distance 2</title><rect x="59.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 2): wall</title><rect x="93.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 3): open, distance 10</title><rect x="127.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 4): wall</title><rect x="161.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 5): open, distance 14</title><rect x="195.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 6): open, distance 13</title><rect x="229.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 7): wall</title><rect x="263.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 8): open, distance 19</title><rect x="297.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 0): open, distance 0, the start</title><rect x="25.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 1): open, distance 1</title><rect x="59.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (3, 2): wall</title><rect x="93.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 3): open, distance 9</title><rect x="127.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 4): open, distance 10</title><rect x="161.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (3, 5): wall</title><rect x="195.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 6): open, distance 12</title><rect x="229.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (3, 7): wall</title><rect x="263.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 8): open, distance 20, the target</title><rect x="297.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (4, 0): open, distance 1</title><rect x="25.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (4, 1): open, distance 2</title><rect x="59.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (4, 2): wall</title><rect x="93.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (4, 3): open, distance 8</title><rect x="127.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (4, 4): wall</title><rect x="161.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (4, 5): open, distance 12</title><rect x="195.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (4, 6): open, distance 11</title><rect x="229.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (4, 7): wall</title><rect x="263.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (4, 8): open</title><rect x="297.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (5, 0): open, distance 2</title><rect x="25.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (5, 1): open, distance 3</title><rect x="59.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (5, 2): wall</title><rect x="93.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (5, 3): open, distance 7</title><rect x="127.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (5, 4): open, distance 8</title><rect x="161.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (5, 5): wall</title><rect x="195.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (5, 6): open, distance 10</title><rect x="229.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (5, 7): wall</title><rect x="263.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (5, 8): open</title><rect x="297.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 0): open, distance 3</title><rect x="25.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 1): open, distance 4</title><rect x="59.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 2): open, distance 5</title><rect x="93.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 3): open, distance 6</title><rect x="127.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 4): open, distance 7</title><rect x="161.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 5): open, distance 8</title><rect x="195.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 6): open, distance 9</title><rect x="229.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (6, 7): wall</title><rect x="263.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (6, 8): open</title><rect x="297.5" y="227.5" width="31" height="31" rx="3"/></g><polyline class="gx-path" points="41,141 41,175 41,209 41,243 75,243 109,243 143,243 177,243 211,243 245,243 245,209 245,175 245,141 245,107 245,73 245,39 279,39 313,39 313,73 313,107 313,141"><title>the path: 20 steps</title></polyline><text class="gx-val" x="41" y="44" text-anchor="middle">3</text><text class="gx-val" x="75" y="44" text-anchor="middle">4</text><text class="gx-val" x="143" y="44" text-anchor="middle">12</text><text class="gx-val" x="211" y="44" text-anchor="middle">16</text><text class="gx-val" x="245" y="44" text-anchor="middle">15</text><text class="gx-val" x="279" y="44" text-anchor="middle">16</text><text class="gx-val" x="313" y="44" text-anchor="middle">17</text><text class="gx-val" x="41" y="78" text-anchor="middle">2</text><text class="gx-val" x="75" y="78" text-anchor="middle">3</text><text class="gx-val" x="143" y="78" text-anchor="middle">11</text><text class="gx-val" x="177" y="78" text-anchor="middle">12</text><text class="gx-val" x="245" y="78" text-anchor="middle">14</text><text class="gx-val" x="313" y="78" text-anchor="middle">18</text><text class="gx-val" x="41" y="112" text-anchor="middle">1</text><text class="gx-val" x="75" y="112" text-anchor="middle">2</text><text class="gx-val" x="143" y="112" text-anchor="middle">10</text><text class="gx-val" x="211" y="112" text-anchor="middle">14</text><text class="gx-val" x="245" y="112" text-anchor="middle">13</text><text class="gx-val" x="313" y="112" text-anchor="middle">19</text><text class="gx-tag" x="28" y="136">S</text><text class="gx-val" x="41" y="149" text-anchor="middle">0</text><text class="gx-val" x="75" y="146" text-anchor="middle">1</text><text class="gx-val" x="143" y="146" text-anchor="middle">9</text><text class="gx-val" x="177" y="146" text-anchor="middle">10</text><text class="gx-val" x="245" y="146" text-anchor="middle">12</text><text class="gx-tag" x="300" y="136">T</text><text class="gx-val" x="313" y="149" text-anchor="middle">20</text><text class="gx-val" x="41" y="180" text-anchor="middle">1</text><text class="gx-val" x="75" y="180" text-anchor="middle">2</text><text class="gx-val" x="143" y="180" text-anchor="middle">8</text><text class="gx-val" x="211" y="180" text-anchor="middle">12</text><text class="gx-val" x="245" y="180" text-anchor="middle">11</text><text class="gx-val" x="41" y="214" text-anchor="middle">2</text><text class="gx-val" x="75" y="214" text-anchor="middle">3</text><text class="gx-val" x="143" y="214" text-anchor="middle">7</text><text class="gx-val" x="177" y="214" text-anchor="middle">8</text><text class="gx-val" x="245" y="214" text-anchor="middle">10</text><text class="gx-val" x="41" y="248" text-anchor="middle">3</text><text class="gx-val" x="75" y="248" text-anchor="middle">4</text><text class="gx-val" x="109" y="248" text-anchor="middle">5</text><text class="gx-val" x="143" y="248" text-anchor="middle">6</text><text class="gx-val" x="177" y="248" text-anchor="middle">7</text><text class="gx-val" x="211" y="248" text-anchor="middle">8</text><text class="gx-val" x="245" y="248" text-anchor="middle">9</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="gx-key-s"></i>S ההתחלה, T היעד</span><span><i class="gx-key is-open"></i>תא פתוח</span><span><i class="gx-key is-wall"></i>קיר</span><span><i class="gx-key-path"></i>המסלול</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מתחילים מ-\( S \) :** ‏`dist` של \( S \) הוא 0, ושל כל שאר התאים <span dir="ltr">−1</span>.
       התור מחזיק את \( S \).
    2. **מוציאים מראש התור :** את התא \( (r, c) \). אם הוא \( T \), מסיימים : המרחק שלו הוא התשובה.
    3. **בודקים את השכנים :** לכל שכן \( (a, b) \) בתוך הלוח, בסדר קבוע (למעלה, למטה, שמאלה, ימינה,
       ועם שמונה כיוונים אחר כך האלכסונים) : אם הוא פתוח ועוד אין לו מרחק,
       \( \text{dist}[a][b] = \text{dist}[r][c] + 1 \), ההורה שלו \( (r, c) \), והוא נכנס לזנב
       התור. קיר, או תא שכבר יש לו מרחק : לא עושים כלום.
    4. **תור ריק :** אם התור התרוקן לפני ש-\( T \) יצא ממנו, אין מסלול : <span dir="ltr">−1</span>.
    5. **המסלול :** מ-\( T \) הולכים להורה עד \( S \), והופכים.

    </div>

    על הדוגמה. ‏BFS מוציא את התאים לפי המרחק, ולכן אפשר לכתוב את הריצה כשכבות : בכל שורה מרחק
    אחד, והתאים שקיבלו אותו, בסדר שבו נכנסו לתור. הגל מתפשט קודם בשתי העמודות שמשמאל לקיר,
    עובר את עמודה 2 בשורה 6 (מרחק 5), מתפצל לשני צדי הזיגזג, וממשיך עד \( T \) במרחק 20 :

    <!-- gen 2 -->

    | המרחק | התאים במרחק הזה, בסדר הכניסה לתור | כמה |
    |:-:|:--|:-:|
    | ‏0 | ‏<span dir="ltr">(3,0)</span> | ‏1 |
    | ‏1 | ‏<span dir="ltr">(2,0) (4,0) (3,1)</span> | ‏3 |
    | ‏2 | ‏<span dir="ltr">(1,0) (2,1) (5,0) (4,1)</span> | ‏4 |
    | ‏3 | ‏<span dir="ltr">(0,0) (1,1) (6,0) (5,1)</span> | ‏4 |
    | ‏4 | ‏<span dir="ltr">(0,1) (6,1)</span> | ‏2 |
    | ‏5 | ‏<span dir="ltr">(6,2)</span> | ‏1 |
    | ‏6 | ‏<span dir="ltr">(6,3)</span> | ‏1 |
    | ‏7 | ‏<span dir="ltr">(5,3) (6,4)</span> | ‏2 |
    | ‏8 | ‏<span dir="ltr">(4,3) (5,4) (6,5)</span> | ‏3 |
    | ‏9 | ‏<span dir="ltr">(3,3) (6,6)</span> | ‏2 |
    | ‏10 | ‏<span dir="ltr">(2,3) (3,4) (5,6)</span> | ‏3 |
    | ‏11 | ‏<span dir="ltr">(1,3) (4,6)</span> | ‏2 |
    | ‏12 | ‏<span dir="ltr">(0,3) (1,4) (3,6) (4,5)</span> | ‏4 |
    | ‏13 | ‏<span dir="ltr">(2,6)</span> | ‏1 |
    | ‏14 | ‏<span dir="ltr">(1,6) (2,5)</span> | ‏2 |
    | ‏15 | ‏<span dir="ltr">(0,6)</span> | ‏1 |
    | ‏16 | ‏<span dir="ltr">(0,5) (0,7)</span> | ‏2 |
    | ‏17 | ‏<span dir="ltr">(0,8)</span> | ‏1 |
    | ‏18 | ‏<span dir="ltr">(1,8)</span> | ‏1 |
    | ‏19 | ‏<span dir="ltr">(2,8)</span> | ‏1 |
    | ‏20 | ‏<span dir="ltr">(3,8)</span> (**T**) | ‏1 |

    <!-- /gen -->

    מכאן המסלול : ההורה של \( (3, 8) \) הוא \( (2, 8) \), שלו \( (1, 8) \), וכן הלאה אחורה עד
    \( S \), 21 תאים ו-20 צעדים. בשכבה 12 נכנסים ארבעה תאים משני הצדדים של הזיגזג : ‏\( (0, 3) \) ו-\( (1, 4) \) משמאלו,
    ו-\( (3, 6) \) ו-\( (4, 5) \) מימינו, אחרי שהגל עקף אותו מלמטה. הלולאה הוציאה 42 תאים עד
    ש-\( T \) יצא.

    **ומה משתנה בשמונה כיוונים.** רק רשימת השכנים : ארבעה אלכסונים נוספים, והבדיקה של הכלל.
    בלוח של הדוגמה המסלול יורד באלכסון לפתח של עמודה 2, עולה בעמודה 6 וחוצה את עמודה 7
    בפינה : 15 צעדים. האיקסים מסמנים חמישה אלכסונים שעוברים בין שני קירות של הזיגזג ; הכלל אוסר אותם,
    ולכן הזיגזג נשאר קיר גם בשמונה כיוונים :

    <!-- gen 3 -->

    <svg class="figure gx-fig" viewBox="0 0 336 266" style="max-width:21rem" role="img" aria-label="אותו לוח עם שמונה כיוונים : המרחקים והמסלול הקצר, והאלכסונים בין שני קירות מסומנים באיקס"><text class="tick" x="41" y="14" text-anchor="middle">0</text><text class="tick" x="75" y="14" text-anchor="middle">1</text><text class="tick" x="109" y="14" text-anchor="middle">2</text><text class="tick" x="143" y="14" text-anchor="middle">3</text><text class="tick" x="177" y="14" text-anchor="middle">4</text><text class="tick" x="211" y="14" text-anchor="middle">5</text><text class="tick" x="245" y="14" text-anchor="middle">6</text><text class="tick" x="279" y="14" text-anchor="middle">7</text><text class="tick" x="313" y="14" text-anchor="middle">8</text><text class="tick" x="17" y="43" text-anchor="end">0</text><text class="tick" x="17" y="77" text-anchor="end">1</text><text class="tick" x="17" y="111" text-anchor="end">2</text><text class="tick" x="17" y="145" text-anchor="end">3</text><text class="tick" x="17" y="179" text-anchor="end">4</text><text class="tick" x="17" y="213" text-anchor="end">5</text><text class="tick" x="17" y="247" text-anchor="end">6</text><g class="gx-cell is-open is-seen"><title>cell (0, 0): open, distance 3</title><rect x="25.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 1): open, distance 3</title><rect x="59.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (0, 2): wall</title><rect x="93.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 3): open, distance 9</title><rect x="127.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (0, 4): wall</title><rect x="161.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 5): open, distance 12</title><rect x="195.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 6): open, distance 12</title><rect x="229.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 7): open, distance 12</title><rect x="263.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (0, 8): open, distance 13</title><rect x="297.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 0): open, distance 2</title><rect x="25.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 1): open, distance 2</title><rect x="59.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 2): wall</title><rect x="93.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 3): open, distance 8</title><rect x="127.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 4): open, distance 8</title><rect x="161.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 5): wall</title><rect x="195.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 6): open, distance 11</title><rect x="229.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 7): wall</title><rect x="263.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (1, 8): open, distance 13</title><rect x="297.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 0): open, distance 1</title><rect x="25.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 1): open, distance 1</title><rect x="59.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 2): wall</title><rect x="93.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 3): open, distance 7</title><rect x="127.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 4): wall</title><rect x="161.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 5): open, distance 10</title><rect x="195.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 6): open, distance 10</title><rect x="229.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 7): wall</title><rect x="263.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (2, 8): open, distance 14</title><rect x="297.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 0): open, distance 0, the start</title><rect x="25.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 1): open, distance 1</title><rect x="59.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (3, 2): wall</title><rect x="93.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 3): open, distance 6</title><rect x="127.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 4): open, distance 6</title><rect x="161.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (3, 5): wall</title><rect x="195.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 6): open, distance 9</title><rect x="229.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (3, 7): wall</title><rect x="263.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (3, 8): open, distance 15, the target</title><rect x="297.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (4, 0): open, distance 1</title><rect x="25.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (4, 1): open, distance 1</title><rect x="59.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (4, 2): wall</title><rect x="93.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (4, 3): open, distance 5</title><rect x="127.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (4, 4): wall</title><rect x="161.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (4, 5): open, distance 8</title><rect x="195.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (4, 6): open, distance 8</title><rect x="229.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (4, 7): wall</title><rect x="263.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (4, 8): open</title><rect x="297.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (5, 0): open, distance 2</title><rect x="25.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (5, 1): open, distance 2</title><rect x="59.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (5, 2): wall</title><rect x="93.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (5, 3): open, distance 4</title><rect x="127.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (5, 4): open, distance 5</title><rect x="161.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (5, 5): wall</title><rect x="195.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (5, 6): open, distance 7</title><rect x="229.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (5, 7): wall</title><rect x="263.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (5, 8): open</title><rect x="297.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 0): open, distance 3</title><rect x="25.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 1): open, distance 3</title><rect x="59.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 2): open, distance 3</title><rect x="93.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 3): open, distance 4</title><rect x="127.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 4): open, distance 5</title><rect x="161.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 5): open, distance 6</title><rect x="195.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open is-seen"><title>cell (6, 6): open, distance 7</title><rect x="229.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (6, 7): wall</title><rect x="263.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (6, 8): open</title><rect x="297.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-squeeze"><title>a diagonal between two walls: (0, 5) to (1, 4) is not a move</title><line x1="189" y1="51" x2="199" y2="61"/><line x1="189" y1="61" x2="199" y2="51"/></g><g class="gx-squeeze"><title>a diagonal between two walls: (1, 4) to (2, 5) is not a move</title><line x1="189" y1="85" x2="199" y2="95"/><line x1="189" y1="95" x2="199" y2="85"/></g><g class="gx-squeeze"><title>a diagonal between two walls: (2, 5) to (3, 4) is not a move</title><line x1="189" y1="119" x2="199" y2="129"/><line x1="189" y1="129" x2="199" y2="119"/></g><g class="gx-squeeze"><title>a diagonal between two walls: (3, 4) to (4, 5) is not a move</title><line x1="189" y1="153" x2="199" y2="163"/><line x1="189" y1="163" x2="199" y2="153"/></g><g class="gx-squeeze"><title>a diagonal between two walls: (4, 5) to (5, 4) is not a move</title><line x1="189" y1="187" x2="199" y2="197"/><line x1="189" y1="197" x2="199" y2="187"/></g><polyline class="gx-path" points="41,141 41,175 75,209 109,243 143,243 177,243 211,243 245,209 245,175 245,141 245,107 245,73 279,39 313,73 313,107 313,141"><title>the path: 15 steps</title></polyline><text class="gx-val" x="41" y="44" text-anchor="middle">3</text><text class="gx-val" x="75" y="44" text-anchor="middle">3</text><text class="gx-val" x="143" y="44" text-anchor="middle">9</text><text class="gx-val" x="211" y="44" text-anchor="middle">12</text><text class="gx-val" x="245" y="44" text-anchor="middle">12</text><text class="gx-val" x="279" y="44" text-anchor="middle">12</text><text class="gx-val" x="313" y="44" text-anchor="middle">13</text><text class="gx-val" x="41" y="78" text-anchor="middle">2</text><text class="gx-val" x="75" y="78" text-anchor="middle">2</text><text class="gx-val" x="143" y="78" text-anchor="middle">8</text><text class="gx-val" x="177" y="78" text-anchor="middle">8</text><text class="gx-val" x="245" y="78" text-anchor="middle">11</text><text class="gx-val" x="313" y="78" text-anchor="middle">13</text><text class="gx-val" x="41" y="112" text-anchor="middle">1</text><text class="gx-val" x="75" y="112" text-anchor="middle">1</text><text class="gx-val" x="143" y="112" text-anchor="middle">7</text><text class="gx-val" x="211" y="112" text-anchor="middle">10</text><text class="gx-val" x="245" y="112" text-anchor="middle">10</text><text class="gx-val" x="313" y="112" text-anchor="middle">14</text><text class="gx-tag" x="28" y="136">S</text><text class="gx-val" x="41" y="149" text-anchor="middle">0</text><text class="gx-val" x="75" y="146" text-anchor="middle">1</text><text class="gx-val" x="143" y="146" text-anchor="middle">6</text><text class="gx-val" x="177" y="146" text-anchor="middle">6</text><text class="gx-val" x="245" y="146" text-anchor="middle">9</text><text class="gx-tag" x="300" y="136">T</text><text class="gx-val" x="313" y="149" text-anchor="middle">15</text><text class="gx-val" x="41" y="180" text-anchor="middle">1</text><text class="gx-val" x="75" y="180" text-anchor="middle">1</text><text class="gx-val" x="143" y="180" text-anchor="middle">5</text><text class="gx-val" x="211" y="180" text-anchor="middle">8</text><text class="gx-val" x="245" y="180" text-anchor="middle">8</text><text class="gx-val" x="41" y="214" text-anchor="middle">2</text><text class="gx-val" x="75" y="214" text-anchor="middle">2</text><text class="gx-val" x="143" y="214" text-anchor="middle">4</text><text class="gx-val" x="177" y="214" text-anchor="middle">5</text><text class="gx-val" x="245" y="214" text-anchor="middle">7</text><text class="gx-val" x="41" y="248" text-anchor="middle">3</text><text class="gx-val" x="75" y="248" text-anchor="middle">3</text><text class="gx-val" x="109" y="248" text-anchor="middle">3</text><text class="gx-val" x="143" y="248" text-anchor="middle">4</text><text class="gx-val" x="177" y="248" text-anchor="middle">5</text><text class="gx-val" x="211" y="248" text-anchor="middle">6</text><text class="gx-val" x="245" y="248" text-anchor="middle">7</text></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="gx-key-s"></i>S ההתחלה, T היעד</span><span><i class="gx-key is-open"></i>תא פתוח</span><span><i class="gx-key is-wall"></i>קיר</span><span><i class="gx-key-path"></i>המסלול</span><span><i class="gx-key-squeeze"></i>אלכסון בין שני קירות : אסור</span></span>

    <!-- /gen -->

    <!-- gen 5 -->

    | הצעדים המותרים | אורך המסלול הקצר | מה קובע |
    |:--|:-:|:--|
    | ארבעה כיוונים | ‏20 | שלושת הקירות, כל אחד עוקפים דרך הפתח שלו |
    | שמונה כיוונים, בלי לעבור בין שני קירות (הכלל שלנו) | ‏15 | צעד באלכסון חוסך בפינות, אבל קיר הזיגזג עדיין סגור |
    | שמונה כיוונים, גם בין שני קירות (שאלת המשך) | ‏12 | המסלול חוצה את קיר הזיגזג באלכסון, בין שתי פינות של קירות |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="shortest_path" linenums="1" hl_lines="15 29 33 40"
        from collections import deque

        DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]                 # up, down, left, right
        DIRS8 = DIRS4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]       # and the four diagonals


        def moves(grid: list[str], r: int, c: int, diag: bool = False, wall: str = "1"):
            """The cells one step from (r, c) inside the grid, in the order of the table; with
            diag also the diagonals, except a diagonal between two walls."""
            m, n = len(grid), len(grid[0])
            for dr, dc in DIRS8 if diag else DIRS4:
                a, b = r + dr, c + dc
                if not (0 <= a < m and 0 <= b < n):
                    continue
                if dr and dc and grid[r][b] == wall and grid[a][c] == wall:   # (1)!
                    continue
                yield a, b


        def shortest_path(grid: list[str], s: tuple, t: tuple, diag: bool = False):
            """BFS from s over the open cells ('0'): the number of steps of a shortest path to t
            and the path itself, cell by cell; (-1, []) when t cannot be reached."""
            m, n = len(grid), len(grid[0])
            dist = [[-1] * n for _ in range(m)]
            parent = [[None] * n for _ in range(m)]
            dist[s[0]][s[1]] = 0
            q = deque([s])
            while q:
                r, c = q.popleft()                                  # (2)!
                if (r, c) == t:
                    break
                for a, b in moves(grid, r, c, diag):
                    if grid[a][b] == "0" and dist[a][b] < 0:        # (3)!
                        dist[a][b] = dist[r][c] + 1
                        parent[a][b] = (r, c)
                        q.append((a, b))
            if dist[t[0]][t[1]] < 0:
                return -1, []
            path, cell = [], t
            while cell is not None:                                 # (4)!
                path.append(cell)
                cell = parent[cell[0]][cell[1]]
            return dist[t[0]][t[1]], path[::-1]
        ```

        1. הכלל של האלכסון : צעד אלכסוני חולף על פני \( (r, b) \) ו-\( (a, c) \), ואם שניהם קירות הוא
           אסור. בצעד ישר אחד מ-`dr`, `dc` הוא 0, והבדיקה לא חלה. ‏`wall` הוא פרמטר כי בסעיף ג הקיר
           הוא `#`.
        2. ‏`popleft` מוציא מהראש ב-\( O(1) \). ‏\( T \) יוצא כשהגיע תורו, וכל התאים שעוד בתור כבר
           לא ישפיעו על המרחק שלו.
        3. רק תא פתוח שעוד אין לו מרחק מקבל מרחק והורה ונכנס לתור, ולכן כל תא נכנס פעם אחת לכל
           היותר. ‏`dist` הוא גם הסימון "כבר נראה".
        4. ‏`parent` של \( S \) נשאר `None`, ושם ההליכה אחורה נעצרת. ‏`path[::-1]` הופך את הרשימה כך
           שהיא מתחילה ב-\( S \).

    === "SystemVerilog"
        ```systemverilog title="function shortest_path" linenums="1" hl_lines="14 34 39 49"
        typedef struct { int r, c; } cell_t;
        localparam int DR[8] = '{-1, 1, 0, 0, -1, -1, 1, 1};     // up, down, left, right, then the diagonals
        localparam int DC[8] = '{0, 0, -1, 1, -1, 1, -1, 1};

        // the cells one step from (r, c) inside the grid, in the order of the table; with diag
        // also the diagonals, except a diagonal between two walls
        function automatic void moves(string grid[], int r, int c, bit diag, byte wall, output cell_t out[$]);
          int m = grid.size(), n = grid[0].len(), a, b;
          out = {};
          for (int k = 0; k < (diag ? 8 : 4); k++) begin
            a = r + DR[k];
            b = c + DC[k];
            if (a < 0 || a >= m || b < 0 || b >= n) continue;
            if (DR[k] != 0 && DC[k] != 0 && grid[r].getc(b) == wall && grid[a].getc(c) == wall) continue;   // (1)!
            out.push_back('{a, b});
          end
        endfunction

        // BFS from s over the open cells ("0"): the number of steps of a shortest path to t, and
        // the path cell by cell; -1 and an empty path when t cannot be reached
        function automatic int shortest_path(string grid[], cell_t s, cell_t t, bit diag, output cell_t path[$]);
          int m = grid.size(), n = grid[0].len(), dst[][];
          cell_t parent[][], q[$], nb[$], u, v;
          dst = new[m];
          parent = new[m];
          foreach (dst[i]) begin
            dst[i] = new[n];
            parent[i] = new[n];
            foreach (dst[i][j]) dst[i][j] = -1;
          end
          dst[s.r][s.c] = 0;
          q.push_back(s);
          while (q.size() > 0) begin
            u = q.pop_front();                                             // (2)!
            if (u.r == t.r && u.c == t.c) break;
            moves(grid, u.r, u.c, diag, "1", nb);
            foreach (nb[i]) begin
              v = nb[i];
              if (grid[v.r].getc(v.c) == "0" && dst[v.r][v.c] < 0) begin   // (3)!
                dst[v.r][v.c] = dst[u.r][u.c] + 1;
                parent[v.r][v.c] = u;
                q.push_back(v);
              end
            end
          end
          path = {};
          if (dst[t.r][t.c] < 0) return -1;
          v = t;
          while (v.r != s.r || v.c != s.c) begin                             // (4)!
            path.push_front(v);
            v = parent[v.r][v.c];
          end
          path.push_front(s);
          return dst[t.r][t.c];
        endfunction
        ```

        1. הכלל של האלכסון : שני התאים שהצעד חולף על פניהם הם קירות. ‏`getc(b)` הוא התו ה-`b`
           של השורה, ו-`wall` הוא `"1"` כאן ו-`"#"` בסעיף ג.
        2. ראש התור יוצא. המערך נקרא `dst` ולא `dist`, כי `dist` היא מילה שמורה ב-SystemVerilog
           (אילוצים).
        3. רק תא פתוח שעוד אין לו מרחק נכנס לתור, ולכן כל תא נכנס פעם אחת לכל היותר.
        4. ההליכה אחורה מ-\( T \) דרך ההורים, ו-`push_front` כך שהתור מתחיל ב-\( S \). הבדיקה
           של `dst` של \( T \) לפניה מבטיחה שהשרשרת מגיעה ל-\( S \).

    #### למה זה נכון { .sol-proof }

    **השמורה :** בכל רגע המרחקים של התאים בתור, מהראש לזנב, אינם יורדים, וההפרש בין הזנב לראש הוא
    לכל היותר 1. באינדוקציה : בהתחלה התור מחזיק רק את \( S \). בצעד יוצא הראש עם מרחק \( d \), וכל
    תא שנכנס מקבל \( d + 1 \) : גדול או שווה לכל מה שבתור (שם המרחקים בין \( d \) ל-\( d + 1 \)), ושוב
    הכול בתוך חלון של 1. לכן **התאים יוצאים מהתור לפי מרחק לא יורד** : קודם כל התאים של שכבה 0,
    אחר כך כל אלה של שכבה 1, וכן הלאה. אלה השכבות של הטבלה.

    **המרחק שנכתב הוא המרחק האמיתי (ההוכחה בשכבות) :** באינדוקציה על המרחק האמיתי \( \delta \).
    התא היחיד עם \( \delta = 0 \) הוא \( S \). נניח שכל תא עם \( \delta = d \) קיבל \( \text{dist} = d \),
    ויהי \( v \) תא עם \( \delta(v) = d + 1 \). במסלול קצר אליו, התא שלפניו \( u \) מקיים
    \( \delta(u) = d \), ולכן \( \text{dist}(u) = d \) ו-\( u \) נכנס לתור. ‏\( v \) לא יכול לקבל מרחק
    קטן מ-\( d + 1 \) : כל מרחק שנכתב הוא אורך של מסלול אמיתי (שרשרת ההורים), ולכן אינו קטן
    מ-\( \delta(v) \). והוא לא יקבל מרחק גדול מ-\( d + 1 \) : כש-\( u \) יוצא מהתור, \( v \) מקבל
    \( d + 1 \) אם עוד אין לו מרחק, ואם כבר יש לו, הוא קיבל אותו מתא שיצא לפני \( u \), כלומר
    עם מרחק \( \le d \) (השמורה), ולכן \( \le d + 1 \). בשני המקרים \( \text{dist}(v) = d + 1 \).

    **העצירה ב-\( T \) והמסלול :** כש-\( T \) יוצא, המרחק שלו כבר סופי (הוא נכתב כשנכנס), ולכן מותר
    לעצור. שרשרת ההורים מ-\( T \) יורדת במרחק ב-1 בכל צעד, \( \text{dist}(\text{parent}(v)) = \text{dist}(v) - 1 \),
    ולכן היא מגיעה ל-\( S \) אחרי \( \text{dist}(T) \) צעדים בדיוק : מסלול באורך הקצר ביותר. אם התור
    מתרוקן ו-\( T \) לא קיבל מרחק, אין אליו מסלול (אחרת התא שלפניו במסלול היה מכניס אותו), והתשובה
    <span dir="ltr">−1</span>.

    **שמונה כיוונים :** ההוכחה לא הזכירה כמה שכנים יש לתא, רק ש"שכן" מוגדר באותו אופן לכל תא, ושכל
    צעד עולה 1. לכן היא נכונה גם עם שמונה כיוונים, והמרחק הוא מספר הצעדים כשצעד באלכסון הוא צעד
    אחד. הכלל של האלכסון רק מוריד קשתות מהגרף.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(RC) \). כל תא נכנס לתור ויוצא ממנו פעם אחת לכל היותר, ובכל יציאה נבדקים 4 או 8
      שכנים, כלומר לכל היותר \( 8RC \) בדיקות. בניית המסלול היא \( O(RC) \) נוספים, כי במסלול
      פשוט כל תא מופיע פעם אחת.
    - **זיכרון :** ‏\( O(RC) \) ל-`dist`, ל-`parent` ולתור.
    - **מקרי קצה :** ‏\( S = T \) מחזיר 0 ומסלול של תא אחד. ‏\( T \) מוקף קירות מחזיר
      <span dir="ltr">−1</span>. לוח של שורה אחת : המסלול הוא הקטע הישר, אם אין בו קיר.

    **נסו בעצמכם.** הלוח של הדוגמה. לחיצה או גרירה על תאים מציירת קירות (ומוחקת אותם), ואת \( S \) ו-\( T \)
    גוררים למקום אחר. כל צעד הוא תא אחד שיוצא מהתור : הוא מוקף, השכנים שלו מסומנים, התאים שבתור
    צבועים, ובכל תא שכבר יצא כתוב המרחק שלו. "הפעלה" מריצה את הגל, ובסוף המסלול מצויר :

    <div class="explorer" data-kind="gridpath" data-mode="a" data-grid="001010000.001001010.001010010.001001010.001010010.001001010.000000010" data-s="3,0" data-t="3,8"></div>

---

### סעיף ב – מותר לשבור עד k קירות

??? tip "רמז 1"
    שני מסלולים יכולים להגיע לאותו תא באותו מספר צעדים, אבל אחד מהם כבר שבר קיר והשני לא. האם
    הם באמת "באותו מקום"? מה צריך לדעת, חוץ מהתא, כדי להמשיך מכאן?

??? tip "רמז 2"
    המצב הוא (שורה, עמודה, שבירות שנשארו). חפשו ב-BFS על המצבים האלה : כניסה לקיר מורידה שבירה
    אחת. ואם כבר הגעתם לתא עם 2 שבירות שנשארו, האם יש טעם להגיע אליו שוב, מאוחר יותר, עם 1?

<div class="selfcheck" data-answer="3" data-show="3 : מ-(3, 0) למעלה ל-(2, 0), שוברים את הקיר (1, 0), ונכנסים ל-(0, 0)" data-hint="עכשיו מותר להיכנס לקיר אחד. איזה קיר עומד בין (2, 0) ל-(0, 0)?" markdown>
באותו לוח <span dir="ltr">0000 / 1110 / 0000 / 0111</span>, עם ארבעה כיוונים, \( S = (3, 0) \),
\( T = (0, 0) \) ו-\( k = 1 \). כמה צעדים במסלול הקצר ביותר?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏BFS על **מצבים** \( (r, c, \ell) \), כש-\( \ell \) הוא מספר השבירות שנשארו : צעד לתא פתוח
        שומר את \( \ell \), צעד לקיר מוריד אותו ב-1, ואסור לרדת מתחת ל-0. לכל תא שומרים את ה-\( \ell \)
        הגדול ביותר שאיתו נכנסו אליו, ומצב חדש נכנס לתור רק אם הוא **גדול ממנו**. כל תא נכנס לכל
        היותר \( k + 1 \) פעמים, ולכן הזמן \( O(RC(k + 1)) \). בדוגמה התשובה יורדת מ-20 (\( k = 0 \))
        ל-14 (\( k = 1, 2 \)) ול-8 (\( k \ge 3 \)).

    <!-- cost: זמן \( O(RC(k + 1)) \) | זיכרון \( O(RC(k + 1)) \) -->

    #### הרעיון { .sol-idea }

    **למה התא לבדו לא מספיק.** ב-BFS של סעיף א תא שכבר ראינו לא נכנס שוב, כי מי שמגיע אליו מאוחר
    יותר לא יכול לעשות משם שום דבר שהראשון לא יכול. עכשיו זה לא נכון : מי שהגיע ראשון אולי בזבז
    את השבירה שלו, ומי שמגיע שני, בדרך ארוכה יותר, עדיין מחזיק אותה, ורק הוא יכול לשבור את הקיר
    הבא. **המצב** של החיפוש, כל מה שקובע מה אפשר לעשות מכאן והלאה, הוא התא **ועוד** מספר השבירות
    שנשארו, \( \ell \). זה גרף חדש : הצמתים הם המצבים \( (r, c, \ell) \), עם \( 0 \le \ell \le k \),
    וצעד מ-\( (r, c, \ell) \) לשכן \( (a, b) \) מוביל ל-\( (a, b, \ell) \) כשהשכן פתוח, ול-\( (a, b, \ell - 1) \)
    כשהוא קיר, אם \( \ell \ge 1 \). כל צעד עדיין עולה 1, ולכן BFS על המצבים מוצא את המסלול הקצר
    ביותר, וההוכחה של סעיף א עובדת כמו שהיא על הגרף הזה.

    **דוגמה נגדית ל-BFS עם סימון לכל תא.** לוח של 3 על 3, מ-\( (0, 0) \) ל-\( (2, 2) \), עם \( k = 1 \) :

    <!-- gen 6 -->

    <svg class="figure gx-fig" viewBox="0 0 132 130" style="max-width:8.25rem" role="img" aria-label="הלוח הקטן של המלכודת : 3 על 3, ההתחלה בפינה השמאלית העליונה והיעד בפינה הימנית התחתונה"><text class="tick" x="41" y="14" text-anchor="middle">0</text><text class="tick" x="75" y="14" text-anchor="middle">1</text><text class="tick" x="109" y="14" text-anchor="middle">2</text><text class="tick" x="17" y="43" text-anchor="end">0</text><text class="tick" x="17" y="77" text-anchor="end">1</text><text class="tick" x="17" y="111" text-anchor="end">2</text><g class="gx-cell is-open"><title>cell (0, 0): open, the start</title><rect x="25.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (0, 1): open</title><rect x="59.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (0, 2): wall</title><rect x="93.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 0): wall</title><rect x="25.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (1, 1): open</title><rect x="59.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 2): wall</title><rect x="93.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (2, 0): open</title><rect x="25.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 1): wall</title><rect x="59.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (2, 2): open, the target</title><rect x="93.5" y="91.5" width="31" height="31" rx="3"/></g><text class="gx-tag" x="28" y="34">S</text><text class="gx-tag" x="96" y="102">T</text></svg>

    <!-- /gen -->

    ‏BFS שמסמן **תאים** (כל תא נכנס פעם אחת, עם ה-\( \ell \) של הכניסה הראשונה). בכל שורה, המצב
    שיוצא מהתור כתוב כמו בקוד, <span dir="ltr">(r, c, ℓ, d)</span> : התא, השבירות שנשארו ומספר
    הצעדים :

    <!-- gen 7 -->

    | הצעד | יוצא מהתור | המהלכים שנבדקים | התור אחרי |
    |:-:|:-:|:--|:--|
    | ‏1 | ‏<span dir="ltr">(0,0,1,0)</span> | למטה <span dir="ltr">(1, 0)</span> קיר : **נכנס עם 0**; ימינה <span dir="ltr">(0, 1)</span> : **נכנס עם 1** | ‏<span dir="ltr">(1,0,0,1) (0,1,1,1)</span> |
    | ‏2 | ‏<span dir="ltr">(1,0,0,1)</span> | למעלה <span dir="ltr">(0, 0)</span> : כבר סומן; למטה <span dir="ltr">(2, 0)</span> : **נכנס עם 0**; ימינה <span dir="ltr">(1, 1)</span> : **נכנס עם 0** | ‏<span dir="ltr">(0,1,1,1) (2,0,0,2) (1,1,0,2)</span> |
    | ‏3 | ‏<span dir="ltr">(0,1,1,1)</span> | למטה <span dir="ltr">(1, 1)</span> : כבר סומן; שמאלה <span dir="ltr">(0, 0)</span> : כבר סומן; ימינה <span dir="ltr">(0, 2)</span> קיר : **נכנס עם 0** | ‏<span dir="ltr">(2,0,0,2) (1,1,0,2) (0,2,0,2)</span> |
    | ‏4 | ‏<span dir="ltr">(2,0,0,2)</span> | למעלה <span dir="ltr">(1, 0)</span> קיר : אין שבירות; ימינה <span dir="ltr">(2, 1)</span> קיר : אין שבירות | ‏<span dir="ltr">(1,1,0,2) (0,2,0,2)</span> |
    | ‏5 | ‏<span dir="ltr">(1,1,0,2)</span> | למעלה <span dir="ltr">(0, 1)</span> : כבר סומן; למטה <span dir="ltr">(2, 1)</span> קיר : אין שבירות; שמאלה <span dir="ltr">(1, 0)</span> קיר : אין שבירות; ימינה <span dir="ltr">(1, 2)</span> קיר : אין שבירות | ‏<span dir="ltr">(0,2,0,2)</span> |
    | ‏6 | ‏<span dir="ltr">(0,2,0,2)</span> | למטה <span dir="ltr">(1, 2)</span> קיר : אין שבירות; שמאלה <span dir="ltr">(0, 1)</span> : כבר סומן | ‏ריק |
    | ‏7 | — | התור ריק : התשובה <span dir="ltr">−1</span> | ריק |

    <!-- /gen -->

    בצעד 2 המצב \( (1, 0) \), שכבר שבר את הקיר שלו, מגיע ראשון לתא האמצעי \( (1, 1) \) ומסמן אותו
    עם \( \ell = 0 \). בצעד 3 המסלול שלא שבר כלום מגיע לאותו תא, עם \( \ell = 1 \), ונדחה כי התא
    "כבר סומן". מהתא האמצעי בלי שבירות אי אפשר להגיע ל-\( T \), והחיפוש נגמר ב-<span dir="ltr">−1</span>.
    התשובה הנכונה היא 4 : ‏\( (0, 0) \to (0, 1) \to (1, 1) \to (2, 1) \to (2, 2) \), עם שבירה של
    \( (2, 1) \).

    **התיקון : הכי הרבה שבירות שנשארו.** לכל תא שומרים את \( \text{best}[a][b] \), ה-\( \ell \)
    הגדול ביותר שאיתו נכנסו אליו עד עכשיו (<span dir="ltr">−1</span> לתא שלא נכנסו אליו). מצב חדש
    \( (a, b, \ell') \) נכנס לתור רק אם \( \ell' > \text{best}[a][b] \). למה מותר לזרוק את השאר : BFS
    מוציא מצבים לפי מספר צעדים לא יורד, ולכן המצב הקודם של התא הגיע אליו בפחות צעדים או באותו מספר,
    ועם לפחות אותן שבירות. כל מה שאפשר לעשות מהמצב החדש אפשר לעשות גם מהקודם, באותו מספר צעדים או
    פחות : המצב החדש **נשלט**. אותה ריצה עם התיקון :

    <!-- gen 8 -->

    | הצעד | יוצא מהתור | המהלכים שנבדקים | התור אחרי |
    |:-:|:-:|:--|:--|
    | ‏1 | ‏<span dir="ltr">(0,0,1,0)</span> | למטה <span dir="ltr">(1, 0)</span> קיר : **נכנס עם 0**; ימינה <span dir="ltr">(0, 1)</span> : **נכנס עם 1** | ‏<span dir="ltr">(1,0,0,1) (0,1,1,1)</span> |
    | ‏2 | ‏<span dir="ltr">(1,0,0,1)</span> | למעלה <span dir="ltr">(0, 0)</span> : 0 לא יותר מ-1; למטה <span dir="ltr">(2, 0)</span> : **נכנס עם 0**; ימינה <span dir="ltr">(1, 1)</span> : **נכנס עם 0** | ‏<span dir="ltr">(0,1,1,1) (2,0,0,2) (1,1,0,2)</span> |
    | ‏3 | ‏<span dir="ltr">(0,1,1,1)</span> | למטה <span dir="ltr">(1, 1)</span> : **נכנס עם 1**; שמאלה <span dir="ltr">(0, 0)</span> : 1 לא יותר מ-1; ימינה <span dir="ltr">(0, 2)</span> קיר : **נכנס עם 0** | ‏<span dir="ltr">(2,0,0,2) (1,1,0,2) (1,1,1,2) (0,2,0,2)</span> |
    | ‏4 | ‏<span dir="ltr">(2,0,0,2)</span> | למעלה <span dir="ltr">(1, 0)</span> קיר : אין שבירות; ימינה <span dir="ltr">(2, 1)</span> קיר : אין שבירות | ‏<span dir="ltr">(1,1,0,2) (1,1,1,2) (0,2,0,2)</span> |
    | ‏5 | ‏<span dir="ltr">(1,1,0,2)</span> | למעלה <span dir="ltr">(0, 1)</span> : 0 לא יותר מ-1; למטה <span dir="ltr">(2, 1)</span> קיר : אין שבירות; שמאלה <span dir="ltr">(1, 0)</span> קיר : אין שבירות; ימינה <span dir="ltr">(1, 2)</span> קיר : אין שבירות | ‏<span dir="ltr">(1,1,1,2) (0,2,0,2)</span> |
    | ‏6 | ‏<span dir="ltr">(1,1,1,2)</span> | למעלה <span dir="ltr">(0, 1)</span> : 1 לא יותר מ-1; למטה <span dir="ltr">(2, 1)</span> קיר : **נכנס עם 0**; שמאלה <span dir="ltr">(1, 0)</span> קיר : 0 לא יותר מ-0; ימינה <span dir="ltr">(1, 2)</span> קיר : **נכנס עם 0** | ‏<span dir="ltr">(0,2,0,2) (2,1,0,3) (1,2,0,3)</span> |
    | ‏7 | ‏<span dir="ltr">(0,2,0,2)</span> | למטה <span dir="ltr">(1, 2)</span> קיר : אין שבירות; שמאלה <span dir="ltr">(0, 1)</span> : 0 לא יותר מ-1 | ‏<span dir="ltr">(2,1,0,3) (1,2,0,3)</span> |
    | ‏8 | ‏<span dir="ltr">(2,1,0,3)</span> | למעלה <span dir="ltr">(1, 1)</span> : 0 לא יותר מ-1; שמאלה <span dir="ltr">(2, 0)</span> : 0 לא יותר מ-0; ימינה <span dir="ltr">(2, 2)</span> : **נכנס עם 0** | ‏<span dir="ltr">(1,2,0,3) (2,2,0,4)</span> |
    | ‏9 | ‏<span dir="ltr">(1,2,0,3)</span> | למעלה <span dir="ltr">(0, 2)</span> קיר : אין שבירות; למטה <span dir="ltr">(2, 2)</span> : 0 לא יותר מ-0; שמאלה <span dir="ltr">(1, 1)</span> : 0 לא יותר מ-1 | ‏<span dir="ltr">(2,2,0,4)</span> |
    | ‏10 | ‏<span dir="ltr">(2,2,0,4)</span> | **היעד** : התשובה 4 | ‏ריק |

    <!-- /gen -->

    הפעם בצעד 3 המצב עם \( \ell = 1 \) מגיע לתא האמצעי, ו-\( 1 > 0 \), ולכן הוא נכנס לתור למרות
    שהתא כבר נראה. בצעד 6 הוא יוצא, ומשם שובר את \( (2, 1) \) ומגיע ל-\( T \) אחרי 4 צעדים. התא
    האמצעי נכנס לתור פעמיים, פעם לכל ערך של \( \ell \) ; זה המחיר של המצב המורחב, ולכן הזמן
    \( O(RC(k + 1)) \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מתחילים :** ‏\( \text{best}[S] = k \), כל השאר <span dir="ltr">−1</span>, והתור מחזיק את
       המצב \( (S, k, 0) \) : התא, השבירות שנשארו והצעדים.
    2. **מוציאים מראש התור :** את \( (r, c, \ell, d) \). אם \( (r, c) = T \), התשובה \( d \).
    3. **בודקים את השכנים :** לכל שכן \( (a, b) \), \( \ell' = \ell - 1 \) אם הוא קיר ו-\( \ell' = \ell \)
       אחרת.
    4. **רק מצב טוב יותר נכנס :** אם \( \ell' > \text{best}[a][b] \), כותבים
       \( \text{best}[a][b] = \ell' \) ומכניסים \( (a, b, \ell', d + 1) \). זה כולל את \( \ell' < 0 \) :
       קיר בלי שבירות נדחה מעצמו, כי \( -1 \) אינו גדול מ-\( \text{best} \ge -1 \).
    5. **תור ריק :** אין מסלול גם עם \( k \) שבירות, <span dir="ltr">−1</span>.

    </div>

    **על הדוגמה הגדולה.** עם \( k = 1 \) המסלול הקצר עובר מתחת לשני הקירות הראשונים ושובר את
    \( (3, 7) \) בעמודה 7, במקום לעלות לפתח שלה : 14 צעדים במקום 20. כך התשובה יורדת עם \( k \) :

    <!-- gen 9 -->

    <svg class="figure gx-fig" viewBox="0 0 336 266" style="max-width:21rem" role="img" aria-label="הדוגמה עם k = 1 : המסלול של 14 צעדים שובר את הקיר של עמודה 7"><text class="tick" x="41" y="14" text-anchor="middle">0</text><text class="tick" x="75" y="14" text-anchor="middle">1</text><text class="tick" x="109" y="14" text-anchor="middle">2</text><text class="tick" x="143" y="14" text-anchor="middle">3</text><text class="tick" x="177" y="14" text-anchor="middle">4</text><text class="tick" x="211" y="14" text-anchor="middle">5</text><text class="tick" x="245" y="14" text-anchor="middle">6</text><text class="tick" x="279" y="14" text-anchor="middle">7</text><text class="tick" x="313" y="14" text-anchor="middle">8</text><text class="tick" x="17" y="43" text-anchor="end">0</text><text class="tick" x="17" y="77" text-anchor="end">1</text><text class="tick" x="17" y="111" text-anchor="end">2</text><text class="tick" x="17" y="145" text-anchor="end">3</text><text class="tick" x="17" y="179" text-anchor="end">4</text><text class="tick" x="17" y="213" text-anchor="end">5</text><text class="tick" x="17" y="247" text-anchor="end">6</text><g class="gx-cell is-open"><title>cell (0, 0): open</title><rect x="25.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (0, 1): open</title><rect x="59.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (0, 2): wall</title><rect x="93.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (0, 3): open</title><rect x="127.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (0, 4): wall</title><rect x="161.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (0, 5): open</title><rect x="195.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (0, 6): open</title><rect x="229.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (0, 7): open</title><rect x="263.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (0, 8): open</title><rect x="297.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (1, 0): open</title><rect x="25.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (1, 1): open</title><rect x="59.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 2): wall</title><rect x="93.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (1, 3): open</title><rect x="127.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (1, 4): open</title><rect x="161.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 5): wall</title><rect x="195.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (1, 6): open</title><rect x="229.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (1, 7): wall</title><rect x="263.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (1, 8): open</title><rect x="297.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (2, 0): open</title><rect x="25.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (2, 1): open</title><rect x="59.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 2): wall</title><rect x="93.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (2, 3): open</title><rect x="127.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 4): wall</title><rect x="161.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (2, 5): open</title><rect x="195.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (2, 6): open</title><rect x="229.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (2, 7): wall</title><rect x="263.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (2, 8): open</title><rect x="297.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (3, 0): open, the start</title><rect x="25.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (3, 1): open</title><rect x="59.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (3, 2): wall</title><rect x="93.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (3, 3): open</title><rect x="127.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (3, 4): open</title><rect x="161.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (3, 5): wall</title><rect x="195.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (3, 6): open</title><rect x="229.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-broken"><title>cell (3, 7): a wall broken on the way</title><rect x="263.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (3, 8): open, the target</title><rect x="297.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (4, 0): open</title><rect x="25.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (4, 1): open</title><rect x="59.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (4, 2): wall</title><rect x="93.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (4, 3): open</title><rect x="127.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (4, 4): wall</title><rect x="161.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (4, 5): open</title><rect x="195.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (4, 6): open</title><rect x="229.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (4, 7): wall</title><rect x="263.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (4, 8): open</title><rect x="297.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (5, 0): open</title><rect x="25.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (5, 1): open</title><rect x="59.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (5, 2): wall</title><rect x="93.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (5, 3): open</title><rect x="127.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (5, 4): open</title><rect x="161.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (5, 5): wall</title><rect x="195.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (5, 6): open</title><rect x="229.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (5, 7): wall</title><rect x="263.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (5, 8): open</title><rect x="297.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (6, 0): open</title><rect x="25.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (6, 1): open</title><rect x="59.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (6, 2): open</title><rect x="93.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (6, 3): open</title><rect x="127.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (6, 4): open</title><rect x="161.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (6, 5): open</title><rect x="195.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (6, 6): open</title><rect x="229.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-wall"><title>cell (6, 7): wall</title><rect x="263.5" y="227.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open"><title>cell (6, 8): open</title><rect x="297.5" y="227.5" width="31" height="31" rx="3"/></g><polyline class="gx-path" points="41,141 41,175 41,209 41,243 75,243 109,243 143,243 177,243 211,243 245,243 245,209 245,175 245,141 279,141 313,141"><title>the path: 14 steps</title></polyline><text class="gx-tag" x="28" y="136">S</text><text class="gx-tag" x="300" y="136">T</text></svg>

    <!-- /gen -->

    <!-- gen 10 -->

    <span class="viz-legend"><span><i class="gx-key-s"></i>S ההתחלה, T היעד</span><span><i class="gx-key is-open"></i>תא פתוח</span><span><i class="gx-key is-wall"></i>קיר</span><span><i class="gx-key is-broken"></i>קיר שנשבר בדרך</span><span><i class="gx-key-path"></i>המסלול</span></span>

    <!-- /gen -->

    <!-- gen 11 -->

    | הצעדים | ‏k = 0 | ‏k = 1 | ‏k = 2 | ‏k = 3 | ‏k = 4 |
    |:--|:-:|:-:|:-:|:-:|:-:|
    | ארבעה כיוונים | ‏20 | ‏14 | ‏14 | ‏8 | ‏8 |
    | שמונה כיוונים | ‏15 | ‏9 | ‏8 | ‏8 | ‏8 |

    <!-- /gen -->

    עם \( k = 2 \) אין שיפור : לשבור שני קירות בשורה 3 משאיר את השלישי, והעקיפה שלו עולה לפחות
    6 צעדים, כמו עם \( k = 1 \). עם \( k = 3 \) שוברים את שלושתם והולכים ישר בשורה 3 : 8 צעדים,
    המרחק בלי שום קיר, ומשם \( k \) גדול יותר כבר לא עוזר. עם שמונה כיוונים שבירה אחת כבר מקצרת
    מ-15 ל-9, כי מ-\( (5, 6) \) עולים באלכסון אל \( (4, 7) \), שוברים אותו, ומשם צעד אלכסוני אחד ל-\( T \).

    #### הקוד { .sol-code }

    === "Python"
        ```python title="shortest_with_breaks" linenums="1" hl_lines="14 15"
        def shortest_with_breaks(grid: list[str], s: tuple, t: tuple, k: int, diag: bool = False) -> int:
            """BFS over the states (row, column, breaks left, steps): stepping into a wall ('1')
            uses one break. best[r][c] is the most breaks left with which (r, c) was entered so
            far; a state that does not beat it is dropped. The number of steps, or -1."""
            m, n = len(grid), len(grid[0])
            best = [[-1] * n for _ in range(m)]
            best[s[0]][s[1]] = k
            q = deque([(s[0], s[1], k, 0)])                         # (1)!
            while q:
                r, c, left, d = q.popleft()
                if (r, c) == t:
                    return d                                        # (2)!
                for a, b in moves(grid, r, c, diag):
                    rest = left - (grid[a][b] == "1")               # (3)!
                    if rest > best[a][b]:                           # (4)!
                        best[a][b] = rest
                        q.append((a, b, rest, d + 1))
            return -1
        ```

        1. המצב כולו בתור : התא, השבירות שנשארו, ומספר הצעדים. ‏`deque` ו-`moves` הם של סעיף א.
        2. היעד יוצא מהתור : זה המספר הקטן ביותר של צעדים, עם כל מספר של שבירות שנשארו.
        3. ‏`True` הוא 1 ב-Python, ולכן כניסה לקיר מורידה שבירה אחת וכניסה לתא פתוח לא.
        4. רק מצב עם **יותר** שבירות ממה שכבר נראה בתא נכנס. מכאן גם ש-`rest = -1` (קיר בלי
           שבירות) נדחה, ושכל תא נכנס לכל היותר \( k + 1 \) פעמים.

    === "SystemVerilog"
        ```systemverilog title="function shortest_with_breaks" linenums="1" hl_lines="22 23"
        typedef struct { int r, c, left, d; } state_t;    // a cell, the breaks left, the steps so far

        // BFS over the states (cell, breaks left): stepping into a wall ("1") uses one break;
        // best[r][c] is the most breaks left with which (r, c) was entered so far, and a state
        // that does not beat it is dropped. The number of steps, or -1
        function automatic int shortest_with_breaks(string grid[], cell_t s, cell_t t, int k, bit diag);
          int m = grid.size(), n = grid[0].len(), best[][], rest;
          state_t q[$], u;
          cell_t nb[$];
          best = new[m];
          foreach (best[i]) begin
            best[i] = new[n];
            foreach (best[i][j]) best[i][j] = -1;
          end
          best[s.r][s.c] = k;
          q.push_back('{s.r, s.c, k, 0});                                // (1)!
          while (q.size() > 0) begin
            u = q.pop_front();
            if (u.r == t.r && u.c == t.c) return u.d;                    // (2)!
            moves(grid, u.r, u.c, diag, "1", nb);
            foreach (nb[i]) begin
              rest = u.left - (grid[nb[i].r].getc(nb[i].c) == "1");      // (3)!
              if (rest > best[nb[i].r][nb[i].c]) begin                   // (4)!
                best[nb[i].r][nb[i].c] = rest;
                q.push_back('{nb[i].r, nb[i].c, rest, u.d + 1});
              end
            end
          end
          return -1;
        endfunction
        ```

        1. המצב כולו בתור, כמבנה. ‏`moves` ו-`cell_t` הם של סעיף א.
        2. היעד יוצא מהתור : המספר הקטן ביותר של צעדים.
        3. ההשוואה `== "1"` היא ביט אחד, 1 לקיר : כניסה לקיר מורידה שבירה אחת.
        4. רק מצב עם יותר שבירות ממה שכבר נראה בתא נכנס, ולכן כל תא נכנס לכל היותר \( k + 1 \) פעמים.

    #### למה זה נכון { .sol-proof }

    **הגרף של המצבים :** מסלול בלוח שנכנס לכל היותר ל-\( k \) קירות הוא בדיוק מסלול בגרף המצבים
    מ-\( (S, k) \) : לאורך המסלול \( \ell \) יורד ב-1 בכל כניסה לקיר ונשאר \( \ge 0 \). לכן המסלול
    הקצר בלוח הוא המסלול הקצר בגרף המצבים אל אחד המצבים \( (T, \ell) \), \( 0 \le \ell \le k \).
    כל הקשתות בגרף הזה עולות 1, ו-BFS עליו (בלי שום גיזום) נכון לפי סעיף א. הראשון מבין \( (T, \ell) \)
    שיוצא מהתור הוא במרחק הקטן ביותר.

    **הגיזום לא מאבד תשובה :** נאמר שמצב \( (v, \ell) \) במרחק \( d \) **נשלט** על ידי \( (v, \ell') \)
    במרחק \( d' \) אם \( \ell' \ge \ell \) ו-\( d' \le d \). כל סדרת צעדים מ-\( (v, \ell) \) אפשרית גם
    מ-\( (v, \ell') \) (יש לפחות אותן שבירות), ומגיעה לאותו תא באותו מספר צעדים נוסף. הקוד דוחה
    מצב רק כש-\( \ell \le \text{best}[v] \), כלומר כשכבר נכנס לתור מצב של אותו תא עם
    \( \ell' \ge \ell \) ; הוא נכנס **לפני**, ובגלל השמורה של BFS עם מרחק \( d' \le d \). לכן המצב
    שנדחה נשלט, וכל מסלול שעבר דרכו קיים, לא ארוך יותר, דרך המצב ששלט בו. באינדוקציה על מספר
    הדחיות, קיים מסלול קצר ביותר שכל המצבים שלו נכנסו לתור.

    **מספר הכניסות :** \( \text{best}[v] \) רק עולה, מ-<span dir="ltr">−1</span> ועד \( k \) לכל
    היותר, וכל כניסה לתור מעלה אותו. לכן כל תא נכנס לכל היותר \( k + 1 \) פעמים.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(RC(k + 1)) \) : לכל היותר \( RC(k + 1) \) מצבים נכנסים ויוצאים, ובכל יציאה 4 או 8
      שכנים. בלי הגיזום (מערך `seen` לכל מצב) אותו חסם, ובפועל יותר כניסות.
    - **זיכרון :** ‏\( O(RC) \) ל-`best`, והתור מחזיק עד \( O(RC(k + 1)) \) מצבים.
    - **קיצור :** עם ארבעה כיוונים, המרחק בלי קירות הוא \( |\Delta r| + |\Delta c| \) (מרחק מנהטן), ומסלול
      באורך הזה נכנס לכל היותר ל-\( |\Delta r| + |\Delta c| - 1 \) קירות (התא האחרון, \( T \), פתוח). לכן
      כש-\( k \ge |\Delta r| + |\Delta c| - 1 \) התשובה היא מרחק מנהטן, בלי חיפוש. בדוגמה \( k \ge 7 \)
      מספיק לזה בוודאות, וכבר \( k = 3 \) מגיע ל-8.

    **נסו בעצמכם.** אותו לוח, עם שדה ל-\( k \) מ-0 עד 5. בכל תא שכבר נכנסו אליו כתוב מספר הצעדים,
    ובפינה הכי הרבה שבירות שנשארו ; קיר שנכנסו אליו נצבע כשבור. שנו את \( k \) וראו איך המסלול
    מתקצר, או ציירו את הלוח של המלכודת :

    <div class="explorer" data-kind="gridpath" data-mode="b" data-grid="001010000.001001010.001010010.001001010.001010010.001001010.000000010" data-s="3,0" data-t="3,8" data-k="1"></div>

---

### סעיף ג – עלות כניסה לכל תא : Dijkstra

??? tip "רמז 1"
    ‏BFS מוצא את המסלול עם הכי מעט **צעדים**. בשטח שבו הר עולה 9 וכביש 1, האם הכי מעט צעדים הוא
    גם הכי זול? מה יקרה ל-BFS אם הדרך הזולה ארוכה יותר?

??? tip "רמז 2"
    במקום תור לפי סדר הגעה, הוציאו בכל פעם את התא עם העלות הקטנה ביותר שידועה עד עכשיו. מבנה
    שנותן את הקטן ביותר מהר הוא ערימה (תור עדיפויות). למה התא הזה כבר לא יכול להשתפר?

<div class="selfcheck" data-answer="6" data-show="6 : מ-(0, 0) למטה דרך (1, 0) ו-(2, 0), ימינה ל-(2, 1) ו-(2, 2), ולמעלה דרך (1, 2) ל-(0, 2) : שישה תאים של 1. הדרך הישירה דרך ה-9 עולה 10" data-hint="העלות של התחלה לא משולמת. השוו את הדרך הישירה דרך (0, 1) לדרך מסביב." markdown>
בלוח העלויות <span dir="ltr">191 / 151 / 111</span> (שלוש שורות), עם ארבעה כיוונים,
\( S = (0, 0) \) ו-\( T = (0, 2) \). מה העלות הקטנה ביותר?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏**Dijkstra** מ-\( S \) : ערימת מינימום של שלשות (עלות, שורה, עמודה). בכל צעד מוציאים את
        השלשה עם העלות הקטנה ביותר ; רשומה ישנה מדלגים, ואם התא הוא \( T \) העלות שלו היא התשובה.
        אחרת, לכל שכן שאינו קיר, אם העלות שלו דרך התא קטנה ממה שידוע, כותבים אותה ודוחפים אותו
        לערימה. העלות של \( S \) היא 0. בדוגמה : 11, במסלול של 11 צעדים לאורך הכביש, כשמסלול ה-BFS
        של 7 צעדים עולה 39.

    <!-- cost: זמן \( O(RC \log(RC)) \) | זיכרון \( O(RC) \) -->

    #### הרעיון { .sol-idea }

    **למה לא BFS.** ‏BFS מוציא תאים לפי מספר הצעדים, ולכן הוא נותן לכל תא את המסלול עם הכי מעט צעדים.
    כשלכל תא עלות אחרת זה כבר לא המסלול הזול : דרך של 11 צעדים על כביש עולה 11, ודרך של 7 צעדים
    דרך הבוץ וההר עולה 39. בשטח של הדוגמה כל המסלולים של 7 צעדים עוברים בהר, והזול שבהם עולה 39.

    **מונחים.** ‏\( \text{cost}[v] \) היא העלות הקטנה ביותר **שידועה כרגע** להגיע ל-\( v \)
    (בהתחלה \( \infty \) לכולם חוץ מ-\( \text{cost}[S] = 0 \)). **שחרור** (relax) של צעד מ-\( u \)
    ל-\( v \) : אם \( \text{cost}[u] + w(v) < \text{cost}[v] \), כש-\( w(v) \) היא עלות הכניסה ל-\( v \),
    מצאנו דרך זולה יותר וכותבים אותה. **ערימת מינימום** (min-heap, תור עדיפויות) נותנת את האיבר
    הקטן ביותר ומכניסה איבר, כל אחד ב-\( O(\log m) \) ; ב-Python זה `heapq` על שלשות, שמושוות לפי
    העלות ובשוויון לפי השורה והעמודה.

    **‏Dijkstra.** מבין התאים שעוד לא יצאו מהערימה, זה עם העלות הקטנה ביותר כבר לא ישתפר : כל דרך
    אחרת אליו יוצאת מהאזור שכבר טופל דרך תא אחר שלא טופל, שהעלות שלו גדולה או שווה, וכל צעד מוסיף
    עלות חיובית. אז מוציאים אותו, משחררים את השכנים שלו, וחוזרים. זה אותו BFS, עם ערימה במקום תור :
    במקום שכבות של צעדים, "קווי גובה" של עלות. כשהיעד יוצא מהערימה, העלות שלו סופית.

    **רשומות ישנות, ולמה כאן אין כאלה.** כמו ב-[0067](0067-network-delay-time.md), כשעלות של תא משתפרת דוחפים רשומה חדשה והישנה
    נשארת בערימה ; כשהיא יוצאת מדלגים עליה (`if d > cost[r][c]`). אבל כאן העלות היא של **התא**,
    לא של הצעד : כל הצעדים אל \( v \) עולים אותו \( w(v) \). השכן הראשון של \( v \) שיוצא מהערימה
    הוא זה עם העלות הקטנה ביותר, ולכן הדחיפה הראשונה של \( v \) כבר סופית ואף פעם לא משתפרת. כל
    תא נכנס לערימה פעם אחת, והבדיקה של הרשומה הישנה אף פעם לא מתקיימת. היא נשארת בקוד כי היא שורה
    אחת, והיא מה שמחזיק את הקוד נכון כשהעלות על הצעד (שאלת המשך). **מה כן משנה הערימה** : את
    **הסדר**. תור FIFO היה מוציא את התאים לפי צעדים, והיה נותן לתא את העלות של הדרך הראשונה, לא
    הזולה.

    השטח של הדוגמה, \( S = (2, 0) \) ו-\( T = (3, 6) \). בפינה של כל תא עלות הכניסה, ובמרכז העלות
    הקטנה ביותר להגיע אליו (לתאים שיצאו מהערימה עד ש-\( T \) יצא). המסלול הזול רציף, ומסלול ה-BFS
    מקווקו :

    <!-- gen 12 -->

    <svg class="figure gx-fig" viewBox="0 0 268 232" style="max-width:16.75rem" role="img" aria-label="השטח של סעיף ג : כביש מסביב, בוץ והר באמצע ; בכל תא העלות הקטנה ביותר להגיע אליו (בפינה עלות הכניסה), המסלול הזול רציף ומסלול ה-BFS מקווקו"><text class="tick" x="41" y="14" text-anchor="middle">0</text><text class="tick" x="75" y="14" text-anchor="middle">1</text><text class="tick" x="109" y="14" text-anchor="middle">2</text><text class="tick" x="143" y="14" text-anchor="middle">3</text><text class="tick" x="177" y="14" text-anchor="middle">4</text><text class="tick" x="211" y="14" text-anchor="middle">5</text><text class="tick" x="245" y="14" text-anchor="middle">6</text><text class="tick" x="17" y="43" text-anchor="end">0</text><text class="tick" x="17" y="77" text-anchor="end">1</text><text class="tick" x="17" y="111" text-anchor="end">2</text><text class="tick" x="17" y="145" text-anchor="end">3</text><text class="tick" x="17" y="179" text-anchor="end">4</text><text class="tick" x="17" y="213" text-anchor="end">5</text><g class="gx-cell is-open gx-t1 is-seen"><title>cell (0, 0): entry cost 1, cost 2</title><rect x="25.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (0, 1): entry cost 1, cost 3</title><rect x="59.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (0, 2): entry cost 1, cost 4</title><rect x="93.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (0, 3): entry cost 1, cost 5</title><rect x="127.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (0, 4): entry cost 1, cost 6</title><rect x="161.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (0, 5): entry cost 1, cost 7</title><rect x="195.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (0, 6): entry cost 1, cost 8</title><rect x="229.5" y="23.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (1, 0): entry cost 1, cost 1</title><rect x="25.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2 is-seen"><title>cell (1, 1): entry cost 5, cost 6</title><rect x="59.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2 is-seen"><title>cell (1, 2): entry cost 5, cost 9</title><rect x="93.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t3 is-seen"><title>cell (1, 3): entry cost 9, cost 14</title><rect x="127.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2 is-seen"><title>cell (1, 4): entry cost 5, cost 11</title><rect x="161.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2 is-seen"><title>cell (1, 5): entry cost 5, cost 12</title><rect x="195.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (1, 6): entry cost 1, cost 9</title><rect x="229.5" y="57.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (2, 0): entry cost 1, cost 0, the start</title><rect x="25.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2 is-seen"><title>cell (2, 1): entry cost 5, cost 5</title><rect x="59.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t3 is-seen"><title>cell (2, 2): entry cost 9, cost 14</title><rect x="93.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t3"><title>cell (2, 3): entry cost 9</title><rect x="127.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t3 is-seen"><title>cell (2, 4): entry cost 9, cost 20</title><rect x="161.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2 is-seen"><title>cell (2, 5): entry cost 5, cost 15</title><rect x="195.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (2, 6): entry cost 1, cost 10</title><rect x="229.5" y="91.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (3, 0): entry cost 1, cost 1</title><rect x="25.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2 is-seen"><title>cell (3, 1): entry cost 5, cost 6</title><rect x="59.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t3 is-seen"><title>cell (3, 2): entry cost 9, cost 15</title><rect x="93.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t3"><title>cell (3, 3): entry cost 9</title><rect x="127.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t3"><title>cell (3, 4): entry cost 9</title><rect x="161.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2"><title>cell (3, 5): entry cost 5</title><rect x="195.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (3, 6): entry cost 1, cost 11, the target</title><rect x="229.5" y="125.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (4, 0): entry cost 1, cost 2</title><rect x="25.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2 is-seen"><title>cell (4, 1): entry cost 5, cost 7</title><rect x="59.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2 is-seen"><title>cell (4, 2): entry cost 5, cost 10</title><rect x="93.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t3 is-seen"><title>cell (4, 3): entry cost 9, cost 19</title><rect x="127.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2"><title>cell (4, 4): entry cost 5</title><rect x="161.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2"><title>cell (4, 5): entry cost 5</title><rect x="195.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1"><title>cell (4, 6): entry cost 1</title><rect x="229.5" y="159.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (5, 0): entry cost 1, cost 3</title><rect x="25.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (5, 1): entry cost 1, cost 4</title><rect x="59.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (5, 2): entry cost 1, cost 5</title><rect x="93.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t2 is-seen"><title>cell (5, 3): entry cost 5, cost 10</title><rect x="127.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1 is-seen"><title>cell (5, 4): entry cost 1, cost 11</title><rect x="161.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1"><title>cell (5, 5): entry cost 1</title><rect x="195.5" y="193.5" width="31" height="31" rx="3"/></g><g class="gx-cell is-open gx-t1"><title>cell (5, 6): entry cost 1</title><rect x="229.5" y="193.5" width="31" height="31" rx="3"/></g><polyline class="gx-path is-ghost" points="41,107 41,141 75,141 109,141 143,141 177,141 211,141 245,141"><title>the fewest steps (BFS): 7 steps</title></polyline><polyline class="gx-path" points="41,107 41,73 41,39 75,39 109,39 143,39 177,39 211,39 245,39 245,73 245,107 245,141"><title>the path: 11 steps</title></polyline><text class="gx-cost" x="54" y="34" text-anchor="end">1</text><text class="gx-val" x="41" y="47" text-anchor="middle">2</text><text class="gx-cost" x="88" y="34" text-anchor="end">1</text><text class="gx-val" x="75" y="47" text-anchor="middle">3</text><text class="gx-cost" x="122" y="34" text-anchor="end">1</text><text class="gx-val" x="109" y="47" text-anchor="middle">4</text><text class="gx-cost" x="156" y="34" text-anchor="end">1</text><text class="gx-val" x="143" y="47" text-anchor="middle">5</text><text class="gx-cost" x="190" y="34" text-anchor="end">1</text><text class="gx-val" x="177" y="47" text-anchor="middle">6</text><text class="gx-cost" x="224" y="34" text-anchor="end">1</text><text class="gx-val" x="211" y="47" text-anchor="middle">7</text><text class="gx-cost" x="258" y="34" text-anchor="end">1</text><text class="gx-val" x="245" y="47" text-anchor="middle">8</text><text class="gx-cost" x="54" y="68" text-anchor="end">1</text><text class="gx-val" x="41" y="81" text-anchor="middle">1</text><text class="gx-cost" x="88" y="68" text-anchor="end">5</text><text class="gx-val" x="75" y="81" text-anchor="middle">6</text><text class="gx-cost" x="122" y="68" text-anchor="end">5</text><text class="gx-val" x="109" y="81" text-anchor="middle">9</text><text class="gx-cost" x="156" y="68" text-anchor="end">9</text><text class="gx-val" x="143" y="81" text-anchor="middle">14</text><text class="gx-cost" x="190" y="68" text-anchor="end">5</text><text class="gx-val" x="177" y="81" text-anchor="middle">11</text><text class="gx-cost" x="224" y="68" text-anchor="end">5</text><text class="gx-val" x="211" y="81" text-anchor="middle">12</text><text class="gx-cost" x="258" y="68" text-anchor="end">1</text><text class="gx-val" x="245" y="81" text-anchor="middle">9</text><text class="gx-tag" x="28" y="102">S</text><text class="gx-cost" x="54" y="102" text-anchor="end">1</text><text class="gx-val" x="41" y="115" text-anchor="middle">0</text><text class="gx-cost" x="88" y="102" text-anchor="end">5</text><text class="gx-val" x="75" y="115" text-anchor="middle">5</text><text class="gx-cost" x="122" y="102" text-anchor="end">9</text><text class="gx-val" x="109" y="115" text-anchor="middle">14</text><text class="gx-cost" x="156" y="102" text-anchor="end">9</text><text class="gx-cost" x="190" y="102" text-anchor="end">9</text><text class="gx-val" x="177" y="115" text-anchor="middle">20</text><text class="gx-cost" x="224" y="102" text-anchor="end">5</text><text class="gx-val" x="211" y="115" text-anchor="middle">15</text><text class="gx-cost" x="258" y="102" text-anchor="end">1</text><text class="gx-val" x="245" y="115" text-anchor="middle">10</text><text class="gx-cost" x="54" y="136" text-anchor="end">1</text><text class="gx-val" x="41" y="149" text-anchor="middle">1</text><text class="gx-cost" x="88" y="136" text-anchor="end">5</text><text class="gx-val" x="75" y="149" text-anchor="middle">6</text><text class="gx-cost" x="122" y="136" text-anchor="end">9</text><text class="gx-val" x="109" y="149" text-anchor="middle">15</text><text class="gx-cost" x="156" y="136" text-anchor="end">9</text><text class="gx-cost" x="190" y="136" text-anchor="end">9</text><text class="gx-cost" x="224" y="136" text-anchor="end">5</text><text class="gx-tag" x="232" y="136">T</text><text class="gx-cost" x="258" y="136" text-anchor="end">1</text><text class="gx-val" x="245" y="149" text-anchor="middle">11</text><text class="gx-cost" x="54" y="170" text-anchor="end">1</text><text class="gx-val" x="41" y="183" text-anchor="middle">2</text><text class="gx-cost" x="88" y="170" text-anchor="end">5</text><text class="gx-val" x="75" y="183" text-anchor="middle">7</text><text class="gx-cost" x="122" y="170" text-anchor="end">5</text><text class="gx-val" x="109" y="183" text-anchor="middle">10</text><text class="gx-cost" x="156" y="170" text-anchor="end">9</text><text class="gx-val" x="143" y="183" text-anchor="middle">19</text><text class="gx-cost" x="190" y="170" text-anchor="end">5</text><text class="gx-cost" x="224" y="170" text-anchor="end">5</text><text class="gx-cost" x="258" y="170" text-anchor="end">1</text><text class="gx-cost" x="54" y="204" text-anchor="end">1</text><text class="gx-val" x="41" y="217" text-anchor="middle">3</text><text class="gx-cost" x="88" y="204" text-anchor="end">1</text><text class="gx-val" x="75" y="217" text-anchor="middle">4</text><text class="gx-cost" x="122" y="204" text-anchor="end">1</text><text class="gx-val" x="109" y="217" text-anchor="middle">5</text><text class="gx-cost" x="156" y="204" text-anchor="end">5</text><text class="gx-val" x="143" y="217" text-anchor="middle">10</text><text class="gx-cost" x="190" y="204" text-anchor="end">1</text><text class="gx-val" x="177" y="217" text-anchor="middle">11</text><text class="gx-cost" x="224" y="204" text-anchor="end">1</text><text class="gx-cost" x="258" y="204" text-anchor="end">1</text></svg>

    <!-- /gen -->

    <!-- gen 13 -->

    <span class="viz-legend"><span><i class="gx-key-s"></i>S ההתחלה, T היעד</span><span><i class="gx-key gx-t1"></i>כביש, 1 עד 3</span><span><i class="gx-key gx-t2"></i>בוץ, 4 עד 6</span><span><i class="gx-key gx-t3"></i>הר, 7 עד 9</span><span><i class="gx-key-path"></i>המסלול</span><span><i class="gx-key-ghost"></i>המסלול עם הכי מעט צעדים (BFS)</span></span>

    <!-- /gen -->

    <!-- gen 14 -->

    | המסלול | צעדים | העלויות של התאים שנכנסים אליהם | העלות |
    |:--|:-:|:--|:-:|
    | ‏BFS : הכי מעט צעדים | ‏7 | ‏<span dir="ltr">1 + 5 + 9 + 9 + 9 + 5 + 1</span> | ‏39 |
    | ‏Dijkstra : הכי זול | ‏11 | ‏<span dir="ltr">1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1</span> | ‏11 |
    | הזול ביותר מבין המסלולים של 7 צעדים | ‏7 | — | ‏39 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מתחילים :** ‏\( \text{cost}[S] = 0 \), כל השאר \( \infty \), והערימה מחזיקה את
       \( (0, S) \). העלות של \( S \) עצמו לא משולמת.
    2. **מוציאים את הקטן מהערימה :** את \( (d, r, c) \). רשומה ישנה (\( d > \text{cost}[r][c] \)) :
       מדלגים.
    3. **היעד :** אם \( (r, c) = T \), התשובה \( d \).
    4. **משחררים :** לכל שכן \( (a, b) \) שאינו קיר, אם \( d + w(a, b) < \text{cost}[a][b] \), כותבים את
       העלות החדשה ודוחפים \( (\text{cost}[a][b], a, b) \).
    5. **ערימה ריקה :** אין מסלול, <span dir="ltr">−1</span>.

    </div>

    על הדוגמה, כל הוצאה מהערימה בשורה. העלויות עולות לאט לאורך הכביש, למעלה ולמטה, ותא הבוץ
    \( (2, 1) \) שליד \( S \), שנדחף כבר בצעד 1 בעלות 5, יוצא רק בצעד 11, כשהעלות הקטנה בערימה הגיעה ל-5 : לפניו
    יוצאים כל תאי הכביש בעלות 0 עד 4, ו-\( (0, 3) \) בעלות 5 (בשוויון, השורה הקטנה קודם). ‏\( T \) יוצא בצעד 25 עם 11 :

    <!-- gen 15 -->

    | הצעד | יוצא מהערימה (תא=עלות) | נכנסים לערימה (תא=עלות) | בערימה אחרי |
    |:-:|:-:|:--|:-:|
    | ‏1 | ‏<span dir="ltr">(2,0)=0</span> | ‏<span dir="ltr">(1,0)=1&nbsp; (3,0)=1&nbsp; (2,1)=5</span> | ‏3 |
    | ‏2 | ‏<span dir="ltr">(1,0)=1</span> | ‏<span dir="ltr">(0,0)=2&nbsp; (1,1)=6</span> | ‏4 |
    | ‏3 | ‏<span dir="ltr">(3,0)=1</span> | ‏<span dir="ltr">(4,0)=2&nbsp; (3,1)=6</span> | ‏5 |
    | ‏4 | ‏<span dir="ltr">(0,0)=2</span> | ‏<span dir="ltr">(0,1)=3</span> | ‏5 |
    | ‏5 | ‏<span dir="ltr">(4,0)=2</span> | ‏<span dir="ltr">(5,0)=3&nbsp; (4,1)=7</span> | ‏6 |
    | ‏6 | ‏<span dir="ltr">(0,1)=3</span> | ‏<span dir="ltr">(0,2)=4</span> | ‏6 |
    | ‏7 | ‏<span dir="ltr">(5,0)=3</span> | ‏<span dir="ltr">(5,1)=4</span> | ‏6 |
    | ‏8 | ‏<span dir="ltr">(0,2)=4</span> | ‏<span dir="ltr">(1,2)=9&nbsp; (0,3)=5</span> | ‏7 |
    | ‏9 | ‏<span dir="ltr">(5,1)=4</span> | ‏<span dir="ltr">(5,2)=5</span> | ‏7 |
    | ‏10 | ‏<span dir="ltr">(0,3)=5</span> | ‏<span dir="ltr">(1,3)=14&nbsp; (0,4)=6</span> | ‏8 |
    | ‏11 | ‏<span dir="ltr">(2,1)=5</span> | ‏<span dir="ltr">(2,2)=14</span> | ‏8 |
    | ‏12 | ‏<span dir="ltr">(5,2)=5</span> | ‏<span dir="ltr">(4,2)=10&nbsp; (5,3)=10</span> | ‏9 |
    | ‏13 | ‏<span dir="ltr">(0,4)=6</span> | ‏<span dir="ltr">(1,4)=11&nbsp; (0,5)=7</span> | ‏10 |
    | ‏14 | ‏<span dir="ltr">(1,1)=6</span> | אף תא : לכל השכנים כבר יש עלות קטנה או שווה | ‏9 |
    | ‏15 | ‏<span dir="ltr">(3,1)=6</span> | ‏<span dir="ltr">(3,2)=15</span> | ‏9 |
    | ‏16 | ‏<span dir="ltr">(0,5)=7</span> | ‏<span dir="ltr">(1,5)=12&nbsp; (0,6)=8</span> | ‏10 |
    | ‏17 | ‏<span dir="ltr">(4,1)=7</span> | אף תא : לכל השכנים כבר יש עלות קטנה או שווה | ‏9 |
    | ‏18 | ‏<span dir="ltr">(0,6)=8</span> | ‏<span dir="ltr">(1,6)=9</span> | ‏9 |
    | ‏19 | ‏<span dir="ltr">(1,2)=9</span> | אף תא : לכל השכנים כבר יש עלות קטנה או שווה | ‏8 |
    | ‏20 | ‏<span dir="ltr">(1,6)=9</span> | ‏<span dir="ltr">(2,6)=10</span> | ‏8 |
    | ‏21 | ‏<span dir="ltr">(2,6)=10</span> | ‏<span dir="ltr">(3,6)=11&nbsp; (2,5)=15</span> | ‏9 |
    | ‏22 | ‏<span dir="ltr">(4,2)=10</span> | ‏<span dir="ltr">(4,3)=19</span> | ‏9 |
    | ‏23 | ‏<span dir="ltr">(5,3)=10</span> | ‏<span dir="ltr">(5,4)=11</span> | ‏9 |
    | ‏24 | ‏<span dir="ltr">(1,4)=11</span> | ‏<span dir="ltr">(2,4)=20</span> | ‏9 |
    | ‏25 | ‏<span dir="ltr">(3,6)=11</span> | **היעד** : העלות הסופית | ‏8 |

    <!-- /gen -->

    **ומה משתנה בשמונה כיוונים.** רק השכנים. בשטח של הדוגמה הצעד באלכסון חוסך את שתי הפינות של
    הכביש העליון, והעלות יורדת ל-9, במסלול של 9 צעדים.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="cheapest_path" linenums="1" hl_lines="13 14 19"
        import heapq


        def cheapest_path(grid: list[str], s: tuple, t: tuple, diag: bool = False) -> int:
            """Dijkstra: grid[r][c] is the cost '1'..'9' of stepping into (r, c) and '#' a wall;
            the start's own cost is not paid. The least total cost from s to t, or -1."""
            m, n = len(grid), len(grid[0])
            inf = float("inf")
            cost = [[inf] * n for _ in range(m)]
            cost[s[0]][s[1]] = 0                                    # (1)!
            heap = [(0, s[0], s[1])]
            while heap:
                d, r, c = heapq.heappop(heap)                       # (2)!
                if d > cost[r][c]:
                    continue                                        # (3)!
                if (r, c) == t:
                    return d                                        # (4)!
                for a, b in moves(grid, r, c, diag, wall="#"):
                    if grid[a][b] != "#" and d + int(grid[a][b]) < cost[a][b]:   # (5)!
                        cost[a][b] = d + int(grid[a][b])
                        heapq.heappush(heap, (cost[a][b], a, b))
            return -1
        ```

        1. העלות של \( S \) עצמו לא משולמת : מתחילים מ-0, לא מ-`int(grid[s])`.
        2. השלשה עם העלות הקטנה ביותר ; בשוויון, השורה הקטנה ואחר כך העמודה, כי `heapq` משווה את
           השלשה כולה.
        3. רשומה ישנה : התא כבר יצא בעלות קטנה יותר. עם עלות לכל תא זה לא קורה אף פעם (ההוכחה
           למטה), אבל זה כן קורה כשהעלות היא של הצעד.
        4. היעד יוצא מהערימה : העלות שלו סופית. לעצור כשהוא **נדחף** לא היה בטוח באופן כללי.
        5. השחרור. ‏`moves` של סעיף א עם `wall="#"`, כך שגם הכלל של האלכסון מתייחס ל-`#`.

    === "SystemVerilog"
        ```systemverilog title="function cheapest_path" linenums="1" hl_lines="17 18 25"
        typedef struct { int d, r, c; } entry_t;    // an entry of the priority queue

        // Dijkstra: the character of a cell is the cost "1".."9" of stepping into it and "#" a
        // wall; the start's own cost is not paid. The least total cost from s to t, or -1
        function automatic int cheapest_path(string grid[], cell_t s, cell_t t, bit diag);
          int m = grid.size(), n = grid[0].len(), cost[][], nd, pos;
          entry_t pq[$], e;
          cell_t nb[$], v;
          cost = new[m];
          foreach (cost[i]) begin
            cost[i] = new[n];
            foreach (cost[i][j]) cost[i][j] = -1;                        // -1 stands for "no cost yet"
          end
          cost[s.r][s.c] = 0;                                            // (1)!
          pq.push_back('{0, s.r, s.c});
          while (pq.size() > 0) begin
            e = pq.pop_front();                                          // (2)!
            if (e.d > cost[e.r][e.c]) continue;                          // (3)!
            if (e.r == t.r && e.c == t.c) return e.d;
            moves(grid, e.r, e.c, diag, "#", nb);
            foreach (nb[i]) begin
              v = nb[i];
              if (grid[v.r].getc(v.c) == "#") continue;
              nd = e.d + (grid[v.r].getc(v.c) - "0");
              if (cost[v.r][v.c] < 0 || nd < cost[v.r][v.c]) begin       // (4)!
                cost[v.r][v.c] = nd;
                pos = 0;                                                 // (5)!
                while (pos < pq.size() && (pq[pos].d < nd || (pq[pos].d == nd && (pq[pos].r < v.r || (pq[pos].r == v.r && pq[pos].c < v.c))))) pos++;
                pq.insert(pos, '{nd, v.r, v.c});
              end
            end
          end
          return -1;
        endfunction
        ```

        1. העלות של \( S \) עצמו לא משולמת.
        2. אין ערימה מובנית ב-SystemVerilog, ולכן התור `pq` נשמר **ממוין** לפי (עלות, שורה, עמודה),
           ו-`pop_front` נותן את הקטן ביותר, כמו `heappop`.
        3. רשומה ישנה, כמו ב-Python ; עם עלות לכל תא היא לא מופיעה.
        4. השחרור. ‏<span dir="ltr">−1</span> מייצג \( \infty \), ולכן הבדיקה היא "אין עלות, או עלות
           גדולה יותר". ‏`getc - "0"` הופך את התו לספרה.
        5. ההכנסה למקום הממוין : \( O(|pq|) \) לכל הכנסה במקום \( O(\log |pq|) \), כמו ב-0067. ללוח
           של כמה מאות תאים זה לא מורגש.

    #### למה זה נכון { .sol-proof }

    **השמורה של Dijkstra :** כשתא \( u \) יוצא מהערימה עם \( d = \text{cost}[u] \) (רשומה לא ישנה),
    \( d \) היא העלות הקטנה ביותר של מסלול מ-\( S \) ל-\( u \). באינדוקציה על סדר היציאה, בהנחה
    שהעלויות אינן שליליות.

    - **הבסיס :** הראשון שיוצא הוא \( S \) עם 0, ואין מסלול זול יותר.
    - **הצעד :** נניח שכל מי שיצא לפני \( u \) יצא עם העלות הנכונה. ניקח מסלול כלשהו \( P \)
      מ-\( S \) ל-\( u \), ונסתכל על התא **הראשון** בו שעוד לא יצא, \( x \) (יש כזה, כי \( u \) עצמו
      לא יצא). התא שלפניו, \( y \), יצא, וכשיצא שוחרר הצעד \( y \to x \), ולכן
      \( \text{cost}[x] \le \text{cost}[y] + w(x) \le \) העלות של \( P \) עד \( x \), שהיא לכל היותר
      העלות של \( P \) כולו, כי המשך המסלול מוסיף עלויות \( \ge 1 \). הרשומה של \( x \) נמצאת בערימה,
      ו-\( d \) הוא הקטן בערימה, ולכן \( d \le \text{cost}[x] \le |P| \). אף מסלול אינו זול מ-\( d \).

    **אין רשומות ישנות :** נניח ש-\( v \) נדחף לראשונה כש-\( u \) יצא, בעלות \( \text{cost}[u] + w(v) \).
    כל תא \( u' \) שיוצא אחרי \( u \) מקיים \( \text{cost}[u'] \ge \text{cost}[u] \) (היציאות לפי
    עלות לא יורדת, כמו בשמורה), ולכן \( \text{cost}[u'] + w(v) \ge \text{cost}[u] + w(v) \) : לא שיפור.
    כל תא נדחף פעם אחת, ובערימה לכל היותר \( RC \) רשומות. זה נכון רק כי לכל הצעדים אל \( v \) אותה
    עלות ; כשהעלות על הצעד (למשל אלכסון יקר יותר) השיפורים חוזרים, והשורה של הרשומה הישנה נחוצה.

    **סעיף א הוא המקרה הפרטי :** כשכל העלויות 1 העלות היא מספר הצעדים, ו-Dijkstra מוציא את התאים
    באותו סדר כמו BFS. התור של BFS כבר ממוין (השמורה של סעיף א), ולכן שם הוא מספיק, בלי הלוגריתם.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(RC \log(RC)) \). כל תא יוצא פעם אחת ומשחרר 4 או 8 שכנים, וכל דחיפה והוצאה עולות
      \( O(\log(RC)) \).
    - **זיכרון :** ‏\( O(RC) \) לעלויות ולערימה.
    - **הגרסה של SystemVerilog :** התור הממוין מכניס ב-\( O(|pq|) \), ולכן עד \( O((RC)^2) \) ; ערימה
      בינארית במערך מחזירה את הסיבוכיות של Python.

    **נסו בעצמכם.** השטח של הדוגמה. בחרו מברשת (קיר, או עלות מ-1 עד 9) וצבעו תאים בלחיצה או בגרירה.
    הצבע של תא אומר את סוג השטח, והמספר הקטן בפינה את העלות שלו. כל צעד הוא הוצאה אחת מהערימה,
    והערימה, ממוינת, מתחת ללוח. השוו את "קווי הגובה" של העלות לשכבות של סעיף א :

    <div class="explorer" data-kind="gridpath" data-mode="c" data-grid="1111111.1559551.1599951.1599951.1559551.1115111" data-s="2,0" data-t="3,6"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : בסעיף ב לסמן תאים במקום מצבים"
    ‏BFS שבו כל **תא** נכנס פעם אחת זורק מסלולים שהגיעו מאוחר יותר עם יותר שבירות. בלוח של 3 על 3
    של סעיף ב הוא מחזיר <span dir="ltr">−1</span> במקום 4. הסימון חייב להיות לפי המצב : מערך `seen`
    של \( R \times C \times (k + 1) \), או, כמו בקוד, הכי הרבה שבירות שנשארו לכל תא.

??? trap "מלכודת : BFS כשיש עלויות"
    "הפעם הראשונה שמגיעים לתא" היא הזולה ביותר רק כשלכל הצעדים אותה עלות. בשטח של סעיף ג, העלות
    של המסלול ש-BFS מוצא היא 39, והזול עולה 11. משקלים שווים : BFS ; משקלים 0 ו-1 : BFS
    עם deque ; משקלים חיוביים כלליים : Dijkstra.

??? trap "מלכודת : לשלם את העלות של S, או לשכוח את העלות של T"
    השאלה מגדירה את העלות כסכום על התאים **שנכנסים** אליהם. התחלה עם `cost[s] = int(grid[s])`
    מוסיפה את העלות של \( S \) לכל תשובה (בדוגמה 12 במקום 11), וסכום שעוצר לפני \( T \) מפספס את
    העלות שלו. בודקים על \( S = T \) : התשובה 0.

??? trap "מלכודת : לשכוח את הכלל של האלכסון"
    בלי הבדיקה של שני הקירות, שמונה כיוונים עוברים דרך קיר הזיגזג של הדוגמה, בין הפינות של שני
    קירות, ומקבלים 12 במקום 15. הכלל צריך להיות כתוב בשאלה ובקוד באותו מקום, בפונקציה אחת של
    "המהלכים מתא", כדי שכל הסעיפים ישתמשו בו.

??? trap "מלכודת : שורה ועמודה, x ו-y"
    התא הוא `grid[r][c]` : קודם השורה, ואחר כך העמודה. מי שכותב \( (x, y) \) ומתבלבל, או בודק את
    הגבול של השורה מול מספר העמודות, מקבל תשובות נכונות על לוח ריבועי ושגיאות על לוח מלבני כמו 7 על 9.
    ב-Python, `grid[-1]` אפילו לא נכשל : זו השורה האחרונה. הבדיקה של הגבולות באה **לפני** הגישה ללוח.

??? followup "שאלות המשך"
    - **הכלל האחר של האלכסון :** מה משתנה אם מותר לעבור באלכסון גם בין שני קירות שנוגעים בפינה?
      ומה אם להפך, אסור לחתוך אפילו פינה של קיר אחד?

        ??? fu-answer "תשובה"
            רק התנאי ב-`moves`. בלי הבדיקה, הזיגזג של הדוגמה כבר לא חוסם, והמסלול יורד מ-15 ל-12.
            בכלל המחמיר (אסור אם **אחד** מהשניים קיר, כמו רובוט שתופס מקום) התנאי הוא `or` במקום
            `and`. ‏BFS וההוכחה לא משתנים : הכלל רק קובע אילו קשתות יש בגרף.

    - **‏A\* במקום Dijkstra :** איך מוצאים את המסלול הזול מהר יותר, כשיודעים איפה היעד?

        ??? fu-answer "תשובה"
            מוציאים מהערימה לפי \( \text{cost}[v] + h(v) \), כש-\( h \) הוא הערכה של מה שנשאר : מספר
            הצעדים ל-\( T \) בלי קירות (מרחק מנהטן, \( |\Delta r| + |\Delta c| \), בארבעה כיוונים ; מרחק
            צ'בישב, \( \max(|\Delta r|, |\Delta c|) \), בשמונה) כפול העלות הקטנה ביותר של תא. ‏\( h \)
            כזה אף פעם לא מעריך יותר מדי, ולכן התשובה נשארת נכונה. בשטח של סעיף ג : 19 הוצאות במקום 25.

    - **‏0-1 BFS :** מה אם העלויות של התאים הן רק 0 ו-1?

        ??? fu-answer "תשובה"
            ‏deque במקום ערימה : תא שנכנסים אליו בעלות 0 נדחף לראש, ובעלות 1 לזנב. ה-deque נשאר ממוין
            עם שני ערכים סמוכים, כמו התור של BFS, והזמן \( O(RC) \) בלי לוגריתם. זה הפתרון של "כמה
            קירות **לפחות** צריך לשבור" (LeetCode 2290) : קיר עולה 1 ותא פתוח 0.

    - **כמה יעדים :** יש כמה תאי יעד, ומספיק להגיע לאחד מהם. מה משתנה?

        ??? fu-answer "תשובה"
            אותו BFS, שעוצר בפעם הראשונה ש**אחד** מהיעדים יוצא מהתור : הוא הקרוב ביותר. כשיש
            הרבה התחלות ויעד אחד, מריצים מ-\( T \) לאחור (בלוח הצעדים סימטריים), או מכניסים את כל
            ההתחלות לתור עם 0 לפני הלולאה (BFS מכמה מקורות).
