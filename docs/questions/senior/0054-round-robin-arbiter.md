---
id: 54
title: Arbiter סבבי – הרעבה, טריק שני ה-encoders, SVA ומשקלים
level: senior
difficulty: hard
kind: design
tags: [digital-logic, sva, systemverilog, python]
source: "שאלת ראיון קלאסית ל-RTL ול-DV (arbiters, fairness)"
added: 2026-10-27
---

## השאלה

‏\( N \) מבקשים חולקים משאב אחד (באס, פורט של זיכרון). בכל מחזור כל מבקש \( i \) מרים
`req[i]` אם הוא רוצה את המשאב, וה-arbiter נותן מענק `gnt` לאחד לכל היותר, באותו מחזור.
מבקש שלא קיבל משאיר את `req[i]` למעלה עד שהוא מקבל.

- **סעיף א – עדיפות קבועה :** כתבו arbiter שבו המבקש עם המספר הנמוך תמיד מנצח. מה הבעיה
  שלו?
- **סעיף ב – ‏round robin :** כתבו arbiter סבבי : אחרי שמבקש קיבל, הוא הופך לאחרון בתור.
  איך עושים את זה בלי לולאה על כל המבקשים בכל מחזור?
- **סעיף ג – ‏SVA והוגנות :** כתבו assertions לחוקים של ה-arbiter, כולל "מבקש מחכה לכל
  היותר \( K \) מחזורים". מה \( K \) הקטן ביותר, ולמה?
- **סעיף ד – משקלים :** למבקש \( i \) יש משקל \( w_i \), והוא אמור לקבל חלק \( w_i / \sum w \)
  מהמשאב בעומס מלא. איך משנים את ה-arbiter, ומה ההמתנה הארוכה ביותר עכשיו?

??? interviewer "מה המראיין בודק"
    - **הרעבה :** האם המועמד רואה מיד שעדיפות קבועה יכולה להשאיר מבקש בלי מענק לעולם.
    - **‏RTL יעיל :** האם הוא מכיר את הטריק של \( x \mathbin{\&} \lnot(x - p) \) לבחירת הבקשה
      הראשונה מעמדה מסוימת, ואת הכפלת הבקשות למעבר מעגלי.
    - **עדכון המצביע :** אחרי מי הוא זז, ומה קורה כשאין אף בקשה.
    - **אימות :** האם ה-assertions מנוסחות כך שהן גם נכשלות על באגים אמיתיים, והאם ההוגנות
      מותנית בהנחה על הסביבה (בקשה נשארת עד שמקבלים).
    - **משקלים :** האם הוא מבין שמשקל משנה את החלוקה, אבל גם מאריך את ההמתנה של האחרים.

---

### סעיף א – עדיפות קבועה

??? tip "רמז 1"
    "הביט הדולק הנמוך ביותר" הוא פעולה מוכרת : מה נותן `x & -x`?

