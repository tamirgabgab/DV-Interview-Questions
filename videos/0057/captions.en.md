# 0057 — ants on a rod: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0057 : נמלים על מוט,
he: שאלה ברמת ג'וניור.
en: Question 0057: ants on a rod,
en: a junior-level question.

he: ארבעה סעיפים : מתי הכול נגמר, כמה התנגשויות,
he: מתי נופלת נמלה מסוימת, ומעגל.
en: Four parts: when it all ends, how many collisions,
en: when a given ant falls, and a ring.

he: על מוט באורך 100 ס"מ עומדות נמלים,
he: כל אחת בנקודה אחרת.
en: Ants stand on a rod 100 cm long,
en: each at a different point.

he: כל נמלה פונה ימינה או שמאלה,
he: והולכת סנטימטר אחד בשנייה.
en: Each ant faces left or right
en: and walks one centimetre a second.

he: כששתי נמלים נפגשות, שתיהן מסתובבות
he: מיד. נמלה שמגיעה לקצה נופלת.
en: When two ants meet, both turn around
en: at once. An ant that reaches an end falls.

he: זו הדוגמה מהעמוד : שש נמלים,
he: במקומות 10, 25, 40, 60, 75 ו-90.
en: The page's example: six ants,
en: at 10, 25, 40, 60, 75 and 90.

he: סעיף א : על המוט 100 נמלים, בכל סידור.
he: מה הזמן הארוך ביותר עד שכולן נופלות?
en: Part A: 100 ants on the rod, in any order.
en: What is the longest time until all have fallen?

he: שתי נמלים, A ו-B, הולכות זו לקראת זו.
he: למעלה הן מסתובבות במפגש, כמו בשאלה.
en: Two ants, A and B, walk toward each other.
en: On top they turn when they meet, as in the question.

he: למטה אותן שתיים, אבל כאן הן עוברות
he: זו דרך זו, כמו רוחות.
en: Below, the same two, but here they pass
en: through each other, like ghosts.

he: מריצים את שתיהן יחד.
he: הן נפגשות באמצע, ב-50.
en: We run both together.
en: They meet in the middle, at 50.

he: אחרי המפגש : למעלה A חוזרת שמאלה,
he: למטה A ממשיכה ימינה.
en: After the meeting: on top A goes back left,
en: below A carries on to the right.

he: אבל המקומות זהים לגמרי : נקודה אחת שמאלה
he: ונקודה אחת ימינה. רק הצבעים התחלפו.
en: But the places are exactly the same: one point left
en: and one point right. Only the colours swapped.

he: מי שלא רואה שמות לא יכול להבדיל.
he: זה כל הטריק : לחשוב על רוחות.
en: Without the names you cannot tell them apart.
en: That is the whole trick: think of ghosts.

he: עכשיו שש הנמלים מהעמוד. מתחת למוט,
he: כל נמלה מציירת קו : מקום מול זמן.
en: Now the page's six ants. Under the rod
en: each ant draws a line: place against time.

he: הזמן יורד למטה. בכל מפגש
he: הקווים של הנמלים נשברים.
en: Time runs downward. At every meeting
en: the ants' lines break.

he: ממשיכים עד שהמוט מתרוקן :
he: האחרונה נופלת אחרי 90 שניות.
en: We go on until the rod is empty:
en: the last ant falls after 90 seconds.

he: ועכשיו אותה ריצה עם רוחות,
he: שהולכות ישר ולא מסתובבות.
en: And now the same run with ghosts,
en: which walk straight and never turn.

he: כל רוח היא קו ישר. אלה בדיוק
he: אותם קווים, רק בצבעים אחרים.
en: Each ghost is a straight line. These are exactly
en: the same lines, only in other colours.

he: רוח שהולכת שמאלה מ-p יוצאת אחרי p שניות,
he: ורוח שהולכת ימינה אחרי 100 פחות p.
en: A ghost walking left from p leaves after p seconds,
en: one walking right after 100 minus p.

