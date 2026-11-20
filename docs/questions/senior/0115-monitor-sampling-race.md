---
id: 115
title: ה-monitor שרואה שגיאות שלא קיימות
level: senior
difficulty: medium
kind: dv
tags: [debug, scoreboard, systemverilog, python]
source: ""
added: 2026-11-20
---

## השאלה

ה-DUT הוא רגיסטר אחד עם מחבר : בכל עלייה של השעון `add1` לוקח את `in_valid` ואת `in_data`,
ובמחזור שאחריה הם מופיעים ביציאה, עם הערך `in_data + 1` :

```systemverilog title="module add1" linenums="1"
module add1 (
  input  logic       clk,
  input  logic       in_valid,
  input  logic [7:0] in_data,
  output logic       out_valid,
  output logic [7:0] out_data
);
  always_ff @(posedge clk) begin
    out_valid <= in_valid;
    out_data  <= in_data + 8'd1;
  end
endmodule
```

לסביבת הבדיקה שלו יש שתי גרסאות, ב-cocotb וב-SystemVerilog, והן בנויות אותו דבר : driver ששולח
עשרה מחזורים של גירוי, ו-monitor עם מודל, שבודק בכל קצה שהיציאה היא הכניסה של הקצה הקודם ועוד
1. ה-monitor מתחיל לפני ה-driver, כדי לא לפספס אף מחזור :

=== "Python"
    ```python title="race_tb.py (cocotb)" linenums="1"
    import cocotb
    from cocotb.clock import Clock
    from cocotb.handle import Immediate
    from cocotb.triggers import ClockCycles, RisingEdge

    # (in_valid, in_data) of every cycle; in_data holds while in_valid is low
    STIM = [(1, 5), (1, 9), (1, 9), (0, 9), (0, 9), (1, 2), (1, 6), (1, 6), (0, 6), (0, 6)]


    def item(valid, data):
        return str(data) if valid else "none"


    async def drive(dut):
        for valid, data in STIM:
            await RisingEdge(dut.clk)
            dut.in_valid.value = Immediate(valid)
            dut.in_data.value = Immediate(data)


    async def monitor(dut, errors):
        """The model: out is in + 1, one cycle later."""
        exp_valid, exp_data, cycle = 0, 0, 0
        while True:
            await RisingEdge(dut.clk)
            cycle += 1
            valid, data = int(dut.out_valid.value), int(dut.out_data.value)
            if valid != exp_valid or (exp_valid and data != exp_data):
                errors.append(f"cycle {cycle}: expected {item(exp_valid, exp_data)}, got {item(valid, data)}")
                dut._log.info(errors[-1])
            exp_valid = int(dut.in_valid.value)              # what the DUT takes at this edge
            exp_data = (int(dut.in_data.value) + 1) % 256


    @cocotb.test()
    async def race_tb(dut):
        dut.in_valid.value = 0
        dut.in_data.value = 0
        cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start(start_high=False))
        errors = []
        cocotb.start_soon(monitor(dut, errors))
        await cocotb.start_soon(drive(dut))
        await ClockCycles(dut.clk, 3)
        assert not errors, f"{len(errors)} mismatches"
    ```

=== "SystemVerilog"
    ```systemverilog title="module race_tb" linenums="1"
    module race_tb;
      localparam int N = 10;
      bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
      logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low
      logic       clk = 0, in_valid = 0, out_valid;
      logic [7:0] in_data = 0, out_data;
      int         cycle = 0, mismatches = 0;

      add1 dut (.*);
      always #5 clk = ~clk;

      function automatic string item(logic valid, logic [7:0] data);
        return valid ? $sformatf("%0d", data) : "none";
      endfunction

      task automatic drive();
        foreach (V[i]) begin
          @(posedge clk);
          in_valid = V[i];
          in_data  = D[i];
        end
      endtask

      task automatic monitor();                  // the model: out is in + 1, one cycle later
        logic       exp_valid = 0;
        logic [7:0] exp_data  = 0;
        forever begin
          @(posedge clk);
          cycle++;
          if (out_valid != exp_valid || (exp_valid && out_data != exp_data)) begin
            mismatches++;
            $display("cycle %0d: expected %s, got %s", cycle, item(exp_valid, exp_data), item(out_valid, out_data));
          end
          exp_valid = in_valid;                  // what the DUT takes at this edge
          exp_data  = in_data + 8'd1;
        end
      endtask

      initial begin
        fork
          monitor();
          drive();
        join_any
        repeat (3) @(posedge clk);
        $display("%0d mismatches", mismatches);
        $finish;
      end
    endmodule
    ```

