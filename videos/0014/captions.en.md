# 0014 — random squares and rectangles without overlap: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0014 : ריבועים ומלבנים אקראיים
he: בלי חפיפה. רמת ג'וניור.
en: Question 0014: random squares and rectangles
en: without overlap. Junior level.

he: שני סעיפים : ריבועים, ואז
he: מלבנים באורכים שונים.
en: Two parts: squares, then
en: rectangles of different sizes.

he: נתון grid של 10 על 8 נקודות : ‏x
he: מ-1 עד 10, ו-y מ-1 עד 8.
en: A grid of 10 by 8 points: x
en: from 1 to 10, and y from 1 to 8.

he: כל צורה מתוארת בשתי נקודות : הפינה
he: השמאלית התחתונה והימנית העליונה.
en: Every shape is given by two points: the
en: bottom-left corner and the top-right one.

he: הריבוע מ-(2, 2) עד (5, 5) : רוחב 3
he: וגובה 3. המלבן : רוחב 3 וגובה 4.
en: The square from (2, 2) to (5, 5): width 3
en: and height 3. The rectangle: width 3, height 4.

he: המטרה : להגריל מספר אקראי של צורות,
he: כך שאף שתיים לא חופפות.
en: The goal: draw a random number of shapes,
en: so that no two of them overlap.

he: מותר שיהיו צמודות : צלע משותפת,
he: חלק מצלע, או רק פינה משותפת.
en: They may touch: a shared edge,
en: part of an edge, or only a shared corner.

he: סעיף א : להגריל מספר אקראי של
he: ריבועים על ה-grid, בלי חפיפה.
en: Part A: draw a random number of
en: squares on the grid, without overlap.

he: נוסיף ריבועים אחד אחד.
he: הראשון : מ-(2, 2) עד (5, 5).
en: Let's add squares one by one.
en: The first: from (2, 2) to (5, 5).

he: הבא, מ-(4, 3) עד (7, 6), נכנס לתוך
he: הראשון : יש שטח משותף. נדחה.
en: The next, from (4, 3) to (7, 6), goes into
en: the first: they share area. Rejected.

he: מ-(5, 2) עד (7, 4) : נוגע בראשון
he: לאורך חלק מהצלע. מותר.
en: From (5, 2) to (7, 4): it touches the first
en: along part of an edge. Allowed.

he: מ-(5, 5) עד (7, 7) : נוגע בראשון
he: רק בפינה אחת. גם זה מותר.
en: From (5, 5) to (7, 7): it touches the first
en: only at one corner. Also allowed.

he: מ-(6, 3) עד (8, 5) : חופף את השני.
he: נדחה.
en: From (6, 3) to (8, 5): it overlaps the second.
en: Rejected.

he: ריבוע קטן בתוך הראשון, מ-(3, 3)
he: עד (4, 4) : גם הוא חופף. נדחה.
en: A small square inside the first, from (3, 3)
en: to (4, 4): it overlaps too. Rejected.

he: מ-(7, 2) עד (9, 4) : צלע משותפת
he: שלמה עם השני. מותר.
en: From (7, 2) to (9, 4): a whole shared
en: edge with the second. Allowed.

he: אז מה אסור? רק שטח משותף.
he: נגיעה בקו או בנקודה מותרת.
en: So what is forbidden? Only shared area.
en: Touching along a line or at a point is fine.

he: קשה לתאר ישירות מתי שני ריבועים
he: חופפים. קל יותר לתאר מתי לא.
en: It is hard to say directly when two squares
en: overlap. Easier to say when they don't.

he: ריבוע j לא חופף את i אם הוא
he: כולו באחד מארבעת האזורים סביבו.
en: Square j does not overlap i if it lies
en: entirely in one of the four zones around it.

he: משמאל : x2 של j לכל היותר x1 של i.
he: כך גם מימין, מתחת ומעל.
en: Left: x2 of j is at most x1 of i.
en: The same for right, below and above.

he: מספיק שאחד מהם מתקיים,
he: ולכן מחברים אותם ב-"או".
en: One of them is enough,
en: so they are joined with "or".

he: הסימן ≤ ולא < : כש-x2 של j שווה
he: ל-x1 של i, יש צלע משותפת. מותר.
en: The sign is <=, not <: when x2 of j equals
en: x1 of i, they share an edge. Allowed.

he: ובצורה ההפוכה : חופפים אם ורק אם
he: ההטלות נפגשות על x וגם על y.
en: And the other way round: they overlap if and
en: only if the projections meet on x and on y.

