---
id: 15
title: שני ילדים, ולפחות אחד מהם בן
level: student
difficulty: easy
tags: [probability, math, logic-puzzles]
source: ""
added: 2026-10-18
---

## השאלה

ליוסי יש שני ילדים. שאלנו אותו: "האם לפחות אחד מהילדים שלך הוא בן?", והוא ענה "כן".

ההנחות בכל השאלה:

- **מין:** כל ילד הוא בן או בת בהסתברות \( 1/2 \), בלי תלות בילד השני.
- **יום לידה:** כל ילד נולד באחד משבעת ימי השבוע בהסתברות שווה, בלי תלות במין שלו
  ובילד השני.

??? interviewer "מה המראיין בודק"
    - **הסתברות מותנית ולא תחושת בטן:** לזהות שהמידע "לפחות אחד" לא מצביע על ילד מסוים,
      ולכן התשובה איננה חצי.
    - **מרחב מדגם נכון:** לכתוב את כל התוצאות שוות ההסתברות, בלי לאחד בטעות את "בן ובת"
      ואת "בת ובן" לתוצאה אחת.
    - **ספירה בלי כפילות:** לראות שבסעיף ב יש משפחה אחת שנספרת פעמיים אם לא נזהרים.
    - **הכללה ובדיקה:** לנסח נוסחה כללית ולבדוק אותה מול המקרים הפרטיים ומקרי קצה.

---

### סעיף א – לפחות אחד בן

מה ההסתברות ששני הילדים של יוסי בנים?

??? tip "רמז 1"
    כמה משפחות שונות עם שני ילדים יש, כשמבחינים בין הילד הראשון לילד השני? האם כולן שוות
    בהסתברותן?

??? tip "רמז 2"
    מחקו את המשפחות שלא מתאימות לתשובה של יוסי. כמה משפחות נשארו, ובכמה מהן שני בנים?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ההסתברות היא \( 1/3 \), ולא \( 1/2 \).

    #### הרעיון { .sol-idea }

    התשובה "כן" פוסלת רק משפחה אחת: שתי בנות. נשארות שלוש משפחות שוות בהסתברותן, ורק
    באחת מהן שני בנים. המידע "לפחות אחד בן" לא אומר **איזה** ילד הוא הבן, ולכן אי אפשר
    "לסמן" את הבן ולשאול רק על הילד השני.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מרחב המדגם:** מסדרים את הילדים לפי סדר הלידה. יש ארבע משפחות, כל אחת בהסתברות
       \( 1/4 \): בן ובן, בן ובת, בת ובן, בת ובת.
    2. **התנאי:** "לפחות אחד בן" פוסל רק את בת ובת. נשארות שלוש משפחות, בהסתברות כוללת
       \( 3/4 \).
    3. **המטרה:** רק אחת מהן היא בן ובן, בהסתברות \( 1/4 \).
    4. **היחס:** מחלקים את ההסתברות של המטרה בהסתברות של התנאי, ומקבלים \( 1/3 \).

    </div>

    #### למה זה נכון { .sol-proof }

    בשרטוט, השורות הן הילד הראשון והעמודות הן הילד השני. כל משבצת היא משפחה בהסתברות
    \( 1/4 \):

    <svg class="figure" viewBox="0 0 300 150" style="max-width:19rem" role="img" aria-label="ארבע המשפחות האפשריות: בן בן, בן בת, בת בן, בת בת. בת בת נפסלת, ומבין שלוש הנותרות רק אחת היא בן בן"><text class="pg-head" x="185" y="18" text-anchor="middle" direction="rtl">בן</text><text class="pg-head" x="75" y="18" text-anchor="middle" direction="rtl">בת</text><text class="pg-head" x="270" y="61" text-anchor="middle" direction="rtl">בן</text><text class="pg-head" x="270" y="117" text-anchor="middle" direction="rtl">בת</text><rect class="pg-hit" x="132" y="30" width="106" height="52" rx="6"/><text class="pg-label" x="185" y="54" text-anchor="middle" direction="rtl">בן, בן</text><text class="pg-small" x="185" y="71" text-anchor="middle">1/4</text><rect class="pg-cond" x="22" y="30" width="106" height="52" rx="6"/><text class="pg-label" x="75" y="54" text-anchor="middle" direction="rtl">בן, בת</text><text class="pg-small" x="75" y="71" text-anchor="middle">1/4</text><rect class="pg-cond" x="132" y="86" width="106" height="52" rx="6"/><text class="pg-label" x="185" y="110" text-anchor="middle" direction="rtl">בת, בן</text><text class="pg-small" x="185" y="127" text-anchor="middle">1/4</text><rect class="pg-out" x="22" y="86" width="106" height="52" rx="6"/><line class="pg-strike" x1="32" y1="130" x2="118" y2="94"/><text class="pg-label" x="75" y="110" text-anchor="middle" direction="rtl">בת, בת</text><text class="pg-small" x="75" y="127" text-anchor="middle">1/4</text></svg>  

    <span class="viz-legend"><span><i class="pg-hit"></i>מקיים את התנאי, ושני הילדים בנים</span><span><i class="pg-cond"></i>מקיים את התנאי, יש גם בת</span><span><i class="pg-out"></i>לא מקיים את התנאי</span></span> 

    נסמן ב-\( A \) את המאורע "שני הילדים בנים" וב-\( B \) את המאורע "לפחות אחד בן". כל
    משפחה עם שני בנים מקיימת גם את \( B \), ולכן \( A \cap B = A \):

    \[
    P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{1/4}{3/4} = \frac{1}{3}
    \]

    **מתי התשובה כן חצי?** אם המידע היה על ילד **מסוים**, למשל "הילד הבכור הוא בן", היו
    נשארות רק המשפחות בן ובן ובן ובת, והתשובה הייתה \( 1/2 \). ב"לפחות אחד בן" הבן יכול
    להיות כל אחד מהשניים, ולכן יש **שתי** משפחות עם בן ובת מול **אחת** עם שני בנים.

