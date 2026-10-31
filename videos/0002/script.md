# 0002 — swap two variables: the video script

The storyboard of the video, beat by beat: the picture (English notes) and the caption
(Hebrew, a `> ` line per caption line, a blank line between captions). The captions are
exactly what the video shows; `videos/render.py` fails when scene.py's captions differ.

The example is the page's: `a = 5`, `b = 3` (`0101` and `0011` in part ג), and the
overflow example of part ב, `a = 2³¹ − 1`, `b = 1`. The code beats load the Python tab of
the page (`swap_temp`, `swap_arith`, `swap_xor`). Each one is first typed into its panel
character by character (`DVQScene.type_code`), a caption after every line, then run on
`v = [5, 3]`, `i = 0`, `j = 1` beside the page's box (split screen); the lines are lit in
the order the tracer saw them run. Each part also plays its box alone after the steps.

## Opening

- The DV mark is drawn stroke by stroke, the id `0002` beside it, the title and the level
  chip below (Hebrew labels).

> שאלה 0002 : החלפת ערכים בין שני משתנים,
> שאלה ברמת סטודנט.

- The three part chips appear, right to left.

> שלושה סעיפים, וכל סעיף מוסיף אילוץ :
> עם משתנה עזר, בלי משתנה עזר, ורק ביטים.

- The header moves away. Two cells, `a = 5` and `b = 3`.

> הפונקציה swap מקבלת שני משתנים, a ו-b,
> ומחליפה ביניהם במקום.

- Ghost values under the cells: `3` under `a`, `5` under `b`, with arrows crossing.

> בסוף a מחזיק את הערך המקורי של b,
> ו-b את הערך המקורי של a.

## Chapter א – with a temp variable

- Chapter card: "סעיף א", "עם משתנה עזר".

> סעיף א : הדרך הפשוטה ביותר, עם משתנה עזר.

**The problem.** The cells `a = 5`, `b = 3`.

> יש לנו שני משתנים : a שווה 5, ו-b שווה 3.

- Ghost targets below the cells.

> המטרה : ש-a יחזיק 3, ו-b יחזיק 5.

**The idea.** A third cell `temp` appears to the right, empty.

> הרעיון : משתנה עזר, temp,
> ששומר את הערך של a לפני שדורסים אותו.

**The steps.** The statement of each step is written above the cells; the value travels
as a card from its source cell to its target.

> שלב 1 : temp = a. הערך 5 נשמר ב-temp.

> שלב 2 : a = b. עכשיו a מחזיק 3,
> וה-5 המקורי עדיין שמור ב-temp.

> שלב 3 : b = temp, ו-b מקבל 5.
> ההחלפה הושלמה.

**The page's box.** The box of the part, captured from the site, large; each step a
click on "next" (an amber ring) and the box's next line.

> אותה דוגמה בתיבה שבעמוד :
> הקוד, ומתחתיו הערך של כל משתנה.

> ‏temp שומר את a0, הערך 5,
> לפני שדורסים את v[i].

> ‏v[i] מקבל את b0, והעמודה הסימבולית
> מראה ש-a0 שמור רק ב-temp.

> ‏v[j] מקבל את a0 מ-temp.
> בסוף a = b0 ו-b = a0.

**The code, typed.** The empty panel of `swap_temp` appears, the amber caret at its first
line, centred.

> עכשיו נכתוב את זה ב-Python, שורה אחרי שורה.

- Line 1 typed, `def swap_temp(v, i, j):`; it is lit softly while the caption shows.

> ב-Python אין העברה של int by reference,
> ולכן מעבירים רשימה v ושני אינדקסים, i ו-j.

- `a ≡ v[i]` and `b ≡ v[j]` appear under the panel.

> כאן v[i] משחק את התפקיד של a,
> ו-v[j] את התפקיד של b.

- Line 2 typed, `temp = v[i]`.

> שורה 2 : שומרים ב-temp את v[i],
> הערך של a, לפני שדורסים אותו.

- Line 3 typed, `v[i] = v[j]`.

> שורה 3 : עכשיו מותר לדרוס את v[i],
> והוא מקבל את הערך של b.

- Line 4 typed, `v[j] = temp`.

> שורה 4 : v[j] מקבל את הערך המקורי של a,
> ששמור ב-temp.

**The code, run, beside the box.** The split screen: the panel moves to the left, the
page's box fades in on the right at its first line; each traced line is lit as the box
steps to the same line (a ring on "next").

