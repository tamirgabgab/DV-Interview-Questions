# 0055 — the divide-by-3 state machine: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); notes/VIDEOS.md.

he: שאלה 0055 : מכונת מצבים לחלוקה ב-3,
he: שאלה ברמת ג'וניור.
en: Question 0055: a state machine for division by 3,
en: a junior-level question.

he: שלושה סעיפים : ביט חדש נכנס כ-LSB,
he: ביט חדש נכנס כ-MSB, ואז כל m וכל בסיס.
en: Three parts: each new bit enters as the LSB,
en: then as the MSB, then any m and any base.

he: בכל מחזור שעון נכנס ביט אחד, din.
he: המספר יכול להיות ארוך כרצוננו.
en: Each clock cycle one bit comes in, din.
en: The number can be as long as you like.

he: אחרי כל ביט, div אומר אם המספר
he: שנקרא עד עכשיו מתחלק ב-3.
en: After each bit, div says whether the number
en: read so far is divisible by 3.

he: סעיף א : הביט החדש הוא הביט הנמוך
he: של המספר, כמו בקריאה רגילה.
en: Part A: the new bit is the number's lowest bit,
en: as in normal reading.

he: ביט חדש מכפיל את המספר ב-2
he: ומוסיף את הביט : v הופך ל-2v + b.
en: A new bit doubles the number
en: and adds the bit: v becomes 2v + b.

he: את v אי אפשר לשמור. אבל השארית
he: של 2v + b תלויה רק בשארית של v.
en: We cannot store v. But the remainder
en: of 2v + b depends only on v's remainder.

he: לכן המצב הוא השארית r : 0, 1 או 2.
he: שלושה מצבים, ו-div דולק כש-r = 0.
en: So the state is the remainder r: 0, 1 or 2.
en: Three states, and div is on when r = 0.

he: שלושת המצבים. המצב 0 בעיגול כפול :
he: שם המספר מתחלק, ו-div = 1.
en: The three states. State 0 has a double ring:
en: there the number is divisible, div = 1.

he: ממצב 0 : הביט 0 משאיר אותו ב-0,
he: והביט 1 מעביר ל-1.
en: From state 0: bit 0 keeps it at 0,
en: and bit 1 moves it to 1.

he: ממצב 1 : 2 · 1 + 0 = 2, ו-2 · 1 + 1 = 3,
he: שהוא 0. לכן ל-2 או ל-0.
en: From state 1: 2·1 + 0 = 2, and 2·1 + 1 = 3,
en: which is 0. So to 2 or to 0.

he: ממצב 2 : 4 שהוא 1, ו-5 שהוא 2.
he: שישה מעברים בסך הכול.
en: From state 2: 4, which is 1, and 5, which is 2.
en: Six transitions in all.

he: הדוגמה מהעמוד : 13, כלומר 1101,
he: מגיע ביט אחרי ביט. מתחילים ב-0.
en: The page's example: 13, that is 1101,
en: arrives bit by bit. We start at 0.

he: הביט 1 : המספר 1, שארית 1.
en: Bit 1: the number 1, remainder 1.

he: הביט 1 : המספר 3, שארית 0. div = 1.
en: Bit 1: the number 3, remainder 0. div = 1.

he: הביט 0 : המספר 6, שארית 0. div = 1.
en: Bit 0: the number 6, remainder 0. div = 1.

he: הביט 1 : המספר 13, שארית 1.
en: Bit 1: the number 13, remainder 1.

he: עכשיו לחומרה. שלושה מצבים הם שני ביטים,
he: ‏Q1 ו-Q0 : 0 הוא 00, 1 הוא 01, 2 הוא 10.
en: Now to hardware. Three states take two bits,
en: Q1 and Q0: 0 is 00, 1 is 01, 2 is 10.

he: הקוד 11 לא בשימוש. בטבלאות הוא
he: ‏Don't care : אפשר לבחור בו מה שנוח.
en: Code 11 is unused. In the tables it is
en: a don't care: we may choose what helps.

he: טבלת המעברים עם הקידוד : כל מצב וביט,
he: והמצב הבא, שהוא הכניסה D1D0.
en: The encoded transition table: each state and bit,
en: and the next state, which is the input D1D0.

he: ושתי שורות של 11 : לא מגיעים אליהן,
he: ולכן המצב הבא שלהן xx.
en: And two rows of 11: we never reach them,
en: so their next state is xx.

he: מפת קרנו לכל כניסה של Flip-Flop :
he: השורות Q1Q0 בסדר Gray, והעמודות b.
en: A Karnaugh map per flip-flop input:
en: rows Q1Q0 in Gray order, columns b.

