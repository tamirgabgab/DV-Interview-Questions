---
id: 43
title: מרוצי סוסים בלי שעון – כמה תחרויות עד ארבעת המהירים
level: junior
difficulty: medium
kind: puzzle
tags: [logic, algorithms, sorting, python, systemverilog]
source: "חידת 25 הסוסים הקלאסית (5 במסלול, שלושת הראשונים, 7 תחרויות); כאן 36 סוסים וארבעה ראשונים, ואז 30 סוסים והתוכנית הכללית"
added: 2026-10-23
---

## השאלה

באורווה **36 סוסים**, ולכל סוס מהירות קבועה שאינה ידועה. במסלול רצים **6 סוסים** בכל
תחרות, ואין שעון עצר : בסוף תחרות רואים רק את **סדר ההגעה**. מהו מספר התחרויות הקטן
ביותר שמבטיח למצוא את **ארבעת הסוסים המהירים ביותר, לפי הסדר**?

??? interviewer "מה המראיין בודק"
    - **מה תחרות נותנת :** לא "מי הכי מהיר", אלא סדר מלא בין 6 סוסים, שממנו נובעים גם
      יחסים עקיפים (אם A1 ניצח את B1 ו-B1 ניצח את B2, אז A1 מהיר מ-B2 בלי שרצו יחד).
    - **מי יוצא ולמה :** סוס שידועים לפחות 4 מהירים ממנו לא יכול להיות בארבעת הראשונים.
      המועמד צריך לספור "כמה ידועים מהירים ממני", לא "באיזה מקום הגעתי".
    - **העצירה הנכונה :** המנצח של הקבוצה השנייה לא בהכרח מקום 2 : המקום השני בקבוצה
      הטובה יכול להיות מהיר ממנו.
    - **חסם תחתון :** לא רק תוכנית שמסיימת ב-9, אלא למה 8 לא מספיקות.
    - **הכללה :** בסעיף ב, האם אותו רעיון עובד כשמספר הסוסים אינו ריבוע, והאם המועמד
      יכול לנסח אותו כאלגוריתם שמחשב בעצמו את התחרות הבאה.

---

### סעיף א – 36 סוסים, 6 במסלול, ארבעת הראשונים

כמה תחרויות צריך, ואילו סוסים רצים בכל אחת?

??? tip "רמז 1"
    כל סוס חייב לרוץ לפחות פעם אחת, אחרת הוא יכול להיות המהיר ביותר ואף אחד לא ידע. זה
    כבר 6 תחרויות של קבוצות. מה יודעים אחריהן?

??? tip "רמז 2"
    מריצים את ששת מנצחי הקבוצות. עכשיו, לסוס שהגיע במקום \( i \) בקבוצתו, וקבוצתו
    היא זו שהמנצח שלה הגיע במקום \( j \) בתחרות המנצחים, ידועים לפחות \( (i - 1) + (j - 1) \)
    סוסים מהירים ממנו. מי נשאר עם פחות מ-4?

