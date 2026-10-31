---
id: 25
title: מודל ייחוס ל-Ack/Nak של PCIe – Sequence Number, ‏Retry Buffer ו-Replay
level: senior
difficulty: medium
kind: dv
tags: [protocols, pcie, python, systemverilog]
source: ""
added: 2026-10-19
---

## השאלה

שכבת ה-Data Link של PCIe מבטיחה שכל TLP יגיע לצד השני **שלם ובסדר**. המנגנון : המשדר
(כאן ה-Root Complex, ‏RC) מצמיד לכל TLP מספר רץ של 12 ביט (Sequence Number) ושומר עותק
ב-**Retry Buffer** עד שהצד השני מאשר אותו. המקבל (ה-Endpoint, ‏EP) בודק את ה-LCRC ואת
המספר, מוסר ל-Transaction Layer רק את ה-TLP שהוא מצפה לו, ומחזיר **Ack** (הכול עד מספר
מסוים התקבל) או **Nak** (הכול עד מספר מסוים התקבל, ומשהו אחריו לא). על Nak המשדר משדר
מחדש (Replay) את כל מה שעוד לא אושר, מהעותק שב-Retry Buffer. כתבו **מודל ייחוס**
(reference model) של המנגנון, מהסוג שמחברים ל-scoreboard : הוא רואה את הפקטים שה-DUT רואה
ואומר מה היה צריך להישלח, להימסר ולהתעלם.

המנגנון סימטרי : כל פורט הוא גם משדר וגם מקבל. כאן ממדלים כיוון אחד, TLPs מה-RC אל ה-EP
ו-Ack/Nak חזרה, ואותן מחלקות משרתות את הכיוון ההפוך.

| מצב | מי מחזיק | ערך התחלתי | משמעות |
|---|---|---|---|
| ‏NEXT_TRANSMIT_SEQ | ‏RC (משדר) | ‏0 | המספר שיקבל ה-TLP החדש הבא; עולה באחד אחרי כל שידור חדש, מודולו 4096 |
| ‏ACKD_SEQ | ‏RC (משדר) | ‏4095 | המספר האחרון שאושר ב-Ack או ב-Nak תקין; ‏4095 הוא "לפני 0" |
| ‏Retry Buffer | ‏RC (משדר) | ריק | העותקים של כל ה-TLPs ששודרו ועוד לא אושרו, בסדר השידור |
| ‏NEXT_RCV_SEQ | ‏EP (מקבל) | ‏0 | המספר שהמקבל מצפה לו ב-TLP הבא |
| ‏NAK_SCHEDULED | ‏EP (מקבל) | ‏0 | נשלח כבר Nak על הפער הנוכחי; לא שולחים עוד אחד עד שהפער נסגר |

שני פקטי DLLP חוזרים מה-EP אל ה-RC, ושניהם **מצטברים** : ‏Ack עם המספר 5 אומר "כל ה-TLPs
עד 5 ועד בכלל התקבלו", לא "התקבל 5". ‏Nak עם 4094 אומר "הכול עד 4094 התקבל; מה שאחריו לא,
שדרו שוב". לכן Nak תקין עושה שני דברים : מוחק מה-Retry Buffer את מה שאושר, ואז משדר מחדש את
כל השאר, מהישן לחדש, **עם המספרים המקוריים**.

הפשטות : אין חישוב LCRC אמיתי, לכל פקט יש שדה `crc_ok` שאומר אם הבדיקה הייתה עוברת; אין
טיימרים במודל (הסביבה קוראת ל-`flush_ack()` ול-`on_replay_timeout()` כשהיא מחליטה); אין
‏Flow Control, ‏Nullified TLPs או LTSSM. המודל מוציא פקטים לתור שידור (`tx_tlps`, ‏`tx_dllps`)
שהסביבה מרוקנת אל הקישור. מחלקות הפקטים נתונות :

=== "Python"
    ```python title="given classes"
    import random
    from dataclasses import dataclass, replace
    from enum import Enum

    SEQ_MOD = 4096                   # Sequence Numbers are 12 bits wide and wrap


    class DllpKind(Enum):
        ACK = "ACK"
        NAK = "NAK"


    @dataclass
    class Tlp:
        payload: int
        seq: int = 0
        crc_ok: bool = True          # stands in for the LCRC check
        is_replay: bool = False


    @dataclass
    class Dllp:
        kind: DllpKind
        seq: int                     # AckNak_Seq_Num: everything through seq arrived
        crc_ok: bool = True
    ```

=== "SystemVerilog"
    ```systemverilog title="given classes"
    typedef bit [11:0] seq_t;                  // Sequence Numbers are 12 bits wide and wrap
    typedef enum bit { DLLP_ACK, DLLP_NAK } dllp_kind_e;

    class pcie_tlp;
      bit [31:0] payload;
      seq_t      seq;
      bit        crc_ok;                       // stands in for the LCRC check
      bit        is_replay;
      function new(bit [31:0] payload = 0, seq_t seq = 0, bit crc_ok = 1, bit is_replay = 0);
        this.payload   = payload;
        this.seq       = seq;
        this.crc_ok    = crc_ok;
        this.is_replay = is_replay;
      endfunction
      function pcie_tlp clone();
        pcie_tlp c = new(payload, seq, crc_ok, is_replay);
        return c;
      endfunction
    endclass

    class pcie_dllp;
      dllp_kind_e kind;
      seq_t       seq;                         // AckNak_Seq_Num: everything through seq arrived
      bit         crc_ok;
      function new(dllp_kind_e kind = DLLP_ACK, seq_t seq = 12'hFFF, bit crc_ok = 1);
        this.kind   = kind;
        this.seq    = seq;
        this.crc_ok = crc_ok;
      endfunction
    endclass
    ```

??? interviewer "מה המראיין בודק"
    - **שני צדדים, שני מצבים :** האם המועמד מפריד בין מצב המשדר (מספור, ‏Retry Buffer) למצב
      המקבל (ציפייה, ‏Nak), ומבין שכל צד לומד על השני רק מהפקטים.
    - **מצטבר, לא בודד :** האם Ack/Nak מוחק **את כל** מה שעד המספר, ולא רק רשומה אחת.
    - **גלישה של 12 ביט :** האם הטיפול ב-Retry Buffer נכון כשהמספרים עוברים מ-4095 ל-0, בלי
      השוואות מספריות רגילות.
    - **מה לא נוגעים בו :** האם פקט פגום, כפול או "מהעתיד" משאיר את המצב כפי שהוא, ואיך
      מונעים סופת Nak-ים.
    - **העותק הנכון :** האם ה-Retry Buffer שומר עותק נקי שהקישור לא יכול להשחית.

---

### סעיף א – הזרימה התקינה : מספור, Ack מצטבר וגלישה

בסעיף זה הקישור מושלם : כל TLP מגיע שלם ובסדר, וכל DLLP מגיע שלם. ממשו שתי מחלקות :

- **משדר** (‏`dll_transmitter`) : ‏`send_tlp(tlp)` מקבל TLP מה-Transaction Layer, מצמיד לו
  את NEXT_TRANSMIT_SEQ, שומר עותק ב-Retry Buffer ומעמיד **עותק נפרד** בתור השידור;
  ‏`receive_dllp(dllp)` מקבל Ack ומוחק מה-Retry Buffer את כל הרשומות עד המספר שלו ועד בכלל;
  ‏`find_in_retry_buffer(seq)` מוצא את מקום הרשומה.
- **מקבל** (‏`dll_receiver`) : ‏`receive_tlp(tlp)` מוסר ל-Transaction Layer את ה-TLP שהמספר
  שלו הוא NEXT_RCV_SEQ ומקדם את הציפייה. ה-Ack מצטבר : המקבל לא מאשר כל TLP בנפרד, אלא
  מגריל **סף** בין 1 ל-`MAX_ACK_COALESCE` (‏4), וכשמספר ה-TLPs שהתקבלו מאז ה-Ack הקודם מגיע
  לסף הוא שולח Ack עם NEXT_RCV_SEQ − 1 ומגריל סף חדש. ‏`flush_ack()` נקראת מהסביבה (במקום
  ה-AckNak Latency Timer) ושולחת Ack על מה שממתין.

הקישור פעיל כבר זמן מה : ה-RC עומד על NEXT_TRANSMIT_SEQ = 4094 (‏ACKD_SEQ = 4093) וה-EP על
‏NEXT_RCV_SEQ = 4094. ה-RC שולח חמישה TLPs, וה-EP מגריל את הספים 2, 3 ואז 1. אילו Ack-ים
יישלחו, ומה יהיה ב-Retry Buffer אחרי כל אחד? למה אסור למחוק מה-Retry Buffer עם השוואה כמו
‏`entry.seq <= ack.seq`?

??? tip "רמז 1"
    ‏Ack עם המספר \( s \) מוחק **קידומת** של ה-Retry Buffer : מהרשומה הראשונה ועד הרשומה
    שהמספר שלה \( s \). מה מגדיר את הקידומת, המספר או המקום בתור?

