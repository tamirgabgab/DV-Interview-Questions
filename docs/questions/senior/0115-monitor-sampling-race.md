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

ה-DUT, `add1`, הוא רגיסטר עם מחבר : בכל עלייה של השעון ה-`always_ff` שלו כותב
`out_valid <= in_valid` ו-`out_data <= in_data + 1`, כך שכל פריט מופיע ביציאה מחזור אחד אחרי
שנכנס. לסביבת הבדיקה שלו יש שתי גרסאות, ב-cocotb וב-SystemVerilog, והן בנויות אותו דבר : driver
ששולח עשרה מחזורים של גירוי, ו-monitor עם מודל, שבודק בכל קצה שהיציאה היא הכניסה של הקצה הקודם
ועוד 1. ה-monitor מתחיל לפני ה-driver (הוא הענף הראשון ב-fork), כדי לא לפספס אף מחזור. השעון
וההדפסות שמסביב שגרתיים, ואלה ה-driver וה-monitor :

=== "Python"
    ```python title="race_tb.py (cocotb)" linenums="1"
    # (in_valid, in_data) of every cycle; in_data holds while in_valid is low
    STIM = [(1, 5), (1, 9), (1, 9), (0, 9), (0, 9), (1, 2), (1, 6), (1, 6), (0, 6), (0, 6)]


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
    ```

=== "SystemVerilog"
    ```systemverilog title="race_tb (SystemVerilog)" linenums="1"
    bit         V[N] = '{1, 1, 1, 0, 0, 1, 1, 1, 0, 0};   // in_valid of every cycle
    logic [7:0] D[N] = '{5, 9, 9, 9, 9, 2, 6, 6, 6, 6};   // in_data, held while in_valid is low

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
    ```

על Verilator 5.053 שתי הגרסאות מדווחות על אותן שש שגיאות :

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

צוות ה-RTL בדק את `add1` ולא מצא כלום. מצאו את הבאג, והסבירו למה השגיאות נופלות בדיוק על
המחזורים 2, 3, 5, 7, 8 ו-10, ולמה לא על 1, 4, 6 ו-9. אחר כך תקנו את שתי הגרסאות, והסבירו לפי
אזורי התזמון של SystemVerilog למה התיקון עובד.

