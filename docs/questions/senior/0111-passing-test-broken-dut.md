---
id: 111
title: הטסט עובר וה-DUT שבור – שלושה באגים בסביבת הבדיקה
level: senior
difficulty: medium
kind: dv
tags: [debug, scoreboard, sva, coverage, systemverilog, python]
source: "שאלת ראיון לתפקידי אימות (סביבה שעוברת על DUT שבור)"
added: 2026-11-20
---

## השאלה

ה-DUT הוא register slice : שלב צינור של מקום אחד בין שני ממשקי valid/ready. פריט עובר
בקצה השעון שבו `valid` ו-`ready` גבוהים יחד, והכלל של הממשק הוא שפריט שמחכה ביציאה
(`out_valid` גבוה ו-`out_ready` נמוך) נשאר במקום ולא משתנה עד שהוא עובר. האיפוס אסינכרוני
ופעיל בנמוך :

```systemverilog title="module reg_slice" linenums="1"
module reg_slice #(parameter int W = 8) (
  input  logic         clk,
  input  logic         rst_n,
  input  logic         in_valid,
  output logic         in_ready,
  input  logic [W-1:0] in_data,
  output logic         out_valid,
  input  logic         out_ready,
  output logic [W-1:0] out_data
);
  logic         full_q, out_ready_q;
  logic [W-1:0] data_q;

  assign out_valid = full_q;
  assign out_data  = data_q;
  assign in_ready  = !full_q || out_ready_q;   // registered: no path from out_ready to in_ready

  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) begin
      full_q      <= 1'b0;
      data_q      <= '0;
      out_ready_q <= 1'b0;
    end else begin
      out_ready_q <= out_ready;
      if (in_valid && in_ready) begin      // a new item, into an empty slice or behind one that leaves
        full_q <= 1'b1;
        data_q <= in_data;
      end else if (out_ready) begin
        full_q <= 1'b0;
      end
    end
endmodule
```

וזו סביבת הבדיקה שלו. היא מריצה 40 מחזורים : שניים של איפוס, 32 של תנועה אקראית מ-LFSR
של 16 ביט, ו-6 אחרונים שרק מרוקנים את ה-slice. יש בה שני בודקים, כלל ה-handshake
כ-assertion ו-scoreboard, וסיכום בסוף :

```systemverilog title="module slice_tb" linenums="1"
module slice_tb #(
  parameter bit          BACKPRESSURE = 0,     // random stalls on out_ready
  parameter logic [15:0] SEED         = 187
);
  localparam int CYCLES = 40;
  logic       clk = 0, rst_n = 0, in_valid = 0, out_ready = 1, took = 0;
  logic [7:0] in_data = 0, out_data;
  logic       in_ready, out_valid;
  int         cycle, errors = 0, n_in = 0, n_out = 0;
  string      first = "";
  event       eot;                             // the end of the test

  reg_slice dut (.*);
  always #5 clk = ~clk;

  function automatic void error(string msg);
    if (errors++ == 0) first = $sformatf("cycle %0d: %s", cycle, msg);
    $display("ERROR at cycle %0d: %s", cycle, msg);
  endfunction

  // ---- stimulus: a 16-bit LFSR, four steps a cycle
  logic [15:0] lfsr = SEED;
  always @(posedge clk) took <= in_valid && in_ready;
  initial begin
    for (cycle = 0; cycle < CYCLES; cycle++) begin
      if (took) in_valid = 0;                    // the item went in at the last edge
      rst_n     = cycle >= 2;
      out_ready = 1;
      if (rst_n && cycle < CYCLES - 6) begin     // the last 6 cycles only drain
        repeat (4) lfsr = {lfsr[14:0], lfsr[15] ^ lfsr[13] ^ lfsr[12] ^ lfsr[10]};
        if (!in_valid && lfsr[1:0] != 0) begin   // a new item, 3 times in 4
          in_valid = 1;
          in_data++;
        end
        if (BACKPRESSURE) out_ready = lfsr[3:2] != 0;   // a stall, 1 time in 4
      end
      @(negedge clk);
    end
    -> eot;
    #1 $display("TEST %s: %0d in, %0d out, %0d errors", errors ? "FAILED" : "PASSED", n_in, n_out, errors);
    if (errors) $display("first error: %s", first);
    $finish;
  end

  // ---- handshake rule: a waiting item stays put
  a_hold: assert property (@(posedge clk) disable iff (rst_n)
      out_valid && !out_ready |=> out_valid && $stable(out_data))
    else error("a_hold: out_data changed while out_ready was low");

  // ---- scoreboard: written for a block that may reorder, so it searches
  logic [7:0] expected[$];
  always @(posedge clk) if (rst_n) begin
    int at[$];
    if (out_valid && out_ready) begin
      n_out++;
      at = expected.find_first_index(x) with (x == out_data);
      if (at.size() == 0) error($sformatf("scoreboard: unexpected item %0d", out_data));
      else expected.delete(at[0]);
    end
    if (in_valid && in_ready) begin
      n_in++;
      expected.push_back(in_data);
    end
  end
endmodule
```

