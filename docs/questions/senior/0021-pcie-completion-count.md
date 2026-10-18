---
id: 21
title: כמה פיצולי Completions יש לקריאה ב-PCIe – ספירה, ונוסחה כללית עם הוכחה
level: senior
difficulty: medium
tags: [protocols, pcie, combinatorics, math, proof]
source: ""
added: 2026-10-18
---

## השאלה

כמו בשאלה [0020](0020-pcie-completion-splits.md): ה-Requester שולח בקשת קריאה של \( L \)
בתים מכתובת \( A \) (עם \( L \le MRRS \), בלי לחצות גבול 4 KB), וה-Completer מחזיר את המידע
ברצף של Completions לפי חוקי ה-SPEC:

1. ה-Completions מכסים את הטווח \( [A, A + L) \) ברצף, בסדר כתובות עולה, בלי חפיפה.
2. ה-Completion הראשון מתחיל ב-\( A \) והאחרון מסתיים ב-\( A + L \).
3. כל נקודת חיתוך בין שני Completions היא כפולה של RCB.
4. אף Completion לא גדול מ-MPS.

הפעם **לא** מבקשים לרשום את הפיצולים, אלא **לספור** אותם. בכל הסעיפים
‏\( MPS = 256 \) ו-\( RCB = 64 \) (כל הפרמטרים חזקות של 2, ו-\( MPS \ge RCB \)).

??? interviewer "מה המראיין בודק"
    - **מודל נכון:** האם המועמד מתרגם את חוקי הפרוטוקול לאובייקט קומבינטורי (תת-קבוצות של
      גבולות, או הרכבות של בלוקים) במקום לנסות לרשום פיצולים.
    - **מתי MPS משנה:** האם הוא שם לב שבבקשה של 256 בתים MPS לא מגביל כלום, ובבקשה של 512
      הוא מגביל, ומה זה עושה לספירה.
    - **יישור:** האם הוא סופר בלוקים ולא בתים, ורואה שכתובת לא מיושרת מוסיפה בלוק.
    - **רקורסיה וסגירה:** האם הוא מגיע לנוסחת נסיגה, יודע להצדיק אותה, ובבונוס לסגור אותה
      לנוסחה מפורשת ולטפל במקרה הקצה.

---

### סעיף א – שתי בקשות של 256 בתים

כמה רצפי Completions חוקיים יש לכל אחת מהבקשות:

1. ‏\( A = \texttt{0x1000} \), ‏\( L = 256 \) (כתובת מיושרת ל-RCB).
2. ‏\( A = \texttt{0x1010} \), ‏\( L = 256 \) (כתובת לא מיושרת).

??? tip "רמז 1"
    כמה גבולות RCB יש **בתוך** כל בקשה? מה ההחלטה שמקבלים בכל גבול כזה?

