# 0012 — sort the digits and subtract: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); notes/VIDEOS.md.

he: שאלה 0012 : ממיינים ספרות ומחסרים,
he: שאלה ברמת סטודנט.
en: Question 0012: sort the digits and subtract,
en: a student-level question.

he: שלושה סעיפים : לבדוק מספר אחד,
he: לבדוק את כל המספרים, ובסיס אחר.
en: Three parts: check one number,
en: check every number, and another base.

he: לוקחים מספר בין 0 ל-999, למשל 352,
he: וכותבים אותו בשלוש ספרות.
en: Take a number from 0 to 999, say 352,
en: and write it with three digits.

he: ממיינים את הספרות מהגדול לקטן, 532,
he: ומהקטן לגדול, 235.
en: Sort the digits from largest to smallest, 532,
en: and from smallest to largest, 235.

he: מחסרים את הקטן מהגדול,
he: ומקבלים 297.
en: Subtract the smaller from the larger,
en: and get 297.

he: אם ההפרש שווה למספר עצמו,
he: המספר נקרא מיוחד.
en: If the difference equals the number itself,
en: the number is called special.

he: כאן 297 שונה מ-352,
he: ולכן 352 לא מיוחד.
en: Here 297 differs from 352,
en: so 352 is not special.

he: סעיף א : פונקציה שמקבלת מספר x,
he: ומחזירה 1 אם הוא מיוחד, ו-0 אחרת.
en: Part A: a function that takes a number x,
en: and returns 1 if it is special, 0 otherwise.

he: קודם כול : מספר קטן מ-100 מקבל
he: אפסים משמאל. ‏7 נכתב 007.
en: First: a number below 100 gets
en: leading zeros. 7 is written 007.

he: מהגדול לקטן זה 700, ומהקטן לגדול 007 :
he: ההפרש 693.
en: Largest to smallest is 700, smallest to largest 007:
en: the difference is 693.

he: הרעיון : שני המספרים בנויים
he: מאותן שלוש ספרות.
en: The idea: both numbers are built
en: from the same three digits.

he: ממיינים פעם אחת בסדר עולה :
he: זה המספר הקטן, 235.
en: Sort once, in ascending order:
en: that is the smaller number, 235.

he: אותן ספרות בסדר הפוך הן הגדול,
he: ‏532. אין צורך במיון שני.
en: The same digits reversed are the larger,
en: 532. No second sort is needed.

he: כך זה נראה בתיבה שבעמוד :
he: החיסור במאונך, עמודה אחרי עמודה.
en: This is how the page's box shows it:
en: the column subtraction, column by column.

he: ‏532 פחות 235, עם שני לווים :
he: ההפרש 297, ולכן 352 לא מיוחד.
en: 532 minus 235, with two borrows:
en: the difference is 297, so 352 is not special.

he: הדוגמה 7 : ‏700 פחות 007 הם 693.
en: The example 7: 700 minus 007 is 693.

he: הדוגמה 45 : ‏540 פחות 045 הם 495.
he: ההפרש שונה מ-45, ולכן 45 לא מיוחד.
en: The example 45: 540 minus 045 is 495.
en: That differs from 45, so 45 is not special.

he: ועכשיו 495 : ‏954 פחות 459
he: הם 495 בדיוק. הוא מיוחד.
en: And now 495: 954 minus 459
en: is exactly 495. It is special.

he: עכשיו נכתוב את זה ב-Python.
en: Now let's write it in Python.

he: הפונקציה is_special מקבלת את x,
he: ומחזירה 1 או 0.
en: The function is_special takes x,
en: and returns 1 or 0.

he: הפורמט 03d כותב את x בשלוש ספרות,
he: עם אפסים משמאל : 7 הופך ל-007.
en: The format 03d writes x with three digits,
en: leading zeros included: 7 becomes 007.

he: ‏sorted ממיינת את שלושת התווים
he: בסדר עולה, לרשימה.
en: sorted sorts the three characters
en: in ascending order, into a list.

he: החיבור של התווים בסדר עולה
he: נותן את המספר הקטן.
en: Joining the characters in ascending order
en: gives the smaller number.

he: אותם תווים בסדר הפוך נותנים
he: את הגדול, בלי מיון שני.
en: The same characters reversed give
en: the larger one, with no second sort.

he: בסוף משווים את ההפרש ל-x,
he: ומחזירים 1 או 0.
en: Finally, compare the difference with x,
en: and return 1 or 0.

he: נריץ את הקוד על 352,
he: לצד התיבה מהעמוד.
en: Let's run the code on 352,
en: beside the page's box.

he: ‏x = 352 : הספרות בסדר עולה
he: הן 2, 3 ו-5.
en: x = 352: the digits in ascending order
en: are 2, 3 and 5.

he: המספר הקטן הוא 235.
en: The smaller number is 235.

he: והגדול הוא 532.
en: And the larger is 532.

