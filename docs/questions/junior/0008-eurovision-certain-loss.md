---
id: 8
title: אירוויזיון 2026 – מתי כבר היה ברור שישראל לא תנצח?
level: junior
difficulty: medium
tags: [math, logic-puzzles, algorithms, python, systemverilog]
source: ""
added: 2026-10-16
---

## השאלה

בגמר האירוויזיון של 2026 ישראל ("Michelle" של נעם בתן) סיימה **במקום השני**, אחרי
בולגריה. הניקוד בגמר מגיע משני מקורות:

- **סט נקודות:** כל מצביע נותן \( 12, 10, 8, 7, 6, 5, 4, 3, 2, 1 \) לעשר מדינות שונות,
  ובסך הכול \( 58 \) נקודות.
- **השופטים:** \( 35 \) מדינות, סט אחד לכל מדינה: \( 35 \times 58 = 2{,}030 \) נקודות.
- **הקהל:** \( 35 \) מדינות ועוד הצבעת "שאר העולם" המאוחדת:
  \( 36 \times 58 = 2{,}088 \) נקודות.
- **סך הכול בגמר:** \( 2{,}030 + 2{,}088 = 4{,}118 \) נקודות.

**סדר הערב:** קודם מכריזים את כל נקודות השופטים. אחר כך מכריזים את נקודות הקהל, כסכום אחד
לכל מדינה, **מהמדינה שבמקום האחרון אחרי השופטים ועד המדינה שבמקום הראשון**. ברגע שמדינה
קיבלה את נקודות הקהל שלה, הניקוד שלה סופי.

ישראל הייתה **במקום 8 אחרי השופטים** עם 123 נקודות. כשהוכרזו 220 נקודות הקהל שלה, היא
עלתה זמנית למקום הראשון עם **343 נקודות**. נשארו שבע מדינות שהשופטים דירגו מעליה, ועדיין
לא קיבלו את נקודות הקהל שלהן.

**שובר שוויון:** אם לשתי מדינות יש אותו סך נקודות, מנצחת זו שקיבלה יותר נקודות מהקהל.

???+ info "טבלת התוצאות הסופית"
    | מקום | מדינה | שופטים | קהל | סך הכול |
    |---|---|---|---|---|
    | 1 | ‏Bulgaria | 204 | 312 | 516 |
    | 2 | **‏Israel** | **123** | **220** | **343** |
    | 3 | ‏Romania | 64 | 232 | 296 |
    | 4 | ‏Australia | 165 | 122 | 287 |
    | 5 | ‏Italy | 134 | 147 | 281 |
    | 6 | ‏Finland | 141 | 138 | 279 |
    | 7 | ‏Denmark | 165 | 78 | 243 |
    | 8 | ‏Moldova | 43 | 183 | 226 |
    | 9 | ‏Ukraine | 54 | 167 | 221 |
    | 10 | ‏Greece | 73 | 147 | 220 |
    | 11 | ‏France | 144 | 14 | 158 |
    | 12 | ‏Poland | 133 | 17 | 150 |
    | 13 | ‏Albania | 60 | 85 | 145 |
    | 14 | ‏Norway | 115 | 19 | 134 |
    | 15 | ‏Croatia | 53 | 71 | 124 |
    | 16 | ‏Czechia | 104 | 9 | 113 |
    | 17 | ‏Serbia | 38 | 52 | 90 |
    | 18 | ‏Malta | 81 | 8 | 89 |
    | 19 | ‏Cyprus | 41 | 34 | 75 |
    | 20 | ‏Sweden | 35 | 16 | 51 |
    | 21 | ‏Belgium | 36 | 0 | 36 |
    | 22 | ‏Lithuania | 10 | 12 | 22 |
    | 23 | ‏Germany | 12 | 0 | 12 |
    | 24 | ‏Austria | 1 | 5 | 6 |
    | 25 | ‏United Kingdom | 1 | 0 | 1 |

    סכום עמודת השופטים הוא בדיוק 2,030, וסכום עמודת הקהל הוא בדיוק 2,088.

??? interviewer "מה המראיין בודק"
    - **רדוקציה לשאלה פשוטה:** האם מצליחים להחליף "לנסות את כל החלוקות של הנקודות" בבדיקה
      אחת שאפשר לחשב ביד.
    - **הוכחה לשני הכיוונים:** לא מספיק להראות שמרגע מסוים ישראל בצרה; צריך גם להראות
      שעד אותו רגע היא עוד הייתה יכולה לנצח.
    - **קריאה מדויקת של הכללים:** סדר ההכרזות, מה נחשב "ידוע" בכל רגע, ושובר השוויון.
    - **מהחידה לקוד:** לתרגם את הנימוק לפונקציה קצרה, ולעבור על ההכרזות בסריקה אחת בלי
      לחשב הכול מחדש בכל צעד.

---

### סעיף א – הרגע המוקדם ביותר

נניח שבזמן ההכרזות אנחנו יודעים רק את מה שכבר נחשף: את ניקוד השופטים של כל המדינות, את
נקודות הקהל שהוכרזו עד עכשיו, ואת סך נקודות הקהל (2,088).

