# 0071 — the three-wizard duel: the English captions
#
# One entry per caption of script.md, in the same order: the Hebrew caption's lines
# (he:), exactly as in the script, then the English cue's lines (en:), at most two
# lines of 12 words. A blank line ends an entry. render.py writes out/captions.en.vtt
# from it with the times of captions.vtt (--captions-only: no render); VIDEOS.md.

he: שאלה 0071 : דו-קרב של שלושה קוסמים,
he: שאלה ברמת סניור.
en: Question 0071: a duel of three wizards,
en: a senior-level question.

he: שלושה סעיפים : אני ראשון, אני בוחר תור,
he: והמקרה הכללי.
en: Three parts: I go first, I choose my turn,
en: and the general case.

he: שלושה קוסמים מכשפים בתורות :
he: קוסם 1, אחריו 2, אחריו 3, וחוזר חלילה.
en: Three wizards cast spells in turns:
en: wizard 1, then 2, then 3, and around again.

he: בתור שלו כל קוסם מכשף על יריב אחד,
he: ופוגע בהסתברות שלו. מותר גם באוויר.
en: On his turn each wizard targets one rival
en: and hits with his chance. Casting into the air is allowed.

he: חוק החתולים : אם אחרי הסבב הראשון
he: כולם חיים, כולם הופכים לחתולים ומפסידים.
en: The cat rule: if all three are alive
en: after the first round, all become cats and lose.

he: השרביט : אני בוחר מראש את ההסתברות שלי,
he: וכולם רואים אותה. כולם משחקים הכי טוב.
en: The wand: I choose my hit chance in advance,
en: and everyone sees it. Everyone plays optimally.

he: סעיף א : אני מכשף ראשון,
he: מול קוסמים של 0.6 ו-0.8.
en: Part A: I cast first,
en: against wizards of 0.6 and 0.8.

he: קוסם 2 פוגע ב-0.6 וקוסם 3 ב-0.8.
he: המשתנה היחיד הוא השרביט שלי, p₁.
en: Wizard 2 hits with 0.6 and wizard 3 with 0.8.
en: The only variable is my wand, p₁.

he: הרעיון : פותרים מהסוף להתחלה. קודם
he: הדו-קרב, אחר כך קוסם 3, קוסם 2, ואני.
en: The idea: solve from the end backward.
en: First the duel, then wizard 3, wizard 2, and me.

he: שלב 1 : כשנשארים שניים, יורים לסירוגין.
he: מי שפותח פוגע מיד, או ששניהם מחטיאים,
en: Step 1: when two are left, they shoot in turn.
en: The opener hits at once, or both miss,

he: וחוזרים לאותו מצב. פותרים, ומקבלים
he: את הסיכוי של הפותח לנצח, V(x,y).
en: and we are back in the same state. Solving gives
en: the opener's chance to win, V(x,y).

he: קוסם 2 פותח מול קוסם 3 ומנצח ב-65% :
he: הירייה הראשונה שווה הרבה.
en: Wizard 2 opening against wizard 3 wins 65%:
en: the first shot is worth a lot.

he: ומי שפגע בסבב הראשון הוא השני בדו-קרב,
he: כי התור עובר למי שנשאר.
en: And whoever hit in the first round is second in the duel,
en: because the turn passes to the one left.

he: שלב 2 : קוסם 3 חייב לכשף,
he: אחרת כולם חתולים. על מי?
en: Step 2: wizard 3 must cast,
en: or everyone becomes a cat. At whom?

he: אם הוא פוגע בי, הוא שני מול קוסם 2.
he: אם בקוסם 2, הוא שני מולי.
en: If he hits me, he is second against wizard 2.
en: If he hits wizard 2, he is second against me.

he: משווים את שני הסיכויים, וכופלים
he: במכנים. נשאר אי-שוויון פשוט ב-p₁.
en: Compare the two chances and clear
en: the denominators: a simple inequality in p₁.

he: הוא מכשף עליי בדיוק כש-p₁ > 0.6,
he: כלומר על החזק מביני ומבין קוסם 2.
en: He targets me exactly when p₁ > 0.6,
en: that is, the stronger of me and wizard 2.

he: שלב 3 : קוסם 2. כש-p₁ < 0.6 קוסם 3 יכשף
he: עליו, ולכן באוויר הוא מפסיד : מכשף על 3.
en: Step 3: wizard 2. When p₁ < 0.6, wizard 3
en: targets him, so the air loses: he targets 3.

he: כש-p₁ > 0.6, באוויר קוסם 3 מכשף עליי,
he: וקוסם 2 פותח אחר כך מולו : ‏12/23.
en: When p₁ > 0.6, in the air wizard 3 targets me,
en: and wizard 2 then opens against him: 12/23.

