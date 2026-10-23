---
id: 32
title: זאב, עז וכרוב – חציית הנהר
level: student
difficulty: easy
tags: [logic-puzzles, algorithms, bfs, python, systemverilog]
source: ""
added: 2026-10-20
---

## השאלה

איכר צריך להעביר **זאב**, **עז** ו**כרוב** מעבר לנהר. הסירה מכילה את האיכר ועוד **אחד**
בלבד (הזאב, העז או הכרוב), והאיכר חייב לחתור. אם משאירים את הזאב עם העז בלי האיכר, הזאב
אוכל את העז; אם משאירים את העז עם הכרוב בלי האיכר, העז אוכלת את הכרוב. הזאב לא אוכל כרוב.

<!-- gen 0 -->

<svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="האיכר, הזאב, העז והכרוב על הגדה הקרובה, והסירה לידם"><rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/><rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text><g><circle class="st-stack" cx="45" cy="70" r="18"/><text class="st-text" x="45" y="75" text-anchor="middle">F</text></g><g><circle class="st-cell" cx="85" cy="70" r="18"/><text class="st-text" x="85" y="75" text-anchor="middle">W</text></g><g><circle class="st-cell" cx="125" cy="70" r="18"/><text class="st-text" x="125" y="75" text-anchor="middle">G</text></g><g><circle class="st-cell" cx="165" cy="70" r="18"/><text class="st-text" x="165" y="75" text-anchor="middle">C</text></g><rect class="boat" x="165" y="100" width="100" height="26" rx="10"/></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="st-stack"></i>האיכר (F)</span><span><i class="st-cell"></i>הזאב (W), העז (G) והכרוב (C)</span><span><i class="boat"></i>הסירה : האיכר ועוד אחד</span></span>

<!-- /gen -->

??? interviewer "מה המראיין בודק"
    - **לחשוב לאחור מהמגבלה :** מי לא יכול להישאר עם מי, ומכאן מי חייב לנסוע ראשון.
    - **הנכונות להחזיר משהו :** הצעד הלא אינטואיטיבי, להחזיר את העז, ואם המועמד נתקע
      כשהכול נראה "כבר בדרך".
    - **מרחב מצבים :** בסעיף ב, האם המועמד מתאר את המצב במספר קטן של ביטים, סופר את
      המצבים, ומזהה חיפוש בגרף.
    - **שלמות ומינימליות :** למה שבע חציות הן המינימום, ולמה אין פתרון אחר (חוץ מהמראה).

---

### סעיף א – התוכנית

מצאו סדר חציות שמעביר את שלושתם בשלום. כמה חציות צריך לכל הפחות?

??? tip "רמז 1"
    מי יכול להישאר לבד עם מי? יש רק זוג אחד שבטוח להשאיר.

??? tip "רמז 2"
    העז היא הבעיה : היא מסוכנת לכרוב ובסכנה מהזאב. לכן היא נוסעת ראשונה. מה עושים אחרי
    שהאיכר חוזר ולוקח את הזאב, כשהזאב והעז עומדים להישאר יחד בצד הרחוק?

