---
id: 90
title: מיון פנקייקים – הפיכות מלמעלה, המקרה הגרוע ופנקייקים שרופים
level: senior
difficulty: hard
kind: code
tags: [algorithms, sorting, permutations, bfs, proof, python, systemverilog]
source: "בעיה קלאסית (Jacob Goodman, 1975); החסם הראשון של Gates ו-Papadimitriou (1979), הפנקייקים השרופים של Cohen ו-Blum (1995)"
added: 2026-11-06
---

## השאלה

על צלחת מונחת ערימה של \( n \) פנקייקים, כולם בגדלים שונים : \( 1, 2, \dots, n \). הפעולה
היחידה המותרת היא **הפיכה** : מכניסים מרית מתחת לאחד הפנקייקים, והופכים בבת אחת את כל
מה שמעליה. הפיכה של \( k \) העליונים הופכת את הסדר שלהם, והפנקייק שהיה עליון יורד למקום
ה-\( k \) מלמעלה. המטרה : ערימה **ממוינת**, הקטן ביותר למעלה והגדול ביותר למטה, בכמה
שפחות הפיכות.

נכתוב ערימה כרשימה **מלמעלה למטה** : `[3, 1, 5, 4, 2]` היא ערימה שהפנקייק העליון בה הוא 3
והתחתון, הצמוד לצלחת, הוא 2. הפיכה של 3 העליונים הופכת אותה ל-`[5, 1, 3, 4, 2]` :

<!-- gen 0 -->

<svg class="figure pk-fig" viewBox="0 0 360 138" style="max-width:22.5rem" role="img" aria-label="הערימה 3, 1, 5, 4, 2 מלמעלה למטה, ואחרי הפיכה של 3 העליונים : 5, 1, 3, 4, 2"><rect class="pk-cake" x="27.2" y="6" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">3</text><rect class="pk-cake" x="50.4" y="30" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">1</text><rect class="pk-cake" x="4.0" y="54" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">5</text><rect class="pk-cake" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake" x="38.8" y="102" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">2</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><path class="pk-arrow" d="M156,40 Q183,18 206,40"/><polygon class="pk-head" points="200,34 210,42 199,45"/><rect class="pk-cake" x="214.0" y="6" width="142.0" height="20" rx="9"/><text class="pk-num" x="285.0" y="21" text-anchor="middle">5</text><rect class="pk-cake" x="260.4" y="30" width="49.2" height="20" rx="9"/><text class="pk-num" x="285.0" y="45" text-anchor="middle">1</text><rect class="pk-cake" x="237.2" y="54" width="95.6" height="20" rx="9"/><text class="pk-num" x="285.0" y="69" text-anchor="middle">3</text><rect class="pk-cake" x="225.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="285.0" y="93" text-anchor="middle">4</text><rect class="pk-cake" x="248.8" y="102" width="72.4" height="20" rx="9"/><text class="pk-num" x="285.0" y="117" text-anchor="middle">2</text><line class="pk-plate" x1="214" x2="356" y1="128" y2="128"/><rect class="pk-flipbox" x="212" y="2" width="146" height="74.0" rx="6"/></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="pk-key-cake"></i>פנקייק, רחב כמו הגודל שלו</span><span><i class="pk-key-flip"></i>הפנקייקים שההפיכה הפכה</span><span><i class="pk-key-done"></i>במקום הסופי</span><span><i class="pk-key-plate"></i>הצלחת</span></span>

<!-- /gen -->

??? interviewer "מה המראיין בודק"
    - **כיוון העבודה :** הפיכה נוגעת רק בחלק העליון. האם המועמד רואה שצריך לסדר מלמטה
      למעלה, את הגדול ביותר קודם, ושפנקייק שהגיע לתחתית כבר לא זז.
    - **ספירה והוכחה :** לא רק "זה עובד", אלא כמה הפיכות לכל היותר, ולמה בדיוק
      \( 2n - 3 \) ולא \( 2n \).
    - **אלגוריתם מול אופטימום :** האם הוא מבחין בין "האלגוריתם שלי משתמש ב-\( 2n - 3 \)"
      לבין "צריך \( 2n - 3 \)", ויודע לבדוק את המקרה הגרוע האמיתי בחיפוש.
    - **מרחב מצבים :** ערימה היא תמורה, הפיכה היא קשת, ו-BFS אחד מהערימה הממוינת מספיק לכל
      הערימות, כי כל הפיכה היא ההופכית של עצמה.
    - **שינוי במודל :** בפנקייקים שרופים לכל פנקייק יש גם כיוון. האם הוא מעדכן את
      האלגוריתם, את החסם ואת מרחב המצבים בהתאם.

---

### סעיף א – האלגוריתם הפשוט, שתי הפיכות לפנקייק { #part-a }

כתבו אלגוריתם שממיין כל ערימה, והוכיחו שהוא משתמש לכל היותר ב-\( 2n - 3 \) הפיכות (ל-\( n
\ge 2 \)). כמה הפיכות הוא עושה על `[3, 1, 5, 4, 2]`?

??? tip "רמז 1"
    איזה פנקייק אפשר לשים במקום הסופי שלו בלי לפגוע אחר כך בשום דבר? מה קורה לפנקייק
    שהגיע לתחתית הערימה?

