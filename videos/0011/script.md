# 0011 — a random final tic-tac-toe board: the video script

The storyboard of the video, beat by beat: the picture (English notes) and the caption
(Hebrew, a `> ` line per caption line, a blank line between captions). The captions are
exactly what the video shows; `videos/render.py` fails when scene.py's captions differ.

The answer is the page's SystemVerilog class `ttt_end` (a DV question whose answer is SV
constraints types the SV class; the owner, 2026-10-31). The page's boxes are captured from
the built site (`BOXES` in scene.py, `lib/box_shots.py`): the ttt box (the conditions, then
each constraint above it) and, in part ב, the tttfive box.

## Opening

- The DV mark, the id, the title and level; the part chips; then the page's board XXXOXOOOX beside the three results.

> שאלה 0011 : לוח סיום אקראי של איקס-עיגול,
> שאלה ברמת סניור.

> שני סעיפים : הלוח הרגיל,
> ואלכסונים שממשיכים מהצד השני.

> צריך לייצר לוח שבו נגמר משחק,
> ויחד איתו את התוצאה : X, O או תיקו.

## Chapter א – the regular board

Chapter card: "סעיף א", "הלוח הרגיל".

> סעיף א : מהם כל התנאים של לוח סיום,
> ואיך כותבים אותם כ-constraints?

The empty board with its cell numbers.

> המשבצות ממוספרות מ-0 עד 8, שורה אחרי שורה.
> ‏X תמיד מתחיל, והשחקנים משחקים לסירוגין.

**The conditions, on the page's box** (BOXES "rules": the ttt box, its controls and board). Each step clicks cells; an amber ring marks each clicked cell.

> זו התיבה מהעמוד, עם הלוח של השאלה :
> ל-X שתי שלישיות, והוא ניצח.

> תנאי 1, הספירה : X מתחיל ומשחקים לסירוגין.
> שלושה X בלי אף O לא קורה במשחק.

> תנאי 2 : אין שני מנצחים.
> המשחק נעצר ברגע שמישהו השלים שלישייה.

> והתנאי שרוב המועמדים שוכחים : ל-X שלישייה,
> אבל n_X = n_O. כלומר O שיחק אחרי הניצחון.

> בלי ה-O האחרון יש n_X = n_O + 1.
> מי שניצח הוא זה ששיחק אחרון.

> ובאותו אופן ל-O : שלישייה של O,
> אין שלישייה של X, ו-n_X = n_O.

> ותיקו : לוח מלא, חמישה X וארבעה O,
> בלי אף שלישייה.

The four conditions as Latin lines (the count, X_WINS, O_WINS, DRAW).

> ארבעה תנאים : הספירה, ותנאי לכל תוצאה.
> כל אחד מהם יהפוך ל-constraint.

**The code.** The SV class `ttt_end` typed into a 14-line scrolling window (comment and blank lines out of the picture, show() left out), a caption after each group.

> עכשיו נכתוב את המחלקה ב-SystemVerilog,
> חלק אחרי חלק.

> שלושה טיפוסים : משבצת היא EMPTY, X או O,
> והתוצאה היא אחת משלוש.

> הלוח הוא מערך של 9 משבצות,
> ממוספרות מ-0 עד 8.

> המחלקה ttt_end. כל קריאה ל-randomize()
> תיתן לוח סיום ותוצאה שמתאימה לו.

> טבלת הקווים : שורות, טורים ושני אלכסונים.
> ארבעת האחרונים שמורים לסעיף ב.

> ‏n_lines = 8 בלוח הרגיל. הוא לא rand,
> ולכן בעיני ה-solver הוא קבוע.

> הלוח והתוצאה הם rand :
> ה-solver בוחר את שניהם יחד.

> ועוד משתני עזר, גם הם rand :
> כמה X וכמה O, ואילו קווים שלמים.

> ‏c_count : משתני העזר שווים לספירה על הלוח,
> ו-n_x הוא n_o או n_o + 1.

> ‏c_lines : x_line[l] הוא 1 בדיוק כשהקו פעיל
> וכל שלוש המשבצות שלו X.

> ‏x_lines ו-o_lines סופרים את הקווים השלמים.
> ה-int' מרחיב את הסכום מעבר לביט אחד.

> ‏c_result : כל תוצאה גוררת את התנאים שלה,
> בדיוק התנאים מהתיבה.

> חץ ולא שוויון : התנאים זרים זה לזה,
> ולכן כל לוח קובע תוצאה אחת.

> ‏solve result before board : קודם תוצאה
> בהסתברות שווה, ורק אחר כך לוח.

> והמחלקה נסגרת. בעמוד יש גם show(),
> שרק מדפיסה את הלוח, ולכן היא לא כאן.

**Each constraint above the box** (BOXES "walk": the board only). The SV lines of one group at the top, full width; the box under them steps to a board that the constraint keeps or rejects. Seeds 7, 1 and 2 draw X, O and a draw.

> ב-c_count : שלושה X ואפס O.
> אין n_o שמקיים את זה, והלוח נפסל.

> ב-c_lines : בלוח של השאלה שני קווים של X שלמים,
> ולכן x_lines = 2.

