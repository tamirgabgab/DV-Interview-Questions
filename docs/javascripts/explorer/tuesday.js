// kinds: tuesday
//   tuesday                0015        part b's grid: the 14 × 14 families of (sex, weekday) pairs counted step by step, the row and the column of the information, the shared cell counted once and the families with two boys; the same grid for "at least one boy" and "the elder is a boy"
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { ltr } = dvqExplorers.lib;
  const NB = " ";

  // A child is one of 14 equally likely kinds: 0..6 a boy born on day 0..6 (Sunday first),
  // 7..13 a girl. The information names a set S of kinds and whether it may be either
  // child ("any", "day") or only the first, the elder ("elder"); a family (c1, c2) meets it
  // when c1 is in S, or c2 is in S for the two symmetric kinds.
  const TU_INFOS = ["any", "day", "elder"];
  const tuesdaySet = (info, day) => (info === "day" ? [day] : [0, 1, 2, 3, 4, 5, 6]);
  const tuesdayCount = (info, day = 2) => {
    const S = new Set(tuesdaySet(info, day)), both = info !== "elder", boy = (c) => c < 7;
    let row = 0, col = 0, overlap = 0, cond = 0, hit = 0, quad = 0;
    for (let c1 = 0; c1 < 14; c1++) for (let c2 = 0; c2 < 14; c2++) {
      const a = S.has(c1), b = both && S.has(c2), two = boy(c1) && boy(c2);
      row += a; col += b; overlap += a && b; quad += two;
      if (a || b) { cond++; hit += two; }
    }
    const g = (x, y) => (y ? g(y, x % y) : x), d = g(hit, cond);
    return { size: S.size, row, col, overlap, cond, hit, quad, num: hit / d, den: cond / d };
  };

  // The grid box (0015 part b): the information and the weekday; the counting in four
  // steps (the first child's row, the second child's column, the shared cells counted
  // once, the families with two boys), a tap on a cell names its family, and the three
  // kinds of information side by side.
  const DAYS = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"], LETTER = "אבגדהוש";
  const INFO_NAME = { any: "לפחות אחד הוא בן", day: "יש בן שנולד ביום מסוים", elder: "הבכור הוא בן" };
  const kindName = (c) => `${c < 7 ? "בן" : "בת"}, יום ${DAYS[c % 7]}`;
  const tuesdayView = () => ({
    mount(box) {
      const D = { info: "day", day: Number(box.dataset.day ?? 2), k: 1 };   // opens on step 1, the first child's row lit (step 0 is the empty grid)
      const st = { ...D, cell: null };
      box.innerHTML =
        `<div class="ex-controls"><label>המידע <select class="tu-info">${TU_INFOS.map((i) => `<option value="${i}">${INFO_NAME[i]}</option>`).join("")}</select></label>` +
        `<label class="tu-daylab"><span>היום</span><select class="tu-day">${DAYS.map((d, i) => `<option value="${i}">${d}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">כל הצעדים</button><span class="ex-pos"></span></div>` +
        `<p class="wv-step tu-step" aria-live="polite"></p><div class="tu-grid"></div><p class="tu-cell" aria-live="polite"></p>` +
        `<span class="viz-legend"><span><i class="tu-key-a"></i>נספרת בצעד הזה</span><span><i class="tu-key-two"></i>נספרה פעמיים</span><span><i class="pg-cond"></i>מקיימת את המידע</span><span><i class="pg-hit"></i>מקיימת, ושני בנים</span><span><i class="pg-quad"></i>שני בנים</span></span>` +
        `<div class="tu-table"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const grid = () => {
        const S = new Set(tuesdaySet(st.info, st.day)), both = st.info !== "elder", k = st.k;
        let s = `<svg class="figure tu-live" viewBox="0 0 432 416" style="max-width:27rem" role="img" aria-label="196 המשפחות : השורות הן הילד הראשון והעמודות הילד השני. לחיצה על משבצת מראה את המשפחה">` +
          `<text class="pg-head" x="279" y="16" text-anchor="middle" direction="rtl">בן</text><text class="pg-head" x="414" y="140" text-anchor="middle" direction="rtl">בן</text>` +
          `<text class="pg-head" x="97" y="16" text-anchor="middle" direction="rtl">בת</text><text class="pg-head" x="414" y="322" text-anchor="middle" direction="rtl">בת</text>`;
        for (let c = 0; c < 14; c++) {
          const hl = S.has(c) && st.info === "day" ? " pg-day-hl" : "";
          s += `<text class="pg-day${hl}" x="${357 - 26 * c}" y="36" text-anchor="middle">${LETTER[c % 7]}</text><text class="pg-day${hl}" x="384" y="${61 + 26 * c}" text-anchor="middle">${LETTER[c % 7]}</text>`;
        }
        for (let c1 = 0; c1 < 14; c1++) for (let c2 = 0; c2 < 14; c2++) {
          const a = S.has(c1), b = both && S.has(c2), two = c1 < 7 && c2 < 7, x = 345 - 26 * c2, y = 45 + 26 * c1;
          const cls = k >= 4 && (a || b) && two ? "pg-hit" : k >= 3 && (a || b) ? "pg-cond"
            : k === 2 && a && b ? "tu-two" : (k >= 1 && a) || (k >= 2 && b) ? "tu-a" : "pg-out";
          const sel = st.cell && st.cell[0] === c1 && st.cell[1] === c2 ? " is-sel" : "";
          s += `<rect class="${cls} tu-c${sel}" data-c="${c1},${c2}" x="${x}" y="${y}" width="24" height="24" rx="3"><title>ילד ראשון ${kindName(c1)}, ילד שני ${kindName(c2)}</title></rect>`;
          if (k >= 3 && a && b) s += `<circle class="pg-twice" cx="${x + 12}" cy="${y + 12}" r="7" pointer-events="none"/>`;
        }
        if (k >= 4) s += `<rect class="pg-quad" x="188" y="44" width="182" height="182" pointer-events="none"/>`;
        return s + `<line class="pg-split" x1="188" y1="44" x2="188" y2="408"/><line class="pg-split" x1="6" y1="226" x2="370" y2="226"/></svg>`;
      };
      const stepText = (r) => {
        const what = st.info === "day" ? `בן מיום ${DAYS[st.day]}` : "בן";
        const sum = (a, b, c) => ltr(`${a} + ${b} − ${c} = ${a + b - c}`);
        if (st.k === 0) return `כל ילד הוא אחד מ-14 סוגים שווי הסתברות, ולכן יש ${ltr("14 × 14 = 196")} משפחות. השורות הן הילד הראשון (הבכור) והעמודות הילד השני. לחצו על ״הצעד הבא״.`;
        if (st.k === 1) return `צעד 1${NB}: הילד הראשון הוא ${what}. ${r.size === 1 ? "זו שורה אחת" : `אלה ${ltr(r.size)} שורות`}, ${ltr(r.row)} משפחות, כי הילד השני הוא כל אחד מ-14 הסוגים.`;
        if (st.k === 2) return st.info === "elder" ? `צעד 2${NB}: המידע הוא על הבכור בלבד, ולכן אין עמודה. ההסתברות היא כמו בבחירה של ילד מסוים.`
          : `צעד 2${NB}: הילד השני הוא ${what}, עוד ${ltr(r.col)} משפחות בעמודות. ${r.overlap === 1 ? "המשבצת" : `‏${ltr(r.overlap)} המשבצות`} שבהצטלבות ${r.overlap === 1 ? "נספרה" : "נספרו"} פעמיים.`;
        if (st.k === 3) return st.info === "elder" ? `צעד 3${NB}: אין משבצות כפולות, ולכן ${ltr(r.cond)} משפחות מקיימות את המידע.`
          : `צעד 3${NB}: כל משפחה נספרת פעם אחת, ולכן ${sum(r.row, r.col, r.overlap)} משפחות מקיימות את המידע (העיגול מסמן את ${r.overlap === 1 ? "המשבצת שנספרה" : "המשבצות שנספרו"} פעמיים).`;
        const twoText = st.info === "elder" ? `‏${ltr(r.hit)} מהן הן שני בנים, כי השני הוא בן מכל יום.`
          : st.info === "day" ? `מתוכן שני בנים : הראשון ${what} והשני בן מכל יום, 7, ולהפך עוד 7, פחות המשבצת המשותפת : ${sum(7, 7, 1)}.`
          : `מתוכן שני בנים : כל ${ltr(r.hit)} המשבצות של הריבוע.`;
        return `צעד 4${NB}: ${twoText} ההסתברות היא ${ltr(`${r.hit} / ${r.cond} = ${r.num}/${r.den}`)}.`;
      };
      const draw = () => {
        const r = tuesdayCount(st.info, st.day);
        $(".tu-info").value = st.info; $(".tu-day").value = String(st.day);
        $(".tu-daylab").hidden = st.info !== "day";
        $(".tu-grid").innerHTML = grid();
        $(".tu-step").innerHTML = stepText(r);
        $(".ex-pos").textContent = `צעד ${st.k} מתוך 4`;
        $(".ex-prev").disabled = st.k === 0;
        $(".ex-next").disabled = st.k >= 4;
        $(".ex-end").disabled = st.k >= 4;
        if (st.cell) {
          const [c1, c2] = st.cell, S = new Set(tuesdaySet(st.info, st.day)), ok = S.has(c1) || (st.info !== "elder" && S.has(c2));
          $(".tu-cell").innerHTML = `ילד ראשון${NB}: ${kindName(c1)}. ילד שני${NB}: ${kindName(c2)}. ` +
            (ok ? (c1 < 7 && c2 < 7 ? "מקיימת את המידע, ושני הילדים בנים." : "מקיימת את המידע, ויש בת.") : "לא מקיימת את המידע.");
        } else $(".tu-cell").textContent = "";
        $(".tu-table").innerHTML = `<table class="bridge-table tu-infos"><thead><tr><th>המידע</th><th>מקיימות</th><th>שני בנים</th><th>ההסתברות</th></tr></thead><tbody>` +
          TU_INFOS.map((i) => { const t = tuesdayCount(i, st.day); return `<tr${i === st.info ? ' class="is-now"' : ""}><td>${i === "day" ? `יש בן שנולד ביום ${DAYS[st.day]}` : INFO_NAME[i]}</td><td>${ltr(t.cond)}</td><td>${ltr(t.hit)}</td><td>${ltr(`${t.num}/${t.den}`)}</td></tr>`; }).join("") +
          `</tbody></table>`;
      };
      $(".tu-grid").addEventListener("click", (e) => { const el = e.target.closest(".tu-c"); if (el) { st.cell = el.dataset.c.split(",").map(Number); draw(); } });
      $(".tu-info").addEventListener("change", () => { st.info = $(".tu-info").value; draw(); });
      $(".tu-day").addEventListener("change", () => { st.day = Number($(".tu-day").value); draw(); });
      $(".ex-next").addEventListener("click", () => { if (st.k < 4) st.k++; draw(); });
      $(".ex-prev").addEventListener("click", () => { if (st.k > 0) st.k--; draw(); });
      $(".ex-end").addEventListener("click", () => { st.k = 4; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, D, { cell: null }); draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { tuesday: tuesdayView },
    help: {
      tuesday: "״הצעד הבא״ סופר את המשפחות שמקיימות את המידע : השורה של הילד הראשון, העמודה של הילד השני, המשבצת שנספרה פעמיים, ובסוף המשפחות עם שני בנים. לחיצה על משבצת מראה את המשפחה. בוחרים מידע אחר או יום אחר, והטבלה משווה את שלושת סוגי המידע.",
    },
    models: { tuesdayCount, tuesdaySet, TU_INFOS },
  });
})();
