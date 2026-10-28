---
id: 26
title: שלושה אנשים ואופנוע אחד – הדרך המהירה להגיע יחד
level: junior
difficulty: easy
kind: puzzle
tags: [math, logic-puzzles]
source: ""
added: 2026-10-19
---

## השאלה

שלושה חברים נמצאים בנקודה \( A \) וצריכים להגיע לנקודה \( B \). יש להם אופנוע אחד, שיכול
לשאת **לכל היותר שני אנשים** : נהג ונוסע. מי שאינו על האופנוע הולך ברגל.

- **הליכה :** הליכה של כל הדרך מ-\( A \) ל-\( B \) אורכת **13 שעות**.
- **נסיעה :** נסיעה באופנוע של כל הדרך אורכת **שעה אחת**, עם נוסע או בלי.
- **ההנחות :** המהירויות קבועות, אפשר ללכת ולנסוע בשני הכיוונים, ועלייה, ירידה ופניית פרסה
  לא לוקחות זמן. האופנוע לא זז בלי נהג. המרחק \( AB \) לא ידוע.

מהו הזמן הקצר ביותר שבו **שלושתם** נמצאים ב-\( B \)? תארו את התוכנית : מי נוסע, מי הולך, ואיפה
כל אחד עולה על האופנוע ויורד ממנו.

ולבסוף, הכלילו : אם הליכה של כל הדרך אורכת \( t_0 \) ונסיעה של כל הדרך אורכת \( t_1 \),
מהו הזמן הקצר ביותר?

??? interviewer "מה המראיין בודק"
    - **מודל לפני חישוב :** להגדיר מהירויות ויחס ביניהן, ולראות שהמרחק הלא ידוע לא נחוץ.
    - **שיפור בשלבים :** להתחיל מתוכנית פשוטה, לשאול מי מבזבז בה זמן, ולתקן.
    - **משוואות תנועה :** בכל שלב שני אנשים זזים אותו זמן במהירויות שונות, ופגישה של שניים
      שנעים זה לקראת זה.
    - **בדיקת שפיות :** לבדוק את הנוסחה הכללית במקרי קצה, ואת התשובה בדרך שנייה.

---

??? tip "רמז 1"
    בתוכנית הפשוטה הנהג מסיע את הראשון עד \( B \) וחוזר לאסוף את השני. מי מחכה בתוכנית
    הזו בלי לזוז, ואיך אפשר לנצל את הזמן הזה?

??? tip "רמז 2"
    תנו לנוסע לרדת **לפני** \( B \) ולהמשיך ברגל, בזמן שהאופנוע חוזר לאסוף את השלישי. את
    נקודת הירידה בוחרים כך ששלושתם מגיעים ל-\( B \) באותו רגע.

??? tip "רמז 3"
    חלקו את התנועה לשלושה שלבים : נסיעה קדימה, חזרה ונסיעה קדימה. בכל שלב, מי שנוסע ומי
    שהולך זזים אותו זמן, וזו משוואה אחת. נוח לעבוד עם יחס המהירויות
    \( \alpha = v_1 / v_0 = 13 \).

<div class="selfcheck" data-answer="2.5" data-show="2.5" data-hint="כולם מגיעים יחד, ולכן כל אחד רוכב אותו מרחק. הנהג מוריד את הנוסע לפני B, חוזר לאסוף את מי שהולך, ושניהם מגיעים יחד עם הנוסע." markdown>
מהו הזמן הקצר ביותר, בשעות, שבו שלושתם ב-B?
</div>

