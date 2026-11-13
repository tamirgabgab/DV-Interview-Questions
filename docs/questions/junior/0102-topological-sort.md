---
id: 102
title: מיון טופולוגי – באיזה סדר להריץ משימות תלויות, ומתי אין סדר כזה
level: junior
difficulty: medium
kind: code
tags: [algorithms, sorting, bfs, python, systemverilog]
source: "LeetCode 207 ו-210 (Course Schedule), האלגוריתם של Kahn מ-1962, ושיטת הנתיב הקריטי (CPM) לתזמון פרויקטים"
added: 2026-11-13
---

## השאלה

יש \( n \) משימות, ממוספרות \( 0 \) עד \( n - 1 \), ורשימה של **תלויות** : הזוג \( (a, b) \) אומר
שהמשימה \( b \) רצה **אחרי** \( a \), כלומר \( b \) לא יכולה להתחיל לפני ש-\( a \) הסתיימה. כתבו
פונקציה שמחזירה סדר להרצת כל המשימות שמכבד את כל התלויות, או מודיעה שאין סדר כזה, כי בתלויות יש
מעגל.

**ההקשר באימות :** זרימה של רגרסיה היא בדיוק רשימה כזו. הקומפילציה של ה-RTL צריכה את הספריות,
סביבת האימות צריכה את מודל הרגיסטרים, ה-elaboration צריך את שתיהן, וכל בדיקה צריכה את
הקונפיגורציה שלה. כך גם הסדר של שלבי bring-up, או של כתיבות קונפיגורציה שבהן רגיסטר אחד נכתב רק
אחרי שאחר הוגדר. תלות מעגלית, למשל מודל רגיסטרים שנוצר מה-RTL אחרי ה-elaboration שצריך אותו, היא
הסיבה הקלאסית לזרימה שנתקעת : כל משימה מחכה לאחרת, ואף אחת לא מתחילה.

הדוגמה בכל הסעיפים היא זרימה של שבע משימות, A עד G. חץ מ-A ל-B אומר ש-B רצה אחרי A :

<!-- gen 0 -->

<svg class="figure ts-fig" viewBox="0 0 464 184" style="max-width:29rem" role="img" aria-label="הדוגמה : שבע משימות A עד G. חץ מ-A ל-B אומר ש-B רצה אחרי A. ‏B ו-C אחרי A, ‏C גם אחרי E, ‏D אחרי B ו-C, ‏F אחרי D ו-G אחרי F"><g class="ts-edge"><title>A → B: B after A</title><line x1="60.0" y1="52.0" x2="115.0" y2="52.0"/><path class="ts-head" d="M122.0,52.0 L115.0,56.5 L115.0,47.5 Z"/></g><g class="ts-edge"><title>A → C: C after A</title><line x1="56.2" y1="62.4" x2="120.5" y2="117.1"/><path class="ts-head" d="M125.8,121.6 L117.6,120.5 L123.4,113.7 Z"/></g><g class="ts-edge"><title>E → C: C after E</title><line x1="60.0" y1="132.0" x2="115.0" y2="132.0"/><path class="ts-head" d="M122.0,132.0 L115.0,136.5 L115.0,127.5 Z"/></g><g class="ts-edge"><title>B → D: D after B</title><line x1="152.7" y1="58.3" x2="210.8" y2="83.0"/><path class="ts-head" d="M217.3,85.7 L209.1,87.1 L212.6,78.9 Z"/></g><g class="ts-edge"><title>C → D: D after C</title><line x1="152.7" y1="125.7" x2="210.8" y2="101.0"/><path class="ts-head" d="M217.3,98.3 L212.6,105.1 L209.1,96.9 Z"/></g><g class="ts-edge"><title>D → F: F after D</title><line x1="248.0" y1="92.0" x2="303.0" y2="92.0"/><path class="ts-head" d="M310.0,92.0 L303.0,96.5 L303.0,87.5 Z"/></g><g class="ts-edge"><title>F → G: G after F</title><line x1="342.0" y1="92.0" x2="397.0" y2="92.0"/><path class="ts-head" d="M404.0,92.0 L397.0,96.5 L397.0,87.5 Z"/></g><g class="ts-node"><title>task A</title><circle cx="44" cy="52" r="16"/><text x="44" y="57" text-anchor="middle">A</text></g><g class="ts-node"><title>task B</title><circle cx="138" cy="52" r="16"/><text x="138" y="57" text-anchor="middle">B</text></g><g class="ts-node"><title>task C</title><circle cx="138" cy="132" r="16"/><text x="138" y="137" text-anchor="middle">C</text></g><g class="ts-node"><title>task D</title><circle cx="232" cy="92" r="16"/><text x="232" y="97" text-anchor="middle">D</text></g><g class="ts-node"><title>task E</title><circle cx="44" cy="132" r="16"/><text x="44" y="137" text-anchor="middle">E</text></g><g class="ts-node"><title>task F</title><circle cx="326" cy="92" r="16"/><text x="326" y="97" text-anchor="middle">F</text></g><g class="ts-node"><title>task G</title><circle cx="420" cy="92" r="16"/><text x="420" y="97" text-anchor="middle">G</text></g></svg>

<!-- /gen -->

<!-- gen 1 -->

| המשימה | מה היא עושה | רצה אחרי |
|:-:|---|:-:|
| ‏A | קומפילציה של הספריות המשותפות | אף אחת |
| ‏B | קומפילציה של ה-RTL | ‏A |
| ‏C | קומפילציה של סביבת האימות | ‏A, E |
| ‏D | ‏elaboration של ה-RTL עם הסביבה | ‏B, C |
| ‏E | יצירת מודל הרגיסטרים (RAL) מהמפרט | אף אחת |
| ‏F | בדיקת sanity קצרה | ‏D |
| ‏G | הרגרסיה המלאה | ‏F |

<!-- /gen -->

בקוד המשימות הן מספרים : A היא 0, ‏B היא 1, וכן הלאה עד G שהיא 6. התלויות של הדוגמה הן
<span dir="ltr">(0, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 5), (5, 6)</span>.

- **סעיף א – Kahn :** מצאו סדר בעזרת מונה לכל משימה של המשימות שהיא עוד מחכה להן, וזהו מעגל.
- **סעיף ב – חיפוש לעומק :** אותה שאלה בחיפוש לעומק (DFS). מה צריך כדי שהחיפוש יבחין במעגל, ורק
  במעגל?
- **סעיף ג – הנתיב הקריטי :** לכל משימה יש משך, ומשימות שאין תלות ביניהן יכולות לרוץ במקביל, בלי
  הגבלה על מספר המריצים. מתי כל המשימות נגמרות, ואילו משימות קובעות את הזמן הזה?

??? interviewer "מה המראיין בודק"
    - **מהבעיה לגרף :** האם המועמד רואה שתלויות הן גרף מכוון, ושהשאלה היא סדר שבו כל חץ הולך
      ממשימה מוקדמת למאוחרת.
    - **סדר אחד מתוך כמה :** האם הוא מבין שבדרך כלל יש כמה סדרים נכונים, ושבודק צריך לבדוק את
      התכונה ולא להשוות לסדר אחד.
    - **מעגל :** האם הוא מזהה מתי אין סדר, ויכול להראות את המעגל עצמו ולא רק להגיד "נכשל".
    - **שתי דרכים :** מונים של תלויות ותור, או חיפוש לעומק, ולמה בחיפוש "ביקרנו או לא" לא מספיק.
    - **מסדר לזמן :** כשיש משכים ומקביליות, האם הוא רואה שהזמן הכולל נקבע על ידי שרשרת אחת של
      תלויות, ומחשב אותו באותו מעבר.

---

### סעיף א – Kahn : דרגות כניסה ותור

??? tip "רמז 1"
    איזו משימה יכולה לרוץ ראשונה? ומה משתנה אצל שאר המשימות אחרי שהיא הסתיימה?

