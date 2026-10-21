// Interactive explorers: a box `<div class="explorer" data-kind="..." data-...>` gets
// sliders, a summary line and charts that redraw on every change. One model per kind:
//   cake-arith / cake-geo  0027, 0028  the law, sliders a and d (or q), and a person-by-person stepper of the cake
//   motorcycle             0026        sliders t0 and t1, a strategy, and play: the travellers on the road and the chart
//   josephus               0016, 0022  sliders N (and L), and the circle played step by step; the survivor chart
//   clock                  0029        a clock face to drag, play or type: meetings of the hands so far
//   strip                  0030        drag the spider and the fly on their walls: the periodic strip and the path
//   hourglass              0018, 0019  A, B and D: the plan on a time axis and event by event (BFS or Dijkstra)
//   probability            0015        p, q and C: the answer, the two-children square and the curve against q
//   bridge                 0031        crossing times: the Dijkstra plan played crossing by crossing
//   river                  0032        cross by hand or let the BFS plan play; the state graph follows
//   pcie                   0020, 0021  address, length, MPS and RCB: the blocks, the count and the map of splits
//   fifo                   0033        burst, write and read rates, a skipping reader: the fill level over time
//   mtbf                   0037        clock and data rates, tau, T0 and overhead: the MTBF of one to three flops
//   triangle               0007        three points to drag or type, inside / edge / outside; play counts every triangle
//   polygon                0007        the same for n vertices (3 to 10): drag, type or draw; random draws against 1 - n / 2^(n-1)
//   boxes                  0009        N boxes on a ring with their cycles, person 0's cut, a walk box by box, rounds without person 0
//   floyd                  0017        the array as the graph i -> nums[i], the tortoise and the hare through both phases
//   bfs01                  0005        the remainders modulo x on a ring, the BFS tree one dequeue at a time, the answer read back
//   brackets               0010        a typed bracket string read character by character: the stack, the depth chart, the first failure
//   ttt                    0011        tap cells on a 3 x 3 board: is it a legal final board and why not; random legal boards; wrap diagonals
//   shapes                 0014        squares or rectangles drawn one at a time with the rejected candidates flashed; a heat map of draws
//   kaprekar               0012, 0013  a number, its sort-and-subtract chain to 495 / 6174, the histogram of chain lengths
//   eurovision             0008        the announcements one by one: the cups under Israel's total against the points left; a what-if box
//   boxes3                 0004        three mislabelled boxes with hidden contents: draw a ball, the deduction line by line
//   edge                   0001        sig drawn cell by cell on a timing strip; sig_q and pulse follow, for a rising, falling or any edge; the reset trap
//   lfsr                   0036        tick the taps, step or play from 0001 on a ring of the 15 states; the output bits; the eight polynomials and their periods
//   div3                   0035        the half-cycle model one clock edge at a time: cnt, a, b and clk_out on a strip, the duty measured; a wake-up in state 3
//   gray                   0034        a pointer step through a synchroniser, bit by bit, in binary and in Gray; a 16-entry FIFO with 5-bit pointers and the flags
// The math of each model is exported under Node, where the question tests compare it with
// the Python reference (tests/0001, 0004, 0005, 0007, 0008, 0009, 0010, 0011, 0012, 0013, 0014, 0015, 0017, 0016, 0018 to 0022, 0026 to 0037).
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

  // Bridge and torch (0031): Dijkstra over (who is across, torch side); a crossing of one
  // or two people from the torch's bank costs the time of the slower. Returns the least
  // time and the crossings as arrays of indices, as the page code does.
  const bridgeSolve = (times) => {
    const n = times.length, everyone = (1 << n) - 1, S = 2 << n;
    const reach = new Array(S).fill(Infinity), prev = new Array(S).fill(-1), via = new Array(S).fill(0), closed = new Array(S).fill(false);
    reach[0] = 0;
    for (;;) {
      let cur = -1;
      for (let s = 0; s < S; s++) if (!closed[s] && (cur < 0 || reach[s] < reach[cur])) cur = s;
      if (cur < 0 || reach[cur] === Infinity) break;
      closed[cur] = true;
      const across = cur >> 1, side = cur & 1;
      if (across === everyone) break;
      for (let i = 0; i < n; i++) {
        if (((across >> i) & 1) !== side) continue;
        for (let j = i; j < n; j++) {
          if (((across >> j) & 1) !== side) continue;
          const cost = Math.max(times[i], times[j]);
          const nxt = ((across ^ (1 << i) ^ (j === i ? 0 : 1 << j)) << 1) | (1 - side);
          if (reach[cur] + cost < reach[nxt]) { reach[nxt] = reach[cur] + cost; prev[nxt] = cur; via[nxt] = (1 << i) | (1 << j); }
        }
      }
    }
    const moves = [];
    for (let s = (everyone << 1) | 1; prev[s] >= 0; s = prev[s]) {
      const g = [];
      for (let i = 0; i < n; i++) if (via[s] & (1 << i)) g.push(i);
      moves.unshift(g);
    }
    return { time: reach[(everyone << 1) | 1], moves };
  };
  const bridgeEscort = (times) => { const s = [...times].sort((u, v) => u - v); return s.length < 3 ? s[s.length - 1] : s[0] * (s.length - 2) + s.slice(1).reduce((u, v) => u + v, 0); };

  // Wolf, goat and cabbage (0032): a state is four bits (farmer 1, wolf 2, goat 4,
  // cabbage 8; 0 near, 1 far). riverSafe is the page's test, riverMoves the crossings
  // from a state as [item, new state], riverPlan the BFS plan (what the farmer takes).
  const RIVER = { farmer: 1, wolf: 2, goat: 4, cabbage: 8 };
  const riverSafe = (s) => {
    const f = !!(s & 1), w = !!(s & 2), g = !!(s & 4), c = !!(s & 8);
    return g === f || (g !== w && g !== c);
  };
  const riverMoves = (s) => {
    const out = [];
    [null, "wolf", "goat", "cabbage"].forEach((item) => {
      if (item && !!(s & RIVER[item]) !== !!(s & 1)) return;
      out.push([item, s ^ 1 ^ (item ? RIVER[item] : 0)]);
    });
    return out;
  };
  const riverPlan = () => {
    const parent = new Map([[0, null]]);
    const queue = [0];
    for (let head = 0; head < queue.length; head++) {
      const s = queue[head];
      if (s === 15) break;
      riverMoves(s).forEach(([item, nxt]) => {
        if (riverSafe(nxt) && !parent.has(nxt)) { parent.set(nxt, [s, item]); queue.push(nxt); }
      });
    }
    const plan = [];
    for (let s = 15; parent.get(s) !== null; ) { const [p, item] = parent.get(s); plan.unshift(item); s = p; }
    return plan;
  };

  // PCIe completion splits (0020, 0021): a read of `len` bytes from `addr` is answered by
  // completions that cut only on RCB boundaries and never exceed MPS. pcieBlocks gives the
  // N blocks (f, RCB, ..., RCB, e), pcieSplits enumerates the splits in the page's order
  // (largest cut first; `limit` stops early), pcieCount counts them by a dynamic program
  // over the cut points, pcieByCompletions splits that count by the number of completions,
  // and pcieFormula is the closed form of 0021: S(N) - S(N - 1) + delta with
  // S(n) = sum_j (-1)^j C(n - m j, j) 2^(n - (m + 1) j), m = MPS / RCB. Counts are BigInt
  // (a 4 KB request over RCB 64 has 63 boundaries).
  const pcieBoundaries = (addr, len, rcb) => {
    const out = [];
    for (let b = (Math.floor(addr / rcb) + 1) * rcb; b < addr + len; b += rcb) out.push(b);
    return out;
  };
  const pciePoints = (addr, len, rcb) => [addr, ...pcieBoundaries(addr, len, rcb), addr + len];
  const pcieBlocks = (addr, len, rcb) => {
    const pts = pciePoints(addr, len, rcb);
    return pts.slice(1).map((b, i) => b - pts[i]);
  };
  const pcieSplits = (addr, len, mps, rcb, limit = Infinity) => {
    const end = addr + len, out = [];
    const extend = (pos, sizes) => {
      if (out.length >= limit) return;
      if (pos === end) { out.push(sizes); return; }
      const cuts = pos + mps >= end ? [end] : [];
      for (let b = (Math.floor(pos / rcb) + 1) * rcb; b < end && b <= pos + mps; b += rcb) cuts.push(b);
      cuts.sort((a, b) => b - a).forEach((cut) => extend(cut, sizes.concat([cut - pos])));
    };
    extend(addr, []);
    return out;
  };
  const pcieByCompletions = (addr, len, mps, rcb) => {
    // ways[i][k] = number of ways to cover pts[i]..end with k completions
    const pts = pciePoints(addr, len, rcb), n = pts.length;
    const ways = Array.from({ length: n }, () => []);
    ways[n - 1] = [1n];
    for (let i = n - 2; i >= 0; i--) {
      const row = [];
      for (let j = i + 1; j < n && pts[j] - pts[i] <= mps; j++) {
        ways[j].forEach((w, k) => { row[k + 1] = (row[k + 1] || 0n) + w; });
      }
      ways[i] = row;
    }
    return Array.from(ways[0], (w) => w || 0n);   // index k = number of completions (index 0 is 0)
  };
  const pcieCount = (addr, len, mps, rcb) => pcieByCompletions(addr, len, mps, rcb).reduce((a, b) => a + b, 0n);
  const bigComb = (n, k) => {
    if (k < 0 || k > n) return 0n;
    let r = 1n;
    for (let i = 1; i <= k; i++) r = (r * BigInt(n - k + i)) / BigInt(i);
    return r;
  };
  const pcieS = (n, m) => {
    if (n < 0) return 0n;
    let s = 0n;
    for (let j = 0; j <= Math.floor(n / (m + 1)); j++) {
      const term = bigComb(n - m * j, j) * (1n << BigInt(n - (m + 1) * j));
      s += j % 2 ? -term : term;
    }
    return s;
  };
  const pcieFormula = (addr, len, mps, rcb) => {
    const m = mps / rcb, N = pcieBlocks(addr, len, rcb).length;
    const delta = N === m + 1 && len <= mps ? 1n : 0n;
    return pcieS(N, m) - pcieS(N - 1, m) + delta;
  };

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

  // Random triangle (0007): three whole angles in degrees on the unit circle. The three arcs
  // between the sorted points decide: every arc below 180 puts the centre inside, an arc of
  // exactly 180 puts it on an edge (that edge is a diameter), and a point on top of another
  // leaves no triangle at all.
  const TRI_M = 360;
  const triNorm = (v) => ((Math.round(v) % TRI_M) + TRI_M) % TRI_M;
  const triArcs = (angles) => {
    const a = angles.map(triNorm).sort((u, v) => u - v);
    return [a[1] - a[0], a[2] - a[1], TRI_M - (a[2] - a[0])];
  };
  const triClass = (angles) => {
    const arcs = triArcs(angles);
    if (arcs.includes(0) || arcs.includes(TRI_M)) return "degenerate";
    const top = Math.max(...arcs);
    return top < 180 ? "in" : top === 180 ? "edge" : "out";
  };
  // The enumeration of the play button: every set of three different angles a < b < c, in
  // increasing order (a first, then b, then c): C(360, 3) frames. For a fixed pair a < b,
  // how many c in (b, t] put the centre inside and how many on an edge (the rest outside).
  const TRI_TOTAL = (TRI_M * (TRI_M - 1) * (TRI_M - 2)) / 6;
  const triCountC = (a, b, t) => {
    if (t <= b) return { in: 0, edge: 0 };
    if (b - a === 180) return { in: 0, edge: t - b };      // a-b is a diameter for every c
    if (b - a > 180) return { in: 0, edge: 0 };             // arc a-b too long for every c
    const lo = Math.max(b + 1, a + 181), hi = Math.min(t, b + 179);   // arcs b-c and c-a below 180
    let edge = 0;
    if (a + 180 <= t) edge++;                               // c = a + 180: arc c-a is 180
    if (b + 180 <= t) edge++;                               // c = b + 180: arc b-c is 180
    return { in: Math.max(0, hi - lo + 1), edge };
  };
  // Running totals per pair (a, b), built once: the frame where the pair starts and the
  // counts of every frame before it.
  let triTables = null;
  const triTable = () => {
    if (triTables) return triTables;
    const P = ((TRI_M - 1) * (TRI_M - 2)) / 2;              // pairs a < b <= 358 (b = 359 has no c)
    const start = new Float64Array(P + 1), cin = new Int32Array(P + 1), cedge = new Int32Array(P + 1);
    const pa = new Uint16Array(P), pb = new Uint16Array(P);
    let p = 0;
    for (let a = 0; a < TRI_M - 2; a++) {
      for (let b = a + 1; b < TRI_M - 1; b++) {
        const n = triCountC(a, b, TRI_M - 1);
        pa[p] = a; pb[p] = b;
        start[p + 1] = start[p] + (TRI_M - 1 - b);
        cin[p + 1] = cin[p] + n.in;
        cedge[p + 1] = cedge[p] + n.edge;
        p++;
      }
    }
    triTables = { P, start, cin, cedge, pa, pb };
    return triTables;
  };
  const triPairIndex = (a, b) => a * (TRI_M - 2) - (a * (a - 1)) / 2 + (b - a - 1);
  // frame k (0-based) -> the angles [a, b, c]
  const triFrame = (k) => {
    const T = triTable();
    k = Math.min(Math.max(Math.floor(k), 0), TRI_TOTAL - 1);
    let lo = 0, hi = T.P - 1;                               // last pair whose start <= k
    while (lo < hi) {
      const mid = (lo + hi + 1) >> 1;
      if (T.start[mid] <= k) lo = mid; else hi = mid - 1;
    }
    const a = T.pa[lo], b = T.pb[lo];
    return [a, b, b + 1 + (k - T.start[lo])];
  };
  // three different angles -> their frame
  const triIndex = (angles) => {
    const [a, b, c] = angles.map(triNorm).sort((u, v) => u - v);
    return triTable().start[triPairIndex(a, b)] + (c - b - 1);
  };
  // the counts of frames 0..k
  const triCounts = (k) => {
    const T = triTable();
    k = Math.min(Math.max(Math.floor(k), 0), TRI_TOTAL - 1);
    const [a, b, c] = triFrame(k);
    const p = triPairIndex(a, b), n = triCountC(a, b, c);
    const seen = k + 1, inside = T.cin[p] + n.in, edge = T.cedge[p] + n.edge;
    return { seen, in: inside, edge, out: seen - inside - edge };
  };

  // Boxes and cycles (0009): notes[b] is the note in box b (1..N), notes[0] unused. The
  // notes are a permutation; its cycles, person 0's one cut, one person's walk, and the
  // closed forms of the two success rates the box compares.
  const permCycles = (notes) => {
    const n = notes.length - 1, seen = new Set(), cycles = [];
    for (let s = 1; s <= n; s++) {
      if (seen.has(s)) continue;
      const c = [s]; seen.add(s);
      for (let b = notes[s]; b !== s; b = notes[b]) { c.push(b); seen.add(b); }
      cycles.push(c);
    }
    return cycles;
  };
  // person 0: the first and the middle box of the one cycle longer than maxOpens, or null
  const permHelper = (notes, maxOpens) => {
    for (const c of permCycles(notes)) if (c.length > maxOpens) return [c[0], c[c.length >> 1]];
    return null;
  };
  const permSwap = (notes, a, b) => { const out = [...notes]; out[a] = notes[b]; out[b] = notes[a]; return out; };
  // person `me`: the boxes opened in order, and whether the note was found
  const permWalk = (notes, me, maxOpens) => {
    const opened = [];
    let box = me;
    for (let k = 0; k < maxOpens; k++) {
      opened.push(box);
      if (notes[box] === me) return { opened, found: true };
      box = notes[box];
    }
    return { opened, found: false };
  };
  const permAllWin = (notes, maxOpens) => permCycles(notes).every((c) => c.length <= maxOpens);
  const permShuffle = (n, rnd = Math.random) => {
    const p = Array.from({ length: n }, (_, i) => i + 1);
    for (let i = n - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [p[i], p[j]] = [p[j], p[i]]; }
    return [0, ...p];
  };
  // every person opens maxOpens boxes chosen at random: do all of them find their note?
  const permRandomPicks = (notes, maxOpens, rnd = Math.random) => {
    const n = notes.length - 1;
    for (let me = 1; me <= n; me++) {
      const boxes = permShuffle(n, rnd).slice(1, maxOpens + 1);
      if (!boxes.some((b) => notes[b] === me)) return false;
    }
    return true;
  };
  // P(no cycle longer than maxOpens) for maxOpens >= n / 2: 1 - sum_{k > maxOpens} 1 / k
  const permStrategyProb = (n, maxOpens) => {
    let p = 1;
    for (let k = maxOpens + 1; k <= n; k++) p -= 1 / k;
    return p;
  };
  const permRandomProb = (n, maxOpens) => Math.pow(maxOpens / n, n);

  // Find the duplicate (0017): nums has n + 1 values in 1..n. The walk i -> nums[i] from
  // 0 is a tail and a cycle (the rho); the entry of the cycle is a duplicate value.
  const floydRho = (nums) => {
    const seen = new Map();                          // node -> position in the walk
    const walk = [];
    let x = 0;
    while (!seen.has(x)) { seen.set(x, walk.length); walk.push(x); x = nums[x]; }
    const mu = seen.get(x), tail = walk.slice(0, mu), cycle = walk.slice(mu);
    const reached = new Set(walk);
    const others = nums.map((_, i) => i).filter((i) => !reached.has(i));
    return { tail, cycle, entry: x, mu, lambda: cycle.length, others };
  };
  // the frames of the page's algorithm: {phase, step, slow, fast}, and the meeting node
  const floydTrace = (nums) => {
    const frames = [{ phase: 1, step: 0, slow: 0, fast: 0 }];
    let slow = 0, fast = 0, step = 0;
    do {
      slow = nums[slow]; fast = nums[nums[fast]]; step++;
      frames.push({ phase: 1, step, slow, fast });
    } while (slow !== fast);
    const meet = slow;
    slow = 0; step = 0;
    frames.push({ phase: 2, step, slow, fast });
    while (slow !== fast) {
      slow = nums[slow]; fast = nums[fast]; step++;
      frames.push({ phase: 2, step, slow, fast });
    }
    return { frames, meet, answer: slow };
  };
  // a random input like the page's test: 1..n, one value copied over another, shuffled
  const floydRandom = (n, rnd = Math.random) => {
    const nums = Array.from({ length: n }, (_, i) => i + 1);
    const v = 1 + Math.floor(rnd() * n);
    nums[Math.floor(rnd() * n)] = v;
    nums.push(v);
    for (let i = nums.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [nums[i], nums[j]] = [nums[j], nums[i]]; }
    return nums;
  };
  // "3, 9, 5" -> the array, or null when it is not n + 1 values in 1..n
  const floydParse = (text) => {
    const parts = String(text).trim().split(/[\s,;]+/).filter(Boolean);
    if (parts.length < 2 || parts.some((p) => !/^\d+$/.test(p))) return null;
    const nums = parts.map(Number), n = nums.length - 1;
    return nums.every((v) => v >= 1 && v <= n) ? nums : null;
  };

  // Smallest 0/1 multiple (0005): the page's BFS over the remainders modulo x, one frame
  // per dequeue: the remainder taken out, its two children (+0 first) with their fate,
  // and the queue after the step. Numbers are strings of digits (they outgrow 2^53).
  const bfs01Trace = (x) => {
    const parent = new Array(x).fill(-1), digit = new Array(x).fill(""), visited = new Array(x).fill(false);
    const start = 1 % x;
    visited[start] = true; digit[start] = "1";
    const number = (r) => { let s = ""; for (let q = r; q !== -1; q = parent[q]) s = digit[q] + s; return s; };
    const queue = [start], frames = [];
    while (!visited[0]) {
      const r = queue.shift(), kids = [];
      for (const d of [0, 1]) {
        const nr = (r * 10 + d) % x;
        if (!visited[nr]) { visited[nr] = true; parent[nr] = r; digit[nr] = String(d); queue.push(nr); kids.push({ d, nr, status: nr === 0 ? "found" : "new" }); }
        else kids.push({ d, nr, status: "seen" });
      }
      frames.push({ r, number: number(r), kids, queue: [...queue] });
    }
    const path = [];                                 // remainders from the start to 0
    for (let q = 0; q !== -1; q = parent[q]) path.unshift(q);
    return { frames, answer: number(0), path, parent, digit, start, dequeues: frames.length };
  };
  // the counts of the page's chart: multiples of x scanned, 0/1 numbers enumerated, dequeues
  const bfs01Counts = (x) => {
    const t = bfs01Trace(x), y = BigInt(t.answer);
    let enumerated = 0n;
    for (const ch of t.answer) enumerated = enumerated * 2n + BigInt(ch);
    return { multiples: (y / BigInt(x)).toString(), enumerated: enumerated.toString(), dequeues: t.dequeues, answer: t.answer };
  };

  // Valid parentheses (0010): the page's stack, one frame per character: push, pop, or
  // the first failure (a closer with an empty stack, or one that does not match the top);
  // openers left at the end are the third failure.
  const BRACKET_OF = { ")": "(", "]": "[", "}": "{" };
  const bracketsClean = (text) => [...String(text)].filter((c) => "()[]{}".includes(c)).join("");
  const bracketsTrace = (s) => {
    const frames = [], stack = [];
    let fail = null;
    for (let i = 0; i < s.length; i++) {
      const ch = s[i];
      if (ch in BRACKET_OF) {
        if (!stack.length) { fail = { i, kind: "unopened" }; frames.push({ i, ch, action: "unopened", stack: stack.join("") }); break; }
        const top = stack[stack.length - 1];
        if (top !== BRACKET_OF[ch]) { fail = { i, kind: "mismatch", top }; frames.push({ i, ch, action: "mismatch", stack: stack.join(""), top }); break; }
        stack.pop();
        frames.push({ i, ch, action: "pop", stack: stack.join("") });
      } else {
        stack.push(ch);
        frames.push({ i, ch, action: "push", stack: stack.join("") });
      }
    }
    if (!fail && stack.length) fail = { i: s.length, kind: "unclosed", left: stack.join("") };
    return { frames, valid: !fail, fail, odd: s.length % 2 === 1 };
  };

  // Tic-tac-toe final boards (0011): the page's four conditions on a board of "X", "O"
  // and "." (cells 0..8 row by row), with the reason a board fails; every legal final
  // board counted once per line set; a draw of the page's randomize().
  const TTT_LINES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
  const TTT_WRAP = TTT_LINES.concat([[1, 5, 6], [2, 3, 7], [0, 5, 7], [1, 3, 8]]);
  const tttCheck = (board, wrap = false) => {
    const lines = wrap ? TTT_WRAP : TTT_LINES;
    const nX = board.filter((c) => c === "X").length, nO = board.filter((c) => c === "O").length;
    const won = (p) => lines.map((l, i) => (l.every((c) => board[c] === p) ? i : -1)).filter((i) => i >= 0);
    const xLines = won("X"), oLines = won("O");
    let result = null, reason = null;
    if (nX !== nO && nX !== nO + 1) reason = "count";
    else if (xLines.length && oLines.length) reason = "both";
    else if (xLines.length) { if (nX === nO + 1) result = "X"; else reason = "o_after"; }
    else if (oLines.length) { if (nX === nO) result = "O"; else reason = "x_after"; }
    else if (nX + nO === 9) result = "draw";
    else reason = "unfinished";
    return { nX, nO, xLines, oLines, result, reason, lines };
  };
  let tttGroupsCache = {};
  const tttFinalBoards = (wrap = false) => {
    const key = wrap ? "wrap" : "plain";
    if (tttGroupsCache[key]) return tttGroupsCache[key];
    const groups = { X: [], O: [], draw: [] };
    const board = new Array(9).fill(".");
    for (let n = 0; n < 19683; n++) {
      let m = n;
      for (let i = 0; i < 9; i++) { board[i] = ".XO"[m % 3]; m = Math.floor(m / 3); }
      const r = tttCheck(board, wrap).result;
      if (r) groups[r].push(board.join(""));
    }
    tttGroupsCache[key] = groups;
    return groups;
  };
  const tttRandom = (wrap = false, rnd = Math.random) => {
    const groups = tttFinalBoards(wrap);
    const results = Object.keys(groups).filter((r) => groups[r].length);
    const result = results[Math.floor(rnd() * results.length)];
    const boards = groups[result];
    return { result, board: boards[Math.floor(rnd() * boards.length)].split("") };
  };

  // Random shapes without overlap (0014): a shape is [x1, y1, x2, y2] on an N x M grid of
  // points. The page's overlap test and candidate list; one shape drawn by rejection
  // (a candidate at random until one is free, so uniform among the free ones, like the
  // page's choice from the filtered list); a whole draw like random_shapes; a heat map.
  const shapesOverlap = (a, b) => a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3];
  const shapesCandidates = (N, M, squares) => {
    const out = [];
    for (let x1 = 1; x1 < N; x1++) for (let x2 = x1 + 1; x2 <= N; x2++)
      for (let y1 = 1; y1 < M; y1++) for (let y2 = y1 + 1; y2 <= M; y2++)
        if (!squares || x2 - x1 === y2 - y1) out.push([x1, y1, x2, y2]);
    return out;
  };
  const shapesOk = (N, M, shapes, squares) => shapes.every((s, k) =>
    1 <= s[0] && s[0] < s[2] && s[2] <= N && 1 <= s[1] && s[1] < s[3] && s[3] <= M &&
    (!squares || s[2] - s[0] === s[3] - s[1]) && !shapes.slice(0, k).some((t) => shapesOverlap(s, t)));
  // the tries of one draw: candidates picked at random, the last one free (or none free)
  const shapesTry = (N, M, shapes, squares, rnd = Math.random, cap = 60) => {
    const all = shapesCandidates(N, M, squares);
    const free = all.filter((c) => !shapes.some((s) => shapesOverlap(c, s)));
    if (!free.length) return { tries: [], shape: null, free: 0, all: all.length };
    const tries = [];
    for (let k = 0; k < cap; k++) {
      const c = all[Math.floor(rnd() * all.length)];
      tries.push(c);
      if (!shapes.some((s) => shapesOverlap(c, s))) return { tries, shape: c, free: free.length, all: all.length };
    }
    const c = free[Math.floor(rnd() * free.length)];               // the cap hit: pick free directly
    tries.push(c);
    return { tries, shape: c, free: free.length, all: all.length };
  };
  // the page's random_shapes: n uniform in 1..max, retry the whole set until n fit
  const shapesRandom = (N, M, maxShapes, squares, rnd = Math.random) => {
    const all = shapesCandidates(N, M, squares);
    // more shapes than unit cells can never fit (the page's loop would never return)
    const n = 1 + Math.floor(rnd() * Math.min(maxShapes, (N - 1) * (M - 1)));
    for (;;) {
      const shapes = [];
      for (let k = 0; k < n; k++) {
        const free = all.filter((c) => !shapes.some((s) => shapesOverlap(c, s)));
        if (!free.length) break;
        shapes.push(free[Math.floor(rnd() * free.length)]);
      }
      if (shapes.length === n) return shapes;
    }
  };
  // how often every unit cell is covered over `rounds` draws, and the side lengths seen
  const shapesHeat = (N, M, maxShapes, squares, rounds, rnd = Math.random) => {
    const cells = Array.from({ length: M - 1 }, () => new Array(N - 1).fill(0));
    const sides = new Array(Math.max(N, M)).fill(0);
    let count = 0;
    for (let r = 0; r < rounds; r++) {
      for (const [x1, y1, x2, y2] of shapesRandom(N, M, maxShapes, squares, rnd)) {
        count++;
        sides[Math.max(x2 - x1, y2 - y1)]++;
        for (let y = y1; y < y2; y++) for (let x = x1; x < x2; x++) cells[y - 1][x - 1]++;
      }
    }
    return { cells, sides, count, rounds };
  };

  // Sort the digits and subtract (0012 with 3 digits, 0013 with 4): one step of the
  // routine, the chain of steps until the value stops changing (495 or 6174, or 0 for
  // repeated digits), and the distribution of chain lengths over every number.
  const kapStep = (x, d) => {
    const digits = String(x).padStart(d, "0").split("").sort();
    const smallest = Number(digits.join("")), largest = Number(digits.slice().reverse().join(""));
    return { x, digits: digits.slice().reverse().join(""), largest, smallest, diff: largest - smallest, special: largest - smallest === x };
  };
  const kapChain = (x, d, cap = 12) => {
    const steps = [];
    let v = x;
    for (let k = 0; k < cap; k++) {
      const s = kapStep(v, d);
      steps.push(s);
      if (s.diff === v) break;
      v = s.diff;
    }
    const last = steps[steps.length - 1];
    return { steps, end: last.diff, length: steps.length - 1, fixed: last.diff === last.x };
  };
  const kapHistogram = (d) => {
    const hist = {}, ends = {};
    for (let x = 0; x < Math.pow(10, d); x++) {
      const c = kapChain(x, d);
      const key = c.end;
      ends[key] = (ends[key] || 0) + 1;
      if (!hist[key]) hist[key] = [];
      hist[key][c.length] = (hist[key][c.length] || 0) + 1;
    }
    return { hist, ends };
  };

  // Eurovision 2026 (0008): the grand final results, the announcement order (lowest jury
  // first), and the page's scan: after every announcement the public points left and the
  // room left under Israel's total; the first announcement after which Israel cannot win.
  const EURO_RESULTS = [
    ["Bulgaria", 204, 312], ["Israel", 123, 220], ["Romania", 64, 232], ["Australia", 165, 122], ["Italy", 134, 147],
    ["Finland", 141, 138], ["Denmark", 165, 78], ["Moldova", 43, 183], ["Ukraine", 54, 167], ["Greece", 73, 147],
    ["France", 144, 14], ["Poland", 133, 17], ["Albania", 60, 85], ["Norway", 115, 19], ["Croatia", 53, 71],
    ["Czechia", 104, 9], ["Serbia", 38, 52], ["Malta", 81, 8], ["Cyprus", 41, 34], ["Sweden", 35, 16],
    ["Belgium", 36, 0], ["Lithuania", 10, 12], ["Germany", 12, 0], ["Austria", 1, 5], ["United Kingdom", 1, 0],
  ];
  const EURO_PUBLIC_TOTAL = 36 * 58;
  // the order of the public announcements: by jury score, Denmark before Australia at 165
  const euroOrder = (results) => results.slice().sort((a, b) => a[1] - b[1] || (a[0] === "Australia") - (b[0] === "Australia"));
  // results with Israel's jury and public scores replaced (the "what if" box)
  const euroWithIsrael = (jury, pub) => EURO_RESULTS.map((r) => (r[0] === "Israel" ? ["Israel", jury, pub] : r));
  // the page's israel_cannot_win
  const euroCannotWin = (israelTotal, juryAbove, pointsLeft) => {
    let room = 0;
    for (const j of juryAbove) { if (j > israelTotal) return true; room += israelTotal - j; }
    return pointsLeft > room;
  };
  // the scan: one row per announcement from Israel's own on, with left, room and the verdict
  const euroScan = (results) => {
    const order = euroOrder(results);
    const idx = order.findIndex((r) => r[0] === "Israel");
    const total = order[idx][1] + order[idx][2];
    const above = order.slice(idx + 1);
    let left = EURO_PUBLIC_TOTAL - order.slice(0, idx + 1).reduce((s, r) => s + r[2], 0);
    let room = above.reduce((s, r) => s + Math.max(0, total - r[1]), 0);
    let lost = euroCannotWin(total, above.map((r) => r[1]), left);
    const rows = [{ country: "Israel", jury: order[idx][1], pub: order[idx][2], total, left, room, lost }];
    let passed = false;
    for (const [country, jury, pub] of above) {
      left -= pub;
      room -= Math.max(0, total - jury);
      passed = passed || jury + pub > total;
      lost = lost || passed || left > room;
      rows.push({ country, jury, pub, total: jury + pub, left, room, lost });
    }
    const first = rows.findIndex((r) => r.lost);               // 0 = right after Israel, -1 = never
    return { order, idx, total, above, rows, first, won: first < 0 };
  };

  // Three mislabelled boxes (0004): the twelve cases (a label order and a content where
  // every label is wrong), a draw from a box, and the page's rule applied to one draw.
  const BOX_LABELS = ["RED", "BLACK", "MIXED"];
  const boxesCases = () => {
    const perms = (a) => (a.length <= 1 ? [a] : a.flatMap((x, i) => perms(a.filter((_, j) => j !== i)).map((p) => [x, ...p])));
    const out = [];
    for (const labels of perms(BOX_LABELS)) for (const content of perms(BOX_LABELS))
      if (labels.every((l, i) => l !== content[i])) out.push({ labels, content });
    return out;
  };
  const boxesDraw = (content, i, rnd = Math.random) => (content[i] === "MIXED" ? (rnd() < 0.5 ? "RED" : "BLACK") : content[i]);
  // the page's fix_labels_simple, given the ball drawn from the box labelled MIXED
  const boxesFix = (labels, ball) => {
    const k = labels.indexOf("MIXED"), other = ball === "RED" ? "BLACK" : "RED", fixed = ["", "", ""];
    fixed[k] = ball;
    labels.forEach((l, i) => { if (l === ball) fixed[i] = other; });
    labels.forEach((l, i) => { if (l === other) fixed[i] = "MIXED"; });
    return fixed;
  };
  // what a draw from box i tells: the contents still possible afterwards
  const boxesDeduce = (labels, i, ball) => {
    const possible = boxesCases().filter((c) => c.labels.join() === labels.join()).map((c) => c.content);
    return possible.filter((content) => content[i] === ball || content[i] === "MIXED");
  };

  // Polygon on the unit circle (0007, part b): n whole angles; the n arcs between the
  // sorted vertices decide exactly as for the triangle. The continuous probability
  // 1 - n / 2^(n-1), and a random draw of n different angles.
  const polyArcs = (angles) => {
    const a = angles.map(triNorm).sort((u, v) => u - v), n = a.length;
    const arcs = [];
    for (let i = 0; i + 1 < n; i++) arcs.push(a[i + 1] - a[i]);
    arcs.push(TRI_M - (a[n - 1] - a[0]));
    return arcs;
  };
  const polyClass = (angles) => {
    const arcs = polyArcs(angles);
    if (arcs.includes(0) || arcs.includes(TRI_M)) return "degenerate";
    const top = Math.max(...arcs);
    return top < 180 ? "in" : top === 180 ? "edge" : "out";
  };
  const polyProb = (n) => 1 - n / Math.pow(2, n - 1);
  const polyRandom = (n, rnd = Math.random) => {
    const used = new Set(), out = [];
    while (out.length < n) { const v = Math.floor(rnd() * TRI_M); if (!used.has(v)) { used.add(v); out.push(v); } }
    return out;
  };

  // Edge detector (0001): sig per cycle, cycle 0 being the reset cycle (rst_n low, so
  // sig_q is 0 there); from cycle 1 sig_q is the previous cycle's sig. pulse follows the
  // page's AND for a rising edge, its mirror for a falling edge, XOR for both.
  const EDGE_MODES = {
    rise: (s, q) => (s && !q ? 1 : 0),
    fall: (s, q) => (!s && q ? 1 : 0),
    both: (s, q) => (s !== q ? 1 : 0),
  };
  const edgeTrace = (sig, mode = "rise") => {
    const fn = EDGE_MODES[mode] || EDGE_MODES.rise;
    const sigQ = sig.map((_, i) => (i === 0 ? 0 : sig[i - 1]));
    const pulse = sig.map((s, i) => fn(s, sigQ[i]));
    // the true edges of sig (between cycles i - 1 and i), independent of the circuit
    const edges = sig.map((s, i) => (i > 0 && fn(s, sig[i - 1]) ? 1 : 0));
    const pulses = [];
    pulse.forEach((p, i) => { if (p && !(i > 0 && pulse[i - 1])) pulses.push(i); });
    const widths = pulses.map((i) => { let w = 0; while (pulse[i + w]) w++; return w; });
    return { sigQ, pulse, edges, pulses, widths, phantom: pulse[0] === 1 };
  };

  // LFSR (0036): the page's step and period on the mask of the taps (bit i of the mask is
  // s[i]; x^k is s[width - k]); the walk from a seed until a state repeats; the eight
  // polynomials x^4 + ... + 1 with their periods.
  const lfsrNext = (state, mask, width) => {
    let fb = 0;
    for (let v = state & mask; v; v >>= 1) fb ^= v & 1;
    return (state >> 1) | (fb << (width - 1));
  };
  const lfsrWalk = (mask, width, seed = 1) => {
    const seen = new Map(), states = [];
    let s = seed;
    while (!seen.has(s)) { seen.set(s, states.length); states.push(s); s = lfsrNext(s, mask, width); }
    return { states, period: states.length - seen.get(s), back: seen.get(s) };
  };
  const lfsrPeriod = (mask, width, seed = 1) => lfsrWalk(mask, width, seed).period;
  const lfsrPoly = (mask, width) => {
    const terms = [`x^${width}`];
    for (let k = width - 1; k >= 1; k--) if ((mask >> (width - k)) & 1) terms.push(k === 1 ? "x" : `x^${k}`);
    return terms.concat("1").join(" + ");
  };
  const lfsrTable = (width) => {
    const rows = [];
    for (let m = 0; m < 1 << (width - 1); m++) {
      const mask = 1 | (m << 1);
      rows.push({ mask, poly: lfsrPoly(mask, width), period: lfsrPeriod(mask, width) });
    }
    return rows;
  };

  // Divide by three (0035): the page's half-cycle model, edge by edge, from any counter
  // state. `counter`: "wrap" is the module (cnt is 2 bits, so 3 + 1 wraps to 0), "wide"
  // is a counter with no wrap (the page's Python model: 3 + 1 = 4 and a never rises),
  // "guard" compares with >= 2. Returns the values after each edge.
  const div3Trace = (halfCycles, cnt0 = 0, counter = "wrap") => {
    let cnt = cnt0, a = 0, b = 0;
    const rows = [];
    for (let edge = 0; edge < halfCycles; edge++) {
      const rising = edge % 2 === 0;
      const pa = a, pb = b, pc = cnt;
      if (rising) {
        a = cnt === 2 ? 1 : 0;
        if (counter === "guard") cnt = cnt >= 2 ? 0 : cnt + 1;
        else if (counter === "wide") cnt = cnt === 2 ? 0 : cnt + 1;
        else cnt = cnt === 2 ? 0 : (cnt + 1) & 3;
      } else b = a;
      rows.push({ edge, rising, cnt, a, b, out: a | b, aChanged: a !== pa, bChanged: b !== pb, cntPrev: pc });
    }
    return rows;
  };
  // The period and the high count of the output from the first rise, and whether it
  // settled into 3 high / 3 low.
  const div3Duty = (rows) => {
    const out = rows.map((r) => r.out);
    const rises = [];
    out.forEach((v, i) => { if (v && !(i > 0 && out[i - 1])) rises.push(i); });
    if (rises.length < 2) return { rises, period: null, high: null };
    const period = rises[1] - rises[0];
    let high = 0;
    for (let i = rises[0]; i < rises[1]; i++) high += out[i];
    const ok = rises.every((r, k) => k === 0 || r - rises[k - 1] === period);
    return { rises, period, high, ok };
  };

  // Gray pointers (0034): the page's conversions, a sampled step b -> b + 1 where each
  // changing bit arrived or not, and the page's full / empty rules.
  const grayOf = (b) => b ^ (b >> 1);
  const grayToBin = (g, bits) => {
    let b = 0, acc = 0;
    for (let i = bits - 1; i >= 0; i--) { acc ^= (g >> i) & 1; b |= acc << i; }
    return b;
  };
  const bitsOf = (v, bits) => v.toString(2).padStart(bits, "0");
  // `arrived` maps a bit index to 1 (the new value was sampled) or 0 (the old one);
  // bits that do not change are the same either way.
  const graySample = (b, bits, arrivedBin, arrivedGray) => {
    const size = 1 << bits, nb = (b + 1) % size;
    const ob = b, og = grayOf(b), ng = grayOf(nb);
    const changedBin = [], changedGray = [];
    for (let i = 0; i < bits; i++) {
      if (((ob ^ nb) >> i) & 1) changedBin.push(i);
      if (((og ^ ng) >> i) & 1) changedGray.push(i);
    }
    const pick = (oldV, newV, changed, arrived) => {
      let v = oldV;
      changed.forEach((i) => { if (arrived[i]) v = (v & ~(1 << i)) | (newV & (1 << i)); });
      return v;
    };
    const seenBin = pick(ob, nb, changedBin, arrivedBin || {});
    const seenGray = pick(og, ng, changedGray, arrivedGray || {});
    return {
      oldB: ob, newB: nb, oldG: og, newG: ng, changedBin, changedGray, seenBin, seenGray,
      binValid: seenBin === ob || seenBin === nb,
      seenGrayAsBin: grayToBin(seenGray, bits),
      wrongCount: changedBin.length >= 1 ? (1 << changedBin.length) - 2 : 0,
    };
  };
  const grayFlags = (w, r, bits) => {
    const wg = grayOf(w), rg = grayOf(r);
    const top = 3 << (bits - 2), rest = (1 << (bits - 2)) - 1;
    const empty = wg === rg;
    const full = (wg & top) === (~rg & top) && (wg & rest) === (rg & rest);
    const occupancy = (w - r) & ((1 << bits) - 1);
    return { wg, rg, empty, full, occupancy };
  };

  const models = {
    cakeSplit, cakeThreshold, cakeFormula, cakeBest,
    motorcyclePlan, motorcycleTime, motorcyclePhases, motorcyclePositions, josephusRun, josephusSteps, josephusZero, josephusFormula,
    clockCounts, clockMeetsIn, clockNext, clockPrev, clockLabel,
    stripImages, stripEdgePoint, stripPoint3, stripFacesBetween, stripLines, stripBest,
    hourglassSolve, hourglassInterval, hourglassReplay, hourglassReachable, probabilityAnswer,
    bridgeSolve, bridgeEscort, riverSafe, riverMoves, riverPlan,
    pcieBoundaries, pcieBlocks, pcieSplits, pcieByCompletions, pcieCount, pcieS, pcieFormula,
    fifoSteps, fifoDepth, fifoFill, mtbfSeconds, mtbfHuman,
    TRI_TOTAL, triArcs, triClass, triCountC, triFrame, triIndex, triCounts, polyArcs, polyClass, polyProb, polyRandom,
    permCycles, permHelper, permSwap, permWalk, permAllWin, permShuffle, permRandomPicks, permStrategyProb, permRandomProb,
    floydRho, floydTrace, floydRandom, floydParse, bfs01Trace, bfs01Counts, bracketsClean, bracketsTrace,
    TTT_LINES, TTT_WRAP, tttCheck, tttFinalBoards, tttRandom,
    shapesOverlap, shapesCandidates, shapesOk, shapesTry, shapesRandom, shapesHeat,
    kapStep, kapChain, kapHistogram,
    EURO_RESULTS, EURO_PUBLIC_TOTAL, euroOrder, euroWithIsrael, euroCannotWin, euroScan,
    boxesCases, boxesDraw, boxesFix, boxesDeduce,
    EDGE_MODES, edgeTrace, lfsrNext, lfsrWalk, lfsrPeriod, lfsrPoly, lfsrTable, div3Trace, div3Duty,
    grayOf, grayToBin, bitsOf, graySample, grayFlags,
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

  // The bridge box (0031): type the crossing times, the Dijkstra of the page runs in the
  // browser, and the crossings play one at a time on the banks figure.
  const bridgeView = () => ({
    mount(box) {
      const NAMES = "ABCDEFGH";
      const defaults = box.dataset.times || "1 2 5 10";
      const st = { times: [], s: 0 };
      box.innerHTML =
        `<div class="ex-controls"><label>הזמנים (עד שמונה) <input type="text" class="ex-times" value="${defaults}" size="22" dir="ltr" inputmode="numeric" aria-label="זמני החצייה, מופרדים ברווחים"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button ex-prev">החצייה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">החצייה הבאה</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button><span class="ex-pos"></span></div>` +
        `<div class="bridge-frame"></div><p class="bridge-caption"></p>` +
        `<span class="viz-legend"><span><i class="st-cell"></i>על הגדה הקרובה</span><span><i class="st-stack"></i>חוצים עכשיו</span><span><i class="st-ok"></i>כבר על הגדה הרחוקה</span><span><i class="torch"></i>הלפיד</span></span>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), input = $(".ex-times");
      let timer = null;
      const parse = () => {
        const ts = input.value.split(/[\s,]+/).filter(Boolean).map(Number).filter((v) => Number.isFinite(v) && v > 0).slice(0, 8);
        return ts.map((v) => Math.round(v * 100) / 100);
      };
      const frameSvg = (times, across, side, moving, forward, t) => {
        const n = times.length, per = Math.max(34, Math.min(40, 170 / Math.max(n, 1)));
        let s = `<svg class="figure bridge-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="הגשר, שתי הגדות, הלפיד והאנשים בזמן ${t}">` +
          `<rect class="bank" x="0" y="20" width="190" height="150" rx="8"/><rect class="bank" x="450" y="20" width="190" height="150" rx="8"/>` +
          `<rect class="river" x="190" y="20" width="260" height="150"/><rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/>` +
          `<text class="legend" x="95" y="160" text-anchor="middle">near</text><text class="legend" x="545" y="160" text-anchor="middle">far</text>`;
        const person = (i, x, y, cls) => `<g><circle class="${cls}" cx="${f(x)}" cy="${y}" r="17"/><text class="st-text" x="${f(x)}" y="${y + 5}" text-anchor="middle">${times[i]}</text>` +
          `<text class="st-small" x="${f(x)}" y="${y + 30}" text-anchor="middle">${NAMES[i]}</text></g>`;
        const near = [], far = [];
        for (let i = 0; i < n; i++) { if (moving.includes(i)) continue; ((across >> i) & 1 ? far : near).push(i); }
        near.forEach((i, k) => { s += person(i, 40 + per * (k % 4), 60 + 60 * Math.floor(k / 4), "st-cell"); });
        far.forEach((i, k) => { s += person(i, 490 + per * (k % 4), 60 + 60 * Math.floor(k / 4), "st-ok"); });
        moving.forEach((i, k) => { s += person(i, 290 + 60 * k, 95, "st-stack"); });
        if (moving.length) {
          const [x0, x1] = forward ? [236, 404] : [404, 236], d = forward ? 9 : -9;
          s += `<line class="ink-line" x1="${x0}" y1="128" x2="${x1}" y2="128" stroke-width="2"/><polygon class="ink-fill" points="${x1},128 ${x1 - d},123 ${x1 - d},133"/>`;
        }
        const tx = moving.length ? 320 : side === 0 ? 150 : 490, ty = moving.length ? 150 : 118;
        s += `<polygon class="torch" points="${tx},${ty - 14} ${tx + 6},${ty - 2} ${tx},${ty + 2} ${tx - 6},${ty - 2}"/><rect class="ink-fill" x="${tx - 1.5}" y="${ty + 2}" width="3" height="10"/>` +
             `<text class="legend" x="630" y="182" text-anchor="end" font-weight="700">t = ${t}</text>`;
        return s + "</svg>";
      };
      const draw = () => {
        const times = st.times;
        if (!times.length) { $(".ex-summary").textContent = "הקלידו זמני חצייה חיוביים, מופרדים ברווחים."; $(".bridge-frame").innerHTML = ""; $(".bridge-caption").textContent = ""; $(".ex-pos").textContent = ""; return; }
        const r = bridgeSolve(times), esc = bridgeEscort(times);
        st.s = Math.min(Math.max(st.s, 0), r.moves.length);
        const names = (g) => g.map((i) => `${NAMES[i]} (${times[i]})`).join(" ו-");
        const planText = r.moves.map((g, k) => `${g.map((i) => NAMES[i]).join("+")}${k % 2 ? "<" : ">"}`).join(" ");
        $(".ex-summary").innerHTML = `${times.length === 1 ? "אדם אחד" : `${ltr(times.length)} אנשים`}: הזמן הקצר ביותר הוא ${ltr(r.time)} דקות ב-${ltr(r.moves.length)} חציות, ${ltr(planText)}. ` +
          (times.length >= 3 ? `אם המהיר היה מלווה את כולם: ${ltr(esc)}${esc > r.time ? `, כלומר ${ltr(esc - r.time)} דקות יותר.` : ", אותו דבר."}` : "");
        let across = 0, side = 0, t = 0, caption = "רגע 0: כולם והלפיד על הגדה הקרובה.";
        let moving = [], forward = true;
        for (let k = 0; k < st.s; k++) {
          const g = r.moves[k], cost = Math.max(...g.map((i) => times[i]));
          forward = side === 0; t += cost;
          if (k === st.s - 1) { moving = g; caption = `חצייה ${k + 1}: ${names(g)} ${g.length > 1 ? "חוצים" : (forward ? "חוצה" : "חוזר")} ${forward ? "קדימה" : "עם הלפיד חזרה"}, ${ltr(cost)} דקות. עברו ${ltr(t)} דקות.`; }
          else { across ^= g.reduce((m, i) => m | (1 << i), 0); side = 1 - side; }
        }
        $(".bridge-frame").innerHTML = frameSvg(times, across, side, moving, forward, t);
        $(".bridge-caption").innerHTML = caption + (st.s === r.moves.length && st.s > 0 ? " כולם בצד הרחוק." : "");
        $(".ex-pos").textContent = `חצייה ${st.s} מתוך ${r.moves.length}`;
        $(".ex-prev").disabled = st.s <= 0; $(".ex-next").disabled = st.s >= r.moves.length;
        if (window.dvqDecorate) window.dvqDecorate($(".bridge-frame"));
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => (st.times.length ? bridgeSolve(st.times).moves.length : 0);
      $(".ex-next").addEventListener("click", () => { stop(); st.s += 1; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s -= 1; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (!total()) return;
        if (st.s >= total()) st.s = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { if (st.s >= total()) { stop(); return; } st.s += 1; draw(); }, 1000);
        st.s += 1; draw();
      });
      input.addEventListener("change", () => { stop(); st.times = parse(); st.s = 0; draw(); });
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      $(".ex-reset").addEventListener("click", () => { stop(); input.value = defaults; st.times = parse(); st.s = 0; draw(); });
      st.times = parse();
      draw();
    },
  });

  // The river box (0032): cross by hand (pick who boards the boat; an unsafe crossing is
  // shown and taken back), or let the BFS plan play; the state graph marks where you are.
  const riverView = () => ({
    mount(box) {
      const LETTER = { farmer: "F", wolf: "W", goat: "G", cabbage: "C" };
      const HEB = { wolf: "הזאב", goat: "העז", cabbage: "הכרוב" };
      const st = { s: 0, history: [], unsafe: null, plan: null, k: 0 };
      box.innerHTML =
        `<div class="ex-controls"><span>האיכר חוצה:</span>` +
        `<button type="button" class="md-button ex-go" data-item="">לבד</button>` +
        ["wolf", "goat", "cabbage"].map((i) => `<button type="button" class="md-button ex-go" data-item="${i}">עם ${HEB[i]}</button>`).join("") +
        `<button type="button" class="md-button ex-undo">צעד אחורה</button>` +
        `<button type="button" class="md-button ex-reset">מההתחלה</button>` +
        `<button type="button" class="md-button md-button--primary ex-solve">פתרון</button></div>` +
        `<div class="river-frame"></div><p class="ex-summary" aria-live="polite"></p>` +
        `<p class="ex-title">גרף המצבים: המצב הנוכחי מודגש, והמסלול שעברתם בכתום</p><div class="river-graph"></div>`;
      const $ = (sel) => box.querySelector(sel);
      let timer = null;
      const bankText = (s, side) => ["farmer", "wolf", "goat", "cabbage"].filter((n) => !!(s & RIVER[n]) === !!side).map((n) => LETTER[n]).join("") || "–";
      const frameSvg = (s, carried, moving, forward, unsafe) => {
        let out = `<svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="הנהר, שתי הגדות והסירה">` +
          `<rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/>` +
          `<rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text>`;
        const who = (name, x, y, cls) => `<g><circle class="${cls}" cx="${x}" cy="${y}" r="18"/><text class="st-text" x="${x}" y="${y + 5}" text-anchor="middle">${LETTER[name]}</text></g>`;
        const onBoat = moving ? new Set(["farmer", ...(carried ? [carried] : [])]) : new Set();
        [[0, 45], [1, 485]].forEach(([side, x0]) => {
          let k = 0;
          ["farmer", "wolf", "goat", "cabbage"].forEach((name) => {
            if (onBoat.has(name) || !!(s & RIVER[name]) !== !!side) return;
            const cls = unsafe && unsafe.includes(name) ? "st-bad" : name === "farmer" ? "st-stack" : "st-cell";
            out += who(name, x0 + 40 * k, 70, cls);
            k += 1;
          });
        });
        const bx = moving ? 320 : (s & 1 ? 365 : 215);
        out += `<rect class="boat" x="${bx - 50}" y="100" width="100" height="26" rx="10"/>`;
        if (moving) {
          out += who("farmer", carried ? bx - 20 : bx, 93, "st-stack") + (carried ? who(carried, bx + 20, 93, "st-cell") : "");
          const [x0, x1] = forward ? [250, 390] : [390, 250], d = forward ? 9 : -9;
          out += `<line class="ink-line" x1="${x0}" y1="150" x2="${x1}" y2="150" stroke-width="2"/><polygon class="ink-fill" points="${x1},150 ${x1 - d},145 ${x1 - d},155"/>`;
        }
        return out + "</svg>";
      };
      const graphSvg = () => {
        const X = (s) => 48 + ((s >> 1) & 7) * 78, Y = (s) => (s & 1 ? 190 : 60);
        const path = new Set();
        st.history.forEach(([a], i) => { const b = i + 1 < st.history.length ? st.history[i + 1][0] : st.s; path.add(`${Math.min(a, b)}-${Math.max(a, b)}`); });
        let out = `<svg class="figure river-graph" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="גרף המצבים עם המצב הנוכחי">`;
        for (let s = 0; s < 16; s++) {
          if (!riverSafe(s) || s & 1) continue;
          riverMoves(s).forEach(([, t]) => {
            if (!riverSafe(t)) return;
            const on = path.has(`${Math.min(s, t)}-${Math.max(s, t)}`);
            out += `<line class="${on ? "box-path" : "ink-line"}" x1="${X(s)}" y1="${Y(s) + 20}" x2="${X(t)}" y2="${Y(t) - 20}" stroke-width="${on ? 3 : 1}"${on ? "" : ' stroke-opacity="0.4"'}/>`;
          });
        }
        for (let s = 0; s < 16; s++) {
          const ok = riverSafe(s);
          const cls = s === st.s ? "st-cur" : s === 0 || s === 15 ? "st-ok" : ok ? "st-cell" : "st-bad";
          out += `<rect class="${cls}" x="${X(s) - 32}" y="${Y(s) - 20}" width="64" height="40" rx="6"/>` +
                 `<text class="st-text st-sm" x="${X(s)}" y="${Y(s) - 4}" text-anchor="middle">${bankText(s, 0)}</text><text class="st-text st-sm" x="${X(s)}" y="${Y(s) + 14}" text-anchor="middle">${bankText(s, 1)}</text>`;
          if (!ok) out += `<line class="pg-strike" x1="${X(s) - 26}" y1="${Y(s) + 16}" x2="${X(s) + 26}" y2="${Y(s) - 16}"/>`;
        }
        out += `<text class="legend" x="8" y="16">farmer near: near bank / far bank</text><text class="legend" x="8" y="240">farmer far</text>`;
        return out + "</svg>";
      };
      const eaten = (s) => {
        const f = !!(s & 1), w = !!(s & 2), g = !!(s & 4), c = !!(s & 8);
        if (w === g && g !== f) return ["wolf", "goat"];
        if (g === c && g !== f) return ["goat", "cabbage"];
        return null;
      };
      const draw = (moving = null) => {
        const s = st.s;
        $(".river-frame").innerHTML = frameSvg(moving ? moving.from : s, moving ? moving.item : null, !!moving, moving ? !(moving.from & 1) : true, st.unsafe ? eaten(st.unsafe.state) : null);
        const n = st.history.length;
        let text;
        if (st.unsafe) {
          const [a, b] = eaten(st.unsafe.state);
          text = `אסור: ${HEB[a]} ו${HEB[b]} נשארים לבד, ו${a === "wolf" ? "הזאב אוכל את העז" : "העז אוכלת את הכרוב"}. החצייה בוטלה.`;
        } else if (s === 15) {
          text = `כולם בצד הרחוק אחרי ${ltr(n)} חציות${n === 7 ? ", המינימום." : n > 7 ? `, ‏${ltr(n - 7)} יותר מהמינימום.` : "."}`;
        } else {
          text = `${n === 0 ? "ההתחלה" : `אחרי ${ltr(n)} חציות`}: על הגדה הקרובה ${ltr(bankText(s, 0))}, על הרחוקה ${ltr(bankText(s, 1))}. האיכר ב${s & 1 ? "צד הרחוק" : "צד הקרוב"}.`;
        }
        $(".ex-summary").innerHTML = text;
        box.querySelectorAll(".ex-go").forEach((b) => {
          const item = b.dataset.item || null;
          b.disabled = s === 15 || !!timer || (item !== null && !!(s & RIVER[item]) !== !!(s & 1));
        });
        $(".ex-undo").disabled = n === 0 || !!timer;
        $(".river-graph").innerHTML = graphSvg();
        if (window.dvqDecorate) window.dvqDecorate($(".river-graph"));
      };
      const cross = (item) => {
        const nxt = st.s ^ 1 ^ (item ? RIVER[item] : 0);
        st.unsafe = null;
        if (!riverSafe(nxt)) { st.unsafe = { state: nxt }; draw(); return false; }
        st.history.push([st.s, item]);
        st.s = nxt;
        draw();
        return true;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; $(".ex-solve").textContent = "פתרון"; };
      box.querySelectorAll(".ex-go").forEach((b) => b.addEventListener("click", () => { stop(); cross(b.dataset.item || null); }));
      $(".ex-undo").addEventListener("click", () => { stop(); st.unsafe = null; if (st.history.length) { st.s = st.history.pop()[0]; } draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); st.s = 0; st.history = []; st.unsafe = null; draw(); });
      $(".ex-solve").addEventListener("click", () => {
        if (timer) { stop(); draw(); return; }
        st.s = 0; st.history = []; st.unsafe = null;
        const plan = riverPlan();
        let k = 0;
        $(".ex-solve").textContent = "עצירה";
        timer = setInterval(() => {
          if (k >= plan.length) { stop(); draw(); return; }
          const item = plan[k];
          draw({ from: st.s, item });                               // on the boat
          setTimeout(() => { if (timer) cross(item); }, 500);
          k += 1;
        }, 1100);
        draw();
      });
      draw();
    },
  });

  // The PCIe box (0020, 0021): address, length, MPS and RCB; the request on the RCB grid
  // cut into its blocks, the count by the dynamic program and by the closed form, the
  // count per number of completions, and the map of the splits (rows, as on the page) when
  // there are few enough to draw.
  const pcieView = () => ({
    mount(box) {
      const PRESETS = [["0x1010", 256, 256, 64, "0020: ‏0x1010, ‏256 B, ‏MPS 256"], ["0x1010", 256, 128, 64, "0020: אותה בקשה עם MPS 128"],
                       ["0x1000", 256, 256, 64, "0021 א: ‏0x1000, ‏256 B"], ["0x1000", 512, 256, 64, "0021 ב: ‏0x1000, ‏512 B"],
                       ["0x1010", 512, 256, 64, "0021 ב: ‏0x1010, ‏512 B"], ["0x1020", 128, 128, 64, "0021 ג: ‏0x1020, ‏128 B, ‏MPS 128 (δ = 1)"]];
      const defaults = { addr: box.dataset.addr || "0x1010", len: Number(box.dataset.len || 256), mps: Number(box.dataset.mps || 256), rcb: Number(box.dataset.rcb || 64) };
      const st = { ...defaults };
      const MAX_ROWS = 40;
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>דוגמאות מהדפים <select class="ex-preset"><option value="">בחרו...</option>${PRESETS.map((p, i) => `<option value="${i}">${p[4]}</option>`).join("")}</select></label>` +
        `<label>הכתובת ${ltr("A")} <input type="text" class="ex-addr" value="${st.addr}" size="8" dir="ltr" inputmode="text" aria-label="כתובת הבקשה, בהקסדצימלי" spellcheck="false"></label>` +
        `<label><span>האורך ${ltr("L")} (בתים)</span><input type="range" class="ex-len" min="4" max="2048" step="4" value="${st.len}" dir="ltr"><output class="out-len" dir="ltr"></output></label>` +
        `<label>MPS <select class="ex-mps">${[128, 256, 512, 1024, 2048, 4096].map((v) => `<option value="${v}"${v === st.mps ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<label>RCB <select class="ex-rcb">${[64, 128].map((v) => `<option value="${v}"${v === st.rcb ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p><div class="pcie-blocks"></div><div class="pcie-counts"></div><div class="pcie-map"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const hex = (v) => "0x" + v.toString(16).toUpperCase();
      const big = (v) => v.toLocaleString("en-US");
      const parseAddr = () => {
        const t = $(".ex-addr").value.trim().toLowerCase().replace(/^0x/, "");
        const v = /^[0-9a-f]{1,8}$/.test(t) ? parseInt(t, 16) : NaN;
        return Number.isNaN(v) ? null : v;
      };
      // An address axis like the page figures: base .. base + span mapped to x0 .. x1
      const axis = (addr, len, rcb, x0, x1) => {
        const base = Math.floor(addr / rcb) * rcb;
        const endBlock = Math.ceil((addr + len) / rcb) * rcb;
        const span = endBlock + rcb - base;
        const sc = (x1 - x0) / span;
        const x = (a) => x0 + (a - base) * sc;
        const grid = (y0, y1, labelsY = 16) => {
          let g = "";
          const every = span <= 6 * rcb ? 1 : span <= 12 * rcb ? 2 : span <= 24 * rcb ? 4 : 8;
          for (let off = 0, i = 0; off <= span; off += rcb, i++) {
            g += `<line class="cs-rcb" x1="${f(x(base + off))}" y1="${y0}" x2="${f(x(base + off))}" y2="${y1}"/>`;
            if (i % every === 0) g += `<text class="coord halo" x="${f(x(base + off))}" y="${labelsY}" text-anchor="middle">${hex(base + off)}</text>`;
          }
          [addr, addr + len].forEach((a) => { g += `<line class="cs-req" x1="${f(x(a))}" y1="${y0}" x2="${f(x(a))}" y2="${y1}"/>`; });
          return g;
        };
        return { x, grid, span };
      };
      const segment = (ax, cls, start, size, y, h, title) => {
        const a = ax.x(start), b = ax.x(start + size);
        let g = `<rect class="${cls}" x="${f(a)}" y="${y}" width="${f(b - a)}" height="${h}" rx="3"><title>${title}</title></rect>`;
        if (b - a >= 22) g += `<text class="cs-size" x="${f((a + b) / 2)}" y="${f(y + h / 2 + 4.5)}" text-anchor="middle">${size}</text>`;
        else if (b - a >= 14) g += `<text class="cs-size" x="${f((a + b) / 2)}" y="${f(y + h / 2 + 3.5)}" text-anchor="middle" style="font-size:9px">${size}</text>`;
        // narrower bars keep only their tooltip: a label above would collide with the row before
        return g;
      };
      const blocksSvg = (addr, len, mps, rcb) => {
        const ax = axis(addr, len, rcb, 40, 600);
        const sizes = pcieBlocks(addr, len, rcb), N = sizes.length, m = mps / rcb;
        const d = N === m + 1 && len <= mps ? 1 : 0;
        let g = `<svg class="figure cs-fig pcie-live" viewBox="0 0 640 132" style="max-width:40rem" role="img" aria-label="הבקשה על רשת ה-RCB, חתוכה ל-${N} בלוקים">${ax.grid(26, 96)}`;
        let pos = addr;
        sizes.forEach((sz, i) => {
          const cls = i === 0 ? "cs-first" : i === N - 1 ? "cs-last" : "cs-mid";
          g += segment(ax, cls, pos, sz, 50, 28, `block ${i + 1}: ${hex(pos)}–${hex(pos + sz - 1)}, ${sz} bytes`);
          pos += sz;
        });
        pcieBoundaries(addr, len, rcb).forEach((b) => { g += `<circle class="cs-can" cx="${f(ax.x(b))}" cy="50" r="4"><title>boundary ${hex(b)}</title></circle>`; });
        g += `<text class="legend" x="40" y="118">N = ${N}, |B| = ${N - 1}, f = ${sizes[0]}, e = ${sizes[N - 1]}, m = MPS / RCB = ${m}, δ = ${d}${d ? " (N = m + 1 and L ≤ MPS)" : ""}</text>`;
        return g + "</svg>";
      };
      const mapSvg = (addr, len, mps, rcb, rows, total) => {
        const labelW = Math.max(...rows.map((sp) => sp.join("+").length)) * 8.2 + 16;   // room for "48+64+64+64+16"
        const x0 = Math.min(330, Math.max(128, Math.round(labelW)));
        const ax = axis(addr, len, rcb, x0, 612);
        const row = 22, gap = 6, head = 24;
        const groups = new Map();
        rows.forEach((sp) => { if (!groups.has(sp.length)) groups.set(sp.length, []); groups.get(sp.length).push(sp); });
        let height = 30 + 4;
        groups.forEach((g) => { height += head + g.length * (row + gap); });
        let g = `<svg class="figure cs-fig pcie-live" viewBox="0 0 640 ${height}" style="max-width:40rem" role="img" aria-label="${rows.length} מתוך ${total} הפיצולים, שורה לכל פיצול">${ax.grid(24, height - 4)}`;
        let y = 30;
        groups.forEach((list, n) => {
          g += `<text class="legend halo" x="${x0 + 8}" y="${y + 15}" font-weight="700">${n} ${n === 1 ? "completion" : "completions"}: ${list.length}${rows.length < total ? "+" : ""} ${list.length === 1 && rows.length === total ? "split" : "splits"}</text>`;
          y += head;
          list.forEach((sp) => {
            g += `<text class="coord halo" x="${x0 - 10}" y="${y + 15}" text-anchor="end">${sp.join("+")}</text>`;
            let pos = addr;
            sp.forEach((size, i) => {
              const r = sp.length === 1 ? "one" : i === 0 ? "first" : i === sp.length - 1 ? "last" : "mid";
              g += segment(ax, `cs-${r}`, pos, size, y, row, `${hex(pos)}–${hex(pos + size - 1)}: ${size} bytes (${r})`);
              pos += size;
            });
            y += row + gap;
          });
        });
        return g + "</svg>";
      };
      const draw = () => {
        const addr = parseAddr();
        $(".out-len").textContent = String(st.len);
        if (addr === null) { $(".ex-summary").innerHTML = "הכתובת צריכה להיות מספר הקסדצימלי, למשל ‏<bdi dir=\"ltr\">0x1010</bdi>."; return; }
        const { len, mps, rcb } = st;
        if (mps < rcb) { $(".ex-summary").textContent = "בשאלה MPS ≥ RCB."; return; }
        const sizes = pcieBlocks(addr, len, rcb), N = sizes.length, m = mps / rcb;
        const byK = pcieByCompletions(addr, len, mps, rcb), total = byK.reduce((a, b) => a + b, 0n);
        const formula = pcieFormula(addr, len, mps, rcb);
        const crosses = (addr % 4096) + len > 4096;
        const first = pcieSplits(addr, len, mps, rcb, 1)[0];
        const blocksText = N === 1 ? `בלוק אחד של ${sizes[0]}` : `${sizes[0]}` + (N > 2 ? ` + ${N - 2} × ${rcb}` : "") + ` + ${sizes[N - 1]}`;
        $(".ex-summary").innerHTML =
          `בקשה של ${ltr(`${len} B`)} מכתובת ${ltr(hex(addr))} על רשת ${ltr(`RCB = ${rcb}`)}: ‏${ltr(`N = ${N}`)} בלוקים (${ltr(blocksText)}), ‏${ltr(`m = ${m}`)}. ` +
          `מספר הפיצולים החוקיים עם ${ltr(`MPS = ${mps}`)}: <b>${ltr(big(total))}</b>` +
          (total === formula ? ` (הנוסחה הסגורה נותנת אותו מספר).` : ` (הנוסחה הסגורה נותנת ${ltr(big(formula))}!).`) +
          (first ? ` הפיצול החמדני, עם הכי פחות Completions: ${ltr(first.join("+"))}.` : " אין פיצול חוקי.") +
          (crosses ? ` <b>הבקשה חוצה גבול 4 KB</b>, וזה אסור ב-PCIe; המספר מחושב כאילו מותר.` : "");
        $(".pcie-blocks").innerHTML = `<p class="ex-title">הבלוקים: הבקשה על רשת ה-RCB, הגבולות הפנימיים בירוק</p>${blocksSvg(addr, len, mps, rcb)}`;
        const counts = byK.map((w, k) => (k && w ? `<tr><td>${k}</td><td>${big(w)}</td></tr>` : "")).join("");
        $(".pcie-counts").innerHTML = total > 1n ? `<p class="ex-title">כמה פיצולים יש לכל מספר Completions</p><table class="pcie-table" dir="ltr"><thead><tr><th>Completions</th><th>פיצולים</th></tr></thead><tbody>${counts}</tbody></table>` : "";
        if (total === 0n) { $(".pcie-map").innerHTML = ""; }
        else {
          const rows = pcieSplits(addr, len, mps, rcb, MAX_ROWS);
          const note = BigInt(rows.length) < total ? `רק ${rows.length} הראשונים מתוך ${big(total)} מצוירים, בסדר של הפונקציה (החיתוך הרחוק קודם)` : `כל ${rows.length === 1 ? "הפיצול היחיד" : `${rows.length} הפיצולים`}, מקובצים לפי מספר ה-Completions`;
          $(".pcie-map").innerHTML = `<p class="ex-title">${note}</p>${mapSvg(addr, len, mps, rcb, rows, Number(total))}` +
            `<span class="viz-legend"><span><i class="cs-first"></i>ה-Completion הראשון (או היחיד)</span><span><i class="cs-mid"></i>אמצעי</span><span><i class="cs-last"></i>אחרון</span><span><i class="cs-rcb"></i>גבול RCB</span><span><i class="cs-req"></i>קצות הבקשה</span></span>`;
        }
        if (window.dvqDecorate) window.dvqDecorate(box);
      };
      $(".ex-addr").addEventListener("input", draw);
      $(".ex-len").addEventListener("input", () => { st.len = Number($(".ex-len").value); draw(); });
      $(".ex-mps").addEventListener("change", () => { st.mps = Number($(".ex-mps").value); draw(); });
      $(".ex-rcb").addEventListener("change", () => { st.rcb = Number($(".ex-rcb").value); draw(); });
      $(".ex-preset").addEventListener("change", () => {
        const p = PRESETS[Number($(".ex-preset").value)];
        if (!p) return;
        [$(".ex-addr").value, st.len, st.mps, st.rcb] = p;
        $(".ex-len").value = st.len; $(".ex-mps").value = st.mps; $(".ex-rcb").value = st.rcb;
        draw();
      });
      $(".ex-reset").addEventListener("click", () => {
        Object.assign(st, defaults);
        $(".ex-addr").value = st.addr; $(".ex-len").value = st.len; $(".ex-mps").value = st.mps; $(".ex-rcb").value = st.rcb; $(".ex-preset").value = "";
        draw();
      });
      draw();
    },
  });

  // The FIFO box (0033): burst, write and read rates and the reader's idle slot; the fill
  // level over time from the cycle simulation, the formula beside it.
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
        `<p class="ex-summary" aria-live="polite"></p><div class="fifo-chart"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const chart = (trace, tEnd, formula, yMax) => {
        const w = 640, h = 240, x0 = 44, right = 16, top = 16, base = 204;
        const X = (t) => x0 + (t / tEnd) * (w - x0 - right), Y = (v) => base - (v / yMax) * (base - top);
        let s = `<svg class="perf-chart fifo-live" viewBox="0 0 ${w} ${h}" role="img" aria-label="רמת המילוי של ה-FIFO לאורך הזמן">`;
        const yStep = yMax <= 10 ? 2 : yMax <= 50 ? 10 : yMax <= 100 ? 20 : yMax <= 300 ? 50 : 100;
        for (let v = 0; v <= yMax; v += yStep) s += `<line class="grid" x1="${x0}" x2="${w - right}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${x0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        const ns = tEnd * 0.05, xStep = ns <= 500 ? 100 : ns <= 2000 ? 250 : ns <= 5000 ? 500 : ns <= 20000 ? 2000 : 5000;
        for (let v = 0; v <= ns; v += xStep) s += `<line class="grid" x1="${f(X(v / 0.05))}" x2="${f(X(v / 0.05))}" y1="${top - 6}" y2="${base}" stroke-dasharray="4 4"/><text class="tick" x="${f(X(v / 0.05))}" y="${base + 18}" text-anchor="middle">${v ? `${v} ns` : "0"}</text>`;
        const pts = [];
        trace.forEach(([t, v], i) => { if (i) pts.push(`${f(X(t))},${f(Y(trace[i - 1][1]))}`); pts.push(`${f(X(t))},${f(Y(v))}`); });
        s += `<polyline class="s1-line" points="${pts.join(" ")}" fill="none" stroke-width="2"/>`;
        s += `<line class="ink-line" x1="${x0}" x2="${w - right}" y1="${f(Y(formula))}" y2="${f(Y(formula))}" stroke-width="1" stroke-dasharray="6 4"/>`;
        s += `<text class="legend" x="${w - right - 4}" y="${f(Y(formula) - 5)}" text-anchor="end">${formula}</text>`;
        return s + `<line class="axis" x1="${x0}" x2="${w - right}" y1="${base}" y2="${base}"/></svg>`;
      };
      const draw = () => {
        ["burst", "fw", "fr"].forEach((k) => { $(`.out-${k}`).textContent = String(st[k]); });
        const duty = st.idle ? 1 - 1 / st.idle : 1;
        const formula = fifoDepth(st.burst, st.fw, st.fr, duty);
        const r = fifoFill(st.burst, fifoSteps(st.fw), fifoSteps(st.fr), st.idle);
        const eff = st.fr * duty;
        const burstNs = (st.burst * 1000) / st.fw;
        $(".ex-summary").innerHTML =
          `פרץ של ${ltr(`B = ${st.burst}`)} מילים ב-${ltr(`${st.fw} MHz`)} נמשך ${ltr(`${fmt(burstNs, 0)} ns`)}; הקורא מוציא באותו זמן ` +
          `${ltr(`${fmt(burstNs * eff / 1000, 1)}`)} מילים (קצב אפקטיבי ${ltr(`${fmt(eff, 1)} MHz`)}). ` +
          `הנוסחה: <b>${ltr(String(formula))}</b>; המילוי המקסימלי בסימולציה: <b>${ltr(String(r.max))}</b>` +
          (r.max > formula ? ` (הפאזה בין השעונים מוסיפה ${r.max - formula}).` : ".") +
          (eff >= st.fw ? " הקורא לא איטי מהכותב, ולכן ה-FIFO כמעט לא מתמלא." : "");
        const tEnd = r.trace[r.trace.length - 1][0] || 1;
        const yMax = Math.max(5, Math.ceil(Math.max(r.max, formula) * 1.15 / 5) * 5);
        $(".fifo-chart").innerHTML = `<p class="ex-title">רמת המילוי לאורך הזמן; הקו המקווקו הוא הנוסחה</p>${chart(r.trace, tEnd, formula, yMax)}`;
        if (window.dvqDecorate) window.dvqDecorate(box);
      };
      ["burst", "fw", "fr"].forEach((k) => $(`.ex-${k}`).addEventListener("input", () => { st[k] = Number($(`.ex-${k}`).value); draw(); }));
      $(".ex-idle").addEventListener("change", () => { st.idle = Number($(".ex-idle").value); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, defaults); ["burst", "fw", "fr", "idle"].forEach((k) => { $(`.ex-${k}`).value = st[k]; }); draw(); });
      draw();
    },
  });

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
        $(".ex-summary").innerHTML = `מחזור של ${ltr(`${fmt(T, 2)} ns`)}; כניסות ל-metastability בשנייה: ${ltr(`T0 · f_clk · f_data = ${(st.t0 * 1e-12 * st.fclk * 1e6 * st.fdata * 1e6).toExponential(2).replace("e+", "·10^")}`)}; כל פלופ נוסף מכפיל את ה-MTBF ב-${ltr(`e^(T/τ) = ${Math.exp(T / (st.tau / 1000)).toExponential(2).replace("e+", "·10^")}`)}.`;
        $(".mtbf-table").innerHTML = `<table class="pcie-table" dir="ltr"><thead><tr><th>פלופים</th><th>t_res</th><th>e^(t_res/τ)</th><th>MTBF</th></tr></thead><tbody>${rows}</tbody></table>`;
        $(".mtbf-chart").innerHTML = `<p class="ex-title">MTBF כפונקציה של תדר השעון, לפלופ אחד (כתום), שניים (כחול) ושלושה (ירוק); הנקודות הן התדר הנבחר</p>${chart()}`;
        if (window.dvqDecorate) window.dvqDecorate(box);
      };
      SL.forEach(([k]) => $(`.ex-${k}`).addEventListener("input", () => { st[k] = Number($(`.ex-${k}`).value); draw(); }));
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, defaults); SL.forEach(([k]) => { $(`.ex-${k}`).value = st[k]; }); draw(); });
      draw();
    },
  });

  // The triangle box (0007): three points on the unit circle, dragged or typed in whole
  // degrees; the triangle is green with the centre inside, amber with the centre on an edge
  // (or no triangle), red without it; the arcs carry their size and the longest one stands
  // out. Play walks through every set of three different angles in increasing order and
  // counts the three kinds; the slider jumps to any frame, and a hand-made triangle shows
  // where it sits in that order.
  const triangleView = () => ({
    mount(box) {
      const C = 160, R = 104, R_ARC = 116, R_LBL = 137, NAMES = ["P1", "P2", "P3"];
      const KIND = {
        in: "המשולש מכיל את המרכז",
        edge: "המרכז על צלע",
        out: "המשולש לא מכיל את המרכז",
        degenerate: "אין משולש",
      };
      const num = (v) => Number(v).toLocaleString("en-US");
      const rad = (d) => (d * Math.PI) / 180;
      const at = (d, r) => [C + r * Math.cos(rad(d)), C - r * Math.sin(rad(d))];
      box.innerHTML =
        `<div class="tri-box"><svg class="figure tri-live" viewBox="0 0 320 320" role="img" aria-label="שלוש נקודות על מעגל היחידה">` +
        `<circle class="axis-c" cx="${C}" cy="${C}" r="${R}" fill="none"/>` +
        `<g class="tri-arcs"></g><polygon class="tri-shape"/>` +
        `<circle class="center-dot" cx="${C}" cy="${C}" r="4"/><text class="tick" x="${C + 7}" y="${C + 15}">O</text>` +
        NAMES.map((n, i) => `<circle class="tri-pt" data-i="${i}" r="9"><title>${n}</title></circle>` +
          `<text class="legend tri-name" data-i="${i}" text-anchor="middle">${n}</text>`).join("") +
        `</svg><div class="tri-panel">` +
        `<p class="tri-angles">` + NAMES.map((n, i) =>
          `<label>${ltr(n)} <input type="number" class="ex-deg" data-i="${i}" min="0" max="359" step="1" dir="ltr" aria-label="הזווית של ${n} במעלות">°</label>`).join(" ") + `</p>` +
        `<div class="ex-controls"><button type="button" class="md-button ex-random">הגרלה</button></div>` +
        `<p class="tri-status" aria-live="polite"></p><p class="tri-arcs-text"></p></div></div>` +
        `<div class="ex-controls tri-run">` +
        `<button type="button" class="md-button md-button--primary ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed">` +
        [[2, "2 משולשים בשנייה"], [30, "30 בשנייה"], [1000, "1,000 בשנייה"], [100000, "100,000 בשנייה"], [1000000, "מיליון בשנייה"]]
          .map(([v, n]) => `<option value="${v}"${v === 30 ? " selected" : ""}>${n}</option>`).join("") +
        `</select></label>` +
        `<button type="button" class="md-button ex-prev" aria-label="המשולש הקודם בספירה">‹ הקודם</button>` +
        `<button type="button" class="md-button ex-next" aria-label="המשולש הבא בספירה">הבא ›</button>` +
        `<button type="button" class="md-button ex-first">להתחלה</button>` +
        `<button type="button" class="md-button ex-last">לסוף</button></div>` +
        `<label class="tri-frames">הספירה <input type="range" class="ex-frame" min="0" max="${TRI_TOTAL - 1}" step="1" dir="ltr" aria-label="מספר המשולש בספירה"></label>` +
        `<p class="tri-frame-text"></p><ul class="tri-counts"></ul>` +
        `<p class="ex-summary tri-compare"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const svg = $("svg"), shape = $(".tri-shape"), arcsG = $(".tri-arcs");
      const pts = [...box.querySelectorAll(".tri-pt")], names = [...box.querySelectorAll(".tri-name")];
      const inputs = [...box.querySelectorAll(".ex-deg")];
      const play = $(".ex-play"), speed = $(".ex-speed"), slider = $(".ex-frame");
      let angles = (box.dataset.angles || "20,140,250").split(",").map(Number).map((v) => ((v % 360) + 360) % 360);
      let frame = 0, running = false, last = 0, pos = 0;

      const arcPath = (from, len) => {
        const [x0, y0] = at(from, R_ARC), [x1, y1] = at(from + len, R_ARC);
        return `M${f(x0)},${f(y0)} A${R_ARC},${R_ARC} 0 ${len > 180 ? 1 : 0} 0 ${f(x1)},${f(y1)}`;
      };
      const render = () => {
        const kind = triClass(angles);
        const order = [0, 1, 2].sort((i, j) => angles[i] - angles[j] || i - j);
        const arcs = triArcs(angles), top = Math.max(...arcs);
        svg.setAttribute("class", `figure tri-live is-${kind}`);
        shape.setAttribute("points", angles.map((d) => at(d, R).map((v) => f(v)).join(",")).join(" "));
        let g = "";
        arcs.forEach((len, n) => {
          if (len <= 0 || len >= 360) return;
          const from = angles[order[n]];
          const [lx, ly] = at(from + len / 2, R_LBL);
          const max = len === top;
          g += `<path class="tri-arc${max ? " is-max" : ""}" d="${arcPath(from, len)}" fill="none"/>` +
               `<text class="legend${max ? " tri-max-label" : ""}" x="${f(lx)}" y="${f(ly + 5)}" text-anchor="middle">${len}°</text>`;
        });
        arcsG.innerHTML = g;
        angles.forEach((d, i) => {
          const [x, y] = at(d, R), [nx, ny] = at(d, R - 24);
          pts[i].setAttribute("cx", f(x)); pts[i].setAttribute("cy", f(y));
          names[i].setAttribute("x", f(nx)); names[i].setAttribute("y", f(ny + 5));
          if (document.activeElement !== inputs[i] || running) inputs[i].value = d;
        });
        svg.setAttribute("aria-label", `שלוש נקודות על מעגל היחידה בזוויות ${angles.join(", ")} מעלות: ${KIND[kind]}`);
        const sorted = order.map((i) => angles[i]);
        const why = {
          in: `כל שלוש הקשתות קטנות מ-180°, הגדולה היא ${ltr(top + "°")}.`,
          edge: `יש קשת של בדיוק 180°, והצלע שמולה היא קוטר שעובר דרך המרכז.`,
          out: `יש קשת של ${ltr(top + "°")}, יותר מ-180°: שלוש הנקודות בחצי מעגל אחד.`,
          degenerate: `שתי נקודות או יותר באותה זווית.`,
        }[kind];
        const mark = { in: "✓", edge: "●", out: "✗", degenerate: "●" }[kind];
        $(".tri-status").innerHTML = `<span class="tri-kind is-${kind}">${mark} ${KIND[kind]}.</span> ${why}`;
        $(".tri-arcs-text").innerHTML = kind === "degenerate" ? "" :
          `הקשתות: ${ltr(`${sorted[1]} − ${sorted[0]} = ${arcs[0]}°`)}, ${ltr(`${sorted[2]} − ${sorted[1]} = ${arcs[1]}°`)}, ` +
          `${ltr(`360 − (${sorted[2]} − ${sorted[0]}) = ${arcs[2]}°`)}.`;
        // the place of this triangle in the enumeration, and the counts up to it
        const distinct = kind !== "degenerate";
        if (distinct) frame = triIndex(angles);
        slider.value = frame;
        const c = triCounts(frame);
        $(".tri-frame-text").innerHTML = distinct
          ? `משולש ${ltr(num(frame + 1))} מתוך ${ltr(num(TRI_TOTAL))} בספירה: כל שלוש זוויות שונות מ-0° עד 359°, בסדר עולה.`
          : `לשתי נקודות באותה זווית אין מקום בספירה; המונים נשארו במשולש ${ltr(num(frame + 1))}.`;
        const pct = (v) => ltr(`${f((100 * v) / c.seen, 2)}%`);
        $(".tri-counts").innerHTML =
          `<li class="is-in">מכילים את המרכז: ${ltr(num(c.in))} (${pct(c.in)})</li>` +
          `<li class="is-edge">המרכז על צלע: ${ltr(num(c.edge))} (${pct(c.edge)})</li>` +
          `<li class="is-out">לא מכילים: ${ltr(num(c.out))} (${pct(c.out)})</li>`;
        const p = c.in / c.seen, exact = 89 / 359;
        const diff = p - exact;
        $(".tri-compare").innerHTML =
          `החלק שמכיל עד כאן: ${ltr(fmt(p, 5))}. בסוף הספירה: ${ltr("1,911,720 / 7,711,320 = 89/359 ≈ 0.24791")} (סעיף ד), ` +
          `ובזוויות רציפות ${ltr("1/4")} (סעיף ג). ההפרש מ-${ltr("89/359")}: ${ltr((diff >= 0 ? "+" : "−") + fmt(Math.abs(diff), 5))}` +
          (c.seen === TRI_TOTAL ? ", והספירה הושלמה." : ". הסדר עולה, ולכן החלק נודד בדרך ומגיע לערך המדויק רק בסוף.");
      };
      const setAngles = (next) => { angles = next.map((v) => ((Math.round(v) % 360) + 360) % 360); render(); };
      const setFrame = (k) => {
        frame = Math.min(Math.max(Math.floor(k), 0), TRI_TOTAL - 1);
        angles = triFrame(frame);
        render();
      };
      const stop = () => {
        running = false;
        play.textContent = "הפעלה";
        $(".tri-status").setAttribute("aria-live", "polite");
      };
      const tick = (now) => {
        if (!running) return;
        pos = Math.min(pos + ((now - last) / 1000) * Number(speed.value), TRI_TOTAL - 1);
        last = now;
        if (Math.floor(pos) !== frame) setFrame(pos);
        if (frame >= TRI_TOTAL - 1) stop(); else requestAnimationFrame(tick);
      };
      play.addEventListener("click", () => {
        if (running) { stop(); return; }
        if (triClass(angles) === "degenerate" || frame >= TRI_TOTAL - 1) setFrame(frame >= TRI_TOTAL - 1 ? 0 : frame);
        pos = frame;
        running = true;
        play.textContent = "עצירה";
        $(".tri-status").setAttribute("aria-live", "off");
        last = performance.now();
        requestAnimationFrame(tick);
      });
      $(".ex-prev").addEventListener("click", () => { stop(); setFrame(frame - 1); });
      $(".ex-next").addEventListener("click", () => { stop(); setFrame(frame + 1); });
      $(".ex-first").addEventListener("click", () => { stop(); setFrame(0); });
      $(".ex-last").addEventListener("click", () => { stop(); setFrame(TRI_TOTAL - 1); });
      slider.addEventListener("input", () => { stop(); setFrame(Number(slider.value)); });
      $(".ex-random").addEventListener("click", () => {
        stop();
        setAngles([0, 1, 2].map(() => Math.floor(Math.random() * 360)));
      });
      inputs.forEach((inp, i) => {
        inp.addEventListener("change", () => {
          const v = Number(inp.value);
          if (inp.value.trim() !== "" && Number.isFinite(v)) {
            stop();
            const next = [...angles]; next[i] = v; setAngles(next);
          } else render();                              // a bad entry falls back to the angle shown
        });
        inp.addEventListener("keydown", (e) => { if (e.key === "Enter") inp.blur(); });
      });

      // drag: the point nearest to the finger follows it around the circle, in whole degrees
      let drag = null;
      const degAt = (e) => {
        const r = svg.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width) * 320 - C, y = C - ((e.clientY - r.top) / r.height) * 320;
        return ((Math.round((Math.atan2(y, x) * 180) / Math.PI) % 360) + 360) % 360;
      };
      svg.addEventListener("pointerdown", (e) => {
        stop();
        const d = degAt(e);
        const dist = (i) => { const u = Math.abs(angles[i] - d); return Math.min(u, 360 - u); };
        const target = e.target.closest(".tri-pt");
        drag = target ? Number(target.dataset.i) : [0, 1, 2].reduce((b, i) => (dist(i) < dist(b) ? i : b), 0);
        svg.setPointerCapture(e.pointerId);
        svg.classList.add("is-dragging");
        const next = [...angles]; next[drag] = d; setAngles(next);
        e.preventDefault();
      });
      svg.addEventListener("pointermove", (e) => {
        if (drag === null) return;
        const d = degAt(e);
        if (d === angles[drag]) return;
        const next = [...angles]; next[drag] = d; setAngles(next);
      });
      const end = () => { drag = null; svg.classList.remove("is-dragging"); };
      svg.addEventListener("pointerup", end);
      svg.addEventListener("pointercancel", end);
      render();
    },
  });

  // The boxes box (0009): N boxes on a ring with an arrow from every box to the box its
  // note names, one colour per cycle and the long cycle in red; person 0's cut as two
  // dashed arrows; a person's walk played opening by opening; and a counter of rounds
  // that compares the strategy without person 0 with random picks.
  const boxesView = () => ({
    mount(box) {
      const EXAMPLE = [0, 7, 11, 15, 16, 13, 2, 12, 14, 4, 5, 6, 3, 1, 8, 9, 10];
      const nmax = Number(box.dataset.nmax || 16);
      const W = 360, C = 180, R = 138, NODE = 15, CYC = 5;    // CYC colours for the cycles
      const num = (v) => Number(v).toLocaleString("en-US");
      const st = { n: nmax, notes: EXAMPLE, helper: true, me: 13, step: 0, runs: 0, strat: 0, rand: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>מספר הקופסאות N</span><input type="range" class="ex-n" min="4" max="${nmax}" step="2" value="${st.n}" dir="ltr"><output class="out-n"></output></label>` +
        `<button type="button" class="md-button md-button--primary ex-shuffle">ערבוב</button>` +
        `<button type="button" class="md-button ex-example">הדוגמה מהדף</button>` +
        `<label><input type="checkbox" class="ex-helper" checked> אדם 0 חותך את המעגל הארוך</label></div>` +
        `<div class="bx-box"><div class="bx-ring"></div><div class="bx-panel">` +
        `<p class="bx-cycles"></p><p class="bx-helper"></p>` +
        `<div class="ex-controls bx-walk-row"><label>אדם <input type="number" class="ex-me" min="1" max="${nmax}" step="1" dir="ltr" aria-label="מספר האדם שהולך"></label>` +
        `<button type="button" class="md-button ex-prev">הפתיחה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הפתיחה הבאה</button>` +
        `<button type="button" class="md-button ex-all">עד הסוף</button>` +
        `<button type="button" class="md-button ex-start">מההתחלה</button></div>` +
        `<p class="bx-walk" aria-live="polite"></p></div></div>` +
        `<div class="ex-controls bx-stats-row">` +
        `<button type="button" class="md-button ex-rounds">1,000 סיבובים בלי אדם 0</button>` +
        `<button type="button" class="md-button ex-rounds-reset">איפוס המונים</button><span class="bx-runs"></span></div>` +
        `<div class="bx-bars"></div><p class="ex-summary bx-formula"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const ring = $(".bx-ring"), meIn = $(".ex-me"), helperCb = $(".ex-helper");
      const pt = (b, r) => { const a = -Math.PI / 2 + (2 * Math.PI * (b - 1)) / st.n; return [C + r * Math.cos(a), C + r * Math.sin(a)]; };
      const maxOpens = () => st.n / 2;
      const effective = () => {
        if (!st.helper) return { notes: st.notes, cut: null };
        const cut = permHelper(st.notes, maxOpens());
        return { notes: cut ? permSwap(st.notes, cut[0], cut[1]) : st.notes, cut };
      };
      // an arrow from box a to box b: a chord bent to its right, so a -> b and b -> a differ
      const arrow = (a, b, cls, dashed) => {
        const [x0, y0] = pt(a, R), [x1, y1] = pt(b, R);
        if (a === b) {
          const [ox, oy] = pt(a, R + 26);
          return `<circle class="bx-arrow ${cls}" cx="${f(ox)}" cy="${f(oy)}" r="9" fill="none"/>`;
        }
        const dx = x1 - x0, dy = y1 - y0, len = Math.hypot(dx, dy);
        const mx = (x0 + x1) / 2 + (-dy / len) * len * 0.22, my = (y0 + y1) / 2 + (dx / len) * len * 0.22;
        const u0 = [(mx - x0) / Math.hypot(mx - x0, my - y0), (my - y0) / Math.hypot(mx - x0, my - y0)];
        const u1 = [(x1 - mx) / Math.hypot(x1 - mx, y1 - my), (y1 - my) / Math.hypot(x1 - mx, y1 - my)];
        const sx = x0 + u0[0] * (NODE + 1), sy = y0 + u0[1] * (NODE + 1);
        const ex = x1 - u1[0] * (NODE + 2), ey = y1 - u1[1] * (NODE + 2);
        const hx = ex - u1[0] * 9, hy = ey - u1[1] * 9;
        return `<path class="bx-arrow ${cls}" d="M${f(sx)},${f(sy)} Q${f(mx)},${f(my)} ${f(ex)},${f(ey)}" fill="none"${dashed ? ' stroke-dasharray="6 4"' : ""}/>` +
               `<polygon class="bx-head ${cls}" points="${f(ex)},${f(ey)} ${f(hx + u1[1] * 4.5)},${f(hy - u1[0] * 4.5)} ${f(hx - u1[1] * 4.5)},${f(hy + u1[0] * 4.5)}"/>`;
      };
      const draw = () => {
        $(".out-n").textContent = String(st.n);
        const { notes, cut } = effective();
        const cycles = permCycles(notes), m = maxOpens();
        const colour = new Map();                    // box -> cycle class
        let k = 0;
        cycles.forEach((c) => {
          const cls = c.length > m ? "bx-long" : `bx-c${k++ % CYC}`;
          c.forEach((b) => colour.set(b, cls));
        });
        const walk = permWalk(notes, st.me, m);
        const shown = walk.opened.slice(0, st.step);
        const cur = shown[shown.length - 1];
        let s = `<svg class="figure bx-live" viewBox="0 0 ${W} ${W}" role="group" aria-label="${st.n} קופסאות במעגל, חץ מכל קופסה לקופסה שהפתק שלה מצביע עליה; לחיצה על קופסה בוחרת את האדם">`;
        for (let b = 1; b <= st.n; b++) {
          const dashed = cut && (b === cut[0] || b === cut[1]);
          const onPath = shown.includes(b) && shown.indexOf(b) < shown.length - 1;
          s += arrow(b, notes[b], colour.get(b) + (onPath ? " is-walked" : ""), dashed);
        }
        for (let b = 1; b <= st.n; b++) {
          const [x, y] = pt(b, R);
          const open = shown.indexOf(b);
          const cls = ["bx-node", colour.get(b), cut && (b === cut[0] || b === cut[1]) ? "is-cut" : "",
            open >= 0 ? "is-open" : "", b === cur ? "is-cur" : "", b === st.me ? "is-me" : ""].join(" ");
          s += `<g class="bx-g" data-b="${b}" tabindex="0" role="button" aria-label="קופסה ${b}, הפתק ${notes[b]}"><circle class="${cls}" cx="${f(x)}" cy="${f(y)}" r="${NODE}"><title>קופסה ${b}: הפתק ${notes[b]}</title></circle>` +
               `<text class="bx-num" x="${f(x)}" y="${f(y + 4)}" text-anchor="middle">${b}</text>`;
          if (open >= 0) { const [bx, by] = pt(b, R + 27); s += `<circle class="bx-badge" cx="${f(bx)}" cy="${f(by)}" r="9"/><text class="bx-badge-num" x="${f(bx)}" y="${f(by + 3.5)}" text-anchor="middle">${open + 1}</text>`; }
          s += `</g>`;
        }
        s += `</svg>`;
        ring.innerHTML = s;
        // the cycles, longest first in the text
        const longest = Math.max(...cycles.map((c) => c.length));
        $(".bx-cycles").innerHTML = (cycles.length === 1 ? "מעגל אחד: " : `${ltr(cycles.length)} מעגלים: `) + cycles.map((c) => {
          const cls = colour.get(c[0]);
          return `<span class="bx-chip ${cls}">${ltr(c.join(" → "))} (${c.length})</span>`;
        }).join(" ") + `. המעגל הארוך ביותר: ${ltr(longest)}, ומותר לפתוח ${ltr(m)}.`;
        const before = permHelper(st.notes, m);
        $(".bx-helper").innerHTML = !before
          ? `אדם 0 רואה שאין מעגל ארוך מ-${ltr(m)}, ולא נוגע בפתקים. כולם ימצאו את הפתק שלהם.`
          : st.helper
            ? `אדם 0 מחליף בין הפתקים של קופסה ${ltr(cut[0])} וקופסה ${ltr(cut[1])} (החצים המקווקווים): המעגל באורך ${ltr(permCycles(st.notes).find((c) => c.length > m).length)} מתפצל לשניים, ${ltr(cycles.filter((c) => c.includes(cut[0]) || c.includes(cut[1])).map((c) => c.length).join(" + "))}.`
            : `<span class="bx-bad">בלי אדם 0 יש מעגל באורך ${ltr(permCycles(st.notes).find((c) => c.length > m).length)}, וכל מי שעליו נכשל.</span>`;
        meIn.value = st.me;
        const line = shown.map((b, i) => `${i + 1}: קופסה ${ltr(b)} ← הפתק ${ltr(notes[b])}`);
        let end = "";
        if (st.step >= walk.opened.length) {
          end = walk.found
            ? ` <span class="bx-ok">✓ אדם ${ltr(st.me)} מצא את הפתק שלו אחרי ${walk.opened.length === 1 ? "פתיחה אחת" : `${ltr(walk.opened.length)} פתיחות`}.</span>`
            : ` <span class="bx-bad">✗ ${ltr(m)} פתיחות נגמרו ואדם ${ltr(st.me)} לא מצא את הפתק שלו: הוא על מעגל באורך ${ltr(cycles.find((c) => c.includes(st.me)).length)}.</span>`;
        }
        $(".bx-walk").innerHTML = `אדם ${ltr(st.me)} מתחיל בקופסה ${ltr(st.me)}.` + (line.length ? " " + line.join(", ") + "." : "") + end;
        // the rounds so far
        $(".bx-runs").textContent = st.runs ? `${num(st.runs)} סיבובים עד כה` : "";
        const pStrat = permStrategyProb(st.n, m), pRand = permRandomProb(st.n, m);
        const bar = (label, wins, p) => {
          const pct = st.runs ? (100 * wins) / st.runs : 0;
          return `<div class="bx-bar"><span class="bx-bar-label">${label}</span><span class="bx-bar-track"><span class="bx-bar-fill" style="width:${f(Math.min(100, pct))}%"></span></span>` +
                 `<span class="bx-bar-val">${st.runs ? `${ltr(num(wins))} (${ltr(f(pct, 1) + "%")})` : "—"}, צפוי ${ltr(f(100 * p, p < 0.01 ? 4 : 1) + "%")}</span></div>`;
        };
        $(".bx-bars").innerHTML = bar("האסטרטגיה בלי אדם 0", st.strat, pStrat) + bar(`כל אחד פותח ${ltr(m)} קופסאות אקראיות`, st.rand, pRand);
        const terms = []; for (let j = m + 1; j <= st.n; j++) terms.push(`1/${j}`);
        $(".bx-formula").innerHTML = `הצפי: האסטרטגיה מצליחה כשאין מעגל ארוך מ-${ltr(m)}, בהסתברות ${ltr(`1 − (${terms.join(" + ")}) ≈ ${fmt(pStrat, 4)}`)}; ` +
          `בחירה אקראית מצליחה לכל אחד בהסתברות ${ltr(`1/2`)}, ולכולם ${ltr(`(1/2)^${st.n} ≈ ${pRand < 1e-3 ? pRand.toExponential(2).replace("e-", "·10^−") : fmt(pRand, 4)}`)}. עם אדם 0 האסטרטגיה מצליחה תמיד.`;
      };
      const setN = (n) => { st.n = n; st.notes = permShuffle(n); st.me = Math.min(st.me, n); st.step = 0; st.runs = st.strat = st.rand = 0; draw(); };
      $(".ex-n").addEventListener("input", () => setN(Number($(".ex-n").value)));
      $(".ex-shuffle").addEventListener("click", () => { st.notes = permShuffle(st.n); st.step = 0; draw(); });
      $(".ex-example").addEventListener("click", () => { st.n = nmax; $(".ex-n").value = nmax; st.notes = EXAMPLE.slice(0, nmax + 1); st.me = 13; st.step = 0; draw(); });
      helperCb.addEventListener("change", () => { st.helper = helperCb.checked; st.step = 0; draw(); });
      const steps = () => permWalk(effective().notes, st.me, maxOpens()).opened.length;
      $(".ex-next").addEventListener("click", () => { st.step = Math.min(st.step + 1, steps()); draw(); });
      $(".ex-prev").addEventListener("click", () => { st.step = Math.max(st.step - 1, 0); draw(); });
      $(".ex-all").addEventListener("click", () => { st.step = steps(); draw(); });
      $(".ex-start").addEventListener("click", () => { st.step = 0; draw(); });
      meIn.addEventListener("change", () => {
        const v = Math.round(Number(meIn.value));
        if (v >= 1 && v <= st.n) { st.me = v; st.step = 0; }
        draw();
      });
      meIn.addEventListener("keydown", (e) => { if (e.key === "Enter") meIn.blur(); });
      ring.addEventListener("click", (e) => {
        const g = e.target.closest(".bx-g");
        if (!g) return;
        st.me = Number(g.dataset.b); st.step = 0; draw();
      });
      ring.addEventListener("keydown", (e) => {
        const g = e.target.closest(".bx-g");
        if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); st.me = Number(g.dataset.b); st.step = 0; draw(); }
      });
      $(".ex-rounds").addEventListener("click", () => {
        const m = maxOpens();
        for (let r = 0; r < 1000; r++) {
          const notes = permShuffle(st.n);
          if (permAllWin(notes, m)) st.strat++;
          if (permRandomPicks(notes, m)) st.rand++;
        }
        st.runs += 1000;
        draw();
      });
      $(".ex-rounds-reset").addEventListener("click", () => { st.runs = st.strat = st.rand = 0; draw(); });
      draw();
    },
  });

  // The Floyd box (0017): the array as a row of cells and as the graph i -> nums[i] laid
  // out as a rho (the tail in a line, the cycle as a circle, unreached indices below);
  // the tortoise and the hare step through the two phases, played or one step at a time.
  const floydView = () => ({
    mount(box) {
      const EXAMPLE = [3, 9, 5, 6, 7, 8, 1, 1, 2, 4];
      const nmax = Number(box.dataset.nmax || 12), NODE = 16;
      const st = { nums: EXAMPLE, k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏n</span><input type="range" class="ex-n" min="3" max="${nmax}" step="1" value="${EXAMPLE.length - 1}" dir="ltr"><output class="out-n"></output></label>` +
        `<button type="button" class="md-button md-button--primary ex-shuffle">הגרלה</button>` +
        `<button type="button" class="md-button ex-example">הדוגמה מהדף</button>` +
        `<label class="fl-input"><span>המערך</span><input type="text" class="ex-nums" dir="ltr" spellcheck="false" aria-label="המערך, מספרים מופרדים בפסיקים"></label>` +
        `<button type="button" class="md-button ex-apply">החלה</button><span class="fl-err" aria-live="polite"></span></div>` +
        `<div class="fl-cells" dir="ltr"></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1500">איטי</option><option value="700" selected>בינוני</option><option value="250">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<div class="fl-graph"></div><p class="fl-step" aria-live="polite"></p><p class="ex-summary fl-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), numsIn = $(".ex-nums");
      let timer = null;
      const graphSvg = (rho, fr, done) => {
        const { tail, cycle, entry, others } = rho;
        const pos = new Map();
        const GAP = 60;
        tail.forEach((v, i) => pos.set(v, [30 + GAP * i, 0]));
        const r = Math.max(48, (cycle.length * 44) / (2 * Math.PI));
        const cx = (tail.length ? 30 + GAP * (tail.length - 1) : -30) + GAP + r;
        cycle.forEach((v, i) => {
          const a = Math.PI - (2 * Math.PI * i) / cycle.length;     // the entry on the left
          pos.set(v, [cx + r * Math.cos(a), -r * Math.sin(a)]);
        });
        const top = r + 30, rowY = r + 70;
        others.forEach((v, i) => pos.set(v, [30 + 50 * i, rowY]));
        const W = Math.max(cx + r + 30, others.length ? 30 + 50 * (others.length - 1) + 30 : 0);
        const H = top + (others.length ? rowY : r) + 30;
        const P = (v) => { const [x, y] = pos.get(v); return [x, y + top]; };
        const dupEdges = done ? new Set(st.nums.map((v, i) => (v === entry ? i : -1)).filter((i) => i >= 0)) : new Set();
        let s = `<svg class="figure fl-live" viewBox="0 0 ${f(W, 0)} ${f(H, 0)}" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו">`;
        st.nums.forEach((v, i) => {
          const [x0, y0] = P(i), [x1, y1] = P(v);
          const faded = others.includes(i) ? " st-faded" : "";
          const hot = dupEdges.has(i);
          if (i === v) {                                           // nums[i] = i: a loop
            s += `<circle class="${hot ? "s2-line" : "ink-line"}${faded}" cx="${f(x0)}" cy="${f(y0 - NODE - 9)}" r="9" fill="none" stroke-width="2.2"/>`;
            return;
          }
          // edges of unreached indices bend upward, so a row of them stays readable
          const bend = faded ? 0.3 : 0;
          const d = Math.hypot(x1 - x0, y1 - y0);
          const mx = (x0 + x1) / 2 - ((y1 - y0) / d) * d * bend, my = (y0 + y1) / 2 + ((x1 - x0) / d) * d * bend - (faded ? 2 : 0);
          const d0 = Math.hypot(mx - x0, my - y0), d1 = Math.hypot(x1 - mx, y1 - my);
          const u0x = (mx - x0) / d0, u0y = (my - y0) / d0, ux = (x1 - mx) / d1, uy = (y1 - my) / d1;
          const ax = x0 + u0x * (NODE + 2), ay = y0 + u0y * (NODE + 2), bx = x1 - ux * (NODE + 3), by = y1 - uy * (NODE + 3);
          const hx = bx - ux * 9, hy = by - uy * 9;
          s += `<g class="fl-edge${faded}"><path class="${hot ? "s2-line" : "ink-line"}" d="M${f(ax)},${f(ay)} Q${f(mx)},${f(my)} ${f(bx)},${f(by)}" fill="none" stroke-width="${hot ? 3 : 2.2}"><title>nums[${i}] = ${v}</title></path>` +
               `<polygon class="${hot ? "s2-fill" : "ink-fill"}" points="${f(bx)},${f(by)} ${f(hx + uy * 4.5)},${f(hy - ux * 4.5)} ${f(hx - uy * 4.5)},${f(hy + ux * 4.5)}"/></g>`;
        });
        st.nums.forEach((_, v) => {
          const [x, y] = P(v);
          const cls = done && v === entry ? "st-ok" : "st-cell";
          s += `<g${others.includes(v) ? ' class="st-faded"' : ""}><circle class="${cls}" cx="${f(x)}" cy="${f(y)}" r="${NODE}"/>` +
               `<text class="st-text st-sm" x="${f(x)}" y="${f(y + 4)}" text-anchor="middle">${v}</text></g>`;
        });
        if (fr) {
          const [sx, sy] = P(fr.slow), [fx, fy] = P(fr.fast);
          s += `<circle class="fl-slow" cx="${f(sx)}" cy="${f(sy)}" r="${NODE + 5}"/><circle class="fl-fast" cx="${f(fx)}" cy="${f(fy)}" r="${NODE + 10}"/>`;
        }
        return s + "</svg>";
      };
      const draw = () => {
        const nums = st.nums, n = nums.length - 1;
        $(".out-n").textContent = String(n);
        if (document.activeElement !== numsIn) numsIn.value = nums.join(", ");
        const rho = floydRho(nums), tr = floydTrace(nums);
        st.k = Math.min(st.k, tr.frames.length - 1);
        const fr = tr.frames[st.k], last = st.k === tr.frames.length - 1;
        $(".fl-cells").innerHTML = `<div class="box-grid fl-grid" style="grid-template-columns: repeat(${n + 1}, minmax(0, 1fr))">` +
          nums.map((v, i) => `<span class="${[i === fr.slow ? "is-slow" : "", i === fr.fast ? "is-fast" : "", last && v === rho.entry ? "hl" : ""].join(" ").trim()}"><small>${i}</small><b>${v}</b></span>`).join("") + `</div>`;
        $(".fl-graph").innerHTML = graphSvg(rho, fr, last);
        $(".ex-pos").textContent = `צעד ${st.k} מתוך ${tr.frames.length - 1}`;
        let text;
        if (fr.phase === 1 && fr.step === 0) text = "שלב 1: הצב והארנב מתחילים באינדקס 0, שאף ערך לא מצביע עליו.";
        else if (fr.phase === 1 && fr.slow !== fr.fast) text = `שלב 1, איטרציה ${ltr(fr.step)}: הצב מתקדם צעד אחד ל-${ltr(fr.slow)}, והארנב שני צעדים ל-${ltr(fr.fast)}.`;
        else if (fr.phase === 1) text = `שלב 1, איטרציה ${ltr(fr.step)}: שניהם ב-${ltr(fr.slow)}. נפגשו בתוך המעגל, ומספר האיטרציות ${ltr(fr.step)} הוא כפולה של אורך המעגל ${ltr(rho.lambda)}.`;
        else if (fr.step === 0) text = `שלב 2: מחזירים את הצב ל-0. הארנב נשאר בנקודת המפגש ${ltr(tr.meet)}, ומעכשיו שניהם צועדים צעד אחד.`;
        else if (fr.slow !== fr.fast) text = `שלב 2, איטרציה ${ltr(fr.step)}: הצב ב-${ltr(fr.slow)}, הארנב ב-${ltr(fr.fast)}.`;
        else {
          const into = nums.map((v, i) => (v === rho.entry ? i : -1)).filter((i) => i >= 0);
          text = `שלב 2, איטרציה ${ltr(fr.step)}: שניהם ב-${ltr(fr.slow)}, הכניסה למעגל. ${into.length === 2 ? "שני חצים נכנסים" : `${ltr(into.length)} חצים נכנסים`} אליה, מהאינדקסים ${ltr(into.join(", "))}, ולכן <b>${ltr(fr.slow)}</b> הוא הערך הכפול.`;
        }
        $(".fl-step").innerHTML = text;
        $(".fl-sum").innerHTML = `הזנב: ${rho.mu === 0 ? "ריק" : ltr(rho.tail.join(" → "))} (${ltr(`μ = ${rho.mu}`)}), המעגל: ${ltr(rho.cycle.join(" → "))} (${ltr(`λ = ${rho.lambda}`)}). ` +
          `המפגש אחרי ${ltr(tr.frames.findIndex((g) => g.phase === 2) - 1)} איטרציות, ושלב 2 לוקח ${ltr(rho.mu)}. התשובה: ${ltr(tr.answer)}.` +
          (rho.others.length ? ` האינדקסים ${ltr(rho.others.join(", "))} לא נגישים מ-0 ולא משנים כלום.` : "");
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const setNums = (nums) => { stop(); st.nums = nums; st.k = 0; $(".ex-n").value = nums.length - 1; $(".fl-err").textContent = ""; draw(); };
      const total = () => floydTrace(st.nums).frames.length - 1;
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= total()) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      $(".ex-n").addEventListener("input", () => setNums(floydRandom(Number($(".ex-n").value))));
      $(".ex-shuffle").addEventListener("click", () => setNums(floydRandom(st.nums.length - 1)));
      $(".ex-example").addEventListener("click", () => setNums(EXAMPLE));
      const apply = () => {
        const nums = floydParse(numsIn.value);
        if (nums && nums.length - 1 <= nmax) setNums(nums);
        else $(".fl-err").textContent = `צריך n + 1 מספרים בין 1 ל-n, עם n עד ${nmax}.`;
      };
      $(".ex-apply").addEventListener("click", apply);
      numsIn.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); apply(); } });
      draw();
    },
  });

  // The remainders box (0005): the x remainders on a ring, the BFS tree growing one
  // dequeue at a time with +0 edges blue and +1 edges orange, the queue beside it, and at
  // the end the path back from 0 that spells the answer, with the step counts of the
  // three methods.
  const bfs01View = () => ({
    mount(box) {
      const xmax = Number(box.dataset.xmax || 40);
      const st = { x: Number(box.dataset.x || 7), k: 0 };
      const big = (s) => { const b = BigInt(s); return b < 10n ** 12n ? Number(b).toLocaleString("en-US") : `${(Number(b / 10n ** BigInt(s.length - 3)) / 100).toFixed(2)}·10^${s.length - 1}`; };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏x</span><input type="range" class="ex-x" min="1" max="${xmax}" step="1" value="${st.x}" dir="ltr"><output class="out-x"></output></label>` +
        `<span class="bf-presets">דוגמאות: ` + [7, 9, 11, 13, 37].filter((v) => v <= xmax).map((v) => `<button type="button" class="md-button ex-preset" data-x="${v}">${v}</button>`).join(" ") + `</span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1500">איטי</option><option value="700" selected>בינוני</option><option value="250">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<span class="viz-legend"><span><i class="s1"></i>הוספת 0</span><span><i class="s2"></i>הוספת 1</span><span><i class="st-stack"></i>בתור</span><span><i class="st-done"></i>טופל</span><span><i class="st-ok"></i>שארית 0</span></span>` +
        `<div class="bf-box"><div class="bf-ring"></div><div class="bf-panel"><p class="bf-step" aria-live="polite"></p><p class="bf-queue"></p><p class="bf-path"></p></div></div>` +
        `<p class="ex-summary bf-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let timer = null, trace = null;
      const ringSvg = (tr, k) => {
        const x = st.x, W = 360, C = 180, R = x <= 12 ? 120 : 140, NODE = x <= 12 ? 16 : x <= 24 ? 13 : 10;
        const pt = (r, rad) => { const a = -Math.PI / 2 + (2 * Math.PI * r) / x; return [C + rad * Math.cos(a), C + rad * Math.sin(a)]; };
        const done = new Set(), queued = new Set(tr.frames.length ? [tr.start] : []);
        const edges = [];
        for (let i = 0; i < k; i++) {
          const fr = tr.frames[i];
          done.add(fr.r); queued.delete(fr.r);
          fr.kids.forEach((kid) => { if (kid.status !== "seen") { queued.add(kid.nr); edges.push([fr.r, kid.nr, kid.d, false]); } });
        }
        const cur = k > 0 ? tr.frames[k - 1] : null;
        if (cur) cur.kids.forEach((kid) => { if (kid.status === "seen") edges.push([cur.r, kid.nr, kid.d, true]); });
        const finished = k >= tr.frames.length;
        const onPath = new Set(finished ? tr.path : []);
        let s = `<svg class="figure bf-live" viewBox="0 0 ${W} ${W}" role="img" aria-label="${x} השאריות מודולו ${x} במעגל, ועץ ה-BFS">`;
        const arrow = (a, b, cls, dashed, thick) => {
          const [x0, y0] = pt(a, R), [x1, y1] = pt(b, R);
          if (a === b) {
            const [ox, oy] = pt(a, R + NODE + 10);
            return `<circle class="${cls}" cx="${f(ox)}" cy="${f(oy)}" r="8" fill="none" stroke-width="${thick ? 3.5 : 2}"${dashed ? ' stroke-dasharray="4 3"' : ""}/>`;
          }
          const dx = x1 - x0, dy = y1 - y0, len = Math.hypot(dx, dy);
          const mx = (x0 + x1) / 2 + (-dy / len) * len * 0.2, my = (y0 + y1) / 2 + (dx / len) * len * 0.2;
          const d1 = Math.hypot(x1 - mx, y1 - my), ux = (x1 - mx) / d1, uy = (y1 - my) / d1;
          const d0 = Math.hypot(mx - x0, my - y0), vx = (mx - x0) / d0, vy = (my - y0) / d0;
          const sx = x0 + vx * (NODE + 1), sy = y0 + vy * (NODE + 1), ex = x1 - ux * (NODE + 2), ey = y1 - uy * (NODE + 2);
          const hx = ex - ux * 8, hy = ey - uy * 8;
          return `<path class="${cls}" d="M${f(sx)},${f(sy)} Q${f(mx)},${f(my)} ${f(ex)},${f(ey)}" fill="none" stroke-width="${thick ? 3.5 : 2}"${dashed ? ' stroke-dasharray="4 3"' : ""}/>` +
                 (dashed ? "" : `<polygon class="${cls === "s1-line" ? "s1-fill" : "s2-fill"}" points="${f(ex)},${f(ey)} ${f(hx + uy * 4)},${f(hy - ux * 4)} ${f(hx - uy * 4)},${f(hy + ux * 4)}"/>`);
        };
        edges.forEach(([a, b, d, pruned]) => {
          const thick = onPath.has(a) && onPath.has(b) && tr.parent[b] === a;
          s += arrow(a, b, d === 0 ? "s1-line" : "s2-line", pruned, thick);
        });
        for (let r = 0; r < x; r++) {
          const [px, py] = pt(r, R);
          const cls = finished && r === 0 ? "st-ok" : cur && r === cur.r ? "st-stack is-cur" : queued.has(r) ? "st-stack" : done.has(r) ? "st-done" : "st-cell";
          s += `<g><circle class="${cls}${onPath.has(r) ? " is-path" : ""}" cx="${f(px)}" cy="${f(py)}" r="${NODE}"><title>שארית ${r}</title></circle>` +
               `<text class="st-text ${x <= 12 ? "st-sm" : "bf-xs"}" x="${f(px)}" y="${f(py + (x <= 12 ? 4 : 3.5))}" text-anchor="middle">${r}</text></g>`;
        }
        return s + "</svg>";
      };
      const draw = () => {
        $(".out-x").textContent = String(st.x);
        trace = bfs01Trace(st.x);
        const tr = trace, total = tr.frames.length;
        st.k = Math.min(st.k, total);
        $(".bf-ring").innerHTML = ringSvg(tr, st.k);
        $(".ex-pos").textContent = `הוצאה ${st.k} מתוך ${total}`;
        const name = (r, n) => `${ltr(`r = ${r}`)} (המספר ${ltr(n)})`;
        let step;
        if (st.k === 0) {
          step = total === 0
            ? `עבור ${ltr(`x = ${st.x}`)} המספר 1 כבר נותן שארית 0, ולכן התשובה היא 1 בלי צעדים.`
            : `מתחילים מהמספר 1, שארית ${ltr(1 % st.x)}. התור: ${ltr(`[${1 % st.x}]`)}.`;
        } else {
          const fr = tr.frames[st.k - 1];
          const kid = (kd) => {
            const n = fr.number + kd.d;
            return `${ltr(`+${kd.d}`)} → ${ltr(n)}, שארית ${ltr(kd.nr)}: ` +
              (kd.status === "new" ? "חדשה, נכנסת לתור" : kd.status === "seen" ? `כבר נראתה, נגזמת ✗` : `<b>0, מצאנו ✓</b>`);
          };
          step = `הוצאה ${ltr(st.k)}: מוציאים ${name(fr.r, fr.number)}. ${kid(fr.kids[0])}; ${kid(fr.kids[1])}.`;
        }
        $(".bf-step").innerHTML = step;
        const q = st.k === 0 ? (total ? [1 % st.x] : []) : tr.frames[st.k - 1].queue;
        $(".bf-queue").innerHTML = st.k > 0 ? `התור אחרי הצעד: ${ltr(`[${q.join(", ")}]`)}.` : "";
        const finished = st.k >= total;
        $(".bf-path").innerHTML = finished
          ? `השחזור: ${ltr(tr.path.slice().reverse().map((r, i) => (i === 0 ? "0" : `← ${r}`)).join(" "))}, הספרות מהסוף להתחלה נותנות <b>${ltr(`y = ${tr.answer}`)}</b> (${ltr(`${tr.answer.length}`)} ספרות).`
          : "";
        const c = bfs01Counts(st.x);
        $(".bf-sum").innerHTML = `עבור ${ltr(`x = ${st.x}`)}: ה-BFS מוציא מהתור ${ltr(c.dequeues)} שאריות${c.dequeues < st.x ? ` (פחות מ-${ltr(st.x)})` : ""}. ` +
          `לשם השוואה, המעבר על מספרי 0/1 בודק ${ltr(big(c.enumerated))} מספרים, והמעבר על הכפולות של ${ltr(st.x)} בודק ${ltr(big(c.multiples))}.`;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => bfs01Trace(st.x).frames.length;
      const setX = (x) => { stop(); st.x = x; st.k = 0; $(".ex-x").value = x; draw(); };
      $(".ex-x").addEventListener("input", () => setX(Number($(".ex-x").value)));
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => setX(Number(b.dataset.x))));
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= total()) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      draw();
    },
  });

  // The brackets box (0010): a typed string of brackets (other characters are dropped),
  // the characters as cells with the one being read marked, the stack as a column that
  // grows and shrinks, the depth chart, and the first failure circled with its reason.
  const bracketsView = () => ({
    mount(box) {
      const PRESETS = ["()", "()[]{}", "{[()]}", "([]{})", "(]", "([)]", "(((", "())", ")("];
      const st = { s: box.dataset.s || "{[()]}", k: 0 };
      const NAMES = { "(": "עגול", "[": "מרובע", "{": "מסולסל" };
      const esc = (c) => c.replace(/</g, "&lt;");
      box.innerHTML =
        `<div class="ex-controls"><label><span>המחרוזת</span><input type="text" class="ex-s" dir="ltr" spellcheck="false" maxlength="40" aria-label="מחרוזת של סוגריים"></label>` +
        `<span class="br-presets">דוגמאות: ` + PRESETS.map((p) => `<button type="button" class="md-button ex-preset" dir="ltr" data-s="${esc(p)}">${esc(p)}</button>`).join(" ") + `</span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">התו הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">התו הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1200">איטי</option><option value="600" selected>בינוני</option><option value="200">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<div class="br-box"><div class="br-main"><div class="br-chars" dir="ltr"></div><div class="br-chart"></div></div>` +
        `<div class="br-stackwrap"><p class="ex-title">המחסנית</p><div class="br-stack" dir="ltr"></div></div></div>` +
        `<p class="br-step" aria-live="polite"></p><p class="ex-summary br-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), input = $(".ex-s");
      let timer = null;
      const draw = () => {
        const s = st.s, tr = bracketsTrace(s), total = tr.frames.length;
        st.k = Math.min(st.k, total);
        if (document.activeElement !== input) input.value = s;
        const fr = st.k ? tr.frames[st.k - 1] : null;
        const failAt = tr.fail && st.k >= total ? tr.fail.i : -1;
        $(".br-chars").innerHTML = s.length ? [...s].map((c, i) =>
          `<span class="${[i === st.k - 1 ? "is-cur" : "", i < st.k - 1 || (i === st.k - 1 && fr.action !== "mismatch" && fr.action !== "unopened") ? "is-done" : "", i === failAt ? "is-fail" : ""].join(" ").trim()}">${esc(c)}</span>`).join("") +
          (tr.fail && tr.fail.kind === "unclosed" && st.k >= total ? `<span class="is-fail is-end" aria-label="סוף המחרוזת">⏎</span>` : "")
          : `<span class="br-empty">(מחרוזת ריקה)</span>`;
        const stack = fr ? fr.stack : "";
        $(".br-stack").innerHTML = stack.length ? [...stack].map((c, i) =>
          `<span class="${i === stack.length - 1 ? "is-top" : ""}">${esc(c)}</span>`).join("") : `<span class="br-empty">ריקה</span>`;
        // the depth after each character read so far
        const depths = tr.frames.map((g) => g.stack.length);
        const n = Math.max(s.length, 1), W = 320, H = 90, X0 = 8, BASE = H - 18, dmax = Math.max(1, ...depths);
        const slot = (W - 2 * X0) / n, bw = Math.max(2, slot * 0.7);
        let c = `<svg class="perf-chart br-depth" viewBox="0 0 ${W} ${H}" role="img" aria-label="עומק המחסנית אחרי כל תו"><line class="axis" x1="${X0}" x2="${W - X0}" y1="${BASE}" y2="${BASE}"/>`;
        for (let d = 1; d <= dmax; d++) { const y = BASE - (d / dmax) * (BASE - 10); c += `<line class="grid" x1="${X0}" x2="${W - X0}" y1="${f(y)}" y2="${f(y)}"/><text class="tick" x="${W - X0 + 2}" y="${f(y + 3)}" font-size="8">${d}</text>`; }
        depths.slice(0, st.k).forEach((d, i) => {
          const h = (d / dmax) * (BASE - 10);
          const cls = i === failAt ? "by-enum" : "by-multiples";
          c += `<rect class="bar ${cls}" x="${f(X0 + i * slot + (slot - bw) / 2)}" y="${f(BASE - h)}" width="${f(bw)}" height="${f(h)}"><title>אחרי התו ${i + 1}: עומק ${d}</title></rect>`;
        });
        if (s.length <= 24) [...s].forEach((ch, i) => { c += `<text class="tick" x="${f(X0 + (i + 0.5) * slot)}" y="${BASE + 12}" text-anchor="middle" font-size="9">${esc(ch)}</text>`; });
        $(".br-chart").innerHTML = c + "</svg>";
        $(".ex-pos").textContent = `תו ${st.k} מתוך ${s.length}`;
        let step;
        if (!fr) step = s.length ? "לפני התו הראשון המחסנית ריקה." : "המחרוזת הריקה תקינה: אין מה לפתוח ואין מה לסגור.";
        else if (fr.action === "push") step = `התו ${ltr(esc(fr.ch))} פותח, ולכן נדחף למחסנית.`;
        else if (fr.action === "pop") step = `התו ${ltr(esc(fr.ch))} סוגר, בראש המחסנית ${ltr(esc(BRACKET_OF[fr.ch]))} מאותו סוג, ולכן מוציאים אותו.`;
        else if (fr.action === "mismatch") step = `<span class="br-bad">✗ התו ${ltr(esc(fr.ch))} סוגר ${NAMES[BRACKET_OF[fr.ch]]}, אבל בראש המחסנית ${ltr(esc(fr.top))}: הסוגר שנפתח אחרון עוד לא נסגר. סוג לא מתאים או סדר לא נכון.</span>`;
        else step = `<span class="br-bad">✗ התו ${ltr(esc(fr.ch))} סוגר, אבל המחסנית ריקה: אין לו סוגר פותח.</span>`;
        if (st.k >= total && tr.fail && tr.fail.kind === "unclosed") step += ` <span class="br-bad">✗ המחרוזת נגמרה והמחסנית לא ריקה: ${ltr(esc(tr.fail.left))} לא נסגרו.</span>`;
        if (st.k >= total && tr.valid && s.length) step += ` <span class="br-ok">✓ כל התווים נקראו והמחסנית ריקה: המחרוזת תקינה.</span>`;
        $(".br-step").innerHTML = step;
        $(".br-sum").innerHTML = (tr.valid ? `<span class="br-ok">תקינה ✓</span>` : `<span class="br-bad">לא תקינה ✗</span>`) +
          (tr.odd ? `, ואפשר לדעת את זה מיד: האורך ${ltr(s.length)} אי-זוגי, והקוד עוצר לפני המחסנית.` : ".") +
          ` העומק המרבי של המחסנית: ${ltr(Math.max(0, ...depths))}.`;
      };
      const total = () => bracketsTrace(st.s).frames.length;
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const setS = (s) => { stop(); st.s = bracketsClean(s).slice(0, 40); st.k = 0; draw(); };
      input.addEventListener("input", () => { const v = bracketsClean(input.value).slice(0, 40); if (v !== input.value) input.value = v; setS(v); });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { setS(b.dataset.s); st.k = total(); draw(); }));
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= total()) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      draw();
    },
  });

  // The tic-tac-toe box (0011): tap a cell to cycle empty, X, O; the page's conditions
  // decide live whether the board is a legal final board and say why not; a random
  // legal board as the page's randomize() draws it; the wrap-around diagonals of part b
  // as a toggle, with the counts of final boards per line set.
  const tttView = () => ({
    mount(box) {
      const st = { board: (box.dataset.board || "XXXOXOOOX").split(""), wrap: false };
      const num = (v) => Number(v).toLocaleString("en-US");
      const REASON = {
        count: "מספר ה-X חייב להיות שווה למספר ה-O או גדול ממנו ב-1: X מתחיל ומשחקים לסירוגין.",
        both: "לשני השחקנים יש שלישייה. המשחק נעצר ברגע שהראשון השלים אחת.",
        o_after: "ל-X יש שלישייה אבל מספר ה-X שווה למספר ה-O: O שיחק אחרי שהמשחק נגמר.",
        x_after: "ל-O יש שלישייה אבל ל-X יש סימן אחד יותר: X שיחק אחרי שהמשחק נגמר.",
        unfinished: "אין שלישייה והלוח לא מלא: המשחק עוד לא נגמר.",
      };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<button type="button" class="md-button md-button--primary ex-random">לוח חוקי אקראי</button>` +
        `<button type="button" class="md-button ex-clear">ניקוי</button>` +
        `<label><input type="checkbox" class="ex-wrap"> אלכסונים מסביב (סעיף ב)</label></div>` +
        `<div class="ttt-box"><div class="ttt-board" role="group" aria-label="לוח 3 על 3, לחיצה על משבצת מחליפה ריק, X ו-O"></div>` +
        `<div class="ttt-panel"><p class="ttt-counts"></p><p class="ttt-verdict" aria-live="polite"></p><p class="ttt-why"></p></div></div>` +
        `<p class="ex-summary ttt-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const boardEl = $(".ttt-board");
      const draw = () => {
        const chk = tttCheck(st.board, st.wrap);
        const lit = new Set();
        chk.xLines.concat(chk.oLines).forEach((i) => chk.lines[i].forEach((c) => lit.add(c)));
        const tint = chk.result === "X" || (chk.xLines.length && !chk.oLines.length) ? "cell-s2" : "cell-s1";
        let s = `<svg class="figure ttt-live" viewBox="0 0 114 114">`;
        st.board.forEach((v, i) => {
          const x = 6 + (i % 3) * 34, y = 6 + Math.floor(i / 3) * 34;
          const inX = chk.xLines.some((l) => chk.lines[l].includes(i));
          s += `<g class="ttt-cell" data-i="${i}" tabindex="0" role="button" aria-label="${v === "." ? `${i}: משבצת ריקה` : `${v} במשבצת ${i}`}">` +
               `<rect class="${lit.has(i) ? (inX ? "cell-s2" : "cell-s1") : "ttt-empty"}" x="${x}" y="${y}" width="34" height="34"/>`;
          if (v === "X") s += `<path class="mark" d="M${x + 9},${y + 9} L${x + 25},${y + 25} M${x + 25},${y + 9} L${x + 9},${y + 25}"/>`;
          else if (v === "O") s += `<circle class="mark" cx="${x + 17}" cy="${y + 17}" r="9"/>`;
          else s += `<text class="ttt-idx" x="${x + 17}" y="${y + 21}" text-anchor="middle">${i}</text>`;
          s += `</g>`;
        });
        s += `<line class="ttt-grid" x1="40" x2="40" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="40" y2="40"/>` +
             `<line class="ttt-grid" x1="74" x2="74" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="74" y2="74"/></svg>`;
        boardEl.innerHTML = s;
        void tint;
        const names = (ls) => ls.map((i) => ltr(`{${chk.lines[i].join(", ")}}`)).join(", ");
        $(".ttt-counts").innerHTML = `${ltr(`n_X = ${chk.nX}`)}, ${ltr(`n_O = ${chk.nO}`)}. שלישיות של X: ${chk.xLines.length ? names(chk.xLines) : "אין"}; של O: ${chk.oLines.length ? names(chk.oLines) : "אין"}.`;
        const verdict = chk.result
          ? `<span class="ttt-ok">✓ לוח סיום חוקי: ${chk.result === "draw" ? "תיקו" : `${chk.result} ניצח`}.</span>`
          : `<span class="ttt-bad">✗ לא לוח סיום.</span>`;
        $(".ttt-verdict").innerHTML = verdict;
        $(".ttt-why").innerHTML = chk.result
          ? (chk.result === "draw" ? "הלוח מלא ולאף אחד אין שלישייה." : chk.result === "X"
            ? `ל-X ${chk.xLines.length === 2 ? "שתי שלישיות שנחתכות" : "שלישייה"}, ל-O אין, ו-${ltr("n_X = n_O + 1")}: X שיחק אחרון.`
            : `ל-O שלישייה, ל-X אין, ו-${ltr("n_X = n_O")}: O שיחק אחרון.`)
          : REASON[chk.reason];
        const g = tttFinalBoards(st.wrap), total = g.X.length + g.O.length + g.draw.length;
        $(".ttt-sum").innerHTML = `עם ${st.wrap ? "12" : "8"} הקווים יש ${ltr(num(total))} לוחות סיום מתוך ${ltr("3^9 = 19,683")} מילויים: ` +
          `${ltr(num(g.X.length))} ניצחונות של X, ${ltr(num(g.O.length))} של O ו-${ltr(num(g.draw.length))} תיקו` +
          (st.wrap ? ". תיקו בלתי אפשרי: כל 5 משבצות מכילות קו שלם." : ".") +
          ` "לוח חוקי אקראי" בוחר תוצאה בהסתברות שווה ואז לוח אחיד מבין הלוחות שלה, כמו ${ltr("solve result before board")}.`;
      };
      const cycle = (i) => { st.board[i] = { ".": "X", X: "O", O: "." }[st.board[i]]; draw(); };
      boardEl.addEventListener("click", (e) => { const g = e.target.closest(".ttt-cell"); if (g) cycle(Number(g.dataset.i)); });
      boardEl.addEventListener("keydown", (e) => {
        const g = e.target.closest(".ttt-cell");
        if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); cycle(Number(g.dataset.i)); }
      });
      $(".ex-random").addEventListener("click", () => { st.board = tttRandom(st.wrap).board; draw(); });
      $(".ex-clear").addEventListener("click", () => { st.board = new Array(9).fill("."); draw(); });
      $(".ex-wrap").addEventListener("change", () => { st.wrap = $(".ex-wrap").checked; draw(); });
      draw();
    },
  });

  // The shapes box (0014): sliders for the grid and the number of shapes, squares or
  // rectangles; "one shape" draws candidates at random and flashes the overlapping ones
  // in red until a free one lands; "a whole draw" runs the page's random_shapes; a heat
  // map over many draws shows where shapes land and which sizes dominate.
  const shapesView = () => ({
    mount(box) {
      const st = { N: Number(box.dataset.n || 10), M: Number(box.dataset.m || 8), max: Number(box.dataset.max || 6), squares: true, shapes: [], heat: null, flash: null };
      const num = (v) => Number(v).toLocaleString("en-US");
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏N (עמודות)</span><input type="range" class="ex-N" min="3" max="14" step="1" value="${st.N}" dir="ltr"><output class="out-N"></output></label>` +
        `<label><span>‏M (שורות)</span><input type="range" class="ex-M" min="3" max="12" step="1" value="${st.M}" dir="ltr"><output class="out-M"></output></label>` +
        `<label><span>צורות לכל היותר</span><input type="range" class="ex-max" min="1" max="10" step="1" value="${st.max}" dir="ltr"><output class="out-max"></output></label>` +
        `<label><select class="ex-kind" aria-label="סוג הצורות"><option value="squares" selected>ריבועים (סעיף א)</option><option value="rects">מלבנים (סעיף ב)</option></select></label></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-one">עוד צורה</button>` +
        `<button type="button" class="md-button ex-all">הגרלה שלמה</button>` +
        `<button type="button" class="md-button ex-clear">ניקוי</button>` +
        `<button type="button" class="md-button ex-heat">500 הגרלות למפת חום</button><span class="sh-note" aria-live="polite"></span></div>` +
        `<div class="sh-box"><div class="sh-grid"></div><div class="sh-heat"></div></div>` +
        `<p class="sh-step" aria-live="polite"></p><p class="ex-summary sh-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      let timer = null;
      const geom = () => { const u = Math.min(30, 300 / Math.max(st.N - 1, st.M - 1)); return { u, W: (st.N - 1) * u + 40, H: (st.M - 1) * u + 30, X: (x) => 30 + (x - 1) * u, Y: (y) => 10 + (st.M - y) * u }; };
      const gridSvg = (extra, label) => {
        const g = geom();
        let s = `<svg class="figure sh-live" viewBox="0 0 ${f(g.W, 0)} ${f(g.H, 0)}" role="img" aria-label="${label}">`;
        for (let x = 1; x <= st.N; x++) s += `<line class="gp-line" x1="${f(g.X(x))}" x2="${f(g.X(x))}" y1="${f(g.Y(st.M))}" y2="${f(g.Y(1))}"/>`;
        for (let y = 1; y <= st.M; y++) s += `<line class="gp-line" x1="${f(g.X(1))}" x2="${f(g.X(st.N))}" y1="${f(g.Y(y))}" y2="${f(g.Y(y))}"/>`;
        s += extra(g);
        for (let x = 1; x <= st.N; x++) s += `<text class="tick" x="${f(g.X(x))}" y="${f(g.Y(1) + 14)}" text-anchor="middle" font-size="9">${x}</text>`;
        for (let y = 1; y <= st.M; y++) s += `<text class="tick" x="${f(g.X(1) - 8)}" y="${f(g.Y(y) + 3)}" text-anchor="end" font-size="9">${y}</text>`;
        return s + "</svg>";
      };
      const rect = (g, [x1, y1, x2, y2], cls, extra = "") =>
        `<rect class="${cls}" x="${f(g.X(x1))}" y="${f(g.Y(y2))}" width="${f(g.X(x2) - g.X(x1))}" height="${f(g.Y(y1) - g.Y(y2))}"${extra}><title>(${x1}, ${y1}) → (${x2}, ${y2})</title></rect>`;
      const draw = () => {
        ["N", "M", "max"].forEach((k) => { $(`.out-${k}`).textContent = String(st[k]); });
        $(".sh-grid").innerHTML = gridSvg((g) => {
          let s = st.shapes.map((sh, i) => rect(g, sh, i % 2 ? "shp-2" : "shp-1") +
            `<text class="coord halo" x="${f((g.X(sh[0]) + g.X(sh[2])) / 2)}" y="${f((g.Y(sh[1]) + g.Y(sh[3])) / 2 + 4)}" text-anchor="middle" font-size="11">${i + 1}</text>`).join("");
          if (st.flash) s += rect(g, st.flash.shape, st.flash.ok ? "sh-accept" : "sh-reject");
          return s;
        }, `grid של ${st.N} על ${st.M} נקודות עם ${st.shapes.length} צורות`);
        const all = shapesCandidates(st.N, st.M, st.squares).length;
        const free = shapesCandidates(st.N, st.M, st.squares).filter((c) => !st.shapes.some((s) => shapesOverlap(c, s))).length;
        const ok = shapesOk(st.N, st.M, st.shapes, st.squares);
        $(".sh-sum").innerHTML = `${st.squares ? "ריבועים" : "מלבנים"} אפשריים על ה-grid: ${ltr(num(all))}; מהם ${ltr(num(free))} לא חופפים את ${st.shapes.length === 1 ? "הצורה שכבר יש" : `${ltr(st.shapes.length)} הצורות שכבר יש`}. ` +
          (st.shapes.length ? `הבודק ${ltr("shapes_ok")} של הדף: ${ok ? "✓ תקין" : "✗ חפיפה"}.` : "");
        if (st.heat) {
          const h = st.heat, top = Math.max(1, ...h.cells.flat());
          $(".sh-heat").innerHTML = gridSvg((g) => {
            let s = "";
            h.cells.forEach((row, yi) => row.forEach((v, xi) => {
              s += `<rect class="sh-cell" x="${f(g.X(xi + 1))}" y="${f(g.Y(yi + 2))}" width="${f(g.u)}" height="${f(g.u)}" fill-opacity="${f(0.85 * v / top, 2)}"><title>תא (${xi + 1}, ${yi + 1}): ${v} מתוך ${h.rounds} הגרלות</title></rect>`;
            }));
            return s;
          }, "מפת חום: כמה פעמים כל תא כוסה") +
            `<p class="sh-sides">${ltr(num(h.rounds))} הגרלות, ${ltr(num(h.count))} צורות (${ltr(f(h.count / h.rounds, 2))} בממוצע). לפי הצלע הארוכה: ` +
            h.sides.map((v, k) => (v ? `${ltr(k)}: ${ltr(f(100 * v / h.count, 1) + "%")}` : "")).filter(Boolean).join(", ") +
            `. רוב הצורות קטנות, כי רוב המועמדים קטנים: צלע 1 לבדה היא ${ltr(`${(st.N - 1) * (st.M - 1)} מתוך ${all}`)} ${st.squares ? "הריבועים" : "המלבנים"}${st.squares ? "" : " (וגם מלבנים דקים רבים)"}.</p>`;
        } else $(".sh-heat").innerHTML = "";
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; st.flash = null; };
      const reset = () => { stop(); st.shapes = []; st.heat = null; $(".sh-step").textContent = ""; $(".sh-note").textContent = ""; draw(); };
      ["N", "M", "max"].forEach((k) => $(`.ex-${k}`).addEventListener("input", () => { st[k] = Number($(`.ex-${k}`).value); reset(); }));
      $(".ex-kind").addEventListener("change", () => { st.squares = $(".ex-kind").value === "squares"; reset(); });
      $(".ex-clear").addEventListener("click", reset);
      $(".ex-one").addEventListener("click", () => {
        stop();
        if (st.shapes.length >= st.max) { $(".sh-step").innerHTML = `כבר יש ${ltr(st.max)} צורות, המספר המרבי. "ניקוי" מתחיל מחדש.`; return; }
        const t = shapesTry(st.N, st.M, st.shapes, st.squares);
        if (!t.shape) { $(".sh-step").innerHTML = `<span class="sh-bad">אין מקום לאף צורה נוספת: כל ${ltr(num(t.all))} המועמדים חופפים. הקוד בדף מתחיל את ההגרלה מהתחלה.</span>`; return; }
        let k = 0;
        const step = () => {
          const c = t.tries[k], last = k === t.tries.length - 1;
          st.flash = { shape: c, ok: last };
          $(".sh-step").innerHTML = last
            ? `<span class="sh-ok">✓ ניסיון ${ltr(k + 1)}: ${ltr(`(${c[0]}, ${c[1]}) → (${c[2]}, ${c[3]})`)} לא חופף, נכנס.</span> ${t.tries.length === 1 ? "" : `${ltr(t.tries.length - 1)} מועמדים נדחו לפניו.`} מועמדים פנויים: ${ltr(num(t.free))} מתוך ${ltr(num(t.all))}.`
            : `<span class="sh-bad">✗ ניסיון ${ltr(k + 1)}: ${ltr(`(${c[0]}, ${c[1]}) → (${c[2]}, ${c[3]})`)} חופף צורה קיימת, נדחה.</span>`;
          draw();
          k++;
          if (last) { clearInterval(timer); timer = null; st.shapes.push(c); st.flash = null; draw(); }
        };
        step();
        if (t.tries.length > 1) timer = setInterval(step, 350);
      });
      $(".ex-all").addEventListener("click", () => {
        stop(); st.heat = null;
        st.shapes = shapesRandom(st.N, st.M, st.max, st.squares);
        $(".sh-step").innerHTML = `הגרלה שלמה כמו ${ltr("random_shapes")}: ${ltr(st.shapes.length)} ${st.shapes.length === 1 ? "צורה" : "צורות"} (מספר אחיד בין 1 ל-${ltr(st.max)}), כל אחת אחידה מבין המועמדים הפנויים אחרי קודמותיה.`;
        draw();
      });
      $(".ex-heat").addEventListener("click", () => {
        stop();
        $(".sh-note").textContent = "מחשב…";
        setTimeout(() => { st.heat = shapesHeat(st.N, st.M, st.max, st.squares, 500); $(".sh-note").textContent = ""; draw(); }, 20);
      });
      draw();
    },
  });

  // The Kaprekar box (0012, 0013): a typed or random number, its sort-and-subtract step,
  // the chain of steps until the value stops changing, and a histogram of chain lengths
  // over every number with the typed one marked.
  const kaprekarView = () => ({
    mount(box) {
      const d = Number(box.dataset.digits || 3), MAX = Math.pow(10, d) - 1;
      const FIXED = d === 3 ? 495 : 6174;
      const presets = (box.dataset.presets || (d === 3 ? "352,7,45,111,0" : "3524,95,1000,7777,0")).split(",").map(Number);
      const st = { x: Number(box.dataset.x || presets[0]) };
      const pad = (v) => String(v).padStart(d, "0");
      const num = (v) => Number(v).toLocaleString("en-US");
      box.innerHTML =
        `<div class="ex-controls"><label><span>המספר</span><input type="number" class="ex-x" min="0" max="${MAX}" step="1" dir="ltr" aria-label="מספר בין 0 ל-${MAX}"></label>` +
        `<button type="button" class="md-button md-button--primary ex-random">הגרלה</button>` +
        `<span class="kp-presets">דוגמאות: ` + presets.map((p) => `<button type="button" class="md-button ex-preset" data-x="${p}">${p}</button>`).join(" ") + `</span></div>` +
        `<div class="kp-table"></div><p class="kp-chain" aria-live="polite"></p>` +
        `<p class="ex-title">מספר הצעדים עד שהערך מפסיק להשתנות, על כל ${ltr(num(MAX + 1))} המספרים; המספר שלכם מסומן</p><div class="kp-chart"></div><p class="ex-summary kp-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const input = $(".ex-x");
      const H = kapHistogram(d);
      const draw = () => {
        const c = kapChain(st.x, d);
        if (document.activeElement !== input) input.value = st.x;
        $(".kp-table").innerHTML = `<table tabindex="0" aria-label="צעדי המיון והחיסור"><thead><tr><th>צעד</th><th>המספר</th><th>מהגדול לקטן</th><th>מהקטן לגדול</th><th>ההפרש</th><th>מיוחד?</th></tr></thead><tbody>` +
          c.steps.map((s, k) => `<tr${k === c.steps.length - 1 ? ' class="is-last"' : ""}><td>${ltr(k + 1)}</td><td>${ltr(pad(s.x))}</td><td>${ltr(s.digits)}</td><td>${ltr(pad(s.smallest))}</td><td>${ltr(pad(s.diff))}</td><td>${s.special ? "✓" : "✗"}</td></tr>`).join("") +
          `</tbody></table>`;
        const chain = c.steps.map((s) => pad(s.x)).concat(c.fixed ? [] : [pad(c.end)]);
        const first = c.steps[0];
        let text = first.special
          ? `<b>${ltr(pad(st.x))} מיוחד:</b> ההפרש שלו הוא הוא עצמו, ולכן השרשרת לא זזה.`
          : `${ltr(pad(st.x))} לא מיוחד. מפעילים את הצעד שוב על ההפרש: ${ltr(chain.join(" → "))}` +
            (c.fixed ? `, ואחרי ${c.length === 1 ? "צעד אחד" : `${ltr(c.length)} צעדים`} מגיעים ל-<b>${ltr(pad(c.end))}</b>, שהוא מיוחד ונשאר.` : `, ועדיין לא נעצר.`);
        if (c.end === 0 && !first.special) text += ` כל הספרות שוות, ולכן ההפרש הוא 0 ושם זה נגמר.`;
        $(".kp-chain").innerHTML = text;
        const hist = H.hist[FIXED] || [], hist0 = H.hist[0] || [];
        const n = Math.max(hist.length, hist0.length);
        const vals = Array.from({ length: n }, (_, k) => (hist[k] || 0) + (hist0[k] || 0));
        const ymax = Math.max(...vals), ticks = [];
        const stepT = ymax > 4000 ? 1000 : ymax > 400 ? 100 : 50;
        for (let v = 0; v <= ymax + stepT - 1; v += stepT) ticks.push(v);
        const fr = frame("התפלגות מספר הצעדים", n, ticks[ticks.length - 1], ticks, (v) => num(v));
        let s = fr.s;
        vals.forEach((v, k) => {
          const bw = Math.max(fr.slot * 0.6, 1), cls = k === c.length ? "by-enum" : "by-multiples";
          s += `<rect class="bar ${cls}" x="${f(fr.cx(k + 1) - bw / 2)}" y="${f(fr.Y(v))}" width="${f(bw)}" height="${f(BASE - fr.Y(v))}"><title>${k} צעדים: ${num(v)} מספרים (${num(hist[k] || 0)} מגיעים ל-${FIXED}, ${num(hist0[k] || 0)} ל-0)</title></rect>` +
               `<text class="tick" x="${f(fr.cx(k + 1))}" y="${f(fr.Y(v) - 4)}" text-anchor="middle" font-size="10">${num(v)}</text>` + fr.xtick(k + 1, k);
        });
        $(".kp-chart").innerHTML = s + fr.close();
        const toFixed = H.ends[FIXED] || 0, toZero = H.ends[0] || 0, longest = hist.length - 1;
        $(".kp-sum").innerHTML = `מתוך ${ltr(num(MAX + 1))} המספרים, ${ltr(num(toFixed))} מגיעים ל-${ltr(FIXED)} (אחרי ${ltr(longest)} צעדים לכל היותר) ו-${ltr(num(toZero))} מגיעים ל-0: אלה המספרים שכל הספרות שלהם שוות${d === 3 ? "" : ""}. ` +
          `רק ${ltr(`0 ו-${FIXED}`)} מיוחדים, כלומר נעצרים ב-0 צעדים.`;
        if (window.dvqDecorate) window.dvqDecorate($(".kp-chart"));
      };
      const set = (x) => { if (Number.isInteger(x) && x >= 0 && x <= MAX) st.x = x; draw(); };
      input.addEventListener("change", () => set(Math.round(Number(input.value))));
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      $(".ex-random").addEventListener("click", () => set(Math.floor(Math.random() * (MAX + 1))));
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => set(Number(b.dataset.x))));
      draw();
    },
  });

  // The Eurovision box (0008): a slider over the public announcements from Israel's own
  // to the last; the cups of the countries still to come (room under Israel's total)
  // against the points left, the moment of certain loss marked; a "what if" box for
  // Israel's own jury and public scores.
  const euroView = () => ({
    mount(box) {
      const st = { k: 0, jury: 123, pub: 220 };
      const num = (v) => Number(v).toLocaleString("en-US");
      box.innerHTML =
        `<div class="ex-controls"><label><span>הכרזות הקהל אחרי ישראל</span><input type="range" class="ex-k" min="0" max="7" step="1" value="0" dir="ltr"><output class="out-k"></output></label>` +
        `<button type="button" class="md-button ex-prev">הקודמת</button><button type="button" class="md-button md-button--primary ex-next">ההכרזה הבאה</button></div>` +
        `<div class="ex-controls eu-what"><span>מה אם לישראל היו</span><label>שופטים <input type="number" class="ex-jury" min="0" max="420" step="1" dir="ltr" aria-label="ניקוד השופטים של ישראל"></label>` +
        `<label>קהל <input type="number" class="ex-pub" min="0" max="432" step="1" dir="ltr" aria-label="ניקוד הקהל של ישראל"></label>` +
        `<button type="button" class="md-button ex-reset">הנתונים האמיתיים</button></div>` +
        `<div class="eu-chart"></div><p class="eu-step" aria-live="polite"></p><p class="ex-summary eu-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const slider = $(".ex-k");
      const draw = () => {
        const sc = euroScan(euroWithIsrael(st.jury, st.pub));
        const n = sc.rows.length - 1;
        slider.max = n; st.k = Math.min(st.k, n); slider.value = st.k;
        $(".out-k").textContent = `${st.k} / ${n}`;
        $(".ex-jury").value = st.jury; $(".ex-pub").value = st.pub;
        const row = sc.rows[st.k];
        // the cups: every country above Israel by the jury, announced or not
        const W = 640, H = 300, X0 = 48, BASE = 240, TOP = 20;
        const ymax = Math.max(sc.total, ...sc.above.map((r) => r[1] + r[2]), 1) * 1.08;
        const Y = (v) => BASE - (v / ymax) * (BASE - TOP);
        const slot = (W - X0 - 12) / Math.max(sc.above.length, 1), bw = slot * 0.6;
        let s = `<svg class="perf-chart eu-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="הכוסות של המדינות שמעל ישראל אחרי ${st.k} הכרזות">`;
        [0, 100, 200, 300, 400, 500].filter((v) => v < ymax).forEach((v) => {
          s += `<line class="grid" x1="${X0}" x2="${W - 12}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        });
        s += `<line class="s2-line" x1="${X0}" x2="${W - 12}" y1="${f(Y(sc.total))}" y2="${f(Y(sc.total))}" stroke-width="2" stroke-dasharray="6 4"/>` +
             `<text class="legend" x="${X0 + 4}" y="${f(Y(sc.total) - 6)}">Israel ${sc.total}</text>`;
        sc.above.forEach(([country, jury, pub], i) => {
          const x = X0 + i * slot + (slot - bw) / 2, announced = i < st.k, cx = x + bw / 2;
          s += `<rect class="bar by-multiples" x="${f(x)}" y="${f(Y(jury))}" width="${f(bw)}" height="${f(BASE - Y(jury))}"><title>${country}: שופטים ${jury}</title></rect>`;
          if (announced) {
            s += `<rect class="bar ${jury + pub > sc.total ? "by-enum" : "by-bfs"}" x="${f(x)}" y="${f(Y(jury + pub))}" width="${f(bw)}" height="${f(Y(jury) - Y(jury + pub))}"><title>${country}: קהל ${pub}, סך הכול ${jury + pub}</title></rect>`;
          } else if (jury < sc.total) {
            s += `<rect class="cup-room" x="${f(x)}" y="${f(Y(sc.total))}" width="${f(bw)}" height="${f(Y(jury) - Y(sc.total))}"><title>${country}: מקום פנוי ${sc.total - jury}</title></rect>`;
          }
          s += `<text class="tick" x="${f(cx)}" y="${BASE + 16}" text-anchor="middle" font-size="10">${country.length > 9 ? country.slice(0, 8) + "…" : country}</text>` +
               `<text class="tick" x="${f(cx)}" y="${BASE + 30}" text-anchor="middle" font-size="10">${announced ? jury + pub : jury}</text>`;
        });
        s += `<line class="axis" x1="${X0}" x2="${W - 12}" y1="${BASE}" y2="${BASE}"/></svg>`;
        $(".eu-chart").innerHTML = s;
        const left = row.left, room = row.room;
        let step = st.k === 0
          ? `מיד אחרי ההכרזה של ישראל (${ltr(`${sc.rows[0].jury} + ${sc.rows[0].pub} = ${sc.total}`)}): `
          : `אחרי ההכרזה של ${ltr(row.country)} (${ltr(`${row.jury} + ${row.pub} = ${row.total}`)}): `;
        step += `נותרו ${ltr(num(left))} נקודות קהל, והמקום הפנוי עד ${ltr(sc.total)} ב${n - st.k === 1 ? "כוס האחרונה" : `-${ltr(n - st.k)} הכוסות שנותרו`} הוא ${ltr(num(room))}. `;
        if (row.total > sc.total && st.k > 0) step += `<span class="eu-bad">✗ ${ltr(row.country)} עברה את ישראל, ההפסד ודאי.</span>`;
        else if (left > room) step += `<span class="eu-bad">✗ יותר מים מנפח (${ltr(`${num(left)} > ${num(room)}`)}): מישהי חייבת לעבור את ישראל.</span>`;
        else step += `<span class="eu-ok">✓ הכול עוד נכנס (${ltr(`${num(left)} ≤ ${num(room)}`)}): ישראל עדיין יכולה לנצח.</span>`;
        $(".eu-step").innerHTML = step;
        const real = st.jury === 123 && st.pub === 220;
        $(".eu-sum").innerHTML = (sc.won
          ? `עם ${ltr(`${st.jury} + ${st.pub} = ${sc.total}`)} אף מדינה לא עוברת את ישראל: היא מנצחת.`
          : sc.first === 0
            ? `עם ${ltr(`${st.jury} + ${st.pub} = ${sc.total}`)} ההפסד ודאי כבר ברגע ההכרזה של ישראל.`
            : `ההפסד ודאי אחרי ההכרזה ה-${ltr(sc.first)} שאחרי ישראל, של ${ltr(sc.rows[sc.first].country)}, כשנותרו ${ltr(n - sc.first)} הכרזות.`) +
          (real ? "" : ` (במציאות: 123 + 220 = 343, וההפסד ודאי אחרי צרפת, ההכרזה הרביעית.)`) +
          ` סדר ההכרזות נקבע לפי ניקוד השופטים${real ? "" : ", ולכן שינוי בניקוד השופטים של ישראל מזיז גם את מקומה בתור"}.`;
      };
      slider.addEventListener("input", () => { st.k = Number(slider.value); draw(); });
      $(".ex-next").addEventListener("click", () => { st.k = Math.min(st.k + 1, Number(slider.max)); draw(); });
      $(".ex-prev").addEventListener("click", () => { st.k = Math.max(st.k - 1, 0); draw(); });
      ["jury", "pub"].forEach((k) => $(`.ex-${k}`).addEventListener("change", () => {
        const v = Math.round(Number($(`.ex-${k}`).value));
        if (v >= 0 && v <= (k === "jury" ? 420 : 432)) { st[k] = v; st.k = 0; }
        draw();
      }));
      $(".ex-reset").addEventListener("click", () => { st.jury = 123; st.pub = 220; st.k = 0; draw(); });
      draw();
    },
  });

  // The three boxes box (0004): every game hides one of the two possible contents behind
  // the labels; tap a box to draw a ball, the deduction appears line by line, and a draw
  // from a box labelled with a colour shows why one ball is not enough.
  const boxes3View = () => ({
    mount(box) {
      const HE = { RED: "אדום", BLACK: "שחור", MIXED: "אדום ושחור" };
      const st = { labels: ["RED", "BLACK", "MIXED"], content: null, draws: [], games: 0, solvedFirst: 0 };
      const newGame = (keepStats = true) => {
        const cases = boxesCases().filter((c) => c.labels.join() === st.labels.join());
        st.content = cases[Math.floor(Math.random() * cases.length)].content;
        st.draws = [];
        if (!keepStats) { st.games = 0; st.solvedFirst = 0; }
      };
      newGame(false);
      box.innerHTML =
        `<div class="ex-controls"><button type="button" class="md-button md-button--primary ex-new">משחק חדש</button>` +
        `<button type="button" class="md-button ex-shuffle">ערבוב התוויות</button>` +
        `<button type="button" class="md-button ex-reveal">גילוי התוכן</button><span class="b3-stats"></span></div>` +
        `<div class="b3-crates" role="group" aria-label="שלוש קופסאות, לחיצה דוגמת כדור"></div>` +
        `<p class="b3-step" aria-live="polite"></p><ol class="b3-lines"></ol><p class="ex-summary b3-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const crate = (i, label, balls, open) => {
        const x = 20 + 200 * i, cx = x + 75;
        // the accessible name repeats the visible texts in order (axe: label-content-name-mismatch)
        const visible = [label === "MIXED" ? "אדום ושחור" : HE[label], open ? "" : "?", `קופסה ${i}${open ? `: ${HE[st.content[i]]}` : ""}`].filter(Boolean).join(" ");
        let s = `<g class="b3-crate" data-i="${i}" tabindex="0" role="button" aria-label="${visible}, דגימת כדור מהקופסה">` +
          `<polygon class="crate-top" points="${x},50 ${x + 30},20 ${x + 180},20 ${x + 150},50"/>` +
          `<polygon class="crate-side" points="${x + 150},50 ${x + 180},20 ${x + 180},120 ${x + 150},150"/>` +
          `<rect class="crate-front" x="${x}" y="50" width="150" height="100"/>`;
        s += `<text class="crate-text" x="${cx}" y="108" font-size="${label === "MIXED" ? 18 : 22}">${label === "MIXED" ? "אדום ושחור" : HE[label]}</text>`;
        s += `<text class="crate-text" x="${cx + 30}" y="42" font-size="20">${open ? "" : "?"}</text>`;
        balls.forEach((b, k) => { s += `<circle class="b3-ball b3-${b.toLowerCase()}" cx="${x + 18 + 22 * k}" cy="166" r="8"><title>כדור ${HE[b]}</title></circle>`; });
        s += `<text class="tick" x="${cx}" y="192" font-size="13" direction="rtl" text-anchor="middle">קופסה ${i}${open ? `: ${HE[st.content[i]]}` : ""}</text></g>`;
        return s;
      };
      const draw = (reveal = false) => {
        const balls = [[], [], []];
        st.draws.forEach((d) => balls[d.i].push(d.ball));
        $(".b3-crates").innerHTML = `<svg class="figure b3-live" viewBox="0 0 620 200">` +
          st.labels.map((l, i) => crate(i, l, balls[i], reveal)).join("") + `</svg>`;
        $(".b3-stats").textContent = st.games ? `${st.games} משחקים, ${st.solvedFirst} נפתרו בדגימה הראשונה` : "";
        const lines = [];
        let sum = "";
        if (!st.draws.length) {
          $(".b3-step").innerHTML = `כל התוויות שגויות. בחרו קופסה ודגמו ממנה כדור.`;
        } else {
          const first = st.draws[0];
          const k = st.labels.indexOf("MIXED");
          const left = boxesDeduce(st.labels, first.i, first.ball);
          if (first.i === k) {
            const fixed = boxesFix(st.labels, first.ball);
            const other = first.ball === "RED" ? "BLACK" : "RED";
            lines.push(`הקופסה "אדום ושחור" לא מעורבת (התווית שגויה), ויצא ממנה ${HE[first.ball]}: יש בה רק ${HE[first.ball]}.`);
            lines.push(`הקופסה שתוויתה "${HE[first.ball]}" לא מכילה ${HE[first.ball]} (תווית שגויה) ולא את התערובת (היא בקופסה ${ltr(k)}): נשאר ${HE[other]}.`);
            lines.push(`הקופסה שתוויתה "${HE[other]}" מקבלת את מה שנשאר: אדום ושחור.`);
            $(".b3-step").innerHTML = `<span class="b3-ok">✓ דגימה אחת הספיקה.</span> התוויות הנכונות: ${fixed.map((c, i) => `קופסה ${ltr(i)} = ${HE[c]}`).join(", ")}.`;
            sum = `הדגימה מהקופסה "אדום ושחור" מכריעה תמיד, כי שני הסידורים האפשריים נבדלים בה בצבע אחד וברור.`;
          } else {
            const otherOfLabel = st.labels[first.i] === "RED" ? "BLACK" : "RED";
            lines.push(`הקופסה "${HE[st.labels[first.i]]}" לא מכילה ${HE[st.labels[first.i]]}, ולכן היא או ${HE[otherOfLabel]} או אדום ושחור.`);
            lines.push(left.length === 2
              ? `כדור ${HE[first.ball]} מתאים לשתי האפשרויות: שני הסידורים עדיין פתוחים.`
              : `כדור ${HE[first.ball]} לא יכול לצאת מקופסה של ${HE[otherOfLabel]} בלבד: הקופסה מעורבת, ונשאר סידור אחד.`);
            if (left.length === 2) {
              $(".b3-step").innerHTML = `<span class="b3-bad">✗ דגימה מקופסה "${HE[st.labels[first.i]]}" לא מכריעה.</span> ` +
                (st.draws.length > 1 ? `דגימות נוספות: ${st.draws.slice(1).map((d) => `קופסה ${ltr(d.i)} ${HE[d.ball]}`).join(", ")}.` : `דגמו שוב, מאותה קופסה או מאחרת.`);
              const rest = boxesDeduce(st.labels, first.i, first.ball).filter((content) => st.draws.every((d) => content[d.i] === d.ball || content[d.i] === "MIXED"));
              if (rest.length === 1) $(".b3-step").innerHTML += ` <span class="b3-ok">✓ אחרי ${ltr(st.draws.length)} דגימות נשאר סידור אחד: ${rest[0].map((c, i) => `קופסה ${ltr(i)} = ${HE[c]}`).join(", ")}.</span>`;
              else $(".b3-step").innerHTML += ` עדיין ${ltr(rest.length)} סידורים אפשריים.`;
            } else {
              $(".b3-step").innerHTML = `<span class="b3-ok">✓ הפעם התמזל: כדור ${HE[first.ball]} מקופסה "${HE[st.labels[first.i]]}" פוסל סידור אחד.</span> הסידור שנשאר: ${left[0].map((c, i) => `קופסה ${ltr(i)} = ${HE[c]}`).join(", ")}. אבל זה מזל, לא הבטחה: הצבע השני היה משאיר שני סידורים.`;
            }
            sum = `דגימה מקופסה שתוויתה צבע מבטיחה הכרעה רק אם יוצא הצבע שעל התווית; הצבע השני משאיר ספק. רק הקופסה "אדום ושחור" מבטיחה הכרעה בכדור אחד.`;
          }
        }
        $(".b3-lines").innerHTML = lines.map((l) => `<li>${l}</li>`).join("");
        $(".b3-sum").innerHTML = sum;
      };
      const drawFrom = (i) => {
        const ball = boxesDraw(st.content, i);
        if (!st.draws.length) { st.games++; if (i === st.labels.indexOf("MIXED")) st.solvedFirst++; }
        st.draws.push({ i, ball });
        draw();
      };
      $(".b3-crates").addEventListener("click", (e) => { const g = e.target.closest(".b3-crate"); if (g) drawFrom(Number(g.dataset.i)); });
      $(".b3-crates").addEventListener("keydown", (e) => { const g = e.target.closest(".b3-crate"); if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); drawFrom(Number(g.dataset.i)); } });
      $(".ex-new").addEventListener("click", () => { newGame(); draw(); });
      $(".ex-shuffle").addEventListener("click", () => { st.labels = st.labels.slice().sort(() => Math.random() - 0.5); newGame(); draw(); });
      $(".ex-reveal").addEventListener("click", () => draw(true));
      draw();
    },
  });

  // The polygon box (0007, part b): the triangle box generalised to n vertices, n from
  // the slider; the same colours, arcs and inputs, a random draw, and a counter of random
  // polygons that contain the centre against 1 - n / 2^(n-1).
  const polygonView = () => ({
    mount(box) {
      const C = 160, R = 104, R_ARC = 116, R_LBL = 137, NMAX = Number(box.dataset.nmax || 10);
      const KIND = { in: "המצולע מכיל את המרכז", edge: "המרכז על צלע", out: "המצולע לא מכיל את המרכז", degenerate: "אין מצולע" };
      const num = (v) => Number(v).toLocaleString("en-US");
      const rad = (d) => (d * Math.PI) / 180;
      const at = (d, r) => [C + r * Math.cos(rad(d)), C - r * Math.sin(rad(d))];
      const st = { n: Math.min(NMAX, Math.max(3, Number(box.dataset.n || 5))), angles: [], runs: 0, hits: 0 };
      const regular = (n) => Array.from({ length: n }, (_, i) => Math.round((20 + (360 * i) / n) % 360));
      st.angles = regular(st.n);
      box.innerHTML =
        `<div class="ex-controls"><label><span>מספר הקודקודים n</span><input type="range" class="ex-n" min="3" max="${NMAX}" step="1" value="${st.n}" dir="ltr"><output class="out-n"></output></label>` +
        `<button type="button" class="md-button md-button--primary ex-random">הגרלה</button>` +
        `<button type="button" class="md-button ex-regular">מצולע משוכלל</button></div>` +
        `<div class="tri-box"><svg class="figure tri-live" viewBox="0 0 320 320" role="img" aria-label="קודקודים על מעגל היחידה">` +
        `<circle class="axis-c" cx="${C}" cy="${C}" r="${R}" fill="none"/><g class="tri-arcs"></g><polygon class="tri-shape"/>` +
        `<circle class="center-dot" cx="${C}" cy="${C}" r="4"/><text class="tick" x="${C + 7}" y="${C + 15}">O</text><g class="poly-pts"></g></svg>` +
        `<div class="tri-panel"><p class="tri-angles"></p><p class="tri-status" aria-live="polite"></p><p class="tri-arcs-text"></p></div></div>` +
        `<div class="ex-controls tri-run"><button type="button" class="md-button ex-rounds">1,000 הגרלות</button>` +
        `<button type="button" class="md-button ex-rounds-reset">איפוס המונה</button></div>` +
        `<p class="ex-summary tri-compare"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const svg = $("svg"), shape = $(".tri-shape"), arcsG = $(".tri-arcs"), ptsG = $(".poly-pts");
      let running = false;
      const arcPath = (from, len) => {
        const [x0, y0] = at(from, R_ARC), [x1, y1] = at(from + len, R_ARC);
        return `M${f(x0)},${f(y0)} A${R_ARC},${R_ARC} 0 ${len > 180 ? 1 : 0} 0 ${f(x1)},${f(y1)}`;
      };
      const render = () => {
        const n = st.n, angles = st.angles;
        $(".out-n").textContent = String(n);
        const kind = polyClass(angles);
        const order = angles.map((_, i) => i).sort((i, j) => angles[i] - angles[j] || i - j);
        const arcs = polyArcs(angles), top = Math.max(...arcs);
        svg.setAttribute("class", `figure tri-live is-${kind}`);
        shape.setAttribute("points", order.map((i) => at(angles[i], R).map((v) => f(v)).join(",")).join(" "));
        let g = "";
        arcs.forEach((len, k) => {
          if (len <= 0 || len >= 360) return;
          const from = angles[order[k]], [lx, ly] = at(from + len / 2, R_LBL), max = len === top;
          g += `<path class="tri-arc${max ? " is-max" : ""}" d="${arcPath(from, len)}" fill="none"/>` +
               (n <= 8 || max ? `<text class="legend${max ? " tri-max-label" : ""}" x="${f(lx)}" y="${f(ly + 5)}" text-anchor="middle" font-size="${n > 6 ? 10 : 12}">${len}°</text>` : "");
        });
        arcsG.innerHTML = g;
        ptsG.innerHTML = angles.map((d, i) => {
          const [x, y] = at(d, R), [nx, ny] = at(d, R - 22);
          return `<circle class="tri-pt" data-i="${i}" cx="${f(x)}" cy="${f(y)}" r="${n > 7 ? 7 : 9}"><title>P${i + 1}</title></circle>` +
                 `<text class="legend tri-name" x="${f(nx)}" y="${f(ny + 4)}" text-anchor="middle" font-size="${n > 6 ? 10 : 12}">P${i + 1}</text>`;
        }).join("");
        // the inputs follow n
        const panel = $(".tri-angles");
        if (panel.children.length !== n) {
          panel.innerHTML = angles.map((_, i) => `<label>${ltr(`P${i + 1}`)} <input type="number" class="ex-deg" data-i="${i}" min="0" max="359" step="1" dir="ltr" aria-label="הזווית של P${i + 1} במעלות">°</label>`).join(" ");
          panel.querySelectorAll(".ex-deg").forEach((inp, i) => {
            inp.addEventListener("change", () => {
              const v = Number(inp.value);
              if (inp.value.trim() !== "" && Number.isFinite(v)) { const next = [...st.angles]; next[i] = ((Math.round(v) % 360) + 360) % 360; st.angles = next; }
              render();
            });
            inp.addEventListener("keydown", (e) => { if (e.key === "Enter") inp.blur(); });
          });
        }
        panel.querySelectorAll(".ex-deg").forEach((inp, i) => { if (document.activeElement !== inp) inp.value = angles[i]; });
        svg.setAttribute("aria-label", `${n} קודקודים על מעגל היחידה בזוויות ${angles.join(", ")} מעלות: ${KIND[kind]}`);
        const why = {
          in: `כל ${ltr(n)} הקשתות קטנות מ-180°, הגדולה היא ${ltr(top + "°")}.`,
          edge: `יש קשת של בדיוק 180°, והצלע שמולה היא קוטר שעובר דרך המרכז.`,
          out: `יש קשת של ${ltr(top + "°")}, יותר מ-180°: כל הקודקודים בחצי מעגל אחד.`,
          degenerate: `שני קודקודים או יותר באותה זווית.`,
        }[kind];
        const mark = { in: "✓", edge: "●", out: "✗", degenerate: "●" }[kind];
        $(".tri-status").innerHTML = `<span class="tri-kind is-${kind}">${mark} ${KIND[kind]}.</span> ${why}`;
        $(".tri-arcs-text").innerHTML = kind === "degenerate" ? "" : `הקשתות לפי הסדר על המעגל: ${ltr(arcs.map((v) => `${v}°`).join(", "))}.`;
        const p = polyProb(n);
        $(".tri-compare").innerHTML = `הנוסחה של סעיף ג לזוויות רציפות: ${ltr(`1 − ${n}/2^${n - 1} = ${fmt(p, 4)}`)}. ` +
          (st.runs ? `מתוך ${ltr(num(st.runs))} מצולעים אקראיים (זוויות שלמות שונות), ${ltr(num(st.hits))} הכילו את המרכז: ${ltr(fmt(st.hits / st.runs, 4))}.` : `לחצו "1,000 הגרלות" כדי להשוות.`);
      };
      const setN = (n) => { st.n = n; st.angles = regular(n); st.runs = st.hits = 0; render(); };
      $(".ex-n").addEventListener("input", () => setN(Number($(".ex-n").value)));
      $(".ex-random").addEventListener("click", () => { st.angles = polyRandom(st.n); render(); });
      $(".ex-regular").addEventListener("click", () => { st.angles = regular(st.n); render(); });
      $(".ex-rounds").addEventListener("click", () => {
        for (let r = 0; r < 1000; r++) if (polyClass(polyRandom(st.n)) === "in") st.hits++;
        st.runs += 1000; render();
      });
      $(".ex-rounds-reset").addEventListener("click", () => { st.runs = st.hits = 0; render(); });
      // drag: the vertex nearest to the finger follows it around the circle
      let drag = null;
      const degAt = (e) => {
        const r = svg.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width) * 320 - C, y = C - ((e.clientY - r.top) / r.height) * 320;
        return ((Math.round((Math.atan2(y, x) * 180) / Math.PI) % 360) + 360) % 360;
      };
      svg.addEventListener("pointerdown", (e) => {
        const d = degAt(e);
        const dist = (i) => { const u = Math.abs(st.angles[i] - d); return Math.min(u, 360 - u); };
        const target = e.target.closest(".tri-pt");
        drag = target ? Number(target.dataset.i) : st.angles.reduce((b, _, i) => (dist(i) < dist(b) ? i : b), 0);
        svg.setPointerCapture(e.pointerId);
        svg.classList.add("is-dragging");
        const next = [...st.angles]; next[drag] = d; st.angles = next; render();
        e.preventDefault();
      });
      svg.addEventListener("pointermove", (e) => {
        if (drag === null) return;
        const d = degAt(e);
        if (d === st.angles[drag]) return;
        const next = [...st.angles]; next[drag] = d; st.angles = next; render();
      });
      const end = () => { drag = null; svg.classList.remove("is-dragging"); };
      svg.addEventListener("pointerup", end);
      svg.addEventListener("pointercancel", end);
      void running;
      render();
    },
  });

  // A timing strip: rows over N slots (clock cycles, or half-cycles with `half`), the
  // names in a left column. Row kinds: "clock" (the square wave), "bit" (a level line,
  // shaded where high), "bus" (labelled boxes merged over equal values). A row's values
  // may stop early (frames not reached yet). `cells` on a row makes every slot a button
  // (data-k); `marks` on a row shades slots; `cursor` outlines one slot.
  const waveStrip = (rows, N, opts = {}) => {
    const L = opts.labelW ?? 66, SW = opts.slotW ?? 36, RH = 30, T = opts.ticks ? 20 : 8;
    const W = L + N * SW + 6, H = T + rows.length * RH + 4;
    const x = (k) => L + k * SW;
    let s = `<svg class="wave-strip" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="${opts.role || "img"}" aria-label="${opts.label || ""}">`;
    for (let k = 0; k <= N; k++) s += `<line class="wv-grid${opts.half && k % 2 ? " wv-grid-half" : ""}" x1="${x(k)}" x2="${x(k)}" y1="${T - 4}" y2="${H - 4}"/>`;
    if (opts.ticks) for (let k = 0; k < N; k++) {
      const t = opts.ticks(k);
      if (t !== "" && t !== undefined && t !== null) s += `<text class="wv-tick" x="${x(k) + SW / 2}" y="${T - 8}" text-anchor="middle">${t}</text>`;
    }
    if (opts.cursor !== undefined && opts.cursor !== null) s += `<rect class="wv-cursor" x="${x(opts.cursor)}" y="${T - 4}" width="${SW}" height="${H - T}"/>`;
    rows.forEach((row, r) => {
      const y0 = T + r * RH, yh = y0 + 5, yl = y0 + RH - 7, ym = (yh + yl) / 2;
      const cls = row.cls ? ` ${row.cls}` : "";
      s += `<text class="wv-name" x="${L - 8}" y="${ym + 4}" text-anchor="end">${row.name}</text>`;
      let len = N;
      if (row.values) { len = row.values.findIndex((v) => v === undefined || v === null); if (len < 0) len = Math.min(N, row.values.length); }
      if (row.marks) row.marks.forEach((m, k) => { if (m && k < len) s += `<rect class="wv-mark" x="${x(k)}" y="${y0 + 2}" width="${SW}" height="${RH - 4}"/>`; });
      if (row.kind === "clock") {
        let d = "";
        for (let k = 0; k < len; k++) {
          const xk = x(k);
          if (opts.half) { const hi = k % 2 === 0; d += `M${xk},${hi ? yl : yh} V${hi ? yh : yl} H${xk + SW} `; }
          else d += `M${xk},${yl} V${yh} H${xk + SW / 2} V${yl} H${xk + SW} `;
        }
        s += `<path class="wv-line wv-clock" d="${d}"/>`;
      } else if (row.kind === "bus") {
        let k = 0;
        while (k < len) {
          let j = k;
          while (j + 1 < len && row.values[j + 1] === row.values[k]) j++;
          const xk = x(k), w = (j - k + 1) * SW;
          s += `<path class="wv-bus${cls}" d="M${xk + 2},${ym} L${xk + 6},${yh} H${xk + w - 6} L${xk + w - 2},${ym} L${xk + w - 6},${yl} H${xk + 6} Z"/>` +
               `<text class="wv-val" x="${xk + w / 2}" y="${ym + 4}" text-anchor="middle">${row.values[k]}</text>`;
          k = j + 1;
        }
      } else {
        let d = "", prev = null;
        for (let k = 0; k < len; k++) {
          const v = row.values[k] ? 1 : 0, xk = x(k), y = v ? yh : yl;
          if (v) s += `<rect class="wv-high${cls}" x="${xk}" y="${yh}" width="${SW}" height="${yl - yh}"/>`;
          d += (k === 0 ? `M${xk},${y}` : prev !== v ? ` V${y}` : "") + ` H${xk + SW}`;
          prev = v;
        }
        if (len) s += `<path class="wv-line${cls}" d="${d}"/>`;
      }
      if (row.cells) for (let k = 0; k < N; k++) {
        s += `<rect class="wv-cell" data-k="${k}" x="${x(k)}" y="${y0 + 1}" width="${SW}" height="${RH - 2}" tabindex="0" role="button" aria-label="${row.cells(k)}"/>`;
      }
    });
    return s + "</svg>";
  };
  const code = (t) => `<code>${t}</code>`;

  // The edge detector box (0001): tap the cells of sig to draw it cycle by cycle (cycle 0
  // is the reset cycle); sig_q and pulse follow the page's circuit, for a rising edge, a
  // falling edge or both; the reset trap as a toggle; the page's own diagram as a preset.
  const edgeView = () => ({
    mount(box) {
      const N = 12;
      const PAGE = [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0];
      const FORMULA = { rise: "sig &amp; ~sig_q", fall: "~sig &amp; sig_q", both: "sig ^ sig_q" };
      const NAME = { rise: "עליית שפה", fall: "ירידת שפה", both: "שפה (עלייה או ירידה)" };
      const st = { sig: PAGE.slice(), mode: "rise", cur: 2 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>השפה שמזהים <select class="ex-mode" aria-label="איזו שפה מזהים"><option value="rise">עלייה</option><option value="fall">ירידה</option><option value="both">שתיהן</option></select></label>` +
        `<label><input type="checkbox" class="ex-hi"> <span>‏${code("sig")} כבר גבוה בזמן האיפוס</span></label>` +
        `<span class="wv-presets">דוגמאות: <button type="button" class="md-button ex-preset" data-p="page">הדיאגרמה שבעמוד</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="short">פולסים קצרים</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="random">אקראי</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="clear">ניקוי</button></span></div>` +
        `<p class="wv-hint">לחיצה על משבצת בשורה של ${code("sig")} הופכת את הערך שלה באותו מחזור. מחזור 0 הוא מחזור האיפוס.</p>` +
        `<div class="wv-wrap" tabindex="0" role="group" aria-label="דיאגרמת תזמון של גלאי השפה, גלילה אופקית"></div>` +
        `<p class="wv-step" aria-live="polite"></p><p class="ex-summary wv-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const draw = () => {
        const tr = edgeTrace(st.sig, st.mode);
        $(".ex-hi").checked = st.sig[0] === 1;
        const rows = [
          { name: "rst_n", kind: "bit", values: st.sig.map((_, i) => (i === 0 ? 0 : 1)), cls: "wv-dim" },
          { name: "clk", kind: "clock" },
          { name: "sig", kind: "bit", values: st.sig, cls: "wv-s1", cells: (k) => `מחזור ${k}: sig = ${st.sig[k]}, לחיצה הופכת` },
          { name: "sig_q", kind: "bit", values: tr.sigQ, cls: "wv-s3" },
          { name: "pulse", kind: "bit", values: tr.pulse, cls: "wv-s2" },
        ];
        $(".wv-wrap").innerHTML = waveStrip(rows, N, { role: "group", label: "דיאגרמת תזמון", cursor: st.cur, ticks: (k) => k });
        const k = st.cur, s = st.sig[k], q = tr.sigQ[k], p = tr.pulse[k];
        const out = ltr(`${code("pulse")} = ${code(FORMULA[st.mode])} = ${p}`);
        let step = k === 0
          ? `מחזור 0 הוא מחזור האיפוס: ${code("rst_n")} נמוך, ולכן ${ltr(`${code("sig_q")} = 0`)} בכוח. ${ltr(`${code("sig")} = ${s}`)} ⇒ ${out}.`
          : `מחזור ${ltr(k)}: ${ltr(`${code("sig")} = ${s}`)} עכשיו, ${ltr(`${code("sig_q")} = ${q}`)} (הערך של ${code("sig")} במחזור ${ltr(k - 1)}) ⇒ ${out}.`;
        if (k === 0 && p) step += ` <span class="wv-bad">פולס בלי שפה: ${code("sig")} היה גבוה כבר בזמן האיפוס, ו-${code("sig_q")} מתחיל מ-0. זו המלכודת מהערה 2 של הקוד.</span>`;
        else if (p) step += ` <span class="wv-ok">${NAME[st.mode]} בין מחזור ${ltr(k - 1)} למחזור ${ltr(k)}: הפולס גבוה במחזור הזה בלבד.</span>`;
        else if (k > 0 && s && q && st.mode === "rise") step += ` ${code("sig")} עדיין גבוה, אבל גם ${code("sig_q")} כבר 1: ה-AND מאפס את המוצא, ולכן הפולס לא מתארך.`;
        $(".wv-step").innerHTML = step;
        const high = tr.pulse.reduce((a, b) => a + b, 0), edges = tr.edges.reduce((a, b) => a + b, 0);
        let sum = `‏${code("pulse")} גבוה ב-${ltr(high)} מחזורים`;
        sum += edges === 1 ? `, ויש ${NAME[st.mode]} אחת` : `, ויש ${ltr(edges)} שפות מהסוג שנבחר`;
        if (tr.phantom) sum += ` ועוד פולס אחד בלי שפה במחזור האיפוס`;
        sum += high === edges + (tr.phantom ? 1 : 0) ? `: מחזור אחד בדיוק לכל שפה ✓` : ".";
        if (st.mode === "both" && tr.widths.some((w) => w > 1)) sum += ` שפות במחזורים עוקבים נותנות פולס רצוף: המוצא גבוה בכל מחזור שבו ${code("sig")} שונה מהמחזור הקודם.`;
        $(".wv-sum").innerHTML = sum;
      };
      const wrap = $(".wv-wrap");
      const tap = (k) => { st.sig[k] = st.sig[k] ? 0 : 1; st.cur = k; draw(); };
      wrap.addEventListener("click", (e) => { const c = e.target.closest(".wv-cell"); if (c) tap(Number(c.dataset.k)); });
      wrap.addEventListener("keydown", (e) => {
        const c = e.target.closest(".wv-cell");
        if (c && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); tap(Number(c.dataset.k)); }
      });
      $(".ex-mode").addEventListener("change", () => { st.mode = $(".ex-mode").value; draw(); });
      $(".ex-hi").addEventListener("change", () => { st.sig[0] = $(".ex-hi").checked ? 1 : 0; st.cur = 0; draw(); });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => {
        const p = b.dataset.p;
        if (p === "page") st.sig = PAGE.slice();
        else if (p === "short") st.sig = [0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1];
        else if (p === "random") st.sig = Array.from({ length: N }, () => (Math.random() < 0.5 ? 1 : 0));
        else st.sig = new Array(N).fill(0);
        st.cur = p === "clear" ? 1 : Math.max(1, st.sig.findIndex((v, i) => i > 0 && v !== st.sig[i - 1]));
        draw();
      }));
      draw();
    },
  });

  // The LFSR box (0036): tick the taps (x^4 and 1 are fixed), step or play from 0001 on a
  // ring of the 15 non-zero states (0000 sits in the middle as the fixed point), the
  // output bits so far, and the table of the eight polynomials with their periods.
  const lfsrView = () => ({
    mount(box) {
      const WIDTH = 4, SEED = 1;
      const st = { mask: 0b0011, k: 0 };
      const bits = (v) => bitsOf(v, WIDTH);
      const sup = (k) => (k === 1 ? "x" : `x<sup>${k}</sup>`);
      const polyHtml = (mask) => {
        const t = [`x<sup>${WIDTH}</sup>`];
        for (let k = WIDTH - 1; k >= 1; k--) if ((mask >> (WIDTH - k)) & 1) t.push(sup(k));
        return ltr(t.concat("1").join(" + "));
      };
      box.innerHTML =
        `<div class="ex-controls"><span class="lf-taps" dir="ltr" role="group" aria-label="בחירת ה-taps"><span class="lf-fixed">${ltr("x<sup>4</sup>")} +</span> ` +
        [3, 2, 1].map((k) => `<label><input type="checkbox" class="ex-tap" data-k="${k}"> <span>${ltr(sup(k))} +</span></label>`).join(" ") +
        `<span class="lf-fixed">1</span></span>` +
        `<span class="lf-presets">הפולינומים של השאלה: <button type="button" class="md-button ex-preset" data-mask="3">${ltr("x<sup>4</sup> + x<sup>3</sup> + 1")}</button> ` +
        `<button type="button" class="md-button ex-preset" data-mask="5">${ltr("x<sup>4</sup> + x<sup>2</sup> + 1")}</button></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">צעד</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1000">איטי</option><option value="500" selected>בינוני</option><option value="180">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד שהמצב חוזר</button><span class="ex-pos"></span></div>` +
        `<div class="lf-box"><div class="lf-ring"></div><div class="lf-panel">` +
        `<p class="lf-poly"></p><p class="lf-state"></p><p class="lf-fb"></p>` +
        `<p class="ex-title">הביטים שיצאו (${code("s[0]")} של כל מצב)</p><p class="lf-out" dir="ltr"></p>` +
        `<p class="ex-summary lf-sum" aria-live="polite"></p></div></div>` +
        `<p class="ex-title">כל שמונת הפולינומים ${ltr("x<sup>4</sup> + … + 1")} ואורך המחזור של כל אחד מ-${code("0001")}</p><div class="lf-table" tabindex="0"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let timer = null;
      const ring = () => {
        const R = 118, C = 150, rr = 17;
        const pos = (v) => { const ang = -Math.PI / 2 + ((v - 1) / 15) * 2 * Math.PI; return [C + R * Math.cos(ang), C + R * Math.sin(ang)]; };
        const walk = lfsrWalk(st.mask, WIDTH, SEED), shown = walk.states.concat(walk.states[walk.back]).slice(0, st.k + 1);
        const visited = new Set(shown), cur = shown[shown.length - 1];
        let s = `<svg class="lf-live" viewBox="0 0 300 300" role="img" aria-label="טבעת של 15 המצבים שאינם אפס, המצבים שבוקרו וחיצים ביניהם">` +
          `<defs><marker id="lf-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="lf-arrowhead"/></marker></defs>`;
        for (let i = 1; i < shown.length; i++) {
          const [x1, y1] = pos(shown[i - 1]), [x2, y2] = pos(shown[i]);
          const dx = x2 - x1, dy = y2 - y1, d = Math.hypot(dx, dy) || 1;
          s += `<line class="lf-edge${i === shown.length - 1 ? " is-cur" : ""}" x1="${f(x1 + (dx / d) * rr)}" y1="${f(y1 + (dy / d) * rr)}" x2="${f(x2 - (dx / d) * (rr + 2))}" y2="${f(y2 - (dy / d) * (rr + 2))}" marker-end="url(#lf-arrow)"/>`;
        }
        for (let v = 1; v < 16; v++) {
          const [x, y] = pos(v);
          s += `<g class="lf-node${visited.has(v) ? " is-seen" : ""}${v === cur ? " is-cur" : ""}${v === SEED ? " is-seed" : ""}"><circle cx="${f(x)}" cy="${f(y)}" r="${rr}"/><text x="${f(x)}" y="${f(y + 4)}" text-anchor="middle">${bits(v)}</text></g>`;
        }
        s += `<g class="lf-node lf-zero"><circle cx="${C}" cy="${C}" r="${rr}"/><text x="${C}" y="${C + 4}" text-anchor="middle">0000</text></g>` +
             `<path class="lf-loop" d="M${C + 12},${C - 13} a 11 11 0 1 1 -24 0" marker-end="url(#lf-arrow)"/></svg>`;
        return s;
      };
      const draw = () => {
        const walk = lfsrWalk(st.mask, WIDTH, SEED), total = walk.period;
        st.k = Math.min(st.k, total);
        box.querySelectorAll(".ex-tap").forEach((c) => { c.checked = ((st.mask >> (WIDTH - Number(c.dataset.k))) & 1) === 1; });
        $(".lf-ring").innerHTML = ring();
        const cur = st.k < total ? walk.states[st.k] : walk.states[walk.back];
        const tapsIdx = [];
        for (let i = 0; i < WIDTH; i++) if ((st.mask >> i) & 1) tapsIdx.push(i);
        let fb = 0; tapsIdx.forEach((i) => { fb ^= (cur >> i) & 1; });
        const next = lfsrNext(cur, st.mask, WIDTH);
        $(".ex-pos").textContent = `צעד ${st.k} מתוך ${total}`;
        $(".lf-poly").innerHTML = `הפולינום ${polyHtml(st.mask)}, המסכה ${code(bits(st.mask))}: היזון חוזר מהביטים ${ltr(tapsIdx.map((i) => `s[${i}]`).join(", "))}.`;
        $(".lf-state").innerHTML = `המצב אחרי ${ltr(st.k)} צעדים: ${code(bits(cur))}` + (st.k === total ? ` — חזר למצב ההתחלה.` : ".");
        $(".lf-fb").innerHTML = `הצעד הבא: ${ltr(`${code("fb")} = ${code(tapsIdx.map((i) => `s[${i}]`).join(" ^ "))} = ${tapsIdx.map((i) => (cur >> i) & 1).join(" ^ ")} = ${fb}`)}, ` +
          `ואז ${ltr(`${code(`(${bits(cur)} >> 1) | (${fb} << 3)`)} = ${code(bits(next))}`)}.`;
        $(".lf-out").innerHTML = walk.states.slice(0, Math.min(st.k, total - 1) + 1).map((v, i) => `<span class="${i === st.k ? "is-cur" : ""}">${v & 1}</span>`).join("");
        const maximal = total === 15;
        $(".lf-sum").innerHTML = st.k < total
          ? `בוקרו ${ltr(st.k + 1)} מצבים מתוך 15. ` + (maximal ? `הפולינום פרימיטיבי: המחזור יהיה 15.` : `המחזור של הפולינום הזה הוא ${ltr(total)}, ולכן ${ltr(15 - total)} מצבים לא יבוקרו לעולם.`)
          : maximal ? `<span class="lf-ok">מחזור מקסימלי: 15 צעדים, כל מצב שאינו אפס פעם אחת ✓</span>`
          : `<span class="lf-bad">מחזור של ${ltr(total)} צעדים בלבד: ${ltr(15 - total)} מצבים לא בוקרו.</span>`;
        $(".lf-table").innerHTML = `<table><thead><tr><th>הפולינום</th><th>המסכה</th><th>אורך המחזור</th></tr></thead><tbody>` +
          lfsrTable(WIDTH).map((r) => `<tr class="${r.mask === st.mask ? "is-cur" : ""}${r.period === 15 ? " is-max" : ""}"><td>${polyHtml(r.mask)}</td><td>${code(bits(r.mask))}</td><td>${ltr(r.period)}${r.period === 15 ? " ✓" : ""}</td></tr>`).join("") +
          `</tbody></table>`;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => lfsrWalk(st.mask, WIDTH, SEED).period;
      box.querySelectorAll(".ex-tap").forEach((c) => c.addEventListener("change", () => {
        const bit = 1 << (WIDTH - Number(c.dataset.k));
        st.mask = c.checked ? st.mask | bit : st.mask & ~bit;
        stop(); st.k = 0; draw();
      }));
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { stop(); st.mask = Number(b.dataset.mask); st.k = 0; draw(); }));
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= total()) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      draw();
    },
  });

  // The divide-by-three box (0035): the page's half-cycle model one clock edge at a time
  // or played; the strip of clk, cnt, a, b and clk_out with the overlap of a and b shaded;
  // the duty measured from the trace; a wake-up in state 3 with the counter as in the
  // module (2 bits, wraps), without a wrap (the Python model) or guarded (>= 2).
  const div3View = () => ({
    mount(box) {
      const TOTAL = 36;
      const st = { k: 0, cnt0: 0, counter: "wrap" };
      box.innerHTML =
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">השפה הבאה</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="900">איטי</option><option value="450" selected>בינוני</option><option value="150">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">איפוס</button>` +
        `<button type="button" class="md-button ex-wake">התעוררות במצב 3</button>` +
        `<label>המונה <select class="ex-counter" aria-label="גרסת המונה"><option value="wrap">2 ביטים, כמו במודול</option><option value="wide">רחב יותר, בלי גלגול</option><option value="guard">מגן: cnt &gt;= 2</option></select></label>` +
        `<span class="ex-pos"></span></div>` +
        `<div class="wv-wrap" tabindex="0" role="group" aria-label="דיאגרמת תזמון של המחלק בשלוש, גלילה אופקית"></div>` +
        `<p class="wv-step" aria-live="polite"></p><p class="ex-summary wv-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let timer = null;
      const draw = () => {
        const rows = div3Trace(TOTAL, st.cnt0, st.counter), shown = rows.slice(0, st.k);
        const val = (key) => shown.map((r) => r[key]);
        const strip = [
          { name: "clk", kind: "clock" },
          { name: "cnt", kind: "bus", values: val("cnt") },
          { name: "a", kind: "bit", values: val("a"), cls: "wv-s1" },
          { name: "b", kind: "bit", values: val("b"), cls: "wv-s3" },
          { name: "clk_out", kind: "bit", values: val("out"), cls: "wv-s2", marks: shown.map((r) => r.a && r.b) },
        ];
        $(".wv-wrap").innerHTML = waveStrip(strip, TOTAL, { half: true, label: "דיאגרמת תזמון בחצאי מחזורים", cursor: st.k ? st.k - 1 : null, ticks: (k) => (k % 2 === 0 ? k / 2 : "") });
        $(".ex-pos").textContent = `שפה ${st.k} מתוך ${TOTAL}`;
        let step;
        if (!st.k) step = st.cnt0 === 3
          ? `המונה התעורר במצב 3, שאינו נגיש אחרי איפוס: ${ltr(`${code("cnt")} = 3`)}, ${ltr(`${code("a")} = 0`)}, ${ltr(`${code("b")} = 0`)}.`
          : `אחרי איפוס: ${ltr(`${code("cnt")} = 0`)}, ${ltr(`${code("a")} = 0`)}, ${ltr(`${code("b")} = 0`)}, והמוצא נמוך.`;
        else {
          const r = rows[st.k - 1], cyc = Math.floor(r.edge / 2);
          if (r.rising) {
            step = `עליית השעון של מחזור ${ltr(cyc)}: ${ltr(`${code("a")} ← (${code("cnt")} == 2) = ${r.a}`)}, ו-${ltr(`${code("cnt")} ← ${r.cnt}`)}` +
              (r.cntPrev === 3 ? (st.counter === "wide" ? ` (‏${ltr("3 + 1 = 4")}: בלי גלגול המונה לא חוזר ל-0)` : st.counter === "guard" ? ` (‏${ltr("3 >= 2")}, ולכן חזרה ל-0)` : ` (‏${ltr("3 + 1")} ב-2 ביטים מתגלגל ל-0)`) : "") + ".";
            if (r.aChanged && r.a) step += ` <span class="wv-ok">‏${code("a")} עלה: המוצא עולה עם עליית השעון.</span>`;
            else if (r.aChanged && !r.a) step += r.b ? ` <span class="wv-ok">‏${code("a")} ירד, אבל ${code("b")} עדיין 1: ה-OR מחזיק את המוצא גבוה, בלי גליץ'.</span>` : ` ${code("a")} ירד ו-${code("b")} כבר 0: המוצא יורד.`;
          } else {
            step = `ירידת השעון באמצע מחזור ${ltr(cyc)}: ${ltr(`${code("b")} ← ${code("a")} = ${r.b}`)}.`;
            if (r.bChanged && r.b) step += ` ‏${code("b")} עלה כש-${code("a")} כבר 1: המוצא כבר גבוה, ואין שינוי בו.`;
            else if (r.bChanged && !r.b) step += ` <span class="wv-ok">‏${code("b")} ירד ו-${code("a")} כבר 0 מחצי מחזור: המוצא יורד בירידת השעון, אחרי 1.5 מחזורים גבוה.</span>`;
          }
        }
        $(".wv-step").innerHTML = step;
        const duty = div3Duty(shown);
        let sum;
        if (duty.period === null) {
          const stuck = st.counter === "wide" && st.cnt0 === 3;
          sum = stuck && st.k >= 6 ? `<span class="wv-bad">המונה ממשיך לספור 4, 5, 6… ולא חוזר ל-2: ${code("a")} לא עולה לעולם והמוצא תקוע נמוך. זה מה שמודל ה-Python של העמוד היה עושה ממצב 3.</span>`
            : `המוצא עוד לא השלים תקופה: ${code("a")} עולה רק אחרי שהמונה עובר 2 ← 0.`;
        } else {
          sum = `מהעלייה הראשונה: תקופה של ${ltr(duty.period)} חצאי מחזורים = ${ltr(duty.period / 2)} מחזורים, גבוה ${ltr(duty.high)} מתוכם: duty ${ltr(Math.round((100 * duty.high) / duty.period))}%` +
            (duty.period === 6 && duty.high === 3 && duty.ok ? ` ✓` : ".");
        }
        $(".wv-sum").innerHTML = sum;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, TOTAL); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; st.cnt0 = 0; draw(); });
      $(".ex-wake").addEventListener("click", () => { stop(); st.k = 0; st.cnt0 = 3; draw(); });
      $(".ex-counter").addEventListener("change", () => { stop(); st.counter = $(".ex-counter").value; st.k = 0; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= TOTAL) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= TOTAL) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      draw();
    },
  });

  // The Gray pointer box (0034). data-mode="sync": a step b -> b + 1 of a 4-bit pointer
  // seen through a synchroniser, every changing bit tapped as arrived or not (or drawn
  // at random), in binary and in Gray side by side. data-mode="flags": a 16-entry FIFO
  // with 5-bit pointers, write and read, the pointers in binary and Gray, empty and full
  // by the page's rules.
  const grayView = (box) => ({
    mount() {
      const BITS = 4;
      if (box.dataset.mode === "flags") { grayFlagsMount(box); return; }
      const st = { b: 7, arrBin: {}, arrGray: {} };
      box.innerHTML =
        `<div class="ex-controls"><label><span>המצביע לפני הצעד</span><input type="range" class="ex-b" min="0" max="15" step="1" value="7" dir="ltr" aria-label="המצביע לפני הצעד"><output class="ex-bout"></output></label>` +
        `<button type="button" class="md-button ex-random">הגרלה: אילו ביטים הגיעו</button>` +
        `<button type="button" class="md-button ex-all">הכול הגיע</button>` +
        `<button type="button" class="md-button ex-none">כלום עוד לא הגיע</button></div>` +
        `<p class="wv-hint">כל ביט שמשתנה בצעד עובר סנכרן משלו, ויכול להידגם ישן או חדש. לחיצה על ביט כזה בשורה "נדגם" הופכת אותו.</p>` +
        `<div class="gr-box"><div class="gr-side gr-bin"></div><div class="gr-side gr-gray"></div></div>` +
        `<p class="ex-summary gr-sum" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const side = (title, oldV, newV, changed, arrived, seen, kind) => {
        const bitsRow = (label, v, sampled) => `<div class="gr-row"><span class="gr-label">${label}</span><span class="gr-bits" dir="ltr">` +
          [...Array(BITS)].map((_, j) => {
            const i = BITS - 1 - j, ch = changed.includes(i), bit = (v >> i) & 1;
            if (sampled && ch) return `<button type="button" class="gr-bit gr-btn ${arrived[i] ? "is-new" : "is-old"}" data-kind="${kind}" data-i="${i}" aria-label="${bit}, ביט ${i}: ${arrived[i] ? "החדש הגיע" : "עדיין הישן"}, לחיצה הופכת">${bit}</button>`;
            return `<span class="gr-bit${ch && !sampled ? " is-changed" : ""}">${bit}</span>`;
          }).join("") + `</span><span class="gr-dec">${ltr(v)}</span></div>`;
        return `<p class="ex-title">${title}</p>` + bitsRow("ישן", oldV, false) + bitsRow("חדש", newV, false) + bitsRow("נדגם", seen, true);
      };
      const draw = () => {
        const r = graySample(st.b, BITS, st.arrBin, st.arrGray);
        $(".ex-b").value = st.b; $(".ex-bout").textContent = String(st.b);
        const bin = side(`בינארי: ${ltr(`${bitsOf(r.oldB, BITS)} → ${bitsOf(r.newB, BITS)}`)}, ${ltr(r.changedBin.length)} ביטים משתנים`, r.oldB, r.newB, r.changedBin, st.arrBin, r.seenBin, "bin");
        const gray = side(`‏Gray: ${ltr(`${bitsOf(r.oldG, BITS)} → ${bitsOf(r.newG, BITS)}`)}, ביט אחד משתנה`, r.oldG, r.newG, r.changedGray, st.arrGray, r.seenGray, "gray");
        const binV = r.binValid
          ? `<p class="gr-ok">הקורא רואה ${ltr(r.seenBin)}: ${r.seenBin === r.oldB ? "הערך הישן" : "הערך החדש"}, ערך שהמצביע באמת עבר בו ✓</p>`
          : `<p class="gr-bad">הקורא רואה ${ltr(r.seenBin)}: לא הישן ולא החדש. המצביע מעולם לא היה שם, והתפוסה שהקורא יחשב שגויה ב-${ltr(Math.abs(r.seenBin - r.oldB))} מילים ✗</p>`;
        const grayV = `<p class="gr-ok">הקורא רואה ${ltr(bitsOf(r.seenGray, BITS))}, כלומר ${ltr(r.seenGrayAsBin)}: ${r.seenGray === r.oldG ? "הערך הישן (במקרה הגרוע הוא מחכה מחזור נוסף)" : "הערך החדש"} ✓</p>`;
        $(".gr-bin").innerHTML = bin + binV;
        $(".gr-gray").innerHTML = gray + grayV;
        const k = r.changedBin.length;
        $(".gr-sum").innerHTML = `בצעד ${ltr(`${r.oldB} → ${r.newB}`)} משתנים ${ltr(k)} ביטים בבינארי: ${ltr(`2^${k} = ${1 << k}`)} צירופים של ישן/חדש, ${ltr(r.wrongCount)} מהם ערכים שגויים. ב-Gray משתנה ביט אחד: שני צירופים, שניהם ערכים שהמצביע עבר בהם.`;
      };
      const randomize = () => {
        const r = graySample(st.b, BITS, {}, {});
        st.arrBin = {}; st.arrGray = {};
        r.changedBin.forEach((i) => { st.arrBin[i] = Math.random() < 0.5 ? 1 : 0; });
        r.changedGray.forEach((i) => { st.arrGray[i] = Math.random() < 0.5 ? 1 : 0; });
      };
      const setAll = (v) => { for (let i = 0; i < BITS; i++) { st.arrBin[i] = v; st.arrGray[i] = v; } };
      $(".ex-b").addEventListener("input", () => { st.b = Number($(".ex-b").value); draw(); });
      $(".ex-random").addEventListener("click", () => { randomize(); draw(); });
      $(".ex-all").addEventListener("click", () => { setAll(1); draw(); });
      $(".ex-none").addEventListener("click", () => { setAll(0); draw(); });
      box.addEventListener("click", (e) => {
        const b = e.target.closest(".gr-btn");
        if (!b) return;
        const map = b.dataset.kind === "bin" ? st.arrBin : st.arrGray, i = Number(b.dataset.i);
        map[i] = map[i] ? 0 : 1;
        draw();
      });
      // the page's example: bits 3 and 0 arrived, 2 and 1 did not (1110); in Gray the old value
      st.arrBin = { 3: 1, 0: 1, 2: 0, 1: 0 }; st.arrGray = { 3: 0 };
      draw();
    },
  });
  const grayFlagsMount = (box) => {
    const BITS = 5, SIZE = 16;
    const st = { w: 0, r: 0 };
    box.innerHTML =
      `<div class="ex-controls">` +
      `<button type="button" class="md-button md-button--primary ex-write">כתיבה</button>` +
      `<button type="button" class="md-button md-button--primary ex-read">קריאה</button>` +
      `<button type="button" class="md-button ex-write8">8 כתיבות</button>` +
      `<button type="button" class="md-button ex-read8">8 קריאות</button>` +
      `<button type="button" class="md-button ex-start">איפוס</button></div>` +
      `<div class="gr-slots" dir="ltr" role="img" aria-label="16 הכניסות של ה-FIFO, המלאות מודגשות, עם מצביעי הכתיבה והקריאה"></div>` +
      `<div class="gr-ptrs"></div><p class="ex-summary gr-sum" aria-live="polite"></p>`;
    const $ = (sel) => box.querySelector(sel);
    const draw = () => {
      const fl = grayFlags(st.w, st.r, BITS);
      $(".ex-write").disabled = fl.full; $(".ex-write8").disabled = fl.full;
      $(".ex-read").disabled = fl.empty; $(".ex-read8").disabled = fl.empty;
      const wa = st.w & (SIZE - 1), ra = st.r & (SIZE - 1);
      let cells = "";
      for (let i = 0; i < SIZE; i++) {
        const filled = ((i - ra) & (SIZE - 1)) < fl.occupancy;
        cells += `<span class="gr-slot${filled ? " is-full" : ""}"><span class="gr-w">${i === wa ? "W" : ""}</span><span class="gr-idx">${i}</span><span class="gr-r">${i === ra ? "R" : ""}</span></span>`;
      }
      $(".gr-slots").innerHTML = cells;
      const split = (v, n) => { const s = bitsOf(v, BITS); return n === 1 ? `<span class="gr-top2">${s[0]}</span>${s.slice(1)}` : `<span class="gr-top">${s[0]}</span><span class="gr-top2">${s[1]}</span>${s.slice(2)}`; };
      $(".gr-ptrs").innerHTML = `<table><thead><tr><th>המצביע</th><th>בינארי</th><th>‏Gray</th><th>כתובת</th></tr></thead><tbody>` +
        `<tr><td>כתיבה ${code("wptr")}</td><td dir="ltr">${split(st.w, 1)}</td><td dir="ltr">${split(fl.wg, 2)}</td><td>${ltr(wa)}</td></tr>` +
        `<tr><td>קריאה ${code("rptr")}</td><td dir="ltr">${split(st.r, 1)}</td><td dir="ltr">${split(fl.rg, 2)}</td><td>${ltr(ra)}</td></tr></tbody></table>`;
      const wg = bitsOf(fl.wg, BITS), rg = bitsOf(fl.rg, BITS);
      const topFlip = wg.slice(0, 2) === rg.slice(0, 2).replace(/[01]/g, (c) => (c === "0" ? "1" : "0")), restEq = wg.slice(2) === rg.slice(2);
      let sum = `תפוסה ${ltr(fl.occupancy)} מתוך 16 (ההפרש בין המצביעים מודולו 32). `;
      sum += fl.empty ? `<span class="gr-ok">ריק ✓</span>: שני ה-Gray שווים (${ltr(wg)} = ${ltr(rg)}). `
        : `ריק? לא: ${ltr(wg)} ≠ ${ltr(rg)}. `;
      sum += fl.full ? `<span class="gr-ok">מלא ✓</span>: שני הביטים העליונים הפוכים (${ltr(wg.slice(0, 2))} מול ${ltr(rg.slice(0, 2))}) ושלושת הנמוכים שווים (${ltr(wg.slice(2))}).`
        : `מלא? לא: ` + (topFlip ? `העליונים הפוכים, אבל הנמוכים ${ltr(wg.slice(2))} מול ${ltr(rg.slice(2))}.` : `העליונים ${ltr(wg.slice(0, 2))} מול ${ltr(rg.slice(0, 2))} אינם הפוכים.`);
      if (fl.occupancy === 0 && st.w !== 0) sum += ` בלי הביט החמישי המצביעים היו ${ltr(bitsOf(wa, 4))} ו-${ltr(bitsOf(ra, 4))}: שווים, בדיוק כמו במצב מלא.`;
      if (fl.full) sum += ` ארבעת הביטים הנמוכים של שני המצביעים שווים (${ltr(bitsOf(wa, 4))}): בלי הביט החמישי זה היה נראה ריק.`;
      $(".gr-sum").innerHTML = sum;
    };
    const step = (dw, dr) => { for (let i = 0; i < dw; i++) if (!grayFlags(st.w, st.r, BITS).full) st.w = (st.w + 1) & 31; for (let i = 0; i < dr; i++) if (!grayFlags(st.w, st.r, BITS).empty) st.r = (st.r + 1) & 31; draw(); };
    $(".ex-write").addEventListener("click", () => step(1, 0));
    $(".ex-read").addEventListener("click", () => step(0, 1));
    $(".ex-write8").addEventListener("click", () => step(8, 0));
    $(".ex-read8").addEventListener("click", () => step(0, 8));
    $(".ex-start").addEventListener("click", () => { st.w = 0; st.r = 0; draw(); });
    draw();
  };

  const VIEWS = {
    "cake-arith": () => cakeView("arith"),
    "cake-geo": () => cakeView("geo"),
    motorcycle: motorcycleView,
    josephus: josephusView,
    clock: clockView,
    strip: stripView,
    hourglass: hourglassView,
    probability: probabilityView,
    bridge: bridgeView,
    river: riverView,
    pcie: pcieView,
    fifo: fifoView,
    mtbf: mtbfView,
    triangle: triangleView,
    polygon: polygonView,
    boxes: boxesView,
    floyd: floydView,
    bfs01: bfs01View,
    brackets: bracketsView,
    ttt: tttView,
    shapes: shapesView,
    kaprekar: kaprekarView,
    eurovision: euroView,
    boxes3: boxes3View,
    edge: edgeView,
    lfsr: lfsrView,
    div3: div3View,
    gray: grayView,
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
