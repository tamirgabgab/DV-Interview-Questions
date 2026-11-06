---
id: 95
title: החיילים של Conway – כמה רחוק אפשר להגיע מעבר לקו
level: senior
difficulty: hard
kind: math
tags: [logic-puzzles, proof, algorithms, python]
source: "חידה של John Conway, 1961"
added: 2026-11-06
---

## השאלה

על לוח משבצות אינסופי מתוח קו אופקי. מתחת לקו, בשורה 0 ובכל השורות שמתחתיה, אפשר להציב
חיילים, כמה שרוצים, אבל מספר סופי. מעל הקו אין אף חייל בהתחלה, והשורות שם ממוספרות 1, 2, 3
וכן הלאה. משבצת נכתבת כזוג \( (x, y) \) : ‏\( x \) העמודה, ו-\( y \) השורה.

מהלך הוא קפיצה של סוליטר : חייל קופץ מעל שכן צמוד, למעלה, למטה, ימינה או שמאלה, אל המשבצת
הריקה שמעבר לשכן, והשכן שקפצו מעליו יוצא מהלוח. אין קפיצות באלכסון. המטרה היא להביא חייל
אחד, אחד מספיק, רחוק ככל האפשר מעל הקו :

<!-- gen 0 -->

<svg class="figure cy-fig" viewBox="0 0 290 163" style="max-width:22.7rem" role="img" aria-label="שני לוחות. בימני חיילים בכל משבצת מתחת לקו, בשורות 0 ומטה, והשורות מעל הקו ממוספרות 1, 2, 3. בשמאלי קפיצה אחת : החייל במשבצת (1, -1) קופץ מעל השכן שלו ב-(1, 0) אל המשבצת הריקה (1, 1) בשורה 1, והחייל שבאמצע יוצא מהלוח"><rect class="cy-sky" x="169.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="186.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="203.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="220.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="237.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="254.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="271.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="169.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="186.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="203.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="220.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="237.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="254.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="271.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="169.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="186.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="203.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="220.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="237.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="254.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="271.5" y="56.5" width="16" height="16"/><rect class="cy-ground" x="169.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="186.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="203.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="220.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="237.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="254.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="271.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="169.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="186.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="203.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="220.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="237.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="254.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="271.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="169.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="186.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="203.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="220.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="237.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="254.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="271.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="169.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="186.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="203.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="220.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="237.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="254.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="271.5" y="124.5" width="16" height="16"/><line class="cy-line" x1="167" y1="73" x2="290" y2="73"/><circle class="cy-man" cx="177.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="177.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="177.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="177.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="194.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="194.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="194.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="194.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="211.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="211.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="211.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="211.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="228.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="228.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="228.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="228.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="245.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="245.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="245.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="245.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="262.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="262.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="262.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="262.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="279.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="279.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="279.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="279.5" cy="81.5" r="5.44"/><text class="cy-lab" x="162" y="34.5" text-anchor="middle">3</text><text class="cy-lab" x="162" y="51.5" text-anchor="middle">2</text><text class="cy-lab" x="162" y="68.5" text-anchor="middle">1</text><text class="cy-cap" x="228.5" y="156" text-anchor="middle" direction="rtl">חיילים מתחת לקו</text><rect class="cy-sky" x="16.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="33.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="50.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="67.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="84.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="101.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="118.5" y="22.5" width="16" height="16"/><rect class="cy-sky" x="16.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="33.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="50.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="67.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="84.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="101.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="118.5" y="39.5" width="16" height="16"/><rect class="cy-sky" x="16.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="33.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="50.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="67.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="84.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="101.5" y="56.5" width="16" height="16"/><rect class="cy-sky" x="118.5" y="56.5" width="16" height="16"/><rect class="cy-ground" x="16.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="33.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="50.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="67.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="84.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="101.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="118.5" y="73.5" width="16" height="16"/><rect class="cy-ground" x="16.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="33.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="50.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="67.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="84.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="101.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="118.5" y="90.5" width="16" height="16"/><rect class="cy-ground" x="16.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="33.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="50.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="67.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="84.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="101.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="118.5" y="107.5" width="16" height="16"/><rect class="cy-ground" x="16.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="33.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="50.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="67.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="84.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="101.5" y="124.5" width="16" height="16"/><rect class="cy-ground" x="118.5" y="124.5" width="16" height="16"/><line class="cy-line" x1="14" y1="73" x2="137" y2="73"/><circle class="cy-gone" cx="92.5" cy="98.5" r="5.44"/><circle class="cy-gone" cx="92.5" cy="81.5" r="5.44"/><path class="cy-arrow" d="M92.5,98.5 L92.5,64.5"/><circle class="cy-man" cx="24.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="24.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="24.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="24.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="41.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="41.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="41.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="41.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="58.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="58.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="58.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="58.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="75.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="75.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="75.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="75.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="92.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="92.5" cy="115.5" r="5.44"/><circle class="cy-new" cx="92.5" cy="64.5" r="5.44"/><circle class="cy-man" cx="109.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="109.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="109.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="109.5" cy="81.5" r="5.44"/><circle class="cy-man" cx="126.5" cy="132.5" r="5.44"/><circle class="cy-man" cx="126.5" cy="115.5" r="5.44"/><circle class="cy-man" cx="126.5" cy="98.5" r="5.44"/><circle class="cy-man" cx="126.5" cy="81.5" r="5.44"/><text class="cy-lab" x="9" y="34.5" text-anchor="middle">3</text><text class="cy-lab" x="9" y="51.5" text-anchor="middle">2</text><text class="cy-lab" x="9" y="68.5" text-anchor="middle">1</text><text class="cy-cap" x="75.5" y="156" text-anchor="middle" direction="rtl">קפיצה לשורה 1</text></svg>

<span class="viz-legend"><span><i class="cy-key-man"></i>חייל</span><span><i class="cy-key-new"></i>החייל שקפץ</span><span><i class="cy-key-gone"></i>המשבצות שהקפיצה פינתה</span><span><i class="cy-key-line"></i>הקו</span></span>

<!-- /gen -->

- **סעיף א – שורות 1, 2 ו-3 :** הראו איך מגיעים לשורה 1 בשני חיילים, לשורה 2 בארבעה ולשורה 3
  בשמונה.
- **סעיף ב – שורה 4 :** מצאו הצבה של 20 חיילים שמגיעה לשורה 4, וכתבו תוכנית שמוצאת אותה.
- **סעיף ג – שורה 5 :** הוכיחו שאף צבא סופי לא מגיע לשורה 5, כמה חיילים שלא יהיו.

??? interviewer "מה המראיין בודק"
    - **פירוק לבעיות קטנות :** האם המועמד רואה שכדי להגיע לשורה \( n \) צריך שני חיילים צמודים
      מתחתיה, ובונה את הפתרון מפתרונות של שורות נמוכות יותר.
    - **חיפוש מהסוף :** האם הוא מבין שקל יותר לחפש אחורה, מהחייל ביעד, מאשר לנחש הצבה ולנסות
      קדימה, ואיך גוזמים את החיפוש.
    - **אינווריאנטה :** הוכחה שמשהו בלתי אפשרי היא כמעט תמיד כמות שקפיצה לא מגדילה. האם הוא
      מחפש משקל לכל משבצת, ומגיע לבד לתנאי \( \sigma^2 + \sigma = 1 \).
    - **דיוק :** הסכום של כל חצי המישור הוא בדיוק 1. האם המועמד שם לב למה שוויון מספיק, כי
      הצבא סופי.

---

### סעיף א – שורות 1, 2 ו-3

הראו איך מגיעים לשורה 1 בשני חיילים, לשורה 2 בארבעה ולשורה 3 בשמונה.

??? tip "רמז 1"
    כדי שחייל ינחת ב-\( (0, n) \) צריך שני חיילים צמודים זה לזה בשורה, או אחד מעל השני בעמודה,
    שהקרוב מביניהם צמוד ל-\( (0, n) \). הכי טבעי : חייל ב-\( (0, n-1) \) וחייל ב-\( (0, n-2) \).

