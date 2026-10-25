---
id: 23
title: מודל ייחוס ל-PCIe Endpoint – כתיבה, קריאה ושידור Completions
level: senior
difficulty: medium
kind: dv
tags: [protocols, pcie, python, systemverilog]
source: ""
added: 2026-10-19
---

## השאלה

ב-PCIe, ה-Endpoint משמש כ-**Completer** : הוא מקבל בקשות זיכרון מה-Requester (למשל
ה-Root Complex), כותב לזיכרון שלו ומחזיר ממנו נתונים. כתבו **מודל ייחוס** (reference model)
של Endpoint כזה, מהסוג שמחברים ל-scoreboard בסביבת אימות : המודל מקבל את אותן בקשות
שה-DUT מקבל, ומייצר את ה-Completions שמותר ל-DUT לשלוח.

המודל מקבל שני סוגי בקשות :

- **‏Memory Write** (MemWr) : כתובת, אורך בבתים ונתונים. זו בקשת posted : המודל מעדכן את
  הזיכרון ולא מחזיר כלום.
- **‏Memory Read** (MemRd) : כתובת, אורך בבתים, Requester ID ו-Tag. המודל קורא מהזיכרון
  ומחזיר Completion אחד או יותר עם נתונים (CplD).

הפרמטרים קבועים : **‏MRRS = 256**, **‏MPS = 256** ו-**‏RCB = 128** בתים (ההגדרות של
שלושתם מוסברות בשאלה [0020](0020-pcie-completion-splits.md)). כללי ה-Completions :

1. כל Completion נושא לכל היותר MPS בתים, וכל הבתים של הבקשה חוזרים : בלי חסר, בלי עודף,
   ובלי לערבב נתונים של שתי בקשות ב-Completion אחד.
2. מותר לחתוך בקשה ל-Completions רק בגבולות RCB, כלומר בכתובות שהן כפולות של 128. ‏RCB
   אינו גודל : Completion יכול להיות קצר מ-128 בתים או ארוך מהם.
3. ה-Completions של אותה בקשה נשלחים **בסדר כתובות עולה**. בין בקשות שונות מותר לשלב
   (interleaving).
4. כל Completion מעתיק את ה-Requester ID ואת ה-Tag של הבקשה, ושדה ה-**Byte Count** שלו
   הוא מספר הבתים שעוד לא הוחזרו, כולל הבתים שבו.
5. לפני שידור ה-Completions של בקשה המודל ממתין זמן אקראי, ובכל מחזור הוא משדר לכל היותר
   Completion אחד.

הזיכרון של ה-Endpoint הוא **associative array של בלוקים באורך RCB** : המפתח הוא כתובת
הבלוק (כפולה של 128) והערך הוא 128 בתים. בית שמעולם לא נכתב נקרא כאפס. הממשק של המודל
הוא ארבע פונקציות : `process_write(req)`, ‏`process_read(req)`, ‏`tick()` שמקדמת את מונה
המחזורים, ו-`get_next_completion()` שהסביבה קוראת לה פעם במחזור ומקבלת Completion מוכן
או null. המחלקות של הבקשות ושל ה-Completion נתונות :

=== "SystemVerilog"
    ```systemverilog title="given classes"
    localparam int MRRS = 256;   // max read request size, bytes
    localparam int MPS  = 256;   // max payload of one completion, bytes
    localparam int RCB  = 128;   // read completion boundary of an endpoint, bytes

    typedef byte unsigned block_t[RCB];   // one memory block

    class mem_write_req;
      bit [63:0]    address;
      int unsigned  length_bytes;
      byte unsigned data[];
      function new(bit [63:0] address = 0, int unsigned length_bytes = 0);
        this.address      = address;
        this.length_bytes = length_bytes;
        this.data         = new[length_bytes];
      endfunction
    endclass

    class mem_read_req;
      bit [63:0]   address;
      int unsigned length_bytes;
      bit [15:0]   requester_id;
      bit [9:0]    tag;
    endclass

    class completion;
      bit [15:0]    requester_id;
      bit [9:0]     tag;
      bit [63:0]    start_address;   // model-internal: where the payload starts
      int unsigned  byte_count;      // bytes still to return, this payload included
      byte unsigned data[];
    endclass

    class pending_read;              // one read waiting to be answered
      completion   cpls[$];          // its completions, in address order
      int unsigned ready_cycle;      // the next one may go out from this cycle on
    endclass
    ```

=== "Python"
    ```python title="given classes"
    import random
    from dataclasses import dataclass, field

    MRRS, MPS, RCB = 256, 256, 128   # max read request, max payload, read completion boundary


    @dataclass
    class MemWriteReq:
        address: int
        data: bytes                  # len(data) is the length in bytes


    @dataclass
    class MemReadReq:
        address: int
        length_bytes: int
        requester_id: int
        tag: int


    @dataclass
    class Completion:
        requester_id: int
        tag: int
        start_address: int           # model-internal: where the payload starts
        byte_count: int              # bytes still to return, this payload included
        data: bytes


    @dataclass
    class PendingRead:               # one read waiting to be answered
        cpls: list = field(default_factory=list)   # its completions, in address order
        ready_cycle: int = 0         # the next one may go out from this cycle on
    ```

הפשטות : אין Byte Enables ואין שדה Lower Address, כל Completion מצליח (אין UR או CA),
האורך נתון בבתים (לא ב-DW), הכתובת היא כתובת בית, בקשה לא חוצה גבול של 4 KB, ו-Tag לא
חוזר על עצמו כל עוד הקריאה שלו פתוחה.

??? interviewer "מה המראיין בודק"
    - **ארכיטקטורה של מודל ייחוס :** האם המועמד מפריד בין המצב (זיכרון), בין בניית
      ה-Completions (דטרמיניסטית עד לבחירת הפיצול) ובין התזמון (אקראי), ולא כותב פונקציה
      אחת ענקית.
    - **חוקי הפרוטוקול כאינווריאנטים :** סדר עולה **בתוך** בקשה, חופש **בין** בקשות, חיתוך רק
      על גבול RCB, ‏Byte Count יורד, Requester ID ו-Tag מועתקים.
    - **זיכרון מפוצל לבלוקים :** האם הוא יודע למצוא את הבלוק ואת ההיסט של בית, ובסעיף ב
      לא מוחק בתים של שכנים כשכותב חלק מבלוק.
    - **אקראיות מבוקרת :** איך מוסיפים אקראיות (פיצול, המתנה, בחירה) בלי לשבור את
      הכללים, ואיך בודקים מודל שהפלט שלו אינו דטרמיניסטי.

---

### סעיף א – כתובות מיושרות ל-RCB

בסעיף זה הניחו שכל בקשה, כתיבה או קריאה, מתחילה בכתובת שהיא כפולה של 128 ואורכה 128
או 256 בתים.

נכתבו 256 בתים לכתובת `0x10000`, והבית ה-\( i \) שווה ל-\( i \). אחר כך מגיעה קריאה של
256 בתים מ-`0x10000` עם Requester ID ‏`0x0200` ו-Tag ‏`0x15`. אילו Completions המודל
רשאי להחזיר, ומה ה-Byte Count של כל אחד? ממשו את המודל השלם : כתיבה, קריאה, פיצול, המתנה
אקראית ושידור עם interleaving בין קריאות שונות.

??? tip "רמז 1"
    בבקשה מיושרת של 256 בתים יש בדיוק גבול RCB אחד **בתוך** הבקשה. כמה דרכים יש לחתוך,
    וכמה דרכים יש בבקשה של 128?

