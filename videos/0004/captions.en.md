# 0004 — three mislabeled boxes: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0004 : שלוש קופסאות עם תוויות שגויות,
he: שאלה ברמת ג'וניור.
en: Question 0004: three boxes with wrong labels,
en: a junior-level question.

he: שני סעיפים : כמה דגימות צריך,
he: ואיך כותבים את זה בקוד.
en: Two parts: how many draws are needed,
en: and how to write it in code.

he: באחת הקופסאות רק כדורים אדומים, באחרת רק שחורים,
he: ובשלישית גם וגם.
en: One box holds only red balls, another only black,
en: and the third holds both.

he: על כל קופסה מודבקת תווית :
he: אדום, שחור, ואדום ושחור.
en: Each box has a label on it:
en: "Red", "Black", and "Red and Black".

he: והחוק היחיד : כל התוויות שגויות.
en: And the only rule: every label is wrong.

he: סעיף א : מהו המספר המינימלי של דגימות
he: שמבטיח שנוכל לתקן את כל התוויות?
en: Part A: what is the minimum number of draws
en: that guarantees we can fix all the labels?

he: דגימה : מצביעים על קופסה,
he: ומקבלים ממנה כדור אחד אקראי.
en: A draw: you point at a box,
en: and get one random ball from it.

he: יש שש דרכים לחלק את שלושת סוגי התוכן
he: בין שלוש הקופסאות.
en: There are six ways to assign the three kinds of content
en: to the three boxes.

he: אבל כל התוויות שגויות, ולכן נפסל
he: כל סידור שבו תוכן תואם לתווית שלו.
en: But every label is wrong, so we rule out
en: any arrangement where a box's content matches its label.

he: נשארים רק שני סידורים אפשריים,
he: וצריך להכריע ביניהם.
en: Only two possible arrangements remain,
en: and we must decide between them.

he: בקופסה "אדום" יש שחור או תערובת.
he: כדור שחור מתאים לשני הסידורים.
en: The "Red" box holds black or the mix.
en: A black ball fits both arrangements.

he: בקופסה "שחור" יש תערובת או אדום,
he: וכדור אדום מתאים לשניהם.
en: The "Black" box holds the mix or red,
en: and a red ball fits both.

he: רק בקופסה "אדום ושחור"
he: שני הסידורים נבדלים בצבע אחד וברור.
en: Only in the "Red and Black" box
en: do the arrangements differ: red in one, black in the other.

he: הרעיון : התווית "אדום ושחור" שגויה,
he: ולכן בקופסה הזו יש צבע אחד בלבד.
en: The idea: the "Red and Black" label is wrong,
en: so this box holds a single color only.

he: מקרה ראשון : מהקופסה "אדום ושחור" יוצא כדור אדום.
he: זו הקופסה האדומה.
en: Case one: the "Red and Black" box gives a red ball.
en: So it is the red box.

he: הקופסה "שחור" לא שחורה, כי התווית שגויה,
he: וגם לא אדומה. לכן היא התערובת.
en: The "Black" box is not black, since its label is wrong,
en: and not red either. So it holds the mix.

he: ולקופסה "אדום" נשאר השחור.
en: And the "Red" box is left with black.

he: מקרה שני : יוצא כדור שחור.
he: אז זו הקופסה השחורה.
en: Case two: a black ball comes out.
en: Then this is the black box.

he: הקופסה "אדום" לא אדומה וגם לא שחורה,
he: לכן היא התערובת, ול"שחור" נשאר האדום.
en: The "Red" box is neither red nor black,
en: so it holds the mix, and "Black" is left with red.

he: הכלל : יצא צבע c? הקופסה שתוויתה c
he: מכילה את הצבע השני, והשלישית את התערובת.
en: The rule: color c came out? The box labeled c
en: holds the other color, and the third holds the mix.

