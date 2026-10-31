# 0010 — valid parentheses: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0010 : סוגריים תקינים,
he: שאלה ברמת סטודנט.
en: Question 0010: valid parentheses,
en: a student-level question.

he: שני סעיפים : קודם פתרון פשוט,
he: ואז פתרון שעובר על המחרוזת פעם אחת.
en: Two parts: first a simple solution,
en: then one that reads the string once.

he: נתונה מחרוזת של סוגריים משלושה סוגים :
he: עגולים, מרובעים ומסולסלים.
en: A string holds brackets of three kinds:
en: round, square and curly.

he: היא תקינה אם כל פותח נסגר בסוגר מאותו סוג,
he: והאחרון שנפתח נסגר ראשון.
en: It is valid if every opener is closed by the same kind,
en: and the last one opened is closed first.

he: סעיף א : פתרון פשוט,
he: גם אם הוא לא יעיל.
en: Part A: a simple solution,
en: even if it is not efficient.

he: המחרוזת מהעמוד : {[()]}.
en: The page's string: {[()]}.

he: הרעיון : במחרוזת תקינה ולא ריקה
he: תמיד יש זוג צמוד, כמו () או [].
en: The idea: a valid, non-empty string
en: always has an adjacent pair, like () or [].

he: מוחקים אותו. מה שנשאר תקין
he: אם ורק אם המחרוזת המקורית תקינה.
en: Delete it. What is left is valid
en: if and only if the original string is valid.

he: עכשיו [] צמוד, ואחריו {}.
he: מוחקים גם אותם.
en: Now [] is adjacent, and after it {}.
en: Delete them too.

he: לא נשאר כלום : המחרוזת תקינה.
en: Nothing is left: the string is valid.

he: מחיקה יכולה ליצור זוג צמוד חדש :
he: ב-(()) מוחקים את הזוג הפנימי,
en: A deletion can create a new adjacent pair:
en: in (()) we delete the inner pair,

he: ורק אז הזוג החיצוני נהיה צמוד.
he: לכן חוזרים על המחיקה, מעבר אחרי מעבר.
en: and only then the outer pair becomes adjacent.
en: So we repeat the deletion, pass after pass.

he: ובמחרוזת ([)] אין אף זוג צמוד :
he: אין מה למחוק, והיא לא ריקה.
en: And the string ([)] has no adjacent pair:
en: nothing to delete, and it is not empty.

he: לכן היא לא תקינה : הסוגר העגול נסגר
he: לפני המרובע, שנפתח אחריו.
en: So it is not valid: the round bracket closes
en: before the square one, opened after it.

he: עכשיו נכתוב את זה ב-Python.
en: Now let's write it in Python.

he: ‏isValid_brute מקבלת את המחרוזת s,
he: ומחזירה True אם היא תקינה.
en: isValid_brute takes the string s,
en: and returns True if it is valid.

he: שורה 2 : הלולאה רצה כל עוד יש במחרוזת
he: זוג צמוד, מאחד משלושת הסוגים.
en: Line 2: the loop runs while the string has
en: an adjacent pair, of any of the three kinds.

he: שורה 3 : מעבר אחד מוחק את כל ה-(),
he: אחר כך את כל ה-[], ואז את כל ה-{}.
en: Line 3: one pass deletes every (),
en: then every [], and then every {}.

he: שורה 4 : כשאין יותר זוג צמוד,
he: המחרוזת תקינה רק אם לא נשאר בה כלום.
en: Line 4: when no adjacent pair is left,
en: the string is valid only if nothing is left.

he: נריץ את הקוד על (()).
en: Let's run the code on (()).

he: יש בה זוג צמוד, ולכן נכנסים ללולאה.
en: It has an adjacent pair, so we enter the loop.

he: שורה 3 : המעבר הראשון מוחק
he: את הזוג הפנימי, ונשאר ().
en: Line 3: the first pass deletes
en: the inner pair, and () is left.

he: המחיקה יצרה זוג צמוד חדש,
he: ולכן הלולאה ממשיכה.
en: The deletion created a new adjacent pair,
en: so the loop goes on.

he: המעבר השני מוחק אותו,
he: ונשארת מחרוזת ריקה.
en: The second pass deletes it,
en: and an empty string is left.

he: אין יותר זוג צמוד,
he: והלולאה נגמרת.
en: No adjacent pair is left,
en: and the loop ends.

he: שורה 4 : המחרוזת ריקה,
he: ולכן מוחזר True.
en: Line 4: the string is empty,
en: so True is returned.

he: על ([)] אין אף זוג צמוד,
he: ולכן הלולאה לא מתחילה בכלל.
en: ([)] has no adjacent pair,
en: so the loop does not even start.

he: שורה 4 : נשארו ארבעה תווים,
he: ולכן מוחזר False.
en: Line 4: four characters are left,
en: so False is returned.