??? tip "רמז 2"
    לשורה 3 צריך בו בזמן חייל בשורה 1 וחייל בשורה 2. בנו קודם את שורה 2 כמו בשורה 2, ואז הביאו
    עוד חייל לשורה 1.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        לשורה 1 : שני חיילים זה מעל זה, והתחתון קופץ. לשורה 2 : שלושה בשורה 0 ועוד אחד מתחת
        לימני שבהם, שלוש קפיצות. לשורה 3 : חמישה בשורה 0 ושלושה מתחת לשלושה הימניים, שבע
        קפיצות. כל קפיצה מורידה
        חייל אחד, ולכן מ-\( k \) חיילים עושים בדיוק \( k - 1 \) קפיצות.

    <!-- cost: קפיצות \( k - 1 \) | בדיקה \( O(k) \) -->

    #### הרעיון { .sol-idea }

    **שורה 1.** חייל ב-\( (0, -1) \) קופץ מעל \( (0, 0) \) אל \( (0, 1) \). שני חיילים, קפיצה
    אחת.

    **שורה 2.** החייל האחרון קופץ מ-\( (0, 0) \) מעל \( (0, 1) \). אז צריך בו בזמן חייל
    ב-\( (0, 1) \), שבונים כמו בשורה 1, ועוד חייל ב-\( (0, 0) \), שהבנייה של \( (0, 1) \) כבר
    רוקנה. ממלאים אותו מהצד : ‏\( (-2, 0) \) קופץ מעל \( (-1, 0) \). ארבעה חיילים :

    <!-- gen 1 -->

    <svg class="figure cy-fig" viewBox="0 0 170 104" style="max-width:13.3rem" role="img" aria-label="שורה 1 בשני חיילים. ההתחלה : 2 חיילים, (0, 0), (0, -1); מהלך 1 : החייל ב-(0, -1) קופץ מעל (0, 0) אל (0, 1)"><rect class="cy-sky" x="108.5" y="22.5" width="19" height="19"/><rect class="cy-sky" x="128.5" y="22.5" width="19" height="19"/><rect class="cy-sky" x="148.5" y="22.5" width="19" height="19"/><rect class="cy-ground" x="108.5" y="42.5" width="19" height="19"/><rect class="cy-ground" x="128.5" y="42.5" width="19" height="19"/><rect class="cy-ground" x="148.5" y="42.5" width="19" height="19"/><rect class="cy-ground" x="108.5" y="62.5" width="19" height="19"/><rect class="cy-ground" x="128.5" y="62.5" width="19" height="19"/><rect class="cy-ground" x="148.5" y="62.5" width="19" height="19"/><line class="cy-line" x1="106" y1="42" x2="170" y2="42"/><rect class="cy-target" x="129.5" y="23.5" width="17" height="17" rx="2"/><circle class="cy-man" cx="138" cy="72" r="6.4"/><circle class="cy-man" cx="138" cy="52" r="6.4"/><text class="cy-lab" x="101" y="36" text-anchor="middle">1</text><text class="cy-cap" x="138" y="97" text-anchor="middle" direction="rtl">ההתחלה, 2 חיילים</text><rect class="cy-sky" x="16.5" y="22.5" width="19" height="19"/><rect class="cy-sky" x="36.5" y="22.5" width="19" height="19"/><rect class="cy-sky" x="56.5" y="22.5" width="19" height="19"/><rect class="cy-ground" x="16.5" y="42.5" width="19" height="19"/><rect class="cy-ground" x="36.5" y="42.5" width="19" height="19"/><rect class="cy-ground" x="56.5" y="42.5" width="19" height="19"/><rect class="cy-ground" x="16.5" y="62.5" width="19" height="19"/><rect class="cy-ground" x="36.5" y="62.5" width="19" height="19"/><rect class="cy-ground" x="56.5" y="62.5" width="19" height="19"/><line class="cy-line" x1="14" y1="42" x2="78" y2="42"/><rect class="cy-target" x="37.5" y="23.5" width="17" height="17" rx="2"/><circle class="cy-gone" cx="46" cy="72" r="6.4"/><circle class="cy-gone" cx="46" cy="52" r="6.4"/><path class="cy-arrow" d="M46,72 L46,32"/><circle class="cy-new" cx="46" cy="32" r="6.4"/><text class="cy-lab" x="9" y="36" text-anchor="middle">1</text><text class="cy-cap" x="46" y="97" text-anchor="middle" direction="rtl">מהלך 1</text></svg>

    <svg class="figure cy-fig" viewBox="0 0 384 116" style="max-width:30.0rem" role="img" aria-label="שורה 2 בארבעה חיילים. ההתחלה : 4 חיילים, (-2, 0), (-1, 0), (0, 0), (0, -1); מהלך 1 : החייל ב-(0, -1) קופץ מעל (0, 0) אל (0, 1); מהלך 2 : החייל ב-(-2, 0) קופץ מעל (-1, 0) אל (0, 0); מהלך 3 : החייל ב-(0, 0) קופץ מעל (0, 1) אל (0, 2)"><rect class="cy-sky" x="310.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="328.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="346.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="364.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="310.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="328.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="346.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="364.5" y="40.5" width="17" height="17"/><rect class="cy-ground" x="310.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="328.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="346.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="364.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="310.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="328.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="346.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="364.5" y="76.5" width="17" height="17"/><line class="cy-line" x1="308" y1="58" x2="384" y2="58"/><rect class="cy-target" x="347.5" y="23.5" width="15" height="15" rx="2"/><circle class="cy-man" cx="319" cy="67" r="5.76"/><circle class="cy-man" cx="337" cy="67" r="5.76"/><circle class="cy-man" cx="355" cy="85" r="5.76"/><circle class="cy-man" cx="355" cy="67" r="5.76"/><text class="cy-lab" x="303" y="35" text-anchor="middle">2</text><text class="cy-lab" x="303" y="53" text-anchor="middle">1</text><text class="cy-cap" x="346" y="109" text-anchor="middle" direction="rtl">ההתחלה, 4 חיילים</text><rect class="cy-sky" x="212.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="230.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="248.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="266.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="212.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="230.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="248.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="266.5" y="40.5" width="17" height="17"/><rect class="cy-ground" x="212.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="230.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="248.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="266.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="212.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="230.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="248.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="266.5" y="76.5" width="17" height="17"/><line class="cy-line" x1="210" y1="58" x2="286" y2="58"/><rect class="cy-target" x="249.5" y="23.5" width="15" height="15" rx="2"/><circle class="cy-gone" cx="257" cy="85" r="5.76"/><circle class="cy-gone" cx="257" cy="67" r="5.76"/><path class="cy-arrow" d="M257,85 L257,49"/><circle class="cy-man" cx="221" cy="67" r="5.76"/><circle class="cy-man" cx="239" cy="67" r="5.76"/><circle class="cy-new" cx="257" cy="49" r="5.76"/><text class="cy-lab" x="205" y="35" text-anchor="middle">2</text><text class="cy-lab" x="205" y="53" text-anchor="middle">1</text><text class="cy-cap" x="248" y="109" text-anchor="middle" direction="rtl">מהלך 1</text><rect class="cy-sky" x="114.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="132.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="150.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="168.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="114.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="132.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="150.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="168.5" y="40.5" width="17" height="17"/><rect class="cy-ground" x="114.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="132.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="150.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="168.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="114.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="132.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="150.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="168.5" y="76.5" width="17" height="17"/><line class="cy-line" x1="112" y1="58" x2="188" y2="58"/><rect class="cy-target" x="151.5" y="23.5" width="15" height="15" rx="2"/><circle class="cy-gone" cx="123" cy="67" r="5.76"/><circle class="cy-gone" cx="141" cy="67" r="5.76"/><path class="cy-arrow" d="M123,67 L159,67"/><circle class="cy-new" cx="159" cy="67" r="5.76"/><circle class="cy-man" cx="159" cy="49" r="5.76"/><text class="cy-lab" x="107" y="35" text-anchor="middle">2</text><text class="cy-lab" x="107" y="53" text-anchor="middle">1</text><text class="cy-cap" x="150" y="109" text-anchor="middle" direction="rtl">מהלך 2</text><rect class="cy-sky" x="16.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="34.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="52.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="70.5" y="22.5" width="17" height="17"/><rect class="cy-sky" x="16.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="34.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="52.5" y="40.5" width="17" height="17"/><rect class="cy-sky" x="70.5" y="40.5" width="17" height="17"/><rect class="cy-ground" x="16.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="34.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="52.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="70.5" y="58.5" width="17" height="17"/><rect class="cy-ground" x="16.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="34.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="52.5" y="76.5" width="17" height="17"/><rect class="cy-ground" x="70.5" y="76.5" width="17" height="17"/><line class="cy-line" x1="14" y1="58" x2="90" y2="58"/><rect class="cy-target" x="53.5" y="23.5" width="15" height="15" rx="2"/><circle class="cy-gone" cx="61" cy="67" r="5.76"/><circle class="cy-gone" cx="61" cy="49" r="5.76"/><path class="cy-arrow" d="M61,67 L61,31"/><circle class="cy-new" cx="61" cy="31" r="5.76"/><text class="cy-lab" x="9" y="35" text-anchor="middle">2</text><text class="cy-lab" x="9" y="53" text-anchor="middle">1</text><text class="cy-cap" x="52" y="109" text-anchor="middle" direction="rtl">מהלך 3</text></svg>

    <span class="viz-legend"><span><i class="cy-key-man"></i>חייל</span><span><i class="cy-key-new"></i>החייל שקפץ</span><span><i class="cy-key-gone"></i>המשבצות שהקפיצה פינתה</span><span><i class="cy-key-target"></i>היעד</span></span>

    <!-- /gen -->

    **שורה 3.** אותו רעיון שורה אחת למעלה : צריך חייל ב-\( (0, 2) \) וחייל ב-\( (0, 1) \).
    בונים את \( (0, 1) \) פעם אחת בעזרת שני חיילים שעולים לשורה 1 בצד, מ-\( (1, 1) \)
    ומ-\( (2, 1) \). משם : ‏\( (0, 0) \) קופץ ל-\( (0, 2) \), ממלאים את \( (0, 0) \) מהצד,
    ‏\( (0, -1) \) עולה ל-\( (0, 1) \), והקפיצה האחרונה :

    <!-- gen 2 -->

    <svg class="figure cy-fig" viewBox="0 0 390 119" style="max-width:30.5rem" role="img" aria-label="שורה 3 בשמונה חיילים, חלק ראשון. ההתחלה : 8 חיילים, (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (0, -1), (1, -1), (2, -1); מהלך 1 : החייל ב-(2, -1) קופץ מעל (2, 0) אל (2, 1); מהלך 2 : החייל ב-(1, -1) קופץ מעל (1, 0) אל (1, 1); מהלך 3 : החייל ב-(2, 1) קופץ מעל (1, 1) אל (0, 1)"><rect class="cy-sky" x="313.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="328.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="343.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="358.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="373.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="313.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="328.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="343.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="358.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="373.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="313.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="328.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="343.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="358.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="373.5" y="52.5" width="14" height="14"/><rect class="cy-ground" x="313.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="328.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="343.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="358.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="373.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="313.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="328.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="343.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="358.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="373.5" y="82.5" width="14" height="14"/><line class="cy-line" x1="311" y1="67" x2="390" y2="67"/><rect class="cy-target" x="344.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-man" cx="320.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="335.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="350.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="350.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="365.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="365.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="380.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="380.5" cy="74.5" r="4.8"/><text class="cy-lab" x="306" y="33.5" text-anchor="middle">3</text><text class="cy-lab" x="306" y="48.5" text-anchor="middle">2</text><text class="cy-lab" x="306" y="63.5" text-anchor="middle">1</text><text class="cy-cap" x="350.5" y="112" text-anchor="middle" direction="rtl">ההתחלה, 8 חיילים</text><rect class="cy-sky" x="214.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="229.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="244.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="259.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="274.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="214.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="229.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="244.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="259.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="274.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="214.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="229.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="244.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="259.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="274.5" y="52.5" width="14" height="14"/><rect class="cy-ground" x="214.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="229.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="244.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="259.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="274.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="214.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="229.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="244.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="259.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="274.5" y="82.5" width="14" height="14"/><line class="cy-line" x1="212" y1="67" x2="291" y2="67"/><rect class="cy-target" x="245.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-gone" cx="281.5" cy="89.5" r="4.8"/><circle class="cy-gone" cx="281.5" cy="74.5" r="4.8"/><path class="cy-arrow" d="M281.5,89.5 L281.5,59.5"/><circle class="cy-man" cx="221.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="236.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="251.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="251.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="266.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="266.5" cy="74.5" r="4.8"/><circle class="cy-new" cx="281.5" cy="59.5" r="4.8"/><text class="cy-lab" x="207" y="33.5" text-anchor="middle">3</text><text class="cy-lab" x="207" y="48.5" text-anchor="middle">2</text><text class="cy-lab" x="207" y="63.5" text-anchor="middle">1</text><text class="cy-cap" x="251.5" y="112" text-anchor="middle" direction="rtl">מהלך 1</text><rect class="cy-sky" x="115.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="130.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="145.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="160.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="175.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="115.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="130.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="145.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="160.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="175.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="115.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="130.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="145.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="160.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="175.5" y="52.5" width="14" height="14"/><rect class="cy-ground" x="115.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="130.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="145.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="160.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="175.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="115.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="130.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="145.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="160.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="175.5" y="82.5" width="14" height="14"/><line class="cy-line" x1="113" y1="67" x2="192" y2="67"/><rect class="cy-target" x="146.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-gone" cx="167.5" cy="89.5" r="4.8"/><circle class="cy-gone" cx="167.5" cy="74.5" r="4.8"/><path class="cy-arrow" d="M167.5,89.5 L167.5,59.5"/><circle class="cy-man" cx="122.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="137.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="152.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="152.5" cy="74.5" r="4.8"/><circle class="cy-new" cx="167.5" cy="59.5" r="4.8"/><circle class="cy-man" cx="182.5" cy="59.5" r="4.8"/><text class="cy-lab" x="108" y="33.5" text-anchor="middle">3</text><text class="cy-lab" x="108" y="48.5" text-anchor="middle">2</text><text class="cy-lab" x="108" y="63.5" text-anchor="middle">1</text><text class="cy-cap" x="152.5" y="112" text-anchor="middle" direction="rtl">מהלך 2</text><rect class="cy-sky" x="16.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="31.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="46.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="61.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="76.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="16.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="31.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="46.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="61.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="76.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="16.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="31.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="46.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="61.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="76.5" y="52.5" width="14" height="14"/><rect class="cy-ground" x="16.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="31.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="46.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="61.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="76.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="16.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="31.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="46.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="61.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="76.5" y="82.5" width="14" height="14"/><line class="cy-line" x1="14" y1="67" x2="93" y2="67"/><rect class="cy-target" x="47.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-gone" cx="83.5" cy="59.5" r="4.8"/><circle class="cy-gone" cx="68.5" cy="59.5" r="4.8"/><path class="cy-arrow" d="M83.5,59.5 L53.5,59.5"/><circle class="cy-man" cx="23.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="38.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="53.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="53.5" cy="74.5" r="4.8"/><circle class="cy-new" cx="53.5" cy="59.5" r="4.8"/><text class="cy-lab" x="9" y="33.5" text-anchor="middle">3</text><text class="cy-lab" x="9" y="48.5" text-anchor="middle">2</text><text class="cy-lab" x="9" y="63.5" text-anchor="middle">1</text><text class="cy-cap" x="53.5" y="112" text-anchor="middle" direction="rtl">מהלך 3</text></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <svg class="figure cy-fig" viewBox="0 0 390 119" style="max-width:30.5rem" role="img" aria-label="שורה 3 בשמונה חיילים, חלק שני. מהלך 4 : החייל ב-(0, 0) קופץ מעל (0, 1) אל (0, 2); מהלך 5 : החייל ב-(-2, 0) קופץ מעל (-1, 0) אל (0, 0); מהלך 6 : החייל ב-(0, -1) קופץ מעל (0, 0) אל (0, 1); מהלך 7 : החייל ב-(0, 1) קופץ מעל (0, 2) אל (0, 3)"><rect class="cy-sky" x="313.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="328.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="343.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="358.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="373.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="313.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="328.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="343.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="358.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="373.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="313.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="328.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="343.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="358.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="373.5" y="52.5" width="14" height="14"/><rect class="cy-ground" x="313.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="328.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="343.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="358.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="373.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="313.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="328.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="343.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="358.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="373.5" y="82.5" width="14" height="14"/><line class="cy-line" x1="311" y1="67" x2="390" y2="67"/><rect class="cy-target" x="344.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-gone" cx="350.5" cy="74.5" r="4.8"/><circle class="cy-gone" cx="350.5" cy="59.5" r="4.8"/><path class="cy-arrow" d="M350.5,74.5 L350.5,44.5"/><circle class="cy-man" cx="320.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="335.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="350.5" cy="89.5" r="4.8"/><circle class="cy-new" cx="350.5" cy="44.5" r="4.8"/><text class="cy-lab" x="306" y="33.5" text-anchor="middle">3</text><text class="cy-lab" x="306" y="48.5" text-anchor="middle">2</text><text class="cy-lab" x="306" y="63.5" text-anchor="middle">1</text><text class="cy-cap" x="350.5" y="112" text-anchor="middle" direction="rtl">מהלך 4</text><rect class="cy-sky" x="214.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="229.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="244.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="259.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="274.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="214.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="229.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="244.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="259.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="274.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="214.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="229.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="244.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="259.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="274.5" y="52.5" width="14" height="14"/><rect class="cy-ground" x="214.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="229.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="244.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="259.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="274.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="214.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="229.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="244.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="259.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="274.5" y="82.5" width="14" height="14"/><line class="cy-line" x1="212" y1="67" x2="291" y2="67"/><rect class="cy-target" x="245.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-gone" cx="221.5" cy="74.5" r="4.8"/><circle class="cy-gone" cx="236.5" cy="74.5" r="4.8"/><path class="cy-arrow" d="M221.5,74.5 L251.5,74.5"/><circle class="cy-man" cx="251.5" cy="89.5" r="4.8"/><circle class="cy-new" cx="251.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="251.5" cy="44.5" r="4.8"/><text class="cy-lab" x="207" y="33.5" text-anchor="middle">3</text><text class="cy-lab" x="207" y="48.5" text-anchor="middle">2</text><text class="cy-lab" x="207" y="63.5" text-anchor="middle">1</text><text class="cy-cap" x="251.5" y="112" text-anchor="middle" direction="rtl">מהלך 5</text><rect class="cy-sky" x="115.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="130.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="145.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="160.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="175.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="115.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="130.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="145.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="160.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="175.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="115.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="130.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="145.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="160.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="175.5" y="52.5" width="14" height="14"/><rect class="cy-ground" x="115.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="130.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="145.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="160.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="175.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="115.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="130.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="145.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="160.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="175.5" y="82.5" width="14" height="14"/><line class="cy-line" x1="113" y1="67" x2="192" y2="67"/><rect class="cy-target" x="146.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-gone" cx="152.5" cy="89.5" r="4.8"/><circle class="cy-gone" cx="152.5" cy="74.5" r="4.8"/><path class="cy-arrow" d="M152.5,89.5 L152.5,59.5"/><circle class="cy-new" cx="152.5" cy="59.5" r="4.8"/><circle class="cy-man" cx="152.5" cy="44.5" r="4.8"/><text class="cy-lab" x="108" y="33.5" text-anchor="middle">3</text><text class="cy-lab" x="108" y="48.5" text-anchor="middle">2</text><text class="cy-lab" x="108" y="63.5" text-anchor="middle">1</text><text class="cy-cap" x="152.5" y="112" text-anchor="middle" direction="rtl">מהלך 6</text><rect class="cy-sky" x="16.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="31.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="46.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="61.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="76.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="16.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="31.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="46.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="61.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="76.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="16.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="31.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="46.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="61.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="76.5" y="52.5" width="14" height="14"/><rect class="cy-ground" x="16.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="31.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="46.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="61.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="76.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="16.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="31.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="46.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="61.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="76.5" y="82.5" width="14" height="14"/><line class="cy-line" x1="14" y1="67" x2="93" y2="67"/><rect class="cy-target" x="47.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-gone" cx="53.5" cy="59.5" r="4.8"/><circle class="cy-gone" cx="53.5" cy="44.5" r="4.8"/><path class="cy-arrow" d="M53.5,59.5 L53.5,29.5"/><circle class="cy-new" cx="53.5" cy="29.5" r="4.8"/><text class="cy-lab" x="9" y="33.5" text-anchor="middle">3</text><text class="cy-lab" x="9" y="48.5" text-anchor="middle">2</text><text class="cy-lab" x="9" y="63.5" text-anchor="middle">1</text><text class="cy-cap" x="53.5" y="112" text-anchor="middle" direction="rtl">מהלך 7</text></svg>

    <span class="viz-legend"><span><i class="cy-key-man"></i>חייל</span><span><i class="cy-key-new"></i>החייל שקפץ</span><span><i class="cy-key-gone"></i>המשבצות שהקפיצה פינתה</span><span><i class="cy-key-target"></i>היעד</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הקפיצה האחרונה :** לשורה \( n \) מגיעים מ-\( (0, n-2) \) מעל \( (0, n-1) \). צריך את
       שני החיילים האלה בו בזמן.
    2. **מלמטה למעלה :** בונים קודם את החייל הגבוה, ואחריו את הנמוך, כי הבנייה של הנמוך עוברת
       דרך משבצות שהגבוה כבר לא צריך.
    3. **מילוי מהצד :** כשמשבצת בשורה 0 התרוקנה, ממלאים אותה בקפיצה אופקית של שני חיילים
       מהשורה, כמו \( (-2, 0) \) מעל \( (-1, 0) \).
    4. **בדיקה :** מריצים את הקפיצות לפי הסדר, ובודקים שכל אחת חוקית והחייל האחרון ביעד.

    </div>

    #### הקוד { .sol-code }

    משבצת היא זוג \( (x, y) \), צבא הוא קבוצה של משבצות, ומהלך הוא שלוש משבצות : מאיפה קופצים,
    מעל מי, ולאן.

    === "Python"
        ```python title="replay" linenums="1" hl_lines="7 8 10 12 18 21"
        DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))


        def jump(army: frozenset, src, over, dst) -> frozenset:
            """One move: the soldier at src jumps over its neighbour at over into the empty
            dst, and the soldier jumped over leaves the board."""
            step = (over[0] - src[0], over[1] - src[1])
            if step not in DIRS or (dst[0] - over[0], dst[1] - over[1]) != step:  # (1)!
                raise ValueError(f"{src} -> {dst} is not a jump over {over}")
            if src not in army or over not in army or dst in army:                 # (2)!
                raise ValueError(f"{src} over {over} into {dst}: a soldier is missing or dst is taken")
            return (army - {src, over}) | {dst}


        def replay(army, moves) -> list:
            """Every board on the way, from an army below the line (y <= 0)."""
            boards = [frozenset(army)]
            if any(y > 0 for _, y in boards[0]):                                   # (3)!
                raise ValueError("the army starts below the line")
            for mv in moves:
                boards.append(jump(boards[-1], *mv))
            return boards


        SOLUTIONS = {                                                              # (4)!
            1: ({(0, 0), (0, -1)},
                [((0, -1), (0, 0), (0, 1))]),
            2: ({(-2, 0), (-1, 0), (0, 0), (0, -1)},
                [((0, -1), (0, 0), (0, 1)), ((-2, 0), (-1, 0), (0, 0)), ((0, 0), (0, 1), (0, 2))]),
            3: ({(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (0, -1), (1, -1), (2, -1)},
                [((2, -1), (2, 0), (2, 1)), ((1, -1), (1, 0), (1, 1)), ((2, 1), (1, 1), (0, 1)),
                 ((0, 0), (0, 1), (0, 2)), ((-2, 0), (-1, 0), (0, 0)), ((0, -1), (0, 0), (0, 1)),
                 ((0, 1), (0, 2), (0, 3))]),
        }
        ```

        1. ‏over צמוד ל-src, ו-dst צמוד ל-over באותו כיוון : קפיצה של שתי משבצות בשורה או בעמודה.
        2. יש חייל לקפוץ איתו ויש חייל לקפוץ מעליו, והמשבצת שנוחתים בה ריקה.
        3. הצבא מתחיל רק מתחת לקו, בשורה 0 ומטה.
        4. שלושת הפתרונות של הסעיף : ההצבה, ואחריה הקפיצות לפי הסדר.

    #### למה זה נכון { .sol-proof }

    ‏`replay` בודקת כל קפיצה : שהיא באורך שתיים בשורה או בעמודה, שיש חייל במוצא ובאמצע, ושהנחיתה
    ריקה. שלושת הפתרונות עוברים אותה, והחייל האחרון של כל אחד נוחת ב-\( (0, n) \).

    ולמה לא פחות? כל קפיצה מורידה חייל, אז \( k \) חיילים עושים \( k - 1 \) קפיצות לכל היותר.
    שורה 1 צריכה קפיצה אחת לפחות, כלומר שני חיילים. ששורה 2 צריכה ארבעה ושורה 3 שמונה, יוצא
    מהפוטנציאל של סעיף ג : שלוש המשבצות הכבדות ביותר שוקלות פחות מ-1 ביחס ל-\( (0, 2) \), ושבע
    הכבדות פחות מ-1 ביחס ל-\( (0, 3) \).

    **נסו בעצמכם.** בחרו שורה ונגנו את הפתרון שלה מהלך אחר מהלך, או שחקו בעצמכם : לוחצים על חייל
    ואז על המשבצת הריקה שמעבר לשכן שלו.

    <div class="explorer" data-kind="soldiers" data-row="3"></div>

    #### סיבוכיות { .sol-cost }

    הבדיקה של \( k \) חיילים היא \( k - 1 \) קפיצות, כל אחת בזמן קבוע : \( O(k) \).

