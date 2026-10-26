// kinds: motorcycle
//   motorcycle             0026        sliders t0 and t1, a strategy, and play: the travellers on the road and the chart; 1 to 5 riders, a km field, a second plan dashed; the proof panel: the drop point D against both arrival times
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { EPS, f, fmt, ltr } = dvqExplorers.lib;

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
  // The three strategies as motion: positions on the road (0 is A, 1 is B) at time t, in
  // units of AB = 1 and t1 = 1 (the walker moves at 1 / alpha). "wait": the walker waits at
  // A; "meanwhile": he walks and the returning motorcycle meets him; "optimal": the plan.
  const motorcyclePhases = (strategy, alpha) => {
    if (strategy === "wait") return { t1: 1, t2: 2, T: 3 };
    if (strategy === "meanwhile") {
      const tm = (2 * alpha) / (alpha + 1);
      return { t1: 1, t2: tm, T: (3 * alpha - 1) / (alpha + 1) };
    }
    const pl = motorcyclePlan(alpha);
    return { t1: pl.t1, t2: pl.t2, T: pl.T };
  };
  // [motorcycle, passenger, walker] positions at time t.
  const motorcyclePositions = (strategy, alpha, t) => {
    const ph = motorcyclePhases(strategy, alpha);
    t = Math.min(Math.max(t, 0), ph.T);
    if (strategy === "wait") {
      const bike = t <= 1 ? t : t <= 2 ? 2 - t : t - 2;
      return [bike, Math.min(t, 1), t <= 2 ? 0 : t - 2];
    }
    if (strategy === "meanwhile") {
      const m = 2 / (alpha + 1);
      const bike = t <= 1 ? t : t <= ph.t2 ? 2 - t : m + (t - ph.t2);
      return [bike, Math.min(t, 1), t <= ph.t2 ? t / alpha : m + (t - ph.t2)];
    }
    const pl = motorcyclePlan(alpha);
    const bike = t <= pl.t1 ? t : t <= pl.t2 ? pl.D - (t - pl.t1) : pl.C + (t - pl.t2);
    const pass = t <= pl.t1 ? t : Math.min(pl.D + (t - pl.t1) / alpha, 1);
    const walk = t <= pl.t2 ? t / alpha : pl.C + (t - pl.t2);
    return [bike, pass, walk];
  };

  // The follow-up with k people needing a ride (one driver): the three strategies as
  // knots [time, position] per traveller, in units of AB = 1 and t1 = 1. "optimal" is the
  // symmetric shuttle (every rider rides the same stretch, nobody waits, all arrive
  // together at ((2k - 1) alpha + 1) / (alpha + 2k - 1)); "wait": the riders wait at A and
  // are driven one by one; "meanwhile": they walk and the returning motorcycle picks
  // them up one by one and drives each to B. motorcycleAt interpolates the positions.
  const motorcycleRiders = (strategy, alpha, k) => {
    const a = alpha, bike = [[0, 0]], riders = Array.from({ length: k }, () => [[0, 0]]);
    const meet = (bikePos, walker, t) => t + (bikePos - walker) / (1 + 1 / a);   // the time the returning motorcycle meets the walking group
    let t = 0, T;
    if (strategy === "wait") {
      for (let i = 0; i < k; i++) {
        riders[i].push([t, 0], [t + 1, 1]);
        bike.push([t + 1, 1]);
        if (i < k - 1) bike.push([t + 2, 0]);
        t += i < k - 1 ? 2 : 1;
      }
      T = t;
    } else if (strategy === "meanwhile") {
      for (let i = 0; i < k; i++) {
        const P = t / a;                             // the group walks from A at 1 / alpha
        riders[i].push([t, P], [t + 1 - P, 1]);
        bike.push([t + 1 - P, 1]);
        const tb = t + 1 - P;
        if (i < k - 1) { const tm = meet(1, tb / a, tb); bike.push([tm, tm / a]); t = tm; } else t = tb;
      }
      T = t;
    } else {
      const ride = (a + 1) / (a + 2 * k - 1);
      for (let i = 0; i < k; i++) {
        const P = t / a, D = P + ride, q = t + ride;
        riders[i].push([t, P], [q, D]);
        bike.push([q, D]);
        if (i < k - 1) { const tm = meet(D, q / a, q); bike.push([tm, tm / a]); t = tm; } else t = q;
      }
      T = t;
      riders.forEach((r) => { const [q, D] = r[r.length - 1]; if (D < 1 - 1e-12) r.push([q + (1 - D) * a, 1]); });
    }
    riders.forEach((r) => { if (r[r.length - 1][0] < T - 1e-12) r.push([T, r[r.length - 1][1]]); });
    const times = [...new Set([...bike, ...riders.flat()].map(([u]) => Math.round(u * 1e9) / 1e9))].sort((u, v) => u - v);
    return { T, bike, riders, times, ride: strategy === "optimal" ? (a + 1) / (a + 2 * k - 1) : null };
  };
  const motorcycleInterp = (knots, t) => {
    if (t <= knots[0][0]) return knots[0][1];
    for (let i = 1; i < knots.length; i++) {
      const [t0, x0] = knots[i - 1], [t1, x1] = knots[i];
      if (t <= t1 + 1e-12) return t1 - t0 < 1e-12 ? x1 : x0 + ((t - t0) / (t1 - t0)) * (x1 - x0);
    }
    return knots[knots.length - 1][1];
  };
  const motorcycleAt = (plan, t) => [motorcycleInterp(plan.bike, t), ...plan.riders.map((r) => motorcycleInterp(r, t))];
  const motorcycleTimeK = (alpha, k) => ((2 * k - 1) * alpha + 1) / (alpha + 2 * k - 1);
  // The drop point of the proof (two need a ride): the passenger rides to d and walks on,
  // the motorcycle rides back to meet the walker, who left A at time 0, and drives him to
  // B. Both arrival times are linear in d, the passenger's falling and the walker's rising,
  // so the latest of the two is smallest where they are equal: the plan's D.
  const motorcycleDrop = (alpha, d) => {
    const meet = d + (d - d / alpha) / (1 + 1 / alpha), C = meet / alpha;
    const passenger = d + (1 - d) * alpha, walker = meet + (1 - C);
    return { meet, C, passenger, walker, T: Math.max(passenger, walker) };
  };

  // Josephus (0016): person 0 stays, the next L - 1 leave, and so on around.
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
  const motorcycleView = () => ({
    mount(box) {
      const defaults = { t0: Number(box.dataset.t0 || 13), t1: Number(box.dataset.t1 || 1), k: 2, km: null, cmp: "none" };
      const st = { ...defaults, strategy: "optimal", t: 0, drop: null };   // drop: the proof's D, null = the plan's
      const NAMES = { wait: "הנוסעים מחכים ב-A", meanwhile: "הנוסעים הולכים בינתיים", optimal: "הנוסעים יורדים בדרך" };
      const NAMES2 = { wait: "השני מחכה ב-A", meanwhile: "השני הולך בינתיים", optimal: "הנוסע יורד בדרך" };
      const CLS = ["s1", "s2", "s3", "s4", "s5"];
      const name = (s) => (st.k === 2 ? NAMES2[s] : NAMES[s]);
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>הליכה של כל הדרך t0 (שעות)</span><input type="range" class="ex-t0" min="2" max="30" step="1" value="${st.t0}" dir="ltr"><output class="out-t0"></output></label>` +
        `<label><span>נסיעה של כל הדרך t1 (שעות)</span><input type="range" class="ex-t1" min="0.5" max="3" step="0.5" value="${st.t1}" dir="ltr"><output class="out-t1"></output></label>` +
        `<label><span>כמה צריכים הסעה</span><input type="range" class="ex-k" min="1" max="5" step="1" value="2" dir="ltr" aria-label="כמה אנשים צריכים הסעה"><output class="out-k">2</output></label>` +
        `<label>המרחק AB (ק"מ, ריק = בלי יחידות) <input type="number" class="ex-num ex-km" min="1" max="10000" step="any" dir="ltr" placeholder="–" aria-label="המרחק מ-A ל-B בקילומטרים"></label>` +
        `<label>התוכנית <select class="ex-strategy">` + Object.keys(NAMES).map((k) => `<option value="${k}"${k === "optimal" ? " selected" : ""}>${NAMES2[k]}</option>`).join("") + `</select></label>` +
        `<label>להשוואה עם <select class="ex-cmp" aria-label="תוכנית שנייה על הגרף"><option value="none">ללא</option>` + Object.keys(NAMES).map((k) => `<option value="${k}">${NAMES2[k]}</option>`).join("") + `</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="0.25">רבע שעה בשנייה</option><option value="0.5" selected>חצי שעה בשנייה</option><option value="1">שעה בשנייה</option><option value="2">שעתיים בשנייה</option></select></label>` +
        `<label class="ex-scrub"><span>הזמן</span><input type="range" class="ex-t" min="0" max="1" step="0.001" value="0" dir="ltr"><output class="out-t" dir="ltr"></output></label></div>` +
        `<div class="road-box"></div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<p class="ex-title road-title"></p><div class="road-chart"></div>` +
        `<span class="viz-legend road-legend"></span>` +
        `<section class="ex-proof road-proof"><p class="ex-proof-title">שלב ההוכחה : למה הנוסע יורד דווקא ב-D</p>` +
        `<div class="ex-controls"><label><span>נקודת הירידה D</span><input type="range" class="ex-drop" min="0" max="1" step="0.005" value="0.875" dir="ltr" aria-label="נקודת הירידה של הנוסע, חלק מהדרך"><output class="out-drop"></output></label>` +
        `<button type="button" class="md-button ex-drop-best">ה-D של התוכנית</button></div>` +
        `<p class="ex-title road-drop-title"></p><div class="road-drop"></div>` +
        `<span class="viz-legend"><span><i class="s1"></i>הנוסע מגיע</span><span><i class="s2"></i>ההולך מגיע</span><span><i class="ink" style="opacity:0.35"></i>כולם מגיעים : המאוחר מהשניים</span></span>` +
        `<p class="road-drop-text"></p></section>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), scrub = $(".ex-t"), summary = $(".ex-summary");
      const road = $(".road-box"), chart = $(".road-chart"), strategy = $(".ex-strategy"), cmpSel = $(".ex-cmp");
      let running = false, last = 0;
      const alpha = () => st.t0 / st.t1;
      const planOf = (s) => motorcycleRiders(s, alpha(), st.k);
      const plan = () => planOf(st.strategy);
      const who = (i) => (i === 0 ? "האופנוע" : st.k === 1 ? "הנוסע" : st.k === 2 ? ["הנוסע", "ההולך"][i - 1] : `נוסע ${i}`);
      const dist = (v) => (st.km === null ? fmt(v, 2) : `${fmt(v * st.km, 1)} ק"מ`);
      const roadSvg = (pos, pl) => {
        const w = 640, h = 96, x0 = 36, x1 = 604, yr = 58;
        const X = (v) => x0 + v * (x1 - x0);
        let s = `<svg class="figure road-live" viewBox="0 0 ${w} ${h}" role="img" aria-label="הדרך מ-A ל-B עם האופנוע והנוסעים במקומם בזמן הנוכחי">` +
          `<line class="axis-c" x1="${x0}" x2="${x1}" y1="${yr}" y2="${yr}" stroke-width="3"/>` +
          `<text class="legend" x="${x0 - 18}" y="${yr + 5}" text-anchor="middle">A</text><text class="legend" x="${x1 + 18}" y="${yr + 5}" text-anchor="middle">B</text>`;   // beside the road, clear of the travellers
        const marks = [];
        if (st.strategy === "optimal" && st.k === 2) {
          const p2 = motorcyclePlan(alpha());
          marks.push(["Q", p2.Q], ["C", p2.C], ["D", p2.D], ["E", p2.E]);
        } else if (st.strategy === "meanwhile" && st.k === 2) marks.push(["M", 2 / (alpha() + 1)]);
        else if (st.strategy !== "wait") pl.riders.forEach((r, i) => { if (r[1][1] > 1e-9) marks.push([`P${i + 1}`, r[1][1]]); if (r[2] && r[2][1] < 1 - 1e-9) marks.push([`D${i + 1}`, r[2][1]]); });
        marks.forEach(([n, v]) => {
          s += `<line class="grid" x1="${f(X(v))}" x2="${f(X(v))}" y1="${yr - 8}" y2="${yr + 8}" stroke-width="1.5"/>` +
               `<text class="tick" x="${f(X(v))}" y="${yr + 24}" text-anchor="middle">${n}</text>`;
        });
        const bike = pos[0];
        s += `<circle class="ink-dot" cx="${f(X(bike))}" cy="${yr}" r="9" fill-opacity="0.45"><title>האופנוע : ${dist(bike)}</title></circle>`;
        pos.slice(1).forEach((v, i) => {
          const onBike = Math.abs(v - bike) < 1e-9, side = i % 2 ? 1 : -1, lift = onBike ? (14 + 8 * Math.floor(i / 2)) * side : 0;
          s += `<circle class="${CLS[i]}-dot" cx="${f(X(v))}" cy="${f(yr + lift)}" r="6"><title>${who(i + 1)} : ${dist(v)}${onBike ? " (על האופנוע)" : ""}</title></circle>`;
        });
        return s + "</svg>";
      };
      const chartSvg = (pl, pos, other) => {
        const w = 640, h = 280, x0 = 52, right = 24, top = 30, base = 246;
        const Tmax = Math.max(pl.T, other ? other.T : 0);
        const X = (t) => x0 + (t / Tmax) * (w - x0 - right);
        const Y = (v) => base - v * (base - top);
        let s = `<svg class="perf-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="המקום של האופנוע ושל הנוסעים לאורך הזמן, עד הזמן הנוכחי${other ? ", והתוכנית להשוואה מקווקות" : ""}">`;
        const yt = [[0, "0"], [1, st.km === null ? "1" : `${st.km}`]];
        if (st.strategy === "optimal" && st.k === 2) { const p2 = motorcyclePlan(alpha()); yt.push([p2.C, dist(p2.C)], [p2.D, dist(p2.D)]); }
        if (st.strategy === "meanwhile" && st.k === 2) yt.push([2 / (alpha() + 1), dist(2 / (alpha() + 1))]);
        yt.forEach(([v, lab]) => {
          s += `<line class="grid" x1="${x0}" x2="${w - right}" y1="${f(Y(v))}" y2="${f(Y(v))}"/>` +
               `<text class="tick" x="${x0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${lab}</text>`;
        });
        // the knots as ticks when they are few; whole hours otherwise
        const xt = pl.times.length <= 8 ? pl.times : Array.from({ length: Math.floor(Tmax * st.t1) + 1 }, (_, h) => h / st.t1).filter((t) => Math.abs(t - pl.T) * st.t1 > 0.4).concat([pl.T]);
        xt.forEach((t) => {
          s += `<line class="grid" x1="${f(X(t))}" x2="${f(X(t))}" y1="${top - 6}" y2="${base}" stroke-dasharray="4 4"/>` +
               `<text class="tick" x="${f(X(t))}" y="${base + 18}" text-anchor="middle">${fmt(t * st.t1, 2)}</text>`;
        });
        const poly = (knots, cls, width, upTo, extra = "") => {
          const ts = knots.map(([u]) => u).filter((u) => u < upTo - 1e-12).concat([upTo]);
          const pts = ts.map((u) => `${f(X(u))},${f(Y(motorcycleInterp(knots, u)))}`).join(" ");
          return `<polyline class="${cls}" points="${pts}" fill="none" stroke-width="${width}" stroke-linejoin="round"${extra}/>`;
        };
        if (other) {
          s += poly(other.bike, "ink-line", 4, other.T, ' stroke-opacity="0.35" stroke-dasharray="7 5"');
          other.riders.forEach((r, i) => { s += poly(r, `${CLS[i]}-line`, 2, other.T, ' stroke-opacity="0.7" stroke-dasharray="7 5"'); });
          s += `<line class="ink-line" x1="${f(X(other.T))}" x2="${f(X(other.T))}" y1="${top - 6}" y2="${base}" stroke-width="1.5" stroke-dasharray="3 3"/>` +
               `<text class="legend" x="${f(X(other.T) - 5)}" y="${base - 8}" text-anchor="end">${fmt(other.T * st.t1, 2)}</text>`;
        }
        s += poly(pl.bike, "ink-line", 7, pl.T, ' stroke-opacity="0.1"');
        pl.riders.forEach((r, i) => { s += poly(r, `${CLS[i]}-line`, 2.5, pl.T, ' stroke-opacity="0.2"'); });
        if (st.t > 0) { s += poly(pl.bike, "ink-line", 7, st.t, ' stroke-opacity="0.28"'); pl.riders.forEach((r, i) => { s += poly(r, `${CLS[i]}-line`, 2.5, st.t); }); }
        s += `<line class="axis-c" x1="${f(X(st.t))}" x2="${f(X(st.t))}" y1="${top - 6}" y2="${base}" stroke-width="1"/>`;
        s += `<circle class="ink-dot" cx="${f(X(st.t))}" cy="${f(Y(pos[0]))}" r="7"/>`;
        pos.slice(1).forEach((v, i) => { s += `<circle class="${CLS[i]}-dot" cx="${f(X(st.t))}" cy="${f(Y(v))}" r="5"/>`; });
        s += `<line class="axis" x1="${x0}" x2="${w - right}" y1="${base}" y2="${base}"/></svg>`;
        return s;
      };
      // the proof panel: both arrival times against the drop point, their maximum, D marked
      const dropSvg = (a, d, best) => {
        const w = 640, h = 240, x0 = 52, right = 24, top = 16, base = 206;
        // the height follows the dragged point, so both of its dots stay on the chart
        const opt = motorcycleDrop(a, best).T, ymax = Math.ceil(Math.max(opt * 1.6, motorcycleDrop(a, 1).T * 1.15, motorcycleDrop(a, d).T * 1.08) * st.t1) / st.t1;
        const X = (v) => x0 + v * (w - x0 - right), Y = (t) => base - (t / ymax) * (base - top);
        // a straight line from d = u0 to d = u1, cut where it leaves the chart at the top
        const seg = (g, u0, u1) => {
          const t0 = g(u0), t1 = g(u1);
          if (t0 > ymax && t1 > ymax) return "";
          const cut = (u, t, uo, to) => (t <= ymax ? [u, t] : [u + ((ymax - t) / (to - t)) * (uo - u), ymax]);
          const [ua, ta] = cut(u0, t0, u1, t1), [ub, tb] = cut(u1, t1, u0, t0);
          return `${f(X(ua))},${f(Y(ta))} ${f(X(ub))},${f(Y(tb))}`;
        };
        const pas = (u) => motorcycleDrop(a, u).passenger, wal = (u) => motorcycleDrop(a, u).walker, both = (u) => motorcycleDrop(a, u).T;
        let s = `<svg class="perf-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="זמן ההגעה של הנוסע ושל ההולך מול נקודת הירידה D : הנוסע מגיע מוקדם יותר ככל ש-D רחוק, ההולך מאוחר יותר, והמאוחר מהשניים הכי קטן כשהם שווים">`;
        const step = ymax * st.t1 <= 6 ? 0.5 : ymax * st.t1 <= 15 ? 1 : 5;
        for (let t = 0; t <= ymax * st.t1 + 1e-9; t += step) {
          s += `<line class="grid" x1="${x0}" x2="${w - right}" y1="${f(Y(t / st.t1))}" y2="${f(Y(t / st.t1))}"/>` +
               `<text class="tick" x="${x0 - 8}" y="${f(Y(t / st.t1) + 4)}" text-anchor="end">${fmt(t, step < 1 ? 1 : 0)}</text>`;
        }
        [0, 0.25, 0.5, 0.75, 1].forEach((v) => { s += `<text class="tick" x="${f(X(v))}" y="${base + 18}" text-anchor="middle">${v === 0 ? "A" : v === 1 ? "B" : fmt(v, 2)}</text>`; });
        const maxPts = [seg(both, 0, best), seg(both, best, 1)].filter(Boolean).join(" ");
        s += `<polyline class="ink-line" points="${maxPts}" fill="none" stroke-width="8" stroke-opacity="0.18" stroke-linejoin="round"/>`;
        s += `<polyline class="s1-line" points="${seg(pas, 0, 1)}" fill="none" stroke-width="2.5"/><polyline class="s2-line" points="${seg(wal, 0, 1)}" fill="none" stroke-width="2.5"/>`;
        s += `<line class="ink-line" x1="${f(X(best))}" x2="${f(X(best))}" y1="${f(Y(opt))}" y2="${base}" stroke-width="1" stroke-dasharray="3 3"/>` +
             `<circle class="ink-dot" cx="${f(X(best))}" cy="${f(Y(opt))}" r="4"><title>המינימום : D = ${fmt(best, 2)}, כולם מגיעים אחרי ${fmt(opt * st.t1, 2)} שעות</title></circle>` +
             `<text class="legend" x="${f(X(best) - 6)}" y="${f(Y(opt) + 18)}" text-anchor="end">${fmt(opt * st.t1, 2)}</text>`;
        const cur = motorcycleDrop(a, d);
        s += `<line class="axis-c" x1="${f(X(d))}" x2="${f(X(d))}" y1="${top}" y2="${base}" stroke-width="1"/>`;
        [["s1", cur.passenger], ["s2", cur.walker]].forEach(([c, t]) => { if (t <= ymax) s += `<circle class="${c}-dot" cx="${f(X(d))}" cy="${f(Y(t))}" r="5.5"/>`; });
        return s + `<line class="axis" x1="${x0}" x2="${w - right}" y1="${base}" y2="${base}"/></svg>`;
      };
      const drawDrop = () => {
        const a = alpha(), panel = $(".road-proof");
        panel.hidden = st.k !== 2 || a <= 1 + EPS;
        if (panel.hidden) return;
        const best = motorcyclePlan(a).D, d = st.drop === null ? best : st.drop;
        $(".ex-drop").value = d;
        $(".out-drop").textContent = fmt(d);
        $(".road-drop-title").textContent = `זמן ההגעה בשעות מול נקודת הירידה D, מ-A עד B${st.km === null ? "" : ` (${st.km} ק"מ)`}`;
        $(".road-drop").innerHTML = dropSvg(a, d, best);
        const cur = motorcycleDrop(a, d), opt = motorcycleDrop(a, best).T, hr = (t) => fmt(t * st.t1, 2);
        const at = Math.abs(d - best) < 1e-9;
        const late = cur.passenger > cur.walker + 1e-9 ? "הנוסע" : "ההולך";
        $(".road-drop-text").innerHTML = (at
          ? `ב-D = ${ltr(dist(best))} הנוסע וההולך מגיעים יחד, אחרי ${hr(opt)} שעות : זה המינימום. `
          : `ב-D = ${ltr(dist(d))} הנוסע מגיע אחרי ${hr(cur.passenger)} שעות וההולך אחרי ${hr(cur.walker)}. ${late} מאחר, ולכן כולם מגיעים אחרי ${hr(cur.T)} שעות, ${hr(cur.T - opt)} יותר מהתוכנית. `) +
          `הזזת D לכיוון B מקצרת את ההליכה של הנוסע, אבל מאריכה את הדרך שהאופנוע חוזר אל ההולך. קו אחד יורד והשני עולה, ולכן המאוחר מהשניים הכי קטן בדיוק כשהם שווים, ב-D = ${ltr(dist(best))}.`;
      };
      const draw = () => {
        drawDrop();
        $(".out-t0").textContent = String(st.t0); $(".out-t1").textContent = String(st.t1); $(".out-k").textContent = String(st.k);
        strategy.querySelectorAll("option").forEach((o) => { o.textContent = name(o.value); });
        cmpSel.querySelectorAll("option").forEach((o) => { if (o.value !== "none") o.textContent = name(o.value); });
        $(".road-title").textContent = st.km === null ? "המקום על הדרך (0 הוא A ו-1 הוא B) מול הזמן בשעות" : `המקום על הדרך בק"מ (0 הוא A ו-${st.km} הוא B) מול הזמן בשעות`;
        $(".road-legend").innerHTML = `<span><i class="ink" style="opacity:0.4"></i>האופנוע</span>` + Array.from({ length: st.k }, (_, i) => `<span><i class="${CLS[i]}"></i>${who(i + 1)}</span>`).join("") +
          (st.cmp !== "none" ? `<span><i class="ink-dash"></i>להשוואה : ${name(st.cmp)}</span>` : "");
        const a = alpha();
        if (a <= 1 + EPS) {
          road.innerHTML = ""; chart.innerHTML = "";
          summary.innerHTML = `יחס המהירויות ${ltr(`α = ${f(a, 2)}`)} : האופנוע לא מהיר מההליכה, ולכן כולם פשוט הולכים, ${fmt(st.t0, 2)} שעות.`;
          return;
        }
        const pl = plan(), other = st.cmp === "none" ? null : planOf(st.cmp);
        st.t = Math.min(st.t, pl.T);
        scrub.max = pl.T; scrub.value = st.t;
        $(".out-t").textContent = `${fmt(st.t * st.t1, 2)} / ${fmt(pl.T * st.t1, 2)} h`;
        const pos = motorcycleAt(pl, st.t);
        road.innerHTML = roadSvg(pos, pl);
        chart.innerHTML = chartSvg(pl, pos, other);
        const T = Object.fromEntries(Object.keys(NAMES).map((s) => [s, planOf(s).T]));
        const people = st.k === 1 ? "שניהם" : st.k === 2 ? "שלושתם" : `כל ${ltr(st.k + 1)}`;
        let text = `יחס המהירויות ${ltr(`α = ${f(a, 2)}`)}${st.k === 2 ? "" : `, ${ltr(st.k)} צריכים הסעה`}. בתוכנית "${name(st.strategy)}" ${people} מגיעים אחרי ${fmt(T[st.strategy] * st.t1, 2)} שעות ` +
          `(להשוואה : ${Object.keys(NAMES).map((s) => `${name(s)} ${fmt(T[s] * st.t1, 2)}`).join(", ")}). `;
        if (st.strategy === "optimal") {
          const ride = pl.ride;
          text += st.k === 2
            ? `הנוסע יורד אחרי ${ltr(dist(motorcyclePlan(a).D))} מהדרך, וכל אחד מהשניים הולך ${ltr(dist(motorcyclePlan(a).y + motorcyclePlan(a).x))} ממנה. `
            : `הנוסחה : ${ltr(`((2n − 1)α + 1) / (α + 2n − 1) · t1 = ${fmt(motorcycleTimeK(a, st.k) * st.t1, 2)}`)} שעות עם ${ltr(`n = ${st.k}`)}; כל נוסע נוסע ${ltr(dist(ride))} והולך ${ltr(dist(1 - ride))}. `;
        }
        if (st.km !== null) text += `מהירויות : הליכה ${ltr(fmt(st.km / st.t0, 1))} קמ"ש, נסיעה ${ltr(fmt(st.km / st.t1, 1))} קמ"ש. `;
        if (other) text += `בתוכנית להשוואה (מקווקו) ${people} מגיעים אחרי ${fmt(other.T * st.t1, 2)} שעות, ${other.T > pl.T ? `${fmt((other.T - pl.T) * st.t1, 2)} שעות יותר` : other.T < pl.T ? `${fmt((pl.T - other.T) * st.t1, 2)} שעות פחות` : "אותו זמן"}. `;
        const seg = pl.times.filter((u) => u <= st.t + 1e-12).length;
        text += `עכשיו (שלב ${ltr(Math.max(1, Math.min(seg, pl.times.length - 1)))}) : ${pos.map((v, i) => `${who(i)} ב-${ltr(dist(v))}`).join(", ")}.`;
        summary.innerHTML = text;
      };
      const stop = () => { running = false; play.textContent = "הפעלה"; summary.setAttribute("aria-live", "polite"); };
      const tick = (now) => {
        if (!running) return;
        const pl = plan();
        st.t = Math.min(st.t + ((now - last) / 1000) * Number(speed.value) / st.t1, pl.T);
        last = now;
        draw();
        if (st.t >= pl.T) stop(); else requestAnimationFrame(tick);
      };
      play.addEventListener("click", () => {
        if (running) { stop(); return; }
        if (alpha() <= 1 + EPS) return;
        if (st.t >= plan().T - 1e-9) st.t = 0;
        running = true;
        play.textContent = "עצירה";
        summary.setAttribute("aria-live", "off");
        last = performance.now();
        requestAnimationFrame(tick);
      });
      scrub.addEventListener("input", () => { stop(); st.t = Number(scrub.value); draw(); });
      ["t0", "t1"].forEach((k) => $(`.ex-${k}`).addEventListener("input", () => { st[k] = Number($(`.ex-${k}`).value); draw(); }));
      $(".ex-k").addEventListener("input", () => { stop(); st.k = Number($(".ex-k").value); st.t = 0; draw(); });
      $(".ex-km").addEventListener("change", () => { const v = Number($(".ex-km").value); st.km = $(".ex-km").value.trim() === "" || !Number.isFinite(v) || v <= 0 ? null : v; $(".ex-km").value = st.km === null ? "" : st.km; draw(); });
      $(".ex-km").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".ex-km").blur(); });
      $(".ex-drop").addEventListener("input", () => { st.drop = Number($(".ex-drop").value); drawDrop(); });
      $(".ex-drop-best").addEventListener("click", () => { st.drop = null; drawDrop(); });
      strategy.addEventListener("change", () => { st.strategy = strategy.value; draw(); });
      cmpSel.addEventListener("change", () => { st.cmp = cmpSel.value; draw(); });
      $(".ex-reset").addEventListener("click", () => {
        stop(); Object.assign(st, defaults, { strategy: "optimal", t: 0, drop: null });
        $(".ex-t0").value = st.t0; $(".ex-t1").value = st.t1; $(".ex-k").value = 2; $(".ex-km").value = ""; strategy.value = "optimal"; cmpSel.value = "none"; draw();
      });
      draw();
    },
  });

  dvqExplorers.register({
    views: { motorcycle: motorcycleView },
    help: {
      motorcycle: "הציור מראה את הנוסעים על הדרך והגרף את מיקומם בזמן. הסליידרים קובעים את מהירויות ההליכה והרכיבה, בורר האסטרטגיה ומספר הרוכבים את התכנית, ״הפעלה״ מריץ אותה, ו״להשוואה עם״ מצייר תכנית שנייה מקווקוות. בשלב ההוכחה מזיזים את נקודת הירידה D ורואים את זמני ההגעה של הנוסע ושל ההולך : המאוחר מהשניים הכי קטן כשהם שווים.",
    },
    models: { motorcyclePlan, motorcycleTime, motorcyclePhases, motorcyclePositions, motorcycleRiders, motorcycleAt, motorcycleTimeK, motorcycleDrop, josephusRun },
  });
})();