---

### סעיף ב – בן שנולד ביום שלישי

הפעם שאלנו את יוסי: "האם יש לך בן שנולד ביום שלישי?", והוא ענה "כן". מה ההסתברות ששני
הילדים בנים?

??? tip "רמז 1"
    כל ילד הוא עכשיו אחד מ-14 סוגים שווי הסתברות: בן או בת, כפול שבעה ימים. כמה זוגות
    מסודרים של ילדים יש?

??? tip "רמז 2"
    ספרו את הזוגות שבהם הילד הראשון הוא בן מיום שלישי, ואת הזוגות שבהם הילד השני הוא כזה.
    יש זוג אחד שנמצא בשתי הקבוצות.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ההסתברות היא \( 13/27 \approx 0.481 \): כמעט חצי, ורחוק מהשליש של סעיף א.

    #### הרעיון { .sol-idea }

    כל ילד הוא אחד מ-14 סוגים שווי הסתברות, ולכן יש \( 14 \times 14 = 196 \) זוגות שווי
    הסתברות. התנאי מתקיים בשורה ובעמודה של "בן מיום שלישי", כלומר בצורת צלב, וסופרים בו
    בהכלה והדחה. ככל שהמידע ספציפי יותר, הוא כמעט מצביע על ילד מסוים, והתשובה מתקרבת
    לחצי של "הבכור הוא בן".

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מרחב המדגם:** לכל ילד 14 סוגים, ולשניהם \( 196 \) זוגות מסודרים, כל זוג
       בהסתברות \( 1/196 \).
    2. **המאורעות:** \( T \) הוא "לפחות אחד מהילדים הוא בן שנולד ביום שלישי", ו-\( A \)
       הוא "שני הילדים בנים".
    3. **סופרים את \( T \):** הילד הראשון בן מיום שלישי בדיוק ב-14 זוגות, כי הילד השני
       הוא כל אחד מ-14 הסוגים. גם הילד השני כזה ב-14 זוגות. הזוג שבו **שניהם** בנים מיום
       שלישי נספר פעמיים, ולכן מורידים אותו: \( |T| = 14 + 14 - 1 = 27 \).
    4. **סופרים את \( A \cap T \):** הילד הראשון בן מיום שלישי והשני בן מכל יום: 7 זוגות.
       השני בן מיום שלישי והראשון בן מכל יום: עוד 7. שוב מורידים את הזוג שנספר פעמיים:
       \( |A \cap T| = 7 + 7 - 1 = 13 \).
    5. **היחס:** כל הזוגות שווי הסתברות, ולכן ההסתברות המותנית היא יחס הספירות:
       \( P(A \mid T) = 13/27 \).

    </div>

    #### למה זה נכון { .sol-proof }

    בשרטוט, השורות הן הילד הראשון והעמודות הן הילד השני. כל צד מחולק לבן ולבת, ובכל אחד
    שבעה ימים, מ-א (ראשון) עד ש (שבת). יום שלישי הוא האות ג. כל משבצת היא זוג בהסתברות
    \( 1/196 \):

    <svg class="figure" viewBox="0 0 432 416" style="max-width:27rem" role="img" aria-label="טבלה של 196 צירופים של מין ויום לידה לשני הילדים. 27 משבצות מקיימות את התנאי, ו-13 מהן הן בן ובן"><text class="pg-head" x="279" y="16" text-anchor="middle" direction="rtl">בן</text><text class="pg-head" x="414" y="140" text-anchor="middle" direction="rtl">בן</text><text class="pg-head" x="97" y="16" text-anchor="middle" direction="rtl">בת</text><text class="pg-head" x="414" y="322" text-anchor="middle" direction="rtl">בת</text><text class="pg-day" x="357" y="36" text-anchor="middle">א</text><text class="pg-day" x="384" y="61" text-anchor="middle">א</text><text class="pg-day" x="331" y="36" text-anchor="middle">ב</text><text class="pg-day" x="384" y="87" text-anchor="middle">ב</text><text class="pg-day pg-day-hl" x="305" y="36" text-anchor="middle">ג</text><text class="pg-day pg-day-hl" x="384" y="113" text-anchor="middle">ג</text><text class="pg-day" x="279" y="36" text-anchor="middle">ד</text><text class="pg-day" x="384" y="139" text-anchor="middle">ד</text><text class="pg-day" x="253" y="36" text-anchor="middle">ה</text><text class="pg-day" x="384" y="165" text-anchor="middle">ה</text><text class="pg-day" x="227" y="36" text-anchor="middle">ו</text><text class="pg-day" x="384" y="191" text-anchor="middle">ו</text><text class="pg-day" x="201" y="36" text-anchor="middle">ש</text><text class="pg-day" x="384" y="217" text-anchor="middle">ש</text><text class="pg-day" x="175" y="36" text-anchor="middle">א</text><text class="pg-day" x="384" y="243" text-anchor="middle">א</text><text class="pg-day" x="149" y="36" text-anchor="middle">ב</text><text class="pg-day" x="384" y="269" text-anchor="middle">ב</text><text class="pg-day" x="123" y="36" text-anchor="middle">ג</text><text class="pg-day" x="384" y="295" text-anchor="middle">ג</text><text class="pg-day" x="97" y="36" text-anchor="middle">ד</text><text class="pg-day" x="384" y="321" text-anchor="middle">ד</text><text class="pg-day" x="71" y="36" text-anchor="middle">ה</text><text class="pg-day" x="384" y="347" text-anchor="middle">ה</text><text class="pg-day" x="45" y="36" text-anchor="middle">ו</text><text class="pg-day" x="384" y="373" text-anchor="middle">ו</text><text class="pg-day" x="19" y="36" text-anchor="middle">ש</text><text class="pg-day" x="384" y="399" text-anchor="middle">ש</text><rect class="pg-out" x="345" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="45" width="24" height="24" rx="3"/><rect class="pg-hit" x="293" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="45" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="71" width="24" height="24" rx="3"/><rect class="pg-hit" x="293" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="71" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="71" width="24" height="24" rx="3"/><rect class="pg-hit" x="345" y="97" width="24" height="24" rx="3"/><rect class="pg-hit" x="319" y="97" width="24" height="24" rx="3"/><rect class="pg-hit" x="293" y="97" width="24" height="24" rx="3"/><circle class="pg-twice" cx="305.0" cy="109.0" r="7.0"/><rect class="pg-hit" x="267" y="97" width="24" height="24" rx="3"/><rect class="pg-hit" x="241" y="97" width="24" height="24" rx="3"/><rect class="pg-hit" x="215" y="97" width="24" height="24" rx="3"/><rect class="pg-hit" x="189" y="97" width="24" height="24" rx="3"/><rect class="pg-cond" x="163" y="97" width="24" height="24" rx="3"/><rect class="pg-cond" x="137" y="97" width="24" height="24" rx="3"/><rect class="pg-cond" x="111" y="97" width="24" height="24" rx="3"/><rect class="pg-cond" x="85" y="97" width="24" height="24" rx="3"/><rect class="pg-cond" x="59" y="97" width="24" height="24" rx="3"/><rect class="pg-cond" x="33" y="97" width="24" height="24" rx="3"/><rect class="pg-cond" x="7" y="97" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="123" width="24" height="24" rx="3"/><rect class="pg-hit" x="293" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="123" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="149" width="24" height="24" rx="3"/><rect class="pg-hit" x="293" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="149" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="175" width="24" height="24" rx="3"/><rect class="pg-hit" x="293" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="175" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="201" width="24" height="24" rx="3"/><rect class="pg-hit" x="293" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="201" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="227" width="24" height="24" rx="3"/><rect class="pg-cond" x="293" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="227" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="253" width="24" height="24" rx="3"/><rect class="pg-cond" x="293" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="253" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="279" width="24" height="24" rx="3"/><rect class="pg-cond" x="293" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="279" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="305" width="24" height="24" rx="3"/><rect class="pg-cond" x="293" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="305" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="331" width="24" height="24" rx="3"/><rect class="pg-cond" x="293" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="331" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="357" width="24" height="24" rx="3"/><rect class="pg-cond" x="293" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="357" width="24" height="24" rx="3"/><rect class="pg-out" x="345" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="319" y="383" width="24" height="24" rx="3"/><rect class="pg-cond" x="293" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="267" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="241" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="215" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="189" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="163" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="137" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="111" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="85" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="59" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="33" y="383" width="24" height="24" rx="3"/><rect class="pg-out" x="7" y="383" width="24" height="24" rx="3"/><rect class="pg-quad" x="188" y="44" width="182" height="182"/><line class="pg-split" x1="188" y1="44" x2="188" y2="408"/><line class="pg-split" x1="6" y1="226" x2="370" y2="226"/></svg> 

    <span class="viz-legend"><span><i class="pg-hit"></i>מקיים את התנאי, ושני הילדים בנים</span><span><i class="pg-cond"></i>מקיים את התנאי, יש גם בת</span><span><i class="pg-out"></i>לא מקיים את התנאי</span><span><i class="pg-quad"></i>כל המשפחות עם שני בנים (49)</span><span><i class="pg-twice"></i>שני בנים שנולדו ביום שלישי, נספר פעם אחת</span></span> 

    מהשרטוט אפשר לקרוא את כל האיברים של נוסחת בייס:

    - **הריבוע המקווקו:** כל המשפחות עם שני בנים, \( 49 \) משבצות, ולכן
      \( P(A) = 49/196 = 1/4 \).
    - **המשבצות הירוקות:** הצלב בתוך הריבוע, \( 13 \) מתוך \( 49 \). זו ההסתברות שבמשפחה
      עם שני בנים לפחות אחד נולד ביום שלישי: \( P(T \mid A) = 1 - (6/7)^2 = 13/49 \).
    - **כל המשבצות הצבעוניות:** הצלב כולו, \( 27 \) מתוך \( 196 \). כל ילד הוא "בן מיום
      שלישי" בהסתברות \( 1/14 \), ולכן \( P(T) = 1 - (13/14)^2 = 27/196 \).

    מציבים בנוסחת בייס:

    \[
    \begin{aligned}
    P(A \mid T) &= \frac{P(T \mid A)\, P(A)}{P(T)}
      = \frac{\frac{13}{49} \cdot \frac{1}{4}}{\frac{27}{196}} \\[1ex]
    &= \frac{13/196}{27/196} = \frac{13}{27}
    \end{aligned}
    \]

    **למה 13 ולא 14?** הזוג "בן מיום שלישי ובן מיום שלישי" (המשבצת המסומנת בעיגול) הוא
    משפחה אחת, אבל הוא נמצא גם בשורה וגם בעמודה של הצלב. בלי ההורדה שלו היינו מקבלים
    \( 14/28 = 1/2 \), וזו טעות.