> ‏X_WINS דורש n_x == n_o + 1.
> כאן n_x == n_o : O שיחק אחרי הניצחון.

> ‏O_WINS : שלישייה של O, אין של X,
> ו-n_x == n_o, כי O שיחק אחרון.

> ‏DRAW : לוח מלא בלי שלישיות. בלי n_x + n_o == 9
> גם לוח באמצע משחק היה תיקו.

> עם solve before, ה-solver בוחר קודם תוצאה.
> בהגרלה הזו יצא X_WINS.

> בהגרלה הבאה יצא O_WINS.

> ובשלישית תיקו, שיוצא בשליש מההגרלות.

**The distribution.** Two sets of bars: plain randomize() (65.3 / 33.0 / 1.7 %) and solve result before board (a third each).

> יש 958 לוחות סיום : 626 של X, 316 של O, ו-16 תיקו.
> בלי solve before, כל לוח מוגרל באותה הסתברות.

> אז X מנצח ב-65% מההגרלות, ותיקו רק ב-1.7%.
> עם solve before, כל תוצאה מקבלת שליש.

> אותם 958 לוחות, בהתפלגות אחרת :
> המקרה הנדיר, התיקו, נבדק הרבה יותר.

**The cost.** Two chips: 3⁹ fillings, 958 final boards.

> מרחב הפתרונות קטן : 3 בחזקת 9 מילויים,
> ומהם רק 958 הם לוחות סיום.

**The trap.** The page's board with its two X lines through cell 0.

> מלכודת : לדרוש שלמנצח שלישייה אחת בלבד.
> כאן X סגר שתיים במהלך אחד, במשבצת 0.

> ‏constraint חזק מדי מסתיר לוחות חוקיים,
> ואף בדיקה לא תתריע עליו.

## Chapter ב – wrap-around diagonals

Chapter card: "סעיף ב", "אלכסונים מסביב".

> סעיף ב : אלכסון ממשיך מהצד השני של הלוח,
> כאילו הלוח מודבק לעצמו.

The board with cells 0, 5, 7 lit.

> למשל המשבצות 0, 5 ו-7 :
> יורדים שמאלה, יוצאים מהלוח וחוזרים מימין.

Four small boards: the four directions, three parallel lines each in three colours.

> ארבעה קווים חדשים, ובסך הכול 12 קווים :
> ארבעה כיוונים, בכל אחד שלושה קווים מקבילים.

> התנאים לא משתנים, רק קבוצת הקווים.
> במחלקה זה משתנה אחד : n_lines.

**The code.** The page's SV usage snippet for part b, typed.

> כך משתמשים במחלקה עם 12 הקווים.

> יוצרים אובייקט של המחלקה מסעיף א.

> ‏n_lines = 12 מדליק את ארבעת הקווים החדשים.
> אף שורה ב-constraints לא משתנה.

> הגרלה רגילה : X או O,
> כל אחד בחצי מההגרלות.

> ‏randomize() with מוסיף constraint זמני.
> כאן הוא תמיד נכשל, כי אין תיקו.

**The box** (BOXES "wrap"): the full draw board, then the wrap toggle.

> בתיבה : לוח מלא בלי שלישייה,
> תיקו עם 8 הקווים.

> מדליקים את האלכסונים מסביב :
> עכשיו גם ל-X וגם ל-O יש שלישייה.

**The proof** as Latin lines: 2 + 2 + 1, 4 × 2 = 8, C(5, 2) = 10, 8 ≠ 10.

> תיקו דורש לוח מלא : חמישה X בלי שלישייה.
> נראה שכל 5 משבצות מכילות קו.

> נניח שאין קו. בכל כיוון המשבצות מתחלקות 2, 2, 1,
> ולכן יש בו 2 זוגות על קו.

> בארבעת הכיוונים : 8 זוגות.
> אבל ל-5 משבצות יש 10 זוגות.

> וכל זוג משבצות נמצא על קו אחד בדיוק.
> סתירה : אין 5 משבצות בלי קו.

**The tttfive box** (BOXES "five"): the page's square 0 1 3 4, then a fifth cell.

> בתיבה : ריבוע של 4 משבצות בלי קו.
> הכוכבים : כל משבצת ריקה משלימה קו.

> משבצת 8 משלימה שני קווים : האלכסון 0, 4, 8,
> וגם 1, 3, 8, שממשיך מהצד השני.

> ומשבצת 2 משלימה את השורה העליונה.

Bars: 882 X, 432 O, 0 draw.

> עם 12 הקווים יש 1,314 לוחות סיום :
> ‏882 של X, 432 של O, ואף תיקו.

> ה-solver לא מוצא אף פתרון עם DRAW :
> הוא מוכיח את המשפט בשבילנו.

## Closing

- One line per part, then the site's address and the id.

> לסיכום : ארבעה תנאים, וכל תנאי הופך ל-constraint.
> מי שניצח הוא זה ששיחק אחרון.

> ועם האלכסונים מסביב אין תיקו.
> נסו בתיבה שבעמוד של שאלה 0011.
