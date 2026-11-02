# 0009 — 16 people, 16 boxes and one helper: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0009 : ‏16 אנשים, 16 קופסאות
he: ועוזר אחד. רמת ג'וניור.
en: Question 0009: 16 people, 16 boxes
en: and one helper. Junior level.

he: שני סעיפים : האסטרטגיה,
he: ואז הקוד שמממש אותה.
en: Two parts: the strategy,
en: then the code that carries it out.

he: בחדר 16 קופסאות, ובכל אחת פתק עם
he: מספר מ-1 עד 16, כל מספר פעם אחת.
en: A room with 16 boxes, each holding a note
en: with a number from 1 to 16, each number once.

he: המספר הקטן הוא הקופסה, והגדול
he: הוא הפתק שבתוכה : בקופסה 1 הפתק 6.
en: The small number is the box, the big one
en: is the note inside: box 1 holds note 6.

he: אדם 0 נכנס ראשון : מציץ בכל הקופסאות,
he: ומחליף פתקים עד 4 פעמים.
en: Person 0 goes in first: he looks into every box
en: and may swap notes up to 4 times.

he: אחריו אנשים 1 עד 16, אחד אחד : כל
he: אחד פותח עד 8 קופסאות, בלי להזיז.
en: Then persons 1 to 16, one at a time:
en: each opens up to 8 boxes, moving nothing.

he: המטרה : כולם צריכים למצוא את הפתק
he: שלהם. אם אחד נכשל, כולם מפסידים.
en: The goal: everybody must find their own note.
en: If one fails, everybody loses.

he: סעיף א : איזו אסטרטגיה מבטיחה
he: שכולם ינצחו, בכל סידור של הפתקים?
en: Part A: which strategy guarantees
en: that everybody wins, for any arrangement?

he: הרעיון : כל אדם פותח קודם את
he: הקופסה עם המספר שלו.
en: The idea: every person first opens
en: the box with his own number.

he: ואז את הקופסה שהמספר שלה כתוב
he: על הפתק שמצא, וכן הלאה.
en: Then the box whose number is written
en: on the note he found, and so on.

he: נעקוב אחרי אדם 1 : קופסה 1, בה פתק 6,
he: ואז 11, 3, 14, 9, 16 ו-4.
en: Let's follow person 1: box 1 holds note 6,
en: then 11, 3, 14, 9, 16 and 4.

he: ‏8 פתיחות נגמרו, והפתק 1 עוד לא נמצא.
he: הוא בקופסה 8, ה-16 בשרשרת.
en: 8 opens are used up and note 1 is still missing.
en: It is in box 8, the 16th in the chain.

he: אם ממשיכים מכל קופסה לפי הפתקים,
he: החצים תמיד נסגרים למעגלים.
en: Following the notes from any box,
en: the arrows always close into cycles.

he: כאן כל 16 הקופסאות על מעגל אחד :
he: קופסה 1 שולחת ל-6, ‏6 ל-11, וכן הלאה.
en: Here all 16 boxes are on one cycle:
en: box 1 points to 6, 6 to 11, and so on.

he: למה מעגלים? מכל קופסה יוצא חץ אחד,
he: ואליה נכנס חץ אחד : כל פתק פעם אחת.
en: Why cycles? One arrow leaves each box
en: and one enters it: every note appears once.

he: אדם i מתחיל בקופסה i, ולכן
he: הוא הולך על המעגל שלה.
en: Person i starts at box i,
en: so he walks along that box's cycle.

he: הפתק i נמצא בקופסה שמצביעה חזרה
he: לקופסה i : האחרונה במעגל.
en: Note i is in the box that points back
en: to box i: the last one on the cycle.

he: לכן מי שעל מעגל באורך L מוצא את
he: הפתק שלו בדיוק בפתיחה ה-L.
en: So whoever is on a cycle of length L finds
en: his note at exactly the L-th open.

he: מעגל עד 8 : כולם בו מצליחים.
he: כאן L = 16 : כל 16 האנשים נכשלים.
en: A cycle of up to 8: everybody on it succeeds.
en: Here L = 16: all 16 people fail.

