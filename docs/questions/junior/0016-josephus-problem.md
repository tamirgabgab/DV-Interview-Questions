---
id: 16
title: בעיית יוספוס – מי נשאר אחרון במעגל?
level: junior
difficulty: medium
tags: [algorithms, math, bitwise, python, systemverilog]
source: ""
added: 2026-10-18
---

## השאלה

‏\( n \) אנשים עומדים במעגל, וממוספרים מ-1 עד \( n \) עם כיוון השעון. מתחילים מאדם 1: הוא
**מדלג**, והאדם שאחריו **יוצא** מהמעגל. ממשיכים מהאדם הבא אחרי מי שיצא: הוא מדלג, והבא
אחריו יוצא. כך ממשיכים סביב המעגל, שוב ושוב, עד שנשאר אדם אחד: **השורד**.

במילים אחרות, כל שני יוצא. למשל, עבור \( n = 5 \) יוצאים לפי הסדר 2, 4, 1 ו-5, והשורד הוא
אדם 3. שימו לב שאדם 1 יוצא בסיבוב השני: אחרי שאדם 5 דילג, הבא בתור הוא שוב אדם 1.

השאלה נקראת על שם יוסף בן מתתיהו. לפי הסיפור, הוא עמד עם 40 לוחמים במערה ביודפת, ובחר
את המקום במעגל שבו יישאר אחרון. בסעיף ג נחזור למספרים שלו.

??? interviewer "מה המראיין בודק"
    - **מבנה הנתונים הנכון לסימולציה:** תור שבו האדם הראשון עובר לסוף או יוצא, ולא מערך
      שמוחקים ממנו איברים באמצע.
    - **חיפוש תבנית:** להריץ מקרים קטנים, לסדר אותם בטבלה ולזהות חוקיות, במקום לנחש
      נוסחה.
    - **הוכחה באינדוקציה:** להראות מה קורה אחרי סיבוב אחד שלם, ולהפריד בין \( n \) זוגי
      לאי-זוגי.
    - **חשיבה בביטים:** לראות שהנוסחה היא פעולה פשוטה על הייצוג הבינארי של \( n \), ושאפשר
      לממש אותה גם במעגל צירופי.
    - **הכללה:** לנסח נוסחת נסיגה לכל \( k \), דרך מספור מחדש של המעגל.

---

### סעיף א – סימולציה

כתבו פונקציה `josephus_sim(n)` שמחזירה את מספר השורד, על ידי סימולציה של המעגל.

??? tip "רמז 1"
    בכל צעד מטפלים רק באדם שנמצא "בתור": הוא מדלג, והבא אחריו יוצא. מי שמדלג חוזר למעגל
    אחרי כל האחרים. איזה מבנה נתונים מתנהג בדיוק כך?