---

### סעיף ב – שורה 4

מצאו הצבה של 20 חיילים שמגיעה לשורה 4, וכתבו תוכנית שמוצאת אותה.

??? tip "רמז 1"
    לחפש קדימה קשה : לא יודעים איפה להציב, ובכל צעד יש הרבה קפיצות. חפשו אחורה : מתחילים
    מחייל אחד ב-\( (0, 4) \), ו"מבטלים" קפיצה : חייל ב-\( c \) הופך לשני חיילים, ב-\( b \)
    וב-\( a \), במשבצות הריקות שלפניו.

??? tip "רמז 2"
    חייל בשורה \( h \) עולה לפחות כמו כל הדרך לשורה \( h \) : 2, 4 או 8 חיילים, כי לחיילים
    שונים יש "אבות" שונים. אם סכום המחירים של כל החיילים עובר את 20, אפשר לוותר על הענף.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        עשרים חיילים : שבעה בשורה 0, מ-\( x = -2 \) עד \( x = 4 \); שישה בשורה \( -1 \), עד
        \( x = 3 \); חמישה בשורה \( -2 \), עד \( x = 2 \); ושניים בשורה \( -3 \), ב-\( x = 0 \)
        וב-\( x = 2 \). ‏19 קפיצות : ב-12 הראשונות בונים את הצבא של שורה 3, שורה אחת למעלה,
        וב-7 האחרונות משחקים את הפתרון של שורה 3. חיפוש אחורה עם שני גיזומים מוצא את זה בכמה
        שניות.

    <!-- cost: קפיצות 19 | חיפוש כ-150 אלף מצבים -->

    #### הרעיון { .sol-idea }

    **אחורה.** ביטול של קפיצה הופך חייל ב-\( c \) לשני חיילים ב-\( b \) וב-\( a \), כש-\( a \),
    ‏\( b \), ‏\( c \) שלוש משבצות רצופות בשורה או בעמודה, ו-\( a \), ‏\( b \) ריקות. מתחילים
    מחייל אחד ב-\( (0, 4) \), מבטלים קפיצות, ומחפשים מצב שבו כל החיילים מתחת לקו. מ-20 חיילים
    יש בדיוק 19 קפיצות.

    **גיזום ראשון, מחיר לכל גובה.** כל חייל על הלוח, בכל רגע, "נולד" מקבוצה של חיילים מההתחלה,
    והקבוצות של חיילים שונים זרות. חייל בשורה \( h \) צריך לבד לפחות כמה שסעיף א מצא : 1 לחייל
    מתחת לקו, ‏2 בשורה 1, ‏4 בשורה 2 ו-8 בשורה 3. אם סכום המחירים עובר את 20, הענף מת.

    **גיזום שני, הפוטנציאל.** בסעיף ג נראה שקפיצה אף פעם לא מגדילה את \( \sum \sigma^{d} \), כש-\( d \)
    המרחק מהיעד. אחורה, הסכום רק גדל, והוא חייב להישאר קטן מהסכום של 20 המשבצות הכבדות ביותר
    מתחת לקו : ‏\( 1 + \sigma^8 \approx 1.0213 \). כלומר כמעט כל ביטול חייב להיות של קפיצה ישר
    לכיוון היעד, וזה מצמצם את החיפוש מאוד.

    **מה החיפוש מצא.** אחרי 12 קפיצות נשארים בדיוק 8 חיילים : חמישה בשורה 1 ושלושה בשורה 0, הצבא
    של שורה 3 מוזז שורה אחת למעלה. משם 7 הקפיצות של שורה 3 מעלות חייל לשורה 4 :

    <!-- gen 4 -->

    <svg class="figure cy-fig" viewBox="0 0 393 164" style="max-width:30.7rem" role="img" aria-label="שורה 4 בעשרים חיילים, שלושה לוחות. בימני ההתחלה : שבעה חיילים בשורה 0 מ-x = -2 עד 4, שישה בשורה -1 מ-x = -2 עד 3, חמישה בשורה -2 מ-x = -2 עד 2, ושניים בשורה -3 ב-x = 0 וב-x = 2. באמצעי, אחרי 12 מהלכים, נשארו שמונה : חמישה בשורה 1 מ-x = -2 עד 2 ושלושה בשורה 0 מ-x = 0 עד 2, הצבא של שורה 3 שורה אחת למעלה. בשמאלי, אחרי 19 מהלכים, חייל אחד ביעד (0, 4)"><rect class="cy-sky" x="286.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="301.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="316.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="331.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="346.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="361.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="376.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="286.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="301.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="316.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="331.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="346.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="361.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="376.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="286.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="301.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="316.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="331.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="346.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="361.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="376.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="286.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="301.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="316.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="331.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="346.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="361.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="376.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="286.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="301.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="316.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="331.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="346.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="361.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="376.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="286.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="301.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="316.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="331.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="346.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="361.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="376.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="286.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="301.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="316.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="331.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="346.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="361.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="376.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="286.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="301.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="316.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="331.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="346.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="361.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="376.5" y="127.5" width="14" height="14"/><line class="cy-line" x1="284" y1="82" x2="393" y2="82"/><rect class="cy-target" x="317.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-man" cx="293.5" cy="119.5" r="4.8"/><circle class="cy-man" cx="293.5" cy="104.5" r="4.8"/><circle class="cy-man" cx="293.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="308.5" cy="119.5" r="4.8"/><circle class="cy-man" cx="308.5" cy="104.5" r="4.8"/><circle class="cy-man" cx="308.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="323.5" cy="134.5" r="4.8"/><circle class="cy-man" cx="323.5" cy="119.5" r="4.8"/><circle class="cy-man" cx="323.5" cy="104.5" r="4.8"/><circle class="cy-man" cx="323.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="338.5" cy="119.5" r="4.8"/><circle class="cy-man" cx="338.5" cy="104.5" r="4.8"/><circle class="cy-man" cx="338.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="353.5" cy="134.5" r="4.8"/><circle class="cy-man" cx="353.5" cy="119.5" r="4.8"/><circle class="cy-man" cx="353.5" cy="104.5" r="4.8"/><circle class="cy-man" cx="353.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="368.5" cy="104.5" r="4.8"/><circle class="cy-man" cx="368.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="383.5" cy="89.5" r="4.8"/><text class="cy-lab" x="279" y="33.5" text-anchor="middle">4</text><text class="cy-lab" x="279" y="48.5" text-anchor="middle">3</text><text class="cy-lab" x="279" y="63.5" text-anchor="middle">2</text><text class="cy-lab" x="279" y="78.5" text-anchor="middle">1</text><text class="cy-cap" x="338.5" y="157" text-anchor="middle" direction="rtl">ההתחלה, 20 חיילים</text><rect class="cy-sky" x="151.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="166.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="181.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="196.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="211.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="226.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="241.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="151.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="166.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="181.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="196.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="211.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="226.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="241.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="151.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="166.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="181.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="196.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="211.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="226.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="241.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="151.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="166.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="181.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="196.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="211.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="226.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="241.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="151.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="166.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="181.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="196.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="211.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="226.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="241.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="151.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="166.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="181.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="196.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="211.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="226.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="241.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="151.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="166.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="181.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="196.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="211.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="226.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="241.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="151.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="166.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="181.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="196.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="211.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="226.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="241.5" y="127.5" width="14" height="14"/><line class="cy-line" x1="149" y1="82" x2="258" y2="82"/><rect class="cy-target" x="182.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-man" cx="158.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="173.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="188.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="188.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="203.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="203.5" cy="74.5" r="4.8"/><circle class="cy-man" cx="218.5" cy="89.5" r="4.8"/><circle class="cy-man" cx="218.5" cy="74.5" r="4.8"/><text class="cy-lab" x="144" y="33.5" text-anchor="middle">4</text><text class="cy-lab" x="144" y="48.5" text-anchor="middle">3</text><text class="cy-lab" x="144" y="63.5" text-anchor="middle">2</text><text class="cy-lab" x="144" y="78.5" text-anchor="middle">1</text><text class="cy-cap" x="203.5" y="157" text-anchor="middle" direction="rtl">אחרי 12 מהלכים</text><rect class="cy-sky" x="16.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="31.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="46.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="61.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="76.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="91.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="106.5" y="22.5" width="14" height="14"/><rect class="cy-sky" x="16.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="31.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="46.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="61.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="76.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="91.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="106.5" y="37.5" width="14" height="14"/><rect class="cy-sky" x="16.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="31.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="46.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="61.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="76.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="91.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="106.5" y="52.5" width="14" height="14"/><rect class="cy-sky" x="16.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="31.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="46.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="61.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="76.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="91.5" y="67.5" width="14" height="14"/><rect class="cy-sky" x="106.5" y="67.5" width="14" height="14"/><rect class="cy-ground" x="16.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="31.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="46.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="61.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="76.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="91.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="106.5" y="82.5" width="14" height="14"/><rect class="cy-ground" x="16.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="31.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="46.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="61.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="76.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="91.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="106.5" y="97.5" width="14" height="14"/><rect class="cy-ground" x="16.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="31.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="46.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="61.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="76.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="91.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="106.5" y="112.5" width="14" height="14"/><rect class="cy-ground" x="16.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="31.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="46.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="61.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="76.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="91.5" y="127.5" width="14" height="14"/><rect class="cy-ground" x="106.5" y="127.5" width="14" height="14"/><line class="cy-line" x1="14" y1="82" x2="123" y2="82"/><rect class="cy-target" x="47.5" y="23.5" width="12" height="12" rx="2"/><circle class="cy-man" cx="53.5" cy="29.5" r="4.8"/><text class="cy-lab" x="9" y="33.5" text-anchor="middle">4</text><text class="cy-lab" x="9" y="48.5" text-anchor="middle">3</text><text class="cy-lab" x="9" y="63.5" text-anchor="middle">2</text><text class="cy-lab" x="9" y="78.5" text-anchor="middle">1</text><text class="cy-cap" x="68.5" y="157" text-anchor="middle" direction="rtl">אחרי 19 מהלכים</text></svg>

    <span class="viz-legend"><span><i class="cy-key-man"></i>חייל</span><span><i class="cy-key-target"></i>היעד</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ההתחלה :** חייל אחד ב-\( (0, 4) \). המחיר שלו כל התקציב, 20, והפוטנציאל שלו 1.
    2. **ביטול קפיצה :** לכל חייל ולכל כיוון, אם שתי המשבצות שלפניו ריקות, מחליפים אותו
       בשניים, ומעדכנים את המחיר ואת הפוטנציאל.
    3. **גיזום :** אם המחיר עבר את התקציב או הפוטנציאל עבר את התקרה, חוזרים אחורה.
    4. **זיכרון :** מצב שכבר נכשל לא נבדק שוב, וגם לא תמונת המראה שלו.
    5. **סוף :** כשכל החיילים מתחת לקו, ההצבה נמצאה, והקפיצות הן הביטולים בסדר הפוך.

    </div>

    #### הקוד { .sol-code }

    הקוד משתמש ב-`DIRS` מסעיף א, והמחירים של שורות 1 עד 3 הם מה שסעיף א מצא.

    === "Python"
        ```python title="search" linenums="1" hl_lines="7 8 12 16 22 32 33 34"
        NEED = {0: 1, 1: 2, 2: 4, 3: 8}    # the fewest soldiers for one soldier on row h (part a)


        def search(n: int, budget: int, width: int = 4, depth: int = 5):
            """A start of at most `budget` soldiers that sends one to (0, n), found backwards:
            from the lone soldier on the target, undo jumps. Returns (army, moves) or None."""
            def cost(c):                                                           # (1)!
                return NEED[max(c[1], 0)] if c[1] < n else budget

            sig = (5 ** 0.5 - 1) / 2
            def weight(c):                                                         # (2)!
                return sig ** (abs(c[0]) + abs(n - c[1]))

            below = sorted((weight((x, y)) for x in range(-width, width + 1)
                            for y in range(-depth, 1)), reverse=True)
            cap = sum(below[:budget]) + 1e-9                                       # (3)!
            seen, path = set(), []

            def back(army, used, pot):
                if all(y <= 0 for _, y in army):
                    return True
                key = min(tuple(sorted(army)), tuple(sorted((-x, y) for x, y in army)))  # (4)!
                if key in seen:
                    return False
                seen.add(key)
                for c in sorted(army, key=lambda c: (-c[1], abs(c[0]))):
                    for dx, dy in DIRS:
                        b, a = (c[0] - dx, c[1] - dy), (c[0] - 2 * dx, c[1] - 2 * dy)
                        if a in army or b in army or abs(a[0]) > width or abs(b[0]) > width \
                                or min(a[1], b[1]) < -depth:
                            continue
                        used2 = used - cost(c) + cost(a) + cost(b)
                        pot2 = pot - weight(c) + weight(a) + weight(b)
                        if used2 > budget or pot2 > cap:                           # (5)!
                            continue
                        path.append((a, b, c))
                        if back((army - {c}) | {a, b}, used2, pot2):
                            return True
                        path.pop()
                return False

            if not back(frozenset({(0, n)}), budget, 1.0):
                return None
            army = {(0, n)}
            for a, b, c in path:
                army = (army - {c}) | {a, b}
            return army, list(reversed(path))                                      # (6)!
        ```

        1. המחיר של חייל לפי השורה שלו. חייל בשורה \( n \) ומעליה עולה את כל התקציב : רק היעד
           עצמו יכול לעמוד שם.
        2. ‏\( \sigma^{d} \), כש-\( d \) מספר הצעדים עד היעד. כאן בנקודה צפה, רק כדי לגזום.
        3. התקרה : סכום המשקלים של \( k \) המשבצות הכבדות ביותר מתחת לקו, עם מרווח קטן כדי ששגיאת
           עיגול לא תגזום ענף טוב.
        4. מצב ותמונת המראה שלו, \( x \to -x \), נשמרים כמצב אחד.
        5. שני הגיזומים : המחיר והפוטנציאל.
        6. הביטולים היו מהיעד אחורה, ולכן הקפיצות הן אותה רשימה הפוך.

    #### למה זה נכון { .sol-proof }

    **מה שהחיפוש מחזיר תקין.** כל ביטול חוקי הופך לקפיצה חוקית, ו-`replay` מסעיף א מריצה את
    19 הקפיצות ומגיעה ל-\( (0, 4) \).

    **הגיזום הראשון לא זורק פתרון.** נסתכל על כל חייל על הלוח ועל הקבוצה של חיילי ההתחלה שהוא
    "בנוי" מהם : קפיצה מחברת את הקבוצות של הקופץ ושל מי שקפצו מעליו. הקבוצות זרות, וכל חייל
    יכול להיבנות מהקבוצה שלו לבד, כי חיילים אחרים רק תופסים משבצות. לכן חייל בשורה \( h \) לבד
    צריך לפחות את המינימום של שורה \( h \), והסכום של כל החיילים חסם תחתון לגודל ההצבה.

    **הגיזום השני לא זורק פתרון.** קדימה, הפוטנציאל רק יורד (סעיף ג), אז אחורה הוא רק עולה.
    בסוף, כל החיילים מתחת לקו, ולכל היותר 20 מהם, ולכן הסכום לא יותר מ-20 המשבצות הכבדות. מצב
    שכבר עבר את התקרה לא יגיע להצבה.

    **ההצבה, והקפיצות לפי הסדר :**

    <!-- gen 5 -->

    | מהלך | שלב | החייל קופץ מ- | מעל | אל |
    |:-:|:-:|:-:|:-:|:-:|
    | ‏1 | בונים את הצבא של שורה 3 | ‏\( (0, -1) \) | ‏\( (0, 0) \) | ‏\( (0, 1) \) |
    | ‏2 | בונים את הצבא של שורה 3 | ‏\( (0, -3) \) | ‏\( (0, -2) \) | ‏\( (0, -1) \) |
    | ‏3 | בונים את הצבא של שורה 3 | ‏\( (-2, -2) \) | ‏\( (-1, -2) \) | ‏\( (0, -2) \) |
    | ‏4 | בונים את הצבא של שורה 3 | ‏\( (1, -1) \) | ‏\( (1, 0) \) | ‏\( (1, 1) \) |
    | ‏5 | בונים את הצבא של שורה 3 | ‏\( (3, -1) \) | ‏\( (2, -1) \) | ‏\( (1, -1) \) |
    | ‏6 | בונים את הצבא של שורה 3 | ‏\( (2, -3) \) | ‏\( (2, -2) \) | ‏\( (2, -1) \) |
    | ‏7 | בונים את הצבא של שורה 3 | ‏\( (2, -1) \) | ‏\( (2, 0) \) | ‏\( (2, 1) \) |
    | ‏8 | בונים את הצבא של שורה 3 | ‏\( (4, 0) \) | ‏\( (3, 0) \) | ‏\( (2, 0) \) |
    | ‏9 | בונים את הצבא של שורה 3 | ‏\( (1, -2) \) | ‏\( (1, -1) \) | ‏\( (1, 0) \) |
    | ‏10 | בונים את הצבא של שורה 3 | ‏\( (0, -2) \) | ‏\( (0, -1) \) | ‏\( (0, 0) \) |
    | ‏11 | בונים את הצבא של שורה 3 | ‏\( (-2, -1) \) | ‏\( (-2, 0) \) | ‏\( (-2, 1) \) |
    | ‏12 | בונים את הצבא של שורה 3 | ‏\( (-1, -1) \) | ‏\( (-1, 0) \) | ‏\( (-1, 1) \) |
    | ‏13 | הפתרון של שורה 3, שורה אחת למעלה | ‏\( (2, 0) \) | ‏\( (2, 1) \) | ‏\( (2, 2) \) |
    | ‏14 | הפתרון של שורה 3, שורה אחת למעלה | ‏\( (1, 0) \) | ‏\( (1, 1) \) | ‏\( (1, 2) \) |
    | ‏15 | הפתרון של שורה 3, שורה אחת למעלה | ‏\( (2, 2) \) | ‏\( (1, 2) \) | ‏\( (0, 2) \) |
    | ‏16 | הפתרון של שורה 3, שורה אחת למעלה | ‏\( (0, 1) \) | ‏\( (0, 2) \) | ‏\( (0, 3) \) |
    | ‏17 | הפתרון של שורה 3, שורה אחת למעלה | ‏\( (-2, 1) \) | ‏\( (-1, 1) \) | ‏\( (0, 1) \) |
    | ‏18 | הפתרון של שורה 3, שורה אחת למעלה | ‏\( (0, 0) \) | ‏\( (0, 1) \) | ‏\( (0, 2) \) |
    | ‏19 | הפתרון של שורה 3, שורה אחת למעלה | ‏\( (0, 2) \) | ‏\( (0, 3) \) | ‏\( (0, 4) \) |

    <!-- /gen -->

    **נסו בעצמכם.** נגנו את 19 הקפיצות, וראו איך המד נשאר על 1 : כל הקפיצות כאן ישר לכיוון היעד.

    <div class="explorer" data-kind="soldiers" data-row="4"></div>

    #### סיבוכיות { .sol-cost }

    בלי הגיזומים מספר המצבים עצום. עם שניהם החיפוש עובר על כ-150 אלף מצבים, כעשר שניות בפייתון.
    הגיזום של הפוטנציאל הוא העיקר : כמעט כל ביטול שלא לכיוון היעד נזרק מיד.