??? tip "רמז 2"
    ב-Retry Buffer הרשומות תמיד בסדר השידור, ולכן אפשר **לחפש** את \( s \) ולמחוק עד
    האינדקס שנמצא. כך 4094, 4095, 0, 1 נמחקים יחד על Ack 1, בלי שום חשבון מודולו.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        חמשת ה-TLPs מקבלים 4094, 4095, 0, 1, 2 ו-NEXT_TRANSMIT_SEQ מגיע ל-3. עם הספים 2,
        3 ו-1 ה-EP שולח Ack 4095 (אחרי שניים), ‏Ack 2 (אחרי שלושה נוספים) ואז ה-Ack הבא
        יבוא אחרי TLP אחד. ‏Ack 4095 מוחק את \( [4094, 4095] \) ומשאיר \( [0, 1, 2] \);
        ‏Ack 2 מרוקן את ה-Retry Buffer, ‏ACKD_SEQ = 2. ההשוואה `entry.seq <= ack.seq` נכשלת
        בגלישה : על Ack 1 היא הייתה מוחקת את 0 ואת 1 ומשאירה את 4094 ו-4095 לנצח. מוחקים
        לפי **מקום** בתור, אחרי חיפוש המספר.

    <!-- cost: שידור \( O(1) \) | אישור \( O(k) \) -->

    #### הרעיון { .sol-idea }

    **שלושה דברים זזים.** המספר הבא לשידור עולה עם כל TLP חדש; ה-Retry Buffer מחזיק עותק
    של כל מה ששודר ועוד לא אושר, בסדר השידור; והציפייה של המקבל עולה עם כל TLP שנמסר. ‏
    Ack סוגר את המעגל : המספר שבו הוא "האחרון שהתקבל", ולכן המשדר מוחק מה-Retry Buffer את
    הקידומת שנגמרת בו. שימו לב למה שהמודל **מוציא** החוצה : עותק של ה-TLP, לא הרשומה
    עצמה. הקישור (ובסעיף ב, הסביבה שמזריקה שגיאות) יכול להשחית את העותק, והרשומה נשארת
    נקייה ל-Replay.

    ```mermaid
    flowchart LR
        TL1[Transaction Layer TX] -->|new TLP| TX[dll_transmitter]
        TX -->|copy, seq = NEXT_TRANSMIT_SEQ| RB[(Retry Buffer)]
        TX -->|another copy| LINK[link: tx_tlps]
        LINK --> RX[dll_receiver]
        RX -->|seq == NEXT_RCV_SEQ| TL2[Transaction Layer RX]
        RX -->|Ack after a random 1..4 TLPs| ACK[link: tx_dllps]
        ACK --> TX
        TX -->|purge through the Ack's seq| RB
    ```

    **‏Ack מצטבר ואקראי.** המקבל סופר כמה TLPs נמסרו מאז ה-Ack האחרון; כשהמספר מגיע לסף
    שהוגרל הוא שולח Ack אחד עם NEXT_RCV_SEQ − 1 ומגריל סף חדש. המשדר לא יודע ולא צריך לדעת
    כמה TLPs "מכוסים" ב-Ack : הוא מוחק עד המספר, וזהו. זה בדיוק מה שהופך את הפרוטוקול
    לעמיד ל-Ack שאבד (סעיף ב) : ה-Ack הבא מכסה גם אותו.

    **גלישה.** המספרים הם 12 ביט ו-4095 נעקב ב-0. אם מוחקים "כל רשומה שהמספר שלה קטן או
    שווה ל-Ack", אז Ack 1 מוחק את 0 ו-1 ומשאיר את 4094 ו-4095, ש"גדולים" ממנו. ה-Retry
    Buffer שומר את סדר השידור, ולכן הדרך הנכונה לא עושה חשבון בכלל : מחפשים את המספר של ה-Ack
    בתור ומוחקים מהראש עד האינדקס שנמצא. גם NEXT_RCV_SEQ − 1 ו-NEXT_TRANSMIT_SEQ + 1
    מחושבים ב-12 ביט, כך שהגלישה חינם.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שידור :** ל-TLP החדש מצמידים את NEXT_TRANSMIT_SEQ, שומרים עותק ב-Retry Buffer, מעמידים
       עותק נוסף בתור השידור, ומקדמים את המונה (מודולו 4096).
    2. **קבלה :** אם המספר הוא NEXT_RCV_SEQ : מוסרים ל-TL, מקדמים את הציפייה, סופרים אחד למי
       שממתין ל-Ack. כשהספירה מגיעה לסף : Ack עם NEXT_RCV_SEQ − 1, איפוס הספירה, סף חדש.
    3. **‏flush_ack :** אם יש TLPs שממתינים ל-Ack, שולחים אותו עכשיו.
    4. **‏Ack במשדר :** מחפשים את המספר ב-Retry Buffer; מוחקים מהראש עד האינדקס ועד בכלל;
       ‏ACKD_SEQ מקבל את המספר.

    </div>

    #### הקוד { .sol-code }

    שתי מחלקות קטנות. הפונקציות שסעיף ב ירחיב (`receive_dllp` ו-`receive_tlp`) מוגדרות
    כ-virtual, ושני צעדי העבודה שלהן (`purge_through` ו-`accept`) נפרדים כדי שסעיף ב יוכל
    להשתמש בהם כפי שהם. ב-Python המקבל מקבל `random.Random`, כדי שבדיקה תוכל לקבע seed.

    === "Python"
        ```python title="DllTransmitter, DllReceiver" linenums="1" hl_lines="17 18 19 30 31 51 64 65 66 67 84"
        class DllTransmitter:
            """The transmit side of a Data Link Layer: numbers the TLPs and keeps every one of
            them until the other side acknowledges it."""

            def __init__(self, start_seq: int = 0):
                self.next_transmit_seq = start_seq % SEQ_MOD      # NEXT_TRANSMIT_SEQ
                self.ackd_seq = (start_seq - 1) % SEQ_MOD         # ACKD_SEQ: 4095 before the first TLP  (1)
                self.retry_buffer: list[Tlp] = []                 # transmitted, not yet acknowledged, in order
                self.tx_tlps: list[Tlp] = []                      # what went to the link, in order
                self.bad_dllp_count = 0
                self.protocol_error_count = 0
                self.replay_count = 0

            def send_tlp(self, tlp: Tlp) -> None:
                """A new TLP from the Transaction Layer: number it, keep a copy, put a copy on the link."""
                stored = replace(tlp, seq=self.next_transmit_seq, crc_ok=True, is_replay=False)
                self.retry_buffer.append(stored)                  # (2)!
                self.tx_tlps.append(replace(stored))
                self.next_transmit_seq = (self.next_transmit_seq + 1) % SEQ_MOD

            def find_in_retry_buffer(self, seq: int) -> int:
                """Position of the entry numbered seq, or -1. A search, so the wrap costs nothing."""
                for i, tlp in enumerate(self.retry_buffer):
                    if tlp.seq == seq:
                        return i
                return -1

            def purge_through(self, index: int, seq: int) -> None:
                """Ack and Nak are cumulative: everything up to and including index goes."""
                del self.retry_buffer[:index + 1]                 # (3)!
                self.ackd_seq = seq

            def receive_dllp(self, dllp: Dllp) -> None:
                """Part a: the link is perfect, so every DLLP is an Ack for an outstanding TLP."""
                index = self.find_in_retry_buffer(dllp.seq)
                if index < 0:
                    raise ValueError(f"Ack {dllp.seq} does not name an outstanding TLP")
                self.purge_through(index, dllp.seq)


        class DllReceiver:
            """The receive side: delivers the TLPs in order and answers with cumulative Acks,
            one Ack per a random number (1..MAX_ACK_COALESCE) of TLPs."""
            MAX_ACK_COALESCE = 4

            def __init__(self, start_seq: int = 0, rng: random.Random | None = None):
                self.rng = rng or random.Random()
                self.next_rcv_seq = start_seq % SEQ_MOD           # NEXT_RCV_SEQ: the number we wait for
                self.nak_scheduled = False                        # NAK_SCHEDULED (part b): one Nak per gap
                self.accepted_since_ack = 0                       # delivered TLPs not yet covered by an Ack
                self.ack_threshold = self.rng.randint(1, self.MAX_ACK_COALESCE)   # (4)!
                self.received_tlps: list[Tlp] = []                # delivered to the Transaction Layer
                self.tx_dllps: list[Dllp] = []                    # Acks and Naks put on the link
                self.bad_tlp_count = 0
                self.duplicate_count = 0

            def last_accepted(self) -> int:
                return (self.next_rcv_seq - 1) % SEQ_MOD          # (5)!

            def accept(self, tlp: Tlp) -> None:
                """The TLP we waited for: deliver it, expect the next one, count it towards an Ack."""
                self.received_tlps.append(tlp)
                self.next_rcv_seq = (self.next_rcv_seq + 1) % SEQ_MOD
                self.nak_scheduled = False
                self.accepted_since_ack += 1
                if self.accepted_since_ack >= self.ack_threshold:
                    self.send_ack()                               # (6)!

            def send_ack(self) -> None:
                """One cumulative Ack for everything delivered so far, then a new random threshold."""
                self.tx_dllps.append(Dllp(DllpKind.ACK, self.last_accepted()))
                self.accepted_since_ack = 0
                self.ack_threshold = self.rng.randint(1, self.MAX_ACK_COALESCE)

            def flush_ack(self) -> None:
                """The environment's Ack timer: acknowledge whatever is pending."""
                if self.accepted_since_ack and not self.nak_scheduled:
                    self.send_ack()

            def receive_tlp(self, tlp: Tlp) -> None:
                """Part a: the link is perfect, so every TLP is the one we wait for."""
                if not tlp.crc_ok or tlp.seq != self.next_rcv_seq:
                    raise ValueError(f"part a assumes an error-free, in-order link (got {tlp})")
                self.accept(tlp)                                  # (7)!
        ```

        1. ‏`(start_seq - 1) % SEQ_MOD` : מ-0 מקבלים 4095, "לפני הראשון", בדיוק הערך ההתחלתי
           שהמפרט דורש ל-ACKD_SEQ.
        2. ‏`replace` יוצר אובייקט חדש : אחד ל-Retry Buffer ואחד לקישור. מי שמכניס את אותו
           אובייקט לשני המקומות ייתן לסביבה (בסעיף ב) להשחית את העותק השמור.
        3. מחיקה לפי **אינדקס** : הקידומת של הרשימה עד הרשומה שנמצאה. גם כשהרשימה היא
           \( [4094, 4095, 0, 1, 2] \) ו-Ack 1 מגיע, נמחקות ארבע הראשונות.
        4. הסף הראשון מוגרל כבר בהקמה, ולכן ה-Ack הראשון יכול לבוא אחרי TLP אחד או אחרי
           ארבעה.
        5. כש-NEXT_RCV_SEQ הוא 0, האחרון שהתקבל הוא 4095.
        6. ה-Ack יוצא **בתוך** הקבלה כשהספירה מגיעה לסף; `flush_ack` משלים מה שנשאר.
        7. בסעיף א כל TLP הוא הצפוי; סעיף ב מחליף את הפונקציה ומשאיר את `accept` כפי שהיא.

    === "SystemVerilog"
        ```systemverilog title="dll_transmitter, dll_receiver" linenums="1" hl_lines="18 19 20 32 33 61 72 73 74 96"
        // The transmit side of a Data Link Layer: numbers the TLPs and keeps every one
        // of them until the other side acknowledges it.
        class dll_transmitter;
          seq_t    next_transmit_seq;        // NEXT_TRANSMIT_SEQ: the number of the next new TLP
          seq_t    ackd_seq;                 // ACKD_SEQ: the last number acknowledged
          pcie_tlp retry_buffer[$];          // transmitted, not yet acknowledged, in order
          pcie_tlp tx_tlps[$];               // what went to the link, in order
          int unsigned bad_dllp_count, protocol_error_count, replay_count;

          function new(seq_t start_seq = 0);
            next_transmit_seq = start_seq;
            ackd_seq          = start_seq - 1;                               // (1)!
          endfunction

          // A new TLP from the Transaction Layer: number it, keep a copy, put a copy on the link.
          function void send_tlp(pcie_tlp tlp);
            pcie_tlp stored = new(tlp.payload, next_transmit_seq, 1, 0);
            retry_buffer.push_back(stored);                                  // (2)!
            tx_tlps.push_back(stored.clone());
            next_transmit_seq++;
          endfunction

          // Position of the entry numbered seq, or -1. A search, so the wrap costs nothing.
          function int find_in_retry_buffer(seq_t seq);
            foreach (retry_buffer[i])
              if (retry_buffer[i].seq == seq) return i;
            return -1;
          endfunction

          // Ack and Nak are cumulative: everything up to and including index goes.
          function void purge_through(int index, seq_t seq);
            repeat (index + 1) void'(retry_buffer.pop_front());
            ackd_seq = seq;
          endfunction

          // Part a: the link is perfect, so every DLLP is an Ack for an outstanding TLP.
          virtual function void receive_dllp(pcie_dllp dllp);
            int index = find_in_retry_buffer(dllp.seq);
            if (index < 0) begin
              $error("Ack %0d does not name an outstanding TLP", dllp.seq);
              return;
            end
            purge_through(index, dllp.seq);                                  // (3)!
          endfunction
        endclass

        // The receive side: delivers the TLPs in order and answers with cumulative Acks,
        // one Ack per a random number (1..MAX_ACK_COALESCE) of TLPs.
        class dll_receiver;
          localparam int MAX_ACK_COALESCE = 4;
          seq_t     next_rcv_seq;            // NEXT_RCV_SEQ: the number we wait for
          bit       nak_scheduled;           // NAK_SCHEDULED (part b): one Nak per gap
          int       accepted_since_ack;      // delivered TLPs not yet covered by an Ack
          int       ack_threshold;           // send the next Ack when the count reaches this
          pcie_tlp  received_tlps[$];        // delivered to the Transaction Layer, in order
          pcie_dllp tx_dllps[$];             // Acks and Naks put on the link, in order
          int unsigned bad_tlp_count, duplicate_count;

          function new(seq_t start_seq = 0);
            next_rcv_seq  = start_seq;
            ack_threshold = $urandom_range(1, MAX_ACK_COALESCE);            // (4)!
          endfunction

          function seq_t last_accepted();
            return next_rcv_seq - 1;                                         // (5)!
          endfunction

          // The TLP we waited for: deliver it, expect the next one, count it towards an Ack.
          function void accept(pcie_tlp tlp);
            received_tlps.push_back(tlp);
            next_rcv_seq++;
            nak_scheduled = 0;
            accepted_since_ack++;
            if (accepted_since_ack >= ack_threshold) send_ack();            // (6)!
          endfunction

          // One cumulative Ack for everything delivered so far, then a new random threshold.
          function void send_ack();
            pcie_dllp ack = new(DLLP_ACK, last_accepted());
            tx_dllps.push_back(ack);
            accepted_since_ack = 0;
            ack_threshold      = $urandom_range(1, MAX_ACK_COALESCE);
          endfunction

          // The environment's Ack timer: acknowledge whatever is pending.
          function void flush_ack();
            if (accepted_since_ack > 0 && !nak_scheduled) send_ack();
          endfunction

          // Part a: the link is perfect, so every TLP is the one we wait for.
          virtual function void receive_tlp(pcie_tlp tlp);
            if (!tlp.crc_ok || tlp.seq != next_rcv_seq) begin
              $error("part a assumes an error-free, in-order link (got seq %0d, crc_ok %0b)", tlp.seq, tlp.crc_ok);
              return;
            end
            accept(tlp);                                                     // (7)!
          endfunction
        endclass
        ```

        1. ‏`start_seq - 1` ב-12 ביט : מ-0 מקבלים 4095, "לפני הראשון", בדיוק הערך ההתחלתי
           שהמפרט דורש ל-ACKD_SEQ.
        2. שתי רשומות נפרדות : אחת ל-Retry Buffer ואחת לקישור. מי שדוחף את אותו אובייקט לשני
           המקומות ייתן לסביבה (בסעיף ב) להשחית את העותק השמור.
        3. מחיקה לפי **אינדקס** : הקידומת של התור עד הרשומה שנמצאה. גם כשהתור הוא
           \( [4094, 4095, 0, 1, 2] \) ו-Ack 1 מגיע, נמחקות ארבע הראשונות.
        4. הסף הראשון מוגרל כבר בהקמה, ולכן ה-Ack הראשון יכול לבוא אחרי TLP אחד או אחרי
           ארבעה.
        5. ‏`next_rcv_seq - 1` ב-12 ביט : כש-NEXT_RCV_SEQ הוא 0, האחרון שהתקבל הוא 4095.
        6. ה-Ack יוצא **בתוך** הקבלה כשהספירה מגיעה לסף; `flush_ack` משלים מה שנשאר.
        7. בסעיף א כל TLP הוא הצפוי; סעיף ב מחליף את הפונקציה ומשאיר את `accept` כפי שהיא.

    #### למה זה נכון { .sol-proof }

    **הדוגמה מהשאלה, צעד אחרי צעד.** הספים של ה-EP הם 2, 3 ואז 1; "pending" הוא כמה TLPs
    נמסרו מאז ה-Ack האחרון, מול הסף :

    <div class="stepper" role="group" aria-label="הזרימה התקינה, צעד אחרי צעד : חמישה TLPs דרך הגלישה ושני Ack-ים מצטברים" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 0 : מצב התחלתי; מצב המשדר והמקבל"><defs><marker id="ana0-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana0-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana0-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 0 · initial state</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">4094</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4093</text><text class="tick" x="30" y="136">retry buffer</text><text class="tick" x="46" y="160">empty</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">4094</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 2</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><text class="tick" x="424" y="184">empty</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><text class="tick" x="320" y="88" text-anchor="middle">initial state</text></svg><figcaption>צעד 0 : הקישור פעיל כבר זמן מה. ה-RC עומד על NEXT_TRANSMIT_SEQ = 4094 ו-ACKD_SEQ = 4093, ה-Retry Buffer ריק; ה-EP מצפה ל-4094 והסף הראשון שהגריל הוא 2.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 1 : ה-RC שולח TLPs 4094, 4095; מצב המשדר והמקבל"><defs><marker id="ana1-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana1-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana1-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 1 · send TLPs 4094, 4095</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><rect class="st-cur" x="166" y="69" width="70" height="24" rx="4"/><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">0</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4093</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4094</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">4095</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">4094</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 2</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><text class="tick" x="424" y="184">empty</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><text class="tick" x="320" y="88" text-anchor="middle">send TLPs</text><text class="tick" x="320" y="104" text-anchor="middle">4094, 4095</text><text class="tick" x="320" y="140" text-anchor="middle">copies kept in the</text><text class="tick" x="320" y="156" text-anchor="middle">retry buffer</text></svg><figcaption>צעד 1 : ה-RC שולח TLPs 4094, 4095. כל אחד מקבל את NEXT_TRANSMIT_SEQ ומקדם אותו; ה-Retry Buffer מחזיק 4094, 4095, ועותקים נפרדים יצאו לקישור. ‏NEXT_TRANSMIT_SEQ = 0.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 2 : ‏TLP 4094 מגיע; מצב המשדר והמקבל"><defs><marker id="ana2-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana2-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana2-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 2 · TLP 4094</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">0</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4093</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4094</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">4095</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><rect class="st-cur" x="544" y="69" width="70" height="24" rx="4"/><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">4095</text><rect class="st-cur" x="544" y="93" width="70" height="24" rx="4"/><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">1 / 2</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#ana2-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">TLP 4094</text><text class="tick" x="320" y="140" text-anchor="middle">accepted</text></svg><figcaption>צעד 2 : ‏TLP 4094 מגיע : המספר הצפוי, נמסר ל-TL. ‏NEXT_RCV_SEQ = 4095, 1 ממתינים ל-Ack מול סף 2.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 3 : ‏TLP 4095 מגיע; מצב המשדר והמקבל"><defs><marker id="ana3-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana3-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana3-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 3 · TLP 4095</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">0</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4093</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4094</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">4095</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><rect class="st-cur" x="544" y="69" width="70" height="24" rx="4"/><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">0</text><rect class="st-cur" x="544" y="93" width="70" height="24" rx="4"/><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><text class="tick" x="408" y="212">sent Ack 4095</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#ana3-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">TLP 4095</text><text class="tick" x="320" y="140" text-anchor="middle">accepted</text></svg><figcaption>צעד 3 : ‏TLP 4095 מגיע : המספר הצפוי, נמסר ל-TL. ‏NEXT_RCV_SEQ = 0; הספירה הגיעה לסף 2, ולכן יוצא Ack 4095 והסף הבא הוא 3.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 4 : ‏Ack 4095 מגיע; מצב המשדר והמקבל"><defs><marker id="ana4-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana4-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana4-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 4 · Ack 4095</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">0</text><rect class="st-cur" x="166" y="93" width="70" height="24" rx="4"/><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4095</text><text class="tick" x="30" y="136">retry buffer</text><text class="tick" x="46" y="160">empty</text><text class="tick" x="30" y="190">purged 4094, 4095</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">0</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><line class="fc-grant" x1="388" y1="118" x2="256" y2="118" marker-end="url(#ana4-s3)"/><text class="tick" x="320" y="88" text-anchor="middle">Ack 4095</text><text class="tick" x="320" y="140" text-anchor="middle">purge through it</text></svg><figcaption>צעד 4 : ‏Ack 4095 מגיע. ה-RC מוצא את 4095 ב-Retry Buffer ומוחק מהראש עד אליו : 4094, 4095. נשאר ריק, ‏ACKD_SEQ = 4095.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 5 : ה-RC שולח TLPs 0, 1, 2; מצב המשדר והמקבל"><defs><marker id="ana5-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana5-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana5-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 5 · send TLPs 0, 1, 2</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><rect class="st-cur" x="166" y="69" width="70" height="24" rx="4"/><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">3</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4095</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">1</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">2</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">0</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><text class="tick" x="320" y="88" text-anchor="middle">send TLPs</text><text class="tick" x="320" y="104" text-anchor="middle">0, 1, 2</text><text class="tick" x="320" y="140" text-anchor="middle">copies kept in the</text><text class="tick" x="320" y="156" text-anchor="middle">retry buffer</text></svg><figcaption>צעד 5 : ה-RC שולח TLPs 0, 1, 2. כל אחד מקבל את NEXT_TRANSMIT_SEQ ומקדם אותו; ה-Retry Buffer מחזיק 0, 1, 2, ועותקים נפרדים יצאו לקישור. ‏NEXT_TRANSMIT_SEQ = 3.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 6 : ‏TLP 0 מגיע; מצב המשדר והמקבל"><defs><marker id="ana6-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana6-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana6-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 6 · TLP 0</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">3</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4095</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">1</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">2</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><rect class="st-cur" x="544" y="69" width="70" height="24" rx="4"/><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">1</text><rect class="st-cur" x="544" y="93" width="70" height="24" rx="4"/><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">1 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#ana6-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">TLP 0</text><text class="tick" x="320" y="140" text-anchor="middle">accepted</text></svg><figcaption>צעד 6 : ‏TLP 0 מגיע : המספר הצפוי, נמסר ל-TL. ‏NEXT_RCV_SEQ = 1, 1 ממתינים ל-Ack מול סף 3.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 7 : ‏TLP 1 מגיע; מצב המשדר והמקבל"><defs><marker id="ana7-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana7-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana7-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 7 · TLP 1</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">3</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4095</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">1</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">2</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><rect class="st-cur" x="544" y="69" width="70" height="24" rx="4"/><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">2</text><rect class="st-cur" x="544" y="93" width="70" height="24" rx="4"/><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">2 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><rect class="fc-slot" x="550" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="569" y="184.5" text-anchor="middle">1</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#ana7-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">TLP 1</text><text class="tick" x="320" y="140" text-anchor="middle">accepted</text></svg><figcaption>צעד 7 : ‏TLP 1 מגיע : המספר הצפוי, נמסר ל-TL. ‏NEXT_RCV_SEQ = 2, 2 ממתינים ל-Ack מול סף 3.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 8 : ‏TLP 2 מגיע; מצב המשדר והמקבל"><defs><marker id="ana8-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana8-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana8-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 8 · TLP 2</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">3</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4095</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">1</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">2</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><rect class="st-cur" x="544" y="69" width="70" height="24" rx="4"/><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">3</text><rect class="st-cur" x="544" y="93" width="70" height="24" rx="4"/><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 1</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><rect class="fc-slot" x="550" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="569" y="184.5" text-anchor="middle">1</text><rect class="fc-slot" x="592" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="611" y="184.5" text-anchor="middle">2</text><text class="tick" x="408" y="212">sent Ack 2</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#ana8-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">TLP 2</text><text class="tick" x="320" y="140" text-anchor="middle">accepted</text></svg><figcaption>צעד 8 : ‏TLP 2 מגיע : המספר הצפוי, נמסר ל-TL. ‏NEXT_RCV_SEQ = 3; הספירה הגיעה לסף 3, ולכן יוצא Ack 2 והסף הבא הוא 1.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 9 : ‏Ack 2 מגיע; מצב המשדר והמקבל"><defs><marker id="ana9-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana9-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="ana9-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 9 · Ack 2</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">3</text><rect class="st-cur" x="166" y="93" width="70" height="24" rx="4"/><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">2</text><text class="tick" x="30" y="136">retry buffer</text><text class="tick" x="46" y="160">empty</text><text class="tick" x="30" y="190">purged 0, 1, 2</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">3</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 1</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><rect class="fc-slot" x="550" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="569" y="184.5" text-anchor="middle">1</text><rect class="fc-slot" x="592" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="611" y="184.5" text-anchor="middle">2</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><line class="fc-grant" x1="388" y1="118" x2="256" y2="118" marker-end="url(#ana9-s3)"/><text class="tick" x="320" y="88" text-anchor="middle">Ack 2</text><text class="tick" x="320" y="140" text-anchor="middle">purge through it</text></svg><figcaption>צעד 9 : ‏Ack 2 מגיע. ה-RC מוצא את 2 ב-Retry Buffer ומוחק מהראש עד אליו : 0, 1, 2. נשאר ריק, ‏ACKD_SEQ = 2.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="10"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <span class="viz-legend"><span><i class="fc-full"></i>רשומה ב-Retry Buffer</span><span><i class="fc-slot"></i>‏TLP שנמסר ל-Transaction Layer</span><span><i class="st-cur"></i>ערך שהשתנה בצעד הזה</span><span><i class="fc-pkt"></i>‏TLP מה-RC ל-EP</span><span><i class="fc-replay"></i>‏TLP משודר מחדש</span><span><i class="fc-grant"></i>‏Ack מה-EP ל-RC</span><span><i class="fc-nak"></i>‏Nak</span><span><i class="fc-drop"></i>פקט שנפגע על הקו</span></span>

    | צעד | אירוע | ‏NEXT_TRANSMIT_SEQ | ‏ACKD_SEQ | ‏Retry Buffer | ‏NEXT_RCV_SEQ | ממתינים / סף | ‏NAK_SCHEDULED |
    |---|---|---|---|---|---|---|---|
    | 0 | מצב התחלתי | 4094 | 4093 | ריק | 4094 | 0 / 2 | 0 |
    | 1 | ה-RC שולח TLPs 4094, 4095 | 0 | 4093 | 4094, 4095 | 4094 | 0 / 2 | 0 |
    | 2 | ‏TLP 4094 מגיע | 0 | 4093 | 4094, 4095 | 4095 | 1 / 2 | 0 |
    | 3 | ‏TLP 4095 מגיע | 0 | 4093 | 4094, 4095 | 0 | 0 / 3 | 0 |
    | 4 | ‏Ack 4095 מגיע | 0 | 4095 | ריק | 0 | 0 / 3 | 0 |
    | 5 | ה-RC שולח TLPs 0, 1, 2 | 3 | 4095 | 0, 1, 2 | 0 | 0 / 3 | 0 |
    | 6 | ‏TLP 0 מגיע | 3 | 4095 | 0, 1, 2 | 1 | 1 / 3 | 0 |
    | 7 | ‏TLP 1 מגיע | 3 | 4095 | 0, 1, 2 | 2 | 2 / 3 | 0 |
    | 8 | ‏TLP 2 מגיע | 3 | 4095 | 0, 1, 2 | 3 | 0 / 1 | 0 |
    | 9 | ‏Ack 2 מגיע | 3 | 2 | ריק | 3 | 0 / 1 | 0 |
    
    **אינווריאנט המשדר.** ה-Retry Buffer מכיל בדיוק את המספרים ACKD_SEQ + 1 עד
    NEXT_TRANSMIT_SEQ − 1, בסדר עולה מודולו 4096 : שידור מוסיף את NEXT_TRANSMIT_SEQ בסוף
    ומקדם אותו; Ack עם מספר \( s \) שנמצא בתור מוחק את הקידומת עד \( s \) ומעמיד
    ACKD_SEQ = \( s \), כך שהרשומה הראשונה שנשארה היא \( s + 1 \). לכן "מחיקה לפי אינדקס"
    ו"מחיקה של כל המספרים מ-ACKD_SEQ + 1 עד \( s \) על המעגל" הן אותה פעולה, והראשונה לא
    צריכה חשבון. ההשוואה `entry.seq <= ack.seq` שקולה להן רק כשאין גלישה בתוך התור.

    **אינווריאנט המקבל.** ‏NEXT_RCV_SEQ שווה למספר ה-TLPs שנמסרו ועוד מספר ההתחלה, מודולו
    4096, וה-TLPs שנמסרו הם בדיוק הקידומת של מה ששודר : כל TLP נמסר פעם אחת, בסדר. ‏Ack
    נושא תמיד NEXT_RCV_SEQ − 1, המספר האחרון שנמסר, ולכן המשדר מוחק רק מה שבאמת הגיע. כמה
    TLPs כל Ack מכסה (1 עד 4) לא משנה לנכונות, רק לכמות ה-DLLPs על הקישור.

    #### סיבוכיות { .sol-cost }

    שידור וקבלה הם \( O(1) \). ‏Ack עולה \( O(k) \) בחיפוש ובמחיקה, עם \( k \) הרשומות
    שעוד לא אושרו (במציאות מוגבל בגודל ה-Retry Buffer). הזיכרון : ה-Retry Buffer ותורי
    הפלט שהסביבה מרוקנת.

