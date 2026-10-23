// kinds: stock
//   stock                  0006        prices to drag or draw, the scan played day by day: the cheapest and dearest day so far, the best long and short; the copy link carries the prices and the day
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { H, STATE_CODECS, W, X0, arrowStep, f, ltr, seedControls } = dvqExplorers.lib;

  // Stock (0006): the page's single scan, day by day: the cheapest and the dearest day so
  // far (before today), the long and the short that would close today, the best of each
  // so far, and the page's verdict (a short wins only when strictly better).
  const stockScan = (prices) => {
    const frames = [];
    let minP = null, minI = null, maxP = null, maxI = null;
    let lb = 0, lo = null, lc = null, sb = 0, so = null, sc = null;
    prices.forEach((p, i) => {
      if (i === 0) { minP = p; minI = 0; maxP = p; maxI = 0; }
      const longToday = p - minP, shortToday = maxP - p;
      const impL = longToday > lb, impS = shortToday > sb;
      if (impL) { lb = longToday; lo = minI; lc = i; }
      if (impS) { sb = shortToday; so = maxI; sc = i; }
      const fr = { i, p, minP, minI, maxP, maxI, longToday, shortToday, impL, impS, lb, lo, lc, sb, so, sc };
      if (p < minP) { minP = p; minI = i; }
      if (p > maxP) { maxP = p; maxI = i; }
      fr.minAfter = minP; fr.minIAfter = minI; fr.maxAfter = maxP; fr.maxIAfter = maxI;
      frames.push(fr);
    });
    const kind = sb > lb ? "short" : lb > 0 ? "long" : null;
    return { frames, long: { best: lb, open: lo, close: lc }, short: { best: sb, open: so, close: sc }, kind };
  };
  const stockRandom = (n, rnd = Math.random) => Array.from({ length: n }, () => 1 + Math.floor(rnd() * 20));

  // The stock box (0006): prices to drag (or draw at random, or the page's example), the
  // page's scan played day by day with the cheapest day so far (the long) and, with the
  // part b toggle, the dearest day so far (the short); the best trade of each kind.
  const stockView = () => ({
    mount(box) {
      const PAGE = [5, 8, 3, 9, 2, 6], PMAX = 20;
      const st = { prices: PAGE.slice(), k: PAGE.length, both: true };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>העסקאות <select class="ex-mode" aria-label="אילו עסקאות מותרות"><option value="long">לונג בלבד (סעיף א)</option><option value="both" selected>לונג ושורט (סעיף ב)</option></select></label>` +
        `<span class="wv-presets">מחירים : <button type="button" class="md-button ex-preset" data-p="page">דוגמת העמוד</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="up">עולה</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="down">יורד</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="random">אקראי</button></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">היום הבא</button>` +
        `<button type="button" class="md-button ex-prev">היום הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1200">איטי</option><option value="700" selected>בינוני</option><option value="250">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<p class="wv-hint">גוררים נקודה למעלה או למטה כדי לשנות את המחיר של אותו יום (או חיצים במקלדת על נקודה מסומנת).</p>` +
        `<div class="st-chart"></div><p class="wv-step" aria-live="polite"></p><p class="ex-summary wv-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), chart = $(".st-chart");
      let timer = null, drag = null;
      const W = 640, H = 300, X0 = 44, X1 = W - 16, Y0 = 16, Y1 = H - 36;
      const X = (i) => X0 + ((i + 0.5) / st.prices.length) * (X1 - X0);
      const Y = (p) => Y1 - (p / PMAX) * (Y1 - Y0);
      const dayName = (i) => `יום ${i}`;
      const draw = () => {
        const prices = st.prices, n = prices.length, sc = stockScan(prices);
        st.k = Math.min(st.k, n);
        const seen = sc.frames.slice(0, st.k), fr = st.k ? seen[st.k - 1] : null;
        let s = `<svg class="perf-chart st-live" viewBox="0 0 ${W} ${H}" role="group" aria-label="גרף המחירים לפי יום, עם המינימום והמקסימום עד כה והעסקאות הטובות">`;
        for (let v = 0; v <= PMAX; v += 5) s += `<line class="grid" x1="${X0}" x2="${X1}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        if (fr) s += `<rect class="st-cursor" x="${f(X(st.k - 1) - (X1 - X0) / n / 2)}" y="${Y0}" width="${f((X1 - X0) / n)}" height="${Y1 - Y0}"/>`;
        s += `<polyline class="st-price" points="${prices.map((p, i) => `${f(X(i))},${f(Y(p))}`).join(" ")}"/>`;
        // the cheapest and the dearest day so far, as steps, over the days scanned
        const stepLine = (key, cls) => {
          if (!seen.length) return "";
          const half = (X1 - X0) / n / 2;
          let d = "";
          seen.forEach((g, i) => { const v = g[key]; d += `${i ? " V" + f(Y(v)) : "M" + f(X(i) - half) + "," + f(Y(v))} H${f(X(i) + half)}`; });
          return `<path class="st-run ${cls}" d="${d}"/>`;
        };
        s += stepLine("minP", "st-min");
        if (st.both) s += stepLine("maxP", "st-max");
        const seg = (o, c, cls) => (o === null || c === null ? "" : `<line class="st-trade ${cls}" x1="${f(X(o))}" y1="${f(Y(prices[o]))}" x2="${f(X(c))}" y2="${f(Y(prices[c]))}"/>`);
        if (fr) { s += seg(fr.lo, fr.lc, "st-min"); if (st.both) s += seg(fr.so, fr.sc, "st-max"); }
        prices.forEach((p, i) => {
          const cur = i === st.k - 1;
          s += `<g class="st-pt${cur ? " is-cur" : ""}${i < st.k ? " is-seen" : ""}" data-i="${i}" tabindex="0" role="slider" aria-label="${dayName(i)} : מחיר ${p}, גרירה או חיצים משנים" aria-valuemin="1" aria-valuemax="${PMAX}" aria-valuenow="${p}"><circle cx="${f(X(i))}" cy="${f(Y(p))}" r="9"/><text x="${f(X(i))}" y="${f(Y(p) - 13)}" text-anchor="middle">${p}</text></g>`;
          s += `<text class="tick" x="${f(X(i))}" y="${Y1 + 18}" text-anchor="middle">${i}</text>`;
        });
        s += `<line class="axis" x1="${X0}" x2="${X1}" y1="${Y1}" y2="${Y1}"/></svg>`;
        chart.innerHTML = s;
        $(".ex-pos").textContent = `יום ${st.k} מתוך ${n}`;
        let step;
        if (!fr) step = `לפני היום הראשון : המינימום והמקסימום עד כה הם המחיר של יום 0, והעסקה הטובה ביותר היא 0.`;
        else {
          step = `${dayName(fr.i)} : המחיר ${ltr(fr.p)}. לונג שנסגר היום : ${ltr(`${fr.p} − ${fr.minP} = ${fr.longToday}`)} (קנייה ב${dayName(fr.minI)})` +
            (fr.impL ? ` <span class="wv-ok">✅ הלונג הטוב ביותר עד כה</span>` : fr.longToday <= 0 ? `, לא מרוויח` : `, לא עובר את ${ltr(fr.lb)}`) + `.`;
          if (st.both) step += ` שורט שנסגר היום : ${ltr(`${fr.maxP} − ${fr.p} = ${fr.shortToday}`)} (מכירה ב${dayName(fr.maxI)})` +
            (fr.impS ? ` <span class="wv-ok">✅ השורט הטוב ביותר עד כה</span>` : fr.shortToday <= 0 ? `, לא מרוויח` : `, לא עובר את ${ltr(fr.sb)}`) + `.`;
          const upd = [];
          if (fr.minAfter !== fr.minP) upd.push(`המינימום עד כה הופך ל-${ltr(fr.minAfter)}`);
          if (st.both && fr.maxAfter !== fr.maxP) upd.push(`המקסימום עד כה הופך ל-${ltr(fr.maxAfter)}`);
          step += upd.length ? ` אחרי היום : ${upd.join(", ")}.` : ` המינימום${st.both ? " והמקסימום" : ""} עד כה לא משתנ${st.both ? "ים" : "ה"}.`;
        }
        $(".wv-step").innerHTML = step;
        const L = fr ? { best: fr.lb, open: fr.lo, close: fr.lc } : sc.long, S = fr ? { best: fr.sb, open: fr.so, close: fr.sc } : sc.short;
        let sum = L.best > 0 ? `הלונג הטוב ביותר : רווח ${ltr(L.best)}, קנייה ביום ${ltr(L.open)} ומכירה ביום ${ltr(L.close)}.` : `אין לונג שמרוויח.`;
        if (st.both) {
          sum += S.best > 0 ? ` השורט הטוב ביותר : רווח ${ltr(S.best)}, מכירה ביום ${ltr(S.open)} וקנייה בחזרה ביום ${ltr(S.close)}.` : ` אין שורט שמרוויח.`;
          if (st.k >= n) sum += S.best > L.best ? ` <span class="wv-ok">התשובה : שורט ברווח ${ltr(S.best)}, ימים ${ltr(S.open)} ו-${ltr(S.close)}.</span>` : L.best > 0 ? ` <span class="wv-ok">התשובה : לונג ברווח ${ltr(L.best)}, ימים ${ltr(L.open)} ו-${ltr(L.close)}.</span>` : ` <span class="wv-ok">התשובה : רווח 0, בלי עסקה.</span>`;
        } else if (st.k >= n) sum += L.best > 0 ? ` <span class="wv-ok">התשובה : רווח ${ltr(L.best)}, ימים ${ltr(L.open)} ו-${ltr(L.close)}.</span>` : ` <span class="wv-ok">התשובה : רווח 0, בלי ימים.</span>`;
        $(".wv-sum").innerHTML = sum;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const setPrices = (p, k) => { stop(); st.prices = p; st.k = k === undefined ? p.length : k; draw(); };
      const priceAt = (e) => {
        const svg = chart.querySelector("svg"), r = svg.getBoundingClientRect();
        const y = ((e.clientY - r.top) / r.height) * H;
        return Math.max(1, Math.min(PMAX, Math.round(((Y1 - y) / (Y1 - Y0)) * PMAX)));
      };
      chart.addEventListener("pointerdown", (e) => {
        const g = e.target.closest(".st-pt");
        if (!g) return;
        stop(); drag = Number(g.dataset.i);
        chart.querySelector("svg").setPointerCapture(e.pointerId);
        chart.classList.add("is-dragging");
        e.preventDefault();
      });
      chart.addEventListener("pointermove", (e) => {
        if (drag === null) return;
        const p = priceAt(e);
        if (p === st.prices[drag]) return;
        const next = [...st.prices]; next[drag] = p; st.prices = next; draw();
        const g = chart.querySelector(`.st-pt[data-i="${drag}"]`); if (g) g.focus({ preventScroll: true });
      });
      const end = () => { drag = null; chart.classList.remove("is-dragging"); };
      chart.addEventListener("pointerup", end);
      chart.addEventListener("pointercancel", end);
      chart.addEventListener("keydown", (e) => {
        const g = e.target.closest(".st-pt");
        if (!g) return;
        const d = e.key === "ArrowUp" || e.key === "ArrowDown" ? Math.sign(arrowStep(e)) * (e.shiftKey ? 5 : 1) : 0;
        if (!d) return;
        e.preventDefault(); e.stopPropagation(); stop();
        const i = Number(g.dataset.i), next = [...st.prices];
        next[i] = Math.max(1, Math.min(PMAX, next[i] + d)); st.prices = next; draw();
        chart.querySelector(`.st-pt[data-i="${i}"]`).focus({ preventScroll: true });
      });
      $(".ex-mode").addEventListener("change", () => { st.both = $(".ex-mode").value === "both"; draw(); });
      const seed = seedControls(box, $(".wv-presets"), (rng) => setPrices(stockRandom(10, rng), 0), { state: {
        get: () => STATE_CODECS.stock.enc({ prices: st.prices, k: st.k, both: st.both }),
        set: (p) => { const d = STATE_CODECS.stock.dec(p); if (!d) return false; st.both = d.both; $(".ex-mode").value = d.both ? "both" : "long"; setPrices(d.prices, d.k); return true; },
      } });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => {
        const p = b.dataset.p;
        if (p === "page") setPrices(PAGE.slice(), 0);
        else if (p === "up") setPrices([3, 4, 6, 7, 9, 11, 12, 14, 16, 18], 0);
        else if (p === "down") setPrices([18, 16, 15, 13, 12, 10, 8, 7, 5, 3], 0);
        else seed.draw();
      }));
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, st.prices.length); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = st.prices.length; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= st.prices.length) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= st.prices.length) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { stock: stockView },
    help: {
      stock: "גוררים מחירים או מגרילים : ״היום הבא״ ו״הפעלה״ מריצים את הסריקה יום אחרי יום עם המינימום והמקסימום עד כה והעסקה הטובה ביותר. הבורר עובר ללונג בלבד.",
    },
    models: { stockScan, stockRandom },
  });
})();
