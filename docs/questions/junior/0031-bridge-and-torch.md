---
id: 31
title: הגשר והלפיד – ארבעה אנשים, שניים על הגשר
level: junior
difficulty: medium
tags: [logic-puzzles, algorithms, dijkstra, python, systemverilog]
source: ""
added: 2026-10-20
---

## השאלה

ארבעה אנשים מגיעים בלילה לגשר צר. יש להם **לפיד אחד**, ובלי לפיד אי אפשר לחצות. הגשר
מחזיק **לכל היותר שני אנשים** בבת אחת, ומי שחוצה בזוג הולך בקצב של **האיטי** מבין השניים.
זמני החצייה הם :

| האדם | ‏A | ‏B | ‏C | ‏D |
|---|:-:|:-:|:-:|:-:|
| דקות לחצייה | ‏1 | ‏2 | ‏5 | ‏10 |

הלפיד צריך לחזור עם מישהו כדי שהבאים יוכלו לחצות, ואי אפשר לזרוק אותו.

<!-- gen 0 -->

<svg class="figure bridge-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="ארבעה אנשים עם הלפיד על הגדה הקרובה של הגשר, עם הזמנים 1, 2, 5 ו-10 דקות"><rect class="bank" x="0" y="20" width="190" height="150" rx="8"/><rect class="bank" x="450" y="20" width="190" height="150" rx="8"/><rect class="river" x="190" y="20" width="260" height="150"/><rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/><text class="legend" x="95" y="160" text-anchor="middle">near</text><text class="legend" x="545" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="40" cy="60" r="17"/><text class="st-text" x="40" y="65" text-anchor="middle">1</text><text class="st-small" x="40" y="90" text-anchor="middle">A</text></g><g><circle class="st-cell" cx="80" cy="60" r="17"/><text class="st-text" x="80" y="65" text-anchor="middle">2</text><text class="st-small" x="80" y="90" text-anchor="middle">B</text></g><g><circle class="st-cell" cx="120" cy="60" r="17"/><text class="st-text" x="120" y="65" text-anchor="middle">5</text><text class="st-small" x="120" y="90" text-anchor="middle">C</text></g><g><circle class="st-cell" cx="160" cy="60" r="17"/><text class="st-text" x="160" y="65" text-anchor="middle">10</text><text class="st-small" x="160" y="90" text-anchor="middle">D</text></g><polygon class="torch" points="150,104 156,116 150,120 144,116"/><rect class="ink-fill" x="148.5" y="120" width="3" height="10"/><text class="legend" x="630" y="182" text-anchor="end" font-weight="700">t = 0</text></svg>

<!-- /gen -->

<!-- gen 1 -->

<span class="viz-legend"><span><i class="st-cell"></i>על הגדה הקרובה</span><span><i class="st-stack"></i>חוצים עכשיו</span><span><i class="st-ok"></i>כבר על הגדה הרחוקה</span><span><i class="torch"></i>הלפיד</span></span>

<!-- /gen -->

??? interviewer "מה המראיין בודק"
    - **הימנעות מהפתרון הראשון :** התוכנית הראשונה שעולה (המהיר מלווה את כולם) נותנת 19,
      והמועמד הטוב שואל אם אפשר פחות.
    - **זיהוי העלות הגדולה :** ה-10 וה-5 חייבים לחצות, והשאלה היא אם משלמים את שניהם או
      רק את הגדול.
    - **מודל של מצבים :** בסעיף ב, האם המועמד מגדיר מצב (מי חצה, איפה הלפיד), רואה שזה גרף
      עם משקלים, ובוחר את האלגוריתם הנכון.
    - **הוכחה קצרה :** למה אי אפשר פחות מ-17, בלי לעבור על כל האפשרויות ביד.

---

### סעיף א – ארבעה אנשים : 1, 2, 5 ו-10

מהו הזמן הקצר ביותר שבו כל הארבעה יהיו בצד הרחוק, ומה סדר החציות?

??? tip "רמז 1"
    מי מחזיר את הלפיד בכל פעם? זה לא חייב להיות אותו אדם.

??? tip "רמז 2"
    ‏C ו-D חייבים לחצות. אם כל אחד מהם חוצה עם A, משלמים גם 10 וגם 5. איך משלמים רק את
    ה-10?

??? tip "רמז 3"
    שלחו את A ואת B ראשונים, כדי שאחד מהם יחכה בצד הרחוק ויחזיר את הלפיד אחרי ש-C ו-D
    חצו יחד.

