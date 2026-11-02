# 0013 — sort four digits and subtract: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0013 : ממיינים ספרות ומחסרים,
he: הפעם עם ארבע ספרות. רמת ג'וניור.
en: Question 0013: sort the digits and subtract,
en: this time with four digits. Junior level.

he: שלושה סעיפים : לבדוק מספר אחד,
he: לבדוק את כל המספרים, ובסיס B.
en: Three parts: check one number,
en: check every number, and base B.

he: בסרטון של שאלה 0012, עם שלוש ספרות,
he: קיבלנו 495. עכשיו ארבע ספרות.
en: In the video of question 0012, with three digits,
en: we got 495. Now four digits.

he: לוקחים מספר בין 0 ל-9999, למשל 3524,
he: וכותבים אותו בארבע ספרות.
en: Take a number from 0 to 9999, say 3524,
en: and write it with four digits.

he: ממיינים את הספרות מהגדול לקטן, 5432,
he: ומהקטן לגדול, 2345.
en: Sort the digits from largest to smallest, 5432,
en: and from smallest to largest, 2345.

he: מחסרים את הקטן מהגדול,
he: ומקבלים 3087.
en: Subtract the smaller from the larger,
en: and get 3087.

he: אם ההפרש שווה למספר עצמו,
he: המספר נקרא מיוחד.
en: If the difference equals the number itself,
en: the number is called special.

he: כאן 3087 שונה מ-3524,
he: ולכן 3524 לא מיוחד.
en: Here 3087 differs from 3524,
en: so 3524 is not special.

he: סעיף א : פונקציה שמקבלת מספר x,
he: ומחזירה 1 אם הוא מיוחד, ו-0 אחרת.
en: Part A: a function that takes a number x,
en: and returns 1 if it is special, 0 otherwise.

he: הרעיון : שני המספרים בנויים
he: מאותן ארבע ספרות.
en: The idea: both numbers are built
en: from the same four digits.

he: ממיינים פעם אחת בסדר עולה :
he: זה המספר הקטן, 2345.
en: Sort once in ascending order:
en: that is the smaller number, 2345.

he: אותן ספרות בסדר הפוך הן הגדול,
he: ‏5432. אין צורך במיון שני.
en: The same digits reversed are the larger,
en: 5432. No second sort is needed.

he: עכשיו נכתוב את זה ב-Python : כמעט
he: אותו קוד כמו בשלוש ספרות.
en: Now let's write it in Python: almost
en: the same code as with three digits.

he: הפונקציה is_special_4 מקבלת את x,
he: ומחזירה 1 או 0.
en: The function is_special_4 takes x,
en: and returns 1 or 0.

he: הפורמט 04d כותב את x בארבע ספרות,
he: עם אפסים משמאל : 95 הופך ל-0095.
en: The format 04d writes x with four digits,
en: zeros on the left: 95 becomes 0095.

he: ‏sorted ממיינת את ארבעת התווים
he: בסדר עולה, לרשימה.
en: sorted sorts the four characters
en: in ascending order, into a list.

he: החיבור של התווים בסדר עולה
he: נותן את המספר הקטן.
en: Joining the characters in ascending order
en: gives the smaller number.

he: אותם תווים בסדר הפוך נותנים
he: את הגדול, בלי מיון שני.
en: The same characters reversed give
en: the larger, with no second sort.

he: בסוף משווים את ההפרש ל-x,
he: ומחזירים 1 או 0.
en: Finally compare the difference with x,
en: and return 1 or 0.

he: נריץ את הקוד על 3524,
he: לצד החיסור במאונך מהתיבה שבעמוד.
en: Let's run the code on 3524,
en: beside the page box's column subtraction.

he: ‏x = 3524 : הספרות בסדר עולה
he: הן 2, 3, 4 ו-5.
en: x = 3524: the digits in ascending order
en: are 2, 3, 4 and 5.

he: המספר הקטן הוא 2345.
en: The smaller number is 2345.

