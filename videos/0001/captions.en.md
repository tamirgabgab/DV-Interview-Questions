# 0001 — the rising edge detector: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); notes/VIDEOS.md.

he: שאלה 0001 : גלאי עליית שפה,
he: שאלה ברמת סטודנט.
en: Question 0001: a rising edge detector,
en: a student-level question.

he: סעיף אחד : לשרטט את המעגל, לכתוב אותו
he: ב-SystemVerilog, ולצייר דיאגרמת תזמון.
en: One part: draw the circuit, write it
en: in SystemVerilog, and draw a timing diagram.

he: נתון אות sig שמסונכרן לשעון clk.
he: מה צריך להיות בתוך הקופסה?
en: A signal sig is synchronous to a clock clk.
en: What goes inside the box?

he: המטרה : פולס ברוחב מחזור שעון אחד
he: בכל פעם ש-sig עולה מ-0 ל-1.
en: The goal: a pulse one clock cycle wide
en: each time sig rises from 0 to 1.

he: הנה sig מהדיאגרמה שבעמוד,
he: עשרה מחזורים של השעון.
en: Here is sig from the page's diagram,
en: ten cycles of the clock.

he: ‏sig עולה פעמיים, ולכן רוצים שני פולסים,
he: כל אחד ברוחב מחזור אחד בדיוק.
en: sig rises twice, so we want two pulses,
en: each exactly one cycle wide.

he: גם כש-sig נשאר גבוה ארבעה מחזורים,
he: הפולס לא מתארך.
en: Even when sig stays high for four cycles,
en: the pulse does not stretch.

he: מעגל צירופי רואה רק את sig של עכשיו.
he: במחזור 2 ובמחזור 4 הוא רואה 1.
en: A combinational circuit sees only sig of now.
en: In cycle 2 and in cycle 4 it sees 1.

he: ההבדל הוא במחזור הקודם : לפני מחזור 2
he: ‏sig היה 0, ולפני מחזור 4 הוא היה 1.
en: The difference is the cycle before: before cycle 2
en: sig was 0, and before cycle 4 it was 1.

he: שינוי הוא השוואה בין שני מחזורים,
he: ולכן המעגל צריך לזכור את sig הקודם.
en: A change is a comparison of two cycles,
en: so the circuit must remember the last sig.

he: את הערך הקודם זוכר Flip-Flop מסוג D :
he: בכל עליית שעון הוא דוגם את sig.
en: A D flip-flop remembers the last value:
en: at every rising clock edge it samples sig.

he: המוצא שלו, sig_q, הוא הערך של sig
he: במחזור הקודם.
en: Its output, sig_q, is the value of sig
en: in the previous cycle.

he: עליית שפה : עכשיו 1, וקודם 0.
he: כלומר sig, וגם ההיפוך של sig_q.
en: A rising edge: 1 now, and 0 before.
en: That is sig, and the inverse of sig_q.

he: המוצא : pulse = sig & ~sig_q.
he: זה כל המעגל : זיכרון אחד ושני שערים.
en: The output: pulse = sig & ~sig_q.
en: That is the whole circuit: one memory, two gates.

he: עכשיו נבנה את דיאגרמת התזמון,
he: מחזור אחרי מחזור, עם אותו sig.
en: Now let's build the timing diagram,
en: cycle by cycle, with the same sig.

he: במחזורים 0 ו-1 sig נמוך. האיפוס
he: מתחיל את sig_q ב-0, וגם pulse הוא 0.
en: In cycles 0 and 1 sig is low. The reset
en: starts sig_q at 0, and pulse is 0 too.

he: במחזור 2 sig עולה. ה-Flip-Flop עדיין
he: זוכר 0, ולכן pulse = 1 & ~0 = 1.
en: In cycle 2 sig rises. The flip-flop still
en: remembers 0, so pulse = 1 & ~0 = 1.

he: בעליית השעון הבאה sig_q תופס את ה-1,
he: ו-~sig_q = 0 מאפס את pulse.
en: At the next clock edge sig_q catches the 1,
en: and ~sig_q = 0 clears pulse.

