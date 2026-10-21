---
id: 20
title: פיצול Completions ב-PCIe – כל הדרכים להחזיר קריאה אחת
level: senior
difficulty: medium
tags: [protocols, pcie, algorithms, recursion, python, systemverilog]
source: ""
added: 2026-10-18
---

## השאלה

ב-PCIe, רכיב (ה-Requester) שולח בקשת קריאה מהזיכרון (MemRd) של `len` בתים
מכתובת `addr`. הצד השני (ה-Completer) מחזיר את המידע ב-Completion אחד או יותר (CplD),
ושלושה פרמטרים קובעים איך:

- **‏MRRS** (Max_Read_Request_Size), בצד ה-Requester: הגודל המקסימלי של בקשה אחת. בשאלה
  הזו הבקשה כבר עומדת בו (\( len \le MRRS \)) ואינה חוצה גבול של 4 KB.
- **‏MPS** (Max_Payload_Size): ה-payload המקסימלי של Completion אחד.
- **‏RCB** (Read Completion Boundary), 64 או 128 בתים: הגבולות המיושרים בזיכרון שבהם מותר
  ל-Completer לחתוך את התשובה.

חוקי הפיצול לפי ה-SPEC (הסעיף Data Return for Read Requests):

1. ה-Completion הראשון מתחיל בכתובת הבקשה, ומסתיים בסוף הבקשה או בכפולה של RCB.
2. כל Completion אמצעי מתחיל ומסתיים בכפולות של RCB, כלומר אורכו כפולה שלמה של RCB.
3. ה-Completion האחרון מסתיים בדיוק בסוף הבקשה.
4. אף Completion לא גדול מ-MPS, וה-Completions חוזרים בסדר כתובות עולה.

כתבו פונקציה `completion_splits(addr, len, mps, rcb)` שמחזירה **את כל** רצפי הגדלים
החוקיים של ה-Completions, כרשימה של רשימות (הניחו ש-MPS ו-RCB הם חזקות של 2
ו-\( MPS \ge RCB \)). למשל, לבקשה של 256 בתים מכתובת `0x1010` עם `RCB = 64` ו-`MPS = 256` יש
16 פיצולים: `[256]`, `[240, 16]`, `[176, 80]`, ועד `[48, 64, 64, 64, 16]`.

??? interviewer "מה המראיין בודק"
    - **הבנת הפרוטוקול:** האם המועמד מבדיל בין MRRS (גודל הבקשה), MPS (גודל כל Completion)
      ו-RCB (איפה מותר לחתוך), ולא מערבב ביניהם.
    - **תרגום חוקים למודל:** האם הוא מצליח לצמצם את ארבעת החוקים של ה-SPEC לתנאי אחד
      פשוט שאפשר לקודד.
    - **מנייה שיטתית:** רקורסיה או backtracking שמייצרים כל פתרון בדיוק פעם אחת, בלי
      לשכוח את המקרה הלא מיושר.
    - **חשיבת DV:** מה עושים עם הרשימה הזו אחר כך: reference model ל-scoreboard, ו-coverage
      על צורות הפיצול.

---

??? tip "רמז 1"
    שלושת החוקים הראשונים אומרים משהו על **נקודות החיתוך** בין Completion ל-Completion.
    איפה בדיוק מותר לחתוך? כמה נקודות כאלה יש בתוך הבקשה של הדוגמה?

??? tip "רמז 2"
    חשבו רקורסיבית: איפה יכול להסתיים ה-Completion **הראשון**? לכל אפשרות, מה שנשאר אחריו
    הוא בדיוק אותה בעיה, מכתובת חדשה. איך MPS נכנס לבחירה הזו?

