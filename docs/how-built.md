---
description: איך דף שאלה נעשה לאתר, ואיך כל דחיפה עוברת את הבדיקות בדרך לפרסום
hide:
  - navigation
---

# איך האתר נבנה

כל דף באתר הוא קובץ Markdown אחד במאגר, וכל מה שרואים בו נבנה ממנו אוטומטית : השרטוטים,
הקוד שאפשר להריץ והתיבות האינטראקטיביות. לפני שדף מתפרסם הוא עובר שתי דרכים, ושני
התרשימים כאן מראים אותן. אפשר לכבות את ההנפשה בכפתור שמעל כל תרשים.

## מדחיפה לאתר

כל דחיפה למאגר מריצה את `.github/workflows/deploy.yml`. השלב הראשון, gate, בודק מה השתנה
ובוחר מסלול, וכל מסלול מריץ רק את הבדיקות שהשינוי צריך. בחרו סוג דחיפה כדי לראות את המסלול שלה.

<!-- gen 0 -->

<div class="sf-box" data-sf="ci">
<div class="sf-controls"><fieldset class="sf-lanes"><legend>איזו דחיפה :</legend><label><input type="radio" name="sf-ci-lane" value="full" checked><span>שינוי בקוד</span></label><label><input type="radio" name="sf-ci-lane" value="fast"><span>רק טקסט</span></label><label><input type="radio" name="sf-ci-lane" value="done"><span>כבר עבר בענף</span></label></fieldset><label class="sf-play"><input type="checkbox" checked><span>הנפשה</span></label></div>
<div class="sf-scroll">
<svg class="figure sf-fig sf-ci" viewBox="0 0 360 420" style="max-width:22.5rem" role="img" aria-labelledby="sf-ci-title sf-ci-desc">
<title id="sf-ci-title">ריצת ה-CI של דחיפה</title>
<desc id="sf-ci-desc">דחיפה עוברת ב-gate, שבוחר אחד משלושה מסלולים: שינוי קוד מריץ את test ואחריו build ו-explorers במקביל, שינוי טקסט בלבד מריץ את quick ואחריו build, וקומיט שכבר עבר בענף הולך ישר ל-build. deploy מפרסם את האתר, רק ב-main.</desc>
<g class="sf-L-all"><path class="sf-edge" d="M180,52 L180,92"/><path class="sf-head" d="M180,92 L176,84 L184,84 Z"/></g>
<g class="sf-L-full"><path class="sf-edge" d="M216,136 L216,144 Q216,152 224,152 L290,152 Q298,152 298,160 L298,184"/><path class="sf-head" d="M298,184 L294,176 L302,176 Z"/></g>
<g class="sf-L-fast"><path class="sf-edge" d="M180,136 L180,184"/><path class="sf-head" d="M180,184 L176,176 L184,176 Z"/></g>
<g class="sf-L-done"><path class="sf-edge" d="M144,136 L144,144 Q144,152 136,152 L48,152 Q40,152 40,160 L40,276"/><path class="sf-head" d="M40,276 L36,268 L44,268 Z"/></g>
<g class="sf-L-fast"><path class="sf-edge" d="M180,228 L180,276"/><path class="sf-head" d="M180,276 L176,268 L184,268 Z"/></g>
<g class="sf-L-full"><path class="sf-edge" d="M280,228 L280,240 Q280,248 272,248 L220,248 Q212,248 212,256 L212,276"/><path class="sf-head" d="M212,276 L208,268 L216,268 Z"/></g>
<g class="sf-L-full"><path class="sf-edge" d="M316,228 L316,276"/><path class="sf-head" d="M316,276 L312,268 L320,268 Z"/></g>
<g class="sf-L-all"><path class="sf-edge" d="M150,320 L150,368"/><path class="sf-head" d="M150,368 L146,360 L154,360 Z"/></g>
<g class="sf-L-full"><path class="sf-edge" d="M298,320 L298,382 Q298,390 290,390 L260,390"/><path class="sf-head" d="M260,390 L268,386 L268,394 Z"/></g>
<g class="sf-lab sf-L-done"><rect x="48" y="203" width="76" height="18" rx="3"/><text x="86" y="216" text-anchor="middle" direction="rtl">כבר עבר בענף</text></g>
<g class="sf-node sf-L-all"><rect x="130" y="8" width="100" height="44" rx="6"/><text class="sf-name" x="180" y="27" text-anchor="middle">push</text><text class="sf-sub" x="180" y="43" text-anchor="middle" direction="rtl">קומיט לענף</text></g>
<g class="sf-node sf-L-all"><rect x="100" y="92" width="160" height="44" rx="6"/><text class="sf-name" x="180" y="111" text-anchor="middle">gate</text><text class="sf-sub" x="180" y="127" text-anchor="middle" direction="rtl">מה השתנה?</text></g>
<g class="sf-node sf-L-full"><rect x="244" y="184" width="108" height="44" rx="6"/><text class="sf-name" x="298" y="203" text-anchor="middle">test</text><text class="sf-sub" x="298" y="219" text-anchor="middle" direction="rtl">כל הבדיקות</text></g>
<g class="sf-node sf-L-fast"><rect x="126" y="184" width="108" height="44" rx="6"/><text class="sf-name" x="180" y="203" text-anchor="middle">quick</text><text class="sf-sub" x="180" y="219" text-anchor="middle" direction="rtl">רק מה שנגע</text></g>
<g class="sf-node sf-L-all"><rect x="8" y="276" width="228" height="44" rx="6"/><text class="sf-name" x="122" y="295" text-anchor="middle">build</text><text class="sf-sub" x="122" y="311" text-anchor="middle" direction="rtl">בנייה, קישורים, טלפון</text></g>
<g class="sf-node sf-L-full"><rect x="244" y="276" width="108" height="44" rx="6"/><text class="sf-name" x="298" y="295" text-anchor="middle">explorers</text><text class="sf-sub" x="298" y="311" text-anchor="middle" direction="rtl">לוחצים על התיבות</text></g>
<g class="sf-node sf-L-all"><rect x="100" y="368" width="160" height="44" rx="6"/><text class="sf-name" x="180" y="387" text-anchor="middle">deploy</text><text class="sf-sub" x="180" y="403" text-anchor="middle" direction="rtl">רק ב-main</text></g>
<g class="sf-anim" aria-hidden="true"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.8667;0.9500;1"/>
<path class="sf-run sf-L-all" d="M180,52 L180,92" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.0833;0.1667;1"/></path>
<path class="sf-run sf-L-full" d="M216,136 L216,144 Q216,152 224,152 L290,152 Q298,152 298,160 L298,184" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.2500;0.3333;1"/></path>
<path class="sf-run sf-L-fast" d="M180,136 L180,184" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.2500;0.3333;1"/></path>
<path class="sf-run sf-L-done" d="M144,136 L144,144 Q144,152 136,152 L48,152 Q40,152 40,160 L40,276" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.2500;0.5000;1"/></path>
<path class="sf-run sf-L-fast" d="M180,228 L180,276" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.4167;0.5000;1"/></path>
<path class="sf-run sf-L-full" d="M280,228 L280,240 Q280,248 272,248 L220,248 Q212,248 212,256 L212,276" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.4167;0.5000;1"/></path>
<path class="sf-run sf-L-full" d="M316,228 L316,276" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.4167;0.5000;1"/></path>
<path class="sf-run sf-L-all" d="M150,320 L150,368" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.5833;0.6667;1"/></path>
<path class="sf-run sf-L-full" d="M298,320 L298,382 Q298,390 290,390 L260,390" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.5833;0.6667;1"/></path>
<rect class="sf-lit sf-L-all" x="130" y="8" width="100" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.0000;0.0333;1"/></rect>
<rect class="sf-lit sf-L-all" x="100" y="92" width="160" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.1667;0.2000;1"/></rect>
<rect class="sf-lit sf-L-full" x="244" y="184" width="108" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.3333;0.3667;1"/></rect>
<rect class="sf-lit sf-L-fast" x="126" y="184" width="108" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.3333;0.3667;1"/></rect>
<rect class="sf-lit sf-L-all" x="8" y="276" width="228" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.5000;0.5333;1"/></rect>
<rect class="sf-lit sf-L-full" x="244" y="276" width="108" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.5000;0.5333;1"/></rect>
<rect class="sf-lit sf-L-all" x="100" y="368" width="160" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.6667;0.7000;1"/></rect>
</g></svg>
</div>
</div>

