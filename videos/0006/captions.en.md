# 0006 — the best single trade of a stock: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0006 : רווח מקסימלי ממניה,
he: שאלה ברמת ג'וניור.
en: Question 0006: the maximum profit from a stock,
en: a junior-level question.

he: שני סעיפים : קודם רק לונג,
he: ואז גם שורט.
en: Two parts: first long trades only,
en: then short trades too.

he: נתון מערך prices : המחיר של המניה בכל יום.
he: מותר לבצע עסקה אחת.
en: An array prices holds the stock's price on each day.
en: One trade is allowed.

he: סעיף א : קונים ביום אחד,
he: ומוכרים ביום מאוחר יותר. עסקת לונג.
en: Part A: buy on one day,
en: sell on a later day. A long trade.

he: המחירים מהעמוד : 5, 8, 3, 9, 2, 6,
he: מחיר אחד לכל יום.
en: The page's prices: 5, 8, 3, 9, 2, 6,
en: one price per day.

he: קונים ביום i ומוכרים ביום j > i.
he: הרווח : prices[j] − prices[i].
en: Buy on day i, sell on day j > i.
en: The profit: prices[j] − prices[i].

he: הדרך הישירה בודקת כל זוג ימים :
he: כאן 15 זוגות, ובכלל זמן O(n²).
en: The direct way checks every pair of days:
en: 15 pairs here, O(n²) time in general.

he: הרעיון : אם מוכרים ביום j, הכי טוב לקנות
he: במחיר הנמוך ביותר עד אותו יום.
en: The idea: when selling on day j, the best buy
en: is at the lowest price up to that day.

he: לכן מספיק לזכור את המינימום עד כה,
he: ולעבור על המערך פעם אחת.
en: So it is enough to remember the minimum so far
en: and scan the array once.

he: כך זה נראה בתיבה שבעמוד, על אותם מחירים.
he: הקו הכחול הוא המינימום עד כה.
en: This is the page's box, on the same prices.
en: The blue line is the minimum so far.

he: יום 0 : המחיר 5. אין יום קודם,
he: ולכן 5 הוא המינימום.
en: Day 0: the price is 5. There is no earlier day,
en: so 5 is the minimum.

he: יום 1 : 8 − 5 = 3.
he: הלונג הטוב ביותר עד כה מרוויח 3.
en: Day 1: 8 − 5 = 3.
en: The best long so far earns 3.

he: יום 2 : 3 − 5 שלילי, אין רווח.
he: אבל 3 הוא המינימום החדש.
en: Day 2: 3 − 5 is negative, no profit.
en: But 3 is the new minimum.

he: יום 3 : 9 − 3 = 6. לונג חדש :
he: קנייה ביום 2 ומכירה ביום 3.
en: Day 3: 9 − 3 = 6. A new best long:
en: buy on day 2, sell on day 3.

he: יום 4 : 2 − 3 שלילי.
he: המינימום החדש הוא 2.
en: Day 4: 2 − 3 is negative.
en: The new minimum is 2.

he: יום 5 : 6 − 2 = 4, פחות מ-6.
he: התשובה : רווח 6, ימים 2 ו-3.
en: Day 5: 6 − 2 = 4, less than 6.
en: The answer: profit 6, days 2 and 3.

he: עכשיו נכתוב את זה ב-Python, שורה אחרי שורה.
en: Now let's write it in Python, line by line.

he: ‏max_long_fast מקבלת את רשימת המחירים,
he: ומחזירה רווח, יום קנייה ויום מכירה.
en: max_long_fast takes the list of prices and returns
en: the profit, the buy day and the sell day.

he: שורה 2 : עוד אין עסקה.
he: רווח 0, ובלי ימים.
en: Line 2: no trade yet.
en: Profit 0, and no days.

he: שורות 3–4 : רשימה ריקה מחזירה מיד
he: את התשובה "אין עסקה".
en: Lines 3–4: an empty list returns
en: "no trade" right away.

