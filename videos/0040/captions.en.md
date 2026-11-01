# 0040 — the 1011 sequence detector: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0040 : גלאי רצף 1011 עם חפיפה,
he: שאלה ברמת סטודנט.
en: Question 0040: a 1011 sequence detector with overlap,
en: a student-level question.

he: שני סעיפים : קודם התבנית 1011,
he: ואז בנייה שיטתית לכל תבנית.
en: Two parts: first the pattern 1011,
en: then a systematic build for any pattern.

he: בכל מחזור שעון מגיע ביט אחד, din.
he: המעגל מוציא found = 1 כשארבעת האחרונים 1011.
en: Each clock cycle brings one bit, din.
en: The circuit sets found = 1 when the last four are 1011.

he: בזרם 1011011 המוצא עולה פעמיים :
he: במחזור 4 ובמחזור 7.
en: On the stream 1011011 the output rises twice:
en: in cycle 4 and in cycle 7.

he: זו החפיפה : ה-1 האחרון של הזיהוי הראשון
he: הוא ה-1 הראשון של השני.
en: That is the overlap: the last 1 of the first match
en: is the first 1 of the second.

he: סעיף א : מכונת מצבים שמזהה את 1011,
he: כולל חפיפה.
en: Part A: a state machine that detects 1011,
en: overlaps included.

he: הרעיון : המצב זוכר כמה מהתבנית כבר ראינו,
he: ולא רק את הביט האחרון.
en: The idea: the state records how much of the pattern we saw,
en: not just the last bit.

he: לפני שהתבנית נגמרת יש ארבע אפשרויות :
he: כלום, 1, 10 ו-101. לכן ארבעה מצבים.
en: Before the pattern ends there are four options:
en: nothing, 1, 10 and 101. So four states.

he: מתקדמים כשהביט מתאים :
he: מ-S0 עם 1, מ-S1 עם 0, ומ-S2 עם 1.
en: Move forward when the bit matches:
en: S0 on 1, S1 on 0, and S2 on 1.

he: ‏S0 עם 0 נשאר במקום, וגם S1 עם 1 :
he: ‏11 מסתיים ב-1, שעדיין פותח את התבנית.
en: S0 on 0 stays put, and so does S1 on 1:
en: 11 ends in 1, which still starts the pattern.

he: ‏S2 עם 0 : הקלט 100. שום סיומת שלו
he: לא פותחת את התבנית, ולכן חוזרים ל-S0.
en: S2 on 0: the input is 100. No suffix of it
en: starts the pattern, so back to S0.

he: ‏S3 עם 0 : הקלט 1010, שמסתיים ב-10.
he: לכן לא חוזרים להתחלה, אלא ל-S2.
en: S3 on 0: the input is 1010, which ends in 10.
en: So not back to the start, but to S2.

he: ‏S3 עם 1 : זיהוי. הפלט 1 על המעבר,
he: וממשיכים ל-S1, כי 1011 מסתיים ב-1.
en: S3 on 1: a match. The output 1 is on the edge,
en: and we go on to S1, since 1011 ends in 1.

he: זו מכונת Mealy : הפלט תלוי במצב ובביט,
he: ולכן found עולה באותו מחזור.
en: A Mealy machine: the output depends on state and bit,
en: so found rises in the same cycle.

he: נריץ את 1011011. מתחילים ב-S0.
en: Let's run 1011011. We start in S0.

he: ‏1, 0, 1 : שלושה מעברים קדימה,
he: והמכונה ב-S3.
en: 1, 0, 1: three steps forward,
en: and the machine is in S3.

he: הביט הרביעי 1 : הפלט 1 במחזור 4,
he: והמכונה עוברת ל-S1.
en: The fourth bit, 1: the output is 1 in cycle 4,
en: and the machine moves to S1.

he: ‏0 ואחריו 1 מחזירים אותה ל-S3,
he: בזכות ה-1 שנשאר מהזיהוי.
en: 0 then 1 bring it back to S3,
en: thanks to the 1 left over from the match.