??? tip "רמז 2"
    תור (queue): מוציאים את הראשון ומכניסים אותו לסוף, כי הוא דילג. את הבא מוציאים ולא
    מחזירים, כי הוא יצא. עוצרים כשנשאר איבר אחד.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מכניסים את 1 עד \( n \) לתור. כל עוד יש יותר מאדם אחד: הראשון עובר לסוף התור, והבא
        יוצא. מה שנשאר בתור הוא השורד. הזמן הוא \( O(n) \).

    #### הרעיון { .sol-idea }

    התור מחזיק את האנשים שעדיין במעגל, לפי הסדר שבו יגיע תורם. מי שמדלג עובר לסוף התור,
    וזה בדיוק מה שקורה במעגל: התור שלו יחזור אחרי כל השאר. מי שיוצא פשוט לא חוזר.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **אתחול:** מכניסים לתור את 1, 2, ..., \( n \). האדם הראשון בתור הוא זה שהתור שלו לדלג.
    2. **דילוג:** מוציאים את הראשון ומכניסים אותו לסוף.
    3. **יציאה:** מוציאים את הראשון החדש ולא מחזירים אותו.
    4. **עצירה:** חוזרים על שני הצעדים עד שנשאר בתור אדם אחד, ומחזירים אותו.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function josephus_sim" linenums="1" hl_lines="5 6"
        function automatic int josephus_sim(int n);
          int circle[$];   // (1)!
          for (int p = 1; p <= n; p++) circle.push_back(p);
          while (circle.size() > 1) begin
            circle.push_back(circle.pop_front());   // (2)!
            void'(circle.pop_front());              // the next one leaves the circle
          end
          return circle[0];
        endfunction
        ```

        1. תור (queue) של SystemVerilog, עם `push_back` ו-`pop_front` ב-\( O(1) \). הראש
           של התור הוא האדם שהתור שלו עכשיו.
        2. ‏`pop_front` מחזיר את האיבר שהוצא, ולכן אפשר להעביר אותו לסוף בשורה אחת. בשורה
           הבאה הערך שהוצא לא נחוץ, ו-`void'()` אומר במפורש שהוא נזרק.

    === "Python"
        ```python title="josephus_sim" linenums="1" hl_lines="7 8"
        from collections import deque


        def josephus_sim(n: int) -> int:
            circle = deque(range(1, n + 1))   # (1)!
            while len(circle) > 1:
                circle.append(circle.popleft())   # skips: back to the end of the queue
                circle.popleft()                  # the next one leaves the circle
            return circle[0]
        ```

        1. ‏`deque` מוציא מההתחלה ב-\( O(1) \). ברשימה רגילה `pop(0)` מזיז את כל האיברים
           שאחריו, וכל הסימולציה הייתה הופכת ל-\( O(n^2) \).

    #### למה זה נכון { .sol-proof }

    **המעגל צעד אחרי צעד.** לחצו "הבא" כדי לעקוב אחרי 10 אנשים. בכחול מי שמדלג, בכתום מי
    שיוצא, ובירוק השורד:

    <div class="stepper" role="group" aria-label="יוספוס עם 10 אנשים, כל שני יוצא" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-cell" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text></g><g><circle class="st-cell" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g><circle class="st-cell" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text></g><g><circle class="st-cell" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text></g><g><circle class="st-cell" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text></g><text class="st-text" x="150" y="146" text-anchor="middle">10</text></svg><figcaption>10 אנשים במעגל. סופרים מאדם 1, וכל שני יוצא. המספר במרכז הוא כמה אנשים נשארו.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-stack" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g><circle class="st-bad" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text><line class="pg-strike" x1="199.7" y1="67.1" x2="223.7" y2="43.1"/></g><g><circle class="st-cell" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g><circle class="st-cell" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text></g><g><circle class="st-cell" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text></g><g><circle class="st-cell" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text></g><text class="st-text" x="150" y="146" text-anchor="middle">9</text></svg><figcaption>יציאה 1: אדם 1 מדלג, ואדם 2 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-cell" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g class="st-faded"><circle class="st-done" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text><line class="pg-strike" x1="199.7" y1="67.1" x2="223.7" y2="43.1"/></g><g><circle class="st-stack" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text></g><g><circle class="st-bad" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text><line class="pg-strike" x1="237.9" y1="184.4" x2="261.9" y2="160.4"/></g><g><circle class="st-cell" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g><circle class="st-cell" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text></g><g><circle class="st-cell" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text></g><g><circle class="st-cell" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text></g><text class="st-text" x="150" y="146" text-anchor="middle">8</text></svg><figcaption>יציאה 2: אדם 3 מדלג, ואדם 4 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-cell" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g class="st-faded"><circle class="st-done" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text><line class="pg-strike" x1="199.7" y1="67.1" x2="223.7" y2="43.1"/></g><g><circle class="st-cell" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text><line class="pg-strike" x1="237.9" y1="184.4" x2="261.9" y2="160.4"/></g><g><circle class="st-stack" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g><circle class="st-bad" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text><line class="pg-strike" x1="138.0" y1="257.0" x2="162.0" y2="233.0"/></g><g><circle class="st-cell" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text></g><g><circle class="st-cell" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text></g><g><circle class="st-cell" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text></g><text class="st-text" x="150" y="146" text-anchor="middle">7</text></svg><figcaption>יציאה 3: אדם 5 מדלג, ואדם 6 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-cell" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g class="st-faded"><circle class="st-done" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text><line class="pg-strike" x1="199.7" y1="67.1" x2="223.7" y2="43.1"/></g><g><circle class="st-cell" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text><line class="pg-strike" x1="237.9" y1="184.4" x2="261.9" y2="160.4"/></g><g><circle class="st-cell" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-done" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text><line class="pg-strike" x1="138.0" y1="257.0" x2="162.0" y2="233.0"/></g><g><circle class="st-stack" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text></g><g><circle class="st-bad" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text><line class="pg-strike" x1="38.1" y1="184.4" x2="62.1" y2="160.4"/></g><g><circle class="st-cell" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text></g><g><circle class="st-cell" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text></g><text class="st-text" x="150" y="146" text-anchor="middle">6</text></svg><figcaption>יציאה 4: אדם 7 מדלג, ואדם 8 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-cell" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g class="st-faded"><circle class="st-done" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text><line class="pg-strike" x1="199.7" y1="67.1" x2="223.7" y2="43.1"/></g><g><circle class="st-cell" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text><line class="pg-strike" x1="237.9" y1="184.4" x2="261.9" y2="160.4"/></g><g><circle class="st-cell" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-done" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text><line class="pg-strike" x1="138.0" y1="257.0" x2="162.0" y2="233.0"/></g><g><circle class="st-cell" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-done" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text><line class="pg-strike" x1="38.1" y1="184.4" x2="62.1" y2="160.4"/></g><g><circle class="st-stack" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text></g><g><circle class="st-bad" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text><line class="pg-strike" x1="76.3" y1="67.1" x2="100.3" y2="43.1"/></g><text class="st-text" x="150" y="146" text-anchor="middle">5</text></svg><figcaption>יציאה 5: אדם 9 מדלג, ואדם 10 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-stack" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g class="st-faded"><circle class="st-done" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text><line class="pg-strike" x1="199.7" y1="67.1" x2="223.7" y2="43.1"/></g><g><circle class="st-bad" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text><line class="pg-strike" x1="237.9" y1="119.6" x2="261.9" y2="95.6"/></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text><line class="pg-strike" x1="237.9" y1="184.4" x2="261.9" y2="160.4"/></g><g><circle class="st-cell" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-done" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text><line class="pg-strike" x1="138.0" y1="257.0" x2="162.0" y2="233.0"/></g><g><circle class="st-cell" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text></g><g class="st-faded"><circle class="st-done" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text><line class="pg-strike" x1="38.1" y1="184.4" x2="62.1" y2="160.4"/></g><g><circle class="st-cell" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text></g><g class="st-faded"><circle class="st-done" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text><line class="pg-strike" x1="76.3" y1="67.1" x2="100.3" y2="43.1"/></g><text class="st-text" x="150" y="146" text-anchor="middle">4</text></svg><figcaption>יציאה 6: אדם 1 מדלג, ואדם 3 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-cell" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g class="st-faded"><circle class="st-done" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text><line class="pg-strike" x1="199.7" y1="67.1" x2="223.7" y2="43.1"/></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text><line class="pg-strike" x1="237.9" y1="119.6" x2="261.9" y2="95.6"/></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text><line class="pg-strike" x1="237.9" y1="184.4" x2="261.9" y2="160.4"/></g><g><circle class="st-stack" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-done" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text><line class="pg-strike" x1="138.0" y1="257.0" x2="162.0" y2="233.0"/></g><g><circle class="st-bad" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text><line class="pg-strike" x1="76.3" y1="236.9" x2="100.3" y2="212.9"/></g><g class="st-faded"><circle class="st-done" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text><line class="pg-strike" x1="38.1" y1="184.4" x2="62.1" y2="160.4"/></g><g><circle class="st-cell" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text></g><g class="st-faded"><circle class="st-done" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text><line class="pg-strike" x1="76.3" y1="67.1" x2="100.3" y2="43.1"/></g><text class="st-text" x="150" y="146" text-anchor="middle">3</text></svg><figcaption>יציאה 7: אדם 5 מדלג, ואדם 7 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-bad" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text><line class="pg-strike" x1="138.0" y1="47.0" x2="162.0" y2="23.0"/></g><g class="st-faded"><circle class="st-done" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text><line class="pg-strike" x1="199.7" y1="67.1" x2="223.7" y2="43.1"/></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text><line class="pg-strike" x1="237.9" y1="119.6" x2="261.9" y2="95.6"/></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text><line class="pg-strike" x1="237.9" y1="184.4" x2="261.9" y2="160.4"/></g><g><circle class="st-cell" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-done" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text><line class="pg-strike" x1="138.0" y1="257.0" x2="162.0" y2="233.0"/></g><g class="st-faded"><circle class="st-done" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text><line class="pg-strike" x1="76.3" y1="236.9" x2="100.3" y2="212.9"/></g><g class="st-faded"><circle class="st-done" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text><line class="pg-strike" x1="38.1" y1="184.4" x2="62.1" y2="160.4"/></g><g><circle class="st-stack" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text></g><g class="st-faded"><circle class="st-done" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text><line class="pg-strike" x1="76.3" y1="67.1" x2="100.3" y2="43.1"/></g><text class="st-text" x="150" y="146" text-anchor="middle">2</text></svg><figcaption>יציאה 8: אדם 9 מדלג, ואדם 1 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g class="st-faded"><circle class="st-done" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text><line class="pg-strike" x1="138.0" y1="47.0" x2="162.0" y2="23.0"/></g><g class="st-faded"><circle class="st-done" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text><line class="pg-strike" x1="199.7" y1="67.1" x2="223.7" y2="43.1"/></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text><line class="pg-strike" x1="237.9" y1="119.6" x2="261.9" y2="95.6"/></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text><line class="pg-strike" x1="237.9" y1="184.4" x2="261.9" y2="160.4"/></g><g><circle class="st-stack" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-done" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text><line class="pg-strike" x1="138.0" y1="257.0" x2="162.0" y2="233.0"/></g><g class="st-faded"><circle class="st-done" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text><line class="pg-strike" x1="76.3" y1="236.9" x2="100.3" y2="212.9"/></g><g class="st-faded"><circle class="st-done" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text><line class="pg-strike" x1="38.1" y1="184.4" x2="62.1" y2="160.4"/></g><g><circle class="st-bad" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text><line class="pg-strike" x1="38.1" y1="119.6" x2="62.1" y2="95.6"/></g><g class="st-faded"><circle class="st-done" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text><line class="pg-strike" x1="76.3" y1="67.1" x2="100.3" y2="43.1"/></g><text class="st-text" x="150" y="146" text-anchor="middle">1</text></svg><figcaption>יציאה 9: אדם 5 מדלג, ואדם 9 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="10 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g class="st-faded"><circle class="st-done" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text><line class="pg-strike" x1="138.0" y1="47.0" x2="162.0" y2="23.0"/></g><g class="st-faded"><circle class="st-done" cx="211.7" cy="55.1" r="17"/><text class="st-text" x="211.7" y="60.1" text-anchor="middle">2</text><line class="pg-strike" x1="199.7" y1="67.1" x2="223.7" y2="43.1"/></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="107.6" r="17"/><text class="st-text" x="249.9" y="112.6" text-anchor="middle">3</text><line class="pg-strike" x1="237.9" y1="119.6" x2="261.9" y2="95.6"/></g><g class="st-faded"><circle class="st-done" cx="249.9" cy="172.4" r="17"/><text class="st-text" x="249.9" y="177.4" text-anchor="middle">4</text><line class="pg-strike" x1="237.9" y1="184.4" x2="261.9" y2="160.4"/></g><g><circle class="st-ok" cx="211.7" cy="224.9" r="17"/><text class="st-text" x="211.7" y="229.9" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-done" cx="150.0" cy="245.0" r="17"/><text class="st-text" x="150.0" y="250.0" text-anchor="middle">6</text><line class="pg-strike" x1="138.0" y1="257.0" x2="162.0" y2="233.0"/></g><g class="st-faded"><circle class="st-done" cx="88.3" cy="224.9" r="17"/><text class="st-text" x="88.3" y="229.9" text-anchor="middle">7</text><line class="pg-strike" x1="76.3" y1="236.9" x2="100.3" y2="212.9"/></g><g class="st-faded"><circle class="st-done" cx="50.1" cy="172.4" r="17"/><text class="st-text" x="50.1" y="177.4" text-anchor="middle">8</text><line class="pg-strike" x1="38.1" y1="184.4" x2="62.1" y2="160.4"/></g><g class="st-faded"><circle class="st-done" cx="50.1" cy="107.6" r="17"/><text class="st-text" x="50.1" y="112.6" text-anchor="middle">9</text><line class="pg-strike" x1="38.1" y1="119.6" x2="62.1" y2="95.6"/></g><g class="st-faded"><circle class="st-done" cx="88.3" cy="55.1" r="17"/><text class="st-text" x="88.3" y="60.1" text-anchor="middle">10</text><line class="pg-strike" x1="76.3" y1="67.1" x2="100.3" y2="43.1"/></g><text class="st-text" x="150" y="146" text-anchor="middle">1</text></svg><figcaption>נשאר אדם 5. הוא השורד.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="11"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    בכל צעד התור מכיל בדיוק את מי שעוד במעגל, מהאדם שהתור שלו עכשיו ועם כיוון השעון. דילוג
    מעביר את הראשון לסוף ושומר על הסדר הזה, ויציאה מוחקת את הראשון. לכן התור מתנהג
    בדיוק כמו המעגל, והאיבר האחרון שנשאר הוא השורד.

    #### סיבוכיות { .sol-cost }

    - **זמן:** \( O(n) \). יש \( n - 1 \) יציאות, וכל אחת עולה שתי פעולות תור.
    - **זיכרון:** \( O(n) \) לתור.