> מימין, התיבה מהעמוד מריצה את אותו הקוד
> על [5, 3], עם i = 0 ו-j = 1.

- Line 2 lit, `temp = 5`.

> קודם temp מקבל את v[i], כלומר 5.

- Line 3 lit, `v[0] = 3`.

> אחר כך v[i] מקבל את v[j], כלומר 3.

- Line 4 lit, `v[1] = 5`.

> ובסוף v[j] מקבל את temp,
> והרשימה היא עכשיו [3, 5].

**Why it works.** A table: a row per moment (start, after 1, 2, 3), the columns `a`, `b`,
`temp`; 5 in amber, 3 in blue.

> למה זה נכון : נעקוב אחרי 5 ו-3,
> ונראה איפה הם נמצאים אחרי כל שלב.

- In every row, a ring around one 5 and one 3.

> בכל שורה, כל אחד מהם נמצא לפחות במשתנה אחד.
> שום ערך לא הולך לאיבוד.

**The cost.** Two chips: `time O(1)`, `memory 1 int`.

> הסיבוכיות : שלוש השמות, כלומר זמן O(1),
> וזיכרון נוסף של משתנה int אחד.

**The trap.** Fresh cells `a = 5`, `b = 3`, no `temp`; the statement `a = b` first.

> המלכודת : לכתוב a = b לפני ששמרנו את a.

- The 3 travels into `a`; the 5 flashes red and is gone.

> הערך 5 נמחק.
> עכשיו גם a וגם b מחזיקים 3.

- `b = a`: `b` stays 3; a red cross.

> ההשמה b = a כבר לא עוזרת :
> שני המשתנים מסתיימים עם 3.

- The right order `temp = a; a = b; b = temp` written in green.

> לכן השמירה ב-temp חייבת לבוא
> לפני הדריסה הראשונה.

## Chapter ב – no temp, arithmetic

- Chapter card: "סעיף ב", "בלי משתנה עזר".

> סעיף ב : אותה החלפה, בלי אף משתנה עזר.
> מותר להשתמש בפעולות חשבון.

**The problem.** The cells `a = 5`, `b = 3` and a `temp` cell, which is struck out and
fades away.

> אין temp. לכן הערך הראשון שנכתוב
> צריך לשמור מידע על שני הערכים.

**The idea.** `5 + 3 = 8`, a brace over the sum.

> הרעיון : הסכום 8 מחזיק את שני הערכים ביחד.

- `8 − 3 = 5` and `8 − 5 = 3` below it.

> כשיודעים את הסכום ואחד הערכים,
> חיסור מחזיר את השני.

**The steps.** The cells, each with its symbolic value under it (`a₀`, `b₀`).

> שלב 1 : a = a + b, ועכשיו a מחזיק 8,
> הסכום של שניהם.

> שלב 2 : b = a − b, כלומר 8 פחות 3,
> ו-b מקבל 5.

> שלב 3 : a = a − b, כלומר 8 פחות 5,
> ו-a מקבל 3. הערכים הוחלפו.

**The page's box.** The box of the part, captured from the site, large; each step a
click on "next" (an amber ring) and the box's next line.

> בתיבה שבעמוד, אותן שלוש שורות,
> ועמודה סימבולית שעוקבת אחרי a0 ו-b0.

> ‏v[i] מקבל את הסכום, 8,
> ובסימבולית a0 + b0.

> ‏v[j] מקבל את הסכום פחות b0,
> כלומר 8 − 3 = 5, שהוא a0.

> ‏v[i] מקבל את הסכום פחות a0,
> כלומר 8 − 5 = 3, שהוא b0.

**The code, typed.** The empty panel of `swap_arith`; each line is typed with its
comment (`# a = a0 + b0` ...).

> בקוד מהעמוד אותן שלוש שורות, על v[i] ו-v[j].

- Line 1 typed.

> אותה חתימה כמו בסעיף א :
> רשימה v ושני אינדקסים, בלי temp.

- Line 2 typed, with its comment.

> שורה 2 : v[i] נדרס בסכום של שניהם,
> וההערה רושמת a = a0 + b0.

- Line 3 typed.

> שורה 3 : הסכום פחות b0 משאיר את a0,
> וזה הערך החדש של v[j].

- Line 4 typed.

> שורה 4 : הסכום פחות a0 משאיר את b0,
> וזה הערך החדש של v[i].

**The code, run, beside the box.** The split screen: the panel moves to the left, the
page's box fades in on the right at its first line; each traced line is lit as the box
steps to the same line (a ring on "next").