he: ולמה לא אפס? בלי דגימה נשארים שני סידורים,
he: ואין דרך לבחור ביניהם.
en: And why not zero? With no draw, two arrangements remain,
en: and there is no way to choose between them.

he: לכן התשובה : דגימה אחת,
he: ודווקא מהקופסה "אדום ושחור".
en: So the answer: one draw,
en: and it must be from the "Red and Black" box.

he: בתיבה שבעמוד אפשר לנסות :
he: לוחצים על קופסה ודוגמים ממנה כדור.
en: In the page's box you can try it:
en: click a box to draw a ball from it.

he: דוגמים מהקופסה "אדום ושחור",
he: ויוצא כדור אדום.
en: We draw from the box "Red and Black",
en: and a red ball comes out.

he: גילוי התוכן מראה בדיוק את מה שהסקנו :
he: שלוש התוויות הנכונות, מדגימה אחת.
en: Revealing the contents shows exactly what we deduced:
en: all three labels, from one draw.

he: המלכודת : לדגום מהקופסה "אדום".
he: כדור שחור משם משאיר את שני הסידורים פתוחים.
en: The trap: drawing from the "Red" box.
en: A black ball from it leaves both arrangements open.

he: אותו דבר בקופסה "שחור".
he: רק "אדום ושחור" ידועה מראש כחד-צבעית.
en: The same goes for the "Black" box.
en: Only "Red and Black" is known in advance to hold one color.

he: סעיף ב : מתרגמים את הפתרון לפונקציה.
en: Part B: turning the solution into a function.

he: הקלט : מערך labels של שלוש תוויות,
he: כלומר RED, BLACK ו-MIXED, בסדר כלשהו.
en: The input: an array labels of three labels,
en: that is, RED, BLACK and MIXED, in some order.

he: ה-API : draw(i) שולף כדור אקראי מקופסה i,
he: ומחזיר RED או BLACK.
en: The API: draw(i) takes a random ball from box i,
en: and returns RED or BLACK.

he: בדוגמה מהעמוד, התוכן האמיתי הוא סידור 1 מסעיף א,
he: ולכן הכדור מקופסה 2 אדום.
en: The page's example uses arrangement 1 from part A,
en: so the ball from box 2 is red.

he: הפתרון הראשון מתרגם את סעיף א כמעט מילה במילה,
he: ובונה מערך fixed חדש.
en: The first solution translates part A almost word for word,
en: and builds a new array, fixed.

he: הפונקציה מקבלת את מערך התוויות,
he: ומחזירה את התוויות הנכונות.
en: The function takes the array of labels
en: and returns the correct labels.

he: המערך fixed יקבל את התוויות המתוקנות.
he: בינתיים שלוש מחרוזות ריקות.
en: The array fixed will hold the corrected labels.
en: For now, three empty strings.

he: לולאה ראשונה : מחפשים את הקופסה
he: שתוויתה MIXED, ושומרים את האינדקס שלה ב-k.
en: First loop: find the box labelled MIXED
en: and keep its index in k.

he: הדגימה היחידה בפונקציה, מקופסה k.
he: היא חד-צבעית, ולכן ball הוא הצבע שלה.
en: The only draw in the function, from box k.
en: That box holds one colour, so ball is its colour.

he: התנאי קובע את הצבע השני, other :
he: אם ball הוא RED אז BLACK, ואחרת RED.
en: The if sets the second colour, other:
en: BLACK if ball is RED, and RED otherwise.

he: קופסה k מקבלת את התווית ball,
he: כי זה הצבע היחיד שבה.
en: Box k gets the label ball,
en: the only colour inside it.

he: לולאה שנייה : הקופסה שתוויתה ball
he: מקבלת other, לפי הכלל של סעיף א.
en: Second loop: the box labelled ball
en: gets other, by the rule of Part A.

he: לולאה שלישית : בקופסה שתוויתה other
he: אין other ואין ball, ולכן היא MIXED.
en: Third loop: the box labelled other holds
en: neither other nor ball, so it is MIXED.

