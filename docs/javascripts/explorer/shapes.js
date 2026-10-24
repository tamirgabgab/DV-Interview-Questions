// kinds: shapes
//   shapes                 0014        squares or rectangles drawn one at a time with the rejected candidates flashed; a heat map of draws; a toggle for the projections of a rejected candidate and a sandbox of two shapes to drag
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
  // The page's four cases of "no overlap", for b against a: b wholly left, right, below or
  // above a (with <=, so a shared side is allowed). They overlap exactly when none holds,
  // that is when the projections meet on both axes.
  const shapesWhy = (a, b) => {
    const left = b[2] <= a[0], right = b[0] >= a[2], below = b[3] <= a[1], above = b[1] >= a[3];
    return { left, right, below, above, overlap: !(left || right || below || above) };
  };
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
        `<label><input type="checkbox" class="ex-proj" checked> ההטלות על הצירים</label>` +
        `<div class="sh-box"><div class="sh-grid"></div><div class="sh-heat"></div></div>` +
        `<p class="sh-step" aria-live="polite"></p><p class="ex-summary sh-sum"></p>` +
        `<div class="sh-sand"><p class="ex-title">שתי צורות להזזה : גוררים את A או את B (או מקש Tab וחצים), וההטלות והתנאים מתעדכנים</p><div class="sh-sand-svg"></div><ul class="sh-conds"></ul></div>`;
      const $ = (sel) => box.querySelector(sel);
      let timer = null;
      const sand = { a: [2, 2, 5, 4], b: [4, 3, 7, 6], N: 9, M: 7 };   // the sandbox: points 1..9 by 1..7
      // the projections need room below the grid and to its right
      const geom = () => { const u = Math.min(30, 300 / Math.max(st.N - 1, st.M - 1)), pr = $(".ex-proj").checked ? 24 : 0; return { u, W: (st.N - 1) * u + 40 + pr, H: (st.M - 1) * u + 30 + pr, X: (x) => 30 + (x - 1) * u, Y: (y) => 10 + (st.M - y) * u }; };
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
      // the two projections of a pair on both axes, below the grid and to its right
      const projections = (g, a, b, N, M) => {
        const yb = g.Y(1) + 20, xr = g.X(N) + 10;
        let s = "";
        [[a, "sh-pa", 0], [b, "sh-pb", 6]].forEach(([r, cls, d]) => {
          s += `<line class="${cls}" x1="${f(g.X(r[0]))}" x2="${f(g.X(r[2]))}" y1="${f(yb + d)}" y2="${f(yb + d)}"/>` +
               `<line class="${cls}" x1="${f(xr + d)}" x2="${f(xr + d)}" y1="${f(g.Y(r[3]))}" y2="${f(g.Y(r[1]))}"/>`;
        });
        const x0 = Math.max(a[0], b[0]), x1 = Math.min(a[2], b[2]), y0 = Math.max(a[1], b[1]), y1 = Math.min(a[3], b[3]);
        if (x0 < x1) s += `<rect class="sh-pmeet" x="${f(g.X(x0))}" y="${f(yb - 4)}" width="${f(g.X(x1) - g.X(x0))}" height="14"/>`;
        if (y0 < y1) s += `<rect class="sh-pmeet" x="${f(xr - 4)}" y="${f(g.Y(y1))}" width="14" height="${f(g.Y(y0) - g.Y(y1))}"/>`;
        return s;
      };
      // the sandbox: two shapes to drag on a small grid, their projections and the four cases
      const SU = 30, SX = (x) => 30 + (x - 1) * SU, SY = (y) => 10 + (sand.M - y) * SU;
      const drawSand = () => {
        const show = $(".ex-proj").checked;
        $(".sh-sand").hidden = !show;
        if (!show) return;
        const g = { u: SU, X: SX, Y: SY }, W = (sand.N - 1) * SU + 70, Hh = (sand.M - 1) * SU + 50;
        let svg = `<svg class="figure sh-live sh-sandbox" viewBox="0 0 ${W} ${Hh}" role="group" aria-label="שתי צורות להזזה, A ו-B">`;
        for (let x = 1; x <= sand.N; x++) svg += `<line class="gp-line" x1="${SX(x)}" x2="${SX(x)}" y1="${SY(sand.M)}" y2="${SY(1)}"/><text class="tick" x="${SX(x)}" y="${SY(1) + 40}" text-anchor="middle" font-size="9">${x}</text>`;
        for (let y = 1; y <= sand.M; y++) svg += `<line class="gp-line" x1="${SX(1)}" x2="${SX(sand.N)}" y1="${SY(y)}" y2="${SY(y)}"/><text class="tick" x="${SX(1) - 8}" y="${SY(y) + 3}" text-anchor="end" font-size="9">${y}</text>`;
        [["a", "A", "shp-1"], ["b", "B", "shp-2"]].forEach(([k, name, cls]) => {
          const r = sand[k];
          svg += `<g class="sh-drag" data-k="${k}" tabindex="0" role="button" aria-label="${name}, הזזה בגרירה או בחצים"><rect class="${cls}" x="${SX(r[0])}" y="${SY(r[3])}" width="${SX(r[2]) - SX(r[0])}" height="${SY(r[1]) - SY(r[3])}"/>` +
                 `<text class="coord halo" x="${(SX(r[0]) + SX(r[2])) / 2}" y="${(SY(r[1]) + SY(r[3])) / 2 + 4}" text-anchor="middle">${name}</text></g>`;
        });
        svg += projections(g, sand.a, sand.b, sand.N, sand.M) + "</svg>";
        $(".sh-sand-svg").innerHTML = svg;
        const w = shapesWhy(sand.a, sand.b), [a, b] = [sand.a, sand.b];
        const row = (ok, text, math) => `<li class="${ok ? "is-true" : ""}">${text} ${ltr(math)} ${ok ? "✓" : "✗"}</li>`;
        $(".sh-conds").innerHTML = row(w.left, "הצורה B משמאל ל-A,", `B.x2 = ${b[2]} ≤ A.x1 = ${a[0]}`) + row(w.right, "הצורה B מימין ל-A,", `B.x1 = ${b[0]} ≥ A.x2 = ${a[2]}`) +
          row(w.below, "הצורה B מתחת ל-A,", `B.y2 = ${b[3]} ≤ A.y1 = ${a[1]}`) + row(w.above, "הצורה B מעל A,", `B.y1 = ${b[1]} ≥ A.y2 = ${a[3]}`) +
          `<li class="sh-verdict">${w.overlap ? `<span class="sh-bad">אף מקרה לא מתקיים : ההטלות נפגשות על שני הצירים (באדום), והצורות חופפות.</span>` : `<span class="sh-ok">מקרה אחד מספיק : ההטלות על ציר אחד לפחות זרות, ואין חפיפה.</span>`}</li>`;
      };
      // the sandbox is drawn only when it changes, so a tick of the animation keeps its focus
      const draw = () => {
        ["N", "M", "max"].forEach((k) => { $(`.out-${k}`).textContent = String(st[k]); });
        $(".sh-grid").innerHTML = gridSvg((g) => {
          let s = st.shapes.map((sh, i) => rect(g, sh, i % 2 ? "shp-2" : "shp-1") +
            `<text class="coord halo" x="${f((g.X(sh[0]) + g.X(sh[2])) / 2)}" y="${f((g.Y(sh[1]) + g.Y(sh[3])) / 2 + 4)}" text-anchor="middle" font-size="11">${i + 1}</text>`).join("");
          if (st.flash) s += rect(g, st.flash.shape, st.flash.ok ? "sh-accept" : "sh-reject");
          // a rejected candidate: its projections and those of the first shape it overlaps,
          // under the grid (x) and beside it (y), the shared stretch of each in red
          if (st.flash && !st.flash.ok && $(".ex-proj").checked) {
            const c = st.flash.shape, o = st.shapes.find((t) => shapesOverlap(c, t));
            if (o) s += projections(g, c, o, st.N, st.M);
          }
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
      $(".ex-proj").addEventListener("change", () => { drawSand(); draw(); });
      // dragging in the sandbox: whole grid steps, kept inside the grid
      const moveTo = (k, dx, dy) => {
        const r = sand[k], w = r[2] - r[0], h = r[3] - r[1];
        const x1 = Math.max(1, Math.min(sand.N - w, r[0] + dx)), y1 = Math.max(1, Math.min(sand.M - h, r[1] + dy));
        if (x1 === r[0] && y1 === r[1]) return false;
        sand[k] = [x1, y1, x1 + w, y1 + h]; drawSand(); return true;
      };
      let drag = null;
      const at = (e) => { const svg = box.querySelector(".sh-sandbox"), p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY; const q = p.matrixTransform(svg.getScreenCTM().inverse()); return [Math.round((q.x - 30) / SU) + 1, sand.M - Math.round((q.y - 10) / SU)]; };
      $(".sh-sand-svg").addEventListener("pointerdown", (e) => {
        const g = e.target.closest(".sh-drag");
        if (!g) return;
        e.preventDefault();
        drag = { k: g.dataset.k, from: at(e) };
        $(".sh-sand-svg").setPointerCapture(e.pointerId);
      });
      $(".sh-sand-svg").addEventListener("pointermove", (e) => {
        if (!drag) return;
        const [x, y] = at(e);
        if (moveTo(drag.k, x - drag.from[0], y - drag.from[1])) drag.from = [x, y];
      });
      ["pointerup", "pointercancel"].forEach((ev) => $(".sh-sand-svg").addEventListener(ev, () => { drag = null; }));
      $(".sh-sand-svg").addEventListener("keydown", (e) => {
        const g = e.target.closest(".sh-drag"), d = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }[e.key];
        if (!g || !d) return;
        e.preventDefault();
        moveTo(g.dataset.k, d[0], d[1]);
        const again = box.querySelector(`.sh-drag[data-k="${g.dataset.k}"]`); if (again) again.focus();
      });
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
            : `<span class="sh-bad">✗ ניסיון ${ltr(k + 1)} : ${ltr(`(${c[0]}, ${c[1]}) → (${c[2]}, ${c[3]})`)} חופף צורה קיימת, נדחה.</span>` +
              ($(".ex-proj").checked ? ` ההטלות שלו ושל צורה ${ltr(st.shapes.findIndex((t) => shapesOverlap(c, t)) + 1)} נפגשות גם על ציר x (מתחת) וגם על ציר y (מימין) : אף אחד מארבעת המקרים לא מתקיים.` : "");
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
      drawSand();
      draw();
    },
  });

  dvqExplorers.register({
    views: { shapes: shapesView },
    help: {
      shapes: "״עוד צורה״ מגריל מועמד ומראה את הנדחים בגלל חפיפה, ״הגרלה שלמה״ מציירת את כולן, ו״500 הגרלות״ בונה מפת חום. N, M ומספר הצורות בסליידרים. המתג ״ההטלות״ מצייר את ההטלות של מועמד שנדחה ושל הצורה שהוא חופף, ומתחת שתי צורות להזזה עם ארבעת התנאים של הדף.",
    },
    models: { shapesOverlap, shapesWhy, shapesCandidates, shapesOk, shapesTry, shapesRandom, shapesHeat },
  });
})();
