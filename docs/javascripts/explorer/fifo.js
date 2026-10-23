// kinds: fifo
//   fifo                   0033        burst, write and read rates, a skipping reader: the fill level over time; a wr / rd timing strip on a real time axis over a sliding window
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { H, W, attr, f, fmt, ltr, stickyNames, waveDromText } = dvqExplorers.lib;

  // FIFO depth (0033): a burst of `burst` words written every t_write steps, read every
  // t_read steps from step t_read on, the reader skipping one read slot in idle_every.
  // fifoDepth is the closed form ceil(B (1 - f_r duty / f_w)), fifoFill the cycle simulation
  // with the fill measured after the write and before the read of the same step; fifoSteps
  // turns a frequency in MHz into a period in steps of 0.05 ns, like the page.
  const fifoSteps = (fMHz) => Math.round(1000 / fMHz / 0.05);
  const fifoDepth = (burst, fWrite, fRead, duty = 1) => {
    const rate = (fRead * duty) / fWrite;
    return rate >= 1 ? 1 : Math.ceil(burst * (1 - rate) - 1e-9);
  };
  const fifoFill = (burst, tWrite, tRead, idleEvery = 0) => {
    let count = 0, written = 0, slot = 0, t = 0, max = 0;
    const trace = [[0, 0]];
    while (written < burst || count > 0) {
      if (t % tWrite === 0 && written < burst) { count++; written++; trace.push([t, count]); }
      if (count > max) max = count;
      if (t > 0 && t % tRead === 0) {
        slot++;
        if (!(idleEvery && slot % idleEvery === 0) && count > 0) { count--; trace.push([t, count]); }
      }
      t++;
      if (t > 5e6) break;
    }
    return { max, trace };
  };
  // WaveDrom draws a lane with an integer `period` only, so the export puts the two clocks
  // on a common grid: a write cycle of a units and a read cycle of b. Exact when the ratio
  // of the periods reduces to a, b <= 8; otherwise the closest ratio with a <= 6.
  const fifoGrid = (tWrite, tRead) => {
    const gcd = (x, y) => (y ? gcd(y, x % y) : x), g = gcd(tWrite, tRead);
    if (tWrite / g <= 8 && tRead / g <= 8) return { a: tWrite / g, b: tRead / g, exact: true };
    let best = null;
    for (let a = 1; a <= 6; a++) {
      const b = Math.max(1, Math.round((a * tRead) / tWrite)), err = Math.abs(b / a - tRead / tWrite);
      if (!best || err < best.err - 1e-12) best = { a, b, err };
    }
    return { a: best.a, b: best.b, exact: best.err < 1e-12 };
  };
  // The same simulation as fifoFill, keeping the events for the timing strip: the time of
  // every write, every read slot (its time, whether the reader skips it, whether a word
  // was read), the fill trace and the end time.
  const fifoEvents = (burst, tWrite, tRead, idleEvery = 0) => {
    let count = 0, written = 0, slot = 0, t = 0, max = 0;
    const trace = [[0, 0]], writes = [], slots = [];
    while (written < burst || count > 0) {
      if (t % tWrite === 0 && written < burst) { count++; written++; writes.push(t); trace.push([t, count]); }
      if (count > max) max = count;
      if (t > 0 && t % tRead === 0) {
        slot++;
        const idle = !!(idleEvery && slot % idleEvery === 0), read = !idle && count > 0;
        if (read) { count--; trace.push([t, count]); }
        slots.push({ t, idle, read });
      }
      t++;
      if (t > 5e6) break;
    }
    return { max, trace, writes, slots, end: t - 1 };
  };

  // The FIFO box (0033): burst, write and read rates and the reader's idle slot; the fill
  // level over time from the cycle simulation, the formula beside it; a timing strip of
  // the two clocks, the transfers and the count on a real time axis, over a window of 40
  // write cycles that a slider moves (marked on the chart).
  const fifoView = () => ({
    mount(box) {
      const defaults = { burst: Number(box.dataset.burst || 120), fw: Number(box.dataset.fw || 100), fr: Number(box.dataset.fr || 80), idle: Number(box.dataset.idle || 0) };
      const st = { ...defaults };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>גודל הפרץ B (מילים)</span><input type="range" class="ex-burst" min="4" max="512" step="4" value="${st.burst}" dir="ltr"><output class="out-burst"></output></label>` +
        `<label><span>קצב הכתיבה (MHz)</span><input type="range" class="ex-fw" min="10" max="400" step="5" value="${st.fw}" dir="ltr"><output class="out-fw"></output></label>` +
        `<label><span>קצב הקריאה (MHz)</span><input type="range" class="ex-fr" min="10" max="400" step="5" value="${st.fr}" dir="ltr"><output class="out-fr"></output></label>` +
        `<label>הקורא מדלג על <select class="ex-idle"><option value="0">כלום</option>${[2, 3, 4, 5, 8, 16].map((k) => `<option value="${k}"${k === st.idle ? " selected" : ""}>משבצת אחת מכל ${k}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<div class="ex-controls"><label class="fifo-winlab"><span>החלון ברצועה</span><input type="range" class="ex-win" min="0" max="0" step="1" value="0" dir="ltr" aria-label="תחילת החלון, במחזורי כתיבה"></label><span class="fifo-wintext"></span></div>` +
        `<div class="wv-wrap fifo-strip" tabindex="0" role="group" aria-label="רצועת תזמון של הכתיבות והקריאות, גלילה אופקית"></div>` +
        `<div class="fifo-chart"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const WIN = 40, CW = 16, L = 66;             // write cycles in the window, px per write cycle
      let win = 0;
      // the window [ws, we): one write cycle before the burst, then WIN write cycles
      const range = (tW) => { const ws = (win - 1) * tW; return [ws, ws + WIN * tW]; };
      // a timing strip on a real time axis: both clocks at their own period, the enables
      // high in the cycle that ends with the transfer (skipped read slots shaded), and
      // the fill count as a bus; its WaveDrom counts in write cycles, the read lanes with
      // period tRead / tWrite and the count sampled at the write clock
      const strip = (ev, tW, tR) => {
        const [ws, we] = range(tW), RH = 30, T = 20, rows = ["wr_clk", "wr_en", "rd_clk", "rd_en", "count"];
        const W = L + WIN * CW + 6, H = T + rows.length * RH + 4, X = (t) => L + ((t - ws) / tW) * CW;
        const clip = (a, b) => [Math.max(a, ws), Math.min(b, we)];
        let s = "";
        const yTop = (r) => T + r * RH + 5, yBot = (r) => T + r * RH + RH - 7;
        for (let k = 0; k <= WIN; k++) {
          const t = ws + k * tW;
          s += `<line class="wv-grid" x1="${f(X(t))}" x2="${f(X(t))}" y1="${T - 4}" y2="${H - 4}"/>`;
          if (k % 5 === 0) s += `<text class="wv-tick" x="${f(X(t))}" y="${T - 8}" text-anchor="${k === WIN ? "end" : k === 0 ? "start" : "middle"}">${f(t * 0.05, 0)}</text>`;
        }
        s += `<text class="wv-name" x="${L - 8}" y="${T - 8}" text-anchor="end">ns</text>`;
        rows.forEach((n, r) => { s += `<text class="wv-name" x="${L - 8}" y="${T + r * RH + RH / 2 + 2}" text-anchor="end">${n}</text>`; });
        const clock = (r, period, cls) => {
          let d = "";
          for (let e = Math.floor(ws / period) * period; e < we; e += period) {
            const [a, b] = clip(e, e + period / 2), [c, g] = clip(e + period / 2, e + period);
            if (b > a) d += `M${f(X(a))},${yTop(r)} H${f(X(b))} `;
            if (g > c) d += `M${f(X(c))},${yBot(r)} H${f(X(g))} `;
            if (e >= ws) d += `M${f(X(e))},${yBot(r)} V${yTop(r)} `;
            if (e + period / 2 >= ws && e + period / 2 < we) d += `M${f(X(e + period / 2))},${yTop(r)} V${yBot(r)} `;
          }
          return `<path class="wv-line wv-clock${cls}" d="${d}"/>`;
        };
        // a level that is high over [t − period, t) for every transfer time t
        const enable = (r, times, period, cls) => {
          let hi = "", d;
          const spans = [];                                // back-to-back transfers merge into one high level
          times.forEach((t) => {
            const [a, b] = clip(t - period, t);
            if (b <= a) return;
            const last = spans[spans.length - 1];
            if (last && last[1] === a) last[1] = b; else spans.push([a, b]);
          });
          let at = ws;
          d = "";
          spans.forEach(([a, b]) => {
            hi += `<rect class="wv-high${cls}" x="${f(X(a))}" y="${yTop(r)}" width="${f(X(b) - X(a))}" height="${yBot(r) - yTop(r)}"/>`;
            d += `M${f(X(at))},${yBot(r)} H${f(X(a))} V${yTop(r)} H${f(X(b))} V${yBot(r)} `;
            at = b;
          });
          d += `M${f(X(at))},${yBot(r)} H${f(X(we))}`;
          return hi + `<path class="wv-line${cls}" d="${d}"/>`;
        };
        s += clock(0, tW, "") + enable(1, ev.writes, tW, " wv-s1") + clock(2, tR, "");
        ev.slots.filter((sl) => sl.idle).forEach((sl) => {
          const [a, b] = clip(sl.t - tR, sl.t);
          if (b > a) s += `<rect class="wv-mark" x="${f(X(a))}" y="${T + 3 * RH + 2}" width="${f(X(b) - X(a))}" height="${RH - 4}"><title>הקורא מדלג על המשבצת הזאת</title></rect>`;
        });
        s += enable(3, ev.slots.filter((sl) => sl.read).map((sl) => sl.t), tR, " wv-s3");
        // the count as a bus: one segment per value inside the window
        const y0 = T + 4 * RH, ym = y0 + RH / 2 - 1, yh = y0 + 5, yl = y0 + RH - 7;
        const seg = [];
        ev.trace.forEach(([t, v], i) => { const next = i + 1 < ev.trace.length ? ev.trace[i + 1][0] : ev.end + 1; seg.push([t, next, v]); });
        const merged = [];
        seg.forEach(([a, b, v]) => { const [ca, cb] = clip(a, b); if (cb <= ca) return; const last = merged[merged.length - 1]; if (last && last[2] === v && last[1] === ca) last[1] = cb; else merged.push([ca, cb, v]); });
        if (ws < 0 && merged.length) merged[0][0] = Math.max(ws, merged[0][0] === 0 ? ws : merged[0][0]);
        merged.forEach(([a, b, v]) => {
          const xa = X(a), w = X(b) - xa;
          if (w < 1) return;
          const e = Math.min(4, w / 2);
          s += `<path class="wv-bus" d="M${f(xa + 0.5)},${ym} L${f(xa + e)},${yh} H${f(xa + w - e)} L${f(xa + w - 0.5)},${ym} L${f(xa + w - e)},${yl} H${f(xa + e)} Z"><title>מילוי ${v}</title></path>`;
          if (w >= 8 * String(v).length + 12) s += `<text class="wv-val" x="${f(xa + w / 2)}" y="${ym + 4}" text-anchor="middle">${v}</text>`;
        });
        // WaveDrom on the integer grid: a write cycle is a units, a read cycle b units; the
        // count is sampled once per unit
        const { a, b, exact } = fifoGrid(tW, tR), u = tW / a, units = WIN * a;
        const e0 = Math.floor(ws / tR) * tR, nR = Math.ceil((we - e0) / tR), phase = Math.round((ws - e0) / (tR / b));
        const lvl = (chars) => chars.map((c, i) => (i && c === chars[i - 1] ? "." : c)).join("");
        const writeAt = new Set(ev.writes), readAt = new Set(ev.slots.filter((sl) => sl.read).map((sl) => sl.t));
        const wrEn = Array.from({ length: WIN }, (_, k) => (writeAt.has(ws + (k + 1) * tW) ? "1" : "0"));
        const rdEn = Array.from({ length: nR }, (_, j) => (readAt.has(e0 + (j + 1) * tR) ? "1" : "0"));
        const countAt = (t) => { let v = 0; for (const [tt, c] of ev.trace) { if (tt <= t) v = c; else break; } return v; };
        const cv = Array.from({ length: units }, (_, k) => countAt(ws + k * u));
        const wd = { signal: [
          { name: "wr_clk", wave: "p" + ".".repeat(WIN - 1), period: a },
          { name: "wr_en", wave: lvl(wrEn), period: a },
          { name: exact ? "rd_clk" : `rd_clk (≈ ${b}/${a})`, wave: "p" + ".".repeat(nR - 1), period: b, phase },
          { name: "rd_en", wave: lvl(rdEn), period: b, phase },
          { name: "count", wave: cv.map((v, k) => (k && v === cv[k - 1] ? "." : "=")).join(""), data: cv.filter((v, k) => !k || v !== cv[k - 1]).map(String) },
        ], head: { text: `t = ${f(ws * 0.05, 1)} .. ${f(we * 0.05, 1)} ns` } };
        wd.signal.forEach((l) => { if (l.period === 1) delete l.period; if (l.phase === 0) delete l.phase; });
        return stickyNames(`<svg class="wave-strip fifo-wave" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="רצועת תזמון : שני השעונים, הכתיבות, הקריאות ומילוי ה-FIFO" data-wavedrom="${attr(waveDromText(wd))}">${s}</svg>`, rows, L, T, RH);
      };
      const chart = (trace, tEnd, formula, yMax, tW) => {
        const w = 640, h = 240, x0 = 44, right = 16, top = 16, base = 204;
        const X = (t) => x0 + (t / tEnd) * (w - x0 - right), Y = (v) => base - (v / yMax) * (base - top);
        let s = `<svg class="perf-chart fifo-live" viewBox="0 0 ${w} ${h}" role="img" aria-label="רמת המילוי של ה-FIFO לאורך הזמן">`;
        const yStep = yMax <= 10 ? 2 : yMax <= 50 ? 10 : yMax <= 100 ? 20 : yMax <= 300 ? 50 : 100;
        for (let v = 0; v <= yMax; v += yStep) s += `<line class="grid" x1="${x0}" x2="${w - right}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${x0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        const ns = tEnd * 0.05, xStep = ns <= 500 ? 100 : ns <= 2000 ? 250 : ns <= 5000 ? 500 : ns <= 20000 ? 2000 : 5000;
        for (let v = 0; v <= ns; v += xStep) s += `<line class="grid" x1="${f(X(v / 0.05))}" x2="${f(X(v / 0.05))}" y1="${top - 6}" y2="${base}" stroke-dasharray="4 4"/><text class="tick" x="${f(X(v / 0.05))}" y="${base + 18}" text-anchor="middle">${v ? `${v} ns` : "0"}</text>`;
        const pts = [];
        trace.forEach(([t, v], i) => { if (i) pts.push(`${f(X(t))},${f(Y(trace[i - 1][1]))}`); pts.push(`${f(X(t))},${f(Y(v))}`); });
        const [ws, we] = range(tW);
        s += `<rect class="fifo-win" x="${f(X(Math.max(0, ws)))}" y="${top - 6}" width="${f(Math.max(2, X(Math.min(tEnd, we)) - X(Math.max(0, ws))))}" height="${base - top + 6}"><title>החלון שברצועה</title></rect>`;
        s += `<polyline class="s1-line" points="${pts.join(" ")}" fill="none" stroke-width="2"/>`;
        s += `<line class="ink-line" x1="${x0}" x2="${w - right}" y1="${f(Y(formula))}" y2="${f(Y(formula))}" stroke-width="1" stroke-dasharray="6 4"/>`;
        s += `<text class="legend" x="${w - right - 4}" y="${f(Y(formula) - 5)}" text-anchor="end">${formula}</text>`;
        return s + `<line class="axis" x1="${x0}" x2="${w - right}" y1="${base}" y2="${base}"/></svg>`;
      };
      const draw = () => {
        ["burst", "fw", "fr"].forEach((k) => { $(`.out-${k}`).textContent = String(st[k]); });
        const duty = st.idle ? 1 - 1 / st.idle : 1;
        const formula = fifoDepth(st.burst, st.fw, st.fr, duty);
        const tW = fifoSteps(st.fw), tR = fifoSteps(st.fr);
        const r = fifoEvents(st.burst, tW, tR, st.idle);
        const eff = st.fr * duty;
        const burstNs = (st.burst * 1000) / st.fw;
        $(".ex-summary").innerHTML =
          `פרץ של ${ltr(`B = ${st.burst}`)} מילים ב-${ltr(`${st.fw} MHz`)} נמשך ${ltr(`${fmt(burstNs, 0)} ns`)}; הקורא מוציא באותו זמן ` +
          `${ltr(`${fmt(burstNs * eff / 1000, 1)}`)} מילים (קצב אפקטיבי ${ltr(`${fmt(eff, 1)} MHz`)}). ` +
          `הנוסחה : <b>${ltr(String(formula))}</b>; המילוי המקסימלי בסימולציה : <b>${ltr(String(r.max))}</b>` +
          (r.max > formula ? ` (הפאזה בין השעונים מוסיפה ${r.max - formula}).` : ".") +
          (eff >= st.fw ? " הקורא לא איטי מהכותב, ולכן ה-FIFO כמעט לא מתמלא." : "");
        const tEnd = r.trace[r.trace.length - 1][0] || 1;
        const yMax = Math.max(5, Math.ceil(Math.max(r.max, formula) * 1.15 / 5) * 5);
        const cycles = Math.ceil(r.end / tW) + 2, maxWin = Math.max(0, cycles - WIN);
        win = Math.min(win, maxWin);
        const slider = $(".ex-win");
        slider.max = String(maxWin); slider.value = String(win); slider.disabled = maxWin === 0;
        const [ws, we] = range(tW);
        $(".fifo-wintext").innerHTML = `מחזורי כתיבה ${ltr(`${win} … ${win + WIN - 1}`)} מתוך ${ltr(cycles - 1)}, ${ltr(`${f(Math.max(0, ws) * 0.05, 0)}–${f(we * 0.05, 0)} ns`)}`;
        $(".fifo-strip").innerHTML = strip(r, tW, tR);
        $(".fifo-chart").innerHTML = `<p class="ex-title">רמת המילוי לאורך הזמן; הקו המקווקו הוא הנוסחה, והמלבן הוא החלון שברצועה</p>${chart(r.trace, tEnd, formula, yMax, tW)}`;

      };
      ["burst", "fw", "fr"].forEach((k) => $(`.ex-${k}`).addEventListener("input", () => { st[k] = Number($(`.ex-${k}`).value); draw(); }));
      $(".ex-win").addEventListener("input", () => { win = Number($(".ex-win").value); draw(); });
      $(".ex-idle").addEventListener("change", () => { st.idle = Number($(".ex-idle").value); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, defaults); win = 0; ["burst", "fw", "fr", "idle"].forEach((k) => { $(`.ex-${k}`).value = st[k]; }); draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { fifo: fifoView },
    help: {
      fifo: "ה-burst וקצבי הכתיבה והקריאה בסליידרים : הרצועה מראה את שני השעונים, הכתיבות, הקריאות (משבצת מדולגת מוצללת) ואת המילוי בזמן אמיתי, הסליידר שלה מזיז חלון של 40 מחזורי כתיבה, והגרף מראה את המילוי לאורך כל ה-burst ליד הנוסחה.",
    },
    models: { fifoSteps, fifoDepth, fifoFill, fifoEvents, fifoGrid },
  });
})();
