# 0011 — a random final tic-tac-toe board: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:). VIDEOS.md.

he: שאלה 0011 : לוח סיום אקראי של איקס-עיגול,
he: שאלה ברמת סניור.
en: Question 0011: a random final tic-tac-toe board,
en: a senior-level question.

he: שני סעיפים : הלוח הרגיל,
he: ואלכסונים שממשיכים מהצד השני.
en: Two parts: the regular board,
en: and diagonals that wrap around to the other side.

he: צריך לייצר לוח שבו נגמר משחק,
he: ויחד איתו את התוצאה : X, O או תיקו.
en: Generate a board where a game has ended,
en: together with its result: X, O or a draw.

he: סעיף א : מהם כל התנאים של לוח סיום,
he: ואיך כותבים אותם כ-constraints?
en: Part A: what are all the conditions of a final board,
en: and how do we write them as constraints?

he: המשבצות ממוספרות מ-0 עד 8, שורה אחרי שורה.
he: ‏X תמיד מתחיל, והשחקנים משחקים לסירוגין.
en: The cells are numbered 0 to 8, row by row.
en: X always starts, and the players alternate.

he: זו התיבה מהעמוד, עם הלוח של השאלה :
he: ל-X שתי שלישיות, והוא ניצח.
en: This is the box from the page, with the question's board:
en: X has two lines, and X won.

he: תנאי 1, הספירה : X מתחיל ומשחקים לסירוגין.
he: שלושה X בלי אף O לא קורה במשחק.
en: Condition 1, the count: X starts and the players alternate.
en: Three X and no O never happens in a game.

he: תנאי 2 : אין שני מנצחים.
he: המשחק נעצר ברגע שמישהו השלים שלישייה.
en: Condition 2: there are no two winners.
en: The game stops the moment someone completes a line.

he: והתנאי שרוב המועמדים שוכחים : ל-X שלישייה,
he: אבל n_X = n_O. כלומר O שיחק אחרי הניצחון.
en: The condition most candidates forget: X has a line,
en: but n_X = n_O. So O moved after the win.

he: בלי ה-O האחרון יש n_X = n_O + 1.
he: מי שניצח הוא זה ששיחק אחרון.
en: Without the last O, n_X = n_O + 1.
en: The winner is the one who moved last.

he: ובאותו אופן ל-O : שלישייה של O,
he: אין שלישייה של X, ו-n_X = n_O.
en: The same for O: a line of O,
en: no line of X, and n_X = n_O.

he: ותיקו : לוח מלא, חמישה X וארבעה O,
he: בלי אף שלישייה.
en: And a draw: a full board, five X and four O,
en: with no line at all.

he: ארבעה תנאים : הספירה, ותנאי לכל תוצאה.
he: כל אחד מהם יהפוך ל-constraint.
en: Four conditions: the count, and one per result.
en: Each one will become a constraint.

he: עכשיו נכתוב את המחלקה ב-SystemVerilog,
he: חלק אחרי חלק.
en: Now let's write the class in SystemVerilog,
en: piece by piece.

he: שלושה טיפוסים : משבצת היא EMPTY, X או O,
he: והתוצאה היא אחת משלוש.
en: Three types: a cell is EMPTY, X or O,
en: and the result is one of three.

he: הלוח הוא מערך של 9 משבצות,
he: ממוספרות מ-0 עד 8.
en: The board is an array of 9 cells,
en: numbered 0 to 8.

he: המחלקה ttt_end. כל קריאה ל-randomize()
he: תיתן לוח סיום ותוצאה שמתאימה לו.
en: The class ttt_end. Every call to randomize()
en: gives a final board and a matching result.

he: טבלת הקווים : שורות, טורים ושני אלכסונים.
he: ארבעת האחרונים שמורים לסעיף ב.
en: The table of lines: rows, columns and two diagonals.
en: The last four are kept for part B.

he: ‏n_lines = 8 בלוח הרגיל. הוא לא rand,
he: ולכן בעיני ה-solver הוא קבוע.
en: n_lines = 8 on the regular board. It is not rand,
en: so the solver treats it as a constant.

he: הלוח והתוצאה הם rand :
he: ה-solver בוחר את שניהם יחד.
en: The board and the result are rand:
en: the solver picks both together.

he: ועוד משתני עזר, גם הם rand :
he: כמה X וכמה O, ואילו קווים שלמים.
en: And helper variables, rand as well:
en: how many X and O, and which lines are complete.