he: בדוגמה : הזמנים של שש הרוחות
he: הם 90, 25, 60, 60, 75 ו-10.
en: In the example the six ghosts' times
en: are 90, 25, 60, 60, 75 and 10.

he: המוט מתרוקן כשהרוח האחרונה יוצאת :
he: המקסימום, 90 שניות.
en: The rod is empty when the last ghost leaves:
en: the maximum, 90 seconds.

he: כל זמן הוא לכל היותר 100, ו-100 מתקבל
he: כשנמלה עומדת בקצה ופונה פנימה.
en: Every time is at most 100, and 100 happens
en: when an ant stands at an end facing inward.

he: וזה לא תלוי בכמה נמלים יש :
he: עם אחת או עם 100, התשובה 100 שניות.
en: And it does not depend on how many ants:
en: with one or with 100, the answer is 100 seconds.

he: עכשיו נכתוב את זה ב-Python.
en: Now let's write it in Python.

he: ‏last_fall מקבלת את המקומות והכיוונים :
he: ‏+1 ימינה, ‏-1 שמאלה.
en: last_fall takes the places and the directions:
en: +1 right, -1 left.

he: לכל נמלה, הזמן של הרוח שלה :
he: ‏p אם היא הולכת שמאלה, אחרת 100 פחות p.
en: For each ant, the time of its ghost:
en: p if it walks left, else 100 minus p.

he: ומחזירים את המקסימום. אין כאן
he: שום סימולציה של התנגשויות.
en: And we return the maximum. There is
en: no simulation of collisions at all.

he: נריץ על שש הנמלים מהעמוד.
en: Let's run it on the page's six ants.

he: הזמנים 90, 25, 60, 60, 75 ו-10,
he: והמקסימום 90.
en: The times are 90, 25, 60, 60, 75 and 10,
en: and the maximum is 90.

he: גם התיבה שבעמוד מציירת את הקווים :
he: מקום לרוחב, וזמן כלפי מטה.
en: The page's box draws the lines too:
en: place across, and time going down.

he: אחרי 25 שניות : ארבע התנגשויות
he: כבר קרו, ושתי נמלים נפלו.
en: After 25 seconds four collisions
en: have happened, and two ants have fallen.

he: כמעט בסוף, אחרי 89.5 שניות, נשארה
he: רק נמלה 4. הקווים שבורים בכל מפגש.
en: Almost at the end, at 89.5 seconds,
en: only ant 4 is left. The lines break at each meeting.

he: המתג "רוחות" מחליף לקווים ישרים :
he: אותם קווים בדיוק, רק הצבעים מתחלפים.
en: The "ghosts" switch turns them into straight lines:
en: the very same lines, only the colours swap.

he: הסיבוכיות : מעבר אחד על הנמלים,
he: זמן O(n) וזיכרון O(1).
en: The cost: one pass over the ants,
en: O(n) time and O(1) memory.

he: מלכודת : לסמלץ התנגשות אחרי התנגשות.
he: עם 100 נמלים יכולות להיות 2500.
en: Trap: simulating collision after collision.
en: With 100 ants there can be 2500 of them.

he: הרוחות חוסכות את כל זה : הזמן תלוי
he: רק במקום ובכיוון של כל נמלה לבד.
en: The ghosts spare all of that: the time depends
en: only on each ant's own place and direction.

he: סעיף ב : כמה התנגשויות יהיו בסידור נתון?
he: ומה המספר הגדול ביותר עם 100 נמלים?
en: Part B: how many collisions in a given arrangement?
en: And what is the most with 100 ants?

he: כל התנגשות היא נקודה שבה שני קווים
he: נחתכים. נסתכל על הקווים הישרים של הרוחות.
en: Every collision is a point where two lines
en: cross. Let's look at the ghosts' straight lines.

he: בדוגמה יש חמישה חיתוכים, ולכן
he: חמש התנגשויות של נמלים.
en: The example has five crossings,
en: so five collisions of ants.

