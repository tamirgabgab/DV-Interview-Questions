---
id: 113
title: הטסט שנגמר בזמן 0
level: junior
difficulty: medium
kind: dv
tags: [uvm, methodology, debug, python, systemverilog]
source: ""
added: 2026-11-20
---

## השאלה

ה-DUT הוא צינור (pipeline) של ארבעה שלבים : כל פריט שנכנס עם `in_valid` יוצא ארבעה מחזורים
אחר כך עם `out_valid`, והנתון שלו גדל ב-1. האיפוס אסינכרוני ופעיל בנמוך :

```systemverilog title="module pipe" linenums="1"
module pipe #(parameter int LAT = 4) (
  input  logic       clk,
  input  logic       rst_n,
  input  logic       in_valid,
  input  logic [7:0] in_data,
  output logic       out_valid,
  output logic [7:0] out_data
);
  logic [LAT-1:0] v;              // a valid bit per stage
  logic [7:0]     d [LAT];        // the data of every stage

  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) v <= '0;
    else        v <= {v[LAT-2:0], in_valid};

  always_ff @(posedge clk) begin
    d[0] <= in_data + 8'd1;
    for (int i = 1; i < LAT; i++) d[i] <= d[i-1];
  end

  assign out_valid = v[LAT-1];
  assign out_data  = d[LAT-1];
endmodule
```

הסביבה היא סביבת UVM רגילה, כמו בשאלה [0049](0049-uvm-testbench-architecture.md) : ‏sequence
ששולחת 8 פריטים, ‏driver שמחזיק את האיפוס שני מחזורים ואז מוסר פריט בכל מחזור, מוניטור כניסה
ומוניטור יציאה שדוגמים בירידת השעון, ו-scoreboard שמשווה ב-`check_phase` את מה שנכנס למה שיצא.
השעון 10 ns, והוא מתחיל בנמוך. הקוד המלא של הסביבה, ב-pyuvm וב-SystemVerilog :