<!-- /gen -->

- **שינוי בקוד** : שינוי בקוד של דף, בשרטוט, בתיבה או בעיצוב. test מריץ את הבדיקות של כל
  השאלות, ב-Python וב-SystemVerilog עם Verilator, ואחריו רצים במקביל build, שבונה את האתר
  ובודק כל דף ברוחב של טלפון, ו-explorers, ארבע מכונות שלוחצות על כל כפתור בכל תיבה.
- **רק טקסט** : שינוי בטקסט של דפי שאלות בלבד, בלי קוד, שרטוטים או תיבות
  (`tools/checks/text_only.py` מזהה אותו). quick מריץ את הבדיקות של השאלות שנגעו, ו-build
  בודק בטלפון רק את הדפים האלה. האתר מתעדכן אחרי כמה דקות.
- **כבר עבר בענף** : קומיט שהגיע ל-main אחרי שעבר את כל הבדיקות בענף העבודה. gate מוצא
  את הריצה הירוקה שלו, ו-build רק בונה את האתר בלי לחזור על הבדיקות.

בכל המסלולים deploy מפרסם את האתר רק מ-main, ורק אם כל מה שלפניו עבר. בענף עבודה הריצה
נעצרת אחרי הבדיקות, וכשל באחת מהן עוצר את הפרסום.