??? success "פתרון סעיף א"
    !!! answer "תשובה בקצרה"
        ‏17 דקות, ולא 19. ‏A ו-B חוצים (2), ‏A חוזר (1), ‏C ו-D חוצים יחד (10), ‏B חוזר (2),
        ‏A ו-B חוצים (2). שני האיטיים חוצים **יחד**, ולכן משלמים את ה-10 פעם אחת ואת ה-5
        בכלל לא.

    <!-- cost: חציות 5 -->

    #### הרעיון { .sol-idea }

    הזמן של חציית זוג הוא הזמן של האיטי. אם D חוצה עם A, הזמן של A "נבלע" ב-10, וכך גם
    כשמלווים את C : משלמים 10 ועוד 5. אבל אם C ו-D חוצים **באותו זוג**, הזמן של C נבלע
    ב-10, ומשלמים רק 10. המחיר של הרעיון : צריך מישהו מהיר שכבר מחכה בצד הרחוק כדי להחזיר
    את הלפיד, ולכן שולחים את שני המהירים קודם. סך הכול 2 + 1 + 10 + 2 + 2 = 17.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **‏A ו-B חוצים :** 2 דקות. ‏B נשאר בצד הרחוק כדי להחזיר את הלפיד אחר כך.
    2. **‏A חוזר עם הלפיד :** דקה. עברו 3 דקות.
    3. **‏C ו-D חוצים יחד :** 10 דקות. הזמן של C נבלע. עברו 13 דקות.
    4. **‏B חוזר עם הלפיד :** 2 דקות. עברו 15 דקות.
    5. **‏A ו-B חוצים :** 2 דקות. כולם בצד הרחוק אחרי 17 דקות.

    </div>

    #### למה זה נכון { .sol-proof }

    **חצייה אחרי חצייה.** לחצו "הבא" כדי לעקוב : מי על הגשר, איפה הלפיד, וכמה זמן עבר :

    <!-- gen 2 -->

    <div class="stepper" role="group" aria-label="התוכנית של 17 דקות, חצייה אחרי חצייה" tabindex="0"><figure class="stepper-frame is-active"><svg class="figure bridge-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="התחלה : כולם על הגדה הקרובה"><rect class="bank" x="0" y="20" width="190" height="150" rx="8"/><rect class="bank" x="450" y="20" width="190" height="150" rx="8"/><rect class="river" x="190" y="20" width="260" height="150"/><rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/><text class="legend" x="95" y="160" text-anchor="middle">near</text><text class="legend" x="545" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="40" cy="60" r="17"/><text class="st-text" x="40" y="65" text-anchor="middle">1</text><text class="st-small" x="40" y="90" text-anchor="middle">A</text></g><g><circle class="st-cell" cx="80" cy="60" r="17"/><text class="st-text" x="80" y="65" text-anchor="middle">2</text><text class="st-small" x="80" y="90" text-anchor="middle">B</text></g><g><circle class="st-cell" cx="120" cy="60" r="17"/><text class="st-text" x="120" y="65" text-anchor="middle">5</text><text class="st-small" x="120" y="90" text-anchor="middle">C</text></g><g><circle class="st-cell" cx="160" cy="60" r="17"/><text class="st-text" x="160" y="65" text-anchor="middle">10</text><text class="st-small" x="160" y="90" text-anchor="middle">D</text></g><polygon class="torch" points="150,104 156,116 150,120 144,116"/><rect class="ink-fill" x="148.5" y="120" width="3" height="10"/><text class="legend" x="630" y="182" text-anchor="end" font-weight="700">t = 0</text></svg><figcaption>רגע 0 : כולם והלפיד על הגדה הקרובה. הגשר מחזיק שניים, והזוג הולך בקצב האיטי.</figcaption></figure><figure class="stepper-frame"><svg class="figure bridge-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 1"><rect class="bank" x="0" y="20" width="190" height="150" rx="8"/><rect class="bank" x="450" y="20" width="190" height="150" rx="8"/><rect class="river" x="190" y="20" width="260" height="150"/><rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/><text class="legend" x="95" y="160" text-anchor="middle">near</text><text class="legend" x="545" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="40" cy="60" r="17"/><text class="st-text" x="40" y="65" text-anchor="middle">5</text><text class="st-small" x="40" y="90" text-anchor="middle">C</text></g><g><circle class="st-cell" cx="80" cy="60" r="17"/><text class="st-text" x="80" y="65" text-anchor="middle">10</text><text class="st-small" x="80" y="90" text-anchor="middle">D</text></g><g><circle class="st-stack" cx="290" cy="95" r="17"/><text class="st-text" x="290" y="100" text-anchor="middle">1</text><text class="st-small" x="290" y="125" text-anchor="middle">A</text></g><g><circle class="st-stack" cx="350" cy="95" r="17"/><text class="st-text" x="350" y="100" text-anchor="middle">2</text><text class="st-small" x="350" y="125" text-anchor="middle">B</text></g><line class="ink-line" x1="236" y1="128" x2="404" y2="128" stroke-width="2"/><polygon class="ink-fill" points="404,128 395,123 395,133"/><polygon class="torch" points="320,136 326,148 320,152 314,148"/><rect class="ink-fill" x="318.5" y="152" width="3" height="10"/><text class="legend" x="630" y="182" text-anchor="end" font-weight="700">t = 2</text></svg><figcaption>חצייה 1 : A (1) ו-B (2) חוצים קדימה, 2 דקות. עברו 2 דקות.</figcaption></figure><figure class="stepper-frame"><svg class="figure bridge-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 2"><rect class="bank" x="0" y="20" width="190" height="150" rx="8"/><rect class="bank" x="450" y="20" width="190" height="150" rx="8"/><rect class="river" x="190" y="20" width="260" height="150"/><rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/><text class="legend" x="95" y="160" text-anchor="middle">near</text><text class="legend" x="545" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="40" cy="60" r="17"/><text class="st-text" x="40" y="65" text-anchor="middle">5</text><text class="st-small" x="40" y="90" text-anchor="middle">C</text></g><g><circle class="st-cell" cx="80" cy="60" r="17"/><text class="st-text" x="80" y="65" text-anchor="middle">10</text><text class="st-small" x="80" y="90" text-anchor="middle">D</text></g><g><circle class="st-ok" cx="490" cy="60" r="17"/><text class="st-text" x="490" y="65" text-anchor="middle">2</text><text class="st-small" x="490" y="90" text-anchor="middle">B</text></g><g><circle class="st-stack" cx="290" cy="95" r="17"/><text class="st-text" x="290" y="100" text-anchor="middle">1</text><text class="st-small" x="290" y="125" text-anchor="middle">A</text></g><line class="ink-line" x1="404" y1="128" x2="236" y2="128" stroke-width="2"/><polygon class="ink-fill" points="236,128 245,123 245,133"/><polygon class="torch" points="320,136 326,148 320,152 314,148"/><rect class="ink-fill" x="318.5" y="152" width="3" height="10"/><text class="legend" x="630" y="182" text-anchor="end" font-weight="700">t = 3</text></svg><figcaption>חצייה 2 : A (1) חוזר עם הלפיד חזרה, 1 דקות. עברו 3 דקות.</figcaption></figure><figure class="stepper-frame"><svg class="figure bridge-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 3"><rect class="bank" x="0" y="20" width="190" height="150" rx="8"/><rect class="bank" x="450" y="20" width="190" height="150" rx="8"/><rect class="river" x="190" y="20" width="260" height="150"/><rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/><text class="legend" x="95" y="160" text-anchor="middle">near</text><text class="legend" x="545" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="40" cy="60" r="17"/><text class="st-text" x="40" y="65" text-anchor="middle">1</text><text class="st-small" x="40" y="90" text-anchor="middle">A</text></g><g><circle class="st-ok" cx="490" cy="60" r="17"/><text class="st-text" x="490" y="65" text-anchor="middle">2</text><text class="st-small" x="490" y="90" text-anchor="middle">B</text></g><g><circle class="st-stack" cx="290" cy="95" r="17"/><text class="st-text" x="290" y="100" text-anchor="middle">5</text><text class="st-small" x="290" y="125" text-anchor="middle">C</text></g><g><circle class="st-stack" cx="350" cy="95" r="17"/><text class="st-text" x="350" y="100" text-anchor="middle">10</text><text class="st-small" x="350" y="125" text-anchor="middle">D</text></g><line class="ink-line" x1="236" y1="128" x2="404" y2="128" stroke-width="2"/><polygon class="ink-fill" points="404,128 395,123 395,133"/><polygon class="torch" points="320,136 326,148 320,152 314,148"/><rect class="ink-fill" x="318.5" y="152" width="3" height="10"/><text class="legend" x="630" y="182" text-anchor="end" font-weight="700">t = 13</text></svg><figcaption>חצייה 3 : C (5) ו-D (10) חוצים קדימה, 10 דקות. עברו 13 דקות.</figcaption></figure><figure class="stepper-frame"><svg class="figure bridge-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 4"><rect class="bank" x="0" y="20" width="190" height="150" rx="8"/><rect class="bank" x="450" y="20" width="190" height="150" rx="8"/><rect class="river" x="190" y="20" width="260" height="150"/><rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/><text class="legend" x="95" y="160" text-anchor="middle">near</text><text class="legend" x="545" y="160" text-anchor="middle">far</text><g><circle class="st-cell" cx="40" cy="60" r="17"/><text class="st-text" x="40" y="65" text-anchor="middle">1</text><text class="st-small" x="40" y="90" text-anchor="middle">A</text></g><g><circle class="st-ok" cx="490" cy="60" r="17"/><text class="st-text" x="490" y="65" text-anchor="middle">5</text><text class="st-small" x="490" y="90" text-anchor="middle">C</text></g><g><circle class="st-ok" cx="530" cy="60" r="17"/><text class="st-text" x="530" y="65" text-anchor="middle">10</text><text class="st-small" x="530" y="90" text-anchor="middle">D</text></g><g><circle class="st-stack" cx="290" cy="95" r="17"/><text class="st-text" x="290" y="100" text-anchor="middle">2</text><text class="st-small" x="290" y="125" text-anchor="middle">B</text></g><line class="ink-line" x1="404" y1="128" x2="236" y2="128" stroke-width="2"/><polygon class="ink-fill" points="236,128 245,123 245,133"/><polygon class="torch" points="320,136 326,148 320,152 314,148"/><rect class="ink-fill" x="318.5" y="152" width="3" height="10"/><text class="legend" x="630" y="182" text-anchor="end" font-weight="700">t = 15</text></svg><figcaption>חצייה 4 : B (2) חוזר עם הלפיד חזרה, 2 דקות. עברו 15 דקות.</figcaption></figure><figure class="stepper-frame"><svg class="figure bridge-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="חצייה 5"><rect class="bank" x="0" y="20" width="190" height="150" rx="8"/><rect class="bank" x="450" y="20" width="190" height="150" rx="8"/><rect class="river" x="190" y="20" width="260" height="150"/><rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/><text class="legend" x="95" y="160" text-anchor="middle">near</text><text class="legend" x="545" y="160" text-anchor="middle">far</text><g><circle class="st-ok" cx="490" cy="60" r="17"/><text class="st-text" x="490" y="65" text-anchor="middle">5</text><text class="st-small" x="490" y="90" text-anchor="middle">C</text></g><g><circle class="st-ok" cx="530" cy="60" r="17"/><text class="st-text" x="530" y="65" text-anchor="middle">10</text><text class="st-small" x="530" y="90" text-anchor="middle">D</text></g><g><circle class="st-stack" cx="290" cy="95" r="17"/><text class="st-text" x="290" y="100" text-anchor="middle">1</text><text class="st-small" x="290" y="125" text-anchor="middle">A</text></g><g><circle class="st-stack" cx="350" cy="95" r="17"/><text class="st-text" x="350" y="100" text-anchor="middle">2</text><text class="st-small" x="350" y="125" text-anchor="middle">B</text></g><line class="ink-line" x1="236" y1="128" x2="404" y2="128" stroke-width="2"/><polygon class="ink-fill" points="404,128 395,123 395,133"/><polygon class="torch" points="320,136 326,148 320,152 314,148"/><rect class="ink-fill" x="318.5" y="152" width="3" height="10"/><text class="legend" x="630" y="182" text-anchor="end" font-weight="700">t = 17</text></svg><figcaption>חצייה 5 : A (1) ו-B (2) חוצים קדימה, 2 דקות. עברו 17 דקות.</figcaption></figure><figure class="stepper-frame"><svg class="figure bridge-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="סיום"><rect class="bank" x="0" y="20" width="190" height="150" rx="8"/><rect class="bank" x="450" y="20" width="190" height="150" rx="8"/><rect class="river" x="190" y="20" width="260" height="150"/><rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/><text class="legend" x="95" y="160" text-anchor="middle">near</text><text class="legend" x="545" y="160" text-anchor="middle">far</text><g><circle class="st-ok" cx="490" cy="60" r="17"/><text class="st-text" x="490" y="65" text-anchor="middle">1</text><text class="st-small" x="490" y="90" text-anchor="middle">A</text></g><g><circle class="st-ok" cx="530" cy="60" r="17"/><text class="st-text" x="530" y="65" text-anchor="middle">2</text><text class="st-small" x="530" y="90" text-anchor="middle">B</text></g><g><circle class="st-ok" cx="570" cy="60" r="17"/><text class="st-text" x="570" y="65" text-anchor="middle">5</text><text class="st-small" x="570" y="90" text-anchor="middle">C</text></g><g><circle class="st-ok" cx="610" cy="60" r="17"/><text class="st-text" x="610" y="65" text-anchor="middle">10</text><text class="st-small" x="610" y="90" text-anchor="middle">D</text></g><polygon class="torch" points="490,104 496,116 490,120 484,116"/><rect class="ink-fill" x="488.5" y="120" width="3" height="10"/><text class="legend" x="630" y="182" text-anchor="end" font-weight="700">t = 17</text></svg><figcaption>כולם על הגדה הרחוקה אחרי 17 דקות.</figcaption></figure><div class="stepper-nav"><button type="button" class="stepper-btn stepper-prev">הקודם</button><span class="stepper-pos" data-total="7"></span><button type="button" class="stepper-btn stepper-next">הבא</button></div></div>

    <!-- /gen -->

    <!-- gen 3 -->

    | חצייה | מי | לאן | הזמן | סה"כ |
    |:-:|---|---|:-:|:-:|
    | 1 | ‏A (1) ו-B (2) | קדימה | 2 | 2 |
    | 2 | ‏A (1) | חזרה | 1 | 3 |
    | 3 | ‏C (5) ו-D (10) | קדימה | 10 | 13 |
    | 4 | ‏B (2) | חזרה | 2 | 15 |
    | 5 | ‏A (1) ו-B (2) | קדימה | 2 | 17 |

    <!-- /gen -->

    **למה 19 היא המלכודת.** התוכנית הטבעית היא ש-A, המהיר, מלווה כל אחד ומחזיר את הלפיד :
    ‏A+D (10), ‏A חוזר (1), ‏A+C (5), ‏A חוזר (1), ‏A+B (2). סך הכול 19. היא משלמת את
    ה-10 **וגם** את ה-5. בתוכנית של 17 משלמים את ה-10 פעם אחת, ובמקום ה-5 משלמים פעמיים
    את ה-2 (‏B חוצה פעמיים) ועוד פעם אחת את ה-1 :

    <!-- gen 4 -->

    | האסטרטגיה | החציות | הזמן |
    |---|---|:-:|
    | המהיר מלווה את כולם | ‏A+D, ‏A, ‏A+C, ‏A, ‏A+B | ‏19 |
    | שני האיטיים חוצים יחד | ‏A+B, ‏A, ‏C+D, ‏B, ‏A+B | ‏17 |
    | אותו רעיון, בסדר אחר | ‏A+B, ‏B, ‏C+D, ‏A, ‏A+B | ‏17 |

    <!-- /gen -->

    **למה אי אפשר פחות מ-17.** צריכות להיות לפחות חמש חציות : שלוש קדימה (כל חצייה קדימה
    מעבירה לכל היותר שני אנשים, ואחרי שתיים נשארים עוד אנשים) ושתיים חזרה (אחרי כל חצייה
    קדימה חוץ מהאחרונה הלפיד חייב לחזור). ‏D חוצה קדימה פעם אחת לפחות, וזה 10. נשארות
    ארבע חציות אחרות, וכל אחת מהן לוקחת לפחות את הזמן של האדם המהיר ביותר בה.
    אם C לא חוצה עם D, יש חצייה נוספת של 5 לפחות, ושלוש חציות נוספות של 1 לפחות :
    ‏\( 10 + 5 + 3 = 18 \). אם C חוצה עם D, מישהו היה צריך להגיע לצד הרחוק לפני כן
    ולהישאר שם (חצייה קדימה של 2 לפחות, כי A לבד לא יכול להישאר ולהחזיר את הלפיד), והלפיד
    חוזר פעמיים (‏1 ו-2 לפחות, כי אותו אדם לא יכול להיות בשני הצדדים), ואז החצייה
    האחרונה של 2 : ‏\( 2 + 1 + 10 + 2 + 2 = 17 \). שני המקרים נותנים 17 לפחות.

    #### סיבוכיות { .sol-cost }

    חמש חציות, ולא יותר : כל תוכנית לארבעה אנשים צריכה בדיוק חמש. מספר התוכניות השונות
    קטן (כמה עשרות), ובסעיף ב החיפוש עובר על כולן בשבריר שנייה.