he: ‏D1 : שתי קבוצות, בעזרת ה-x.
he: ‏Q0·b' ועוד Q1·b.
en: D1: two groups, with the help of the x.
en: Q0·b' plus Q1·b.

he: ‏D0 : Q1·b' ועוד תא בודד,
he: ‏Q1'·Q0'·b, שאין לו שכן.
en: D0: Q1·b' plus a single cell,
en: Q1'·Q0'·b, which has no neighbour.

he: והיציאה תלויה רק במצב : div דולק
he: ב-00, כלומר div = Q1'·Q0'.
en: And the output depends only on the state:
en: div is on at 00, so div = Q1'·Q0'.

he: המעגל. משמאל המסילות : b, ההיפוך שלו
he: דרך שער NOT, וארבעת המוצאים של המצב.
en: The circuit. On the left the rails: b, its inverse
en: through a NOT gate, and the four state outputs.

he: שער AND לכל מכפלה של המשוואות,
he: ונקודה מסמנת חיבור למסילה.
en: An AND gate for each product of the equations;
en: a dot marks a connection to a rail.

he: שערי OR מחברים את המכפלות
he: לכניסות D1 ו-D0.
en: OR gates join the products
en: into the inputs D1 and D0.

he: שני Flip-Flops מסוג D, עם שעון ואיפוס
he: אסינכרוני ל-00. Q ו-Q' חוזרים למסילות.
en: Two D flip-flops with a clock and an asynchronous
en: reset to 00. Q and Q' go back to the rails.

he: ושער AND אחרון : div = Q1'·Q0'.
he: חוט כתום נושא 1, חוט אפור נושא 0.
en: And a last AND gate: div = Q1'·Q0'.
en: An amber wire carries 1, a grey wire 0.

he: אחרי האיפוס המצב 00 ו-div = 1 :
he: המספר 0 מתחלק. עכשיו 1101.
en: After reset the state is 00 and div = 1:
en: the number 0 is divisible. Now 1101.

he: הביט 1 : Q1'·Q0'·b דולק,
he: ולכן D0 = 1 ו-D1 = 0. המצב הבא 01.
en: Bit 1: Q1'·Q0'·b is on,
en: so D0 = 1 and D1 = 0. The next state is 01.

he: עליית שעון : המצב 01, כלומר שארית 1.
he: ‏div = 0, כי 1 לא מתחלק.
en: Clock edge: state 01, that is remainder 1.
en: div = 0, because 1 is not divisible.

he: שוב הביט 1. עכשיו אף מכפלה לא דולקת :
he: ‏D1D0 = 00.
en: Bit 1 again. Now no product is on:
en: D1D0 = 00.

he: המצב 00 ו-div = 1 : המספר 3 מתחלק.
en: State 00 and div = 1: the number 3 is divisible.

he: הביט 0 במצב 00 : כל המכפלות כבויות,
he: והמצב נשאר 00.
en: Bit 0 in state 00: all products are off,
en: and the state stays 00.

he: המספר 6, ו-div נשאר 1.
en: The number 6, and div stays 1.

he: הביט 1 במצב 00 : שוב Q1'·Q0'·b,
he: והמצב הבא 01.
en: Bit 1 in state 00: Q1'·Q0'·b again,
en: and the next state is 01.

he: המספר 13 : שארית 1, ו-div = 0.
he: בדיוק כמו בדיאגרמה.
en: The number 13: remainder 1, and div = 0.
en: Exactly as in the diagram.

he: מה אם הפליפ-פלופים מתחילים ב-11?
he: עם b = 0 : D1 = Q0·b' = 1, וגם D0 = 1.
en: What if the flip-flops start at 11?
en: With b = 0: D1 = Q0·b' = 1, and D0 = 1 too.

he: המצב 11 נשאר 11 כל עוד b = 0, ו-div
he: תקוע ב-0. לכן האיפוס ל-00 חשוב.
en: State 11 stays 11 as long as b = 0, and div
en: is stuck at 0. So the reset to 00 matters.

he: וכך זה נראה בתיבה שבעמוד,
he: על אותו 1101.
en: And this is how it looks in the page's box,
en: on the same 1101.

he: הביט 1 : מ-0 ל-1, בחץ הכתום.
en: Bit 1: from 0 to 1, on the orange arrow.

he: הביט 1 : מ-1 ל-0. ‏3 מתחלק.
en: Bit 1: from 1 to 0. 3 is divisible.

he: הביט 0 : נשארים ב-0. ‏6 מתחלק.
en: Bit 0: we stay at 0. 6 is divisible.

he: הביט 1 : ל-1. ‏13 לא מתחלק.
en: Bit 1: to 1. 13 is not divisible.

