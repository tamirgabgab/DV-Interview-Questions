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

ה-DUT מקבל בתים בשני ערוצים, ועם כל בית ביט זוגיות (even parity, ‏`^data`). הוא סופר בכל
ערוץ, ב-`errs0` וב-`errs1`, את הפריטים שהביט שלהם שגוי. בסביבה, כמו
ב-[ארכיטקטורה של סביבת UVM](0049-uvm-testbench-architecture.md), יש agent לכל ערוץ, ובו
sequencer ו-driver. ה-driver הרגיל, `ParityDriver`, שולח שמונה בתים עם ביט נכון, והטסט הבסיסי,
`ParityTest`, מדפיס בסוף לכל driver את ה-class שלו ואת המונה של ה-DUT. כדי לבדוק את המונים
כתבו `ErrDriver`, שהופך את הביט בכל פריט רביעי, ו-`ErrTest`, שמבקש מה-factory לבנות אותו בכל
מקום שבו נבנה `ParityDriver` (type override), בלי לגעת ב-env :

=== "Python"
    ```python title="pyuvm: ErrDriver, Agent, ErrTest" linenums="1"
    class ErrDriver(ParityDriver):
        def parity(self, data):
            return super().parity(data) ^ (self.sent % 4 == 3)


    class Agent(uvm_agent):
        def build_phase(self):
            self.seqr = uvm_sequencer.create("seqr", self)
            self.drv = ParityDriver("drv", self)

        def connect_phase(self):
            self.drv.seq_item_port.connect(self.seqr.seq_item_export)


    class ErrTest(ParityTest):
        def build_phase(self):
            uvm_factory().set_type_override_by_type(ParityDriver, ErrDriver)
            self.env = Env.create("env", self)
    ```

=== "SystemVerilog"
    ```systemverilog title="UVM: err_driver, agent, err_test" linenums="1"
    function bit err_driver::parity(bit [7:0] data);
      return super.parity(data) ^ (sent % 4 == 3);
    endfunction

    function void agent::build_phase(uvm_phase phase);
      seqr = uvm_sequencer#(byte_item)::type_id::create("seqr", this);
      drv  = new("drv", this);
    endfunction

    function void err_test::build_phase(uvm_phase phase);
      parity_driver::type_id::set_type_override(err_driver::get_type());
      env = tb_env::type_id::create("env", this);
    endfunction
    ```

