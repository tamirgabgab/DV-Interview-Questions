---
id: 80
title: לאיזה כיס ייכנס הכדור – שולחן ביליארד, כיסים ברוחב w וכל נקודת התחלה
level: senior
difficulty: hard
kind: math
tags: [geometry, number-theory, math, algorithms, python]
source: "שאלת ראיון בגאומטריה ובתורת המספרים, על שולחן סנוקר במידות מעוגלות"
added: 2026-11-04
---

## השאלה

שולחן ביליארד הוא מלבן באורך \( a \) לאורך ציר \( x \) וברוחב \( b \) לאורך ציר \( y \),
והפינה השמאלית התחתונה שלו בראשית \( (0, 0) \). בכל השאלה זה שולחן סנוקר במידות מעוגלות :
\( a = 360 \) ס"מ ו-\( b = 180 \) ס"מ (שולחן תקני הוא בערך 357 על 178 ס"מ).

כדור יוצא בקו ישר בזווית \( \alpha \) מעל ציר \( x \), כאשר \( 0 < \alpha < 90^\circ \). כשהוא
פוגע בדופן הוא מוחזר כמו קרן אור : זווית הפגיעה שווה לזווית ההחזרה. אין חיכוך, והכדור ממשיך
עד שהוא נכנס לכיס.

<!-- gen 0 -->

<svg class="figure" viewBox="0 0 714 368" style="max-width:30rem" role="img" aria-label="שולחן ביליארד של 360 על 180 ס״מ. הפינה השמאלית התחתונה בראשית (0, 0), ציר x לאורך השולחן וציר y לרוחבו. הכדור יוצא מהראשית בזווית α מעל ציר x, והכיסים בארבע הפינות"><rect class="bil-felt" x="109.2" y="30.4" width="576.0" height="288.0"></rect><circle class="bil-pocket" cx="109.2" cy="318.4" r="5.0"><title>הפינה השמאלית התחתונה (0, 0)</title></circle><circle class="bil-pocket" cx="685.2" cy="318.4" r="5.0"><title>הפינה הימנית התחתונה (360, 0)</title></circle><circle class="bil-pocket" cx="109.2" cy="30.4" r="5.0"><title>הפינה השמאלית העליונה (0, 180)</title></circle><circle class="bil-pocket" cx="685.2" cy="30.4" r="5.0"><title>הפינה הימנית העליונה (360, 180)</title></circle><line class="ink-line" x1="109.2" y1="318.4" x2="221.2" y2="318.4" stroke-width="1.2" stroke-dasharray="4 3"/><line class="bil-path" x1="109.2" y1="318.4" x2="262.8" y2="203.2" stroke-width="3"/><path class="ink-line" d="M 182.8 318.4 A 73.6 73.6 0 0 0 168.1 274.2" fill="none" stroke-width="1.2"/><text class="legend" x="198.8" y="299.2" text-anchor="middle" style="font-size:17px">α</text><circle class="ink-dot" cx="109.2" cy="318.4" r="6"><title>הכדור בראשית (0, 0)</title></circle><text class="legend" x="397.2" y="340.8" text-anchor="middle" style="font-size:15px">a = 360</text><text class="legend" x="86.8" y="174.4" text-anchor="end" style="font-size:15px">b = 180</text><text class="legend" x="109.2" y="340.8" text-anchor="middle" style="font-size:13px">(0, 0)</text><text class="legend" x="685.2" y="18.0" text-anchor="end" style="font-size:13px">(360, 180)</text></svg>

<!-- /gen -->

??? interviewer "מה המראיין בודק"
    - **מעקב שיטתי :** בסעיף הראשון מספיק לעקוב אחרי הכדור ביד. המראיין בודק דיוק, ושהמועמד
      לא מתבלבל בכיוון אחרי כל פגיעה.
    - **הרעיון שמפשט הכול :** האם המועמד מגיע, לבד או עם רמז, לכך שאפשר לשקף את השולחן במקום
      את הכדור, ושאז המסלול הוא קו ישר?
    - **תורת המספרים :** מקו ישר ונקודות של רשת מגיעים לשבר מצומצם, לזוגיות ולקירוב של מספר
      בשברים.
    - **הוכחה, לא רק נוסחה :** למה שתי פינות בלתי אפשריות, ולמה הכדור תמיד נכנס לכיס כשיש
      לכיסים רוחב.
    - **ביקורת על ההנחות :** בסעיף האחרון התוצאה משתנה כשמזיזים את נקודת ההתחלה. המראיין בודק
      שהמועמד מבין מאיפה הגיעה התוצאה הקודמת.
    - **לפי רמה :** אפשר לעצור אחרי כל סעיף. סעיף א מתאים לכל מועמד, וסעיפים ג ו-ד מבדילים בין
      המועמדים החזקים.

---

### סעיף א – מכה אחת, ביד { #by-hand }

הכיסים הם נקודות בארבע הפינות בלבד. הכדור יוצא מ-\( (0, 0) \), ומכוונים אותו לנקודה
\( (240, 180) \) על הדופן העליונה, כלומר \( \tan\alpha = 180/240 = 3/4 \).

1. לאיזה כיס ייכנס הכדור?
2. כמה פעמים הוא יפגע בדפנות לפני כן?

??? tip "רמז 1"
    עקבו אחרי הכדור מקטע אחרי מקטע. על כל 4 ס"מ לאורך השולחן הכדור עובר 3 ס"מ לרוחבו, ובכל
    פגיעה מתהפך רק כיוון אחד.

??? tip "רמז 2"
    פגיעה בדופן העליונה או התחתונה הופכת את הכיוון ב-\( y \), ופגיעה בדופן הימנית או השמאלית
    את הכיוון ב-\( x \). מ-\( (0, 0) \) עד הדופן העליונה הכדור עולה 180 ס"מ, ולכן זז 240 ימינה.

??? tip "רמז 3"
    אחרי שלוש פגיעות הכדור ב-\( (240, 0) \) ונע שמאלה ולמעלה. כמה הוא עולה עד שהוא מגיע
    ל-\( x = 0 \)?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        הכדור נכנס לכיס השמאלי העליון \( (0, 180) \) אחרי 3 פגיעות : בדופן העליונה, בימנית
        ובתחתונה. המסלול באורך 900 ס"מ.

    #### הרעיון { .sol-idea }

    עוקבים אחרי הכדור. כל מקטע הוא קו בשיפוע \( 3/4 \) או \( -3/4 \), ובכל פגיעה מתהפך סימן
    אחד : למעלה הופך ללמטה, או ימינה לשמאלה.

    <!-- gen 1 -->

    <svg class="figure" viewBox="0 0 643 355" style="max-width:30rem" role="img" aria-label="סעיף א : הכדור יוצא מ-(0, 0) לכיוון (240, 180). הוא פוגע בדופן העליונה ב-(240, 180), בימנית ב-(360, 90) ובתחתונה ב-(240, 0), ונכנס לכיס השמאלי העליון (0, 180) : שלוש פגיעות"><rect class="bil-felt" x="33.6" y="33.4" width="576.0" height="288.0"></rect><circle class="bil-pocket" cx="33.6" cy="321.4" r="5.0"><title>הפינה השמאלית התחתונה (0, 0)</title></circle><circle class="bil-pocket" cx="609.6" cy="321.4" r="5.0"><title>הפינה הימנית התחתונה (360, 0)</title></circle><circle class="bil-pocket is-in" cx="33.6" cy="33.4" r="5.0"><title>הפינה השמאלית העליונה (0, 180)</title></circle><circle class="bil-pocket" cx="609.6" cy="33.4" r="5.0"><title>הפינה הימנית העליונה (360, 180)</title></circle><line class="bil-path" x1="33.6" y1="321.4" x2="417.6" y2="33.4" stroke-width="3"/><line class="bil-path" x1="417.6" y1="33.4" x2="609.6" y2="177.4" stroke-width="3"/><line class="bil-path" x1="609.6" y1="177.4" x2="417.6" y2="321.4" stroke-width="3"/><line class="bil-path" x1="417.6" y1="321.4" x2="33.6" y2="33.4" stroke-width="3"/><circle class="s1-dot" cx="417.6" cy="33.4" r="5"><title>פגיעה 1 בדופן (240, 180)</title></circle><text class="legend" x="417.6" y="23.4" text-anchor="middle" style="font-size:15px">1</text><circle class="s1-dot" cx="609.6" cy="177.4" r="5"><title>פגיעה 2 בדופן (360, 90)</title></circle><text class="legend" x="597.6" y="177.4" text-anchor="middle" style="font-size:15px">2</text><circle class="s1-dot" cx="417.6" cy="321.4" r="5"><title>פגיעה 3 בדופן (240, 0)</title></circle><text class="legend" x="417.6" y="341.4" text-anchor="middle" style="font-size:15px">3</text><circle class="ink-dot" cx="33.6" cy="321.4" r="6"><title>הכדור יוצא מ-(0, 0)</title></circle></svg>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="ink"></i>נקודת היציאה</span><span><i class="bil-path"></i>המסלול</span><span><i class="s1"></i>פגיעה בדופן, לפי הסדר</span><span><i class="bil-key-in"></i>הכיס שהכדור נכנס אליו</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **למעלה וימינה :** מ-\( (0, 0) \) עד \( y = 180 \) הכדור זז \( 180 \cdot 4/3 = 240 \)
       ימינה, ופוגע בדופן העליונה ב-\( (240, 180) \).

    2. **למטה וימינה :** עד \( x = 360 \) נשארו 120 ס"מ, כלומר 90 ס"מ למטה. הכדור פוגע בדופן
       הימנית ב-\( (360, 90) \).

    3. **למטה ושמאלה :** 90 ס"מ למטה הם 120 ס"מ שמאלה. הכדור פוגע בדופן התחתונה
       ב-\( (240, 0) \).

    4. **למעלה ושמאלה :** עד \( x = 0 \) נשארו 240 ס"מ, כלומר 180 ס"מ למעלה. הכדור מגיע
       ל-\( (0, 180) \), פינה, ונכנס לכיס.

    </div>

    <!-- gen 3 -->

    | מקטע | מנקודה | לנקודה | מה קורה שם |
    |:-:|:-:|:-:|:-:|
    | 1 | <span dir="ltr">(0, 0)</span> | <span dir="ltr">(240, 180)</span> | פגיעה בדופן העליונה |
    | 2 | <span dir="ltr">(240, 180)</span> | <span dir="ltr">(360, 90)</span> | פגיעה בדופן הימנית |
    | 3 | <span dir="ltr">(360, 90)</span> | <span dir="ltr">(240, 0)</span> | פגיעה בדופן התחתונה |
    | 4 | <span dir="ltr">(240, 0)</span> | <span dir="ltr">(0, 180)</span> | **כניסה לכיס <span dir="ltr">(0, 180)</span>** |

    <!-- /gen -->

    #### למה זה נכון { .sol-proof }

    **האורך.** בכל מקטע הכדור עובר \( 5/4 \) מהתזוזה שלו לאורך השולחן, כי
    \( \sqrt{4^2 + 3^2} = 5 \). התזוזות לאורך השולחן הן 240, 120, 120 ו-240, יחד 720 ס"מ, ולכן
    המסלול \( 720 \cdot 5/4 = 900 \) ס"מ.

    **רמז לסעיף הבא.** יחד הכדור זז \( 720 = 2a \) לאורך ו-\( 540 = 3b \) לרוחב, כפולה שלמה
    של \( a \) וכפולה שלמה של \( b \). כך בכל מכה שנכנסת לפינה : בסך הכול הכדור זז \( pa \)
    לאורך ו-\( qb \) לרוחב, עם \( p \) ו-\( q \) שלמים (כאן 2 ו-3, ובמכות אחרות מספרים אחרים),
    וזה בדיוק מה שסעיף ב מנצל.

---

### סעיף ב – כל זווית, כיסים נקודתיים { #point-pockets }

עכשיו \( \alpha \) היא זווית כלשהי בין 0 ל-\( 90^\circ \). הכיסים עדיין נקודות בארבע הפינות
בלבד, והכדור עדיין יוצא מ-\( (0, 0) \).

1. לאיזה כיס ייכנס הכדור?
2. כמה פגיעות בדפנות יהיו?
3. האם הכדור תמיד ייכנס לכיס? למשל במכה של \( 37^\circ \)?

??? tip "רמז 1"
    במקום לשקף את הכדור בכל פגיעה, שקפו את השולחן.

??? tip "רמז 2"
    אחרי כל השיקופים העותקים של השולחן מרצפים את המישור, והכדור נע על הישר
    \( y = x\tan\alpha \). הפינות של כל העותקים הן הנקודות \( (pa, qb) \). מתי הישר עובר
    דרך אחת מהן?

??? tip "רמז 3"
    בסעיף א הישר הגיע ל-\( (720, 540) = (2a, 3b) \). איך הזוגיות של 2 ושל 3 קובעת שזו הפינה
    \( (0, b) \)?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        נגדיר \( r = a\tan\alpha / b \), ובשולחן שלנו \( r = 2\tan\alpha \). הכדור נכנס לכיס
        רק כש-\( r \) רציונלי. אם \( r = q/p \) כשבר מצומצם, הכיס הוא \( x = a \) כש-\( p \)
        אי־זוגי ו-\( x = 0 \) כש-\( p \) זוגי, \( y = b \) כש-\( q \) אי־זוגי ו-\( y = 0 \)
        כש-\( q \) זוגי, אחרי \( p + q - 2 \) פגיעות. ב-\( 37^\circ \) הכדור לא נכנס לעולם.

    #### הרעיון { .sol-idea }

    פותחים את השולחן : בכל פגיעה משקפים את השולחן מעבר לדופן, והכדור ממשיך ישר אל העותק. כך
    המסלול השבור של סעיף א הופך לקו ישר מ-\( (0, 0) \) ל-\( (720, 540) \), וכל פגיעה בדופן
    היא חצייה של קו ברשת העותקים :

    <!-- gen 4 -->

    <svg class="figure" viewBox="0 0 608 460" style="max-width:30rem" role="img" aria-label="סעיף א אחרי פתיחת השולחן : שישה עותקים של השולחן, שתי עמודות ושלוש שורות. הקו הישר מ-(0, 0) ל-(720, 540) חוצה קו אנכי אחד ושני קווים אופקיים, שלוש הפגיעות, ומגיע לנקודת הרשת (720, 540), שהיא הפינה (0, 180) של השולחן האמיתי"><rect class="bil-felt" x="38.0" y="294.5" width="270.0" height="135.0"></rect><rect class="box-copy" x="38.0" y="159.5" width="270.0" height="135.0"></rect><rect class="box-copy" x="38.0" y="24.5" width="270.0" height="135.0"></rect><rect class="box-copy" x="308.0" y="294.5" width="270.0" height="135.0"></rect><rect class="box-copy" x="308.0" y="159.5" width="270.0" height="135.0"></rect><rect class="box-copy" x="308.0" y="24.5" width="270.0" height="135.0"></rect><circle class="bil-pocket" cx="38.0" cy="429.5" r="4"><title>(0, 0) : הפינה (0, 0)</title></circle><text class="legend" x="43.0" y="443.5" text-anchor="start" style="font-size:12px">(0, 0)</text><circle class="bil-pocket" cx="38.0" cy="294.5" r="4"><title>(0, 180) : הפינה (0, 180)</title></circle><text class="legend" x="43.0" y="288.5" text-anchor="start" style="font-size:12px">(0, 180)</text><circle class="bil-pocket" cx="38.0" cy="159.5" r="4"><title>(0, 360) : הפינה (0, 0)</title></circle><text class="legend" x="43.0" y="153.5" text-anchor="start" style="font-size:12px">(0, 0)</text><circle class="bil-pocket" cx="38.0" cy="24.5" r="4"><title>(0, 540) : הפינה (0, 180)</title></circle><text class="legend" x="43.0" y="18.5" text-anchor="start" style="font-size:12px">(0, 180)</text><circle class="bil-pocket" cx="308.0" cy="429.5" r="4"><title>(360, 0) : הפינה (360, 0)</title></circle><text class="legend" x="313.0" y="443.5" text-anchor="start" style="font-size:12px">(360, 0)</text><circle class="bil-pocket" cx="308.0" cy="294.5" r="4"><title>(360, 180) : הפינה (360, 180)</title></circle><text class="legend" x="313.0" y="288.5" text-anchor="start" style="font-size:12px">(360, 180)</text><circle class="bil-pocket" cx="308.0" cy="159.5" r="4"><title>(360, 360) : הפינה (360, 0)</title></circle><text class="legend" x="313.0" y="153.5" text-anchor="start" style="font-size:12px">(360, 0)</text><circle class="bil-pocket" cx="308.0" cy="24.5" r="4"><title>(360, 540) : הפינה (360, 180)</title></circle><text class="legend" x="313.0" y="18.5" text-anchor="start" style="font-size:12px">(360, 180)</text><circle class="bil-pocket" cx="578.0" cy="429.5" r="4"><title>(720, 0) : הפינה (0, 0)</title></circle><text class="legend" x="573.0" y="443.5" text-anchor="end" style="font-size:12px">(0, 0)</text><circle class="bil-pocket" cx="578.0" cy="294.5" r="4"><title>(720, 180) : הפינה (0, 180)</title></circle><text class="legend" x="573.0" y="288.5" text-anchor="end" style="font-size:12px">(0, 180)</text><circle class="bil-pocket" cx="578.0" cy="159.5" r="4"><title>(720, 360) : הפינה (0, 0)</title></circle><text class="legend" x="573.0" y="153.5" text-anchor="end" style="font-size:12px">(0, 0)</text><circle class="bil-pocket is-in" cx="578.0" cy="24.5" r="4"><title>(720, 540) : הפינה (0, 180)</title></circle><text class="legend" x="573.0" y="18.5" text-anchor="end" style="font-size:12px">(0, 180)</text><line class="bil-path" x1="38.0" y1="429.5" x2="578.0" y2="24.5" stroke-width="3"/><circle class="s1-dot" cx="218.0" cy="294.5" r="5"><title>חצייה 1 : פגיעה בדופן</title></circle><text class="legend" x="230.0" y="298.5" text-anchor="middle" style="font-size:14px">1</text><circle class="s1-dot" cx="308.0" cy="227.0" r="5"><title>חצייה 2 : פגיעה בדופן</title></circle><text class="legend" x="320.0" y="231.0" text-anchor="middle" style="font-size:14px">2</text><circle class="s1-dot" cx="398.0" cy="159.5" r="5"><title>חצייה 3 : פגיעה בדופן</title></circle><text class="legend" x="410.0" y="163.5" text-anchor="middle" style="font-size:14px">3</text><circle class="ink-dot" cx="38.0" cy="429.5" r="5"><title>הכדור יוצא מ-(0, 0)</title></circle></svg>

    <!-- /gen -->

    <!-- gen 5 -->

    <span class="viz-legend"><span><i class="bil-key-felt"></i>השולחן עצמו</span><span><i class="box-copy"></i>העותקים המשוקפים</span><span><i class="bil-path"></i>המסלול, קו ישר</span><span><i class="s1"></i>חצייה של קו ברשת : פגיעה בדופן</span><span><i class="bil-key-pocket"></i>נקודת רשת : פינה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הישר :** אחרי הפתיחה הכדור נע על \( y = x\tan\alpha \) על פני כל העותקים.

    2. **הפינות :** הפינות של כל העותקים הן \( (pa, qb) \) עם \( p, q \) שלמים. הכדור נכנס
       לכיס כשהישר עובר דרך אחת מהן : \( qb = pa\tan\alpha \), כלומר \( r = q/p \).

    3. **הפינה הראשונה :** כל נקודות הרשת על הישר הן \( (pa, qb) \) עם \( q/p = r \), והכדור
       מגיע קודם לזו עם \( p \) הקטן ביותר : השבר המצומצם.

    4. **איזה כיס :** כל מעבר לעותק שכן הופך את הכיוון בציר שלו. לכן \( x = pa \) הוא
       \( x = a \) בשולחן האמיתי כש-\( p \) אי־זוגי ו-\( x = 0 \) כש-\( p \) זוגי, ובאותו אופן
       \( y \) לפי \( q \) :

        | ‏\( p \) | ‏\( q \) | הכיס |
        |:-:|:-:|:-:|
        | אי־זוגי | אי־זוגי | ‏\( (a, b) \), הפינה הנגדית |
        | אי־זוגי | זוגי | ‏\( (a, 0) \) |
        | זוגי | אי־זוגי | ‏\( (0, b) \) |
        | זוגי | זוגי | אי אפשר : השבר מצומצם |

    5. **כמה פגיעות :** בדרך ל-\( (pa, qb) \) הישר חוצה את הקווים \( x = a, \dots, (p-1)a \)
       ואת \( y = b, \dots, (q-1)b \), ולעולם לא שניים מהם באותה נקודה, כי זו הייתה נקודת רשת
       קודמת. כל חצייה היא פגיעה : \( (p - 1) + (q - 1) = p + q - 2 \).

    6. **‏\( r \) אי־רציונלי :** אין שלמים עם \( q/p = r \), הישר לא עובר באף פינה, והכדור לא
       נכנס לעולם. כך ב-\( 37^\circ \) : הערכים הרציונליים היחידים של \( \tan \) בזווית שלמה
       במעלות הם 0 ו-\( \pm 1 \), ולכן \( \tan 37^\circ \) אי־רציונלי.

    </div>

    כמה מכות על השולחן. "מכוונים ל-" היא הנקודה הראשונה שהכדור פוגע בה, או הכיס עצמו :

    <!-- gen 6 -->

    | מכוונים ל- | ‏\( \tan\alpha \) | ‏\( r = 2\tan\alpha \) | ‏\( p \) | ‏\( q \) | הכיס | פגיעות |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | <span dir="ltr">(360, 180)</span> | <span dir="ltr">1/2</span> | <span dir="ltr">1</span> | 1 | 1 | <span dir="ltr">(360, 180)</span> | 0 |
    | <span dir="ltr">(180, 180)</span> | <span dir="ltr">1</span> | <span dir="ltr">2</span> | 1 | 2 | <span dir="ltr">(360, 0)</span> | 1 |
    | <span dir="ltr">(240, 180)</span> | <span dir="ltr">3/4</span> | <span dir="ltr">3/2</span> | 2 | 3 | <span dir="ltr">(0, 180)</span> | 3 |
    | <span dir="ltr">(270, 180)</span> | <span dir="ltr">2/3</span> | <span dir="ltr">4/3</span> | 3 | 4 | <span dir="ltr">(360, 0)</span> | 5 |
    | <span dir="ltr">(360, 120)</span> | <span dir="ltr">1/3</span> | <span dir="ltr">2/3</span> | 3 | 2 | <span dir="ltr">(360, 0)</span> | 3 |
    | <span dir="ltr">(360, 150)</span> | <span dir="ltr">5/12</span> | <span dir="ltr">5/6</span> | 6 | 5 | <span dir="ltr">(0, 180)</span> | 9 |
    | ‏37° | <span dir="ltr">0.7536…</span> | <span dir="ltr">1.5071…</span> | – | – | אין | אינסוף |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="point_pocket" linenums="1" hl_lines="7 8 9"
        from fractions import Fraction


        def point_pocket(a, b, tan):
            """Point pockets at the corners, the ball from (0, 0) at slope tan (a Fraction):
            the pocket it enters and how many cushions it hits first."""
            r = Fraction(a) * tan / b             # (1)!
            p, q = r.denominator, r.numerator     # (2)!
            pocket = (a if p % 2 else 0, b if q % 2 else 0)
            return pocket, p + q - 2
        ```

        1. ‏\( r = a\tan\alpha / b \), שבר. ‏`Fraction` שומר אותו תמיד מצומצם.
        2. הכדור מגיע לנקודת הרשת \( (pa, qb) \). הזוגיות של \( p \) ושל \( q \) קובעת את הכיס.

    #### למה זה נכון { .sol-proof }

    **השיקוף שומר על המסלול.** כשמשקפים את השולחן מעבר לדופן, ההמשך הישר של הכדור בעותק הוא
    בדיוק ההחזרה שלו בשולחן האמיתי, משוקפת : זווית הפגיעה שווה לזווית ההחזרה.

    **הכדור לא חוזר לראשית.** \( p \) ו-\( q \) זרים, ולכן הם לא שניהם זוגיים : הפינה
    \( (0, 0) \) לא מופיעה בטבלה.

    **רק \( r \) חשוב.** \( a \), ‏\( b \) ו-\( \alpha \) לא צריכים להיות שלמים או רציונליים, הם
    קובעים רק את המספר \( r \). שולחן אחר עם אותו \( r \) נותן אותו כיס ואותו מספר פגיעות.

---

### סעיף ג – כיסים ברוחב w, וגם באמצע { #wide-pockets }

עכשיו השולחן דומה יותר לשולחן סנוקר אמיתי :

- לכל כיס יש רוחב \( w = 9 \) ס"מ. הכדור נכנס לכיס כשהוא עובר במרחק קטן מ-\( w/2 \) ממרכז
  הכיס.
- יש שני כיסים נוספים, באמצע הדופן התחתונה \( (180, 0) \) ובאמצע הדופן העליונה
  \( (180, 180) \), גם הם ברוחב \( w \).
- הכדור עדיין יוצא ממרכז הכיס \( (0, 0) \), ואת הכיס הזה מתעלמים.

לאיזה כיס ייכנס הכדור? חלקו למקרים לפי ששת הכיסים. האם הוא תמיד נכנס לכיס? ולאן תיכנס עכשיו
המכה של \( 37^\circ \)? (מניחים כיסים קטנים ביחס לשולחן : \( w < a/2 \) ו-\( w < b\cos\alpha \).)

??? tip "רמז 1"
    פתחו שוב את השולחן. איפה עומדים הכיסים האמצעיים ברשת?

??? tip "רמז 2"
    כל ששת הכיסים יושבים על קווים אנכיים כל \( a/2 \). כיס בפינה הוא רבע עיגול ברדיוס
    \( w/2 \), וכיס באמצע הוא חצי עיגול. מה הם אחרי הפתיחה?

??? tip "רמז 3"
    בקו האנכי ה-\( k \), ‏\( x = k \cdot a/2 \), הישר בגובה \( k \cdot (a/2) \tan\alpha \). כמה
    הוא רחוק מהכפולה הקרובה של \( b \), ומה המרחק הניצב מהנקודה?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        נגדיר \( s = \frac{a\tan\alpha}{2b} \) ו-\( \varepsilon = \frac{w}{2b\cos\alpha} \),
        ובשולחן שלנו \( s = \tan\alpha \). ‏\( K \) הוא ה-\( k \) הראשון עם
        \( \lVert k s \rVert < \varepsilon \), ו-\( m = \operatorname{round}(K s) \). ‏\( K \)
        אי־זוגי : כיס אמצעי, למטה כש-\( m \) זוגי ולמעלה כש-\( m \) אי־זוגי. ‏\( K \equiv 2 \pmod 4 \) :
        הפינה \( (a, b) \), ו-\( K \equiv 0 \pmod 4 \) : הפינה \( (0, b) \). לפינות \( (a, 0) \)
        ו-\( (0, 0) \) הכדור לא נכנס אף פעם, ולכיס כלשהו הוא נכנס תמיד. ב-\( 37^\circ \) :
        ‏\( K = 4 \), ‏\( m = 3 \), הפינה \( (0, 180) \).

    <!-- cost: צעדים \( K \le \lceil 1/\varepsilon \rceil \) | בשברים משולבים \( O(\log(1/\varepsilon)) \) -->

    #### הרעיון { .sol-idea }

    פותחים את השולחן כמו בסעיף ב, אבל עכשיו נקודות הרשת הן כל \( a/2 \) לרוחב : פינות וכיסים
    אמצעיים לסירוגין. כל כיס הוא עיגול ברדיוס \( w/2 \), והשאלה היא לאיזה עיגול הישר נכנס
    ראשון :

    <!-- gen 7 -->

    <svg class="figure" viewBox="0 0 593 451" style="max-width:30rem" role="img" aria-label="סעיף ג אחרי פתיחת השולחן : שישה עותקים, ונקודות הרשת כל 180 ס״מ לרוחב : פינות וכיסים אמצעיים לסירוגין, כל כיס עיגול ברדיוס 4.5 ס״מ. הקו של 37° עובר ליד שלוש נקודות רשת ונכנס לעיגול של (720, 540), הפינה (0, 180). הקו המקווקו, tan α = 2/3, נכנס כבר ב-(540, 360), הכיס האמצעי התחתון"><rect class="bil-felt" x="23.0" y="293.0" width="270.0" height="135.0"></rect><rect class="box-copy" x="23.0" y="158.0" width="270.0" height="135.0"></rect><rect class="box-copy" x="23.0" y="23.0" width="270.0" height="135.0"></rect><rect class="box-copy" x="293.0" y="293.0" width="270.0" height="135.0"></rect><rect class="box-copy" x="293.0" y="158.0" width="270.0" height="135.0"></rect><rect class="box-copy" x="293.0" y="23.0" width="270.0" height="135.0"></rect><circle class="bil-hole" cx="23.0" cy="428.0" r="3.38"><title>(0, 0) : הפינה השמאלית התחתונה (0, 0)</title></circle><circle class="bil-hole" cx="23.0" cy="293.0" r="3.38"><title>(0, 180) : הפינה השמאלית העליונה (0, 180)</title></circle><circle class="bil-hole" cx="23.0" cy="158.0" r="3.38"><title>(0, 360) : הפינה השמאלית התחתונה (0, 0)</title></circle><circle class="bil-hole" cx="23.0" cy="23.0" r="3.38"><title>(0, 540) : הפינה השמאלית העליונה (0, 180)</title></circle><line class="ink-line" x1="158.0" y1="428.0" x2="158.0" y2="23.0" stroke-width="0.8" stroke-dasharray="2 4"/><circle class="bil-hole" cx="158.0" cy="428.0" r="3.38"><title>(180, 0) : הכיס האמצעי התחתון (180, 0)</title></circle><circle class="bil-hole" cx="158.0" cy="293.0" r="3.38"><title>(180, 180) : הכיס האמצעי העליון (180, 180)</title></circle><circle class="bil-hole" cx="158.0" cy="158.0" r="3.38"><title>(180, 360) : הכיס האמצעי התחתון (180, 0)</title></circle><circle class="bil-hole" cx="158.0" cy="23.0" r="3.38"><title>(180, 540) : הכיס האמצעי העליון (180, 180)</title></circle><circle class="bil-hole" cx="293.0" cy="428.0" r="3.38"><title>(360, 0) : הפינה הימנית התחתונה (360, 0)</title></circle><circle class="bil-hole" cx="293.0" cy="293.0" r="3.38"><title>(360, 180) : הפינה הימנית העליונה (360, 180)</title></circle><circle class="bil-hole" cx="293.0" cy="158.0" r="3.38"><title>(360, 360) : הפינה הימנית התחתונה (360, 0)</title></circle><circle class="bil-hole" cx="293.0" cy="23.0" r="3.38"><title>(360, 540) : הפינה הימנית העליונה (360, 180)</title></circle><line class="ink-line" x1="428.0" y1="428.0" x2="428.0" y2="23.0" stroke-width="0.8" stroke-dasharray="2 4"/><circle class="bil-hole" cx="428.0" cy="428.0" r="3.38"><title>(540, 0) : הכיס האמצעי התחתון (180, 0)</title></circle><circle class="bil-hole" cx="428.0" cy="293.0" r="3.38"><title>(540, 180) : הכיס האמצעי העליון (180, 180)</title></circle><circle class="bil-hole is-in" cx="428.0" cy="158.0" r="3.38"><title>(540, 360) : הכיס האמצעי התחתון (180, 0)</title></circle><circle class="bil-hole" cx="428.0" cy="23.0" r="3.38"><title>(540, 540) : הכיס האמצעי העליון (180, 180)</title></circle><circle class="bil-hole" cx="563.0" cy="428.0" r="3.38"><title>(720, 0) : הפינה השמאלית התחתונה (0, 0)</title></circle><circle class="bil-hole" cx="563.0" cy="293.0" r="3.38"><title>(720, 180) : הפינה השמאלית העליונה (0, 180)</title></circle><circle class="bil-hole" cx="563.0" cy="158.0" r="3.38"><title>(720, 360) : הפינה השמאלית התחתונה (0, 0)</title></circle><circle class="bil-hole is-in" cx="563.0" cy="23.0" r="3.38"><title>(720, 540) : הפינה השמאלית העליונה (0, 180)</title></circle><line class="bil-path" x1="23.0" y1="428.0" x2="563.0" y2="21.1" stroke-width="2.5"/><line class="s2-line" x1="23.0" y1="428.0" x2="428.0" y2="158.0" stroke-width="2" stroke-dasharray="7 5"/><text class="legend" x="549.0" y="37.1" text-anchor="end" style="font-size:14px">37°</text><text class="legend" x="438.0" y="176.0" text-anchor="start" style="font-size:13px">tan α = 2/3</text><circle class="ink-dot" cx="23.0" cy="428.0" r="5"><title>הכדור יוצא מ-(0, 0)</title></circle></svg>

    <!-- /gen -->

    <!-- gen 8 -->

    <span class="viz-legend"><span><i class="bil-key-felt"></i>השולחן עצמו</span><span><i class="box-copy"></i>העותקים</span><span><i class="bil-key-hole"></i>כיס, ברדיוס 4.5 ס״מ</span><span><i class="bil-path"></i>‏37° : נכנס ל-<span dir="ltr">(0, 180)</span></span><span><i class="bil-key-dash"></i>‏tan α = 2/3 : נכנס לאמצעי התחתון</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הרשת :** כל הכיסים, בכל העותקים, הם הנקודות
       \( P_{k,m} = \left(k \cdot \tfrac a2,\ m \cdot b\right) \). ‏\( k \) זוגי : פינות.
       ‏\( k \) אי־זוגי : כיסים אמצעיים.

    2. **כיס הופך לעיגול :** בשולחן האמיתי כיס בפינה הוא רבע עיגול ברדיוס \( w/2 \), וכיס
       באמצע הוא חצי עיגול. אחרי הפתיחה ארבעה רבעים, או שני חצאים, משלימים עיגול שלם סביב
       נקודת הרשת. לכן התנאי לכניסה זהה לכל ששת הכיסים.

    3. **המרחק בקו ה-\( k \) :** הישר עובר ב-\( x = k \cdot a/2 \) בגובה
       \( k \frac a2 \tan\alpha = k s \cdot b \). הכפולה הקרובה של \( b \) היא \( m b \) עם
       \( m = \operatorname{round}(k s) \), והפער האנכי \( \lVert k s \rVert \, b \), כאשר
       \( \lVert x \rVert \) הוא המרחק של \( x \) מהשלם הקרוב, למשל
       \( \lVert 5.67 \rVert = 0.33 \). המרחק הניצב קטן פי \( \cos\alpha \) :

        \[
        \lVert k s \rVert \, b \cos\alpha < \frac w2
        \iff \lVert k s \rVert < \varepsilon
        \]

    4. **הכיס הראשון :** ‏\( K \) הוא ה-\( k \) הראשון שמקיים את התנאי. העיגולים של קווים
       שונים לא נוגעים זה בזה כי \( w < a/2 \), ובכל קו לכל היותר עיגול אחד קרוב מספיק כי
       \( w < b\cos\alpha \). הכיס האמיתי : שני שיקופים באותו ציר מחזירים את השולחן למצבו, ולכן
       העותקים חוזרים על עצמם כל \( 2a \) לאורך, כלומר כל ארבעה קווים. במחזור אחד הקווים
       \( K \equiv 0, 1, 2, 3 \pmod 4 \) הם \( x = 0 \), ‏\( a/2 \), ‏\( a \) ושוב \( a/2 \) (האמצע
       של העותק המשוקף), ו-\( y \) לפי הזוגיות של \( m \), כמו בסעיף ב.

    5. **ששת המקרים :**

        <!-- gen 9 -->

        | הכיס | נכנס כאשר | כיסים נקודתיים, \( s = q/p \) מצומצם | דוגמה : מכוונים ל- | ‏\( K, m \) ב-\( w = 9 \) |
        |:-:|:-:|:-:|:-:|:-:|
        | הכיס האמצעי התחתון <span dir="ltr">(180, 0)</span> | ‏\( K \) אי־זוגי, \( m \) זוגי | ‏\( p \) אי־זוגי, \( q \) זוגי | <span dir="ltr">(270, 180)</span> | <span dir="ltr">3, 2</span> |
        | הכיס האמצעי העליון <span dir="ltr">(180, 180)</span> | ‏\( K \) אי־זוגי, \( m \) אי־זוגי | ‏\( p \) אי־זוגי, \( q \) אי־זוגי | <span dir="ltr">(180, 180)</span> | <span dir="ltr">1, 1</span> |
        | הפינה הימנית העליונה <span dir="ltr">(360, 180)</span> | ‏\( K \equiv 2 \pmod 4 \) | ‏\( p \equiv 2 \pmod 4 \) | <span dir="ltr">(360, 180)</span> | <span dir="ltr">2, 1</span> |
        | הפינה השמאלית העליונה <span dir="ltr">(0, 180)</span> | ‏\( K \equiv 0 \pmod 4 \) | ‏\( p \equiv 0 \pmod 4 \) | <span dir="ltr">(240, 180)</span> | <span dir="ltr">4, 3</span> |
        | הפינה הימנית התחתונה <span dir="ltr">(360, 0)</span> | **אף פעם** | **אף פעם** | – | – |
        | הפינה השמאלית התחתונה <span dir="ltr">(0, 0)</span> | **אף פעם** | **אף פעם** | – | – |

        <!-- /gen -->

    6. **‏\( 37^\circ \) :** ‏\( s = \tan 37^\circ \approx 0.7536 \) ו-
       \( \varepsilon = 9/(360 \cos 37^\circ) \approx 0.0313 \) :

        <!-- gen 10 -->

        | ‏\( k \) | ‏\( k s \) | ‏\( \lVert k s \rVert \) | קטן מ-\( \varepsilon \approx 0.0313 \)? |
        |:-:|:-:|:-:|:-:|
        | 1 | <span dir="ltr">0.7536</span> | <span dir="ltr">0.2464</span> | לא |
        | 2 | <span dir="ltr">1.5071</span> | <span dir="ltr">0.4929</span> | לא |
        | 3 | <span dir="ltr">2.2607</span> | <span dir="ltr">0.2607</span> | לא |
        | 4 | <span dir="ltr">3.0142</span> | <span dir="ltr">0.0142</span> | **כן** : <span dir="ltr">K = 4, m = 3</span> |

        <!-- /gen -->

        הכדור נכנס לפינה \( (0, 180) \), כמו המכה של סעיף א. עם כיסים נקודתיים אותה מכה לא
        נכנסת לעולם, ולכן רוחב הכיסים הוא מה שמכריע.

    </div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="corner_shot" linenums="1" hl_lines="7 8 10 13 14"
        import math


        def corner_shot(a, b, alpha_deg, w):
            """From the corner (0, 0): K, m and the pocket (x, y) the ball enters."""
            alpha = math.radians(alpha_deg)
            s = a * math.tan(alpha) / (2 * b)          # (1)!
            eps = w / (2 * b * math.cos(alpha))        # (2)!
            k = 1
            while abs(k * s - round(k * s)) >= eps:    # (3)!
                k += 1
            m = round(k * s)
            x = [0, a / 2, a, a / 2][k % 4]            # (4)!
            y = b if m % 2 else 0
            return k, m, (x, y)
        ```

        1. כמה הישר עולה, ביחידות של \( b \), בכל צעד של \( a/2 \) ימינה.
        2. רדיוס הכיס באותן יחידות, אחרי ההכפלה ב-\( \cos\alpha \) של המרחק הניצב.
        3. ‏\( \lVert k s \rVert \) : המרחק מהשלם הקרוב. הלולאה נגמרת תמיד, לפי משפט דיריכלה.
        4. ‏\( k \) זוגי : פינה, \( x = 0 \) או \( a \). ‏\( k \) אי־זוגי : כיס אמצעי.

    #### למה זה נכון { .sol-proof }

    **שתי פינות בלתי אפשריות.** כדי להגיע ל-\( (a, 0) \) או ל-\( (0, 0) \) צריך \( K \) זוגי
    ו-\( m \) זוגי : \( K = 2j \) ו-\( m = 2i \). אבל אז

    \[
    \lvert j s - i \rvert = \tfrac12 \lvert K s - m \rvert < \tfrac{\varepsilon}{2} < \varepsilon
    \]

    כלומר כבר בצעד \( j < K \) הכדור היה נכנס לכיס, בסתירה לכך ש-\( K \) הוא הראשון. במילים :
    המסלול עובר בדיוק באמצע הדרך דרך כיס אחר, שתופס את הכדור קודם. כך המכה של \( 45^\circ \),
    שבסעיף ב נכנסה ל-\( (360, 0) \), נכנסת עכשיו לכיס האמצעי העליון כבר בצעד הראשון.

    **הכדור תמיד נכנס לכיס.** לפי משפט דיריכלה, לכל \( s \) ולכל \( N \) יש
    \( 1 \le k \le N \) עם \( \lVert k s \rVert < 1/N \) : החלקים השבריים של
    \( 0, s, 2s, \dots, Ns \) הם \( N + 1 \) מספרים ב-\( N \) קטעים באורך \( 1/N \), שניים מהם
    באותו קטע, וההפרש בין האינדקסים שלהם הוא \( k \). עם \( N = \lceil 1/\varepsilon \rceil \)
    מקבלים \( K \le \lceil 1/\varepsilon \rceil \), גם כש-\( s \) אי־רציונלי. זה ההבדל המהותי
    מסעיף ב. בשולחן שלנו \( \varepsilon \ge 9/360 = 1/40 \), ולכן \( K \le 40 \) בכל זווית.

    **חיפוש מהיר יותר.** לכל \( k < K \) מתקיים \( \lVert k s \rVert \ge \varepsilon >
    \lVert K s \rVert \), כלומר \( K \) הוא קירוב טוב ביותר של \( s \). קירובים כאלה הם תמיד
    מכנים של השברים המקורבים של \( s \) בפיתוח לשבר משולב, ולכן מספיק לבדוק
    \( O(\log(1/\varepsilon)) \) מכנים במקום \( O(1/\varepsilon) \) צעדים.

---

### סעיף ד – נקודת התחלה כלשהי { #any-start }

"אבל בסנוקר אמיתי הכדור נכנס לכל כיס!" עכשיו הכדור יוצא מנקודה כלשהי \( (x_0, y_0) \) על
השולחן, לא בתוך כיס. הכיסים כמו בסעיף ג.

1. אילו כיסים אפשריים עכשיו?
2. איך מוצאים את הכיס? נסו על מכה ממרכז השולחן \( (180, 90) \) בשיפוע \( \tan\alpha = 7/6 \).
3. האם הכדור עדיין תמיד נכנס לכיס?

??? tip "רמז 1"
    למה בסעיף ג שתי פינות היו חסומות? מה היה מיוחד בנקודת ההתחלה?

??? tip "רמז 2"
    אותה רשת ואותו מעבר על הקווים \( x = k \cdot a/2 \), רק שהישר מתחיל ב-\( (x_0, y_0) \).
    מאיזה \( k \) מתחילים, ומה צריך לבדוק ליד נקודת ההתחלה?

??? tip "רמז 3"
    דיריכלה עבד כי הישר יצא מנקודת רשת. מה קורה כש-\( s \) רציונלי והכדור לא יוצא מנקודת
    רשת, למשל מכה של \( 45^\circ \) מ-\( (180, 45) \)?

??? success "פתרון סעיף ד"
    !!! answer "תשובה בקצרה"
        כל ששת הכיסים אפשריים : מהמרכז בשיפוע \( 7/6 \) הכדור נכנס ל-\( (0, 0) \) אחרי 4
        פגיעות. בכל קו \( x = k \cdot a/2 \), מ-\( k = \lfloor (2x_0 - w)/a \rfloor \), בודקים את
        שתי נקודות הרשת הקרובות לישר, ומקבלים את הראשונה שנמצאת לפני הכדור ובמרחק קטן
        מ-\( w/2 \) מהמסלול. הכדור לא תמיד נכנס : כש-\( s \) רציונלי המסלול מחזורי ויכול לפספס
        את כל הכיסים, למשל מכה של \( 45^\circ \) מ-\( (180, 45) \).

    #### הרעיון { .sol-idea }

    שתי פינות היו חסומות בגלל טיעון האמצע של סעיף ג ("שתי פינות בלתי אפשריות") : כשהכדור יוצא
    מנקודת רשת, באמצע הדרך לפינה עם \( K \) ו-\( m \) זוגיים יש נקודת רשת נוספת, והמסלול עובר
    לידה בחצי מהמרחק, כך שכיס אחר תופס את הכדור קודם. כשהכדור יוצא מנקודה אחרת, אמצע הדרך הוא
    בדרך כלל לא נקודת רשת, הטיעון נופל, וכל ששת הכיסים אפשריים. השיטה נשארת : אותה רשת, אותו מעבר על הקווים האנכיים, ושני
    תיקונים ליד נקודת ההתחלה. המכה מהמרכז :

    <!-- gen 11 -->

    <svg class="figure" viewBox="0 0 643 355" style="max-width:30rem" role="img" aria-label="סעיף ד : הכדור יוצא ממרכז השולחן (180, 90) בשיפוע tan α = 7/6. הוא פוגע בדופן העליונה, בימנית, בתחתונה ושוב בעליונה, ונכנס לכיס (0, 0) : ארבע פגיעות"><rect class="bil-felt" x="33.6" y="33.4" width="576.0" height="288.0"></rect><circle class="bil-pocket is-in" cx="33.6" cy="321.4" r="7.2"><title>הפינה השמאלית התחתונה (0, 0)</title></circle><circle class="bil-pocket" cx="321.6" cy="321.4" r="7.2"><title>הכיס האמצעי התחתון (180, 0)</title></circle><circle class="bil-pocket" cx="609.6" cy="321.4" r="7.2"><title>הפינה הימנית התחתונה (360, 0)</title></circle><circle class="bil-pocket" cx="33.6" cy="33.4" r="7.2"><title>הפינה השמאלית העליונה (0, 180)</title></circle><circle class="bil-pocket" cx="321.6" cy="33.4" r="7.2"><title>הכיס האמצעי העליון (180, 180)</title></circle><circle class="bil-pocket" cx="609.6" cy="33.4" r="7.2"><title>הפינה הימנית העליונה (360, 180)</title></circle><line class="bil-path" x1="321.6" y1="177.4" x2="445.0" y2="33.4" stroke-width="3"/><line class="bil-path" x1="445.0" y1="33.4" x2="609.6" y2="225.4" stroke-width="3"/><line class="bil-path" x1="609.6" y1="225.4" x2="527.3" y2="321.4" stroke-width="3"/><line class="bil-path" x1="527.3" y1="321.4" x2="280.5" y2="33.4" stroke-width="3"/><line class="bil-path" x1="280.5" y1="33.4" x2="33.6" y2="321.4" stroke-width="3"/><circle class="s1-dot" cx="445.0" cy="33.4" r="5"><title>פגיעה 1 בדופן (257.14, 180)</title></circle><text class="legend" x="445.0" y="23.4" text-anchor="middle" style="font-size:15px">1</text><circle class="s1-dot" cx="609.6" cy="225.4" r="5"><title>פגיעה 2 בדופן (360, 60)</title></circle><text class="legend" x="597.6" y="225.4" text-anchor="middle" style="font-size:15px">2</text><circle class="s1-dot" cx="527.3" cy="321.4" r="5"><title>פגיעה 3 בדופן (308.57, 0)</title></circle><text class="legend" x="527.3" y="341.4" text-anchor="middle" style="font-size:15px">3</text><circle class="s1-dot" cx="280.5" cy="33.4" r="5"><title>פגיעה 4 בדופן (154.29, 180)</title></circle><text class="legend" x="280.5" y="23.4" text-anchor="middle" style="font-size:15px">4</text><circle class="ink-dot" cx="321.6" cy="177.4" r="6"><title>הכדור יוצא מ-(180, 90)</title></circle></svg>

    <!-- /gen -->

    <!-- gen 12 -->

    <span class="viz-legend"><span><i class="ink"></i>נקודת היציאה</span><span><i class="bil-path"></i>המסלול</span><span><i class="s1"></i>פגיעה בדופן, לפי הסדר</span><span><i class="bil-key-in"></i>הכיס שהכדור נכנס אליו</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **הישר :** בקו \( x = k \cdot a/2 \) הישר בגובה
       \( y_k = y_0 + \left(k \frac a2 - x_0\right) \tan\alpha \). שתי נקודות הרשת הקרובות הן
       \( m b \) עם \( m = \lfloor y_k / b \rfloor \) ו-\( m + 1 \), והמרחק הניצב מכל אחת
       הוא \( \lvert y_k - m b \rvert \cos\alpha \).

    2. **רק כיסים שלפני הכדור :** נקודה על הישר יכולה להיות מאחורי הכדור. בודקים שהנקודה
       של המסלול הכי קרובה לכיס היא אחרי נקודת ההתחלה, כלומר שהכדור עוד מתקרב לכיס.

    3. **מאיפה מתחילים :** כיס שנמצא מעט מאחורי הכדור בציר \( x \) עוד יכול להיות קרוב למסלול
       לפניו. כדור ב-\( (2, 170) \) בזווית \( 80^\circ \) עולה כמעט אנכית, עובר במרחק 3.7 ס"מ
       מהפינה \( (0, 180) \), שנמצאת 2 ס"מ משמאלו, ונכנס אליה. לכן לא מתחילים מהקו הראשון אחרי
       הכדור. העיגולים של הקו \( k \) מגיעים עד \( x = k \frac a2 + \frac w2 \), והכדור נע ימינה,
       ולכן קו שבו \( k \frac a2 + \frac w2 < x_0 \) כולו מאחוריו. מתחילים מהשלם שמתחת לגבול
       הזה, \( k = \lfloor (2x_0 - w)/a \rfloor \) : בדוגמה \( k = -1 \), ואחריו \( k = 0 \) עם הפינה.

    4. **הכיס :** ה-\( k \) הראשון שיש בו כיס כזה הוא \( K \). הכיס האמיתי :

        | | ‏\( m \) זוגי | ‏\( m \) אי־זוגי |
        |:-:|:-:|:-:|
        | ‏\( K \equiv 1, 3 \pmod 4 \) | ‏\( (\frac a2, 0) \) | ‏\( (\frac a2, b) \) |
        | ‏\( K \equiv 2 \pmod 4 \) | ‏\( (a, 0) \) | ‏\( (a, b) \) |
        | ‏\( K \equiv 0 \pmod 4 \) | ‏\( (0, 0) \) | ‏\( (0, b) \) |

    5. **המכה מהמרכז :** ‏\( y_k = 90 + 210(k - 1) \) :

        <!-- gen 13 -->

        | ‏\( k \) | ‏\( k \cdot 180 \) | ‏\( y_k \) | ‏\( m \) | המרחק של הקו מהכיס | נכנס? |
        |:-:|:-:|:-:|:-:|:-:|:-:|
        | 0 | 0 | <span dir="ltr">−120</span> | – | – | לא : מאחורי הכדור |
        | 1 | 180 | <span dir="ltr">90</span> | – | – | לא : נקודת היציאה |
        | 2 | 360 | <span dir="ltr">300</span> | 2 | <span dir="ltr">39.05</span> | לא |
        | 3 | 540 | <span dir="ltr">510</span> | 3 | <span dir="ltr">19.52</span> | לא |
        | 4 | 720 | <span dir="ltr">720</span> | 4 | <span dir="ltr">0</span> | **כן** : <span dir="ltr">(0, 0)</span> |

        <!-- /gen -->

        ‏\( K = 4 \) ו-\( m = 4 \) : הפינה \( (0, 0) \). בדרך הכדור פוגע בדופן העליונה,
        בימנית, בתחתונה ושוב בעליונה.

    6. **לא תמיד נכנס :** נסמן \( c = (y_0 - x_0 \tan\alpha)/b \), ואז \( y_k / b = k s + c \)
       והתנאי הוא \( \lVert k s + c \rVert < \varepsilon \). כש-\( s \) אי־רציונלי, הערכים
       \( k s + c \) מודולו 1 צפופים בקטע (משפט קרונקר), ולכן הכדור נכנס לבסוף. כש-\( s = q/p \)
       רציונלי, הם מקבלים רק \( p \) ערכים, והמסלול מחזורי. אם אף אחד מהם לא קרוב מספיק לשלם,
       הכדור לא נכנס לעולם. מ-\( (180, 45) \) ב-\( 45^\circ \) : ‏\( s = 1 \), ‏\( c = -0.75 \),
       ו-\( \lVert c \rVert = 0.25 > \varepsilon \approx 0.035 \). הכדור חוזר על אותו מעוין בלי
       סוף.

    </div>

    **נסו בעצמכם.** הקלידו בתיבה את שתי המכות הקשות ונחשו לפני "מכה" : ‏\( 45^\circ \)
    מ-\( (180, 45) \), שלא נכנסת לעולם (מה הפער בכל קו של כיסים, ולמה הוא לא קטן?), ו-\( 37^\circ \)
    מהפינה עם כיסים של 1 ס"מ (כמה קווים עד \( K \), ולאיזה כיס?). אחר כך גררו את הכדור ואת
    החץ לכל מקום. מה שהתיבה מוסיפה על האיורים : כל נקודת יציאה וכל כיוון, המסלול האמיתי לצד
    השולחן הפתוח, והחישוב של סעיפים ג ו-ד קו אחרי קו.

    <div class="explorer" data-kind="billiard" data-x0="180" data-y0="90" data-deg="49.4"></div>

    #### הקוד { .sol-code }

    === "Python"
        ```python title="find_pocket" linenums="1" hl_lines="13 16 19 20 21"
        import math


        def find_pocket(a, b, alpha_deg, w, x0=0.0, y0=0.0, max_k=10**6):
            """The pocket the ball enters, as a point (x, y), or None if there is none by max_k.

            Six pockets of width w: the corners and the middles (a/2, 0) and (a/2, b). The ball
            starts at (x0, y0), not inside a pocket (or at the centre of the one it leaves), and
            moves at alpha_deg degrees, 0 < alpha < 90. Assumes w < a/2 and w < b cos(alpha).
            """
            alpha = math.radians(alpha_deg)
            dx, dy = math.cos(alpha), math.sin(alpha)
            k = math.floor((2 * x0 - w) / a)                # (1)!
            while k <= max_k:
                px = k * a / 2                               # the k-th line of pockets
                y_k = y0 + (px - x0) * dy / dx               # (2)!
                for m in (math.floor(y_k / b), math.floor(y_k / b) + 1):
                    fx, fy = px - x0, m * b - y0             # from the ball to the pocket
                    ahead = fx * dx + fy * dy                # (3)!
                    off = abs(fx * dy - fy * dx)             # (4)!
                    if ahead > 0 and off < w / 2:
                        x = [0, a / 2, a, a / 2][k % 4]      # (5)!
                        y = b if m % 2 else 0
                        return (x, y)
                k += 1
            return None
        ```

        1. גם כיס שנמצא מעט מאחורי הכדור בציר \( x \) יכול להיות קרוב למסלול לפניו.
        2. הגובה של המסלול על הקו \( x = k \cdot a/2 \) ברשת.
        3. ההיטל על כיוון התנועה : חיובי כשהנקודה הכי קרובה לכיס היא לפני הכדור. כיס שהכדור
           יוצא ממרכזו נותן 0, ולכן לא נספר.
        4. המרחק הניצב מהכיס למסלול : המכפלה הווקטורית עם וקטור היחידה של הכיוון.
        5. כמו בסעיף ג. ב-Python גם \( k \) ו-\( m \) שליליים נותנים כאן את הכיס הנכון.

    #### למה זה נכון { .sol-proof }

    **הסדר נשמר.** כשהכדור נכנס לעיגול של כיס בקו \( k \), הוא בתוך הרצועה
    \( k \frac a2 - \frac w2 < x < k \frac a2 + \frac w2 \). הרצועות של קווים שונים זרות כי
    \( w < a/2 \), והכדור נע ימינה, ולכן הקו הראשון שיש בו כיס כזה הוא גם הכיס הראשון בזמן.

    **הבדיקה ליד ההתחלה מדויקת.** הכדור נכנס לעיגול בדיוק כשהקרן שיוצאת ממנו עוברת בעיגול. אם
    הנקודה הכי קרובה לכיס על הישר היא לפני הכדור, זה המרחק הניצב. אם היא מאחוריו, הכדור רק
    מתרחק מהכיס, והוא לא התחיל בתוכו.

    **בדיקה.** הקוד הושווה לסימולציה פיזיקלית עם החזרות אמיתיות, אלפי מכות אקראיות מכל
    נקודה על השולחן, והתוצאות זהות. בלי שני התיקונים, 21 מתוך 3651 מכות יצאו שגויות.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : סימולציה צעד אחרי צעד בלי עצירה"
    סימולציה של ההחזרות היא נכונה, אבל צריך לדעת מתי לעצור. בסעיף ב, ב-\( 37^\circ \), היא לא
    נגמרת לעולם, וגם בסעיף ד יש מכות מחזוריות שלא נכנסות אף פעם. צריך חסם (כמו \( K \le
    \lceil 1/\varepsilon \rceil \) של סעיף ג) או `max_k`.

??? trap "מלכודת : שבר שלא צומצם"
    ב-\( \tan\alpha = 3/4 \), ‏\( r = 6/4 \) נותן \( p = 4 \) ו-\( q = 6 \), שניהם זוגיים, כאילו
    הכדור חוזר ל-\( (0, 0) \). אבל הוא נכנס קודם ל-\( (2a, 3b) \), הפינה \( (0, b) \). רק השבר
    המצומצם \( 3/2 \) נותן את הכיס.

??? trap "מלכודת : לבלבל בין \( K \) ו-\( m \) לבין \( Ks \)"
    ‏\( K \) ו-\( m \) שלמים, ורק \( K s \) ממשי. השאלה "האם 5.67 זוגי?" אין לה משמעות : מעגלים
    ל-\( m = 6 \), והמרחק הוא \( \lVert 5.67 \rVert = 0.33 \).

??? trap "מלכודת : צעד של a במקום a/2"
    בסעיף ג צעד של \( a \) בודק רק את הפינות ומפספס את הכיסים האמצעיים. המכה של \( 45^\circ \)
    ייצאה אז \( (360, 0) \), אבל היא נכנסת לכיס האמצעי העליון כבר בצעד הראשון.

??? trap "מלכודת : הפער האנכי במקום המרחק הניצב"
    הפער \( \lvert y_k - m b \rvert \) הוא לאורך הקו האנכי, לא המרחק מהמסלול. צריך להכפיל
    ב-\( \cos\alpha \), אחרת מכות שעוברות קרוב לכיס בזווית חדה נחשבות כמפספסות.

??? trap "מלכודת : להתחיל אחרי הכדור ולמדוד מרחק מהישר"
    בגרסה של סעיף ד שמתחילה מ-\( k = \lfloor 2x_0/a \rfloor + 1 \) ובודקת את המרחק מהישר כולו
    יש שתי טעויות ליד נקודת ההתחלה. כדור ב-\( (2, 170) \) בזווית \( 80^\circ \) נכנס
    ל-\( (0, 180) \), שמאחוריו בציר \( x \), והגרסה הזו לא בודקת את הכיס הזה בכלל. כדור
    ב-\( (179, 5) \) בזווית \( 60^\circ \) מתרחק מ-\( (180, 0) \), אבל הישר כולו עובר קרוב אליו,
    והגרסה הזו מכניסה אותו לשם.

??? trap "מלכודת : \"בסנוקר הכדור נכנס לכל כיס, אז סעיף ג שגוי\""
    התוצאה של סעיף ג נכונה, ובאה מכך שהכדור יוצא מנקודת רשת, הפינה. מנקודה אחרת, כמו בסעיף ד,
    כל הכיסים אפשריים.

??? followup "שאלות המשך"
    - **שינוי קטן בכיוון :** בסעיף א, מה קורה אם מכוונים ל-\( (241, 180) \) במקום
      ל-\( (240, 180) \)?

        ??? fu-answer "תשובה"
            ‏\( r = 360/241 \), מצומצם : \( p = 241 \) ו-\( q = 360 \). הכדור נכנס ל-\( (360, 0) \)
            אחרי 599 פגיעות. ביד זה כבר לא עובד, ובנוסחה זה שורה אחת.

    - **סיבוכיות :** כמה צעדים לוקח החיפוש של סעיף ג, ואיך משפרים?

        ??? fu-answer "תשובה"
            עד \( \lceil 1/\varepsilon \rceil \) צעדים. עם שברים משולבים בודקים רק מכנים של
            שברים מקורבים : ב-\( 37^\circ \) עם כיסים של 1 ס"מ, ‏\( K = 211 \), והמכנים הם 1, 4,
            69, 142 ו-211. חמש בדיקות במקום 211.

    - **כיוונים אחרים :** מה קורה כש-\( \alpha \ge 90^\circ \), או כשהכדור נע שמאלה או למטה?

        ??? fu-answer "תשובה"
            משקפים את השולחן : \( x \to a - x \) כשהכדור נע שמאלה, ו-\( y \to b - y \) כשהוא נע
            למטה. פותרים כרגיל ומשקפים את הכיס בחזרה. התיבה עושה בדיוק את זה.

    - **כדור עם רדיוס :** איך משתנה הפתרון כשלכדור יש רדיוס \( \rho > 0 \)?

        ??? fu-answer "תשובה"
            מכווצים את השולחן ב-\( \rho \) מכל צד : מרכז הכדור נע על שולחן
            \( (a - 2\rho) \times (b - 2\rho) \), והכיסים בפינות ובאמצעים שלו. כדור סנוקר,
            ‏\( \rho = 2.625 \) ס"מ, נותן שולחן של 354.75 על 174.75, ו-\( s \) כבר לא שווה
            בדיוק ל-\( \tan\alpha \).

    - **כמה פגיעות :** כמה פעמים הכדור פוגע בדפנות בסעיף ג?

        ??? fu-answer "תשובה"
            סופרים קווים ברשת שהישר חוצה לפני שהוא נכנס לעיגול : \( \lceil K/2 \rceil - 1 \)
            אנכיים ו-\( m - 1 \) אופקיים, ועוד אחד כשהכדור פוגע בדופן שליד הכיס רגע לפני שהוא
            נכנס. ב-\( 37^\circ \) : ‏\( 1 + 2 = 3 \).

    - **כיסים ברוחב שונה :** מה אם רוחב הפינות \( w_c \) ורוחב האמצעיים \( w_m \)?

        ??? fu-answer "תשובה"
            ההוכחה ששתי פינות חסומות עוברת כש-\( w_c \le 2 w_m \) : הכיס באמצע הדרך צריך להיות
            רחב מספיק. עם \( w_c = 9 \) ו-\( w_m = 1 \), מכה של \( 0.5^\circ \) מתגלגלת ליד הדופן
            התחתונה, עוברת ליד הכיס האמצעי בלי להיכנס, ונכנסת ל-\( (360, 0) \).