??? tip "רמז 2"
    לכל משימה ספרו כמה משימות עוד צריכות להסתיים לפניה. משימה שהמונה שלה 0 מוכנה לרוץ. מה אומר
    מצב שבו נשארו משימות, ואף אחת מהן לא מוכנה?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        לכל משימה סופרים את **דרגת הכניסה** שלה, מספר המשימות שהיא מחכה להן. תור מחזיק את
        המשימות שהדרגה שלהן 0 ; מוציאים אחת, מוסיפים אותה לסדר, ומורידים ב-1 את הדרגה של כל
        משימה שרצה אחריה, ומשימה שהגיעה ל-0 נכנסת לתור. אם יצאו כל \( n \) המשימות זה הסדר, ואם
        התור התרוקן קודם יש מעגל. בדוגמה : <span dir="ltr">A, E, B, C, D, F, G</span>.

    <!-- cost: זמן \( O(n + m) \) | זיכרון \( O(n + m) \) -->

    #### הרעיון { .sol-idea }

    **מונחים.** התלויות הן **גרף מכוון** : המשימות הן הצמתים, וכל תלות היא חץ \( a \to b \),
    "‏\( b \) אחרי \( a \)". יש \( m \) חצים. ‏\( b \) היא **עוקבת** של \( a \) כשיש חץ
    \( a \to b \). **דרגת הכניסה** של משימה היא מספר החצים שנכנסים אליה, כלומר מספר המשימות שהיא
    מחכה להן. **מיון טופולוגי** הוא סדר של כל המשימות שבו כל חץ הולך ממשימה מוקדמת למשימה מאוחרת.

    **הרעיון של Kahn.** משימה עם דרגת כניסה 0 לא מחכה לאף אחת, ולכן אפשר להריץ אותה ראשונה. אחרי
    שהיא רצה היא כבר לא מעכבת אף אחת, ולכן מוחקים אותה מהגרף : מורידים ב-1 את דרגת הכניסה של כל
    עוקבת שלה. אולי עכשיו יש משימות חדשות עם דרגה 0, ושוב לוקחים אחת. **תור** (FIFO) מחזיק את
    המשימות המוכנות, אלה שהדרגה שלהן 0 ועוד לא רצו.

    **מתי נתקעים.** אם התור התרוקן ונשארו משימות, לכל אחת מהן דרגה גדולה מ-0, והדרגה סופרת רק חצים
    ממשימות שעוד לא רצו : כל אחת מחכה לאחת אחרת מהנשארות. הולכים אחורה מאחת מהן, בכל צעד אל משימה
    נשארת שהיא מחכה לה. מספר המשימות סופי, ולכן ההליכה חוזרת למשימה שכבר ראתה, וזה **מעגל**. לכן
    "התור התרוקן לפני שכולן יצאו" שקול ל"יש מעגל".

    הדוגמה לפי **סבבים** : בכל עמודה המשימות שהדרגה שלהן מגיעה ל-0 יחד, וליד כל משימה הדרגה שלה
    בהתחלה. ‏A ו-E מוכנות מיד, ‏B ו-C אחרי שתיהן, ואחר כך D, ‏F ו-G אחת אחרי השנייה :

    <!-- gen 2 -->

    <svg class="figure ts-fig" viewBox="0 0 464 184" style="max-width:29rem" role="img" aria-label="הדוגמה לפי הסבבים של Kahn : בסבב 1 המשימות A ו-E, בלי תלות. בסבב 2 B ו-C, בסבב 3 D, בסבב 4 F ובסבב 5 G. ליד כל משימה דרגת הכניסה שלה בהתחלה"><rect class="ts-band" x="4" y="22" width="80" height="158" rx="8"/><g class="ts-round"><circle cx="44" cy="12" r="9"/><text x="44" y="16" text-anchor="middle">1</text></g><rect class="ts-band is-alt" x="98" y="22" width="80" height="158" rx="8"/><g class="ts-round"><circle cx="138" cy="12" r="9"/><text x="138" y="16" text-anchor="middle">2</text></g><rect class="ts-band" x="192" y="22" width="80" height="158" rx="8"/><g class="ts-round"><circle cx="232" cy="12" r="9"/><text x="232" y="16" text-anchor="middle">3</text></g><rect class="ts-band is-alt" x="286" y="22" width="80" height="158" rx="8"/><g class="ts-round"><circle cx="326" cy="12" r="9"/><text x="326" y="16" text-anchor="middle">4</text></g><rect class="ts-band" x="380" y="22" width="80" height="158" rx="8"/><g class="ts-round"><circle cx="420" cy="12" r="9"/><text x="420" y="16" text-anchor="middle">5</text></g><g class="ts-edge"><title>A → B: B after A</title><line x1="60.0" y1="52.0" x2="115.0" y2="52.0"/><path class="ts-head" d="M122.0,52.0 L115.0,56.5 L115.0,47.5 Z"/></g><g class="ts-edge"><title>A → C: C after A</title><line x1="56.2" y1="62.4" x2="120.5" y2="117.1"/><path class="ts-head" d="M125.8,121.6 L117.6,120.5 L123.4,113.7 Z"/></g><g class="ts-edge"><title>E → C: C after E</title><line x1="60.0" y1="132.0" x2="115.0" y2="132.0"/><path class="ts-head" d="M122.0,132.0 L115.0,136.5 L115.0,127.5 Z"/></g><g class="ts-edge"><title>B → D: D after B</title><line x1="152.7" y1="58.3" x2="210.8" y2="83.0"/><path class="ts-head" d="M217.3,85.7 L209.1,87.1 L212.6,78.9 Z"/></g><g class="ts-edge"><title>C → D: D after C</title><line x1="152.7" y1="125.7" x2="210.8" y2="101.0"/><path class="ts-head" d="M217.3,98.3 L212.6,105.1 L209.1,96.9 Z"/></g><g class="ts-edge"><title>D → F: F after D</title><line x1="248.0" y1="92.0" x2="303.0" y2="92.0"/><path class="ts-head" d="M310.0,92.0 L303.0,96.5 L303.0,87.5 Z"/></g><g class="ts-edge"><title>F → G: G after F</title><line x1="342.0" y1="92.0" x2="397.0" y2="92.0"/><path class="ts-head" d="M404.0,92.0 L397.0,96.5 L397.0,87.5 Z"/></g><g class="ts-node is-src"><title>task A</title><circle cx="44" cy="52" r="16"/><text x="44" y="57" text-anchor="middle">A</text></g><g class="ts-badge is-zero"><title>in-degree of A: 0</title><rect x="49" y="21" width="20" height="17" rx="5"/><text x="59" y="34" text-anchor="middle">0</text></g><g class="ts-node"><title>task B</title><circle cx="138" cy="52" r="16"/><text x="138" y="57" text-anchor="middle">B</text></g><g class="ts-badge"><title>in-degree of B: 1</title><rect x="143" y="21" width="20" height="17" rx="5"/><text x="153" y="34" text-anchor="middle">1</text></g><g class="ts-node"><title>task C</title><circle cx="138" cy="132" r="16"/><text x="138" y="137" text-anchor="middle">C</text></g><g class="ts-badge"><title>in-degree of C: 2</title><rect x="143" y="101" width="20" height="17" rx="5"/><text x="153" y="114" text-anchor="middle">2</text></g><g class="ts-node"><title>task D</title><circle cx="232" cy="92" r="16"/><text x="232" y="97" text-anchor="middle">D</text></g><g class="ts-badge"><title>in-degree of D: 2</title><rect x="237" y="61" width="20" height="17" rx="5"/><text x="247" y="74" text-anchor="middle">2</text></g><g class="ts-node is-src"><title>task E</title><circle cx="44" cy="132" r="16"/><text x="44" y="137" text-anchor="middle">E</text></g><g class="ts-badge is-zero"><title>in-degree of E: 0</title><rect x="49" y="101" width="20" height="17" rx="5"/><text x="59" y="114" text-anchor="middle">0</text></g><g class="ts-node"><title>task F</title><circle cx="326" cy="92" r="16"/><text x="326" y="97" text-anchor="middle">F</text></g><g class="ts-badge"><title>in-degree of F: 1</title><rect x="331" y="61" width="20" height="17" rx="5"/><text x="341" y="74" text-anchor="middle">1</text></g><g class="ts-node"><title>task G</title><circle cx="420" cy="92" r="16"/><text x="420" y="97" text-anchor="middle">G</text></g><g class="ts-badge"><title>in-degree of G: 1</title><rect x="425" y="61" width="20" height="17" rx="5"/><text x="435" y="74" text-anchor="middle">1</text></g></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="ts-key-src"></i>דרגת כניסה 0 : אפשר להריץ מיד</span><span><i class="ts-key-badge"></i>דרגת הכניסה : כמה משימות עוד צריכות להסתיים לפניה</span><span><i class="ts-key-band"></i>סבב : המשימות שהדרגה שלהן מגיעה ל-0 יחד</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סופרים דרגות :** לכל חץ \( (a, b) \) מוסיפים את \( b \) לרשימת העוקבות של \( a \), ו-
       \( \mathrm{indeg}[b] \) עולה ב-1.
    2. **התור ההתחלתי :** כל המשימות עם דרגה 0, לפי המספר שלהן.
    3. **מוציאים מראש התור :** את \( u \), ומוסיפים אותה לסוף הסדר.
    4. **מורידים דרגות :** לכל עוקבת \( v \) של \( u \), ‏\( \mathrm{indeg}[v] \) יורד ב-1. אם הגיע
       ל-0, ‏\( v \) נכנסת לזנב התור.
    5. **הסוף :** כשהתור ריק, אם יש בסדר \( n \) משימות מחזירים אותו, ואחרת `None` : יש מעגל.

    </div>

    על הדוגמה. בכל שורה משימה אחת שיוצאת מהתור, הדרגות שהיא מורידה (מה היה ומה נהיה), התור אחרי
    זה, והסדר עד עכשיו :

    <!-- gen 4 -->

    | הצעד | יוצאת מהתור | הדרגות שיורדות | התור אחרי | הסדר עד עכשיו |
    |:-:|:-:|---|:-:|:-:|
    | ‏1 | ‏A | ‏B : <span dir="ltr">1 → 0</span>, נכנסת לתור; ‏C : <span dir="ltr">2 → 1</span> | ‏<span dir="ltr">E B</span> | ‏<span dir="ltr">A</span> |
    | ‏2 | ‏E | ‏C : <span dir="ltr">1 → 0</span>, נכנסת לתור | ‏<span dir="ltr">B C</span> | ‏<span dir="ltr">A E</span> |
    | ‏3 | ‏B | ‏D : <span dir="ltr">2 → 1</span> | ‏<span dir="ltr">C</span> | ‏<span dir="ltr">A E B</span> |
    | ‏4 | ‏C | ‏D : <span dir="ltr">1 → 0</span>, נכנסת לתור | ‏<span dir="ltr">D</span> | ‏<span dir="ltr">A E B C</span> |
    | ‏5 | ‏D | ‏F : <span dir="ltr">1 → 0</span>, נכנסת לתור | ‏<span dir="ltr">F</span> | ‏<span dir="ltr">A E B C D</span> |
    | ‏6 | ‏F | ‏G : <span dir="ltr">1 → 0</span>, נכנסת לתור | ‏<span dir="ltr">G</span> | ‏<span dir="ltr">A E B C D F</span> |
    | ‏7 | ‏G | אין לה עוקבות | ריק | ‏<span dir="ltr">A E B C D F G</span> |

    <!-- /gen -->

    הסדר <span dir="ltr">A, E, B, C, D, F, G</span>. זה לא הסדר היחיד : A ו-E יכולות להתחלף, וגם B
    ו-C, ו-B יכולה לרוץ גם לפני E. בסך הכול יש לדוגמה 5 סדרים נכונים, ו-Kahn מחזיר אחד מהם,
    לפי הסדר שבו המשימות נכנסות לתור.

    **ומה אם יש מעגל?** נניח שמודל הרגיסטרים E נוצר מה-RTL אחרי ה-elaboration, כלומר נוסף החץ
    \( D \to E \). ‏A ו-B יוצאות מהתור, ואז התור ריק :

    <!-- gen 5 -->

    <svg class="figure ts-fig" viewBox="0 0 464 202" style="max-width:29rem" role="img" aria-label="הדוגמה עם עוד חץ, מ-D ל-E : ‏A ו-B יוצאות מהתור, ואז התור ריק. חמש משימות נשארות עם דרגת כניסה 1, וביניהן המעגל C, D, E ובחזרה ל-C"><g class="ts-edge is-done"><title>A → B: B after A</title><line x1="60.0" y1="52.0" x2="115.0" y2="52.0"/><path class="ts-head" d="M122.0,52.0 L115.0,56.5 L115.0,47.5 Z"/></g><g class="ts-edge is-done"><title>A → C: C after A</title><line x1="56.2" y1="62.4" x2="120.5" y2="117.1"/><path class="ts-head" d="M125.8,121.6 L117.6,120.5 L123.4,113.7 Z"/></g><g class="ts-edge is-cycle"><title>E → C: C after E</title><line x1="60.0" y1="132.0" x2="115.0" y2="132.0"/><path class="ts-head" d="M122.0,132.0 L115.0,136.5 L115.0,127.5 Z"/></g><g class="ts-edge is-done"><title>B → D: D after B</title><line x1="152.7" y1="58.3" x2="210.8" y2="83.0"/><path class="ts-head" d="M217.3,85.7 L209.1,87.1 L212.6,78.9 Z"/></g><g class="ts-edge is-cycle"><title>C → D: D after C</title><line x1="152.7" y1="125.7" x2="210.8" y2="101.0"/><path class="ts-head" d="M217.3,98.3 L212.6,105.1 L209.1,96.9 Z"/></g><g class="ts-edge"><title>D → F: F after D</title><line x1="248.0" y1="92.0" x2="303.0" y2="92.0"/><path class="ts-head" d="M310.0,92.0 L303.0,96.5 L303.0,87.5 Z"/></g><g class="ts-edge"><title>F → G: G after F</title><line x1="342.0" y1="92.0" x2="397.0" y2="92.0"/><path class="ts-head" d="M404.0,92.0 L397.0,96.5 L397.0,87.5 Z"/></g><g class="ts-edge is-cycle"><title>D → E: E after D</title><path d="M223.5,105.5 Q150,222 61.5,146.9" fill="none"/><path class="ts-head" d="M56.2,142.4 L64.4,143.5 L58.6,150.3 Z"/></g><g class="ts-node is-out"><title>task A</title><circle cx="44" cy="52" r="16"/><text x="44" y="57" text-anchor="middle">A</text></g><g class="ts-badge is-zero"><title>in-degree of A: 0</title><rect x="49" y="21" width="20" height="17" rx="5"/><text x="59" y="34" text-anchor="middle">0</text></g><g class="ts-node is-out"><title>task B</title><circle cx="138" cy="52" r="16"/><text x="138" y="57" text-anchor="middle">B</text></g><g class="ts-badge is-zero"><title>in-degree of B: 0</title><rect x="143" y="21" width="20" height="17" rx="5"/><text x="153" y="34" text-anchor="middle">0</text></g><g class="ts-node is-cycle"><title>task C</title><circle cx="138" cy="132" r="16"/><text x="138" y="137" text-anchor="middle">C</text></g><g class="ts-badge"><title>in-degree of C: 1</title><rect x="143" y="101" width="20" height="17" rx="5"/><text x="153" y="114" text-anchor="middle">1</text></g><g class="ts-node is-cycle"><title>task D</title><circle cx="232" cy="92" r="16"/><text x="232" y="97" text-anchor="middle">D</text></g><g class="ts-badge"><title>in-degree of D: 1</title><rect x="237" y="61" width="20" height="17" rx="5"/><text x="247" y="74" text-anchor="middle">1</text></g><g class="ts-node is-cycle"><title>task E</title><circle cx="44" cy="132" r="16"/><text x="44" y="137" text-anchor="middle">E</text></g><g class="ts-badge"><title>in-degree of E: 1</title><rect x="49" y="101" width="20" height="17" rx="5"/><text x="59" y="114" text-anchor="middle">1</text></g><g class="ts-node is-stuck"><title>task F</title><circle cx="326" cy="92" r="16"/><text x="326" y="97" text-anchor="middle">F</text></g><g class="ts-badge"><title>in-degree of F: 1</title><rect x="331" y="61" width="20" height="17" rx="5"/><text x="341" y="74" text-anchor="middle">1</text></g><g class="ts-node is-stuck"><title>task G</title><circle cx="420" cy="92" r="16"/><text x="420" y="97" text-anchor="middle">G</text></g><g class="ts-badge"><title>in-degree of G: 1</title><rect x="425" y="61" width="20" height="17" rx="5"/><text x="435" y="74" text-anchor="middle">1</text></g></svg>

    <!-- /gen -->

    <!-- gen 6 -->

    <span class="viz-legend"><span><i class="ts-key-out"></i>יצאה מהתור</span><span><i class="ts-key-cycle"></i>המעגל</span><span><i class="ts-key-stuck"></i>תקועה אחרי המעגל, לא עליו</span><span><i class="ts-key-badge"></i>דרגת הכניסה שנשארה</span></span>

    <!-- /gen -->

    <!-- gen 7 -->

    | המשימה | ‏C | ‏D | ‏E | ‏F | ‏G |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | דרגת הכניסה שנשארה | 1 | 1 | 1 | 1 | 1 |
    | מחכה ל | ‏E | ‏C | ‏D | ‏D | ‏F |

    <!-- /gen -->

    חמש המשימות שנשארו מחכות כל אחת לאחת מהן. הולכים אחורה מ-C : היא מחכה ל-E, ‏E מחכה ל-D, ו-D
    מחכה ל-C. זה המעגל <span dir="ltr">C → D → E → C</span>. ‏F ו-G תקועות בגללו, אבל הן לא עליו :
    המשימות שנשארו **מכילות** מעגל, ולא כולן חלק ממנו.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="topo_kahn" linenums="1" hl_lines="11 18 22"
        from collections import deque


        def topo_kahn(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
            """An order of the tasks 0..n-1 in which a comes before b for every edge (a, b),
            "b after a"; None when the dependencies contain a cycle."""
            succ = [[] for _ in range(n)]
            indeg = [0] * n
            for a, b in edges:
                succ[a].append(b)
                indeg[b] += 1                          # (1)!
            q = deque(v for v in range(n) if indeg[v] == 0)
            order = []
            while q:
                u = q.popleft()
                order.append(u)
                for v in succ[u]:
                    indeg[v] -= 1                      # (2)!
                    if indeg[v] == 0:
                        q.append(v)
            if len(order) < n:
                return None                            # (3)!
            return order
        ```

        1. חץ שמופיע פעמיים נספר פעמיים, וגם נכנס פעמיים לרשימת העוקבות, ולכן גם יורד פעמיים. זה
           מה ששומר על הקוד נכון עם חצים כפולים (ראו המלכודת).
        2. משימה נכנסת לתור בדיוק פעם אחת : ברגע שהדרגה שלה יורדת ל-0, אחרי שכל המשימות שהיא
           מחכה להן יצאו.
        3. פחות מ-\( n \) משימות יצאו : מה שנשאר מכיל מעגל. אפשר להחזיר גם אותו, בהליכה אחורה
           בין המשימות שנשארו.

    === "SystemVerilog"
        ```systemverilog title="function topo_kahn" linenums="1" hl_lines="9 18 22"
        // an order of the tasks 0..n-1 in which a comes before b for every edge {a, b}, "b after a";
        // returns 0, with the tasks that did run, when the dependencies contain a cycle
        function automatic bit topo_kahn(int n, int edges[][2], output int order[$]);
          int succ[int][$];                                  // (1)!
          int indeg[], q[$], u, v;
          indeg = new[n];                                    // (2)!
          foreach (edges[i]) begin
            succ[edges[i][0]].push_back(edges[i][1]);
            indeg[edges[i][1]]++;
          end
          order.delete();
          for (int t = 0; t < n; t++) if (indeg[t] == 0) q.push_back(t);
          while (q.size() > 0) begin
            u = q.pop_front();
            order.push_back(u);
            if (succ.exists(u)) foreach (succ[u][j]) begin
              v = succ[u][j];
              indeg[v]--;
              if (indeg[v] == 0) q.push_back(v);
            end
          end
          return order.size() == n;                          // (3)!
        endfunction
        ```

        1. רשימות העוקבות כמערך אסוציאטיבי של תורים : ‏`succ[u]` הוא תור העוקבות של \( u \).
           משימה בלי עוקבות אינה מופיעה בו, ולכן הבדיקה `succ.exists(u)` לפני הלולאה.
        2. ‏`new[n]` מאתחל את כל הדרגות ל-0.
        3. ‏0 אומר שיש מעגל. ‏`order` מחזיק אז את המשימות שכן רצו, ואפשר לדווח מי נשארה.

    #### למה זה נכון { .sol-proof }

    **כל חץ הולך קדימה :** משימה \( b \) נכנסת לתור רק כשהדרגה שלה 0, כלומר אחרי שכל \( a \) עם
    חץ \( a \to b \) יצאה מהתור והורידה אותה. לכן כל \( a \) כזו נמצאת בסדר לפני \( b \).

    **בלי מעגל, כולן יוצאות :** נניח שהתור התרוקן ונשארה קבוצה לא ריקה \( S \) של משימות. לכל
    משימה ב-\( S \) דרגה גדולה מ-0, והדרגה סופרת רק חצים ממשימות שלא יצאו, כלומר מ-\( S \). אז
    לכל משימה ב-\( S \) יש קודמת ב-\( S \), והליכה אחורה בתוך \( S \) חוזרת על משימה אחרי לכל
    היותר \( |S| \) צעדים : מעגל. לכן בגרף בלי מעגל \( S \) ריקה, וכל \( n \) המשימות יוצאות.

    **עם מעגל, לא כולן יוצאות :** תהי \( v \) המשימה הראשונה מהמעגל שיוצאת מהתור. כדי להיכנס
    לתור הדרגה שלה הייתה צריכה להגיע ל-0, אבל הקודמת שלה במעגל עוד לא יצאה ולא הורידה אותה.
    סתירה, ולכן אף משימה מהמעגל לא יוצאת, וגם לא משימה שמחכה להן. ‏`None` מוחזר בדיוק כשיש מעגל.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n + m) \). כל משימה נכנסת לתור ויוצאת ממנו פעם אחת לכל היותר, וכל חץ נספר
      פעם אחת ומוריד דרגה פעם אחת.
    - **זיכרון :** ‏\( O(n + m) \) לרשימות העוקבות, ועוד \( O(n) \) לדרגות, לתור ולסדר.
    - **מקרי קצה :** בלי חצים כל המשימות בתור מההתחלה, והסדר הוא <span dir="ltr">0, 1, …, n − 1</span>.
      לולאה עצמית \( (a, a) \) היא מעגל באורך 1 : הדרגה של \( a \) לא יורדת לעולם, והתשובה
      `None`. גרף של כמה רכיבים לא מפריע : בתור ההתחלתי יש משימה מכל רכיב.

    **נסו בעצמכם.** לחצו "הצעד הבא" ועקבו אחרי הדרגות ליד המשימות ואחרי התור שמתחת לגרף. אחר כך
    בחרו "הדוגמה עם מעגל" ולחצו "עד הסוף" : אחרי A ו-B התור מתרוקן, והמעגל
    <span dir="ltr">C → D → E</span> מסומן באדום. לבסוף לחצו על D ואחר כך על E כדי למחוק את
    החץ ביניהן, והזרימה משתחררת. בתיבה עורכים את הגרף בלחיצות או בשדה החצים, ורואים כל הורדה של
    דרגה כצעד בפני עצמו :

    <div class="explorer" data-kind="toposort" data-mode="kahn" data-n="7" data-edges="AB AC EC BD CD DF FG" data-dur="3.2.4.1.5.1.4"></div>

---

### סעיף ב – חיפוש לעומק ושלושה צבעים

??? tip "רמז 1"
    חיפוש לעומק (DFS) מ-\( u \) מבקר בכל מה שאפשר להגיע אליו מ-\( u \) לפני שהוא חוזר מ-\( u \).
    איפה \( u \) צריכה להיות בסדר ביחס לכל המשימות האלה?

??? tip "רמז 2"
    כשהחיפוש פוגש משימה שהוא כבר ראה, יש שתי אפשרויות שונות מאוד : שהוא כבר סיים איתה ויצא ממנה,
    או שהוא עדיין בתוכה, על המסלול הנוכחי. איזו מהן אומרת שיש מעגל?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        חיפוש לעומק מכל משימה שעוד לא בוקרה, עם שלושה צבעים : **לבנה** (עוד לא נכנסנו), **אפורה**
        (על המסלול הנוכחי) ו**שחורה** (יצאנו ממנה). יוצאים ממשימה רק אחרי שיצאנו מכל העוקבות
        שלה, ולכן **ההיפוך של סדר היציאה** הוא סדר נכון. חץ אל משימה אפורה הוא **קשת אחורה**, ואז
        יש מעגל : המסלול האפור ממנה עד המשימה הנוכחית. בדוגמה :
        <span dir="ltr">E, A, C, B, D, F, G</span>.

    <!-- cost: זמן \( O(n + m) \) | זיכרון \( O(n + m) \) -->

    #### הרעיון { .sol-idea }

    **חיפוש לעומק.** נכנסים למשימה, ממנה לעוקבת הראשונה שעוד לא בוקרה, ממנה הלאה, עד שאין לאן
    להמשיך ; אז **יוצאים** מהמשימה וחוזרים צעד אחד אחורה, לעוקבת הבאה של הקודמת. כשהחיפוש מ-\( s \)
    נגמר, מתחילים חיפוש חדש מהמשימה הבאה שעוד לא בוקרה.

    **שלושה צבעים.** כל משימה מתחילה **לבנה**. כשנכנסים אליה היא נעשית **אפורה**, וכשיוצאים ממנה
    **שחורה**. בכל רגע המשימות האפורות הן בדיוק המסלול מנקודת ההתחלה עד המשימה הנוכחית, כל אחת
    עוקבת של הקודמת.

    **למה ההיפוך של סדר היציאה.** כשיוצאים מ-\( u \), כל העוקבות שלה כבר שחורות : או שנכנסנו
    אליהן מ-\( u \) ויצאנו לפני שחזרנו, או שיצאנו מהן עוד קודם. לכן כל עוקבת יוצאת לפני \( u \),
    ובסדר ההפוך \( u \) לפני כל העוקבות שלה.

    **למה צריך אפור.** חץ אל משימה שכבר ראינו יכול להוביל לשני מקרים. משימה **שחורה** כבר סגורה,
    ושום מסלול ממנה לא חוזר אלינו : זה בסדר, כמו ביהלום \( A \to B \to D \), ‏\( A \to C \to D \),
    שבו C מגיעה ל-D אחרי שכבר יצאנו ממנה דרך B. משימה **אפורה** נמצאת על המסלול הנוכחי, כלומר
    יש ממנה מסלול אלינו, והחץ סוגר מעגל. "ביקרנו או לא" לא מבדיל בין שני המקרים :

    <!-- gen 11 -->

    <svg class="figure ts-fig" viewBox="0 0 260 140" style="max-width:16.25rem" role="img" aria-label="היהלום A, B, C, D ברגע ש-C מסתכלת על D : ‏D כבר שחורה, יצאנו ממנה דרך B. זה לא מעגל, ובדיקה של ביקרנו או לא הייתה מדווחת כאן מעגל בטעות"><g class="ts-edge"><title>A → B</title><line x1="54.6" y1="63.5" x2="109.0" y2="39.3"/><path class="ts-head" d="M115.4,36.5 L110.8,43.5 L107.2,35.2 Z"/></g><g class="ts-edge"><title>A → C</title><line x1="54.6" y1="76.5" x2="109.0" y2="100.7"/><path class="ts-head" d="M115.4,103.5 L107.2,104.8 L110.8,96.5 Z"/></g><g class="ts-edge"><title>B → D</title><line x1="144.6" y1="36.5" x2="199.0" y2="60.7"/><path class="ts-head" d="M205.4,63.5 L197.2,64.8 L200.8,56.5 Z"/></g><g class="ts-edge is-now"><title>C → D</title><line x1="144.6" y1="103.5" x2="199.0" y2="79.3"/><path class="ts-head" d="M205.4,76.5 L200.8,83.5 L197.2,75.2 Z"/></g><g class="ts-node is-grey"><title>task A</title><circle cx="40" cy="70" r="16"/><text x="40" y="75" text-anchor="middle">A</text></g><g class="ts-node is-black"><title>task B</title><circle cx="130" cy="30" r="16"/><text x="130" y="35" text-anchor="middle">B</text></g><g class="ts-node is-grey"><title>task C</title><circle cx="130" cy="110" r="16"/><text x="130" y="115" text-anchor="middle">C</text></g><g class="ts-node is-black"><title>task D</title><circle cx="220" cy="70" r="16"/><text x="220" y="75" text-anchor="middle">D</text></g></svg>

    <!-- /gen -->

    **בלי רקורסיה.** הדרך הטבעית לכתוב DFS היא רקורסיה, אבל עומק הרקורסיה הוא אורך המסלול, עד
    \( n \). שרשרת של עשרת אלפים משימות מפילה את Python, שמגביל את העומק ל-1,000 כברירת מחדל.
    הקוד כאן מחזיק **מחסנית** משלו : לכל משימה אפורה, מהי העוקבת הבאה שעוד לא נבדקה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מתחילים :** בונים את רשימות העוקבות, וכל המשימות לבנות.
    2. **נקודת התחלה :** לכל משימה \( s \) שעדיין לבנה, לפי המספר : צובעים אותה אפור ודוחפים
       <span dir="ltr">[s, 0]</span> למחסנית.
    3. **העוקבת הבאה :** בראש המחסנית <span dir="ltr">[u, i]</span>. אם ל-\( u \) יש עוקבת
       במקום \( i \), מקדמים את \( i \) ובודקים אותה. אפורה : מעגל, מחזירים את המסלול ממנה.
       לבנה : צובעים אפור ודוחפים. שחורה : ממשיכים.
    4. **יוצאים :** אם נגמרו העוקבות של \( u \), מוציאים אותה מהמחסנית, צובעים שחור, ומוסיפים
       לרשימת היציאות.
    5. **הסוף :** הסדר הוא רשימת היציאות מהסוף להתחלה.

    </div>

    על הדוגמה. השעון עולה ב-1 בכל כניסה ובכל יציאה ; לכל משימה מתי נכנסנו אליה ומתי יצאנו :

    <!-- gen 8 -->

    | המשימה | נכנסים (אפורה) | יוצאים (שחורה) |
    |:-:|:-:|:-:|
    | ‏A | 1 | 12 |
    | ‏B | 2 | 9 |
    | ‏C | 10 | 11 |
    | ‏D | 3 | 8 |
    | ‏E | 13 | 14 |
    | ‏F | 4 | 7 |
    | ‏G | 5 | 6 |

    <!-- /gen -->

    החיפוש הראשון מ-A עובר דרך B, ‏D, ‏F עד G, יוצא מהן מהסוף, ואז נכנס ל-C. החץ
    <span dir="ltr">C → D</span> מגיע ל-D שכבר שחורה (יצאנו ממנה בזמן 8), כלומר היהלום ולא
    מעגל. בסוף נכנסים ל-E, והחץ <span dir="ltr">E → C</span> מגיע ל-C השחורה. סדר היציאה
    <span dir="ltr">G, F, D, B, C, A, E</span>, וההיפוך שלו <span dir="ltr">E, A, C, B, D, F, G</span> :
    סדר נכון אחר מזה של Kahn. אפשר לראות את זה גם בעמודה האחרונה : זמן היציאה של כל משימה גדול מזה
    של כל העוקבות שלה.

    **על הדוגמה עם המעגל.** עם החץ <span dir="ltr">D → E</span> החיפוש הולך
    <span dir="ltr">A → B → D → F → G</span>, יוצא מ-G ומ-F, ואז ממשיך מ-D ל-E ומ-E ל-C. מ-C החץ
    חוזר ל-D, שעדיין אפורה :

    <!-- gen 9 -->

    <svg class="figure ts-fig" viewBox="0 0 464 202" style="max-width:29rem" role="img" aria-label="החיפוש לעומק על הדוגמה עם המעגל : המסלול האפור A, B, D, E, C. ‏F ו-G כבר שחורות. מ-C החץ חוזר ל-D, שעדיין אפורה : קשת אחורה, והמעגל הוא D, E, C"><g class="ts-edge is-path"><title>A → B: B after A</title><line x1="60.0" y1="52.0" x2="115.0" y2="52.0"/><path class="ts-head" d="M122.0,52.0 L115.0,56.5 L115.0,47.5 Z"/></g><g class="ts-edge"><title>A → C: C after A</title><line x1="56.2" y1="62.4" x2="120.5" y2="117.1"/><path class="ts-head" d="M125.8,121.6 L117.6,120.5 L123.4,113.7 Z"/></g><g class="ts-edge is-path"><title>E → C: C after E</title><line x1="60.0" y1="132.0" x2="115.0" y2="132.0"/><path class="ts-head" d="M122.0,132.0 L115.0,136.5 L115.0,127.5 Z"/></g><g class="ts-edge is-path"><title>B → D: D after B</title><line x1="152.7" y1="58.3" x2="210.8" y2="83.0"/><path class="ts-head" d="M217.3,85.7 L209.1,87.1 L212.6,78.9 Z"/></g><g class="ts-edge is-back"><title>C → D: D after C</title><line x1="152.7" y1="125.7" x2="210.8" y2="101.0"/><path class="ts-head" d="M217.3,98.3 L212.6,105.1 L209.1,96.9 Z"/></g><g class="ts-edge"><title>D → F: F after D</title><line x1="248.0" y1="92.0" x2="303.0" y2="92.0"/><path class="ts-head" d="M310.0,92.0 L303.0,96.5 L303.0,87.5 Z"/></g><g class="ts-edge"><title>F → G: G after F</title><line x1="342.0" y1="92.0" x2="397.0" y2="92.0"/><path class="ts-head" d="M404.0,92.0 L397.0,96.5 L397.0,87.5 Z"/></g><g class="ts-edge is-path"><title>D → E: E after D</title><path d="M223.5,105.5 Q150,222 61.5,146.9" fill="none"/><path class="ts-head" d="M56.2,142.4 L64.4,143.5 L58.6,150.3 Z"/></g><g class="ts-node is-grey"><title>task A</title><circle cx="44" cy="52" r="16"/><text x="44" y="57" text-anchor="middle">A</text></g><g class="ts-node is-grey"><title>task B</title><circle cx="138" cy="52" r="16"/><text x="138" y="57" text-anchor="middle">B</text></g><g class="ts-node is-grey"><title>task C</title><circle cx="138" cy="132" r="16"/><text x="138" y="137" text-anchor="middle">C</text></g><g class="ts-node is-grey"><title>task D</title><circle cx="232" cy="92" r="16"/><text x="232" y="97" text-anchor="middle">D</text></g><g class="ts-node is-grey"><title>task E</title><circle cx="44" cy="132" r="16"/><text x="44" y="137" text-anchor="middle">E</text></g><g class="ts-node is-black"><title>task F</title><circle cx="326" cy="92" r="16"/><text x="326" y="97" text-anchor="middle">F</text></g><g class="ts-node is-black"><title>task G</title><circle cx="420" cy="92" r="16"/><text x="420" y="97" text-anchor="middle">G</text></g></svg>

    <!-- /gen -->

    <!-- gen 10 -->

    <span class="viz-legend"><span><i class="ts-key-white"></i>לבנה : עוד לא נכנסנו</span><span><i class="ts-key-grey"></i>אפורה : על המסלול הנוכחי</span><span><i class="ts-key-black"></i>שחורה : יצאנו ממנה, כל מה שאחריה סגור</span><span><i class="ts-key-path"></i>המסלול האפור</span><span><i class="ts-key-back"></i>קשת אחורה, אל משימה אפורה</span></span>

    <!-- /gen -->

    המסלול האפור במחסנית הוא <span dir="ltr">A, B, D, E, C</span>, ומ-D ועד סופו זה המעגל
    <span dir="ltr">D → E → C → D</span>, אותו מעגל ש-Kahn מצא, מנקודה אחרת.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="topo_dfs" linenums="1" hl_lines="22 24 30 32"
        WHITE, GREY, BLACK = 0, 1, 2


        def topo_dfs(n: int, edges: list[tuple[int, int]]) -> tuple[list[int] | None, list[int] | None]:
            """(order, None) as topo_kahn, or (None, cycle) with the tasks of one cycle in edge order:
            a depth-first search with three colours and a stack of its own, without recursion."""
            succ = [[] for _ in range(n)]
            for a, b in edges:
                succ[a].append(b)
            color = [WHITE] * n
            done = []                                  # the tasks in the order the search leaves them
            for s in range(n):
                if color[s] != WHITE:
                    continue
                color[s] = GREY
                stack = [[s, 0]]                       # (1)!
                while stack:
                    u, i = stack[-1]
                    if i < len(succ[u]):
                        stack[-1][1] += 1
                        v = succ[u][i]
                        if color[v] == GREY:           # (2)!
                            path = [w for w, _ in stack]
                            return None, path[path.index(v):]
                        if color[v] == WHITE:
                            color[v] = GREY
                            stack.append([v, 0])
                    else:
                        stack.pop()
                        color[u] = BLACK               # (3)!
                        done.append(u)
            return done[::-1], None                    # (4)!
        ```

        1. כל איבר במחסנית הוא משימה אפורה והמקום של העוקבת הבאה שלה שעוד לא נבדקה. המחסנית היא
           המסלול האפור, ומחליפה את הרקורסיה.
        2. קשת אחורה. המשימות במחסנית מ-\( v \) עד הראש הן מסלול, כל אחת עוקבת של הקודמת, והחץ
           מהראש חזרה ל-\( v \) סוגר אותו למעגל.
        3. יוצאים מ-\( u \) רק כשכל העוקבות שלה נבדקו, כלומר כולן כבר שחורות.
        4. ההיפוך של סדר היציאה. ‏`list.insert(0, u)` בכל יציאה היה עובד, אבל ב-\( O(n) \) לכל
           הכנסה.

    === "SystemVerilog"
        ```systemverilog title="function topo_dfs" linenums="1" hl_lines="19 31 32"
        // 1 and an order as topo_kahn, or 0 and one cycle with its tasks in edge order: a
        // depth-first search with three colours and a stack of its own, without recursion
        function automatic bit topo_dfs(int n, int edges[][2], output int order[$], output int cycle[$]);
          int succ[int][$];
          byte color[];                                      // (1)!
          int path[$], nxt[$], u, v, k;
          color = new[n];
          foreach (edges[i]) succ[edges[i][0]].push_back(edges[i][1]);
          order.delete(); cycle.delete();
          for (int s = 0; s < n; s++) begin
            if (color[s] != 0) continue;
            color[s] = 1; path.push_back(s); nxt.push_back(0);
            while (path.size() > 0) begin
              u = path[path.size() - 1];                     // (2)!
              k = nxt[nxt.size() - 1];
              if (succ.exists(u) && k < succ[u].size()) begin
                nxt[nxt.size() - 1] = k + 1;
                v = succ[u][k];
                if (color[v] == 1) begin                     // (3)!
                  k = 0;
                  while (path[k] != v) k++;
                  for (int j = k; j < path.size(); j++) cycle.push_back(path[j]);
                  order.delete();
                  return 0;
                end
                if (color[v] == 0) begin
                  color[v] = 1; path.push_back(v); nxt.push_back(0);
                end
              end else begin
                void'(path.pop_back()); void'(nxt.pop_back());
                color[u] = 2;
                order.push_front(u);                         // (4)!
              end
            end
          end
          return 1;
        endfunction
        ```

        1. ‏0 לבנה, 1 אפורה, 2 שחורה. ‏`new[n]` מתחיל את כולן לבנות.
        2. המחסנית היא שני תורים מקבילים : ‏`path` המשימות האפורות, ו-`nxt` המקום של העוקבת הבאה
           של כל אחת.
        3. קשת אחורה : המעגל הוא החלק של `path` מ-\( v \) עד הסוף.
        4. ‏`push_front` של כל משימה שיוצאים ממנה בונה את ההיפוך של סדר היציאה ישירות. בתור של
           SystemVerilog זו פעולה זולה.

    #### למה זה נכון { .sol-proof }

    **כל חץ הולך קדימה :** כשהחיפוש בודק חץ \( u \to v \), ‏\( u \) אפורה. אם \( v \) לבנה, נכנסים
    אליה ויוצאים ממנה לפני שחוזרים ל-\( u \). אם \( v \) שחורה, כבר יצאנו ממנה. בשני המקרים יוצאים
    מ-\( v \) לפני \( u \), ובסדר ההפוך \( u \) לפני \( v \). המקרה השלישי, \( v \) אפורה, עוצר את
    החיפוש עם מעגל.

    **קשת אחורה היא מעגל :** המשימות האפורות הן המסלול במחסנית. אם \( v \) אפורה, יש מסלול מ-\( v \)
    ל-\( u \) במחסנית, והחץ \( u \to v \) סוגר אותו. לכן כל מעגל שהקוד מחזיר הוא מעגל אמיתי.

    **כל מעגל נמצא :** תהי \( v \) המשימה הראשונה מהמעגל שנעשית אפורה, ו-\( u \) הקודמת שלה
    במעגל. ברגע ש-\( v \) נעשית אפורה, כל שאר המשימות במעגל לבנות, ויש מ-\( v \) מסלול לבן
    ל-\( u \) לאורך המעגל. החיפוש לא יוצא מ-\( v \) לפני שהוא יוצא מכל מה שאפשר להגיע אליו
    ממנה במשימות לבנות, ובפרט הוא נכנס ל-\( u \) כש-\( v \) עוד אפורה. כשהוא בודק את
    \( u \to v \), ‏\( v \) אפורה : קשת אחורה. לכן בגרף עם מעגל הקוד לא מחזיר סדר.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n + m) \). כל משימה נכנסת ויוצאת פעם אחת, וכל חץ נבדק פעם אחת, כשמקדמים את
      המקום של העוקבת הבאה.
    - **זיכרון :** ‏\( O(n + m) \) לרשימות העוקבות, ועוד \( O(n) \) לצבעים ולמחסנית, שעומקה עד
      \( n \) : שרשרת ארוכה עולה כאן זיכרון, לא קריסה.
    - **מול Kahn :** אותה סיבוכיות. ‏DFS מחזיר מעגל ישירות מהמחסנית, ו-Kahn נותן גם את הסבבים
      (ראו שאלות ההמשך).