---

### סעיף ב – קוד : כל מספר אנשים

כתבו פונקציה שמקבלת רשימת זמני חצייה (עד שמונה אנשים) ומחזירה את הזמן הקצר ביותר ואת
סדר החציות. הקוד צריך להיות קריא, ולא לנחש כלל : הוא צריך למצוא את המינימום בוודאות.

??? tip "רמז 1"
    מה צריך לדעת כדי לתאר את המצב באמצע? מי כבר חצה, ואיפה הלפיד. כמה מצבים כאלה יש
    עם \( N \) אנשים?

??? tip "רמז 2"
    חצייה היא מעבר בין שני מצבים, עם מחיר. מה המחיר, ולמה BFS רגיל לא מספיק?

??? tip "רמז 3"
    זה מסלול קצר ביותר בגרף עם משקלים חיוביים : Dijkstra, כמו בשאלה
    [0019](../senior/0019-hourglass-measure-interval.md).

??? success "פתרון סעיף ב"
    !!! answer "תשובה בקצרה"
        המצב הוא (מי בצד הרחוק, איפה הלפיד) : ‏\( 2^N \cdot 2 \) מצבים. קשת היא חצייה של אדם
        אחד או שניים מהגדה שבה הלפיד, במחיר הזמן של האיטי. מריצים **Dijkstra** מ"כולם
        בצד הקרוב, הלפיד בצד הקרוב" עד "כולם בצד הרחוק", ומשחזרים את החציות דרך ההורים.

    <!-- cost: זמן \( O(S N^2 \log S) \) | זיכרון \( O(S) \) | מצבים \( 2^N \cdot 2 \) -->

    #### הרעיון { .sol-idea }

    **המצב.** מסכת ביטים של מי בצד הרחוק, ועוד ביט לצד של הלפיד. כל מה שקרה קודם לא
    משנה : מכאן והלאה האפשרויות תלויות רק במי בכל צד ואיפה הלפיד. הזמן שעבר **לא** חלק
    מהמצב, הוא המחיר של המסלול, בדיוק כמו בשאלה 0019.

    **הקשתות.** מהמצב הנוכחי, כל קבוצה של אדם אחד או שניים **מהגדה של הלפיד** יכולה
    לחצות. המחיר הוא הזמן של האיטי בקבוצה, והלפיד עובר לצד השני. BFS סופר קשתות ולא זמן,
    ולכן הוא מוצא את התוכנית עם הכי מעט חציות, שאיננה בהכרח המהירה. עם מחירים חיוביים
    המסלול הזול ביותר הוא בדיוק מה ש-Dijkstra מוצא.

    **השחזור.** לכל מצב שומרים מאיזה מצב הגיעו אליו הכי בזול ומי חצה. בסוף הולכים מהמצב
    הסופי אחורה עד ההתחלה, והופכים את הרשימה.

    #### השלבים { .sol-steps }

    <div class="steps" markdown>

    1. **אתחול :** המרחק של המצב ההתחלתי הוא 0, ושל כל השאר אינסוף.
    2. **הוצאה :** מוציאים את המצב עם המרחק הקטן ביותר שעוד לא טופל. אם כולם בצד הרחוק,
       סיימנו.
    3. **הרחבה :** לכל קבוצה של אחד או שניים מהגדה של הלפיד מחשבים את המצב החדש ואת
       המחיר. אם מצאנו דרך זולה יותר למצב הזה, מעדכנים את המרחק ואת ההורה.
    4. **שחזור :** מהמצב הסופי הולכים אחורה לפי ההורים ואוספים את החציות.

    </div>

    #### הקוד { .sol-code }

    === "SystemVerilog"
        ```systemverilog title="bridge_time" linenums="1" hl_lines="22 23 24 25 26 27 28 29 30 31 32 33"
        localparam int MAXN   = 8;
        localparam int STATES = 2 * (1 << MAXN);     // (who is across) * 2 + (torch side)
        localparam int INF    = 1 << 30;

        // The least time for everyone to cross; `plan` lists the crossings, e.g. "AB> A< CD> B< AB>".
        function automatic int bridge_time(int n, int times[MAXN], output string plan);
          int everyone = (1 << n) - 1;
          int reach[STATES];                        // the best time known to reach each state
          int prev[STATES];                         // the state before it on that path
          int via[STATES];                          // the mask of the people who crossed
          bit closed[STATES];
          int cur, pick, across, side, cost, nxt;
          string who;

          foreach (reach[s]) begin reach[s] = INF; prev[s] = -1; closed[s] = 0; end
          reach[0] = 0;                             // nobody across, the torch on the near bank
          for (int k = 0; k < 2 * (1 << n); k++) begin
            cur = -1; pick = INF;
            for (int s = 0; s < 2 * (1 << n); s++)
              if (!closed[s] && reach[s] < pick) begin pick = reach[s]; cur = s; end   // (1)!
            if (cur < 0) break;                     // nothing reachable is left
            closed[cur] = 1;
            across = cur >> 1;
            side   = cur & 1;
            if (across == everyone) break;
            for (int i = 0; i < n; i++) begin
              if (((across >> i) & 1) != side) continue;       // i is not on the torch's bank
              for (int j = i; j < n; j++) begin                  // j == i: one person crosses (2)
                if (((across >> j) & 1) != side) continue;
                cost = times[i] > times[j] ? times[i] : times[j];
                nxt  = ((across ^ (1 << i) ^ (j == i ? 0 : 1 << j)) << 1) | (1 - side);
                if (reach[cur] + cost < reach[nxt]) begin        // (3)!
                  reach[nxt] = reach[cur] + cost;
                  prev[nxt]  = cur;
                  via[nxt]   = (1 << i) | (1 << j);
                end
              end
            end
          end

          plan = "";                                // walk the parents back and write the crossings in order
          for (int s = (everyone << 1) | 1; prev[s] >= 0; s = prev[s]) begin
            who = "";
            for (int i = 0; i < n; i++)
              if (via[s] & (1 << i)) who = {who, $sformatf("%c", "A" + i)};
            plan = {who, (s & 1) ? ">" : "<", (plan == "") ? "" : " ", plan};
          end
          return reach[(everyone << 1) | 1];
        endfunction
        ```

        1. בחירת המצב הפתוח עם המרחק הקטן ביותר בסריקה : ‏\( O(S) \) לכל הוצאה במקום ערימה.
           עם \( S \le 512 \) זה פשוט יותר וגם מהיר.
        2. הלולאה הפנימית מתחילה מ-\( j = i \) : כש-\( j = i \) אדם אחד חוצה, אחרת שניים.
           המסכה \( (1 \ll i) \mid (1 \ll j) \) נכונה בשני המקרים.
        3. השחרור (relax) : רק דרך זולה יותר מעדכנת את המרחק, ההורה ומי חצה.

    === "Python"
        ```python title="bridge" linenums="1" hl_lines="17 18 19 20 21 22 23 24"
        import heapq
        from itertools import combinations


        def bridge(times):
            """The least time for everyone to cross, and the crossings as tuples of indices."""
            n = len(times)
            everyone = (1 << n) - 1
            start = (0, 0)                          # (who is across, torch side: 0 near, 1 far)
            best = {start: 0}
            parent = {start: None}
            queue = [(0, start)]
            while queue:
                t, state = heapq.heappop(queue)
                if t > best[state]:
                    continue                        # a stale entry: this state was reached faster (1)
                across, side = state
                if across == everyone:
                    break
                bank = [i for i in range(n) if ((across >> i) & 1) == side]     # (2)!
                for group in [(i,) for i in bank] + list(combinations(bank, 2)):
                    cost = t + max(times[i] for i in group)                      # (3)!
                    new = (across ^ sum(1 << i for i in group), 1 - side)
                    if cost < best.get(new, float("inf")):                       # (4)!
                        best[new] = cost
                        parent[new] = (state, group)
                        heapq.heappush(queue, (cost, new))
            moves, state = [], (everyone, 1)
            while parent[state] is not None:                                     # (5)!
                state, group = parent[state]
                moves.append(group)
            return best[(everyone, 1)], moves[::-1]
        ```

        1. רשומה ישנה בערימה : המצב כבר הושג בזמן קטן יותר, וזורקים אותה.
        2. מי נמצא בגדה של הלפיד : הביט שלו במסכה שווה לצד של הלפיד.
        3. המחיר של קבוצה הוא הזמן של האיטי בה.
        4. השחרור של Dijkstra : רק דרך זולה יותר נכנסת לערימה, עם ההורה ומי חצה.
        5. השחזור : מהמצב הסופי אחורה עד ההתחלה, ואז הופכים.

    #### למה זה נכון { .sol-proof }

    **הגרף נכון.** כל תוכנית חוקית היא מסלול בגרף : כל חצייה מעבירה אחד או שניים מהגדה
    של הלפיד, הלפיד עובר איתם, והזמן שלה הוא הזמן של האיטי. ובכיוון ההפוך, כל מסלול הוא
    תוכנית חוקית. המצב מכיל את כל מה שמשפיע על ההמשך, ולכן אין צורך לזכור את ההיסטוריה.

    **‏Dijkstra מחזיר את המינימום.** כל המחירים חיוביים, ולכן המצבים יוצאים לפי סדר עולה
    של המרחק הקצר ביותר אליהם, והמצב הסופי יוצא עם המרחק הקצר ביותר האפשרי.

    **הכלל החמדני.** לפתרון יש גם צורה סגורה : ממיינים, ולשני האיטיים \( t_{n-1} \le t_n \)
    משווים שתי דרכים להעביר אותם ולהחזיר את הלפיד למהירים :

    \[
    \min\big(t_1 + 2t_2 + t_n,\; 2t_1 + t_{n-1} + t_n\big)
    \]

    הראשונה היא "שני האיטיים יחד" (הזוג המהיר חוצה, הכי מהיר חוזר, האיטיים חוצים, השני
    חוזר), והשנייה היא "המהיר מלווה כל אחד". מורידים את שני האיטיים וממשיכים, עד שנשארים
    שלושה (‏\( t_1 + t_2 + t_3 \)) או שניים (‏\( t_2 \)). עבור 1, 2, 5, 10 : ‏\( \min(1 + 4 + 10,\; 2 + 5 + 10) = 15 \),
    ועוד 2 לזוג האחרון : 17. החיפוש והכלל מסכימים על כל הדוגמאות, והבדיקות של השאלה
    משוות אותם על אלפי קבוצות אקראיות :

    <!-- gen 5 -->

    | הזמנים | המהיר מלווה | החיפוש (Dijkstra) | הכלל החמדני |
    |---|:-:|:-:|:-:|
    | ‏1, 2, 5, 10 | ‏19 | ‏17 | ‏17 |
    | ‏1, 2, 3, 4 | ‏11 | ‏11 | ‏11 |
    | ‏1, 3, 4, 6 | ‏15 | ‏15 | ‏15 |
    | ‏1, 1, 1, 1 | ‏5 | ‏5 | ‏5 |
    | ‏2, 2, 2, 2, 2 | ‏14 | ‏14 | ‏14 |
    | ‏1, 2, 5, 10, 20 | ‏40 | ‏33 | ‏33 |
    | ‏1, 4, 5, 6, 7, 8 | ‏34 | ‏34 | ‏34 |

    <!-- /gen -->

    **נסו בעצמכם.** הקלידו זמנים (עד שמונה אנשים), והקוד מוצא את התוכנית ומריץ אותה חצייה
    אחרי חצייה. הטבלה משווה לשתי התוכניות הקלאסיות, ואפשר להריץ גם אותן; גשר שמחזיק שלושה
    הוא שאלת ההמשך. המתג "הכלל החמדני" מראה את הכלל סיבוב אחרי סיבוב : בכל סיבוב שתי
    הדרכים להעביר את שני האיטיים, הזולה מביניהן מודגשת, והסכום מגיע לזמן של החיפוש :

    <div class="explorer" data-kind="bridge" data-times="1 2 5 10"></div>

    #### סיבוכיות { .sol-cost }

    - **מצבים :** ‏\( S = 2^N \cdot 2 \). עם שמונה אנשים, 512.
    - **קשתות :** מכל מצב \( O(N^2) \) קבוצות. ‏Python עם ערימה : ‏\( O(S N^2 \log S) \);
      ‏SystemVerilog עם סריקה : ‏\( O(S^2 + S N^2) \). עם \( N \le 8 \) שניהם מיידיים.
    - **זיכרון :** ‏\( O(S) \) למרחקים ולהורים.

