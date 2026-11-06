# 0016 — the Josephus problem: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); notes/VIDEOS.md.

he: שאלה 0016 : בעיית יוספוס,
he: שאלה ברמת ג'וניור.
en: Question 0016: the Josephus problem,
en: a junior-level question.

he: שלושה סעיפים : אחד יוצא, שניים יוצאים,
he: ובבונוס L − 1 יוצאים.
en: Three parts: one leaves, two leave,
en: and in the bonus L − 1 leave.

he: במעגל עומדים N אנשים, ממוספרים
he: מ-0 עד N − 1 עם כיוון השעון.
en: N people stand in a circle, numbered
en: from 0 to N − 1 clockwise.

he: אדם 0 נשאר, הבאים אחריו יוצאים,
he: הבא נשאר, וכך שוב ושוב סביב המעגל.
en: Person 0 stays, the next ones leave,
en: the next stays, and so on around the circle.

he: עד שנשאר אדם אחד : השורד.
he: מי הוא, ומה הנוסחה לכל N?
en: Until one person is left: the survivor.
en: Who is it, and what is the formula for any N?

he: סעיף א : אדם 0 נשאר ואדם 1 יוצא,
he: כלומר כל שני יוצא. השורד הוא F(N).
en: Part A: person 0 stays and person 1 leaves,
en: so every second one leaves. The survivor is F(N).

he: נתחיל ב-5 אנשים. אדם 0 נשאר,
he: ואדם 1 יוצא.
en: Start with 5 people. Person 0 stays,
en: and person 1 leaves.

he: אדם 2 נשאר, ואדם 3 יוצא.
en: Person 2 stays, and person 3 leaves.

he: אדם 4 נשאר, והספירה ממשיכה סביב
he: המעגל : אדם 0 יוצא.
en: Person 4 stays, and the count goes on around
en: the circle: person 0 leaves.

he: אדם 2 נשאר, ואדם 4 יוצא.
he: השורד הוא אדם 2 : F(5) = 2.
en: Person 2 stays, and person 4 leaves.
en: The survivor is person 2: F(5) = 2.

he: נחשב את השורד לכל N עד 32,
he: ושורה חדשה בכל חזקה של 2.
en: Compute the survivor for every N up to 32,
en: with a new row at each power of 2.

he: בכל חזקה של 2 השורד הוא 0, ומשם
he: הוא עולה ב-2 עם כל אדם נוסף.
en: At each power of 2 the survivor is 0, and from
en: there it climbs by 2 with each extra person.

he: למשל 12 = 8 + 4 נותן 8, ו-31 = 16 + 15
he: נותן 30, התא האחרון של השורה של 16.
en: For example 12 = 8 + 4 gives 8, and 31 = 16 + 15
en: gives 30, the last cell of the row of 16.

he: ההשערה : אם N = 2ᵐ + r עם r < 2ᵐ,
he: אז F(N) = 2r. עכשיו נוכיח.
en: The guess: if N = 2ᵐ + r with r < 2ᵐ,
en: then F(N) = 2r. Now let's prove it.

he: קודם חזקה של 2 : עם 8 אנשים,
he: מי שמתחיל את הספירה הוא השורד.
en: First a power of 2: with 8 people,
en: whoever starts the count is the survivor.

he: סיבוב 1 : יוצאים כל האי-זוגיים, נשארו 4,
he: והספירה חוזרת בדיוק לאדם 0.
en: Round 1: all the odd ones leave, 4 are left,
en: and the count comes back exactly to person 0.

he: כל סיבוב חוצה את המעגל, וחוזר למי
he: שהתחיל. אחרי 3 סיבובים נשאר רק אדם 0.
en: Every round halves the circle and returns to the starter.
en: After 3 rounds only person 0 is left.

he: עם 2ᵐ אנשים כל סיבוב משאיר חצי, שוב
he: חזקה של 2, ולכן מי שמתחיל שורד.
en: With 2ᵐ people every round leaves half, again
en: a power of 2, so whoever starts survives.

