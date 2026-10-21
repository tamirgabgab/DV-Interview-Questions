---
id: 24
title: מודל ייחוס לקרדיטים של נתיב USB4 – Credit Grant, שידור ו-Path Credit Sync
level: senior
difficulty: medium
tags: [protocols, usb4, python, systemverilog]
source: ""
added: 2026-10-19
---

## השאלה

ב-USB4 התעבורה עוברת במנהרות (tunnels) על גבי **נתיבים** (Paths): נתיב הוא חד-כיווני,
מ-**Egress Adapter** של הראוטר המשדר (כאן: ה-HOST) אל **Ingress Adapter** של הראוטר המקבל
(כאן: ה-DEVICE), ומזוהה ב-Hop ID. כל פקטה (Tunneled Packet) שנשלחת על הנתיב תופסת תא אחד
ב-**buffer ייעודי** של ה-Ingress Adapter, ולכן ה-Egress רשאי לשדר רק כשיש לו **קרדיט**:
הבטחה מראש לתא פנוי. כתבו **מודל ייחוס** (reference model) של בקרת הזרימה הזו
(Dedicated Flow Control, פרק 5 של המפרט), מהסוג שמחברים ל-scoreboard בסביבת אימות: המודל רואה את אותן
פקטות שה-DUT רואה, ויודע בכל רגע אם מותר לשדר ומה צריכים להכיל פקטי הקרדיטים.

לכל נתיב ארבעה מונים של 8 ביט. כולם **מצטברים** מאז הקמת הנתיב, ומתקדמים **מודולו 256**:

| מונה | מי מחזיק | משמעות |
|---|---|---|
| ‏PCC – Path Credits Consumed | ‏Egress | כמה פקטות שודרו בפועל |
| ‏PCL – Path Credit Limit | ‏Egress | הערך האחרון שהגיע ב-Credit Grant |
| ‏PCR – Path Credits Received | ‏Ingress | כמה פקטות התקבלו אל ה-buffer |
| ‏PCA – Path Credits Allocated | ‏Ingress | כמה תאים הוקצו לנתיב מאז ההקמה: ההקצאה ההתחלתית, ועוד תא על כל פקטה שיצאה מה-buffer |

שני פקטי ניהול עוברים בין הצדדים:

- **‏Credit Grant** (מה-Ingress אל ה-Egress): נושא את PCA הנוכחי, ערך מצטבר ולא תוספת.
  ה-Egress **מחליף** בו את PCL.
- **‏Path Credit Sync** (מה-Egress אל ה-Ingress): נושא את PCC הנוכחי. ה-Ingress משתמש בו כדי
  ליישר את החשבונאות שלו אחרי שפקטות אבדו (סעיף ב).

ההנחות: Dedicated Flow Control בלבד (בלי Shared Credits); כל פקטה צורכת קרדיט אחד; ה-buffer
הייעודי מכיל בדיוק `initial_credits` תאים; הקישור שומר על סדר (פקטה ששודרה לפני פקט אחר
מגיעה לפניו, או אובדת); פקטה שאבדה או שהגיעה פגומה אינה נספרת ב-Ingress; פרטי ה-Link Layer
(ECC, ‏HEC, תזמונים) מחוץ לשאלה. מחלקות הפקטים נתונות:

=== "SystemVerilog"
    ```systemverilog title="given classes"
    typedef bit [7:0] credit_t;      // every counter is 8 bits wide and wraps
    typedef bit [6:0] hop_id_t;

    class tunneled_packet;
      hop_id_t     hop_id;
      int unsigned packet_id;
      function new(hop_id_t hop_id = 0, int unsigned packet_id = 0);
        this.hop_id    = hop_id;
        this.packet_id = packet_id;
      endfunction
    endclass

    class credit_grant_packet;
      hop_id_t hop_id;
      credit_t credits;              // the Ingress Adapter's PCA, cumulative
    endclass

    class credit_sync_packet;
      hop_id_t hop_id;
      credit_t pcc;                  // the Egress Adapter's PCC, cumulative
    endclass
    ```

=== "Python"
    ```python title="given classes"
    from dataclasses import dataclass

    MOD = 256                        # every counter is 8 bits wide and wraps


    @dataclass
    class TunneledPacket:
        hop_id: int
        packet_id: int = 0


    @dataclass
    class CreditGrant:
        hop_id: int
        credits: int                 # the Ingress Adapter's PCA, cumulative


    @dataclass
    class CreditSync:
        hop_id: int
        pcc: int                     # the Egress Adapter's PCC, cumulative
    ```

??? interviewer "מה המראיין בודק"
    - **בעלות על מצב:** האם המועמד מפריד בין המונים של הצד המשדר למונים של הצד המקבל, ומבין
      שכל צד רואה את הצד השני **רק** דרך הפקטים שמגיעים ממנו.
    - **מונים מצטברים מול מצב רגעי:** האם הוא מבדיל בין "כמה תאים פנויים עכשיו" לבין מונה
      שרק עולה, ומה ההבדל בין ערך מצטבר שמחליף לבין תוספת שמצטברת.
    - **אריתמטיקה מודולו 256:** האם ההשוואה בין שני מונים נכונה גם אחרי גלישה, ואיך עושים
      אותה בקוד בלי מקרים מיוחדים.
    - **מודל ייחוס שבודק את הסביבה:** האם המודל מזהה הפרה (שידור בלי קרדיט, buffer מלא,
      ‏Hop ID זר) ומדווח, במקום להמשיך בשקט.
    - **סדר פעולות:** האם הוא שם לב שעדכון אחד משתמש בערך הישן של עדכון אחר, ומה קורה
      כשהופכים את הסדר.

---

### סעיף א – הזרימה התקינה: קרדיטים, שידור ו-Credit Grant

ממשו שתי מחלקות, אחת לכל צד של הנתיב:

- **‏Egress** (‏`egress_credit_model`): מאותחל עם Hop ID ומחזיק את PCC ואת PCL. הפונקציות:
  ‏`can_transmit()`, ‏`on_packet_transmitted()` (נקראת רק על פקטה ששודרה **בפועל**), ‏
  `consume_credit_grant(grant)`.
- **‏Ingress** (‏`ingress_credit_model`): מאותחל עם Hop ID ו-`initial_credits`, ומחזיק את PCR,
  את PCA ואת תפוסת ה-buffer. הפונקציות: `on_packet_received(pkt, accepted)` (ה-`accepted`
  מגיע מהמקלט: 0 לפקטה שהגיעה פגומה ולא נכנסה ל-buffer), ‏`on_packet_dequeued()` (פקטה
  יצאה מה-buffer), ‏`build_credit_grant()`.

המודל מזהה הפרות ומדווח עליהן: שידור בלי קרדיט, קבלה ל-buffer מלא, הוצאה מ-buffer ריק,
פקט עם Hop ID אחר, והקצאה התחלתית שאינה נכנסת למונה של 8 ביט.

הכלל לשידור, כפי שהוא כתוב במפרט: מותר לשדר כאשר \( 0 < PCL - PCC < 128 \), או
כאשר \( PCL - PCC < 0 \) וגם \( PCC - PCL > 128 \).

1. ה-Ingress הוקם עם 5 קרדיטים ושלח Credit Grant. ה-Egress שידר שלוש פקטות וכולן התקבלו;
   ה-Ingress הוציא שתיים מה-buffer ושלח Credit Grant נוסף. מה ערכי ארבעת המונים אחרי כל
   צעד, וכמה פקטות ה-Egress רשאי לשדר עכשיו?
2. ‏PCC = 251 ו-PCL = 254. כמה פקטות מותר לשדר? אחר כך מגיע Credit Grant עם הערך 2: כמה
   עכשיו? למה הבדיקה `PCL > PCC` אינה נכונה, ומה הבדיקה הנכונה?

??? tip "רמז 1"
    ‏PCL ו-PCC הם שני מונים מצטברים שמתחילים שניהם מאפס, וההפרש ביניהם הוא "כמה קרדיטים
    נשארו". איך מחשבים הפרש של שני מונים שגולשים ב-256?