he: ‏532 פחות 235 הם 297, לא 352 :
he: הפונקציה מחזירה 0.
en: 532 minus 235 is 297, not 352:
en: the function returns 0.

he: עכשיו x = 495 : הספרות
he: בסדר עולה הן 4, 5 ו-9.
en: Now x = 495: the digits
en: in ascending order are 4, 5 and 9.

he: הקטן הוא 459, והגדול 954.
en: The smaller is 459, the larger 954.

he: ההפרש 495, בדיוק x :
he: הפונקציה מחזירה 1.
en: The difference is 495, exactly x:
en: the function returns 1.

he: הסיבוכיות : תמיד שלוש ספרות,
he: ולכן זמן O(1) וזיכרון O(1).
en: The cost: always three digits,
en: so O(1) time and O(1) memory.

he: מלכודת : לשכוח את האפסים. בלי ריפוד,
he: ‏45 נותן 54 פחות 45, כלומר 9.
en: A trap: forgetting the zeros. Without padding,
en: 45 gives 54 minus 45, that is 9.

he: עם ריפוד זה 540 פחות 045, כלומר 495.
he: מספר קטן הוא עדיין מספר בן שלוש ספרות.
en: With padding it is 540 minus 045, that is 495.
en: A small number is still a three-digit number.

he: סעיף ב : מריצים את הפונקציה על 0 עד 999.
he: אילו מספרים מיוחדים, ולמה?
en: Part B: run the function on 0 to 999.
en: Which numbers are special, and why?

he: נסמן את הספרות הממוינות :
he: הגדולה a, האמצעית b, והקטנה c.
en: Name the sorted digits:
en: the largest a, the middle b, the smallest c.

he: הגדול פחות הקטן : מאות, עשרות ואחדות,
he: פעם בסדר אחד ופעם בסדר ההפוך.
en: The larger minus the smaller: hundreds, tens, units,
en: once in one order and once reversed.

he: ספרת האמצע b מופיעה פעמיים, 10b,
he: ומתבטלת בחיסור.
en: The middle digit b appears twice, as 10b,
en: and cancels in the subtraction.

he: נשאר 99 כפול a פחות c :
he: ההפרש תמיד כפולה של 99.
en: What is left is 99 times a minus c:
en: the difference is always a multiple of 99.

he: נסמן d = a − c. הוא בין 0 ל-9,
he: ולכן יש רק עשרה הפרשים אפשריים.
en: Let d = a − c. It is between 0 and 9,
en: so only ten differences are possible.

he: מספר מיוחד שווה להפרש שלו,
he: ולכן הוא אחד מעשרת המועמדים האלה.
en: A special number equals its difference,
en: so it is one of these ten candidates.

he: בודקים את תשעת המועמדים שאינם 0 :
he: ממיינים, מחסרים ומשווים.
en: Check the nine non-zero candidates:
en: sort, subtract and compare.

he: רק 495 חוזר לעצמו : ‏954 פחות 459.
he: יחד עם 0, אלה שני המספרים המיוחדים.
en: Only 495 returns to itself: 954 minus 459.
en: With 0, these are the two special numbers.

he: שימו לב : d ו-10 פחות d בנויים
he: מאותן ספרות, ונותנים אותו הפרש.
en: Note: d and 10 minus d are built
en: from the same digits, and give the same difference.

he: ההוכחה בלי טבלה : ל-99d יש תמיד
he: את הספרות d − 1, ‏9 ו-10 − d.
en: The proof without the table: 99d always
en: has the digits d − 1, 9 and 10 − d.

he: אם x שווה להפרש, יש בו 9, הספרה
he: הגדולה ביותר : לכן a = 9, ו-c = 9 − d.
en: If x equals its difference, it has a 9, the largest
en: digit: so a = 9, and c = 9 − d.

he: שתי הספרות האחרות שוות לשתיים מימין,
he: ו-9 − d לא יכול להיות 10 − d.
en: The other two digits equal the two on the right,
en: and 9 − d cannot be 10 − d.

he: לכן 9 − d = d − 1, כלומר d = 5,
he: והמספר הוא 99 כפול 5 : ‏495.
en: So 9 − d = d − 1, that is d = 5,
en: and the number is 99 times 5: 495.

he: ובקוד : בלי ההוכחה, פשוט בודקים הכול.
en: And in code: no proof, just check everything.

he: ‏find_special לא מקבלת כלום,
he: ומחזירה רשימה.
en: find_special takes nothing,
en: and returns a list.

he: היא עוברת על x מ-0 עד 999, ושומרת
he: כל x ש-is_special מחזירה עבורו 1.
en: It goes over x from 0 to 999, and keeps
en: every x for which is_special returns 1.

he: ‏x = 0 : כל הספרות 0, וההפרש 0.
he: הוא מיוחד, ונכנס לרשימה.
en: x = 0: all digits are 0, the difference is 0.
en: It is special, and joins the list.

he: מ-1 עד 494 אין אף מספר מיוחד,
he: ולכן קופצים קדימה.
en: From 1 to 494 no number is special,
en: so we jump ahead.