he: ובכלל, כש-N זוגי סיבוב שלם משאיר את
he: הזוגיים ומתחיל שוב מ-0 : F(2k) = 2F(k).
en: In general, for an even N a full round leaves
en: the evens and starts from 0 again: F(2k) = 2F(k).

he: למשל F(20) = 2F(10) = 4F(5) = 8,
he: ואת F(5) = 2 כבר ראינו.
en: For example F(20) = 2F(10) = 4F(5) = 8,
en: and we already saw F(5) = 2.

he: לפי הסיפור, ביודפת עמדו 41 אנשים
he: במעגל, אבל שם כל שלישי יצא, כלל אחר.
en: In the story, 41 people stood in a circle at Yodfat,
en: but there every third one left, a different rule.

he: נריץ את הכלל שלנו על 41 = 32 + 9 :
he: חזקה של 2, ועוד 9 אנשים.
en: Run our rule on 41 = 32 + 9:
en: a power of 2, plus 9 people.

he: מוציאים 9 אנשים, 1, 3 עד 17,
he: עד שנשארים בדיוק 32 : חזקה של 2.
en: Remove 9 people, 1, 3 up to 17,
en: until exactly 32 are left: a power of 2.

he: ועכשיו הספירה מתחילה מאדם 18.
he: מעגל של 32, ולכן 18 הוא השורד.
en: Now the count starts from person 18.
en: A circle of 32, so 18 is the survivor.

he: באופן כללי : אחרי r יציאות יצאו כל
he: האי-זוגיים עד 2r − 1, ומתחיל אדם 2r.
en: In general: after r eliminations all the odd ones
en: up to 2r − 1 are gone, and person 2r starts.

he: כל אדם נוסף מוסיף יציאה אחת לפני
he: החזקה של 2, ולכן השורד זז ב-2.
en: Each extra person adds one elimination before
en: the power of 2, so the survivor moves by 2.

he: נמשיך עד הסוף, כדי לבדוק :
he: כולם יוצאים, חוץ מאדם 18.
en: Let's run to the end to check:
en: everyone leaves, except person 18.

he: השורד הוא 18 : F(41) = 18. ובאותה
he: דרך, 20 = 16 + 4 נותן F(20) = 8.
en: The survivor is 18: F(41) = 18. In the same
en: way, 20 = 16 + 4 gives F(20) = 8.

he: בבינארי : 20 הוא 10100. הביט העליון
he: הוא 16, והביטים שאחריו הם r = 4.
en: In binary: 20 is 10100. The top bit
en: is 16, and the bits after it are r = 4.

he: הביט העליון עובר לסוף והופך ל-0 :
he: מקבלים 01000, כלומר 2r = 8, השורד.
en: The top bit moves to the end and becomes 0:
en: we get 01000, that is 2r = 8, the survivor.

he: ועם 41, כלומר 101001 : מקבלים 010010,
he: כלומר 18, כמו בסימולציה.
en: And with 41, that is 101001: we get 010010,
en: that is 18, as in the simulation.

he: במספור מ-0 הביט מגיע לסוף כ-0.
he: במספור מ-1 הוא נשאר 1, והשורד הוא 2r + 1.
en: Numbering from 0, the bit arrives at the end as 0.
en: From 1, it stays 1, and the survivor is 2r + 1.

he: בחומרה זה גלאי של ה-1 העליון והזזה :
he: תשובה במחזור שעון אחד, לכל N.
en: In hardware: a leading-one detector and a shift,
en: the answer in one clock cycle, for any N.

he: בתיבה שבעמוד : 20 אנשים במעגל,
he: צעד אחרי צעד.
en: In the page's box: 20 people in a circle,
en: step by step.

he: אחרי 10 צעדים, סוף סיבוב 1 :
he: נשארו רק הזוגיים.
en: After 10 steps, the end of round 1:
en: only the even ones are left.

he: אחרי 15 צעדים, סוף סיבוב 2 :
he: נשארו 0, 4, 8, 12 ו-16.
en: After 15 steps, the end of round 2:
en: 0, 4, 8, 12 and 16 are left.

