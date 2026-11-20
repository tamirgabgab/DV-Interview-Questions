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

ה-DUT הוא צינור (pipeline) של ארבעה שלבים : כל פריט שנכנס עם `in_valid` יוצא עם `out_valid`
ארבעה מחזורים אחר כך, והנתון שלו גדל ב-1. השעון 10 ns, והוא מתחיל בנמוך : עליות ב-5, 15, 25
ns וכן הלאה.

הסביבה היא סביבת UVM רגילה, כמו בשאלה [0049](0049-uvm-testbench-architecture.md). ה-sequence
שולחת 8 פריטים. ה-driver מחזיק את האיפוס בשתי העליות הראשונות, ואז מוסר פריט בכל מחזור. מוניטור
כניסה ומוניטור יציאה דוגמים בירידת השעון, ושולחים ל-scoreboard את מה שראו. ה-scoreboard משווה
בסוף, ב-`check_phase`, ונכשל אם יש אי-התאמה או פריט שנכנס ולא יצא. זה ה-test, ב-pyuvm וב-UVM של
SystemVerilog :

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

‏UVM ב-SystemVerilog לא רץ בבדיקות של האתר, כי ל-Verilator אין ספריית UVM. גרסת ה-Python,
‏pyuvm מעל cocotb ו-Verilator, כן רצה, וכל המספרים בעמוד באים ממנה.

השורות של ה-scoreboard בלוג של הריצה :

<!-- gen 0 -->

```text
INFO     [uvm_test_top.env.sb] 0 ns: 0 compared, 0 mismatches, 0 missing
INFO     [uvm_test_top.env.sb] TEST PASSED
```

<!-- /gen -->

??? interviewer "מה המראיין בודק"
    - **מתי ה-run phase נגמר :** לא כשה-sequence נגמרת, אלא כשאין אף objection מורם.
    - **איפה מרימים objection :** ב-test, סביב ה-sequence, ולא ברכיבים שרצים לנצח.
    - **פריטים שבדרך :** ה-latency של ה-DUT, ה-drain time, ומה ה-scoreboard בודק בסוף.
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
        ו-0 יצאו, ולכן אין חסרים ו"עבר". התיקון : ‏`raise_objection` ב-test לפני `seq.start`,
        ו-`drop_objection` אחרי שהיא חוזרת.

    #### הרעיון { .sol-idea }

    ‏UVM מריץ את ה-phases בסדר קבוע : ‏`build_phase` מלמעלה למטה, ‏`connect_phase` מלמטה למעלה,
    אחריהם `run_phase`, היחיד שצורך זמן סימולציה, ובסוף `check_phase` ו-`report_phase`,
    פונקציות בלי זמן. ב-`run_phase` ה-task של כל רכיב רץ במקביל לאחרים, ושל ה-driver ושל
    המוניטורים הוא לולאה אינסופית. לכן UVM לא מחכה שה-tasks ייגמרו, אלא סופר objections : רכיב
    שמרים objection אומר "אני עוד באמצע", וה-run phase נגמר כשהמונה חוזר ל-0. בלי אף objection
    המונה 0 מההתחלה, וה-run phase נגמר מיד.

    ה-scoreboard לא מצא כלום כי לא היה מה למצוא : מוניטור הכניסה לא ראה אף פריט, ולכן גם אף פריט
    לא חסר. ‏pyuvm לפחות מזהיר, ‏`You did not call self.raise_objection() in any run_phase`. ‏UVM
    ב-SystemVerilog שותק.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הסימן בלוג :** ‏`0 ns`, ‏`0 compared`. טסט ששולח 8 פריטים לא נגמר בזמן 0.
    2. **הסיבה :** אין objection, ולכן ה-run phase נגמר מיד, וה-sequence לא הספיקה לשלוח כלום.
    3. **התיקון :** ה-test מרים objection בשורה הראשונה של `run_phase`, ומוריד אחרי ש-`seq.start`
       חוזרת.
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

        1. לפני כל `await` : ה-run phase בודק אם הורם objection מיד אחרי שכל ה-tasks התחילו.
        2. חוזרת כשה-driver קרא ל-`item_done` של הפריט האחרון.

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
    חוזרת, ה-objection יורד, והריצה נגמרת ב-95 ns.

---

### סעיף ב – ארבעה פריטים שלא הגיעו

