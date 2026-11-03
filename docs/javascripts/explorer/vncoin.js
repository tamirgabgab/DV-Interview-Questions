// kinds: vncoin cmpcoin
//   vncoin                 0079 (a)    a coin with P(1) = p, flipped in pairs by seed: HT gives 1, TH gives 0, HH and TT are thrown away (von Neumann); the last pairs and bits, the flips per bit against 1/(p(1−p)) and the share of ones against 1/2
//   cmpcoin                0079 (b)    a coin with any p from a fair coin: the fair flips against the binary digits of p, stopped at the first difference (1 when p has 1 there); one flip, a whole trial or 1000 trials by seed, the share of ones against p and the flips against 2 (2 − 2^(1−k) for a p of k digits)
// Loaded after core.js on the pages that have these kinds (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { ltr, mulberry32, autoplay, speedSel, seedControls } = dvqExplorers.lib;
  const NB = " ";

  // --- part a: von Neumann's pairs -----------------------------------------------------------
  // the bit of a pair: 1 for HT (a = 1, b = 0), 0 for TH, null for HH and TT
  const vnPair = (a, b) => (a === b ? null : a);
  // the expected flips per fair bit: rounds of two flips, each deciding with 2p(1 − p)
  const vnExpected = (p) => 1 / (p * (1 - p));
  // `pairs` pairs flipped by a seeded generator: the flips and the bits they give
  const vnRun = (seed, p, pairs) => {
    const rng = mulberry32(seed), flips = [], bits = [];
    for (let i = 0; i < pairs; i++) {
      const a = rng() < p ? 1 : 0, b = rng() < p ? 1 : 0, v = vnPair(a, b);
      flips.push(a, b);
      if (v !== null) bits.push(v);
    }
    return { flips, bits };
  };

  // --- part b: the comparison with the digits of p ----------------------------------------
  // the first k binary digits of num/den in (0, 1), shorter when the expansion ends (a dyadic p)
  const bcDigits = (num, den, k) => {
    let out = "";
    for (let i = 0; i < k && num > 0; i++) {
      num *= 2;
      const d = num >= den ? 1 : 0;
      num -= d * den;
      out += d;
    }
    return out;
  };
  // the same for a double: doubling and subtracting 1 are exact
  const bcDigitsOf = (x, k) => {
    let out = "";
    for (let i = 0; i < k && x > 0; i++) { x *= 2; const d = x >= 1 ? 1 : 0; x -= d; out += d; }
    return out;
  };
  // the comparison of the fair flips (0 / 1) with the digits of p (a string; `ends` when the
  // expansion has no more digits): {done, out, stop}, stop the index of the deciding flip,
  // or the number of digits when they ran out (no flip: U >= p, out 0)
  const bcCompare = (digits, flips, ends) => {
    for (let i = 0; ; i++) {
      if (ends && i === digits.length) return { done: true, out: 0, stop: i };
      if (i >= flips.length) return { done: false, out: null, stop: -1 };
      const d = i < digits.length ? Number(digits[i]) : 0;
      if (flips[i] !== d) return { done: true, out: d, stop: i };
    }
  };
  // the expected flips: 2 for a p with no end, 2 − 2^(1−k) for a p of k digits
  const bcExpected = (k) => (k === null ? 2 : 2 - 2 ** (1 - k));
  // the p of the box: a fraction, or 1/√2
  const BC_PS = { "1/3": [1, 3], "2/3": [2, 3], "1/5": [1, 5], "2/5": [2, 5], "3/4": [3, 4], "5/8": [5, 8], "1/√2": null };
  const BC_LONG = 1100;     // more digits than any double has, and than any trial reaches
  const bcOf = (key) => {
    const f = BC_PS[key];
    const value = f ? f[0] / f[1] : Math.SQRT1_2;
    const all = f ? bcDigits(f[0], f[1], BC_LONG) : bcDigitsOf(value, BC_LONG);
    const ends = f ? (f[1] & (f[1] - 1)) === 0 : false;   // 1/√2 as a double ends too, after 53 digits: shown as the real 1/√2
    return { value, digits: all, ends, k: ends ? all.length : null };
  };
  // `trials` comparisons by a seeded fair coin: the number of ones and of flips
  const bcRun = (seed, key, trials) => {
    const rng = mulberry32(seed), P = bcOf(key);
    let ones = 0, flips = 0;
    for (let t = 0; t < trials; t++) {
      const fl = [];
      for (;;) {
        const c = bcCompare(P.digits, fl, P.ends);
        if (c.done) { ones += c.out; break; }
        fl.push(rng() < 0.5 ? 1 : 0);
        flips++;
      }
    }
    return { ones, flips };
  };

  const SHOW = 16, BITS = 24;
  // a bit cell; a cell marked same or stop shows that tint instead of the tint of a 1
  const cell = (bit, cls = "") => `<td class="gs-b${(bit === 1 || bit === "1") && !/bc-/.test(cls) ? " is-one" : ""}${cls}">${bit}</td>`;
  const empty = () => `<td class="gs-b is-lead"> </td>`;
  const num = (v, n = 2) => (Math.abs(v - Math.round(v)) < 1e-9 ? String(Math.round(v)) : v.toFixed(n));

  // --- the vncoin box -----------------------------------------------------------------------
  const vncoinView = () => ({
    mount(box) {
      const P0 = Math.min(0.95, Math.max(0.05, Number(box.dataset.p) || 0.3));
      const st = { p: P0, rng: mulberry32(79), pairs: [], bits: [], flips: 0, ones: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏P(1) = p</span><input type="range" class="vn-p" min="0.05" max="0.95" step="0.05" value="${P0}" dir="ltr" aria-label="ההסתברות של המטבע להראות 1"><output class="vn-out">${P0.toFixed(2)}</output></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערך של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">זוג אחד</button>` +
        `<button type="button" class="md-button vn-many">100 זוגות</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(900, 450, 150) +
        `<button type="button" class="md-button ex-start">ניקוי</button><span class="vn-anchor"></span></div>` +
        `<p class="ex-summary vn-sum" aria-live="polite"></p>` +
        `<p class="ex-title">${SHOW} הזוגות האחרונים, מהישן לחדש</p>` +
        `<div class="gs-scroll" data-steady><table class="gs-bits vn-pairs" dir="ltr" aria-label="הזוגות האחרונים והביט של כל זוג"><tbody></tbody></table></div>` +
        `<span class="viz-legend"><span><i class="gs-key-one"></i>הטלה של 1</span><span><i class="bc-key-one"></i>‏HT : הביט 1</span><span><i class="bc-key-zero"></i>‏TH : הביט 0</span><span><i class="gs-key-lead"></i>זוג שווה : נזרק (↺)</span></span>` +
        `<p class="ex-title">${BITS} הביטים ההוגנים האחרונים</p>` +
        `<div class="gs-scroll" data-steady><table class="gs-bits vn-bits" dir="ltr" aria-label="הביטים ההוגנים האחרונים"><tbody></tbody></table></div>` +
        `<p class="vn-count"></p>`;
      const $ = (s) => box.querySelector(s);
      const slider = $(".vn-p"), play = $(".ex-play"), speed = $(".ex-speed");
      const clear = () => { st.pairs = []; st.bits = []; st.flips = 0; st.ones = 0; };
      const one = () => {
        const a = st.rng() < st.p ? 1 : 0, b = st.rng() < st.p ? 1 : 0, v = vnPair(a, b);
        st.pairs.push([a, b]);
        if (st.pairs.length > SHOW) st.pairs.shift();
        st.flips += 2;
        if (v !== null) { st.bits.push(v); st.ones += v; }
      };
      const total = () => st.bits.length;
      const draw = () => {
        const p = st.p, e = vnExpected(p);
        $(".vn-out").textContent = p.toFixed(2);
        $(".vn-sum").innerHTML = `מטבע עם ${ltr(`p = ${p.toFixed(2)}`)}${NB}: זוג שונה בהסתברות ${ltr((2 * p * (1 - p)).toFixed(3))}, ` +
          `ולכן בממוצע ${ltr(num(e))} הטלות לביט הוגן, ${ltr("1/(p(1 − p))")}.`;
        let r1 = "", r2 = "", r3 = "";
        for (let i = 0; i < SHOW; i++) {
          const pr = st.pairs[i - (SHOW - st.pairs.length)];
          if (!pr) { r1 += empty(); r2 += empty(); r3 += empty(); continue; }
          const v = vnPair(pr[0], pr[1]), last = i === SHOW - 1 ? " vn-last" : "";
          r1 += cell(pr[0], last); r2 += cell(pr[1], last);
          r3 += v === null ? `<td class="gs-b is-lead${last}">↺</td>` : `<td class="gs-b ${v ? "bc-one" : "bc-zero"}${last}">${v}</td>`;
        }
        $(".vn-pairs tbody").innerHTML = `<tr><th>ראשונה</th>${r1}</tr><tr><th>שנייה</th>${r2}</tr><tr><th>הביט</th>${r3}</tr>`;
        const shown = st.bits.slice(-BITS);
        let b = "";
        for (let i = 0; i < BITS; i++) { const v = shown[i - (BITS - shown.length)]; b += v === undefined ? empty() : `<td class="gs-b ${v ? "bc-one" : "bc-zero"}">${v}</td>`; }
        $(".vn-bits tbody").innerHTML = `<tr><th>ביטים</th>${b}</tr>`;
        const k = total();
        $(".vn-count").innerHTML = !st.flips ? `עוד לא הוטל אף זוג. "זוג אחד" מטיל שתי הטלות, ו-"100 זוגות" מטיל מאתיים.` :
          `${ltr(st.flips)} הטלות, ${ltr(k)} ביטים הוגנים` + (k ? `${NB}: ${ltr(st.ones)} אחדות ו-${ltr(k - st.ones)} אפסים, כלומר ${ltr(`${(100 * st.ones / k).toFixed(1)}%`)} אחדות (התוחלת 50%). ` +
            `בממוצע ${ltr((st.flips / k).toFixed(2))} הטלות לביט, והתוחלת ${ltr(num(e))}.` : ". עוד לא יצא זוג שונה.");
      };
      const stop = autoplay(play, speed, { step: () => { one(); draw(); }, done: () => false, restart: () => {} });
      seedControls(box, $(".vn-anchor"), (rng) => { stop(); st.rng = rng; clear(); draw(); }, { seed: 79 });
      slider.addEventListener("input", () => { stop(); st.p = Number(slider.value); clear(); draw(); });
      $(".ex-next").addEventListener("click", () => { one(); draw(); });
      $(".vn-many").addEventListener("click", () => { stop(); for (let i = 0; i < 100; i++) one(); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); clear(); draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); slider.value = String(P0); slider.dispatchEvent(new Event("input", { bubbles: true })); });
      draw();
    },
  });

  // --- the cmpcoin box ----------------------------------------------------------------------
  const cmpcoinView = () => ({
    mount(box) {
      const K0 = BC_PS[box.dataset.p] !== undefined ? box.dataset.p : "1/3";
      const st = { key: K0, P: bcOf(K0), rng: mulberry32(79), flips: [], trials: 0, ones: 0, used: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>‏p <select class="cc-p" aria-label="ההסתברות הרצויה p">${Object.keys(BC_PS).map((k) => `<option value="${k}"${k === K0 ? " selected" : ""}>${k}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערך של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">הטלה אחת</button>` +
        `<button type="button" class="md-button cc-trial">עד הכרעה</button>` +
        `<button type="button" class="md-button cc-many">1000 ניסויים</button>` +
        `<button type="button" class="md-button ex-start">ניקוי</button><span class="cc-anchor"></span></div>` +
        `<p class="ex-summary cc-sum" aria-live="polite"></p>` +
        `<p class="ex-title">הספרות של p מול ההטלות ההוגנות של הניסוי הנוכחי</p>` +
        `<div class="gs-scroll" data-steady><table class="gs-bits cc-bits" dir="ltr" aria-label="הספרות הבינאריות של p וההטלות של הניסוי הנוכחי"><tbody></tbody></table></div>` +
        `<span class="viz-legend"><span><i class="gs-key-one"></i>ספרה או הטלה של 1</span><span><i class="bc-key-same"></i>שווה : ממשיכים</span><span><i class="bc-key-stop"></i>ההבדל הראשון : מכריעים</span></span>` +
        `<p class="cc-now"></p><p class="cc-count"></p>`;
      const $ = (s) => box.querySelector(s);
      const sel = $(".cc-p");
      const cmp = () => bcCompare(st.P.digits, st.flips, st.P.ends);
      const finish = (c) => { st.trials++; st.ones += c.out; st.used += st.flips.length; };
      // one flip of the current trial; a decided trial is cleared first
      const flip = () => {
        if (cmp().done) st.flips = [];
        let c = cmp();
        if (c.done) { finish(c); return; }   // a dyadic p whose digits already ran out: no flip
        st.flips.push(st.rng() < 0.5 ? 1 : 0);
        c = cmp();
        if (c.done) finish(c);
      };
      const trial = () => {
        if (cmp().done) st.flips = [];
        for (let c = cmp(); !c.done; c = cmp()) st.flips.push(st.rng() < 0.5 ? 1 : 0);
        finish(cmp());
      };
      const clear = () => { st.flips = []; st.trials = 0; st.ones = 0; st.used = 0; };
      const draw = () => {
        const P = st.P, c = cmp(), shown = P.ends ? P.digits : P.digits.slice(0, SHOW) + "…";
        $(".cc-sum").innerHTML = `${ltr(`p = ${st.key} = 0.${shown}`)}${NB}: ` + (P.ends
          ? `לפיתוח יש ${ltr(P.k)} ספרות, ולכן לכל היותר ${ltr(P.k)} הטלות, ובממוצע ${ltr(`2 − 2^(1−${P.k}) = ${num(bcExpected(P.k), 3)}`)}.`
          : `הפיתוח לא נגמר. כל הטלה מכריעה בהסתברות חצי, ולכן בממוצע 2 הטלות, בלי חסם.`);
        let top = "", low = "";
        for (let i = 0; i < SHOW; i++) {
          const d = i < P.digits.length ? P.digits[i] : null, f = st.flips[i];
          const cls = c.done && i === c.stop ? " bc-stop" : f !== undefined && (!c.done || i < c.stop) ? " bc-same" : "";
          top += d === null ? `<td class="gs-b is-lead${cls}">0</td>` : cell(d, cls);
          low += f === undefined ? empty() : cell(f, cls);
        }
        $(".cc-bits tbody").innerHTML = `<tr><th>p</th>${top}</tr><tr><th>U</th>${low}</tr>`;
        const n = st.flips.length;
        $(".cc-now").innerHTML = !n && !c.done ? `הניסוי הנוכחי עוד לא התחיל.` :
          !c.done ? `${ltr(n)} הטלות שוות לספרות של ${ltr("p")}, ועוד לא ידוע אם ${ltr("U < p")}.` :
          c.stop === n && c.stop === P.digits.length ? `הספרות של ${ltr("p")} נגמרו, וכל ההטלות שוות להן${NB}: ${ltr("U ≥ p")}, והתוצאה 0.` :
          `בהטלה ${ltr(c.stop + 1)} ל-${ltr("p")} יש ${ltr(P.digits[c.stop])} ולהטלה ${ltr(st.flips[c.stop])}${NB}: ` +
          (c.out ? `${ltr("U < p")}, והתוצאה 1.` : `${ltr("U > p")}, והתוצאה 0.`);
        const e = bcExpected(P.k);
        $(".cc-count").innerHTML = !st.trials ? `עוד אין ניסויים שהוכרעו.` :
          `${ltr(st.trials)} ניסויים${NB}: ${ltr(st.ones)} יצאו 1, כלומר ${ltr((st.ones / st.trials).toFixed(3))}, מול ${ltr(`p = ${P.value.toFixed(3)}`)}. ` +
          `בממוצע ${ltr((st.used / st.trials).toFixed(2))} הטלות לניסוי, והתוחלת ${ltr(num(e, 3))}.`;
      };
      seedControls(box, $(".cc-anchor"), (rng) => { st.rng = rng; clear(); draw(); }, { seed: 79 });
      sel.addEventListener("change", () => { st.key = sel.value; st.P = bcOf(st.key); clear(); draw(); });
      $(".ex-next").addEventListener("click", () => { flip(); draw(); });
      $(".cc-trial").addEventListener("click", () => { trial(); draw(); });
      $(".cc-many").addEventListener("click", () => { for (let i = 0; i < 1000; i++) trial(); draw(); });
      $(".ex-start").addEventListener("click", () => { clear(); draw(); });
      $(".ex-reset").addEventListener("click", () => { sel.value = K0; sel.dispatchEvent(new Event("change", { bubbles: true })); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { vncoin: vncoinView, cmpcoin: cmpcoinView },
    help: {
      vncoin: "בוחרים p, ומטילים זוג אחד, מאה זוגות או בהפעלה רציפה. זוג שונה נותן ביט (HT נותן 1 ו-TH נותן 0), וזוג שווה נזרק. הספירה משווה את מספר ההטלות לביט לתוחלת 1/(p(1−p)), ואת השבר של האחדות לחצי.",
      cmpcoin: "בוחרים p, ומטילים מטבע הוגן הטלה אחת בכל פעם, עד הכרעה או אלף ניסויים. ההטלות מושוות לספרות הבינאריות של p, וההבדל הראשון מכריע : 1 כש-p יש שם 1. הספירה משווה את השבר של האחדות ל-p ואת מספר ההטלות ל-2.",
    },
    models: { vnPair, vnExpected, vnRun, bcDigits, bcDigitsOf, bcCompare, bcExpected, bcOf, bcRun },
  });
})();