שתי הגרסאות, על Verilator 5.053, מדווחות על אותן שש שגיאות :

<!-- gen 0 -->

```text
cycle 2: expected none, got 6
cycle 3: expected 6, got 10
cycle 5: expected 10, got none
cycle 7: expected none, got 3
cycle 8: expected 3, got 7
cycle 10: expected 7, got none
6 mismatches
```

<!-- /gen -->

וזו צורת הגל מה-dump של אותה ריצה. כל עמודה היא מחזור, עם הערכים שאחרי הקצה שפותח אותו,
והשורה `mismatch` מסמנת את הקצוות שבהם ה-monitor דיווח :

<!-- gen 1 -->

```wavedrom
{ signal: [
  { name: "clk",       wave: "p........." },
  { name: "cycle",     wave: "==========", data: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] },
  { name: "in_valid",  wave: "1..0.1..0." },
  { name: "in_data",   wave: "==...==...", data: ["5", "9", "2", "6"] },
  { name: "out_valid", wave: "1..0.1..0." },
  { name: "out_data",  wave: "==...==...", data: ["6", "10", "3", "7"] },
  { name: "mismatch",  wave: "01.0101.01" }
]}
```

<!-- /gen -->

צוות ה-RTL בדק את `add1` ולא מצא כלום : פליפ-פלופ ומחבר. מצאו את הבאג. הסבירו למה השגיאות
נופלות בדיוק על המחזורים 2, 3, 5, 7, 8 ו-10, ולמה לא על 1, 4, 6 ו-9. תקנו את שתי הגרסאות,
והסבירו לפי אזורי התזמון של SystemVerilog (<span dir="ltr">Preponed, Active, NBA, Observed, Reactive,
Postponed</span>) למה כל תיקון עובד.

??? interviewer "מה המראיין בודק"
    - **‏race מול באג :** האם המועמד שם לב שהשגיאות תלויות בגירוי ולא בחשבון : הן נופלות רק אחרי
      קצוות שבהם הכניסה השתנתה, ואין בהן שום דבר שמחבר של 8 ביטים יכול לטעות בו.
    - **אזורי התזמון :** מה רץ ב-Active, מה נדחה ל-NBA, ולמה clocking block דוגם ב-Preponed
      ודוחף מאוחר יותר באותו צעד זמן.
    - **שלושה צדדים לקצה :** ה-driver כותב, ה-DUT וה-monitor קוראים. תיקון של צד אחד לא מספיק,
      והמועמד צריך לדעת איזה צד.
    - **מה הסימולטור עושה בפועל :** השפה לא קובעת את הסדר, ולכן סימולטור אחר יכול להראות שגיאות
      אחרות או אף אחת. וב-cocotb : מתי כתיבה מגיעה לסימולטור.

---

??? tip "רמז 1"
    מה משותף למחזורים בלי שגיאה? השוו את `in_valid` ו-`in_data` לפני כל קצה ואחריו.

??? tip "רמז 2"
    בקצה שפותח את מחזור 2 יש ל-`in_data` שני ערכים : 5 לפני שה-driver כותב, ו-9 אחרי. שלושה
    תהליכים נוגעים בו באותו צעד זמן. מי מהם רואה איזה ערך, ומי קבע את הסדר?