he: ומחזירים את fixed.
he: המערך labels עצמו לא השתנה.
en: And return fixed.
en: The array labels itself is unchanged.

he: נריץ על הדוגמה מהעמוד, ליד התיבה,
he: כש-draw מחזיר RED.
en: We run it on the page's example, beside the box,
en: with draw returning RED.

he: המעבר הראשון מחפש את MIXED.
he: הוא בקופסה 2, ולכן k = 2.
en: The first pass looks for MIXED.
en: It is on box 2, so k = 2.

he: דגימה אחת מקופסה 2 : יוצא RED.
en: One draw from box 2: it gives RED.

he: הצבע השני, other, הוא BLACK,
he: וקופסה 2 מקבלת RED.
en: The other color, other, is BLACK,
en: and box 2 gets RED.

he: המעבר השני : הקופסה שתוויתה RED
he: מקבלת את other, כלומר BLACK.
en: The second pass: the box labeled RED
en: gets other, that is, BLACK.

he: המעבר השלישי : הקופסה שתוויתה BLACK
he: מקבלת MIXED.
en: The third pass: the box labeled BLACK
en: gets MIXED.

he: התוצאה : BLACK, MIXED, RED.
he: בדיוק סידור 1.
en: The result: BLACK, MIXED, RED.
en: Exactly arrangement 1.

he: ואם הכדור שחור? other הוא RED,
he: וקופסה 2 מקבלת BLACK.
en: And if the ball is black? other is RED,
en: and box 2 gets BLACK.

he: קופסה 1 מקבלת RED, וקופסה 0 מקבלת MIXED.
he: זה סידור 2.
en: Box 1 gets RED, and box 0 gets MIXED.
en: That is arrangement 2.

he: הפתרון נכון וקריא, אבל עובר על המערך שלוש פעמים
he: ומחזיק מערך נוסף.
en: Correct and readable, but it makes three passes
en: over the array and keeps an extra array.

he: הפתרון השני מתחיל מתצפית :
he: התיקון הוא סיבוב של שלוש התוויות.
en: The second solution starts from an observation:
en: the fix is a rotation of the three labels.

he: נקרא same לקופסה שתוויתה כצבע הכדור,
he: ו-other לקופסה השלישית.
en: Call same the box labeled with the ball's color,
en: and other the third box.

he: צבע הכדור עובר ל-k, MIXED עובר ל-other,
he: והצבע השני עובר ל-same.
en: The ball's color moves to k, MIXED moves to other,
en: and the other color moves to same.

he: וסיבוב של שלושה איברים
he: הוא בדיוק שתי החלפות.
en: And a rotation of three elements
en: is exactly two swaps.

he: בתיבה שבעמוד, fix_labels רץ שלב אחרי שלב
he: על הדוגמה מהעמוד.
en: In the page's box, fix_labels runs step by step
en: on the page's example.

he: החצים מעל הקופסאות הם הסיבוב
he: של שלוש התוויות, ו-same ו-other מסומנים.
en: The arrows over the boxes are the rotation
en: of the three labels; same and other are marked.

he: ובסוף התיבה מגלה את התוכן :
he: שלוש התוויות נכונות, אחרי שתי החלפות.
en: At the end the box reveals the contents:
en: all three labels are right, after two swaps.

he: הקוד : אחרי הדגימה לא מחפשים שוב,
he: ולא בונים מערך חדש.
en: The code: after the draw there is no second search,
en: and no new array.

he: הפעם הפונקציה מתקנת את labels במקום,
he: ומחזירה את אותו מערך.
en: This time the function fixes labels in place
en: and returns the same array.

he: המתודה index מוצאת את MIXED בשורה אחת,
he: והדגימה היחידה היא שוב מקופסה k.
en: The index method finds MIXED in one line,
en: and the only draw is again from box k.