אחרי התיקון של סעיף א, ה-scoreboard של `ObjectionTest` כותב :

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
        הפריטים האחרונים עוד בצינור, ויוצאים ב-100 עד 130 ns, אחרי שהריצה נגמרה. ה-drain time
        הוא הזמן ש-UVM מחכה אחרי שהמונה מגיע ל-0, לפני שהוא מסיים את ה-phase. הוא צריך לכסות את
        ה-latency : כאן יותר מ-35 ns, ולכן 40 ns.

    #### הרעיון { .sol-idea }

    ה-objection ירד כשה-stimulus נגמר, לא כשהבדיקה נגמרה. בין השניים עומד ה-latency : פריט
    שנכנס בעלייה של \( t \) נראה ביציאה ב-\( t + 35 \) ns. ב-95 ns, כשהאחרון נכנס, פריטים 4
    עד 7 עוד בצינור :

    <!-- gen 2 -->

    <svg class="perf-chart q113-timeline" viewBox="0 0 400 158" style="max-width:34rem" role="img" aria-label="8 items: taken by the DUT at 25 to 95 ns, seen at the output at 60 to 130 ns; the objection drops at 95 ns, the drain ends at 135 ns"><rect class="hist-near" x="262.2" y="14" width="94.4" height="112"/><text class="tick" x="38.0" y="144" text-anchor="middle" style="font-size:14px">0</text><text class="tick" x="156.0" y="144" text-anchor="middle" style="font-size:14px">50</text><text class="tick" x="274.0" y="144" text-anchor="middle" style="font-size:14px">100</text><text class="tick" x="392.0" y="144" text-anchor="end" style="font-size:14px">150 ns</text><line class="axis" x1="38" x2="392" y1="126" y2="126"/><text class="tick" x="32" y="45" text-anchor="end" style="font-size:14px">in</text><text class="tick" x="32" y="97" text-anchor="end" style="font-size:14px">out</text><rect class="ink-line" x="74.9" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="85.2" y="45" text-anchor="middle" style="font-size:14px">0</text><rect class="s1-line" x="169.3" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="179.6" y="97" text-anchor="middle" style="font-size:14px">0</text><rect class="ink-line" x="98.5" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="108.8" y="45" text-anchor="middle" style="font-size:14px">1</text><rect class="s1-line" x="192.9" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="203.2" y="97" text-anchor="middle" style="font-size:14px">1</text><rect class="ink-line" x="122.1" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="132.4" y="45" text-anchor="middle" style="font-size:14px">2</text><rect class="s1-line" x="216.5" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="226.8" y="97" text-anchor="middle" style="font-size:14px">2</text><rect class="ink-line" x="145.7" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="156.0" y="45" text-anchor="middle" style="font-size:14px">3</text><rect class="s1-line" x="240.1" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="250.4" y="97" text-anchor="middle" style="font-size:14px">3</text><rect class="ink-line" x="169.3" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="179.6" y="45" text-anchor="middle" style="font-size:14px">4</text><rect class="s2-line" x="263.7" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="274.0" y="97" text-anchor="middle" style="font-size:14px">4</text><rect class="ink-line" x="192.9" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="203.2" y="45" text-anchor="middle" style="font-size:14px">5</text><rect class="s2-line" x="287.3" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="297.6" y="97" text-anchor="middle" style="font-size:14px">5</text><rect class="ink-line" x="216.5" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="226.8" y="45" text-anchor="middle" style="font-size:14px">6</text><rect class="s2-line" x="310.9" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="321.2" y="97" text-anchor="middle" style="font-size:14px">6</text><rect class="ink-line" x="240.1" y="28" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="250.4" y="45" text-anchor="middle" style="font-size:14px">7</text><rect class="s2-line" x="334.5" y="80" width="20.6" height="24" rx="3" fill="none" stroke-width="2"/><text class="tick" x="344.8" y="97" text-anchor="middle" style="font-size:14px">7</text><line class="ink-line" x1="262.2" x2="262.2" y1="14" y2="126" stroke-width="1.5" stroke-dasharray="5 4"/><line class="ink-line" x1="356.6" x2="356.6" y1="14" y2="126" stroke-width="1.5"/><text class="tick" x="262.2" y="12" text-anchor="middle" style="font-size:13px">95</text><text class="tick" x="356.6" y="12" text-anchor="middle" style="font-size:13px">135</text></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="s1"></i>פריט שיצא לפני 95 ns : נבדק בשתי הריצות</span><span><i class="s2"></i>פריט שעוד היה בצינור : נבדק רק עם drain</span><span><i class="ink-dash"></i>הורדת ה-objection בלי drain, ב-95 ns</span><span><i class="ink"></i>סוף הריצה עם drain של 40 ns, ב-135 ns</span></span>

    <!-- /gen -->

    ב-UVM ה-drain time נקבע על ה-objection של ה-phase : כשהמונה מגיע ל-0, ‏UVM מחכה עוד זמן
    ה-drain, ואם מישהו מרים objection בזמן הזה, ההמתנה מתחילה מחדש. ‏pyuvm 5.0.0 לא מממש drain
    time : אין לו `set_drain_time`. המקבילה שם היא להחזיק את ה-objection עוד אותו זמן.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מי חסר :** ארבעה, בדיוק מספר השלבים של הצינור.
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

        1. ל-pyuvm אין drain time, ולכן ה-test מחזיק את ה-objection עוד 40 ns. בזמן הזה
           המוניטורים ממשיכים לדגום.

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

        1. ב-UVM 1.1 כותבים `phase.phase_done.set_drain_time(this, 40ns)`.

    #### למה זה נכון { .sol-proof }

    ביט ה-valid של פריט \( i \) נכתב לשלב הראשון בעלייה של \( 25 + 10i \) ns, ולרביעי שלוש
    עליות אחר כך, ב-\( 55 + 10i \) ns. מוניטור היציאה דוגם בירידה הבאה, ב-\( 60 + 10i \) ns.
    הריצה נגמרת ב-\( 95 + D \) ns, ו-`check_phase` בודק כל פריט שנראה לפני כן, כלומר כל \( i \)
    עם \( 60 + 10i < 95 + D \). עם \( D = 0 \) אלה פריטים 0 עד 3, ועם \( D > 35 \) כל השמונה :

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

    **נסו בעצמכם.** התיבה מריצה את אותה סביבה מחזור אחרי מחזור : הפריטים בצינור, המונה של
    ה-objections, ומה ה-scoreboard ראה. כבו את ה-objection של ה-test, ושנו את ה-drain : הריצה
    נגמרת ב-0, ב-95 ns או ב-\( 95 + D \). סמנו "המוניטור מרים objection" כדי לראות ריצה שלא נגמרת
    (שאלת ההמשך הראשונה) :

    <div class="explorer" data-kind="objrun"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : objection שמורם מאוחר או יורד מוקדם"
    ה-run phase בודק אם הורם objection מיד אחרי שכל ה-tasks שלו התחילו. ‏test שמחכה קודם
    למחזור שעון, ורק אז מרים, מאחר : הריצה כבר נגמרה בזמן 0. כך גם test שמרים, מפעיל את
    ה-sequence ברקע (`cocotb.start_soon`, או `fork ... join_none`) ומוריד מיד : המונה עלה וירד
    באותו רגע. במקרה השני ‏pyuvm גם לא מזהיר, כי objection כן הורם.