he: והגדול הוא 5432.
en: And the larger is 5432.

he: ‏5432 פחות 2345 הם 3087, לא 3524 :
he: הפונקציה מחזירה 0.
en: 5432 minus 2345 is 3087, not 3524:
en: the function returns 0.

he: ומה אם מפעילים את אותו צעד שוב ושוב,
he: כל פעם על ההפרש?
en: And what if we apply the same step again and again,
en: each time to the difference?

he: ‏3524 נותן 3087, ‏3087 נותן 8352,
he: ו-8352 נותן 6174.
en: 3524 gives 3087, 3087 gives 8352,
en: and 8352 gives 6174.

he: ושם הוא נעצר : 7641 פחות 1467 הם
he: ‏6174 בדיוק. על 6174 הפונקציה מחזירה 1.
en: And there it stops: 7641 minus 1467 is
en: exactly 6174. On 6174 the function returns 1.

he: מלכודת ראשונה : כל הספרות שוות, כמו
he: ‏7777. ההפרש 0, ולכן 7777 לא מיוחד.
en: First trap: all digits equal, like
en: 7777. The difference is 0, so 7777 is not special.

he: אבל 0 עצמו כן מיוחד : 0000 פחות 0000
he: הם 0, בדיוק המספר. כך גם בטבלה שבעמוד.
en: But 0 itself is special: 0000 minus 0000
en: is 0, the number itself. So says the page's table too.

he: מלכודת שנייה : מספר קצר. בלי אפסים
he: משמאל, 95 נותן 95 פחות 59, כלומר 36.
en: Second trap: a short number. Without zeros
en: on the left, 95 gives 95 minus 59, that is 36.

he: עם ריפוד לארבע ספרות זה 0095 :
he: ‏9500 פחות 0059, כלומר 9441.
en: Padded to four digits it is 0095:
en: 9500 minus 0059, that is 9441.

he: הסיבוכיות : תמיד ארבע ספרות,
he: ולכן זמן O(1) וזיכרון O(1).
en: The cost: always four digits,
en: so O(1) time and O(1) memory.

he: סעיף ב : מריצים את הפונקציה על 0 עד 9999.
he: אילו מספרים מיוחדים, ולמה?
en: Part B: run the function on 0 to 9999.
en: Which numbers are special, and why?

he: נסמן את הספרות הממוינות,
he: מהגדולה a עד הקטנה d.
en: Call the sorted digits,
en: from the largest a to the smallest d.

he: הגדול פחות הקטן : אותן ספרות,
he: פעם בסדר אחד ופעם בסדר ההפוך.
en: The larger minus the smaller: the same digits,
en: once in one order and once reversed.

he: הפעם ספרות האמצע לא מתבטלות,
he: אבל הכול מתקבץ לשני הפרשים.
en: This time the middle digits do not cancel,
en: but everything groups into two gaps.

he: ‏p הוא המרחק בין הגדולה לקטנה,
he: ו-q המרחק בין שתי האמצעיות.
en: p is the gap between the largest and the smallest,
en: and q the gap between the two middle ones.

he: ההפרש הוא 999p ועוד 90q :
he: הוא תלוי רק בזוג p, q.
en: The difference is 999p plus 90q:
en: it depends only on the pair p, q.

he: כי b ו-c בין a ל-d, מתקיים q ≤ p ≤ 9 :
he: יש רק 55 זוגות, ולכן 55 הפרשים.
en: b, c lie between a and d, so q ≤ p ≤ 9:
en: only 55 pairs, so only 55 differences.

he: כל משבצת היא זוג אחד, ובתוכה ההפרש
he: שהוא נותן, 999p + 90q. ‏p = 0 נותן רק 0.
en: Each cell is one pair, holding the difference
en: it gives, 999p + 90q. p = 0 gives only 0.

he: בודקים כל משבצת : האם לספרות של
he: ההפרש יש שוב אותו p ואותו q?
en: Check every cell: do the digits
en: of the difference give the same p and q again?