??? interviewer "מה המראיין בודק"
    - **‏race מול באג :** האם המועמד רואה שהשגיאות תלויות בגירוי ולא בחשבון : הן נופלות רק אחרי
      קצוות שבהם הכניסה השתנתה.
    - **אזורי התזמון :** מה רץ ב-Active, מה נדחה ל-NBA, ולמה clocking block דוגם ב-Preponed ודוחף
      ב-Re-NBA. וב-cocotb : מתי כתיבה מגיעה לסימולטור.
    - **שלושה צדדים לקצה :** ה-driver כותב, ה-DUT וה-monitor קוראים, והשפה לא קובעת את הסדר.

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
        ולכן כל קצה שבו הכניסה השתנתה נותן שגיאה בקצה הבא. התיקון, clocking block ב-SystemVerilog
        וכתיבה רגילה בלי `Immediate` ב-cocotb, כותב רק אחרי שכולם קראו : 0 שגיאות, בכל סדר.

    #### הרעיון { .sol-idea }

    בקצה שפותח את מחזור 2 שלושה תהליכים נוגעים ב-`in_data` : ה-driver כותב 9, ה-monitor קורא,
    וה-`always_ff` של ה-DUT קורא. עם `=` שלושתם רצים באזור ה-Active, והשפה לא קובעת את הסדר
    ביניהם (IEEE 1800, סעיף 4.7). ‏Verilator 5.053 מריץ את התהליכים שמחכים ל-`@(posedge clk)`
    בסדר שבו התחילו לחכות, ואת ה-`always_ff` אחריהם (כך בריצות של השאלה, לא מובטח) : ה-monitor
    קורא 5, ה-driver כותב 9, וה-DUT לוקח 9. ה-DUT לא טועה, אבל ה-monitor חושב שעבר 5, מצפה ל-6
    בקצה הבא, ומקבל 10. התיקון נותן לכל ערך בקצה רגע אחד מוגדר : קוראים את מה שהיה **לפני**
    הקצה, וכותבים **אחרי** שכל הקוראים קראו.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מה משותף לשגיאות :** כל שגיאה באה קצה אחד אחרי קצה שבו `in_valid` או `in_data` השתנו.
    2. **מי רואה מה :** ה-driver כותב ב-`=` באזור ה-Active. ה-monitor רץ לפניו ורואה את הישן,
       ה-DUT רץ אחריו ורואה את החדש.
    3. **התיקון :** כתיבה שאף קורא לא רואה באותו קצה, ודגימה של מה שהיה לפניו. אותו גירוי נותן
       0 שגיאות, גם כשמחליפים את הסדר של ה-monitor וה-driver.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="race_tb.py (fixed)" hl_lines="4 5"
        async def drive(dut):
            for valid, data in STIM:
                await RisingEdge(dut.clk)
                dut.in_valid.value = valid                   # (1)!
                dut.in_data.value = data
        ```

        1. כתיבה רגילה נשמרת בתור, ו-cocotb מחיל אותה רק בשלב ה-ReadWrite, אחרי שהסימולטור עיבד
           את הקצה : כמו `<=`. ה-DUT וכל coroutine שקורא אחרי `RisingEdge` רואים את הישן. ה-monitor
           לא משתנה.

    === "SystemVerilog"
        ```systemverilog title="race_tb (fixed)" linenums="1" hl_lines="1 2 5 6 11 12 13"
        clocking drv_cb @(posedge clk);            // the driver's side (1)
          output #0 in_valid, in_data;
        endclocking

        clocking mon_cb @(posedge clk);            // the monitor's side (2)
          input #1step in_valid, in_data, out_valid, out_data;
        endclocking

        task automatic drive();
          foreach (V[i]) begin
            @(drv_cb);
            drv_cb.in_valid <= V[i];
            drv_cb.in_data  <= D[i];
          end
        endtask
        ```

        1. ‏output עם skew של `#0` : ה-clocking block דוחף את הערך באזור ה-Re-NBA של הקצה, אחרי
           שה-`always_ff` של ה-DUT קרא את הכניסה ב-Active ועדכן את היציאה ב-NBA.
        2. ‏input עם skew של `#1step` (גם ברירת המחדל) : הערך מסוף צעד הזמן הקודם, אזור
           ה-Preponed, לפני שמישהו נגע בו בקצה. כך ה-monitor רואה את מה שה-DUT דוגם.

        ה-monitor משתנה רק בקריאות : הוא מחכה ל-`@(mon_cb)` במקום ל-`@(posedge clk)`, וקורא
        `mon_cb.in_valid`, ‏`mon_cb.out_data` וכן הלאה במקום את האותות עצמם.

    #### למה זה נכון { .sol-proof }

    **השגיאות, קצה אחרי קצה.** בקצה \( k \) ה-driver כותב את השורה ה-\( k \) של הגירוי, וה-DUT
    לוקח אותה מיד. ה-monitor קורא את השורה הקודמת, שעוד נמצאת שם כשהוא רץ. היציאה בקצה \( k \) היא
    מה שה-DUT לקח בקצה הקודם ועוד 1, וה-monitor מצפה למה שהוא עצמו קרא שם ועוד 1. לכן בקצה
    \( k \) יש שגיאה בדיוק כשבקצה \( k - 1 \) ה-monitor קרא שורה אחרת מזו שה-DUT לקח, כלומר
    כשהכניסה השתנתה. במחזור 1 אין קצה קודם, ולפני מחזורים 4, ‏6 ו-9 שתי השורות זהות : 9 אחרי 9,
    ‏`in_valid` נמוך אחרי נמוך, 6 אחרי 6.

    **נסו בעצמכם.** התיבה מריצה את עשרת המחזורים אירוע אחרי אירוע, ומפרקת כל קצה לאזורים שלו.
    היא נפתחת על הסביבה כמו שנמצאה. החליפו את הכתיבה של ה-driver, את נקודת הדגימה של ה-monitor
    או את הסדר של התהליכים, וראו מה כל אחד קורא, ועל אילו מחזורים ה-monitor מדווח :

    <div class="explorer" data-kind="edgerace"></div>

    **למה התיקון עובד.** ה-monitor של ה-clocking block דוגם ב-Preponed, לפני כל דבר שקורה בקצה,
    וה-DUT קורא ב-Active, לפני שהכתיבה של `drv_cb` מגיעה ב-Re-NBA : שניהם רואים את השורה שנכתבה
    בקצה הקודם, בכל סדר. גם `<=` ב-driver מספיק לבד : הכתיבה נדחית ל-NBA, אחרי הקריאות של
    ה-Active. וב-cocotb כתיבה רגילה נשמרת בתור (`_schedule_write` ב-`cocotb/handle.py`) עד שלב
    ה-ReadWrite, אחרי הקצה. ‏`Immediate` כותב מיד, כמו `=`, והתיעוד של cocotb מזהיר שכתיבה כזו
    ב-Verilog היא לא דטרמיניסטית.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לתקן רק את ה-monitor"
    ה-DUT קורא את אותה כניסה באותו קצה, ולכן הוא חלק מה-race. ‏monitor שדוגם דרך clocking block,
    עם driver שעדיין כותב ב-`=`, מדווח ב-Verilator על אותן שש שגיאות : הוא קורא את הישן, וה-DUT
    עדיין לוקח את החדש. מתקנים את הכתיבה, ואחר כך בוחרים נקודת דגימה אחת לכל האותות.