??? tip "רמז 2"
    שני דברים שונים נקבעים באקראי : **איך** מפצלים (פעם אחת, כשהבקשה מגיעה) ו-**מתי**
    שולחים (בכל מחזור). שמרו לכל קריאה את ה-Completions שלה בתור משלה, ובכל מחזור בחרו
    קריאה אחת מבין המוכנות.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        שתי תשובות חוקיות : Completion אחד של 256 בתים עם Byte Count 256, או שניים של
        128 בתים מ-`0x10000` ומ-`0x10080`, עם Byte Count 256 ואז 128. החיתוך היחיד המותר
        הוא בגבול `0x10080`. המודל : זיכרון של בלוקים לפי כתובת הבלוק; כל קריאה הופכת
        **מיד** לרשימת Completions בסדר כתובות עם מחזור מוכנות אקראי; בכל מחזור קריאה
        מוכנה אחת, אקראית, שולחת את ה-Completion הראשון שנותר לה.

    <!-- cost: זמן \( O(len) \) | שליפה \( O(p) \) -->

    #### הרעיון { .sol-idea }

    **מה מותר להחזיר.** הבקשה מכסה את `0x10000` עד `0x100FF`. כפולות של 128 בתוך הטווח,
    לא כולל הקצוות : רק `0x10080`. לכן יש שתי אפשרויות : לא לחתוך (256 בתים, פחות מ-MPS
    ולכן חוקי) או לחתוך פעם אחת (128 + 128). ‏Byte Count של Completion הוא כמה בתים
    נותרו **לפניו** : 256 ואז 128. הזיכרון שמאחורי הבקשה הוא שני בלוקים, ‏`memory[0x10000]`
    ו-`memory[0x10080]`, שהכתיבה יצרה :

    <svg class="figure cs-fig" viewBox="0 0 640 206" style="max-width:40rem" role="img" aria-label="קריאה מיושרת של 256 בתים מכתובת 0x10000 : שני הבלוקים בזיכרון, ושתי התשובות החוקיות : Completion אחד של 256 בתים, או שניים של 128"><line class="cs-rcb" x1="40.0" y1="26" x2="40.0" y2="174"/><text class="coord halo" x="40.0" y="18" text-anchor="middle">0xFF80</text><line class="cs-rcb" x1="180.0" y1="26" x2="180.0" y2="174"/><text class="coord halo" x="180.0" y="18" text-anchor="middle">0x10000</text><line class="cs-rcb" x1="320.0" y1="26" x2="320.0" y2="174"/><text class="coord halo" x="320.0" y="18" text-anchor="middle">0x10080</text><line class="cs-rcb" x1="460.0" y1="26" x2="460.0" y2="174"/><text class="coord halo" x="460.0" y="18" text-anchor="middle">0x10100</text><line class="cs-rcb" x1="600.0" y1="26" x2="600.0" y2="174"/><text class="coord halo" x="600.0" y="18" text-anchor="middle">0x10180</text><line class="cs-req" x1="180.0" y1="30" x2="180.0" y2="174"/><line class="cs-req" x1="460.0" y1="30" x2="460.0" y2="174"/><text class="legend halo" x="44" y="46">memory after the write</text><rect class="cs-blk" x="180.0" y="52" width="140.0" height="26" rx="3"><title>block 0x10000: 128 bytes</title></rect><text class="coord" x="250.0" y="69.5" text-anchor="middle">memory[0x10000]</text><rect class="cs-blk" x="320.0" y="52" width="140.0" height="26" rx="3"><title>block 0x10080: 128 bytes</title></rect><text class="coord" x="390.0" y="69.5" text-anchor="middle">memory[0x10080]</text><text class="tick" x="530.0" y="69" text-anchor="middle">no entry</text><text class="legend halo" x="44" y="98">one completion</text><rect class="cs-one" x="180.0" y="104" width="280.0" height="26" rx="3"><title>0x10000–0x100FF, byte count 256</title></rect><text class="cs-size" x="320.0" y="121.5" text-anchor="middle">256 B · BC 256</text><circle class="cs-can" cx="320.0" cy="117" r="4.5"><title>0x10080: the only legal cut</title></circle><text class="legend halo" x="44" y="150">two completions</text><rect class="cs-first" x="180.0" y="156" width="140.0" height="26" rx="3"><title>0x10000–0x1007F, byte count 256</title></rect><text class="cs-size" x="250.0" y="173.5" text-anchor="middle">128 B · BC 256</text><rect class="cs-last" x="320.0" y="156" width="140.0" height="26" rx="3"><title>0x10080–0x100FF, byte count 128</title></rect><text class="cs-size" x="390.0" y="173.5" text-anchor="middle">128 B · BC 128</text><text class="legend halo" x="320.0" y="198" text-anchor="middle">request: 256 B from 0x10000, RID 0x0200, tag 0x15</text></svg>

    <span class="viz-legend"><span><i class="cs-rcb"></i>גבול RCB</span><span><i class="cs-req"></i>תחילת הבקשה וסופה</span><span><i class="cs-blk"></i>בלוק בזיכרון, המפתח הוא כתובת הבלוק</span><span><i class="cs-can"></i>נקודת החיתוך המותרת</span><span><i class="cs-one"></i>‏Completion יחיד</span><span><i class="cs-first"></i>ראשון</span><span><i class="cs-last"></i>אחרון</span></span>

    **שלושה חלקים במודל.** הזיכרון הוא associative array שהמפתח שלו הוא כתובת בלוק. כתיבה
    מיושרת מחליפה בלוקים שלמים, וקריאה מיושרת מדביקה בלוקים שלמים (בלוק שאינו קיים תורם
    אפסים). `process_read` בונה **מיד** את כל ה-Completions של הקריאה, בסדר כתובות, עם
    הנתונים מהזיכרון ועם Byte Count שיורד, ומכניס אותם לאובייקט `pending_read` אחד עם מחזור
    מוכנות אקראי. `get_next_completion` רץ פעם במחזור : אוסף את הקריאות שהמחזור שלהן הגיע,
    בוחרת אחת מהן באקראי, ומוציאה ממנה את ה-Completion **הראשון** שנותר. כך הסדר בתוך קריאה
    נשמר מעצמו, וה-interleaving נוצר מהבחירה האקראית בין קריאות :

    ```mermaid
    flowchart LR
        W["MemWr<br/>address, length, data"] --> PW["process_write"]
        PW --> M[("memory<br/>block_t per block address")]
        R["MemRd<br/>address, length, RID, tag"] --> PR["process_read"]
        M --> PR
        PR -- "completions in address order,<br/>ready_cycle = now + rand(1..20)" --> Q["pending_reads[$]"]
        T["tick()"] --> C["current_cycle"]
        Q --> G["get_next_completion()"]
        C --> G
        G -- "at most one CplD per cycle,<br/>from a random ready read" --> OUT["CplD out"]
    ```

    **דוגמה עם שתי קריאות.** אחרי כתיבה של 512 בתים מ-`0x10000` מגיעות באותו מחזור קריאה A
    (‏`0x10000`, 256 בתים, Tag ‏`0x15`) וקריאה B (‏`0x10100`, 256 בתים, Tag ‏`0x16`). שתיהן
    פוצלו ל-128 + 128; A מוכנה ממחזור 5 ו-B ממחזור 3. עברו מחזור אחרי מחזור :

    <div class="stepper" role="group" aria-label="שתי קריאות ממתינות, מחזור אחרי מחזור" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure cs-fig" viewBox="0 0 640 236" style="max-width:40rem" role="img" aria-label="מחזור 0 : תורי ההמתנה של שתי הקריאות וה-Completions שכבר נשלחו"><text class="coord" x="8" y="22" font-weight="700">cycle 0</text><text class="coord" x="8" y="60">A · tag 0x15</text><text class="tick" x="8" y="80">ready at 5</text><rect class="cs-first" x="200" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="60" text-anchor="middle">128 B @ 0x10000</text><text class="tick" x="260" y="76" text-anchor="middle">BC 256</text><rect class="cs-first" x="332" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="60" text-anchor="middle">128 B @ 0x10080</text><text class="tick" x="392" y="76" text-anchor="middle">BC 128</text><text class="coord" x="8" y="118">B · tag 0x16</text><text class="tick" x="8" y="138">ready at 3</text><rect class="cs-last" x="200" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="118" text-anchor="middle">128 B @ 0x10100</text><text class="tick" x="260" y="134" text-anchor="middle">BC 256</text><rect class="cs-last" x="332" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="118" text-anchor="middle">128 B @ 0x10180</text><text class="tick" x="392" y="134" text-anchor="middle">BC 128</text><text class="coord" x="8" y="192">sent</text><text class="tick" x="70" y="195">nothing yet</text></svg><figcaption>מחזור 0 : שתי הקריאות הגיעו. כל אחת פוצלה ל-128 + 128 וקיבלה מחזור מוכנות אקראי : A מוכנה ממחזור 5, ‏B ממחזור 3.</figcaption></figure><figure class="stepper-frame"><svg class="figure cs-fig" viewBox="0 0 640 236" style="max-width:40rem" role="img" aria-label="מחזור 1 : תורי ההמתנה של שתי הקריאות וה-Completions שכבר נשלחו"><text class="coord" x="8" y="22" font-weight="700">cycle 1</text><text class="coord" x="8" y="60">A · tag 0x15</text><text class="tick" x="8" y="80">ready at 5</text><rect class="cs-first" x="200" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="60" text-anchor="middle">128 B @ 0x10000</text><text class="tick" x="260" y="76" text-anchor="middle">BC 256</text><rect class="cs-first" x="332" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="60" text-anchor="middle">128 B @ 0x10080</text><text class="tick" x="392" y="76" text-anchor="middle">BC 128</text><text class="coord" x="8" y="118">B · tag 0x16</text><text class="tick" x="8" y="138">ready at 3</text><rect class="cs-last" x="200" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="118" text-anchor="middle">128 B @ 0x10100</text><text class="tick" x="260" y="134" text-anchor="middle">BC 256</text><rect class="cs-last" x="332" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="118" text-anchor="middle">128 B @ 0x10180</text><text class="tick" x="392" y="134" text-anchor="middle">BC 128</text><text class="coord" x="8" y="192">sent</text><text class="tick" x="70" y="195">nothing yet</text></svg><figcaption>מחזור 1 : אף קריאה לא מוכנה עדיין, ולכן אין Completion.</figcaption></figure><figure class="stepper-frame"><svg class="figure cs-fig" viewBox="0 0 640 236" style="max-width:40rem" role="img" aria-label="מחזור 3 : תורי ההמתנה של שתי הקריאות וה-Completions שכבר נשלחו"><text class="coord" x="8" y="22" font-weight="700">cycle 3</text><text class="coord" x="8" y="60">A · tag 0x15</text><text class="tick" x="8" y="80">ready at 5</text><rect class="cs-first" x="200" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="60" text-anchor="middle">128 B @ 0x10000</text><text class="tick" x="260" y="76" text-anchor="middle">BC 256</text><rect class="cs-first" x="332" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="60" text-anchor="middle">128 B @ 0x10080</text><text class="tick" x="392" y="76" text-anchor="middle">BC 128</text><text class="coord" x="8" y="118">B · tag 0x16</text><circle class="cs-can" cx="14" cy="134" r="4.5"/><text class="tick" x="24" y="138">ready</text><rect class="cs-last" x="200" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="118" text-anchor="middle">128 B @ 0x10100</text><text class="tick" x="260" y="134" text-anchor="middle">BC 256</text><rect class="cs-last" x="332" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="118" text-anchor="middle">128 B @ 0x10180</text><text class="tick" x="392" y="134" text-anchor="middle">BC 128</text><text class="coord" x="8" y="192">sent</text><rect class="cs-last" x="70" y="170" width="100" height="40" rx="3"/><text class="cs-size" x="120" y="186" text-anchor="middle">cycle 3</text><text class="tick" x="120" y="202" text-anchor="middle">B: 0x10100</text></svg><figcaption>מחזור 3 : נבחרה B ושלחה את ה-Completion הבא שלה : 128 בתים מ-<span dir="ltr">0x10100</span>, Byte Count 256. ‏B ממתינה שוב, עם מחזור מוכנות חדש.</figcaption></figure><figure class="stepper-frame"><svg class="figure cs-fig" viewBox="0 0 640 236" style="max-width:40rem" role="img" aria-label="מחזור 5 : תורי ההמתנה של שתי הקריאות וה-Completions שכבר נשלחו"><text class="coord" x="8" y="22" font-weight="700">cycle 5</text><text class="coord" x="8" y="60">A · tag 0x15</text><circle class="cs-can" cx="14" cy="76" r="4.5"/><text class="tick" x="24" y="80">ready</text><rect class="cs-first" x="200" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="60" text-anchor="middle">128 B @ 0x10000</text><text class="tick" x="260" y="76" text-anchor="middle">BC 256</text><rect class="cs-first" x="332" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="60" text-anchor="middle">128 B @ 0x10080</text><text class="tick" x="392" y="76" text-anchor="middle">BC 128</text><text class="coord" x="8" y="118">B · tag 0x16</text><text class="tick" x="8" y="138">ready at 6</text><rect class="st-done" x="200" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="118" text-anchor="middle">128 B @ 0x10100</text><text class="tick" x="260" y="134" text-anchor="middle">BC 256</text><rect class="cs-last" x="332" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="118" text-anchor="middle">128 B @ 0x10180</text><text class="tick" x="392" y="134" text-anchor="middle">BC 128</text><text class="coord" x="8" y="192">sent</text><rect class="cs-last" x="70" y="170" width="100" height="40" rx="3"/><text class="cs-size" x="120" y="186" text-anchor="middle">cycle 3</text><text class="tick" x="120" y="202" text-anchor="middle">B: 0x10100</text><rect class="cs-first" x="180" y="170" width="100" height="40" rx="3"/><text class="cs-size" x="230" y="186" text-anchor="middle">cycle 5</text><text class="tick" x="230" y="202" text-anchor="middle">A: 0x10000</text></svg><figcaption>מחזור 5 : נבחרה A ושלחה את ה-Completion הבא שלה : 128 בתים מ-<span dir="ltr">0x10000</span>, Byte Count 256. ‏A ממתינה שוב, עם מחזור מוכנות חדש.</figcaption></figure><figure class="stepper-frame"><svg class="figure cs-fig" viewBox="0 0 640 236" style="max-width:40rem" role="img" aria-label="מחזור 6 : תורי ההמתנה של שתי הקריאות וה-Completions שכבר נשלחו"><text class="coord" x="8" y="22" font-weight="700">cycle 6</text><text class="coord" x="8" y="60">A · tag 0x15</text><circle class="cs-can" cx="14" cy="76" r="4.5"/><text class="tick" x="24" y="80">ready</text><rect class="st-done" x="200" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="60" text-anchor="middle">128 B @ 0x10000</text><text class="tick" x="260" y="76" text-anchor="middle">BC 256</text><rect class="cs-first" x="332" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="60" text-anchor="middle">128 B @ 0x10080</text><text class="tick" x="392" y="76" text-anchor="middle">BC 128</text><text class="coord" x="8" y="118">B · tag 0x16</text><circle class="cs-can" cx="14" cy="134" r="4.5"/><text class="tick" x="24" y="138">ready</text><rect class="st-done" x="200" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="118" text-anchor="middle">128 B @ 0x10100</text><text class="tick" x="260" y="134" text-anchor="middle">BC 256</text><rect class="cs-last" x="332" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="118" text-anchor="middle">128 B @ 0x10180</text><text class="tick" x="392" y="134" text-anchor="middle">BC 128</text><text class="coord" x="8" y="192">sent</text><rect class="cs-last" x="70" y="170" width="100" height="40" rx="3"/><text class="cs-size" x="120" y="186" text-anchor="middle">cycle 3</text><text class="tick" x="120" y="202" text-anchor="middle">B: 0x10100</text><rect class="cs-first" x="180" y="170" width="100" height="40" rx="3"/><text class="cs-size" x="230" y="186" text-anchor="middle">cycle 5</text><text class="tick" x="230" y="202" text-anchor="middle">A: 0x10000</text><rect class="cs-last" x="290" y="170" width="100" height="40" rx="3"/><text class="cs-size" x="340" y="186" text-anchor="middle">cycle 6</text><text class="tick" x="340" y="202" text-anchor="middle">B: 0x10180</text></svg><figcaption>מחזור 6 : שתי הקריאות מוכנות, והבחירה ביניהן אקראית. נבחרה B ושלחה את ה-Completion הבא שלה : 128 בתים מ-<span dir="ltr">0x10180</span>, Byte Count 128. זה היה ה-Completion האחרון של B.</figcaption></figure><figure class="stepper-frame"><svg class="figure cs-fig" viewBox="0 0 640 236" style="max-width:40rem" role="img" aria-label="מחזור 7 : תורי ההמתנה של שתי הקריאות וה-Completions שכבר נשלחו"><text class="coord" x="8" y="22" font-weight="700">cycle 7</text><text class="coord" x="8" y="60">A · tag 0x15</text><circle class="cs-can" cx="14" cy="76" r="4.5"/><text class="tick" x="24" y="80">ready</text><rect class="st-done" x="200" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="60" text-anchor="middle">128 B @ 0x10000</text><text class="tick" x="260" y="76" text-anchor="middle">BC 256</text><rect class="cs-first" x="332" y="44" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="60" text-anchor="middle">128 B @ 0x10080</text><text class="tick" x="392" y="76" text-anchor="middle">BC 128</text><text class="coord" x="8" y="118">B · tag 0x16</text><text class="tick" x="8" y="138">done</text><rect class="st-done" x="200" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="260" y="118" text-anchor="middle">128 B @ 0x10100</text><text class="tick" x="260" y="134" text-anchor="middle">BC 256</text><rect class="st-done" x="332" y="102" width="120" height="40" rx="3"/><text class="cs-size" x="392" y="118" text-anchor="middle">128 B @ 0x10180</text><text class="tick" x="392" y="134" text-anchor="middle">BC 128</text><text class="coord" x="8" y="192">sent</text><rect class="cs-last" x="70" y="170" width="100" height="40" rx="3"/><text class="cs-size" x="120" y="186" text-anchor="middle">cycle 3</text><text class="tick" x="120" y="202" text-anchor="middle">B: 0x10100</text><rect class="cs-first" x="180" y="170" width="100" height="40" rx="3"/><text class="cs-size" x="230" y="186" text-anchor="middle">cycle 5</text><text class="tick" x="230" y="202" text-anchor="middle">A: 0x10000</text><rect class="cs-last" x="290" y="170" width="100" height="40" rx="3"/><text class="cs-size" x="340" y="186" text-anchor="middle">cycle 6</text><text class="tick" x="340" y="202" text-anchor="middle">B: 0x10180</text><rect class="cs-first" x="400" y="170" width="100" height="40" rx="3"/><text class="cs-size" x="450" y="186" text-anchor="middle">cycle 7</text><text class="tick" x="450" y="202" text-anchor="middle">A: 0x10080</text></svg><figcaption>מחזור 7 : נבחרה A ושלחה את ה-Completion הבא שלה : 128 בתים מ-<span dir="ltr">0x10080</span>, Byte Count 128. זה היה ה-Completion האחרון של A.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="6"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <span class="viz-legend"><span><i class="cs-first"></i>‏Completions של קריאה A</span><span><i class="cs-last"></i>‏Completions של קריאה B</span><span><i class="st-done"></i>כבר נשלח</span><span><i class="cs-can"></i>קריאה שמחזור המוכנות שלה הגיע</span></span>

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **כתיבה :** לכל 128 בתים של הבקשה, `memory[address + k]` מקבל בלוק חדש. אין
       Completion.
    2. **קריאת הנתונים :** מדביקים את הבלוקים `memory[address]`, ‏`memory[address + 128]`
       וכן הלאה; בלוק חסר תורם 128 אפסים.
    3. **פיצול :** בקשה של 128 בתים היא Completion אחד; בקשה של 256 בתים היא אחד או שניים,
       לפי הטלת מטבע.
    4. **בניית ה-Completions :** לכל גודל ברשימה : Requester ID ו-Tag מהבקשה, כתובת ההתחלה
       הנוכחית, Byte Count שווה למספר הבתים שעוד לא כוסו, והנתונים מההיסט המתאים. מקדמים
       כתובת ומורידים מהיתרה.
    5. **תור ההמתנה :** כל ה-Completions של הקריאה נכנסים ל-`pending_read` אחד, עם
       `ready_cycle` אקראי קדימה, והוא נכנס לרשימת הקריאות הפתוחות.
    6. **שידור, פעם במחזור :** אוספים את הקריאות שה-`ready_cycle` שלהן הגיע. אם אין, מחזירים
       null. אחרת בוחרים אחת באקראי, מוציאים את ה-Completion הראשון שלה, ומגרילים לה
       `ready_cycle` חדש (או מוחקים אותה אם זה היה האחרון).

    </div>

    #### הקוד { .sol-code }

    שלוש הפונקציות שתלויות ביישור (כתיבה, קריאת הנתונים והפיצול) מוגדרות כ-virtual, כי
    בסעיף ב נחליף בדיוק אותן. ב-Python המודל מקבל מופע של `random.Random`, כדי שבדיקה
    תוכל לקבע seed.

    === "SystemVerilog"
        ```systemverilog title="class endpoint_ref_model" linenums="1" hl_lines="19 28 36 63 83 84"
        // Completer model for RCB-aligned traffic: writes and reads of whole 128-byte blocks.
        class endpoint_ref_model;
          localparam int MIN_DELAY = 1, MAX_DELAY = 20;   // cycles before the first completion of a read
          localparam int MAX_GAP = 10;                    // cycles between two completions of one read

          block_t      memory[bit [63:0]];                // key: block address (a multiple of RCB)
          pending_read pending_reads[$];                  // one entry per read not fully answered yet
          int unsigned current_cycle;

          // Posted write: replace whole blocks, no completion.
          virtual function void process_write(mem_write_req req);
            block_t blk;
            if (req.address % RCB != 0 || req.length_bytes % RCB != 0) begin
              $error("aligned model: write of %0d bytes at 0x%0h", req.length_bytes, req.address);
              return;
            end
            for (int k = 0; k < req.length_bytes; k += RCB) begin
              for (int j = 0; j < RCB; j++) blk[j] = req.data[k + j];
              memory[req.address + k] = blk;                                 // (1)!
            end
          endfunction

          // The bytes of a read, block by block; a block never written reads as zeros.
          virtual function void read_bytes(bit [63:0] address, int unsigned length_bytes,
                                           ref byte unsigned data[]);
            data = new[length_bytes];
            for (int k = 0; k < length_bytes; k += RCB) begin
              if (!memory.exists(address + k)) continue;                     // (2)!
              for (int j = 0; j < RCB; j++) data[k + j] = memory[address + k][j];
            end
          endfunction

          // Payload sizes of the completions: 256 bytes may be cut at the one interior boundary.
          virtual function void create_fragments(bit [63:0] address, int unsigned length_bytes,
                                                 ref int unsigned sizes[$]);
            sizes.delete();
            if (length_bytes == 2 * RCB && $urandom_range(0, 1)) begin      // (3)!
              sizes.push_back(RCB);
              sizes.push_back(RCB);
            end else
              sizes.push_back(length_bytes);
          endfunction

          // Build every completion of the read now, in address order, and park them until ready.
          virtual function void process_read(mem_read_req req);
            pending_read pending = new();
            int unsigned sizes[$];
            byte unsigned data[];
            bit [63:0]   address   = req.address;
            int unsigned remaining = req.length_bytes;
            if (req.length_bytes == 0 || req.length_bytes > MRRS) begin
              $error("read of %0d bytes exceeds MRRS", req.length_bytes);
              return;
            end
            read_bytes(req.address, req.length_bytes, data);
            create_fragments(req.address, req.length_bytes, sizes);
            foreach (sizes[i]) begin
              completion cpl = new();
              cpl.requester_id  = req.requester_id;
              cpl.tag           = req.tag;
              cpl.start_address = address;
              cpl.byte_count    = remaining;                                 // (4)!
              cpl.data          = new[sizes[i]];
              foreach (cpl.data[j]) cpl.data[j] = data[address - req.address + j];
              pending.cpls.push_back(cpl);
              address   += sizes[i];
              remaining -= sizes[i];
            end
            pending.ready_cycle = current_cycle + $urandom_range(MIN_DELAY, MAX_DELAY);
            pending_reads.push_back(pending);
          endfunction

          // Called once per cycle: a random ready read sends its next completion, or null.
          virtual function completion get_next_completion();
            int ready[$];
            int pick;
            completion cpl;
            foreach (pending_reads[i])
              if (pending_reads[i].ready_cycle <= current_cycle) ready.push_back(i);
            if (ready.size() == 0) return null;
            pick = ready[$urandom_range(0, ready.size() - 1)];               // (5)!
            cpl  = pending_reads[pick].cpls.pop_front();                     // (6)!
            if (pending_reads[pick].cpls.size() == 0)
              pending_reads.delete(pick);
            else
              pending_reads[pick].ready_cycle = current_cycle + $urandom_range(1, MAX_GAP);
            return cpl;
          endfunction

          virtual function void tick();
            current_cycle++;
          endfunction
        endclass
        ```

        1. המפתח הוא כתובת הבלוק. בכתיבה מיושרת זו בדיוק כתובת הבקשה ועוד כפולות של 128,
           והבלוק הישן מוחלף כולו.
        2. ‏`new[length_bytes]` מאפס את המערך, ולכן בלוק שלא נכתב מעולם משאיר אפסים בלי
           טיפול מיוחד.
        3. ההטלה היחידה שקובעת את צורת הפיצול. בקשה של 128 בתים לעולם לא מתפצלת.
        4. ‏Byte Count הוא היתרה **לפני** ה-Completion : 256 ואז 128, לא גודל ה-payload.
        5. הבחירה בין קריאות מוכנות היא החופש היחיד בסדר השידור; מכאן ה-interleaving.
        6. ‏`pop_front` תמיד : בתוך קריאה אחת הסדר הוא סדר הכתובות, בלי יוצא מן הכלל.

    === "Python"
        ```python title="class EndpointRefModel" linenums="1" hl_lines="17 21 26 40 51 52"
        class EndpointRefModel:
            """Completer model for RCB-aligned traffic: writes and reads of whole 128-byte blocks."""
            MIN_DELAY, MAX_DELAY = 1, 20     # cycles before the first completion of a read
            MAX_GAP = 10                     # cycles between two completions of one read

            def __init__(self, rng: random.Random | None = None):
                self.memory: dict[int, bytearray] = {}        # key: block address (a multiple of RCB)
                self.pending_reads: list[PendingRead] = []    # one entry per read not fully answered yet
                self.current_cycle = 0
                self.rng = rng or random.Random()

            def process_write(self, req: MemWriteReq) -> None:
                """Posted write: replace whole blocks, no completion."""
                if req.address % RCB or len(req.data) % RCB:
                    raise ValueError(f"aligned model: write of {len(req.data)} bytes at {req.address:#x}")
                for k in range(0, len(req.data), RCB):
                    self.memory[req.address + k] = bytearray(req.data[k:k + RCB])   # (1)!

            def read_bytes(self, address: int, length_bytes: int) -> bytes:
                """The bytes of a read, block by block; a block never written reads as zeros."""
                return b"".join(bytes(self.memory.get(address + k, bytes(RCB)))     # (2)!
                                for k in range(0, length_bytes, RCB))

            def create_fragments(self, address: int, length_bytes: int) -> list[int]:
                """Payload sizes of the completions: 256 bytes may be cut at the one interior boundary."""
                if length_bytes == 2 * RCB and self.rng.randint(0, 1):              # (3)!
                    return [RCB, RCB]
                return [length_bytes]

            def process_read(self, req: MemReadReq) -> None:
                """Build every completion of the read now, in address order, and park them until ready."""
                if not 0 < req.length_bytes <= MRRS:
                    raise ValueError(f"read of {req.length_bytes} bytes exceeds MRRS")
                data = self.read_bytes(req.address, req.length_bytes)
                pending = PendingRead()
                address, remaining = req.address, req.length_bytes
                for size in self.create_fragments(req.address, req.length_bytes):
                    offset = address - req.address
                    pending.cpls.append(Completion(req.requester_id, req.tag, address,
                                                   remaining, data[offset:offset + size]))   # (4)!
                    address += size
                    remaining -= size
                pending.ready_cycle = self.current_cycle + self.rng.randint(self.MIN_DELAY, self.MAX_DELAY)
                self.pending_reads.append(pending)

            def get_next_completion(self) -> Completion | None:
                """Called once per cycle: a random ready read sends its next completion, or None."""
                ready = [p for p in self.pending_reads if p.ready_cycle <= self.current_cycle]
                if not ready:
                    return None
                pick = self.rng.choice(ready)                                       # (5)!
                cpl = pick.cpls.pop(0)                                              # (6)!
                if pick.cpls:
                    pick.ready_cycle = self.current_cycle + self.rng.randint(1, self.MAX_GAP)
                else:
                    self.pending_reads.remove(pick)
                return cpl

            def tick(self) -> None:
                self.current_cycle += 1
        ```

        1. המפתח הוא כתובת הבלוק. בכתיבה מיושרת זו בדיוק כתובת הבקשה ועוד כפולות של 128,
           והבלוק הישן מוחלף כולו.
        2. בלוק שלא נכתב מעולם תורם `bytes(RCB)`, כלומר 128 אפסים.
        3. ההטלה היחידה שקובעת את צורת הפיצול. בקשה של 128 בתים לעולם לא מתפצלת.
        4. ‏Byte Count הוא היתרה **לפני** ה-Completion : 256 ואז 128, לא גודל ה-payload.
        5. הבחירה בין קריאות מוכנות היא החופש היחיד בסדר השידור; מכאן ה-interleaving.
        6. תמיד הראשון : בתוך קריאה אחת הסדר הוא סדר הכתובות, בלי יוצא מן הכלל.

    #### למה זה נכון { .sol-proof }

    כל כלל מהשאלה נשמר על ידי חלק אחד ברור של הקוד, וזה בדיוק מה ש-scoreboard יבדוק על
    ה-DUT :

    - **כל הבתים, בסדר, בלי חיתוך אסור :** `process_read` עובר על הגדלים ברצף מכתובת הבקשה;
      סכום הגדלים הוא אורך הבקשה, וכתובת ההתחלה של כל Completion היא סוף הקודם. חיתוך קיים
      רק ב-`address + 128` של בקשת 256, שהיא כפולה של 128 כי הכתובת מיושרת.
    - **‏Byte Count :** `remaining` מתחיל באורך הבקשה ויורד בגודל כל Completion, ולכן הוא
      תמיד "כמה נשאר כולל אותי".
    - **סדר בתוך קריאה :** ה-Completions נכנסים לתור בסדר כתובות, ויוצאים רק ב-`pop_front`.
      אין מסלול אחר החוצה.
    - **חופש בין קריאות :** הבחירה ב-`get_next_completion` היא בין **קריאות**, לא בין
      Completions, ולכן ה-interleaving לעולם לא הופך את הסדר הפנימי.
    - **תזמון :** Completion יוצא רק כש-`ready_cycle` הגיע, ופעם אחת לכל קריאה ל-
      `get_next_completion`, כלומר לכל היותר אחד במחזור.

    הריצה מהאיור, כטבלה. ‏Byte Count יורד בתוך כל קריאה, וה-Completions של A ושל B
    משולבים :

    | מחזור | קריאה | כתובת | גודל | ‏Byte Count |
    |---|---|---|---|---|
    | 3 | ‏B (Tag 0x16) | ‏`0x10100` | 128 | 256 |
    | 5 | ‏A (Tag 0x15) | ‏`0x10000` | 128 | 256 |
    | 6 | ‏B (Tag 0x16) | ‏`0x10180` | 128 | 128 |
    | 7 | ‏A (Tag 0x15) | ‏`0x10080` | 128 | 128 |

    #### סיבוכיות { .sol-cost }

    כתיבה וקריאה הן \( O(len) \) בהעתקת בתים, עם \( len / RCB \) גישות ל-associative array.
    ‏`get_next_completion` היא \( O(p) \) במספר הקריאות הפתוחות \( p \). הזיכרון במודל
    הוא רק הבלוקים שנכתבו ועוד ה-Completions שטרם נשלחו, ולכן כתובות של 64 ביט אינן בעיה.

