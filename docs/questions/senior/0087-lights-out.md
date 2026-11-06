---
id: 87
title: כיבוי הנורות – Lights Out, XOR ואלגברה לינארית מעל GF(2)
level: senior
difficulty: hard
kind: math
tags: [logic-puzzles, matrices, bitwise, proof, algorithms, python, systemverilog]
source: "המשחק של Tiger Electronics מ-1995; הניתוח האלגברי לפי Anderson ו-Feil ולפי Sutner"
added: 2026-11-06
---

## השאלה

לפניכם לוח של \( n \times n \) נורות, וכל נורה דולקת או כבויה. לחיצה על נורה הופכת אותה ואת
השכנות שלה **למעלה, למטה, ימינה ושמאלה** : דולקת נכבית, וכבויה נדלקת. לנורה פנימית יש ארבע
שכנות, ולכן לחיצה עליה הופכת 5 נורות. לנורה בשפה יש שלוש שכנות, ולנורה בפינה שתיים, ולכן לחיצה
עליהן הופכת 4 ו-3 נורות. שכנות באלכסון לא נחשבות, עד סעיף ג.

<!-- gen 0 -->

<svg class="figure lo-fig" viewBox="0 0 432 152" style="max-width:27.0rem" role="img" aria-label="שלושה לוחות של 3 על 3, על כל אחד לחיצה אחת על לוח כבוי. לחיצה על הנורה האמצעית מדליקה 5 נורות : אותה ואת 4 השכנות שלה. לחיצה על נורה בשפה מדליקה 4, ולחיצה על פינה 3"><rect class="lo-cell" x="310" y="2" width="40" height="40"/><circle class="lo-off" cx="330" cy="22" r="10.8"/><rect class="lo-cell" x="350" y="2" width="40" height="40"/><circle class="lo-on" cx="370" cy="22" r="10.8"/><rect class="lo-cell" x="390" y="2" width="40" height="40"/><circle class="lo-off" cx="410" cy="22" r="10.8"/><rect class="lo-cell" x="310" y="42" width="40" height="40"/><circle class="lo-on" cx="330" cy="62" r="10.8"/><rect class="lo-cell" x="350" y="42" width="40" height="40"/><rect class="lo-press" x="353" y="45" width="34" height="34" rx="4"/><circle class="lo-on" cx="370" cy="62" r="10.8"/><rect class="lo-cell" x="390" y="42" width="40" height="40"/><circle class="lo-on" cx="410" cy="62" r="10.8"/><rect class="lo-cell" x="310" y="82" width="40" height="40"/><circle class="lo-off" cx="330" cy="102" r="10.8"/><rect class="lo-cell" x="350" y="82" width="40" height="40"/><circle class="lo-on" cx="370" cy="102" r="10.8"/><rect class="lo-cell" x="390" y="82" width="40" height="40"/><circle class="lo-off" cx="410" cy="102" r="10.8"/><rect class="lo-frame" x="310" y="2" width="120" height="120"/><text class="lo-cap" x="370" y="142" text-anchor="middle" direction="rtl">פנימית : 5 נורות</text><rect class="lo-cell" x="156" y="2" width="40" height="40"/><circle class="lo-on" cx="176" cy="22" r="10.8"/><rect class="lo-cell" x="196" y="2" width="40" height="40"/><rect class="lo-press" x="199" y="5" width="34" height="34" rx="4"/><circle class="lo-on" cx="216" cy="22" r="10.8"/><rect class="lo-cell" x="236" y="2" width="40" height="40"/><circle class="lo-on" cx="256" cy="22" r="10.8"/><rect class="lo-cell" x="156" y="42" width="40" height="40"/><circle class="lo-off" cx="176" cy="62" r="10.8"/><rect class="lo-cell" x="196" y="42" width="40" height="40"/><circle class="lo-on" cx="216" cy="62" r="10.8"/><rect class="lo-cell" x="236" y="42" width="40" height="40"/><circle class="lo-off" cx="256" cy="62" r="10.8"/><rect class="lo-cell" x="156" y="82" width="40" height="40"/><circle class="lo-off" cx="176" cy="102" r="10.8"/><rect class="lo-cell" x="196" y="82" width="40" height="40"/><circle class="lo-off" cx="216" cy="102" r="10.8"/><rect class="lo-cell" x="236" y="82" width="40" height="40"/><circle class="lo-off" cx="256" cy="102" r="10.8"/><rect class="lo-frame" x="156" y="2" width="120" height="120"/><text class="lo-cap" x="216" y="142" text-anchor="middle" direction="rtl">בשפה : 4 נורות</text><rect class="lo-cell" x="2" y="2" width="40" height="40"/><rect class="lo-press" x="5" y="5" width="34" height="34" rx="4"/><circle class="lo-on" cx="22" cy="22" r="10.8"/><rect class="lo-cell" x="42" y="2" width="40" height="40"/><circle class="lo-on" cx="62" cy="22" r="10.8"/><rect class="lo-cell" x="82" y="2" width="40" height="40"/><circle class="lo-off" cx="102" cy="22" r="10.8"/><rect class="lo-cell" x="2" y="42" width="40" height="40"/><circle class="lo-on" cx="22" cy="62" r="10.8"/><rect class="lo-cell" x="42" y="42" width="40" height="40"/><circle class="lo-off" cx="62" cy="62" r="10.8"/><rect class="lo-cell" x="82" y="42" width="40" height="40"/><circle class="lo-off" cx="102" cy="62" r="10.8"/><rect class="lo-cell" x="2" y="82" width="40" height="40"/><circle class="lo-off" cx="22" cy="102" r="10.8"/><rect class="lo-cell" x="42" y="82" width="40" height="40"/><circle class="lo-off" cx="62" cy="102" r="10.8"/><rect class="lo-cell" x="82" y="82" width="40" height="40"/><circle class="lo-off" cx="102" cy="102" r="10.8"/><rect class="lo-frame" x="2" y="2" width="120" height="120"/><text class="lo-cap" x="62" y="142" text-anchor="middle" direction="rtl">בפינה : 3 נורות</text></svg>

<span class="viz-legend"><span><i class="lo-key-press"></i>לחיצה</span><span><i class="lo-key-on"></i>נורה דולקת</span><span><i class="lo-key-off"></i>נורה כבויה</span></span>

<!-- /gen -->

המטרה היא לכבות את כל הנורות. בכל סעיף שואלים אם אפשר, באילו לחיצות, ובכמה דרכים.

??? interviewer "מה המראיין בודק"
    - **מידול :** לראות שהסדר של הלחיצות לא משנה ושלחיצה כפולה מבטלת את עצמה. לכן פתרון הוא
      קבוצה של משבצות, כלומר וקטור של ביטים.
    - **‏XOR כחיבור :** הפיכה היא חיבור מודולו 2, והחידה היא מערכת משוואות לינאריות מעל GF(2)
      שנפתרת בדירוג גאוס עם XOR, בלי חילוק ובלי שברים.
    - **מתי אין פתרון :** דרגה, משתנים חופשיים ולחיצות "שקטות", ולמה מטריצה סימטרית נותנת מבחן
      פשוט לכל מצב.
    - **קיצור דרך :** רדיפת אורות, שמקטינה \( n^2 \) נעלמים ל-\( n \).
    - **הכללה עם הוכחה :** לא רק טבלה של גדלים, אלא הסבר למה גודל מסוים פתיר תמיד ואחר לא.

---

### סעיף א – לוח של 3 על 3 { #three }

בלוח של 3 על 3 דולקת רק השורה העליונה. על אילו נורות צריך ללחוץ? כתבו פונקציה שמוצאת את
הלחיצות לכל מצב ולכל \( n \), והראו שבלוח של 3 על 3 לכל מצב יש פתרון אחד בדיוק.

??? tip "רמז 1"
    האם הסדר של הלחיצות משנה? ומה עושות שתי לחיצות על אותה נורה?

??? tip "רמז 2"
    לכל משבצת \( i \) משתנה \( x_i \) שהוא 0 או 1 : לוחצים עליה או לא. נורה \( j \) נכבית כשמספר
    הלחיצות שהופכות אותה זוגי אם היא כבויה, ואי-זוגי אם היא דולקת.