he: שני קווים ישרים נחתכים רק אם
he: הם הולכים זה לקראת זה.
en: Two straight lines cross only
en: if they head toward each other.

he: זוג נפגש אם השמאלית הולכת ימינה
he: והימנית שמאלה. זוגות אחרים אף פעם.
en: A pair meets if the left one goes right
en: and the right one goes left. Other pairs never meet.

he: והם תמיד נפגשים בזמן, באמצע הדרך,
he: לפני שאחת מהן יוצאת מהמוט.
en: And they always meet in time, halfway,
en: before either of them leaves the rod.

he: סופרים : לכל נמלה שהולכת שמאלה,
he: כמה הולכות ימינה ונמצאות משמאלה.
en: We count: for each ant going left,
en: how many going right are on its left.

he: ‏25 פוגשת את 10. ‏60 ו-75 פוגשות
he: כל אחת את 10 ואת 40.
en: 25 meets 10. 60 and 75
en: each meet 10 and 40.

he: סך הכול 1 ועוד 2 ועוד 2 :
he: חמש התנגשויות.
en: In all 1 plus 2 plus 2:
en: five collisions.

he: עם k נמלים שהולכות ימינה,
he: יש לכל היותר k כפול n פחות k זוגות.
en: With k ants going right,
en: there are at most k times n minus k pairs.

he: והמקסימום כשכל ההולכות ימינה
he: משמאל לכל ההולכות שמאלה.
en: And the most is when all those going right
en: are left of all those going left.

he: ‏k(n − k) הכי גדול ב-k = n/2 :
he: עם 100 נמלים, 50 כפול 50, ‏2500.
en: k(n − k) is largest at k = n/2:
en: with 100 ants, 50 times 50, 2500.

he: עכשיו נכתוב את זה ב-Python.
en: Now let's write it in Python.

he: ‏collisions מקבלת את המקומות והכיוונים,
he: ומחזירה את מספר ההתנגשויות.
en: collisions takes the places and the directions
en: and returns the number of collisions.

he: שני מונים : count להתנגשויות,
he: ו-right לנמלים שהולכות ימינה שעברנו.
en: Two counters: count for the collisions,
en: and right for the right-goers passed so far.

he: עוברים על הנמלים משמאל לימין,
he: אחרי מיון לפי המקום.
en: We go over the ants from left to right,
en: after sorting them by place.

he: נמלה שהולכת ימינה : מוסיפים אחת
he: ל-right. היא תפגוש את מי שמימינה.
en: An ant going right: add one
en: to right. It will meet those on its right.

he: נמלה שהולכת שמאלה פוגשת את כל
he: ההולכות ימינה שמשמאלה : מוסיפים right.
en: An ant going left meets every right-goer
en: on its left: add right.

he: בסוף מחזירים את count.
en: At the end we return count.

he: נריץ על שש הנמלים מהעמוד.
he: שני המונים מתחילים ב-0.
en: Let's run it on the page's six ants.
en: Both counters start at 0.

he: ‏10 הולכת ימינה : right = 1.
en: 10 goes right: right = 1.

he: ‏25 הולכת שמאלה, ופוגשת את 10 :
he: ‏count = 1.
en: 25 goes left and meets 10:
en: count = 1.

he: ‏40 הולכת ימינה : right = 2.
en: 40 goes right: right = 2.

he: ‏60 הולכת שמאלה, ופוגשת את 10 ואת 40 :
he: ‏count = 3.
en: 60 goes left and meets 10 and 40:
en: count = 3.

he: ‏75 גם הולכת שמאלה, ופוגשת את שתיהן :
he: ‏count = 5.
en: 75 also goes left and meets both:
en: count = 5.

he: ‏90 הולכת ימינה, ואין אף אחת מימינה
he: שתפגוש אותה : right = 3.
en: 90 goes right, and there is no one on its right
en: to meet it: right = 3.

he: הלולאה נגמרה : הפונקציה מחזירה 5.
en: The loop is over: the function returns 5.