he: שורה 5 : המינימום עד כה מתחיל
he: במחיר של היום הראשון, יום 0.
en: Line 5: the minimum so far starts
en: at the first day's price, day 0.

he: שורה 6 : עוברים על הימים לפי הסדר.
he: ‏i הוא היום, ו-p המחיר שלו.
en: Line 6: go over the days in order.
en: i is the day, p its price.

he: שורות 7–8 : מוכרים היום, וקנינו במינימום.
he: רווח גדול יותר נשמר עם שני הימים.
en: Lines 7–8: sell today, bought at the minimum.
en: A larger profit is saved with both days.

he: שורות 9–10 : רק אחרי הבדיקה מעדכנים
he: את המינימום, כדי לא לקנות ולמכור באותו יום.
en: Lines 9–10: update the minimum only after the check,
en: so we never buy and sell on the same day.

he: שורה 11 : מחזירים את העסקה הטובה ביותר.
en: Line 11: return the best trade.

he: נריץ את הקוד על הדוגמה,
he: והתיבה מהעמוד מתקדמת יחד איתו.
en: Let's run the code on the example,
en: with the page's box stepping along.

he: שורות 2–5 : אין עסקה עדיין,
he: והמינימום הוא 5, מיום 0.
en: Lines 2–5: no trade yet,
en: and the minimum is 5, from day 0.

he: יום 0 : 5 − 5 = 0, לא יותר מ-0.
he: המינימום נשאר 5.
en: Day 0: 5 − 5 = 0, not more than 0.
en: The minimum stays 5.

he: יום 1 : 8 − 5 = 3. שורה 8 שומרת
he: רווח 3, קנייה ביום 0 ומכירה ביום 1.
en: Day 1: 8 − 5 = 3. Line 8 saves profit 3,
en: buy on day 0, sell on day 1.

he: יום 2 : 3 − 5 שלילי, ושורה 10
he: מעדכנת את המינימום ל-3, ביום 2.
en: Day 2: 3 − 5 is negative, and line 10
en: moves the minimum to 3, on day 2.

he: יום 3 : 9 − 3 = 6, יותר מ-3.
he: העסקה החדשה : ימים 2 ו-3.
en: Day 3: 9 − 3 = 6, more than 3.
en: The new trade: days 2 and 3.

he: יום 4 : 2 − 3 שלילי.
he: המינימום יורד ל-2, ביום 4.
en: Day 4: 2 − 3 is negative.
en: The minimum drops to 2, on day 4.

he: יום 5 : 6 − 2 = 4, פחות מ-6.
he: שום דבר לא משתנה.
en: Day 5: 6 − 2 = 4, less than 6.
en: Nothing changes.

he: הלולאה נגמרה. התשובה :
he: רווח 6, קנייה ביום 2 ומכירה ביום 3.
en: The loop is done. The answer:
en: profit 6, buy on day 2, sell on day 3.

he: למה זה נכון : לכל יום מכירה j, הקנייה
he: הטובה ביותר היא במינימום של הימים שלפניו.
en: Why it works: for each sell day j, the best buy
en: is at the minimum of the days before it.

he: הלולאה בודקת בדיוק את הערך הזה לכל יום,
he: ולכן המקסימום שלה הוא המקסימום על כל הזוגות.
en: The loop checks exactly that value for every day,
en: so its maximum is the maximum over all pairs.

he: המלכודת : לחשב את המחיר הגבוה ביותר
he: פחות הנמוך ביותר, בכל המערך.
en: The trap: the highest price minus
en: the lowest price of the whole array.

he: עבור 9, 1 ההפרש הוא 8, אבל הקנייה חייבת
he: לבוא לפני המכירה : אין לונג שמרוויח.
en: For 9, 1 the difference is 8, but the buy must come
en: before the sale: no long makes a profit.

