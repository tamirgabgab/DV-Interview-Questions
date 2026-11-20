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

- **ממשק ההגדרות :** כתיבה לרגיסטר במחזור שבו `cfg_valid` גבוה, והערך החדש תקף מהמחזור
  הבא. ‏`CTRL` (כתובת 0) מחזיק את `enable` בביט 0, ו-`KEY` (כתובת 1) את המפתח. האפיק מקבל
  כתיבה אחת בכל שלושה מחזורים.
- **ממשק החבילות :** בייט בכל מחזור, ו-`in_last` על הבייט האחרון של החבילה. כל בייט יוצא
  במחזור הבא, אחרי XOR עם `key` של המחזור שבו נכנס.

לבלוק שני כללים. חבילה שהבייט הראשון שלה מגיע כש-`enable` נמוך נזרקת כולה, והמונה `drops`
סופר אותה. ואת `KEY` ו-`CTRL` מותר לשנות רק בין חבילות.

הסביבה בנויה כמו בשאלה [0049](../junior/0049-uvm-testbench-architecture.md) : שני agents
פעילים, ו-virtual sequencer שמחזיק handles ל-sequencers של שניהם, `reg_seqr` ו-`pkt_seqr`.
‏`ConfigSeq` כותב רגיסטרים לפי הסדר (בברירת המחדל המפתח 0x5A ואחריו `enable`), ו-`TrafficSeq`
שולח 8 חבילות של 3 בייטים, כל אחת ב-`send(k)`. ה-checker מסתכל על הפינים : הוא מנבא כל חבילה
לפי הרגיסטרים שנכתבו, משווה ליציאה, ומדווח על כתיבה באמצע חבילה. בסוף הטסט כל חבילה ששלחנו
צריכה לצאת :

<!-- gen 0 -->