he: כדי שפגיעה בקוסם 3 תשתלם לו, צריך
he: ‏p₁ < 0.355. זה סותר, ולכן הוא באוויר.
en: For hitting wizard 3 to pay, he would need
en: p₁ < 0.355. A contradiction, so he casts into the air.

he: שלב 4 : אני. אם אכשף, אכשף על קוסם 3,
he: החזק. אבל האם כדאי לי לכשף בכלל?
en: Step 4: me. If I cast, I target wizard 3,
en: the stronger. But should I cast at all?

he: אם p₁ < 0.6, אף אחד לא מכשף עליי.
he: אני מכשף באוויר, ופותח מול מי שנשאר.
en: If p₁ < 0.6, nobody targets me.
en: I cast into the air and open against whoever is left.

he: קוסם 2 פוגע ב-3 בהסתברות 0.6. אחרת קוסם 3
he: פוגע ב-2, בהסתברות 0.4 כפול 0.8.
en: Wizard 2 hits 3 with chance 0.6. Otherwise
en: wizard 3 hits 2, with chance 0.4 times 0.8.

he: אם p₁ > 0.6, קוסם 3 מכשף עליי. אני חייב
he: לפגוע מיד, ומקבל לכל היותר 0.4.
en: If p₁ > 0.6, wizard 3 targets me. I must
en: hit at once, and get at most 0.4.

he: הסיכוי שלי לפי השרביט : עולה עד ממש
he: לפני 0.6, וצונח כשאני עובר את קוסם 2.
en: My chance by wand: it rises until just
en: below 0.6, and drops once I pass wizard 2.

he: ב-0.6 מלמטה : ‏513/805, כמעט 64%.
he: צלף, שרביט 1, מקבל רק 40%.
en: Just below 0.6: 513/805, almost 64%.
en: A sniper, wand 1, gets only 40%.

he: למה לא 0.6 בדיוק? שם קוסם 3 אדיש,
he: ועלול לבחור בי. לכן קצת מתחת, למשל 0.59.
en: Why not exactly 0.6? There wizard 3 is indifferent
en: and might pick me. So slightly below, say 0.59.

he: הטבלה מהעמוד : עד 0.6 אני באוויר,
he: ומעליו אני חייב לכשף על קוסם 3.
en: The page's table: up to 0.6 I cast into the air,
en: and above it I must target wizard 3.

he: מעל 0.6 הסיכוי קופץ למטה, ל-0.223,
he: ועולה רק עד 0.4 בצלף.
en: Above 0.6 the chance drops to 0.223,
en: and climbs only to 0.4 with a sniper.

he: העיקרון אצל שניהם : לחסל את החזק,
he: כדי להישאר בסוף מול החלש, מולי.
en: The principle for both: kill the stronger,
en: to face the weaker, me, at the end.

he: עכשיו כל המשחק כשרשרת מרקוב :
he: כל מצב הוא מי חי, ומי מכשף עכשיו.
en: Now the whole game as a Markov chain:
en: a state is who is alive and whose turn it is.

he: בשורה העליונה הסבב הראשון : אני באוויר,
he: קוסם 2 על 3, ואם החטיא, קוסם 3 על 2.
en: The top row is the first round: I cast into the air,
en: wizard 2 at 3, and if he missed, wizard 3 at 2.

he: פגיעה מעבירה לדו-קרב, שבו מכשפים
he: לסירוגין עד שמישהו פוגע.
en: A hit leads to a duel, where they cast
en: in turn until someone hits.

he: בשורה התחתונה הניצחונות. הסיכוי לכל סוף
he: הוא סכום על המסלולים אליו.
en: The bottom row is the wins. The chance of each end
en: is a sum over the paths into it.

he: דו-קרב 1 מול 2, תורי : אני פוגע ב-0.6,
he: אחרת קוסם 2 מכשף, ואם החטיא, שוב אני.
en: Duel 1 vs 2, my turn: I hit with 0.6,
en: else wizard 2 casts, and if he missed, me again.

he: זו הלולאה של V : מהמצב הזה
he: אני מנצח ב-5/7.
en: This is the loop of V: from this state
en: I win with 5/7.

he: ודו-קרב 1 מול 3, תורי : מגיעים אליו
he: ב-0.32, ואני מנצח בו ב-15/23.
en: And duel 1 vs 3, my turn: we reach it
en: with 0.32, and I win it with 15/23.

he: כל מסלול הוא מכפלת ההסתברויות
he: שעל החצים שלו.
en: Each path is the product of the chances
en: on its arrows.

