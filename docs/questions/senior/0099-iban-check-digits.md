---
id: 99
title: ספרות הביקורת של IBAN – בודק בחומרה, ולמה דווקא 97
level: senior
difficulty: medium
kind: design
tags: [number-theory, digits, fsm, digital-design, proof, python, systemverilog]
source: "תקן IBAN (ISO 13616) ושיטת הבדיקה ISO 7064 MOD 97-10. ה-IBAN לדוגמה הוא הדוגמה הרשמית של ישראל במרשם ה-IBAN"
added: 2026-11-07
---

## השאלה

מספר חשבון בנק בינלאומי, **IBAN**, נכתב כך :
<span dir="ltr">IL62 0108 0000 0009 9999 999</span>. ‏IL הוא קוד המדינה, 62 הן **שתי ספרות
ביקורת**, והשאר הוא מספר החשבון בישראל : בנק, סניף וחשבון. ספרות הביקורת נבחרות כך
שהבדיקה הזו יוצאת נכונה :

1. **העברה :** מעבירים את ארבעת התווים הראשונים לסוף.
2. **אותיות לספרות :** כל אות נכתבת כשתי ספרות, \( A = 10 \), \( B = 11 \) ועד
   \( Z = 35 \). ספרה נשארת כמו שהיא.
3. **הבדיקה :** המספר הארוך שמתקבל חייב לתת שארית **1** בחלוקה ל-97.

השאלה בארבעה סעיפים : לבדוק IBAN ביד ובקוד, לתכנן בודק בחומרה שמקבל ספרה בכל שעון עם
כמה שפחות פליפ-פלופים, לחשב את ספרות הביקורת, ולהבין אילו טעויות 97 תופס ולמה דווקא 97.

??? interviewer "מה המראיין בודק"
    - **חשבון מודולרי בלי מספרים ענקיים :** המספר כאן הוא בן 25 ספרות. האם המועמד מחשב את
      השארית ספרה אחרי ספרה, ויודע למה זה מותר.
    - **ספרות ביקורת מהכיוון ההפוך :** לבדוק זה דבר אחד. האם הוא יודע לחשב את שתי הספרות,
      ולהסביר למה השארית היא 1 ולא 0.
    - **הוכחה ולא רק ניסוי :** "כל טעות בספרה אחת נתפסת" צריך להוכיח מערכי המקומות
      \( 10^k \bmod 97 \), ולהסביר מה מיוחד ב-97 לעומת 100 או 99.
    - **חומרה :** האם הוא רואה מכונת מצבים של 97 מצבים, 7 פליפ-פלופים, ומממש את המעבר
      \( r \to (10r + d) \bmod 97 \) במחברים ובהשוואות בלי חילוק. האם הוא פותר את הבעיה
      שארבעת התווים הראשונים מגיעים ראשונים אבל שייכים לסוף, בלי לשמור אותם, ויודע כמה
      פליפ-פלופים הם המינימום.

---

### סעיף א – לבדוק IBAN ביד

בדקו ביד שה-IBAN ‏<span dir="ltr">IL62 0108 0000 0009 9999 999</span> תקין, בלי לחשב עם
מספר בן 25 ספרות. אחר כך כתבו פונקציה שבודקת IBAN.

??? tip "רמז 1"
    השארית של \( 10a + d \) בחלוקה ל-97 תלויה רק בשארית של \( a \). כמה מהמספר צריך לזכור
    בכל צעד?

