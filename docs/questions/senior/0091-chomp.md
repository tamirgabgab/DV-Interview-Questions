---
id: 91
title: Chomp – טבלת השוקולד המורעלת, גניבת אסטרטגיה וחיפוש עם זיכרון
level: senior
difficulty: medium
kind: math
tags: [game-theory, logic-puzzles, algorithms, dynamic-programming, recursion, proof, python, systemverilog]
source: "משחק קלאסי (Gale, 1974); הוכחת גניבת האסטרטגיה"
added: 2026-11-06
---

## השאלה

שני שחקנים מתחלקים בטבלת שוקולד של \( m \) שורות ו-\( n \) עמודות. נקרא למשבצות כמו בלוח
שחמט : העמודות a, b, c, ... משמאל לימין, והשורות 1, 2, 3, ... מלמטה למעלה. המשבצת a1, בפינה
השמאלית התחתונה, מורעלת.

בכל תור השחקן בוחר משבצת שעוד נשארה, ואוכל אותה ואת כל המשבצות שמעליה ומימינה : כל משבצת
שהעמודה שלה לא משמאל לזו שנבחרה, והשורה שלה לא מתחתיה. השחקנים מתחלפים, ושניהם משחקים הכי
טוב שאפשר. מי שאוכל את a1 מפסיד, ולכן מי שנשארה לו רק a1 בתורו הפסיד. למשל, ב-4 על 4, מי
שבוחר את c3 אוכל ארבע משבצות :

<!-- gen 0 -->

<svg class="figure cp-fig" viewBox="0 0 264 160" style="max-width:16.5rem" role="img" aria-label="טבלת שוקולד של 4 על 4. העמודות a עד d משמאל לימין, השורות 1 עד 4 מלמטה למעלה, והמשבצת המורעלת a1 בפינה השמאלית התחתונה. מימין הטבלה לפני המהלך, משמאל אחריו : מי שבוחר את c3 אוכל אותה ואת כל מה שמעליה ומימינה, c3, d3, c4 ו-d4, ונשארות 12 משבצות"><rect class="cp-poison" x="167" y="95" width="22" height="22" rx="3"/><path class="cp-cross" d="M171.28,99.28 L184.72,112.72 M171.28,112.72 L184.72,99.28"/><rect class="cp-sq" x="167" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="167" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="167" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="191" y="95" width="22" height="22" rx="3"/><rect class="cp-sq" x="191" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="191" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="191" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="215" y="95" width="22" height="22" rx="3"/><rect class="cp-sq" x="215" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="215" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="215" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="239" y="95" width="22" height="22" rx="3"/><rect class="cp-sq" x="239" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="239" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="239" y="23" width="22" height="22" rx="3"/><text class="cp-lab" x="178" y="131" text-anchor="middle">a</text><text class="cp-lab" x="202" y="131" text-anchor="middle">b</text><text class="cp-lab" x="226" y="131" text-anchor="middle">c</text><text class="cp-lab" x="250" y="131" text-anchor="middle">d</text><text class="cp-lab" x="157" y="110" text-anchor="middle">1</text><text class="cp-lab" x="157" y="86" text-anchor="middle">2</text><text class="cp-lab" x="157" y="62" text-anchor="middle">3</text><text class="cp-lab" x="157" y="38" text-anchor="middle">4</text><text class="cp-cap" x="214" y="150" text-anchor="middle" direction="rtl">לפני</text><rect class="cp-poison" x="17" y="95" width="22" height="22" rx="3"/><path class="cp-cross" d="M21.28,99.28 L34.72,112.72 M21.28,112.72 L34.72,99.28"/><rect class="cp-sq" x="17" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="17" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="17" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="41" y="95" width="22" height="22" rx="3"/><rect class="cp-sq" x="41" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="41" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="41" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="65" y="95" width="22" height="22" rx="3"/><rect class="cp-sq" x="65" y="71" width="22" height="22" rx="3"/><rect class="cp-gone" x="66" y="48" width="20" height="20" rx="3"/><rect class="cp-gone" x="66" y="24" width="20" height="20" rx="3"/><rect class="cp-sq" x="89" y="95" width="22" height="22" rx="3"/><rect class="cp-sq" x="89" y="71" width="22" height="22" rx="3"/><rect class="cp-gone" x="90" y="48" width="20" height="20" rx="3"/><rect class="cp-gone" x="90" y="24" width="20" height="20" rx="3"/><rect class="cp-pick" x="65" y="47" width="22" height="22" rx="3"/><text class="cp-lab" x="28" y="131" text-anchor="middle">a</text><text class="cp-lab" x="52" y="131" text-anchor="middle">b</text><text class="cp-lab" x="76" y="131" text-anchor="middle">c</text><text class="cp-lab" x="100" y="131" text-anchor="middle">d</text><text class="cp-lab" x="7" y="110" text-anchor="middle">1</text><text class="cp-lab" x="7" y="86" text-anchor="middle">2</text><text class="cp-lab" x="7" y="62" text-anchor="middle">3</text><text class="cp-lab" x="7" y="38" text-anchor="middle">4</text><text class="cp-cap" x="64" y="150" text-anchor="middle" direction="rtl">אחרי c3</text></svg>

<span class="viz-legend"><span><i class="cp-key-sq"></i>שוקולד</span><span><i class="cp-key-poison"></i>המשבצת המורעלת, a1</span><span><i class="cp-key-pick"></i>המשבצת שנבחרה</span><span><i class="cp-key-gone"></i>מה שהמהלך אכל</span></span>

<!-- /gen -->

- **סעיף א – לוח 4 על 4 :** מי מנצח, ובאיזה מהלך ראשון?
- **סעיף ב – לוח 8 על 8 :** ומה בלוח של 8 על 8, או בכל לוח ריבועי? כתבו תוכנית שבודקת את
  התשובה.
- **סעיף ג – לוח m על n :** מי מנצח בלוח מלבני כללי? איך מוצאים מהלך מנצח, כמה זה עולה, ומה
  האסטרטגיה המפורשת בלוח של 2 שורות?

??? interviewer "מה המראיין בודק"
    - **סימטריה :** האם המועמד מחפש מהלך ראשון שמשאיר מצב סימטרי, ואז מחקה את היריב.
    - **הוכחת קיום :** גניבת האסטרטגיה מוכיחה שהראשון מנצח בלי לומר איך. האם המועמד יודע
      להסביר למה ההוכחה תקפה, ומה היא לא נותנת.
    - **מצב המשחק :** האם הוא רואה שהמצב הוא "מדרגות", גובה לכל עמודה, ולא קבוצה כלשהי של
      משבצות. זה ההבדל בין \( \binom{m+n}{n} \) מצבים ל-\( 2^{mn} \).
    - **חיפוש עם זיכרון :** מצב מנצח אם יש ממנו מהלך למצב מפסיד. האם הקוד מגדיר נכון את
      סוף המשחק, ולא הופך בטעות את החוק.
    - **מה לא ידוע :** אין נוסחה לכל לוח. מועמד טוב יודע לומר מה מוכח, מה מחושב, ומה פתוח.

---

### סעיף א – לוח 4 על 4

מי מנצח בלוח של 4 על 4, ובאיזה מהלך ראשון?

??? tip "רמז 1"
    התחילו מלוח של 2 על 2. מה קורה אם הראשון אוכל את b2? ואם הוא אוכל את b1 או את a2?

