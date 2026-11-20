---
id: 112
title: ה-override שלא נכנס לתוקף
level: junior
difficulty: medium
kind: dv
tags: [uvm, methodology, debug, python, systemverilog]
source: ""
added: 2026-11-20
---

## השאלה

ה-DUT מקבל בתים בשני ערוצים. עם כל בית מגיע ביט זוגיות (even parity, ‏`^data`), וה-DUT סופר
בכל ערוץ את הפריטים שביט הזוגיות שלהם שגוי :

```systemverilog title="module parity_rx" linenums="1"
module parity_rx (
  input  logic       clk,
  input  logic       valid0, valid1,
  input  logic [7:0] data0, data1,
  input  logic       par0, par1,      // even parity: ^data
  output logic [7:0] errs0 = 0,       // items whose parity bit was wrong
  output logic [7:0] errs1 = 0
);
  always_ff @(posedge clk) begin
    if (valid0 && par0 != ^data0) errs0 <= errs0 + 1;
    if (valid1 && par1 != ^data1) errs1 <= errs1 + 1;
  end
endmodule
```

סביבת הבדיקה בנויה כמו ב-[ארכיטקטורה של סביבת UVM](0049-uvm-testbench-architecture.md) : agent
לכל ערוץ, ובו sequencer ו-driver. ה-driver הרגיל, `ParityDriver`, שולח כל בית עם ביט זוגיות
נכון. כדי לבדוק את המונים כתבו לו תת-class, `ErrDriver`, ששולח ביט הפוך בכל פריט רביעי. הטסט
`ErrTest` לא נוגע ב-env : הוא מבקש מה-factory לבנות `ErrDriver` בכל מקום שבו נבנה
`ParityDriver` (type override). הסביבה כתובה ב-Python עם [pyuvm](https://github.com/pyuvm/pyuvm)
ורצה ב-cocotb על Verilator, ולצדה הגרסה של SystemVerilog UVM :

=== "Python"
    ```python title="pyuvm: item, sequence, drivers" linenums="1"
    import cocotb
    from cocotb.clock import Clock
    from cocotb.triggers import FallingEdge
    import pyuvm
    from pyuvm import *


    class ByteItem(uvm_sequence_item):
        def __init__(self, name="item"):
            super().__init__(name)
            self.data = 0


    class Bytes(uvm_sequence):
        """Eight bytes on one channel."""

        async def body(self):
            for n in range(8):
                item = ByteItem.create(f"item{n}")
                await self.start_item(item)
                item.data = 37 * n % 256
                await self.finish_item(item)


    class ParityDriver(uvm_driver):
        """A byte and its even parity bit, one item every two cycles."""

        def build_phase(self):
            self.valid, self.data, self.par, self.errs = ConfigDB().get(self, "", "BUS")   # (1)!
            self.sent = 0

        def parity(self, data):
            return bin(data).count("1") % 2

        async def run_phase(self):
            while True:
                item = await self.seq_item_port.get_next_item()
                await FallingEdge(cocotb.top.clk)
                self.valid.value = 1
                self.data.value = item.data
                self.par.value = self.parity(item.data)
                self.sent += 1
                await FallingEdge(cocotb.top.clk)
                self.valid.value = 0
                self.seq_item_port.item_done()


    class ErrDriver(ParityDriver):
        """The same driver, with a wrong parity bit on every fourth item."""

        def parity(self, data):
            return super().parity(data) ^ (self.sent % 4 == 3)   # (2)!
    ```

    1. האותות של הערוץ מגיעים מ-`ConfigDB`, כמו virtual interface ב-SystemVerilog : ה-env שם
       בו לכל agent את האותות של הערוץ שלו.
    2. ‏`sent` סופר את הפריטים שכבר נשלחו, ולכן הפריטים שמתהפכים הם 3 ו-7 : שניים מתוך שמונה
       בכל ערוץ.

=== "SystemVerilog"
    ```systemverilog title="UVM: item, sequence, drivers" linenums="1"
    `include "uvm_macros.svh"
    import uvm_pkg::*;

    interface ch_if (input logic clk);
      logic       valid, par;
      logic [7:0] data, errs;
    endinterface

    class byte_item extends uvm_sequence_item;
      `uvm_object_utils(byte_item)
      bit [7:0] data;
      function new(string name = "item");
        super.new(name);
      endfunction
    endclass

    class bytes_seq extends uvm_sequence #(byte_item);
      `uvm_object_utils(bytes_seq)
      function new(string name = "bytes");
        super.new(name);
      endfunction
      task body();
        for (int n = 0; n < 8; n++) begin
          req = byte_item::type_id::create($sformatf("item%0d", n));
          start_item(req);
          req.data = 37 * n % 256;
          finish_item(req);
        end
      endtask
    endclass

    class parity_driver extends uvm_driver #(byte_item);
      `uvm_component_utils(parity_driver)
      virtual ch_if vif;
      int sent;
      function new(string name, uvm_component parent);
        super.new(name, parent);
      endfunction
      function void build_phase(uvm_phase phase);
        if (!uvm_config_db#(virtual ch_if)::get(this, "", "BUS", vif))
          `uvm_fatal("NOBUS", "no BUS for this driver")
      endfunction
      virtual function bit parity(bit [7:0] data);
        return ^data;
      endfunction
      task run_phase(uvm_phase phase);
        forever begin
          seq_item_port.get_next_item(req);
          @(negedge vif.clk);
          vif.valid <= 1;
          vif.data  <= req.data;
          vif.par   <= parity(req.data);
          sent++;
          @(negedge vif.clk);
          vif.valid <= 0;
          seq_item_port.item_done();
        end
      endtask
    endclass

    class err_driver extends parity_driver;
      `uvm_component_utils(err_driver)
      function new(string name, uvm_component parent);
        super.new(name, parent);
      endfunction
      function bit parity(bit [7:0] data);
        return super.parity(data) ^ (sent % 4 == 3);
      endfunction
    endclass
    ```

ה-agent, ה-env והטסט :

=== "Python"
    ```python title="pyuvm: agent, env, test" linenums="1"
    class Agent(uvm_agent):
        def build_phase(self):
            self.seqr = uvm_sequencer.create("seqr", self)
            self.drv = ParityDriver("drv", self)

        def connect_phase(self):
            self.drv.seq_item_port.connect(self.seqr.seq_item_export)


    class Env(uvm_env):
        def build_phase(self):
            dut = cocotb.top
            ConfigDB().set(self, "agt0.*", "BUS", (dut.valid0, dut.data0, dut.par0, dut.errs0))   # (1)!
            ConfigDB().set(self, "agt1.*", "BUS", (dut.valid1, dut.data1, dut.par1, dut.errs1))
            self.agt0 = Agent.create("agt0", self)
            self.agt1 = Agent.create("agt1", self)


    class ErrTest(uvm_test):
        """Wrong parity bits on both channels: the DUT must count them."""

        def build_phase(self):
            uvm_factory().set_type_override_by_type(ParityDriver, ErrDriver)
            self.env = Env.create("env", self)

        async def run_phase(self):
            self.raise_objection()
            for agt in (self.env.agt0, self.env.agt1):
                await Bytes.create("bytes").start(agt.seqr)
            self.drop_objection()

        def report_phase(self):
            for agt in (self.env.agt0, self.env.agt1):
                drv = agt.drv
                self.logger.info(f"{drv.get_full_name()}: {drv.get_type_name()}, "
                                 f"{int(drv.errs.value)} parity errors")


    @cocotb.test()
    async def err_test(dut):
        Clock(dut.clk, 10, unit="ns").start()
        await uvm_root().run_test(ErrTest)
    ```

    1. ב-pyuvm הפונקציה `run_test` מנקה את `ConfigDB` ואת ה-overrides של ה-factory לפני שהיא
       בונה את הטסט, ולכן האותות נכנסים כאן, בתוך העץ, ולא בבדיקת ה-cocotb.

=== "SystemVerilog"
    ```systemverilog title="UVM: agent, env, test" linenums="1"
    class agent extends uvm_agent;
      `uvm_component_utils(agent)
      uvm_sequencer #(byte_item) seqr;
      parity_driver drv;
      function new(string name, uvm_component parent);
        super.new(name, parent);
      endfunction
      function void build_phase(uvm_phase phase);
        seqr = uvm_sequencer#(byte_item)::type_id::create("seqr", this);
        drv  = new("drv", this);
      endfunction
      function void connect_phase(uvm_phase phase);
        drv.seq_item_port.connect(seqr.seq_item_export);
      endfunction
    endclass

    class tb_env extends uvm_env;
      `uvm_component_utils(tb_env)
      agent agt0, agt1;
      function new(string name, uvm_component parent);
        super.new(name, parent);
      endfunction
      function void build_phase(uvm_phase phase);
        agt0 = agent::type_id::create("agt0", this);
        agt1 = agent::type_id::create("agt1", this);
      endfunction
    endclass

    class err_test extends uvm_test;
      `uvm_component_utils(err_test)
      tb_env env;
      function new(string name, uvm_component parent);
        super.new(name, parent);
      endfunction
      function void build_phase(uvm_phase phase);
        parity_driver::type_id::set_type_override(err_driver::get_type());
        env = tb_env::type_id::create("env", this);
      endfunction
      task run_phase(uvm_phase phase);
        agent agents[2] = '{env.agt0, env.agt1};
        bytes_seq seq;
        phase.raise_objection(this);
        foreach (agents[i]) begin
          seq = bytes_seq::type_id::create("bytes");
          seq.start(agents[i].seqr);
        end
        phase.drop_objection(this);
      endtask
      function void report_phase(uvm_phase phase);
        agent agents[2] = '{env.agt0, env.agt1};
        foreach (agents[i])
          `uvm_info("REPORT", $sformatf("%s: %s, %0d parity errors", agents[i].drv.get_full_name(),
                    agents[i].drv.get_type_name(), agents[i].drv.vif.errs), UVM_NONE)
      endfunction
    endclass

    module top;
      logic clk = 0;
      always #5 clk = ~clk;
      ch_if ch0 (clk), ch1 (clk);
      parity_rx dut (.clk,
                     .valid0(ch0.valid), .data0(ch0.data), .par0(ch0.par), .errs0(ch0.errs),
                     .valid1(ch1.valid), .data1(ch1.data), .par1(ch1.par), .errs1(ch1.errs));
      initial begin
        uvm_config_db#(virtual ch_if)::set(null, "uvm_test_top.env.agt0.*", "BUS", ch0);
        uvm_config_db#(virtual ch_if)::set(null, "uvm_test_top.env.agt1.*", "BUS", ch1);
        run_test("err_test");
      end
    endmodule
    ```

ה-UVM של SystemVerilog לא רץ בבדיקות של האתר (ל-Verilator אין ספריית UVM). הגרסה של Python
היא זו שרצה, ב-pyuvm על Verilator, והבדיקות מוודאות שבגרסה של SystemVerilog יש אותם
class-ים ואותן קריאות בנקודות שהשאלה עוסקת בהן.

הטסט היה אמור להראות שתי שגיאות בכל ערוץ. השורות של `report_phase` מהלוג :

<!-- gen 0 -->

```text
uvm_test_top.env.agt0.drv: ParityDriver, 0 parity errors
uvm_test_top.env.agt1.drv: ParityDriver, 0 parity errors
```

<!-- /gen -->

??? interviewer "מה המראיין בודק"
    - **מה ה-factory באמת עושה :** האם המועמד יודע ש-override הוא רשומה בטבלה, ושמישהו צריך
      לשאול את הטבלה הזו בזמן הבנייה.
    - **קריאת לוג :** האם הוא שם לב לשם ה-class של הרכיב שנבנה, ולא רק למספר השגיאות.
    - **‏type מול instance :** מתי מחליפים את כל המופעים של טיפוס, ומתי רק מופע אחד לפי הנתיב שלו
      בעץ.
    - **דיבאג שיטתי :** האם הוא יודע להדפיס את מה שה-factory שמר ולהשוות לשם המלא של הרכיב,
      במקום לנסות נתיבים עד שמשהו עובד.
    - **סדר ה-phases :** מתי נבנה כל רכיב, ועד מתי אפשר עוד לקבוע override.

---

### סעיף א – ה-driver שלא הוחלף

ה-override נקבע ב-`build_phase` של הטסט, לפני שה-env נבנה, ובכל זאת שני ה-drivers הם
`ParityDriver` ואין אף שגיאה. למה? תקנו, ואמרו מה הלוג יראה אחרי התיקון.

??? tip "רמז 1"
    באיזו שורה ה-driver נבנה? ומי, בשורה הזו, יכול לדעת שיש override?

??? tip "רמז 2"
    ה-override הוא רשומה בטבלה של ה-factory. איזו קריאה בכלל קוראת את הטבלה הזו?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ה-agent בונה את ה-driver בקריאה ישירה לבנאי, `ParityDriver("drv", self)` (ב-SystemVerilog
        ‏`new("drv", this)`). קריאה כזו בונה תמיד בדיוק את ה-class שכתוב בה, וה-factory לא נשאל.
        התיקון : ‏`ParityDriver.create("drv", self)` (ב-SystemVerilog
        ‏`parity_driver::type_id::create("drv", this)`). אחרי התיקון שני ה-drivers הם `ErrDriver`,
        וה-DUT סופר שתי שגיאות בכל ערוץ.

    #### הרעיון { .sol-idea }

    ‏`set_type_override_by_type` לא משנה אף אובייקט ואף class. הוא רק כותב שורה בטבלה של
    ה-factory : "מי שמבקש `ParityDriver` יקבל `ErrDriver`". השורה הזו משפיעה רק על מי ששואל
    את ה-factory, כלומר על `create`. ‏`create` מקבל את ה-class שביקשו ואת הנתיב של הרכיב החדש,
    בודק בטבלה, ובונה את ה-class שהטבלה אומרת. קריאה ישירה לבנאי לא עוברת שם בכלל :

    <!-- gen 1 -->

    <svg class="figure uv-fig" viewBox="0 0 420 256" style="max-width:28rem" role="img" aria-label="שתי דרכים לבנות את ה-driver : קריאה ישירה ל-ParityDriver בונה ParityDriver, ו-create עובר דרך ה-factory, שמחזיר ErrDriver"><defs><marker id="fo-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs><g class="uv-box is-cont"><text x="105" y="24" text-anchor="middle">ParityDriver("drv", self)</text><text x="315" y="24" text-anchor="middle">ParityDriver.create(…)</text></g><line class="uv-arrow uv-pin" x1="105" y1="36" x2="105" y2="196" marker-end="url(#fo-arrow)"/><line class="uv-arrow uv-tlm" x1="315" y1="36" x2="315" y2="76" marker-end="url(#fo-arrow)"/><g class="uv-box uv-scoreboard"><rect x="230" y="80" width="170" height="72" rx="6"/><text x="315" y="103" text-anchor="middle">factory</text><text x="315" y="121" text-anchor="middle">ParityDriver</text><text x="315" y="139" text-anchor="middle">→ ErrDriver</text></g><line class="uv-arrow uv-tlm" x1="315" y1="152" x2="315" y2="196" marker-end="url(#fo-arrow)"/><g class="uv-box"><rect x="35" y="200" width="140" height="44" rx="6"/><text x="105" y="227" text-anchor="middle">ParityDriver</text></g><g class="uv-box uv-dut"><rect x="245" y="200" width="140" height="44" rx="6"/><text x="315" y="227" text-anchor="middle">ErrDriver</text></g></svg>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="uv-key-pin"></i>קריאה ישירה לבנאי : ה-factory לא נשאל</span><span><i class="uv-key-tlm"></i>דרך create : ה-factory בוחר את ה-class</span></span>

    <!-- /gen -->

    לכן הכלל ב-UVM : כל רכיב וכל אובייקט (גם sequence ו-sequence item) נבנים דרך ה-factory.
    ‏`new` אחד, אפילו בעומק העץ, הוא מקום שאף test לא יוכל להחליף.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הלוג :** השם של ה-class שנבנה, `ParityDriver`, אומר שה-override לא הגיע ל-driver. זו
       לא בעיה של ה-DUT ולא של המונים.
    2. **ה-override נרשם :** ‏`uvm_factory().print(0)` מראה ש-`ErrDriver` רשום כ-type override של
       `ParityDriver`, ולכן הבעיה לא בטסט.
    3. **השורה האשמה :** ב-`build_phase` של ה-agent, ה-sequencer נבנה ב-`create` וה-driver
       בבנאי.
    4. **התיקון :** ‏`create` גם ל-driver. ה-env וה-agent לא צריכים לדעת על `ErrDriver`.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="Agent" hl_lines="4"
        class Agent(uvm_agent):
            def build_phase(self):
                self.seqr = uvm_sequencer.create("seqr", self)
                self.drv = ParityDriver.create("drv", self)   # (1)!

            def connect_phase(self):
                self.drv.seq_item_port.connect(self.seqr.seq_item_export)
        ```

        1. ‏`create` הוא class method : ‏pyuvm רושם כל class שיורש מ-`uvm_void` ב-factory לבד,
           בלי מאקרו, ואין `type_id`.

    === "SystemVerilog"
        ```systemverilog title="class agent" hl_lines="10"
        class agent extends uvm_agent;
          `uvm_component_utils(agent)
          uvm_sequencer #(byte_item) seqr;
          parity_driver drv;
          function new(string name, uvm_component parent);
            super.new(name, parent);
          endfunction
          function void build_phase(uvm_phase phase);
            seqr = uvm_sequencer#(byte_item)::type_id::create("seqr", this);
            drv  = parity_driver::type_id::create("drv", this);   // (1)!
          endfunction
          function void connect_phase(uvm_phase phase);
            drv.seq_item_port.connect(seqr.seq_item_export);
          endfunction
        endclass
        ```

        1. ‏`type_id::create` קיים רק ל-class שנרשם ב-`` `uvm_component_utils``. גם
           `err_driver` צריך את המאקרו, אחרת אין לו `get_type()` לתת ל-override.

    #### למה זה נכון { .sol-proof }

    אותה ריצה, עם ה-agent המתוקן :

    <!-- gen 3 -->

    ```text
    uvm_test_top.env.agt0.drv: ErrDriver, 2 parity errors
    uvm_test_top.env.agt1.drv: ErrDriver, 2 parity errors
    ```

    <!-- /gen -->

    כל `ErrDriver` שולח שמונה פריטים, ומהפך את ביט הזוגיות כש-`sent` הוא 3 או 7, לפני שהוא
    עולה. ה-DUT רואה שני פריטים שגויים בכל ערוץ, ו-`errs0` ו-`errs1` מגיעים ל-2. לפני התיקון
    הקוד של `ErrDriver` לא רץ בכלל, כי אף אובייקט ממנו לא נבנה.

    שימו לב שה-env לא השתנה ולא יודע על `ErrDriver`. זה כל הטעם של ה-factory : test אחד מזריק
    שגיאות, test אחר רץ נקי, ושניהם משתמשים באותה סביבה.

---

### סעיף ב – override לערוץ אחד

עכשיו רוצים טסט שמזריק שגיאות רק בערוץ 1, וערוץ 0 נשאר נקי, לביקורת.

- **‏type מול instance :** מה ההבדל בין type override ל-instance override? ומה קורה כשיש
  לאותו טיפוס את שניהם?
- **הנתיב :** עמית כתב את הטסט הזה, וקיבל `ParityDriver` בשני הערוצים ו-0 שגיאות. למה? איך
  מוצאים את זה בלי לנחש? תקנו.
- **הזמן :** האם משנה איפה בתוך `build_phase` של הטסט נמצאת הקריאה? ומה אם היא עוברת
  ל-`connect_phase`?

=== "Python"
    ```python title="Chan1Test"
    class Chan1Test(ErrTest):
        """Wrong parity bits on channel 1 only."""

        def build_phase(self):
            uvm_factory().set_inst_override_by_type(ParityDriver, ErrDriver, "env.agt1.drv")
            self.env = Env.create("env", self)


    @cocotb.test()
    async def chan1_test(dut):
        Clock(dut.clk, 10, unit="ns").start()
        await uvm_root().run_test(Chan1Test)
    ```

=== "SystemVerilog"
    ```systemverilog title="class chan1_test"
    class chan1_test extends err_test;
      `uvm_component_utils(chan1_test)
      function new(string name, uvm_component parent);
        super.new(name, parent);
      endfunction
      function void build_phase(uvm_phase phase);
        uvm_factory factory = uvm_factory::get();
        factory.set_inst_override_by_type(parity_driver::get_type(), err_driver::get_type(), "env.agt1.drv");
        env = tb_env::type_id::create("env", this);
      endfunction
    endclass
    ```

??? tip "רמז 1"
    מה השם המלא של ה-driver של `agt1`? הלוג של `report_phase` כבר מדפיס אותו.

??? tip "רמז 2"
    ‏`uvm_factory().print(0)` מדפיס את ה-overrides בדיוק כמו שה-factory שמר אותם. השוו את
    הנתיב שם לשם המלא.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏type override מחליף את הטיפוס בכל מקום שבו הוא נבנה. ‏instance override מחליף אותו רק
        ב-create שהנתיב המלא שלו מתאים לתבנית, והוא קודם ל-type override. הנתיב של העמית,
        `env.agt1.drv`, לא מתאים לשום רכיב : השם המלא מתחיל ב-`uvm_test_top`, השם שנותן
        `run_test` לטסט. התיקון : הנתיב המלא, `uvm_test_top.env.agt1.drv`, שנבנה
        מ-`get_full_name()` של הטסט. המקום בתוך `build_phase` לא משנה, אבל `connect_phase` מאוחר
        מדי : כל ה-drivers כבר נבנו.

    #### הרעיון { .sol-idea }

    בכל `create` ה-factory מקבל שני דברים : ה-class שביקשו, והשם המלא של הרכיב החדש, כלומר
    השם של ההורה, נקודה, והשם שניתן ל-`create`. קודם הוא בודק את ה-instance overrides של
    ה-class, לפי סדר הרישום, ומשווה כל תבנית לשם המלא כולו. אם אף אחת לא מתאימה, הוא בודק אם
    יש type override. אם גם אין, הוא בונה את ה-class שביקשו.

    התבנית היא glob : ‏`*` מתאים לכל רצף, גם עם נקודות, ו-`?` לתו אחד. אבל היא חייבת להתאים
    לשם **כולו**, מההתחלה. `env.agt1.drv` הוא סוף השם, לא השם. ה-factory לא מתריע על תבנית
    שלא התאימה לאף רכיב : מבחינתו זו רשומה שאף אחד לא ביקש.

    העץ והשמות שלו, אחרי התיקון :

    <!-- gen 4 -->

    <svg class="figure uv-fig" viewBox="0 0 480 232" style="max-width:30rem" role="img" aria-label="עץ הרכיבים : uvm_test_top, בתוכו env, בתוכו agt0 ו-agt1, ובכל אחד seqr ו-drv. ה-drv של agt1 נבנה כ-ErrDriver"><g class="uv-box is-cont"><rect x="6" y="6" width="468" height="220" rx="8"/><text x="14" y="23">uvm_test_top</text></g><g class="uv-box is-cont"><rect x="16" y="32" width="448" height="184" rx="8"/><text x="24" y="49">env</text></g><g class="uv-box is-cont"><rect x="26" y="58" width="208" height="148" rx="8"/><text x="34" y="75">agt0</text></g><g class="uv-box"><rect x="36" y="84" width="188" height="40" rx="6"/><text x="130" y="109" text-anchor="middle">seqr</text></g><g class="uv-box"><rect x="36" y="136" width="188" height="56" rx="6"/><text x="130" y="160" text-anchor="middle">drv</text><text x="130" y="178" text-anchor="middle">ParityDriver</text></g><g class="uv-box is-cont"><rect x="246" y="58" width="208" height="148" rx="8"/><text x="254" y="75">agt1</text></g><g class="uv-box"><rect x="256" y="84" width="188" height="40" rx="6"/><text x="350" y="109" text-anchor="middle">seqr</text></g><g class="uv-box uv-dut"><rect x="256" y="136" width="188" height="56" rx="6"/><text x="350" y="160" text-anchor="middle">drv</text><text x="350" y="178" text-anchor="middle">ErrDriver</text></g></svg>

    <!-- /gen -->

    ‏`build_phase` רץ מלמעלה למטה : קודם כל ה-`build_phase` של הטסט, אחר כך של ה-env, ורק אז
    של כל agent, שבו נבנה ה-driver. לכן ה-override צריך להיות בטבלה לפני ה-`build_phase` של
    ה-agent, וכל מקום ב-`build_phase` של הטסט טוב. ב-`connect_phase` העץ כבר שלם, והרשומה
    החדשה לא משנה רכיב שכבר קיים.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מה נבנה :** הלוג אומר ש-`uvm_test_top.env.agt1.drv` הוא `ParityDriver`. זה השם
       המלא, כמו ש-`get_full_name()` מחזיר אותו.
    2. **מה נרשם :** ‏`uvm_factory().print(0)` ב-`end_of_elaboration_phase` מראה
       instance override בנתיב `env.agt1.drv`.
    3. **ההשוואה :** התבנית לא מתאימה לשם המלא, כי חסר לה בהתחלה `uvm_test_top` והנקודה שאחריו.
    4. **התיקון :** הנתיב נבנה מ-`get_full_name()` של הטסט, ולא נכתב ביד. כך גם שינוי בשם
       של הטסט לא שובר אותו.
    5. **הבדיקה :** אחרי התיקון `agt0.drv` הוא `ParityDriver` עם 0 שגיאות, ו-`agt1.drv` הוא
       `ErrDriver` עם 2.

    </div>

    הלוג של העמית, עם ההדפסה של ה-factory :

    <!-- gen 5 -->

    ```text
    --- overrides ---

    Overrides:
    ParityDriver             : Type Override: None       || Instance Overrides: env.agt1.drv => ErrDriver

    uvm_test_top.env.agt0.drv: ParityDriver, 0 parity errors
    uvm_test_top.env.agt1.drv: ParityDriver, 0 parity errors
    ```

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="Chan1Test" hl_lines="5 6 10"
        class Chan1Test(ErrTest):
            """Wrong parity bits on channel 1 only."""

            def build_phase(self):
                path = f"{self.get_full_name()}.env.agt1.drv"   # (1)!
                uvm_factory().set_inst_override_by_type(ParityDriver, ErrDriver, path)
                self.env = Env.create("env", self)

            def end_of_elaboration_phase(self):
                uvm_factory().print(0)   # (2)!
        ```

        1. ‏pyuvm מתאים את הנתיב עם `fnmatch` של Python, ותמיד מול השם המלא. אין ל-`uvm_component`
           שלו פונקציה עם נתיב יחסי, כמו ב-SystemVerilog.
        2. ‏0 מדפיס רק את ה-overrides. כדי לשאול על נתיב אחד :
           `uvm_factory().find_override_by_type(ParityDriver, "uvm_test_top.env.agt1.drv")`
           מחזיר את ה-class שה-factory היה בונה שם.

    === "SystemVerilog"
        ```systemverilog title="class chan1_test" hl_lines="8 9 14"
        class chan1_test extends err_test;
          `uvm_component_utils(chan1_test)
          function new(string name, uvm_component parent);
            super.new(name, parent);
          endfunction
          function void build_phase(uvm_phase phase);
            uvm_factory factory = uvm_factory::get();
            string path = {get_full_name(), ".env.agt1.drv"};   // (1)!
            factory.set_inst_override_by_type(parity_driver::get_type(), err_driver::get_type(), path);
            env = tb_env::type_id::create("env", this);
          endfunction
          function void end_of_elaboration_phase(uvm_phase phase);
            uvm_factory factory = uvm_factory::get();
            factory.print(0);   // (2)!
          endfunction
        endclass
        ```

        1. ה-factory מקבל נתיב מלא. ל-`uvm_component` יש גם
           `set_inst_override_by_type("env.agt1.drv", parity_driver::get_type(), err_driver::get_type())`,
           עם נתיב **יחסי** לרכיב שקורא לו (והנתיב ראשון), וכך גם
           `parity_driver::type_id::set_inst_override(err_driver::get_type(), "env.agt1.drv", this)`.
           אצלם הנתיב של העמית היה עובד. ב-pyuvm אין את שתי הצורות האלה.
        2. כדי לשאול על נתיב אחד :
           `factory.debug_create_by_type(parity_driver::get_type(), "uvm_test_top.env.agt1", "drv")`
           מדפיס מה היה נבנה שם ולמה. ‏`uvm_top.print_topology()` מדפיס את העץ עם השמות.

    #### למה זה נכון { .sol-proof }

    כל שורה בטבלאות היא ריצה של הסביבה המתוקנת מסעיף א, עם ה-instance override של השורה. בכל
    ריצה ה-DUT ספר 2 שגיאות בערוץ של כל `ErrDriver`, ו-0 בערוץ של `ParityDriver`. קודם
    נתיבים, כולם ב-`build_phase` של הטסט :

    <!-- gen 6 -->

    | הנתיב | מי נבנה כ-`ErrDriver` |
    |---|---|
    | ‏`uvm_test_top.env.agt1.drv` | רק `agt1` |
    | ‏`env.agt1.drv` | אף אחד |
    | ‏`uvm_test_top.env.agt1` | אף אחד |
    | ‏`*.agt1.*` | רק `agt1` |
    | ‏`uvm_test_top.env.agt*.drv` | **שניהם** |

    <!-- /gen -->

    ואחר כך הנתיב המלא, `uvm_test_top.env.agt1.drv`, בזמנים אחרים :

    <!-- gen 7 -->

    | מתי נקבע | מי נבנה כ-`ErrDriver` |
    |---|---|
    | ‏`build_phase`, לפני `Env.create` | רק `agt1` |
    | ‏`build_phase`, אחרי `Env.create` | רק `agt1` |
    | ‏`connect_phase` | אף אחד |
    | לפני `run_test` | אף אחד |

    <!-- /gen -->

    - **בלי `uvm_test_top` :** התבנית צריכה להתאים לשם כולו, ו-`env.agt1.drv` הוא רק סופו.
    - **הנתיב של ה-agent :** ה-override חל על מה שנבנה **בנתיב** הזה. ב-`uvm_test_top.env.agt1`
      נבנה `Agent`, לא `ParityDriver`, ולכן הרשומה לא נוגעת לאף רכיב.
    - **תבניות :** ‏`*.agt1.*` מתאים רק לרכיבים בתוך `agt1`, ו-`agt*` מתאים לשני ה-agents.
    - **אחרי `Env.create` :** עדיין עובד. ‏`Env.create` מפעיל רק את הבנאי של ה-env, וה-driver
      נבנה שתי רמות למטה, ב-`build_phase` של ה-agent, אחרי שה-`build_phase` של הטסט הסתיים.
    - **‏`connect_phase` :** מאוחר. אותו נתיב בדיוק, אבל ה-drivers נבנו כבר ב-`build_phase`.
    - **לפני `run_test` :** ייחודי ל-pyuvm : ‏`run_test` מנקה את ה-overrides לפני שהוא בונה את
      הטסט. ב-SystemVerilog, override שנקבע ב-`initial` של ה-top לפני `run_test` נשאר.

    **‏type ו-instance יחד.** כשיש לטיפוס שני ה-overrides, ה-instance override קובע בנתיבים שהוא
    מתאים להם, וה-type override בכל השאר. ריצה עם type override ל-`ErrDriver` ועם instance
    override של `agt0.drv` ל-class שלישי בונה את ה-class השלישי ב-`agt0` ואת `ErrDriver` ב-`agt1`.
    ‏`Chan1Test` כותב את `build_phase` מחדש ולא קורא ל-`super().build_phase()`, ולכן ה-type override
    של `ErrTest` לא נקבע בו. אילו נקבע, גם `agt0` היה מקבל `ErrDriver`.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : ‏`new` אחד בעומק העץ"
    מספיק `new` אחד, ב-agent שמישהו כתב פעם, כדי שאף override לא יגיע לרכיב הזה, ואין שום
    שגיאה. אותו דבר ל-sequence item : אם ה-sequence בונה את ה-item ב-`new`, ‏override של ה-item
    (למשל item עם constraints שמייצרים שגיאות) לא נכנס לתוקף. ב-code review מחפשים `new(` של
    רכיבים ו-items מחוץ לבנאים עצמם.

??? trap "מלכודת : ה-override עבד, והשגיאות עדיין לא שם"
    ב-SystemVerilog, אם `parity` של `parity_driver` לא מוגדרת `virtual`, הקריאה `parity(req.data)`
    בתוך `run_phase` של ה-class הבסיסי קוראת לגרסה הבסיסית גם באובייקט של `err_driver`. הלוג
    יראה `err_driver`, וה-DUT 0 שגיאות. ב-Python כל מתודה היא virtual, ולכן אין שם את
    המלכודת הזו.

??? trap "מלכודת : ‏override לפני `run_test` ב-pyuvm"
    ב-pyuvm, ‏`run_test` מנקה את ה-overrides ואת `ConfigDB` (אלא אם `keep_singletons=True`). מה
    שנקבע בבדיקת ה-cocotb לפני הקריאה נמחק בשקט. את ה-overrides קובעים ב-`build_phase` של
    הטסט.

??? followup "שאלות המשך"
    - **למה לא פשוט לשנות את ה-agent :** למה לא לכתוב ב-agent `ErrDriver.create(...)`, או
      להוסיף ל-`ParityDriver` דגל `inject_errors`?

        ??? fu-answer "תשובה"
            ה-agent משותף לכל הטסטים ולפעמים לפרויקטים אחרים. override משאיר אותו נקי,
            והטסט בוחר. דגל ב-`ConfigDB` הוא גם דרך לגיטימית, אבל הוא מכניס לכל driver קוד
            של כל טסט.

    - **שני instance overrides :** מה קורה אם שני instance overrides מתאימים לאותו נתיב?

        ??? fu-answer "תשובה"
            הראשון שנרשם קובע, גם ב-pyuvm וגם ב-SystemVerilog. לכן רושמים קודם את התבנית
            הספציפית, ואחריה את הכללית.

    - **‏override של override :** ‏`A` מוחלף ב-`B`, ו-`B` מוחלף ב-`C`. מה נבנה כשמבקשים `A`?

        ??? fu-answer "תשובה"
            ‏`C` : ה-factory ממשיך לחפש override גם ל-class שמצא, עד class שאין לו override.
            לולאה (`A` ל-`B` ו-`B` ל-`A`) ‏pyuvm מזהה, ומדפיס שגיאה במקום להיתקע.

    - **‏override של sequence item :** איך הייתם מזריקים את אותן שגיאות בלי לגעת ב-driver?

        ??? fu-answer "תשובה"
            ‏item עם שדה `bad_parity`, ותת-class שלו שמדליק אותו, ו-type override של ה-item.
            זה עובד רק אם ה-sequence בונה את ה-items ב-`create`, וה-driver קורא את השדה.