---

### סעיף ג – הנוסחה הכללית

ליוסי יש \( C \) ילדים. כל ילד הוא בן בהסתברות \( p \), ולכל ילד יש תכונה מסוימת (כמו
"נולד ביום שלישי") בהסתברות \( q \), בלי תלות במין שלו ובשאר הילדים. ידוע שלפחות אחד
מהילדים הוא בן עם התכונה. מה ההסתברות שכל הילדים בנים?

??? tip "רמז 1"
    הסתכלו על המאורע המשלים: אף ילד איננו בן עם התכונה. מה ההסתברות שילד אחד איננו כזה?

??? tip "רמז 2"
    אם כל הילדים בנים, התנאי אומר רק שלפחות לאחד מהם יש את התכונה.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        \[
        P(A \mid T) = \frac{p^C \left(1 - (1 - q)^C\right)}{1 - (1 - pq)^C}
        \]

    #### הרעיון { .sol-idea }

    גם המונה וגם המכנה הם מאורעות של "לפחות אחד", ואת שניהם הכי קל לחשב דרך המשלים: "אף
    אחד לא". אי התלות בין הילדים הופכת כל משלים למכפלה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **המאורעות:** \( A \) הוא "כל \( C \) הילדים בנים", ו-\( T \) הוא "לפחות ילד אחד
       הוא בן עם התכונה".
    2. **המכנה:** ילד אחד הוא בן עם התכונה בהסתברות \( pq \), ואיננו כזה בהסתברות
       \( 1 - pq \). הילדים בלתי תלויים, ולכן אף אחד מהם איננו כזה בהסתברות
       \( (1 - pq)^C \), ו-\( P(T) = 1 - (1 - pq)^C \).
    3. **המונה:** כל הילדים בנים בהסתברות \( p^C \). אם כולם בנים, \( T \) אומר רק שלפחות
       לאחד יש התכונה, וזה קורה בהסתברות \( 1 - (1 - q)^C \). לכן
       \( P(A \cap T) = p^C \left(1 - (1 - q)^C\right) \).
    4. **היחס:** מחלקים את המונה במכנה, ומקבלים את הנוסחה.

    </div>

    #### למה זה נכון { .sol-proof }

    הנוסחה מחזירה את שני הסעיפים הקודמים, עם \( C = 2 \) ו-\( p = 1/2 \):

    - **בלי תכונה,** כלומר \( q = 1 \): מתקבל
      \( p^C / \left(1 - (1 - p)^C\right) = \frac{1/4}{3/4} = 1/3 \), התשובה של סעיף א.
    - **יום בשבוע,** כלומר \( q = 1/7 \): המונה הוא \( \frac{1}{4} \cdot \frac{13}{49} = \frac{13}{196} \)
      והמכנה הוא \( 1 - (13/14)^2 = \frac{27}{196} \), ולכן מתקבל \( 13/27 \), התשובה של
      סעיף ב.
    - **תכונה נדירה מאוד,** כלומר \( q \to 0 \): בקירוב \( (1 - q)^C \approx 1 - Cq \)
      ו-\( (1 - pq)^C \approx 1 - Cpq \), ולכן התשובה שואפת ל-\( p^{C-1} \). תכונה נדירה
      מצביעה כמעט בוודאות על בן **אחד מסוים**, ונשארת רק השאלה על שאר הילדים. עם שני
      ילדים זה בדיוק החצי של "הבכור הוא בן".

    ערכים לדוגמה, עם \( p = 1/2 \):

    | התכונה | ‏\( C = 2 \) | ‏\( C = 3 \) |
    |---|---|---|
    | בלי תכונה (סעיף א), \( q = 1 \) | ‏\( 1/3 \approx 0.333 \) | ‏\( 1/7 \approx 0.143 \) |
    | הטלת מטבע, \( q = 1/2 \) | ‏\( 3/7 \approx 0.429 \) | ‏\( 7/37 \approx 0.189 \) |
    | יום בשבוע, \( q = 1/7 \) | ‏\( 13/27 \approx 0.481 \) | ‏\( 127/547 \approx 0.232 \) |
    | יום בשנה, \( q = 1/365 \) | ‏\( 729/1459 \approx 0.500 \) | ‏\( 398581/1596511 \approx 0.250 \) |

    ככל ש-\( q \) קטן, המידע ספציפי יותר והתשובה עולה מ-\( (1/2)^C / (1 - (1/2)^C) \)
    לכיוון \( (1/2)^{C-1} \).