---

### סעיף ב – כתובות שאינן מיושרות

עכשיו הכתובת היא כל כתובת בית, והאורך הוא כל מספר בין 1 ל-MRRS, גם בכתיבות וגם
בקריאות.

נכתבו 256 בתים לכתובת `0x10020`, ואחר כך מגיעה קריאה של 256 בתים מ-`0x10020` עם
‏Requester ID ‏`0x0300` ו-Tag ‏`0x22`. אילו פיצולים חוקיים, ומה ה-Byte Count של כל
‏Completion? למה הפיצול 128 + 128 אסור? אילו פונקציות במודל של סעיף א צריכות להשתנות,
ואיך?

??? tip "רמז 1"
    באיזה בלוק יושב הבית שבכתובת \( a \), ובאיזה היסט בתוכו? בקשה לא מיושרת נוגעת בבלוק
    הראשון ובבלוק האחרון **רק בחלקם**. מה קורה לבתים האחרים של הבלוק אם מחליפים אותו
    כולו?

??? tip "רמז 2"
    הגבולות שבהם מותר לחתוך הם כפולות של 128 שגדולות מהכתובת וקטנות מסוף הבקשה. כל
    תת-קבוצה שלהם היא פיצול חוקי, ואין פיצולים אחרים (ההוכחה בשאלה 0020). איך הופכים
    תת-קבוצה של גבולות לרשימת גדלים?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        שני גבולות בתוך הבקשה, ‏`0x10080` ו-`0x10100`, ולכן ארבעה פיצולים : ‏256,
        ‏96 + 160, ‏224 + 32 ו-96 + 128 + 32. ‏Byte Count : בכל פיצול הראשון הוא 256,
        ואחריו היתרה (למשל 256, 160, 32). ‏128 + 128 חותך ב-`0x100A0`, שאינו כפולה של
        128. במודל משתנות שלוש פונקציות : הכתיבה (עדכון חלקי של בלוק, קריאה-שינוי-כתיבה),
        קריאת הנתונים (הליכה בלוק אחרי בלוק) והפיצול (תת-קבוצה אקראית של הגבולות
        הפנימיים). ההמתנה והשידור לא משתנים.

    <!-- cost: זמן \( O(len) \) | שליפה \( O(p) \) -->

    #### הרעיון { .sol-idea }

    **בלוק והיסט.** הבית שבכתובת \( a \) יושב בבלוק \( \lfloor a / 128 \rfloor \cdot 128 \)
    בהיסט \( a \bmod 128 \) : בחזקות של 2 זה `a & ~127` ו-`a & 127`. בקשה של 256 בתים
    מ-`0x10020` נוגעת בשלושה בלוקים : 96 בתים אחרונים של `0x10000`, כל `0x10080`, ו-32
    הבתים הראשונים של `0x10100`. כתיבה שמחליפה את הבלוק `0x10000` כולו הייתה מוחקת את 32
    הבתים שלפני הבקשה, ולכן כותבים **קריאה-שינוי-כתיבה** : לוקחים את הבלוק הקיים (או בלוק
    אפסים), מעדכנים רק את הבתים שנגעו, ומחזירים. אותה הליכה, בלוק אחרי בלוק, אוספת את
    הבתים של קריאה :

    <svg class="figure cs-fig" viewBox="0 0 640 176" style="max-width:40rem" role="img" aria-label="בקשה של 256 בתים מכתובת 0x10020 נוגעת בשלושה בלוקים : 96 בתים אחרונים של 0x10000, כל 0x10080, ו-32 הבתים הראשונים של 0x10100; שני גבולות RCB בתוך הבקשה"><line class="cs-rcb" x1="40.0" y1="26" x2="40.0" y2="124"/><text class="coord halo" x="40.0" y="18" text-anchor="middle">0xFF80</text><line class="cs-rcb" x1="180.0" y1="26" x2="180.0" y2="124"/><text class="coord halo" x="180.0" y="18" text-anchor="middle">0x10000</text><line class="cs-rcb" x1="320.0" y1="26" x2="320.0" y2="124"/><text class="coord halo" x="320.0" y="18" text-anchor="middle">0x10080</text><line class="cs-rcb" x1="460.0" y1="26" x2="460.0" y2="124"/><text class="coord halo" x="460.0" y="18" text-anchor="middle">0x10100</text><line class="cs-rcb" x1="600.0" y1="26" x2="600.0" y2="124"/><text class="coord halo" x="600.0" y="18" text-anchor="middle">0x10180</text><rect class="cs-blk" x="180.0" y="40" width="140.0" height="30" rx="3"></rect><text class="coord halo" x="250.0" y="88" text-anchor="middle">memory[0x10000]</text><rect class="cs-blk" x="320.0" y="40" width="140.0" height="30" rx="3"></rect><text class="coord halo" x="390.0" y="88" text-anchor="middle">memory[0x10080]</text><rect class="cs-blk" x="460.0" y="40" width="140.0" height="30" rx="3"></rect><text class="coord halo" x="530.0" y="88" text-anchor="middle">memory[0x10100]</text><rect class="cs-keep" x="180.0" y="41" width="35.0" height="28" rx="3"><title>0x10000–0x1001F: 32 bytes kept as they were</title></rect><text class="cs-size" x="197.5" y="59.5" text-anchor="middle">32</text><rect class="cs-keep" x="495.0" y="41" width="105.0" height="28" rx="3"><title>0x10120–0x1017F: 96 bytes kept as they were</title></rect><text class="cs-size" x="547.5" y="59.5" text-anchor="middle">96</text><rect class="cs-new" x="215.0" y="41" width="105.0" height="28" rx="3"><title>block 0x10000, offset 32, 96 bytes</title></rect><text class="cs-size" x="267.5" y="59.5" text-anchor="middle">96</text><rect class="cs-new" x="320.0" y="41" width="140.0" height="28" rx="3"><title>block 0x10080, offset 0, 128 bytes</title></rect><text class="cs-size" x="390.0" y="59.5" text-anchor="middle">128</text><rect class="cs-new" x="460.0" y="41" width="35.0" height="28" rx="3"><title>block 0x10100, offset 0, 32 bytes</title></rect><text class="cs-size" x="477.5" y="59.5" text-anchor="middle">32</text><line class="cs-req" x1="215.0" y1="30" x2="215.0" y2="124"/><line class="cs-req" x1="495.0" y1="30" x2="495.0" y2="124"/><line class="ink-line" x1="215.0" y1="106" x2="495.0" y2="106" stroke-width="1.6"/><circle class="cs-can" cx="320.0" cy="106" r="4.5"><title>0x10080: a legal cut</title></circle><circle class="cs-can" cx="460.0" cy="106" r="4.5"><title>0x10100: a legal cut</title></circle><text class="legend halo" x="355.0" y="140" text-anchor="middle">request: 256 B from 0x10020 (0x10020 … 0x1011F)</text><text class="legend halo" x="355.0" y="164" text-anchor="middle">cuts allowed at 0x10080 and 0x10100</text></svg>

    <span class="viz-legend"><span><i class="cs-blk"></i>בלוק בזיכרון</span><span><i class="cs-new"></i>בתים שהבקשה נוגעת בהם</span><span><i class="cs-keep"></i>בתים קיימים שנשמרים</span><span><i class="cs-can"></i>גבול RCB בתוך הבקשה</span><span><i class="cs-req"></i>תחילת הבקשה וסופה</span></span>

    הלולאה אחת לשני הצדדים : `done` סופר כמה בתים כבר טופלו; בכל סיבוב מחשבים את הבלוק
    ואת ההיסט של הבית הבא, ואת מספר הבתים עד סוף הבלוק או עד סוף הבקשה, הקטן מביניהם :

    | סיבוב | בלוק (המפתח) | היסט | בתים (n) | מכסה |
    |---|---|---|---|---|
    | 1 | ‏`0x10000` | 32 | 96 | <span dir="ltr">0x10020 … 0x1007F</span> |
    | 2 | ‏`0x10080` | 0 | 128 | <span dir="ltr">0x10080 … 0x100FF</span> |
    | 3 | ‏`0x10100` | 0 | 32 | <span dir="ltr">0x10100 … 0x1011F</span> |

    **הגבולות הפנימיים והפיצולים.** הפיצול לא תלוי בזיכרון, רק בכתובות : הגבולות
    האפשריים הם כפולות של 128 בין הכתובת לסוף הבקשה, לא כולל. כל תת-קבוצה של הגבולות
    האלה היא פיצול חוקי, ולכן במקום לרשום אפשרויות מטילים מטבע לכל גבול : אם הוא נבחר,
    הקטע מהחיתוך הקודם עד אליו הוא Completion. מה שנשאר אחרי הגבול האחרון הוא ה-Completion
    האחרון. ‏Byte Count יורד בגדלים שנבחרו. החלוקה 128 + 128 אינה תת-קבוצה של הגבולות,
    כי נקודת החיתוך שלה, ‏`0x100A0`, אינה גבול :

    <svg class="figure cs-fig" viewBox="0 0 640 274" style="max-width:40rem" role="img" aria-label="ארבעת הפיצולים החוקיים של קריאה של 256 בתים מכתובת 0x10020, עם Byte Count של כל Completion, והפיצול הפסול 128 + 128 שחותך ב-0x100A0"><line class="cs-rcb" x1="40.0" y1="26" x2="40.0" y2="252"/><text class="coord halo" x="40.0" y="18" text-anchor="middle">0xFF80</text><line class="cs-rcb" x1="180.0" y1="26" x2="180.0" y2="252"/><text class="coord halo" x="180.0" y="18" text-anchor="middle">0x10000</text><line class="cs-rcb" x1="320.0" y1="26" x2="320.0" y2="252"/><text class="coord halo" x="320.0" y="18" text-anchor="middle">0x10080</text><line class="cs-rcb" x1="460.0" y1="26" x2="460.0" y2="252"/><text class="coord halo" x="460.0" y="18" text-anchor="middle">0x10100</text><line class="cs-rcb" x1="600.0" y1="26" x2="600.0" y2="252"/><text class="coord halo" x="600.0" y="18" text-anchor="middle">0x10180</text><line class="cs-req" x1="215.0" y1="30" x2="215.0" y2="252"/><line class="cs-req" x1="495.0" y1="30" x2="495.0" y2="252"/><text class="legend halo" x="44" y="60">256</text><rect class="cs-one" x="215.0" y="44" width="280.0" height="26" rx="3"><title>0x10020–0x1011F: 256 bytes, byte count 256</title></rect><text class="cs-size" x="355.0" y="61.5" text-anchor="middle">256</text><text class="tick" x="355.0" y="40" text-anchor="middle">BC 256</text><text class="legend halo" x="44" y="104">96 + 160</text><rect class="cs-first" x="215.0" y="88" width="105.0" height="26" rx="3"><title>0x10020–0x1007F: 96 bytes, byte count 256</title></rect><text class="cs-size" x="267.5" y="105.5" text-anchor="middle">96</text><text class="tick" x="267.5" y="84" text-anchor="middle">BC 256</text><rect class="cs-last" x="320.0" y="88" width="175.0" height="26" rx="3"><title>0x10080–0x1011F: 160 bytes, byte count 160</title></rect><text class="cs-size" x="407.5" y="105.5" text-anchor="middle">160</text><text class="tick" x="407.5" y="84" text-anchor="middle">BC 160</text><text class="legend halo" x="44" y="148">224 + 32</text><rect class="cs-first" x="215.0" y="132" width="245.0" height="26" rx="3"><title>0x10020–0x100FF: 224 bytes, byte count 256</title></rect><text class="cs-size" x="337.5" y="149.5" text-anchor="middle">224</text><text class="tick" x="337.5" y="128" text-anchor="middle">BC 256</text><rect class="cs-last" x="460.0" y="132" width="35.0" height="26" rx="3"><title>0x10100–0x1011F: 32 bytes, byte count 32</title></rect><text class="cs-size" x="477.5" y="149.5" text-anchor="middle">32</text><text class="tick" x="477.5" y="128" text-anchor="middle">BC 32</text><text class="legend halo" x="44" y="192">96 + 128 + 32</text><rect class="cs-first" x="215.0" y="176" width="105.0" height="26" rx="3"><title>0x10020–0x1007F: 96 bytes, byte count 256</title></rect><text class="cs-size" x="267.5" y="193.5" text-anchor="middle">96</text><text class="tick" x="267.5" y="172" text-anchor="middle">BC 256</text><rect class="cs-mid" x="320.0" y="176" width="140.0" height="26" rx="3"><title>0x10080–0x100FF: 128 bytes, byte count 160</title></rect><text class="cs-size" x="390.0" y="193.5" text-anchor="middle">128</text><text class="tick" x="390.0" y="172" text-anchor="middle">BC 160</text><rect class="cs-last" x="460.0" y="176" width="35.0" height="26" rx="3"><title>0x10100–0x1011F: 32 bytes, byte count 32</title></rect><text class="cs-size" x="477.5" y="193.5" text-anchor="middle">32</text><text class="tick" x="477.5" y="172" text-anchor="middle">BC 32</text><text class="legend halo" x="44" y="236">128 + 128 ✕</text><rect class="cs-bad" x="215.0" y="220" width="140.0" height="26" rx="3"><title>0x10020–0x1009F</title></rect><text class="cs-size" x="285.0" y="237.5" text-anchor="middle">128</text><rect class="cs-bad" x="355.0" y="220" width="140.0" height="26" rx="3"><title>0x100A0–0x1011F</title></rect><text class="cs-size" x="425.0" y="237.5" text-anchor="middle">128</text><text class="cs-no halo" x="355.0" y="216" text-anchor="middle">cut at 0x100A0: not a boundary</text></svg>

    <span class="viz-legend"><span><i class="cs-one"></i>‏Completion יחיד</span><span><i class="cs-first"></i>ראשון : מכתובת הבקשה עד גבול</span><span><i class="cs-mid"></i>אמצעי : מגבול לגבול</span><span><i class="cs-last"></i>אחרון : עד סוף הבקשה</span><span><i class="cs-bad"></i>חיתוך שלא על גבול RCB</span></span>

    | פיצול | כתובות ההתחלה | גדלים | ‏Byte Count |
    |---|---|---|---|
    | ‏256 | <span dir="ltr">0x10020</span> | <span dir="ltr">256</span> | <span dir="ltr">256</span> |
    | ‏96 + 160 | <span dir="ltr">0x10020, 0x10080</span> | <span dir="ltr">96, 160</span> | <span dir="ltr">256, 160</span> |
    | ‏224 + 32 | <span dir="ltr">0x10020, 0x10100</span> | <span dir="ltr">224, 32</span> | <span dir="ltr">256, 32</span> |
    | ‏96 + 128 + 32 | <span dir="ltr">0x10020, 0x10080, 0x10100</span> | <span dir="ltr">96, 128, 32</span> | <span dir="ltr">256, 160, 32</span> |

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **כתיבה בבלוקים :** כל עוד נותרו בתים : בלוק והיסט של הבית הבא, ‏\( n \) בתים עד סוף
       הבלוק או עד סוף הבקשה. מביאים את הבלוק (קיים, או אפסים), מעדכנים \( n \) בתים
       מההיסט, מחזירים אותו לזיכרון, ומקדמים ב-\( n \).
    2. **קריאה בבלוקים :** אותה הליכה; מכל בלוק מעתיקים \( n \) בתים מההיסט אל הפלט. בלוק
       חסר תורם אפסים.
    3. **גבולות פנימיים :** הגבול הראשון אחרי הכתובת הוא
       \( (\lfloor address / RCB \rfloor + 1) \cdot RCB \), והבאים בקפיצות של RCB, כל עוד הם
       קטנים מסוף הבקשה.
    4. **תת-קבוצה אקראית :** לכל גבול מטילים מטבע. גבול שנבחר סוגר Completion מהחיתוך הקודם
       (בהתחלה : כתובת הבקשה) עד אליו. בסוף הלולאה מוסיפים את הקטע מהחיתוך האחרון עד סוף
       הבקשה.
    5. **כל השאר כמו בסעיף א :** `process_read` ממיר את הגדלים ל-Completions עם Byte Count
       יורד, ו-`get_next_completion` משדר עם interleaving. הן לא יודעות שהכתובת לא מיושרת.

    </div>

    #### הקוד { .sol-code }

    מחלקה יורשת שמחליפה את שלוש הפונקציות; בניית ה-Completions והשידור עוברים בירושה.
    מי שכתב בסעיף א את הפיצול הכללי כבר בהתחלה, נשאר רק עם הזיכרון.

    === "SystemVerilog"
        ```systemverilog title="class unaligned_endpoint_model" linenums="1" hl_lines="11 14 15 43 46 52"
        // Any byte address and any length up to MRRS: a request touches one block or more, and
        // the first and last of them only partly. Everything else is inherited.
        class unaligned_endpoint_model extends endpoint_ref_model;

          // Posted write, block by block: read the block, patch the touched bytes, write it back.
          virtual function void process_write(mem_write_req req);
            block_t    blk;
            bit [63:0] key;
            int        off, n, done = 0;
            while (done < req.length_bytes) begin
              key = (req.address + done) & ~64'(RCB - 1);                    // (1)!
              off = (req.address + done) & (RCB - 1);
              n   = (RCB - off < req.length_bytes - done) ? RCB - off : req.length_bytes - done;
              if (memory.exists(key)) blk = memory[key];                      // (2)!
              else foreach (blk[j]) blk[j] = 8'h00;
              for (int j = 0; j < n; j++) blk[off + j] = req.data[done + j];
              memory[key] = blk;
              done += n;
            end
          endfunction

          // The same walk gathers the bytes of a read.
          virtual function void read_bytes(bit [63:0] address, int unsigned length_bytes,
                                           ref byte unsigned data[]);
            bit [63:0] key;
            int        off, n, done = 0;
            data = new[length_bytes];
            while (done < length_bytes) begin
              key = (address + done) & ~64'(RCB - 1);
              off = (address + done) & (RCB - 1);
              n   = (RCB - off < length_bytes - done) ? RCB - off : length_bytes - done;
              if (memory.exists(key))
                for (int j = 0; j < n; j++) data[done + j] = memory[key][off + j];
              done += n;
            end
          endfunction

          // Every RCB boundary strictly inside the read is a possible cut; pick a random subset.
          virtual function void create_fragments(bit [63:0] address, int unsigned length_bytes,
                                                 ref int unsigned sizes[$]);
            bit [63:0] end_address = address + length_bytes;
            bit [63:0] boundary    = (address / RCB + 1) * RCB;                // (3)!
            bit [63:0] last        = address;
            sizes.delete();
            while (boundary < end_address) begin
              if ($urandom_range(0, 1)) begin                                  // (4)!
                sizes.push_back(int'(boundary - last));
                last = boundary;
              end
              boundary += RCB;
            end
            sizes.push_back(int'(end_address - last));                         // (5)!
          endfunction
        endclass
        ```

        1. כתובת הבלוק של הבית הבא : מאפסים את 7 הביטים התחתונים. ההיסט הוא אותם 7 ביטים.
        2. קריאה-שינוי-כתיבה : הבלוק הקיים נשמר, ורק \( n \) בתים מההיסט מתעדכנים. בלי זה
           כתיבה של בית אחד הייתה מאפסת 127 שכנים.
        3. הגבול הראשון **אחרי** הכתובת, גם כשהכתובת עצמה מיושרת (אז זה `address + 128`).
        4. מטבע לכל גבול פנימי : תת-קבוצה אקראית. בלי גבולות פנימיים הלולאה לא רצה, ויש
           Completion אחד.
        5. הקטע האחרון, מהחיתוך האחרון עד סוף הבקשה, נכנס תמיד; לכן סכום הגדלים הוא
           האורך.

    === "Python"
        ```python title="class UnalignedEndpointModel" linenums="1" hl_lines="9 11 25 29 33"
        class UnalignedEndpointModel(EndpointRefModel):
            """Any byte address and any length up to MRRS: a request touches one block or more,
            and the first and last of them only partly. Everything else is inherited."""

            def process_write(self, req: MemWriteReq) -> None:
                """Posted write, block by block: patch only the touched bytes of each block."""
                done = 0
                while done < len(req.data):
                    block, off = divmod(req.address + done, RCB)                    # (1)!
                    n = min(RCB - off, len(req.data) - done)
                    blk = self.memory.setdefault(block * RCB, bytearray(RCB))       # (2)!
                    blk[off:off + n] = req.data[done:done + n]
                    done += n

            def read_bytes(self, address: int, length_bytes: int) -> bytes:
                """The same walk gathers the bytes of a read."""
                out, done = bytearray(), 0
                while done < length_bytes:
                    block, off = divmod(address + done, RCB)
                    n = min(RCB - off, length_bytes - done)
                    out += self.memory.get(block * RCB, bytes(RCB))[off:off + n]
                    done += n
                return bytes(out)

            def create_fragments(self, address: int, length_bytes: int) -> list[int]:
                """Every RCB boundary strictly inside the read is a possible cut; pick a random subset."""
                end_address = address + length_bytes
                sizes, last = [], address
                boundary = (address // RCB + 1) * RCB                               # (3)!
                while boundary < end_address:
                    if self.rng.randint(0, 1):                                      # (4)!
                        sizes.append(boundary - last)
                        last = boundary
                    boundary += RCB
                sizes.append(end_address - last)                                    # (5)!
                return sizes
        ```

        1. מספר הבלוק וההיסט של הבית הבא, בפעולה אחת. המפתח במילון הוא כתובת הבלוק,
           `block * RCB`, כמו ב-SystemVerilog.
        2. ‏`setdefault` מחזיר את הבלוק הקיים או יוצר בלוק אפסים, ואז מתעדכנים רק \( n \)
           בתים מההיסט. בלי זה כתיבה של בית אחד הייתה מאפסת 127 שכנים.
        3. הגבול הראשון **אחרי** הכתובת, גם כשהכתובת עצמה מיושרת (אז זה `address + 128`).
        4. מטבע לכל גבול פנימי : תת-קבוצה אקראית. בלי גבולות פנימיים הלולאה לא רצה, ויש
           Completion אחד.
        5. הקטע האחרון, מהחיתוך האחרון עד סוף הבקשה, נכנס תמיד; לכן סכום הגדלים הוא
           האורך.

    #### למה זה נכון { .sol-proof }

    **הזיכרון.** בכל סיבוב של ההליכה \( n \ge 1 \), ו-\( off + n \le RCB \), ולכן הסיבוב
    נשאר בתוך בלוק אחד ומתקדם; הסיבובים מכסים בדיוק את \( [address, address + length) \)
    ברצף. בכתיבה, בתים של הבלוק מחוץ לטווח הזה לא נגעו, ולכן כל בית בזיכרון שווה לערך
    האחרון שנכתב אליו, בכל כתובת ובכל אורך : זו ההגדרה של זיכרון. קריאה מחזירה בדיוק את
    הבתים האלה, ואפס לבית שלא נכתב.

    **הפיצול.** בשאלה [0020](0020-pcie-completion-splits.md) הראינו ששלושת חוקי ה-SPEC
    שקולים לתנאי אחד : כל נקודת חיתוך היא כפולה של RCB בתוך הבקשה. הלולאה מייצרת חיתוך
    רק בגבול כזה (גבול נבחר), ולכן כל פלט חוקי; וכל תת-קבוצה של גבולות מתקבלת בהסתברות
    חיובית, ולכן אין פיצול חוקי שהמודל לעולם לא ייצר. עם \( c \) גבולות פנימיים יש
    \( 2^c \) פיצולים : 4 בדוגמה. ‏MPS אינו דורש בדיקה כאן כי \( MPS = MRRS \), ולכן גם
    הפיצול הריק (בקשה שלמה) עומד בו. ‏Byte Count והסדר באים מ-`process_read` של סעיף א,
    שלא השתנה.

    **הריצה עם שתי קריאות.** אחרי כתיבה של 512 בתים מ-`0x10000` (הבית ה-\( i \) שווה
    ל-\( i \bmod 256 \)) מגיעות קריאה A (‏`0x10000`, 256, Tag ‏`0x15`), שפוצלה ל-128 + 128,
    וקריאה B (‏`0x10020`, 256, Tag ‏`0x22`), שפוצלה ל-96 + 128 + 32. פלט אפשרי אחד :

    | מחזור | ‏Requester ID | ‏Tag | כתובת | גודל | ‏Byte Count | הבית הראשון והאחרון |
    |---|---|---|---|---|---|---|
    | 2 | ‏`0x0300` | ‏`0x22` | ‏`0x10020` | 96 | 256 | <span dir="ltr">0x20 … 0x7F</span> |
    | 4 | ‏`0x0200` | ‏`0x15` | ‏`0x10000` | 128 | 256 | <span dir="ltr">0x00 … 0x7F</span> |
    | 5 | ‏`0x0300` | ‏`0x22` | ‏`0x10080` | 128 | 160 | <span dir="ltr">0x80 … 0xFF</span> |
    | 6 | ‏`0x0200` | ‏`0x15` | ‏`0x10080` | 128 | 128 | <span dir="ltr">0x80 … 0xFF</span> |
    | 7 | ‏`0x0300` | ‏`0x22` | ‏`0x10100` | 32 | 32 | <span dir="ltr">0x00 … 0x1F</span> |

    ה-Completions של B מתחילים ב-`0x10020`, ב-`0x10080` וב-`0x10100` : הראשון בכתובת
    הבקשה, השאר על גבולות RCB. הבית הראשון של כל אחד הוא בדיוק הבית שנכתב לכתובת הזו.

    **לנסות בעצמכם.** בתיבה הבאה בונים בקשות : כתיבה צובעת את הבתים שלה במפת הבלוקים,
    וקריאה נחתכת בגבולות RCB אקראיים ומחכה זמן אקראי. "מחזור" מריץ את הלולאה של המודל
    (`tick` ואז `get_next_completion`), וה-Completions של קריאות שונות משתלבים. שתי הדוגמאות
    שבעמוד טעונות עם ההגרלות המדויקות שלהן. מתחת לקריאות הפתוחות יש ציר מחזורים : לכל קריאה
    ההמתנה האקראית מקווקוות, הזמן שבו היא מוכנה ומחכה לתורה מלא, ועיגול בכל Completion
    שיצא; קו אנכי מסמן את המחזור הנוכחי. מתחתיו ציר המחזורים : לכל מחזור ה-Completion שיצא
    בו (Tag, גודל ו-Byte Count), ולכל קריאה שורה שגבוהה כשהיא מוכנה ומחכה לתורה.

    <div class="explorer" data-kind="endpoint"></div>

    #### סיבוכיות { .sol-cost }

    כמו בסעיף א : \( O(len) \) לבקשה, עם \( \lceil len / RCB \rceil + 1 \) בלוקים לכל היותר.
    הפיצול הוא \( O(len / RCB) \) הטלות מטבע. ‏`get_next_completion` נשארה \( O(p) \)
    במספר הקריאות הפתוחות.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להתייחס ל-RCB כגודל Completion"
    "‏RCB = 128, אז נחזיר 128 בכל פעם" נותן ב-`0x10020` את החלוקה 128 + 128, שחותכת
    ב-`0x100A0` : לא גבול, ולכן Completion שה-Requester רשאי לדחות. ‏RCB אומר **איפה**
    מותר לחתוך, לא **כמה**. ה-Completion הראשון של בקשה לא מיושרת קצר מ-128 (או ארוך מ-128
    אם דילגו על גבול), והאחרון יכול להיות 32 בתים.