he: העלות : שני Flip-Flops, חמישה שערי AND,
he: שני OR ו-NOT אחד, בלי קשר לאורך המספר.
en: The cost: two flip-flops, five AND gates, two ORs
en: and one NOT, whatever the number's length.

he: סעיף ב : הביט החדש הוא הביט הגבוה
he: של המספר. 6 = 110 מגיע כ-0, 1, 1.
en: Part B: the new bit is the number's highest bit.
en: 6 = 110 arrives as 0, 1, 1.

he: עכשיו הביט ה-k מוסיף b · 2^k, ו-2^k
he: מודולו 3 מתחלף : 1, 2, 1, 2.
en: Now bit k adds b·2^k, and 2^k
en: modulo 3 alternates: 1, 2, 1, 2.

he: הניסיון הראשון : לשמור את השארית
he: וגם את הזוגיות של k. שישה מצבים.
en: The first attempt: keep the remainder
en: and the parity of k. Six states.

he: אבל העתיד תלוי רק ב-x = r · 2^-k.
he: ב-3 הפכי של 2 הוא 2.
en: But the future depends only on x = r·2^-k.
en: Modulo 3 the inverse of 2 is 2.

he: ואז x' = 2(x + b) mod 3 : המיקום k נעלם.
he: שוב שלושה מצבים, ו-div דולק כש-x = 0.
en: Then x' = 2(x + b) mod 3: the position k is gone.
en: Three states again, and div is on when x = 0.

he: שוב שלושה מצבים, עם מעברים אחרים.
he: המצב 0 בעיגול כפול.
en: Three states again, with other transitions.
en: State 0 has a double ring.

he: ממצב 0 : הביט 0 נשאר ב-0,
he: והביט 1 נותן 2 · 1 = 2.
en: From state 0: bit 0 stays at 0,
en: and bit 1 gives 2·1 = 2.

he: ממצב 1 : 2 · 1 = 2, ו-2 · 2 = 4,
he: שהוא 1. לכן ל-2 או ל-1.
en: From state 1: 2·1 = 2, and 2·2 = 4,
en: which is 1. So to 2 or to 1.

he: ממצב 2 : 2 · 2 = 4 שהוא 1,
he: ו-2 · 3 = 6 שהוא 0.
en: From state 2: 2·2 = 4, which is 1,
en: and 2·3 = 6, which is 0.

he: זו המכונה של סעיף א, עם 1 ו-2
he: בתפקידים הפוכים. אותו קידוד : 00, 01, 10.
en: This is part A's machine with 1 and 2
en: swapped. The same code: 00, 01, 10.

he: הטבלה המקודדת של סעיף ב : x, הביט,
he: והמצב הבא x' = 2(x + b) mod 3.
en: Part B's encoded table: x, the bit,
en: and the next state x' = 2(x + b) mod 3.

he: ושוב 11 הוא Don't care.
en: And again 11 is a don't care.

he: שתי מפות קרנו, באותו סדר Gray.
en: Two Karnaugh maps, in the same Gray order.

he: ‏D1 : Q0·b' בעזרת ה-x,
he: ועוד התא הבודד Q1'·Q0'·b.
en: D1: Q0·b' with the help of the x,
en: plus the single cell Q1'·Q0'·b.

he: ‏D0 : Q0·b ועוד Q1·b'.
he: אותן מכפלות, רק במקומות אחרים.
en: D0: Q0·b plus Q1·b'.
en: The same products, just in other places.

he: והיציאה כמו בסעיף א : div = Q1'·Q0',
he: כי x = 0 בדיוק כשהמספר מתחלק.
en: The output is as in part A: div = Q1'·Q0',
en: since x = 0 exactly when the number divides.

he: אותן מסילות : b ו-b', ו-Q1, Q1', Q0, Q0'
he: שחוזרים מהפליפ-פלופים.
en: The same rails: b and b', and Q1, Q1', Q0, Q0'
en: coming back from the flip-flops.

he: ארבעה שערי AND למכפלות של סעיף ב.
en: Four AND gates for part B's products.

he: שני OR, ל-D1 ול-D0.
en: Two ORs, for D1 and D0.

he: אותם שני Flip-Flops, עם איפוס ל-00.
he: גם כאן 11 נשאר 11 כש-b = 0.
en: The same two flip-flops, reset to 00.
en: Here too 11 stays 11 when b = 0.

he: ‏div = Q1'·Q0', כמו קודם.
en: div = Q1'·Q0', as before.

he: עכשיו 6 = 110, מה-LSB : 0, 1, 1.
he: אחרי האיפוס x = 0.
en: Now 6 = 110, from the LSB: 0, 1, 1.
en: After reset x = 0.