he: ‏c_count : משתני העזר שווים לספירה על הלוח,
he: ו-n_x הוא n_o או n_o + 1.
en: c_count: the helpers equal the count on the board,
en: and n_x is n_o or n_o + 1.

he: ‏c_lines : x_line[l] הוא 1 בדיוק כשהקו פעיל
he: וכל שלוש המשבצות שלו X.
en: c_lines: x_line[l] is 1 exactly when the line is active
en: and all three of its cells are X.

he: ‏x_lines ו-o_lines סופרים את הקווים השלמים.
he: ה-int' מרחיב את הסכום מעבר לביט אחד.
en: x_lines and o_lines count the complete lines.
en: The int' cast widens the sum beyond one bit.

he: ‏c_result : כל תוצאה גוררת את התנאים שלה,
he: בדיוק התנאים מהתיבה.
en: c_result: each result implies its own conditions,
en: exactly the conditions from the box.

he: חץ ולא שוויון : התנאים זרים זה לזה,
he: ולכן כל לוח קובע תוצאה אחת.
en: An implication, not an equality: the cases are disjoint,
en: so every board determines one result.

he: ‏solve result before board : קודם תוצאה
he: בהסתברות שווה, ורק אחר כך לוח.
en: solve result before board: first a result,
en: with equal probability, and only then a board.

he: והמחלקה נסגרת. בעמוד יש גם show(),
he: שרק מדפיסה את הלוח, ולכן היא לא כאן.
en: And the class closes. The page also has show(),
en: which only prints the board, so it is left out.

he: ב-c_count : שלושה X ואפס O.
he: אין n_o שמקיים את זה, והלוח נפסל.
en: In c_count: three X and zero O.
en: No n_o satisfies that, so the board is rejected.

he: ב-c_lines : בלוח של השאלה שני קווים של X שלמים,
he: ולכן x_lines = 2.
en: In c_lines: the question's board has two complete X lines,
en: so x_lines = 2.

he: ‏X_WINS דורש n_x == n_o + 1.
he: כאן n_x == n_o : O שיחק אחרי הניצחון.
en: X_WINS requires n_x == n_o + 1.
en: Here n_x == n_o: O moved after the win.

he: ‏O_WINS : שלישייה של O, אין של X,
he: ו-n_x == n_o, כי O שיחק אחרון.
en: O_WINS: a line of O, none of X,
en: and n_x == n_o, because O moved last.

he: ‏DRAW : לוח מלא בלי שלישיות. בלי n_x + n_o == 9
he: גם לוח באמצע משחק היה תיקו.
en: DRAW: a full board with no lines. Without n_x + n_o == 9
en: a board in mid-game would also be a draw.

he: עם solve before, ה-solver בוחר קודם תוצאה.
he: בהגרלה הזו יצא X_WINS.
en: With solve before, the solver picks the result first.
en: This draw came out X_WINS.

he: בהגרלה הבאה יצא O_WINS.
en: The next draw came out O_WINS.

he: ובשלישית תיקו, שיוצא בשליש מההגרלות.
en: And the third: a draw,
en: which now comes out a third of the time.

he: יש 958 לוחות סיום : 626 של X, 316 של O, ו-16 תיקו.
he: בלי solve before, כל לוח מוגרל באותה הסתברות.
en: 958 final boards: 626 for X, 316 for O, 16 draws.
en: Without solve before, every board is equally likely.

he: אז X מנצח ב-65% מההגרלות, ותיקו רק ב-1.7%.
he: עם solve before, כל תוצאה מקבלת שליש.
en: Then X wins 65% of the draws, and a draw only 1.7%.
en: With solve before, each result gets a third.

he: אותם 958 לוחות, בהתפלגות אחרת :
he: המקרה הנדיר, התיקו, נבדק הרבה יותר.
en: The same 958 boards, with a different distribution:
en: the rare case, the draw, gets tested far more.

he: מרחב הפתרונות קטן : 3 בחזקת 9 מילויים,
he: ומהם רק 958 הם לוחות סיום.
en: The solution space is small: 3 to the power of 9 fillings,
en: and only 958 of them are final boards.

he: מלכודת : לדרוש שלמנצח שלישייה אחת בלבד.
he: כאן X סגר שתיים במהלך אחד, במשבצת 0.
en: A trap: requiring exactly one line for the winner.
en: Here X closed two lines in one move, at cell 0.

he: ‏constraint חזק מדי מסתיר לוחות חוקיים,
he: ואף בדיקה לא תתריע עליו.
en: A constraint that is too strong hides legal boards,
en: and no test will complain about it.

