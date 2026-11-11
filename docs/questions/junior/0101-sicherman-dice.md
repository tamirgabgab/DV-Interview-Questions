---
id: 101
title: קוביות Sicherman – מספרים אחרים על הפאות, אותה התפלגות של הסכום
level: junior
difficulty: medium
kind: math
tags: [probability, combinatorics, coverage, math, proof, python, systemverilog]
source: "קוביות Sicherman, על שם George Sicherman, שפרסם Martin Gardner ב-Scientific American ב-1978"
added: 2026-11-11
---

## השאלה

מטילים שתי קוביות הוגנות רגילות, עם המספרים 1 עד 6 על הפאות, ומחברים את שתי התוצאות. כל אחת
מ-36 ההטלות סבירה באותה מידה, והסכום הוא מ-2 עד 12. ההתפלגות שלו היא משולש : 7 מתקבל ב-6
הטלות, ו-2 ו-12 רק באחת.

<!-- gen 0 -->

<svg class="perf-chart" viewBox="0 0 420 196" style="max-width:26.25rem" role="img" aria-label="התפלגות הסכום של שתי קוביות רגילות : הסכומים 2 עד 12, ומספר ההטלות מתוך 36 שנותנות כל סכום, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1"><line class="grid" x1="34" x2="412" y1="166.0" y2="166.0"/><text class="tick" x="26" y="170.0" text-anchor="end">0</text><line class="grid" x1="34" x2="412" y1="116.7" y2="116.7"/><text class="tick" x="26" y="120.7" text-anchor="end">2</text><line class="grid" x1="34" x2="412" y1="67.3" y2="67.3"/><text class="tick" x="26" y="71.3" text-anchor="end">4</text><line class="grid" x1="34" x2="412" y1="18.0" y2="18.0"/><text class="tick" x="26" y="22.0" text-anchor="end">6</text><rect class="bar by-multiples" x="39.5" y="141.3" width="23.4" height="24.7" rx="2"><title>sum 2: 1 of 36</title></rect><text class="tick" x="51.2" y="136.3" text-anchor="middle">1</text><rect class="bar by-multiples" x="73.9" y="116.7" width="23.4" height="49.3" rx="2"><title>sum 3: 2 of 36</title></rect><text class="tick" x="85.5" y="111.7" text-anchor="middle">2</text><rect class="bar by-multiples" x="108.2" y="92.0" width="23.4" height="74.0" rx="2"><title>sum 4: 3 of 36</title></rect><text class="tick" x="119.9" y="87.0" text-anchor="middle">3</text><rect class="bar by-multiples" x="142.6" y="67.3" width="23.4" height="98.7" rx="2"><title>sum 5: 4 of 36</title></rect><text class="tick" x="154.3" y="62.3" text-anchor="middle">4</text><rect class="bar by-multiples" x="177.0" y="42.7" width="23.4" height="123.3" rx="2"><title>sum 6: 5 of 36</title></rect><text class="tick" x="188.6" y="37.7" text-anchor="middle">5</text><rect class="bar by-multiples" x="211.3" y="18.0" width="23.4" height="148.0" rx="2"><title>sum 7: 6 of 36</title></rect><text class="tick" x="223.0" y="13.0" text-anchor="middle">6</text><rect class="bar by-multiples" x="245.7" y="42.7" width="23.4" height="123.3" rx="2"><title>sum 8: 5 of 36</title></rect><text class="tick" x="257.4" y="37.7" text-anchor="middle">5</text><rect class="bar by-multiples" x="280.0" y="67.3" width="23.4" height="98.7" rx="2"><title>sum 9: 4 of 36</title></rect><text class="tick" x="291.7" y="62.3" text-anchor="middle">4</text><rect class="bar by-multiples" x="314.4" y="92.0" width="23.4" height="74.0" rx="2"><title>sum 10: 3 of 36</title></rect><text class="tick" x="326.1" y="87.0" text-anchor="middle">3</text><rect class="bar by-multiples" x="348.8" y="116.7" width="23.4" height="49.3" rx="2"><title>sum 11: 2 of 36</title></rect><text class="tick" x="360.5" y="111.7" text-anchor="middle">2</text><rect class="bar by-multiples" x="383.1" y="141.3" width="23.4" height="24.7" rx="2"><title>sum 12: 1 of 36</title></rect><text class="tick" x="394.8" y="136.3" text-anchor="middle">1</text><text class="tick" x="51.2" y="184" text-anchor="middle">2</text><text class="tick" x="85.5" y="184" text-anchor="middle">3</text><text class="tick" x="119.9" y="184" text-anchor="middle">4</text><text class="tick" x="154.3" y="184" text-anchor="middle">5</text><text class="tick" x="188.6" y="184" text-anchor="middle">6</text><text class="tick" x="223.0" y="184" text-anchor="middle">7</text><text class="tick" x="257.4" y="184" text-anchor="middle">8</text><text class="tick" x="291.7" y="184" text-anchor="middle">9</text><text class="tick" x="326.1" y="184" text-anchor="middle">10</text><text class="tick" x="360.5" y="184" text-anchor="middle">11</text><text class="tick" x="394.8" y="184" text-anchor="middle">12</text><line class="axis" x1="34" x2="412" y1="166" y2="166"/></svg>

<!-- /gen -->

עכשיו מוחקים את המספרים וכותבים על הפאות של שתי הקוביות מספרים אחרים. כל קובייה נשארת קובייה
הוגנת עם שש פאות, ועל כל פאה מספר שלם חיובי. מותר לחזור על מספר באותה קובייה, ומותר מספר גדול
מ-6. אפשר לבחור את המספרים כך שהסכום יתפלג בדיוק כמו קודם, בלי ששתי הקוביות יהיו הרגילות? השאלה
בשלושה סעיפים :

1. **שש פאות :** מצאו זוג כזה, והוכיחו שהוא הזוג היחיד מלבד הרגיל.
2. **גם 0 על פאה :** מותר גם 0, כלומר מספרים שלמים מ-0 ומעלה. כמה זוגות יש עכשיו, ומה הקשר
   ביניהם?
3. **מספר פאות כללי :** שתי קוביות של \( n \) פאות, וההתפלגות של הסכום של שתי קוביות רגילות של
   \( n \) פאות. לאילו \( n \) יש זוג אחר, וכמה זוגות יש?

??? interviewer "מה המראיין בודק"
    - **ניסוי וטעייה מסודר :** האם המועמד מתחיל מהסכומים הנדירים, 2 ו-12, ומסיק מהם משהו על
      הפאות, או מנחש מספרים.
    - **כלי מתאים :** האם הוא מוצא דרך לחשב את ההתפלגות של סכום כפעולה אחת שאפשר גם לפרק, ולא
      רק למלא טבלאות.
    - **הוכחה שאין עוד :** למצוא זוג זה חצי מהעבודה. האם הוא מראה למה כל אפשרות אחרת נשללת.
    - **עין של אימות :** האם הוא רואה מה בדיקה שמסתכלת רק על הסכום לא יכולה לתפוס.

---

### סעיף א – שש פאות

מצאו שתי קוביות של שש פאות, עם מספרים שלמים חיוביים, שאינן הזוג הרגיל, והסכום שלהן מתפלג כמו
הסכום של שתי קוביות רגילות. הוכיחו שאין זוג נוסף. כתבו קוד שבודק אם לזוג נתון יש את ההתפלגות
הזו, וקוד שמוצא את כל הזוגות.

??? tip "רמז 1"
    הסכום 2 מתקבל רק בהטלה אחת. כמה פעמים יכול להופיע 1 על כל קובייה? ומה אומר הסכום 3, שמתקבל
    בשתי הטלות?

??? tip "רמז 2"
    כתבו קובייה כפולינום : לכל פאה \( f \) מחברים \( x^f \). הקובייה הרגילה היא
    \( x + x^2 + \dots + x^6 \). מה סופרים המקדמים של המכפלה של שני פולינומים כאלה?