---

### סעיף ב – נוסחה סגורה

הריצו את הסימולציה על \( n = 1, 2, \ldots, 16 \). איזו תבנית אתם רואים? מצאו נוסחה
לשורד, הוכיחו אותה, וכתבו פונקציה שמחשבת אותו בלי סימולציה.

??? tip "רמז 1"
    הסתכלו על הערכים של \( n \) שבהם השורד הוא 1. מה משותף להם? ומה קורה לשורד בין שניים
    כאלה?

??? tip "רמז 2"
    מה נשאר אחרי סיבוב אחד שלם סביב המעגל, כש-\( n \) זוגי? וכש-\( n \) אי-זוגי? בשני
    המקרים נשארת אותה בעיה בגודל חצי, רק עם מספרים אחרים.

??? tip "רמז 3"
    כתבו את \( n \) ואת השורד בבינארי, אחד ליד השני.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        כותבים \( n = 2^m + L \), כש-\( 2^m \) היא החזקה הגדולה ביותר של 2 שלא גדולה
        מ-\( n \), ו-\( 0 \le L < 2^m \). השורד הוא \( J(n) = 2L + 1 \). בבינארי: **מעבירים
        את הביט העליון של \( n \) לסוף**. למשל, \( 41 = 32 + 9 \), והשורד הוא 19.

    #### הרעיון { .sol-idea }

    הטבלה מראה שבכל חזקה של 2 השורד הוא 1, ומשם הוא עולה ב-2 עם כל אדם נוסף, עד החזקה
    הבאה. למה בחזקה של 2 השורד הוא 1? כשמספר האנשים זוגי, סיבוב שלם מוציא בדיוק חצי
    מהם, והאחרון שיוצא הוא האחרון במעגל. לכן הסיבוב הבא מתחיל שוב מאותו אדם. בחזקה של 2
    זה קורה בכל סיבוב, עד שנשאר רק מי שהתחיל.

    ומכאן לכל \( n = 2^m + L \): אחרי \( L \) יציאות יצאו \( 2, 4, \ldots, 2L \), ונשארו
    בדיוק \( 2^m \) אנשים. הספירה ממשיכה מאדם \( 2L + 1 \), וכמו שראינו, במעגל של חזקה של
    2 מי שמתחיל הוא השורד.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **טבלה:** מריצים את הסימולציה על מקרים קטנים ומזהים את התבנית.
    2. **סיבוב אחד, \( n \) זוגי:** יוצאים כל הזוגיים, והבעיה חוזרת עם חצי מהאנשים.
    3. **סיבוב אחד, \( n \) אי-זוגי:** יוצאים כל הזוגיים ואחריהם אדם 1, וגם כאן נשארת בעיה
       בגודל חצי.
    4. **אינדוקציה:** משתי נוסחאות הנסיגה מוכיחים ש-\( J(n) = 2L + 1 \).
    5. **ביטים:** מתרגמים את \( 2L + 1 \) לפעולה על הייצוג הבינארי.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="functions josephus_formula and josephus_bits" linenums="1" hl_lines="4 10"
        function automatic int josephus_formula(int n);
          int top = 1;                     // 2^m: the largest power of 2 that is <= n
          while (top <= n / 2) top *= 2;   // (1)!
          return 2 * (n - top) + 1;        // n = 2^m + L  ->  2L + 1
        endfunction

        function automatic int josephus_bits(int n);
          int top = 1;
          while (top <= n / 2) top *= 2;
          return ((n ^ top) << 1) | 1;   // (2)!
        endfunction
        ```

        1. הלולאה רצה \( m \) פעמים, כלומר \( O(\log n) \). התנאי הוא `top <= n / 2` ולא
           `2 * top <= n`: עבור \( n \ge 2^{30} \) ההכפלה גולשת ב-`int` של 32 ביט, והלולאה
           לא נעצרת. בחומרה זה **מגלה ה-1 העליון** (leading-one detector), מעגל צירופי
           שנותן את התשובה בבת אחת.
        2. ‏`n ^ top` מוחק את הביט העליון ומשאיר את \( L \). ההזזה שמאלה מכפילה ב-2, ו-`| 1`
           מוסיף 1 בסוף. יחד זה בדיוק "להעביר את הביט העליון לסוף".

    === "Python"
        ```python title="josephus_formula and josephus_bits" linenums="1" hl_lines="3 8"
        def josephus_formula(n: int) -> int:
            top = 1 << (n.bit_length() - 1)   # (1)!
            return 2 * (n - top) + 1          # n = 2^m + L  ->  2L + 1


        def josephus_bits(n: int) -> int:
            top = 1 << (n.bit_length() - 1)
            return ((n ^ top) << 1) | 1   # (2)!
        ```

        1. ‏`bit_length()` הוא מספר הביטים של \( n \), כלומר \( m + 1 \). לכן `1 << m` היא
           החזקה \( 2^m \), בלי לולאה.
        2. מוחקים את הביט העליון, מכפילים ב-2 ומוסיפים 1: אותה פעולה כמו בגרסת
           ה-SystemVerilog.

    #### למה זה נכון { .sol-proof }

    **התבנית.** הסימולציה על \( n = 1 \) עד 16:

    | ‏\( n \) | בבינארי | ‏\( 2^m + L \) | השורד |
    |---|---|---|---|
    | 1 | ‏`1` | ‏\( 1 + 0 \) | **1** |
    | 2 | ‏`10` | ‏\( 2 + 0 \) | **1** |
    | 3 | ‏`11` | ‏\( 2 + 1 \) | **3** |
    | 4 | ‏`100` | ‏\( 4 + 0 \) | **1** |
    | 5 | ‏`101` | ‏\( 4 + 1 \) | **3** |
    | 6 | ‏`110` | ‏\( 4 + 2 \) | **5** |
    | 7 | ‏`111` | ‏\( 4 + 3 \) | **7** |
    | 8 | ‏`1000` | ‏\( 8 + 0 \) | **1** |
    | 9 | ‏`1001` | ‏\( 8 + 1 \) | **3** |
    | 10 | ‏`1010` | ‏\( 8 + 2 \) | **5** |
    | 11 | ‏`1011` | ‏\( 8 + 3 \) | **7** |
    | 12 | ‏`1100` | ‏\( 8 + 4 \) | **9** |
    | 13 | ‏`1101` | ‏\( 8 + 5 \) | **11** |
    | 14 | ‏`1110` | ‏\( 8 + 6 \) | **13** |
    | 15 | ‏`1111` | ‏\( 8 + 7 \) | **15** |
    | 16 | ‏`10000` | ‏\( 16 + 0 \) | **1** |

    **אותם ערכים בגרף**, עד \( n = 40 \). השורד עולה ב-2 עם כל אדם נוסף, ונופל ל-1 בכל
    חזקה של 2, כשהוא פוגש את הקו \( J = n \):

    <span class="viz-legend"><span><i class="s1"></i>השורד</span><span><i class="s2"></i>חזקה של 2: השורד הוא 1</span><span><i class="ink"></i>הקו \( J = n \)</span></span>

    <svg class="perf-chart" viewBox="0 0 640 290" role="img" aria-label="השורד כפונקציה של מספר האנשים, מ-1 עד 40"><line class="grid" x1="44" x2="624" y1="250.0" y2="250.0"/><text class="tick" x="36" y="254.0" text-anchor="end">0</text><line class="grid" x1="44" x2="624" y1="202.8" y2="202.8"/><text class="tick" x="36" y="206.8" text-anchor="end">8</text><line class="grid" x1="44" x2="624" y1="155.6" y2="155.6"/><text class="tick" x="36" y="159.6" text-anchor="end">16</text><line class="grid" x1="44" x2="624" y1="108.4" y2="108.4"/><text class="tick" x="36" y="112.4" text-anchor="end">24</text><line class="grid" x1="44" x2="624" y1="61.2" y2="61.2"/><text class="tick" x="36" y="65.2" text-anchor="end">32</text><line class="grid" x1="44" x2="624" y1="14.0" y2="14.0"/><text class="tick" x="36" y="18.0" text-anchor="end">40</text><line class="ink-line" x1="44.0" y1="250.0" x2="624.0" y2="14.0" stroke-width="1.2" stroke-dasharray="5 4"/><line class="s1-line" x1="65.8" y1="244.1" x2="80.2" y2="232.3" stroke-width="1.5"/><line class="s1-line" x1="94.8" y1="244.1" x2="109.2" y2="232.3" stroke-width="1.5"/><line class="s1-line" x1="109.2" y1="232.3" x2="123.8" y2="220.5" stroke-width="1.5"/><line class="s1-line" x1="123.8" y1="220.5" x2="138.2" y2="208.7" stroke-width="1.5"/><line class="s1-line" x1="152.8" y1="244.1" x2="167.2" y2="232.3" stroke-width="1.5"/><line class="s1-line" x1="167.2" y1="232.3" x2="181.8" y2="220.5" stroke-width="1.5"/><line class="s1-line" x1="181.8" y1="220.5" x2="196.2" y2="208.7" stroke-width="1.5"/><line class="s1-line" x1="196.2" y1="208.7" x2="210.8" y2="196.9" stroke-width="1.5"/><line class="s1-line" x1="210.8" y1="196.9" x2="225.2" y2="185.1" stroke-width="1.5"/><line class="s1-line" x1="225.2" y1="185.1" x2="239.8" y2="173.3" stroke-width="1.5"/><line class="s1-line" x1="239.8" y1="173.3" x2="254.2" y2="161.5" stroke-width="1.5"/><line class="s1-line" x1="268.8" y1="244.1" x2="283.2" y2="232.3" stroke-width="1.5"/><line class="s1-line" x1="283.2" y1="232.3" x2="297.8" y2="220.5" stroke-width="1.5"/><line class="s1-line" x1="297.8" y1="220.5" x2="312.2" y2="208.7" stroke-width="1.5"/><line class="s1-line" x1="312.2" y1="208.7" x2="326.8" y2="196.9" stroke-width="1.5"/><line class="s1-line" x1="326.8" y1="196.9" x2="341.2" y2="185.1" stroke-width="1.5"/><line class="s1-line" x1="341.2" y1="185.1" x2="355.8" y2="173.3" stroke-width="1.5"/><line class="s1-line" x1="355.8" y1="173.3" x2="370.2" y2="161.5" stroke-width="1.5"/><line class="s1-line" x1="370.2" y1="161.5" x2="384.8" y2="149.7" stroke-width="1.5"/><line class="s1-line" x1="384.8" y1="149.7" x2="399.2" y2="137.9" stroke-width="1.5"/><line class="s1-line" x1="399.2" y1="137.9" x2="413.8" y2="126.1" stroke-width="1.5"/><line class="s1-line" x1="413.8" y1="126.1" x2="428.2" y2="114.3" stroke-width="1.5"/><line class="s1-line" x1="428.2" y1="114.3" x2="442.8" y2="102.5" stroke-width="1.5"/><line class="s1-line" x1="442.8" y1="102.5" x2="457.2" y2="90.7" stroke-width="1.5"/><line class="s1-line" x1="457.2" y1="90.7" x2="471.8" y2="78.9" stroke-width="1.5"/><line class="s1-line" x1="471.8" y1="78.9" x2="486.2" y2="67.1" stroke-width="1.5"/><line class="s1-line" x1="500.8" y1="244.1" x2="515.2" y2="232.3" stroke-width="1.5"/><line class="s1-line" x1="515.2" y1="232.3" x2="529.8" y2="220.5" stroke-width="1.5"/><line class="s1-line" x1="529.8" y1="220.5" x2="544.2" y2="208.7" stroke-width="1.5"/><line class="s1-line" x1="544.2" y1="208.7" x2="558.8" y2="196.9" stroke-width="1.5"/><line class="s1-line" x1="558.8" y1="196.9" x2="573.2" y2="185.1" stroke-width="1.5"/><line class="s1-line" x1="573.2" y1="185.1" x2="587.8" y2="173.3" stroke-width="1.5"/><line class="s1-line" x1="587.8" y1="173.3" x2="602.2" y2="161.5" stroke-width="1.5"/><line class="s1-line" x1="602.2" y1="161.5" x2="616.8" y2="149.7" stroke-width="1.5"/><circle class="s2-dot" cx="51.2" cy="244.1" r="4.5"><title>n = 1: 1</title></circle><text class="tick" x="51.2" y="268" text-anchor="middle">1</text><circle class="s2-dot" cx="65.8" cy="244.1" r="4.5"><title>n = 2: 1</title></circle><circle class="s1-dot" cx="80.2" cy="232.3" r="4.5"><title>n = 3: 3</title></circle><circle class="s2-dot" cx="94.8" cy="244.1" r="4.5"><title>n = 4: 1</title></circle><text class="tick" x="94.8" y="268" text-anchor="middle">4</text><circle class="s1-dot" cx="109.2" cy="232.3" r="4.5"><title>n = 5: 3</title></circle><circle class="s1-dot" cx="123.8" cy="220.5" r="4.5"><title>n = 6: 5</title></circle><circle class="s1-dot" cx="138.2" cy="208.7" r="4.5"><title>n = 7: 7</title></circle><circle class="s2-dot" cx="152.8" cy="244.1" r="4.5"><title>n = 8: 1</title></circle><text class="tick" x="152.8" y="268" text-anchor="middle">8</text><circle class="s1-dot" cx="167.2" cy="232.3" r="4.5"><title>n = 9: 3</title></circle><circle class="s1-dot" cx="181.8" cy="220.5" r="4.5"><title>n = 10: 5</title></circle><circle class="s1-dot" cx="196.2" cy="208.7" r="4.5"><title>n = 11: 7</title></circle><circle class="s1-dot" cx="210.8" cy="196.9" r="4.5"><title>n = 12: 9</title></circle><text class="tick" x="210.8" y="268" text-anchor="middle">12</text><circle class="s1-dot" cx="225.2" cy="185.1" r="4.5"><title>n = 13: 11</title></circle><circle class="s1-dot" cx="239.8" cy="173.3" r="4.5"><title>n = 14: 13</title></circle><circle class="s1-dot" cx="254.2" cy="161.5" r="4.5"><title>n = 15: 15</title></circle><circle class="s2-dot" cx="268.8" cy="244.1" r="4.5"><title>n = 16: 1</title></circle><text class="tick" x="268.8" y="268" text-anchor="middle">16</text><circle class="s1-dot" cx="283.2" cy="232.3" r="4.5"><title>n = 17: 3</title></circle><circle class="s1-dot" cx="297.8" cy="220.5" r="4.5"><title>n = 18: 5</title></circle><circle class="s1-dot" cx="312.2" cy="208.7" r="4.5"><title>n = 19: 7</title></circle><circle class="s1-dot" cx="326.8" cy="196.9" r="4.5"><title>n = 20: 9</title></circle><text class="tick" x="326.8" y="268" text-anchor="middle">20</text><circle class="s1-dot" cx="341.2" cy="185.1" r="4.5"><title>n = 21: 11</title></circle><circle class="s1-dot" cx="355.8" cy="173.3" r="4.5"><title>n = 22: 13</title></circle><circle class="s1-dot" cx="370.2" cy="161.5" r="4.5"><title>n = 23: 15</title></circle><circle class="s1-dot" cx="384.8" cy="149.7" r="4.5"><title>n = 24: 17</title></circle><text class="tick" x="384.8" y="268" text-anchor="middle">24</text><circle class="s1-dot" cx="399.2" cy="137.9" r="4.5"><title>n = 25: 19</title></circle><circle class="s1-dot" cx="413.8" cy="126.1" r="4.5"><title>n = 26: 21</title></circle><circle class="s1-dot" cx="428.2" cy="114.3" r="4.5"><title>n = 27: 23</title></circle><circle class="s1-dot" cx="442.8" cy="102.5" r="4.5"><title>n = 28: 25</title></circle><text class="tick" x="442.8" y="268" text-anchor="middle">28</text><circle class="s1-dot" cx="457.2" cy="90.7" r="4.5"><title>n = 29: 27</title></circle><circle class="s1-dot" cx="471.8" cy="78.9" r="4.5"><title>n = 30: 29</title></circle><circle class="s1-dot" cx="486.2" cy="67.1" r="4.5"><title>n = 31: 31</title></circle><circle class="s2-dot" cx="500.8" cy="244.1" r="4.5"><title>n = 32: 1</title></circle><text class="tick" x="500.8" y="268" text-anchor="middle">32</text><circle class="s1-dot" cx="515.2" cy="232.3" r="4.5"><title>n = 33: 3</title></circle><circle class="s1-dot" cx="529.8" cy="220.5" r="4.5"><title>n = 34: 5</title></circle><circle class="s1-dot" cx="544.2" cy="208.7" r="4.5"><title>n = 35: 7</title></circle><circle class="s1-dot" cx="558.8" cy="196.9" r="4.5"><title>n = 36: 9</title></circle><text class="tick" x="558.8" y="268" text-anchor="middle">36</text><circle class="s1-dot" cx="573.2" cy="185.1" r="4.5"><title>n = 37: 11</title></circle><circle class="s1-dot" cx="587.8" cy="173.3" r="4.5"><title>n = 38: 13</title></circle><circle class="s1-dot" cx="602.2" cy="161.5" r="4.5"><title>n = 39: 15</title></circle><circle class="s1-dot" cx="616.8" cy="149.7" r="4.5"><title>n = 40: 17</title></circle><text class="tick" x="616.8" y="268" text-anchor="middle">40</text><line class="axis" x1="44" x2="624" y1="250" y2="250"/><text class="tick" x="342" y="286" text-anchor="middle">n</text></svg>

    **סיבוב אחד שלם.** אחרי הסיבוב הראשון נשארים כל האי-זוגיים, והספירה ממשיכה מהאדם
    שאחרי מי שיצא אחרון. נותנים להם מספרים חדשים לפי הסדר של הספירה: הראשון ברשימה מקבל
    את המספר 1, השני את 2, וכן הלאה.

    | ‏\( n \) | יוצאים | נשארים, לפי הסדר |
    |---|---|---|
    | 10 | 2, 4, 6, 8, 10 | 1, 3, 5, 7, 9 |
    | 11 | 2, 4, 6, 8, 10, 1 | 3, 5, 7, 9, 11 |

    - **‏\( n = 2j \) זוגי:** יוצאים \( 2, 4, \ldots, 2j \), והספירה ממשיכה מאדם 1. נשארים
      \( j \) אנשים, ואדם עם המספר החדש \( i \) הוא אדם \( 2i - 1 \) במספור הישן.
    - **‏\( n = 2j + 1 \) אי-זוגי:** יוצאים \( 2, 4, \ldots, 2j \), אדם \( 2j + 1 \) מדלג, ואדם
      1 יוצא. הספירה ממשיכה מאדם 3, ואדם עם המספר החדש \( i \) הוא אדם \( 2i + 1 \).

    מכאן שתי נוסחאות נסיגה:

    \[
    \begin{aligned}
    J(1) &= 1 \\
    J(2j) &= 2J(j) - 1 \\
    J(2j + 1) &= 2J(j) + 1
    \end{aligned}
    \]

    **האינדוקציה.** עבור \( n = 1 \): ‏\( m = 0 \), ‏\( L = 0 \), ו-\( J(1) = 1 = 2L + 1 \).
    נניח שהנוסחה נכונה לכל מספר קטן מ-\( n \), ונכתוב \( n = 2^m + L \) עם \( m \ge 1 \):

    - **‏\( n \) זוגי:** גם \( L \) זוגי, ו-\( j = n / 2 = 2^{m-1} + L/2 \). לפי ההנחה
      \( J(j) = L + 1 \), ולכן \( J(n) = 2(L + 1) - 1 = 2L + 1 \).
    - **‏\( n \) אי-זוגי:** ‏\( L \) אי-זוגי, ו-\( j = (n - 1)/2 = 2^{m-1} + (L - 1)/2 \). לפי
      ההנחה \( J(j) = L \), ולכן \( J(n) = 2L + 1 \).

    **בביטים.** בבינארי, \( n \) הוא 1 ואחריו \( m \) ביטים, ואלה בדיוק הביטים של \( L \).
    הכפלה ב-2 מזיזה אותם שמאלה, והוספת 1 כותבת 1 בסוף. כלומר הביט העליון עבר מההתחלה
    לסוף:

    <svg class="figure" viewBox="0 0 618 196" style="max-width:39rem" role="img" aria-label="הסיבוב של הביטים: הביט העליון של n עובר לסוף, והתוצאה היא השורד"><defs><marker id="q16-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q16-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="legend" x="58" y="34" text-anchor="end">10</text><rect class="st-bad" x="70" y="14" width="30" height="30" rx="4"/><text class="st-text" x="85.0" y="35" text-anchor="middle">1</text><rect class="st-cell" x="104" y="14" width="30" height="30" rx="4"/><text class="st-text" x="119.0" y="35" text-anchor="middle">0</text><rect class="st-cell" x="138" y="14" width="30" height="30" rx="4"/><text class="st-text" x="153.0" y="35" text-anchor="middle">1</text><rect class="st-cell" x="172" y="14" width="30" height="30" rx="4"/><text class="st-text" x="187.0" y="35" text-anchor="middle">0</text><rect class="st-cell" x="296" y="14" width="30" height="30" rx="4"/><text class="st-text" x="311.0" y="35" text-anchor="middle">0</text><rect class="st-cell" x="330" y="14" width="30" height="30" rx="4"/><text class="st-text" x="345.0" y="35" text-anchor="middle">1</text><rect class="st-cell" x="364" y="14" width="30" height="30" rx="4"/><text class="st-text" x="379.0" y="35" text-anchor="middle">0</text><rect class="st-ok" x="398" y="14" width="30" height="30" rx="4"/><text class="st-text" x="413.0" y="35" text-anchor="middle">1</text><text class="legend" x="440" y="34">5</text><line class="ink-line" x1="218" y1="29.0" x2="282" y2="29.0" stroke-width="1.5" marker-end="url(#q16-ink)"/><path class="s2-line" d="M85.0,48 C85.0,84 413.0,84 413.0,50" fill="none" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#q16-s2)"/><text class="legend" x="58" y="120" text-anchor="end">41</text><rect class="st-bad" x="70" y="100" width="30" height="30" rx="4"/><text class="st-text" x="85.0" y="121" text-anchor="middle">1</text><rect class="st-cell" x="104" y="100" width="30" height="30" rx="4"/><text class="st-text" x="119.0" y="121" text-anchor="middle">0</text><rect class="st-cell" x="138" y="100" width="30" height="30" rx="4"/><text class="st-text" x="153.0" y="121" text-anchor="middle">1</text><rect class="st-cell" x="172" y="100" width="30" height="30" rx="4"/><text class="st-text" x="187.0" y="121" text-anchor="middle">0</text><rect class="st-cell" x="206" y="100" width="30" height="30" rx="4"/><text class="st-text" x="221.0" y="121" text-anchor="middle">0</text><rect class="st-cell" x="240" y="100" width="30" height="30" rx="4"/><text class="st-text" x="255.0" y="121" text-anchor="middle">1</text><rect class="st-cell" x="364" y="100" width="30" height="30" rx="4"/><text class="st-text" x="379.0" y="121" text-anchor="middle">0</text><rect class="st-cell" x="398" y="100" width="30" height="30" rx="4"/><text class="st-text" x="413.0" y="121" text-anchor="middle">1</text><rect class="st-cell" x="432" y="100" width="30" height="30" rx="4"/><text class="st-text" x="447.0" y="121" text-anchor="middle">0</text><rect class="st-cell" x="466" y="100" width="30" height="30" rx="4"/><text class="st-text" x="481.0" y="121" text-anchor="middle">0</text><rect class="st-cell" x="500" y="100" width="30" height="30" rx="4"/><text class="st-text" x="515.0" y="121" text-anchor="middle">1</text><rect class="st-ok" x="534" y="100" width="30" height="30" rx="4"/><text class="st-text" x="549.0" y="121" text-anchor="middle">1</text><text class="legend" x="576" y="120">19</text><line class="ink-line" x1="286" y1="115.0" x2="350" y2="115.0" stroke-width="1.5" marker-end="url(#q16-ink)"/><path class="s2-line" d="M85.0,134 C85.0,170 549.0,170 549.0,136" fill="none" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#q16-s2)"/></svg>

    #### סיבוכיות { .sol-cost }

    - **זמן:** \( O(\log n) \) עם הלולאה, ו-\( O(1) \) עם `bit_length()` או עם הוראת
      מעבד שסופרת אפסים מובילים. לעומת \( O(n) \) בסימולציה.
    - **זיכרון:** \( O(1) \).
    - **בחומרה:** מגלה 1 עליון, מחיקה של הביט שנמצא ו-shift, כולם צירופיים. השורד מחושב
      במחזור שעון אחד, לכל \( n \).

---

### סעיף ג – כל \( k \)-י יוצא

עכשיו סופרים \( k \) אנשים, והאחרון בספירה יוצא. הספירה מתחילה מאדם 1, ואחרי כל יציאה
היא מתחילה מחדש מהאדם הבא. עבור \( k = 2 \) זו הבעיה מסעיפים א ו-ב.

כתבו סימולציה לכל \( k \), ואחר כך פתרון בזמן \( O(n) \) ובזיכרון \( O(1) \), בלי
סימולציה.

??? tip "רמז 1"
    אחרי שהראשון יוצא נשארים \( n - 1 \) אנשים, והספירה מתחילה מהאדם שאחריו. זו אותה
    בעיה בגודל \( n - 1 \), רק במספור אחר.

??? tip "רמז 2"
    מספרו את המקומות במעגל מ-0 עד \( n - 1 \). אם אדם מקבל את המקום \( q \) במעגל הקטן,
    איזה מקום היה לו במעגל המקורי?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        במספור מ-0: ‏\( f(1) = 0 \), ו-\( f(m) = \left(f(m - 1) + k\right) \bmod m \). השורד
        הוא \( f(n) + 1 \). זמן \( O(n) \), זיכרון \( O(1) \). עבור \( n = 41 \) ו-\( k = 3 \)
        השורד הוא 31.

    #### הרעיון { .sol-idea }

    אחרי יציאה אחת המעגל הוא בדיוק מעגל של \( m - 1 \) אנשים, שהספירה בו מתחילה מהאדם
    שאחרי מי שיצא. אם יודעים מי שורד במעגל הקטן, צריך רק לתרגם את המקום שלו בחזרה למספור
    של המעגל הגדול. התרגום הוא הזזה ב-\( k \) מקומות, מודולו \( m \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סימולציה:** אותו תור כמו בסעיף א, אבל \( k - 1 \) אנשים עוברים לסוף לפני שהבא
       יוצא.
    2. **מספור מ-0:** המקומות במעגל של \( m \) אנשים הם \( 0, \ldots, m - 1 \), והספירה מתחילה
       במקום 0.
    3. **מספור מחדש:** אחרי היציאה הראשונה, המקום \( q \) במעגל הקטן הוא המקום
       \( (q + k) \bmod m \) במעגל הגדול.
    4. **נסיגה:** מתחילים מ-\( f(1) = 0 \) ומחשבים את \( f(2), f(3), \ldots, f(n) \) בלולאה.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="functions josephus_sim_k and josephus_k" linenums="1" hl_lines="5 14"
        function automatic int josephus_sim_k(int n, int k);
          int circle[$];
          for (int p = 1; p <= n; p++) circle.push_back(p);
          while (circle.size() > 1) begin
            repeat (k - 1) circle.push_back(circle.pop_front());   // k - 1 are counted and stay
            void'(circle.pop_front());                             // the k-th leaves
          end
          return circle[0];
        endfunction

        function automatic int josephus_k(int n, int k);
          int f = 0;                       // 0-based survivor of a circle of one person
          for (int m = 2; m <= n; m++)
            f = (f + k) % m;   // (1)!
          return f + 1;   // (2)!
        endfunction
        ```

        1. מעבר ממעגל של \( m - 1 \) אנשים למעגל של \( m \): המקום \( f \) במעגל הקטן הוא
           המקום \( (f + k) \bmod m \) במעגל הגדול. כל הערכים חיוביים, ולכן `%` בטוח כאן.
        2. המספור בנוסחה מתחיל מ-0, והאנשים בשאלה ממוספרים מ-1.

    === "Python"
        ```python title="josephus_sim_k and josephus_k" linenums="1" hl_lines="4 12"
        def josephus_sim_k(n: int, k: int) -> int:
            circle = deque(range(1, n + 1))
            while len(circle) > 1:
                circle.rotate(-(k - 1))   # (1)!
                circle.popleft()          # the k-th leaves
            return circle[0]


        def josephus_k(n: int, k: int) -> int:
            f = 0                         # 0-based survivor of a circle of one person
            for m in range(2, n + 1):
                f = (f + k) % m           # from a circle of m - 1 to a circle of m
            return f + 1
        ```

        1. ‏`rotate(-(k - 1))` מעביר את \( k - 1 \) הראשונים לסוף, בדיוק כמו הלולאה בגרסת
           ה-SystemVerilog. ‏`deque` משתמש ב-`collections` מסעיף א.

    #### למה זה נכון { .sol-proof }

    **המספור מחדש.** במעגל של \( m \) אנשים, במקומות \( 0, \ldots, m - 1 \), יוצא המקום
    \( k - 1 \) (מודולו \( m \)). הספירה הבאה מתחילה מהמקום \( k \bmod m \), ולכן נותנים לו
    את המקום 0 במעגל הקטן, למקום שאחריו את המקום 1, וכן הלאה. כלומר, המקום \( q \) במעגל
    הקטן הוא המקום \( (q + k) \bmod m \) במעגל הגדול. השורד של המעגל הקטן, במקום
    \( f(m - 1) \), הוא גם השורד של הגדול:

    \[
    f(m) = \left(f(m - 1) + k\right) \bmod m
    \]

    **דוגמה: \( n = 7 \), כל שלישי יוצא.** קודם הסימולציה:

    <div class="stepper" role="group" aria-label="יוספוס עם 7 אנשים, כל שלישי יוצא" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="7 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-cell" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="232.1" cy="74.5" r="17"/><text class="st-text" x="232.1" y="79.5" text-anchor="middle">2</text></g><g><circle class="st-cell" cx="252.4" cy="163.4" r="17"/><text class="st-text" x="252.4" y="168.4" text-anchor="middle">3</text></g><g><circle class="st-cell" cx="195.6" cy="234.6" r="17"/><text class="st-text" x="195.6" y="239.6" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="104.4" cy="234.6" r="17"/><text class="st-text" x="104.4" y="239.6" text-anchor="middle">5</text></g><g><circle class="st-cell" cx="47.6" cy="163.4" r="17"/><text class="st-text" x="47.6" y="168.4" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="67.9" cy="74.5" r="17"/><text class="st-text" x="67.9" y="79.5" text-anchor="middle">7</text></g><text class="st-text" x="150" y="146" text-anchor="middle">7</text></svg><figcaption>7 אנשים במעגל. סופרים מאדם 1, וכל שלישי יוצא. המספר במרכז הוא כמה אנשים נשארו.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="7 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-stack" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g><circle class="st-stack" cx="232.1" cy="74.5" r="17"/><text class="st-text" x="232.1" y="79.5" text-anchor="middle">2</text></g><g><circle class="st-bad" cx="252.4" cy="163.4" r="17"/><text class="st-text" x="252.4" y="168.4" text-anchor="middle">3</text><line class="pg-strike" x1="240.4" y1="175.4" x2="264.4" y2="151.4"/></g><g><circle class="st-cell" cx="195.6" cy="234.6" r="17"/><text class="st-text" x="195.6" y="239.6" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="104.4" cy="234.6" r="17"/><text class="st-text" x="104.4" y="239.6" text-anchor="middle">5</text></g><g><circle class="st-cell" cx="47.6" cy="163.4" r="17"/><text class="st-text" x="47.6" y="168.4" text-anchor="middle">6</text></g><g><circle class="st-cell" cx="67.9" cy="74.5" r="17"/><text class="st-text" x="67.9" y="79.5" text-anchor="middle">7</text></g><text class="st-text" x="150" y="146" text-anchor="middle">6</text></svg><figcaption>יציאה 1: סופרים את 1 ו-2, ואדם 3 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="7 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-cell" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g><circle class="st-cell" cx="232.1" cy="74.5" r="17"/><text class="st-text" x="232.1" y="79.5" text-anchor="middle">2</text></g><g class="st-faded"><circle class="st-done" cx="252.4" cy="163.4" r="17"/><text class="st-text" x="252.4" y="168.4" text-anchor="middle">3</text><line class="pg-strike" x1="240.4" y1="175.4" x2="264.4" y2="151.4"/></g><g><circle class="st-stack" cx="195.6" cy="234.6" r="17"/><text class="st-text" x="195.6" y="239.6" text-anchor="middle">4</text></g><g><circle class="st-stack" cx="104.4" cy="234.6" r="17"/><text class="st-text" x="104.4" y="239.6" text-anchor="middle">5</text></g><g><circle class="st-bad" cx="47.6" cy="163.4" r="17"/><text class="st-text" x="47.6" y="168.4" text-anchor="middle">6</text><line class="pg-strike" x1="35.6" y1="175.4" x2="59.6" y2="151.4"/></g><g><circle class="st-cell" cx="67.9" cy="74.5" r="17"/><text class="st-text" x="67.9" y="79.5" text-anchor="middle">7</text></g><text class="st-text" x="150" y="146" text-anchor="middle">5</text></svg><figcaption>יציאה 2: סופרים את 4 ו-5, ואדם 6 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="7 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-stack" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g><circle class="st-bad" cx="232.1" cy="74.5" r="17"/><text class="st-text" x="232.1" y="79.5" text-anchor="middle">2</text><line class="pg-strike" x1="220.1" y1="86.5" x2="244.1" y2="62.5"/></g><g class="st-faded"><circle class="st-done" cx="252.4" cy="163.4" r="17"/><text class="st-text" x="252.4" y="168.4" text-anchor="middle">3</text><line class="pg-strike" x1="240.4" y1="175.4" x2="264.4" y2="151.4"/></g><g><circle class="st-cell" cx="195.6" cy="234.6" r="17"/><text class="st-text" x="195.6" y="239.6" text-anchor="middle">4</text></g><g><circle class="st-cell" cx="104.4" cy="234.6" r="17"/><text class="st-text" x="104.4" y="239.6" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-done" cx="47.6" cy="163.4" r="17"/><text class="st-text" x="47.6" y="168.4" text-anchor="middle">6</text><line class="pg-strike" x1="35.6" y1="175.4" x2="59.6" y2="151.4"/></g><g><circle class="st-stack" cx="67.9" cy="74.5" r="17"/><text class="st-text" x="67.9" y="79.5" text-anchor="middle">7</text></g><text class="st-text" x="150" y="146" text-anchor="middle">4</text></svg><figcaption>יציאה 3: סופרים את 7 ו-1, ואדם 2 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="7 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-cell" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g class="st-faded"><circle class="st-done" cx="232.1" cy="74.5" r="17"/><text class="st-text" x="232.1" y="79.5" text-anchor="middle">2</text><line class="pg-strike" x1="220.1" y1="86.5" x2="244.1" y2="62.5"/></g><g class="st-faded"><circle class="st-done" cx="252.4" cy="163.4" r="17"/><text class="st-text" x="252.4" y="168.4" text-anchor="middle">3</text><line class="pg-strike" x1="240.4" y1="175.4" x2="264.4" y2="151.4"/></g><g><circle class="st-stack" cx="195.6" cy="234.6" r="17"/><text class="st-text" x="195.6" y="239.6" text-anchor="middle">4</text></g><g><circle class="st-stack" cx="104.4" cy="234.6" r="17"/><text class="st-text" x="104.4" y="239.6" text-anchor="middle">5</text></g><g class="st-faded"><circle class="st-done" cx="47.6" cy="163.4" r="17"/><text class="st-text" x="47.6" y="168.4" text-anchor="middle">6</text><line class="pg-strike" x1="35.6" y1="175.4" x2="59.6" y2="151.4"/></g><g><circle class="st-bad" cx="67.9" cy="74.5" r="17"/><text class="st-text" x="67.9" y="79.5" text-anchor="middle">7</text><line class="pg-strike" x1="55.9" y1="86.5" x2="79.9" y2="62.5"/></g><text class="st-text" x="150" y="146" text-anchor="middle">3</text></svg><figcaption>יציאה 4: סופרים את 4 ו-5, ואדם 7 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="7 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-stack" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text></g><g class="st-faded"><circle class="st-done" cx="232.1" cy="74.5" r="17"/><text class="st-text" x="232.1" y="79.5" text-anchor="middle">2</text><line class="pg-strike" x1="220.1" y1="86.5" x2="244.1" y2="62.5"/></g><g class="st-faded"><circle class="st-done" cx="252.4" cy="163.4" r="17"/><text class="st-text" x="252.4" y="168.4" text-anchor="middle">3</text><line class="pg-strike" x1="240.4" y1="175.4" x2="264.4" y2="151.4"/></g><g><circle class="st-stack" cx="195.6" cy="234.6" r="17"/><text class="st-text" x="195.6" y="239.6" text-anchor="middle">4</text></g><g><circle class="st-bad" cx="104.4" cy="234.6" r="17"/><text class="st-text" x="104.4" y="239.6" text-anchor="middle">5</text><line class="pg-strike" x1="92.4" y1="246.6" x2="116.4" y2="222.6"/></g><g class="st-faded"><circle class="st-done" cx="47.6" cy="163.4" r="17"/><text class="st-text" x="47.6" y="168.4" text-anchor="middle">6</text><line class="pg-strike" x1="35.6" y1="175.4" x2="59.6" y2="151.4"/></g><g class="st-faded"><circle class="st-done" cx="67.9" cy="74.5" r="17"/><text class="st-text" x="67.9" y="79.5" text-anchor="middle">7</text><line class="pg-strike" x1="55.9" y1="86.5" x2="79.9" y2="62.5"/></g><text class="st-text" x="150" y="146" text-anchor="middle">2</text></svg><figcaption>יציאה 5: סופרים את 1 ו-4, ואדם 5 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="7 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g><circle class="st-bad" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text><line class="pg-strike" x1="138.0" y1="47.0" x2="162.0" y2="23.0"/></g><g class="st-faded"><circle class="st-done" cx="232.1" cy="74.5" r="17"/><text class="st-text" x="232.1" y="79.5" text-anchor="middle">2</text><line class="pg-strike" x1="220.1" y1="86.5" x2="244.1" y2="62.5"/></g><g class="st-faded"><circle class="st-done" cx="252.4" cy="163.4" r="17"/><text class="st-text" x="252.4" y="168.4" text-anchor="middle">3</text><line class="pg-strike" x1="240.4" y1="175.4" x2="264.4" y2="151.4"/></g><g><circle class="st-stack" cx="195.6" cy="234.6" r="17"/><text class="st-text" x="195.6" y="239.6" text-anchor="middle">4</text></g><g class="st-faded"><circle class="st-done" cx="104.4" cy="234.6" r="17"/><text class="st-text" x="104.4" y="239.6" text-anchor="middle">5</text><line class="pg-strike" x1="92.4" y1="246.6" x2="116.4" y2="222.6"/></g><g class="st-faded"><circle class="st-done" cx="47.6" cy="163.4" r="17"/><text class="st-text" x="47.6" y="168.4" text-anchor="middle">6</text><line class="pg-strike" x1="35.6" y1="175.4" x2="59.6" y2="151.4"/></g><g class="st-faded"><circle class="st-done" cx="67.9" cy="74.5" r="17"/><text class="st-text" x="67.9" y="79.5" text-anchor="middle">7</text><line class="pg-strike" x1="55.9" y1="86.5" x2="79.9" y2="62.5"/></g><text class="st-text" x="150" y="146" text-anchor="middle">1</text></svg><figcaption>יציאה 6: סופרים את 1 ו-4, ואדם 1 יוצא.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 300 280" style="max-width:19rem" role="img" aria-label="7 אנשים במעגל"><circle cx="150" cy="140" r="105" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/><g class="st-faded"><circle class="st-done" cx="150.0" cy="35.0" r="17"/><text class="st-text" x="150.0" y="40.0" text-anchor="middle">1</text><line class="pg-strike" x1="138.0" y1="47.0" x2="162.0" y2="23.0"/></g><g class="st-faded"><circle class="st-done" cx="232.1" cy="74.5" r="17"/><text class="st-text" x="232.1" y="79.5" text-anchor="middle">2</text><line class="pg-strike" x1="220.1" y1="86.5" x2="244.1" y2="62.5"/></g><g class="st-faded"><circle class="st-done" cx="252.4" cy="163.4" r="17"/><text class="st-text" x="252.4" y="168.4" text-anchor="middle">3</text><line class="pg-strike" x1="240.4" y1="175.4" x2="264.4" y2="151.4"/></g><g><circle class="st-ok" cx="195.6" cy="234.6" r="17"/><text class="st-text" x="195.6" y="239.6" text-anchor="middle">4</text></g><g class="st-faded"><circle class="st-done" cx="104.4" cy="234.6" r="17"/><text class="st-text" x="104.4" y="239.6" text-anchor="middle">5</text><line class="pg-strike" x1="92.4" y1="246.6" x2="116.4" y2="222.6"/></g><g class="st-faded"><circle class="st-done" cx="47.6" cy="163.4" r="17"/><text class="st-text" x="47.6" y="168.4" text-anchor="middle">6</text><line class="pg-strike" x1="35.6" y1="175.4" x2="59.6" y2="151.4"/></g><g class="st-faded"><circle class="st-done" cx="67.9" cy="74.5" r="17"/><text class="st-text" x="67.9" y="79.5" text-anchor="middle">7</text><line class="pg-strike" x1="55.9" y1="86.5" x2="79.9" y2="62.5"/></g><text class="st-text" x="150" y="146" text-anchor="middle">1</text></svg><figcaption>נשאר אדם 4. הוא השורד.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="8"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    ועכשיו אותה תשובה מהנוסחה, בלי סימולציה:

    | מספר האנשים \( m \) | החישוב | ‏\( f(m) \) | השורד, \( f(m) + 1 \) |
    |---|---|---|---|
    | 1 | בסיס: אדם אחד | 0 | 1 |
    | 2 | ‏\( (0 + 3) \bmod 2 \) | 1 | 2 |
    | 3 | ‏\( (1 + 3) \bmod 3 \) | 1 | 2 |
    | 4 | ‏\( (1 + 3) \bmod 4 \) | 0 | 1 |
    | 5 | ‏\( (0 + 3) \bmod 5 \) | 3 | 4 |
    | 6 | ‏\( (3 + 3) \bmod 6 \) | 0 | 1 |
    | 7 | ‏\( (0 + 3) \bmod 7 \) | 3 | 4 |

    **המספרים של יוסף.** עם 41 אנשים וכל שלישי יוצא, הנוסחה נותנת 31. לפי הסיפור, זה המקום
    שבו עמד יוסף. מי שעומד במקום 16 יוצא אחרון לפניו.

    #### סיבוכיות { .sol-cost }

    | | סימולציה | נוסחת הנסיגה |
    |---|---|---|
    | זמן | ‏\( O(nk) \) | ‏\( O(n) \) |
    | זיכרון | ‏\( O(n) \) | ‏\( O(1) \) |

    עבור \( k = 2 \) הנוסחה הסגורה מסעיף ב טובה יותר משתיהן, אבל לכל \( k \) כללי אין
    נוסחה סגורה פשוטה.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: האינדקס אחרי מחיקה ממערך"
    בסימולציה עם מערך ואינדקס, אחרי שמוחקים את האיבר במקום \( i \), האדם הבא נמצא **באותו
    מקום** \( i \), ולא ב-\( i + 1 \), כי כל מי שאחריו זז מקום אחד אחורה. צריך גם לחשב את
    המודולו לפי הגודל **החדש** של המערך. שתי הטעויות נותנות שורד שגוי רק בחלק מהמקרים,
    ולכן כדאי להשוות לנוסחה על הרבה ערכים של \( n \).

??? trap "מלכודת: לערבב מספור מ-0 ומספור מ-1"
    נוסחת הנסיגה נכונה רק במספור מ-0, כי המודולו נותן ערכים בין 0 ל-\( m - 1 \). אם מפעילים
    אותה על מספרים מ-1, או שוכחים להוסיף 1 בסוף, התשובה זזה במקום אחד.

??? followup "שאלות המשך"
    - **השני מהסוף:** מי יוצא אחרון לפני השורד? איך משנים את הסימולציה, ואיך את הנסיגה?
    - **‏\( n \) ענק ו-\( k \) קטן:** כש-\( n = 10^{18} \) לולאה של \( n \) צעדים לא אפשרית.
      אפשר לדלג על סיבוב שלם בבת אחת ולקבל זמן של בערך \( O(k \log n) \). איך?
    - **מעגל צירופי:** תכננו בחומרה מעגל שמקבל \( n \) של 16 ביט ומוציא את השורד עבור
      \( k = 2 \). מה העומק שלו?
    - **הכיוון ההפוך:** בהינתן מקום \( s \) שבו רוצים לעמוד, עבור איזה \( n \) הוא השורד
      כש-\( k = 2 \)?