??? trap "מלכודת : ״אצלי זה עובר״"
    מספיק להחליף את הסדר ב-fork, `drive()` לפני `monitor()`, כדי ש-Verilator יראה 0 שגיאות. ה-race
    לא נעלם : ה-DUT עדיין לוקח כל פריט באותו קצה שבו נכתב, וסימולטור שמריץ את ה-`always_ff` לפני
    ה-driver יראה שגיאות. טסט שעובר או נכשל לפי הסדר של שורות ב-fork הוא לא טסט.

??? trap "מלכודת : לחפש את הבאג ב-DUT"
    השגיאות כאן אמיתיות רק בסביבה. זה המקרה ההפוך מ-[שאלה 0111](0111-passing-test-broken-dut.md),
    שבה טסט עובר על DUT שבור. בשני המקרים שואלים קודם מה כל צד של הבדיקה ראה בפועל, ובאיזה רגע.

??? followup "שאלות המשך"
    - **למה `#1step` ולא `#0` ב-input של clocking block?**

        ??? fu-answer "תשובה"
            ‏input עם `#0` נדגם באזור ה-Observed, אחרי ה-NBA של הקצה, ולכן הוא רואה יציאות שה-DUT
            כבר עדכן בקצה הזה. ‏`#1step` הוא הערך שלפני הקצה, אותו ערך שה-`always_ff` דוגם.

    - **מה היה משנה program block?**

        ??? fu-answer "תשובה"
            לפי התקן, התהליכים של program רצים באזור ה-Reactive, אחרי ה-Active וה-NBA של ה-DUT.
            ‏Verilator 5.053 לא מפריד את האזורים האלה : בטסטים של השאלה driver שכותב ב-`=` מתוך
            program עדיין נלקח באותו קצה.

    - **‏scoreboard שמשווה לפי הסדר, עם תור, היה מוצא את השגיאות?**

        ??? fu-answer "תשובה"
            לא. שני הצדדים רואים את אותו רצף, 6, 10, 10, 3, 7, 7, רק מוזז במחזור, ותור לא בודק
            מתי. השהיה בודקים במפורש (ראו גם [שאלה 0050](0050-out-of-order-scoreboard.md)).