---

### סעיף ג – שורה 5

הוכיחו שאף צבא סופי לא מגיע לשורה 5, כמה חיילים שלא יהיו.

??? tip "רמז 1"
    תנו לכל משבצת משקל שתלוי רק במרחק שלה מהיעד \( (0, 5) \), מספר הצעדים למעלה, למטה ולצדדים,
    ‏\( \sigma^{d} \) עם \( 0 < \sigma < 1 \). מתי קפיצה ישר לכיוון היעד לא משנה את הסכום?

??? tip "רמז 2"
    קפיצה לכיוון היעד : ‏\( \sigma^{k+2} \) ו-\( \sigma^{k+1} \) יוצאים, ‏\( \sigma^{k} \) נכנס. כדי
    שזה יהיה שוויון צריך \( \sigma^2 + \sigma = 1 \). עכשיו סכמו את המשקל של כל חצי המישור.

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        המשקל של משבצת במרחק \( d \) מ-\( (0, 5) \) הוא \( \sigma^{d} \), עם \( \sigma = (\sqrt5 - 1)/2 \),
        כך ש-\( \sigma^2 + \sigma = 1 \). קפיצה אף פעם לא מגדילה את סכום המשקלים של החיילים. חייל
        ביעד לבד שוקל 1, אבל כל חצי המישור מתחת לקו שוקל בדיוק 1, ולכן כל צבא סופי שוקל פחות
        מ-1. אי אפשר להגיע.

    <!-- cost: חישוב מדויק ב-\( \mathbb{Q}(\sqrt5) \) | בלי קירוב -->

    #### הרעיון { .sol-idea }

    **משקל לכל משבצת.** ‏\( d \) הוא המרחק מהיעד, \( |x| + |5 - y| \). ביעד \( d = 0 \) והמשקל 1,
    וב-\( (0, 0) \), המשבצת הקרובה ביותר מתחת לקו, \( d = 5 \) :

    <!-- gen 6 -->

    <svg class="figure cy-fig" viewBox="0 0 234 246" style="max-width:18.3rem" role="img" aria-label="המרחק של כל משבצת מהיעד (0, 5), צעדים למעלה, למטה ולצדדים. ביעד עצמו 0, ובמשבצת (0, 0), הקרובה ביותר מתחת לקו, 5. בכל שורה המרחק גדל ב-1 לכל צעד הצידה, ובכל עמודה ב-1 לכל שורה למטה. המשקל של משבצת במרחק d הוא סיגמא בחזקת d, ומתחת לקו המשבצות כהות יותר ככל שהן קרובות"><rect class="cy-sky" x="14.5" y="22.5" width="23" height="23"/><text class="cy-wsky" x="26" y="38" text-anchor="middle">4</text><rect class="cy-sky" x="38.5" y="22.5" width="23" height="23"/><text class="cy-wsky" x="50" y="38" text-anchor="middle">3</text><rect class="cy-sky" x="62.5" y="22.5" width="23" height="23"/><text class="cy-wsky" x="74" y="38" text-anchor="middle">2</text><rect class="cy-sky" x="86.5" y="22.5" width="23" height="23"/><text class="cy-wsky" x="98" y="38" text-anchor="middle">1</text><rect class="cy-sky" x="110.5" y="22.5" width="23" height="23"/><text class="cy-wsky" x="122" y="38" text-anchor="middle">0</text><rect class="cy-sky" x="134.5" y="22.5" width="23" height="23"/><text class="cy-wsky" x="146" y="38" text-anchor="middle">1</text><rect class="cy-sky" x="158.5" y="22.5" width="23" height="23"/><text class="cy-wsky" x="170" y="38" text-anchor="middle">2</text><rect class="cy-sky" x="182.5" y="22.5" width="23" height="23"/><text class="cy-wsky" x="194" y="38" text-anchor="middle">3</text><rect class="cy-sky" x="206.5" y="22.5" width="23" height="23"/><text class="cy-wsky" x="218" y="38" text-anchor="middle">4</text><text class="cy-lab" x="7" y="38" text-anchor="middle">5</text><rect class="cy-sky" x="14.5" y="46.5" width="23" height="23"/><text class="cy-wsky" x="26" y="62" text-anchor="middle">5</text><rect class="cy-sky" x="38.5" y="46.5" width="23" height="23"/><text class="cy-wsky" x="50" y="62" text-anchor="middle">4</text><rect class="cy-sky" x="62.5" y="46.5" width="23" height="23"/><text class="cy-wsky" x="74" y="62" text-anchor="middle">3</text><rect class="cy-sky" x="86.5" y="46.5" width="23" height="23"/><text class="cy-wsky" x="98" y="62" text-anchor="middle">2</text><rect class="cy-sky" x="110.5" y="46.5" width="23" height="23"/><text class="cy-wsky" x="122" y="62" text-anchor="middle">1</text><rect class="cy-sky" x="134.5" y="46.5" width="23" height="23"/><text class="cy-wsky" x="146" y="62" text-anchor="middle">2</text><rect class="cy-sky" x="158.5" y="46.5" width="23" height="23"/><text class="cy-wsky" x="170" y="62" text-anchor="middle">3</text><rect class="cy-sky" x="182.5" y="46.5" width="23" height="23"/><text class="cy-wsky" x="194" y="62" text-anchor="middle">4</text><rect class="cy-sky" x="206.5" y="46.5" width="23" height="23"/><text class="cy-wsky" x="218" y="62" text-anchor="middle">5</text><text class="cy-lab" x="7" y="62" text-anchor="middle">4</text><rect class="cy-sky" x="14.5" y="70.5" width="23" height="23"/><text class="cy-wsky" x="26" y="86" text-anchor="middle">6</text><rect class="cy-sky" x="38.5" y="70.5" width="23" height="23"/><text class="cy-wsky" x="50" y="86" text-anchor="middle">5</text><rect class="cy-sky" x="62.5" y="70.5" width="23" height="23"/><text class="cy-wsky" x="74" y="86" text-anchor="middle">4</text><rect class="cy-sky" x="86.5" y="70.5" width="23" height="23"/><text class="cy-wsky" x="98" y="86" text-anchor="middle">3</text><rect class="cy-sky" x="110.5" y="70.5" width="23" height="23"/><text class="cy-wsky" x="122" y="86" text-anchor="middle">2</text><rect class="cy-sky" x="134.5" y="70.5" width="23" height="23"/><text class="cy-wsky" x="146" y="86" text-anchor="middle">3</text><rect class="cy-sky" x="158.5" y="70.5" width="23" height="23"/><text class="cy-wsky" x="170" y="86" text-anchor="middle">4</text><rect class="cy-sky" x="182.5" y="70.5" width="23" height="23"/><text class="cy-wsky" x="194" y="86" text-anchor="middle">5</text><rect class="cy-sky" x="206.5" y="70.5" width="23" height="23"/><text class="cy-wsky" x="218" y="86" text-anchor="middle">6</text><text class="cy-lab" x="7" y="86" text-anchor="middle">3</text><rect class="cy-sky" x="14.5" y="94.5" width="23" height="23"/><text class="cy-wsky" x="26" y="110" text-anchor="middle">7</text><rect class="cy-sky" x="38.5" y="94.5" width="23" height="23"/><text class="cy-wsky" x="50" y="110" text-anchor="middle">6</text><rect class="cy-sky" x="62.5" y="94.5" width="23" height="23"/><text class="cy-wsky" x="74" y="110" text-anchor="middle">5</text><rect class="cy-sky" x="86.5" y="94.5" width="23" height="23"/><text class="cy-wsky" x="98" y="110" text-anchor="middle">4</text><rect class="cy-sky" x="110.5" y="94.5" width="23" height="23"/><text class="cy-wsky" x="122" y="110" text-anchor="middle">3</text><rect class="cy-sky" x="134.5" y="94.5" width="23" height="23"/><text class="cy-wsky" x="146" y="110" text-anchor="middle">4</text><rect class="cy-sky" x="158.5" y="94.5" width="23" height="23"/><text class="cy-wsky" x="170" y="110" text-anchor="middle">5</text><rect class="cy-sky" x="182.5" y="94.5" width="23" height="23"/><text class="cy-wsky" x="194" y="110" text-anchor="middle">6</text><rect class="cy-sky" x="206.5" y="94.5" width="23" height="23"/><text class="cy-wsky" x="218" y="110" text-anchor="middle">7</text><text class="cy-lab" x="7" y="110" text-anchor="middle">2</text><rect class="cy-sky" x="14.5" y="118.5" width="23" height="23"/><text class="cy-wsky" x="26" y="134" text-anchor="middle">8</text><rect class="cy-sky" x="38.5" y="118.5" width="23" height="23"/><text class="cy-wsky" x="50" y="134" text-anchor="middle">7</text><rect class="cy-sky" x="62.5" y="118.5" width="23" height="23"/><text class="cy-wsky" x="74" y="134" text-anchor="middle">6</text><rect class="cy-sky" x="86.5" y="118.5" width="23" height="23"/><text class="cy-wsky" x="98" y="134" text-anchor="middle">5</text><rect class="cy-sky" x="110.5" y="118.5" width="23" height="23"/><text class="cy-wsky" x="122" y="134" text-anchor="middle">4</text><rect class="cy-sky" x="134.5" y="118.5" width="23" height="23"/><text class="cy-wsky" x="146" y="134" text-anchor="middle">5</text><rect class="cy-sky" x="158.5" y="118.5" width="23" height="23"/><text class="cy-wsky" x="170" y="134" text-anchor="middle">6</text><rect class="cy-sky" x="182.5" y="118.5" width="23" height="23"/><text class="cy-wsky" x="194" y="134" text-anchor="middle">7</text><rect class="cy-sky" x="206.5" y="118.5" width="23" height="23"/><text class="cy-wsky" x="218" y="134" text-anchor="middle">8</text><text class="cy-lab" x="7" y="134" text-anchor="middle">1</text><rect class="cy-w5" x="14.5" y="142.5" width="23" height="23"/><text class="cy-wnum" x="26" y="158" text-anchor="middle">9</text><rect class="cy-w4" x="38.5" y="142.5" width="23" height="23"/><text class="cy-wnum" x="50" y="158" text-anchor="middle">8</text><rect class="cy-w3" x="62.5" y="142.5" width="23" height="23"/><text class="cy-wnum" x="74" y="158" text-anchor="middle">7</text><rect class="cy-w2" x="86.5" y="142.5" width="23" height="23"/><text class="cy-wnum" x="98" y="158" text-anchor="middle">6</text><rect class="cy-w1" x="110.5" y="142.5" width="23" height="23"/><text class="cy-wnum" x="122" y="158" text-anchor="middle">5</text><rect class="cy-w2" x="134.5" y="142.5" width="23" height="23"/><text class="cy-wnum" x="146" y="158" text-anchor="middle">6</text><rect class="cy-w3" x="158.5" y="142.5" width="23" height="23"/><text class="cy-wnum" x="170" y="158" text-anchor="middle">7</text><rect class="cy-w4" x="182.5" y="142.5" width="23" height="23"/><text class="cy-wnum" x="194" y="158" text-anchor="middle">8</text><rect class="cy-w5" x="206.5" y="142.5" width="23" height="23"/><text class="cy-wnum" x="218" y="158" text-anchor="middle">9</text><rect class="cy-w6" x="14.5" y="166.5" width="23" height="23"/><text class="cy-wnum" x="26" y="182" text-anchor="middle">10</text><rect class="cy-w5" x="38.5" y="166.5" width="23" height="23"/><text class="cy-wnum" x="50" y="182" text-anchor="middle">9</text><rect class="cy-w4" x="62.5" y="166.5" width="23" height="23"/><text class="cy-wnum" x="74" y="182" text-anchor="middle">8</text><rect class="cy-w3" x="86.5" y="166.5" width="23" height="23"/><text class="cy-wnum" x="98" y="182" text-anchor="middle">7</text><rect class="cy-w2" x="110.5" y="166.5" width="23" height="23"/><text class="cy-wnum" x="122" y="182" text-anchor="middle">6</text><rect class="cy-w3" x="134.5" y="166.5" width="23" height="23"/><text class="cy-wnum" x="146" y="182" text-anchor="middle">7</text><rect class="cy-w4" x="158.5" y="166.5" width="23" height="23"/><text class="cy-wnum" x="170" y="182" text-anchor="middle">8</text><rect class="cy-w5" x="182.5" y="166.5" width="23" height="23"/><text class="cy-wnum" x="194" y="182" text-anchor="middle">9</text><rect class="cy-w6" x="206.5" y="166.5" width="23" height="23"/><text class="cy-wnum" x="218" y="182" text-anchor="middle">10</text><rect class="cy-w6" x="14.5" y="190.5" width="23" height="23"/><text class="cy-wnum" x="26" y="206" text-anchor="middle">11</text><rect class="cy-w6" x="38.5" y="190.5" width="23" height="23"/><text class="cy-wnum" x="50" y="206" text-anchor="middle">10</text><rect class="cy-w5" x="62.5" y="190.5" width="23" height="23"/><text class="cy-wnum" x="74" y="206" text-anchor="middle">9</text><rect class="cy-w4" x="86.5" y="190.5" width="23" height="23"/><text class="cy-wnum" x="98" y="206" text-anchor="middle">8</text><rect class="cy-w3" x="110.5" y="190.5" width="23" height="23"/><text class="cy-wnum" x="122" y="206" text-anchor="middle">7</text><rect class="cy-w4" x="134.5" y="190.5" width="23" height="23"/><text class="cy-wnum" x="146" y="206" text-anchor="middle">8</text><rect class="cy-w5" x="158.5" y="190.5" width="23" height="23"/><text class="cy-wnum" x="170" y="206" text-anchor="middle">9</text><rect class="cy-w6" x="182.5" y="190.5" width="23" height="23"/><text class="cy-wnum" x="194" y="206" text-anchor="middle">10</text><rect class="cy-w6" x="206.5" y="190.5" width="23" height="23"/><text class="cy-wnum" x="218" y="206" text-anchor="middle">11</text><rect class="cy-w6" x="14.5" y="214.5" width="23" height="23"/><text class="cy-wnum" x="26" y="230" text-anchor="middle">12</text><rect class="cy-w6" x="38.5" y="214.5" width="23" height="23"/><text class="cy-wnum" x="50" y="230" text-anchor="middle">11</text><rect class="cy-w6" x="62.5" y="214.5" width="23" height="23"/><text class="cy-wnum" x="74" y="230" text-anchor="middle">10</text><rect class="cy-w5" x="86.5" y="214.5" width="23" height="23"/><text class="cy-wnum" x="98" y="230" text-anchor="middle">9</text><rect class="cy-w4" x="110.5" y="214.5" width="23" height="23"/><text class="cy-wnum" x="122" y="230" text-anchor="middle">8</text><rect class="cy-w5" x="134.5" y="214.5" width="23" height="23"/><text class="cy-wnum" x="146" y="230" text-anchor="middle">9</text><rect class="cy-w6" x="158.5" y="214.5" width="23" height="23"/><text class="cy-wnum" x="170" y="230" text-anchor="middle">10</text><rect class="cy-w6" x="182.5" y="214.5" width="23" height="23"/><text class="cy-wnum" x="194" y="230" text-anchor="middle">11</text><rect class="cy-w6" x="206.5" y="214.5" width="23" height="23"/><text class="cy-wnum" x="218" y="230" text-anchor="middle">12</text><rect class="cy-target" x="111.5" y="23.5" width="21" height="21" rx="2"/><line class="cy-line" x1="12" y1="142" x2="232" y2="142"/></svg>

    <span class="viz-legend"><span><i class="cy-key-w"></i>מתחת לקו : כהה יותר, כבד יותר</span><span><i class="cy-key-target"></i>היעד</span><span><i class="cy-key-line"></i>הקו</span></span>

    <!-- /gen -->

    **מה קפיצה עושה לסכום.** שלוש משבצות רצופות \( a \), ‏\( b \), ‏\( c \) בשורה או בעמודה. אחרי
    הקפיצה \( a \) ו-\( b \) ריקות ו-\( c \) תפוסה, ולכן הסכום משתנה ב-\( \sigma^{d(c)} - \sigma^{d(a)} - \sigma^{d(b)} \).
    יש שלושה מקרים :

    - **לכיוון היעד :** ‏\( d(a) = k + 2 \), ‏\( d(b) = k + 1 \), ‏\( d(c) = k \). השינוי
      \( \sigma^{k}(1 - \sigma - \sigma^2) = 0 \).
    - **הרחק מהיעד :** ‏\( d(a) = k \), ‏\( d(b) = k + 1 \), ‏\( d(c) = k + 2 \). השינוי
      \( \sigma^{k}(\sigma^2 - 1 - \sigma) = -2\sigma^{k+1} < 0 \).
    - **מעל העמודה או השורה של היעד :** ‏\( b \) קרובה יותר מ-\( a \) ומ-\( c \), שבאותו מרחק
      \( k \). השינוי \( -\sigma^{k-1} < 0 \).

    **כל חצי המישור.** נסמן ב-\( S \) את סכום המשקלים של כל המשבצות \( y \le 0 \). בשורה \( y \)
    המשקלים הם \( \sigma^{5-y} \) כפול \( 1 + 2\sigma + 2\sigma^2 + \cdots \), וסכום השורות הוא טור
    הנדסי. בעזרת \( 1 - \sigma = \sigma^2 \) הכול יוצא בדיוק 1 :

    \[
    \begin{aligned}
    S &= \sigma^{5} \cdot \frac{1}{1 - \sigma} \cdot \Big(1 + \frac{2\sigma}{1 - \sigma}\Big) \\
      &= \sigma^{5} \cdot \frac{1}{\sigma^{2}} \cdot \Big(1 + \frac{2}{\sigma}\Big) \\
      &= \sigma^{3} + 2\sigma^{2} = 1
    \end{aligned}
    \]

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏σ :** הפתרון החיובי של \( \sigma^2 + \sigma = 1 \), ‏\( \sigma = (\sqrt5 - 1)/2 \approx 0.618 \).
    2. **פוטנציאל :** סכום \( \sigma^{d} \) על כל החיילים. חייל ביעד לבד נותן 1.
    3. **קפיצה :** משאירה את הפוטנציאל או מקטינה אותו, לפי שלושת המקרים.
    4. **ההתחלה :** צבא סופי מתחת לקו שוקל פחות מכל חצי המישור, שהוא בדיוק 1.
    5. **סתירה :** הפוטנציאל מתחיל מתחת ל-1, לא עולה, ולכן לעולם לא יגיע ל-1.

    </div>

    #### הקוד { .sol-code }

    מספרים מהצורה \( a + b\sqrt5 \) עם \( a \), ‏\( b \) רציונליים : חיבור, כפל, חילוק והשוואה
    מדויקים, בלי שגיאת עיגול. הסכום של חצי המישור יוצא 1 בדיוק, ולא 0.9999999.

    === "Python"
        ```python title="potential" linenums="1" hl_lines="20 24 25 29 30 31 32 33 34 55 60 69 70 71"
        from fractions import Fraction


        class Q5:
            """a + b√5 with rational a and b: exact arithmetic with σ = (√5 − 1)/2."""

            def __init__(self, a, b=0):
                self.a, self.b = Fraction(a), Fraction(b)

            @staticmethod
            def of(x):
                return x if isinstance(x, Q5) else Q5(x)

            def __add__(self, o):
                o = Q5.of(o)
                return Q5(self.a + o.a, self.b + o.b)

            def __mul__(self, o):
                o = Q5.of(o)
                return Q5(self.a * o.a + 5 * self.b * o.b, self.a * o.b + self.b * o.a)

            def __truediv__(self, o):
                o = Q5.of(o)
                d = o.a * o.a - 5 * o.b * o.b                                      # (1)!
                return self * Q5(o.a / d, -o.b / d)

            def sign(self) -> int:
                """The sign of a + b√5, exactly: compare a² with 5b² when the signs differ."""
                sa, sb = (self.a > 0) - (self.a < 0), (self.b > 0) - (self.b < 0)
                if sa == sb or sb == 0:
                    return sa
                if sa == 0:
                    return sb
                return sa if self.a * self.a > 5 * self.b * self.b else sb

            def __neg__(self): return Q5(-self.a, -self.b)
            def __sub__(self, o): return self + -Q5.of(o)
            def __rsub__(self, o): return Q5.of(o) - self
            def __rtruediv__(self, o): return Q5.of(o) / self
            __radd__, __rmul__ = __add__, __mul__
            def __eq__(self, o): return (self - o).sign() == 0
            def __lt__(self, o): return (self - o).sign() < 0
            def __le__(self, o): return (self - o).sign() <= 0
            def __gt__(self, o): return (self - o).sign() > 0
            def __ge__(self, o): return (self - o).sign() >= 0
            def __float__(self): return float(self.a) + float(self.b) * 5 ** 0.5

            def __pow__(self, k: int):
                r, x = Q5(1), self if k >= 0 else Q5(1) / self
                for _ in range(abs(k)):
                    r = r * x
                return r


        SIGMA = Q5(Fraction(-1, 2), Fraction(1, 2))                                # (2)!


        def weight(cell, n: int) -> Q5:
            """σ to the power of the distance from cell to the target (0, n)."""
            return SIGMA ** (abs(cell[0]) + abs(n - cell[1]))


        def potential(army, n: int) -> Q5:
            return sum((weight(c, n) for c in army), Q5(0))


        def half_plane(n: int) -> Q5:
            """The weight of every cell y <= 0 together, in closed form."""
            rows = 1 / (1 - SIGMA)                                                 # (3)!
            row = 1 + 2 * SIGMA / (1 - SIGMA)                                      # (4)!
            return SIGMA ** n * rows * row
        ```

        1. ‏\( 1/(a + b\sqrt5) = (a - b\sqrt5)/(a^2 - 5b^2) \), והמכנה אף פעם לא 0, כי \( \sqrt5 \) לא
           רציונלי.
        2. ‏\( \sigma = -\tfrac12 + \tfrac12\sqrt5 \).
        3. ‏\( 1 + \sigma + \sigma^2 + \cdots \) : השורות 0, ‏\( -1 \), ‏\( -2 \) וכן הלאה, כל אחת
           רחוקה ב-1 יותר.
        4. שורה אחת : העמודה \( x = 0 \), ועוד פעמיים \( \sigma + \sigma^2 + \cdots \) לשני הצדדים.

    #### למה זה נכון { .sol-proof }

    נניח שצבא סופי \( A \) מתחת לקו מביא חייל ל-\( (0, 5) \). נסמן ב-\( P \) את הפוטנציאל ביחס
    ל-\( (0, 5) \) :

    1. **בסוף :** יש חייל ביעד, ולכן \( P \ge \sigma^{0} = 1 \).
    2. **בדרך :** כל קפיצה משאירה את \( P \) או מקטינה אותו, לפי שלושת המקרים. ולכן \( P \) בסוף
       לא גדול מ-\( P(A) \).
    3. **בהתחלה :** ‏\( A \) סופי, ולכן יש משבצת מתחת לקו בלי חייל, ומשקלה חיובי. לכן
       \( P(A) \) קטן ממש מהמשקל של כל חצי המישור, שהוא 1.

    יוצא \( 1 \le P_{\text{end}} \le P(A) < 1 \), סתירה. אותו חישוב לשורה \( n \) נותן חצי מישור
    במשקל \( \sigma^{n-5} \), שגדול מ-1 כש-\( n \le 4 \) : שם הטיעון לא אוסר כלום, ובאמת מגיעים.
    המספרים ל-\( n = 1 \) עד 5, ומה הפוטנציאל אומר על מספר החיילים :

    <!-- gen 7 -->

    | שורה | המשקל של כל חצי המישור | הפוטנציאל אומר : לפחות | הכי מעט חיילים |
    |:-:|:-:|:-:|:-:|
    | ‏1 | ‏\( \varphi^{4} \approx 6.854 \) | ‏2 | ‏2 |
    | ‏2 | ‏\( \varphi^{3} \approx 4.236 \) | ‏4 | ‏4 |
    | ‏3 | ‏\( \varphi^{2} \approx 2.618 \) | ‏8 | ‏8 |
    | ‏4 | ‏\( \varphi \approx 1.618 \) | ‏19 | ‏20 |
    | ‏5 | ‏\( 1 \) | אי אפשר | אי אפשר |

    <!-- /gen -->

    העמודה "הפוטנציאל אומר" היא ה-\( k \) הקטן ביותר שבו \( k \) המשבצות הכבדות ביותר שוקלות
    לפחות 1. בשורות 1 עד 3 החסם הזה כבר שווה לפתרון של סעיף א, ולכן הוא מוכיח שאי אפשר בפחות.
    בשורה 4 החסם 19, ועשרים הוא המינימום הידוע.

    **נסו בעצמכם.** בשורה 5 המד לא מגיע ל-1. הציבו חיילים, הרבה ככל שתרצו, וראו כמה קרוב אפשר
    להגיע :

    <div class="explorer" data-kind="soldiers" data-row="5"></div>

    #### סיבוכיות { .sol-cost }

    הפוטנציאל של \( k \) חיילים הוא \( k \) חזקות של \( \sigma \), כל אחת עד המרחק הגדול ביותר,
    והכול בשברים מדויקים. הסכום של חצי המישור הוא נוסחה סגורה, בלי לולאה בכלל.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : סכום אינסופי שווה 1, אז אפשר"
    הסכום של כל חצי המישור הוא בדיוק 1, אבל הצבא סופי ותמיד חסרה משבצת, ולכן הוא קטן ממש מ-1.
    גם צבא אינסופי לא עוזר : מספר סופי של קפיצות משתמש רק במספר סופי של חיילים.

