# 0001 — the rising edge detector: the video script

The storyboard of the video: the captions of every beat (Hebrew, a `> ` line per caption
line, a blank line between captions), in the order the video shows them. The captions are
exactly what the video shows; `videos/render.py` fails when scene.py's captions differ.

One part, on the page's `sig` (0 0 1 1 1 1 0 0 1 1): the problem and why a combinational circuit cannot tell "rose now" from "high for long"; the circuit drawn in Manim (a D flip-flop, NOT and AND, `pulse = sig & ~sig_q`); the timing diagram built cycle by cycle under the circuit, the flip-flop showing the `sig` it remembers; the page's WaveDrom diagram whole (`wave_shot.py`); the page's edge box drawn click by click (`BOXES['draw']`), with the reset trap and the falling and any-edge follow-ups; the SystemVerilog module typed (the answer is hardware, as in 0011) and walked beside the box; the cost and the page's two traps (`@(posedge sig)`, an asynchronous `sig`).

## Opening

> שאלה 0001 : גלאי עליית שפה,
> שאלה ברמת סטודנט.

> סעיף אחד : לשרטט את המעגל, לכתוב אותו
> ב-SystemVerilog, ולצייר דיאגרמת תזמון.

> נתון אות sig שמסונכרן לשעון clk.
> מה צריך להיות בתוך הקופסה?

## Chapter גלאי עליית שפה – מעגל, קוד ותזמון

> המטרה : פולס ברוחב מחזור שעון אחד
> בכל פעם ש-sig עולה מ-0 ל-1.

> הנה sig מהדיאגרמה שבעמוד,
> עשרה מחזורים של השעון.

> ‏sig עולה פעמיים, ולכן רוצים שני פולסים,
> כל אחד ברוחב מחזור אחד בדיוק.

> גם כש-sig נשאר גבוה ארבעה מחזורים,
> הפולס לא מתארך.

> מעגל צירופי רואה רק את sig של עכשיו.
> במחזור 2 ובמחזור 4 הוא רואה 1.

> ההבדל הוא במחזור הקודם : לפני מחזור 2
> ‏sig היה 0, ולפני מחזור 4 הוא היה 1.

> שינוי הוא השוואה בין שני מחזורים,
> ולכן המעגל צריך לזכור את sig הקודם.

> את הערך הקודם זוכר Flip-Flop מסוג D :
> בכל עליית שעון הוא דוגם את sig.

> המוצא שלו, sig_q, הוא הערך של sig
> במחזור הקודם.

> עליית שפה : עכשיו 1, וקודם 0.
> כלומר sig, וגם ההיפוך של sig_q.

> המוצא : pulse = sig & ~sig_q.
> זה כל המעגל : זיכרון אחד ושני שערים.

> עכשיו נבנה את דיאגרמת התזמון,
> מחזור אחרי מחזור, עם אותו sig.

> במחזורים 0 ו-1 sig נמוך. האיפוס
> מתחיל את sig_q ב-0, וגם pulse הוא 0.

> במחזור 2 sig עולה. ה-Flip-Flop עדיין
> זוכר 0, ולכן pulse = 1 & ~0 = 1.

> בעליית השעון הבאה sig_q תופס את ה-1,
> ו-~sig_q = 0 מאפס את pulse.

> במחזורים 4 ו-5 sig עדיין גבוה,
> אבל גם sig_q : הפולס לא מתארך.

> במחזור 6 sig יורד, וה-AND מתאפס מיד :
> ירידה לא מייצרת פולס.

> במחזור 7 גם sig_q יורד ל-0,
> מחזור אחד אחרי sig.

> במחזור 8 sig עולה שוב. ‏sig_q הוא 0,
> ולכן יוצא פולס שני.

> ובמחזור 9 sig_q תופס את ה-1,
> והפולס נגמר אחרי מחזור אחד.

> ‏sig_q הוא העתק של sig, מאוחר במחזור אחד.
> הפולס : המחזורים שבהם sig = 1 ו-sig_q = 0.

> וזו הדיאגרמה שבעמוד, ב-WaveDrom :
> אותם ארבעה אותות, אותם מחזורים.

> בתיבה שבעמוד מציירים את sig בלחיצות,
> והמעגל מצייר את sig_q ואת pulse.

> לוחצים על מחזור 2 : sig עולה,
> ו-pulse גבוה במחזור 2 בלבד.

> מחזור 3 : sig עדיין גבוה, אבל sig_q כבר 1,
> ולכן אין פולס.

> גם עם מחזורים 4 ו-5 :
> פולס אחד, ברוחב מחזור אחד.

> עלייה שנייה במחזור 8 :
> עוד פולס, שוב מחזור אחד.

> ומחזור 9 משלים את הדיאגרמה שבעמוד.

> המלכודת של האיפוס : sig כבר גבוה
> כשהאיפוס משתחרר, במחזור 0.

> ‏sig_q מתחיל מ-0, ולכן יוצא פולס
> במחזור 0, בלי עליית שפה.

> אם זה לא רצוי, מאפסים את sig_q ל-1,
> או מסננים את המחזור הראשון.

> שאלת המשך : ירידת שפה היא ~sig & sig_q,
> עכשיו 0 וקודם 1.

> וכל שינוי, עלייה או ירידה,
> הוא sig ^ sig_q.

> עכשיו נכתוב את זה ב-SystemVerilog.

> המודול rise_detect : שעון, איפוס בפעיל נמוך,
> הכניסה sig והמוצא pulse.

> ‏sig_q : כל הזיכרון של המעגל,
> ביט אחד, ה-sig של המחזור הקודם.

> ‏always_ff : לוגיקה רשומה, שמתעדכנת
> בעליית clk או בירידה של rst_n.

> באיפוס sig_q מתאפס ל-0,
> ובכל מחזור אחר הוא דוגם את sig.

> ‏assign : המוצא צירופי,
> בדיוק pulse = sig & ~sig_q.

> וזה כל המודול : Flip-Flop אחד,
> שער NOT ושער AND.

> נעבור על הקוד לצד התיבה,
> מהדיאגרמה הריקה.

> במחזור 2 sig = 1 ו-sig_q = 0,
> ולכן ה-assign מוציא pulse = 1.

> בעליית השעון הבאה : sig_q <= sig.
> עכשיו sig_q = 1.

> ה-assign מחשב מחדש : ~sig_q = 0,
> ו-pulse יורד אחרי מחזור אחד.

> כל עוד sig גבוה, sig_q נשאר 1
> והפולס לא חוזר.

> ובאיפוס sig_q <= 0 גם כש-sig כבר גבוה :
> זה הפולס של המלכודת.

> העלות : Flip-Flop אחד ושני שערים.
> מהכניסה sig למוצא יש שער אחד בלבד.

> לכן המעגל לא מגביל את תדר השעון,
> ואין בו מונה או מכונת מצבים.

> מלכודת : לזהות שפה עם always @(posedge sig).
> זה הופך את sig לשעון נוסף.

> אין ממנו דרך פשוטה לפולס ברוחב מחזור
> של clk. במקום זה דוגמים את sig עם clk.

> מלכודת : sig שמגיע מדומיין שעון אחר.
> קודם מסנכרנים אותו בשני Flip-Flops,

> ורק אז מזהים את השפה. אחרת metastability
> עלול לייצר פולסים כפולים או חסרים.

## Closing

> לסיכום : Flip-Flop אחד זוכר את sig,
> ו-pulse = sig & ~sig_q.

> נסו לצייר את sig בעצמכם בתיבה
> שבעמוד של שאלה 0001 באתר.