??? tip "רמז 3"
    מותר להחזיר משהו לצד הקרוב.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שבע חציות : האיכר לוקח את העז, חוזר לבד, לוקח את הזאב, **מחזיר את העז**, לוקח את
        הכרוב, חוזר לבד, ולוקח את העז. אפשר גם להחליף את הזאב והכרוב בתפקידים. פחות משבע
        אי אפשר.

    #### הרעיון { .sol-idea }

    הזוג היחיד שבטוח להשאיר לבד הוא הזאב והכרוב. לכן העז חייבת להיות תמיד או עם האיכר או
    לבד. בחצייה הראשונה האיכר לוקח את העז (כל בחירה אחרת משאירה אותה עם מישהו שאסור).
    אחרי שהוא מביא את הזאב, הזאב והעז עומדים להישאר יחד, ולכן האיכר **לוקח את העז חזרה**
    איתו. זה הצעד שאנשים מפספסים : נדמה שהוא "מבזבז" חצייה, אבל בלעדיו אין פתרון.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **העז קדימה :** על הגדה הקרובה נשארים הזאב והכרוב, וזה בטוח.
    2. **האיכר חוזר לבד :** העז לבד בצד הרחוק.
    3. **הזאב קדימה :** אם האיכר יחזור עכשיו, הזאב יאכל את העז.
    4. **העז חזרה :** האיכר מחזיר את העז. בצד הרחוק נשאר הזאב לבד.
    5. **הכרוב קדימה :** בצד הרחוק הזאב והכרוב, וזה בטוח. על הגדה הקרובה העז לבד.
    6. **האיכר חוזר לבד.**
    7. **העז קדימה :** כולם בצד הרחוק.

    </div>

    #### למה זה נכון { .sol-proof }

    **חצייה אחרי חצייה.** לחצו "הבא" כדי לעקוב : מי בסירה, ומי נשאר על כל גדה :

    <!-- gen 2 -->

    <div class="stepper" role="group" aria-label="שבע החציות של האיכר, חצייה אחרי חצייה" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="התחלה : כולם על הגדה הקרובה"><rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/><rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text><g><circle class="st-stack" cx="45" cy="70" r="18"/><text class="st-text" x="45" y="75" text-anchor="middle">F</text></g><g><circle class="st-cell" cx="85" cy="70" r="18"/><text class="st-text" x="85" y="75" text-anchor="middle">W</text></g><g><circle class="st-cell" cx="125" cy="70" r="18"/><text class="st-text" x="125" y="75" text-anchor="middle">G</text></g><g><circle class="st-cell" cx="165" cy="70" r="18"/><text class="st-text" x="165" y="75" text-anchor="middle">C</text></g><rect class="boat" x="165" y="100" width="100" height="26" rx="10"/></svg><figcaption>רגע 0 : כולם על הגדה הקרובה. הסירה מכילה את האיכר ועוד אחד.</figcaption></figure><figure class="stepper-frame"><svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 1"><rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/><rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="45" cy="70" r="18"/><text class="st-text" x="45" y="75" text-anchor="middle">W</text></g><g><circle class="st-cell" cx="85" cy="70" r="18"/><text class="st-text" x="85" y="75" text-anchor="middle">C</text></g><rect class="boat" x="270" y="100" width="100" height="26" rx="10"/><g><circle class="st-stack" cx="300" cy="93" r="18"/><text class="st-text" x="300" y="98" text-anchor="middle">F</text></g><g><circle class="st-cell" cx="340" cy="93" r="18"/><text class="st-text" x="340" y="98" text-anchor="middle">G</text></g><line class="ink-line" x1="250" y1="150" x2="390" y2="150" stroke-width="2"/><polygon class="ink-fill" points="390,150 381,145 381,155"/></svg><figcaption>חצייה 1 : האיכר לוקח את העז קדימה. על הגדה שעזב נשארים הזאב, הכרוב, וזה בטוח.</figcaption></figure><figure class="stepper-frame"><svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 2"><rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/><rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="45" cy="70" r="18"/><text class="st-text" x="45" y="75" text-anchor="middle">W</text></g><g><circle class="st-cell" cx="85" cy="70" r="18"/><text class="st-text" x="85" y="75" text-anchor="middle">C</text></g><g><circle class="st-cell" cx="485" cy="70" r="18"/><text class="st-text" x="485" y="75" text-anchor="middle">G</text></g><rect class="boat" x="270" y="100" width="100" height="26" rx="10"/><g><circle class="st-stack" cx="320" cy="93" r="18"/><text class="st-text" x="320" y="98" text-anchor="middle">F</text></g><line class="ink-line" x1="390" y1="150" x2="250" y2="150" stroke-width="2"/><polygon class="ink-fill" points="250,150 259,145 259,155"/></svg><figcaption>חצייה 2 : האיכר חוזר לבד חזרה. על הגדה שעזב נשארים העז, וזה בטוח.</figcaption></figure><figure class="stepper-frame"><svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 3"><rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/><rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="45" cy="70" r="18"/><text class="st-text" x="45" y="75" text-anchor="middle">C</text></g><g><circle class="st-cell" cx="485" cy="70" r="18"/><text class="st-text" x="485" y="75" text-anchor="middle">G</text></g><rect class="boat" x="270" y="100" width="100" height="26" rx="10"/><g><circle class="st-stack" cx="300" cy="93" r="18"/><text class="st-text" x="300" y="98" text-anchor="middle">F</text></g><g><circle class="st-cell" cx="340" cy="93" r="18"/><text class="st-text" x="340" y="98" text-anchor="middle">W</text></g><line class="ink-line" x1="250" y1="150" x2="390" y2="150" stroke-width="2"/><polygon class="ink-fill" points="390,150 381,145 381,155"/></svg><figcaption>חצייה 3 : האיכר לוקח את הזאב קדימה. על הגדה שעזב נשארים הכרוב, וזה בטוח.</figcaption></figure><figure class="stepper-frame"><svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 4"><rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/><rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="45" cy="70" r="18"/><text class="st-text" x="45" y="75" text-anchor="middle">C</text></g><g><circle class="st-cell" cx="485" cy="70" r="18"/><text class="st-text" x="485" y="75" text-anchor="middle">W</text></g><rect class="boat" x="270" y="100" width="100" height="26" rx="10"/><g><circle class="st-stack" cx="300" cy="93" r="18"/><text class="st-text" x="300" y="98" text-anchor="middle">F</text></g><g><circle class="st-cell" cx="340" cy="93" r="18"/><text class="st-text" x="340" y="98" text-anchor="middle">G</text></g><line class="ink-line" x1="390" y1="150" x2="250" y2="150" stroke-width="2"/><polygon class="ink-fill" points="250,150 259,145 259,155"/></svg><figcaption>חצייה 4 : האיכר לוקח את העז חזרה. על הגדה שעזב נשארים הזאב, וזה בטוח.</figcaption></figure><figure class="stepper-frame"><svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 5"><rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/><rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="45" cy="70" r="18"/><text class="st-text" x="45" y="75" text-anchor="middle">G</text></g><g><circle class="st-cell" cx="485" cy="70" r="18"/><text class="st-text" x="485" y="75" text-anchor="middle">W</text></g><rect class="boat" x="270" y="100" width="100" height="26" rx="10"/><g><circle class="st-stack" cx="300" cy="93" r="18"/><text class="st-text" x="300" y="98" text-anchor="middle">F</text></g><g><circle class="st-cell" cx="340" cy="93" r="18"/><text class="st-text" x="340" y="98" text-anchor="middle">C</text></g><line class="ink-line" x1="250" y1="150" x2="390" y2="150" stroke-width="2"/><polygon class="ink-fill" points="390,150 381,145 381,155"/></svg><figcaption>חצייה 5 : האיכר לוקח את הכרוב קדימה. על הגדה שעזב נשארים העז, וזה בטוח.</figcaption></figure><figure class="stepper-frame"><svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 6"><rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/><rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="45" cy="70" r="18"/><text class="st-text" x="45" y="75" text-anchor="middle">G</text></g><g><circle class="st-cell" cx="485" cy="70" r="18"/><text class="st-text" x="485" y="75" text-anchor="middle">W</text></g><g><circle class="st-cell" cx="525" cy="70" r="18"/><text class="st-text" x="525" y="75" text-anchor="middle">C</text></g><rect class="boat" x="270" y="100" width="100" height="26" rx="10"/><g><circle class="st-stack" cx="320" cy="93" r="18"/><text class="st-text" x="320" y="98" text-anchor="middle">F</text></g><line class="ink-line" x1="390" y1="150" x2="250" y2="150" stroke-width="2"/><polygon class="ink-fill" points="250,150 259,145 259,155"/></svg><figcaption>חצייה 6 : האיכר חוזר לבד חזרה. על הגדה שעזב נשארים הזאב, הכרוב, וזה בטוח.</figcaption></figure><figure class="stepper-frame"><svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 7"><rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/><rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="485" cy="70" r="18"/><text class="st-text" x="485" y="75" text-anchor="middle">W</text></g><g><circle class="st-cell" cx="525" cy="70" r="18"/><text class="st-text" x="525" y="75" text-anchor="middle">C</text></g><rect class="boat" x="270" y="100" width="100" height="26" rx="10"/><g><circle class="st-stack" cx="300" cy="93" r="18"/><text class="st-text" x="300" y="98" text-anchor="middle">F</text></g><g><circle class="st-cell" cx="340" cy="93" r="18"/><text class="st-text" x="340" y="98" text-anchor="middle">G</text></g><line class="ink-line" x1="250" y1="150" x2="390" y2="150" stroke-width="2"/><polygon class="ink-fill" points="390,150 381,145 381,155"/></svg><figcaption>חצייה 7 : האיכר לוקח את העז קדימה. הגדה שעזב ריקה.</figcaption></figure><figure class="stepper-frame"><svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="סיום"><rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/><rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text><g><circle class="st-stack" cx="485" cy="70" r="18"/><text class="st-text" x="485" y="75" text-anchor="middle">F</text></g><g><circle class="st-cell" cx="525" cy="70" r="18"/><text class="st-text" x="525" y="75" text-anchor="middle">W</text></g><g><circle class="st-cell" cx="565" cy="70" r="18"/><text class="st-text" x="565" y="75" text-anchor="middle">G</text></g><g><circle class="st-cell" cx="605" cy="70" r="18"/><text class="st-text" x="605" y="75" text-anchor="middle">C</text></g><rect class="boat" x="315" y="100" width="100" height="26" rx="10"/></svg><figcaption>כולם על הגדה הרחוקה אחרי 7 חציות.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="9"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <!-- /gen -->

    <!-- gen 3 -->

    | חצייה | מי בסירה | לאן | הגדה הקרובה אחרי | הגדה הרחוקה אחרי |
    |:-:|---|---|:-:|:-:|
    | 1 | האיכר והעז | קדימה | ‏WC | ‏FG |
    | 2 | האיכר לבד | חזרה | ‏FWC | ‏G |
    | 3 | האיכר והזאב | קדימה | ‏C | ‏FWG |
    | 4 | האיכר והעז | חזרה | ‏FGC | ‏W |
    | 5 | האיכר והכרוב | קדימה | ‏G | ‏FWC |
    | 6 | האיכר לבד | חזרה | ‏FG | ‏WC |
    | 7 | האיכר והעז | קדימה | ‏– | ‏FWGC |

    <!-- /gen -->

    **למה שבע.** כל חצייה קדימה מעבירה לכל היותר פריט אחד, ולכן צריך לפחות שלוש חציות
    קדימה, ובין כל שתיים חצייה חזרה : חמש לפחות. בחמש חציות כל חצייה קדימה מעבירה פריט
    וכל חצייה חזרה היא לבד. החצייה הראשונה חייבת להיות העז (אחרת היא נשארת עם הזאב או עם
    הכרוב), ואחרי החזרה לבד האיכר מביא פריט שני, ואז בצד הרחוק העז עם הזאב או עם הכרוב
    בלי האיכר. לכן אחת החזרות היא עם פריט, וזה מוסיף חצייה קדימה : שבע לפחות. הגרף של
    סעיף ב מאשר : המסלול הקצר ביותר הוא באורך שבע, ויש בדיוק שניים כאלה.

    #### סיבוכיות { .sol-cost }

    ארבעה "דברים" בשני צדדים : \( 2^4 = 16 \) מצבים, ורק עשרה מהם בטוחים. זה מספיק קטן
    כדי לצייר את כל הגרף ביד.