??? success "פתרון"
    !!! answer "תשובה בקצרה"
        שלושת החוקים הראשונים שקולים לתנאי אחד: **כל נקודת חיתוך בין שני Completions היא
        כפולה של RCB**. לכן בונים את הפיצולים ברקורסיה: מהמיקום הנוכחי מנסים כל גבול RCB
        שבתוך הבקשה ובמרחק של עד MPS, וגם את סוף הבקשה אם הוא בהישג יד. כל מסלול שמגיע
        לסוף הבקשה הוא פיצול חוקי. בדוגמה יש 4 גבולות בתוך הבקשה, ולכן \( 2^4 = 16 \)
        פיצולים.

    #### הרעיון { .sol-idea }

    **הפרמטרים על ציר הכתובות.** הבקשה מכסה את הטווח `0x1010` עד `0x110F`. גבולות ה-RCB
    הם כפולות של 64: ‏`0x1040`, ‏`0x1080`, ‏`0x10C0` ו-`0x1100` נמצאים בתוך הבקשה, ואלה
    נקודות החיתוך היחידות המותרות. ה-MPS מגביל כמה רחוק מגיע כל Completion מנקודת
    ההתחלה שלו:

    <svg class="figure cs-fig" viewBox="0 0 640 196" style="max-width:40rem" role="img" aria-label="בקשת קריאה של 256 בתים מכתובת 0x1010 על רשת גבולות ה-RCB, טווח ה-MPS של ה-Completion הראשון, ופיצול חוקי אחד: 48, 128, 80"><defs><marker id="cs-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="cs-rcb" x1="40.0" y1="26" x2="40.0" y2="150"/><text class="coord halo" x="40.0" y="18" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="152.0" y1="26" x2="152.0" y2="150"/><text class="coord halo" x="152.0" y="18" text-anchor="middle">0x1040</text><line class="cs-rcb" x1="264.0" y1="26" x2="264.0" y2="150"/><text class="coord halo" x="264.0" y="18" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="376.0" y1="26" x2="376.0" y2="150"/><text class="coord halo" x="376.0" y="18" text-anchor="middle">0x10C0</text><line class="cs-rcb" x1="488.0" y1="26" x2="488.0" y2="150"/><text class="coord halo" x="488.0" y="18" text-anchor="middle">0x1100</text><line class="cs-rcb" x1="600.0" y1="26" x2="600.0" y2="150"/><text class="coord halo" x="600.0" y="18" text-anchor="middle">0x1140</text><line class="cs-req" x1="68.0" y1="30" x2="68.0" y2="150"/><line class="cs-req" x1="516.0" y1="30" x2="516.0" y2="150"/><line class="ink-line" x1="68.0" y1="48" x2="291.0" y2="48" stroke-width="1.6" marker-end="url(#cs-arrow)"/><text class="legend halo" x="180.0" y="42" text-anchor="middle">MPS = 128</text><circle class="cs-can" cx="152.0" cy="48" r="4.5"><title>0x1040: a legal end of the first completion</title></circle><circle class="cs-can" cx="264.0" cy="48" r="4.5"><title>0x1080: a legal end of the first completion</title></circle><text class="cs-no" x="376.0" y="52.5" text-anchor="middle">✕</text><rect class="cs-first" x="68.0" y="62" width="84.0" height="30" rx="3"><title>0x1010–0x103F: 48 bytes</title></rect><text class="cs-size" x="110.0" y="82" text-anchor="middle">48</text><text class="tick" x="110.0" y="108" text-anchor="middle">first</text><rect class="cs-mid" x="152.0" y="62" width="224.0" height="30" rx="3"><title>0x1040–0x10BF: 128 bytes</title></rect><text class="cs-size" x="264.0" y="82" text-anchor="middle">128</text><text class="tick" x="264.0" y="108" text-anchor="middle">mid</text><rect class="cs-last" x="376.0" y="62" width="140.0" height="30" rx="3"><title>0x10C0–0x110F: 80 bytes</title></rect><text class="cs-size" x="446.0" y="82" text-anchor="middle">80</text><text class="tick" x="446.0" y="108" text-anchor="middle">last</text><line class="ink-line" x1="153.0" y1="128" x2="263.0" y2="128" stroke-width="1.6" marker-start="url(#cs-arrow)" marker-end="url(#cs-arrow)"/><text class="legend halo" x="208.0" y="122" text-anchor="middle">RCB = 64</text><line class="ink-line" x1="69.0" y1="160" x2="515.0" y2="160" stroke-width="1.6" marker-start="url(#cs-arrow)" marker-end="url(#cs-arrow)"/><text class="legend halo" x="292.0" y="178" text-anchor="middle">request: 256 B from 0x1010 (≤ MRRS)</text></svg>

    <span class="viz-legend"><span><i class="cs-rcb"></i>גבול RCB: כאן מותר לחתוך</span><span><i class="cs-req"></i>תחילת הבקשה וסופה</span><span><i class="cs-can"></i>סוף אפשרי ל-Completion הראשון</span><span><i class="cs-first"></i>ראשון: עד גבול RCB</span><span><i class="cs-mid"></i>אמצעי: כפולה של RCB</span><span><i class="cs-last"></i>אחרון: עד סוף הבקשה</span></span>

    **למה "כל חיתוך על גבול RCB" מספיק.** אם כל נקודת חיתוך היא כפולה של RCB, אז
    ה-Completion הראשון מסתיים על גבול (חוק 1), כל אמצעי מתחיל ומסתיים על גבולות ולכן
    אורכו כפולה של RCB (חוק 2), והאחרון מסתיים בסוף הבקשה כי שם הרקורסיה נעצרת (חוק 3).
    ולהפך: מהחוקים נובע שכל חיתוך הוא על גבול. אז במקום לבדוק שלושה חוקים בודקים
    תנאי אחד על כתובות החיתוך, ו-MPS הוא סינון נוסף על המרחק בין חיתוכים עוקבים.

    **הרקורסיה.** המצב הוא `pos`, הבית הראשון שעוד לא כוסה, והרשימה `sizes` של הגדלים
    עד כה. מ-`pos` יש קבוצה קטנה של סיומים אפשריים ל-Completion הבא: סוף הבקשה אם
    \( pos + MPS \ge end \), וכל גבול RCB \( b \) עם \( pos < b < end \) ו-\( b \le pos + MPS \).
    לכל סיום כזה קוראים שוב עם `cut` ועם הגודל `cut - pos` מצורף לרשימה. כשמגיעים ל-`end`
    הרשימה היא פיצול שלם. הסיומים נבדקים **מהרחוק לקרוב**, ולכן הפיצול הראשון שמוחזר הוא
    זה עם הכי פחות Completions (החמדני), והאחרון הוא זה שחותך בכל גבול.

    ```mermaid
    flowchart TD
        A["extend(pos, sizes)"] --> B{"pos == end ?"}
        B -- "yes" --> C["sizes is a complete split:<br/>append it to the result"]
        B -- "no" --> D["cuts = [ ]"]
        D --> E{"pos + MPS ≥ end ?"}
        E -- "yes" --> F["add end to cuts"]
        E -- "no" --> G
        F --> G["b = first RCB boundary after pos"]
        G --> H{"b < end and b ≤ pos + MPS ?"}
        H -- "yes" --> I["add b to cuts<br/>b = b + RCB"] --> H
        H -- "no" --> J["for each cut, largest first"]
        J --> K["extend(cut, sizes + [cut − pos])"]
        K -. "recursion" .-> A
    ```

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סוף הבקשה:** מחשבים \( end = addr + len \). הרקורסיה מתחילה מ-`pos = addr` ומרשימה
       ריקה.
    2. **תנאי עצירה:** אם `pos == end`, הרשימה שנצברה היא פיצול חוקי שלם. שומרים אותה.
    3. **הסיומים האפשריים:** סוף הבקשה, אם הוא במרחק של עד MPS; וכל גבול RCB שגדול
       מ-`pos`, קטן מ-`end` ובמרחק של עד MPS. הגבול הראשון אחרי `pos` הוא
       \( (\lfloor pos / RCB \rfloor + 1) \cdot RCB \), והשאר בקפיצות של RCB.
    4. **הסתעפות:** לכל סיום `cut`, מהרחוק לקרוב, קוראים ל-`extend(cut, sizes + [cut - pos])`.
    5. **התוצאה:** רשימת כל הפיצולים, בסדר שבו נמצאו: הראשון עם הכי פחות Completions,
       האחרון עם הכי הרבה.

    </div>

    #### הקוד { .sol-code }

    בדוגמה הפונקציה מחזירה 16 רשימות, מ-`[256]` ועד `[48, 64, 64, 64, 16]`. ב-SystemVerilog
    התוצאה היא תור של תורים (`int splits[$][$]`), והרקורסיה יושבת בפונקציית עזר כי
    הפונקציה הראשית רק מאפסת את התוצאה וקוראת לה.

    === "SystemVerilog"
        ```systemverilog title="function completion_splits" linenums="1" hl_lines="17 21 22 27"
        // Every legal sequence of completion payload sizes for a read of `len` bytes from
        // `addr` (len <= MRRS, no 4 KB crossing). `splits` gets one queue of sizes per
        // split, in address order; the first split has the fewest completions.
        function automatic void completion_splits(longint unsigned addr, int len, int mps, int rcb,
                                                  ref int splits[$][$]);
          int sizes[$];
          splits.delete();
          extend_split(addr, addr + len, mps, rcb, sizes, splits);
        endfunction

        // One step of the recursion: `pos` is the first byte not covered yet and `sizes` the
        // completions chosen so far.
        function automatic void extend_split(longint unsigned pos, longint unsigned req_end,
                                             int mps, int rcb, int sizes[$], ref int splits[$][$]);
          longint unsigned cuts[$];
          longint unsigned boundary;
          int longer[$];
          if (pos == req_end) begin                                   // (1)!
            splits.push_back(sizes);
            return;
          end
          if (pos + mps >= req_end) cuts.push_back(req_end);          // (2)!
          boundary = (pos / rcb + 1) * rcb;                           // (3)!
          while (boundary < req_end && boundary <= pos + mps) begin
            cuts.push_back(boundary);
            boundary += rcb;
          end
          cuts.rsort();                                               // (4)!
          foreach (cuts[i]) begin
            longer = sizes;
            longer.push_back(int'(cuts[i] - pos));
            extend_split(cuts[i], req_end, mps, rcb, longer, splits);
          end
        endfunction
        ```

        1. תנאי העצירה: כל הבתים כוסו, והרשימה שנצברה היא פיצול חוקי. `sizes` מועבר
           **בערך** (עותק), ולכן כל ענף של הרקורסיה מחזיק רשימה משלו.
        2. סוף הבקשה הוא סיום אפשרי רק אם הוא במרחק של עד MPS מ-`pos`. בלי התנאי הזה
           הפונקציה הייתה מחזירה גם `[256]` כש-MPS הוא 128.
        3. הגבול הראשון אחרי `pos`: חילוק שלם, ועוד אחד, כפול RCB. אם `pos` עצמו על גבול
           (כמו באמצע הבקשה) מקבלים את הגבול הבא, לא את `pos`. הלולאה עוצרת בסוף הבקשה או
           כשהגבול רחוק מ-MPS.
        4. מיון יורד: הסיום הרחוק קודם. כך `splits[0]` הוא הפיצול החמדני (הכי פחות
           Completions) ו-`splits[$]` הוא זה שחותך בכל גבול.

    === "Python"
        ```python title="completion_splits" linenums="1" hl_lines="10 14 16 20"
        def completion_splits(addr: int, length: int, mps: int, rcb: int) -> list[list[int]]:
            """Every legal sequence of completion payload sizes for a read of `length` bytes
            from `addr` (length <= MRRS, no 4 KB crossing), in address order. Each split is
            a list of sizes; the first split has the fewest completions, the last the most."""
            end = addr + length
            splits = []

            def extend(pos, sizes):
                """`pos` is the first byte not covered yet, `sizes` the completions so far."""
                if pos == end:                                  # (1)!
                    splits.append(sizes)
                    return
                cuts = []
                if pos + mps >= end:                            # (2)!
                    cuts.append(end)
                boundary = (pos // rcb + 1) * rcb               # (3)!
                while boundary < end and boundary <= pos + mps:
                    cuts.append(boundary)
                    boundary += rcb
                for cut in sorted(cuts, reverse=True):          # (4)!
                    extend(cut, sizes + [cut - pos])

            extend(addr, [])
            return splits
        ```

        1. תנאי העצירה: כל הבתים כוסו, והרשימה שנצברה היא פיצול חוקי. `sizes + [...]`
           יוצר רשימה חדשה בכל קריאה, ולכן כל ענף של הרקורסיה מחזיק רשימה משלו.
        2. סוף הבקשה הוא סיום אפשרי רק אם הוא במרחק של עד MPS מ-`pos`. בלי התנאי הזה
           הפונקציה הייתה מחזירה גם `[256]` כש-MPS הוא 128.
        3. הגבול הראשון אחרי `pos`: חילוק שלם, ועוד אחד, כפול RCB. אם `pos` עצמו על גבול
           (כמו באמצע הבקשה) מקבלים את הגבול הבא, לא את `pos`. הלולאה עוצרת בסוף הבקשה או
           כשהגבול רחוק מ-MPS.
        4. מיון יורד: הסיום הרחוק קודם. כך `splits[0]` הוא הפיצול החמדני (הכי פחות
           Completions) ו-`splits[-1]` הוא זה שחותך בכל גבול.

    #### למה זה נכון { .sol-proof }

    **כל 16 הפיצולים של הדוגמה.** כל שורה היא פיצול אחד על ציר הכתובות, בסדר שהפונקציה
    מחזירה. בכל שורה החיתוכים נופלים רק על הקווים המקווקווים (גבולות ה-RCB):

    <svg class="figure cs-fig" viewBox="0 0 640 602" style="max-width:40rem" role="img" aria-label="כל הפיצולים החוקיים של הבקשה, שורה לכל פיצול, מקובצים לפי מספר ה-Completions"><line class="cs-rcb" x1="128.0" y1="24" x2="128.0" y2="598"/><text class="coord halo" x="128.0" y="16" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="224.8" y1="24" x2="224.8" y2="598"/><text class="coord halo" x="224.8" y="16" text-anchor="middle">0x1040</text><line class="cs-rcb" x1="321.6" y1="24" x2="321.6" y2="598"/><text class="coord halo" x="321.6" y="16" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="418.4" y1="24" x2="418.4" y2="598"/><text class="coord halo" x="418.4" y="16" text-anchor="middle">0x10C0</text><line class="cs-rcb" x1="515.2" y1="24" x2="515.2" y2="598"/><text class="coord halo" x="515.2" y="16" text-anchor="middle">0x1100</text><line class="cs-rcb" x1="612.0" y1="24" x2="612.0" y2="598"/><text class="coord halo" x="612.0" y="16" text-anchor="middle">0x1140</text><line class="cs-req" x1="152.2" y1="24" x2="152.2" y2="598"/><line class="cs-req" x1="539.4" y1="24" x2="539.4" y2="598"/><text class="legend halo" x="136" y="45" font-weight="700">1 completion: 1 split</text><g><text class="coord halo" x="118" y="69" text-anchor="end">256</text><rect class="cs-one" x="152.2" y="54" width="387.2" height="22" rx="3"><title>0x1010–0x110F: 256 bytes (one)</title></rect><text class="cs-size" x="345.8" y="69" text-anchor="middle">256</text></g><text class="legend halo" x="136" y="97" font-weight="700">2 completions: 4 splits</text><g><text class="coord halo" x="118" y="121" text-anchor="end">240+16</text><rect class="cs-first" x="152.2" y="106" width="363.0" height="22" rx="3"><title>0x1010–0x10FF: 240 bytes (first)</title></rect><text class="cs-size" x="333.7" y="121" text-anchor="middle">240</text><rect class="cs-last" x="515.2" y="106" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="121" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="149" text-anchor="end">176+80</text><rect class="cs-first" x="152.2" y="134" width="266.2" height="22" rx="3"><title>0x1010–0x10BF: 176 bytes (first)</title></rect><text class="cs-size" x="285.3" y="149" text-anchor="middle">176</text><rect class="cs-last" x="418.4" y="134" width="121.0" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="478.9" y="149" text-anchor="middle">80</text></g><g><text class="coord halo" x="118" y="177" text-anchor="end">112+144</text><rect class="cs-first" x="152.2" y="162" width="169.4" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="236.9" y="177" text-anchor="middle">112</text><rect class="cs-last" x="321.6" y="162" width="217.8" height="22" rx="3"><title>0x1080–0x110F: 144 bytes (last)</title></rect><text class="cs-size" x="430.5" y="177" text-anchor="middle">144</text></g><g><text class="coord halo" x="118" y="205" text-anchor="end">48+208</text><rect class="cs-first" x="152.2" y="190" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="205" text-anchor="middle">48</text><rect class="cs-last" x="224.8" y="190" width="314.6" height="22" rx="3"><title>0x1040–0x110F: 208 bytes (last)</title></rect><text class="cs-size" x="382.1" y="205" text-anchor="middle">208</text></g><text class="legend halo" x="136" y="233" font-weight="700">3 completions: 6 splits</text><g><text class="coord halo" x="118" y="257" text-anchor="end">176+64+16</text><rect class="cs-first" x="152.2" y="242" width="266.2" height="22" rx="3"><title>0x1010–0x10BF: 176 bytes (first)</title></rect><text class="cs-size" x="285.3" y="257" text-anchor="middle">176</text><rect class="cs-mid" x="418.4" y="242" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="466.8" y="257" text-anchor="middle">64</text><rect class="cs-last" x="515.2" y="242" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="257" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="285" text-anchor="end">112+128+16</text><rect class="cs-first" x="152.2" y="270" width="169.4" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="236.9" y="285" text-anchor="middle">112</text><rect class="cs-mid" x="321.6" y="270" width="193.6" height="22" rx="3"><title>0x1080–0x10FF: 128 bytes (mid)</title></rect><text class="cs-size" x="418.4" y="285" text-anchor="middle">128</text><rect class="cs-last" x="515.2" y="270" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="285" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="313" text-anchor="end">112+64+80</text><rect class="cs-first" x="152.2" y="298" width="169.4" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="236.9" y="313" text-anchor="middle">112</text><rect class="cs-mid" x="321.6" y="298" width="96.8" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="313" text-anchor="middle">64</text><rect class="cs-last" x="418.4" y="298" width="121.0" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="478.9" y="313" text-anchor="middle">80</text></g><g><text class="coord halo" x="118" y="341" text-anchor="end">48+192+16</text><rect class="cs-first" x="152.2" y="326" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="341" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="326" width="290.4" height="22" rx="3"><title>0x1040–0x10FF: 192 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="341" text-anchor="middle">192</text><rect class="cs-last" x="515.2" y="326" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="341" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="369" text-anchor="end">48+128+80</text><rect class="cs-first" x="152.2" y="354" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="369" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="354" width="193.6" height="22" rx="3"><title>0x1040–0x10BF: 128 bytes (mid)</title></rect><text class="cs-size" x="321.6" y="369" text-anchor="middle">128</text><rect class="cs-last" x="418.4" y="354" width="121.0" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="478.9" y="369" text-anchor="middle">80</text></g><g><text class="coord halo" x="118" y="397" text-anchor="end">48+64+144</text><rect class="cs-first" x="152.2" y="382" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="397" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="382" width="96.8" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="273.2" y="397" text-anchor="middle">64</text><rect class="cs-last" x="321.6" y="382" width="217.8" height="22" rx="3"><title>0x1080–0x110F: 144 bytes (last)</title></rect><text class="cs-size" x="430.5" y="397" text-anchor="middle">144</text></g><text class="legend halo" x="136" y="425" font-weight="700">4 completions: 4 splits</text><g><text class="coord halo" x="118" y="449" text-anchor="end">112+64+64+16</text><rect class="cs-first" x="152.2" y="434" width="169.4" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="236.9" y="449" text-anchor="middle">112</text><rect class="cs-mid" x="321.6" y="434" width="96.8" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="449" text-anchor="middle">64</text><rect class="cs-mid" x="418.4" y="434" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="466.8" y="449" text-anchor="middle">64</text><rect class="cs-last" x="515.2" y="434" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="449" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="477" text-anchor="end">48+128+64+16</text><rect class="cs-first" x="152.2" y="462" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="477" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="462" width="193.6" height="22" rx="3"><title>0x1040–0x10BF: 128 bytes (mid)</title></rect><text class="cs-size" x="321.6" y="477" text-anchor="middle">128</text><rect class="cs-mid" x="418.4" y="462" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="466.8" y="477" text-anchor="middle">64</text><rect class="cs-last" x="515.2" y="462" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="477" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="505" text-anchor="end">48+64+128+16</text><rect class="cs-first" x="152.2" y="490" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="505" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="490" width="96.8" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="273.2" y="505" text-anchor="middle">64</text><rect class="cs-mid" x="321.6" y="490" width="193.6" height="22" rx="3"><title>0x1080–0x10FF: 128 bytes (mid)</title></rect><text class="cs-size" x="418.4" y="505" text-anchor="middle">128</text><rect class="cs-last" x="515.2" y="490" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="505" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="533" text-anchor="end">48+64+64+80</text><rect class="cs-first" x="152.2" y="518" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="533" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="518" width="96.8" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="273.2" y="533" text-anchor="middle">64</text><rect class="cs-mid" x="321.6" y="518" width="96.8" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="533" text-anchor="middle">64</text><rect class="cs-last" x="418.4" y="518" width="121.0" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="478.9" y="533" text-anchor="middle">80</text></g><text class="legend halo" x="136" y="561" font-weight="700">5 completions: 1 split</text><g><text class="coord halo" x="118" y="585" text-anchor="end">48+64+64+64+16</text><rect class="cs-first" x="152.2" y="570" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="585" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="570" width="96.8" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="273.2" y="585" text-anchor="middle">64</text><rect class="cs-mid" x="321.6" y="570" width="96.8" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="585" text-anchor="middle">64</text><rect class="cs-mid" x="418.4" y="570" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="466.8" y="585" text-anchor="middle">64</text><rect class="cs-last" x="515.2" y="570" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="585" text-anchor="middle">16</text></g></svg>

    <span class="viz-legend"><span><i class="cs-first"></i>ה-Completion הראשון (או היחיד)</span><span><i class="cs-mid"></i>אמצעי</span><span><i class="cs-last"></i>אחרון</span></span>

    | מספר Completions | כמה פיצולים | הפיצולים (בסדר שהאלגוריתם מחזיר) |
    |:-:|:-:|---|
    | 1 | 1 | ‏256 |
    | 2 | 4 | ‏240+16, ‏176+80, ‏112+144, ‏48+208 |
    | 3 | 6 | ‏176+64+16, ‏112+128+16, ‏112+64+80, ‏48+192+16, ‏48+128+80, ‏48+64+144 |
    | 4 | 4 | ‏112+64+64+16, ‏48+128+64+16, ‏48+64+128+16, ‏48+64+64+80 |
    | 5 | 1 | ‏48+64+64+64+16 |
    | **סך הכול** | **16** | |

    **שלמות ונכונות.** פיצול חוקי הוא בחירה של תת-קבוצה של גבולות ה-RCB שבתוך הבקשה
    (כל גבול: לחתוך בו או לא), עם התנאי שהמרחק בין שני חיתוכים עוקבים (כולל ההתחלה
    והסוף) לא עולה על MPS. הרקורסיה בונה את תת-הקבוצות האלה לפי סדר הכתובות: מ-`pos`
    היא מנסה **כל** סיום מותר ולא שום דבר אחר, ושני ענפים שונים נבדלים בסיום של
    Completion כלשהו, ולכן נותנים פיצולים שונים. כל מסלול שמגיע ל-`end` עובר רק דרך
    גבולות RCB ומרחקים של עד MPS, ולכן הוא חוקי; וכל פיצול חוקי הוא מסלול כזה.

    **כמה פיצולים יש.** מספר הגבולות שבתוך הבקשה הוא

    \[
    c = \left\lfloor \frac{addr + len - 1}{RCB} \right\rfloor - \left\lfloor \frac{addr}{RCB} \right\rfloor .
    \]

    בלי מגבלת MPS (כלומר כש-\( MPS \ge len \)) כל תת-קבוצה חוקית ויש בדיוק \( 2^c \)
    פיצולים. בדוגמה \( c = 4 \), ולכן 16. מספר ה-Completions המקסימלי הוא \( c + 1 \) (חיתוך
    בכל גבול), והמינימלי הוא הפיצול החמדני, שהוא הראשון ברשימה.

    **איך MPS גוזם.** אותה בקשה עם `MPS = 128`: כל פיצול שיש בו Completion גדול מ-128 נפסל,
    ונשארים 8. שימו לב שפיצול כמו `[128, 128]` לא קיים בכלל: מכתובת לא מיושרת
    ה-Completion הראשון חייב להסתיים על גבול, ולכן הוא 48, 112, 176 או 240, אף פעם לא 128:

    <svg class="figure cs-fig" viewBox="0 0 640 602" style="max-width:40rem" role="img" aria-label="אותם פיצולים כש-MPS = 128: הפיצולים שיש בהם Completion גדול מ-128 מסומנים ודהויים"><line class="cs-rcb" x1="128.0" y1="24" x2="128.0" y2="598"/><text class="coord halo" x="128.0" y="16" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="224.8" y1="24" x2="224.8" y2="598"/><text class="coord halo" x="224.8" y="16" text-anchor="middle">0x1040</text><line class="cs-rcb" x1="321.6" y1="24" x2="321.6" y2="598"/><text class="coord halo" x="321.6" y="16" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="418.4" y1="24" x2="418.4" y2="598"/><text class="coord halo" x="418.4" y="16" text-anchor="middle">0x10C0</text><line class="cs-rcb" x1="515.2" y1="24" x2="515.2" y2="598"/><text class="coord halo" x="515.2" y="16" text-anchor="middle">0x1100</text><line class="cs-rcb" x1="612.0" y1="24" x2="612.0" y2="598"/><text class="coord halo" x="612.0" y="16" text-anchor="middle">0x1140</text><line class="cs-req" x1="152.2" y1="24" x2="152.2" y2="598"/><line class="cs-req" x1="539.4" y1="24" x2="539.4" y2="598"/><text class="legend halo" x="136" y="45" font-weight="700">1 completion: 1 split</text><g class="st-faded"><text class="coord halo" x="118" y="69" text-anchor="end">256</text><rect class="cs-bad" x="152.2" y="54" width="387.2" height="22" rx="3"><title>0x1010–0x110F: 256 bytes (one)</title></rect><text class="cs-size" x="345.8" y="69" text-anchor="middle">256</text></g><text class="legend halo" x="136" y="97" font-weight="700">2 completions: 4 splits</text><g class="st-faded"><text class="coord halo" x="118" y="121" text-anchor="end">240+16</text><rect class="cs-bad" x="152.2" y="106" width="363.0" height="22" rx="3"><title>0x1010–0x10FF: 240 bytes (first)</title></rect><text class="cs-size" x="333.7" y="121" text-anchor="middle">240</text><rect class="cs-last" x="515.2" y="106" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="121" text-anchor="middle">16</text></g><g class="st-faded"><text class="coord halo" x="118" y="149" text-anchor="end">176+80</text><rect class="cs-bad" x="152.2" y="134" width="266.2" height="22" rx="3"><title>0x1010–0x10BF: 176 bytes (first)</title></rect><text class="cs-size" x="285.3" y="149" text-anchor="middle">176</text><rect class="cs-last" x="418.4" y="134" width="121.0" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="478.9" y="149" text-anchor="middle">80</text></g><g class="st-faded"><text class="coord halo" x="118" y="177" text-anchor="end">112+144</text><rect class="cs-first" x="152.2" y="162" width="169.4" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="236.9" y="177" text-anchor="middle">112</text><rect class="cs-bad" x="321.6" y="162" width="217.8" height="22" rx="3"><title>0x1080–0x110F: 144 bytes (last)</title></rect><text class="cs-size" x="430.5" y="177" text-anchor="middle">144</text></g><g class="st-faded"><text class="coord halo" x="118" y="205" text-anchor="end">48+208</text><rect class="cs-first" x="152.2" y="190" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="205" text-anchor="middle">48</text><rect class="cs-bad" x="224.8" y="190" width="314.6" height="22" rx="3"><title>0x1040–0x110F: 208 bytes (last)</title></rect><text class="cs-size" x="382.1" y="205" text-anchor="middle">208</text></g><text class="legend halo" x="136" y="233" font-weight="700">3 completions: 6 splits</text><g class="st-faded"><text class="coord halo" x="118" y="257" text-anchor="end">176+64+16</text><rect class="cs-bad" x="152.2" y="242" width="266.2" height="22" rx="3"><title>0x1010–0x10BF: 176 bytes (first)</title></rect><text class="cs-size" x="285.3" y="257" text-anchor="middle">176</text><rect class="cs-mid" x="418.4" y="242" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="466.8" y="257" text-anchor="middle">64</text><rect class="cs-last" x="515.2" y="242" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="257" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="285" text-anchor="end">112+128+16</text><rect class="cs-first" x="152.2" y="270" width="169.4" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="236.9" y="285" text-anchor="middle">112</text><rect class="cs-mid" x="321.6" y="270" width="193.6" height="22" rx="3"><title>0x1080–0x10FF: 128 bytes (mid)</title></rect><text class="cs-size" x="418.4" y="285" text-anchor="middle">128</text><rect class="cs-last" x="515.2" y="270" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="285" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="313" text-anchor="end">112+64+80</text><rect class="cs-first" x="152.2" y="298" width="169.4" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="236.9" y="313" text-anchor="middle">112</text><rect class="cs-mid" x="321.6" y="298" width="96.8" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="313" text-anchor="middle">64</text><rect class="cs-last" x="418.4" y="298" width="121.0" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="478.9" y="313" text-anchor="middle">80</text></g><g class="st-faded"><text class="coord halo" x="118" y="341" text-anchor="end">48+192+16</text><rect class="cs-first" x="152.2" y="326" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="341" text-anchor="middle">48</text><rect class="cs-bad" x="224.8" y="326" width="290.4" height="22" rx="3"><title>0x1040–0x10FF: 192 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="341" text-anchor="middle">192</text><rect class="cs-last" x="515.2" y="326" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="341" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="369" text-anchor="end">48+128+80</text><rect class="cs-first" x="152.2" y="354" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="369" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="354" width="193.6" height="22" rx="3"><title>0x1040–0x10BF: 128 bytes (mid)</title></rect><text class="cs-size" x="321.6" y="369" text-anchor="middle">128</text><rect class="cs-last" x="418.4" y="354" width="121.0" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="478.9" y="369" text-anchor="middle">80</text></g><g class="st-faded"><text class="coord halo" x="118" y="397" text-anchor="end">48+64+144</text><rect class="cs-first" x="152.2" y="382" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="397" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="382" width="96.8" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="273.2" y="397" text-anchor="middle">64</text><rect class="cs-bad" x="321.6" y="382" width="217.8" height="22" rx="3"><title>0x1080–0x110F: 144 bytes (last)</title></rect><text class="cs-size" x="430.5" y="397" text-anchor="middle">144</text></g><text class="legend halo" x="136" y="425" font-weight="700">4 completions: 4 splits</text><g><text class="coord halo" x="118" y="449" text-anchor="end">112+64+64+16</text><rect class="cs-first" x="152.2" y="434" width="169.4" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="236.9" y="449" text-anchor="middle">112</text><rect class="cs-mid" x="321.6" y="434" width="96.8" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="449" text-anchor="middle">64</text><rect class="cs-mid" x="418.4" y="434" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="466.8" y="449" text-anchor="middle">64</text><rect class="cs-last" x="515.2" y="434" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="449" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="477" text-anchor="end">48+128+64+16</text><rect class="cs-first" x="152.2" y="462" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="477" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="462" width="193.6" height="22" rx="3"><title>0x1040–0x10BF: 128 bytes (mid)</title></rect><text class="cs-size" x="321.6" y="477" text-anchor="middle">128</text><rect class="cs-mid" x="418.4" y="462" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="466.8" y="477" text-anchor="middle">64</text><rect class="cs-last" x="515.2" y="462" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="477" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="505" text-anchor="end">48+64+128+16</text><rect class="cs-first" x="152.2" y="490" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="505" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="490" width="96.8" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="273.2" y="505" text-anchor="middle">64</text><rect class="cs-mid" x="321.6" y="490" width="193.6" height="22" rx="3"><title>0x1080–0x10FF: 128 bytes (mid)</title></rect><text class="cs-size" x="418.4" y="505" text-anchor="middle">128</text><rect class="cs-last" x="515.2" y="490" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="505" text-anchor="middle">16</text></g><g><text class="coord halo" x="118" y="533" text-anchor="end">48+64+64+80</text><rect class="cs-first" x="152.2" y="518" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="533" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="518" width="96.8" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="273.2" y="533" text-anchor="middle">64</text><rect class="cs-mid" x="321.6" y="518" width="96.8" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="533" text-anchor="middle">64</text><rect class="cs-last" x="418.4" y="518" width="121.0" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="478.9" y="533" text-anchor="middle">80</text></g><text class="legend halo" x="136" y="561" font-weight="700">5 completions: 1 split</text><g><text class="coord halo" x="118" y="585" text-anchor="end">48+64+64+64+16</text><rect class="cs-first" x="152.2" y="570" width="72.6" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="188.5" y="585" text-anchor="middle">48</text><rect class="cs-mid" x="224.8" y="570" width="96.8" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="273.2" y="585" text-anchor="middle">64</text><rect class="cs-mid" x="321.6" y="570" width="96.8" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="585" text-anchor="middle">64</text><rect class="cs-mid" x="418.4" y="570" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="466.8" y="585" text-anchor="middle">64</text><rect class="cs-last" x="515.2" y="570" width="24.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size" x="527.3" y="585" text-anchor="middle">16</text></g></svg>

    <span class="viz-legend"><span><i class="cs-first"></i>ה-Completion הראשון (או היחיד)</span><span><i class="cs-mid"></i>אמצעי</span><span><i class="cs-last"></i>אחרון</span><span><i class="cs-bad"></i>גדול מ-MPS, הפיצול נפסל</span></span>

    | הפיצול | ה-Completion הגדול ביותר | ‏MPS = 256 | ‏MPS = 128 |
    |---|:-:|:-:|:-:|
    | ‏256 | 256 | ✓ | ✗ |
    | ‏240+16 | 240 | ✓ | ✗ |
    | ‏176+80 | 176 | ✓ | ✗ |
    | ‏176+64+16 | 176 | ✓ | ✗ |
    | ‏112+144 | 144 | ✓ | ✗ |
    | ‏112+128+16 | 128 | ✓ | ✓ |
    | ‏112+64+80 | 112 | ✓ | ✓ |
    | ‏112+64+64+16 | 112 | ✓ | ✓ |
    | ‏48+208 | 208 | ✓ | ✗ |
    | ‏48+192+16 | 192 | ✓ | ✗ |
    | ‏48+128+80 | 128 | ✓ | ✓ |
    | ‏48+128+64+16 | 128 | ✓ | ✓ |
    | ‏48+64+144 | 144 | ✓ | ✗ |
    | ‏48+64+128+16 | 128 | ✓ | ✓ |
    | ‏48+64+64+80 | 80 | ✓ | ✓ |
    | ‏48+64+64+64+16 | 64 | ✓ | ✓ |
    | **סך הכול** | | **16** | **8** |

    **עץ הרקורסיה** לאותה בקשה עם `RCB = 128` (גבולות בתוך הבקשה: ‏`0x1080` ו-`0x1100`),
    פעם עם `MPS = 256` ופעם עם `MPS = 128`. על כל קשת: גודל ה-Completion והכתובת שאליה
    מגיעים. הצמתים המקווקווים הם הענפים שנגזמים כש-MPS הוא 128, כי הסיום רחוק מדי:

    ```mermaid
    flowchart TD
        r["pos = 0x1010<br/>sizes = [ ]"]
        r -- "256 → 0x1110" --> a["[256] ✓"]
        r -- "240 → 0x1100" --> b["pos = 0x1100<br/>sizes = [240]"]
        r -- "112 → 0x1080" --> c["pos = 0x1080<br/>sizes = [112]"]
        b -- "16 → 0x1110" --> b1["[240, 16] ✓"]
        c -- "144 → 0x1110" --> c1["[112, 144] ✓"]
        c -- "128 → 0x1100" --> c2["pos = 0x1100<br/>sizes = [112, 128]"]
        c2 -- "16 → 0x1110" --> c3["[112, 128, 16] ✓"]
        classDef pruned stroke-dasharray: 5 4,opacity:0.55;
        classDef found stroke:#1baf7a,stroke-width:3px;
        class a,b,b1,c1 pruned;
        class c3 found;
    ```

    עם `MPS = 128` נשאר פיצול אחד, `[112, 128, 16]`: מ-`0x1010` אפשר להגיע רק עד `0x1090`,
    ולכן הסיום היחיד הוא הגבול `0x1080`; משם מגיעים עד `0x1100`, וסוף הבקשה `0x1110` עדיין
    רחוק מדי.

    #### סיבוכיות { .sol-cost }

    - **זמן:** תלוי בגודל הפלט. יש לכל היותר \( 2^c \) פיצולים, וכל אחד מועתק (עד \( c + 1 \)
      גדלים) כשהוא נשמר, כלומר \( O(c \cdot 2^c) \) במקרה הגרוע, כש-MPS לא גוזם כלום. בכל
      צומת של הרקורסיה נבדקים לכל היותר \( MPS / RCB + 1 \) סיומים.
    - **בפועל:** לבקשות של ראיון (עד 512 בתים) מדובר בעשרות עד מאות פיצולים. לבקשה של
      4 KB עם `RCB = 64` יש \( c = 63 \) גבולות, ומנייה מלאה לא אפשרית; אז סופרים בלי למנות
      (ראו שאלות ההמשך) או מגרילים פיצול אחד.
    - **זיכרון:** התוצאה עצמה, ועומק רקורסיה של עד \( c + 1 \).

    **נסו בעצמכם.** שנו את הכתובת, את האורך, את MPS ואת RCB: התיבה מציירת את הבלוקים
    של הבקשה על רשת ה-RCB, סופרת את הפיצולים (ומשווה לנוסחה הסגורה של
    [שאלה 0021](0021-pcie-completion-count.md)), ומציירת את מפת הפיצולים כמו למעלה, עד
    ארבעים שורות. הדוגמאות מהדף נמצאות ברשימה.

    <div class="explorer" data-kind="pcie" data-addr="0x1010" data-len="256" data-mps="256" data-rcb="64"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: לקרוא את הגדלים הפוך"
    אם `[48, 64, 144]` חוקי, למה `[144, 64, 48]` לא? כי החוקים הם על **כתובות**, לא על
    גדלים. ה-Completions חוזרים בסדר כתובות עולה, ולכן `[144, 64, 48]` מ-`0x1010` חותך
    ב-`0x10A0` וב-`0x10E0`, ואף אחת מהן לא כפולה של 64. הבקשה לא סימטרית: ה"שבר" של 48
    בתים נמצא בהתחלה (עד הגבול `0x1040`) והשבר של 16 בסוף (מהגבול `0x1100`). בדיקה נכונה
    של פיצול שקיבלתם ממירה את הגדלים לכתובות חיתוך ובודקת \( cut \bmod RCB = 0 \).

??? trap "מלכודת: לפצל לפי MPS במקום לפי RCB"
    עם `MPS = 128` מפתה לענות `[128, 128]`: שני Completions "מלאים". מ-`0x1010` זה חותך
    ב-`0x1090`, שאינו גבול RCB, ולכן פסול. המינימום בכתובת לא מיושרת הוא **שלושה**
    Completions, למשל `[112, 128, 16]`. ה-MPS קובע את המינימום רק דרך הגבולות שבהישג יד;
    הוא לא נקודת חיתוך בעצמו.

??? trap "מלכודת: לבלבל MRRS עם MPS"
    ‏MRRS שייך לצד ה-Requester ומגביל את **הבקשה**; MPS מגביל כל **Completion**. השניים
    בלתי תלויים: עם `MRRS = 512` ו-`MPS = 256` בקשה אחת של 512 בתים חוקית, והיא תיענה
    בלפחות שני Completions. ואם הקריאה גדולה מ-MRRS (או חוצה 4 KB), ה-Requester מפצל אותה
    לכמה בקשות עם Tag שונה לכל אחת, וה-Completer לעולם לא מאחד Completions של בקשות שונות.

??? followup "שאלות המשך"
    - **לספור בלי למנות:** כמה פיצולים יש לבקשה של 4 KB? תכנון דינמי: \( ways(end) = 1 \)
      ו-\( ways(pos) = \sum ways(cut) \) על כל הסיומים המותרים מ-`pos`; \( O(c \cdot MPS / RCB) \)
      במקום \( 2^c \). כש-\( MPS \ge len \) מקבלים \( 2^c \) בדיוק. הנוסחה הסגורה וההוכחה
      שלה נמצאות בשאלה [0021](0021-pcie-completion-count.md).
    - **המינימום והמקסימום בנוסחה:** המקסימום הוא \( c + 1 \). המינימום הוא החמדני: בכל
      צעד הסיום הרחוק ביותר שבהישג יד. למה החמדני אופטימלי כאן?
    - **שדות ה-header:** לכל Completion יש `Length` ב-DW, `Byte Count` (כמה בתים נשארו כולל
      הנוכחי) ו-`Lower Address` (7 הביטים התחתונים של הבית הראשון). כתבו את שלושתם עבור
      `[48, 64, 64, 64, 16]` מ-`0x1010`. (Byte Count: 256, 208, 144, 80, 16.) איך ה-Requester
      יודע שהגיע ה-Completion האחרון?
    - **‏Scoreboard ו-coverage:** איך בודקים רצף Completions שהתקבל בסימולציה בלי לייצר את
      כל הרשימה? (כתובות החיתוך כפולות של RCB, כל Completion עד MPS, ‏Byte Count יורד
      בעקביות, הסכום שווה ל-`len`.) ואילו bins כדאי להגדיר? (מספר ה-Completions, גודל
      הראשון, האם היה Completion בגודל MPS מלא, Completion אחרון של 16 בתים.)
    - **מי קובע את ה-RCB:** ב-Root Port הביט ב-Link Control הוא לקריאה בלבד (64 או 128);
      ב-Endpoint התוכנה מגדירה אותו כדי לשקף את ה-Root Port שמעליו. למה ל-Requester חשוב
      לדעת את ה-RCB של ה-Completer? (הקצאת באפרים ל-\( c + 1 \) headers לכל בקשה.)
