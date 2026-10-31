# 0002 — swap two variables: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0002 : החלפת ערכים בין שני משתנים,
he: שאלה ברמת סטודנט.
en: Question 0002: swapping the values of two variables,
en: a student-level question.

he: שלושה סעיפים, וכל סעיף מוסיף אילוץ :
he: עם משתנה עזר, בלי משתנה עזר, ורק ביטים.
en: Three parts, and each part adds a constraint:
en: with a temp variable, without one, and bits only.

he: הפונקציה swap מקבלת שני משתנים, a ו-b,
he: ומחליפה ביניהם במקום.
en: The function swap takes two variables, a and b,
en: and swaps them in place.

he: בסוף a מחזיק את הערך המקורי של b,
he: ו-b את הערך המקורי של a.
en: At the end, a holds the original value of b,
en: and b holds the original value of a.

he: סעיף א : הדרך הפשוטה ביותר, עם משתנה עזר.
en: Part A: the simplest way, with a temp variable.

he: יש לנו שני משתנים : a שווה 5, ו-b שווה 3.
en: We have two variables: a equals 5, and b equals 3.

he: המטרה : ש-a יחזיק 3, ו-b יחזיק 5.
en: The goal: a should hold 3, and b should hold 5.

he: הרעיון : משתנה עזר, temp,
he: ששומר את הערך של a לפני שדורסים אותו.
en: The idea: an extra variable, temp,
en: that saves the value of a before it is overwritten.

he: שלב 1 : temp = a. הערך 5 נשמר ב-temp.
en: Step 1: temp = a. The value 5 is saved in temp.

he: שלב 2 : a = b. עכשיו a מחזיק 3,
he: וה-5 המקורי עדיין שמור ב-temp.
en: Step 2: a = b. Now a holds 3,
en: and the original 5 is still saved in temp.

he: שלב 3 : b = temp, ו-b מקבל 5.
he: ההחלפה הושלמה.
en: Step 3: b = temp, and b gets 5.
en: The swap is complete.

he: ב-Python אין העברה של int by reference,
he: ולכן מעבירים רשימה v ושני אינדקסים, i ו-j.
en: Python cannot pass an int by reference,
en: so we pass a list v and two indices, i and j.

he: כאן v[i] משחק את התפקיד של a,
he: ו-v[j] את התפקיד של b.
en: Here v[i] plays the role of a,
en: and v[j] plays the role of b.

he: שורה 2 : temp מקבל את v[i], כלומר 5.
en: Line 2: temp gets v[i], that is, 5.

he: שורה 3 : v[i] מקבל את v[j], כלומר 3.
en: Line 3: v[i] gets v[j], that is, 3.

he: שורה 4 : v[j] מקבל את temp,
he: והרשימה היא עכשיו [3, 5].
en: Line 4: v[j] gets temp,
en: and the list is now [3, 5].

he: למה זה נכון : נעקוב אחרי 5 ו-3,
he: ונראה איפה הם נמצאים אחרי כל שלב.
en: Why it works: let's follow 5 and 3,
en: and see where they are after each step.

he: בכל שורה, כל אחד מהם נמצא לפחות במשתנה אחד.
he: שום ערך לא הולך לאיבוד.
en: In every row, each of them is in at least one variable.
en: No value is ever lost.

he: הסיבוכיות : שלוש השמות, כלומר זמן O(1),
he: וזיכרון נוסף של משתנה int אחד.
en: The cost: three assignments, so O(1) time,
en: and extra memory of one int variable.

he: המלכודת : לכתוב a = b לפני ששמרנו את a.
en: The trap: writing a = b before saving a.

he: הערך 5 נמחק.
he: עכשיו גם a וגם b מחזיקים 3.
en: The value 5 is erased.
en: Now both a and b hold 3.

he: ההשמה b = a כבר לא עוזרת :
he: שני המשתנים מסתיימים עם 3.
en: The assignment b = a no longer helps:
en: both variables end up with 3.

he: לכן השמירה ב-temp חייבת לבוא
he: לפני הדריסה הראשונה.
en: So saving into temp must come
en: before the first overwrite.

he: סעיף ב : אותה החלפה, בלי אף משתנה עזר.
he: מותר להשתמש בפעולות חשבון.
en: Part B: the same swap, with no temp variable at all.
en: Arithmetic operations are allowed.

he: אין temp. לכן הערך הראשון שנכתוב
he: צריך לשמור מידע על שני הערכים.
en: There is no temp. So the first value we write
en: must keep information about both values.

he: הרעיון : הסכום 8 מחזיק את שני הערכים ביחד.
en: The idea: the sum, 8, holds both values together.

he: כשיודעים את הסכום ואחד הערכים,
he: חיסור מחזיר את השני.
en: Knowing the sum and one of the values,
en: a subtraction gives back the other.