he: ואחרי 19 צעדים : השורד הוא אדם 8.
en: And after 19 steps: the survivor is person 8.

he: סעיף ב : אדם 0 נשאר, ו-1 ו-2 יוצאים,
he: וכך הלאה. השורד הוא F₃(N).
en: Part B: person 0 stays, 1 and 2 leave,
en: and so on. The survivor is F₃(N).

he: שבעה אנשים. אדם 0 נשאר,
he: ואנשים 1 ו-2 יוצאים.
en: Seven people. Person 0 stays,
en: and people 1 and 2 leave.

he: אדם 3 נשאר, ו-4 ו-5 יוצאים.
en: Person 3 stays, and 4 and 5 leave.

he: אדם 6 נשאר, ו-0 ו-3 יוצאים.
he: השורד הוא 6 : F₃(7) = 6.
en: Person 6 stays, and 0 and 3 leave.
en: The survivor is 6: F₃(7) = 6.

he: השורד לכל N עד 30. צעד מוריד שניים,
he: ולכן מסדרים לפי זוגיות : שתי שרשראות.
en: The survivor for every N up to 30. A step removes
en: two, so we sort by parity: two chains.

he: השורד נופל לאפס ב-1, 3, 9 ו-27,
he: ובזוגיים ב-2, 6 ו-18.
en: The survivor drops to zero at 1, 3, 9 and 27,
en: and among the evens at 2, 6 and 18.

he: ובין שתי נקודות אפס בשרשרת, השורד
he: עולה ב-3 בכל צעד של 2.
en: Between two zero points of a chain, the survivor
en: climbs by 3 with every step of 2.

he: מה שהשתנה : שתי שרשראות, נקודות אפס
he: ב-3ᵐ וב-2 · 3ᵐ, ועלייה של 3.
en: What changed: two chains, zero points
en: at 3ᵐ and 2 · 3ᵐ, and a climb of 3.

he: סיבוב שלם על כפולה של 3 משאיר את
he: הכפולות של 3, והספירה חוזרת לאדם 0.
en: A full round on a multiple of 3 leaves the multiples
en: of 3, and the count returns to person 0.

he: עם 9 אנשים : נשארים 0, 3 ו-6,
he: ושוב מאדם 0. ואז נשאר רק 0.
en: With 9 people: 0, 3 and 6 are left,
en: again from person 0. Then only 0 is left.

he: ומכיוון ש-F₃(1) = F₃(2) = 0, בכל נקודת
he: אפס, 3ᵐ או 2 · 3ᵐ, מי שמתחיל שורד.
en: Since F₃(1) = F₃(2) = 0, at every zero point,
en: 3ᵐ or 2 · 3ᵐ, whoever starts survives.

he: אותו רעיון עם 30 אנשים. נקודת האפס
he: הזוגית שמתחת ל-30 היא 18.
en: The same idea with 30 people. The even
en: zero point below 30 is 18.

he: כל צעד מוציא שניים. אחרי 6 צעדים
he: נשארים בדיוק 18 : נקודת אפס.
en: Each step removes two. After 6 steps
en: exactly 18 are left: a zero point.

he: והספירה מתחילה מאדם 18, שלושה
he: לכל צעד : 3 · 6 = 18. הוא השורד.
en: And the count starts from person 18, three
en: per step: 3 · 6 = 18. That is the survivor.

he: נמשיך עד הסוף : כולם יוצאים,
he: חוץ מאדם 18.
en: Let's run to the end: everyone leaves,
en: except person 18.

he: כללית : מ-N יורדים ב-j צעדים לנקודת
he: האפס M באותה זוגיות, והשורד הוא 3j.
en: In general: from N go down j steps to the zero
en: point M of the same parity; the survivor is 3j.

he: זהירות מהשרשרת : 21 אי-זוגי, ולכן M = 9
he: ולא 18, והשורד שוב 18.
en: Mind the chain: 21 is odd, so M = 9
en: and not 18, and the survivor is 18 again.