??? info "הסביבה המלאה : פריט, sequence, ‏driver, מוניטורים, scoreboard ו-env"
    === "Python"
        ```python title="pipe_env (pyuvm)" linenums="1"
        import cocotb
        from cocotb.clock import Clock
        from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge, SimTimeoutError, Timer, with_timeout
        from cocotb.utils import get_sim_time
        import pyuvm
        from pyuvm import *

        N = 8                                       # items per test


        class Item(uvm_sequence_item):
            def __init__(self, name="item", data=0):
                super().__init__(name)
                self.data = data


        class ItemSeq(uvm_sequence):
            async def body(self):
                for k in range(N):
                    item = Item("item", data=0x10 + k)
                    await self.start_item(item)
                    await self.finish_item(item)


        class Driver(uvm_driver):
            async def run_phase(self):
                dut = cocotb.top
                dut.rst_n.value = 0
                dut.in_valid.value = 0
                await ClockCycles(dut.clk, 2)           # (1)!
                dut.rst_n.value = 1
                while True:                             # (2)!
                    item = await self.seq_item_port.get_next_item()
                    dut.in_valid.value = 1
                    dut.in_data.value = item.data
                    await RisingEdge(dut.clk)           # the DUT takes the item here
                    dut.in_valid.value = 0
                    self.seq_item_port.item_done()


        class InMonitor(uvm_monitor):
            PINS = ("in_valid", "in_data")

            def build_phase(self):
                self.ap = uvm_analysis_port("ap", self)

            async def run_phase(self):
                valid, data = (getattr(cocotb.top, p) for p in self.PINS)
                while True:
                    await FallingEdge(cocotb.top.clk)   # (3)!
                    if valid.value:
                        self.ap.write(int(data.value))


        class OutMonitor(InMonitor):
            PINS = ("out_valid", "out_data")


        class Scoreboard(uvm_component):
            def build_phase(self):
                self.sent = uvm_tlm_analysis_fifo("sent", self)
                self.seen = uvm_tlm_analysis_fifo("seen", self)

            def check_phase(self):                      # (4)!
                sent, seen = [], []
                for fifo, items in ((self.sent, sent), (self.seen, seen)):
                    while fifo.can_get():
                        items.append(fifo.try_get()[1])
                bad = sum(out != x + 1 for x, out in zip(sent, seen))
                missing = len(sent) - len(seen)
                self.logger.info(f"{get_sim_time('ns'):g} ns: {len(seen)} compared, "
                                 f"{bad} mismatches, {missing} missing")
                if bad or missing:
                    self.logger.error("TEST FAILED")
                else:
                    self.logger.info("TEST PASSED")


        class PipeEnv(uvm_env):
            def build_phase(self):
                self.seqr = uvm_sequencer("seqr", self)
                self.drv = Driver("drv", self)
                self.mon_in = InMonitor("mon_in", self)
                self.mon_out = OutMonitor("mon_out", self)
                self.sb = Scoreboard("sb", self)

            def connect_phase(self):
                self.drv.seq_item_port.connect(self.seqr.seq_item_export)
                self.mon_in.ap.connect(self.sb.sent.analysis_export)
                self.mon_out.ap.connect(self.sb.seen.analysis_export)
        ```

        1. האיפוס : שתי עליות של השעון, ב-5 וב-15 ns. הפריט הראשון נכנס בעלייה של 25 ns.
        2. ‏driver ומוניטור רצים בלולאה אינסופית : הם לא יודעים מתי הטסט נגמר, ולא צריכים לדעת.
        3. דגימה בירידה, באמצע המחזור, כשהאותות כבר יציבים. מוניטור הכניסה רואה את פריט
           ‏\( i \) ב-\( 20 + 10i \) ns, ומוניטור היציאה ב-\( 60 + 10i \) ns.
        4. ההשוואה בסוף : מה שנכנס ועוד 1 מול מה שיצא, לפי הסדר. פריט שנכנס ולא יצא נספר
           כחסר.

    === "SystemVerilog"
        ```systemverilog title="pipe_env (UVM)" linenums="1"
        interface pipe_if (input logic clk);
          logic       rst_n, in_valid, out_valid;
          logic [7:0] in_data, out_data;
        endinterface

        class item extends uvm_sequence_item;
          `uvm_object_utils(item)
          bit [7:0] data;
          function new(string name = "item"); super.new(name); endfunction
        endclass

        class item_seq extends uvm_sequence #(item);
          `uvm_object_utils(item_seq)
          function new(string name = "item_seq"); super.new(name); endfunction
          task body();
            for (int k = 0; k < 8; k++) begin
              item it = item::type_id::create("item");
              start_item(it);
              it.data = 8'h10 + k;
              finish_item(it);
            end
          endtask
        endclass

        class driver extends uvm_driver #(item);
          `uvm_component_utils(driver)
          virtual pipe_if vif;
          function new(string name, uvm_component parent); super.new(name, parent); endfunction
          task run_phase(uvm_phase phase);
            vif.rst_n <= 0;
            vif.in_valid <= 0;
            repeat (2) @(posedge vif.clk);
            vif.rst_n <= 1;
            forever begin
              seq_item_port.get_next_item(req);
              vif.in_valid <= 1;
              vif.in_data <= req.data;
              @(posedge vif.clk);
              vif.in_valid <= 0;
              seq_item_port.item_done();
            end
          endtask
        endclass

        class in_monitor extends uvm_monitor;
          `uvm_component_utils(in_monitor)
          virtual pipe_if vif;
          uvm_analysis_port #(bit [7:0]) ap;
          function new(string name, uvm_component parent); super.new(name, parent); ap = new("ap", this); endfunction
          task run_phase(uvm_phase phase);
            forever begin
              @(negedge vif.clk);
              if (vif.in_valid) ap.write(vif.in_data);
            end
          endtask
        endclass

        class out_monitor extends uvm_monitor;
          `uvm_component_utils(out_monitor)
          virtual pipe_if vif;
          uvm_analysis_port #(bit [7:0]) ap;
          function new(string name, uvm_component parent); super.new(name, parent); ap = new("ap", this); endfunction
          task run_phase(uvm_phase phase);
            forever begin
              @(negedge vif.clk);
              if (vif.out_valid) ap.write(vif.out_data);
            end
          endtask
        endclass

        class scoreboard extends uvm_component;
          `uvm_component_utils(scoreboard)
          uvm_tlm_analysis_fifo #(bit [7:0]) sent, seen;
          function new(string name, uvm_component parent);
            super.new(name, parent);
            sent = new("sent", this);
            seen = new("seen", this);
          endfunction
          function void check_phase(uvm_phase phase);
            bit [7:0] x, out;
            int n = 0, bad = 0, missing;
            while (seen.try_get(out)) begin
              void'(sent.try_get(x));
              n++;
              if (out != 8'(x + 1)) bad++;
            end
            missing = sent.used();
            `uvm_info("SB", $sformatf("%0t: %0d compared, %0d mismatches, %0d missing", $time, n, bad, missing), UVM_LOW)
            if (bad || missing) `uvm_error("SB", "TEST FAILED")
            else                `uvm_info("SB", "TEST PASSED", UVM_LOW)
          endfunction
        endclass

        class pipe_env extends uvm_env;
          `uvm_component_utils(pipe_env)
          virtual pipe_if         vif;
          uvm_sequencer #(item)   seqr;
          driver                  drv;
          in_monitor              mon_in;
          out_monitor             mon_out;
          scoreboard              sb;
          function new(string name, uvm_component parent); super.new(name, parent); endfunction
          function void build_phase(uvm_phase phase);
            if (!uvm_config_db #(virtual pipe_if)::get(this, "", "vif", vif)) `uvm_fatal("ENV", "no vif")
            seqr    = uvm_sequencer #(item)::type_id::create("seqr", this);
            drv     = driver::type_id::create("drv", this);
            mon_in  = in_monitor::type_id::create("mon_in", this);
            mon_out = out_monitor::type_id::create("mon_out", this);
            sb      = scoreboard::type_id::create("sb", this);
          endfunction
          function void connect_phase(uvm_phase phase);
            drv.vif = vif;
            mon_in.vif = vif;
            mon_out.vif = vif;
            drv.seq_item_port.connect(seqr.seq_item_export);
            mon_in.ap.connect(sb.sent.analysis_export);
            mon_out.ap.connect(sb.seen.analysis_export);
          endfunction
        endclass

        module top;
          logic clk = 0;
          always #5 clk = ~clk;
          pipe_if pif (clk);
          pipe dut (.clk, .rst_n(pif.rst_n), .in_valid(pif.in_valid), .in_data(pif.in_data),
                    .out_valid(pif.out_valid), .out_data(pif.out_data));
          initial begin
            uvm_config_db #(virtual pipe_if)::set(null, "uvm_test_top.env", "vif", pif);
            run_test();                     // +UVM_TESTNAME=smoke_test
          end
        endmodule
        ```

    ‏UVM ב-SystemVerilog לא רץ בבדיקות של האתר : ל-Verilator אין ספריית UVM. הגרסה של Python
    רצה, ‏pyuvm מעל cocotb ו-Verilator, וכל המספרים בעמוד באים ממנה. הבדיקות משוות את שתי
    הגרסאות לפי המבנה : אותן מחלקות, אותם רכיבים ואותן קריאות.

הטסט הראשון שנכתב לסביבה, וה-cocotb test שמריץ אותו :

=== "Python"
    ```python title="SmokeTest"
    class SmokeTest(uvm_test):
        def build_phase(self):
            self.env = PipeEnv("env", self)

        async def run_phase(self):
            await ItemSeq("seq").start(self.env.seqr)


    async def run(dut, test):
        cocotb.start_soon(Clock(dut.clk, 10, "ns").start(start_high=False))
        await uvm_root().run_test(test)


    @cocotb.test()
    async def smoke(dut):
        await run(dut, SmokeTest)
    ```

=== "SystemVerilog"
    ```systemverilog title="class smoke_test"
    class smoke_test extends uvm_test;
      `uvm_component_utils(smoke_test)
      pipe_env env;

      function new(string name, uvm_component parent);
        super.new(name, parent);
      endfunction

      function void build_phase(uvm_phase phase);
        env = pipe_env::type_id::create("env", this);
      endfunction

      task run_phase(uvm_phase phase);
        item_seq seq = item_seq::type_id::create("seq");
        seq.start(env.seqr);
      endtask
    endclass
    ```

