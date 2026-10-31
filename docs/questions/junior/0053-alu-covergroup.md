---
id: 53
title: Covergroup ל-ALU – bins, cross ומתי הכיסוי נסגר
level: junior
difficulty: medium
kind: dv
tags: [coverage, systemverilog, python, randomization]
source: "שאלת ראיון נפוצה לתפקידי אימות (functional coverage)"
added: 2026-10-27
---

## השאלה

ל-ALU יש פעולה `op` מתוך חמש : ‏`ADD`, ‏`SUB`, ‏`AND`, ‏`OR` ו-`SHL` (קוד של 3 ביטים, והקודים
5 עד 7 לא מוגדרים), שני אופרנדים `a` ו-`b` של 8 ביטים, ודגל `carry` ביציאה. ה-testbench
מגריל טרנזקציות, ואתם אחראים על הכיסוי הפונקציונלי.

- **סעיף א – ‏coverpoints ו-bins :** כתבו covergroup שמודד את כל הפעולות, את ערכי הקצה
  של האופרנדים (0, ‏0xFF ו-0x80) ואת `carry`, רק בפעולות שבהן יש לו משמעות. כמה bins יש?
- **סעיף ב – ‏cross :** הוסיפו cross של הפעולה עם שני האופרנדים. אילו תאים לא כדאי לספור,
  ואיך? כמה תאים נשארים, ומה אחוז הכיסוי אחרי טרנזקציה אחת?
- **סעיף ג – מתי זה נסגר :** כמה טרנזקציות אקראיות צריך בממוצע עד שכל ה-cross מכוסה, עם
  `randomize()` רגיל? ומה `dist` משנה?

??? interviewer "מה המראיין בודק"
    - **‏bins ולא ערכים :** האם המועמד מגדיר מחלקות של ערכים שמעניינות את התכנון, במקום 256
      bins אוטומטיים לכל אופרנד.
    - **‏illegal מול ignore :** האם הוא יודע ש-`illegal_bins` עוצר את הטסט, ו-`ignore_bins` רק
      מוריד תא מהספירה.
    - **מה נחשב :** ‏`iff`, תאים בלתי אפשריים ב-cross, ולמה כיסוי שלא מגיע ל-100% לפעמים הוא
      באג בהגדרה ולא בטסט.
    - **הסתברות :** האם הוא מבין שגירוי אחיד כמעט לא פוגע בערכי קצה, ויודע לחשב כמה זמן זה
      ייקח.
    - **פעולה :** מה עושים עם התוצאה : ‏`dist`, טסט מכוון, או החלטה שהתא לא חשוב.

---

### סעיף א – ‏coverpoints ו-bins

??? tip "רמז 1"
    בלי `bins` מפורשים, coverpoint של 8 ביטים מקבל bins אוטומטיים (עד 64 כברירת מחדל, כל
    אחד טווח). האם הם אומרים משהו על 0x80?

??? tip "רמז 2"
    ‏bin יכול להיות ערך אחד (`{8'h80}`) או קבוצה של טווחים (`{[1:127], [129:254]}`). ול-`carry`
    יש `iff`.