he: זו השלילה של ה-"או", לפי דה-מורגן.
he: נשתמש בה בבודק, בהמשך.
en: This is the negation of the "or", by De Morgan.
en: We'll use it in the checker, later.

he: כל התנאים יחד. כמות : n בין 1
he: ל-MAX_SHAPES.
en: All the rules together. Count: n from 1
en: to MAX_SHAPES.

he: כל צורה בתוך ה-grid, והסוף מימין
he: ומעל להתחלה : צלע באורך 1 לפחות.
en: Every shape on the grid, its end right of and
en: above its start: an edge of at least 1.

he: ריבוע : הרוחב שווה לגובה. ולכל
he: זוג i < j : אחד מארבעת האזורים.
en: A square: width equals height. And for every
en: pair i < j: one of the four zones.

he: עכשיו נכתוב את המחלקה
he: ב-SystemVerilog, עם constraints.
en: Now let's write the class
en: in SystemVerilog, with constraints.

he: המחלקה : גודל ה-grid,
he: ומספר הצורות המרבי, 6.
en: The class: the size of the grid,
en: and the most shapes, 6.

he: המשתנים האקראיים : n, ומערכים
he: דינמיים לפינות של כל צורה.
en: The random variables: n, and dynamic
en: arrays for every shape's corners.

he: התנאי הראשון : n בין 1 ל-6,
he: וגודל כל מערך שווה ל-n.
en: The first constraint: n from 1 to 6,
en: and every array's size equals n.

he: השני : לכל צורה, בתוך ה-grid,
he: והסוף מימין ומעל להתחלה.
en: The second: every shape on the grid,
en: its end right of and above its start.

he: השלישי : הרוחב שווה לגובה. הוא
he: לבד בכוונה, בשביל סעיף ב.
en: The third: width equals height. It stands
en: alone on purpose, for part B.

he: והרביעי : לכל זוג i < j, ארבעת
he: האזורים מחוברים ב-"או", עם ≤.
en: And the fourth: for every pair i < j, the four
en: zones joined with "or", with <=.

he: ‏randomize() פותר את כל התנאים יחד.
he: הנה פתרון אחד, מהדוגמאות שבעמוד.
en: randomize() solves all the constraints together.
en: Here is one solution, from the page's examples.

he: ‏c_count : ה-solver בוחר n = 6,
he: וארבעת המערכים בגודל 6.
en: c_count: the solver picks n = 6,
en: and the four arrays have size 6.

he: ‏c_on_grid : כל צורה בתוך ה-grid,
he: והפינה השנייה מימין ומעל.
en: c_on_grid: every shape on the grid,
en: the second corner right of and above the first.

he: ‏c_square : הרוחב של כל אחת שווה
he: לגובה שלה. כולן ריבועים.
en: c_square: each one's width equals
en: its height. They are all squares.

he: ‏c_no_overlap : ‏6 צורות, ‏15 זוגות.
he: בכל זוג אחד מארבעת המקרים.
en: c_no_overlap: 6 shapes, 15 pairs.
en: In every pair one of the four cases holds.

he: שימו לב לזוגות הצמודים : ‏1 ו-5, למשל,
he: נוגעים בפינה. ה-≤ מאפשר אותם.
en: Note the touching pairs: 1 and 5, for example,
en: touch at a corner. The <= allows them.

he: מלכודת : בלי i < j הלולאה בודקת
he: גם צורה מול עצמה.
en: A trap: without i < j the loop also checks
en: a shape against itself.

he: שם אף מקרה לא מתקיים, ולכן
he: ‏randomize() נכשל תמיד.
en: There no case holds, so
en: randomize() always fails.

he: מלכודת שנייה : < במקום ≤. אז
he: צורות צמודות נחשבות חופפות.
en: A second trap: < instead of <=. Then
en: touching shapes count as overlapping.

he: בפתרון הזה 7 זוגות צמודים, וכולם
he: היו נפסלים, בניגוד לדרישה.
en: This solution has 7 touching pairs, and all
en: would be refused, against the requirement.

he: ב-DV לא סומכים על randomize() בלי
he: לבדוק : קודם, שהוא החזיר 1.
en: In DV we don't trust randomize() without
en: checking: first, that it returned 1.

he: ואחר כך בודק נפרד, shapes_ok, שכתוב
he: בצורת ה-"וגם" : חפיפה על שני הצירים.
en: Then a separate checker, shapes_ok, written
en: in the "and" form: overlap on both axes.

he: שני ניסוחים של אותו תנאי : טעות
he: באחד לא תעבור בשני.
en: Two wordings of the same rule: a mistake
en: in one won't get past the other.