he: שימו לב לתנאי של הלולאה : יש זוג צמוד.
he: עם "המחרוזת לא ריקה" היא הייתה אינסופית.
en: Note the loop's condition: there is an adjacent pair.
en: With "the string is not empty" it would never end.

he: כמה זה עולה? ניקח מחרוזת מקוננת,
he: ‏(((()))), באורך 8.
en: What does it cost? Take a nested string,
en: (((()))), of length 8.

he: כל מעבר מוחק רק את הזוג הפנימי :
he: אחרי שני מעברים נשארה (()).
en: Each pass deletes only the inner pair:
en: after two passes, (()) is left.

he: עוד שני מעברים, ורק אז המחרוזת ריקה :
he: ארבעה מעברים בסך הכול.
en: Two more passes, and only then is the string empty:
en: four passes in all.

he: כל מעבר קורא את המחרוזת שלוש פעמים,
he: פעם לכל replace : 44 תווים, לעומת 8.
en: Each pass reads the string three times,
en: once per replace: 44 characters, against 8.

he: גם התיבה שבעמוד מראה את המעברים,
he: ואת מספר התווים שנקראו בכל אחד.
en: The page's box shows the passes too,
en: and the characters read in each one.

he: במחרוזת מקוננת באורך n יש n/2 מעברים,
he: וכל מעבר עולה O(n) : בסך הכול O(n²).
en: A nested string of length n takes n/2 passes,
en: each costs O(n): O(n²) in all.

he: הסיבוכיות : זמן O(n²), וזיכרון O(n)
he: למחרוזות החדשות. אפשר לעשות יותר טוב.
en: The cost: O(n²) time, and O(n) memory
en: for the new strings. We can do better.

he: סעיף ב : פתרון שעובר על המחרוזת
he: פעם אחת בלבד.
en: Part B: a solution that reads the string
en: only once.

he: הרעיון : הסוגר שנפתח אחרון
he: נסגר ראשון.
en: The idea: the bracket opened last
en: is closed first.

he: כשמגיע סוגר סוגר, רק הפותח האחרון
he: שעוד לא נסגר יכול להתאים לו.
en: When a closer comes, only the last opener
en: not closed yet can match it.

he: זו בדיוק מחסנית :
he: נכנס אחרון, יוצא ראשון.
en: That is exactly a stack:
en: last in, first out.

he: כך זה נראה בתיבה שבעמוד. המחסנית
he: משמאל, ועומק המחסנית בגרף.
en: This is the page's box. The stack is on the left,
en: and the stack's depth in the chart.