he: השכנים של k במעגל, n1 ו-n2,
he: בלי לולאה ובלי חיפוש.
en: The neighbours of k on the circle, n1 and n2,
en: with no loop and no search.

he: בדיקה אחת : השכן שתוויתו כצבע הכדור
he: הוא same, והשני הוא other.
en: One check: the neighbour labelled with the ball's colour
en: is same, and the other one is other.

he: החלפה ראשונה, בהשמה מרובה ובלי tmp :
he: קופסה k מקבלת את צבע הכדור.
en: The first swap, by multiple assignment, with no tmp:
en: box k gets the ball's colour.

he: החלפה שנייה, בין same ל-other.
he: שתי ההחלפות יחד הן הסיבוב.
en: The second swap, between same and other.
en: Together the two swaps are the rotation.

he: ומחזירים את labels, מתוקן במקום.
en: And return labels, fixed in place.

he: ועכשיו הריצה ליד התיבה מהעמוד,
he: שוב עם כדור אדום.
en: And now the run beside the page's box,
en: again with a red ball.

he: שוב k = 2, והכדור שיוצא אדום.
en: Again k = 2, and the ball that comes out is red.

he: השכנים של k : ‏(k + 1) % 3, כלומר 0,
he: ו-(k + 2) % 3, כלומר 1.
en: The neighbors of k: (k + 1) % 3, that is, 0,
en: and (k + 2) % 3, that is, 1.

he: בקופסה 0 כתוב RED, כמו הכדור,
he: ולכן same = 0 ו-other = 1.
en: Box 0 says RED, like the ball,
en: so same = 0 and other = 1.

he: החלפה ראשונה, בין k ל-same : קופסה 2 כבר נכונה,
he: ו-MIXED עובר זמנית ל-0.
en: First swap, k with same: box 2 is now correct,
en: and MIXED moves to 0 for the moment.

he: החלפה שנייה, בין same ל-other :
he: מתקבל BLACK, MIXED, RED.
en: Second swap, same with other:
en: the result is BLACK, MIXED, RED.

he: אותה תוצאה כמו בפתרון הראשון,
he: בשתי החלפות במקום.
en: The same result as the first solution,
en: with two swaps in place.

he: ולמה (k + 2) % 3 ולא (k − 1) % 3?
he: שניהם אמורים לתת את השכן הקודם במעגל.
en: And why (k + 2) % 3 and not (k − 1) % 3?
en: Both should give the previous neighbor on the circle.

he: ב-Python, ‏(0 − 1) % 3 הוא 2,
he: כי שם התוצאה של % אף פעם לא שלילית.
en: In Python, (0 − 1) % 3 is 2,
en: because there the result of % is never negative.

he: ב-SystemVerilog וב-C, % שומר על סימן המחולק :
he: יוצא −1, אינדקס לא חוקי.
en: In SystemVerilog and C, % keeps the sign of the dividend:
en: it gives −1, an invalid index.

he: חיבור 2 שקול לחיסור 1 מודולו 3, ונשאר חיובי.
he: לכן הקוד זהה בשתי השפות.
en: Adding 2 equals subtracting 1 modulo 3, and stays positive.
en: So the code is the same in both languages.

he: הסיבוכיות : שני הפתרונות O(1),
he: עם דגימה אחת.
en: The cost: both solutions are O(1),
en: with a single draw.

he: השני עושה מעבר אחד ושתי החלפות במקום,
he: בלי מערך נוסף.
en: The second makes one pass and two swaps in place,
en: with no extra array.

he: לסיכום : דגימה אחת מהקופסה "אדום ושחור"
he: מתקנת את שלוש התוויות.
en: To sum up: one draw from the "Red and Black" box
en: fixes all three labels.

he: ובקוד התיקון הוא סיבוב, שתי החלפות במקום.
he: נסו בתיבה שבעמוד של שאלה 0004.
en: In code, the fix is a rotation: two swaps in place.
en: Try it in the box on the page of question 0004.
