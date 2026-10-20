// Interactive explorers: a box `<div class="explorer" data-kind="..." data-...>` gets
// sliders, a summary line and charts that redraw on every change. One model per kind:
//   cake-arith / cake-geo  0027, 0028  the law, sliders a and d (or q), and a person-by-person stepper of the cake
//   motorcycle             0026        sliders t0 and t1, a strategy, and play: the travellers on the road and the chart
//   josephus               0016, 0022  sliders N (and L), and the circle played step by step; the survivor chart
//   clock                  0029        a clock face to drag, play or type: meetings of the hands so far
//   strip                  0030        drag the spider and the fly on their walls: the periodic strip and the path
//   hourglass              0018, 0019  A, B and D: the plan on a time axis and event by event (BFS or Dijkstra)
//   probability            0015        p, q and C: the answer, the two-children square and the curve against q
// The math of each model is exported under Node, where the question tests compare it with
// the Python reference (tests/0015, 0016, 0018, 0019, 0022, 0026, 0027, 0028, 0029, 0030).
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
  // The elimination step by step: [who stays, [who leave]] per step, and the survivor.
  const josephusSteps = (n, L) => {
    const circle = Array.from({ length: n }, (_, i) => i), steps = [];
    let i = 0;
    while (circle.length > 1) {
      const stays = circle[i], leave = [];
      const count = Math.min(L - 1, circle.length - 1);
      for (let s = 0; s < count; s++) {
        const j = (i + 1) % circle.length;
        leave.push(circle.splice(j, 1)[0]);
        if (j < i) i -= 1;
      }
      steps.push([stays, leave]);
      i = (i + 1) % circle.length;
    }
    return { steps, survivor: circle[0] };
  };

  // Clock (0029), time in seconds from 00:00:00. Hands i and j meet at k * P / q: the second
  // and minute hands every 3600/59 s, second and hour every 43200/719 s, minute and hour every
  // 43200/11 s. A "second" is the window [sec, sec + 1), so integer arithmetic stays exact.
  const CLOCK_PERIOD = { s: 60, m: 3600, h: 43200 };
  const CLOCK_PAIRS = [["s", "m", 3600, 59], ["s", "h", 43200, 719], ["m", "h", 43200, 11]];
  const CLOCK_DAY = 86400, CLOCK_HALF = 43200;
  // Meetings from 00:00:00 to the end of second sec: per pair, all three, and distinct moments.
  const clockCounts = (sec) => {
    const pairs = CLOCK_PAIRS.map(([, , P, q]) => Math.floor(((sec + 1) * q - 1) / P) + 1);
    const triple = Math.floor(sec / CLOCK_HALF) + 1;
    return { pairs, triple, total: pairs[0] + pairs[1] + pairs[2] - 2 * triple };
  };
  // The meetings inside second sec, as [pair index, time].
  const clockMeetsIn = (sec) => {
    const out = [];
    CLOCK_PAIRS.forEach(([, , P, q], n) => {
      const k = Math.floor((sec * q + P - 1) / P);           // the first k with k P >= sec q
      if (k * P < (sec + 1) * q) out.push([n, (k * P) / q]);
    });
    return out;
  };
  // The first meeting after t, or the last one before it (null outside the day).
  // `mask` limits the search to some pairs (indices into CLOCK_PAIRS).
  const clockNext = (t, mask = [0, 1, 2]) => {
    let best = null;
    mask.forEach((n) => {
      const [, , P, q] = CLOCK_PAIRS[n];
      const v = ((Math.floor((t * q) / P + EPS) + 1) * P) / q;
      if (v < CLOCK_DAY && (best === null || v < best)) best = v;
    });
    return best;
  };
  const clockPrev = (t, mask = [0, 1, 2]) => {
    let best = null;
    mask.forEach((n) => {
      const [, , P, q] = CLOCK_PAIRS[n];
      const k = Math.ceil((t * q) / P - EPS) - 1;
      if (k >= 0 && (best === null || (k * P) / q > best)) best = (k * P) / q;
    });
    return best;
  };
  // "H:MM:SS.ss" as tools/figures/q0029.py writes it: hundredths rounded, but at most .99.
  const clockLabel = (t) => {
    const sec = Math.floor(t);
    const two = (v) => String(v).padStart(2, "0");
    const base = `${Math.floor(sec / 3600)}:${two(Math.floor(sec / 60) % 60)}:${two(sec % 60)}`;
    if (Math.abs(t - sec) < 1e-9) return base;
    return `${base}.${two(Math.min(Math.floor((t - sec) * 100 + 0.5), 99))}`;
  };

  // Strip (0030): the four lateral faces of the box [0, a] x [0, b] x [0, h] unrolled along
  // x, with the perimeter coordinate p running bottom -> sideB -> top -> side0 (period
  // 2(b + h)). An end face folded flat on one of its edges puts its point at x = -gap (or
  // a + gap); the shortest valid straight line between an image of S and an image of F is
  // the path. The same math as tools/figures/q0030.py and the page code.
  const STRIP_FACES = ["bottom", "sideB", "top", "side0"];
  const stripPeriod = (b, h) => 2 * (b + h);
  const stripBands = (b, h) => ({ bottom: [0, b], sideB: [b, b + h], top: [b + h, 2 * b + h], side0: [2 * b + h, 2 * (b + h)] });
  // The four images of the point (y, z) of an end face: the edge it leaves through, its
  // distance to that edge, the p of the foot on the edge and the p-range of the edge.
  const stripImages = (y, z, b, h) => [
    { edge: "bottom", gap: z, p: y, lo: 0, hi: b },
    { edge: "sideB", gap: b - y, p: b + z, lo: b, hi: b + h },
    { edge: "top", gap: h - z, p: b + h + (b - y), lo: b + h, hi: 2 * b + h },
    { edge: "side0", gap: y, p: 2 * b + h + (h - z), lo: 2 * b + h, hi: 2 * (b + h) },
  ];
  const stripMod = (p, b, h) => { const P = stripPeriod(b, h); return ((p % P) + P) % P; };
  // The (y, z) of an end face at perimeter coordinate p on the given edge.
  const stripEdgePoint = (edge, p, b, h) => {
    p = stripMod(p, b, h);
    if (edge === "bottom") return [p, 0];
    if (edge === "sideB") return [b, p - b];
    if (edge === "top") return [2 * b + h - p, h];
    return [0, 2 * b + 2 * h - p];
  };
  // The 3D point of (x, p) on the lateral faces.
  const stripPoint3 = (x, p, b, h) => {
    const q = stripMod(p, b, h);
    if (q < b) return [x, q, 0];
    if (q < b + h) return [x, b, q - b];
    if (q < 2 * b + h) return [x, 2 * b + h - q, h];
    return [x, 0, 2 * b + 2 * h - q];
  };
  const stripBandOf = (p, b, h) => {
    const q = stripMod(p, b, h), bands = stripBands(b, h);
    return STRIP_FACES.find((n) => bands[n][0] <= q && q < bands[n][1]) || "side0";
  };
  // The lateral faces a straight strip line crosses from pFrom to pTo, in order.
  const stripFacesBetween = (pFrom, pTo, b, h) => {
    const P = stripPeriod(b, h), step = pTo >= pFrom ? 1 : -1;
    const cuts = [];
    for (let k = -2; k <= 2; k++) [0, b, b + h, 2 * b + h].forEach((lo) => cuts.push(lo + k * P));
    cuts.sort((u, v) => u - v);
    const at = (p) => stripBandOf(p + step * 1e-7, b, h);          // just past the cut, in the direction of travel
    const out = [at(pFrom)];
    let p = pFrom;
    for (;;) {
      const next = step > 0 ? cuts.find((c) => c > p + EPS) : [...cuts].reverse().find((c) => c < p - EPS);
      if (next === undefined || (step > 0 ? next >= pTo - EPS : next <= pTo + EPS)) return out;
      p = next;
      out.push(at(p));
    }
  };
  // Every straight line of the strip method (4 x 4 x 3), shortest first.
  const stripLines = (a, b, h, y0, z0, y1, z1) => {
    const P = stripPeriod(b, h), out = [];
    stripImages(y0, z0, b, h).forEach((s) => stripImages(y1, z1, b, h).forEach((f) => [-1, 0, 1].forEach((k) => {
      const dx = a + f.gap + s.gap, dp = f.p + k * P - s.p;
      const pExit = s.p + (dp * s.gap) / dx, pEnter = s.p + (dp * (s.gap + a)) / dx;
      const valid = s.lo - EPS <= pExit && pExit <= s.hi + EPS &&
        f.lo + k * P - EPS <= pEnter && pEnter <= f.hi + k * P + EPS;
      out.push({ length: Math.hypot(dx, dp), sEdge: s.edge, fEdge: f.edge, k, xs: -s.gap, ps: s.p,
                 xf: a + f.gap, pf: f.p + k * P, dx, dp, pExit, pEnter, valid });
    })));
    return out.sort((u, v) => u.length - v.length || u.k - v.k);
  };
  // The best line with the path point by point: faces, 3D points and segment lengths.
  const stripBest = (a, b, h, y0, z0, y1, z1) => {
    const lines = stripLines(a, b, h, y0, z0, y1, z1);
    const c = lines.find((l) => l.valid);
    const faces = ["end0", ...stripFacesBetween(c.pExit, c.pEnter, b, h), "enda"];
    const P = stripPeriod(b, h);
    const ts = [-c.xs / c.dx];                                    // where the line crosses x = 0
    const cuts = [];
    for (let k = -2; k <= 2; k++) [0, b, b + h, 2 * b + h].forEach((lo) => cuts.push(lo + k * P));
    cuts.filter((q) => (q - c.pExit) * (q - c.pEnter) < -EPS).sort((u, v) => u - v)
      .forEach((q) => ts.push((q - c.ps) / c.dp));
    ts.sort((u, v) => u - v);
    ts.push((a - c.xs) / c.dx);                                   // where it crosses x = a
    const pts = [[0, y0, z0], ...ts.map((t) => stripPoint3(c.xs + t * c.dx, c.ps + t * c.dp, b, h)), [a, y1, z1]];
    pts[1][0] = 0; pts[pts.length - 2][0] = a;                    // exact on the two walls
    const segs = [ts[0], ...ts.slice(1).map((t, i) => t - ts[i]), 1 - ts[ts.length - 1]].map((t) => t * c.length);
    const exit = stripEdgePoint(c.sEdge, c.pExit, b, h), enter = stripEdgePoint(c.fEdge, c.pEnter, b, h);
    return { line: c, lines, faces, pts, segs, exit: [0, ...exit], enter: [a, ...enter],
             valid: lines.filter((l) => l.valid).length };
  };

  // Hourglasses (0018, 0019): A and B minutes, flipped only when one runs out. A plan is a
  // list of events [t, action] (action "", "A", "B" or "AB"). hourglassSolve is the BFS of
  // 0018 (measure D from time 0); hourglassInterval is the Dijkstra of 0019 (the earliest
  // measurement of D between two events). Both follow the page code line by line.
  const hourglassStep = (A, B, a, b, fa, fb) => {
    const a2 = fa ? A - a : a, b2 = fb ? B - b : b;
    const running = [a2, b2].filter((s) => s > 0);
    if (!running.length) return null;
    const w = Math.min(...running);
    return [w, Math.max(a2 - w, 0), Math.max(b2 - w, 0)];
  };
  const hourglassSolve = (A, B, D) => {
    const seen = new Set(["0,0,0"]);
    const queue = [[0, 0, 0, []]];
    for (let head = 0; head < queue.length; head++) {
      const [t, a, b, plan] = queue[head];
      if (t === D) return plan;
      for (const fa of [0, 1]) for (const fb of [0, 1]) {
        const r = hourglassStep(A, B, a, b, fa, fb);
        if (!r || t + r[0] > D) continue;
        const key = `${t + r[0]},${r[1]},${r[2]}`;
        if (seen.has(key)) continue;
        seen.add(key);
        queue.push([t + r[0], r[1], r[2], [...plan, [t, (fa ? "A" : "") + (fb ? "B" : "")]]]);
      }
    }
    return null;
  };
  const hourglassInterval = (A, B, D) => {
    const best = new Map([["0,0,-1", 0]]);
    const queue = [[0, 0, [0, 0, -1], null, []]];      // [t, tie, state, start, plan]
    let tie = 1;
    const pop = () => { queue.sort((u, v) => u[0] - v[0] || u[1] - v[1]); return queue.shift(); };
    while (queue.length) {
      const [t, , state, start, plan] = pop();
      const key = state.join();
      if (t > best.get(key)) continue;
      const [a, b, m] = state;
      if (m === D) return { start, plan };
      const options = [];
      if (m === -1) options.push([[a, b, 0], t, t, plan]);
      for (const fa of [0, 1]) for (const fb of [0, 1]) {
        const r = hourglassStep(A, B, a, b, fa, fb);
        if (!r) continue;
        const m2 = m === -1 ? -1 : m + r[0];
        if (m2 > D) continue;
        options.push([[r[1], r[2], m2], t + r[0], start, [...plan, [t, (fa ? "A" : "") + (fb ? "B" : "")]]]);
      }
      options.forEach(([s2, t2, st2, pl2]) => {
        const k2 = s2.join();
        if (!best.has(k2) || t2 < best.get(k2)) { best.set(k2, t2); queue.push([t2, tie++, s2, st2, pl2]); }
      });
    }
    return null;
  };
  // Replay a plan from rest: the events as [t, action, [a, b] on arrival, [a, b] after].
  const hourglassReplay = (A, B, plan, end) => {
    let t = 0, a = 0, b = 0;
    const events = [];
    const acts = new Map(plan.map(([w, act]) => [w, act]));
    for (;;) {
      const act = acts.has(t) ? acts.get(t) : null;
      if (act === null) { events.push([t, "", [a, b], null]); return events; }
      const r = hourglassStep(A, B, a, b, act.includes("A"), act.includes("B"));
      const fa = act.includes("A"), fb = act.includes("B");
      events.push([t, act, [a, b], [fa ? A - a : a, fb ? B - b : b]]);
      if (!r) return events;
      t += r[0]; a = r[1]; b = r[2];
      if (end !== undefined && t > end) return events;
    }
  };
  // Every D that can be measured from time 0, up to a bound.
  const hourglassReachable = (A, B, bound) => {
    const seen = new Set(["0,0,0"]), times = new Set([0]);
    const queue = [[0, 0, 0]];
    for (let head = 0; head < queue.length; head++) {
      const [t, a, b] = queue[head];
      for (const fa of [0, 1]) for (const fb of [0, 1]) {
        const r = hourglassStep(A, B, a, b, fa, fb);
        if (!r || t + r[0] > bound) continue;
        const key = `${t + r[0]},${r[1]},${r[2]}`;
        if (seen.has(key)) continue;
        seen.add(key); times.add(t + r[0]);
        queue.push([t + r[0], r[1], r[2]]);
      }
    }
    return [...times].sort((u, v) => u - v).filter((v) => v > 0);
  };

  // Probability (0015): P(all C children are boys | at least one is a boy with the trait).
  const probabilityAnswer = (C, p, q) => (Math.pow(p, C) * (1 - Math.pow(1 - q, C))) / (1 - Math.pow(1 - p * q, C));

  const models = {
    cakeSplit, cakeThreshold, cakeFormula, cakeBest,
    motorcyclePlan, motorcycleTime, motorcyclePhases, motorcyclePositions, josephusRun, josephusSteps, josephusZero, josephusFormula,
    clockCounts, clockMeetsIn, clockNext, clockPrev, clockLabel,
    stripImages, stripEdgePoint, stripPoint3, stripFacesBetween, stripLines, stripBest,
    hourglassSolve, hourglassInterval, hourglassReplay, hourglassReachable, probabilityAnswer,
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

  // The cake box (0027, 0028): the law (arithmetic or geometric, with the same a), the two
  // sliders, and a stepper that adds one person at a time: the slice appears on the cake,
  // the row joins the table and the bar lights up. Play adds a person every moment.
  const cakeView = (kind0) => ({
    mount(box) {
      const d = box.dataset;
      const SL = { arith: { a: [0.005, 0.6, 0.005], step: [0.01, 0.5, 0.01], name: "ההפרש d", law: "החשבוני" },
                   geo: { a: [0.005, 0.6, 0.005], step: [1.05, 2, 0.05], name: "המנה q", law: "ההנדסי" } };
      const defaults = { kind: kind0, a: Number(d.a || 0.01), step: { arith: 0.1, geo: 1.5 } };
      defaults.step[kind0] = Number(d.step || defaults.step[kind0]);
      const st = { kind: kind0, a: defaults.a, step: { ...defaults.step }, shown: 1 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>החוק <select class="ex-kind"><option value="arith">חשבוני, ‏p = a + (k − 1)d</option><option value="geo">הנדסי, ‏p = a · q^(k − 1)</option></select></label>` +
        `<label><span>השבר הראשון a</span><input type="range" class="ex-a" dir="ltr"><output class="out-a"></output></label>` +
        `<label><span class="step-name"></span><input type="range" class="ex-step" dir="ltr"><output class="out-step"></output></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">האדם הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">האדם הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<button type="button" class="md-button ex-all">כולם</button>` +
        `<span class="ex-pos"></span></div>` +
        `<div class="cake-box"><div class="cake-pie"></div><div class="cake-panel"><p class="cake-now"></p><table class="cake-table"><thead><tr><th>האדם</th><th>השבר</th><th>נשאר לפניו</th><th>מקבל</th></tr></thead><tbody></tbody></table></div></div>` +
        `<p class="ex-summary" aria-live="polite"></p><div class="cake-charts"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const kindSel = $(".ex-kind"), aIn = $(".ex-a"), stepIn = $(".ex-step"), pie = $(".cake-pie"), charts = $(".cake-charts");
      const play = $(".ex-play");
      let timer = null;
      const setSliders = () => {
        const sl = SL[st.kind];
        [aIn.min, aIn.max, aIn.step] = sl.a; [stepIn.min, stepIn.max, stepIn.step] = sl.step;
        aIn.value = st.a; stepIn.value = st.step[st.kind];
        $(".step-name").textContent = sl.name;
        kindSel.value = st.kind;
      };
      const rowsOf = (kind) => cakeSplit(kind, st.a, st.step[kind]);
      const pieSvg = (rows, peak) => {
        const C = 110, R = 92;
        const pt = (turn, r = R) => [C + r * Math.sin(2 * Math.PI * turn), C - r * Math.cos(2 * Math.PI * turn)];
        let s = `<svg class="figure cake-live" viewBox="0 0 220 220" role="img" aria-label="העוגה עם הפרוסות של האנשים שכבר חתכו">` +
                `<circle class="cake-rest" cx="${C}" cy="${C}" r="${R}"/>`;
        let c = 0;
        rows.slice(0, st.shown).forEach((r) => {
          const from = c, to = Math.min(c + r.S, 1);
          c = to;
          const [x0, y0] = pt(from), [x1, y1] = pt(to);
          const big = to - from > 0.5 ? 1 : 0;
          const cls = peak.includes(r.k) ? "cake-peak" : r.k % 2 ? "cake-slice" : "cake-slice2";
          const path = to - from >= 1 - 1e-9 ? `M${C},${C - R} A${R},${R} 0 1 1 ${C - 0.01},${C - R} Z`
            : `M${C},${C} L${f(x0, 2)},${f(y0, 2)} A${R},${R} 0 ${big} 1 ${f(x1, 2)},${f(y1, 2)} Z`;
          s += `<path class="${cls}${r.k === st.shown ? " is-now" : ""}" d="${path}"><title>אדם ${r.k}: p = ${fmt(r.p, 3)}, S = ${fmt(r.S, 4)}</title></path>`;
          if (to - from > 0.045) {
            const [tx, ty] = pt((from + to) / 2, R * 0.68);
            s += `<text class="st-text" x="${f(tx)}" y="${f(ty + 5)}" text-anchor="middle" style="fill:var(--md-default-bg-color)">${r.k}</text>`;
          }
        });
        s += `<circle class="cake-edge" cx="${C}" cy="${C}" r="${R}" fill="none"/>`;
        return s + "</svg>";
      };
      const draw = () => {
        const rows = rowsOf(st.kind), n = rows.length;
        st.shown = Math.min(Math.max(st.shown, 1), n);
        $(".out-a").textContent = String(st.a); $(".out-step").textContent = String(st.step[st.kind]);
        const peak = cakeBest(rows), T = cakeThreshold(st.kind, st.step[st.kind]), fm = cakeFormula(st.kind, st.a, st.step[st.kind]);
        const seen = rows.slice(0, st.shown), topSeen = Math.max(...seen.map((r) => r.S));
        const peakSeen = seen.filter((r) => Math.abs(r.S - topSeen) <= EPS * topSeen).map((r) => r.k);
        pie.innerHTML = pieSvg(rows, st.shown >= n ? peak : peakSeen);
        const now = rows[st.shown - 1];
        $(".cake-now").innerHTML = `האדם ה-${now.k} מוצא ${ltr(fmt(now.R, 4))} מהעוגה, לוקח ממנה ${ltr(fmt(now.p, 3))} ומקבל ${ltr(fmt(now.S, 4))}` +
          (now.p >= 1 ? ", את כל מה שנשאר." : `; נשאר ${ltr(fmt(now.R - now.S, 4))} לבאים אחריו.`);
        $(".cake-table tbody").innerHTML = seen.map((r) =>
          `<tr${peakSeen.includes(r.k) ? ' class="is-best"' : ""}${r.k === st.shown ? ' data-now="1"' : ""}><td>${ltr(r.k)}</td><td>${ltr(fmt(r.p, 3))}</td><td>${ltr(fmt(r.R, 4))}</td><td>${ltr(fmt(r.S, 4))}</td></tr>`).join("");
        $(".ex-pos").textContent = `אדם ${st.shown} מתוך ${n}`;
        $(".ex-prev").disabled = st.shown <= 1; $(".ex-next").disabled = st.shown >= n; $(".ex-all").disabled = st.shown >= n;
        const who = peak.length > 1 ? `תיקו בין האדם ה-${peak[0]} לאדם ה-${peak[1]}` : `האדם ה-${peak[0]}`;
        const other = st.kind === "arith" ? "geo" : "arith";
        const orows = rowsOf(other), opeak = cakeBest(orows);
        const agree = fm.k === peak[0] && fm.tie === (peak.length > 1);
        summary.innerHTML = `בחוק ${SL[st.kind].law}: המקבל הגדול הוא ${who}, עם ${ltr(fmt(rows[peak[0] - 1].S))} מהעוגה, מתוך ${n} אנשים. ` +
          `הסף הוא ${ltr(`T ≈ ${fmt(T)}`)}, והנוסחה נותנת את האדם ה-${fm.k}${fm.tie ? " (תיקו עם הבא)" : ""}${agree ? ", בדיוק כמו בעמודות." : ", שלא כמו בעמודות."} ` +
          `להשוואה, בחוק ${SL[other].law} עם אותו ${ltr("a")} ו-${ltr(`${SL[other].name.split(" ")[1]} = ${st.step[other]}`)}: האדם ה-${opeak[0]} עם ${ltr(fmt(orows[opeak[0] - 1].S))}, מתוך ${orows.length}.`;
        const shares = barsChart("החלק של כל אדם", rows.map((r) => r.S), peak, (k, v) => `S(${k}) = ${fmt(v, 4)}`)
          .replace(/<rect class="bar ([a-z-]+)" /g, (m0, cls, off) => m0);
        // bars of people not yet shown are faint
        let i = 0;
        const sharesShown = shares.replace(/<rect class="bar [a-z-]+" /g, (m0) => { i += 1; return i > st.shown ? m0.replace('class="bar', 'fill-opacity="0.22" class="bar') : m0; });
        const fr = frame("השבר של כל אדם מול הסף", n, 1, [0, 0.25, 0.5, 0.75, 1]);
        let fs = fr.s + hline(fr, T, `T ≈ ${fmt(T)}`);
        rows.forEach((r) => {
          const cls = r.k === peak[0] ? "s2" : r.p < T - EPS ? "s1" : "ink";
          const rad = r.k === peak[0] ? 6 : Math.min(4.5, Math.max(1.5, fr.slot * 0.35));
          const dim = r.k > st.shown ? ' opacity="0.25"' : "";
          fs += `<line class="${cls}-line" x1="${f(fr.cx(r.k))}" x2="${f(fr.cx(r.k))}" y1="${BASE}" y2="${f(fr.Y(r.p))}" stroke-width="${f(Math.min(2, fr.slot * 0.4))}"${dim}/>` +
                `<circle class="${cls}-dot" cx="${f(fr.cx(r.k))}" cy="${f(fr.Y(r.p))}" r="${f(rad)}"${dim}><title>p(${r.k}) = ${fmt(r.p, 4)}</title></circle>`;
          if (r.k % fr.every === 0 || r.k === 1 || r.k === peak[0]) fs += fr.xtick(r.k);
        });
        charts.innerHTML = `<p class="ex-title">החלק של כל אדם</p>${sharesShown}<p class="ex-title">השבר של כל אדם מול הסף</p>${fs + fr.close()}`;
        if (window.dvqDecorate) window.dvqDecorate(charts);
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
        timer = setInterval(() => { if (st.shown >= rowsOf(st.kind).length) { stop(); return; } go(st.shown + 1); }, 700);
        go(st.shown + 1);
      });
      kindSel.addEventListener("change", () => { stop(); st.kind = kindSel.value; st.shown = 1; setSliders(); draw(); });
      aIn.addEventListener("input", () => { stop(); st.a = Number(aIn.value); draw(); });
      stepIn.addEventListener("input", () => { stop(); st.step[st.kind] = Number(stepIn.value); draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); st.kind = kind0; st.a = defaults.a; st.step = { ...defaults.step }; st.shown = 1; setSliders(); draw(); });
      setSliders();
      draw();
    },
  });

  const motorcycleView = () => ({
    mount(box) {
      const defaults = { t0: Number(box.dataset.t0 || 13), t1: Number(box.dataset.t1 || 1) };
      const st = { ...defaults, strategy: "optimal", t: 0 };
      const NAMES = { wait: "השני מחכה ב-A", meanwhile: "השני הולך בינתיים", optimal: "הנוסע יורד בדרך" };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>הליכה של כל הדרך t0 (שעות)</span><input type="range" class="ex-t0" min="2" max="30" step="1" value="${st.t0}" dir="ltr"><output class="out-t0"></output></label>` +
        `<label><span>נסיעה של כל הדרך t1 (שעות)</span><input type="range" class="ex-t1" min="0.5" max="3" step="0.5" value="${st.t1}" dir="ltr"><output class="out-t1"></output></label>` +
        `<label>התוכנית <select class="ex-strategy">` + Object.entries(NAMES).map(([k, n]) => `<option value="${k}"${k === "optimal" ? " selected" : ""}>${n}</option>`).join("") + `</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="0.25">רבע שעה בשנייה</option><option value="0.5" selected>חצי שעה בשנייה</option><option value="1">שעה בשנייה</option><option value="2">שעתיים בשנייה</option></select></label>` +
        `<label class="ex-scrub"><span>הזמן</span><input type="range" class="ex-t" min="0" max="1" step="0.001" value="0" dir="ltr"><output class="out-t" dir="ltr"></output></label></div>` +
        `<div class="road-box"></div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<p class="ex-title">המקום על הדרך (0 הוא A ו-1 הוא B) מול הזמן בשעות</p><div class="road-chart"></div>` +
        `<span class="viz-legend"><span><i class="ink" style="opacity:0.4"></i>האופנוע</span><span><i class="s1"></i>הנוסע</span><span><i class="s2"></i>ההולך</span></span>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), scrub = $(".ex-t"), summary = $(".ex-summary");
      const road = $(".road-box"), chart = $(".road-chart"), strategy = $(".ex-strategy");
      let running = false, last = 0;
      const alpha = () => st.t0 / st.t1;
      const phases = () => motorcyclePhases(st.strategy, alpha());

      const roadSvg = (pos, ph) => {
        const w = 640, h = 96, x0 = 36, x1 = 604, yr = 58;
        const X = (v) => x0 + v * (x1 - x0);
        let s = `<svg class="figure road-live" viewBox="0 0 ${w} ${h}" role="img" aria-label="הדרך מ-A ל-B עם האופנוע, הנוסע וההולך במקומם בזמן הנוכחי">` +
          `<line class="axis-c" x1="${x0}" x2="${x1}" y1="${yr}" y2="${yr}" stroke-width="3"/>` +
          `<text class="legend" x="${x0}" y="${yr + 24}" text-anchor="middle">A</text><text class="legend" x="${x1}" y="${yr + 24}" text-anchor="middle">B</text>`;
        const marks = [];
        if (st.strategy === "optimal") {
          const pl = motorcyclePlan(alpha());
          marks.push(["Q", pl.Q], ["C", pl.C], ["D", pl.D], ["E", pl.E]);
        } else if (st.strategy === "meanwhile") marks.push(["M", 2 / (alpha() + 1)]);
        marks.forEach(([n, v]) => {
          s += `<line class="grid" x1="${f(X(v))}" x2="${f(X(v))}" y1="${yr - 8}" y2="${yr + 8}" stroke-width="1.5"/>` +
               `<text class="tick" x="${f(X(v))}" y="${yr + 24}" text-anchor="middle">${n}</text>`;
        });
        const [bike, pass, walk] = pos;
        const onBike = (v) => Math.abs(v - bike) < 1e-9;
        s += `<circle class="ink-dot" cx="${f(X(bike))}" cy="${yr}" r="9" fill-opacity="0.45"><title>האופנוע: ${fmt(bike)}</title></circle>`;
        [["s1", pass, "הנוסע", -1], ["s2", walk, "ההולך", 1]].forEach(([cls, v, name, side]) => {
          const cy = onBike(v) ? yr - 12 * side - (side < 0 ? 6 : -6) : yr;
          s += `<circle class="${cls}-dot" cx="${f(X(v))}" cy="${f(onBike(v) ? yr + 14 * side : yr)}" r="6"><title>${name}: ${fmt(v)}${onBike(v) ? " (על האופנוע)" : ""}</title></circle>`;
          void cy;
        });
        return s + "</svg>";
      };
      const chartSvg = (ph, pos) => {
        const w = 640, h = 280, x0 = 52, right = 24, top = 30, base = 246;
        const X = (t) => x0 + (t / ph.T) * (w - x0 - right);
        const Y = (v) => base - v * (base - top);
        let s = `<svg class="perf-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="המקום של האופנוע ושל שני ההולכים לאורך הזמן, עד הזמן הנוכחי">`;
        const yt = [[0, "0"], [1, "1"]];
        if (st.strategy === "optimal") { const pl = motorcyclePlan(alpha()); yt.push([pl.C, fmt(pl.C, 3)], [pl.D, fmt(pl.D, 3)]); }
        if (st.strategy === "meanwhile") yt.push([2 / (alpha() + 1), fmt(2 / (alpha() + 1), 3)]);
        yt.forEach(([v, lab]) => {
          s += `<line class="grid" x1="${x0}" x2="${w - right}" y1="${f(Y(v))}" y2="${f(Y(v))}"/>` +
               `<text class="tick" x="${x0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${lab}</text>`;
        });
        [0, ph.t1, ph.t2, ph.T].forEach((t) => {
          s += `<line class="grid" x1="${f(X(t))}" x2="${f(X(t))}" y1="${top - 6}" y2="${base}" stroke-dasharray="4 4"/>` +
               `<text class="tick" x="${f(X(t))}" y="${base + 18}" text-anchor="middle">${fmt(t * st.t1, 2)}</text>`;
        });
        // the paths are polylines through the phase ends; the drawn part stops at the time shown
        const knots = [0, ph.t1, ph.t2, ph.T];
        const line = (idx, cls, width, upTo, extra = "") => {
          const ts = knots.filter((t) => t < upTo - 1e-12).concat([upTo]);
          const pts = ts.map((t) => `${f(X(t))},${f(Y(motorcyclePositions(st.strategy, alpha(), t)[idx]))}`).join(" ");
          return `<polyline class="${cls}" points="${pts}" fill="none" stroke-width="${width}" stroke-linejoin="round"${extra}/>`;
        };
        s += line(0, "ink-line", 7, ph.T, ' stroke-opacity="0.1"') + line(1, "s1-line", 2.5, ph.T, ' stroke-opacity="0.2"') + line(2, "s2-line", 2.5, ph.T, ' stroke-opacity="0.2"');
        if (st.t > 0) s += line(0, "ink-line", 7, st.t, ' stroke-opacity="0.28"') + line(1, "s1-line", 2.5, st.t) + line(2, "s2-line", 2.5, st.t);
        s += `<line class="axis-c" x1="${f(X(st.t))}" x2="${f(X(st.t))}" y1="${top - 6}" y2="${base}" stroke-width="1"/>`;
        [["ink-dot", pos[0], 7], ["s1-dot", pos[1], 5], ["s2-dot", pos[2], 5]].forEach(([cls, v, r]) => {
          s += `<circle class="${cls}" cx="${f(X(st.t))}" cy="${f(Y(v))}" r="${r}"/>`;
        });
        s += `<line class="axis" x1="${x0}" x2="${w - right}" y1="${base}" y2="${base}"/></svg>`;
        return s;
      };
      const draw = () => {
        $(".out-t0").textContent = String(st.t0); $(".out-t1").textContent = String(st.t1);
        const a = alpha();
        if (a <= 1 + EPS) {
          road.innerHTML = ""; chart.innerHTML = "";
          summary.innerHTML = `יחס המהירויות ${ltr(`α = ${f(a, 2)}`)}: האופנוע לא מהיר מההליכה, ולכן כולם פשוט הולכים, ${fmt(st.t0, 2)} שעות.`;
          return;
        }
        const ph = phases();
        st.t = Math.min(st.t, ph.T);
        scrub.max = ph.T; scrub.value = st.t;
        $(".out-t").textContent = `${fmt(st.t * st.t1, 2)} / ${fmt(ph.T * st.t1, 2)} h`;
        const pos = motorcyclePositions(st.strategy, a, st.t);
        road.innerHTML = roadSvg(pos, ph);
        chart.innerHTML = chartSvg(ph, pos);
        const T = { wait: 3, meanwhile: (3 * a - 1) / (a + 1), optimal: motorcyclePlan(a).T };
        const pl = motorcyclePlan(a);
        const phase = st.t < ph.t1 ? 1 : st.t < ph.t2 ? 2 : 3;
        summary.innerHTML = `יחס המהירויות ${ltr(`α = ${f(a, 2)}`)}. בתוכנית "${NAMES[st.strategy]}" שלושתם מגיעים אחרי ${fmt(T[st.strategy] * st.t1, 2)} שעות ` +
          `(להשוואה: מחכה ${fmt(T.wait * st.t1, 2)}, הולך בינתיים ${fmt(T.meanwhile * st.t1, 2)}, יורד בדרך ${fmt(T.optimal * st.t1, 2)}). ` +
          (st.strategy === "optimal" ? `הנוסע יורד אחרי ${fmt(pl.D, 3)} מהדרך, וכל אחד מהשניים הולך ${fmt(pl.y + pl.x, 3)} ממנה. ` : "") +
          `עכשיו שלב ${phase}: האופנוע ב-${ltr(fmt(pos[0]))}, הנוסע ב-${ltr(fmt(pos[1]))}, ההולך ב-${ltr(fmt(pos[2]))}.`;
        if (window.dvqDecorate) window.dvqDecorate(chart);
      };
      const stop = () => { running = false; play.textContent = "הפעלה"; summary.setAttribute("aria-live", "polite"); };
      const tick = (now) => {
        if (!running) return;
        const ph = phases();
        st.t = Math.min(st.t + ((now - last) / 1000) * Number(speed.value) / st.t1, ph.T);
        last = now;
        draw();
        if (st.t >= ph.T) stop(); else requestAnimationFrame(tick);
      };
      play.addEventListener("click", () => {
        if (running) { stop(); return; }
        if (alpha() <= 1 + EPS) return;
        if (st.t >= phases().T - 1e-9) st.t = 0;
        running = true;
        play.textContent = "עצירה";
        summary.setAttribute("aria-live", "off");
        last = performance.now();
        requestAnimationFrame(tick);
      });
      scrub.addEventListener("input", () => { stop(); st.t = Number(scrub.value); draw(); });
      ["t0", "t1"].forEach((k) => $(`.ex-${k}`).addEventListener("input", () => { st[k] = Number($(`.ex-${k}`).value); draw(); }));
      strategy.addEventListener("change", () => { st.strategy = strategy.value; draw(); });
      $(".ex-reset").addEventListener("click", () => {
        stop(); Object.assign(st, defaults, { strategy: "optimal", t: 0 });
        $(".ex-t0").value = st.t0; $(".ex-t1").value = st.t1; strategy.value = "optimal"; draw();
      });
      draw();
    },
  });

  // The Josephus box (0016, 0022): sliders for N (and L), and a circle that plays the
  // elimination step by step or at a chosen speed; the survivor can be highlighted from the
  // start, the people who left are listed in order, and the survivor chart stays.
  const josephusView = (box) => ({
    mount(box2) {
      const withL = box.dataset.lmax && Number(box.dataset.lmax) > Number(box.dataset.l);
      const nmax = Number(box.dataset.nmax || 64);
      const defaults = { n: Number(box.dataset.n || 20), l: Number(box.dataset.l || 2) };
      const st = { ...defaults, s: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>מספר האנשים N</span><input type="range" class="ex-n" min="1" max="${nmax}" step="1" value="${st.n}" dir="ltr"><output class="out-n"></output></label>` +
        (withL ? `<label><span>הכלל ${ltr("L")}: אחד נשאר, ${ltr("L − 1")} יוצאים</span><input type="range" class="ex-l" min="2" max="${box.dataset.lmax}" step="1" value="${st.l}" dir="ltr"><output class="out-l"></output></label>` : "") +
        `<label><input type="checkbox" class="ex-mark" checked> להדגיש את השורד מההתחלה</label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1200">איטי</option><option value="500" selected>בינוני</option><option value="150">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<span class="ex-pos"></span></div>` +
        `<div class="jos-box"><div class="jos-circle"></div><div class="jos-panel"><p class="jos-now"></p><p class="jos-order"></p></div></div>` +
        `<p class="ex-summary" aria-live="polite"></p><p class="ex-title">השורד לכל N, עם N הנבחר מודגש; נקודות שחורות הן נקודות אפס</p><div class="jos-chart"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), mark = $(".ex-mark");
      let timer = null, chartFor = "";
      const circleSvg = (n, out, stays, leave, winner) => {
        let w, R, r, small;
        if (n <= 12) [w, R, r, small] = [300, 105, 17, ""];
        else if (n <= 20) [w, R, r, small] = [300, 118, 15, ""];
        else if (n <= 40) [w, R, r, small] = [340, 140, 11, " st-sm"];
        else [w, R, r, small] = [340, 150, 7, " st-none"];
        const cx = w / 2, cy = w / 2, h = w - 20;
        let s = `<svg class="figure jos-live" viewBox="0 0 ${w} ${h}" style="max-width:${(w / 16).toFixed(0)}rem" role="img" aria-label="${n} אנשים במעגל">` +
                `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/>`;
        for (let i = 0; i < n; i++) {
          const a = -Math.PI / 2 + (2 * Math.PI * i) / n;
          const x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
          const cls = i === winner ? "st-ok" : leave.includes(i) ? "st-bad" : i === stays ? "st-stack" : out.has(i) ? "st-done" : "st-cell";
          const faded = out.has(i) && !leave.includes(i) ? ' class="st-faded"' : "";
          s += `<g${faded}><circle class="${cls}" cx="${f(x)}" cy="${f(y)}" r="${r}"><title>אדם ${i}</title></circle>`;
          if (small !== " st-none") s += `<text class="st-text${small}" x="${f(x)}" y="${f(y + (small ? 4 : 5))}" text-anchor="middle">${i}</text>`;
          if (out.has(i)) { const dd = Math.max(r - 3, 3); s += `<line class="pg-strike" x1="${f(x - dd)}" y1="${f(y + dd)}" x2="${f(x + dd)}" y2="${f(y - dd)}"/>`; }
          s += "</g>";
        }
        s += `<text class="st-text" x="${cx}" y="${cy + 6}" text-anchor="middle">${n - out.size}</text></svg>`;
        return s;
      };
      const chartSvg = (n, L) => {
        const vals = Array.from({ length: nmax }, (_, i) => josephusRun(i + 1, L));
        const ymax = Math.max(nmax, 1), step = ymax > 40 ? 16 : 8, ticks = [];
        for (let v = 0; v <= ymax; v += step) ticks.push(v);
        const fr = frame("השורד לכל גודל מעגל", nmax, ymax, ticks);
        let s = fr.s;
        vals.forEach((v, i) => {
          const k = i + 1, cls = k === n ? "s2-dot" : v === 0 ? "ink-dot" : "s1-dot";
          s += `<circle class="${cls}" cx="${f(fr.cx(k))}" cy="${f(fr.Y(v))}" r="${k === n ? 6 : Math.min(4, fr.slot * 0.4).toFixed(1)}"><title>N = ${k}: ${v}</title></circle>`;
          if (k % fr.every === 0 || k === 1 || k === n) s += fr.xtick(k);
        });
        return s + fr.close();
      };
      const people = (nums) => nums.length === 1 ? String(nums[0]) : `${nums.slice(0, -1).join(", ")} ו-${nums[nums.length - 1]}`;
      const draw = () => {
        const n = st.n, L = st.l;
        $(".out-n").textContent = String(n);
        if (withL) $(".out-l").textContent = String(L);
        const { steps, survivor } = josephusSteps(n, L);
        st.s = Math.min(Math.max(st.s, 0), steps.length);
        const out = new Set();
        steps.slice(0, st.s).forEach(([, leave]) => leave.forEach((p) => out.add(p)));
        const cur = st.s > 0 ? steps[st.s - 1] : null;
        const done = st.s >= steps.length;
        const winner = done || mark.checked ? survivor : null;
        $(".jos-circle").innerHTML = circleSvg(n, out, cur ? cur[0] : null, cur ? cur[1] : [], winner);
        const rule = L === 2 ? "נשאר, והבא אחריו יוצא" : `נשאר, ו-${L - 1} הבאים אחריו יוצאים`;
        let round = 0, prev = null;
        steps.slice(0, Math.max(st.s, 1)).forEach(([stays]) => { if (prev === null || stays <= prev) round += 1; prev = stays; });
        $(".jos-now").innerHTML = st.s === 0 ? `${n} אנשים במעגל. מתחילים מאדם 0: הוא ${rule}. המספר במרכז הוא כמה אנשים נשארו.`
          : done && steps.length === st.s ? `צעד ${st.s}: אדם ${cur[0]} נשאר, ${cur[1].length === 1 ? `ואדם ${cur[1][0]} יוצא` : `ואנשים ${people(cur[1])} יוצאים`}. נשאר אדם ${survivor}, והוא השורד.`
          : `צעד ${st.s}, סיבוב ${round}: אדם ${cur[0]} נשאר, ${cur[1].length === 1 ? `ואדם ${cur[1][0]} יוצא` : `ואנשים ${people(cur[1])} יוצאים`}.`;
        const order = steps.slice(0, st.s).flatMap(([, leave]) => leave);
        $(".jos-order").innerHTML = order.length ? `סדר היציאה (${ltr(order.length)} מתוך ${ltr(n - 1)}): ` +
          order.map((p, i) => `<span class="jos-chip${i >= order.length - (cur ? cur[1].length : 0) ? " is-now" : ""}">${p}</span>`).join(" ") : "עוד אף אחד לא יצא.";
        $(".ex-pos").textContent = `צעד ${st.s} מתוך ${steps.length}`;
        $(".ex-prev").disabled = st.s <= 0; $(".ex-next").disabled = done;
        const sim = survivor, form = josephusFormula(n, L), M = josephusZero(n, L);
        $(".ex-summary").innerHTML = `עם ${ltr(`N = ${n}`)} ו-${ltr(`L = ${L}`)} השורד הוא ${sim} בסימולציה, והנוסחה ` +
          `${ltr(`${L}(N − M) / ${L - 1}`)} עם נקודת האפס ${ltr(`M = ${M}`)} נותנת ${form}` +
          `${sim === form ? ", אותו דבר." : ", שלא כמו בסימולציה."}` +
          (L === 2 ? ` בבינארי: ${ltr(`N = ${n.toString(2)}`)}, והשורד ${ltr(sim.toString(2))}.` : "");
        if (chartFor !== `${n}/${L}`) { chartFor = `${n}/${L}`; $(".jos-chart").innerHTML = chartSvg(n, L); if (window.dvqDecorate) window.dvqDecorate($(".jos-chart")); }
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => josephusSteps(st.n, st.l).steps.length;
      $(".ex-next").addEventListener("click", () => { stop(); st.s += 1; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s -= 1; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.s >= total()) st.s = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { if (st.s >= total()) { stop(); return; } st.s += 1; draw(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      mark.addEventListener("change", draw);
      $(".ex-n").addEventListener("input", () => { stop(); st.n = Number($(".ex-n").value); st.s = 0; draw(); });
      if (withL) $(".ex-l").addEventListener("input", () => { stop(); st.l = Number($(".ex-l").value); st.s = 0; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, defaults, { s: 0 }); $(".ex-n").value = st.n; if (withL) $(".ex-l").value = st.l; draw(); });
      draw();
    },
  });

  // The clock box: a face whose hands can be dragged, a play button with a speed, a day
  // slider, a time field and jumps to the next or previous meeting. The counters cover
  // 00:00:00 to the end of the second shown; hands that meet inside that second turn orange.
  const clockView = () => ({
    mount(box) {
      const C = 140, R = 124, LAST = CLOCK_DAY - 1e-6;
      const HAND = { h: ["ink", 62, 7], m: ["s1", 96, 4.5], s: ["s3", 108, 2] };
      const NAMES = { s: "השניות", m: "הדקות", h: "השעות" };
      const PAIR_NAME = CLOCK_PAIRS.map(([i, j]) => `${NAMES[i]} ו${NAMES[j]}`);
      const pt = (turn, r) => [C + r * Math.sin(2 * Math.PI * turn), C - r * Math.cos(2 * Math.PI * turn)];
      let face = `<svg class="figure clock-live" viewBox="0 0 280 280" role="img" aria-label="שעון">` +
        `<circle class="clock-face" cx="${C}" cy="${C}" r="${R}"/>`;
      for (let n = 0; n < 60; n++) {
        const [x0, y0] = pt(n / 60, R - (n % 5 ? 5 : 11)), [x1, y1] = pt(n / 60, R);
        face += `<line class="${n % 5 ? "clock-tick" : "clock-tick5"}" x1="${f(x0)}" y1="${f(y0)}" x2="${f(x1)}" y2="${f(y1)}"/>`;
      }
      for (let n = 1; n <= 12; n++) {
        const [x, y] = pt(n / 12, R - 26);
        face += `<text class="legend" x="${f(x)}" y="${f(y + 5)}" text-anchor="middle">${n}</text>`;
      }
      ["h", "m", "s"].forEach((k) => {
        const [cls, len, w] = HAND[k];
        face += `<line class="${cls}-line hand hand-${k}" x1="${C}" y1="${C}" x2="${C}" y2="${C - len}" ` +
                `stroke-width="${w}" stroke-linecap="round"/>`;
      });
      face += `<circle class="ink-dot" cx="${C}" cy="${C}" r="5"/></svg>`;

      box.innerHTML =
        `<div class="ex-controls">` +
        `<button type="button" class="md-button md-button--primary ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed">` +
        [[1, "זמן אמת"], [10, "פי 10"], [60, "דקה בשנייה"], [600, "10 דקות בשנייה"], [3600, "שעה בשנייה"]]
          .map(([v, n]) => `<option value="${v}"${v === 60 ? " selected" : ""}>${n}</option>`).join("") +
        `</select></label>` +
        `<button type="button" class="md-button ex-prev">לפגישה הקודמת</button>` +
        `<button type="button" class="md-button ex-next">לפגישה הבאה</button>` +
        `<button type="button" class="md-button ex-triple">למשולשת הבאה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה ל-00:00</button></div>` +
        `<div class="ex-controls clock-filter"><span>הקפיצות ופס הזמן:</span>` +
        PAIR_NAME.map((name, n) => `<label><input type="checkbox" class="ex-pair" value="${n}" checked> ${name}</label>`).join("") + `</div>` +
        `<div class="clock-box">${face}<div class="clock-panel">` +
        `<p class="clock-time" dir="ltr"></p>` +
        `<label>שעה <input type="text" class="ex-time" inputmode="numeric" maxlength="8" size="8" ` +
        `placeholder="HH:MM:SS" aria-label="שעה, שעות:דקות:שניות" dir="ltr"></label>` +
        `<p class="clock-total"></p><ul class="clock-counts"></ul></div></div>` +
        `<label class="clock-day">היממה <input type="range" class="ex-day" min="0" max="${CLOCK_DAY - 1}" step="1" dir="ltr"></label>` +
        `<div class="clock-timeline" dir="ltr"></div>` +
        `<p class="ex-summary" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const svg = $("svg"), hands = {}, play = $(".ex-play"), speed = $(".ex-speed");
      const timeIn = $(".ex-time"), day = $(".ex-day"), summary = $(".ex-summary");
      ["h", "m", "s"].forEach((k) => { hands[k] = $(`.hand-${k}`); });
      let t = Number(box.dataset.t || 0), shown = -1, running = false, last = 0;
      const mask = () => {
        const on = [...box.querySelectorAll(".ex-pair")].filter((c) => c.checked).map((c) => Number(c.value));
        return on.length ? on : [0, 1, 2];
      };
      // the timeline: one row per pair with a tick at every meeting; dense bands show where
      // the meetings of a pair cluster. A click jumps to the nearest meeting of that row.
      const TL_W = 600, TL_CLS = ["s1-line", "s3-line", "s2-line"];
      const tlX = (sec) => (sec / CLOCK_DAY) * TL_W;
      const timeline = $(".clock-timeline");
      timeline.innerHTML = CLOCK_PAIRS.map(([, , P, q], n) => {
        let ticks = "";
        for (let k = 0; k * P < CLOCK_DAY * q; k++) {
          const x = tlX((k * P) / q).toFixed(1);
          ticks += `<line class="${TL_CLS[n]}" x1="${x}" x2="${x}" y1="1" y2="13" stroke-width="${n === 2 ? 2 : 1}" stroke-opacity="${n === 2 ? 0.9 : 0.55}"/>`;
        }
        return `<div class="tl-row" data-pair="${n}"><span class="tl-name">${PAIR_NAME[n]}</span>` +
          `<svg viewBox="0 0 ${TL_W} 14" preserveAspectRatio="none" role="img" aria-label="הפגישות של ${PAIR_NAME[n]} לאורך היממה">${ticks}` +
          `<line class="tl-cursor" x1="0" x2="0" y1="0" y2="14"/></svg></div>`;
      }).join("") + `<div class="tl-axis"><span>00:00</span><span class="tl-mid">06:00</span><span>12:00</span><span class="tl-mid">18:00</span><span>24:00</span></div>`;
      timeline.querySelectorAll(".tl-row").forEach((row) => {
        const n = Number(row.dataset.pair), svg = row.querySelector("svg");
        svg.addEventListener("click", (e) => {
          const r = svg.getBoundingClientRect();
          const at = ((e.clientX - r.left) / r.width) * CLOCK_DAY;
          const [, , P, q] = CLOCK_PAIRS[n];
          const k = Math.round((at * q) / P);
          stop();
          setTime(Math.min(Math.max((k * P) / q, 0), LAST));
        });
      });

      const two = (v) => String(v).padStart(2, "0");
      const hms = (sec) => `${two(Math.floor(sec / 3600))}:${two(Math.floor(sec / 60) % 60)}:${two(sec % 60)}`;
      const render = (force) => {
        ["h", "m", "s"].forEach((k) => {
          const turn = (t / CLOCK_PERIOD[k]) % 1;
          hands[k].setAttribute("transform", `rotate(${(turn * 360).toFixed(3)} ${C} ${C})`);
        });
        const sec = Math.floor(t);
        if (sec === shown && !force) return;
        shown = sec;
        const meets = clockMeetsIn(sec), cnt = clockCounts(sec);
        const on = new Set();
        meets.forEach(([n]) => { on.add(CLOCK_PAIRS[n][0]); on.add(CLOCK_PAIRS[n][1]); });
        ["h", "m", "s"].forEach((k) => hands[k].classList.toggle("is-meet", on.has(k)));
        $(".clock-time").textContent = hms(sec);
        svg.setAttribute("aria-label", `שעון בשעה ${hms(sec)}`);
        if (document.activeElement !== timeIn || running) timeIn.value = hms(sec);
        day.value = sec;
        const enabled = mask();
        timeline.querySelectorAll(".tl-row").forEach((row) => {
          row.classList.toggle("is-off", !enabled.includes(Number(row.dataset.pair)));
          const x = tlX(t).toFixed(1);
          const c = row.querySelector(".tl-cursor");
          c.setAttribute("x1", x); c.setAttribute("x2", x);
        });
        $(".clock-total").innerHTML = `מתחילת היממה: ${cnt.total === 1 ? "פגישה אחת" : `${ltr(cnt.total)} פגישות`}`;
        const hit = new Set(meets.map(([n]) => n));
        $(".clock-counts").innerHTML = PAIR_NAME.map((name, n) =>
          `<li${hit.has(n) ? ' class="is-meet"' : ""}>${name}: ${ltr(cnt.pairs[n])}</li>`).join("") +
          `<li${sec % CLOCK_HALF === 0 ? ' class="is-meet"' : ""}>שלושתם יחד: ${ltr(cnt.triple)}, ` +
          `ולכן ${ltr(`${cnt.pairs.join(" + ")} − 2 · ${cnt.triple} = ${cnt.total}`)}</li>`;
        let text;
        const triple = sec % CLOCK_HALF === 0;               // all three meet only at 00:00 and 12:00
        if (triple) {
          text = `בשנייה הזו שלושת המחוגים נפגשים, ב-${ltr(clockLabel(meets[0][1]))}.`;
        } else if (meets.length) {
          text = "בשנייה הזו: " + meets.map(([n, v]) => `${PAIR_NAME[n]} נפגשים ב-${ltr(clockLabel(v))}`).join(", ") + ".";
        } else {
          const nx = clockNext(sec + 1 - 1e-9, mask());
          text = "בשנייה הזו אין פגישה." + (nx === null ? " אין עוד פגישות עד סוף היממה."
            : ` הבאה: ב-${ltr(clockLabel(nx))}, ${clockMeetsIn(Math.floor(nx)).map(([n]) => PAIR_NAME[n]).join(" וגם ")}.`);
        }
        summary.innerHTML = text;                    // built from numbers and fixed names only
      };
      const setTime = (v) => { t = Math.min(Math.max(v, 0), LAST); render(); };
      const stop = () => {
        running = false;
        play.textContent = "הפעלה";
        summary.setAttribute("aria-live", "polite");
      };
      const tick = (now) => {
        if (!running) return;
        t = Math.min(t + ((now - last) / 1000) * Number(speed.value), LAST);
        last = now;
        render();
        if (t >= LAST) stop(); else requestAnimationFrame(tick);
      };
      play.addEventListener("click", () => {
        if (running) { stop(); return; }
        if (t >= LAST) t = 0;
        running = true;
        play.textContent = "עצירה";
        summary.setAttribute("aria-live", "off");
        last = performance.now();
        requestAnimationFrame(tick);
      });
      $(".ex-next").addEventListener("click", () => { stop(); const v = clockNext(t, mask()); if (v !== null) setTime(v); });
      $(".ex-prev").addEventListener("click", () => { stop(); const v = clockPrev(t, mask()); if (v !== null) setTime(v); });
      $(".ex-triple").addEventListener("click", () => { stop(); setTime(t < CLOCK_HALF - 1e-9 ? CLOCK_HALF : 0); });
      box.querySelectorAll(".ex-pair").forEach((c) => c.addEventListener("change", () => render(true)));
      $(".ex-reset").addEventListener("click", () => { stop(); setTime(0); });
      day.addEventListener("input", () => { stop(); setTime(Number(day.value)); });
      timeIn.addEventListener("change", () => {
        const m = /^\s*(\d{1,2})(?::(\d{1,2}))?(?::(\d{1,2}))?\s*$/.exec(timeIn.value);
        const [h, mi, se] = m ? [1, 2, 3].map((n) => Number(m[n] || 0)) : [];
        if (m && h < 24 && mi < 60 && se < 60) { stop(); setTime(h * 3600 + mi * 60 + se); }
        render(true);                                   // a bad entry falls back to the time shown
      });
      timeIn.addEventListener("keydown", (e) => { if (e.key === "Enter") timeIn.blur(); });

      // drag: the hand nearest to the finger follows it; a full turn of that hand moves the
      // time by its period (60 s, an hour or 12 hours)
      let drag = null;
      const where = (e) => {
        const r = svg.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width * 280 - C, y = (e.clientY - r.top) / r.height * 280 - C;
        return [((Math.atan2(x, -y) / (2 * Math.PI)) + 1) % 1, Math.hypot(x, y)];
      };
      const turnAt = (e) => where(e)[0];
      svg.addEventListener("pointerdown", (e) => {
        stop();
        const [at, rad] = where(e);
        const dist = (k) => { const d = Math.abs(((t / CLOCK_PERIOD[k]) % 1) - at); return Math.min(d, 1 - d); };
        const best = Math.min(...["s", "m", "h"].map(dist));
        const near = ["s", "m", "h"].filter((k) => dist(k) < best + 0.02);
        // hands on top of each other: the length of the hand under the finger decides
        const byLength = rad > 100 ? "s" : rad > 66 ? "m" : "h";
        const k = near.includes(byLength) ? byLength : near[0];
        drag = { k, at };
        svg.setPointerCapture(e.pointerId);
        svg.classList.add("is-dragging");
        e.preventDefault();
      });
      svg.addEventListener("pointermove", (e) => {
        if (!drag) return;
        const at = turnAt(e);
        let d = at - drag.at;
        if (d > 0.5) d -= 1;
        if (d < -0.5) d += 1;
        drag.at = at;
        setTime(t + d * CLOCK_PERIOD[drag.k]);
      });
      const end = () => { drag = null; svg.classList.remove("is-dragging"); };
      svg.addEventListener("pointerup", end);
      svg.addEventListener("pointercancel", end);
      render(true);
    },
  });

  // The strip box (0030): two wall panels where S and F can be dragged, sliders for the box,
  // and the periodic strip redrawn on every change with the eight images, the 48 lines and
  // the shortest valid one; the summary lists the path face by face.
  const stripView = () => ({
    mount(box) {
      const d = box.dataset;
      const defaults = { a: Number(d.a || 30), b: Number(d.b || 12), h: Number(d.h || 12),
                         y0: Number(d.y0 || 6), z0: Number(d.z0 || 11), y1: Number(d.y1 || 6), z1: Number(d.z1 || 1) };
      const st = { ...defaults };
      const HEB = { bottom: "הרצפה", sideB: "הקיר הרחוק", top: "התקרה", side0: "הקיר הקרוב", end0: "הקיר של העכביש", enda: "הקיר של הזבוב" };
      const num = (v) => { const s = Number(v).toFixed(2); return s.replace(/\.?0+$/, ""); };
      const p3 = (p) => `(${p.map(num).join(", ")})`;
      box.innerHTML =
        `<div class="ex-controls">` +
        [["a", "האורך a", 1, 60, 1], ["b", "הרוחב b", 1, 30, 1], ["h", "הגובה h", 1, 30, 1]].map(([k, label, min, max, step]) =>
          `<label><span>${label}</span><input type="range" class="ex-${k}" min="${min}" max="${max}" step="${step}" value="${st[k]}" dir="ltr"><output class="out-${k}"></output></label>`).join("") +
        `<label>הקווים <select class="ex-show"><option value="valid" selected>החוקיים</option><option value="all">כל 48</option><option value="best">הקצר בלבד</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="strip-walls">` +
        `<div class="strip-wall"><p>הקיר של העכביש, ‏<bdi dir="ltr">x = 0</bdi>: גררו את S</p><svg class="figure wall-s" role="img" aria-label="הקיר של העכביש"></svg>` +
        `<p class="strip-coords" dir="ltr"><label>y<sub>0</sub> <input type="number" class="ex-y0" step="0.25" min="0"></label> ` +
        `<label>z<sub>0</sub> <input type="number" class="ex-z0" step="0.25" min="0"></label></p></div>` +
        `<div class="strip-wall"><p>הקיר של הזבוב, ‏<bdi dir="ltr">x = a</bdi>: גררו את F</p><svg class="figure wall-f" role="img" aria-label="הקיר של הזבוב"></svg>` +
        `<p class="strip-coords" dir="ltr"><label>y<sub>1</sub> <input type="number" class="ex-y1" step="0.25" min="0"></label> ` +
        `<label>z<sub>1</sub> <input type="number" class="ex-z1" step="0.25" min="0"></label></p></div></div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<p class="ex-title">הרצועה המחזורית: הדמויות של S משמאל, של F מימין, והקווים ביניהן</p>` +
        `<div class="strip-chart"></div>` +
        `<span class="viz-legend"><span><i class="s1"></i>S והדמות הנבחרת שלו</span><span><i class="s2"></i>F והדמות הנבחרת שלו</span>` +
        `<span><i class="ink"></i>שאר הדמויות</span><span><i class="box-path"></i>המסלול הקצר ביותר</span>` +
        `<span><i class="strip-valid"></i>קו חוקי אחר</span><span><i class="strip-faint"></i>קו שנפסל</span>` +
        `<span><i class="s3"></i>צלעות היציאה והכניסה, והנקודות עליהן</span></span>` +
        `<p class="ex-title">המסלול, פאה אחרי פאה</p><div class="strip-segments"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const show = $(".ex-show"), summary = $(".ex-summary"), chart = $(".strip-chart"), segsBox = $(".strip-segments");
      const walls = { s: $(".wall-s"), f: $(".wall-f") };
      const inputs = {};
      ["a", "b", "h", "y0", "z0", "y1", "z1"].forEach((k) => { inputs[k] = $(`.ex-${k}`); });

      const clamp = () => {
        st.y0 = Math.min(Math.max(st.y0, 0), st.b); st.y1 = Math.min(Math.max(st.y1, 0), st.b);
        st.z0 = Math.min(Math.max(st.z0, 0), st.h); st.z1 = Math.min(Math.max(st.z1, 0), st.h);
      };
      // A wall panel: y to the right, z up; the hinge edge of the best line and its point.
      const wallSvg = (svg, who, res) => {
        const { b, h } = st, S = 11, pad = 26, W = b * S + 2 * pad, Hh = h * S + 2 * pad;
        const X = (y) => pad + y * S, Y = (z) => pad + (h - z) * S;
        const l = res.line, edge = who === "s" ? l.sEdge : l.fEdge, pt = who === "s" ? res.exit : res.enter;
        const me = who === "s" ? [st.y0, st.z0] : [st.y1, st.z1];
        const edges = { bottom: [[0, 0], [b, 0]], sideB: [[b, 0], [b, h]], top: [[0, h], [b, h]], side0: [[0, 0], [0, h]] };
        const [[ey0, ez0], [ey1, ez1]] = edges[edge];
        svg.setAttribute("viewBox", `0 0 ${W} ${Hh}`);
        svg.innerHTML =
          `<rect class="box-end" x="${X(0)}" y="${Y(h)}" width="${f(b * S)}" height="${f(h * S)}"/>` +
          `<line class="s3-line" x1="${f(X(ey0))}" y1="${f(Y(ez0))}" x2="${f(X(ey1))}" y2="${f(Y(ez1))}" stroke-width="5"><title>צלע ${who === "s" ? "היציאה" : "הכניסה"}: ${HEB[edge]}</title></line>` +
          `<line class="box-path" x1="${f(X(me[0]))}" y1="${f(Y(me[1]))}" x2="${f(X(pt[1]))}" y2="${f(Y(pt[2]))}" stroke-width="2.5"/>` +
          `<circle class="s3-dot" cx="${f(X(pt[1]))}" cy="${f(Y(pt[2]))}" r="4"><title>${who === "s" ? "נקודת היציאה" : "נקודת הכניסה"} ${p3(pt)}</title></circle>` +
          `<circle class="${who === "s" ? "s1" : "s2"}-dot wall-pt" cx="${f(X(me[0]))}" cy="${f(Y(me[1]))}" r="8"><title>${who.toUpperCase()} = ${p3(who === "s" ? [0, ...me] : [st.a, ...me])}</title></circle>` +
          `<text class="legend" x="${f(X(b / 2))}" y="${Hh - 6}" text-anchor="middle">y</text>` +
          `<text class="legend" x="${pad - 12}" y="${f(Y(h / 2) + 4)}" text-anchor="middle">z</text>` +
          `<text class="legend" x="${f(X(0))}" y="${Hh - 6}" text-anchor="middle" style="font-size:10px">0</text>` +
          `<text class="legend" x="${f(X(b))}" y="${Hh - 6}" text-anchor="middle" style="font-size:10px">${b}</text>` +
          `<text class="legend" x="${pad - 12}" y="${f(Y(h) + 4)}" text-anchor="middle" style="font-size:10px">${h}</text>`;
        svg.dataset.pad = pad; svg.dataset.s = S; svg.dataset.w = W; svg.dataset.h = Hh;
      };
      // The strip: p up, x to the right, one period of the lateral faces with a band of b
      // above and below for the shifted images.
      const stripSvg = (res) => {
        const { a, b, h } = st, P = stripPeriod(b, h);
        const bands = stripBands(b, h);
        const xmin = -h - 2, xmax = a + h + 2, pmin = -b, pmax = P + b;
        const S = Math.min(640 / (xmax - xmin), 420 / (pmax - pmin));
        const padL = 30, padT = 14, padR = 48, padB = 22;
        const W = (xmax - xmin) * S + padL + padR, Hh = (pmax - pmin) * S + padT + padB;
        const X = (x) => padL + (x - xmin) * S, Y = (p) => padT + (pmax - p) * S;
        let s = `<svg class="figure strip-live" viewBox="0 0 ${f(W)} ${f(Hh)}" role="img" aria-label="הרצועה המחזורית עם הדמויות של העכביש ושל הזבוב והקווים ביניהן">`;
        [-1, 0, 1].forEach((k) => STRIP_FACES.forEach((name) => {
          const lo = Math.max(bands[name][0] + k * P, pmin), hi = Math.min(bands[name][1] + k * P, pmax);
          if (hi <= lo) return;
          s += `<rect class="${k === 0 ? "box-face" : "box-copy"}" x="${f(X(0))}" y="${f(Y(hi))}" width="${f(a * S)}" height="${f((hi - lo) * S)}"><title>${HEB[name]}${k === 0 ? "" : " (עותק מחזורי)"}</title></rect>`;
          if (k === 0 && (hi - lo) * S > 14) s += `<text class="legend" x="${f(X(0) + 6)}" y="${f(Y(hi) + 14)}" style="font-size:12px">${name}</text>`;
        }));
        s += `<line class="axis-c" x1="${f(X(0))}" x2="${f(X(0))}" y1="${f(Y(pmin))}" y2="${f(Y(pmax))}" stroke-width="1.5"/>` +
             `<line class="axis-c" x1="${f(X(a))}" x2="${f(X(a))}" y1="${f(Y(pmin))}" y2="${f(Y(pmax))}" stroke-width="1.5"/>` +
             `<line class="ink-line" x1="${f(X(xmin))}" x2="${f(X(xmax))}" y1="${f(Y(0))}" y2="${f(Y(0))}" stroke-width="1" stroke-dasharray="4 3"/>` +
             `<line class="ink-line" x1="${f(X(xmin))}" x2="${f(X(xmax))}" y1="${f(Y(P))}" y2="${f(Y(P))}" stroke-width="1" stroke-dasharray="4 3"/>` +
             `<text class="legend" x="${f(X(0))}" y="${f(Hh - 6)}" text-anchor="middle" style="font-size:12px">x = 0</text>` +
             `<text class="legend" x="${f(X(a))}" y="${f(Hh - 6)}" text-anchor="middle" style="font-size:12px">x = ${a}</text>` +
             `<text class="legend" x="${f(X(xmax) + 4)}" y="${f(Y(0) - 3)}" style="font-size:10px">p = 0</text>` +
             `<text class="legend" x="${f(X(xmax) + 4)}" y="${f(Y(P) - 3)}" style="font-size:10px">p = ${P}</text>`;
        const mode = show.value, best = res.line;
        const seg = (l, cls, w) =>
          `<line class="${cls}" x1="${f(X(l.xs))}" y1="${f(Y(l.ps))}" x2="${f(X(l.xf))}" y2="${f(Y(l.pf))}" stroke-width="${w}">` +
          `<title>S דרך ${HEB[l.sEdge]}, F דרך ${HEB[l.fEdge]}${l.k ? `, k = ${l.k}` : ""}: ${num(l.length)}${l.valid ? "" : ", נפסל"}</title></line>`;
        if (mode === "all") res.lines.filter((l) => !l.valid).forEach((l) => { s += seg(l, "strip-faint", 1); });
        if (mode !== "best") res.lines.filter((l) => l.valid && l !== best).forEach((l) => { s += seg(l, "strip-valid", 1.3); });
        const sImg = stripImages(st.y0, st.z0, b, h), fImg = stripImages(st.y1, st.z1, b, h);
        const sEdge = sImg.find((i) => i.edge === best.sEdge), fEdge = fImg.find((i) => i.edge === best.fEdge);
        s += `<line class="s3-line" x1="${f(X(0))}" x2="${f(X(0))}" y1="${f(Y(sEdge.lo))}" y2="${f(Y(sEdge.hi))}" stroke-width="5"/>` +
             `<line class="s3-line" x1="${f(X(a))}" x2="${f(X(a))}" y1="${f(Y(fEdge.lo + best.k * P))}" y2="${f(Y(fEdge.hi + best.k * P))}" stroke-width="5"/>` +
             seg(best, "box-path", 3);
        sImg.forEach((i) => {
          const chosen = i.edge === best.sEdge;
          s += `<circle class="${chosen ? "s1" : "ink"}-dot" cx="${f(X(-i.gap))}" cy="${f(Y(i.p))}" r="${chosen ? 5 : 3.5}"><title>S דרך ${HEB[i.edge]}: x = −${num(i.gap)}, p = ${num(i.p)}</title></circle>`;
        });
        fImg.forEach((i) => [-1, 0, 1].forEach((k) => {
          const p = i.p + k * P;
          if (p < pmin || p > pmax) return;
          const chosen = i.edge === best.fEdge && k === best.k;
          s += `<circle class="${chosen ? "s2" : "ink"}-dot" cx="${f(X(a + i.gap))}" cy="${f(Y(p))}" r="${chosen ? 5 : 3.5}"><title>F דרך ${HEB[i.edge]}${k ? `, k = ${k}` : ""}: x = ${num(a + i.gap)}, p = ${num(p)}</title></circle>`;
        }));
        s += `<circle class="s3-dot" cx="${f(X(0))}" cy="${f(Y(best.pExit))}" r="4"><title>נקודת היציאה: p = ${num(best.pExit)}</title></circle>` +
             `<circle class="s3-dot" cx="${f(X(a))}" cy="${f(Y(best.pEnter))}" r="4"><title>נקודת הכניסה: p = ${num(best.pEnter)}</title></circle>` +
             `<text class="legend" x="${f(X((best.xs + best.xf) / 2) - 8)}" y="${f(Y((best.ps + best.pf) / 2) + 20)}" text-anchor="end" style="font-size:15px">d = ${num(best.length)}</text>`;
        return s + "</svg>";
      };
      const draw = () => {
        clamp();
        ["a", "b", "h"].forEach((k) => { $(`.out-${k}`).textContent = String(st[k]); inputs[k].value = st[k]; });
        ["y0", "z0", "y1", "z1"].forEach((k) => { if (document.activeElement !== inputs[k]) inputs[k].value = num(st[k]); });
        inputs.y0.max = inputs.y1.max = st.b; inputs.z0.max = inputs.z1.max = st.h;
        const res = stripBest(st.a, st.b, st.h, st.y0, st.z0, st.y1, st.z1);
        const air = Math.hypot(st.a, st.y1 - st.y0, st.z1 - st.z0);
        wallSvg(walls.s, "s", res);
        wallSvg(walls.f, "f", res);
        chart.innerHTML = stripSvg(res);
        summary.innerHTML = `המרחק הקצר ביותר הוא ${ltr(num(res.line.length))}, דרך ${res.faces.length} פאות: ${ltr(res.faces.join(" → "))}. ` +
          `העכביש עוזב את הקיר שלו ב-${ltr(p3(res.exit))} ונכנס לקיר של הזבוב ב-${ltr(p3(res.enter))}. ` +
          `מתוך 48 הקווים ${ltr(res.valid)} חוקיים; דרך האוויר המרחק הוא ${ltr(num(air))}.`;
        segsBox.innerHTML = `<table><thead><tr><th>הפאה</th><th>אורך הקטע</th><th>הנקודה בסוף הקטע</th></tr></thead><tbody>` +
          res.faces.map((name, i) => `<tr><td>${HEB[name]} <bdi dir="ltr">(${name})</bdi></td><td>${ltr(num(res.segs[i]))}</td><td>${ltr(p3(res.pts[i + 1]))}</td></tr>`).join("") +
          `</tbody></table>`;
        if (window.dvqDecorate) window.dvqDecorate(chart);
      };
      ["a", "b", "h"].forEach((k) => inputs[k].addEventListener("input", () => { st[k] = Number(inputs[k].value); draw(); }));
      ["y0", "z0", "y1", "z1"].forEach((k) => inputs[k].addEventListener("change", () => {
        const v = Number(inputs[k].value);
        if (Number.isFinite(v)) st[k] = v;
        draw();
      }));
      show.addEventListener("change", draw);
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, defaults); show.value = "valid"; draw(); });
      // drag S or F inside its wall
      Object.entries(walls).forEach(([who, svg]) => {
        let drag = false;
        const at = (e) => {
          const r = svg.getBoundingClientRect();
          const x = (e.clientX - r.left) / r.width * Number(svg.dataset.w), y = (e.clientY - r.top) / r.height * Number(svg.dataset.h);
          const pad = Number(svg.dataset.pad), S = Number(svg.dataset.s);
          const yy = Math.round(((x - pad) / S) * 4) / 4, zz = Math.round((st.h - (y - pad) / S) * 4) / 4;
          return [Math.min(Math.max(yy, 0), st.b), Math.min(Math.max(zz, 0), st.h)];
        };
        const move = (e) => {
          const [y, z] = at(e);
          if (who === "s") { st.y0 = y; st.z0 = z; } else { st.y1 = y; st.z1 = z; }
          draw();
        };
        svg.addEventListener("pointerdown", (e) => { drag = true; svg.setPointerCapture(e.pointerId); svg.classList.add("is-dragging"); move(e); e.preventDefault(); });
        svg.addEventListener("pointermove", (e) => { if (drag) move(e); });
        const end = () => { drag = false; svg.classList.remove("is-dragging"); };
        svg.addEventListener("pointerup", end);
        svg.addEventListener("pointercancel", end);
      });
      draw();
    },
  });

  // The hourglass box (0018: measure D from 0 by BFS; 0019: the earliest interval by
  // Dijkstra): sliders for A, B and D, the plan on a time axis with the flips marked and the
  // measured window framed, and the events one at a time with the two hourglasses.
  const hourglassView = (box) => ({
    mount(box2) {
      const interval = box.dataset.mode === "interval";
      const defaults = { A: Number(box.dataset.a || 7), B: Number(box.dataset.b || 11), D: Number(box.dataset.d || (interval ? 1 : 15)) };
      const st = { ...defaults, s: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        [["A", "שעון A (דקות)", 1, 30], ["B", "שעון B (דקות)", 1, 30], ["D", "המטרה D (דקות)", 1, 60]].map(([k, label, min, max]) =>
          `<label><span>${label}</span><input type="range" class="ex-${k}" min="${min}" max="${max}" step="1" value="${st[k]}" dir="ltr"><output class="out-${k}"></output></label>`).join("") +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<div class="hg-axis"></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button ex-prev">האירוע הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">האירוע הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button><span class="ex-pos"></span></div>` +
        `<div class="hg-frame"></div><p class="hg-caption"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play");
      let timer = null, uid = 0;
      const HEB = { "": "לא הופכים כלום", A: "הופכים את A", B: "הופכים את B", AB: "הופכים את A ואת B" };
      // one hourglass glyph, as tools/figures/hourglass.py draws it
      const glass = (x, y, top, total, kind) => {
        const W = 30, H = 50, NECK = 3, cx = x + W / 2, mid = y + H / 2;
        uid += 1;
        const id = `exhg${uid}`;
        const bt = `${x},${y} ${x + W},${y} ${cx + NECK},${mid} ${cx - NECK},${mid}`;
        const bb = `${cx - NECK},${mid} ${cx + NECK},${mid} ${x + W},${y + H} ${x},${y + H}`;
        const th = (H / 2) * top / total, bh = (H / 2) * (total - top) / total;
        let s = `<clipPath id="${id}t"><polygon points="${bt}"/></clipPath><clipPath id="${id}b"><polygon points="${bb}"/></clipPath>`;
        if (top) s += `<rect class="sand-${kind}" clip-path="url(#${id}t)" x="${x}" y="${f(mid - th)}" width="${W}" height="${f(th)}"/>` +
                      `<line class="stream-${kind}" x1="${cx}" y1="${mid}" x2="${cx}" y2="${f(y + H - bh - 1)}"/>`;
        if (total - top) s += `<rect class="sand-${kind}" clip-path="url(#${id}b)" x="${x}" y="${f(y + H - bh)}" width="${W}" height="${f(bh)}"/>`;
        s += `<polygon class="glass" points="${bt}"/><polygon class="glass" points="${bb}"/>` +
             `<line class="frame" x1="${x - 4}" y1="${y}" x2="${x + W + 4}" y2="${y}"/><line class="frame" x1="${x - 4}" y1="${y + H}" x2="${x + W + 4}" y2="${y + H}"/>` +
             `<text class="tick" x="${x + W + 7}" y="${y + 12}">${top}</text><text class="tick" x="${x + W + 7}" y="${y + H - 2}">${total - top}</text>` +
             `<text class="legend" x="${cx}" y="${y + H + 15}" text-anchor="middle">${kind.toUpperCase()}</text>`;
        return s;
      };
      const pair = (x, y, a, b) => glass(x, y, a, st.A, "a") + glass(x + 64, y, b, st.B, "b");
      const frameSvg = (ev, measuring, verdict) => {
        const [t, act, before, after] = ev, cy = 12 + 25;
        let s = `<svg class="figure hourglass-fig" viewBox="0 0 460 92" style="max-width:29rem" role="img" aria-label="אירוע ברגע ${t}">`;
        if (measuring) s += `<rect class="measure" x="2" y="2" width="456" height="88" rx="6"/>`;
        s += `<text class="legend" x="10" y="${cy - 4}" font-weight="700">t = ${t}</text><text class="tick" x="10" y="${cy + 14}">${verdict.event}</text>` + pair(92, 12, before[0], before[1]);
        if (after === null) s += `<text class="legend" x="226" y="${cy + 5}" font-weight="700">${verdict.text}</text>`;
        else s += `<line class="ink-line" x1="222" y1="${cy}" x2="306" y2="${cy}" stroke-width="1.5"/><polygon class="ink-fill" points="312,${cy} 304,${cy - 4} 304,${cy + 4}"/>` +
                  `<text class="legend" x="267" y="${cy - 8}" text-anchor="middle">${verdict.text}</text>` + pair(336, 12, after[0], after[1]);
        return s + "</svg>";
      };
      const axisSvg = (events, start, end) => {
        const w = 640, x0 = 30, x1 = 610, y = 40, last = Math.max(end, 1);
        const X = (t) => x0 + (t / last) * (x1 - x0);
        let s = `<svg class="perf-chart hg-live" viewBox="0 0 ${w} 78" role="img" aria-label="ציר הזמן של התוכנית: האירועים, ההיפוכים וחלון המדידה">`;
        if (start !== null) s += `<rect class="measure" x="${f(X(start))}" y="${y - 22}" width="${f(X(end) - X(start))}" height="44" rx="4"/>`;
        s += `<line class="axis" x1="${x0}" x2="${x1}" y1="${y}" y2="${y}"/>`;
        events.forEach(([t, act], i) => {
          const cur = i === st.s;
          s += `<line class="${cur ? "s2-line" : "ink-line"}" x1="${f(X(t))}" x2="${f(X(t))}" y1="${y - 10}" y2="${y + 10}" stroke-width="${cur ? 3 : 1.5}"/>` +
               `<text class="tick" x="${f(X(t))}" y="${y + 26}" text-anchor="middle">${t}</text>` +
               (act ? `<text class="legend" x="${f(X(t))}" y="${y - 14}" text-anchor="middle" style="font-size:11px">${act === "AB" ? "A+B" : act}</text>` : "");
        });
        return s + "</svg>";
      };
      const solve = () => {
        if (interval) { const r = hourglassInterval(st.A, st.B, st.D); return r ? { start: r.start, plan: r.plan, end: r.start + st.D } : null; }
        const plan = hourglassSolve(st.A, st.B, st.D);
        return plan ? { start: 0, plan, end: st.D } : null;
      };
      const draw = () => {
        ["A", "B", "D"].forEach((k) => { $(`.out-${k}`).textContent = String(st[k]); });
        const res = solve();
        const summary = $(".ex-summary");
        if (!res) {
          const g = (u, v) => (v ? g(v, u % v) : u);
          st.s = 0;
          summary.innerHTML = `עם שעונים של ${ltr(st.A)} ו-${ltr(st.B)} דקות אי אפשר למדוד ${ltr(st.D)} דקות${interval ? "" : " מרגע 0"}` +
            (st.D % g(st.A, st.B) ? `: ‏${ltr(st.D)} איננו כפולה של ${ltr(`gcd(${st.A}, ${st.B}) = ${g(st.A, st.B)}`)}.` : ".") +
            (interval ? "" : ` מרגע 0 אפשר למדוד: ${ltr(hourglassReachable(st.A, st.B, 60).join(", "))} (עד 60).`);
          $(".hg-axis").innerHTML = ""; $(".hg-frame").innerHTML = ""; $(".hg-caption").textContent = ""; $(".ex-pos").textContent = "";
          $(".ex-prev").disabled = $(".ex-next").disabled = true;
          return;
        }
        const events = hourglassReplay(st.A, st.B, res.plan, res.end);
        st.s = Math.min(Math.max(st.s, 0), events.length - 1);
        const flips = res.plan.map(([t, act]) => `${ltr(t)}: ${HEB[act]}`).join("; ");
        summary.innerHTML = (interval ? `המדידה שמסתיימת הכי מוקדם: מרגע ${ltr(res.start)} עד רגע ${ltr(res.end)}, ‏${ltr(`${res.end} − ${res.start} = ${st.D}`)}. ` : `מודדים ${ltr(st.D)} דקות מרגע 0 ב-${ltr(events.length - 1)} אירועים. `) +
          `התוכנית: ${flips}.` + (interval ? "" : ` מרגע 0 אפשר למדוד גם: ${ltr(hourglassReachable(st.A, st.B, 60).filter((v) => v !== st.D).slice(0, 12).join(", "))}, ...`);
        $(".hg-axis").innerHTML = axisSvg(events, interval ? res.start : null, res.end);
        const ev = events[st.s], [t, act, before, after] = ev;
        // which hourglass ran out: the one whose sand on top after the previous action equals the wait
        const prevEv = st.s > 0 ? events[st.s - 1] : null;
        const out = [];
        if (prevEv) { const w = t - prevEv[0]; if (prevEv[3][0] === w) out.push("A"); if (prevEv[3][1] === w) out.push("B"); }
        const what = st.s === 0 ? "start" : `${out.join(" + ")} run${out.length === 1 ? "s" : ""} out`;
        const ran = st.s === 0 ? "התחלה" : out.length === 2 ? "שני השעונים נגמרים" : `שעון ${out[0]} נגמר`;
        const done = st.s === events.length - 1;
        const flip = act ? `flip ${act === "AB" ? "A + B" : act}` : "";
        let verdict;
        if (done) verdict = { event: what, text: interval ? `STOP ✓ ${res.end} − ${res.start} = ${st.D}` : `✓ D = ${st.D}` };
        else if (interval && t === res.start) verdict = { event: what, text: flip ? `START, ${flip}` : "START" };
        else verdict = { event: what, text: flip || "wait" };
        $(".hg-frame").innerHTML = frameSvg(ev, interval && t >= res.start, verdict);
        $(".hg-caption").innerHTML = `רגע ${ltr(t)}: ${ran}. חול למעלה: ${ltr(`A = ${before[0]}, B = ${before[1]}`)}. ` +
          (done ? (interval ? `מסיימים: נמדדו ${ltr(st.D)} דקות מרגע ${ltr(res.start)}.` : `עברו בדיוק ${ltr(st.D)} דקות מרגע 0.`)
            : `${interval && t === res.start ? "מתחילים למדוד, ו" : ""}${HEB[act]}${act ? `; אחרי ההיפוך למעלה ${ltr(`A = ${after[0]}, B = ${after[1]}`)}` : ""}.`);
        $(".ex-pos").textContent = `אירוע ${st.s + 1} מתוך ${events.length}`;
        $(".ex-prev").disabled = st.s <= 0; $(".ex-next").disabled = done;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const count = () => { const r = solve(); return r ? hourglassReplay(st.A, st.B, r.plan, r.end).length : 0; };
      $(".ex-next").addEventListener("click", () => { stop(); st.s += 1; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s -= 1; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (!count()) return;
        if (st.s >= count() - 1) st.s = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { if (st.s >= count() - 1) { stop(); return; } st.s += 1; draw(); }, 1100);
        draw();
      });
      ["A", "B", "D"].forEach((k) => $(`.ex-${k}`).addEventListener("input", () => { stop(); st[k] = Number($(`.ex-${k}`).value); st.s = 0; draw(); }));
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, defaults, { s: 0 }); ["A", "B", "D"].forEach((k) => { $(`.ex-${k}`).value = st[k]; }); draw(); });
      draw();
    },
  });

  // The probability box (0015): p, q and the number of children move the answer; for two
  // children an area-proportional grid of the four kinds of child, and a curve of the
  // answer against q for the chosen p and C.
  const probabilityView = () => ({
    mount(box) {
      const QS = [["1", "בלי תכונה (q = 1)"], ["0.5", "הטלת מטבע (q = 1/2)"], ["0.14285714285714285", "יום בשבוע (q = 1/7)"],
                  ["0.08333333333333333", "חודש בשנה (q = 1/12)", ], ["0.0027397260273972603", "יום בשנה (q = 1/365)"]];
      const defaults = { p: Number(box.dataset.p || 0.5), q: QS[2][0], C: Number(box.dataset.c || 2) };
      const st = { ...defaults };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>ההסתברות לבן p</span><input type="range" class="ex-p" min="0.05" max="0.95" step="0.05" value="${st.p}" dir="ltr"><output class="out-p"></output></label>` +
        `<label>התכונה <select class="ex-q">${QS.map(([v, n]) => `<option value="${v}"${v === st.q ? " selected" : ""}>${n}</option>`).join("")}</select></label>` +
        `<label><span>מספר הילדים C</span><input type="range" class="ex-C" min="1" max="6" step="1" value="${st.C}" dir="ltr"><output class="out-C"></output></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p><div class="prob-box"><div class="prob-grid"></div><div class="prob-chart"></div></div>`;
      const $ = (sel) => box.querySelector(sel);
      const gridSvg = (p, q) => {
        // child 1 along the rows, child 2 along the columns; four kinds each, with areas
        // proportional to their probabilities
        const kinds = [["בן, עם", p * q, true, true], ["בן, בלי", p * (1 - q), true, false], ["בת, עם", (1 - p) * q, false, true], ["בת, בלי", (1 - p) * (1 - q), false, false]];
        const S = 240, x0 = 70, y0 = 30;
        let s = `<svg class="figure prob-live" viewBox="0 0 ${x0 + S + 10} ${y0 + S + 10}" style="max-width:21rem" role="img" aria-label="ריבוע ההסתברות של שני ילדים: שטח כל משבצת הוא ההסתברות של הזוג">`;
        let cy = y0;
        kinds.forEach(([n1, w1, boy1, tr1]) => {
          let cx = x0 + S;
          kinds.forEach(([n2, w2, boy2, tr2]) => {
            const cw = w2 * S, ch = w1 * S;
            cx -= cw;
            const cond = (boy1 && tr1) || (boy2 && tr2), hit = cond && boy1 && boy2;
            if (cw > 0.2 && ch > 0.2) s += `<rect class="${hit ? "pg-hit" : cond ? "pg-cond" : "pg-out"}" x="${f(cx)}" y="${f(cy)}" width="${f(cw)}" height="${f(ch)}"><title>${n1} / ${n2}: ${fmt(w1 * w2, 4)}</title></rect>`;
          });
          if (w1 * S > 11) s += `<text class="pg-day" x="${x0 - 6}" y="${f(cy + (w1 * S) / 2 + 4)}" text-anchor="start" direction="rtl">${n1}</text>`;
          cy += w1 * S;
        });
        let cx = x0 + S;
        kinds.forEach(([n2, w2]) => { cx -= w2 * S; if (w2 * S > 30) s += `<text class="pg-day" x="${f(cx + (w2 * S) / 2)}" y="${y0 - 8}" text-anchor="middle" direction="rtl">${n2}</text>`; });
        s += `<rect class="pg-quad" x="${x0 + S - p * S}" y="${y0}" width="${f(p * S)}" height="${f(p * S)}"/>`;
        return s + "</svg>";
      };
      const curveSvg = (p, C, q) => {
        const fr = frame("התשובה כפונקציה של q", 100, 1, [0, 0.25, 0.5, 0.75, 1]);
        let s = fr.s;
        const pts = [];
        for (let i = 1; i <= 100; i++) { const qq = i / 100; pts.push(`${f(fr.cx(i))},${f(fr.Y(probabilityAnswer(C, p, qq)))}`); }
        s += `<polyline class="s1-line" points="${pts.join(" ")}" fill="none" stroke-width="2.5"/>`;
        s += hline(fr, Math.pow(p, C - 1), `q → 0: p^(C−1) = ${fmt(Math.pow(p, C - 1))}`);
        s += `<circle class="s2-dot" cx="${f(fr.cx(Math.max(q * 100, 0.5)))}" cy="${f(fr.Y(probabilityAnswer(C, p, q)))}" r="6"/>`;
        [1, 25, 50, 75, 100].forEach((i) => { s += fr.xtick(i, (i / 100).toFixed(2)); });
        return s + fr.close();
      };
      const draw = () => {
        const p = st.p, q = Number(st.q), C = st.C;
        $(".out-p").textContent = String(p); $(".out-C").textContent = String(C);
        const PT = 1 - Math.pow(1 - p * q, C), PAT = Math.pow(p, C) * (1 - Math.pow(1 - q, C)), ans = probabilityAnswer(C, p, q);
        $(".ex-summary").innerHTML = `עם ${ltr(`p = ${p}`)}, ‏${ltr(`q = ${fmt(q, 4)}`)} ו-${ltr(`C = ${C}`)}: ‏${ltr(`P(T) = ${fmt(PT, 4)}`)}, ‏${ltr(`P(A ∩ T) = ${fmt(PAT, 4)}`)}, ` +
          `ולכן ${ltr(`P(A | T) = ${fmt(ans, 4)}`)}. בלי התכונה (${ltr("q = 1")}) התשובה היא ${ltr(fmt(Math.pow(p, C) / (1 - Math.pow(1 - p, C)), 4))}, ` +
          `ועם תכונה נדירה מאוד היא שואפת ל-${ltr(`p^(C−1) = ${fmt(Math.pow(p, C - 1), 4)}`)}.`;
        $(".prob-grid").innerHTML = C === 2 ? `<p class="ex-title">שני ילדים: שטח כל משבצת הוא ההסתברות של הזוג; הריבוע המקווקו הוא "שני בנים"</p>${gridSvg(p, q)}` +
          `<span class="viz-legend"><span><i class="pg-hit"></i>מקיים את התנאי, ושני הילדים בנים</span><span><i class="pg-cond"></i>מקיים את התנאי, יש גם בת</span><span><i class="pg-out"></i>לא מקיים את התנאי</span></span>`
          : `<p class="ex-title">הריבוע מצויר רק לשני ילדים; עם ${C} ילדים המספרים בשורה שלמעלה</p>`;
        $(".prob-chart").innerHTML = `<p class="ex-title">התשובה כפונקציה של q, עם p ו-C הנבחרים; הנקודה היא q הנבחר</p>${curveSvg(p, C, q)}`;
        if (window.dvqDecorate) window.dvqDecorate(box);
      };
      $(".ex-p").addEventListener("input", () => { st.p = Number($(".ex-p").value); draw(); });
      $(".ex-C").addEventListener("input", () => { st.C = Number($(".ex-C").value); draw(); });
      $(".ex-q").addEventListener("change", () => { st.q = $(".ex-q").value; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, defaults); $(".ex-p").value = st.p; $(".ex-C").value = st.C; $(".ex-q").value = st.q; draw(); });
      draw();
    },
  });

  const VIEWS = {
    "cake-arith": () => cakeView("arith"),
    "cake-geo": () => cakeView("geo"),
    motorcycle: motorcycleView,
    josephus: josephusView,
    clock: clockView,
    strip: stripView,
    hourglass: hourglassView,
    probability: probabilityView,
  };

  // --- the box -----------------------------------------------------------------------------

  const setup = (box) => {
    const make = VIEWS[box.dataset.kind];
    if (!make) return;
    const view = make(box);
    if (view.mount) { view.mount(box); return; }      // a box with its own controls
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
      if (window.dvqDecorate) window.dvqDecorate(charts);   // enlarge buttons (reading-tools.js)
    };
    draw();
  };

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".explorer").forEach(setup);
  });
})();
