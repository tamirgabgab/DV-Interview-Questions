---
id: 48
title: החוואי, האוכל והמים
level: student
difficulty: medium
kind: math
tags: [math, geometry, logic-puzzles, python, systemverilog]
source: ""
added: 2026-10-26
---

## השאלה

בשטח יש שני קווים אופקיים מקבילים, והמרחק האנכי ביניהם הוא \( H \) :

- **הקו העליון :** לאורכו אפשר לאסוף **אוכל**.
- **הקו התחתון :** לאורכו אפשר לאסוף **מים**.

חוואי עומד בנקודה \( A \) ורוצה להגיע לפרה בנקודה \( B \). שתי הנקודות נמצאות בין שני
הקווים או עליהם :

- **החוואי :** הנקודה \( A \) נמצאת בגובה \( a \) מעל הקו התחתון.
- **הפרה :** הנקודה \( B \) נמצאת בגובה \( b \) מעל הקו התחתון.
- **המרחק :** המרחק האופקי בין \( A \) ל-\( B \) הוא \( L \).

בדרך לפרה החוואי חייב קודם להגיע לקו העליון ולקחת אוכל, אחר כך להגיע לקו התחתון ולקחת
מים, ומשם ללכת ישר אל הפרה. כל קטע בדרך הוא קו ישר.

סימונים למרחקים האופקיים :

- **‏\( x \) :** מ-\( A \) לנקודת איסוף האוכל.
- **‏\( y \) :** מנקודת האוכל לנקודת המים.
- **‏\( w \) :** מנקודת המים לפרה.

מתקיים \( x + y + w = L \). את אורכי שלושת הקטעים האלכסוניים של המסלול מסמנים
\( z_1, z_2, z_3 \), ואת אורך המסלול כולו \( z = z_1 + z_2 + z_3 \).

- **סעיף א – גבהים נתונים :** החוואי בשליש הגובה והפרה בשני שלישים. מה המסלול הקצר ביותר,
  ואיפה עוצרים?
- **סעיף ב – הבעיה ההפוכה :** העצירות ידועות, בשליש ובשני שלישים מהדרך. באילו גבהים עומדים
  החוואי והפרה?
- **סעיף ג – קו אוכל נטוי :** קו האוכל נוטה בזווית \( \theta \) בין 0 ל-60 מעלות, והקווים
  מתרחקים לכיוון הפרה. מה האורך ומה העצירות, ומתי השיקוף עדיין עובד?

<!-- gen 0 -->

<svg class="figure" viewBox="0 0 578 293" style="max-width:30rem" role="img" aria-label="שני קווים אופקיים במרחק H זה מזה : קו האוכל למעלה וקו המים למטה. החוואי A בגובה a מעל קו המים והפרה B בגובה b, במרחק אופקי L. מסלול לדוגמה : מ-A לקו האוכל (z1, התקדמות אופקית x), משם לקו המים (z2, התקדמות y) ומשם לפרה (z3, התקדמות w)"><rect class="box-face" x="100.4" y="38.6" width="378.0" height="162.0"></rect><line class="s1-line" x1="35.6" y1="200.6" x2="543.2" y2="200.6" stroke-width="3" stroke-dasharray="9 6"/><line class="s3-line" x1="35.6" y1="38.6" x2="543.2" y2="38.6" stroke-width="3" stroke-dasharray="9 6"/><line class="box-path" x1="100.4" y1="146.6" x2="262.4" y2="38.6" stroke-width="3"/><line class="box-path" x1="262.4" y1="38.6" x2="370.4" y2="200.6" stroke-width="3"/><line class="box-path" x1="370.4" y1="200.6" x2="478.4" y2="92.6" stroke-width="3"/><text class="legend" x="169.4" y="88.6" text-anchor="middle" style="font-size:17px">z1</text><text class="legend" x="332.4" y="115.6" text-anchor="middle" style="font-size:17px">z2</text><text class="legend" x="414.4" y="138.6" text-anchor="middle" style="font-size:17px">z3</text><line class="ink-line" x1="100.4" y1="224.9" x2="262.4" y2="224.9" stroke-width="1.2"/><line class="ink-line" x1="100.4" y1="216.8" x2="100.4" y2="233.0" stroke-width="1.2"/><line class="ink-line" x1="262.4" y1="216.8" x2="262.4" y2="233.0" stroke-width="1.2"/><text class="legend" x="181.4" y="218.9" text-anchor="middle" style="font-size:16px">x</text><line class="ink-line" x1="262.4" y1="224.9" x2="370.4" y2="224.9" stroke-width="1.2"/><line class="ink-line" x1="262.4" y1="216.8" x2="262.4" y2="233.0" stroke-width="1.2"/><line class="ink-line" x1="370.4" y1="216.8" x2="370.4" y2="233.0" stroke-width="1.2"/><text class="legend" x="316.4" y="218.9" text-anchor="middle" style="font-size:16px">y</text><line class="ink-line" x1="370.4" y1="224.9" x2="478.4" y2="224.9" stroke-width="1.2"/><line class="ink-line" x1="370.4" y1="216.8" x2="370.4" y2="233.0" stroke-width="1.2"/><line class="ink-line" x1="478.4" y1="216.8" x2="478.4" y2="233.0" stroke-width="1.2"/><text class="legend" x="424.4" y="218.9" text-anchor="middle" style="font-size:16px">w</text><line class="ink-line" x1="100.4" y1="262.7" x2="478.4" y2="262.7" stroke-width="1.2"/><line class="ink-line" x1="100.4" y1="254.6" x2="100.4" y2="270.8" stroke-width="1.2"/><line class="ink-line" x1="478.4" y1="254.6" x2="478.4" y2="270.8" stroke-width="1.2"/><text class="legend" x="289.4" y="256.7" text-anchor="middle" style="font-size:16px">L</text><line class="ink-line" x1="81.5" y1="200.6" x2="81.5" y2="146.6" stroke-width="1.2"/><text class="legend" x="71.5" y="178.6" text-anchor="middle" style="font-size:16px">a</text><line class="ink-line" x1="46.4" y1="200.6" x2="46.4" y2="38.6" stroke-width="1.2"/><text class="legend" x="36.4" y="124.6" text-anchor="middle" style="font-size:16px">H</text><line class="ink-line" x1="497.3" y1="200.6" x2="497.3" y2="92.6" stroke-width="1.2"/><text class="legend" x="507.3" y="151.6" text-anchor="middle" style="font-size:16px">b</text><circle class="s3-dot" cx="262.4" cy="38.6" r="6"><title>נקודת האוכל</title></circle><circle class="s1-dot" cx="370.4" cy="200.6" r="6"><title>נקודת המים</title></circle><circle class="ink-dot" cx="100.4" cy="146.6" r="6"><title>החוואי A</title></circle><text class="legend" x="114.4" y="138.6" text-anchor="middle" style="font-size:18px">A</text><circle class="s2-dot" cx="478.4" cy="92.6" r="6"><title>הפרה B</title></circle><text class="legend" x="464.4" y="84.6" text-anchor="middle" style="font-size:18px">B</text></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="s3"></i>קו האוכל</span><span><i class="s1"></i>קו המים</span><span><i class="ink"></i>החוואי A</span><span><i class="s2"></i>הפרה B</span><span><i class="box-path"></i>מסלול לדוגמה, לא הקצר ביותר</span></span>

<!-- /gen -->

??? interviewer "מה המראיין בודק"
    - **להחליף בעיה בבעיה מוכרת :** לראות ששיקוף דרך קו הופך מסלול שבור לקו ישר, ושהקו
      הישר הוא הקצר ביותר.
    - **שיקוף כפול :** לשקף פעמיים, בסדר הנכון, ולחשב נכון את הגובה של הנקודה המשוקפת.
    - **משולשים דומים :** לחלק את הדרך האופקית לפי ההתקדמות האנכית, בלי נגזרות.
    - **בעיה הפוכה :** להפוך את הנוסחאות, ולשים לב מתי לבעיה ההפוכה אין פתרון.
    - **שיקוף דרך קווים נחתכים :** לזהות ששני שיקופים הם סיבוב בזווית כפולה, לשקף בניצב לקו
      הנטוי, ולבדוק שהקו הישר באמת חוצה את הקווים בסדר הנכון.

---

### סעיף א – החוואי בשליש הגובה והפרה בשני שלישים

נתון \( a = H/3 \) ו-\( b = 2H/3 \). מצאו את אורך המסלול הקצר ביותר ואת נקודות העצירה
\( (x, y, w) \).

??? tip "רמז 1"
    מה קורה למסלול כשמשקפים את הפרה דרך קו? הקטע האחרון שווה באורכו לקטע אל הנקודה
    המשוקפת.