## מדף שאלה לאתר

<!-- gen 1 -->

<div class="sf-box" data-sf="page">
<div class="sf-controls"><label class="sf-play"><input type="checkbox" checked><span>הנפשה</span></label></div>
<div class="sf-scroll">
<svg class="figure sf-fig sf-page" viewBox="0 0 360 416" style="max-width:22.5rem" role="img" aria-labelledby="sf-page-title sf-page-desc">
<title id="sf-page-title">איך דף שאלה נעשה לאתר</title>
<desc id="sf-page-desc">מחולל השרטוטים כותב את השרטוטים לתוך דף השאלה עם fill.py. הבדיקות מריצות את קוד הדף, MkDocs וה-hook בונים ממנו את האתר יחד עם קוד התיבות, ובדיקות האתר עוברות על הדפים הבנויים.</desc>
<g class="sf-L-all"><path class="sf-edge" d="M132,52 L132,96"/><path class="sf-head" d="M132,96 L128,88 L136,88 Z"/></g>
<g class="sf-L-all"><path class="sf-edge" d="M216,118 L240,118"/><path class="sf-head" d="M240,118 L232,122 L232,114 Z"/></g>
<g class="sf-L-all"><path class="sf-edge" d="M132,140 L132,184"/><path class="sf-head" d="M132,184 L128,176 L136,176 Z"/></g>
<g class="sf-L-all"><path class="sf-edge" d="M132,228 L132,272"/><path class="sf-head" d="M132,272 L128,264 L136,264 Z"/></g>
<g class="sf-L-all"><path class="sf-edge" d="M296,228 L296,286 Q296,294 288,294 L216,294"/><path class="sf-head" d="M216,294 L224,290 L224,298 Z"/></g>
<g class="sf-L-all"><path class="sf-edge" d="M132,316 L132,360"/><path class="sf-head" d="M132,360 L128,352 L136,352 Z"/></g>
<g class="sf-lab sf-L-all"><rect x="142" y="65" width="52" height="18" rx="3"/><text x="168" y="78" text-anchor="middle" direction="rtl">fill.py</text></g>
<g class="sf-node sf-L-all"><rect x="48" y="8" width="168" height="44" rx="6"/><text class="sf-name" x="132" y="27" text-anchor="middle">q‹id›.py</text><text class="sf-sub" x="132" y="43" text-anchor="middle" direction="rtl">מחולל השרטוטים</text></g>
<g class="sf-node sf-L-all"><rect x="48" y="96" width="168" height="44" rx="6"/><text class="sf-name" x="132" y="115" text-anchor="middle">‹id›-‹slug›.md</text><text class="sf-sub" x="132" y="131" text-anchor="middle" direction="rtl">דף השאלה, טקסט וקוד</text></g>
<g class="sf-node sf-L-all"><rect x="240" y="96" width="112" height="44" rx="6"/><text class="sf-name" x="296" y="115" text-anchor="middle">tests</text><text class="sf-sub" x="296" y="131" text-anchor="middle" direction="rtl">מריצים את קוד הדף</text></g>
<g class="sf-node sf-L-all"><rect x="48" y="184" width="168" height="44" rx="6"/><text class="sf-name" x="132" y="203" text-anchor="middle">hooks/questions.py</text><text class="sf-sub" x="132" y="219" text-anchor="middle" direction="rtl">MkDocs וה-hook</text></g>
<g class="sf-node sf-L-all"><rect x="240" y="184" width="112" height="44" rx="6"/><text class="sf-name" x="296" y="203" text-anchor="middle">explorer/*.js</text><text class="sf-sub" x="296" y="219" text-anchor="middle" direction="rtl">קוד התיבות</text></g>
<g class="sf-node sf-L-all"><rect x="48" y="272" width="168" height="44" rx="6"/><text class="sf-name" x="132" y="291" text-anchor="middle">site/</text><text class="sf-sub" x="132" y="307" text-anchor="middle" direction="rtl">HTML, site.css ו-JS</text></g>
<g class="sf-node sf-L-all"><rect x="48" y="360" width="168" height="44" rx="6"/><text class="sf-name" x="132" y="379" text-anchor="middle">check_*.py</text><text class="sf-sub" x="132" y="395" text-anchor="middle" direction="rtl">טלפון, קישורים, תיבות</text></g>
<g class="sf-anim" aria-hidden="true"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.8667;0.9500;1"/>
<path class="sf-run sf-L-all" d="M132,52 L132,96" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.0833;0.1667;1"/></path>
<path class="sf-run sf-L-all" d="M216,118 L240,118" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.2500;0.3333;1"/></path>
<path class="sf-run sf-L-all" d="M132,140 L132,184" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.2500;0.3333;1"/></path>
<path class="sf-run sf-L-all" d="M132,228 L132,272" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.4167;0.5000;1"/></path>
<path class="sf-run sf-L-all" d="M296,228 L296,286 Q296,294 288,294 L216,294" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.4167;0.5000;1"/></path>
<path class="sf-run sf-L-all" d="M132,316 L132,360" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" dur="6s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.5833;0.6667;1"/></path>
<rect class="sf-lit sf-L-all" x="48" y="8" width="168" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.0000;0.0333;1"/></rect>
<rect class="sf-lit sf-L-all" x="48" y="96" width="168" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.1667;0.2000;1"/></rect>
<rect class="sf-lit sf-L-all" x="240" y="96" width="112" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.3333;0.3667;1"/></rect>
<rect class="sf-lit sf-L-all" x="48" y="184" width="168" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.3333;0.3667;1"/></rect>
<rect class="sf-lit sf-L-all" x="240" y="184" width="112" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.3333;0.3667;1"/></rect>
<rect class="sf-lit sf-L-all" x="48" y="272" width="168" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.5000;0.5333;1"/></rect>
<rect class="sf-lit sf-L-all" x="48" y="360" width="168" height="44" rx="6" opacity="0"><animate attributeName="opacity" dur="6s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;0.6667;0.7000;1"/></rect>
</g></svg>
</div>
</div>

<!-- /gen -->

דף שאלה הוא המקור היחיד של כל מה שיש בו :

- **השרטוטים** נוצרים בקוד Python, במחולל `tools/figures/q<id>.py`, ו-`fill.py` כותב אותם
  לתוך הדף בין שתי הערות. בדיקה של השאלה נכשלת אם העותק בדף לא תואם למחולל.
- **הקוד** של הפתרון כתוב בדף עצמו, ב-Python וב-SystemVerilog. הבדיקות מוציאות אותו מהדף
  ומריצות אותו כמו שהוא, כך שקוד שמופיע באתר תמיד נבדק.
- **הבנייה** : MkDocs בונה את הדפים, וה-hook `hooks/questions.py` מוסיף את מה שמשותף לכולם :
  כרטיס השאלה, הטבלאות והתגיות, אינדקס החיפוש, וקובץ העיצוב האחד `site.css`.
- **התיבות האינטראקטיביות** כתובות ב-JavaScript, קובץ לכל סוג תיבה ב-`explorer/`, ונבדקות
  מול הקוד של Python באותה שאלה.
- **בדיקות האתר** פותחות את הדפים הבנויים בדפדפן : ברוחב של טלפון, במצב כהה, עם המקלדת בלבד,
  ובכל תיבה הן לוחצות על הכפתורים ובודקות שהשרטוטים לא קופצים.