**מהו הרגע המוקדם ביותר שבו אפשר היה לדעת בוודאות שישראל לא תנצח?**

??? tip "רמז 1"
    הניקוד של ישראל, 343, כבר סופי. מי עוד יכול לעבור אותו? רק מדינות שעוד לא קיבלו
    נקודות קהל. מה החלוקה של הנקודות שנותרו שהכי **טובה** לישראל?

??? tip "רמז 2"
    ישראל עם 343 נקודות היא "תקרה". כמה נקודות קהל יכולה כל מדינה שמעליה לקבל, בלי
    לעבור את התקרה? ומה קורה אם נשארו יותר נקודות ממה שכל המדינות האלה יכולות "לבלוע"?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **מיד אחרי שצרפת קיבלה 14 נקודות מהקהל**, ההכרזה הרביעית אחרי ישראל: באותו רגע
        נותרו 512 נקודות, אבל לשלוש המדינות שעוד לא הוכרזו היה מקום רק ל-495 נקודות בלי
        לעבור את ישראל.

    #### הרעיון { .sol-idea }

    כל מדינה שעוד לא קיבלה נקודות קהל היא **כוס** שהשפה שלה היא 343, ונקודות הקהל שעוד
    לא הוכרזו הן **מים** שחייבים להישפך לכוסות האלה. כל עוד המים נכנסים בכוסות ישראל
    עדיין יכולה לנצח; ברגע שיש יותר מים מנפח, כוס אחת לפחות עולה על גדותיה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **לחשב את הנפח:** לכל מדינה שעוד לא הוכרזה, המקום הפנוי הוא
       \( \mathit{room}_c = 343 - \mathit{jury}_c \). סוכמים את כולם.
    2. **לחשב את המים:** הנקודות שנותרו הן 2,088 פחות כל נקודות הקהל שכבר הוכרזו.
    3. **להשוות:** אם הנקודות שנותרו גדולות מסך המקום הפנוי, ישראל בוודאות לא תנצח.
    4. **אחרי כל הכרזה לעדכן:** מהמים יורדות נקודות הקהל של המדינה שהוכרזה, ומהנפח יורדת
       הכוס שלה **כולה**. חוזרים לשלב 3 עד שההשוואה נכשלת לראשונה.

    </div>

    #### למה זה נכון { .sol-proof }

    **כוסות ומים.** כל מדינה שעוד לא קיבלה נקודות קהל היא **כוס**. התחתית שלה היא ניקוד
    השופטים שלה, והשפה שלה היא 343, הניקוד של ישראל. הנפח הפנוי בכוס הוא

    \[
    \mathit{room}_c = 343 - \mathit{jury}_c
    \]

    נקודות הקהל שעוד לא הוכרזו הן **מים**, וכולם חייבים להישפך לכוסות האלה, כי הניקוד
    של כל מי שכבר הוכרז סופי.

    - **אם המים נכנסים בכוסות** (\( \mathit{left} \le \sum \mathit{room}_c \)), אפשר עדיין לחלק את הנקודות
      כך שאף מדינה לא תעבור את ישראל. כלומר, ישראל עדיין יכולה לנצח.
    - **אם יש יותר מים מנפח** (\( \mathit{left} > \sum \mathit{room}_c \)), לפי **עקרון שובך היונים** לפחות
      כוס אחת עולה על גדותיה. מדינה אחת לפחות תעבור את ישראל, וישראל בוודאות לא תנצח.

    **מה לגבי תיקו?** מדינה שמגיעה בדיוק ל-343 קיבלה מהקהל בדיוק \( \mathit{room}_c \) נקודות.
    הנפח הגדול ביותר כאן הוא של פולין: \( 343 - 133 = 210 \), וזה פחות מ-220 נקודות הקהל
    של ישראל. לכן בכל תיקו ישראל מנצחת, ומותר "למלא כוס עד השפה".

    **מיד אחרי ההכרזה של ישראל.** עד ישראל, כולל ישראל, הוכרזו 18 מדינות, והן קיבלו יחד
    1,260 נקודות קהל. לכן נשארו \( 2{,}088 - 1{,}260 = 828 \) נקודות. הנפח הפנוי של שבע
    המדינות שמעל ישראל:

    | מדינה | ‏Poland | ‏Italy | ‏Finland | ‏France | ‏Denmark | ‏Australia | ‏Bulgaria | סך הכול |
    |---|---|---|---|---|---|---|---|---|
    | שופטים | 133 | 134 | 141 | 144 | 165 | 165 | 204 | |
    | מקום פנוי | 210 | 209 | 202 | 199 | 178 | 178 | 139 | **1,315** |

    828 נקודות נכנסות בנפח של 1,315, ולכן ישראל עדיין יכולה לנצח:

    <span class="viz-legend"><span><i class="by-multiples"></i>ניקוד השופטים</span><span><i class="s3"></i>ניקוד הקהל (כבר הוכרז)</span><span><i class="cup-room"></i>מקום פנוי עד 343</span><span><i class="left-bar"></i>נקודות קהל שנותרו</span></span>

    <svg class="perf-chart" viewBox="0 0 640 330" role="img" aria-label="המקום הפנוי של כל מדינה עד 343 נקודות, מיד אחרי ההכרזה של ישראל"><line class="grid" x1="48" x2="630" y1="230.0" y2="230.0"/><text class="tick" x="40" y="234.0" text-anchor="end">0</text><line class="grid" x1="48" x2="630" y1="176.5" y2="176.5"/><text class="tick" x="40" y="180.5" text-anchor="end">100</text><line class="grid" x1="48" x2="630" y1="123.0" y2="123.0"/><text class="tick" x="40" y="127.0" text-anchor="end">200</text><line class="grid" x1="48" x2="630" y1="69.5" y2="69.5"/><text class="tick" x="40" y="73.5" text-anchor="end">300</text><line class="grid" x1="48" x2="630" y1="16.0" y2="16.0"/><text class="tick" x="40" y="20.0" text-anchor="end">400</text><rect class="bar by-multiples" x="66.3" y="158.8" width="46.6" height="71.2"><title>Poland: jury 133</title></rect><rect class="cup-room" x="66.3" y="46.5" width="46.6" height="112.3"><title>Poland: room 210</title></rect><text class="tick" x="89.6" y="106.7" text-anchor="middle">210</text><text class="tick" x="89.6" y="246" text-anchor="middle">Poland</text><rect class="bar by-multiples" x="149.4" y="158.3" width="46.6" height="71.7"><title>Italy: jury 134</title></rect><rect class="cup-room" x="149.4" y="46.5" width="46.6" height="111.8"><title>Italy: room 209</title></rect><text class="tick" x="172.7" y="106.4" text-anchor="middle">209</text><text class="tick" x="172.7" y="246" text-anchor="middle">Italy</text><rect class="bar by-multiples" x="232.6" y="154.6" width="46.6" height="75.4"><title>Finland: jury 141</title></rect><rect class="cup-room" x="232.6" y="46.5" width="46.6" height="108.1"><title>Finland: room 202</title></rect><text class="tick" x="255.9" y="104.5" text-anchor="middle">202</text><text class="tick" x="255.9" y="246" text-anchor="middle">Finland</text><rect class="bar by-multiples" x="315.7" y="153.0" width="46.6" height="77.0"><title>France: jury 144</title></rect><rect class="cup-room" x="315.7" y="46.5" width="46.6" height="106.5"><title>France: room 199</title></rect><text class="tick" x="339.0" y="103.7" text-anchor="middle">199</text><text class="tick" x="339.0" y="246" text-anchor="middle">France</text><rect class="bar by-multiples" x="398.9" y="141.7" width="46.6" height="88.3"><title>Denmark: jury 165</title></rect><rect class="cup-room" x="398.9" y="46.5" width="46.6" height="95.2"><title>Denmark: room 178</title></rect><text class="tick" x="422.1" y="98.1" text-anchor="middle">178</text><text class="tick" x="422.1" y="246" text-anchor="middle">Denmark</text><rect class="bar by-multiples" x="482.0" y="141.7" width="46.6" height="88.3"><title>Australia: jury 165</title></rect><rect class="cup-room" x="482.0" y="46.5" width="46.6" height="95.2"><title>Australia: room 178</title></rect><text class="tick" x="505.3" y="98.1" text-anchor="middle">178</text><text class="tick" x="505.3" y="246" text-anchor="middle">Australia</text><rect class="bar by-multiples" x="565.1" y="120.9" width="46.6" height="109.1"><title>Bulgaria: jury 204</title></rect><rect class="cup-room" x="565.1" y="46.5" width="46.6" height="74.4"><title>Bulgaria: room 139</title></rect><text class="tick" x="588.4" y="87.7" text-anchor="middle">139</text><text class="tick" x="588.4" y="246" text-anchor="middle">Bulgaria</text><line class="axis" x1="48" x2="630" y1="230" y2="230"/><line class="israel-line" x1="48" x2="630" y1="46.5" y2="46.5"/><text class="legend" x="52" y="40.5">Israel 343</text><rect class="cup-room" x="48" y="262" width="443.3" height="20"><title>room: 1315</title></rect><text class="legend" x="499.3" y="277">1315</text><rect class="left-bar" x="48" y="292" width="279.2" height="20"><title>left: 828</title></rect><text class="legend" x="335.2" y="307">828</text></svg>

    **צעד אחרי צעד.** אחרי כל הכרזה **שני** דברים משתנים: מהמים יורדות נקודות הקהל של
    המדינה, ומהנפח יורדת הכוס שלה כולה, כי היא כבר לא יכולה לקבל עוד נקודות.

    | אחרי ההכרזה של | ניקוד הקהל | סך הכול | נקודות שנותרו | מקום פנוי עד 343 | ישראל עדיין יכולה לנצח? |
    |---|---|---|---|---|---|
    | ‏Israel | 220 | 343 | 828 | 1315 | כן |
    | ‏Poland | 17 | 150 | 811 | 1105 | כן |
    | ‏Italy | 147 | 281 | 664 | 896 | כן |
    | ‏Finland | 138 | 279 | 526 | 694 | כן |
    | ‏France | 14 | 158 | 512 | 495 | **לא** |
    | ‏Denmark | 78 | 243 | 434 | 317 | **לא** |
    | ‏Australia | 122 | 287 | 312 | 139 | **לא** |
    | ‏Bulgaria | 312 | 516 | 0 | 0 | **לא** |

    **התשובה: מיד אחרי שצרפת קיבלה 14 נקודות מהקהל**, כשנותרו עוד שלוש הכרזות (דנמרק,
    אוסטרליה ובולגריה). באותו רגע נשארו 512 נקודות, אבל לשלוש המדינות היה מקום רק ל-495. גם
    בחלוקה הכי "טובה" לישראל, 17 נקודות עודפות מעבירות מישהי את ה-343.

    <svg class="perf-chart" viewBox="0 0 640 330" role="img" aria-label="המקום הפנוי של כל מדינה עד 343 נקודות, אחרי ההכרזה של צרפת"><line class="grid" x1="48" x2="630" y1="230.0" y2="230.0"/><text class="tick" x="40" y="234.0" text-anchor="end">0</text><line class="grid" x1="48" x2="630" y1="176.5" y2="176.5"/><text class="tick" x="40" y="180.5" text-anchor="end">100</text><line class="grid" x1="48" x2="630" y1="123.0" y2="123.0"/><text class="tick" x="40" y="127.0" text-anchor="end">200</text><line class="grid" x1="48" x2="630" y1="69.5" y2="69.5"/><text class="tick" x="40" y="73.5" text-anchor="end">300</text><line class="grid" x1="48" x2="630" y1="16.0" y2="16.0"/><text class="tick" x="40" y="20.0" text-anchor="end">400</text><rect class="bar by-multiples" x="66.3" y="158.8" width="46.6" height="71.2"><title>Poland: jury 133</title></rect><rect class="bar by-bfs" x="66.3" y="149.8" width="46.6" height="9.1"><title>Poland: public 17, total 150</title></rect><text class="tick" x="89.6" y="143.8" text-anchor="middle">150</text><text class="tick" x="89.6" y="246" text-anchor="middle">Poland</text><rect class="bar by-multiples" x="149.4" y="158.3" width="46.6" height="71.7"><title>Italy: jury 134</title></rect><rect class="bar by-bfs" x="149.4" y="79.7" width="46.6" height="78.6"><title>Italy: public 147, total 281</title></rect><text class="tick" x="172.7" y="73.7" text-anchor="middle">281</text><text class="tick" x="172.7" y="246" text-anchor="middle">Italy</text><rect class="bar by-multiples" x="232.6" y="154.6" width="46.6" height="75.4"><title>Finland: jury 141</title></rect><rect class="bar by-bfs" x="232.6" y="80.7" width="46.6" height="73.8"><title>Finland: public 138, total 279</title></rect><text class="tick" x="255.9" y="74.7" text-anchor="middle">279</text><text class="tick" x="255.9" y="246" text-anchor="middle">Finland</text><rect class="bar by-multiples" x="315.7" y="153.0" width="46.6" height="77.0"><title>France: jury 144</title></rect><rect class="bar by-bfs" x="315.7" y="145.5" width="46.6" height="7.5"><title>France: public 14, total 158</title></rect><text class="tick" x="339.0" y="139.5" text-anchor="middle">158</text><text class="tick" x="339.0" y="246" text-anchor="middle">France</text><rect class="bar by-multiples" x="398.9" y="141.7" width="46.6" height="88.3"><title>Denmark: jury 165</title></rect><rect class="cup-room" x="398.9" y="46.5" width="46.6" height="95.2"><title>Denmark: room 178</title></rect><text class="tick" x="422.1" y="98.1" text-anchor="middle">178</text><text class="tick" x="422.1" y="246" text-anchor="middle">Denmark</text><rect class="bar by-multiples" x="482.0" y="141.7" width="46.6" height="88.3"><title>Australia: jury 165</title></rect><rect class="cup-room" x="482.0" y="46.5" width="46.6" height="95.2"><title>Australia: room 178</title></rect><text class="tick" x="505.3" y="98.1" text-anchor="middle">178</text><text class="tick" x="505.3" y="246" text-anchor="middle">Australia</text><rect class="bar by-multiples" x="565.1" y="120.9" width="46.6" height="109.1"><title>Bulgaria: jury 204</title></rect><rect class="cup-room" x="565.1" y="46.5" width="46.6" height="74.4"><title>Bulgaria: room 139</title></rect><text class="tick" x="588.4" y="87.7" text-anchor="middle">139</text><text class="tick" x="588.4" y="246" text-anchor="middle">Bulgaria</text><line class="axis" x1="48" x2="630" y1="230" y2="230"/><line class="israel-line" x1="48" x2="630" y1="46.5" y2="46.5"/><text class="legend" x="52" y="40.5">Israel 343</text><rect class="cup-room" x="48" y="262" width="166.9" height="20"><title>room: 495</title></rect><text class="legend" x="222.9" y="277">495</text><rect class="left-bar" x="48" y="292" width="172.6" height="20"><title>left: 512</title></rect><text class="legend" x="228.6" y="307">512 = 495 + 17</text><rect class="overflow" x="214.9" y="292" width="5.7" height="20"><title>overflow: 17</title></rect><line class="israel-line" x1="214.9" x2="214.9" y1="256" y2="318"/></svg>

    הגרף הבא מראה את שני הגדלים אחרי כל הכרזה. ישראל בחוץ מהרגע שהקו של הנקודות שנותרו
    עובר את הקו של המקום הפנוי:

    <span class="viz-legend"><span><i class="s2"></i>מקום פנוי עד 343</span><span><i class="ink"></i>נקודות קהל שנותרו</span></span>

    <svg class="perf-chart" viewBox="0 0 640 290" role="img" aria-label="המקום הפנוי מול הנקודות שנותרו אחרי כל הכרזה"><line class="grid" x1="56" x2="630" y1="250.0" y2="250.0"/><text class="tick" x="48" y="254.0" text-anchor="end">0</text><line class="grid" x1="56" x2="630" y1="216.6" y2="216.6"/><text class="tick" x="48" y="220.6" text-anchor="end">200</text><line class="grid" x1="56" x2="630" y1="183.1" y2="183.1"/><text class="tick" x="48" y="187.1" text-anchor="end">400</text><line class="grid" x1="56" x2="630" y1="149.7" y2="149.7"/><text class="tick" x="48" y="153.7" text-anchor="end">600</text><line class="grid" x1="56" x2="630" y1="116.3" y2="116.3"/><text class="tick" x="48" y="120.3" text-anchor="end">800</text><line class="grid" x1="56" x2="630" y1="82.9" y2="82.9"/><text class="tick" x="48" y="86.9" text-anchor="end">1000</text><line class="grid" x1="56" x2="630" y1="49.4" y2="49.4"/><text class="tick" x="48" y="53.4" text-anchor="end">1200</text><line class="grid" x1="56" x2="630" y1="16.0" y2="16.0"/><text class="tick" x="48" y="20.0" text-anchor="end">1400</text><rect class="lost-zone" x="328.0" y="16" width="302.0" height="234"/><text class="legend" x="372.0" y="34">France: 512 &gt; 495</text><text class="tick" x="76.0" y="268" text-anchor="middle">Israel</text><text class="tick" x="148.0" y="268" text-anchor="middle">Poland</text><text class="tick" x="220.0" y="268" text-anchor="middle">Italy</text><text class="tick" x="292.0" y="268" text-anchor="middle">Finland</text><text class="tick" x="364.0" y="268" text-anchor="middle">France</text><text class="tick" x="436.0" y="268" text-anchor="middle">Denmark</text><text class="tick" x="508.0" y="268" text-anchor="middle">Australia</text><text class="tick" x="580.0" y="268" text-anchor="middle">Bulgaria</text><path class="s2-line" d="M76.0,30.2 L148.0,65.3 L220.0,100.2 L292.0,134.0 L364.0,167.3 L436.0,197.0 L508.0,226.8 L580.0,250.0" fill="none" stroke-width="2"/><circle class="s2-dot" cx="76.0" cy="30.2" r="4"><title>after Israel: room 1315</title></circle><circle class="s2-dot" cx="148.0" cy="65.3" r="4"><title>after Poland: room 1105</title></circle><circle class="s2-dot" cx="220.0" cy="100.2" r="4"><title>after Italy: room 896</title></circle><circle class="s2-dot" cx="292.0" cy="134.0" r="4"><title>after Finland: room 694</title></circle><circle class="s2-dot" cx="364.0" cy="167.3" r="4"><title>after France: room 495</title></circle><circle class="s2-dot" cx="436.0" cy="197.0" r="4"><title>after Denmark: room 317</title></circle><circle class="s2-dot" cx="508.0" cy="226.8" r="4"><title>after Australia: room 139</title></circle><circle class="s2-dot" cx="580.0" cy="250.0" r="4"><title>after Bulgaria: room 0</title></circle><path class="ink-line" d="M76.0,111.6 L148.0,114.4 L220.0,139.0 L292.0,162.1 L364.0,164.4 L436.0,177.5 L508.0,197.9 L580.0,250.0" fill="none" stroke-width="2"/><circle class="ink-dot" cx="76.0" cy="111.6" r="4"><title>after Israel: points left 828</title></circle><circle class="ink-dot" cx="148.0" cy="114.4" r="4"><title>after Poland: points left 811</title></circle><circle class="ink-dot" cx="220.0" cy="139.0" r="4"><title>after Italy: points left 664</title></circle><circle class="ink-dot" cx="292.0" cy="162.1" r="4"><title>after Finland: points left 526</title></circle><circle class="ink-dot" cx="364.0" cy="164.4" r="4"><title>after France: points left 512</title></circle><circle class="ink-dot" cx="436.0" cy="177.5" r="4"><title>after Denmark: points left 434</title></circle><circle class="ink-dot" cx="508.0" cy="197.9" r="4"><title>after Australia: points left 312</title></circle><circle class="ink-dot" cx="580.0" cy="250.0" r="4"><title>after Bulgaria: points left 0</title></circle><line class="axis" x1="56" x2="630" y1="250" y2="250"/></svg>

    **נסו בעצמכם.** הזיזו את ה-slider הכרזה אחרי הכרזה: כל מדינה שעוד לא הוכרזה היא כוס
    עם מקום פנוי עד 343, ומדינה שהוכרזה מקבלת את הקהל שלה. הרגע שבו יש יותר נקודות ממקום
    מסומן באדום. בתיבת "מה אם" אפשר לשנות את ניקוד השופטים או הקהל של ישראל ולראות איך
    הרגע זז, ואיפה ישראל הייתה מנצחת.

    <div class="explorer" data-kind="eurovision"></div>

    **למה דווקא צרפת?** אחרי כל הכרזה ההפרש \( \sum \mathit{room} - \mathit{left} \) קטן
    בדיוק ב-\( 343 - \mathit{total}_c \), כלומר במרחק של המדינה שהוכרזה מהניקוד של ישראל. צרפת סיימה עם 158
    בלבד, ולכן "בזבזה" 185 נקודות של מקום פנוי בבת אחת: ההפרש ירד מ-168 ל-\( -17 \).

    לאוסטרליה ולדנמרק היו 165 נקודות שופטים לכל אחת. בטבלת השופטים אוסטרליה דורגה שנייה
    ודנמרק שלישית, ולכן דנמרק קיבלה את נקודות הקהל לפני אוסטרליה. הסדר ביניהן לא משנה את
    התשובה, כי ההכרעה מגיעה לפני שתיהן.

