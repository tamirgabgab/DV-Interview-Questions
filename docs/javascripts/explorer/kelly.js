// kinds: kelly
//   kelly                  0096        the Kelly criterion: a fraction f of the wealth bet every round on a win of probability p that pays a times the stake, a loss taking b times the stake. 30 seeded paths of 100 rounds from 100 on a log scale with the median per round and the line 100·e^(g t), beside the curve g(f) with f* and the current f; buttons set f = f* and half of it
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, ltr, mulberry32, seedControls } = dvqExplorers.lib;
  const NB = " ";
  const W0 = 100, ROUNDS = 100, PATHS = 30;

  // --- the models ------------------------------------------------------------------------------

  // the growth rate per round, p ln(1 + a f) + q ln(1 - b f); minus infinity when a loss ruins
  const kyGrowth = (f, p, a, b) => {
    const q = 1 - p;
    if (b * f >= 1) return q > 0 ? -Infinity : p * Math.log1p(a * f);
    return p * Math.log1p(a * f) + (q > 0 ? q * Math.log1p(-b * f) : 0);
  };
  // the page's kelly_fraction: p/b - q/a when p a > q b, else 0
  const kyBest = (p, a, b) => (p * a > (1 - p) * b ? p / b - (1 - p) / a : 0);
  // n seeded paths of the wealth after every round, path after path, one draw a round
  const kyPaths = (seed, f, p, a, b, rounds = ROUNDS, n = PATHS) => {
    const rng = mulberry32(seed), out = [];
    for (let i = 0; i < n; i++) {
      let w = W0;
      const path = [w];
      for (let t = 0; t < rounds; t++) { w *= rng() < p ? 1 + a * f : Math.max(0, 1 - b * f); path.push(w); }
      out.push(path);
    }
    return out;
  };
  // the median of the paths at every round (the mean of the two middle ones for an even count)
  const kyMedian = (paths) => paths[0].map((_, t) => {
    const v = paths.map((p) => p[t]).sort((x, y) => x - y), m = v.length >> 1;
    return v.length % 2 ? v[m] : (v[m - 1] + v[m]) / 2;
  });

  // --- drawing -------------------------------------------------------------------------------------

  const f2 = (v) => v.toFixed(2), f3 = (v) => v.toFixed(3), f4 = (v) => v.toFixed(4);
  const key = (cls, text) => `<span><i class="${cls}"></i><span>${text}</span></span>`;
  const money = (v) => (v >= 1e6 ? v.toExponential(1).replace("e+", " · 10^") : v >= 100 ? Math.round(v).toLocaleString("en-US") : v >= 0.01 ? v.toFixed(2) : v > 0 ? v.toExponential(1).replace("e-", " · 10^-") : "0");
  const LOGMIN = -2, LOGMAX = 9;     // the wealth axis: 0.01 to 10^9
  const SUP = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
  const sup = (d) => String(d).split("").map((c) => SUP[c]).join("");

  // the paths on a log scale between the decades that hold them, the median and the formula
  const pathsSvg = (paths, med, g) => {
    const W = 340, H = 240, X0 = 46, X1 = 330, TOP = 12, BASE = 210;
    let lo = Infinity, hi = -Infinity;
    for (const p of paths) for (const v of p) if (v > 0) { lo = Math.min(lo, Math.log10(v)); hi = Math.max(hi, Math.log10(v)); }
    let d0 = Math.max(LOGMIN, Math.floor(Math.min(lo, 2))), d1 = Math.min(LOGMAX, Math.ceil(Math.max(hi, 2)));
    if (d1 - d0 < 2) d1 = d0 + 2;
    const X = (t) => X0 + (t / ROUNDS) * (X1 - X0);
    const Y = (v) => { const l = v > 0 ? Math.min(Math.max(Math.log10(v), d0), d1) : d0; return BASE - ((l - d0) / (d1 - d0)) * (BASE - TOP); };
    const label = `${paths.length} מסלולים של ההון מ-100 לאורך ${ROUNDS} סיבובים בסקאלה לוגריתמית. החציון אחרי ${ROUNDS} סיבובים ${money(med[ROUNDS])}`;
    let s = `<svg class="perf-chart ky-paths" viewBox="0 0 ${W} ${H}" role="img" aria-label="${label}">`;
    const step = d1 - d0 > 6 ? 2 : 1;
    for (let d = d0; d <= d1; d += step) {
      const y = Y(10 ** d).toFixed(1), lab = d >= 0 && d <= 3 ? (10 ** d).toLocaleString("en-US") : `10${sup(d)}`;
      s += `<line class="grid" x1="${X0}" x2="${X1}" y1="${y}" y2="${y}"/><text class="tick" x="${X0 - 6}" y="${(Number(y) + 4).toFixed(1)}" text-anchor="end">${lab}</text>`;
    }
    for (const p of paths) s += `<polyline class="ky-path" points="${p.map((v, t) => `${X(t).toFixed(1)},${Y(v).toFixed(1)}`).join(" ")}" fill="none" stroke-width="1.2"/>`;
    if (Number.isFinite(g)) {
      const pts = [];
      for (let t = 0; t <= ROUNDS; t += 5) pts.push(`${X(t).toFixed(1)},${Y(W0 * Math.exp(g * t)).toFixed(1)}`);
      s += `<polyline class="s2-line" points="${pts.join(" ")}" fill="none" stroke-width="2.5" stroke-dasharray="7 5"/>`;
    }
    s += `<polyline class="ink-line ky-median" points="${med.map((v, t) => `${X(t).toFixed(1)},${Y(v).toFixed(1)}`).join(" ")}" fill="none" stroke-width="3"/>`;
    for (const t of [0, 50, 100]) s += `<text class="tick" x="${X(t).toFixed(1)}" y="${BASE + 18}" text-anchor="middle">${t}</text>`;
    s += `<line class="axis" x1="${X0}" x2="${X1}" y1="${BASE}" y2="${BASE}"/><text class="tick" x="${X0 - 6}" y="${BASE + 18}" text-anchor="end">t</text></svg>`;
    return s;
  };
  // the curve g(f) on [0, 1] with the zero line, f* and the current f
  const curveSvg = (p, a, b, f, fs) => {
    const W = 340, H = 240, X0 = 50, X1 = 330, TOP = 16, BASE = 210, N = 100;
    const gs = [];
    for (let i = 0; i <= N; i++) gs.push(kyGrowth(i / N, p, a, b));
    const top = Math.max(0.005, ...gs.filter(Number.isFinite), kyGrowth(Math.min(fs, 1), p, a, b)) * 1.2;
    const bottom = -Math.max(top, 0.005) * 1.5;
    const X = (x) => X0 + x * (X1 - X0);
    const Y = (v) => BASE - ((Math.min(Math.max(Number.isFinite(v) ? v : bottom, bottom), top) - bottom) / (top - bottom)) * (BASE - TOP);
    const gf = kyGrowth(f, p, a, b);
    let s = `<svg class="perf-chart ky-curve" viewBox="0 0 ${W} ${H}" role="img" aria-label="קצב הגדילה g לפי f מ-0 עד 1. השיא ב-f* = ${f3(fs)}, וב-f = ${f2(f)} הקצב ${Number.isFinite(gf) ? f4(gf) : "מינוס אינסוף"}">`;
    for (const v of [bottom, 0, top]) s += `<line class="grid" x1="${X0}" x2="${X1}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}"/><text class="tick" x="${X0 - 6}" y="${(Y(v) + 4).toFixed(1)}" text-anchor="end">${v === 0 ? "0" : v.toFixed(3)}</text>`;
    s += `<line class="ink-line" x1="${X0}" x2="${X1}" y1="${Y(0).toFixed(1)}" y2="${Y(0).toFixed(1)}" stroke-width="1.5"/>`;
    s += `<polyline class="s1-line" points="${gs.map((v, i) => `${X(i / N).toFixed(1)},${Y(v).toFixed(1)}`).join(" ")}" fill="none" stroke-width="2.5"/>`;
    const fsIn = Math.min(fs, 1);
    s += `<line class="s1-line" x1="${X(fsIn).toFixed(1)}" x2="${X(fsIn).toFixed(1)}" y1="${TOP}" y2="${BASE}" stroke-width="1" stroke-dasharray="3 3"/>`;
    s += `<circle class="s1-dot ky-best" cx="${X(fsIn).toFixed(1)}" cy="${Y(kyGrowth(fsIn, p, a, b)).toFixed(1)}" r="6"></circle>`;
    s += `<circle class="ink-dot ky-now" cx="${X(f).toFixed(1)}" cy="${Y(gf).toFixed(1)}" r="5"></circle>`;
    for (const x of [0, 0.5, 1]) s += `<text class="tick" x="${X(x).toFixed(1)}" y="${BASE + 18}" text-anchor="middle">${x}</text>`;
    s += `<line class="axis" x1="${X0}" x2="${X1}" y1="${BASE}" y2="${BASE}"/><text class="tick" x="${X0 - 6}" y="${BASE + 18}" text-anchor="end">f</text></svg>`;
    return s;
  };

  const kellyView = () => ({
    mount(box) {
      const d = box.dataset;
      const num = (v, lo, hi, def) => { const x = Number(v); return Number.isFinite(x) && x >= lo && x <= hi ? x : def; };
      const P0 = num(d.p, 0.05, 0.95, 0.6), A0 = num(d.a, 0.2, 5, 1), B0 = num(d.b, 0.1, 1, 1), F0 = num(d.f, 0, 1, 0.2);
      const st = { p: P0, a: A0, b: B0, f: F0, seed: 96 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏p, הסיכוי לזכות</span><input type="range" class="ky-p" min="0.05" max="0.95" step="0.01" value="${P0}" dir="ltr" aria-label="הסיכוי לזכות p"><output class="ky-op"></output></label>` +
        `<label><span>‏a, הזכייה</span><input type="range" class="ky-a" min="0.2" max="5" step="0.1" value="${A0}" dir="ltr" aria-label="הזכייה a, פי כמה מהסכום"><output class="ky-oa"></output></label>` +
        `<label><span>‏b, ההפסד</span><input type="range" class="ky-b" min="0.1" max="1" step="0.05" value="${B0}" dir="ltr" aria-label="ההפסד b, פי כמה מהסכום"><output class="ky-ob"></output></label></div>` +
        `<div class="ex-controls">` +
        `<label><span>‏f, ההימור</span><input type="range" class="ky-f" min="0" max="1" step="0.01" value="${F0}" dir="ltr" aria-label="החלק מההון שמהמרים עליו f"><output class="ky-of"></output></label>` +
        `<button type="button" class="md-button md-button--primary ky-set-best">${ltr("f = f*")}</button>` +
        `<button type="button" class="md-button ky-set-half">חצי Kelly</button>` +
        `<button type="button" class="md-button ky-draw">הגרלה חדשה</button><span class="ky-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<p class="ex-summary ky-sum" aria-live="polite"></p>` +
        `<div class="ky-grid"><div class="ky-pathwrap" data-steady></div><div class="ky-curvewrap" data-steady></div></div>` +
        `<span class="viz-legend">${key("ky-key-path", "מסלול אחד")}${key("ink", "החציון בכל סיבוב")}${key("s2", `הנוסחה ${ltr("100 · e^(g t)")}`)}` +
        `${key("s1", `העקומה ${ltr("g(f)")} והשיא ${ltr("f*")}`)}${key("ink", `ה-${ltr("f")} הנוכחי`)}</span>`;
      const $ = (sel) => box.querySelector(sel);
      const draw = () => {
        const { p, a, b, f } = st, fs = kyBest(p, a, b), g = kyGrowth(f, p, a, b);
        const paths = kyPaths(st.seed, f, p, a, b), med = kyMedian(paths);
        $(".ky-p").value = String(p); $(".ky-op").textContent = f2(p);
        $(".ky-a").value = String(a); $(".ky-oa").textContent = a.toFixed(1);
        $(".ky-b").value = String(b); $(".ky-ob").textContent = f2(b);
        $(".ky-f").value = String(f); $(".ky-of").textContent = f2(f);
        const edge = p * a - (1 - p) * b;
        const best = fs === 0
          ? `אין יתרון (${ltr(`pa − qb = ${f3(edge)}`)})${NB}: הטוב ביותר הוא לא להמר, ${ltr("f* = 0")}.`
          : fs > 1
            ? `ההימור הטוב ביותר ${ltr(`f* = ${f3(fs)}`)}, יותר מכל ההון. בלי הלוואה מהמרים על הכול, ${ltr("f = 1")}.`
            : `ההימור הטוב ביותר ${ltr(`f* = ${f3(fs)}`)}, וקצב הגדילה בו ${ltr(f4(kyGrowth(fs, p, a, b)))} לסיבוב.`;
        const now = Number.isFinite(g)
          ? `ב-${ltr(`f = ${f2(f)}`)} הקצב ${ltr(f4(g))}, והנוסחה ${ltr(`100 · e^(100g)`)} נותנת ${ltr(money(W0 * Math.exp(ROUNDS * g)))}.`
          : `ב-${ltr(`f = ${f2(f)}`)} הפסד אחד מאפס את ההון, והקצב מינוס אינסוף.`;
        $(".ky-sum").innerHTML = `${best} ${now} ההון החציוני של ${ltr(PATHS)} המסלולים אחרי ${ltr(ROUNDS)} סיבובים${NB}: ${ltr(money(med[ROUNDS]))}.`;
        $(".ky-pathwrap").innerHTML = pathsSvg(paths, med, g);
        $(".ky-curvewrap").innerHTML = curveSvg(p, a, b, f, fs);
        answer(box, fs === 0 ? `לא להמר${NB}: ${ltr("f* = 0")}.` : `‏${ltr(`f* = ${f3(fs)}`)}, הקצב ${ltr(f4(kyGrowth(Math.min(fs, 1), p, a, b)))} לסיבוב.`, ".ky-best");
      };
      const seeded = seedControls(box, $(".ky-anchor"), (rng, seed) => { st.seed = seed; draw(); }, { seed: 96 });
      const slider = (cls, k) => $(cls).addEventListener("input", () => { st[k] = Number($(cls).value); draw(); });
      slider(".ky-p", "p"); slider(".ky-a", "a"); slider(".ky-b", "b"); slider(".ky-f", "f");
      $(".ky-set-best").addEventListener("click", () => { st.f = Math.round(Math.min(kyBest(st.p, st.a, st.b), 1) * 100) / 100; draw(); });
      $(".ky-set-half").addEventListener("click", () => { st.f = Math.round((Math.min(kyBest(st.p, st.a, st.b), 1) / 2) * 100) / 100; draw(); });
      $(".ky-draw").addEventListener("click", () => seeded.draw());
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, { p: P0, a: A0, b: B0, f: F0, seed: 96 }); box.querySelector(".ex-seed").value = "96"; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { kelly: kellyView },
    help: {
      kelly: "הסרגלים קובעים את הסיכוי לזכות p, כמה מקבלים בזכייה (a כפול הסכום) וכמה מפסידים בהפסד (b כפול הסכום), ואת f, החלק מההון שמהמרים עליו בכל סיבוב. מימין 30 מסלולים של ההון לאורך 100 סיבובים בסקאלה לוגריתמית, עם החציון בקו עבה והנוסחה 100·e^(g t) בקו מקווקו. משמאל קצב הגדילה g(f) עם השיא f*. \"f = f*\" ו-\"חצי Kelly\" מזיזים את f, ו-\"הגרלה חדשה\" מגריל מסלולים אחרים.",
    },
    models: { kyGrowth, kyBest, kyPaths, kyMedian },
  });
})();