he: ‏x = 495 : ‏954 פחות 459 הם 495.
he: מיוחד, ונכנס לרשימה.
en: x = 495: 954 minus 459 is 495.
en: Special, and it joins the list.

he: ומ-496 עד 999 שוב אין אף אחד :
he: התוצאה היא 0 ו-495.
en: And from 496 to 999 there is none again:
en: the result is 0 and 495.

he: התיבה שבעמוד מפעילה את הצעד שוב ושוב
he: על ההפרש : ‏352 מגיע ל-495.
en: The page's box applies the step again and again
en: to the difference: 352 reaches 495.

he: ‏100 הוא הארוך ביותר : שישה צעדים
he: עד 495, ושם הוא נעצר.
en: 100 is the longest: six steps
en: to 495, where it stops.

he: על כל 1,000 המספרים : ‏990 מגיעים ל-495
he: תוך שישה צעדים לכל היותר, ו-10 ל-0.
en: Over all 1,000 numbers: 990 reach 495
en: within six steps at most, and 10 reach 0.

he: והמפה של d : ‏352 נותן d = 3.
he: כל צעד מעביר את d לערך הבא.
en: And the map of d: 352 gives d = 3.
en: Each step moves d to its next value.

he: צעד 1 : ‏352 הופך ל-297,
he: ו-d קופץ מ-3 ל-7.
en: Step 1: 352 becomes 297,
en: and d jumps from 3 to 7.

he: צעד 2 : ‏297 הופך ל-693, ו-d = 6.
en: Step 2: 297 becomes 693, and d = 6.

he: צעד 3 : ‏693 הופך ל-594, ו-d = 5.
en: Step 3: 693 becomes 594, and d = 5.

he: צעד 4 : ‏594 הופך ל-495. רק 5
he: מצביע על עצמו : נקודת השבת.
en: Step 4: 594 becomes 495. Only 5
en: points to itself: the fixed point.

he: הלולאה בודקת 1,000 מספרים, כל אחד ב-O(1).
he: לפי ההוכחה מספיק לבדוק עשרה.
en: The loop checks 1,000 numbers, each in O(1).
en: By the proof, checking ten is enough.

he: סעיף ג, בקצרה : אותו תהליך,
he: אבל המספר כתוב בבסיס b.
en: Part C, briefly: the same process,
en: but the number is written in base b.

he: אותו חישוב : ספרת האמצע מתבטלת,
he: וההפרש הוא d כפול b² − 1.
en: The same computation: the middle digit cancels,
en: and the difference is d times b² − 1.

he: הספרות שלו תמיד d − 1, ‏b − 1 ו-b − d,
he: ולכן ה-d הבא תלוי רק ב-d.
en: Its digits are always d − 1, b − 1 and b − d,
en: so the next d depends only on d.

he: ה-d הבא הוא המקסימום של b − d ו-d − 1 :
he: המפה דוחפת את d לאמצע, b/2.
en: The next d is the maximum of b − d and d − 1:
en: the map pushes d to the middle, b/2.

he: בסיס זוגי : d = b/2 נשאר במקום.
he: נקודת שבת יחידה, ובבסיס 10 זה 495.
en: Even base: d = b/2 stays put.
en: A single fixed point; in base 10 it is 495.

he: בסיס אי-זוגי : אין אמצע שלם, ו-d
he: מתנדנד בין שני שלמים : מחזור באורך 2.
en: Odd base: no whole middle, so d
en: swings between two integers: a cycle of length 2.

he: בתיבה שבעמוד : בסיס 7, מתחילים מ-610.
he: ה-d שלו הוא 6 פחות 0, כלומר 6.
en: In the page's box: base 7, starting from 610.
en: Its d is 6 minus 0, that is 6.

he: צעד 1 : ‏610 הופך ל-561, ו-d = 5.
en: Step 1: 610 becomes 561, and d = 5.

he: צעד 2 : ‏561 הופך ל-462, ו-d = 4.
en: Step 2: 561 becomes 462, and d = 4.

he: צעד 3 : ‏462 הופך ל-363, ו-d = 3.
he: מכאן 363 ו-264 מתחלפים לנצח.
en: Step 3: 462 becomes 363, and d = 3.
en: From here 363 and 264 alternate forever.

he: התשובה : בבסיס זוגי נקודת שבת אחת,
he: ובבסיס אי-זוגי מחזור של שני מספרים.
en: The answer: an even base has one fixed point,
en: an odd base a cycle of two numbers.

he: לסיכום : ממיינים פעם אחת ומחסרים,
he: וההפרש תמיד כפולה של 99.
en: In short: sort once and subtract,
en: and the difference is always a multiple of 99.

he: נסו מספרים ובסיסים משלכם בתיבות
he: שבעמוד של שאלה 0012 באתר.
en: Try your own numbers and bases in the boxes
en: on the page of question 0012 on the site.