he: וה-1 האחרון מזהה שוב, במחזור 7 :
he: שני זיהויים, כמו שצריך.
en: And the last 1 matches again, in cycle 7:
en: two detections, as required.

he: כך זה נראה בתיבה שבעמוד : הגרף,
he: ורצועת תזמון שגדלה ביט אחרי ביט.
en: This is the page's box: the graph,
en: and a timing strip that grows bit by bit.

he: לוחצים 1, 0, 1 : המצב הנוכחי מודגש,
he: והרצועה מראה din, state ו-found.
en: Click 1, 0, 1: the current state is highlighted,
en: and the strip shows din, state and found.

he: עוד 1 : המעבר 1 / 1 נלקח,
he: ו-found עולה במחזור 4.
en: Another 1: the edge 1 / 1 is taken,
en: and found rises in cycle 4.

he: ‏0 ו-1 מחזירים את המכונה ל-S3.
en: 0 and 1 bring the machine back to S3.

he: וה-1 האחרון : זיהוי שני, במחזור 7.
en: And the last 1: a second match, in cycle 7.

he: עכשיו נכתוב את המודול ב-SystemVerilog.
en: Now let's write the module in SystemVerilog.

he: המודול : שעון, איפוס שפעיל ב-0,
he: ביט הקלט din והמוצא found.
en: The module: a clock, an active-low reset,
en: the input bit din and the output found.

he: ארבעה מצבים, בשמות של מה שכבר נראה.
he: שני ביטים מספיקים לארבעה.
en: Four states, named after what was seen so far.
en: Two bits are enough for four.

he: בקוד S10 הוא S2 מהגרף,
he: ו-S101 הוא S3.
en: In the code S10 is S2 of the graph,
en: and S101 is S3.

he: לוגיקה צירופית. ברירת המחדל :
he: המצב לא משתנה, והמוצא 0.
en: Combinational logic. The defaults:
en: the state does not change, and the output is 0.

he: ‏case על המצב : המעברים של S0,
he: של S1 ושל S10, לפי din.
en: A case on the state: the edges of S0,
en: S1 and S10, by din.

he: ב-S101 : found = din. זה ה-Mealy,
he: הפלט תלוי גם בביט שנכנס.
en: In S101: found = din. That is the Mealy part,
en: the output also depends on the incoming bit.

he: ואחר כך : עם 1 ל-S1, בשביל החפיפה,
he: ועם 0 ל-S10.
en: Then: on 1 to S1, for the overlap,
en: and on 0 to S10.

he: הפלופים : באיפוס חוזרים ל-S0,
he: ובכל עליית שעון state מקבל את next.
en: The flip-flops: reset goes back to S0,
en: and on every clock edge state takes next.

he: נעבור על הקוד לצד התיבה,
he: על אותו זרם 1011011.
en: Let's walk the code beside the box,
en: on the same stream 1011011.

he: אחרי האיפוס המצב S0, ועוד לא הגיע ביט.
en: After the reset the state is S0, and no bit came yet.

he: מחזור 1, din = 1 : ב-S0 השורה הזו
he: בוחרת next = S1.
en: Cycle 1, din = 1: in S0 this line
en: chooses next = S1.

he: מחזור 2, din = 0 : מ-S1 ל-S10.
en: Cycle 2, din = 0: from S1 to S10.

he: מחזור 3, din = 1 : מ-S10 ל-S101.
en: Cycle 3, din = 1: from S10 to S101.

he: מחזור 4, din = 1 : ב-S101 found = din,
he: כלומר 1. והמצב הבא S1.
en: Cycle 4, din = 1: in S101 found = din,
en: that is 1. And the next state is S1.

he: בעליית השעון state מקבל את next :
he: המכונה ב-S1, מוכנה לחפיפה.
en: On the clock edge state takes next:
en: the machine is in S1, ready for the overlap.

he: מחזורים 5 ו-6 : ‏0 ואחריו 1,
he: ושוב מגיעים ל-S101.
en: Cycles 5 and 6: 0 then 1,
en: and we reach S101 again.

he: מחזור 7 : שוב found = 1,
he: באותו מחזור שבו ה-1 על הקו.
en: Cycle 7: found = 1 again,
en: in the same cycle the 1 is on the wire.