## נקודות חשובות ושאלות המשך

??? trap "מלכודת : המהיר מלווה את כולם"
    התוכנית הראשונה שעולה נותנת 19, ונראית אופטימלית כי "המהיר תמיד מחזיר את הלפיד". היא
    משלמת גם 10 וגם 5. הרעיון החסר : שני האיטיים חוצים יחד, והמהירים עושים את העבודה
    של הלפיד.

??? trap "מלכודת : לשכוח את הלפיד"
    ‏"C ו-D חוצים ראשונים, 10 דקות, ואז A ו-B, 2 דקות : 12". מי החזיר את הלפיד? בלי לפיד
    אין חצייה. כל חצייה קדימה חוץ מהאחרונה מחייבת חצייה חזרה.

??? trap "מלכודת : BFS במקום Dijkstra"
    ‏BFS מוצא את התוכנית עם **הכי מעט חציות**. לארבעה אנשים כל התוכניות הן חמש חציות,
    ולכן BFS יחזיר סתם את הראשונה שמצא, אולי 19. כשהקשתות שוקלות שונה צריך Dijkstra.

??? trap "מלכודת : הזמן בתוך המצב"
    מי שמכניס את הזמן שעבר למצב מקבל גרף שבו כל מצב "חדש", הגיזום לא עובד, והחיפוש
    מתפוצץ. הזמן הוא המחיר של המסלול, לא חלק מהמצב (כמו בשאלה 0019).