he: הסיבוכיות : המיון עולה O(n log n),
he: והמעבר עצמו O(n). זיכרון O(n) לרשימה.
en: The cost: the sort is O(n log n),
en: the pass itself O(n). O(n) memory for the list.

he: מלכודת : לספור כל זוג שהולך בכיוונים
he: שונים. כאן 25 שמאלה ו-40 ימינה.
en: Trap: counting every pair with opposite
en: directions. Here 25 goes left and 40 right.

he: הן מתרחקות זו מזו, ולא נפגשות אף פעם.
he: סופרים רק זוגות שפונים זה לזה.
en: They move apart and never meet.
en: Count only pairs that face each other.

he: סעיף ג : מתי, ומאיזה צד, נופלת
he: הנמלה ה-k משמאל? ואיזו נופלת אחרונה?
en: Part C: when, and from which side, does
en: the k-th ant from the left fall? Which falls last?

he: הרעיון הראשון : נמלים לא עוברות זו את זו.
he: הן רק נפגשות ומסתובבות.
en: The first idea: ants never pass each other.
en: They only meet and turn.

he: לכן הסדר לאורך המוט לא משתנה :
he: נמלה 1 תמיד הכי שמאלית.
en: So the order along the rod never changes:
en: ant 1 is always the leftmost.

he: הנמלה שנופלת משמאל היא תמיד
he: השמאלית ביותר שעוד על המוט.
en: The ant that falls on the left is always
en: the leftmost one still on the rod.

he: הרעיון השני : כל רוח שיוצאת משמאל
he: מפילה נמלה משמאל. שלוש רוחות הולכות שמאלה.
en: The second idea: every ghost leaving on the left
en: drops an ant on the left. Three ghosts go left.

he: לכן נמלים 1, 2 ו-3 נופלות שמאלה,
he: אחרי 25, 60 ו-75 שניות, לפי הסדר.
en: So ants 1, 2 and 3 fall on the left,
en: after 25, 60 and 75 seconds, in order.

he: הרוחות שהולכות ימינה יוצאות
he: אחרי 90, 60 ו-10 שניות.
en: The ghosts going right leave
en: after 90, 60 and 10 seconds.

he: מימין הנמלה הימנית ביותר נופלת ראשונה :
he: נמלה 6 ב-10, נמלה 5 ב-60, ונמלה 4 ב-90.
en: On the right the rightmost ant falls first:
en: ant 6 at 10, ant 5 at 60, ant 4 at 90.

he: הטבלה : לכל נמלה, מאיזה צד
he: היא נופלת ומתי.
en: The table: for each ant, which side
en: it falls from, and when.

he: נמלה 4 התחילה ב-60 והלכה שמאלה,
he: אבל היא נופלת מימין, אחרונה, ב-90.
en: Ant 4 started at 60 walking left,
en: yet it falls on the right, last, at 90.

he: עכשיו נכתוב את זה ב-Python.
en: Now let's write it in Python.

he: ‏fall_times מחזירה את זמן הנפילה
he: של כל נמלה, לפי הסדר משמאל.
en: fall_times returns when each ant falls,
en: in their order from the left.

he: הזמנים של הרוחות שיוצאות משמאל :
he: ‏p של ההולכות שמאלה, מהקטן לגדול.
en: The times of the ghosts leaving on the left:
en: p of the left-goers, smallest first.

he: הזמנים של הרוחות שיוצאות מימין :
he: ‏100 פחות p של ההולכות ימינה.
en: The times of the ghosts leaving on the right:
en: 100 minus p of the right-goers.

he: השמאליות קודם, ואחריהן הימניות
he: בסדר הפוך : הימנית ביותר נופלת ראשונה.
en: The left ones first, then the right ones
en: reversed: the rightmost ant falls first.

he: נריץ על הדוגמה : משמאל יוצאות
he: הרוחות של 25, 60 ו-75.
en: On the example: on the left leave
en: the ghosts of 25, 60 and 75.