> ונריץ ליד התיבה מהעמוד,
> על אותה דוגמה, v = [5, 3].

> קודם v[i] מקבל את הסכום, 8.

> אחר כך v[j] מקבל 8 פחות 3, כלומר 5.

> ובסוף v[i] מקבל 8 פחות 5, כלומר 3.

> ב-Python הסכום אף פעם לא גולש,
> כי מספרים שלמים הם בגודל לא מוגבל.

**Why it works.** A number line from 0 to 9 with 3, 5 and 8 marked.

> למה זה נכון : על ציר המספרים,
> מ-8 חוזרים 3 צעדים ומגיעים ל-5.

> ומ-8 חוזרים 5 צעדים ומגיעים ל-3.
> שום מידע לא אבד.

- The symbolic table of the page: start, 1, 2, 3 with `a₀`, `b₀`.

> ובאופן כללי, עם a₀ ו-b₀ :
> בסוף a = b₀ ו-b = a₀, לכל שני ערכים.

**Overflow.** The 32-bit wheel: 0 at the top, the positive values down the right side,
the negative ones up the left, the seam at the bottom between `2³¹ − 1` and `−2³¹` (not
to scale).

> ומה עם גלישה? ב-SystemVerilog, int הוא 32 ביט,
> והחשבון הוא מודולו 2³².

- The seam lights up.

> הערכים יושבים על גלגל :
> אחרי 2³¹ − 1 בא מיד −2³¹.

- A dot for `a` at `2³¹ − 1`; one step forward crosses the seam to `−2³¹`.

> נניח a = 2³¹ − 1 ו-b = 1.
> הסכום עובר את התפר ונעטף אל −2³¹.

- `b = a − b`: a dot steps back across the seam to `2³¹ − 1`.

> שלב 2 : החיסור מסובב את הגלגל אחורה,
> ו-b מקבל 2³¹ − 1.

- `a = a − b`: the dot for `a` lands on 1.

> שלב 3 : a מקבל 1.
> ההחלפה נכונה, למרות שהסכום גלש.

- The identity `((a₀ + b₀) − b₀) mod 2³² = a₀ mod 2³²`.

> כל השוויונים נכונים גם מודולו 2³²,
> ולכן הגלישה לא מזיקה.

**The cost.** Two chips: `time O(1)`, `memory 0`.

> הסיבוכיות : זמן O(1), וזיכרון נוסף אפס,
> וזה כל העניין של הסעיף.

**The trap.** One cell `x = 5`, the names `a` and `b` both pointing at it.

> המלכודת : לקרוא ל-swap עם אותו משתנה פעמיים,
> למשל swap(x, x).

- `x = x + x`: 10.

> כאן a ו-b הם שני שמות לאותו משתנה.
> שלב 1 : x מקבל 5 + 5, כלומר 10.

- `x = x − x`: 0, in red.

> שלב 2 : x מקבל x − x, כלומר 0.
> הערך המקורי אבד.

- `x = x − x`: still 0.

> שלב 3 משאיר 0.
> הגרסה עם temp לא נפגעת מזה.

> ב-Python מגינים על הפונקציה בבדיקה :
> אם i == j, יוצאים מיד.

## Chapter ג – bitwise only

- Chapter card: "סעיף ג", "רק אופרטורים על ביטים".

> סעיף ג : בלי משתנה עזר ובלי חשבון.
> מותר רק &, |, ^ ו-~.

**The problem.** The two values as 4-bit rows: `a = 0101` (5), `b = 0011` (3), the bits in
columns.

> נכתוב את שני הערכים בביטים :
> הערך 5 הוא 0101, והערך 3 הוא 0011.

**The idea.** The XOR table, 2×2.

> הרעיון : XOR, שנותן 1 בדיוק כשהביטים שונים.

- `x ^ x = 0` and `x ^ 0 = x` beside it.

> לכן x ^ x = 0 ו-x ^ 0 = x.
> כך XOR הוא גם החיבור וגם החיסור של סעיף ב.

**The steps.** In each step the columns where the other row has a 1 light up, and the bits
there flip.

> שלב 1 : a = a ^ b. הביט של a מתהפך
> בכל עמודה שבה ב-b יש 1.

> עכשיו a הוא 0110, כלומר 6 :
> הוא מסמן את העמודות שבהן 5 ו-3 שונים.

> שלב 2 : b = a ^ b, ו-b מתהפך היכן ש-a הוא 1.
> יוצא 0101, כלומר 5.

