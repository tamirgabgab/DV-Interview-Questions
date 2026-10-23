// kinds: coverage
//   coverage               0041        2 to 10 bins with a weight each and at_least k: tests played one at a time into the bins, 1,000 runs as a histogram against the exact expectation (the integral, the k = 1 closed form)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, H, TOP, W, X0, autoplay, f, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Coverage (0041): n bins with probabilities p, at_least k. The expectation by the
  // Poisson embedding (Simpson's rule on 1 - prod P(Poisson(p_i t) >= k)), the k = 1
  // closed form over the subsets, the chain on the number of covered equal bins, and
  // one simulated run.
  const covProbs = (weights) => { const s = weights.reduce((a, b) => a + b, 0); return weights.map((w) => w / s); };
  const covPoissonAtLeast = (lam, k) => { let term = Math.exp(-lam), below = 0; for (let j = 0; j < k; j++) { below += term; term *= lam / (j + 1); } return 1 - below; };
  const covExpected = (p, k, h = 0.02) => {
    const uncovered = (t) => { let prod = 1; for (const pi of p) prod *= covPoissonAtLeast(pi * t, k); return 1 - prod; };
    let total = 0, t = 0;
    for (;;) {
      const a = uncovered(t), m = uncovered(t + h / 2), b = uncovered(t + h);
      total += (h * (a + 4 * m + b)) / 6;
      t += h;
      if (t > 1 && b < 1e-12) return total;
    }
  };
  const covK1 = (p) => {
    let total = 0;
    for (let mask = 1; mask < 1 << p.length; mask++) {
      let s = 0, bits = 0;
      for (let i = 0; i < p.length; i++) if ((mask >> i) & 1) { s += p[i]; bits++; }
      total += (bits % 2 ? 1 : -1) / s;
    }
    return total;
  };
  const covStep = (prob, n) => prob.map((v, c) => (v * c) / n + (c ? (prob[c - 1] * (n - c + 1)) / n : 0));
  const covCurve = (n, tmax) => { let prob = [1].concat(new Array(n).fill(0)); const out = []; for (let t = 0; t <= tmax; t++) { out.push(prob[n]); prob = covStep(prob, n); } return out; };
  const covQuantile = (n, q) => { let prob = [1].concat(new Array(n).fill(0)), t = 0; while (prob[n] < q) { prob = covStep(prob, n); t++; } return t; };
  const covDraw = (p, rnd) => { let r = rnd(), i = 0; while (i < p.length - 1 && r >= p[i]) { r -= p[i]; i++; } return i; };
  const covSimulate = (p, k, rnd) => { const hits = new Array(p.length).fill(0); let left = p.length, t = 0; while (left) { const i = covDraw(p, rnd); hits[i]++; t++; if (hits[i] === k) left--; } return t; };

  // The coverage box (0041): 2 to 10 bins with a weight slider each (the probabilities
  // are the weights normalised) and at_least k; tests played one at a time into the bins
  // until every bin has k hits; 1,000 seeded runs as a histogram of the number of tests
  // with the mean and the 95 % point against the exact expectation.
  const coverageView = () => ({
    mount(box) {
      const d = box.dataset;
      const NMAX = 10, KMAX = 5, RUNS = 1000;
      const W0 = (d.weights || "1 1 1 1").split(/\s+/).map(Number).filter((v) => v >= 1 && v <= 10).slice(0, NMAX);
      const N0 = Math.min(NMAX, Math.max(2, Number(d.n || W0.length))), K0 = Math.min(KMAX, Math.max(1, Number(d.k || 1)));
      while (W0.length < N0) W0.push(1);
      const st = { w: W0.slice(0, N0), k: K0, hits: [], t: 0, runs: null, seed: null };
      const presets = [["equal", "שווים"], ["rare", "אחד נדיר"], ["steps", "מדרגות"]];
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>תאים <select class="cv-n" aria-label="מספר התאים">${Array.from({ length: NMAX - 1 }, (_, i) => `<option value="${i + 2}"${i + 2 === N0 ? " selected" : ""}>${i + 2}</option>`).join("")}</select></label>` +
        `<label>‏at_least <select class="cv-k" aria-label="פגיעות נדרשות בכל תא">${Array.from({ length: KMAX }, (_, i) => `<option value="${i + 1}"${i + 1 === K0 ? " selected" : ""}>${i + 1}</option>`).join("")}</select></label>` +
        `<span class="wv-presets">משקלים : ${presets.map(([v, t]) => `<button type="button" class="md-button ex-preset" data-w="${v}">${t}</button>`).join(" ")}</span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="cv-weights" role="group" aria-label="המשקל של כל תא"></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">הטסט הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(700, 300, 80) +
        `<button type="button" class="md-button ex-end">עד הכיסוי</button>` +
        `<button type="button" class="md-button ex-start">ניקוי</button>` +
        `<button type="button" class="md-button ex-random">${ltr("1,000")} ריצות</button><span class="ex-pos"></span></div>` +
        `<p class="ex-summary cv-sum" aria-live="polite"></p><p class="cv-run"></p>` +
        `<div class="cv-bins"></div>` +
        `<p class="ex-title cv-hist-title"></p><div class="cv-hist"></div><p class="ex-note cv-hist-note"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let stop = () => {}, runRng = Math.random;
      const probs = () => covProbs(st.w);
      const covered = () => st.hits.every((h) => h >= st.k);
      const weightsHtml = () => {
        $(".cv-weights").innerHTML = st.w.map((w, i) => `<label><span>תא ${i}</span><input type="range" class="cv-w" data-i="${i}" min="1" max="10" step="1" value="${w}" dir="ltr" aria-label="המשקל של תא ${i}"><output>${w}</output></label>`).join("");
        box.querySelectorAll(".cv-w").forEach((r) => r.addEventListener("input", () => { st.w[Number(r.dataset.i)] = Number(r.value); r.nextElementSibling.textContent = r.value; st.runs = null; clear(); }));
      };
      const binsSvg = (p) => {
        const n = st.w.length, W = 640, H = 190, X0 = 40, BASE = 150, TOP = 20, slot = (W - X0 - 12) / n, bw = Math.min(56, slot * 0.6);
        const top = Math.max(st.k + 1, ...st.hits), Y = (v) => BASE - (v / top) * (BASE - TOP);
        let h = `<svg class="perf-chart cv-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="${n} התאים : מספר הפגיעות בכל אחד, והקו של at_least">`;
        const step = top > 20 ? 5 : top > 8 ? 2 : 1;
        for (let v = 0; v <= top; v += step) h += `<line class="grid" x1="${X0}" x2="${W - 12}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        h += `<line class="ink-line" x1="${X0}" x2="${W - 12}" y1="${f(Y(st.k))}" y2="${f(Y(st.k))}" stroke-width="1.5" stroke-dasharray="6 4"/><text class="legend halo" x="${X0 + 6}" y="${f(Y(st.k) - 5)}">at_least = ${st.k}</text>`;
        st.hits.forEach((v, i) => {
          const x = X0 + (i + 0.5) * slot, done = v >= st.k;
          h += `<rect class="bar ${done ? "by-bfs" : "by-multiples"}" x="${f(x - bw / 2)}" y="${f(Y(v))}" width="${f(bw)}" height="${f(BASE - Y(v))}" rx="2"><title>תא ${i} : ${v} פגיעות, p = ${p[i].toFixed(3)}</title></rect>` +
               `<text class="tick" x="${f(x)}" y="${f(Y(v) - 5)}" text-anchor="middle">${v}</text>` +
               `<text class="tick" x="${f(x)}" y="${BASE + 16}" text-anchor="middle">${i}</text><text class="tick" x="${f(x)}" y="${BASE + 32}" text-anchor="middle">${p[i].toFixed(2)}</text>`;
        });
        return h + `<line class="axis" x1="${X0}" x2="${W - 12}" y1="${BASE}" y2="${BASE}"/></svg>`;
      };
      const histSvg = (exact) => {
        const runs = st.runs, m = runs.length, lo = Math.min(...runs), hi = Math.max(...runs);
        const width = Math.max(1, Math.ceil((hi - lo + 1) / 40)), nb = Math.ceil((hi - lo + 1) / width);
        const counts = new Array(nb).fill(0);
        runs.forEach((v) => { counts[Math.floor((v - lo) / width)]++; });
        const sorted = runs.slice().sort((a, b) => a - b), mean = runs.reduce((a, b) => a + b, 0) / m, q95 = sorted[Math.min(m - 1, Math.ceil(0.95 * m) - 1)];
        const W = 640, H = 210, X0 = 40, BASE = 170, TOP = 16, slot = (W - X0 - 12) / nb, cmax = Math.max(...counts);
        const Y = (v) => BASE - (v / cmax) * (BASE - TOP), X = (v) => X0 + ((v - lo) / width) * slot;
        let h = `<svg class="perf-chart cv-histsvg" viewBox="0 0 ${W} ${H}" role="img" aria-label="היסטוגרמה של מספר הטסטים ב-${m} ריצות">`;
        counts.forEach((c, b) => { h += `<rect class="bar by-multiples" x="${f(X0 + b * slot + 1)}" y="${f(Y(c))}" width="${f(Math.max(1, slot - 2))}" height="${f(BASE - Y(c))}"><title>${lo + b * width}${width > 1 ? `–${lo + b * width + width - 1}` : ""} טסטים : ${c} ריצות</title></rect>`; });
        const mark = (v, cls, lab, dy) => `<line class="${cls}" x1="${f(X(v) + slot / 2)}" x2="${f(X(v) + slot / 2)}" y1="${TOP}" y2="${BASE}" stroke-width="2"/><text class="legend halo" x="${f(X(v) + slot / 2 + 4)}" y="${TOP + dy}">${lab}</text>`;
        h += mark(mean, "s2-line", `ממוצע ${mean.toFixed(1)}`, 12) + mark(exact, "ink-line", `תוחלת ${exact.toFixed(1)}`, 28) + mark(q95, "s3-line", `95% : ${q95}`, 44);
        const every = Math.max(1, Math.ceil(nb / 8));
        for (let b = 0; b < nb; b += every) h += `<text class="tick" x="${f(X0 + b * slot + slot / 2)}" y="${BASE + 16}" text-anchor="middle">${lo + b * width}</text>`;
        return h + `<line class="axis" x1="${X0}" x2="${W - 12}" y1="${BASE}" y2="${BASE}"/></svg>`;
      };
      const draw = () => {
        const p = probs(), n = st.w.length, exact = covExpected(p, st.k), k1 = st.k === 1 ? covK1(p) : null;
        const done = covered();
        $(".cv-bins").innerHTML = binsSvg(p);
        $(".ex-pos").textContent = `${st.t} טסטים`;
        $(".ex-next").disabled = done; $(".ex-end").disabled = done;
        const equal = st.w.every((w) => w === st.w[0]);
        $(".cv-sum").innerHTML = `${ltr(n)} תאים${equal ? " שווים" : ` עם ההסתברויות ${ltr(p.map((x) => x.toFixed(2)).join(", "))}`}, לפחות ${ltr(st.k)} ${st.k === 1 ? "פגיעה" : "פגיעות"} בכל תא : התוחלת היא ${ltr(exact.toFixed(2))} טסטים` +
          (k1 !== null ? ` (הנוסחה הסגורה : ${ltr(k1.toFixed(2))}${equal ? `, כלומר ${ltr(`${n}·H${n}`)}` : ""})` : " (האינטגרל)") + (equal && st.k === 1 ? `; ל-95% צריך ${ltr(covQuantile(n, 0.95))}.` : ".");
        const left = st.hits.filter((h) => h < st.k).length;
        $(".cv-run").innerHTML = st.t === 0 ? `עוד לא רץ אף טסט. "הטסט הבא" מגריל תא לפי ההסתברויות.` :
          done ? `<span class="wv-ok">✓ כיסוי מלא אחרי ${ltr(st.t)} טסטים</span>` + (st.t > exact ? `, יותר מהתוחלת.` : `, פחות מהתוחלת.`) :
          `אחרי ${ltr(st.t)} טסטים חסרים עוד ${ltr(left)} ${left === 1 ? "תא" : "תאים"} (${ltr(st.hits.map((h, i) => (h < st.k ? i : null)).filter((v) => v !== null).join(", "))}); הסיכוי שהטסט הבא מתקדם : ${ltr(st.hits.reduce((acc, h, i) => acc + (h < st.k ? p[i] : 0), 0).toFixed(2))}.`;
        if (st.runs) {
          const m = st.runs.length, mean = st.runs.reduce((a, b) => a + b, 0) / m;
          $(".cv-hist-title").innerHTML = `${ltr("1,000")} ריצות מהזרע ${ltr(st.seed)} : היסטוגרמה של מספר הטסטים עד הכיסוי`;
          $(".cv-hist").innerHTML = histSvg(exact);
          const sd = Math.sqrt(st.runs.reduce((a, v) => a + (v - mean) ** 2, 0) / m);
          $(".cv-hist-note").innerHTML = `הממוצע ${ltr(mean.toFixed(1))} לעומת התוחלת ${ltr(exact.toFixed(1))} (סטיית תקן ${ltr(sd.toFixed(1))}, שגיאת הממוצע כ-${ltr((sd / Math.sqrt(m)).toFixed(1))}); ` +
            `הריצה הקצרה ${ltr(Math.min(...st.runs))} והארוכה ${ltr(Math.max(...st.runs))}.`;
        } else { $(".cv-hist-title").textContent = ""; $(".cv-hist").innerHTML = ""; $(".cv-hist-note").textContent = ""; }
      };
      const clear = () => { stop(); st.hits = new Array(st.w.length).fill(0); st.t = 0; draw(); };
      const test = () => { if (covered()) return; const i = covDraw(probs(), runRng); st.hits[i]++; st.t++; draw(); };
      const setN = (n) => { st.w = st.w.slice(0, n); while (st.w.length < n) st.w.push(1); st.runs = null; weightsHtml(); clear(); };
      $(".cv-n").addEventListener("change", () => setN(Number($(".cv-n").value)));
      $(".cv-k").addEventListener("change", () => { st.k = Number($(".cv-k").value); st.runs = null; clear(); });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => {
        const n = st.w.length;
        st.w = b.dataset.w === "equal" ? new Array(n).fill(5) : b.dataset.w === "rare" ? [1].concat(new Array(n - 1).fill(10)) : Array.from({ length: n }, (_, i) => i + 1);
        st.runs = null; weightsHtml(); clear();
      }));
      $(".ex-reset").addEventListener("click", () => { st.w = W0.slice(0, N0); st.k = K0; $(".cv-n").value = String(N0); $(".cv-k").value = String(K0); st.runs = null; weightsHtml(); clear(); });
      $(".ex-next").addEventListener("click", () => { stop(); test(); });
      $(".ex-end").addEventListener("click", () => { stop(); while (!covered()) { const i = covDraw(probs(), runRng); st.hits[i]++; st.t++; } draw(); });
      $(".ex-start").addEventListener("click", clear);
      const seed = seedControls(box, $(".ex-random"), (rng, s) => { stop(); st.seed = s; st.runs = Array.from({ length: RUNS }, () => covSimulate(probs(), st.k, rng)); draw(); });
      $(".ex-random").addEventListener("click", () => seed.draw());
      stop = autoplay(play, speed, { step: test, done: covered, restart: () => { st.hits = new Array(st.w.length).fill(0); st.t = 0; draw(); } });
      weightsHtml();
      clear();
    },
  });

  dvqExplorers.register({
    views: { coverage: coverageView },
    help: {
      coverage: "בוחרים מספר תאים, משקל לכל תא ו-at_least : ״הטסט הבא״ ו״הפעלה״ מגרילים טסט אחרי טסט עד שכל התאים מכוסים, ו״1,000 ריצות״ מציירות היסטוגרמה של מספר הטסטים עם הממוצע וה-95% לעומת התוחלת המחושבת.",
    },
    models: { covProbs, covExpected, covK1, covCurve, covQuantile, covSimulate, covDraw },
  });
})();
