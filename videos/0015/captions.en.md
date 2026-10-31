# 0015 — two children, at least one a boy: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0015 : שני ילדים, ולפחות אחד בן.
he: שאלה ברמת סטודנט.
en: Question 0015: two children, at least one a boy.
en: A student-level question.

he: שלושה סעיפים, וכולם הוכחה צעד אחרי
he: צעד : אין כאן קוד, רק ספירה.
en: Three parts, each a proof step by step:
en: no code here, only counting.

he: ליוסי יש שני ילדים. שאלנו אותו : האם
he: לפחות אחד מהם בן? והוא ענה כן.
en: Yossi has two children. We asked him: is at least
en: one of them a boy? He said yes.

he: מה ההסתברות ששני הילדים בנים?
en: What is the probability that both children are boys?

he: ההנחות : כל ילד בן או בת בחצי, וכל
he: יום בשבוע שווה הסתברות, בלי תלות.
en: The assumptions: each child is a boy or a girl with 1/2,
en: and every weekday is equally likely, all independent.

he: מה ההסתברות ששני הילדים בנים?
he: התשובה המהירה היא חצי. האם היא נכונה?
en: What is the probability that both are boys?
en: The quick answer is a half. Is it right?

he: הניחוש : יש בן אחד, והילד השני הוא
he: בן או בת בחצי. אז חצי?
en: The guess: there is one boy, and the other child
en: is a boy or a girl with 1/2. So a half?

he: מסדרים את הילדים לפי סדר הלידה :
he: ארבע משפחות, כל אחת בהסתברות 1/4.
en: Order the children by birth:
en: four families, each with probability 1/4.

he: בן ובת, ובת ובן, הן שתי משפחות
he: שונות, ולא תוצאה אחת.
en: Boy-girl and girl-boy are two different families,
en: not one outcome.

he: התשובה כן פוסלת רק משפחה אחת :
he: שתי בנות.
en: The answer yes rules out one family only:
en: two girls.

he: נשארות שלוש משפחות שוות הסתברות,
he: בהסתברות כוללת של 3/4.
en: Three equally likely families remain,
en: with total probability 3/4.

he: רק באחת מהן שני בנים :
he: בן ובן, בהסתברות 1/4.
en: Only one of them has two boys:
en: boy-boy, with probability 1/4.

he: נסמן : A הוא שני הילדים בנים,
he: ו-B הוא לפחות אחד בן.
en: Let A be both children boys,
en: and B at least one boy.

he: כל משפחה עם שני בנים מקיימת גם את B,
he: ולכן החיתוך הוא A עצמו.
en: Every family with two boys also meets B,
en: so the intersection is A itself.

he: ההסתברות המותנית : ההסתברות של
he: החיתוך, חלקי ההסתברות של התנאי.
en: The conditional probability: the probability
en: of the intersection over that of the condition.

he: מציבים : 1/4 בשביל שני בנים,
he: ו-3/4 בשביל שלוש המשפחות שנשארו.
en: Substitute: 1/4 for two boys,
en: and 3/4 for the three families left.

he: ומקבלים שליש, ולא חצי.
en: And we get a third, not a half.

he: איפה הניחוש טעה? "לפחות אחד בן"
he: לא אומר איזה מהשניים הוא הבן.
en: Where did the guess go wrong? "At least one boy"
en: does not say which of the two is the boy.

he: אם המידע היה "הבכור הוא בן", נשארת
he: רק השורה העליונה : בן ובן, ובן ובת.
en: Had the information been "the elder is a boy",
en: only the top row would remain: boy-boy and boy-girl.

he: אז התשובה הייתה חצי : המידע
he: מצביע על ילד מסוים.
en: Then the answer would be a half:
en: the information points at a specific child.

he: ב"לפחות אחד" הבן יכול להיות כל אחד :
he: שתי משפחות של בן ובת, מול אחת של שני בנים.
en: With "at least one" the boy can be either child:
en: two boy-girl families against one with two boys.

he: מלכודת : לספור בן ובת כתוצאה אחת.
he: היא קורית בשני סדרים, ולכן ההסתברות שלה חצי.
en: Trap: counting boy-and-girl as one outcome.
en: It happens in two orders, so its probability is a half.

he: עכשיו יוסי עונה כן לשאלה : יש לך בן
he: שנולד ביום שלישי? מה ההסתברות עכשיו?
en: Now Yossi says yes to: do you have a boy
en: born on a Tuesday? What is the probability now?

he: נראה שיום הלידה לא אמור לשנות כלום.
he: בואו נספור.
en: The birthday seems not to matter at all.
en: Let's count.

he: כל ילד הוא אחד מ-14 סוגים שווי הסתברות :
he: בן או בת, כפול שבעה ימים.
en: Each child is one of 14 equally likely kinds:
en: boy or girl, times seven days.

he: בן שנולד ביום שלישי הוא סוג אחד מהם,
he: בהסתברות 1/14.
en: A boy born on a Tuesday is one of those kinds,
en: with probability 1/14.