ה-regression מריץ את `slice_tb` עם ערכי ברירת המחדל ומדפיס
`TEST PASSED: 24 in, 24 out, 0 errors`. צוות האינטגרציה מדווח שכשהצד המקבל עוצר
(backpressure), פריטים נעלמים. ב-DUT יש באג אחד. בסביבה יש שלושה, וכל אחד מהם מסתיר את
הבאג של ה-DUT בדרך אחרת.

- **סעיף א – הטסט עובר :** למה הטסט עובר? מה הגירוי לא עושה אף פעם, ואיך הייתם יודעים את
  זה בלי לקרוא את הקוד? תקנו כך שהמקרה יקרה, ושהטסט ייכשל אם הוא לא קרה. מה מדפיס הטסט
  אחרי התיקון?
- **סעיף ב – ה-assertion :** ‏`a_hold` היה אמור לתפוס את הבאג. למה הוא שותק גם אחרי התיקון
  של סעיף א? תקנו, והוסיפו את מה שהיה מראה שהוא שותק.
- **סעיף ג – ה-scoreboard :** גם בלי ה-assertion, ה-scoreboard היה צריך לתפוס פריט שנעלם.
  למה הוא לא מתלונן? תקנו.
- **סעיף ד – הבאג ב-DUT :** עם הסביבה המתוקנת הטסט נכשל (הלוג ודיאגרמת התזמון בסעיף). מצאו
  את השורה ב-RTL ותקנו אותה.

??? interviewer "מה המראיין בודק"
    - **טסט שעבר הוא טענה :** האם המועמד שואל מה הטסט בדק בפועל, ולא רק אם הוא עבר : כיסוי
      של הגירוי, assertions שבדקו משהו, ובדיקות של מה שלא קרה.
    - **שלושה סוגים של שקט :** גירוי שלא מגיע למקרה, בודק מנוטרל, ובודק שמסתכל רק על מה
      שיצא. לכל אחד תיקון אחר, ולכל אחד בדיקה שמראה אותו בפעם הבאה.
    - **מהשגיאה לשורה ב-RTL :** האם הוא קורא את דיאגרמת התזמון אחורה, מהמחזור של השגיאה
      לקצה השעון שבו הנתון התחלף, ומשם לביטוי של `in_ready`.
    - **תיקון שלא שובר :** האם הוא מבין למה ה-ready נלקח מרגיסטר (תזמון), ויודע איך עושים
      את זה נכון.

---

### סעיף א – הטסט עובר

??? tip "רמז 1"
    מה הערך של `out_ready` בכל מחזור כשהטסט רץ עם ערכי ברירת המחדל? ובאיזה מצב ה-slice
    צריך בכלל להחזיק פריט?

