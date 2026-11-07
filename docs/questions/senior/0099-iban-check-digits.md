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

תכננו בודק IBAN בחומרה : רגיסטרים של פליפ-פלופים מסוג D, ולוגיקה צירופית. מותר להניח
בלוקים של כפל, חיבור וחיסור על מספרים של עד 10 ביטים, כלומר עד 1023, ובלוק שמחשב את השארית
בחלוקה ל-97 של מספר כזה. ה-IBAN מגיע כפי שהוא כתוב, ספרה אחת בכל שעון ב-4 ביטים. כל אות כבר
פוצלה לשתי הספרות שלה, ולכן 6 הספרות הראשונות הן הראש : שתי האותיות ושתי ספרות הביקורת. עם
הספרה האחרונה מגיע האות `last`. תארו את כל הארכיטקטורה : אילו רגיסטרים, אילו בלוקים, מה
בוחר ביניהם בכל שעון, ומתי יוצאת התשובה.

??? tip "רמז 1"
    מספר בן 25 ספרות לא נכנס לשום רגיסטר. מה מספיק לזכור ממנו אחרי כל ספרה?

??? tip "רמז 2"
    הראש מגיע ראשון אבל בבדיקה הוא בסוף המספר. מה קורה למספר כשכותבים אחריו עוד 6 ספרות?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        **שלושה רגיסטרים, 17 פליפ-פלופים, ושני בלוקים של חשבון.** בכל שעון בלוק אחד מחשב
        \( 10x + d \) ובלוק אחד את השארית בחלוקה ל-97, כש-\( x \) הוא אחד משני רגיסטרים של 7
        ביטים : \( h \), השארית של 6 ספרות הראש, ו-\( r \), השארית של כל השאר. אחרי הספרה
        האחרונה הבודק מכניס עוד 6 פעמים את הספרה 0, וכך \( r \) הופך לשארית של
        \( R \cdot 10^6 \) : השאר, מוזז 6 ספרות שמאלה, בדיוק כמו אחרי ההעברה. מונה של 3 ביטים
        סופר את 6 השעונים האלה. בסוף ה-IBAN תקין אם ורק אם \( r + h \) הוא 1 או 98.

    <!-- cost: פליפ-פלופים 17 | שעונים 31 | בלוקים בשעון 2 -->

    #### הרעיון { .sol-idea }

    **רעיון 1 : לזכור רק את השארית.** כשמגיעה ספרה \( d \), המספר שנקרא עד עכשיו, \( a \),
    הופך ל-\( 10a + d \), והשארית החדשה תלויה רק בשארית הקודמת :
    \( r \to (10r + d) \bmod 97 \). השארית היא בין 0 ל-96, ולכן מספיקים 7 ביטים. זו **מכונת
    מצבים** : מצב לכל אחת מ-97 השאריות, ובכל שעון מעבר לפי הספרה.

    **רעיון 2 : החשבון נכנס ב-10 ביטים.** ‏\( 10r + d \le 10 \cdot 96 + 9 = 969 \), ולכן בלוק
    אחד של כפל וחיבור ובלוק אחד של mod 97 מחשבים את המעבר בשעון אחד.

    **רעיון 3 : הראש בלי לשמור אותו.** אחרי ההעברה המספר הוא השאר ואחריו 6 ספרות הראש :
    \( N = R \cdot 10^6 + H \). כתיבה של 6 ספרות אחרי \( R \) מזיזה אותו 6 מקומות שמאלה,
    כלומר מכפילה ב-\( 10^6 \), ו-\( H \) נוסף. לכן :

    - את 6 ספרות הראש מחשבים לרגיסטר משלהן, \( h = H \bmod 97 \), באותם בלוקים.
    - את השאר מחשבים ל-\( r = R \bmod 97 \).
    - את ההזזה ב-\( 10^6 \) עושים כמו שהיא נשמעת : עוד 6 שעונים שבהם נכנסת הספרה 0. כל אחד
      מהם מכפיל את \( r \) ב-10, ובסוף \( r = R \cdot 10^6 \bmod 97 \).
    - ‏\( N \bmod 97 = (r + h) \bmod 97 \). ‏\( r + h \le 192 \), ולכן השארית היא 1 אם ורק אם
      \( r + h \) הוא 1 או 98. מספיקים מחבר והשוואה.

    **הארכיטקטורה.** כל זה יחד, בתרשים אחד :

    <!-- gen 2 -->

    <svg class="figure ih-fig ih-dp" viewBox="0 0 400 520" direction="ltr" style="max-width:25rem" role="img" aria-label="תרשים המלבנים של הבודק : שלושה רגיסטרים, h ו-r של 7 ביטים ומונה n של 3 ביטים. הבקרה מחשבת head כש-r לפחות 97 ו-tail כש-n גדול מ-0. מרבב בוחר את h בזמן הראש ואת r אחריו, מרבב שני מכניס 0 במקום הספרה בזמן הזנב, בלוק אחד מחשב 10x ועוד הספרה ובלוק אחד mod 97. התוצאה נכתבת ל-h בזמן הראש ול-r אחריו. בסוף בודקים אם y ועוד h שווה 1 או 98"><defs><marker id="ih-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="ih-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs><g class="ih-blk ih-reg"><rect x="20" y="14" width="104" height="44" rx="5"/><text x="72" y="34" text-anchor="middle">h</text><text class="ih-sub" x="72" y="49" text-anchor="middle">7 flip-flops</text></g><g class="ih-blk ih-reg"><rect x="148" y="14" width="104" height="44" rx="5"/><text x="200" y="34" text-anchor="middle">r</text><text class="ih-sub" x="200" y="49" text-anchor="middle">7 flip-flops</text></g><g class="ih-blk ih-reg"><rect x="276" y="14" width="104" height="44" rx="5"/><text x="328" y="34" text-anchor="middle">n</text><text class="ih-sub" x="328" y="49" text-anchor="middle">3 flip-flops</text></g><g class="ih-blk ih-ctl"><rect x="148" y="84" width="104" height="30" rx="5"/><text x="200" y="104" text-anchor="middle">r ≥ 97 ?</text></g><g class="ih-blk ih-ctl"><rect x="276" y="84" width="104" height="30" rx="5"/><text x="328" y="104" text-anchor="middle">n > 0 ?</text></g><path class="ih-wire" d="M200,58 L200,84" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M328,58 L328,84" marker-end="url(#ih-hb)"/><text class="ih-wlab" x="144" y="128" text-anchor="end">head</text><text class="ih-wlab" x="326" y="128" text-anchor="end">tail</text><g class="ih-blk ih-mux"><rect x="40" y="150" width="150" height="36" rx="5"/><text x="115" y="173" text-anchor="middle">x = head ? h : r</text></g><g class="ih-blk ih-mux"><rect x="220" y="150" width="150" height="36" rx="5"/><text x="295" y="173" text-anchor="middle">e = tail ? 0 : d</text></g><path class="ih-wire" d="M72,58 L72,150" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M170,58 L170,70 L134,70 L134,150" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M148,114 L148,132 L115,132 L115,150" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M330,114 L330,132 L295,132 L295,150" marker-end="url(#ih-hb)"/><text class="ih-wlab" x="352" y="134" text-anchor="start">d[3:0]</text><path class="ih-wire" d="M350,138 L350,150" marker-end="url(#ih-hb)"/><g class="ih-blk ih-add"><rect x="90" y="214" width="220" height="44" rx="5"/><text x="200" y="234" text-anchor="middle">s = 10x + e</text><text class="ih-sub" x="200" y="249" text-anchor="middle">≤ 969, 10 bits</text></g><path class="ih-wire" d="M115,186 L115,214" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M295,186 L295,214" marker-end="url(#ih-hb)"/><g class="ih-blk ih-stage"><rect x="90" y="284" width="220" height="44" rx="5"/><text x="200" y="304" text-anchor="middle">y = s mod 97</text><text class="ih-sub" x="200" y="319" text-anchor="middle">0 .. 96</text></g><path class="ih-wire" d="M200,258 L200,284" marker-end="url(#ih-hb)"/><g class="ih-blk ih-mux"><rect x="40" y="356" width="320" height="44" rx="5"/><text x="200" y="376" text-anchor="middle">head: h ← y, r ← r + 1 (0 after 102)</text><text class="ih-sub" x="200" y="391" text-anchor="middle">rest and tail: r ← y; tail: n ← n + 1</text></g><path class="ih-wire" d="M200,328 L200,356" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M40,378 L8,378 L8,36 L20,36" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M360,378 L392,378 L392,6 L200,6 L200,14" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M328,6 L328,14" marker-end="url(#ih-hb)"/><g class="ih-blk ih-add"><rect x="40" y="432" width="140" height="44" rx="5"/><text x="110" y="452" text-anchor="middle">y + h</text><text class="ih-sub" x="110" y="467" text-anchor="middle">≤ 192</text></g><g class="ih-blk ih-out"><rect x="220" y="432" width="140" height="44" rx="5"/><text x="290" y="452" text-anchor="middle">= 1 or 98 ?</text><text class="ih-sub" x="290" y="467" text-anchor="middle">ok, n = 6</text></g><path class="ih-wire" d="M110,400 L110,432" marker-end="url(#ih-hb)"/><path class="ih-wire" d="M180,454 L220,454" marker-end="url(#ih-hb)"/><text class="ih-sub" x="200" y="506" text-anchor="middle">one clock: a mux, 10x + e, mod 97</text></svg>

    <!-- /gen -->

    - **הרגיסטרים :** ‏\( h \) ו-\( r \), 7 פליפ-פלופים כל אחד, ומונה \( n \) של 3 פליפ-פלופים.
      אחרי איפוס \( h = 0 \), ‏\( r = 97 \) ו-\( n = 0 \).
    - **הבקרה :** שני אותות שמחושבים מהרגיסטרים עצמם. ‏`head` הוא \( r \ge 97 \) : שארית אף פעם
      לא מגיעה ל-97, ולכן בזמן הראש \( r \) שומר בערכים 97 עד 102 את מספר ספרות הראש שעברו,
      בלי מונה נוסף. ‏`tail` הוא \( n > 0 \), השעונים של ה-0 בסוף.
    - **המרבב הראשון :** \( x = \) `head` ? \( h \) : \( r \). רק נתיב חשבון אחד, ושתי השאריות
      משתמשות בו לפי התור.
    - **המרבב השני :** \( e = \) `tail` ? 0 : \( d \). בזנב נכנסת הספרה 0 במקום הקלט.
    - **החשבון :** \( s = 10x + e \), לכל היותר 969, ואחריו \( y = s \bmod 97 \).
    - **הכתיבה :** בראש \( h \leftarrow y \) ו-\( r \leftarrow r + 1 \), ואחרי 102,
      \( r \leftarrow 0 \). אחר כך \( r \leftarrow y \). בזנב גם \( n \leftarrow n + 1 \), ו-`last`
      מתחיל אותו, \( n \leftarrow 1 \).
    - **המונה :** \( n \) לא סופר כל הזמן. כש-\( n = 0 \) הוא כבוי ולא זז, וזה המצב שלו
      בכל הראש והשאר. ‏`last` טוען לתוכו 1. כל עוד \( n \ne 0 \) הוא עולה ב-1 בכל שעון, וכש-\( n = 6 \)
      השעון הבא טוען 0 ולא 7 : \( n \leftarrow (n = 6)\ ?\ 0 : n + 1 \). לכן הוא לא מסתובב, אלא
      עובר פעם אחת 1, 2, ... 6, חוזר ל-0 ונשאר שם עד ה-`last` הבא.
    - **התשובה :** בשעון שבו \( n = 6 \), ‏`done` עולה, ו-`ok` אומר אם \( y + h \) הוא 1 או 98.

    כך עובר דרכו ה-IBAN של העמוד, שעון אחרי שעון :

    <!-- gen 3 -->

    | שעון | נכנס | מה נכנס לבלוקים | ‏10x + e | ‏mod 97 | אחרי השעון |
    |:-:|:-:|---|:-:|:-:|---|
    | 1 | 1 | ספרת ראש, ‏<span dir="ltr">x = h = 0</span> | 1 | 1 | ‏<span dir="ltr">h = 1, r = 98</span> |
    | 2 | 8 | ספרת ראש, ‏<span dir="ltr">x = h = 1</span> | 18 | 18 | ‏<span dir="ltr">h = 18, r = 99</span> |
    | 3 | 2 | ספרת ראש, ‏<span dir="ltr">x = h = 18</span> | 182 | 85 | ‏<span dir="ltr">h = 85, r = 100</span> |
    | 4 | 1 | ספרת ראש, ‏<span dir="ltr">x = h = 85</span> | 851 | 75 | ‏<span dir="ltr">h = 75, r = 101</span> |
    | 5 | 6 | ספרת ראש, ‏<span dir="ltr">x = h = 75</span> | 756 | 77 | ‏<span dir="ltr">h = 77, r = 102</span> |
    | 6 | 2 | ספרת ראש, ‏<span dir="ltr">x = h = 77</span> | 772 | 93 | ‏<span dir="ltr">h = 93, r = 0</span> |
    | 7 | 0 | ספרה, ‏<span dir="ltr">x = r = 0</span> | 0 | 0 | ‏<span dir="ltr">h = 93, r = 0</span> |
    | 8 | 1 | ספרה, ‏<span dir="ltr">x = r = 0</span> | 1 | 1 | ‏<span dir="ltr">h = 93, r = 1</span> |
    | 9 | 0 | ספרה, ‏<span dir="ltr">x = r = 1</span> | 10 | 10 | ‏<span dir="ltr">h = 93, r = 10</span> |
    | 10 | 8 | ספרה, ‏<span dir="ltr">x = r = 10</span> | 108 | 11 | ‏<span dir="ltr">h = 93, r = 11</span> |
    | … | | | | | |
    | 25 | 9 | ספרה, ‏<span dir="ltr">x = r = 76</span> | 769 | 90 | ‏<span dir="ltr">h = 93, r = 90, n = 1</span> |
    | 26 | 0 | ‏0 של הזנב, ‏<span dir="ltr">n = 1, x = r = 90</span> | 900 | 27 | ‏<span dir="ltr">h = 93, r = 27, n = 2</span> |
    | 27 | 0 | ‏0 של הזנב, ‏<span dir="ltr">n = 2, x = r = 27</span> | 270 | 76 | ‏<span dir="ltr">h = 93, r = 76, n = 3</span> |
    | 28 | 0 | ‏0 של הזנב, ‏<span dir="ltr">n = 3, x = r = 76</span> | 760 | 81 | ‏<span dir="ltr">h = 93, r = 81, n = 4</span> |
    | 29 | 0 | ‏0 של הזנב, ‏<span dir="ltr">n = 4, x = r = 81</span> | 810 | 34 | ‏<span dir="ltr">h = 93, r = 34, n = 5</span> |
    | 30 | 0 | ‏0 של הזנב, ‏<span dir="ltr">n = 5, x = r = 34</span> | 340 | 49 | ‏<span dir="ltr">h = 93, r = 49, n = 6</span> |
    | 31 | 0 | ‏0 של הזנב, ‏<span dir="ltr">n = 6, x = r = 49</span> | 490 | 5 | ‏<span dir="ltr">h = 93, r = 5, n = 0</span> |
    | סוף | | ‏<span dir="ltr">y + h</span> | | | ‏<span dir="ltr">5 + 93 = 98</span>, תקין |

    <!-- /gen -->

    ובהשוואה לדרך הישירה, ששומרת את 6 ספרות הראש ומכניסה אותן שוב בסוף :

    <!-- gen 4 -->

    | הבודק | פליפ-פלופים | שעונים ל-IBAN הישראלי |
    |---|:-:|:-:|
    | שומרים את 6 ספרות הראש ומכניסים אותן שוב בסוף | ‏<span dir="ltr">24 + 7 + 3 = 34</span> | 31 |
    | שארית לראש, שש ספרות 0 בסוף (הפתרון) | ‏<span dir="ltr">7 + 7 + 3 = 17</span> | 31 |
    | עם מכפל של 12 ביטים, ‏<span dir="ltr">(27r + h) mod 97</span> | ‏<span dir="ltr">7 + 7 = 14</span> | 25 |

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הראש, 6 שעונים :** ‏`head` דולק, \( h \leftarrow (10h + d) \bmod 97 \), ו-\( r \) סופר
       97, 98, ... 102, ואז 0.
    2. **השאר, שעון לכל ספרה :** \( r \leftarrow (10r + d) \bmod 97 \). ‏\( h \) לא משתנה.
    3. **הזנב, 6 שעונים :** `last` מדליק את המונה. \( r \leftarrow 10r \bmod 97 \), והמונה עולה
       עד 6.
    4. **התשובה :** בשעון השישי של הזנב, תקין אם ורק אם \( y + h \in \{1, 98\} \).

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="check_stream" linenums="1" hl_lines="12 13 15 18 19 20"
        def stream(iban):
            """The digits as they arrive: the IBAN as written, every letter as two digits."""
            s = iban.replace(" ", "").upper()
            return [int(c) for c in "".join(str(int(ch, 36)) for ch in s)]


        def check_stream(digits):
            """The checker, a clock a line: h and r (7 bits), and 6 clocks of the digit 0 at the
            end. r = 97 + k means "digit k of the head", which no remainder can be."""
            h, r = 0, 97                                         # (1)!
            for d in digits:
                if r >= 97:                                      # head
                    h, r = (10 * h + d) % 97, (0 if r == 102 else r + 1)
                else:
                    r = (10 * r + d) % 97                        # (2)!
            if r >= 97:
                return False                                     # shorter than the head
            for n in range(1, 7):                                # (3)!
                r = (10 * r + 0) % 97
            return r + h in (1, 98)                              # (4)!
        ```

        1. המצב אחרי איפוס : ‏\( h = 0 \), ו-\( r = 97 \), ספרה 0 של הראש.
        2. אותם שני בלוקים, \( 10x + e \) ו-mod 97, רק עם \( x = r \).
        3. הזנב : 6 פעמים הספרה 0, כלומר \( r \) כפול \( 10^6 \). בחומרה המונה \( n \) סופר אותם.
        4. ‏\( r + h \le 192 \), ולכן \( (r + h) \bmod 97 = 1 \) רק כשהסכום 1 או 98.

    === "SystemVerilog"
        ```systemverilog title="module iban_checker" linenums="1" hl_lines="15 16 17 18 19 20 21 23 24 28 30 31"
        // One digit a clock: the IBAN as written, every letter already split into its two
        // digits, so the first 6 digits are the head. 17 flip-flops: h, r and the counter n.
        module iban_checker (
          input  logic       clk, rst_n,
          input  logic       start,          // a new IBAN: this clock's digit is its first
          input  logic       valid,          // d holds a digit this clock
          input  logic       last,           // d is the IBAN's last digit
          input  logic [3:0] d,
          output logic       done,           // one clock, at the end of the tail
          output logic       ok);            // with done: the IBAN is valid

          logic [6:0] h, r;                  // r = 97 + k: digit k of the head
          logic [2:0] n;                     // the tail: 1 .. 6

          wire [6:0] rr = start ? 7'd97 : r, hh = start ? 7'd0 : h;
          wire       head = rr >= 7'd97;
          wire       tail = n != 0;
          wire [6:0] x = head ? hh : rr;                     // the first multiplexer
          wire [3:0] e = tail ? 4'd0 : d;                    // the second
          wire [9:0] s = 10'd10 * x + e;                     // at most 969
          wire [6:0] y = 7'(s % 10'd97);                     // the mod 97 block
          wire [7:0] sum = y + hh;                           // at most 192
          assign done = tail && n == 3'd6;
          assign ok = done && (sum == 8'd1 || sum == 8'd98);

          always_ff @(posedge clk or negedge rst_n)
            if (!rst_n) begin h <= '0; r <= 7'd97; n <= '0; end
            else if (tail) begin r <= y; n <= n == 3'd6 ? '0 : n + 3'd1; end
            else if (valid) begin
              if (head) begin h <= y; r <= rr == 7'd102 ? 7'd0 : rr + 7'd1; end
              else begin h <= hh; r <= y; n <= last ? 3'd1 : '0; end
            end
        endmodule
        ```

    #### למה זה נכון { .sol-proof }

    **השארית ספרה אחרי ספרה.** זה סעיף א : \( (10a + d) \bmod 97 \) תלוי רק ב-\( a \bmod 97 \).
    באינדוקציה, אחרי הראש \( h = H \bmod 97 \), ואחרי השאר \( r = R \bmod 97 \).

    **הזנב.** כל שעון של הזנב מחשב \( (10r + 0) \bmod 97 \), השארית של המספר עם 0 נוסף בסופו.
    אחרי 6 שעונים \( r = R \cdot 10^6 \bmod 97 \).

    **הסכום.** ‏\( N = R \cdot 10^6 + H \), ולכן \( N \equiv r + h \pmod{97} \). ‏\( r \) ו-\( h \)
    בין 0 ל-96, ולכן \( r + h \) בין 0 ל-192. בטווח הזה רק 1 ו-98 נותנים שארית 1.

    **הקודים 97 עד 102.** שארית תמיד קטנה מ-97, ולכן \( r \ge 97 \) לא יכול להיות שארית, והבודק
    יודע בכל שעון אם הוא בראש בלי פליפ-פלופ נוסף. בזנב \( r \) כבר שארית, ולכן שם צריך את
    המונה.

    **נסו בעצמכם.** התקדמו שעון אחרי שעון. התיבה מראה את תרשים המלבנים עם הערך בכל חוט ובכל
    בלוק בשעון הזה, והנתיב של השעון מודגש. מתחתיו הפליפ-פלופים ביט אחרי ביט, וטבלה של כל
    האותות, עמודה לכל שעון, כמו בצורת גל :

    <div class="explorer" data-kind="ibanhw"></div>

    #### סיבוכיות { .sol-cost }

    שעון לכל ספרה ועוד 6 שעונים של הזנב : 31 שעונים ל-IBAN ישראלי. בכל שעון מרבב, בלוק
    \( 10x + e \) ובלוק mod 97, כולם על מספרים של עד 10 ביטים. ‏17 פליפ-פלופים, לעומת 34 בדרך
    הישירה.

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

    <!-- gen 5 -->

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

    <!-- gen 6 -->

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
    - **מהר יותר :** איך בודקים את אותו IBAN בפחות שעונים?

        ??? fu-answer "תשובה"
            ‏\( 100 = 97 + 3 \), ולכן שתי ספרות בשעון הן \( r \to (3r + 10a + b) \bmod 97 \), לכל
            היותר 387 : חצי מהשעונים, 13 במקום 25 לחלק של הספרות, ושוב בלוקים של 10 ביטים. אות
            שלמה בשעון אחד היא אותו רעיון, \( (3r + v) \bmod 97 \), והזנב מתקצר ל-3 שעונים של
            "00".

    - **כמה פליפ-פלופים לכל הפחות :** אפשר בפחות מ-17?

        ??? fu-answer "תשובה"
            עם מכפל של 12 ביטים אין צורך בזנב : \( 10^6 \equiv 27 \pmod97 \), ובספרה האחרונה
            בודקים \( (27r + h) \bmod 97 = 1 \). אז אין מונה, ו-14 פליפ-פלופים מספיקים. זה גם
            המינימום : בזמן השאר הבודק חייב להבדיל בין כל \( 97 \cdot 97 = 9409 \) הזוגות
            \( (h, r) \), כי לכל שני זוגות יש המשך שאחד מהם תקין בו והשני לא, ו-9409 יותר
            מ-\( 2^{13} = 8192 \).

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
