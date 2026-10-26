// kinds: kappairs
//   kappairs               0013        the 54 pairs (p, q) of part b's proof as a clickable grid: the difference 999p + 90q, its digits by step 3, the case of step 6 (or step 5 for q = 0), conditions a and b, and the arrow to the next pair along the path to 6174
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { f, ltr } = dvqExplorers.lib;
  const NB = " ";

  // One candidate of 0013 part b: the difference 999p + 90q (1 <= p <= 9, 0 <= q <= p),
  // its digits from the column subtraction of step 3, the digits sorted, the next pair
  // (largest minus smallest, the two middle digits' distance), conditions a and b of
  // step 4, and the cases of step 6 that hold (several when two expressions tie).
  // Expressions of step 6: P = p, Q1 = q - 1, N = 9 - q, T = 10 - p.
  const KP_CASES = { "P,Q1": 1, "P,N": 2, "P,T": 3, "N,Q1": 4, "N,T": 5, "T,Q1": 6, "T,N": 7 };
  const kapPair = (p, q) => {
    const value = 999 * p + 90 * q;
    const digits = q >= 1 ? [p, q - 1, 9 - q, 10 - p] : [p - 1, 9, 9, 10 - p];
    const sorted = [...digits].sort((u, v) => v - u);
    const next = [sorted[0] - sorted[3], sorted[1] - sorted[2]];
    let cases = [];
    if (q >= 1) {
      const ex = { P: p, Q1: q - 1, N: 9 - q, T: 10 - p };
      const hi = Math.max(ex.P, ex.N, ex.T), lo = Math.min(ex.Q1, ex.N, ex.T);
      const tops = ["P", "N", "T"].filter((k) => ex[k] === hi), bottoms = ["Q1", "N", "T"].filter((k) => ex[k] === lo);
      tops.forEach((t) => bottoms.forEach((b) => { if (t !== b && KP_CASES[`${t},${b}`]) cases.push(KP_CASES[`${t},${b}`]); }));
      cases = [...new Set(cases)].sort((u, v) => u - v);
    }
    return { p, q, value, digits, sorted, next, condA: next[0] === p, condB: next[1] === q, cases };
  };
  // The pairs from (p, q) until a pair repeats (6174 = (6, 2) points to itself).
  const kapPairPath = (p, q) => {
    const path = [[p, q]];
    for (;;) {
      const [np, nq] = kapPair(...path[path.length - 1]).next;
      if (path.some(([u, v]) => u === np && v === nq)) return path;
      path.push([np, nq]);
    }
  };

  // The pairs box (0013 part b): the grid of the static chart above it, a cell clicked (or
  // picked in the select) shows its difference, the digits of step 3 with the largest and
  // the smallest marked, the case of step 6, conditions a and b, and the arrow to the next
  // pair; the path to 6174 is drawn from the picked cell.
  const CW = 46, CH = 26, GX = 52, GY = 26;
  const NAMES = { P: "p", Q1: "q − 1", N: "9 − q", T: "10 − p" };
  const kappairsView = () => ({
    mount(box) {
      const d0 = box.dataset, P0 = Number(d0.p || 9), Q0 = Number(d0.q || 5);
      const pairs = [];
      for (let p = 1; p <= 9; p++) for (let q = 0; q <= p; q++) pairs.push([p, q]);
      box.innerHTML =
        `<div class="ex-controls"><label>הזוג <select class="kpp-pick" dir="ltr" aria-label="הזוג p, q">` +
        pairs.map(([p, q]) => `<option value="${p}-${q}"${p === P0 && q === Q0 ? " selected" : ""}>(${p}, ${q}) · ${String(999 * p + 90 * q).padStart(4, "0")}</option>`).join("") +
        `</select></label>` +
        `<button type="button" class="md-button md-button--primary ex-next">לזוג הבא</button>` +
        `<button type="button" class="md-button ex-prev">חזרה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לדוגמה של העמוד</button></div>` +
        `<p class="ex-title">הזוגות (p, q) : לחיצה על משבצת בוחרת אותה, והחץ מוביל לזוג של ההפרש הבא</p><div class="kpp-grid"></div>` +
        `<span class="viz-legend"><span><i class="kpp-key-q0"></i>העמודה q = 0 (שלב 5)</span><span><i class="kpp-key-fixed"></i>‏6174, חוזר לעצמו</span><span><i class="kq-key-path"></i>המסלול מהזוג שנבחר</span></span>` +
        `<div class="kpp-text" aria-live="polite"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const st = { p: P0, q: Q0, back: [] };
      const cx = (q) => GX + q * CW + CW / 2, cy = (p) => GY + (p - 1) * CH + CH / 2;
      const grid = () => {
        const path = kapPairPath(st.p, st.q);
        let nums = "";                                    // the numbers, drawn over the path with a halo
        let s = `<svg class="figure kpp-svg" viewBox="0 0 ${GX + 10 * CW + 6} ${GY + 9 * CH + 6}" role="group" aria-label="54 הזוגות, לחיצה על משבצת בוחרת אותה">`;
        for (let q = 0; q <= 9; q++) s += `<text class="tick" x="${cx(q)}" y="${GY - 9}" text-anchor="middle">q = ${q}</text>`;
        for (let p = 1; p <= 9; p++) {
          const y = GY + (p - 1) * CH;
          s += `<text class="tick" x="${GX - 8}" y="${y + CH / 2 + 5}" text-anchor="end">p = ${p}</text>`;
          for (let q = 0; q <= p; q++) {
            const x = GX + q * CW, v = 999 * p + 90 * q, on = p === st.p && q === st.q;
            const cls = p === 6 && q === 2 ? "cell-s2" : q === 0 ? "cell-s1" : "";
            s += `<g class="kpp-cell${on ? " is-pick" : ""}" data-p="${p}" data-q="${q}" tabindex="0" role="button" aria-pressed="${on}" aria-label="${String(v).padStart(4, "0")}, p = ${p}, q = ${q}">` +
                 `<rect class="box-node" x="${x}" y="${y}" width="${CW}" height="${CH}"/>` + (cls ? `<rect class="${cls}" x="${x}" y="${y}" width="${CW}" height="${CH}"/>` : "") +
                 `</g>`;
            nums += `<text class="box-num kpp-num" x="${x + CW / 2}" y="${y + CH / 2 + 5}" text-anchor="middle">${String(v).padStart(4, "0")}</text>`;
          }
        }
        // the path: each arrow bowed to one side, from a cell's edge to the next cell's edge,
        // under the numbers (which keep a halo), so it never hides a value it passes
        const rim = (x, y, dx, dy) => { const t = Math.min(dx ? (CW / 2) / Math.abs(dx) : Infinity, dy ? (CH / 2) / Math.abs(dy) : Infinity); return [x + dx * t, y + dy * t]; };
        path.forEach(([p, q], i) => {
          const [np, nq] = kapPair(p, q).next;
          if (np === p && nq === q) return;
          const x1 = cx(q), y1 = cy(p), x2 = cx(nq), y2 = cy(np), len = Math.hypot(x2 - x1, y2 - y1);
          const mx = (x1 + x2) / 2 - ((y2 - y1) / len) * len * 0.18, my = (y1 + y2) / 2 + ((x2 - x1) / len) * len * 0.18;
          const [ax, ay] = rim(x1, y1, mx - x1, my - y1), [bx, by] = rim(x2, y2, mx - x2, my - y2);
          s += `<path class="kq-path kpp-curve${i ? " kpp-later" : ""}" d="M${f(ax)},${f(ay)} Q${f(mx)},${f(my)} ${f(bx)},${f(by)}"/>` +
               `<circle class="kq-head${i ? " kpp-later" : ""}" cx="${f(bx)}" cy="${f(by)}" r="3.5"/>`;
        });
        return s + nums + "</svg>";
      };
      const text = () => {
        const r = kapPair(st.p, st.q), { p, q } = r, steps = kapPairPath(p, q).length - 1;
        const four = r.digits.join(", ");
        let h = `<p>הזוג ${ltr(`(p, q) = (${p}, ${q})`)}${NB}: ההפרש הוא ${ltr(`999 · ${p} + 90 · ${q} = ${String(r.value).padStart(4, "0")}`)}.</p>`;
        if (q === 0) {
          h += `<p>כאן ${ltr("q = 0")}, ולפי שלב 3 הספרות הן ${ltr(`p − 1, 9, 9, 10 − p = ${four}`)}. שלב 5 פוסל את כל העמודה${NB}: יש בהפרש שתי ספרות 9, ` +
               `ולכן גם ${ltr("c = 9")} ושלוש ספרות 9. ${p === 1 ? `כאן ${ltr("10 − p = 9")}, אבל המרחק בין הגדולה לקטנה הוא 9 ולא 1.` : `כאן אף אחת מ-${ltr(`p − 1 = ${p - 1}`)} ו-${ltr(`10 − p = ${10 - p}`)} איננה 9.`}</p>`;
        } else {
          const ex = { P: p, Q1: q - 1, N: 9 - q, T: 10 - p };
          const hi = r.sorted[0], lo = r.sorted[3];
          const tag = (k) => `${ltr(`${NAMES[k]} = ${ex[k]}`)}${ex[k] === hi ? " (הגדולה)" : ex[k] === lo ? " (הקטנה)" : ""}`;
          h += `<p>לפי שלב 3 הספרות הן ${["P", "Q1", "N", "T"].map(tag).join(", ")}. ` +
               (r.cases.length === 1 ? `זה <b>מקרה ${r.cases[0]}</b> של שלב 6.` : `יש תיקו, ולכן חלים <b>המקרים ${r.cases.join(" ו-")}</b> של שלב 6.`) + `</p>`;
        }
        const [np, nq] = r.next, mids = [r.sorted[1], r.sorted[2]];
        h += `<p>ממוינות${NB}: ${ltr(r.sorted.join(", "))}. ` +
             `<span class="${r.condA ? "eu-ok" : "eu-bad"}">תנאי א${NB}: ${ltr(`${r.sorted[0]} − ${r.sorted[3]} = ${np}`)}${r.condA ? `, שווה ל-${ltr(`p = ${p}`)} ✓` : `, ולא ${ltr(`p = ${p}`)} ✗`}.</span> ` +
             `<span class="${r.condB ? "eu-ok" : "eu-bad"}">תנאי ב${NB}: ${ltr(`${mids[0]} − ${mids[1]} = ${nq}`)}${r.condB ? `, שווה ל-${ltr(`q = ${q}`)} ✓` : `, ולא ${ltr(`q = ${q}`)} ✗`}.</span></p>`;
        h += r.condA && r.condB
          ? `<p><b>שני התנאים מתקיימים${NB}: ‏6174 חוזר לעצמו</b>, והוא המספר המיוחד היחיד מלבד 0.</p>`
          : `<p>לכן ההפרש הבא שייך לזוג ${ltr(`(${np}, ${nq})`)}, כלומר ${ltr(String(999 * np + 90 * nq).padStart(4, "0"))}, והחץ מוביל אליו. ` +
            `מכאן ${ltr(steps)} ${steps === 1 ? "צעד" : "צעדים"} עד 6174.</p>`;
        return h;
      };
      const draw = () => {
        $(".kpp-pick").value = `${st.p}-${st.q}`;
        $(".kpp-grid").innerHTML = grid();
        $(".kpp-text").innerHTML = text();
        $(".ex-prev").disabled = !st.back.length;
        const [np, nq] = kapPair(st.p, st.q).next;
        $(".ex-next").disabled = np === st.p && nq === st.q;
      };
      const go = (p, q, remember = true) => { if (p === st.p && q === st.q) return; if (remember) st.back.push([st.p, st.q]); st.p = p; st.q = q; draw(); };
      const pickCell = (g, keyboard) => {
        go(Number(g.dataset.p), Number(g.dataset.q));
        if (keyboard) { const again = box.querySelector(`.kpp-cell[data-p="${g.dataset.p}"][data-q="${g.dataset.q}"]`); if (again) again.focus(); }
      };
      $(".kpp-grid").addEventListener("click", (e) => { const g = e.target.closest(".kpp-cell"); if (g) pickCell(g, false); });
      $(".kpp-grid").addEventListener("keydown", (e) => { const g = e.target.closest(".kpp-cell"); if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); e.stopPropagation(); pickCell(g, true); } });
      $(".kpp-pick").addEventListener("change", () => { const [p, q] = $(".kpp-pick").value.split("-").map(Number); go(p, q); });
      $(".ex-next").addEventListener("click", () => go(...kapPair(st.p, st.q).next));
      $(".ex-prev").addEventListener("click", () => { if (st.back.length) { const [p, q] = st.back.pop(); go(p, q, false); } });
      $(".ex-reset").addEventListener("click", () => { st.back = []; go(P0, Q0, false); draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { kappairs: kappairsView },
    help: {
      kappairs: "לוחצים על משבצת (או בוחרים זוג ברשימה) : השורות מתחת מראות את ההפרש, את הספרות לפי שלב 3, את המקרה של שלב 6 ואת שני התנאים, והחץ מוביל לזוג הבא. ״לזוג הבא״ הולך בעקבות החץ, ו״חזרה״ חוזר לזוג הקודם.",
    },
    models: { kapPair, kapPairPath },
  });
})();