he: הביט 0 במצב 00 : אף מכפלה לא דולקת,
he: והמצב הבא 00.
en: Bit 0 in state 00: no product is on,
en: and the next state is 00.

he: המספר 0 מתחלק : div = 1.
en: The number 0 is divisible: div = 1.

he: הביט 1 : Q1'·Q0'·b דולק,
he: ולכן D1 = 1. המצב הבא 10.
en: Bit 1: Q1'·Q0'·b is on,
en: so D1 = 1. The next state is 10.

he: ‏x = 2 : המספר 2 לא מתחלק, div = 0.
en: x = 2: the number 2 is not divisible, div = 0.

he: הביט 1 במצב 10 : Q1·b' כבוי, ו-Q0·b כבוי.
he: המצב הבא 00.
en: Bit 1 in state 10: Q1·b' is off, and Q0·b is off.
en: The next state is 00.

he: ‏x = 0 : המספר 6 מתחלק, div = 1.
en: x = 0: the number 6 is divisible, div = 1.

he: בתיבה בוחרים שרשור ל-MSB : הספרה
he: החדשה נכנסת משמאל. שוב 110.
en: In the box choose concatenation at the MSB:
en: the new digit enters on the left. Again 110.

he: הביט 0 : נשארים ב-0.
en: Bit 0: we stay at 0.

he: הביט 1 : ל-2. המספר 2.
en: Bit 1: to 2. The number 2.

he: הביט 1 : חזרה ל-0. ‏6 מתחלק.
en: Bit 1: back to 0. 6 is divisible.

he: אותה עלות בדיוק : גם מה-LSB
he: מספיקים שלושה מצבים ושני Flip-Flops.
en: Exactly the same cost: from the LSB too,
en: three states and two flip-flops are enough.

he: סעיף ג : חלוקה ב-m, כשבכל מחזור נכנסת
he: ספרה בבסיס B, ו-B ו-m זרים.
en: Part C: division by m, a base-B digit
en: entering each cycle, with B and m coprime.

he: מה-MSB ספרה חדשה הופכת את v ל-Bv + d,
he: והמצב הוא השארית : m מצבים.
en: From the MSB a new digit turns v into Bv + d,
en: and the state is the remainder: m states.

he: מה-LSB אותו טריק של סעיף ב, עם B^-1 :
he: גם כאן m מצבים.
en: From the LSB, part B's trick with B^-1:
en: m states here too.

he: ‏k ביטים במחזור הם ספרה בבסיס 2^k :
he: אותם m מצבים, רק המכפילים משתנים.
en: k bits a cycle are one digit in base 2^k:
en: the same m states, only the multipliers change.

he: דוגמה : חלוקה ב-7, ספרה עשרונית במחזור.
he: המכפיל 3, וההפכי של 10 הוא 5.
en: An example: division by 7, a decimal digit a cycle.
en: The multiplier is 3, the inverse of 10 is 5.

he: בתיבה : 343 = 7³, מה-MSB.
he: שבעה מצבים על הטבעת.
en: In the box: 343 = 7³, from the MSB.
en: Seven states on the ring.

he: הספרה 3 : שארית 3.
en: Digit 3: remainder 3.

he: הספרה 4 : 3 · 3 + 4 = 13, שארית 6.
en: Digit 4: 3·3 + 4 = 13, remainder 6.

he: הספרה 3 : 3 · 6 + 3 = 21, שארית 0.
he: ‏343 מתחלק ב-7.
en: Digit 3: 3·6 + 3 = 21, remainder 0.
en: 343 is divisible by 7.

he: ועכשיו מה-LSB, הספרה 3 קודם :
he: ‏(0 + 3) · 5 = 15, כלומר 1.
en: And now from the LSB, digit 3 first:
en: (0 + 3)·5 = 15, that is 1.

he: הספרה 4 : (1 + 4) · 5 = 25, כלומר 4.
en: Digit 4: (1 + 4)·5 = 25, that is 4.

he: הספרה 3 : (4 + 3) · 5 = 35, כלומר 0.
he: שוב מתחלק, מהכיוון השני.
en: Digit 3: (4 + 3)·5 = 35, that is 0.
en: Divisible again, from the other end.

he: לסיכום : שלושה מצבים בשני הכיוונים,
he: שני Flip-Flops ומעט שערים.
en: In short: three states in both directions,
en: two flip-flops and a few gates.

he: נסו מספרים משלכם בתיבה
he: שבעמוד של שאלה 0055 באתר.
en: Try your own numbers in the box
en: on the page of question 0055 on the site.