השורות של ה-scoreboard בלוג של הריצה :

<!-- gen 0 -->

```text
INFO     [uvm_test_top.env.sb] 0 ns: 0 compared, 0 mismatches, 0 missing
INFO     [uvm_test_top.env.sb] TEST PASSED
```

<!-- /gen -->

הטסט עבר. שלושת הסעיפים שואלים מה קרה כאן, מה קורה אחרי התיקון הראשון, ומה קורה כשמתקנים
באופן אחר.

??? interviewer "מה המראיין בודק"
    - **מתי ה-run phase נגמר :** לא כשה-sequence נגמרת, אלא כשאין אף objection מורם.
    - **איפה מרימים objection :** ב-test, סביב ה-sequence, ולא ברכיבים שרצים לנצח.
    - **פריטים שבדרך :** ה-latency של ה-DUT, ה-drain time, ומה ה-scoreboard בודק בסוף.
    - **דיבאג של ריצה שלא נגמרת :** ‏timeout גלובלי, ורשימת ה-objections שעדיין מורמים.
    - **ביקורת על "עבר" :** טסט שלא בדק אף פריט לא עבר, גם אם אין בלוג אף שגיאה.

---

### סעיף א – הטסט שנגמר בזמן 0

הריצה נגמרה בזמן 0, וה-scoreboard לא השווה אף פריט. למה, ולמה הוא בכל זאת כותב
`TEST PASSED`? איפה צריך להרים את ה-objection, ואיפה להוריד אותו?

??? tip "רמז 1"
    ה-`run_phase` של כל הרכיבים רץ במקביל, ושל ה-driver ושל המוניטורים לא נגמר אף פעם. אז לפי
    מה UVM מחליט שה-run phase נגמר?

