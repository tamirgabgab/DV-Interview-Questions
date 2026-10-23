// kinds: mtbf
//   mtbf                   0037        clock and data rates, tau, T0 and overhead: the MTBF of one to three flops
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { f, fmt, ltr } = dvqExplorers.lib;

  // Synchronizer MTBF (0037): exp(t_res / tau) / (T0 f_clk f_data) with
  // t_res = N T_clk - overhead; frequencies in MHz, tau and T0 in ps, overhead in ns.
  const YEAR = 365.25 * 86400;
  const mtbfSeconds = (fClkMHz, fDataMHz, tauPs, t0Ps, overheadNs, flops) => {
    const fClk = fClkMHz * 1e6, tRes = flops / fClk - overheadNs * 1e-9;
    if (tRes <= 0) return 0;
    return Math.exp(tRes / (tauPs * 1e-12)) / (t0Ps * 1e-12 * fClk * fDataMHz * 1e6);
  };
  const mtbfHuman = (s) => {
    if (s <= 0) return "0";
    const units = [["שנים", YEAR], ["ימים", 86400], ["שעות", 3600], ["דקות", 60], ["שניות", 1], ["ms", 1e-3], ["µs", 1e-6]];
    for (const [name, u] of units) {
      if (s >= u) { const v = s / u; return `${v < 1e6 ? Number(v.toPrecision(3)) : v.toExponential(2).replace("e+", "·10^")} ${name}`; }
    }
    return `${s.toExponential(2)} s`;
  };

  // The MTBF box (0037): the parameters as sliders, the MTBF of one to three flops in
  // readable units, and the chart against the clock frequency with the chosen point.
  const mtbfView = () => ({
    mount(box) {
      const defaults = { fclk: Number(box.dataset.fclk || 500), fdata: Number(box.dataset.fdata || 50), tau: Number(box.dataset.tau || 100), t0: Number(box.dataset.t0 || 50), overhead: Number(box.dataset.overhead || 0.3) };
      const st = { ...defaults };
      const SL = [["fclk", "תדר השעון (MHz)", 100, 2000, 50], ["fdata", "קצב המעברים של האות (MHz)", 1, 500, 1], ["tau", "τ (ps)", 10, 300, 5], ["t0", "T0 (ps)", 10, 300, 5], ["overhead", "setup + clock-to-q (ns)", 0.1, 1.0, 0.05]];
      box.innerHTML =
        `<div class="ex-controls">` +
        SL.map(([k, label, min, max, step]) => `<label><span>${label}</span><input type="range" class="ex-${k}" min="${min}" max="${max}" step="${step}" value="${st[k]}" dir="ltr"><output class="out-${k}" dir="ltr"></output></label>`).join("") +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p><div class="mtbf-table"></div><div class="mtbf-chart"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const chart = () => {
        const w = 640, h = 280, x0 = 56, right = 16, top = 16, base = 240, xMin = 100, xMax = 2000, eMin = -6, eMax = 24;
        const X = (f) => x0 + ((f - xMin) / (xMax - xMin)) * (w - x0 - right);
        const Y = (v) => { const e = Math.min(eMax, Math.max(eMin, Math.log10(Math.max(v, 1e-300)))); return base - ((e - eMin) / (eMax - eMin)) * (base - top); };
        let s = `<svg class="perf-chart mtbf-live" viewBox="0 0 ${w} ${h}" role="img" aria-label="MTBF בשניות, בסקאלה לוגריתמית, כפונקציה של תדר השעון">`;
        for (let e = eMin; e <= eMax; e += 6) s += `<line class="grid" x1="${x0}" x2="${w - right}" y1="${f(Y(10 ** e))}" y2="${f(Y(10 ** e))}"/><text class="tick" x="${x0 - 8}" y="${f(Y(10 ** e) + 4)}" text-anchor="end">10<tspan dy="-6" font-size="9">${e}</tspan></text>`;
        for (let v = 200; v <= xMax; v += 300) s += `<line class="grid" x1="${f(X(v))}" x2="${f(X(v))}" y1="${top - 6}" y2="${base}" stroke-dasharray="4 4"/><text class="tick" x="${f(X(v))}" y="${base + 18}" text-anchor="middle">${v} MHz</text>`;
        [[YEAR, "שנה"], [1000 * YEAR, "אלף שנים"]].forEach(([v, label]) => {
          s += `<line class="ink-line" x1="${x0}" x2="${w - right}" y1="${f(Y(v))}" y2="${f(Y(v))}" stroke-width="1" stroke-dasharray="6 4"/><text class="legend" x="${w - right - 4}" y="${f(Y(v) - 5)}" text-anchor="start" direction="rtl">${label}</text>`;
        });
        [[1, "s2"], [2, "s1"], [3, "s3"]].forEach(([n, cls]) => {
          const pts = [];
          for (let fm = xMin; fm <= xMax; fm += 10) { const v = mtbfSeconds(fm, st.fdata, st.tau, st.t0, st.overhead, n); if (v > 0 && v <= 10 ** eMax) pts.push(`${f(X(fm))},${f(Y(v))}`); }
          s += `<polyline class="${cls}-line" points="${pts.join(" ")}" fill="none" stroke-width="2"/>`;
          const v = mtbfSeconds(st.fclk, st.fdata, st.tau, st.t0, st.overhead, n);
          if (v > 0) s += `<circle class="${cls}-dot" cx="${f(X(st.fclk))}" cy="${f(Y(v))}" r="5"><title>${n} flops at ${st.fclk} MHz: ${mtbfHuman(v)}</title></circle>`;
        });
        return s + `<line class="axis" x1="${x0}" x2="${w - right}" y1="${base}" y2="${base}"/></svg>`;
      };
      const draw = () => {
        SL.forEach(([k]) => { $(`.out-${k}`).textContent = String(st[k]); });
        const T = 1000 / st.fclk;
        const rows = [1, 2, 3].map((n) => {
          const tRes = n * T - st.overhead, v = mtbfSeconds(st.fclk, st.fdata, st.tau, st.t0, st.overhead, n);
          return `<tr><td>${n}</td><td>${tRes > 0 ? fmt(tRes, 2) : "—"} ns</td><td>${tRes > 0 ? Math.exp(tRes / (st.tau / 1000)).toExponential(2).replace("e+", "·10^") : "—"}</td><td>${mtbfHuman(v)}</td></tr>`;
        }).join("");
        $(".ex-summary").innerHTML = `מחזור של ${ltr(`${fmt(T, 2)} ns`)}; כניסות ל-metastability בשנייה : ${ltr(`T0 · f_clk · f_data = ${(st.t0 * 1e-12 * st.fclk * 1e6 * st.fdata * 1e6).toExponential(2).replace("e+", "·10^")}`)}; כל פלופ נוסף מכפיל את ה-MTBF ב-${ltr(`e^(T/τ) = ${Math.exp(T / (st.tau / 1000)).toExponential(2).replace("e+", "·10^")}`)}.`;
        $(".mtbf-table").innerHTML = `<table class="pcie-table" dir="ltr"><thead><tr><th>פלופים</th><th>t_res</th><th>e^(t_res/τ)</th><th>MTBF</th></tr></thead><tbody>${rows}</tbody></table>`;
        $(".mtbf-chart").innerHTML = `<p class="ex-title">MTBF כפונקציה של תדר השעון, לפלופ אחד (כתום), שניים (כחול) ושלושה (ירוק); הנקודות הן התדר הנבחר</p>${chart()}`;

      };
      SL.forEach(([k]) => $(`.ex-${k}`).addEventListener("input", () => { st[k] = Number($(`.ex-${k}`).value); draw(); }));
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, defaults); SL.forEach(([k]) => { $(`.ex-${k}`).value = st[k]; }); draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { mtbf: mtbfView },
    help: {
      mtbf: "תדר השעון והנתונים, tau, T0 ו-overhead : התיבה מחשבת את ה-MTBF של פלופ אחד עד שלושה ביחידות קריאות, ומציירת אותו כנגד תדר השעון.",
    },
    models: { mtbfSeconds, mtbfHuman },
  });
})();