---

### סעיף ב – כתבו את הקוד

כתבו פונקציה שמקבלת את הנתונים שידועים ברגע מסוים, ומחזירה האם ישראל **בוודאות** לא
תנצח:

- ‏`israel_total` – הניקוד של ישראל אחרי השופטים והקהל (343).
- ‏`jury_above` – ניקוד השופטים של המדינות שעוד לא קיבלו נקודות קהל.
- ‏`points_left` – כמה נקודות קהל עוד לא הוכרזו.

אחר כך כתבו פונקציה שעוברת על ההכרזות שאחרי ישראל, לפי הסדר, ומחזירה אחרי כמה הכרזות
ההפסד של ישראל הפך לוודאי. עבור נתוני 2026 התשובה היא 4 (צרפת).

האלגוריתם צריך להיות פשוט ויעיל: מעבר אחד על הנתונים.

??? tip "רמז 1"
    תרגמו את פתרון סעיף א לנוסחה: איזה סכום מחשבים מתוך `jury_above`, ולמה משווים אותו?
    זו כבר הפונקציה הראשונה.

??? tip "רמז 2"
    בסריקה אין צורך לחשב הכול מחדש אחרי כל הכרזה. מה בדיוק משתנה בנפח ובמים כשמדינה אחת
    מקבלת את נקודות הקהל שלה?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **השוואה אחת:** ההפסד ודאי כאשר `points_left` גדול מסכום המקום הפנוי
        \( \sum (343 - \mathit{jury}_c) \) של המדינות שעוד לא הוכרזו, או כשמדינה כבר עברה את
        343. בסריקה מעדכנים את שני הסכומים אחרי כל הכרזה, ב-\( O(k) \); עבור נתוני 2026
        מוחזר **4**.

    #### הרעיון { .sol-idea }

    הבדיקה ברגע אחד היא בדיוק הנימוק של סעיף א: סוכמים את המקום הפנוי ומשווים לנקודות
    שנותרו. בסריקה לא קוראים לבדיקה מחדש אחרי כל הכרזה, אלא מעדכנים את שני הסכומים
    בצורה מצטברת.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הבדיקה ברגע אחד:** עוברים על `jury_above`. אם מדינה כבר עברה את ישראל עם ניקוד
       השופטים בלבד, מחזירים "ודאי" מיד; אחרת מוסיפים את \( 343 - \mathit{jury} \) שלה
       ל-`room`. בסוף מחזירים `points_left > room`.
    2. **לפני הסריקה:** מחשבים את `room` ההתחלתי, ובודקים אם ההפסד ודאי כבר מיד אחרי
       ההכרזה של ישראל (תשובה 0).
    3. **לכל הכרזה בתור:** מורידים מ-`points_left` את נקודות הקהל של המדינה, ומורידים
       מ-`room` את המקום הפנוי שלה, \( 343 - \mathit{jury} \).
    4. **לבדוק שני תנאים:** אם המדינה שהוכרזה עברה את ישראל, או ש-`points_left > room`,
       מחזירים את מספר ההכרזה. אם הסריקה נגמרת בלי זה, ישראל ניצחה.

    </div>

    #### הקוד { .sol-code }

    **הבדיקה ברגע אחד, \( O(k) \).** סוכמים את המקום הפנוי של כל המדינות שמעל ישראל,
    ומשווים לנקודות שנותרו. אם מדינה כבר עברה את ישראל רק עם ניקוד השופטים, ההפסד ודאי מיד.

    === "SystemVerilog"
        ```systemverilog title="function israel_cannot_win" hl_lines="7 9"
        // True when the public points still to come cannot be shared among the countries
        // above Israel without at least one of them passing Israel's total.
        function automatic bit israel_cannot_win(int israel_total, int jury_above[$], int points_left);
          int room = 0;                                  // points they can take and stay <= Israel
          foreach (jury_above[i]) begin
            if (jury_above[i] > israel_total) return 1;  // already ahead before any public points (1)
            room += israel_total - jury_above[i];
          end
          return points_left > room;                     // pigeonhole: someone must pass Israel (2)
        endfunction
        ```

        1. בלי הבדיקה הזו מדינה שכבר מעל ישראל הייתה תורמת מקום פנוי **שלילי**, מקטינה את
           `room` ומסתירה את העובדה שישראל כבר הפסידה.
        2. ההשוואה היא `>` ולא `>=`: מילוי כוס בדיוק עד השפה הוא תיקו, ובתיקו ישראל מנצחת
           (ראו סעיף א). אם שובר השוויון היה הפוך, היה צריך להקטין כל כוס ב-1.

    === "Python"
        ```python title="israel_cannot_win" hl_lines="8 9"
        def israel_cannot_win(israel_total, jury_above, points_left):
            """True when the public points still to come cannot be shared among the countries
            above Israel without at least one of them passing Israel's total."""
            room = 0                                   # points they can take and stay <= Israel
            for jury in jury_above:
                if jury > israel_total:                # already ahead before any public points (1)
                    return True
                room += israel_total - jury
            return points_left > room                  # pigeonhole: someone must pass Israel (2)
        ```

        1. מדינה שכבר מעל ישראל לא תורמת מקום פנוי שלילי; ההפסד ודאי מיד.
        2. ‏`>` ולא `>=`, כי בתיקו ישראל מנצחת.

    **הסריקה על ההכרזות, גם היא \( O(k) \).** אפשר לקרוא לבדיקה מחדש אחרי כל הכרזה, אבל
    זה \( O(k^2) \). במקום זה מעדכנים את שני הסכומים: כשמדינה מקבלת `public` נקודות,
    הנקודות שנותרו יורדות ב-`public`, והמקום הפנוי יורד במקום של הכוס שלה, \( 343 - jury \).
    צריך לבדוק גם מקרה אחד נוסף: אם המדינה שהוכרזה עברה את ישראל, ההפסד ודאי.

    === "SystemVerilog"
        ```systemverilog title="function earliest_certain_loss" linenums="1" hl_lines="20 21 22"
        typedef struct {
          string country;
          int    jury;
          int    public_pts;
        } country_t;

        // above: the countries ranked above Israel by the jury, in announcement order, with the
        // public points each one got. Returns how many of them had been announced when Israel's
        // loss became certain (0 = right after Israel's own turn), or -1 when Israel won.
        function automatic int earliest_certain_loss(int israel_total, country_t above[$],
                                                     int points_left);
          int room = 0;
          foreach (above[i]) begin
            if (above[i].jury > israel_total) return 0;
            room += israel_total - above[i].jury;
          end
          if (points_left > room) return 0;   // (1)!

          foreach (above[k]) begin
            points_left -= above[k].public_pts;           // this country got its public points,
            room        -= israel_total - above[k].jury;  // so its room is no longer free (2)
            if (above[k].jury + above[k].public_pts > israel_total || points_left > room)   // (3)!
              return k + 1;   // (4)!
          end
          return -1;                                      // nobody passed Israel: Israel won
        endfunction
        ```

        1. הבדיקה "ברגע אפס", מיד אחרי ההכרזה של ישראל ולפני שמישהי מעליה קיבלה נקודות.
           בלי זה הסריקה הייתה מפספסת הפסד שכבר ודאי מההתחלה.
        2. מהנפח יורדת הכוס **כולה**, \( 343 - \mathit{jury} \), ולא רק הנקודות שהמדינה
           קיבלה בפועל: אחרי ההכרזה היא כבר לא יכולה לבלוע כלום.
        3. שני התנאים, בסדר הזה: מדינה שעברה את ישראל (למשל כוס שעלתה על גדותיה) מכריעה
           גם כשהחשבון של הנפח עדיין נראה בסדר, כי הנקודות העודפות שלה כבר לא "במים".
        4. ‏`k` מתחיל מ-0, והשאלה סופרת הכרזות, ולכן מחזירים `k + 1`. עבור נתוני 2026 צרפת
           היא `above[3]`, והתשובה 4.

    === "Python"
        ```python title="earliest_certain_loss" linenums="1" hl_lines="14 15 16"
        def earliest_certain_loss(israel_total, above, points_left):
            """above: (country, jury, public) for the countries ranked above Israel by the jury,
            in announcement order. Returns how many of them had been announced when Israel's
            loss became certain (0 = right after Israel's own turn), or None when Israel won."""
            room = 0
            for _, jury, _ in above:
                if jury > israel_total:
                    return 0
                room += israel_total - jury
            if points_left > room:   # (1)!
                return 0

            for k, (_, jury, public) in enumerate(above, start=1):
                points_left -= public                  # this country got its public points,
                room -= israel_total - jury            # so its room is no longer free (2)
                if jury + public > israel_total or points_left > room:   # (3)!
                    return k
            return None                                # nobody passed Israel: Israel won
        ```

        1. הבדיקה ברגע אפס, לפני הסריקה.
        2. יורדת הכוס כולה, לא רק הנקודות שהתקבלו בפועל.
        3. שני התנאים: מדינה שעברה את ישראל, או יותר מים מנפח. כאן `enumerate` מתחיל מ-1,
           ולכן `k` הוא כבר מספר ההכרזה.

    #### למה זה נכון { .sol-proof }

    הבדיקה ברגע אחד היא בדיוק טיעון הכוסות של סעיף א, ולכן היא נכונה לשני הכיוונים. בסריקה,
    אחרי כל הכרזה שני הסכומים שווים בדיוק למה שהבדיקה הייתה מחשבת מאפס: הנקודות שנותרו הן
    הסכום הקודם פחות `public`, והמקום הפנוי הוא הסכום הקודם פחות הכוס של המדינה שיצאה
    מהמשחק. התנאי הנוסף מכסה מדינה שכבר עברה את ישראל, כי הנקודות שלה כבר לא חלק מהמים.

    עם נתוני 2026: `israel_total = 343`, `points_left = 828`, והרשימה `above` היא פולין,
    איטליה, פינלנד, צרפת, דנמרק, אוסטרליה ובולגריה עם ניקוד השופטים והקהל שלהן. הפונקציה
    מחזירה 4, כלומר ההפסד ודאי אחרי ההכרזה הרביעית שאחרי ישראל, של צרפת, בדיוק כמו בטבלה
    של סעיף א.

    #### סיבוכיות { .sol-cost }

    זמן \( O(k) \), כאשר \( k \) הוא מספר המדינות שמעל ישראל, וזיכרון \( O(1) \): שני
    משתנים בלבד, `room` ו-`points_left`. קריאה חוזרת לבדיקה אחרי כל הכרזה הייתה נותנת
    \( O(k^2) \); העדכון המצטבר חוסך את זה, כי אחרי כל הכרזה משתנים רק שני מספרים.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: להתעלם משובר השוויון"
    את שובר השוויון בודקים במפורש ולא מניחים. כאן ישראל מנצחת בכל תיקו, ולכן
    \( \mathit{room}_c = 343 - \mathit{jury}_c \) וההשוואה היא `>`. אם מדינה מנצחת את ישראל
    בתיקו, הנפח שלה קטן ב-1, ותשובה שמתעלמת מזה עלולה לפספס רגע אחד.

