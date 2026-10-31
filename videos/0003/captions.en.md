# 0003 — what does this code do: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0003 : מה עושה הקוד?
he: שאלה ברמת סטודנט.
en: Question 0003: what does this code do?
en: A student-level question.

he: סעיף אחד : לקרוא קוד קצר,
he: להריץ אותו על דוגמה, ולהסביר מה הוא עושה.
en: One part: read a short piece of code,
en: run it on an example, and explain what it does.

he: נתונה פונקציה קצרה שמקבלת רשימה
he: של מספרים. מה היא עושה לרשימה?
en: A short function takes a list of numbers.
en: What does it do to the list?

he: הנה הקוד של השאלה, ב-Python.
he: ננסה להבין מה הוא עושה.
en: Here is the question's code, in Python.
en: Let's work out what it does.

he: הפונקציה mystery מקבלת רשימה A
he: של מספרים שלמים, ומשנה אותה במקום.
en: The function mystery takes a list A
en: of integers and changes it in place.

he: קודם n, מספר האיברים ב-A.
en: First n, the number of elements in A.

he: הלולאה החיצונית : i עובר
he: על כל האינדקסים, מ-0 עד n − 1.
en: The outer loop: i runs over
en: every index, from 0 to n − 1.

he: הלולאה הפנימית : גם j עובר על כולם,
he: מ-0, ולא רק על אלה שאחרי i.
en: The inner loop: j also runs over all of them,
en: from 0, not only over those after i.

he: אם A[i] קטן מ-A[j],
he: מחליפים ביניהם.
en: If A[i] is less than A[j],
en: the two are swapped.

he: במבט ראשון זה נראה כמו מיון יורד :
he: איבר קטן ב-i מתחלף עם איבר גדול ממנו.
en: At first sight it looks like a descending sort:
en: a small element at i swaps with a larger one.

he: אבל לפני שעונים, מריצים דוגמה קטנה.
he: השאלה מבקשת מערך בגודל 4.
en: But before answering, run a small example.
en: The question asks for an array of size 4.

he: התיבה שבעמוד מריצה את הקוד
he: על המערך של העמוד : 3, 1, 4, 2.
en: The page's box runs the code
en: on the page's array: 3, 1, 4, 2.

he: השוואה 1 : i = 0 ו-j = 0.
he: האם 3 < 3? לא, אין החלפה.
en: Comparison 1: i = 0 and j = 0.
en: Is 3 < 3? No, no swap.

he: השוואה 2 : j = 1.
he: האם 3 < 1? לא.
en: Comparison 2: j = 1.
en: Is 3 < 1? No.

he: השוואה 3 : j = 2. האם 3 < 4? כן.
he: מחליפים, ו-A הוא 4, 1, 3, 2.
en: Comparison 3: j = 2. Is 3 < 4? Yes.
en: Swap, and A is 4, 1, 3, 2.

he: השוואה 4 : האם 4 < 2? לא.
he: בסוף i = 0, המקסימום 4 יושב ב-A[0].
en: Comparison 4: is 4 < 2? No.
en: At the end of i = 0, the maximum 4 sits in A[0].

he: הכפתור "עד סוף i" משלים את i = 1 :
he: החלפה אחת, ב-j = 0, של 1 עם 4.
en: The "until the end of i" button completes i = 1:
en: one swap, at j = 0, of 1 with 4.

he: סוף i = 2 : החלפה אחת, ב-j = 1.
he: ה-3 נכנס לפני ה-4 : 1, 3, 4, 2.
en: End of i = 2: one swap, at j = 1.
en: The 3 goes in before the 4: 1, 3, 4, 2.

he: סוף i = 3 : שתי החלפות, ב-j = 1 וב-j = 2.
he: המערך 1, 2, 3, 4.
en: End of i = 3: two swaps, at j = 1 and j = 2.
en: The array is 1, 2, 3, 4.

he: התשובה : הקוד ממיין בסדר עולה,
he: מהקטן לגדול. לא יורד!
en: The answer: the code sorts in ascending order,
en: smallest to largest. Not descending!

he: נחזור לקוד ונריץ אותו על הדוגמה,
he: לצד התיבה, ונעצור על כל החלפה.
en: Back to the code: run it on the example
en: beside the box, stopping at every swap.

he: בהתחלה n = 4,
he: ו-A הוא 3, 1, 4, 2.
en: At the start n = 4,
en: and A is 3, 1, 4, 2.

he: השוואה 1 : i = 0, j = 0.
he: ‏3 < 3 לא מתקיים.
en: Comparison 1: i = 0, j = 0.
en: 3 < 3 does not hold.

he: השוואה 2 : 3 < 1. לא.
en: Comparison 2: 3 < 1. No.

he: השוואה 3 : 3 < 4. כן,
he: וההחלפה מביאה את 4 ל-A[0].
en: Comparison 3: 3 < 4. Yes,
en: and the swap brings 4 to A[0].

he: השוואה 4 : 4 < 2. לא. הלולאה הפנימית
he: נגמרה, והמקסימום ב-A[0].
en: Comparison 4: 4 < 2. No. The inner loop
en: is over, and the maximum is in A[0].