<div class="selfcheck" data-answer="15" data-show="15 = 5 + 4 + 4 + 2" data-hint="חמש פעולות, ארבע מחלקות לכל אופרנד, ושני ערכים ל-carry." markdown>
כמה bins יש בארבעת ה-coverpoints יחד, בלי ה-cross?
</div>

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏`cp_op` עם bin לכל פעולה ו-`illegal_bins` לקודים 5 עד 7; ‏`cp_a` ו-`cp_b` עם ארבעה bins :
        ‏zero, ‏max, ‏msb ו-mid (כל השאר); ‏`cp_carry` עם `iff (op inside {ADD, SUB, SHL})`.
        יחד 15 bins.

    #### הרעיון { .sol-idea }

    **‏bin הוא שאלה.** כל bin שואל "האם הגענו למצב הזה?", ולכן מגדירים bins לפי מה
    שמעניין את התכנון ולא לפי ערכים : 0 (כל הביטים כבויים), ‏0xFF (כולם דולקים, גלישה ב-ADD),
    ‏0x80 (רק הביט העליון, סימן וגלישה), וכל השאר יחד. 256 bins לכל אופרנד היו נותנים
    מספר בלי משמעות, ו-bins אוטומטיים לא מבטיחים שאף אחד מהם הוא בדיוק 0x80.

    **מה לא נחשב.** קוד פעולה 5 עד 7 הוא באג, ולכן `illegal_bins` : הסימולטור מדווח שגיאה
    כשהוא מופיע. ‏`carry` של `AND` ו-`OR` לא מוגדר, ולכן `iff` : הדגימה פשוט לא נספרת.

    <!-- gen 0 -->

    | ה-coverpoint | ה-bins | כמה |
    |---|---|:-:|
    | ‏`cp_op` | ‏ADD, ‏SUB, ‏AND, ‏OR, ‏SHL; ‏`illegal_bins` לקודים 5 עד 7 | ‏5 |
    | ‏`cp_a` | ‏zero ‏(0), ‏max ‏(0xFF), ‏msb ‏(0x80), ‏mid (כל השאר) | ‏4 |
    | ‏`cp_b` | כמו `cp_a` | ‏4 |
    | ‏`cp_carry` | ‏0 ו-1, רק כש-`op` הוא ADD, ‏SUB או SHL (‏`iff`) | ‏2 |
    | ‏`x_op_a_b` | ‏\( 5 \times 4 \times 4 = 80 \), פחות 8 תאים של SHL ב-0x80 או 0xFF | ‏72 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏cp_op :** ‏bin לכל פעולה, ו-`illegal_bins` לשאר הקודים.
    2. **‏cp_a ו-cp_b :** ארבעה bins : שלושה ערכי קצה ו-bin אחד לכל השאר.
    3. **‏cp_carry :** שני ה-bins האוטומטיים (0 ו-1), עם `iff` לפעולות שיש בהן carry.
    4. **דגימה :** ‏`sample()` עם ארגומנטים, מהמוניטור, פעם אחת לכל טרנזקציה.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="value_bin, AluCoverage" linenums="1" hl_lines="6 16 23 29 34"
        OPS = ("ADD", "SUB", "AND", "OR", "SHL")
        CARRY_OPS = ("ADD", "SUB", "SHL")


        def value_bin(v: int) -> str:
            return {0x00: "zero", 0xFF: "max", 0x80: "msb"}.get(v, "mid")   # (1)!


        def ignored(op: str, b_bin: str) -> bool:
            return op == "SHL" and b_bin in ("max", "msb")


        class AluCoverage:
            """The covergroup as a model: the bins hit, and the group's coverage the LRM way
            (the average of its coverpoints and its cross, each the share of its bins hit)."""
            SIZES = {"op": 5, "a": 4, "b": 4, "carry": 2, "cross": 5 * 4 * 4 - 8}

            def __init__(self):
                self.hit = {k: set() for k in self.SIZES}

            def sample(self, op: str, a: int, b: int, carry: int) -> None:
                if op not in OPS:
                    raise ValueError(f"illegal op {op}")                  # (2)!
                xa, xb = value_bin(a), value_bin(b)
                self.hit["op"].add(op)
                self.hit["a"].add(xa)
                self.hit["b"].add(xb)
                if op in CARRY_OPS:
                    self.hit["carry"].add(carry)                          # (3)!
                if not ignored(op, xb):
                    self.hit["cross"].add((op, xa, xb))

            def coverage(self) -> float:
                return 100 * sum(len(self.hit[k]) / n for k, n in self.SIZES.items()) / len(self.SIZES)
        ```

        1. אותן ארבע מחלקות כמו ב-covergroup.
        2. ‏`illegal_bins` : קוד לא מוגדר הוא שגיאה.
        3. ‏`iff` : רק בפעולות שיש בהן carry.

    === "SystemVerilog"
        ```systemverilog title="covergroup alu_cg" linenums="1" hl_lines="6 9 16 18"
        typedef enum logic [2:0] {ADD, SUB, AND, OR, SHL} alu_op_e;

        covergroup alu_cg with function sample(alu_op_e op, logic [7:0] a, logic [7:0] b, logic carry);
          cp_op: coverpoint op {
            bins add = {ADD}; bins sub = {SUB}; bins and_ = {AND}; bins or_ = {OR}; bins shl = {SHL};
            illegal_bins undefined = {[5:7]};                       // (1)!
          }
          cp_a: coverpoint a {
            bins zero = {8'h00}; bins max = {8'hFF}; bins msb = {8'h80};   // (2)!
            bins mid  = {[8'h01:8'h7F], [8'h81:8'hFE]};
          }
          cp_b: coverpoint b {
            bins zero = {8'h00}; bins max = {8'hFF}; bins msb = {8'h80};
            bins mid  = {[8'h01:8'h7F], [8'h81:8'hFE]};
          }
          cp_carry: coverpoint carry iff (op inside {ADD, SUB, SHL});   // (3)!
          x_op_a_b: cross cp_op, cp_a, cp_b {
            ignore_bins shl_out = binsof(cp_op.shl) && (binsof(cp_b.max) || binsof(cp_b.msb));   // (4)!
          }
        endgroup
        ```

        1. קוד לא מוגדר הוא שגיאה, לא חור בכיסוי : הסימולטור מדווח עליו ברגע שהוא מופיע.
        2. ערכי הקצה, כל אחד bin משלו. ‏`mid` הוא bin אחד של שני טווחים.
        3. ‏`iff` : בפעולות `AND` ו-`OR` הדגימה של `carry` לא נספרת בכלל.
        4. סעיף ב : הזזה ב-0x80 או ב-0xFF מוציאה את כל הביטים, והתוצאה תמיד אפס. התאים האלה לא נספרים.

    #### למה זה נכון { .sol-proof }

    **הספירה.** ‏5 bins לפעולה, 4 לכל אופרנד ו-2 ל-`carry` : ‏15. ה-`illegal_bins` לא נספר,
    כי הוא לא משהו שצריך להגיע אליו; וגם לא bins אוטומטיים, כי הגדרנו bins מפורשים.

    **בדיקה בסימולטור.** הטסט של השאלה מריץ את ה-covergroup הזה ב-Verilator, ומשווה את
    `get_inst_coverage()` למודל ה-Python על אותן טרנזקציות.

---

### סעיף ב – ‏cross

??? tip "רמז 1"
    ‏cross של שלושה coverpoints הוא מכפלה : כמה צירופים יש? האם כולם הגיוניים?

??? tip "רמז 2"
    ‏`SHL` ב-0x80 או ב-0xFF מוציא את כל הביטים. האם צריך לבדוק את זה פעם לכל מחלקה של `a`?
    ומה ההבדל בין להתעלם מתא לבין להגדיר אותו כאסור?

<div class="selfcheck" data-answer="72" data-show="72 = 80 − 8" data-hint="5 כפול 4 כפול 4 צירופים, פחות התאים של SHL כש-b הוא 0x80 או 0xFF, לכל ערך של a." markdown>
כמה תאים יש ב-cross אחרי ה-ignore?
</div>

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏`cross cp_op, cp_a, cp_b` נותן \( 5 \cdot 4 \cdot 4 = 80 \) תאים. ‏8 מהם (`SHL` עם `b`
        שהוא 0x80 או 0xFF, לכל אחת מ-4 המחלקות של `a`) לא מעניינים, ולכן `ignore_bins` : נשארים
        72. ‏`illegal_bins` רק למה שאסור שיקרה. אחרי טרנזקציה אחת הכיסוי \( 24.28\% \) : הממוצע
        של \( 20, 25, 25, 50 \) ו-\( 100/72 \).

    #### הרעיון { .sol-idea }

    **ה-cross הוא המקום שבו מתגלים באגים.** כל פעולה בנפרד וכל ערך קצה בנפרד קלים לכסות;
    ‏`SUB` עם `a = 0` ו-`b = 0x80` הוא צירוף שהטסט אולי מעולם לא הגיע אליו. לכן ה-cross הוא
    רוב העבודה, 72 מתוך 87 bins.

    **‏ignore מול illegal.** תא שלא מעניין (הזזה שמאפסת הכול) מקבל `ignore_bins` : הוא לא
    נספר, ואם הוא מופיע זה בסדר. תא שאסור שיופיע מקבל `illegal_bins` : הופעה שלו היא שגיאה.
    לסמן תא לגיטימי כ-illegal מפיל טסטים טובים; לא לסמן תא בלתי אפשרי בכלל משאיר את הכיסוי
    מתחת ל-100% לתמיד.

    **הכיסוי של הקבוצה.** לפי ה-LRM, הכיסוי של covergroup הוא ממוצע (עם משקל 1 לכל אחד) של
    הכיסוי של כל coverpoint וכל cross, וכל אחד מהם הוא החלק של ה-bins שלו שנפגעו. לכן cross
    גדול שכמעט לא כוסה מוריד את הממוצע רק בחמישית.

    <!-- gen 1 -->

    <svg class="figure cg-fig" viewBox="0 0 660 196" style="max-width:41rem" role="img" aria-label="ה-cross של op, a ו-b : חמש מפות של 4 על 4, תאים נדירים כהים, ושמונה תאים של SHL מסומנים כמושמטים"><defs><pattern id="cg-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" class="cg-hatch-line"/></pattern></defs><text class="cg-op" x="98" y="22" text-anchor="middle">ADD</text><rect class="cg-cell is-r2" x="46" y="34" width="24" height="24"><title>ADD, a zero, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="72" y="34" width="24" height="24"><title>ADD, a zero, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="98" y="34" width="24" height="24"><title>ADD, a zero, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="124" y="34" width="24" height="24"><title>ADD, a zero, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r2" x="46" y="60" width="24" height="24"><title>ADD, a max, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="72" y="60" width="24" height="24"><title>ADD, a max, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="98" y="60" width="24" height="24"><title>ADD, a max, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="124" y="60" width="24" height="24"><title>ADD, a max, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r2" x="46" y="86" width="24" height="24"><title>ADD, a msb, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="72" y="86" width="24" height="24"><title>ADD, a msb, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="98" y="86" width="24" height="24"><title>ADD, a msb, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="124" y="86" width="24" height="24"><title>ADD, a msb, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="46" y="112" width="24" height="24"><title>ADD, a mid, b zero: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="72" y="112" width="24" height="24"><title>ADD, a mid, b max: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="98" y="112" width="24" height="24"><title>ADD, a mid, b msb: p = 253/327680</title></rect><rect class="cg-cell is-r0" x="124" y="112" width="24" height="24"><title>ADD, a mid, b mid: p = 64009/327680</title></rect><text class="tick" x="40" y="51" text-anchor="end">0</text><text class="tick" x="40" y="77" text-anchor="end">FF</text><text class="tick" x="40" y="103" text-anchor="end">80</text><text class="tick" x="40" y="129" text-anchor="end">mid</text><text class="tick" x="58.0" y="152" text-anchor="middle">0</text><text class="tick" x="84.0" y="152" text-anchor="middle">FF</text><text class="tick" x="110.0" y="152" text-anchor="middle">80</text><text class="tick" x="136.0" y="152" text-anchor="middle">mid</text><text class="cg-op" x="216" y="22" text-anchor="middle">SUB</text><rect class="cg-cell is-r2" x="164" y="34" width="24" height="24"><title>SUB, a zero, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="190" y="34" width="24" height="24"><title>SUB, a zero, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="216" y="34" width="24" height="24"><title>SUB, a zero, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="242" y="34" width="24" height="24"><title>SUB, a zero, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r2" x="164" y="60" width="24" height="24"><title>SUB, a max, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="190" y="60" width="24" height="24"><title>SUB, a max, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="216" y="60" width="24" height="24"><title>SUB, a max, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="242" y="60" width="24" height="24"><title>SUB, a max, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r2" x="164" y="86" width="24" height="24"><title>SUB, a msb, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="190" y="86" width="24" height="24"><title>SUB, a msb, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="216" y="86" width="24" height="24"><title>SUB, a msb, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="242" y="86" width="24" height="24"><title>SUB, a msb, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="164" y="112" width="24" height="24"><title>SUB, a mid, b zero: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="190" y="112" width="24" height="24"><title>SUB, a mid, b max: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="216" y="112" width="24" height="24"><title>SUB, a mid, b msb: p = 253/327680</title></rect><rect class="cg-cell is-r0" x="242" y="112" width="24" height="24"><title>SUB, a mid, b mid: p = 64009/327680</title></rect><text class="tick" x="176.0" y="152" text-anchor="middle">0</text><text class="tick" x="202.0" y="152" text-anchor="middle">FF</text><text class="tick" x="228.0" y="152" text-anchor="middle">80</text><text class="tick" x="254.0" y="152" text-anchor="middle">mid</text><text class="cg-op" x="334" y="22" text-anchor="middle">AND</text><rect class="cg-cell is-r2" x="282" y="34" width="24" height="24"><title>AND, a zero, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="308" y="34" width="24" height="24"><title>AND, a zero, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="334" y="34" width="24" height="24"><title>AND, a zero, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="360" y="34" width="24" height="24"><title>AND, a zero, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r2" x="282" y="60" width="24" height="24"><title>AND, a max, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="308" y="60" width="24" height="24"><title>AND, a max, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="334" y="60" width="24" height="24"><title>AND, a max, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="360" y="60" width="24" height="24"><title>AND, a max, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r2" x="282" y="86" width="24" height="24"><title>AND, a msb, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="308" y="86" width="24" height="24"><title>AND, a msb, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="334" y="86" width="24" height="24"><title>AND, a msb, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="360" y="86" width="24" height="24"><title>AND, a msb, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="282" y="112" width="24" height="24"><title>AND, a mid, b zero: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="308" y="112" width="24" height="24"><title>AND, a mid, b max: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="334" y="112" width="24" height="24"><title>AND, a mid, b msb: p = 253/327680</title></rect><rect class="cg-cell is-r0" x="360" y="112" width="24" height="24"><title>AND, a mid, b mid: p = 64009/327680</title></rect><text class="tick" x="294.0" y="152" text-anchor="middle">0</text><text class="tick" x="320.0" y="152" text-anchor="middle">FF</text><text class="tick" x="346.0" y="152" text-anchor="middle">80</text><text class="tick" x="372.0" y="152" text-anchor="middle">mid</text><text class="cg-op" x="452" y="22" text-anchor="middle">OR</text><rect class="cg-cell is-r2" x="400" y="34" width="24" height="24"><title>OR, a zero, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="426" y="34" width="24" height="24"><title>OR, a zero, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="452" y="34" width="24" height="24"><title>OR, a zero, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="478" y="34" width="24" height="24"><title>OR, a zero, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r2" x="400" y="60" width="24" height="24"><title>OR, a max, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="426" y="60" width="24" height="24"><title>OR, a max, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="452" y="60" width="24" height="24"><title>OR, a max, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="478" y="60" width="24" height="24"><title>OR, a max, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r2" x="400" y="86" width="24" height="24"><title>OR, a msb, b zero: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="426" y="86" width="24" height="24"><title>OR, a msb, b max: p = 1/327680</title></rect><rect class="cg-cell is-r2" x="452" y="86" width="24" height="24"><title>OR, a msb, b msb: p = 1/327680</title></rect><rect class="cg-cell is-r1" x="478" y="86" width="24" height="24"><title>OR, a msb, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="400" y="112" width="24" height="24"><title>OR, a mid, b zero: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="426" y="112" width="24" height="24"><title>OR, a mid, b max: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="452" y="112" width="24" height="24"><title>OR, a mid, b msb: p = 253/327680</title></rect><rect class="cg-cell is-r0" x="478" y="112" width="24" height="24"><title>OR, a mid, b mid: p = 64009/327680</title></rect><text class="tick" x="412.0" y="152" text-anchor="middle">0</text><text class="tick" x="438.0" y="152" text-anchor="middle">FF</text><text class="tick" x="464.0" y="152" text-anchor="middle">80</text><text class="tick" x="490.0" y="152" text-anchor="middle">mid</text><text class="cg-op" x="570" y="22" text-anchor="middle">SHL</text><rect class="cg-cell is-r2" x="518" y="34" width="24" height="24"><title>SHL, a zero, b zero: p = 1/327680</title></rect><rect class="cg-cell is-ign" x="544" y="34" width="24" height="24"><title>SHL, a zero, b max: ignored</title></rect><rect class="cg-cell is-ign" x="570" y="34" width="24" height="24"><title>SHL, a zero, b msb: ignored</title></rect><rect class="cg-cell is-r1" x="596" y="34" width="24" height="24"><title>SHL, a zero, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r2" x="518" y="60" width="24" height="24"><title>SHL, a max, b zero: p = 1/327680</title></rect><rect class="cg-cell is-ign" x="544" y="60" width="24" height="24"><title>SHL, a max, b max: ignored</title></rect><rect class="cg-cell is-ign" x="570" y="60" width="24" height="24"><title>SHL, a max, b msb: ignored</title></rect><rect class="cg-cell is-r1" x="596" y="60" width="24" height="24"><title>SHL, a max, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r2" x="518" y="86" width="24" height="24"><title>SHL, a msb, b zero: p = 1/327680</title></rect><rect class="cg-cell is-ign" x="544" y="86" width="24" height="24"><title>SHL, a msb, b max: ignored</title></rect><rect class="cg-cell is-ign" x="570" y="86" width="24" height="24"><title>SHL, a msb, b msb: ignored</title></rect><rect class="cg-cell is-r1" x="596" y="86" width="24" height="24"><title>SHL, a msb, b mid: p = 253/327680</title></rect><rect class="cg-cell is-r1" x="518" y="112" width="24" height="24"><title>SHL, a mid, b zero: p = 253/327680</title></rect><rect class="cg-cell is-ign" x="544" y="112" width="24" height="24"><title>SHL, a mid, b max: ignored</title></rect><rect class="cg-cell is-ign" x="570" y="112" width="24" height="24"><title>SHL, a mid, b msb: ignored</title></rect><rect class="cg-cell is-r0" x="596" y="112" width="24" height="24"><title>SHL, a mid, b mid: p = 64009/327680</title></rect><text class="tick" x="530.0" y="152" text-anchor="middle">0</text><text class="tick" x="556.0" y="152" text-anchor="middle">FF</text><text class="tick" x="582.0" y="152" text-anchor="middle">80</text><text class="tick" x="608.0" y="152" text-anchor="middle">mid</text><text class="legend" x="652" y="188" text-anchor="end">rows: a, columns: b</text></svg>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="cg-key-r2"></i>שני ערכי קצה : ‏1 ל-327,680</span><span><i class="cg-key-r1"></i>ערך קצה אחד : ‏1 ל-1,295 בערך</span><span><i class="cg-key-r0"></i>בלי ערכי קצה : ‏1 ל-5.1 בערך</span><span><i class="cg-key-ign"></i>‏ignore_bins</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מכפלה :** ‏5 פעולות כפול 4 מחלקות של `a` כפול 4 של `b` : ‏80 תאים.
    2. **מה לא מעניין :** ‏`SHL` שמוציא את כל הביטים, 2 מחלקות של `b` כפול 4 של `a` : ‏8 תאים.
    3. **‏ignore_bins עם binsof :** ‏`binsof(cp_op.shl) && (binsof(cp_b.max) || binsof(cp_b.msb))`.
    4. **אחרי טרנזקציה אחת :** \( (1/5 + 1/4 + 1/4 + 1/2 + 1/72) / 5 = 24.28\% \).

    </div>

    #### למה זה נכון { .sol-proof }

    **הסימולטור מסכים.** ב-Verilator, אחרי `sample(ADD, 0, 0, 0)` אחד, `get_inst_coverage()`
    מחזיר 24.277778, ואחרי סריקה של כל הפעולות וכל המחלקות הוא מחזיר 100 בדיוק : ה-8 תאים
    לא נספרים. הטסט של השאלה בודק את שני המספרים ואת המודל של ה-Python על טרנזקציות
    אקראיות.

    **מלכודת ה-get_coverage.** ‏`get_coverage()` מחזיר את הכיסוי של **הסוג** (כל המופעים יחד),
    ו-`get_inst_coverage()` של המופע. עם שני מופעים של אותו covergroup, המספרים שונים.

---

### סעיף ג – מתי זה נסגר

??? tip "רמז 1"
    כל טרנזקציה פוגעת בדיוק בתא אחד של ה-cross (או בתא מושמט). זו בעיית אספן הקופונים, כמו
    ב[שאלה 0041](0041-coverage-random-tests.md). מה ההסתברות של התא הנדיר ביותר?

??? tip "רמז 2"
    עם `randomize()` רגיל, \( P(a = 0) = 1/256 \). תא של `op` מסוים עם שני ערכי קצה : 
    \( \frac15 \cdot \frac{1}{256} \cdot \frac{1}{256} \).

<div class="selfcheck" data-answer="327680" data-show="1/327,680" data-hint="פעולה אחת מתוך 5, וערך קצה מסוים מתוך 256 לכל אחד משני האופרנדים." markdown>
אחד חלקי כמה היא ההסתברות של התא הנדיר ביותר, עם `randomize()` רגיל?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        עם גירוי אחיד, 39 תאים הם בהסתברות \( 1/327{,}680 \), והתוחלת עד שכל ה-cross מכוסה היא
        כ-**1.39 מיליון** טרנזקציות. עם `dist` שנותן לכל ערך קצה 1/5, היא **534**; ואם כל
        מחלקה מקבלת 1/4, ‏**389**, בדיוק \( 80 H_{72} \). ‏`dist` לא משנה את מה שנבדק, רק את
        ההסתברויות.

    <!-- cost: זמן \( O(\text{cells} \cdot \text{steps}) \) -->

    #### הרעיון { .sol-idea }

    **אספן קופונים לא שוויוני.** כל טרנזקציה בוחרת תא אחד, וצריך לאסוף את כל 72 התאים.
    כשההסתברויות שונות, התוחלת היא
    \( E = \int_0^\infty \left(1 - \prod_i (1 - e^{-p_i t})\right) dt \)
    (כמו ב-0041), והיא נשלטת על ידי התאים הנדירים : בערך \( \frac{1}{p_{\min}} \ln(\#\text{rare}) \).

    **גירוי אחיד כמעט לא פוגע בקצוות.** ‏`a = 0` הוא 1 מתוך 256, ושני אופרנדים קיצוניים יחד
    עם פעולה מסוימת הם 1 מתוך 327,680. לכן הכיסוי מגיע מהר ל-90% ונתקע שם.

    **‏dist.** ‏`a dist {8'h00 := 1, 8'hFF := 1, 8'h80 := 1, [8'h01:8'h7F] :/ 1, [8'h81:8'hFE] :/ 1}`
    נותן לכל ערך קצה 1/5. התא הנדיר עולה ל-1/125, והתוחלת יורדת פי 2,600.

    <!-- gen 3 -->

    | הגירוי | התא הנדיר ביותר | תוחלת הטרנזקציות עד שכל ה-cross מכוסה |
    |---|:-:|:-:|
    | אחיד (‏`randomize` רגיל) | ‏1/327680 | ‏1,393,801 |
    | ‏`dist` : כל ערך קצה 1/5, השאר 2/5 | ‏1/125 | ‏534 |
    | ‏`dist` : כל מחלקה 1/4 | ‏1/80 | ‏389 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ההסתברות של כל תא :** ‏\( \frac15 P(a \in X) P(b \in Y) \); תאים מושמטים לא נאספים.
    2. **האינטגרל :** ‏\( E = \int_0^\infty (1 - \prod_i (1 - e^{-p_i t})) dt \), בחישוב מספרי
       על ציר זמן לוגריתמי.
    3. **ההשוואה :** אותו חישוב לכל `dist`, והתא הנדיר אומר כמה זמן זה ייקח.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="cell_probs, expected_closure" linenums="1" hl_lines="7 18 19"
        import math


        def cell_probs(p_bin: dict) -> list[float]:
            """The probability of every counted cell; p_bin[c] is P(an operand is in bin c)."""
            bins = ("zero", "max", "msb", "mid")
            return [p_bin[x] * p_bin[y] / len(OPS) for op in OPS for x in bins for y in bins if not ignored(op, y)]   # (1)!


        def expected_closure(p: list[float], steps: int = 20000) -> float:
            """E[transactions until every cell is hit]: the integral of 1 - prod(1 - exp(-p t))."""
            lo, hi = 1e-3, (60 + math.log(len(p))) / min(p)
            du = (math.log(hi) - math.log(lo)) / steps
            e, prev = lo, 1.0                                    # the integrand is 1 near 0
            for k in range(1, steps + 1):
                t = lo * math.exp(k * du)
                f = 1 - math.prod(1 - math.exp(-pi * t) for pi in p)
                e += 0.5 * (prev * t * math.exp(-du) + f * t) * du   # (2)!
                prev = f
            return e
        ```

        1. כל תא שאינו מושמט : פעולה (1/5), מחלקה של `a` ומחלקה של `b`.
        2. טרפז על \( u = \ln t \).

    === "SystemVerilog"
        ```systemverilog title="expected_closure" linenums="1" hl_lines="10 13"
        // E[transactions until every cell is hit], p[] the probability of each cell:
        // the integral of 1 - prod(1 - exp(-p t)), on a logarithmic grid of t
        function automatic real expected_closure(real p[$]);
          real pmin = p[0], lo, hi, du, e, t, f, prev = 1.0, prod;
          int  steps = 20000;
          foreach (p[i]) if (p[i] < pmin) pmin = p[i];
          lo = 1e-3; hi = (60.0 + $ln(p.size())) / pmin;
          du = ($ln(hi) - $ln(lo)) / steps;
          e = lo;                                                  // the integrand is 1 near 0
          for (int k = 1; k <= steps; k++) begin
            t = lo * $exp(k * du);
            prod = 1.0;
            foreach (p[i]) prod *= 1.0 - $exp(-p[i] * t);          // (1)!
            f = 1.0 - prod;
            e += 0.5 * (prev * t * $exp(-du) + f * t) * du;        // (2)!
            prev = f;
          end
          return e;
        endfunction
        ```

        1. ההסתברות שכל התאים כבר נפגעו עד הזמן \( t \) (בתהליך פואסון).
        2. טרפז על \( u = \ln t \) : ‏\( dt = t \, du \).

    #### למה זה נכון { .sol-proof }

    **האינטגרל.** אם הטרנזקציות מגיעות כתהליך פואסון בקצב 1, תא \( i \) נפגע עד הזמן \( t \)
    בהסתברות \( 1 - e^{-p_i t} \), והתאים בלתי תלויים. לכן
    \( P(\text{closed by } t) = \prod_i (1 - e^{-p_i t}) \), והתוחלת היא האינטגרל של המשלים.
    מספר הטרנזקציות עד אותו רגע הוא בתוחלת אותו מספר (משפט וולד), ולכן זו גם התוחלת בבדיד.

    **בדיקה מדויקת.** התאים מתחלקים לשלוש קבוצות שוות הסתברות (שני ערכי קצה, אחד, אף אחד),
    ולכן אפשר לחשב את התוחלת בדיוק בהכלה והדחה על הקבוצות, בשברים. הטבלה למעלה חושבה כך,
    והטסטים משווים לאינטגרל של הקוד; ל-1/4 לכל מחלקה, ‏\( 80 H_{72} = 388.86 \).

    **נסו בעצמכם.** בוחרים גירוי (אחיד, `dist`, או טרנזקציה ביד) ושולחים 100, ‏1,000 או 10,000
    טרנזקציות, או "עד הסגירה". המפה של ה-cross מתמלאת, העמודות של ה-coverpoints מתמלאות,
    והגרף מראה את הכיסוי כפונקציה של מספר הטרנזקציות. המתג "לספור את התאים המושמטים" מראה
    למה כיסוי בלי `ignore_bins` לא מגיע ל-100% :

    <div class="explorer" data-kind="covergroup"></div>

    #### סיבוכיות { .sol-cost }

    האינטגרל עולה \( O(\text{cells} \cdot \text{steps}) \) : ‏72 תאים כפול 20,000 צעדים. החישוב
    המדויק בהכלה והדחה עולה \( O(\prod_g (n_g + 1)) \), כאן \( 40 \cdot 29 \cdot 6 \) איברים.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : ‏bins אוטומטיים"
    ‏`coverpoint a;` בלי bins נותן עד 64 bins של טווחים שווים. 100% עליהם לא אומר שראיתם
    0x80, ו-cross שלהם עם 5 פעולות הוא אלפי תאים שאף אחד לא יקרא.

??? trap "מלכודת : ‏illegal_bins לתא לגיטימי"
    מי שמסמן "`SHL` ב-0xFF" כ-illegal יקבל שגיאה בכל פעם שהגירוי מייצר אותו, אף שה-DUT מטפל
    בו נכון. ‏ignore_bins אומר "לא מעניין", illegal_bins אומר "באג".

??? trap "מלכודת : ‏get_coverage במקום get_inst_coverage"
    ‏`get_coverage()` הוא הכיסוי של הסוג, על כל המופעים. כש-covergroup מופיע בכל agent, המספר
    שלו לא אומר כלום על agent אחד.

??? trap "מלכודת : לסגור כיסוי עם seed"
    "הרצתי seed שהגיע ל-100%" לא אומר שה-regression יגיע. אם התא הנדיר הוא 1 ל-327,680, רוב
    ה-seeds לא יגיעו אליו. ‏`dist` או טסט מכוון סוגרים אותו בכל הרצה.

??? followup "שאלות המשך"
    - **‏transition bins :** איך בודקים ש-`ADD` הגיע מיד אחרי `SUB`?

        ??? fu-answer "תשובה"
            ‏`bins sub_add = (SUB => ADD);` ב-coverpoint של `op`. רצף ארוך יותר : ‏`(SUB => ADD => SHL)`, וחזרות :
            ‏`(ADD [*3])`.

    - **משקל :** ה-cross חשוב יותר מה-coverpoints. איך זה משפיע על המספר?

        ??? fu-answer "תשובה"
            ‏`option.weight` לכל coverpoint ו-cross. עם `option.weight = 0` על ה-coverpoints, הכיסוי הוא רק
            של ה-cross. ‏`type_option.weight` לסוג.

    - **‏at_least :** ‏bin נחשב מכוסה אחרי פגיעה אחת. מה אם רוצים 10?

        ??? fu-answer "תשובה"
            ‏`option.at_least = 10`. בבעיית הקופונים זה מכפיל את הזמן בערך פי 10 לתא הנדיר, כמו בסעיף ב
            של שאלה 0041.

    - **‏cross עם תנאי :** איך סופרים `carry` רק עבור `ADD` עם `a = 0xFF`?

        ??? fu-answer "תשובה"
            ‏cross של `cp_op`, ‏`cp_a` ו-`cp_carry` עם `ignore_bins` לכל השאר, או `bins` מפורשים ב-cross :
            ‏`bins add_ff_c = binsof(cp_op.add) && binsof(cp_a.max) && binsof(cp_carry) intersect {1};`.
