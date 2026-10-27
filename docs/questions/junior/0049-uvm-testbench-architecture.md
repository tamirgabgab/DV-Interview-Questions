---
id: 49
title: ארכיטקטורה של סביבת UVM – הרכיבים ומסלול הטרנזקציה
level: junior
difficulty: medium
kind: dv
tags: [uvm, methodology, systemverilog]
source: "שאלת פתיחה נפוצה בראיונות אימות"
added: 2026-10-27
---

## השאלה

המראיין נותן לך לוח ואומר : "יש לנו רכיב עם ממשק כניסה אחד וממשק יציאה אחד. שרטט לי
סביבת UVM שבודקת אותו, והסבר מה כל רכיב עושה".

- **סעיף א – הסכימה :** שרטטו את הרכיבים ואת החיבורים ביניהם, והסבירו בשורה או שתיים
  את התפקיד של כל אחד, וגם מה הוא **לא** אמור לעשות.
- **סעיף ב – מסלול של טרנזקציה :** עקבו אחרי טרנזקציה אחת : מה-sequence ועד שה-scoreboard
  מכריע. איזו פונקציה נקראת בכל שלב, ובאיזה phase הכול נבנה ומתחבר?
- **סעיף ג – החלטות תכנון :** למה ה-driver והמוניטור הם רכיבים נפרדים? למה ה-agent
  של היציאה פסיבי? ומה משתנה כשהבלוק נכנס לסביבה של מערכת שלמה?

??? interviewer "מה המראיין בודק"
    - **הפרדת תפקידים :** האם המועמד יודע מי מייצר stimulus, מי רק מסתכל, ומי מחליט אם
      התוצאה נכונה.
    - **החיבורים, לא רק הקופסאות :** האם הוא יודע איך טרנזקציה עוברת בין רכיבים (TLM,
      analysis port) ואיך רכיב מגיע לאותות (virtual interface דרך `config_db`).
    - **מחזור החיים :** ‏phases, ‏objections, ומתי כל רכיב נוצר.
    - **שימוש חוזר :** האם הסביבה בנויה כך שה-agent עובר כמו שהוא לבלוק אחר או לסביבת מערכת.
    - **ניסיון אמיתי :** האם הוא יודע איפה דברים נשברים (מוניטור שכותב לאותות, scoreboard
      שמקבל מה-driver).

---

### סעיף א – הסכימה

??? tip "רמז 1"
    התחילו מהקצוות : ה-DUT למטה, וה-test למעלה. מה צריך באמצע כדי לייצר קלט, לראות את
    הקלט ואת הפלט, ולהחליט אם הפלט נכון?