---

### סעיף ב – שגיאות : LCRC, פערים, כפילויות ו-Replay

עכשיו הקישור לא מושלם, והסביבה מזריקה שגיאות **על הקו**, אחרי שהמודל הוציא את הפקט :
‏`crc_ok = 0` על TLP או על DLLP, השמטה של פקט, או שינוי המספר ב-DLLP. ממשו מחלקות
יורשות שמשלימות את ההתנהגות :

- **מקבל :** TLP עם LCRC שגוי נזרק, ו-Nak עם NEXT_RCV_SEQ − 1 יוצא **רק אם** NAK_SCHEDULED
  כבוי, ואז הוא נדלק. ‏TLP "מהעתיד" (המספר לא הצפוי ולא ישן) מעיד שמשהו אבד : אותו טיפול.
  ‏TLP ישן (כפול) נזרק בלי למסור שוב, ובמקום Nak חוזר Ack עם NEXT_RCV_SEQ − 1, כי כנראה
  ה-Ack הקודם אבד; כל עוד NAK_SCHEDULED דולק אין Ack כלל, כי ה-Nak שכבר יצא מאשר את אותו
  מספר. ‏NAK_SCHEDULED כבה כשה-TLP הצפוי סוף סוף מגיע. "ישן" פירושו מרחק
  אחורה של 1 עד 2048 מהציפייה.