??? tip "רמז 2"
    ‏cover על `out_valid && !out_ready` היה מראה 0. מה צריך כדי ש-0 כזה יכשיל את הטסט, ולא
    רק יופיע בדוח שאף אחד לא קורא?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏`BACKPRESSURE` הוא 0 כברירת מחדל, ולכן `out_ready` תמיד 1 : אף פריט לא מחכה ביציאה,
        ומה ש-`a_hold` וה-scoreboard אמורים לבדוק לא קורה. התיקון : עצירות אקראיות כברירת
        מחדל (`BACKPRESSURE = 1`), ו-cover על `out_valid && !out_ready` שמכשיל את הטסט אם לא
        היו לו פגיעות. אחרי התיקון הבאג קורה והטסט עדיין עובר :
        `TEST PASSED: 21 in, 20 out, 0 errors`.

    #### הרעיון { .sol-idea }

    טסט שעבר אומר רק שאף בודק לא התלונן. כש-`out_ready` תמיד 1, ה-slice מעביר כל פריט בקצה
    שאחרי שהוא נכנס, והמצב שבו פריט מחכה לא קורה אף פעם. הלוגיקה שמחזיקה פריט, וזה בדיוק
    המקום של הבאג, לא רצה בכלל. יותר מזה : כש-`out_ready` תמיד 1, הביטוי הבעייתי של
    `in_ready` נותן בכל מחזור את אותו ערך כמו הביטוי הנכון (סעיף ד), ולכן הטסט הזה לא יכול
    להבדיל בין ה-DUT השבור למתוקן : שניהם מדפיסים `24 in, 24 out`.

    איך יודעים את זה בלי לקרוא את הגירוי? כיסוי. ‏cover על המצב "פריט מחכה" היה מראה 0
    פגיעות. אבל מספר בדוח שאף אחד לא קורא לא עוזר : הכיסוי צריך להיות **יעד**, ו-0 פגיעות
    בסוף הטסט הוא שגיאה כמו כל שגיאה אחרת.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הגירוי :** ‏`BACKPRESSURE = 1` כברירת מחדל. ה-knob נשאר להרצות של bring-up, אבל
       ה-regression לא יכול לשכוח להדליק אותו. ‏`out_ready` יורד פעם בארבעה מחזורים
       (ביטים 3 ו-2 של ה-LFSR).
    2. **הכיסוי :** ‏`c_stall` סופר את המחזורים שבהם פריט מחכה ביציאה.
    3. **היעד :** בסוף הטסט, 0 פגיעות הוא שגיאה.
    4. **הלוג :** קוראים את המספרים ולא רק את המילה PASSED.

    </div>

    #### הקוד { .sol-code }

    החלק החדש נכנס אחרי הגירוי, וברירת המחדל בראש המודול הופכת ל-`BACKPRESSURE = 1` :

    ```systemverilog title="slice_tb: coverage" linenums="1" hl_lines="3 4"
    // ---- coverage: the test fails if the stimulus never reached the case
    int stalls = 0;
    c_stall: cover property (@(posedge clk) disable iff (!rst_n) out_valid && !out_ready) stalls++;   // (1)!
    always @(eot) if (stalls == 0) error("c_stall: no cycle with out_valid && !out_ready");          // (2)!
    ```

    1. ‏Verilator 5.053 מריץ את בלוק הפעולה של `cover property` רק כשהסביבה נבנית עם
       `--coverage-user`. בלי הדגל המונה נשאר 0 והטסט נכשל ב-`c_stall` : כישלון רועש, לא
       מעבר שקט. הטסטים של השאלה בונים עם הדגל.
    2. ‏`eot` הוא האירוע של סוף הטסט, אחרי ששת מחזורי הניקוז. הבדיקה רצה לפני שורת הסיכום.

    #### למה זה נכון { .sol-proof }

    - **לפני התיקון :** ההשמה היחידה של 0 ל-`out_ready` נמצאת תחת `if (BACKPRESSURE)`.
      עם 0 היא לא רצה, `out_valid && !out_ready` לא מתקיים באף מחזור, ו-`c_stall` היה מראה
      0 פגיעות.
    - **אחרי התיקון :** עם ערך האתחול 187 יש 6 מחזורים שבהם פריט מחכה : 3, 11, 14, 27, 31
      ו-32, והיעד מתקיים.
    - **למה הטסט עדיין עובר :** במחזור 11 פריט 5 מחכה ביציאה, `out_ready` יורד, ופריט 6 נכנס
      ודורס אותו. ‏`a_hold` מנוטרל (סעיף ב) וה-scoreboard משאיר את פריט 5 ברשימה בלי לומר
      כלום (סעיף ג). הלוג אומר `21 in, 20 out` : בטסט שששת המחזורים האחרונים שלו מרוקנים את
      ה-slice, פער בין הכניסות ליציאות הוא כבר כישלון, אבל אף בודק לא משווה אותם.

---

### סעיף ב – ה-assertion

??? tip "רמז 1"
    מתי `disable iff` מנטרל את ה-property? ומה הערך של `rst_n` בזמן שהטסט רץ?