he: לשני ילדים יש 14 × 14 = 196 זוגות
he: מסודרים, כל אחד בהסתברות 1/196.
en: Two children have 14 × 14 = 196 ordered pairs,
en: each with probability 1/196.

he: השורות הן הילד הראשון, והעמודות השני.
he: האות ג היא יום שלישי.
en: The rows are the first child, the columns the second.
en: Tuesday is the third letter, gimel.

he: הילד הראשון בן מיום שלישי : זו שורה
he: אחת של 14 זוגות, השני הוא כל סוג.
en: The first child a Tuesday boy: one row
en: of 14 pairs, the second child of any kind.

he: גם הילד השני יכול להיות בן מיום שלישי :
he: עמודה אחת, עוד 14 זוגות.
en: The second child can be a Tuesday boy too:
en: one column, another 14 pairs.

he: המשבצת שבהצטלבות, שני בנים מיום שלישי,
he: נספרה פעמיים. מורידים אותה פעם אחת.
en: The cell where they cross, two Tuesday boys,
en: was counted twice. Remove it once.

he: לכן התנאי מתקיים ב-27 זוגות,
he: ולא ב-28.
en: So the condition holds in 27 pairs,
en: not 28.

he: מתוכם, שני בנים : הריבוע המקווקו.
he: שבעה בשורה, שבעה בעמודה, פחות הכפולה.
en: Of these, two boys: the dashed square.
en: Seven in the row, seven in the column, less the double.

he: כל הזוגות שווי הסתברות, ולכן ההסתברות
he: היא 13 חלקי 27, בערך 0.481.
en: All pairs are equally likely, so the probability
en: is 13 over 27, about 0.481.

he: כמעט חצי, ורחוק מהשליש של סעיף א.
he: המידע הספציפי שינה את התשובה.
en: Almost a half, and far from part A's third.
en: The specific information changed the answer.

he: בלי ההורדה של המשבצת הכפולה היינו
he: מקבלים 14 חלקי 28, כלומר חצי. וזו טעות.
en: Without removing the double cell we would get
en: 14 over 28, a half. That is a mistake.

he: למה? יום שלישי הוא מידע כמעט על ילד
he: מסוים, כמו "הבכור הוא בן", שנותן חצי.
en: Why? A Tuesday is information almost about one child,
en: like "the elder is a boy", which gives a half.

he: אותה תשובה דרך בייס. הריבוע של שני
he: בנים : 49 משבצות מתוך 196, רבע.
en: The same answer through Bayes. The two-boys square:
en: 49 cells out of 196, a quarter.

he: בתוך הריבוע, אף בן לא נולד ביום
he: שלישי בהסתברות (6/7)². המשלים 13/49.
en: Inside the square, no boy was born on a Tuesday
en: with probability (6/7)². The complement is 13/49.

he: כל ילד הוא בן מיום שלישי ב-1/14,
he: ולכן התנאי קורה ב-1 פחות (13/14)².
en: Each child is a Tuesday boy with 1/14,
en: so the condition has 1 minus (13/14)².

he: מציבים בנוסחת בייס :
he: ‏13/196 חלקי 27/196, שוב 13/27.
en: Into Bayes' formula:
en: 13/196 over 27/196, again 13/27.

he: התיבה שבעמוד סופרת את אותו צלב, צעד
he: אחרי צעד. צעד 1 : השורה, 14 משפחות.
en: The page's box counts the same cross, step by step.
en: Step 1: the row, 14 families.

he: צעד 2 : העמודה של הילד השני, עוד 14.
he: המשבצת שבהצטלבות נספרה פעמיים.
en: Step 2: the second child's column, another 14.
en: The cell where they cross was counted twice.

he: צעד 3 : כל משפחה נספרת פעם אחת,
he: ‏14 + 14 − 1 = 27 משפחות.
en: Step 3: each family counted once,
en: 14 + 14 − 1 = 27 families.

he: צעד 4 : מתוכן שני בנים,
he: ‏7 + 7 − 1 = 13. ההסתברות 13/27.
en: Step 4: of them two boys,
en: 7 + 7 − 1 = 13. The probability is 13/27.

he: הטבלה שבתיבה משווה שלושה סוגי מידע,
he: כל אחד על אותן 196 משפחות.
en: The box's table compares three kinds of information,
en: each on the same 196 families.

he: לפחות אחד בן נותן שליש, בן מיום שלישי
he: ‏13/27, והבכור הוא בן נותן חצי.
en: At least one boy gives a third, a Tuesday boy
en: 13/27, and the elder is a boy gives a half.

he: יום שלישי נמצא ביניהם : ככל שהמידע
he: ספציפי יותר, התשובה קרובה יותר לחצי.
en: Tuesday sits between them: the more specific
en: the information, the closer the answer to a half.

he: עכשיו בכלליות : C ילדים, כל אחד בן
he: בהסתברות p, ועם התכונה בהסתברות q.
en: Now in general: C children, each a boy
en: with probability p, with the trait with probability q.

