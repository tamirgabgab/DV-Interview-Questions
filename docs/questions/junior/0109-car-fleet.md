---
id: 109
title: שיירות של מכוניות – כמה מגיעות ליעד, ומתי כל מכונית משיגה
level: junior
difficulty: medium
kind: code
tags: [algorithms, sorting, stack, python, systemverilog]
source: "LeetCode 853 (Car Fleet) ו-LeetCode 1776 (Car Fleet II)"
added: 2026-11-13
---

## השאלה

על כביש עם נתיב אחד נוסעות \( n \) מכוניות באותו כיוון, אל יעד במקום `target`. מכונית \( i \)
מתחילה במקום `position[i]` ונוסעת במהירות קבועה `speed[i]`. כל המקומות שונים וקטנים מהיעד.
אסור לעקוף : מכונית שמשיגה את המכונית שלפניה נצמדת אליה, וממשיכה במהירות שלה. מכוניות צמודות
הן **שיירה** (fleet), וגם מכונית לבד היא שיירה. מכוניות שנפגשות בדיוק ביעד נחשבות לשיירה אחת.

**ההקשר באימות :** מודל ייחוס של ערוץ שאין בו עקיפות, כמו תור FIFO או צינור שמוציא פקודות לפי
הסדר. כל פריט היה מוכן בזמן משלו, אבל הוא לא יוצא לפני הפריט שלפניו. המודל צריך לדעת מתי יוצא
כל פריט ובכמה גלים, וזו בדיוק השאלה הזו.

**הדוגמה :** <span dir="ltr">target = 12</span>, <span dir="ltr">position = [10, 8, 0, 5, 3]</span>,
<span dir="ltr">speed = [2, 4, 1, 1, 3]</span>. התשובה 3. המכוניות מ-10 ומ-8 נפגשות בדיוק ביעד,
בזמן 1. המכונית מ-3 משיגה את זו מ-5 בזמן 1 במקום 6, ומשם הן נוסעות יחד במהירות 1 ומגיעות בזמן
7. המכונית מ-0 מגיעה לבד בזמן 12. בכל מכונית בציור כתובה המהירות שלה :

<!-- gen 0 -->

<svg class="figure cf-road" viewBox="0 0 640 108" direction="ltr" role="img" aria-label="הדוגמה בזמן 0 : היעד ב-12, והמכוניות במקומות 0, 3, 5, 8 ו-10 עם המהירויות 1, 3, 1, 4 ו-2"><line class="cf-lane" x1="16" x2="600.0" y1="62" y2="62"/><line class="cf-tickl" x1="30.0" x2="30.0" y1="58" y2="66"/><text class="tick" x="30.0" y="84" text-anchor="middle">0</text><line class="cf-tickl" x1="77.5" x2="77.5" y1="58" y2="66"/><line class="cf-tickl" x1="125.0" x2="125.0" y1="58" y2="66"/><text class="tick" x="125.0" y="84" text-anchor="middle">2</text><line class="cf-tickl" x1="172.5" x2="172.5" y1="58" y2="66"/><line class="cf-tickl" x1="220.0" x2="220.0" y1="58" y2="66"/><text class="tick" x="220.0" y="84" text-anchor="middle">4</text><line class="cf-tickl" x1="267.5" x2="267.5" y1="58" y2="66"/><line class="cf-tickl" x1="315.0" x2="315.0" y1="58" y2="66"/><text class="tick" x="315.0" y="84" text-anchor="middle">6</text><line class="cf-tickl" x1="362.5" x2="362.5" y1="58" y2="66"/><line class="cf-tickl" x1="410.0" x2="410.0" y1="58" y2="66"/><text class="tick" x="410.0" y="84" text-anchor="middle">8</text><line class="cf-tickl" x1="457.5" x2="457.5" y1="58" y2="66"/><line class="cf-tickl" x1="505.0" x2="505.0" y1="58" y2="66"/><text class="tick" x="505.0" y="84" text-anchor="middle">10</text><line class="cf-tickl" x1="552.5" x2="552.5" y1="58" y2="66"/><line class="cf-tickl" x1="600.0" x2="600.0" y1="58" y2="66"/><text class="tick" x="600.0" y="84" text-anchor="middle">12</text><line class="cf-goal" x1="600.0" x2="600.0" y1="18" y2="70"/><path class="cf-flag" d="M600.0,18 l16,6 l-16,6 Z"/><g class="cf-car"><title>car at 0, speed 1</title><rect x="17.0" y="28" width="26" height="22" rx="6"/><text x="30.0" y="44" text-anchor="middle">1</text><path class="cf-arrow" d="M46.0,34 l7,5 l-7,5 Z"/></g><g class="cf-car"><title>car at 3, speed 3</title><rect x="159.5" y="28" width="26" height="22" rx="6"/><text x="172.5" y="44" text-anchor="middle">3</text><path class="cf-arrow" d="M188.5,34 l7,5 l-7,5 Z"/></g><g class="cf-car"><title>car at 5, speed 1</title><rect x="254.5" y="28" width="26" height="22" rx="6"/><text x="267.5" y="44" text-anchor="middle">1</text><path class="cf-arrow" d="M283.5,34 l7,5 l-7,5 Z"/></g><g class="cf-car"><title>car at 8, speed 4</title><rect x="397.0" y="28" width="26" height="22" rx="6"/><text x="410.0" y="44" text-anchor="middle">4</text><path class="cf-arrow" d="M426.0,34 l7,5 l-7,5 Z"/></g><g class="cf-car"><title>car at 10, speed 2</title><rect x="492.0" y="28" width="26" height="22" rx="6"/><text x="505.0" y="44" text-anchor="middle">2</text><path class="cf-arrow" d="M521.0,34 l7,5 l-7,5 Z"/></g></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="cf-key-car"></i>מכונית, ובתוכה המהירות שלה</span><span><i class="cf-key-goal"></i>היעד</span></span>

<!-- /gen -->

- **סעיף א – כמה שיירות מגיעות :** כמה שיירות מגיעות ליעד? פתרו ב-\( O(n \log n) \). מכוניות
  נפגשות גם בזמנים שאינם שלמים, ומכונית נוסעת חלק מהזמן במהירות שלה וחלק במהירות של מי
  שלפניה. הסבירו איך נוסחה שלא מחשבת אף מפגש יכולה בכל זאת להיות נכונה.
- **סעיף ב – מתי כל מכונית משיגה :** עכשיו אין יעד, והכביש לא נגמר. המקומות נתונים בסדר עולה,
  כך שמכונית \( i \) נוסעת מאחורי מכונית \( i + 1 \). מתי כל מכונית משיגה את המכונית שלפניה,
  או את השיירה שזו כבר בתוכה? אם אף פעם לא, התשובה <span dir="ltr">−1</span>. פתרו ב-\( O(n) \).