??? tip "רמז 2"
    מי בקוד הזה אמר ל-UVM "אל תסיים עדיין"? ומה ה-scoreboard סופר כשלא נכנס אף פריט?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ה-run phase נגמר כשאין אף objection מורם, ואף אחד לא הרים objection. לכן הוא נגמר כבר
        בזמן 0, לפני שה-driver סיים את האיפוס, וה-`check_phase` רץ על scoreboard ריק : ‏0 נכנסו
        ו-0 יצאו, אין חסרים ואין אי-התאמות, ולכן "עבר". התיקון : ‏`raise_objection` ב-test לפני
        `seq.start`, ו-`drop_objection` אחרי שהיא חוזרת.

    #### הרעיון { .sol-idea }

    ‏UVM מריץ את ה-phases לפי סדר קבוע (שאלה [0049](0049-uvm-testbench-architecture.md)) :
    ‏`build_phase` מלמעלה למטה, כי הורה יוצר את ילדיו; ‏`connect_phase` מלמטה למעלה; אחריהם
    `run_phase`, היחיד שצורך זמן סימולציה, שבו ה-task של כל רכיב רץ במקביל לאחרים; ובסוף
    `extract_phase`, ‏`check_phase` ו-`report_phase`, פונקציות בלי זמן.

    ה-`run_phase` של ה-driver ושל המוניטורים הוא לולאה אינסופית, ולכן UVM לא מחכה שה-tasks
    ייגמרו. הוא סופר objections : רכיב שמרים objection אומר "אני עוד באמצע", וה-run phase נגמר
    ברגע שהמונה חוזר ל-0. אם אף אחד לא הרים objection, המונה 0 מההתחלה, וה-run phase נגמר מיד,
    בזמן 0. ב-SystemVerilog ‏UVM הורג אז את כל ה-tasks של ה-run phase. ‏pyuvm לא הורג אותם,
    אבל השלבים שאחריו לא נותנים להם זמן, ו-cocotb מבטל אותם כשה-test שלו נגמר.

    ה-scoreboard לא מצא כלום כי לא היה מה למצוא : מוניטור הכניסה לא ראה אף פריט, ולכן גם אף פריט
    לא חסר. ‏pyuvm לפחות מזהיר, ‏`You did not call self.raise_objection() in any run_phase`. ‏UVM
    ב-SystemVerilog שותק.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הסימן בלוג :** ‏`0 ns`, ‏`0 compared`. טסט ששולח 8 פריטים לא נגמר בזמן 0.
    2. **הסיבה :** אין objection, ולכן ה-run phase נגמר מיד, וה-sequence לא הספיקה לשלוח כלום.
    3. **התיקון :** ה-test מרים objection לפני `seq.start` ומוריד אחרי שהיא חוזרת. ‏`seq.start`
       חוזרת כשה-driver סיים את הפריט האחרון.
    4. **הבדיקה :** הריצה נגמרת עכשיו ב-95 ns, וכל 8 הפריטים נכנסו. מה ה-scoreboard אומר על
       זה, בסעיף ב.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="ObjectionTest"
        class ObjectionTest(SmokeTest):
            async def run_phase(self):
                self.raise_objection()                      # (1)!
                await ItemSeq("seq").start(self.env.seqr)   # (2)!
                self.drop_objection()


        @cocotb.test()
        async def objection(dut):
            await run(dut, ObjectionTest)
        ```

        1. בשורה הראשונה של `run_phase`, לפני כל `await` : ה-run phase בודק אם הורם objection
           מיד אחרי שכל ה-tasks התחילו.
        2. חוזרת כשה-driver קרא ל-`item_done` של הפריט האחרון, ב-95 ns.

    === "SystemVerilog"
        ```systemverilog title="class objection_test" hl_lines="8 10"
        class objection_test extends smoke_test;
          `uvm_component_utils(objection_test)
          function new(string name, uvm_component parent);
            super.new(name, parent);
          endfunction
          task run_phase(uvm_phase phase);
            item_seq seq = item_seq::type_id::create("seq");
            phase.raise_objection(this);
            seq.start(env.seqr);
            phase.drop_objection(this);
          endtask
        endclass
        ```

    #### למה זה נכון { .sol-proof }

    ה-objection מורם בזמן 0, ולכן ה-run phase לא נגמר עד שהוא יורד. ה-driver מחזיק את האיפוס
    בעליות של 5 ו-15 ns, ומוסר פריט בכל מחזור : ה-DUT לוקח את פריט \( i \) בעלייה של
    \( 25 + 10i \) ns, ואת האחרון, פריט 7, ב-95 ns. אז ה-driver קורא ל-`item_done`, ‏`seq.start`
    חוזרת, ה-objection יורד, והריצה נגמרת ב-95 ns. את הלוג של הריצה הזו מראה סעיף ב.

    אפשר גם להרים את ה-objection בתוך ה-sequence הראשית : ב-UVM 1.2 ‏`starting_phase` של
    sequence שהופעלה כ-default sequence, או `set_automatic_phase_objection(1)`. ב-pyuvm אין לזה
    מקבילה, ושם הוא נשאר ב-test.

---

### סעיף ב – ארבעה פריטים שלא הגיעו

אחרי התיקון של סעיף א, אותה סביבה מריצה את `ObjectionTest`, וה-scoreboard כותב :

<!-- gen 1 -->

```text
INFO     [uvm_test_top.env.sb] 95 ns: 4 compared, 0 mismatches, 4 missing
ERROR    [uvm_test_top.env.sb] TEST FAILED
```

<!-- /gen -->

ה-DUT תקין. לאן נעלמו ארבעת הפריטים? למה משמש ה-drain time, ואיך קובעים אותו?

??? tip "רמז 1"
    מתי בדיוק `seq.start` חוזרת : כשהפריט האחרון יצא מה-DUT, או כשהוא נכנס אליו?