??? tip "רמז 2"
    ‏assertion עובר גם כשהוא מנוטרל, וגם כשה-antecedent שלו לא מתקיים אף פעם. איזה cover היה
    מראה ש-`a_hold` לא בדק אף מחזור?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏`disable iff (rst_n)` מנטרל את `a_hold` כל עוד `rst_n` גבוה, כלומר בכל הטסט חוץ
        משני מחזורי האיפוס, ובהם `out_valid` נמוך. הוא עובר בלי לבדוק אף מחזור. התיקון :
        `disable iff (!rst_n)`, ולצדו cover של ה-antecedent עם יעד. עם התיקונים של א ו-ב
        הטסט נכשל : ‏`a_hold` מדווח במחזור 12 ש-`out_data` השתנה בזמן ש-`out_ready` נמוך.

    #### הרעיון { .sol-idea }

    האיפוס פעיל בנמוך, ולכן "לא לבדוק בזמן איפוס" הוא `disable iff (!rst_n)`. הקוד כתוב
    הפוך : הוא לא בודק **מחוץ** לאיפוס. ‏assertion כזה לא נכשל אף פעם, וזה בדיוק מה שנראה
    כמו הצלחה.

    יש שתי דרכים ל-assertion לעבור בלי לבדוק כלום : הוא מנוטרל, או שה-antecedent שלו לא
    מתקיים (סעיף א). התרופה לשתיהן זהה : **cover של ה-antecedent**, באותו שעון ובאותו
    `disable iff`. הוא סופר בדיוק את הניסיונות שבודקים משהו, ו-0 בסוף הטסט הוא שגיאה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **לקרוא את התנאי כמשפט :** "לנטרל כש-`rst_n` גבוה" הוא ההפך מהכוונה.
    2. **להפוך את הקוטביות :** ‏`disable iff (!rst_n)`.
    3. **לצרף cover :** ‏`c_hold` על אותו antecedent, אותו שעון ואותו `disable iff`.
    4. **יעד :** בסוף הטסט, 0 פגיעות של `c_hold` הוא שגיאה.

    </div>

    #### הקוד { .sol-code }

    ```systemverilog title="slice_tb: handshake rule" linenums="1" hl_lines="2 6 7"
    // ---- handshake rule: a waiting item stays put
    a_hold: assert property (@(posedge clk) disable iff (!rst_n)          // (1)!
        out_valid && !out_ready |=> out_valid && $stable(out_data))
      else error("a_hold: out_data changed while out_ready was low");
    int holds = 0;
    c_hold: cover property (@(posedge clk) disable iff (!rst_n) out_valid && !out_ready) holds++;   // (2)!
    always @(eot) if (holds == 0) error("c_hold: a_hold never checked anything");
    ```

    1. ‏Verilator 5.053 מריץ את ה-property כמו שהוא כתוב : `disable iff`, ‏`|=>` ו-`$stable`
       נתמכים, והשגיאה מגיעה מבלוק ה-`else`.
    2. אותו ביטוי כמו `c_stall` של סעיף א, אבל תפקיד אחר : `c_stall` שואל אם הגירוי יצר את
       המקרה, ו-`c_hold` שייך ל-assertion ושואל אם הוא בדק משהו. כשה-antecedent הוא sequence
       ארוך יותר, השניים כבר לא זהים.

    #### למה זה נכון { .sol-proof }

    - **לפני התיקון :** במחזורים 0 ו-1 ‏`rst_n` נמוך, ה-property פעיל, אבל ה-DUT באיפוס
      ו-`out_valid` נמוך : ה-antecedent לא מתקיים. ממחזור 2 עד הסוף `rst_n` גבוה וה-property
      מנוטרל. אין אף ניסיון שבודק משהו, ולכן אין אף כישלון.
    - **אחרי התיקון :** ‏`c_hold` מראה 6 פגיעות, ו-`a_hold` בודק 6 ניסיונות. הניסיון של מחזור
      11 (`out_data` הוא 5 ו-`out_ready` נמוך) נכשל במחזור 12, כי שם `out_data` הוא 6.
    - **ה-cover תופס גם את הבאג של סעיף א :** עם ה-assertion המתוקן אבל בלי עצירות, ‏`c_hold`
      נשאר 0 והטסט נכשל בסוף : `ERROR at cycle 40: c_hold: a_hold never checked anything`.

---

### סעיף ג – ה-scoreboard

??? tip "רמז 1"
    פריט שנכנס ולא יצא : באיזו שורה של ה-scoreboard הוא מטופל?

??? tip "רמז 2"
    ‏scoreboard שמחפש ומוחק מגיב רק לפריט שיוצא. מה בודקים כשהטסט נגמר? ומה בודקים על פריט
    שמחכה יותר מדי זמן?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ה-scoreboard מגיב רק לפריט שיוצא : מחפש אותו ומוחק. פריט שנעלם לא יוצא, ולכן הוא נשאר
        ברשימה, ואף שורה לא מסתכלת על הרשימה. התיקון : לכל פריט זמן כניסה, שגיאה על פריט
        שמחכה כבר `MAX_WAIT = 10` מחזורים, ובסוף הטסט כל פריט שנשאר ברשימה הוא שגיאה. בלי
        ה-assertion (התיקונים של א ו-ג) ה-scoreboard מדווח על פריט 5 פעמיים : במחזור 20
        (`still waiting after 10 cycles`) ובסוף הטסט (`never came out`).

    #### הרעיון { .sol-idea }

    השוואה בכל פריט שיוצא לא יכולה לראות פריט שלא יצא. "מה שלא קרה" צריך **זמן** : מגבלה
    על ההמתנה של כל פריט, ובדיקה בסוף הטסט שהרשימה ריקה. הבדיקה בסוף נכונה רק אחרי
    שה-DUT התרוקן, ולכן הסביבה מפסיקה לשלוח פריטים 6 מחזורים לפני הסוף.

    החיפוש עצמו נשאר : הוא נכתב לבלוק שמותר לו לשנות סדר. ה-slice לא אמור לשנות סדר, ולכן
    השוואה לפי הסדר הייתה תופסת יותר מוקדם (שאלות ההמשך).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **זמן כניסה :** כל פריט נשמר ברשימה עם המחזור שבו נכנס.
    2. **יציאה :** חיפוש ומחיקה, כמו קודם.
    3. **מגבלת המתנה :** בכל קצה, פריט שמחכה כבר `MAX_WAIT` מחזורים ועוד ברשימה מדווח פעם
       אחת.
    4. **סוף הטסט :** אחרי הניקוז, כל פריט שנשאר ברשימה הוא שגיאה.

    </div>

    #### הקוד { .sol-code }

    ```systemverilog title="slice_tb: scoreboard" linenums="1" hl_lines="3 15 17 18 21"
    // ---- scoreboard: still a search, now with a wait bound and an end check
    localparam int MAX_WAIT = 10;
    typedef struct { logic [7:0] data; int since; } item_t;
    item_t expected[$];
    always @(posedge clk) if (rst_n) begin
      int at[$];
      if (out_valid && out_ready) begin
        n_out++;
        at = expected.find_first_index(x) with (x.data == out_data);
        if (at.size() == 0) error($sformatf("scoreboard: unexpected item %0d", out_data));
        else expected.delete(at[0]);
      end
      if (in_valid && in_ready) begin
        n_in++;
        expected.push_back('{in_data, cycle});
      end
      foreach (expected[i])                      // (1)!
        if (cycle - expected[i].since == MAX_WAIT)
          error($sformatf("scoreboard: item %0d still waiting after %0d cycles", expected[i].data, MAX_WAIT));
    end
    always @(eot) foreach (expected[i]) error($sformatf("scoreboard: item %0d never came out", expected[i].data));
    ```

    1. הבדיקה רצה אחרי היציאה של אותו קצה : פריט שיוצא בדיוק אחרי `MAX_WAIT` מחזורים כבר
       נמחק. השוויון (ולא `>=`) מדווח על כל פריט פעם אחת.

    #### למה זה נכון { .sol-proof }

    - **הפריט שנעלם :** פריט 5 נכנס בקצה של מחזור 10, ובקצה של מחזור 11 פריט 6 דורס אותו.
      הוא לא מופיע ביציאה אף פעם, ולכן נשאר ברשימה. במחזור 20, עשרה מחזורים אחרי שנכנס, הוא
      עוד שם : שגיאה. בסוף הטסט הוא עדיין שם : עוד שגיאה.
    - **בלי אזעקות שווא :** עם ה-DUT המתוקן פריט מחכה ב-slice רק כל עוד `out_ready` נמוך. בכל
      65,535 ערכי האתחול של ה-LFSR ההמתנה הארוכה ביותר היא 8 מחזורים, ולכן מגבלה של 10 לא
      נפגעת על DUT תקין. בדיקת הסוף לא נפגעת כי ששת מחזורי הניקוז מוציאים כל פריט.

