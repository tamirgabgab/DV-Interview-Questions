// kinds: mtbf metamc
//   mtbf                   0037        clock and data rates, tau, T0 and overhead: the MTBF of one to three flops
//   metamc                 0037        part a by Monte Carlo: data edges folded onto one clock period with the T0 window, the settling times of those inside it against the exponential, and the t_res cut that each flop moves by T_clk
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { f, fmt, ltr, seedControls } = dvqExplorers.lib;
  // a number in scientific notation with a real superscript: 4.14·10<sup>-8</sup>
  const sci10 = (v) => { const [m, e] = Number(v).toExponential(2).split("e"); return `${m}·10<sup>${Number(e)}</sup>`; };
  const NB = "\u00a0";

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
      if (s >= u) { const v = s / u; return `${v < 1e6 ? Number(v.toPrecision(3)) : sci10(v)} ${name}`; }
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
          return `<tr><td>${n}</td><td>${tRes > 0 ? fmt(tRes, 2) : "—"} ns</td><td>${tRes > 0 ? sci10(Math.exp(tRes / (st.tau / 1000))) : "—"}</td><td>${mtbfHuman(v)}</td></tr>`;
        }).join("");
        $(".ex-summary").innerHTML = `מחזור של ${ltr(`${fmt(T, 2)} ns`)}; כניסות ל-metastability בשנייה : ${ltr(`T0 · f_clk · f_data = ${sci10(st.t0 * 1e-12 * st.fclk * 1e6 * st.fdata * 1e6)}`)}; כל פלופ נוסף מכפיל את ה-MTBF ב-${ltr(`e<sup>T/τ</sup> = ${sci10(Math.exp(T / (st.tau / 1000)))}`)}.`;
        $(".mtbf-table").innerHTML = `<table class="pcie-table" dir="ltr"><thead><tr><th>פלופים</th><th>t_res</th><th>e<sup>t_res/τ</sup></th><th>MTBF</th></tr></thead><tbody>${rows}</tbody></table>`;
        $(".mtbf-chart").innerHTML = `<p class="ex-title">MTBF כפונקציה של תדר השעון, לפלופ אחד (כתום), שניים (כחול) ושלושה (ירוק); הנקודות הן התדר הנבחר</p>${chart()}`;

      };
      SL.forEach(([k]) => $(`.ex-${k}`).addEventListener("input", () => { st[k] = Number($(`.ex-${k}`).value); draw(); }));
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, defaults); SL.forEach(([k]) => { $(`.ex-${k}`).value = st[k]; }); draw(); });
      draw();
    },
  });

  // Part a by Monte Carlo (times in ps): every data edge lands at a uniform phase around
  // the nearest clock edge, in [−T/2, T/2); inside the window |phase| < T0 / 2 the flop
  // goes metastable and settles after an exponential time with mean tau. The two factors
  // of the formula: the share of edges inside the window, T0 / T = T0 f_clk, and the share
  // of those still unsettled after t_res = N T − overhead, exp(−t_res / tau).
  const metaDraw = (count, T, t0, tau, rnd) => {
    const phases = [], meta = [], settle = [];
    for (let i = 0; i < count; i++) {
      const ph = (rnd() - 0.5) * T;
      phases.push(ph);
      if (Math.abs(ph) < t0 / 2) { meta.push(i); settle.push(-tau * Math.log(1 - rnd())); }
    }
    return { phases, meta, settle };
  };
  const metaFactors = (fClkMHz, fDataMHz, tauPs, t0Ps, overheadNs, flops) => {
    const T = 1e6 / fClkMHz, tRes = flops * T - overheadNs * 1000;
    const pEnter = t0Ps / T, enterPerSec = pEnter * fDataMHz * 1e6, pStay = tRes > 0 ? Math.exp(-tRes / tauPs) : 1;
    return { T, tRes, pEnter, enterPerSec, pStay, mtbf: tRes > 0 ? 1 / (enterPerSec * pStay) : 0 };
  };

  // The Monte Carlo box (0037 part a): tau, T0 and the number of flops, the page's clock,
  // data rate and overhead; 100 or 1,000 seeded data edges folded onto one clock period
  // with the window shaded, a histogram of the settling times of the edges inside it
  // against the exponential, the cut at t_res (one T_clk further per flop) with the edges
  // beyond it, and the two factors measured against the formula.
  const FCLK = 500, FDATA = 50, OVER = 0.3;
  const metamcView = () => ({
    mount(box) {
      const D = { tau: Number(box.dataset.tau || 100), t0: Number(box.dataset.t0 || 50), flops: Number(box.dataset.flops || 1) };
      const st = { ...D, count: 1000, seed: null, rnd: null, draw: null };
      box.innerHTML =
        `<div class="ex-controls"><label><span>‏τ (ps)</span><input type="range" class="mc-tau" min="10" max="300" step="5" value="${D.tau}" dir="ltr"><output class="mc-out-tau"></output></label>` +
        `<label><span>‏T0 (ps)</span><input type="range" class="mc-t0" min="10" max="300" step="5" value="${D.t0}" dir="ltr"><output class="mc-out-t0"></output></label>` +
        `<label>פלופים <select class="mc-flops" aria-label="מספר הפלופים בסנכרן">${[1, 2, 3].map((v) => `<option value="${v}">${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button md-button--primary mc-100">${ltr("100")} קצוות</button>` +
        `<button type="button" class="md-button md-button--primary mc-1000">${ltr("1,000")} קצוות</button></div>` +
        `<p class="ex-title mc-t1"></p><div class="mc-phase"></div>` +
        `<p class="ex-title mc-t2"></p><div class="mc-hist"></div>` +
        `<span class="viz-legend"><span><i class="mc-key-in"></i>נפל בחלון, metastable</span><span><i class="mc-key-out"></i>נפל מחוץ לחלון</span><span><i class="ink"></i>הצפוי לפי ${ltr("e<sup>−t/τ</sup>")}</span><span><i class="mc-key-cut"></i>מעבר ל-${ltr("t_res")} : כשל</span></span>` +
        `<div class="mc-table"></div><p class="ex-summary mc-sum" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const hash = (i) => ((i * 0.6180339887) % 1);
      const phaseSvg = (T, d) => {
        const W = 640, H = 120, X0 = 20, X1 = 620, Y0 = 14, Y1 = 92, X = (ph) => X0 + ((ph + T / 2) / T) * (X1 - X0);
        const half = Math.max(1.5, (X(st.t0 / 2) - X(-st.t0 / 2)) / 2);
        let s = `<svg class="perf-chart mc-phasesvg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${d.phases.length} קצוות של הנתונים סביב שפת השעון, ${d.meta.length} מהם בחלון">`;
        s += `<rect class="mc-window" x="${f(X(0) - half)}" y="${Y0}" width="${f(2 * half)}" height="${Y1 - Y0}"/>`;
        const inside = new Set(d.meta);
        d.phases.forEach((ph, i) => { s += `<circle class="${inside.has(i) ? "mc-in" : "mc-out"}" cx="${f(X(ph))}" cy="${f(Y0 + 4 + hash(i + 1) * (Y1 - Y0 - 8))}" r="${inside.has(i) ? 3.2 : 2}"/>`; });
        s += `<line class="mc-clk" x1="${f(X(0))}" x2="${f(X(0))}" y1="${Y0 - 6}" y2="${Y1 + 4}"/>`;
        s += `<line class="axis" x1="${X0}" x2="${X1}" y1="${Y1 + 4}" y2="${Y1 + 4}"/>`;
        [[-T / 2, `−${fmt(T / 2000, 1)} ns`], [0, "שפת השעון"], [T / 2, `+${fmt(T / 2000, 1)} ns`]].forEach(([ph, lab], k) => {
          s += `<text class="tick" x="${f(X(ph))}" y="${Y1 + 20}" text-anchor="${k === 0 ? "start" : k === 2 ? "end" : "middle"}"${k === 1 ? ' direction="rtl"' : ""}>${lab}</text>`;
        });
        return s + "</svg>";
      };
      const histSvg = (d, r) => {
        const W = 640, H = 240, X0 = 44, X1 = 620, Y0 = 16, Y1 = 200, tRes = r.tRes;
        const xmax = Math.max(tRes * 1.08, 6 * st.tau), B = 40, bw = xmax / B, k = d.settle.length;
        const counts = new Array(B).fill(0);
        d.settle.forEach((t) => { if (t < xmax) counts[Math.floor(t / bw)]++; });
        const expect = Array.from({ length: B }, (_, b) => k * (Math.exp(-(b * bw) / st.tau) - Math.exp(-((b + 1) * bw) / st.tau)));
        const top = Math.max(1, ...counts, ...expect) * 1.1, X = (t) => X0 + (t / xmax) * (X1 - X0), Y = (v) => Y1 - (v / top) * (Y1 - Y0);
        let s = `<svg class="perf-chart mc-histsvg" viewBox="0 0 ${W} ${H}" role="img" aria-label="היסטוגרמה של זמני ההתייצבות של ${k} הקצוות שנפלו בחלון, והחתך t_res">`;
        const step = top > 40 ? 10 : top > 16 ? 5 : top > 6 ? 2 : 1;
        for (let v = 0; v <= top; v += step) s += `<line class="grid" x1="${X0}" x2="${X1}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 6}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        if (tRes < xmax) s += `<rect class="mc-fail" x="${f(X(tRes))}" y="${Y0}" width="${f(X1 - X(tRes))}" height="${Y1 - Y0}"/>`;
        counts.forEach((c, b) => { if (c) s += `<rect class="bar by-multiples" x="${f(X(b * bw) + 0.5)}" y="${f(Y(c))}" width="${f(Math.max(1, X(bw) - X0 - 1))}" height="${f(Y1 - Y(c))}"><title>${fmt(b * bw / 1000, 2)}–${fmt((b + 1) * bw / 1000, 2)} ns : ${c}</title></rect>`; });
        s += `<polyline class="ink-line" fill="none" stroke-width="1.8" points="${expect.map((v, b) => `${f(X((b + 0.5) * bw))},${f(Y(v))}`).join(" ")}"/>`;
        // the edges that did not settle by t_res, as marks on the axis
        d.settle.forEach((t) => { if (t >= tRes) s += `<circle class="mc-failed" cx="${f(X(Math.min(t, xmax)))}" cy="${Y1}" r="5"><title>${fmt(t / 1000, 2)} ns, אחרי t_res</title></circle>`; });
        s += `<line class="mc-cut" x1="${f(X(Math.min(tRes, xmax)))}" x2="${f(X(Math.min(tRes, xmax)))}" y1="${Y0 - 4}" y2="${Y1}"/><text class="legend halo" x="${f(X(Math.min(tRes, xmax)) - 5)}" y="${Y0 + 10}" text-anchor="end">t_res = ${fmt(tRes / 1000, 2)} ns</text>`;
        for (let b = 0; b <= 4; b++) { const t = (b * xmax) / 4; s += `<text class="tick" x="${f(X(t))}" y="${Y1 + 18}" text-anchor="${b === 4 ? "end" : "middle"}">${fmt(t / 1000, 2)} ns</text>`; }
        return s + `<line class="axis" x1="${X0}" x2="${X1}" y1="${Y1}" y2="${Y1}"/></svg>`;
      };
      const sci = (v) => (v >= 0.01 && v < 1e4 ? Number(v.toPrecision(3)).toLocaleString("en-US") : sci10(v));
      const draw = () => {
        const r = metaFactors(FCLK, FDATA, st.tau, st.t0, OVER, st.flops), d = st.draw, n = d.phases.length, k = d.settle.length;
        const late = d.settle.filter((t) => t >= r.tRes).length;
        $(".mc-tau").value = st.tau; $(".mc-out-tau").textContent = String(st.tau);
        $(".mc-t0").value = st.t0; $(".mc-out-t0").textContent = String(st.t0); $(".mc-flops").value = String(st.flops);
        $(".mc-t1").innerHTML = `הגרלה של ${ltr(n.toLocaleString("en-US"))} קצוות של הנתונים, כל אחד במקום שלו ביחס לשפת השעון הקרובה (מחזור של ${ltr(`${fmt(r.T / 1000, 1)} ns`)}), ובאמצע החלון של ${ltr(`T0 = ${st.t0} ps`)}`;
        $(".mc-phase").innerHTML = phaseSvg(r.T, d);
        $(".mc-t2").innerHTML = `כמה זמן לקח ל-${ltr(k)} הקצוות שבחלון להתייצב, מול ${ltr(`t_res = ${st.flops} · ${fmt(r.T / 1000, 1)} − ${OVER} = ${fmt(r.tRes / 1000, 2)} ns`)}`;
        $(".mc-hist").innerHTML = histSvg(d, r);
        $(".mc-table").innerHTML = `<table class="bridge-table mc-factors"><thead><tr><th>הגורם</th><th>בהגרלה</th><th>בנוסחה</th></tr></thead><tbody>` +
          `<tr><td>חלק הקצוות שנופלים בחלון</td><td>${ltr(`${k}/${n} = ${fmt(k / n, 4)}`)}</td><td>${ltr(`T0 · f_clk = ${fmt(r.pEnter, 4)}`)}</td></tr>` +
          `<tr><td>מהם, חלק שלא התייצב עד ${ltr("t_res")}</td><td>${ltr(k ? `${late}/${k}` : "—")}</td><td>${ltr(`e<sup>−t_res/τ</sup> = ${sci(r.pStay)}`)}</td></tr>` +
          `<tr><td>כניסות ל-metastability בשנייה</td><td>${ltr(sci((k / n) * FDATA * 1e6))}</td><td>${ltr(`T0 · f_clk · f_data = ${sci(r.enterPerSec)}`)}</td></tr></tbody></table>`;
        $(".mc-sum").innerHTML = `ה-MTBF הוא ההופכי של המכפלה${NB}: ${ltr(`1 / (${sci(r.enterPerSec)} · ${sci(r.pStay)})`)}, כלומר ${mtbfHuman(r.mtbf)}. ` +
          (late ? `בהגרלה הזו ${ltr(late)} ${late === 1 ? "קצה לא התייצב" : "קצוות לא התייצבו"} בזמן, והם הכשלים.` : `אף קצה בהגרלה לא עבר את החתך, כי הזנב המעריכי דועך מהר.`) +
          ` כל פלופ נוסף מזיז את החתך ב-${ltr(`T_clk = ${fmt(r.T / 1000, 1)} ns`)} ימינה, ומכפיל את ה-MTBF ב-${ltr(`e<sup>T_clk/τ</sup> = ${sci(Math.exp(r.T / st.tau))}`)}.`;
      };
      const redraw = () => { st.draw = metaDraw(st.count, 1e6 / FCLK, st.t0, st.tau, st.rnd()); draw(); };
      // a seeded draw: the phases and the settling times both come from one generator, so a
      // seed replays the same edges (a slider redraws from the same seed)
      const seed = seedControls(box, $(".mc-1000"), (rng, sd) => { st.seed = sd; st.rnd = () => dvqExplorers.lib.mulberry32(sd); redraw(); }, { fresh: false });
      $(".mc-100").addEventListener("click", () => { st.count = 100; seed.draw(); });
      $(".mc-1000").addEventListener("click", () => { st.count = 1000; seed.draw(); });
      ["tau", "t0"].forEach((k) => $(`.mc-${k}`).addEventListener("input", () => { st[k] = Number($(`.mc-${k}`).value); redraw(); }));
      $(".mc-flops").addEventListener("change", () => { st.flops = Number($(".mc-flops").value); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, D, { count: 1000 }); box.dvqSeed.runSeed(Number(box.dataset.seed || 3)); });
      if (!st.draw) box.dvqSeed.runSeed(Number(box.dataset.seed || 3));
    },
  });

  dvqExplorers.register({
    views: { mtbf: mtbfView, metamc: metamcView },
    help: {
      mtbf: "תדר השעון והנתונים, tau, T0 ו-overhead : התיבה מחשבת את ה-MTBF של פלופ אחד עד שלושה ביחידות קריאות, ומציירת אותו כנגד תדר השעון.",
      metamc: "״100 קצוות״ ו״1,000 קצוות״ מגרילים קצוות של הנתונים : למעלה כל קצה במקומו ביחס לשפת השעון, ומי שנפל בחלון T0 נכנס ל-metastability. למטה זמני ההתייצבות שלהם מול הזנב המעריכי, והחתך t_res, שכל פלופ מזיז ב-T_clk. ‏τ ו-T0 בסליידרים.",
    },
    models: { mtbfSeconds, mtbfHuman, metaDraw, metaFactors },
  });
})();