??? tip "רמז 3"
    זו משוואה לינארית מודולו 2 לכל נורה : 9 משוואות ב-9 נעלמים. חיבור מודולו 2 הוא XOR, ודירוג
    גאוס עובד עליהן בדיוק כמו על מספרים ממשיים.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        לוחצים על כל השורה האמצעית ועל הנורה האמצעית שבשורה התחתונה, ארבע לחיצות. בכל לוח לחיצה
        היא XOR של המסכה שלה, ולכן הסדר לא משנה ושתי לחיצות על אותה נורה מבטלות זו את זו. פתרון
        הוא וקטור \( x \) של \( n^2 \) ביטים עם \( A x = b \) מעל GF(2), כש-\( A \) היא מטריצת
        הלחיצות ו-\( b \) הנורות הדולקות. ב-3 על 3 הדרגה של \( A \) היא 9, ולכן לכל מצב יש פתרון
        יחיד.

    <!-- cost: זמן \( O(n^6) \) לדירוג | זיכרון \( O(n^4) \) ביטים -->

    #### הרעיון { .sol-idea }

    שתי הבחנות הופכות את החידה לאלגברה. הראשונה : לחיצה עושה XOR של המסכה שלה עם הלוח, ו-XOR
    הוא חילופי וקיבוצי, ולכן הסדר לא משנה. השנייה : XOR של מסכה עם עצמה הוא 0, ולכן מספיק לדעת
    על כל משבצת אם לוחצים עליה מספר זוגי או אי-זוגי של פעמים. פתרון הוא אפוא קבוצה של משבצות.
    בדוגמה, לחיצה על הנורות הדולקות עצמן לא עוזרת, ודווקא הלחיצות בשורה שמתחתן מכבות אותן :

    <!-- gen 1 -->

    <svg class="figure lo-fig" viewBox="0 0 432 152" style="max-width:27.0rem" role="img" aria-label="סעיף א : לוח של 3 על 3 שבו דולקת רק השורה העליונה, הנורות 0, 1 ו-2. הפתרון הוא ארבע לחיצות, על הנורות 3, 4, 5, 7 : כל השורה האמצעית והאמצעית שבשורה התחתונה. אחריהן כל הנורות כבויות"><rect class="lo-cell" x="310" y="2" width="40" height="40"/><circle class="lo-on" cx="330" cy="25" r="8.8"/><text class="lo-ix" x="314" y="15">0</text><rect class="lo-cell" x="350" y="2" width="40" height="40"/><circle class="lo-on" cx="370" cy="25" r="8.8"/><text class="lo-ix" x="354" y="15">1</text><rect class="lo-cell" x="390" y="2" width="40" height="40"/><circle class="lo-on" cx="410" cy="25" r="8.8"/><text class="lo-ix" x="394" y="15">2</text><rect class="lo-cell" x="310" y="42" width="40" height="40"/><circle class="lo-off" cx="330" cy="65" r="8.8"/><text class="lo-ix" x="314" y="55">3</text><rect class="lo-cell" x="350" y="42" width="40" height="40"/><circle class="lo-off" cx="370" cy="65" r="8.8"/><text class="lo-ix" x="354" y="55">4</text><rect class="lo-cell" x="390" y="42" width="40" height="40"/><circle class="lo-off" cx="410" cy="65" r="8.8"/><text class="lo-ix" x="394" y="55">5</text><rect class="lo-cell" x="310" y="82" width="40" height="40"/><circle class="lo-off" cx="330" cy="105" r="8.8"/><text class="lo-ix" x="314" y="95">6</text><rect class="lo-cell" x="350" y="82" width="40" height="40"/><circle class="lo-off" cx="370" cy="105" r="8.8"/><text class="lo-ix" x="354" y="95">7</text><rect class="lo-cell" x="390" y="82" width="40" height="40"/><circle class="lo-off" cx="410" cy="105" r="8.8"/><text class="lo-ix" x="394" y="95">8</text><rect class="lo-frame" x="310" y="2" width="120" height="120"/><text class="lo-cap" x="370" y="142" text-anchor="middle" direction="rtl">ההתחלה</text><rect class="lo-cell" x="156" y="2" width="40" height="40"/><circle class="lo-on" cx="176" cy="25" r="8.8"/><text class="lo-ix" x="160" y="15">0</text><rect class="lo-cell" x="196" y="2" width="40" height="40"/><circle class="lo-on" cx="216" cy="25" r="8.8"/><text class="lo-ix" x="200" y="15">1</text><rect class="lo-cell" x="236" y="2" width="40" height="40"/><circle class="lo-on" cx="256" cy="25" r="8.8"/><text class="lo-ix" x="240" y="15">2</text><rect class="lo-cell" x="156" y="42" width="40" height="40"/><rect class="lo-press" x="159" y="45" width="34" height="34" rx="4"/><circle class="lo-off" cx="176" cy="65" r="8.8"/><text class="lo-ix" x="160" y="55">3</text><rect class="lo-cell" x="196" y="42" width="40" height="40"/><rect class="lo-press" x="199" y="45" width="34" height="34" rx="4"/><circle class="lo-off" cx="216" cy="65" r="8.8"/><text class="lo-ix" x="200" y="55">4</text><rect class="lo-cell" x="236" y="42" width="40" height="40"/><rect class="lo-press" x="239" y="45" width="34" height="34" rx="4"/><circle class="lo-off" cx="256" cy="65" r="8.8"/><text class="lo-ix" x="240" y="55">5</text><rect class="lo-cell" x="156" y="82" width="40" height="40"/><circle class="lo-off" cx="176" cy="105" r="8.8"/><text class="lo-ix" x="160" y="95">6</text><rect class="lo-cell" x="196" y="82" width="40" height="40"/><rect class="lo-press" x="199" y="85" width="34" height="34" rx="4"/><circle class="lo-off" cx="216" cy="105" r="8.8"/><text class="lo-ix" x="200" y="95">7</text><rect class="lo-cell" x="236" y="82" width="40" height="40"/><circle class="lo-off" cx="256" cy="105" r="8.8"/><text class="lo-ix" x="240" y="95">8</text><rect class="lo-frame" x="156" y="2" width="120" height="120"/><text class="lo-cap" x="216" y="142" text-anchor="middle" direction="rtl">הלחיצות</text><rect class="lo-cell" x="2" y="2" width="40" height="40"/><circle class="lo-off" cx="22" cy="25" r="8.8"/><text class="lo-ix" x="6" y="15">0</text><rect class="lo-cell" x="42" y="2" width="40" height="40"/><circle class="lo-off" cx="62" cy="25" r="8.8"/><text class="lo-ix" x="46" y="15">1</text><rect class="lo-cell" x="82" y="2" width="40" height="40"/><circle class="lo-off" cx="102" cy="25" r="8.8"/><text class="lo-ix" x="86" y="15">2</text><rect class="lo-cell" x="2" y="42" width="40" height="40"/><circle class="lo-off" cx="22" cy="65" r="8.8"/><text class="lo-ix" x="6" y="55">3</text><rect class="lo-cell" x="42" y="42" width="40" height="40"/><circle class="lo-off" cx="62" cy="65" r="8.8"/><text class="lo-ix" x="46" y="55">4</text><rect class="lo-cell" x="82" y="42" width="40" height="40"/><circle class="lo-off" cx="102" cy="65" r="8.8"/><text class="lo-ix" x="86" y="55">5</text><rect class="lo-cell" x="2" y="82" width="40" height="40"/><circle class="lo-off" cx="22" cy="105" r="8.8"/><text class="lo-ix" x="6" y="95">6</text><rect class="lo-cell" x="42" y="82" width="40" height="40"/><circle class="lo-off" cx="62" cy="105" r="8.8"/><text class="lo-ix" x="46" y="95">7</text><rect class="lo-cell" x="82" y="82" width="40" height="40"/><circle class="lo-off" cx="102" cy="105" r="8.8"/><text class="lo-ix" x="86" y="95">8</text><rect class="lo-frame" x="2" y="2" width="120" height="120"/><text class="lo-cap" x="62" y="142" text-anchor="middle" direction="rtl">אחרי הלחיצות</text></svg>

    <span class="viz-legend"><span><i class="lo-key-press"></i>לחיצה</span><span><i class="lo-key-on"></i>נורה דולקת</span><span><i class="lo-key-ix"></i>המספר של הנורה, ‏r·3 + c</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המודל :** המשבצת בשורה \( r \) ובעמודה \( c \) היא הביט \( k = r n + c \). המסכה של
       לחיצה על \( k \) היא הביטים של הנורה ושל השכנות שלה.

    2. **המשוואות :** הנורה \( j \) נכבית כש-\( \bigoplus_i A_{ji} x_i = b_j \), כש-\( A_{ji} = 1 \)
       אם לחיצה על \( i \) הופכת את \( j \). המטריצה סימטרית, כי \( i \) הופכת את \( j \) בדיוק
       כש-\( j \) הופכת את \( i \). לכן השורה של הנורה \( j \) היא המסכה של \( j \).

    3. **הדירוג :** כל משוואה היא מספר שלם אחד : בביטים 0 עד \( N - 1 \) המקדמים, ובביט \( N \)
       הצד הימני. לכל עמודה מחפשים משוואה עם 1 בעמודה, מעבירים אותה למקום, ומאפסים את העמודה
       בכל שאר המשוואות ב-XOR איתה.

    4. **התשובה :** משוואה שנשארה בצורה \( 0 = 1 \) אומרת שאין פתרון. אחרת, המשתנה של כל עמודה
       עם ציר שווה לצד הימני של השורה שלו, ומשתנה חופשי מקבל 0.

    </div>

    זו המערכת של הדוגמה, לפני הדירוג. שורה היא נורה, עמודה היא לחיצה, ובשורה התחתונה הפתרון :

    <!-- gen 2 -->

    <div class="gs-scroll" tabindex="0" role="region" aria-label="סעיף א : מערכת המשוואות של הלוח 3 על 3"><table class="gs-bits lo-sys" dir="ltr" aria-label="סעיף א : מערכת 9 על 9 מעל GF(2). שורה j היא הנורה j, עמודה i היא הלחיצה x_i, ו-1 אומר שהלחיצה הופכת את הנורה. בעמודה האחרונה הנורות שדולקות בהתחלה. בשורה התחתונה הפתרון"><tbody><tr class="lo-head"><th>light</th><th>x0</th><th>x1</th><th>x2</th><th>x3</th><th>x4</th><th>x5</th><th>x6</th><th>x7</th><th>x8</th><th></th><th>lit</th></tr><tr><th>0</th><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="lo-eq">=</td><td class="gs-b is-one">1</td></tr><tr><th>1</th><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="lo-eq">=</td><td class="gs-b is-one">1</td></tr><tr><th>2</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="lo-eq">=</td><td class="gs-b is-one">1</td></tr><tr><th>3</th><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="lo-eq">=</td><td class="gs-b">0</td></tr><tr><th>4</th><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="lo-eq">=</td><td class="gs-b">0</td></tr><tr><th>5</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="lo-eq">=</td><td class="gs-b">0</td></tr><tr><th>6</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="lo-eq">=</td><td class="gs-b">0</td></tr><tr><th>7</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="lo-eq">=</td><td class="gs-b">0</td></tr><tr><th>8</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b">0</td><td class="gs-b is-one">1</td><td class="gs-b is-one">1</td><td class="lo-eq">=</td><td class="gs-b">0</td></tr><tr class="lo-sol"><th>x</th><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b">0</td><td class="gs-b lo-x">1</td><td class="gs-b lo-x">1</td><td class="gs-b lo-x">1</td><td class="gs-b">0</td><td class="gs-b lo-x">1</td><td class="gs-b">0</td><td></td><td></td></tr></tbody></table></div>

    <span class="viz-legend"><span><i class="gs-key-one"></i>1 : הלחיצה הופכת את הנורה</span><span><i class="lo-key-x"></i>1 בפתרון : לוחצים</span></span>

    <!-- /gen -->

    בתיבה לוחצים על נורות. "הצגת פתרון" מסמנת את הלחיצות המעטות ביותר מהמצב הנוכחי :

    <div class="explorer" data-kind="lightsout" data-mode="play" data-n="3" data-diag="0" data-lit="7"></div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="press_masks, gauss, solve_lights" linenums="1" hl_lines="12 31 34 43"
        def press_masks(n: int, diag: bool = False) -> list[int]:
            """Cell (r, c) is bit r*n + c. masks[k]: the lights a press on cell k flips, the cell
            and its neighbours up, down, left and right (with diag, also the four diagonal ones)."""
            masks = []
            for r in range(n):
                for c in range(n):
                    m = 0
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr and dc and not diag:
                                continue
                            if 0 <= r + dr < n and 0 <= c + dc < n:   # (1)!
                                m |= 1 << ((r + dr) * n + c + dc)
                    masks.append(m)
            return masks


        def gauss(eqs: list[int], nvars: int) -> tuple[int | None, int]:
            """A linear system over GF(2): equation k is eqs[k], the variables in bits 0..nvars-1
            and the right side in bit nvars. Returns (a solution, with the free variables 0, or
            None when there is none; the number of free variables)."""
            eqs, pivots = list(eqs), []
            for col in range(nvars):
                r = len(pivots)
                p = next((i for i in range(r, len(eqs)) if eqs[i] >> col & 1), None)
                if p is None:
                    continue                                 # (2)!
                eqs[r], eqs[p] = eqs[p], eqs[r]
                for i in range(len(eqs)):
                    if i != r and eqs[i] >> col & 1:
                        eqs[i] ^= eqs[r]                     # (3)!
                pivots.append(col)
            if any(e == 1 << nvars for e in eqs[len(pivots):]):
                return None, nvars - len(pivots)             # (4)!
            x = sum(1 << col for r, col in enumerate(pivots) if eqs[r] >> nvars & 1)
            return x, nvars - len(pivots)


        def solve_lights(n: int, lit: int, diag: bool = False) -> tuple[int | None, int]:
            """The presses that turn every light of lit (bit r*n + c) off, or None, and the number
            of free variables. Light j goes off when the presses that flip it are odd in number."""
            masks = press_masks(n, diag)
            eqs = [masks[j] | (lit >> j & 1) << n * n for j in range(n * n)]   # (5)!
            return gauss(eqs, n * n)
        ```

        1. נורה בשפה או בפינה : שכנה שמחוץ ללוח פשוט לא נכנסת למסכה.
        2. אין משוואה עם 1 בעמודה הזו : המשתנה שלה חופשי.
        3. ‏XOR של שתי משוואות הוא החיבור והחיסור מעל GF(2). אין חילוק, כי המקדם של הציר הוא תמיד 1.
        4. משוואה שכל המקדמים שלה התאפסו אבל הצד הימני 1 : ‏\( 0 = 1 \).
        5. השורה של הנורה \( j \) היא המסכה של \( j \), כי המטריצה סימטרית. הצד הימני בביט \( n^2 \).

    === "SystemVerilog"
        ```systemverilog title="press_masks, gauss, solve_lights" linenums="1" hl_lines="13 33 37 48"
        // Part a: boards up to 11 x 11. A vector holds one bit per cell (bit r*n + c), and an
        // equation also its right side in the bit after the variables.
        typedef bit [127:0] vec_t;

        // masks[k]: the lights a press on cell k flips (with diag, also the diagonal neighbours).
        function automatic void press_masks(int n, bit diag, ref vec_t masks[$]);
          masks.delete();
          for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) begin
              vec_t m = '0;
              for (int dr = -1; dr <= 1; dr++)
                for (int dc = -1; dc <= 1; dc++)
                  if ((dr == 0 || dc == 0 || diag) &&                       // (1)!
                      r + dr >= 0 && r + dr < n && c + dc >= 0 && c + dc < n)
                    m[(r + dr) * n + c + dc] = 1;
              masks.push_back(m);
            end
        endfunction

        // A system over GF(2): the variables in bits 0..nvars-1, the right side in bit nvars.
        // Returns the number of free variables; ok = 0 when there is no solution.
        function automatic int gauss(vec_t eqs[$], int nvars, output vec_t x, output bit ok);
          int pivots[$];
          for (int col = 0; col < nvars; col++) begin
            int r = pivots.size(), p = -1;
            for (int i = r; i < eqs.size() && p < 0; i++) if (eqs[i][col]) p = i;
            if (p < 0) continue;                                          // (2)!
            begin
              vec_t t = eqs[r];
              eqs[r] = eqs[p];
              eqs[p] = t;
            end
            foreach (eqs[i]) if (i != r && eqs[i][col]) eqs[i] ^= eqs[r];  // (3)!
            pivots.push_back(col);
          end
          ok = 1;
          for (int i = pivots.size(); i < eqs.size(); i++) if (eqs[i][nvars]) ok = 0;   // (4)!
          x = '0;
          foreach (pivots[i]) x[pivots[i]] = eqs[i][nvars];
          return nvars - pivots.size();
        endfunction

        // The presses that turn every light of lit off (ok = 0 if none), and the free variables.
        function automatic int solve_lights(int n, vec_t lit, bit diag, output vec_t x, output bit ok);
          vec_t masks[$], eqs[$];
          press_masks(n, diag, masks);
          for (int j = 0; j < n * n; j++) begin
            vec_t e = masks[j];                                           // (5)!
            e[n * n] = lit[j];
            eqs.push_back(e);
          end
          return gauss(eqs, n * n, x, ok);
        endfunction
        ```

        1. אותה מסכה כמו ב-Python : באלכסון רק עם `diag`, ורק בתוך הלוח.
        2. עמודה בלי ציר : משתנה חופשי.
        3. ‏XOR של וקטור של 128 ביטים, פעולה אחת לשורה.
        4. שורה בלי ציר שהצד הימני שלה 1 : אין פתרון.
        5. השורה של הנורה \( j \) היא המסכה שלה, והצד הימני בביט \( n^2 \). השם `solve_lights` ולא
           `solve`, כי `solve` היא מילה שמורה ב-SystemVerilog (‏`solve ... before` באילוצים).

    #### למה זה נכון { .sol-proof }

    **הסדר והלחיצות הכפולות.** לחיצה על \( i \) מחליפה את הלוח \( b \) ב-\( b \oplus m_i \), כש-\( m_i \)
    המסכה שלה. ‏XOR חילופי וקיבוצי ו-\( m_i \oplus m_i = 0 \), ולכן אחרי כל סדרת לחיצות הלוח הוא
    \( b \oplus \bigoplus_i x_i m_i \), כש-\( x_i \) הזוגיות של מספר הלחיצות על \( i \).

    **המערכת.** הלוח כבוי בדיוק כש-\( \bigoplus_i x_i m_i = b \), ובכל ביט \( j \) זו המשוואה
    \( \bigoplus_i A_{ji} x_i = b_j \).

    **הדירוג.** החלפת שתי משוואות, והחלפת משוואה ב-XOR שלה עם אחרת, לא משנות את קבוצת הפתרונות :
    כל פתרון של שתיהן מקיים גם את ה-XOR, והפעולה הפוכה לעצמה. בסוף, כל עמודה עם ציר מופיעה רק
    במשוואה של הציר שלה, ולכן הצבה של 0 במשתנים החופשיים קובעת את השאר.

    **יחידות ב-3 על 3.** הדירוג מוצא ציר בכל 9 העמודות. אין משתנים חופשיים, \( A \) הפיכה, ולכל
    \( b \) יש פתרון אחד בדיוק, \( x = A^{-1} b \). בדוגמה הוא הלחיצות 3, 4, 5 ו-7.

    #### סיבוכיות { .sol-cost }

    יש \( N = n^2 \) נעלמים ו-\( N \) משוואות. לכל עמודה XOR עם עד \( N \) משוואות באורך
    \( N + 1 \) ביטים : זמן \( O(N^3) = O(n^6) \) פעולות על ביטים, או \( O(n^6 / w) \) כשמשוואה
    יושבת במילים של \( w \) ביטים, כמו המספר השלם ב-Python והווקטור ב-SystemVerilog. זיכרון
    \( O(n^4) \) ביטים.

---

### סעיף ב – לוח של 6 על 6, ומה שונה ב-5 על 5 { #six }

האם בלוח של 6 על 6 אפשר לכבות כל מצב? ובלוח של 5 על 5? כמה מהמצבים אפשר לכבות, ובכמה דרכים?
מצאו גם דרך לפתור שמשתמשת ב-\( n \) נעלמים בלבד, במקום \( n^2 \).

??? tip "רמז 1"
    הריצו את הדירוג של סעיף א וספרו משתנים חופשיים. מה הם אומרים על מספר הפתרונות, ועל מספר
    המצבים שאפשר לכבות?

??? tip "רמז 2"
    לחיצה בשורה \( r + 1 \) היא הדרך היחידה לכבות נורה בשורה \( r \) בלי לגעת בשורות שמעליה. מה
    קורה אם לוחצים מתחת לכל נורה דולקת, שורה אחרי שורה?

??? tip "רמז 3"
    מה שנשאר בשורה התחתונה נקבע לגמרי לפי הלחיצות בשורה העליונה, ובאופן לינארי.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ב-6 על 6 הדרגה 36 : כל מצב אפשר לכבות, בדרך אחת. ב-5 על 5 הדרגה 23, ויש 2 משתנים חופשיים.
        לכן יש שלושה דפוסים "שקטים", לחיצות שלא משנות אף נורה, ורק רבע מהמצבים אפשר לכבות, כל
        אחד ב-4 דרכים. מצב אפשר לכבות בדיוק כשבתוך כל דפוס שקט יש מספר זוגי של נורות דולקות.
        ברדיפת אורות לוחצים מתחת לכל נורה דולקת, שורה אחרי שורה. מה שנשאר בשורה התחתונה הוא
        פונקציה לינארית של \( n \) הלחיצות בשורה העליונה, ולכן מספיק לפתור \( n \) משוואות.

    <!-- cost: זמן \( O(n^3) \) ברדיפת אורות | זיכרון \( O(n^2) \) -->

    #### הרעיון { .sol-idea }

    הדירוג של סעיף א נותן לכל גודל את מספר המשתנים החופשיים, ומהם נובע כל השאר. כש-\( f \)
    משתנים חופשיים, ל-\( A \) יש \( 2^f \) וקטורים שהיא שולחת ל-0, ואלה הדפוסים השקטים. אם \( x \)
    פתרון, גם \( x \oplus q \) פתרון לכל דפוס שקט \( q \) : לכל מצב שאפשר לכבות יש \( 2^f \)
    פתרונות, ורק \( 2^{N - f} \) מתוך \( 2^N \) המצבים אפשר לכבות :

    <!-- gen 3 -->

    | הלוח | נעלמים | הדרגה | משתנים חופשיים | המצבים שאפשר לכבות | פתרונות לכל מצב כזה |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | 3 × 3 | 9 | 9 | 0 | כולם | 1 |
    | 4 × 4 | 16 | 12 | 4 | ‏1 מתוך 16 | 16 |
    | 5 × 5 | 25 | 23 | 2 | ‏1 מתוך 4 | 4 |
    | 6 × 6 | 36 | 36 | 0 | כולם | 1 |
    | 7 × 7 | 49 | 49 | 0 | כולם | 1 |

    <!-- /gen -->

    אלה שלושת הדפוסים השקטים של 5 על 5. כל אחד הופך כל נורה מספר זוגי של פעמים :

    <!-- gen 4 -->

    <svg class="figure lo-fig" viewBox="0 0 386 116" style="max-width:24.1rem" role="img" aria-label="סעיף ב : שלושת הדפוסים השקטים של הלוח 5 על 5, לחיצות שלא משנות אף נורה. כל אחד מהם הוא סכום XOR של שני האחרים, ויחד עם הדפוס הריק הם ארבעה"><rect class="lo-cell" x="274" y="2" width="22" height="22"/><circle class="lo-off" cx="285" cy="13" r="5.9"/><rect class="lo-cell" x="296" y="2" width="22" height="22"/><rect class="lo-press" x="299" y="5" width="16" height="16" rx="4"/><circle class="lo-off" cx="307" cy="13" r="5.9"/><rect class="lo-cell" x="318" y="2" width="22" height="22"/><rect class="lo-press" x="321" y="5" width="16" height="16" rx="4"/><circle class="lo-off" cx="329" cy="13" r="5.9"/><rect class="lo-cell" x="340" y="2" width="22" height="22"/><rect class="lo-press" x="343" y="5" width="16" height="16" rx="4"/><circle class="lo-off" cx="351" cy="13" r="5.9"/><rect class="lo-cell" x="362" y="2" width="22" height="22"/><circle class="lo-off" cx="373" cy="13" r="5.9"/><rect class="lo-cell" x="274" y="24" width="22" height="22"/><rect class="lo-press" x="277" y="27" width="16" height="16" rx="4"/><circle class="lo-off" cx="285" cy="35" r="5.9"/><rect class="lo-cell" x="296" y="24" width="22" height="22"/><circle class="lo-off" cx="307" cy="35" r="5.9"/><rect class="lo-cell" x="318" y="24" width="22" height="22"/><rect class="lo-press" x="321" y="27" width="16" height="16" rx="4"/><circle class="lo-off" cx="329" cy="35" r="5.9"/><rect class="lo-cell" x="340" y="24" width="22" height="22"/><circle class="lo-off" cx="351" cy="35" r="5.9"/><rect class="lo-cell" x="362" y="24" width="22" height="22"/><rect class="lo-press" x="365" y="27" width="16" height="16" rx="4"/><circle class="lo-off" cx="373" cy="35" r="5.9"/><rect class="lo-cell" x="274" y="46" width="22" height="22"/><rect class="lo-press" x="277" y="49" width="16" height="16" rx="4"/><circle class="lo-off" cx="285" cy="57" r="5.9"/><rect class="lo-cell" x="296" y="46" width="22" height="22"/><rect class="lo-press" x="299" y="49" width="16" height="16" rx="4"/><circle class="lo-off" cx="307" cy="57" r="5.9"/><rect class="lo-cell" x="318" y="46" width="22" height="22"/><circle class="lo-off" cx="329" cy="57" r="5.9"/><rect class="lo-cell" x="340" y="46" width="22" height="22"/><rect class="lo-press" x="343" y="49" width="16" height="16" rx="4"/><circle class="lo-off" cx="351" cy="57" r="5.9"/><rect class="lo-cell" x="362" y="46" width="22" height="22"/><rect class="lo-press" x="365" y="49" width="16" height="16" rx="4"/><circle class="lo-off" cx="373" cy="57" r="5.9"/><rect class="lo-cell" x="274" y="68" width="22" height="22"/><rect class="lo-press" x="277" y="71" width="16" height="16" rx="4"/><circle class="lo-off" cx="285" cy="79" r="5.9"/><rect class="lo-cell" x="296" y="68" width="22" height="22"/><circle class="lo-off" cx="307" cy="79" r="5.9"/><rect class="lo-cell" x="318" y="68" width="22" height="22"/><rect class="lo-press" x="321" y="71" width="16" height="16" rx="4"/><circle class="lo-off" cx="329" cy="79" r="5.9"/><rect class="lo-cell" x="340" y="68" width="22" height="22"/><circle class="lo-off" cx="351" cy="79" r="5.9"/><rect class="lo-cell" x="362" y="68" width="22" height="22"/><rect class="lo-press" x="365" y="71" width="16" height="16" rx="4"/><circle class="lo-off" cx="373" cy="79" r="5.9"/><rect class="lo-cell" x="274" y="90" width="22" height="22"/><circle class="lo-off" cx="285" cy="101" r="5.9"/><rect class="lo-cell" x="296" y="90" width="22" height="22"/><rect class="lo-press" x="299" y="93" width="16" height="16" rx="4"/><circle class="lo-off" cx="307" cy="101" r="5.9"/><rect class="lo-cell" x="318" y="90" width="22" height="22"/><rect class="lo-press" x="321" y="93" width="16" height="16" rx="4"/><circle class="lo-off" cx="329" cy="101" r="5.9"/><rect class="lo-cell" x="340" y="90" width="22" height="22"/><rect class="lo-press" x="343" y="93" width="16" height="16" rx="4"/><circle class="lo-off" cx="351" cy="101" r="5.9"/><rect class="lo-cell" x="362" y="90" width="22" height="22"/><circle class="lo-off" cx="373" cy="101" r="5.9"/><rect class="lo-frame" x="274" y="2" width="110" height="110"/><rect class="lo-cell" x="138" y="2" width="22" height="22"/><rect class="lo-press" x="141" y="5" width="16" height="16" rx="4"/><circle class="lo-off" cx="149" cy="13" r="5.9"/><rect class="lo-cell" x="160" y="2" width="22" height="22"/><circle class="lo-off" cx="171" cy="13" r="5.9"/><rect class="lo-cell" x="182" y="2" width="22" height="22"/><rect class="lo-press" x="185" y="5" width="16" height="16" rx="4"/><circle class="lo-off" cx="193" cy="13" r="5.9"/><rect class="lo-cell" x="204" y="2" width="22" height="22"/><circle class="lo-off" cx="215" cy="13" r="5.9"/><rect class="lo-cell" x="226" y="2" width="22" height="22"/><rect class="lo-press" x="229" y="5" width="16" height="16" rx="4"/><circle class="lo-off" cx="237" cy="13" r="5.9"/><rect class="lo-cell" x="138" y="24" width="22" height="22"/><rect class="lo-press" x="141" y="27" width="16" height="16" rx="4"/><circle class="lo-off" cx="149" cy="35" r="5.9"/><rect class="lo-cell" x="160" y="24" width="22" height="22"/><circle class="lo-off" cx="171" cy="35" r="5.9"/><rect class="lo-cell" x="182" y="24" width="22" height="22"/><rect class="lo-press" x="185" y="27" width="16" height="16" rx="4"/><circle class="lo-off" cx="193" cy="35" r="5.9"/><rect class="lo-cell" x="204" y="24" width="22" height="22"/><circle class="lo-off" cx="215" cy="35" r="5.9"/><rect class="lo-cell" x="226" y="24" width="22" height="22"/><rect class="lo-press" x="229" y="27" width="16" height="16" rx="4"/><circle class="lo-off" cx="237" cy="35" r="5.9"/><rect class="lo-cell" x="138" y="46" width="22" height="22"/><circle class="lo-off" cx="149" cy="57" r="5.9"/><rect class="lo-cell" x="160" y="46" width="22" height="22"/><circle class="lo-off" cx="171" cy="57" r="5.9"/><rect class="lo-cell" x="182" y="46" width="22" height="22"/><circle class="lo-off" cx="193" cy="57" r="5.9"/><rect class="lo-cell" x="204" y="46" width="22" height="22"/><circle class="lo-off" cx="215" cy="57" r="5.9"/><rect class="lo-cell" x="226" y="46" width="22" height="22"/><circle class="lo-off" cx="237" cy="57" r="5.9"/><rect class="lo-cell" x="138" y="68" width="22" height="22"/><rect class="lo-press" x="141" y="71" width="16" height="16" rx="4"/><circle class="lo-off" cx="149" cy="79" r="5.9"/><rect class="lo-cell" x="160" y="68" width="22" height="22"/><circle class="lo-off" cx="171" cy="79" r="5.9"/><rect class="lo-cell" x="182" y="68" width="22" height="22"/><rect class="lo-press" x="185" y="71" width="16" height="16" rx="4"/><circle class="lo-off" cx="193" cy="79" r="5.9"/><rect class="lo-cell" x="204" y="68" width="22" height="22"/><circle class="lo-off" cx="215" cy="79" r="5.9"/><rect class="lo-cell" x="226" y="68" width="22" height="22"/><rect class="lo-press" x="229" y="71" width="16" height="16" rx="4"/><circle class="lo-off" cx="237" cy="79" r="5.9"/><rect class="lo-cell" x="138" y="90" width="22" height="22"/><rect class="lo-press" x="141" y="93" width="16" height="16" rx="4"/><circle class="lo-off" cx="149" cy="101" r="5.9"/><rect class="lo-cell" x="160" y="90" width="22" height="22"/><circle class="lo-off" cx="171" cy="101" r="5.9"/><rect class="lo-cell" x="182" y="90" width="22" height="22"/><rect class="lo-press" x="185" y="93" width="16" height="16" rx="4"/><circle class="lo-off" cx="193" cy="101" r="5.9"/><rect class="lo-cell" x="204" y="90" width="22" height="22"/><circle class="lo-off" cx="215" cy="101" r="5.9"/><rect class="lo-cell" x="226" y="90" width="22" height="22"/><rect class="lo-press" x="229" y="93" width="16" height="16" rx="4"/><circle class="lo-off" cx="237" cy="101" r="5.9"/><rect class="lo-frame" x="138" y="2" width="110" height="110"/><rect class="lo-cell" x="2" y="2" width="22" height="22"/><rect class="lo-press" x="5" y="5" width="16" height="16" rx="4"/><circle class="lo-off" cx="13" cy="13" r="5.9"/><rect class="lo-cell" x="24" y="2" width="22" height="22"/><rect class="lo-press" x="27" y="5" width="16" height="16" rx="4"/><circle class="lo-off" cx="35" cy="13" r="5.9"/><rect class="lo-cell" x="46" y="2" width="22" height="22"/><circle class="lo-off" cx="57" cy="13" r="5.9"/><rect class="lo-cell" x="68" y="2" width="22" height="22"/><rect class="lo-press" x="71" y="5" width="16" height="16" rx="4"/><circle class="lo-off" cx="79" cy="13" r="5.9"/><rect class="lo-cell" x="90" y="2" width="22" height="22"/><rect class="lo-press" x="93" y="5" width="16" height="16" rx="4"/><circle class="lo-off" cx="101" cy="13" r="5.9"/><rect class="lo-cell" x="2" y="24" width="22" height="22"/><circle class="lo-off" cx="13" cy="35" r="5.9"/><rect class="lo-cell" x="24" y="24" width="22" height="22"/><circle class="lo-off" cx="35" cy="35" r="5.9"/><rect class="lo-cell" x="46" y="24" width="22" height="22"/><circle class="lo-off" cx="57" cy="35" r="5.9"/><rect class="lo-cell" x="68" y="24" width="22" height="22"/><circle class="lo-off" cx="79" cy="35" r="5.9"/><rect class="lo-cell" x="90" y="24" width="22" height="22"/><circle class="lo-off" cx="101" cy="35" r="5.9"/><rect class="lo-cell" x="2" y="46" width="22" height="22"/><rect class="lo-press" x="5" y="49" width="16" height="16" rx="4"/><circle class="lo-off" cx="13" cy="57" r="5.9"/><rect class="lo-cell" x="24" y="46" width="22" height="22"/><rect class="lo-press" x="27" y="49" width="16" height="16" rx="4"/><circle class="lo-off" cx="35" cy="57" r="5.9"/><rect class="lo-cell" x="46" y="46" width="22" height="22"/><circle class="lo-off" cx="57" cy="57" r="5.9"/><rect class="lo-cell" x="68" y="46" width="22" height="22"/><rect class="lo-press" x="71" y="49" width="16" height="16" rx="4"/><circle class="lo-off" cx="79" cy="57" r="5.9"/><rect class="lo-cell" x="90" y="46" width="22" height="22"/><rect class="lo-press" x="93" y="49" width="16" height="16" rx="4"/><circle class="lo-off" cx="101" cy="57" r="5.9"/><rect class="lo-cell" x="2" y="68" width="22" height="22"/><circle class="lo-off" cx="13" cy="79" r="5.9"/><rect class="lo-cell" x="24" y="68" width="22" height="22"/><circle class="lo-off" cx="35" cy="79" r="5.9"/><rect class="lo-cell" x="46" y="68" width="22" height="22"/><circle class="lo-off" cx="57" cy="79" r="5.9"/><rect class="lo-cell" x="68" y="68" width="22" height="22"/><circle class="lo-off" cx="79" cy="79" r="5.9"/><rect class="lo-cell" x="90" y="68" width="22" height="22"/><circle class="lo-off" cx="101" cy="79" r="5.9"/><rect class="lo-cell" x="2" y="90" width="22" height="22"/><rect class="lo-press" x="5" y="93" width="16" height="16" rx="4"/><circle class="lo-off" cx="13" cy="101" r="5.9"/><rect class="lo-cell" x="24" y="90" width="22" height="22"/><rect class="lo-press" x="27" y="93" width="16" height="16" rx="4"/><circle class="lo-off" cx="35" cy="101" r="5.9"/><rect class="lo-cell" x="46" y="90" width="22" height="22"/><circle class="lo-off" cx="57" cy="101" r="5.9"/><rect class="lo-cell" x="68" y="90" width="22" height="22"/><rect class="lo-press" x="71" y="93" width="16" height="16" rx="4"/><circle class="lo-off" cx="79" cy="101" r="5.9"/><rect class="lo-cell" x="90" y="90" width="22" height="22"/><rect class="lo-press" x="93" y="93" width="16" height="16" rx="4"/><circle class="lo-off" cx="101" cy="101" r="5.9"/><rect class="lo-frame" x="2" y="2" width="110" height="110"/></svg>

    <span class="viz-legend"><span><i class="lo-key-press"></i>לחיצה בדפוס השקט</span><span><i class="lo-key-off"></i>כל הנורות נשארות כמו שהן</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הרדיפה :** לכל שורה \( r \) מ-0 עד \( n - 2 \), לכל נורה דולקת בה, לוחצים על המשבצת
       שמתחתיה. הלחיצה מכבה אותה, ולא נוגעת בשורות שמעל \( r \).

    2. **מה שנשאר :** אחרי הרדיפה כל השורות כבויות חוץ מהתחתונה, ובה נשאר וקטור \( \ell \) של
       \( n \) ביטים.

    3. **השורה העליונה :** רדיפה מלוח כבוי, אחרי לחיצות \( f \) בשורה העליונה, משאירה \( L f \).
       הרדיפה לינארית, ולכן רדיפה מהלוח שלנו אחרי \( f \) משאירה \( \ell \oplus L f \). פותרים
       \( L f = \ell \) : ‏\( n \) משוואות. העמודה \( c \) של \( L \) היא מה שנשאר אחרי רדיפה מלחיצה
       אחת, בעמודה \( c \).

    4. **רדיפה שנייה :** לוחצים על \( f \) בשורה העליונה ורודפים שוב. הפעם גם השורה התחתונה נכבית.
       אם ל-\( L f = \ell \) אין פתרון, אי אפשר לכבות את הלוח.

    </div>

    ב-5 על 5 אפשר לשנן את המערכת הקטנה כטבלה : לכל שורה תחתונה שהרדיפה יכולה להשאיר, הלחיצות
    בשורה העליונה (העמודה 0 משמאל). רק 8 מתוך 32 השורות התחתונות מופיעות, עוד דרך לראות שרק רבע
    מהמצבים אפשר לכבות :

    <!-- gen 5 -->

    | נשארו דולקות בשורה התחתונה | לוחצים בשורה העליונה | לחיצות |
    |:-:|:-:|:-:|
    | ‏<span dir="ltr">00000</span> | ‏<span dir="ltr">00000</span> | 0 |
    | ‏<span dir="ltr">00111</span> | ‏<span dir="ltr">00010</span> | 1 |
    | ‏<span dir="ltr">01010</span> | ‏<span dir="ltr">01001</span> | 2 |
    | ‏<span dir="ltr">01101</span> | ‏<span dir="ltr">10000</span> | 1 |
    | ‏<span dir="ltr">10001</span> | ‏<span dir="ltr">00011</span> | 2 |
    | ‏<span dir="ltr">10110</span> | ‏<span dir="ltr">00001</span> | 1 |
    | ‏<span dir="ltr">11011</span> | ‏<span dir="ltr">00100</span> | 1 |
    | ‏<span dir="ltr">11100</span> | ‏<span dir="ltr">01000</span> | 1 |

    <!-- /gen -->

    בתיבה כל הנורות של 5 על 5 דולקות. כל צעד הוא לחיצה אחת של הרדיפה, ואחרי השורה התחתונה מגיעים
    התיקון של השורה העליונה והרדיפה השנייה :

    <div class="explorer" data-kind="lightsout" data-mode="chase" data-n="5" data-lit="1ffffff"></div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="chase, solve_by_chasing" linenums="1" hl_lines="10 11 12 20 26"
        def chase(n: int, lit: int, first: int = 0) -> tuple[int, int]:
            """Press the cells of first (bits 0..n-1) on row 0, then, row by row, the cell under
            every light still on. Returns (the presses, the lights left on the bottom row)."""
            masks, press = press_masks(n), 0
            for c in range(n):
                if first >> c & 1:
                    press, lit = press | 1 << c, lit ^ masks[c]
            for r in range(n - 1):
                for c in range(n):
                    if lit >> (r * n + c) & 1:                     # (1)!
                        k = (r + 1) * n + c
                        press, lit = press | 1 << k, lit ^ masks[k]
            return press, lit >> (n - 1) * n


        def solve_by_chasing(n: int, lit: int) -> int | None:
            """Part b: the presses by light chasing. The bottom row is an affine function of the
            first row, so n equations in the n presses of row 0 replace n*n."""
            rest = chase(n, lit)[1]
            cols = [chase(n, 0, 1 << c)[1] for c in range(n)]      # (2)!
            eqs = [sum((cols[c] >> b & 1) << c for c in range(n)) | (rest >> b & 1) << n
                   for b in range(n)]
            first, _ = gauss(eqs, n)
            if first is None:
                return None                                        # (3)!
            return chase(n, lit, first)[0]
        ```

        1. נורה דולקת בשורה \( r \) : לוחצים מתחתיה. ‏`press | 1 << k` ולא XOR, כי בכל מעבר כל
           משבצת נלחצת לכל היותר פעם אחת.
        2. העמודה \( c \) של \( L \) : מה שנשאר אחרי רדיפה מלוח כבוי, עם לחיצה אחת בשורה העליונה.
        3. אין שורה עליונה שמנקה את \( \ell \) : הלוח לא פתיר.

    === "SystemVerilog"
        ```systemverilog title="chase, solve_by_chasing" linenums="1" hl_lines="10 11 12 26 36"
        // Part b: press first on row 0, then under every light still on, row by row. Returns the
        // presses; rest gets the lights left on the bottom row (bit c for column c).
        function automatic vec_t chase(int n, vec_t lit, vec_t first, output vec_t rest);
          vec_t masks[$], press = '0;
          press_masks(n, 0, masks);
          for (int c = 0; c < n; c++)
            if (first[c]) begin press[c] = 1; lit ^= masks[c]; end
          for (int r = 0; r < n - 1; r++)
            for (int c = 0; c < n; c++)
              if (lit[r * n + c]) begin                                   // (1)!
                press[(r + 1) * n + c] = 1;
                lit ^= masks[(r + 1) * n + c];
              end
          rest = lit >> ((n - 1) * n);
          return press;
        endfunction

        // The presses by light chasing: n equations in the n presses of row 0. Returns 0 if none.
        function automatic bit solve_by_chasing(int n, vec_t lit, output vec_t press);
          vec_t rest, col[$], eqs[$], first, unused, one, r;
          bit ok;
          void'(chase(n, lit, '0, rest));
          for (int c = 0; c < n; c++) begin
            one = '0;
            one[c] = 1;
            void'(chase(n, '0, one, r));                                  // (2)!
            col.push_back(r);
          end
          for (int b = 0; b < n; b++) begin
            vec_t e = '0;
            for (int c = 0; c < n; c++) e[c] = col[c][b];
            e[n] = rest[b];
            eqs.push_back(e);
          end
          void'(gauss(eqs, n, first, ok));
          if (!ok) return 0;                                              // (3)!
          press = chase(n, lit, first, unused);
          return 1;
        endfunction
        ```

        1. כמו ב-Python : נורה דולקת, לחיצה מתחתיה.
        2. העמודה \( c \) של \( L \) מרדיפה מלחיצה אחת.
        3. ‏`gauss` של סעיף א על המערכת הקטנה, של \( n \) נעלמים.

    #### למה זה נכון { .sol-proof }

    **הרדיפה.** לחיצה על \( (r + 1, c) \) הופכת בשורה \( r \) רק את \( (r, c) \), ולא נוגעת בשורות
    שמעליה. לכן אחרי המעבר על שורה \( r \) היא כבויה, והשורות הבאות לא מדליקות אותה שוב.

    **הלינאריות.** כל החלטה של הרדיפה, ללחוץ או לא, היא הערך של נורה אחת ברגע ההחלטה, וזה XOR של
    ביטים של הלוח ההתחלתי ושל \( f \). לכן גם השורה שנשארת היא XOR כזה :
    \( \text{rest}(b, f) = \text{rest}(b, 0) \oplus \text{rest}(0, f) = \ell \oplus L f \).

    **אין פתרון שהרדיפה מפספסת.** בכל פתרון, הלחיצות בשורה \( r + 1 \) נקבעות לפי השורות שמעליהן :
    בשורה \( r \) נשארות דולקות רק נורות שאין מתחתן לחיצה, ולכן חייבים ללחוץ בדיוק מתחת לנורות
    שדולקות בה. כך כל פתרון נקבע לפי השורה העליונה שלו, והשורה הזו פותרת \( L f = \ell \).

    **מבחן הזוגיות.** \( A \) סימטרית, ולכן לכל דפוס שקט \( q \) ולכל לחיצה \( m_i = A e_i \) :
    \( q \cdot m_i = q^\top A e_i = (A q)^\top e_i = 0 \). כל לחיצה משנה את מספר הנורות הדולקות בתוך
    \( q \) במספר זוגי, ולכן הזוגיות \( q \cdot b \) לא משתנה. אם היא 1, הלוח לא יגיע ל-0. בכיוון
    השני, התמונה של מטריצה סימטרית היא המשלים האורתוגונלי של הגרעין שלה, ולכן אם \( q \cdot b = 0 \)
    לכל \( q \) שקט, יש פתרון. ב-5 על 5 הגרעין נפרש על ידי שני דפוסים, כל אחד מהם פוסל חצי מהמצבים,
    ונשאר רבע.

    **‏6 על 6.** הדירוג מוצא 36 צירים : אין דפוס שקט, וכל מצב אפשר לכבות בדרך אחת.

    #### סיבוכיות { .sol-cost }

    רדיפה עוברת על \( n^2 \) משבצות, וכל לחיצה הופכת עד 5 נורות : ‏\( O(n^2) \). הקוד רודף
    \( n + 2 \) פעמים ופותר מערכת של \( n \) נעלמים, ולכן זמן \( O(n^3) \), במקום \( O(n^6) \) של
    סעיף א. זיכרון \( O(n^2) \).