??? tip "רמז 2"
    האם יש Completion שיכול לחרוג מ-MPS כש-\( L \le MPS \)? אם לא, כל צירוף של החלטות
    חוקי.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        בכתובת המיושרת **8** פיצולים (\( 2^3 \)), בכתובת הלא מיושרת **16** (\( 2^4 \)). כש-\( L \le MPS \)
        כל תת-קבוצה של הגבולות הפנימיים היא פיצול חוקי, והכתובת הלא מיושרת נוגעת בבלוק אחד
        יותר, ולכן יש לה גבול פנימי אחד יותר ופי שניים פיצולים.

    #### הרעיון { .sol-idea }

    חוקים 1 עד 3 אומרים שפיצול נקבע **רק** על ידי קבוצת נקודות החיתוך שלו, וכל נקודת חיתוך
    היא גבול RCB שנמצא ממש בתוך הבקשה. אם נסמן ב-\( \mathcal{B} \) את קבוצת הגבולות
    הפנימיים, כל תת-קבוצה \( X \subseteq \mathcal{B} \) היא פיצול (חותכים בדיוק בנקודות של
    \( X \)), ופיצולים שונים נותנים תת-קבוצות שונות. בלי חוק 4 התשובה היא לכן
    \( 2^{|\mathcal{B}|} \).

    חוק 4 יכול רק לפסול תת-קבוצות: כאלה שבהן שני חיתוכים עוקבים (או קצה הבקשה וחיתוך)
    רחוקים יותר מ-MPS. אבל כל Completion הוא חלק מהבקשה, ולכן אורכו לכל היותר \( L \). אם
    \( L \le MPS \), אף Completion לא יכול לחרוג, **שום** תת-קבוצה לא נפסלת, והתשובה היא
    \( 2^{|\mathcal{B}|} \) בדיוק. בשני המקרים כאן \( L = 256 = MPS \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הבלוקים:** מציירים את הבקשה על רשת של 64 בתים וסופרים כמה בלוקים \( N \) היא נוגעת
       בהם. מספר הגבולות הפנימיים הוא \( N - 1 \).
    2. **מיושרת:** ‏\( \texttt{0x1000} \) עד \( \texttt{0x10FF} \): ארבעה בלוקים מלאים של 64,
       שלושה גבולות פנימיים (‏\( \texttt{0x1040} \), ‏\( \texttt{0x1080} \), ‏\( \texttt{0x10C0} \)).
    3. **לא מיושרת:** ‏\( \texttt{0x1010} \) עד \( \texttt{0x110F} \): בלוק ראשון של 48 בתים,
       שלושה בלוקים מלאים, ובלוק אחרון של 16: חמישה בלוקים, ארבעה גבולות פנימיים (נוסף
       ‏\( \texttt{0x1100} \)).
    4. **‏MPS:** ‏\( L = 256 \le MPS \), ולכן אף תת-קבוצה לא נפסלת.
    5. **הספירה:** ‏\( 2^3 = 8 \) ו-\( 2^4 = 16 \).

    </div>

    #### למה זה נכון { .sol-proof }

    **מבנה הבלוקים.** בשתי הבקשות אותו אורך, אבל הכתובת הלא מיושרת "שופכת" את 256 הבתים על
    חמישה בלוקים במקום ארבעה:

    <svg class="figure cs-fig" viewBox="0 0 640 132" style="max-width:40rem" role="img" aria-label="בקשה של 256 בתים מכתובת 0x1000 על רשת RCB של 64: 4 בלוקים, 3 גבולות פנימיים"><line class="cs-rcb" x1="40.0" y1="26" x2="40.0" y2="96"/><text class="coord halo" x="40.0" y="16" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="152.0" y1="26" x2="152.0" y2="96"/><text class="coord halo" x="152.0" y="16" text-anchor="middle">0x1040</text><line class="cs-rcb" x1="264.0" y1="26" x2="264.0" y2="96"/><text class="coord halo" x="264.0" y="16" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="376.0" y1="26" x2="376.0" y2="96"/><text class="coord halo" x="376.0" y="16" text-anchor="middle">0x10C0</text><line class="cs-rcb" x1="488.0" y1="26" x2="488.0" y2="96"/><text class="coord halo" x="488.0" y="16" text-anchor="middle">0x1100</text><line class="cs-rcb" x1="600.0" y1="26" x2="600.0" y2="96"/><text class="coord halo" x="600.0" y="16" text-anchor="middle">0x1140</text><line class="cs-req" x1="40.0" y1="26" x2="40.0" y2="96"/><line class="cs-req" x1="488.0" y1="26" x2="488.0" y2="96"/><rect class="cs-first" x="40.0" y="50" width="112.0" height="28" rx="3"><title>block 1: 0x1000–0x103F, 64 bytes</title></rect><text class="cs-size" x="96.0" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="152.0" y="50" width="112.0" height="28" rx="3"><title>block 2: 0x1040–0x107F, 64 bytes</title></rect><text class="cs-size" x="208.0" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="264.0" y="50" width="112.0" height="28" rx="3"><title>block 3: 0x1080–0x10BF, 64 bytes</title></rect><text class="cs-size" x="320.0" y="68.5" text-anchor="middle">64</text><rect class="cs-last" x="376.0" y="50" width="112.0" height="28" rx="3"><title>block 4: 0x10C0–0x10FF, 64 bytes</title></rect><text class="cs-size" x="432.0" y="68.5" text-anchor="middle">64</text><circle class="cs-can" cx="152.0" cy="50" r="4"><title>boundary 0x1040</title></circle><circle class="cs-can" cx="264.0" cy="50" r="4"><title>boundary 0x1080</title></circle><circle class="cs-can" cx="376.0" cy="50" r="4"><title>boundary 0x10C0</title></circle><text class="legend" x="40" y="118">N = 4, |B| = 3, f = 64, e = 64, m = MPS / RCB = 4, δ = 0</text></svg>

    <svg class="figure cs-fig" viewBox="0 0 640 132" style="max-width:40rem" role="img" aria-label="בקשה של 256 בתים מכתובת 0x1010 על רשת RCB של 64: 5 בלוקים, 4 גבולות פנימיים"><line class="cs-rcb" x1="40.0" y1="26" x2="40.0" y2="96"/><text class="coord halo" x="40.0" y="16" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="133.3" y1="26" x2="133.3" y2="96"/><text class="coord halo" x="133.3" y="16" text-anchor="middle">0x1040</text><line class="cs-rcb" x1="226.7" y1="26" x2="226.7" y2="96"/><text class="coord halo" x="226.7" y="16" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="320.0" y1="26" x2="320.0" y2="96"/><text class="coord halo" x="320.0" y="16" text-anchor="middle">0x10C0</text><line class="cs-rcb" x1="413.3" y1="26" x2="413.3" y2="96"/><text class="coord halo" x="413.3" y="16" text-anchor="middle">0x1100</text><line class="cs-rcb" x1="506.7" y1="26" x2="506.7" y2="96"/><text class="coord halo" x="506.7" y="16" text-anchor="middle">0x1140</text><line class="cs-rcb" x1="600.0" y1="26" x2="600.0" y2="96"/><text class="coord halo" x="600.0" y="16" text-anchor="middle">0x1180</text><line class="cs-req" x1="63.3" y1="26" x2="63.3" y2="96"/><line class="cs-req" x1="436.7" y1="26" x2="436.7" y2="96"/><rect class="cs-first" x="63.3" y="50" width="70.0" height="28" rx="3"><title>block 1: 0x1010–0x103F, 48 bytes</title></rect><text class="cs-size" x="98.3" y="68.5" text-anchor="middle">48</text><rect class="cs-mid" x="133.3" y="50" width="93.3" height="28" rx="3"><title>block 2: 0x1040–0x107F, 64 bytes</title></rect><text class="cs-size" x="180.0" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="226.7" y="50" width="93.3" height="28" rx="3"><title>block 3: 0x1080–0x10BF, 64 bytes</title></rect><text class="cs-size" x="273.3" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="320.0" y="50" width="93.3" height="28" rx="3"><title>block 4: 0x10C0–0x10FF, 64 bytes</title></rect><text class="cs-size" x="366.7" y="68.5" text-anchor="middle">64</text><rect class="cs-last" x="413.3" y="50" width="23.3" height="28" rx="3"><title>block 5: 0x1100–0x110F, 16 bytes</title></rect><text class="cs-size" x="425.0" y="68.5" text-anchor="middle">16</text><circle class="cs-can" cx="133.3" cy="50" r="4"><title>boundary 0x1040</title></circle><circle class="cs-can" cx="226.7" cy="50" r="4"><title>boundary 0x1080</title></circle><circle class="cs-can" cx="320.0" cy="50" r="4"><title>boundary 0x10C0</title></circle><circle class="cs-can" cx="413.3" cy="50" r="4"><title>boundary 0x1100</title></circle><text class="legend" x="40" y="118">N = 5, |B| = 4, f = 48, e = 16, m = MPS / RCB = 4, δ = 1 (N = m + 1 and L ≤ MPS)</text></svg>

    <span class="viz-legend"><span><i class="cs-first"></i>הבלוק הראשון, f בתים</span><span><i class="cs-mid"></i>בלוק מלא, RCB בתים</span><span><i class="cs-last"></i>הבלוק האחרון, e בתים</span><span><i class="cs-can"></i>גבול פנימי: כאן מותר לחתוך</span></span>

    **כל הפיצולים.** שמונה תת-קבוצות של שלושה גבולות, ושש-עשרה של ארבעה. באף שורה אין
    Completion גדול מ-256, כי כל הבקשה היא 256:

    <svg class="figure cs-fig" viewBox="0 0 640 354" style="max-width:40rem" role="img" aria-label="כל 8 הפיצולים החוקיים של בקשה של 256 בתים מכתובת 0x1000 עם MPS = 256 ו-RCB = 64, שורה לכל פיצול"><line class="cs-rcb" x1="128.0" y1="24" x2="128.0" y2="350"/><text class="coord halo" x="128.0" y="16" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="224.8" y1="24" x2="224.8" y2="350"/><text class="coord halo" x="224.8" y="16" text-anchor="middle">0x1040</text><line class="cs-rcb" x1="321.6" y1="24" x2="321.6" y2="350"/><text class="coord halo" x="321.6" y="16" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="418.4" y1="24" x2="418.4" y2="350"/><text class="coord halo" x="418.4" y="16" text-anchor="middle">0x10C0</text><line class="cs-rcb" x1="515.2" y1="24" x2="515.2" y2="350"/><text class="coord halo" x="515.2" y="16" text-anchor="middle">0x1100</text><line class="cs-rcb" x1="612.0" y1="24" x2="612.0" y2="350"/><text class="coord halo" x="612.0" y="16" text-anchor="middle">0x1140</text><line class="cs-req" x1="128.0" y1="24" x2="128.0" y2="350"/><line class="cs-req" x1="515.2" y1="24" x2="515.2" y2="350"/><text class="legend halo" x="136" y="45" font-weight="700">1 completion: 1 split</text><text class="coord halo" x="118" y="69" text-anchor="end">256</text><rect class="cs-one" x="128.0" y="54" width="387.2" height="22" rx="3"><title>0x1000–0x10FF: 256 bytes (one)</title></rect><text class="cs-size" x="321.6" y="69.5" text-anchor="middle">256</text><text class="legend halo" x="136" y="97" font-weight="700">2 completions: 3 splits</text><text class="coord halo" x="118" y="121" text-anchor="end">192+64</text><rect class="cs-first" x="128.0" y="106" width="290.4" height="22" rx="3"><title>0x1000–0x10BF: 192 bytes (first)</title></rect><text class="cs-size" x="273.2" y="121.5" text-anchor="middle">192</text><rect class="cs-last" x="418.4" y="106" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (last)</title></rect><text class="cs-size" x="466.8" y="121.5" text-anchor="middle">64</text><text class="coord halo" x="118" y="149" text-anchor="end">128+128</text><rect class="cs-first" x="128.0" y="134" width="193.6" height="22" rx="3"><title>0x1000–0x107F: 128 bytes (first)</title></rect><text class="cs-size" x="224.8" y="149.5" text-anchor="middle">128</text><rect class="cs-last" x="321.6" y="134" width="193.6" height="22" rx="3"><title>0x1080–0x10FF: 128 bytes (last)</title></rect><text class="cs-size" x="418.4" y="149.5" text-anchor="middle">128</text><text class="coord halo" x="118" y="177" text-anchor="end">64+192</text><rect class="cs-first" x="128.0" y="162" width="96.8" height="22" rx="3"><title>0x1000–0x103F: 64 bytes (first)</title></rect><text class="cs-size" x="176.4" y="177.5" text-anchor="middle">64</text><rect class="cs-last" x="224.8" y="162" width="290.4" height="22" rx="3"><title>0x1040–0x10FF: 192 bytes (last)</title></rect><text class="cs-size" x="370.0" y="177.5" text-anchor="middle">192</text><text class="legend halo" x="136" y="205" font-weight="700">3 completions: 3 splits</text><text class="coord halo" x="118" y="229" text-anchor="end">128+64+64</text><rect class="cs-first" x="128.0" y="214" width="193.6" height="22" rx="3"><title>0x1000–0x107F: 128 bytes (first)</title></rect><text class="cs-size" x="224.8" y="229.5" text-anchor="middle">128</text><rect class="cs-mid" x="321.6" y="214" width="96.8" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="229.5" text-anchor="middle">64</text><rect class="cs-last" x="418.4" y="214" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (last)</title></rect><text class="cs-size" x="466.8" y="229.5" text-anchor="middle">64</text><text class="coord halo" x="118" y="257" text-anchor="end">64+128+64</text><rect class="cs-first" x="128.0" y="242" width="96.8" height="22" rx="3"><title>0x1000–0x103F: 64 bytes (first)</title></rect><text class="cs-size" x="176.4" y="257.5" text-anchor="middle">64</text><rect class="cs-mid" x="224.8" y="242" width="193.6" height="22" rx="3"><title>0x1040–0x10BF: 128 bytes (mid)</title></rect><text class="cs-size" x="321.6" y="257.5" text-anchor="middle">128</text><rect class="cs-last" x="418.4" y="242" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (last)</title></rect><text class="cs-size" x="466.8" y="257.5" text-anchor="middle">64</text><text class="coord halo" x="118" y="285" text-anchor="end">64+64+128</text><rect class="cs-first" x="128.0" y="270" width="96.8" height="22" rx="3"><title>0x1000–0x103F: 64 bytes (first)</title></rect><text class="cs-size" x="176.4" y="285.5" text-anchor="middle">64</text><rect class="cs-mid" x="224.8" y="270" width="96.8" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="273.2" y="285.5" text-anchor="middle">64</text><rect class="cs-last" x="321.6" y="270" width="193.6" height="22" rx="3"><title>0x1080–0x10FF: 128 bytes (last)</title></rect><text class="cs-size" x="418.4" y="285.5" text-anchor="middle">128</text><text class="legend halo" x="136" y="313" font-weight="700">4 completions: 1 split</text><text class="coord halo" x="118" y="337" text-anchor="end">64+64+64+64</text><rect class="cs-first" x="128.0" y="322" width="96.8" height="22" rx="3"><title>0x1000–0x103F: 64 bytes (first)</title></rect><text class="cs-size" x="176.4" y="337.5" text-anchor="middle">64</text><rect class="cs-mid" x="224.8" y="322" width="96.8" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="273.2" y="337.5" text-anchor="middle">64</text><rect class="cs-mid" x="321.6" y="322" width="96.8" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="337.5" text-anchor="middle">64</text><rect class="cs-last" x="418.4" y="322" width="96.8" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (last)</title></rect><text class="cs-size" x="466.8" y="337.5" text-anchor="middle">64</text></svg>

    <svg class="figure cs-fig" viewBox="0 0 640 602" style="max-width:40rem" role="img" aria-label="כל 16 הפיצולים החוקיים של בקשה של 256 בתים מכתובת 0x1010 עם MPS = 256 ו-RCB = 64, שורה לכל פיצול"><line class="cs-rcb" x1="128.0" y1="24" x2="128.0" y2="598"/><text class="coord halo" x="128.0" y="16" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="208.7" y1="24" x2="208.7" y2="598"/><text class="coord halo" x="208.7" y="16" text-anchor="middle">0x1040</text><line class="cs-rcb" x1="289.3" y1="24" x2="289.3" y2="598"/><text class="coord halo" x="289.3" y="16" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="370.0" y1="24" x2="370.0" y2="598"/><text class="coord halo" x="370.0" y="16" text-anchor="middle">0x10C0</text><line class="cs-rcb" x1="450.7" y1="24" x2="450.7" y2="598"/><text class="coord halo" x="450.7" y="16" text-anchor="middle">0x1100</text><line class="cs-rcb" x1="531.3" y1="24" x2="531.3" y2="598"/><text class="coord halo" x="531.3" y="16" text-anchor="middle">0x1140</text><line class="cs-rcb" x1="612.0" y1="24" x2="612.0" y2="598"/><text class="coord halo" x="612.0" y="16" text-anchor="middle">0x1180</text><line class="cs-req" x1="148.2" y1="24" x2="148.2" y2="598"/><line class="cs-req" x1="470.8" y1="24" x2="470.8" y2="598"/><text class="legend halo" x="136" y="45" font-weight="700">1 completion: 1 split</text><text class="coord halo" x="118" y="69" text-anchor="end">256</text><rect class="cs-one" x="148.2" y="54" width="322.7" height="22" rx="3"><title>0x1010–0x110F: 256 bytes (one)</title></rect><text class="cs-size" x="309.5" y="69.5" text-anchor="middle">256</text><text class="legend halo" x="136" y="97" font-weight="700">2 completions: 4 splits</text><text class="coord halo" x="118" y="121" text-anchor="end">240+16</text><rect class="cs-first" x="148.2" y="106" width="302.5" height="22" rx="3"><title>0x1010–0x10FF: 240 bytes (first)</title></rect><text class="cs-size" x="299.4" y="121.5" text-anchor="middle">240</text><rect class="cs-last" x="450.7" y="106" width="20.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size halo" x="460.8" y="101" text-anchor="middle">16</text><text class="coord halo" x="118" y="149" text-anchor="end">176+80</text><rect class="cs-first" x="148.2" y="134" width="221.8" height="22" rx="3"><title>0x1010–0x10BF: 176 bytes (first)</title></rect><text class="cs-size" x="259.1" y="149.5" text-anchor="middle">176</text><rect class="cs-last" x="370.0" y="134" width="100.8" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="420.4" y="149.5" text-anchor="middle">80</text><text class="coord halo" x="118" y="177" text-anchor="end">112+144</text><rect class="cs-first" x="148.2" y="162" width="141.2" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="218.8" y="177.5" text-anchor="middle">112</text><rect class="cs-last" x="289.3" y="162" width="181.5" height="22" rx="3"><title>0x1080–0x110F: 144 bytes (last)</title></rect><text class="cs-size" x="380.1" y="177.5" text-anchor="middle">144</text><text class="coord halo" x="118" y="205" text-anchor="end">48+208</text><rect class="cs-first" x="148.2" y="190" width="60.5" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="178.4" y="205.5" text-anchor="middle">48</text><rect class="cs-last" x="208.7" y="190" width="262.2" height="22" rx="3"><title>0x1040–0x110F: 208 bytes (last)</title></rect><text class="cs-size" x="339.8" y="205.5" text-anchor="middle">208</text><text class="legend halo" x="136" y="233" font-weight="700">3 completions: 6 splits</text><text class="coord halo" x="118" y="257" text-anchor="end">176+64+16</text><rect class="cs-first" x="148.2" y="242" width="221.8" height="22" rx="3"><title>0x1010–0x10BF: 176 bytes (first)</title></rect><text class="cs-size" x="259.1" y="257.5" text-anchor="middle">176</text><rect class="cs-mid" x="370.0" y="242" width="80.7" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="410.3" y="257.5" text-anchor="middle">64</text><rect class="cs-last" x="450.7" y="242" width="20.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size halo" x="460.8" y="237" text-anchor="middle">16</text><text class="coord halo" x="118" y="285" text-anchor="end">112+128+16</text><rect class="cs-first" x="148.2" y="270" width="141.2" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="218.8" y="285.5" text-anchor="middle">112</text><rect class="cs-mid" x="289.3" y="270" width="161.3" height="22" rx="3"><title>0x1080–0x10FF: 128 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="285.5" text-anchor="middle">128</text><rect class="cs-last" x="450.7" y="270" width="20.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size halo" x="460.8" y="265" text-anchor="middle">16</text><text class="coord halo" x="118" y="313" text-anchor="end">112+64+80</text><rect class="cs-first" x="148.2" y="298" width="141.2" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="218.8" y="313.5" text-anchor="middle">112</text><rect class="cs-mid" x="289.3" y="298" width="80.7" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="329.7" y="313.5" text-anchor="middle">64</text><rect class="cs-last" x="370.0" y="298" width="100.8" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="420.4" y="313.5" text-anchor="middle">80</text><text class="coord halo" x="118" y="341" text-anchor="end">48+192+16</text><rect class="cs-first" x="148.2" y="326" width="60.5" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="178.4" y="341.5" text-anchor="middle">48</text><rect class="cs-mid" x="208.7" y="326" width="242.0" height="22" rx="3"><title>0x1040–0x10FF: 192 bytes (mid)</title></rect><text class="cs-size" x="329.7" y="341.5" text-anchor="middle">192</text><rect class="cs-last" x="450.7" y="326" width="20.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size halo" x="460.8" y="321" text-anchor="middle">16</text><text class="coord halo" x="118" y="369" text-anchor="end">48+128+80</text><rect class="cs-first" x="148.2" y="354" width="60.5" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="178.4" y="369.5" text-anchor="middle">48</text><rect class="cs-mid" x="208.7" y="354" width="161.3" height="22" rx="3"><title>0x1040–0x10BF: 128 bytes (mid)</title></rect><text class="cs-size" x="289.3" y="369.5" text-anchor="middle">128</text><rect class="cs-last" x="370.0" y="354" width="100.8" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="420.4" y="369.5" text-anchor="middle">80</text><text class="coord halo" x="118" y="397" text-anchor="end">48+64+144</text><rect class="cs-first" x="148.2" y="382" width="60.5" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="178.4" y="397.5" text-anchor="middle">48</text><rect class="cs-mid" x="208.7" y="382" width="80.7" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="249.0" y="397.5" text-anchor="middle">64</text><rect class="cs-last" x="289.3" y="382" width="181.5" height="22" rx="3"><title>0x1080–0x110F: 144 bytes (last)</title></rect><text class="cs-size" x="380.1" y="397.5" text-anchor="middle">144</text><text class="legend halo" x="136" y="425" font-weight="700">4 completions: 4 splits</text><text class="coord halo" x="118" y="449" text-anchor="end">112+64+64+16</text><rect class="cs-first" x="148.2" y="434" width="141.2" height="22" rx="3"><title>0x1010–0x107F: 112 bytes (first)</title></rect><text class="cs-size" x="218.8" y="449.5" text-anchor="middle">112</text><rect class="cs-mid" x="289.3" y="434" width="80.7" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="329.7" y="449.5" text-anchor="middle">64</text><rect class="cs-mid" x="370.0" y="434" width="80.7" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="410.3" y="449.5" text-anchor="middle">64</text><rect class="cs-last" x="450.7" y="434" width="20.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size halo" x="460.8" y="429" text-anchor="middle">16</text><text class="coord halo" x="118" y="477" text-anchor="end">48+128+64+16</text><rect class="cs-first" x="148.2" y="462" width="60.5" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="178.4" y="477.5" text-anchor="middle">48</text><rect class="cs-mid" x="208.7" y="462" width="161.3" height="22" rx="3"><title>0x1040–0x10BF: 128 bytes (mid)</title></rect><text class="cs-size" x="289.3" y="477.5" text-anchor="middle">128</text><rect class="cs-mid" x="370.0" y="462" width="80.7" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="410.3" y="477.5" text-anchor="middle">64</text><rect class="cs-last" x="450.7" y="462" width="20.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size halo" x="460.8" y="457" text-anchor="middle">16</text><text class="coord halo" x="118" y="505" text-anchor="end">48+64+128+16</text><rect class="cs-first" x="148.2" y="490" width="60.5" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="178.4" y="505.5" text-anchor="middle">48</text><rect class="cs-mid" x="208.7" y="490" width="80.7" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="249.0" y="505.5" text-anchor="middle">64</text><rect class="cs-mid" x="289.3" y="490" width="161.3" height="22" rx="3"><title>0x1080–0x10FF: 128 bytes (mid)</title></rect><text class="cs-size" x="370.0" y="505.5" text-anchor="middle">128</text><rect class="cs-last" x="450.7" y="490" width="20.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size halo" x="460.8" y="485" text-anchor="middle">16</text><text class="coord halo" x="118" y="533" text-anchor="end">48+64+64+80</text><rect class="cs-first" x="148.2" y="518" width="60.5" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="178.4" y="533.5" text-anchor="middle">48</text><rect class="cs-mid" x="208.7" y="518" width="80.7" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="249.0" y="533.5" text-anchor="middle">64</text><rect class="cs-mid" x="289.3" y="518" width="80.7" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="329.7" y="533.5" text-anchor="middle">64</text><rect class="cs-last" x="370.0" y="518" width="100.8" height="22" rx="3"><title>0x10C0–0x110F: 80 bytes (last)</title></rect><text class="cs-size" x="420.4" y="533.5" text-anchor="middle">80</text><text class="legend halo" x="136" y="561" font-weight="700">5 completions: 1 split</text><text class="coord halo" x="118" y="585" text-anchor="end">48+64+64+64+16</text><rect class="cs-first" x="148.2" y="570" width="60.5" height="22" rx="3"><title>0x1010–0x103F: 48 bytes (first)</title></rect><text class="cs-size" x="178.4" y="585.5" text-anchor="middle">48</text><rect class="cs-mid" x="208.7" y="570" width="80.7" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="249.0" y="585.5" text-anchor="middle">64</text><rect class="cs-mid" x="289.3" y="570" width="80.7" height="22" rx="3"><title>0x1080–0x10BF: 64 bytes (mid)</title></rect><text class="cs-size" x="329.7" y="585.5" text-anchor="middle">64</text><rect class="cs-mid" x="370.0" y="570" width="80.7" height="22" rx="3"><title>0x10C0–0x10FF: 64 bytes (mid)</title></rect><text class="cs-size" x="410.3" y="585.5" text-anchor="middle">64</text><rect class="cs-last" x="450.7" y="570" width="20.2" height="22" rx="3"><title>0x1100–0x110F: 16 bytes (last)</title></rect><text class="cs-size halo" x="460.8" y="565" text-anchor="middle">16</text></svg>

    <span class="viz-legend"><span><i class="cs-first"></i>ה-Completion הראשון (או היחיד)</span><span><i class="cs-mid"></i>אמצעי</span><span><i class="cs-last"></i>אחרון</span></span>

    **נקודה שכדאי לשים לב אליה לקראת הבונוס.** בכתובת הלא מיושרת הפיצול `[256]` הוא
    Completion יחיד שמכסה **חמישה** בלוקים, יותר מ-\( m = MPS / RCB = 4 \). הוא חוקי רק
    בגלל ששני בלוקי הקצה קצרים (‏\( 48 + 16 = 64 \le RCB \)), ולכן האורך הכולל נשאר 256.
    בספירה "לפי בלוקים" של סעיף ב הוא לא ייספר, ובנוסחה הכללית הוא מופיע כאיבר תיקון
    \( \delta = 1 \). כאן, כש-\( L \le MPS \), הדרך הפשוטה \( 2^{N-1} \) כבר כוללת אותו.

---

### סעיף ב – שתי בקשות של 512 בתים

אותה שאלה לבקשות ארוכות יותר, שבהן \( L > MPS \):

1. ‏\( A = \texttt{0x1000} \), ‏\( L = 512 \).
2. ‏\( A = \texttt{0x1010} \), ‏\( L = 512 \).

??? tip "רמז 1"
    עכשיו תת-קבוצה של גבולות יכולה להיפסל. נסחו את חוק 4 במונחים של **בלוקים**: כמה בלוקים
    של 64 יכול Completion אחד להכיל?

??? tip "רמז 2"
    חשבו על ה-Completion הראשון: הוא מכסה 1, 2, 3 או 4 בלוקים, ומה שנשאר הוא אותה בעיה עם
    פחות בלוקים. כתבו נוסחת נסיגה וחשבו טבלה.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        בכתובת המיושרת **108** פיצולים, בכתובת הלא מיושרת **208**. מספר הפיצולים הוא מספר
        הדרכים לחלק את \( N \) בלוקים לקבוצות עוקבות של 1 עד 4 בלוקים, \( C(N) \), עם
        \( C(N) = C(N-1) + \dots + C(N-4) \). המיושרת נוגעת ב-8 בלוקים
        (\( C(8) = 108 \)), הלא מיושרת ב-9 (\( C(9) = 208 \)).

    #### הרעיון { .sol-idea }

    **חוק 4 במונחי בלוקים.** Completion הוא תמיד איחוד של בלוקים **עוקבים**. כש-\( r \)
    הבלוקים כולם מלאים, אורכו \( 64r \), והוא חוקי אם ורק אם \( r \le 4 \). אם הוא מכיל את
    הבלוק הראשון (‏\( f \) בתים, ‏\( 0 < f \le 64 \)) ועוד \( r - 1 \) בלוקים מלאים, אורכו
    \( f + 64(r - 1) \), וגם זה \( \le 256 \) אם ורק אם \( r \le 4 \): עם \( r = 5 \) מקבלים
    \( f + 256 > 256 \) לכל \( f > 0 \), ועם \( r = 4 \) מקבלים \( f + 192 \le 256 \) לכל
    \( f \le 64 \). אותו דבר לבלוק האחרון. המקרה היחיד שבו הכלל "\( r \le 4 \)" לא מדויק הוא
    Completion שמכיל את **שני** הקצוות, כלומר Completion יחיד לכל הבקשה; עם \( L = 512 > MPS \)
    הוא ממילא לא חוקי. לכן בסעיף הזה:

    > פיצול חוקי \( \iff \) חלוקה של \( N \) הבלוקים לקבוצות עוקבות של **1 עד 4** בלוקים.

    **נוסחת הנסיגה.** נסמן ב-\( C(n) \) את מספר החלוקות של \( n \) בלוקים עוקבים לקבוצות של
    1 עד 4. ה-Completion הראשון מכסה \( i \in \{1, 2, 3, 4\} \) בלוקים, ומה שנשאר הוא בדיוק אותה
    בעיה על \( n - i \) בלוקים:

    \[
    \begin{aligned}
    C(n) &= C(n-1) + C(n-2) \\
         &\quad + C(n-3) + C(n-4), \\
    C(0) &= 1, \qquad C(n) = 0 \;\; (n < 0).
    \end{aligned}
    \]

    זו סדרת "טטרנאצ'י": ‏\( 1, 1, 2, 4, 8, 15, 29, 56, 108, 208, \dots \)

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הבלוקים:** מיושרת: ‏\( \texttt{0x1000} \) עד \( \texttt{0x11FF} \), שמונה בלוקים
       מלאים, ‏\( N = 8 \). לא מיושרת: ‏\( \texttt{0x1010} \) עד \( \texttt{0x120F} \), ‏48 ועוד
       שבעה בלוקים מלאים ועוד 16, ‏\( N = 9 \).
    2. **החסם:** כל Completion מכסה 1 עד 4 בלוקים (‏\( m = 256 / 64 = 4 \)).
    3. **הנסיגה:** ‏\( C(n) = C(n-1) + \dots + C(n-4) \) עם \( C(0) = 1 \).
    4. **הטבלה:** ‏\( 1, 1, 2, 4, 8, 15, 29, 56, 108, 208 \) עבור \( n = 0 \) עד \( 9 \).
    5. **הקריאה:** ‏\( C(8) = 108 \) ו-\( C(9) = 208 \).

    </div>

    #### למה זה נכון { .sol-proof }

    **מבנה הבלוקים** של שתי הבקשות. שוב הכתובת הלא מיושרת מוסיפה בלוק:

    <svg class="figure cs-fig" viewBox="0 0 640 132" style="max-width:40rem" role="img" aria-label="בקשה של 512 בתים מכתובת 0x1000 על רשת RCB של 64: 8 בלוקים, 7 גבולות פנימיים"><line class="cs-rcb" x1="40.0" y1="26" x2="40.0" y2="96"/><text class="coord halo" x="40.0" y="16" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="102.2" y1="26" x2="102.2" y2="96"/><line class="cs-rcb" x1="164.4" y1="26" x2="164.4" y2="96"/><text class="coord halo" x="164.4" y="16" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="226.7" y1="26" x2="226.7" y2="96"/><line class="cs-rcb" x1="288.9" y1="26" x2="288.9" y2="96"/><text class="coord halo" x="288.9" y="16" text-anchor="middle">0x1100</text><line class="cs-rcb" x1="351.1" y1="26" x2="351.1" y2="96"/><line class="cs-rcb" x1="413.3" y1="26" x2="413.3" y2="96"/><text class="coord halo" x="413.3" y="16" text-anchor="middle">0x1180</text><line class="cs-rcb" x1="475.6" y1="26" x2="475.6" y2="96"/><line class="cs-rcb" x1="537.8" y1="26" x2="537.8" y2="96"/><text class="coord halo" x="537.8" y="16" text-anchor="middle">0x1200</text><line class="cs-rcb" x1="600.0" y1="26" x2="600.0" y2="96"/><line class="cs-req" x1="40.0" y1="26" x2="40.0" y2="96"/><line class="cs-req" x1="537.8" y1="26" x2="537.8" y2="96"/><rect class="cs-first" x="40.0" y="50" width="62.2" height="28" rx="3"><title>block 1: 0x1000–0x103F, 64 bytes</title></rect><text class="cs-size" x="71.1" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="102.2" y="50" width="62.2" height="28" rx="3"><title>block 2: 0x1040–0x107F, 64 bytes</title></rect><text class="cs-size" x="133.3" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="164.4" y="50" width="62.2" height="28" rx="3"><title>block 3: 0x1080–0x10BF, 64 bytes</title></rect><text class="cs-size" x="195.6" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="226.7" y="50" width="62.2" height="28" rx="3"><title>block 4: 0x10C0–0x10FF, 64 bytes</title></rect><text class="cs-size" x="257.8" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="288.9" y="50" width="62.2" height="28" rx="3"><title>block 5: 0x1100–0x113F, 64 bytes</title></rect><text class="cs-size" x="320.0" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="351.1" y="50" width="62.2" height="28" rx="3"><title>block 6: 0x1140–0x117F, 64 bytes</title></rect><text class="cs-size" x="382.2" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="413.3" y="50" width="62.2" height="28" rx="3"><title>block 7: 0x1180–0x11BF, 64 bytes</title></rect><text class="cs-size" x="444.4" y="68.5" text-anchor="middle">64</text><rect class="cs-last" x="475.6" y="50" width="62.2" height="28" rx="3"><title>block 8: 0x11C0–0x11FF, 64 bytes</title></rect><text class="cs-size" x="506.7" y="68.5" text-anchor="middle">64</text><circle class="cs-can" cx="102.2" cy="50" r="4"><title>boundary 0x1040</title></circle><circle class="cs-can" cx="164.4" cy="50" r="4"><title>boundary 0x1080</title></circle><circle class="cs-can" cx="226.7" cy="50" r="4"><title>boundary 0x10C0</title></circle><circle class="cs-can" cx="288.9" cy="50" r="4"><title>boundary 0x1100</title></circle><circle class="cs-can" cx="351.1" cy="50" r="4"><title>boundary 0x1140</title></circle><circle class="cs-can" cx="413.3" cy="50" r="4"><title>boundary 0x1180</title></circle><circle class="cs-can" cx="475.6" cy="50" r="4"><title>boundary 0x11C0</title></circle><text class="legend" x="40" y="118">N = 8, |B| = 7, f = 64, e = 64, m = MPS / RCB = 4, δ = 0</text></svg>

    <svg class="figure cs-fig" viewBox="0 0 640 132" style="max-width:40rem" role="img" aria-label="בקשה של 512 בתים מכתובת 0x1010 על רשת RCB של 64: 9 בלוקים, 8 גבולות פנימיים"><line class="cs-rcb" x1="40.0" y1="26" x2="40.0" y2="96"/><text class="coord halo" x="40.0" y="16" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="96.0" y1="26" x2="96.0" y2="96"/><line class="cs-rcb" x1="152.0" y1="26" x2="152.0" y2="96"/><text class="coord halo" x="152.0" y="16" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="208.0" y1="26" x2="208.0" y2="96"/><line class="cs-rcb" x1="264.0" y1="26" x2="264.0" y2="96"/><text class="coord halo" x="264.0" y="16" text-anchor="middle">0x1100</text><line class="cs-rcb" x1="320.0" y1="26" x2="320.0" y2="96"/><line class="cs-rcb" x1="376.0" y1="26" x2="376.0" y2="96"/><text class="coord halo" x="376.0" y="16" text-anchor="middle">0x1180</text><line class="cs-rcb" x1="432.0" y1="26" x2="432.0" y2="96"/><line class="cs-rcb" x1="488.0" y1="26" x2="488.0" y2="96"/><text class="coord halo" x="488.0" y="16" text-anchor="middle">0x1200</text><line class="cs-rcb" x1="544.0" y1="26" x2="544.0" y2="96"/><line class="cs-rcb" x1="600.0" y1="26" x2="600.0" y2="96"/><text class="coord halo" x="600.0" y="16" text-anchor="middle">0x1280</text><line class="cs-req" x1="54.0" y1="26" x2="54.0" y2="96"/><line class="cs-req" x1="502.0" y1="26" x2="502.0" y2="96"/><rect class="cs-first" x="54.0" y="50" width="42.0" height="28" rx="3"><title>block 1: 0x1010–0x103F, 48 bytes</title></rect><text class="cs-size" x="75.0" y="68.5" text-anchor="middle">48</text><rect class="cs-mid" x="96.0" y="50" width="56.0" height="28" rx="3"><title>block 2: 0x1040–0x107F, 64 bytes</title></rect><text class="cs-size" x="124.0" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="152.0" y="50" width="56.0" height="28" rx="3"><title>block 3: 0x1080–0x10BF, 64 bytes</title></rect><text class="cs-size" x="180.0" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="208.0" y="50" width="56.0" height="28" rx="3"><title>block 4: 0x10C0–0x10FF, 64 bytes</title></rect><text class="cs-size" x="236.0" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="264.0" y="50" width="56.0" height="28" rx="3"><title>block 5: 0x1100–0x113F, 64 bytes</title></rect><text class="cs-size" x="292.0" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="320.0" y="50" width="56.0" height="28" rx="3"><title>block 6: 0x1140–0x117F, 64 bytes</title></rect><text class="cs-size" x="348.0" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="376.0" y="50" width="56.0" height="28" rx="3"><title>block 7: 0x1180–0x11BF, 64 bytes</title></rect><text class="cs-size" x="404.0" y="68.5" text-anchor="middle">64</text><rect class="cs-mid" x="432.0" y="50" width="56.0" height="28" rx="3"><title>block 8: 0x11C0–0x11FF, 64 bytes</title></rect><text class="cs-size" x="460.0" y="68.5" text-anchor="middle">64</text><rect class="cs-last" x="488.0" y="50" width="14.0" height="28" rx="3"><title>block 9: 0x1200–0x120F, 16 bytes</title></rect><text class="cs-size halo" x="495.0" y="45" text-anchor="middle">16</text><circle class="cs-can" cx="96.0" cy="50" r="4"><title>boundary 0x1040</title></circle><circle class="cs-can" cx="152.0" cy="50" r="4"><title>boundary 0x1080</title></circle><circle class="cs-can" cx="208.0" cy="50" r="4"><title>boundary 0x10C0</title></circle><circle class="cs-can" cx="264.0" cy="50" r="4"><title>boundary 0x1100</title></circle><circle class="cs-can" cx="320.0" cy="50" r="4"><title>boundary 0x1140</title></circle><circle class="cs-can" cx="376.0" cy="50" r="4"><title>boundary 0x1180</title></circle><circle class="cs-can" cx="432.0" cy="50" r="4"><title>boundary 0x11C0</title></circle><circle class="cs-can" cx="488.0" cy="50" r="4"><title>boundary 0x1200</title></circle><text class="legend" x="40" y="118">N = 9, |B| = 8, f = 48, e = 16, m = MPS / RCB = 4, δ = 0</text></svg>

    **הצעד הראשון של הנסיגה** עבור \( N = 8 \): לפי כמה בלוקים מכסה ה-Completion הראשון,
    ומה שנשאר הוא מופע קטן יותר של אותה בעיה. ארבעת המקרים זרים ומכסים הכול, ולכן סוכמים:

    <svg class="figure cs-fig" viewBox="0 0 640 240" style="max-width:40rem" role="img" aria-label="הפיצול לפי מספר הבלוקים של ה-Completion הראשון: C(8) כסכום של C(7) עד C(4)"><line class="cs-rcb" x1="150" y1="24" x2="150" y2="214"/><line class="cs-rcb" x1="194" y1="24" x2="194" y2="214"/><line class="cs-rcb" x1="238" y1="24" x2="238" y2="214"/><line class="cs-rcb" x1="282" y1="24" x2="282" y2="214"/><line class="cs-rcb" x1="326" y1="24" x2="326" y2="214"/><line class="cs-rcb" x1="370" y1="24" x2="370" y2="214"/><line class="cs-rcb" x1="414" y1="24" x2="414" y2="214"/><line class="cs-rcb" x1="458" y1="24" x2="458" y2="214"/><line class="cs-rcb" x1="502" y1="24" x2="502" y2="214"/><text class="tick" x="172.0" y="20" text-anchor="middle">β1</text><text class="tick" x="216.0" y="20" text-anchor="middle">β2</text><text class="tick" x="260.0" y="20" text-anchor="middle">β3</text><text class="tick" x="304.0" y="20" text-anchor="middle">β4</text><text class="tick" x="348.0" y="20" text-anchor="middle">β5</text><text class="tick" x="392.0" y="20" text-anchor="middle">β6</text><text class="tick" x="436.0" y="20" text-anchor="middle">β7</text><text class="tick" x="480.0" y="20" text-anchor="middle">β8</text><text class="legend halo" x="140" y="53" text-anchor="end">first covers 1</text><rect class="cs-first" x="150" y="34" width="44" height="30" rx="3"><title>the first completion: 1 block</title></rect><text class="cs-size" x="172.0" y="53" text-anchor="middle">1</text><rect class="cs-mid" x="194" y="34" width="308" height="30" rx="3"><title>what is left: 7 blocks, C(7) = 56 ways</title></rect><text class="cs-size" x="348.0" y="53" text-anchor="middle">C(7) = 56</text><text class="legend halo" x="140" y="97" text-anchor="end">first covers 2</text><rect class="cs-first" x="150" y="78" width="88" height="30" rx="3"><title>the first completion: 2 blocks</title></rect><text class="cs-size" x="194.0" y="97" text-anchor="middle">2</text><rect class="cs-mid" x="238" y="78" width="264" height="30" rx="3"><title>what is left: 6 blocks, C(6) = 29 ways</title></rect><text class="cs-size" x="370.0" y="97" text-anchor="middle">C(6) = 29</text><text class="legend halo" x="140" y="141" text-anchor="end">first covers 3</text><rect class="cs-first" x="150" y="122" width="132" height="30" rx="3"><title>the first completion: 3 blocks</title></rect><text class="cs-size" x="216.0" y="141" text-anchor="middle">3</text><rect class="cs-mid" x="282" y="122" width="220" height="30" rx="3"><title>what is left: 5 blocks, C(5) = 15 ways</title></rect><text class="cs-size" x="392.0" y="141" text-anchor="middle">C(5) = 15</text><text class="legend halo" x="140" y="185" text-anchor="end">first covers 4</text><rect class="cs-first" x="150" y="166" width="176" height="30" rx="3"><title>the first completion: 4 blocks</title></rect><text class="cs-size" x="238.0" y="185" text-anchor="middle">4</text><rect class="cs-mid" x="326" y="166" width="176" height="30" rx="3"><title>what is left: 4 blocks, C(4) = 8 ways</title></rect><text class="cs-size" x="414.0" y="185" text-anchor="middle">C(4) = 8</text><text class="legend" x="150" y="232" font-weight="700">C(8) = 56 + 29 + 15 + 8 = 108</text></svg>

    **הטבלה המלאה.** כל שורה היא סכום ארבע השורות שלפניה (עם \( C(0) = 1 \) ו-\( C(n) = 0 \)
    לשליליים):

    | ‏\( N \) | החישוב | ‏\( C_4(N) \) |
    |:-:|---|:-:|
    | 1 | בלוק אחד, Completion אחד | **1** |
    | 2 | ‏\( 1 + 1 \) | **2** |
    | 3 | ‏\( 2 + 1 + 1 \) | **4** |
    | 4 | ‏\( 4 + 2 + 1 + 1 \) | **8** |
    | 5 | ‏\( 8 + 4 + 2 + 1 \) | **15** |
    | 6 | ‏\( 15 + 8 + 4 + 2 \) | **29** |
    | 7 | ‏\( 29 + 15 + 8 + 4 \) | **56** |
    | 8 | ‏\( 56 + 29 + 15 + 8 \) | **108** |
    | 9 | ‏\( 108 + 56 + 29 + 15 \) | **208** |

    **למה לא \( 2^{N-1} \).** בלי MPS היו \( 2^7 = 128 \) ו-\( 2^8 = 256 \) תת-קבוצות. ההפרש
    (‏20 ו-48) הוא מספר תת-הקבוצות שבהן יש "רווח" של חמישה בלוקים או יותר בין שני חיתוכים
    עוקבים, כלומר Completion של 320 בתים ומעלה (או \( 48 + 256 = 304 \) בקצה), והוא נפסל.

    **לפי מספר ה-Completions.** אפשר גם לספור כמה פיצולים יש עם בדיוק \( k \) Completions
    (הנוסחה והוכחתה בסעיף ג). השורות מסתכמות ל-108 ול-208:

    | מספר Completions ‏\( k \) | ‏\( T(8, k) \) |
    |:-:|:-:|
    | 2 | 1 |
    | 3 | 12 |
    | 4 | 31 |
    | 5 | 35 |
    | 6 | 21 |
    | 7 | 7 |
    | 8 | 1 |
    | **סך הכול** | **108** |

    | מספר Completions ‏\( k \) | ‏\( T(9, k) \) |
    |:-:|:-:|
    | 3 | 10 |
    | 4 | 40 |
    | 5 | 65 |
    | 6 | 56 |
    | 7 | 28 |
    | 8 | 8 |
    | 9 | 1 |
    | **סך הכול** | **208** |

    שימו לב שבכתובת הלא מיושרת המינימום הוא שלושה Completions, לא שניים: ‏\( 256 + 256 \)
    היה חותך ב-\( \texttt{0x1110} \), שאינו גבול RCB, ו-\( 240 + 256 + 16 \) הוא כבר שלושה.

---

### סעיף ג (בונוס) – הנוסחה הכללית והוכחתה

מצאו נוסחה סגורה למספר הפיצולים החוקיים \( \mathrm{Count}(A, L, MPS, RCB) \) לכל
‏\( A \), \( L \), \( MPS \) ו-\( RCB \) (עם \( RCB \mid MPS \)), הוכיחו אותה, וכתבו אותה במפורש
עבור \( MPS = 256 \) ו-\( RCB = 64 \).

??? tip "רמז 1"
    הכלילו את סעיף ב: Completion מכסה לכל היותר \( m = MPS / RCB \) בלוקים, חוץ ממקרה קצה
    אחד. אילו ערכים של \( N \) ו-\( L \) מאפשרים ל-Completion יחיד להכיל יותר מ-\( m \)
    בלוקים ובכל זאת לעמוד ב-MPS?

??? tip "רמז 2"
    מספר ההרכבות (compositions) של \( N \) לחלקים בגודל 1 עד \( m \) נספר על ידי הפונקציה
    היוצרת \( 1 / (1 - P(x)) \) עם \( P(x) = x + x^2 + \dots + x^m \). פשטו אותה, ופתחו את
    \( 1 / (1 - 2x + x^{m+1}) \) כטור הנדסי כדי לקבל מקדם מפורש.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        עם \( a = A \bmod RCB \), ‏\( m = MPS / RCB \) ו-\( N = \lceil (a + L) / RCB \rceil \) (מספר
        הבלוקים):
        \( \mathrm{Count} = S(N) - S(N-1) + \delta \), כאשר
        \( S(n) = \sum_{j} (-1)^j \binom{n - mj}{j} 2^{\,n - (m+1)j} \), ‏\( S(-1) = 0 \),
        ו-\( \delta = 1 \) בדיוק כאשר \( N = m + 1 \) וגם \( L \le MPS \) (אחרת 0). עבור
        \( MPS = 256 \), ‏\( RCB = 64 \): ‏\( m = 4 \), הסכום רץ על \( j \le n / 5 \), ו-\( \delta = 1 \)
        רק כש-\( N = 5 \) ו-\( L \le 256 \).

    #### הרעיון { .sol-idea }

    ההוכחה בנויה מחמש למות, כל אחת צעד אחד:

    1. **רדוקציה:** פיצול שמקיים את חוקים 1 עד 3 הוא בדיוק תת-קבוצה של הגבולות הפנימיים.
    2. **חוק MPS בבלוקים:** Completion חוקי אם ורק אם הוא מכיל לכל היותר \( m \) בלוקים, פרט
       ל-Completion יחיד שמכיל את שני הקצוות.
    3. **החריג:** המקרה היחיד שבו Completion יחיד עם יותר מ-\( m \) בלוקים חוקי הוא
       \( N = m + 1 \) עם \( L \le MPS \). זה ה-\( \delta \).
    4. **הרכבות:** בלי החריג, הספירה היא מספר ההרכבות של \( N \) לחלקים של 1 עד \( m \), עם
       נוסחת נסיגה ופונקציה יוצרת \( (1 - x) / (1 - 2x + x^{m+1}) \).
    5. **נוסחה סגורה:** פיתוח הפונקציה היוצרת כטור הנדסי ובינום נותן את \( S(n) \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **סימונים:** ‏\( a = A \bmod RCB \), ‏\( m = MPS / RCB \) (שלם, כי \( RCB \mid MPS \)),
       ‏\( N = \lceil (a + L) / RCB \rceil \) מספר הבלוקים, ‏\( \mathcal{B} \) הגבולות הפנימיים
       (‏\( |\mathcal{B}| = N - 1 \)), ‏\( f \) ו-\( e \) גדלי בלוקי הקצה (‏\( 0 < f, e \le RCB \)).
    2. **למה 1:** התאמה חד-חד-ערכית ועל בין פיצולים (חוקים 1 עד 3) לתת-קבוצות של
       \( \mathcal{B} \).
    3. **למה 2:** חוק 4 הופך ל-"\( r \le m \) בלוקים", עם חריג אחד.
    4. **למה 3:** החריג קיים בדיוק כאשר \( N = m + 1 \) ו-\( L \le MPS \), ואז הוא מוסיף פיצול
       אחד בדיוק: ‏\( \delta \).
    5. **למה 4:** הרכבות עם חלקים חסומים: נסיגה, פונקציה יוצרת ופישוטה.
    6. **למה 5:** המקדם \( [x^n] \) של \( 1 / (1 - 2x + x^{m+1}) \) הוא \( S(n) \); כפל ב-\( (1 - x) \)
       נותן \( S(N) - S(N-1) \).
    7. **הצבה:** ‏\( MPS = 256 \), ‏\( RCB = 64 \), ובדיקה מול סעיפים א ו-ב.

    </div>

    #### למה זה נכון { .sol-proof }

    **סימונים.** הגבולות הפנימיים מחלקים את \( [A, A + L) \) ל-\( N \) בלוקים
    \( \beta_1, \dots, \beta_N \). הבלוקים הפנימיים הם בגודל RCB בדיוק, ושני הקצוות בגדלים
    \( f = |\beta_1| \) ו-\( e = |\beta_N| \), עם \( 0 < f, e \le RCB \). הבלוק הראשון מלא
    (‏\( f = RCB \)) אם ורק אם \( a = 0 \), והאחרון מלא אם ורק אם \( (A + L) \bmod RCB = 0 \).
    הקשר בין האורך לבלוקים, כש-\( N \ge 2 \):

    \[
    L = f + (N - 2) \cdot RCB + e .
    \]

    **המשפט.** לכל \( A, L, MPS, RCB \):

    \[
    \boxed{\;\mathrm{Count} = S(N) - S(N-1) + \delta\;}
    \]

    \[
    \begin{aligned}
    S(n) &= \sum_{j=0}^{\lfloor n / (m+1) \rfloor} (-1)^j \binom{n - mj}{j}\, 2^{\,n - (m+1)j}, \\
    S(-1) &= 0,
    \end{aligned}
    \]

    \[
    \delta =
    \begin{cases}
    1 & N = m + 1 \;\text{ and }\; L \le MPS \\
    0 & \text{otherwise}
    \end{cases}
    \]

    ---

    **למה 1 (רדוקציה לתת-קבוצות של גבולות).** קיימת התאמה חד-חד-ערכית ועל בין רצפי
    Completions שמקיימים את חוקים 1 עד 3 לבין תת-הקבוצות \( X \subseteq \mathcal{B} \).

    *הוכחה.* בכיוון אחד, לרצף Completions נתאים את קבוצת נקודות החיתוך שלו (סוף כל Completion
    שאינו האחרון). לפי חוק 3 כל נקודה כזו היא כפולה של RCB, ולפי חוקים 1 ו-2 היא בתוך
    \( (A, A + L) \), ולכן \( X \subseteq \mathcal{B} \). בכיוון השני, תת-קבוצה
    \( X = \{x_1 < \dots < x_{k-1}\} \) קובעת רצף יחיד

    \[
    [A, x_1),\; [x_1, x_2),\; \dots,\; [x_{k-1}, A + L),
    \]

    שמקיים את חוקים 1 עד 3 לפי הבנייה. שתי ההתאמות הפוכות זו לזו: נקודות החיתוך של הרצף
    שנבנה מ-\( X \) הן בדיוק \( X \), והרצף שנבנה מנקודות החיתוך של רצף נתון הוא אותו רצף.
    \( \blacksquare \)

    *מסקנה.* כל Completion הוא איחוד של בלוקים **צמודים** \( \beta_i \cup \dots \cup \beta_{i'} \),
    ולספור פיצולים חוקיים פירושו לספור את תת-הקבוצות \( X \) שבהן כל Completion מקיים גם את
    חוק 4.

    ---

    **למה 2 (חוק MPS במונחי בלוקים).** Completion שמכיל \( r \) בלוקים צמודים מקיים את חוק 4
    אם ורק אם \( r \le m \), **פרט** למקרה אחד: Completion שמכיל גם את \( \beta_1 \) וגם את
    \( \beta_N \), כלומר Completion יחיד לכל הבקשה.

    *הוכחה.* שלושה מקרים, לפי אילו בלוקי קצה ה-Completion מכיל:

    <svg class="figure cs-fig" viewBox="0 0 640 220" style="max-width:40rem" role="img" aria-label="שלושת המקרים של למה 2: Completion פנימי, Completion עם קצה אחד, ו-Completion יחיד שמכיל את שני הקצוות"><line class="cs-req" x1="30.0" y1="28" x2="30.0" y2="216"/><line class="cs-rcb" x1="58.8" y1="28" x2="58.8" y2="216"/><line class="cs-rcb" x1="122.8" y1="28" x2="122.8" y2="216"/><line class="cs-rcb" x1="186.8" y1="28" x2="186.8" y2="216"/><line class="cs-rcb" x1="250.8" y1="28" x2="250.8" y2="216"/><line class="cs-rcb" x1="314.8" y1="28" x2="314.8" y2="216"/><line class="cs-req" x1="334.0" y1="28" x2="334.0" y2="216"/><text class="tick" x="44.4" y="24" text-anchor="middle">f</text><text class="tick" x="90.8" y="24" text-anchor="middle">RCB</text><text class="tick" x="154.8" y="24" text-anchor="middle">RCB</text><text class="tick" x="218.8" y="24" text-anchor="middle">RCB</text><text class="tick" x="282.8" y="24" text-anchor="middle">RCB</text><text class="tick" x="324.4" y="24" text-anchor="middle">e</text><rect class="cs-mid" x="30.0" y="40" width="28.8" height="28" rx="2"/><rect class="cs-first" x="58.8" y="40" width="64.0" height="28" rx="2"/><rect class="cs-first" x="122.8" y="40" width="64.0" height="28" rx="2"/><rect class="cs-first" x="186.8" y="40" width="64.0" height="28" rx="2"/><rect class="cs-mid" x="250.8" y="40" width="64.0" height="28" rx="2"/><rect class="cs-mid" x="314.8" y="40" width="19.2" height="28" rx="2"/><line class="ink-line" x1="60.8" y1="76" x2="248.8" y2="76" stroke-width="1.6"/><text class="legend" x="348.0" y="51" font-weight="700">(a) interior, r = 3</text><text class="tick" x="348.0" y="68">3·RCB ≤ MPS ⇔ r ≤ 4</text><rect class="cs-first" x="30.0" y="98" width="28.8" height="28" rx="2"/><rect class="cs-first" x="58.8" y="98" width="64.0" height="28" rx="2"/><rect class="cs-first" x="122.8" y="98" width="64.0" height="28" rx="2"/><rect class="cs-first" x="186.8" y="98" width="64.0" height="28" rx="2"/><rect class="cs-mid" x="250.8" y="98" width="64.0" height="28" rx="2"/><rect class="cs-mid" x="314.8" y="98" width="19.2" height="28" rx="2"/><line class="ink-line" x1="32.0" y1="134" x2="248.8" y2="134" stroke-width="1.6"/><text class="legend" x="348.0" y="109" font-weight="700">(b) one end, r = 4</text><text class="tick" x="348.0" y="126">f + 3·RCB ≤ MPS ⇔ r ≤ 4</text><rect class="cs-one" x="30.0" y="156" width="28.8" height="28" rx="2"/><rect class="cs-one" x="58.8" y="156" width="64.0" height="28" rx="2"/><rect class="cs-one" x="122.8" y="156" width="64.0" height="28" rx="2"/><rect class="cs-one" x="186.8" y="156" width="64.0" height="28" rx="2"/><rect class="cs-one" x="250.8" y="156" width="64.0" height="28" rx="2"/><rect class="cs-one" x="314.8" y="156" width="19.2" height="28" rx="2"/><line class="ink-line" x1="32.0" y1="192" x2="332.0" y2="192" stroke-width="1.6"/><text class="legend" x="348.0" y="167" font-weight="700">(c) both ends, r = N</text><text class="tick" x="348.0" y="184">L ≤ MPS ? (the δ case)</text></svg>

    **(א) Completion פנימי**, שלא מכיל את \( \beta_1 \) ולא את \( \beta_N \). כל בלוקיו מלאים,
    ולכן אורכו \( r \cdot RCB \), ו-

    \[
    r \cdot RCB \le m \cdot RCB \iff r \le m .
    \]

    **(ב) Completion שמכיל קצה אחד בלבד**, נאמר \( \beta_1 \), ועוד \( r - 1 \) בלוקים מלאים.
    אורכו \( f + (r - 1) \cdot RCB \), ומכיוון ש-\( 0 < f \le RCB \):

    \[
    \begin{aligned}
    f + (r - 1) \cdot RCB &\le m \cdot RCB \\
    \iff r - 1 &\le m - \frac{f}{RCB} \\
    \iff r &\le m .
    \end{aligned}
    \]

    השקילות האחרונה היא הלב של הלמה: \( r \) שלם ו-\( 0 < f / RCB \le 1 \), ולכן
    \( m - f / RCB \) נמצא בקטע \( [m - 1, m) \), ומספר שלם קטן או שווה לו אם ורק אם הוא
    קטן או שווה ל-\( m - 1 \). במילים: בלוק קצה חלקי "לא עוזר" להכניס בלוק מלא נוסף, כי
    \( f + m \cdot RCB > m \cdot RCB = MPS \) לכל \( f > 0 \); ומצד שני הוא אף פעם לא מפריע,
    כי \( f + (m - 1) \cdot RCB \le m \cdot RCB \). אותו טיעון בדיוק חל על \( \beta_N \) עם
    \( e \).

    **(ג) Completion שמכיל את שני הקצוות.** לפי למה 1 זה אפשרי רק כאשר \( X = \emptyset \):
    Completion יחיד באורך \( L \) שמכיל \( r = N \) בלוקים. הוא חוקי אם ורק אם \( L \le MPS \),
    וזה **לא** בהכרח שקול ל-\( N \le m \), כי שני הקצוות החלקיים יכולים "להתחלק" בבלוק
    אחד. \( \blacksquare \)

    ---

    **למה 3 (החריג).** קיים בדיוק פיצול חוקי אחד שהכלל "\( r \le m \)" לא סופר אם ורק אם
    \( \delta = 1 \), כלומר \( N = m + 1 \) ו-\( L \le MPS \).

    *הוכחה.* רק מקרה (ג) יכול לסטות מהכלל, והוא פיצול אחד לכל היותר (ה-Completion היחיד).
    אם \( N \le m \), אז \( r = N \le m \) והכלל כבר סופר אותו: אין סטייה. הסטייה קיימת רק כאשר
    \( N > m \) **וגם** \( L \le MPS \). נציב \( L = f + (N - 2) \cdot RCB + e \) בתנאי
    \( L \le m \cdot RCB \):

    \[
    f + e \le (m - N + 2) \cdot RCB .
    \]

    - עבור \( N = m + 1 \) התנאי הוא \( f + e \le RCB \), וזה אפשרי: למשל \( f = e = RCB / 2 \),
      או \( f = 48 \), ‏\( e = 16 \) כמו בסעיף א.
    - עבור \( N \ge m + 2 \) צד ימין הוא \( \le 0 \), אבל \( f + e > 0 \). סתירה.

    לכן החריג קיים בדיוק כאשר \( N = m + 1 \) ו-\( L \le MPS \), ואז נוסף פיצול אחד בדיוק.
    \( \blacksquare \)

    *הערה.* אם \( a = 0 \) אז \( f = RCB \) ו-\( f + e > RCB \), ולכן בכתובת מיושרת תמיד
    \( \delta = 0 \). החריג דורש ששני הקצוות יהיו חלקיים, וביחד לא יותר מבלוק אחד.

    **הדוגמה של סעיף א** היא בדיוק החריג: ‏\( \texttt{0x1010} \), ‏\( L = 256 \), ‏\( N = 5 = m + 1 \),
    ‏\( f + e = 48 + 16 = 64 \le RCB \). הספירה לפי בלוקים נותנת \( C_4(5) = 15 \), ועוד
    \( \delta = 1 \) עבור `[256]`, סך הכול 16, כמו \( 2^4 \). דוגמה קטנה יותר, עם
    \( MPS = 128 \) (‏\( m = 2 \)): ‏\( A = \texttt{0x1020} \), ‏\( L = 128 \). הבלוקים הם
    ‏\( 32, 64, 32 \), כלומר \( N = 3 = m + 1 \) ו-\( L \le MPS \), ולכן
    \( C_2(3) + 1 = 3 + 1 = 4 \) פיצולים:

    <svg class="figure cs-fig" viewBox="0 0 640 132" style="max-width:40rem" role="img" aria-label="בקשה של 128 בתים מכתובת 0x1020 על רשת RCB של 64: 3 בלוקים, 2 גבולות פנימיים"><line class="cs-rcb" x1="40.0" y1="26" x2="40.0" y2="96"/><text class="coord halo" x="40.0" y="16" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="180.0" y1="26" x2="180.0" y2="96"/><text class="coord halo" x="180.0" y="16" text-anchor="middle">0x1040</text><line class="cs-rcb" x1="320.0" y1="26" x2="320.0" y2="96"/><text class="coord halo" x="320.0" y="16" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="460.0" y1="26" x2="460.0" y2="96"/><text class="coord halo" x="460.0" y="16" text-anchor="middle">0x10C0</text><line class="cs-rcb" x1="600.0" y1="26" x2="600.0" y2="96"/><text class="coord halo" x="600.0" y="16" text-anchor="middle">0x1100</text><line class="cs-req" x1="110.0" y1="26" x2="110.0" y2="96"/><line class="cs-req" x1="390.0" y1="26" x2="390.0" y2="96"/><rect class="cs-first" x="110.0" y="50" width="70.0" height="28" rx="3"><title>block 1: 0x1020–0x103F, 32 bytes</title></rect><text class="cs-size" x="145.0" y="68.5" text-anchor="middle">32</text><rect class="cs-mid" x="180.0" y="50" width="140.0" height="28" rx="3"><title>block 2: 0x1040–0x107F, 64 bytes</title></rect><text class="cs-size" x="250.0" y="68.5" text-anchor="middle">64</text><rect class="cs-last" x="320.0" y="50" width="70.0" height="28" rx="3"><title>block 3: 0x1080–0x109F, 32 bytes</title></rect><text class="cs-size" x="355.0" y="68.5" text-anchor="middle">32</text><circle class="cs-can" cx="180.0" cy="50" r="4"><title>boundary 0x1040</title></circle><circle class="cs-can" cx="320.0" cy="50" r="4"><title>boundary 0x1080</title></circle><text class="legend" x="40" y="118">N = 3, |B| = 2, f = 32, e = 32, m = MPS / RCB = 2, δ = 1 (N = m + 1 and L ≤ MPS)</text></svg>

    <svg class="figure cs-fig" viewBox="0 0 640 218" style="max-width:40rem" role="img" aria-label="כל 4 הפיצולים החוקיים של בקשה של 128 בתים מכתובת 0x1020 עם MPS = 128 ו-RCB = 64, שורה לכל פיצול"><line class="cs-rcb" x1="128.0" y1="24" x2="128.0" y2="214"/><text class="coord halo" x="128.0" y="16" text-anchor="middle">0x1000</text><line class="cs-rcb" x1="249.0" y1="24" x2="249.0" y2="214"/><text class="coord halo" x="249.0" y="16" text-anchor="middle">0x1040</text><line class="cs-rcb" x1="370.0" y1="24" x2="370.0" y2="214"/><text class="coord halo" x="370.0" y="16" text-anchor="middle">0x1080</text><line class="cs-rcb" x1="491.0" y1="24" x2="491.0" y2="214"/><text class="coord halo" x="491.0" y="16" text-anchor="middle">0x10C0</text><line class="cs-rcb" x1="612.0" y1="24" x2="612.0" y2="214"/><text class="coord halo" x="612.0" y="16" text-anchor="middle">0x1100</text><line class="cs-req" x1="188.5" y1="24" x2="188.5" y2="214"/><line class="cs-req" x1="430.5" y1="24" x2="430.5" y2="214"/><text class="legend halo" x="136" y="45" font-weight="700">1 completion: 1 split</text><text class="coord halo" x="118" y="69" text-anchor="end">128</text><rect class="cs-one" x="188.5" y="54" width="242.0" height="22" rx="3"><title>0x1020–0x109F: 128 bytes (one)</title></rect><text class="cs-size" x="309.5" y="69.5" text-anchor="middle">128</text><text class="legend halo" x="136" y="97" font-weight="700">2 completions: 2 splits</text><text class="coord halo" x="118" y="121" text-anchor="end">96+32</text><rect class="cs-first" x="188.5" y="106" width="181.5" height="22" rx="3"><title>0x1020–0x107F: 96 bytes (first)</title></rect><text class="cs-size" x="279.2" y="121.5" text-anchor="middle">96</text><rect class="cs-last" x="370.0" y="106" width="60.5" height="22" rx="3"><title>0x1080–0x109F: 32 bytes (last)</title></rect><text class="cs-size" x="400.2" y="121.5" text-anchor="middle">32</text><text class="coord halo" x="118" y="149" text-anchor="end">32+96</text><rect class="cs-first" x="188.5" y="134" width="60.5" height="22" rx="3"><title>0x1020–0x103F: 32 bytes (first)</title></rect><text class="cs-size" x="218.8" y="149.5" text-anchor="middle">32</text><rect class="cs-last" x="249.0" y="134" width="181.5" height="22" rx="3"><title>0x1040–0x109F: 96 bytes (last)</title></rect><text class="cs-size" x="339.8" y="149.5" text-anchor="middle">96</text><text class="legend halo" x="136" y="177" font-weight="700">3 completions: 1 split</text><text class="coord halo" x="118" y="201" text-anchor="end">32+64+32</text><rect class="cs-first" x="188.5" y="186" width="60.5" height="22" rx="3"><title>0x1020–0x103F: 32 bytes (first)</title></rect><text class="cs-size" x="218.8" y="201.5" text-anchor="middle">32</text><rect class="cs-mid" x="249.0" y="186" width="121.0" height="22" rx="3"><title>0x1040–0x107F: 64 bytes (mid)</title></rect><text class="cs-size" x="309.5" y="201.5" text-anchor="middle">64</text><rect class="cs-last" x="370.0" y="186" width="60.5" height="22" rx="3"><title>0x1080–0x109F: 32 bytes (last)</title></rect><text class="cs-size" x="400.2" y="201.5" text-anchor="middle">32</text></svg>

    ה-Completion היחיד `[128]` מכיל שלושה בלוקים, יותר מ-\( m = 2 \), ובכל זאת אורכו 128.

    ---

    **למה 4 (הרכבות עם חלקים חסומים).** לפי למות 1 עד 3,

    \[
    \mathrm{Count} = C_m(N) + \delta ,
    \]

    כאשר \( C_m(N) \) הוא מספר ה**הרכבות** (compositions) של \( N \): מספר הדרכים לכתוב
    \( r_1 + r_2 + \dots + r_k = N \) כסכום **מסודר** של שלמים עם \( 1 \le r_i \le m \). כל
    \( r_i \) הוא מספר הבלוקים של ה-Completion ה-\( i \).

    *נסיגה.* לפי גודל החלק הראשון \( r_1 = i \) (או האחרון, זה סימטרי), החלוקה למקרים זרה
    ומלאה:

    \[
    \begin{aligned}
    C_m(N) &= \sum_{i=1}^{m} C_m(N - i), \\
    C_m(0) &= 1, \qquad C_m(n) = 0 \;\; (n < 0).
    \end{aligned}
    \]

    *פונקציה יוצרת.* נסמן \( G_m(x) = \sum_{n \ge 0} C_m(n)\, x^n \). חלק בודד מיוצג על ידי

    \[
    P(x) = x + x^2 + \dots + x^m = \frac{x\,(1 - x^m)}{1 - x},
    \]

    כי המעריך של \( x \) הוא גודל החלק. רצף של \( k \) חלקים מיוצג על ידי \( P(x)^k \), כי כפל
    טורים מסכם מעריכים: המקדם של \( x^n \) ב-\( P(x)^k \) הוא מספר הדרכים לבחור \( k \) חלקים
    שסכומם \( n \). סכימה על כל \( k \ge 0 \) נותנת טור הנדסי (פורמלי, כי ל-\( P \) אין איבר
    חופשי):

    \[
    G_m(x) = \sum_{k \ge 0} P(x)^k = \frac{1}{1 - P(x)} .
    \]

    *פישוט.* מכפילים מונה ומכנה ב-\( (1 - x) \):

    \[
    \begin{aligned}
    G_m(x) &= \frac{1}{1 - \dfrac{x\,(1 - x^m)}{1 - x}} \\[4pt]
           &= \frac{1 - x}{(1 - x) - x\,(1 - x^m)} \\[4pt]
           &= \frac{1 - x}{1 - 2x + x^{m+1}} .
    \end{aligned}
    \]

    ---

    **למה 5 (נוסחה סגורה).** המקדם של \( x^n \) ב-\( 1 / (1 - 2x + x^{m+1}) \) הוא \( S(n) \).

    *הוכחה.* נסמן \( y = 2x - x^{m+1} \), כך ש-\( 1 - 2x + x^{m+1} = 1 - y \), ונפתח כטור הנדסי
    פורמלי (מותר, כי ל-\( y \) אין איבר חופשי):

    \[
    \frac{1}{1 - y} = \sum_{k \ge 0} y^k = \sum_{k \ge 0} \left(2x - x^{m+1}\right)^k .
    \]

    לפי הבינום של ניוטון, עם \( j \) הפעמים שבוחרים את האיבר \( -x^{m+1} \):

    \[
    \begin{aligned}
    \left(2x - x^{m+1}\right)^k
    &= \sum_{j=0}^{k} \binom{k}{j} (2x)^{k-j} \left(-x^{m+1}\right)^{j} \\[4pt]
    &= \sum_{j=0}^{k} (-1)^j \binom{k}{j}\, 2^{k-j}\, x^{\,k + mj} .
    \end{aligned}
    \]

    המעריך של \( x \) הוא \( (k - j) + (m + 1) j = k + mj \). המקדם של \( x^n \) מתקבל מכל
    הזוגות \( (k, j) \) עם \( k + mj = n \), כלומר \( k = n - mj \). מציבים:

    \[
    \begin{aligned}
    &[x^n]\,\frac{1}{1 - 2x + x^{m+1}} \\
    &\quad = \sum_{j} (-1)^j \binom{n - mj}{j}\, 2^{\,n - mj - j} = S(n) .
    \end{aligned}
    \]

    תחום הסכימה: צריך \( 0 \le j \le k = n - mj \), כלומר \( (m + 1) j \le n \), או
    \( j \le n / (m + 1) \). \( \blacksquare \)

    *סיום ההוכחה של המשפט.* כפל טור ב-\( (1 - x) \) מחסיר מכל מקדם את המקדם שלפניו:

    \[
    \begin{aligned}
    C_m(N) &= [x^N]\,\frac{1 - x}{1 - 2x + x^{m+1}} \\
           &= S(N) - S(N - 1),
    \end{aligned}
    \]

    ויחד עם למה 3 (והסכמה \( S(-1) = 0 \) עבור \( N = 0 \)):

    \[
    \mathrm{Count} = S(N) - S(N - 1) + \delta . \qquad \blacksquare
    \]

    ---

    **מסקנה: ספירה לפי מספר ה-Completions.** מספר הפיצולים החוקיים עם **בדיוק** \( k \)
    Completions (כש-\( \delta = 0 \), או לכל \( k \ge 2 \)) הוא

    \[
    T(N, k) = \sum_{j=0}^{\lfloor (N - k) / m \rfloor} (-1)^j \binom{k}{j} \binom{N - jm - 1}{k - 1},
    \]

    עבור \( \lceil N / m \rceil \le k \le N \) (ו-0 מחוץ לתחום).

    *הוכחה.* בלי חסם עליון, מספר ההרכבות של \( N \) ל-\( k \) חלקים חיוביים הוא
    \( \binom{N-1}{k-1} \): "כוכבים ומחיצות", בוחרים \( k - 1 \) נקודות חיתוך מתוך \( N - 1 \)
    הגבולות. נסמן ב-\( E_i \) את המאורע "החלק ה-\( i \) גדול מ-\( m \)". עבור קבוצת אינדקסים
    \( J \) עם \( |J| = j \), מחסירים \( m \) מכל חלק ב-\( J \): זו התאמה חד-חד-ערכית ועל בין
    ההרכבות שבהן כל החלקים ב-\( J \) גדולים מ-\( m \) לבין הרכבות חופשיות של \( N - jm \)
    ל-\( k \) חלקים חיוביים, ולכן

    \[
    \Bigl|\bigcap_{i \in J} E_i\Bigr| = \binom{N - jm - 1}{k - 1} .
    \]

    לפי עקרון ההכלה וההפרדה, סוכמים על \( j \) עם סימן מתחלף ועל \( \binom{k}{j} \) הבחירות של
    \( J \), ומקבלים את הנוסחה. בדיקת עקביות: \( \sum_k T(N, k) = C_m(N) \). \( \blacksquare \)

    הטבלאות של סעיף ב (108 ו-208 לפי \( k \)) חושבו בדיוק כך. למשל
    \( T(8, 3) = \binom{7}{2} - \binom{3}{1}\binom{3}{2} = 21 - 9 = 12 \).

    ---

    **מקרים מיוחדים**, כבדיקת שפיות של הנוסחה:

    | המצב | ‏\( C_m(N) \) | הסבר |
    |---|:-:|---|
    | ‏\( m = 1 \) | ‏\( 1 \) | כל Completion הוא בלוק אחד, אין בחירה (‏\( MPS = RCB \)) |
    | ‏\( m = 2 \) | ‏\( F_{N+1} \) | ‏\( C(N) = C(N-1) + C(N-2) \): פיבונאצ'י. ‏\( MPS = 128 \), ‏\( RCB = 64 \) |
    | ‏\( m \ge N \) | ‏\( 2^{N-1} \) | החסם לא פעיל, כל גבול פנימי חופשי. זה סעיף א |

    ---

    **המקרה הפרטי \( MPS = 256 \), ‏\( RCB = 64 \).** כאן \( m = 4 \), ‏\( N = \lceil (a + L) / 64 \rceil \)
    עם \( a = A \bmod 64 \), והמשפט נעשה:

    \[
    \mathrm{Count} = S(N) - S(N-1) + \delta,
    \]

    \[
    S(n) = \sum_{j=0}^{\lfloor n / 5 \rfloor} (-1)^j \binom{n - 4j}{j}\, 2^{\,n - 5j},
    \]

    \[
    \delta = 1 \iff N = 5 \;\text{ and }\; L \le 256 .
    \]

    הנסיגה היא \( C(n) = C(n-1) + C(n-2) + C(n-3) + C(n-4) \) והפונקציה היוצרת
    \( (1 - x) / (1 - 2x + x^5) \). עד \( n = 4 \) יש רק את האיבר \( j = 0 \), כלומר
    \( S(n) = 2^n \); מ-\( n = 5 \) נכנס האיבר \( j = 1 \), ומ-\( n = 10 \) גם \( j = 2 \):

    | ‏\( n \) | האיברים של \( S(n) \) | ‏\( S(n) \) | ‏\( S(n) - S(n-1) \) | ‏\( C_4(n) \) |
    |:-:|---|:-:|:-:|:-:|
    | 0 | ‏\( 1 \) | 1 | 1 | 1 |
    | 1 | ‏\( 2 \) | 2 | 1 | 1 |
    | 2 | ‏\( 4 \) | 4 | 2 | 2 |
    | 3 | ‏\( 8 \) | 8 | 4 | 4 |
    | 4 | ‏\( 16 \) | 16 | 8 | 8 |
    | 5 | ‏\( 32 - 1 \) | 31 | 15 | 15 |
    | 6 | ‏\( 64 - 4 \) | 60 | 29 | 29 |
    | 7 | ‏\( 128 - 12 \) | 116 | 56 | 56 |
    | 8 | ‏\( 256 - 32 \) | 224 | 108 | 108 |
    | 9 | ‏\( 512 - 80 \) | 432 | 208 | 208 |

    **בדיקה מול סעיפים א ו-ב:**

    | הבקשה | ‏\( a \) | ‏\( N \) | ‏\( \delta \) | ‏\( S(N) - S(N-1) + \delta \) | במנייה |
    |---|:-:|:-:|:-:|:-:|:-:|
    | ‏0x1000, 256 B | 0 | 4 | 0 | ‏\( 16 - 8 + 0 = \mathbf{8} \) | 8 |
    | ‏0x1010, 256 B | 16 | 5 | 1 | ‏\( 31 - 16 + 1 = \mathbf{16} \) | 16 |
    | ‏0x1000, 512 B | 0 | 8 | 0 | ‏\( 224 - 116 + 0 = \mathbf{108} \) | 108 |
    | ‏0x1010, 512 B | 16 | 9 | 0 | ‏\( 432 - 224 + 0 = \mathbf{208} \) | 208 |

    ---

    **אימות נומרי.** הנוסחה נבדקה מול ספירה ישירה (תכנון דינמי על נקודות החיתוך, בלי
    להניח כלום מההוכחה) עבור \( RCB \in \{64, 128\} \), ‏\( MPS \in \{128, 256, 512, 1024\} \),
    כל היסט \( a \) בקפיצות של 4 בתים (רזולוציית DW), וכל אורך \( L \) מ-4 עד 1596 בתים
    בקפיצות של 4, בלי לחצות גבול 4 KB: **76,608 מקרים, 0 אי-התאמות**. הבדיקה הזו רצה
    אוטומטית בבדיקות של האתר (`tests/0021`), יחד עם בדיקת \( T(N, k) \) מול מנייה מלאה.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: לספור 2 בחזקת מספר הגבולות גם כש-MPS מגביל"
    ‏\( 2^{N-1} \) נכון רק כש-\( L \le MPS \) (או באופן כללי \( m \ge N \)). בסעיף ב זה היה נותן
    128 ו-256 במקום 108 ו-208: עשרים ו-48 תת-קבוצות מכילות Completion של חמישה בלוקים
    ומעלה. מי שעונה \( 2^{N-1} \) צריך לפחות להגיד מתי זה נכון.

??? trap "מלכודת: לחשב N מתוך L במקום מתוך הכתובת"
    ‏\( 512 / 64 = 8 \), אבל בכתובת \( \texttt{0x1010} \) הבקשה נוגעת ב-**9** בלוקים. מספר
    הבלוקים הוא \( \lceil (a + L) / RCB \rceil \), ובלוקי הקצה החלקיים נספרים כבלוקים שלמים
    לצורך הספירה (למה 2). ההבדל בין 108 ל-208 כולו בגלל 16 הבתים של ההיסט.

??? trap "מלכודת: לשכוח את δ, או להוסיף אותו כשלא צריך"
    ה-\( \delta \) מופיע רק כש-\( N = m + 1 \) ו-\( L \le MPS \), ואז הוא תמיד 1. בכתובת מיושרת
    הוא אף פעם לא מופיע (‏\( f = RCB \)). מי שסופר "לפי בלוקים" בסעיף א עם הכתובת הלא מיושרת
    מקבל 15 ושוכח את `[256]`; מי שסופר "לפי תת-קבוצות" מקבל 16 ישר. שתי הדרכים נכונות אם
    זוכרים את ההנחה של כל אחת.

??? followup "שאלות המשך"
    - **‏RCB = 128:** חזרו על סעיפים א ו-ב עם \( RCB = 128 \) (‏\( m = 2 \), פיבונאצ'י). (‏2, 4, 5, 8:
      שימו לב שהבקשה הלא מיושרת של 256 בתים נוגעת בשלושה בלוקים עם \( f + e = 112 + 16 \le 128 \),
      ולכן שוב \( \delta = 1 \): ‏\( F_4 + 1 = 4 \).)
    - **מספר Completions ממוצע:** אם ה-Completer בוחר פיצול באקראי באופן אחיד, מה התוחלת של
      מספר ה-Completions? (‏\( \sum_k k \cdot T(N, k) / C_m(N) \); עבור \( N = 8 \), ‏\( m = 4 \):
      ‏\( 4.8 \) בערך.)
    - **כמה בקשות:** קריאה של 2 KB עם \( MRRS = 512 \) מתפצלת לארבע בקשות. כמה רצפי Completions
      יש לכל הקריאה? (מכפלה של ארבע ספירות, כי ה-Completions של בקשות שונות לא מתערבבים
      בתוך בקשה; סדר ההגעה בין בקשות הוא שאלה אחרת.)
    - **מה חומרה אמיתית עושה:** Root Complex טיפוסי מחזיר Completions גדולים ככל האפשר, כלומר
      פיצול אחד מתוך המאות. מה זה אומר על coverage של ה-Requester, ואיך מכריחים פיצולים
      אחרים בסימולציה? (מודל Completer עם knob על "כמה בלוקים ב-Completion", ו-bins על
      \( k \) ועל גודל ה-Completion הראשון.)
    - **גבול 4 KB:** למה הבקשה לא חוצה 4 KB, ומה היה קורה לספירה אם כן? (הבקשה עצמה אסורה;
      ה-Requester מפצל אותה, וחוזרים למקרה של כמה בקשות.)