??? success "פתרון"
    !!! answer "תשובה בקצרה"
        ה-driver כותב את הכניסות ב-`=` (וב-cocotb ב-`Immediate`) בדיוק בקצה שבו ה-DUT וה-monitor
        קוראים אותן : race. ב-Verilator ה-monitor רואה את הערך שלפני הכתיבה וה-DUT את זה שאחריה,
        ולכן כל קצה שבו הכניסה השתנתה נותן שגיאה בקצה הבא. התיקון : לכתוב רק אחרי שכולם קראו.
        ‏clocking block, ‏`<=` או הירידה של השעון ב-SystemVerilog, וכתיבה רגילה בלי `Immediate`
        ב-cocotb : 0 שגיאות, בכל סדר של התהליכים.

    #### הרעיון { .sol-idea }

    בקצה שפותח את מחזור 2 שלושה תהליכים נוגעים ב-`in_data` באותו צעד זמן : ה-driver כותב 9,
    ה-monitor קורא, וה-`always_ff` של ה-DUT קורא. עם `=` שלושתם רצים באזור ה-Active, והשפה לא
    קובעת את הסדר ביניהם (IEEE 1800, סעיף 4.7). הנה הקצה הזה, מוגדל, לפני התיקון ואחריו :

    <!-- gen 2 -->

    <svg class="perf-chart" viewBox="0 0 400 272" style="max-width:30rem" role="img" aria-label="הקצה של מחזור 2 מוגדל לאזורי התזמון. למעלה, עם כתיבה חוסמת, ה-monitor קורא 5 וה-DUT קורא 9. למטה, עם clocking block, שניהם קוראים 5"><text class="legend" x="6" y="15" style="font-size:15px">in_data = D[i]   (blocking, as found)</text><line class="grid" x1="74" x2="74" y1="24" y2="126" stroke-dasharray="3 3"/><text class="tick" x="106" y="38" text-anchor="middle" style="font-size:13px">Preponed</text><line class="grid" x1="138" x2="138" y1="24" y2="126" stroke-dasharray="3 3"/><text class="tick" x="194" y="38" text-anchor="middle" style="font-size:13px">Active</text><line class="grid" x1="250" x2="250" y1="24" y2="126" stroke-dasharray="3 3"/><text class="tick" x="286" y="38" text-anchor="middle" style="font-size:13px">NBA</text><line class="grid" x1="322" x2="322" y1="24" y2="126" stroke-dasharray="3 3"/><text class="tick" x="358" y="38" text-anchor="middle" style="font-size:13px">Re-NBA</text><line class="grid" x1="394" x2="394" y1="24" y2="126" stroke-dasharray="3 3"/><path class="ink-line" fill="none" stroke-width="1.5" d="M74,63 L141,63 L145,49 L394,49"/><text class="tick" x="68" y="61" text-anchor="end" style="font-size:14px">clk</text><text class="tick" x="68" y="95" text-anchor="end" style="font-size:14px">in_data</text><text class="tick" x="68" y="121" text-anchor="end" style="font-size:14px">out_data</text><polygon class="ink-line" fill="none" stroke-width="1.5" points="74,82 190,82 194,90 190,98 74,98"/><text class="tick" x="134" y="95" text-anchor="middle" style="font-size:14px">5</text><polygon class="ink-line" fill="none" stroke-width="1.5" points="198,82 394,82 394,98 198,98 194,90"/><text class="tick" x="294" y="95" text-anchor="middle" style="font-size:14px">9</text><polygon class="ink-line" fill="none" stroke-width="1.5" points="74,108 282,108 286,116 282,124 74,124"/><text class="tick" x="180" y="121" text-anchor="middle" style="font-size:14px">6</text><polygon class="ink-line" fill="none" stroke-width="1.5" points="290,108 394,108 394,124 290,124 286,116"/><text class="tick" x="340" y="121" text-anchor="middle" style="font-size:14px">10</text><circle class="s1-dot" cx="158" cy="90" r="5"/><text class="tick" x="158" y="76" text-anchor="middle" style="font-size:14px">mon</text><circle class="ink-dot" cx="194" cy="90" r="5"/><text class="tick" x="194" y="76" text-anchor="middle" style="font-size:14px">drv</text><circle class="s2-dot" cx="230" cy="90" r="5"/><text class="tick" x="230" y="76" text-anchor="middle" style="font-size:14px">DUT</text><text class="legend" x="6" y="155" style="font-size:15px">drv_cb.in_data &lt;= D[i]   (clocking block)</text><line class="grid" x1="74" x2="74" y1="164" y2="266" stroke-dasharray="3 3"/><text class="tick" x="106" y="178" text-anchor="middle" style="font-size:13px">Preponed</text><line class="grid" x1="138" x2="138" y1="164" y2="266" stroke-dasharray="3 3"/><text class="tick" x="194" y="178" text-anchor="middle" style="font-size:13px">Active</text><line class="grid" x1="250" x2="250" y1="164" y2="266" stroke-dasharray="3 3"/><text class="tick" x="286" y="178" text-anchor="middle" style="font-size:13px">NBA</text><line class="grid" x1="322" x2="322" y1="164" y2="266" stroke-dasharray="3 3"/><text class="tick" x="358" y="178" text-anchor="middle" style="font-size:13px">Re-NBA</text><line class="grid" x1="394" x2="394" y1="164" y2="266" stroke-dasharray="3 3"/><path class="ink-line" fill="none" stroke-width="1.5" d="M74,203 L141,203 L145,189 L394,189"/><text class="tick" x="68" y="201" text-anchor="end" style="font-size:14px">clk</text><text class="tick" x="68" y="235" text-anchor="end" style="font-size:14px">in_data</text><text class="tick" x="68" y="261" text-anchor="end" style="font-size:14px">out_data</text><polygon class="ink-line" fill="none" stroke-width="1.5" points="74,222 354,222 358,230 354,238 74,238"/><text class="tick" x="216" y="235" text-anchor="middle" style="font-size:14px">5</text><polygon class="ink-line" fill="none" stroke-width="1.5" points="362,222 394,222 394,238 362,238 358,230"/><text class="tick" x="376" y="235" text-anchor="middle" style="font-size:14px">9</text><polygon class="ink-line" fill="none" stroke-width="1.5" points="74,248 282,248 286,256 282,264 74,264"/><text class="tick" x="180" y="261" text-anchor="middle" style="font-size:14px">1</text><polygon class="ink-line" fill="none" stroke-width="1.5" points="290,248 394,248 394,264 290,264 286,256"/><text class="tick" x="340" y="261" text-anchor="middle" style="font-size:14px">6</text><circle class="s1-dot" cx="106" cy="230" r="5"/><text class="tick" x="106" y="216" text-anchor="middle" style="font-size:14px">mon</text><circle class="s2-dot" cx="194" cy="230" r="5"/><text class="tick" x="194" y="216" text-anchor="middle" style="font-size:14px">DUT</text><circle class="ink-dot" cx="358" cy="230" r="5"/><text class="tick" x="358" y="216" text-anchor="middle" style="font-size:14px">drv</text></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="s1"></i>הקריאה של ה-monitor (mon)</span><span><i class="ink"></i>הכתיבה של ה-driver (drv)</span><span><i class="s2"></i>הקריאה של ה-<code>always_ff</code> של ה-DUT (DUT)</span></span>

    <!-- /gen -->

    ‏Verilator 5.053 מריץ את התהליכים שמחכים ל-`@(posedge clk)` בסדר שבו התחילו לחכות, ואת
    ה-`always_ff` של ה-DUT אחריהם. זה מה שהוא עושה בריצות של השאלה, לא משהו שמובטח. ה-monitor
    הוא הענף הראשון ב-fork, ולכן הוא קורא 5, ה-driver כותב 9, וה-DUT לוקח 9. ה-DUT לא טועה : הוא
    מוסיף 1 למה שקיבל. אבל ה-monitor חושב שעבר 5, מצפה ל-6 בקצה הבא, ומקבל 10. כך כל קצה שבו
    הכניסה השתנתה נותן שגיאה קצה אחד אחריו, ובקצה שבו היא לא השתנתה שני הערכים זהים ואין על מה
    לריב. בצורת הגל זה נראה כמו פליפ-פלופ בלי השהיה : `out_data` מתחלף באותו קצה כמו `in_data`,
    כי ה-DUT לקח את הכניסה של אותו קצה.

    התיקון נותן לכל ערך בקצה רגע אחד מוגדר : קוראים את מה שהיה **לפני** הקצה, וכותבים **אחרי**
    שכל הקוראים קראו. ‏clocking block עושה את שניהם : ה-input שלו נדגם ב-`#1step`, הערך מסוף צעד
    הזמן הקודם (אזור ה-Preponed), וה-output שלו נדחף באזור ה-Re-NBA, אחרי שה-DUT קרא ב-Active
    ועדכן ב-NBA. גם cocotb בנוי כך : כתיבה רגילה נשמרת בתור עד אחרי שהסימולטור עיבד את הקצה. רק
    `Immediate` עוקף את התור, ומחזיר את ה-race.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מה משותף לשגיאות :** כל שגיאה באה קצה אחד אחרי קצה שבו `in_valid` או `in_data` השתנו.
       לפני מחזורים 4, 6 ו-9 הכניסה לא השתנתה (9 אחרי 9, ‏`in_valid` נמוך אחרי נמוך, 6 אחרי 6).
    2. **מה הגל אומר :** ‏`out_data` מתחלף באותו קצה כמו `in_data`. לרגיסטר אמיתי יש השהיה של
       מחזור : ה-DUT לקח ערך שנכתב באותו קצה.
    3. **מי רואה מה :** ה-driver כותב ב-`=` באזור ה-Active. ה-monitor רץ לפניו ורואה את הישן,
       ה-DUT רץ אחריו ורואה את החדש.
    4. **התיקון :** כתיבה שאף קורא לא רואה באותו קצה : ‏clocking block, ‏`<=`, או הקצה השני של
       השעון. ב-cocotb : כתיבה רגילה במקום `Immediate`.
    5. **הבדיקה :** אותו גירוי, 0 שגיאות, וגם כשמחליפים את הסדר של ה-monitor וה-driver.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="race_tb.py (fixed)" linenums="1" hl_lines="16 17"
        import cocotb
        from cocotb.clock import Clock
        from cocotb.triggers import ClockCycles, RisingEdge

        # (in_valid, in_data) of every cycle; in_data holds while in_valid is low
        STIM = [(1, 5), (1, 9), (1, 9), (0, 9), (0, 9), (1, 2), (1, 6), (1, 6), (0, 6), (0, 6)]


        def item(valid, data):
            return str(data) if valid else "none"


        async def drive(dut):
            for valid, data in STIM:
                await RisingEdge(dut.clk)
                dut.in_valid.value = valid                   # (1)!
                dut.in_data.value = data


        async def monitor(dut, errors):
            """The model: out is in + 1, one cycle later."""
            exp_valid, exp_data, cycle = 0, 0, 0
            while True:
                await RisingEdge(dut.clk)
                cycle += 1
                valid, data = int(dut.out_valid.value), int(dut.out_data.value)   # (2)!
                if valid != exp_valid or (exp_valid and data != exp_data):
                    errors.append(f"cycle {cycle}: expected {item(exp_valid, exp_data)}, got {item(valid, data)}")
                    dut._log.info(errors[-1])
                exp_valid = int(dut.in_valid.value)              # what the DUT takes at this edge
                exp_data = (int(dut.in_data.value) + 1) % 256


        @cocotb.test()
        async def race_tb(dut):
            dut.in_valid.value = 0
            dut.in_data.value = 0
            cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start(start_high=False))
            errors = []
            cocotb.start_soon(monitor(dut, errors))
            await cocotb.start_soon(drive(dut))
            await ClockCycles(dut.clk, 3)
            assert not errors, f"{len(errors)} mismatches"
        ```

        1. כתיבה רגילה היא deposit : ‏cocotb 2.1 שומר אותה בתור ומחיל אותה בתחילת שלב ה-ReadWrite
           הבא, אחרי שהסימולטור עיבד את הקצה. ה-DUT לוקח בקצה את הערך הקודם, וגם כל coroutine
           שקורא אחרי `RisingEdge`, באיזה סדר שלא יהיה : כמו `<=`.
        2. מיד אחרי `RisingEdge`, על Verilator, יציאה רשומה מראה את הערך שלפני הקצה, וכניסה מראה את
           הערך שה-DUT לוקח בקצה. זו אותה נקודה של `#1step`, והמודל שלם כשקוראים בה את הכול.

    === "SystemVerilog"
        ```systemverilog title="module race_tb_cb" linenums="1" hl_lines="12 13 16 17 26 27 28 36 38 42 43"
        module race_tb_cb;
          localparam int N = 10;
          bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
          logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low
          logic       clk = 0, in_valid = 0, out_valid;
          logic [7:0] in_data = 0, out_data;
          int         cycle = 0, mismatches = 0;

          add1 dut (.*);
          always #5 clk = ~clk;

          clocking drv_cb @(posedge clk);            // the driver's side (1)
            output #0 in_valid, in_data;
          endclocking

          clocking mon_cb @(posedge clk);            // the monitor's side (2)
            input #1step in_valid, in_data, out_valid, out_data;
          endclocking

          function automatic string item(logic valid, logic [7:0] data);
            return valid ? $sformatf("%0d", data) : "none";
          endfunction

          task automatic drive();
            foreach (V[i]) begin
              @(drv_cb);
              drv_cb.in_valid <= V[i];
              drv_cb.in_data  <= D[i];
            end
          endtask

          task automatic monitor();                  // the model: out is in + 1, one cycle later
            logic       exp_valid = 0;
            logic [7:0] exp_data  = 0;
            forever begin
              @(mon_cb);
              cycle++;
              if (mon_cb.out_valid != exp_valid || (exp_valid && mon_cb.out_data != exp_data)) begin
                mismatches++;
                $display("cycle %0d: expected %s, got %s", cycle, item(exp_valid, exp_data), item(mon_cb.out_valid, mon_cb.out_data));
              end
              exp_valid = mon_cb.in_valid;           // the value from before the edge
              exp_data  = mon_cb.in_data + 8'd1;
            end
          endtask

          initial begin
            fork
              monitor();
              drive();
            join_any
            repeat (3) @(posedge clk);
            $display("%0d mismatches", mismatches);
            $finish;
          end
        endmodule
        ```

        1. ‏output עם skew של `#0` : ה-clocking block דוחף את הערך באזור ה-Re-NBA של הקצה, אחרי
           שה-`always_ff` של ה-DUT קרא את הכניסה ב-Active ועדכן את היציאה ב-NBA.
        2. ‏input עם skew של `#1step` (גם ברירת המחדל) : הערך מסוף צעד הזמן הקודם, אזור
           ה-Preponed, לפני שמישהו נגע בו בקצה. כך ה-monitor רואה את מה שה-DUT דוגם.

    שני תיקונים נוספים, כל אחד מהם מספיק לבד. רק `drive` של `race_tb` משתנה, וה-monitor נשאר כמו
    שהוא :

    ```systemverilog title="drive: nonblocking writes" hl_lines="4 5"
    task automatic drive();
      foreach (V[i]) begin
        @(posedge clk);
        in_valid <= V[i];                        // written in the NBA region
        in_data  <= D[i];
      end
    endtask
    ```

    ```systemverilog title="drive: the falling edge" hl_lines="3"
    task automatic drive();
      foreach (V[i]) begin
        @(negedge clk);                          // half a cycle away from the sampling edge
        in_valid = V[i];
        in_data  = D[i];
      end
    endtask
    ```

    #### למה זה נכון { .sol-proof }

    **השגיאות, קצה אחרי קצה.** בקצה \( k \) ה-driver כותב את השורה ה-\( k \) של הגירוי, וה-DUT
    לוקח אותה מיד. ה-monitor קורא את השורה הקודמת, שעוד נמצאת שם כשהוא רץ. היציאה בקצה \( k \) היא
    מה שה-DUT לקח בקצה הקודם, ועוד 1, וה-monitor מצפה למה שהוא עצמו קרא שם, ועוד 1 (בטבלה, —
    הוא מחזור בלי פריט) :

    <!-- gen 4 -->

    | מחזור | ה-monitor קרא | ה-DUT לקח | ה-monitor מצפה | ביציאה | שגיאה |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | 1 | — | 5 | — | — |  |
    | 2 | 5 | 9 | — | 6 | ✗ |
    | 3 | 9 | 9 | 6 | 10 | ✗ |
    | 4 | 9 | — | 10 | 10 |  |
    | 5 | — | — | 10 | — | ✗ |
    | 6 | — | 2 | — | — |  |
    | 7 | 2 | 6 | — | 3 | ✗ |
    | 8 | 6 | 6 | 3 | 7 | ✗ |
    | 9 | 6 | — | 7 | 7 |  |
    | 10 | — | — | 7 | — | ✗ |

    <!-- /gen -->

    לכן בקצה \( k \) יש שגיאה בדיוק כשבקצה \( k - 1 \) ה-monitor קרא שורה אחרת מזו שה-DUT לקח,
    כלומר כשהכניסה השתנתה בקצה הקודם. במחזור 1 אין קצה קודם, ושני הצדדים ריקים. לפני
    מחזורים 4, ‏6 ו-9 שתי השורות זהות : 9 אחרי 9, ‏`in_valid` נמוך אחרי נמוך, 6 אחרי 6.

    **למה כל תיקון עובד.**

    - **‏clocking block :** ה-monitor דוגם ב-Preponed, לפני כל דבר שקורה בקצה. ה-DUT קורא ב-Active,
      והכתיבה של `drv_cb` מגיעה רק ב-Re-NBA, אחרי ש-Active ו-NBA נגמרו. שניהם רואים את השורה
      שנכתבה בקצה הקודם, בכל סדר של התהליכים.
    - **‏`<=` ב-driver :** הכתיבה נדחית לאזור ה-NBA. ה-DUT וה-monitor קוראים ב-Active, לפני
      שהיא מתבצעת, ושניהם רואים את הישן. ה-NBA של ה-driver ושל ה-DUT באותו אזור, אבל ה-DUT כבר
      חישב את הצד הימני ב-Active, ולכן אין ביניהם race.
    - **‏driver בירידה :** הכתיבה קורית חצי מחזור לפני העלייה, ובעלייה יש ל-`in_data` ערך אחד.
      זה התיקון של הימים שלפני clocking blocks, והוא עובד כל עוד אף אחד לא דוגם בירידה.
    - **‏cocotb :** ב-cocotb 2.1 כתיבה רגילה נשמרת בתור (`_schedule_write` ב-`cocotb/handle.py`)
      ומוחלת בתחילת שלב ה-ReadWrite, אחרי שהסימולטור עיבד את הקצה. ה-DUT דוגם את הישן, וכל
      coroutine שקורא אחרי `RisingEdge` רואה את הישן : כמו `<=`. ‏`Immediate` כותב מיד, בתוך
      הקצה, כמו `=`, והתיעוד של cocotb מזהיר שכתיבה כזו ב-Verilog היא לא דטרמיניסטית.

    כל הגרסאות, על אותו גירוי ב-Verilator 5.053 (הטסטים של השאלה מריצים את כולן) :

    <!-- gen 5 -->

    | הגרסה | הכתיבה של ה-driver | ה-DUT לוקח | ה-monitor קורא | שגיאות |
    |---|---|:-:|:-:|---|
    | ב-SystemVerilog, כמו שנמצאה | ‏`=` ב-Active, בין שני הקוראים | החדש | הישן | 6 : במחזורים 2, 3, 5, 7, 8 ו-10 |
    | אותה סביבה, `drive()` ראשון ב-fork | ‏`=` ב-Active, לפני שני הקוראים | החדש | החדש | 0 |
    | רק ה-monitor דרך clocking block | ‏`=` ב-Active | החדש | הישן, מה-Preponed | 6 : במחזורים 2, 3, 5, 7, 8 ו-10 |
    | רק ה-monitor בירידה של השעון | ‏`=` ב-Active | החדש | הכול אחרי הקצה | 6 : במחזורים 1, 2, 4, 6, 7 ו-9 |
    | התיקון : clocking block, בשני הסדרים | ב-Re-NBA | הישן | הישן, מה-Preponed | 0 |
    | תיקון : `<=` ב-driver | ב-NBA | הישן | הישן | 0 |
    | תיקון : driver בירידה של השעון | חצי מחזור לפני הקצה | היחיד | היחיד | 0 |
    | ב-cocotb, כמו שנמצאה (`Immediate`) | מיד, בתוך הקצה | החדש | הישן | 6 : במחזורים 2, 3, 5, 7, 8 ו-10 |
    | אותה סביבה, ה-driver מתחיל ראשון | מיד, לפני שני הקוראים | החדש | החדש | 0 |
    | אותה סביבה, ה-monitor ב-`ReadOnly()` | מיד, בתוך הקצה | החדש | הכול אחרי הקצה | 6 : במחזורים 1, 2, 4, 6, 7 ו-9 |
    | התיקון : כתיבה רגילה, בשני הסדרים | ב-ReadWrite, אחרי הקצה | הישן | הישן | 0 |
    | התיקון, ה-monitor ב-`ReadOnly()` | ב-ReadWrite, אחרי הקצה | הישן | הכול אחרי הקצה | 0 |

    <!-- /gen -->

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לתקן רק את ה-monitor"
    ה-DUT קורא את אותה כניסה באותו קצה, ולכן הוא חלק מה-race. ‏monitor שדוגם דרך clocking block
    עם driver שעדיין כותב ב-`=` מדווח על אותן שש שגיאות ב-Verilator : הוא כבר קרא את הערך הישן
    קודם, וה-DUT עדיין לוקח את החדש. ב-cocotb, ‏monitor שקורא ב-`ReadOnly()` עם driver של
    `Immediate` רואה את מה שה-DUT לקח, אבל גם את היציאה אחרי הקצה, ומדווח שוב על שש שגיאות, מחזור
    אחד מוקדם יותר. מתקנים את הכתיבה, ואחר כך בוחרים נקודת דגימה אחת לכל האותות.