> שלב 3 : a = a ^ b, ו-a מתהפך היכן ש-b הוא 1.
> יוצא 0011, כלומר 3.

**The page's box.** The box of the part, captured from the site, large; each step a
click on "next" (an amber ring) and the box's next line.

> והתיבה שבעמוד, הפעם עם XOR :
> אותן שלוש שורות, עם ^.

> ‏v[i] מקבל 5 ^ 3, כלומר 6,
> ובסימבולית a0 ^ b0.

> ‏v[j] מקבל 6 ^ 3, כלומר 5 :
> ה-b0 מתבטל ונשאר a0.

> ‏v[i] מקבל 6 ^ 5, כלומר 3 :
> ה-a0 מתבטל ונשאר b0.

**The code, typed.** The empty panel of `swap_xor`, typed line by line with its comments.

> הקוד מהעמוד : אותן שלוש שורות,
> עם ^ במקום + ו-−.

- Line 1 typed.

> שוב אותה חתימה : רשימה v ושני אינדקסים.

- Line 2 typed.

> שורה 2 : v[i] מקבל a0 ^ b0,
> העמודות שבהן שני הערכים שונים.

- Line 3 typed.

> שורה 3 : XOR עם b0 מבטל אותו,
> ונשאר a0, הערך החדש של v[j].

- Line 4 typed.

> שורה 4 : XOR עם a0 מבטל אותו,
> ונשאר b0, הערך החדש של v[i].

**The code, run, beside the box.** The split screen: the panel moves to the left, the
page's box fades in on the right at its first line; each traced line is lit as the box
steps to the same line (a ring on "next").

> ועכשיו הריצה על 5 ו-3,
> לצד התיבה מהעמוד.

> קודם v[i] מקבל 5 ^ 3, כלומר 6.

> אחר כך v[j] מקבל 6 ^ 3, כלומר 5.

> ובסוף v[i] מקבל 6 ^ 5, כלומר 3.

**Why it works.** The truth table of the page: `a₀`, `b₀`, step 1, step 2, step 3.

> למה זה נכון : XOR פועל על כל עמודה לבד,
> בלי נשא, אז מספיק לבדוק ביט אחד.

- The four rows fill in.

> יש רק ארבעה צירופים של a₀ ו-b₀.
> נריץ על כל אחד את שלושת השלבים.

- The column of step 2 rings green against `a₀`, step 3 against `b₀`.

> בכל הארבעה, שלב 2 מחזיר את a₀,
> ושלב 3 מחזיר את b₀.

- The algebra: `(a₀ ^ b₀) ^ b₀ = a₀ ^ (b₀ ^ b₀) = a₀ ^ 0 = a₀`.

> ובאלגברה : b₀ ^ b₀ מתבטל ל-0, ונשאר a₀.

**The cost.** Two chips: `time O(1)`, `memory 0`.

> הסיבוכיות : זמן O(1) וזיכרון אפס,
> בלי נשא ובלי גלישה.

> שלוש הפעולות תלויות זו בזו, ולכן רצות בטור.
> זה טריק, לא אופטימיזציה.

**The traps.** One cell `x = 0101`, `x ^ x`.

> מלכודת ראשונה : שוב אותו משתנה.
> כי x ^ x הוא 0, והערך נמחק כבר בשלב 1.

- The tables of `&` and `|` beside XOR's.

> מלכודת שנייה : למה לא & או |?
> כי הם מאבדים מידע.

- In the `&` table, the row `b = 0`: both cells 0, ringed red.

> בעמודה שבה b הוא 0, a & b יוצא 0
> גם כש-a היה 0 וגם כש-a היה 1.

- In the `|` table, the row `b = 1`: both cells 1, ringed red.

> ב-| אותו דבר כש-b הוא 1.
> אחרי זה כבר אי אפשר לשחזר את a.

- XOR's rows ringed green: each row holds 0 and 1.

> רק ב-XOR, כש-b ידוע,
> אפשר תמיד לשחזר את a.

## Closing

- The three answers, a line each, with the part's letter: `temp = a; a = b; b = temp`,
  `a = a + b; b = a - b; a = a - b`, `a = a ^ b; b = a ^ b; a = a ^ b`.

> לסיכום : משתנה עזר, סכום וחיסור,
> או שלוש פעולות XOR.

- The DV mark, the site's address and `#0002`.

> נסו את שלוש הגרסאות בתיבה
> שבעמוד של שאלה 0002 באתר.