??? tip "רמז 2"
    ציירו את 256 הערכים על מעגל. "יש קרדיטים" פירושו ש-PCL נמצא 1 עד 127 צעדים **קדימה**
    מ-PCC על המעגל, בלי קשר למי מהם מספר גדול יותר. המרחק קדימה הוא
    \( (PCL - PCC) \bmod 256 \).

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏(1) ‏Credit Grant: ‏PCL ‏0 ← 5. שלוש פקטות: PCC ו-PCR עולים יחד 1, 2, 3, התפוסה 3.
        שתי הוצאות: PCA ‏5 ← 6 ← 7, ‏PCR נשאר 3. ‏Credit Grant: ‏PCL = 7, ונשארו
        \( 7 - 3 = 4 \) פקטות. ‏(2) שלוש פקטות (251 עד 254), ואחרי Credit Grant של 2 עוד
        ארבע: ‏254, 255, 0, 1 ואז 2. ‏`PCL > PCC` נכשל בגלישה (‏\( 2 > 254 \) שקר, אף שיש
        ארבעה קרדיטים). הבדיקה הנכונה: המרחק קדימה \( (PCL - PCC) \bmod 256 \) הוא בין 1
        ל-127.

    #### הרעיון { .sol-idea }

    **כל צד סופר רק את מה שהוא רואה.** ה-Egress סופר פקטות ששידר (PCC) וזוכר את הגבול
    האחרון שקיבל (PCL). ה-Ingress סופר פקטות שנכנסו ל-buffer (PCR) ותאים שהקצה (PCA): בהקמה
    את כל התאים, ואחר כך תא על כל פקטה שיצאה מה-buffer, כי התא שלה התפנה. ה-Credit Grant
    מעביר את PCA, וה-Egress מחליף בו את PCL. כל המונים מצטברים, ולכן ההפרש
    \( PCL - PCC \) הוא "כמה תאים הובטחו לי ועוד לא השתמשתי בהם":

    ```mermaid
    sequenceDiagram
        participant H as HOST · Egress Adapter<br/>PCC, PCL
        participant D as DEVICE · Ingress Adapter<br/>PCR, PCA, RX buffer
        Note over D: Path setup: PCA = initial credits
        D->>H: Credit Grant (credits = PCA)
        Note over H: PCL = credits
        loop while (PCL − PCC) mod 256 is 1 … 127
            H->>D: Tunneled Packet
            Note over H: PCC += 1
            Note over D: accepted: PCR += 1, buffer += 1
        end
        Note over D: dequeue: buffer −= 1, PCA += 1
        D->>H: Credit Grant (credits = PCA)
        Note over H: PCL = credits
    ```

    **מונים על מעגל.** המונים הם 8 ביט, ולכן אחרי 255 בא 0. "יש קרדיטים" פירושו ש-PCL
    לפני PCC **על המעגל**, ולא שהמספר שלו גדול יותר. המרחק קדימה
    \( d = (PCL - PCC) \bmod 256 \) הוא תמיד מספר בין 0 ל-255, וכל עוד המרחק האמיתי קטן
    מ-128 הוא נמדד נכון, עם גלישה ובלי. כאן נכנס המספר 127 של המפרט: מרחק של 128 ומעלה
    נקרא כ"PCL מאחור", ולכן נתיב לא יכול להחזיק יותר מ-127 קרדיטים פתוחים. שני המקרים
    מהשאלה, בלי גלישה ועם גלישה, נותנים אותו מרחק:

    <svg class="figure" viewBox="0 0 640 294" style="max-width:40rem" role="img" aria-label="שני מצבים עם אותו מרחק קדימה: PCC = 9 ו-PCL = 13 בלי גלישה, PCC = 254 ו-PCL = 2 עם גלישה; בשניהם ארבעה קרדיטים"><text class="legend halo" x="160" y="22" text-anchor="middle">no wrap: PCC = 9, PCL = 13</text><circle class="fc-ring" cx="160" cy="156" r="86"/><line class="fc-tick" x1="160.0" y1="75.0" x2="160.0" y2="65.0"/><text class="tick" x="160.0" y="57.0" text-anchor="middle">0</text><line class="fc-tick" x1="217.3" y1="98.7" x2="224.3" y2="91.7"/><text class="tick" x="232.8" y="87.2" text-anchor="middle">32</text><line class="fc-tick" x1="241.0" y1="156.0" x2="251.0" y2="156.0"/><text class="tick" x="263.0" y="160.0" text-anchor="middle">64</text><line class="fc-tick" x1="217.3" y1="213.3" x2="224.3" y2="220.3"/><text class="tick" x="232.8" y="232.8" text-anchor="middle">96</text><line class="fc-tick" x1="160.0" y1="237.0" x2="160.0" y2="247.0"/><text class="tick" x="160.0" y="263.0" text-anchor="middle">128</text><line class="fc-tick" x1="102.7" y1="213.3" x2="95.7" y2="220.3"/><text class="tick" x="87.2" y="232.8" text-anchor="middle">160</text><line class="fc-tick" x1="79.0" y1="156.0" x2="69.0" y2="156.0"/><text class="tick" x="57.0" y="160.0" text-anchor="middle">192</text><line class="fc-tick" x1="102.7" y1="98.7" x2="95.7" y2="91.7"/><text class="tick" x="87.2" y="87.2" text-anchor="middle">224</text><path class="fc-window" d="M180.9,72.6 A86,86 0 0 1 143.2,240.3"/><path class="fc-ahead" d="M178.8,72.1 A86,86 0 0 1 187.0,74.3"/><line class="fc-tick" x1="178.8" y1="72.1" x2="144.6" y2="30.9"/><circle class="ink-dot" cx="178.8" cy="72.1" r="5.5"><title>PCC = 9</title></circle><text class="coord halo" x="144.6" y="34.9" text-anchor="middle">PCC 9</text><line class="fc-tick" x1="187.0" y1="74.3" x2="237.5" y2="56.7"/><circle class="s3-dot" cx="187.0" cy="74.3" r="5.5"><title>PCL = 13</title></circle><text class="coord halo" x="237.5" y="60.7" text-anchor="middle">PCL 13</text><text class="st-text" x="160" y="157" text-anchor="middle">4 credits</text><text class="tick" x="160" y="176" text-anchor="middle">(13 − 9) mod 256 = 4</text><text class="legend halo" x="480" y="22" text-anchor="middle">wrap: PCC = 254, PCL = 2</text><circle class="fc-ring" cx="480" cy="156" r="86"/><line class="fc-tick" x1="480.0" y1="75.0" x2="480.0" y2="65.0"/><text class="tick" x="480.0" y="57.0" text-anchor="middle">0</text><line class="fc-tick" x1="537.3" y1="98.7" x2="544.3" y2="91.7"/><text class="tick" x="552.8" y="87.2" text-anchor="middle">32</text><line class="fc-tick" x1="561.0" y1="156.0" x2="571.0" y2="156.0"/><text class="tick" x="583.0" y="160.0" text-anchor="middle">64</text><line class="fc-tick" x1="537.3" y1="213.3" x2="544.3" y2="220.3"/><text class="tick" x="552.8" y="232.8" text-anchor="middle">96</text><line class="fc-tick" x1="480.0" y1="237.0" x2="480.0" y2="247.0"/><text class="tick" x="480.0" y="263.0" text-anchor="middle">128</text><line class="fc-tick" x1="422.7" y1="213.3" x2="415.7" y2="220.3"/><text class="tick" x="407.2" y="232.8" text-anchor="middle">160</text><line class="fc-tick" x1="399.0" y1="156.0" x2="389.0" y2="156.0"/><text class="tick" x="377.0" y="160.0" text-anchor="middle">192</text><line class="fc-tick" x1="422.7" y1="98.7" x2="415.7" y2="91.7"/><text class="tick" x="407.2" y="87.2" text-anchor="middle">224</text><path class="fc-window" d="M477.9,70.0 A86,86 0 0 1 486.3,241.8"/><path class="fc-ahead" d="M475.8,70.1 A86,86 0 0 1 484.2,70.1"/><line class="fc-tick" x1="475.8" y1="70.1" x2="431.8" y2="39.6"/><circle class="ink-dot" cx="475.8" cy="70.1" r="5.5"><title>PCC = 254</title></circle><text class="coord halo" x="431.8" y="43.6" text-anchor="middle">PCC 254</text><line class="fc-tick" x1="484.2" y1="70.1" x2="528.2" y2="39.6"/><circle class="s3-dot" cx="484.2" cy="70.1" r="5.5"><title>PCL = 2</title></circle><text class="coord halo" x="528.2" y="43.6" text-anchor="middle">PCL 2</text><text class="st-text" x="480" y="157" text-anchor="middle">4 credits</text><text class="tick" x="480" y="176" text-anchor="middle">(2 − 254) mod 256 = 4</text></svg>

    <span class="viz-legend"><span><i class="ink"></i>‏PCC</span><span><i class="s3"></i>‏PCL</span><span><i class="fc-ahead"></i>המרחק קדימה: הקרדיטים שנותרו</span><span><i class="fc-window"></i>חלון של 127 צעדים קדימה מ-PCC: רק שם PCL נקרא כ"לפני"</span></span>

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הקמה:** ‏Egress: ‏PCC = 0, ‏PCL = 0. ‏Ingress: ‏PCR = 0, ‏PCA = `initial_credits`,
       ‏buffer ריק. ערך התחלתי שאינו בין 1 ל-255 נדחה.
    2. **מרחק קדימה:** פונקציה אחת, \( (b - a) \bmod 256 \), משרתת את כל ההשוואות. ‏
       `can_transmit` מחזירה אמת כשהמרחק מ-PCC ל-PCL הוא 1 עד 127.
    3. **שידור:** אחרי בדיקת `can_transmit`, ‏PCC מתקדם באחד. שידור בלי קרדיט הוא הפרה.
    4. **קבלה:** פקטה שהתקבלה ל-buffer מקדמת את PCR ואת התפוסה; פקטה פגומה לא משנה דבר.
       קבלה ל-buffer מלא היא הפרה.
    5. **הוצאה מה-buffer:** התפוסה יורדת ו-PCA עולה באחד. ‏PCR לא משתנה.
    6. **‏Credit Grant:** ה-Ingress שולח את PCA; ה-Egress בודק Hop ID ומחליף את PCL בערך
       שהגיע.

    </div>

    #### הקוד { .sol-code }

    שתי מחלקות קטנות ופונקציית עזר אחת למרחק על המעגל. ההפרש מחושב בטיפוס רחב וחתום ורק
    אז נחתך ל-8 ביט, כדי שגלישה לא תהיה מקרה מיוחד.

    === "SystemVerilog"
        ```systemverilog title="egress_credit_model, ingress_credit_model" linenums="1" hl_lines="3 21 38 57 66 82 88"
        // How far b is ahead of a on the modulo-256 circle: 0..255.
        function automatic credit_t forward_distance(credit_t a, credit_t b);
          return credit_t'(int'(b) - int'(a));                                 // (1)!
        endfunction

        // The transmitting side of one Path: what it consumed, and the limit it was granted.
        class egress_credit_model;
          hop_id_t hop_id;
          credit_t pcc;                  // Path Credits Consumed: packets actually transmitted
          credit_t pcl;                  // Path Credit Limit: the latest Credit Grant

          function new(hop_id_t hop_id);
            this.hop_id = hop_id;
            pcc = 0;
            pcl = 0;
          endfunction

          // The limit is 1..127 steps ahead of the consumed counter on the circle.
          function bit can_transmit();
            credit_t ahead = forward_distance(pcc, pcl);
            return ahead > 0 && ahead < 128;                                   // (2)!
          endfunction

          // Called for a packet that really went out, after can_transmit() said yes.
          function void on_packet_transmitted();
            if (!can_transmit()) begin
              $error("hop %0d: transmission without a Path credit (PCC=%0d, PCL=%0d)", hop_id, pcc, pcl);
              return;
            end
            pcc = credit_t'(pcc + 1);
          endfunction

          function void consume_credit_grant(credit_grant_packet grant);
            if (grant == null || grant.hop_id != hop_id) begin
              $error("hop %0d: Credit Grant of another Path, or null", hop_id);
              return;
            end
            pcl = grant.credits;                                               // (3)!
          endfunction
        endclass

        // The receiving side of one Path: a dedicated buffer, what it received, what it freed.
        class ingress_credit_model;
          hop_id_t     hop_id;
          int unsigned buffer_size;      // slots of the dedicated RX buffer = the initial credits
          int unsigned rx_occupancy;
          credit_t     pcr;              // Path Credits Received: packets accepted into the buffer
          credit_t     pca;              // Path Credits Allocated: slots ever handed to the Path

          function new(hop_id_t hop_id, int unsigned initial_credits);
            if (initial_credits == 0 || initial_credits > 255)
              $error("hop %0d: %0d initial credits do not fit an 8-bit counter", hop_id, initial_credits);
            this.hop_id  = hop_id;
            buffer_size  = initial_credits;
            rx_occupancy = 0;
            pcr = 0;
            pca = credit_t'(initial_credits);                                  // (4)!
          endfunction

          // `accepted` comes from the receiver: a corrupted packet never enters the buffer.
          function void on_packet_received(tunneled_packet pkt, bit accepted = 1);
            if (pkt == null || pkt.hop_id != hop_id) begin
              $error("hop %0d: packet of another Path, or null", hop_id);
              return;
            end
            if (!accepted) return;                                             // (5)!
            if (rx_occupancy >= buffer_size) begin
              $error("hop %0d: dedicated RX buffer overflow", hop_id);
              return;
            end
            pcr = credit_t'(pcr + 1);
            rx_occupancy++;
          endfunction

          // A packet left the buffer: its slot is free again, so one more credit, cumulative.
          function void on_packet_dequeued();
            if (rx_occupancy == 0) begin
              $error("hop %0d: dequeue from an empty RX buffer", hop_id);
              return;
            end
            rx_occupancy--;
            pca = credit_t'(pca + 1);                                          // (6)!
          endfunction

          function credit_grant_packet build_credit_grant();
            credit_grant_packet grant = new();
            grant.hop_id  = hop_id;
            grant.credits = pca;                                               // (7)!
            return grant;
          endfunction
        endclass
        ```

        1. ההפרש מחושב ב-`int` חתום, למשל \( 2 - 254 = -252 \), והחיתוך ל-8 ביט נותן
           \( -252 \bmod 256 = 4 \). בלי ההרחבה ל-`int` התוצאה זהה, אבל הכוונה פחות
           ברורה.
        2. תנאי אחד לשני המקרים של המפרט: מרחק 1 עד 127 קדימה. ‏0 פירושו שהקרדיטים נגמרו,
           ו-128 ומעלה פירושו ש-PCL מאחורי PCC, כלומר Credit Grant ישן או מושחת.
        3. החלפה, לא חיבור: ‏Credit Grant נושא ערך מצטבר. חיבור היה מכפיל קרדיטים בכל Grant
           חוזר.
        4. ‏PCA מתחיל מגודל ה-buffer: אלה התאים שהוקצו לנתיב בהקמה, ואותם ה-Ingress יפרסם
           ב-Credit Grant הראשון.
        5. פקטה שלא נכנסה ל-buffer לא משנה אף מונה. ה-Egress כן ספר אותה ב-PCC, וזה הפער
           שסעיף ב מתקן.
        6. ‏PCA עולה כשהתא **מתפנה**, לא כשהפקטה **מתקבלת**: הקבלה תופסת תא, ההוצאה
           משחררת אותו.
        7. הערך המצטבר, לא מספר התאים הפנויים ולא כמה תאים התפנו מאז ה-Grant הקודם.

    === "Python"
        ```python title="EgressCreditModel, IngressCreditModel" linenums="1" hl_lines="3 23 34 48 54 65 68"
        def forward_distance(a: int, b: int) -> int:
            """How far b is ahead of a on the modulo-256 circle: 0..255."""
            return (b - a) % MOD                                             # (1)!


        def check_hop(hop_id: int, pkt) -> None:
            """Every packet of the Path carries its Hop ID; anything else is an environment bug."""
            if pkt.hop_id != hop_id:
                raise ValueError(f"hop {hop_id}: packet of hop {pkt.hop_id}")


        class EgressCreditModel:
            """The transmitting side of one Path: what it consumed, and the limit it was granted."""

            def __init__(self, hop_id: int):
                self.hop_id = hop_id
                self.pcc = 0             # Path Credits Consumed: packets actually transmitted
                self.pcl = 0             # Path Credit Limit: the latest Credit Grant

            def can_transmit(self) -> bool:
                """The limit is 1..127 steps ahead of the consumed counter on the circle."""
                ahead = forward_distance(self.pcc, self.pcl)
                return 0 < ahead < 128                                       # (2)!

            def on_packet_transmitted(self) -> None:
                """Called for a packet that really went out, after can_transmit() said yes."""
                if not self.can_transmit():
                    raise ValueError(f"hop {self.hop_id}: transmission without a Path credit "
                                     f"(PCC={self.pcc}, PCL={self.pcl})")
                self.pcc = (self.pcc + 1) % MOD

            def consume_credit_grant(self, grant: CreditGrant) -> None:
                check_hop(self.hop_id, grant)
                self.pcl = grant.credits                                     # (3)!


        class IngressCreditModel:
            """The receiving side of one Path: a dedicated buffer, what it received, what it freed."""

            def __init__(self, hop_id: int, initial_credits: int):
                if not 0 < initial_credits < MOD:
                    raise ValueError(f"hop {hop_id}: {initial_credits} initial credits do not fit "
                                     "an 8-bit counter")
                self.hop_id = hop_id
                self.buffer_size = initial_credits   # slots of the dedicated RX buffer
                self.rx_occupancy = 0
                self.pcr = 0                         # Path Credits Received: packets accepted
                self.pca = initial_credits           # Path Credits Allocated: slots ever handed out  (4)

            def on_packet_received(self, pkt: TunneledPacket, accepted: bool = True) -> None:
                """`accepted` comes from the receiver: a corrupted packet never enters the buffer."""
                check_hop(self.hop_id, pkt)
                if not accepted:
                    return                                                   # (5)!
                if self.rx_occupancy >= self.buffer_size:
                    raise ValueError(f"hop {self.hop_id}: dedicated RX buffer overflow")
                self.pcr = (self.pcr + 1) % MOD
                self.rx_occupancy += 1

            def on_packet_dequeued(self) -> None:
                """A packet left the buffer: its slot is free again, so one more credit, cumulative."""
                if self.rx_occupancy == 0:
                    raise ValueError(f"hop {self.hop_id}: dequeue from an empty RX buffer")
                self.rx_occupancy -= 1
                self.pca = (self.pca + 1) % MOD                              # (6)!

            def build_credit_grant(self) -> CreditGrant:
                return CreditGrant(self.hop_id, self.pca)                    # (7)!
        ```

        1. ‏`%` של Python מחזיר תמיד ערך בין 0 ל-255, גם להפרש שלילי: \( (2 - 254) \bmod 256 = 4 \).
        2. תנאי אחד לשני המקרים של המפרט: מרחק 1 עד 127 קדימה. ‏0 פירושו שהקרדיטים נגמרו,
           ו-128 ומעלה פירושו ש-PCL מאחורי PCC, כלומר Credit Grant ישן או מושחת.
        3. החלפה, לא חיבור: ‏Credit Grant נושא ערך מצטבר. חיבור היה מכפיל קרדיטים בכל Grant
           חוזר.
        4. ‏PCA מתחיל מגודל ה-buffer: אלה התאים שהוקצו לנתיב בהקמה, ואותם ה-Ingress יפרסם
           ב-Credit Grant הראשון.
        5. פקטה שלא נכנסה ל-buffer לא משנה אף מונה. ה-Egress כן ספר אותה ב-PCC, וזה הפער
           שסעיף ב מתקן.
        6. ‏PCA עולה כשהתא **מתפנה**, לא כשהפקטה **מתקבלת**: הקבלה תופסת תא, ההוצאה
           משחררת אותו.
        7. הערך המצטבר, לא מספר התאים הפנויים ולא כמה תאים התפנו מאז ה-Grant הקודם.

    #### למה זה נכון { .sol-proof }

    **הדוגמה מהשאלה, צעד אחרי צעד.** הערכים מסומנים כשהם משתנים; "credits" הוא המרחק קדימה
    מ-PCC ל-PCL:

    <div class="stepper" role="group" aria-label="הזרימה התקינה, צעד אחרי צעד: Credit Grant, שלוש פקטות, שתי הוצאות ו-Grant נוסף" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 0: הקמת הנתיב; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fca0-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca0-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca0-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 0 · Path setup</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">0</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">0</text><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">0</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">0</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">5</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-slot" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">0 of 5 slots used</text><text class="coord" x="320" y="118" text-anchor="middle" font-weight="700">Path setup</text></svg><figcaption>צעד 0: הקמת הנתיב. ה-Egress מתחיל מ-PCC = 0 ו-PCL = 0; ה-Ingress מ-PCR = 0 ו-PCA = 5, כמספר התאים ב-buffer. המרחק מ-PCC ל-PCL הוא 0, ולכן עדיין אסור לשדר.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 1: ‏Credit Grant של 5; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fca1-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca1-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca1-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 1 · Credit Grant (5)</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">0</text><rect class="st-cur" x="180" y="97" width="56" height="24" rx="4"/><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">5</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">0</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">5</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-slot" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">0 of 5 slots used</text><line class="fc-grant" x1="388" y1="118" x2="256" y2="118" marker-end="url(#fca1-s3)"/><text class="tick" x="320" y="104" text-anchor="middle">Credit Grant (5)</text><text class="tick" x="320" y="138" text-anchor="middle">credits = PCA</text><text class="tick" x="320" y="154" text-anchor="middle">→ PCL</text></svg><figcaption>צעד 1: ה-Ingress שולח Credit Grant עם PCA = 5, וה-Egress מחליף: PCL = 5. המרחק מ-PCC = 0 הוא 5 קרדיטים. בדיוק מספר התאים הפנויים, 5.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 2: פקטה 1 שודרה והתקבלה; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fca2-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca2-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca2-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 2 · packet 1</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><rect class="st-cur" x="180" y="71" width="56" height="24" rx="4"/><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">1</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">4</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><rect class="st-cur" x="558" y="71" width="56" height="24" rx="4"/><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">1</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">5</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">1 of 5 slots used</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#fca2-s1)"/><text class="tick" x="320" y="104" text-anchor="middle">packet 1</text><text class="tick" x="320" y="138" text-anchor="middle">PCC + 1, PCR + 1</text></svg><figcaption>צעד 2: פקטה 1 שודרה והתקבלה. ‏PCC = 1, ‏PCR = 1, התפוסה 1. נשארו 4 קרדיטים.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 3: פקטה 2 שודרה והתקבלה; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fca3-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca3-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca3-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 3 · packet 2</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><rect class="st-cur" x="180" y="71" width="56" height="24" rx="4"/><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">2</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">3</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><rect class="st-cur" x="558" y="71" width="56" height="24" rx="4"/><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">2</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">5</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-full" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">2 of 5 slots used</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#fca3-s1)"/><text class="tick" x="320" y="104" text-anchor="middle">packet 2</text><text class="tick" x="320" y="138" text-anchor="middle">PCC + 1, PCR + 1</text></svg><figcaption>צעד 3: פקטה 2 שודרה והתקבלה. ‏PCC = 2, ‏PCR = 2, התפוסה 2. נשארו 3 קרדיטים.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 4: פקטה 3 שודרה והתקבלה; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fca4-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca4-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca4-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 4 · packet 3</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><rect class="st-cur" x="180" y="71" width="56" height="24" rx="4"/><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">3</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">2</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><rect class="st-cur" x="558" y="71" width="56" height="24" rx="4"/><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">3</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">5</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-full" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-full" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">3 of 5 slots used</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#fca4-s1)"/><text class="tick" x="320" y="104" text-anchor="middle">packet 3</text><text class="tick" x="320" y="138" text-anchor="middle">PCC + 1, PCR + 1</text></svg><figcaption>צעד 4: פקטה 3 שודרה והתקבלה. ‏PCC = 3, ‏PCR = 3, התפוסה 3. נשארו 2 קרדיטים.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 5: פקטה יצאה מה-buffer; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fca5-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca5-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca5-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 5 · dequeue</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">3</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">2</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">3</text><rect class="st-cur" x="558" y="97" width="56" height="24" rx="4"/><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">6</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-full" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">2 of 5 slots used</text><text class="coord" x="320" y="112" text-anchor="middle" font-weight="700">dequeue</text><text class="tick" x="320" y="138" text-anchor="middle">one slot freed:</text><text class="tick" x="320" y="154" text-anchor="middle">PCA + 1</text></svg><figcaption>צעד 5: פקטה יוצאת מה-buffer. התפוסה 2, ‏PCA = 6. ‏PCR נשאר 3: הוא סופר קבלות, לא תפוסה.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 6: פקטה יצאה מה-buffer; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fca6-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca6-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca6-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 6 · dequeue</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">3</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">2</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">3</text><rect class="st-cur" x="558" y="97" width="56" height="24" rx="4"/><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">7</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">1 of 5 slots used</text><text class="coord" x="320" y="112" text-anchor="middle" font-weight="700">dequeue</text><text class="tick" x="320" y="138" text-anchor="middle">one slot freed:</text><text class="tick" x="320" y="154" text-anchor="middle">PCA + 1</text></svg><figcaption>צעד 6: פקטה יוצאת מה-buffer. התפוסה 1, ‏PCA = 7. ‏PCR נשאר 3: הוא סופר קבלות, לא תפוסה.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 7: ‏Credit Grant של 7; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fca7-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca7-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca7-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 7 · Credit Grant (7)</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">3</text><rect class="st-cur" x="180" y="97" width="56" height="24" rx="4"/><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">7</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">4</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">3</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">7</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">1 of 5 slots used</text><line class="fc-grant" x1="388" y1="118" x2="256" y2="118" marker-end="url(#fca7-s3)"/><text class="tick" x="320" y="104" text-anchor="middle">Credit Grant (7)</text><text class="tick" x="320" y="138" text-anchor="middle">credits = PCA</text><text class="tick" x="320" y="154" text-anchor="middle">→ PCL</text></svg><figcaption>צעד 7: ה-Ingress שולח Credit Grant עם PCA = 7, וה-Egress מחליף: PCL = 7. המרחק מ-PCC = 3 הוא 4 קרדיטים. בדיוק מספר התאים הפנויים, 4.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 8: פקטות 4 עד 7 שודרו והתקבלו; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fca8-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca8-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fca8-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 8 · packets 4 … 7</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><rect class="st-cur" x="180" y="71" width="56" height="24" rx="4"/><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">7</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">7</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">0</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><rect class="st-cur" x="558" y="71" width="56" height="24" rx="4"/><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">7</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">7</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-full" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-full" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-full" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-full" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">5 of 5 slots used</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#fca8-s1)"/><text class="tick" x="320" y="104" text-anchor="middle">packets 4 … 7</text><text class="tick" x="320" y="138" text-anchor="middle">PCC + 1, PCR + 1</text></svg><figcaption>צעד 8: פקטות 4 עד 7 שודרו והתקבלו. ‏PCC = 7 = PCL, ‏PCR = 7, התפוסה 5 וה-buffer מלא. המרחק 0, ולכן can_transmit מחזירה 0 עד ה-Credit Grant הבא.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="9"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <span class="viz-legend"><span><i class="fc-full"></i>תא תפוס ב-buffer</span><span><i class="fc-slot"></i>תא פנוי</span><span><i class="st-cur"></i>ערך שהשתנה בצעד הזה</span><span><i class="fc-pkt"></i>‏Tunneled Packet, מה-HOST ל-DEVICE</span><span><i class="fc-grant"></i>‏Credit Grant, מה-DEVICE ל-HOST</span><span><i class="fc-sync"></i>‏Path Credit Sync</span><span><i class="fc-drop"></i>פקטה שאבדה בדרך</span></span>

    | צעד | אירוע | ‏PCC | ‏PCL | ‏PCR | ‏PCA | תפוסה | קרדיטים |
    |---|---|---|---|---|---|---|---|
    | 0 | הקמת הנתיב | 0 | 0 | 0 | 5 | 0 | 0 |
    | 1 | ‏Credit Grant של 5 | 0 | 5 | 0 | 5 | 0 | 5 |
    | 2 | פקטה 1 שודרה והתקבלה | 1 | 5 | 1 | 5 | 1 | 4 |
    | 3 | פקטה 2 שודרה והתקבלה | 2 | 5 | 2 | 5 | 2 | 3 |
    | 4 | פקטה 3 שודרה והתקבלה | 3 | 5 | 3 | 5 | 3 | 2 |
    | 5 | פקטה יצאה מה-buffer | 3 | 5 | 3 | 6 | 2 | 2 |
    | 6 | פקטה יצאה מה-buffer | 3 | 5 | 3 | 7 | 1 | 2 |
    | 7 | ‏Credit Grant של 7 | 3 | 7 | 3 | 7 | 1 | 4 |
    | 8 | פקטות 4 עד 7 שודרו והתקבלו | 7 | 7 | 7 | 7 | 5 | 0 |
        
    **למה ה-buffer לעולם לא עולה על גדותיו.** נסמן במספרים שלמים (בלי מודולו): \( T \)
    פקטות שודרו, \( R \) התקבלו, \( D \) יצאו מה-buffer, ו-\( N \) הוא גודל ה-buffer. בלי
    אובדנים \( R \le T \), והתפוסה היא \( R - D \). ‏PCA שווה ל-\( N + D \), ו-PCL הוא PCA
    של רגע ה-Grant האחרון, \( N + D' \) עם \( D' \le D \). ההפרש האמיתי
    \( PCL - PCC = N + D' - T \) הוא בין 0 ל-\( N \), ולכן כל עוד \( N \le 127 \) המרחק
    קדימה על המעגל שווה לו בדיוק. שידור מותר רק כשההפרש הוא לפחות 1, כלומר
    \( T + 1 \le N + D' \le N + D \), ואז אחרי שהפקטה תתקבל התפוסה
    \( R + 1 - D \le T + 1 - D \le N \). ‏PCL מפגר אחרי PCA רק לכיוון הבטוח: ה-Egress עשוי
    לראות **פחות** קרדיטים מהתאים הפנויים, לעולם לא יותר.

    **הכלל של המפרט הוא אותו תנאי.** נסמן \( s = PCL - PCC \) כמספר חתום בין \( -255 \)
    ל-255, ו-\( d = s \bmod 256 \) את המרחק קדימה:

    | המקרה | ‏\( s \) | ‏\( d = s \bmod 256 \) | המפרט | ‏`can_transmit` |
    |---|---|---|---|---|
    | ‏PCL מעט לפני, בלי גלישה | ‏\( 1 \ldots 127 \) | ‏\( s \) | מותר (התנאי הראשון) | מותר |
    | ‏PCL מעט לפני, עם גלישה | ‏\( -255 \ldots -129 \) | ‏\( s + 256 = 1 \ldots 127 \) | מותר (התנאי השני: \( PCC - PCL > 128 \)) | מותר |
    | הקרדיטים נגמרו | ‏0 | ‏0 | אסור | אסור |
    | ‏PCL "מאחור" | ‏\( -128 \ldots -1 \) או \( 128 \ldots 255 \) | ‏\( 128 \ldots 255 \) | אסור | אסור |

    בדוגמה 2: ‏\( s = 254 - 251 = 3 \) ואז 3 פקטות; אחרי Credit Grant של 2, ‏
    \( s = 2 - 254 = -252 \), ‏\( d = 4 \), ו-`PCL > PCC` היה אומר "אפס". ה-test מריץ את
    ההשוואה הזו על כל 65,536 הזוגות.

    #### סיבוכיות { .sol-cost }

    כל פעולה היא \( O(1) \): חיבור, חיסור ו-mod על בתים. המצב של נתיב הוא ארבעה בתים ותפוסה
    אחת, בלי תורים, ולכן אפשר להחזיק מודל לכל Hop ID בלי לחשוב על זיכרון.

---

### סעיף ב – אובדן פקטה ו-Path Credit Sync

אותו נתיב ואותה התחלה: Credit Grant של 5. הפעם הפקטה **השנייה** מבין השלוש אובדת בדרך:
ה-Egress שידר אותה, וה-Ingress לא קיבל אותה.

1. מה ערכי המונים בשני הצדדים אחרי הפקטה השלישית? ה-Ingress מוציא מה-buffer את שתי
   הפקטות שקיבל ושולח Credit Grant: כמה קרדיטים ה-Egress רואה, וכמה תאים פנויים יש באמת?
   מה יקרה אחרי עוד ארבעה אובדנים כאלה?
2. ממשו `build_credit_sync()` ב-Egress ו-`consume_credit_sync(sync)` ב-Ingress, כך שאחרי
   ‏Sync ו-Credit Grant נוסף שני הצדדים מסכימים שוב. באיזה סדר מעדכנים את PCA ואת PCR,
   ולמה?
3. לפני ה-Sync: ‏PCA = 254 ו-PCR = 253, וב-Sync הגיע PCC = 1. מה המצב אחריו?

??? tip "רמז 1"
    בלי אובדנים PCC של ה-Egress ו-PCR של ה-Ingress שווים (בניכוי מה שעדיין בדרך). פקטה
    שאבדה הזיזה את PCC אבל לא את PCR, ולעולם לא תצא מה-buffer, ולכן PCA לעולם לא יתקדם
    בשבילה. מי "חייב" למי קרדיט?

??? tip "רמז 2"
    ה-Sync מביא ל-Ingress את PCC. המרחק קדימה מ-PCR אל PCC הוא בדיוק מספר הפקטות שאבדו
    מאז היישור הקודם. מה עושים עם המספר הזה, ומה צריך לקרות ל-PCR כדי שאותם אובדנים לא
    ייספרו פעמיים ב-Sync הבא?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏(1) אחרי שלוש פקטות: PCC = 3 אבל PCR = 2, התפוסה 2, ‏PCA = 5. אחרי שתי הוצאות
        ‏PCA = 7, ו-Credit Grant נותן PCL = 7: ה-Egress רואה \( 7 - 3 = 4 \) קרדיטים
        וה-buffer ריק עם 5 תאים. קרדיט אחד דלף; אחרי חמישה אובדנים הנתיב נתקע לתמיד. ‏(2)
        ‏Sync נושא את PCC. ה-Ingress מחשב \( missing = (PCC_{sync} - PCR) \bmod 256 \) עם
        ה-PCR **הישן**, מוסיף אותו ל-PCA, ורק אז קובע \( PCR = PCC_{sync} \). בדוגמה:
        ‏PCA ‏7 ← 8, ‏PCR ‏2 ← 3, וה-Grant הבא נותן PCL = 8, חמישה קרדיטים. ‏(3) המרחק
        מ-253 ל-1 הוא 4, ולכן PCA = (254 + 4) mod 256 = 2 ו-PCR = 1.

    #### הרעיון { .sol-idea }

    **איפה הקרדיט נעלם.** ה-Egress צרך קרדיט לפקטה 2 (‏PCC = 2), אבל ה-Ingress מעולם לא
    ראה אותה: היא לא נכנסה ל-buffer, לא תצא ממנו, ו-PCA לא יעלה בשבילה. מאותו רגע PCA
    מפגר אחרי מה שהיה צריך להיות באחד, וכל Credit Grant עתידי מפגר איתו: ה-Egress רואה
    תמיד קרדיט אחד פחות מהתאים הפנויים. אובדנים מצטברים, ואחרי \( N \) אובדנים ה-Egress
    לא ישדר יותר לעולם, אף שה-buffer ריק.

    **התיקון.** ה-Ingress לא יכול לדעת על פקטה שלא הגיעה, אבל ה-Egress יודע כמה שידר. ‏
    Path Credit Sync מביא את PCC ל-Ingress, והמרחק קדימה מ-PCR אל PCC הוא מספר הפקטות
    ששודרו ולא התקבלו. הקישור שומר על סדר, ולכן כשה-Sync מגיע כל פקטה ששודרה לפניו כבר
    התקבלה או אבדה: המרחק הוא בדיוק האובדנים, בלי פקטות שעדיין בדרך. התאים שלהן מעולם לא
    נתפסו, ולכן הקרדיטים חוזרים ל-PCA, ואז PCR מיושר ל-PCC כדי שהאובדנים האלה לא ייספרו
    שוב ב-Sync הבא. הסדר הוא העיקר: אם PCR מתעדכן קודם, המרחק הוא אפס והתיקון ריק.
    הדוגמה השלישית, על המעגל:

    <svg class="figure" viewBox="0 0 640 294" style="max-width:40rem" role="img" aria-label="תיקון ה-Credit Sync מעבר לגלישה: מ-PCR = 253 ל-PCC = 1 המרחק 4, ולכן PCA מתקדם מ-254 ל-2"><text class="legend halo" x="160" y="22" text-anchor="middle">Sync: PCR = 253, received PCC = 1</text><circle class="fc-ring" cx="160" cy="156" r="86"/><line class="fc-tick" x1="160.0" y1="75.0" x2="160.0" y2="65.0"/><text class="tick" x="160.0" y="57.0" text-anchor="middle">0</text><line class="fc-tick" x1="217.3" y1="98.7" x2="224.3" y2="91.7"/><text class="tick" x="232.8" y="87.2" text-anchor="middle">32</text><line class="fc-tick" x1="241.0" y1="156.0" x2="251.0" y2="156.0"/><text class="tick" x="263.0" y="160.0" text-anchor="middle">64</text><line class="fc-tick" x1="217.3" y1="213.3" x2="224.3" y2="220.3"/><text class="tick" x="232.8" y="232.8" text-anchor="middle">96</text><line class="fc-tick" x1="160.0" y1="237.0" x2="160.0" y2="247.0"/><text class="tick" x="160.0" y="263.0" text-anchor="middle">128</text><line class="fc-tick" x1="102.7" y1="213.3" x2="95.7" y2="220.3"/><text class="tick" x="87.2" y="232.8" text-anchor="middle">160</text><line class="fc-tick" x1="79.0" y1="156.0" x2="69.0" y2="156.0"/><text class="tick" x="57.0" y="160.0" text-anchor="middle">192</text><line class="fc-tick" x1="102.7" y1="98.7" x2="95.7" y2="91.7"/><text class="tick" x="87.2" y="87.2" text-anchor="middle">224</text><path class="fc-window" d="M155.8,70.1 A86,86 0 0 1 168.4,241.6"/><path class="fc-ahead" d="M153.7,70.2 A86,86 0 0 1 162.1,70.0"/><line class="fc-tick" x1="153.7" y1="70.2" x2="108.9" y2="40.8"/><circle class="ink-dot" cx="153.7" cy="70.2" r="5.5"><title>PCR = 253</title></circle><text class="coord halo" x="108.9" y="44.8" text-anchor="middle">PCR 253</text><line class="fc-tick" x1="162.1" y1="70.0" x2="205.3" y2="38.4"/><circle class="s3-dot" cx="162.1" cy="70.0" r="5.5"><title>PCC = 1</title></circle><text class="coord halo" x="205.3" y="42.4" text-anchor="middle">PCC 1</text><text class="st-text" x="160" y="157" text-anchor="middle">4 missing</text><text class="tick" x="160" y="176" text-anchor="middle">(1 − 253) mod 256 = 4</text><text class="legend halo" x="480" y="22" text-anchor="middle">PCA = (254 + 4) mod 256</text><circle class="fc-ring" cx="480" cy="156" r="86"/><line class="fc-tick" x1="480.0" y1="75.0" x2="480.0" y2="65.0"/><text class="tick" x="480.0" y="57.0" text-anchor="middle">0</text><line class="fc-tick" x1="537.3" y1="98.7" x2="544.3" y2="91.7"/><text class="tick" x="552.8" y="87.2" text-anchor="middle">32</text><line class="fc-tick" x1="561.0" y1="156.0" x2="571.0" y2="156.0"/><text class="tick" x="583.0" y="160.0" text-anchor="middle">64</text><line class="fc-tick" x1="537.3" y1="213.3" x2="544.3" y2="220.3"/><text class="tick" x="552.8" y="232.8" text-anchor="middle">96</text><line class="fc-tick" x1="480.0" y1="237.0" x2="480.0" y2="247.0"/><text class="tick" x="480.0" y="263.0" text-anchor="middle">128</text><line class="fc-tick" x1="422.7" y1="213.3" x2="415.7" y2="220.3"/><text class="tick" x="407.2" y="232.8" text-anchor="middle">160</text><line class="fc-tick" x1="399.0" y1="156.0" x2="389.0" y2="156.0"/><text class="tick" x="377.0" y="160.0" text-anchor="middle">192</text><line class="fc-tick" x1="422.7" y1="98.7" x2="415.7" y2="91.7"/><text class="tick" x="407.2" y="87.2" text-anchor="middle">224</text><path class="fc-window" d="M477.9,70.0 A86,86 0 0 1 486.3,241.8"/><path class="fc-ahead" d="M475.8,70.1 A86,86 0 0 1 484.2,70.1"/><line class="fc-tick" x1="475.8" y1="70.1" x2="431.8" y2="39.6"/><circle class="ink-dot" cx="475.8" cy="70.1" r="5.5"><title>old PCA = 254</title></circle><text class="coord halo" x="431.8" y="43.6" text-anchor="middle">old PCA 254</text><line class="fc-tick" x1="484.2" y1="70.1" x2="528.2" y2="39.6"/><circle class="s3-dot" cx="484.2" cy="70.1" r="5.5"><title>new PCA = 2</title></circle><text class="coord halo" x="528.2" y="43.6" text-anchor="middle">new PCA 2</text><text class="st-text" x="480" y="157" text-anchor="middle">4 credits back</text><text class="tick" x="480" y="176" text-anchor="middle">then PCR = 1</text></svg>

    <span class="viz-legend"><span><i class="ink"></i>הערך הישן</span><span><i class="s3"></i>הערך שהגיע, או החדש</span><span><i class="fc-ahead"></i>המרחק קדימה: פקטות שאבדו, והקרדיטים שחוזרים</span><span><i class="fc-window"></i>חלון של 127 צעדים קדימה</span></span>

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏Sync יוצא:** ה-Egress שם בפקט את PCC של **הרגע**: פקטות ששודרו, לא פקטות שמחכות
       בתור לשידור.
    2. **בדיקה:** ה-Ingress מאמת שה-Sync שייך לנתיב (Hop ID).
    3. **כמה אבדו:** \( missing = (PCC_{sync} - PCR) \bmod 256 \), עם PCR הישן.
    4. **הקרדיטים חוזרים:** \( PCA = (PCA + missing) \bmod 256 \).
    5. **יישור:** \( PCR = PCC_{sync} \). ה-Credit Grant הבא נושא את PCA המתוקן, ושני הצדדים
       מסכימים.

    </div>

    #### הקוד { .sol-code }

    שתי מחלקות יורשות שמוסיפות פונקציה אחת כל אחת; הקוד של סעיף א נשאר כפי שהוא.

    === "SystemVerilog"
        ```systemverilog title="egress_sync_model, ingress_sync_model" linenums="1" hl_lines="11 28 29 30"
        // Part b adds the Path Credit Sync to both sides; everything else is inherited.
        class egress_sync_model extends egress_credit_model;
          function new(hop_id_t hop_id);
            super.new(hop_id);
          endfunction

          // Carries PCC as it is now: packets already on the link, not packets waiting to go.
          function credit_sync_packet build_credit_sync();
            credit_sync_packet sync = new();
            sync.hop_id = hop_id;
            sync.pcc    = pcc;                                                 // (1)!
            return sync;
          endfunction
        endclass

        class ingress_sync_model extends ingress_credit_model;
          function new(hop_id_t hop_id, int unsigned initial_credits);
            super.new(hop_id, initial_credits);
          endfunction

          // Packets the Egress transmitted and we never received: their credits come back.
          function void consume_credit_sync(credit_sync_packet sync);
            credit_t missing;
            if (sync == null || sync.hop_id != hop_id) begin
              $error("hop %0d: Credit Sync of another Path, or null", hop_id);
              return;
            end
            missing = forward_distance(pcr, sync.pcc);                         // (2)!
            pca     = credit_t'(pca + missing);                                // (3)!
            pcr     = sync.pcc;                                                // (4)!
          endfunction
        endclass
        ```

        1. ‏PCC מונה רק פקטות ששודרו בפועל, ולכן הערך ב-Sync כולל בדיוק את הפקטות שהגיעו
           לפניו או אבדו. פקטה שמחכה לשידור הייתה נספרת כ"אבדה" ומחזירה קרדיט לתא שהיא
           עוד תתפוס.
        2. עם PCR **הישן**: המרחק קדימה מ-PCR אל PCC שהגיע הוא מספר הפקטות שלא התקבלו, גם
           כשהמונים גלשו (‏\( (1 - 253) \bmod 256 = 4 \)).
        3. התאים של הפקטות האלה מעולם לא נתפסו, ולכן הקרדיטים שלהן חוזרים להקצאה.
        4. רק עכשיו PCR מיושר ל-PCC. ה-Sync הבא ימדוד אובדנים מנקודה זו והלאה.

    === "Python"
        ```python title="EgressSyncModel, IngressSyncModel" linenums="1" hl_lines="6 15 16 17"
        class EgressSyncModel(EgressCreditModel):
            """Part b adds the Path Credit Sync to both sides; everything else is inherited."""

            def build_credit_sync(self) -> CreditSync:
                """Carries PCC as it is now: packets already on the link, not packets waiting to go."""
                return CreditSync(self.hop_id, self.pcc)                     # (1)!


        class IngressSyncModel(IngressCreditModel):

            def consume_credit_sync(self, sync: CreditSync) -> None:
                """Packets the Egress transmitted and we never received: their credits come back."""
                check_hop(self.hop_id, sync)
                missing = forward_distance(self.pcr, sync.pcc)               # (2)!
                self.pca = (self.pca + missing) % MOD                        # (3)!
                self.pcr = sync.pcc                                          # (4)!
        ```

        1. ‏PCC מונה רק פקטות ששודרו בפועל, ולכן הערך ב-Sync כולל בדיוק את הפקטות שהגיעו
           לפניו או אבדו. פקטה שמחכה לשידור הייתה נספרת כ"אבדה" ומחזירה קרדיט לתא שהיא
           עוד תתפוס.
        2. עם PCR **הישן**: המרחק קדימה מ-PCR אל PCC שהגיע הוא מספר הפקטות שלא התקבלו, גם
           כשהמונים גלשו (‏\( (1 - 253) \bmod 256 = 4 \)).
        3. התאים של הפקטות האלה מעולם לא נתפסו, ולכן הקרדיטים שלהן חוזרים להקצאה.
        4. רק עכשיו PCR מיושר ל-PCC. ה-Sync הבא ימדוד אובדנים מנקודה זו והלאה.

    #### למה זה נכון { .sol-proof }

    **הדוגמה, צעד אחרי צעד.** פקטה 2 אובדת; אחרי ההוצאות וה-Grant רואים את הדליפה, ואחרי
    ה-Sync וה-Grant הבא שני הצדדים מסכימים שוב:

    <div class="stepper" role="group" aria-label="אובדן פקטה, צעד אחרי צעד: הדליפה, ה-Credit Sync והתיקון" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 0: הקמת הנתיב; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fcb0-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb0-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb0-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 0 · Path setup</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">0</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">0</text><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">0</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">0</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">5</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-slot" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">0 of 5 slots used</text><text class="coord" x="320" y="118" text-anchor="middle" font-weight="700">Path setup</text></svg><figcaption>צעד 0: הקמת הנתיב. ה-Egress מתחיל מ-PCC = 0 ו-PCL = 0; ה-Ingress מ-PCR = 0 ו-PCA = 5, כמספר התאים ב-buffer. המרחק מ-PCC ל-PCL הוא 0, ולכן עדיין אסור לשדר.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 1: ‏Credit Grant של 5; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fcb1-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb1-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb1-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 1 · Credit Grant (5)</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">0</text><rect class="st-cur" x="180" y="97" width="56" height="24" rx="4"/><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">5</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">0</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">5</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-slot" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">0 of 5 slots used</text><line class="fc-grant" x1="388" y1="118" x2="256" y2="118" marker-end="url(#fcb1-s3)"/><text class="tick" x="320" y="104" text-anchor="middle">Credit Grant (5)</text><text class="tick" x="320" y="138" text-anchor="middle">credits = PCA</text><text class="tick" x="320" y="154" text-anchor="middle">→ PCL</text></svg><figcaption>צעד 1: ה-Ingress שולח Credit Grant עם PCA = 5, וה-Egress מחליף: PCL = 5. המרחק מ-PCC = 0 הוא 5 קרדיטים. בדיוק מספר התאים הפנויים, 5.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 2: פקטה 1 שודרה והתקבלה; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fcb2-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb2-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb2-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 2 · packet 1</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><rect class="st-cur" x="180" y="71" width="56" height="24" rx="4"/><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">1</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">4</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><rect class="st-cur" x="558" y="71" width="56" height="24" rx="4"/><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">1</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">5</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">1 of 5 slots used</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#fcb2-s1)"/><text class="tick" x="320" y="104" text-anchor="middle">packet 1</text><text class="tick" x="320" y="138" text-anchor="middle">PCC + 1, PCR + 1</text></svg><figcaption>צעד 2: פקטה 1 שודרה והתקבלה. ‏PCC = 1, ‏PCR = 1, התפוסה 1. נשארו 4 קרדיטים.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 3: פקטה 2 שודרה ואבדה; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fcb3-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb3-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb3-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 3 · packet 2</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><rect class="st-cur" x="180" y="71" width="56" height="24" rx="4"/><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">2</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">3</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">1</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">5</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">1 of 5 slots used</text><line class="fc-drop" x1="252" y1="118" x2="308" y2="118"/><text class="cs-no" x="320" y="123" text-anchor="middle">✕</text><text class="tick" x="320" y="104" text-anchor="middle">packet 2 lost</text><text class="tick" x="320" y="138" text-anchor="middle">PCC + 1;</text><text class="tick" x="320" y="154" text-anchor="middle">Ingress: no change</text></svg><figcaption>צעד 3: פקטה 2 שודרה ואבדה. ה-Egress צרך קרדיט, ‏PCC = 2, אבל ה-Ingress לא ראה את הפקטה: ‏PCR נשאר 1, ‏PCA נשאר 5 והתפוסה 1. הקרדיט הזה לא יחזור מעצמו.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 4: פקטה 3 שודרה והתקבלה; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fcb4-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb4-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb4-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 4 · packet 3</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><rect class="st-cur" x="180" y="71" width="56" height="24" rx="4"/><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">3</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">2</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><rect class="st-cur" x="558" y="71" width="56" height="24" rx="4"/><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">2</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">5</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-full" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">2 of 5 slots used</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#fcb4-s1)"/><text class="tick" x="320" y="104" text-anchor="middle">packet 3</text><text class="tick" x="320" y="138" text-anchor="middle">PCC + 1, PCR + 1</text></svg><figcaption>צעד 4: פקטה 3 שודרה והתקבלה. ‏PCC = 3, ‏PCR = 2, התפוסה 2. נשארו 2 קרדיטים.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 5: פקטה יצאה מה-buffer; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fcb5-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb5-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb5-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 5 · dequeue</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">3</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">2</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">2</text><rect class="st-cur" x="558" y="97" width="56" height="24" rx="4"/><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">6</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-full" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">1 of 5 slots used</text><text class="coord" x="320" y="112" text-anchor="middle" font-weight="700">dequeue</text><text class="tick" x="320" y="138" text-anchor="middle">one slot freed:</text><text class="tick" x="320" y="154" text-anchor="middle">PCA + 1</text></svg><figcaption>צעד 5: פקטה יוצאת מה-buffer. התפוסה 1, ‏PCA = 6. ‏PCR נשאר 2: הוא סופר קבלות, לא תפוסה.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 6: פקטה יצאה מה-buffer; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fcb6-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb6-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb6-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 6 · dequeue</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">3</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">5</text><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">2</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">2</text><rect class="st-cur" x="558" y="97" width="56" height="24" rx="4"/><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">7</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-slot" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">0 of 5 slots used</text><text class="coord" x="320" y="112" text-anchor="middle" font-weight="700">dequeue</text><text class="tick" x="320" y="138" text-anchor="middle">one slot freed:</text><text class="tick" x="320" y="154" text-anchor="middle">PCA + 1</text></svg><figcaption>צעד 6: פקטה יוצאת מה-buffer. התפוסה 0, ‏PCA = 7. ‏PCR נשאר 2: הוא סופר קבלות, לא תפוסה.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 7: ‏Credit Grant של 7; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fcb7-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb7-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb7-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 7 · Credit Grant (7)</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">3</text><rect class="st-cur" x="180" y="97" width="56" height="24" rx="4"/><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">7</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">4</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">2</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">7</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-slot" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">0 of 5 slots used</text><line class="fc-grant" x1="388" y1="118" x2="256" y2="118" marker-end="url(#fcb7-s3)"/><text class="tick" x="320" y="104" text-anchor="middle">Credit Grant (7)</text><text class="tick" x="320" y="138" text-anchor="middle">credits = PCA</text><text class="tick" x="320" y="154" text-anchor="middle">→ PCL</text></svg><figcaption>צעד 7: ה-Ingress שולח Credit Grant עם PCA = 7, וה-Egress מחליף: PCL = 7. המרחק מ-PCC = 3 הוא 4 קרדיטים. אבל ב-buffer יש 5 תאים פנויים: קרדיט אחד דלף עם הפקטה שאבדה.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 8: ‏Credit Sync עם PCC = 3; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fcb8-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb8-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb8-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 8 · Credit Sync (PCC = 3)</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">3</text><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">7</text><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">4</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><rect class="st-cur" x="558" y="71" width="56" height="24" rx="4"/><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">3</text><rect class="st-cur" x="558" y="97" width="56" height="24" rx="4"/><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">8</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-slot" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">0 of 5 slots used</text><line class="fc-sync" x1="252" y1="118" x2="384" y2="118" marker-end="url(#fcb8-ink)"/><text class="tick" x="320" y="104" text-anchor="middle">Credit Sync (PCC = 3)</text><text class="tick" x="320" y="138" text-anchor="middle">PCA + missing,</text><text class="tick" x="320" y="154" text-anchor="middle">then PCR = PCC</text></svg><figcaption>צעד 8: ה-Egress שולח Credit Sync עם PCC = 3. ה-Ingress מודד מ-PCR = 2 עד 3: המרחק 1, פקטה אחת אבדה. ‏PCA = 7 + 1 = 8, ואז PCR = 3.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" aria-label="צעד 9: ‏Credit Grant של 8; המונים של שני הצדדים ותפוסת ה-buffer"><defs><marker id="fcb9-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb9-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="fcb9-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 9 · Credit Grant (8)</text><rect class="cs-blk" x="16" y="36" width="230" height="166" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">HOST · Egress Adapter</text><text class="tick" x="30" y="88">PCC</text><text class="st-text" x="230" y="88" text-anchor="end">3</text><rect class="st-cur" x="180" y="97" width="56" height="24" rx="4"/><text class="tick" x="30" y="114">PCL</text><text class="st-text" x="230" y="114" text-anchor="end">8</text><rect class="st-cur" x="180" y="123" width="56" height="24" rx="4"/><text class="tick" x="30" y="140">credits</text><text class="st-text" x="230" y="140" text-anchor="end">5</text><rect class="cs-blk" x="394" y="36" width="230" height="166" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">DEVICE · Ingress Adapter</text><text class="tick" x="408" y="88">PCR</text><text class="st-text" x="608" y="88" text-anchor="end">3</text><text class="tick" x="408" y="114">PCA</text><text class="st-text" x="608" y="114" text-anchor="end">8</text><text class="tick" x="408" y="172">RX buffer</text><rect class="fc-slot" x="486" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="513" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="540" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="567" y="156" width="22" height="22" rx="3"/><rect class="fc-slot" x="594" y="156" width="22" height="22" rx="3"/><text class="tick" x="608" y="196" text-anchor="end">0 of 5 slots used</text><line class="fc-grant" x1="388" y1="118" x2="256" y2="118" marker-end="url(#fcb9-s3)"/><text class="tick" x="320" y="104" text-anchor="middle">Credit Grant (8)</text><text class="tick" x="320" y="138" text-anchor="middle">credits = PCA</text><text class="tick" x="320" y="154" text-anchor="middle">→ PCL</text></svg><figcaption>צעד 9: ה-Ingress שולח Credit Grant עם PCA = 8, וה-Egress מחליף: PCL = 8. המרחק מ-PCC = 3 הוא 5 קרדיטים. בדיוק מספר התאים הפנויים, 5.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="10"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <span class="viz-legend"><span><i class="fc-full"></i>תא תפוס ב-buffer</span><span><i class="fc-slot"></i>תא פנוי</span><span><i class="st-cur"></i>ערך שהשתנה בצעד הזה</span><span><i class="fc-pkt"></i>‏Tunneled Packet, מה-HOST ל-DEVICE</span><span><i class="fc-grant"></i>‏Credit Grant, מה-DEVICE ל-HOST</span><span><i class="fc-sync"></i>‏Path Credit Sync</span><span><i class="fc-drop"></i>פקטה שאבדה בדרך</span></span>

    | צעד | אירוע | ‏PCC | ‏PCL | ‏PCR | ‏PCA | תפוסה | קרדיטים |
    |---|---|---|---|---|---|---|---|
    | 0 | הקמת הנתיב | 0 | 0 | 0 | 5 | 0 | 0 |
    | 1 | ‏Credit Grant של 5 | 0 | 5 | 0 | 5 | 0 | 5 |
    | 2 | פקטה 1 שודרה והתקבלה | 1 | 5 | 1 | 5 | 1 | 4 |
    | 3 | פקטה 2 שודרה ואבדה | 2 | 5 | 1 | 5 | 1 | 3 |
    | 4 | פקטה 3 שודרה והתקבלה | 3 | 5 | 2 | 5 | 2 | 2 |
    | 5 | פקטה יצאה מה-buffer | 3 | 5 | 2 | 6 | 1 | 2 |
    | 6 | פקטה יצאה מה-buffer | 3 | 5 | 2 | 7 | 0 | 2 |
    | 7 | ‏Credit Grant של 7 | 3 | 7 | 2 | 7 | 0 | 4 |
    | 8 | ‏Credit Sync עם PCC = 3 | 3 | 7 | 3 | 8 | 0 | 4 |
    | 9 | ‏Credit Grant של 8 | 3 | 8 | 3 | 8 | 0 | 5 |
        
    **החשבון הכללי.** בסימונים של סעיף א, עם \( L \) פקטות שאבדו: \( T = R + L \) ברגע
    שאין פקטות בדרך. בלי Sync, ‏\( PCA = N + D \) ו-\( PCL - PCC = N + D' - T \le N - (R - D) - L \):
    התאים הפנויים פחות \( L \). כל אובדן מקטין את החלון לתמיד, ואחרי \( N \) אובדנים אין
    קרדיטים. ב-Sync, הקישור שומר על סדר, ולכן כל פקטה ששודרה לפני ה-Sync כבר התקבלה או
    אבדה: ‏\( PCC_{sync} - PCR = T - R = L' \), האובדנים מאז היישור הקודם, והמרחק קדימה
    מחזיר אותו כל עוד \( L' \le 127 \) (אובדנים רבים יותר בין שני Sync-ים אינם אפשריים
    בנתיב תקין, כי \( L' \le N \le 127 \)). אחרי העדכון \( PCA = N + D + L \): תא פנוי על כל
    פקטה שיצאה **או אבדה**, וה-Grant הבא נותן \( PCL - PCC = N - (R - D) \): בדיוק התאים
    הפנויים. ‏\( PCR = PCC_{sync} \) מבטיח שה-Sync הבא ימדוד רק אובדנים חדשים. ה-test
    מריץ תעבורה אקראית עם אובדנים דרך מאות גלישות ובודק את שתי הטענות: אין גלישת buffer
    אף פעם, ואחרי Sync ו-Grant הקרדיטים שווים לתאים הפנויים.

    **לנסות בעצמכם.** בתיבה הבאה ארבעת המונים הם מחוגים על מעגל אחד של 256 ערכים: הקשת
    מ-PCC ל-PCL היא הקרדיטים, והקשת מ-PCR ל-PCA היא התאים הפנויים כפי שה-Ingress סופר
    אותם. שתי הדוגמאות שלמעלה הן תסריטים, ולצדן אירועים חופשיים: Grant, שידור, פקטה
    שהתקבלה או אבדה, הוצאה מה-buffer ו-Sync. "להתחיל מ-250" מראה את הגלישה.

    <div class="explorer" data-kind="credits"></div>

    #### סיבוכיות { .sol-cost }

    עדיין \( O(1) \) לכל פעולה, ושני שדות נוספים בפקטים. ‏Sync תקופתי עולה פקט אחד; בלי
    אובדנים הוא לא משנה דבר (המרחק 0), ולכן אפשר לשלוח אותו תמיד.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: Credit Grant כתוספת"
    ‏`PCL += grant.credits` נראה טבעי ("קיבלתי עוד קרדיטים"), אבל ה-Grant נושא את PCA
    המצטבר. Grant חוזר עם אותו ערך היה מכפיל את הקרדיטים, וה-Egress היה שולח ל-buffer
    מלא. ‏PCL תמיד **מוחלף**. באותו אופן, ה-Grant לא נושא "כמה תאים פנויים" ולא "כמה
    התפנו מאז": ערך רגעי לא שורד אובדן של Grant, ערך מצטבר כן.

??? trap "מלכודת: PCR כתפוסה"
    ‏PCR לא יורד ב-dequeue ו-PCA לא עולה בקבלה. ‏PCR סופר כניסות ל-buffer, ‏PCA סופר
    הקצאות, והתפוסה היא משתנה נפרד. מי שמוריד את PCR ב-dequeue שובר את ההשוואה ל-PCC
    ב-Sync, ומי שמעלה את PCA בקבלה מחלק קרדיט על תא **תפוס**.

??? trap "מלכודת: PCL > PCC"
    הבדיקה הטבעית נכשלת בגלישה: ‏PCL = 2 ו-PCC = 254 הם ארבעה קרדיטים, ו-`2 > 254` שקר.
    הנתיב היה נתקע אחת ל-256 פקטות. המרחק קדימה \( (PCL - PCC) \bmod 256 \), עם ההפרש
    בטיפוס רחב וחתום, מכסה את שני המקרים של המפרט בתנאי אחד.

??? trap "מלכודת: הסדר ב-Credit Sync"
    ‏`pcr = sync.pcc` ואז `pca += ...` נותן תמיד תוספת 0: המרחק נמדד מ-PCR שכבר יושר.
    התיקון חייב להשתמש ב-PCR הישן. טעות שכנה: לאפס את המונים ב-Sync, במקום לתקן אותם.
    ‏Sync הוא יישור, לא אתחול.

??? trap "מלכודת: פקטה בתור נספרת ב-PCC"
    ‏PCC (וערך ה-Sync) סופרים פקטות ש**שודרו**. מי שמעלה את PCC כשהפקטה נכנסת לתור
    השידור גורם ל-Sync לדווח על פקטה שעוד לא יצאה; ה-Ingress יחשיב אותה כאבודה ויחזיר
    קרדיט לתא שהיא עוד תתפוס, וה-buffer עלול לעלות על גדותיו.

??? followup "שאלות המשך"
    - **למה 127 ולא 255?** המרחק על המעגל אינו יכול להבדיל בין "127 קדימה" ל"129 אחורה"
      בלי מידע נוסף; המפרט בוחר חלון של חצי מעגל, ולכן נתיב מחזיק לכל היותר 127 קרדיטים
      פתוחים. מה היה קורה עם buffer של 200 תאים ו-Grant ראשון של 200?
    - **‏Credit Grant שאבד:** מה קורה? כלום לאורך זמן: ה-Grant הבא נושא ערך מצטבר גדול
      יותר, וה-Egress רק ראה פחות קרדיטים בינתיים. ו-Sync שאבד?
    - **מתי שולחים Sync?** באיזה תדירות, ומה המחיר של Sync שמגיע בעוד פקטות בדרך, אם
      הקישור **לא** היה שומר על סדר?
    - **‏Shared Credits:** במפרט יש גם ארבעה מונים משותפים לכל הנתיבים של הקישור (SCC,
      ‏SCL, ‏SCR, ‏SCA). איך היה נראה כלל השידור כשמותר להשתמש בשני הסוגים?
    - **מודל ייחוס כבודק:** איך מחברים את שתי המחלקות ל-scoreboard של DUT אמיתי: מי קורא
      ל-`on_packet_transmitted`, מי מחליט על `accepted`, ומה המודל צריך לדווח כשה-DUT
      שולח פקטה בלי קרדיט?
    - **‏HIA E2E credits:** פרק 12 של המפרט מגדיר קרדיטים של descriptors בין ה-Host
      Interface Adapter לתוכנה. למה אסור לערבב אותם עם קרדיטי הנתיב של פרק 5?
