// kinds: transpose
//   transpose              0074        an m x n matrix stored row by row transposed in place, one placement per step: the value in hand put at k m mod (mn - 1) and the one there picked up, the memory shown as the n x m result, every value tinted by its cycle; with a bit per entry, or without marks (each cycle from its leader, the walks counted)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";

  // The cycles of the places: the value at k goes to k m mod (mn - 1); 0 and mn - 1 stay.
  const tpNext = (k, m, size) => (k === size - 1 ? k : (k * m) % (size - 1));
  const tpCycles = (m, n) => {
    const size = m * n, seen = new Set(), out = [];
    for (let s = 0; s < size; s++) {
      if (seen.has(s)) continue;
      const cyc = [];
      for (let p = s; !seen.has(p); p = size > 1 ? tpNext(p, m, size) : p) { seen.add(p); cyc.push(p); }
      out.push(cyc);
    }
    return out;
  };
  // The steps of the walks that look for the leaders without marks (the page's part c).
  const tpWalk = (s, m, size) => {
    let k = (s * m) % (size - 1), steps = 1;
    while (k > s) { k = (k * m) % (size - 1); steps++; }
    return { steps, leader: k === s };
  };
  const tpChecks = (m, n) => {
    const size = m * n;
    if (size <= 2) return 0;
    let total = 0;
    for (let s = 1; s < size - 1; s++) total += tpWalk(s, m, size).steps;
    return total;
  };
  // The placements, as the page's code runs them: the array after each, the value in hand,
  // where it was put, the cycle's start and the walk steps spent so far (without marks).
  const tpSteps = (m, n, leader) => {
    const size = m * n, arr = Array.from({ length: size }, (_, i) => i);
    const frames = [{ arr: arr.slice(), carry: null, at: null, s: null, checks: 0 }];
    if (size <= 2) return frames;
    const done = new Array(size).fill(false);
    let checks = 0;
    for (let s = 1; s < size - 1; s++) {
      if (leader) { const w = tpWalk(s, m, size); checks += w.steps; if (!w.leader) continue; }
      else if (done[s]) continue;
      let k = s, carry = arr[s];
      for (;;) {
        k = (k * m) % (size - 1);
        const put = carry;
        carry = arr[k]; arr[k] = put; done[k] = true;
        frames.push({ arr: arr.slice(), carry: k === s ? null : carry, put, at: k, s, checks });
        if (k === s) break;
      }
    }
    return frames;
  };

  const METHODS = { marks: "ביט לכל איבר (סעיף ב)", leader: "בלי סימון, מהמנהיג (סעיף ג)" };

  const transposeView = () => ({
    mount(box) {
      const clamp = (v) => Math.min(8, Math.max(1, v));
      const d0 = { method: box.dataset.method === "leader" ? "leader" : "marks", m: clamp(Number(box.dataset.m || 2)), n: clamp(Number(box.dataset.n || 3)) };
      const st = { ...d0, s: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>השיטה <select class="tp-method" aria-label="השיטה">${Object.entries(METHODS).map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<label><span>שורות ${ltr("m")}</span><input type="range" class="tp-m" min="1" max="8" step="1" dir="ltr" aria-label="מספר השורות"><output class="tp-mo"></output></label>` +
        `<label><span>עמודות ${ltr("n")}</span><input type="range" class="tp-n" min="1" max="8" step="1" dir="ltr" aria-label="מספר העמודות"><output class="tp-no"></output></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">מההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">ההנחה הבאה</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary tp-sum" aria-live="polite"></p>` +
        `<div class="tp-fig" data-steady></div>` +
        `<span class="viz-legend"><span><i class="pm-key-c1"></i>הצבע : המעגל</span><span><i class="pm-key-hl"></i>ההנחה של הצעד</span><span><i class="tp-key-off"></i>לא זז</span></span>` +
        `<p class="tp-note"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const frames = () => tpSteps(st.m, st.n, st.method === "leader");

      const grid = (title, aria, vals, rows, cols, opts) => {
        let t = `<tr class="pm-head"><th></th>${Array.from({ length: cols }, (_, j) => `<td>${j}</td>`).join("")}</tr>`;
        for (let i = 0; i < rows; i++) {
          t += `<tr><th>${i}</th>${Array.from({ length: cols }, (_, j) => {
            const p = i * cols + j, v = vals[p];
            return `<td class="pm-c ${opts.cls(v, p)}">${v}</td>`;
          }).join("")}</tr>`;
        }
        return `<p class="ex-title">${title}</p><div class="pm-scroll" tabindex="0" role="region" aria-label="${aria}"><table class="pm-cells tp-cells" dir="ltr"><tbody>${t}</tbody></table></div>`;
      };

      const draw = () => {
        const fr = frames(), T = fr.length - 1;
        st.s = Math.min(Math.max(st.s, 0), T);
        const f = fr[st.s], m = st.m, n = st.n, size = m * n;
        $(".tp-method").value = st.method;
        $(".tp-m").value = String(m); $(".tp-mo").textContent = String(m);
        $(".tp-n").value = String(n); $(".tp-no").textContent = String(n);
        $(".ex-pos").textContent = `הנחה ${st.s} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.s === T;
        const cycles = tpCycles(m, n), cyc = new Map();
        cycles.forEach((c, ci) => c.forEach((p) => cyc.set(p, ci)));
        let tint = 0;
        const tintOf = new Map();
        cycles.forEach((c, ci) => { if (c.length > 1) tintOf.set(ci, `c${(tint++ % 5) + 1}`); });
        const cls = (v) => (cycles[cyc.get(v)].length === 1 ? "is-off" : tintOf.get(cyc.get(v)));
        const target = Array.from({ length: size }, (_, k) => { const j = Math.floor(k / m), i = k % m; return i * n + j; });
        $(".tp-fig").innerHTML =
          grid(`המקור, ${ltr(`${m}×${n}`)}`, `המקור, ${m} שורות ו-${n} עמודות`, Array.from({ length: size }, (_, k) => k), m, n, { cls: (v) => cls(v) }) +
          grid(`הזיכרון עכשיו, כמטריצה ${ltr(`${n}×${m}`)}`, `הזיכרון עכשיו, כמטריצה של ${n} שורות ו-${m} עמודות`, f.arr, n, m, { cls: (v, p) => `${cls(v)}${p === f.at ? " is-hl" : ""}${v === target[p] ? " is-done" : ""}` }) +
          `<p class="tp-hand">ביד${NB}: <span class="tp-carry">${f.carry === null ? "—" : f.carry}</span></p>`;
        const long = cycles.filter((c) => c.length > 1).length;
        $(".tp-sum").innerHTML = `${ltr(`${m}×${n}`)}, ${ltr(`mn − 1 = ${size - 1}`)}${NB}: הערך באינדקס ${ltr("k")} עובר ל-${ltr(`${m}k mod ${Math.max(size - 1, 1)}`)}. ` +
          `${ltr(long)} מעגלים שזזים, ${ltr(T)} הנחות. ` +
          (st.method === "leader" ? `בלי סימון, ההליכות לחיפוש המנהיגים${NB}: ${ltr(f.checks)} צעדים עד עכשיו, ${ltr(tpChecks(m, n))} בסך הכול.` : `עם סימון${NB}: ${ltr(size)} ביטים של "בוצע".`);
        $(".tp-note").innerHTML = st.s === 0
          ? (size <= 2 ? "מטריצה של איבר אחד או שניים, או שורה ועמודה אחת : השחלוף לא מזיז כלום." : `מתחילים מ-${ltr("s = 1")}. כל ערך מונח במקום שלו, ומה שהיה שם עולה ליד.`)
          : `מניחים את ${ltr(f.put)} באינדקס ${ltr(f.at)} (${ltr(`${f.put}·${m} mod ${size - 1} = ${f.at}`)})` +
            (f.carry === null ? `, והמעגל של ${ltr(f.s)} נסגר.` : `, ומרימים את ${ltr(f.carry)}.`) +
            (st.method === "leader" ? ` ‏${ltr(f.s)} הוא המנהיג${NB}: אין במעגל שלו אינדקס קטן ממנו.` : "");
        if (st.s === T && T > 0) answer(box, `הזיכרון מחזיק את השחלוף ${ltr(`${n}×${m}`)}, שורה אחרי שורה.`, ".tp-cells .is-hl");
        else answer(box, null);
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.s++; draw(); }, done: () => st.s >= frames().length - 1, restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; draw(); };
      $(".tp-method").addEventListener("change", () => { st.method = $(".tp-method").value; restart(); });
      $(".tp-m").addEventListener("input", () => { st.m = Number($(".tp-m").value); restart(); });
      $(".tp-n").addEventListener("input", () => { st.n = Number($(".tp-n").value); restart(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = frames().length - 1; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, d0); restart(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { transpose: transposeView },
    help: {
      transpose: "בוחרים שיטה ומידות. כל צעד מניח את הערך שביד במקום שלו ומרים את מה שהיה שם. הטבלה העליונה היא המקור, והתחתונה היא הזיכרון עכשיו, מוצג כמטריצה המשוחלפת. ערך שהגיע למקומו מודגש, וכל ערך צבוע לפי המעגל שלו. בלי סימון, הסיכום סופר גם את צעדי ההליכה שמחפשים את מנהיג כל מעגל.",
    },
    models: { tpCycles, tpChecks, tpSteps },
  });
})();