??? trap "מלכודת : ״אצלי זה עובר״"
    מספיק להחליף את הסדר ב-fork, `drive()` לפני `monitor()`, כדי ש-Verilator יראה 0 שגיאות : עכשיו
    ה-driver רץ ראשון, וה-monitor וה-DUT רואים שניהם את הערך החדש. ה-race לא נעלם : ה-DUT עדיין
    לוקח כל פריט באותו קצה שבו הוא נכתב, וסימולטור שמריץ את ה-`always_ff` לפני ה-driver יראה את
    השגיאות בצד השני. טסט שעובר או נכשל לפי הסדר של שורות ב-fork הוא לא טסט.

??? trap "מלכודת : צורת הגל מסתירה את הסדר"
    ה-dump שומר ערך אחד לכל אות בכל צעד זמן, הערך שבסופו. שני הערכים של `in_data` בקצה, ומי קרא
    כל אחד מהם, לא מופיעים בו. הרמז היחיד הוא ש-`out_data` מתחלף באותו קצה כמו `in_data`, השהיה
    של אפס מחזורים לרגיסטר. כשבגל כניסה מתחלפת בדיוק על הקצה שדוגם אותה, הסביבה יצרה הפרה של
    hold בסימולציה בלי השהיות.

??? trap "מלכודת : לחפש את הבאג ב-DUT"
    השגיאות כאן אמיתיות רק בסביבה. זה המקרה ההפוך מ-[שאלה 0111](0111-passing-test-broken-dut.md),
    שבה טסט עובר על DUT שבור. בשני המקרים מתחילים מאותה שאלה : מה כל צד של הבדיקה ראה בפועל,
    ובאיזה רגע.