??? tip "רמז 2"
    שקפו את הפרה פעמיים : קודם דרך קו המים, ואז את התמונה דרך קו האוכל. כל מסלול חוקי
    שווה באורכו לקו שבור מ-\( A \) אל התמונה השנייה, והקו השבור הקצר ביותר הוא קו ישר.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        המסלול הקצר ביותר הוא \( z = \sqrt{L^2 + 49H^2/9} \), והעצירות הן
        \( x = 2L/7 \), \( y = 3L/7 \) ו-\( w = 2L/7 \).

    #### הרעיון { .sol-idea }

    במקום לחפש את שתי נקודות העצירה, משקפים את הפרה. שיקוף דרך קו לא משנה את אורך הקטע
    שנוגע בו, ולכן כל מסלול חוקי שווה באורכו לקו שבור מ-\( A \) אל נקודה \( B'' \) שנמצאת
    בגובה \( 2H + b \). הקו השבור הקצר ביותר הוא קו ישר, והוא היתר של משולש ישר זווית
    שהניצבים שלו ידועים.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שיקוף דרך קו המים :** משקפים את \( B \) דרך הקו התחתון ומקבלים את \( B' \), בעומק
       \( b \) מתחת לקו. לכל נקודה \( Q \) על קו המים מתקיים \( |QB| = |QB'| \), ולכן
       הקטע האחרון של המסלול שווה באורכו לקטע אל \( B' \).
    2. **שיקוף דרך קו האוכל :** משקפים את \( B' \) דרך הקו העליון ומקבלים את \( B'' \).
       המרחק של \( B' \) מהקו העליון הוא \( H + b \), ולכן \( B'' \) נמצאת בגובה
       \( 2H + b \) מעל קו המים. הקטע מנקודת האוכל אל קו המים ומשם אל \( B' \) שווה באורכו
       לקטעים המשוקפים שלו, מנקודת האוכל אל \( B'' \).
    3. **קו ישר :** כל מסלול חוקי שווה באורכו לקו שבור מ-\( A \) אל \( B'' \). ההפרש
       האופקי ביניהן הוא \( L \) וההפרש האנכי הוא \( D = 2H + b - a \), ולכן לפי פיתגורס

        \[
        z_{\min} = \sqrt{L^2 + (2H + b - a)^2}
        \]

    4. **נקודות העצירה :** לאורך קו ישר ההתקדמות האופקית פרופורציונלית להתקדמות האנכית.
       הקו עולה \( H - a \) עד קו האוכל, עוד \( H \) עד התמונה של קו המים, ועוד \( b \) עד
       \( B'' \). לכן
       \( x = L(H - a)/D \), ‏\( y = LH/D \) ו-\( w = Lb/D \).
    5. **הצבה :** עם \( a = H/3 \) ו-\( b = 2H/3 \) מקבלים \( D = 7H/3 \), ולכן
       \( x = 2L/7 \), ‏\( y = 3L/7 \), ‏\( w = 2L/7 \) ו-\( z_{\min} = \sqrt{L^2 + 49H^2/9} \).

    </div>

    #### למה זה נכון { .sol-proof }

    בשרטוט הרצועה המקורית נמצאת בין 0 ל-\( H \). מתחתיה השיקוף שלה דרך קו המים, ובו
    \( B' \). מעליה שני שיקופים, ובעליון \( B'' \). הקו הישר המקווקו מ-\( A \) אל \( B'' \)
    הוא המסלול הקצר ביותר אחרי הפרישה : הוא חוצה את קו האוכל בנקודת האוכל ואת השיקוף של קו
    המים בתמונה של נקודת המים.

    <!-- gen 2 -->

    <svg class="figure" viewBox="0 0 480 478" style="max-width:26rem" role="img" aria-label="סעיף א עם H = 3, a = 1, b = 2, L = 7 : הרצועה, השיקוף שלה למטה דרך קו המים עם B′, ושני שיקופים למעלה עם B″ בגובה 2H + b = 8. הקו הישר מ-A ל-B″ חוצה את קו האוכל ואת השיקוף של קו המים בנקודות העצירה. הוא היתר של משולש ישר זווית עם ניצבים L ו-2H + b − a, ושלושת המשולשים הקטנים לאורכו דומים לו"><rect class="box-copy" x="90.8" y="351.2" width="252.0" height="108.0"></rect><rect class="box-face" x="90.8" y="243.2" width="252.0" height="108.0"></rect><rect class="box-copy" x="90.8" y="135.2" width="252.0" height="108.0"></rect><rect class="box-copy" x="90.8" y="27.2" width="252.0" height="108.0"></rect><line class="s3-line" x1="76.4" y1="459.2" x2="357.2" y2="459.2" stroke-width="3" stroke-dasharray="9 6"/><line class="s1-line" x1="76.4" y1="351.2" x2="357.2" y2="351.2" stroke-width="3" stroke-dasharray="9 6"/><line class="s3-line" x1="76.4" y1="243.2" x2="357.2" y2="243.2" stroke-width="3" stroke-dasharray="9 6"/><line class="s1-line" x1="76.4" y1="135.2" x2="357.2" y2="135.2" stroke-width="3" stroke-dasharray="9 6"/><line class="s3-line" x1="76.4" y1="27.2" x2="357.2" y2="27.2" stroke-width="3" stroke-dasharray="9 6"/><text class="legend" x="71.0" y="464.2" text-anchor="end" style="font-size:14px">−H</text><text class="legend" x="71.0" y="356.2" text-anchor="end" style="font-size:14px">0</text><text class="legend" x="71.0" y="248.2" text-anchor="end" style="font-size:14px">H</text><text class="legend" x="71.0" y="140.2" text-anchor="end" style="font-size:14px">2H</text><text class="legend" x="71.0" y="32.2" text-anchor="end" style="font-size:14px">3H</text><line class="box-path" x1="90.8" y1="315.2" x2="162.8" y2="243.2" stroke-width="3"/><line class="box-path" x1="162.8" y1="243.2" x2="270.8" y2="351.2" stroke-width="3"/><line class="box-path" x1="270.8" y1="351.2" x2="342.8" y2="279.2" stroke-width="3"/><line class="ink-line" x1="270.8" y1="351.2" x2="342.8" y2="423.2" stroke-width="1.5" stroke-dasharray="4 3"/><line class="box-path" x1="90.8" y1="315.2" x2="342.8" y2="63.2" stroke-width="3" stroke-dasharray="8 5"/><line class="ink-line" x1="342.8" y1="279.2" x2="342.8" y2="423.2" stroke-width="1" stroke-dasharray="2 3"/><line class="ink-line" x1="90.8" y1="315.2" x2="342.8" y2="315.2" stroke-width="1.2"/><line class="ink-line" x1="342.8" y1="315.2" x2="342.8" y2="63.2" stroke-width="1.2"/><text class="legend" x="216.8" y="333.2" text-anchor="middle" style="font-size:15px">L</text><line class="ink-line" x1="90.8" y1="315.2" x2="162.8" y2="315.2" stroke-width="1" stroke-dasharray="3 3"/><line class="ink-line" x1="162.8" y1="315.2" x2="162.8" y2="243.2" stroke-width="1" stroke-dasharray="3 3"/><text class="legend" x="126.8" y="310.2" text-anchor="middle" style="font-size:13px">x</text><text class="legend" x="167.8" y="284.2" text-anchor="start" style="font-size:13px">H − a</text><text class="legend" x="118.8" y="275.2" text-anchor="end" style="font-size:15px">z1</text><line class="ink-line" x1="162.8" y1="243.2" x2="270.8" y2="243.2" stroke-width="1" stroke-dasharray="3 3"/><line class="ink-line" x1="270.8" y1="243.2" x2="270.8" y2="135.2" stroke-width="1" stroke-dasharray="3 3"/><text class="legend" x="216.8" y="238.2" text-anchor="middle" style="font-size:13px">y</text><text class="legend" x="275.8" y="194.2" text-anchor="start" style="font-size:13px">H</text><text class="legend" x="208.8" y="185.2" text-anchor="end" style="font-size:15px">z2</text><line class="ink-line" x1="270.8" y1="135.2" x2="342.8" y2="135.2" stroke-width="1" stroke-dasharray="3 3"/><line class="ink-line" x1="342.8" y1="135.2" x2="342.8" y2="63.2" stroke-width="1" stroke-dasharray="3 3"/><text class="legend" x="306.8" y="130.2" text-anchor="middle" style="font-size:13px">w</text><text class="legend" x="347.8" y="104.2" text-anchor="start" style="font-size:13px">b</text><text class="legend" x="298.8" y="95.2" text-anchor="end" style="font-size:15px">z3</text><line class="ink-line" x1="368.0" y1="315.2" x2="368.0" y2="63.2" stroke-width="1.2"/><line class="ink-line" x1="362.6" y1="315.2" x2="373.4" y2="315.2" stroke-width="1.2"/><line class="ink-line" x1="362.6" y1="63.2" x2="373.4" y2="63.2" stroke-width="1.2"/><text class="legend" x="374.0" y="194.2" text-anchor="start" style="font-size:14px">2H + b − a</text><circle class="s3-dot" cx="162.8" cy="243.2" r="5"><title>נקודת האוכל</title></circle><circle class="s1-dot" cx="270.8" cy="351.2" r="5"><title>נקודת המים</title></circle><circle class="s1-dot" cx="270.8" cy="135.2" r="4"><title>נקודת המים אחרי השיקוף</title></circle><circle class="ink-dot" cx="90.8" cy="315.2" r="6"><title>החוואי A</title></circle><text class="legend" x="78.8" y="309.2" text-anchor="middle" style="font-size:18px">A</text><circle class="s2-dot" cx="342.8" cy="279.2" r="6"><title>הפרה B</title></circle><text class="legend" x="354.8" y="273.2" text-anchor="middle" style="font-size:18px">B</text><circle class="ink-dot" cx="342.8" cy="423.2" r="4"><title>B′ : השיקוף של B דרך קו המים</title></circle><text class="legend" x="356.8" y="439.2" text-anchor="middle" style="font-size:18px">B′</text><circle class="s2-dot" cx="342.8" cy="63.2" r="6"><title>B″ : השיקוף של B′ דרך קו האוכל</title></circle><text class="legend" x="342.8" y="51.2" text-anchor="middle" style="font-size:18px">B″</text></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="s3"></i>קו האוכל ושיקופיו</span><span><i class="s1"></i>קו המים ושיקופיו</span><span><i class="box-face"></i>השטח עצמו</span><span><i class="box-copy"></i>השיקופים שלו</span><span><i class="box-path"></i>המסלול הקצר ביותר, והקו הישר מ-A ל-B″</span></span>

    <!-- /gen -->

    **כל מסלול ארוך לפחות כמו הקו הישר.** ניקח מסלול כלשהו שעוצר באוכל ב-\( P \) ובמים
    ב-\( Q \). השיקוף דרך קו המים לא משנה את \( |QB| \), ולכן \( |QB| = |QB'| \). השיקוף
    דרך קו האוכל לא משנה את \( |PQ| \) ואת \( |QB'| \), ולכן
    \( |PQ| + |QB'| = |PQ''| + |Q''B''| \), כאשר \( Q'' \) היא התמונה של \( Q \). מכאן שאורך
    המסלול הוא \( |AP| + |PQ''| + |Q''B''| \), קו שבור מ-\( A \) אל \( B'' \), ולפי אי
    שוויון המשולש הוא לפחות \( |AB''| \). השוויון מתקיים רק כשהנקודות על הקו הישר.

    **פיתגורס על שלושת הקטעים.** בכל קטע האורך האלכסוני הוא היתר של משולש ישר זווית :

    | הקטע | התקדמות אופקית | התקדמות אנכית | האורך |
    |---|---|---|---|
    | מ-\( A \) לאוכל | ‏\( x = 2L/7 \) | ‏\( H - a = 2H/3 \) | ‏\( z_1 = \tfrac{2}{7} z \) |
    | מהאוכל למים | ‏\( y = 3L/7 \) | ‏\( H \) | ‏\( z_2 = \tfrac{3}{7} z \) |
    | מהמים לפרה | ‏\( w = 2L/7 \) | ‏\( b = 2H/3 \) | ‏\( z_3 = \tfrac{2}{7} z \) |
    | כל המסלול | ‏\( L \) | ‏\( 7H/3 \) | ‏\( z = \sqrt{L^2 + 49H^2/9} \) |

    שלושת המשולשים הקטנים דומים למשולש הגדול, כי לכולם אותו שיפוע \( D/L \). לכן כל אחד
    מהם הוא אותו חלק מהמשולש הגדול בכל הצלעות : \( z_1 = \sqrt{x^2 + (H - a)^2} \) הוא
    שני שביעים של \( z \), וכן הלאה. בדיקה : ‏<span dir="ltr">2/7 + 3/7 + 2/7 = 1</span>.

    **דוגמה במספרים.** עם \( L = 7 \) ו-\( H = 3 \) מקבלים \( a = 1 \), ‏\( b = 2 \),
    ‏\( D = 7 \), והקו עולה בזווית של 45 מעלות : ‏<span dir="ltr">x = 2, y = 3, w = 2</span>
    ו-\( z = \sqrt{98} \approx 9.9 \).

    **נסו בעצמכם.** בתיבה הבאה גוררים את החוואי ואת הפרה לאורך הדפנות (סעיף א), או את
    נקודות העצירה לאורך הקווים (סעיף ב), ואת ארבע הפינות של המלבן כדי לשנות את \( L \) ואת
    \( H \). אפשר גם להקליד ערכים, או להגריל אותם. המסלול הקצר ביותר מקווקו, והטבלה מתחת
    לציור מחשבת את שלושת הקטעים לפי פיתגורס. "הצגת השיקוף" מוסיפה את הרצועות המשוקפות, את
    \( B' \) ואת \( B'' \) ואת המשולש הגדול.

    <div class="explorer" data-kind="farm" data-mode="a" data-l="7" data-h="3" data-a="1" data-b="2"></div>

---

### סעיף ב – העצירות בשליש ובשני שלישים

כעת הבעיה הפוכה : ידוע שבמסלול האופטימלי החוואי עצר לקחת אוכל בשליש מהדרך האופקית,
ולקחת מים בשני שלישים ממנה. מצאו את \( a \) ואת \( b \).

??? tip "רמז 1"
    השתמשו בנוסחאות של סעיף א בכיוון ההפוך : מהנוסחה של \( y \) אפשר למצוא את ההפרש האנכי
    הכולל \( D \).

??? tip "רמז 2"
    שימו לב שהשיפוע של הקו הישר קבוע : בקטע האמצעי הוא עולה \( H \) על פני \( y \). כמה הוא
    עולה על פני \( x \) ועל פני \( w \)?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏\( a = 0 \) ו-\( b = H \) : החוואי עומד על קו המים, והפרה נמצאת על קו האוכל.

    #### הרעיון { .sol-idea }

    המסלול הקצר ביותר הוא קו ישר אחרי הפרישה, ולכן השיפוע שלו זהה בשלושת הקטעים. בקטע
    האמצעי הוא עולה \( H \) על פני \( y \), וכך יודעים כמה הוא עולה בקטע הראשון
    (\( H - a \)) ובאחרון (\( b \)).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **ההפרש הכולל :** מהנוסחה \( y = LH/D \) מקבלים \( D = LH/y \).
    2. **הגובה של החוואי :** מ-\( x = L(H - a)/D = y(H - a)/H \) מקבלים
       \( a = H(1 - x/y) \).
    3. **הגובה של הפרה :** מ-\( w = Lb/D = yb/H \) מקבלים \( b = Hw/y \).
    4. **תנאי קיום :** צריך \( 0 \le a \le H \) ו-\( 0 \le b \le H \). התנאי \( a \ge 0 \)
       הוא \( x \le y \), והתנאי \( b \le H \) הוא \( w \le y \). כלומר הקטע האמצעי \( y \)
       הוא הארוך מבין שלושת המרחקים האופקיים. אחרת אין גבהים שבהם זה המסלול הקצר ביותר.
    5. **הצבה :** נקודת האוכל ב-\( L/3 \) ונקודת המים ב-\( 2L/3 \), ולכן
       \( x = y = w = L/3 \). מקבלים \( a = H(1 - 1) = 0 \) ו-\( b = H \cdot 1 = H \).

    </div>

    #### למה זה נכון { .sol-proof }

    **בדיקה בנוסחאות של סעיף א.** עם \( a = 0 \) ו-\( b = H \) מקבלים
    \( D = 2H + H - 0 = 3H \), ולכן \( x = LH/3H = L/3 \), וכך גם \( y \) ו-\( w \). הקו
    הישר מ-\( A \) אל \( B'' \) עולה \( 3H \) על פני \( L \), ושלושת המשולשים לאורכו חופפים,
    עם ניצבים \( L/3 \) ו-\( H \) :

    <!-- gen 3 -->

    <svg class="figure" viewBox="0 0 480 478" style="max-width:26rem" role="img" aria-label="סעיף ב עם H = 3, a = 0, b = 3, L = 7 : החוואי על קו המים והפרה על קו האוכל. B″ בגובה 3H, והקו הישר מ-A אליו חוצה את קו האוכל ואת השיקוף של קו המים בשליש ובשני שלישים מהדרך : שלושה משולשים חופפים עם ניצבים L/3 ו-H"><rect class="box-copy" x="90.8" y="351.2" width="252.0" height="108.0"></rect><rect class="box-face" x="90.8" y="243.2" width="252.0" height="108.0"></rect><rect class="box-copy" x="90.8" y="135.2" width="252.0" height="108.0"></rect><rect class="box-copy" x="90.8" y="27.2" width="252.0" height="108.0"></rect><line class="s3-line" x1="76.4" y1="459.2" x2="357.2" y2="459.2" stroke-width="3" stroke-dasharray="9 6"/><line class="s1-line" x1="76.4" y1="351.2" x2="357.2" y2="351.2" stroke-width="3" stroke-dasharray="9 6"/><line class="s3-line" x1="76.4" y1="243.2" x2="357.2" y2="243.2" stroke-width="3" stroke-dasharray="9 6"/><line class="s1-line" x1="76.4" y1="135.2" x2="357.2" y2="135.2" stroke-width="3" stroke-dasharray="9 6"/><line class="s3-line" x1="76.4" y1="27.2" x2="357.2" y2="27.2" stroke-width="3" stroke-dasharray="9 6"/><text class="legend" x="71.0" y="464.2" text-anchor="end" style="font-size:14px">−H</text><text class="legend" x="71.0" y="356.2" text-anchor="end" style="font-size:14px">0</text><text class="legend" x="71.0" y="248.2" text-anchor="end" style="font-size:14px">H</text><text class="legend" x="71.0" y="140.2" text-anchor="end" style="font-size:14px">2H</text><text class="legend" x="71.0" y="32.2" text-anchor="end" style="font-size:14px">3H</text><line class="box-path" x1="90.8" y1="351.2" x2="174.8" y2="243.2" stroke-width="3"/><line class="box-path" x1="174.8" y1="243.2" x2="258.8" y2="351.2" stroke-width="3"/><line class="box-path" x1="258.8" y1="351.2" x2="342.8" y2="243.2" stroke-width="3"/><line class="ink-line" x1="258.8" y1="351.2" x2="342.8" y2="459.2" stroke-width="1.5" stroke-dasharray="4 3"/><line class="box-path" x1="90.8" y1="351.2" x2="342.8" y2="27.2" stroke-width="3" stroke-dasharray="8 5"/><line class="ink-line" x1="342.8" y1="243.2" x2="342.8" y2="459.2" stroke-width="1" stroke-dasharray="2 3"/><line class="ink-line" x1="90.8" y1="351.2" x2="342.8" y2="351.2" stroke-width="1.2"/><line class="ink-line" x1="342.8" y1="351.2" x2="342.8" y2="27.2" stroke-width="1.2"/><text class="legend" x="216.8" y="369.2" text-anchor="middle" style="font-size:15px">L</text><line class="ink-line" x1="90.8" y1="351.2" x2="174.8" y2="351.2" stroke-width="1" stroke-dasharray="3 3"/><line class="ink-line" x1="174.8" y1="351.2" x2="174.8" y2="243.2" stroke-width="1" stroke-dasharray="3 3"/><text class="legend" x="132.8" y="346.2" text-anchor="middle" style="font-size:13px">L/3</text><text class="legend" x="179.8" y="302.2" text-anchor="start" style="font-size:13px">H</text><text class="legend" x="124.8" y="293.2" text-anchor="end" style="font-size:15px">z1</text><line class="ink-line" x1="174.8" y1="243.2" x2="258.8" y2="243.2" stroke-width="1" stroke-dasharray="3 3"/><line class="ink-line" x1="258.8" y1="243.2" x2="258.8" y2="135.2" stroke-width="1" stroke-dasharray="3 3"/><text class="legend" x="216.8" y="238.2" text-anchor="middle" style="font-size:13px">L/3</text><text class="legend" x="263.8" y="194.2" text-anchor="start" style="font-size:13px">H</text><text class="legend" x="208.8" y="185.2" text-anchor="end" style="font-size:15px">z2</text><line class="ink-line" x1="258.8" y1="135.2" x2="342.8" y2="135.2" stroke-width="1" stroke-dasharray="3 3"/><line class="ink-line" x1="342.8" y1="135.2" x2="342.8" y2="27.2" stroke-width="1" stroke-dasharray="3 3"/><text class="legend" x="300.8" y="130.2" text-anchor="middle" style="font-size:13px">L/3</text><text class="legend" x="347.8" y="86.2" text-anchor="start" style="font-size:13px">H</text><text class="legend" x="292.8" y="77.2" text-anchor="end" style="font-size:15px">z3</text><line class="ink-line" x1="368.0" y1="351.2" x2="368.0" y2="27.2" stroke-width="1.2"/><line class="ink-line" x1="362.6" y1="351.2" x2="373.4" y2="351.2" stroke-width="1.2"/><line class="ink-line" x1="362.6" y1="27.2" x2="373.4" y2="27.2" stroke-width="1.2"/><text class="legend" x="374.0" y="194.2" text-anchor="start" style="font-size:14px">2H + b − a</text><circle class="s3-dot" cx="174.8" cy="243.2" r="5"><title>נקודת האוכל</title></circle><circle class="s1-dot" cx="258.8" cy="351.2" r="5"><title>נקודת המים</title></circle><circle class="s1-dot" cx="258.8" cy="135.2" r="4"><title>נקודת המים אחרי השיקוף</title></circle><circle class="ink-dot" cx="90.8" cy="351.2" r="6"><title>החוואי A</title></circle><text class="legend" x="78.8" y="345.2" text-anchor="middle" style="font-size:18px">A</text><circle class="s2-dot" cx="342.8" cy="243.2" r="6"><title>הפרה B</title></circle><text class="legend" x="354.8" y="237.2" text-anchor="middle" style="font-size:18px">B</text><circle class="ink-dot" cx="342.8" cy="459.2" r="4"><title>B′ : השיקוף של B דרך קו המים</title></circle><text class="legend" x="356.8" y="475.2" text-anchor="middle" style="font-size:18px">B′</text><circle class="s2-dot" cx="342.8" cy="27.2" r="6"><title>B″ : השיקוף של B′ דרך קו האוכל</title></circle><text class="legend" x="342.8" y="15.2" text-anchor="middle" style="font-size:18px">B″</text></svg>

    <!-- /gen -->

    **הפתרון יחיד.** הנוסחאות של \( a \) ושל \( b \) נקבעות לגמרי לפי \( x \) ו-\( y \),
    ולכן לכל זוג עצירות יש לכל היותר זוג גבהים אחד. כאן התשובה נמצאת בדיוק על הגבול של
    תנאי הקיום : \( x = y \) נותן \( a = 0 \), ו-\( w = y \) נותן \( b = H \). זו הסיבה
    שבשאלה כתוב שהנקודות נמצאות "בין הקווים או עליהם".

    בתיבה של סעיף א בוחרים "סעיף ב" וגוררים את נקודות העצירה : הגבהים מתעדכנים, והגרירה
    נעצרת בגבול של תנאי הקיום.

---

### סעיף ג – קו האוכל נוטה בזווית

עכשיו הקווים לא מקבילים. קו המים נשאר הקו האופקי \( y = 0 \), וקו האוכל עובר דרך הנקודה
\( (0, H) \) ונוטה כלפי מעלה בזווית \( \theta \), בין 0 ל-60 מעלות. לכן המרחק בין הקווים
גדל משמאל לימין, לכיוון הפרה. בצד שמאל הקווים נפגשים בנקודה
\( O = (-H/\tan\theta, 0) \), משמאל לחוואי.

- **השטח :** שני הקווים מתחילים ב-\( O \) וממשיכים ימינה בלי סוף, והחוואי יכול ללכת בכל
  השטח שביניהם, גם משמאל ל-\( A \). נקודות העצירה יכולות להיות בכל מקום על הקווים.
- **הנקודות :** החוואי ב-\( A = (0, a) \) עם \( 0 \le a \le H \), והפרה ב-\( B = (L, b) \)
  עם \( 0 \le b \le H + L\tan\theta \), כלומר שתיהן בין הקווים או עליהם.
- **המסלול :** כמו קודם, מ-\( A \) לקו האוכל, משם לקו המים ומשם לפרה, בקווים ישרים.

מצאו נוסחה לאורך המסלול הקצר ביותר ולשתי נקודות העצירה, ובדקו מתי השיקוף עדיין נותן את
התשובה. כש-\( \theta = 0 \) זה בדיוק סעיף א.

<!-- gen 5 -->

<svg class="figure" viewBox="0 0 547 198" style="max-width:32rem" role="img" aria-label="סעיף ג : קו המים אופקי, וקו האוכל עובר דרך (0, H) ונוטה כלפי מעלה בזווית θ. הקווים נפגשים בנקודה O משמאל לחוואי ומתרחקים זה מזה לכיוון הפרה. החוואי A בגובה a על הקו x = 0, הפרה B בגובה b על הקו x = L, ומסלול לדוגמה : מ-A לקו האוכל, משם לקו המים ומשם לפרה"><polygon class="box-face" points="25.6,153.0 522.1,153.0 522.1,20.0"/><line class="s1-line" x1="25.6" y1="153.0" x2="532.5" y2="153.0" stroke-width="3" stroke-dasharray="9 6"/><line class="s3-line" x1="25.6" y1="153.0" x2="532.5" y2="17.2" stroke-width="3" stroke-dasharray="9 6"/><path class="farm-arc" d="M 108.8 153.0 A 83.2 83.2 0 0 0 106.0 131.5" stroke-width="1.5"/><text class="legend" x="124.4" y="145.8" text-anchor="start" style="font-size:16px">θ</text><line class="ink-line" x1="316.7" y1="153.0" x2="316.7" y2="75.0" stroke-width="1" stroke-dasharray="2 3"/><line class="ink-line" x1="498.7" y1="153.0" x2="498.7" y2="26.2" stroke-width="1" stroke-dasharray="2 3"/><line class="box-path" x1="316.7" y1="127.0" x2="394.7" y2="54.1" stroke-width="3"/><line class="box-path" x1="394.7" y1="54.1" x2="446.7" y2="153.0" stroke-width="3"/><line class="box-path" x1="446.7" y1="153.0" x2="498.7" y2="101.0" stroke-width="3"/><line class="ink-line" x1="307.6" y1="153.0" x2="307.6" y2="127.0" stroke-width="1.2"/><text class="legend" x="299.6" y="145.0" text-anchor="end" style="font-size:15px">a</text><line class="ink-line" x1="288.1" y1="153.0" x2="288.1" y2="75.0" stroke-width="1.2"/><text class="legend" x="280.1" y="119.0" text-anchor="end" style="font-size:15px">H</text><line class="ink-line" x1="507.8" y1="153.0" x2="507.8" y2="101.0" stroke-width="1.2"/><text class="legend" x="515.8" y="132.0" text-anchor="start" style="font-size:15px">b</text><line class="ink-line" x1="316.7" y1="167.3" x2="498.7" y2="167.3" stroke-width="1.2"/><line class="ink-line" x1="316.7" y1="163.4" x2="316.7" y2="171.2" stroke-width="1.2"/><line class="ink-line" x1="498.7" y1="163.4" x2="498.7" y2="171.2" stroke-width="1.2"/><text class="legend" x="407.7" y="184.3" text-anchor="middle" style="font-size:15px">L</text><circle class="s3-dot" cx="394.7" cy="54.1" r="5"><title>נקודת האוכל</title></circle><circle class="s1-dot" cx="446.7" cy="153.0" r="5"><title>נקודת המים</title></circle><circle class="ink-dot" cx="25.6" cy="153.0" r="5"><title>O : נקודת המפגש של הקווים, (−H/tanθ, 0)</title></circle><text class="legend" x="25.6" y="173.0" text-anchor="middle" style="font-size:18px">O</text><circle class="ink-dot" cx="316.7" cy="127.0" r="6"><title>החוואי A = (0, a)</title></circle><text class="legend" x="329.7" y="120.0" text-anchor="middle" style="font-size:18px">A</text><circle class="s2-dot" cx="498.7" cy="101.0" r="6"><title>הפרה B = (L, b)</title></circle><text class="legend" x="485.7" y="94.0" text-anchor="middle" style="font-size:18px">B</text></svg>

<!-- /gen -->

<!-- gen 6 -->

<span class="viz-legend"><span><i class="s3"></i>קו האוכל, בזווית θ</span><span><i class="s1"></i>קו המים</span><span><i class="box-face"></i>השטח בין הקווים</span><span><i class="ink"></i>החוואי A ונקודת המפגש O</span><span><i class="s2"></i>הפרה B</span><span><i class="box-path"></i>מסלול לדוגמה, לא הקצר ביותר</span></span>

<!-- /gen -->

??? tip "רמז 1"
    שני השיקופים עדיין עובדים : משקפים את \( B \) דרך קו המים, ואת התמונה דרך קו האוכל
    הנטוי. כל מסלול חוקי שווה באורכו לקו שבור מ-\( A \) אל התמונה השנייה. שימו לב שהשיקוף
    דרך קו נטוי הולך בניצב לקו, לא בניצב לציר.

??? tip "רמז 2"
    שני שיקופים דרך קווים שנחתכים ב-\( O \) בזווית \( \theta \) הם סיבוב סביב \( O \)
    בזווית \( 2\theta \). כדי לבדוק שהקו הישר באמת עובר דרך שני הקווים, ובסדר הנכון,
    מסתכלים על הזוויות של הנקודות כפי שרואים אותן מ-\( O \).

<div class="selfcheck" data-answer="106" data-show="106, כלומר z ≈ 10.30" data-hint="עם θ = 45° הזווית 2θ היא 90 מעלות. B1 = (7, −2), והווקטור מ-(0, 3) אל B1 הוא (7, −5). הופכים את הסימן של y ומסובבים : (7, 5) מסובב ב-90 מעלות הוא (−5, 7), ולכן B2 = (−5, 10). z² הוא ריבוע המרחק מ-A = (0, 1) אל B2." markdown>
עם \( L = 7 \), ‏\( H = 3 \), ‏\( a = 1 \), ‏\( b = 2 \) ו-\( \theta = 45^\circ \) : מה הריבוע
\( z^2 \) של אורך המסלול הקצר ביותר?
</div>

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        השיקוף הכפול הוא סיבוב של \( B \) ב-\( 2\theta \) סביב \( O \), והוא נותן את

        \[
        \begin{aligned}
        B_2 = \big(& L\cos 2\theta - (H + b)\sin 2\theta, \\
                   & H + L\sin 2\theta + (H + b)\cos 2\theta\big)
        \end{aligned}
        \]

        המסלול הקצר ביותר הוא \( z = |AB_2| \) :

        \[
        \begin{aligned}
        z^2 = {} & L^2 + (H + b)^2 + (H - a)^2 \\
                 & + 2(H - a)\big(L\sin 2\theta + (H + b)\cos 2\theta\big)
        \end{aligned}
        \]

        נקודת האוכל נמצאת על קו האוכל במרחק \( s \) מ-\( (0, H) \), ונקודת המים היא המקום
        שבו הקו מנקודת האוכל אל \( B_1 = (L, -b) \) חוצה את קו המים. בכל \( \theta \) בין 0
        ל-60 מעלות השיקוף תקף, בלי מקרי קצה.

    <!-- cost: זמן \( O(1) \) | זיכרון \( O(1) \) -->

    #### הרעיון { .sol-idea }

    בסעיף א שני השיקופים דרך שני קווים מקבילים הזיזו את הפרה \( 2H \) כלפי מעלה : זו
    **הזזה**. כשהקווים נחתכים ב-\( O \) בזווית \( \theta \), אותם שני שיקופים הם **סיבוב**
    סביב \( O \) בזווית \( 2\theta \). כל שיקוף שומר על המרחק מ-\( O \), כי \( O \) על הקו,
    והופך את הזווית : הפרה בזווית \( \beta \) עוברת ל-\( -\beta \) דרך קו המים, ואז
    ל-\( 2\theta + \beta \) דרך קו האוכל. לכן \( B_2 \) הוא \( B \) מסובב ב-\( 2\theta \),
    והמסלול הקצר ביותר הוא שוב קו ישר מ-\( A \) אל \( B_2 \). הסעיף מוסיף שאלה שלא הייתה
    בסעיף א : האם הקו הישר באמת חוצה את קו האוכל ואחריו את התמונה של קו המים? כאן עוזרות
    הזוויות סביב \( O \).

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **שיקוף דרך קו המים :** קו המים אופקי, ולכן \( B_1 = (L, -b) \). בדוגמה
       \( L = 7 \), ‏\( H = 3 \), ‏\( a = 1 \), ‏\( b = 2 \), ‏\( \theta = 15^\circ \) מקבלים
       \( B_1 = (7, -2) \).
    2. **שיקוף דרך קו האוכל :** קו האוכל עובר דרך \( C = (0, H) \) בזווית \( \theta \).
       כדי לשקף דרכו מסובבים ב-\( -\theta \) סביב \( C \) כדי שהקו יהיה אופקי, הופכים את
       הסימן של \( y \), ומסובבים בחזרה ב-\( \theta \). שלושת הצעדים יחד הם : הופכים את
       הסימן של \( y \) ומסובבים ב-\( 2\theta \). הווקטור מ-\( C \) אל \( B_1 \) הוא
       \( (L, -(H + b)) \), אחרי היפוך הסימן \( (L, H + b) \), ואחרי הסיבוב

        \[
        \begin{aligned}
        B_2 = \big(& L\cos 2\theta - (H + b)\sin 2\theta, \\
                   & H + L\sin 2\theta + (H + b)\cos 2\theta\big)
        \end{aligned}
        \]

        בדוגמה \( 2\theta = 30^\circ \), ולכן

        \[
        \begin{aligned}
        B_2 &= \big((7\sqrt{3} - 5)/2,\ (13 + 5\sqrt{3})/2\big) \\
            &\approx (3.56,\ 10.83)
        \end{aligned}
        \]

    3. **האורך :** ‏\( z = |AB_2| \). מפתחים את הריבוע של המרחק מ-\( A = (0, a) \) אל
       \( B_2 \), ומשתמשים ב-\( \cos^2 + \sin^2 = 1 \), ומקבלים את הנוסחה של \( z^2 \) שבתשובה
       בקצרה. בדוגמה ‏<span dir="ltr">z² = 49 + 25 + 4 + 4 · (3.5 + 2.5√3) = 92 + 10√3 ≈ 109.32</span>,
       כלומר \( z \approx 10.456 \). בסעיף א, עם קווים מקבילים, היה \( \sqrt{98} \approx 9.90 \) :
       קו האוכל רחוק יותר מהפרה, והדרך ארוכה יותר.
    4. **בדיקה ב-θ = 0 :** ‏\( \sin 0 = 0 \) ו-\( \cos 0 = 1 \), ולכן

        \[
        \begin{aligned}
        z^2 &= L^2 + (H + b)^2 + (H - a)^2 \\
            &\quad + 2(H - a)(H + b) \\
            &= L^2 + (2H + b - a)^2
        \end{aligned}
        \]

        בדיוק הנוסחה של סעיף א. גם \( B_2 \) הופך ל-\( (L, 2H + b) \), התמונה \( B'' \) של סעיף א.
    5. **נקודת האוכל :** הקו מ-\( A \) אל \( B_2 \) חוצה את קו האוכל לפי היחס בין המרחקים
       **הניצבים** של שתי הנקודות מהקו. ‏\( A \) נמצאת \( (H - a)\cos\theta \) מתחת לקו,
       ו-\( B_2 \) נמצאת \( L\sin\theta + (H + b)\cos\theta \) מעליו, כמו \( B_1 \) מתחתיו,
       כי שיקוף שומר על המרחק מהקו. מכאן שנקודת האוכל נמצאת על קו האוכל במרחק

        \[
        s = \frac{(H - a)\big(L\cos 2\theta - (H + b)\sin 2\theta\big)}{L\sin\theta + (2H + b - a)\cos\theta}
        \]

        מ-\( C \), כלומר בנקודה \( P = (s\cos\theta,\ H + s\sin\theta) \). בדוגמה
        \( s = 2(7\sqrt{3} - 5)/(7\sqrt{6}) \approx 0.831 \) ו-\( P \approx (0.80, 3.22) \).
    6. **נקודת המים :** מקפלים בחזרה את השיקוף דרך קו האוכל. אחרי הקיפול הקטע מ-\( P \)
       הולך ישר אל \( B_1 \), ולכן נקודת המים \( Q \) היא המקום שבו הקטע \( PB_1 \) חוצה את
       \( y = 0 \) :
       \( Q_x = P_x + (L - P_x)\,P_y/(P_y + b) \). בדוגמה \( Q \approx (4.62, 0) \).
    7. **התנאי, בזוויות סביב O :** בדוגמה \( O = (-3(2 + \sqrt{3}), 0) \approx (-11.20, 0) \).
       מ-\( O \) רואים את \( A \) בזווית \( \alpha \approx 5.10^\circ \) ואת \( B \) בזווית
       \( \beta \approx 6.27^\circ \), ולכן את \( B_2 \) בזווית \( 2\theta + \beta \approx 36.27^\circ \).
       הקו הישר מסתובב סביב \( O \) רק ב-\( 2\theta + \beta - \alpha \approx 31.17^\circ \), פחות
       מ-180 מעלות, והוא עובר את קו האוכל (בזווית \( \theta \)) ואחריו את התמונה של קו המים
       (בזווית \( 2\theta \)). בהוכחה נראה שזה תמיד כך.

    </div>

    הפרישה של הדוגמה : השטח, השיקוף שלו דרך קו המים, ושני שיקופים דרך קו האוכל. הקשת
    המקווקוות היא הסיבוב של \( B \) סביב \( O \) אל \( B_2 \) :

    <!-- gen 7 -->

    <svg class="figure" viewBox="0 0 509 394" style="max-width:30rem" role="img" aria-label="סעיף ג עם L = 7, H = 3, a = 1, b = 2, θ = 15° : השטח בין הקווים, השיקוף שלו דרך קו המים עם B1, ושני שיקופים דרך קו האוכל, עם תמונת קו המים בזווית 2θ ועם B2. B2 הוא B מסובב ב-2θ = 30° סביב O. הקו הישר מ-A ל-B2 חוצה את קו האוכל בנקודת האוכל ואת תמונת קו המים בתמונה של נקודת המים"><polygon class="box-copy" points="26.8,304.4 26.8,304.4 286.6,374.0 482.7,374.0 482.7,304.4"/><polygon class="box-face" points="26.8,304.4 26.8,304.4 482.7,304.4 482.7,182.2"/><polygon class="box-copy" points="26.8,304.4 26.8,304.4 482.7,182.2 482.7,41.2"/><polygon class="box-copy" points="26.8,304.4 26.8,304.4 482.7,41.2 482.7,16.4 314.8,16.4"/><line class="s3-line" x1="26.8" y1="304.4" x2="286.6" y2="374.0" stroke-width="2" stroke-dasharray="9 6"/><line class="s1-line" x1="26.8" y1="304.4" x2="482.7" y2="304.4" stroke-width="3" stroke-dasharray="9 6"/><line class="s3-line" x1="26.8" y1="304.4" x2="482.7" y2="182.2" stroke-width="3" stroke-dasharray="9 6"/><line class="s1-line" x1="26.8" y1="304.4" x2="482.7" y2="41.2" stroke-width="2" stroke-dasharray="9 6"/><line class="s3-line" x1="26.8" y1="304.4" x2="314.8" y2="16.4" stroke-width="2" stroke-dasharray="9 6"/><path class="farm-arc" d="M 463.5 256.4 A 439.3 439.3 0 0 0 381.0 44.5" stroke-width="1.5" stroke-dasharray="5 4"/><text class="legend" x="444.2" y="145.0" text-anchor="start" style="font-size:16px">2θ</text><path class="farm-arc" d="M 89.2 304.4 A 62.4 62.4 0 0 0 87.1 288.2" stroke-width="1.5"/><text class="legend" x="102.2" y="300.0" text-anchor="start" style="font-size:15px">θ</text><line class="ink-line" x1="463.5" y1="256.4" x2="463.5" y2="352.4" stroke-width="1" stroke-dasharray="2 3"/><line class="ink-line" x1="463.5" y1="352.4" x2="381.0" y2="44.5" stroke-width="1" stroke-dasharray="2 3"/><line class="box-path" x1="295.5" y1="280.4" x2="314.8" y2="227.2" stroke-width="3"/><line class="box-path" x1="314.8" y1="227.2" x2="406.5" y2="304.4" stroke-width="3"/><line class="box-path" x1="406.5" y1="304.4" x2="463.5" y2="256.4" stroke-width="3"/><line class="ink-line" x1="406.5" y1="304.4" x2="463.5" y2="352.4" stroke-width="1.5" stroke-dasharray="4 3"/><line class="box-path" x1="295.5" y1="280.4" x2="381.0" y2="44.5" stroke-width="3" stroke-dasharray="8 5"/><circle class="s3-dot" cx="314.8" cy="227.2" r="5"><title>נקודת האוכל P</title></circle><text class="legend" x="304.8" y="219.2" text-anchor="end" style="font-size:15px">P</text><circle class="s1-dot" cx="406.5" cy="304.4" r="5"><title>נקודת המים Q</title></circle><text class="legend" x="406.5" y="324.4" text-anchor="middle" style="font-size:15px">Q</text><circle class="s1-dot" cx="355.6" cy="114.6" r="4"><title>Q* : התמונה של Q דרך קו האוכל</title></circle><text class="legend" x="365.6" y="118.6" text-anchor="start" style="font-size:15px">Q*</text><circle class="ink-dot" cx="26.8" cy="304.4" r="5"><title>O : נקודת המפגש של הקווים</title></circle><text class="legend" x="26.8" y="324.4" text-anchor="middle" style="font-size:18px">O</text><circle class="ink-dot" cx="295.5" cy="280.4" r="6"><title>החוואי A</title></circle><text class="legend" x="283.5" y="274.4" text-anchor="middle" style="font-size:18px">A</text><circle class="s2-dot" cx="463.5" cy="256.4" r="6"><title>הפרה B</title></circle><text class="legend" x="476.5" y="250.4" text-anchor="middle" style="font-size:18px">B</text><circle class="ink-dot" cx="463.5" cy="352.4" r="4"><title>B1 : השיקוף של B דרך קו המים</title></circle><text class="legend" x="479.5" y="358.4" text-anchor="middle" style="font-size:18px">B1</text><circle class="s2-dot" cx="381.0" cy="44.5" r="6"><title>B2 : השיקוף של B1 דרך קו האוכל, B מסובב ב-2θ סביב O</title></circle><text class="legend" x="381.0" y="32.5" text-anchor="middle" style="font-size:18px">B2</text></svg>

    <!-- /gen -->

    <!-- gen 8 -->

    <span class="viz-legend"><span><i class="s3"></i>קו האוכל ושיקופיו</span><span><i class="s1"></i>קו המים ושיקופיו</span><span><i class="box-face"></i>השטח עצמו</span><span><i class="box-copy"></i>השיקופים שלו</span><span><i class="farm-arc"></i>הסיבוב של B סביב O</span><span><i class="box-path"></i>המסלול הקצר ביותר, והקו הישר מ-A ל-B2</span></span>

    <!-- /gen -->

    שלושת הקטעים של הדוגמה, ואחריהם הקו הישר שהם שווים לו אחרי הפרישה :

    <!-- gen 9 -->

    | הקטע | עד הנקודה | האורך |
    |---|:-:|:-:|
    | מהחוואי \( A \) לאוכל | ‏<span dir="ltr">P = (0.80, 3.22)</span> | ‏<span dir="ltr">z1 ≈ 2.356</span> |
    | מהאוכל למים | ‏<span dir="ltr">Q = (4.62, 0.00)</span> | ‏<span dir="ltr">z2 ≈ 4.993</span> |
    | מהמים לפרה | ‏<span dir="ltr">B = (7.00, 2.00)</span> | ‏<span dir="ltr">z3 ≈ 3.106</span> |
    | הקו הישר מ-\( A \) ל-\( B_2 \) | ‏<span dir="ltr">B2 = (3.56, 10.83)</span> | ‏<span dir="ltr">z ≈ 10.456</span> |

    <!-- /gen -->

    הסכום ‏<span dir="ltr">2.356 + 4.993 + 3.106</span> שווה ל-\( z \approx 10.456 \) עד
    שגיאת העיגול.

    #### הקוד { .sol-code }

    === "Python"
        ```python title="tilted_path" linenums="1" hl_lines="12 13 15 17"
        import math


        def tilted_path(L, H, a, b, theta):
            """The shortest path A -> food line -> water line -> B. The water line is y = 0, the
            food line passes through (0, H) at theta degrees above it (0 <= theta <= 60).
            Returns the length z, the food stop and the water stop, as (x, y) points."""
            t = math.radians(theta)  # (1)!
            assert 0 <= theta <= 60 and 0 <= a <= H and 0 <= b <= H + L * math.tan(t) + 1e-9
            c2, s2 = math.cos(2 * t), math.sin(2 * t)
            u, v = H + b, H - a
            bx, by = L * c2 - u * s2, H + L * s2 + u * c2  # (2)!
            z = math.hypot(bx, by - a)
            den = L * math.sin(t) + (2 * H + b - a) * math.cos(t)
            s = v * (L * c2 - u * s2) / den  # (3)!
            fx, fy = s * math.cos(t), H + s * math.sin(t)
            wx = fx + (L - fx) * fy / (fy + b)  # (4)!
            return z, (fx, fy), (wx, 0.0)
        ```

        1. ‏`math.cos` מקבלת רדיאנים. ‏`math.cos(15)` היא הקוסינוס של 15 רדיאנים, לא של 15
           מעלות.
        2. ‏\( B_2 \) : הווקטור \( (L, H + b) \) מסובב ב-\( 2\theta \), ועוד \( (0, H) \).
        3. המרחק \( s \) של נקודת האוכל מ-\( (0, H) \) לאורך קו האוכל, משלב 5. המכנה חיובי
           תמיד, כי \( 2H + b - a \ge H > 0 \).
        4. החיתוך של הקטע מנקודת האוכל אל \( B_1 = (L, -b) \) עם \( y = 0 \). המכנה
           \( f_y + b \) הוא אפס רק אם נקודת האוכל היא \( O \) והפרה על קו המים, וזה לא קורה.

    === "SystemVerilog"
        ```systemverilog title="function tilted_path" linenums="1" hl_lines="11 14 17 18"
        // The shortest path A -> food line -> water line -> B. The water line is y = 0, the
        // food line passes through (0, H) at theta degrees above it (0 <= theta <= 60).
        // Returns the length z; the food stop is (fx, fy) and the water stop (wx, 0).
        function automatic real tilted_path(real L, real H, real a, real b, real theta,
                                            output real fx, output real fy, output real wx);
          real t, c2, s2, u, v, bx, by, den, s;
          t = theta * 3.14159265358979323846 / 180.0;   // (1)!
          c2 = $cos(2.0 * t);
          s2 = $sin(2.0 * t);
          u = H + b; v = H - a;
          bx = L * c2 - u * s2;                         // (2)!
          by = H + L * s2 + u * c2;
          den = L * $sin(t) + (2.0 * H + b - a) * $cos(t);
          s = v * (L * c2 - u * s2) / den;              // (3)!
          fx = s * $cos(t);
          fy = H + s * $sin(t);
          wx = fx + (L - fx) * fy / (fy + b);           // (4)!
          return $sqrt(bx * bx + (by - a) * (by - a));
        endfunction
        ```

        1. ‏`$cos` ו-`$sin` מקבלות רדיאנים, כמו ב-Python : ממירים את המעלות.
        2. ‏\( B_2 \) : הווקטור \( (L, H + b) \) מסובב ב-\( 2\theta \), ועוד \( (0, H) \).
        3. המרחק \( s \) של נקודת האוכל מ-\( (0, H) \) לאורך קו האוכל, משלב 5.
        4. החיתוך של הקטע מנקודת האוכל אל \( B_1 = (L, -b) \) עם קו המים.

    #### למה זה נכון { .sol-proof }

    **שני שיקופים הם סיבוב.** שיקוף דרך קו שעובר ב-\( O \) לא משנה את המרחק מ-\( O \),
    והופך זווית \( \varphi \) (נמדדת מ-\( O \) מקו המים) ל-\( 2\gamma - \varphi \), כאשר
    \( \gamma \) היא הזווית של הקו. דרך קו המים (\( \gamma = 0 \)) ‏\( \varphi \) עוברת
    ל-\( -\varphi \), ודרך קו האוכל (\( \gamma = \theta \)) היא עוברת ל-\( 2\theta + \varphi \).
    כלומר שני השיקופים יחד הם סיבוב ב-\( 2\theta \) סביב \( O \). כש-\( \theta = 0 \) אין
    נקודת חיתוך : השיקוף דרך \( y = 0 \) ואחריו השיקוף דרך \( y = H \) מעבירים את \( y \)
    ל-\( -y \) ואז ל-\( 2H + y \), הזזה ב-\( 2H \). זה סעיף א, והוא המקרה הגבולי של הסיבוב,
    כש-\( O \) מתרחקת שמאלה בלי סוף.

    **כל מסלול ארוך לפחות כמו \( |AB_2| \).** ניקח מסלול שעוצר באוכל ב-\( P \) ובמים
    ב-\( Q \). השיקוף דרך קו המים נותן \( |QB| = |QB_1| \). השיקוף דרך קו האוכל לא משנה את
    \( P \), ולכן \( |PQ| + |QB_1| = |PQ^*| + |Q^*B_2| \), כאשר \( Q^* \) היא התמונה של
    \( Q \). אורך המסלול הוא \( |AP| + |PQ^*| + |Q^*B_2| \), קו שבור מ-\( A \) אל \( B_2 \),
    ולכן לפחות \( |AB_2| \). החסם הזה נכון בכל זווית.

    **הקו הישר הוא מסלול חוקי.** כדי שהחסם יושג, הקטע \( AB_2 \) צריך לפגוש את קו האוכל
    בנקודה \( P \) ואחריה את התמונה של קו המים, הקרן מ-\( O \) בזווית \( 2\theta \), בנקודה
    \( Q^* \). אז מקפלים בחזרה, ומקבלים מסלול חוקי באורך \( |AB_2| \). מסתכלים מ-\( O \) :
    \( A \) בזווית \( \alpha \) ו-\( B \) בזווית \( \beta \), שתיהן בין 0 ל-\( \theta \)
    כי הנקודות בין הקווים, ולכן \( B_2 \) בזווית \( 2\theta + \beta \). קטע שלא עובר
    ב-\( O \) נראה ממנה בזווית קטנה מ-180 מעלות, והכיוון אליו משתנה לאורכו בלי לחזור
    אחורה. כאן ההפרש בין הזוויות של הקצוות הוא

    \[
    2\theta + \beta - \alpha \le 3\theta \le 180^\circ
    \]

    ולכן הקטע עובר בדיוק את הזוויות מ-\( \alpha \) עד \( 2\theta + \beta \), בכיוון הזה :
    קודם את \( \theta \), קו האוכל, ואחר כך את \( 2\theta \), התמונה של קו המים. לכן
    **ל-θ בין 0 ל-60 מעלות השיקוף תקף תמיד**, וזה המקור של הגבול 60 : שלוש פעמים 60 הן 180.
    השוויון \( 2\theta + \beta - \alpha = 180^\circ \) קורה רק כש-\( \theta = 60^\circ \), החוואי על
    קו המים והפרה על קו האוכל. אז \( A \), ‏\( O \) ו-\( B_2 \) על קו אחד, והמסלול עובר
    דרך \( O \) עצמה ונוגע בה בשני הקווים, באורך \( |OA| + |OB| = |AB_2| \).

    **נקודת עצירה משמאל לחוואי.** ‏\( s < 0 \) בדיוק כש-\( L\cos 2\theta < (H + b)\sin 2\theta \),
    כלומר כש-\( B_2 \) משמאל לציר \( x = 0 \). בדוגמה זה קורה מ-\( \theta \approx 27.2^\circ \) :
    ב-\( \theta = 30^\circ \) נקודת האוכל ב-\( x \approx -0.15 \). זה מותר, כי הקווים ממשיכים
    שמאלה עד \( O \). אם הייתה גדר ב-\( x = 0 \), התשובה הייתה אחרת (ראו את שאלות ההמשך).

    **בדיקה מספרית.** הבדיקות של העמוד משוות את הנוסחאות לחיפוש מספרי של שתי נקודות העצירה,
    באלפי מקרים אקראיים של \( L \), ‏\( H \), ‏\( a \), ‏\( b \) ו-\( \theta \) עד 60 מעלות,
    ובזוויות שבהן \( \cos\theta \) ו-\( \sin\theta \) רציונליים (כמו 3/5 ו-4/5) הן בודקות
    בחשבון מדויק שהנקודות על הקווים ושהקטעים על קו ישר אחד.

    #### סיבוכיות { .sol-cost }

    - **חישוב :** ‏\( O(1) \), כמה פונקציות טריגונומטריות ושורש אחד.
    - **בלי חיפוש :** אין צורך לבדוק מקרי קצה, כי התנאי מתקיים תמיד בתחום של השאלה.

    **נסו בעצמכם.** בתיבה הבאה משנים את \( \theta \) במחוון או בשדה, וגוררים את החוואי ואת
    הפרה לאורך הדפנות. "הצגת השיקוף" מוסיפה את שלושת השיקופים של השטח, את \( B_1 \) ואת
    \( B_2 \), ואת הקשת של הסיבוב סביב \( O \). קנה המידה של הציור קבוע בזמן שמשנים את
    \( \theta \), כדי שאפשר יהיה לראות איך \( B_2 \) מסתובב.

    <div class="explorer" data-kind="farm" data-mode="c" data-l="7" data-h="3" data-a="1" data-b="2" data-t="15"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : לשקף רק פעם אחת"
    שיקוף אחד של הפרה דרך קו המים פותר בעיה עם עצירה אחת בלבד. כאן יש שתי עצירות, ולכן
    צריך שני שיקופים : את התמונה \( B' \) משקפים שוב דרך קו האוכל. מי שמשקף את \( B \)
    ישירות דרך קו האוכל מקבל גובה \( 2H - b \), וזה לא נכון.

??? trap "מלכודת : לשכוח את התנאי b ≤ H"
    מהנוסחה \( b = Hw/y \) קל לבדוק רק ש-\( b \ge 0 \). אבל הפרה חייבת להיות מתחת לקו האוכל
    או עליו, ולכן צריך גם \( w \le y \). בלי התנאי הזה נראה שיש פתרון גם כשהקטע האחרון
    ארוך מהאמצעי.

??? trap "מלכודת : לגזור במקום לשקף"
    אפשר לכתוב את אורך המסלול כפונקציה של שתי נקודות העצירה ולגזור, אבל מקבלים שתי
    משוואות עם שורשים. השיקוף נותן את התשובה בשורה אחת, וגם מוכיח שזה המינימום.

??? trap "מלכודת : לשקף בסדר ההפוך"
    בסעיף ג הסדר של השיקופים חשוב. מי שמשקף את \( B \) קודם דרך קו האוכל ואחר כך דרך קו
    המים מסובב אותו ב-\( -2\theta \) במקום ב-\( 2\theta \), ופותר את הבעיה של "קודם מים
    ואחר כך אוכל". השיקוף הראשון הוא דרך הקו האחרון שהמסלול נוגע בו לפני הפרה.

??? trap "מלכודת : מרחק אנכי במקום מרחק ניצב"
    שיקוף דרך קו האוכל הנטוי הולך בניצב לקו. מי שמשקף את \( B_1 = (L, -b) \) בקו אנכי,
    כאילו הקו אופקי בגובה \( H + L\tan\theta \), מקבל נקודה מעל \( B \) בדיוק, בגובה
    \( 2H + 2L\tan\theta + b \), וזה לא נכון כש-\( \theta > 0 \). המרחק הנכון של
    \( B_1 \) מהקו הוא \( L\sin\theta + (H + b)\cos\theta \), לא \( H + b + L\tan\theta \).

??? trap "מלכודת : מעלות ורדיאנים"
    ‏`math.cos(15)` ב-Python ו-`$cos(15)` ב-SystemVerilog מחשבות קוסינוס של 15 רדיאנים. בלי
    המרה ל-\( \theta\pi/180 \) מקבלים מספר סביר למראה ושגוי לגמרי.

??? followup "שאלות המשך"
    - **קודם מים ואחר כך אוכל :** מה המסלול הקצר ביותר?

        ??? fu-answer "תשובה"
            משקפים קודם דרך קו האוכל ואז דרך קו המים. הקו הישר עולה \( a + H + (H - b) \), ולכן
            \( D = 2H + a - b \) ו-\( z = \sqrt{L^2 + (2H + a - b)^2} \).

    - **סדר חופשי :** אם מותר לבחור את הסדר, איזה סדר עדיף?

        ??? fu-answer "תשובה"
            הסדר שבו \( D \) קטן יותר : אוכל קודם כש-\( a \ge b \), ומים קודם כש-\( a < b \).
            בשני המקרים \( D = 2H - |a - b| \).

    - **שלוש עצירות :** אוכל, מים ושוב אוכל. כמה שיקופים צריך, ואיפה תהיה התמונה האחרונה?

        ??? fu-answer "תשובה"
            שלושה שיקופים, אחד לכל עצירה. הקו עולה \( (H - a) + H + H + (H - b) \), ולכן
            \( D = 4H - a - b \) והתמונה האחרונה בגובה \( 4H - b \).

    - **קווים מתכנסים :** קו האוכל יורד לכיוון הפרה, כלומר \( \theta < 0 \). מה משתנה, ומתי
      השטח נסגר לפני הפרה?

        ??? fu-answer "תשובה"
            אותן נוסחאות עם \( \theta \) שלילי : הקווים נפגשים מימין, ב-\( x = H/\tan|\theta| \),
            והשיקוף הכפול מסובב את הפרה ב-\( 2|\theta| \) בכיוון השעון סביב הנקודה הזו. אותו
            טיעון של זוויות מראה שהשיקוף תקף כל עוד \( |\theta| \le 60^\circ \). הפרה בשטח רק
            כש-\( 0 \le b \le H - L\tan|\theta| \), ולכן כש-\( L\tan|\theta| \ge H \) הקווים
            נפגשים לפני הפרה או בדיוק אצלה, והשטח נסגר.

    - **זווית גדולה מ-60 מעלות :** מה קורה כש-\( 2\theta + \beta - \alpha > 180^\circ \)?

        ??? fu-answer "תשובה"
            הקו הישר מ-\( A \) אל \( B_2 \) עובר מהצד השני של \( O \), ולא חוצה את הקווים
            בסדר הנכון. אז המסלול הקצר ביותר עובר דרך \( O \) עצמה, נוגע שם בשני הקווים,
            ואורכו \( |OA| + |OB| \), יותר מ-\( |AB_2| \). זה המקרה היחיד שבו השיקוף לא נותן
            את התשובה, והוא דורש \( \theta > 60^\circ \).

    - **גדר ב-x = 0 :** אם אסור לעצור משמאל לחוואי, מה התשובה כש-\( s < 0 \)?

        ??? fu-answer "תשובה"
            הפונקציה של אורך המסלול קמורה, ולכן כשהמינימום בלי הגדר נמצא משמאל לה, המינימום
            עם הגדר נמצא על הגדר : לוקחים אוכל ב-\( (0, H) \), ישר מעל החוואי, וממשיכים בשיקוף
            אחד. האורך הוא \( (H - a) + \sqrt{L^2 + (H + b)^2} \).
