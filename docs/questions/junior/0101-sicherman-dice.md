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
3. **שלוש קוביות ויותר :** שלוש קוביות של שש פאות, ואחר כך \( k \) קוביות, וההתפלגות של
   הסכום של אותו מספר קוביות רגילות. אילו קבוצות של קוביות יש, וכמה?

??? interviewer "מה המראיין בודק"
    - **ניסוי וטעייה מסודר :** האם המועמד מתחיל מהסכומים הנדירים, 2 ו-12, ומסיק מהם משהו על
      הפאות, או מנחש מספרים.
    - **כלי מתאים :** האם הוא מוצא דרך לחשב את ההתפלגות של סכום כפעולה אחת שאפשר גם לפרק, ולא
      רק למלא טבלאות.
    - **הוכחה שאין עוד :** למצוא זוג זה חצי מהעבודה. האם הוא מראה למה כל אפשרות אחרת נשללת.
    - **הכללה :** האם הוא מעביר את הטיעון של שתי קוביות לשלוש ול-\( k \), ורואה מה נשאר
      כמו שהוא ומה משתנה.
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

    <div class="explorer" data-kind="sicherman" data-a="1.2.2.3.3.4" data-b="1.3.4.5.6.8"></div>

    #### סיבוכיות { .sol-cost }

    ‏`same_sum` כופלת שני פולינומים : \( O(n^2) \). ‏`dice_pairs` עוברת על כל הקוביות A,
    רשימות לא יורדות של \( n \) פאות מתוך \( 2n - 1 \) ערכים. יש
    \( \binom{3n-2}{n} \) כאלה, ולכל אחת חילוק ארוך של \( O(n^2) \). עם \( n = 6 \) אלה 8,008
    קוביות, פחות משנייה. המספר גדל מעריכית, וגדל עוד יותר עם יותר קוביות, ולכן בסעיף ג
    מחלקים את הגורמים במקום לחפש.

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

    <div class="explorer" data-kind="sicherman" data-a="0.1.1.2.2.3" data-b="2.4.5.6.7.9"></div>

---

### סעיף ג – שלוש קוביות ויותר

עכשיו יש יותר משתי קוביות, כולן של שש פאות עם מספרים שלמים חיוביים. הסכום של שלוש קוביות
רגילות הוא מ-3 עד 18, ומתוך 216 ההטלות 10 ו-11 מתקבלים ב-27 הטלות כל אחד :

<!-- gen 6 -->