??? success "פתרון"
    !!! answer "תשובה בקצרה"
        שעתיים וחצי. הנהג מסיע את הנוסע \( \tfrac78 \) מהדרך, חוזר לאסוף את השלישי שהלך
        בינתיים ומסיע אותו ל-\( B \), והנוסע מגיע ברגל באותו רגע. באופן כללי
        \( T = \dfrac{3t_0 + t_1}{t_0 + 3t_1}\, t_1 \).

    #### הרעיון { .sol-idea }

    נקרא לשלושה **הנהג**, **הנוסע** ו**ההולך**. התוכנית הראשונה שעולה בראש : הנהג מסיע את
    הנוסע עד \( B \), חוזר ריק ל-\( A \) ומסיע את ההולך. זה לוקח 3 שעות, וההולך מבזבז
    שעתיים בהמתנה. אם ההולך יוצא לדרך בזמן הזה, האופנוע פוגש אותו מוקדם יותר, והזמן יורד
    לכ-2.71 שעות. אבל עכשיו הנוסע מגיע ראשון ויושב ב-\( B \) בלי לעשות כלום.

    המסקנה : **אף אחד לא צריך לחכות**. הנוסע יורד לפני \( B \) וממשיך ברגל, האופנוע חוזר
    מוקדם יותר אל ההולך, ובוחרים את נקודת הירידה כך ששלושתם מגיעים ל-\( B \) יחד. ככה
    אף דקה של אף אחד לא מתבזבזת, והזמן יורד לשעתיים וחצי :

    <!-- gen 0 -->

    | האסטרטגיה | הזמן הכללי | כש-\( \alpha = 13 \) |
    |---|---|---|
    | השני מחכה ב-\( A \) | ‏\( 3\,t_1 \) | ‏\( 3 \) שעות |
    | השני הולך בינתיים | ‏\( \dfrac{3\alpha - 1}{\alpha + 1}\, t_1 \) | ‏\( \tfrac{19}{7} \approx 2.714 \) שעות |
    | הנוסע יורד בדרך | ‏\( \dfrac{3\alpha + 1}{\alpha + 3}\, t_1 \) | ‏\( 2.5 \) שעות |

    <!-- /gen -->

    <!-- gen 1 -->

    <svg class="perf-chart" viewBox="0 0 560 150" style="max-width:35rem" role="img" aria-label="הזמן של שלוש האסטרטגיות : 3 שעות כשהשני מחכה, כ-2.71 שעות כשהוא הולך בינתיים, ו-2.5 שעות כשהנוסע יורד בדרך"><line class="grid" x1="24.0" x2="24.0" y1="6" y2="130"/><text class="tick" x="24.0" y="146" text-anchor="middle">0</text><line class="grid" x1="182.7" x2="182.7" y1="6" y2="130"/><text class="tick" x="182.7" y="146" text-anchor="middle">1</text><line class="grid" x1="341.3" x2="341.3" y1="6" y2="130"/><text class="tick" x="341.3" y="146" text-anchor="middle">2</text><line class="grid" x1="500.0" x2="500.0" y1="6" y2="130"/><text class="tick" x="500.0" y="146" text-anchor="middle">3</text><rect class="bar by-multiples" x="24" y="10" width="476.0" height="28" rx="3"><title>3</title></rect><text class="legend" x="508.0" y="29">3</text><rect class="bar by-enum" x="24" y="50" width="430.7" height="28" rx="3"><title>2.714</title></rect><text class="legend" x="462.7" y="69">2.714</text><rect class="bar by-bfs" x="24" y="90" width="396.7" height="28" rx="3"><title>2.5</title></rect><text class="legend" x="428.7" y="109">2.5</text><line class="axis" x1="24" x2="510" y1="130" y2="130"/><text class="tick" x="524" y="146" text-anchor="middle">t</text></svg>

    <!-- /gen -->

    <!-- gen 2 -->

    <span class="viz-legend"><span><i class="by-multiples"></i>השני מחכה ב-\( A \)</span><span><i class="by-enum"></i>השני הולך בינתיים</span><span><i class="by-bfs"></i>הנוסע יורד בדרך</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    נסמן את מהירות ההליכה ב-\( v_0 \), את מהירות האופנוע ב-\( v_1 \), ואת היחס ביניהן
    ב-\( \alpha \). זמני הדרך כולה הם \( t_0 = AB / v_0 \) ו-\( t_1 = AB / v_1 \), ולכן

    \[
    \alpha = \frac{v_1}{v_0} = \frac{t_0}{t_1} = \frac{13}{1} = 13
    \]

    התוכנית מחלקת את הדרך לחמישה קטעים, \( y, x, z, x, r \), ואת הזמן לשלושה שלבים. בין
    הקטעים יש ארבע נקודות, לפי הסדר מ-\( A \) : ‏\( Q \) הוא המקום של ההולך ברגע שהנוסע
    יורד, \( C \) המקום שבו האופנוע אוסף את ההולך, \( D \) המקום שבו הנוסע יורד, ו-\( E \)
    המקום של הנוסע ברגע שההולך עולה. בשרטוט (סכמטי), כל שורה היא שלב, והחצים מראים מי זז
    ולאן :

    <!-- gen 3 -->

    <svg class="figure" viewBox="0 0 640 228" style="max-width:40rem" role="img" aria-label="הדרך מ-A ל-B עם הנקודות Q, C, D, E והקטעים y, x, z, x, r, ומתחתיה שלושת השלבים : מי נוסע ומי הולך בכל שלב"><defs><marker id="q26-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q26-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q26-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="ink-line" x1="40.0" y1="50" x2="610.0" y2="50" stroke-width="2"/><line class="axis-c" x1="43.0" y1="36" x2="138.8" y2="36" stroke-width="1"/><text class="legend" x="90.9" y="30" text-anchor="middle" font-style="italic" style="font-size:20px">y</text><line class="axis-c" x1="144.8" y1="36" x2="199.9" y2="36" stroke-width="1"/><text class="legend" x="172.3" y="30" text-anchor="middle" font-style="italic" style="font-size:20px">x</text><line class="axis-c" x1="205.9" y1="36" x2="444.1" y2="36" stroke-width="1"/><text class="legend" x="325.0" y="30" text-anchor="middle" font-style="italic" style="font-size:20px">z</text><line class="axis-c" x1="450.1" y1="36" x2="505.2" y2="36" stroke-width="1"/><text class="legend" x="477.7" y="30" text-anchor="middle" font-style="italic" style="font-size:20px">x</text><line class="axis-c" x1="511.2" y1="36" x2="607.0" y2="36" stroke-width="1"/><text class="legend" x="559.1" y="30" text-anchor="middle" font-style="italic" style="font-size:20px">r</text><line class="axis-c" x1="40.0" y1="43" x2="40.0" y2="57"/><text class="legend" x="40.0" y="78" text-anchor="middle" style="font-size:20px">A</text><line class="axis-c" x1="141.8" y1="43" x2="141.8" y2="57"/><text class="legend" x="141.8" y="78" text-anchor="middle" style="font-size:20px">Q</text><line class="axis-c" x1="202.9" y1="43" x2="202.9" y2="57"/><text class="legend" x="202.9" y="78" text-anchor="middle" style="font-size:20px">C</text><line class="axis-c" x1="447.1" y1="43" x2="447.1" y2="57"/><text class="legend" x="447.1" y="78" text-anchor="middle" style="font-size:20px">D</text><line class="axis-c" x1="508.2" y1="43" x2="508.2" y2="57"/><text class="legend" x="508.2" y="78" text-anchor="middle" style="font-size:20px">E</text><line class="axis-c" x1="610.0" y1="43" x2="610.0" y2="57"/><text class="legend" x="610.0" y="78" text-anchor="middle" style="font-size:20px">B</text><text class="legend" x="18" y="115" text-anchor="middle" style="font-size:20px">1</text><line class="ink-line" x1="42.0" y1="101" x2="445.1" y2="101" stroke-width="3" marker-end="url(#q26-ink)"/><line class="s2-line" x1="42.0" y1="115" x2="139.8" y2="115" stroke-width="2" marker-end="url(#q26-s2)"/><text class="legend" x="18" y="155" text-anchor="middle" style="font-size:20px">2</text><line class="ink-line" x1="445.1" y1="141" x2="204.9" y2="141" stroke-width="3" marker-end="url(#q26-ink)"/><line class="s1-line" x1="449.1" y1="155" x2="506.2" y2="155" stroke-width="2" marker-end="url(#q26-s1)"/><line class="s2-line" x1="143.8" y1="155" x2="200.9" y2="155" stroke-width="2" marker-end="url(#q26-s2)"/><text class="legend" x="18" y="195" text-anchor="middle" style="font-size:20px">3</text><line class="ink-line" x1="204.9" y1="181" x2="608.0" y2="181" stroke-width="3" marker-end="url(#q26-ink)"/><line class="s1-line" x1="510.2" y1="195" x2="608.0" y2="195" stroke-width="2" marker-end="url(#q26-s1)"/></svg>

    <!-- /gen -->

    <!-- gen 4 -->

    <span class="viz-legend"><span><i class="ink"></i>האופנוע (הנהג, ואיתו נוסע או לא)</span><span><i class="s1"></i>הנוסע הולך ברגל</span><span><i class="s2"></i>ההולך הולך ברגל</span></span>

    <!-- /gen -->

    <div class="steps" markdown>

    1. **שלב 1, נסיעה ל-\( D \) :** הנהג והנוסע נוסעים מ-\( A \) עד \( D \), מרחק
       \( y + x + z \). באותו זמן ההולך עובר \( y \) ומגיע ל-\( Q \) :

        \[
        \begin{aligned}
        \frac{y}{v_0} &= \frac{y + x + z}{v_1} \\
        \alpha y &= y + x + z
        \end{aligned}
        \tag{1}
        \]

    2. **שלב 2, חזרה ל-\( C \) :** הנוסע יורד ב-\( D \) וממשיך ברגל. הנהג חוזר מרחק
       \( z \) ופוגש את ההולך ב-\( C \), אחרי שההולך עבר \( x \) מ-\( Q \) :

        \[
        \begin{aligned}
        \frac{x}{v_0} &= \frac{z}{v_1} \\
        z &= \alpha x
        \end{aligned}
        \tag{2}
        \]

        באותו זמן גם הנוסע הולך, ולכן גם הוא עובר \( x \), מ-\( D \) עד \( E \).

    3. **שלב 3, נסיעה ל-\( B \) :** הנהג אוסף את ההולך ונוסע מ-\( C \) עד \( B \), מרחק
       \( z + x + r \). באותו זמן הנוסע עובר ברגל את \( r \) שנשאר לו :

        \[
        \begin{aligned}
        \frac{r}{v_0} &= \frac{z + x + r}{v_1} \\
        \alpha r &= z + x + r
        \end{aligned}
        \tag{3}
        \]

    4. **מציבים את \( z = \alpha x \) :** משוואות 1 ו-3 נותנות את אותה תוצאה :

        \[
        \begin{aligned}
        \alpha y = y + x + \alpha x \quad&\Longrightarrow\quad y = \frac{\alpha + 1}{\alpha - 1}\, x \\
        \alpha r = r + x + \alpha x \quad&\Longrightarrow\quad r = \frac{\alpha + 1}{\alpha - 1}\, x
        \end{aligned}
        \]

        כלומר \( y = r \) : הסימטריה יוצאת לבד. ההולך הולך \( y + x \) בהתחלה, והנוסע הולך
        \( x + r \) בסוף, אותו מרחק בדיוק.

    5. **אורך הדרך :** מחברים את חמשת הקטעים ומציבים :

        \[
        \begin{aligned}
        AB &= y + x + z + x + r = 2x + 2y + \alpha x \\
           &= \left(2 + \alpha + \frac{2(\alpha + 1)}{\alpha - 1}\right) x \\
           &= \frac{\alpha(\alpha + 3)}{\alpha - 1}\, x
        \end{aligned}
        \]

        ומכאן כל הקטעים, כחלק מ-\( AB \) :

        \[
        \begin{aligned}
        x &= \frac{\alpha - 1}{\alpha(\alpha + 3)}\, AB \\
        y = r &= \frac{\alpha + 1}{\alpha(\alpha + 3)}\, AB \\
        z &= \frac{\alpha - 1}{\alpha + 3}\, AB
        \end{aligned}
        \]

    6. **הזמן הכולל :** הכי קל לחשב אותו דרך ההולך. הוא הולך \( y + x \) ונוסע את השאר :

        \[
        \begin{aligned}
        y + x &= \frac{(\alpha + 1) + (\alpha - 1)}{\alpha(\alpha + 3)}\, AB \\
              &= \frac{2}{\alpha + 3}\, AB \\
        T &= \frac{2}{\alpha + 3}\, t_0 + \frac{\alpha + 1}{\alpha + 3}\, t_1 \\
          &= \frac{2\alpha + \alpha + 1}{\alpha + 3}\, t_1
           = \frac{3\alpha + 1}{\alpha + 3}\, t_1
        \end{aligned}
        \]

        עם \( \alpha = t_0 / t_1 \), כופלים מונה ומכנה ב-\( t_1 \) ומקבלים נוסחה שתלויה רק
        בזמנים, בלי המרחק :

        \[
        T = \frac{3t_0 + t_1}{t_0 + 3t_1}\, t_1
        \]

    7. **מציבים את המספרים :** ‏\( t_0 = 13 \) ו-\( t_1 = 1 \) :

        \[
        T = \frac{3 \cdot 13 + 1}{13 + 3 \cdot 1} = \frac{40}{16} = 2.5
        \]

        כלומר שעתיים וחצי.

    </div>

    #### למה זה נכון { .sol-proof }

    **בדיקה דרך האופנוע.** האופנוע לא עוצר אף פעם : קדימה \( y + x + z \), אחורה \( z \),
    ושוב קדימה \( z + x + r \). עם \( y = r \) הוא עובר בסך הכול \( 2x + 2y + 3z \), ואחרי
    הצבה של הקטעים :

    \[
    \begin{aligned}
    T &= \frac{2x + 2y + 3z}{v_1} \\
      &= \frac{2(\alpha - 1) + 2(\alpha + 1) + 3\alpha(\alpha - 1)}{\alpha(\alpha + 3)} \cdot \frac{AB}{v_1} \\
      &= \frac{3\alpha^2 + \alpha}{\alpha(\alpha + 3)}\, t_1
       = \frac{3\alpha + 1}{\alpha + 3}\, t_1
    \end{aligned}
    \]

    אותה תוצאה כמו דרך ההולך, כמו שצריך : האופנוע וההולך מגיעים ל-\( B \) יחד.

    **למה הנוסע יורד דווקא שם.** נניח \( AB = 1 \) ו-\( t_1 = 1 \), והנוסע יורד במרחק \( d \)
    מ-\( A \). הוא מגיע ל-\( B \) אחרי \( d + \alpha (1 - d) \), זמן שיורד ככל ש-\( d \) גדל.
    ההולך מגיע אחרי \( 1 + \frac{2(\alpha - 1)}{\alpha + 1}\, d \), זמן שעולה עם \( d \) : ככל
    שהאופנוע מרחיק, הדרך חזרה אל ההולך ארוכה יותר. כולם ב-\( B \) כשהמאוחר מהשניים מגיע,
    והמקסימום של קו יורד וקו עולה הכי נמוך בדיוק בנקודה שבה הם נפגשים :
    \( d = \frac{\alpha + 1}{\alpha + 3} = \tfrac78 \), ושם שניהם מגיעים אחרי 2.5 שעות.

    **למה אין תוכנית מהירה יותר.** הבדיקות עד כאן מראות שהתוכנית עקבית, לא שאין טובה
    ממנה. הנה חסם לכל תוכנית, ב-\( AB = 1 \) ו-\( t_1 = 1 \). נסמן ב-\( f_i \) וב-\( b_i \)
    את המרחק שאדם \( i \) רוכב קדימה ואחורה, וב-\( M_f \) וב-\( M_b \) את המרחק שהאופנוע
    נוסע קדימה ואחורה. אפשר להניח שאף אחד לא עובר את \( B \) : אם מחליפים כל מקום מעבר
    ל-\( B \) ב-\( B \) עצמו, התוכנית נשארת חוקית ולא מתארכת.

    - **כל אדם :** הוא רוכב \( f_i + b_i \) שעות, ונשאר לו ללכת לפחות \( 1 - f_i + b_i \), ולכן
      \( T \ge f_i + b_i + \alpha (1 - f_i + b_i) \).
    - **מי על האופנוע :** לכל היותר שניים, ותמיד נהג. לכן \( \sum f_i \le 2M_f \)
      ו-\( \sum b_i \ge M_b \). והאופנוע מסיים לכל היותר ב-\( B \), כלומר \( M_b \ge M_f - 1 \).
    - **הזמן של האופנוע :** הוא עובר \( M_f + M_b \ge 2M_f - 1 \) במהירות 1 בתוך \( T \), ולכן
      \( M_f \le \frac{T + 1}{2} \).

    מחברים את שלושת החסמים של האנשים. ב-\( \alpha \ge 1 \) המקדם של \( \sum f_i \) לא חיובי
    והמקדם של \( \sum b_i \) חיובי, ולכן מותר להציב את שני החסמים :

    \[
    \begin{aligned}
    3T &\ge 3\alpha + (1 - \alpha) \textstyle\sum f_i + (1 + \alpha) \sum b_i \\
       &\ge 3\alpha + 2(1 - \alpha) M_f + (1 + \alpha)(M_f - 1) \\
       &= 2\alpha - 1 + (3 - \alpha) M_f \\
       &\ge 2\alpha - 1 + (3 - \alpha)\, \tfrac{T + 1}{2}
    \end{aligned}
    \]

    הצעד האחרון נכון כש-\( \alpha \ge 3 \), כי אז \( 3 - \alpha \le 0 \). מסדרים ומקבלים
    \( (\alpha + 3)\, T \ge 3\alpha + 1 \), כלומר \( T \ge \frac{3\alpha + 1}{\alpha + 3}\, t_1 \),
    שעתיים וחצי עבור \( \alpha = 13 \). החסם לא מניח כלום על מי נוהג ומתי, ולכן הוא מכסה גם
    החלפת נהגים, נסיעה אחורה עם נוסע ואופנוע שעומד בצד. והתוכנית שלנו משיגה שוויון בכל
    צעד : קדימה תמיד שניים על האופנוע, אחורה רק הנהג, האופנוע לא עוצר ומסיים ב-\( B \),
    ואף אחד לא הולך אחורה.

    **התוכנית על גרף.** בגרף, הציר האופקי הוא הזמן בשעות והציר האנכי הוא המקום על הדרך :
    0 הוא \( A \) ו-1 הוא \( B \). השיפוע של קו הוא המהירות : קו תלול הוא נסיעה, וקו כמעט
    שטוח הוא הליכה. בשלב 1 הנוסע נוסע על האופנוע, ולכן הקו שלו מכסה את קו האופנוע. בשלב 3
    ההולך על האופנוע. נקודה שבה שני קווים נפגשים היא פגישה על הדרך :

    <!-- gen 5 -->

    <svg class="perf-chart" viewBox="0 0 640 320" role="img" aria-label="המקום של האופנוע ושל שני האנשים שאינם נוהגים כפונקציה של הזמן : האופנוע נוסע קדימה, חוזר ונוסע שוב קדימה, ושלושתם מגיעים ל-B יחד אחרי 2.5 שעות"><defs><marker id="q26-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q26-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q26-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><line class="grid" x1="52" x2="616" y1="286.0" y2="286.0"/><text class="tick" x="44" y="290.0" text-anchor="end">0</text><line class="grid" x1="52" x2="616" y1="254.5" y2="254.5"/><text class="tick" x="44" y="258.5" text-anchor="end">1/8</text><line class="grid" x1="52" x2="616" y1="65.5" y2="65.5"/><text class="tick" x="44" y="69.5" text-anchor="end">7/8</text><line class="grid" x1="52" x2="616" y1="34.0" y2="34.0"/><text class="tick" x="44" y="38.0" text-anchor="end">1</text><line class="grid" x1="52.0" x2="52.0" y1="28" y2="286" stroke-dasharray="4 4"/><text class="tick" x="52.0" y="304" text-anchor="middle">0</text><line class="grid" x1="249.4" x2="249.4" y1="28" y2="286" stroke-dasharray="4 4"/><text class="tick" x="249.4" y="304" text-anchor="middle">0.875</text><line class="grid" x1="418.6" x2="418.6" y1="28" y2="286" stroke-dasharray="4 4"/><text class="tick" x="418.6" y="304" text-anchor="middle">1.625</text><line class="grid" x1="616.0" x2="616.0" y1="28" y2="286" stroke-dasharray="4 4"/><text class="tick" x="616.0" y="304" text-anchor="middle">2.5</text><text class="legend" x="150.7" y="20" text-anchor="middle" direction="rtl">שלב 1</text><text class="legend" x="334.0" y="20" text-anchor="middle" direction="rtl">שלב 2</text><text class="legend" x="517.3" y="20" text-anchor="middle" direction="rtl">שלב 3</text><polyline class="ink-line" points="52.0,286.0 249.4,65.5 418.6,254.5 616.0,34.0" fill="none" stroke-width="7" stroke-opacity="0.28" stroke-linejoin="round"/><polyline class="s1-line" points="52.0,286.0 249.4,65.5 418.6,51.0 616.0,34.0" fill="none" stroke-width="2.5"/><polyline class="s2-line" points="52.0,286.0 249.4,269.0 418.6,254.5 616.0,34.0" fill="none" stroke-width="2.5"/><circle class="s2-dot" cx="249.4" cy="269.0" r="5"><title>Q : ההולך כשהנוסע יורד, t = 0.875</title></circle><text class="legend" x="249.4" y="259.0" text-anchor="middle" style="font-size:17px">Q</text><circle class="s1-dot" cx="249.4" cy="65.5" r="5"><title>D : הנוסע יורד, t = 0.875</title></circle><text class="legend" x="249.4" y="53.5" text-anchor="middle" style="font-size:17px">D</text><circle class="s2-dot" cx="418.6" cy="254.5" r="5"><title>C : האופנוע אוסף את ההולך, t = 1.625</title></circle><text class="legend" x="418.6" y="276.5" text-anchor="middle" style="font-size:17px">C</text><circle class="s1-dot" cx="418.6" cy="51.0" r="5"><title>E : הנוסע כשההולך עולה, t = 1.625</title></circle><text class="legend" x="418.6" y="39.0" text-anchor="middle" style="font-size:17px">E</text><circle class="ink-dot" cx="616.0" cy="34.0" r="5"><title>B : שלושתם מגיעים, t = 2.5</title></circle><text class="legend" x="600.0" y="28.0" text-anchor="middle" style="font-size:17px">B</text><line class="axis" x1="52" x2="616" y1="286" y2="286"/><text class="tick" x="630" y="290" text-anchor="middle">t</text></svg>

    <!-- /gen -->

    <!-- gen 6 -->

    <span class="viz-legend"><span><i class="ink" style="opacity:0.4"></i>האופנוע</span><span><i class="s1"></i>הנוסע</span><span><i class="s2"></i>ההולך</span></span>

    <!-- /gen -->

    בגרף רואים את הסימטריה : הקטע השטוח של ההולך בהתחלה ושל הנוסע בסוף מקבילים ושווים.
    אותם מספרים בטבלה :

    <!-- gen 7 -->

    | שלב | השעות | האופנוע | הנוסע | ההולך |
    |---|---|---|---|---|
    | שלב 1 | ‏0 עד 0.875 | ‏\( A \to D \) | על האופנוע | ‏\( A \to Q \) |
    | שלב 2 | ‏0.875 עד 1.625 | ‏\( D \to C \) | ‏\( D \to E \) | ‏\( Q \to C \) |
    | שלב 3 | ‏1.625 עד 2.5 | ‏\( C \to B \) | ‏\( E \to B \) | על האופנוע |

    <!-- /gen -->

    ובמקומות על הדרך, עם \( \alpha = 13 \) :

    <!-- gen 8 -->

    | הנקודה | המרחק מ-\( A \) | מה קורה שם |
    |---|---|---|
    | ‏\( Q \) | ‏\( \tfrac{7}{104}\,AB \approx 0.067\,AB \) | ההולך, כשהנוסע יורד מהאופנוע |
    | ‏\( C \) | ‏\( \tfrac{1}{8}\,AB \approx 0.125\,AB \) | האופנוע אוסף את ההולך |
    | ‏\( D \) | ‏\( \tfrac{7}{8}\,AB \approx 0.875\,AB \) | הנוסע יורד מהאופנוע |
    | ‏\( E \) | ‏\( \tfrac{97}{104}\,AB \approx 0.933\,AB \) | הנוסע, כשהאופנוע אוסף את ההולך |

    <!-- /gen -->

    כל אחד מהשניים הולך \( \tfrac18 \) מהדרך, שעה ו-37.5 דקות, ונוסע \( \tfrac78 \) מהדרך,
    52.5 דקות. בסך הכול שעתיים וחצי לכל אחד.

    **מקרי קצה.** הנוסחה \( T = \frac{3\alpha + 1}{\alpha + 3}\, t_1 \) מתנהגת כמו שצריך :

    - **אופנוע איטי :** כש-\( \alpha \to 1 \) האופנוע לא מהיר מהליכה, ו-\( T \to t_1 = t_0 \).
      אין טעם באופנוע, כולם פשוט הולכים.
    - **אופנוע מהיר מאוד :** כש-\( \alpha \to \infty \) ההליכה זניחה, ו-\( T \to 3t_1 \).
      האופנוע עובר את הדרך שלוש פעמים : קדימה, אחורה וקדימה.
    - **תמיד מהר יותר מהליכה :** ‏\( T < t_0 = \alpha t_1 \) כי
      \( 3\alpha + 1 < \alpha^2 + 3\alpha \), כלומר \( \alpha^2 > 1 \).

    **דוגמה נוספת.** ‏\( AB = 360 \) ק"מ, האופנוע נוסע 60 קמ"ש וההליכה 15 קמ"ש. אז
    \( \alpha = 4 \) ו-\( t_1 = 6 \) שעות, והזמן הוא
    \( T = \frac{13}{7} \cdot 6 = \frac{78}{7} \approx 11.14 \) שעות, לעומת 24 שעות ברגל.

    **נסו בעצמכם.** לחצו על "הפעלה" וראו את שלושת האנשים זזים על הדרך בזמן שהגרף מצטייר :
    האופנוע נוסע קדימה, חוזר ונוסע שוב, והשניים הולכים בקטעים השטוחים. פס הזמן מזיז את התמונה
    ביד, ובבחירת התוכנית אפשר להשוות לשתי התוכניות הפשוטות, שבהן מישהו מחכה. הזיזו את זמן ההליכה
    ואת זמן הנסיעה, וראו איך נקודת הירידה \( D \), נקודת המפגש \( C \) והזמן הכולל זזים. שאלות
    ההמשך גם כאן : הסליידר "כמה צריכים הסעה" מכליל לארבעה אנשים ויותר (כל נוסע נוסע אותו מרחק,
    וכולם מגיעים יחד לפי הנוסחה), שדה המרחק בק"מ מתרגם למהירויות ולקילומטרים של כל אחד,
    ו"להשוואה עם" מצייר תוכנית שנייה מקווקות על אותו גרף, ואומר מי מחכה בה ב-\( B \) וכמה זמן.
    בשלב ההוכחה, בתחתית התיבה, מזיזים את נקודת הירידה \( D \) : הקו של הנוסע יורד, הקו של ההולך
    עולה, והמאוחר מביניהם הכי קטן בדיוק כשהם נפגשים, ב-\( \tfrac78 \) :

    <div class="explorer" data-kind="motorcycle" data-t0="13" data-t1="1"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : להסיע את הנוסע עד הסוף"
    התוכנית "להסיע אחד, לחזור, להסיע את השני" נשמעת יעילה, אבל בה הנוסע מגיע ראשון
    ומחכה. כל זמן המתנה של מישהו הוא זמן שאפשר היה לנצל להליכה. בתוכנית הטובה ביותר
    שלושתם מגיעים יחד.

??? trap "מלכודת : לשכוח שההולך לא עומד במקום"
    בזמן שהאופנוע חוזר, ההולך ממשיך ללכת לקראתו. הם מתקרבים זה לזה במהירות
    \( v_1 + v_0 \), ולא במהירות \( v_1 \). מי שמחשב את נקודת המפגש כאילו ההולך עדיין
    ב-\( Q \) מקבל אותה רחוק מדי לאחור. משוואה 2 עושה את זה נכון : שניהם זזים אותו זמן.

??? trap "מלכודת : לחפש את המרחק"
    המרחק \( AB \) לא ידוע, ולא צריך אותו. כל הקטעים הם חלק ממנו, והזמן תלוי רק ביחס
    \( \alpha = t_0 / t_1 \). אפשר גם פשוט להגדיר \( AB = 1 \).

??? followup "שאלות המשך"
    - **מספרים :** אם המרחק הוא 52 ק"מ, מה המהירויות, וכמה ק"מ הולך כל אחד מהשניים?

        ??? fu-answer "תשובה"
            הליכה 4 ק"מ לשעה ונסיעה 52 ק"מ לשעה. כל אחד מהשניים נוסע \( \tfrac78 \) מהדרך, 45.5
            ק"מ, והולך 6.5 ק"מ, והזמן נשאר שעתיים וחצי.

    - **איפה הנוסע יורד :** הראו שהנוסע יורד במרחק \( \frac{\alpha + 1}{\alpha + 3}\, AB \)
      מ-\( A \), ובדקו שעבור \( \alpha = 13 \) זה \( \tfrac78 \) מהדרך.

        ??? fu-answer "תשובה"
            הנוסע וההולך מגיעים יחד, ולכן כל אחד מהם נוסע אותו מרחק \( x \). ב-\( AB = 1 \)
            ו-\( t_1 = 1 \) האופנוע זז כל הזמן : קדימה \( x \), אחורה \( 2x - 1 \) עד ההולך,
            וקדימה \( x \), סך הכול \( 4x - 1 \), וזה שווה לזמן \( x + \alpha (1 - x) \).
            מכאן \( x = \frac{\alpha + 1}{\alpha + 3} \),
            ועבור \( \alpha = 13 \) : \( \tfrac{14}{16} = \tfrac78 \).

    - **ארבעה אנשים :** אותו אופנוע, ושלושה צריכים הסעה. הראו שהזמן הקצר ביותר הוא
      \( \frac{5\alpha + 1}{\alpha + 5}\, t_1 \), כלומר שלוש שעות ו-40 דקות עבור
      \( \alpha = 13 \). רמז : כל אחד מהשלושה נוסע אותו מרחק.

        ??? fu-answer "תשובה"
            כל אחד מהשלושה נוסע \( x \). האופנוע נוסע קדימה \( 3x \) ואחורה \( 3x - 1 \), סך
            הכול \( 6x - 1 \), וזה שווה ל-\( x + \alpha (1 - x) \).
            לכן \( x = \frac{\alpha + 1}{\alpha + 5} = \tfrac79 \),
            והזמן \( 6x - 1 = \tfrac{11}{3} \) שעות, כלומר שלוש שעות ו-40 דקות.

    - **הכללה :** עם \( n \) אנשים שצריכים הסעה, הראו שהזמן הוא
      \( \frac{(2n - 1)\alpha + 1}{\alpha + 2n - 1}\, t_1 \). מה קורה כש-\( n \) גדל?

        ??? fu-answer "תשובה"
            אותו חשבון עם \( 2nx - 1 \) נותן \( x = \frac{\alpha + 1}{\alpha + 2n - 1} \) ואת
            הזמן שבשאלה. כש-\( n \) גדל, \( x \to 0 \) והזמן שואף ל-\( \alpha t_1 = t_0 \) : כל
            אחד הולך כמעט את כל הדרך, והאופנוע כמעט לא עוזר.

    - **למה אין מהר יותר :** הוכיחו שאין תוכנית מהירה יותר, בהנחה שהנהג קבוע. כיוון :
      האופנוע חייב לנסוע קדימה לפחות את סכום הנסיעות של השניים, וכל אחד מהם הולך את מה
      שלא נסע. שני החסמים נפגשים בדיוק בתשובה.

        ??? fu-answer "תשובה"
            נסמן ב-\( r \) את הקטן מבין מרחקי הנסיעה קדימה של השניים (ב-\( AB = 1 \)
            ו-\( t_1 = 1 \)). האופנוע נוסע קדימה לפחות \( 2r \), מתקדם נטו 1 ועובר לכל
            היותר \( T \), ולכן \( T \ge 4r - 1 \). מי שנסע \( r \) הולך לפחות \( 1 - r \),
            ולכן \( T \ge r + \alpha (1 - r) \). החסם הראשון עולה ב-\( r \) והשני יורד,
            ולכן \( T \) לפחות ערך החיתוך, \( \frac{3\alpha + 1}{\alpha + 3} \).