he: חתולים : שניהם מחטיאים,
he: ‏0.4 כפול 0.2, כלומר 8%.
en: Cats: both miss,
en: 0.4 times 0.2, that is 8%.

he: אני : ‏0.6 כפול 5/7, ועוד 0.32 כפול 15/23.
he: בסך הכול 63.7%.
en: Me: 0.6 times 5/7, plus 0.32 times 15/23.
en: In total 63.7%.

he: קוסם 2 : פוגע ב-3 ומנצח כשני מולי,
he: ‏0.6 כפול 2/7, כ-17.1%.
en: Wizard 2: hits 3 and wins as second against me,
en: 0.6 times 2/7, about 17.1%.

he: קוסם 3 : ‏0.32 כפול 8/23, כ-11.1%.
he: החזק מכולם מקבל הכי מעט.
en: Wizard 3: 0.32 times 8/23, about 11.1%.
en: The strongest of all gets the least.

he: הבדיקה : ‏63.7 ועוד 17.1, 11.1 ו-8,
he: בדיוק 100%.
en: The check: 63.7 plus 17.1, 11.1 and 8,
en: exactly 100%.

he: בתיבה שבעמוד : אני ראשון עם 0.599,
he: ושרשרת מרקוב של הבחירה.
en: In the page's box: me first with 0.599,
en: and the Markov chain of the choice.

he: שרביט 0.8 : קוסם 3 מכשף עליי,
he: וקוסם 2 מכשף באוויר.
en: Wand 0.8: wizard 3 targets me,
en: and wizard 2 casts into the air.

he: צלף : אני פוגע בקוסם 3 מיד,
he: וקוסם 2 פותח מולי. רק 40%.
en: A sniper: I hit wizard 3 at once,
en: and wizard 2 opens against me. Only 40%.

he: ובחזרה ממש מתחת ל-0.6 :
he: שוב 63.7%.
en: And back just below 0.6:
en: 63.7% again.

he: המלכודת : לחשוב שהשרביט החזק הוא הטוב.
he: כאן הוא נותן 40%, מול 63.7% לחלש.
en: The trap: thinking the strongest wand is best.
en: Here it gives 40%, against 63.7% for the weak one.

he: סעיף ב : עכשיו אני בוחר גם את התור,
he: ואת הסדר של שני היריבים.
en: Part B: now I also choose my turn,
en: and the order of the two rivals.

he: שלושה תורות, ובכל אחד שני סדרים :
he: שישה סדרים. כל אחד נפתר כמו סעיף א.
en: Three turns, two orders in each:
en: six orders. Each is solved like part A.

he: בכל אחד השרביט הטוב יוצא קצת מתחת
he: ל-0.6 : להיות החלש, שלא יכשפו עליי.
en: In each, the best wand comes out just below
en: 0.6: be the weakest, so nobody targets me.

he: ראשון או שני : ‏63.7% או 60.7%,
he: לפי מי מהיריבים מכשף קודם.
en: First or second: 63.7% or 60.7%,
en: depending on which rival casts first.

he: שלישי אחרי 0.6 ואז 0.8 : ‏65.1%, הכי טוב.
he: אחרי 0.8 ואז 0.6 רק 55.6%.
en: Third after 0.6 then 0.8: 65.1%, the best.
en: After 0.8 then 0.6, only 55.6%.

he: נפתח את הסדר המנצח. אני קוסם 3, עם p₃.
he: קוסם 1 פוגע ב-0.6, וקוסם 2 ב-0.8.
en: Let's work out the winning order. I am wizard 3, with p₃.
en: Wizard 1 hits with 0.6, and wizard 2 with 0.8.

he: הדו-קרבים של הסדר הזה, באותה נוסחה :
he: אני פותח, או שהיריב פותח מולי.
en: The duels of this order, with the same formula:
en: I open, or the rival opens against me.

he: אני אחרון בסבב : חייב לכשף, ועל החזק,
he: קוסם 2, כדי להישאר מול החלש.
en: I am last in the round: I must cast, at the stronger,
en: wizard 2, to stay against the weaker.

he: קוסם 2 : באוויר אני מחסל אותו. לכן מכשף,
he: על החזק מבין קוסם 1 ואותי : על 1.
en: Wizard 2: in the air I kill him. So he casts,
en: at the stronger of wizard 1 and me: at 1.

he: קוסם 1 : פגיעה בקוסם 2 עדיפה על האוויר
he: כל עוד p₃ < 5/6. לכן גם הוא מכשף על 2.
en: Wizard 1: hitting wizard 2 beats the air
en: as long as p₃ < 5/6. So he also targets 2.