---

### סעיף ב – קוד : מציאת התוכנית בחיפוש

כתבו פונקציה שמחזירה את סדר החציות, בלי לדעת את הפתרון מראש : הקוד צריך למצוא אותו.

??? tip "רמז 1"
    תארו מצב בארבעה ביטים : באיזה צד האיכר, הזאב, העז והכרוב. אילו מצבים אסורים?

??? tip "רמז 2"
    מכל מצב בטוח יוצאות לכל היותר ארבע חציות : האיכר לבד, או עם אחד הפריטים שנמצא בצד
    שלו. מצאו את המסלול הקצר ביותר ממצב ההתחלה למצב הסיום.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        המצב הוא מסכה של ארבעה ביטים (0 קרוב, 1 רחוק). מצב בטוח הוא כזה שבו העז עם
        האיכר, או רחוקה גם מהזאב וגם מהכרוב. מריצים **BFS** מ-0000 ל-1111, מתקדמים רק
        למצבים בטוחים, ושומרים לכל מצב מאיפה הגיעו. כל הקשתות שוות, ולכן BFS מוצא את
        המסלול עם הכי מעט חציות.

    #### הרעיון { .sol-idea }

    **המצב.** ארבעה ביטים, ביט לכל אחד : האיכר, הזאב, העז והכרוב. ‏\( 0 \) הגדה הקרובה,
    ‏\( 1 \) הרחוקה. התחלה \( 0000 \), סיום \( 1111 \).

    **הבדיקה.** מישהו נאכל רק כשהאיכר לא שם : העז עם הזאב בלי האיכר, או העז עם הכרוב בלי
    האיכר. בשני המקרים העז בצד אחר מהאיכר. לכן המצב בטוח כש-\( g = f \) (העז עם
    האיכר), או כש-\( g \ne w \) וגם \( g \ne c \) (העז לבד בצד שלה). ששה מצבים נפסלים.

    **הקשתות.** האיכר תמיד חוצה (הביט שלו מתהפך), ואיתו לכל היותר פריט אחד מהצד שלו
    (גם הביט שלו מתהפך). מכל מצב לכל היותר ארבע קשתות. כל חצייה שווה לכל חצייה אחרת,
    ולכן BFS, ולא Dijkstra כמו בשאלה [0031](../junior/0031-bridge-and-torch.md).

    <!-- gen 4 -->

    <svg class="figure river-graph" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="גרף המצבים : שש עשרה חלוקות של האיכר ושלושת הפריטים בין הגדות, שש אסורות, ושני המסלולים הקצרים ביותר"><line class="box-path" x1="48" y1="80" x2="204" y2="170" stroke-width="3" /><line class="box-path" x1="126" y1="80" x2="282" y2="170" stroke-width="3" /><line class="box-path" x1="126" y1="80" x2="438" y2="170" stroke-width="3" /><line class="box-path" x1="204" y1="80" x2="204" y2="170" stroke-width="3" /><line class="box-path" x1="204" y1="80" x2="282" y2="170" stroke-width="3" /><line class="box-path" x1="204" y1="80" x2="516" y2="170" stroke-width="3" /><line class="box-path" x1="360" y1="80" x2="438" y2="170" stroke-width="3" /><line class="box-path" x1="360" y1="80" x2="516" y2="170" stroke-width="3" /><line class="box-path" x1="438" y1="80" x2="438" y2="170" stroke-width="3" /><line class="box-path" x1="438" y1="80" x2="594" y2="170" stroke-width="3" /><rect class="st-ok" x="16" y="40" width="64" height="40" rx="6"/><text class="st-text st-sm" x="48" y="56" text-anchor="middle">FWGC</text><text class="st-text st-sm" x="48" y="74" text-anchor="middle">–</text><rect class="st-bad" x="16" y="170" width="64" height="40" rx="6"/><text class="st-text st-sm" x="48" y="186" text-anchor="middle">WGC</text><text class="st-text st-sm" x="48" y="204" text-anchor="middle">F</text><line class="pg-strike" x1="22" y1="206" x2="74" y2="174"/><rect class="st-cell" x="94" y="40" width="64" height="40" rx="6"/><text class="st-text st-sm" x="126" y="56" text-anchor="middle">FGC</text><text class="st-text st-sm" x="126" y="74" text-anchor="middle">W</text><rect class="st-bad" x="94" y="170" width="64" height="40" rx="6"/><text class="st-text st-sm" x="126" y="186" text-anchor="middle">GC</text><text class="st-text st-sm" x="126" y="204" text-anchor="middle">FW</text><line class="pg-strike" x1="100" y1="206" x2="152" y2="174"/><rect class="st-cell" x="172" y="40" width="64" height="40" rx="6"/><text class="st-text st-sm" x="204" y="56" text-anchor="middle">FWC</text><text class="st-text st-sm" x="204" y="74" text-anchor="middle">G</text><rect class="st-cell" x="172" y="170" width="64" height="40" rx="6"/><text class="st-text st-sm" x="204" y="186" text-anchor="middle">WC</text><text class="st-text st-sm" x="204" y="204" text-anchor="middle">FG</text><rect class="st-bad" x="250" y="40" width="64" height="40" rx="6"/><text class="st-text st-sm" x="282" y="56" text-anchor="middle">FC</text><text class="st-text st-sm" x="282" y="74" text-anchor="middle">WG</text><line class="pg-strike" x1="256" y1="76" x2="308" y2="44"/><rect class="st-cell" x="250" y="170" width="64" height="40" rx="6"/><text class="st-text st-sm" x="282" y="186" text-anchor="middle">C</text><text class="st-text st-sm" x="282" y="204" text-anchor="middle">FWG</text><rect class="st-cell" x="328" y="40" width="64" height="40" rx="6"/><text class="st-text st-sm" x="360" y="56" text-anchor="middle">FWG</text><text class="st-text st-sm" x="360" y="74" text-anchor="middle">C</text><rect class="st-bad" x="328" y="170" width="64" height="40" rx="6"/><text class="st-text st-sm" x="360" y="186" text-anchor="middle">WG</text><text class="st-text st-sm" x="360" y="204" text-anchor="middle">FC</text><line class="pg-strike" x1="334" y1="206" x2="386" y2="174"/><rect class="st-cell" x="406" y="40" width="64" height="40" rx="6"/><text class="st-text st-sm" x="438" y="56" text-anchor="middle">FG</text><text class="st-text st-sm" x="438" y="74" text-anchor="middle">WC</text><rect class="st-cell" x="406" y="170" width="64" height="40" rx="6"/><text class="st-text st-sm" x="438" y="186" text-anchor="middle">G</text><text class="st-text st-sm" x="438" y="204" text-anchor="middle">FWC</text><rect class="st-bad" x="484" y="40" width="64" height="40" rx="6"/><text class="st-text st-sm" x="516" y="56" text-anchor="middle">FW</text><text class="st-text st-sm" x="516" y="74" text-anchor="middle">GC</text><line class="pg-strike" x1="490" y1="76" x2="542" y2="44"/><rect class="st-cell" x="484" y="170" width="64" height="40" rx="6"/><text class="st-text st-sm" x="516" y="186" text-anchor="middle">W</text><text class="st-text st-sm" x="516" y="204" text-anchor="middle">FGC</text><rect class="st-bad" x="562" y="40" width="64" height="40" rx="6"/><text class="st-text st-sm" x="594" y="56" text-anchor="middle">F</text><text class="st-text st-sm" x="594" y="74" text-anchor="middle">WGC</text><line class="pg-strike" x1="568" y1="76" x2="620" y2="44"/><rect class="st-ok" x="562" y="170" width="64" height="40" rx="6"/><text class="st-text st-sm" x="594" y="186" text-anchor="middle">–</text><text class="st-text st-sm" x="594" y="204" text-anchor="middle">FWGC</text><text class="legend" x="8" y="16">farmer near: near bank / far bank</text><text class="legend" x="8" y="240">farmer far</text></svg>

    <!-- /gen -->

    <!-- gen 5 -->

    <span class="viz-legend"><span><i class="st-ok"></i>ההתחלה והסיום</span><span><i class="st-cell"></i>מצב בטוח</span><span><i class="st-bad"></i>מצב אסור : מישהו נאכל</span><span><i class="box-path"></i>שני המסלולים הקצרים ביותר</span><span><i class="ink"></i>חצייה בטוחה אחרת</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **תור והורים :** מכניסים את 0000 לתור, ורושמים שאין לו הורה.
    2. **הוצאה :** מוציאים מצב. אם הוא 1111, סיימנו.
    3. **הרחבה :** לכל אחת מארבע החציות האפשריות מחשבים את המצב החדש. אם הוא בטוח ועוד
       לא נראה, רושמים את ההורה ומה האיכר לקח, ומכניסים לתור.
    4. **שחזור :** מ-1111 הולכים אחורה לפי ההורים, אוספים מה נלקח בכל חצייה, והופכים.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="river_plan" linenums="1" hl_lines="6 7 28 29 30 31 32"
        localparam int FARMER = 1, WOLF = 2, GOAT = 4, CABBAGE = 8;   // the bit of each one
        localparam int EVERYONE = FARMER | WOLF | GOAT | CABBAGE;

        // Nobody is eaten: the goat is with the farmer, or away from both the wolf and the cabbage.
        function automatic bit river_safe(int state);
          bit f = (state & FARMER) != 0, w = (state & WOLF) != 0, g = (state & GOAT) != 0, c = (state & CABBAGE) != 0;
          return (g == f) || (g != w && g != c);
        endfunction

        // The crossings from everyone near to everyone far, e.g. "G> -< W> G< C> -< G>"
        // (the letter of what the farmer takes, or - for alone; > forward, < back). Returns their number.
        function automatic int river_plan(output string plan);
          int queue[$];
          int prev[16], took[16];                  // the parent state and what was carried
          bit seen[16];
          int s, nxt, item, n = 0;
          int cargo[4] = '{0, WOLF, GOAT, CABBAGE};
          string letter[4] = '{"-", "W", "G", "C"};

          foreach (seen[i]) seen[i] = 0;
          seen[0] = 1; prev[0] = -1;
          queue.push_back(0);
          while (queue.size() > 0) begin
            s = queue.pop_front();
            if (s == EVERYONE) break;
            for (int k = 0; k < 4; k++) begin
              item = cargo[k];
              if (item != 0 && ((s & item) != 0) != ((s & FARMER) != 0)) continue;   // (1)!
              nxt = s ^ FARMER ^ item;                                                // (2)!
              if (!river_safe(nxt) || seen[nxt]) continue;
              seen[nxt] = 1; prev[nxt] = s; took[nxt] = k;
              queue.push_back(nxt);
            end
          end

          plan = "";
          for (s = EVERYONE; prev[s] >= 0; s = prev[s]) begin                         // (3)!
            plan = {letter[took[s]], (s & FARMER) ? ">" : "<", (plan == "") ? "" : " ", plan};
            n++;
          end
          return n;
        endfunction
        ```

        1. פריט שנמצא בצד השני מהאיכר לא יכול לעלות לסירה.
        2. החצייה הופכת את הביט של האיכר ואת הביט של מה שהוא לוקח (0 כשהוא לבד).
        3. השחזור : מהסיום אחורה, כל פעם מוסיפים את החצייה **לפני** מה שכבר נאסף.

    === "Python"
        ```python title="river_plan" linenums="1" hl_lines="9 10 11 23 24 25 26"
        from collections import deque

        FARMER, WOLF, GOAT, CABBAGE = 1, 2, 4, 8          # the bit of each one in the state
        EVERYONE = FARMER | WOLF | GOAT | CABBAGE
        CARGO = {None: 0, "wolf": WOLF, "goat": GOAT, "cabbage": CABBAGE}


        def river_safe(state):
            """Nobody is eaten: the goat is with the farmer, or away from both the wolf and the cabbage."""
            f, w, g, c = (bool(state & b) for b in (FARMER, WOLF, GOAT, CABBAGE))
            return g == f or (g != w and g != c)


        def river_plan():
            """What the farmer takes on each crossing (None = alone), from everyone near to everyone far."""
            parent = {0: None}
            queue = deque([0])
            while queue:
                s = queue.popleft()
                if s == EVERYONE:
                    break
                for item, bit in CARGO.items():
                    if bit and bool(s & bit) != bool(s & FARMER):
                        continue                              # that item is on the other bank (1)
                    nxt = s ^ FARMER ^ bit                    # (2)!
                    if river_safe(nxt) and nxt not in parent:
                        parent[nxt] = (s, item)
                        queue.append(nxt)
            plan, s = [], EVERYONE
            while parent[s] is not None:                      # (3)!
                s, item = parent[s]
                plan.append(item)
            return plan[::-1]
        ```

        1. פריט שנמצא בצד השני מהאיכר לא יכול לעלות לסירה.
        2. החצייה הופכת את הביט של האיכר ואת הביט של מה שהוא לוקח (0 כשהוא לבד).
        3. השחזור : מהסיום אחורה לפי ההורים, ואז הופכים.

    #### למה זה נכון { .sol-proof }

    **הגרף מכיל כל תוכנית.** כל חצייה חוקית היא קשת בין שני מצבים, והתוכנית היא מסלול
    מ-0000 ל-1111 שעובר רק במצבים בטוחים. BFS מבקר במצבים לפי מרחק עולה מההתחלה, ולכן
    המצב 1111 מתגלה דרך מסלול באורך מינימלי. עם 16 מצבים אפשר גם לבדוק ביד : הטבלה
    מראה את עשרת המצבים הבטוחים, והגרף למעלה את כל הקשתות ביניהם. שני המסלולים
    באורך שבע הם תמונת ראי זה של זה (הזאב והכרוב מתחלפים), כי הבדיקה סימטרית בהם.

    <!-- gen 6 -->

    | הגדה הקרובה | הגדה הרחוקה | בטוח? | למה |
    |---|---|:-:|---|
    | ‏FWGC | ‏– | כן | העז עם האיכר |
    | ‏WGC | ‏F | לא | הזאב אוכל את העז |
    | ‏FGC | ‏W | כן | העז עם האיכר |
    | ‏GC | ‏FW | לא | העז אוכלת את הכרוב |
    | ‏FWC | ‏G | כן | העז לבד, הזאב והכרוב עם האיכר |
    | ‏WC | ‏FG | כן | העז עם האיכר |
    | ‏FC | ‏WG | לא | הזאב אוכל את העז |
    | ‏C | ‏FWG | כן | העז עם האיכר |
    | ‏FWG | ‏C | כן | העז עם האיכר |
    | ‏WG | ‏FC | לא | הזאב אוכל את העז |
    | ‏FG | ‏WC | כן | העז עם האיכר |
    | ‏G | ‏FWC | כן | העז לבד, הזאב והכרוב עם האיכר |
    | ‏FW | ‏GC | לא | העז אוכלת את הכרוב |
    | ‏W | ‏FGC | כן | העז עם האיכר |
    | ‏F | ‏WGC | לא | הזאב אוכל את העז |
    | ‏– | ‏FWGC | כן | העז עם האיכר |

    <!-- /gen -->

    **נסו בעצמכם.** נסו לעבור בעצמכם : בוחרים מי עולה לסירה, והדף אומר אם מישהו נאכל.
    הכפתור "פתרון" מריץ את ה-BFS ומראה את התוכנית חצייה אחרי חצייה, והגרף מסמן איפה
    אתם. בשלב ההוכחה, בתחתית התיבה, "השכבה הבאה" ממלא את הגרף כמו החיפוש עצמו : כל
    שכבה עם המרחק שלה והחץ מהמצב שממנו הגענו, עד ש-FWGC נכנס בשכבה 7 בשני מסלולים :

    <div class="explorer" data-kind="river"></div>

    #### סיבוכיות { .sol-cost }

    ‏\( 16 \) מצבים, לכל היותר \( 4 \) קשתות מכל אחד : BFS ב-\( O(1) \) בפועל. הזיכרון הוא
    ארבעה מערכים של 16.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לא להחזיר את העז"
    אחרי שהעז בצד הרחוק והאיכר מביא את הזאב, הרבה מועמדים נתקעים, כי כל חצייה חזרה
    "לבד" משאירה את הזאב עם העז. הפתרון דורש להחזיר פריט לצד הקרוב, וזה מרגיש כמו
    צעד אחורה.

??? trap "מלכודת : לבדוק רק את הצד שעוזבים"
    החצייה משנה את שני הצדדים : גם הצד שאליו מגיעים צריך להיות בטוח **אחרי שהאיכר יעזוב
    אותו** בחצייה הבאה. בקוד זה פשוט : בודקים את המצב החדש כולו.

??? trap "מלכודת : מצב בלי האיכר"
    מי שמתאר את המצב רק לפי שלושת הפריטים מקבל שמונה מצבים, אבל לא יודע מאיזה צד
    האיכר יכול לקחת. הביט של האיכר הוא חלק מהמצב.

??? followup "שאלות המשך"
    - **סירה לשניים :** אם הסירה מכילה את האיכר ועוד שניים, כמה חציות צריך? ‏(שלוש : הזאב
      והכרוב קדימה, חזרה לבד, העז קדימה; או העז ועוד אחד, חזרה, האחרון.)
    - **ארבעה פריטים :** זאב, עז, כרוב ועוד עז. האם יש פתרון עם סירה לאחד? ‏(לא : כשהאיכר
      עוזב צד עם שתי עזים, אחת מהן נשארת עם הזאב או עם הכרוב, ואם שתיהן עם הזאב בלבד,
      הזאב אוכל. ‏BFS על \( 2^5 \) מצבים מאשר שאין מסלול.)
    - **הכללה :** פריטים שמסוכנים זה לזה לפי גרף נתון, סירה בקיבולת \( k \). איך משנים את
      בדיקת הבטיחות ואת מספר המצבים? ‏(בדיקה לפי כל זוג מסוכן באותו צד בלי האיכר;
      ‏\( 2^{n+1} \) מצבים ו-\( \binom{n}{\le k} \) קשתות מכל אחד.)