??? followup "שאלות המשך"
    - **חמישה אנשים :** ‏1, 2, 5, 10, 20. ‏(33 : ‏A+B, ‏A, ‏D+E, ‏B, ‏A+B, ‏A, ‏A+C : ‏2 + 1 + 20 + 2 + 2 + 1 + 5.
      הכלל נותן \( \min(1 + 4 + 20, 2 + 10 + 20) = 25 \) ועוד \( 1 + 2 + 5 = 8 \).)
    - **כולם שווים :** ‏\( N \) אנשים, כל אחד \( t \) דקות. ‏(‏\( (2N - 3)\,t \) : ‏\( N - 1 \) חציות
      קדימה ו-\( N - 2 \) חזרה.)
    - **הגשר מחזיק שלושה :** עם 1, 2, 5, 10. ‏(13 : ‏A+C+D חוצים, 10; ‏A חוזר, 1; ‏A+B חוצים, 2.)
    - **מתי "המהיר מלווה" כן אופטימלי :** מצאו תנאי על הזמנים שבו \( 2t_1 + t_{n-1} + t_n \le t_1 + 2t_2 + t_n \).
      ‏(‏\( t_{n-1} + t_1 \le 2t_2 \) : כשהשני-הכי-איטי לא רחוק מהשני-הכי-מהיר, למשל 1, 2, 3, 4.)