---

### סעיף ד – הבאג ב-DUT

עם שלושת התיקונים, ערך האתחול 187 נותן את הלוג הזה :

<!-- gen 0 -->

```text
ERROR at cycle 12: a_hold: out_data changed while out_ready was low
ERROR at cycle 20: scoreboard: item 5 still waiting after 10 cycles
ERROR at cycle 40: scoreboard: item 5 never came out
TEST FAILED: 21 in, 20 out, 3 errors
first error: cycle 12: a_hold: out_data changed while out_ready was low
```

<!-- /gen -->

ודיאגרמת התזמון של המחזורים 8 עד 14, מה-dump של אותה ריצה. כל עמודה היא מחזור, עם הערכים
שהקצה בסופו דוגם, ו-`full_q` הוא גם `out_valid` :

<!-- gen 1 -->

```wavedrom
{ signal: [
  { name: "clk",         wave: "p......" },
  { name: "cycle",       wave: "=======", data: ["8", "9", "10", "11", "12", "13", "14"] },
  { name: "in_valid",    wave: "01....0" },
  { name: "in_ready",    wave: "1...01." },
  { name: "in_data",     wave: "=====..", data: ["3", "4", "5", "6", "7"] },
  { name: "full_q",      wave: "101..01" },
  { name: "out_ready",   wave: "1..01.0" },
  { name: "out_data",    wave: "=.===.=", data: ["3", "4", "5", "6", "7"] },
  { name: "out_ready_q", wave: "1...01." }
]}
```

<!-- /gen -->

מצאו את השורה ב-RTL שגורמת לשגיאה, ותקנו אותה.

??? tip "רמז 1"
    ‏`a_hold` נכשל במחזור 12, ולכן הניסיון התחיל במחזור 11. איזה ענף של ה-`always_ff` כותב
    ל-`data_q`, ומה התנאי שלו?