??? tip "רמז 3"
    נשארים 9 מועמדים למקומות 2, 3 ו-4. המועמדים למקום 2 הם רק שניים, ולמקום 3 חמישה.
    איזו תחרות של 6 מכריעה את מקומות 2 ו-3 בבת אחת, ומה נשאר לתחרות האחרונה?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏**9 תחרויות.** שש תחרויות של קבוצות, תחרות של ששת המנצחים (שקובעת את מקום 1
        ומשאירה 9 מועמדים למקומות 2 עד 4), תחרות שמינית של ששת המועמדים עם הכי הרבה
        השוואות חסרות (שמכריעה את מקומות 2 ו-3), ותחרות תשיעית קצרה על מקום 4. פחות
        מ-9 לא מספיק.

    <!-- cost: תחרויות 9 -->

    #### הרעיון { .sol-idea }

    **מה ידוע אחרי תחרות.** נשמור לכל סוס את קבוצת הסוסים שידוע שהם מהירים ממנו, כולל
    עקיפים : אם \( x \) ניצח את \( y \) ו-\( y \) ניצח את \( z \), אז \( x \) מהיר מ-\( z \).
    סוס עם **4 או יותר** מהירים ידועים לא יכול להיות בארבעת הראשונים ויוצא מהמשחק. סוס
    שהמהירים ממנו והאיטיים ממנו מצטרפים ל-35 "נקבע" : הדירוג שלו ידוע בדיוק.

    **הקבוצות והמנצחים.** נסמן את הקבוצות לפי תוצאת תחרות המנצחים : A היא הקבוצה של
    המנצח הכללי, B זו שהמנצח שלה הגיע שני, וכך הלאה; A1 הוא מנצח A, A2 השני בה. אחרי
    7 תחרויות, לסוס במקום \( i \) בקבוצה \( j \) (שניהם מ-1) ידועים \( (i - 1) + (j - 1) \)
    מהירים : \( i - 1 \) בקבוצתו, ו-\( j - 1 \) מנצחים שמהירים ממנצח קבוצתו. A1 הוא מקום 1,
    ונשארים בדיוק המקומות עם \( (i - 1) + (j - 1) \le 3 \) : תשעה מועמדים, מדרגות :

    <!-- gen 0 -->

    | מקום בקבוצה \ המנצח הגיע | 1 | 2 | 3 | 4 | 5 | 6 |
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏1 | ‏0 (מקום 1) | ‏**1** ✓ | ‏**2** ✓ | ‏**3** ✓ | ‏4 ✗ | ‏5 ✗ |
    | ‏2 | ‏**1** ✓ | ‏**2** ✓ | ‏**3** ✓ | ‏4 ✗ | ‏5 ✗ | ‏6 ✗ |
    | ‏3 | ‏**2** ✓ | ‏**3** ✓ | ‏4 ✗ | ‏5 ✗ | ‏6 ✗ | ‏7 ✗ |
    | ‏4 | ‏**3** ✓ | ‏4 ✗ | ‏5 ✗ | ‏6 ✗ | ‏7 ✗ | ‏8 ✗ |
    | ‏5 | ‏4 ✗ | ‏5 ✗ | ‏6 ✗ | ‏7 ✗ | ‏8 ✗ | ‏9 ✗ |
    | ‏6 | ‏5 ✗ | ‏6 ✗ | ‏7 ✗ | ‏8 ✗ | ‏9 ✗ | ‏10 ✗ |

    <!-- /gen -->

    **המדרגות.** למקום 2 מועמדים רק A2 ו-B1 (מהיר ידוע אחד בלבד). למקום 3 מצטרפים A3, B2
    ו-C1. למקום 4 מצטרפים A4, B3, C2 ו-D1. כל השאר, 26 סוסים, יצאו.

    **שתי התחרויות האחרונות.** תחרות 8 מריצה את ששת המועמדים שביניהם הכי הרבה זוגות
    שעוד לא הושוו : A2, B1, A3, B2, C1 ו-D1. כל המועמדים למקומות 2 ו-3 נמצאים בה, ולכן
    שני הראשונים בה הם מקומות 2 ו-3. למקום 4 נשארים השלישי בתחרות 8 ומי מבין A4, B3,
    C2 שעדיין יש לו פחות מ-4 מהירים ידועים : לכל היותר ארבעה סוסים, ותחרות 9 מכריעה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **תחרויות 1 עד 6 :** שש קבוצות של 6. בכל קבוצה המקומות 5 ו-6 יוצאים מיד (ארבעה
       מהירים ידועים).
    2. **תחרות 7 :** ששת המנצחים. המנצח הוא מקום 1. קבוצות E ו-F יוצאות כולן, וכך גם
       D2 ומטה, C3 ומטה, B4 ומטה ו-A5 ומטה. נשארו 9 :

        <!-- gen 1 -->

        <svg class="figure hr-grid" viewBox="0 0 464 280" style="max-width:29rem" role="img" aria-label="הסוסים אחרי 7 תחרויות : שורה לכל קבוצה לפי סדר המנצחים, תא ירוק נקבע, כחול מועמד, אפור נפסל"><text class="tick" x="102" y="20" text-anchor="middle">1</text><text class="tick" x="166" y="20" text-anchor="middle">2</text><text class="tick" x="230" y="20" text-anchor="middle">3</text><text class="tick" x="294" y="20" text-anchor="middle">4</text><text class="tick" x="358" y="20" text-anchor="middle">5</text><text class="tick" x="422" y="20" text-anchor="middle">6</text><text class="tick" x="62" y="54" text-anchor="end">C (1)</text><g class="hr-cell is-placed"><rect x="72" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="55" text-anchor="middle">C1</text><text class="hr-count" x="128" y="43" text-anchor="end">0</text></g><g class="hr-cell is-cand"><rect x="136" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="55" text-anchor="middle">C2</text><text class="hr-count" x="192" y="43" text-anchor="end">1</text></g><g class="hr-cell is-cand"><rect x="200" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="55" text-anchor="middle">C3</text><text class="hr-count" x="256" y="43" text-anchor="end">2</text></g><g class="hr-cell is-cand"><rect x="264" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="55" text-anchor="middle">C4</text><text class="hr-count" x="320" y="43" text-anchor="end">3</text></g><g class="hr-cell is-out"><rect x="328" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="55" text-anchor="middle">C5</text><text class="hr-count" x="384" y="43" text-anchor="end">4</text></g><g class="hr-cell is-out"><rect x="392" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="55" text-anchor="middle">C6</text><text class="hr-count" x="448" y="43" text-anchor="end">5</text></g><text class="tick" x="62" y="94" text-anchor="end">F (2)</text><g class="hr-cell is-cand"><rect x="72" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="95" text-anchor="middle">F1</text><text class="hr-count" x="128" y="83" text-anchor="end">1</text></g><g class="hr-cell is-cand"><rect x="136" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="95" text-anchor="middle">F2</text><text class="hr-count" x="192" y="83" text-anchor="end">2</text></g><g class="hr-cell is-cand"><rect x="200" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="95" text-anchor="middle">F3</text><text class="hr-count" x="256" y="83" text-anchor="end">3</text></g><g class="hr-cell is-out"><rect x="264" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="95" text-anchor="middle">F4</text><text class="hr-count" x="320" y="83" text-anchor="end">4</text></g><g class="hr-cell is-out"><rect x="328" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="95" text-anchor="middle">F5</text><text class="hr-count" x="384" y="83" text-anchor="end">5</text></g><g class="hr-cell is-out"><rect x="392" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="95" text-anchor="middle">F6</text><text class="hr-count" x="448" y="83" text-anchor="end">6</text></g><text class="tick" x="62" y="134" text-anchor="end">B (3)</text><g class="hr-cell is-cand"><rect x="72" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="135" text-anchor="middle">B1</text><text class="hr-count" x="128" y="123" text-anchor="end">2</text></g><g class="hr-cell is-cand"><rect x="136" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="135" text-anchor="middle">B2</text><text class="hr-count" x="192" y="123" text-anchor="end">3</text></g><g class="hr-cell is-out"><rect x="200" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="135" text-anchor="middle">B3</text><text class="hr-count" x="256" y="123" text-anchor="end">4</text></g><g class="hr-cell is-out"><rect x="264" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="135" text-anchor="middle">B4</text><text class="hr-count" x="320" y="123" text-anchor="end">5</text></g><g class="hr-cell is-out"><rect x="328" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="135" text-anchor="middle">B5</text><text class="hr-count" x="384" y="123" text-anchor="end">6</text></g><g class="hr-cell is-out"><rect x="392" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="135" text-anchor="middle">B6</text><text class="hr-count" x="448" y="123" text-anchor="end">7</text></g><text class="tick" x="62" y="174" text-anchor="end">E (4)</text><g class="hr-cell is-cand"><rect x="72" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="175" text-anchor="middle">E1</text><text class="hr-count" x="128" y="163" text-anchor="end">3</text></g><g class="hr-cell is-out"><rect x="136" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="175" text-anchor="middle">E2</text><text class="hr-count" x="192" y="163" text-anchor="end">4</text></g><g class="hr-cell is-out"><rect x="200" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="175" text-anchor="middle">E3</text><text class="hr-count" x="256" y="163" text-anchor="end">5</text></g><g class="hr-cell is-out"><rect x="264" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="175" text-anchor="middle">E4</text><text class="hr-count" x="320" y="163" text-anchor="end">6</text></g><g class="hr-cell is-out"><rect x="328" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="175" text-anchor="middle">E5</text><text class="hr-count" x="384" y="163" text-anchor="end">7</text></g><g class="hr-cell is-out"><rect x="392" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="175" text-anchor="middle">E6</text><text class="hr-count" x="448" y="163" text-anchor="end">8</text></g><text class="tick" x="62" y="214" text-anchor="end">D (5)</text><g class="hr-cell is-out"><rect x="72" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="215" text-anchor="middle">D1</text><text class="hr-count" x="128" y="203" text-anchor="end">4</text></g><g class="hr-cell is-out"><rect x="136" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="215" text-anchor="middle">D2</text><text class="hr-count" x="192" y="203" text-anchor="end">5</text></g><g class="hr-cell is-out"><rect x="200" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="215" text-anchor="middle">D3</text><text class="hr-count" x="256" y="203" text-anchor="end">6</text></g><g class="hr-cell is-out"><rect x="264" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="215" text-anchor="middle">D4</text><text class="hr-count" x="320" y="203" text-anchor="end">7</text></g><g class="hr-cell is-out"><rect x="328" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="215" text-anchor="middle">D5</text><text class="hr-count" x="384" y="203" text-anchor="end">8</text></g><g class="hr-cell is-out"><rect x="392" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="215" text-anchor="middle">D6</text><text class="hr-count" x="448" y="203" text-anchor="end">9</text></g><text class="tick" x="62" y="254" text-anchor="end">A (6)</text><g class="hr-cell is-out"><rect x="72" y="232" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="255" text-anchor="middle">A1</text><text class="hr-count" x="128" y="243" text-anchor="end">5</text></g><g class="hr-cell is-out"><rect x="136" y="232" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="255" text-anchor="middle">A2</text><text class="hr-count" x="192" y="243" text-anchor="end">6</text></g><g class="hr-cell is-out"><rect x="200" y="232" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="255" text-anchor="middle">A3</text><text class="hr-count" x="256" y="243" text-anchor="end">7</text></g><g class="hr-cell is-out"><rect x="264" y="232" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="255" text-anchor="middle">A4</text><text class="hr-count" x="320" y="243" text-anchor="end">8</text></g><g class="hr-cell is-out"><rect x="328" y="232" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="255" text-anchor="middle">A5</text><text class="hr-count" x="384" y="243" text-anchor="end">9</text></g><g class="hr-cell is-out"><rect x="392" y="232" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="255" text-anchor="middle">A6</text><text class="hr-count" x="448" y="243" text-anchor="end">10</text></g></svg>

        <!-- /gen -->

        <!-- gen 2 -->

        <span class="viz-legend"><span><i class="hr-key-placed"></i>נקבע : הדירוג המדויק ידוע</span><span><i class="hr-key-cand"></i>מועמד : פחות מ-c מהירים ידועים</span><span><i class="hr-key-out"></i>נפסל : לפחות c מהירים ידועים (המספר בפינה)</span></span>

        <!-- /gen -->

    3. **תחרות 8 :** ‏A2, B1, A3, B2, C1, D1. שני הראשונים הם מקומות 2 ו-3; השלישי הוא
       מועמד למקום 4.
    4. **תחרות 9 :** השלישי של תחרות 8 נגד מי שנשאר עם פחות מ-4 מהירים ידועים מבין A4,
       B3 ו-C2. הראשון הוא מקום 4.
    5. **דוגמה מוגרלת.** הקבוצות שומרות על השמות המקוריים (A עד F לפי הסדר באורווה,
       המספר לפי המקום בקבוצה), והמנצח הכללי כאן הוא C1. בכל שורה : מי נפסל ולמה, ומי
       נקבע :

        <!-- gen 3 -->

        | תחרות | מי רץ | התוצאה | נפסלו (ולמה) | נקבעו | עוד פתוחים |
        |:-:|---|---|---|---|:-:|
        | ‏1 | ‏קבוצה A | ‏A1 > A2 > A3 > A4 > A5 > A6 | ‏2 : A5, A6 | ‏— | ‏34 |
        | ‏2 | ‏קבוצה B | ‏B1 > B2 > B3 > B4 > B5 > B6 | ‏2 : B5, B6 | ‏— | ‏32 |
        | ‏3 | ‏קבוצה C | ‏C1 > C2 > C3 > C4 > C5 > C6 | ‏2 : C5, C6 | ‏— | ‏30 |
        | ‏4 | ‏קבוצה D | ‏D1 > D2 > D3 > D4 > D5 > D6 | ‏2 : D5, D6 | ‏— | ‏28 |
        | ‏5 | ‏קבוצה E | ‏E1 > E2 > E3 > E4 > E5 > E6 | ‏2 : E5, E6 | ‏— | ‏26 |
        | ‏6 | ‏קבוצה F | ‏F1 > F2 > F3 > F4 > F5 > F6 | ‏2 : F5, F6 | ‏— | ‏24 |
        | ‏7 | ‏A1, B1, C1, D1, E1, F1 | ‏C1 > F1 > B1 > E1 > D1 > A1 | ‏14 : A1, A2, A3, A4, B3, B4, D1, D2, D3, D4, E2, E3, E4, F4 | ‏C1 מקום 1 | ‏9 |
        | ‏8 | ‏F1, C2, B1, F2, C3, E1 | ‏F1 > F2 > B1 > E1 > C2 > C3 | ‏B2 (B1, C1, F1, F2); C2 (B1, C1, E1, F2 ועוד 1); C3 (B1, C1, C2, E1 ועוד 2); C4 (B1, C1, C2, C3 ועוד 3); E1 (B1, C1, F1, F2) | ‏F1 מקום 2, F2 מקום 3 | ‏2 |
        | ‏9 | ‏B1, F3 | ‏B1 > F3 | ‏F3 (B1, C1, F1, F2) | ‏B1 מקום 4 | ‏0 |

        <!-- /gen -->

    </div>

    #### למה זה נכון { .sol-proof }

    **כל יציאה מוצדקת.** סוס יוצא רק כשידועים 4 סוסים מהירים ממנו, וכל ידיעה כזו היא
    שרשרת של תוצאות תחרויות. לכן ארבעת הראשונים לעולם לא יוצאים, ומי שנקבע במקום
    \( r \) באמת מהיר מ-\( 36 - r \) סוסים ואיטי מ-\( r - 1 \).

    **תחרות 8 מכריעה את מקומות 2 ו-3.** כל סוס שיכול להיות מקום 2 או 3 אחרי תחרות 7 הוא
    אחד מ-A2, B1, A3, B2, C1 (למקום 3 צריך לכל היותר 2 מהירים ידועים, וזו בדיוק הרשימה
    עם \( (i - 1) + (j - 1) \le 2 \)). כולם רצים בתחרות 8, ולכן הסדר ביניהם ידוע במלואו,
    ושני הראשונים הם מקומות 2 ו-3.

    **תחרות 9 קצרה.** אחרי תחרות 8 המועמדים למקום 4 הם השלישי בה ומי מבין A4, B3, C2
    שעדיין לא נפסל. A4 נפסל אם A3 הפסיד למישהו נוסף, B3 אם B2 הפסיד, C2 אם C1 הפסיד;
    לכל היותר שלושה שורדים, והתחרות התשיעית מדרגת אותם מול השלישי.

    **ולמה 8 לא מספיקות (טיעון יריב).** נניח תוכנית של 8 תחרויות. כל סוס חייב לרוץ,
    וזה דורש 6 תחרויות לפחות; כדי שידע מישהו מי מקום 1, מנצחי הקבוצות חייבים להיפגש,
    והיריב מסדר את תחרות המנצחים כרצונו. אחרי 7 תחרויות, בכל תוכנית, נשארים לפחות 9
    סוסים שלכל אחד מהם ידועים לכל היותר 3 מהירים, ושהיחסים ביניהם ידועים רק בתוך שורה
    (אותה קבוצה) ובתוך העמודה הראשונה (המנצחים). תחרות אחת מריצה 6 מהם ומשאירה 3 בחוץ.
    היריב בוחר את תוצאת התחרות כך שאחד מהסוסים שבחוץ נשאר עם בדיוק 3 מהירים ידועים :
    הוא לא רץ נגד הסוס שסיים רביעי בין המועמדים, ושום שרשרת לא מחברת ביניהם. שני סוסים
    שמעולם לא הושוו, לא ישירות ולא דרך שרשרת, אפשר לסדר בשני האופנים, ולכן מקום 4 לא
    נקבע. אם התוכנית לא מתחילה בשש קבוצות זרות, יש סוס שלא רץ עד התחרות השביעית, והיריב
    משאיר אותו ואת מי שאחריו באותו מצב.

    **נסו בעצמכם.** התיבה מגרילה מהירויות (נסתרות, כמו בחידה), מריצה תחרות אחרי תחרות,
    צובעת את הסוסים ברשת (נפסל, מועמד, נקבע) ומסבירה בכל תחרות מי נפסל ולמה. מתג "חשיפת
    המהירויות" מראה את הדירוג האמיתי לבדיקה. בשלב ההוכחה לוחצים על סוס : הרשת מסמנת את
    הסוסים שידוע שהם מהירים ממנו ואת החצים של התוצאות שמוכיחות את זה, והטבלה מסמנת את
    התחרויות שבשרשרת :

    <div class="explorer" data-kind="horses" data-fixed="1" data-a="36" data-b="6" data-c="4" data-seed="3"></div>

    #### סיבוכיות { .sol-cost }

    ‏9 תחרויות, ואין פחות. במונחי מידע : 36 סוסים ו-4 ראשונים לפי הסדר הם
    \( 36 \cdot 35 \cdot 34 \cdot 33 \approx 1.4 \cdot 10^6 \) תשובות אפשריות, ותחרות של 6
    נותנת לכל היותר \( 6! = 720 \) תוצאות, ולכן לפחות 3 תחרויות גם עם שעון; בלי שעון
    המבנה (כל סוס רץ, המנצחים נפגשים, המדרגות) מעלה את החסם ל-9.