??? tip "רמז 2"
    כמה פריטים יש בתוך צינור של ארבעה שלבים, ברגע שהאחרון נכנס?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏`seq.start` חוזרת כשהפריט האחרון נכנס ל-DUT, ב-95 ns, וה-objection יורד מיד. ארבעת
        הפריטים האחרונים עוד בתוך הצינור, ויוצאים רק ב-100 עד 130 ns, אחרי שהריצה כבר נגמרה. ה-drain
        time הוא זמן ש-UVM מחכה אחרי שה-objection האחרון ירד, לפני שהוא מסיים את ה-run phase.
        הוא צריך להיות ארוך מה-latency : כאן יותר מ-35 ns, ולכן 40 ns.

    #### הרעיון { .sol-idea }

    ה-objection ירד כשה-stimulus נגמר, לא כשהבדיקה נגמרה. בין השניים עומד ה-latency של
    ה-DUT : פריט שנכנס בעלייה של \( t \) נראה ביציאה ב-\( t + 35 \) ns, שלושה מחזורים וחצי
    אחר כך. ב-95 ns, כשהאחרון נכנס, פריטים 4 עד 7 עוד בצינור :

    <!-- gen 2 -->

    <svg class="perf-chart q113-timeline" viewBox="0 0 400 158" style="max-width:34rem" role="img" aria-label="8 items: taken by the DUT at 25 to 95 ns, seen at the output at 60 to 130 ns; the objection drops at 95 ns, the drain ends at 135 ns"><rect class="hist-near" x="262.2" y="14" width="94.4" height="112"/><text class="tick" x="38.0" y="144" text-anchor="middle" style="font-size:14px">0</text><text class="tick" x="156.0" y="144" text-anchor="middle" style="font-size:14px">50</text><text class="tick" x="274.0" y="144" text-anchor="middle" style="font-size:14px">100</text><text class="tick" x="392.0" y="144" text-anchor="end" style="font-size:14px">150 ns</text><line class="axis" x1="38" x2="392" y1="126" y2="126"/><text class="tick" x="32" y="45" text-anchor="end" style="font-size:14px">in</text><text class="tick" x="32" y="97" text-anchor="end" style="font-size:14px">out</text><rect class="ink-line" x="74.9" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="85.2" y="45" text-anchor="middle" style="font-size:14px">0</text><rect class="s1-line" x="169.3" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="179.6" y="97" text-anchor="middle" style="font-size:14px">0</text><rect class="ink-line" x="98.5" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="108.8" y="45" text-anchor="middle" style="font-size:14px">1</text><rect class="s1-line" x="192.9" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="203.2" y="97" text-anchor="middle" style="font-size:14px">1</text><rect class="ink-line" x="122.1" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="132.4" y="45" text-anchor="middle" style="font-size:14px">2</text><rect class="s1-line" x="216.5" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="226.8" y="97" text-anchor="middle" style="font-size:14px">2</text><rect class="ink-line" x="145.7" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="156.0" y="45" text-anchor="middle" style="font-size:14px">3</text><rect class="s1-line" x="240.1" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="250.4" y="97" text-anchor="middle" style="font-size:14px">3</text><rect class="ink-line" x="169.3" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="179.6" y="45" text-anchor="middle" style="font-size:14px">4</text><rect class="s2-line" x="263.7" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="274.0" y="97" text-anchor="middle" style="font-size:14px">4</text><rect class="ink-line" x="192.9" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="203.2" y="45" text-anchor="middle" style="font-size:14px">5</text><rect class="s2-line" x="287.3" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="297.6" y="97" text-anchor="middle" style="font-size:14px">5</text><rect class="ink-line" x="216.5" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="226.8" y="45" text-anchor="middle" style="font-size:14px">6</text><rect class="s2-line" x="310.9" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="321.2" y="97" text-anchor="middle" style="font-size:14px">6</text><rect class="ink-line" x="240.1" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="250.4" y="45" text-anchor="middle" style="font-size:14px">7</text><rect class="s2-line" x="334.5" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="344.8" y="97" text-anchor="middle" style="font-size:14px">7</text><line class="ink-line" x1="262.2" x2="262.2" y1="14" y2="126" stroke-width="1.5" stroke-dasharray="5 4"/><line class="ink-line" x1="356.6" x2="356.6" y1="14" y2="126" stroke-width="1.5"/><text class="tick" x="262.2" y="12" text-anchor="middle" style="font-size:13px">95</text><text class="tick" x="356.6" y="12" text-anchor="middle" style="font-size:13px">135</text></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="s1"></i>פריט שיצא לפני 95 ns : נבדק בשתי הריצות</span><span><i class="s2"></i>פריט שעוד היה בצינור : נבדק רק עם drain</span><span><i class="ink-dash"></i>הורדת ה-objection בלי drain, ב-95 ns</span><span><i class="ink"></i>סוף הריצה עם drain של 40 ns, ב-135 ns</span></span>

    <!-- /gen -->

    ‏UVM נותן לזה כלי : ‏drain time על ה-objection של ה-phase. כשהמונה מגיע ל-0, ‏UVM מחכה את
    זמן ה-drain, ורק אז מסיים את ה-phase. אם מישהו מרים objection בזמן הזה, ההמתנה מתחילה מחדש.
    ‏pyuvm 5.0.0 לא מממש drain time : אין לו `set_drain_time`, וה-phase נגמר ברגע שהמונה מגיע ל-0.
    המקבילה שם היא להחזיק את ה-objection עוד אותו זמן, ‏`await Timer(...)` לפני `drop_objection`.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מי חסר :** ארבעה, בדיוק ‏LAT, מספר השלבים של הצינור.
    2. **מתי הם יוצאים :** פריט \( i \) נראה ביציאה ב-\( 60 + 10i \) ns, והאחרון ב-130 ns.
    3. **כמה לחכות :** מהורדת ה-objection, ב-95 ns, עד 130 ns, כלומר 35 ns. כל drain ארוך מזה
       מספיק.
    4. **התיקון :** ‏drain של 40 ns, ארבעה מחזורים. הריצה נגמרת ב-135 ns, ו-8 פריטים נבדקים.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="DrainTest"
        DRAIN_NS = 40


        class DrainTest(SmokeTest):
            async def run_phase(self):
                self.raise_objection()
                await ItemSeq("seq").start(self.env.seqr)
                await Timer(DRAIN_NS, "ns")                 # (1)!
                self.drop_objection()


        @cocotb.test()
        async def drain(dut):
            await run(dut, DrainTest)
        ```

        1. ‏pyuvm אין לו drain time, ולכן ה-test מחזיק את ה-objection עוד 40 ns. בזמן הזה
           המוניטורים וה-scoreboard ממשיכים לרוץ.

    === "SystemVerilog"
        ```systemverilog title="class drain_test" hl_lines="8"
        class drain_test extends smoke_test;
          `uvm_component_utils(drain_test)
          function new(string name, uvm_component parent);
            super.new(name, parent);
          endfunction
          task run_phase(uvm_phase phase);
            item_seq seq = item_seq::type_id::create("seq");
            phase.get_objection().set_drain_time(this, 40ns);   // (1)!
            phase.raise_objection(this);
            seq.start(env.seqr);
            phase.drop_objection(this);
          endtask
        endclass
        ```

        1. ב-UVM 1.1 כותבים `phase.phase_done.set_drain_time(this, 40ns)`. מ-UVM 1.2
           ‏`get_objection()` מחזירה את אותו objection.

    #### למה זה נכון { .sol-proof }

    ה-DUT לוקח את פריט \( i \) בעלייה של \( 25 + 10i \) ns, וביט ה-valid שלו עובר ארבעה
    רגיסטרים : הראשון נכתב באותה עלייה, והרביעי שלוש עליות אחר כך, ב-\( 55 + 10i \) ns.
    מוניטור היציאה דוגם בירידה הבאה, ב-\( 60 + 10i \) ns. הריצה נגמרת בהורדת ה-objection ועוד
    ה-drain, \( 95 + D \) ns, וה-scoreboard בודק כל פריט שנראה לפני כן, כלומר כל \( i \) עם
    \( 60 + 10i < 95 + D \). עם \( D = 0 \) אלה פריטים 0 עד 3, ועם \( D > 35 \) כל השמונה :

    <!-- gen 4 -->

    | ה-drain | סוף הריצה | נבדקו | חסרים | התוצאה |
    |:-:|:-:|:-:|:-:|:-:|
    | 0 ns | 95 ns | 4 | 4 | נכשל |
    | 10 ns | 105 ns | 5 | 3 | נכשל |
    | 20 ns | 115 ns | 6 | 2 | נכשל |
    | 30 ns | 125 ns | 7 | 1 | נכשל |
    | 40 ns | 135 ns | 8 | 0 | עובר |
    | 50 ns | 145 ns | 8 | 0 | עובר |

    <!-- /gen -->

    ה-drain קבוע, ולכן הוא נכון רק כל עוד ה-latency קבוע. ‏DUT עם backpressure, או עם latency
    שתלוי בנתונים, צריך סוף אחר : המלכודות למטה.