he: שלב 1 : a = a + b, ועכשיו a מחזיק 8,
he: הסכום של שניהם.
en: Step 1: a = a + b, and now a holds 8,
en: the sum of both.

he: שלב 2 : b = a − b, כלומר 8 פחות 3,
he: ו-b מקבל 5.
en: Step 2: b = a − b, that is, 8 minus 3,
en: and b gets 5.

he: שלב 3 : a = a − b, כלומר 8 פחות 5,
he: ו-a מקבל 3. הערכים הוחלפו.
en: Step 3: a = a − b, that is, 8 minus 5,
en: and a gets 3. The values are swapped.

he: בקוד מהעמוד אותן שלוש שורות, על v[i] ו-v[j].
en: The page's code: the same three lines, on v[i] and v[j].

he: שורה 2 : v[i] מקבל את הסכום, 8.
en: Line 2: v[i] gets the sum, 8.

he: שורה 3 : v[j] מקבל 8 פחות 3, כלומר 5.
en: Line 3: v[j] gets 8 minus 3, that is, 5.

he: שורה 4 : v[i] מקבל 8 פחות 5, כלומר 3.
en: Line 4: v[i] gets 8 minus 5, that is, 3.

he: ב-Python הסכום אף פעם לא גולש,
he: כי מספרים שלמים הם בגודל לא מוגבל.
en: In Python the sum never overflows,
en: because Python integers are unbounded.

he: למה זה נכון : על ציר המספרים,
he: מ-8 חוזרים 3 צעדים ומגיעים ל-5.
en: Why it works: on the number line,
en: going back 3 steps from 8 lands on 5.

he: ומ-8 חוזרים 5 צעדים ומגיעים ל-3.
he: שום מידע לא אבד.
en: And going back 5 steps from 8 lands on 3.
en: No information is lost.

he: ובאופן כללי, עם a₀ ו-b₀ :
he: בסוף a = b₀ ו-b = a₀, לכל שני ערכים.
en: And in general, with a₀ and b₀:
en: at the end a = b₀ and b = a₀, for any two values.

he: ומה עם גלישה? ב-SystemVerilog, int הוא 32 ביט,
he: והחשבון הוא מודולו 2³².
en: What about overflow? In SystemVerilog, int is 32 bits,
en: and the arithmetic is modulo 2³².

he: הערכים יושבים על גלגל :
he: אחרי 2³¹ − 1 בא מיד −2³¹.
en: The values sit on a wheel:
en: right after 2³¹ − 1 comes −2³¹.

he: נניח a = 2³¹ − 1 ו-b = 1.
he: הסכום עובר את התפר ונעטף אל −2³¹.
en: Say a = 2³¹ − 1 and b = 1.
en: The sum crosses the seam and wraps around to −2³¹.

he: שלב 2 : החיסור מסובב את הגלגל אחורה,
he: ו-b מקבל 2³¹ − 1.
en: Step 2: the subtraction turns the wheel back,
en: and b gets 2³¹ − 1.

he: שלב 3 : a מקבל 1.
he: ההחלפה נכונה, למרות שהסכום גלש.
en: Step 3: a gets 1.
en: The swap is correct, even though the sum overflowed.

he: כל השוויונים נכונים גם מודולו 2³²,
he: ולכן הגלישה לא מזיקה.
en: All the equalities also hold modulo 2³²,
en: so the overflow does no harm.

he: הסיבוכיות : זמן O(1), וזיכרון נוסף אפס,
he: וזה כל העניין של הסעיף.
en: The cost: O(1) time and zero extra memory,
en: which is the whole point of this part.

he: המלכודת : לקרוא ל-swap עם אותו משתנה פעמיים,
he: למשל swap(x, x).
en: The trap: calling swap with the same variable twice,
en: for example swap(x, x).

he: כאן a ו-b הם שני שמות לאותו משתנה.
he: שלב 1 : x מקבל 5 + 5, כלומר 10.
en: Here a and b are two names for the same variable.
en: Step 1: x gets 5 + 5, that is, 10.

he: שלב 2 : x מקבל x − x, כלומר 0.
he: הערך המקורי אבד.
en: Step 2: x gets x − x, that is, 0.
en: The original value is lost.

he: שלב 3 משאיר 0.
he: הגרסה עם temp לא נפגעת מזה.
en: Step 3 leaves 0.
en: The temp version is not affected by this.

he: ב-Python מגינים על הפונקציה בבדיקה :
he: אם i == j, יוצאים מיד.
en: In Python, the function is guarded by a check:
en: if i == j, return at once.

he: סעיף ג : בלי משתנה עזר ובלי חשבון.
he: מותר רק &, |, ^ ו-~.
en: Part C: no temp variable and no arithmetic.
en: Only &, |, ^ and ~ are allowed.