he: ‏53 משבצות נכשלות : הספרות של
he: ההפרש שלהן נותנות זוג אחר.
en: 53 cells fail: the digits
en: of their difference give another pair.

he: רק משבצת אחת עוברת :
he: ‏p = 6, ‏q = 2, כלומר 6174.
en: Only one cell passes:
en: p = 6, q = 2, that is 6174.

he: יחד עם 0, יש בדיוק שני מספרים
he: מיוחדים : 0 ו-6174.
en: Together with 0, there are exactly two
en: special numbers: 0 and 6174.

he: ולמה? חיסור במאונך נותן את ספרות ההפרש
he: ישר מ-p ו-q, עם לווה בעמודות הנמוכות.
en: Why? Column subtraction gives the digits of the difference
en: straight from p and q, borrowing in the low columns.

he: מספר מיוחד שווה להפרש, ולכן לספרות
he: ההפרש יש אותו p ואותו q : שני תנאים.
en: A special number equals its difference, so the difference's
en: digits have the same p and q: two conditions.

he: כש-q = 0 יש בהפרש שתי ספרות 9, ואז
he: צריך שלוש. זה לא מסתדר : העמודה נפסלת.
en: When q = 0 the difference has two 9s, and then
en: it needs three. That fails: the column is out.

he: כש-q ≥ 1 בודקים מי הספרה הגדולה
he: ומי הקטנה : יש רק שבעה מקרים.
en: When q ≥ 1, check which digit is the largest
en: and which the smallest: only seven cases.

he: שישה מקרים נפסלים. במקרה היחיד
he: שנשאר, הגדולה 9 − q והקטנה q − 1.
en: Six cases are ruled out. In the only one
en: left, the largest is 9 − q, the smallest q − 1.

he: התנאי השני נותן q = 2, ולכן p = 6 :
he: ‏999 · 6 + 90 · 2 = 6174.
en: The second condition gives q = 2, so p = 6:
en: 999 · 6 + 90 · 2 = 6174.

he: ובקוד : בלי ההוכחה, פשוט בודקים הכול.
en: And in code: no proof, just check everything.

he: ‏find_special_4 לא מקבלת כלום,
he: ומחזירה רשימה.
en: find_special_4 takes nothing,
en: and returns a list.

he: היא עוברת על x מ-0 עד 9999, ושומרת
he: כל x ש-is_special_4 מחזירה עבורו 1.
en: It goes over x from 0 to 9999, and keeps
en: every x for which is_special_4 returns 1.

he: ‏x = 0 : כל הספרות 0, וההפרש 0.
he: הוא מיוחד, ונכנס לרשימה.
en: x = 0: all digits are 0, and the difference is 0.
en: It is special, and goes into the list.

he: מ-1 עד 6173 אין אף מספר מיוחד,
he: ולכן קופצים קדימה.
en: From 1 to 6173 there is no special number,
en: so we jump ahead.

he: ‏x = 6174 : ‏7641 פחות 1467 הם 6174.
he: מיוחד, ונכנס לרשימה.
en: x = 6174: 7641 minus 1467 is 6174.
en: Special, and it goes into the list.

he: ומ-6175 עד 9999 שוב אין אף אחד :
he: התוצאה היא 0 ו-6174.
en: And from 6175 to 9999 again there is none:
en: the result is 0 and 6174.

he: בתיבה שבעמוד לוחצים על זוג, והחץ
he: מוביל לזוג של ההפרש הבא. מתחילים מ-9441.
en: In the page's box you click a pair, and the arrow
en: leads to the pair of the next difference. Start from 9441.

he: ‏9441 נותן את הזוג p = 8, ‏q = 0,
he: כלומר 7992.
en: 9441 gives the pair p = 8, q = 0,
en: that is 7992.

he: ‏7992 מוביל ל-7173,
en: 7992 leads to 7173,

he: ‏7173 ל-6354,
en: 7173 to 6354,

he: ‏6354 ל-3087,
en: 6354 to 3087,