he: הסיכוי שלי : שלוש דרכים לדו-קרב.
he: האחרונה, הפגיעה שלי, היא רק גיבוי.
en: My chance: three ways into a duel.
en: The last one, my own hit, is just a backup.

he: בגבול מתחת ל-0.6 : ‏13101/20125,
he: כ-65.1%.
en: In the limit just below 0.6: 13101/20125,
en: about 65.1%.

he: השרשרת של הסדר הזה : קוסם 1 על 2,
he: אם החטיא קוסם 2 על 1, ואם החטיא אני.
en: The chain of this order: wizard 1 at 2,
en: if he missed wizard 2 at 1, and if he missed, me.

he: הדו-קרבים : בכולם אני משחק
he: מול מי שנשאר.
en: The duels: in all of them I play
en: against whoever is left.

he: בסוף : אני 65.1%, קוסם 1 ‏20.6%,
he: קוסם 2 ‏11.1%.
en: At the end: me 65.1%, wizard 1 20.6%,
en: wizard 2 11.1%.

he: חתולים רק אם שלושתנו מחטיאים :
he: ‏0.4 כפול 0.2 כפול 0.4, כלומר 3.2%.
en: Cats only if all three of us miss:
en: 0.4 times 0.2 times 0.4, that is 3.2%.

he: וקוסם 1 : פוגע בקוסם 2 ומנצח כשני מולי,
he: או פותח מולי אחרי הפגיעה שלי.
en: And wizard 1: hits wizard 2 and wins as second against me,
en: or opens against me after my hit.

he: ואני : שלוש דרכים לדו-קרב,
he: ובשתיים הראשונות אני פותח.
en: And me: three ways into a duel,
en: and in the first two I open.

he: קוסם 2 : רק אם פגע בקוסם 1, ואז הוא
he: שני מולי : ‏0.32 כפול 8/23, כ-11.1%.
en: Wizard 2: only if he hit wizard 1, and then he is
en: second against me: 0.32 times 8/23, about 11.1%.

he: למה זה מנצח? כשאני אחרון, שני היריבים
he: מכשפים לפניי, והחתולים יורדים ל-3.2%.
en: Why does this win? When I am last, both rivals
en: cast before me, and the cats drop to 3.2%.

he: והחלש מכשף ראשון : הוא מכשף על 0.8,
he: ואני נשאר מול 0.6 ולא מול 0.8.
en: And the weaker casts first: he targets 0.8,
en: and I stay against 0.6, not 0.8.

he: בתיבה, הכפתור הבחירה הטובה ביותר
he: עובר על ששת הסדרים.
en: In the box, the "best choice" button
en: goes through the six orders.

he: הוא בוחר שלישי, אחרי 0.6 ואז 0.8,
he: ממש מתחת ל-0.6 : ‏65.1%.
en: It picks third, after 0.6 then 0.8,
en: just below 0.6: 65.1%.

he: ושרשרת מרקוב של הבחירה הזו,
he: עם אותם מספרים.
en: And the Markov chain of this choice,
en: with the same numbers.

he: סעיף ג : יריבים כלשהם, a < b.
he: מה הבחירה הכי טובה?
en: Part C: any rivals, a < b.
en: What is the best choice?

he: מה שראינו : כל קוסם מכשף על החזק
he: מבין שני האחרים. על החלש מכולם לא מכשפים.
en: What we saw: each wizard targets the stronger
en: of the other two. Nobody targets the weakest.

he: לכן יש שתי תוכניות : להסתתר כחלש,
he: או להיות צלף ולהרוג את החזק ראשון.
en: So there are two plans: hide as the weakest,
en: or be a sniper and kill the strongest first.

he: צלף ראשון : שרביט 1, ואני הורג את b מיד.
he: היריב a פותח מולי, ומנצח רק אם פגע.
en: Sniper first: wand 1, and I kill b at once.
en: Rival a opens against me, and wins only if he hits.

he: להסתתר : שלישי, אחרי a ואז b,
he: עם שרביט קצת מתחת ל-a, כמו בסעיף ב.
en: Hide: third, after a then b,
en: with a wand just below a, as in part B.

he: צלף בתור שני או שלישי לא מקבל יותר :
he: מי שמכשף לפניו רואה בו את החזק.
en: A sniper second or third gets no more:
en: whoever casts before him sees him as the strongest.

he: בתוכנית ההסתרה, כמו בסעיף ב : אני
he: אחרון ומכשף על b, ו-b מכשף על a.
en: In the hiding plan, as in part B: I am
en: last and target b, and b targets a.

