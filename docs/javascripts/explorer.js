// Interactive explorers: a box `<div class="explorer" data-kind="..." data-...>` gets
// sliders, a summary line and charts that redraw on every change. One model per kind:
//   cake-arith / cake-geo  0027, 0028  sliders a and d (or q): shares and fractions vs T
//   motorcycle             0026        sliders t0 and t1: the position-time chart
//   josephus               0016, 0022  sliders N (and L): the survivor of every circle size
// The math of each model is exported under Node, where the question tests compare it with
// the Python reference (tests/0016, 0022, 0026, 0027, 0028).
(() => {
  const EPS = 1e-9;

  // --- models: pure math ---------------------------------------------------------------

  // Cake: person k takes p of what is left (R); a fraction of 1 or more takes the rest.
  const cakeSplit = (kind, a, step) => {
    const rows = [];
    let R = 1;
    for (let k = 1; k <= 2000; k++) {
      const raw = kind === "arith" ? a + (k - 1) * step : a * Math.pow(step, k - 1);
      const p = Math.min(raw, 1);
      rows.push({ k, p, R, S: p * R });
      if (p >= 1) break;
      R *= 1 - p;
    }
    return rows;
  };
  const cakeThreshold = (kind, step) =>
    kind === "arith" ? (Math.sqrt(step * step + 4 * step) - step) / 2 : 1 - 1 / step;
  const cakeFormula = (kind, a, step) => {
    const T = cakeThreshold(kind, step);
    const x = kind === "arith" ? (T - a) / step + 1 : Math.log((step - 1) / a) / Math.log(step);
    const k = Math.max(1, Math.ceil(x - EPS));
    const pk = kind === "arith" ? a + (k - 1) * step : a * Math.pow(step, k - 1);
    return { k, tie: Math.abs(pk - T) < EPS };
  };
  const cakeBest = (rows) => {
    const top = Math.max(...rows.map((r) => r.S));
    return rows.filter((r) => Math.abs(r.S - top) <= EPS * top).map((r) => r.k);
  };

  // Motorcycle (0026), units AB = 1 and ride time 1: the segments, points and phase ends.
  const motorcyclePlan = (alpha) => {
    const x = (alpha - 1) / (alpha * (alpha + 3));
    const y = (alpha + 1) / (alpha * (alpha + 3));
    const z = alpha * x;
    const Q = y, C = y + x, D = C + z, E = D + x;
    const t1 = D, t2 = D + z, T = t2 + (1 - C);
    return { x, y, z, r: y, Q, C, D, E, t1, t2, T };
  };
  const motorcycleTime = (t0, t1) => (3 * t0 + t1) / (t0 + 3 * t1) * t1;

  // Josephus (0016, 0022): person 0 stays, the next L - 1 leave, and so on around.
  const josephusRun = (n, L) => {
    const circle = Array.from({ length: n }, (_, i) => i);
    let i = 0;
    while (circle.length > 1) {
      const leave = Math.min(L - 1, circle.length - 1);   // fixed before anyone leaves
      for (let s = 0; s < leave; s++) {
        const j = (i + 1) % circle.length;
        circle.splice(j, 1);
        if (j < i) i -= 1;
      }
      i = (i + 1) % circle.length;
    }
    return circle[0];
  };
  const josephusZero = (n, L) => {
    let m = 1 + ((n - 1) % (L - 1));
    while (m * L <= n) m *= L;
    return m;
  };
  const josephusFormula = (n, L) => (L * (n - josephusZero(n, L))) / (L - 1);

  const models = {
    cakeSplit, cakeThreshold, cakeFormula, cakeBest,
    motorcyclePlan, motorcycleTime, josephusRun, josephusZero, josephusFormula,
  };
  if (typeof module !== "undefined" && module.exports) {
    module.exports = models;
    return;
  }

  // --- drawing helpers ---------------------------------------------------------------

  const f = (v, n = 1) => Number(v).toFixed(n);
  const ltr = (x) => `<bdi dir="ltr">${x}</bdi>`;   // math and numbers inside Hebrew text
  const fmt = (v, n = 3) => Number(v).toFixed(n);
  const W = 640, H = 230, X0 = 46, RIGHT = 12, TOP = 14, BASE = 198;

  // A chart frame with n slots along x and the value range [0, ymax] along y.
  const frame = (label, n, ymax, yticks, tickFmt = (v) => String(v)) => {
    const slot = (W - X0 - RIGHT) / n;
    const Y = (v) => BASE - (v / ymax) * (BASE - TOP);
    const cx = (k) => X0 + (k - 0.5) * slot;
    let s = `<svg class="perf-chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="${label}">`;
    yticks.forEach((v) => {
      s += `<line class="grid" x1="${X0}" x2="${W - RIGHT}" y1="${f(Y(v))}" y2="${f(Y(v))}"/>` +
           `<text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${tickFmt(v)}</text>`;
    });
    const every = Math.ceil(n / 16);
    const xtick = (k, label = k) =>
      `<text class="tick" x="${f(cx(k))}" y="${BASE + 18}" text-anchor="middle">${label}</text>`;
    const close = () => `<line class="axis" x1="${X0}" x2="${W - RIGHT}" y1="${BASE}" y2="${BASE}"/></svg>`;
    return { s, slot, Y, cx, every, xtick, close };
  };

  const hline = (fr, v, label) =>
    `<line class="ink-line" x1="${X0}" x2="${W - RIGHT}" y1="${f(fr.Y(v))}" y2="${f(fr.Y(v))}" ` +
    `stroke-width="1.5" stroke-dasharray="6 4"/>` +
    (label ? `<text class="legend" x="${X0 + 6}" y="${f(fr.Y(v) - 6)}">${label}</text>` : "");

  const barsChart = (label, values, highlight, titleOf) => {
    const vmax = Math.max(...values);
    const ymax = Math.ceil(vmax * 20 + 0.6) / 20;
    const ticks = [];
    for (let v = 0; v <= ymax + 1e-9; v += 0.05) ticks.push(Math.round(v * 100) / 100);
    const fr = frame(label, values.length, ymax, ticks, (v) => v.toFixed(2));
    let s = fr.s;
    values.forEach((v, i) => {
      const k = i + 1, bw = Math.max(fr.slot * 0.68, 1);
      const cls = highlight.includes(k) ? "by-enum" : "by-multiples";
      s += `<rect class="bar ${cls}" x="${f(fr.cx(k) - bw / 2)}" y="${f(fr.Y(v))}" width="${f(bw)}" ` +
           `height="${f(BASE - fr.Y(v))}"><title>${titleOf(k, v)}</title></rect>`;
      if (k % fr.every === 0 || k === 1 || highlight.includes(k)) s += fr.xtick(k);
    });
    return s + fr.close();
  };

  // --- views: one per kind ----------------------------------------------------------------

  const cakeView = (kind) => ({
    sliders: kind === "arith"
      ? [{ key: "a", label: "השבר הראשון a", min: 0.005, max: 0.6, step: 0.005 },
         { key: "step", label: "ההפרש d", min: 0.01, max: 0.5, step: 0.01 }]
      : [{ key: "a", label: "השבר הראשון a", min: 0.001, max: 0.5, step: 0.001 },
         { key: "step", label: "המנה q", min: 1.05, max: 2, step: 0.05 }],
    draw(st) {
      const rows = cakeSplit(kind, st.a, st.step);
      const peak = cakeBest(rows);
      const T = cakeThreshold(kind, st.step);
      const fm = cakeFormula(kind, st.a, st.step);
      const who = peak.length > 1 ? `תיקו בין האדם ה-${peak[0]} לאדם ה-${peak[1]}` : `האדם ה-${peak[0]}`;
      const agree = fm.k === peak[0] && fm.tie === (peak.length > 1);
      const summary = `המקבל הגדול: ${who}, עם ${fmt(rows[peak[0] - 1].S)} מהעוגה, מתוך ${rows.length} אנשים. ` +
        `הסף הוא ${ltr(`T ≈ ${fmt(T)}`)}, והנוסחה נותנת את האדם ה-${fm.k}${fm.tie ? " (תיקו עם הבא)" : ""}` +
        `${agree ? ", בדיוק כמו בעמודות." : ", שלא כמו בעמודות."}`;
      const shares = barsChart("החלק של כל אדם", rows.map((r) => r.S), peak, (k, v) => `S(${k}) = ${fmt(v, 4)}`);
      const fr = frame("השבר של כל אדם מול הסף", rows.length, 1, [0, 0.25, 0.5, 0.75, 1]);
      let fs = fr.s + hline(fr, T, `T ≈ ${fmt(T)}`);
      rows.forEach((r) => {
        const cls = r.k === peak[0] ? "s2" : r.p < T - EPS ? "s1" : "ink";
        const rad = r.k === peak[0] ? 6 : Math.min(4.5, Math.max(1.5, fr.slot * 0.35));
        fs += `<line class="${cls}-line" x1="${f(fr.cx(r.k))}" x2="${f(fr.cx(r.k))}" y1="${BASE}" y2="${f(fr.Y(r.p))}" ` +
              `stroke-width="${f(Math.min(2, fr.slot * 0.4))}"/>` +
              `<circle class="${cls}-dot" cx="${f(fr.cx(r.k))}" cy="${f(fr.Y(r.p))}" r="${f(rad)}">` +
              `<title>p(${r.k}) = ${fmt(r.p, 4)}</title></circle>`;
        if (r.k % fr.every === 0 || r.k === 1 || r.k === peak[0]) fs += fr.xtick(r.k);
      });
      return { summary, charts: [["החלק של כל אדם", shares], ["השבר של כל אדם מול הסף", fs + fr.close()]] };
    },
  });

  const motorcycleView = () => ({
    sliders: [
      { key: "t0", label: "הליכה של כל הדרך t0 (שעות)", min: 2, max: 30, step: 1 },
      { key: "t1", label: "נסיעה של כל הדרך t1 (שעות)", min: 0.5, max: 3, step: 0.5 },
    ],
    draw(st) {
      const alpha = st.t0 / st.t1;
      if (alpha <= 1 + EPS) {
        return { summary: `יחס המהירויות ${ltr(`α = ${f(alpha, 2)}`)}: האופנוע לא מהיר מההליכה, ולכן כולם פשוט הולכים, ${fmt(st.t0, 2)} שעות.`, charts: [] };
      }
      const pl = motorcyclePlan(alpha);
      const T = pl.T * st.t1;
      const naive = 3 * st.t1, meanwhile = (3 * alpha - 1) / (alpha + 1) * st.t1;
      const summary = `יחס המהירויות ${ltr(`α = ${f(alpha, 2)}`)}. שלושתם מגיעים אחרי ${fmt(T, 2)} שעות ` +
        `(להסיע אחד ולחזור: ${fmt(naive, 2)}, ההולך יוצא בינתיים: ${fmt(meanwhile, 2)}, רק ברגל: ${fmt(st.t0, 2)}). ` +
        `הנוסע יורד אחרי ${fmt(pl.D, 3)} מהדרך, וכל אחד מהשניים הולך ${fmt(pl.y + pl.x, 3)} ממנה.`;
      const w = 640, h = 280, x0 = 52, right = 24, top = 30, base = 246;
      const X = (t) => x0 + (t / pl.T) * (w - x0 - right);
      const Y = (v) => base - v * (base - top);
      let s = `<svg class="perf-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="המקום של האופנוע ושל שני ההולכים לאורך הזמן">`;
      [[0, "0"], [pl.C, fmt(pl.C, 3)], [pl.D, fmt(pl.D, 3)], [1, "1"]].forEach(([v, lab]) => {
        s += `<line class="grid" x1="${x0}" x2="${w - right}" y1="${f(Y(v))}" y2="${f(Y(v))}"/>` +
             `<text class="tick" x="${x0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${lab}</text>`;
      });
      [0, pl.t1, pl.t2, pl.T].forEach((t) => {
        s += `<line class="grid" x1="${f(X(t))}" x2="${f(X(t))}" y1="${top - 6}" y2="${base}" stroke-dasharray="4 4"/>` +
             `<text class="tick" x="${f(X(t))}" y="${base + 18}" text-anchor="middle">${fmt(t * st.t1, 2)}</text>`;
      });
      const path = (pts) => pts.map(([t, v]) => `${f(X(t))},${f(Y(v))}`).join(" ");
      s += `<polyline class="ink-line" points="${path([[0, 0], [pl.t1, pl.D], [pl.t2, pl.C], [pl.T, 1]])}" fill="none" ` +
           `stroke-width="7" stroke-opacity="0.28" stroke-linejoin="round"/>` +
           `<polyline class="s1-line" points="${path([[0, 0], [pl.t1, pl.D], [pl.t2, pl.E], [pl.T, 1]])}" fill="none" stroke-width="2.5"/>` +
           `<polyline class="s2-line" points="${path([[0, 0], [pl.t1, pl.Q], [pl.t2, pl.C], [pl.T, 1]])}" fill="none" stroke-width="2.5"/>`;
      [["D", pl.t1, pl.D, "s1-dot", -12], ["C", pl.t2, pl.C, "s2-dot", 22], ["B", pl.T, 1, "ink-dot", -8]].forEach(([n, t, v, cls, dy]) => {
        s += `<circle class="${cls}" cx="${f(X(t))}" cy="${f(Y(v))}" r="5"/>` +
             `<text class="legend" x="${f(X(t) - (n === "B" ? 14 : 0))}" y="${f(Y(v) + dy)}" text-anchor="middle">${n}</text>`;
      });
      s += `<line class="axis" x1="${x0}" x2="${w - right}" y1="${base}" y2="${base}"/></svg>`;
      return { summary, charts: [["המקום על הדרך (0 הוא A ו-1 הוא B) מול הזמן בשעות", s]] };
    },
  });

  const josephusView = (box) => {
    const withL = box.dataset.lmax && Number(box.dataset.lmax) > Number(box.dataset.l);
    const sliders = [{ key: "n", label: "מספר האנשים N", min: 1, max: Number(box.dataset.nmax || 64), step: 1 }];
    if (withL) sliders.push({ key: "l", label: `הכלל ${ltr("L")}: אחד נשאר, ${ltr("L − 1")} יוצאים`, min: 2, max: Number(box.dataset.lmax), step: 1 });
    return {
      sliders,
      draw(st) {
        const L = st.l, n = st.n, nmax = sliders[0].max;
        const sim = josephusRun(n, L), form = josephusFormula(n, L), M = josephusZero(n, L);
        const summary = `עם ${ltr(`N = ${n}`)} ו-${ltr(`L = ${L}`)} השורד הוא ${sim} בסימולציה, והנוסחה ` +
          `${ltr(`${L}(N − M) / ${L - 1}`)} עם נקודת האפס ${ltr(`M = ${M}`)} נותנת ${form}` +
          `${sim === form ? ", אותו דבר." : ", שלא כמו בסימולציה."}` +
          (L === 2 ? ` בבינארי: ${ltr(`N = ${n.toString(2)}`)}, והשורד ${ltr(sim.toString(2))}.` : "");
        const vals = Array.from({ length: nmax }, (_, i) => josephusRun(i + 1, L));
        const ymax = Math.max(nmax, 1);
        const step = ymax > 40 ? 16 : 8;
        const ticks = [];
        for (let v = 0; v <= ymax; v += step) ticks.push(v);
        const fr = frame("השורד לכל גודל מעגל", nmax, ymax, ticks);
        let s = fr.s;
        vals.forEach((v, i) => {
          const k = i + 1;
          const cls = k === n ? "s2-dot" : v === 0 ? "ink-dot" : "s1-dot";
          s += `<circle class="${cls}" cx="${f(fr.cx(k))}" cy="${f(fr.Y(v))}" r="${k === n ? 6 : Math.min(4, fr.slot * 0.4).toFixed(1)}">` +
               `<title>N = ${k}: ${v}</title></circle>`;
          if (k % fr.every === 0 || k === 1 || k === n) s += fr.xtick(k);
        });
        return { summary, charts: [["השורד לכל N, עם N הנבחר מודגש; נקודות שחורות הן נקודות אפס", s + fr.close()]] };
      },
    };
  };

  const VIEWS = {
    "cake-arith": () => cakeView("arith"),
    "cake-geo": () => cakeView("geo"),
    motorcycle: motorcycleView,
    josephus: josephusView,
  };

  // --- the box -----------------------------------------------------------------------------

  const setup = (box) => {
    const make = VIEWS[box.dataset.kind];
    if (!make) return;
    const view = make(box);
    const defaults = {};
    view.sliders.forEach((sl) => { defaults[sl.key] = Number(box.dataset[sl.key] ?? sl.min); });
    const state = { ...defaults };
    if (state.l === undefined) state.l = Number(box.dataset.l || 2);
    const controls = document.createElement("div");
    controls.className = "ex-controls";
    const inputs = [], outputs = {};
    view.sliders.forEach((sl) => {
      const label = document.createElement("label");
      const id = `ex-${box.dataset.kind}-${sl.key}-${Math.random().toString(36).slice(2, 7)}`;
      label.htmlFor = id;
      label.innerHTML = `<span>${sl.label}</span>`;
      const input = document.createElement("input");
      Object.assign(input, { type: "range", id, min: sl.min, max: sl.max, step: sl.step, value: state[sl.key] });
      input.dir = "ltr";
      const out = document.createElement("output");
      out.htmlFor = id;
      outputs[sl.key] = out;
      input.addEventListener("input", () => { state[sl.key] = Number(input.value); draw(); });
      inputs.push([sl.key, input]);
      label.append(input, out);
      controls.append(label);
    });
    const reset = document.createElement("button");
    reset.type = "button";
    reset.className = "md-button ex-reset";
    reset.textContent = "חזרה לערכים של השאלה";
    reset.addEventListener("click", () => {
      Object.assign(state, defaults);
      inputs.forEach(([key, input]) => { input.value = state[key]; });
      draw();
    });
    controls.append(reset);
    const summary = document.createElement("p");
    summary.className = "ex-summary";
    summary.setAttribute("aria-live", "polite");
    const charts = document.createElement("div");
    box.append(controls, summary, charts);

    const draw = () => {
      Object.entries(outputs).forEach(([key, out]) => { out.textContent = String(state[key]); });
      const res = view.draw(state);
      summary.innerHTML = res.summary;          // built from numbers only
      charts.innerHTML = res.charts.map(([title, svg]) => `<p class="ex-title">${title}</p>${svg}`).join("");
    };
    draw();
  };

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".explorer").forEach(setup);
  });
})();