he: בלי אדם 0 זה קורה הרבה : האסטרטגיה
he: מצליחה רק בכשליש מהסידורים.
en: Without person 0 this happens a lot: the strategy
en: succeeds in only about a third of arrangements.

he: ובחירה אקראית של 8 קופסאות גרועה
he: בהרבה : כמעט אף פעם.
en: And opening 8 random boxes is far worse:
en: it almost never works.

he: כאן נכנס אדם 0. הוא רואה את כל
he: הקופסאות, ולכן רואה את המעגל.
en: Now person 0 comes in. He sees every box,
en: so he sees the cycle.

he: הוא מחליף בין הפתק של קופסה 1,
he: תחילת המעגל, לפתק של קופסה 12, באמצע.
en: He swaps the note of box 1, the start of the cycle,
en: with the note of box 12, in the middle.

he: פתק 6 עובר לקופסה 12,
he: ופתק 7 עובר לקופסה 1.
en: Note 6 moves to box 12,
en: and note 7 moves to box 1.

he: רק שני חצים משתנים, והמעגל מתפצל
he: לשני מעגלים, כל אחד באורך 8.
en: Only two arrows change, and the cycle splits
en: into two cycles, each of length 8.

he: אדם 1 עכשיו : ‏1, 7, 2, 15, 5, 10, 13 ו-8.
he: בפתיחה השמינית הפתק שלו.
en: Person 1 now: 1, 7, 2, 15, 5, 10, 13 and 8.
en: His note is at the eighth open.

he: כך כל אחד מוצא את הפתק שלו בדיוק
he: בפתיחה ה-8 : כולם מנצחים.
en: So everybody finds his note at exactly
en: the 8th open: everybody wins.

he: למה זה עובד בכל סידור? עובדה ראשונה :
he: יש לכל היותר מעגל ארוך אחד.
en: Why does it work for any arrangement? First fact:
en: there is at most one long cycle.

he: סכום אורכי המעגלים הוא 16, ושני
he: מעגלים מעל 8 כבר צריכים 18 קופסאות.
en: The cycle lengths add up to 16, and two cycles
en: over 8 would already need 18 boxes.

he: עובדה שנייה : החלפה בין הפתקים של c0
he: ושל ch חותכת את המעגל לשני מעגלים.
en: Second fact: swapping the notes of c0
en: and ch cuts the cycle into two cycles.

he: אחד באורך L − h, והשני באורך h.
en: One of length L − h, the other of length h.

he: בוחרים את האמצע, h = ⌊L/2⌋. כי L ≤ 16,
he: שני החלקים באורך 8 לכל היותר.
en: Choose the middle, h = ⌊L/2⌋. Since L ≤ 16,
en: both pieces have length 8 at most.

he: לכן החלפה אחת תמיד מספיקה,
he: ושלוש ההחלפות הנוספות מיותרות.
en: So one swap is always enough,
en: and the other three swaps are not needed.

he: סידור שני, הדוגמה מהעמוד :
he: הפתקים בקופסאות 1 עד 16.
en: A second arrangement, the page's example:
en: the notes in boxes 1 to 16.

he: בעקבות החצים יש שלושה מעגלים :
he: באורך 11, באורך 3 ובאורך 2.
en: Following the arrows gives three cycles:
en: of lengths 11, 3 and 2.

he: אדם 13 על המעגל הארוך : ‏13, 1, 7, 12,
he: ‏3, 15, 9 ו-4. נגמרו 8 פתיחות.
en: Person 13 is on the long cycle: 13, 1, 7, 12,
en: 3, 15, 9 and 4. 8 opens are used up.

he: הפתק 13 בקופסה 5,
he: ה-11 במעגל : רחוק מדי.
en: Note 13 is in box 5,
en: the 11th on the cycle: too far.

he: אדם 0 מחליף בין קופסה 1 לקופסה 9 :
he: הן c0 ו-c5, כי ⌊11/2⌋ = 5.
en: Person 0 swaps box 1 and box 9:
en: they are c0 and c5, since ⌊11/2⌋ = 5.