??? trap "מלכודת : Byte Count כגודל ה-payload"
    בפיצול 96 + 128 + 32 ערכי ה-Byte Count הם 256, 160, 32, לא 96, 128, 32. השדה אומר
    ל-Requester כמה בתים **עוד** יגיעו כולל ה-Completion הנוכחי, וכך הוא יודע מתי הבקשה
    הושלמה. רק ב-Completion האחרון שני המספרים שווים.

??? trap "מלכודת : להחליף בלוק שלם בכתיבה חלקית"
    ‏`memory[key] = new_block` נוח, אבל כתיבה של 32 בתים לאמצע בלוק קיים מאפסת 96 בתים
    של שכנים, וקריאה מאוחרת יותר מהם תחזיר אפסים במקום הנתונים הישנים. ה-scoreboard
    יתלונן על ה-DUT, שבעצם צודק. בלוק צריך לעבור קריאה-שינוי-כתיבה, או שהזיכרון
    נשמר ברזולוציית בית מלכתחילה (associative array של בתים : פשוט יותר, כבד יותר).

??? trap "מלכודת : אקראיות בין Completions במקום בין קריאות"
    תור אחד של כל ה-Completions שממנו שולפים אקראית הוא **שגוי** : הוא יכול לשלוח את
    החצי השני של קריאה לפני הראשון. תור FIFO אחד הוא **חוקי אבל חלש** : אין interleaving,
    והמודל לא ילמד את ה-scoreboard לקבל סדרים חוקיים אחרים. הנכון : תור לכל קריאה, אקראיות
    בבחירת **הקריאה**.