- **משדר :** DLLP עם CRC שגוי נספר ונזרק, בלי לגעת במצב. מספר שאינו ב-Retry Buffer ואינו
  ACKD_SEQ הוא Data Link Protocol Error : נספר ונזרק. ‏Nak תקין מוחק עד המספר ואז משדר מחדש
  את **כל** מה שנשאר, בסדר, עם המספרים המקוריים ו-`is_replay = 1`; ‏Nak עם ACKD_SEQ עצמו
  (בלי התקדמות) רק משדר מחדש. ‏`on_replay_timeout()` נקראת מהסביבה (במקום ה-REPLAY_TIMER)
  כשיש רשומות שלא אושרו זמן רב : משדרים מחדש את כולן.

אותה התחלה כמו בסעיף א (‏NEXT_TRANSMIT_SEQ = NEXT_RCV_SEQ = 4094), והספים של ה-EP הם 3
ואז 1. ה-RC שולח 4094, 4095, 0 ו-1. על הקו 4095 נפגע (LCRC), ואחר כך ה-Ack הראשון
שה-EP שולח נפגע גם הוא. עקבו אחרי שני הצדדים עד שה-Retry Buffer מתרוקן : אילו Nak-ים
ו-Ack-ים נשלחים, מה נמסר ל-Transaction Layer ומתי, מה משודר מחדש ולמה פעמיים, ומה קורה
ל-Ack עם מספר שאינו קיים (למשל 9)? למה ה-Retry Buffer חייב לשמור עותק שהקישור לא נוגע בו?

??? tip "רמז 1"
    שלושה סוגי TLP מגיעים למקבל : הצפוי, ישן יותר, חדש יותר. רק הראשון משנה מצב. השני
    אומר שה-Ack שלי לא הגיע; השלישי אומר שמשהו **לפניו** לא הגיע. מה כל אחד מהם צריך
    להחזיר, ומה קורה אם שולחים Nak על כל TLP מהעתיד?