??? followup "שאלות המשך"
    - **למה `#1step` ולא `#0` ב-input של clocking block?**

        ??? fu-answer "תשובה"
            ‏input עם `#0` נדגם באזור ה-Observed, אחרי ה-NBA של הקצה, ולכן הוא רואה יציאות שה-DUT
            כבר עדכן בקצה הזה, וגם כתיבות של `=` מאותו Active. ‏`#1step` הוא הערך שלפני הקצה, אותו
            ערך שה-`always_ff` דוגם.

    - **מה היה משנה program block?**

        ??? fu-answer "תשובה"
            לפי התקן, התהליכים של program רצים באזור ה-Reactive, אחרי ה-Active וה-NBA של ה-DUT,
            ולכן driver שכותב ב-`=` מתוך program לא נראה ל-DUT באותו קצה. ‏Verilator 5.053 לא מפריד
            את האזורים האלה : בטסטים של השאלה driver כזה מתוך program עדיין נלקח באותו קצה.

    - **‏scoreboard שמשווה לפי הסדר, עם תור, היה מוצא את השגיאות?**

        ??? fu-answer "תשובה"
            לא. שני הצדדים רואים את אותו רצף, 6, 10, 10, 3, 7, 7, רק מוזז במחזור, ותור לא בודק
            מתי. הוא היה מעביר את הטסט, והבעיה, ה-DUT שלוקח פריטים קצה אחד מוקדם מהכוונה, הייתה
            נשארת. השהיה בודקים במפורש (ראו גם [שאלה 0050](0050-out-of-order-scoreboard.md)).

    - **מה ראה monitor שדוגם בירידה של השעון, עם ה-driver המקורי?**

        ??? fu-answer "תשובה"
            בירידה הכול יציב, אבל ה-DUT כבר לקח את הערך החדש בעלייה. ה-monitor רואה כניסה ויציאה
            של אותו פריט באותו חצי מחזור, ומודל של השהיה אחת עדיין נכשל. דגימה בצד השני לא מתקנת
            race של הכתיבה.
