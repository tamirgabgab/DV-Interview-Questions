---
id: 9
title: 16 אנשים, 16 קופסאות ועוזר אחד
level: junior
difficulty: medium
tags: [logic-puzzles, combinatorics, algorithms, python, systemverilog]
source: ""
added: 2026-10-16
---

## השאלה

יש 16 אנשים, ממוספרים מ-1 עד 16, ואיתם אדם נוסף מיוחד: **אדם מספר 0**.

בחדר יש 16 קופסאות ממוספרות מ-1 עד 16. בכל קופסה יש פתק אחד, ועליו מספר בין 1 ל-16. כל
מספר מופיע בדיוק פעם אחת, והפתקים עורבבו באקראי. למשל, בקופסה 1 יש אולי פתק 3, ובקופסה 2
יש פתק 15.

- **אדם 0** נכנס ראשון. הוא מציץ **בכל** הקופסאות, ויכול לבצע **עד 4 החלפות** של פתקים
  בין שתי קופסאות. אחר כך הוא יוצא לחדר המנצחים.
- **אנשים 1 עד 16** נכנסים אחר כך, אחד אחד. כל אחד מציץ בעד **8 קופסאות** לפי בחירתו. אם
  הוא מוצא את הפתק עם המספר שלו, הוא עובר לחדר המנצחים. החדר חוזר למצבו בין אדם לאדם:
  אסור להזיז פתקים.
- **מטרה:** כל 16 האנשים צריכים להגיע לחדר המנצחים. מספיק שאחד ייכשל וכולם מפסידים.

לפני שהמשחק מתחיל כולם, כולל אדם 0, יכולים לתכנן אסטרטגיה משותפת. מהרגע שהראשון נכנס
לחדר אין יותר תקשורת: מי שיצא לא יכול לחזור, ואי אפשר להעביר מידע למי שבחוץ.

---

### סעיף א – האסטרטגיה

מהי אסטרטגיה שמבטיחה שכולם ינצחו, **בכל** סידור של הפתקים?

??? tip "רמז 1"
    נסו לחשוב על הקופסאות כעל גרף: חץ מכל קופסה אל הקופסה שהמספר שלה כתוב על הפתק. איך
    נראה גרף כזה?

??? tip "רמז 2"
    זו גרסה של חידת "100 האסירים". בלי אדם 0, האסטרטגיה הידועה מצליחה רק בכשליש מהמקרים.
    מתי היא נכשלת, וכמה החלפות צריך כדי למנוע את זה?