he: ו-3087 ל-8352.
en: and 3087 to 8352.

he: ‏8352 מוביל ל-6174, והזוג (6, 2)
he: מצביע על עצמו : המסלול נעצר.
en: 8352 leads to 6174, and the pair (6, 2)
en: points to itself: the path stops.

he: על כל 10,000 המספרים : ‏9,990 מגיעים
he: ל-6174 תוך שבעה צעדים לכל היותר.
en: Over all 10,000 numbers: 9,990 reach
en: 6174 within seven steps at most.

he: ועשרת המספרים שכל הספרות שלהם שוות,
he: כמו 7777, נופלים ל-0.
en: And the ten numbers whose digits are all equal,
en: like 7777, fall to 0.

he: הלולאה בודקת 10,000 מספרים, כל אחד
he: ב-O(1). לפי ההוכחה מספיק לבדוק 55.
en: The loop checks 10,000 numbers, each
en: in O(1). By the proof, checking 55 is enough.

he: סעיף ג, בקצרה : אותו תהליך,
he: אבל המספר כתוב בבסיס B.
en: Part C, briefly: the same process,
en: but the number is written in base B.

he: אותו חישוב, עם B במקום 10 :
he: ההפרש תלוי שוב רק ב-p וב-q.
en: The same computation, with B instead of 10:
en: the difference again depends only on p and q.

he: והספרות שלו, כש-q ≥ 1, הן p, ‏q − 1,
he: ‏B − q − 1 ו-B − p.
en: And its digits, when q ≥ 1, are p, q − 1,
en: B − q − 1 and B − p.

he: אותם שני תנאים. רק חלוקה אחת של
he: הספרות נותנת משפחה : p = 3q ו-B = 5q.
en: The same two conditions. Only one split of
en: the digits gives a family: p = 3q and B = 5q.

he: התשובה : נקודת שבת קיימת כש-B מתחלק
he: ב-5, והספרות שלה 3k, ‏k − 1, ‏4k − 1, ‏2k.
en: The answer: a fixed point exists when B is divisible
en: by 5; its digits: 3k, k − 1, 4k − 1, 2k.

he: בסיס 5 נותן 3032, בסיס 15 נותן 92B6,
he: ובבסיס 10, עם k = 2, זה 6174.
en: Base 5 gives 3032, base 15 gives 92B6,
en: and in base 10, with k = 2, it is 6174.

he: ועוד שני חריגים : 0111 ו-1001 בבסיס 2,
he: ו-3021 בבסיס 4. בכל בסיס אחר אין.
en: And two exceptions: 0111 and 1001 in base 2,
en: and 3021 in base 4. No other base has one.

he: אבל קיום אינו התכנסות. בתיבה שבעמוד :
he: בסיס 15, ונקודת השבת שלו 92B6.
en: But existence is not convergence. In the page's box:
en: base 15, and its fixed point 92B6.

he: ‏1234 בבסיס 15 לא מגיע אליה : הוא נכנס
he: למחזור של ארבעה, 30DC עד 9676.
en: 1234 in base 15 does not reach it: it enters
en: a cycle of four, 30DC to 9676.

he: אותן ספרות בבסיס 10 :
he: ‏1234, עם p = 3 ו-q = 1.
en: The same digits in base 10:
en: 1234, with p = 3 and q = 1.

he: שלושה צעדים, דרך 3087 ו-8352,
he: והוא נעצר ב-6174.
en: Three steps, through 3087 and 8352,
en: and it stops at 6174.

he: לסיכום : ההפרש תלוי רק ב-p וב-q,
he: ורק הזוג (6, 2) חוזר לעצמו : 6174.
en: In short: the difference depends only on p and q,
en: and only the pair (6, 2) returns to itself: 6174.

he: נסו מספרים ובסיסים משלכם בתיבות
he: שבעמוד של שאלה 0013 באתר.
en: Try your own numbers and bases in the boxes
en: on the page of question 0013 on the site.