---

### סעיף ג – משכים ומקביליות : הנתיב הקריטי

לכל משימה יש **משך**, בדקות. משימות שאין תלות ביניהן יכולות לרוץ במקביל, ויש כמה מריצים שצריך.
מתי כל המשימות נגמרות לכל המוקדם, ומתי מתחילה כל משימה? אילו משימות **קריטיות**, כלומר כל עיכוב
שלהן מעכב את הסוף? המשכים בדוגמה :
<span dir="ltr">A = 3, B = 2, C = 4, D = 1, E = 5, F = 1, G = 4</span>.

??? tip "רמז 1"
    משימה יכולה להתחיל ברגע שהאחרונה מבין המשימות שהיא מחכה להן הסתיימה. באיזה סדר צריך לעבור על
    המשימות כדי שכשמגיעים למשימה, הזמנים של כל אלה שהיא מחכה להן כבר ידועים?

??? tip "רמז 2"
    הזמן הכולל הוא סכום המשכים לאורך שרשרת אחת של תלויות. איזו שרשרת? ואיך יודעים כמה משימה שלא
    עליה יכולה להתאחר?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        מעבר אחד בסדר טופולוגי : ההתחלה המוקדמת של \( v \) היא המקסימום, על כל \( a \to v \), של
        \( \mathrm{start}[a] + d[a] \) (או 0), והזמן הכולל הוא המקסימום של
        \( \mathrm{start}[v] + d[v] \). זה המשקל של המסלול הכבד ביותר, **הנתיב הקריטי**. מעבר שני
        בסדר ההפוך נותן לכל משימה את הסיום המאוחר ביותר שלא מעכב את הסוף, וההפרש הוא **המרווח**
        (slack) ; משימות במרווח 0 קריטיות. בדוגמה : 15 דקות (מריץ אחד היה צריך 20), והנתיב
        <span dir="ltr">E → C → D → F → G</span>.

    <!-- cost: זמן \( O(n + m) \) | זיכרון \( O(n + m) \) -->

    #### הרעיון { .sol-idea }

    **התחלה מוקדמת.** משימה מתחילה ברגע שכל המשימות שהיא מחכה להן הסתיימו, ולא לפני. עם מספר לא
    מוגבל של מריצים אין סיבה לחכות יותר, ולכן
    \( \mathrm{start}[v] = \max_{a \to v} (\mathrm{start}[a] + d[a]) \), ו-0 למשימה שלא מחכה
    לאף אחת. כדי לחשב את זה צריך את הזמנים של כל הקודמות קודם : זה בדיוק **סדר טופולוגי**, ו-Kahn
    של סעיף א נותן אותו.

    **הזמן הכולל הוא המסלול הכבד.** משימות על שרשרת של תלויות רצות אחת אחרי השנייה, ולכן כל
    לוח זמנים לוקח לפחות את סכום המשכים של כל שרשרת. ההתחלה המוקדמת משיגה את זה בדיוק : מכל
    משימה אפשר ללכת אחורה דרך הקודמת שקבעה את ההתחלה שלה, ומתקבלת שרשרת בלי רגע אחד של המתנה.
    הזמן הכולל הוא לכן המשקל של המסלול הכבד ביותר, לפי סכום המשכים ולא לפי מספר המשימות.

    **מרווח.** הסיום המאוחר של \( u \), ‏\( \mathrm{late}[u] \), הוא הרגע האחרון שבו \( u \) יכולה
    להסתיים בלי לעכב את הסוף : הזמן הכולל למשימה בלי עוקבות, ואחרת המינימום של
    \( \mathrm{late}[v] - d[v] \) על כל עוקבת \( v \), כלומר ההתחלה המאוחרת של העוקבת הדחופה
    ביותר. מחשבים אותו בסדר ההפוך. **המרווח** הוא
    \( \mathrm{late}[v] - d[v] - \mathrm{start}[v] \) : כמה אפשר לאחר את \( v \). משימה במרווח 0
    היא **קריטית**, וכל דקה שלה היא דקה של הסוף.

    הדוגמה כלוח זמנים, פס לכל משימה מההתחלה המוקדמת עד הסיום המוקדם :

    <!-- gen 12 -->

    <svg class="perf-chart ts-gantt" viewBox="0 0 464 222" style="max-width:29rem" role="img" aria-label="לוח הזמנים עם מספר לא מוגבל של מריצים : פס לכל משימה מההתחלה המוקדמת עד הסיום המוקדם. הנתיב הקריטי E, C, D, F, G בלי מרווח, והכול נגמר בזמן 15. ‏A ו-B יכולות להתאחר ב-2 וב-4 דקות"><line class="grid" x1="30.0" x2="30.0" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="30.0" y="214" text-anchor="middle">0</text><line class="grid" x1="56.2" x2="56.2" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="56.2" y="214" text-anchor="middle"></text><line class="grid" x1="82.5" x2="82.5" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="82.5" y="214" text-anchor="middle">2</text><line class="grid" x1="108.8" x2="108.8" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="108.8" y="214" text-anchor="middle"></text><line class="grid" x1="135.0" x2="135.0" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="135.0" y="214" text-anchor="middle">4</text><line class="grid" x1="161.2" x2="161.2" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="161.2" y="214" text-anchor="middle"></text><line class="grid" x1="187.5" x2="187.5" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="187.5" y="214" text-anchor="middle">6</text><line class="grid" x1="213.8" x2="213.8" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="213.8" y="214" text-anchor="middle"></text><line class="grid" x1="240.0" x2="240.0" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="240.0" y="214" text-anchor="middle">8</text><line class="grid" x1="266.2" x2="266.2" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="266.2" y="214" text-anchor="middle"></text><line class="grid" x1="292.5" x2="292.5" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="292.5" y="214" text-anchor="middle">10</text><line class="grid" x1="318.8" x2="318.8" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="318.8" y="214" text-anchor="middle"></text><line class="grid" x1="345.0" x2="345.0" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="345.0" y="214" text-anchor="middle">12</text><line class="grid" x1="371.2" x2="371.2" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="371.2" y="214" text-anchor="middle"></text><line class="grid" x1="397.5" x2="397.5" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="397.5" y="214" text-anchor="middle">14</text><line class="grid" x1="423.8" x2="423.8" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="423.8" y="214" text-anchor="middle">15</text><line class="grid" x1="450.0" x2="450.0" y1="4" y2="196" stroke-dasharray="4 4"/><text class="tick" x="450.0" y="214" text-anchor="middle">16</text><text class="ts-glab" x="22" y="29" text-anchor="end">A</text><rect class="ts-slack" x="108.8" y="19" width="52.5" height="12" rx="3"><title>A: slack 2, may finish as late as 5</title></rect><g class="ts-bar"><title>A: 3 minutes, from 0 to 3, slack 2</title><rect x="30.0" y="16" width="78.8" height="18" rx="3"/><text x="69.4" y="29" text-anchor="middle">3</text></g><text class="ts-glab" x="22" y="55" text-anchor="end">B</text><rect class="ts-slack" x="161.2" y="45" width="105.0" height="12" rx="3"><title>B: slack 4, may finish as late as 9</title></rect><g class="ts-bar"><title>B: 2 minutes, from 3 to 5, slack 4</title><rect x="108.8" y="42" width="52.5" height="18" rx="3"/><text x="135.0" y="55" text-anchor="middle">2</text></g><text class="ts-glab" x="22" y="81" text-anchor="end">C</text><g class="ts-bar is-crit"><title>C: 4 minutes, from 5 to 9, critical</title><rect x="161.2" y="68" width="105.0" height="18" rx="3"/><text x="213.8" y="81" text-anchor="middle">4</text></g><text class="ts-glab" x="22" y="107" text-anchor="end">D</text><g class="ts-bar is-crit"><title>D: 1 minutes, from 9 to 10, critical</title><rect x="266.2" y="94" width="26.2" height="18" rx="3"/><text x="279.4" y="107" text-anchor="middle">1</text></g><text class="ts-glab" x="22" y="133" text-anchor="end">E</text><g class="ts-bar is-crit"><title>E: 5 minutes, from 0 to 5, critical</title><rect x="30.0" y="120" width="131.2" height="18" rx="3"/><text x="95.6" y="133" text-anchor="middle">5</text></g><text class="ts-glab" x="22" y="159" text-anchor="end">F</text><g class="ts-bar is-crit"><title>F: 1 minutes, from 10 to 11, critical</title><rect x="292.5" y="146" width="26.2" height="18" rx="3"/><text x="305.6" y="159" text-anchor="middle">1</text></g><text class="ts-glab" x="22" y="185" text-anchor="end">G</text><g class="ts-bar is-crit"><title>G: 4 minutes, from 11 to 15, critical</title><rect x="318.8" y="172" width="105.0" height="18" rx="3"/><text x="371.2" y="185" text-anchor="middle">4</text></g><line class="ts-total" x1="423.8" x2="423.8" y1="4" y2="196"/><line class="axis" x1="30" x2="450" y1="196" y2="196"/></svg>

    <!-- /gen -->

    <!-- gen 13 -->

    <span class="viz-legend"><span><i class="ts-key-crit"></i>על הנתיב הקריטי, בלי מרווח</span><span><i class="ts-key-bar"></i>משימה עם מרווח</span><span><i class="ts-key-slack"></i>המרווח : כמה אפשר לאחר בלי לאחר את הסוף</span><span><i class="ts-key-total"></i>הסוף, הזמן הכולל</span><span>המספר בפס : המשך בדקות</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סדר :** `topo_kahn` של סעיף א. אם יש מעגל, אין לוח זמנים.
    2. **קדימה :** \( \mathrm{start} = 0 \) לכולן. לכל \( u \) לפי הסדר ולכל עוקבת \( v \) שלה :
       \( \mathrm{start}[v] = \max(\mathrm{start}[v], \mathrm{start}[u] + d[u]) \).
    3. **הסוף :** הזמן הכולל הוא המקסימום של \( \mathrm{start}[v] + d[v] \).
    4. **אחורה :** \( \mathrm{late} \) שווה לזמן הכולל לכולן. לכל \( u \) בסדר ההפוך ולכל עוקבת
       \( v \) שלה : \( \mathrm{late}[u] = \min(\mathrm{late}[u], \mathrm{late}[v] - d[v]) \).
    5. **המרווח :** \( \mathrm{late}[v] - d[v] - \mathrm{start}[v] \). הקריטיות הן אלה שהמרווח
       שלהן 0.

    </div>

    על הדוגמה. ההתחלה והסיום המוקדמים מהמעבר קדימה, הסיום המאוחר מהמעבר אחורה, והמרווח :

    <!-- gen 14 -->

    | המשימה | המשך | רצה אחרי | התחלה מוקדמת | סיום מוקדם | סיום מאוחר | המרווח |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏A | 3 | – | 0 | 3 | 5 | 2 |
    | ‏B | 2 | ‏A | 3 | 5 | 9 | 4 |
    | ‏C | 4 | ‏A, E | 5 | 9 | 9 | **0** |
    | ‏D | 1 | ‏B, C | 9 | 10 | 10 | **0** |
    | ‏E | 5 | – | 0 | 5 | 5 | **0** |
    | ‏F | 1 | ‏D | 10 | 11 | 11 | **0** |
    | ‏G | 4 | ‏F | 11 | 15 | 15 | **0** |

    <!-- /gen -->

    הנתיב הקריטי הוא <span dir="ltr">E → C → D → F → G</span>,
    <span dir="ltr">5 + 4 + 1 + 1 + 4 = 15</span>. ‏A מסתיימת בזמן 3, אבל C מחכה גם ל-E עד 5,
    ולכן ל-A מרווח 2 ; ‏B מסתיימת ב-5 ו-D מתחילה רק ב-9, ולכן ל-B מרווח 4. מריץ אחד היה צריך את
    סכום כל המשכים, 20 דקות, והמקביליות חוסכת 5. גם השרשרת
    <span dir="ltr">A → B → D → F → G</span> ארוכה באותה מידה במספר המשימות, חמש, אבל היא שוקלת
    רק 11.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="critical_path" linenums="1" hl_lines="14 15 19 20"
        def critical_path(n: int, edges: list[tuple[int, int]], dur: list[int]):
            """Unlimited workers: (total, start, slack), the time until every task is done, the
            earliest start of every task and how long it may slip without delaying the total;
            None on a cycle. The tasks with slack 0 are the critical ones."""
            order = topo_kahn(n, edges)
            if order is None:
                return None
            succ = [[] for _ in range(n)]
            for a, b in edges:
                succ[a].append(b)
            start = [0] * n
            for u in order:                            # (1)!
                for v in succ[u]:
                    start[v] = max(start[v], start[u] + dur[u])
            total = max((start[v] + dur[v] for v in range(n)), default=0)
            late = [total] * n                         # (2)!
            for u in reversed(order):
                for v in succ[u]:
                    late[u] = min(late[u], late[v] - dur[v])
            slack = [late[v] - dur[v] - start[v] for v in range(n)]
            return total, start, slack
        ```

        1. בסדר טופולוגי, כשמגיעים ל-\( u \) כל הקודמות שלה כבר דחפו את \( \mathrm{start}[u] \)
           לערך הסופי, ולכן מותר לדחוף ממנה הלאה.
        2. ‏`late` הוא הסיום המאוחר. משימה בלי עוקבות נשארת עם הזמן הכולל ; ההתחלה המאוחרת של
           \( v \) היא \( \mathrm{late}[v] - d[v] \).

    === "SystemVerilog"
        ```systemverilog title="function critical_path" linenums="1" hl_lines="7 13 22 25"
        // unlimited workers: the time until every task is done (-1 on a cycle), the earliest
        // start of every task and how long it may slip; the tasks with slack 0 are critical
        function automatic int critical_path(int n, int edges[][2], int dur[], output int start[], output int slack[]);
          int order[$], succ[int][$], late[];
          int total = 0, u, v;
          start = new[n]; slack = new[n]; late = new[n];
          if (!topo_kahn(n, edges, order)) return -1;          // (1)!
          foreach (edges[i]) succ[edges[i][0]].push_back(edges[i][1]);
          foreach (order[i]) begin
            u = order[i];
            if (succ.exists(u)) foreach (succ[u][j]) begin
              v = succ[u][j];
              if (start[u] + dur[u] > start[v]) start[v] = start[u] + dur[u];
            end
          end
          for (int t = 0; t < n; t++) if (start[t] + dur[t] > total) total = start[t] + dur[t];
          foreach (late[t]) late[t] = total;
          for (int i = n - 1; i >= 0; i--) begin
            u = order[i];
            if (succ.exists(u)) foreach (succ[u][j]) begin
              v = succ[u][j];
              if (late[v] - dur[v] < late[u]) late[u] = late[v] - dur[v];   // (2)!
            end
          end
          for (int t = 0; t < n; t++) slack[t] = late[t] - dur[t] - start[t];
          return total;
        endfunction
        ```

        1. אותו `topo_kahn` של סעיף א. ‏<span dir="ltr">−1</span> אומר שיש מעגל, ואז אין לוח זמנים.
        2. המעבר אחורה : ההתחלה המאוחרת של העוקבת הדחופה ביותר.

    #### למה זה נכון { .sol-proof }

    **ההתחלה המוקדמת :** באינדוקציה על הסדר. כשמגיעים ל-\( u \), כל הקודמות שלה כבר עברו, וכל
    אחת מהן דחפה את \( \mathrm{start}[u] \) לפחות לסיום שלה. לכן \( \mathrm{start}[u] \) הוא
    המקסימום של הסיומים שלהן, וזה הרגע המוקדם ביותר שבו \( u \) יכולה להתחיל.

    **הזמן הכולל :** כל שרשרת \( v_1 \to v_2 \to \dots \to v_k \) מחייבת
    \( \mathrm{start}[v_k] + d[v_k] \ge d[v_1] + \dots + d[v_k] \), ולכן הזמן הכולל לפחות המשקל
    של המסלול הכבד ביותר. מהצד השני, ההליכה אחורה מהמשימה שמסתיימת אחרונה, בכל צעד אל קודמת
    שהסיום שלה הוא בדיוק ההתחלה של הנוכחית, נותנת שרשרת שהמשקל שלה הוא הזמן הכולל. לכן הזמן
    הכולל שווה למשקל המסלול הכבד ביותר, וכל המשימות על השרשרת הזו במרווח 0.

    **המרווח :** \( \mathrm{late}[u] \) הוא בדיוק הסיום המאוחר ביותר שמאפשר לכל העוקבות להתחיל עד
    ההתחלה המאוחרת שלהן, ובאינדוקציה מהסוף, לכל המשימות שאחריה להסתיים עד הזמן הכולל. משימה
    שמאחרת ב-\( x \) דקות לכל היותר מהמרווח שלה לא מזיזה את הסוף, ואיחור גדול יותר מזיז אותו.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n + m) \) : מיון טופולוגי, ועוד שני מעברים שכל אחד בודק כל חץ פעם אחת.
    - **זיכרון :** ‏\( O(n + m) \).
    - **מריצים :** "לא מוגבל" אומר בפועל לכל היותר כמספר המשימות שרצות באותו רגע. בדוגמה שני
      מריצים מספיקים כדי לסיים ב-15 (ראו שאלות ההמשך).

    **נסו בעצמכם.** התיבה נפתחת על לוח הזמנים של הדוגמה. לחצו "עד הסוף" ומצאו את הנתיב הקריטי
    בלוח שמתחת לגרף. אחר כך שנו בשדה המשכים את המשך של A מ-3 ל-6 : הנתיב הקריטי עובר ל-A, ‏C,
    ‏D, ‏F, ‏G, הסוף זז ל-16, ו-E מקבלת מרווח. בחרו "הדוגמה עם מעגל" : אין לוח זמנים. התיבה
    מוסיפה ללוח של העמוד את ההתחלה של כל משימה צעד אחרי צעד, ואת מה שקורה כשמשנים משך אחד :

    <div class="explorer" data-kind="toposort" data-mode="sched" data-n="7" data-edges="AB AC EC BD CD DF FG" data-dur="3.2.4.1.5.1.4"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להשוות לסדר אחד"
    לדוגמה יש 5 סדרים נכונים. ‏Kahn מחזיר <span dir="ltr">A, E, B, C, D, F, G</span> ו-DFS מחזיר
    <span dir="ltr">E, A, C, B, D, F, G</span>, ושניהם נכונים. בודק שמשווה לסדר צפוי אחד נכשל על
    מימוש נכון, או עובר רק כי המימוש במקרה עובר על המשימות באותו סדר. הבודק הנכון בודק את התכונה
    עצמה : כל משימה מופיעה פעם אחת, ולכל חץ \( (a, b) \) המקום של \( a \) קטן מהמקום של \( b \).
    זה \( O(n + m) \), כמו המיון עצמו.

??? trap "מלכודת : שני צבעים במקום שלושה"
    ‏DFS עם "ביקרנו או לא" טועה לשני כיוונים. אם משימה שכבר ביקרנו בה נחשבת מעגל, היהלום
    <span dir="ltr">A → B → D</span>, <span dir="ltr">A → C → D</span> מדווח מעגל שאין : C מגיעה
    ל-D שכבר בוקרה, אבל שחורה. אם מדלגים על משימה שכבר ביקרנו בה בלי לבדוק, מעגל לא נמצא לעולם,
    והקוד מחזיר "סדר" גם ל-<span dir="ltr">A → B → A</span>. רק ההבחנה בין אפורה (על המסלול)
    לשחורה (סגורה) נותנת את שני הכיוונים נכון.

??? trap "מלכודת : חץ כפול שנספר פעם אחת"
    אם התלויות מגיעות עם כפילויות, \( (A, B) \) פעמיים, צריך להיות עקביים. הקוד בעמוד סופר את
    החץ פעמיים בדרגה ומוריד פעמיים, ולכן נכון. מי שבונה את העוקבות כקבוצה (`set`) אבל סופר את
    הדרגה מהרשימה, מעלה את הדרגה של B ל-2 ומוריד אותה רק פעם אחת : B לא מגיעה ל-0, והקוד מדווח
    מעגל שאין. ההפך, דרגה מקבוצה ועוקבות מרשימה, מוריד את B מתחת ל-0, ובדיקה של
    "‏\( \le 0 \)" תכניס אותה לתור פעמיים. או סופרים כל עותק, או מסירים כפילויות לפני הכול.

??? trap "מלכודת : עומק הרקורסיה"
    ‏DFS רקורסיבי הוא שש שורות, ועל שרשרת של עשרת אלפים משימות הוא נופל : Python עוצר ב-1,000
    קריאות כברירת מחדל (`RecursionError`), והגדלת הגבול עם `sys.setrecursionlimit` רק מעבירה את
    הבעיה לגודל המחסנית של התהליך. גם בסימולטור של SystemVerilog המחסנית מוגבלת. זרימה של רגרסיה
    עם אלפי בדיקות היא בדיוק שרשרת ארוכה, ולכן הקוד בעמוד מחזיק מחסנית משלו, או שמשתמשים ב-Kahn,
    שאין בו רקורסיה בכלל.

??? trap "מלכודת : לולאה עצמית ומעגל באורך 1"
    תלות \( (a, a) \), משימה שמחכה לעצמה, היא מעגל באורך 1. שני האלגוריתמים בעמוד מזהים אותה :
    ב-Kahn הדרגה של \( a \) לא יורדת לעולם, וב-DFS \( a \) אפורה כשבודקים את החץ ממנה אליה. אבל
    קוד שמסנן "חצים מצומת לעצמו" כרעש, או שמחפש מעגל רק בין שתי משימות שונות, מחזיר סדר לזרימה
    שלא תסתיים לעולם.

??? trap "מלכודת : לחפש מעגל רק בהתחלה"
    "אם אין אף משימה עם דרגה 0, יש מעגל" נכון, אבל ההפך לא. בדוגמה עם החץ
    <span dir="ltr">D → E</span> יש משימה כזו, A, והתור מתחיל לא ריק ; המעגל מתגלה רק אחרי ש-A
    ו-B יוצאות. הבדיקה הנכונה היא בסוף : האם יצאו כל \( n \) המשימות.

??? trap "מלכודת : השרשרת הארוכה במספר משימות"
    הזמן הכולל של סעיף ג הוא המסלול **הכבד** ביותר, לפי סכום המשכים. בדוגמה שתי השרשראות
    <span dir="ltr">A → B → D → F → G</span> ו-<span dir="ltr">E → C → D → F → G</span> ארוכות
    באותה מידה, חמש משימות, אבל הראשונה שוקלת 11 והשנייה 15. גם סכום כל המשכים, 20, הוא לא
    התשובה : זה הזמן עם מריץ אחד.

??? followup "שאלות המשך"
    - **בחומרה :** איך נראה אותו רעיון ב-scoreboard של מעבד, שמוציא לביצוע פקודות שהאופרנדים
      שלהן מוכנים?

        ??? fu-answer "תשובה"
            כל פקודה מחכה לפקודות שכותבות את האופרנדים שלה, כמו דרגת כניסה. לוגיקת ה-issue
            מוציאה **בשעון אחד** את כל הפקודות שהאופרנדים שלהן מוכנים, כלומר את כל הצמתים בדרגה 0
            יחד : סבב אחד של Kahn בכל שעון. בדוגמה זה 5 שעונים במקום 7. המתנה מעגלית בחומרה
            (שתי יחידות שכל אחת מחכה ל-credit של השנייה) היא **deadlock** : אין מי שיגלה אותה,
            ולכן מונעים אותה בתכנון, למשל בסדר קבוע של משאבים, ובודקים אותה ב-watchdog וב-assertion.

    - **הסדר הקטן ביותר :** איך מחזירים מכל הסדרים הנכונים את הקטן ביותר בסדר מילוני?

        ??? fu-answer "תשובה"
            מחליפים את התור בערימת מינימום : בכל צעד יוצאת המשימה המוכנה הקטנה ביותר. בדוגמה
            <span dir="ltr">A, B, E, C, D, F, G</span>, בזמן \( O((n + m) \log n) \).

    - **האם הסדר יחיד?** איך יודעים אם יש בדיוק סדר אחד?

        ??? fu-answer "תשובה"
            הסדר יחיד בדיוק כשבתור של Kahn אין אף פעם יותר ממשימה אחת, כלומר כשבין כל שתי
            משימות סמוכות בסדר יש חץ. בדוגמה בתור יש A ו-E כבר בהתחלה, ולכן יש יותר מסדר אחד.

    - **מספר מוגבל של מריצים :** ומה אם יש רק \( k \) מריצים, כמו ב-`make -j k`?

        ??? fu-answer "תשובה"
            הבעיה המדויקת קשה (NP-hard) כבר עם מעט מריצים. בפועל מריצים **list scheduling** : בכל
            פעם שמריץ מתפנה, הוא לוקח משימה מוכנה, עדיף עם המרווח הקטן ביותר. ‏Graham הוכיח
            שהתוצאה לכל היותר פי \( 2 - 1/k \) מהאופטימום. בדוגמה עם שני מריצים מתקבל 15, כמו
            בלי הגבלה.

    - **למצוא את המעגל ב-Kahn :** הקוד של סעיף א מחזיר רק `None`. איך מחזירים מעגל?

        ??? fu-answer "תשובה"
            בסוף נשארות המשימות שלא יצאו, ולכל אחת יש קודמת שגם היא נשארה. הולכים אחורה מאחת
            מהן דרך קודמות שנשארו, עד שמשימה חוזרת ; הקטע בין שתי הפגישות, הפוך, הוא מעגל. זה
            \( O(n + m) \), וזה מה שהתיבה של סעיף א מסמנת באדום.
