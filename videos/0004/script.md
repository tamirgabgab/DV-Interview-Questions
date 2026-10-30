# 0004 — three mislabeled boxes: the video script

The storyboard of the video, beat by beat: the picture (English notes) and the caption
(Hebrew, a `> ` line per caption line, a blank line between captions). The captions are
exactly what the video shows; `videos/render.py` fails when scene.py's captions differ.

The example is the page's: the labels `RED, BLACK, MIXED` on boxes 0, 1, 2, and the true
contents of arrangement 1 (black, mixed, red), so the ball drawn from box 2 is red. The
code beats load the Python tab of the page (`fix_labels_simple`, `fix_labels`) and run it
with `draw()` returning the ball of the example; the lines are lit in the order the tracer
saw them run. The Hebrew words in the frame (the box labels, the chapter cards, the stamp)
are PNG labels drawn by the browser (`lib/he_label.py`).

## Opening

- The DV mark is drawn, the id `0004` beside it, the title and the level chip below.

> שאלה 0004 : שלוש קופסאות עם תוויות שגויות,
> שאלה ברמת ג'וניור.

- The two part chips.

> שני סעיפים : כמה דגימות צריך,
> ואיך כותבים את זה בקוד.

- Three wooden crates, each with a few balls of its true content visible above it.

> באחת הקופסאות רק כדורים אדומים, באחרת רק שחורים,
> ובשלישית גם וגם.

- The balls sink into the crates; the labels "אדום", "שחור", "אדום ושחור" appear on the
  fronts.

> על כל קופסה מודבקת תווית :
> אדום, שחור, ואדום ושחור.

- A red stamp "כל התוויות שגויות" lands over the crates.

> והחוק היחיד : כל התוויות שגויות.

## Chapter א – the minimum number of draws

- Chapter card: "סעיף א", "מספר הדגימות המינימלי".

> סעיף א : מהו המספר המינימלי של דגימות
> שמבטיח שנוכל לתקן את כל התוויות?

**The problem.** The three crates with their labels; a ball rises out of one of them.

> דגימה : מצביעים על קופסה,
> ומקבלים ממנה כדור אחד אקראי.

**The cases.** A table: a column per label, a row per way to fill the boxes; the content
drawn as balls (red, black, or one of each).

> יש שש דרכים לחלק את שלושת סוגי התוכן
> בין שלוש הקופסאות.

- Every cell whose content matches its column's label gets a red cross.

> אבל כל התוויות שגויות, ולכן נפסל
> כל סידור שבו תוכן תואם לתווית שלו.

- The four rows with a cross fade; two rows remain, numbered 1 and 2.

> נשארים רק שני סידורים אפשריים,
> וצריך להכריע ביניהם.

**The idea.** The columns are ringed one by one.

> בקופסה "אדום" יש שחור או תערובת.
> כדור שחור מתאים לשני הסידורים.

> בקופסה "שחור" יש תערובת או אדום,
> וכדור אדום מתאים לשניהם.

- The column "אדום ושחור" is ringed amber: red in one row, black in the other.

> רק בקופסה "אדום ושחור"
> שני הסידורים נבדלים בצבע אחד וברור.

> הרעיון : התווית "אדום ושחור" שגויה,
> ולכן בקופסה הזו יש צבע אחד בלבד.

**The steps.** The crates again. A red ball rises from the crate labelled "אדום ושחור"; its
true content (a red ball) is pinned under it.

> מקרה ראשון : מהקופסה "אדום ושחור" יוצא כדור אדום.
> זו הקופסה האדומה.

- The crate labelled "שחור" gets the mixed content.

> הקופסה "שחור" לא שחורה, כי התווית שגויה,
> וגם לא אדומה. לכן היא התערובת.

- The crate labelled "אדום" gets the black content.

> ולקופסה "אדום" נשאר השחור.

- Reset. A black ball rises from the same crate.

> מקרה שני : יוצא כדור שחור.
> אז זו הקופסה השחורה.

- The crate "אדום" gets the mix, the crate "שחור" the red.

> הקופסה "אדום" לא אדומה וגם לא שחורה,
> לכן היא התערובת, ול"שחור" נשאר האדום.

- The two remaining rows of the table, each with its deciding ball at its side.

> הכלל : יצא צבע c? הקופסה שתוויתה c
> מכילה את הצבע השני, והשלישית את התערובת.

**Why one is the minimum.** The two rows with question marks.

> ולמה לא אפס? בלי דגימה נשארים שני סידורים,
> ואין דרך לבחור ביניהם.

- The answer chip: `1 draw`.

> לכן התשובה : דגימה אחת,
> ודווקא מהקופסה "אדום ושחור".

**The trap.** A black ball rises from the crate labelled "אדום"; both rows stay lit, each
with a question mark.

> המלכודת : לדגום מהקופסה "אדום".
> כדור שחור משם משאיר את שני הסידורים פתוחים.

> אותו דבר בקופסה "שחור".
> רק "אדום ושחור" ידועה מראש כחד-צבעית.

## Chapter ב – the code

- Chapter card: "סעיף ב", "הקוד".

> סעיף ב : מתרגמים את הפתרון לפונקציה.

**The problem.** The array `labels = ["RED", "BLACK", "MIXED"]`, its indices 0 1 2 below.