he: נבנה את דיאגרמת התזמון, מחזור אחרי מחזור.
he: במחזור 0, אחרי האיפוס, המצב S0.
en: Let's build the timing diagram, cycle by cycle.
en: In cycle 0, after the reset, the state is S0.

he: בכל עליית שעון הפלופים שומרים את next.
he: אחרי 1, 0, 1 הם מחזיקים S101.
en: On every rising edge the flip-flops store next.
en: After 1, 0, 1 they hold S101.

he: במחזור 4 המצב S101 ו-din = 1 :
he: ‏found עולה מיד, באותו מחזור.
en: In cycle 4 the state is S101 and din = 1:
en: found rises at once, in the same cycle.

he: בעלייה הבאה המצב S1, ו-found יורד.
he: מחזורים 5 ו-6 מביאים שוב ל-S101.
en: On the next edge the state is S1, and found falls.
en: Cycles 5 and 6 bring it back to S101.

he: ובמחזור 7 found עולה שוב.
he: זו בדיוק דיאגרמת התזמון שבעמוד.
en: And in cycle 7 found rises again.
en: This is exactly the timing diagram on the page.

he: העלות : שני פלופים לארבעה מצבים, ושער אחד
he: מ-din ל-found. בלי רגיסטר הזזה ומשווה.
en: The cost: two flip-flops for four states, one gate
en: from din to found. No shift register or comparator.

he: מלכודת : לחזור ל-S0 בכל ביט שלא מתאים.
he: נבדוק את הזרם 101011.
en: Trap: going back to S0 on every bit that does not match.
en: Let's check the stream 101011.

he: אחרי 1010 הגלאי הזה כבר ב-S0, ו-11
he: לא מספיקים לו : במחזור 6 אין זיהוי.
en: After 1010 this detector is already in S0, and 11
en: is not enough: no match in cycle 6.

he: המכונה הנכונה עוברת ל-S2 אחרי 1010,
he: כי 10 עוד יכול לפתוח זיהוי, ומזהה במחזור 6.
en: The right machine goes to S2 after 1010,
en: since 10 can still start a match, and detects in cycle 6.

he: סעיף ב : בונים את המכונה לכל תבנית,
he: בלי לחשוב על כל מקרה ביד.
en: Part B: build the machine for any pattern,
en: without working out each case by hand.

he: ניקח תבנית אחרת, 10101. המצב s אומר :
he: ה-s הביטים האחרונים הם ה-s הראשונים שלה.
en: Take another pattern, 10101. The state s means:
en: the last s bits are its first s bits.

he: ב-S3 ראינו 101, ומגיע 1.
he: הקלט מסתיים עכשיו ב-1011.
en: In S3 we saw 101, and a 1 arrives.
en: The input now ends in 1011.

he: מזיזים את התבנית מתחת לקלט. בלי הזזה
he: הביט הרביעי לא מתאים : 1 מול 0.
en: Slide the pattern under the input. With no shift
en: the fourth bit does not match: 1 against 0.

he: מזיזים צעד אחרי צעד, עד שסוף הקלט
he: מתחיל את התבנית.
en: Shift step by step, until the end of the input
en: starts the pattern.

he: ביט אחד מתאים : המצב הבא S1.
he: זו הסיומת הארוכה ביותר שהיא גם התחלה.
en: One bit matches: the next state is S1.
en: That is the longest suffix that is also a prefix.

he: אין צורך להזיז ביד. ‏fail(s) הוא המצב
he: של אותה סיומת, בלי הביט הראשון שלה.
en: No need to slide by hand. fail(s) is the state
en: of the same suffix, without its first bit.

he: ואת fail של המצב הבא מחשבים
he: מאותה טבלה, בשורה אחת.
en: And the next state's fail is computed
en: from the same table, in one line.

he: נבנה את הטבלה של 10101, שורה אחרי שורה.
he: בכתום : המעברים שמתקדמים.
en: Let's build the table of 10101, row by row.
en: In amber: the edges that move forward.