??? tip "רמז 2"
    כדי להוריד את הגדול ביותר לתחתית צריך שהוא יהיה קודם למעלה. כמה הפיכות זה לכל היותר?
    ומה קורה כשנשארים רק שני פנקייקים?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        מסדרים מהגדול לקטן. לכל \( k = n, n - 1, \dots, 2 \) : אם \( k \) לא במקומו,
        מעלים אותו לראש בהפיכה אחת (אם הוא לא שם כבר), ומורידים אותו למקום \( k \) בהפיכה
        של \( k \) העליונים. כל פנקייק עולה לכל היותר שתי הפיכות, ושני האחרונים לכל היותר
        אחת, ולכן \( 2(n - 2) + 1 = 2n - 3 \). על `[3, 1, 5, 4, 2]` הוא עושה 7 הפיכות, בדיוק
        החסם.

    <!-- cost: הפיכות \( 2n - 3 \) | זמן \( O(n^2) \) -->

    #### הרעיון { .sol-idea }

    הפיכה של \( k \) העליונים לא נוגעת במה שמתחתם. לכן פנקייק שהונח בתחתית נשאר שם לתמיד,
    כל עוד הופכים רק מעליו. זה מה שקובע את הכיוון : קודם הגדול ביותר, \( n \), לתחתית, אחריו
    \( n - 1 \) מעליו, וכן הלאה. כדי להוריד פנקייק למקום \( k \) מלמטה, הוא צריך להיות
    למעלה, ואז הפיכה של \( k \) העליונים מורידה אותו בדיוק לשם.

    על הערימה של השאלה, הפיכה אחרי הפיכה. המסגרת מקיפה את הפנקייקים שההפיכה הפכה, והירוקים
    כבר במקומם הסופי :

    <!-- gen 2 -->

    <div class="stepper" role="group" aria-label="האלגוריתם הפשוט על הערימה של השאלה, הפיכה אחרי הפיכה" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="התחלה"><rect class="pk-cake" x="27.2" y="6" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">3</text><rect class="pk-cake" x="50.4" y="30" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">1</text><rect class="pk-cake" x="4.0" y="54" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">5</text><rect class="pk-cake" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake" x="38.8" y="102" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">2</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/></svg><figcaption>התחלה : הערימה <code>[3, 1, 5, 4, 2]</code>, מלמעלה למטה.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 1"><rect class="pk-cake" x="4.0" y="6" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">5</text><rect class="pk-cake" x="50.4" y="30" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">1</text><rect class="pk-cake" x="27.2" y="54" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><rect class="pk-cake" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake" x="38.8" y="102" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">2</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="74.0" rx="6"/></svg><figcaption>הפיכה 1 : הופכים את 3 העליונים, כדי להעלות את 5 לראש הערימה. עכשיו <code>[5, 1, 3, 4, 2]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 2"><rect class="pk-cake" x="38.8" y="6" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">2</text><rect class="pk-cake" x="15.6" y="30" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">4</text><rect class="pk-cake" x="27.2" y="54" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><rect class="pk-cake" x="50.4" y="78" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">1</text><rect class="pk-cake pk-done" x="4.0" y="102" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">5</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="122.0" rx="6"/></svg><figcaption>הפיכה 2 : הופכים את 5 העליונים, והפנקייק 5 יורד למקום הסופי שלו. עכשיו <code>[2, 4, 3, 1, 5]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 3"><rect class="pk-cake" x="15.6" y="6" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">4</text><rect class="pk-cake" x="38.8" y="30" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">2</text><rect class="pk-cake" x="27.2" y="54" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><rect class="pk-cake" x="50.4" y="78" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">1</text><rect class="pk-cake pk-done" x="4.0" y="102" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">5</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="50.0" rx="6"/></svg><figcaption>הפיכה 3 : הופכים את 2 העליונים, כדי להעלות את 4 לראש הערימה. עכשיו <code>[4, 2, 3, 1, 5]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 4"><rect class="pk-cake" x="50.4" y="6" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">1</text><rect class="pk-cake" x="27.2" y="30" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">3</text><rect class="pk-cake" x="38.8" y="54" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">2</text><rect class="pk-cake pk-done" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake pk-done" x="4.0" y="102" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">5</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="98.0" rx="6"/></svg><figcaption>הפיכה 4 : הופכים את 4 העליונים, והפנקייק 4 יורד למקום הסופי שלו. עכשיו <code>[1, 3, 2, 4, 5]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 5"><rect class="pk-cake" x="27.2" y="6" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">3</text><rect class="pk-cake" x="50.4" y="30" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">1</text><rect class="pk-cake" x="38.8" y="54" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">2</text><rect class="pk-cake pk-done" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake pk-done" x="4.0" y="102" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">5</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="50.0" rx="6"/></svg><figcaption>הפיכה 5 : הופכים את 2 העליונים, כדי להעלות את 3 לראש הערימה. עכשיו <code>[3, 1, 2, 4, 5]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 6"><rect class="pk-cake" x="38.8" y="6" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">2</text><rect class="pk-cake" x="50.4" y="30" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">1</text><rect class="pk-cake pk-done" x="27.2" y="54" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><rect class="pk-cake pk-done" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake pk-done" x="4.0" y="102" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">5</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="74.0" rx="6"/></svg><figcaption>הפיכה 6 : הופכים את 3 העליונים, והפנקייק 3 יורד למקום הסופי שלו. עכשיו <code>[2, 1, 3, 4, 5]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 7"><rect class="pk-cake pk-done" x="50.4" y="6" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">1</text><rect class="pk-cake pk-done" x="38.8" y="30" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">2</text><rect class="pk-cake pk-done" x="27.2" y="54" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><rect class="pk-cake pk-done" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake pk-done" x="4.0" y="102" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">5</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="50.0" rx="6"/></svg><figcaption>הפיכה 7 : הופכים את 2 העליונים, והפנקייק 2 יורד למקום הסופי שלו. עכשיו <code>[1, 2, 3, 4, 5]</code>. <strong>ממוין אחרי 7 הפיכות.</strong></figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="8"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מהגדול לקטן :** עוברים על \( k = n, n - 1, \dots, 2 \). מתחת לפנקייק \( k \) כבר
       מונחים \( k + 1, \dots, n \) במקומם.
    2. **מחפשים :** המקום \( p \) של הפנקייק \( k \) (0 הוא העליון). אם \( p = k - 1 \),
       הוא כבר במקומו, ועוברים הלאה.
    3. **מעלים :** אם \( p > 0 \), הופכים את \( p + 1 \) העליונים, ו-\( k \) עולה לראש.
    4. **מורידים :** הופכים את \( k \) העליונים, ו-\( k \) יורד למקום \( k - 1 \), מעל
       \( k + 1 \).
    5. **הפנקייק 1 :** כשכל השאר במקומם, גם הוא במקומו : אין לו לאן ללכת.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="simple_sort" linenums="1" hl_lines="11 15 17"
        def flip(stack, k):
            """Turn the top k pancakes over: stack[0] is the top."""
            return stack[:k][::-1] + stack[k:]


        def simple_sort(stack):
            """Largest first: bring pancake k to the top, then flip it down to place k.
            Returns the sorted stack and the flips (each one: how many from the top)."""
            s, flips = list(stack), []
            for k in range(len(s), 1, -1):
                p = s.index(k)                        # (1)!
                if p == k - 1:
                    continue                          # (2)!
                if p > 0:
                    s = flip(s, p + 1)                # (3)!
                    flips.append(p + 1)
                s = flip(s, k)                        # (4)!
                flips.append(k)
            return s, flips
        ```

        1. ‏\( p \) הוא המקום של הפנקייק \( k \), מלמעלה, החל מ-0.
        2. כבר במקומו : מעליו הכול קטן ממנו, ומתחתיו \( k + 1, \dots, n \) מסודרים.
        3. מעלים את \( k \) לראש. כש-\( p = 0 \) הוא כבר שם, וההפיכה הזו נחסכת.
        4. ‏\( k \) יורד מהראש למקום \( k - 1 \), מעל מה שכבר מסודר.

    === "SystemVerilog"
        ```systemverilog title="function automatic int simple_sort" linenums="1" hl_lines="16 18 21"
        // Turn the top k pancakes over: s[0] is the top.
        function automatic void flip(ref int s[$], input int k);
          int i = 0, j = k - 1, t;
          while (i < j) begin
            t = s[i]; s[i] = s[j]; s[j] = t;
            i++; j--;
          end
        endfunction

        // Largest first; returns the number of flips, flips lists them ("3 5 2 ...").
        function automatic int simple_sort(ref int s[$], output string flips);
          int n = s.size(), count = 0, p;
          flips = "";
          for (int k = n; k >= 2; k--) begin
            for (p = 0; s[p] != k; p++) ;               // where pancake k is
            if (p == k - 1) continue;                    // (1)!
            if (p > 0) begin
              flip(s, p + 1); count++;                   // (2)!
              flips = {flips, $sformatf("%0d ", p + 1)};
            end
            flip(s, k); count++;                         // (3)!
            flips = {flips, $sformatf("%0d ", k)};
          end
          return count;
        endfunction
        ```

        1. ‏\( k \) כבר במקומו.
        2. ‏\( k \) עולה לראש.
        3. ‏\( k \) יורד למקום \( k - 1 \).

    #### למה זה נכון { .sol-proof }

    **נכונות.** לפני הסיבוב של \( k \), הפנקייקים \( k + 1, \dots, n \) נמצאים במקומם, בתחתית.
    שתי ההפיכות של הסיבוב הופכות רק את \( k \) העליונים, ולכן לא נוגעות בהם. אחרי ההפיכה
    השנייה \( k \) עומד במקום \( k - 1 \), מעליהם. באינדוקציה, אחרי הסיבוב של 2 כל הפנקייקים
    מ-2 עד \( n \) במקומם, וה-1 נשאר למעלה, במקומו.

    **ספירה.** כל אחד מהסיבובים \( k = n, \dots, 3 \) עולה לכל היותר שתי הפיכות. בסיבוב של
    2 נשארו רק שני פנקייקים מעל המסודרים : או שהם כבר בסדר, או שה-2 למעלה, והפיכה אחת של 2
    מסיימת. בסך הכול לכל היותר \( 2(n - 2) + 1 = 2n - 3 \). החסם הדוק לאלגוריתם הזה : לכל
    \( n \) יש ערימה שהוא עושה עליה בדיוק \( 2n - 3 \) הפיכות, כמו `[3, 1, 5, 4, 2]` ב-\( n = 5 \).

    #### סיבוכיות { .sol-cost }

    לכל היותר \( 2n - 3 \) הפיכות. כל הפיכה וכל חיפוש עולים \( O(n) \), ולכן הזמן
    \( O(n^2) \), והזיכרון \( O(n) \).

---

### סעיף ב – המקרה הגרוע המדויק { #part-b }

האם \( 2n - 3 \) הוא המספר שבאמת צריך? מצאו, לכל \( n \le 8 \), את **מספר הפנקייק**
\( P(n) \) : הכי מעט הפיכות שמספיקות לכל ערימה של \( n \). כמה הפיכות צריך באמת
ל-`[3, 1, 5, 4, 2]`, ואיך?

??? tip "רמז 1"
    כל ערימה היא תמורה של \( 1, \dots, n \), וכל הפיכה מעבירה מתמורה לתמורה. איזה גרף זה,
    וכמה צמתים יש בו?

??? tip "רמז 2"
    הפיכה של אותם \( k \) פעמיים מחזירה את הערימה. מה זה אומר על המרחק מערימה לערימה
    הממוינת, ועל המרחק בכיוון ההפוך?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏BFS אחד מהערימה הממוינת על כל \( n! \) הערימות נותן את המרחק של כל אחת מהן : זה
        מספר ההפיכות הקטן ביותר שממיין אותה, כי כל הפיכה היא ההופכית של עצמה. המקסימום
        הוא \( P(n) \) : ‏0, 1, 3, 4, 5, 7, 8, 9 ל-\( n \) מ-1 עד 8, מול \( 2n - 3 \) שעולה
        ל-13. את `[3, 1, 5, 4, 2]` אפשר למיין ב-5 הפיכות במקום 7.

    <!-- cost: ערימות \( n! \) | זמן \( O(n! \cdot n^2) \) -->

    #### הרעיון { .sol-idea }

    נבנה גרף : צומת לכל ערימה, וקשת בין שתי ערימות שהפיכה אחת עוברת ביניהן. מספר
    ההפיכות הקטן ביותר שממיין ערימה הוא המרחק שלה בגרף מהערימה הממוינת. הפיכה של \( k \)
    העליונים, פעמיים, מחזירה את המצב, ולכן כל קשת היא דו-כיוונית. מספיק BFS **אחד**, מהערימה
    הממוינת, כדי לדעת את המרחק של כל הערימות. הגדול שבהם הוא \( P(n) \).

    התוצאה, מול החסם של סעיף א. "המקרה הגרוע" הוא \( P(n) \), "ערימות קשות" הן הערימות שצריכות בדיוק
    \( P(n) \) הפיכות, ו"האלגוריתם הפשוט" הוא הכי הרבה הפיכות שהוא עושה על ערימה של \( n \). הפער
    גדל עם \( n \) :

    <!-- gen 3 -->

    | ‏n | ערימות | המקרה הגרוע | ערימות קשות | האלגוריתם הפשוט | ‏\( 2n - 3 \) |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | 1 | 1 | 0 | 1 | 0 | ‏– |
    | 2 | 2 | 1 | 1 | 1 | 1 |
    | 3 | 6 | 3 | 1 | 3 | 3 |
    | 4 | 24 | 4 | 3 | 5 | 5 |
    | 5 | 120 | 5 | 20 | 7 | 7 |
    | 6 | 720 | 7 | 2 | 9 | 9 |
    | 7 | 5,040 | 8 | 35 | 11 | 11 |
    | 8 | 40,320 | 9 | 455 | 13 | 13 |

    <!-- /gen -->

    <!-- gen 4 -->

    <svg class="perf-chart" viewBox="0 0 520 230" role="img" aria-label="המקרה הגרוע לכל n מ-2 עד 8 : הנקודות הן הכי מעט הפיכות לערימה הקשה ביותר, והקו הוא 2n − 3 של האלגוריתם הפשוט"><line class="grid" x1="42" x2="508" y1="190.0" y2="190.0"/><text class="tick" x="34" y="194.0" text-anchor="end">0</text><line class="grid" x1="42" x2="508" y1="164.9" y2="164.9"/><text class="tick" x="34" y="168.9" text-anchor="end">2</text><line class="grid" x1="42" x2="508" y1="139.7" y2="139.7"/><text class="tick" x="34" y="143.7" text-anchor="end">4</text><line class="grid" x1="42" x2="508" y1="114.6" y2="114.6"/><text class="tick" x="34" y="118.6" text-anchor="end">6</text><line class="grid" x1="42" x2="508" y1="89.4" y2="89.4"/><text class="tick" x="34" y="93.4" text-anchor="end">8</text><line class="grid" x1="42" x2="508" y1="64.3" y2="64.3"/><text class="tick" x="34" y="68.3" text-anchor="end">10</text><line class="grid" x1="42" x2="508" y1="39.1" y2="39.1"/><text class="tick" x="34" y="43.1" text-anchor="end">12</text><line class="grid" x1="42" x2="508" y1="14.0" y2="14.0"/><text class="tick" x="34" y="18.0" text-anchor="end">14</text><text class="tick" x="75.3" y="208" text-anchor="middle">2</text><text class="tick" x="141.9" y="208" text-anchor="middle">3</text><text class="tick" x="208.4" y="208" text-anchor="middle">4</text><text class="tick" x="275.0" y="208" text-anchor="middle">5</text><text class="tick" x="341.6" y="208" text-anchor="middle">6</text><text class="tick" x="408.1" y="208" text-anchor="middle">7</text><text class="tick" x="474.7" y="208" text-anchor="middle">8</text><polyline class="s2-line" points="75.3,177.4 141.9,152.3 208.4,127.1 275.0,102.0 341.6,76.9 408.1,51.7 474.7,26.6" fill="none" stroke-width="2.5"/><circle class="s2-dot" cx="75.3" cy="177.4" r="3.5"><title>n = 2 : 2n − 3 = 1</title></circle><circle class="s1-dot" cx="75.3" cy="177.4" r="5"><title>n = 2 : 1 הפיכות</title></circle><text class="legend" x="75.3" y="191.4" text-anchor="middle">1</text><circle class="s2-dot" cx="141.9" cy="152.3" r="3.5"><title>n = 3 : 2n − 3 = 3</title></circle><circle class="s1-dot" cx="141.9" cy="152.3" r="5"><title>n = 3 : 3 הפיכות</title></circle><text class="legend" x="141.9" y="166.3" text-anchor="middle">3</text><circle class="s2-dot" cx="208.4" cy="127.1" r="3.5"><title>n = 4 : 2n − 3 = 5</title></circle><circle class="s1-dot" cx="208.4" cy="139.7" r="5"><title>n = 4 : 4 הפיכות</title></circle><text class="legend" x="208.4" y="153.7" text-anchor="middle">4</text><circle class="s2-dot" cx="275.0" cy="102.0" r="3.5"><title>n = 5 : 2n − 3 = 7</title></circle><circle class="s1-dot" cx="275.0" cy="127.1" r="5"><title>n = 5 : 5 הפיכות</title></circle><text class="legend" x="275.0" y="141.1" text-anchor="middle">5</text><circle class="s2-dot" cx="341.6" cy="76.9" r="3.5"><title>n = 6 : 2n − 3 = 9</title></circle><circle class="s1-dot" cx="341.6" cy="102.0" r="5"><title>n = 6 : 7 הפיכות</title></circle><text class="legend" x="341.6" y="116.0" text-anchor="middle">7</text><circle class="s2-dot" cx="408.1" cy="51.7" r="3.5"><title>n = 7 : 2n − 3 = 11</title></circle><circle class="s1-dot" cx="408.1" cy="89.4" r="5"><title>n = 7 : 8 הפיכות</title></circle><text class="legend" x="408.1" y="103.4" text-anchor="middle">8</text><circle class="s2-dot" cx="474.7" cy="26.6" r="3.5"><title>n = 8 : 2n − 3 = 13</title></circle><circle class="s1-dot" cx="474.7" cy="76.9" r="5"><title>n = 8 : 9 הפיכות</title></circle><text class="legend" x="474.7" y="90.9" text-anchor="middle">9</text><text class="tick" x="508" y="224" text-anchor="end">n</text></svg>

    <!-- /gen -->

    <!-- gen 5 -->

    <span class="viz-legend"><span><i class="pk-key-best"></i>המקרה הגרוע האמיתי (BFS)</span><span><i class="pk-key-bound"></i>החסם של האלגוריתם הפשוט, <span dir="ltr">2n − 3</span></span></span>

    <!-- /gen -->

    כדי למיין ערימה בפועל בכמה שפחות הפיכות, הולכים בגרף לאורך המרחקים : בכל ערימה בוחרים
    הפיכה שמביאה לערימה קרובה יותר ב-1. על הערימה של השאלה :

    <!-- gen 6 -->

    <div class="stepper" role="group" aria-label="הדרך הקצרה ביותר לאותה ערימה, חמש הפיכות" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="התחלה"><rect class="pk-cake" x="27.2" y="6" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">3</text><rect class="pk-cake" x="50.4" y="30" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">1</text><rect class="pk-cake" x="4.0" y="54" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">5</text><rect class="pk-cake" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake" x="38.8" y="102" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">2</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/></svg><figcaption>התחלה : <code>[3, 1, 5, 4, 2]</code>. ‏BFS אומר שמכאן צריך 5 הפיכות.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 1"><rect class="pk-cake" x="50.4" y="6" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">1</text><rect class="pk-cake" x="27.2" y="30" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">3</text><rect class="pk-cake" x="4.0" y="54" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">5</text><rect class="pk-cake" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake" x="38.8" y="102" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">2</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="50.0" rx="6"/></svg><figcaption>הפיכה 1 : הופכים את 2 העליונים. עכשיו <code>[1, 3, 5, 4, 2]</code>. נשארו 4 הפיכות.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 2"><rect class="pk-cake" x="15.6" y="6" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">4</text><rect class="pk-cake" x="4.0" y="30" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">5</text><rect class="pk-cake" x="27.2" y="54" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><rect class="pk-cake" x="50.4" y="78" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">1</text><rect class="pk-cake" x="38.8" y="102" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">2</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="98.0" rx="6"/></svg><figcaption>הפיכה 2 : הופכים את 4 העליונים. עכשיו <code>[4, 5, 3, 1, 2]</code>. נשארו 3 הפיכות.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 3"><rect class="pk-cake" x="4.0" y="6" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">5</text><rect class="pk-cake" x="15.6" y="30" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">4</text><rect class="pk-cake" x="27.2" y="54" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><rect class="pk-cake" x="50.4" y="78" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">1</text><rect class="pk-cake" x="38.8" y="102" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">2</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="50.0" rx="6"/></svg><figcaption>הפיכה 3 : הופכים את 2 העליונים. עכשיו <code>[5, 4, 3, 1, 2]</code>. נשארו 2 הפיכות.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 4"><rect class="pk-cake" x="38.8" y="6" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">2</text><rect class="pk-cake" x="50.4" y="30" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">1</text><rect class="pk-cake pk-done" x="27.2" y="54" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><rect class="pk-cake pk-done" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake pk-done" x="4.0" y="102" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">5</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="122.0" rx="6"/></svg><figcaption>הפיכה 4 : הופכים את 5 העליונים. עכשיו <code>[2, 1, 3, 4, 5]</code>. נשארה הפיכה אחת.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 138" style="max-width:9.4rem" role="img" aria-label="הפיכה 5"><rect class="pk-cake pk-done" x="50.4" y="6" width="49.2" height="20" rx="9"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">1</text><rect class="pk-cake pk-done" x="38.8" y="30" width="72.4" height="20" rx="9"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">2</text><rect class="pk-cake pk-done" x="27.2" y="54" width="95.6" height="20" rx="9"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><rect class="pk-cake pk-done" x="15.6" y="78" width="118.8" height="20" rx="9"/><text class="pk-num" x="75.0" y="93" text-anchor="middle">4</text><rect class="pk-cake pk-done" x="4.0" y="102" width="142.0" height="20" rx="9"/><text class="pk-num" x="75.0" y="117" text-anchor="middle">5</text><line class="pk-plate" x1="4" x2="146" y1="128" y2="128"/><rect class="pk-flipbox" x="2" y="2" width="146" height="50.0" rx="6"/></svg><figcaption>הפיכה 5 : הופכים את 2 העליונים. עכשיו <code>[1, 2, 3, 4, 5]</code>. <strong>ממוין, בחמש הפיכות במקום שבע.</strong></figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="6"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **צומת :** ערימה, כ-tuple של \( 1, \dots, n \) מלמעלה למטה.
    2. **מקור :** הערימה הממוינת, במרחק 0.
    3. **שכנים :** מכל ערימה, \( n - 1 \) הפיכות : של \( k = 2, \dots, n \) העליונים (הפיכה
       של אחד לא משנה כלום).
    4. **חיפוש לרוחב :** ‏BFS עם תור ומילון מרחקים. ערימה שכבר יש לה מרחק לא נכנסת שוב.
    5. **התשובה :** \( P(n) \) הוא המרחק הגדול ביותר במילון. כדי למיין ערימה, בכל צעד
       בוחרים \( k \) שמקטין את המרחק ב-1.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="pancake_distances" linenums="1" hl_lines="12 21 28"
        from collections import deque


        def pancake_distances(n):
            """The fewest flips that sort every stack of n: one BFS from the sorted stack."""
            start = tuple(range(1, n + 1))
            dist = {start: 0}
            queue = deque([start])
            while queue:
                s = queue.popleft()
                for k in range(2, n + 1):
                    t = s[:k][::-1] + s[k:]                   # (1)!
                    if t not in dist:
                        dist[t] = dist[s] + 1
                        queue.append(t)
            return dist


        def pancake_number(n):
            """P(n): the fewest flips that are enough for every stack of n."""
            return max(pancake_distances(n).values())


        def best_flips(stack, dist):
            """A shortest sorting: at each stack the smallest k that is one flip closer."""
            s, flips = tuple(stack), []
            while dist[s]:
                k = next(k for k in range(2, len(s) + 1) if dist[s[:k][::-1] + s[k:]] == dist[s] - 1)  # (2)!
                s = s[:k][::-1] + s[k:]
                flips.append(k)
            return flips
        ```

        1. מהממוינת אל \( t \) או מ-\( t \) אל הממוינת, אותו מספר הפיכות : כל הפיכה היא
           ההופכית של עצמה, ולכן הדרך הפוכה היא דרך.
        2. ערימה במרחק \( d > 0 \) הגיעה ל-BFS מערימה במרחק \( d - 1 \), ולכן תמיד יש
           \( k \) כזה.

    === "SystemVerilog"
        ```systemverilog title="function automatic int pancake_number" linenums="1" hl_lines="9 16 20"
        // P(n) for n <= 8: one BFS from the sorted stack over all n! stacks (depth: the flips from
        // the sorted one), a stack packed in an int, 4 bits a pancake, the top in the low bits.
        function automatic int pancake_number(int n);
          int depth[int];
          int queue[$];
          int s, t, d, worst = 0;
          int a[8];
          s = 0;
          for (int i = 0; i < n; i++) s |= (i + 1) << (4 * i);
          depth[s] = 0;
          queue.push_back(s);
          while (queue.size() > 0) begin
            s = queue.pop_front();
            d = depth[s];
            if (d > worst) worst = d;
            for (int i = 0; i < n; i++) a[i] = (s >> (4 * i)) & 15;     // (1)!
            for (int k = 2; k <= n; k++) begin
              t = s;
              for (int i = 0; i < k; i++)
                t = (t & ~(15 << (4 * i))) | (a[k - 1 - i] << (4 * i));   // (2)!
              if (!depth.exists(t)) begin
                depth[t] = d + 1;
                queue.push_back(t);
              end
            end
          end
          return worst;
        endfunction
        ```

        1. פורקים את הערימה : \( a[0] \) הוא העליון.
        2. ההפיכה : במקום \( i \) נכנס מה שהיה במקום \( k - 1 - i \), לכל \( i < k \).

    #### למה זה נכון { .sol-proof }

    **המרחק הוא מספר ההפיכות.** סדרת הפיכות שממיינת את \( s \) היא מסלול בגרף מ-\( s \)
    לערימה הממוינת, והאורך שלה הוא מספר ההפיכות. לכן הכי מעט הפיכות הוא אורך המסלול הקצר
    ביותר. כל הפיכה היא ההופכית של עצמה, אז אותו מסלול בכיוון ההפוך מוביל מהממוינת ל-\( s \),
    באותו אורך. ‏BFS מהממוינת מוצא את כל המרחקים האלה בבת אחת.

    **‏P(n) הוא המקסימום.** כל ערימה ממוינת ב-\( d(s) \le \max d \) הפיכות, וערימה שבה
    המרחק מקסימלי לא ממוינת בפחות. בטבלה : ‏\( P(5) = 5 \), ויש בדיוק 20 ערימות של 5 שצריכות
    5 הפיכות. ‏`[3, 1, 5, 4, 2]` היא אחת מהן, ולכן 5 הוא גם התשובה בשבילה, והאלגוריתם הפשוט
    מבזבז שתיים.

    **מה ידוע מעבר.** החיפוש נעשה כבד מהר : \( n! \) צמתים. מ-\( n = 9 \) והלאה הערכים חושבו
    בחיפושים מתוחכמים בהרבה. לגבי \( n \) גדול ידועים רק חסמים : ‏Gates ו-Papadimitriou הוכיחו
    ב-1979 שמספיקות בערך \( 5n/3 \) הפיכות, החסם העליון הטוב ביותר היום הוא בערך
    \( 18n/11 \), וידוע שיש ערימות שצריכות לפחות בערך \( 15n/14 \).

    **נסו בעצמכם.** לוחצים על פנקייק כדי להפוך אותו ואת כל מה שמעליו. הדף סופר הפיכות
    ומשווה למינימום של BFS. "רמז" מסמן הפיכה שמקרבת למיון, ו"הגרלה" נותנת ערימה חדשה :

    <div class="explorer" data-kind="pancake" data-n="5" data-burnt="0" data-stack="3,1,5,4,2"></div>

    #### סיבוכיות { .sol-cost }

    ‏\( n! \) ערימות, מכל אחת \( n - 1 \) הפיכות, וכל הפיכה בונה ערימה חדשה ב-\( O(n) \) :
    זמן \( O(n! \cdot n^2) \) וזיכרון \( O(n! \cdot n) \). ל-\( n = 8 \) אלה 40,320 ערימות.