he: התו { פותח, ולכן נדחף למחסנית.
en: { is an opener, so it is pushed onto the stack.

he: גם [ פותח, ונדחף מעליו.
en: [ is an opener too, pushed on top of it.

he: גם ( נדחף, ועכשיו הוא
he: בראש המחסנית.
en: ( is pushed as well, and it is now
en: at the top of the stack.

he: התו ) סוגר. בראש המחסנית ( מאותו סוג,
he: ולכן מוציאים אותו.
en: ) is a closer. The top is ( of the same kind,
en: so we pop it.

he: התו ] סוגר את ה-[ שבראש המחסנית.
en: ] closes the [ at the top of the stack.

he: התו } סוגר את ה-{. המחסנית ריקה :
he: המחרוזת תקינה.
en: } closes the {. The stack is empty:
en: the string is valid.

he: עכשיו ([)], שאין בה אף זוג צמוד.
en: Now ([)], which has no adjacent pair.

he: ‏( ואחריו [ נדחפים למחסנית.
en: ( and then [ are pushed onto the stack.

he: התו ) סוגר עגול, אבל בראש המחסנית [ :
he: לא תקינה, ועוצרים מיד.
en: ) closes a round bracket, but the top is [:
en: not valid, and we stop at once.

he: ובמחרוזת ((( כל תו פותח,
he: וכולם נדחפים למחסנית.
en: And in ((( every character is an opener,
en: and all are pushed onto the stack.

he: המחרוזת נגמרה, והמחסנית לא ריקה :
he: שלושה פותחים לא נסגרו.
en: The string has ended and the stack is not empty:
en: three openers were never closed.

he: אלה שלושת הכישלונות : סוג לא מתאים,
he: סוגר בלי פותח, ופותחים שנשארו.
en: These are the three failures: a wrong kind,
en: a closer with no opener, and openers left over.

he: עכשיו נכתוב את זה ב-Python.
en: Now let's write it in Python.

he: ‏isValid מקבלת מחרוזת,
he: ומחזירה True אם היא תקינה.
en: isValid takes a string,
en: and returns True if it is valid.

he: שורות 2–3 : אורך אי-זוגי אף פעם לא תקין,
he: כי סוגריים באים בזוגות.
en: Lines 2–3: an odd length is never valid,
en: because brackets come in pairs.

he: שורה 5 : מילון מכל סוגר סוגר
he: לפותח מאותו סוג.
en: Line 5: a dictionary from each closer
en: to the opener of its kind.

he: שורה 6 : המחסנית, בהתחלה רשימה ריקה.
en: Line 6: the stack, an empty list at first.

he: שורה 8 : עוברים על התווים,
he: אחד אחרי השני.
en: Line 8: we go over the characters,
en: one after the other.

he: שורות 9–11 : לסוגר סוגר צריך את הפותח שלו
he: בראש המחסנית. אם אין, מחזירים False.
en: Lines 9–11: a closer needs its opener
en: at the top of the stack. If not, return False.

he: שורה 12 : אם הוא שם,
he: מוציאים אותו מהמחסנית.
en: Line 12: if it is there,
en: we pop it off the stack.

he: שורות 13–14 : סוגר פותח
he: נדחף למחסנית.
en: Lines 13–14: an opener
en: is pushed onto the stack.

he: שורה 16 : בסוף, תקינה רק אם המחסנית ריקה,
he: כלומר כל הפותחים נסגרו.
en: Line 16: at the end, valid only if the stack is empty,
en: that is, every opener was closed.

he: נריץ על {[()]},
he: לצד התיבה מהעמוד.
en: Let's run it on {[()]},
en: beside the page's box.

he: האורך 6, זוגי. המילון מוכן,
he: והמחסנית ריקה.
en: The length is 6, even. The dictionary is ready,
en: and the stack is empty.

he: התו { פותח : שורה 14 דוחפת אותו.
en: { is an opener: line 14 pushes it.

he: גם [ נדחף.
en: [ is pushed too.

he: גם ( נדחף. עכשיו במחסנית
he: שלושה פותחים.
en: ( is pushed too. Now the stack
en: holds three openers.

he: התו ) סוגר, ובראש המחסנית ( :
he: שורה 12 מוציאה אותו.
en: ) is a closer, and the top is (:
en: line 12 pops it.

he: התו ] סוגר את ה-[.
en: ] closes the [.

he: התו } סוגר את ה-{.
en: } closes the {.

he: הלולאה נגמרה והמחסנית ריקה :
he: שורה 16 מחזירה True.
en: The loop has ended and the stack is empty:
en: line 16 returns True.

he: עכשיו ([)] : האורך 4, זוגי.
en: Now ([)]: the length is 4, even.

he: התו ( נדחף.
en: ( is pushed.

he: התו [ נדחף מעליו.
en: [ is pushed on top of it.

he: התו ) סוגר, ובראש המחסנית [ :
he: שורה 11 מחזירה False.
en: ) is a closer, and the top is [:
en: line 11 returns False.

he: ועל ((( הקוד עוצר כבר בשורה 3 :
he: האורך 3, אי-זוגי, בלי לקרוא אף תו.
en: And on ((( the code stops at line 3 already:
en: the length is 3, odd, before reading a character.

he: התיבה קוראת עד הסוף ומראה את הפותחים
he: שנשארו. הקוד יודע את זה קודם, מהאורך.
en: The box reads to the end and shows the openers
en: left over. The code knows it earlier, from the length.

he: ופותחים שנשארו באורך זוגי? למשל (([] :
he: האורך 4, ולכן הלולאה רצה.
en: And openers left over at an even length? Say (([]:
en: the length is 4, so the loop runs.

he: שלושת הפותחים נדחפים למחסנית.
en: The three openers are pushed onto the stack.

he: התו ] סוגר את ה-[, ושורה 12 מוציאה אותו.
en: ] closes the [, and line 12 pops it.

he: הלולאה נגמרה, ונשארו במחסנית (( :
he: שורה 16 מחזירה False.
en: The loop has ended, and (( is left on the stack:
en: line 16 returns False.

he: הסיבוכיות : כל תו נקרא פעם אחת, זמן O(n),
he: וזיכרון O(n) למחסנית במקרה הגרוע.
en: The cost: each character is read once, O(n) time,
en: and O(n) memory for the stack at worst.

he: מלכודת : לא מספיק לספור פותחים וסוגרים.
he: ב-)( יש אחד מכל סוג.
en: A trap: counting openers and closers is not enough.
en: )( has one of each.

he: אבל הסוגר מגיע כשהמחסנית ריקה,
he: ושורות 10–11 מחזירות False.
en: But the closer comes while the stack is empty,
en: and lines 10–11 return False.

he: לסיכום : מחיקת זוגות צמודים, O(n²),
he: או מחסנית במעבר אחד, O(n).
en: In short: deleting adjacent pairs, O(n²),
en: or a stack in one pass, O(n).

he: נסו מחרוזות משלכם בתיבה
he: שבעמוד של שאלה 0010 באתר.
en: Try strings of your own in the box
en: on the page of question 0010 on the site.