he: הסיבוכיות : מעבר אחד, זמן O(n),
he: וזיכרון O(1), במקום O(n²) של כל הזוגות.
en: The cost: one pass, O(n) time, and O(1) memory,
en: instead of O(n²) for all pairs.

he: סעיף ב : הטוויסט. מותר גם שורט.
en: Part B: the twist. Short selling is allowed too.

he: שורט : מוכרים ביום i, וקונים בחזרה
he: ביום מאוחר יותר j.
en: A short: sell on day i,
en: buy it back on a later day j.

he: הרווח בשורט : prices[i] − prices[j].
he: מרוויחים כשהמחיר יורד.
en: The short's profit: prices[i] − prices[j].
en: It earns when the price falls.

he: בדוגמה, הלונג הטוב ביותר מרוויח 6,
he: והשורט הטוב ביותר מרוויח 7.
en: In the example, the best long earns 6,
en: and the best short earns 7.

he: לכן התשובה : שורט, רווח 7, ימים 3 ו-4.
en: So the answer: short, profit 7, days 3 and 4.

he: הרעיון : רווח השורט הוא מינוס רווח הלונג
he: באותם ימים.
en: The idea: a short's profit is minus
en: the long's profit on the same days.

he: לכן בשורט זוכרים את המקסימום עד כה,
he: ושני החישובים רצים באותה לולאה.
en: So for the short we remember the maximum so far,
en: and both run in the same loop.

he: בתיבה : הקו הכחול הוא המינימום עד כה,
he: והכתום הוא המקסימום עד כה.
en: In the box: the blue line is the minimum so far,
en: the orange one the maximum so far.

he: יום 0 : המינימום והמקסימום הם 5.
en: Day 0: the minimum and the maximum are 5.

he: יום 1 : לונג 8 − 5 = 3.
he: המקסימום עולה ל-8.
en: Day 1: long 8 − 5 = 3.
en: The maximum rises to 8.

he: יום 2 : שורט 8 − 3 = 5.
he: המינימום יורד ל-3.
en: Day 2: short 8 − 3 = 5.
en: The minimum drops to 3.

he: יום 3 : לונג 9 − 3 = 6.
he: המקסימום עולה ל-9.
en: Day 3: long 9 − 3 = 6.
en: The maximum rises to 9.

he: יום 4 : שורט 9 − 2 = 7.
he: המינימום יורד ל-2.
en: Day 4: short 9 − 2 = 7.
en: The minimum drops to 2.

he: יום 5 : לונג 4 ושורט 3, בלי שיפור.
he: השורט, 7, מנצח את הלונג, 6.
en: Day 5: long 4, short 3, no improvement.
en: The short, 7, beats the long, 6.

he: ב-Python זו אותה לולאה, עם שני מועמדים.
en: In Python it is the same loop, with two candidates.

he: ‏max_profit_fast מחזירה רווח, סוג העסקה,
he: ויום הפתיחה ויום הסגירה שלה.
en: max_profit_fast returns the profit, the trade's type,
en: and its opening and closing days.

he: שורות 2–3 : עסקה צריכה שני ימים.
he: עם פחות משני מחירים אין עסקה.
en: Lines 2–3: a trade needs two days.
en: With fewer than two prices there is none.

he: שורות 5–6 : המינימום והמקסימום עד כה,
he: שניהם מתחילים במחיר של יום 0.
en: Lines 5–6: the minimum and maximum so far,
en: both start at day 0's price.

he: שורות 8–9 : שני מועמדים, לונג ושורט,
he: כל אחד עם רווח 0 ובלי ימים.
en: Lines 8–9: two candidates, long and short,
en: each with profit 0 and no days.

he: שורה 11 : לולאה אחת על כל הימים.
en: Line 11: one loop over all the days.

he: שורות 12–14 : בדיקת הלונג, כמו בסעיף א,
he: מול המינימום של הימים הקודמים.
en: Lines 12–14: the long check, as in part A,
en: against the minimum of the earlier days.

