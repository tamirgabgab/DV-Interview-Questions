// kinds: cake-arith cake-geo
//   cake-arith / cake-geo  0027, 0028  the law, sliders a and d (or q) with exact fields (a tiny a, a negative d, q below 1), and a person-by-person stepper of the cake; the proof panel: the people on the condition curve against the threshold
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, EPS, RIGHT, TOP, W, X0, f, fmt, frame, hline, ltr, speedSel } = dvqExplorers.lib;

  // Cake: person k takes p of what is left (R); a fraction of 1 or more takes the rest.
  // Fractions that never reach 1 (d <= 0, q <= 1) stop at the first negligible one (below
  // CAKE_MIN_P, or negative) or at CAKE_MAX people; the last row then has p < 1 and the
  // cake is not finished.
  const CAKE_MAX = 10000, CAKE_MIN_P = 1e-9;
  const cakeSplit = (kind, a, step) => {
    const rows = [];
    let R = 1;
    for (let k = 1; k <= CAKE_MAX; k++) {
      const raw = kind === "arith" ? a + (k - 1) * step : a * Math.pow(step, k - 1);
      if (raw < CAKE_MIN_P && k > 1) break;
      const p = Math.min(raw, 1);
      rows.push({ k, p, R, S: p * R });
      if (p >= 1) break;
      R *= 1 - p;
    }
    return rows;
  };
  const cakeDone = (rows) => rows.length > 0 && rows[rows.length - 1].p >= 1;
  const cakeThreshold = (kind, step) =>
    kind === "arith" ? (Math.sqrt(step * step + 4 * step) - step) / 2 : 1 - 1 / step;
  const cakeFormula = (kind, a, step) => {
    const T = cakeThreshold(kind, step);
    const x = kind === "arith" ? (T - a) / step + 1 : Math.log((step - 1) / a) / Math.log(step);
    const k = Math.max(1, Math.ceil(x - EPS));
    const pk = kind === "arith" ? a + (k - 1) * step : a * Math.pow(step, k - 1);
    return { k, tie: Math.abs(pk - T) < EPS };
  };
  // The condition of the proof, "the next person gets more", as a curve against p and a
  // level: arithmetic, f(p) = p² / (1 − p) below d; geometric, q (1 − p) above 1. They meet
  // at the threshold T.
  const cakeCondition = (kind, step, p) =>
    kind === "arith" ? { g: (p * p) / (1 - p), level: step, more: (p * p) / (1 - p) < step }
                     : { g: step * (1 - p), level: 1, more: step * (1 - p) > 1 };
  const cakeBest = (rows) => {
    const top = Math.max(...rows.map((r) => r.S));
    return rows.filter((r) => Math.abs(r.S - top) <= EPS * top).map((r) => r.k);
  };

  const barsChart = (label, values, highlight, titleOf, first = 1) => {
    const vmax = Math.max(...values);
    const ymax = Math.ceil(vmax * 20 + 0.6) / 20;
    const ticks = [];
    for (let v = 0; v <= ymax + 1e-9; v += 0.05) ticks.push(Math.round(v * 100) / 100);
    const fr = frame(label, values.length, ymax, ticks, (v) => v.toFixed(2));
    let s = fr.s;
    values.forEach((v, i) => {
      const k = i + first, bw = Math.max(fr.slot * 0.68, 1);
      const cls = highlight.includes(k) ? "by-enum" : "by-multiples";
      s += `<rect class="bar ${cls}" x="${f(fr.cx(i + 1) - bw / 2)}" y="${f(fr.Y(v))}" width="${f(bw)}" ` +
           `height="${f(BASE - fr.Y(v))}"><title>${titleOf(k, v)}</title></rect>`;
      const nearPeak = highlight.some((h) => h !== k && Math.abs(h - k) < fr.every);
      if (highlight.includes(k) || (!nearPeak && (k % fr.every === 0 || i === 0))) s += fr.xtick(i + 1, k);
    });
    return s + fr.close();
  };

  const cakeView = (kind0) => ({
    mount(box) {
      const d = box.dataset;
      // slider ranges [min, max, step]; the number field beside each slider takes any value
      // within LIM (a tiny a, a negative d, q below 1)
      const SL = { arith: { a: [0.0001, 0.6, 0.0001], step: [-0.2, 0.8, 0.01], name: "ההפרש d", law: "החשבוני" },
                   geo: { a: [0.0001, 0.6, 0.0001], step: [0.5, 3, 0.05], name: "המנה q", law: "ההנדסי" } };
      const LIM = { a: [0.0001, 1], arith: [-1, 1], geo: [0.1, 10] };
      const WIN = 200;   // people in the charts and the table at once
      const defaults = { kind: kind0, a: Number(d.a || 0.01), step: { arith: 0.1, geo: 1.5 } };
      defaults.step[kind0] = Number(d.step || defaults.step[kind0]);
      const st = { kind: kind0, a: defaults.a, step: { ...defaults.step }, shown: 1 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>החוק <select class="ex-kind"><option value="arith">חשבוני, ‏p = a + (k − 1)d</option><option value="geo">הנדסי, ‏p = a · q^(k − 1)</option></select></label>` +
        `<label><span>השבר הראשון a</span><input type="range" class="ex-a" dir="ltr"><input type="number" class="ex-num num-a" dir="ltr" step="any" aria-label="השבר הראשון a, ערך מדויק"></label>` +
        `<label><span class="step-name"></span><input type="range" class="ex-step" dir="ltr"><input type="number" class="ex-num num-step" dir="ltr" step="any" aria-label="ערך מדויק"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">האדם הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">האדם הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 700, 250) +
        `<button type="button" class="md-button ex-all">כולם</button>` +
        `<span class="ex-pos"></span></div>` +
        `<div class="cake-box"><div class="cake-pie"></div><div class="cake-panel"><p class="cake-now"></p><div class="cake-scroll"><table class="cake-table"><thead><tr><th>האדם</th><th>השבר</th><th>נשאר לפניו</th><th>מקבל</th></tr></thead><tbody></tbody></table></div></div></div>` +
        `<p class="ex-summary" aria-live="polite"></p><p class="ex-note cake-note"></p><div class="cake-charts"></div>` +
        `<section class="ex-proof cake-proof"><p class="ex-proof-title">שלב ההוכחה : הסף שבו נקבעת הפסגה</p>` +
        `<div class="cake-proof-chart"></div><span class="viz-legend cake-proof-legend"></span><p class="cake-proof-text"></p></section>`;
      const $ = (sel) => box.querySelector(sel);
      const kindSel = $(".ex-kind"), aIn = $(".ex-a"), stepIn = $(".ex-step"), pie = $(".cake-pie"), charts = $(".cake-charts");
      const numA = $(".num-a"), numStep = $(".num-step");
      const play = $(".ex-play");
      let timer = null;
      const setSliders = () => {
        const sl = SL[st.kind];
        [aIn.min, aIn.max, aIn.step] = sl.a; [stepIn.min, stepIn.max, stepIn.step] = sl.step;
        [numA.min, numA.max] = LIM.a; [numStep.min, numStep.max] = LIM[st.kind];
        aIn.value = st.a; stepIn.value = st.step[st.kind];
        numA.value = st.a; numStep.value = st.step[st.kind];
        $(".step-name").textContent = sl.name;
        kindSel.value = st.kind;
      };
      const rowsOf = (kind) => cakeSplit(kind, st.a, st.step[kind]);
      // the window of people drawn: the first WIN, or WIN around the peak when it is further
      const windowOf = (rows, peak) => {
        const n = rows.length;
        if (n <= WIN) return [1, n];
        const lo = peak <= WIN - 20 ? 1 : Math.min(peak - 100, n - WIN + 1);
        return [lo, lo + WIN - 1];
      };
      const pd = () => (st.a < 0.001 ? 5 : 3);   // decimals of the fractions
      const pieSvg = (rows, peak) => {
        const C = 110, R = 92;
        const pt = (turn, r = R) => [C + r * Math.sin(2 * Math.PI * turn), C - r * Math.cos(2 * Math.PI * turn)];
        let s = `<svg class="figure cake-live" viewBox="0 0 220 220" role="img" aria-label="העוגה עם הפרוסות של האנשים שכבר חתכו">` +
                `<circle class="cake-rest" cx="${C}" cy="${C}" r="${R}"/>`;
        let c = 0;
        const slice = (from, to, cls, title, label) => {
          const [x0, y0] = pt(from), [x1, y1] = pt(to);
          const big = to - from > 0.5 ? 1 : 0;
          const path = to - from >= 1 - 1e-9 ? `M${C},${C - R} A${R},${R} 0 1 1 ${C - 0.01},${C - R} Z`
            : `M${C},${C} L${f(x0, 2)},${f(y0, 2)} A${R},${R} 0 ${big} 1 ${f(x1, 2)},${f(y1, 2)} Z`;
          s += `<path class="${cls}" d="${path}"><title>${title}</title></path>`;
          if (label && to - from > 0.045) {
            const [tx, ty] = pt((from + to) / 2, R * 0.68);
            s += `<text class="st-text" x="${f(tx)}" y="${f(ty + 5)}" text-anchor="middle" style="fill:var(--md-default-bg-color)">${label}</text>`;
          }
        };
        // slices below a thousandth of the cake are not visible one by one: a run of them is one region
        let tiny = null;
        const flushTiny = () => { if (tiny) slice(tiny.from, c, "cake-tiny", `אנשים ${tiny.k0} עד ${tiny.k1} : יחד ${fmt(c - tiny.from, 4)} מהעוגה`); tiny = null; };
        rows.slice(0, st.shown).forEach((r) => {
          const from = c, to = Math.min(c + r.S, 1);
          c = to;
          if (r.S < 0.001 && !peak.includes(r.k)) { if (tiny) tiny.k1 = r.k; else tiny = { from, k0: r.k, k1: r.k }; return; }
          flushTiny();
          const cls = peak.includes(r.k) ? "cake-peak" : r.k % 2 ? "cake-slice" : "cake-slice2";
          slice(from, to, cls + (r.k === st.shown ? " is-now" : ""), `אדם ${r.k} : p = ${fmt(r.p, pd())}, S = ${fmt(r.S, pd() + 1)}`, r.k);
        });
        flushTiny();
        s += `<circle class="cake-edge" cx="${C}" cy="${C}" r="${R}" fill="none"/>`;
        return s + "</svg>";
      };
      // the proof panel: the condition curve, the level line, the threshold T and the people
      // seen so far as dots on the curve (before the peak, the peak, after it)
      const proofSvg = (rows, peak, T) => {
        const step = st.step[st.kind], arith = st.kind === "arith";
        const g = (p) => cakeCondition(st.kind, step, p).g;
        const xmax = arith ? Math.min(0.95, Math.ceil(T * 20 - 1e-9) / 10) : 1, ymax = arith ? g(xmax) : step;
        const X = (p) => X0 + (p / xmax) * (W - X0 - RIGHT), Y = (v) => BASE - (Math.min(v, ymax) / ymax) * (BASE - TOP);
        const ys = [0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1, 2].find((u) => ymax / u <= 6) || 5, yt = [];
        for (let v = 0; v <= ymax + 1e-9; v += ys) yt.push(v);
        const fr = frame(arith ? "הפונקציה f(p) = p² / (1 − p) מול הקו y = d, והשברים של האנשים כנקודות על העקומה" : "הקו y = q (1 − p) מול הקו y = 1, והשברים של האנשים כנקודות עליו", 1, ymax, yt, (v) => fmt(v, ys < 0.1 ? 2 : ys < 1 ? 2 : 0));
        let s = fr.s;
        for (let i = 0; i <= 4; i++) s += `<text class="tick" x="${f(X((i * xmax) / 4))}" y="${BASE + 18}" text-anchor="middle">${fmt((i * xmax) / 4, 2)}</text>`;
        const pts = []; for (let i = 0; i <= 120; i++) { const p = (i / 120) * xmax; pts.push(`${f(X(p))},${f(Y(g(p)))}`); }
        s += `<polyline class="s1-line" points="${pts.join(" ")}" fill="none" stroke-width="2.5"/>` +
             hline(fr, arith ? step : 1, arith ? `y = d = ${fmt(step, 3)}` : "y = 1") +
             `<line class="ink-line" x1="${f(X(T))}" x2="${f(X(T))}" y1="${f(Y(arith ? step : 1))}" y2="${BASE}" stroke-width="1" stroke-dasharray="3 3"/>` +
             `<text class="legend" x="${f(X(T) + 6)}" y="${BASE - 6}">T ≈ ${fmt(T)}</text>`;
        const dots = rows.filter((r) => r.k <= st.shown && r.p < 1 && r.p <= xmax);
        let lastX = -1e9;                                // a number only where it does not touch the previous one
        dots.forEach((r) => {
          const big = r.k === peak[0], cls = big ? "s2" : r.k < peak[0] ? "s1" : "ink";
          s += `<circle class="${cls}-dot" cx="${f(X(r.p))}" cy="${f(Y(g(r.p)))}" r="${big ? 6 : 4.5}"><title>p(${r.k}) = ${fmt(r.p, 4)}</title></circle>`;
          if (big || X(r.p) - lastX >= 16) { s += `<text class="tick" x="${f(X(r.p))}" y="${f(Y(g(r.p)) - 9)}" text-anchor="middle">${r.k}</text>`; lastX = X(r.p); }
        });
        return { svg: s + fr.close(), off: rows.filter((r) => r.k <= st.shown && r.p < 1 && r.p > xmax).length };
      };
      const drawProof = (rows, peak, T, grows) => {
        const arith = st.kind === "arith", step = st.step[st.kind], P = pd();
        const chartBox = $(".cake-proof-chart"), legend = $(".cake-proof-legend"), text = $(".cake-proof-text");
        const cond = `<span class="ex-nowrap">${arith ? ltr("f(p<sub>k</sub>) = p<sub>k</sub>² / (1 − p<sub>k</sub>) < d") : ltr("q (1 − p<sub>k</sub>) > 1")}</span>`;
        if (!grows) {
          chartBox.innerHTML = ""; legend.innerHTML = "";
          text.innerHTML = `האדם הבא מקבל יותר בדיוק כש-${cond}. כש-${ltr(arith ? "d ≤ 0" : "q ≤ 1")} זה לא קורה אף פעם, ולכן החלקים רק יורדים מהאדם הראשון.`;
          return;
        }
        const pr = proofSvg(rows, peak, T);
        chartBox.innerHTML = pr.svg;
        legend.innerHTML = `<span><i class="s1"></i>${ltr(arith ? "f(p) = p² / (1 − p)" : `y = ${fmt(step, 2)} (1 − p)`)}</span><span><i class="ink-dash"></i>הקו ${ltr(arith ? "y = d" : "y = 1")}</span>` +
          `<span><i class="s2"></i>האדם ה-${peak[0]} : הראשון ${arith ? "שמגיע לקו" : "שיורד לקו"}</span><span><i class="ink"></i>אחריו</span>`;
        const side = arith ? "מתחת לקו" : "מעל הקו", other = arith ? "מעליו" : "מתחתיו";
        const before = Math.min(st.shown, peak[0] - 1), tie = peak.length > 1;
        const lead = `האדם הבא מקבל יותר בדיוק כש-${cond}. ${arith ? "העקומה עולה" : "הקו יורד"} והשברים ${ltr("p<sub>k</sub>")} עולים, ולכן הנקודות נעות לאורכו בכיוון אחד בלבד : `;
        text.innerHTML = lead + (st.shown < peak[0]
          ? `עד עכשיו ${ltr(st.shown)} נקודות, כולן ${side}, והחלקים עדיין עולים. הוסיפו אנשים וראו איפה הנקודות עוברות את הקו.`
          : `${ltr(before)} נקודות ${side}, והנקודה של האדם ה-${peak[0]} היא הראשונה ${tie ? `שנוגעת בקו : תיקו עם הבא אחריו` : other}. ` +
            `מכאן הנקודות לא חוזרות, ולכן יש פסגה אחת, אצל האדם ה-${peak[0]}${tie ? ` וה-${peak[1]}` : ""}, עם השבר ${ltr(fmt(rows[peak[0] - 1].p, P))} מול הסף ${ltr(`T ≈ ${fmt(T)}`)}.`) +
          (pr.off ? ` (עוד ${ltr(pr.off)} אנשים מימין לגרף.)` : "");
      };
      const draw = () => {
        const rows = rowsOf(st.kind), n = rows.length, done = cakeDone(rows), step = st.step[st.kind];
        st.shown = Math.min(Math.max(st.shown, 1), n);
        numA.value = st.a; numStep.value = step; aIn.value = st.a; stepIn.value = step;
        const peak = cakeBest(rows), T = cakeThreshold(st.kind, step), fm = cakeFormula(st.kind, st.a, step);
        const grows = st.kind === "arith" ? step > 0 : step > 1;   // the threshold and the formula exist only then
        const seen = rows.slice(0, st.shown), topSeen = Math.max(...seen.map((r) => r.S));
        const peakSeen = seen.filter((r) => Math.abs(r.S - topSeen) <= EPS * topSeen).map((r) => r.k);
        const [lo, hi] = windowOf(rows, peak[0]), win = rows.slice(lo - 1, hi), P = pd();
        pie.innerHTML = pieSvg(rows, st.shown >= n ? peak : peakSeen);
        const now = rows[st.shown - 1];
        $(".cake-now").innerHTML = `האדם ה-${now.k} מוצא ${ltr(fmt(now.R, P + 1))} מהעוגה, לוקח ממנה ${ltr(fmt(now.p, P))} ומקבל ${ltr(fmt(now.S, P + 1))}` +
          (now.p >= 1 ? ", את כל מה שנשאר." : `; נשאר ${ltr(fmt(now.R - now.S, P + 1))} לבאים אחריו.`);
        $(".cake-table tbody").innerHTML = win.filter((r) => r.k <= st.shown).map((r) =>
          `<tr${peakSeen.includes(r.k) ? ' class="is-best"' : ""}${r.k === st.shown ? ' data-now="1"' : ""}><td>${ltr(r.k)}</td><td>${ltr(fmt(r.p, P))}</td><td>${ltr(fmt(r.R, P + 1))}</td><td>${ltr(fmt(r.S, P + 1))}</td></tr>`).join("");
        const scroll = $(".cake-scroll"), nowRow = $(".cake-table tr[data-now]");   // keep the current person in view of the scrolling table
        if (nowRow) scroll.scrollTop = Math.max(0, nowRow.offsetTop - scroll.clientHeight + nowRow.offsetHeight * 2);
        $(".ex-pos").textContent = `אדם ${st.shown} מתוך ${n}`;
        $(".ex-prev").disabled = st.shown <= 1; $(".ex-next").disabled = st.shown >= n; $(".ex-all").disabled = st.shown >= n;
        const who = peak.length > 1 ? `תיקו בין האדם ה-${peak[0]} לאדם ה-${peak[1]}` : `האדם ה-${peak[0]}`;
        const other = st.kind === "arith" ? "geo" : "arith";
        const orows = rowsOf(other), opeak = cakeBest(orows);
        const agree = fm.k === peak[0] && fm.tie === (peak.length > 1);
        const last = rows[n - 1], left = last.R - last.S;
        const ending = done ? `מתוך ${n} אנשים. `
          : n >= CAKE_MAX ? `העוגה לא נגמרת : השברים לא עולים, ואחרי ${ltr(CAKE_MAX)} אנשים עדיין נשאר ${ltr(fmt(left, P + 1))} ממנה. `
          : `השברים מתכווצים : מהאדם ה-${n + 1} השבר כבר אפסי (קטן מ-${ltr("10⁻⁹")}) או שלילי, ו-${ltr(fmt(left, P + 1))} מהעוגה נשאר בלי לוקח. `;
        const threshold = grows
          ? `הסף הוא ${ltr(`T ≈ ${fmt(T)}`)}, והנוסחה נותנת את האדם ה-${fm.k}${fm.tie ? " (תיקו עם הבא)" : ""}${agree ? ", בדיוק כמו בעמודות." : ", שלא כמו בעמודות."} `
          : `אין סף : כשהשברים לא עולים (${ltr(st.kind === "arith" ? "d ≤ 0" : "q ≤ 1")}) גם השבר וגם מה שנשאר רק קטנים, ולכן האדם הראשון מקבל הכי הרבה. `;
        summary.innerHTML = `בחוק ${SL[st.kind].law} : המקבל הגדול הוא ${who}, עם ${ltr(fmt(rows[peak[0] - 1].S, P + 1))} מהעוגה, ${ending}` + threshold +
          `להשוואה, בחוק ${SL[other].law} עם אותו ${ltr("a")} ו-${ltr(`${SL[other].name.split(" ")[1]} = ${st.step[other]}`)} : האדם ה-${opeak[0]} עם ${ltr(fmt(orows[opeak[0] - 1].S, P + 1))}, מתוך ${orows.length}.`;
        $(".cake-note").textContent = n > WIN ? `בטבלה ובגרפים מוצגים האנשים ${lo} עד ${hi} מתוך ${n}, והפסגה ביניהם.` : "";
        const shares = barsChart("החלק של כל אדם", win.map((r) => r.S), peak, (k, v) => `S(${k}) = ${fmt(v, P + 1)}`, lo);
        // bars of people not yet shown are faint
        let i = lo - 1;
        const sharesShown = shares.replace(/<rect class="bar [a-z-]+" /g, (m0) => { i += 1; return i > st.shown ? m0.replace('class="bar', 'fill-opacity="0.22" class="bar') : m0; });
        const fr = frame("השבר של כל אדם מול הסף", win.length, 1, [0, 0.25, 0.5, 0.75, 1]);
        let fs = fr.s + (grows ? hline(fr, T, `T ≈ ${fmt(T)}`) : "");
        win.forEach((r) => {
          const x = r.k - lo + 1;
          const cls = r.k === peak[0] ? "s2" : grows && r.p < T - EPS ? "s1" : "ink";
          const rad = r.k === peak[0] ? 6 : Math.min(4.5, Math.max(1.5, fr.slot * 0.35));
          const dim = r.k > st.shown ? ' opacity="0.25"' : "";
          fs += `<line class="${cls}-line" x1="${f(fr.cx(x))}" x2="${f(fr.cx(x))}" y1="${BASE}" y2="${f(fr.Y(r.p))}" stroke-width="${f(Math.min(2, fr.slot * 0.4))}"${dim}/>` +
                `<circle class="${cls}-dot" cx="${f(fr.cx(x))}" cy="${f(fr.Y(r.p))}" r="${f(rad)}"${dim}><title>p(${r.k}) = ${fmt(r.p, P + 1)}</title></circle>`;
          const nearPeak = r.k !== peak[0] && Math.abs(r.k - peak[0]) < fr.every;
          if (r.k === peak[0] || (!nearPeak && (r.k % fr.every === 0 || x === 1))) fs += fr.xtick(x, r.k);
        });
        drawProof(rows, peak, T, grows);
        charts.innerHTML = `<p class="ex-title">החלק של כל אדם</p>${sharesShown}<p class="ex-title">${grows ? "השבר של כל אדם מול הסף" : "השבר של כל אדם"}</p>${fs + fr.close()}`;
      };
      const summary = $(".ex-summary");
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const go = (k) => { st.shown = k; draw(); };
      $(".ex-next").addEventListener("click", () => { stop(); go(st.shown + 1); });
      $(".ex-prev").addEventListener("click", () => { stop(); go(st.shown - 1); });
      $(".ex-all").addEventListener("click", () => { stop(); go(rowsOf(st.kind).length); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.shown >= rowsOf(st.kind).length) st.shown = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { if (st.shown >= rowsOf(st.kind).length) { stop(); return; } go(st.shown + 1); }, Number($(".ex-speed").value));
        go(st.shown + 1);
      });
      $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      kindSel.addEventListener("change", () => { stop(); st.kind = kindSel.value; st.shown = 1; setSliders(); draw(); });
      const clamp = (v, [lo, hi], fallback) => (Number.isFinite(v) ? Math.min(hi, Math.max(lo, v)) : fallback);
      aIn.addEventListener("input", () => { stop(); st.a = Number(aIn.value); draw(); });
      stepIn.addEventListener("input", () => { stop(); st.step[st.kind] = Number(stepIn.value); draw(); });
      numA.addEventListener("change", () => { stop(); st.a = clamp(Number(numA.value), LIM.a, st.a); draw(); });
      numStep.addEventListener("change", () => { stop(); st.step[st.kind] = clamp(Number(numStep.value), LIM[st.kind], st.step[st.kind]); draw(); });
      [numA, numStep].forEach((el) => el.addEventListener("keydown", (e) => { if (e.key === "Enter") el.blur(); }));
      $(".ex-reset").addEventListener("click", () => { stop(); st.kind = kind0; st.a = defaults.a; st.step = { ...defaults.step }; st.shown = 1; setSliders(); draw(); });
      setSliders();
      draw();
    },
  });

  dvqExplorers.register({
    views: { "cake-arith": () => cakeView("arith"), "cake-geo": () => cakeView("geo") },
    help: {
      "cake-arith": "העוגה מחולקת לפי החוק החשבוני : a הוא החלק הראשון ו-d התוספת לכל אדם. הסליידרים ושדות המספר קובעים אותם, ״הבא״ ו״הפעלה״ עוברים אדם אחרי אדם, והטבלה והגרפים מראים מי מקבל הכי הרבה. שלב ההוכחה מראה כל אדם כנקודה על עקומת התנאי, והפסגה היא הנקודה הראשונה שעוברת את הקו.",
      "cake-geo": "העוגה מחולקת לפי החוק ההנדסי : a הוא החלק הראשון ו-q היחס בין אדם לאדם. הסליידרים ושדות המספר קובעים אותם, ״הבא״ ו״הפעלה״ עוברים אדם אחרי אדם, והטבלה והגרפים מראים מי מקבל הכי הרבה. שלב ההוכחה מראה כל אדם כנקודה על עקומת התנאי, והפסגה היא הנקודה הראשונה שעוברת את הקו.",
    },
    models: { cakeSplit, cakeThreshold, cakeFormula, cakeCondition, cakeBest, CAKE_MAX, cakeDone },
  });
})();