??? tip "רמז 2"
    אות היא שתי ספרות. מה קורה לשארית כשמוסיפים שתי ספרות בבת אחת?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        **תקין :** השארית יוצאת 1. אחרי ההעברה וההמרה של \( I = 18 \) ו-\( L = 21 \) המספר
        הוא <span dir="ltr">0108000000099999999 182162</span>, ובמקום לחלק אותו מחשבים
        את השארית ספרה אחרי ספרה, \( r \leftarrow (10r + d) \bmod 97 \), ו-\( r \) תמיד
        קטן מ-97.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    אחרי ההעברה, ספרות הביקורת הן שתי הספרות האחרונות של המספר. את השארית של מספר ארוך
    לא מחשבים מהמספר עצמו : קוראים אותו משמאל לימין, וכל ספרה חדשה הופכת את המספר שנקרא
    עד עכשיו, \( a \), ל-\( 10a + d \). מספיק לזכור את השארית של \( a \), שתמיד קטנה מ-97.

    <!-- gen 0 -->

    | השלב | המחרוזת |
    |---|---|
    | כפי שנכתב | ‏<span dir="ltr">IL62 0108 0000 0009 9999 999</span> |
    | ‏4 התווים הראשונים לסוף | ‏<span dir="ltr">0108000000099999999 IL62</span> |
    | כל אות לשתי ספרות, ‏<span dir="ltr">I = 18</span> ו-<span dir="ltr">L = 21</span> | ‏<span dir="ltr">0108000000099999999 182162</span> |

    <!-- /gen -->

    כך מתקדמת השארית לאורך 25 הספרות. בכל עמודה הספרה, ומתחתיה השארית אחריה :

    <!-- gen 1 -->

    <div class="gs-scroll" tabindex="0" role="region" aria-label="הספרות של IL62 0108 0000 0009 9999 999 אחרי ההעברה, ומתחת לכל ספרה השארית בחלוקה ל-97 עד אליה. השארית בסוף היא 1"><table class="gs-bits ib-tab" dir="ltr" aria-label="הספרות של IL62 0108 0000 0009 9999 999 אחרי ההעברה, ומתחת לכל ספרה השארית בחלוקה ל-97 עד אליה. השארית בסוף היא 1"><tbody><tr><th>d</th><td class="gs-b ib-d">0</td><td class="gs-b ib-d">1</td><td class="gs-b ib-d">0</td><td class="gs-b ib-d">8</td><td class="gs-b ib-d">0</td><td class="gs-b ib-d">0</td><td class="gs-b ib-d">0</td><td class="gs-b ib-d">0</td><td class="gs-b ib-d">0</td><td class="gs-b ib-d">0</td></tr><tr class="ib-rrow"><th>r</th><td class="gs-b ib-r">0</td><td class="gs-b ib-r">1</td><td class="gs-b ib-r">10</td><td class="gs-b ib-r">11</td><td class="gs-b ib-r">13</td><td class="gs-b ib-r">33</td><td class="gs-b ib-r">39</td><td class="gs-b ib-r">2</td><td class="gs-b ib-r">20</td><td class="gs-b ib-r">6</td></tr><tr><th>d</th><td class="gs-b ib-d">0</td><td class="gs-b ib-d">9</td><td class="gs-b ib-d">9</td><td class="gs-b ib-d">9</td><td class="gs-b ib-d">9</td><td class="gs-b ib-d">9</td><td class="gs-b ib-d">9</td><td class="gs-b ib-d">9</td><td class="gs-b ib-d">9</td><td class="gs-b ib-d ib-let">1</td></tr><tr class="ib-rrow"><th>r</th><td class="gs-b ib-r">60</td><td class="gs-b ib-r">27</td><td class="gs-b ib-r">85</td><td class="gs-b ib-r">83</td><td class="gs-b ib-r">63</td><td class="gs-b ib-r">57</td><td class="gs-b ib-r">94</td><td class="gs-b ib-r">76</td><td class="gs-b ib-r">90</td><td class="gs-b ib-r">28</td></tr><tr><th>d</th><td class="gs-b ib-d ib-let">8</td><td class="gs-b ib-d ib-let">2</td><td class="gs-b ib-d ib-let">1</td><td class="gs-b ib-d ib-chk">6</td><td class="gs-b ib-d ib-chk">2</td><td class="gs-b ib-pad"></td><td class="gs-b ib-pad"></td><td class="gs-b ib-pad"></td><td class="gs-b ib-pad"></td><td class="gs-b ib-pad"></td></tr><tr class="ib-rrow"><th>r</th><td class="gs-b ib-r">94</td><td class="gs-b ib-r">69</td><td class="gs-b ib-r">12</td><td class="gs-b ib-r">29</td><td class="gs-b ib-r ib-last">1</td><td class="gs-b ib-pad"></td><td class="gs-b ib-pad"></td><td class="gs-b ib-pad"></td><td class="gs-b ib-pad"></td><td class="gs-b ib-pad"></td></tr></tbody></table></div>

    <span class="viz-legend"><span><i class="ib-key-let"></i><span>ספרות של אות (<span dir="ltr">I = 18, L = 21</span>)</span></span><span><i class="ib-key-chk"></i><span>ספרות הביקורת</span></span><span><i class="ib-key-last"></i><span>השארית בסוף, 1</span></span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ניקוי :** מורידים רווחים, ובודקים שתי אותיות, שתי ספרות, ואחריהן רק אותיות
       וספרות.
    2. **העברה :** ארבעת התווים הראשונים עוברים לסוף.
    3. **ספרות :** כל אות נכתבת כשתי ספרות, ‏\( A = 10 \) עד \( Z = 35 \).
    4. **השארית :** ‏\( r = 0 \), ולכל ספרה \( r \leftarrow (10r + d) \bmod 97 \). למשל
       אחרי <span dir="ltr">0108</span> השארית היא 11, כי \( 108 \bmod 97 = 11 \).
    5. **התשובה :** תקין אם ורק אם בסוף \( r = 1 \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="is_valid" linenums="1" hl_lines="8 9 16 24"
        import re


        def to_digits(iban):
            """The IBAN as one string of digits: the spaces out, the first four characters moved
            to the end, and every letter written as two digits (A = 10 ... Z = 35)."""
            s = iban.replace(" ", "").upper()
            s = s[4:] + s[:4]                                     # (1)!
            return "".join(str(int(c, 36)) for c in s)            # (2)!


        def mod97(digits):
            """The remainder of a long number mod 97, one digit at a time: no big numbers."""
            r = 0
            for d in digits:
                r = (10 * r + int(d)) % 97                        # (3)!
            return r


        def is_valid(iban):
            s = iban.replace(" ", "").upper()
            if not re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z0-9]+", s):
                return False                                      # (4)!
            return mod97(to_digits(s)) == 1
        ```

        1. קוד המדינה וספרות הביקורת עוברים לסוף, ולכן ספרות הביקורת הן שתי הספרות האחרונות
           של המספר. זה מה שמאפשר לחשב אותן בסעיף ג.
        2. ‏`int(c, 36)` קורא תו כספרה בבסיס 36 : התווים 0 עד 9 נשארים 0 עד 9, והאותיות A
           עד Z הן 10 עד 35. ‏`str` כותב אות כשתי ספרות.
        3. ‏\( r \) קטן מ-97, ולכן \( 10r + d \) קטן מ-970. אף מספר בחישוב לא גדול מזה.
        4. בדיקה של הצורה בלבד. בנק בודק גם את האורך של כל מדינה, 23 תווים בישראל, ולמה זה
           חשוב מופיע במלכודות.

    === "SystemVerilog"
        ```systemverilog title="function automatic bit iban_valid" linenums="1" hl_lines="11 12"
        // The value of a character: a digit 0..9, a letter 10..35
        function automatic int char_value(byte c);
          return c >= "A" ? c - "A" + 10 : c - "0";
        endfunction

        // The remainder mod 97 of the IBAN (no spaces) with its first four characters moved to
        // the end, one character at a time
        function automatic int iban_mod97(string s);
          int r = 0, v;
          for (int i = 0; i < s.len(); i++) begin
            v = char_value(s[(i + 4) % s.len()]);              // (1)!
            r = v >= 10 ? (100 * r + v) % 97 : (10 * r + v) % 97;   // (2)!
          end
          return r;
        endfunction

        function automatic bit iban_valid(string s);
          return s.len() > 4 && iban_mod97(s) == 1;
        endfunction
        ```

        1. במקום לבנות מחרוזת חדשה, קוראים מהמקום \( i + 4 \) ומסתובבים : כך ארבעת התווים
           הראשונים נקראים אחרונים.
        2. אות היא שתי ספרות, ולכן \( 100r + v \) במקום \( 10r + d \).

    #### למה זה נכון { .sol-proof }

    **השארית ספרה אחרי ספרה.** נסמן ב-\( a_k \) את המספר של \( k \) הספרות הראשונות.
    אז \( a_{k+1} = 10a_k + d \), ואם \( a_k = 97q + r \), אז
    \( a_{k+1} = 97 \cdot 10q + (10r + d) \). החלק \( 97 \cdot 10q \) מתחלק ב-97, ולכן
    \( a_{k+1} \bmod 97 = (10r + d) \bmod 97 \). באינדוקציה, אחרי כל הספרות \( r \) הוא
    בדיוק השארית של המספר כולו.

    **נסו בעצמכם.** הקלידו IBAN או בחרו דוגמה, והתקדמו ספרה אחרי ספרה. הטבלה מראה את
    הספרות אחרי ההעברה, ומתחת לכל אחת את השארית עד אליה :

    <div class="explorer" data-kind="iban"></div>

    #### סיבוכיות { .sol-cost }

    כל תו מטופל פעם אחת, בחשבון על מספרים קטנים מ-970 : זמן \( O(n) \) לאורך ה-IBAN,
    וזיכרון \( O(1) \).

---

### סעיף ב – בודק בחומרה, ספרה בכל שעון

תכננו בודק IBAN בחומרה : רגיסטרים של פליפ-פלופים מסוג D, ולוגיקה צירופית של מחברים
והשוואות, בלי חילוק. ה-IBAN מגיע כפי שהוא כתוב, ספרה אחת בכל שעון ב-4 ביטים. כל אות כבר
פוצלה לשתי הספרות שלה, ולכן 6 הספרות הראשונות הן הראש : שתי האותיות ושתי ספרות הביקורת,
שאחרי ההעברה שייכות לסוף. עם הספרה האחרונה מגיע האות `last`, ובאותו שעון הבודק אומר אם
ה-IBAN תקין. כמה פליפ-פלופים צריך, וכמה שעונים? ואיך מקטינים את שניהם?

??? tip "רמז 1"
    כמה ערכים שונים יכולה לקבל השארית? כמה פליפ-פלופים צריך כדי לזכור אחד מהם?

??? tip "רמז 2"
    הראש מגיע ראשון אבל שייך לסוף. אם \( R \) הוא המספר של השאר ו-\( H \) המספר של 6
    ספרות הראש, המספר כולו הוא \( R \cdot 10^6 + H \). מה זה \( 10^6 \bmod 97 \)?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **‏14 פליפ-פלופים ו-25 שעונים.** הבודק הוא מכונת מצבים של השארית : 97 מצבים, 7
        פליפ-פלופים, ובכל שעון \( r \to (10r + d) \bmod 97 \), שהלוגיקה מחשבת כ-\( 8r + 2r + d \)
        ועוד ארבעה שלבים של השוואה וחיסור. את הראש לא שומרים : שארית נפרדת \( h \) לשש
        הספרות הראשונות, ובסוף בודקים \( (27r + h) \bmod 97 = 1 \), כי \( 10^6 \equiv 27 \).
        את ספרות הראש סופרים בערכים 97 עד 102 של \( r \), שאף שארית לא משתמשת בהם. ‏14 הוא
        גם המינימום : יש 9,409 זוגות \( (h, r) \) שהבודק חייב להבדיל ביניהם, יותר
        מ-\( 2^{13} \).

    <!-- cost: פליפ-פלופים 14 | שעונים 25 | שלבים 4 בשעון -->

    #### הרעיון { .sol-idea }

    בסעיף א ראינו שאחרי כל ספרה מספיק לזכור את השארית של מה שנקרא עד עכשיו. לכן הבודק הוא
    **מכונת מצבים** : מצב לכל שארית, 0 עד 96, ובכל שעון מעבר לפי הספרה,
    \( r \to (10r + d) \bmod 97 \). כך נראית אותה מכונה כשמחלקים ב-3 במקום ב-97 : שלושה
    מצבים, ו-\( 10 \equiv 1 \pmod 3 \), כך שכל ספרה מוסיפה לשארית את השארית שלה עצמה :

    <!-- gen 2 -->

    <svg class="figure ih-fig" viewBox="0 0 380 350" style="max-width:23.75rem" role="img" aria-label="מכונת המצבים של השארית בחלוקה ל-3 : שלושה מצבים, 0, 1 ו-2. מכל מצב ספרה מקבוצה 0, 3, 6, 9 משאירה במקום, ספרה מקבוצה 1, 4, 7 מוסיפה 1, וספרה מקבוצה 2, 5, 8 מוסיפה 2, מודולו 3. ההתחלה ב-0, ו-0 הוא גם המצב שבו המספר מתחלק ב-3"><defs><marker id="ih-h3" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="ih-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs><path class="ih-edge ih-e1" d="M198.6,130.1 Q222.9,203.6 285.3,244.3" marker-end="url(#ih-h3)"/><text class="ih-lab ih-e1" x="222.9" y="207.6" text-anchor="middle">1,4,7</text><path class="ih-edge ih-e2" d="M167.1,119.3 Q102.9,162.4 80.4,233.5" marker-end="url(#ih-h3)"/><text class="ih-lab ih-e2" x="102.9" y="166.4" text-anchor="middle">2,5,8</text><path class="ih-edge ih-e1" d="M284.0,253.0 Q190.0,228.0 99.0,253.0" marker-end="url(#ih-h3)"/><text class="ih-lab ih-e1" x="190.0" y="232.0" text-anchor="middle">1,4,7</text><path class="ih-edge ih-e2" d="M301.4,235.9 Q277.1,162.4 214.7,121.7" marker-end="url(#ih-h3)"/><text class="ih-lab ih-e2" x="277.1" y="166.4" text-anchor="middle">2,5,8</text><path class="ih-edge ih-e1" d="M92.9,246.7 Q157.1,203.6 179.6,132.5" marker-end="url(#ih-h3)"/><text class="ih-lab ih-e1" x="157.1" y="207.6" text-anchor="middle">1,4,7</text><path class="ih-edge ih-e2" d="M96.0,271.0 Q190.0,296.0 281.0,271.0" marker-end="url(#ih-h3)"/><text class="ih-lab ih-e2" x="190.0" y="300.0" text-anchor="middle">2,5,8</text><path class="ih-edge ih-e0" d="M178,82 C160,42 220,42 202,80" marker-end="url(#ih-h3)"/><text class="ih-lab" x="190" y="38" text-anchor="middle">0,3,6,9</text><g class="ih-state ih-start"><circle cx="190" cy="104" r="26"/><text x="190" y="110" text-anchor="middle">0</text></g><path class="ih-edge ih-e0" d="M298,284 C280,324 340,324 322,286" marker-end="url(#ih-h3)"/><text class="ih-lab" x="310" y="338" text-anchor="middle">0,3,6,9</text><g class="ih-state"><circle cx="310" cy="262" r="26"/><text x="310" y="268" text-anchor="middle">1</text></g><path class="ih-edge ih-e0" d="M58,284 C40,324 100,324 82,286" marker-end="url(#ih-h3)"/><text class="ih-lab" x="70" y="338" text-anchor="middle">0,3,6,9</text><g class="ih-state"><circle cx="70" cy="262" r="26"/><text x="70" y="268" text-anchor="middle">2</text></g></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="ih-key-start"></i>ההתחלה, ומתחלק ב-3</span><span><i class="ih-key-e0"></i>ספרות שלא משנות את השארית</span><span><i class="ih-key-e1"></i>מוסיפות 1</span><span><i class="ih-key-e2"></i>מוסיפות 2</span></span>

    <!-- /gen -->

    ב-97 יש 97 מצבים ו-970 קשתות, יותר מדי לציור אחד. כך נראות הקשתות של שני מצבים : ממצב
    1 הספרה \( d \) מובילה ל-\( 10 + d \), וממצב 96 ל-\( (960 + d) \bmod 97 = 87 + d \) :

    <!-- gen 4 -->

    <svg class="figure ih-fig" viewBox="0 0 420 330" style="max-width:26.25rem" role="img" aria-label="שני מצבים של מכונת השארית מודולו 97 : ממצב 1 עשר קשתות, לספרות 0 עד 9, אל המצבים 10 עד 19. ממצב 96 עשר קשתות אל המצבים 87 עד 96, כי 960 מודולו 97 הוא 87"><defs><marker id="ih-hf" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="ih-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs><g class="ih-state ih-src"><circle cx="40" cy="160" r="22"/><text x="40" y="166" text-anchor="middle">1</text></g><path class="ih-edge" d="M62,160 C110,160 110,18 152,18" marker-end="url(#ih-hf)"/><text class="ih-lab" x="132" y="14" text-anchor="middle">0</text><g class="ih-state ih-small"><circle cx="172" cy="18" r="15"/><text x="172" y="23" text-anchor="middle">10</text></g><path class="ih-edge" d="M62,160 C110,160 110,50 152,50" marker-end="url(#ih-hf)"/><text class="ih-lab" x="132" y="46" text-anchor="middle">1</text><g class="ih-state ih-small"><circle cx="172" cy="50" r="15"/><text x="172" y="55" text-anchor="middle">11</text></g><path class="ih-edge" d="M62,160 C110,160 110,82 152,82" marker-end="url(#ih-hf)"/><text class="ih-lab" x="132" y="78" text-anchor="middle">2</text><g class="ih-state ih-small"><circle cx="172" cy="82" r="15"/><text x="172" y="87" text-anchor="middle">12</text></g><path class="ih-edge" d="M62,160 C110,160 110,114 152,114" marker-end="url(#ih-hf)"/><text class="ih-lab" x="132" y="110" text-anchor="middle">3</text><g class="ih-state ih-small"><circle cx="172" cy="114" r="15"/><text x="172" y="119" text-anchor="middle">13</text></g><path class="ih-edge" d="M62,160 C110,160 110,146 152,146" marker-end="url(#ih-hf)"/><text class="ih-lab" x="132" y="142" text-anchor="middle">4</text><g class="ih-state ih-small"><circle cx="172" cy="146" r="15"/><text x="172" y="151" text-anchor="middle">14</text></g><path class="ih-edge" d="M62,160 C110,160 110,178 152,178" marker-end="url(#ih-hf)"/><text class="ih-lab" x="132" y="174" text-anchor="middle">5</text><g class="ih-state ih-small"><circle cx="172" cy="178" r="15"/><text x="172" y="183" text-anchor="middle">15</text></g><path class="ih-edge" d="M62,160 C110,160 110,210 152,210" marker-end="url(#ih-hf)"/><text class="ih-lab" x="132" y="206" text-anchor="middle">6</text><g class="ih-state ih-small"><circle cx="172" cy="210" r="15"/><text x="172" y="215" text-anchor="middle">16</text></g><path class="ih-edge" d="M62,160 C110,160 110,242 152,242" marker-end="url(#ih-hf)"/><text class="ih-lab" x="132" y="238" text-anchor="middle">7</text><g class="ih-state ih-small"><circle cx="172" cy="242" r="15"/><text x="172" y="247" text-anchor="middle">17</text></g><path class="ih-edge" d="M62,160 C110,160 110,274 152,274" marker-end="url(#ih-hf)"/><text class="ih-lab" x="132" y="270" text-anchor="middle">8</text><g class="ih-state ih-small"><circle cx="172" cy="274" r="15"/><text x="172" y="279" text-anchor="middle">18</text></g><path class="ih-edge" d="M62,160 C110,160 110,306 152,306" marker-end="url(#ih-hf)"/><text class="ih-lab" x="132" y="302" text-anchor="middle">9</text><g class="ih-state ih-small"><circle cx="172" cy="306" r="15"/><text x="172" y="311" text-anchor="middle">19</text></g><g class="ih-state ih-src"><circle cx="236" cy="160" r="22"/><text x="236" y="166" text-anchor="middle">96</text></g><path class="ih-edge" d="M258,160 C306,160 306,18 348,18" marker-end="url(#ih-hf)"/><text class="ih-lab" x="328" y="14" text-anchor="middle">0</text><g class="ih-state ih-small"><circle cx="368" cy="18" r="15"/><text x="368" y="23" text-anchor="middle">87</text></g><path class="ih-edge" d="M258,160 C306,160 306,50 348,50" marker-end="url(#ih-hf)"/><text class="ih-lab" x="328" y="46" text-anchor="middle">1</text><g class="ih-state ih-small"><circle cx="368" cy="50" r="15"/><text x="368" y="55" text-anchor="middle">88</text></g><path class="ih-edge" d="M258,160 C306,160 306,82 348,82" marker-end="url(#ih-hf)"/><text class="ih-lab" x="328" y="78" text-anchor="middle">2</text><g class="ih-state ih-small"><circle cx="368" cy="82" r="15"/><text x="368" y="87" text-anchor="middle">89</text></g><path class="ih-edge" d="M258,160 C306,160 306,114 348,114" marker-end="url(#ih-hf)"/><text class="ih-lab" x="328" y="110" text-anchor="middle">3</text><g class="ih-state ih-small"><circle cx="368" cy="114" r="15"/><text x="368" y="119" text-anchor="middle">90</text></g><path class="ih-edge" d="M258,160 C306,160 306,146 348,146" marker-end="url(#ih-hf)"/><text class="ih-lab" x="328" y="142" text-anchor="middle">4</text><g class="ih-state ih-small"><circle cx="368" cy="146" r="15"/><text x="368" y="151" text-anchor="middle">91</text></g><path class="ih-edge" d="M258,160 C306,160 306,178 348,178" marker-end="url(#ih-hf)"/><text class="ih-lab" x="328" y="174" text-anchor="middle">5</text><g class="ih-state ih-small"><circle cx="368" cy="178" r="15"/><text x="368" y="183" text-anchor="middle">92</text></g><path class="ih-edge" d="M258,160 C306,160 306,210 348,210" marker-end="url(#ih-hf)"/><text class="ih-lab" x="328" y="206" text-anchor="middle">6</text><g class="ih-state ih-small"><circle cx="368" cy="210" r="15"/><text x="368" y="215" text-anchor="middle">93</text></g><path class="ih-edge" d="M258,160 C306,160 306,242 348,242" marker-end="url(#ih-hf)"/><text class="ih-lab" x="328" y="238" text-anchor="middle">7</text><g class="ih-state ih-small"><circle cx="368" cy="242" r="15"/><text x="368" y="247" text-anchor="middle">94</text></g><path class="ih-edge" d="M258,160 C306,160 306,274 348,274" marker-end="url(#ih-hf)"/><text class="ih-lab" x="328" y="270" text-anchor="middle">8</text><g class="ih-state ih-small"><circle cx="368" cy="274" r="15"/><text x="368" y="279" text-anchor="middle">95</text></g><path class="ih-edge" d="M258,160 C306,160 306,306 348,306" marker-end="url(#ih-hf)"/><text class="ih-lab" x="328" y="302" text-anchor="middle">9</text><g class="ih-state ih-small"><circle cx="368" cy="306" r="15"/><text x="368" y="311" text-anchor="middle">96</text></g></svg>

    <!-- /gen -->

    **מהמצבים לפליפ-פלופים.** ‏97 מצבים צריכים \( \lceil \log_2 97 \rceil = 7 \) ביטים. הקידוד
    הטבעי הוא השארית עצמה בבינארי, וכך הלוגיקה של המעבר היא חשבון : ‏\( 10r = 8r + 2r \) הוא
    שתי הזזות ומחבר, ‏\( 10r + d \) לכל היותר 969, עשרה ביטים, ואת המודולו מקבלים בארבעה
    שלבים, שכל אחד מהם משווה ומחסר כפולה של 97, מהגדולה לקטנה :

    <!-- gen 5 -->

    <svg class="figure ih-fig ih-dp" viewBox="0 0 400 470" style="max-width:25rem" role="img" aria-label="תרשים המלבנים של הבודק עם 14 פליפ-פלופים : שני רגיסטרים של 7 ביטים, h ו-r. מרבב בוחר את h בזמן הראש ואת r אחריו, מחשבים 8x ועוד 2x ועוד d, ואז ארבעה שלבים של השוואה וחיסור של 776, 388, 194 ו-97. בזמן הראש r סופר 97 ועוד k. בספרה האחרונה מחשבים 27r ועוד h מודולו 97 ובודקים שזה 1"><defs><marker id="ih-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="ih-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs><g class="ih-blk ih-in"><rect x="150" y="10" width="100" height="30" rx="5"/><text x="200" y="30" text-anchor="middle">d[3:0]</text></g><g class="ih-blk ih-reg"><rect x="30" y="60" width="110" height="40" rx="5"/><text x="85" y="80" text-anchor="middle">h</text><text class="ih-sub" x="85" y="95" text-anchor="middle">7 D flip-flops</text></g><g class="ih-blk ih-reg"><rect x="260" y="60" width="110" height="40" rx="5"/><text x="315" y="80" text-anchor="middle">r</text><text class="ih-sub" x="315" y="95" text-anchor="middle">7 D flip-flops</text></g><g class="ih-blk ih-mux"><rect x="150" y="128" width="100" height="34" rx="5"/><text x="200" y="150" text-anchor="middle">mux: r ≥ 97 ?</text></g><path class="ih-wire" d="M85,100 L85,145 L150,145" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M315,100 L315,145 L250,145" marker-end="url(#ih-hb)"/><g class="ih-blk ih-add"><rect x="110" y="186" width="180" height="40" rx="5"/><text x="200" y="206" text-anchor="middle">8x + 2x + d</text><text class="ih-sub" x="200" y="221" text-anchor="middle">two adders, ≤ 969</text></g><path class="ih-wire" d="M200,162 L200,186" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M200,40 L200,52 L380,52 L380,206 L290,206" marker-end="url(#ih-hb)"/><g class="ih-blk ih-stage"><rect x="16" y="250" width="86" height="40" rx="5"/><text x="59" y="270" text-anchor="middle">≥ 776 ?</text><text class="ih-sub" x="59" y="285" text-anchor="middle">− 776</text></g><g class="ih-blk ih-stage"><rect x="110" y="250" width="86" height="40" rx="5"/><text x="153" y="270" text-anchor="middle">≥ 388 ?</text><text class="ih-sub" x="153" y="285" text-anchor="middle">− 388</text></g><path class="ih-wire" d="M102,270 L110,270" marker-end="url(#ih-hb)"/><g class="ih-blk ih-stage"><rect x="204" y="250" width="86" height="40" rx="5"/><text x="247" y="270" text-anchor="middle">≥ 194 ?</text><text class="ih-sub" x="247" y="285" text-anchor="middle">− 194</text></g><path class="ih-wire" d="M196,270 L204,270" marker-end="url(#ih-hb)"/><g class="ih-blk ih-stage"><rect x="298" y="250" width="86" height="40" rx="5"/><text x="341" y="270" text-anchor="middle">≥ 97 ?</text><text class="ih-sub" x="341" y="285" text-anchor="middle">− 97</text></g><path class="ih-wire" d="M290,270 L298,270" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M200,226 L200,238 L59,238 L59,250" marker-end="url(#ih-hb)"/><g class="ih-blk ih-mux"><rect x="110" y="314" width="180" height="40" rx="5"/><text x="200" y="334" text-anchor="middle">write h or r</text><text class="ih-sub" x="200" y="349" text-anchor="middle">head: r ← r + 1</text></g><path class="ih-wire" d="M345,290 L345,304 L290,324" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M110,334 L14,334 L14,80 L30,80" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M290,334 L392,334 L392,80 L370,80" marker-end="url(#ih-hb)"/><g class="ih-blk ih-add"><rect x="30" y="380" width="150" height="40" rx="5"/><text x="105" y="400" text-anchor="middle">27r + h</text><text class="ih-sub" x="105" y="415" text-anchor="middle">at the last digit</text></g><g class="ih-blk ih-stage"><rect x="200" y="380" width="90" height="40" rx="5"/><text x="245" y="400" text-anchor="middle">5 stages</text><text class="ih-sub" x="245" y="415" text-anchor="middle">mod 97</text></g><g class="ih-blk ih-out"><rect x="310" y="380" width="70" height="40" rx="5"/><text x="345" y="400" text-anchor="middle">= 1 ?</text><text class="ih-sub" x="345" y="415" text-anchor="middle">ok</text></g><path class="ih-wire" d="M180,400 L200,400" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M290,400 L310,400" marker-end="url(#ih-hb)"/><text class="ih-sub" x="200" y="452" text-anchor="middle">critical path: mux, two adders, four stages</text></svg>

    <!-- /gen -->

    **הראש.** הדרך הישירה שומרת את 6 ספרות הראש, 24 פליפ-פלופים, ומכניסה אותן שוב אחרי
    השאר, בשישה שעונים נוספים. אבל \( 10^6 \equiv 27 \pmod{97} \), ולכן מספיק לשמור את
    השארית של הראש, \( h \) : בסוף \( N \bmod 97 = (27r + h) \bmod 97 \). את מספר ספרות הראש
    צריך לספור, וכאן נחסכים עוד פליפ-פלופים : בזמן הראש \( r \) לא בשימוש, ושארית אף פעם לא
    מגיעה ל-97. לכן \( r = 97 + k \) אומר "ספרה \( k \) של הראש", ואין צורך במונה :

    <!-- gen 6 -->

    | הגרסה | פליפ-פלופים | שעונים ל-IBAN הישראלי |
    |---|:-:|:-:|
    | שומרים את 6 ספרות הראש ומכניסים אותן שוב בסוף | ‏<span dir="ltr">24 + 3 + 7 = 34</span> | 31 |
    | שתי שאריות, h לראש ו-r לשאר, ומונה לראש | ‏<span dir="ltr">7 + 7 + 3 = 17</span> | 25 |
    | המונה בתוך r, שלא בשימוש בזמן הראש, ועוד ביט של שלב | ‏<span dir="ltr">7 + 7 + 1 = 15</span> | 25 |
    | הערכים 97 עד 102 של r הם שלבי הראש | ‏<span dir="ltr">7 + 7 = 14</span> | 25 |

    <!-- /gen -->

    **מהר יותר.** ‏\( 100 = 97 + 3 \), ולכן שתי ספרות בבת אחת הן \( (3r + 10a + b) \bmod 97 \).
    הסכום לכל היותר 387, ומספיקים שני שלבים, 194 ו-97 : חצי מהשעונים, ונתיב קצר יותר. אות
    שלמה בשעון אחד היא אותו רעיון, \( (3r + v) \bmod 97 \) :

    <!-- gen 7 -->

    | בכל שעון | הצעד | השלבים | שעונים ל-IBAN הישראלי |
    |---|---|:-:|:-:|
    | ספרה, 4 ביטים | ‏<span dir="ltr">(10r + d) mod 97</span> | 4 | 25 |
    | תו, 6 ביטים, אות כערך אחד | ‏<span dir="ltr">(3r + v) mod 97</span> לאות | 4 | 23 |
    | שתי ספרות, 8 ביטים | ‏<span dir="ltr">(3r + 10a + b) mod 97</span> | 2 | 13 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **השארית :** רגיסטר \( r \) של 7 פליפ-פלופים. בכל שעון \( s = 8r + 2r + d \), ואחריו
       ארבעה שלבים : אם \( s \ge 776 \) מחסרים 776, וכך גם 388, ‏194 ו-97.
    2. **הראש :** רגיסטר \( h \) של 7 פליפ-פלופים מקבל את שש הספרות הראשונות באותו צעד, דרך
       מרבב שבוחר בין \( h \) ל-\( r \).
    3. **הספירה :** אחרי איפוס \( r = 97 \). כל ספרת ראש מעלה את \( r \) ב-1, ואחרי
       השישית, ב-\( r = 102 \), ‏\( r \leftarrow 0 \).
    4. **התשובה :** בשעון של הספרה האחרונה, \( (27r + h) \bmod 97 = 1 \), עם
       \( 27r = 16r + 8r + 2r + r \) וחמישה שלבים, 1552 עד 97.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="check_stream" linenums="1" hl_lines="4 5 6 7 31 32 33"
        def step(r, d):
            """(10r + d) mod 97 the way the hardware does it: shifts and adders, then four
            compare-and-subtract stages. No division."""
            s = (r << 3) + (r << 1) + d                          # (1)!
            for m in (776, 388, 194, 97):                        # (2)!
                if s >= m:
                    s -= m
            return s


        def finish(r, h):
            """(27r + h) mod 97: the head's 6 digits come after the rest, and 10^6 = 27 mod 97."""
            s = (r << 4) + (r << 3) + (r << 1) + r + h           # 27r + h, at most 2688
            for m in (1552, 776, 388, 194, 97):
                if s >= m:
                    s -= m
            return s


        def stream(iban):
            """The digits as they arrive: the IBAN as written, every letter as two digits."""
            s = iban.replace(" ", "").upper()
            return [int(c) for c in "".join(str(int(ch, 36)) for ch in s)]


        def check_stream(digits):
            """The checker, a digit a clock, with two 7-bit registers and nothing else:
            r = 97 + k means "digit k of the head", which no remainder can be."""
            h, r = 0, 97                                         # (3)!
            for d in digits:
                if r >= 97:
                    h = step(h, d)
                    r = 0 if r == 102 else r + 1
                else:
                    r = step(r, d)
            return r < 97 and finish(r, h) == 1
        ```

        1. ‏`r << 3` הוא \( 8r \) ו-`r << 1` הוא \( 2r \) : בחומרה אלה רק חוטים, והסכום הוא
           שני מחברים. ‏\( 10 \cdot 96 + 9 = 969 \), עשרה ביטים.
        2. ארבעה שלבים, כפולות של 97 מהגדולה לקטנה : 8, 4, 2 ו-1 כפול 97. כל שלב הוא מחסר
           שהלווה שלו אומר אם \( s \ge m \), ומרבב שבוחר את \( s \) או את \( s - m \).
        3. המצב אחרי איפוס : \( r = 97 \), ספרה 0 של הראש. ‏14 הפליפ-פלופים הם \( h \) ו-\( r \).

    === "SystemVerilog"
        ```systemverilog title="module iban_checker" linenums="1" hl_lines="11 15 16 17 18 19 35 37 38"
        // One digit a clock: the IBAN as written, every letter already split into its two
        // digits, so the first 6 digits are the head. 14 flip-flops: h and r.
        module iban_checker (
          input  logic       clk, rst_n,
          input  logic       start,          // a new IBAN: this clock's digit is its first
          input  logic       valid,          // d holds a digit this clock
          input  logic       last,           // d is the IBAN's last digit
          input  logic [3:0] d,
          output logic       ok);            // with last: the IBAN is valid

          logic [6:0] h, r;                  // r = 97 + k: digit k of the head

          function automatic logic [6:0] step(logic [6:0] x, logic [3:0] v);
            logic [9:0] s;
            s = {x, 3'b000} + {x, 1'b0} + 10'(v);       // 8x + 2x + v, at most 969
            if (s >= 776) s -= 776;
            if (s >= 388) s -= 388;
            if (s >= 194) s -= 194;
            if (s >= 97)  s -= 97;
            return s[6:0];
          endfunction

          function automatic logic [6:0] finish(logic [6:0] x, logic [6:0] y);
            logic [11:0] s;
            s = {x, 4'b0} + {x, 3'b0} + {x, 1'b0} + 12'(x) + 12'(y);   // 27x + y
            if (s >= 1552) s -= 1552;
            if (s >= 776)  s -= 776;
            if (s >= 388)  s -= 388;
            if (s >= 194)  s -= 194;
            if (s >= 97)   s -= 97;
            return s[6:0];
          endfunction

          wire [6:0] rr = start ? 7'd97 : r, hh = start ? 7'd0 : h;
          wire       head = rr >= 7'd97;
          wire [6:0] h_next = head ? step(hh, d) : hh;
          wire [6:0] r_next = head ? (rr == 7'd102 ? 7'd0 : rr + 7'd1) : step(rr, d);
          assign ok = valid && last && !head && finish(r_next, h_next) == 7'd1;

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin h <= '0; r <= 7'd97; end
            else if (valid) begin h <= h_next; r <= r_next; end
        endmodule
        ```

    #### למה זה נכון { .sol-proof }

    **השלבים.** לפני השלב של \( m \) מתקיים \( s < 2m \) : בהתחלה \( s \le 969 < 1552 \).
    אם \( s \ge m \) מחסרים \( m \), ובכל מקרה אחרי השלב \( s < m \), שזה בדיוק התנאי לשלב
    הבא, \( m/2 \). אחרי השלב של 97 ‏\( s < 97 \), ורק כפולות של 97 הוחסרו, ולכן
    \( s = (10r + d) \bmod 97 \). אותו טיעון ל-\( 27r + h \le 2688 < 3104 \) עם חמישה שלבים.

    **הראש בסוף.** אחרי ההעברה המספר הוא \( N = R \cdot 10^6 + H \), כש-\( H \) הוא המספר של
    6 ספרות הראש. ‏\( 10^6 = 97 \cdot 10309 + 27 \), ולכן
    \( N \equiv 27 \cdot (R \bmod 97) + (H \bmod 97) \pmod{97} \) : שתי השאריות מחושבות
    כשהספרות מגיעות, כל אחת באותה מכונה, ונפגשות רק בסוף.

    **הקודים 97 עד 102.** שארית תמיד קטנה מ-97, ולכן ערך של \( r \) מ-97 ומעלה לא יכול להיות
    שארית, והבודק יודע בכל שעון אם הוא בראש או בשאר בלי פליפ-פלופ נוסף.

    **למה 14 הוא המינימום.** בזמן השאר הבודק חייב להבדיל בין כל שני זוגות שונים
    \( (h, r) \) ו-\( (h', r') \) : יש המשך שעבורו האחד תקין והשני לא. אם \( r = r' \), המשך
    שמשלים את הראשון ל-1 משאיר את השני ב-\( 1 + h' - h \ne 1 \). אם \( r \ne r' \), המשך של
    \( k \) ספרות שמשלים את הראשון משאיר את השני ב-\( 1 + 27 \cdot 10^k (r' - r) + (h' - h) \).
    כדי ששני ההמשכים, באורך 2 ובאורך 3, יתנו 1 בשניהם, היה צריך
    \( 27 \cdot 900 \cdot (r' - r) \equiv 0 \), ו-97 ראשוני שלא מחלק אף גורם. לכן יש
    \( 97 \cdot 97 = 9409 \) מצבים שונים, יותר מ-\( 2^{13} = 8192 \), ו-13 פליפ-פלופים לא
    מספיקים.

    **נסו בעצמכם.** התקדמו ספרה אחרי ספרה ובחרו גרסה. התיבה מראה בכל שעון את הפליפ-פלופים,
    ביט אחרי ביט, ואת המצב של המכונה עם עשר הקשתות שלו :

    <div class="explorer" data-kind="ibanhw"></div>

    #### סיבוכיות { .sol-cost }

    שעון לכל ספרה, 25 שעונים ל-IBAN ישראלי, והתשובה באותו שעון של הספרה האחרונה. בכל שעון
    הנתיב הארוך הוא מרבב, שני מחברים וארבעה שלבים של השוואה וחיסור. בסוף עוד מחבר של
    \( 27r + h \) וחמישה שלבים, פעם אחת. ‏14 פליפ-פלופים, המינימום.

---

### סעיף ג – לחשב את ספרות הביקורת

מקבלים IBAN בלי ספרות ביקורת : קוד מדינה ומספר חשבון. איך מחשבים את שתי הספרות? הוכיחו
שאחרי החישוב השארית יוצאת בדיוק 1, והסבירו למה הנוסחה היא \( 98 - m \) ולא \( 97 - m \).

??? tip "רמז 1"
    אחרי ההעברה, ספרות הביקורת הן שתי הספרות האחרונות. מה קורה לשארית כששמים בהן 00?

??? tip "רמז 2"
    אם השארית עם 00 היא \( m \), ושמים במקומן מספר \( c \), השארית הופכת ל-\( m + c \),
    מודולו 97. איזה \( c \) נותן 1?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        שמים **00** במקום ספרות הביקורת, מחשבים את השארית \( m \), וספרות הביקורת הן
        \( 98 - m \), בשתי ספרות. ב-IBAN לדוגמה \( m = 36 \) ו-\( 98 - 36 = 62 \). השארית
        יוצאת 1 כי \( m + 98 - m = 98 = 97 + 1 \). כך ספרות הביקורת תמיד בין 02 ל-98, ולעולם
        לא 00 או 01.

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    ספרות הביקורת הן שתי הספרות האחרונות של המספר, ולכן הן פשוט **מתווספות** לו : אם
    המספר עם 00 הוא \( N_0 \), המספר עם ספרות הביקורת \( c \) הוא \( N_0 + c \). נשאר לבחור
    \( c \) כך ש-\( N_0 + c \) ייתן שארית 1.

    <!-- gen 8 -->

    | ה-IBAN | השארית עם 00 | ‏98 פחות השארית | ספרות הביקורת שבו |
    |---|:-:|:-:|:-:|
    | ‏<span dir="ltr">IL00 0108 0000 0009 9999 999</span> | 36 | 62 | 62 |
    | ‏<span dir="ltr">GB00 WEST 1234 5698 7654 32</span> | 16 | 82 | 82 |
    | ‏<span dir="ltr">DE00 3704 0044 0532 0130 00</span> | 9 | 89 | 89 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏00 במקומן :** את התווים 3 ו-4 מחליפים ב-00.
    2. **השארית :** ‏\( m \) היא השארית של המספר בחלוקה ל-97, כמו בסעיף א.
    3. **ספרות הביקורת :** ‏\( 98 - m \), עם 0 מקדים כשהוא קטן מ-10.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="check_digits" linenums="1" hl_lines="4 5"
        def check_digits(iban):
            """The two check digits of an IBAN: 00 in their place, the remainder m, then 98 - m."""
            s = iban.replace(" ", "").upper()
            m = mod97(to_digits(s[:2] + "00" + s[4:]))           # (1)!
            return f"{98 - m:02d}"                               # (2)!
        ```

        1. מה שכתוב כרגע בתווים 3 ו-4 לא משנה : במקומם שמים 00. את `mod97` ו-`to_digits`
           כתבנו בסעיף א.
        2. ‏‏`02d` כותב תמיד שתי ספרות. \( m \) בין 0 ל-96, ולכן התוצאה בין 02 ל-98.

    === "SystemVerilog"
        ```systemverilog title="function automatic int iban_check_digits" linenums="1" hl_lines="3"
        // The two check digits: the remainder m with 00 in their place, then 98 - m (iban_mod97 of part a)
        function automatic int iban_check_digits(string s);
          return 98 - iban_mod97({s.substr(0, 1), "00", s.substr(4, s.len() - 1)});
        endfunction
        ```

    #### למה זה נכון { .sol-proof }

    **השארית 1.** אחרי ההעברה המספר הוא \( N = N_0 + c \), כש-\( N_0 \) הוא המספר עם 00
    ו-\( c \) המספר של שתי ספרות הביקורת, כי הן שתי הספרות האחרונות. אם \( N_0 \bmod 97 = m \)
    ו-\( c = 98 - m \), אז \( N \equiv m + 98 - m = 98 \equiv 1 \pmod{97} \). להפך, אם
    \( N \equiv 1 \), אז \( c \equiv 98 - m \pmod{97} \) : ספרות הביקורת נקבעות עד כדי 97.
    בין 00 ל-99 יכולים להיות שני ערכים כאלה, למשל 01 ו-98 כש-\( m = 0 \), והתקן בוחר תמיד
    ב-\( 98 - m \). לכן לכל חשבון יש ספרות ביקורת אחת ויחידה.

    **‏98 ולא 97.** ‏\( m \) הוא שארית, בין 0 ל-96, ולכן \( 98 - m \) בין 2 ל-98. עם
    \( 97 - m \) השארית של IBAN תקין הייתה 0, וספרות הביקורת היו בין 01 ל-97. התקן
    (ISO 7064, ‏MOD 97-10) בחר בשארית 1, וכך הצירופים 00 ו-01 לא מופיעים אף פעם כספרות
    ביקורת. בפרט 00, שבו משתמשים בזמן החישוב, לעולם אינו ספרות הביקורת של IBAN אמיתי.

    #### סיבוכיות { .sol-cost }

    חישוב אחד של שארית : זמן \( O(n) \) וזיכרון \( O(1) \).

---

### סעיף ד – מה 97 תופס, ולמה דווקא 97

הוכיחו שכל טעות בספרה אחת, וכל החלפה של שתי ספרות שכנות, משנות את השארית. אילו טעויות
עוברות בלי שהבדיקה תרגיש? ולמה בוחרים דווקא 97, ולא 100, 99 או 98?

??? tip "רמז 1"
    טעות בספרה שערך המקום שלה \( 10^k \) משנה את המספר ב-\( (b - a) \cdot 10^k \). מתי
    השינוי הזה מתחלק ב-97?

??? tip "רמז 2"
    ‏97 ראשוני. מה זה אומר על מכפלה של שני מספרים שאף אחד מהם לא מתחלק ב-97?

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        טעות נתפסת אם ורק אם היא משנה את המספר בסכום **שאינו** כפולה של 97. ספרה אחת שגויה
        משנה אותו ב-\( (b - a) \cdot 10^k \), והחלפה של שכנות ב-\( 9(b - a) \cdot 10^k \).
        ‏97 ראשוני ואינו מחלק אף אחד מהגורמים, ולכן גם לא את המכפלה : הן תמיד נתפסות. יותר
        מזה, ‏\( 10^d \equiv 1 \pmod{97} \) רק כש-96 מחלק את \( d \), ולכן כל החלפה של שתי
        ספרות ב-IBAN נתפסת. מה שעובר הוא בערך 1 מכל 97 טעויות "אקראיות", למשל שתי ספרות
        שגויות שהשינוי שלהן יחד הוא כפולה של 97 :
        <span dir="ltr">…99</span> ל-<span dir="ltr">…02</span>.

    <!-- cost: ספרה שגויה 100% | החלפה 100% | שתי ספרות כ-99% -->

    #### הרעיון { .sol-idea }

    הבדיקה רואה רק את השארית. טעות שמשנה את המספר ב-\( \Delta \) משנה את השארית
    ב-\( \Delta \bmod 97 \), ולכן היא עוברת בדיוק כש-97 מחלק את \( \Delta \). לכל סוג של
    טעות כותבים את \( \Delta \) כמכפלה, ושואלים אם 97 יכול לחלק אותה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ספרה אחת :** ‏\( a \) הופכת ל-\( b \) במקום \( 10^k \), ו-\( \Delta = (b - a) \cdot 10^k \).
    2. **שכנות :** ‏\( ab \) הופכות ל-\( ba \) במקומות \( 10^{k+1} \) ו-\( 10^k \), ו-
       \( \Delta = (b - a)(10^{k+1} - 10^k) = 9(b - a) \cdot 10^k \).
    3. **כל החלפה :** ספרות במרחק \( d \) זו מזו, ו-\( \Delta = (b - a) \cdot 10^k (10^d - 1) \).
    4. **אותיות :** אות היא שתי ספרות, \( 10 \) עד \( 35 \), ולכן אות שגויה משנה את המספר
       ב-\( (v' - v) \cdot 10^k \), עם \( |v' - v| \le 25 \).

    </div>

    #### למה זה נכון { .sol-proof }

    **ספרה אחת.** ‏\( 0 < |b - a| \le 9 \), ולכן 97 לא מחלק את \( b - a \). גם את
    \( 10^k = 2^k 5^k \) הוא לא מחלק. ‏97 ראשוני, וראשוני שמחלק מכפלה מחלק לפחות אחד מהגורמים
    שלה. לכן הוא לא מחלק את \( \Delta \), והטעות נתפסת. אותו טיעון עובד לאות שהוחלפה באות
    אחרת, כי \( |v' - v| \le 25 < 97 \).

    **החלפה של שכנות.** ‏\( \Delta = 9(b - a) \cdot 10^k \), ו-97 לא מחלק אף אחד משלושת
    הגורמים. נתפסת.

    **כל החלפה.** ‏\( \Delta = (b - a) \cdot 10^k \cdot (10^d - 1) \). הגורם החדש הוא
    \( 10^d - 1 \), ו-97 מחלק אותו רק כש-\( 10^d \equiv 1 \pmod{97} \). הסדר של 10 מודולו 97
    הוא 96 : החזקות של 10 עוברות על 96 שאריות שונות לפני שהן חוזרות ל-1. ב-IBAN יש לכל היותר
    34 תווים, ולכן \( d < 96 \), וכל החלפה של שתי ספרות נתפסת, גם רחוקות.

    **מה עובר.** טעות של כמה ספרות יחד יכולה לתת \( \Delta \) שהוא כפולה של 97. ב-IBAN
    לדוגמה, אם שתי הספרות האחרונות <span dir="ltr">99</span> נכתבות <span dir="ltr">02</span>,
    המספר קטן ב-\( 97 \cdot 10^6 \), והשארית לא משתנה :
    <span dir="ltr">IL62 0108 0000 0009 9999 902</span> עובר את הבדיקה. מבין כל הטעויות של
    שתי ספרות בחשבונות אקראיים עובר בערך 1%, קרוב ל-\( 1/97 \). גם אות וספרה צמודות יכולות
    לעבור : <span dir="ltr">B1</span> ו-<span dir="ltr">1B</span> נכתבים שניהם
    <span dir="ltr">111</span>, וכך גם <span dir="ltr">M2</span> ו-<span dir="ltr">X3</span>.

    **למה 97.** שתי ספרות ביקורת מחזיקות עד 100 ערכים, והשאלה היא איזה מודולו קטן מ-100 תופס
    הכי הרבה. כך נראים ארבעה מודולים על כל הטעויות בחלק החשבון של 30 IBAN ישראליים מומצאים :

    <!-- gen 9 -->

    | סוג הטעות | ‏מודולו 100 | ‏מודולו 99 | ‏מודולו 98 | ‏מודולו 97 |
    |---|:-:|:-:|:-:|:-:|
    | ספרה אחת שגויה | 0.0% | 100% | 100% | 100% |
    | שתי שכנות הוחלפו | 0.0% | 100% | 100% | 100% |
    | החלפה בדילוג, <span dir="ltr">abc</span> ל-<span dir="ltr">cba</span> | 0.0% | 0.0% | 100% | 100% |
    | שתי ספרות שגויות | 0.0% | 96.6% | 98.1% | 99.1% |

    <!-- /gen -->

    - **‏100 :** השארית היא רק שתי הספרות האחרונות, ספרות הביקורת עצמן. כל טעות בחשבון עוברת.
    - **‏99 :** ‏\( 10^2 = 100 \equiv 1 \pmod{99} \), הסדר של 10 הוא 2, ולכן החלפה בדילוג,
      ‏<span dir="ltr">abc</span> ל-<span dir="ltr">cba</span>, משנה את המספר ב-\( 99(c - a) \cdot 10^k \)
      ועוברת תמיד.
    - **‏98 :** ‏\( 98 = 2 \cdot 7^2 \) לא ראשוני, ויש יותר שינויים שמתחלקים בו. שתי ספרות
      שגויות עוברות כמעט פי שניים יותר.
    - **‏97 :** הראשוני הגדול ביותר עם שתי ספרות. ראשוני מבטיח שכל טעות "קטנה" נתפסת, והגודל
      מקטין את מה שעובר מטעויות גדולות, לבערך \( 1/97 \).

    **נסו בעצמכם.** בחרו מקום, ושנו את התו שם או החליפו אותו עם השכן שלו. התיבה מראה אם
    הטעות נתפסה או עברה. הדוגמה "שתי טעויות שעוברות" היא המספר של הפסקה הקודמת :

    <div class="explorer" data-kind="iban" data-pos="15"></div>

    #### סיבוכיות { .sol-cost }

    כל ההוכחות הן חשבון על הגורמים של \( \Delta \). הטבלה סופרת את כל הטעויות מכל סוג בחלק
    החשבון, 19 ספרות, של 30 IBAN : ספרה שגויה 171 טעויות לכל IBAN, ושתי ספרות שגויות 13,851.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : המספר כולו בבת אחת"
    ב-Python ‏`int(digits) % 97` עובד, כי יש בה מספרים שלמים בכל גודל. ב-C או
    ב-SystemVerilog המספר בן 25 ספרות לא נכנס ב-64 ביטים, שמחזיקים רק עד בערך
    \( 1.8 \cdot 10^{19} \), 20 ספרות. החישוב גולש בשקט ונותן שארית לא נכונה. צריך את
    השארית ספרה אחרי ספרה.

??? trap "מלכודת : לשכוח את ההעברה"
    השארית של המספר כפי שהוא כתוב, בלי להעביר את ארבעת התווים הראשונים, היא משהו אחר
    לגמרי. ב-IBAN לדוגמה היא לא 1, וה-IBAN נראה לא תקין.

??? trap "מלכודת : אות כספרה אחת"
    ‏\( A = 1 \), או קוד ASCII ‏(\( A = 65 \)), נותנים מספר אחר. התקן קובע \( A = 10 \) עד
    \( Z = 35 \), שתי ספרות לכל אות.

??? trap "מלכודת : בדיקה בלי אורך"
    טעות שמחליפה ספרה באות משנה את אורך המספר, ואז 97 כבר לא מבטיח כלום. ב-IBAN לדוגמה,
    שלוש החלפות כאלה של ספרה בחשבון באות עוברות את בדיקת השארית. לכן בודקים גם את המבנה של המדינה :
    בישראל 23 תווים, וכולם ספרות אחרי IL.

??? followup "שאלות המשך"
    - **‏9 ספרות בכל פעם :** התקן מציע לחשב את השארית מ-9 ספרות בכל פעם. למה דווקא 9?

        ??? fu-answer "תשובה"
            מספר בן 9 ספרות קטן מ-\( 2^{31} \), ונכנס במספר שלם של 32 ביטים. בצעדים הבאים
            כותבים את השארית, עד שתי ספרות, ואחריה 7 ספרות חדשות : שוב 9 ספרות לכל היותר.

    - **‏10 בחזקת 6 :** בודק בחומרה מקבל את ה-IBAN מהסוף להתחלה. מה משתנה?

        ??? fu-answer "תשובה"
            מהסוף, כל ספרה חדשה היא הספרה המשמעותית ביותר, ומוסיפים אותה עם ערך המקום שלה :
            \( r \leftarrow (r + d \cdot p) \bmod 97 \), ‏\( p \leftarrow 10p \bmod 97 \).
            צריך רגיסטר נוסף לערך המקום, כמו בגלאי ההתחלקות של 0055 כשהביט החדש נכנס כ-MSB.

    - **‏Luhn מול 97 :** מה תופס יותר, ספרת Luhn של כרטיס אשראי או שתי ספרות מודולו 97?

        ??? fu-answer "תשובה"
            ‏97. ‏Luhn, ספרה אחת מודולו 10, מפספס את ההחלפה של 09 ו-90 ולא תופס החלפות
            בדילוג. ‏97 תופס כל טעות בספרה אחת וכל החלפה של שתי ספרות, במחיר של ספרת ביקורת
            נוספת.
