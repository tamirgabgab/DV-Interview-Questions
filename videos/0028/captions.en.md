# 0028 — a cake split in a geometric sequence: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); notes/VIDEOS.md.

he: שאלה 0028 : חלוקת עוגה בסדרה הנדסית,
he: שאלה ברמת ג'וניור.
en: Question 0028: a cake split in a geometric sequence,
en: a junior-level question.

he: שני סעיפים : הצבה מספרית,
he: ואז המקרה הכללי עם הוכחה.
en: Two parts: plugging in numbers,
en: then the general case with a proof.

he: כמו בשאלה 0027, אבל עכשיו השבר
he: גדל פי q, ולא בתוספת קבועה.
en: As in question 0027, but now the fraction
en: grows by a factor q, not by a fixed step.

he: עוגה בגודל 1. כל אחד בתורו חותך
he: שבר p_k ממה שנשאר, לא מהעוגה כולה.
en: A cake of size 1. Each person in turn cuts
en: a fraction p_k of what is left, not of the whole cake.

he: דוגמה עם a = 0.1 ו-q = 2 : השברים
he: ‏0.1, 0.2, 0.4, 0.8, והחמישי לוקח את השארית.
en: An example with a = 0.1 and q = 2: the fractions
en: 0.1, 0.2, 0.4, 0.8, and the fifth takes the rest.

he: השבר גדל, אבל מה שנשאר לחתוך ממנו
he: קטן. מי מקבל את החלק הגדול ביותר?
en: The fraction grows, but what is left
en: to cut from shrinks. Who gets the largest piece?

he: סעיף א : a = 0.01 ו-q = 1.5. השברים
he: ‏0.01, 0.015, 0.0225, כל אחד פי 1.5.
en: Part A: a = 0.01 and q = 1.5. The fractions
en: 0.01, 0.015, 0.0225, each 1.5 times the last.

he: למעלה העוגה, ולמטה גרף : החלק
he: שכל אחד מקבל, עמודה לכל אדם.
en: The cake on top, a chart below:
en: the share each person gets, a bar per person.

he: חמשת הראשונים לוקחים פרוסות דקות :
he: השבר קטן, והעוגה כמעט שלמה.
en: The first five cut thin slices:
en: the fraction is small and the cake is almost whole.

he: השבר ממשיך לגדול פי 1.5, והעמודות
he: עולות. עד האדם התשיעי כל אחד מקבל יותר.
en: The fraction keeps growing by 1.5 and the bars
en: rise. Up to the ninth, each one gets more.

he: האדם העשירי לוקח 0.3844 ממה שנשאר,
he: ומקבל 0.1697 : העמודה הגבוהה ביותר.
en: The tenth takes 0.3844 of what is left
en: and gets 0.1697: the tallest bar.

he: אחריו השבר גדול, אבל נשאר מעט.
he: העמודות יורדות, והאדם ה-13 לוקח את השארית.
en: After him the fraction is large, but little is left.
en: The bars fall, and the 13th takes the rest.

he: תשעת הראשונים לקחו יחד פחות מ-60%
he: מהעוגה, ומשם השבר קופץ מהר.
en: The first nine took less than 60% of the cake
en: together, and from there the fraction jumps fast.

he: מלכודת : לאחרון יש השבר הגדול ביותר,
he: כל השארית. אבל נשאר לו רק 0.0155.
en: TODO

he: סימון : R_k הוא מה שנשאר לפני האדם ה-k.
he: הוא לוקח p_k ממנו, והשאר עובר הלאה.
en: Notation: R_k is what is left before person k.
en: He takes p_k of it, and the rest passes on.

he: משווים שני שכנים : מה שנשאר מצטמצם,
he: ועם p_{k+1} = q·p_k מצטמצם גם השבר.
en: Compare two neighbours: what is left cancels,
en: and with p_{k+1} = q·p_k the fraction cancels too.

he: נשאר יחס פשוט מאוד : q כפול 1 − p_k.
he: הוא לא תלוי בכלל במה שנשאר.
en: A very simple ratio is left: q times 1 − p_k.
en: It does not depend on what is left at all.

he: האדם הבא מקבל יותר בדיוק כשהיחס
he: גדול מ-1, כלומר כשהשבר מתחת לשליש.
en: The next person gets more exactly when the ratio
en: is above 1, that is, when the fraction is below a third.

he: כאן כל עמודה היא השבר של אדם,
he: והקו המקווקו הוא הסף שליש.
en: Here each bar is one person's fraction,
en: and the dashed line is the threshold, one third.

he: תשעה שברים מתחת לסף : אחרי כל אחד
he: מהם בא מישהו שמקבל יותר.
en: Nine fractions are below the threshold: each of them
en: is followed by someone who gets more.

he: השבר העשירי הוא הראשון שעובר את הסף.
he: אחריו כל השברים מעליו.
en: The tenth fraction is the first above the threshold.
en: All the fractions after it are above it.

he: מי עובר את הסף? כופלים ב-q חלקי a,
he: כי 0.5 חלקי 0.01 הוא 50.
en: Who passes the threshold? Multiply by q over a,
en: since 0.5 over 0.01 is 50.

he: לוקחים לוגריתם בבסיס 1.5 ומעגלים
he: למעלה : האדם העשירי.
en: Take the logarithm in base 1.5 and round
en: up: the tenth person.

he: מלכודת : סף 1 במקום שליש מוצא את
he: האחרון, שלוקח את השארית : 13 במקום 10.
en: TODO

he: בדיקה ישירה : השבר התשיעי מתחת לסף,
he: והעשירי כבר מעליו.
en: A direct check: the ninth fraction is below
en: the threshold, and the tenth is already above it.