??? tip "רמז 2"
    במחזור 11 ‏`in_ready` גבוה, למרות ש-`full_q` גבוה ו-`out_ready` נמוך. מאיפה הוא מקבל את
    ה-1?

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        ‏`in_ready` מחושב מ-`out_ready_q`, הערך של `out_ready` במחזור הקודם. במחזור הראשון של
        עצירה `out_ready` כבר ירד, `out_ready_q` עוד 1, וה-slice המלא מקבל פריט חדש שדורס את
        הפריט שמחכה. התיקון : `assign in_ready = !full_q || out_ready;`, והרגיסטר
        `out_ready_q` יוצא. עם ארבעת התיקונים : `TEST PASSED: 23 in, 23 out, 0 errors`.

    #### הרעיון { .sol-idea }

    קוראים את הדיאגרמה אחורה מהשגיאה. ‏`a_hold` נכשל במחזור 12, ולכן ה-antecedent התקיים
    במחזור 11 : פריט 5 חיכה ביציאה. במחזור 12 ‏`out_data` הוא 6, כלומר `data_q` התחלף בקצה
    של מחזור 11. רק ענף אחד כותב ל-`data_q`, ‏`in_valid && in_ready`, ולכן `in_ready` היה 1
    כש-`full_q` היה 1. לפי הביטוי, זה אומר `out_ready_q = 1`, בזמן ש-`out_ready` עצמו 0.

    מי שכתב את ה-RTL רצה לחתוך את המסלול הצירופי מ-`out_ready` ל-`in_ready` (תזמון). ב-slice
    של מקום אחד אי אפשר : כשהוא מלא, השאלה אם יש מקום לפריט חדש היא בדיוק השאלה אם הפריט
    הנוכחי יוצא **במחזור הזה**, ואת זה אומר רק `out_ready` של המחזור הזה. הדרך הנכונה לרגיסטר
    את ה-ready היא skid buffer של שני מקומות (שאלות ההמשך).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מהשגיאה לקצה :** ‏`a_hold` נכשל במחזור 12, וה-antecedent של מחזור 11 נכון. הנתון
       התחלף בקצה של מחזור 11.
    2. **מהקצה לענף :** רק `in_valid && in_ready` כותב ל-`data_q`, ולכן `in_ready` היה 1
       במחזור 11.
    3. **מהענף לביטוי :** ‏`full_q` היה 1, ולכן `out_ready_q` היה 1 : הערך של `out_ready`
       ממחזור 10.
    4. **התיקון :** ‏`in_ready` מ-`out_ready` של אותו מחזור, והרגיסטר יוצא.
    5. **להריץ שוב :** כל הבודקים, והטסט עובר.

    </div>

    #### הקוד { .sol-code }

    ```systemverilog title="module reg_slice (fixed)" linenums="1" hl_lines="11 16"
    module reg_slice #(parameter int W = 8) (
      input  logic         clk,
      input  logic         rst_n,
      input  logic         in_valid,
      output logic         in_ready,
      input  logic [W-1:0] in_data,
      output logic         out_valid,
      input  logic         out_ready,
      output logic [W-1:0] out_data
    );
      logic         full_q;
      logic [W-1:0] data_q;

      assign out_valid = full_q;
      assign out_data  = data_q;
      assign in_ready  = !full_q || out_ready;     // room now, or the item leaves at this edge

      always_ff @(posedge clk or negedge rst_n)
        if (!rst_n) begin
          full_q <= 1'b0;
          data_q <= '0;
        end else if (in_valid && in_ready) begin
          full_q <= 1'b1;
          data_q <= in_data;
        end else if (out_ready) begin
          full_q <= 1'b0;
        end
    endmodule
    ```

    המודל של הריצה כולה בפייתון, מחזור אחרי מחזור, עם ארבעת התיקונים כמתגים. התיבה שבסוף
    הסעיף מריצה את אותו מודל ב-JavaScript, והטסטים של השאלה משווים את שניהם ל-Verilator
    בכל 16 הצירופים :

    ```python title="run_bench" linenums="1" hl_lines="28 33 35 39 48 67"
    CYCLES, RESET, DRAIN, MAX_WAIT = 40, 2, 6, 10


    def lfsr_step(s: int) -> int:
        """x^16 + x^14 + x^13 + x^11 + 1: the bench's shift."""
        bit = ((s >> 15) ^ (s >> 13) ^ (s >> 12) ^ (s >> 10)) & 1
        return ((s << 1) | bit) & 0xFFFF


    def run_bench(seed, backpressure, assert_fixed, sb_fixed, dut_fixed):
        """One run of slice_tb; the four fixes are flags. Errors are (cycle, checker, item)."""
        lfsr, in_valid, in_data, took = seed, 0, 0, 0
        full = data = rq = 0                       # full_q, data_q, out_ready_q
        expected, errors, rows = [], [], []        # expected: (item, the cycle it went in)
        stalls = holds = checked = n_in = n_out = 0
        prev = None
        for t in range(CYCLES):
            if took:                               # the driver, between two edges
                in_valid = 0
            rst_n, out_ready = int(t >= RESET), 1
            if rst_n and t < CYCLES - DRAIN:
                for _ in range(4):
                    lfsr = lfsr_step(lfsr)
                if not in_valid and lfsr & 3:
                    in_valid, in_data = 1, in_data + 1
                if backpressure:
                    out_ready = int((lfsr >> 2) & 3 != 0)
            in_ready = int(not full or (out_ready if dut_fixed else rq))
            row = dict(t=t, rst_n=rst_n, in_valid=in_valid, in_ready=in_ready, in_data=in_data,
                       out_valid=full, out_ready=out_ready, out_data=data, full_q=full, out_ready_q=rq)
            rows.append(row)
            if rst_n:                              # the checkers, at the edge that ends cycle t
                if assert_fixed and prev and prev["rst_n"] and prev["out_valid"] and not prev["out_ready"]:
                    checked += 1                   # an attempt of a_hold that checks something
                    if not (full and data == prev["out_data"]):
                        errors.append((t, "a_hold", prev["out_data"]))
                if full and out_ready:
                    n_out += 1
                    at = next((i for i, (d, _) in enumerate(expected) if d == data), None)
                    if at is None:
                        errors.append((t, "unexpected", data))
                    else:
                        expected.pop(at)
                if in_valid and in_ready:
                    n_in += 1
                    expected.append((in_data, t))
                if sb_fixed:
                    errors += [(t, "wait", d) for d, t0 in expected if t - t0 == MAX_WAIT]
                if full and not out_ready:         # c_stall and c_hold, when they exist
                    stalls += backpressure
                    holds += assert_fixed
            took = int(in_valid and in_ready)      # the edge
            if not rst_n:
                full = data = rq = 0
            else:
                if in_valid and in_ready:
                    full, data = 1, in_data
                elif out_ready:
                    full = 0
                rq = out_ready
            prev = row
        if backpressure and stalls == 0:           # the end of the test
            errors.append((CYCLES, "c_stall", 0))
        if assert_fixed and holds == 0:
            errors.append((CYCLES, "c_hold", 0))
        if sb_fixed:
            errors += [(CYCLES, "missing", d) for d, _ in expected]
        return dict(rows=rows, errors=errors, n_in=n_in, n_out=n_out, left=[d for d, _ in expected],
                    stalls=stalls, holds=holds, checked=checked)
    ```

    #### למה זה נכון { .sol-proof }

    **התיקון לא מאבד ולא משכפל.** כשה-slice ריק, `in_ready = 1` והפריט נכנס למקום פנוי.
    כשהוא מלא ו-`out_ready = 1`, הפריט הנוכחי יוצא באותו קצה, ופריט חדש, אם יש, תופס את
    מקומו. כשהוא מלא ו-`out_ready = 0`, ‏`in_ready = 0` ואף ענף לא כותב : `full_q` ו-`data_q`
    נשארים, ו-`a_hold` מתקיים. כל פריט נכנס פעם אחת ויוצא פעם אחת, לפי הסדר.

    **למה הטסט המקורי לא ראה את הבאג.** כש-`out_ready` תמיד 1, ‏`out_ready_q` הוא 1 מהמחזור
    השני אחרי האיפוס, וה-slice מלא רק אחרי שפריט נכנס, כלומר מאוחר יותר. בכל מחזור שבו
    `full_q = 1`, שני הביטויים של `in_ready` שווים, וה-DUT השבור מתנהג בדיוק כמו המתוקן.

    **מתי בדיוק פריט הולך לאיבוד.** כש-`full_q`, ‏`out_ready_q` ו-`in_valid` גבוהים
    ו-`out_ready` נמוך : המחזור הראשון של עצירה, כשפריט חדש מחכה בכניסה. עם ערך האתחול 187
    זה קורה רק במחזור 11, מתוך 6 מחזורי עצירה. בשאר העצירות או שאין פריט בכניסה, או שזה
    כבר המחזור השני של העצירה ו-`out_ready_q` ירד. הבאג עולה גם בתפוקה : כש-`full_q = 1`,
    ‏`out_ready = 1` ו-`out_ready_q = 0` (מחזור 4, למשל), ה-slice מסרב לפריט חדש בלי סיבה.

    **הטבלה.** כל צירוף של התיקונים עם ערך האתחול 187, כמו ש-Verilator מריץ אותו :

    <!-- gen 2 -->

    | א : עצירות ויעד | ב : ה-assertion | ג : ה-scoreboard | ה-DUT השבור | ה-DUT המתוקן |
    |:-:|:-:|:-:|:--|:--|
    | — | — | — | עובר : <span dir="ltr">24 in, 24 out</span> | עובר : <span dir="ltr">24 in, 24 out</span> |
    | — | — | ✓ | עובר : <span dir="ltr">24 in, 24 out</span> | עובר : <span dir="ltr">24 in, 24 out</span> |
    | — | ✓ | — | נכשל : שגיאה של `c_hold` במחזור 40 | נכשל : שגיאה של `c_hold` במחזור 40 |
    | — | ✓ | ✓ | נכשל : שגיאה של `c_hold` במחזור 40 | נכשל : שגיאה של `c_hold` במחזור 40 |
    | ✓ | — | — | עובר : <span dir="ltr">21 in, 20 out</span> | עובר : <span dir="ltr">23 in, 23 out</span> |
    | ✓ | — | ✓ | נכשל : 2 שגיאות, הראשונה של `scoreboard` במחזור 20 | עובר : <span dir="ltr">23 in, 23 out</span> |
    | ✓ | ✓ | — | נכשל : שגיאה של `a_hold` במחזור 12 | עובר : <span dir="ltr">23 in, 23 out</span> |
    | ✓ | ✓ | ✓ | נכשל : 3 שגיאות, הראשונה של `a_hold` במחזור 12 | עובר : <span dir="ltr">23 in, 23 out</span> |

    <!-- /gen -->

    **נסו בעצמכם.** התיבה נפתחת על הסביבה כמו שנמצאה. סמנו את המתג "א : עצירות ויעד" : הבאג
    קורה במחזור 11 (העמודה המסומנת), הרשימה של ה-scoreboard שומרת את פריט 5 עד הסוף, והתוצאה
    עדיין PASSED. הוסיפו את "ב : ה-assertion" ועברו למחזור 12 : ה-✗ של `a_hold`. אחר כך השאירו
    רק את "ב", בלי עצירות : הטסט נכשל בסוף, כי `c_hold` נשאר 0. מעבר לדיאגרמות, התיבה מריצה
    כל ערך אתחול של ה-LFSR וכל צירוף של המתגים, ומראה מחזור אחרי מחזור מה כל בודק ראה :

    <div class="explorer" data-kind="falsepass"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : ״הטסט עבר״ בלי לשאול מה הוא בדק"
    הצלחה היא היעדר תלונות, לא הוכחה. לפני שסוגרים באג או מאשרים RTL, שואלים מה הגירוי
    הגיע אליו (כיסוי עם יעדים), אילו assertions בדקו משהו (cover של כל antecedent), ומה
    בודק את מה שלא קרה (בדיקות סוף והגבלות זמן). ספירות בשורת הסיכום (`21 in, 20 out`)
    הן בדיקה זולה שתופסת הרבה.