??? trap "מלכודת: להוריד מהנפח רק את הנקודות שהתקבלו"
    אחרי הכרזה המדינה יוצאת מהמשחק, ולכן מהמקום הפנוי יורדת **הכוס כולה**,
    \( 343 - \mathit{jury} \), ולא רק נקודות הקהל שהיא קיבלה בפועל. זה בדיוק מה שהופך את
    צרפת למכריעה: מהמים ירדו רק 14 נקודות, אבל מהנפח ירדה כוס שלמה של 199.

??? followup "שאלות המשך"
    - **האם התשובה מדויקת?** המודל מתעלם מכך שכל מצביע נותן נקודות לעשר מדינות **שונות**,
      ושמדינה יכולה לקבל מהקהל לכל היותר \( 36 \times 12 = 432 \). הוספת אילוצים רק מצמצמת
      את האפשרויות, ולכן אם במודל הפשוט ישראל הפסידה בוודאות, היא הפסידה בוודאות גם במציאות.
      במציאות ההפסד יכול להיות ודאי **מוקדם יותר**, אבל לעולם לא מאוחר יותר.
    - **מתי היה ודאי שבולגריה מנצחת?** רק אחרי ההכרזה של אוסטרליה, שלפני האחרונה. בולגריה
      הוכרזה אחרונה, ולכן ברגע הזה כל 312 הנקודות שנותרו היו שלה: \( 204 + 312 = 516 \).
      רגע אחד קודם, אחרי דנמרק, נשארו 434 נקודות לאוסטרליה ולבולגריה. אם כולן היו הולכות
      לאוסטרליה, היא הייתה מגיעה ל-599 ועוקפת את בולגריה.
    - **הכללה:** כתבו פונקציה שמחזירה, אחרי כל הכרזה, את רשימת כל המדינות שעוד יכולות
      לנצח.