---

### סעיף ג – פנקייקים שרופים { #part-c }

עכשיו לכל פנקייק יש צד שרוף. הפיכה הופכת גם את הפנקייקים עצמם : מי שהצד השרוף שלו היה
למטה, יוצא עם הצד השרוף למעלה, ולהפך. המטרה : ערימה ממוינת, וגם **כל הצדדים השרופים
למטה**. ברשימה, פנקייק שהצד השרוף שלו למעלה נכתב במספר שלילי : `[-1, -2, -3]` היא ערימה
ממוינת שכל הפנקייקים בה הפוכים. כתבו אלגוריתם עם חסם, ומצאו את המקרה הגרוע המדויק
ל-\( n \le 7 \).

??? tip "רמז 1"
    אותו רעיון של סעיף א, מהגדול לקטן. אחרי שהפנקייק \( k \) עלה לראש, באיזה כיוון הוא
    צריך להיות כדי שההפיכה שמורידה אותו תשאיר אותו עם הצד השרוף למטה?

??? tip "רמז 2"
    עכשיו גם הפיכה של פנקייק אחד היא מהלך : היא הופכת את העליון על הצד השני. כמה ערימות
    יש עכשיו?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        לכל \( k = n, \dots, 1 \) : מעלים את \( k \) לראש, הופכים אותו לבד אם הצד השרוף שלו
        למטה, ומורידים אותו. לכל היותר שלוש הפיכות לפנקייק, ואחת לאחרון : \( 3n - 2 \).
        ‏BFS על \( 2^n \cdot n! \) הערימות נותן את המקרה הגרוע : ‏1, 4, 6, 8, 10, 12, 14
        ל-\( n \) מ-1 עד 7. מ-\( n = 2 \) זה בדיוק \( 2n \), והערימה הממוינת שכל
        הפנקייקים בה הפוכים תמיד בין הקשות ביותר.

    <!-- cost: הפיכות \( 3n - 2 \) | ערימות \( 2^n \cdot n! \) -->

    #### הרעיון { .sol-idea }

    הפיכה של \( k \) העליונים מורידה את העליון למקום \( k - 1 \) **והופכת אותו**. לכן כדי
    שהוא יגיע למקומו עם הצד השרוף למטה, הוא צריך לעמוד בראש הערימה עם הצד השרוף **למעלה**.
    אם הוא עלה לראש בכיוון הלא נכון, הפיכה של אחד, של העליון בלבד, מתקנת את זה. זו ההפיכה
    השלישית שמתווספת לכל פנקייק.

    והמקרה הגרוע : המרחב גדל ל-\( 2^n \cdot n! \) ערימות, ושוב כל הפיכה היא ההופכית של עצמה
    (גם הסדר וגם הצדדים חוזרים). ‏BFS אחד מהערימה הממוינת, הפעם עם הפיכות של \( k = 1, \dots,
    n \). הערימה `[-1, -2, -3]` כבר ממוינת, ובכל זאת צריך שש הפיכות, המקסימום ל-\( n = 3 \) :

    <!-- gen 7 -->

    <div class="stepper" role="group" aria-label="ערימה ממוינת עם כל הצדדים השרופים למעלה, והדרך הקצרה ביותר שלה" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure pk-fig" viewBox="0 0 150 90" style="max-width:9.4rem" role="img" aria-label="התחלה"><rect class="pk-cake" x="42.7" y="6" width="64.7" height="20" rx="9"/><rect class="pk-burnt" x="47.7" y="6" width="54.7" height="4" rx="2"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">1</text><rect class="pk-cake" x="23.3" y="30" width="103.3" height="20" rx="9"/><rect class="pk-burnt" x="28.3" y="30" width="93.3" height="4" rx="2"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">2</text><rect class="pk-cake" x="4.0" y="54" width="142.0" height="20" rx="9"/><rect class="pk-burnt" x="9.0" y="54" width="132.0" height="4" rx="2"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><line class="pk-plate" x1="4" x2="146" y1="80" y2="80"/></svg><figcaption>התחלה : הערימה ממוינת, אבל כל הצדדים השרופים למעלה. ברשימה <code>[-1, -2, -3]</code> : מספר שלילי הוא פנקייק שהצד השרוף שלו למעלה.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 90" style="max-width:9.4rem" role="img" aria-label="הפיכה 1"><rect class="pk-cake" x="23.3" y="6" width="103.3" height="20" rx="9"/><rect class="pk-burnt" x="28.3" y="22" width="93.3" height="4" rx="2"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">2</text><rect class="pk-cake" x="42.7" y="30" width="64.7" height="20" rx="9"/><rect class="pk-burnt" x="47.7" y="46" width="54.7" height="4" rx="2"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">1</text><rect class="pk-cake" x="4.0" y="54" width="142.0" height="20" rx="9"/><rect class="pk-burnt" x="9.0" y="54" width="132.0" height="4" rx="2"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><line class="pk-plate" x1="4" x2="146" y1="80" y2="80"/><rect class="pk-flipbox" x="2" y="2" width="146" height="50.0" rx="6"/></svg><figcaption>הפיכה 1 : הופכים את 2 העליונים. עכשיו <code>[2, 1, -3]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 90" style="max-width:9.4rem" role="img" aria-label="הפיכה 2"><rect class="pk-cake" x="4.0" y="6" width="142.0" height="20" rx="9"/><rect class="pk-burnt" x="9.0" y="22" width="132.0" height="4" rx="2"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">3</text><rect class="pk-cake" x="42.7" y="30" width="64.7" height="20" rx="9"/><rect class="pk-burnt" x="47.7" y="30" width="54.7" height="4" rx="2"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">1</text><rect class="pk-cake" x="23.3" y="54" width="103.3" height="20" rx="9"/><rect class="pk-burnt" x="28.3" y="54" width="93.3" height="4" rx="2"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">2</text><line class="pk-plate" x1="4" x2="146" y1="80" y2="80"/><rect class="pk-flipbox" x="2" y="2" width="146" height="74.0" rx="6"/></svg><figcaption>הפיכה 2 : הופכים את 3 העליונים. עכשיו <code>[3, -1, -2]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 90" style="max-width:9.4rem" role="img" aria-label="הפיכה 3"><rect class="pk-cake" x="42.7" y="6" width="64.7" height="20" rx="9"/><rect class="pk-burnt" x="47.7" y="22" width="54.7" height="4" rx="2"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">1</text><rect class="pk-cake" x="4.0" y="30" width="142.0" height="20" rx="9"/><rect class="pk-burnt" x="9.0" y="30" width="132.0" height="4" rx="2"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">3</text><rect class="pk-cake" x="23.3" y="54" width="103.3" height="20" rx="9"/><rect class="pk-burnt" x="28.3" y="54" width="93.3" height="4" rx="2"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">2</text><line class="pk-plate" x1="4" x2="146" y1="80" y2="80"/><rect class="pk-flipbox" x="2" y="2" width="146" height="50.0" rx="6"/></svg><figcaption>הפיכה 3 : הופכים את 2 העליונים. עכשיו <code>[1, -3, -2]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 90" style="max-width:9.4rem" role="img" aria-label="הפיכה 4"><rect class="pk-cake" x="23.3" y="6" width="103.3" height="20" rx="9"/><rect class="pk-burnt" x="28.3" y="22" width="93.3" height="4" rx="2"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">2</text><rect class="pk-cake" x="4.0" y="30" width="142.0" height="20" rx="9"/><rect class="pk-burnt" x="9.0" y="46" width="132.0" height="4" rx="2"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">3</text><rect class="pk-cake" x="42.7" y="54" width="64.7" height="20" rx="9"/><rect class="pk-burnt" x="47.7" y="54" width="54.7" height="4" rx="2"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">1</text><line class="pk-plate" x1="4" x2="146" y1="80" y2="80"/><rect class="pk-flipbox" x="2" y="2" width="146" height="74.0" rx="6"/></svg><figcaption>הפיכה 4 : הופכים את 3 העליונים. עכשיו <code>[2, 3, -1]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 90" style="max-width:9.4rem" role="img" aria-label="הפיכה 5"><rect class="pk-cake" x="4.0" y="6" width="142.0" height="20" rx="9"/><rect class="pk-burnt" x="9.0" y="6" width="132.0" height="4" rx="2"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">3</text><rect class="pk-cake" x="23.3" y="30" width="103.3" height="20" rx="9"/><rect class="pk-burnt" x="28.3" y="30" width="93.3" height="4" rx="2"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">2</text><rect class="pk-cake" x="42.7" y="54" width="64.7" height="20" rx="9"/><rect class="pk-burnt" x="47.7" y="54" width="54.7" height="4" rx="2"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">1</text><line class="pk-plate" x1="4" x2="146" y1="80" y2="80"/><rect class="pk-flipbox" x="2" y="2" width="146" height="50.0" rx="6"/></svg><figcaption>הפיכה 5 : הופכים את 2 העליונים. עכשיו <code>[-3, -2, -1]</code>.</figcaption></figure><figure class="stepper-frame"><svg class="figure pk-fig" viewBox="0 0 150 90" style="max-width:9.4rem" role="img" aria-label="הפיכה 6"><rect class="pk-cake pk-done" x="42.7" y="6" width="64.7" height="20" rx="9"/><rect class="pk-burnt" x="47.7" y="22" width="54.7" height="4" rx="2"/><text class="pk-num" x="75.0" y="21" text-anchor="middle">1</text><rect class="pk-cake pk-done" x="23.3" y="30" width="103.3" height="20" rx="9"/><rect class="pk-burnt" x="28.3" y="46" width="93.3" height="4" rx="2"/><text class="pk-num" x="75.0" y="45" text-anchor="middle">2</text><rect class="pk-cake pk-done" x="4.0" y="54" width="142.0" height="20" rx="9"/><rect class="pk-burnt" x="9.0" y="70" width="132.0" height="4" rx="2"/><text class="pk-num" x="75.0" y="69" text-anchor="middle">3</text><line class="pk-plate" x1="4" x2="146" y1="80" y2="80"/><rect class="pk-flipbox" x="2" y="2" width="146" height="74.0" rx="6"/></svg><figcaption>הפיכה 6 : הופכים את 3 העליונים. עכשיו <code>[1, 2, 3]</code>. <strong>ממוין, וכל הצדדים השרופים למטה, אחרי 6 הפיכות.</strong></figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="7"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <!-- /gen -->

    <!-- gen 8 -->

    <span class="viz-legend"><span><i class="pk-key-cake"></i>פנקייק, רחב כמו הגודל שלו</span><span><i class="pk-key-burnt"></i>הצד השרוף</span><span><i class="pk-key-flip"></i>הפנקייקים שההפיכה הפכה</span><span><i class="pk-key-done"></i>במקום הסופי</span><span><i class="pk-key-plate"></i>הצלחת</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מהגדול לקטן :** \( k = n, \dots, 1 \). אם \( k \) במקומו והצד השרוף שלו למטה,
       עוברים הלאה.
    2. **מעלים :** אם הוא לא בראש, הפיכה של \( p + 1 \) מעלה אותו.
    3. **מכוונים :** אם בראש הצד השרוף שלו למטה, הפיכה של 1 הופכת אותו.
    4. **מורידים :** הפיכה של \( k \) מורידה אותו למקומו, עם הצד השרוף למטה.
    5. **מרחק מדויק :** אותו BFS של סעיף ב, צמתים עם סימן, והפיכות מ-1 עד \( n \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="burnt_simple" linenums="1" hl_lines="15 18 20"
        def burnt_flip(stack, k):
            """Turn the top k over: the order reverses and each one shows its other side
            (a negative size: the burnt side is up)."""
            return [-x for x in stack[:k][::-1]] + stack[k:]


        def burnt_simple(stack):
            """Largest first, three flips a pancake at most: up, turn, down."""
            s, flips = list(stack), []
            for k in range(len(s), 0, -1):
                p = [abs(x) for x in s].index(k)
                if p == k - 1 and s[p] > 0:
                    continue                          # in place, burnt side down
                if p > 0:
                    s = burnt_flip(s, p + 1)          # (1)!
                    flips.append(p + 1)
                if s[0] > 0:
                    s = burnt_flip(s, 1)              # (2)!
                    flips.append(1)
                s = burnt_flip(s, k)                  # (3)!
                flips.append(k)
            return s, flips


        def burnt_distances(n):
            """The fewest flips for every burnt stack of n: one BFS, flips of 1 to n."""
            start = tuple(range(1, n + 1))
            dist = {start: 0}
            queue = deque([start])
            while queue:
                s = queue.popleft()
                for k in range(1, n + 1):
                    t = tuple(-x for x in s[:k][::-1]) + s[k:]
                    if t not in dist:
                        dist[t] = dist[s] + 1
                        queue.append(t)
            return dist
        ```

        1. ‏\( k \) עולה לראש, והפעם גם מתהפך.
        2. בראש, הצד השרוף למטה : הפיכה של העליון לבד מעלה אותו למעלה.
        3. בירידה \( k \) מתהפך שוב, ומגיע למקומו עם הצד השרוף למטה.

    === "SystemVerilog"
        ```systemverilog title="function automatic int burnt_simple" linenums="1" hl_lines="8 23 26"
        // Turn the top k over: the order reverses and each one changes side (negative: burnt up).
        function automatic void burnt_flip(ref int s[$], input int k);
          int i = 0, j = k - 1, t;
          while (i < j) begin
            t = s[i]; s[i] = -s[j]; s[j] = -t;
            i++; j--;
          end
          if (i == j) s[i] = -s[i];                    // (1)!
        endfunction

        // Largest first, up to three flips a pancake; returns the number of flips.
        function automatic int burnt_simple(ref int s[$], output string flips);
          int n = s.size(), count = 0, p;
          flips = "";
          for (int k = n; k >= 1; k--) begin
            for (p = 0; s[p] != k && s[p] != -k; p++) ;
            if (p == k - 1 && s[p] > 0) continue;
            if (p > 0) begin
              burnt_flip(s, p + 1); count++;
              flips = {flips, $sformatf("%0d ", p + 1)};
            end
            if (s[0] > 0) begin
              burnt_flip(s, 1); count++;               // (2)!
              flips = {flips, "1 "};
            end
            burnt_flip(s, k); count++;
            flips = {flips, $sformatf("%0d ", k)};
          end
          return count;
        endfunction
        ```

        1. במספר אי-זוגי של פנקייקים, האמצעי לא זז אבל מתהפך.
        2. הצד השרוף של העליון למטה : הופכים אותו לבד.

    #### למה זה נכון { .sol-proof }

    **נכונות.** כמו בסעיף א, לפני הסיבוב של \( k \) הפנקייקים \( k + 1, \dots, n \) במקומם,
    עם הצד השרוף למטה, וההפיכות של הסיבוב לא נוגעות בהם. אחרי שלב "מכוונים" \( k \) בראש עם
    הצד השרוף למעלה, וההפיכה של \( k \) מורידה אותו למקום \( k - 1 \) והופכת אותו, עם הצד
    השרוף למטה. בסיבוב של 1 הוא כבר בראש : לכל היותר הפיכה אחת שלו לבד.

    **ספירה.** לכל היותר שלוש הפיכות לכל \( k \ge 2 \) ואחת ל-1 : \( 3(n - 1) + 1 = 3n - 2 \).
    החסם הדוק לאלגוריתם : הטסט מריץ אותו על כל הערימות עד \( n = 6 \), והמקסימום הוא
    בדיוק \( 3n - 2 \).

    **המקרה הגרוע.** הפיכה של אותם \( k \) פעמיים מחזירה גם את הסדר וגם את הצדדים, ולכן
    אותו נימוק של סעיף ב : BFS אחד מהערימה הממוינת נותן את כל המרחקים :

    <!-- gen 9 -->

    | ‏n | המקרה הגרוע | ערימות קשות | ממוינת והפוכה | האלגוריתם הפשוט | ‏\( 3n - 2 \) |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | 1 | 1 | 1 | 1 | 1 | 1 |
    | 2 | 4 | 1 | 4 | 4 | 4 |
    | 3 | 6 | 2 | 6 | 7 | 7 |
    | 4 | 8 | 3 | 8 | 10 | 10 |
    | 5 | 10 | 4 | 10 | 13 | 13 |
    | 6 | 12 | 1 | 12 | 16 | 16 |
    | 7 | 14 | 1 | 14 | ‏– | 19 |

    <!-- /gen -->

    העמודה "ממוינת והפוכה" היא המרחק של `[-1, -2, ..., -n]`, הערימה הממוינת שכל הפנקייקים בה
    הפוכים. עד \( n = 7 \) היא תמיד בין הקשות ביותר, וב-6 וב-7 היא הקשה היחידה. התבנית
    \( 2n \) לא נמשכת : ב-\( n = 8 \) ידוע ש-15 הפיכות מספיקות לכל ערימה.

    **נסו בעצמכם.** אותה תיבה, עם צדדים שרופים : לחיצה על פנקייק הופכת אותו ואת כל מה שמעליו,
    כולל הצדדים. הפס העבה הוא הצד השרוף :

    <div class="explorer" data-kind="pancake" data-n="3" data-burnt="1" data-stack="-1,-2,-3"></div>

    #### סיבוכיות { .sol-cost }

    האלגוריתם : לכל היותר \( 3n - 2 \) הפיכות, זמן \( O(n^2) \). ה-BFS : ‏\( 2^n \cdot n! \)
    ערימות ו-\( n \) הפיכות מכל אחת. ל-\( n = 7 \) אלה 645,120 ערימות.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : מהקטן לגדול"
    "מעלים את הקטן ביותר לראש" לא מתקדם לשום מקום : הפיכה הבאה, כדי לסדר את השני, תזיז
    אותו שוב. הפיכה נוגעת רק בחלק העליון, ולכן מה שמסודר סופית חייב להיות בתחתית. מתחילים
    מהגדול.

??? trap "מלכודת : האלגוריתם הפשוט הוא לא האופטימום"
    ‏\( 2n - 3 \) הוא חסם על האלגוריתם, לא על הבעיה. `[3, 1, 5, 4, 2]` לוקחת לו 7 הפיכות,
    ו-5 מספיקות. כבר ב-\( n = 8 \) הפער הוא 13 מול 9.

??? trap "מלכודת : BFS מכל ערימה בנפרד"
    כדי לדעת את המרחק של כל הערימות, אין צורך ב-\( n! \) חיפושים. כל הפיכה היא ההופכית של
    עצמה, ולכן המרחק מ-\( s \) לממוינת שווה למרחק מהממוינת ל-\( s \) : חיפוש אחד מהממוינת
    נותן את כולם.

??? trap "מלכודת : לשכוח שהפיכה הופכת גם את הצד"
    בפנקייקים שרופים, פנקייק שעלה לראש והורד מיד מגיע למקומו בכיוון ההפוך מזה שהיה לו
    בראש. מי שמעתיק את סעיף א כמו שהוא מקבל ערימה ממוינת עם חלק מהצדדים השרופים למעלה.

??? followup "שאלות המשך"
    - **חסם תחתון בלי חיפוש :** איך מוכיחים ש-`[3, 1, 5, 4, 2]` צריכה לפחות כמה הפיכות,
      בלי BFS?

        ??? fu-answer "תשובה"
            סופרים "שכנויות שבורות" : זוגות סמוכים שאינם גדלים עוקבים, כשהצלחת היא
            \( n + 1 \) מתחת לערימה. הפיכה משנה רק את הזוג שבנקודת החיתוך, ולכן מתקנת לכל
            היותר שבירה אחת. ב-`[3, 1, 5, 4, 2]` יש 4, ולכן צריך לפחות 4 הפיכות. האמת היא 5.

    - **ערימה אחת גדולה :** האם אפשר למצוא את המספר המינימלי לערימה של 100 פנקייקים?

        ??? fu-answer "תשובה"
            לא ביעילות, ככל הידוע : ב-2015 הוכח שמציאת המספר המינימלי של הפיכות לערימה נתונה
            היא בעיה NP-קשה. בפועל משתמשים ב-A* או ב-IDA* עם השכנויות השבורות כהערכה.

    - **למה זה מעניין מחוץ למטבח :** איפה מופיעות הפיכות של רישא?

        ??? fu-answer "תשובה"
            ברשתות קישור בין מעבדים (גרף הפנקייקים הוא טופולוגיה עם קוטר קטן), ובביולוגיה,
            כמודל להיפוכים של מקטעי DNA. הפנקייקים השרופים הם מקטעים עם כיוון.