??? tip "רמז 3"
    פרקו את \( x + x^2 + \dots + x^6 \) לגורמים שאי אפשר לפרק עוד. כמה מכל גורם כל קובייה חייבת
    לקבל? הציבו \( x = 0 \) ו-\( x = 1 \).

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **‏\( \{1, 2, 2, 3, 3, 4\} \) ו-\( \{1, 3, 4, 5, 6, 8\} \)**, וזה הזוג היחיד מלבד הרגיל.
        כותבים קובייה כפולינום, \( x^f \) לכל פאה, והסכום של שתי קוביות הוא המכפלה של
        הפולינומים. הקובייה הרגילה מתפרקת ל-\( x(1 + x)(1 + x + x^2)(1 - x + x^2) \), וכל קובייה
        חייבת לקבל \( x \), ‏\( 1 + x \) ו-\( 1 + x + x^2 \) אחד. נשאר לחלק רק את שני הגורמים
        \( 1 - x + x^2 \) : אחד לכל קובייה נותן את הרגילות, ושניהם לאותה קובייה נותנים את קוביות
        Sicherman.

    <!-- cost: זמן \( O(\binom{3n-2}{n} \, n^2) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **ניסוי וטעייה.** טבלה של 6 על 6, שורה לכל פאה של קובייה A ועמודה לכל פאה של קובייה B,
    מראה את כל 36 ההטלות, ובכל תא את הסכום. בקוביות הרגילות כל סכום יושב על אלכסון אחד. בזוג
    שמחפשים אותם 36 תאים מסודרים אחרת, אבל כל סכום מופיע אותו מספר פעמים :

    <!-- gen 1 -->

    <div class="sc-pair"><figure class="sc-fig"><svg class="figure sc-sums" viewBox="0 0 200 200" style="max-width:12.5rem" role="img" aria-label="טבלת הסכומים של שתי קוביות רגילות : שורה לכל פאה של A, עמודה לכל פאה של B. כל סכום יושב על אלכסון אחד, 7 על האלכסון הארוך"><text class="sc-corner" x="16.0" y="20.0" text-anchor="middle">+</text><text class="sc-face" x="44.0" y="20.0" text-anchor="middle">1</text><text class="sc-face" x="72.0" y="20.0" text-anchor="middle">2</text><text class="sc-face" x="100.0" y="20.0" text-anchor="middle">3</text><text class="sc-face" x="128.0" y="20.0" text-anchor="middle">4</text><text class="sc-face" x="156.0" y="20.0" text-anchor="middle">5</text><text class="sc-face" x="184.0" y="20.0" text-anchor="middle">6</text><text class="sc-face" x="16.0" y="48.0" text-anchor="middle">1</text><g class="sc-cell sc-lo sc-f1"><title>1 + 1 = 2</title><rect x="31" y="31" width="26" height="26" rx="3"/><text x="44.0" y="48.0" text-anchor="middle">2</text></g><g class="sc-cell sc-lo sc-f2"><title>1 + 2 = 3</title><rect x="59" y="31" width="26" height="26" rx="3"/><text x="72.0" y="48.0" text-anchor="middle">3</text></g><g class="sc-cell sc-lo sc-f3"><title>1 + 3 = 4</title><rect x="87" y="31" width="26" height="26" rx="3"/><text x="100.0" y="48.0" text-anchor="middle">4</text></g><g class="sc-cell sc-lo sc-f4"><title>1 + 4 = 5</title><rect x="115" y="31" width="26" height="26" rx="3"/><text x="128.0" y="48.0" text-anchor="middle">5</text></g><g class="sc-cell sc-lo sc-f5"><title>1 + 5 = 6</title><rect x="143" y="31" width="26" height="26" rx="3"/><text x="156.0" y="48.0" text-anchor="middle">6</text></g><g class="sc-cell sc-mid sc-f6"><title>1 + 6 = 7</title><rect x="171" y="31" width="26" height="26" rx="3"/><text x="184.0" y="48.0" text-anchor="middle">7</text></g><text class="sc-face" x="16.0" y="76.0" text-anchor="middle">2</text><g class="sc-cell sc-lo sc-f2"><title>2 + 1 = 3</title><rect x="31" y="59" width="26" height="26" rx="3"/><text x="44.0" y="76.0" text-anchor="middle">3</text></g><g class="sc-cell sc-lo sc-f3"><title>2 + 2 = 4</title><rect x="59" y="59" width="26" height="26" rx="3"/><text x="72.0" y="76.0" text-anchor="middle">4</text></g><g class="sc-cell sc-lo sc-f4"><title>2 + 3 = 5</title><rect x="87" y="59" width="26" height="26" rx="3"/><text x="100.0" y="76.0" text-anchor="middle">5</text></g><g class="sc-cell sc-lo sc-f5"><title>2 + 4 = 6</title><rect x="115" y="59" width="26" height="26" rx="3"/><text x="128.0" y="76.0" text-anchor="middle">6</text></g><g class="sc-cell sc-mid sc-f6"><title>2 + 5 = 7</title><rect x="143" y="59" width="26" height="26" rx="3"/><text x="156.0" y="76.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f5"><title>2 + 6 = 8</title><rect x="171" y="59" width="26" height="26" rx="3"/><text x="184.0" y="76.0" text-anchor="middle">8</text></g><text class="sc-face" x="16.0" y="104.0" text-anchor="middle">3</text><g class="sc-cell sc-lo sc-f3"><title>3 + 1 = 4</title><rect x="31" y="87" width="26" height="26" rx="3"/><text x="44.0" y="104.0" text-anchor="middle">4</text></g><g class="sc-cell sc-lo sc-f4"><title>3 + 2 = 5</title><rect x="59" y="87" width="26" height="26" rx="3"/><text x="72.0" y="104.0" text-anchor="middle">5</text></g><g class="sc-cell sc-lo sc-f5"><title>3 + 3 = 6</title><rect x="87" y="87" width="26" height="26" rx="3"/><text x="100.0" y="104.0" text-anchor="middle">6</text></g><g class="sc-cell sc-mid sc-f6"><title>3 + 4 = 7</title><rect x="115" y="87" width="26" height="26" rx="3"/><text x="128.0" y="104.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f5"><title>3 + 5 = 8</title><rect x="143" y="87" width="26" height="26" rx="3"/><text x="156.0" y="104.0" text-anchor="middle">8</text></g><g class="sc-cell sc-hi sc-f4"><title>3 + 6 = 9</title><rect x="171" y="87" width="26" height="26" rx="3"/><text x="184.0" y="104.0" text-anchor="middle">9</text></g><text class="sc-face" x="16.0" y="132.0" text-anchor="middle">4</text><g class="sc-cell sc-lo sc-f4"><title>4 + 1 = 5</title><rect x="31" y="115" width="26" height="26" rx="3"/><text x="44.0" y="132.0" text-anchor="middle">5</text></g><g class="sc-cell sc-lo sc-f5"><title>4 + 2 = 6</title><rect x="59" y="115" width="26" height="26" rx="3"/><text x="72.0" y="132.0" text-anchor="middle">6</text></g><g class="sc-cell sc-mid sc-f6"><title>4 + 3 = 7</title><rect x="87" y="115" width="26" height="26" rx="3"/><text x="100.0" y="132.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f5"><title>4 + 4 = 8</title><rect x="115" y="115" width="26" height="26" rx="3"/><text x="128.0" y="132.0" text-anchor="middle">8</text></g><g class="sc-cell sc-hi sc-f4"><title>4 + 5 = 9</title><rect x="143" y="115" width="26" height="26" rx="3"/><text x="156.0" y="132.0" text-anchor="middle">9</text></g><g class="sc-cell sc-hi sc-f3"><title>4 + 6 = 10</title><rect x="171" y="115" width="26" height="26" rx="3"/><text x="184.0" y="132.0" text-anchor="middle">10</text></g><text class="sc-face" x="16.0" y="160.0" text-anchor="middle">5</text><g class="sc-cell sc-lo sc-f5"><title>5 + 1 = 6</title><rect x="31" y="143" width="26" height="26" rx="3"/><text x="44.0" y="160.0" text-anchor="middle">6</text></g><g class="sc-cell sc-mid sc-f6"><title>5 + 2 = 7</title><rect x="59" y="143" width="26" height="26" rx="3"/><text x="72.0" y="160.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f5"><title>5 + 3 = 8</title><rect x="87" y="143" width="26" height="26" rx="3"/><text x="100.0" y="160.0" text-anchor="middle">8</text></g><g class="sc-cell sc-hi sc-f4"><title>5 + 4 = 9</title><rect x="115" y="143" width="26" height="26" rx="3"/><text x="128.0" y="160.0" text-anchor="middle">9</text></g><g class="sc-cell sc-hi sc-f3"><title>5 + 5 = 10</title><rect x="143" y="143" width="26" height="26" rx="3"/><text x="156.0" y="160.0" text-anchor="middle">10</text></g><g class="sc-cell sc-hi sc-f2"><title>5 + 6 = 11</title><rect x="171" y="143" width="26" height="26" rx="3"/><text x="184.0" y="160.0" text-anchor="middle">11</text></g><text class="sc-face" x="16.0" y="188.0" text-anchor="middle">6</text><g class="sc-cell sc-mid sc-f6"><title>6 + 1 = 7</title><rect x="31" y="171" width="26" height="26" rx="3"/><text x="44.0" y="188.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f5"><title>6 + 2 = 8</title><rect x="59" y="171" width="26" height="26" rx="3"/><text x="72.0" y="188.0" text-anchor="middle">8</text></g><g class="sc-cell sc-hi sc-f4"><title>6 + 3 = 9</title><rect x="87" y="171" width="26" height="26" rx="3"/><text x="100.0" y="188.0" text-anchor="middle">9</text></g><g class="sc-cell sc-hi sc-f3"><title>6 + 4 = 10</title><rect x="115" y="171" width="26" height="26" rx="3"/><text x="128.0" y="188.0" text-anchor="middle">10</text></g><g class="sc-cell sc-hi sc-f2"><title>6 + 5 = 11</title><rect x="143" y="171" width="26" height="26" rx="3"/><text x="156.0" y="188.0" text-anchor="middle">11</text></g><g class="sc-cell sc-hi sc-f1"><title>6 + 6 = 12</title><rect x="171" y="171" width="26" height="26" rx="3"/><text x="184.0" y="188.0" text-anchor="middle">12</text></g></svg><figcaption>קוביות רגילות</figcaption></figure><figure class="sc-fig"><svg class="figure sc-sums" viewBox="0 0 200 200" style="max-width:12.5rem" role="img" aria-label="טבלת הסכומים של קוביות Sicherman, A עם הפאות 1, 2, 2, 3, 3, 4 ו-B עם 1, 3, 4, 5, 6, 8 : אותם 36 סכומים, מפוזרים אחרת, ושוב 7 שש פעמים"><text class="sc-corner" x="16.0" y="20.0" text-anchor="middle">+</text><text class="sc-face" x="44.0" y="20.0" text-anchor="middle">1</text><text class="sc-face" x="72.0" y="20.0" text-anchor="middle">3</text><text class="sc-face" x="100.0" y="20.0" text-anchor="middle">4</text><text class="sc-face" x="128.0" y="20.0" text-anchor="middle">5</text><text class="sc-face" x="156.0" y="20.0" text-anchor="middle">6</text><text class="sc-face" x="184.0" y="20.0" text-anchor="middle">8</text><text class="sc-face" x="16.0" y="48.0" text-anchor="middle">1</text><g class="sc-cell sc-lo sc-f1"><title>1 + 1 = 2</title><rect x="31" y="31" width="26" height="26" rx="3"/><text x="44.0" y="48.0" text-anchor="middle">2</text></g><g class="sc-cell sc-lo sc-f3"><title>1 + 3 = 4</title><rect x="59" y="31" width="26" height="26" rx="3"/><text x="72.0" y="48.0" text-anchor="middle">4</text></g><g class="sc-cell sc-lo sc-f4"><title>1 + 4 = 5</title><rect x="87" y="31" width="26" height="26" rx="3"/><text x="100.0" y="48.0" text-anchor="middle">5</text></g><g class="sc-cell sc-lo sc-f5"><title>1 + 5 = 6</title><rect x="115" y="31" width="26" height="26" rx="3"/><text x="128.0" y="48.0" text-anchor="middle">6</text></g><g class="sc-cell sc-mid sc-f6"><title>1 + 6 = 7</title><rect x="143" y="31" width="26" height="26" rx="3"/><text x="156.0" y="48.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f4"><title>1 + 8 = 9</title><rect x="171" y="31" width="26" height="26" rx="3"/><text x="184.0" y="48.0" text-anchor="middle">9</text></g><text class="sc-face" x="16.0" y="76.0" text-anchor="middle">2</text><g class="sc-cell sc-lo sc-f2"><title>2 + 1 = 3</title><rect x="31" y="59" width="26" height="26" rx="3"/><text x="44.0" y="76.0" text-anchor="middle">3</text></g><g class="sc-cell sc-lo sc-f4"><title>2 + 3 = 5</title><rect x="59" y="59" width="26" height="26" rx="3"/><text x="72.0" y="76.0" text-anchor="middle">5</text></g><g class="sc-cell sc-lo sc-f5"><title>2 + 4 = 6</title><rect x="87" y="59" width="26" height="26" rx="3"/><text x="100.0" y="76.0" text-anchor="middle">6</text></g><g class="sc-cell sc-mid sc-f6"><title>2 + 5 = 7</title><rect x="115" y="59" width="26" height="26" rx="3"/><text x="128.0" y="76.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f5"><title>2 + 6 = 8</title><rect x="143" y="59" width="26" height="26" rx="3"/><text x="156.0" y="76.0" text-anchor="middle">8</text></g><g class="sc-cell sc-hi sc-f3"><title>2 + 8 = 10</title><rect x="171" y="59" width="26" height="26" rx="3"/><text x="184.0" y="76.0" text-anchor="middle">10</text></g><text class="sc-face" x="16.0" y="104.0" text-anchor="middle">2</text><g class="sc-cell sc-lo sc-f2"><title>2 + 1 = 3</title><rect x="31" y="87" width="26" height="26" rx="3"/><text x="44.0" y="104.0" text-anchor="middle">3</text></g><g class="sc-cell sc-lo sc-f4"><title>2 + 3 = 5</title><rect x="59" y="87" width="26" height="26" rx="3"/><text x="72.0" y="104.0" text-anchor="middle">5</text></g><g class="sc-cell sc-lo sc-f5"><title>2 + 4 = 6</title><rect x="87" y="87" width="26" height="26" rx="3"/><text x="100.0" y="104.0" text-anchor="middle">6</text></g><g class="sc-cell sc-mid sc-f6"><title>2 + 5 = 7</title><rect x="115" y="87" width="26" height="26" rx="3"/><text x="128.0" y="104.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f5"><title>2 + 6 = 8</title><rect x="143" y="87" width="26" height="26" rx="3"/><text x="156.0" y="104.0" text-anchor="middle">8</text></g><g class="sc-cell sc-hi sc-f3"><title>2 + 8 = 10</title><rect x="171" y="87" width="26" height="26" rx="3"/><text x="184.0" y="104.0" text-anchor="middle">10</text></g><text class="sc-face" x="16.0" y="132.0" text-anchor="middle">3</text><g class="sc-cell sc-lo sc-f3"><title>3 + 1 = 4</title><rect x="31" y="115" width="26" height="26" rx="3"/><text x="44.0" y="132.0" text-anchor="middle">4</text></g><g class="sc-cell sc-lo sc-f5"><title>3 + 3 = 6</title><rect x="59" y="115" width="26" height="26" rx="3"/><text x="72.0" y="132.0" text-anchor="middle">6</text></g><g class="sc-cell sc-mid sc-f6"><title>3 + 4 = 7</title><rect x="87" y="115" width="26" height="26" rx="3"/><text x="100.0" y="132.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f5"><title>3 + 5 = 8</title><rect x="115" y="115" width="26" height="26" rx="3"/><text x="128.0" y="132.0" text-anchor="middle">8</text></g><g class="sc-cell sc-hi sc-f4"><title>3 + 6 = 9</title><rect x="143" y="115" width="26" height="26" rx="3"/><text x="156.0" y="132.0" text-anchor="middle">9</text></g><g class="sc-cell sc-hi sc-f2"><title>3 + 8 = 11</title><rect x="171" y="115" width="26" height="26" rx="3"/><text x="184.0" y="132.0" text-anchor="middle">11</text></g><text class="sc-face" x="16.0" y="160.0" text-anchor="middle">3</text><g class="sc-cell sc-lo sc-f3"><title>3 + 1 = 4</title><rect x="31" y="143" width="26" height="26" rx="3"/><text x="44.0" y="160.0" text-anchor="middle">4</text></g><g class="sc-cell sc-lo sc-f5"><title>3 + 3 = 6</title><rect x="59" y="143" width="26" height="26" rx="3"/><text x="72.0" y="160.0" text-anchor="middle">6</text></g><g class="sc-cell sc-mid sc-f6"><title>3 + 4 = 7</title><rect x="87" y="143" width="26" height="26" rx="3"/><text x="100.0" y="160.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f5"><title>3 + 5 = 8</title><rect x="115" y="143" width="26" height="26" rx="3"/><text x="128.0" y="160.0" text-anchor="middle">8</text></g><g class="sc-cell sc-hi sc-f4"><title>3 + 6 = 9</title><rect x="143" y="143" width="26" height="26" rx="3"/><text x="156.0" y="160.0" text-anchor="middle">9</text></g><g class="sc-cell sc-hi sc-f2"><title>3 + 8 = 11</title><rect x="171" y="143" width="26" height="26" rx="3"/><text x="184.0" y="160.0" text-anchor="middle">11</text></g><text class="sc-face" x="16.0" y="188.0" text-anchor="middle">4</text><g class="sc-cell sc-lo sc-f4"><title>4 + 1 = 5</title><rect x="31" y="171" width="26" height="26" rx="3"/><text x="44.0" y="188.0" text-anchor="middle">5</text></g><g class="sc-cell sc-mid sc-f6"><title>4 + 3 = 7</title><rect x="59" y="171" width="26" height="26" rx="3"/><text x="72.0" y="188.0" text-anchor="middle">7</text></g><g class="sc-cell sc-hi sc-f5"><title>4 + 4 = 8</title><rect x="87" y="171" width="26" height="26" rx="3"/><text x="100.0" y="188.0" text-anchor="middle">8</text></g><g class="sc-cell sc-hi sc-f4"><title>4 + 5 = 9</title><rect x="115" y="171" width="26" height="26" rx="3"/><text x="128.0" y="188.0" text-anchor="middle">9</text></g><g class="sc-cell sc-hi sc-f3"><title>4 + 6 = 10</title><rect x="143" y="171" width="26" height="26" rx="3"/><text x="156.0" y="188.0" text-anchor="middle">10</text></g><g class="sc-cell sc-hi sc-f1"><title>4 + 8 = 12</title><rect x="171" y="171" width="26" height="26" rx="3"/><text x="184.0" y="188.0" text-anchor="middle">12</text></g></svg><figcaption>קוביות Sicherman : ‏<span dir="ltr">A = {1, 2, 2, 3, 3, 4}</span> ו-<span dir="ltr">B = {1, 3, 4, 5, 6, 8}</span></figcaption></figure></div>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="sc-key-lo"></i>סכום קטן מ-7</span><span><i class="sc-key-mid"></i>הסכום 7</span><span><i class="sc-key-hi"></i>סכום גדול מ-7</span><span>ככל שהסכום נפוץ יותר, הצבע עמוק יותר</span></span>

    <!-- /gen -->

    מהסכומים הנדירים אפשר להסיק הרבה :

    - **הסכום 2 :** הוא מתקבל רק מ-1 ועוד 1, ורק בהטלה אחת. לכן על כל קובייה יש 1, ובדיוק
      פעם אחת. קובייה עם 1 פעמיים, למשל \( \{1, 1, 2, 3, 4, 5\} \), נותנת את הסכום 2 בשתי
      הטלות.
    - **הסכום 3 :** הוא מתקבל בשתי הטלות, 1 ועוד 2 או 2 ועוד 1. יש 1 אחד בכל קובייה, ולכן יש
      בסך הכול שני 2 : שניים על קובייה אחת, או אחד על כל אחת.
    - **הסכום 12 :** הוא מתקבל בהטלה אחת, ולכן לכל קובייה יש פאה גבוהה ביותר אחת, והסכום של
      שתי הגבוהות הוא 12.

    אפשר להמשיך כך סכום אחרי סכום, אבל כל צעד מתפצל לכמה מקרים, וקשה להיות בטוחים שאף מקרה לא
    נשכח. צריך כלי שעושה את כל החשבון הזה בבת אחת.

    **קובייה כפולינום.** כותבים קובייה כפולינום : לכל פאה \( f \) איבר \( x^f \). הקובייה הרגילה
    היא \( P(x) = x + x^2 + x^3 + x^4 + x^5 + x^6 \). כשכופלים פולינומים של שתי קוביות, כל זוג
    איברים, אחד מכל קובייה, נותן \( x^a \cdot x^b = x^{a+b} \) : המעריכים מתחברים, כמו הפאות
    בהטלה. לכן המקדם של \( x^s \) במכפלה הוא מספר ההטלות שנותנות את הסכום \( s \). דוגמה קטנה,
    קובייה עם הפאות 1 ו-2 וקובייה של שלוש פאות עם 1, 1 ו-3 :

    \[
    (x + x^2)(2x + x^3) = 2x^2 + 2x^3 + x^4 + x^5
    \]

    הסכום 2 מתקבל בשתי הטלות, 1 עם כל אחד משני ה-1, גם 3 בשתיים, ו-4 ו-5 באחת. סכום המקדמים,
    6, הוא מספר ההטלות, \( 2 \cdot 3 \). מכאן שהשאלה היא שאלה על פולינומים : מחפשים \( A(x) \)
    ו-\( B(x) \) עם מקדמים שלמים לא שליליים, שהמכפלה שלהם היא \( P(x)^2 \), הפולינום של שתי
    קוביות רגילות.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **פירוק :** ‏\( P(x) = x(1 + x)(1 + x + x^2)(1 - x + x^2) \), וכל גורם כאן לא מתפרק
       יותר. ב-\( P(x)^2 \) כל אחד מארבעת הגורמים מופיע פעמיים, ו-\( A(x) \) ו-\( B(x) \)
       מחלקים ביניהם את שמונת הגורמים.
    2. **אין פאה 0 :** ‏\( A(0) \) הוא מספר הפאות של A שעליהן 0, כלומר 0. מבין הגורמים רק \( x \)
       מתאפס ב-0, ולכן כל קובייה מקבלת לפחות \( x \) אחד. יש שניים : אחד לכל קובייה.
    3. **שש פאות :** ‏\( A(1) \) הוא מספר הפאות, 6. ב-\( x = 1 \) הגורמים שווים ל-1, 2, 3 ו-1,
       ולכן \( A(1) = 2^i \cdot 3^j \), כש-\( i \) ו-\( j \) הם מספר הגורמים \( 1 + x \)
       ו-\( 1 + x + x^2 \) ש-A קיבלה. ‏\( 2^i \cdot 3^j = 6 \) רק כש-\( i = j = 1 \).
    4. **הגורם החופשי :** ‏\( 1 - x + x^2 \) שווה 1 ב-\( x = 1 \), ולכן הוא לא משנה את מספר
       הפאות. אחד לכל קובייה נותן \( A = B = P \), הקוביות הרגילות. שניהם ל-B נותנים
       \( A(x) = x + 2x^2 + 2x^3 + x^4 \), ו-\( B(x) \), שהוא \( A(x) \) כפול
       \( (1 - x + x^2)^2 \), הוא \( x + x^3 + x^4 + x^5 + x^6 + x^8 \).
    5. **בדיקה :** כל המקדמים לא שליליים, ולכן אלה קוביות : A עם הפאות
       \( \{1, 2, 2, 3, 3, 4\} \) ו-B עם \( \{1, 3, 4, 5, 6, 8\} \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="dice_pairs" linenums="1" hl_lines="17 57 58"
        from itertools import combinations_with_replacement


        def die_poly(faces):
            """The die as a polynomial, its coefficients from x^0 up: c[f] is the number of
            faces that show f."""
            c = [0] * (max(faces) + 1)
            for f in faces:
                c[f] += 1
            return c


        def poly_mul(p, q):
            r = [0] * (len(p) + len(q) - 1)
            for i, a in enumerate(p):
                for j, b in enumerate(q):
                    r[i + j] += a * b                            # (1)!
            return r


        def faces_of(c):
            """The faces of a die polynomial, from the lowest up."""
            return tuple(f for f, k in enumerate(c) for _ in range(k))


        def sum_counts(a, b):
            """counts[s]: how many of the rolls of the dice a and b give the sum s."""
            return poly_mul(die_poly(a), die_poly(b))


        def same_sum(a, b):
            """The sum of a and b is distributed as the sum of two standard dice."""
            std = range(1, len(a) + 1)
            return len(a) == len(b) and sum_counts(a, b) == sum_counts(std, std)


        def poly_div(p, q):
            """p / q when q divides p with whole coefficients, else None (long division)."""
            p, out = list(p), [0] * max(0, len(p) - len(q) + 1)
            for i in reversed(range(len(out))):
                c, r = divmod(p[i + len(q) - 1], q[-1])
                if r:
                    return None
                out[i] = c
                for j, v in enumerate(q):
                    p[i + j] -= c * v
            return out if out and not any(p) else None


        def dice_pairs(n, low=1):
            """Every pair of n-sided dice, faces whole numbers from low up, whose sum is
            distributed as the sum of two standard dice; each pair once."""
            std = range(1, n + 1)
            target = sum_counts(std, std)
            pairs = []
            for a in combinations_with_replacement(range(low, 2 * n + 1 - low), n):   # (2)!
                b = poly_div(target, die_poly(a))                # (3)!
                if b is None or min(b) < 0 or any(b[:low]):      # (4)!
                    continue
                if a <= faces_of(b):                             # (5)!
                    pairs.append((a, faces_of(b)))
            return pairs
        ```

        1. ‏\( x^i \cdot x^j = x^{i+j} \) : הפאה \( i \) של קובייה אחת והפאה \( j \) של השנייה
           נותנות את הסכום \( i + j \), והמקדם סופר את ההטלות.
        2. כל קובייה A, כרשימה לא יורדת של פאות. פאה של A היא לכל היותר \( 2n - \text{low} \),
           כי הפאה הקטנה של B היא לפחות `low` והסכום הגדול הוא \( 2n \).
        3. אם \( A \cdot B = P^2 \) אז \( B = P^2 / A \) : הקובייה השנייה נקבעת, ולא צריך לחפש
           אותה.
        4. ‏B היא קובייה רק אם אין לה מקדם שלילי ואין לה פאה מתחת ל-`low`.
        5. כל זוג נמצא פעמיים, פעם כ-(A, B) ופעם כ-(B, A). שומרים רק את הסדר שבו A קודמת.

    === "SystemVerilog"
        ```systemverilog title="function automatic bit same_sum" linenums="1" hl_lines="16 87"
        typedef int poly_t[$];                  // coefficients from x^0 up

        // The die as a polynomial: c[f] is the number of faces that show f
        function automatic poly_t die_poly(int faces[$]);
          poly_t c;
          int top = 0;
          foreach (faces[i]) if (faces[i] > top) top = faces[i];
          repeat (top + 1) c.push_back(0);
          foreach (faces[i]) c[faces[i]]++;
          return c;
        endfunction

        function automatic poly_t poly_mul(poly_t p, poly_t q);
          poly_t r;
          repeat (p.size() + q.size() - 1) r.push_back(0);
          foreach (p[i]) foreach (q[j]) r[i + j] += p[i] * q[j];   // (1)!
          return r;
        endfunction

        // The faces of a die polynomial, from the lowest up
        function automatic poly_t faces_of(poly_t c);
          poly_t f;
          foreach (c[i]) repeat (c[i]) f.push_back(i);
          return f;
        endfunction

        // 1 when the sum of a and b is distributed as the sum of two standard dice
        function automatic bit same_sum(int a[$], int b[$]);
          int std[$];
          poly_t got, want;
          if (a.size() != b.size()) return 0;
          for (int f = 1; f <= a.size(); f++) std.push_back(f);
          got = poly_mul(die_poly(a), die_poly(b));
          want = poly_mul(die_poly(std), die_poly(std));
          if (got.size() != want.size()) return 0;
          foreach (got[s]) if (got[s] != want[s]) return 0;
          return 1;
        endfunction

        // p / q into out when q divides p with whole coefficients (long division); 0 if not
        function automatic bit poly_div(poly_t p, poly_t q, output poly_t out);
          int c, top = q.size() - 1;
          out.delete();
          if (p.size() < q.size()) return 0;
          repeat (p.size() - top) out.push_back(0);
          for (int i = out.size() - 1; i >= 0; i--) begin
            if (p[i + top] % q[top] != 0) return 0;
            c = p[i + top] / q[top];
            out[i] = c;
            foreach (q[j]) p[i + j] -= c * q[j];
          end
          foreach (p[i]) if (p[i] != 0) return 0;
          return 1;
        endfunction

        // 1 when a die polynomial has no negative coefficient and no face under low
        function automatic bit is_die(poly_t c, int low);
          foreach (c[f]) if (c[f] < 0 || (f < low && c[f] != 0)) return 0;
          return 1;
        endfunction

        // The pair as text, "1 2 2 3 3 4 + 1 3 4 5 6 8", when a comes before b or is b, so that
        // each pair is kept once; 0 otherwise
        function automatic bit pair_text(poly_t a, poly_t b, output string line);
          foreach (a[i]) if (a[i] != b[i]) begin
            if (a[i] > b[i]) return 0;
            break;
          end
          line = "";
          foreach (a[k]) line = {line, $sformatf("%0d ", a[k])};
          line = {line, "+"};
          foreach (b[k]) line = {line, $sformatf(" %0d", b[k])};
          return 1;
        endfunction

        // Every pair of n-sided dice, faces from low up, with the sum of two standard dice:
        // die A runs over every non-decreasing list of faces, B = P^2 / A
        function automatic void dice_pairs(int n, int low, ref string pairs[$]);
          int a[$], std[$], i, hi = 2 * n - low;
          poly_t target, q;
          string line;
          for (int f = 1; f <= n; f++) std.push_back(f);
          target = poly_mul(die_poly(std), die_poly(std));
          repeat (n) a.push_back(low);
          pairs.delete();
          forever begin
            if (poly_div(target, die_poly(a), q) && is_die(q, low) && pair_text(a, faces_of(q), line))
              pairs.push_back(line);
            i = n - 1;                          // (2)!
            while (i >= 0 && a[i] == hi) i--;
            if (i < 0) break;
            a[i]++;
            for (int j = i + 1; j < n; j++) a[j] = a[i];
          end
        endfunction
        ```

        1. כמו ב-Python : הפאות \( i \) ו-\( j \) נותנות את הסכום \( i + j \).
        2. הרשימה הבאה, כמו מונה קילומטרים : מוצאים את הפאה האחרונה שעוד יכולה לגדול, מגדילים
           אותה, וכל הפאות אחריה מקבלות את אותו ערך, כדי שהרשימה תישאר לא יורדת.

    #### למה זה נכון { .sol-proof }

    **מכפלה היא התפלגות של סכום.** כל אחת מ-\( 6 \cdot 6 \) ההטלות היא זוג איברים, אחד מכל
    פולינום, ותורמת 1 למקדם של \( x \) בחזקת הסכום שלה. לכן שני זוגות קוביות נותנים את אותה
    התפלגות של הסכום בדיוק כשהמכפלות שלהם שוות, ו-\( A(x) B(x) = P(x)^2 \).

    **פירוק יחיד.** פולינום עם מקדמים שלמים מתפרק לגורמים שאי אפשר לפרק עוד בדרך אחת בלבד, כמו
    מספר לגורמים ראשוניים. ‏\( x \) ו-\( 1 + x \) הם ממעלה 1. ל-\( 1 + x + x^2 \) ול-\( 1 - x + x^2 \)
    אין שורש ממשי (הדיסקרימיננטה של שניהם היא \( -3 \)), ולכן אין להם גורם ממעלה 1, והם לא
    מתפרקים. מכאן ש-\( A(x) \) היא מכפלה של חלק משמונת הגורמים של \( P(x)^2 \), ו-\( B(x) \) של
    השאר. גם מספר קבוע כמו 2 לא יכול להיות גורם של \( A(x) \), כי אז הוא היה מחלק את כל המקדמים
    של \( P(x)^2 \), והמקדם של \( x^2 \) הוא 1.

    **הספירה.** שלבים 2 ו-3 קבעו את כל הגורמים חוץ מ-\( 1 - x + x^2 \), ממנו A מקבלת 0, 1 או 2.
    ‏1 נותן את הרגילות. 0 ו-2 נותנים אותו זוג, רק עם A ו-B מוחלפות. בשני המקרים המקדמים לא
    שליליים, ולכן יש בדיוק שני זוגות, הרגיל ו-Sicherman :

    <!-- gen 3 -->

    <div class="sc-pair"><figure class="sc-fig"><svg class="figure sc-split" viewBox="0 0 206 198" style="max-width:12.875rem" role="img" aria-label="הגורמים של הקוביות הרגילות : לכל קובייה x, ‏1 + x, ‏1 + x + x² ו-1 − x + x² אחד, והפאות 1 עד 6"><text class="sc-head" x="50.0" y="16" text-anchor="middle">A</text><g class="sc-chip sc-px"><rect x="6" y="28" width="88" height="22" rx="11"/><text x="50.0" y="43" text-anchor="middle">x</text></g><g class="sc-chip sc-p2"><rect x="6" y="56" width="88" height="22" rx="11"/><text x="50.0" y="71" text-anchor="middle">1 + x</text></g><g class="sc-chip sc-p3"><rect x="6" y="84" width="88" height="22" rx="11"/><text x="50.0" y="99" text-anchor="middle">1 + x + x²</text></g><g class="sc-chip sc-p6"><rect x="6" y="112" width="88" height="22" rx="11"/><text x="50.0" y="127" text-anchor="middle">1 − x + x²</text></g><rect class="sc-chip sc-empty" x="6" y="140" width="88" height="22" rx="11"/><line class="sc-rule" x1="6" x2="94" y1="172" y2="172"/><text class="sc-faces" x="50.0" y="190" text-anchor="middle">1 2 3 4 5 6</text><text class="sc-head" x="156.0" y="16" text-anchor="middle">B</text><g class="sc-chip sc-px"><rect x="112" y="28" width="88" height="22" rx="11"/><text x="156.0" y="43" text-anchor="middle">x</text></g><g class="sc-chip sc-p2"><rect x="112" y="56" width="88" height="22" rx="11"/><text x="156.0" y="71" text-anchor="middle">1 + x</text></g><g class="sc-chip sc-p3"><rect x="112" y="84" width="88" height="22" rx="11"/><text x="156.0" y="99" text-anchor="middle">1 + x + x²</text></g><g class="sc-chip sc-p6"><rect x="112" y="112" width="88" height="22" rx="11"/><text x="156.0" y="127" text-anchor="middle">1 − x + x²</text></g><rect class="sc-chip sc-empty" x="112" y="140" width="88" height="22" rx="11"/><line class="sc-rule" x1="112" x2="200" y1="172" y2="172"/><text class="sc-faces" x="156.0" y="190" text-anchor="middle">1 2 3 4 5 6</text></svg><figcaption>הזוג הרגיל : ‏<span dir="ltr">1 − x + x²</span> אחד לכל קובייה</figcaption></figure><figure class="sc-fig"><svg class="figure sc-split" viewBox="0 0 206 198" style="max-width:12.875rem" role="img" aria-label="הגורמים של קוביות Sicherman : ל-A רק x, ‏1 + x ו-1 + x + x², והפאות 1, 2, 2, 3, 3, 4. ל-B אותם שלושה ושני הגורמים 1 − x + x², והפאות 1, 3, 4, 5, 6, 8"><text class="sc-head" x="50.0" y="16" text-anchor="middle">A</text><g class="sc-chip sc-px"><rect x="6" y="28" width="88" height="22" rx="11"/><text x="50.0" y="43" text-anchor="middle">x</text></g><g class="sc-chip sc-p2"><rect x="6" y="56" width="88" height="22" rx="11"/><text x="50.0" y="71" text-anchor="middle">1 + x</text></g><g class="sc-chip sc-p3"><rect x="6" y="84" width="88" height="22" rx="11"/><text x="50.0" y="99" text-anchor="middle">1 + x + x²</text></g><rect class="sc-chip sc-empty" x="6" y="112" width="88" height="22" rx="11"/><rect class="sc-chip sc-empty" x="6" y="140" width="88" height="22" rx="11"/><line class="sc-rule" x1="6" x2="94" y1="172" y2="172"/><text class="sc-faces" x="50.0" y="190" text-anchor="middle">1 2 2 3 3 4</text><text class="sc-head" x="156.0" y="16" text-anchor="middle">B</text><g class="sc-chip sc-px"><rect x="112" y="28" width="88" height="22" rx="11"/><text x="156.0" y="43" text-anchor="middle">x</text></g><g class="sc-chip sc-p2"><rect x="112" y="56" width="88" height="22" rx="11"/><text x="156.0" y="71" text-anchor="middle">1 + x</text></g><g class="sc-chip sc-p3"><rect x="112" y="84" width="88" height="22" rx="11"/><text x="156.0" y="99" text-anchor="middle">1 + x + x²</text></g><g class="sc-chip sc-p6"><rect x="112" y="112" width="88" height="22" rx="11"/><text x="156.0" y="127" text-anchor="middle">1 − x + x²</text></g><g class="sc-chip sc-p6"><rect x="112" y="140" width="88" height="22" rx="11"/><text x="156.0" y="155" text-anchor="middle">1 − x + x²</text></g><line class="sc-rule" x1="112" x2="200" y1="172" y2="172"/><text class="sc-faces" x="156.0" y="190" text-anchor="middle">1 3 4 5 6 8</text></svg><figcaption>זוג Sicherman : שניהם לקובייה B</figcaption></figure></div>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="sc-key-px"></i>הגורם x</span><span><i class="sc-key-p2"></i>הגורם <span dir="ltr">1 + x</span></span><span><i class="sc-key-p3"></i>הגורם <span dir="ltr">1 + x + x²</span></span><span><i class="sc-key-p6"></i>הגורם החופשי <span dir="ltr">1 − x + x²</span></span><span><i class="sc-key-empty"></i>מקום ריק</span></span>

    <!-- /gen -->

    **החיפוש בקוד.** ‏`dice_pairs` לא מניח את הפירוק : היא עוברת על כל קובייה A אפשרית, ולכל
    אחת מחלקת. אם יש B כזו, היא בהכרח \( P(x)^2 / A(x) \), ולכן אף זוג לא מתפספס. על
    \( n = 6 \) היא מוצאת בדיוק את שני הזוגות.

    **נסו בעצמכם.** בתיבה כותבים מספר על כל פאה של שתי הקוביות, ורואים את טבלת הסכומים ואת
    ההיסטוגרמה של הסכום מול המשולש. היא נפתחת על קוביות Sicherman : כל עמודה בגובה הקו שלה.
    שנו את ה-8 של B ל-7 : ארבעה סכומים יוצאים מהמשולש, 8, 9, 11 ו-12, ובטבלה ממוסגרים התאים
    שלהם. אחר כך לחצו על
    "ניסיון : 1 פעמיים" : הסכום 2 מתקבל פעמיים ו-12 אף פעם. מה אומרת השורה שמתחת להיסטוגרמה על
    כל קובייה לבד, כשלוחצים על "Sicherman"?

    <div class="explorer" data-kind="sicherman" data-n="6" data-a="1.2.2.3.3.4" data-b="1.3.4.5.6.8"></div>

    #### סיבוכיות { .sol-cost }

    ‏`same_sum` כופלת שני פולינומים : \( O(n^2) \). ‏`dice_pairs` עוברת על כל הקוביות A,
    רשימות לא יורדות של \( n \) פאות מתוך \( 2n - 1 \) ערכים. יש
    \( \binom{3n-2}{n} \) כאלה, ולכל אחת חילוק ארוך של \( O(n^2) \). עם \( n = 6 \) אלה 8,008
    קוביות, פחות משנייה. המספר גדל מעריכית, ולכן בסעיף ג מחלקים את הגורמים במקום לחפש.

---

### סעיף ב – גם 0 על פאה

עכשיו מותר לכתוב גם 0 על פאה : מספרים שלמים מ-0 ומעלה. כמה זוגות של קוביות של שש פאות נותנים
את ההתפלגות של הסכום של שתי קוביות רגילות? מה הקשר בין הזוגות החדשים לזוגות של סעיף א?

??? tip "רמז 1"
    מורידים 1 מכל פאה של קובייה אחת ומוסיפים 1 לכל פאה של השנייה. מה קורה לכל אחת מ-36
    ההטלות?

??? tip "רמז 2"
    בסעיף א הצבנו \( x = 0 \) כדי לחלק את שני הגורמים \( x \), אחד לכל קובייה. מה משתנה כשמותרת
    פאה 0?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **‏5 זוגות :** שני הזוגות של סעיף א ושלוש הזזות שלהם. מורידים 1 מכל הפאות של קובייה
        אחת ומוסיפים 1 לכל הפאות של השנייה, וכל הטלה שומרת על הסכום שלה. בפולינומים : שני
        הגורמים \( x \) כבר לא חייבים להתחלק אחד לכל קובייה. את הרגילות אפשר להזיז בדרך אחת, כי
        הן זהות, ואת Sicherman בשתיים, לפי הקובייה שיורדת : \( 2 + 1 + 2 = 5 \).

    #### הרעיון { .sol-idea }

    הזזה לא משנה סכום : אם A יורדת ב-1 ו-B עולה ב-1, כל אחת מ-36 ההטלות נותנת את אותו סכום
    כמו קודם. בסעיף א הזזה כזו הייתה אסורה, כי הפאה הקטנה של כל קובייה היא 1, ואחרי ההזזה היה
    0. עכשיו מותר, ומכל זוג של סעיף א יוצאים זוגות חדשים :

    <!-- gen 5 -->

    | הזוג | קובייה A | קובייה B |
    |---|---|---|
    | הרגילות | ‏<span dir="ltr">1, 2, 3, 4, 5, 6</span> | ‏<span dir="ltr">1, 2, 3, 4, 5, 6</span> |
    | ‏Sicherman | ‏<span dir="ltr">1, 2, 2, 3, 3, 4</span> | ‏<span dir="ltr">1, 3, 4, 5, 6, 8</span> |
    | הרגילות, A פחות 1 ו-B ועוד 1 | ‏<span dir="ltr">0, 1, 2, 3, 4, 5</span> | ‏<span dir="ltr">2, 3, 4, 5, 6, 7</span> |
    | ‏Sicherman, הקטנה פחות 1 והגדולה ועוד 1 | ‏<span dir="ltr">0, 1, 1, 2, 2, 3</span> | ‏<span dir="ltr">2, 4, 5, 6, 7, 9</span> |
    | ‏Sicherman, הגדולה פחות 1 והקטנה ועוד 1 | ‏<span dir="ltr">0, 2, 3, 4, 5, 7</span> | ‏<span dir="ltr">2, 3, 3, 4, 4, 5</span> |

    <!-- /gen -->

    אין הזזה ב-2 : אז הפאה הקטנה של B הייתה 3, ושל A הייתה \( -1 \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **אותו פירוק :** ‏\( A(1) = 6 \) עדיין מחייב \( 1 + x \) ו-\( 1 + x + x^2 \) אחד לכל
       קובייה, ו-\( 1 - x + x^2 \) מתחלק 0, 1 או 2.
    2. **שני ה-\( x \) :** לכל גורם אחר יש מקדם חופשי 1, ולכן הפאה הקטנה של A היא מספר
       הגורמים \( x \) ש-A קיבלה : 0, 1 או 2. ‏B מקבלת את השאר.
    3. **תשע חלוקות :** שלוש אפשרויות ל-\( x \) כפול שלוש ל-\( 1 - x + x^2 \). הכפלה ב-\( x \)
       רק מזיזה את המקדמים, ולכן כל התשע הן קוביות.
    4. **זוגות בלי סדר :** החלפת A ו-B הופכת חלוקה לחלוקה הנגדית. רק \( x \) אחד ו-\( 1 - x + x^2 \)
       אחד לכל קובייה, הזוג הרגיל, נגדית לעצמה. לכן יש \( 1 + 8 / 2 = 5 \) זוגות.

    </div>

    הקוד של סעיף א מוצא אותם כמו שהוא : ‏`dice_pairs(6, low=0)` מחזירה את חמשת הזוגות של הטבלה.

    #### למה זה נכון { .sol-proof }

    **הזזה.** הזזה של A למטה ב-\( c \) ושל B למעלה ב-\( c \) היא \( x^{-c} A(x) \cdot x^{c} B(x) \),
    ואותה מכפלה.

    **הגבול.** ‏\( 1 + x \), ‏\( 1 + x + x^2 \) ו-\( 1 - x + x^2 \) שווים 1
    ב-\( x = 0 \), ולכן אם A קיבלה \( k \) גורמים \( x \), המקדם הנמוך שלה הוא של \( x^k \) : הפאה
    הקטנה שלה היא \( k \). יש רק שני גורמים \( x \), ולכן הפאות הקטנות של A ו-B הן 0 ו-2, 1 ו-1,
    או 2 ו-0. בזה הספירה של השלבים מלאה. אם היו מותרים גם מספרים שליליים, כל הזזה \( c \) הייתה
    עובדת, והיו אינסוף זוגות.

    **נסו בעצמכם.** התיבה נפתחת על ההזזה של Sicherman שבה הקובייה הקטנה יורדת. לחצו על
    "Sicherman" ועל "הזזה 2 של Sicherman" : הטבלה משתנה וההיסטוגרמה לא. איזו קובייה ירדה בכל
    הזזה? אחר כך כתבו 1 במקום ה-0 של A, בלי לגעת ב-B : שישה סכומים יוצאים מהמשולש, 2, 3 ו-4
    ו-8, 9 ו-10. רק הזזה של קובייה שלמה, יחד עם הזזה הפוכה של השנייה, שומרת על כל הסכומים.

    <div class="explorer" data-kind="sicherman" data-n="6" data-a="0.1.1.2.2.3" data-b="2.4.5.6.7.9"></div>

---

### סעיף ג – מספר פאות כללי

שתי קוביות של \( n \) פאות, עם מספרים שלמים חיוביים, צריכות לתת את ההתפלגות של הסכום של שתי
קוביות רגילות של \( n \) פאות, עם המספרים 1 עד \( n \). לאילו \( n \) יש זוג חוץ מהרגיל? מצאו
את כל הזוגות של \( n = 4 \) ושל \( n = 8 \), וכתבו קוד שמוצא אותם לכל \( n \) בלי לעבור על כל
הקוביות.

??? tip "רמז 1"
    ‏\( P_n(x) = x + x^2 + \dots + x^n = x \cdot \frac{x^n - 1}{x - 1} \). איך מתפרק \( x^n - 1 \)?
    נסו \( n = 4 \) : ‏\( x^4 - 1 = (x - 1)(x + 1)(x^2 + 1) \).

??? tip "רמז 2"
    ‏\( x^n - 1 \) מתפרק לגורם אחד \( \Phi_d(x) \) לכל מחלק \( d \) של \( n \), שנקרא הפולינום
    הציקלוטומי. מה הערך של כל גורם ב-\( x = 1 \), ומה זה אומר כש-\( n \) ראשוני?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        **יש זוג אחר בדיוק כש-\( n \) פריק.** ‏\( P_n(x) = x \prod_{d \mid n,\ d > 1} \Phi_d(x) \),
        וכל זוג הוא חלוקה : \( x \) אחד לכל קובייה, ומכל \( \Phi_d \) עותק אחד, שניים או אף אחד
        לקובייה A. נשארות החלוקות שבהן \( A(1) = n \) ואין מקדם שלילי. כש-\( n \) ראשוני יש רק
        \( \Phi_n \), והזוג הרגיל לבד. ל-\( n = 4 \) יש זוג אחד נוסף, \( \{1, 2, 2, 3\} \)
        ו-\( \{1, 3, 3, 5\} \), ול-\( n = 8 \) שלושה.

    <!-- cost: זמן \( O(3^{\tau(n)} \, \tau(n) \, n^2) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    כמו בסעיף א, מפרקים את הקובייה הרגילה. ‏\( P_n(x) = x(1 + x + \dots + x^{n-1}) \), והסוגריים
    הם \( \frac{x^n - 1}{x - 1} \). השורשים של \( x^n - 1 \) הם \( n \) שורשי היחידה, והם
    מתקבצים לפי הסדר שלהם : לכל מחלק \( d \) של \( n \) גורם אחד, \( \Phi_d(x) \), שהשורשים שלו
    הם שורשי היחידה מסדר \( d \) בדיוק. לכן \( x^n - 1 = \prod_{d \mid n} \Phi_d(x) \), ו-\( \Phi_1 = x - 1 \)
    מצטמצם. אלה הגורמים של \( n \) עד 12 :

    <!-- gen 6 -->

    | המחלק d | הגורם \( \Phi_d(x) \) | הערך \( \Phi_d(1) \) |
    |:-:|---|:-:|
    | 2 | ‏\( 1 + x \) | 2 |
    | 3 | ‏\( 1 + x + x^2 \) | 3 |
    | 4 | ‏\( 1 + x^2 \) | 2 |
    | 5 | ‏\( 1 + x + x^2 + x^3 + x^4 \) | 5 |
    | 6 | ‏\( 1 - x + x^2 \) | 1 |
    | 7 | ‏\( 1 + x + \dots + x^{6} \) | 7 |
    | 8 | ‏\( 1 + x^4 \) | 2 |
    | 9 | ‏\( 1 + x^3 + x^6 \) | 3 |
    | 10 | ‏\( 1 - x + x^2 - x^3 + x^4 \) | 1 |
    | 11 | ‏\( 1 + x + \dots + x^{10} \) | 11 |
    | 12 | ‏\( 1 - x^2 + x^4 \) | 1 |

    <!-- /gen -->

    לכל \( \Phi_d \) מקדמים שלמים, והוא לא מתפרק (משפט ידוע). ל-\( n = 6 \) אלה בדיוק
    הגורמים של סעיף א : \( \Phi_2 = 1 + x \), ‏\( \Phi_3 = 1 + x + x^2 \) ו-\( \Phi_6 = 1 - x + x^2 \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הגורמים :** ‏\( P_n(x) = x \prod_{d \mid n,\ d > 1} \Phi_d(x) \), וב-\( P_n(x)^2 \) כל
       אחד מהם פעמיים.
    2. **אין פאה 0 :** כמו בסעיף א, \( x \) אחד לכל קובייה.
    3. **החלוקה :** לכל מחלק \( d > 1 \) בוחרים \( k_d \in \{0, 1, 2\} \) : ‏A מקבלת \( k_d \)
       עותקים של \( \Phi_d \), ו-B את \( 2 - k_d \) האחרים.
    4. **מספר הפאות :** ‏\( A(1) = \prod_d \Phi_d(1)^{k_d} \) צריך להיות \( n \). ‏\( \Phi_d(1) \)
       הוא \( p \) כש-\( d \) חזקה של ראשוני \( p \), ו-1 בכל מקרה אחר.
    5. **מקדמים לא שליליים :** שומרים רק חלוקה שבה ל-A ול-B אין מקדם שלילי.
    6. **בלי כפילויות :** חלוקה והנגדית שלה, \( 2 - k_d \) לכל \( d \), הן אותו זוג.

    </div>

    כך יוצא מספר הזוגות לכל \( n \) עד 12, כולל הזוג הרגיל. העמודה האחרונה מתירה גם 0 על פאה, כמו
    בסעיף ב : אז גם שני הגורמים \( x \) מתחלקים 0, 1 או 2.

    <!-- gen 7 -->

    | הפאות n | הגורמים של \( P_n \) מלבד x | הזוגות, פאות חיוביות | הזוגות, גם 0 |
    |:-:|---|:-:|:-:|
    | 2 | ‏\( \Phi_{2} \) | 1 | 2 |
    | 3 | ‏\( \Phi_{3} \) | 1 | 2 |
    | 4 | ‏\( \Phi_{2} \, \Phi_{4} \) | 2 | 5 |
    | 5 | ‏\( \Phi_{5} \) | 1 | 2 |
    | 6 | ‏\( \Phi_{2} \, \Phi_{3} \, \Phi_{6} \) | 2 | 5 |
    | 7 | ‏\( \Phi_{7} \) | 1 | 2 |
    | 8 | ‏\( \Phi_{2} \, \Phi_{4} \, \Phi_{8} \) | 4 | 11 |
    | 9 | ‏\( \Phi_{3} \, \Phi_{9} \) | 2 | 5 |
    | 10 | ‏\( \Phi_{2} \, \Phi_{5} \, \Phi_{10} \) | 2 | 5 |
    | 11 | ‏\( \Phi_{11} \) | 1 | 2 |
    | 12 | ‏\( \Phi_{2} \, \Phi_{3} \, \Phi_{4} \, \Phi_{6} \, \Phi_{12} \) | 8 | 23 |

    <!-- /gen -->

    אלה הזוגות של \( n = 4 \) ושל \( n = 8 \), כל אחד עם הגורמים של כל קובייה :

    <!-- gen 8 -->

    | הפאות n | קובייה A | הגורמים של A | קובייה B | הגורמים של B |
    |:-:|---|---|---|---|
    | 4 | ‏<span dir="ltr">1, 2, 3, 4</span> | ‏\( x \, \Phi_{2} \, \Phi_{4} \) | ‏<span dir="ltr">1, 2, 3, 4</span> | ‏\( x \, \Phi_{2} \, \Phi_{4} \) |
    | 4 | ‏<span dir="ltr">1, 2, 2, 3</span> | ‏\( x \, \Phi_{2}^2 \) | ‏<span dir="ltr">1, 3, 3, 5</span> | ‏\( x \, \Phi_{4}^2 \) |
    | 8 | ‏<span dir="ltr">1, 2, 3, 4, 5, 6, 7, 8</span> | ‏\( x \, \Phi_{2} \, \Phi_{4} \, \Phi_{8} \) | ‏<span dir="ltr">1, 2, 3, 4, 5, 6, 7, 8</span> | ‏\( x \, \Phi_{2} \, \Phi_{4} \, \Phi_{8} \) |
    | 8 | ‏<span dir="ltr">1, 2, 3, 3, 4, 4, 5, 6</span> | ‏\( x \, \Phi_{2} \, \Phi_{4}^2 \) | ‏<span dir="ltr">1, 2, 5, 5, 6, 6, 9, 10</span> | ‏\( x \, \Phi_{2} \, \Phi_{8}^2 \) |
    | 8 | ‏<span dir="ltr">1, 2, 2, 3, 5, 6, 6, 7</span> | ‏\( x \, \Phi_{2}^2 \, \Phi_{8} \) | ‏<span dir="ltr">1, 3, 3, 5, 5, 7, 7, 9</span> | ‏\( x \, \Phi_{4}^2 \, \Phi_{8} \) |
    | 8 | ‏<span dir="ltr">1, 2, 2, 3, 3, 4, 4, 5</span> | ‏\( x \, \Phi_{2}^2 \, \Phi_{4} \) | ‏<span dir="ltr">1, 3, 5, 5, 7, 7, 9, 11</span> | ‏\( x \, \Phi_{4} \, \Phi_{8}^2 \) |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="factor_pairs" linenums="1" hl_lines="9 18 25"
        from itertools import product


        def cyclotomic(d):
            """Phi_d: x^d - 1 divided by Phi_e of every e < d that divides d."""
            p = [-1] + [0] * (d - 1) + [1]
            for e in range(1, d):
                if d % e == 0:
                    p = poly_div(p, cyclotomic(e))               # (1)!
            return p


        def factor_pairs(n):
            """The pairs of n-sided dice (positive faces) whose sum is distributed as the sum
            of two standard dice, from the factors x * Phi_d, d > 1 dividing n; each pair once."""
            ds = [d for d in range(2, n + 1) if n % d == 0]
            pairs = []
            for split in product((0, 1, 2), repeat=len(ds)):    # (2)!
                a, b = [0, 1], [0, 1]
                for d, k in zip(ds, split):
                    for _ in range(k):
                        a = poly_mul(a, cyclotomic(d))
                    for _ in range(2 - k):
                        b = poly_mul(b, cyclotomic(d))
                if sum(a) == n and min(a) >= 0 and min(b) >= 0:  # (3)!
                    if faces_of(a) <= faces_of(b):
                        pairs.append((faces_of(a), faces_of(b)))
            return sorted(pairs)
        ```

        1. ‏\( x^d - 1 \) הוא המכפלה של כל \( \Phi_e \) ש-\( e \) מחלק את \( d \). מחלקים בכל
           האחרים, ונשאר \( \Phi_d \). החילוק תמיד מדויק.
        2. ‏\( k_d \) לכל מחלק : \( 3^{\tau(n) - 1} \) חלוקות, כש-\( \tau(n) \) הוא מספר המחלקים
           של \( n \).
        3. ‏\( A(1) \), סכום המקדמים, הוא מספר הפאות. אם הוא \( n \), גם ל-B יש \( n \) פאות,
           כי \( A(1) B(1) = n^2 \).

    === "SystemVerilog"
        ```systemverilog title="function automatic void factor_pairs" linenums="1" hl_lines="11 28 33"
        // Phi_d: x^d - 1 divided by Phi_e of every e < d that divides d, the e's in rising order
        function automatic poly_t cyclotomic(int d);
          poly_t phi[int];                      // phi[e]: the factors found so far
          poly_t p, q;
          for (int m = 1; m <= d; m++) begin
            if (d % m != 0) continue;
            p.delete();
            p.push_back(-1);
            repeat (m - 1) p.push_back(0);
            p.push_back(1);
            for (int e = 1; e < m; e++) if (m % e == 0) begin void'(poly_div(p, phi[e], q)); p = q; end
            phi[m] = p;
          end
          return phi[d];
        endfunction

        // The pairs of n-sided dice with the sum of two standard dice, from the factors x * Phi_d
        function automatic void factor_pairs(int n, ref string pairs[$]);
          int ds[$], total = 1, code, k;
          poly_t a, b, phi;
          string line;
          for (int d = 2; d <= n; d++) if (n % d == 0) begin ds.push_back(d); total *= 3; end
          pairs.delete();
          for (int s = 0; s < total; s++) begin
            a = {0, 1}; b = {0, 1};
            code = s;
            foreach (ds[i]) begin               // k_d: the next base-3 digit of s
              k = code % 3; code /= 3;
              phi = cyclotomic(ds[i]);
              repeat (k) a = poly_mul(a, phi);
              repeat (2 - k) b = poly_mul(b, phi);
            end
            if (a.sum() == n && is_die(a, 1) && is_die(b, 1) && pair_text(faces_of(a), faces_of(b), line))
              pairs.push_back(line);
          end
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **הערך ב-1.** ‏\( 1 + x + \dots + x^{n-1} = \prod_{d \mid n,\ d > 1} \Phi_d(x) \), ובהצבה
    \( x = 1 \) : ‏\( n = \prod_{d \mid n,\ d > 1} \Phi_d(1) \). לחזקה של ראשוני, \( d = p^j \),
    ‏\( \Phi_d(x) = 1 + x^{p^{j-1}} + x^{2p^{j-1}} + \dots \) עם \( p \) איברים, ולכן
    \( \Phi_d(1) = p \). החזקות של \( p \) שמחלקות את \( n \) כבר נותנות יחד את כל החזקה של \( p \)
    ב-\( n \), ולכן כל שאר הגורמים שווים 1 ב-\( x = 1 \).

    **ראשוני.** אם \( n \) ראשוני, \( P_n = x \, \Phi_n \) ו-\( \Phi_n(1) = n \). כדי ש-\( A(1) = n \),
    ‏A מקבלת \( \Phi_n \) אחד בדיוק, ו-\( A = B = P_n \) : אין זוג אחר.

    **פריק, בלי פולינומים.** אם \( n = pm \) עם \( p, m \ge 2 \), אפשר לכתוב תוצאה של קובייה
    רגילה בשתי דרכים : \( 1 + u + p v \), ו-\( 1 + w + m z \), כש-\( u, z \) מ-0 עד \( p - 1 \)
    ו-\( v, w \) מ-0 עד \( m - 1 \), כולם אחידים ובלתי תלויים. לכן הסכום של שתי קוביות רגילות
    מתפלג כמו \( (1 + u + w) + (1 + p v + m z) \). כל סוגריים הם קובייה הוגנת של \( pm = n \)
    פאות : A עם הפאות \( 1 + u + w \), ו-B עם הפאות \( 1 + p v + m z \). ל-\( n = 6 \),
    ‏\( p = 2 \) ו-\( m = 3 \), אלה בדיוק קוביות Sicherman, ול-\( n = 4 \) הזוג
    \( \{1, 2, 2, 3\} \) ו-\( \{1, 3, 3, 5\} \). ב-A יש פאה 2 פעמיים, ולכן היא לא רגילה.

    **מקדמים שליליים.** התנאי \( A(1) = n \) לא מספיק. ל-\( n = 12 \) החלוקה
    \( A = x \, \Phi_3 \, \Phi_4^2 \, \Phi_6^2 \) נותנת \( A(1) = 3 \cdot 2^2 = 12 \), אבל
    \( A(x) = x - x^2 + 4x^3 - \dots \) : המקדם של \( x^2 \) הוא \( -1 \), ומספר פאות לא יכול
    להיות שלילי. לכן הקוד בודק את המקדמים.

    **נסו בעצמכם.** התיבה נפתחת על \( n = 8 \). לחצו על שלושת הזוגות : בכל אחד הטבלה אחרת
    וההיסטוגרמה זהה. בזוג 1 שנו את ה-11 של B ל-10 : ארבעה סכומים יוצאים מהמשולש. אילו? אחר כך בחרו 4 פאות
    ולחצו על "הזוג האחר" : זה הזוג \( 1 + u + w \) ו-\( 1 + 2v + 2z \) של ההוכחה.

    <div class="explorer" data-kind="sicherman" data-n="8" data-a="1.2.2.3.3.4.4.5" data-b="1.3.5.5.7.7.9.11"></div>

    #### סיבוכיות { .sol-cost }

    ‏\( 3^{\tau(n) - 1} \) חלוקות, ובכל אחת עד \( 2\tau(n) \) כפלי פולינומים ממעלה עד \( 2n \) :
    זמן \( O(3^{\tau(n)} \, \tau(n) \, n^2) \). ל-\( n = 12 \), עם 6 מחלקים, אלה 243 חלוקות, מול
    יותר מחצי מיליארד קוביות בחיפוש של סעיף א. הזיכרון הוא כמה פולינומים, \( O(n) \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : בודק שמסתכל רק על הסכום"
    מחולל של שתי קוביות במודל אימות, ובודק שאוסף היסטוגרמה של הסכום ומשווה אותה למשולש, או
    covergroup עם coverpoint אחד על הסכום. באג שמחליף את הקוביות בקוביות Sicherman עובר את
    שניהם : ההתפלגות של הסכום זהה. בודקים כל קובייה לבד, שכל פאה 1 עד 6 יוצאת בשישית מהמקרים, ואת
    ההתפלגות המשותפת, 36 הזוגות, כשהקוביות צריכות להיות בלתי תלויות.

??? trap "מלכודת : לחפש רק בפאות 1 עד 6"
    חיפוש שמגביל כל פאה ל-1 עד 6 לא מוצא את Sicherman, כי יש בה 8. הגבול הנכון הוא \( 2n - 1 \) :
    הפאה הקטנה של הקובייה השנייה היא לפחות 1, והסכום הגדול הוא \( 2n \).

??? trap "מלכודת : לבדוק רק את מספר הפאות"
    חלוקה של הגורמים עם \( A(1) = n \) נותנת פולינום עם סכום מקדמים נכון, אבל לא תמיד קובייה :
    ל-\( n = 12 \) יש חלוקות עם מקדם שלילי. גם הגורם \( 1 - x + x^2 \) לבד הוא לא קובייה. בודקים
    כל מקדם.

??? trap "מלכודת : לספור כל זוג פעמיים"
    ‏(A, B) ו-(B, A) הם אותו זוג. חיפוש שעובר על כל A מוצא את Sicherman פעמיים, ואת הרגילות פעם
    אחת. שומרים סדר קבוע, למשל A קודמת ל-B.

??? followup "שאלות המשך"
    - **קוביות בגדלים שונים :** קובייה של 4 פאות וקובייה של 9 פאות, עם מספרים שלמים חיוביים.
      איך מקבלים את ההתפלגות של הסכום של שתי קוביות רגילות של 6 פאות?

        ??? fu-answer "תשובה"
            אותם גורמים, עם \( A(1) = 4 \) ו-\( B(1) = 9 \) : ל-A שני \( 1 + x \) ואף
            \( 1 + x + x^2 \). יש שלושה זוגות : \( \{1, 2, 2, 3\} \) עם
            \( \{1, 3, 3, 5, 5, 5, 7, 7, 9\} \), ‏\( \{1, 2, 4, 5\} \) עם
            \( \{1, 2, 3, 3, 4, 5, 5, 6, 7\} \), ו-\( \{1, 4, 4, 7\} \) עם
            \( \{1, 2, 2, 3, 3, 3, 4, 4, 5\} \).

    - **שלוש קוביות :** שלוש קוביות של שש פאות, עם ההתפלגות של הסכום של שלוש קוביות רגילות. אילו
      שלישיות יש?

        ??? fu-answer "תשובה"
            כל קובייה מקבלת \( x \), ‏\( 1 + x \) ו-\( 1 + x + x^2 \) אחד, ושלושת העותקים של
            \( 1 - x + x^2 \) מתחלקים ביניהן. עותק לכל קובייה נותן את הרגילות. שניים לאחת ואחד
            לשנייה נותנים את זוג Sicherman עם קובייה רגילה. שלושה לאותה קובייה נותנים מקדם שלילי.
            לכן השלישייה האחרת היחידה היא קוביות Sicherman וקובייה רגילה.

    - **‏covergroup :** איך כותבים covergroup למחולל של שתי קוביות כך שבאג של קוביות Sicherman
      יתגלה?

        ??? fu-answer "תשובה"
            ‏coverpoint לכל קובייה עם bin לכל ערך מ-1 עד 6, ו-illegal_bins לכל ערך אחר. עם
            קוביות Sicherman הפאה 8 של B נופלת ב-illegal_bins, ה-bins של 5 ו-6 של A ושל 2 של B
            נשארים ריקים, ו-cross של שני ה-coverpoints מראה 20 מתוך 36 זוגות בלבד. ה-coverpoint
            של הסכום לבד מגיע ל-100%.