he: מימין : ‏100 פחות 10, 40 ו-90,
he: ממוינים : 10, 60 ו-90.
en: On the right: 100 minus 10, 40 and 90,
en: sorted: 10, 60 and 90.

he: והתוצאה : 25, 60, 75, ואז 90, 60 ו-10.
he: המקסימום של נמלה 4, ‏90.
en: The result: 25, 60, 75, then 90, 60 and 10.
en: The maximum is ant 4's, 90.

he: בתיבה שבעמוד : המוט, ומתחתיו
he: מתי נופלת כל נמלה.
en: In the page's box: the rod, and under it
en: when each ant falls.

he: אחרי 10 שניות נמלה 6 נופלת מימין,
he: הראשונה.
en: After 10 seconds ant 6 falls on the right,
en: the first one.

he: אחרי 25 שניות נמלה 1 נופלת משמאל.
en: After 25 seconds ant 1 falls on the left.

he: אחרי 60 שניות שתיים נופלות יחד :
he: נמלה 2 משמאל, ונמלה 5 מימין.
en: After 60 seconds two fall together:
en: ant 2 on the left and ant 5 on the right.

he: ב-75 נמלה 3 נופלת משמאל. נשארה רק
he: נמלה 4, והיא תיפול מימין ב-90.
en: At 75 ant 3 falls on the left. Only
en: ant 4 is left; it will fall on the right at 90.

he: הסיבוכיות : שני מיונים, O(n log n),
he: ושתי רשימות של זמנים, O(n).
en: The cost: two sorts, O(n log n),
en: and two lists of times, O(n).

he: מלכודת : "הנמלה נופלת מהצד שאליו
he: היא פונה". נמלה 4 פונה שמאלה.
en: Trap: "an ant falls on the side
en: it faces". Ant 4 faces left.

he: אבל היא נופלת מימין. מה שהולך ישר
he: הוא הרוח, לא הנמלה.
en: But it falls on the right. What walks straight
en: is the ghost, not the ant.

he: סעיף ד, בקצרה : המוט מתעקם למעגל,
he: בלי קצוות, ואף נמלה לא נופלת.
en: Part D, briefly: the rod bends into a ring,
en: with no ends, and no ant falls.

he: אותן שש נמלים, אבל ארבע הולכות
he: עם כיוון השעון, ורק 60 ו-75 נגדו.
en: The same six ants, but four walk
en: clockwise, and only 60 and 75 against it.

he: כל רוח משלימה סיבוב ב-100 שניות :
he: קבוצת המקומות והכיוונים חוזרת.
en: Each ghost completes a lap in 100 seconds:
en: the set of places and directions returns.

he: אבל הסדר המעגלי מסתובב : כל נמלה
he: זזה s = R − L מקומות, כאן 2.
en: But the circular order turns: each ant
en: moves s = R − L places, here 2.

he: אחרי 100 שניות : נמלה 0 עומדת
he: במקום של נמלה 2, וכך כולן.
en: After 100 seconds: ant 0 stands
en: where ant 2 started, and so for all.

he: אחרי 200 שניות : עוד שני מקומות.
en: After 200 seconds: two more places.

he: אחרי 300 שניות כולן בבית,
he: באותו מקום ובאותו כיוון.
en: After 300 seconds all are home,
en: in the same place and the same direction.

he: בכלל : n חלקי gcd של n ו-s סיבובים.
he: כאן 6 חלקי 2, שלושה סיבובים : ‏300 שניות.
en: In general: n over gcd(n, s) laps.
en: Here 6 over 2, three laps: 300 seconds.

he: לסיכום : רוחות שעוברות זו דרך זו
he: פותרות את כל ארבעת הסעיפים.
en: To sum up: ghosts that pass through each other
en: solve all four parts.

he: נסו סידורים משלכם בתיבה
he: שבעמוד של שאלה 0057 באתר.
en: Try your own arrangements in the box
en: on the page of question 0057 on the site.
