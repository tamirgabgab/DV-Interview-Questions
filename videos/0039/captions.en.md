# 0039 — eggs and floors: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); notes/VIDEOS.md.

he: שאלה 0039 : ביצים וקומות,
he: שאלה ברמת ג'וניור.
en: Question 0039: eggs and floors,
en: a junior-level question.

he: שני סעיפים : שלוש ביצים ומאה קומות,
he: ואז k ביצים ו-n קומות, עם קוד.
en: Two parts: three eggs and a hundred floors,
en: then k eggs and n floors, with code.

he: בניין של 100 קומות, ושלוש ביצים זהות.
he: בבניין יש קומת סף.
en: A building of 100 floors, and three identical eggs.
en: The building has a threshold floor.

he: ביצה שמטילים מעל הסף נשברת,
he: ומהסף ומתחתיו היא לא נשברת.
en: An egg dropped above the threshold breaks,
en: and from the threshold or below it does not.

he: הסף יכול להיות כל מספר מ-0 עד 100.
he: צריך למצוא אותו במקרה הגרוע.
en: The threshold can be any number from 0 to 100.
en: We must find it in the worst case.

he: סעיף א : כמה הטלות צריך במקרה הגרוע,
he: ומאילו קומות מטילים?
en: Part A: how many drops in the worst case,
en: and from which floors do we drop?

he: עם ביצה אחת אין ברירה :
he: מטילים מקומה 1, ‏2, ‏3, וכן הלאה.
en: With one egg there is no choice:
en: drop from floor 1, 2, 3, and so on.

he: אם היא נשברת באמצע, אין ביצה נוספת.
he: לכן במקרה הגרוע : ‏100 הטלות.
en: If it breaks midway, there is no other egg.
en: So in the worst case: 100 drops.

he: עם שתי ביצים, הראשונה קופצת,
he: והשנייה עוברת קומה אחר קומה מתחתיה.
en: With two eggs, the first one jumps,
en: and the second goes floor by floor below it.

he: הקפיצות קטנות באחת : ‏14, ‏27, ‏39.
he: כל קפיצה עולה הטלה לביצה הראשונה.
en: The jumps shrink by one: 14, 27, 39.
en: Every jump costs the first egg a drop.

he: אם הראשונה נשברת ב-27, השנייה בודקת
he: את 15 עד 26 : ‏2 + 12 = 14 הטלות.
en: If the first breaks at 27, the second checks
en: 15 to 26: 2 + 12 = 14 drops.

he: בכל מקום שהראשונה נשברת יוצא 14.
he: זה המקרה הגרוע עם שתי ביצים.
en: Wherever the first one breaks, it comes to 14.
en: That is the worst case with two eggs.

he: הרעיון : להפוך את השאלה. כמה קומות
he: אפשר לסדר עם k ביצים ו-t הטלות?
en: The idea: turn the question around. How many floors
en: can k eggs and t drops settle?

he: מטילים מקומה אחת. אם נשברה, הסף מתחת,
he: ונשארו ביצה אחת פחות והטלה אחת פחות.
en: Drop from one floor. If it broke, the threshold is below,
en: with one egg fewer and one drop fewer.

he: אם לא נשברה, הסף מעל : אותן ביצים,
he: והטלה אחת פחות.
en: If it did not break, the threshold is above:
en: the same eggs, and one drop fewer.

he: ועוד הקומה עצמה. זו נוסחת הנסיגה,
he: עם אפס כשאין ביצים או אין הטלות.
en: Plus the floor itself. That is the recurrence,
en: with zero when there are no eggs or no drops.

he: ממלאים טבלה : ביצה אחת מסדרת t קומות,
he: ושתיים t(t + 1)/2.
en: Fill a table: one egg settles t floors,
en: and two settle t(t + 1)/2.

he: עמודת שלוש הביצים : כל תא הוא
he: התא שמשמאל למעלה, ועוד 1, ועוד התא שמעליו.
en: The three-egg column: every cell is
en: the cell up-left, plus 1, plus the cell above.

he: למשל ‏129 = 36 + 1 + 92.
he: עם 8 הטלות רק 92 קומות, פחות מ-100.
en: For example 129 = 36 + 1 + 92.
en: With 8 drops only 92 floors, fewer than 100.

he: ועם 9 הטלות כבר 129 קומות.
he: לכן התשובה היא 9 הטלות.
en: And with 9 drops already 129 floors.
en: So the answer is 9 drops.

he: ההטלה הראשונה : אם נשברה, נשארו שתי ביצים
he: ו-8 הטלות, ל-36 קומות. לכן מקומה 37.
en: The first drop: if it broke, two eggs
en: and 8 drops are left for 36 floors. So from floor 37.

he: אם לא נשברה, הקפיצה הבאה קטנה :
he: לקומה 66, אחר כך 88, ואז 100.
en: If it did not break, the next jump is smaller:
en: to floor 66, then 88, then 100.

he: נריץ את התוכנית על הדוגמה שבעמוד,
he: כשהסף הוא קומה 36.
en: Let us run the plan on the page's example,
en: with the threshold at floor 36.