??? tip "רמז 2"
    חפשו מהלך ראשון שמשאיר צורה סימטרית, כך שכל מהלך של היריב בצד אחד אפשר להעתיק בצד השני.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        הראשון מנצח : הוא אוכל את b2, ונשארת צורת L של שתי זרועות שוות, a2 עד a4 למעלה ו-b1
        עד d1 ימינה. מעכשיו, על כל מהלך של היריב בזרוע אחת הוא עונה באותו מהלך בזרוע השנייה,
        כמו במראה. שתי הזרועות נשארות שוות, ולכן ליריב תמיד יש מה לאכול אחרי הראשון, עד שנשארת
        לו רק a1.

    <!-- cost: זמן \( O(n) \) למהלך | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    **אחרי b2.** המהלך b2 אוכל את כל הריבוע של 3 על 3 מעל a1 ומימינה. נשארות רק השורה
    התחתונה והעמודה השמאלית, כלומר a1 ושתי זרועות : הזרוע העליונה a2, a3, a4, והזרוע הימנית
    b1, c1, d1. כל זרוע היא שורה פשוטה : משבצת שנבחרת בזרוע אוכלת אותה ואת כל מה שאחריה
    בזרוע, ולא נוגעת בזרוע השנייה.

    **מראה.** ‏L עם שתי זרועות שוות הוא מצב מפסיד למי שתורו : אם הוא מקצר זרוע אחת לאורך
    \( k \), עונים בקיצור הזרוע השנייה לאותו \( k \). ההתחלה אחרי b2, וכך משחק שלם :

    <!-- gen 1 -->

    <svg class="figure cp-fig" viewBox="0 0 378 160" style="max-width:23.6rem" role="img" aria-label="משחק על 4 על 4, חלק ראשון. ההתחלה; אתם אוכלים את b2, ונשארת צורת L : הזרוע העליונה a2, a3, a4 והזרוע הימנית b1, c1, d1, שלוש משבצות בכל אחת; היריב אוכל את d1, ונשארות שתיים בזרוע הימנית"><rect class="cp-poison" x="281" y="95" width="22" height="22" rx="3"/><path class="cp-cross" d="M285.28,99.28 L298.72,112.72 M285.28,112.72 L298.72,99.28"/><rect class="cp-sq" x="281" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="281" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="281" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="305" y="95" width="22" height="22" rx="3"/><rect class="cp-sq" x="305" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="305" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="305" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="329" y="95" width="22" height="22" rx="3"/><rect class="cp-sq" x="329" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="329" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="329" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="353" y="95" width="22" height="22" rx="3"/><rect class="cp-sq" x="353" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="353" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="353" y="23" width="22" height="22" rx="3"/><text class="cp-lab" x="292" y="131" text-anchor="middle">a</text><text class="cp-lab" x="316" y="131" text-anchor="middle">b</text><text class="cp-lab" x="340" y="131" text-anchor="middle">c</text><text class="cp-lab" x="364" y="131" text-anchor="middle">d</text><text class="cp-lab" x="271" y="110" text-anchor="middle">1</text><text class="cp-lab" x="271" y="86" text-anchor="middle">2</text><text class="cp-lab" x="271" y="62" text-anchor="middle">3</text><text class="cp-lab" x="271" y="38" text-anchor="middle">4</text><text class="cp-cap" x="328" y="150" text-anchor="middle" direction="rtl">ההתחלה</text><rect class="cp-poison" x="149" y="95" width="22" height="22" rx="3"/><path class="cp-cross" d="M153.28,99.28 L166.72,112.72 M153.28,112.72 L166.72,99.28"/><rect class="cp-sq" x="149" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="149" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="149" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="173" y="95" width="22" height="22" rx="3"/><rect class="cp-gone" x="174" y="72" width="20" height="20" rx="3"/><rect class="cp-gone" x="174" y="48" width="20" height="20" rx="3"/><rect class="cp-gone" x="174" y="24" width="20" height="20" rx="3"/><rect class="cp-sq" x="197" y="95" width="22" height="22" rx="3"/><rect class="cp-gone" x="198" y="72" width="20" height="20" rx="3"/><rect class="cp-gone" x="198" y="48" width="20" height="20" rx="3"/><rect class="cp-gone" x="198" y="24" width="20" height="20" rx="3"/><rect class="cp-sq" x="221" y="95" width="22" height="22" rx="3"/><rect class="cp-gone" x="222" y="72" width="20" height="20" rx="3"/><rect class="cp-gone" x="222" y="48" width="20" height="20" rx="3"/><rect class="cp-gone" x="222" y="24" width="20" height="20" rx="3"/><rect class="cp-pick" x="173" y="71" width="22" height="22" rx="3"/><text class="cp-lab" x="160" y="131" text-anchor="middle">a</text><text class="cp-lab" x="184" y="131" text-anchor="middle">b</text><text class="cp-lab" x="208" y="131" text-anchor="middle">c</text><text class="cp-lab" x="232" y="131" text-anchor="middle">d</text><text class="cp-lab" x="139" y="110" text-anchor="middle">1</text><text class="cp-lab" x="139" y="86" text-anchor="middle">2</text><text class="cp-lab" x="139" y="62" text-anchor="middle">3</text><text class="cp-lab" x="139" y="38" text-anchor="middle">4</text><text class="cp-cap" x="196" y="150" text-anchor="middle" direction="rtl">אתם : b2</text><rect class="cp-poison" x="17" y="95" width="22" height="22" rx="3"/><path class="cp-cross" d="M21.28,99.28 L34.72,112.72 M21.28,112.72 L34.72,99.28"/><rect class="cp-sq" x="17" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="17" y="47" width="22" height="22" rx="3"/><rect class="cp-sq" x="17" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="41" y="95" width="22" height="22" rx="3"/><rect class="cp-empty" x="41" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="41" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="41" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="65" y="95" width="22" height="22" rx="3"/><rect class="cp-empty" x="65" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="65" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="65" y="23" width="22" height="22" rx="3"/><rect class="cp-gone" x="90" y="96" width="20" height="20" rx="3"/><rect class="cp-empty" x="89" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="89" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="89" y="23" width="22" height="22" rx="3"/><rect class="cp-pick" x="89" y="95" width="22" height="22" rx="3"/><text class="cp-lab" x="28" y="131" text-anchor="middle">a</text><text class="cp-lab" x="52" y="131" text-anchor="middle">b</text><text class="cp-lab" x="76" y="131" text-anchor="middle">c</text><text class="cp-lab" x="100" y="131" text-anchor="middle">d</text><text class="cp-lab" x="7" y="110" text-anchor="middle">1</text><text class="cp-lab" x="7" y="86" text-anchor="middle">2</text><text class="cp-lab" x="7" y="62" text-anchor="middle">3</text><text class="cp-lab" x="7" y="38" text-anchor="middle">4</text><text class="cp-cap" x="64" y="150" text-anchor="middle" direction="rtl">היריב : d1</text></svg>

    <!-- /gen -->

    <!-- gen 2 -->

    <svg class="figure cp-fig" viewBox="0 0 378 160" style="max-width:23.6rem" role="img" aria-label="משחק על 4 על 4, חלק שני. אתם עונים ב-a4, ושוב שתי הזרועות שוות, שתיים בכל אחת; היריב אוכל את b1, והזרוע הימנית נעלמת; אתם אוכלים את a2, והזרוע העליונה נעלמת. נשארה רק a1 המורעלת, והיריב חייב לאכול אותה"><rect class="cp-poison" x="281" y="95" width="22" height="22" rx="3"/><path class="cp-cross" d="M285.28,99.28 L298.72,112.72 M285.28,112.72 L298.72,99.28"/><rect class="cp-sq" x="281" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="281" y="47" width="22" height="22" rx="3"/><rect class="cp-gone" x="282" y="24" width="20" height="20" rx="3"/><rect class="cp-sq" x="305" y="95" width="22" height="22" rx="3"/><rect class="cp-empty" x="305" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="305" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="305" y="23" width="22" height="22" rx="3"/><rect class="cp-sq" x="329" y="95" width="22" height="22" rx="3"/><rect class="cp-empty" x="329" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="329" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="329" y="23" width="22" height="22" rx="3"/><rect class="cp-empty" x="353" y="95" width="22" height="22" rx="3"/><rect class="cp-empty" x="353" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="353" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="353" y="23" width="22" height="22" rx="3"/><rect class="cp-pick" x="281" y="23" width="22" height="22" rx="3"/><text class="cp-lab" x="292" y="131" text-anchor="middle">a</text><text class="cp-lab" x="316" y="131" text-anchor="middle">b</text><text class="cp-lab" x="340" y="131" text-anchor="middle">c</text><text class="cp-lab" x="364" y="131" text-anchor="middle">d</text><text class="cp-lab" x="271" y="110" text-anchor="middle">1</text><text class="cp-lab" x="271" y="86" text-anchor="middle">2</text><text class="cp-lab" x="271" y="62" text-anchor="middle">3</text><text class="cp-lab" x="271" y="38" text-anchor="middle">4</text><text class="cp-cap" x="328" y="150" text-anchor="middle" direction="rtl">אתם : a4</text><rect class="cp-poison" x="149" y="95" width="22" height="22" rx="3"/><path class="cp-cross" d="M153.28,99.28 L166.72,112.72 M153.28,112.72 L166.72,99.28"/><rect class="cp-sq" x="149" y="71" width="22" height="22" rx="3"/><rect class="cp-sq" x="149" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="149" y="23" width="22" height="22" rx="3"/><rect class="cp-gone" x="174" y="96" width="20" height="20" rx="3"/><rect class="cp-empty" x="173" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="173" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="173" y="23" width="22" height="22" rx="3"/><rect class="cp-gone" x="198" y="96" width="20" height="20" rx="3"/><rect class="cp-empty" x="197" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="197" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="197" y="23" width="22" height="22" rx="3"/><rect class="cp-empty" x="221" y="95" width="22" height="22" rx="3"/><rect class="cp-empty" x="221" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="221" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="221" y="23" width="22" height="22" rx="3"/><rect class="cp-pick" x="173" y="95" width="22" height="22" rx="3"/><text class="cp-lab" x="160" y="131" text-anchor="middle">a</text><text class="cp-lab" x="184" y="131" text-anchor="middle">b</text><text class="cp-lab" x="208" y="131" text-anchor="middle">c</text><text class="cp-lab" x="232" y="131" text-anchor="middle">d</text><text class="cp-lab" x="139" y="110" text-anchor="middle">1</text><text class="cp-lab" x="139" y="86" text-anchor="middle">2</text><text class="cp-lab" x="139" y="62" text-anchor="middle">3</text><text class="cp-lab" x="139" y="38" text-anchor="middle">4</text><text class="cp-cap" x="196" y="150" text-anchor="middle" direction="rtl">היריב : b1</text><rect class="cp-poison" x="17" y="95" width="22" height="22" rx="3"/><path class="cp-cross" d="M21.28,99.28 L34.72,112.72 M21.28,112.72 L34.72,99.28"/><rect class="cp-gone" x="18" y="72" width="20" height="20" rx="3"/><rect class="cp-gone" x="18" y="48" width="20" height="20" rx="3"/><rect class="cp-empty" x="17" y="23" width="22" height="22" rx="3"/><rect class="cp-empty" x="41" y="95" width="22" height="22" rx="3"/><rect class="cp-empty" x="41" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="41" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="41" y="23" width="22" height="22" rx="3"/><rect class="cp-empty" x="65" y="95" width="22" height="22" rx="3"/><rect class="cp-empty" x="65" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="65" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="65" y="23" width="22" height="22" rx="3"/><rect class="cp-empty" x="89" y="95" width="22" height="22" rx="3"/><rect class="cp-empty" x="89" y="71" width="22" height="22" rx="3"/><rect class="cp-empty" x="89" y="47" width="22" height="22" rx="3"/><rect class="cp-empty" x="89" y="23" width="22" height="22" rx="3"/><rect class="cp-pick" x="17" y="71" width="22" height="22" rx="3"/><text class="cp-lab" x="28" y="131" text-anchor="middle">a</text><text class="cp-lab" x="52" y="131" text-anchor="middle">b</text><text class="cp-lab" x="76" y="131" text-anchor="middle">c</text><text class="cp-lab" x="100" y="131" text-anchor="middle">d</text><text class="cp-lab" x="7" y="110" text-anchor="middle">1</text><text class="cp-lab" x="7" y="86" text-anchor="middle">2</text><text class="cp-lab" x="7" y="62" text-anchor="middle">3</text><text class="cp-lab" x="7" y="38" text-anchor="middle">4</text><text class="cp-cap" x="64" y="150" text-anchor="middle" direction="rtl">אתם : a2</text></svg>

    <span class="viz-legend"><span><i class="cp-key-pick"></i>המשבצת שנבחרה</span><span><i class="cp-key-gone"></i>מה שהמהלך אכל</span><span><i class="cp-key-poison"></i>המשבצת המורעלת, a1</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המהלך הראשון :** אוכלים את b2. נשארות שתי זרועות של 3 משבצות.
    2. **התשובה :** אחרי כל מהלך של היריב סופרים את שתי הזרועות. אם הזרוע העליונה ארוכה
       יותר, מקצרים אותה לאורך של הימנית. ואם הימנית ארוכה יותר, מקצרים אותה.
    3. **הסוף :** כששתי הזרועות ריקות, נשארת רק a1, ותורו של היריב.

    </div>

    #### הקוד { .sol-code }

    מצב הוא הגובה של כל עמודה, מ-a ימינה, ומשבצת היא זוג אינדקסים מ-0 : עמודה ושורה. כך b2
    היא `(1, 1)` ו-a1 היא `(0, 0)`.

    === "Python"
        ```python title="mirror_move" linenums="1" hl_lines="5 6 7 8 9 10 11 12"
        def mirror_move(h: tuple):
            """The mirror strategy on a square board, for the full board or the L left after b2.
            h: the column heights, column a first (the poison is at the bottom of column a).
            Returns the square to eat as (column, row), 0-based, or None when the two arms
            are already equal."""
            if len(h) > 1 and h[1] > 1:
                return 1, 1                               # (1)!
            up = h[0] - 1                                 # (2)!
            right = sum(1 for x in h if x > 0) - 1
            if up > right:
                return 0, right + 1                       # (3)!
            if right > up:
                return up + 1, 0
            return None                                   # (4)!
        ```

        1. ‏b2 עוד שם : זו ההתחלה, והמהלך הוא b2. הפונקציה מניחה שקוראים לה על הלוח המלא או על
           ה-L שנשאר אחרי b2. במצב אחר, שבו היריב כבר אכל משהו לפני b2, המהלך b2 לא בהכרח מנצח.
        2. אחרי b2 נשארת צורת L : הזרוע העליונה היא העמודה a בלי a1, והימנית היא השורה 1 בלי a1.
        3. הזרוע העליונה ארוכה יותר : אוכלים בעמודה a את המשבצת שמעל אורך הזרוע הימנית.
        4. הזרועות שוות : מי שתורו מפסיד, ואין מהלך שמציל אותו.

    === "SystemVerilog"
        ```systemverilog title="mirror_move" linenums="1" hl_lines="6 7 9 11 12 13"
        // the mirror strategy on an n x n board. h packs the column heights, 4 bits a column:
        // column a in bits 3:0, column b in bits 7:4, and so on. The square to eat comes out
        // in col and row (0-based); returns 0 when the two arms are already equal
        function automatic bit mirror_move(int h, int n, output int col, output int row);
          int up, right;
          if (n > 1 && h[7:4] > 1) begin                       // (1)!
            col = 1; row = 1; return 1;
          end
          up = h[3:0] - 1;                                      // (2)!
          right = -1;
          for (int c = 0; c < n; c++) if (h[4*c +: 4] > 0) right++;
          if (up > right) begin col = 0; row = right + 1; return 1; end   // (3)!
          if (right > up) begin col = up + 1; row = 0; return 1; end
          return 0;                                             // (4)!
        endfunction
        ```

        1. ‏b2 עוד שם : המהלך הראשון.
        2. אורך הזרוע העליונה, וספירת העמודות שלא ריקות לאורך הזרוע הימנית.
        3. מקצרים את הזרוע הארוכה לאורך של הקצרה.
        4. הזרועות שוות : אין מהלך מנצח.

    #### למה זה נכון { .sol-proof }

    נקרא \( L_k \) למצב של a1 ושתי זרועות של \( k \) משבצות כל אחת. הטענה : מי שתורו ב-\( L_k \)
    מפסיד. באינדוקציה על \( k \) :

    1. **‏k = 0 :** נשארה רק a1, ומי שתורו חייב לאכול אותה.
    2. **מ-L עם זרועות שוות יוצאים :** כל מהלך, חוץ מ-a1 שמפסיד מיד, הוא משבצת באחת הזרועות,
       ומקצר רק אותה, לאורך \( j < k \). הזרוע השנייה נשארת באורך \( k \).
    3. **ל-L עם זרועות שוות חוזרים :** עונים בקיצור הזרוע השנייה לאותו \( j \), ומגיעים
       ל-\( L_j \), שלפי ההנחה מפסיד למי שתורו, כלומר ליריב.

    המהלך b2 מעביר את הלוח המלא ל-\( L_3 \), ולכן הראשון מנצח. ומי שמשחק כך לא נתקע אף פעם : אחרי
    כל מהלך של היריב יש זרוע ארוכה יותר, ובה מהלך.

    **נסו בעצמכם.** בתיבה המחשב הוא הראשון : הוא פותח ב-b2 ומשחק במראה, ואתם היריב. היא מוסיפה
    לציור משחק שלם נגד כל תשובה שתבחרו.

    - לחצו על d1 : המחשב עונה ב-a4, ונשארות 2 משבצות בכל זרוע, כמו בציור. אחר כך לחצו על b1 : הוא
      אוכל את a2, ואחרי 5 מהלכים נשארה לכם רק a1.
    - התחילו משחק חדש ולחצו על a2, כל הזרוע העליונה : המחשב עונה ב-b1, והפסדתם אחרי 3 מהלכים. זה
      המשחק הקצר ביותר.
    - בחרו לוח של 8 על 8 ולחצו על "מהלך אקראי של היריב" עד הסוף : אחרי כל תשובה של המחשב שתי
      הזרועות שוות, והמשחק לא עובר 15 מהלכים.

    <div class="explorer" data-kind="chomp" data-mode="mirror" data-n="4"></div>

    #### סיבוכיות { .sol-cost }

    מהלך של המראה סופר את העמודות שלא ריקות : \( O(n) \) זמן, וזיכרון קבוע. אין שום חיפוש.