שאר הסביבה בבדיקות של האתר : ה-Python רץ ב-[pyuvm](https://github.com/pyuvm/pyuvm) וב-cocotb על
Verilator, וה-SystemVerilog (ל-Verilator אין UVM) נבדק מול ה-Python. הטסט היה אמור להראות שתי
שגיאות בכל ערוץ, וזה הלוג :

<!-- gen 0 -->

```text
uvm_test_top.env.agt0.drv: ParityDriver, 0 parity errors
uvm_test_top.env.agt1.drv: ParityDriver, 0 parity errors
```

<!-- /gen -->

??? interviewer "מה המראיין בודק"
    - **מה ה-factory עושה :** ‏override הוא רשומה בטבלה, ומישהו צריך לשאול את הטבלה בזמן הבנייה.
    - **קריאת לוג :** האם המועמד שם לב לשם ה-class שנבנה, ולא רק למספר השגיאות.
    - **‏type מול instance :** כל המופעים של טיפוס, או רק מופע אחד לפי השם המלא שלו בעץ.
    - **דיבאג שיטתי :** להדפיס את מה שה-factory שמר ולהשוות לשם המלא, במקום לנחש נתיבים.

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
        ‏`new("drv", this)`). קריאה כזו בונה תמיד את ה-class שכתוב בה, וה-factory לא נשאל.
        התיקון : ‏`ParityDriver.create("drv", self)` (ב-SystemVerilog
        ‏`parity_driver::type_id::create("drv", this)`). אחרי התיקון שני ה-drivers הם `ErrDriver`,
        וה-DUT סופר שתי שגיאות בכל ערוץ.

    #### הרעיון { .sol-idea }

    ‏`set_type_override_by_type` לא משנה אף אובייקט ואף class. הוא רק כותב שורה בטבלה של
    ה-factory : "מי שמבקש `ParityDriver` יקבל `ErrDriver`". את הטבלה קורא רק `create`, שמקבל את
    ה-class שביקשו ואת השם של הרכיב החדש ובונה את מה שהטבלה אומרת. קריאה ישירה לבנאי לא עוברת שם :

    <!-- gen 1 -->

    <svg class="figure uv-fig" viewBox="0 0 420 256" style="max-width:28rem" role="img" aria-label="שתי דרכים לבנות את ה-driver : קריאה ישירה ל-ParityDriver בונה ParityDriver, ו-create עובר דרך ה-factory, שמחזיר ErrDriver"><defs><marker id="fo-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs><g class="uv-box is-cont"><text x="105" y="24" text-anchor="middle">ParityDriver("drv", self)</text><text x="315" y="24" text-anchor="middle">ParityDriver.create(…)</text></g><line class="uv-arrow uv-pin" x1="105" y1="36" x2="105" y2="196" marker-end="url(#fo-arrow)"/><line class="uv-arrow uv-tlm" x1="315" y1="36" x2="315" y2="76" marker-end="url(#fo-arrow)"/><g class="uv-box uv-scoreboard"><rect x="230" y="80" width="170" height="72" rx="6"/><text x="315" y="103" text-anchor="middle">factory</text><text x="315" y="121" text-anchor="middle">ParityDriver</text><text x="315" y="139" text-anchor="middle">→ ErrDriver</text></g><line class="uv-arrow uv-tlm" x1="315" y1="152" x2="315" y2="196" marker-end="url(#fo-arrow)"/><g class="uv-box"><rect x="35" y="200" width="140" height="44" rx="6"/><text x="105" y="227" text-anchor="middle">ParityDriver</text></g><g class="uv-box uv-dut"><rect x="245" y="200" width="140" height="44" rx="6"/><text x="315" y="227" text-anchor="middle">ErrDriver</text></g></svg>

    <span class="viz-legend"><span><i class="uv-key-pin"></i>קריאה ישירה לבנאי : ה-factory לא נשאל</span><span><i class="uv-key-tlm"></i>דרך create : ה-factory בוחר את ה-class</span></span>

    <!-- /gen -->

    לכן הכלל ב-UVM : כל רכיב וכל אובייקט (גם sequence ו-item) נבנים דרך ה-factory. ‏`new` אחד,
    אפילו בעומק העץ, הוא מקום שאף טסט לא יוכל להחליף.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הלוג וה-factory :** נבנה `ParityDriver`, אבל `uvm_factory().print(0)` מראה ש-`ErrDriver`
       רשום כ-type override שלו. הבעיה לא ב-DUT ולא בטסט.
    2. **השורה האשמה :** ב-`build_phase` של ה-agent, ה-sequencer נבנה ב-`create` וה-driver
       בבנאי. מתקנים את השורה הזו בלבד : ה-env וה-agent לא צריכים לדעת על `ErrDriver`.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="Agent.build_phase: the driver's line"
        self.drv = ParityDriver.create("drv", self)   # (1)!
        ```

        1. ‏`create` הוא class method : ‏pyuvm רושם ב-factory כל class שיורש מ-`uvm_void`, בלי
           מאקרו, ואין `type_id`.

    === "SystemVerilog"
        ```systemverilog title="agent::build_phase: the driver's line"
        drv  = parity_driver::type_id::create("drv", this);   // (1)!
        ```

        1. ‏`type_id::create` קיים רק ל-class שנרשם ב-`` `uvm_component_utils``. גם
           `err_driver` צריך את המאקרו, אחרת אין לו `get_type()` לתת ל-override.

    #### למה זה נכון { .sol-proof }

    אותה ריצה, עם השורה המתוקנת :

    <!-- gen 2 -->

    ```text
    uvm_test_top.env.agt0.drv: ErrDriver, 2 parity errors
    uvm_test_top.env.agt1.drv: ErrDriver, 2 parity errors
    ```

    <!-- /gen -->

    כל `ErrDriver` מהפך את הביט כש-`sent` (הפריטים שכבר נשלחו) הוא 3 או 7, שני פריטים
    מתוך שמונה. וה-env לא השתנה : טסט אחד מזריק שגיאות, טסט אחר רץ נקי, באותה סביבה.

---

### סעיף ב – override לערוץ אחד

עכשיו רוצים טסט שמזריק שגיאות רק בערוץ 1, וערוץ 0 נשאר נקי, לביקורת. עמית כתב אותו עם
instance override, וקיבל `ParityDriver` בשני הערוצים ו-0 שגיאות :

=== "Python"
    ```python title="Chan1Test"
    class Chan1Test(ParityTest):
        def build_phase(self):
            uvm_factory().set_inst_override_by_type(ParityDriver, ErrDriver, "env.agt1.drv")
            self.env = Env.create("env", self)
    ```

=== "SystemVerilog"
    ```systemverilog title="chan1_test::build_phase"
    function void chan1_test::build_phase(uvm_phase phase);
      uvm_factory factory = uvm_factory::get();
      factory.set_inst_override_by_type(parity_driver::get_type(), err_driver::get_type(), "env.agt1.drv");
      env = tb_env::type_id::create("env", this);
    endfunction
    ```

מה ההבדל בין type override ל-instance override? למה הטסט של העמית לא עבד, ואיך מוצאים את זה
בלי לנחש? תקנו.

??? tip "רמז 1"
    מה השם המלא של ה-driver של `agt1`? הלוג של הטסט כבר מדפיס אותו.

??? tip "רמז 2"
    ‏`uvm_factory().print(0)` מדפיס את ה-overrides כמו שה-factory שמר אותם. השוו לשם המלא.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏type override מחליף את הטיפוס בכל מקום שבו הוא נבנה. ‏instance override מחליף אותו רק
        ב-`create` שהשם המלא שלו מתאים לתבנית, והוא נבדק לפני ה-type override. הנתיב של העמית,
        `env.agt1.drv`, לא מתאים לשום רכיב : השם המלא מתחיל ב-`uvm_test_top`, השם שנותן `run_test`
        לטסט. התיקון : הנתיב המלא, שנבנה מ-`get_full_name()` של הטסט.

    #### הרעיון { .sol-idea }

    בכל `create` ה-factory מקבל את ה-class שביקשו ואת השם המלא של הרכיב החדש. קודם הוא משווה
    לשם את התבניות של ה-instance overrides של ה-class, לפי סדר הרישום, אחר כך את ה-type override,
    ואם אין אף אחד, בונה את ה-class שביקשו. התבנית היא glob (‏`*` לכל רצף, ‏`?` לתו אחד), והיא
    חייבת להתאים לשם **כולו**. ‏`env.agt1.drv` הוא רק סוף השם, וה-factory לא מתריע על תבנית שלא
    התאימה. בתיבה בונים את העץ צעד אחר צעד, עם `create` או `new` בכל שורה, ורואים מה ה-factory
    בדק בכל צעד ולמה נתיב לא התאים :

    <div class="explorer" data-kind="factory"></div>

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מה נבנה :** הלוג אומר ש-`uvm_test_top.env.agt1.drv` הוא `ParityDriver`. זה השם המלא,
       כמו ש-`get_full_name()` מחזיר אותו.
    2. **מה נרשם :** ‏`uvm_factory().print(0)` ב-`end_of_elaboration_phase` מראה instance override
       בנתיב `env.agt1.drv`.
    3. **ההשוואה והתיקון :** לתבנית חסר בהתחלה `uvm_test_top.`, ולכן בונים אותה
       מ-`get_full_name()` של הטסט, ולא כותבים ביד. כך גם שם אחר לטסט לא שובר אותה.

    </div>

    הלוג של העמית, עם ההדפסה של ה-factory :

    <!-- gen 3 -->

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
        ```python title="Chan1Test.build_phase: the override's line"
        path = f"{self.get_full_name()}.env.agt1.drv"   # (1)!
        uvm_factory().set_inst_override_by_type(ParityDriver, ErrDriver, path)
        ```

        1. ‏pyuvm מתאים את הנתיב עם `fnmatch`, תמיד מול השם המלא. כדי לשאול על נתיב אחד,
           `uvm_factory().find_override_by_type(ParityDriver, path)` מחזיר את ה-class שהיה נבנה שם.

    === "SystemVerilog"
        ```systemverilog title="chan1_test::build_phase: the override's line"
        string path = {get_full_name(), ".env.agt1.drv"};   // (1)!
        factory.set_inst_override_by_type(parity_driver::get_type(), err_driver::get_type(), path);
        ```

        1. ל-`uvm_component` יש גם `set_inst_override_by_type`, עם נתיב **יחסי** לרכיב שקורא לו
           (והנתיב ראשון). שם `"env.agt1.drv"` היה עובד. ב-pyuvm אין את הצורה הזו.

    #### למה זה נכון { .sol-proof }

    כל שורה בטבלה היא ריצה של `Chan1Test`, עם השורה המתוקנת של סעיף א ועם התבנית של השורה. בכל
    ריצה ה-DUT ספר 2 שגיאות בערוץ של כל `ErrDriver`, ו-0 בערוץ של `ParityDriver` :

    <!-- gen 4 -->

    | הנתיב | מי נבנה כ-`ErrDriver` |
    |---|---|
    | ‏`uvm_test_top.env.agt1.drv` | רק `agt1` |
    | ‏`env.agt1.drv` | אף אחד |
    | ‏`uvm_test_top.env.agt1` | אף אחד |
    | ‏`*.agt1.*` | רק `agt1` |
    | ‏`uvm_test_top.env.agt*.drv` | **שניהם** |

    <!-- /gen -->

    התבנית של ה-agent, `uvm_test_top.env.agt1`, לא נוגעת לאף רכיב : ה-override חל על מה שנבנה
    **בנתיב** הזה, ושם נבנה `Agent`, לא `ParityDriver`.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : ‏`new` אחד בעומק העץ"
    מספיק `new` אחד, ב-agent שמישהו כתב פעם, כדי שאף override לא יגיע לרכיב הזה, בלי שום
    שגיאה. כך גם ל-sequence item שנבנה ב-`new`. ב-code review מחפשים `new(` של רכיבים ו-items.

??? trap "מלכודת : ה-override עבד, והשגיאות עדיין לא שם"
    ב-SystemVerilog, אם `parity` של `parity_driver` לא מוגדרת `virtual`, הקריאה בתוך
    `run_phase` של ה-class הבסיסי קוראת לגרסה הבסיסית גם באובייקט של `err_driver`. הלוג יראה
    `err_driver`, וה-DUT 0 שגיאות. ב-Python כל מתודה היא virtual.

??? trap "מלכודת : ‏override לפני `run_test` ב-pyuvm"
    ב-pyuvm, ‏`run_test` מנקה את ה-overrides ואת `ConfigDB` לפני שהוא בונה את הטסט. מה שנקבע
    בבדיקת ה-cocotb לפני הקריאה נמחק בשקט. ב-SystemVerilog, override מה-`initial` של ה-top נשאר.

??? followup "שאלות המשך"
    - **‏type ו-instance יחד :** ‏type override ל-`ErrDriver`, ו-instance override של
      `agt0.drv` ל-class שלישי. מה נבנה בכל ערוץ?

        ??? fu-answer "תשובה"
            ה-instance override קובע בנתיב שהוא מתאים לו, וה-type override בכל השאר : ב-`agt0`
            נבנה ה-class השלישי, וב-`agt1` ‏`ErrDriver`.

    - **הזמן :** האם משנה אם הקריאה נמצאת אחרי `Env.create`? ומה אם היא עוברת ל-`connect_phase`?

        ??? fu-answer "תשובה"
            אחרי `Env.create` היא עדיין עובדת : ה-driver נבנה שתי רמות למטה, ב-`build_phase` של
            ה-agent, אחרי שה-`build_phase` של הטסט הסתיים. ב-`connect_phase` העץ כבר שלם, והרשומה
            לא משנה אף רכיב.

    - **‏override של override :** ‏`A` מוחלף ב-`B`, ו-`B` מוחלף ב-`C`. מה נבנה כשמבקשים `A`?

        ??? fu-answer "תשובה"
            ‏`C` : ה-factory ממשיך לחפש override גם ל-class שמצא. לולאה (`A` ל-`B` ו-`B` ל-`A`)
            ‏pyuvm מזהה, ומדפיס שגיאה במקום להיתקע.

    - **‏override של sequence item :** איך הייתם מזריקים את אותן שגיאות בלי לגעת ב-driver?

        ??? fu-answer "תשובה"
            ‏item עם שדה `bad_parity`, תת-class שלו שמדליק אותו, ו-type override של ה-item. זה
            עובד רק אם ה-sequence בונה את ה-items ב-`create`, וה-driver קורא את השדה.