<svg class="perf-chart" viewBox="0 0 420 196" style="max-width:26.25rem" role="img" aria-label="התפלגות הסכום של שלוש קוביות רגילות : הסכומים 3 עד 18, ומספר ההטלות מתוך 216 שנותנות כל סכום, 1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1"><line class="grid" x1="34" x2="412" y1="166.0" y2="166.0"/><text class="tick" x="26" y="170.0" text-anchor="end">0</text><line class="grid" x1="34" x2="412" y1="116.7" y2="116.7"/><text class="tick" x="26" y="120.7" text-anchor="end">9</text><line class="grid" x1="34" x2="412" y1="67.3" y2="67.3"/><text class="tick" x="26" y="71.3" text-anchor="end">18</text><line class="grid" x1="34" x2="412" y1="18.0" y2="18.0"/><text class="tick" x="26" y="22.0" text-anchor="end">27</text><rect class="bar by-multiples" x="37.8" y="160.5" width="16.1" height="5.5" rx="2"><title>sum 3: 1 of 216</title></rect><text class="tick" x="45.8" y="155.5" text-anchor="middle">1</text><rect class="bar by-multiples" x="61.4" y="149.6" width="16.1" height="16.4" rx="2"><title>sum 4: 3 of 216</title></rect><text class="tick" x="69.4" y="144.6" text-anchor="middle">3</text><rect class="bar by-multiples" x="85.0" y="133.1" width="16.1" height="32.9" rx="2"><title>sum 5: 6 of 216</title></rect><text class="tick" x="93.1" y="128.1" text-anchor="middle">6</text><rect class="bar by-multiples" x="108.7" y="111.2" width="16.1" height="54.8" rx="2"><title>sum 6: 10 of 216</title></rect><text class="tick" x="116.7" y="106.2" text-anchor="middle">10</text><rect class="bar by-multiples" x="132.3" y="83.8" width="16.1" height="82.2" rx="2"><title>sum 7: 15 of 216</title></rect><text class="tick" x="140.3" y="78.8" text-anchor="middle">15</text><rect class="bar by-multiples" x="155.9" y="50.9" width="16.1" height="115.1" rx="2"><title>sum 8: 21 of 216</title></rect><text class="tick" x="163.9" y="45.9" text-anchor="middle">21</text><rect class="bar by-multiples" x="179.5" y="29.0" width="16.1" height="137.0" rx="2"><title>sum 9: 25 of 216</title></rect><text class="tick" x="187.6" y="24.0" text-anchor="middle">25</text><rect class="bar by-multiples" x="203.2" y="18.0" width="16.1" height="148.0" rx="2"><title>sum 10: 27 of 216</title></rect><text class="tick" x="211.2" y="13.0" text-anchor="middle">27</text><rect class="bar by-multiples" x="226.8" y="18.0" width="16.1" height="148.0" rx="2"><title>sum 11: 27 of 216</title></rect><text class="tick" x="234.8" y="13.0" text-anchor="middle">27</text><rect class="bar by-multiples" x="250.4" y="29.0" width="16.1" height="137.0" rx="2"><title>sum 12: 25 of 216</title></rect><text class="tick" x="258.4" y="24.0" text-anchor="middle">25</text><rect class="bar by-multiples" x="274.0" y="50.9" width="16.1" height="115.1" rx="2"><title>sum 13: 21 of 216</title></rect><text class="tick" x="282.1" y="45.9" text-anchor="middle">21</text><rect class="bar by-multiples" x="297.7" y="83.8" width="16.1" height="82.2" rx="2"><title>sum 14: 15 of 216</title></rect><text class="tick" x="305.7" y="78.8" text-anchor="middle">15</text><rect class="bar by-multiples" x="321.3" y="111.2" width="16.1" height="54.8" rx="2"><title>sum 15: 10 of 216</title></rect><text class="tick" x="329.3" y="106.2" text-anchor="middle">10</text><rect class="bar by-multiples" x="344.9" y="133.1" width="16.1" height="32.9" rx="2"><title>sum 16: 6 of 216</title></rect><text class="tick" x="352.9" y="128.1" text-anchor="middle">6</text><rect class="bar by-multiples" x="368.5" y="149.6" width="16.1" height="16.4" rx="2"><title>sum 17: 3 of 216</title></rect><text class="tick" x="376.6" y="144.6" text-anchor="middle">3</text><rect class="bar by-multiples" x="392.2" y="160.5" width="16.1" height="5.5" rx="2"><title>sum 18: 1 of 216</title></rect><text class="tick" x="400.2" y="155.5" text-anchor="middle">1</text><text class="tick" x="45.8" y="184" text-anchor="middle">3</text><text class="tick" x="69.4" y="184" text-anchor="middle">4</text><text class="tick" x="93.1" y="184" text-anchor="middle">5</text><text class="tick" x="116.7" y="184" text-anchor="middle">6</text><text class="tick" x="140.3" y="184" text-anchor="middle">7</text><text class="tick" x="163.9" y="184" text-anchor="middle">8</text><text class="tick" x="187.6" y="184" text-anchor="middle">9</text><text class="tick" x="211.2" y="184" text-anchor="middle">10</text><text class="tick" x="234.8" y="184" text-anchor="middle">11</text><text class="tick" x="258.4" y="184" text-anchor="middle">12</text><text class="tick" x="282.1" y="184" text-anchor="middle">13</text><text class="tick" x="305.7" y="184" text-anchor="middle">14</text><text class="tick" x="329.3" y="184" text-anchor="middle">15</text><text class="tick" x="352.9" y="184" text-anchor="middle">16</text><text class="tick" x="376.6" y="184" text-anchor="middle">17</text><text class="tick" x="400.2" y="184" text-anchor="middle">18</text><line class="axis" x1="34" x2="412" y1="166" y2="166"/></svg>

