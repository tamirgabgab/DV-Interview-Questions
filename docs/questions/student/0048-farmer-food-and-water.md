---
id: 48
title: החוואי, האוכל והמים
level: student
difficulty: medium
kind: math
tags: [math, geometry, logic-puzzles]
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

    - **קווים לא מקבילים :** מה משתנה כשהקווים נחתכים בזווית?

        ??? fu-answer "תשובה"
            שני שיקופים דרך קווים נחתכים הם סיבוב סביב נקודת החיתוך, בזווית כפולה מהזווית
            ביניהם. מסובבים את הפרה, והמסלול הקצר ביותר הוא שוב קו ישר אל התמונה, כל עוד הוא
            חוצה את שני הקווים בסדר הנכון.