he: נכתוב את שני הערכים בביטים :
he: הערך 5 הוא 0101, והערך 3 הוא 0011.
en: Let's write both values in bits:
en: 5 is 0101, and 3 is 0011.

he: הרעיון : XOR, שנותן 1 בדיוק כשהביטים שונים.
en: The idea: XOR, which gives 1 exactly when the bits differ.

he: לכן x ^ x = 0 ו-x ^ 0 = x.
he: כך XOR הוא גם החיבור וגם החיסור של סעיף ב.
en: So x ^ x = 0 and x ^ 0 = x.
en: XOR is thus both the addition and the subtraction of part B.

he: שלב 1 : a = a ^ b. הביט של a מתהפך
he: בכל עמודה שבה ב-b יש 1.
en: Step 1: a = a ^ b. A bit of a flips
en: in every column where b has a 1.

he: עכשיו a הוא 0110, כלומר 6 :
he: הוא מסמן את העמודות שבהן 5 ו-3 שונים.
en: Now a is 0110, that is, 6:
en: it marks the columns where 5 and 3 differ.

he: שלב 2 : b = a ^ b, ו-b מתהפך היכן ש-a הוא 1.
he: יוצא 0101, כלומר 5.
en: Step 2: b = a ^ b, and b flips where a is 1.
en: The result is 0101, that is, 5.

he: שלב 3 : a = a ^ b, ו-a מתהפך היכן ש-b הוא 1.
he: יוצא 0011, כלומר 3.
en: Step 3: a = a ^ b, and a flips where b is 1.
en: The result is 0011, that is, 3.

he: הקוד מהעמוד : אותן שלוש שורות,
he: עם ^ במקום + ו-−.
en: The code from the page: the same three lines,
en: with ^ instead of + and −.

he: שורה 2 : v[i] מקבל 5 ^ 3, כלומר 6.
en: Line 2: v[i] gets 5 ^ 3, that is, 6.

he: שורה 3 : v[j] מקבל 6 ^ 3, כלומר 5.
en: Line 3: v[j] gets 6 ^ 3, that is, 5.

he: שורה 4 : v[i] מקבל 6 ^ 5, כלומר 3.
en: Line 4: v[i] gets 6 ^ 5, that is, 3.

he: למה זה נכון : XOR פועל על כל עמודה לבד,
he: בלי נשא, אז מספיק לבדוק ביט אחד.
en: Why it works: XOR acts on each column alone,
en: with no carry, so checking one bit is enough.

he: יש רק ארבעה צירופים של a₀ ו-b₀.
he: נריץ על כל אחד את שלושת השלבים.
en: There are only four combinations of a₀ and b₀.
en: We run the three steps on each one.

he: בכל הארבעה, שלב 2 מחזיר את a₀,
he: ושלב 3 מחזיר את b₀.
en: In all four, step 2 gives back a₀,
en: and step 3 gives back b₀.

he: ובאלגברה : b₀ ^ b₀ מתבטל ל-0, ונשאר a₀.
en: And in algebra: b₀ ^ b₀ cancels to 0, leaving a₀.

he: הסיבוכיות : זמן O(1) וזיכרון אפס,
he: בלי נשא ובלי גלישה.
en: The cost: O(1) time and zero memory,
en: with no carry and no overflow.

he: שלוש הפעולות תלויות זו בזו, ולכן רצות בטור.
he: זה טריק, לא אופטימיזציה.
en: The three steps depend on each other, so they run serially.
en: It is a trick, not an optimization.

he: מלכודת ראשונה : שוב אותו משתנה.
he: כי x ^ x הוא 0, והערך נמחק כבר בשלב 1.
en: First trap: the same variable again.
en: Since x ^ x is 0, step 1 already erases the value.

he: מלכודת שנייה : למה לא & או |?
he: כי הם מאבדים מידע.
en: Second trap: why not & or |?
en: Because they lose information.

he: בעמודה שבה b הוא 0, a & b יוצא 0
he: גם כש-a היה 0 וגם כש-a היה 1.
en: Where b is 0, a & b comes out 0
en: whether a was 0 or 1.

he: ב-| אותו דבר כש-b הוא 1.
he: אחרי זה כבר אי אפשר לשחזר את a.
en: The same with | when b is 1.
en: After that, a can no longer be recovered.

he: רק ב-XOR, כש-b ידוע,
he: אפשר תמיד לשחזר את a.
en: Only with XOR, when b is known,
en: can a always be recovered.

he: לסיכום : משתנה עזר, סכום וחיסור,
he: או שלוש פעולות XOR.
en: To sum up: a temp variable, a sum and subtractions,
en: or three XOR operations.

he: נסו את שלוש הגרסאות בתיבה
he: שבעמוד של שאלה 0002 באתר.
en: Try all three versions in the box
en: on the page of question 0002 on the site.