he: סעיף ב : אלכסון ממשיך מהצד השני של הלוח,
he: כאילו הלוח מודבק לעצמו.
en: Part B: a diagonal continues on the other side of the board,
en: as if the board were glued to itself.

he: למשל המשבצות 0, 5 ו-7 :
he: יורדים שמאלה, יוצאים מהלוח וחוזרים מימין.
en: For example cells 0, 5 and 7:
en: go down-left, leave the board and come back on the right.

he: ארבעה קווים חדשים, ובסך הכול 12 קווים :
he: ארבעה כיוונים, בכל אחד שלושה קווים מקבילים.
en: Four new lines, 12 lines in all:
en: four directions, each with three parallel lines.

he: התנאים לא משתנים, רק קבוצת הקווים.
he: במחלקה זה משתנה אחד : n_lines.
en: The conditions do not change, only the set of lines.
en: In the class it is one variable: n_lines.

he: כך משתמשים במחלקה עם 12 הקווים.
en: This is how the class is used with the 12 lines.

he: יוצרים אובייקט של המחלקה מסעיף א.
en: Create an object of the class from part A.

he: ‏n_lines = 12 מדליק את ארבעת הקווים החדשים.
he: אף שורה ב-constraints לא משתנה.
en: n_lines = 12 turns on the four new lines.
en: Not one line of the constraints changes.

he: הגרלה רגילה : X או O,
he: כל אחד בחצי מההגרלות.
en: A regular draw: X or O,
en: each in half of the draws.

he: ‏randomize() with מוסיף constraint זמני.
he: כאן הוא תמיד נכשל, כי אין תיקו.
en: randomize() with adds a temporary constraint.
en: Here it always fails, because there is no draw.

he: בתיבה : לוח מלא בלי שלישייה,
he: תיקו עם 8 הקווים.
en: In the box: a full board with no line,
en: a draw with the 8 lines.

he: מדליקים את האלכסונים מסביב :
he: עכשיו גם ל-X וגם ל-O יש שלישייה.
en: Turn on the wrap-around diagonals:
en: now both X and O have a line.

he: תיקו דורש לוח מלא : חמישה X בלי שלישייה.
he: נראה שכל 5 משבצות מכילות קו.
en: A draw needs a full board: five X with no line.
en: Let's show that every 5 cells contain a line.

he: נניח שאין קו. בכל כיוון המשבצות מתחלקות 2, 2, 1,
he: ולכן יש בו 2 זוגות על קו.
en: Assume no line. Each direction splits the cells 2, 2, 1,
en: so it has 2 pairs on a line.

he: בארבעת הכיוונים : 8 זוגות.
he: אבל ל-5 משבצות יש 10 זוגות.
en: Over the four directions: 8 pairs.
en: But 5 cells have 10 pairs.

he: וכל זוג משבצות נמצא על קו אחד בדיוק.
he: סתירה : אין 5 משבצות בלי קו.
en: And every pair of cells lies on exactly one line.
en: A contradiction: no 5 cells without a line.

he: בתיבה : ריבוע של 4 משבצות בלי קו.
he: הכוכבים : כל משבצת ריקה משלימה קו.
en: In the box: a square of 4 cells with no line.
en: The stars: every empty cell completes a line.

he: משבצת 8 משלימה שני קווים : האלכסון 0, 4, 8,
he: וגם 1, 3, 8, שממשיך מהצד השני.
en: Cell 8 completes two lines: the diagonal 0, 4, 8,
en: and 1, 3, 8, which wraps around.

he: ומשבצת 2 משלימה את השורה העליונה.
en: And cell 2 completes the top row.

he: עם 12 הקווים יש 1,314 לוחות סיום :
he: ‏882 של X, 432 של O, ואף תיקו.
en: With the 12 lines there are 1,314 final boards:
en: 882 for X, 432 for O, and no draw.

he: ה-solver לא מוצא אף פתרון עם DRAW :
he: הוא מוכיח את המשפט בשבילנו.
en: The solver finds no solution with DRAW:
en: it proves the theorem for us.

he: לסיכום : ארבעה תנאים, וכל תנאי הופך ל-constraint.
he: מי שניצח הוא זה ששיחק אחרון.
en: To sum up: four conditions, each one a constraint.
en: The winner is the one who moved last.

he: ועם האלכסונים מסביב אין תיקו.
he: נסו בתיבה שבעמוד של שאלה 0011.
en: And with the wrap-around diagonals there is no draw.
en: Try it in the box on the page of question 0011.
