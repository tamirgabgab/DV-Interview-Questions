---
id: 11
title: לוח סיום אקראי של איקס-עיגול
level: senior
difficulty: medium
kind: dv
tags: [systemverilog, constraints, randomization, combinatorics, math, python]
source: ""
added: 2026-10-16
---

## השאלה

צריך לייצר, באופן אקראי, **לוח שבו נגמר משחק איקס-עיגול** על לוח של 3 על 3, ויחד איתו משתנה
שמתאר את **התוצאה** : X ניצח, O ניצח או תיקו. X תמיד מתחיל, והשחקנים משחקים לסירוגין.

הלוח **לא חייב להיות מלא**. משחק נגמר ברגע שאחד השחקנים משלים שלישייה בשורה, בטור או
באלכסון, ולכן אפשר לנצח גם לפני שכל המשבצות מלאות.

- **ב-SystemVerilog :** class עם משתנים מסוג `rand` ו-constraints, כך שכל קריאה ל-`randomize()`
  מחזירה לוח חוקי ותוצאה שמתאימה לו.
- **ב-Python :** פונקציה שמחזירה תוצאה ולוח אקראיים עם אותם תנאים.

המשבצות ממוספרות מ-0 עד 8, שורה אחרי שורה :

<svg class="figure" viewBox="0 0 110 110" style="max-width:8rem" role="img" aria-label="מספור המשבצות 0 עד 8, שורה אחרי שורה"><g><text class="box-num" x="21.0" y="26.0" text-anchor="middle">0</text><text class="box-num" x="55.0" y="26.0" text-anchor="middle">1</text><text class="box-num" x="89.0" y="26.0" text-anchor="middle">2</text><text class="box-num" x="21.0" y="60.0" text-anchor="middle">3</text><text class="box-num" x="55.0" y="60.0" text-anchor="middle">4</text><text class="box-num" x="89.0" y="60.0" text-anchor="middle">5</text><text class="box-num" x="21.0" y="94.0" text-anchor="middle">6</text><text class="box-num" x="55.0" y="94.0" text-anchor="middle">7</text><text class="box-num" x="89.0" y="94.0" text-anchor="middle">8</text><line class="ttt-grid" x1="38" x2="38" y1="4" y2="106"/><line class="ttt-grid" x1="4" x2="106" y1="38" y2="38"/><line class="ttt-grid" x1="72" x2="72" y1="4" y2="106"/><line class="ttt-grid" x1="4" x2="106" y1="72" y2="72"/></g></svg>

??? interviewer "מה המראיין בודק"
    - **רשימת תנאים מלאה :** האם מגיעים לכל התנאים שלוח סיום אמיתי מקיים, או עוצרים אחרי
      "למישהו יש שלישייה". יש תנאי אחד שרוב המועמדים שוכחים, והוא מייצר לוחות שלא יכולים
      לקרות במשחק.
    - **לא לדרוש יותר מדי :** constraint חזק מדי הוא באג באימות, כי הוא מסתיר מצבים אמיתיים
      מהבדיקות. המראיין בודק אם מוודאים שכל לוח חוקי עדיין אפשרי.
    - **ספירות בשפת ה-constraints :** איך מבטאים "כמה X יש על הלוח" ו"האם שורה מלאה" בצורה
      שה-solver מבין, ומה תפקידם של משתני עזר מסוג `rand`.
    - **שליטה בהתפלגות :** מה `solve ... before` משנה ומה הוא לא משנה, ולמה זה חשוב כשיש
      תוצאה נדירה.
    - **בדיקה עצמאית :** איך מוודאים שה-constraints נכונים בלי להסתמך עליהם עצמם.

---

### סעיף א – הלוח הרגיל

מהם **כל** התנאים שלוח צריך לקיים כדי שיהיה סוף של משחק אמיתי? ממשו את המחלקה.

??? tip "רמז 1"
    כמה X וכמה O יכולים להיות על הלוח? ומי עשה את המהלך האחרון אם X ניצח?