he: גם כאן יש כלל בספרות, בבסיס 3 : כותבים
he: את חצי N, מחסרים 10…0 או 11…1, ומוסיפים 0.
en: A digit rule here too, in base 3: write half of N,
en: subtract 10…0 or 11…1, and append 0.

he: עם 30 : 15 הוא 120 בבסיס 3, פחות 100
he: נותן 20, ועם 0 בסוף 200, כלומר 18.
en: With 30: 15 is 120 in base 3, minus 100
en: gives 20, and with 0 appended 200, that is 18.

he: עם 21, אי-זוגי : 10 הוא 101, פחות 11
he: נותן 20, ושוב 200, כלומר 18.
en: With 21, odd: 10 is 101, minus 11
en: gives 20, and again 200, that is 18.

he: בתיבה שבעמוד, עם הכלל של סעיף ב :
he: שלושים אנשים במעגל.
en: In the page's box, with the rule of part B:
en: thirty people in a circle.

he: אחרי 10 צעדים נשארו רק הכפולות
he: של 3, והספירה שוב מאדם 0.
en: After 10 steps only the multiples of 3
en: are left, and the count is from person 0 again.

he: אחרי 14 צעדים נשארו 18 ו-27.
en: After 14 steps 18 and 27 are left.

he: ובצעד ה-15 אדם 27 יוצא :
he: השורד הוא אדם 18.
en: And at step 15 person 27 leaves:
en: the survivor is person 18.

he: סעיף ג, בונוס : אחד נשאר ו-L − 1 יוצאים,
he: לכל L. נוסחה אחת לכל המקרים.
en: Part C, bonus: one stays and L − 1 leave,
en: for any L. One formula for every case.

he: צעד אחד מוריד L − 1 אנשים, ומזיז
he: את המספור ב-L.
en: One step removes L − 1 people, and shifts
en: the numbering by L.

he: לכן יש L − 1 שרשראות, לפי השארית
he: של N בחלוקה ב-L − 1.
en: So there are L − 1 chains, by the remainder
en: of N divided by L − 1.

he: נקודות האפס הן b · Lᵐ עם 1 ≤ b < L,
he: וביניהן השורד עולה ב-L בכל צעד.
en: The zero points are b · Lᵐ with 1 ≤ b < L,
en: and between them the survivor climbs by L each step.

he: והבסיס : עם פחות מ-L אנשים, אדם 0
he: נשאר וכל השאר יוצאים מיד.
en: And the base: with fewer than L people, person 0
en: stays and all the others leave at once.

he: הנוסחה : M היא נקודת האפס של השרשרת
he: שמתחת ל-N, והשורד הוא L/(L − 1) · (N − M).
en: The formula: M is the chain's zero point below N,
en: and the survivor is L/(L − 1) · (N − M).

he: עם L = 2 : שרשרת אחת, M = 2ᵐ,
he: ו-F = 2(N − 2ᵐ). זה סעיף א.
en: With L = 2: one chain, M = 2ᵐ,
en: and F = 2(N − 2ᵐ). That is part A.

he: עם L = 3 : שתי שרשראות לפי הזוגיות,
he: ו-F = 3/2 · (N − M). זה סעיף ב.
en: With L = 3: two chains by parity,
en: and F = 3/2 · (N − M). That is part B.

he: עם L = 4 יש שלוש שרשראות, לפי
he: השארית של N בחלוקה ב-3.
en: With L = 4 there are three chains, by
en: the remainder of N divided by 3.

he: ועם L = 4 ו-N = 20 : r = 2 ו-M = 8,
he: והשורד הוא 4/3 · 12 = 16.
en: And with L = 4 and N = 20: r = 2 and M = 8,
en: and the survivor is 4/3 · 12 = 16.

he: לסיכום : יורדים לנקודת אפס, שבה מי
he: שמתחיל שורד, וסופרים כמה צעדים עברו.
en: To sum up: go down to a zero point, where whoever
en: starts survives, and count the steps it took.

he: נסו כל N וכל L בתיבה שבעמוד
he: של שאלה 0016 באתר.
en: Try any N and any L in the box on the page
en: of question 0016 on the site.