he: שורות 16–18 : תמונת הראי בשביל השורט :
he: המקסימום עד כה פחות מחיר היום.
en: Lines 16–18: the mirror image for the short:
en: the maximum so far minus today's price.

he: שורות 20–23 : רק אחרי שתי הבדיקות
he: מעדכנים את המינימום ואת המקסימום.
en: Lines 20–23: only after both checks
en: are the minimum and maximum updated.

he: שורות 25–26 : אם השורט טוב יותר מהלונג,
he: מחזירים אותו.
en: Lines 25–26: if the short beats the long,
en: return it.

he: שורות 27–29 : אחרת את הלונג, אם הוא מרוויח.
he: ואם לא, אין עסקה.
en: Lines 27–29: otherwise the long, if it earns.
en: If not, there is no trade.

he: נריץ על הדוגמה, יום אחרי יום,
he: לצד התיבה מהעמוד.
en: Let's run it on the example, day by day,
en: beside the page's box.

he: שורות 2–9 : המינימום והמקסימום הם 5,
he: ושני המועמדים ברווח 0.
en: Lines 2–9: the minimum and maximum are 5,
en: and both candidates have profit 0.

he: יום 0 : אין רווח לאף כיוון.
en: Day 0: no profit either way.

he: יום 1 : לונג 8 − 5 = 3, ושורה 23
he: מעלה את המקסימום ל-8.
en: Day 1: long 8 − 5 = 3, and line 23
en: raises the maximum to 8.

he: יום 2 : שורט 8 − 3 = 5, ושורה 21
he: מורידה את המינימום ל-3.
en: Day 2: short 8 − 3 = 5, and line 21
en: lowers the minimum to 3.

he: יום 3 : לונג 9 − 3 = 6,
he: והמקסימום עולה ל-9.
en: Day 3: long 9 − 3 = 6,
en: and the maximum rises to 9.

he: יום 4 : שורט 9 − 2 = 7,
he: והמינימום יורד ל-2.
en: Day 4: short 9 − 2 = 7,
en: and the minimum drops to 2.

he: יום 5 : לונג 4 ושורט 3, בלי שיפור.
en: Day 5: long 4, short 3, no improvement.

he: הלולאה נגמרה : הלונג הטוב ביותר 6,
he: והשורט הטוב ביותר 7.
en: The loop is done: the best long is 6,
en: the best short 7.

he: שורה 25 : 7 גדול מ-6, ולכן מוחזר
he: שורט, רווח 7, ימים 3 ו-4.
en: Line 25: 7 is more than 6, so it returns
en: short, profit 7, days 3 and 4.

he: הסיבוכיות : עדיין מעבר אחד, זמן O(n),
he: וזיכרון נוסף קבוע, O(1).
en: The cost: still one pass, O(n) time,
en: and constant extra memory, O(1).

he: עבור מיליון ימים : כחמש מאות מיליארד זוגות,
he: מול מיליון צעדים בלבד.
en: For a million days: about 500 billion pairs,
en: against only a million steps.

he: מלכודת : תיקו בין לונג לשורט.
he: למשל 1, 4, 1 : לונג 3 ושורט 3.
en: A trap: a tie between long and short.
en: For 1, 4, 1: long 3 and short 3.

he: ההשוואה החדה בשורה 25 מחזירה את הלונג.
he: כל זוג עם הרווח המקסימלי הוא תשובה נכונה.
en: The strict comparison on line 25 returns the long.
en: Any pair with the maximum profit is correct.

he: לסיכום : המינימום עד כה נותן את הלונג,
he: והמקסימום עד כה נותן את השורט.
en: In short: the minimum so far gives the long,
en: and the maximum so far gives the short.

he: נסו מחירים משלכם בתיבה
he: שבעמוד של שאלה 0006 באתר.
en: Try your own prices in the box
en: on the page of question 0006.