??? tip "רמז 2"
    מה קורה למבקש 3 אם מבקש 0 מבקש בכל מחזור?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏`gnt = req & (~req + 1)`, כלומר `req & -req` : הביט הדולק הנמוך ביותר. הבעיה היא
        **הרעבה** : כל עוד מבקש עם מספר נמוך יותר מבקש, מבקש גבוה לא יקבל לעולם, ואין חסם
        על ההמתנה שלו.

    <!-- cost: שערים \( O(N) \) | השהיה \( O(\log N) \) -->

    #### הרעיון { .sol-idea }

    בשלילה בשיטת המשלים ל-2, \( -x = \lnot x + 1 \) : כל הביטים מתהפכים, וה-+1 רץ עד הביט
    הדולק הנמוך ביותר של \( x \). מתחתיו, \( x \) ו-\( -x \) הם אפסים; בו, שניהם 1; מעליו,
    הם הפוכים. לכן \( x \mathbin{\&} -x \) משאיר בדיוק את הביט הדולק הנמוך ביותר.

    העדיפות הקבועה פשוטה ומהירה, ומתאימה כשיש מבקש שבאמת דחוף יותר (פסיקה, ריענון של
    DRAM). אבל בעומס מלא היא לא הוגנת : מבקש 0 לוקח הכול.

    <!-- gen 0 -->

    <svg class="figure arb-fig" viewBox="0 0 660 364" style="max-width:41rem" role="img" aria-label="ארבעה מבקשים שמבקשים כל הזמן : ב-fixed priority רק מבקש 0 מקבל, ב-round robin כל אחד מקבל פעם בארבעה מחזורים"><text class="tick" x="167.0" y="20" text-anchor="middle">0</text><text class="tick" x="201.0" y="20" text-anchor="middle">1</text><text class="tick" x="235.0" y="20" text-anchor="middle">2</text><text class="tick" x="269.0" y="20" text-anchor="middle">3</text><text class="tick" x="303.0" y="20" text-anchor="middle">4</text><text class="tick" x="337.0" y="20" text-anchor="middle">5</text><text class="tick" x="371.0" y="20" text-anchor="middle">6</text><text class="tick" x="405.0" y="20" text-anchor="middle">7</text><text class="arb-name" x="80" y="103.0" text-anchor="middle">fixed</text><text class="tick" x="142" y="51.0" text-anchor="end">req 0</text><rect class="arb-cell is-gnt" x="150" y="30" width="31" height="31" rx="3"/><text class="arb-mark" x="166.0" y="51.0" text-anchor="middle">G</text><rect class="arb-cell is-gnt" x="184" y="30" width="31" height="31" rx="3"/><text class="arb-mark" x="200.0" y="51.0" text-anchor="middle">G</text><rect class="arb-cell is-gnt" x="218" y="30" width="31" height="31" rx="3"/><text class="arb-mark" x="234.0" y="51.0" text-anchor="middle">G</text><rect class="arb-cell is-gnt" x="252" y="30" width="31" height="31" rx="3"/><text class="arb-mark" x="268.0" y="51.0" text-anchor="middle">G</text><rect class="arb-cell is-gnt" x="286" y="30" width="31" height="31" rx="3"/><text class="arb-mark" x="302.0" y="51.0" text-anchor="middle">G</text><rect class="arb-cell is-gnt" x="320" y="30" width="31" height="31" rx="3"/><text class="arb-mark" x="336.0" y="51.0" text-anchor="middle">G</text><rect class="arb-cell is-gnt" x="354" y="30" width="31" height="31" rx="3"/><text class="arb-mark" x="370.0" y="51.0" text-anchor="middle">G</text><rect class="arb-cell is-gnt" x="388" y="30" width="31" height="31" rx="3"/><text class="arb-mark" x="404.0" y="51.0" text-anchor="middle">G</text><text class="tick" x="142" y="85.0" text-anchor="end">req 1</text><rect class="arb-cell is-wait" x="150" y="64" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="184" y="64" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="218" y="64" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="252" y="64" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="286" y="64" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="320" y="64" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="354" y="64" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="388" y="64" width="31" height="31" rx="3"/><text class="tick" x="142" y="119.0" text-anchor="end">req 2</text><rect class="arb-cell is-wait" x="150" y="98" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="184" y="98" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="218" y="98" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="252" y="98" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="286" y="98" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="320" y="98" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="354" y="98" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="388" y="98" width="31" height="31" rx="3"/><text class="tick" x="142" y="153.0" text-anchor="end">req 3</text><rect class="arb-cell is-wait" x="150" y="132" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="184" y="132" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="218" y="132" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="252" y="132" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="286" y="132" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="320" y="132" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="354" y="132" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="388" y="132" width="31" height="31" rx="3"/><text class="arb-name" x="80" y="265.0" text-anchor="middle">round robin</text><text class="tick" x="142" y="213.0" text-anchor="end">req 0</text><rect class="arb-cell is-gnt" x="150" y="192" width="31" height="31" rx="3"/><text class="arb-mark" x="166.0" y="213.0" text-anchor="middle">G</text><rect class="arb-cell is-wait" x="184" y="192" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="218" y="192" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="252" y="192" width="31" height="31" rx="3"/><rect class="arb-cell is-gnt" x="286" y="192" width="31" height="31" rx="3"/><text class="arb-mark" x="302.0" y="213.0" text-anchor="middle">G</text><rect class="arb-cell is-wait" x="320" y="192" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="354" y="192" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="388" y="192" width="31" height="31" rx="3"/><text class="tick" x="142" y="247.0" text-anchor="end">req 1</text><rect class="arb-cell is-wait" x="150" y="226" width="31" height="31" rx="3"/><rect class="arb-cell is-gnt" x="184" y="226" width="31" height="31" rx="3"/><text class="arb-mark" x="200.0" y="247.0" text-anchor="middle">G</text><rect class="arb-cell is-wait" x="218" y="226" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="252" y="226" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="286" y="226" width="31" height="31" rx="3"/><rect class="arb-cell is-gnt" x="320" y="226" width="31" height="31" rx="3"/><text class="arb-mark" x="336.0" y="247.0" text-anchor="middle">G</text><rect class="arb-cell is-wait" x="354" y="226" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="388" y="226" width="31" height="31" rx="3"/><text class="tick" x="142" y="281.0" text-anchor="end">req 2</text><rect class="arb-cell is-wait" x="150" y="260" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="184" y="260" width="31" height="31" rx="3"/><rect class="arb-cell is-gnt" x="218" y="260" width="31" height="31" rx="3"/><text class="arb-mark" x="234.0" y="281.0" text-anchor="middle">G</text><rect class="arb-cell is-wait" x="252" y="260" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="286" y="260" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="320" y="260" width="31" height="31" rx="3"/><rect class="arb-cell is-gnt" x="354" y="260" width="31" height="31" rx="3"/><text class="arb-mark" x="370.0" y="281.0" text-anchor="middle">G</text><rect class="arb-cell is-wait" x="388" y="260" width="31" height="31" rx="3"/><text class="tick" x="142" y="315.0" text-anchor="end">req 3</text><rect class="arb-cell is-wait" x="150" y="294" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="184" y="294" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="218" y="294" width="31" height="31" rx="3"/><rect class="arb-cell is-gnt" x="252" y="294" width="31" height="31" rx="3"/><text class="arb-mark" x="268.0" y="315.0" text-anchor="middle">G</text><rect class="arb-cell is-wait" x="286" y="294" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="320" y="294" width="31" height="31" rx="3"/><rect class="arb-cell is-wait" x="354" y="294" width="31" height="31" rx="3"/><rect class="arb-cell is-gnt" x="388" y="294" width="31" height="31" rx="3"/><text class="arb-mark" x="404.0" y="315.0" text-anchor="middle">G</text><text class="legend" x="652" y="360" text-anchor="end">cycle →</text></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="arb-key-gnt"></i>מענק (G)</span><span><i class="arb-key-wait"></i>מבקש ומחכה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏-req :** ‏`~req + 1` מהפך הכול ומוסיף 1, שרץ עד הבקשה הנמוכה ביותר.
    2. **‏AND :** ‏`req & -req` משאיר רק אותה.
    3. **אין בקשה :** ‏`req = 0` נותן `gnt = 0`, בלי מקרה מיוחד.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="function fixed_priority"
        // the lowest requester wins
        function automatic logic [N-1:0] fixed_priority(logic [N-1:0] req);
          return req & (~req + 1'b1);
        endfunction
        ```

    === "Python"
        ```python title="fixed_priority"
        def fixed_priority(req: int) -> int:
            """The lowest requester wins: the lowest set bit."""
            return req & -req
        ```

    #### למה זה נכון { .sol-proof }

    **הביט הנמוך ביותר.** יהי \( k \) הביט הדולק הנמוך ביותר של \( x \). ב-\( \lnot x \) הביטים
    \( 0 \dots k - 1 \) דולקים והביט \( k \) כבוי, ולכן ה-+1 מאפס את \( 0 \dots k - 1 \), מדליק
    את \( k \) ונעצר. מעל \( k \), \( -x \) שווה ל-\( \lnot x \), והם מתאפסים ב-AND עם \( x \).

    **ההרעבה.** אם מבקש 0 מבקש בכל מחזור, `gnt = 1` בכל מחזור, ומבקש 3 מחכה לנצח. אין
    שום \( K \) שחוסם את ההמתנה.

---

### סעיף ב – ‏round robin

??? tip "רמז 1"
    שומרים מצביע : מאיזה מבקש מתחילים לחפש. אחרי מענק, המצביע עובר למבקש **שאחרי** המנצח.

??? tip "רמז 2"
    "הבקשה הראשונה מעמדה \( p \) והלאה" היא `x & ~(x - (1 << p))`. כדי לעבור את הקצה ולהמשיך
    ממבקש 0, מכפילים את הבקשות : ‏`{req, req}`.

<div class="selfcheck" data-answer="3" data-show="3" data-hint="בעומס מלא, כל אחד מהמבקשים האחרים יכול לקבל לפניך פעם אחת לכל היותר." markdown>
עם 4 מבקשים שמבקשים כל הזמן, כמה מחזורים לכל היותר מבקש מחכה בלי מענק?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        שומרים `pri`, מצביע one-hot. ‏`dbl = {req, req}`, ‏`sel = dbl & ~(dbl - pri)` הוא הבקשה הראשונה
        מ-`pri` והלאה, ו-`gnt = sel[N-1:0] | sel[2N-1:N]`. אחרי מענק, `pri` עובר לסיבוב שמאלה של
        `gnt` (המבקש שאחרי המנצח); בלי מענק, `pri` נשאר. בעומס מלא כל מבקש מקבל פעם ב-\( N \)
        מחזורים, ומחכה \( N - 1 \) לכל היותר.

    <!-- cost: שערים \( O(N) \) | השהיה \( O(\log N) \) | פלופים \( N \) -->

    #### הרעיון { .sol-idea }

    **מהמצביע והלאה.** חיסור של \( 2^p \) מ-\( x \) מתחיל בביט \( p \) : אם הוא דולק, הוא
    מתאפס ותו לא; אם לא, הלווה רץ למעלה עד הביט הדולק הראשון ומאפס אותו (והביטים שעבר דולקים).
    ‏\( \lnot(x - 2^p) \) דולק בדיוק בביט הזה מבין הביטים הדולקים של \( x \) מ-\( p \) והלאה, ולכן
    \( x \mathbin{\&} \lnot(x - 2^p) \) הוא הבקשה הראשונה מ-\( p \) והלאה. זו אותה הפעולה
    כמו בסעיף א, רק עם נקודת התחלה.

    **הכפלה במקום מעגל.** אם אין בקשה מ-\( p \) והלאה, צריך להמשיך ממבקש 0. בגרסה הכפולה
    `{req, req}` מבקש 0 מופיע שוב בעמדה \( N \), ולכן החיפוש פשוט ממשיך. התוצאה נמצאת
    בחצי אחד מהשניים, ו-OR של החצאים מחזיר אותה ל-\( N \) ביטים.

    **הדוגמה.** ‏`req = 1011`, העדיפות אצל מבקש 2 : אין בקשה ב-2, ולכן 3 זוכה :

    <!-- gen 2 -->

    | השלב | הביטים (3 עד 0, או 7 עד 0) | מה זה |
    |---|:-:|---|
    | ‏`req` | ‏`1011` | מבקשים 0, 1 ו-3 |
    | ‏`pri` | ‏`0100` | העדיפות אצל מבקש 2 |
    | ‏`dbl = {req, req}` | ‏`10111011` | הבקשות פעמיים, כדי לעבור את הקצה |
    | ‏`dbl - pri` | ‏`10110111` | הלווה רץ מ-`pri` עד הבקשה הראשונה ומאפס אותה |
    | ‏`~(dbl - pri)` | ‏`01001000` | עכשיו רק היא דולקת מבין הבקשות שמעל `pri` |
    | ‏`sel = dbl & ~(dbl - pri)` | ‏`00001000` | הבקשה הראשונה מ-`pri` והלאה, במעגל |
    | ‏`gnt` : ‏OR של שני החצאים | ‏`1000` | מבקש 3 זוכה |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הכפלה :** ‏`dbl = {req, req}`, ‏\( 2N \) ביטים.
    2. **בחירה :** ‏`sel = dbl & ~(dbl - pri)`, כש-`pri` מורחב ל-\( 2N \) ביטים.
    3. **קיפול :** ‏`gnt = sel[N-1:0] | sel[2N-1:N]`.
    4. **מצביע :** אם יש מענק, `pri <= {gnt[N-2:0], gnt[N-1]}` (המבקש שאחרי המנצח); אחרת `pri`
       נשאר.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module rr_arbiter" linenums="1" hl_lines="13 14 15 20"
        module rr_arbiter #(
          parameter int N = 4
        ) (
          input  logic         clk,
          input  logic         rst_n,
          input  logic [N-1:0] req,
          output logic [N-1:0] gnt
        );
          logic [N-1:0]   pri;                                  // one-hot: who is searched first
          logic [2*N-1:0] dbl, sel;

          always_comb begin
            dbl = {req, req};                                   // (1)!
            sel = dbl & ~(dbl - {{N{1'b0}}, pri});              // (2)!
            gnt = sel[N-1:0] | sel[2*N-1:N];
          end

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n)    pri <= N'(1);
            else if (|gnt) pri <= {gnt[N-2:0], gnt[N-1]};       // (3)!
        endmodule
        ```

        1. הבקשות פעמיים : החיפוש ממשיך מעבר למבקש \( N - 1 \) אל מבקש 0.
        2. הבקשה הראשונה מ-`pri` והלאה : החיסור מאפס אותה, וההיפוך וה-AND משאירים רק אותה.
        3. המבקש שאחרי המנצח מקבל עדיפות. בלי מענק המצביע לא זז.

    === "Python"
        ```python title="rr_pick, rr_run" linenums="1" hl_lines="5 6 14"
        def rr_pick(req: int, pri: int, n: int) -> int:
            """The grant of the round robin: the first request at or after the one-hot pri."""
            mask = (1 << 2 * n) - 1
            dbl = req << n | req
            sel = dbl & ~(dbl - pri) & mask       # (1)!
            return (sel | sel >> n) & ((1 << n) - 1)


        def rr_run(reqs: list[int], n: int) -> list[int]:
            pri, grants = 1, []
            for req in reqs:
                gnt = rr_pick(req, pri, n)
                if gnt:
                    pri = (gnt << 1 | gnt >> (n - 1)) & ((1 << n) - 1)   # (2)!
                grants.append(gnt)
            return grants
        ```

        1. ב-Python מספרים לא מוגבלים, ולכן המסכה שומרת על \( 2N \) ביטים.
        2. סיבוב שמאלה של המענק : המבקש שאחריו.

    #### למה זה נכון { .sol-proof }

    **הבחירה.** לפי הרעיון, `sel` הוא הביט הדולק הראשון של `dbl` מעמדה \( p \) והלאה. אם יש
    בקשה ב-\( p \dots N - 1 \), הוא בחצי התחתון; אחרת הוא העותק של הבקשה הראשונה מ-0 בחצי
    העליון. בשני המקרים בדיוק ביט אחד ב-`sel` (או אף אחד, אם `req = 0`), ולכן `gnt` הוא one-hot.

    **ההמתנה.** נניח שמבקש \( i \) מבקש. בכל מחזור שבו הוא לא זוכה, זוכה מישהו אחר \( j \),
    והמצביע עובר ל-\( j + 1 \), כלומר "מתקרב" ל-\( i \) במעגל ולא עובר אותו. כל מבקש אחר יכול
    לזכות לכל היותר פעם אחת לפני \( i \), ולכן \( i \) מחכה לכל היותר \( N - 1 \) מחזורים.
    בעומס מלא החסם מושג : כל אחד מקבל פעם ב-\( N \) מחזורים, כמו בציור בסעיף א.

    #### סיבוכיות { .sol-cost }

    מחסר של \( 2N \) ביטים, \( 2N \) שערי AND ו-\( N \) שערי OR, ו-\( N \) פלופים למצביע. ההשהיה היא
    של שרשרת הלווה, \( O(\log N) \) עם מחסר מהיר. לולאה "מהמצביע והלאה" הייתה מסונתזת לשרשרת
    של \( N \) רמות.

---

### סעיף ג – ‏SVA והוגנות

??? tip "רמז 1"
    שלושה חוקים על ה-arbiter (one-hot, אין מענק בלי בקשה, הוגנות), וחוק אחד על הסביבה :
    בקשה שלא קיבלה נשארת. בלי החוק הזה, איך ייראה כישלון של ההוגנות?

??? tip "רמז 2"
    "מקבל תוך \( K \) מחזורים" הוא `req[i] |-> ##[0:K] gnt[i]`. מסעיף ב, מה \( K \)?

<div class="selfcheck" data-answer="7" data-show="7 = N − 1" data-hint="כל אחד מהמבקשים האחרים יכול לזכות פעם אחת לכל היותר לפניך." markdown>
עם 8 מבקשים, מה החסם הקטן ביותר \( K \) ב-`req[i] |-> ##[0:K] gnt[i]`?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ‏`$onehot0(gnt)`; ‏`(gnt & ~req) == 0`; לכל \( i \) : ‏`req[i] |-> ##[0:N-1] gnt[i]`; ועל
        הסביבה : ‏`req[i] && !gnt[i] |=> req[i]`. ‏\( K = N - 1 \) הוא הקטן ביותר : בעומס מלא יש
        מבקש שמחכה בדיוק \( N - 1 \) מחזורים. הבודק סופר כל כישלון, וכל באג ב-arbiter מפיל
        assertion אחרת.

    #### הרעיון { .sol-idea }

    **ארבעה חוקים.** שלושה על ה-arbiter : לכל היותר מענק אחד, מענק רק למי שביקש, ומי
    שמבקש מקבל תוך \( N - 1 \) מחזורים. חוק אחד על הסביבה : מי שביקש ולא קיבל ממשיך לבקש.
    בלי החוק הרביעי, מבקש שמוריד את הבקשה לפני שקיבל ייראה כהפרה של ההוגנות, אף שה-arbiter
    בסדר; בפורמלי הוא `assume`, ובסימולציה `assert` שבודק את ה-testbench.

    **כל באג ו-assertion משלו.** מצביע שלא זז הופך את ה-arbiter לעדיפות קבועה, והוגנות
    נכשלת. מצביע שעובר **אל** המנצח ולא אחריו נותן לו לזכות שוב ושוב, וגם אז הוגנות נכשלת.
    ‏OR של שתי הבחירות (במקום הבחירה מ-`pri`) נותן שני מענקים, ו-one-hot נכשל. התיבה למטה
    מראה כל אחד מהם.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏one-hot :** ‏`$onehot0(gnt)`, בכל מחזור.
    2. **אין מענק בלי בקשה :** ‏`(gnt & ~req) == '0`.
    3. **הסביבה :** ‏`req[i] && !gnt[i] |=> req[i]`, לכל \( i \).
    4. **הוגנות :** ‏`req[i] |-> ##[0:MAX_WAIT] gnt[i]`, עם `MAX_WAIT = N - 1`.
    5. **‏disable iff :** כל החוקים מושבתים באיפוס.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module arb_checker" linenums="1" hl_lines="11 13 17 19"
        module arb_checker #(
          parameter int N = 4,
          parameter int MAX_WAIT = N - 1
        ) (
          input logic         clk,
          input logic         rst_n,
          input logic [N-1:0] req,
          input logic [N-1:0] gnt
        );
          int fails_onehot = 0, fails_spurious = 0, fails_hold = 0, fails_fair = 0;
          a_onehot: assert property (@(posedge clk) disable iff (!rst_n) $onehot0(gnt))
            else fails_onehot++;
          a_spurious: assert property (@(posedge clk) disable iff (!rst_n) (gnt & ~req) == '0)
            else fails_spurious++;
          for (genvar i = 0; i < N; i++) begin : g_req
            // the environment: a request that was not granted stays (assume in formal)
            a_hold: assert property (@(posedge clk) disable iff (!rst_n) req[i] && !gnt[i] |=> req[i])
              else fails_hold++;
            a_fair: assert property (@(posedge clk) disable iff (!rst_n) req[i] |-> ##[0:MAX_WAIT] gnt[i])   // (1)!
              else fails_fair++;
          end
        endmodule
        ```

        1. ניסיון חדש מתחיל בכל מחזור שבו `req[i]` דולק, וכל אחד צריך מענק בחלון של \( N \) מחזורים.

    === "Python"
        ```python title="check_trace" linenums="1" hl_lines="6 7 8 9"
        def check_trace(reqs: list[int], grants: list[int], n: int, max_wait: int) -> dict:
            """How many times each rule fails on a trace, counted as the assertions count them."""
            T = len(reqs)
            got = lambda t, i: grants[t] >> i & 1   # noqa: E731
            asked = lambda t, i: reqs[t] >> i & 1   # noqa: E731
            onehot = sum(1 for g in grants if g & (g - 1))
            spurious = sum(1 for r, g in zip(reqs, grants) if g & ~r)
            hold = sum(1 for t in range(T - 1) for i in range(n) if asked(t, i) and not got(t, i) and not asked(t + 1, i))
            fair = sum(1 for i in range(n) for t in range(T - max_wait)
                       if asked(t, i) and not any(got(u, i) for u in range(t, t + max_wait + 1)))   # (1)!
            return {"onehot": onehot, "spurious": spurious, "hold": hold, "fair": fair}
        ```

        1. ניסיון שהחלון שלו עובר את סוף הטרייס לא נספר, כמו ב-assertion שעוד לא הסתיימה.

    #### למה זה נכון { .sol-proof }

    **‏\( K = N - 1 \) מספיק** לפי ההוכחה של סעיף ב, בהנחה שהבקשה נשארת. **והוא הכרחי** :
    בעומס מלא, מבקש שזה עתה קיבל מבקש שוב במחזור הבא, ומקבל רק אחרי \( N - 1 \) מחזורים.
    עם \( K = N - 2 \) ה-assertion הייתה נכשלת על arbiter תקין.

    **ה-assertions נבדקות.** הטסט של השאלה מריץ את `arb_checker` ב-Verilator על תנועה אקראית
    שמכבדת את חוק הסביבה, עם ה-arbiter התקין ועם שלושת הבאגים, ומשווה את המונים לספירה של
    `check_trace` בדיוק. ה-arbiter התקין לא מפיל אף אחת; כל באג מפיל את שלו.

    **נסו בעצמכם.** מציירים בקשות על הרשת (או בוחרים דוגמה), ורואים איך עדיפות קבועה, ‏round
    robin ו-WRR מחלקים את המענקים, עם ההמתנה הארוכה ביותר לכל מבקש. הלוח "הטריק" מראה את
    החישוב של `sel` במחזור הנבחר, והמתג "באג" מכניס אחד משלושת הבאגים ומסמן את ה-assertions
    שנכשלות :

    <div class="explorer" data-kind="arbiter"></div>

---

### סעיף ד – משקלים

??? tip "רמז 1"
    במקום להעביר את המצביע אחרי כל מענק, נותנים למבקש לשמור אותו עד \( w_i \) מענקים ברצף.

??? tip "רמז 2"
    צריך מונה : כמה מענקים קיבל בעל המצביע בתור הנוכחי. מתי מאפסים אותו?

<div class="selfcheck" data-answer="9" data-show="9 = 2 + 3 + 4" data-hint="בעומס מלא, כל אחד מהאחרים לוקח עד המשקל שלו ברצף לפניך." markdown>
עם משקלים 1, ‏2, ‏3 ו-4, כמה מחזורים לכל היותר מחכה מבקש 0?
</div>

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        מונה `used` של המענקים שבעל המצביע קיבל ברצף. אם המנצח הוא בעל המצביע, `used` גדל; אחרת
        מתחיל תור חדש עם `used = 1`. כש-`used` מגיע ל-\( w_i \), המצביע עובר למבקש שאחרי \( i \)
        ו-`used` מתאפס; אחרת המצביע נשאר על \( i \). בעומס מלא \( i \) מקבל \( w_i / \sum w \),
        וההמתנה הארוכה ביותר שלו היא \( \sum_{j \ne i} w_j \).

    <!-- cost: פלופים \( N + \log_2 w_{\max} \) | השהיה כמו round robin -->

    #### הרעיון { .sol-idea }

    **תור של \( w_i \) מענקים.** ה-round robin הוא WRR עם כל המשקלים 1. עם משקלים, המצביע
    "נדבק" למנצח עד שהוא מנצל את המשקל שלו, או עד שהוא מפסיק לבקש (ואז הבחירה מהמצביע
    עוברת למבקש הבא ממילא). בעומס מלא נוצר מחזור של \( \sum w \) מחזורים שבו כל \( i \) מקבל
    \( w_i \) מענקים ברצף.

    **המחיר.** ההוגנות נשמרת, אבל החסם גדל : מבקש עם משקל 1 מחכה לכל התורות של כל האחרים.
    עם משקלים 1, 2, 3 ו-4, מבקש 0 מחכה עד 9 מחזורים ומקבל 10% :

    <!-- gen 3 -->

    | המבקש | המשקל | החלק שלו בעומס מלא | ההמתנה הארוכה ביותר | ‏\( \sum_{j \ne i} w_j \) |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏0 | ‏1 | ‏1/10 = 10% | ‏9 | ‏9 |
    | ‏1 | ‏2 | ‏2/10 = 20% | ‏8 | ‏8 |
    | ‏2 | ‏3 | ‏3/10 = 30% | ‏7 | ‏7 |
    | ‏3 | ‏4 | ‏4/10 = 40% | ‏6 | ‏6 |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="module wrr_arbiter" linenums="1" hl_lines="17 20 28 31"
        module wrr_arbiter #(
          parameter int N  = 4,
          parameter int WB = 4                                   // bits of a weight
        ) (
          input  logic          clk,
          input  logic          rst_n,
          input  logic [N-1:0]  req,
          input  logic [WB-1:0] weight [N],                      // 1 or more
          output logic [N-1:0]  gnt
        );
          logic [N-1:0]   pri, next;
          logic [2*N-1:0] dbl, sel;
          logic [WB-1:0]  used, w;

          always_comb begin
            dbl  = {req, req};
            sel  = dbl & ~(dbl - {{N{1'b0}}, pri});              // the same pick as round robin
            gnt  = sel[N-1:0] | sel[2*N-1:N];
            w    = '0;
            for (int i = 0; i < N; i++) if (gnt[i]) w = weight[i];
            next = {gnt[N-2:0], gnt[N-1]};
          end

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin
              pri <= N'(1); used <= '0;
            end else if (|gnt) begin
              if ((gnt == pri ? used + 1'b1 : WB'(1)) == w) begin   // (1)!
                pri <= next; used <= '0;
              end else begin
                pri <= gnt; used <= (gnt == pri) ? used + 1'b1 : WB'(1);   // (2)!
              end
            end
        endmodule
        ```

        1. המענק הזה סוגר את התור : \( w_i \) מענקים ברצף. המצביע עובר למבקש שאחרי המנצח.
        2. התור נמשך : המצביע נשאר על המנצח. מנצח חדש מתחיל תור עם `used = 1`.

    === "Python"
        ```python title="wrr_run" linenums="1" hl_lines="7 8 9"
        def wrr_run(reqs: list[int], weights: list[int]) -> list[int]:
            n, pri, used, grants = len(weights), 1, 0, []
            for req in reqs:
                gnt = rr_pick(req, pri, n)
                if gnt:
                    i = gnt.bit_length() - 1
                    used = used + 1 if gnt == pri else 1          # (1)!
                    if used == weights[i]:
                        pri, used = (gnt << 1 | gnt >> (n - 1)) & ((1 << n) - 1), 0
                    else:
                        pri = gnt
                grants.append(gnt)
            return grants
        ```

        1. בעל המצביע ממשיך את התור שלו; מנצח אחר (בעל המצביע לא ביקש) מתחיל תור חדש.

    #### למה זה נכון { .sol-proof }

    **החלק בעומס מלא.** כשכולם מבקשים, המצביע עובר על המבקשים לפי הסדר, וכל אחד מחזיק אותו
    בדיוק \( w_i \) מענקים. המחזור הוא \( \sum w \) מחזורים, ו-\( i \) מקבל \( w_i \) מהם.

    **ההמתנה.** כשמבקש \( i \) מחכה, כל מבקש אחר \( j \) מחזיק את המצביע לכל היותר תור אחד,
    כלומר \( w_j \) מענקים, לפני שהמצביע מגיע ל-\( i \). לכן ההמתנה חסומה ב-\( \sum_{j \ne i} w_j \),
    והחסם מושג בעומס מלא כש-\( i \) בדיוק סיים תור. ב-assertion : ‏`MAX_WAIT = W - w_min`.

    **הבדיקה.** הטסט של השאלה מריץ את המודול ב-Verilator מול `wrr_run` ומול מימוש עם לולאה
    מהמצביע, על תנועה אקראית ומשקלים אקראיים, ובודק את החלוקה ואת החסם.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : המצביע עובר אל המנצח ולא אחריו"
    ‏`pri <= gnt` במקום הסיבוב : המנצח נשאר עם העדיפות הגבוהה ביותר, וכל עוד הוא מבקש הוא
    זוכה. זו עדיפות "דביקה", לא סבב, וההוגנות נכשלת בעומס מלא.

??? trap "מלכודת : לעדכן את המצביע גם בלי מענק"
    "מקדמים את המצביע בכל מחזור" נראה הוגן, אבל המענק הבא תלוי במחזור שבו הבקשות מגיעות,
    והחסם \( N - 1 \) כבר לא מובטח : מבקש יכול להיות "מאחורי" המצביע בכל פעם שהוא מבקש.

??? trap "מלכודת : הוגנות בלי הנחה על הסביבה"
    ‏`req[i] |-> ##[0:N-1] gnt[i]` בלי הדרישה שבקשה נשארת : ‏testbench שמרים ומוריד בקשות באקראי
    יפיל את ה-assertion על arbiter תקין, וכולם יתחילו להתעלם ממנה.

??? trap "מלכודת : מענק צירופי שמגיע ל-req באותו מחזור"
    ‏`gnt` נגזר צירופית מ-`req`. אם המבקש מחשב את `req` מ-`gnt` (למשל "מוריד את הבקשה כשקיבל"
    באותו מחזור), נוצרת לולאה צירופית. בממשקים כאלה `gnt` רשום, ואז ההמתנה גדלה במחזור.

??? followup "שאלות המשך"
    - **‏N שאינו חזקה של 2 ו-N גדול :** מה משתנה ב-RTL כש-\( N = 64 \)?

        ??? fu-answer "תשובה"
            כלום בנכונות; ההשהיה של מחסר של 128 ביטים היא הבעיה. מחלקים לקבוצות (arbiter של
            קבוצות מעל arbiters בתוך כל קבוצה), או משתמשים ב-parallel prefix ל-"הביט הראשון".

    - **‏arbiter עם תור מצביעים (matrix arbiter) :** מה היתרון?

        ??? fu-answer "תשובה"
            מטריצה \( N \times N \) של "i עדיף על j" : אחרי מענק ל-\( i \), כל השורה שלו מתאפסת. זה LRU
            מדויק (מי שקיבל הכי מזמן עדיף), במחיר \( N^2 / 2 \) פלופים.

    - **‏grant רשום :** מה משתנה ב-assertions אם `gnt` יוצא מרגיסטר?

        ??? fu-answer "תשובה"
            המענק מגיע מחזור אחרי הבקשה : ‏`req[i] |-> ##[1:N] gnt[i]`, ו-"אין מענק בלי בקשה" נבדק
            מול `$past(req)`.

    - **כיסוי :** איך יודעים שה-testbench בכלל בדק את החסם?

        ??? fu-answer "תשובה"
            ‏`cover property (req[i] && !gnt[i] [*N-1] ##1 gnt[i])` : הגענו להמתנה של \( N - 1 \) מחזורים. בלי
            זה, assertion של הוגנות שעוברת לא אומרת שהמקרה הקשה קרה.