??? followup "שאלות המשך"
    - **כתיבה באמצע :** מה אם מגיעה כתיבה לאותה כתובת בין קבלת הקריאה לשידור
      ה-Completions שלה? במודל הנתונים נלקחים ברגע הבקשה, כפי שכללי הסדר של PCIe דורשים :
      קריאה לא עוקפת כתיבה posted שהגיעה לפניה, וכתיבה שהגיעה אחריה לא אמורה להשתקף
      בתשובה. מה ה-DUT עושה, ואיך בודקים את זה?
    - **איך בודקים את המודל עצמו :** הפלט אקראי, אז בודקים אינווריאנטים : כתובת ההתחלה של כל
      Completion היא סוף הקודם, חיתוכים על כפולות של RCB, ‏Byte Count שווה ליתרה, סכום
      ה-payloads שווה לאורך, הנתונים שווים לזיכרון צל ברזולוציית בית, וכל קריאה נסגרת.
      ועם seed קבוע : ריצה חוזרת.
    - **‏Coverage :** אילו bins מגדירים על הפיצול? (מספר ה-Completions, האם החיתוך היה בגבול
      הראשון או השני, קריאה שמתחילה באמצע בלוק ונגמרת באמצע בלוק אחר.) כמה פיצולים יש
      לבקשה כללית? ראו [0020](0020-pcie-completion-splits.md)
      ו-[0021](0021-pcie-completion-count.md).
    - **השדות שהשמטנו :** איך מוסיפים Lower Address (7 הביטים התחתונים של כתובת ההתחלה)
      ו-First/Last DW Byte Enable? מה משתנה כשהאורך נתון ב-DW?
    - **‏Tag חוזר :** מה המודל צריך לעשות אם מגיעה קריאה עם Requester ID ו-Tag של קריאה
      שעדיין פתוחה? (זו שגיאת פרוטוקול של ה-Requester : לדווח, לא לשרת.)