??? tip "רמז 2"
    ‏Nak הוא Ack ועוד בקשה : קודם מוחקים כמו ב-Ack, ואז משדרים מחדש את מה שנשאר. ‏Ack
    שאבד אינו אסון כי ה-Ack הבא מצטבר; אבל אם לא יבוא עוד Ack, מי יזיז את המשדר? זה
    תפקיד ה-REPLAY_TIMER, וה-Replay שהוא גורם מביא למקבל TLPs שהוא כבר מסר.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏4094 נמסר; ‏4095 הפגום נזרק ויוצא Nak 4094 (‏NAK_SCHEDULED = 1); ‏0 ו-1 נזרקים
        בשקט. ה-RC מוחק את 4094, משדר מחדש 4095, 0, 1, וה-EP מוסר אותם; אחרי שלושה יוצא
        Ack 1, שנפגע על הקו : ה-RC סופר DLLP פגום ולא זז. הטיימר מפעיל Replay שני : ‏4095,
        0 ו-1 מגיעים ככפולים, כל אחד נזרק ועונה ב-Ack 1; ה-Ack הראשון מהם מרוקן את ה-Retry
        Buffer (ACKD_SEQ = 1) והשניים הבאים הם Ack חוזר על ACKD_SEQ, בלי השפעה. ‏Ack 9
        אינו ב-Retry Buffer ואינו ACKD_SEQ : שגיאת פרוטוקול, בלי שינוי. ה-Replay שולח את
        העותק מה-Retry Buffer; אילו הקישור היה משחית אותו, כל Replay היה פגום לנצח.

    <!-- cost: שידור \( O(1) \) | חזרה \( O(k) \) -->

    #### הרעיון { .sol-idea }

    **המקבל מסווג, לא מתקן.** ‏TLP שהמספר שלו הוא הצפוי נמסר; כל השאר נזרק, והשאלה היא
    רק מה לענות. פגום או מהעתיד : משהו חסר, ‏Nak עם המספר האחרון שנמסר, אבל **פעם אחת**
    לפער (NAK_SCHEDULED), כי כל TLP נוסף שמגיע בינתיים יעיד על אותו פער, וסופת Nak-ים
    הייתה גורמת לסופת Replay-ים. ישן : כבר נמסר, ה-Ack שלי כנראה אבד, עונים ב-Ack חוזר
    ולא ב-Nak, כי אין מה לשדר מחדש. ההבחנה בין ישן לחדש היא מרחק על מעגל של 4096 : עד
    2048 אחורה זה ישן.

    ```mermaid
    flowchart TD
        IN[TLP from the link] --> CRC{crc_ok?}
        CRC -->|no| NAK[Nak NEXT_RCV_SEQ − 1<br/>only if NAK_SCHEDULED == 0, then set it]
        CRC -->|yes| SEQ{seq == NEXT_RCV_SEQ?}
        SEQ -->|yes| ACC[deliver, NEXT_RCV_SEQ + 1,<br/>NAK_SCHEDULED = 0, count towards an Ack]
        SEQ -->|no| DUP{1 ≤ NEXT_RCV_SEQ − seq ≤ 2048?}
        DUP -->|yes: an old one| ACK[discard, Ack NEXT_RCV_SEQ − 1 again]
        DUP -->|no: a future one| NAK
    ```

    **המשדר מאמין רק ל-DLLP תקין.** CRC שגוי : אי אפשר לסמוך על הסוג ולא על המספר, זורקים.
    מספר תקין הוא או רשומה ב-Retry Buffer (התקדמות : מוחקים עד אליה) או ACKD_SEQ (אין
    התקדמות); כל מספר אחר הוא שגיאת פרוטוקול. ואז, אם זה Nak, משדרים מחדש את כל מה שנשאר.
    ‏Replay תמיד מה-Retry Buffer, שבו העותק נקי : לכן `send_tlp` הוציא לקישור עותק נפרד.

    ```mermaid
    flowchart TD
        IN[DLLP from the link] --> CRC{crc_ok?}
        CRC -->|no| BAD[discard, bad_dllp_count + 1]
        CRC -->|yes| FIND{seq in the Retry Buffer?}
        FIND -->|yes| PURGE[purge through it, ACKD_SEQ = seq]
        FIND -->|no| SAME{seq == ACKD_SEQ?}
        SAME -->|no| ERR[discard, protocol_error_count + 1]
        SAME -->|yes| KIND
        PURGE --> KIND{Ack or Nak?}
        KIND -->|Ack| DONE[done]
        KIND -->|Nak| REPLAY[replay every entry left, in order, same numbers]
    ```

    **מי סוגר Ack שאבד.** ‏Ack מצטבר, ולכן אם יגיע עוד Ack הכול יסתדר. אם לא יגיע (זה היה
    האחרון, או שהמקבל ממתין ל-TLP שלא יבוא), ה-REPLAY_TIMER של המשדר מפעיל Replay; המקבל
    מקבל כפילויות, זורק אותן ועונה ב-Ack חוזר, שמרוקן את ה-Retry Buffer. כאן הטיימר הוא
    קריאה מהסביבה, `on_replay_timeout()`.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **קבלת TLP :** ‏`crc_ok = 0` → `schedule_nak`. המספר הצפוי → `accept` של סעיף א. ישן
       (מרחק אחורה 1 עד 2048) → נספר ככפול, ו-`send_ack` אם אין Nak ממתין. אחרת, מהעתיד →
       `schedule_nak`.
    2. **‏schedule_nak :** אם NAK_SCHEDULED דולק, כלום. אחרת Nak עם NEXT_RCV_SEQ − 1,
       הדלקה, ואיפוס הספירה ל-Ack (ה-Nak מאשר אותם).
    3. **קבלת DLLP :** ‏`crc_ok = 0` → נספר ונזרק. חיפוש המספר : נמצא → `purge_through`;
       לא נמצא ושווה ל-ACKD_SEQ → בלי שינוי; אחרת → שגיאת פרוטוקול ויציאה. אם Nak →
       `replay`.
    4. **‏replay :** לכל רשומה ב-Retry Buffer, מהראשונה, עותק עם `is_replay = 1` לתור
       השידור. ‏`on_replay_timeout` עושה בדיוק את זה.

    </div>

    #### הקוד { .sol-code }

    שתי מחלקות יורשות. `accept`, ‏`send_ack` ו-`purge_through` של סעיף א נשארים כפי שהם.

    === "Python"
        ```python title="TransmitterWithReplay, ReceiverWithNak" linenums="1" hl_lines="6 8 12 15 26 35 44 46 47 49 56"
        class TransmitterWithReplay(DllTransmitter):
            """Part b: the transmitter learns to distrust DLLPs and to replay."""

            def receive_dllp(self, dllp: Dllp) -> None:
                if not dllp.crc_ok:
                    self.bad_dllp_count += 1                      # (1)!
                    return
                index = self.find_in_retry_buffer(dllp.seq)
                if index >= 0:
                    self.purge_through(index, dllp.seq)
                elif dllp.seq != self.ackd_seq:
                    self.protocol_error_count += 1                # (2)!
                    return
                if dllp.kind is DllpKind.NAK:
                    self.replay()                                 # (3)!

            def on_replay_timeout(self) -> None:
                """The replay timer (kept by the environment) expired with TLPs still unacknowledged."""
                self.replay()

            def replay(self) -> None:
                """Every unacknowledged TLP again, oldest first, with its original Sequence Number."""
                if not self.retry_buffer:
                    return
                for tlp in self.retry_buffer:
                    self.tx_tlps.append(replace(tlp, is_replay=True))   # (4)!
                self.replay_count += 1


        class ReceiverWithNak(DllReceiver):
            """Part b: the receiver sorts every TLP into expected, old or future, and answers each."""

            def is_duplicate(self, seq: int) -> bool:
                """An old one: up to half the sequence space behind the number we wait for."""
                behind = (self.next_rcv_seq - seq) % SEQ_MOD      # (5)!
                return 0 < behind <= SEQ_MOD // 2

            def receive_tlp(self, tlp: Tlp) -> None:
                if not tlp.crc_ok:
                    self.bad_tlp_count += 1
                    self.schedule_nak()
                elif tlp.seq == self.next_rcv_seq:
                    self.accept(tlp)
                elif self.is_duplicate(tlp.seq):
                    self.duplicate_count += 1
                    if not self.nak_scheduled:
                        self.send_ack()                           # (6)!
                else:
                    self.bad_tlp_count += 1                       # (7)!
                    self.schedule_nak()

            def schedule_nak(self) -> None:
                """One Nak per gap: the next one only after the expected TLP arrived."""
                if self.nak_scheduled:
                    return
                self.tx_dllps.append(Dllp(DllpKind.NAK, self.last_accepted()))
                self.nak_scheduled = True                         # (8)!
                self.accepted_since_ack = 0
        ```

        1. פקט עם CRC שגוי : גם הסוג וגם המספר עלולים להיות שגויים, ולכן שום דבר בו לא
           משפיע על המצב.
        2. לא ב-Retry Buffer ולא ACKD_SEQ : המקבל "אישר" משהו שלא שודר. זורקים וסופרים.
        3. ‏Nak הוא Ack ועוד Replay; Nak עם ACKD_SEQ (אין התקדמות) מגיע לכאן בלי מחיקה.
        4. עותק מהרשומה השמורה, שהקישור לא נגע בה : גם אם העותק הקודם הושחת על הקו, ה-Replay
           תקין.
        5. המרחק אחורה על המעגל : 1 עד 2048 הוא ישן, 2049 ומעלה הוא "מהעתיד" (מרחק קדימה של
           1 עד 2047).
        6. כפול : כבר נמסר, לא מוסרים שוב, ועונים ב-Ack חוזר כדי שהמשדר יוכל לנקות. אם Nak
           כבר ממתין, הוא מאשר את אותו מספר, ואין Ack כל עוד NAK_SCHEDULED דולק.
        7. מהעתיד : ה-TLP הזה אולי תקין, אבל מה שלפניו חסר, ולכן זורקים ומבקשים Replay.
        8. הדגל שמונע סופת Nak-ים; `accept` של סעיף א מכבה אותו כשהפער נסגר.

    === "SystemVerilog"
        ```systemverilog title="dll_transmitter_with_replay, dll_receiver_with_nak" linenums="1" hl_lines="10 13 17 20 32 33 48 58 60 62 71"
        // Part b: the transmitter learns to distrust DLLPs and to replay.
        class dll_transmitter_with_replay extends dll_transmitter;
          function new(seq_t start_seq = 0);
            super.new(start_seq);
          endfunction

          virtual function void receive_dllp(pcie_dllp dllp);
            int index;
            if (!dllp.crc_ok) begin
              bad_dllp_count++;                                              // (1)!
              return;
            end
            index = find_in_retry_buffer(dllp.seq);
            if (index >= 0)
              purge_through(index, dllp.seq);
            else if (dllp.seq != ackd_seq) begin
              protocol_error_count++;                                        // (2)!
              return;
            end
            if (dllp.kind == DLLP_NAK) replay();                             // (3)!
          endfunction

          // The replay timer (kept by the environment) expired with TLPs still unacknowledged.
          function void on_replay_timeout();
            replay();
          endfunction

          // Every unacknowledged TLP again, oldest first, with its original Sequence Number.
          function void replay();
            if (retry_buffer.size() == 0) return;
            foreach (retry_buffer[i]) begin
              pcie_tlp copy = retry_buffer[i].clone();                       // (4)!
              copy.is_replay = 1;
              tx_tlps.push_back(copy);
            end
            replay_count++;
          endfunction
        endclass

        // Part b: the receiver sorts every TLP into expected, old or future, and answers each.
        class dll_receiver_with_nak extends dll_receiver;
          function new(seq_t start_seq = 0);
            super.new(start_seq);
          endfunction

          // An old one: up to half the sequence space behind the number we wait for.
          function bit is_duplicate(seq_t seq);
            seq_t behind = next_rcv_seq - seq;                               // (5)!
            return behind != 0 && behind <= 2048;
          endfunction

          virtual function void receive_tlp(pcie_tlp tlp);
            if (!tlp.crc_ok) begin
              bad_tlp_count++;
              schedule_nak();
            end else if (tlp.seq == next_rcv_seq)
              accept(tlp);
            else if (is_duplicate(tlp.seq)) begin
              duplicate_count++;
              if (!nak_scheduled) send_ack();                                // (6)!
            end else begin
              bad_tlp_count++;                                               // (7)!
              schedule_nak();
            end
          endfunction

          // One Nak per gap: the next one only after the expected TLP arrived.
          function void schedule_nak();
            pcie_dllp nak;
            if (nak_scheduled) return;
            nak = new(DLLP_NAK, last_accepted());
            tx_dllps.push_back(nak);
            nak_scheduled      = 1;                                          // (8)!
            accepted_since_ack = 0;
          endfunction
        endclass
        ```

        1. פקט עם CRC שגוי : גם הסוג וגם המספר עלולים להיות שגויים, ולכן שום דבר בו לא
           משפיע על המצב.
        2. לא ב-Retry Buffer ולא ACKD_SEQ : המקבל "אישר" משהו שלא שודר. זורקים וסופרים.
        3. ‏Nak הוא Ack ועוד Replay; Nak עם ACKD_SEQ (אין התקדמות) מגיע לכאן בלי מחיקה.
        4. עותק מהרשומה השמורה, שהקישור לא נגע בה : גם אם העותק הקודם הושחת על הקו, ה-Replay
           תקין.
        5. ‏`next_rcv_seq - seq` ב-12 ביט הוא המרחק אחורה על המעגל : 1 עד 2048 הוא ישן,
           2049 ומעלה הוא "מהעתיד" (מרחק קדימה של 1 עד 2047).
        6. כפול : כבר נמסר, לא מוסרים שוב, ועונים ב-Ack חוזר כדי שהמשדר יוכל לנקות. אם Nak
           כבר ממתין, הוא מאשר את אותו מספר, ואין Ack כל עוד NAK_SCHEDULED דולק.
        7. מהעתיד : ה-TLP הזה אולי תקין, אבל מה שלפניו חסר, ולכן זורקים ומבקשים Replay.
        8. הדגל שמונע סופת Nak-ים; `accept` של סעיף א מכבה אותו כשהפער נסגר.

    #### למה זה נכון { .sol-proof }

    **הדוגמה, צעד אחרי צעד.** ‏4095 נפגע על הקו, ואחר כך Ack 1; הטיימר סוגר את הפער, ו-Ack
    9 נזרק :

    <div class="stepper" role="group" aria-label="שגיאות, צעד אחרי צעד : TLP פגום, Nak ו-Replay, Ack פגום, טיימר, כפילויות ו-Ack לא חוקי" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 0 : מצב התחלתי; מצב המשדר והמקבל"><defs><marker id="anb0-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb0-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb0-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 0 · initial state</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">4094</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4093</text><text class="tick" x="30" y="136">retry buffer</text><text class="tick" x="46" y="160">empty</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">4094</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><text class="tick" x="424" y="184">empty</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><text class="tick" x="320" y="88" text-anchor="middle">initial state</text></svg><figcaption>צעד 0 : הקישור פעיל כבר זמן מה. ה-RC עומד על NEXT_TRANSMIT_SEQ = 4094 ו-ACKD_SEQ = 4093, ה-Retry Buffer ריק; ה-EP מצפה ל-4094 והסף הראשון שהגריל הוא 3.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 1 : ה-RC שולח TLPs 4094, 4095, 0, 1; מצב המשדר והמקבל"><defs><marker id="anb1-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb1-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb1-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 1 · send TLPs 4094, 4095, 0, 1</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><rect class="st-cur" x="166" y="69" width="70" height="24" rx="4"/><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4093</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4094</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="172" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="191" y="160.5" text-anchor="middle">1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">4094</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><text class="tick" x="424" y="184">empty</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><text class="tick" x="320" y="88" text-anchor="middle">send TLPs</text><text class="tick" x="320" y="104" text-anchor="middle">4094, 4095, 0, 1</text><text class="tick" x="320" y="140" text-anchor="middle">copies kept in the</text><text class="tick" x="320" y="156" text-anchor="middle">retry buffer</text></svg><figcaption>צעד 1 : ה-RC שולח TLPs 4094, 4095, 0, 1. כל אחד מקבל את NEXT_TRANSMIT_SEQ ומקדם אותו; ה-Retry Buffer מחזיק 4094, 4095, 0, 1, ועותקים נפרדים יצאו לקישור. ‏NEXT_TRANSMIT_SEQ = 2.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 2 : ‏TLP 4094 מגיע; מצב המשדר והמקבל"><defs><marker id="anb2-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb2-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb2-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 2 · TLP 4094</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4093</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4094</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="172" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="191" y="160.5" text-anchor="middle">1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><rect class="st-cur" x="544" y="69" width="70" height="24" rx="4"/><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">4095</text><rect class="st-cur" x="544" y="93" width="70" height="24" rx="4"/><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">1 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><text class="tick" x="408" y="232" font-size="11">bad TLP 0 · duplicates 0</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#anb2-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">TLP 4094</text><text class="tick" x="320" y="140" text-anchor="middle">accepted</text></svg><figcaption>צעד 2 : ‏TLP 4094 מגיע : המספר הצפוי, נמסר ל-TL. ‏NEXT_RCV_SEQ = 4095, 1 ממתינים ל-Ack מול סף 3.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 3 : ‏TLP 4095 מגיע עם LCRC שגוי; מצב המשדר והמקבל"><defs><marker id="anb3-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb3-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb3-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 3 · TLP 4095 bad LCRC</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4093</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4094</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="172" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="191" y="160.5" text-anchor="middle">1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">4095</text><rect class="st-cur" x="544" y="93" width="70" height="24" rx="4"/><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 3</text><rect class="st-cur" x="544" y="117" width="70" height="24" rx="4"/><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">1</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><text class="tick" x="408" y="212">sent Nak 4094</text><text class="cs-no" x="408" y="232" font-size="11">bad TLP 1 · duplicates 0</text><line class="fc-drop" x1="252" y1="118" x2="308" y2="118"/><text class="cs-no" x="320" y="123" text-anchor="middle">✕</text><text class="tick" x="320" y="88" text-anchor="middle">TLP 4095</text><text class="tick" x="320" y="104" text-anchor="middle">bad LCRC</text><text class="tick" x="320" y="140" text-anchor="middle">discarded;</text><text class="tick" x="320" y="156" text-anchor="middle">Nak once</text></svg><figcaption>צעד 3 : ‏TLP 4095 מגיע עם LCRC שגוי. ה-EP זורק אותו ושולח Nak 4094 (האחרון שנמסר); NAK_SCHEDULED נדלק והספירה ל-Ack מתאפסת. ‏NEXT_RCV_SEQ נשאר 4095.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 4 : ‏TLP 0 מגיע לפני זמנו; מצב המשדר והמקבל"><defs><marker id="anb4-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb4-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb4-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 4 · TLP 0</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4093</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4094</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="172" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="191" y="160.5" text-anchor="middle">1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">4095</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">1</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><text class="cs-no" x="408" y="232" font-size="11">bad TLP 2 · duplicates 0</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#anb4-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">TLP 0</text><text class="tick" x="320" y="140" text-anchor="middle">future:</text><text class="tick" x="320" y="156" text-anchor="middle">discarded, no Nak</text></svg><figcaption>צעד 4 : ‏TLP 0 מגיע לפני זמנו : ה-EP עדיין מצפה ל-4095, ולכן זה TLP "מהעתיד". נזרק, ובלי Nak נוסף כי NAK_SCHEDULED דולק.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 5 : ‏TLP 1 מגיע לפני זמנו; מצב המשדר והמקבל"><defs><marker id="anb5-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb5-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb5-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 5 · TLP 1</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4093</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4094</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="172" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="191" y="160.5" text-anchor="middle">1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 0</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">4095</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">1</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><text class="cs-no" x="408" y="232" font-size="11">bad TLP 3 · duplicates 0</text><line class="fc-pkt" x1="252" y1="118" x2="384" y2="118" marker-end="url(#anb5-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">TLP 1</text><text class="tick" x="320" y="140" text-anchor="middle">future:</text><text class="tick" x="320" y="156" text-anchor="middle">discarded, no Nak</text></svg><figcaption>צעד 5 : ‏TLP 1 מגיע לפני זמנו : ה-EP עדיין מצפה ל-4095, ולכן זה TLP "מהעתיד". נזרק, ובלי Nak נוסף כי NAK_SCHEDULED דולק.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 6 : ‏Nak 4094 מגיע; מצב המשדר והמקבל"><defs><marker id="anb6-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb6-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb6-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 6 · Nak 4094</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><rect class="st-cur" x="166" y="93" width="70" height="24" rx="4"/><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4094</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">1</text><text class="tick" x="30" y="190">purged 4094; replay 4095, 0, 1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 1</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">4095</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 3</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">1</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><text class="tick" x="408" y="232" font-size="11">bad TLP 3 · duplicates 0</text><line class="fc-nak" x1="388" y1="118" x2="256" y2="118" marker-end="url(#anb6-s2)"/><text class="tick" x="320" y="88" text-anchor="middle">Nak 4094</text><text class="tick" x="320" y="140" text-anchor="middle">purge, then</text><text class="tick" x="320" y="156" text-anchor="middle">replay the rest</text></svg><figcaption>צעד 6 : ‏Nak 4094 מגיע. קודם כמו Ack : 4094 נמחק ו-ACKD_SEQ = 4094; ואז Replay של כל מה שנשאר, בסדר ועם המספרים המקוריים : 4095, 0, 1.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 7 : ‏TLP 4095 מגיע (Replay); מצב המשדר והמקבל"><defs><marker id="anb7-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb7-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb7-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 7 · replayed TLP 4095</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4094</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 1</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><rect class="st-cur" x="544" y="69" width="70" height="24" rx="4"/><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">0</text><rect class="st-cur" x="544" y="93" width="70" height="24" rx="4"/><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">1 / 3</text><rect class="st-cur" x="544" y="117" width="70" height="24" rx="4"/><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><text class="tick" x="408" y="232" font-size="11">bad TLP 3 · duplicates 0</text><line class="fc-replay" x1="252" y1="118" x2="384" y2="118" marker-end="url(#anb7-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">replayed TLP 4095</text><text class="tick" x="320" y="140" text-anchor="middle">accepted</text></svg><figcaption>צעד 7 : ‏TLP 4095 מגיע (Replay) : המספר הצפוי, נמסר ל-TL ו-NAK_SCHEDULED כבה. ‏NEXT_RCV_SEQ = 0, 1 ממתינים ל-Ack מול סף 3.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 8 : ‏TLP 0, 1 מגיע (Replay); מצב המשדר והמקבל"><defs><marker id="anb8-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb8-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb8-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 8 · replayed TLPs 0, 1</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4094</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 0 · protocol err 0 · replays 1</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><rect class="st-cur" x="544" y="69" width="70" height="24" rx="4"/><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">2</text><rect class="st-cur" x="544" y="93" width="70" height="24" rx="4"/><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 1</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><rect class="fc-slot" x="550" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="569" y="184.5" text-anchor="middle">1</text><text class="tick" x="408" y="212">sent Ack 1</text><text class="tick" x="408" y="232" font-size="11">bad TLP 3 · duplicates 0</text><line class="fc-replay" x1="252" y1="118" x2="384" y2="118" marker-end="url(#anb8-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">replayed TLPs</text><text class="tick" x="320" y="104" text-anchor="middle">0, 1</text><text class="tick" x="320" y="140" text-anchor="middle">accepted</text></svg><figcaption>צעד 8 : ‏TLP 0, 1 מגיע (Replay) : המספרים הצפויים, נמסרים ל-TL. ‏NEXT_RCV_SEQ = 2; הספירה הגיעה לסף 3, ולכן יוצא Ack 1 והסף הבא הוא 1.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 9 : ‏Ack 1 מגיע עם CRC שגוי; מצב המשדר והמקבל"><defs><marker id="anb9-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb9-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb9-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 9 · Ack 1 bad CRC</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4094</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">1</text><text class="cs-no" x="30" y="226" font-size="11">bad DLLP 1 · protocol err 0 · replays 1</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">2</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 1</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><rect class="fc-slot" x="550" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="569" y="184.5" text-anchor="middle">1</text><text class="tick" x="408" y="232" font-size="11">bad TLP 3 · duplicates 0</text><line class="fc-drop" x1="388" y1="118" x2="332" y2="118"/><text class="cs-no" x="320" y="123" text-anchor="middle">✕</text><text class="tick" x="320" y="88" text-anchor="middle">Ack 1</text><text class="tick" x="320" y="104" text-anchor="middle">bad CRC</text><text class="tick" x="320" y="140" text-anchor="middle">discarded,</text><text class="tick" x="320" y="156" text-anchor="middle">nothing changes</text></svg><figcaption>צעד 9 : ‏Ack 1 מגיע עם CRC שגוי. אי אפשר לסמוך על הסוג ולא על המספר : ה-RC סופר DLLP פגום ולא נוגע ב-Retry Buffer (4095, 0, 1) ולא ב-ACKD_SEQ.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 10 : ה-REPLAY_TIMER פג; מצב המשדר והמקבל"><defs><marker id="anb10-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb10-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb10-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 10 · replay timer expired</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4094</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">1</text><text class="tick" x="30" y="190">replay 4095, 0, 1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 1 · protocol err 0 · replays 2</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">2</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 1</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><rect class="fc-slot" x="550" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="569" y="184.5" text-anchor="middle">1</text><text class="tick" x="408" y="232" font-size="11">bad TLP 3 · duplicates 0</text><text class="tick" x="320" y="88" text-anchor="middle">replay timer expired</text><text class="tick" x="320" y="140" text-anchor="middle">replay everything</text><text class="tick" x="320" y="156" text-anchor="middle">unacknowledged</text></svg><figcaption>צעד 10 : ה-REPLAY_TIMER פג וב-Retry Buffer עוד 4095, 0, 1. ה-RC משדר מחדש את כולם מהעותקים השמורים : 4095, 0, 1.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 11 : ‏TLP 4095, 0, 1 מגיע שוב (כפול); מצב המשדר והמקבל"><defs><marker id="anb11-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb11-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb11-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 11 · replayed TLPs 4095, 0, 1</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">4094</text><text class="tick" x="30" y="136">retry buffer</text><rect class="fc-full" x="46" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="65" y="160.5" text-anchor="middle">4095</text><rect class="fc-full" x="88" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="107" y="160.5" text-anchor="middle">0</text><rect class="fc-full" x="130" y="144" width="38" height="24" rx="3"/><text class="st-text st-sm" x="149" y="160.5" text-anchor="middle">1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 1 · protocol err 0 · replays 2</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">2</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 1</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><rect class="fc-slot" x="550" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="569" y="184.5" text-anchor="middle">1</text><text class="tick" x="408" y="212">sent Ack 1, Ack 1, Ack 1</text><text class="cs-no" x="408" y="232" font-size="11">bad TLP 3 · duplicates 3</text><line class="fc-replay" x1="252" y1="118" x2="384" y2="118" marker-end="url(#anb11-s1)"/><text class="tick" x="320" y="88" text-anchor="middle">replayed TLPs</text><text class="tick" x="320" y="104" text-anchor="middle">4095, 0, 1</text><text class="tick" x="320" y="140" text-anchor="middle">old: discarded,</text><text class="tick" x="320" y="156" text-anchor="middle">Ack again</text></svg><figcaption>צעד 11 : ‏TLP 4095, 0, 1 מגיע שוב (כפול). ה-EP כבר מסר אותם (NEXT_RCV_SEQ = 2), ולכן כל אחד נזרק ועונה ב-Ack חוזר : Ack 1, Ack 1, Ack 1. ‏Nak אין, כי שום דבר לא חסר.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 12 : ‏Ack 1 מגיע; מצב המשדר והמקבל"><defs><marker id="anb12-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb12-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb12-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 12 · Ack 1</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><rect class="st-cur" x="166" y="93" width="70" height="24" rx="4"/><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">1</text><text class="tick" x="30" y="136">retry buffer</text><text class="tick" x="46" y="160">empty</text><text class="tick" x="30" y="190">purged 4095, 0, 1</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 1 · protocol err 0 · replays 2</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">2</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 1</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><rect class="fc-slot" x="550" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="569" y="184.5" text-anchor="middle">1</text><text class="tick" x="408" y="232" font-size="11">bad TLP 3 · duplicates 3</text><line class="fc-grant" x1="388" y1="118" x2="256" y2="118" marker-end="url(#anb12-s3)"/><text class="tick" x="320" y="88" text-anchor="middle">Ack 1</text><text class="tick" x="320" y="140" text-anchor="middle">purge through it</text></svg><figcaption>צעד 12 : ‏Ack 1 מגיע. ה-RC מוצא את 1 ב-Retry Buffer ומוחק מהראש עד אליו : 4095, 0, 1. נשאר ריק, ‏ACKD_SEQ = 1.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 13 : ‏Ack 1 מגיע; מצב המשדר והמקבל"><defs><marker id="anb13-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb13-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb13-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 13 · Ack 1</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">1</text><text class="tick" x="30" y="136">retry buffer</text><text class="tick" x="46" y="160">empty</text><text class="tick" x="30" y="226" font-size="11">bad DLLP 1 · protocol err 0 · replays 2</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">2</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 1</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><rect class="fc-slot" x="550" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="569" y="184.5" text-anchor="middle">1</text><text class="tick" x="408" y="232" font-size="11">bad TLP 3 · duplicates 3</text><line class="fc-grant" x1="388" y1="118" x2="256" y2="118" marker-end="url(#anb13-s3)"/><text class="tick" x="320" y="88" text-anchor="middle">Ack 1</text><text class="tick" x="320" y="140" text-anchor="middle">purge through it</text></svg><figcaption>צעד 13 : ‏Ack 1 מגיע. המספר הוא ACKD_SEQ עצמו : Ack חוזר בלי התקדמות, שום דבר לא משתנה.</figcaption></figure><figure class="stepper-frame"><svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="צעד 14 : ‏Ack 9 מגיע עם מספר לא מוכר; מצב המשדר והמקבל"><defs><marker id="anb14-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb14-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="anb14-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><text class="coord" x="8" y="20" font-weight="700">step 14 · Ack 9 unknown seq</text><rect class="cs-blk" x="16" y="36" width="230" height="204" rx="6"/><text class="coord" x="131" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text><text class="tick" x="30" y="86">NEXT_TRANSMIT_SEQ</text><text class="st-text" x="230" y="86" text-anchor="end">2</text><text class="tick" x="30" y="110">ACKD_SEQ</text><text class="st-text" x="230" y="110" text-anchor="end">1</text><text class="tick" x="30" y="136">retry buffer</text><text class="tick" x="46" y="160">empty</text><text class="cs-no" x="30" y="226" font-size="11">bad DLLP 1 · protocol err 1 · replays 2</text><rect class="cs-blk" x="394" y="36" width="230" height="204" rx="6"/><text class="coord" x="509" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text><text class="tick" x="408" y="86">NEXT_RCV_SEQ</text><text class="st-text" x="608" y="86" text-anchor="end">2</text><text class="tick" x="408" y="110">pending / threshold</text><text class="st-text" x="608" y="110" text-anchor="end">0 / 1</text><text class="tick" x="408" y="134">NAK_SCHEDULED</text><text class="st-text" x="608" y="134" text-anchor="end">0</text><text class="tick" x="408" y="160">delivered to TL</text><rect class="fc-slot" x="424" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="443" y="184.5" text-anchor="middle">4094</text><rect class="fc-slot" x="466" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="485" y="184.5" text-anchor="middle">4095</text><rect class="fc-slot" x="508" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="527" y="184.5" text-anchor="middle">0</text><rect class="fc-slot" x="550" y="168" width="38" height="24" rx="3"/><text class="st-text st-sm" x="569" y="184.5" text-anchor="middle">1</text><text class="tick" x="408" y="232" font-size="11">bad TLP 3 · duplicates 3</text><line class="fc-grant" x1="388" y1="118" x2="256" y2="118" marker-end="url(#anb14-s3)"/><text class="cs-no" x="320" y="123" text-anchor="middle">?</text><text class="tick" x="320" y="88" text-anchor="middle">Ack 9</text><text class="tick" x="320" y="104" text-anchor="middle">unknown seq</text><text class="tick" x="320" y="140" text-anchor="middle">protocol error,</text><text class="tick" x="320" y="156" text-anchor="middle">nothing changes</text></svg><figcaption>צעד 14 : ‏Ack 9 מגיע עם מספר לא מוכר. המספר אינו ב-Retry Buffer ואינו ACKD_SEQ (1) : Data Link Protocol Error, נספר ונזרק בלי שינוי.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="15"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <span class="viz-legend"><span><i class="fc-full"></i>רשומה ב-Retry Buffer</span><span><i class="fc-slot"></i>‏TLP שנמסר ל-Transaction Layer</span><span><i class="st-cur"></i>ערך שהשתנה בצעד הזה</span><span><i class="fc-pkt"></i>‏TLP מה-RC ל-EP</span><span><i class="fc-replay"></i>‏TLP משודר מחדש</span><span><i class="fc-grant"></i>‏Ack מה-EP ל-RC</span><span><i class="fc-nak"></i>‏Nak</span><span><i class="fc-drop"></i>פקט שנפגע על הקו</span></span>

    | צעד | אירוע | ‏NEXT_TRANSMIT_SEQ | ‏ACKD_SEQ | ‏Retry Buffer | ‏NEXT_RCV_SEQ | ממתינים / סף | ‏NAK_SCHEDULED |
    |---|---|---|---|---|---|---|---|
    | 0 | מצב התחלתי | 4094 | 4093 | ריק | 4094 | 0 / 3 | 0 |
    | 1 | ה-RC שולח TLPs 4094, 4095, 0, 1 | 2 | 4093 | 4094, 4095, 0, 1 | 4094 | 0 / 3 | 0 |
    | 2 | ‏TLP 4094 מגיע | 2 | 4093 | 4094, 4095, 0, 1 | 4095 | 1 / 3 | 0 |
    | 3 | ‏TLP 4095 מגיע עם LCRC שגוי | 2 | 4093 | 4094, 4095, 0, 1 | 4095 | 0 / 3 | 1 |
    | 4 | ‏TLP 0 מגיע לפני זמנו | 2 | 4093 | 4094, 4095, 0, 1 | 4095 | 0 / 3 | 1 |
    | 5 | ‏TLP 1 מגיע לפני זמנו | 2 | 4093 | 4094, 4095, 0, 1 | 4095 | 0 / 3 | 1 |
    | 6 | ‏Nak 4094 מגיע | 2 | 4094 | 4095, 0, 1 | 4095 | 0 / 3 | 1 |
    | 7 | ‏TLP 4095 מגיע (Replay) | 2 | 4094 | 4095, 0, 1 | 0 | 1 / 3 | 0 |
    | 8 | ‏TLP 0, 1 מגיע (Replay) | 2 | 4094 | 4095, 0, 1 | 2 | 0 / 1 | 0 |
    | 9 | ‏Ack 1 מגיע עם CRC שגוי | 2 | 4094 | 4095, 0, 1 | 2 | 0 / 1 | 0 |
    | 10 | ה-REPLAY_TIMER פג | 2 | 4094 | 4095, 0, 1 | 2 | 0 / 1 | 0 |
    | 11 | ‏TLP 4095, 0, 1 מגיע שוב (כפול) | 2 | 4094 | 4095, 0, 1 | 2 | 0 / 1 | 0 |
    | 12 | ‏Ack 1 מגיע | 2 | 1 | ריק | 2 | 0 / 1 | 0 |
    | 13 | ‏Ack 1 מגיע | 2 | 1 | ריק | 2 | 0 / 1 | 0 |
    | 14 | ‏Ack 9 מגיע עם מספר לא מוכר | 2 | 1 | ריק | 2 | 0 / 1 | 0 |
    
    **מסירה אמינה ובסדר.** המקבל מוסר רק TLP תקין שהמספר שלו הוא NEXT_RCV_SEQ, ולכן
    המסירות הן תמיד קידומת רצופה של סדר השידור, בלי חורים ובלי כפילויות, תהיה ההשחתה אשר
    תהיה. נשאר להראות שכל TLP יימסר **בסופו של דבר** : רשומה נמחקת מה-Retry Buffer רק על
    DLLP תקין שהמספר שלו ב-Retry Buffer, והמקבל שולח מספר רק כ-NEXT_RCV_SEQ − 1, כלומר
    מספר שכבר נמסר; לכן ב-Retry Buffer יש תמיד את כל מה שלא נמסר (עם עותק נקי). ‏Nak או
    הטיימר משדרים את כולו מחדש בסדר, כך שה-TLP הצפוי מגיע לפני כל מה שאחריו. כל עוד הקישור
    מעביר פקט תקין מדי פעם, הציפייה מתקדמת. ה-tests מריצים תעבורה אקראית עם השחתות,
    השמטות ומספרים לא חוקיים דרך כמה גלישות, ובודקים שהמסירות שוות לשידורים.

    **מספר Nak-ים.** בין שני TLPs צפויים שנמסרו יוצא לכל היותר Nak אחד, כי `schedule_nak`
    שולח רק כש-NAK_SCHEDULED כבוי ורק `accept` מכבה אותו. לכן Replay אחד לפער, לא אחד לכל
    TLP שנזרק. באותו זמן גם לא יוצא Ack, לא מהטיימר ולא על כפול : ה-Nak כבר אישר את
    NEXT_RCV_SEQ − 1, ‏`schedule_nak` איפס את הספירה ורק `accept` מעלה אותה.

    **לנסות בעצמכם.** התיבה הבאה מריצה את שני המודלים עם הקישור ביניהם : שתי הדוגמאות שלמעלה
    כתסריטים, צעד אחרי צעד, וגם אירועים חופשיים : ה-RC שולח TLP, הפקט שבראש כל תור נמסר,
    נמסר עם CRC שגוי או אובד, ושני הטיימרים. בכל צעד מודגש מה השתנה, ושני האינווריאנטים
    נבדקים. "הרצה אקראית" מגרילה תסריט כמו ה-test של העמוד, עם שיעור תקלות לבחירה, ובודקת
    את שני האינווריאנטים אחרי כל אירוע; הפרה ראשונה הייתה עוצרת את התסריט, ואותו ערך אתחול
    נותן את אותו תסריט. ציר האירועים מתחת לשני הצדדים מוסיף עמודה לכל אירוע, עם המונים אחריו
    ו-✗ כשאינווריאנט נופל.

    <div class="explorer" data-kind="acknak"></div>

    #### סיבוכיות { .sol-cost }

    כמו בסעיף א, ועוד Replay ב-\( O(k) \) לכל הרשומות שלא אושרו. בכל פקט פגום העלות היא
    \( O(1) \) : בדיקה, מונה, ולכל היותר DLLP אחד.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : Ack מוחק רשומה אחת"
    ‏Ack 5 הוא "הכול עד 5", לא "5". מי שמוחק רק את הרשומה 5 משאיר את 3 ו-4 ב-Retry Buffer
    לנצח, וכל Nak עתידי ישדר אותן מחדש כפולות. גם Nak מוחק קודם : ‏Nak 4094 אומר ש-4094
    הגיע.