---

### סעיף ג – עם אלכסונים { #diagonals }

עכשיו לחיצה הופכת את הנורה ואת כל שמונה השכנות שלה, גם באלכסון. הוכיחו שבלוח של \( n \times n \)
אפשר לכבות כל מצב אם ורק אם \( n \bmod 3 \ne 2 \), ושכאשר \( n \bmod 3 = 2 \) יש בדיוק
\( 2n - 1 \) משתנים חופשיים.

??? tip "רמז 1"
    התחילו משורה אחת של \( n \) נורות, שבה לחיצה הופכת נורה ואת שתי השכנות שלה בשורה. אילו לחיצות
    לא משנות כלום?

??? tip "רמז 2"
    כתבו את הלחיצות כמטריצה \( X \) של \( n \) על \( n \). לחיצה עם אלכסונים היא "שורה אחת" לאורך
    העמודות ואחר כך "שורה אחת" לאורך השורות. כש-\( P \) היא המטריצה של שורה אחת, האפקט הוא
    \( P X P \).

??? tip "רמז 3"
    מתי \( P X P = 0 \)? כל עמודה של \( X P \) חייבת להיות בגרעין של \( P \).

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        נסמן ב-\( P \) את המטריצה של \( n \) על \( n \) עם אחדות על האלכסון ומשני צדדיו : שורה אחת
        שבה לחיצה הופכת נורה ואת שתי השכנות שלה. לחיצות \( X \) על הלוח עם אלכסונים הופכות את
        \( P X P \). המטריצה \( P \) לא הפיכה בדיוק כש-\( n \bmod 3 = 2 \), ואז הגרעין שלה הוא
        הווקטור \( u \) = <span dir="ltr">1 1 0 1 1 0 … 1 1</span>. הלחיצות השקטות נפרשות על ידי
        \( u \) לאורך כל אחת מ-\( n \) העמודות ולאורך כל אחת מ-\( n \) השורות, עם תלות אחת ביניהן,
        ולכן יש \( 2n - 1 \) משתנים חופשיים. ב-5 על 5 הם 9.

    <!-- cost: זמן \( O(1) \) לבדיקה \( n \bmod 3 \), ‏\( O(n^3) \) לבניית הדפוסים | זיכרון \( O(n^3) \) -->

    #### הרעיון { .sol-idea }

    עם אלכסונים, לחיצה על \( (r, c) \) הופכת כל \( (r', c') \) עם \( |r - r'| \le 1 \) ו-\( |c - c'| \le 1 \).
    התנאי נפרד לשורה ולעמודה, ולכן הלוח הוא "מכפלה" של שתי שורות. בשורה אחת של 5 נורות, לחיצה
    על הנורות 0, 1, 3 ו-4 הופכת כל נורה פעמיים :

    <!-- gen 6 -->

    <svg class="figure lo-fig" viewBox="0 0 204 114" style="max-width:12.8rem" role="img" aria-label="סעיף ג : שורה של 5 נורות, ולחיצה הופכת נורה ואת שתי השכנות שלה בשורה. לוחצים על הנורות 0, 1, 3 ו-4. מתחת, כמה פעמים כל נורה מתהפכת : 2, 2, 2, 2, 2. כל נורה מתהפכת מספר זוגי של פעמים, ולכן הלחיצות לא משנות כלום"><rect class="lo-cell" x="2" y="2" width="40" height="40"/><rect class="lo-press" x="5" y="5" width="34" height="34" rx="4"/><circle class="lo-off" cx="22" cy="22" r="10.8"/><text class="lo-num" x="22" y="70" text-anchor="middle">2</text><rect class="lo-cell" x="42" y="2" width="40" height="40"/><rect class="lo-press" x="45" y="5" width="34" height="34" rx="4"/><circle class="lo-off" cx="62" cy="22" r="10.8"/><text class="lo-num" x="62" y="70" text-anchor="middle">2</text><rect class="lo-cell" x="82" y="2" width="40" height="40"/><circle class="lo-off" cx="102" cy="22" r="10.8"/><text class="lo-num" x="102" y="70" text-anchor="middle">2</text><rect class="lo-cell" x="122" y="2" width="40" height="40"/><rect class="lo-press" x="125" y="5" width="34" height="34" rx="4"/><circle class="lo-off" cx="142" cy="22" r="10.8"/><text class="lo-num" x="142" y="70" text-anchor="middle">2</text><rect class="lo-cell" x="162" y="2" width="40" height="40"/><rect class="lo-press" x="165" y="5" width="34" height="34" rx="4"/><circle class="lo-off" cx="182" cy="22" r="10.8"/><text class="lo-num" x="182" y="70" text-anchor="middle">2</text><rect class="lo-frame" x="2" y="2" width="200" height="40"/><text class="lo-cap" x="102" y="108" text-anchor="middle" direction="rtl">כמה פעמים כל נורה מתהפכת</text></svg>

    <!-- /gen -->

    כשמניחים את הדפוס הזה לאורך עמודה, או לאורך שורה, הוא שקט גם בלוח :

    <!-- gen 7 -->

    <svg class="figure lo-fig" viewBox="0 0 454 162" style="max-width:28.4rem" role="img" aria-label="סעיף ג : שלושה דפוסים שקטים של הלוח 5 על 5 עם אלכסונים. הראשון הוא 1 1 0 1 1 בעמודה 0, השני 1 1 0 1 1 בשורה 0, והשלישי הלחיצות בכל משבצת שהשורה שלה והעמודה שלה הן 0, 1, 3 או 4"><rect class="lo-cell" x="322" y="2" width="26" height="26"/><rect class="lo-press" x="325" y="5" width="20" height="20" rx="4"/><circle class="lo-off" cx="335" cy="15" r="7.0"/><rect class="lo-cell" x="348" y="2" width="26" height="26"/><circle class="lo-off" cx="361" cy="15" r="7.0"/><rect class="lo-cell" x="374" y="2" width="26" height="26"/><circle class="lo-off" cx="387" cy="15" r="7.0"/><rect class="lo-cell" x="400" y="2" width="26" height="26"/><circle class="lo-off" cx="413" cy="15" r="7.0"/><rect class="lo-cell" x="426" y="2" width="26" height="26"/><circle class="lo-off" cx="439" cy="15" r="7.0"/><rect class="lo-cell" x="322" y="28" width="26" height="26"/><rect class="lo-press" x="325" y="31" width="20" height="20" rx="4"/><circle class="lo-off" cx="335" cy="41" r="7.0"/><rect class="lo-cell" x="348" y="28" width="26" height="26"/><circle class="lo-off" cx="361" cy="41" r="7.0"/><rect class="lo-cell" x="374" y="28" width="26" height="26"/><circle class="lo-off" cx="387" cy="41" r="7.0"/><rect class="lo-cell" x="400" y="28" width="26" height="26"/><circle class="lo-off" cx="413" cy="41" r="7.0"/><rect class="lo-cell" x="426" y="28" width="26" height="26"/><circle class="lo-off" cx="439" cy="41" r="7.0"/><rect class="lo-cell" x="322" y="54" width="26" height="26"/><circle class="lo-off" cx="335" cy="67" r="7.0"/><rect class="lo-cell" x="348" y="54" width="26" height="26"/><circle class="lo-off" cx="361" cy="67" r="7.0"/><rect class="lo-cell" x="374" y="54" width="26" height="26"/><circle class="lo-off" cx="387" cy="67" r="7.0"/><rect class="lo-cell" x="400" y="54" width="26" height="26"/><circle class="lo-off" cx="413" cy="67" r="7.0"/><rect class="lo-cell" x="426" y="54" width="26" height="26"/><circle class="lo-off" cx="439" cy="67" r="7.0"/><rect class="lo-cell" x="322" y="80" width="26" height="26"/><rect class="lo-press" x="325" y="83" width="20" height="20" rx="4"/><circle class="lo-off" cx="335" cy="93" r="7.0"/><rect class="lo-cell" x="348" y="80" width="26" height="26"/><circle class="lo-off" cx="361" cy="93" r="7.0"/><rect class="lo-cell" x="374" y="80" width="26" height="26"/><circle class="lo-off" cx="387" cy="93" r="7.0"/><rect class="lo-cell" x="400" y="80" width="26" height="26"/><circle class="lo-off" cx="413" cy="93" r="7.0"/><rect class="lo-cell" x="426" y="80" width="26" height="26"/><circle class="lo-off" cx="439" cy="93" r="7.0"/><rect class="lo-cell" x="322" y="106" width="26" height="26"/><rect class="lo-press" x="325" y="109" width="20" height="20" rx="4"/><circle class="lo-off" cx="335" cy="119" r="7.0"/><rect class="lo-cell" x="348" y="106" width="26" height="26"/><circle class="lo-off" cx="361" cy="119" r="7.0"/><rect class="lo-cell" x="374" y="106" width="26" height="26"/><circle class="lo-off" cx="387" cy="119" r="7.0"/><rect class="lo-cell" x="400" y="106" width="26" height="26"/><circle class="lo-off" cx="413" cy="119" r="7.0"/><rect class="lo-cell" x="426" y="106" width="26" height="26"/><circle class="lo-off" cx="439" cy="119" r="7.0"/><rect class="lo-frame" x="322" y="2" width="130" height="130"/><text class="lo-cap" x="387" y="152" text-anchor="middle" direction="rtl">בעמודה 0</text><rect class="lo-cell" x="162" y="2" width="26" height="26"/><rect class="lo-press" x="165" y="5" width="20" height="20" rx="4"/><circle class="lo-off" cx="175" cy="15" r="7.0"/><rect class="lo-cell" x="188" y="2" width="26" height="26"/><rect class="lo-press" x="191" y="5" width="20" height="20" rx="4"/><circle class="lo-off" cx="201" cy="15" r="7.0"/><rect class="lo-cell" x="214" y="2" width="26" height="26"/><circle class="lo-off" cx="227" cy="15" r="7.0"/><rect class="lo-cell" x="240" y="2" width="26" height="26"/><rect class="lo-press" x="243" y="5" width="20" height="20" rx="4"/><circle class="lo-off" cx="253" cy="15" r="7.0"/><rect class="lo-cell" x="266" y="2" width="26" height="26"/><rect class="lo-press" x="269" y="5" width="20" height="20" rx="4"/><circle class="lo-off" cx="279" cy="15" r="7.0"/><rect class="lo-cell" x="162" y="28" width="26" height="26"/><circle class="lo-off" cx="175" cy="41" r="7.0"/><rect class="lo-cell" x="188" y="28" width="26" height="26"/><circle class="lo-off" cx="201" cy="41" r="7.0"/><rect class="lo-cell" x="214" y="28" width="26" height="26"/><circle class="lo-off" cx="227" cy="41" r="7.0"/><rect class="lo-cell" x="240" y="28" width="26" height="26"/><circle class="lo-off" cx="253" cy="41" r="7.0"/><rect class="lo-cell" x="266" y="28" width="26" height="26"/><circle class="lo-off" cx="279" cy="41" r="7.0"/><rect class="lo-cell" x="162" y="54" width="26" height="26"/><circle class="lo-off" cx="175" cy="67" r="7.0"/><rect class="lo-cell" x="188" y="54" width="26" height="26"/><circle class="lo-off" cx="201" cy="67" r="7.0"/><rect class="lo-cell" x="214" y="54" width="26" height="26"/><circle class="lo-off" cx="227" cy="67" r="7.0"/><rect class="lo-cell" x="240" y="54" width="26" height="26"/><circle class="lo-off" cx="253" cy="67" r="7.0"/><rect class="lo-cell" x="266" y="54" width="26" height="26"/><circle class="lo-off" cx="279" cy="67" r="7.0"/><rect class="lo-cell" x="162" y="80" width="26" height="26"/><circle class="lo-off" cx="175" cy="93" r="7.0"/><rect class="lo-cell" x="188" y="80" width="26" height="26"/><circle class="lo-off" cx="201" cy="93" r="7.0"/><rect class="lo-cell" x="214" y="80" width="26" height="26"/><circle class="lo-off" cx="227" cy="93" r="7.0"/><rect class="lo-cell" x="240" y="80" width="26" height="26"/><circle class="lo-off" cx="253" cy="93" r="7.0"/><rect class="lo-cell" x="266" y="80" width="26" height="26"/><circle class="lo-off" cx="279" cy="93" r="7.0"/><rect class="lo-cell" x="162" y="106" width="26" height="26"/><circle class="lo-off" cx="175" cy="119" r="7.0"/><rect class="lo-cell" x="188" y="106" width="26" height="26"/><circle class="lo-off" cx="201" cy="119" r="7.0"/><rect class="lo-cell" x="214" y="106" width="26" height="26"/><circle class="lo-off" cx="227" cy="119" r="7.0"/><rect class="lo-cell" x="240" y="106" width="26" height="26"/><circle class="lo-off" cx="253" cy="119" r="7.0"/><rect class="lo-cell" x="266" y="106" width="26" height="26"/><circle class="lo-off" cx="279" cy="119" r="7.0"/><rect class="lo-frame" x="162" y="2" width="130" height="130"/><text class="lo-cap" x="227" y="152" text-anchor="middle" direction="rtl">בשורה 0</text><rect class="lo-cell" x="2" y="2" width="26" height="26"/><rect class="lo-press" x="5" y="5" width="20" height="20" rx="4"/><circle class="lo-off" cx="15" cy="15" r="7.0"/><rect class="lo-cell" x="28" y="2" width="26" height="26"/><rect class="lo-press" x="31" y="5" width="20" height="20" rx="4"/><circle class="lo-off" cx="41" cy="15" r="7.0"/><rect class="lo-cell" x="54" y="2" width="26" height="26"/><circle class="lo-off" cx="67" cy="15" r="7.0"/><rect class="lo-cell" x="80" y="2" width="26" height="26"/><rect class="lo-press" x="83" y="5" width="20" height="20" rx="4"/><circle class="lo-off" cx="93" cy="15" r="7.0"/><rect class="lo-cell" x="106" y="2" width="26" height="26"/><rect class="lo-press" x="109" y="5" width="20" height="20" rx="4"/><circle class="lo-off" cx="119" cy="15" r="7.0"/><rect class="lo-cell" x="2" y="28" width="26" height="26"/><rect class="lo-press" x="5" y="31" width="20" height="20" rx="4"/><circle class="lo-off" cx="15" cy="41" r="7.0"/><rect class="lo-cell" x="28" y="28" width="26" height="26"/><rect class="lo-press" x="31" y="31" width="20" height="20" rx="4"/><circle class="lo-off" cx="41" cy="41" r="7.0"/><rect class="lo-cell" x="54" y="28" width="26" height="26"/><circle class="lo-off" cx="67" cy="41" r="7.0"/><rect class="lo-cell" x="80" y="28" width="26" height="26"/><rect class="lo-press" x="83" y="31" width="20" height="20" rx="4"/><circle class="lo-off" cx="93" cy="41" r="7.0"/><rect class="lo-cell" x="106" y="28" width="26" height="26"/><rect class="lo-press" x="109" y="31" width="20" height="20" rx="4"/><circle class="lo-off" cx="119" cy="41" r="7.0"/><rect class="lo-cell" x="2" y="54" width="26" height="26"/><circle class="lo-off" cx="15" cy="67" r="7.0"/><rect class="lo-cell" x="28" y="54" width="26" height="26"/><circle class="lo-off" cx="41" cy="67" r="7.0"/><rect class="lo-cell" x="54" y="54" width="26" height="26"/><circle class="lo-off" cx="67" cy="67" r="7.0"/><rect class="lo-cell" x="80" y="54" width="26" height="26"/><circle class="lo-off" cx="93" cy="67" r="7.0"/><rect class="lo-cell" x="106" y="54" width="26" height="26"/><circle class="lo-off" cx="119" cy="67" r="7.0"/><rect class="lo-cell" x="2" y="80" width="26" height="26"/><rect class="lo-press" x="5" y="83" width="20" height="20" rx="4"/><circle class="lo-off" cx="15" cy="93" r="7.0"/><rect class="lo-cell" x="28" y="80" width="26" height="26"/><rect class="lo-press" x="31" y="83" width="20" height="20" rx="4"/><circle class="lo-off" cx="41" cy="93" r="7.0"/><rect class="lo-cell" x="54" y="80" width="26" height="26"/><circle class="lo-off" cx="67" cy="93" r="7.0"/><rect class="lo-cell" x="80" y="80" width="26" height="26"/><rect class="lo-press" x="83" y="83" width="20" height="20" rx="4"/><circle class="lo-off" cx="93" cy="93" r="7.0"/><rect class="lo-cell" x="106" y="80" width="26" height="26"/><rect class="lo-press" x="109" y="83" width="20" height="20" rx="4"/><circle class="lo-off" cx="119" cy="93" r="7.0"/><rect class="lo-cell" x="2" y="106" width="26" height="26"/><rect class="lo-press" x="5" y="109" width="20" height="20" rx="4"/><circle class="lo-off" cx="15" cy="119" r="7.0"/><rect class="lo-cell" x="28" y="106" width="26" height="26"/><rect class="lo-press" x="31" y="109" width="20" height="20" rx="4"/><circle class="lo-off" cx="41" cy="119" r="7.0"/><rect class="lo-cell" x="54" y="106" width="26" height="26"/><circle class="lo-off" cx="67" cy="119" r="7.0"/><rect class="lo-cell" x="80" y="106" width="26" height="26"/><rect class="lo-press" x="83" y="109" width="20" height="20" rx="4"/><circle class="lo-off" cx="93" cy="119" r="7.0"/><rect class="lo-cell" x="106" y="106" width="26" height="26"/><rect class="lo-press" x="109" y="109" width="20" height="20" rx="4"/><circle class="lo-off" cx="119" cy="119" r="7.0"/><rect class="lo-frame" x="2" y="2" width="130" height="130"/><text class="lo-cap" x="67" y="152" text-anchor="middle" direction="rtl">בשורות ובעמודות</text></svg>

    <span class="viz-legend"><span><i class="lo-key-press"></i>לחיצה בדפוס השקט</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שורה אחת :** הדטרמיננטה של \( P \) מעל GF(2) מקיימת \( d_k = d_{k-1} + d_{k-2} \) (פיתוח
       לפי השורה הראשונה), עם \( d_0 = d_1 = 1 \). לכן \( d_2 = 0 \), \( d_3 = 1 \), \( d_4 = 1 \),
       \( d_5 = 0 \), במחזור של 3, ו-\( d_n = 0 \) בדיוק כש-\( n \bmod 3 = 2 \).

    2. **הגרעין של P :** כש-\( n = 3m + 2 \), הווקטור \( u \) עם 1 בכל מקום שאינו 2 מודולו 3 הופך
       כל נורה פעמיים או אף פעם. הדרגה של \( P \) היא לפחות \( n - 1 \) : אם מוחקים את השורה הראשונה
       ואת העמודה האחרונה נשארת מטריצה משולשת עם אחדות באלכסון. לכן הגרעין הוא בדיוק 0 ו-\( u \).

    3. **הלוח :** הלחיצות הן מטריצה \( X \), והנורה \( (r', c') \) מתהפכת \( \sum_{r, c} P_{r' r} X_{r c} P_{c c'} \)
       פעמים, כלומר הלוח מתהפך ב-\( P X P \). זו מכפלת קרונקר \( P \otimes P \) שפועלת על \( X \).

    4. **הספירה :** אם \( P \) הפיכה, \( X = P^{-1} B P^{-1} \) הוא פתרון יחיד לכל לוח \( B \). אחרת
       סופרים את הפתרונות של \( P X P = 0 \) בהוכחה למטה, ומגיעים ל-\( 2n - 1 \).

    </div>

    בתיבה, לוח של 5 על 5 עם אלכסונים שבו דולקת רק הפינה. "הצגת פתרון" מראה דפוס שקט שמוכיח
    שאי אפשר לכבות אותה :

    <div class="explorer" data-kind="lightsout" data-mode="play" data-n="5" data-diag="1" data-lit="1"></div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="path_kernel, king_quiet" linenums="1" hl_lines="6 16 17"
        def path_kernel(n: int) -> int | None:
            """Part c: the presses on a line of n lights that change nothing, when a press flips a
            light and its two neighbours: 1 1 0 1 1 0 ... 1 1, only when n % 3 == 2."""
            if n % 3 != 2:
                return None
            return sum(1 << i for i in range(n) if i % 3 != 2)


        def king_quiet(n: int) -> list[int]:
            """Part c: 2n - 1 independent presses that change nothing on the n x n board with
            diagonals: u in one column, and u along one row (u the line's quiet pattern)."""
            u = path_kernel(n)
            if u is None:
                return []
            on = [i for i in range(n) if u >> i & 1]
            cols = [sum(1 << (r * n + j) for r in on) for j in range(n)]       # (1)!
            rows = [sum(1 << (i * n + c) for c in on) for i in range(1, n)]    # (2)!
            return cols + rows
        ```

        1. ‏\( u e_j^\top \) : הדפוס \( u \) בעמודה \( j \), לכל אחת מ-\( n \) העמודות.
        2. ‏\( e_i u^\top \) : הדפוס לאורך שורה \( i \). השורה 0 חסרה, כי סכום הדפוסים בשורות שבהן
           \( u \) הוא 1 שווה לסכום הדפוסים בעמודות כאלה : \( u u^\top \) נספר פעמיים.

    === "SystemVerilog"
        ```systemverilog title="king_quiet" linenums="1" hl_lines="6 7 12"
        // Part c: 2n - 1 independent presses that change nothing on the n x n board with diagonals.
        function automatic void king_quiet(int n, ref vec_t pats[$]);
          int on[$];
          pats.delete();
          if (n % 3 != 2) return;
          for (int i = 0; i < n; i++) if (i % 3 != 2) on.push_back(i);   // 1 1 0 1 1 0 ... 1 1
          for (int j = 0; j < n; j++) begin                               // (1)!
            vec_t v = '0;
            foreach (on[k]) v[on[k] * n + j] = 1;
            pats.push_back(v);
          end
          for (int i = 1; i < n; i++) begin                               // (2)!
            vec_t v = '0;
            foreach (on[k]) v[i * n + on[k]] = 1;
            pats.push_back(v);
          end
        endfunction
        ```

        1. הדפוס בכל אחת מ-\( n \) העמודות.
        2. הדפוס לאורך השורות 1 עד \( n - 1 \) : ‏\( 2n - 1 \) דפוסים בסך הכול.

    #### למה זה נכון { .sol-proof }

    **האפקט.** לחיצה על \( (r, c) \) הופכת את \( (r', c') \) כש-\( P_{r' r} = 1 \) וגם \( P_{c c'} = 1 \).
    לכן הלוח מתהפך ב-\( P X P \), ולוח \( B \) אפשר לכבות כש-\( P X P = B \).

    **‏P הפיכה.** אז \( X = P^{-1} B P^{-1} \) לכל \( B \) : פתרון אחד בדיוק.

    **‏P לא הפיכה.** נסמן \( Y = X P \). ‏\( P Y = 0 \) אומר שכל עמודה של \( Y \) היא 0 או \( u \),
    כלומר \( Y = u w^\top \) לאיזה \( w \). מצד שני, כל שורה של \( Y = X P \) היא צירוף של שורות
    \( P \), כלומר בתמונה של \( P \). ‏\( P \) סימטרית, ולכן התמונה שלה היא \( u^\perp \), הווקטורים
    עם \( w \cdot u = 0 \). השורות של \( u w^\top \) הן \( w \) או 0, ולכן \( Y \) אפשרי בדיוק כש-
    \( w \cdot u = 0 \) : ‏\( n - 1 \) ממדים. לכל \( Y \) כזה, הפתרונות של \( X P = Y \) הם פתרון אחד ועוד
    כל \( X \) עם \( X P = 0 \), כלומר עם כל השורות בגרעין, \( X = v u^\top \) : עוד \( n \) ממדים.
    ביחד \( (n - 1) + n = 2n - 1 \) משתנים חופשיים, כמו בקוד : ‏\( n \) דפוסים בעמודות ו-\( n - 1 \)
    לאורך שורות.

    **הטבלה.** הדירוג של סעיף א, עם אלכסונים, מאשר את זה לכל גודל עד 14 :

    <!-- gen 8 -->

    | ‏\( n \) | ‏\( n \bmod 3 \) | משתנים חופשיים עם אלכסונים | ‏\( 2n - 1 \) |
    |:-:|:-:|:-:|:-:|
    | 2 | 2 | 3 | 3 |
    | 3 | 0 | 0 | – |
    | 4 | 1 | 0 | – |
    | 5 | 2 | 9 | 9 |
    | 6 | 0 | 0 | – |
    | 7 | 1 | 0 | – |
    | 8 | 2 | 15 | 15 |
    | 9 | 0 | 0 | – |
    | 10 | 1 | 0 | – |
    | 11 | 2 | 21 | 21 |
    | 12 | 0 | 0 | – |
    | 13 | 1 | 0 | – |
    | 14 | 2 | 27 | 27 |

    <!-- /gen -->

    #### סיבוכיות { .sol-cost }

    התשובה לשאלה "פתיר תמיד?" היא בדיקה של \( n \bmod 3 \). בניית \( 2n - 1 \) הדפוסים לוקחת
    \( O(n^3) \) ביטים, ‏\( n \) ביטים לכל אחד מ-\( O(n) \) דפוסים, כל אחד במילה של \( n^2 \) ביטים.

---

### סעיף ד – אילו גדלים פתירים תמיד, בלי אלכסונים { #general }

בלי אלכסונים אין חוק פשוט כמו בסעיף ג : בלוחות 3, 6 ו-7 כל מצב פתיר, וב-4 וב-5 לא. הסבירו מה
קובע את מספר המשתנים החופשיים, כתבו קוד שמחשב אותו בלי מטריצה של \( n^2 \times n^2 \), ובדקו אותו
מול הדרגה. הוכיחו גם שבכל גודל אפשר לכבות את המצב שבו כל הנורות דולקות.

??? tip "רמז 1"
    כמו בסעיף ג, כתבו את הלחיצות כמטריצה \( X \). הפעם הלוח מתהפך ב-\( A X + X A + X \), כש-\( A \)
    המטריצה של השכנות בשורה אחת, עם אפסים באלכסון.

??? tip "רמז 2"
    הלחיצות השקטות הן \( X \) עם \( A X = X (A + I) \), כי מעל GF(2) פלוס ומינוס הם אותו דבר. מתי
    למשוואה \( A X = X B \) יש פתרון חוץ מ-0? חשבו על הפולינומים האופייניים של \( A \) ושל \( B \).

??? tip "רמז 3"
    למצב שבו הכול דולק : לכל וקטור \( x \) בגרעין, מה אומר \( x^\top A x = 0 \), כשבאלכסון של \( A \)
    יש רק אחדות?

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        נגדיר \( p_n(x) = \det(x I + A) \) מעל GF(2) : ‏\( p_0 = 1 \), \( p_1 = x \) ו-
        \( p_{k+1} = x p_k + p_{k-1} \). מספר המשתנים החופשיים בלוח \( n \times n \) הוא המעלה של
        \( \gcd(p_n(x), p_n(x + 1)) \) (‏Sutner). לכן לוח פתיר תמיד בדיוק כששני הפולינומים זרים. עד
        20 הגדלים שבהם לא כל מצב פתיר הם 4, 5, 9, 11, 14, 16, 17 ו-19. המצב שבו כל הנורות דולקות
        פתיר תמיד, בכל גודל ובכל גרף שבו לחיצה הופכת גם את הנורה עצמה.

    <!-- cost: זמן \( O(n^2) \) פעולות על מילים של \( n + 1 \) ביטים | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    בלי אלכסונים, השכנות למעלה ולמטה הן \( A X \), השכנות לימין ולשמאל הן \( X A \), והנורה עצמה
    היא \( X \). הלוח מתהפך ב-\( A X + X (A + I) \), ולחיצות שקטות הן פתרונות של \( A X = X (A + I) \).
    המשוואה מערבבת שתי מטריצות שונות, ולכן הכול תלוי במה שמשותף להן : הגורמים המשותפים של
    הפולינומים האופייניים \( p_n(x) \) ו-\( p_n(x + 1) \). הנה ארבעה גדלים :

    <!-- gen 9 -->

    | ‏\( n \) | ‏\( p_n(x) \) | ‏\( p_n(x + 1) \) | המחלק המשותף | המעלה |
    |:-:|:-:|:-:|:-:|:-:|
    | 3 | ‏<span dir="ltr">x³</span> | ‏<span dir="ltr">x³ + x² + x + 1</span> | ‏<span dir="ltr">1</span> | 0 |
    | 4 | ‏<span dir="ltr">x⁴ + x² + 1</span> | ‏<span dir="ltr">x⁴ + x² + 1</span> | ‏<span dir="ltr">x⁴ + x² + 1</span> | 4 |
    | 5 | ‏<span dir="ltr">x⁵ + x</span> | ‏<span dir="ltr">x⁵ + x⁴</span> | ‏<span dir="ltr">x² + x</span> | 2 |
    | 6 | ‏<span dir="ltr">x⁶ + x⁴ + 1</span> | ‏<span dir="ltr">x⁶ + x² + 1</span> | ‏<span dir="ltr">1</span> | 0 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הפולינום :** \( p_n \) בנוסחת הנסיגה, כמספר שלם שבו הביט \( k \) הוא המקדם של \( x^k \).
       הנסיגה היא פיתוח הדטרמיננטה של \( x I + A \) לפי השורה האחרונה.

    2. **ההזזה :** \( p_n(x + 1) \) בשיטת הורנר : \( q \leftarrow q \cdot (x + 1) + a_k \) מהמקדם
       הגבוה לנמוך. כפל ב-\( x + 1 \) הוא `q << 1 ^ q`.

    3. **המחלק המשותף :** אוקלידס מעל GF(2)[x] : שארית החלוקה היא XOR חוזר של המחלק המוזז, עד
       שהמעלה יורדת.

    4. **התשובה :** המעלה של המחלק המשותף היא מספר המשתנים החופשיים. 0 אומר שכל מצב פתיר.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="path_poly, poly_mod, plus_nullity" linenums="1" hl_lines="6 12 21 23"
        def path_poly(n: int) -> int:
            """Part d: det(xI + A) over GF(2) for the line of n lights (A: the neighbours on the
            line), bit k the coefficient of x^k. p0 = 1, p1 = x, p(k+1) = x p(k) + p(k-1)."""
            a, b = 1, 0b10
            for _ in range(n):
                a, b = b, (b << 1) ^ a
            return a


        def poly_mod(a: int, b: int) -> int:
            while a and a.bit_length() >= b.bit_length():
                a ^= b << (a.bit_length() - b.bit_length())   # (1)!
            return a


        def plus_nullity(n: int) -> int:
            """Part d: how many free variables the n x n board has (no diagonals):
            deg gcd(p(x), p(x + 1)) with p = path_poly(n)."""
            p, q = path_poly(n), 0
            for k in range(p.bit_length() - 1, -1, -1):       # (2)!
                q = (q << 1) ^ q ^ (p >> k & 1)
            while q:
                p, q = q, poly_mod(p, q)
            return p.bit_length() - 1
        ```

        1. מחסרים את המחלק כפול \( x \) בחזקה המתאימה : מעל GF(2) חיסור הוא XOR, והמקדם המוביל
           של כל פולינום הוא 1.
        2. הורנר עם \( x + 1 \) : ‏`q << 1 ^ q` הוא \( q \cdot x + q \).

    === "SystemVerilog"
        ```systemverilog title="path_poly, poly_mod, plus_nullity" linenums="1" hl_lines="11 19 26 28"
        // Part d: polynomials over GF(2) in a 64-bit word, bit k the coefficient of x^k.
        function automatic int deg(longint unsigned p);
          for (int k = 63; k >= 0; k--) if (p[k]) return k;
          return -1;
        endfunction

        // det(xI + A) of the line of n lights: p0 = 1, p1 = x, p(k+1) = x p(k) + p(k-1).
        function automatic longint unsigned path_poly(int n);
          longint unsigned a = 1, b = 2, t;
          repeat (n) begin
            t = (b << 1) ^ a;
            a = b;
            b = t;
          end
          return a;
        endfunction

        function automatic longint unsigned poly_mod(longint unsigned a, longint unsigned b);
          while (a != 0 && deg(a) >= deg(b)) a ^= b << (deg(a) - deg(b));  // (1)!
          return a;
        endfunction

        // The free variables of the n x n board without diagonals: deg gcd(p(x), p(x + 1)).
        function automatic int plus_nullity(int n);
          longint unsigned p = path_poly(n), q = 0, t;
          for (int k = deg(p); k >= 0; k--) q = (q << 1) ^ q ^ longint'(p[k]);   // (2)!
          while (q != 0) begin
            t = poly_mod(p, q);
            p = q;
            q = t;
          end
          return deg(p);
        endfunction
        ```

        1. אותה חלוקה עם שארית כמו ב-Python, על מילה של 64 ביטים : עד \( n = 62 \).
        2. הורנר עם \( x + 1 \). ‏`longint'(p[k])` מרחיב את הביט למילה.

    #### למה זה נכון { .sol-proof }

    **הפולינום.** פיתוח של \( \det(x I + A) \) לפי השורה האחרונה נותן \( x \) כפול הדטרמיננטה של
    \( n - 1 \) הנורות הראשונות, ועוד הדטרמיננטה של \( n - 2 \) הראשונות : זו הנסיגה. ‏\( (A + I) \)
    היא \( A \) ועוד \( I \), ולכן \( \det(x I + A + I) = p_n(x + 1) \).

    **כשהפולינומים זרים, אין דפוס שקט.** נניח \( A X = X B \) עם \( B = A + I \). אז \( A^k X = X B^k \)
    לכל \( k \), ולכל פולינום \( g \) : \( g(A) X = X g(B) \). אם \( \gcd(p_n(x), p_n(x + 1)) = 1 \),
    יש פולינומים \( s, t \) עם \( s(x) p_n(x) + t(x) q(x) = 1 \), כש-\( q(x) = p_n(x + 1) \) הוא
    הפולינום האופייני של \( B \). לפי קיילי-המילטון \( p_n(A) = 0 \) ו-\( q(B) = 0 \). מהראשון,
    \( X\, p_n(B) = p_n(A)\, X = 0 \). מהשני :

    \[
    \begin{aligned}
    I &= s(B)\, p_n(B) + t(B)\, q(B) \\
      &= s(B)\, p_n(B) ,
    \end{aligned}
    \]

    כלומר \( p_n(B) \) הפיכה, ומ-\( X\, p_n(B) = 0 \) נובע \( X = 0 \). אין לחיצה שקטה מלבד 0, וכל
    מצב פתיר.

    **בכיוון השני, והספירה.** ל-\( A \) יש וקטור \( e_1 \) שהחזקות שלו \( e_1, A e_1, \dots, A^{n-1} e_1 \)
    בלתי תלויות (ב-\( A^k e_1 \) האחד האחרון במקום \( k + 1 \)), ולכן הפולינום המינימלי של \( A \)
    הוא \( p_n \), וכך גם ל-\( B \) עם \( p_n(x + 1) \). לשתי מטריצות כאלה (ציקליות), ממד הפתרונות של
    \( A X = X B \) הוא בדיוק המעלה של המחלק המשותף של הפולינומים המינימליים שלהן (משפט של
    Frobenius). זה מה ש-`plus_nullity` מחשב, והבדיקות משוות אותו לדרגה של סעיף א לכל \( n \) עד 40 :

    <!-- gen 10 -->

    | ‏\( n \) | חופשיים, מהדרגה | המעלה של המחלק המשותף | כל מצב פתיר? | עם אלכסונים |
    |:-:|:-:|:-:|:-:|:-:|
    | 1 | 0 | 0 | כן | 0 |
    | 2 | 0 | 0 | כן | 3 |
    | 3 | 0 | 0 | כן | 0 |
    | 4 | 4 | 4 | **לא** | 0 |
    | 5 | 2 | 2 | **לא** | 9 |
    | 6 | 0 | 0 | כן | 0 |
    | 7 | 0 | 0 | כן | 0 |
    | 8 | 0 | 0 | כן | 15 |
    | 9 | 8 | 8 | **לא** | 0 |
    | 10 | 0 | 0 | כן | 0 |
    | 11 | 6 | 6 | **לא** | 21 |
    | 12 | 0 | 0 | כן | 0 |
    | 13 | 0 | 0 | כן | 0 |
    | 14 | 4 | 4 | **לא** | 27 |
    | 15 | 0 | 0 | כן | 0 |
    | 16 | 8 | 8 | **לא** | 0 |
    | 17 | 2 | 2 | **לא** | 33 |
    | 18 | 0 | 0 | כן | 0 |
    | 19 | 16 | 16 | **לא** | 0 |
    | 20 | 0 | 0 | כן | 39 |

    <!-- /gen -->

    **הכול דולק.** לכל \( x \) בגרעין של \( A \) (כאן \( A \) היא המטריצה של סעיף א, עם אחדות באלכסון) :
    \( 0 = x^\top A x = \sum_i A_{ii} x_i + 2 \sum_{i < j} A_{ij} x_i x_j = \sum_i x_i \) מעל GF(2), כי
    \( x_i^2 = x_i \) ו-2 הוא 0. כלומר הווקטור שכולו אחדות ניצב לגרעין, ולכן הוא בתמונה של המטריצה
    הסימטרית : המצב שבו הכול דולק פתיר. הנימוק משתמש רק בסימטריה ובאחדות באלכסון, ולכן הוא נכון
    בכל גרף שבו לחיצה הופכת את הנורה ואת השכנות שלה. גם ב-5 על 5, שבו רק רבע מהמצבים פתירים, הכול
    דולק פתיר, ב-15 לחיצות לפחות.

    #### סיבוכיות { .sol-cost }

    הנסיגה, ההזזה והמחלק המשותף עושים \( O(n) \) צעדים, כל אחד \( O(n) \) פעולות על ביטים, או פעולה
    אחת על מילה של \( n + 1 \) ביטים : זמן \( O(n^2) \) על ביטים, וזיכרון \( O(n) \). זה במקום
    \( O(n^6) \) של הדירוג.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : ללחוץ על הנורות הדולקות"
    לחיצה על נורה דולקת מכבה אותה, אבל מדליקה את השכנות שלה. בדוגמה של סעיף א, לחיצה על שלוש
    הנורות הדולקות משאירה 5 נורות דולקות במקום 3. הפתרון שם לא נוגע בשורה העליונה בכלל.