he: והחלק שלו : 0.3844 מתוך 0.4415
he: שנשארו, כלומר בערך 17% מהעוגה.
en: And his share: 0.3844 of the 0.4415 left,
en: that is, about 17% of the cake.

he: כך זה נראה בתיבה שבעמוד : העוגה
he: ועד עכשיו תשעה אנשים בטבלה.
en: This is the page's box: the cake,
en: and so far nine people in the table.

he: האדם הבא : העשירי חותך 0.3844
he: ממה שנשאר, ומקבל 0.1697.
en: The next person: the tenth cuts 0.3844
en: of what is left and gets 0.1697.

he: והאחד-עשר מקבל פחות, 0.1567.
he: הפסגה היא האדם העשירי.
en: And the eleventh gets less, 0.1567.
en: The peak is the tenth person.

he: וכולם : אחרי העשירי החלקים רק
he: יורדים, עד 0.0155 של האחרון.
en: TODO

he: סעיף ב : a ו-q כלשהם, עם 1 < q ≤ 2.
he: מי מקבל הכי הרבה, ולמה יש פסגה אחת?
en: Part B: any a and q, with 1 < q ≤ 2.
en: Who gets the most, and why is there one peak?

he: היחס בין שכנים, q(1 − p_k), לא תלוי
he: במספרים של סעיף א. כאן הוא בגרף, נקודה לכל k.
en: The neighbours' ratio, q(1 − p_k), does not depend on
en: Part A's numbers. Here it is as a dot per k.

he: השברים עולים, ולכן היחס רק יורד.
he: תשע נקודות מעל הקו : החלקים עולים.
en: The fractions grow, so the ratio only falls.
en: Nine dots above the line: the shares grow.

he: הנקודה של האדם העשירי היא הראשונה
he: מתחת לקו, וכל מה שאחריה נשאר מתחת.
en: The tenth person's dot is the first one
en: below the line, and all after it stay below.

he: לכן יש פסגה אחת : החלקים עולים
he: עד האדם הראשון שיורד לקו, ואחריו רק יורדים.
en: So there is one peak: the shares grow up to
en: the first person who drops to the line, then only fall.

he: הסף הוא הנקודה שבה היחס שווה ל-1 :
he: ‏T = 1 − 1/q. שליש עבור q = 1.5.
en: The threshold is where the ratio equals 1:
en: T = 1 − 1/q. One third for q = 1.5.

he: מי עובר את הסף : כופלים ב-q חלקי a
he: ולוקחים לוגריתם בבסיס q.
en: Who passes the threshold: multiply by q over a
en: and take the logarithm in base q.

he: והנוסחה : האדם הראשון שהשבר שלו
he: מגיע לסף. אם a כבר מעליו, זה הראשון.
en: And the formula: the first person whose fraction
en: reaches the threshold. If a is above it, the first.

he: והאחרון? השבר שלו נחתך ל-1, ולכן
he: היחס אליו הוא 1 − p חלקי p, ולא q(1 − p).
en: TODO

he: כש-q ≤ 2 הסף לכל היותר חצי. מתחת
he: לסף היחס הזה גדול מ-1, כמו שהתנאי אומר.
en: TODO

he: ומעל הסף החיתוך רק מקטין את היחס.
he: בשני המקרים התשובה לא משתנה.
en: TODO

he: עם a = 0.01 ו-q אחרים : q = 2 נותן
he: את האדם השביעי, עם 0.313 מהעוגה.
en: With a = 0.01 and other q: q = 2 gives
en: the seventh person, with 0.313 of the cake.

he: ככל ש-q קרוב ל-1, הפסגה מאוחרת יותר,
he: נמוכה ושטוחה : עם 1.1, האדם ה-25.
en: The closer q is to 1, the later the peak,
en: low and flat: with 1.1, the 25th person.

he: ומתי יש תיקו? כש-q^k שווה בדיוק
he: ל-(q − 1)/a. למשל a = 0.25 ו-q = 2.
en: When is there a tie? When q^k equals
en: (q − 1)/a exactly. For example a = 0.25 and q = 2.

he: השבר השני הוא בדיוק חצי, הסף.
he: השני והשלישי מקבלים 0.375 כל אחד.
en: The second fraction is exactly a half, the threshold.
en: The second and third get 0.375 each.

he: כאן הלוגריתם יוצא מספר שלם. מחשבון
he: שמחזיר 2.0000001 יעגל ל-3, ויפספס את התיקו.
en: TODO

he: לכן כשהלוגריתם קרוב לשלם, בודקים
he: ישירות את q^k מול (q − 1)/a.
en: TODO

he: בתיבה שבעמוד, בשלב ההוכחה, כל אדם
he: הוא נקודה על הקו q(1 − p), מול הקו y = 1.
en: In the page's box, at the proof step, each person
en: is a dot on the line q(1 − p), against y = 1.

he: ועם a = 0.25 ו-q = 2, הנקודה השנייה
he: נוגעת בקו בדיוק : תיקו עם השלישי.
en: And with a = 0.25 and q = 2, the second dot
en: touches the line exactly: a tie with the third.

he: כש-q גדול מ-2 האחרון יכול לשבור את
he: הנוסחה. שאלות ההמשך בעמוד מראות מתי.
en: When q is above 2 the last person can break
en: the formula. The page's follow-ups show when.

he: לסיכום : היחס בין שכנים הוא q(1 − p_k),
he: והפסגה אצל הראשון שעובר את 1 − 1/q.
en: To sum up: the neighbours' ratio is q(1 − p_k),
en: and the peak is at the first to pass 1 − 1/q.

he: נסו a ו-q משלכם בתיבה
he: שבעמוד של שאלה 0028 באתר.
en: Try your own a and q in the box
en: on the page of question 0028 on the site.