??? trap "מלכודת : מרחק אוקלידי"
    עם \( \sigma \) בחזקת המרחק האוקלידי, קפיצה לכיוון היעד לא שומרת על הסכום. המרחק הנכון
    הוא מספר הצעדים, \( |x| + |5 - y| \), כי הקפיצות הן רק בשורה ובעמודה.

??? trap "מלכודת : לחפש קדימה מההצבה"
    קדימה צריך לנחש גם איפה להציב את 20 החיילים וגם באיזה סדר לקפוץ, ובכל צעד יש עשרות קפיצות.
    אחורה מתחילים מחייל אחד, והגיזומים זורקים כמעט כל ענף.

??? trap "מלכודת : הגיזום של המחיר בלי הוכחה"
    "חייל בשורה 3 עולה 8" נכון רק כי החיילים שבונים חיילים שונים זרים, וכל אחד יכול להיבנות
    לבד. בלי הטיעון הזה הגיזום יכול לזרוק פתרון.

??? followup "שאלות המשך"
    - **על קו אחד :** החיילים על הישר, ב-\( x \le 0 \), וקופצים רק ימינה ושמאלה. כמה רחוק מגיעים?

        ??? fu-answer "תשובה"
            ל-\( x = 1 \) בלבד, בשני חיילים. כדי להגיע ל-\( x = 2 \) צריך חיילים ב-0 וב-1 בו בזמן, והפוטנציאל
            ביחס ל-\( x = 2 \) של כל הקרן \( x \le 0 \) הוא \( \sigma^2/(1 - \sigma) = 1 \) בדיוק,
            ולכן צבא סופי לא מגיע.

    - **למה 19 לא נפסל :** הפוטנציאל אומר שצריך לפחות 19 חיילים לשורה 4. למה לא 19?

        ??? fu-answer "תשובה"
            ‏19 המשבצות הכבדות ביותר שוקלות בדיוק 1. אז 19 חיילים יצטרכו לעמוד בדיוק עליהן, וכל
            קפיצה תצטרך להיות ישר לכיוון היעד, בלי אף איבוד. חיפוש ממצה מראה שזה לא מסתדר, ו-20 הוא
            המינימום. הפוטנציאל לבדו לא מספיק כדי להוכיח את זה.

    - **קפיצות באלכסון :** אם מותר לקפוץ גם באלכסון, האם ההוכחה של סעיף ג עדיין עובדת?

        ??? fu-answer "תשובה"
            לא. קפיצה באלכסון לכיוון היעד מקטינה את המרחק ב-2 בכל צעד, והשינוי בסכום הוא
            \( \sigma^{k}(1 - \sigma^2 - \sigma^4) > 0 \) : הפוטנציאל עולה, והטיעון נשבר. צריך
            משקלים אחרים.

    - **כמה מהר החיפוש :** למה הגיזום של הפוטנציאל כל כך חזק בשורה 4?

        ??? fu-answer "תשובה"
            הסכום של 20 המשבצות הכבדות הוא \( 1 + \sigma^8 \approx 1.0213 \), ומהיעד מתחילים ב-1.
            כל ביטול של קפיצה שלא לכיוון היעד מוסיף לפחות \( 2\sigma^{k+1} \) או \( \sigma^{k-1} \),
            ולכן כמעט כל ביטול כזה עובר את התקרה מיד.