??? trap "מלכודת : השוואה מספרית בגלישה"
    ‏`entry.seq <= ack.seq` נכשלת כש-4095 נעקב ב-0, וכך גם `received < expected` לזיהוי
    כפילות. ב-Retry Buffer מוחקים לפי מקום אחרי חיפוש; במקבל מודדים מרחק אחורה ב-12 ביט
    ומשווים ל-2048.

??? trap "מלכודת : ה-Retry Buffer שומר את מה שעל הקו"
    אם `send_tlp` דוחף את אותו אובייקט ל-Retry Buffer ולקישור, הזרקת `crc_ok = 0` על הקו
    משחיתה גם את העותק השמור, וכל Replay ייפגע לנצח. מודל נכון שומר עותק ומוציא עותק.

??? trap "מלכודת : Nak על כל TLP שנזרק"
    אחרי TLP פגום מגיעים גם כל ה-TLPs שאחריו, וכולם "מהעתיד". בלי NAK_SCHEDULED כל אחד מהם
    היה מייצר Nak, וכל Nak עוד Replay של אותו תוכן : סופה. ‏Nak אחד לפער, וה-TLP הצפוי מכבה
    את הדגל.

??? trap "מלכודת : לסמוך על DLLP פגום"
    ‏DLLP עם CRC שגוי יכול לשאת מספר שגוי או סוג שגוי. ‏Ack 4095 שהשתבש ל-Ack 95 היה מוחק
    רשומות שלא אושרו, ו-TLP שאבד לא היה משודר שוב לעולם. פקט פגום נספר ונזרק, וגם מספר
    "חוקי" שאינו ב-Retry Buffer ואינו ACKD_SEQ נזרק.

