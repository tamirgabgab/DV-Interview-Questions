// kinds: shapes
//   shapes                 0014        squares or rectangles drawn one at a time with the rejected candidates flashed; a heat map of draws
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { H, W, f, ltr, seedControls } = dvqExplorers.lib;

  // Random shapes without overlap (0014): a shape is [x1, y1, x2, y2] on an N x M grid of
  // points. The page's overlap test and candidate list; one shape drawn by rejection
  // (a candidate at random until one is free, so uniform among the free ones, like the
  // page's choice from the filtered list); a whole draw like random_shapes; a heat map.
  const shapesOverlap = (a, b) => a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3];
  const shapesCandidates = (N, M, squares) => {
    const out = [];
    for (let x1 = 1; x1 < N; x1++) for (let x2 = x1 + 1; x2 <= N; x2++)
      for (let y1 = 1; y1 < M; y1++) for (let y2 = y1 + 1; y2 <= M; y2++)
        if (!squares || x2 - x1 === y2 - y1) out.push([x1, y1, x2, y2]);
    return out;
  };
  const shapesOk = (N, M, shapes, squares) => shapes.every((s, k) =>
    1 <= s[0] && s[0] < s[2] && s[2] <= N && 1 <= s[1] && s[1] < s[3] && s[3] <= M &&
    (!squares || s[2] - s[0] === s[3] - s[1]) && !shapes.slice(0, k).some((t) => shapesOverlap(s, t)));
  // the tries of one draw: candidates picked at random, the last one free (or none free)
  const shapesTry = (N, M, shapes, squares, rnd = Math.random, cap = 60) => {
    const all = shapesCandidates(N, M, squares);
    const free = all.filter((c) => !shapes.some((s) => shapesOverlap(c, s)));
    if (!free.length) return { tries: [], shape: null, free: 0, all: all.length };
    const tries = [];
    for (let k = 0; k < cap; k++) {
      const c = all[Math.floor(rnd() * all.length)];
      tries.push(c);
      if (!shapes.some((s) => shapesOverlap(c, s))) return { tries, shape: c, free: free.length, all: all.length };
    }
    const c = free[Math.floor(rnd() * free.length)];               // the cap hit: pick free directly
    tries.push(c);
    return { tries, shape: c, free: free.length, all: all.length };
  };
  // the page's random_shapes: n uniform in 1..max, retry the whole set until n fit
  const shapesRandom = (N, M, maxShapes, squares, rnd = Math.random) => {
    const all = shapesCandidates(N, M, squares);
    // more shapes than unit cells can never fit (the page's loop would never return)
    const n = 1 + Math.floor(rnd() * Math.min(maxShapes, (N - 1) * (M - 1)));
    for (;;) {
      const shapes = [];
      for (let k = 0; k < n; k++) {
        const free = all.filter((c) => !shapes.some((s) => shapesOverlap(c, s)));
        if (!free.length) break;
        shapes.push(free[Math.floor(rnd() * free.length)]);
      }
      if (shapes.length === n) return shapes;
    }
  };
  // how often every unit cell is covered over `rounds` draws, and the side lengths seen
  const shapesHeat = (N, M, maxShapes, squares, rounds, rnd = Math.random) => {
    const cells = Array.from({ length: M - 1 }, () => new Array(N - 1).fill(0));
    const sides = new Array(Math.max(N, M)).fill(0);
    let count = 0;
    for (let r = 0; r < rounds; r++) {
      for (const [x1, y1, x2, y2] of shapesRandom(N, M, maxShapes, squares, rnd)) {
        count++;
        sides[Math.max(x2 - x1, y2 - y1)]++;
        for (let y = y1; y < y2; y++) for (let x = x1; x < x2; x++) cells[y - 1][x - 1]++;
      }
    }
    return { cells, sides, count, rounds };
  };

  // The shapes box (0014): sliders for the grid and the number of shapes, squares or
  // rectangles; "one shape" draws candidates at random and flashes the overlapping ones
  // in red until a free one lands; "a whole draw" runs the page's random_shapes; a heat
  // map over many draws shows where shapes land and which sizes dominate.
  const shapesView = () => ({
    mount(box) {
      const st = { N: Number(box.dataset.n || 10), M: Number(box.dataset.m || 8), max: Number(box.dataset.max || 6), squares: true, shapes: [], heat: null, flash: null };
      const num = (v) => Number(v).toLocaleString("en-US");
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏N (עמודות)</span><input type="range" class="ex-N" min="3" max="14" step="1" value="${st.N}" dir="ltr"><output class="out-N"></output></label>` +
        `<label><span>‏M (שורות)</span><input type="range" class="ex-M" min="3" max="12" step="1" value="${st.M}" dir="ltr"><output class="out-M"></output></label>` +
        `<label><span>צורות לכל היותר</span><input type="range" class="ex-max" min="1" max="10" step="1" value="${st.max}" dir="ltr"><output class="out-max"></output></label>` +
        `<label><select class="ex-kind" aria-label="סוג הצורות"><option value="squares" selected>ריבועים (סעיף א)</option><option value="rects">מלבנים (סעיף ב)</option></select></label></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-one">עוד צורה</button>` +
        `<button type="button" class="md-button ex-all">הגרלה שלמה</button>` +
        `<button type="button" class="md-button ex-clear">ניקוי</button>` +
        `<button type="button" class="md-button ex-heat">500 הגרלות למפת חום</button><span class="sh-note" aria-live="polite"></span></div>` +
        `<div class="sh-box"><div class="sh-grid"></div><div class="sh-heat"></div></div>` +
        `<p class="sh-step" aria-live="polite"></p><p class="ex-summary sh-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      let timer = null;
      const geom = () => { const u = Math.min(30, 300 / Math.max(st.N - 1, st.M - 1)); return { u, W: (st.N - 1) * u + 40, H: (st.M - 1) * u + 30, X: (x) => 30 + (x - 1) * u, Y: (y) => 10 + (st.M - y) * u }; };
      const gridSvg = (extra, label) => {
        const g = geom();
        let s = `<svg class="figure sh-live" viewBox="0 0 ${f(g.W, 0)} ${f(g.H, 0)}" role="img" aria-label="${label}">`;
        for (let x = 1; x <= st.N; x++) s += `<line class="gp-line" x1="${f(g.X(x))}" x2="${f(g.X(x))}" y1="${f(g.Y(st.M))}" y2="${f(g.Y(1))}"/>`;
        for (let y = 1; y <= st.M; y++) s += `<line class="gp-line" x1="${f(g.X(1))}" x2="${f(g.X(st.N))}" y1="${f(g.Y(y))}" y2="${f(g.Y(y))}"/>`;
        s += extra(g);
        for (let x = 1; x <= st.N; x++) s += `<text class="tick" x="${f(g.X(x))}" y="${f(g.Y(1) + 14)}" text-anchor="middle" font-size="9">${x}</text>`;
        for (let y = 1; y <= st.M; y++) s += `<text class="tick" x="${f(g.X(1) - 8)}" y="${f(g.Y(y) + 3)}" text-anchor="end" font-size="9">${y}</text>`;
        return s + "</svg>";
      };
      const rect = (g, [x1, y1, x2, y2], cls, extra = "") =>
        `<rect class="${cls}" x="${f(g.X(x1))}" y="${f(g.Y(y2))}" width="${f(g.X(x2) - g.X(x1))}" height="${f(g.Y(y1) - g.Y(y2))}"${extra}><title>(${x1}, ${y1}) → (${x2}, ${y2})</title></rect>`;
      const draw = () => {
        ["N", "M", "max"].forEach((k) => { $(`.out-${k}`).textContent = String(st[k]); });
        $(".sh-grid").innerHTML = gridSvg((g) => {
          let s = st.shapes.map((sh, i) => rect(g, sh, i % 2 ? "shp-2" : "shp-1") +
            `<text class="coord halo" x="${f((g.X(sh[0]) + g.X(sh[2])) / 2)}" y="${f((g.Y(sh[1]) + g.Y(sh[3])) / 2 + 4)}" text-anchor="middle" font-size="11">${i + 1}</text>`).join("");
          if (st.flash) s += rect(g, st.flash.shape, st.flash.ok ? "sh-accept" : "sh-reject");
          return s;
        }, `grid של ${st.N} על ${st.M} נקודות עם ${st.shapes.length} צורות`);
        const all = shapesCandidates(st.N, st.M, st.squares).length;
        const free = shapesCandidates(st.N, st.M, st.squares).filter((c) => !st.shapes.some((s) => shapesOverlap(c, s))).length;
        const ok = shapesOk(st.N, st.M, st.shapes, st.squares);
        $(".sh-sum").innerHTML = `${st.squares ? "ריבועים" : "מלבנים"} אפשריים על ה-grid : ${ltr(num(all))}; מהם ${ltr(num(free))} לא חופפים את ${st.shapes.length === 1 ? "הצורה שכבר יש" : `${ltr(st.shapes.length)} הצורות שכבר יש`}. ` +
          (st.shapes.length ? `הבודק ${ltr("shapes_ok")} של הדף : ${ok ? "✓ תקין" : "✗ חפיפה"}.` : "");
        if (st.heat) {
          const h = st.heat, top = Math.max(1, ...h.cells.flat());
          $(".sh-heat").innerHTML = gridSvg((g) => {
            let s = "";
            h.cells.forEach((row, yi) => row.forEach((v, xi) => {
              s += `<rect class="sh-cell" x="${f(g.X(xi + 1))}" y="${f(g.Y(yi + 2))}" width="${f(g.u)}" height="${f(g.u)}" fill-opacity="${f(0.85 * v / top, 2)}"><title>תא (${xi + 1}, ${yi + 1})  : ${v} מתוך ${h.rounds} הגרלות</title></rect>`;
            }));
            return s;
          }, "מפת חום : כמה פעמים כל תא כוסה") +
            `<p class="sh-sides">${ltr(num(h.rounds))} הגרלות, ${ltr(num(h.count))} צורות (${ltr(f(h.count / h.rounds, 2))} בממוצע). לפי הצלע הארוכה : ` +
            h.sides.map((v, k) => (v ? `${ltr(k)}: ${ltr(f(100 * v / h.count, 1) + "%")}` : "")).filter(Boolean).join(", ") +
            `. רוב הצורות קטנות, כי רוב המועמדים קטנים : צלע 1 לבדה היא ${ltr(`${(st.N - 1) * (st.M - 1)} מתוך ${all}`)} ${st.squares ? "הריבועים" : "המלבנים"}${st.squares ? "" : " (וגם מלבנים דקים רבים)"}.</p>`;
        } else $(".sh-heat").innerHTML = "";
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; st.flash = null; };
      const reset = () => { stop(); st.shapes = []; st.heat = null; $(".sh-step").textContent = ""; $(".sh-note").textContent = ""; draw(); };
      ["N", "M", "max"].forEach((k) => $(`.ex-${k}`).addEventListener("input", () => { st[k] = Number($(`.ex-${k}`).value); reset(); }));
      $(".ex-kind").addEventListener("change", () => { st.squares = $(".ex-kind").value === "squares"; reset(); });
      $(".ex-clear").addEventListener("click", reset);
      $(".ex-one").addEventListener("click", () => {
        stop();
        if (st.shapes.length >= st.max) { $(".sh-step").innerHTML = `כבר יש ${ltr(st.max)} צורות, המספר המרבי. "ניקוי" מתחיל מחדש.`; return; }
        const t = shapesTry(st.N, st.M, st.shapes, st.squares);
        if (!t.shape) { $(".sh-step").innerHTML = `<span class="sh-bad">אין מקום לאף צורה נוספת : כל ${ltr(num(t.all))} המועמדים חופפים. הקוד בדף מתחיל את ההגרלה מהתחלה.</span>`; return; }
        let k = 0;
        const step = () => {
          const c = t.tries[k], last = k === t.tries.length - 1;
          st.flash = { shape: c, ok: last };
          $(".sh-step").innerHTML = last
            ? `<span class="sh-ok">✓ ניסיון ${ltr(k + 1)} : ${ltr(`(${c[0]}, ${c[1]}) → (${c[2]}, ${c[3]})`)} לא חופף, נכנס.</span> ${t.tries.length === 1 ? "" : `${ltr(t.tries.length - 1)} מועמדים נדחו לפניו.`} מועמדים פנויים : ${ltr(num(t.free))} מתוך ${ltr(num(t.all))}.`
            : `<span class="sh-bad">✗ ניסיון ${ltr(k + 1)} : ${ltr(`(${c[0]}, ${c[1]}) → (${c[2]}, ${c[3]})`)} חופף צורה קיימת, נדחה.</span>`;
          draw();
          k++;
          if (last) { clearInterval(timer); timer = null; st.shapes.push(c); st.flash = null; draw(); }
        };
        step();
        if (t.tries.length > 1) timer = setInterval(step, 350);
      });
      const seed = seedControls(box, $(".ex-heat"), (rng) => {
        stop(); st.heat = null;
        st.shapes = shapesRandom(st.N, st.M, st.max, st.squares, rng);
        $(".sh-step").innerHTML = `הגרלה שלמה כמו ${ltr("random_shapes")} : ${ltr(st.shapes.length)} ${st.shapes.length === 1 ? "צורה" : "צורות"} (מספר אחיד בין 1 ל-${ltr(st.max)}), כל אחת אחידה מבין המועמדים הפנויים אחרי קודמותיה.`;
        draw();
      });
      $(".ex-all").addEventListener("click", seed.draw);
      $(".ex-heat").addEventListener("click", () => {
        stop();
        $(".sh-note").textContent = "מחשב…";
        setTimeout(() => { st.heat = shapesHeat(st.N, st.M, st.max, st.squares, 500); $(".sh-note").textContent = ""; draw(); }, 20);
      });
      draw();
    },
  });

  dvqExplorers.register({
    views: { shapes: shapesView },
    help: {
      shapes: "״עוד צורה״ מגריל מועמד ומראה את הנדחים בגלל חפיפה, ״הגרלה שלמה״ מציירת את כולן, ו״500 הגרלות״ בונה מפת חום. N, M ומספר הצורות בסליידרים.",
    },
    models: { shapesOverlap, shapesCandidates, shapesOk, shapesTry, shapesRandom, shapesHeat },
  });
})();