??? tip "רמז 2"
    האם ייתכן ששני השחקנים השלימו שלישייה? והאם ייתכן שלשחקן אחד יש **שתי** שלישיות?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ארבעה תנאים : \( n_X = n_O \) או \( n_X = n_O + 1 \); X ניצח רק אם יש לו שלישייה, ל-O
        אין, ו-\( n_X = n_O + 1 \); O ניצח רק אם יש לו שלישייה, ל-X אין, ו-\( n_X = n_O \);
        תיקו הוא לוח מלא בלי שלישיות. **יש בדיוק 958 לוחות סיום** : 626 ניצחונות של X,
        316 של O ו-16 תיקו.

    <!-- cost: סריקה \( 3^9 \) לוחות | הגרלה \( O(1) \) | זיכרון 958 לוחות -->

    #### הרעיון { .sol-idea }

    המשחק לסירוגין קובע את הספירה, והעובדה שהמשחק **נעצר** ברגע הניצחון קובעת את השאר : למנצח
    יש שלישייה, למפסיד אין, ומי שניצח הוא זה ששיחק אחרון. כל תנאי כזה הופך ל-constraint על
    משתני עזר שה-solver מחייב להיות שווים לספירה האמיתית על הלוח.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מספר הסימנים :** נסמן ב-\( n_X, n_O \) את מספר ה-X וה-O על הלוח. X מתחיל ומשחקים
       לסירוגין, ולכן \( n_X = n_O \) או \( n_X = n_O + 1 \).
    2. ‏**X ניצח :** נסמן ב-\( L_X, L_O \) את מספר השלישיות (שורות, טורים ואלכסונים) שכל שחקן
       השלים. אז \( L_X \ge 1 \), \( L_O = 0 \), ו-\( n_X = n_O + 1 \). המהלך האחרון היה של X,
       כי המשחק נעצר ברגע הניצחון.
    3. ‏**O ניצח :** \( L_O \ge 1 \), \( L_X = 0 \), ו-\( n_X = n_O \).
    4. **תיקו :** הלוח מלא (\( n_X = 5, n_O = 4 \)), ולאף שחקן אין שלישייה.
    5. **מתרגמים ל-constraints :** הלוח והתוצאה הם `rand`, וגם משתני העזר (`n_x`, `x_line`
       וכו') הם `rand`. constraints של שוויון מחייבים אותם להיות שווים לספירה על הלוח, ושלוש
       אימפליקציות קושרות את התוצאה לתנאים 2 עד 4.
    6. **קובעים את ההתפלגות :** `solve result before board`, כדי שכל תוצאה תתקבל בשליש
       מהמקרים ולא לפי מספר הלוחות שלה.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        כל תנאי הופך ל-constraint. משתני העזר (`n_x`, `x_line` וכו') הם גם `rand`, וה-constraints
        מחייבים אותם להיות שווים לספירה האמיתית על הלוח :

        ```systemverilog title="class ttt_end" linenums="1" hl_lines="38 39 40 41"
        typedef enum bit [1:0] {EMPTY, X, O} cell_e;
        typedef enum bit [1:0] {X_WINS, O_WINS, DRAW} result_e;
        typedef cell_e board_t[9];

        class ttt_end;
          // Cells are numbered 0..8 row by row. The last 4 lines are used only in part b.
          static const int LINES[12][3] = '{'{0, 1, 2}, '{3, 4, 5}, '{6, 7, 8},   // rows
                                            '{0, 3, 6}, '{1, 4, 7}, '{2, 5, 8},   // columns
                                            '{0, 4, 8}, '{2, 4, 6},               // diagonals
                                            '{1, 5, 6}, '{2, 3, 7},               // wrap-around
                                            '{0, 5, 7}, '{1, 3, 8}};              // (part b)
          int n_lines = 8;                     // 8 = classic board, 12 = part b

          rand board_t  board;
          rand result_e result;   // (1)!
          rand int      n_x, n_o;              // how many X / O are on the board
          rand bit      x_line[12], o_line[12];// line l is complete for X / for O
          rand int      x_lines, o_lines;      // how many complete lines each one has

          constraint c_count {
            n_x == board.sum() with (int'(item == X));   // (2)!
            n_o == board.sum() with (int'(item == O));
            n_x inside {n_o, n_o + 1};         // X starts and the players alternate
          }

          constraint c_lines {
            foreach (x_line[l]) {
              x_line[l] == (l < n_lines && board[LINES[l][0]] == X &&   // (3)!
                            board[LINES[l][1]] == X && board[LINES[l][2]] == X);
              o_line[l] == (l < n_lines && board[LINES[l][0]] == O &&
                            board[LINES[l][1]] == O && board[LINES[l][2]] == O);
            }
            x_lines == x_line.sum() with (int'(item));   // (4)!
            o_lines == o_line.sum() with (int'(item));
          }

          constraint c_result {
            (result == X_WINS) -> (x_lines > 0 && o_lines == 0 && n_x == n_o + 1);   // (5)!
            (result == O_WINS) -> (o_lines > 0 && x_lines == 0 && n_x == n_o);
            (result == DRAW)   -> (x_lines == 0 && o_lines == 0 && n_x + n_o == 9);   // (6)!
            solve result before board;          // every possible result is equally likely
          }

          function string show();
            string s = "";
            foreach (board[i])
              s = {s, (board[i] == X) ? "X" : (board[i] == O) ? "O" : ".", (i % 3 == 2) ? "\n" : " "};
            return s;
          endfunction
        endclass
        ```

        1. גם התוצאה היא `rand` : ה-solver בוחר אותה יחד עם הלוח, בכפוף ל-`c_result`. זה מה
           שמאפשר אחר כך לתת לה עדיפות עם `solve ... before`.
        2. ספירה בתוך constraint : `sum() with` רץ על מערך `rand`, והשוויון הופך את `n_x`
           למשתנה שנגזר מהלוח. בלי השוויון הזה `n_x` היה מוגרל בנפרד, בלי שום קשר ללוח.
        3. ‏`l < n_lines` מכבה את ארבעת הקווים האחרונים בלוח הרגיל. `n_lines` אינו `rand`, ולכן
           מבחינת ה-solver הוא קבוע, ואפשר לשנות אותו בין קריאות (סעיף ב) בלי לגעת
           ב-constraints.
        4. ‏`with (int'(item))` הוא לא קישוט : `sum()` על מערך של `bit` מחזיר תוצאה ברוחב של
           איבר אחד, כלומר ביט אחד, ושתי שלישיות היו נספרות כ-0. ההמרה ל-`int` נותנת ספירה
           אמיתית.
        5. אימפליקציה ולא שוויון : `->` אומר "אם התוצאה היא X_WINS אז התנאים מתקיימים". שלושת
           התנאים זרים זה לזה, ולכן ביחד הם קובעים את התוצאה באופן חד-משמעי לכל לוח חוקי.
        6. תיקו דורש לוח **מלא** : `n_x + n_o == 9`. בלי התנאי הזה לוח ריק או לוח באמצע המשחק
           היה "תיקו" חוקי.

        **מה `solve result before board` משנה.** בלי השורה הזו, ה-solver בוחר **לוח** אחיד
        מבין כל 958 הפתרונות. אז X מנצח בכ-65% מהמקרים (626 מתוך 958), ותיקו יוצא רק ב-1.7%
        (16 מתוך 958). בבדיקות אימות זה אומר שהמקרה הנדיר כמעט לא נבדק. עם
        `solve result before board` ה-solver בוחר קודם תוצאה אפשרית, בהסתברות שווה, ורק אחר
        כך לוח אחיד מבין הלוחות עם התוצאה הזו, וכל תוצאה מקבלת שליש. חשוב להבין
        ש-`solve ... before` **לא משנה את מרחב הפתרונות**, רק את ההסתברות של כל פתרון : אותם
        958 לוחות חוקיים, בהתפלגות אחרת.

        שימוש :

        ```systemverilog title="usage"
        ttt_end t = new();
        repeat (3) begin
          if (!t.randomize()) $fatal(1, "randomize() failed");
          $display("%s\n%s", t.result.name(), t.show());
        end
        ```

        **בדיקה עצמאית.** כדאי לבדוק את ה-constraints עם קוד **אחר**, שלא נכתב באותה צורה.
        הפונקציה הבאה מקבלת לוח ומחזירה אם הוא לוח סיום, ומה התוצאה :

        ```systemverilog title="function final_result" linenums="1" hl_lines="16 18 22"
        // 1 when `board` can be the end of a game that X started; `result` tells who won
        function automatic bit final_result(board_t board, int n_lines, output result_e result);
          int n_x = 0, n_o = 0, x_lines = 0, o_lines = 0;
          foreach (board[i]) begin
            n_x += (board[i] == X);   // (1)!
            n_o += (board[i] == O);
          end
          for (int l = 0; l < n_lines; l++) begin
            x_lines += (board[ttt_end::LINES[l][0]] == X && board[ttt_end::LINES[l][1]] == X &&   // (2)!
                        board[ttt_end::LINES[l][2]] == X);
            o_lines += (board[ttt_end::LINES[l][0]] == O && board[ttt_end::LINES[l][1]] == O &&
                        board[ttt_end::LINES[l][2]] == O);
          end

          result = DRAW;
          if (n_x != n_o && n_x != n_o + 1) return 0;          // X starts, players alternate (3)
          if (x_lines > 0 && o_lines == 0 && n_x == n_o + 1) begin
            result = X_WINS;                                    // X made the last move (4)
            return 1;
          end
          if (o_lines > 0 && x_lines == 0 && n_x == n_o) begin
            result = O_WINS;                                    // O made the last move
            return 1;
          end
          return x_lines == 0 && o_lines == 0 && n_x + n_o == 9;   // full board, nobody won (5)
        endfunction
        ```

        1. השוואה מחזירה `bit`, והחיבור ל-`int` סופר אותו. זו ספירה פרוצדורלית רגילה, בכוונה
           שונה מ-`sum() with` של המחלקה, כדי ששתי הדרכים לא יחלקו את אותה טעות.
        2. ‏`ttt_end::LINES` נגיש דרך שם המחלקה כי הוא `static const` : הפונקציה לא צריכה אובייקט,
           ורשימת הקווים נשארת במקום אחד.
        3. קודם פוסלים לוחות שלא יכולים להיווצר במשחק לסירוגין, ורק אחר כך שואלים מי ניצח.
           לוח עם שלישייה של X אבל 4 X מול 1 O נפסל כאן, לא בבדיקת הניצחון.
        4. ניצחון של X מחייב \( n_X = n_O + 1 \) : מי שניצח שיחק אחרון. לוח עם שלישייה של X
           ו-\( n_X = n_O \) אומר ש-O שיחק **אחרי** שהמשחק נגמר, והפונקציה מחזירה 0 עליו.
        5. תיקו הוא לוח מלא בלי אף שלישייה. לוח **לא** מלא בלי שלישיות הוא משחק באמצע, ולכן
           התוצאה כאן 0.

    === "Python"
        ב-Python אין solver, אבל הלוח קטן : יש רק \( 3^9 = 19{,}683 \) מילויים אפשריים. עוברים על
        כולם פעם אחת, שומרים את החוקיים לפי תוצאה, ובוחרים מהם. זה בדיוק מה ש-`randomize()` עם
        `solve result before board` מבטיח : קודם תוצאה אפשרית בהסתברות שווה, ואחר כך לוח אחיד מבין
        הלוחות עם התוצאה הזו.

        ```python title="randomize" linenums="1" hl_lines="48 49"
        import random
        from functools import cache
        from itertools import product

        X, O, EMPTY = "X", "O", "."

        # Cells are numbered 0..8 row by row:   0 1 2 / 3 4 5 / 6 7 8
        LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8),     # rows
                 (0, 3, 6), (1, 4, 7), (2, 5, 8),     # columns
                 (0, 4, 8), (2, 4, 6))                # diagonals


        def count_lines(board, player, lines):
            return sum(all(board[i] == player for i in line) for line in lines)


        def final_result(board, lines=LINES):
            """"X", "O" or "draw" when `board` can be the end of a game that X started, else None."""
            n_x, n_o = board.count(X), board.count(O)
            x_lines, o_lines = count_lines(board, X, lines), count_lines(board, O, lines)

            if n_x not in (n_o, n_o + 1):                 # X starts and the players alternate
                return None
            if x_lines > 0 and o_lines == 0 and n_x == n_o + 1:  # (1)!
                return "X"                                # X made the last move
            if o_lines > 0 and x_lines == 0 and n_x == n_o:
                return "O"                                # O made the last move
            if x_lines == 0 and o_lines == 0 and n_x + n_o == 9:
                return "draw"                             # full board, nobody won
            return None


        @cache  # (2)!
        def final_boards(lines=LINES):
            """Every legal final board (out of all 3^9 fillings), grouped by result."""
            groups = {"X": [], "O": [], "draw": []}
            for board in product((X, O, EMPTY), repeat=9):  # (3)!
                result = final_result(board, lines)
                if result:
                    groups[result].append(board)
            return groups


        def randomize(lines=LINES, rng=random):
            """Like SV randomize() with "solve result before board": first a result that has at
            least one board, uniformly, then a board with that result, uniformly."""
            groups = final_boards(lines)
            result = rng.choice([r for r in groups if groups[r]])  # (4)!
            return result, rng.choice(groups[result])  # (5)!


        def show(board):
            return "\n".join(" ".join(board[r * 3:r * 3 + 3]) for r in range(3))
        ```

        1. הסדר של הבדיקות חשוב : קודם ספירה, ואז ניצחון של X עם \( n_X = n_O + 1 \). שלישייה
           של X על לוח עם \( n_X = n_O \) נופלת לתנאי הבא, נכשלת שם כי \( L_X \ne 0 \), ומגיעה
           ל-`None` : O שיחק אחרי הניצחון.
        2. ‏`@cache` שומר את תוצאת הסריקה לכל קבוצת קווים, ולכן 19,683 הלוחות נבדקים פעם אחת
           בלבד. בגלל זה `lines` חייב להיות tuple ולא רשימה : ארגומנט של פונקציה עם cache חייב
           להיות hashable.
        3. ‏`product` מייצר את כל \( 3^9 \) המילויים, כולל לא חוקיים, ו-`final_result` מסננת.
           זה המקביל הישיר ל"מרחב הפתרונות" שה-solver עובר עליו.
        4. בוחרים רק מבין תוצאות שיש להן לפחות לוח אחד. זה בדיוק `solve result before board`,
           ובסעיף ב זה גם מה שמשמיט את התיקו מעצמו, בלי קוד מיוחד.
        5. לוח אחיד מבין הלוחות של התוצאה שנבחרה : השלב השני של `solve ... before`.

    !!! note "איך נבדק הקוד"
        ‏`final_result` נבדקה מול סריקה מלאה של עץ המשחק, גם ב-Python וגם ב-SystemVerilog
        ב-Verilator : היא מקבלת בדיוק את 958 לוחות הסיום (ו-1,314 בסעיף ב), ופוסלת את כל
        השאר. המחלקה רצה **כמו שהיא כתובה כאן** ב-Verilator עם ה-solver ‏z3, בכל עדכון של
        האתר : 150 הגרלות על הלוח הקלאסי ו-150 עם האלכסונים המעגליים, כל לוח עבר את
        `final_result` עם התוצאה שהמחלקה בחרה, שלוש התוצאות הופיעו בלוח הקלאסי, ואף תיקו
        לא הופיע בסעיף ב. בנוסף, `randomize() with { result == DRAW; }` נכשל עם 12 הקווים
        ומצליח עם 8. (גרסת השחרור 5.052 של Verilator קורסת על המחלקה הזו; ב-CI רצה גרסת
        פיתוח מאוחרת יותר, ובסימולטור מסחרי הקוד רץ כמו שהוא.)

    #### למה זה נכון { .sol-proof }

    <svg class="figure" viewBox="0 0 696 136" role="img" aria-label="דוגמאות ללוחות סיום חוקיים ולא חוקיים"><g><rect class="cell-s2" x="6" y="6" width="34" height="34"/><path class="mark" d="M15,15 L31,31 M31,15 L15,31"/><rect class="cell-s2" x="40" y="6" width="34" height="34"/><path class="mark" d="M49,15 L65,31 M65,15 L49,31"/><rect class="cell-s2" x="74" y="6" width="34" height="34"/><path class="mark" d="M83,15 L99,31 M99,15 L83,31"/><circle class="mark" cx="23.0" cy="57.0" r="9.0"/><rect class="cell-s2" x="40" y="40" width="34" height="34"/><path class="mark" d="M49,49 L65,65 M65,49 L49,65"/><circle class="mark" cx="91.0" cy="57.0" r="9.0"/><circle class="mark" cx="23.0" cy="91.0" r="9.0"/><circle class="mark" cx="57.0" cy="91.0" r="9.0"/><rect class="cell-s2" x="74" y="74" width="34" height="34"/><path class="mark" d="M83,83 L99,99 M99,83 L83,99"/><line class="ttt-grid" x1="40" x2="40" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="40" y2="40"/><line class="ttt-grid" x1="74" x2="74" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="74" y2="74"/><text class="legend" x="57.0" y="128" text-anchor="middle" direction="rtl">X ניצח : 2 שלישיות</text></g><g><path class="mark" d="M157,15 L173,31 M173,15 L157,31"/><path class="mark" d="M191,15 L207,31 M207,15 L191,31"/><rect class="cell-s1" x="216" y="6" width="34" height="34"/><circle class="mark" cx="233.0" cy="23.0" r="9.0"/><path class="mark" d="M157,49 L173,65 M173,49 L157,65"/><rect class="cell-s1" x="182" y="40" width="34" height="34"/><circle class="mark" cx="199.0" cy="57.0" r="9.0"/><rect class="cell-s1" x="148" y="74" width="34" height="34"/><circle class="mark" cx="165.0" cy="91.0" r="9.0"/><line class="ttt-grid" x1="182" x2="182" y1="6" y2="108"/><line class="ttt-grid" x1="148" x2="250" y1="40" y2="40"/><line class="ttt-grid" x1="216" x2="216" y1="6" y2="108"/><line class="ttt-grid" x1="148" x2="250" y1="74" y2="74"/><text class="legend" x="199.0" y="128" text-anchor="middle" direction="rtl">O ניצח</text></g><g><path class="mark" d="M299,15 L315,31 M315,15 L299,31"/><circle class="mark" cx="341.0" cy="23.0" r="9.0"/><path class="mark" d="M367,15 L383,31 M383,15 L367,31"/><path class="mark" d="M299,49 L315,65 M315,49 L299,65"/><circle class="mark" cx="341.0" cy="57.0" r="9.0"/><circle class="mark" cx="375.0" cy="57.0" r="9.0"/><circle class="mark" cx="307.0" cy="91.0" r="9.0"/><path class="mark" d="M333,83 L349,99 M349,83 L333,99"/><path class="mark" d="M367,83 L383,99 M383,83 L367,99"/><line class="ttt-grid" x1="324" x2="324" y1="6" y2="108"/><line class="ttt-grid" x1="290" x2="392" y1="40" y2="40"/><line class="ttt-grid" x1="358" x2="358" y1="6" y2="108"/><line class="ttt-grid" x1="290" x2="392" y1="74" y2="74"/><text class="legend" x="341.0" y="128" text-anchor="middle" direction="rtl">תיקו</text></g><g><rect class="cell-s2" x="432" y="6" width="34" height="34"/><path class="mark" d="M441,15 L457,31 M457,15 L441,31"/><rect class="cell-s2" x="466" y="6" width="34" height="34"/><path class="mark" d="M475,15 L491,31 M491,15 L475,31"/><rect class="cell-s2" x="500" y="6" width="34" height="34"/><path class="mark" d="M509,15 L525,31 M525,15 L509,31"/><rect class="cell-s1" x="432" y="40" width="34" height="34"/><circle class="mark" cx="449.0" cy="57.0" r="9.0"/><rect class="cell-s1" x="466" y="40" width="34" height="34"/><circle class="mark" cx="483.0" cy="57.0" r="9.0"/><rect class="cell-s1" x="500" y="40" width="34" height="34"/><circle class="mark" cx="517.0" cy="57.0" r="9.0"/><line class="ttt-grid" x1="466" x2="466" y1="6" y2="108"/><line class="ttt-grid" x1="432" x2="534" y1="40" y2="40"/><line class="ttt-grid" x1="500" x2="500" y1="6" y2="108"/><line class="ttt-grid" x1="432" x2="534" y1="74" y2="74"/><text class="legend" x="483.0" y="128" text-anchor="middle" direction="rtl">✗ שניהם ניצחו</text></g><g><rect class="cell-s2" x="574" y="6" width="34" height="34"/><path class="mark" d="M583,15 L599,31 M599,15 L583,31"/><rect class="cell-s2" x="608" y="6" width="34" height="34"/><path class="mark" d="M617,15 L633,31 M633,15 L617,31"/><rect class="cell-s2" x="642" y="6" width="34" height="34"/><path class="mark" d="M651,15 L667,31 M667,15 L651,31"/><circle class="mark" cx="591.0" cy="57.0" r="9.0"/><circle class="mark" cx="625.0" cy="57.0" r="9.0"/><circle class="mark" cx="591.0" cy="91.0" r="9.0"/><line class="ttt-grid" x1="608" x2="608" y1="6" y2="108"/><line class="ttt-grid" x1="574" x2="676" y1="40" y2="40"/><line class="ttt-grid" x1="642" x2="642" y1="6" y2="108"/><line class="ttt-grid" x1="574" x2="676" y1="74" y2="74"/><text class="legend" x="625.0" y="128" text-anchor="middle" direction="rtl">✗ O שיחק אחרי הניצחון</text></g></svg>

    **נסו בעצמכם.** לחצו על משבצות כדי לבנות לוח (ריק, X, O), והתנאים של הדף מכריעים חי
    אם זה לוח סיום חוקי ולמה לא : ספירה שגויה, שני מנצחים, מהלך אחרי הניצחון או משחק שלא
    נגמר. "לוח חוקי אקראי" מגריל כמו `randomize()` של הדף, והמתג מוסיף את האלכסונים
    המעגליים של סעיף ב, שאיתם התיקו נעלם.

    <div class="explorer" data-kind="ttt" data-board="XXXOXOOOX"></div>

    **"שלישייה אחת בלבד"? לא בדיוק.** טעות נפוצה היא לדרוש שלמנצח תהיה שלישייה אחת בלבד.
    אבל X יכול להשלים **שתי** שלישיות במהלך האחרון, אם שתיהן עוברות במשבצת שבה הוא שם את
    ה-X האחרון. בלוח הראשון למעלה, X שם את הסימן האחרון במשבצת 0, והשלים בבת אחת את השורה
    העליונה ואת האלכסון.

    - **ל-X יש לכל היותר 2 שלישיות.** שתי שלישיות מקבילות (בלי משבצת משותפת) דורשות 6 X,
      ולשלוש שלישיות צריך לפחות 6. על הלוח יש לכל היותר 5 X.
    - **ל-O יש לכל היותר שלישייה אחת.** שתי שלישיות דורשות לפחות 5 O, ויש לכל היותר 4.
    - **שתי שלישיות של X תמיד חותכות זו את זו** (כי מקבילות לא אפשריות), ולכן המשבצת
      המשותפת יכולה להיות המהלך האחרון.

    **למה התנאים מספיקים.** צריך להראות שכל לוח שמקיים את התנאים הוא באמת סוף של משחק.
    ניקח לוח שבו X ניצח. נוריד X אחד מהמשבצת שמשותפת לכל השלישיות שלו. נשאר לוח בלי אף
    שלישייה, עם \( n_X = n_O \). לוח כזה אפשר לבנות בכל סדר של מהלכים לסירוגין, כי אף פעם לא
    נוצרת בו שלישייה באמצע. עכשיו X משחק את המהלך האחרון ומנצח. אותו טיעון עובד ל-O, ותיקו
    הוא פשוט לוח מלא בלי שלישיות.

    **בדיקה :** בדקנו את התנאים מול כל המשחקים האפשריים (סריקה של עץ המשחק). מתקבלים בדיוק
    **958** לוחות סיום : 626 שבהם X ניצח, 316 שבהם O ניצח, ו-16 לוחות תיקו.

    #### סיבוכיות { .sol-cost }

    | | ‏SystemVerilog | ‏Python |
    |-|---------------|---------|
    | עבודה חד-פעמית | אין | סריקה של \( 3^9 = 19{,}683 \) לוחות, פעם אחת (`@cache`) |
    | הגרלה אחת | קריאה ל-`randomize()` : ה-solver עובד על 9 משתנים של 3 ערכים ועוד משתני עזר | שתי בחירות אקראיות, \( O(1) \) |
    | זיכרון | האובייקט בלבד | 958 לוחות שמורים לפי תוצאה |

    הלוח קטן מספיק כדי שסריקה מלאה תהיה זולה, ולכן ב-Python היא גם הדרך הפשוטה וגם הדרך
    שמשחזרת בדיוק את ההתפלגות של `solve result before board`. בלוח 4 על 4 (\( 3^{16} \approx 43 \)
    מיליון מילויים) כבר היה צריך לחשוב על סריקה של עץ המשחק במקום על כל המילויים.

---

### סעיף ב – אלכסונים "מסביב"

עכשיו מוסיפים חוק : אלכסון יכול **להמשיך מהצד השני** של הלוח (wrap-around), כאילו הלוח
מודבק לעצמו מימין לשמאל ומלמעלה למטה. למשל, המשבצות 0, 5, 7 הן שלישייה : מתחילים ב-0,
יורדים שמאלה, יוצאים מהלוח וחוזרים מימין.

<svg class="figure" viewBox="0 0 476 136" role="img" aria-label="אלכסונים שממשיכים מהצד השני של הלוח"><g class="ttt-ghost"><rect class="cell-s2" x="6" y="6" width="34" height="34"/><path class="mark" d="M15,15 L31,31 M31,15 L15,31"/><rect class="cell-s2" x="74" y="40" width="34" height="34"/><path class="mark" d="M83,49 L99,65 M99,49 L83,65"/><rect class="cell-s2" x="40" y="74" width="34" height="34"/><path class="mark" d="M49,83 L65,99 M65,83 L49,99"/><line class="ttt-grid" x1="40" x2="40" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="40" y2="40"/><line class="ttt-grid" x1="74" x2="74" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="74" y2="74"/></g><g><rect class="cell-s2" x="112" y="6" width="34" height="34"/><path class="mark" d="M121,15 L137,31 M137,15 L121,31"/><rect class="cell-s2" x="180" y="40" width="34" height="34"/><path class="mark" d="M189,49 L205,65 M205,49 L189,65"/><rect class="cell-s2" x="146" y="74" width="34" height="34"/><path class="mark" d="M155,83 L171,99 M171,83 L155,99"/><line class="ttt-grid" x1="146" x2="146" y1="6" y2="108"/><line class="ttt-grid" x1="112" x2="214" y1="40" y2="40"/><line class="ttt-grid" x1="180" x2="180" y1="6" y2="108"/><line class="ttt-grid" x1="112" x2="214" y1="74" y2="74"/><text class="legend" x="163.0" y="128" text-anchor="middle" direction="rtl">המשבצות 0, 5, 7</text></g><polyline class="s2-line" points="129.0,23.0 91.0,57.0 57.0,91.0" fill="none" stroke-width="3"/><g class="ttt-ghost"><rect class="cell-s2" x="432" y="6" width="34" height="34"/><path class="mark" d="M441,15 L457,31 M457,15 L441,31"/><rect class="cell-s2" x="364" y="40" width="34" height="34"/><path class="mark" d="M373,49 L389,65 M389,49 L373,65"/><rect class="cell-s2" x="398" y="74" width="34" height="34"/><path class="mark" d="M407,83 L423,99 M423,83 L407,99"/><line class="ttt-grid" x1="398" x2="398" y1="6" y2="108"/><line class="ttt-grid" x1="364" x2="466" y1="40" y2="40"/><line class="ttt-grid" x1="432" x2="432" y1="6" y2="108"/><line class="ttt-grid" x1="364" x2="466" y1="74" y2="74"/></g><g><rect class="cell-s2" x="326" y="6" width="34" height="34"/><path class="mark" d="M335,15 L351,31 M351,15 L335,31"/><rect class="cell-s2" x="258" y="40" width="34" height="34"/><path class="mark" d="M267,49 L283,65 M283,49 L267,65"/><rect class="cell-s2" x="292" y="74" width="34" height="34"/><path class="mark" d="M301,83 L317,99 M317,83 L301,99"/><line class="ttt-grid" x1="292" x2="292" y1="6" y2="108"/><line class="ttt-grid" x1="258" x2="360" y1="40" y2="40"/><line class="ttt-grid" x1="326" x2="326" y1="6" y2="108"/><line class="ttt-grid" x1="258" x2="360" y1="74" y2="74"/><text class="legend" x="309.0" y="128" text-anchor="middle" direction="rtl">המשבצות 2, 3, 7</text></g><polyline class="s2-line" points="343.0,23.0 381.0,57.0 415.0,91.0" fill="none" stroke-width="3"/></svg>

עדכנו את התנאים ואת הקוד. מה מיוחד בלוח הזה?

??? tip "רמז 1"
    רשמו את האלכסונים החדשים לפי מספרי המשבצות. כמה קווים יש עכשיו בסך הכול, ולכמה
    "כיוונים" הם מתחלקים?

??? tip "רמז 2"
    נסו למצוא לוח מלא (5 X ו-4 O) שבו לאף אחד אין שלישייה. כמה שלישיות עוברות דרך כל זוג
    משבצות?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        מוסיפים 4 אלכסונים, ובסך הכול 12 קווים; **התנאים עצמם לא משתנים**, רק קבוצת הקווים.
        המיוחד : **אף משחק לא נגמר בתיקו**, כי כל 5 משבצות מכילות קו שלם. יש 1,314 לוחות
        סיום : 882 של X, 432 של O ו-0 תיקו.

    #### הרעיון { .sol-idea }

    ארבעת האלכסונים החדשים משלימים 12 קווים בארבעה כיוונים, וכל כיוון מחלק את הלוח לשלושה
    קווים מקבילים. כל זוג משבצות נמצא על קו אחד בדיוק (מערכת שטיינר \( S(2,3,9) \)), וספירת זוגות מראה שאי אפשר
    לשים 5 סימנים בלי להשלים קו. לכן ל-X תמיד יש שלישייה בלוח מלא, ותיקו בלתי אפשרי.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מוסיפים את 4 הקווים :** \( \{1,5,6\}, \{2,3,7\}, \{0,5,7\}, \{1,3,8\} \). יחד עם השורות,
       הטורים ושני האלכסונים יש 12 קווים.
    2. **בודקים שהטיעונים נשארים :** שני קווים באותו כיוון זרים, ולכן שתי שלישיות מקבילות של
       X דורשות 6 X. לכן ל-X יש עד 2 שלישיות שנחתכות, ול-O יש עד אחת. התנאים מסעיף א
       נשארים כמו שהם.
    3. **משנים רק את קבוצת הקווים בקוד :** ב-SystemVerilog `n_lines = 12`, וב-Python
       `WRAP_LINES`.
    4. **שמים לב שהתיקו נעלם :** ה-solver לא מוצא אף פתרון עם `result == DRAW`, וההוכחה
       בהמשך מסבירה למה.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="usage, part b"
            ttt_end t = new();
            t.n_lines = 12;                                  // add the 4 wrap-around diagonals (1)
            if (!t.randomize()) $fatal(1, "randomize() failed");
            if (t.randomize() with { result == DRAW; })      // never succeeds, see below (2)
              $fatal(1, "a draw should be impossible");
        ```

        1. ‏`n_lines` אינו `rand`, ולכן משנים אותו כמו שדה רגיל לפני `randomize()`. ה-constraint
           `c_lines` קורא אותו דרך `l < n_lines`, וכך 4 הקווים הנוספים נדלקים בלי לשנות שורה
           אחת ב-constraints.
        2. ‏`randomize() with { ... }` מוסיף constraint זמני לקריאה הזו בלבד. כשאין אף פתרון הוא
           מחזיר 0 ולא משנה את האובייקט, ולכן זו דרך נוחה לתת ל-solver "להוכיח" שאין תיקו.

    === "Python"
        ```python title="WRAP_LINES"
            WRAP_LINES = LINES + ((1, 5, 6), (2, 3, 7),   # wrap-around diagonals (part b) (1)
                                  (0, 5, 7), (1, 3, 8))

            # randomize(WRAP_LINES) never returns "draw": final_boards(WRAP_LINES)["draw"] is empty
        ```

        1. יוצרים tuple חדש ולא רשימה שמוסיפים אליה : `final_boards` משתמשת ב-`@cache`, ולכן
           קבוצת הקווים חייבת להיות hashable. כל קבוצה מקבלת סריקה משלה, פעם אחת.

    #### למה זה נכון { .sol-proof }

    **שנים-עשר הקווים.** לשורות ולטורים מצטרפים 4 אלכסונים חדשים, ובסך הכול יש **12 קווים** בארבעה
    **כיוונים**. כל כיוון מחלק את 9 המשבצות ל-3 קווים מקבילים :

    <span class="viz-legend"><span><i class="s1"></i>קו ראשון</span><span><i class="s2"></i>קו שני</span><span><i class="s3"></i>קו שלישי</span></span>

    <svg class="figure" viewBox="0 0 528 136" role="img" aria-label="ארבעת הכיוונים : כל כיוון מחלק את הלוח לשלושה קווים מקבילים"><g><rect class="cell-s1" x="6" y="6" width="34" height="34"/><text class="box-num" x="23.0" y="28.0" text-anchor="middle">0</text><rect class="cell-s1" x="40" y="6" width="34" height="34"/><text class="box-num" x="57.0" y="28.0" text-anchor="middle">1</text><rect class="cell-s1" x="74" y="6" width="34" height="34"/><text class="box-num" x="91.0" y="28.0" text-anchor="middle">2</text><rect class="cell-s2" x="6" y="40" width="34" height="34"/><text class="box-num" x="23.0" y="62.0" text-anchor="middle">3</text><rect class="cell-s2" x="40" y="40" width="34" height="34"/><text class="box-num" x="57.0" y="62.0" text-anchor="middle">4</text><rect class="cell-s2" x="74" y="40" width="34" height="34"/><text class="box-num" x="91.0" y="62.0" text-anchor="middle">5</text><rect class="cell-s3" x="6" y="74" width="34" height="34"/><text class="box-num" x="23.0" y="96.0" text-anchor="middle">6</text><rect class="cell-s3" x="40" y="74" width="34" height="34"/><text class="box-num" x="57.0" y="96.0" text-anchor="middle">7</text><rect class="cell-s3" x="74" y="74" width="34" height="34"/><text class="box-num" x="91.0" y="96.0" text-anchor="middle">8</text><line class="ttt-grid" x1="40" x2="40" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="40" y2="40"/><line class="ttt-grid" x1="74" x2="74" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="74" y2="74"/><text class="legend" x="57.0" y="128" text-anchor="middle" direction="rtl">שורות</text></g><g><rect class="cell-s1" x="144" y="6" width="34" height="34"/><text class="box-num" x="161.0" y="28.0" text-anchor="middle">0</text><rect class="cell-s2" x="178" y="6" width="34" height="34"/><text class="box-num" x="195.0" y="28.0" text-anchor="middle">1</text><rect class="cell-s3" x="212" y="6" width="34" height="34"/><text class="box-num" x="229.0" y="28.0" text-anchor="middle">2</text><rect class="cell-s1" x="144" y="40" width="34" height="34"/><text class="box-num" x="161.0" y="62.0" text-anchor="middle">3</text><rect class="cell-s2" x="178" y="40" width="34" height="34"/><text class="box-num" x="195.0" y="62.0" text-anchor="middle">4</text><rect class="cell-s3" x="212" y="40" width="34" height="34"/><text class="box-num" x="229.0" y="62.0" text-anchor="middle">5</text><rect class="cell-s1" x="144" y="74" width="34" height="34"/><text class="box-num" x="161.0" y="96.0" text-anchor="middle">6</text><rect class="cell-s2" x="178" y="74" width="34" height="34"/><text class="box-num" x="195.0" y="96.0" text-anchor="middle">7</text><rect class="cell-s3" x="212" y="74" width="34" height="34"/><text class="box-num" x="229.0" y="96.0" text-anchor="middle">8</text><line class="ttt-grid" x1="178" x2="178" y1="6" y2="108"/><line class="ttt-grid" x1="144" x2="246" y1="40" y2="40"/><line class="ttt-grid" x1="212" x2="212" y1="6" y2="108"/><line class="ttt-grid" x1="144" x2="246" y1="74" y2="74"/><text class="legend" x="195.0" y="128" text-anchor="middle" direction="rtl">טורים</text></g><g><rect class="cell-s1" x="282" y="6" width="34" height="34"/><text class="box-num" x="299.0" y="28.0" text-anchor="middle">0</text><rect class="cell-s2" x="316" y="6" width="34" height="34"/><text class="box-num" x="333.0" y="28.0" text-anchor="middle">1</text><rect class="cell-s3" x="350" y="6" width="34" height="34"/><text class="box-num" x="367.0" y="28.0" text-anchor="middle">2</text><rect class="cell-s3" x="282" y="40" width="34" height="34"/><text class="box-num" x="299.0" y="62.0" text-anchor="middle">3</text><rect class="cell-s1" x="316" y="40" width="34" height="34"/><text class="box-num" x="333.0" y="62.0" text-anchor="middle">4</text><rect class="cell-s2" x="350" y="40" width="34" height="34"/><text class="box-num" x="367.0" y="62.0" text-anchor="middle">5</text><rect class="cell-s2" x="282" y="74" width="34" height="34"/><text class="box-num" x="299.0" y="96.0" text-anchor="middle">6</text><rect class="cell-s3" x="316" y="74" width="34" height="34"/><text class="box-num" x="333.0" y="96.0" text-anchor="middle">7</text><rect class="cell-s1" x="350" y="74" width="34" height="34"/><text class="box-num" x="367.0" y="96.0" text-anchor="middle">8</text><line class="ttt-grid" x1="316" x2="316" y1="6" y2="108"/><line class="ttt-grid" x1="282" x2="384" y1="40" y2="40"/><line class="ttt-grid" x1="350" x2="350" y1="6" y2="108"/><line class="ttt-grid" x1="282" x2="384" y1="74" y2="74"/><text class="legend" x="333.0" y="128" text-anchor="middle" direction="rtl">אלכסונים ↘</text></g><g><rect class="cell-s1" x="420" y="6" width="34" height="34"/><text class="box-num" x="437.0" y="28.0" text-anchor="middle">0</text><rect class="cell-s2" x="454" y="6" width="34" height="34"/><text class="box-num" x="471.0" y="28.0" text-anchor="middle">1</text><rect class="cell-s3" x="488" y="6" width="34" height="34"/><text class="box-num" x="505.0" y="28.0" text-anchor="middle">2</text><rect class="cell-s2" x="420" y="40" width="34" height="34"/><text class="box-num" x="437.0" y="62.0" text-anchor="middle">3</text><rect class="cell-s3" x="454" y="40" width="34" height="34"/><text class="box-num" x="471.0" y="62.0" text-anchor="middle">4</text><rect class="cell-s1" x="488" y="40" width="34" height="34"/><text class="box-num" x="505.0" y="62.0" text-anchor="middle">5</text><rect class="cell-s3" x="420" y="74" width="34" height="34"/><text class="box-num" x="437.0" y="96.0" text-anchor="middle">6</text><rect class="cell-s1" x="454" y="74" width="34" height="34"/><text class="box-num" x="471.0" y="96.0" text-anchor="middle">7</text><rect class="cell-s2" x="488" y="74" width="34" height="34"/><text class="box-num" x="505.0" y="96.0" text-anchor="middle">8</text><line class="ttt-grid" x1="454" x2="454" y1="6" y2="108"/><line class="ttt-grid" x1="420" x2="522" y1="40" y2="40"/><line class="ttt-grid" x1="488" x2="488" y1="6" y2="108"/><line class="ttt-grid" x1="420" x2="522" y1="74" y2="74"/><text class="legend" x="471.0" y="128" text-anchor="middle" direction="rtl">אלכסונים ↙</text></g></svg>

    בדקו שני זוגות משבצות שרירותיים : תמיד יש **בדיוק קו אחד** שעובר דרך שתיהן. מבנה כזה
    נקרא **מערכת שטיינר** \( S(2, 3, 9) \) : 9 נקודות, קווים של 3, וכל זוג נקודות נמצא על קו
    אחד בדיוק. זה גם המישור האפיני \( AG(2, 3) \).

    **התנאים לא משתנים**, רק קבוצת הקווים גדלה מ-8 ל-12. גם הטיעונים נשארים : שני קווים
    באותו כיוון זרים, ולכן שתי שלישיות מקבילות של X דורשות 6 X. לכן ל-X יש עד 2 שלישיות
    שנחתכות, ול-O יש עד אחת.

    **הטריק : אין תיקו.** עם 12 הקווים **אף משחק לא נגמר בתיקו**. תיקו דורש לוח מלא, כלומר
    5 X בלי אף שלישייה. נראה שזה בלתי אפשרי : **כל 5 משבצות מכילות קו שלם**.

    **ההוכחה.** נניח שיש קבוצה \( S \) של 5 משבצות בלי קו שלם, כלומר כל קו מכיל לכל היותר 2
    משבצות של \( S \).

    <div class="steps" markdown>

    1. **בכל כיוון החלוקה היא 2, 2, 1.** שלושת הקווים של כיוון אחד מכסים את כל הלוח, ולכן
       סכום המשבצות של \( S \) עליהם הוא 5. כל קו מכיל לכל היותר 2, והדרך היחידה להגיע ל-5
       היא \( 2 + 2 + 1 \).
    2. **בכל כיוון יש בדיוק 2 זוגות.** קו עם 2 משבצות של \( S \) מכיל זוג אחד מ-\( S \), וקו
       עם משבצת אחת לא מכיל אף זוג. בארבעת הכיוונים יחד יש \( 4 \times 2 = 8 \) זוגות.
    3. **אבל ב-\( S \) יש 10 זוגות.** מ-5 משבצות אפשר ליצור \( \binom{5}{2} = 10 \) זוגות,
       ולפי \( S(2,3,9) \) **כל** זוג נמצא על קו אחד בדיוק, ולכן נספר בדיוק פעם אחת.
    4. **סתירה.** הזוגות נספרו פעמיים : פעם 8 ופעם 10. לכן לכל 5 משבצות יש קו שלם. בפרט,
       בלוח מלא ל-X תמיד יש שלישייה, ולכן המשחק נגמר בניצחון לפני שהלוח מתמלא, או במהלך
       האחרון. ∎

    </div>

    **הערה על הוכחה דרך זוגיות.** טיעון כמו "כל קו נוגע ב-\( S \) ב-0 או ב-2 משבצות, ולכן
    הסכום על 3 שורות זוגי" לא עובד : קו יכול לגעת ב-\( S \) גם במשבצת **אחת**, והחלוקה 2, 2, 1
    בדיוק מראה את זה. ההוכחה הנכונה סופרת **זוגות** ולא משבצות.

    **אפשר לראות את זה גם בציור.** ל-4 משבצות כבר אפשר להגיע בלי קו, למשל ריבוע 2 על 2 בפינה.
    כל משבצת חמישית שמוסיפים משלימה קו :

    <svg class="figure" viewBox="0 0 610 136" role="img" aria-label="ריבוע של 4 משבצות בלי קו, וכל משבצת חמישית משלימה קו"><g><rect class="cell-s2" x="6" y="6" width="34" height="34"/><path class="mark" d="M15,15 L31,31 M31,15 L15,31"/><rect class="cell-s2" x="40" y="6" width="34" height="34"/><path class="mark" d="M49,15 L65,31 M65,15 L49,31"/><rect class="cell-s2" x="74" y="6" width="34" height="34"/><path class="mark mark-new" d="M83,15 L99,31 M99,15 L83,31"/><path class="mark" d="M15,49 L31,65 M31,49 L15,65"/><path class="mark" d="M49,49 L65,65 M65,49 L49,65"/><line class="ttt-grid" x1="40" x2="40" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="40" y2="40"/><line class="ttt-grid" x1="74" x2="74" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="74" y2="74"/><text class="legend" x="57.0" y="128" text-anchor="middle" direction="rtl">משבצת 2</text></g><g><path class="mark" d="M139,15 L155,31 M155,15 L139,31"/><path class="mark" d="M173,15 L189,31 M189,15 L173,31"/><rect class="cell-s2" x="130" y="40" width="34" height="34"/><path class="mark" d="M139,49 L155,65 M155,49 L139,65"/><rect class="cell-s2" x="164" y="40" width="34" height="34"/><path class="mark" d="M173,49 L189,65 M189,49 L173,65"/><rect class="cell-s2" x="198" y="40" width="34" height="34"/><path class="mark mark-new" d="M207,49 L223,65 M223,49 L207,65"/><line class="ttt-grid" x1="164" x2="164" y1="6" y2="108"/><line class="ttt-grid" x1="130" x2="232" y1="40" y2="40"/><line class="ttt-grid" x1="198" x2="198" y1="6" y2="108"/><line class="ttt-grid" x1="130" x2="232" y1="74" y2="74"/><text class="legend" x="181.0" y="128" text-anchor="middle" direction="rtl">משבצת 5</text></g><g><rect class="cell-s2" x="254" y="6" width="34" height="34"/><path class="mark" d="M263,15 L279,31 M279,15 L263,31"/><path class="mark" d="M297,15 L313,31 M313,15 L297,31"/><rect class="cell-s2" x="254" y="40" width="34" height="34"/><path class="mark" d="M263,49 L279,65 M279,49 L263,65"/><path class="mark" d="M297,49 L313,65 M313,49 L297,65"/><rect class="cell-s2" x="254" y="74" width="34" height="34"/><path class="mark mark-new" d="M263,83 L279,99 M279,83 L263,99"/><line class="ttt-grid" x1="288" x2="288" y1="6" y2="108"/><line class="ttt-grid" x1="254" x2="356" y1="40" y2="40"/><line class="ttt-grid" x1="322" x2="322" y1="6" y2="108"/><line class="ttt-grid" x1="254" x2="356" y1="74" y2="74"/><text class="legend" x="305.0" y="128" text-anchor="middle" direction="rtl">משבצת 6</text></g><g><path class="mark" d="M387,15 L403,31 M403,15 L387,31"/><rect class="cell-s2" x="412" y="6" width="34" height="34"/><path class="mark" d="M421,15 L437,31 M437,15 L421,31"/><path class="mark" d="M387,49 L403,65 M403,49 L387,65"/><rect class="cell-s2" x="412" y="40" width="34" height="34"/><path class="mark" d="M421,49 L437,65 M437,49 L421,65"/><rect class="cell-s2" x="412" y="74" width="34" height="34"/><path class="mark mark-new" d="M421,83 L437,99 M437,83 L421,99"/><line class="ttt-grid" x1="412" x2="412" y1="6" y2="108"/><line class="ttt-grid" x1="378" x2="480" y1="40" y2="40"/><line class="ttt-grid" x1="446" x2="446" y1="6" y2="108"/><line class="ttt-grid" x1="378" x2="480" y1="74" y2="74"/><text class="legend" x="429.0" y="128" text-anchor="middle" direction="rtl">משבצת 7</text></g><g><rect class="cell-s2" x="502" y="6" width="34" height="34"/><path class="mark" d="M511,15 L527,31 M527,15 L511,31"/><rect class="cell-s2" x="536" y="6" width="34" height="34"/><path class="mark" d="M545,15 L561,31 M561,15 L545,31"/><rect class="cell-s2" x="502" y="40" width="34" height="34"/><path class="mark" d="M511,49 L527,65 M527,49 L511,65"/><rect class="cell-s2" x="536" y="40" width="34" height="34"/><path class="mark" d="M545,49 L561,65 M561,49 L545,65"/><rect class="cell-s2" x="570" y="74" width="34" height="34"/><path class="mark mark-new" d="M579,83 L595,99 M595,83 L579,99"/><line class="ttt-grid" x1="536" x2="536" y1="6" y2="108"/><line class="ttt-grid" x1="502" x2="604" y1="40" y2="40"/><line class="ttt-grid" x1="570" x2="570" y1="6" y2="108"/><line class="ttt-grid" x1="502" x2="604" y1="74" y2="74"/><text class="legend" x="553.0" y="128" text-anchor="middle" direction="rtl">משבצת 8</text></g></svg>

    **נסו בעצמכם.** בתיבה הבאה בוחרים עד חמש משבצות, והטבלה סופרת לכל כיוון כמה מהן על כל
    אחד משלושת הקווים, וכמה זוגות נמצאים על קו. סכום הזוגות תמיד \( \binom{m}{2} \), כמו
    בשלב 3. הדוגמה היא הריבוע מהציור : ארבע משבצות בלי קו, והכוכבים מראים שכל משבצת ריקה
    משלימה קו. נסו לבחור חמש בלי קו, ותראו שזה לא מצליח.

    <div class="explorer" data-kind="tttfive" data-cells="0 1 3 4"></div>

    **בדיקה :** בדקנו את כל 126 הבחירות של 5 משבצות מתוך 9, ובכולן יש קו שלם. עם 12 הקווים
    יש **1,314** לוחות סיום : 882 שבהם X ניצח, 432 שבהם O ניצח, ו-0 לוחות תיקו.

    **מה ה-solver עושה עם זה?** `randomize() with { result == DRAW; }` מחזיר 0, כי אין אף
    פתרון. ובלי ה-`with`, הערך `DRAW` פשוט לא נבחר אף פעם, ו-X ו-O מנצחים כל אחד בחצי
    מהמקרים. ה-solver "מוכיח" את המשפט בשבילנו : הוא עובר על מרחב הפתרונות ולא מוצא תיקו.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : O המשיך לשחק אחרי הניצחון"
    הרבה מועמדים כותבים "X ניצח" כ-"ל-X יש שלישייה ול-O אין", ושוכחים את \( n_X = n_O + 1 \).
    אז ה-solver מייצר לוחות שבהם X השלים שלישייה ו-O "המשיך לשחק" אחרי שהפסיד. הכלל : מי
    שניצח הוא זה ששיחק אחרון, וזה מתבטא בספירה.

??? trap "מלכודת : לדרוש שלישייה אחת בלבד"
    הדרישה "למנצח בדיוק שלישייה אחת" פוסלת לוחות חוקיים שבהם X סוגר שתי שלישיות במהלך
    אחד (משבצת משותפת לשורה ולאלכסון). constraint חזק מדי הוא באג באימות : הוא מסתיר מצבים
    אמיתיים מהבדיקות, ואף בדיקה לא תתריע עליו כי כל לוח שכן מתקבל הוא חוקי.

??? trap "מלכודת : sum על מערך של ביטים"
    ‏`x_line.sum()` בלי `with (int'(item))` מחזיר תוצאה ברוחב של איבר אחד, כלומר ביט אחד.
    שתי שלישיות נספרות כ-0, ולוח שבו X סגר שתי שלישיות במהלך אחד לא יכול להתקבל כניצחון
    של X, בדיוק הלוחות המעניינים. כשסוכמים ביטים ב-SystemVerilog תמיד מרחיבים במפורש.

??? followup "שאלות המשך"
    - **כל לוח באמצע משחק :** איך משנים את ה-constraints כדי לקבל גם לוחות שבהם המשחק עוד
      לא נגמר?

        ??? fu-answer "תשובה"
            מוסיפים תוצאה רביעית, `IN_PROGRESS`, עם
            `(result == IN_PROGRESS) -> (x_lines == 0 && o_lines == 0 && n_x + n_o < 9);`. ספירת
            התורות לא משתנה. יחד עם שלוש התוצאות זה נותן את כל 5,478 הלוחות של משחק אמיתי, מהם
            4,520 באמצע משחק.

    - **התפלגות לפי מספר המהלכים :** הוסיפו constraint עם `dist` כך שמשחקים קצרים (ניצחון
      אחרי 5 מהלכים) יופיעו לעתים קרובות יותר.

        ??? fu-answer "תשובה"
            משתנה עזר `rand int n_moves` עם `n_moves == n_x + n_o`, ועליו
            `n_moves dist { 5 := 4, [6:9] := 1 };`. בגלל `solve result before board` ההטיה פועלת
            בתוך כל תוצאה; ב-`O_WINS` אין משחק של 5 מהלכים, וה-solver מחלק בין הערכים האפשריים.

    - **לוח 4 על 4 עם רביעיות :** אילו מהתנאים משתנים? מה המספר המקסימלי של רביעיות שיכולות
      להיות למנצח?

        ??? fu-answer "תשובה"
            משתנים רק הקווים (10 קווים של 4) ותנאי התיקו (\( n_X + n_O = 16 \)); הספירה נשארת.
            למנצח יש לכל היותר **2** רביעיות : כולן עוברות במשבצת של המהלך האחרון, דרך משבצת עוברים
            לכל היותר 3 קווים, ושלושה כאלה דורשים 10 סימנים, יותר מ-8 שיש לשחקן.