he: פתק 7 עובר לקופסה 9, ופתק 4 לקופסה 1.
he: המעגל של 11 מתפצל ל-6 ול-5.
en: Note 7 moves to box 9, and note 4 to box 1.
en: The cycle of 11 splits into 6 and 5.

he: ועכשיו אדם 13 : ‏13, 1, 4, 16, 10 ו-5.
he: בקופסה 5 הפתק שלו, בפתיחה השישית.
en: And now person 13: 13, 1, 4, 16, 10 and 5.
en: Box 5 holds his note, at the sixth open.

he: כך כל 16 האנשים : לכל אחד
he: מספיקות 6 פתיחות לכל היותר.
en: And so for all 16 people: each of them
en: needs 6 opens at most.

he: בתיבה שבעמוד אותו סידור. החצים
he: המקווקווים הם ההחלפה של אדם 0.
en: The page's box has the same arrangement. The dashed
en: arrows are person 0's swap.

he: בכל לחיצה אדם 13 פותח קופסה :
he: קודם קופסה 13, ובה הפתק 1.
en: With each click person 13 opens a box:
en: first box 13, which holds note 1.

he: ממשיך לפי הפתקים :
he: קופסה 1, ואז קופסה 4.
en: He follows the notes:
en: box 1, then box 4.

he: ובפתיחה השישית, בקופסה 5,
he: הוא מוצא את הפתק שלו.
en: And at the sixth open, in box 5,
en: he finds his note.

he: בלי אדם 0 המעגל של 11 חוזר באדום,
he: ואדם 13 נכשל אחרי 8 פתיחות.
en: Without person 0 the cycle of 11 is red again,
en: and person 13 fails after 8 opens.

he: סעיף ב : לממש את החדר עם המגבלות,
he: את אדם 0, את כל השאר ומשחק שלם.
en: Part B: implement the room with its limits,
en: person 0, everybody else, and a whole game.

he: קודם החדר, בקצרה ובלי להקליד :
he: המחלקה Room שאוכפת את הכללים.
en: First the room, briefly and not typed:
en: the class Room that enforces the rules.

he: המגבלות : 8 פתיחות ו-4 החלפות. החדר
he: שומר עותק פרטי של הפתקים.
en: The limits: 8 opens and 4 swaps.
en: The room keeps a private copy of the notes.

he: ‏look_all ו-swap רק לאדם 0, לפני
he: שמישהו נכנס, ועד 4 החלפות.
en: look_all and swap only for person 0, before
en: anybody else enters, and up to 4 swaps.

he: ‏enter נותן לכל נכנס 8 פתיחות, ו-open_box
he: סופרת אותן : הכללים נאכפים בחדר.
en: enter gives everyone who enters 8 opens, and open_box
en: counts them: the room enforces the rules.

he: עכשיו האסטרטגיה. קודם פונקציית עזר,
he: משותפת לאדם 0 ולכל השאר.
en: Now the strategy. First a helper function,
en: shared by person 0 and everybody else.

he: ‏cycle_from מקבלת את הפתקים
he: וקופסת התחלה.
en: cycle_from takes the notes
en: and a starting box.

he: מתחילים רשימה עם קופסת ההתחלה,
he: ועוברים לקופסה שהפתק שלה מראה.
en: Start a list with the starting box,
en: and move to the box its note names.

he: כל עוד לא חזרנו להתחלה : מוסיפים
he: את הקופסה, והולכים לפי הפתק שבה.
en: Until we are back at the start: add the box,
en: and follow its note.

he: בסוף מחזירים את כל המעגל.
en: At the end, return the whole cycle.

he: בדוגמה מהעמוד, מקופסה 2 :
he: ‏2, 11, 6, וחזרה ל-2.
en: In the page's example, from box 2:
en: 2, 11, 6, and back to 2.

he: אדם 0 הוא הפונקציה helper,
he: שמקבלת את החדר.
en: Person 0 is the function helper,
en: which takes the room.

