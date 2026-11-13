// kinds: carfleet
//   carfleet               0109        car fleets on a one-lane road (data-mode fleets or collide, data-target "12", data-pos "10.8.0.5.3", data-speed "2.4.1.1.3"): up to 6 cars typed or picked from presets (LeetCode's example, a meeting at half a second, a chain where a car is absorbed before it is reached) or drawn; a time slider over a grid of 24 steps and every event at its exact time; on top the road at that time (the cars stacked in their fleets), under it the position-time graph (the free lines dashed, the real paths bold, the meetings ringed, the target, a line at the time); beside them part a's table of the lone times from the front with the running maximum and the fleet of every car, or part b's table of the collision times and the car whose free line each one meets
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const MINUS = "−";
  const NMAX = 6, PMAX = 99, SMAX = 20, TMAX = 100, GRID = 24;

  // --- exact numbers: [numerator, denominator], the denominator positive, in lowest terms --------
  const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
  const Q = (n, d = 1) => { if (d < 0) { n = -n; d = -d; } const g = gcd(n, d); return [n / g, d / g]; };
  const cmp = (a, b) => Math.sign(a[0] * b[1] - b[0] * a[1]);
  const qmin = (a, b) => (cmp(a, b) <= 0 ? a : b);
  const qmax = (a, b) => (cmp(a, b) >= 0 ? a : b);
  const at = (p, s, t) => Q(p * t[1] + s * t[0], t[1]);              // p + s t
  const val = (q) => q[0] / q[1];

  // --- the model, as tools/figures/q0109.py ----------------------------------------------------
  // the cars in road order, from the back: [[p, s]]
  const cfRoad = (pos, speed) => pos.map((p, i) => [p, speed[i]]).sort((a, b) => a[0] - b[0]);
  const cfLone = (target, p, s) => Q(target - p, s);
  // the fleets from event to event: every fleet drives on its front car's free line; touch[r]
  // is the time car r touches car r + 1, arrive[r] its arrival (target null: an infinite road)
  const cfSim = (pos, speed, target) => {
    const cars = cfRoad(pos, speed), n = cars.length;
    const touch = Array(n).fill(null), arrive = Array(n).fill(null), events = [];
    let fleets = cars.map((_, r) => [r, r]);
    const line = (f) => cars[f[1]];
    const where = (f, t) => at(line(f)[0], line(f)[1], t);
    while (fleets.length) {
      let t = null;
      const take = (c) => { t = t === null ? c : qmin(t, c); };
      for (let k = 0; k + 1 < fleets.length; k++) {
        const [pa, sa] = line(fleets[k]), [pb, sb] = line(fleets[k + 1]);
        if (sa > sb) {
          const c = Q(pb - pa, sa - sb);
          if (target === null || cmp(at(pa, sa, c), [target, 1]) <= 0) take(c);
        }
      }
      if (target !== null) fleets.forEach((f) => take(cfLone(target, ...line(f))));
      if (t === null) break;
      const merged = [fleets[0]];
      for (const f of fleets.slice(1)) {
        const g = merged[merged.length - 1], x = where(f, t);
        if (cmp(where(g, t), x) === 0) {
          touch[g[1]] = t;
          events.push({ kind: "meet", t, x, a: g[1], b: f[0] });
          merged[merged.length - 1] = [g[0], f[1]];
        } else merged.push(f);
      }
      fleets = merged;
      if (target !== null) {
        const done = fleets.filter((f) => cmp(where(f, t), [target, 1]) === 0);
        done.forEach((f) => {
          const cs = [];
          for (let r = f[0]; r <= f[1]; r++) { arrive[r] = t; cs.push(r); }
          events.push({ kind: "arrive", t, cars: cs });
        });
        fleets = fleets.filter((f) => !done.includes(f));
      }
    }
    return { touch, arrive, events };
  };
  // car r's place at time t: the lowest free line of r and of every car ahead (and the target)
  const cfAt = (pos, speed, target, r, t) => {
    const cars = cfRoad(pos, speed);
    let x = null;
    for (let j = r; j < cars.length; j++) { const y = at(cars[j][0], cars[j][1], t); x = x === null ? y : qmin(x, y); }
    return target === null ? x : qmin(x, [target, 1]);
  };
  // part a, front first: [r, p, s, alone, T, fleet, new]
  const cfFormula = (target, pos, speed) => {
    const cars = cfRoad(pos, speed), rows = [];
    let ahead = [0, 1], count = 0;
    for (let r = cars.length - 1; r >= 0; r--) {
      const [p, s] = cars[r], t = cfLone(target, p, s), isNew = cmp(t, ahead) > 0;
      if (isNew) { count++; ahead = t; }
      rows.push([r, p, s, t, ahead, count, isNew]);
    }
    return { rows, count };
  };
  // part b's stack (road order): the time every car hits the car ahead (null if never) and the
  // car whose free line it meets
  const cfStack = (pos, speed) => {
    const cars = cfRoad(pos, speed), n = cars.length, ans = Array(n).fill(null), on = Array(n).fill(null), stack = [];
    for (let i = n - 1; i >= 0; i--) {
      while (stack.length) {
        const j = stack[stack.length - 1];
        if (cars[i][1] > cars[j][1]) {
          const c = Q(cars[j][0] - cars[i][0], cars[i][1] - cars[j][1]);
          if (ans[j] === null || cmp(c, ans[j]) < 0) { ans[i] = c; on[i] = j; break; }
        }
        stack.pop();
      }
      stack.push(i);
    }
    return { ans, on };
  };
  // the times of the slider: GRID equal steps up to the end, and every event at its own time
  const cfFrames = (end, events) => {
    const ts = [];
    for (let k = 0; k <= GRID; k++) ts.push(Q(end[0] * k, end[1] * GRID));
    events.forEach((e) => { if (cmp(e.t, end) <= 0) ts.push(e.t); });
    ts.sort(cmp);
    return ts.filter((t, k) => k === 0 || cmp(t, ts[k - 1]) !== 0);
  };
  // the end of the slider: the last arrival, or on an infinite road a quarter after the last
  // collision (2 when nobody collides)
  const cfEnd = (sim, target) => {
    const ts = (target === null ? sim.touch : sim.arrive).filter(Boolean);
    if (!ts.length) return [2, 1];
    const last = ts.reduce(qmax);
    return target === null ? Q(5 * last[0], 4 * last[1]) : last;
  };
  // "1, 2, 3", "1.2.3" or "1 2 3": 1 to NMAX whole numbers from lo to hi, else null
  const cfParse = (text, lo = 0, hi = PMAX) => {
    const p = String(text || "").trim().split(/[\s,.;]+/).filter(Boolean);
    if (!p.length || p.length > NMAX || p.some((x) => !/^\d+$/.test(x) || Number(x) < lo || Number(x) > hi)) return null;
    return p.map(Number);
  };
  // why an input is refused, or "" when it is a road: distinct places, a speed per car, the
  // target past every car
  const cfCheck = (target, pos, speed) => {
    if (!pos) return `המקומות : בין 1 ל-${NMAX} מספרים שלמים מ-0 עד ${PMAX}, מופרדים בפסיקים.`;
    if (!speed) return `המהירויות : בין 1 ל-${NMAX} מספרים שלמים מ-1 עד ${SMAX}, מופרדים בפסיקים.`;
    if (new Set(pos).size !== pos.length) return "שתי מכוניות באותו מקום : המקומות צריכים להיות שונים.";
    if (speed.length !== pos.length) return `${pos.length} מקומות ו-${speed.length} מהירויות : צריך מהירות לכל מכונית.`;
    if (target !== null && !(Number.isInteger(target) && target > Math.max(...pos) && target <= TMAX)) return `היעד : מספר שלם אחרי המכונית הקדמית (${Math.max(...pos)}) ועד ${TMAX}.`;
    return "";
  };
  const cfPresets = [
    ["LeetCode 853", 12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]],
    ["מפגש בזמן חצי", 10, [0, 1], [3, 1]],
    ["שרשרת : נבלעת לפני שמשיגים אותה", 12, [3, 5, 6, 9], [4, 4, 3, 1]],
  ];

  // --- drawing ---------------------------------------------------------------------------------
  const fr = (q) => (q[1] === 1 ? (q[0] < 0 ? `${MINUS}${-q[0]}` : String(q[0])) : `${q[0] < 0 ? MINUS : ""}${Math.abs(q[0])}/${q[1]}`);
  const dec = (q) => (q[1] === 1 ? "" : ` ≈ ${(+val(q).toFixed(2)).toString()}`);
  const tt = (q) => ltr(`t = ${fr(q)}${dec(q)}`);
  const f1 = (x) => x.toFixed(1);
  const list = (xs) => xs.join(", ");
  const words = (xs) => (xs.length < 2 ? String(xs[0]) : `${xs.slice(0, -1).join(", ")} ו-${xs[xs.length - 1]}`);
  const nice = (span, most) => [0.25, 0.5, 1, 2, 5, 10, 20, 25, 50, 100, 200].find((s) => span / s <= most) || 500;

  // the road at time t: the cars at their places, a fleet stacked in one column (the front car
  // at the bottom), a column that would touch the one behind it raised above it
  const RW = 640;
  const roadSvg = (v) => {
    const { n, xs, lo, hi, target, col, t } = v;
    const H = 44 + 20 * n, Y = H - 26, X0 = 26, X1 = RW - 30;
    const X = (x) => X0 + ((x - lo) / (hi - lo)) * (X1 - X0);
    let o = `<svg class="figure cf-road cf-live" viewBox="0 0 ${RW} ${H}" direction="ltr" role="img" ` +
      `aria-label="הכביש בזמן ${fr(t)}${NB}: ${xs.map((x, r) => `מכונית ${r} במקום ${fr(x)}`).join(", ")}">` +
      `<line class="cf-lane" x1="${X0 - 12}" x2="${f1(target === null ? X1 + 12 : X(target))}" y1="${Y}" y2="${Y}"/>`;
    const step = nice(hi - lo, 10);
    for (let x = Math.ceil(lo / step) * step; x <= hi + 1e-9; x += step) {
      o += `<line class="cf-tickl" x1="${f1(X(x))}" x2="${f1(X(x))}" y1="${Y - 4}" y2="${Y + 4}"/>` +
        `<text class="tick" x="${f1(X(x))}" y="${Y + 20}" text-anchor="middle">${+x.toFixed(2)}</text>`;
    }
    if (target !== null) o += `<line class="cf-goal" x1="${f1(X(target))}" x2="${f1(X(target))}" y1="${Y - 20 * n - 10}" y2="${Y + 8}"/>` +
      `<path class="cf-flag" d="M${f1(X(target))},${Y - 20 * n - 10} l14,5 l-14,5 Z"/>`;
    // columns: the cars at one place, from the back
    const cols = [];
    xs.forEach((x, r) => {
      const c = cols[cols.length - 1];
      if (c && cmp(c.x, x) === 0) c.cars.push(r); else cols.push({ x, cars: [r] });
    });
    let prevX = -1e9, prevTop = 0;
    cols.forEach((c) => {
      const px = X(val(c.x)), base = px - prevX < 22 ? prevTop : 0;
      [...c.cars].reverse().forEach((r, k) => {
        const cy = Y - 14 - 20 * (base + k);
        const done = target !== null && cmp(c.x, [target, 1]) === 0;
        o += `<g class="cf-car cf-c${col[r] % 6}${done ? " is-done" : ""}"><title>car ${r} at ${fr(c.x)}</title>` +
          `<circle cx="${f1(px)}" cy="${cy}" r="9"/><text x="${f1(px)}" y="${cy + 4}" text-anchor="middle">${r}</text></g>`;
      });
      prevX = px; prevTop = base + c.cars.length;
    });
    return o + "</svg>";
  };

  // the position-time graph: the free lines dashed, the real paths bold (the envelope at its
  // kinks), the meetings ringed (filled once they happened), the target and the time t
  const GW = 640, GH = 300, GX0 = 44, GXR = 16, GTOP = 16, GBASE = 262;
  const graphSvg = (v) => {
    const { cars, n, target, end, lo, hi, col, t, events, stops, byCar, P, S } = v;
    const tmax = val(end) * 1.04;
    const X = (x) => GX0 + (x / tmax) * (GW - GX0 - GXR);
    const Y = (y) => GBASE - ((y - lo) / (hi - lo)) * (GBASE - GTOP);
    let o = `<svg class="perf-chart cf-graph cf-live" viewBox="0 0 ${GW} ${GH}" direction="ltr" role="img" ` +
      `aria-label="המקום מול הזמן${NB}: הקו החופשי של כל מכונית מקווקו והדרך האמיתית שלה מודגשת, והקו האנכי הוא הזמן ${fr(t)}">`;
    const ys = nice(hi - lo, 7), xs = nice(tmax, 12);
    for (let y = Math.ceil(lo / ys) * ys; y <= hi + 1e-9; y += ys) {
      o += `<line class="grid" x1="${GX0}" x2="${GW - GXR}" y1="${f1(Y(y))}" y2="${f1(Y(y))}"/>` +
        `<text class="tick" x="${GX0 - 8}" y="${f1(Y(y) + 4)}" text-anchor="end">${+y.toFixed(2)}</text>`;
    }
    for (let x = 0; x <= tmax + 1e-9; x += xs) o += `<text class="tick" x="${f1(X(x))}" y="${GBASE + 18}" text-anchor="middle">${+x.toFixed(2)}</text>`;
    if (target !== null) o += `<line class="cf-target" x1="${GX0}" x2="${GW - GXR}" y1="${f1(Y(target))}" y2="${f1(Y(target))}"/>`;
    cars.forEach(([p, s], r) => {
      const te = Math.min(target !== null ? (target - p) / s : (hi - p) / s, tmax);
      o += `<line class="cf-free cf-c${col[r] % 6}" x1="${f1(X(0))}" y1="${f1(Y(p))}" x2="${f1(X(te))}" y2="${f1(Y(p + s * te))}"><title>car ${r}: x = ${p} + ${s}t</title></line>`;
    });
    cars.forEach(([p], r) => {
      const stop = stops[r], ts = [[0, 1], stop];
      for (let k = r; k < n; k++) for (let m = k + 1; m < n; m++) {
        if (cars[k][1] === cars[m][1]) continue;
        const c = Q(cars[m][0] - cars[k][0], cars[k][1] - cars[m][1]);
        if (c[0] > 0 && cmp(c, stop) < 0) ts.push(c);
      }
      ts.sort(cmp);
      const pts = ts.map((q) => `${f1(X(val(q)))},${f1(Y(val(cfAt(P, S, target, r, q))))}`).join(" ");
      const w = byCar ? (3 + 1.6 * (n - 1 - r)).toFixed(1) : "3.2";
      o += `<polyline class="cf-path cf-c${col[r] % 6}" points="${pts}" fill="none" stroke-width="${w}"/>`;
      if (byCar) o += `<text class="cf-carno cf-c${r % 6}" x="${f1(X(0) + 9)}" y="${f1(Y(p) - 7)}" text-anchor="middle">${r}</text>`;
    });
    const seen = new Set();
    events.filter((e) => e.kind === "meet").forEach((e) => {
      const key = `${fr(e.t)}:${fr(e.x)}`;
      if (seen.has(key)) return;
      seen.add(key);
      o += `<circle class="cf-meet${cmp(e.t, t) <= 0 ? " is-past" : ""}" cx="${f1(X(val(e.t)))}" cy="${f1(Y(val(e.x)))}" r="5.5"><title>t = ${fr(e.t)}, x = ${fr(e.x)}: car ${e.a} reaches car ${e.b}</title></circle>`;
    });
    o += `<line class="cf-now" x1="${f1(X(val(t)))}" x2="${f1(X(val(t)))}" y1="${GTOP - 6}" y2="${GBASE}"/>`;
    v.xs.forEach((x, r) => { o += `<circle class="cf-dot cf-c${col[r] % 6}" cx="${f1(X(val(t)))}" cy="${f1(Y(val(x)))}" r="4"/>`; });
    o += `<line class="axis" x1="${GX0}" x2="${GW - GXR}" y1="${GBASE}" y2="${GBASE}"/><line class="axis" x1="${GX0}" x2="${GX0}" y1="${GTOP}" y2="${GBASE}"/>`;
    return o + "</svg>";
  };

  // part a's table, front first; part b's table, from the front car back (the stack's order)
  const swatch = (c) => `<i class="cf-sw cf-c${c % 6}" aria-hidden="true"></i>`;
  const tableA = (v) => {
    const { rows, arrive, t, col } = v;
    let o = `<table class="cf-tab"><caption>מהמכונית הקרובה ליעד${NB}: הזמן לבד ${ltr("t")} והמקסימום ${ltr("T")}</caption>` +
      `<thead><tr><th scope="col">מכונית</th><th scope="col">${ltr("p")}</th><th scope="col">${ltr("s")}</th><th scope="col">${ltr("t")} לבד</th><th scope="col">${ltr("T")}</th><th scope="col">השיירה</th></tr></thead><tbody>`;
    let prev = null;
    rows.forEach(([r, p, s, lone, T, k, isNew]) => {
      const inn = cmp(arrive[r], t) <= 0;
      const what = isNew ? "חדשה" : prev && cmp(lone, prev) === 0 ? "ביעד" : "מצטרפת";
      o += `<tr class="cf-row${isNew ? " is-new" : ""}${inn ? " is-in" : ""}"><td>${swatch(col[r])}${r}</td><td>${p}</td><td>${s}</td><td>${ltr(fr(lone))}</td>` +
        `<td>${isNew ? `<b>${ltr(fr(T))}</b>` : ltr(fr(T))}</td><td>${k}, ${what}</td></tr>`;
      prev = T;
    });
    return o + "</tbody></table>";
  };
  const tableB = (v) => {
    const { cars, ans, on, t, col } = v;
    let o = `<table class="cf-tab"><caption>מהמכונית הקדמית אחורה${NB}: מתי כל אחת פוגשת את הדרך של זו שלפניה</caption>` +
      `<thead><tr><th scope="col">מכונית</th><th scope="col">${ltr("p")}</th><th scope="col">${ltr("s")}</th><th scope="col">על הקו של</th><th scope="col">בזמן</th></tr></thead><tbody>`;
    for (let r = cars.length - 1; r >= 0; r--) {
      const hit = ans[r] !== null && cmp(ans[r], t) <= 0;
      o += `<tr class="cf-row${hit ? " is-in" : ""}"><td>${swatch(col[r])}${r}</td><td>${cars[r][0]}</td><td>${cars[r][1]}</td>` +
        `<td>${on[r] === null ? "–" : on[r]}</td><td>${ans[r] === null ? ltr(`${MINUS}1`) : ltr(fr(ans[r]))}</td></tr>`;
    }
    return o + "</tbody></table>";
  };

  const fleetView = () => ({
    mount(box) {
      const mode = box.dataset.mode === "collide" ? "collide" : "fleets";
      const read = (v, lo, hi) => cfParse(String(v || "").split(".").join(", "), lo, hi);
      const p0 = read(box.dataset.pos, 0, PMAX), s0 = read(box.dataset.speed, 1, SMAX), g0 = Number(box.dataset.target);
      const ok0 = p0 && s0 && !cfCheck(mode === "fleets" ? g0 : null, p0, s0);
      const init = ok0 ? { target: g0 || 12, pos: p0, speed: s0 } : { target: cfPresets[0][1], pos: cfPresets[0][2].slice(), speed: cfPresets[0][3].slice() };
      const st = { ...init, pos: init.pos.slice(), speed: init.speed.slice(), k: 0, err: "" };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הכביש <select class="cf-preset" aria-label="איזה כביש">${cfPresets.map(([name], i) => `<option value="${i}">${name}</option>`).join("")}<option value="custom">משלכם</option></select></label>` +
        (mode === "fleets" ? `<label>היעד <input type="number" class="cf-target-f" min="1" max="${TMAX}" step="1" dir="ltr" inputmode="numeric" aria-label="המקום של היעד"></label>` : "") +
        `<label>המקומות <input type="text" class="cf-pos-f" dir="ltr" spellcheck="false" autocomplete="off" aria-label="המקום של כל מכונית, למשל 10, 8, 0"></label>` +
        `<label>המהירויות <input type="text" class="cf-speed-f" dir="ltr" spellcheck="false" autocomplete="off" aria-label="המהירות של כל מכונית, באותו סדר"></label>` +
        `<button type="button" class="md-button cf-rand">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(900, 450, 200) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary cf-sum" aria-live="polite"></p>` +
        `<div class="cf-wrap cf-roadwrap"></div>` +
        `<div class="cf-wrap cf-graphwrap"></div>` +
        `<span class="viz-legend"><span><i class="cf-key-free"></i>הקו החופשי</span><span><i class="cf-key-path"></i>הדרך האמיתית, ${mode === "fleets" ? "בצבע של השיירה" : "בצבע של המכונית"}</span>` +
        `<span><i class="cf-key-meet"></i>מפגש שכבר קרה</span><span><i class="cf-key-now"></i>הזמן של הכביש</span>${mode === "fleets" ? `<span><i class="cf-key-target"></i>היעד</span>` : ""}</span>` +
        `<div class="cf-tabwrap"></div>` +
        `<p class="cf-note"></p>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speedEl = $(".ex-speed");
      const presetOf = () => cfPresets.findIndex(([, g, p, s]) => (mode === "collide" || g === st.target) && p.join() === st.pos.join() && s.join() === st.speed.join());
      const sync = () => {
        const i = presetOf();
        $(".cf-preset").value = i < 0 ? "custom" : String(i);
        if (mode === "fleets") $(".cf-target-f").value = String(st.target);
        $(".cf-pos-f").value = list(st.pos);
        $(".cf-speed-f").value = list(st.speed);
      };
      let v = null;
      const build = () => {               // everything that depends on the input, not on the time
        const target = mode === "fleets" ? st.target : null, P = st.pos, S = st.speed;
        const cars = cfRoad(P, S), n = cars.length, sim = cfSim(P, S, target), end = cfEnd(sim, target);
        const frames = cfFrames(end, sim.events);
        const fa = mode === "fleets" ? cfFormula(target, P, S) : null, sb = mode === "collide" ? cfStack(P, S) : null;
        const col = Array(n).fill(0);
        if (fa) fa.rows.forEach(([r, , , , , k]) => { col[r] = k - 1; }); else col.forEach((_, r) => { col[r] = r; });
        const lo = Math.min(...P), hiQ = cfAt(P, S, target, n - 1, Q(end[0] * 26, end[1] * 25));
        const hi = target !== null ? target : Math.max(val(hiQ), lo + 1);
        const stops = cars.map((_, r) => (target !== null ? sim.arrive[r] : Q(end[0] * 26, end[1] * 25)));
        v = { mode, target, P, S, cars, n, sim, end, frames, fa, sb, col, lo, hi, stops, events: sim.events, byCar: mode === "collide",
          rows: fa ? fa.rows : null, arrive: sim.arrive, ans: sb ? sb.ans : null, on: sb ? sb.on : null };
      };
      const draw = () => {
        const { frames, n, target } = v;
        st.k = Math.min(Math.max(st.k, 0), frames.length - 1);
        const k = st.k, t = frames[k], last = k === frames.length - 1;
        v.t = t;
        v.xs = v.cars.map((_, r) => cfAt(v.P, v.S, target, r, t));
        $(".ex-pos").textContent = `צעד ${k} מתוך ${frames.length - 1}, t = ${fr(t)}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = last;
        $(".cf-roadwrap").innerHTML = roadSvg(v);
        $(".cf-graphwrap").innerHTML = graphSvg(v);
        $(".cf-tabwrap").innerHTML = mode === "fleets" ? tableA(v) : tableB(v);
        // the fleets on the road now, and those already at the target
        const groups = [];
        v.xs.forEach((x, r) => { const g = groups[groups.length - 1]; if (g && cmp(g.x, x) === 0) g.cars.push(r); else groups.push({ x, cars: [r] }); });
        const there = target === null ? [] : groups.filter((g) => cmp(g.x, [target, 1]) === 0);
        const onRoad = groups.length - there.length;
        const arrived = target === null ? 0 : new Set(v.cars.map((_, r) => r).filter((r) => cmp(v.arrive[r], t) <= 0).map((r) => fr(v.arrive[r]))).size;
        $(".cf-sum").innerHTML = `${tt(t)}${NB}: ${onRoad} ${onRoad === 1 ? "שיירה" : "שיירות"} על הכביש` +
          (target === null ? "." : `, ${arrived === 1 ? "שיירה אחת הגיעה" : `${arrived} שיירות הגיעו`} ליעד.`);
        const now = v.events.filter((e) => cmp(e.t, t) === 0);
        const front = (x) => Math.max(...v.xs.map((y, r) => (cmp(y, x) === 0 ? r : -1)));
        let note;
        if (st.err) note = `<span class="cf-err">${st.err}</span>`;
        else if (now.length) {
          // the meetings of this moment by place (several cars that meet at one place are one
          // sentence), then the arrivals
          const places = [];
          now.filter((e) => e.kind === "meet").forEach((e) => { if (!places.some((x) => cmp(x, e.x) === 0)) places.push(e.x); });
          const meets = places.map((x) => {
            const es = now.filter((e) => e.kind === "meet" && cmp(e.x, x) === 0);
            const atTarget = target !== null && cmp(x, [target, 1]) === 0;
            const who = es.length === 1 ? `מכונית ${es[0].a} משיגה את ${es[0].b}`
              : `מכוניות ${words(v.xs.map((y, r) => (cmp(y, x) === 0 ? r : -1)).filter((r) => r >= 0))} נפגשות`;
            return atTarget ? `${who} בדיוק ביעד${NB}: ${es.length === 1 ? "הן מגיעות" : "כולן מגיעות"} יחד, שיירה אחת.`
              : `${who} במקום ${ltr(fr(x))}, ומעכשיו ${es.length === 1 ? "נוסעת" : "הן נוסעות"} במהירות ${v.cars[front(x)][1]}, של מכונית ${front(x)} שבראש השיירה.`;
          });
          const arrivals = now.filter((e) => e.kind === "arrive").map((e) =>
            `${e.cars.length === 1 ? `מכונית ${e.cars[0]} מגיעה ליעד` : `השיירה של ${words(e.cars)} מגיעה ליעד`}${NB}: ${ltr(`T = ${fr(e.t)}`)}, המקסימום של ${ltr("t")} מהקדמית עד ${e.cars.length === 1 ? "אליה" : `מכונית ${e.cars[0]}`}.`);
          note = [...meets, ...arrivals].join(" ");
        } else if (k === 0) {
          note = mode === "fleets"
            ? `המכוניות ממוספרות לפי הסדר על הכביש, מ-0 מאחור. כל צעד מזיז את הזמן, וגם כל מפגש וכל הגעה הם צעד בזמן המדויק שלהם, שלם או לא.`
            : `אין יעד${NB}: הכביש לא נגמר. המכוניות ממוספרות לפי הסדר על הכביש, מ-0 מאחור, וכל אחת בצבע משלה. הטבלה היא התשובה של המחסנית.`;
        } else {
          note = "בין המפגשים כל שיירה נוסעת על הקו החופשי של המכונית שבראשה. בגרף, הדרך של כל מכונית היא המינימום של הקווים שלה ושל כל מי שלפניה.";
        }
        $(".cf-note").innerHTML = note;
        if (last && !st.err) {
          if (mode === "fleets") {
            const ts = v.fa.rows.filter((row) => row[6]).map((row) => ltr(fr(row[4])));
            answer(box, `${v.fa.count === 1 ? "שיירה אחת מגיעה" : `${v.fa.count} שיירות מגיעות`} ליעד, ${v.fa.count === 1 ? "בזמן" : "בזמנים"} ${words(ts)}.`, ".cf-tabwrap .cf-row.is-new");
          } else {
            answer(box, `זמני ההתנגשות, ממכונית 0${NB}: ${ltr(list(v.ans.map((a) => (a === null ? `${MINUS}1` : fr(a)))))}.`, ".cf-graphwrap .cf-meet");
          }
        } else answer(box, null);
      };
      const stop = autoplay(play, speedEl, { step: () => { st.k++; draw(); }, done: () => st.k >= v.frames.length - 1, restart: () => { st.k = 0; draw(); } });
      const setInput = (target, pos, speed) => {
        st.target = target; st.pos = pos; st.speed = speed; st.err = ""; st.k = 0;
        stop(); sync(); build(); draw();
      };
      $(".cf-preset").addEventListener("change", () => {
        const pr = cfPresets[Number($(".cf-preset").value)];
        if (!pr) return;                  // "your own": the road stays, ready to be typed over
        setInput(pr[1], pr[2].slice(), pr[3].slice());
      });
      const typed = () => {
        const target = mode === "fleets" ? Number($(".cf-target-f").value) : null;
        const pos = cfParse($(".cf-pos-f").value, 0, PMAX), speed = cfParse($(".cf-speed-f").value, 1, SMAX);
        const why = cfCheck(target, pos, speed);
        if (why) { stop(); st.err = why; st.k = 0; draw(); return; }
        setInput(mode === "fleets" ? target : st.target, pos, speed);
      };
      box.querySelectorAll(".cf-pos-f, .cf-speed-f, .cf-target-f").forEach((el) => el.addEventListener("change", typed));
      $(".cf-rand").addEventListener("click", () => {
        const n = 3 + Math.floor(Math.random() * 4), target = 12 + Math.floor(Math.random() * 9);
        const spots = Array.from({ length: target }, (_, i) => i);
        for (let i = spots.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [spots[i], spots[j]] = [spots[j], spots[i]]; }
        setInput(target, spots.slice(0, n), Array.from({ length: n }, () => 1 + Math.floor(Math.random() * 5)));
      });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = v.frames.length - 1; draw(); });
      $(".ex-reset").addEventListener("click", () => setInput(init.target, init.pos.slice(), init.speed.slice()));
      sync(); build(); draw();
    },
  });

  dvqExplorers.register({
    views: { carfleet: fleetView },
    help: {
      carfleet: "בוחרים כביש או כותבים את המקומות ואת המהירויות של עד 6 מכוניות (ובסעיף א גם את היעד). הפס מתחת לכפתורים הוא הזמן : 24 צעדים שווים עד הסוף, ועוד צעד לכל מפגש ולכל הגעה ליעד, בזמן המדויק שלו. למעלה הכביש באותו זמן, ומכוניות באותו מקום הן שיירה אחת, בעמודה. מתחת המקום מול הזמן : הקו החופשי של כל מכונית מקווקו, הדרך האמיתית מודגשת, ומפגש מסומן בעיגול. בצד הטבלה של הסעיף : בסעיף א הזמן לבד והמקסימום מהקדמית, ובסעיף ב מתי כל מכונית פוגשת את הדרך של זו שלפניה.",
    },
    cols: { carfleet: { main: ".cf-roadwrap, .cf-graphwrap, .viz-legend", side: ".cf-tabwrap, .cf-note" } },   // the road, the graph and the legend beside the table and the step's note
    models: { cfRoad, cfLone, cfSim, cfAt, cfFormula, cfStack, cfFrames, cfEnd, cfParse, cfCheck, cfPresets },
  });
})();