he: ‏37 גבוהה מהסף : הביצה נשברת.
he: נשארו שתי ביצים ושמונה הטלות ל-1 עד 36.
en: 37 is above the threshold: the egg breaks.
en: Two eggs and eight drops are left for 1 to 36.

he: השנייה בקפיצות יורדות : ‏8, ‏15, ‏21, ‏26,
he: ‏30, ‏33, ‏35. אף אחת לא נשברת.
en: The second in shrinking jumps: 8, 15, 21, 26,
en: 30, 33, 35. None of them breaks.

he: ההטלה התשיעית, מקומה 36, לא נשברת.
he: ‏36 בטוחה ו-37 שוברת : הסף 36.
en: The ninth drop, from floor 36, does not break.
en: 36 is safe and 37 breaks: the threshold is 36.

he: התיבה שבעמוד מריצה את אותה דוגמה,
he: הטלה אחרי הטלה.
en: The page's box runs the same example,
en: drop after drop.

he: הטלה 1 מקומה 37 : נשברה.
he: החלק שמעל 36 ידוע כשובר.
en: Drop 1 from floor 37: broke.
en: The part above 36 is known to break.

he: הטלה 2 מקומה 8 : לא נשברה.
he: הטווח הלא ידוע הוא 9 עד 36.
en: Drop 2 from floor 8: did not break.
en: The unknown range is 9 to 36.

he: וכך 15, ‏21 ו-26 : הטווח הלא ידוע
he: קטן בכל הטלה, מלמטה.
en: Then 15, 21 and 26: the unknown range
en: shrinks with every drop, from below.

he: ואחריהן 30, ‏33 ו-35.
he: אף אחת לא נשברת.
en: And after them 30, 33 and 35.
en: None of them breaks.

he: ובהטלה התשיעית, מקומה 36 : הסף הוא 36.
he: תשע הטלות, כמו בחישוב.
en: And in the ninth drop, from floor 36: the threshold is 36.
en: Nine drops, as computed.

he: ולמה לא 8? שמונה הטלות ושלוש ביצים
he: מבדילות בין 93 ספים לכל היותר.
en: And why not 8? Eight drops and three eggs
en: tell apart at most 93 thresholds.

he: ויש 101 ספים אפשריים, מ-0 עד 100.
he: ההוכחה המלאה בסעיף ב.
en: And there are 101 possible thresholds, from 0 to 100.
en: The full proof is in part B.

he: מספר ההטלות גדל כמו שורש שלישי של 6n :
he: ‏19 ל-1,000 קומות, ו-40 ל-10,000.
en: The number of drops grows like the cube root of 6n:
en: 19 for 1,000 floors, and 40 for 10,000.

he: מלכודת : חיפוש בינארי. מקומה 50,
he: והביצה נשברת.
en: A trap: binary search. From floor 50,
en: and the egg breaks.

he: נשארו שתי ביצים ל-49 קומות, שדורשות
he: ‏10 הטלות. בסך הכול 11, ולא 9.
en: Two eggs are left for 49 floors, which need
en: 10 drops. 11 in all, not 9.

he: סעיף ב : כל מספר ביצים וכל מספר קומות.
he: נוסחה, הוכחה וקוד.
en: Part B: any number of eggs and any number of floors.
en: A formula, a proof and code.

he: לנוסחת הנסיגה יש פתרון סגור :
he: סכום של מקדמים בינומיים.
en: The recurrence has a closed form:
en: a sum of binomial coefficients.

he: ההוכחה באינדוקציה, עם הזהות של פסקל.
he: לשלוש ביצים ו-9 הטלות : ‏129.
en: The proof is by induction, with Pascal's rule.
en: For three eggs and 9 drops: 129.

he: כל תוכנית היא עץ החלטות : בכל צומת
he: הטלה, שמאלה נשברה וימינה לא נשברה.
en: Every plan is a decision tree: at each node
en: a drop, left if it broke and right if not.

he: בכל מסלול לכל היותר k שבירות.
he: עם שתי ביצים ושלוש הטלות, 000 אסור.
en: Every path has at most k breaks.
en: With two eggs and three drops, 000 is impossible.

he: לכן לכל היותר 7 עלים, ו-7 ספים :
he: בדיוק 6 קומות, ‏f(2, 3).
en: So at most 7 leaves, and 7 thresholds:
en: exactly 6 floors, f(2, 3).

he: בכלל : עלה לכל סף, ולכן צריך
he: ‏f(k, t) ≥ n. התנאי שהקוד מחפש.
en: In general: a leaf per threshold, so we need
en: f(k, t) ≥ n. The condition the code looks for.

he: עם שלוש ביצים ו-8 הטלות : ‏93 עלים,
he: ויש 101 ספים. לכן 8 לא מספיקות.
en: With three eggs and 8 drops: 93 leaves,
en: and there are 101 thresholds. So 8 is not enough.

he: עכשיו נכתוב את זה ב-Python.
en: Now let us write it in Python.

