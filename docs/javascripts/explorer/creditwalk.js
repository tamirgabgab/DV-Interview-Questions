// kinds: creditwalk
//   creditwalk             0094        a credit counter between 0 (empty) and N (full) as a random walk, in three models (data-mode): pq, +1 with p and -1 with 1 - p; pqr, +1 with p, -1 with q, no change with r; rates, a credit back with λ1 and one used with λ2 in a cycle (geometric waits), both at once no change. The counter walks cycle by cycle from k (step, to the wall, 100 runs, play, a seed); the walk is drawn over the last 40 cycles, the runs are counted against the formula, and beside it the curves of P(full) and of the expected cycles for every start k
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, mulberry32, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMIN = 2, NMAX = 40, WIN = 40, CAP = 1000000;

  // --- the models ------------------------------------------------------------------------------

  // the walk's p (up only) and q (down only) from the two sliders of a model
  const cwSteps = (mode, a, b) => {
    if (mode === "rates") return { p: a * (1 - b), q: b * (1 - a) };
    if (mode === "pqr") return { p: a, q: b };
    return { p: a, q: 1 - a };
  };
  // the page's walk_odds in floats: P(full), P(empty) and the expected cycles from k
  const cwOdds = (k, N, p, q) => {
    if (k <= 0) return { full: 0, empty: 1, cycles: 0 };
    if (k >= N) return { full: 1, empty: 0, cycles: 0 };
    const s = p + q, a = p / s, b = q / s;
    let full, moves;
    if (Math.abs(a - b) < 1e-12) { full = k / N; moves = k * (N - k); }
    else if (a === 0) { full = 0; moves = k; }
    else {
      const rho = b / a;
      // the form whose powers stay under 1: divide by rho^N when rho > 1
      full = rho < 1 ? (1 - rho ** k) / (1 - rho ** N) : (rho ** -N - rho ** (k - N)) / (rho ** -N - 1);
      moves = (k - N * full) / (b - a);
    }
    return { full, empty: 1 - full, cycles: moves / s };
  };
  // both curves for every start 0..N
  const cwCurves = (N, p, q) => {
    const full = [], cycles = [];
    for (let k = 0; k <= N; k++) { const o = cwOdds(k, N, p, q); full.push(o.full); cycles.push(o.cycles); }
    return { full, cycles };
  };
  // one cycle: +1, -1 or 0; the rates model draws the return first, then the use
  const cwStep = (mode, a, b, rng) => {
    if (mode === "rates") { const back = rng() < a, used = rng() < b; return (back ? 1 : 0) - (used ? 1 : 0); }
    const { p, q } = cwSteps(mode, a, b), u = rng();
    return u < p ? 1 : u < p + q ? -1 : 0;
  };
  // a whole run from k with a seeded generator: the counter after every cycle
  const cwRun = (seed, mode, a, b, k, N) => {
    const rng = mulberry32(seed), path = [k];
    while (path[path.length - 1] > 0 && path[path.length - 1] < N && path.length <= CAP) path.push(path[path.length - 1] + cwStep(mode, a, b, rng));
    return path;
  };

  // --- drawing -------------------------------------------------------------------------------------

  const f2 = (v) => v.toFixed(2), f3 = (v) => v.toFixed(3);
  const key = (cls, text) => `<span><i class="${cls}"></i><span>${text}</span></span>`;
  const MODES = {
    pq: { name: "‏p ו-q = 1 − p", la: "‏p, לעלות", lb: "‏q = 1 − p", a: 0.5, b: 0.5 },
    pqr: { name: "‏p, q ו-r", la: "‏p, לעלות", lb: "‏q, לרדת", a: 0.3, b: 0.2 },
    rates: { name: "‏λ1 ו-λ2, זמנים גאומטריים", la: "‏λ1, החזרה", lb: "‏λ2, צריכה", a: 0.5, b: 0.25 },
  };
  const clampStep = (v) => Math.min(0.95, Math.max(0.05, Math.round(v * 20) / 20));

  // the walk over the last WIN cycles, between the walls 0 and N; a narrow box (a phone)
  // gets a narrower, taller drawing, so its numbers and its steps stay readable
  const walkSvg = (path, N, ended, narrow) => {
    const W = narrow ? 400 : 640, H = narrow ? 250 : 220, X0 = 40, X1 = W - 12, TOP = 14, BASE = H - 30;
    const last = path.length - 1, from = Math.max(0, last - WIN);
    const X = (t) => X0 + ((t - from) / WIN) * (X1 - X0);
    const Y = (v) => BASE - (v / N) * (BASE - TOP);
    const label = `הריצה הנוכחית של המונה, ${last} מחזורים, בין 0 ל-${N}`;
    let s = `<svg class="perf-chart cw-walk" viewBox="0 0 ${W} ${H}" role="img" aria-label="${label}">`;
    const ticks = [0, Math.round(N / 4), Math.round(N / 2), Math.round((3 * N) / 4), N].filter((x, i, arr) => arr.indexOf(x) === i);
    for (const v of ticks) s += `<line class="grid" x1="${X0}" x2="${X1}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}"/><text class="tick" x="${X0 - 8}" y="${(Y(v) + 4).toFixed(1)}" text-anchor="end">${v}</text>`;
    s += `<line class="s1-line" x1="${X0}" x2="${X1}" y1="${Y(N).toFixed(1)}" y2="${Y(N).toFixed(1)}" stroke-width="2.5" stroke-dasharray="6 4"/>`;
    s += `<line class="s2-line" x1="${X0}" x2="${X1}" y1="${Y(0).toFixed(1)}" y2="${Y(0).toFixed(1)}" stroke-width="2.5" stroke-dasharray="6 4"/>`;
    for (let t = Math.ceil(from / 10) * 10; t <= from + WIN; t += 10) s += `<text class="tick" x="${X(t).toFixed(1)}" y="${BASE + 18}" text-anchor="middle">${t}</text>`;
    const pts = path.slice(from).map((v, i) => `${X(from + i).toFixed(1)},${Y(v).toFixed(1)}`).join(" ");
    s += `<polyline class="ink-line" points="${pts}" fill="none" stroke-width="2.5"/>`;
    const v = path[last], cls = ended ? (v === N ? "s1" : "s2") : "ink";
    s += `<circle class="${cls}-dot cw-now-dot" cx="${X(last).toFixed(1)}" cy="${Y(v).toFixed(1)}" r="6"></circle>`;
    s += `<line class="axis" x1="${X0}" x2="${X1}" y1="${BASE}" y2="${BASE}"/><text class="tick" x="${X0 - 8}" y="${BASE + 18}" text-anchor="end">t</text></svg>`;
    return s;
  };
  // a curve over the starts 0..N with the current k marked and the measured value beside it
  const curveSvg = (label, values, N, k, ymax, line, dot, measured, fmtTick) => {
    const W = 320, H = 200, X0 = 40, X1 = 310, TOP = 12, BASE = 170;
    const X = (i) => X0 + (i / N) * (X1 - X0);
    const Y = (v) => BASE - (v / ymax) * (BASE - TOP);
    let s = `<svg class="perf-chart cw-curve" viewBox="0 0 ${W} ${H}" role="img" aria-label="${label}">`;
    for (const v of [0, ymax / 2, ymax]) s += `<line class="grid" x1="${X0}" x2="${X1}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}"/><text class="tick" x="${X0 - 6}" y="${(Y(v) + 4).toFixed(1)}" text-anchor="end">${fmtTick(v)}</text>`;
    s += `<line class="ink-line" x1="${X(k).toFixed(1)}" x2="${X(k).toFixed(1)}" y1="${TOP}" y2="${BASE}" stroke-width="1" stroke-dasharray="3 3"/>`;
    s += `<polyline class="${line}" points="${values.map((v, i) => `${X(i).toFixed(1)},${Y(v).toFixed(1)}`).join(" ")}" fill="none" stroke-width="2.5"/>`;
    if (measured !== null) s += `<circle class="cw-meas" cx="${X(k).toFixed(1)}" cy="${Y(Math.min(measured, ymax)).toFixed(1)}" r="7"></circle>`;
    s += `<circle class="${dot}" cx="${X(k).toFixed(1)}" cy="${Y(values[k]).toFixed(1)}" r="5"></circle>`;
    for (const i of [0, k, N].filter((x, j, arr) => arr.indexOf(x) === j)) s += `<text class="tick" x="${X(i).toFixed(1)}" y="${BASE + 18}" text-anchor="middle">${i}</text>`;
    s += `<line class="axis" x1="${X0}" x2="${X1}" y1="${BASE}" y2="${BASE}"/></svg>`;
    return s;
  };

  const creditwalkView = () => ({
    mount(box) {
      const d = box.dataset;
      const mode0 = MODES[d.mode] ? d.mode : "pq";
      const a0 = d.a !== undefined ? clampStep(Number(d.a)) : MODES[mode0].a;
      const b0 = mode0 === "pq" ? 1 - a0 : d.b !== undefined ? clampStep(Number(d.b)) : MODES[mode0].b;
      const nIn = Number(d.n), N0 = Number.isInteger(nIn) && nIn >= NMIN && nIn <= NMAX ? nIn : 10;
      const kIn = Number(d.k), K0 = Number.isInteger(kIn) && kIn > 0 && kIn < N0 ? kIn : Math.floor(N0 / 2);
      const st = { mode: mode0, a: a0, b: b0, N: N0, k: K0, rng: mulberry32(94), path: [K0], runs: 0, full: 0, cycles: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>המודל</span><select class="cw-mode" aria-label="המודל של המונה">${Object.entries(MODES).map(([m, o]) => `<option value="${m}"${m === mode0 ? " selected" : ""}>${o.name}</option>`).join("")}</select></label>` +
        `<label><span class="cw-la"></span><input type="range" class="cw-a" min="0.05" max="0.95" step="0.05" value="${a0}" dir="ltr" aria-label="ההסתברות הראשונה"><output class="cw-oa"></output></label>` +
        `<label><span class="cw-lb"></span><input type="range" class="cw-b" min="0.05" max="0.95" step="0.05" value="${f2(b0)}" dir="ltr" aria-label="ההסתברות השנייה"><output class="cw-ob"></output></label></div>` +
        `<div class="ex-controls">` +
        `<label><span>‏N</span><input type="text" inputmode="numeric" class="ex-num cw-n" dir="ltr" spellcheck="false" autocomplete="off" value="${N0}" aria-label="הקיר העליון N${NB}: מספר שלם מ-${NMIN} עד ${NMAX}"></label>` +
        `<label><span>‏k, ההתחלה</span><input type="range" class="cw-k" min="1" max="${N0 - 1}" step="1" value="${K0}" dir="ltr" aria-label="נקודת ההתחלה k"><output class="cw-ok">${K0}</output></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err cw-err" role="status"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">מחזור אחד</button>` +
        `<button type="button" class="md-button cw-finish">עד הקיר</button>` +
        `<button type="button" class="md-button cw-many">100 ריצות</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(500, 160, 40) +
        `<button type="button" class="md-button ex-start">ניקוי</button><span class="cw-anchor"></span></div>` +
        `<p class="ex-summary cw-sum" aria-live="polite"></p>` +
        `<div class="cw-grid"><div class="cw-walkwrap" data-steady></div><div class="cw-curves" data-steady></div></div>` +
        `<span class="viz-legend">${key("cw-key-full", "הקיר N, מלא")}${key("cw-key-empty", "הקיר 0, ריק")}${key("ink", "הריצה הנוכחית")}` +
        `${key("s1", "הסיכוי להתמלא מכל k")}${key("s2", "מחזורים בממוצע מכל k")}${key("cw-key-meas", "מה שנמדד בריצות")}</span>` +
        `<p class="cw-now"></p><p class="cw-count"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const steps = () => cwSteps(st.mode, st.a, st.b);
      const ended = () => { const v = st.path[st.path.length - 1]; return v <= 0 || v >= st.N; };
      const finishRun = () => { st.runs++; st.full += st.path[st.path.length - 1] >= st.N ? 1 : 0; st.cycles += st.path.length - 1; };
      const fresh = () => { st.path = [st.k]; };
      const clear = () => { fresh(); st.runs = 0; st.full = 0; st.cycles = 0; };
      const cycle = () => {
        if (ended()) fresh();
        st.path.push(st.path[st.path.length - 1] + cwStep(st.mode, st.a, st.b, st.rng));
        if (ended()) finishRun();
      };
      const toWall = () => {
        if (ended()) fresh();
        while (!ended() && st.path.length <= CAP) st.path.push(st.path[st.path.length - 1] + cwStep(st.mode, st.a, st.b, st.rng));
        finishRun();
      };
      const draw = () => {
        const M = MODES[st.mode], { p, q } = steps(), o = cwOdds(st.k, st.N, p, q), cv = cwCurves(st.N, p, q);
        $(".cw-mode").value = st.mode;
        $(".cw-la").textContent = M.la;
        $(".cw-lb").textContent = M.lb;
        $(".cw-a").value = String(st.a);
        $(".cw-b").value = f2(st.b);
        $(".cw-b").disabled = st.mode === "pq";
        $(".cw-oa").textContent = f2(st.a);
        $(".cw-ob").textContent = f2(st.b);
        if (document.activeElement !== $(".cw-n")) $(".cw-n").value = String(st.N);
        $(".cw-k").max = String(st.N - 1);
        $(".cw-k").value = String(st.k);
        $(".cw-ok").textContent = String(st.k);
        const r = 1 - p - q;
        const model = st.mode === "rates"
          ? `החזרה ב-${ltr(`λ1 = ${f2(st.a)}`)} וצריכה ב-${ltr(`λ2 = ${f2(st.b)}`)}${NB}: המונה עולה ב-${ltr(`p = λ1(1 − λ2) = ${f3(p)}`)}, יורד ב-${ltr(`q = λ2(1 − λ1) = ${f3(q)}`)} ונשאר ב-${ltr(`r = ${f3(r)}`)}.`
          : st.mode === "pqr"
            ? `המונה עולה ב-${ltr(`p = ${f2(p)}`)}, יורד ב-${ltr(`q = ${f2(q)}`)} ונשאר ב-${ltr(`r = ${f2(Math.max(0, r))}`)}. לאן הוא מגיע תלוי רק ב-${ltr(`p/(p + q) = ${f3(p / (p + q))}`)}.`
            : `המונה עולה ב-${ltr(`p = ${f2(p)}`)} ויורד ב-${ltr(`q = ${f2(q)}`)}.`;
        $(".cw-sum").innerHTML = `${model} מ-${ltr(`k = ${st.k}`)} עם ${ltr(`N = ${st.N}`)}, לפי הנוסחה${NB}: מתמלא ב-${ltr(f3(o.full))}, מתרוקן ב-${ltr(f3(o.empty))}, ובממוצע ${ltr(o.cycles.toFixed(2))} מחזורים.`;
        const done = ended();
        $(".cw-walkwrap").innerHTML = walkSvg(st.path, st.N, done, box.clientWidth > 0 && box.clientWidth < 520);
        const emax = Math.max(...cv.cycles) || 1, ytop = Math.max(2, Math.ceil((emax * 1.1) / 2)) * 2;
        $(".cw-curves").innerHTML =
          curveSvg(`הסיכוי להתמלא מכל נקודת התחלה מ-0 עד ${st.N}, ובנקודה ${st.k} הוא ${f3(o.full)}`, cv.full, st.N, st.k, 1, "s1-line", "s1-dot cw-at", st.runs ? st.full / st.runs : null, (v) => (v === 0.5 ? "0.5" : String(v))) +
          curveSvg(`מספר המחזורים הממוצע מכל נקודת התחלה מ-0 עד ${st.N}, ובנקודה ${st.k} הוא ${o.cycles.toFixed(2)}`, cv.cycles, st.N, st.k, ytop, "s2-line", "s2-dot cw-at", st.runs ? st.cycles / st.runs : null, (v) => String(Math.round(v)));
        const last = st.path.length - 1, v = st.path[last];
        $(".cw-now").innerHTML = !last ? `הריצה מתחילה ב-${ltr(st.k)} credits. "מחזור אחד" מזיז את המונה פעם אחת.`
          : done ? `הריצה נגמרה אחרי ${ltr(last)} מחזורים${NB}: ${v >= st.N ? `המונה <b class="cw-tag cw-tag-full">התמלא</b>, הגיע ל-${ltr(st.N)}` : `המונה <b class="cw-tag cw-tag-empty">התרוקן</b>, הגיע ל-${ltr(0)}`}.`
          : `מחזור ${ltr(last)}${NB}: המונה ב-${ltr(v)}.`;
        $(".cw-count").innerHTML = !st.runs ? `עוד אין ריצות שהסתיימו. "עד הקיר" מסיים ריצה, ו-"100 ריצות" מוסיף מאה.`
          : `עד עכשיו ${ltr(st.runs)} ריצות${NB}: ${ltr(st.full)} התמלאו, כלומר ${ltr(f3(st.full / st.runs))} (בנוסחה ${ltr(f3(o.full))}), ו-${ltr(st.runs - st.full)} התרוקנו. ` +
            `בממוצע ${ltr((st.cycles / st.runs).toFixed(2))} מחזורים לריצה (בנוסחה ${ltr(o.cycles.toFixed(2))}).`;
        answer(box, `מ-${ltr(st.k)} עם ${ltr(`N = ${st.N}`)}${NB}: הסיכוי להתמלא ${ltr(f3(o.full))}, להתרוקן ${ltr(f3(o.empty))}, ובממוצע ${ltr(o.cycles.toFixed(2))} מחזורים.`, ".cw-at");
      };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { cycle(); draw(); }, done: () => false, restart: () => {} });
      const restart = () => { stop(); clear(); draw(); };
      seedControls(box, $(".cw-anchor"), (rng) => { stop(); st.rng = rng; clear(); draw(); }, { seed: 94, fresh: false });
      $(".cw-mode").addEventListener("change", () => {
        st.mode = MODES[$(".cw-mode").value] ? $(".cw-mode").value : "pq";
        st.a = MODES[st.mode].a;
        st.b = MODES[st.mode].b;
        restart();
      });
      $(".cw-a").addEventListener("input", () => {
        st.a = clampStep(Number($(".cw-a").value));
        if (st.mode === "pq") st.b = 1 - st.a;
        else if (st.mode === "pqr" && st.a + st.b > 1 + 1e-9) st.b = clampStep(1 - st.a);
        restart();
      });
      $(".cw-b").addEventListener("input", () => {
        st.b = clampStep(Number($(".cw-b").value));
        if (st.mode === "pqr" && st.a + st.b > 1 + 1e-9) st.a = clampStep(1 - st.b);
        restart();
      });
      $(".cw-n").addEventListener("change", () => {
        const t = $(".cw-n").value.trim(), n = Number(t);
        if (!/^\d+$/.test(t) || n < NMIN || n > NMAX) { $(".cw-err").textContent = `‏N${NB}: מספר שלם מ-${NMIN} עד ${NMAX}`; return; }
        $(".cw-err").textContent = "";
        st.N = n;
        st.k = Math.min(Math.max(st.k, 1), n - 1);
        restart();
      });
      $(".cw-k").addEventListener("input", () => { st.k = Math.min(Math.max(Math.round(Number($(".cw-k").value)), 1), st.N - 1); restart(); });
      $(".ex-next").addEventListener("click", () => { cycle(); draw(); });
      $(".cw-finish").addEventListener("click", () => { stop(); toWall(); draw(); });
      $(".cw-many").addEventListener("click", () => { stop(); for (let i = 0; i < 100; i++) toWall(); draw(); });
      $(".ex-start").addEventListener("click", restart);
      $(".ex-reset").addEventListener("click", () => {
        stop();
        $(".cw-err").textContent = "";
        Object.assign(st, { mode: mode0, a: a0, b: b0, N: N0, k: K0 });
        clear();
        draw();
      });
      draw();
    },
  });

  dvqExplorers.register({
    views: { creditwalk: creditwalkView },
    help: {
      creditwalk: "בוחרים מודל : p ו-q, או p, q ו-r, או λ1 ו-λ2 של הזמנים הגאומטריים. N הוא הקיר העליון ו-k נקודת ההתחלה. \"מחזור אחד\" מזיז את המונה פעם אחת, \"עד הקיר\" מסיים את הריצה, ו-\"100 ריצות\" מוסיף מאה ריצות לספירה. הספירה מושווית לנוסחה, ובשני הגרפים העקומות של הסיכוי להתמלא ושל מספר המחזורים הממוצע לכל k, עם העיגול הריק של מה שנמדד.",
    },
    models: { cwSteps, cwOdds, cwCurves, cwStep, cwRun },
  });
})();
