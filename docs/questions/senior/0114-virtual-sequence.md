---
id: 114
title: סנכרון שני agents ב-virtual sequence
level: senior
difficulty: hard
kind: dv
tags: [uvm, methodology, protocols, python, systemverilog]
source: ""
added: 2026-11-20
---

## השאלה

ה-DUT הוא `pkt_xor` : בלוק שמצפין חבילות ב-XOR עם מפתח. יש לו שני ממשקים, ולכל אחד agent
משלו בסביבה :

- **ממשק ההגדרות :** כתיבה לרגיסטר במחזור שבו `cfg_valid` גבוה. ‏`CTRL` (כתובת 0) מחזיק את
  `enable` בביט 0, ו-`KEY` (כתובת 1) את המפתח. האפיק מקבל כתיבה אחת בכל שלושה מחזורים.
- **ממשק החבילות :** בייט בכל מחזור, ו-`in_last` על הבייט האחרון של החבילה. כל בייט יוצא
  במחזור הבא, אחרי XOR עם `key`.

לבלוק שני כללים. חבילה שהבייט הראשון שלה מגיע כש-`enable` נמוך נזרקת כולה, והמונה `drops`
סופר אותה. ואת `KEY` ו-`CTRL` מותר לשנות רק בין חבילות :

```systemverilog title="module pkt_xor" linenums="1"
module pkt_xor (
  input  logic       clk,
  input  logic       rst_n,
  input  logic       cfg_valid,      // a register write
  input  logic       cfg_addr,       // 0: CTRL (bit 0 = enable), 1: KEY
  input  logic [7:0] cfg_data,
  input  logic       in_valid,       // a packet: one byte a cycle, in_last on its last byte
  input  logic       in_last,
  input  logic [7:0] in_data,
  output logic       out_valid,
  output logic       out_last,
  output logic [7:0] out_data,
  output logic [7:0] drops           // packets dropped because the block was disabled
);
  logic       enable, mid, keep;
  logic [7:0] key;
  wire        pass = mid ? keep : enable;   // the first byte decides for the whole packet

  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) begin
      {enable, mid, keep, key, out_valid, out_last, out_data, drops} <= '0;
    end else begin
      if (cfg_valid) begin
        if (cfg_addr) key    <= cfg_data;
        else          enable <= cfg_data[0];
      end
      out_valid <= in_valid && pass;
      out_last  <= in_last;
      out_data  <= in_data ^ key;
      if (in_valid) begin
        mid  <= !in_last;
        keep <= pass;
        if (!mid && !enable) drops <= drops + 1;
      end
    end
endmodule
```

הסביבה בנויה כמו בשאלה [0049](../junior/0049-uvm-testbench-architecture.md), עם שני agents
פעילים ו-virtual sequencer שמחזיק handles ל-sequencers של שניהם. ה-checker מסתכל על כל הפינים :
הוא מנבא כל חבילה לפי הרגיסטרים שנכתבו, משווה ליציאה, ומדווח על כתיבה באמצע חבילה. בסוף הטסט
כל חבילה ששלחנו צריכה לצאת :

<!-- gen 0 -->