he: ‏egg_table בונה את הטבלה F : כמה קומות
he: מסדרות e ביצים ב-t הטלות.
en: egg_table builds the table F: how many floors
en: e eggs settle in t drops.

he: בהתחלה הכול אפס : בלי ביצים
he: או בלי הטלות לא מסדרים אף קומה.
en: At first everything is zero: with no eggs
en: or no drops no floor is settled.

he: לכל e ולכל t, נוסחת הנסיגה מסעיף א,
he: עם תקרה n : מעל n הערך לא משנה.
en: For every e and every t, the recurrence of part A,
en: capped at n: above n the value changes nothing.

he: ומחזירה את הטבלה.
en: And returns the table.

he: ‏min_drops : ה-t הראשון
he: שבו הטבלה מכסה את כל n הקומות.
en: min_drops: the first t
en: at which the table covers all n floors.

he: ‏egg_run מריצה את התוכנית מול סף נתון,
he: ומחזירה את ההטלות.
en: egg_run runs the plan against a given threshold,
en: and returns the drops.

he: ‏low : הקומה הבטוחה הידועה. ‏high :
he: הקומה השוברת הידועה. ועוד eggs ו-t.
en: low: the highest floor known to be safe. high:
en: the lowest floor known to break. Plus eggs and t.

he: כל עוד יש קומה לא ידועה
he: בין low ל-high, מטילים.
en: As long as some floor between low and high
en: is unknown, we drop.

he: הקומה הבאה : מעל low בדיוק מה
he: שהביצים שיישארו מסדרות, ועוד אחת.
en: The next floor: above low by exactly what
en: the eggs left can settle, plus one.

he: מעל הסף הביצה נשברת.
he: רושמים את ההטלה ואת התוצאה.
en: Above the threshold the egg breaks.
en: We record the drop and its result.

he: בכל מקרה נשארת הטלה אחת פחות.
en: Either way one drop fewer is left.

he: נשברה : high יורד לקומה, וביצה פחות.
he: לא נשברה : low עולה לקומה.
en: Broke: high comes down to the floor, and one egg fewer.
en: Not broken: low goes up to the floor.

he: כש-high = low + 1 אין קומה לא ידועה,
he: ומחזירים את ההטלות.
en: When high = low + 1 no floor is unknown,
en: and we return the drops.

he: נריץ על הדוגמה שבעמוד : שלוש ביצים,
he: ‏100 קומות, והסף 36.
en: Let us run it on the page's example: three eggs,
en: 100 floors, and the threshold 36.

he: ההטלה הראשונה מקומה 37, מעל הסף :
he: נשברה. ‏high = 37, ונשארו שתי ביצים.
en: The first drop, from floor 37, is above the threshold:
en: it broke. high = 37, and two eggs are left.

he: השנייה : ‏0 + F[1][7] + 1 = 8.
he: לא נשברה, ולכן low = 8.
en: The second: 0 + F[1][7] + 1 = 8.
en: It did not break, so low = 8.

he: וכך שש הטלות שלא נשברות :
he: ‏15, ‏21, ‏26, ‏30, ‏33 ו-35.
en: Then six drops that do not break:
en: 15, 21, 26, 30, 33 and 35.

he: התשיעית מקומה 36 : לא נשברה.
he: ‏low = 36, ו-high = 37.
en: The ninth from floor 36: did not break.
en: low = 36, and high = 37.

he: אין יותר קומה לא ידועה : הסף 36,
he: אחרי תשע הטלות, כמו בסעיף א.
en: No floor is unknown any more: the threshold is 36,
en: after nine drops, as in part A.

he: התיבה מריצה את התוכנית מול כל סף,
he: מ-0 עד 100, וסופרת את ההטלות.
en: The box runs the plan against every threshold,
en: from 0 to 100, and counts the drops.

he: אף סף לא עובר 9, ו-46 ספים
he: מגיעים בדיוק ל-9 : זה המקרה הגרוע.
en: No threshold goes past 9, and 46 thresholds
en: reach exactly 9: that is the worst case.

he: הסיבוכיות : הטבלה O(kn), ריצה אחת O(t),
he: והבדיקה מול כל הספים O(nt).
en: The cost: the table O(kn), one run O(t),
en: and the check against every threshold O(nt).

he: מלכודת : לספור 100 ספים. הסף יכול
he: להיות גם 0 וגם 100 : יש n + 1 ספים.
en: A trap: counting 100 thresholds. The threshold can
en: also be 0 or 100: there are n + 1 thresholds.

he: מי שסופר n מקבל חסם תחתון
he: שטועה באחת.
en: Whoever counts n gets a lower bound
en: that is off by one.

he: לסיכום : במקום כמה הטלות, כמה קומות
he: מסדרות t הטלות.
en: To sum up: instead of how many drops, how many floors
en: t drops settle.

he: נסו מספרים משלכם בתיבה
he: שבעמוד של שאלה 0039 באתר.
en: Try your own numbers in the box
en: on the page of question 0039 on the site.