??? trap "מלכודת : דירוג מעל המספרים הממשיים"
    המשוואות הן מודולו 2, ולא מעל המספרים הממשיים. ב-4 על 4 הדרגה הממשית של המטריצה היא 14, ומעל
    GF(2) היא 12 : דירוג רגיל מבטיח פתרון עם שברים או מספרים שליליים, שאין להם משמעות כלחיצות, ומפספס
    שני משתנים חופשיים.

??? trap "מלכודת : רדיפת אורות עם אלכסונים"
    עם אלכסונים, לחיצה על \( (r + 1, c) \) הופכת בשורה \( r \) שלוש נורות, ולא רק את \( (r, c) \).
    אי אפשר לכבות שורה נורה אחרי נורה, והשיטה של סעיף ב לא עובדת כמו שהיא.

??? trap "מלכודת : לספור לחיצות במקום זוגיות"
    פתרון שלוחץ פעמיים על אותה נורה אף פעם לא המינימלי : שתי הלחיצות מבטלות זו את זו. פתרון הוא קבוצה,
    ומספר הלחיצות שלו הוא הגודל שלה.

??? followup "שאלות המשך"
    - **לוח מעגלי :** הקצה הימני מחובר לשמאלי והעליון לתחתון, ולכל נורה ארבע שכנות. מה קורה?

        ??? fu-answer "תשובה"
            אותו דירוג עם מסכות מעגליות. בלוח מעגלי של 3 על 3 יש 4 משתנים חופשיים, ב-4 על 4, 7 על 7
            ו-8 על 8 אין אף אחד, וב-5 על 5 ו-6 על 6 יש 8.

    - **מלבנים :** מה קובע את מספר המשתנים החופשיים בלוח של \( m \times n \)?

        ??? fu-answer "תשובה"
            אותו טיעון עם שתי שורות באורכים שונים : המעלה של \( \gcd(p_m(x), p_n(x + 1)) \). למשל
            בלוח של 2 על 3 יש 2 משתנים חופשיים, ובלוח של 3 על 4 אין.

    - **גדלים שגוררים גדלים :** אם בלוח של \( m \times m \) לא כל מצב פתיר, מה עוד ידוע?

        ??? fu-answer "תשובה"
            גם בכל לוח \( n \times n \) שבו \( m + 1 \) מחלק את \( n + 1 \) : ‏\( p_m \) מחלק את \( p_n \) אז,
            כמו במספרי פיבונאצ'י. מ-4 נובע ש-9, 14, 19 ו-24 בעייתיים, ומ-5 ש-11, 17 ו-23.

    - **הכי מעט לחיצות :** איך מוצאים את הפתרון הקצר ביותר כשיש משתנים חופשיים?

        ??? fu-answer "תשובה"
            עוברים על כל \( 2^f \) הצירופים של הדפוסים השקטים ומוסיפים אותם לפתרון אחד. ב-5 על 5, כשהכול
            דולק, 4 פתרונות, והקצר ביותר 15 לחיצות. בגרף כללי זו בעיה של פענוח קוד לינארי : מציאת
            מילת קוד במשקל מינימלי, בעיה קשה (NP-hard), ולכן אין כאן קיצור דרך כללי.