<svg class="figure uv-fig" viewBox="0 0 500 440" style="max-width:32rem" role="img" aria-label="הסביבה : virtual sequence על virtual sequencer שמחזיק handles לשני sequencers, של reg_agent ושל pkt_agent; שני drivers מחוברים ל-pkt_xor, ו-checker מסתכל על הפינים"><defs><marker id="vs-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs><g class="uv-box is-cont uv-test"><rect x="6" y="6" width="488" height="340" rx="8"/><text x="14" y="23">test</text></g><g class="uv-box is-cont uv-env"><rect x="14" y="76" width="472" height="262" rx="8"/><text x="22" y="93">env</text></g><g class="uv-box is-cont uv-reg_agent"><rect x="24" y="156" width="170" height="172" rx="8"/><text x="32" y="173">reg_agent</text></g><g class="uv-box is-cont uv-pkt_agent"><rect x="306" y="156" width="170" height="172" rx="8"/><text x="468" y="173" text-anchor="end">pkt_agent</text></g><line class="uv-arrow uv-tlm" x1="250.0" y1="60.0" x2="250.0" y2="98.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow stream-c" x1="215.4" y1="136.0" x2="131.7" y2="182.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow stream-c" x1="284.6" y1="136.0" x2="368.3" y2="182.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow uv-tlm" x1="99.0" y1="218.0" x2="99.0" y2="276.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow uv-tlm" x1="401.0" y1="218.0" x2="401.0" y2="276.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow uv-pin" x1="124.6" y1="312.0" x2="210.1" y2="372.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow uv-pin" x1="375.4" y1="312.0" x2="289.9" y2="372.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow uv-pin" x1="250.0" y1="372.0" x2="250.0" y2="312.0" marker-end="url(#vs-arrow)"/><g class="uv-box uv-vseq"><rect x="167" y="28" width="166" height="32" rx="6"/><text x="250.0" y="49.0" text-anchor="middle">virtual sequence</text></g><g class="uv-box uv-vseqr"><rect x="160" y="98" width="180" height="38" rx="6"/><text x="250.0" y="122.0" text-anchor="middle">virtual sequencer</text></g><g class="uv-box uv-reg_seqr"><rect x="44" y="182" width="110" height="36" rx="6"/><text x="99.0" y="205.0" text-anchor="middle">sequencer</text></g><g class="uv-box uv-reg_drv"><rect x="44" y="276" width="110" height="36" rx="6"/><text x="99.0" y="299.0" text-anchor="middle">driver</text></g><g class="uv-box uv-pkt_seqr"><rect x="346" y="182" width="110" height="36" rx="6"/><text x="401.0" y="205.0" text-anchor="middle">sequencer</text></g><g class="uv-box uv-pkt_drv"><rect x="346" y="276" width="110" height="36" rx="6"/><text x="401.0" y="299.0" text-anchor="middle">driver</text></g><g class="uv-box uv-checker"><rect x="200" y="276" width="100" height="36" rx="6"/><text x="250.0" y="299.0" text-anchor="middle">checker</text></g><g class="uv-box uv-dut"><rect x="165" y="372" width="170" height="56" rx="6"/><text x="250.0" y="405.0" text-anchor="middle">pkt_xor</text></g></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="uv-key-tlm"></i>פריטים : start ו-seq_item_port</span><span><i class="by-bfs"></i>מצביע ל-sequencer, נקבע ב-connect_phase</span><span><i class="uv-key-pin"></i>אותות</span></span>

<!-- /gen -->

??? example "הסביבה המלאה ב-pyuvm, כמו שהיא רצה על Verilator"
    ```python title="the environment" linenums="1"
    import cocotb
    import pyuvm
    from cocotb.clock import Clock
    from cocotb.triggers import ClockCycles, Event, FallingEdge, RisingEdge
    from pyuvm import *

    CTRL, KEY = 0, 1                       # the two registers
    PACKETS, LENGTH = 8, 3                 # the traffic: 8 packets of 3 bytes


    class RegWrite(uvm_sequence_item):
        def __init__(self, name="write", addr=CTRL, data=0):
            super().__init__(name)
            self.addr, self.data = addr, data


    class Packet(uvm_sequence_item):
        def __init__(self, name="packet", data=()):
            super().__init__(name)
            self.data = list(data)


    class ConfigSeq(uvm_sequence):
        """Register writes in order: by default the key, then enable."""
        def __init__(self, name="config", writes=((KEY, 0x5A), (CTRL, 1))):
            super().__init__(name)
            self.writes = writes

        async def body(self):
            for addr, data in self.writes:
                w = RegWrite("write", addr, data)
                await self.start_item(w)
                await self.finish_item(w)


    class TrafficSeq(uvm_sequence):
        """PACKETS packets of LENGTH bytes; packet k holds 16k, 16k + 1, ..."""
        async def body(self):
            for k in range(PACKETS):
                await self.send(k)

        async def send(self, k):
            p = Packet(f"p{k}", [16 * k + i for i in range(LENGTH)])
            await self.start_item(p)
            await self.finish_item(p)


    class RegDriver(uvm_driver):
        async def run_phase(self):
            dut = cocotb.top
            while True:
                w = await self.seq_item_port.get_next_item()
                dut.cfg_valid.value, dut.cfg_addr.value, dut.cfg_data.value = 1, w.addr, w.data
                await RisingEdge(dut.clk)
                dut.cfg_valid.value = 0
                await ClockCycles(dut.clk, 2)  # the bus takes one write every three cycles
                self.seq_item_port.item_done()


    class PktDriver(uvm_driver):
        async def run_phase(self):
            dut = cocotb.top
            while True:
                p = await self.seq_item_port.get_next_item()
                for i, byte in enumerate(p.data):
                    dut.in_valid.value, dut.in_last.value, dut.in_data.value = 1, int(i == len(p.data) - 1), byte
                    await RisingEdge(dut.clk)
                dut.in_valid.value = 0
                self.seq_item_port.item_done()


    class Agent(uvm_agent):
        driver = None                      # the subclass names its driver

        def build_phase(self):
            self.seqr = uvm_sequencer("seqr", self)
            self.drv = self.driver.create("drv", self)

        def connect_phase(self):
            self.drv.seq_item_port.connect(self.seqr.seq_item_export)


    class RegAgent(Agent):
        driver = RegDriver


    class PktAgent(Agent):
        driver = PktDriver


    class VirtualSequencer(uvm_sequencer):
        """No driver: only the handles of the two agents' sequencers."""
        def __init__(self, name, parent):
            super().__init__(name, parent)
            self.reg_seqr = self.pkt_seqr = None


    def hexes(data):
        return " ".join(f"{b:02x}" for b in data)


    class Checker(uvm_component):
        """Predicts every packet from the input pins and compares the output pins, in order."""
        def build_phase(self):
            self.sent = self.out = self.dropped = 0
            self.errors = []

        def error(self, cycle, msg):
            self.errors.append(f"cycle {cycle}: {msg}")
            self.logger.error(self.errors[-1])

        async def run_phase(self):
            dut = cocotb.top
            enable = key = 0                   # the model of the two registers
            pkt, expected, got, cycle = None, [], [], -1
            while True:
                await FallingEdge(dut.clk)     # mid-cycle: what the next rising edge samples
                if not dut.rst_n.value:
                    continue
                cycle += 1
                if dut.out_valid.value:        # the output, a cycle behind the input
                    got.append(int(dut.out_data.value))
                    if dut.out_last.value:
                        k, want = expected.pop(0)
                        self.out += 1
                        if got != want:
                            self.error(cycle, f"packet {k} came out {hexes(got)}, expected {hexes(want)}")
                        got = []
                if dut.in_valid.value:
                    if pkt is None:            # the first byte: kept or dropped, and its key
                        pkt = (self.sent, enable, key, [])
                    pkt[3].append(int(dut.in_data.value) ^ pkt[2])
                    if dut.in_last.value:
                        k, keep, _, data = pkt
                        self.sent += 1
                        if keep:
                            expected.append((k, data))
                        else:
                            self.dropped += 1
                        pkt = None
                if dut.cfg_valid.value:
                    if pkt is not None:
                        self.error(cycle, f"a register write during packet {pkt[0]}")
                    if dut.cfg_addr.value:
                        key = int(dut.cfg_data.value)
                    else:
                        enable = int(dut.cfg_data.value) & 1


    class Env(uvm_env):
        def build_phase(self):
            self.reg_agent = RegAgent.create("reg_agent", self)
            self.pkt_agent = PktAgent.create("pkt_agent", self)
            self.vseqr = VirtualSequencer.create("vseqr", self)
            self.checker = Checker.create("checker", self)

        def connect_phase(self):
            self.vseqr.reg_seqr = self.reg_agent.seqr
            self.vseqr.pkt_seqr = self.pkt_agent.seqr


    class BaseTest(uvm_test):
        vseq = None                        # the subclass names its virtual sequence

        def build_phase(self):
            self.env = Env.create("env", self)

        async def run_phase(self):
            self.raise_objection()
            dut = cocotb.top
            for s in (dut.cfg_valid, dut.cfg_addr, dut.cfg_data, dut.in_valid, dut.in_last, dut.in_data):
                s.value = 0
            dut.rst_n.value = 0
            cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
            await ClockCycles(dut.clk, 2)
            dut.rst_n.value = 1
            await self.vseq("vseq").start(self.env.vseqr)
            await ClockCycles(dut.clk, 3)      # the last packet leaves the DUT
            self.drop_objection()

        def check_phase(self):
            c, drops = self.env.checker, int(cocotb.top.drops.value)
            self.logger.info(f"{c.sent} packets in, {c.out} out, {drops} dropped, {len(c.errors)} errors")
            assert drops == c.dropped, "the DUT and the model disagree on the dropped packets"
            assert c.out == c.sent and not c.errors, "packets were lost or changed"
    ```

ה-virtual sequence של הטסט הראשון מריץ את ההגדרה (המפתח 0x5A, ואחריו `enable`) ואת התנועה, 8
חבילות של 3 בייטים, במקביל :

=== "Python"
    ```python title="BootVseq" hl_lines="3 4"
    class BootVseq(uvm_sequence):
        async def body(self):
            cfg = cocotb.start_soon(ConfigSeq("boot").start(self.sequencer.reg_seqr))
            await TrafficSeq("traffic").start(self.sequencer.pkt_seqr)
            await cfg


    @pyuvm.test()
    class BootTest(BaseTest):
        vseq = BootVseq
    ```

=== "SystemVerilog"
    ```systemverilog title="class boot_vseq" hl_lines="12 13 14"
    class boot_vseq extends uvm_sequence;
      `uvm_object_utils(boot_vseq)
      `uvm_declare_p_sequencer(virtual_sequencer)

      function new(string name = "boot_vseq");
        super.new(name);
      endfunction

      task body();
        config_seq  cfg     = config_seq::type_id::create("boot");
        traffic_seq traffic = traffic_seq::type_id::create("traffic");
        fork
          cfg.start(p_sequencer.reg_seqr, this);
          traffic.start(p_sequencer.pkt_seqr, this);
        join
      endtask
    endclass
    ```

ה-SystemVerilog של UVM לא רץ בטסטים של האתר, כי ל-Verilator אין ספריית UVM. גרסת הפייתון
(pyuvm על Verilator) רצה, והטסטים בודקים שה-SV מקביל לה : אותן מחלקות ואותו סדר של קריאות.

הטסט נכשל :

```text title="BootTest"
ERROR  cycle 0: a register write during packet 0
ERROR  cycle 3: a register write during packet 1
INFO   8 packets in, 6 out, 2 dropped, 2 errors
FAIL   AssertionError: packets were lost or changed
```

- **סעיף א – הסדר :** למה שתי חבילות נזרקו, ולמה ה-checker מדווח על כתיבות באמצע חבילה?
  תקנו את ה-virtual sequence. מאיפה הוא מקבל את שני ה-sequencers?
- **סעיף ב – מפתח חדש באמצע התנועה :** טסט אחר מחליף את המפתח בזמן שהתנועה רצה (הקוד והלוג
  בסעיף). איך מסנכרנים כך שההחלפה תיפול בין שתי חבילות?
- **סעיף ג – lock, ‏grab ו-arbitration :** על sequencer אחד רצים שני זרמי תנועה, A ו-B, ו-sequence
  דחוף I ששולח שלושה פריטים שאסור שייכנס ביניהם פריט אחר. מה ה-driver מקבל, ומה משנים
  עדיפות, `lock()` ו-`grab()`?

??? interviewer "מה המראיין בודק"
    - **מי קובע את הסדר :** האם המועמד יודע שאין שום סדר בין פריטים של שני sequencers, ושה-virtual
      sequence הוא המקום היחיד שקובע אותו. ‏`fork` הוא החלטה שאין סדר.
    - **נקודת סנכרון אמיתית :** האם הוא מחליף "מספר מחזורים" בלחיצת יד עם מי שיודע איפה נגמרת
      חבילה, ויודע מתי `start()` של sequence חוזר.
    - **עדיפות, lock ו-grab :** האם הוא מבדיל בין "לנצח בבחירה הבאה", "להחזיק את ה-sequencer עד
      שמשחררים" ו"לעקוף את התור", ויודע שב-FIFO, ברירת המחדל, העדיפות לא משנה כלום.
    - **הבדיקה שתופסת :** האם ה-checker בודק גם את הכלל של הממשק (כתיבה רק בין חבילות) ואת
      הכוונה של הטסט (כל חבילה יוצאת), ולא רק השוואה של נתונים.

---

### סעיף א – הסדר

??? tip "רמז 1"
    באיזה מחזור עולה `enable`, ובאיזה מחזור מתחילה כל אחת מהחבילות הראשונות? זכרו שהאפיק
    מקבל כתיבה אחת בכל שלושה מחזורים.

??? tip "רמז 2"
    ‏`fork` מתחיל את שני ה-sequences באותו רגע. מה היה מבטיח שההגדרה הסתיימה לפני שהבייט
    הראשון יוצא, ומתי `start()` חוזר?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ב-`fork` שני ה-sequences מתחילים במחזור 0. המפתח נכתב במחזור 0 ו-`enable` במחזור 3,
        ולכן הבלוק פועל רק ממחזור 4. חבילות 0 ו-1 התחילו במחזורים 0 ו-3 ונזרקו, ושתי הכתיבות
        נפלו באמצע שלהן. התיקון : לחכות ל-`start()` של ההגדרה ורק אז להתחיל את התנועה, בלי
        `fork`. ה-handles מגיעים מה-virtual sequencer, שה-env ממלא ב-`connect_phase`. אחרי
        התיקון : `8 packets in, 8 out, 0 dropped, 0 errors`.

    #### הרעיון { .sol-idea }

    כל sequencer מסדר רק את הפריטים שלו. אין ב-UVM שום מנגנון שמסדר פריט של ה-agent של
    ההגדרות מול פריט של ה-agent של החבילות : שני ה-drivers רצים במקביל, כל אחד בקצב שלו. מי
    שיודע שההגדרה צריכה לבוא קודם הוא ה-virtual sequence, והוא אומר את זה בסדר של הקריאות.
    ‏`start()` חוזר כשה-`body()` של ה-sequence נגמר, כלומר אחרי ה-`item_done` של הכתיבה
    האחרונה, וזו נקודת הסנכרון.

    שימו לב שה-DUT לא שבור : הוא זרק בדיוק את מה שהכלל שלו אומר, וה-checker מנבא את אותן
    שתי זריקות. מה שנכשל הוא הכוונה של הטסט, שכל חבילה תצא, והכלל שכתיבה מותרת רק בין
    חבילות. בלי שתי הבדיקות האלה, טסט כזה עובר עם 6 חבילות במקום 8 ואף אחד לא שם לב.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **קוראים את הלוג :** שתי חבילות נזרקו ושתי כתיבות נפלו באמצע חבילה : התנועה רצה לפני
       שההגדרה הסתיימה.
    2. **הזמנים :** המפתח במחזור 0, ‏`CTRL` במחזור 3, ו-`enable` עולה בקצה שבסוף מחזור 3.
       חבילה 0 תופסת את מחזורים 0 עד 2 וחבילה 1 את 3 עד 5 : שתיהן מתחילות כש-`enable` עוד 0.
    3. **התיקון :** ‏`await` על ה-`start()` של ההגדרה, ורק אחריו `start()` של התנועה.
    4. **ה-handles :** ה-virtual sequencer מחזיק את `reg_seqr` ו-`pkt_seqr`, וה-env מחבר
       אותם ב-`connect_phase`. ב-SV ה-sequence ניגש אליהם דרך `p_sequencer`.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="BootVseqFixed" hl_lines="3 4"
        class BootVseqFixed(uvm_sequence):
            async def body(self):
                await ConfigSeq("boot").start(self.sequencer.reg_seqr)   # (1)!
                await TrafficSeq("traffic").start(self.sequencer.pkt_seqr)


        @pyuvm.test()
        class BootTestFixed(BaseTest):
            vseq = BootVseqFixed
        ```

        1. ‏`self.sequencer` הוא ה-sequencer שה-virtual sequence הופעל עליו, ה-`VirtualSequencer`
           של הסביבה. ב-pyuvm אין `p_sequencer`, וה-handle נגיש ישירות.

    === "SystemVerilog"
        ```systemverilog title="class boot_vseq_fixed" linenums="1" hl_lines="3 4 24 25"
        class virtual_sequencer extends uvm_sequencer;
          `uvm_component_utils(virtual_sequencer)
          uvm_sequencer #(reg_write) reg_seqr;   // set by env::connect_phase
          uvm_sequencer #(packet)    pkt_seqr;

          function new(string name, uvm_component parent);
            super.new(name, parent);
          endfunction
        endclass

        // env::connect_phase: vseqr.reg_seqr = reg_agent.seqr; vseqr.pkt_seqr = pkt_agent.seqr;

        class boot_vseq_fixed extends uvm_sequence;
          `uvm_object_utils(boot_vseq_fixed)
          `uvm_declare_p_sequencer(virtual_sequencer)   // (1)!

          function new(string name = "boot_vseq_fixed");
            super.new(name);
          endfunction

          task body();
            config_seq  cfg     = config_seq::type_id::create("boot");
            traffic_seq traffic = traffic_seq::type_id::create("traffic");
            cfg.start(p_sequencer.reg_seqr, this);   // returns after the last write's item_done
            traffic.start(p_sequencer.pkt_seqr, this);
          endtask
        endclass
        ```

        1. המאקרו מגדיר את `p_sequencer` מהטיפוס `virtual_sequencer`, ומבצע cast מ-`m_sequencer`
           כשה-sequence מתחיל. בלעדיו אין גישה ל-`reg_seqr` ול-`pkt_seqr`.

    #### למה זה נכון { .sol-proof }

    המחזורים הראשונים של הריצה עם ה-`fork`, מהפינים של Verilator. ‏`drops` עולה ל-1 אחרי הבייט
    הראשון של חבילה 0 ול-2 אחרי הבייט הראשון של חבילה 1, ו-`out_valid` עולה לראשונה במחזור 7,
    הבייט הראשון של חבילה 2 :

    <!-- gen 2 -->

    ```wavedrom
    { signal: [
      { name: "clk",       wave: "p......." },
      { name: "cycle",     wave: "========", data: ["0", "1", "2", "3", "4", "5", "6", "7"] },
      { name: "cfg",       wave: "=z.=z...", data: ["KEY", "CTRL"] },
      { name: "enable",    wave: "0...1..." },
      { name: "in_valid",  wave: "1......." },
      { name: "in_data",   wave: "========", data: ["00", "01", "02", "10", "11", "12", "20", "21"] },
      { name: "in_last",   wave: "0.10.10." },
      { name: "drops",     wave: "==..=...", data: ["0", "1", "2"] },
      { name: "out_valid", wave: "0......1" }
    ]}
    ```

    <!-- /gen -->

    - **הכתיבות באמצע חבילה :** הכתיבה של המפתח, במחזור 0, נופלת עם הבייט הראשון של חבילה 0,
      ו-`CTRL`, במחזור 3, עם הבייט הראשון של חבילה 1. ה-checker מדווח על שתיהן.
    - **אחרי התיקון :** ההגדרה תופסת את מחזורים 0 עד 5, והחבילה הראשונה מתחילה במחזור 6,
      כש-`enable` כבר 1. כל 8 החבילות יוצאות, בלי שגיאות, והטסט עובר. המחיר הוא 6 מחזורים
      של המתנה בהתחלה : 33 מחזורים במקום 27.

---

### סעיף ב – מפתח חדש באמצע התנועה

הטסט השני מגדיר את הבלוק, מתחיל את התנועה ברקע, ו-10 מחזורים אחרי שהיא התחילה מחליף את
המפתח ל-0xC3. התנועה לא אמורה להיעצר לפני הזמן, ואי אפשר לדעת מראש באיזה מחזור נגמרת
חבילה :

=== "Python"
    ```python title="RekeyVseq" hl_lines="8 9 10"
    REKEY_AT = 10                          # cycles after the traffic starts


    class RekeyVseq(uvm_sequence):
        async def body(self):
            seqr = self.sequencer
            await ConfigSeq("boot").start(seqr.reg_seqr)
            traffic = cocotb.start_soon(TrafficSeq("traffic").start(seqr.pkt_seqr))
            await ClockCycles(cocotb.top.clk, REKEY_AT)
            await ConfigSeq("rekey", [(KEY, 0xC3)]).start(seqr.reg_seqr)
            await traffic


    @pyuvm.test()
    class RekeyTest(BaseTest):
        vseq = RekeyVseq
    ```

=== "SystemVerilog"
    ```systemverilog title="class rekey_vseq" linenums="1" hl_lines="17 20"
    class rekey_vseq extends uvm_sequence;
      `uvm_object_utils(rekey_vseq)
      `uvm_declare_p_sequencer(virtual_sequencer)
      int rekey_at = 10;                      // cycles of 10 ns after the traffic starts

      function new(string name = "rekey_vseq");
        super.new(name);
      endfunction

      task body();
        config_seq  boot    = config_seq::type_id::create("boot");
        config_seq  rekey   = config_seq::type_id::create("rekey");
        traffic_seq traffic = traffic_seq::type_id::create("traffic");
        rekey.writes = '{'{KEY, 8'hC3}};
        boot.start(p_sequencer.reg_seqr, this);
        fork
          traffic.start(p_sequencer.pkt_seqr, this);
        join_none
        #(rekey_at * 10ns);
        rekey.start(p_sequencer.reg_seqr, this);
        wait fork;
      endtask
    endclass
    ```

והלוג :

```text title="RekeyTest"
ERROR  cycle 16: a register write during packet 3
ERROR  cycle 18: packet 3 came out 6a 6b f1, expected 6a 6b 68
INFO   8 packets in, 8 out, 0 dropped, 2 errors
FAIL   AssertionError: packets were lost or changed
```

מה קרה, ואיך גורמים להחלפה ליפול בין שתי חבילות?

??? tip "רמז 1"
    ה-sequencer של ההגדרות לא יודע כלום על החבילות. מי בסביבה יודע מתי חבילה אחת נגמרה
    והבאה עוד לא התחילה?

??? tip "רמז 2"
    ה-sequence של התנועה עובר בין חבילות בנקודה אחת בקוד : אחרי `finish_item` של חבילה ולפני
    `start_item` של הבאה. מה אם הוא ישאל שם "ביקשו ממני לעצור"?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        הכתיבה יצאה במחזור 16, באמצע חבילה 3 (מחזורים 15 עד 17), והבייט האחרון שלה הוצפן
        במפתח החדש : ‏f1 במקום 68. ‏10 מחזורים הם זמן, לא גבול של חבילה. התיקון : לחיצת יד.
        ה-virtual sequence מבקש לעצור (`pause.request()`), ה-sequence של התנועה בודק את
        הבקשה לפני כל חבילה ועוצר שם, וה-virtual sequence כותב את המפתח וממשיך את התנועה
        (`pause.resume()`). המפתח נכתב במחזור 18, אחרי חבילה 3, והתנועה ממשיכה במחזור 21 :
        `8 packets in, 8 out, 0 dropped, 0 errors`.

    #### הרעיון { .sol-idea }

    רק ה-sequence של התנועה יודע איפה הגבול בין חבילות : בין `finish_item` של חבילה לבין
    `start_item` של הבאה. לכן הסנכרון הוא בקשה ותשובה. ה-virtual sequence מבקש, התנועה עוצרת
    בגבול הבא ומודיעה שעצרה, ה-virtual sequence עושה את השינוי ומשחרר. אף צד לא צריך לדעת
    כמה זמן לוקחת חבילה או כתיבה.

    שני הדגלים הם **מצב**, לא אירוע רגעי. ‏`Event` של cocotb נשאר דלוק עד `clear()`, וב-SV
    ‏`wait (stopped)` בודק רמה. אם התנועה עוצרת לפני שה-virtual sequence מתחיל לחכות, ההודעה
    לא הולכת לאיבוד. עם `->` ו-`@` של SV היא הייתה יכולה ללכת לאיבוד, והטסט היה נתקע.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **האבחנה :** הכתיבה במחזור 16 נופלת בבייט השני של חבילה 3, והבייט השלישי, 32, יוצא
       כ-f1 (32 XOR c3) במקום 68 (32 XOR 5a).
    2. **הבקשה :** ‏`pause.request()` מדליק את `requested` ומחכה ל-`stopped`.
    3. **העצירה :** לפני כל חבילה התנועה קוראת ל-`pause.boundary()`. כשיש בקשה היא מדליקה את
       `stopped` ומחכה.
    4. **השינוי והשחרור :** ה-virtual sequence מריץ את הכתיבה, ו-`pause.resume()` מכבה את
       הבקשה ומשחרר את התנועה.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="Pause, PausableTraffic, RekeyVseqFixed" linenums="1" hl_lines="8 9 10 13 15 29 39 41"
        class Pause:
            """A stop between two packets, asked for by the virtual sequence."""
            def __init__(self):
                self.requested = False
                self.stopped, self.resumed = Event(), Event()

            async def boundary(self):          # the traffic, before each packet
                if self.requested:
                    self.stopped.set()
                    await self.resumed.wait()

            async def request(self):           # returns when the traffic stopped
                self.requested = True
                self.resumed.clear()
                await self.stopped.wait()

            def resume(self):
                self.requested = False
                self.stopped.clear()
                self.resumed.set()


        class PausableTraffic(TrafficSeq):
            def __init__(self, name, pause):
                super().__init__(name)
                self.pause = pause

            async def send(self, k):
                await self.pause.boundary()
                await super().send(k)


        class RekeyVseqFixed(uvm_sequence):
            async def body(self):
                seqr, pause = self.sequencer, Pause()
                await ConfigSeq("boot").start(seqr.reg_seqr)
                traffic = cocotb.start_soon(PausableTraffic("traffic", pause).start(seqr.pkt_seqr))
                await ClockCycles(cocotb.top.clk, REKEY_AT)
                await pause.request()                    # (1)!
                await ConfigSeq("rekey", [(KEY, 0xC3)]).start(seqr.reg_seqr)
                pause.resume()
                await traffic


        @pyuvm.test()
        class RekeyTestFixed(BaseTest):
            vseq = RekeyVseqFixed
        ```

        1. הבקשה במחזור 16. חבילה 3 עוד באמצע, והקריאה חוזרת רק אחרי הבייט האחרון שלה.

    === "SystemVerilog"
        ```systemverilog title="pause_c, pausable_traffic, rekey_vseq_fixed" linenums="1" hl_lines="5 6 7 12 13 31 55 57"
        class pause_c;
          bit requested, stopped;

          task boundary();                       // the traffic, before each packet
            if (requested) begin
              stopped = 1;
              wait (!requested);
            end
          endtask

          task request();                        // returns when the traffic stopped
            requested = 1;
            wait (stopped);
          endtask

          function void resume();
            requested = 0;
            stopped   = 0;
          endfunction
        endclass

        class pausable_traffic extends traffic_seq;
          `uvm_object_utils(pausable_traffic)
          pause_c pause;

          function new(string name = "pausable_traffic");
            super.new(name);
          endfunction

          task send(int k);                      // virtual in traffic_seq
            pause.boundary();
            super.send(k);
          endtask
        endclass

        class rekey_vseq_fixed extends rekey_vseq;
          `uvm_object_utils(rekey_vseq_fixed)

          function new(string name = "rekey_vseq_fixed");
            super.new(name);
          endfunction

          task body();
            pause_c          pause   = new();
            config_seq       boot    = config_seq::type_id::create("boot");
            config_seq       rekey   = config_seq::type_id::create("rekey");
            pausable_traffic traffic = pausable_traffic::type_id::create("traffic");
            traffic.pause = pause;
            rekey.writes  = '{'{KEY, 8'hC3}};
            boot.start(p_sequencer.reg_seqr, this);
            fork
              traffic.start(p_sequencer.pkt_seqr, this);
            join_none
            #(rekey_at * 10ns);
            pause.request();
            rekey.start(p_sequencer.reg_seqr, this);
            pause.resume();
            wait fork;
          endtask
        endclass
        ```

    #### למה זה נכון { .sol-proof }

    הריצה בלי לחיצת היד, במחזורים 14 עד 19 : הכתיבה במחזור 16, ‏`key` מתחלף בקצה שבסופו, והבייט
    32 של מחזור 17 יוצא במחזור 18 כ-f1. ה-checker, שלקח את המפתח בבייט הראשון של החבילה, מצפה
    ל-68 :

    <!-- gen 3 -->

    ```wavedrom
    { signal: [
      { name: "clk",       wave: "p....." },
      { name: "cycle",     wave: "======", data: ["14", "15", "16", "17", "18", "19"] },
      { name: "cfg",       wave: "z.=z..", data: ["KEY"] },
      { name: "key",       wave: "=..=..", data: ["5a", "c3"] },
      { name: "in_data",   wave: "======", data: ["22", "30", "31", "32", "40", "41"] },
      { name: "in_last",   wave: "10.10." },
      { name: "out_valid", wave: "1....." },
      { name: "out_data",  wave: "======", data: ["7b", "78", "6a", "6b", "f1", "83"] }
    ]}
    ```

    <!-- /gen -->

    - **עם לחיצת היד :** הבקשה במחזור 16. חבילה 3 נגמרת במחזור 17, התנועה עוצרת לפני חבילה 4,
      והכתיבה יוצאת במחזור 18, כשאין חבילה בדרך. האפיק תופס שלושה מחזורים, והתנועה ממשיכה
      במחזור 21 עם המפתח החדש. ה-checker לא מדווח כלום : חבילות 0 עד 3 במפתח 5a, ו-4 עד 7
      ב-c3.
    - **המחיר :** שלושה מחזורים בלי תנועה, 36 מחזורים במקום 33. עצירה בגבול של חבילה היא
      המחיר של הכלל של הבלוק, וכל דרך נכונה משלמת אותו.
    - **אם הבקשה מגיעה בין חבילות :** `boundary()` רואה אותה לפני החבילה הבאה, והכתיבה יוצאת
      מיד. אם התנועה כבר נגמרה, אף אחד לא יענה, ו-`request()` יחכה לנצח (המלכודות).

---

### סעיף ג – lock, ‏grab ו-arbitration

על sequencer אחד רצים שלושה sequences. ‏A ו-B שולחים כל אחד 6 פריטים ברצף מהמשבצת הראשונה.
‏I מתחיל באמצע משבצת 1, בזמן ש-B0 על ה-driver : הוא שולח את I0, מחכה משבצת אחת לתשובה,
ואז שולח את I1 ו-I2. אסור שפריט של A או B ייכנס בין I0 ל-I2. ה-driver לוקח פריט אחד בכל
משבצת.

מה ה-driver מקבל עם ה-arbitration של ברירת המחדל? מה משנה עדיפות 500 ל-I (לשאר 100)? מה
עושים `lock()` ו-`grab()`, ומה ההבדל ביניהם?

??? tip "רמז 1"
    ב-`UVM_SEQ_ARB_FIFO`, ברירת המחדל, ה-sequencer בוחר את הבקשה הוותיקה בתור. איפה בבחירה
    הזו נכנסת העדיפות שמעבירים ל-`start()`?

??? tip "רמז 2"
    עדיפות קובעת רק מי מנצח בבחירה. מה קורה במשבצת שבה I מחכה לתשובה ואין לו בקשה בתור?
    ‏`lock()` נכנס לתור כמו בקשה, ו-`grab()` נכנס לראש התור.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        בברירת המחדל I מחכה בתור כמו כולם, ו-A1, ‏B1 ואחרים נכנסים בין הפריטים שלו. עדיפות 500
        לבד לא משנה כלום, כי FIFO מתעלם מעדיפות. עם `UVM_SEQ_ARB_STRICT_FIFO` ‏I מנצח כל בחירה
        שיש לו בה בקשה, אבל במשבצת שבה הוא מחכה לתשובה A1 נכנס. רק נעילה נותנת רצף : `lock()`
        מחכה לבקשות שכבר היו בתור לפניו (A1), ומאז ה-sequencer משרת רק את I, גם במשבצת שבה I
        לא שולח כלום. ‏`grab()` לא מחכה לתור : הפריט הבא שה-driver לוקח הוא של I. שניהם
        משתחררים ב-`unlock()` או `ungrab()`.

    #### הרעיון { .sol-idea }

    בכל פעם שה-driver מבקש פריט (`get_next_item`), ה-sequencer בוחר בין הבקשות שבתור, כלומר
    sequences שקראו ל-`start_item` ומחכים. מצב ה-arbitration קובע את הבחירה :

    | המצב | איך נבחרת הבקשה |
    |---|---|
    | ‏`UVM_SEQ_ARB_FIFO` | הוותיקה בתור. ברירת המחדל, והעדיפות לא משפיעה |
    | ‏`UVM_SEQ_ARB_STRICT_FIFO` | הוותיקה מבין אלה עם העדיפות הגבוהה ביותר |
    | ‏`UVM_SEQ_ARB_WEIGHTED` | הגרלה, בהסתברות ביחס לעדיפות |
    | ‏`UVM_SEQ_ARB_RANDOM` | הגרלה אחידה, בלי עדיפות |
    | ‏`UVM_SEQ_ARB_STRICT_RANDOM` | הגרלה בין אלה עם העדיפות הגבוהה ביותר |
    | ‏`UVM_SEQ_ARB_USER` | הפונקציה `user_priority_arbitration()` שכותבים ב-sequencer |

    עדיפות ומצב עונים על השאלה "מי הבא". הם לא יכולים להבטיח רצף, כי sequence שאין לו
    בקשה בתור לא משתתף בבחירה. נעילה עונה על שאלה אחרת : "מי מותר לו בכלל". לפי התקן
    (IEEE 1800.2), בקשת `lock()` נכנסת לסוף התור ומתקבלת אחרי שהבקשות שלפניה קיבלו את
    ה-driver. בקשת `grab()` נכנסת לראש התור ומתקבלת בבחירה הבאה. שתיהן מחכות אם sequence אחר
    כבר מחזיק נעילה. כשהנעילה מתקבלת, ה-sequencer נותן את ה-driver רק ל-sequence הנועל
    ולילדים שלו (sequences שהוא הפעיל עם `this` כהורה), עד `unlock()` או `ungrab()`.

    ל-pyuvm 5.0.0 אין `lock()`, ‏`grab()` או מצבי arbitration : ה-sequencer שלו הוא תור FIFO.
    לכן הפייתון כאן הוא **מודל** של sequencer, לא pyuvm. הוא מממש את הכללים של התקן שלמעלה
    במשבצות זמן, והטסטים של השאלה בודקים אותו מול הכללים האלה. ה-SystemVerilog הוא הצורה
    של UVM.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **התור :** ‏`start_item` מוסיף בקשה לסוף התור, ו-sequence שסיים פריט מבקש את הבא
       לפני הבחירה הבאה.
    2. **הבחירה :** בכל משבצת, מבין הבקשות שלא חסומות בנעילה, לפי המצב.
    3. **‏`lock()` :** בקשת נעילה בסוף התור. היא מתקבלת כשהיא מגיעה לראש התור, ומאז רק
       ה-sequence הנועל וילדיו עוברים.
    4. **‏`grab()` :** בקשת נעילה בראש התור. היא מתקבלת מיד, אלא אם מישהו אחר כבר נועל.
    5. **השחרור :** ‏`unlock()` או `ungrab()`, ובקשות הנעילה שמחכות בראש התור מקבלות את
       תורן.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="a model of a sequencer" linenums="1" hl_lines="18 21 39 41 45 73 75 76"
        class Seq:
            """A sequence of the model: its steps run in order from the time start() is called."""
            def __init__(self, name, steps, start=0, priority=100):
                self.name, self.steps, self.start, self.priority = name, steps, start, priority
                self.parent, self.pc, self.wake = None, 0, start


        def sequencer(seqs, mode="FIFO"):
            """The items one sequencer gives its driver, one a slot ("-": none). Steps:
            ("item", name), ("wait", slots), ("lock",), ("grab",), ("unlock",), ("ungrab",),
            ("run", child): child.start(m_sequencer, this), which waits for the child."""
            queue, locks, ready, out = [], [], [], []    # the requests in order; the lock holders
            everyone, busy = list(seqs), None

            def blocked(s):                    # a lock held by a sequence that is not s or above s
                def above(h, s):
                    return s is not None and (s is h or above(h, s.parent))
                return any(not above(h, s) for h in locks)

            def grant_locks():                 # the lock requests at the head of the queue
                while queue and queue[0][0] == "lock" and not blocked(queue[0][1]):
                    s = queue.pop(0)[1]
                    locks.append(s)
                    ready.append(s)

            def run(s, now):
                while s.pc < len(s.steps):
                    op, *arg = s.steps[s.pc]
                    s.pc += 1
                    if op == "item":           # start_item: wait for the arbitration
                        queue.append(("item", s, arg[0]))
                        return
                    if op == "wait":
                        s.wake = now + arg[0]
                        return
                    if op in ("lock", "grab"):
                        request = ("lock", s)
                        if op == "lock":
                            queue.append(request)
                        else:
                            queue.insert(0, request)
                        grant_locks()
                        return
                    if op in ("unlock", "ungrab"):
                        locks.remove(s)
                        grant_locks()
                    if op == "run":
                        child = arg[0]
                        child.parent, child.wake = s, None
                        everyone.append(child)
                        ready.append(child)
                        return
                if s.parent:                   # a child ended: its parent goes on
                    ready.append(s.parent)

            t = 0
            while t == 0 or queue or busy or any(s.wake is not None for s in everyone):
                assert t < 100, "a sequence waits forever"
                if busy:                       # item_done: the sequence goes on at once
                    ready.append(busy)
                    busy = None
                for now in (t, t + 0.5):       # a slot's start, then its middle
                    for s in everyone:
                        if s.wake == now:
                            s.wake = None
                            ready.append(s)
                    while ready:
                        run(ready.pop(0), now)
                    if now == t:               # the driver asks for the next item
                        grant_locks()
                        while ready:
                            run(ready.pop(0), now)
                        free = [r for r in queue if r[0] == "item" and not blocked(r[1])]
                        if mode == "STRICT_FIFO" and free:
                            top = max(r[1].priority for r in free)
                            free = [r for r in free if r[1].priority == top]
                        if free:
                            queue.remove(free[0])
                            busy = free[0][1]
                        out.append(free[0][2] if free else "-")
                t += 1
            while out and out[-1] == "-":
                out.pop()
            return out


        def traffic(name, n=6):
            """A or B: n items back to back from slot 0."""
            return Seq(name, [("item", f"{name}{i}") for i in range(n)])


        def irq(how=None, priority=100):
            """I, from the middle of slot 1: I0, a slot waiting for its answer, I1 and I2.
            how: None, "lock" or "grab" (released by "unlock" or "ungrab" at the end)."""
            steps = [("item", "I0"), ("wait", 1), ("item", "I1"), ("item", "I2")]
            if how:
                steps = [(how,)] + steps + [("un" + how,)]
            return Seq("I", steps, start=1.5, priority=priority)
        ```

    === "SystemVerilog"
        ```systemverilog title="class irq_seq" linenums="1" hl_lines="11 12 14 17 18 30 31"
        class irq_seq extends uvm_sequence #(packet);
          `uvm_object_utils(irq_seq)
          bit use_grab;                          // grab() instead of lock()

          function new(string name = "irq_seq");
            super.new(name);
          endfunction

          task body();
            packet rsp;
            if (use_grab) m_sequencer.grab(this);   // to the head of the queue
            else          m_sequencer.lock(this);   // behind the requests already queued
            send_one("I0");
            get_response(rsp);                   // a slot without a request: nobody else gets it
            send_one("I1");
            send_one("I2");
            if (use_grab) m_sequencer.ungrab(this);
            else          m_sequencer.unlock(this);
          endtask

          task send_one(string name);
            packet p = packet::type_id::create(name);
            start_item(p);
            finish_item(p);
          endtask
        endclass

        // the priority alone, in the virtual sequence: no lock, and not in a row
        task start_urgent(irq_seq irq);
          p_sequencer.pkt_seqr.set_arbitration(UVM_SEQ_ARB_STRICT_FIFO);   // FIFO ignores priorities
          irq.start(p_sequencer.pkt_seqr, this, 500);                       // the others have 100
        endtask
        ```

    #### למה זה נכון { .sol-proof }

    הסדר שה-driver מקבל בכל אחת מההגדרות, מהמודל (‏· היא משבצת שבה ה-driver לא מקבל כלום) :

    <!-- gen 4 -->

    | ההגדרה | מה ה-driver מקבל | רצף של I? |
    |---|---|:-:|
    | ברירת המחדל, `FIFO` | ‏<span dir="ltr">A0 B0 A1 <b>I0</b> B1 A2 B2 <b>I1</b> A3 B3 <b>I2</b> A4 …</span> | לא |
    | עדיפות 500 ל-I, ‏`FIFO` | ‏<span dir="ltr">A0 B0 A1 <b>I0</b> B1 A2 B2 <b>I1</b> A3 B3 <b>I2</b> A4 …</span> | לא |
    | עדיפות 500 ל-I, ‏`STRICT_FIFO` | ‏<span dir="ltr">A0 B0 <b>I0</b> A1 <b>I1</b> <b>I2</b> B1 …</span> | לא |
    | ‏`lock()`, ‏`FIFO` | ‏<span dir="ltr">A0 B0 A1 <b>I0</b> · <b>I1</b> <b>I2</b> B1 …</span> | כן |
    | ‏`grab()`, ‏`FIFO` | ‏<span dir="ltr">A0 B0 <b>I0</b> · <b>I1</b> <b>I2</b> A1 …</span> | כן |

    <!-- /gen -->

    - **ברירת המחדל ועדיפות 500 :** אותו סדר בדיוק. ‏I0 נכנס לתור במשבצת 1.5, אחרי A1, ולכן
      יוצא אחריו. כל פריט של I מחכה לבקשות שנכנסו לפניו.
    - **‏`STRICT_FIFO` :** ‏I0 עוקף את A1 שכבר חיכה. אבל במשבצת 3, כש-I מחכה לתשובה, אין לו
      בקשה בתור, ו-A1 עובר.
    - **‏`lock()` :** הבקשה נכנסת לתור במשבצת 1.5, אחרי A1, ולכן A1 עובר ראשון. מאז ה-sequencer
      נעול : במשבצת שבה I מחכה ה-driver לא מקבל כלום, ו-B1, שביקש לפני I1, מחכה עד `unlock()`.
    - **‏`grab()` :** הבקשה נכנסת לראש התור ומתקבלת מיד. B0 כבר על ה-driver ומסתיים, אבל
      הפריט הבא הוא I0, לפני A1 שחיכה.
    - **מה זה עולה :** גם ב-lock וגם ב-grab יש משבצת שבה ה-driver לא מקבל כלום, למרות ש-A
      ו-B מחכים. נעילה קונה רצף במחיר של רוחב פס.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : ‏`fork` ב-virtual sequence בלי לשאול מה הסדר"
    ‏`fork` של שני sequences על שני agents אומר "אין ביניהם תלות". כשיש תלות, הגדרה לפני
    תנועה או איפוס לפני הכול, כותבים אותה בסדר של הקריאות. הטסט עם ה-`fork` לא נתקע ולא
    קורס : הוא רק מאבד חבילות, ובלי בדיקה שכל חבילה יצאה אף אחד לא שם לב.

??? trap "מלכודת : ‏`item_done` זה לא ״ההגדרה נכנסה״"
    ‏`start()` של ההגדרה חוזר כשה-driver סיים את הכתיבה על האפיק. אם לבלוק יש latency
    (סנכרון בין שעונים, אפיק עם תשובה מאוחרת), הרגיסטר עוד לא התעדכן. אז ה-virtual sequence
    צריך לחכות לאישור : קריאה חוזרת של הרגיסטר, ביט סטטוס, או התשובה של האפיק.

??? trap "מלכודת : עדיפות בלי מצב arbitration שמשתמש בה"
    ‏`start(seqr, this, 500)` עם ה-arbitration של ברירת המחדל לא משנה כלום : FIFO מתעלם
    מעדיפות. וגם עם `STRICT_FIFO` עדיפות לא נותנת רצף. כשצריך רצף, נועלים.

??? trap "מלכודת : לחיצת יד שאף אחד לא עונה לה"
    ‏`pause.request()` מחכה שהתנועה תעצור. אם התנועה כבר נגמרה, או שהיא נתקעה, הבקשה מחכה
    לנצח. בסביבה אמיתית `boundary()` נקרא גם בסוף התנועה, או שהבקשה מוגבלת בזמן ומדווחת
    שגיאה.

??? trap "מלכודת : ‏`lock()` בלי `unlock()`"
    ‏sequence שנעל ונגמר, או נעצר באמצע, בלי לשחרר, משאיר את ה-sequencer חסום לכל השאר.
    משחררים בכל מסלול יציאה, ולא נועלים לזמן ארוך : כל משבצת נעולה היא משבצת שהתנועה
    האחרת לא מקבלת.

??? followup "שאלות המשך"
    - **איך virtual sequence מקבל את ה-sequencers בלי virtual sequencer?**

        ??? fu-answer "תשובה"
            ה-test שם את ה-handles ב-virtual sequence עצמו לפני `start()` (או דרך
            `uvm_config_db`), ומפעיל אותו בלי sequencer : `vseq.start(null)` ב-SV, ‏`start()`
            ב-pyuvm. אז אין `p_sequencer`, וה-sequence לא יכול לשלוח פריטים בעצמו.

    - **ב-SV, למה לא לנעול מה-virtual sequence את ה-sequencer של החבילות במקום לחיצת היד?**

        ??? fu-answer "תשובה"
            ‏`p_sequencer.pkt_seqr.lock(this)` עוצר את התנועה בין שני פריטים, וזה עובד כאן
            כי חבילה היא פריט אחד. אם חבילה הייתה כמה פריטים, הנעילה הייתה עוצרת באמצע
            חבילה. לחיצת היד עוצרת בגבול של הפרוטוקול, לא של ה-sequencer.

    - **מה קורה ל-`grab()` כש-sequence אחר כבר מחזיק `lock()`?**

        ??? fu-answer "תשובה"
            הוא מחכה. ‏`grab()` עוקף את התור, לא את מי שכבר נועל. הוא מתקבל אחרי `unlock()`.

    - **שני virtual sequences נועלים כל אחד את שני ה-sequencers. מה יכול לקרות?**

        ??? fu-answer "תשובה"
            קיפאון : אחד נעל את הראשון ומחכה לשני, והאחר להפך. נועלים תמיד באותו סדר, או
            נועלים רק את מה שבאמת צריך.

    - **ב-`UVM_SEQ_ARB_WEIGHTED`, עם עדיפות 500 ל-I ו-100 ל-A ול-B, באיזה סיכוי I מנצח?**

        ??? fu-answer "תשובה"
            כשלשלושתם יש בקשה בתור : ‏500 מתוך 700, כלומר 5 מתוך 7. כש-I לבד מול A :
            ‏500 מתוך 600.