---

### סעיף ב – לוח 8 על 8

מי מנצח בלוח של 8 על 8, ובכל לוח ריבועי? כתבו תוכנית שבודקת את התשובה, בלי להניח אותה.

??? tip "רמז 1"
    האם המראה של סעיף א השתמשה במשהו שנכון רק ב-4 על 4?

??? tip "רמז 2"
    לבדיקה : מצב מנצח למי שתורו אם יש ממנו מהלך למצב מפסיד, ומפסיד אם כל המהלכים ממנו מובילים
    למצבים מנצחים. כמה מצבים שונים יכולים להופיע? הסתכלו על הגבהים של העמודות.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        אותה תשובה : בכל לוח של \( n \) על \( n \), עם \( n \ge 2 \), הראשון מנצח באכילת b2 ובמראה,
        כי אחרי b2 שתי הזרועות הן באורך \( n - 1 \). חיפוש עם זיכרון על כל המצבים מאשר : ב-8 על 8
        יש 12,869 מצבים עם המשבצת המורעלת, ו-b2 הוא המהלך הראשון המנצח היחיד.

    <!-- cost: מצבים \( \binom{2n}{n} \) | זמן \( O\big(\binom{2n}{n}\, n^3\big) \) | זיכרון \( O\big(\binom{2n}{n}\big) \) -->

    #### הרעיון { .sol-idea }

    **המראה בכל ריבוע.** בלוח של \( n \) על \( n \) המהלך b2 משאיר את a1 ושתי זרועות : a2 עד
    \( a_n \) למעלה, ו-b1 עד המשבצת האחרונה בשורה 1 ימינה. לשתיהן \( n - 1 \) משבצות, כי הלוח
    ריבועי. ההוכחה של סעיף א עובדת מילה במילה.

    **מצב הוא מדרגות.** כדי לבדוק בלי להניח את התשובה, מחפשים על כל המצבים. אחרי כל מהלך,
    הגובה של כל עמודה לא גדל משמאל לימין : אם משבצת נאכלה, נאכל גם כל מה שמימינה ומעליה. לכן
    מצב הוא רשימת גבהים יורדת, כמו מדרגות, ולא קבוצה כלשהי של משבצות. מהלך ב-\( (c, r) \) הופך
    כל גובה מעמודה \( c \) ימינה ל-\( \min(h, r) \).

    **מנצח ומפסיד.** מי שתורו מנצח אם יש מהלך, שאינו a1, שמשאיר ליריב מצב מפסיד. כשנשארה רק a1
    אין מהלך כזה, והוא מפסיד. כל מהלך מקטין את מספר המשבצות, ולכן ההגדרה לא מעגלית, וזיכרון
    של כל מצב שכבר חושב מונע לחשב אותו שוב. בלוחות הריבועיים :

    <!-- gen 3 -->

    | הלוח | מצבים עם המשבצת המורעלת | המהלכים הראשונים המנצחים | המראה מנצחת כל תשובה |
    |:-:|:-:|:-:|:-:|
    | ‏2 × 2 | ‏5 | ‏b2 | כן |
    | ‏3 × 3 | ‏19 | ‏b2 | כן |
    | ‏4 × 4 | ‏69 | ‏b2 | כן |
    | ‏5 × 5 | ‏251 | ‏b2 | כן |
    | ‏6 × 6 | ‏923 | ‏b2 | כן |
    | ‏7 × 7 | ‏3,431 | ‏b2 | כן |
    | ‏8 × 8 | ‏12,869 | ‏b2 | כן |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המצב :** רשימת הגבהים של העמודות, יורדת משמאל לימין.
    2. **המהלכים :** כל משבצת \( (c, r) \) שנשארה, חוץ מ-a1. אחרי המהלך כל גובה מ-\( c \) ימינה
       הוא לכל היותר \( r \).
    3. **מנצח :** מצב מנצח אם אחד המהלכים מוביל למצב מפסיד. עם a1 לבד אין מהלכים, והמצב מפסיד.
    4. **זיכרון :** שומרים את התוצאה של כל מצב. כל מצב מחושב פעם אחת.
    5. **המהלכים המנצחים :** מהלוח המלא, כל מהלך שמוביל למצב מפסיד.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="eat, moves, wins, winning_moves" linenums="1" hl_lines="6 13 14 20 25"
        from functools import lru_cache


        def eat(h: tuple, c: int, r: int) -> tuple:
            """Eat column c, row r (0-based): every column from c on keeps at most r squares."""
            return tuple(min(x, r) if i >= c else x for i, x in enumerate(h))   # (1)!


        def moves(h: tuple):
            """Every move but the poison, with the staircase after it."""
            for c, height in enumerate(h):
                for r in range(height):
                    if (c, r) != (0, 0):
                        yield (c, r), eat(h, c, r)


        @lru_cache(maxsize=None)
        def wins(h: tuple) -> bool:
            """The player to move wins from the staircase h."""
            return any(not wins(t) for _, t in moves(h))                       # (2)!


        def winning_moves(m: int, n: int) -> list:
            """The winning first moves on m rows x n columns, as (column, row), 0-based."""
            return [mv for mv, t in moves((m,) * n) if not wins(t)]            # (3)!
        ```

        1. המשבצת \( (c, r) \) ומה שמעליה ומימינה : כל עמודה מ-\( c \) ימינה נשארת עם \( r \)
           משבצות לכל היותר. המדרגות נשארות מדרגות.
        2. ‏`any` על רשימה ריקה הוא `False` : עם a1 לבד אין מהלכים, ומי שתורו מפסיד. ‏`lru_cache`
           הוא הזיכרון, לפי רשימת הגבהים.
        3. מהלך ראשון מנצח הוא מהלך שמשאיר ליריב מצב מפסיד.

    === "SystemVerilog"
        ```systemverilog title="eat, chomp_table, winning_first" linenums="1" hl_lines="5 14 18 19 20 21 22 23 24 25 26"
        // a staircase packs the column heights, 4 bits a column: column a in bits 3:0 (up to
        // 8 columns of up to 15 rows)
        function automatic int eat(int h, int n, int c, int r);
          for (int i = c; i < n; i++)
            if (h[4*i +: 4] > r) h[4*i +: 4] = r;                          // (1)!
          return h;
        endfunction

        // win[h]: the player to move wins from h, for every staircase of m rows x n columns
        function automatic void chomp_table(int m, int n, ref bit win[int]);
          int ht[8], h, i;
          bit any_lost;
          ht = '{default: 0};
          forever begin                                                    // (2)!
            h = 0;
            for (int c = 0; c < n; c++) h[4*c +: 4] = ht[c];
            any_lost = 0;
            for (int c = 0; c < n; c++)
              for (int r = 0; r < ht[c]; r++)
                if ((c != 0 || r != 0) && !win[eat(h, n, c, r)]) any_lost = 1;   // (3)!
            win[h] = any_lost;
            i = n - 1;                                                     // (4)!
            while (i >= 0 && ht[i] == (i == 0 ? m : ht[i - 1])) i--;
            if (i < 0) break;
            ht[i]++;
            for (int j = i + 1; j < n; j++) ht[j] = 0;
          end
        endfunction

        // the first winning first move on the full m x n board; returns 0 when there is none
        function automatic bit winning_first(int m, int n, ref bit win[int], output int col, output int row);
          int full = 0;
          for (int c = 0; c < n; c++) full[4*c +: 4] = m;
          for (int c = 0; c < n; c++)
            for (int r = 0; r < m; r++)
              if ((c != 0 || r != 0) && !win[eat(full, n, c, r)]) begin
                col = c; row = r; return 1;
              end
          return 0;
        endfunction
        ```

        1. גובה של עמודה הוא 4 ביטים במילה, ולכן הקוד מתאים ללוחות של עד 8 עמודות ו-15 שורות. כל
           עמודה מ-\( c \) ימינה יורדת ל-\( r \) לכל היותר.
        2. כל המדרגות בסדר מילוני עולה, מהמצב הריק ועד הלוח המלא, בלי רקורסיה. מהלך רק מוריד
           גבהים, ולכן המצב אחריו קטן ממנו בסדר המילוני, וכבר חושב.
        3. מהלך, שאינו a1, למצב מפסיד : המצב מנצח. עם a1 לבד אין מהלך כזה, והמצב מפסיד.
        4. המדרגה הבאה : מגדילים את הגובה הימני ביותר שעוד אפשר להגדיל בלי לעבור את העמודה
           שמשמאלו, ומאפסים את מה שמימינו. יוצאים בדיוק \( \binom{m+n}{n} \) מצבים.

    #### למה זה נכון { .sol-proof }

    **החיפוש.** באינדוקציה על מספר המשבצות : עם משבצת אחת, a1, אין מהלך מלבד לאכול את הרעל,
    ו-`wins` מחזירה `False`, נכון. במצב עם יותר משבצות, כל מהלך מוביל למצב קטן יותר, ש-`wins`
    שלו נכון לפי ההנחה. אם אחד מהם מפסיד למי שתורו שם, כלומר ליריב, המהלך אליו מנצח. ואם כולם
    מנצחים ליריב, כל מהלך מפסיד, ואכילת a1 מפסידה מיד. זו בדיוק ההגדרה של `wins`.

    **כמה מצבים.** רשימת גבהים יורדת של \( n \) עמודות עם גבהים מ-0 עד \( m \) היא מסלול על
    רשת : מהפינה השמאלית העליונה לימנית התחתונה, \( n \) צעדים ימינה ו-\( m \) צעדים למטה, לאורך
    השפה של המדרגות. יש \( \binom{m+n}{n} \) מסלולים כאלה, ומהם רק המצב הריק לא כולל את a1. ב-8 על
    8 זה \( \binom{16}{8} - 1 = 12{,}869 \), וכולם יכולים להופיע במשחק. הקוד ב-Python לא מחשב את כולם :
    `any` עוצרת במהלך הראשון שמוביל למצב מפסיד, וכדי לענות על הלוח המלא `wins` מחשבת רק 3,832 מצבים.
    הטבלה ב-SystemVerilog ממלאת את כולם.

    **המהלך b2 הוא היחיד.** מהלך ראשון בעמודה a או בשורה 1 משאיר מלבן גדול מ-1 על 1, ובמלבן כזה מי שתורו
    מנצח (סעיף ג). כל מהלך ראשון אחר, שאינו b2, לא נוגע בעמודה a ובשורה 1 ומשאיר את b2 על הלוח : היריב אוכל את
    b2, ומגיע בעצמו ל-L עם שתי זרועות שלמות ושוות.

    **נסו בעצמכם.** משחקים נגד המחשב על 8 על 8, והוא לא טועה. "סימון המהלכים" מוסיף לחיפוש את
    התשובה שלו לכל משבצת, בכל מצב : מסגרת ירוקה למהלך מנצח, ונקודה אפורה למהלך שמשאיר ליריב מצב
    מנצח.

    - הדליקו את הסימון : בהתחלה רק b2 ירוקה.
    - אכלו את h8, הפינה : המחשב עונה ב-b2 ואוכל 48 משבצות, ועכשיו אין אף משבצת ירוקה.
    - בחרו שהמחשב מתחיל : הוא פותח ב-b2, והשורה שליד הלוח אומרת שאין מהלך מנצח.
    - חזרו להתחיל בעצמכם ואכלו את c3 : המחשב עונה ב-a8, לא ב-b2, ושוב אין משבצת ירוקה.

    <div class="explorer" data-kind="chomp" data-mode="play" data-m="8" data-n="8"></div>

    #### סיבוכיות { .sol-cost }

    יש \( \binom{2n}{n} \) מצבים, בערך \( 4^n / \sqrt{\pi n} \). מכל מצב יש עד \( n^2 \) מהלכים, וכל
    מהלך בונה רשימה של \( n \) גבהים : \( O\big(\binom{2n}{n}\, n^3\big) \) זמן ו-\( O\big(\binom{2n}{n}\big) \)
    זיכרון. ב-8 על 8 אלה כמה מיליוני צעדים פשוטים, פחות משנייה. בלי המדרגות, כל קבוצה של משבצות הייתה מצב :
    \( 2^{64} \).

---

### סעיף ג – לוח m על n

מי מנצח בלוח של \( m \) שורות ו-\( n \) עמודות, ואיך מוצאים מהלך מנצח? כמה זה עולה? ומה
האסטרטגיה המפורשת כשיש 2 שורות?

??? tip "רמז 1"
    אל תחפשו את המהלך המנצח. הניחו שהשני מנצח, וחפשו סתירה.

??? tip "רמז 2"
    נסו מהלך ראשון קטן ככל האפשר : המשבצת הימנית העליונה לבדה. מה משותף לכל תשובה של השני?

??? tip "רמז 3"
    בשתי שורות, השוו את האורך של השורה התחתונה לאורך של העליונה. איזה הפרש מפסיד למי שתורו?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        הראשון מנצח בכל לוח חוץ מ-1 על 1, וההוכחה היא גניבת אסטרטגיה, בלי לומר מה המהלך. כדי
        למצוא אותו מחפשים כמו בסעיף ב, על \( \binom{m+n}{n} \) מצבים. ב-2 שורות יש אסטרטגיה
        מפורשת : אוכלים את המשבצת הימנית העליונה, ומשאירים תמיד את השורה התחתונה ארוכה באחת
        מהעליונה. בלוח של 3 שורות ו-3 עמודות ומעלה, שאינו ריבוע, אין נוסחה ידועה, ויש רק חישוב.

    <!-- cost: מצבים \( \binom{m+n}{n} \) | זמן \( O\big(\binom{m+n}{n}\, m n^2\big) \) | שתי שורות \( O(1) \) למהלך -->

    #### הרעיון { .sol-idea }

    **גניבת אסטרטגיה.** נניח, בשלילה, שבלוח של \( m \) על \( n \), גדול מ-1 על 1, השני מנצח.
    הראשון אוכל רק את המשבצת הימנית העליונה. לפי ההנחה, לשני יש עכשיו תשובה \( X \) שמשאירה
    לראשון מצב מפסיד. אבל \( X \) אוכל גם את המשבצת הימנית העליונה, כי היא מעל \( X \) ומימינו.
    לכן המצב אחרי \( X \) לבד, כמהלך ראשון, זהה למצב אחרי שני המהלכים, והוא מפסיד למי שתורו :
    הראשון יכול היה לפתוח ב-\( X \) ולנצח. סתירה.

    <!-- gen 4 -->

    <svg class="figure cp-fig" viewBox="0 0 424 130" style="max-width:26.5rem" role="img" aria-label="גניבת אסטרטגיה על 3 על 5. בלוח הימני הראשון אוכל רק את הפינה הימנית העליונה, e3. באמצעי השני עונה במהלך המנצח שלו X, כאן d3. בשמאלי הראשון אוכל את X כבר במהלך הראשון, d3 יחד עם e3, ומקבל בדיוק אותו מצב, כי X אוכל גם את e3"><rect class="cp-poison" x="313" y="67" width="20" height="20" rx="3"/><path class="cp-cross" d="M316.84,70.84 L329.16,83.16 M316.84,83.16 L329.16,70.84"/><rect class="cp-sq" x="313" y="45" width="20" height="20" rx="3"/><rect class="cp-sq" x="313" y="23" width="20" height="20" rx="3"/><rect class="cp-sq" x="335" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="335" y="45" width="20" height="20" rx="3"/><rect class="cp-sq" x="335" y="23" width="20" height="20" rx="3"/><rect class="cp-sq" x="357" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="357" y="45" width="20" height="20" rx="3"/><rect class="cp-sq" x="357" y="23" width="20" height="20" rx="3"/><rect class="cp-sq" x="379" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="379" y="45" width="20" height="20" rx="3"/><rect class="cp-sq" x="379" y="23" width="20" height="20" rx="3"/><rect class="cp-sq" x="401" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="401" y="45" width="20" height="20" rx="3"/><rect class="cp-gone" x="402" y="24" width="18" height="18" rx="3"/><rect class="cp-pick" x="401" y="23" width="20" height="20" rx="3"/><text class="cp-lab" x="323" y="101" text-anchor="middle">a</text><text class="cp-lab" x="345" y="101" text-anchor="middle">b</text><text class="cp-lab" x="367" y="101" text-anchor="middle">c</text><text class="cp-lab" x="389" y="101" text-anchor="middle">d</text><text class="cp-lab" x="411" y="101" text-anchor="middle">e</text><text class="cp-lab" x="303" y="81" text-anchor="middle">1</text><text class="cp-lab" x="303" y="59" text-anchor="middle">2</text><text class="cp-lab" x="303" y="37" text-anchor="middle">3</text><text class="cp-cap" x="367" y="120" text-anchor="middle" direction="rtl">הראשון : e3</text><rect class="cp-poison" x="165" y="67" width="20" height="20" rx="3"/><path class="cp-cross" d="M168.84,70.84 L181.16,83.16 M168.84,83.16 L181.16,70.84"/><rect class="cp-sq" x="165" y="45" width="20" height="20" rx="3"/><rect class="cp-sq" x="165" y="23" width="20" height="20" rx="3"/><rect class="cp-sq" x="187" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="187" y="45" width="20" height="20" rx="3"/><rect class="cp-sq" x="187" y="23" width="20" height="20" rx="3"/><rect class="cp-sq" x="209" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="209" y="45" width="20" height="20" rx="3"/><rect class="cp-sq" x="209" y="23" width="20" height="20" rx="3"/><rect class="cp-sq" x="231" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="231" y="45" width="20" height="20" rx="3"/><rect class="cp-gone" x="232" y="24" width="18" height="18" rx="3"/><rect class="cp-sq" x="253" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="253" y="45" width="20" height="20" rx="3"/><rect class="cp-empty" x="253" y="23" width="20" height="20" rx="3"/><rect class="cp-pick" x="231" y="23" width="20" height="20" rx="3"/><text class="cp-lab" x="175" y="101" text-anchor="middle">a</text><text class="cp-lab" x="197" y="101" text-anchor="middle">b</text><text class="cp-lab" x="219" y="101" text-anchor="middle">c</text><text class="cp-lab" x="241" y="101" text-anchor="middle">d</text><text class="cp-lab" x="263" y="101" text-anchor="middle">e</text><text class="cp-lab" x="155" y="81" text-anchor="middle">1</text><text class="cp-lab" x="155" y="59" text-anchor="middle">2</text><text class="cp-lab" x="155" y="37" text-anchor="middle">3</text><text class="cp-cap" x="219" y="120" text-anchor="middle" direction="rtl">התשובה X</text><rect class="cp-poison" x="17" y="67" width="20" height="20" rx="3"/><path class="cp-cross" d="M20.84,70.84 L33.16,83.16 M20.84,83.16 L33.16,70.84"/><rect class="cp-sq" x="17" y="45" width="20" height="20" rx="3"/><rect class="cp-sq" x="17" y="23" width="20" height="20" rx="3"/><rect class="cp-sq" x="39" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="39" y="45" width="20" height="20" rx="3"/><rect class="cp-sq" x="39" y="23" width="20" height="20" rx="3"/><rect class="cp-sq" x="61" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="61" y="45" width="20" height="20" rx="3"/><rect class="cp-sq" x="61" y="23" width="20" height="20" rx="3"/><rect class="cp-sq" x="83" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="83" y="45" width="20" height="20" rx="3"/><rect class="cp-gone" x="84" y="24" width="18" height="18" rx="3"/><rect class="cp-sq" x="105" y="67" width="20" height="20" rx="3"/><rect class="cp-sq" x="105" y="45" width="20" height="20" rx="3"/><rect class="cp-gone" x="106" y="24" width="18" height="18" rx="3"/><rect class="cp-pick" x="83" y="23" width="20" height="20" rx="3"/><text class="cp-lab" x="27" y="101" text-anchor="middle">a</text><text class="cp-lab" x="49" y="101" text-anchor="middle">b</text><text class="cp-lab" x="71" y="101" text-anchor="middle">c</text><text class="cp-lab" x="93" y="101" text-anchor="middle">d</text><text class="cp-lab" x="115" y="101" text-anchor="middle">e</text><text class="cp-lab" x="7" y="81" text-anchor="middle">1</text><text class="cp-lab" x="7" y="59" text-anchor="middle">2</text><text class="cp-lab" x="7" y="37" text-anchor="middle">3</text><text class="cp-cap" x="71" y="120" text-anchor="middle" direction="rtl">רק X</text></svg>

    <!-- /gen -->

    בציור, ב-3 על 5, \( X \) הוא d3 : זו התשובה המנצחת היחידה ל-e3, וזה גם המהלך הראשון המנצח של
    הלוח. ההוכחה עצמה לא אומרת מה המהלך המנצח, ואפילו לא שהמשבצת הימנית העליונה היא מהלך טוב. ב-3
    על 3, למשל, היא מפסידה. כדי למצוא מהלך מחפשים כמו בסעיף ב.

    **שתי שורות.** בלוח של 2 על \( n \) הראשון אוכל את המשבצת הימנית העליונה, והשורה העליונה
    נשארת קצרה באחת מהתחתונה. מכאן, אם היריב מקצר את התחתונה לאורך \( k \), גם העליונה מתקצרת
    ל-\( k \) בדיוק, כי היא הייתה באורך \( k \) לפחות, והראשון מקצר אותה ל-\( k - 1 \). ואם היריב מקצר את העליונה ל-\( k \),
    הראשון מקצר את התחתונה ל-\( k + 1 \). בסוף התחתונה היא a1 לבד, העליונה ריקה, ותורו של היריב :

    <!-- gen 5 -->

    <svg class="figure cp-fig" viewBox="0 0 450 104" style="max-width:28.1rem" role="img" aria-label="משחק על 2 על 6. אתם אוכלים את f2, והשורה העליונה קצרה באחת מהתחתונה, 5 מול 6; היריב אוכל את d1 ואת כל מה שמימינה ומעליה, ונשארות 3 בכל שורה; אתם אוכלים את c2, ושוב 2 מול 3"><rect class="cp-poison" x="329" y="43" width="18" height="18" rx="3"/><path class="cp-cross" d="M332.4,46.4 L343.6,57.6 M332.4,57.6 L343.6,46.4"/><rect class="cp-sq" x="329" y="23" width="18" height="18" rx="3"/><rect class="cp-sq" x="349" y="43" width="18" height="18" rx="3"/><rect class="cp-sq" x="349" y="23" width="18" height="18" rx="3"/><rect class="cp-sq" x="369" y="43" width="18" height="18" rx="3"/><rect class="cp-sq" x="369" y="23" width="18" height="18" rx="3"/><rect class="cp-sq" x="389" y="43" width="18" height="18" rx="3"/><rect class="cp-sq" x="389" y="23" width="18" height="18" rx="3"/><rect class="cp-sq" x="409" y="43" width="18" height="18" rx="3"/><rect class="cp-sq" x="409" y="23" width="18" height="18" rx="3"/><rect class="cp-sq" x="429" y="43" width="18" height="18" rx="3"/><rect class="cp-gone" x="430" y="24" width="16" height="16" rx="3"/><rect class="cp-pick" x="429" y="23" width="18" height="18" rx="3"/><text class="cp-lab" x="338" y="75" text-anchor="middle">a</text><text class="cp-lab" x="358" y="75" text-anchor="middle">b</text><text class="cp-lab" x="378" y="75" text-anchor="middle">c</text><text class="cp-lab" x="398" y="75" text-anchor="middle">d</text><text class="cp-lab" x="418" y="75" text-anchor="middle">e</text><text class="cp-lab" x="438" y="75" text-anchor="middle">f</text><text class="cp-lab" x="319" y="56" text-anchor="middle">1</text><text class="cp-lab" x="319" y="36" text-anchor="middle">2</text><text class="cp-cap" x="388" y="94" text-anchor="middle" direction="rtl">אתם : f2</text><rect class="cp-poison" x="173" y="43" width="18" height="18" rx="3"/><path class="cp-cross" d="M176.4,46.4 L187.6,57.6 M176.4,57.6 L187.6,46.4"/><rect class="cp-sq" x="173" y="23" width="18" height="18" rx="3"/><rect class="cp-sq" x="193" y="43" width="18" height="18" rx="3"/><rect class="cp-sq" x="193" y="23" width="18" height="18" rx="3"/><rect class="cp-sq" x="213" y="43" width="18" height="18" rx="3"/><rect class="cp-sq" x="213" y="23" width="18" height="18" rx="3"/><rect class="cp-gone" x="234" y="44" width="16" height="16" rx="3"/><rect class="cp-gone" x="234" y="24" width="16" height="16" rx="3"/><rect class="cp-gone" x="254" y="44" width="16" height="16" rx="3"/><rect class="cp-gone" x="254" y="24" width="16" height="16" rx="3"/><rect class="cp-gone" x="274" y="44" width="16" height="16" rx="3"/><rect class="cp-empty" x="273" y="23" width="18" height="18" rx="3"/><rect class="cp-pick" x="233" y="43" width="18" height="18" rx="3"/><text class="cp-lab" x="182" y="75" text-anchor="middle">a</text><text class="cp-lab" x="202" y="75" text-anchor="middle">b</text><text class="cp-lab" x="222" y="75" text-anchor="middle">c</text><text class="cp-lab" x="242" y="75" text-anchor="middle">d</text><text class="cp-lab" x="262" y="75" text-anchor="middle">e</text><text class="cp-lab" x="282" y="75" text-anchor="middle">f</text><text class="cp-lab" x="163" y="56" text-anchor="middle">1</text><text class="cp-lab" x="163" y="36" text-anchor="middle">2</text><text class="cp-cap" x="232" y="94" text-anchor="middle" direction="rtl">היריב : d1</text><rect class="cp-poison" x="17" y="43" width="18" height="18" rx="3"/><path class="cp-cross" d="M20.4,46.4 L31.6,57.6 M20.4,57.6 L31.6,46.4"/><rect class="cp-sq" x="17" y="23" width="18" height="18" rx="3"/><rect class="cp-sq" x="37" y="43" width="18" height="18" rx="3"/><rect class="cp-sq" x="37" y="23" width="18" height="18" rx="3"/><rect class="cp-sq" x="57" y="43" width="18" height="18" rx="3"/><rect class="cp-gone" x="58" y="24" width="16" height="16" rx="3"/><rect class="cp-empty" x="77" y="43" width="18" height="18" rx="3"/><rect class="cp-empty" x="77" y="23" width="18" height="18" rx="3"/><rect class="cp-empty" x="97" y="43" width="18" height="18" rx="3"/><rect class="cp-empty" x="97" y="23" width="18" height="18" rx="3"/><rect class="cp-empty" x="117" y="43" width="18" height="18" rx="3"/><rect class="cp-empty" x="117" y="23" width="18" height="18" rx="3"/><rect class="cp-pick" x="57" y="23" width="18" height="18" rx="3"/><text class="cp-lab" x="26" y="75" text-anchor="middle">a</text><text class="cp-lab" x="46" y="75" text-anchor="middle">b</text><text class="cp-lab" x="66" y="75" text-anchor="middle">c</text><text class="cp-lab" x="86" y="75" text-anchor="middle">d</text><text class="cp-lab" x="106" y="75" text-anchor="middle">e</text><text class="cp-lab" x="126" y="75" text-anchor="middle">f</text><text class="cp-lab" x="7" y="56" text-anchor="middle">1</text><text class="cp-lab" x="7" y="36" text-anchor="middle">2</text><text class="cp-cap" x="76" y="94" text-anchor="middle" direction="rtl">אתם : c2</text></svg>

    <!-- /gen -->

    <!-- gen 6 -->

    <svg class="figure cp-fig" viewBox="0 0 294 104" style="max-width:18.4rem" role="img" aria-label="המשך המשחק על 2 על 6. היריב אוכל את a2, וכל השורה העליונה נעלמת; אתם אוכלים את b1, ונשארת רק a1 המורעלת, והיריב חייב לאכול אותה"><rect class="cp-poison" x="173" y="43" width="18" height="18" rx="3"/><path class="cp-cross" d="M176.4,46.4 L187.6,57.6 M176.4,57.6 L187.6,46.4"/><rect class="cp-gone" x="174" y="24" width="16" height="16" rx="3"/><rect class="cp-sq" x="193" y="43" width="18" height="18" rx="3"/><rect class="cp-gone" x="194" y="24" width="16" height="16" rx="3"/><rect class="cp-sq" x="213" y="43" width="18" height="18" rx="3"/><rect class="cp-empty" x="213" y="23" width="18" height="18" rx="3"/><rect class="cp-empty" x="233" y="43" width="18" height="18" rx="3"/><rect class="cp-empty" x="233" y="23" width="18" height="18" rx="3"/><rect class="cp-empty" x="253" y="43" width="18" height="18" rx="3"/><rect class="cp-empty" x="253" y="23" width="18" height="18" rx="3"/><rect class="cp-empty" x="273" y="43" width="18" height="18" rx="3"/><rect class="cp-empty" x="273" y="23" width="18" height="18" rx="3"/><rect class="cp-pick" x="173" y="23" width="18" height="18" rx="3"/><text class="cp-lab" x="182" y="75" text-anchor="middle">a</text><text class="cp-lab" x="202" y="75" text-anchor="middle">b</text><text class="cp-lab" x="222" y="75" text-anchor="middle">c</text><text class="cp-lab" x="242" y="75" text-anchor="middle">d</text><text class="cp-lab" x="262" y="75" text-anchor="middle">e</text><text class="cp-lab" x="282" y="75" text-anchor="middle">f</text><text class="cp-lab" x="163" y="56" text-anchor="middle">1</text><text class="cp-lab" x="163" y="36" text-anchor="middle">2</text><text class="cp-cap" x="232" y="94" text-anchor="middle" direction="rtl">היריב : a2</text><rect class="cp-poison" x="17" y="43" width="18" height="18" rx="3"/><path class="cp-cross" d="M20.4,46.4 L31.6,57.6 M20.4,57.6 L31.6,46.4"/><rect class="cp-empty" x="17" y="23" width="18" height="18" rx="3"/><rect class="cp-gone" x="38" y="44" width="16" height="16" rx="3"/><rect class="cp-empty" x="37" y="23" width="18" height="18" rx="3"/><rect class="cp-gone" x="58" y="44" width="16" height="16" rx="3"/><rect class="cp-empty" x="57" y="23" width="18" height="18" rx="3"/><rect class="cp-empty" x="77" y="43" width="18" height="18" rx="3"/><rect class="cp-empty" x="77" y="23" width="18" height="18" rx="3"/><rect class="cp-empty" x="97" y="43" width="18" height="18" rx="3"/><rect class="cp-empty" x="97" y="23" width="18" height="18" rx="3"/><rect class="cp-empty" x="117" y="43" width="18" height="18" rx="3"/><rect class="cp-empty" x="117" y="23" width="18" height="18" rx="3"/><rect class="cp-pick" x="37" y="43" width="18" height="18" rx="3"/><text class="cp-lab" x="26" y="75" text-anchor="middle">a</text><text class="cp-lab" x="46" y="75" text-anchor="middle">b</text><text class="cp-lab" x="66" y="75" text-anchor="middle">c</text><text class="cp-lab" x="86" y="75" text-anchor="middle">d</text><text class="cp-lab" x="106" y="75" text-anchor="middle">e</text><text class="cp-lab" x="126" y="75" text-anchor="middle">f</text><text class="cp-lab" x="7" y="56" text-anchor="middle">1</text><text class="cp-lab" x="7" y="36" text-anchor="middle">2</text><text class="cp-cap" x="76" y="94" text-anchor="middle" direction="rtl">אתם : b1</text></svg>

    <!-- /gen -->

    **מה עוד ידוע.** בלוח של שורה אחת אוכלים את b1, ובעמודה אחת את a2, ונשארת a1 לבד. בכל לוח
    אחר החיפוש מוצא את המהלכים המנצחים. בכל הלוחות עד 7 שורות ו-8 עמודות יש מהלך ראשון מנצח
    אחד בדיוק, ואין בהם דפוס פשוט מעבר לשורות 1 ו-2, לעמודות 1 ו-2 ולאלכסון של הלוחות הריבועיים.
    הטבלה סימטרית : החלפה של השורות בעמודות מחליפה גם את האות במספר (ב-3 על 4 המהלך הוא c2, וב-4
    על 3 הוא b3), ולכן מספיק לקרוא חצי ממנה :

    <!-- gen 7 -->

    | שורות \ עמודות | ‏1 | ‏2 | ‏3 | ‏4 | ‏5 | ‏6 | ‏7 | ‏8 |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏1 | אין | ‏b1 | ‏b1 | ‏b1 | ‏b1 | ‏b1 | ‏b1 | ‏b1 |
    | ‏2 | ‏a2 | ‏b2 | ‏c2 | ‏d2 | ‏e2 | ‏f2 | ‏g2 | ‏h2 |
    | ‏3 | ‏a2 | ‏b3 | ‏b2 | ‏c2 | ‏d3 | ‏d2 | ‏e3 | ‏e2 |
    | ‏4 | ‏a2 | ‏b4 | ‏b3 | ‏b2 | ‏c3 | ‏c2 | ‏d3 | ‏d2 |
    | ‏5 | ‏a2 | ‏b5 | ‏c4 | ‏c3 | ‏b2 | ‏d3 | ‏c2 | ‏g5 |
    | ‏6 | ‏a2 | ‏b6 | ‏b4 | ‏b3 | ‏c4 | ‏b2 | ‏e5 | ‏d3 |
    | ‏7 | ‏a2 | ‏b7 | ‏c5 | ‏c4 | ‏b3 | ‏e5 | ‏b2 | ‏c3 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מי מנצח :** בלוח של 1 על 1 השני, ובכל לוח אחר הראשון, לפי גניבת האסטרטגיה.
    2. **2 שורות :** אם השורה התחתונה ארוכה באחת מהעליונה, אין מהלך מנצח. אם העליונה שווה
       לתחתונה, מקצרים אותה באחת. אחרת מקצרים את התחתונה לאורך העליונה ועוד 1.
    3. **כל לוח אחר :** חיפוש עם זיכרון על המדרגות, כמו בסעיף ב, ומהלך שמוביל למצב מפסיד.
    4. **ריבוע :** b2 והמראה, בלי חיפוש.

    </div>

    #### הקוד { .sol-code }

    האסטרטגיה של 2 שורות, לפי האורכים של השורות. ללוח כללי, `winning_moves` של סעיף ב.

    === "Python"
        ```python title="two_rows_move" linenums="1" hl_lines="5 6 7 8 9"
        def two_rows_move(bottom: int, top: int):
            """2 x n: the lengths of the two rows (top <= bottom). A move as (column, row),
            0-based, that leaves the bottom row exactly one longer than the top, or None when
            it already is (the player to move loses)."""
            if top == bottom - 1:
                return None                   # (1)!
            if top == bottom:
                return bottom - 1, 1          # (2)!
            return top + 1, 0                 # (3)!
        ```

        1. התחתונה ארוכה באחת : כל מהלך הורס את זה, והיריב מתקן. כולל 1 ו-0, a1 לבד.
        2. השורות שוות, כמו בהתחלה : אוכלים את המשבצת האחרונה בשורה העליונה.
        3. העליונה קצרה ביותר מאחת : אוכלים בשורה התחתונה את המשבצת שמימין לאורך העליונה ועוד 1.

    === "SystemVerilog"
        ```systemverilog title="two_rows_move" linenums="1" hl_lines="5 6 7"
        // 2 x n: the lengths of the two rows (top <= bottom). The move that leaves the bottom
        // row exactly one longer than the top comes out in col and row (0-based); returns 0
        // when it already is (the player to move loses)
        function automatic bit two_rows_move(int bottom, int top, output int col, output int row);
          if (top == bottom - 1) return 0;                          // (1)!
          if (top == bottom) begin col = bottom - 1; row = 1; end   // (2)!
          else begin col = top + 1; row = 0; end                    // (3)!
          return 1;
        endfunction
        ```

        1. התחתונה ארוכה באחת : מי שתורו מפסיד.
        2. השורות שוות : המשבצת האחרונה בשורה העליונה.
        3. העליונה קצרה מדי : מקצרים את התחתונה לאורך העליונה ועוד 1.

    #### למה זה נכון { .sol-proof }

    **גניבת האסטרטגיה, בפירוט.** המשחק סופי ואין בו תיקו, ולכן לאחד משני השחקנים יש אסטרטגיה
    מנצחת, באינדוקציה של סעיף ב. נסמן ב-\( T \) את המשבצת הימנית העליונה. אם אחרי \( T \) נשארה רק
    a1, כמו ב-1 על 2, \( T \) עצמו מנצח. אחרת, אם התשובה הטובה של
    השני ל-\( T \) היא \( X \), אז \( X \ne T \), ו-\( X \) מעל a1 או מימינה, ולכן \( T \) מעל
    \( X \) ומימינו, ו-\( X \) אוכל אותה. המצב "\( T \) ואז \( X \)" שווה למצב "\( X \) לבד", מפסיד
    למי שתורו. לכן \( X \) הוא מהלך ראשון מנצח, ואין לשני אסטרטגיה מנצחת. היוצא מן הכלל הוא
    1 על 1 : שם \( T \) היא a1 עצמה, ואין מהלך.

    **שתי שורות.** נסמן את האורכים \( b \) לתחתונה ו-\( t \le b \) לעליונה. הטענה : מי שתורו
    מפסיד בדיוק כש-\( t = b - 1 \).

    1. **הסוף :** \( b = 1, t = 0 \) הוא a1 לבד, מפסיד.
    2. **מ-t = b − 1 יוצאים :** מהלך בעליונה מקטין רק את \( t \), ומהלך בתחתונה בעמודה \( c \ge 1 \)
       הופך את \( b \) ל-\( c \) ואת \( t \) ל-\( \min(t, c) = c \), כי \( c \le b - 1 = t \). בשני
       המקרים ההפרש כבר לא 1.
    3. **ל-t = b − 1 חוזרים :** אם \( t = b \), מורידים את העליונה ל-\( b - 1 \). אם \( t < b - 1 \),
       מורידים את התחתונה ל-\( t + 1 \), והעליונה לא משתנה כי \( t \le t + 1 \). זה בדיוק
       `two_rows_move`.

    **נסו בעצמכם.** לוח של 3 על 5, נגד המחשב. כאן אין מראה ואין נוסחה, והתיבה מראה את מה שהחיפוש
    מוצא בכל מצב.

    - הדליקו את "סימון המהלכים" : בלוח הזה המהלך המנצח היחיד הוא d3.
    - אכלו במקומו את e3, הפינה : המחשב עונה ב-d3. זו גניבת האסטרטגיה, במשחק אמיתי.
    - לחצו על "לוח של 2 על 6" ואכלו את f2 : המחשב עונה ב-f1, ועכשיו רק e2 ירוקה. בכל תור, המהלך
      המנצח משאיר את השורה התחתונה ארוכה באחת מהעליונה.
    - בחרו 3 שורות ו-4 עמודות, משחק המחלקים של 72 משאלות ההמשך : רק c2, המחלק 12, ירוקה.

    <div class="explorer" data-kind="chomp" data-mode="play" data-m="3" data-n="5"></div>

    #### סיבוכיות { .sol-cost }

    בלוח כללי : \( \binom{m+n}{n} \) מצבים, עד \( mn \) מהלכים מכל אחד, ו-\( O(n) \) לבנות כל
    מצב. ב-3 שורות זה \( O(n^3) \) מצבים, פולינומי, ובכל זאת לא ידועה נוסחה למהלך המנצח. ב-2
    שורות : \( O(1) \) למהלך. ב-10 על 10 כבר 184,756 מצבים, וב-20 על 20 יותר מ-\( 10^{11} \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : מראה בלוח מלבני"
    ב-3 על 5, אחרי b2, הזרוע העליונה באורך 2 והימנית באורך 4, והמראה לא מתחילה. במלבן אין
    מהלך ראשון שמשאיר שתי זרועות שוות ושום דבר אחר, וגניבת האסטרטגיה רק אומרת שיש מהלך מנצח.

??? trap "מלכודת : המשבצת הימנית העליונה היא המהלך המנצח"
    ההוכחה משתמשת ב-\( T \) רק כדי לגנוב, ולא טוענת שהיא טובה. ב-3 על 3 אחרי c3 נשאר מצב שמנצח
    למי שתורו : הוא אוכל את b2 ומשאיר זרועות שוות. בטבלה של סעיף ג היא המהלך המנצח רק בלוחות של 2
    שורות או 2 עמודות, ובלוחות 1 על 2 ו-2 על 1.

??? trap "מלכודת : סוף המשחק הפוך"
    אם מגדירים "הלוח ריק : מי שתורו מפסיד" ומרשים לאכול את a1 כמו כל משבצת, כל התוצאות
    מתהפכות : מי שאוכל את a1 משאיר לוח ריק, ולכן "מנצח". הסוף הנכון הוא a1 לבד : מי שתורו מפסיד, ואכילת
    a1 לא נחשבת מהלך בחיפוש.

??? trap "מלכודת : מצב הוא קבוצה של משבצות"
    שמירה של כל קבוצה אפשרית של משבצות עולה \( 2^{mn} \), ‏\( 2^{64} \) ב-8 על 8. רק מדרגות יכולות
    להופיע, ויש פחות מ-13,000 כאלה (סעיף ב). מפתח הזיכרון הוא רשימת הגבהים.

??? followup "שאלות המשך"
    - **שורה אחת או עמודה אחת :** מי מנצח ב-1 על \( n \)?

        ??? fu-answer "תשובה"
            הראשון, כש-\( n \ge 2 \) : הוא אוכל את b1, ונשארת a1 לבד. ב-1 על 1 הוא חייב לאכול את
            a1 ומפסיד.

    - **מהלך מנצח יחיד :** האם בכל לוח יש מהלך ראשון מנצח אחד בלבד?

        ??? fu-answer "תשובה"
            לא. בכל הלוחות עד 7 שורות ו-8 עמודות יש אחד בדיוק, אבל בלוח של 8 שורות ו-10 עמודות יש
            שניים : f5 ו-i4, לפי `winning_moves(8, 10)`. בלוחות ריבועיים ובשתי שורות היחידות מוכחת.

    - **משחק המחלקים :** שחקנים אומרים בתורות מחלק של 72 שאינו כפולה של מחלק שכבר נאמר. מי
      שאומר 1 מפסיד. מי מנצח?

        ??? fu-answer "תשובה"
            ‏\( 72 = 2^3 \cdot 3^2 \), והמחלקים הם \( 2^a 3^b \) עם \( 0 \le a \le 3 \) ו-\( 0 \le b \le 2 \) :
            לוח של 3 שורות ו-4 עמודות. מחלק פוסל את כל הכפולות שלו, כלומר כל מה שמעליו ומימינו, ו-1
            הוא a1. זה Chomp, והראשון מנצח. לפי הטבלה, המהלך המנצח הוא c2, המחלק \( 2^2 \cdot 3 = 12 \).

    - **כמה מצבים ב-10 על 10?**

        ??? fu-answer "תשובה"
            ‏\( \binom{20}{10} = 184{,}756 \), כולל המצב הריק. חיפוש עם זיכרון עוד עובד בשניות.