he: נסמן : A הוא כל הילדים בנים, ו-T הוא
he: לפחות ילד אחד שהוא בן עם התכונה.
en: Let A be all children boys, and T
en: at least one child a boy with the trait.

he: שניהם מאורעות של "לפחות אחד", ואת
he: שניהם הכי קל לחשב דרך המשלים : "אף אחד".
en: Both are "at least one" events, and both are easiest
en: through the complement: "none".

he: ילד אחד הוא בן עם התכונה בהסתברות pq,
he: ואיננו כזה בהסתברות 1 − pq.
en: One child is a boy with the trait with probability pq,
en: and is not with probability 1 − pq.

he: הילדים בלתי תלויים, ולכן אף אחד מהם
he: איננו כזה בהסתברות (1 − pq) בחזקת C.
en: The children are independent, so none of them is
en: with probability (1 − pq) to the power C.

he: המכנה הוא המשלים : 1 פחות
he: החזקה הזו. זו ההסתברות של T.
en: The denominator is the complement: 1 minus
en: that power. This is the probability of T.

he: המונה : כל הילדים בנים
he: בהסתברות p בחזקת C.
en: The numerator: all children are boys
en: with probability p to the power C.

he: אם כולם בנים, T אומר רק שלפחות לאחד
he: יש את התכונה : אחד פחות (1 − q) בחזקת C.
en: If all are boys, T only says that at least one has
en: the trait: one minus (1 − q) to the power C.

he: לכן החיתוך הוא המכפלה : ההסתברות
he: שכולם בנים, כפול זו של התכונה.
en: So the intersection is the product: the probability
en: all are boys, times that of the trait.

he: מחלקים את המונה במכנה,
he: ומקבלים את הנוסחה הכללית.
en: Divide the numerator by the denominator,
en: and we get the general formula.

he: בדיקה : בלי תכונה, q = 1, הנוסחה
he: נותנת רבע חלקי שלושה רבעים, שליש.
en: Check: no trait, q = 1, the formula
en: gives a quarter over three quarters, a third.

he: יום בשבוע, q = 1/7 : המונה 13/196,
he: המכנה 27/196, ושוב 13/27.
en: A weekday, q = 1/7: the numerator is 13/196,
en: the denominator 27/196, again 13/27.

he: תכונה נדירה מאוד, q שואף ל-0 :
he: התשובה שואפת ל-p בחזקת C − 1.
en: A very rare trait, q tends to 0:
en: the answer tends to p to the power C − 1.

he: עם שני ילדים זה חצי : המידע מצביע
he: כמעט בוודאות על בן אחד מסוים.
en: With two children that is a half: the information
en: points almost surely at one specific boy.

he: ככל ש-q קטן, המידע ספציפי יותר,
he: והתשובה עולה מהשליש לכיוון החצי.
en: The smaller q, the more specific the information,
en: and the answer rises from a third towards a half.

he: עם שלושה ילדים, מאותה נוסחה : מהשביעית
he: של "לפחות אחד בן" ועד רבע.
en: With three children, from the same formula:
en: from "at least one boy"'s seventh up to a quarter.

he: התיבה שבעמוד מחשבת את הנוסחה. בערכי
he: העמוד, p = 1/2 ו-q = 1/7, התשובה 0.4815.
en: The page's box computes the formula. On the page's
en: values, p = 1/2 and q = 1/7, the answer is 0.4815.

he: בריבוע, השטח של כל משבצת הוא ההסתברות
he: של הזוג. הצלב הצבעוני הוא התנאי.
en: In the square, each cell's area is the probability
en: of the pair. The coloured cross is the condition.

he: החלק הירוק, בתוך הריבוע המקווקו של
he: שני בנים, הוא המטרה.
en: The green part, inside the dashed
en: two-boys square, is the target.

he: העקומה : התשובה לכל q. מימין, q = 1
he: והשליש. משמאל, q קטן והקו של החצי.
en: The curve: the answer for every q. Right: q = 1
en: and the third. Left: small q, and the half line.

he: עם שלושה ילדים, C = 3 : התשובה 0.2322,
he: כלומר 127/547, והגבול הוא רבע.
en: With three children, C = 3: the answer is 0.2322,
en: that is 127/547, and the limit is a quarter.

he: מלכודת אחרונה : התשובה תלויה בדרך
he: שבה התקבל המידע. שאלנו שאלה של כן או לא.
en: A last trap: the answer depends on how the information
en: came. We asked a yes-or-no question.

he: אם יוסי היה בוחר ילד באקראי ומספר עליו,
he: המידע היה על ילד מסוים, והתשובה חצי.
en: Had Yossi picked a child at random and told us about it,
en: the information would be about one child: a half.

he: לסיכום : שליש, 13/27, ונוסחה אחת
he: שמחזירה את שניהם.
en: To sum up: a third, 13/27, and one formula
en: that gives back both.

he: נסו ערכים משלכם בתיבות
he: שבעמוד של שאלה 0015 באתר.
en: Try your own values in the boxes
en: on the page of question 0015 on the site.