??? followup "שאלות המשך"
    - **הטיימרים :** איך היו נראים AckNak Latency Timer ו-REPLAY_TIMER בתוך המודל, ומה
      REPLAY_NUM (ארבעה Replay-ים ללא התקדמות → אימון מחדש של הקישור) היה מוסיף?

        ??? fu-answer "תשובה"
            הטיימר AckNak Latency שייך למקבל : מתחיל כשנמסר TLP שעוד לא אושר, ובפקיעה שולח Ack,
            כלומר `flush_ack()`. ה-REPLAY_TIMER שייך למשדר : רץ כל עוד ה-Retry Buffer לא ריק,
            מתאפס על Ack או Nak שמתקדמים, ובפקיעה קורא ל-`on_replay_timeout()`. ה-REPLAY_NUM הוא
            מונה של 2 ביט שעולה בכל Replay ומתאפס בהתקדמות; כשהוא גולש מ-3 ל-0 המודל מדווח על
            אימון מחדש של הקישור, ואחריו ה-Replay ממשיך.

    - **‏TLP מהעתיד שהוא בעצם תקין :** ה-TLP 0 שנזרק אחרי 4095 הפגום היה שלם. למה בכל זאת
      זורקים אותו במקום לשמור אותו עד שהחסר יגיע (Selective Repeat)? מה ההשלכה על גודל
      ה-Buffer ועל Ack מצטבר?

        ??? fu-answer "תשובה"
            זה Go-Back-N : המקבל מחזיק רק את NEXT_RCV_SEQ ומוסר רק את הצפוי, בלי buffer לסידור
            מחדש, וה-Ack המצטבר נכון כי כל מה שעד המספר באמת נמסר. המחיר : TLPs תקינים משודרים
            שוב. ‏Selective Repeat חוסך את זה, אבל דורש במקבל buffer בגודל החלון כולו ו-Ack
            לכל TLP או מפת ביטים.

    - **‏Nak עם ACKD_SEQ :** מתי המקבל שולח Nak שאינו מתקדם, ומה ההבדל בינו ל-Ack חוזר?

        ??? fu-answer "תשובה"
            כשה-TLP הראשון אחרי ה-Ack האחרון פגום או חסר : NEXT_RCV_SEQ − 1 עוד לא זז, ולכן
            ה-Nak נושא את ACKD_SEQ. ‏Ack חוזר עם ACKD_SEQ לא עושה כלום, ו-Nak עם אותו מספר לא
            מוחק כלום, אבל משדר מחדש את כל ה-Retry Buffer.

    - **הכיוון ההפוך :** כל פורט הוא גם משדר וגם מקבל. איך מרכיבים משתי המחלקות "פורט", ומה
      משותף לשני הכיוונים?

        ??? fu-answer "תשובה"
            פורט מחזיק `dll_transmitter` לכיוון שלו ו-`dll_receiver` לכיוון של השכן : DLLPs
            נכנסים הולכים למשדר, ו-TLPs נכנסים למקבל. אין מצב משותף : המספרים, ה-Retry Buffer
            ו-NAK_SCHEDULED נפרדים לכל כיוון, ומשותף להם רק הקישור, שבו ה-TLPs של המשדר וה-DLLPs
            של המקבל יוצאים על אותו חוט.

    - **גודל ה-Retry Buffer :** למה המפרט מגביל את מספר ה-TLPs שלא אושרו (2048 מספרים
      "לפנים"), ומה קורה לזיהוי הכפילויות אם המשדר חורג?

        ??? fu-answer "תשובה"
            המקבל מסווג TLP כ"ישן" אם הוא 1 עד 2048 אחורה מהציפייה, ואחרת "מהעתיד". המשדר נעצר
            כשההפרש בין NEXT_TRANSMIT_SEQ ל-ACKD_SEQ, מודולו 4096, מגיע ל-2048, וכך כל
            עותק ב-Replay נמצא בחצי האחורי. אם יחרוג, עותק ישן מדי ייראה "מהעתיד" : המקבל
            ישלח Nak במקום Ack חוזר, והסיווג נשבר.

    - **מודל ייחוס כבודק :** מה ה-scoreboard משווה בין המודל ל-DUT : תור השידור, ה-DLLPs,
      או רק מה שנמסר ל-TL?

        ??? fu-answer "תשובה"
            מה שנמסר ל-TL משווים במדויק : כל TLP פעם אחת, בסדר. התזמון של ה-Ack-ים אקראי (סף,
            טיימר), ולכן את ה-DLLPs ואת תור השידור בודקים כחוקיות ולא כהעתק : מספר ה-Ack
            בין ACKD_SEQ ל-NEXT_RCV_SEQ − 1, ‏Nak אחד לפער, ו-Replay שמכיל בדיוק את מה שעוד לא
            אושר, בסדר ועם המספרים המקוריים.