??? interviewer "מה המראיין בודק"
    - **מהסיפור לנוסחה :** האם המועמד רואה שהזמן שבו מכונית מגיעה תלוי בשני מספרים בלבד, ולא בכל
      הסיפור של המפגשים.
    - **הוכחה ולא טריק :** האם הוא יודע להסביר למה מותר להתעלם מהזמן ומהמקום של מפגש.
    - **חשבון מדויק :** שוויון ביעד, וזמנים שמשווים בלי שגיאת עיגול.
    - **התנגשות אמיתית מול התנגשות על הנייר :** האם הוא שם לב שמכונית שכבר נבלעה בשיירה לא
      נוסעת יותר על הקו שלה.
    - **מחסנית מונוטונית :** מה נשמר בה, ולמה כל איבר נכנס ויוצא פעם אחת.

---

### סעיף א – כמה שיירות מגיעות

??? tip "רמז 1"
    התחילו מהמכונית הקרובה ביותר ליעד. מתי היא מגיעה? ומה אפשר להגיד על המכונית שמאחוריה, אם
    יודעים מתי זו שלפניה מגיעה?

??? tip "רמז 2"
    בלי לחשב איפה ומתי שתי מכוניות נפגשות : אילו שני חסמים תחתונים יש על הזמן שבו מכונית מגיעה
    ליעד? ומתי כל אחד מהם מושג?

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ממיינים את המכוניות מהקרובה ליעד. לכל מכונית \( t_i = (\mathrm{target} - p_i) / s_i \) הוא
        הזמן שבו הייתה מגיעה לבד, והזמן שבו היא מגיעה באמת הוא \( T_i = \max(t_i, T_{i-1}) \) : המקסימום
        של \( t \) מהמכונית הראשונה ועד אליה. שיירה חדשה מגיעה בכל פעם שהמקסימום **גדל ממש**
        (שוויון הוא מפגש ביעד), ומספר השיירות הוא מספר הפעמים האלה. בדוגמה \( t \) מהקרובה ליעד
        הוא 1, 1, 7, 3, 12, והמקסימום גדל שלוש פעמים.

    <!-- cost: זמן \( O(n \log n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **השאלה של הסעיף.** מכונית יכולה להשיג את זו שלפניה בזמן חצי ובמקום 1.5, ומשם להמשיך במהירות
    אחרת. נוסחה שלא יודעת מתי ואיפה זה קרה נראית חשודה. אבל הזמן שבו מכונית מגיעה ליעד לא תלוי
    במפגש עצמו, אלא רק בשני מספרים. נמיין את המכוניות מהקרובה ליעד, כך ש-\( i - 1 \) היא זו
    שלפני \( i \), ונסמן ב-\( T_i \) את הזמן שבו \( i \) מגיעה באמת.

    **שני חסמים תחתונים.** שניהם נכונים תמיד :

    - **לא מהר מהמהירות שלה :** בכל רגע המכונית נוסעת במהירות \( s_i \) או לאט יותר, ולכן הדרך
      \( \mathrm{target} - p_i \) לוקחת לפחות \( t_i \), כלומר \( T_i \ge t_i \).
    - **לא לפני מי שלפניה :** אסור לעקוף, ולכן היא לא מגיעה ליעד לפני מכונית \( i - 1 \), כלומר
      \( T_i \ge T_{i-1} \).

    **ואחד מהם מושג.** יש רק שתי אפשרויות :

    - **היא לא משיגה את \( i - 1 \) לפני היעד :** אף אחת לא מעכבת אותה. היא נוסעת כל הדרך במהירות
      שלה ומגיעה ב-\( t_i \).
    - **היא משיגה את \( i - 1 \) ברגע \( \tau \), שלם או לא, ובכל מקום :** מאותו רגע היא צמודה
      אליה, וגם אם \( i - 1 \) מאטה אחר כך, הן נשארות יחד. לכן היא מגיעה בדיוק כש-\( i - 1 \)
      מגיעה, ב-\( T_{i-1} \).

    בשני המקרים \( T_i \) שווה לאחד החסמים, ולכן לגדול מביניהם :

    \[
    T_i = \max(t_i,\ T_{i-1}) .
    \]

    הרגע \( \tau \), המקום של המפגש והמהירות שאחריו לא מופיעים בתשובה. במקרה השני הם רק מחלקים את
    הנסיעה לשני חלקים, וסכום החלקים הוא בדיוק \( T_{i-1} \).

    **דוגמה עם שבר.** היעד ב-10. מכונית B מתחילה ב-1 במהירות 1, ולבד הייתה מגיעה ב-\( t_B = 9 \).
    מכונית A מתחילה ב-0 במהירות 3, ולבד הייתה מגיעה ב-\( t_A = \tfrac{10}{3} \). היא משיגה את B
    כש-\( 3\tau = 1 + \tau \), כלומר ב-\( \tau = \tfrac{1}{2} \), במקום \( \tfrac{3}{2} \). משם
    היא נוסעת במהירות 1, והדרך שנשארה, \( 10 - \tfrac{3}{2} = \tfrac{17}{2} \), לוקחת
    \( \tfrac{17}{2} \). היא מגיעה ב-\( \tfrac{1}{2} + \tfrac{17}{2} = 9 \), וזה בדיוק
    \( \max(\tfrac{10}{3}, 9) \). בגרף הזמן על הציר האופקי והמקום על האנכי :

    <!-- gen 2 -->

    <svg class="perf-chart cf-graph" direction="ltr" viewBox="0 0 640 300" role="img" aria-label="שתי מכוניות והיעד ב-10 : A מ-0 במהירות 3 ו-B מ-1 במהירות 1. A משיגה את B בזמן חצי, במקום 1.5, ומשם נוסעת במהירות 1 ומגיעה בזמן 9, ולא בזמן 10 חלקי 3 של הקו החופשי שלה"><line class="grid" x1="44" x2="624" y1="262.0" y2="262.0"/><text class="tick" x="36" y="266.0" text-anchor="end">0</text><line class="grid" x1="44" x2="624" y1="212.8" y2="212.8"/><text class="tick" x="36" y="216.8" text-anchor="end">2</text><line class="grid" x1="44" x2="624" y1="163.6" y2="163.6"/><text class="tick" x="36" y="167.6" text-anchor="end">4</text><line class="grid" x1="44" x2="624" y1="114.4" y2="114.4"/><text class="tick" x="36" y="118.4" text-anchor="end">6</text><line class="grid" x1="44" x2="624" y1="65.2" y2="65.2"/><text class="tick" x="36" y="69.2" text-anchor="end">8</text><line class="grid" x1="44" x2="624" y1="16.0" y2="16.0"/><text class="tick" x="36" y="20.0" text-anchor="end">10</text><text class="tick" x="44.0" y="280" text-anchor="middle">0</text><text class="tick" x="105.1" y="280" text-anchor="middle">1</text><text class="tick" x="166.1" y="280" text-anchor="middle">2</text><text class="tick" x="227.2" y="280" text-anchor="middle">3</text><text class="tick" x="288.2" y="280" text-anchor="middle">4</text><text class="tick" x="349.3" y="280" text-anchor="middle">5</text><text class="tick" x="410.3" y="280" text-anchor="middle">6</text><text class="tick" x="471.4" y="280" text-anchor="middle">7</text><text class="tick" x="532.4" y="280" text-anchor="middle">8</text><text class="tick" x="593.5" y="280" text-anchor="middle">9</text><line class="cf-target" x1="44" x2="624" y1="16.0" y2="16.0"/><line class="cf-free cf-c0" x1="44.0" y1="262.0" x2="247.5" y2="16.0"><title>car 0: free line x = 0 + 3t</title></line><line class="cf-free cf-c0" x1="44.0" y1="237.4" x2="593.5" y2="16.0"><title>car 1: free line x = 1 + 1t</title></line><polyline class="cf-path cf-c0" points="44.0,262.0 74.5,225.1 593.5,16.0" fill="none" stroke-width="3.2"/><polyline class="cf-path cf-c0" points="44.0,237.4 593.5,16.0" fill="none" stroke-width="3.2"/><circle class="cf-meet" cx="74.5" cy="225.1" r="5.5"><title>t = 1/2, x = 3/2: car 0 reaches car 1</title></circle><text class="cf-lab" x="96.5" y="241.1" text-anchor="middle">τ = 1/2</text><text class="cf-lab" x="271.5" y="34.0" text-anchor="middle">10/3</text><text class="cf-lab" x="607.5" y="34.0" text-anchor="middle">9</text><line class="axis" x1="44" x2="624" y1="262" y2="262"/><line class="axis" x1="44" x2="44" y1="16" y2="262"/></svg>

    <!-- /gen -->

    <!-- gen 3 -->

    <span class="viz-legend"><span><i class="cf-key-free"></i>הקו החופשי : המקום אילו המכונית נסעה לבד</span><span><i class="cf-key-path"></i>הדרך האמיתית, בצבע של השיירה</span><span><i class="cf-key-meet"></i>מפגש</span><span><i class="cf-key-target"></i>היעד</span></span>

    <!-- /gen -->

    **התמונה : מקום מול זמן.** מכונית שנוסעת לבד היא קו ישר, \( x = p_i + s_i t \), הקו החופשי
    שלה. הדרך האמיתית של מכונית \( i \) היא

    \[
    x_i(t) = \min\bigl(p_i + s_i t,\ x_{i-1}(t)\bigr) ,
    \]

    כי היא לא יכולה להיות לפני המקום שהייתה מגיעה אליו לבד, ולא לפני המכונית שלפניה, וכל עוד היא
    מאחורי \( i - 1 \) היא נוסעת חופשי. כשפותחים את הנוסחה עד המכונית הראשונה, הדרך של \( i \) היא
    **המעטפת התחתונה** של הקווים החופשיים שלה ושל כל המכוניות שלפניה, עד היעד : בכל רגע, הנמוך
    מביניהם. השבירות של המעטפת הן המפגשים, בכל זמן ממשי, והשיפוע שלה הוא המהירות של אותו רגע. היא
    מגיעה לגובה של היעד רק כשכל הקווים כבר הגיעו אליו, ב-\( \max_j t_j \), וזה שוב \( T_i \).
    בדוגמה :

    <!-- gen 4 -->

    <svg class="perf-chart cf-graph" direction="ltr" viewBox="0 0 640 300" role="img" aria-label="המקום מול הזמן בדוגמה : הקווים החופשיים מקווקווים והדרכים האמיתיות מודגשות. המכוניות מ-8 ומ-10 נפגשות ביעד בזמן 1, המכונית מ-3 משיגה את זו מ-5 בזמן 1 במקום 6 ומגיעה איתה בזמן 7, והמכונית מ-0 מגיעה לבד בזמן 12. שלוש שיירות"><line class="grid" x1="44" x2="624" y1="262.0" y2="262.0"/><text class="tick" x="36" y="266.0" text-anchor="end">0</text><line class="grid" x1="44" x2="624" y1="221.0" y2="221.0"/><text class="tick" x="36" y="225.0" text-anchor="end">2</text><line class="grid" x1="44" x2="624" y1="180.0" y2="180.0"/><text class="tick" x="36" y="184.0" text-anchor="end">4</text><line class="grid" x1="44" x2="624" y1="139.0" y2="139.0"/><text class="tick" x="36" y="143.0" text-anchor="end">6</text><line class="grid" x1="44" x2="624" y1="98.0" y2="98.0"/><text class="tick" x="36" y="102.0" text-anchor="end">8</text><line class="grid" x1="44" x2="624" y1="57.0" y2="57.0"/><text class="tick" x="36" y="61.0" text-anchor="end">10</text><line class="grid" x1="44" x2="624" y1="16.0" y2="16.0"/><text class="tick" x="36" y="20.0" text-anchor="end">12</text><text class="tick" x="44.0" y="280" text-anchor="middle">0</text><text class="tick" x="90.4" y="280" text-anchor="middle">1</text><text class="tick" x="136.8" y="280" text-anchor="middle">2</text><text class="tick" x="183.2" y="280" text-anchor="middle">3</text><text class="tick" x="229.6" y="280" text-anchor="middle">4</text><text class="tick" x="276.0" y="280" text-anchor="middle">5</text><text class="tick" x="322.4" y="280" text-anchor="middle">6</text><text class="tick" x="368.8" y="280" text-anchor="middle">7</text><text class="tick" x="415.2" y="280" text-anchor="middle">8</text><text class="tick" x="461.6" y="280" text-anchor="middle">9</text><text class="tick" x="508.0" y="280" text-anchor="middle">10</text><text class="tick" x="554.4" y="280" text-anchor="middle">11</text><text class="tick" x="600.8" y="280" text-anchor="middle">12</text><line class="cf-target" x1="44" x2="624" y1="16.0" y2="16.0"/><line class="cf-free cf-c2" x1="44.0" y1="262.0" x2="600.8" y2="16.0"><title>car 0: free line x = 0 + 1t</title></line><line class="cf-free cf-c1" x1="44.0" y1="200.5" x2="183.2" y2="16.0"><title>car 1: free line x = 3 + 3t</title></line><line class="cf-free cf-c1" x1="44.0" y1="159.5" x2="368.8" y2="16.0"><title>car 2: free line x = 5 + 1t</title></line><line class="cf-free cf-c0" x1="44.0" y1="98.0" x2="90.4" y2="16.0"><title>car 3: free line x = 8 + 4t</title></line><line class="cf-free cf-c0" x1="44.0" y1="57.0" x2="90.4" y2="16.0"><title>car 4: free line x = 10 + 2t</title></line><polyline class="cf-path cf-c2" points="44.0,262.0 90.4,241.5 368.8,118.5 600.8,16.0" fill="none" stroke-width="3.2"/><polyline class="cf-path cf-c1" points="44.0,200.5 90.4,139.0 368.8,16.0" fill="none" stroke-width="3.2"/><polyline class="cf-path cf-c1" points="44.0,159.5 90.4,139.0 368.8,16.0" fill="none" stroke-width="3.2"/><polyline class="cf-path cf-c0" points="44.0,98.0 90.4,16.0" fill="none" stroke-width="3.2"/><polyline class="cf-path cf-c0" points="44.0,57.0 90.4,16.0" fill="none" stroke-width="3.2"/><circle class="cf-meet" cx="90.4" cy="139.0" r="5.5"><title>t = 1, x = 6: car 1 reaches car 2</title></circle><circle class="cf-meet" cx="90.4" cy="16.0" r="5.5"><title>t = 1, x = 12: car 3 reaches car 4</title></circle><line class="axis" x1="44" x2="624" y1="262" y2="262"/><line class="axis" x1="44" x2="44" y1="16" y2="262"/></svg>

    <!-- /gen -->

    <!-- gen 5 -->

    <span class="viz-legend"><span><i class="cf-key-free"></i>הקו החופשי : המקום אילו המכונית נסעה לבד</span><span><i class="cf-key-path"></i>הדרך האמיתית, בצבע של השיירה</span><span><i class="cf-key-meet"></i>מפגש</span><span><i class="cf-key-target"></i>היעד</span></span>

    <!-- /gen -->

    **למה מכונית לא משתחררת.** מינימום של קווים הוא פונקציה קעורה. לכן ההפרש
    \( f(t) = p_i + s_i t - x_{i-1}(t) \), קו פחות פונקציה קעורה, הוא פונקציה קמורה. הוא מתחיל
    שלילי, כי המכונית מאחור, ופונקציה קמורה שעלתה ל-0 כבר לא יורדת מתחתיו. לכן יש לכל היותר
    מפגש אחד : עד אליו המכונית חופשית, ואחריו היא צמודה עד הסוף. זה המקרה השני של ההוכחה, והוא
    יחזור בסעיף ב.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מיון :** ממיינים את הזוגות של מקום ומהירות לפי המקום, מהגדול לקטן.
    2. **הזמן לבד :** לכל מכונית \( t = (\mathrm{target} - p) / s \), כשבר מדויק.
    3. **המקסימום :** אם \( t > T \), מגיעה שיירה חדשה, ו-\( T \) מקבל את \( t \). אחרת המכונית
       מצטרפת לשיירה שלפניה, גם כש-\( t = T \) : אז הן נפגשות בדיוק ביעד.
    4. **התשובה :** מספר השיירות החדשות.

    </div>

    על הדוגמה, מהמכונית הקרובה ליעד. המקסימום המודגש הוא שיירה חדשה :

    <!-- gen 6 -->

    | המקום \( p \) | המהירות \( s \) | לבד, \( t = (12 - p) / s \) | ‏\( T \), המקסימום עד כאן | השיירה |
    |:-:|:-:|:-:|:-:|---|
    | 10 | 2 | 1 | **1** | שיירה חדשה, 1 |
    | 8 | 4 | 1 | 1 | מצטרפת ל-1, נפגשות ביעד |
    | 5 | 1 | 7 | **7** | שיירה חדשה, 2 |
    | 3 | 3 | 3 | 7 | מצטרפת ל-2 |
    | 0 | 1 | 12 | **12** | שיירה חדשה, 3 |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="car_fleets" linenums="1" hl_lines="9 11"
        from fractions import Fraction


        def car_fleets(target: int, position: list[int], speed: list[int]) -> int:
            """How many fleets reach the target: the cars from the front, each arriving at
            T = max(its time alone, T of the car ahead); a new fleet whenever T grows."""
            fleets, ahead = 0, Fraction(0)             # ahead: T of the car in front
            for p, s in sorted(zip(position, speed), reverse=True):   # (1)!
                alone = Fraction(target - p, s)        # (2)!
                if alone > ahead:                      # (3)!
                    fleets += 1
                    ahead = alone
            return fleets
        ```

        1. ‏`sorted` על זוגות ממיין לפי המקום, ו-`reverse=True` שם את הקרובה ליעד ראשונה. המקומות
           שונים, ולכן המהירות אף פעם לא שוברת שוויון.
        2. ‏`Fraction` שומר את הזמן כשבר מדויק, ולכן שוויון נבדק בדיוק (ראו המלכודת על מספרים
           עשרוניים).
        3. ‏`>` ולא `>=` : מכונית ש-\( t \) שלה שווה למקסימום משיגה את מי שלפניה בדיוק ביעד, והן
           שיירה אחת.

    === "SystemVerilog"
        ```systemverilog title="function car_fleets" linenums="1" hl_lines="9 12"
        // how many fleets reach the target: the cars from the front, a new fleet whenever the
        // time alone, (target - p) / s, is later than every time before it
        function automatic int car_fleets(int target, int position[], int speed[]);
          int order[$], fleets = 0, i;
          longint num = 0, den = 1;                          // T of the car in front, num / den
          foreach (position[k]) order.push_back(k);
          order.rsort() with (position[item]);               // (1)!
          foreach (order[k]) begin
            i = order[k];
            if (longint'(target - position[i]) * den > num * speed[i]) begin   // (2)!
              fleets++;
              num = target - position[i];
              den = speed[i];
            end
          end
          return fleets;
        endfunction
        ```

        1. ‏`rsort() with` ממיין את האינדקסים לפי המקום, מהגדול לקטן.
        2. ‏\( a / b > c / d \) בדיוק כש-\( a d > c b \), כשהמכנים חיוביים : השוואה מדויקת בלי חילוק.
           ‏`longint` כדי שהמכפלה לא תגלוש.

    #### למה זה נכון { .sol-proof }

    **באינדוקציה מהקרובה ליעד.** הראשונה לא מעוכבת אף פעם, ולכן \( T_1 = t_1 \). אם \( T_{i-1} \)
    נכון, הנימוק של הרעיון נותן \( T_i = \max(t_i, T_{i-1}) \) : שני החסמים נכונים תמיד, ואחד מהם
    מושג. המשתנה `ahead` מתעדכן רק כשהזמן לבד גדול ממנו, ולכן הוא תמיד \( T \) של המכונית האחרונה
    שנבדקה.

    **מי באותה שיירה.** מכונית \( i \) מגיעה עם \( i - 1 \) בדיוק כש-\( t_i \le T_{i-1} \) : אז היא
    משיגה אותה לפני היעד או בו. כש-\( t_i > T_{i-1} \) היא מגיעה אחריה, ולכן לא השיגה אותה. שתי
    שיירות לא מגיעות באותו זמן, כי אז היו נפגשות ביעד. לכן השיירות הן קטעים רצופים בסדר הממוין,
    וכל אחת מתחילה במכונית שבה המקסימום גדל ממש.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n \log n) \) למיון, ואחריו מעבר אחד.
    - **זיכרון :** ‏\( O(n) \) לזוגות הממוינים.
    - **בלי השוואות של מיון :** כשהמקומות שלמים וקטנים, מיון מנייה לפי המקום נותן
      \( O(n + \mathrm{target}) \).

    **נסו בעצמכם.** התיבה נפתחת על הדוגמה, והמכוניות בה ממוספרות לפי הסדר על הכביש, מ-0 מאחור.
    הזיזו את הפס לצעד של \( t = 1 \) : מכוניות 3 ו-4 נפגשות בדיוק ביעד, ובטבלה \( t \) שלהן שווה.
    בחרו "מפגש בזמן חצי" : בצעד של \( t = \tfrac{1}{2} \) מכונית 0 משיגה את 1 במקום
    \( \tfrac{3}{2} \), ובגרף הדרך שלה נשברת אל הקו של 1. לבסוף בחרו "שרשרת" : מכונית 0 לא משיגה
    אף פעם את הקו החופשי של 1, כי המהירות שלהן שווה, ובכל זאת מגיעה איתה, כי 1 האטה. מעבר
    לציורים, בתיבה רואים את הכביש בכל רגע, ואפשר לכתוב כל כביש עד 6 מכוניות :

    <div class="explorer" data-kind="carfleet" data-mode="fleets" data-target="12" data-pos="10.8.0.5.3" data-speed="2.4.1.1.3"></div>

---

### סעיף ב – מתי כל מכונית משיגה

??? tip "רמז 1"
    בסעיף א הדרך האמיתית של מכונית היא המעטפת התחתונה של הקווים החופשיים שלה ושל מי שלפניה.
    מכונית \( i \) משיגה את \( i + 1 \) כשהקו החופשי שלה פוגש את הדרך של \( i + 1 \). מאילו קווים
    הדרך הזו בנויה, ובאיזה סדר בזמן?

??? tip "רמז 2"
    עברו מהמכונית הקדמית אחורה. כשמכונית \( i \) מצאה את הרגע שבו היא משיגה, אילו קווים כבר לא
    יהיו חלק מהדרך שמכונית מאחוריה תפגוש?

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        עוברים מהמכונית הקדמית אחורה, עם מחסנית של המכוניות שהקווים החופשיים שלהן בונים את הדרך
        שלפנים, הקרובה למעלה. למכונית \( i \) : כל עוד למעלה יש מכונית \( j \), מוציאים אותה אם
        \( s_i \le s_j \) (אף פעם לא תשיג את הקו שלה), או אם הזמן שבו הייתה פוגשת את הקו שלה,
        \( (p_j - p_i) / (s_i - s_j) \), לא לפני \( c_j \), הרגע שבו \( j \) עצמה נבלעת. מה שנשאר
        למעלה נותן את \( c_i \), ומחסנית ריקה היא <span dir="ltr">−1</span>. בסוף \( i \) נכנסת
        למחסנית. בדוגמה של LeetCode, <span dir="ltr">position = [3, 5, 6, 9]</span> ו-<span dir="ltr">speed = [4, 4, 3, 1]</span>,
        התשובה <span dir="ltr">[2, 1, 1.5, −1]</span>. כל מכונית נכנסת ויוצאת לכל היותר פעם אחת,
        ולכן \( O(n) \).

    <!-- cost: זמן \( O(n) \) | זיכרון \( O(n) \) -->

    #### הרעיון { .sol-idea }

    **הנקודה העדינה.** הזמן שבו \( i \) הייתה פוגשת את הקו החופשי של \( i + 1 \) נכון רק אם
    \( i + 1 \) עוד נוסעת על הקו שלה באותו רגע, כלומר לפני שהיא עצמה נבלעה בשיירה איטית יותר.
    בדוגמה למכוניות 0 ו-1 אותה מהירות, 4, ולכן על הקו של 1 מכונית 0 לא משיגה אותה אף פעם. אבל 1
    משיגה את 2 בזמן 1 ומאטה ל-3, והשיירה משיגה את 3 בזמן \( \tfrac{3}{2} \) ומאטה ל-1. מכונית 0
    משיגה את השיירה בזמן 2. גם הקו של 2 לא עוזר : מכונית 0 חוצה אותו רק בזמן 3, ו-2 נמצאת בשיירה
    של 3 כבר מ-\( \tfrac{3}{2} \).

    **התמונה.** בלי יעד, הדרך של \( i + 1 \) היא המעטפת התחתונה של הקווים החופשיים של
    \( i + 1, i + 2, \dots \), כמו בסעיף א. היא בנויה מחלקים לפי הזמן : הקו של \( i + 1 \) עד
    \( c_{i+1} \), אחריו הקו של המכונית ש-\( i + 1 \) השיגה עד שגם היא נבלעת, וכן הלאה, והזמנים
    עולים. ‏\( c_i \) הוא הרגע הראשון שבו הקו של \( i \) פוגש את המעטפת, ולפי הקמירות של סעיף א יש
    לכל היותר רגע אחד כזה. לכן עוברים על החלקים לפי הסדר. בחלק של \( j \), שנגמר ב-\( c_j \), הקו
    של \( i \) פוגש את הקו של \( j \) ב-\( (p_j - p_i) / (s_i - s_j) \), אם \( s_i > s_j \). אם זה
    לפני \( c_j \), זה הרגע. אחרת הקו של \( i \) מתחת לכל החלק, ועוברים לחלק הבא.

    **המחסנית.** המחסנית מחזיקה בדיוק את החלקים האלה, והראשון בזמן למעלה. מה שיוצא בשביל \( i \)
    לא יחזור : בשביל המכוניות שמאחורי \( i \), הדרך שלפנים היא הקו של \( i \) עד \( c_i \), ואחריו
    רק החלקים שנגמרים אחרי \( c_i \). החלקים שיצאו נגמרים לפני כן. בגרף של הדוגמה כל מכונית בצבע
    שלה, וקטע שכמה מכוניות נוסעות בו יחד הוא בצבע של זו שבראש, כי השיירה נוסעת על הקו שלה :

    <!-- gen 7 -->

    <svg class="perf-chart cf-graph" direction="ltr" viewBox="0 0 640 300" role="img" aria-label="השרשרת של סעיף ב בלי יעד : מכוניות 0 עד 3 מהמקומות 3, 5, 6 ו-9 במהירויות 4, 4, 3 ו-1. מכונית 2 משיגה את 3 בזמן 3 חלקי 2, מכונית 1 את 2 בזמן 1, ומכונית 0 את השיירה בזמן 2. הקו החופשי של 0 חותך את הקו של 2 רק בזמן 3, אחרי ש-2 כבר נבלעה"><line class="grid" x1="44" x2="624" y1="243.1" y2="243.1"/><text class="tick" x="36" y="247.1" text-anchor="end">4</text><line class="grid" x1="44" x2="624" y1="205.2" y2="205.2"/><text class="tick" x="36" y="209.2" text-anchor="end">6</text><line class="grid" x1="44" x2="624" y1="167.4" y2="167.4"/><text class="tick" x="36" y="171.4" text-anchor="end">8</text><line class="grid" x1="44" x2="624" y1="129.5" y2="129.5"/><text class="tick" x="36" y="133.5" text-anchor="end">10</text><line class="grid" x1="44" x2="624" y1="91.7" y2="91.7"/><text class="tick" x="36" y="95.7" text-anchor="end">12</text><line class="grid" x1="44" x2="624" y1="53.8" y2="53.8"/><text class="tick" x="36" y="57.8" text-anchor="end">14</text><line class="grid" x1="44" x2="624" y1="16.0" y2="16.0"/><text class="tick" x="36" y="20.0" text-anchor="end">16</text><text class="tick" x="44.0" y="280" text-anchor="middle">0</text><text class="tick" x="222.5" y="280" text-anchor="middle">1</text><text class="tick" x="400.9" y="280" text-anchor="middle">2</text><text class="tick" x="579.4" y="280" text-anchor="middle">3</text><line class="cf-free cf-c0" x1="44.0" y1="262.0" x2="624.0" y2="16.0"><title>car 0: free line x = 3 + 4t</title></line><line class="cf-free cf-c1" x1="44.0" y1="224.2" x2="534.8" y2="16.0"><title>car 1: free line x = 5 + 4t</title></line><line class="cf-free cf-c2" x1="44.0" y1="205.2" x2="624.0" y2="20.7"><title>car 2: free line x = 6 + 3t</title></line><line class="cf-free cf-c3" x1="44.0" y1="148.5" x2="624.0" y2="87.0"><title>car 3: free line x = 9 + 1t</title></line><polyline class="cf-path cf-c0" points="44.0,262.0 222.5,186.3 281.9,161.1 311.7,148.5 400.9,110.6 579.4,91.7 624.0,87.0" fill="none" stroke-width="7.8"/><text class="cf-carno cf-c0" x="53.0" y="255.0" text-anchor="middle">0</text><polyline class="cf-path cf-c1" points="44.0,224.2 222.5,148.5 281.9,129.5 311.7,120.1 624.0,87.0" fill="none" stroke-width="6.2"/><text class="cf-carno cf-c1" x="53.0" y="217.2" text-anchor="middle">1</text><polyline class="cf-path cf-c2" points="44.0,205.2 311.7,120.1 624.0,87.0" fill="none" stroke-width="4.6"/><text class="cf-carno cf-c2" x="53.0" y="198.2" text-anchor="middle">2</text><polyline class="cf-path cf-c3" points="44.0,148.5 624.0,87.0" fill="none" stroke-width="3.0"/><text class="cf-carno cf-c3" x="53.0" y="141.5" text-anchor="middle">3</text><circle class="cf-ghost" cx="579.4" cy="34.9" r="5"><title>t = 3, x = 15: the lines cross, but too late</title></circle><circle class="cf-meet" cx="222.5" cy="148.5" r="5.5"><title>t = 1, x = 9: car 1 reaches car 2</title></circle><circle class="cf-meet" cx="311.7" cy="120.1" r="5.5"><title>t = 3/2, x = 21/2: car 2 reaches car 3</title></circle><circle class="cf-meet" cx="400.9" cy="110.6" r="5.5"><title>t = 2, x = 11: car 0 reaches car 1</title></circle><line class="axis" x1="44" x2="624" y1="262" y2="262"/><line class="axis" x1="44" x2="44" y1="16" y2="262"/></svg>

    <!-- /gen -->

    <!-- gen 8 -->

    <span class="viz-legend"><span><i class="cf-key-free"></i>הקו החופשי : המקום אילו המכונית נסעה לבד</span><span><i class="cf-key-path"></i>הדרך האמיתית, בצבע של המכונית : קטע משותף בצבע של המכונית שבראש</span><span><i class="cf-key-meet"></i>מפגש</span><span><i class="cf-key-ghost"></i>קווים שנחתכים מאוחר מדי : המכונית שלפנים כבר האטה</span></span>

    <!-- /gen -->

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **מהקדמית אחורה :** עוברים על \( i \) מ-\( n - 1 \) עד 0, עם מחסנית ריקה.
    2. **מוציאים :** כל עוד למעלה יש \( j \), ו-\( s_i \le s_j \) או שהמפגש עם הקו של \( j \) לא
       לפני \( c_j \), מוציאים את \( j \).
    3. **התשובה :** אם נשארה \( j \), אז \( c_i = (p_j - p_i) / (s_i - s_j) \). אחרת \( c_i = -1 \).
    4. **נכנסת :** מכונית \( i \) נכנסת למחסנית.

    </div>

    על הדוגמה. המחסנית רשומה מלמעלה למטה :

    <!-- gen 9 -->

    | המכונית | המקום \( p \) | המהירות \( s \) | המחסנית לפני, מלמעלה | מה קורה | הזמן |
    |:-:|:-:|:-:|:-:|---|:-:|
    | 3 | 9 | 1 | ריקה | אין לפניה אף אחת | ‏<span dir="ltr">−1</span> |
    | 2 | 6 | 3 | ‏<span dir="ltr">3</span> | פוגשת את הקו של 3 ב-\( \tfrac{3}{2} \) | ‏\( \tfrac{3}{2} \) |
    | 1 | 5 | 4 | ‏<span dir="ltr">2, 3</span> | פוגשת את הקו של 2 ב-1, לפני ש-2 נבלעת | 1 |
    | 0 | 3 | 4 | ‏<span dir="ltr">1, 2, 3</span> | מוציאים את 1 : 0 לא מהירה ממנה (4 מול 4). מוציאים את 2 : הקווים נפגשים ב-3, אבל 2 נבלעת כבר ב-\( \tfrac{3}{2} \). פוגשת את הקו של 3 ב-2 | 2 |

    <!-- /gen -->

    #### הקוד { .sol-code }

    === "Python"
        ```python title="collision_times" linenums="1" hl_lines="14 15 18"
        from fractions import Fraction


        def collision_times(position: list[int], speed: list[int]) -> list:
            """For every car (positions increasing: car i is behind car i + 1), the time it
            hits the car ahead, exact, or -1 when it never does."""
            n = len(position)
            times: list = [-1] * n
            stack: list[int] = []                      # the lines of the way ahead, nearest on top
            for i in range(n - 1, -1, -1):
                while stack:
                    j = stack[-1]
                    if speed[i] > speed[j]:
                        t = Fraction(position[j] - position[i], speed[i] - speed[j])   # (1)!
                        if times[j] == -1 or t < times[j]:                              # (2)!
                            times[i] = t
                            break
                    stack.pop()                                                        # (3)!
                stack.append(i)
            return times
        ```

        1. הרגע שבו \( i \) פוגשת את הקו החופשי של \( j \), כשבר מדויק.
        2. ‏\( j \) עוד נוסעת על הקו שלה ברגע הזה : היא לא נבלעת אף פעם, או נבלעת רק אחריו. עם `<=`
           הייתה יוצאת אותה תשובה (ראו ההוכחה).
        3. מגיעים לכאן כש-\( i \) לא מהירה מ-\( j \), או כשהמפגש מאוחר מדי : \( j \) כבר לא על
           הדרך שלפנים, לא בשביל \( i \) ולא בשביל מי שמאחוריה.

    === "SystemVerilog"
        ```systemverilog title="function collision_times" linenums="1" hl_lines="13 14 18"
        // for every car (positions increasing), the time it hits the car ahead as num[i] / den[i],
        // or den[i] = 0 when it never does; a / b < c / d is compared as a * d < c * b
        function automatic void collision_times(int position[], int speed[], output longint num[], output longint den[]);
          int n, j, stack[$];
          bit hit;
          n = position.size();
          num = new[n];
          den = new[n];                                      // (1)!
          for (int i = n - 1; i >= 0; i--) begin
            hit = 0;
            while (stack.size() > 0 && !hit) begin
              j = stack[$];
              if (speed[i] > speed[j] &&
                  (den[j] == 0 || longint'(position[j] - position[i]) * den[j] < num[j] * (speed[i] - speed[j]))) begin
                num[i] = position[j] - position[i];
                den[i] = speed[i] - speed[j];
                hit = 1;                                     // (2)!
              end else void'(stack.pop_back());
            end
            stack.push_back(i);
          end
        endfunction
        ```

        1. ‏`new[n]` מאתחל ל-0, ו-`den[i] == 0` אומר שאין התנגשות, כמו <span dir="ltr">−1</span>
           ב-Python.
        2. הדגל `hit` עוצר את הלולאה, במקום `break`.

    #### למה זה נכון { .sol-proof }

    **מה המחסנית מחזיקה.** נניח שאחרי הטיפול ב-\( i + 1 \) המחסנית, מלמעלה, היא
    \( j_1 = i + 1, j_2, \dots \), עם \( c_{j_1} < c_{j_2} < \dots \) והתחתונה עם
    <span dir="ltr">−1</span>, ושהדרך של \( i + 1 \) היא הקו של \( j_1 \) עד \( c_{j_1} \), אחריו
    הקו של \( j_2 \) עד \( c_{j_2} \), וכן הלאה.

    **החיפוש.** ההפרש \( f(t) = p_i + s_i t - x_{i+1}(t) \) קמור ומתחיל שלילי, ולכן יש לו לכל היותר
    אפס אחד, והוא \( c_i \). על החלק של \( j \), עד \( c_j \), ‏\( f \) הוא ההפרש בין שני קווים,
    והוא שלילי בתחילת החלק. אם \( s_i \le s_j \) הוא לא עולה, ולא מתאפס בחלק. אחרת הוא מתאפס
    ב-\( (p_j - p_i) / (s_i - s_j) \), וזה בתוך החלק בדיוק כשהרגע הזה לפני \( c_j \). כשהוא בדיוק
    \( c_j \), גם הקו של החלק הבא עובר שם, והבדיקה שלו נותנת את אותו רגע.

    **המחסנית נשארת כזו.** אחרי \( c_i \) מכונית \( i \) צמודה לדרך של \( i + 1 \), ולכן הדרך של
    \( i \) היא הקו שלה עד \( c_i \), ואחריו החלקים של \( i + 1 \) שנגמרים אחרי \( c_i \). זו בדיוק
    המחסנית אחרי ההוצאות, עם \( i \) למעלה, ו-\( c_i \) קטן מ-\( c_j \) של המכונית שמתחתיה.

    #### סיבוכיות { .sol-cost }

    - **זמן :** ‏\( O(n) \) : כל מכונית נכנסת פעם אחת ויוצאת לכל היותר פעם אחת.
    - **זיכרון :** ‏\( O(n) \) למחסנית ולתשובות.
    - **מול כל הזוגות :** בלי המחסנית, לכל מכונית בודקים את כל הקווים שלפניה, \( O(n^2) \).

    **נסו בעצמכם.** התיבה נפתחת על השרשרת, בלי יעד. לחצו "עד הסוף" : בטבלה מכונית 0 פוגשת את הקו
    של 3, ולא של 1 או של 2, וכל המפגשים בגרף מלאים. חזרו להתחלה ולכו צעד אחרי צעד : בצעד של
    \( t = 1 \) מכונית 1 משיגה את 2, ובצעד של \( t = \tfrac{3}{2} \) השיירה משיגה את 3. לבסוף לחצו
    "הגרלה" ובדקו בגרף שכל זמן בטבלה הוא נקודה שבה קו מקווקו פוגש את הדרך המודגשת שלפניו. בתיבה
    אפשר לראות את הכביש בכל רגע, גם בין המפגשים :

    <div class="explorer" data-kind="carfleet" data-mode="collide" data-target="12" data-pos="3.5.6.9" data-speed="4.4.3.1"></div>

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : זמנים במספרים עשרוניים"
    כל עוד כל זמן הוא חילוק אחד, השוואה של `float` בטוחה לקלטים קטנים : החילוק מעוגל נכון, ושני
    שברים שווים יוצאים אותו מספר. הבעיה מתחילה כשזמן נבנה מכמה פעולות, כמו בסימולציה. היעד ב-2,
    מכונית A מ-0 במהירות 7 ו-B מ-1 במהירות 1. מכונית A משיגה את B ב-\( \tau = \tfrac{1}{6} \),
    במקום \( \tfrac{7}{6} \), ומגיעה ב-\( \tfrac{1}{6} + \tfrac{5}{6} = 1 \), עם B. בחשבון של
    `float` יוצא 1.0000000000000002, מאוחר מ-B, והקוד סופר שתי שיירות. בחילוק של שלמים, כמו `/`
    על `int` ב-C או ב-SystemVerilog, זה גרוע יותר : עם היעד ב-10 ושתי מכוניות במהירות 3, מ-0 ומ-1,
    גם <span dir="ltr">10 / 3</span> וגם <span dir="ltr">9 / 3</span> יוצאים 3, והקוד מאחד שתי
    מכוניות שלא נפגשות אף פעם. משווים בשברים, או בכפל בהצלבה.

??? trap "מלכודת : שוויון ביעד נספר כשתי שיירות"
    בדוגמה המכוניות מ-10 ומ-8 היו מגיעות לבד שתיהן בזמן 1 : הן נפגשות בדיוק ביעד, והשאלה סופרת
    אותן כשיירה אחת. קוד שבודק `alone >= ahead` פותח שיירה חדשה גם בשוויון ומחזיר 4 במקום 3.

??? trap "מלכודת : להשוות רק לקו של המכונית שלפנים"
    הבדיקה "האם \( i \) משיגה את הקו החופשי של \( i - 1 \) לפני היעד" שוכחת ש-\( i - 1 \) יכולה
    להאט. היעד ב-10, מכונית C ב-6 במהירות 1, מכונית B ב-2 במהירות 4 ומכונית A ב-0 במהירות 3.
    מכונית B מהירה מ-A, ולכן A לא משיגה את הקו של B אף פעם. אבל B משיגה את C בזמן
    \( \tfrac{4}{3} \) ומגיעה איתה ב-4, ו-A, שלבד הייתה מגיעה ב-\( \tfrac{10}{3} \), משיגה את
    השיירה בזמן 3, במקום 9. זו שיירה אחת, והבדיקה אומרת שתיים. המקסימום רואה את זה בלי לחשב אף
    מפגש : \( \max(\tfrac{10}{3}, 4) = 4 \).

??? trap "מלכודת : סימולציה בצעדים של זמן"
    סימולציה שמזיזה את המכוניות בצעדים של שנייה מפספסת את מה שקורה בין הצעדים. בדוגמה עם השבר,
    ב-\( t = 1 \) מכונית A כבר ב-3 ו-B ב-2, כלומר A עקפה את B, אלא אם הקוד מתקן את זה. גם הגעות
    מתערבבות : היעד ב-20, ושתי מכוניות במהירות 2, מ-0 ומ-1, מגיעות ב-10 וב-\( \tfrac{19}{2} \). הן
    לא נפגשות אף פעם, אבל סימולציה שסופרת את המכוניות שעברו את היעד באותו צעד רואה את שתיהן
    ב-\( t = 10 \) ומחזירה שיירה אחת. וגם כשהיא נכונה, היא עולה זמן לפי האורך של הכביש, ולא לפי
    \( n \).

??? trap "מלכודת : לפגוש קו של מכונית שכבר נבלעה"
    בסעיף ב, הרגע שבו \( i \) פוגשת את הקו של \( i + 1 \) נכון רק כל עוד \( i + 1 \) לא נבלעה. בדוגמה,
    מי שבודק רק את השכנה מחזיר למכונית 0 את <span dir="ltr">−1</span>, כי למכוניות 0 ו-1 אותה
    מהירות. מי שעובר על המכוניות שלפנים לפי הסדר ולוקח את הקו הראשון שהוא חוצה מקבל 3, עם הקו של
    2. התשובה היא 2, עם הקו של 3 : בזמן 2 מכונית 3 היא זו שבראש השיירה.

??? followup "שאלות המשך"
    - **כמה שיירות ברגע \( T \) :** על הכביש של סעיף ב, כמה שיירות יש ברגע נתון \( T \)?

        ??? fu-answer "תשובה"
            מכונית \( i \) נמצאת באותה שיירה עם \( i + 1 \) בדיוק מהרגע \( c_i \). לכן מספר השיירות
            ברגע \( T \) הוא מספר המכוניות שעוד לא השיגו את זו שלפניהן : \( c_i = -1 \) או
            \( c_i > T \). בדוגמה, ברגע 1 אלה מכוניות 0, 2 ו-3, שלוש שיירות.

    - **יציאה לפי הסדר בחומרה :** פקודות במעבד מוכנות כל אחת בזמן משלה, אבל יוצאות מהצינור לפי
      הסדר. מתי יוצאת כל פקודה, ובכמה פרצים?

        ??? fu-answer "תשובה"
            אותו מקסימום : \( \mathrm{retire}_i = \max(\mathrm{ready}_i, \mathrm{retire}_{i-1}) \),
            כשהפקודה הראשונה בתור היא המכונית הקדמית ואין גבול לכמה יוצאות יחד. פקודה איטית בראש
            עוצרת את כל מה שמאחוריה (head-of-line blocking), וכל פרץ הוא שיירה. פקודות שמוכנות
            ב-5, 3, 4, 9, 8 יוצאות ב-5, 5, 5, 9, 9, בשני פרצים.

    - **הנמלים על המוט :** ב[שאלה 0057](0057-ants-on-a-pole.md) נמלים שנפגשות מסתובבות, ואפשר
      להעמיד פנים שהן עוברות זו דרך זו. למה הטריק הזה לא עובד כאן?

        ??? fu-answer "תשובה"
            שם לכל הנמלים אותה מהירות, ולכן מפגש שבו הן מסתובבות נראה מבחוץ כמו מעבר : אותה קבוצה
            של מקומות, וכל קו נשאר ישר. כאן מפגש משנה את המהירות של מי שמאחור, ולכן הדרך היא
            מינימום של קווים, מעטפת עם שבירות, ולא קבוצה של קווים ישרים.