he: ו-a מכשף על b, כי 1 − a גדול תמיד
he: מ-(1 − b)a.
en: And a targets b, since 1 − a is always
en: greater than (1 − b)a.

he: הסיכוי שלי : סכום על שלושת המסלולים
he: של השרשרת, כמו בסעיף ב.
en: My chance: a sum over the three paths
en: of the chain, as in part B.

he: מציבים את V משלב 1. מול יריב שווה לי :
he: השבר מצטמצם ל-1/(2 − a).
en: Substitute V from step 1. Against an equal rival,
en: the fraction reduces to 1/(2 − a).

he: ומול b : ‏a חלקי a + b − ab.
he: כאן אין מה לצמצם.
en: And against b: a over a + b − ab.
en: Nothing to reduce here.

he: וזה הביטוי הכללי של הסיכוי שלי,
he: ב-a וב-b בלבד.
en: And this is the general expression of my chance,
en: in a and b only.

he: ובאותה דרך, הסיכויים של שני היריבים
he: ושל החתולים.
en: In the same way, the chances of the two rivals
en: and of the cats.

he: החתולים : שלושתנו מחטיאים, כי השרביט
he: שלי קרוב ל-a : ‏(1 − a)² כפול (1 − b).
en: The cats: all three miss, since my wand
en: is close to a: (1 − a)² times (1 − b).

he: בדיקה : a = 0.6 ו-b = 0.8 נותנים
he: ‏13101/20125, בדיוק התשובה של סעיף ב.
en: Check: a = 0.6 and b = 0.8 give
en: 13101/20125, exactly the answer of part B.

he: אלה גבולות : שרביט קצת מתחת ל-a
he: מתקרב אליהם כמה שרוצים.
en: These are limits: a wand just below a
en: gets as close to them as you like.

he: מסתתרים כשהביטוי הזה גדול מ-1 − a,
he: הסיכוי של הצלף.
en: Hide when this expression is greater than 1 − a,
en: the sniper's chance.

he: האיבר הראשון לבדו עובר את 1 − a
he: כש-a > 2 − √2, כ-0.586.
en: The first term alone beats 1 − a
en: when a > 2 − √2, about 0.586.

he: עם שני האיברים האחרים, הסף a* נמוך יותר,
he: ותלוי מעט ב-b : בין 0.456 ל-0.478.
en: With the other two terms the threshold a* is lower,
en: and depends a little on b: between 0.456 and 0.478.

he: מתחת לסף, צלף ראשון. מעליו, להסתתר.
he: בסעיף ב, a = 0.6, ולכן מסתתרים.
en: Below the threshold, sniper first. Above it, hide.
en: In part B, a = 0.6, so we hide.

he: הכלל על כמה זוגות יריבים : בכל שורה
he: הסיכוי בכל תוכנית, והבחירה.
en: The rule on a few pairs of rivals: each row
en: has the chance of each plan, and the choice.

he: ‏0.4 ו-0.8 מתחת לסף : צלף, 60%.
he: ‏0.47 ו-0.9 כבר מעליו : להסתתר.
en: 0.4 and 0.8 are below the threshold: sniper, 60%.
en: 0.47 and 0.9 are already above it: hide.

he: ‏0.47 ו-0.55 : הסף עולה כש-b קטן,
he: וצלף מנצח בקושי. ו-0.7 ו-0.9 : ‏73.8%.
en: 0.47 and 0.55: the threshold rises as b shrinks,
en: and the sniper barely wins. And 0.7 and 0.9: 73.8%.

he: בתיבה : יריבים 0.4 ו-0.8,
he: מתחת לסף.
en: In the box: rivals 0.4 and 0.8,
en: below the threshold.

he: הבחירה הטובה : צלף ראשון, 60%,
he: מול 48.6% אם מסתתרים.
en: The best choice: sniper first, 60%,
en: against 48.6% when hiding.

he: ועכשיו יריבים 0.7 ו-0.9,
he: מעל הסף.
en: And now rivals 0.7 and 0.9,
en: above the threshold.

he: הבחירה : שלישי, ממש מתחת ל-0.7,
he: עם 73.8%.
en: The choice: third, just below 0.7,
en: with 73.8%.

he: לסיכום : להיות החלש, לכשף אחרון,
he: ולתת לחזקים להילחם ביניהם.
en: In short: be the weakest, cast last,
en: and let the strong ones fight each other.

he: נסו יריבים משלכם בתיבה
he: שבעמוד של שאלה 0071 באתר.
en: Try your own rivals in the box
en: on the page of question 0071 on the site.