he: בתיבה שבעמוד : ה-grid של 10 על 8,
he: ועד 6 צורות בכל הגרלה.
en: In the page's box: the grid of 10 by 8,
en: and up to 6 shapes in each draw.

he: ערך אתחול 7 : הגרלה של צורה אחת.
he: גם 1 הוא מספר חוקי.
en: Seed 7: a draw of one shape.
en: 1 is a legal number too.

he: ערך אתחול 12 : שני ריבועים.
en: Seed 12: two squares.

he: ערך אתחול 25 : ארבעה ריבועים,
he: ושלושה מהם צמודים זה לזה.
en: Seed 25: four squares,
en: three of them touching each other.

he: הסיבוכיות : n(n−1)/2 תנאי זוגות.
he: עם 6 צורות, 15 שה-solver פותר יחד.
en: The cost: n(n-1)/2 pair constraints.
en: With 6 shapes, 15 that the solver solves together.

he: סעיף ב : מלבנים באורכים שונים.
he: עדיין בלי חפיפה, ומותר צמוד.
en: Part B: rectangles of different sizes.
en: Still no overlap, and touching is allowed.

he: איזה תנאי שייך רק לריבועים?
he: רק אחד : הרוחב שווה לגובה.
en: Which rule belongs only to squares?
en: Just one: width equals height.

he: אותו מוציאים. וכל השאר נשארים,
he: גם תנאי החפיפה, כמו שהוא.
en: That one goes out. All the rest stay,
en: the overlap rule too, as it is.

he: מחלקה יורשת : rect_set מקבלת את
he: כל התנאים של square_set.
en: A derived class: rect_set gets
en: all the constraints of square_set.

he: ‏constraint באותו שם מחליף את זה
he: של מחלקת הבסיס. גוף ריק : בלי תנאי.
en: A constraint with the same name replaces the
en: base class's one. An empty body: no rule.

he: דרך שנייה, בלי מחלקה חדשה : לכבות
he: את התנאי באובייקט קיים.
en: A second way, with no new class: turn
en: the constraint off in an existing object.

he: יוצרים square_set רגיל.
en: Create an ordinary square_set.

he: ‏constraint_mode(0) מכבה את c_square
he: באובייקט הזה : עכשיו הוא מגריל מלבנים.
en: constraint_mode(0) turns c_square off
en: in this object: now it draws rectangles.

he: ומגרילים כרגיל.
en: And randomize as usual.

he: הגרלה של מלבנים, מהדוגמאות שבעמוד :
he: שש צורות, רובן צמודות, בלי שטח משותף.
en: A draw of rectangles, from the page's examples:
en: six shapes, most touching, no shared area.

he: למה לא לבדוק לפי פינות? הנה שני
he: מלבנים בצורת צלב.
en: Why not check by corners? Here are two
en: rectangles in the shape of a cross.

he: אף פינה של אחד לא בתוך השני,
he: ובכל זאת יש שטח משותף.
en: No corner of one is inside the other,
en: and still they share area.

he: התנאי שלנו בודק את ההטלות : הן
he: נפגשות על x וגם על y. חופפים.
en: Our rule checks the projections: they
en: meet on x and on y. They overlap.

he: בריבועים צלב לא ייתכן, ולכן רק
he: התנאי על הצירים נכון לשני הסעיפים.
en: With squares a cross is impossible, so only
en: the rule on the axes is right for both parts.

he: בתיבה שבעמוד : עוברים למלבנים,
he: סעיף ב.
en: In the page's box: switch to rectangles,
en: part B.

he: ערך אתחול 5 : חמישה מלבנים,
he: ושלושה מהם צמודים.
en: Seed 5: five rectangles,
en: three of them touching.

he: ערך אתחול 9 : שני מלבנים.
en: Seed 9: two rectangles.

he: בפתרון ב-Python שבעמוד : ‏196 ריבועים
he: אפשריים ב-grid, ו-1,260 מלבנים.
en: In the page's Python solution: 196 possible
en: squares on the grid, and 1,260 rectangles.

he: וב-SystemVerilog אותה סיבוכיות :
he: תנאי זוגות, n(n−1)/2.
en: And in SystemVerilog the same cost:
en: pair constraints, n(n-1)/2.

he: לסיכום : ארבעה אזורים ב-"או", עם ≤
he: כדי שצורות צמודות יהיו מותרות.
en: In short: four zones joined with "or", with <=
en: so that touching shapes are allowed.

he: נסו הגרלות משלכם בתיבה שבעמוד
he: של שאלה 0014 באתר.
en: Try draws of your own in the box
en: on the page of question 0014 on the site.