??? trap "מלכודת : scoreboard שעובר על אפס"
    ה-scoreboard של השאלה בודק אי-התאמות וחסרים, ושניהם 0 כשלא נכנס כלום. בדיקה שלא בדקה אף
    פריט צריכה להיכשל : ב-`check_phase` שורה כמו `if not seen: self.logger.error(...)`, או
    השוואה של מספר הפריטים לזה שה-sequence התכוונה לשלוח.

??? trap "מלכודת : drain time במקום לחכות לפריטים"
    ‏drain קבוע הוא ניחוש של ה-latency. ‏DUT עם backpressure, או ש-latency שלו תלוי בנתונים,
    יעבור בריצה אחת וייכשל באחרת, ו-drain ארוך מדי מאריך כל טסט. סוף מדויק יותר : ה-test מחכה,
    אחרי ה-sequence, שה-scoreboard לא יחכה לאף פריט, עם גבול זמן.

??? followup "שאלות המשך"
    - **מוניטור שמחזיק objection :** עמית כתב מוניטור יציאה שמרים objection בתחילת `run_phase`,
      לפני הלולאה, ומוריד אחריה, "כדי שהטסט יחכה לו". מה קורה?

        ??? fu-answer "תשובה"
            הלולאה אינסופית, ולכן ההורדה לא מתבצעת אף פעם : המונה לא חוזר ל-0, והריצה לא נגמרת.
            ‏timeout של 100 µs (‏`with_timeout` סביב `run_test`) עוצר אותה, ו-`str(ObjectionHandler())`
            מראה objection אחד שנשאר, של `uvm_test_top.env.mon_out`.

    - **‏timeout :** למה לא לסמוך על ה-timeout של ברירת המחדל של UVM?

        ??? fu-answer "תשובה"
            כי הוא 9200 s של זמן סימולציה : ריצה תקועה תופסת מכונה שעות לפני שהיא נכשלת. ‏timeout
            קצר (‏`uvm_top.set_timeout`) נכשל מהר, ו-`+UVM_OBJECTION_TRACE` מראה מי הרים ולא הוריד.

    - **ספירה :** מה קורה כש-test מרים objection פעמיים ומוריד פעם אחת? וכשהוא מוריד בלי שהרים?

        ??? fu-answer "תשובה"
            ‏objection הוא מונה, לא דגל : אחרי שתי הרמות והורדה אחת המונה 1, והריצה לא נגמרת.
            הורדה בלי הרמה היא שגיאה : ב-UVM ‏`UVM_ERROR` עם `OBJTN_ZERO`, וב-pyuvm אזהרה, והמונה
            לא יורד מתחת ל-0.

    - **‏sequence שמרימה :** אפשר להרים את ה-objection בתוך ה-sequence הראשית?

        ??? fu-answer "תשובה"
            כן, ב-UVM 1.2 : ‏`set_automatic_phase_objection(1)`, או `starting_phase` של sequence
            שהופעלה כ-default sequence. ב-pyuvm אין לזה מקבילה, ושם הוא נשאר ב-test.

    - **‏phase_ready_to_end :** מה הוא נותן שה-drain time לא נותן?

        ??? fu-answer "תשובה"
            ‏UVM קורא לו כשהמונה של phase מגיע ל-0. ה-scoreboard יכול להרים שם objection, לחכות
            שהתור שלו יתרוקן ולהוריד : סוף שתלוי במה שקרה בפועל, לא בזמן קבוע.