he: במחזורים 4 ו-5 sig עדיין גבוה,
he: אבל גם sig_q : הפולס לא מתארך.
en: In cycles 4 and 5 sig is still high,
en: but so is sig_q: the pulse does not stretch.

he: במחזור 6 sig יורד, וה-AND מתאפס מיד :
he: ירידה לא מייצרת פולס.
en: In cycle 6 sig falls, and the AND clears at once:
en: a falling edge makes no pulse.

he: במחזור 7 גם sig_q יורד ל-0,
he: מחזור אחד אחרי sig.
en: In cycle 7 sig_q falls to 0 as well,
en: one cycle after sig.

he: במחזור 8 sig עולה שוב. ‏sig_q הוא 0,
he: ולכן יוצא פולס שני.
en: In cycle 8 sig rises again. sig_q is 0,
en: so a second pulse comes out.

he: ובמחזור 9 sig_q תופס את ה-1,
he: והפולס נגמר אחרי מחזור אחד.
en: And in cycle 9 sig_q catches the 1,
en: and the pulse ends after one cycle.

he: ‏sig_q הוא העתק של sig, מאוחר במחזור אחד.
he: הפולס : המחזורים שבהם sig = 1 ו-sig_q = 0.
en: sig_q is a copy of sig, one cycle late.
en: The pulse: the cycles where sig = 1 and sig_q = 0.

he: וזו הדיאגרמה שבעמוד, ב-WaveDrom :
he: אותם ארבעה אותות, אותם מחזורים.
en: And this is the page's diagram, in WaveDrom:
en: the same four signals, the same cycles.

he: בתיבה שבעמוד מציירים את sig בלחיצות,
he: והמעגל מצייר את sig_q ואת pulse.
en: In the page's box you draw sig by clicking,
en: and the circuit draws sig_q and pulse.

he: לוחצים על מחזור 2 : sig עולה,
he: ו-pulse גבוה במחזור 2 בלבד.
en: Click cycle 2: sig rises,
en: and pulse is high in cycle 2 only.

he: מחזור 3 : sig עדיין גבוה, אבל sig_q כבר 1,
he: ולכן אין פולס.
en: Cycle 3: sig is still high, but sig_q is already 1,
en: so there is no pulse.

he: גם עם מחזורים 4 ו-5 :
he: פולס אחד, ברוחב מחזור אחד.
en: With cycles 4 and 5 as well:
en: one pulse, one cycle wide.

he: עלייה שנייה במחזור 8 :
he: עוד פולס, שוב מחזור אחד.
en: A second rise in cycle 8:
en: another pulse, again one cycle.

he: ומחזור 9 משלים את הדיאגרמה שבעמוד.
en: And cycle 9 completes the page's diagram.

he: המלכודת של האיפוס : sig כבר גבוה
he: כשהאיפוס משתחרר, במחזור 0.
en: The reset trap: sig is already high
en: when the reset is released, in cycle 0.

he: ‏sig_q מתחיל מ-0, ולכן יוצא פולס
he: במחזור 0, בלי עליית שפה.
en: sig_q starts at 0, so a pulse comes out
en: in cycle 0, with no rising edge.

he: אם זה לא רצוי, מאפסים את sig_q ל-1,
he: או מסננים את המחזור הראשון.
en: If that is not wanted, reset sig_q to 1,
en: or filter out the first cycle.

he: שאלת המשך : ירידת שפה היא ~sig & sig_q,
he: עכשיו 0 וקודם 1.
en: A follow-up: a falling edge is ~sig & sig_q,
en: 0 now and 1 before.

he: וכל שינוי, עלייה או ירידה,
he: הוא sig ^ sig_q.
en: And any change, rising or falling,
en: is sig ^ sig_q.

he: עכשיו נכתוב את זה ב-SystemVerilog.
en: Now let's write it in SystemVerilog.