> הקלט : מערך labels של שלוש תוויות,
> כלומר RED, BLACK ו-MIXED, בסדר כלשהו.

- Crates above the cells, with the English labels; an arrow `draw(2)` points into crate 2
  and a red ball rises, `"RED"` beside it.

> ה-API : draw(i) שולף כדור אקראי מקופסה i,
> ומחזיר RED או BLACK.

- The true contents shown faintly under the crates.

> בדוגמה מהעמוד, התוכן האמיתי הוא סידור 1 מסעיף א,
> ולכן הכדור מקופסה 2 אדום.

**Solution 1.** `fix_labels_simple` from the page (the comment lines and blank lines left
out of the picture), the variables `i`, `k`, `ball`, `other`, `fixed` beside it.

> הפתרון הראשון מתרגם את סעיף א כמעט מילה במילה,
> ובונה מערך fixed חדש.

- Lines 2, 5–7 run (the first loop).

> המעבר הראשון מחפש את MIXED.
> הוא בקופסה 2, ולכן k = 2.

- Line 8.

> דגימה אחת מקופסה 2 : יוצא RED.

- Lines 11, 12, 15.

> הצבע השני, other, הוא BLACK,
> וקופסה 2 מקבלת RED.

- Lines 18–20 (the second loop).

> המעבר השני : הקופסה שתוויתה RED
> מקבלת את other, כלומר BLACK.

- Lines 23–25 (the third loop).

> המעבר השלישי : הקופסה שתוויתה BLACK
> מקבלת MIXED.

- Line 27, `fixed = ['BLACK', 'MIXED', 'RED']`.

> התוצאה : BLACK, MIXED, RED.
> בדיוק סידור 1.

- The same code again with a black ball, fast, up to line 15.

> ואם הכדור שחור? other הוא RED,
> וקופסה 2 מקבלת BLACK.

- The second and third loops and the return.

> קופסה 1 מקבלת RED, וקופסה 0 מקבלת MIXED.
> זה סידור 2.

- Two chips: `passes 3`, `memory new array`.

> הפתרון נכון וקריא, אבל עובר על המערך שלוש פעמים
> ומחזיק מערך נוסף.

**Solution 2, the idea.** The three cells `RED BLACK MIXED`, tagged `same`, `other`, `k`
below; three curved arrows of the cycle above.

> הפתרון השני מתחיל מתצפית :
> התיקון הוא סיבוב של שלוש התוויות.

> נקרא same לקופסה שתוויתה כצבע הכדור,
> ו-other לקופסה השלישית.

- The labels slide along the arrows: `BLACK MIXED RED`.

> צבע הכדור עובר ל-k, MIXED עובר ל-other,
> והצבע השני עובר ל-same.

> וסיבוב של שלושה איברים
> הוא בדיוק שתי החלפות.

**Solution 2, the code.** `fix_labels` from the page (comments left out of the picture),
the variables under it.

> הקוד : אחרי הדגימה לא מחפשים שוב,
> ולא בונים מערך חדש.

- Lines 2–3.

> שוב k = 2, והכדור שיוצא אדום.

- Line 5.

> השכנים של k : ‏(k + 1) % 3, כלומר 0,
> ו-(k + 2) % 3, כלומר 1.

- Lines 6–7.

> בקופסה 0 כתוב RED, כמו הכדור,
> ולכן same = 0 ו-other = 1.

- Line 10.

> החלפה ראשונה, בין k ל-same : קופסה 2 כבר נכונה,
> ו-MIXED עובר זמנית ל-0.

- Lines 11–12.

> החלפה שנייה, בין same ל-other :
> מתקבל BLACK, MIXED, RED.

> אותה תוצאה כמו בפתרון הראשון,
> בשתי החלפות במקום.

**The `%` note.** Two columns, Python and SystemVerilog, for `k = 0`.

> ולמה (k + 2) % 3 ולא (k − 1) % 3?
> שניהם אמורים לתת את השכן הקודם במעגל.

- Python: `(0 - 1) % 3` gives `2`.

> ב-Python, ‏(0 − 1) % 3 הוא 2,
> כי שם התוצאה של % אף פעם לא שלילית.

- SystemVerilog: `(0 - 1) % 3` gives `-1`, an invalid index, in red.

> ב-SystemVerilog וב-C, % שומר על סימן המחולק :
> יוצא −1, אינדקס לא חוקי.

- `(0 + 2) % 3` gives `2` in both, green.

> חיבור 2 שקול לחיסור 1 מודולו 3, ונשאר חיובי.
> לכן הקוד זהה בשתי השפות.

**The cost.** The two functions side by side: passes, extra memory, label operations,
draws.

> הסיבוכיות : שני הפתרונות O(1),
> עם דגימה אחת.

> השני עושה מעבר אחד ושתי החלפות במקום,
> בלי מערך נוסף.

## Closing

- The two answers, a line each, with the part's letter.

> לסיכום : דגימה אחת מהקופסה "אדום ושחור"
> מתקנת את שלוש התוויות.

- The DV mark, the site's address and `#0004`.

> ובקוד התיקון הוא סיבוב, שתי החלפות במקום.
> נסו בתיבה שבעמוד של שאלה 0004.