<!-- /gen -->

מצאו את כל השלישיות של קוביות, חוץ מהרגילות, שהסכום שלהן מתפלג כך. אחר כך \( k \) קוביות :
אילו קבוצות של \( k \) קוביות נותנות את ההתפלגות של הסכום של \( k \) קוביות רגילות, וכמה יש?
ומה משתנה כשמותר גם 0 על פאה? כתבו קוד שמוצא את כל הקבוצות.

??? tip "רמז 1"
    ההתפלגות של הסכום של שלוש קוביות היא המכפלה של שלושה פולינומים. איך מתפרק \( P(x)^3 \) לגורמים,
    וכמה מכל גורם כל קובייה חייבת לקבל?

??? tip "רמז 2"
    הגורם \( 1 - x + x^2 \) לא משנה את מספר הפאות, ולכן נשאר לחלק רק אותו. כמה עותקים שלו
    יכולה קובייה אחת לקבל? חשבו את המקדם של \( x^2 \) בקובייה שקיבלה שלושה.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        **זוגות Sicherman וקוביות רגילות, ותו לא.** כל קובייה מקבלת \( x \), ‏\( 1 + x \)
        ו-\( 1 + x + x^2 \) אחד, ו-\( e \) עותקים של \( 1 - x + x^2 \), כש-\( e \) הוא 0, 1 או
        2 : הקטנה של Sicherman, הרגילה או הגדולה. סכום ה-\( e \) הוא \( k \), ולכן יש קטנות
        כמו גדולות. לשלוש קוביות יש שלישייה אחת מלבד הרגילות, זוג Sicherman וקובייה רגילה,
        ול-\( k \) קוביות יש \( \lfloor k/2 \rfloor + 1 \) קבוצות.

    <!-- cost: זמן \( O(k^3) \) | זיכרון \( O(k^2) \) -->

    #### הרעיון { .sol-idea }

    כמו בסעיף א : הסכום של \( k \) קוביות מתפלג כמו הסכום של \( k \) קוביות רגילות בדיוק
    כשהמכפלה של \( k \) הפולינומים היא \( P(x)^k \). ב-\( P(x)^k \) כל אחד מארבעת הגורמים
    מופיע \( k \) פעמים, וכל קובייה מקבלת חלק מהם. ההצבות \( x = 0 \) ו-\( x = 1 \) קובעות
    שוב את שלושת הגורמים הראשונים, אחד מכל אחד לכל קובייה. רק \( k \) העותקים של
    \( 1 - x + x^2 \) מתחלקים בחופשיות, וכל קובייה נקבעת לפי מספר העותקים \( e \) שקיבלה :

    <!-- gen 7 -->

    | העותקים e | הקובייה | הפולינום | הפאות |
    |:-:|---|---|---|
    | 0 | הקטנה של Sicherman | ‏\( x + 2x^2 + 2x^3 + x^4 \) | ‏<span dir="ltr">1, 2, 2, 3, 3, 4</span> |
    | 1 | הרגילה | ‏\( x + x^2 + x^3 + x^4 + x^5 + x^6 \) | ‏<span dir="ltr">1, 2, 3, 4, 5, 6</span> |
    | 2 | הגדולה של Sicherman | ‏\( x + x^3 + x^4 + x^5 + x^6 + x^8 \) | ‏<span dir="ltr">1, 3, 4, 5, 6, 8</span> |
    | 3 | לא קובייה | ‏\( x - x^2 + 2x^3 + \dots + x^{10} \) | אין : המקדם של \( x^2 \) שלילי |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שלוש קוביות :** שלושת העותקים של \( 1 - x + x^2 \) מתחלקים בין שלוש הקוביות. חלוקה
       של \( 1 + 1 + 1 \) נותנת שלוש קוביות רגילות. חלוקה של \( 0 + 1 + 2 \) נותנת את הקטנה
       של Sicherman, רגילה ואת הגדולה : זוג Sicherman וקובייה רגילה. חלוקה של
       \( 0 + 0 + 3 \) לא אפשרית, כי לקובייה עם שלושה עותקים יש מקדם שלילי.
    2. **מספר כללי של קוביות :** כל קובייה היא אחת משלוש הקוביות של הטבלה, וה-\( e \) שלהן
       מסתכמים ל-\( k \). אם \( j \) קוביות הן הקטנה של Sicherman ו-\( l \) הן הגדולה, הסכום
       הוא \( (k - j - l) + 2l = k \), ולכן \( l = j \) : כל קטנה באה עם גדולה. קבוצה היא
       \( j \) זוגות Sicherman ו-\( k - 2j \) קוביות רגילות, עם \( j \) מ-0 עד
       \( \lfloor k/2 \rfloor \), ולכן יש \( \lfloor k/2 \rfloor + 1 \) קבוצות.
    3. **גם 0 על פאה :** כמו בסעיף ב, \( k \) הגורמים \( x \) כבר לא חייבים להתחלק אחד לכל
       קובייה. קובייה שקיבלה \( a \) מהם מתחילה ב-\( a \), וה-\( a \) מסתכמים ל-\( k \). לכל
       קבוצה של שלב 2 סופרים את הדרכים לחלק את ה-\( x \), וקוביות זהות לא נספרות פעמיים.
       בשלוש קוביות רגילות יש שלוש חלוקות : \( 1 + 1 + 1 \), ‏\( 0 + 1 + 2 \) ו-\( 0 + 0 + 3 \).
       ב-Sicherman ורגילה שלוש הקוביות שונות, וכל אחת מ-10 החלוקות עם סדר נותנת קבוצה
       אחרת. ביחד 13 קבוצות, והפאה הראשונה של כל קובייה היא מספר ה-\( x \) שלה :

        <!-- gen 8 -->

        | הבסיס | קובייה 1 | קובייה 2 | קובייה 3 |
        |---|---|---|---|
        | רגילות | ‏<span dir="ltr">1, 2, 3, 4, 5, 6</span> | ‏<span dir="ltr">1, 2, 3, 4, 5, 6</span> | ‏<span dir="ltr">1, 2, 3, 4, 5, 6</span> |
        | רגילות | ‏<span dir="ltr">0, 1, 2, 3, 4, 5</span> | ‏<span dir="ltr">0, 1, 2, 3, 4, 5</span> | ‏<span dir="ltr">3, 4, 5, 6, 7, 8</span> |
        | רגילות | ‏<span dir="ltr">0, 1, 2, 3, 4, 5</span> | ‏<span dir="ltr">1, 2, 3, 4, 5, 6</span> | ‏<span dir="ltr">2, 3, 4, 5, 6, 7</span> |
        | ‏Sicherman ורגילה | ‏<span dir="ltr">1, 2, 2, 3, 3, 4</span> | ‏<span dir="ltr">1, 2, 3, 4, 5, 6</span> | ‏<span dir="ltr">1, 3, 4, 5, 6, 8</span> |
        | ‏Sicherman ורגילה | ‏<span dir="ltr">0, 1, 1, 2, 2, 3</span> | ‏<span dir="ltr">0, 1, 2, 3, 4, 5</span> | ‏<span dir="ltr">3, 5, 6, 7, 8, 10</span> |
        | ‏Sicherman ורגילה | ‏<span dir="ltr">0, 1, 1, 2, 2, 3</span> | ‏<span dir="ltr">1, 2, 3, 4, 5, 6</span> | ‏<span dir="ltr">2, 4, 5, 6, 7, 9</span> |
        | ‏Sicherman ורגילה | ‏<span dir="ltr">0, 1, 1, 2, 2, 3</span> | ‏<span dir="ltr">2, 3, 4, 5, 6, 7</span> | ‏<span dir="ltr">1, 3, 4, 5, 6, 8</span> |
        | ‏Sicherman ורגילה | ‏<span dir="ltr">0, 1, 1, 2, 2, 3</span> | ‏<span dir="ltr">3, 4, 5, 6, 7, 8</span> | ‏<span dir="ltr">0, 2, 3, 4, 5, 7</span> |
        | ‏Sicherman ורגילה | ‏<span dir="ltr">1, 2, 2, 3, 3, 4</span> | ‏<span dir="ltr">0, 1, 2, 3, 4, 5</span> | ‏<span dir="ltr">2, 4, 5, 6, 7, 9</span> |
        | ‏Sicherman ורגילה | ‏<span dir="ltr">1, 2, 2, 3, 3, 4</span> | ‏<span dir="ltr">2, 3, 4, 5, 6, 7</span> | ‏<span dir="ltr">0, 2, 3, 4, 5, 7</span> |
        | ‏Sicherman ורגילה | ‏<span dir="ltr">2, 3, 3, 4, 4, 5</span> | ‏<span dir="ltr">0, 1, 2, 3, 4, 5</span> | ‏<span dir="ltr">1, 3, 4, 5, 6, 8</span> |
        | ‏Sicherman ורגילה | ‏<span dir="ltr">2, 3, 3, 4, 4, 5</span> | ‏<span dir="ltr">1, 2, 3, 4, 5, 6</span> | ‏<span dir="ltr">0, 2, 3, 4, 5, 7</span> |
        | ‏Sicherman ורגילה | ‏<span dir="ltr">3, 4, 4, 5, 5, 6</span> | ‏<span dir="ltr">0, 1, 2, 3, 4, 5</span> | ‏<span dir="ltr">0, 2, 3, 4, 5, 7</span> |

        <!-- /gen -->

        כך סופרים לכל \( k \) : לכל \( j \) מחלקים את ה-\( x \) בין שלושת סוגי הקוביות, ובתוך
        כל סוג לפי מספר הקוביות שלו. זה סכום, ולא נוסחה סגורה כמו \( \lfloor k/2 \rfloor + 1 \).
        עם שתי קוביות יוצאים חמשת הזוגות של סעיף ב :

        <!-- gen 9 -->

        | הקוביות k | הקבוצות, פאות חיוביות | הקבוצות, גם 0 |
        |:-:|:-:|:-:|
        | 2 | 2 | 5 |
        | 3 | 2 | 13 |
        | 4 | 3 | 41 |
        | 5 | 3 | 98 |
        | 6 | 4 | 250 |

        <!-- /gen -->

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="dice_sets" linenums="1" hl_lines="18 25"
        from itertools import combinations_with_replacement


        def same_sum_k(dice):
            """The sum of the dice is distributed as the sum of as many standard six-sided dice."""
            got, want = [1], [1]
            for d in dice:
                got = poly_mul(got, die_poly(d))
                want = poly_mul(want, die_poly(range(1, 7)))
            return got == want


        def dice_sets(k, low=1):
            """Every set of k six-sided dice, faces whole numbers from low up, whose sum is
            distributed as the sum of k standard dice; each set once, its dice in order."""
            kinds, p = [], [1, 2, 2, 1]                          # (1)!
            for e in range(k + 1):
                if min(p) >= 0:                                  # (2)!
                    kinds.append((e, p))
                p = poly_mul(p, [1, -1, 1])
            dice = [(e, a, faces_of([0] * a + p))                # (3)!
                    for a in range(low, k + 1) for e, p in kinds]
            sets = []
            for pick in combinations_with_replacement(dice, k):
                if sum(d[0] for d in pick) == k and sum(d[1] for d in pick) == k:   # (4)!
                    sets.append(tuple(d[2] for d in pick))
            return sets
        ```

        1. ‏\( (1 + x)(1 + x + x^2) = 1 + 2x + 2x^2 + x^3 \) : הגורמים שכל קובייה מקבלת אחד
           מכל אחד, בלי \( x \).
        2. הקוד לא מניח ש-\( e \le 2 \) : הוא מנסה כל \( e \) עד \( k \), ושומר רק פולינום
           בלי מקדם שלילי. נשארים 0, 1 ו-2.
        3. כל קובייה אפשרית : ‏\( x^a \) כפול אחד הסוגים. הלולאה על \( a \) בחוץ ועל \( e \)
           בפנים מסדרת את הקוביות לפי הפאות שלהן, ולכן כל קבוצה יוצאת פעם אחת, והקוביות שלה
           בסדר.
        4. ב-\( P(x)^k \) יש \( k \) עותקים של \( 1 - x + x^2 \) ו-\( k \) גורמים \( x \), והקבוצה
           לוקחת את כולם, לא פחות ולא יותר.

    === "SystemVerilog"
        ```systemverilog title="function automatic void dice_sets" linenums="1" hl_lines="37 51"
        // 1 when the sum of the dice is distributed as the sum of as many standard six-sided dice;
        // faces holds the dice one after another, six faces each
        function automatic bit same_sum_k(int faces[$]);
          int die[$], std[$] = '{1, 2, 3, 4, 5, 6};
          poly_t got = {1}, want = {1};
          if (faces.size() % 6 != 0) return 0;
          for (int d = 0; d < faces.size(); d += 6) begin
            die.delete();
            for (int j = 0; j < 6; j++) die.push_back(faces[d + j]);
            got = poly_mul(got, die_poly(die));
            want = poly_mul(want, die_poly(std));
          end
          if (got.size() != want.size()) return 0;
          foreach (got[s]) if (got[s] != want[s]) return 0;
          return 1;
        endfunction

        // The faces of a die polynomial as text, "1 2 2 3 3 4"
        function automatic string faces_text(poly_t c);
          poly_t f = faces_of(c);
          string s = "";
          foreach (f[i]) begin
            if (i > 0) s = {s, " "};
            s = {s, $sformatf("%0d", f[i])};
          end
          return s;
        endfunction

        // Every set of k six-sided dice, faces from low up, with the sum of k standard dice, as text,
        // "1 2 2 3 3 4 + 1 2 3 4 5 6 + 1 3 4 5 6 8": a die is x^a (1 + x)(1 + x + x^2)(1 - x + x^2)^e,
        // and a set takes k of them whose e's and a's both add up to k
        function automatic void dice_sets(int k, int low, ref string sets[$]);
          poly_t kind[int], p = {1, 2, 2, 1}, free = {1, -1, 1}, f;
          int ce[$], ca[$], pick[$], i, se, sa;
          string cf[$], line;
          for (int e = 0; e <= k; e++) begin
            if (is_die(p, 0)) kind[e] = p;                  // (1)!
            p = poly_mul(p, free);
          end
          for (int a = low; a <= k; a++) foreach (kind[e]) begin
            f = kind[e];                                    // (2)!
            repeat (a) f.push_front(0);
            ce.push_back(e); ca.push_back(a); cf.push_back(faces_text(f));
          end
          sets.delete();
          if (k < 1 || cf.size() == 0) return;
          repeat (k) pick.push_back(0);
          forever begin
            se = 0; sa = 0;
            foreach (pick[j]) begin se += ce[pick[j]]; sa += ca[pick[j]]; end
            if (se == k && sa == k) begin                   // (3)!
              line = cf[pick[0]];
              for (int j = 1; j < k; j++) line = {line, " + ", cf[pick[j]]};
              sets.push_back(line);
            end
            i = k - 1;                                      // the next list, as in dice_pairs
            while (i >= 0 && pick[i] == cf.size() - 1) i--;
            if (i < 0) break;
            pick[i]++;
            for (int j = i + 1; j < k; j++) pick[j] = pick[i];
          end
        endfunction
        ```

        1. כמו ב-Python : ‏`is_die(p, 0)` של סעיף א בודקת שאין לפולינום מקדם שלילי.
        2. ‏\( x^a \) מזיז את המקדמים ב-\( a \) מקומות. ‏\( a \) בחוץ ו-\( e \) בפנים, ולכן הקוביות
           מסודרות לפי הפאות שלהן.
        3. ה-\( e \) וה-\( a \) של הקבוצה מסתכמים ל-\( k \), כמו ב-Python.

    #### למה זה נכון { .sol-proof }

    **אחד מכל גורם קבוע.** כמו בסעיף א, כל קובייה מקבלת חלק מהגורמים של \( P(x)^k \), כי
    הפירוק יחיד. אין פאה 0, ולכן \( A(0) = 0 \) וכל קובייה מקבלת לפחות \( x \) אחד. יש \( k \)
    כאלה ל-\( k \) קוביות, ולכן בדיוק אחד לכל אחת. ‏\( A(1) = 6 = 2^i \cdot 3^j \) מחייב
    \( 1 + x \) אחד ו-\( 1 + x + x^2 \) אחד לכל קובייה, ו-\( k \) העותקים של כל אחד מהם
    מתחלקים כך בדיוק.

    **לכל היותר שני עותקים.** קובייה עם \( e \) עותקים של \( 1 - x + x^2 \) מתחילה כך :

    \[
    \begin{aligned}
    &x \, (1 + 2x + \dots)(1 - e x + \dots) \\
    &\quad = x + (2 - e) \, x^2 + \dots
    \end{aligned}
    \]

    המקדם של \( x^2 \) הוא מספר הפאות שעליהן 2, ולכן \( e \le 2 \). כש-\( e \) הוא 0, 1 או 2
    כל המקדמים לא שליליים, כמו בטבלה.

    **הספירה.** ה-\( e \) של הקוביות מסתכמים ל-\( k \), כל אחד מ-0 עד 2. אם \( j \) מהם 0
    ו-\( l \) מהם 2, אז \( (k - j - l) + 2l = k \), כלומר \( l = j \). כל \( j \) מ-0 עד
    \( \lfloor k/2 \rfloor \) נותן קבוצה אחת, \( j \) זוגות Sicherman ו-\( k - 2j \) קוביות
    רגילות, ו-\( j \) שונה נותן קבוצה אחרת. לכן יש \( \lfloor k/2 \rfloor + 1 \) קבוצות.

    **גם 0 על פאה.** ‏\( A(1) = 6 \) ו-\( e \le 2 \) לא תלויים בפאה הקטנה, ולכן הקוביות הן אותן
    שלוש, כל אחת כפול \( x^a \). הפאה הקטנה שלה היא \( a \ge 0 \), וה-\( a \) מסתכמים
    ל-\( k \). כל חלוקה כזו נותנת קבוצה, כי הזזה לא יוצרת מקדם שלילי. אם \( a \) אחד היה
    שלילי, הייתה פאה שלילית.

    **בדיקה בלי הפירוק.** ‏`dice_sets` נשענת על הפירוק. כדי לבדוק אותה בלעדיו, `same_sum_k`
    כופלת את הפולינומים של כל קבוצה שהיא מחזירה, וחיפוש מאפס מוצא את אותן 13 קבוצות של שלוש
    קוביות. החיפוש לוקח כל קובייה של 6 פאות מ-0 עד 18 שמחלקת את \( P(x)^3 \) בלי שארית, ואחר
    כך כל שתיים מהן.

    #### סיבוכיות { .sol-cost }

    עם פאות חיוביות יש שלוש קוביות אפשריות, ו-`dice_sets` עוברת על כל הבחירות של \( k \) מהן
    עם חזרות, \( \binom{k+2}{2} \) בחירות, ובכל אחת שני סכומים של \( k \) מספרים : זמן
    \( O(k^3) \). הזיכרון הוא בעיקר התשובה, \( \lfloor k/2 \rfloor + 1 \) קבוצות של \( k \)
    קוביות : \( O(k^2) \). כשמותר 0 יש \( 3(k + 1) \) קוביות אפשריות ו-\( \binom{4k+2}{k} \)
    בחירות, ול-\( k = 6 \) אלה 230,230 בחירות, פחות משנייה. חיפוש מאפס כמו בסעיף א עובר
    כבר בשלוש קוביות על 134,596 קוביות, כל הקוביות של 6 פאות מ-0 עד 18.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : בודק שמסתכל רק על הסכום"
    מחולל של שתי קוביות במודל אימות, ובודק שאוסף היסטוגרמה של הסכום ומשווה אותה למשולש, או
    covergroup עם coverpoint אחד על הסכום. באג שמחליף את הקוביות בקוביות Sicherman עובר את
    שניהם : ההתפלגות של הסכום זהה. בודקים כל קובייה לבד, שכל פאה 1 עד 6 יוצאת בשישית מהמקרים, ואת
    ההתפלגות המשותפת, 36 הזוגות, כשהקוביות צריכות להיות בלתי תלויות.

??? trap "מלכודת : לחפש רק בפאות 1 עד 6"
    חיפוש שמגביל כל פאה ל-1 עד 6 לא מוצא את Sicherman, כי יש בה 8. הגבול הנכון הוא 11 : הפאה
    הקטנה של הקובייה השנייה היא לפחות 1, והסכום הגדול הוא 12. בשלוש קוביות הגבול הוא 16, ואם
    מותר 0, הוא 18.

??? trap "מלכודת : לבדוק רק את מספר הפאות"
    חלוקה של הגורמים עם \( A(1) = 6 \) נותנת פולינום עם סכום מקדמים נכון, אבל לא תמיד קובייה :
    שלושה עותקים של \( 1 - x + x^2 \) לאותה קובייה נותנים סכום מקדמים 6, והמקדם של \( x^2 \)
    הוא \( -1 \). גם הגורם \( 1 - x + x^2 \) לבד הוא לא קובייה. בודקים כל מקדם.

??? trap "מלכודת : לספור קבוצה כמה פעמים"
    ‏(A, B) ו-(B, A) הם אותו זוג. חיפוש שעובר על כל A מוצא את Sicherman פעמיים, ואת הרגילות פעם
    אחת. עם שלוש קוביות, זוג Sicherman וקובייה רגילה נמצאים בשישה סדרים. שומרים סדר קבוע, למשל
    הקוביות מסודרות לפי הפאות שלהן.

??? followup "שאלות המשך"
    - **קוביות בגדלים שונים :** קובייה של 4 פאות וקובייה של 9 פאות, עם מספרים שלמים חיוביים.
      איך מקבלים את ההתפלגות של הסכום של שתי קוביות רגילות של 6 פאות?

        ??? fu-answer "תשובה"
            אותם גורמים, עם \( A(1) = 4 \) ו-\( B(1) = 9 \) : ל-A שני \( 1 + x \) ואף
            \( 1 + x + x^2 \). יש שלושה זוגות : \( \{1, 2, 2, 3\} \) עם
            \( \{1, 3, 3, 5, 5, 5, 7, 7, 9\} \), ‏\( \{1, 2, 4, 5\} \) עם
            \( \{1, 2, 3, 3, 4, 5, 5, 6, 7\} \), ו-\( \{1, 4, 4, 7\} \) עם
            \( \{1, 2, 2, 3, 3, 3, 4, 4, 5\} \).

    - **מספר פאות אחר :** שתי קוביות של \( n \) פאות, עם ההתפלגות של הסכום של שתי קוביות
      רגילות של \( n \) פאות. לאילו \( n \) יש זוג אחר מלבד הרגיל?

        ??? fu-answer "תשובה"
            בדיוק כש-\( n \) פריק. כש-\( n \) ראשוני, \( 1 + x + \dots + x^{n-1} \) לא מתפרק,
            ונשאר רק הזוג הרגיל. ל-\( n = 4 \) יש זוג אחד נוסף, \( \{1, 2, 2, 3\} \)
            ו-\( \{1, 3, 3, 5\} \), ול-\( n = 8 \) שלושה.

    - **‏covergroup :** איך כותבים covergroup למחולל של שתי קוביות כך שבאג של קוביות Sicherman
      יתגלה?

        ??? fu-answer "תשובה"
            ‏coverpoint לכל קובייה עם bin לכל ערך מ-1 עד 6, ו-illegal_bins לכל ערך אחר. עם
            קוביות Sicherman הפאה 8 של B נופלת ב-illegal_bins, ה-bins של 5 ו-6 של A ושל 2 של B
            נשארים ריקים, ו-cross של שני ה-coverpoints מראה 20 מתוך 36 זוגות בלבד. ה-coverpoint
            של הסכום לבד מגיע ל-100%.