---

### סעיף ב – 30 סוסים, 6 במסלול, שלושת הראשונים : והתוכנית הכללית { #general }

באורווה אחרת 30 סוסים, המסלול עדיין ל-6, וצריך את **שלושת** הראשונים לפי הסדר. כמה
תחרויות? שימו לב : 30 אינו ריבוע, ולתחרות המנצחים נשאר מקום פנוי. ואז הכלילו : כתבו
פונקציה שמקבלת \( a \) סוסים, \( b \) במסלול ו-\( c \) ראשונים (עם \( a \le b^2 \)),
ומחליטה בעצמה, תחרות אחרי תחרות, מי רץ, עד שהדירוג של \( c \) הראשונים ידוע.

??? tip "רמז 1"
    חמש קבוצות של 6, ואז חמישה מנצחים. האם כדאי להוסיף סוס שישי לתחרות המנצחים? מי?
    לפני התחרות אף אחד לא יודע איזו קבוצה היא הטובה.

??? tip "רמז 2"
    אחרי תחרות המנצחים אותן מדרגות : \( (i - 1) + (j - 1) \le 2 \) נותן חמישה מועמדים
    למקומות 2 ו-3, והם נכנסים לתחרות אחת.

??? tip "רמז 3"
    לתוכנית הכללית : שמרו לכל סוס מי ידוע מהיר ממנו ומי איטי ממנו (עם סגירות), פסלו את מי
    שיש לו \( c \) מהירים, ובכל תחרות הריצו את המועמדים שבין זוגותיהם הכי הרבה השוואות
    חסרות.

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ‏**7 תחרויות**, והמקום הפנוי לא עוזר : חמש קבוצות, המנצחים (מקום 1 נקבע, נשארים
        A2, B1, A3, B2, C1), ותחרות אחת של החמישה. התוכנית הכללית : קבוצות, מנצחים, ואז
        שוב ושוב "המועמדים עם הכי הרבה השוואות חסרות" עד שמקומות 1 עד \( c \) נקבעים.
        ל-\( a \le b^2 \) ו-\( c(c + 1) / 2 - 1 \le b \) זה \( \lceil a / b \rceil + 2 \)
        תחרויות (ו-\( \lceil a / b \rceil + 1 \) כש-\( c = 1 \)), ובמקרים גדולים יותר
        התוכנית מוסיפה את מה שהמדרגות דורשות.

    <!-- cost: תחרויות 7 | תוצאה \( O(a^2) \) | זיכרון \( O(a^2) \) -->

    #### הרעיון { .sol-idea }

    **אותה מכונה, קלט אחר.** המועמד לא צריך "לראות" את הפתרון של כל מקרה : מספיק מנגנון
    אחד. לכל סוס שתי קבוצות, מהירים ידועים ואיטיים ידועים, סגורות תחת מעבר (תוצאה חדשה
    \( x \) מנצח \( y \) מחברת את כל מי שמעל \( x \) לכל מי שמתחת ל-\( y \)). סוס עם
    \( c \) מהירים ידועים יוצא; סוס שהשתיים מצטרפות ל-\( a - 1 \) נקבע.

    **מי רץ בתחרות הבאה.** אחרי הקבוצות והמנצחים, לוקחים את המועמדים הפתוחים, ממיינים
    לפי "כמה מהירים ידועים" (מעט קודם) ו"כמה איטיים ידועים" (הרבה קודם), ובונים את
    התחרות בחמדנות : בכל פעם הסוס שמוסיף הכי הרבה זוגות שעוד לא הושוו לנבחרים. זה
    בדיוק מה שנותן בסעיף א את תחרות 8 (A2, B1, A3, B2, C1, D1) ואת תחרות 9 הקצרה.

    **המקום הפנוי.** ב-30 סוסים תחרות המנצחים מריצה 5. להוסיף סוס שישי אפשר, אבל לפני
    התחרות אין דרך לדעת מי כדאי : הסוס היחיד שהיה עוזר הוא השני בקבוצה הטובה ביותר, והיא
    נקבעת רק בתחרות עצמה. היריב פשוט בוחר שהקבוצה של הסוס שהוספנו לא תהיה הטובה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **קבוצות :** ‏\( \lceil a / b \rceil \) תחרויות (5 ל-30 סוסים), והאחרונה קטנה
       יותר כש-\( a \) אינו כפולה של \( b \).
    2. **מנצחים :** תחרות אחת של מנצחי הקבוצות (5 מתוך 6 מקומות).
    3. **פסילה :** כל סוס עם \( c \) מהירים ידועים יוצא; נשארו \( c(c + 1) / 2 - 1 \)
       מועמדים (5 ל-\( c = 3 \)) :

        <!-- gen 4 -->

        <svg class="figure hr-grid" viewBox="0 0 464 240" style="max-width:29rem" role="img" aria-label="הסוסים אחרי 6 תחרויות : שורה לכל קבוצה לפי סדר המנצחים, תא ירוק נקבע, כחול מועמד, אפור נפסל"><text class="tick" x="102" y="20" text-anchor="middle">1</text><text class="tick" x="166" y="20" text-anchor="middle">2</text><text class="tick" x="230" y="20" text-anchor="middle">3</text><text class="tick" x="294" y="20" text-anchor="middle">4</text><text class="tick" x="358" y="20" text-anchor="middle">5</text><text class="tick" x="422" y="20" text-anchor="middle">6</text><text class="tick" x="62" y="54" text-anchor="end">A (1)</text><g class="hr-cell is-placed"><rect x="72" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="55" text-anchor="middle">A1</text><text class="hr-count" x="128" y="43" text-anchor="end">0</text></g><g class="hr-cell is-cand"><rect x="136" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="55" text-anchor="middle">A2</text><text class="hr-count" x="192" y="43" text-anchor="end">1</text></g><g class="hr-cell is-cand"><rect x="200" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="55" text-anchor="middle">A3</text><text class="hr-count" x="256" y="43" text-anchor="end">2</text></g><g class="hr-cell is-out"><rect x="264" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="55" text-anchor="middle">A4</text><text class="hr-count" x="320" y="43" text-anchor="end">3</text></g><g class="hr-cell is-out"><rect x="328" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="55" text-anchor="middle">A5</text><text class="hr-count" x="384" y="43" text-anchor="end">4</text></g><g class="hr-cell is-out"><rect x="392" y="32" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="55" text-anchor="middle">A6</text><text class="hr-count" x="448" y="43" text-anchor="end">5</text></g><text class="tick" x="62" y="94" text-anchor="end">D (2)</text><g class="hr-cell is-cand"><rect x="72" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="95" text-anchor="middle">D1</text><text class="hr-count" x="128" y="83" text-anchor="end">1</text></g><g class="hr-cell is-cand"><rect x="136" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="95" text-anchor="middle">D2</text><text class="hr-count" x="192" y="83" text-anchor="end">2</text></g><g class="hr-cell is-out"><rect x="200" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="95" text-anchor="middle">D3</text><text class="hr-count" x="256" y="83" text-anchor="end">3</text></g><g class="hr-cell is-out"><rect x="264" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="95" text-anchor="middle">D4</text><text class="hr-count" x="320" y="83" text-anchor="end">4</text></g><g class="hr-cell is-out"><rect x="328" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="95" text-anchor="middle">D5</text><text class="hr-count" x="384" y="83" text-anchor="end">5</text></g><g class="hr-cell is-out"><rect x="392" y="72" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="95" text-anchor="middle">D6</text><text class="hr-count" x="448" y="83" text-anchor="end">6</text></g><text class="tick" x="62" y="134" text-anchor="end">C (3)</text><g class="hr-cell is-cand"><rect x="72" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="135" text-anchor="middle">C1</text><text class="hr-count" x="128" y="123" text-anchor="end">2</text></g><g class="hr-cell is-out"><rect x="136" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="135" text-anchor="middle">C2</text><text class="hr-count" x="192" y="123" text-anchor="end">3</text></g><g class="hr-cell is-out"><rect x="200" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="135" text-anchor="middle">C3</text><text class="hr-count" x="256" y="123" text-anchor="end">4</text></g><g class="hr-cell is-out"><rect x="264" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="135" text-anchor="middle">C4</text><text class="hr-count" x="320" y="123" text-anchor="end">5</text></g><g class="hr-cell is-out"><rect x="328" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="135" text-anchor="middle">C5</text><text class="hr-count" x="384" y="123" text-anchor="end">6</text></g><g class="hr-cell is-out"><rect x="392" y="112" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="135" text-anchor="middle">C6</text><text class="hr-count" x="448" y="123" text-anchor="end">7</text></g><text class="tick" x="62" y="174" text-anchor="end">B (4)</text><g class="hr-cell is-out"><rect x="72" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="175" text-anchor="middle">B1</text><text class="hr-count" x="128" y="163" text-anchor="end">3</text></g><g class="hr-cell is-out"><rect x="136" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="175" text-anchor="middle">B2</text><text class="hr-count" x="192" y="163" text-anchor="end">4</text></g><g class="hr-cell is-out"><rect x="200" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="175" text-anchor="middle">B3</text><text class="hr-count" x="256" y="163" text-anchor="end">5</text></g><g class="hr-cell is-out"><rect x="264" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="175" text-anchor="middle">B4</text><text class="hr-count" x="320" y="163" text-anchor="end">6</text></g><g class="hr-cell is-out"><rect x="328" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="175" text-anchor="middle">B5</text><text class="hr-count" x="384" y="163" text-anchor="end">7</text></g><g class="hr-cell is-out"><rect x="392" y="152" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="175" text-anchor="middle">B6</text><text class="hr-count" x="448" y="163" text-anchor="end">8</text></g><text class="tick" x="62" y="214" text-anchor="end">E (5)</text><g class="hr-cell is-out"><rect x="72" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="102" y="215" text-anchor="middle">E1</text><text class="hr-count" x="128" y="203" text-anchor="end">4</text></g><g class="hr-cell is-out"><rect x="136" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="166" y="215" text-anchor="middle">E2</text><text class="hr-count" x="192" y="203" text-anchor="end">5</text></g><g class="hr-cell is-out"><rect x="200" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="230" y="215" text-anchor="middle">E3</text><text class="hr-count" x="256" y="203" text-anchor="end">6</text></g><g class="hr-cell is-out"><rect x="264" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="294" y="215" text-anchor="middle">E4</text><text class="hr-count" x="320" y="203" text-anchor="end">7</text></g><g class="hr-cell is-out"><rect x="328" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="358" y="215" text-anchor="middle">E5</text><text class="hr-count" x="384" y="203" text-anchor="end">8</text></g><g class="hr-cell is-out"><rect x="392" y="192" width="60" height="36" rx="4"/><text class="hr-name" x="422" y="215" text-anchor="middle">E6</text><text class="hr-count" x="448" y="203" text-anchor="end">9</text></g></svg>

        <!-- /gen -->

    4. **המועמדים :** תחרות של החמישה, וסדר ההגעה שלה הוא מקומות 2 ו-3 :

        <!-- gen 5 -->

        | תחרות | מי רץ | התוצאה | נפסלו (ולמה) | נקבעו | עוד פתוחים |
        |:-:|---|---|---|---|:-:|
        | ‏1 | ‏קבוצה A | ‏A1 > A2 > A3 > A4 > A5 > A6 | ‏3 : A4, A5, A6 | ‏— | ‏27 |
        | ‏2 | ‏קבוצה B | ‏B1 > B2 > B3 > B4 > B5 > B6 | ‏3 : B4, B5, B6 | ‏— | ‏24 |
        | ‏3 | ‏קבוצה C | ‏C1 > C2 > C3 > C4 > C5 > C6 | ‏3 : C4, C5, C6 | ‏— | ‏21 |
        | ‏4 | ‏קבוצה D | ‏D1 > D2 > D3 > D4 > D5 > D6 | ‏3 : D4, D5, D6 | ‏— | ‏18 |
        | ‏5 | ‏קבוצה E | ‏E1 > E2 > E3 > E4 > E5 > E6 | ‏3 : E4, E5, E6 | ‏— | ‏15 |
        | ‏6 | ‏A1, B1, C1, D1, E1 | ‏A1 > D1 > C1 > B1 > E1 | ‏9 : B1, B2, B3, C2, C3, D3, E1, E2, E3 | ‏A1 מקום 1 | ‏5 |
        | ‏7 | ‏D1, A2, C1, D2, A3 | ‏D1 > C1 > A2 > A3 > D2 | ‏A2 (A1, C1, D1); A3 (A1, A2, C1 ועוד 1); D2 (A1, A2, A3 ועוד 2) | ‏D1 מקום 2, C1 מקום 3 | ‏0 |

        <!-- /gen -->

    5. **התוכנית הכללית :** הקוד חוזר על שלבים 3 ו-4 עד שמקומות 1 עד \( c \) נקבעו, ובכל
       סיבוב בוחר את \( b \) המועמדים עם הכי הרבה השוואות חסרות.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="hr_beats, hr_race, horses_plan" linenums="1" hl_lines="10 11 12 42 43 51 52 53 54"
        localparam int MAXA = 64;       // horses: the known sets are 64-bit masks
        localparam int MAXB = 8;        // horses per race
        localparam int MAXR = 80;       // races at most

        typedef longint unsigned mask_t;

        // x beats y: everyone known above x beats everyone known below y (transitive closure).
        function automatic void hr_beats(int x, int y, inout mask_t faster[MAXA], inout mask_t slower[MAXA]);
          mask_t up = faster[x] | (mask_t'(1) << x), down = slower[y] | (mask_t'(1) << y);
          if (slower[x][y]) return;
          for (int u = 0; u < MAXA; u++) if (up[u]) slower[u] |= down;        // (1)!
          for (int v = 0; v < MAXA; v++) if (down[v]) faster[v] |= up;
        endfunction

        // One race: the n horses sorted by the hidden speed (lower is faster), every pair recorded.
        function automatic void hr_race(int n, inout int horses[MAXB], int speed[MAXA], inout mask_t faster[MAXA], inout mask_t slower[MAXA]);
          for (int i = 1; i < n; i++) begin
            int x = horses[i], j = i;
            while (j > 0 && speed[horses[j - 1]] > speed[x]) begin horses[j] = horses[j - 1]; j--; end
            horses[j] = x;
          end
          for (int i = 0; i < n; i++) for (int k = i + 1; k < n; k++) hr_beats(horses[i], horses[k], faster, slower);
        endfunction

        // The plan: groups, the winners, then the most promising unsettled candidates until the
        // first c ranks are known. Returns the number of races; races[r] holds race r in finishing order.
        function automatic int horses_plan(int a, int b, int c, int speed[MAXA], output int ranking[MAXB], output int races[MAXR][MAXB], output int sizes[MAXR]);
          mask_t faster[MAXA], slower[MAXA];
          int horses[MAXB], pool[MAXA], n = 0, groups = (a + b - 1) / b, np, nc, best, score, bs;
          bit settled;
          foreach (faster[i]) begin faster[i] = 0; slower[i] = 0; end
          for (int k = 0; k < groups; k++) begin                                  // the groups
            sizes[n] = (a - k * b < b) ? a - k * b : b;
            for (int i = 0; i < sizes[n]; i++) horses[i] = k * b + i;
            hr_race(sizes[n], horses, speed, faster, slower);
            races[n] = horses; n++;
          end
          if (groups > 1) begin                                                    // the winners
            for (int k = 0; k < groups; k++) horses[k] = races[k][0];
            sizes[n] = groups; hr_race(groups, horses, speed, faster, slower); races[n] = horses; n++;
          end
          forever begin
            settled = 1;
            for (int r = 1; r <= c; r++) begin
              bit found = 0;
              for (int x = 0; x < a; x++) if ($countones(faster[x]) == r - 1 && $countones(faster[x] | slower[x]) == a - 1) found = 1;
              if (!found) settled = 0;
            end
            if (settled) break;
            np = 0;                                                                // the open candidates, most promising first
            for (int x = 0; x < a; x++)
              if ($countones(faster[x]) < c && $countones(faster[x] | slower[x]) < a - 1) begin
                int j = np;
                while (j > 0 && (($countones(faster[pool[j - 1]]) > $countones(faster[x])) ||
                                 ($countones(faster[pool[j - 1]]) == $countones(faster[x]) && $countones(slower[pool[j - 1]]) < $countones(slower[x])))) begin
                  pool[j] = pool[j - 1]; j--;
                end
                pool[j] = x; np++;
              end
            nc = 0;
            while (nc < b && np > 0) begin                                         // greedy: the most comparisons still missing
              bs = -1;
              for (int p = 0; p < np; p++) begin
                score = 0;
                for (int q = 0; q < nc; q++) if (!faster[pool[p]][horses[q]] && !slower[pool[p]][horses[q]]) score++;
                if (score > bs) begin bs = score; best = p; end
              end
              horses[nc] = pool[best]; nc++;
              for (int p = best; p + 1 < np; p++) pool[p] = pool[p + 1];
              np--;
            end
            sizes[n] = nc; hr_race(nc, horses, speed, faster, slower); races[n] = horses; n++;
          end
          for (int r = 1; r <= c; r++)
            for (int x = 0; x < a; x++) if ($countones(faster[x]) == r - 1 && $countones(faster[x] | slower[x]) == a - 1) ranking[r - 1] = x;
          return n;
        endfunction
        ```

        1. הסגירות : מי שמעל \( x \) (כולל \( x \)) מקבל את כל מי שמתחת ל-\( y \) (כולל \( y \))
           כאיטיים, ולהפך.
        2. המועמד הפתוח : פחות מ-\( c \) מהירים ידועים, והדירוג עדיין לא ידוע.
        3. המיון : מעט מהירים ידועים קודם, ובשוויון הרבה איטיים ידועים קודם.
        4. הבחירה החמדנית : הסוס שמוסיף הכי הרבה זוגות שעוד לא הושוו לנבחרים עד כה; בשוויון
           הראשון ברשימה הממוינת.

    === "Python"
        ```python title="horses_plan" linenums="1" hl_lines="11 12 13 32 33 36 37 38"
        def horses_plan(a: int, b: int, c: int, race) -> tuple[list[int], list[list[int]]]:
            """The c fastest of a horses in order, b per race, without a stopwatch: race(horses)
            returns them fastest first. Returns the ranking and every race in finishing order."""
            faster = [set() for _ in range(a)]              # horses known to beat x
            slower = [set() for _ in range(a)]
            log = []

            def beats(x, y):
                if y in slower[x]:
                    return
                for u in faster[x] | {x}:                   # (1)!
                    for v in slower[y] | {y}:
                        slower[u].add(v); faster[v].add(u)

            def run(group):
                order = race(group)
                log.append(order)
                for i, x in enumerate(order):
                    for y in order[i + 1:]:
                        beats(x, y)

            def rank(x):                                    # the exact rank once both sets are complete
                return len(faster[x]) + 1 if len(faster[x]) + len(slower[x]) == a - 1 else None

            groups = [list(range(k, min(k + b, a))) for k in range(0, a, b)]
            for g in groups:
                run(g)
            if len(groups) > 1:
                run([log[k][0] for k in range(len(groups))])
            while any(all(rank(x) != r for x in range(a)) for r in range(1, c + 1)):
                pool = [x for x in range(a) if len(faster[x]) < c and rank(x) is None]      # (2)!
                pool.sort(key=lambda x: (len(faster[x]), -len(slower[x]), x))             # (3)!
                chosen = []
                while len(chosen) < b and pool:
                    best = max(pool, key=lambda x: (sum(1 for y in chosen if y not in faster[x] and y not in slower[x]),
                                                    -len(faster[x]), len(slower[x]), -x))  # (4)!
                    pool.remove(best)
                    chosen.append(best)
                run(chosen)
            return [x for r in range(1, c + 1) for x in range(a) if rank(x) == r], log
        ```

        1. הסגירות : מי שמעל \( x \) (כולל \( x \)) מקבל את כל מי שמתחת ל-\( y \) (כולל \( y \))
           כאיטיים, ולהפך.
        2. המועמד הפתוח : פחות מ-\( c \) מהירים ידועים, והדירוג עדיין לא ידוע.
        3. המיון : מעט מהירים ידועים קודם, ובשוויון הרבה איטיים ידועים קודם.
        4. הבחירה החמדנית : הסוס שמוסיף הכי הרבה זוגות שעוד לא הושוו לנבחרים עד כה; בשוויון
           הראשון ברשימה הממוינת.

    #### למה זה נכון { .sol-proof }

    **נכונות.** כל יחס שנרשם נובע מתוצאות, ולכן אף סוס מארבעת (או \( c \)) הראשונים לא
    נפסל, ומי שנקבע במקום \( r \) באמת שם. הלולאה מסתיימת : כל תחרות של מועמדים פתוחים
    מוסיפה לפחות זוג אחד שלא הושווה (אחרת כל הזוגות ידועים, הסדר בין המועמדים מלא, וכולם
    היו נקבעים), ומספר הזוגות סופי.

    **‏7 ל-30 סוסים, ולא 6.** חמש תחרויות כדי שכל סוס ירוץ. בתחרות השישית חייבים להיפגש
    כל המנצחים (מנצח שלא פגש אחר יכול להיות מקום 1), ונשאר מקום אחד לסוס נוסף \( X \).
    היריב קובע את סדר המנצחים **אחרי** שראה מי \( X \) : הוא בוחר שהקבוצה של \( X \) לא
    תהיה הטובה ביותר. אז A2 (השני בקבוצה הטובה) ו-B1 מעולם לא הושוו, ושניהם יכולים להיות
    מקום 2. לכן צריך תחרות שביעית, והמדרגות של \( c = 3 \), חמישה סוסים, נכנסות בה.

    **המקרה הכללי.** עם \( g = \lceil a / b \rceil \le b \) קבוצות, אחרי \( g + 1 \)
    תחרויות למועמד במקום \( i \) בקבוצה \( j \) ידועים \( (i - 1) + (j - 1) \) מהירים, ולכן
    נשארים \( c(c + 1) / 2 - 1 \) מועמדים (פחות, אם \( g < c \)). כשהם נכנסים לתחרות אחת
    זה \( g + 2 \) תחרויות, וחסם היריב של \( g + 1 \) עובד כמו למעלה לכל \( c \ge 2 \).
    כשהם לא נכנסים, כל תחרות של \( b \) מוציאה לכל היותר \( b - 1 \) מהם, וזה חסם תחתון
    פשוט על השלב השלישי, שלא תמיד מושג. הבדיקות של השאלה מריצות את התוכנית מול **כל**
    הסדרים האפשריים של מועמדי המדרגות בסעיפים א ו-ב (768 ו-16 סדרים), ובכולם 9 ו-7.

    **דוגמאות.** מספר התחרויות של התוכנית במקרה הגרוע על מהירויות מוגרלות :

    <!-- gen 6 -->

    | ‏a | ‏b | ‏c | קבוצות | מועמדי המדרגות | תחרויות |
    |:-:|:-:|:-:|:-:|:-:|:-:|
    | ‏25 | ‏5 | ‏3 | ‏5 | ‏5 | ‏**7** |
    | ‏25 | ‏5 | ‏1 | ‏5 | ‏0 | ‏**6** |
    | ‏36 | ‏6 | ‏4 | ‏6 | ‏9 | ‏**9** |
    | ‏30 | ‏6 | ‏3 | ‏5 | ‏5 | ‏**7** |
    | ‏16 | ‏4 | ‏3 | ‏4 | ‏5 | ‏**7** |
    | ‏49 | ‏7 | ‏5 | ‏7 | ‏14 | ‏**10** |
    | ‏64 | ‏8 | ‏4 | ‏8 | ‏9 | ‏**10** |
    | ‏20 | ‏5 | ‏2 | ‏4 | ‏2 | ‏**6** |
    | ‏12 | ‏4 | ‏3 | ‏3 | ‏5 | ‏**6** |

    <!-- /gen -->

    **נסו בעצמכם.** בוחרים מספר סוסים, גודל מסלול וכמה ראשונים (עד 64 סוסים, ולא יותר
    קבוצות ממה שתחרות מכילה), מגרילים מהירויות ומריצים תחרות אחרי תחרות :

    <div class="explorer" data-kind="horses" data-a="30" data-b="6" data-c="3" data-seed="11"></div>

    #### סיבוכיות { .sol-cost }

    - **תחרויות :** ‏\( \lceil a / b \rceil + 1 \) ועוד מה שהמדרגות דורשות; בסעיף א 9,
      בסעיף ב 7.
    - **זמן :** כל תוצאה "‏\( x \) מנצח \( y \)" עולה \( O(a^2) \) בסגירות הנאיבית, ויש
      \( O(b^2) \) תוצאות לתחרות; עם 64 סוסים ומסכות של 64 ביט זה מיידי.
    - **זיכרון :** שתי קבוצות לכל סוס, \( O(a^2) \) ביטים.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : המנצח של הקבוצה השנייה הוא מקום 2"
    תחרות המנצחים מדרגת **קבוצות**, לא סוסים. B1 ניצח את C1, אבל מול A2 הוא מעולם לא רץ,
    ו-A2 יכול להיות מהיר ממנו. לכן המועמדים למקום 2 הם שניים, ולמקום 4 ארבעה חדשים.

??? trap "מלכודת : 7 תחרויות גם ל-36 סוסים"
    החידה הקלאסית (25, 5, 3) מסתיימת ב-7 כי חמשת מועמדי המדרגות נכנסים לתחרות אחת של 5.
    עם ארבעה ראשונים יש 9 מועמדים, יותר מ-6, ושתי תחרויות הן המינימום : אחת לא יכולה
    להוציא 8 מהם.

??? trap "מלכודת : המקום הפנוי בתחרות המנצחים"
    ‏30 סוסים נותנים 5 מנצחים ל-6 מקומות, ומפתה להוסיף "את השני של הקבוצה הטובה". אבל
    איזו קבוצה טובה יודעים רק מהתחרות הזו עצמה. סוס שמוסיפים בלי לדעת לא חוסך תחרות.

??? trap "מלכודת : לספור מקומות במקום מהירים ידועים"
    "C1 הגיע שלישי בין המנצחים, אז הוא מקום 3 לכל היותר"? לא : הוא מקום 3 **לפחות**, כי
    ידועים שניים מהירים ממנו. מי שסופר "מקומות" במקום "כמה ידועים מהירים ממני" מוציא
    סוסים לא נכונים.

??? followup "שאלות המשך"
    - **הראשונים בלי סדר :** צריך רק את קבוצת שלושת המהירים, לא את הסדר ביניהם. חוסכים
      תחרות? ‏(ב-25 / 5 / 3 לא : תחרות 7 עדיין נחוצה כדי להבדיל בין A2, B1, A3, B2 ו-C1.)
    - **המהיר ביותר בלבד :** ‏\( c = 1 \). ‏(‏\( \lceil (a - 1) / (b - 1) \rceil \) תחרויות,
      כי כל תחרות מוציאה לכל היותר \( b - 1 \) סוסים, וזה הדוק.)
    - **יותר קבוצות ממקומות :** 100 סוסים, 5 במסלול, שלושת הראשונים. ‏(20 קבוצות; המנצחים
      צריכים טורניר של 4 תחרויות ועוד אחת, ואז מדרגות עמוקות יותר.)
    - **עם שעון עצר :** כל תחרות נותנת זמנים. כמה תחרויות ל-36 סוסים? ‏(6 : כל סוס רץ פעם
      אחת והזמנים ניתנים להשוואה.)
    - **המינימום המדויק :** לכתוב חיפוש ממצה על עצי החלטה למקרים זעירים (9 סוסים, 3
      במסלול, שניים ראשונים) ולהשוות לתוכנית. ‏(ב-9 / 3 / 2 התוכנית נותנת 5 והמינימום
      הוא 5.)