---

### סעיף ג – הטסט שלא נגמר

עמית ראה את סעיף ב ותיקן אחרת. לדעתו מוניטור היציאה הוא זה שיודע מתי הפריט האחרון יצא, ולכן
הוא צריך להחזיק objection. הוא החליף את `OutMonitor` בגרסה הזו, והריץ את `DrainTest` :

=== "Python"
    ```python title="OutMonitor, the colleague's version"
    class OutMonitor(InMonitor):
        PINS = ("out_valid", "out_data")

        async def run_phase(self):
            self.raise_objection()          # (1)!
            await super().run_phase()
            self.drop_objection()
    ```

    1. "שהטסט יחכה למוניטור".

=== "SystemVerilog"
    ```systemverilog title="class out_monitor, the colleague's version" hl_lines="7 12"
    class out_monitor extends uvm_monitor;
      `uvm_component_utils(out_monitor)
      virtual pipe_if vif;
      uvm_analysis_port #(bit [7:0]) ap;
      function new(string name, uvm_component parent); super.new(name, parent); ap = new("ap", this); endfunction
      task run_phase(uvm_phase phase);
        phase.raise_objection(this);
        forever begin
          @(negedge vif.clk);
          if (vif.out_valid) ap.write(vif.out_data);
        end
        phase.drop_objection(this);
      endtask
    endclass
    ```

הריצה לא נגמרת. למה? איך רואים מי מחזיק אותה, ואיך מתקנים?

??? tip "רמז 1"
    מתי `super().run_phase()` חוזרת?

??? tip "רמז 2"
    ריצה שלא נגמרת לא כותבת כלום ללוג. מה גורם לה להיעצר ולהגיד מי עוד מחזיק objection?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ה-`run_phase` של מוניטור הוא לולאה אינסופית, ולכן השורה שמורידה את ה-objection לא
        מתבצעת אף פעם. המונה לא חוזר ל-0, וה-run phase לא נגמר. רואים את זה עם timeout גלובלי,
        שעוצר את הריצה ומדפיס את ה-objections שעדיין מורמים : אחד, של
        `uvm_test_top.env.mon_out`. התיקון : להחזיר את `OutMonitor` המקורי. ‏driver ומוניטור לא
        מרימים objection בלולאה שלהם, וה-drain של סעיף ב הוא שמחכה לפריטים שבדרך.

    #### הרעיון { .sol-idea }

    בכוונה של העמית יש היגיון : מי שרואה את היציאה יודע מתי הפריט האחרון יצא. אבל הוא הרים
    objection אחד לכל הריצה, במקום שאין לו סוף, ולא לכל פריט שבדרך. ‏`super().run_phase()` היא
    הלולאה של `InMonitor`, והיא לא חוזרת. ב-SystemVerilog זה ה-`forever`, וה-`drop_objection`
    שאחריו לא מתבצע.

    בלי timeout הסימולציה רצה עד שמישהו עוצר אותה : השעון ממשיך, וה-objection מורם לנצח. ‏UVM
    ב-SystemVerilog עוצר בסוף ב-timeout של ברירת המחדל, 9200 s של זמן סימולציה, עם `UVM_FATAL`
    ‏`PH_TIMEOUT`, ואז כבר עברו שעות. ‏pyuvm ו-cocotb לא עוצרים בכלל. לכן כל סביבה צריכה timeout
    משלה, קצר : כאן 100 µs, פי 700 בערך מאורך הטסט.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **לעצור :** ‏timeout גלובלי. ב-cocotb ‏`with_timeout` סביב `run_test`, וב-UVM
       ‏`uvm_top.set_timeout`.
    2. **לראות מי מחזיק :** ב-pyuvm ‏`str(ObjectionHandler())` מדפיס כל objection מורם, מי הרים
       ובאיזו שורה. ב-UVM ‏`+UVM_OBJECTION_TRACE` מדפיס כל הרמה והורדה, ו-`display_objections()`
       את המצב ברגע נתון.
    3. **הסיבה :** ‏`mon_out` הרים objection לפני לולאה אינסופית.
    4. **התיקון :** ‏`OutMonitor` המקורי, בלי objection. ‏`DrainTest` נגמר אז ב-135 ns, ו-8
       פריטים נבדקים.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="run, with a global timeout"
        async def run(dut, test, limit_us=100):
            cocotb.start_soon(Clock(dut.clk, 10, "ns").start(start_high=False))
            try:
                await with_timeout(uvm_root().run_test(test), limit_us, "us")   # (1)!
            except SimTimeoutError:
                dut._log.critical(f"timeout at {get_sim_time('ns'):g} ns\n{ObjectionHandler()}")
                raise                                                          # (2)!
        ```

        1. ‏`run_test` כמו קודם, אבל עם גבול : אחרי 100 µs ‏cocotb מבטל אותה וזורק
           `SimTimeoutError`.
        2. ה-cocotb test נכשל, אחרי שהלוג אמר מי עוד מחזיק objection.

    === "SystemVerilog"
        ```systemverilog title="module top, with a global timeout" hl_lines="9"
        module top;
          logic clk = 0;
          always #5 clk = ~clk;
          pipe_if pif (clk);
          pipe dut (.clk, .rst_n(pif.rst_n), .in_valid(pif.in_valid), .in_data(pif.in_data),
                    .out_valid(pif.out_valid), .out_data(pif.out_data));
          initial begin
            uvm_config_db #(virtual pipe_if)::set(null, "uvm_test_top.env", "vif", pif);
            uvm_top.set_timeout(100us);     // (1)!
            run_test();
          end
        endmodule
        ```

        1. או בשורת הפקודה, ‏`+UVM_TIMEOUT`. בלי אחד מהם ה-timeout הוא 9200 s.

    #### למה זה נכון { .sol-proof }

    עם הגרסה של העמית, ה-`run` המתוקן עוצר את `DrainTest` ב-100 µs, והלוג אומר מי מחזיק (‏pyuvm
    מוסיף גם את הקובץ והשורה של ההרמה) :

    <!-- gen 5 -->

    ```text
    CRITICAL [cocotb.pipe] timeout at 100000 ns
    Active objections:
     raised by uvm_test_top.env.mon_out, description=""
    ```

    <!-- /gen -->

    ה-test הוריד את ה-objection שלו ב-135 ns, ולכן ברשימה נשאר רק זה של `mon_out`. בלי ההרמה
    של העמית אף רכיב שרץ לנצח לא מחזיק objection, והמונה חוזר ל-0 בדיוק כשה-test מוריד. ארבע
    הריצות של העמוד, כמו ש-Verilator מריץ אותן :

    <!-- gen 6 -->

    | הריצה | סוף הריצה | נבדקו | חסרים | מה ה-scoreboard אומר |
    |:--|:-:|:-:|:-:|:--|
    | ‏`SmokeTest`, בלי objection | 0 ns | 0 | 0 | עובר : לא נבדק כלום |
    | ‏`ObjectionTest`, בלי drain | 95 ns | 4 | 4 | נכשל |
    | ‏`DrainTest`, ‏drain של 40 ns | 135 ns | 8 | 0 | עובר |
    | ‏`DrainTest` עם המוניטור של העמית | אין סוף : נעצר ב-100 µs | — | — | לא מגיע ל-`check_phase` |

    <!-- /gen -->

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : objection שמורם מאוחר או יורד מוקדם"
    ה-run phase בודק אם הורם objection מיד אחרי שכל ה-tasks שלו התחילו. ‏test שמחכה קודם
    למחזור שעון, ‏`await ClockCycles(clk, 1)` ורק אז מרים, מאחר : הריצה כבר נגמרה בזמן 0. כך גם
    test שמרים, מפעיל את ה-sequence ברקע (`cocotb.start_soon`, או `fork ... join_none`) ומוריד
    מיד : המונה עלה וירד באותו רגע, והריצה נגמרת ב-0. במקרה השני ‏pyuvm גם לא מזהיר, כי objection
    כן הורם.