??? trap "מלכודת : `disable iff` בקוטביות הלא נכונה"
    איפוס בפעיל נמוך מנטרלים עם `disable iff (!rst_n)`. הטעות לא נראית אף פעם, כי היא לא
    מייצרת כישלונות : רק cover של ה-antecedent, או בדיקה מכוונת של ה-assertion מול DUT שבור,
    חושפים אותה. כדאי להגדיר את תנאי האיפוס פעם אחת (`default disable iff`) ולא בכל property.

??? trap "מלכודת : בדיקת סוף בלי ניקוז"
    בדיקה שהרשימה ריקה בסוף הטסט נכונה רק כשה-DUT סיים את העבודה. בלי ניקוז, פריט שעוד
    בדרך נראה כמו פריט שנעלם, והפתרון המתבקש, "להוריד את הבדיקה", מחזיר את הבאג של סעיף ג.
    מפסיקים לשלוח, מחכים שה-DUT יתרוקן (עם גבול זמן), ורק אז בודקים.

??? trap "מלכודת : לתקן את התזמון בלי לתקן את הפרוטוקול"
    ‏`out_ready_q` נוסף כדי לחתוך מסלול צירופי, וזו סיבה טובה. אבל valid/ready דורש
    שההחלטה לקבל פריט תתאים למקום שיש באמת באותו קצה. רגיסטר על ready דורש מקום נוסף לפריט
    שמגיע במחזור שבו ה-ready הרשום עוד לא ירד (skid buffer).