??? success "פתרון סעיף א"
    #### שלב 1 – לכל אחד: ללכת לפי הפתקים

    כל אדם \( i \) פותח קודם את **הקופסה שלו**, קופסה \( i \). אם הפתק לא שלו, הוא
    פותח את הקופסה **שהמספר שלה כתוב על הפתק**, וכן הלאה.

    כל קופסה מצביעה על הקופסה הבאה, כמו **רשימה מקושרת**. מכיוון שכל מספר מופיע על פתק
    אחד בדיוק, לכל קופסה נכנס חץ אחד ויוצא חץ אחד. לכן הגרף מתפרק **למעגלים** זרים, וזו
    בדיוק פירוק התמורה למעגלים.

    **למה זה עובד?** אדם \( i \) מתחיל בקופסה \( i \), ולכן הוא הולך על המעגל שקופסה
    \( i \) נמצאת בו. הפתק \( i \) נמצא בקופסה שמצביעה **חזרה** אל קופסה \( i \), כלומר
    בקופסה האחרונה של אותו מעגל. מי שנמצא במעגל באורך \( L \) מוצא את הפתק שלו בדיוק
    בפתיחה ה-\( L \)-ית.

    לכן: **כל מי שנמצא במעגל באורך 8 לכל היותר מצליח**, ומי שנמצא במעגל ארוך יותר נכשל.

    #### שלב 2 – אדם 0 מציל את המצב

    - **יש לכל היותר מעגל ארוך אחד.** סכום אורכי המעגלים הוא 16. שני מעגלים באורך 9
      לפחות כבר דורשים 18 קופסאות.
    - **החלפה אחת חוצה מעגל לשניים.** אם המעגל הוא
      \( c_0 \to c_1 \to \dots \to c_{L-1} \to c_0 \), ומחליפים בין הפתקים של קופסה
      \( c_0 \) וקופסה \( c_h \), מתקבלים שני מעגלים:
      \( c_0 \to c_{h+1} \to \dots \to c_{L-1} \to c_0 \) באורך \( L - h \), ו-
      \( c_1 \to c_2 \to \dots \to c_h \to c_1 \) באורך \( h \).
    - **בוחרים את האמצע:** \( h = \lfloor L/2 \rfloor \). מכיוון ש-\( L \le 16 \), שני
      החלקים הם באורך 8 לכל היותר.

    **האסטרטגיה המלאה:** אדם 0 מוצא את המעגלים. אם יש מעגל ארוך מ-8, הוא מחליף בין הפתק
    בתחילת המעגל לפתק שבאמצע שלו. אחר כך כל אחד הולך לפי הפתקים. **החלפה אחת מספיקה**,
    ושלוש ההחלפות הנוספות מיותרות.

    #### דוגמה: לפני ההחלפה

    בכל משבצת, המספר הקטן הוא מספר הקופסה, והמספר הגדול הוא הפתק שבתוכה:

    <div class="box-grid" dir="ltr"><span class="hl"><small>1</small><b>7</b></span><span><small>2</small><b>11</b></span><span><small>3</small><b>15</b></span><span><small>4</small><b>16</b></span><span><small>5</small><b>13</b></span><span><small>6</small><b>2</b></span><span><small>7</small><b>12</b></span><span><small>8</small><b>14</b></span><span class="hl"><small>9</small><b>4</b></span><span><small>10</small><b>5</b></span><span><small>11</small><b>6</b></span><span><small>12</small><b>3</b></span><span><small>13</small><b>1</b></span><span><small>14</small><b>8</b></span><span><small>15</small><b>9</b></span><span><small>16</small><b>10</b></span></div>

    בעקבות החצים מקבלים שלושה מעגלים: אחד באורך **11**, אחד באורך 3 ואחד באורך 2. כל 11
    האנשים שבמעגל הארוך היו נכשלים. אדם 0 מחליף בין הפתקים של **קופסה 1** ו**קופסה 9**,
    שהן \( c_0 \) ו-\( c_5 \) במעגל הארוך.

    <span class="viz-legend"><span><i class="s2"></i>המעגל הארוך (11)</span><span><i class="ink"></i>מעגלים קצרים</span></span>

    <svg class="figure" viewBox="0 0 640 300" role="img" aria-label="המעגלים לפני ההחלפה: מעגל באורך 11, מעגל באורך 3 ומעגל באורך 2"><defs><marker id="q9b-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q9b-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q9b-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q9b-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><path class="s2-line" d="M193.9,31.5 A120,120 0 0 1 223.1,40.1" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 1 holds note 7</title></path><path class="s2-line" d="M255.0,60.5 A120,120 0 0 1 274.9,83.6" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 7 holds note 12</title></path><path class="s2-line" d="M290.7,118.0 A120,120 0 0 1 295.0,148.1" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 12 holds note 3</title></path><path class="s2-line" d="M289.6,185.6 A120,120 0 0 1 276.9,213.3" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 3 holds note 15</title></path><path class="s2-line" d="M252.2,241.9 A120,120 0 0 1 226.5,258.4" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 15 holds note 9</title></path><path class="s2-line" d="M190.2,269.0 A120,120 0 0 1 159.8,269.0" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 9 holds note 4</title></path><path class="s2-line" d="M123.5,258.4 A120,120 0 0 1 97.8,241.9" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 4 holds note 16</title></path><path class="s2-line" d="M73.1,213.3 A120,120 0 0 1 60.4,185.6" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 16 holds note 10</title></path><path class="s2-line" d="M55.0,148.1 A120,120 0 0 1 59.3,118.0" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 10 holds note 5</title></path><path class="s2-line" d="M75.1,83.6 A120,120 0 0 1 95.0,60.5" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 5 holds note 13</title></path><path class="s2-line" d="M126.9,40.1 A120,120 0 0 1 156.1,31.5" fill="none" stroke-width="2.5" marker-end="url(#q9b-s2)"><title>box 13 holds note 1</title></path><text class="legend" x="175" y="154" text-anchor="middle">L = 11</text><path class="ink-line" d="M448.7,93.0 A60,60 0 0 1 488.7,162.3" fill="none" stroke-width="2.5" marker-end="url(#q9b-ink)"><title>box 2 holds note 11</title></path><path class="ink-line" d="M470.0,194.7 A60,60 0 0 1 390.0,194.7" fill="none" stroke-width="2.5" marker-end="url(#q9b-ink)"><title>box 11 holds note 6</title></path><path class="ink-line" d="M371.3,162.3 A60,60 0 0 1 411.3,93.0" fill="none" stroke-width="2.5" marker-end="url(#q9b-ink)"><title>box 6 holds note 2</title></path><text class="legend" x="430" y="154" text-anchor="middle">L = 3</text><path class="ink-line" d="M583.4,109.0 A45,45 0 0 1 583.4,191.0" fill="none" stroke-width="2.5" marker-end="url(#q9b-ink)"><title>box 8 holds note 14</title></path><path class="ink-line" d="M546.6,191.0 A45,45 0 0 1 546.6,109.0" fill="none" stroke-width="2.5" marker-end="url(#q9b-ink)"><title>box 14 holds note 8</title></path><text class="legend" x="565" y="154" text-anchor="middle">L = 2</text><circle class="box-node box-hl" cx="175.0" cy="30.0" r="15"><title>box 1</title></circle><text class="box-num" x="175.0" y="35.0" text-anchor="middle">1</text><circle class="box-node" cx="239.9" cy="49.0" r="15"><title>box 7</title></circle><text class="box-num" x="239.9" y="54.0" text-anchor="middle">7</text><circle class="box-node" cx="284.2" cy="100.2" r="15"><title>box 12</title></circle><text class="box-num" x="284.2" y="105.2" text-anchor="middle">12</text><circle class="box-node" cx="293.8" cy="167.1" r="15"><title>box 3</title></circle><text class="box-num" x="293.8" y="172.1" text-anchor="middle">3</text><circle class="box-node" cx="265.7" cy="228.6" r="15"><title>box 15</title></circle><text class="box-num" x="265.7" y="233.6" text-anchor="middle">15</text><circle class="box-node box-hl" cx="208.8" cy="265.1" r="15"><title>box 9</title></circle><text class="box-num" x="208.8" y="270.1" text-anchor="middle">9</text><circle class="box-node" cx="141.2" cy="265.1" r="15"><title>box 4</title></circle><text class="box-num" x="141.2" y="270.1" text-anchor="middle">4</text><circle class="box-node" cx="84.3" cy="228.6" r="15"><title>box 16</title></circle><text class="box-num" x="84.3" y="233.6" text-anchor="middle">16</text><circle class="box-node" cx="56.2" cy="167.1" r="15"><title>box 10</title></circle><text class="box-num" x="56.2" y="172.1" text-anchor="middle">10</text><circle class="box-node" cx="65.8" cy="100.2" r="15"><title>box 5</title></circle><text class="box-num" x="65.8" y="105.2" text-anchor="middle">5</text><circle class="box-node" cx="110.1" cy="49.0" r="15"><title>box 13</title></circle><text class="box-num" x="110.1" y="54.0" text-anchor="middle">13</text><circle class="box-node" cx="430.0" cy="90.0" r="15"><title>box 2</title></circle><text class="box-num" x="430.0" y="95.0" text-anchor="middle">2</text><circle class="box-node" cx="482.0" cy="180.0" r="15"><title>box 11</title></circle><text class="box-num" x="482.0" y="185.0" text-anchor="middle">11</text><circle class="box-node" cx="378.0" cy="180.0" r="15"><title>box 6</title></circle><text class="box-num" x="378.0" y="185.0" text-anchor="middle">6</text><circle class="box-node" cx="565.0" cy="105.0" r="15"><title>box 8</title></circle><text class="box-num" x="565.0" y="110.0" text-anchor="middle">8</text><circle class="box-node" cx="565.0" cy="195.0" r="15"><title>box 14</title></circle><text class="box-num" x="565.0" y="200.0" text-anchor="middle">14</text></svg>

    #### דוגמה: אחרי ההחלפה

    <div class="box-grid" dir="ltr"><span class="hl"><small>1</small><b>4</b></span><span><small>2</small><b>11</b></span><span><small>3</small><b>15</b></span><span><small>4</small><b>16</b></span><span><small>5</small><b>13</b></span><span><small>6</small><b>2</b></span><span><small>7</small><b>12</b></span><span><small>8</small><b>14</b></span><span class="hl"><small>9</small><b>7</b></span><span><small>10</small><b>5</b></span><span><small>11</small><b>6</b></span><span><small>12</small><b>3</b></span><span><small>13</small><b>1</b></span><span><small>14</small><b>8</b></span><span><small>15</small><b>9</b></span><span><small>16</small><b>10</b></span></div>

    הפתק 7 עבר מקופסה 1 לקופסה 9, והפתק 4 עבר מקופסה 9 לקופסה 1. שני חצים בלבד השתנו
    (בקו מקווקו), והמעגל באורך 11 התפצל למעגל באורך 6 ולמעגל באורך 5:

    <span class="viz-legend"><span><i class="s1"></i>החצי הראשון (6)</span><span><i class="s3"></i>החצי השני (5)</span><span><i class="ink"></i>מעגלים שלא השתנו</span></span>

    <svg class="figure" viewBox="0 0 640 300" role="img" aria-label="המעגלים אחרי ההחלפה: מעגלים באורך 6, 5, 3 ו-2"><defs><marker id="q9a-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q9a-s1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s1-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q9a-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker><marker id="q9a-s3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="s3-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs><path class="s1-line" d="M128.8,67.1 A85,85 0 0 1 172.4,92.2" fill="none" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#q9a-s1)"><title>box 1 holds note 4</title></path><path class="s1-line" d="M191.2,124.9 A85,85 0 0 1 191.2,175.1" fill="none" stroke-width="2.5" marker-end="url(#q9a-s1)"><title>box 4 holds note 16</title></path><path class="s1-line" d="M172.4,207.8 A85,85 0 0 1 128.8,232.9" fill="none" stroke-width="2.5" marker-end="url(#q9a-s1)"><title>box 16 holds note 10</title></path><path class="s1-line" d="M91.2,232.9 A85,85 0 0 1 47.6,207.8" fill="none" stroke-width="2.5" marker-end="url(#q9a-s1)"><title>box 10 holds note 5</title></path><path class="s1-line" d="M28.8,175.1 A85,85 0 0 1 28.8,124.9" fill="none" stroke-width="2.5" marker-end="url(#q9a-s1)"><title>box 5 holds note 13</title></path><path class="s1-line" d="M47.6,92.2 A85,85 0 0 1 91.2,67.1" fill="none" stroke-width="2.5" marker-end="url(#q9a-s1)"><title>box 13 holds note 1</title></path><text class="legend" x="110" y="154" text-anchor="middle">L = 6</text><path class="s3-line" d="M318.8,72.2 A80,80 0 0 1 368.1,108.1" fill="none" stroke-width="2.5" marker-end="url(#q9a-s3)"><title>box 3 holds note 15</title></path><path class="s3-line" d="M379.8,143.9 A80,80 0 0 1 360.9,201.8" fill="none" stroke-width="2.5" marker-end="url(#q9a-s3)"><title>box 15 holds note 9</title></path><path class="s3-line" d="M330.5,224.0 A80,80 0 0 1 269.5,224.0" fill="none" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#q9a-s3)"><title>box 9 holds note 7</title></path><path class="s3-line" d="M239.1,201.8 A80,80 0 0 1 220.2,143.9" fill="none" stroke-width="2.5" marker-end="url(#q9a-s3)"><title>box 7 holds note 12</title></path><path class="s3-line" d="M231.9,108.1 A80,80 0 0 1 281.2,72.2" fill="none" stroke-width="2.5" marker-end="url(#q9a-s3)"><title>box 12 holds note 3</title></path><text class="legend" x="300" y="154" text-anchor="middle">L = 5</text><path class="ink-line" d="M483.6,98.2 A55,55 0 0 1 519.1,159.7" fill="none" stroke-width="2.5" marker-end="url(#q9a-ink)"><title>box 2 holds note 11</title></path><path class="ink-line" d="M500.5,192.0 A55,55 0 0 1 429.5,192.0" fill="none" stroke-width="2.5" marker-end="url(#q9a-ink)"><title>box 11 holds note 6</title></path><path class="ink-line" d="M410.9,159.7 A55,55 0 0 1 446.4,98.2" fill="none" stroke-width="2.5" marker-end="url(#q9a-ink)"><title>box 6 holds note 2</title></path><text class="legend" x="465" y="154" text-anchor="middle">L = 3</text><path class="ink-line" d="M598.3,114.4 A40,40 0 0 1 598.3,185.6" fill="none" stroke-width="2.5" marker-end="url(#q9a-ink)"><title>box 8 holds note 14</title></path><path class="ink-line" d="M561.7,185.6 A40,40 0 0 1 561.7,114.4" fill="none" stroke-width="2.5" marker-end="url(#q9a-ink)"><title>box 14 holds note 8</title></path><text class="legend" x="580" y="154" text-anchor="middle">L = 2</text><circle class="box-node box-hl" cx="110.0" cy="65.0" r="15"><title>box 1</title></circle><text class="box-num" x="110.0" y="70.0" text-anchor="middle">1</text><circle class="box-node" cx="183.6" cy="107.5" r="15"><title>box 4</title></circle><text class="box-num" x="183.6" y="112.5" text-anchor="middle">4</text><circle class="box-node" cx="183.6" cy="192.5" r="15"><title>box 16</title></circle><text class="box-num" x="183.6" y="197.5" text-anchor="middle">16</text><circle class="box-node" cx="110.0" cy="235.0" r="15"><title>box 10</title></circle><text class="box-num" x="110.0" y="240.0" text-anchor="middle">10</text><circle class="box-node" cx="36.4" cy="192.5" r="15"><title>box 5</title></circle><text class="box-num" x="36.4" y="197.5" text-anchor="middle">5</text><circle class="box-node" cx="36.4" cy="107.5" r="15"><title>box 13</title></circle><text class="box-num" x="36.4" y="112.5" text-anchor="middle">13</text><circle class="box-node" cx="300.0" cy="70.0" r="15"><title>box 3</title></circle><text class="box-num" x="300.0" y="75.0" text-anchor="middle">3</text><circle class="box-node" cx="376.1" cy="125.3" r="15"><title>box 15</title></circle><text class="box-num" x="376.1" y="130.3" text-anchor="middle">15</text><circle class="box-node box-hl" cx="347.0" cy="214.7" r="15"><title>box 9</title></circle><text class="box-num" x="347.0" y="219.7" text-anchor="middle">9</text><circle class="box-node" cx="253.0" cy="214.7" r="15"><title>box 7</title></circle><text class="box-num" x="253.0" y="219.7" text-anchor="middle">7</text><circle class="box-node" cx="223.9" cy="125.3" r="15"><title>box 12</title></circle><text class="box-num" x="223.9" y="130.3" text-anchor="middle">12</text><circle class="box-node" cx="465.0" cy="95.0" r="15"><title>box 2</title></circle><text class="box-num" x="465.0" y="100.0" text-anchor="middle">2</text><circle class="box-node" cx="512.6" cy="177.5" r="15"><title>box 11</title></circle><text class="box-num" x="512.6" y="182.5" text-anchor="middle">11</text><circle class="box-node" cx="417.4" cy="177.5" r="15"><title>box 6</title></circle><text class="box-num" x="417.4" y="182.5" text-anchor="middle">6</text><circle class="box-node" cx="580.0" cy="110.0" r="15"><title>box 8</title></circle><text class="box-num" x="580.0" y="115.0" text-anchor="middle">8</text><circle class="box-node" cx="580.0" cy="190.0" r="15"><title>box 14</title></circle><text class="box-num" x="580.0" y="195.0" text-anchor="middle">14</text></svg>

    #### כולם מצליחים

    אחרי ההחלפה כל אחד מוצא את הפתק שלו ב-6 פתיחות לכל היותר:

    | אדם | הקופסאות שהוא פותח, לפי הסדר | פתיחות | הצליח? |
    |---|---|---|---|
    | 1 | <span dir="ltr">1 → 4 → 16 → 10 → 5 → 13</span> | 6 | ✓ |
    | 2 | <span dir="ltr">2 → 11 → 6</span> | 3 | ✓ |
    | 3 | <span dir="ltr">3 → 15 → 9 → 7 → 12</span> | 5 | ✓ |
    | 4 | <span dir="ltr">4 → 16 → 10 → 5 → 13 → 1</span> | 6 | ✓ |
    | 5 | <span dir="ltr">5 → 13 → 1 → 4 → 16 → 10</span> | 6 | ✓ |
    | 6 | <span dir="ltr">6 → 2 → 11</span> | 3 | ✓ |
    | 7 | <span dir="ltr">7 → 12 → 3 → 15 → 9</span> | 5 | ✓ |
    | 8 | <span dir="ltr">8 → 14</span> | 2 | ✓ |
    | 9 | <span dir="ltr">9 → 7 → 12 → 3 → 15</span> | 5 | ✓ |
    | 10 | <span dir="ltr">10 → 5 → 13 → 1 → 4 → 16</span> | 6 | ✓ |
    | 11 | <span dir="ltr">11 → 6 → 2</span> | 3 | ✓ |
    | 12 | <span dir="ltr">12 → 3 → 15 → 9 → 7</span> | 5 | ✓ |
    | 13 | <span dir="ltr">13 → 1 → 4 → 16 → 10 → 5</span> | 6 | ✓ |
    | 14 | <span dir="ltr">14 → 8</span> | 2 | ✓ |
    | 15 | <span dir="ltr">15 → 9 → 7 → 12 → 3</span> | 5 | ✓ |
    | 16 | <span dir="ltr">16 → 10 → 5 → 13 → 1 → 4</span> | 6 | ✓ |

    לשם השוואה, לפני ההחלפה אדם 13 היה פותח את הקופסאות
    <span dir="ltr">13 → 1 → 7 → 12 → 3 → 15 → 9 → 4</span>, ונעצר אחרי 8 פתיחות בלי
    למצוא את הפתק שלו. הפתק 13 היה בקופסה 5, הקופסה ה-11 במעגל.

---

### סעיף ב – כתבו את הקוד

הקופסאות הן מערך `notes`: `notes[b]` הוא המספר שכתוב על הפתק שבקופסה `b` (הקופסאות
ממוספרות מ-1 עד 16, ותא 0 לא בשימוש). לחדר יש API:

- **לאדם 0 בלבד, לפני שמישהו אחר נכנס:** `look_all()` מחזיר את כל המערך, ו-`swap(a, b)`
  מחליף בין הפתקים של שתי קופסאות, עד 4 פעמים.
- **לאנשים 1 עד 16:** `enter()` כשנכנסים, ואחר כך `open_box(b)` שמחזיר את הפתק שבקופסה
  `b`, עד 8 פעמים לכל אדם.

ממשו את החדר עם האכיפה של המגבלות, את האסטרטגיה של אדם 0, את האסטרטגיה של כל אחד מהאחרים,
ומשחק שלם שמחזיר האם כולם ניצחו.

??? tip "רמז"
    תתחילו מפונקציית עזר שמקבלת קופסת התחלה ומחזירה את רשימת הקופסאות במעגל שלה.

??? success "פתרון סעיף ב"
    #### החדר וה-API

    המערך עצמו פרטי. הדרך היחידה לראות אותו היא דרך ה-API, ושם נאכפות המגבלות: אחרי
    שהאדם הראשון נכנס, אדם 0 כבר לא יכול להציץ או להחליף, ואף אחד לא יכול לפתוח יותר
    מ-8 קופסאות.

    === "SystemVerilog"
        ```systemverilog
        localparam int N         = 16;      // people and boxes
        localparam int MAX_OPENS = N / 2;   // boxes each person may open
        localparam int MAX_SWAPS = 4;       // swaps person 0 may make

        typedef int notes_t[N + 1];         // notes[b] = the note in box b (1..N); [0] unused

        class room_c;
          local notes_t notes;              // hidden: only the API below can read it
          int swaps_left  = MAX_SWAPS;
          int opens_left  = 0;
          bit helper_done = 0;              // set when the first of persons 1..N walks in

          function new(notes_t initial_notes);
            notes = initial_notes;
          endfunction

          // ---- person 0 only ----
          function void look_all(output notes_t all_notes);
            assert (!helper_done) else $fatal(1, "only person 0 may look at all the boxes");
            all_notes = notes;
          endfunction

          function void swap(int a, int b);
            int tmp;
            assert (!helper_done && swaps_left > 0) else $fatal(1, "no swaps allowed");
            swaps_left--;
            tmp      = notes[a];
            notes[a] = notes[b];
            notes[b] = tmp;
          endfunction

          // ---- persons 1..N, one at a time ----
          function void enter();
            helper_done = 1;
            opens_left  = MAX_OPENS;
          endfunction

          function int open_box(int box);
            assert (opens_left > 0) else $fatal(1, "no opens left");
            opens_left--;
            return notes[box];
          endfunction
        endclass
        ```

    === "Python"
        ```python
        N = 16               # people and boxes
        MAX_OPENS = N // 2   # boxes each person may open
        MAX_SWAPS = 4        # swaps person 0 may make


        class Room:
            """notes[b] is the note in box b (1..N); notes[0] is unused."""

            def __init__(self, notes):
                self._notes = list(notes)    # hidden: only the API below can read it
                self.swaps_left = MAX_SWAPS
                self.opens_left = 0
                self.helper_done = False     # set when the first of persons 1..N walks in

            # ---- person 0 only ----
            def look_all(self):
                assert not self.helper_done, "only person 0 may look at all the boxes"
                return list(self._notes)

            def swap(self, a, b):
                assert not self.helper_done and self.swaps_left > 0, "no swaps allowed"
                self.swaps_left -= 1
                self._notes[a], self._notes[b] = self._notes[b], self._notes[a]

            # ---- persons 1..N, one at a time ----
            def enter(self):
                self.helper_done = True
                self.opens_left = MAX_OPENS

            def open_box(self, box):
                assert self.opens_left > 0, "no opens left"
                self.opens_left -= 1
                return self._notes[box]
        ```

    #### האסטרטגיה

    `cycle_from` הולכת לפי הפתקים מקופסה מסוימת עד שחוזרים אליה. אדם 0 משתמש בה כדי למצוא
    את המעגל הארוך, וכל אחד מהאחרים עושה את אותו הילוך בדיוק, אבל דרך `open_box` ועם
    מגבלה של 8 פתיחות.

    === "SystemVerilog"
        ```systemverilog
        typedef int box_list_t[$];

        // The boxes met when following the notes from box `start` until back at `start`
        function automatic box_list_t cycle_from(notes_t notes, int start);
          box_list_t cycle = '{start};
          int        box   = notes[start];
          while (box != start) begin
            cycle.push_back(box);
            box = notes[box];
          end
          return cycle;
        endfunction

        // Person 0: find the one cycle longer than MAX_OPENS (if any) and cut it in half
        function automatic void helper(room_c room);
          notes_t    notes;
          bit        seen[N + 1] = '{default: 0};
          box_list_t cycle;
          room.look_all(notes);
          for (int start = 1; start <= N; start++) begin
            if (seen[start]) continue;
            cycle = cycle_from(notes, start);
            foreach (cycle[i]) seen[cycle[i]] = 1;
            if (cycle.size() > MAX_OPENS) begin
              room.swap(cycle[0], cycle[cycle.size() / 2]);  // -> cycles of L/2 and L - L/2
              return;                                        // there is at most one long cycle
            end
          end
        endfunction

        // Person `me`: open my own box, then always the box whose number is on the note
        function automatic bit find_my_note(room_c room, int me);
          int box = me;
          int note;
          room.enter();
          repeat (MAX_OPENS) begin
            note = room.open_box(box);
            if (note == me) return 1;
            box = note;
          end
          return 0;
        endfunction

        // The whole game: person 0 first, then persons 1..N. True when everybody wins.
        function automatic bit play(notes_t notes);
          room_c room    = new(notes);
          int    winners = 0;
          helper(room);
          for (int me = 1; me <= N; me++)
            if (find_my_note(room, me)) winners++;
          return winners == N;
        endfunction
        ```

    === "Python"
        ```python
        def cycle_from(notes, start):
            """The boxes met when following the notes from box `start` until back at `start`."""
            cycle = [start]
            box = notes[start]
            while box != start:
                cycle.append(box)
                box = notes[box]
            return cycle


        def helper(room):
            """Person 0: find the one cycle longer than MAX_OPENS (if any) and cut it in half."""
            notes = room.look_all()
            seen = set()
            for start in range(1, N + 1):
                if start in seen:
                    continue
                cycle = cycle_from(notes, start)
                seen.update(cycle)
                if len(cycle) > MAX_OPENS:
                    room.swap(cycle[0], cycle[len(cycle) // 2])   # -> cycles of L/2 and L - L/2
                    return                                        # there is at most one long cycle


        def find_my_note(room, me):
            """Person `me`: open my own box, then always the box whose number is on the note."""
            room.enter()
            box = me
            for _ in range(MAX_OPENS):
                note = room.open_box(box)
                if note == me:
                    return True
                box = note
            return False


        def play(notes):
            """The whole game: person 0 first, then persons 1..N. True when everybody wins."""
            room = Room(notes)
            helper(room)
            winners = [me for me in range(1, N + 1) if find_my_note(room, me)]
            return len(winners) == N
        ```

    **סיבוכיות:** אדם 0 עובר על כל קופסה פעם אחת, \( O(N) \) זמן וזיכרון. כל אחד
    מהאחרים פותח לכל היותר \( N/2 \) קופסאות, וזוכר רק את הקופסה הבאה.

    **בדיקה:** הקוד נבדק על כל אחד מ-231 מבני המעגלים האפשריים של 16 קופסאות (כל חלוקה של
    16 לאורכי מעגלים), ועל 20,000 סידורים אקראיים. בכולם כל 16 האנשים ניצחו, ואדם 0
    השתמש בהחלפה אחת לכל היותר. בלי אדם 0, אותה אסטרטגיה מצליחה רק בכ-34% מהסידורים.

## נקודות חשובות ושאלות המשך

??? note "נקודות שהמראיין מחפש"
    - **פירוק תמורה למעגלים:** "ללכת לפי הפתקים" זה בדיוק לעבור על רשימה מקושרת, וכל
      רשימה כזו נסגרת למעגל.
    - **למה מתחילים מהקופסה שלך?** כך מובטח שאתה על המעגל שמכיל את הפתק שלך. מי שמתחיל
      מקופסה אחרת עלול להסתובב במעגל אחר.
    - **ספירה פשוטה:** אין מקום לשני מעגלים ארוכים, ולכן החלפה אחת מספיקה. 4 ההחלפות הן
      הסחת דעת.
    - **API עם מגבלות:** האכיפה בתוך החדר, ולא "בהבטחה" של מי שקורא לו. זה אותו רעיון כמו
      checker בסביבת אימות.

??? note "שאלות המשך"
    - **בלי אדם 0, מה סיכוי ההצלחה?** הסיכוי שבתמורה אקראית של 16 יש מעגל באורך
      \( L > 8 \) הוא \( \sum_{L=9}^{16} \frac{1}{L} \approx 0.663 \). לכן הסיכוי שכולם מצליחים הוא
      בערך 33.7%. ב-100 האסירים המקוריים הוא בערך 31%.
    - **עם 4 החלפות, כמה פתיחות באמת צריך?** כדי לחתוך מעגל באורך \( L \) לחלקים באורך
      \( m \) לכל היותר צריך \( \lceil L/m \rceil - 1 \) החלפות. עם \( m = 4 \) אף פעם לא
      צריך יותר מ-3 החלפות, ולכן **4 פתיחות מספיקות**. עם \( m = 3 \), מעגל אחד באורך 16 דורש
      5 החלפות, ולכן זה לא תמיד אפשרי.
    - **ומה אם אדם 0 יכול רק להציץ ולא להחליף?** אז הוא לא יכול להעביר מידע לאחרים, וחוזרים
      לסיכוי של כשליש.