he: מצב 1 : 0 מתקדם, ו-1 הולך לאן שהולך
he: מצב הכישלון 0 עם 1. מצב 2 באותה דרך.
en: State 1: 0 moves forward, and 1 goes where
en: the fail state 0 goes on 1. State 2 likewise.

he: מצב 3 : 0 מתקדם, ו-1 כמו ממצב 1.
he: מצב 4 : 1 משלים את התבנית.
en: State 3: 0 moves forward, and 1 as from state 1.
en: State 4: 1 completes the pattern.

he: המצב המלא 5 מתנהג כמו מצב 3 :
he: ‏101 הוא גם סוף וגם התחלה של 10101.
en: The full state 5 behaves like state 3:
en: 101 is both an end and a start of 10101.

he: בעמוד, הפונקציה next_state בונה
he: בדיוק את הטבלה הזו, בלולאה אחת.
en: On the page, the function next_state builds
en: exactly this table, in one loop.

he: בכל שורה : התקדמות על התאמה,
he: אחרת המעבר של מצב הכישלון.
en: Each row: advance on a match,
en: otherwise the edge of the fail state.

he: ושורה אחת מעדכנת את fail
he: למצב הבא, מאותה טבלה.
en: And one line updates fail
en: for the next state, from the same table.

he: בתיבה מקלידים תבנית, והגרף נבנה לבד.
he: מתחתיו : איך נבנה כל מעבר.
en: In the box you type a pattern, and the graph builds itself.
en: Below it: how each edge is built.

he: אחרי 1, 0, 1 המכונה ב-S3,
he: והתבנית מוזזת לשני הביטים הבאים.
en: After 1, 0, 1 the machine is in S3,
en: and the pattern is slid for both next bits.

he: ‏0 מתקדם ל-S4. עכשיו 1
he: ישלים את התבנית.
en: 0 moves on to S4. Now a 1
en: will complete the pattern.

he: ‏1 משלים את 10101 : הפלט 1,
he: וממשיכים מ-S3, לא מההתחלה.
en: 1 completes 10101: the output is 1,
en: and we continue from S3, not from the start.

he: ‏Mealy מול Moore. ב-Moore הפלט שייך למצב,
he: ולכן צריך מצב חמישי, S4, שמוציא 1.
en: Mealy against Moore. In Moore the output is the state's,
en: so a fifth state, S4, outputs 1.

he: מ-S4 : ‏0 ל-S2 ו-1 ל-S1, בדיוק כמו מ-S3
he: ב-Mealy. לכן Mealy מסתפק בארבעה.
en: From S4: 0 to S2 and 1 to S1, as from S3
en: in Mealy. So Mealy makes do with four.

he: על 1011011 : ‏Mealy מוציא 1 במחזורים 4 ו-7,
he: ו-Moore מחזור אחד אחריו, ב-5 וב-8.
en: On 1011011: Mealy outputs 1 in cycles 4 and 7,
en: and Moore one cycle later, in 5 and 8.

he: ‏Moore : מצב אחד יותר ומחזור אחד מאוחר,
he: אבל המוצא רשום ונקי מגליצ'ים.
en: Moore: one more state and one cycle later,
en: but the output is registered and free of glitches.

he: בתיבה : אותו זרם ב-Mealy,
he: ו-found עולה במחזורים 4 ו-7.
en: In the box: the same stream in Mealy,
en: and found rises in cycles 4 and 7.

he: עוברים ל-Moore : חמישה מצבים,
he: ו-found זז מחזור אחד ימינה.
en: Switch to Moore: five states,
en: and found moves one cycle to the right.

he: העלות : לוג של L + 1 פלופים,
he: ומעבר אחד בטבלה לכל ביט.
en: The cost: log of L + 1 flip-flops,
en: and one table lookup per bit.

he: לסיכום : ארבעה מצבים לפי מה שכבר נראה,
he: ובנייה שיטתית לכל תבנית.
en: To sum up: four states by what was already seen,
en: and a systematic build for any pattern.

he: נסו תבניות משלכם בתיבה
he: שבעמוד של שאלה 0040 באתר.
en: Try your own patterns in the box
en: on the page of question 0040 on the site.