<svg class="figure uv-fig" viewBox="0 0 500 440" style="max-width:32rem" role="img" aria-label="הסביבה : virtual sequence על virtual sequencer שמחזיק handles לשני sequencers, של reg_agent ושל pkt_agent; שני drivers מחוברים ל-pkt_xor, ו-checker מסתכל על הפינים"><defs><marker id="vs-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs><g class="uv-box is-cont uv-test"><rect x="6" y="6" width="488" height="340" rx="8"/><text x="14" y="23">test</text></g><g class="uv-box is-cont uv-env"><rect x="14" y="76" width="472" height="262" rx="8"/><text x="22" y="93">env</text></g><g class="uv-box is-cont uv-reg_agent"><rect x="24" y="156" width="170" height="172" rx="8"/><text x="32" y="173">reg_agent</text></g><g class="uv-box is-cont uv-pkt_agent"><rect x="306" y="156" width="170" height="172" rx="8"/><text x="468" y="173" text-anchor="end">pkt_agent</text></g><line class="uv-arrow uv-tlm" x1="250.0" y1="60.0" x2="250.0" y2="98.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow stream-c" x1="215.4" y1="136.0" x2="131.7" y2="182.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow stream-c" x1="284.6" y1="136.0" x2="368.3" y2="182.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow uv-tlm" x1="99.0" y1="218.0" x2="99.0" y2="276.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow uv-tlm" x1="401.0" y1="218.0" x2="401.0" y2="276.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow uv-pin" x1="124.6" y1="312.0" x2="210.1" y2="372.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow uv-pin" x1="375.4" y1="312.0" x2="289.9" y2="372.0" marker-end="url(#vs-arrow)"/><line class="uv-arrow uv-pin" x1="250.0" y1="372.0" x2="250.0" y2="312.0" marker-end="url(#vs-arrow)"/><g class="uv-box uv-vseq"><rect x="167" y="28" width="166" height="32" rx="6"/><text x="250.0" y="49.0" text-anchor="middle">virtual sequence</text></g><g class="uv-box uv-vseqr"><rect x="160" y="98" width="180" height="38" rx="6"/><text x="250.0" y="122.0" text-anchor="middle">virtual sequencer</text></g><g class="uv-box uv-reg_seqr"><rect x="44" y="182" width="110" height="36" rx="6"/><text x="99.0" y="205.0" text-anchor="middle">sequencer</text></g><g class="uv-box uv-reg_drv"><rect x="44" y="276" width="110" height="36" rx="6"/><text x="99.0" y="299.0" text-anchor="middle">driver</text></g><g class="uv-box uv-pkt_seqr"><rect x="346" y="182" width="110" height="36" rx="6"/><text x="401.0" y="205.0" text-anchor="middle">sequencer</text></g><g class="uv-box uv-pkt_drv"><rect x="346" y="276" width="110" height="36" rx="6"/><text x="401.0" y="299.0" text-anchor="middle">driver</text></g><g class="uv-box uv-checker"><rect x="200" y="276" width="100" height="36" rx="6"/><text x="250.0" y="299.0" text-anchor="middle">checker</text></g><g class="uv-box uv-dut"><rect x="165" y="372" width="170" height="56" rx="6"/><text x="250.0" y="405.0" text-anchor="middle">pkt_xor</text></g></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="uv-key-tlm"></i>פריטים : start ו-seq_item_port</span><span><i class="by-bfs"></i>מצביע ל-sequencer, נקבע ב-connect_phase</span><span><i class="uv-key-pin"></i>אותות</span></span>

<!-- /gen -->

ה-virtual sequence של הטסט הראשון מריץ את ההגדרה ואת התנועה במקביל :

=== "Python"
    ```python title="BootVseq" hl_lines="3 4"
    class BootVseq(uvm_sequence):
        async def body(self):
            cfg = cocotb.start_soon(ConfigSeq("boot").start(self.sequencer.reg_seqr))
            await TrafficSeq("traffic").start(self.sequencer.pkt_seqr)
            await cfg
    ```

=== "SystemVerilog"
    ```systemverilog title="class boot_vseq" hl_lines="9 10 11"
    class boot_vseq extends uvm_sequence;
      `uvm_object_utils(boot_vseq)
      `uvm_declare_p_sequencer(virtual_sequencer)
      function new(string name = "boot_vseq"); super.new(name); endfunction

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

הפייתון רץ ב-pyuvm על Verilator, עם ה-RTL של הבלוק והסביבה המלאה שבתיקיית הטסטים של השאלה. ה-SystemVerilog של
UVM לא רץ, כי ל-Verilator אין ספריית UVM, והטסטים בודקים שהוא מקביל לפייתון. הטסט נכשל :

```text title="BootTest"
ERROR  cycle 0: a register write during packet 0
ERROR  cycle 3: a register write during packet 1
INFO   8 packets in, 6 out, 2 dropped, 2 errors
FAIL   AssertionError: packets were lost or changed
```

- **סעיף א – הסדר :** למה שתי חבילות נזרקו, ולמה ה-checker מדווח על כתיבות באמצע חבילה?
  תקנו את ה-virtual sequence. מאיפה הוא מקבל את שני ה-sequencers?
- **סעיף ב – מפתח חדש באמצע התנועה :** טסט אחר מחליף את המפתח בזמן שהתנועה רצה (הקוד
  בסעיף). איך מסנכרנים כך שההחלפה תיפול בין שתי חבילות?
- **סעיף ג – lock, ‏grab ו-arbitration :** על sequencer אחד רצים שני זרמי תנועה ו-sequence
  דחוף ששולח שלושה פריטים ברצף. מה ה-driver מקבל, ומה משנים עדיפות, `lock()` ו-`grab()`?

??? interviewer "מה המראיין בודק"
    - **מי קובע את הסדר :** שאין שום סדר בין פריטים של שני sequencers, ושה-virtual sequence
      הוא המקום היחיד שקובע אותו. ‏`fork` הוא החלטה שאין סדר.
    - **נקודת סנכרון אמיתית :** לחיצת יד עם מי שיודע איפה נגמרת חבילה, במקום "מספר מחזורים".
    - **עדיפות, lock ו-grab :** ההבדל בין "לנצח בבחירה הבאה", "להחזיק את ה-sequencer"
      ו"לעקוף את התור", ושב-FIFO, ברירת המחדל, העדיפות לא משנה כלום.

---

### סעיף א – הסדר

??? tip "רמז 1"
    באיזה מחזור עולה `enable`, ובאיזה מחזור מתחילה כל אחת מהחבילות הראשונות? האפיק מקבל
    כתיבה אחת בכל שלושה מחזורים.

??? tip "רמז 2"
    מתי `start()` של sequence חוזר?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שני ה-sequences מתחילים במחזור 0. המפתח נכתב במחזור 0 ו-`enable` במחזור 3, ולכן
        הבלוק פועל רק ממחזור 4. חבילות 0 ו-1 התחילו במחזורים 0 ו-3 ונזרקו, ושתי הכתיבות נפלו
        באמצע שלהן. התיקון : לחכות ל-`start()` של ההגדרה ורק אז להתחיל את התנועה. ה-handles
        מגיעים מה-virtual sequencer, שה-env ממלא ב-`connect_phase`. אחרי התיקון :
        `8 packets in, 8 out, 0 dropped, 0 errors`.

    #### הרעיון { .sol-idea }

    כל sequencer מסדר רק את הפריטים שלו, ושני ה-drivers רצים במקביל, כל אחד בקצב שלו. מי
    שיודע שההגדרה צריכה לבוא קודם הוא ה-virtual sequence, והוא אומר את זה בסדר של הקריאות.
    ‏`start()` חוזר כשה-`body()` נגמר, אחרי ה-`item_done` של הכתיבה האחרונה : זו נקודת הסנכרון.
    וה-DUT לא שבור : הוא זרק בדיוק את מה שהכלל שלו אומר. בלי הבדיקה שכל חבילה יצאה, טסט כזה
    עובר עם 6 חבילות במקום 8.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="BootVseqFixed" hl_lines="3 4"
        class BootVseqFixed(uvm_sequence):
            async def body(self):
                await ConfigSeq("boot").start(self.sequencer.reg_seqr)   # (1)!
                await TrafficSeq("traffic").start(self.sequencer.pkt_seqr)
        ```

        1. ‏`self.sequencer` הוא ה-`VirtualSequencer` שה-virtual sequence הופעל עליו. ב-pyuvm אין
           `p_sequencer`, וה-handles נגישים ישירות.

    === "SystemVerilog"
        ```systemverilog title="class boot_vseq_fixed" linenums="1" hl_lines="3 4 16 17"
        class virtual_sequencer extends uvm_sequencer;
          `uvm_component_utils(virtual_sequencer)
          uvm_sequencer #(reg_write) reg_seqr;   // env::connect_phase: vseqr.reg_seqr = reg_agent.seqr;
          uvm_sequencer #(packet)    pkt_seqr;
          function new(string name, uvm_component parent); super.new(name, parent); endfunction
        endclass

        class boot_vseq_fixed extends uvm_sequence;
          `uvm_object_utils(boot_vseq_fixed)
          `uvm_declare_p_sequencer(virtual_sequencer)   // (1)!
          function new(string name = "boot_vseq_fixed"); super.new(name); endfunction

          task body();
            config_seq  cfg     = config_seq::type_id::create("boot");
            traffic_seq traffic = traffic_seq::type_id::create("traffic");
            cfg.start(p_sequencer.reg_seqr, this);   // returns after the last write's item_done
            traffic.start(p_sequencer.pkt_seqr, this);
          endtask
        endclass
        ```

        1. המאקרו מגדיר את `p_sequencer` מהטיפוס `virtual_sequencer`, ב-cast מ-`m_sequencer`.

    #### למה זה נכון { .sol-proof }

    המחזורים הראשונים של הריצה עם ה-`fork`, מהפינים של Verilator. ‏`drops` עולה אחרי הבייט
    הראשון של חבילה 0 ושל חבילה 1, ו-`out_valid` עולה לראשונה במחזור 7, עם חבילה 2 :

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

    אחרי התיקון ההגדרה תופסת את מחזורים 0 עד 5, והחבילה הראשונה מתחילה במחזור 6, כש-`enable`
    כבר 1. המחיר : 6 מחזורים של המתנה, 33 מחזורים במקום 27.

---

### סעיף ב – מפתח חדש באמצע התנועה

הטסט השני מגדיר את הבלוק, מתחיל את התנועה ברקע, ו-10 מחזורים אחרי שהיא התחילה מחליף את
המפתח ל-0xC3. אי אפשר לדעת מראש באיזה מחזור נגמרת חבילה :

=== "Python"
    ```python title="RekeyVseq" hl_lines="6 7"
    class RekeyVseq(uvm_sequence):
        async def body(self):
            seqr = self.sequencer
            await ConfigSeq("boot").start(seqr.reg_seqr)
            traffic = cocotb.start_soon(TrafficSeq("traffic").start(seqr.pkt_seqr))
            await ClockCycles(cocotb.top.clk, REKEY_AT)    # REKEY_AT = 10
            await ConfigSeq("rekey", [(KEY, 0xC3)]).start(seqr.reg_seqr)
            await traffic
    ```

=== "SystemVerilog"
    ```systemverilog title="class rekey_vseq" hl_lines="13 15"
    class rekey_vseq extends uvm_sequence;
      `uvm_object_utils(rekey_vseq)
      `uvm_declare_p_sequencer(virtual_sequencer)
      int rekey_at = 10;                      // cycles of 10 ns after the traffic starts
      function new(string name = "rekey_vseq"); super.new(name); endfunction

      task body();
        config_seq  boot    = config_seq::type_id::create("boot");
        config_seq  rekey   = config_seq::type_id::create("rekey");
        traffic_seq traffic = traffic_seq::type_id::create("traffic");
        rekey.writes = '{'{KEY, 8'hC3}};
        boot.start(p_sequencer.reg_seqr, this);
        fork traffic.start(p_sequencer.pkt_seqr, this); join_none
        #(rekey_at * 10ns);
        rekey.start(p_sequencer.reg_seqr, this);
        wait fork;
      endtask
    endclass
    ```

```text title="RekeyTest"
ERROR  cycle 16: a register write during packet 3
ERROR  cycle 18: packet 3 came out 6a 6b f1, expected 6a 6b 68
INFO   8 packets in, 8 out, 0 dropped, 2 errors
FAIL   AssertionError: packets were lost or changed
```

??? tip "רמז 1"
    ה-sequencer של ההגדרות לא יודע כלום על החבילות. מי יודע מתי חבילה אחת נגמרה והבאה עוד
    לא התחילה?

??? tip "רמז 2"
    ה-sequence של התנועה עובר בין חבילות בנקודה אחת : אחרי `finish_item` של חבילה ולפני
    `start_item` של הבאה. מה אם הוא ישאל שם "ביקשו ממני לעצור"?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        הכתיבה יצאה במחזור 16, באמצע חבילה 3 (מחזורים 15 עד 17), והבייט האחרון שלה הוצפן
        במפתח החדש : ‏f1 במקום 68. ‏10 מחזורים הם זמן, לא גבול של חבילה. התיקון : לחיצת יד.
        ה-virtual sequence מבקש לעצור, התנועה בודקת את הבקשה לפני כל חבילה ועוצרת שם, וה-virtual
        sequence כותב את המפתח וממשיך את התנועה. המפתח נכתב במחזור 18, אחרי חבילה 3 :
        `8 packets in, 8 out, 0 dropped, 0 errors`.

    #### הרעיון { .sol-idea }

    רק ה-sequence של התנועה יודע איפה הגבול בין חבילות, ולכן הסנכרון הוא בקשה ותשובה : מבקשים,
    התנועה עוצרת בגבול הבא ומודיעה, עושים את השינוי ומשחררים. אף צד לא צריך לדעת כמה זמן
    לוקחת חבילה. שני הדגלים הם **מצב**, לא אירוע רגעי (`Event` של cocotb נשאר דלוק עד `clear()`,
    וב-SV ‏`wait (stopped)` בודק רמה), ולכן הודעה שקדמה להמתנה לא הולכת לאיבוד.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="Pause, PausableTraffic, RekeyVseqFixed" linenums="1" hl_lines="7 8 9 12 14 28 38 40"
        class Pause:
            """A stop between two packets, asked for by the virtual sequence."""
            def __init__(self):
                self.requested, self.stopped, self.resumed = False, Event(), Event()

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
        ```

        1. הבקשה במחזור 16. חבילה 3 עוד באמצע, והקריאה חוזרת רק אחרי הבייט האחרון שלה.

    === "SystemVerilog"
        ```systemverilog title="pause_c, pausable_traffic, rekey_vseq_fixed" linenums="1" hl_lines="4 7 8 17 33 35"
        class pause_c;
          bit requested, stopped;
          task boundary();                       // the traffic, before each packet
            if (requested) begin stopped = 1; wait (!requested); end
          endtask
          task request();                        // returns when the traffic stopped
            requested = 1;
            wait (stopped);
          endtask
          function void resume(); requested = 0; stopped = 0; endfunction
        endclass

        class pausable_traffic extends traffic_seq;
          `uvm_object_utils(pausable_traffic)
          pause_c pause;
          function new(string name = "pausable_traffic"); super.new(name); endfunction
          task send(int k); pause.boundary(); super.send(k); endtask   // virtual in traffic_seq
        endclass

        class rekey_vseq_fixed extends rekey_vseq;
          `uvm_object_utils(rekey_vseq_fixed)
          function new(string name = "rekey_vseq_fixed"); super.new(name); endfunction
          task body();
            pause_c          pause   = new();
            config_seq       boot    = config_seq::type_id::create("boot");
            config_seq       rekey   = config_seq::type_id::create("rekey");
            pausable_traffic traffic = pausable_traffic::type_id::create("traffic");
            traffic.pause = pause;
            rekey.writes  = '{'{KEY, 8'hC3}};
            boot.start(p_sequencer.reg_seqr, this);
            fork traffic.start(p_sequencer.pkt_seqr, this); join_none
            #(rekey_at * 10ns);
            pause.request();
            rekey.start(p_sequencer.reg_seqr, this);
            pause.resume();
            wait fork;
          endtask
        endclass
        ```

    #### למה זה נכון { .sol-proof }

    בלי לחיצת היד, ‏`key` מתחלף בקצה שבסוף מחזור 16, והבייט 32 של מחזור 17 יוצא כ-f1 (32 XOR
    c3) במקום 68 (32 XOR 5a). עם לחיצת היד חבילה 3 נגמרת במחזור 17, הכתיבה יוצאת במחזור 18,
    והתנועה ממשיכה במחזור 21 : חבילות 0 עד 3 במפתח 5a, ו-4 עד 7 ב-c3. המחיר : שלושה מחזורים
    בלי תנועה, 36 מחזורים במקום 33.

---

### סעיף ג – lock, ‏grab ו-arbitration

על sequencer אחד רצים שלושה sequences. ‏A ו-B שולחים כל אחד 6 פריטים ברצף מהמשבצת הראשונה.
‏I מתחיל באמצע משבצת 1, בזמן ש-B0 על ה-driver : הוא שולח את I0, מחכה משבצת אחת לתשובה,
ואז שולח את I1 ו-I2. אסור שפריט של A או B ייכנס בין I0 ל-I2. ה-driver לוקח פריט אחד בכל
משבצת. מה ה-driver מקבל עם ה-arbitration של ברירת המחדל? מה משנה עדיפות 500 ל-I (לשאר 100)?
מה עושים `lock()` ו-`grab()`?

??? tip "רמז 1"
    ב-`UVM_SEQ_ARB_FIFO`, ברירת המחדל, ה-sequencer בוחר את הבקשה הוותיקה בתור. איפה נכנסת
    העדיפות שמעבירים ל-`start()`?

??? tip "רמז 2"
    מה קורה במשבצת שבה I מחכה לתשובה ואין לו בקשה בתור?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        בברירת המחדל I מחכה בתור כמו כולם, ופריטים של A ו-B נכנסים בין הפריטים שלו. עדיפות 500
        לבד לא משנה כלום, כי FIFO מתעלם מעדיפות. עם `UVM_SEQ_ARB_STRICT_FIFO` ‏I מנצח כל בחירה
        שיש לו בה בקשה, אבל במשבצת שבה הוא מחכה לתשובה A1 נכנס. רק נעילה נותנת רצף : `lock()`
        מחכה לבקשות שכבר בתור (A1), ומאז ה-sequencer משרת רק את I. ‏`grab()` עוקף את התור : הפריט
        הבא הוא של I. שניהם משתחררים ב-`unlock()` או `ungrab()`.

    #### הרעיון { .sol-idea }

    בכל פעם שה-driver מבקש פריט, ה-sequencer בוחר בין הבקשות שבתור (sequences שקראו
    ל-`start_item`) לפי מצב ה-arbitration, שנקבע ב-`set_arbitration()`. את העדיפות מעבירים
    ל-`start()`, למשל `irq.start(p_sequencer.pkt_seqr, this, 500)` :

    | המצב | איך נבחרת הבקשה |
    |---|---|
    | ‏`UVM_SEQ_ARB_FIFO` | הוותיקה בתור. ברירת המחדל, והעדיפות לא משפיעה |
    | ‏`UVM_SEQ_ARB_STRICT_FIFO` | הוותיקה מבין אלה עם העדיפות הגבוהה ביותר |
    | ‏`UVM_SEQ_ARB_WEIGHTED` | הגרלה, בהסתברות ביחס לעדיפות |
    | ‏`UVM_SEQ_ARB_RANDOM`, ‏`UVM_SEQ_ARB_STRICT_RANDOM` | הגרלה אחידה, בין כולן או בין אלה עם העדיפות הגבוהה |
    | ‏`UVM_SEQ_ARB_USER` | הפונקציה `user_priority_arbitration()` שכותבים ב-sequencer |

    מצב ועדיפות עונים על "מי הבא", ולא יכולים להבטיח רצף : sequence בלי בקשה בתור לא משתתף
    בבחירה. נעילה עונה על "מי מותר לו בכלל". לפי התקן (IEEE 1800.2), בקשת `lock()` נכנסת לסוף
    התור, ובקשת `grab()` לראשו. הנעילה מתקבלת כשהבקשה בראש התור ואף sequence אחר לא נועל, ומאז
    ה-driver מקבל רק פריטים של הנועל ושל הילדים שלו, עד השחרור.

    #### הקוד { .sol-code }

    ל-pyuvm 5.0.0 אין `lock()`, ‏`grab()` או מצבי arbitration : ה-sequencer שלו הוא תור FIFO.
    לכן הפייתון כאן מתאר את A, ‏B ו-I כצעדים של **מודל** של sequencer, שכתוב לפי הכללים שלמעלה
    (‏`Seq` ו-`sequencer(seqs, mode)` ב-`tools/figures/q0114.py`), והתיבה למטה מריצה אותו.

    === "Python"
        ```python title="A, B and I, for the model of the sequencer" linenums="1" hl_lines="8 10"
        def traffic(name, n=6):
            """A or B: n items back to back from slot 0."""
            return Seq(name, [("item", f"{name}{i}") for i in range(n)])


        def irq(how=None, priority=100, start=1.5):
            """I: I0, a slot waiting for its answer, then I1 and I2. how: None, "lock" or "grab"."""
            steps = [("item", "I0"), ("wait", 1), ("item", "I1"), ("item", "I2")]
            if how:
                steps = [(how,)] + steps + [("un" + how,)]
            return Seq("I", steps, start=start, priority=priority)
        ```

    === "SystemVerilog"
        ```systemverilog title="class irq_seq" linenums="1" hl_lines="8 9 11 14 15"
        class irq_seq extends uvm_sequence #(packet);
          `uvm_object_utils(irq_seq)
          bit use_grab;                          // grab() instead of lock()
          function new(string name = "irq_seq"); super.new(name); endfunction

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
        ```

    #### למה זה נכון { .sol-proof }

    מה ה-driver מקבל בכל הגדרה, מהמודל (‏· היא משבצת שבה ה-driver לא מקבל כלום) :

    <!-- gen 3 -->

    | ההגדרה | מה ה-driver מקבל | רצף של I? |
    |---|---|:-:|
    | ברירת המחדל, `FIFO` | ‏<span dir="ltr">A0 B0 A1 <b>I0</b> B1 A2 B2 <b>I1</b> A3 B3 <b>I2</b> A4 …</span> | לא |
    | עדיפות 500 ל-I, ‏`FIFO` | ‏<span dir="ltr">A0 B0 A1 <b>I0</b> B1 A2 B2 <b>I1</b> A3 B3 <b>I2</b> A4 …</span> | לא |
    | עדיפות 500 ל-I, ‏`STRICT_FIFO` | ‏<span dir="ltr">A0 B0 <b>I0</b> A1 <b>I1</b> <b>I2</b> B1 …</span> | לא |
    | ‏`lock()`, ‏`FIFO` | ‏<span dir="ltr">A0 B0 A1 <b>I0</b> · <b>I1</b> <b>I2</b> B1 …</span> | כן |
    | ‏`grab()`, ‏`FIFO` | ‏<span dir="ltr">A0 B0 <b>I0</b> · <b>I1</b> <b>I2</b> A1 …</span> | כן |

    <!-- /gen -->

    - **ברירת המחדל ועדיפות 500 :** אותו סדר. ‏I0 נכנס לתור במשבצת 1.5, אחרי A1, ויוצא אחריו.
    - **‏`STRICT_FIFO` :** ‏I0 עוקף את A1. אבל במשבצת 3 ל-I אין בקשה בתור, ו-A1 עובר.
    - **‏`lock()` :** הבקשה נכנסת אחרי A1, ולכן A1 עובר ראשון. מאז, גם במשבצת שבה I מחכה,
      ה-driver לא מקבל פריט של A או B.
    - **‏`grab()` :** הבקשה נכנסת לראש התור, והפריט הבא הוא I0, לפני A1 שחיכה.
    - **המחיר :** בשתי הנעילות יש משבצת ריקה, למרות ש-A ו-B מחכים. נעילה קונה רצף ברוחב פס.

    בתיבה בוחרים את המצב, את העדיפות של I, את סוג הנעילה ואת המשבצת שבה I מתחיל, ועוברים
    משבצת אחרי משבצת : מה בתור, מי נועל, ומה ה-driver מקבל ולמה.

    <div class="explorer" data-kind="seqarb"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : ‏`fork` ב-virtual sequence בלי לשאול מה הסדר"
    ‏`fork` של שני sequences על שני agents אומר "אין ביניהם תלות". כשיש תלות, כותבים אותה
    בסדר של הקריאות. הטסט עם ה-`fork` לא נתקע : הוא רק מאבד חבילות, ובלי בדיקה שכל חבילה יצאה
    אף אחד לא שם לב.

??? trap "מלכודת : ‏`item_done` זה לא ״ההגדרה נכנסה״"
    ‏`start()` של ההגדרה חוזר כשה-driver סיים את הכתיבה על האפיק. אם לבלוק יש latency (סנכרון
    בין שעונים, אפיק עם תשובה מאוחרת), הרגיסטר עוד לא התעדכן, וצריך לחכות לאישור : קריאה חוזרת,
    ביט סטטוס, או התשובה של האפיק.

??? trap "מלכודת : ‏`lock()` בלי `unlock()`"
    ‏sequence שנעל ונגמר, או נעצר באמצע, בלי לשחרר, משאיר את ה-sequencer חסום לכל השאר.
    משחררים בכל מסלול יציאה, ולא נועלים לזמן ארוך : כל משבצת נעולה היא משבצת שהתנועה האחרת לא
    מקבלת.

??? followup "שאלות המשך"
    - **מה קורה ללחיצת היד של סעיף ב אם התנועה כבר נגמרה?**

        ??? fu-answer "תשובה"
            אף אחד לא קורא ל-`boundary()`, ו-`request()` מחכה לנצח. בסביבה אמיתית `boundary()`
            נקרא גם בסוף התנועה, או שהבקשה מוגבלת בזמן ומדווחת שגיאה.

    - **ב-SV, למה לא לנעול מה-virtual sequence את ה-sequencer של החבילות במקום לחיצת היד?**

        ??? fu-answer "תשובה"
            ‏`p_sequencer.pkt_seqr.lock(this)` עוצר בין שני פריטים, וזה עובד כאן כי חבילה היא
            פריט אחד. אם חבילה הייתה כמה פריטים, הנעילה הייתה עוצרת באמצע חבילה.

    - **שני virtual sequences נועלים כל אחד את שני ה-sequencers. מה יכול לקרות?**

        ??? fu-answer "תשובה"
            קיפאון : אחד נעל את הראשון ומחכה לשני, והאחר להפך. נועלים תמיד באותו סדר, או רק את
            מה שבאמת צריך.

    - **ב-`UVM_SEQ_ARB_WEIGHTED`, עם עדיפות 500 ל-I ו-100 ל-A ול-B, באיזה סיכוי I מנצח?**

        ??? fu-answer "תשובה"
            כשלשלושתם יש בקשה בתור : ‏500 מתוך 700, כלומר 5 מתוך 7. כש-I לבד מול A : ‏500 מתוך 600.