??? trap "מלכודת : scoreboard שעובר על אפס"
    ה-scoreboard של השאלה בודק אי-התאמות וחסרים, ושניהם 0 כשלא נכנס כלום. בדיקה שלא בדקה אף
    פריט צריכה להיכשל : ב-`check_phase` שורה כמו `if not seen: self.logger.error(...)`, או
    השוואה של מספר הפריטים לזה שה-sequence התכוונה לשלוח. אותו דבר ל-coverage : טסט שעובר בלי
    שהגיע לשום bin מסתיר בעיה בסביבה.

??? trap "מלכודת : drain time במקום לחכות לפריטים"
    ‏drain קבוע הוא ניחוש של ה-latency. ‏DUT עם backpressure, או ש-latency שלו תלוי בנתונים,
    יעבור אותו בריצה אחת וייכשל באחרת, ו-drain ארוך מדי מאריך כל טסט. סוף מדויק יותר : ה-test
    מחכה, אחרי ה-sequence, שה-scoreboard לא יחכה לאף פריט, עם גבול זמן; או שה-scoreboard מרים
    objection כשפריט נכנס ומוריד כשהוא יוצא, בכל מסלול, גם באי-התאמה.

??? followup "שאלות המשך"
    - **איפה עוד מרימים objection :** האם מותר להרים objection ב-driver?

        ??? fu-answer "תשובה"
            מותר, לכל פריט : הרמה ב-`get_next_item` והורדה ב-`item_done`. אבל זה עולה בביצועים,
            וכל מסלול שיוצא מהלולאה בלי הורדה תוקע את הריצה. ברוב הסביבות ה-test או ה-sequence
            הראשית מחזיקים objection אחד.

    - **‏phase_ready_to_end :** מה הוא נותן שה-drain time לא נותן?

        ??? fu-answer "תשובה"
            ‏UVM קורא לו כשהמונה של phase מגיע ל-0. רכיב, למשל ה-scoreboard, יכול להרים שם
            objection, לחכות שהתור שלו יתרוקן ולהוריד. זה סוף שתלוי במה שקרה בפועל, לא בזמן קבוע.

    - **‏run phase מול runtime phases :** מה ההבדל בין `run_phase` ל-`main_phase`?

        ??? fu-answer "תשובה"
            ה-`run_phase` רץ במקביל ל-12 ה-runtime phases (‏`reset`, ‏`configure`, ‏`main`, ‏`shutdown`
            ועוד), ולכל אחד מהם objection משלו. ‏pyuvm מממש רק את `run_phase`.

    - **‏timeout :** למה לא לסמוך על ה-timeout של ברירת המחדל של UVM?

        ??? fu-answer "תשובה"
            כי הוא 9200 s של זמן סימולציה : ריצה תקועה תופסת מכונה ורישיון שעות לפני שהיא נכשלת.
            ‏timeout קצר, בסדר גודל אחד או שניים מעל אורך הטסט, נכשל מהר ואומר מי מחזיק.

    - **ספירה :** מה קורה כש-test מרים objection פעמיים ומוריד פעם אחת? וכשהוא מוריד בלי שהרים?

        ??? fu-answer "תשובה"
            ‏objection הוא מונה, לא דגל : אחרי שתי הרמות והורדה אחת המונה 1, והריצה לא נגמרת, כמו
            בסעיף ג. הורדה בלי הרמה היא שגיאה : ב-UVM ‏`UVM_ERROR` עם `OBJTN_ZERO`, וב-pyuvm אזהרה,
            והמונה לא יורד מתחת ל-0.