## נקודות חשובות ושאלות המשך

??? trap "מלכודת: איך יוסי מסר את המידע"
    התשובה תלויה ב**דרך** שבה התקבל המידע, ולא רק בתוכן שלו. בשאלה אנחנו שאלנו את יוסי
    שאלה של כן או לא, ולכן כל המשפחות שמקיימות את התנאי נשארות במשחק. אם יוסי היה בוחר
    ילד אחד באקראי ומספר עליו "הוא בן שנולד ביום שלישי", המידע היה על ילד מסוים, והתשובה
    בשני הסעיפים הייתה \( 1/2 \). כדאי לומר את ההנחה הזו בקול בראיון.

??? trap "מלכודת: לספור את יום שלישי פעמיים"
    בסעיף ב קל לספור 14 זוגות לכל ילד ולקבל \( 14 + 14 = 28 \) זוגות בתנאי ו-\( 14 \)
    זוגות של שני בנים, כלומר חצי. הזוג "שני בנים מיום שלישי" נמצא בשתי הקבוצות, ומורידים
    אותו פעם אחת מכל ספירה.

??? trap "מלכודת: בן ובת כתוצאה אחת"
    אם מחשבים את סעיף א עם שלוש תוצאות, "שני בנים", "בן ובת" ו"שתי בנות", ומניחים שכל
    אחת מהן בהסתברות \( 1/3 \), מקבלים \( 1/2 \). אבל "בן ובת" קורה בשני סדרים, ולכן
    ההסתברות שלה היא \( 1/2 \) ולא \( 1/3 \). מרחב מדגם עם תוצאות שוות הסתברות מקבלים רק
    כשמסדרים את הילדים.

??? followup "שאלות המשך"
    - **הבכור הוא בן:** מה התשובה אם ידוע שהילד **הבכור** הוא בן? למה המידע הזה שונה
      מ"לפחות אחד"?
    - **שלושה ילדים:** ליוסי שלושה ילדים ולפחות אחד מהם בן. מה ההסתברות שכולם בנים? בדקו
      מול הטבלה של סעיף ג.
    - **יום הולדת:** מה התשובה אם ידוע שיש בן שנולד ב-1 בינואר? למה היא כמעט בדיוק חצי?
    - **סימולציה ב-SystemVerilog:** איך מאמתים את \( 13/27 \) בסימולציה? אפשר להגריל מין
      ויום לכל ילד ולזרוק את ההגרלות שלא מקיימות את התנאי. האם מותר לשים את התנאי
      ב-`constraint` במקום לזרוק? (כן: פותר האילוצים בוחר באחידות מבין הצירופים החוקיים,
      ו-196 הצירופים שווי הסתברות מלכתחילה. `solve ... before` היה מקלקל את האחידות.)