he: המודול rise_detect : שעון, איפוס בפעיל נמוך,
he: הכניסה sig והמוצא pulse.
en: The module rise_detect: a clock, an active-low reset,
en: the input sig and the output pulse.

he: ‏sig_q : כל הזיכרון של המעגל,
he: ביט אחד, ה-sig של המחזור הקודם.
en: sig_q: all the memory of the circuit,
en: one bit, the sig of the previous cycle.

he: ‏always_ff : לוגיקה רשומה, שמתעדכנת
he: בעליית clk או בירידה של rst_n.
en: always_ff: registered logic, updated
en: on a rising clk or a falling rst_n.

he: באיפוס sig_q מתאפס ל-0,
he: ובכל מחזור אחר הוא דוגם את sig.
en: On reset sig_q is cleared to 0,
en: and in every other cycle it samples sig.

he: ‏assign : המוצא צירופי,
he: בדיוק pulse = sig & ~sig_q.
en: assign: the output is combinational,
en: exactly pulse = sig & ~sig_q.

he: וזה כל המודול : Flip-Flop אחד,
he: שער NOT ושער AND.
en: And that is the whole module: one flip-flop,
en: a NOT gate and an AND gate.

he: נעבור על הקוד לצד התיבה,
he: מהדיאגרמה הריקה.
en: Let's walk through the code beside the box,
en: from the empty diagram.

he: במחזור 2 sig = 1 ו-sig_q = 0,
he: ולכן ה-assign מוציא pulse = 1.
en: In cycle 2 sig = 1 and sig_q = 0,
en: so the assign drives pulse = 1.

he: בעליית השעון הבאה : sig_q <= sig.
he: עכשיו sig_q = 1.
en: At the next clock edge: sig_q <= sig.
en: Now sig_q = 1.

he: ה-assign מחשב מחדש : ~sig_q = 0,
he: ו-pulse יורד אחרי מחזור אחד.
en: The assign computes again: ~sig_q = 0,
en: and pulse falls after one cycle.

he: כל עוד sig גבוה, sig_q נשאר 1
he: והפולס לא חוזר.
en: As long as sig stays high, sig_q stays 1
en: and the pulse does not come back.

he: ובאיפוס sig_q <= 0 גם כש-sig כבר גבוה :
he: זה הפולס של המלכודת.
en: And on reset sig_q <= 0 even when sig is high:
en: that is the trap's pulse.

he: העלות : Flip-Flop אחד ושני שערים.
he: מהכניסה sig למוצא יש שער אחד בלבד.
en: The cost: one flip-flop and two gates.
en: From the input sig to the output: one gate.

he: לכן המעגל לא מגביל את תדר השעון,
he: ואין בו מונה או מכונת מצבים.
en: So the circuit does not limit the clock rate,
en: and it has no counter or state machine.

he: מלכודת : לזהות שפה עם always @(posedge sig).
he: זה הופך את sig לשעון נוסף.
en: A trap: detecting the edge with always @(posedge sig).
en: That turns sig into another clock.

he: אין ממנו דרך פשוטה לפולס ברוחב מחזור
he: של clk. במקום זה דוגמים את sig עם clk.
en: It gives no simple pulse one clk cycle wide.
en: Instead, sample sig with clk.

he: מלכודת : sig שמגיע מדומיין שעון אחר.
he: קודם מסנכרנים אותו בשני Flip-Flops,
en: A trap: sig coming from another clock domain.
en: First synchronize it with two flip-flops,

he: ורק אז מזהים את השפה. אחרת metastability
he: עלול לייצר פולסים כפולים או חסרים.
en: and only then detect the edge. Otherwise metastability
en: may make double or missing pulses.

he: לסיכום : Flip-Flop אחד זוכר את sig,
he: ו-pulse = sig & ~sig_q.
en: In short: one flip-flop remembers sig,
en: and pulse = sig & ~sig_q.

he: נסו לצייר את sig בעצמכם בתיבה
he: שבעמוד של שאלה 0001 באתר.
en: Try drawing sig yourself in the box
en: on the page of question 0001 on the site.