he: ב-i = 1 כבר ההשוואה הראשונה מחליפה :
he: ‏1 < 4, וה-1 עובר להתחלה.
en: At i = 1 the very first comparison swaps:
en: 1 < 4, and the 1 moves to the front.

he: עכשיו A[1] הוא 4, המקסימום,
he: ולכן בשאר ה-j של i = 1 אין החלפות.
en: Now A[1] is 4, the maximum,
en: so the rest of the j's of i = 1 swap nothing.

he: ב-i = 2 : 3 < 1 לא, אבל 3 < 4 כן.
he: ה-3 נכנס לפני ה-4 : 1, 3, 4, 2.
en: At i = 2: 3 < 1 no, but 3 < 4 yes.
en: The 3 goes in before the 4: 1, 3, 4, 2.

he: ב-j = 2 וב-j = 3, A[2] הוא 4,
he: המקסימום, ואין החלפות.
en: At j = 2 and j = 3, A[2] is 4,
en: the maximum, and nothing swaps.

he: ב-i = 3 : 2 < 3, וה-2 מתחלף עם ה-3.
he: המערך 1, 2, 4, 3.
en: At i = 3: 2 < 3, and the 2 swaps with the 3.
en: The array is 1, 2, 4, 3.

he: ב-j = 2 : 3 < 4, עוד החלפה,
he: והמערך 1, 2, 3, 4.
en: At j = 2: 3 < 4, one more swap,
en: and the array is 1, 2, 3, 4.

he: ההשוואה האחרונה, 4 < 4, לא מתקיימת.
he: ‏16 השוואות, 5 החלפות, ומיון עולה.
en: The last comparison, 4 < 4, does not hold.
en: 16 comparisons, 5 swaps, an ascending sort.

he: למה זה עובד תמיד? נסתכל על המערך
he: בסוף כל איטרציה של i.
en: Why does it always work? Look at the array
en: at the end of every iteration of i.

he: הטענה : בסוף איטרציה i, החלק A[0..i]
he: ממוין, ו-A[i] הוא המקסימום של כל המערך.
en: The claim: at the end of iteration i, A[0..i]
en: is sorted, and A[i] is the maximum of the array.

he: שלב 1, i = 0 : כל איבר גדול יותר מתחלף
he: עם A[0], ולכן בסוף A[0] הוא המקסימום.
en: Step 1, i = 0: every larger element swaps
en: with A[0], so at the end A[0] is the maximum.

he: שלב 2, j < i : A[i] נכנס למקומו בחלק
he: הממוין, כמו ב-insertion sort.
en: Step 2, j < i: A[i] goes into its place
en: in the sorted part, as in insertion sort.

he: הגדולים ממנו זזים מקום אחד ימינה,
he: והמקסימום מגיע בדיוק ל-A[i].
en: The larger ones move one place to the right,
en: and the maximum lands exactly in A[i].

he: שלב 3, j ≥ i : A[i] הוא כבר המקסימום,
he: ולכן התנאי לא מתקיים ואין החלפות.
en: Step 3, j ≥ i: A[i] is already the maximum,
en: so the condition never holds and nothing swaps.

he: שלב 4 : אחרי i = n − 1, החלק הממוין
he: הוא כל המערך. מיון עולה.
en: Step 4: after i = n − 1, the sorted part
en: is the whole array. An ascending sort.

he: הסיבוכיות : תמיד n² השוואות, גם
he: כשהמערך כבר ממוין. זמן Θ(n²).
en: The cost: always n² comparisons, even
en: when the array is already sorted. Time Θ(n²).

he: אין יציאה מוקדמת, והמיון במקום :
he: זיכרון נוסף O(1).
en: No early exit, and the sort is in place:
en: O(1) extra memory.

he: על 4 איברים, 16 השוואות.
he: על 1,000 איברים, מיליון השוואות.
en: On 4 elements, 16 comparisons.
en: On 1,000 elements, a million comparisons.

he: המלכודת : לנחש את הכיוון מהתנאי.
he: הניחוש "יורד" נכון רק אם j מתחיל מ-i + 1.
en: The trap: guessing the direction from the condition.
en: "Descending" is right only if j starts at i + 1.

he: אז זה selection sort, והתוצאה 4, 3, 2, 1.
he: אותו תנאי, כיוון הפוך.
en: That is selection sort, and the result is 4, 3, 2, 1.
en: The same condition, the opposite direction.

he: שם כל i מביא ל-A[i] את המקסימום
he: של A[i..n − 1], ולכן הגדולים בהתחלה.
en: There each i brings the maximum of A[i..n − 1]
en: to A[i], so the large ones come first.

he: לסיכום : הקוד ממיין בסדר עולה,
he: תמיד ב-n² השוואות.
en: In short: the code sorts in ascending order,
en: always with n² comparisons.

he: נסו מערך משלכם בתיבה
he: שבעמוד של שאלה 0003 באתר.
en: Try an array of your own in the box
en: on the page of question 0003 on the site.