??? followup "שאלות המשך"
    - **ה-RTL צריך `in_ready` ישירות מרגיסטר, בלי מסלול מ-`out_ready`. איך?**

        ??? fu-answer "תשובה"
            ‏skid buffer : שני מקומות. ‏`in_ready` הוא "המקום השני ריק", ערך של רגיסטר. פריט
            שמגיע במחזור הראשון של עצירה נכנס למקום השני, ו-`in_ready` יורד בקצה הבא. כשהיציאה
            ממשיכה, הפריט מהמקום השני עובר לראשון.

    - **איזה cover היה מצביע ישר על התנאי של הבאג?**

        ??? fu-answer "תשובה"
            ‏`out_valid && !out_ready && in_valid` : פריט מחכה ביציאה ופריט חדש מחכה בכניסה.
            עם ערך האתחול 187 ו-DUT שבור הוא מתקיים רק במחזור 11. ‏cover שלא מגיע למצב
            כזה אומר שהגירוי לא בדק את המקרה שבו slice באמת צריך לסרב.

    - **ה-slice לא משנה סדר. מה היה קורה עם scoreboard שמשווה לפי הסדר?**

        ??? fu-answer "תשובה"
            הוא היה נכשל במחזור 12, באותו מחזור כמו `a_hold` : יוצא פריט 6 והראשון ברשימה
            הוא 5. חיפוש מתאים רק כשהמפרט מתיר שינוי סדר, ועדיף אז סדר לפי ID (שאלה 0050).

    - **מה עוד הופך assertion לריק?**

        ??? fu-answer "תשובה"
            שעון לא נכון, antecedent שלא מתקיים, `$assertoff` שנשאר מה-bring-up, מודול
            checker שלא מחובר (`bind` חסר), או סימולטור שלא מריץ את ה-action. ‏cover של
            ה-antecedent עם יעד תופס את כולם.

    - **למה ששת המחזורים האחרונים לא שולחים פריטים?**

        ??? fu-answer "תשובה"
            כדי שבדיקת הסוף תראה DUT ריק. בלי ניקוז, פריט שנכנס במחזור האחרון עוד יושב
            ב-slice ונספר כחסר. בסביבה אמיתית מחכים לריקון עם גבול זמן, ולא מספר קבוע.