??? tip "רמז 2"
    לכל ממשק יש agent : ‏sequencer, ‏driver ומוניטור. מעל ה-agents יש env, ובו גם מי
    שמשווה (scoreboard) ומי שסופר מה נבדק (coverage).

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ה-test יוצר env; ב-env יש agent אקטיבי לכניסה (sequencer, ‏driver, מוניטור), agent
        פסיבי ליציאה (מוניטור בלבד), scoreboard עם מודל ייחוס, ו-coverage. ה-driver
        והמוניטורים מגיעים לאותות דרך virtual interface שה-top שם ב-`config_db`. ה-driver
        רק מייצר, המוניטורים רק מסתכלים, וה-scoreboard רק מחליט.

    #### הרעיון { .sol-idea }

    הסביבה בנויה משכבות, וכל שכבה עושה דבר אחד. **ה-sequence** אומר *מה* לשלוח, ברמת
    טרנזקציה. **ה-driver** יודע *איך* לשלוח אותה לפי הפרוטוקול. **המוניטור** רק מסתכל על
    האותות ובונה מהם טרנזקציה. **ה-scoreboard** מחליט אם מה שיצא נכון. **ה-coverage** סופר
    מה כבר נבדק. כך כל חלק אפשר להחליף או להשתמש בו שוב בלי לגעת בשאר.

    <!-- gen 0 -->

    <svg class="figure uv-fig" viewBox="0 0 680 520" style="max-width:42rem" role="img" aria-label="סביבת UVM : test, env, שני agents, scoreboard ו-coverage מעל ה-DUT, עם ה-interfaces ביניהם"><defs><marker id="uv-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs><g class="uv-box is-cont uv-top"><rect x="8" y="8" width="664" height="504" rx="8"/><text x="16" y="25">tb_top</text></g><g class="uv-box is-cont uv-test"><rect x="18" y="30" width="644" height="326" rx="8"/><text x="26" y="47">test</text></g><g class="uv-box is-cont uv-env"><rect x="28" y="80" width="624" height="266" rx="8"/><text x="36" y="97">env</text></g><g class="uv-box is-cont uv-agent_in"><rect x="38" y="104" width="252" height="232" rx="8"/><text x="46" y="121">agent (active)</text></g><g class="uv-box is-cont uv-agent_out"><rect x="470" y="104" width="172" height="232" rx="8"/><text x="478" y="121">agent (passive)</text></g><line class="uv-arrow uv-tlm" x1="164.2" y1="70.0" x2="119.8" y2="132.0" marker-end="url(#uv-arrow)"/><line class="uv-arrow uv-tlm" x1="102.8" y1="176.0" x2="99.2" y2="240.0" marker-end="url(#uv-arrow)"/><line class="uv-arrow uv-pin" x1="108.4" y1="284.0" x2="155.5" y2="384.0" marker-end="url(#uv-arrow)"/><line class="uv-arrow uv-pin" x1="275.7" y1="420.0" x2="300.0" y2="423.9" marker-end="url(#uv-arrow)"/><line class="uv-arrow uv-pin" x1="171.8" y1="384.0" x2="215.4" y2="284.0" marker-end="url(#uv-arrow)"/><line class="uv-arrow uv-pin" x1="450.0" y1="421.9" x2="470.0" y2="418.2" marker-end="url(#uv-arrow)"/><line class="uv-arrow uv-pin" x1="555.9" y1="384.0" x2="555.2" y2="284.0" marker-end="url(#uv-arrow)"/><line class="uv-arrow uv-tlm" x1="259.6" y1="240.0" x2="328.7" y2="196.0" marker-end="url(#uv-arrow)"/><line class="uv-arrow uv-tlm" x1="280.0" y1="262.0" x2="304.0" y2="262.0" marker-end="url(#uv-arrow)"/><line class="uv-arrow uv-tlm" x1="515.5" y1="240.0" x2="436.5" y2="196.0" marker-end="url(#uv-arrow)"/><g class="uv-box uv-sequence"><rect x="120" y="40" width="110" height="30" rx="6"/><text x="175.0" y="60.0" text-anchor="middle">sequence</text></g><g class="uv-box uv-sequencer"><rect x="48" y="132" width="112" height="44" rx="6"/><text x="104.0" y="159.0" text-anchor="middle">sequencer</text></g><g class="uv-box uv-driver"><rect x="48" y="240" width="100" height="44" rx="6"/><text x="98.0" y="267.0" text-anchor="middle">driver</text></g><g class="uv-box uv-monitor_in"><rect x="170" y="240" width="110" height="44" rx="6"/><text x="225.0" y="267.0" text-anchor="middle">monitor</text></g><g class="uv-box uv-scoreboard"><rect x="304" y="132" width="150" height="64" rx="6"/><text x="379.0" y="169.0" text-anchor="middle">scoreboard</text></g><g class="uv-box uv-coverage"><rect x="304" y="240" width="150" height="44" rx="6"/><text x="379.0" y="267.0" text-anchor="middle">coverage</text></g><g class="uv-box uv-monitor_out"><rect x="500" y="240" width="110" height="44" rx="6"/><text x="555.0" y="267.0" text-anchor="middle">monitor</text></g><g class="uv-box uv-vif_in"><rect x="48" y="384" width="232" height="36" rx="6"/><text x="164.0" y="407.0" text-anchor="middle">interface in</text></g><g class="uv-box uv-dut"><rect x="300" y="376" width="150" height="120" rx="6"/><text x="375.0" y="441.0" text-anchor="middle">DUT</text></g><g class="uv-box uv-vif_out"><rect x="470" y="384" width="172" height="36" rx="6"/><text x="556.0" y="407.0" text-anchor="middle">interface out</text></g></svg>

    <!-- /gen -->

    <!-- gen 1 -->

    <span class="viz-legend"><span><i class="uv-key-tlm"></i>חיבור TLM : טרנזקציות</span><span><i class="uv-key-pin"></i>אותות דרך ה-interface</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏tb_top (מודול, לא class) :** מייצר שעון ואיפוס, מחבר את ה-DUT ל-interfaces, שם
       אותם ב-`uvm_config_db` וקורא ל-`run_test()`. לא מכיל לוגיקת בדיקה.
    2. **‏test :** בוחר תצורה (הגדרות ב-`config_db`, ‏factory overrides), יוצר את ה-env,
       ומריץ sequences ב-`run_phase` בין `raise_objection` ל-`drop_objection`.
    3. **‏env :** מכיל את ה-agents, את ה-scoreboard ואת ה-coverage, ומחבר ביניהם
       ב-`connect_phase`. אין בו stimulus ואין בו בדיקות.
    4. **‏agent :** מאגד sequencer, ‏driver ומוניטור של ממשק אחד. אקטיבי יוצר את שלושתם;
       פסיבי רק את המוניטור.
    5. **‏sequence ו-sequence item :** ה-item הוא טרנזקציה עם שדות `rand` ו-constraints;
       ה-sequence מייצר items ושולח אותם. הם objects, לא components : הם נוצרים ונעלמים
       בזמן ריצה.
    6. **‏sequencer :** מתווך בין sequences ל-driver : מחזיק תור, ובוחר (arbitration) כשכמה
       sequences רצים עליו בבת אחת.
    7. **‏driver :** לוקח item ב-`get_next_item`, מתרגם אותו לאותות דרך ה-virtual
       interface, ומחזיר `item_done`. לא בודק נכונות.
    8. **מוניטור :** דוגם את האותות, בונה טרנזקציה, ושולח אותה ב-`analysis_port.write()`
       לכל המנויים. לא משנה אף אות, וגם לא בודק תוצאות (לכל היותר בדיקות פרוטוקול).
    9. **‏scoreboard :** מקבל טרנזקציות משני המוניטורים; מודל הייחוס מחשב מהקלט את הפלט
       הצפוי, וה-scoreboard משווה אותו לפלט האמיתי. בסוף בודק שלא נשאר כלום בהמתנה.
    10. **‏coverage :** ‏`uvm_subscriber` שמקבל טרנזקציות ודוגם covergroups. עונה על "מה
        נבדק", לא על "האם זה עבד".

    </div>

    #### למה זה נכון { .sol-proof }

    **החיבורים.** כל חץ בסכימה הוא מנגנון מסוים, וכדאי לדעת לשיים אותו :

    <!-- gen 2 -->

    | החיבור | המנגנון | מה עובר בו |
    |---|---|---|
    | ‏sequence → sequencer | ‏`start_item` / `finish_item` | ה-sequence מבקש תור, מקבל אישור, ממלא את הפריט ושולח אותו |
    | ‏sequencer → driver | ‏`seq_item_port` ← `seq_item_export` | ה-driver מושך פריט ב-`get_next_item` ומחזיר `item_done` |
    | ‏driver → interface | ‏virtual interface | ה-driver משנה אותות לפי הפרוטוקול |
    | ‏interface → monitor | ‏virtual interface | המוניטור רק דוגם אותות, ובונה מהם טרנזקציה |
    | ‏monitor → scoreboard / coverage | ‏`uvm_analysis_port` ← `uvm_analysis_imp` | ‏`write()` לכל המנויים, בלי לחכות |
    | ‏config_db → driver / monitor | ‏`uvm_config_db#(virtual ...)::get` | ה-top שם את ה-interface, והרכיבים לוקחים אותו ב-`build_phase` |

    <!-- /gen -->

    **למה המוניטור של הכניסה מחובר ל-scoreboard.** ה-scoreboard צריך לדעת מה **באמת**
    נכנס ל-DUT, לא מה ה-sequence ביקש. אם ה-driver עיכב, חילק או ביטל פריט, רק המוניטור
    יודע. לכן הצפוי מחושב מהמוניטור של הכניסה, והאמיתי מגיע מהמוניטור של היציאה.

---

### סעיף ב – מסלול של טרנזקציה

??? tip "רמז 1"
    טרנזקציה עוברת שלוש "צורות" : אובייקט ב-sequence, אותות על הממשק, ושוב אובייקט אצל
    המוניטור. מי מבצע כל המרה?

??? tip "רמז 2"
    בין ה-sequence ל-driver יש לחיצת יד : ‏`start_item`, ‏`finish_item`, ‏`get_next_item`,
    ‏`item_done`. מי מחכה למי?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        ה-test מריץ sequence על ה-sequencer; ה-sequence יוצר item, ‏`start_item` מחכה
        לאישור מה-sequencer, וה-item מקבל ערכים (`randomize`) ונשלח ב-`finish_item`. ה-driver
        מושך אותו ב-`get_next_item`, מניע את האותות ומחזיר `item_done`. המוניטורים בונים
        טרנזקציות מהאותות ושולחים אותן ב-`write()`; ה-scoreboard מחשב את הצפוי מהכניסה
        ומשווה ליציאה. הכול נבנה ב-`build_phase` מלמעלה למטה, מתחבר ב-`connect_phase`,
        ורץ ב-`run_phase` כל עוד יש objection.

    #### הרעיון { .sol-idea }

    **לחיצת היד בין sequence ל-driver** היא החלק שמבלבל הכי הרבה. ה-sequence וה-driver רצים
    כל אחד ב-thread משלו, וה-sequencer מתאם ביניהם : ‏`start_item` חוסם עד שה-sequencer בחר
    ב-sequence הזה וה-driver מוכן לפריט; ‏`finish_item` מוסר את הפריט וחוסם עד שה-driver
    אומר `item_done`. לכן מקובל לתת ערכים לפריט **אחרי** `start_item` : כך הם נקבעים ברגע
    השליחה, ויכולים להתחשב במצב של אותו רגע.

    **הצד של המוניטורים** הוא שידור (broadcast) : ‏`write()` לא חוסם ולא מחכה לתשובה, ולכל
    analysis port יכולים להיות אפס או הרבה מנויים. זו הסיבה שאפשר להוסיף coverage או
    scoreboard נוסף בלי לגעת במוניטור.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏test :** ב-`run_phase` מרים objection ומריץ `seq.start(env.agent_in.sequencer)`.
    2. **‏sequence :** ‏`req = item::type_id::create("req")`, ‏`start_item(req)`,
       ‏`req.randomize()`, ‏`finish_item(req)`.
    3. **‏sequencer :** בוחר בין ה-sequences שמחכים, ומעביר את הפריט ל-driver.
    4. **‏driver :** ‏`seq_item_port.get_next_item(req)`, מניע אותות לפי הפרוטוקול דרך
       ה-virtual interface, ו-`seq_item_port.item_done()`.
    5. **‏DUT :** מעבד, ומוציא תוצאה בממשק היציאה.
    6. **מוניטור הכניסה :** רואה את הטרנזקציה על הפינים, ו-`ap.write(tr)` ל-scoreboard
       (שמחשב את הצפוי במודל) ול-coverage.
    7. **מוניטור היציאה :** רואה את התוצאה, ו-`ap.write(tr)` ל-scoreboard.
    8. **‏scoreboard :** משווה צפוי לאמיתי. בסוף, ב-`check_phase`, מוודא שלא נשאר כלום.
    9. **‏test :** ‏`drop_objection`, ו-UVM עובר לשלבי הסיכום.

    </div>

    #### למה זה נכון { .sol-proof }

    **ה-phases.** הסדר מבטיח שכשמשהו מתחבר, הוא כבר קיים, וכשמשהו רץ, הוא כבר מחובר :

    <!-- gen 3 -->

    | השלב | הסדר | מה קורה בו |
    |---|:-:|---|
    | ‏`build_phase` | מלמעלה למטה | יצירת הרכיבים (`type_id::create`) ולקיחת הגדרות מ-`config_db` |
    | ‏`connect_phase` | מלמטה למעלה | חיבור ה-ports : ‏driver ל-sequencer, מוניטורים ל-scoreboard |
    | ‏`end_of_elaboration_phase` | מלמטה למעלה | הדפסת הטופולוגיה, בדיקות שהכול מחובר |
    | ‏`run_phase` | במקביל, זמן סימולציה | ה-test מרים objection, מריץ sequences ומוריד objection |
    | ‏`extract` / `check` / `report` | מלמטה למעלה | בדיקות סוף : תורים ריקים ב-scoreboard, סיכום שגיאות |

    <!-- /gen -->

    **למה `build_phase` מלמעלה למטה.** ה-test קובע הגדרות (`config_db::set`, ‏factory
    overrides) **לפני** שה-env נוצר, וה-env לפני ה-agents. כך כל רכיב קורא את ההגדרות שלו
    ב-`build_phase` שלו, כשהן כבר קיימות.

    **למה objection.** ה-`run_phase` של כל הרכיבים רץ במקביל, וה-driver והמוניטורים רצים
    בלולאה אינסופית. UVM מסיים את הריצה רק כשאין אף objection מורם, וזה מה שאומר לו "ה-test
    סיים לייצר stimulus".

    **נסו בעצמכם.** לחיצה על רכיב בסכימה מראה מה הוא עושה, מה הוא לא עושה ואת הפונקציות
    החשובות שלו. "הצעד הבא" מעביר טרנזקציה לאורך המסלול, שלב אחרי שלב. במצב "חידון"
    התיבה שואלת "מי עושה את זה?" ואתם לוחצים על הרכיב :

    <div class="explorer" data-kind="uvmarch"></div>

---

### סעיף ג – החלטות תכנון

??? tip "רמז 1"
    חשבו על אותו בלוק אחרי שנה, בתוך סביבה של כל השבב : מי עוד מניע את הממשק שלו?

??? tip "רמז 2"
    מה קורה ל-scoreboard אם הוא מקבל את הטרנזקציות מה-driver, וה-driver עצמו מכיל באג?

??? success "פתרון סעיף ג"
    !!! answer "תשובה בקצרה"
        ה-driver והמוניטור נפרדים כי ברמת המערכת ה-driver נעלם (בלוק אחר מניע את הממשק)
        והמוניטור נשאר; וכי מוניטור עצמאי בודק גם את ה-driver. ה-agent של היציאה פסיבי
        כי ה-DUT מניע את היציאה. בסביבת מערכת כל ה-agents הפנימיים הופכים לפסיביים
        (`is_active = UVM_PASSIVE`), וה-scoreboards והמוניטורים עוברים כמו שהם.

    #### הרעיון { .sol-idea }

    **מי מניע ומי מסתכל.** בממשק יש בדיוק מקור אחד לכל אות. בסביבת הבלוק, ה-driver הוא
    המקור של ממשק הכניסה, וה-DUT של ממשק היציאה. בסביבת המערכת, הממשק של הבלוק מחובר
    לבלוק אחר, וה-driver חייב לרדת. מי שנשאר הוא המוניטור, ואיתו כל הבדיקות שמחוברות
    אליו. לכן כל מה שבודק נכונות "נתלה" על המוניטור, אף פעם לא על ה-driver.

    **עצמאות.** אם ה-scoreboard מקבל מה-driver את מה ש"נשלח", באג ב-driver (למשל ביט שנשכח)
    ייראה בשני הצדדים באותה צורה, וה-scoreboard יגיד שהכול בסדר. מוניטור שבנוי מהמפרט, לא
    מהקוד של ה-driver, הוא בדיקה שנייה ובלתי תלויה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏agent מוגדר :** שדה `is_active` (או אובייקט config) קובע אם ה-sequencer וה-driver
       נוצרים ב-`build_phase`.
    2. **רכיבים דרך ה-factory :** ‏`type_id::create` בכל מקום, כדי שה-test יוכל להחליף
       driver, item או sequence ב-override בלי לגעת בקוד.
    3. **‏env של מערכת :** משתמש ב-env של הבלוק כתת-env, עם agents פסיביים, ומוסיף
       scoreboards של מקצה לקצה.
    4. **כמה ממשקים :** ‏virtual sequence (על virtual sequencer או בלעדיו) מתאם sequences
       על כמה sequencers.

    </div>

    #### למה זה נכון { .sol-proof }

    **שימוש חוזר בלי שינוי.** בסביבת המערכת אותו agent, מאותו קוד, נוצר עם
    `UVM_PASSIVE` : אין driver שמתנגש עם הבלוק השכן, והמוניטור, ה-scoreboard וה-coverage
    ממשיכים לעבוד. אם בדיקה כלשהי הייתה בתוך ה-driver, היא הייתה נעלמת יחד איתו.

    **ה-factory.** ‏`new()` ישיר קובע את הטיפוס בזמן הקומפילציה. ‏`type_id::create` שואל את
    ה-factory, ולכן test אחד יכול להחליף את ה-driver ב-driver שמזריק שגיאות, ו-test אחר
    לא, בלי לשנות את ה-env.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : מוניטור שמשנה אותות"
    מוניטור "שעוזר" ומשנה `ready` או מנקה אות הוא כבר driver, ובסביבה פסיבית הוא יתנגש
    עם הבלוק האמיתי. המוניטור רק קורא.

??? trap "מלכודת : scoreboard שמקבל מה-driver או מה-sequence"
    כך ה-scoreboard בודק את מה שה-test **רצה** לשלוח, לא את מה שנשלח, ובאג של ה-driver
    עובר בלי שמישהו ירגיש. הצפוי מחושב ממוניטור הכניסה.

??? trap "מלכודת : לשכוח objection"
    ‏test שלא מרים objection נגמר מיד בזמן 0, ו"עובר" בלי שנשלחה אף טרנזקציה. test שמרים
    ולא מוריד נתקע עד ה-timeout. כדאי גם לבדוק בסוף שה-scoreboard ראה לפחות טרנזקציה אחת.

??? trap "מלכודת : `new()` במקום `type_id::create`"
    עובד, עד שמישהו מנסה override ב-factory ושום דבר לא משתנה. כל רכיב וכל item נוצרים
    דרך ה-factory.

??? followup "שאלות המשך"
    - **‏uvm_component מול uvm_object :** מה ההבדל, ולאיזו קטגוריה שייך sequence?

        ??? fu-answer "תשובה"
            ‏component קיים לכל אורך הסימולציה, יש לו מקום בהיררכיה ו-phases. ‏object נוצר ונעלם
            בזמן ריצה, בלי phases. ‏sequence ו-sequence item הם objects.

    - **‏get_next_item מול get :** מה ההבדל, ומתי משתמשים בכל אחד?

        ??? fu-answer "תשובה"
            ‏`get_next_item` משאיר את הפריט "בטיפול" עד `item_done`, ולכן ה-sequence חוסם עד
            שה-driver סיים. ‏`get` משחרר מיד. משתמשים ב-`get` כשה-driver מחזיק כמה פריטים בבת
            אחת (pipeline), ומחזיר תשובות ב-`put_response`.

    - **‏virtual sequencer :** מתי צריך אותו?

        ??? fu-answer "תשובה"
            כשטסט צריך לתאם sequences על כמה agents (למשל לכתוב בממשק אחד ולקרוא באחר). ה-virtual
            sequence מחזיק handles ל-sequencers האמיתיים ומריץ עליהם sequences.

    - **‏RAL :** איפה נכנס register model לסכימה?

        ??? fu-answer "תשובה"
            ה-register model נמצא ב-env, עם adapter שמתרגם פעולות רגיסטר ל-items של ה-agent של
            הבאס, ו-predictor שמעדכן את המודל מהמוניטור של הבאס.

    - **שני מוניטורים לממשק אחד :** האם זה רעיון טוב?

        ??? fu-answer "תשובה"
            לרוב לא : מוניטור אחד לממשק, ומספר מנויים ל-analysis port שלו. כך כל הצרכנים רואים
            בדיוק את אותן טרנזקציות.