he: הוא קורא את כל הפתקים בבת אחת,
he: וזוכר באילו קופסאות כבר ביקר.
en: He reads all the notes at once,
en: and remembers which boxes he has visited.

he: עובר על הקופסאות, מדלג על מי שכבר
he: במעגל, ומוצא את המעגל של כל קופסה חדשה.
en: He goes over the boxes, skips those already on a cycle,
en: and finds the cycle of each new box.

he: מעגל ארוך מ-8 : החלפה בין הראשונה
he: לאמצעית, ויציאה. אין מעגל ארוך שני.
en: A cycle longer than 8: swap the first and the middle,
en: and leave. There is no second long cycle.

he: נריץ את אדם 0 על הדוגמה מהעמוד.
en: Let's run person 0 on the page's example.

he: המעגל של קופסה 1 הוא המעגל הארוך,
he: עם 11 קופסאות.
en: The cycle of box 1 is the long cycle,
en: with 11 boxes.

he: ‏11 ארוך מ-8 : מחליף בין cycle[0] = 1
he: ל-cycle[5] = 9, ויוצא. החלפה אחת.
en: 11 is longer than 8: he swaps cycle[0] = 1
en: and cycle[5] = 9, and leaves. One swap.

he: כל אחד מהאחרים הוא find_my_note :
he: מקבל את החדר ואת המספר שלו.
en: Everybody else is find_my_note:
en: it takes the room and his own number.

he: נכנס, ומתחיל בקופסה שלו : כך הוא
he: בטוח על המעגל של הפתק שלו.
en: Enter, and start at your own box: that way
en: you are on the cycle of your note.

he: עד 8 פעמים פותח קופסה,
he: ואם הפתק שלו, הוא מצא.
en: Up to 8 times, open a box,
en: and if the note is yours, you found it.

he: אחרת עובר לקופסה שעל הפתק. אחרי
he: ‏8 פתיחות בלי הפתק : נכשל.
en: Otherwise move to the box on the note. After
en: 8 opens without the note: failed.

he: אדם 13, אחרי ההחלפה של אדם 0.
en: Person 13, after person 0's swap.

he: הוא מתחיל בקופסה 13, ובה הפתק 1 :
he: לא שלו, ולכן עובר לקופסה 1.
en: He starts at box 13, which holds note 1:
en: not his, so he moves to box 1.

he: אחר כך קופסאות 1, 4, 16 ו-10,
he: עם הפתקים 4, 16, 10 ו-5.
en: Then boxes 1, 4, 16 and 10,
en: with notes 4, 16, 10 and 5.

he: בקופסה 5 הפתק 13 : הוא מצא,
he: בפתיחה השישית.
en: Box 5 holds note 13: he found it,
en: at the sixth open.

he: ‏play בונה חדר, מריץ את אדם 0, ואז
he: את כולם, ובודק שכל 16 מצאו.
en: play builds a room, runs person 0, then
en: everybody else, and checks that all 16 found theirs.

he: הקוד נבדק על 231 מבני המעגלים
he: ועל 20,000 סידורים אקראיים.
en: The code was tested on all 231 cycle structures
en: and on 20,000 random arrangements.

he: בכולם כל 16 האנשים ניצחו,
he: עם החלפה אחת לכל היותר.
en: In all of them all 16 people won,
en: with at most one swap.

he: הסיבוכיות : אדם 0 בזמן ובזיכרון O(N),
he: וכל אחד מהאחרים בזיכרון O(1).
en: The cost: person 0 takes O(N) time and memory,
en: and each of the others O(1) memory.

he: לסיכום : הפתקים יוצרים מעגלים, ואדם 0
he: חותך את המעגל הארוך בהחלפה אחת.
en: To sum up: the notes form cycles, and person 0
en: cuts the long cycle with one swap.

he: נסו סידורים משלכם בתיבה שבעמוד
he: של שאלה 0009 באתר.
en: Try your own arrangements in the box
en: on the page of question 0009 on the site.
