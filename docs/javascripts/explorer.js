// Interactive explorers: a box `<div class="explorer" data-kind="..." data-...>` mounts
// the controls, a summary line and figures of its kind, redrawn on every change. One
// model per kind:
//   cake-arith / cake-geo  0027, 0028  the law, sliders a and d (or q) with exact fields (a tiny a, a negative d, q below 1), and a person-by-person stepper of the cake
//   motorcycle             0026        sliders t0 and t1, a strategy, and play: the travellers on the road and the chart; 1 to 5 riders, a km field, a second plan dashed
//   josephus               0016, 0022  sliders N (and L), and the circle played step by step; the survivor chart; Josephus's own rule (0016), a seat lookup, N up to a million
//   clock                  0029        a clock face to drag, play or type: meetings of the hands so far
//   strip                  0030        drag the spider and the fly on their walls: the periodic strip and the path
//   hourglass              0018, 0019  A, B (and C) and D: the plan on a time axis and event by event (BFS or Dijkstra), the page's objective or the fewest flips
//   probability            0015        p, q and C: the answer, the two-children square and the curve against q
//   bridge                 0031        crossing times, a bridge of two or three: the Dijkstra plan (or one of the two classic plans) played crossing by crossing
//   river                  0032        cross by hand or let the BFS plan play; the state graph follows
//   pcie                   0020, 0021  address, length, MPS and RCB: the blocks, the count and the map of splits
//   fifo                   0033        burst, write and read rates, a skipping reader: the fill level over time; a wr / rd timing strip on a real time axis over a sliding window
//   mtbf                   0037        clock and data rates, tau, T0 and overhead: the MTBF of one to three flops
//   triangle               0007        three points to drag, type or nudge with arrow keys, inside / edge / outside; play counts every triangle; a largest-arc histogram of 1,000 draws
//   polygon                0007        the same for n vertices (3 to 10): drag, type, arrow keys or draw; random draws against 1 - n / 2^(n-1)
//   boxes                  0009        N boxes on a ring with their cycles, person 0's cut, a walk box by box, rounds without person 0; the copy link carries the arrangement and the walk
//   floyd                  0017        the array as the graph i -> nums[i], the tortoise and the hare through both phases; the copy link carries the array and the step
//   bfs01                  0005        the remainders modulo x on a ring, the BFS tree one dequeue at a time, the answer read back; a digit set and a length-only mode
//   abmap                  0005        the 45 digit pairs a < b for one x: the length of the smallest multiple or ✗, the answer, x = 2^s 5^t m and the rule of the theorem
//   brackets               0010        a typed bracket string read character by character: the stack, the depth chart, the first failure
//   ttt                    0011        tap cells on a 3 x 3 board: is it a legal final board and why not; random legal boards; wrap diagonals
//   shapes                 0014        squares or rectangles drawn one at a time with the rejected candidates flashed; a heat map of draws
//   kaprekar               0012, 0013  a number, its sort-and-subtract chain to 495 / 6174, the histogram of chain lengths
//   eurovision             0008        the announcements one by one: the cups under Israel's total against the points left; a what-if box
//   boxes3                 0004        three mislabelled boxes with hidden contents: draw a ball, the deduction line by line
//   edge                   0001        sig drawn cell by cell on a timing strip; sig_q and pulse follow, for a rising, falling or any edge; the reset trap
//   lfsr                   0036        a width of 3 to 8 bits: tick the taps, step or play from 0…01 on a ring of the states (up to 6 bits); a strip of clk, state, s[0] and fb; the polynomials and their periods, the primitive ones counted
//   div3                   0035        the half-cycle model one clock edge at a time: cnt, a, b and clk_out on a strip, the duty measured; a wake-up in an unreachable state; a divide by N (2 to 10) and a strip length
//   gray                   0034        a pointer step through a synchroniser, bit by bit, in binary and in Gray, for 3 to 6 bits; a FIFO of 8 to 64 entries with the pointers one bit wider, the flags and a strip of the operations
//   stock                  0006        prices to drag or draw, the scan played day by day: the cheapest and dearest day so far, the best long and short; the copy link carries the prices and the day
//   handshake              0038        req and ack drawn cell by cell; the four rules checked every cycle, a failure marked on its assertion's row
//   acknak                 0025        the RC and the EP with the two link queues: send, deliver / corrupt / lose, the timers; the page's examples as scripts; random traffic at a fault rate with the invariants checked; an event axis of the counters
//   credits                0024        the four counters as hands on a modulo-256 circle, the buffer, packets in flight; grant, transmit, lose, dequeue, sync; random legal traffic at a loss rate with the invariants checked; an event axis of the counters
//   endpoint               0023        a request builder on the block map, reads cut at RCB boundaries and interleaved cycle by cycle, the completions table; a timeline of every read's waits and completions; a cycle axis of the completions and the ready reads
//   trace                  0002, 0003  the page's Python one line (or one comparison) at a time: the swaps (and the three-variable XOR rotation) with a0 / b0 / c0 expressions, the double loop with its invariant
// The math of each model is exported under Node, where the question tests compare it with
// the Python reference (tests/0001 to 0022, 0026 to 0038).
(() => {
  const EPS = 1e-9;

  // mulberry32: a small seeded generator, so a random draw can be replayed from its seed
  // (the question tests use the same recurrence).
  const mulberry32 = (seed) => {
    let a = seed | 0;
    return () => {
      a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };
  const SEED_MAX = 99999;
  const newSeed = () => 1 + Math.floor(Math.random() * SEED_MAX);

  // --- models: pure math ---------------------------------------------------------------

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

  // The general rule "keep people stay, remove leave" (the page's L rule is keep 1,
  // remove L - 1; Josephus's own story is keep 2, remove 1): the steps as
  // [who stay (an array), who leave] and the survivor, by the same semantics as
  // josephusSteps (the count of leavers is fixed before anyone leaves).
  const josephusKR = (n, keep, remove) => {
    const circle = Array.from({ length: n }, (_, i) => i), steps = [];
    let i = 0;
    while (circle.length > 1) {
      const stays = [];
      for (let k = 0; k < keep; k++) { stays.push(circle[(i + k) % circle.length]); }
      i = (i + keep - 1) % circle.length;
      const leave = [], count = Math.min(remove, circle.length - 1);
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
  // The survivor alone, in O(n) with a circular linked list (N up to a million).
  const josephusSurvivor = (n, keep, remove) => {
    if (n === 1) return 0;
    const next = new Int32Array(n);
    for (let i = 0; i < n; i++) next[i] = (i + 1) % n;
    let cur = 0, left = n;                          // cur is the first to stay in the step
    while (left > 1) {
      for (let k = 0; k < keep - 1; k++) cur = next[cur];
      const count = Math.min(remove, left - 1);
      for (let s = 0; s < count; s++) { next[cur] = next[next[cur]]; left -= 1; }   // the one after cur leaves
      cur = next[cur];
    }
    return cur;
  };
  // Josephus's own rule has no closed form: the recurrence f(m) = (f(m - 1) + 3) mod m.
  const josephusRecurrence = (n, step = 3) => { let f = 0; for (let m = 2; m <= n; m++) f = (f + step) % m; return f; };
  // The reverse lookup: the first `count` circle sizes N (up to `limit`) in which seat s
  // survives. The page's L rule uses the closed form; Josephus's rule (L null) the recurrence.
  const josephusSeats = (s, L, count = 5, limit = 1000000) => {
    const out = [];
    if (L === null) {
      let f = 0;
      if (s === 0) out.push(1);
      for (let m = 2; m <= limit && out.length < count; m++) { f = (f + 3) % m; if (f === s) out.push(m); }
      return out;
    }
    if (s % L !== 0) return out;                    // F_L is always a multiple of L
    for (let n = 1; n <= limit && out.length < count; n++) if (josephusFormula(n, L) === s) out.push(n);
    return out;
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

  // The follow-ups of 0018 and 0019 in one search: `sizes` is [A, B] or [A, B, C] (letters
  // A, B, C in the actions), `interval` measures between two events as 0019 does, and
  // `objective` is "events" (every event costs 1: the BFS of 0018), "time" (the earliest
  // end: the Dijkstra of 0019) or "flips" (every hourglass flipped costs 1, a wait is
  // free, equal flips settled by time). Dijkstra on a binary heap. Returns
  // { start, plan, end, events, flips, explored } or null.
  const hourglassStepN = (sizes, tops, mask) => {
    const next = tops.map((v, i) => ((mask >> i) & 1 ? sizes[i] - v : v));
    const running = next.filter((v) => v > 0);
    if (!running.length) return null;
    const w = Math.min(...running);
    return [w, next.map((v) => Math.max(v - w, 0))];
  };
  const hourglassSearch = (sizes, D, { interval = false, objective = "events" } = {}) => {
    const n = sizes.length, letters = (mask) => sizes.map((_, i) => ((mask >> i) & 1 ? "ABC"[i] : "")).join("");
    const heap = [];
    const push = (item) => { heap.push(item); let i = heap.length - 1; while (i > 0) { const j = (i - 1) >> 1; if (heap[j][0] < item[0] || (heap[j][0] === item[0] && heap[j][1] < item[1])) break; heap[i] = heap[j]; i = j; } heap[i] = item; };
    const pop = () => { const top = heap[0], last = heap.pop(); if (!heap.length) return top; let i = 0; for (;;) { let m = i; const l = 2 * i + 1, r = l + 1; const lt = (x, y) => x[0] < y[0] || (x[0] === y[0] && x[1] < y[1]); if (l < heap.length && lt(heap[l], last) && (r >= heap.length || lt(heap[l], heap[r]))) m = l; else if (r < heap.length && lt(heap[r], last)) m = r; if (m === i) break; heap[i] = heap[m]; i = m; } heap[i] = last; return top; };
    // the flips objective breaks ties by time (a flip is worth more than any wait)
    const cost = (w, mask) => (objective === "flips" ? [...Array(n)].reduce((c, _, i) => c + ((mask >> i) & 1), 0) * 10000 + w : objective === "time" ? w : 1);
    // state: tops (and m, the minutes measured so far, -1 before the start, in the interval mode)
    const best = new Map();
    let tie = 0, explored = 0;
    const start0 = { t: 0, tops: sizes.map(() => 0), m: interval ? -1 : 0, start: interval ? null : 0, plan: [] };
    const key = (st) => (interval ? `${st.tops.join()},${st.m}` : `${st.t},${st.tops.join()}`);
    best.set(key(start0), 0);
    push([0, tie++, start0]);
    while (heap.length) {
      const [c, , st] = pop();
      if (c > best.get(key(st))) continue;
      explored += 1;
      const measured = interval ? st.m : st.t;
      if (measured === D) {
        const flips = st.plan.reduce((f, [, act]) => f + act.length, 0);
        return { start: st.start, plan: st.plan, end: st.t, events: st.plan.length, flips, explored };
      }
      const options = [];
      if (interval && st.m === -1) options.push([0, { ...st, m: 0, start: st.t }]);
      for (let mask = 0; mask < 1 << n; mask++) {
        const r = hourglassStepN(sizes, st.tops, mask);
        if (!r) continue;
        const [w, tops] = r, m2 = interval ? (st.m === -1 ? -1 : st.m + w) : st.t + w;
        if ((interval ? m2 : st.t + w) > D) continue;
        options.push([cost(w, mask), { t: st.t + w, tops, m: interval ? m2 : 0, start: st.start, plan: [...st.plan, [st.t, letters(mask)]] }]);
      }
      options.forEach(([dc, s2]) => {
        const k2 = key(s2), c2 = c + dc;
        if (!best.has(k2) || c2 < best.get(k2)) { best.set(k2, c2); push([c2, tie++, s2]); }
      });
    }
    return null;
  };
  // Replay a plan on any number of hourglasses: [t, action, tops on arrival, tops after].
  const hourglassReplayN = (sizes, plan, end) => {
    let t = 0, tops = sizes.map(() => 0);
    const events = [], acts = new Map(plan.map(([w, act]) => [w, act]));
    for (;;) {
      const act = acts.has(t) ? acts.get(t) : null;
      if (act === null) { events.push([t, "", tops, null]); return events; }
      const mask = sizes.reduce((m, _, i) => m | (act.includes("ABC"[i]) ? 1 << i : 0), 0);
      const r = hourglassStepN(sizes, tops, mask);
      events.push([t, act, tops, tops.map((v, i) => ((mask >> i) & 1 ? sizes[i] - v : v))]);
      if (!r) return events;
      t += r[0]; tops = r[1];
      if (end !== undefined && t > end) return events;
    }
  };
  const hourglassReachableN = (sizes, bound) => {
    const n = sizes.length, seen = new Set([`0,${sizes.map(() => 0).join()}`]), times = new Set();
    const queue = [[0, sizes.map(() => 0)]];
    for (let head = 0; head < queue.length; head++) {
      const [t, tops] = queue[head];
      for (let mask = 0; mask < 1 << n; mask++) {
        const r = hourglassStepN(sizes, tops, mask);
        if (!r || t + r[0] > bound) continue;
        const k = `${t + r[0]},${r[1].join()}`;
        if (seen.has(k)) continue;
        seen.add(k); times.add(t + r[0]); queue.push([t + r[0], r[1]]);
      }
    }
    return [...times].sort((u, v) => u - v);
  };

  // Probability (0015): P(all C children are boys | at least one is a boy with the trait).
  const probabilityAnswer = (C, p, q) => (Math.pow(p, C) * (1 - Math.pow(1 - q, C))) / (1 - Math.pow(1 - p * q, C));

  // Bridge and torch (0031): Dijkstra over (who is across, torch side); a crossing of one
  // or two people from the torch's bank costs the time of the slower. Returns the least
  // time and the crossings as arrays of indices, as the page code does.
  // bridgeSolve: Dijkstra over (who is across, torch side); `cap` people fit on the bridge
  // (2 on the page, 3 in the follow-up). Groups are tried as i <= j <= k so that the
  // tie-break of the page's figure is kept.
  const bridgeSolve = (times, cap = 2) => {
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
      const bank = [];
      for (let i = 0; i < n; i++) if (((across >> i) & 1) === side) bank.push(i);
      const relax = (g) => {
        const mask = g.reduce((m, i) => m | (1 << i), 0), cost = Math.max(...g.map((i) => times[i]));
        const nxt = ((across ^ mask) << 1) | (1 - side);
        if (reach[cur] + cost < reach[nxt]) { reach[nxt] = reach[cur] + cost; prev[nxt] = cur; via[nxt] = mask; }
      };
      bank.forEach((i, a) => bank.slice(a).forEach((j, b) => {
        if (cap >= 3) bank.slice(a + b).forEach((k) => relax([i, j, k]));
        else relax([i, j]);
      }));
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
  // The two classic plans of the page as crossings (a bridge of two): the fastest escorts
  // everyone one by one; or, round after round, the two slowest cross together (the fast
  // pair goes first, the fastest brings the torch back, the slowest pair crosses, the
  // second brings it back), with three or fewer left done directly. bridgeTime replays.
  const bridgeTime = (times, moves) => moves.reduce((t, g) => t + Math.max(...g.map((i) => times[i])), 0);
  const bridgeOrder = (times) => times.map((t, i) => i).sort((u, v) => times[u] - times[v] || u - v);
  const bridgeEscortMoves = (times) => {
    const o = bridgeOrder(times), moves = [];
    if (o.length === 1) return [[o[0]]];
    o.slice(1).forEach((p, k) => { moves.push([o[0], p]); if (k < o.length - 2) moves.push([o[0]]); });
    return moves;
  };
  const bridgePairMoves = (times) => {
    const o = bridgeOrder(times), moves = [];
    let rest = o;
    while (rest.length > 3) {
      const [f, s] = rest, slow2 = rest.slice(-2);
      moves.push([f, s], [f], slow2, [s]);
      rest = rest.slice(0, -2);
    }
    if (rest.length === 3) moves.push([rest[0], rest[1]], [rest[0]], [rest[0], rest[2]]);
    else moves.push(rest);
    return moves;
  };

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

  // Shareable state (0006, 0017, 0009): the payload after `#state-<kind>.` reopens a box
  // with the typed input and the step it was at. enc() writes the payload, dec() returns
  // the state (the step clamped to the trace) or null for anything malformed, out of
  // range or not a permutation.
  const intList = (text, lo, hi) => {
    if (!/^\d+(\.\d+)*$/.test(text)) return null;
    const v = text.split(".").map(Number);
    return v.every((x) => x >= lo && x <= hi) ? v : null;
  };
  const STATE_CODECS = {
    stock: {
      enc: (s) => `${s.prices.join(".")}-${s.k}-${s.both ? "both" : "long"}`,
      dec: (text) => {
        const m = /^([\d.]+)-(\d+)-(both|long)$/.exec(text);
        const prices = m && intList(m[1], 1, 20);
        if (!prices || prices.length < 2 || prices.length > 20) return null;
        return { prices, k: Math.min(Number(m[2]), prices.length), both: m[3] === "both" };
      },
    },
    floyd: {
      enc: (s) => `${s.nums.join(".")}-${s.k}`,
      dec: (text, nmax = 12) => {
        const m = /^([\d.]+)-(\d+)$/.exec(text);
        const nums = m && floydParse(m[1].replace(/\./g, " "));
        if (!nums || nums.length - 1 > nmax) return null;
        return { nums, k: Math.min(Number(m[2]), floydTrace(nums).frames.length - 1) };
      },
    },
    boxes: {
      enc: (s) => `${s.notes.slice(1).join(".")}-${s.me}-${s.helper ? 1 : 0}-${s.step}`,
      dec: (text, nmax = 16) => {
        const m = /^([\d.]+)-(\d+)-([01])-(\d+)$/.exec(text);
        const p = m && intList(m[1], 1, nmax), n = p ? p.length : 0, me = m && Number(m[2]);
        if (!p || n < 4 || n % 2 || n > nmax || me < 1 || me > n) return null;
        if ([...p].sort((a, b) => a - b).some((v, i) => v !== i + 1)) return null;
        return { n, notes: [0, ...p], me, helper: m[3] === "1", step: Number(m[4]) };
      },
    },
  };

  // Smallest 0/1 multiple (0005): the page's BFS over the remainders modulo x, one frame
  // per dequeue: the remainder taken out, its children (the smaller digit first) with
  // their fate, and the queue after the step. Numbers are strings of digits (they outgrow
  // 2^53). `digits` is the allowed set (the page's [0, 1]; the follow-up's [3, 7]): the
  // BFS starts from every non-zero digit, and when the queue empties before the
  // remainder 0 there is no multiple (answer null). `depth` is the BFS layer of every
  // remainder reached (the length of its number), for the length-only mode.
  const bfs01Trace = (x, digits = [0, 1]) => {
    const parent = new Array(x).fill(-1), digit = new Array(x).fill(""), visited = new Array(x).fill(false), depth = new Array(x).fill(0);
    const starts = [], queue = [];
    digits.filter((d) => d > 0).forEach((d) => {
      const r = d % x;
      if (visited[r]) return;
      visited[r] = true; digit[r] = String(d); depth[r] = 1; starts.push(r); queue.push(r);
    });
    const number = (r) => { let s = ""; for (let q = r; q !== -1; q = parent[q]) s = digit[q] + s; return s; };
    const frames = [];
    while (!visited[0] && queue.length) {
      const r = queue.shift(), kids = [];
      for (const d of digits) {
        const nr = (r * 10 + d) % x;
        if (!visited[nr]) { visited[nr] = true; parent[nr] = r; digit[nr] = String(d); depth[nr] = depth[r] + 1; queue.push(nr); kids.push({ d, nr, status: nr === 0 ? "found" : "new" }); }
        else kids.push({ d, nr, status: "seen" });
      }
      frames.push({ r, number: number(r), kids, queue: [...queue] });
    }
    const found = visited[0];
    const path = [];                                 // remainders from the start to 0
    if (found) for (let q = 0; q !== -1; q = parent[q]) path.unshift(q);
    return { frames, answer: found ? number(0) : null, path, parent, digit, depth, start: starts[0], starts, dequeues: frames.length, digits };
  };
  // the counts of the page's chart: multiples of x scanned, numbers over the digit set
  // enumerated in increasing order up to the answer, dequeues
  const bfs01Counts = (x, digits = [0, 1]) => {
    const t = bfs01Trace(x, digits);
    if (t.answer === null) return { multiples: null, enumerated: null, dequeues: t.dequeues, answer: null };
    const y = BigInt(t.answer), k = BigInt(digits.length), nz = digits.filter((d) => d > 0), L = t.answer.length;
    let enumerated = 0n, pow = 1n;                   // numbers shorter than the answer
    for (let len = 1; len < L; len++) { enumerated += BigInt(nz.length) * pow; pow *= k; }
    let rank = 0n;                                   // the answer's place among the numbers of its length
    for (let i = 0; i < L; i++) {
      const d = Number(t.answer[i]);
      rank = rank * k + BigInt(i === 0 ? nz.indexOf(d) : digits.indexOf(d));
    }
    enumerated += rank + 1n;
    return { multiples: (y / BigInt(x)).toString(), enumerated: enumerated.toString(), dequeues: t.dequeues, answer: t.answer };
  };

  // Two general digits a < b (0005 follow-up): the page's smallest_ab_multiple (the BFS
  // without frames, for every pair at once) and has_ab_solution with the rule of the
  // theorem that decided, for the map of the 45 pairs.
  const abMultiple = (x, a, b) => {
    const parent = new Int32Array(x).fill(-1), digit = new Int8Array(x), visited = new Uint8Array(x), queue = new Int32Array(x);
    let head = 0, tail = 0;
    for (const d of [a, b]) if (d > 0 && !visited[d % x]) { visited[d % x] = 1; digit[d % x] = d; queue[tail++] = d % x; }
    while (head < tail && !visited[0]) {
      const r = queue[head++];
      for (const d of [a, b]) {
        const nr = (r * 10 + d) % x;
        if (!visited[nr]) { visited[nr] = 1; parent[nr] = r; digit[nr] = d; queue[tail++] = nr; }
      }
    }
    if (!visited[0]) return { answer: null, dequeues: head };
    const out = [];
    for (let r = 0; r !== -1; r = parent[r]) out.push(digit[r]);
    return { answer: out.reverse().join(""), dequeues: head };
  };
  const abExists = (x, a, b) => {
    let m = x, s = 0, t = 0, halvings = 0;
    while (m % 2 === 0) { m /= 2; s++; }
    while (m % 5 === 0) { m /= 5; t++; }
    const out = (ok, rule) => ({ ok, rule, s, t, m, halvings, a2: a, b2: b });
    if (a === 0) return out(true, "zero");
    if (s > 0 && t > 0) return out(false, "ten");
    if (t > 0) {
      if (a !== 5 && b !== 5) return out(false, "no5");
      if (t === 1) return out(true, "five");
      if (t === 2) return (a === 2 && b === 5) || (a === 5 && b === 7) ? out(true, "twentyfive") : out(false, "no25");
      return out(false, "no125");
    }
    if (s === 0) return out(true, "coprime");
    let a2 = a, b2 = b, s2 = s;
    while (s2 > 0 && a2 % 2 === 0 && b2 % 2 === 0) { a2 /= 2; b2 /= 2; s2--; halvings++; }
    const res = s2 === 0 ? { ok: true, rule: "halved" } : a2 % 2 !== b2 % 2 ? { ok: true, rule: "mixed" } : { ok: false, rule: "odd" };
    return { ...res, s, t, m, halvings, a2, b2 };
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
  // The discrete count of part d for n vertices at whole degrees (M points): the bad sets
  // by the first vertex of the half circle, M * C(floor(M / 2), n - 1) of the C(M, n).
  // Exact in BigInt: { num, den } reduced, and the value.
  const bigGcd = (a, b) => (b ? bigGcd(b, a % b) : a);
  const polyProbDiscrete = (n, M = TRI_M) => {
    const all = bigComb(M, n), bad = BigInt(M) * bigComb(Math.floor(M / 2), n - 1), good = all - bad;
    const g = bigGcd(good, all);
    return { num: (good / g).toString(), den: (all / g).toString(), value: Number(good) / Number(all) };
  };
  // The largest arc of three random points: the continuous distribution function (the
  // arcs are Dirichlet(1, 1, 1)), and a histogram of `draws` random whole-degree
  // triangles in bins of `bin` degrees from 120 to 360, split inside / outside (a
  // largest arc below 180 is inside; exactly 180 is the centre on an edge, counted
  // outside; a degenerate triangle is skipped and counted).
  const triArcCdf = (x) => {
    const u = x / 360;
    if (x <= 120) return 0;
    if (x >= 360) return 1;
    return x < 180 ? 1 - 3 * (1 - u) * (1 - u) + 3 * (1 - 2 * u) * (1 - 2 * u) : 1 - 3 * (1 - u) * (1 - u);
  };
  const triHistogram = (rnd = Math.random, draws = 1000, bin = 10) => {
    const bins = [];
    for (let lo = 120; lo < 360; lo += bin) bins.push({ lo, hi: lo + bin, in: 0, out: 0, expected: draws * (triArcCdf(lo + bin) - triArcCdf(lo)) });
    let degenerate = 0;
    for (let k = 0; k < draws; k++) {
      const angles = [0, 1, 2].map(() => Math.floor(rnd() * TRI_M));
      const kind = triClass(angles);
      if (kind === "degenerate") { degenerate += 1; continue; }
      const top = Math.max(...triArcs(angles));
      const b = bins[Math.min(bins.length - 1, Math.floor((top - 120) / bin))];
      if (kind === "in") b.in += 1; else b.out += 1;
    }
    return { bins, draws, degenerate };
  };
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
  // The LFSR strip: one slot per state visited so far (step 0 .. k), its value, the bit
  // that leaves (s[0]) and the feedback bit that enters the next state.
  const lfsrStrip = (mask, width, k, seed = 1) => {
    const walk = lfsrWalk(mask, width, seed), total = walk.period;
    const states = walk.states.concat(walk.states[walk.back]).slice(0, Math.min(k, total) + 1);
    const fb = states.map((s) => { let v = 0; for (let x = s & mask; x; x >>= 1) v ^= x & 1; return v; });
    return { states, out: states.map((s) => s & 1), fb, total };
  };
  // φ(2^n − 1) / n: the number of primitive polynomials of degree n (Euler's totient by trial division)
  const lfsrPrimitiveCount = (width) => {
    let n = (1 << width) - 1, phi = n;
    for (let p = 2; p * p <= n; p++) if (n % p === 0) { while (n % p === 0) n /= p; phi -= phi / p; }
    if (n > 1) phi -= phi / n;
    return phi / width;
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
  // The follow-up generalises to a divide by N: the counter is modulo N in
  // ceil(log2 N) bits, a is high for the last floor(N / 2) counts (one for N = 3, two
  // for N = 5 and for N = 4), b is a half a cycle later, and the output is a | b for an
  // odd N (high N / 2 cycles) and a alone for an even N (already 50%; the OR would add
  // half a cycle). The highest state of the counter, 2^bits - 1, is unreachable when it
  // is >= N.
  const div3Params = (N) => {
    const bits = Math.max(1, Math.ceil(Math.log2(N) - 1e-9)), top = (1 << bits) - 1;
    const high = Math.floor(N / 2);
    return { N, bits, mask: top, high, from: N - high, wake: top >= N ? top : null, odd: N % 2 === 1 };
  };
  const div3Trace = (halfCycles, cnt0 = 0, counter = "wrap", N = 3) => {
    const P = div3Params(N);
    let cnt = cnt0, a = 0, b = 0;
    const rows = [];
    for (let edge = 0; edge < halfCycles; edge++) {
      const rising = edge % 2 === 0;
      const pa = a, pb = b, pc = cnt;
      if (rising) {
        a = cnt >= P.from && cnt <= N - 1 ? 1 : 0;
        if (counter === "guard") cnt = cnt >= N - 1 ? 0 : cnt + 1;
        else if (counter === "wide") cnt = cnt === N - 1 ? 0 : cnt + 1;
        else cnt = cnt === N - 1 ? 0 : (cnt + 1) & P.mask;
      } else b = a;
      rows.push({ edge, rising, cnt, a, b, out: P.odd ? a | b : a, aChanged: a !== pa, bChanged: b !== pb, cntPrev: pc });
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
  // The FIFO strip: the operations so far, one column each (a burst is several), with the
  // pointers and the flags after it; a full FIFO refuses a write and an empty one a read,
  // so a burst stops early. Column 0 is the reset.
  const grayFlagsOps = (ops, size) => {
    const bits = Math.log2(size) + 1, wrap = 2 * size - 1;
    let w = 0, r = 0;
    const col = (op) => { const fl = grayFlags(w, r, bits); return { op, w, r, wg: fl.wg, rg: fl.rg, full: fl.full, empty: fl.empty, occupancy: fl.occupancy }; };
    const cols = [col(null)];
    ops.forEach((op) => {
      const fl = grayFlags(w, r, bits);
      if (op === "w" && !fl.full) { w = (w + 1) & wrap; cols.push(col("w")); }
      else if (op === "r" && !fl.empty) { r = (r + 1) & wrap; cols.push(col("r")); }
    });
    return cols;
  };
  const grayFlags = (w, r, bits) => {
    const wg = grayOf(w), rg = grayOf(r);
    const top = 3 << (bits - 2), rest = (1 << (bits - 2)) - 1;
    const empty = wg === rg;
    const full = (wg & top) === (~rg & top) && (wg & rest) === (rg & rest);
    const occupancy = (w - r) & ((1 << bits) - 1);
    return { wg, rg, empty, full, occupancy };
  };

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

  // Handshake (0038): the page's reference model on sampled values (index = cycle); the
  // cycle at which each rule fails is the cycle at which the SVA reports it.
  const hsCheck = (req, ack, maxWait = 3) => {
    const n = req.length, fails = { hold: [], late: [], orphan: [], drop: [] };
    for (let t = 0; t < n; t++) {
      const prevReq = t ? req[t - 1] : 0, prevAck = t ? ack[t - 1] : 0;
      if (t && prevReq && !prevAck && !req[t]) fails.hold.push(t);
      if (req[t] && !prevReq) {
        const window = ack.slice(t + 1, t + 1 + maxWait);
        if (window.length === maxWait && !window.some((v) => v)) fails.late.push(t + maxWait);
      }
      if (ack[t] && !req[t]) fails.orphan.push(t);
      if (t && prevAck && req[t]) fails.drop.push(t);
    }
    return fails;
  };
  // The page's four traces as WaveDrom strings; a wave string expanded to n cycles.
  const HS_PRESETS = {
    ok: ["01..0...", "0..10..."],
    late: ["01....0.", "0....10."],
    drop: ["01.0....", "0......."],
    orphan: ["0.......", "0.10...."],
  };
  const hsWave = (text, n) => {
    const out = [];
    for (let i = 0; i < n; i++) { const c = text[i]; out.push(c === undefined || c === "." ? (out.length ? out[out.length - 1] : 0) : Number(c)); }
    return out;
  };

  // Ack/Nak (0025): the page's TransmitterWithReplay and ReceiverWithNak as one state
  // object with the two link queues between them (TLPs towards the EP, DLLPs towards
  // the RC). `anApply` is pure: it returns the next state and a log of what happened.
  // `rnd()` draws the EP's next Ack threshold (1..4), as the page's rng.randint(1, 4).
  const AN_MOD = 4096;
  const anInit = (startSeq, rnd) => ({
    nts: startSeq % AN_MOD, ackd: (startSeq - 1 + AN_MOD) % AN_MOD, retry: [], link: [], dllps: [],
    badDllp: 0, proto: 0, replays: 0,
    nrs: startSeq % AN_MOD, nak: false, pending: 0, threshold: rnd(), received: [], badTlp: 0, dups: 0,
    payload: 0xA0,
  });
  const anClone = (s) => ({ ...s, retry: s.retry.map((t) => ({ ...t })), link: s.link.map((t) => ({ ...t })), dllps: s.dllps.map((d) => ({ ...d })), received: [...s.received] });
  const anApply = (state, ev, rnd) => {
    const s = anClone(state), log = { type: ev.type, how: ev.how, items: [] };
    const lastAccepted = () => (s.nrs - 1 + AN_MOD) % AN_MOD;
    const sendAck = () => { s.dllps.push({ kind: "ACK", seq: lastAccepted(), crcOk: true }); s.pending = 0; s.threshold = rnd(); log.items.push({ out: "ack", seq: lastAccepted() }); };
    const scheduleNak = () => { if (s.nak) { log.items.push({ out: "nakHeld" }); return; } s.dllps.push({ kind: "NAK", seq: lastAccepted(), crcOk: true }); s.nak = true; s.pending = 0; log.items.push({ out: "nak", seq: lastAccepted() }); };
    const accept = (t) => { s.received.push(t.seq); s.nrs = (s.nrs + 1) % AN_MOD; s.nak = false; s.pending += 1; log.items.push({ out: "accepted", seq: t.seq, replay: t.replay }); if (s.pending >= s.threshold) sendAck(); };
    const isDup = (seq) => { const behind = (s.nrs - seq + AN_MOD) % AN_MOD; return behind > 0 && behind <= AN_MOD / 2; };
    const replay = () => { if (!s.retry.length) { log.items.push({ out: "nothingToReplay" }); return; } s.retry.forEach((t) => s.link.push({ ...t, crcOk: true, replay: true })); s.replays += 1; log.items.push({ out: "replay", seqs: s.retry.map((t) => t.seq) }); };
    if (ev.type === "send") {
      for (let i = 0; i < (ev.n || 1); i++) {
        const t = { seq: s.nts, payload: s.payload, crcOk: true, replay: false };
        s.retry.push({ seq: t.seq, payload: t.payload }); s.link.push(t);
        log.items.push({ out: "sent", seq: t.seq });
        s.nts = (s.nts + 1) % AN_MOD; s.payload += 1;
      }
    } else if (ev.type === "tlp") {
      for (let i = 0; i < (ev.count || 1); i++) {
        const t = s.link.shift();
        if (!t) { log.items.push({ out: "emptyLink" }); break; }
        if (ev.how === "lose") { log.items.push({ out: "lost", seq: t.seq }); continue; }
        if (ev.how === "bad" && i === 0) t.crcOk = false;
        if (!t.crcOk) { s.badTlp += 1; log.items.push({ out: "badTlp", seq: t.seq }); scheduleNak(); }
        else if (t.seq === s.nrs) accept(t);
        else if (isDup(t.seq)) { s.dups += 1; log.items.push({ out: "dup", seq: t.seq }); sendAck(); }
        else { s.badTlp += 1; log.items.push({ out: "future", seq: t.seq, expected: s.nrs }); scheduleNak(); }
      }
    } else if (ev.type === "dllp") {
      const d = s.dllps.shift();
      if (!d) log.items.push({ out: "emptyLink" });
      else if (ev.how === "lose") log.items.push({ out: "lost", kind: d.kind, seq: d.seq });
      else {
        if (ev.how === "bad") d.crcOk = false;
        if (ev.tamper !== undefined) d.seq = ev.tamper;
        log.kind = d.kind; log.seq = d.seq;
        if (!d.crcOk) { s.badDllp += 1; log.items.push({ out: "badDllp", kind: d.kind, seq: d.seq }); }
        else {
          const idx = s.retry.findIndex((t) => t.seq === d.seq);
          if (idx >= 0) { const purged = s.retry.slice(0, idx + 1).map((t) => t.seq); s.retry.splice(0, idx + 1); s.ackd = d.seq; log.items.push({ out: "purged", kind: d.kind, seq: d.seq, seqs: purged }); if (d.kind === "NAK") replay(); }
          else if (d.seq !== s.ackd) { s.proto += 1; log.items.push({ out: "protoErr", kind: d.kind, seq: d.seq }); }
          else { log.items.push({ out: "noProgress", kind: d.kind, seq: d.seq }); if (d.kind === "NAK") replay(); }
        }
      }
    } else if (ev.type === "flush") {
      if (s.pending && !s.nak) sendAck(); else log.items.push({ out: s.nak ? "flushNak" : "flushNothing" });
    } else if (ev.type === "timeout") {
      replay();
    }
    return { state: s, log };
  };
  // The page's two examples (tools/figures/q0025.py): start at 4094, scripted thresholds.
  const AN_SCRIPTS = {
    a: { start: 4094, thresholds: [2, 3, 1], steps: [
      { type: "send", n: 2 }, { type: "tlp", how: "ok" }, { type: "tlp", how: "ok" }, { type: "dllp", how: "ok" },
      { type: "send", n: 3 }, { type: "tlp", how: "ok" }, { type: "tlp", how: "ok" }, { type: "tlp", how: "ok" }, { type: "dllp", how: "ok" }] },
    b: { start: 4094, thresholds: [3, 1, 1, 1, 1], steps: [
      { type: "send", n: 4 }, { type: "tlp", how: "ok" }, { type: "tlp", how: "bad" }, { type: "tlp", how: "ok" }, { type: "tlp", how: "ok" },
      { type: "dllp", how: "ok" }, { type: "tlp", how: "ok" }, { type: "tlp", how: "ok", count: 2 }, { type: "dllp", how: "bad" },
      { type: "timeout" }, { type: "tlp", how: "ok", count: 3 }, { type: "dllp", how: "ok" }, { type: "dllp", how: "ok" }, { type: "dllp", how: "ok", tamper: 9 }] },
  };
  const anRun = (script, rnd) => {
    const th = [...script.thresholds];
    const draw = () => (th.length ? th.shift() : rnd());
    let s = anInit(script.start, draw);
    const states = [s];
    script.steps.forEach((ev) => { s = anApply(s, ev, draw).state; states.push(s); });
    return states;
  };
  // The two invariants the box checks, as the names of those that fail: "retry" (the
  // Retry Buffer holds exactly ACKD_SEQ + 1 .. NEXT_TRANSMIT_SEQ − 1) and "order" (the
  // TLPs were delivered once, in order).
  const anInvariants = (s) => {
    const expect = [];
    for (let q = (s.ackd + 1) % AN_MOD; q !== s.nts && expect.length <= AN_MOD; q = (q + 1) % AN_MOD) expect.push(q);
    const bad = [];
    if (expect.length !== s.retry.length || expect.some((q, i) => q !== s.retry[i].seq)) bad.push("retry");
    if (s.received.some((q, i) => i > 0 && q !== (s.received[i - 1] + 1) % AN_MOD)) bad.push("order");
    return bad;
  };
  // Random traffic, the way the page's test drives the link: `count` events drawn from
  // rnd (sends of 1 or 2 TLPs while fewer than 12 wait for an Ack, the head of a queue
  // delivered, the Ack timer, the replay timer once the link is drained), a delivery
  // corrupted or lost with probability `rate` (half each). The Ack thresholds are drawn
  // first and kept in the script, so the box replays it exactly. The invariants are
  // checked after every event and the first violation ends the script there (the
  // page's model never reaches one; the test corrupts a state to see the check fire).
  const anRandomScript = (start, count, rate, rnd) => {
    const thresholds = Array.from({ length: count + 2 }, () => 1 + Math.floor(rnd() * 4));
    const th = [...thresholds], draw = () => (th.length ? th.shift() : 1 + Math.floor(rnd() * 4));
    let s = anInit(start, draw);
    const steps = [], faults = { lost: 0, bad: 0 };
    let violation = null;
    const how = () => (rnd() < rate ? (rnd() < 0.5 ? "lose" : "bad") : "ok");
    while (steps.length < count) {
      const r = rnd();
      let ev;
      if (r < 0.15) { if (s.retry.length >= 12) continue; ev = { type: "send", n: 1 + Math.floor(rnd() * 2) }; }
      else if (r < 0.6) { if (!s.link.length) continue; ev = { type: "tlp", how: how() }; }
      else if (r < 0.85) { if (!s.dllps.length) continue; ev = { type: "dllp", how: how() }; }
      else if (r < 0.93) ev = { type: "flush" };
      else { if (s.link.length || !s.retry.length) continue; ev = { type: "timeout" }; }
      if (ev.how === "lose") faults.lost += 1; else if (ev.how === "bad") faults.bad += 1;
      steps.push(ev);
      s = anApply(s, ev, draw).state;
      const bad = anInvariants(s);
      if (bad.length) { violation = { index: steps.length, names: bad }; break; }
    }
    return { start, thresholds, steps, random: { count, rate, faults, violation } };
  };

  // The event axis of the box (X146): a short label per event, from its log.
  const anEventLabel = (log) => {
    if (!log) return "start";
    const mark = log.how === "bad" ? "!" : log.how === "lose" ? "×" : "";
    if (log.type === "send") return `TX${log.items.length > 1 ? log.items.length : ""}`;
    if (log.type === "tlp") return `TLP${mark}`;
    if (log.type === "dllp") { const it = log.items.find((x) => x.kind); const k = log.kind || (it && it.kind); return `${k === "NAK" ? "Nak" : k === "ACK" ? "Ack" : "DLLP"}${mark}`; }
    return log.type === "flush" ? "flush" : log.type === "timeout" ? "replay" : log.type;
  };
  // USB4 path credits (0024): the page's EgressSyncModel and IngressSyncModel as one
  // state with the packets in flight between them. Errors the page raises (a transmission
  // without a credit, a buffer overflow, a dequeue from an empty buffer) are counted and
  // leave the counters as they were.
  const CR_MOD = 256;
  const crDist = (a, b) => (b - a + CR_MOD) % CR_MOD;
  const crInit = (size, base = 0) => ({
    size, pcc: base % CR_MOD, pcl: base % CR_MOD, pcr: base % CR_MOD, pca: (base + size) % CR_MOD,
    occ: 0, link: [], nextId: 1, errors: 0,
  });
  const crCanTransmit = (s) => { const ahead = crDist(s.pcc, s.pcl); return ahead > 0 && ahead < 128; };
  const crApply = (state, ev) => {
    const s = { ...state, link: [...state.link] }, log = { type: ev.type, how: ev.how, items: [] };
    const transmit = () => {
      if (!crCanTransmit(s)) { s.errors += 1; log.items.push({ out: "noCredit", pcc: s.pcc, pcl: s.pcl }); return false; }
      s.pcc = (s.pcc + 1) % CR_MOD; s.link.push(s.nextId); log.items.push({ out: "transmitted", id: s.nextId }); s.nextId += 1; return true;
    };
    const receive = (how) => {
      const id = s.link.shift();
      if (id === undefined) { log.items.push({ out: "emptyLink" }); return; }
      if (how === "lose") { log.items.push({ out: "lost", id }); return; }
      if (s.occ >= s.size) { s.errors += 1; log.items.push({ out: "overflow", id }); return; }
      s.pcr = (s.pcr + 1) % CR_MOD; s.occ += 1; log.items.push({ out: "received", id });
    };
    if (ev.type === "grant") { s.pcl = s.pca; log.items.push({ out: "grant", value: s.pca, credits: crDist(s.pcc, s.pcl) }); }
    else if (ev.type === "transmit") transmit();
    else if (ev.type === "receive") receive(ev.how);
    else if (ev.type === "packet") { if (transmit()) receive(ev.how); }
    else if (ev.type === "dequeue") {
      if (s.occ === 0) { s.errors += 1; log.items.push({ out: "emptyBuffer" }); }
      else { s.occ -= 1; s.pca = (s.pca + 1) % CR_MOD; log.items.push({ out: "dequeued", pca: s.pca }); }
    } else if (ev.type === "sync") {
      const missing = crDist(s.pcr, s.pcc);
      s.pca = (s.pca + missing) % CR_MOD; log.items.push({ out: "sync", pcc: s.pcc, pcrBefore: s.pcr, missing, pca: s.pca }); s.pcr = s.pcc;
    }
    return { state: s, log };
  };
  // The page's two examples (tools/figures/q0024.py): a buffer of 5.
  const CR_SCRIPTS = {
    a: { size: 5, steps: [{ type: "grant" }, { type: "packet", how: "ok" }, { type: "packet", how: "ok" }, { type: "packet", how: "ok" }, { type: "dequeue" }, { type: "dequeue" }, { type: "grant" },
      { type: "packet", how: "ok" }, { type: "packet", how: "ok" }, { type: "packet", how: "ok" }, { type: "packet", how: "ok" }] },
    b: { size: 5, steps: [{ type: "grant" }, { type: "packet", how: "ok" }, { type: "packet", how: "lose" }, { type: "packet", how: "ok" }, { type: "dequeue" }, { type: "dequeue" }, { type: "grant" }, { type: "sync" }, { type: "grant" }] },
  };
  const crRun = (script, base = 0) => {
    let s = crInit(script.size, base);
    const states = [s];
    script.steps.forEach((ev) => { s = crApply(s, ev).state; states.push(s); });
    return states;
  };
  // What the credits add up to against the buffer: the credits the Egress holds plus the
  // packets in flight can never exceed the free slots; the gap is slots freed but not yet
  // granted (PCA − PCL) plus packets lost and not yet synced (the leak). A negative leak
  // means a Sync counted a packet in flight as lost, and the gap turns into an overflow
  // risk. crInvariants names what fails: "overflow" (an error of the page's models, or
  // more packets than slots) and "credits" (credits + in flight > free slots).
  const crBalance = (s) => {
    const credits = crDist(s.pcc, s.pcl), free = s.size - s.occ, ungranted = crDist(s.pcl, s.pca);
    return { credits, inFlight: s.link.length, free, ungranted, leak: free - credits - s.link.length - ungranted };
  };
  const crInvariants = (s) => {
    const b = crBalance(s), bad = [];
    if (s.errors || s.occ > s.size) bad.push("overflow");
    if (b.credits + b.inFlight > b.free) bad.push("credits");
    return bad;
  };
  // Random traffic as the page's test drives it: only legal events (a transmission with a
  // credit, a dequeue from a non-empty buffer, a Sync when nothing is in flight, since on
  // the in-order link it arrives after the packets ahead of it), a received packet lost
  // with probability `rate`. The invariants are checked after every event; the first
  // violation ends the script there.
  const crRandomScript = (size, base, count, rate, rnd) => {
    let s = crInit(size, base);
    const steps = [], faults = { lost: 0, syncs: 0 };
    let violation = null;
    while (steps.length < count) {
      const r = rnd();
      let ev;
      if (r < 0.3) { if (!crCanTransmit(s)) continue; ev = { type: "transmit" }; }
      else if (r < 0.65) { if (!s.link.length) continue; ev = { type: "receive", how: rnd() < rate ? "lose" : "ok" }; }
      else if (r < 0.8) { if (!s.occ) continue; ev = { type: "dequeue" }; }
      else if (r < 0.93) ev = { type: "grant" };
      else { if (s.link.length) continue; ev = { type: "sync" }; }
      if (ev.how === "lose") faults.lost += 1; else if (ev.type === "sync") faults.syncs += 1;
      steps.push(ev);
      s = crApply(s, ev).state;
      const bad = crInvariants(s);
      if (bad.length) { violation = { index: steps.length, names: bad }; break; }
    }
    return { size, steps, random: { count, rate, faults, violation } };
  };

  const crEventLabel = (log) => {
    if (!log) return "start";
    const mark = log.how === "lose" ? "×" : "";
    return { grant: "Grant", transmit: "TX", receive: `RX${mark}`, packet: `pkt${mark}`, dequeue: "deq", sync: "Sync" }[log.type] || log.type;
  };
  // PCIe endpoint (0023): the page's UnalignedEndpointModel. `rng` is {randint(a, b),
  // choice(n)}: the draws in the page's order (the cut coins of a read, then its delay;
  // the pick among the ready reads, then the gap), so they can be scripted (the page's
  // examples) or replayed by the tests.
  const EP_RCB = 128, EP_MRRS = 256, EP_MIN_DELAY = 1, EP_MAX_DELAY = 20, EP_MAX_GAP = 10;
  const epUnitRng = (units, rnd = Math.random) => {
    const next = () => (units.length ? units.shift() : rnd());
    return { randint: (a, b) => a + Math.floor(next() * (b - a + 1)), choice: (n) => Math.floor(next() * n) };
  };
  const epValueRng = (values, fallback) => ({
    randint: (a, b) => (values.length ? values.shift() : fallback.randint(a, b)),
    choice: (n) => (values.length ? values.shift() : fallback.choice(n)),
  });
  const epInit = () => ({ memory: {}, pending: [], cycle: 0, out: [], writes: [], reads: [], nextTag: 0x15, nextRead: 0 });
  const epWrite = (s, address, data) => {
    let done = 0;
    while (done < data.length) {
      const block = Math.floor((address + done) / EP_RCB), off = (address + done) % EP_RCB;
      const n = Math.min(EP_RCB - off, data.length - done), key = block * EP_RCB;
      if (!s.memory[key]) s.memory[key] = new Array(EP_RCB).fill(0);
      for (let i = 0; i < n; i++) s.memory[key][off + i] = data[done + i];
      done += n;
    }
    s.writes.push({ address, length: data.length, id: s.writes.length + 1 });
  };
  const epReadBytes = (s, address, length) => {
    const out = [];
    let done = 0;
    while (done < length) {
      const block = Math.floor((address + done) / EP_RCB), off = (address + done) % EP_RCB;
      const n = Math.min(EP_RCB - off, length - done), blk = s.memory[block * EP_RCB];
      for (let i = 0; i < n; i++) out.push(blk ? blk[off + i] : 0);
      done += n;
    }
    return out;
  };
  const epFragments = (address, length, rng) => {
    const end = address + length, sizes = [];
    let last = address, boundary = (Math.floor(address / EP_RCB) + 1) * EP_RCB;
    while (boundary < end) {
      if (rng.randint(0, 1)) { sizes.push(boundary - last); last = boundary; }
      boundary += EP_RCB;
    }
    sizes.push(end - last);
    return sizes;
  };
  const epRead = (s, req, rng) => {
    if (!(req.length > 0 && req.length <= EP_MRRS)) throw new Error("read exceeds MRRS");
    const data = epReadBytes(s, req.address, req.length);
    const p = { id: s.nextRead++, tag: req.tag, rid: req.rid, address: req.address, length: req.length, cpls: [], ready: 0, sent: 0 };
    let address = req.address, remaining = req.length;
    epFragments(req.address, req.length, rng).forEach((size) => {
      const off = address - req.address;
      p.cpls.push({ address, size, bc: remaining, data: data.slice(off, off + size) });
      address += size; remaining -= size;
    });
    p.total = p.cpls.length;
    p.ready = s.cycle + rng.randint(EP_MIN_DELAY, EP_MAX_DELAY);
    s.pending.push(p);
    // the read's record keeps its timeline: issued at, and every wait window [from, ready]
    s.reads.push({ id: p.id, tag: p.tag, rid: p.rid, address: p.address, length: p.length, sizes: p.cpls.map((c) => c.size), issued: s.cycle, waits: [[s.cycle, p.ready]] });
    return p;
  };
  const epNext = (s, rng) => {
    const ready = s.pending.filter((p) => p.ready <= s.cycle);
    if (!ready.length) return null;
    const pick = ready[rng.choice(ready.length)], cpl = pick.cpls.shift();
    pick.sent += 1;
    if (pick.cpls.length) { pick.ready = s.cycle + rng.randint(1, EP_MAX_GAP); s.reads.find((r) => r.id === pick.id).waits.push([s.cycle, pick.ready]); }
    else s.pending.splice(s.pending.indexOf(pick), 1);
    const rec = { cycle: s.cycle, read: pick.id, tag: pick.tag, rid: pick.rid, address: cpl.address, size: cpl.size, bc: cpl.bc, first: cpl.data[0], last: cpl.data[cpl.data.length - 1] };
    s.out.push(rec);
    return rec;
  };
  // One cycle as the page's run does it: tick, then one completion at most.
  const epCycle = (s, rng) => { s.cycle += 1; return epNext(s, rng); };
  // The page's two examples (tools/figures/q0023.py): a 512-byte write of i mod 256, two reads.
  const EP_SCRIPTS = {
    a: { reads: [[0x10000, 256, 0x0200, 0x15], [0x10100, 256, 0x0200, 0x16]], draws: [1, 5, 1, 3, 0, 3, 0, 1, 1, 0] },
    b: { reads: [[0x10000, 256, 0x0200, 0x15], [0x10020, 256, 0x0300, 0x22]], draws: [1, 4, 1, 1, 2, 0, 3, 0, 2, 0, 1, 0, 0] },
  };
  // The cycle axis of the endpoint box (X146): per cycle 0 .. now, the completion that
  // went out (or none), and for each of the last `keep` reads whether it was ready and
  // waiting its turn: from a wait window's ready cycle to the completion that ends it.
  const epStrip = (s, keep = 6) => {
    const n = s.cycle + 1, byCycle = new Map(s.out.map((c) => [c.cycle, c]));
    const cpl = Array.from({ length: n }, (_, c) => byCycle.get(c) || null);
    const reads = s.reads.slice(-keep).map((r) => {
      const outs = s.out.filter((c) => c.read === r.id).map((c) => c.cycle);
      const ready = Array.from({ length: n }, () => 0);
      r.waits.forEach(([, rdy], k) => { const end = k < outs.length ? outs[k] : s.cycle; for (let c = rdy; c <= end && c < n; c++) ready[c] = 1; });
      return { id: r.id, tag: r.tag, ready };
    });
    return { n, cpl, reads };
  };
  const epRunScript = (script) => {
    const s = epInit(), rng = epValueRng([...script.draws], epUnitRng([]));
    epWrite(s, 0x10000, Array.from({ length: 512 }, (_, i) => i & 0xFF));
    script.reads.forEach(([address, length, rid, tag]) => epRead(s, { address, length, rid, tag }, rng));
    let guard = 0;
    while (s.pending.length && guard++ < 400) epCycle(s, rng);
    return s;
  };

  // Code tracer (0002, 0003): the page's swap functions and the double loop replayed one
  // line (or one comparison) at a time, with the values and, for the swaps, the symbolic
  // expressions in a0 and b0.
  // swapTrace: `kind` is temp / arith / xor; `same` aliases the two cells (swap(v, i, i));
  // `bits` = 8 keeps the values modulo 256 (0 means unbounded integers).
  const SWAP_CODE = {
    temp: ["temp = v[i]", "v[i] = v[j]", "v[j] = temp"],
    arith: ["v[i] = v[i] + v[j]", "v[j] = v[i] - v[j]", "v[i] = v[i] - v[j]"],
    xor: ["v[i] = v[i] ^ v[j]", "v[j] = v[i] ^ v[j]", "v[i] = v[i] ^ v[j]"],
  };
  // A symbolic value is {p, q, r?}: p*a0 + q*b0 (+ r*c0) for arith (and temp), the xor
  // of the same terms for xor and the rotation.
  const symText = (sym, kind) => {
    const op = kind === "arith" || kind === "temp" ? " + " : " ^ ";
    const terms = [];
    const coef = (c, name) => (c === 1 ? name : `${c}·${name}`);
    if (sym.p) terms.push(coef(sym.p, "a0"));
    if (sym.q) terms.push(coef(sym.q, "b0"));
    if (sym.r) terms.push(coef(sym.r, "c0"));
    return terms.length ? terms.join(op) : "0";
  };
  const swapTrace = (kind, a, b, same = false, bits = 0) => {
    const wrap = (v) => (bits ? ((v % (1 << bits)) + (1 << bits)) % (1 << bits) : v);
    const cells = same ? [wrap(a)] : [wrap(a), wrap(b)];   // v[i] is cells[0], v[j] is cells[same ? 0 : 1]
    const syms = same ? [{ p: 1, q: 0 }] : [{ p: 1, q: 0 }, { p: 0, q: 1 }];
    const I = 0, J = same ? 0 : 1;
    let temp = null, tempSym = null;
    const combine = (x, y, op) => {
      if (kind === "xor") return { p: x.p ^ y.p, q: x.q ^ y.q };
      return op === "+" ? { p: x.p + y.p, q: x.q + y.q } : { p: x.p - y.p, q: x.q - y.q };
    };
    const snap = (line, text) => ({ line, text, a: cells[I], b: cells[J], temp, aSym: symText(syms[I], kind), bSym: symText(syms[J], kind), tempSym: tempSym === null ? null : symText(tempSym, kind) });
    const frames = [snap(-1, "")];
    if (kind === "temp") {
      temp = cells[I]; tempSym = syms[I]; frames.push(snap(0, `temp = ${cells[I]}`));
      cells[I] = cells[J]; syms[I] = syms[J]; frames.push(snap(1, `v[i] = ${cells[I]}`));
      cells[J] = temp; syms[J] = tempSym; frames.push(snap(2, `v[j] = ${cells[J]}`));
    } else {
      const op = kind === "xor" ? "^" : null;
      const apply = (line, target, x, y, o) => {
        const before = [cells[x], cells[y]];
        const raw = o === "^" ? cells[x] ^ cells[y] : o === "+" ? cells[x] + cells[y] : cells[x] - cells[y];
        cells[target] = wrap(raw); syms[target] = combine(syms[x], syms[y], o);
        frames.push(snap(line, `${before[0]} ${o} ${before[1]} = ${raw}${wrap(raw) !== raw ? ` → ${wrap(raw)} (mod ${1 << bits})` : ""}`));
      };
      apply(0, I, I, J, op || "+");
      apply(1, J, I, J, op || "-");
      apply(2, I, I, J, op || "-");
    }
    return { code: SWAP_CODE[kind], frames, ok: !same && cells[I] === wrap(b) && cells[J] === wrap(a), same };
  };
  // rotTrace: the follow-up rotation a <- b, b <- c, c <- a without a helper, as two XOR
  // swaps (a with b, then b with c): six lines, one frame each, with the values and the
  // symbolic expressions in a0, b0 and c0.
  const ROT_CODE = ["a = a ^ b", "b = a ^ b", "a = a ^ b", "b = b ^ c", "c = b ^ c", "b = b ^ c"];
  const ROT_STEPS = [["a", "b"], ["b", "a"], ["a", "b"], ["b", "c"], ["c", "b"], ["b", "c"]];   // target, other
  const rotTrace = (a, b, c, bits = 0) => {
    const wrap = (v) => (bits ? ((v % (1 << bits)) + (1 << bits)) % (1 << bits) : v);
    const v = { a, b, c }, sym = { a: { p: 1, q: 0, r: 0 }, b: { p: 0, q: 1, r: 0 }, c: { p: 0, q: 0, r: 1 } };
    const snap = (line, text) => ({ line, text, a: v.a, b: v.b, c: v.c, temp: null, aSym: symText(sym.a, "xor"), bSym: symText(sym.b, "xor"), cSym: symText(sym.c, "xor"), tempSym: null });
    const frames = [snap(-1, "")];
    ROT_STEPS.forEach(([t, o], line) => {
      const [x, y] = [t, o].sort(), before = [v[x], v[y]], raw = v[t] ^ v[o];   // printed in the order of the line
      v[t] = wrap(raw);
      sym[t] = { p: sym[t].p ^ sym[o].p, q: sym[t].q ^ sym[o].q, r: sym[t].r ^ sym[o].r };
      frames.push(snap(line, `${before[0]} ^ ${before[1]} = ${raw}`));
    });
    return { code: ROT_CODE, frames, ok: v.a === wrap(b) && v.b === wrap(c) && v.c === wrap(a) };
  };
  // loopTrace: the page's mystery(A), one comparison per frame; `endOfI` marks the last
  // comparison of an outer iteration, with the sorted prefix and the maximum noted.
  const LOOP_CODE = ["n = len(A)", "for i in range(n):", "    for j in range(n):", "        if A[i] < A[j]:", "            A[i], A[j] = A[j], A[i]"];
  const loopTrace = (A0) => {
    const A = [...A0], n = A.length, frames = [];
    let comparisons = 0, swaps = 0;
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        const before = [...A], swapped = A[i] < A[j];
        comparisons += 1;
        if (swapped) { const t = A[i]; A[i] = A[j]; A[j] = t; swaps += 1; }
        frames.push({ i, j, before, after: [...A], swapped, comparisons, swaps, endOfI: j === n - 1 });
      }
    }
    return { code: LOOP_CODE, frames, result: A, comparisons, swaps };
  };

  // A timing strip as WaveDrom, the format of the ```wavedrom blocks on the pages: one
  // lane per row, a character per slot ("." repeats the previous level or value), bus
  // values in `data`; a clock is "p…" per cycle, or "h"/"l" per slot on a half-cycle
  // strip; a flag row is a level that is high where the rule fails. Names lose their
  // markup. Rows that stop early (frames not reached yet) give a shorter lane.
  const plainText = (s) => String(s).replace(/<[^>]*>/g, "").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n))).replace(/&amp;/g, "&").replace(/\u200f/g, "").trim();
  const waveDromOf = (rows, N, opts = {}) => {
    const signal = rows.map((row) => {
      let len = N;
      if (row.values) { len = row.values.findIndex((v) => v === undefined || v === null); if (len < 0) len = Math.min(N, row.values.length); }
      const lane = { name: plainText(row.name) };
      if (row.kind === "clock") lane.wave = opts.half ? Array.from({ length: len }, (_, k) => (k % 2 ? "l" : "h")).join("") : len ? "p" + ".".repeat(len - 1) : "";
      else if (row.kind === "bus") {
        let wave = "";
        const data = [];
        for (let k = 0; k < len; k++) {
          if (k && !row.split && row.values[k] === row.values[k - 1]) wave += ".";
          else { wave += "="; data.push(plainText(row.values[k])); }
        }
        lane.wave = wave; lane.data = data;
      } else {
        let wave = "";
        for (let k = 0; k < len; k++) { const v = row.values[k] ? "1" : "0"; wave += k && v === (row.values[k - 1] ? "1" : "0") ? "." : v; }
        lane.wave = wave;
      }
      return lane;
    });
    const out = { signal };
    // the first tick as a string: WaveDrom 3.5 throws on a numeric tick when the strip has
    // a single slot; a windowed strip starts at its first column's own number
    if (opts.ticks && !opts.half) { const t0 = Number(opts.ticks(0)); out.head = { tick: String(Number.isFinite(t0) ? t0 : 0) }; }
    return out;
  };
  // WaveDrom text as the pages write it: one lane per line.
  const waveDromText = (wd) => {
    const lanes = wd.signal.map((l) => "  " + JSON.stringify(l)).join(",\n");
    const rest = Object.keys(wd).filter((k) => k !== "signal").map((k) => `,\n  ${JSON.stringify(k)}: ${JSON.stringify(wd[k])}`).join("");
    return `{ "signal": [\n${lanes}\n]${rest} }`;
  };

  const models = {
    mulberry32, waveDromOf, waveDromText,
    cakeSplit, cakeThreshold, cakeFormula, cakeBest,
    motorcyclePlan, motorcycleTime, motorcyclePhases, motorcyclePositions, motorcycleRiders, motorcycleAt, motorcycleTimeK, josephusRun, josephusSteps, josephusZero, josephusFormula,
    josephusKR, josephusSurvivor, josephusRecurrence, josephusSeats,
    clockCounts, clockMeetsIn, clockNext, clockPrev, clockLabel,
    stripImages, stripEdgePoint, stripPoint3, stripFacesBetween, stripLines, stripBest,
    hourglassSolve, hourglassInterval, hourglassReplay, hourglassReachable, hourglassStepN, hourglassSearch, hourglassReplayN, hourglassReachableN, probabilityAnswer,
    bridgeSolve, bridgeEscort, bridgeTime, bridgeEscortMoves, bridgePairMoves, riverSafe, riverMoves, riverPlan,
    pcieBoundaries, pcieBlocks, pcieSplits, pcieByCompletions, pcieCount, pcieS, pcieFormula,
    fifoSteps, fifoDepth, fifoFill, fifoEvents, fifoGrid, mtbfSeconds, mtbfHuman,
    TRI_TOTAL, triArcs, triClass, triCountC, triFrame, triIndex, triCounts, triArcCdf, triHistogram, polyArcs, polyClass, polyProb, polyProbDiscrete, polyRandom,
    permCycles, permHelper, permSwap, permWalk, permAllWin, permShuffle, permRandomPicks, permStrategyProb, permRandomProb,
    floydRho, floydTrace, floydRandom, floydParse, STATE_CODECS, bfs01Trace, bfs01Counts, abMultiple, abExists, bracketsClean, bracketsTrace,
    TTT_LINES, TTT_WRAP, tttCheck, tttFinalBoards, tttRandom,
    shapesOverlap, shapesCandidates, shapesOk, shapesTry, shapesRandom, shapesHeat,
    kapStep, kapChain, kapHistogram,
    EURO_RESULTS, EURO_PUBLIC_TOTAL, euroOrder, euroWithIsrael, euroCannotWin, euroScan,
    boxesCases, boxesDraw, boxesFix, boxesDeduce,
    EDGE_MODES, edgeTrace, lfsrNext, lfsrWalk, lfsrPeriod, lfsrPoly, lfsrTable, lfsrPrimitiveCount, div3Params, div3Trace, div3Duty,
    grayOf, grayToBin, bitsOf, graySample, grayFlags, grayFlagsOps, lfsrStrip,
    stockScan, stockRandom, hsCheck, HS_PRESETS, hsWave,
    AN_MOD, anInit, anApply, AN_SCRIPTS, anRun, anInvariants, anRandomScript, anEventLabel, crEventLabel, epStrip, CR_MOD, crDist, crInit, crCanTransmit, crApply, CR_SCRIPTS, crRun, crBalance, crInvariants, crRandomScript,
    EP_RCB, epUnitRng, epValueRng, epInit, epWrite, epReadBytes, epFragments, epRead, epNext, epCycle, EP_SCRIPTS, epRunScript,
    CAKE_MAX, cakeDone, SWAP_CODE, swapTrace, ROT_CODE, rotTrace, LOOP_CODE, loopTrace,
  };
  if (typeof module !== "undefined" && module.exports) {
    module.exports = models;
    return;
  }

  // --- drawing helpers ---------------------------------------------------------------

  const f = (v, n = 1) => Number(v).toFixed(n);
  const attr = (s) => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const ltr = (x) => `<bdi dir="ltr">${x}</bdi>`;   // math and numbers inside Hebrew text
  // Arrow keys on a focused point: +1 for right / up, -1 for left / down, ten times with Shift.
  const arrowStep = (e) => {
    const d = e.key === "ArrowRight" || e.key === "ArrowUp" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowDown" ? -1 : 0;
    return d * (e.shiftKey ? 10 : 1);
  };
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

  const chartFrame = frame;   // for views whose own `frame` is a number (the triangle enumeration)

  const hline = (fr, v, label) =>
    `<line class="ink-line" x1="${X0}" x2="${W - RIGHT}" y1="${f(fr.Y(v))}" y2="${f(fr.Y(v))}" ` +
    `stroke-width="1.5" stroke-dasharray="6 4"/>` +
    (label ? `<text class="legend" x="${X0 + 6}" y="${f(fr.Y(v) - 6)}">${label}</text>` : "");

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

  // --- views: one per kind ----------------------------------------------------------------

  // The cake box (0027, 0028): the law (arithmetic or geometric, with the same a), the two
  // sliders, and a stepper that adds one person at a time: the slice appears on the cake,
  // the row joins the table and the bar lights up. Play adds a person every moment.
  // --- shared controls ---------------------------------------------------------------------

  // A speed select (milliseconds per step) and the play loop of a stepper: the play
  // button toggles a timer that calls step() every speed.value ms until done(); pressed
  // at the end, restart() rewinds first. Returns stop(), for the other controls.
  // The seed of a box's random draws: a seed field and a "copy link" button inserted after
  // `after`; run(rng, seed) redraws with a seeded generator. draw() picks a new seed and
  // runs it, a typed seed replays, and `#seed-<kind>-<n>` in the URL replays on load (the
  // first box of that kind on the page). opts.seed fills the field without running.
  // opts.state = { get, set }: get() returns the box's state as a payload (or null to fall
  // back to the seed), the copy button then writes `#state-<kind>.<payload>` and set()
  // reopens it on load (true when the payload was valid).
  const SEED_HASH = /^#seed-([a-z0-9-]+)-(\d+)$/;
  const STATE_HASH = /^#state-([a-z0-9-]+)\.(.+)$/;
  const seedControls = (box, after, run, opts = {}) => {
    const kind = box.dataset.kind;
    const label = document.createElement("label");
    label.className = "ex-seedlab";
    label.innerHTML = `<span>זרע</span> <input type="number" class="ex-seed" min="1" max="${SEED_MAX}" step="1" dir="ltr" inputmode="numeric" aria-label="זרע ההגרלה, מספר לשחזור">`;
    const copy = document.createElement("button");
    copy.type = "button"; copy.className = "md-button ex-copy"; copy.textContent = "העתקת קישור";
    copy.title = opts.state ? "קישור שפותח את התיבה במצב הזה" : "קישור שפותח את התיבה עם אותו זרע";
    after.after(label, copy);
    const input = label.querySelector("input");
    if (opts.seed) input.value = opts.seed;
    const runSeed = (seed) => { input.value = seed; run(mulberry32(seed), seed); };
    const draw = () => runSeed(newSeed());
    input.addEventListener("change", () => { const v = Math.round(Number(input.value)); if (v >= 1 && v <= SEED_MAX) runSeed(v); else input.value = ""; });
    input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
    copy.addEventListener("click", () => {
      const payload = opts.state ? opts.state.get() : null;
      if (!payload && !input.value) draw();
      const url = `${location.origin}${location.pathname}#${payload ? `state-${kind}.${payload}` : `seed-${kind}-${input.value}`}`;
      const done = () => { copy.textContent = "הועתק ✓"; setTimeout(() => { copy.textContent = "העתקת קישור"; }, 1500); };
      const fallback = () => { window.prompt("הקישור:", url); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, fallback); else fallback();
    });
    const first = box === document.querySelector(`.explorer[data-kind="${kind}"]`);
    const m = SEED_HASH.exec(location.hash), sm = STATE_HASH.exec(location.hash);
    if (first && m && m[1] === kind) {
      runSeed(Number(m[2]));
      requestAnimationFrame(() => box.scrollIntoView({ block: "start" }));
    } else if (first && sm && sm[1] === kind && opts.state && opts.state.set(sm[2])) {
      requestAnimationFrame(() => box.scrollIntoView({ block: "start" }));
    }
    return { draw };
  };
  // The random traffic row of the two protocol boxes (0025, 0024): how many events and
  // the fault rate; the run button draws a new seed. `randNote` is the line under the box
  // once a random script runs: the counts, and whether the invariants held.
  const randomRow = (label, title) =>
    `<div class="ex-controls an-free an-random"><span class="ex-title">${title}</span>` +
    `<label>אירועים <select class="ex-count" aria-label="מספר האירועים">${[20, 50, 200].map((v) => `<option value="${v}"${v === 50 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
    `<label>${label} <input type="range" class="ex-rate" min="0" max="50" step="5" value="20" dir="ltr" aria-label="${label} באחוזים"><output class="out-rate">20%</output></label>` +
    `<button type="button" class="md-button md-button--primary ex-run">הרצה אקראית</button></div>`;
  const RAND_HASH = /^r(20|50|200)\.(\d+)\.(\d+)$/;
  // The event axis of 0025 / 0024: the states before every event in the history and the
  // current one, a column each (the last 64, ticks with the absolute event number).
  const EVENT_KEEP = 64;
  const eventStrip = (st, rowsOf, label, invariants) => {
    const states = st.history.map((h) => h.state).concat([st.state]);
    const logs = [st.history.length ? st.history[0].log : null].concat(st.history.slice(1).map((h) => h.log), st.history.length ? [st.log] : []);
    const base = st.dropped || 0, from = Math.max(0, states.length - EVENT_KEEP);
    const S = states.slice(from), Lg = logs.slice(from), n = S.length;
    const first = base + from;
    const rows = [{ name: "event", kind: "bus", split: true, values: Lg.map((l, i) => (first + i === 0 ? "start" : label(l))) }]
      .concat(rowsOf(S), [{ name: "✗", kind: "flag", values: S.map((s) => (invariants(s).length ? 1 : 0)) }]);
    return waveStrip(rows, n, { slotW: 52, labelW: 92, cursor: n - 1, ticks: (k) => first + k, label: `ציר האירועים: ${n} עמודות` });
  };
  const randNote = (rd, seed, faults, names, checks) => {
    const v = rd.violation;
    return `תנועה אקראית מהזרע ${ltr(seed)}: ${ltr(rd.count)} אירועים בשיעור ${ltr(`${Math.round(rd.rate * 100)}%`)}, ${faults}. ${checks} ` +
      (v ? `<span class="wv-bad">✗ אחרי אירוע ${ltr(v.index)} הופר: ${v.names.map((n) => names[n]).join(", ")}; התסריט נעצר שם.</span>` : `<span class="wv-ok">✓ אף אחד מהם לא הופר לאורך כל התסריט.</span>`) +
      ` אותו זרע נותן את אותו תסריט; "הצעד הקודם" חוזר אחורה.`;
  };
  const speedSel = (slow, mid, fast) =>
    `<label>הקצב <select class="ex-speed"><option value="${slow}">איטי</option><option value="${mid}" selected>בינוני</option><option value="${fast}">מהיר</option></select></label>`;
  const autoplay = (play, speed, { step, done, restart }) => {
    let timer = null;
    const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
    play.addEventListener("click", () => {
      if (timer) { stop(); return; }
      if (done()) restart();
      if (done()) return;
      play.textContent = "עצירה";
      timer = setInterval(() => { step(); if (done()) stop(); }, Number(speed.value));
    });
    speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
    return stop;
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
        `<p class="ex-summary" aria-live="polite"></p><p class="ex-note cake-note"></p><div class="cake-charts"></div>`;
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
        const flushTiny = () => { if (tiny) slice(tiny.from, c, "cake-tiny", `אנשים ${tiny.k0} עד ${tiny.k1}: יחד ${fmt(c - tiny.from, 4)} מהעוגה`); tiny = null; };
        rows.slice(0, st.shown).forEach((r) => {
          const from = c, to = Math.min(c + r.S, 1);
          c = to;
          if (r.S < 0.001 && !peak.includes(r.k)) { if (tiny) tiny.k1 = r.k; else tiny = { from, k0: r.k, k1: r.k }; return; }
          flushTiny();
          const cls = peak.includes(r.k) ? "cake-peak" : r.k % 2 ? "cake-slice" : "cake-slice2";
          slice(from, to, cls + (r.k === st.shown ? " is-now" : ""), `אדם ${r.k}: p = ${fmt(r.p, pd())}, S = ${fmt(r.S, pd() + 1)}`, r.k);
        });
        flushTiny();
        s += `<circle class="cake-edge" cx="${C}" cy="${C}" r="${R}" fill="none"/>`;
        return s + "</svg>";
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
          : n >= CAKE_MAX ? `העוגה לא נגמרת: השברים לא עולים, ואחרי ${ltr(CAKE_MAX)} אנשים עדיין נשאר ${ltr(fmt(left, P + 1))} ממנה. `
          : `השברים מתכווצים: מהאדם ה-${n + 1} השבר כבר אפסי (קטן מ-${ltr("10⁻⁹")}) או שלילי, ו-${ltr(fmt(left, P + 1))} מהעוגה נשאר בלי לוקח. `;
        const threshold = grows
          ? `הסף הוא ${ltr(`T ≈ ${fmt(T)}`)}, והנוסחה נותנת את האדם ה-${fm.k}${fm.tie ? " (תיקו עם הבא)" : ""}${agree ? ", בדיוק כמו בעמודות." : ", שלא כמו בעמודות."} `
          : `אין סף: כשהשברים לא עולים (${ltr(st.kind === "arith" ? "d ≤ 0" : "q ≤ 1")}) גם השבר וגם מה שנשאר רק קטנים, ולכן האדם הראשון מקבל הכי הרבה. `;
        summary.innerHTML = `בחוק ${SL[st.kind].law}: המקבל הגדול הוא ${who}, עם ${ltr(fmt(rows[peak[0] - 1].S, P + 1))} מהעוגה, ${ending}` + threshold +
          `להשוואה, בחוק ${SL[other].law} עם אותו ${ltr("a")} ו-${ltr(`${SL[other].name.split(" ")[1]} = ${st.step[other]}`)}: האדם ה-${opeak[0]} עם ${ltr(fmt(orows[opeak[0] - 1].S, P + 1))}, מתוך ${orows.length}.`;
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

  const motorcycleView = () => ({
    mount(box) {
      const defaults = { t0: Number(box.dataset.t0 || 13), t1: Number(box.dataset.t1 || 1), k: 2, km: null, cmp: "none" };
      const st = { ...defaults, strategy: "optimal", t: 0 };
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
        `<span class="viz-legend road-legend"></span>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), scrub = $(".ex-t"), summary = $(".ex-summary");
      const road = $(".road-box"), chart = $(".road-chart"), strategy = $(".ex-strategy"), cmpSel = $(".ex-cmp");
      let running = false, last = 0;
      const alpha = () => st.t0 / st.t1;
      const planOf = (s) => motorcycleRiders(s, alpha(), st.k);
      const plan = () => planOf(st.strategy);
      const who = (i) => (i === 0 ? "האופנוע" : st.k === 1 ? "הנוסע" : st.k === 2 ? ["הנוסע", "ההולך"][i - 1] : `נוסע ${i}`);
      const dist = (v) => (st.km === null ? fmt(v) : `${fmt(v * st.km, 1)} ק"מ`);
      const roadSvg = (pos, pl) => {
        const w = 640, h = 96, x0 = 36, x1 = 604, yr = 58;
        const X = (v) => x0 + v * (x1 - x0);
        let s = `<svg class="figure road-live" viewBox="0 0 ${w} ${h}" role="img" aria-label="הדרך מ-A ל-B עם האופנוע והנוסעים במקומם בזמן הנוכחי">` +
          `<line class="axis-c" x1="${x0}" x2="${x1}" y1="${yr}" y2="${yr}" stroke-width="3"/>` +
          `<text class="legend" x="${x0}" y="${yr + 24}" text-anchor="middle">A</text><text class="legend" x="${x1}" y="${yr + 24}" text-anchor="middle">B</text>`;
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
        s += `<circle class="ink-dot" cx="${f(X(bike))}" cy="${yr}" r="9" fill-opacity="0.45"><title>האופנוע: ${dist(bike)}</title></circle>`;
        pos.slice(1).forEach((v, i) => {
          const onBike = Math.abs(v - bike) < 1e-9, side = i % 2 ? 1 : -1, lift = onBike ? (14 + 8 * Math.floor(i / 2)) * side : 0;
          s += `<circle class="${CLS[i]}-dot" cx="${f(X(v))}" cy="${f(yr + lift)}" r="6"><title>${who(i + 1)}: ${dist(v)}${onBike ? " (על האופנוע)" : ""}</title></circle>`;
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
      const draw = () => {
        $(".out-t0").textContent = String(st.t0); $(".out-t1").textContent = String(st.t1); $(".out-k").textContent = String(st.k);
        strategy.querySelectorAll("option").forEach((o) => { o.textContent = name(o.value); });
        cmpSel.querySelectorAll("option").forEach((o) => { if (o.value !== "none") o.textContent = name(o.value); });
        $(".road-title").textContent = st.km === null ? "המקום על הדרך (0 הוא A ו-1 הוא B) מול הזמן בשעות" : `המקום על הדרך בק"מ (0 הוא A ו-${st.km} הוא B) מול הזמן בשעות`;
        $(".road-legend").innerHTML = `<span><i class="ink" style="opacity:0.4"></i>האופנוע</span>` + Array.from({ length: st.k }, (_, i) => `<span><i class="${CLS[i]}"></i>${who(i + 1)}</span>`).join("") +
          (st.cmp !== "none" ? `<span><i class="ink-dash"></i>להשוואה: ${name(st.cmp)}</span>` : "");
        const a = alpha();
        if (a <= 1 + EPS) {
          road.innerHTML = ""; chart.innerHTML = "";
          summary.innerHTML = `יחס המהירויות ${ltr(`α = ${f(a, 2)}`)}: האופנוע לא מהיר מההליכה, ולכן כולם פשוט הולכים, ${fmt(st.t0, 2)} שעות.`;
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
          `(להשוואה: ${Object.keys(NAMES).map((s) => `${name(s)} ${fmt(T[s] * st.t1, 2)}`).join(", ")}). `;
        if (st.strategy === "optimal") {
          const ride = pl.ride;
          text += st.k === 2
            ? `הנוסע יורד אחרי ${ltr(dist(motorcyclePlan(a).D))} מהדרך, וכל אחד מהשניים הולך ${ltr(dist(motorcyclePlan(a).y + motorcyclePlan(a).x))} ממנה. `
            : `הנוסחה: ${ltr(`((2n − 1)α + 1) / (α + 2n − 1) · t1 = ${fmt(motorcycleTimeK(a, st.k) * st.t1, 2)}`)} שעות עם ${ltr(`n = ${st.k}`)}; כל נוסע נוסע ${ltr(dist(ride))} והולך ${ltr(dist(1 - ride))}. `;
        }
        if (st.km !== null) text += `מהירויות: הליכה ${ltr(fmt(st.km / st.t0, 1))} קמ"ש, נסיעה ${ltr(fmt(st.km / st.t1, 1))} קמ"ש. `;
        if (other) text += `בתוכנית להשוואה (מקווקו) ${people} מגיעים אחרי ${fmt(other.T * st.t1, 2)} שעות, ${other.T > pl.T ? `${fmt((other.T - pl.T) * st.t1, 2)} שעות יותר` : other.T < pl.T ? `${fmt((pl.T - other.T) * st.t1, 2)} שעות פחות` : "אותו זמן"}. `;
        const seg = pl.times.filter((u) => u <= st.t + 1e-12).length;
        text += `עכשיו (שלב ${ltr(Math.max(1, Math.min(seg, pl.times.length - 1)))}): ${pos.map((v, i) => `${who(i)} ב-${ltr(dist(v))}`).join(", ")}.`;
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
      strategy.addEventListener("change", () => { st.strategy = strategy.value; draw(); });
      cmpSel.addEventListener("change", () => { st.cmp = cmpSel.value; draw(); });
      $(".ex-reset").addEventListener("click", () => {
        stop(); Object.assign(st, defaults, { strategy: "optimal", t: 0 });
        $(".ex-t0").value = st.t0; $(".ex-t1").value = st.t1; $(".ex-k").value = 2; $(".ex-km").value = ""; strategy.value = "optimal"; cmpSel.value = "none"; draw();
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
      const nmax = Number(box.dataset.nmax || 64), NBIG = 1000000, NCIRCLE = 128;
      const defaults = { n: Number(box.dataset.n || 20), l: Number(box.dataset.l || 2), rule: "page" };
      const st = { ...defaults, s: 0, seat: null };
      // rule "josephus" (0016 only): keep 2, remove 1, no closed form
      const jos = () => st.rule === "josephus";
      const keepRemove = () => (jos() ? [2, 1] : [1, st.l - 1]);
      const runFast = (n) => josephusSurvivor(n, ...keepRemove());
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>מספר האנשים N</span><input type="range" class="ex-n" min="1" max="${nmax}" step="1" value="${st.n}" dir="ltr"><output class="out-n"></output>` +
        `<input type="number" class="ex-num ex-nbig" min="1" max="${NBIG}" step="1" value="${st.n}" dir="ltr" aria-label="מספר האנשים, עד מיליון"></label>` +
        (withL ? "" : `<label>הכלל <select class="ex-rule" aria-label="כלל היציאה"><option value="page">אחד נשאר, אחד יוצא (השאלה)</option><option value="josephus">שניים נשארים, אחד יוצא (הגרסה של יוסף)</option></select></label>` +
          `<button type="button" class="md-button ex-41">41 אנשים, הגרסה של יוסף</button>`) +
        (withL ? `<label><span>הכלל ${ltr("L")}: אחד נשאר, ${ltr("L − 1")} יוצאים</span><input type="range" class="ex-l" min="2" max="${box.dataset.lmax}" step="1" value="${st.l}" dir="ltr"><output class="out-l"></output></label>` : "") +
        `<label><input type="checkbox" class="ex-mark" checked> להדגיש את השורד מההתחלה</label>` +
        `<label>המושב <input type="number" class="ex-num ex-seat" min="0" step="1" dir="ltr" placeholder="s" aria-label="מושב לחיפוש הפוך: לאילו N הוא שורד"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1200">איטי</option><option value="500" selected>בינוני</option><option value="150">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<span class="ex-pos"></span></div>` +
        `<div class="jos-box"><div class="jos-circle"></div><div class="jos-panel"><p class="jos-now"></p><p class="jos-order"></p></div></div>` +
        `<p class="ex-summary" aria-live="polite"></p><p class="ex-note jos-seat"></p><p class="ex-title">השורד לכל N, עם N הנבחר מודגש; נקודות שחורות הן נקודות אפס</p><div class="jos-chart"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), mark = $(".ex-mark");
      let timer = null, chartFor = "";
      const circleSvg = (n, out, stays, leave, winner) => {   // stays: the people who stay in this step
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
          const cls = i === winner ? "st-ok" : leave.includes(i) ? "st-bad" : stays.includes(i) ? "st-stack" : out.has(i) ? "st-done" : "st-cell";
          const faded = out.has(i) && !leave.includes(i) ? ' class="st-faded"' : "";
          s += `<g${faded}><circle class="${cls}" cx="${f(x)}" cy="${f(y)}" r="${r}"><title>אדם ${i}</title></circle>`;
          if (small !== " st-none") s += `<text class="st-text${small}" x="${f(x)}" y="${f(y + (small ? 4 : 5))}" text-anchor="middle">${i}</text>`;
          if (out.has(i)) { const dd = Math.max(r - 3, 3); s += `<line class="pg-strike" x1="${f(x - dd)}" y1="${f(y + dd)}" x2="${f(x + dd)}" y2="${f(y - dd)}"/>`; }
          s += "</g>";
        }
        s += `<text class="st-text" x="${cx}" y="${cy + 6}" text-anchor="middle">${n - out.size}</text></svg>`;
        return s;
      };
      const chartSvg = (n, seat) => {
        const vals = Array.from({ length: nmax }, (_, i) => runFast(i + 1));
        const ymax = Math.max(nmax, 1), step = ymax > 40 ? 16 : 8, ticks = [];
        for (let v = 0; v <= ymax; v += step) ticks.push(v);
        const fr = frame("השורד לכל גודל מעגל", nmax, ymax, ticks);
        let s = fr.s;
        vals.forEach((v, i) => {
          const k = i + 1, cls = k === n ? "s2-dot" : v === 0 ? "ink-dot" : "s1-dot";
          if (seat !== null && v === seat) s += `<circle class="jos-seat-ring" cx="${f(fr.cx(k))}" cy="${f(fr.Y(v))}" r="8"/>`;
          s += `<circle class="${cls}" cx="${f(fr.cx(k))}" cy="${f(fr.Y(v))}" r="${k === n ? 6 : Math.min(4, fr.slot * 0.4).toFixed(1)}"><title>N = ${k}: ${v}</title></circle>`;
          const nearN = k !== n && Math.abs(k - n) < fr.every;   // a tick that would overlap the chosen N's
          if (k === n || (!nearN && (k % fr.every === 0 || k === 1))) s += fr.xtick(k);
        });
        return s + fr.close();
      };
      const digitsIn = (v, base) => v.toString(base);
      const people = (nums) => nums.length === 1 ? String(nums[0]) : `${nums.slice(0, -1).join(", ")} ו-${nums[nums.length - 1]}`;
      const draw = () => {
        const n = st.n, L = st.l, big = n > NCIRCLE;
        $(".out-n").textContent = String(n); $(".ex-nbig").value = n; $(".ex-n").value = Math.min(n, nmax);
        if (withL) $(".out-l").textContent = String(L);
        // the circle and the steps up to NCIRCLE people; above that only the numbers
        const [keep, remove] = keepRemove();
        const { steps, survivor } = big ? { steps: [], survivor: runFast(n) } : josephusKR(n, keep, remove);
        st.s = Math.min(Math.max(st.s, 0), steps.length);
        const out = new Set();
        steps.slice(0, st.s).forEach(([, leave]) => leave.forEach((p) => out.add(p)));
        const cur = st.s > 0 ? steps[st.s - 1] : null;
        const done = st.s >= steps.length;
        const winner = done || mark.checked ? survivor : null;
        $(".jos-box").hidden = big;
        $(".ex-play-row").hidden = big;
        if (!big) {
          const stays = cur ? cur[0] : [];
          $(".jos-circle").innerHTML = circleSvg(n, out, stays, cur ? cur[1] : [], winner);
          const rule = jos() ? "נשאר, גם הבא אחריו, והשלישי יוצא" : L === 2 ? "נשאר, והבא אחריו יוצא" : `נשאר, ו-${L - 1} הבאים אחריו יוצאים`;
          let round = 0, prev = null;
          steps.slice(0, Math.max(st.s, 1)).forEach(([st0]) => { if (prev === null || st0[0] <= prev) round += 1; prev = st0[0]; });
          const stayText = stays.length === 1 ? `אדם ${stays[0]} נשאר` : `אנשים ${people(stays)} נשארים`;
          const leaveText = cur ? (cur[1].length === 1 ? `ואדם ${cur[1][0]} יוצא` : `ואנשים ${people(cur[1])} יוצאים`) : "";
          $(".jos-now").innerHTML = st.s === 0 ? `${n} אנשים במעגל. מתחילים מאדם 0: הוא ${rule}. המספר במרכז הוא כמה אנשים נשארו.`
            : done && steps.length === st.s ? `צעד ${st.s}: ${stayText}, ${leaveText}. נשאר אדם ${survivor}, והוא השורד.`
            : `צעד ${st.s}, סיבוב ${round}: ${stayText}, ${leaveText}.`;
          const order = steps.slice(0, st.s).flatMap(([, leave]) => leave);
          $(".jos-order").innerHTML = order.length ? `סדר היציאה (${ltr(order.length)} מתוך ${ltr(n - 1)}): ` +
            order.map((p, i) => `<span class="jos-chip${i >= order.length - (cur ? cur[1].length : 0) ? " is-now" : ""}">${p}</span>`).join(" ") : "עוד אף אחד לא יצא.";
          $(".ex-pos").textContent = `צעד ${st.s} מתוך ${steps.length}`;
          $(".ex-prev").disabled = st.s <= 0; $(".ex-next").disabled = done;
        }
        const sim = survivor, how = big ? "בסימולציה ברשימה מקושרת" : "בסימולציה";
        let text;
        if (jos()) {
          const rec = josephusRecurrence(n);
          text = `בגרסה של יוסף (שניים נשארים, אחד יוצא) עם ${ltr(`N = ${n}`)}: השורד הוא ${sim} ${how} (${ltr(sim + 1)} במספור מ-1), והנסיגה ` +
            `${ltr("f(m) = (f(m − 1) + 3) mod m")} נותנת ${rec}${rec === sim ? ", אותו דבר" : ", שלא כמו בסימולציה"}. לכלל הזה אין נוסחה סגורה כמו ${ltr("2r")}: הנסיגה עוברת על כל ${ltr("m")}.`;
        } else {
          const form = josephusFormula(n, L), M = josephusZero(n, L);
          text = `עם ${ltr(`N = ${n}`)} ו-${ltr(`L = ${L}`)} השורד הוא ${sim} ${how}, והנוסחה ` +
            `${ltr(`${L}(N − M) / ${L - 1}`)} עם נקודת האפס ${ltr(`M = ${M}`)} נותנת ${form}` +
            `${sim === form ? ", אותו דבר." : ", שלא כמו בסימולציה."}` +
            (L === 2 ? ` בבינארי: ${ltr(`N = ${digitsIn(n, 2)}`)}, והשורד ${ltr(digitsIn(sim, 2))}.`
              : L === 3 ? ` בבסיס 3: ${ltr(`N = ${digitsIn(n, 3)}`)}, והשורד ${ltr(digitsIn(sim, 3))}.` : "");
        }
        $(".ex-summary").innerHTML = text + (big ? ` המעגל והצעדים מצוירים עד ${ltr(NCIRCLE)} אנשים.` : "");
        // the reverse lookup: in which circles does seat s survive
        let seatText = "";
        if (st.seat !== null) {
          const ns = josephusSeats(st.seat, jos() ? null : L, 5);
          seatText = ns.length === 0
            ? `המושב ${ltr(st.seat)} לא שורד באף מעגל${jos() ? " עד מיליון אנשים" : L === 2 ? ": השורד תמיד זוגי" : `: השורד תמיד כפולה של ${ltr(L)}`}.`
            : `המושב ${ltr(st.seat)} שורד כש-${ltr("N")} הוא ${ltr(ns.join(", "))}${ns.length === 5 ? ", …" : ""}` +
              (jos() ? " (לפי הנסיגה)." : L === 2 ? ` (כל ${ltr("N = 2^k + s/2")} עם ${ltr("2^k > s/2")}).` : ` (כל ${ltr("N = M + s(L − 1)/L")} עם נקודת אפס ${ltr("M")} מתאימה).`) +
              (ns.some((v) => v <= nmax) ? " בגרף הם מוקפים." : "");
        }
        $(".jos-seat").innerHTML = seatText;
        const key = `${n}/${L}/${st.rule}/${st.seat}`;
        if (chartFor !== key) { chartFor = key; $(".jos-chart").innerHTML = chartSvg(n, st.seat); }
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => (st.n > NCIRCLE ? 0 : josephusKR(st.n, ...keepRemove()).steps.length);
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
      $(".ex-nbig").addEventListener("change", () => { const v = Math.round(Number($(".ex-nbig").value)); if (!Number.isFinite(v) || v < 1) { $(".ex-nbig").value = st.n; return; } stop(); st.n = Math.min(NBIG, v); st.s = 0; draw(); });
      $(".ex-seat").addEventListener("change", () => { const v = Math.round(Number($(".ex-seat").value)); stop(); st.seat = $(".ex-seat").value === "" || !Number.isFinite(v) || v < 0 ? null : v; draw(); });
      [$(".ex-nbig"), $(".ex-seat")].forEach((el) => el.addEventListener("keydown", (e) => { if (e.key === "Enter") el.blur(); }));
      if (withL) $(".ex-l").addEventListener("input", () => { stop(); st.l = Number($(".ex-l").value); st.s = 0; draw(); });
      if (!withL) {
        $(".ex-rule").addEventListener("change", () => { stop(); st.rule = $(".ex-rule").value; st.s = 0; draw(); });
        $(".ex-41").addEventListener("click", () => { stop(); st.rule = "josephus"; $(".ex-rule").value = "josephus"; st.n = 41; st.s = 0; draw(); });
      }
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, defaults, { s: 0, seat: null }); $(".ex-n").value = st.n; $(".ex-seat").value = ""; if (withL) $(".ex-l").value = st.l; else $(".ex-rule").value = "page"; draw(); });
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
      const defaults = { A: Number(box.dataset.a || 7), B: Number(box.dataset.b || 11), D: Number(box.dataset.d || (interval ? 1 : 15)), C: null, objective: "page" };
      const st = { ...defaults, s: 0 };
      // sizes: [A, B] or [A, B, C]; the page's objective ("page": fewest events on 0018,
      // the earliest end on 0019) or the fewest flips of the follow-up
      const sizes = () => (st.C === null ? [st.A, st.B] : [st.A, st.B, st.C]);
      const LET = "ABC";
      box.innerHTML =
        `<div class="ex-controls">` +
        [["A", "שעון A (דקות)", 1, 30], ["B", "שעון B (דקות)", 1, 30], ["D", "המטרה D (דקות)", 1, 60]].map(([k, label, min, max]) =>
          `<label><span>${label}</span><input type="range" class="ex-${k}" min="${min}" max="${max}" step="1" value="${st[k]}" dir="ltr"><output class="out-${k}"></output></label>`).join("") +
        `<label>שעון C (דקות, ריק = בלי) <input type="number" class="ex-num ex-C" min="1" max="30" step="1" dir="ltr" placeholder="–" aria-label="שעון חול שלישי בדקות, ריק בלי שעון שלישי"></label>` +
        `<label>המטרה <select class="ex-obj" aria-label="מטרת החיפוש"><option value="page">${interval ? "הסיום המוקדם ביותר (השאלה)" : "הכי מעט אירועים (השאלה)"}</option><option value="flips">הכי מעט היפוכים</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<div class="hg-axis"></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button ex-prev">האירוע הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">האירוע הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1100, 400) + `<span class="ex-pos"></span></div>` +
        `<div class="hg-frame"></div><p class="hg-caption"></p><p class="ex-note hg-compare"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play");
      let timer = null, uid = 0;
      const HEB = (act) => (act ? `הופכים את ${[...act].join(" ואת ")}` : "לא הופכים כלום");
      const plus = (act) => [...act].join("+");
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
      const group = (x, y, tops) => tops.map((v, i) => glass(x + 64 * i, y, v, sizes()[i], "abc"[i])).join("");
      const frameSvg = (ev, measuring, verdict) => {
        const [t, act, before, after] = ev, cy = 12 + 25, n = sizes().length, gw = 64 * (n - 1) + 30;
        const left = 92 - (n - 2) * 40, ax0 = left + gw + 22, ax1 = ax0 + 84, right = ax1 + 30, W = right + gw + 30;
        let s = `<svg class="figure hourglass-fig" viewBox="0 0 ${W} 92" style="max-width:${(W / 16).toFixed(0)}rem" role="img" aria-label="אירוע ברגע ${t}">`;
        if (measuring) s += `<rect class="measure" x="2" y="2" width="${W - 4}" height="88" rx="6"/>`;
        s += `<text class="legend" x="10" y="${cy - 4}" font-weight="700">t = ${t}</text><text class="tick" x="10" y="${cy + 14}">${verdict.event}</text>` + group(left, 12, before);
        if (after === null) s += `<text class="legend" x="${ax0 + 4}" y="${cy + 5}" font-weight="700">${verdict.text}</text>`;
        else s += `<line class="ink-line" x1="${ax0}" y1="${cy}" x2="${ax1}" y2="${cy}" stroke-width="1.5"/><polygon class="ink-fill" points="${ax1 + 6},${cy} ${ax1 - 2},${cy - 4} ${ax1 - 2},${cy + 4}"/>` +
                  `<text class="legend" x="${(ax0 + ax1) / 2}" y="${cy - 8}" text-anchor="middle">${verdict.text}</text>` + group(right, 12, after);
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
               (act ? `<text class="legend" x="${f(X(t))}" y="${y - 14}" text-anchor="middle" style="font-size:11px">${plus(act)}</text>` : "");
        });
        return s + "</svg>";
      };
      // the page's code for two hourglasses and the page's objective; the general search otherwise
      const solveFor = (objective) => {
        const sz = sizes();
        if (objective === "page" && sz.length === 2) {
          let res;
          if (interval) { const r = hourglassInterval(st.A, st.B, st.D); res = r ? { start: r.start, plan: r.plan, end: r.start + st.D } : null; }
          else { const plan = hourglassSolve(st.A, st.B, st.D); res = plan ? { start: 0, plan, end: st.D } : null; }
          if (res) { res.events = res.plan.length; res.flips = res.plan.reduce((c, [, act]) => c + act.length, 0); res.explored = null; }
          return res;
        }
        return hourglassSearch(sz, st.D, { interval, objective: objective === "page" ? (interval ? "time" : "events") : "flips" });
      };
      const solve = () => solveFor(st.objective);
      const replay = (res) => hourglassReplayN(sizes(), res.plan, res.end);
      const reach = () => hourglassReachableN(sizes(), 60);
      const draw = () => {
        ["A", "B", "D"].forEach((k) => { $(`.out-${k}`).textContent = String(st[k]); });
        const res = solve(), sz = sizes(), names = sz.map((v, i) => `${LET[i]} = ${v}`);
        const sizesText = sz.length === 2 ? `${ltr(st.A)} ו-${ltr(st.B)}` : `${ltr(st.A)}, ${ltr(st.B)} ו-${ltr(st.C)}`;
        const summary = $(".ex-summary");
        if (!res) {
          const g = (u, v) => (v ? g(v, u % v) : u), gAll = sz.reduce(g);
          st.s = 0;
          summary.innerHTML = `עם שעונים של ${sizesText} דקות אי אפשר למדוד ${ltr(st.D)} דקות${interval ? "" : " מרגע 0"}` +
            (st.D % gAll ? `: ‏${ltr(st.D)} איננו כפולה של ${ltr(`gcd(${sz.join(", ")}) = ${gAll}`)}.` : ".") +
            (interval ? "" : ` מרגע 0 אפשר למדוד: ${ltr(reach().join(", "))} (עד 60).`);
          $(".hg-axis").innerHTML = ""; $(".hg-frame").innerHTML = ""; $(".hg-caption").textContent = ""; $(".ex-pos").textContent = ""; $(".hg-compare").textContent = "";
          $(".ex-prev").disabled = $(".ex-next").disabled = true;
          return;
        }
        const events = replay(res);
        st.s = Math.min(Math.max(st.s, 0), events.length - 1);
        const flips = res.plan.map(([t, act]) => `${ltr(t)}: ${HEB(act)}`).join("; ");
        summary.innerHTML = (interval ? `${st.objective === "page" ? "המדידה שמסתיימת הכי מוקדם" : "המדידה עם הכי מעט היפוכים"}: מרגע ${ltr(res.start)} עד רגע ${ltr(res.end)}, ‏${ltr(`${res.end} − ${res.start} = ${st.D}`)}. ` : `מודדים ${ltr(st.D)} דקות מרגע 0 ב-${ltr(events.length - 1)} אירועים${st.objective === "page" ? "" : ` ו-${ltr(res.flips)} היפוכים`}. `) +
          `התוכנית: ${flips}.` + (interval ? "" : ` מרגע 0 אפשר למדוד גם: ${ltr(reach().filter((v) => v !== st.D).slice(0, 12).join(", "))}, ...`);
        // the other objective, for comparison
        const other = solveFor(st.objective === "page" ? "flips" : "page");
        const describe = (r) => (interval ? `מסתיימת ברגע ${ltr(r.end)}, ${ltr(r.events)} אירועים ו-${ltr(r.flips)} היפוכים` : `${ltr(r.events)} אירועים ו-${ltr(r.flips)} היפוכים`);
        $(".hg-compare").innerHTML = `התוכנית הזו: ${describe(res)}. ` +
          (other ? `במטרה האחרת (${st.objective === "page" ? "הכי מעט היפוכים" : interval ? "הסיום המוקדם ביותר" : "הכי מעט אירועים"}): ${describe(other)}${other.flips === res.flips && other.events === res.events && other.end === res.end ? ", אותו דבר" : ""}.` : "") +
          (res.explored !== null ? ` החיפוש בדק ${ltr(res.explored)} מצבים${sz.length === 3 ? " (עם שעון שלישי: 8 אפשרויות בכל אירוע)" : ""}.` : "");
        $(".hg-axis").innerHTML = axisSvg(events, interval ? res.start : null, res.end);
        const ev = events[st.s], [t, act, before, after] = ev;
        // which hourglasses ran out: those whose sand on top after the previous action equals the wait
        const prevEv = st.s > 0 ? events[st.s - 1] : null;
        const out = [];
        if (prevEv) { const w = t - prevEv[0]; prevEv[3].forEach((v, i) => { if (v === w) out.push(LET[i]); }); }
        const what = st.s === 0 ? "start" : `${out.join(" + ")} run${out.length === 1 ? "s" : ""} out`;
        const ran = st.s === 0 ? "התחלה" : out.length > 1 ? `שעונים ${out.join(" ו-")} נגמרים` : `שעון ${out[0]} נגמר`;
        const done = st.s === events.length - 1;
        const flip = act ? `flip ${[...act].join(" + ")}` : "";
        let verdict;
        if (done) verdict = { event: what, text: interval ? `STOP ✓ ${res.end} − ${res.start} = ${st.D}` : `✓ D = ${st.D}` };
        else if (interval && t === res.start) verdict = { event: what, text: flip ? `START, ${flip}` : "START" };
        else verdict = { event: what, text: flip || "wait" };
        $(".hg-frame").innerHTML = frameSvg(ev, interval && t >= res.start, verdict);
        const tops = (arr) => ltr(arr.map((v, i) => `${LET[i]} = ${v}`).join(", "));
        $(".hg-caption").innerHTML = `רגע ${ltr(t)}: ${ran}. חול למעלה: ${tops(before)}. ` +
          (done ? (interval ? `מסיימים: נמדדו ${ltr(st.D)} דקות מרגע ${ltr(res.start)}.` : `עברו בדיוק ${ltr(st.D)} דקות מרגע 0.`)
            : `${interval && t === res.start ? "מתחילים למדוד, ו" : ""}${HEB(act)}${act ? `; אחרי ההיפוך למעלה ${tops(after)}` : ""}.`);
        void names;
        $(".ex-pos").textContent = `אירוע ${st.s + 1} מתוך ${events.length}`;
        $(".ex-prev").disabled = st.s <= 0; $(".ex-next").disabled = done;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const count = () => { const r = solve(); return r ? replay(r).length : 0; };
      $(".ex-next").addEventListener("click", () => { stop(); st.s += 1; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s -= 1; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (!count()) return;
        if (st.s >= count() - 1) st.s = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { if (st.s >= count() - 1) { stop(); return; } st.s += 1; draw(); }, Number($(".ex-speed").value));
        draw();
      });
      $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      ["A", "B", "D"].forEach((k) => $(`.ex-${k}`).addEventListener("input", () => { stop(); st[k] = Number($(`.ex-${k}`).value); st.s = 0; draw(); }));
      $(".ex-C").addEventListener("change", () => {
        const v = Math.round(Number($(".ex-C").value));
        stop(); st.C = $(".ex-C").value.trim() === "" || !Number.isFinite(v) || v < 1 ? null : Math.min(30, v); $(".ex-C").value = st.C === null ? "" : st.C; st.s = 0; draw();
      });
      $(".ex-C").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".ex-C").blur(); });
      $(".ex-obj").addEventListener("change", () => { stop(); st.objective = $(".ex-obj").value; st.s = 0; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, defaults, { s: 0 }); ["A", "B", "D"].forEach((k) => { $(`.ex-${k}`).value = st[k]; }); $(".ex-C").value = ""; $(".ex-obj").value = "page"; draw(); });
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
      const PLANS = { best: "החיפוש (הקצרה ביותר)", escort: "המהיר מלווה את כולם", pair: "שני האיטיים חוצים יחד" };
      const st = { times: [], s: 0, cap: 2, plan: "best" };
      box.innerHTML =
        `<div class="ex-controls"><label>הזמנים (עד שמונה) <input type="text" class="ex-times" value="${defaults}" size="22" dir="ltr" inputmode="numeric" aria-label="זמני החצייה, מופרדים ברווחים"></label>` +
        `<label>הגשר מחזיק <select class="ex-cap" aria-label="כמה אנשים הגשר מחזיק"><option value="2" selected>שניים</option><option value="3">שלושה</option></select></label>` +
        `<label>התוכנית <select class="ex-plan" aria-label="התוכנית שמוצגת">${Object.entries(PLANS).map(([k, v]) => `<option value="${k}">${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p><div class="bridge-plans"></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button ex-prev">החצייה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">החצייה הבאה</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1600, 1000, 400) + `<span class="ex-pos"></span></div>` +
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
      // the plans on the current times: the search (for the chosen capacity) and, on a
      // bridge of two, the two classic plans of the page
      const plansOf = () => {
        const times = st.times, best = bridgeSolve(times, st.cap);
        const out = { best };
        if (st.cap === 2) {
          out.escort = { moves: bridgeEscortMoves(times) }; out.escort.time = bridgeTime(times, out.escort.moves);
          out.pair = { moves: bridgePairMoves(times) }; out.pair.time = bridgeTime(times, out.pair.moves);
        }
        return out;
      };
      const planText = (moves) => moves.map((g, k) => `${g.map((i) => NAMES[i]).join("+")}${k % 2 ? "<" : ">"}`).join(" ");
      const draw = () => {
        const times = st.times;
        if (!times.length) { $(".ex-summary").textContent = "הקלידו זמני חצייה חיוביים, מופרדים ברווחים."; $(".bridge-plans").innerHTML = ""; $(".bridge-frame").innerHTML = ""; $(".bridge-caption").textContent = ""; $(".ex-pos").textContent = ""; return; }
        const plans = plansOf();
        if (!plans[st.plan]) { st.plan = "best"; $(".ex-plan").value = "best"; }
        const r = plans[st.plan], best = plans.best;
        st.s = Math.min(Math.max(st.s, 0), r.moves.length);
        const names = (g) => g.map((i) => `${NAMES[i]} (${times[i]})`).join(" ו-");
        $(".ex-summary").innerHTML = `${times.length === 1 ? "אדם אחד" : `${ltr(times.length)} אנשים`} על גשר של ${st.cap === 2 ? "שניים" : "שלושה"}: הזמן הקצר ביותר הוא ${ltr(best.time)} דקות ב-${ltr(best.moves.length)} חציות, ${ltr(planText(best.moves))}.` +
          (st.plan === "best" ? "" : ` מוצגת התוכנית "${PLANS[st.plan]}": ${ltr(r.time)} דקות${r.time > best.time ? `, ${ltr(r.time - best.time)} יותר מהקצרה ביותר` : ", בדיוק כמו הקצרה ביותר"}.`);
        $(".bridge-plans").innerHTML = st.cap === 2 && times.length >= 2
          ? `<table class="bridge-table"><thead><tr><th>התוכנית</th><th>החציות</th><th>הזמן</th></tr></thead><tbody>` +
            Object.keys(PLANS).map((k) => `<tr${k === st.plan ? ' class="is-now"' : ""}${plans[k].time === best.time ? ' data-best="1"' : ""}><td>${PLANS[k]}</td><td>${ltr(planText(plans[k].moves))}</td><td>${ltr(plans[k].time)}</td></tr>`).join("") + `</tbody></table>`
          : st.cap === 3 ? `<p class="ex-note">שתי התוכניות הקלאסיות מוגדרות לגשר של שניים; לגשר של שלושה מוצג החיפוש בלבד${times.length >= 3 ? `, לעומת ${ltr(bridgeSolve(times, 2).time)} דקות על גשר של שניים` : ""}.</p>` : "";
        $(".ex-plan").querySelectorAll("option").forEach((o) => { o.disabled = !plans[o.value]; });
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

      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => (st.times.length ? plansOf()[st.plan].moves.length : 0);
      $(".ex-next").addEventListener("click", () => { stop(); st.s += 1; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s -= 1; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (!total()) return;
        if (st.s >= total()) st.s = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { if (st.s >= total()) { stop(); return; } st.s += 1; draw(); }, Number($(".ex-speed").value));
        st.s += 1; draw();
      });
      $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      input.addEventListener("change", () => { stop(); st.times = parse(); st.s = 0; draw(); });
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      $(".ex-cap").addEventListener("change", () => { stop(); st.cap = Number($(".ex-cap").value); st.s = 0; draw(); });
      $(".ex-plan").addEventListener("change", () => { stop(); st.plan = $(".ex-plan").value; st.s = 0; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); input.value = defaults; st.times = parse(); st.cap = 2; st.plan = "best"; $(".ex-cap").value = "2"; $(".ex-plan").value = "best"; st.s = 0; draw(); });
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
        `<button type="button" class="md-button md-button--primary ex-solve">פתרון</button>` + speedSel(1800, 1100, 500) + `</div>` +
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
        const ms = Number($(".ex-speed").value);
        $(".ex-solve").textContent = "עצירה";
        timer = setInterval(() => {
          if (k >= plan.length) { stop(); draw(); return; }
          const item = plan[k];
          draw({ from: st.s, item });                               // on the boat
          setTimeout(() => { if (timer) cross(item); }, ms * 0.45);
          k += 1;
        }, ms);
        draw();
      });
      $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); $(".ex-solve").click(); } });
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
        return stickyNames(`<svg class="wave-strip fifo-wave" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="רצועת תזמון: שני השעונים, הכתיבות, הקריאות ומילוי ה-FIFO" data-wavedrom="${attr(waveDromText(wd))}">${s}</svg>`, rows, L, T, RH);
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
          `הנוסחה: <b>${ltr(String(formula))}</b>; המילוי המקסימלי בסימולציה: <b>${ltr(String(r.max))}</b>` +
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
        `<div class="tri-box"><svg class="figure tri-live" viewBox="0 0 320 320" role="group" aria-label="שלוש נקודות על מעגל היחידה">` +
        `<circle class="axis-c" cx="${C}" cy="${C}" r="${R}" fill="none"/>` +
        `<g class="tri-arcs"></g><polygon class="tri-shape"/>` +
        `<circle class="center-dot" cx="${C}" cy="${C}" r="4"/><text class="tick" x="${C + 7}" y="${C + 15}">O</text>` +
        NAMES.map((n, i) => `<circle class="tri-pt" data-i="${i}" r="9" tabindex="0" role="slider" aria-valuemin="0" aria-valuemax="359"><title>${n}</title></circle>` +
          `<text class="legend tri-name" data-i="${i}" text-anchor="middle">${n}</text>`).join("") +
        `</svg><div class="tri-panel">` +
        `<p class="tri-angles">` + NAMES.map((n, i) =>
          `<label>${ltr(n)} <input type="number" class="ex-deg" data-i="${i}" min="0" max="359" step="1" dir="ltr" aria-label="הזווית של ${n} במעלות">°</label>`).join(" ") + `</p>` +
        `<div class="ex-controls"><button type="button" class="md-button ex-random">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
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
        `<p class="ex-summary tri-compare"></p>` +
        `<div class="ex-controls tri-hist-row"><button type="button" class="md-button ex-hist">1,000 הגרלות: הקשת הגדולה</button><span class="tri-hist-text"></span></div><div class="tri-hist"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const svg = $("svg"), shape = $(".tri-shape"), arcsG = $(".tri-arcs");
      // the histogram of the largest arc over 1,000 random triangles, stacked inside / outside
      const histSvg = (h) => {
        const n = h.bins.length, vmax = Math.max(...h.bins.map((b) => Math.max(b.in + b.out, b.expected)));
        const ymax = Math.ceil(vmax / 20) * 20 || 20, ticks = [];
        for (let v = 0; v <= ymax; v += ymax / 4) ticks.push(v);
        const fr = chartFrame("הקשת הגדולה ביותר ב-1,000 משולשים אקראיים", n, ymax, ticks);
        let s = fr.s;
        h.bins.forEach((b, i) => {
          const x = fr.cx(i + 1), bw = Math.max(fr.slot * 0.72, 1);
          const yOut = fr.Y(b.out), yIn = fr.Y(b.in + b.out);
          const title = `${b.lo}° עד ${b.hi}°: ${b.in} בפנים, ${b.out} בחוץ; צפוי ${fmt(b.expected, 1)}`;
          if (b.lo === 170) s += `<rect class="hist-near" x="${f(x - fr.slot / 2)}" y="${TOP}" width="${f(fr.slot)}" height="${f(BASE - TOP)}"/>`;
          if (b.out) s += `<rect class="bar hist-out" x="${f(x - bw / 2)}" y="${f(yOut)}" width="${f(bw)}" height="${f(BASE - yOut)}"><title>${title}</title></rect>`;
          if (b.in) s += `<rect class="bar hist-in${b.lo === 120 ? " is-fat" : ""}" x="${f(x - bw / 2)}" y="${f(yIn)}" width="${f(bw)}" height="${f(yOut - yIn)}"><title>${title}</title></rect>`;
          s += `<line class="ink-line" x1="${f(x - bw / 2)}" x2="${f(x + bw / 2)}" y1="${f(fr.Y(b.expected))}" y2="${f(fr.Y(b.expected))}" stroke-width="2" stroke-dasharray="3 2"/>`;
          if (b.lo % 30 === 0) s += fr.xtick(i + 1, `${b.lo}°`);
        });
        return s + fr.close();
      };
      const drawHist = (rng) => {
        const h = triHistogram(rng, 1000, 10);
        const fat = h.bins[0], near = h.bins.find((b) => b.lo === 170), inside = h.bins.reduce((t, b) => t + b.in, 0);
        $(".tri-hist").innerHTML = histSvg(h);
        $(".tri-hist-text").innerHTML = `${ltr(num(inside))} מתוך ${ltr(num(h.draws - h.degenerate))} בפנים${h.degenerate ? ` (${ltr(h.degenerate)} מנוונים הושמטו)` : ""}; ` +
          `"שמנים", קשת מתחת ל-130°: ${ltr(fat.in)} (צפוי ${ltr(fmt(fat.expected, 1))}); כמעט מנוונים, 170° עד 180°: ${ltr(near.in)} (צפוי ${ltr(fmt(near.expected, 1))}). הקו המקווקו בכל עמודה הוא הצפי מההתפלגות הרציפה.`;
      };
      const pts = [...box.querySelectorAll(".tri-pt")], names = [...box.querySelectorAll(".tri-name")];
      const inputs = [...box.querySelectorAll(".ex-deg")];
      const play = $(".ex-play"), speed = $(".ex-speed"), slider = $(".ex-frame");
      let angles = (box.dataset.angles || "20,140,250").split(",").map(Number).map((v) => ((v % 360) + 360) % 360);
      const PAGE = angles.slice();
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
          pts[i].setAttribute("aria-valuenow", d); pts[i].setAttribute("aria-label", `${NAMES[i]}: ${d} מעלות, חיצים מזיזים`);
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
      const seed = seedControls(box, $(".ex-random"), (rng) => { stop(); setAngles([0, 1, 2].map(() => Math.floor(rng() * 360))); });
      $(".ex-random").addEventListener("click", seed.draw);
      $(".ex-hist").addEventListener("click", () => { drawHist(mulberry32(Number($(".ex-seed").value) || 1)); });
      $(".ex-reset").addEventListener("click", () => { stop(); setAngles(PAGE); $(".tri-hist").innerHTML = ""; $(".tri-hist-text").textContent = ""; });
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
      // keyboard: a focused point moves one degree per arrow, ten with Shift
      svg.addEventListener("keydown", (e) => {
        const t = e.target.closest(".tri-pt"), d = arrowStep(e);
        if (!t || !d) return;
        e.preventDefault(); e.stopPropagation(); stop();
        const i = Number(t.dataset.i), next = [...angles]; next[i] += d; setAngles(next);
      });
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
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1500, 700, 250) +
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
      const steps = () => permWalk(effective().notes, st.me, maxOpens()).opened.length;
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: () => { st.step = Math.min(st.step + 1, steps()); draw(); },
        done: () => st.step >= steps(),
        restart: () => { st.step = 0; draw(); },
      });
      const setN = (n) => { stop(); st.n = n; st.notes = permShuffle(n); st.me = Math.min(st.me, n); st.step = 0; st.runs = st.strat = st.rand = 0; draw(); };
      $(".ex-n").addEventListener("input", () => setN(Number($(".ex-n").value)));
      const seed = seedControls(box, $(".ex-example"), (rng) => { stop(); st.notes = permShuffle(st.n, rng); st.step = 0; draw(); }, { state: {
        get: () => STATE_CODECS.boxes.enc({ notes: st.notes, me: st.me, helper: st.helper, step: st.step }),
        set: (p) => {
          const d = STATE_CODECS.boxes.dec(p, nmax);
          if (!d) return false;
          stop(); st.n = d.n; $(".ex-n").value = d.n; st.notes = d.notes; st.me = d.me; st.helper = d.helper; helperCb.checked = d.helper;
          st.step = Math.min(d.step, steps()); draw(); return true;
        },
      } });
      $(".ex-shuffle").addEventListener("click", seed.draw);
      $(".ex-example").addEventListener("click", () => { stop(); st.n = nmax; $(".ex-n").value = nmax; st.notes = EXAMPLE.slice(0, nmax + 1); st.me = 13; st.step = 0; draw(); });
      helperCb.addEventListener("change", () => { stop(); st.helper = helperCb.checked; st.step = 0; draw(); });
      $(".ex-next").addEventListener("click", () => { stop(); st.step = Math.min(st.step + 1, steps()); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.step = Math.max(st.step - 1, 0); draw(); });
      $(".ex-all").addEventListener("click", () => { stop(); st.step = steps(); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.step = 0; draw(); });
      meIn.addEventListener("change", () => {
        stop();
        const v = Math.round(Number(meIn.value));
        if (v >= 1 && v <= st.n) { st.me = v; st.step = 0; }
        draw();
      });
      meIn.addEventListener("keydown", (e) => { if (e.key === "Enter") meIn.blur(); });
      ring.addEventListener("click", (e) => {
        const g = e.target.closest(".bx-g");
        if (!g) return;
        stop(); st.me = Number(g.dataset.b); st.step = 0; draw();
      });
      ring.addEventListener("keydown", (e) => {
        const g = e.target.closest(".bx-g");
        if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); stop(); st.me = Number(g.dataset.b); st.step = 0; draw(); }
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
      const seed = seedControls(box, $(".ex-example"), (rng) => setNums(floydRandom(st.nums.length - 1, rng)), { state: {
        get: () => STATE_CODECS.floyd.enc({ nums: st.nums, k: st.k }),
        set: (p) => { const d = STATE_CODECS.floyd.dec(p, nmax); if (!d) return false; setNums(d.nums); st.k = d.k; draw(); return true; },
      } });
      $(".ex-shuffle").addEventListener("click", seed.draw);
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
      const st = { x: Number(box.dataset.x || 7), k: 0, digits: [0, 1], lenOnly: false };
      const big = (s) => { const b = BigInt(s); return b < 10n ** 12n ? Number(b).toLocaleString("en-US") : `${(Number(b / 10n ** BigInt(s.length - 3)) / 100).toFixed(2)}·10^${s.length - 1}`; };
      const DIGIT_CLS = ["s1", "s2", "s3"];          // one colour per allowed digit, in order
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏x</span><input type="range" class="ex-x" min="1" max="${xmax}" step="1" value="${st.x}" dir="ltr"><output class="out-x"></output></label>` +
        `<span class="bf-presets">דוגמאות: ` + [7, 9, 11, 13, 37].filter((v) => v <= xmax).map((v) => `<button type="button" class="md-button ex-preset" data-x="${v}">${v}</button>`).join(" ") + `</span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls">` +
        `<label>הספרות המותרות <input type="text" class="ex-digits" value="0 1" size="7" dir="ltr" inputmode="numeric" aria-label="הספרות המותרות, עד שלוש"></label>` +
        `<span class="bf-presets"><button type="button" class="md-button ex-digitset" data-digits="0 1">0 ו-1 (השאלה)</button> <button type="button" class="md-button ex-digitset" data-digits="3 7">3 ו-7 (שאלת ההמשך)</button></span>` +
        `<label><input type="checkbox" class="ex-lenonly"> <span>רק האורך, בלי שחזור ההורים</span></label><span class="fl-err bf-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1500">איטי</option><option value="700" selected>בינוני</option><option value="250">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<span class="viz-legend bf-legend"></span>` +
        `<div class="bf-box"><div class="bf-ring"></div><div class="bf-panel"><p class="bf-step" aria-live="polite"></p><p class="bf-queue"></p><p class="bf-path"></p></div></div>` +
        `<p class="ex-summary bf-sum"></p><p class="ex-note bf-mem"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let timer = null, trace = null;
      const clsOf = (d) => DIGIT_CLS[st.digits.indexOf(d)] || "ink";
      const legend = () => st.digits.map((d) => `<span><i class="${clsOf(d)}"></i>הוספת ${d}</span>`).join("") +
        `<span><i class="st-stack"></i>בתור</span><span><i class="st-done"></i>טופל</span><span><i class="st-ok"></i>שארית 0</span>`;
      const ringSvg = (tr, k) => {
        const x = st.x, W = 360, C = 180, R = x <= 12 ? 120 : 140, NODE = x <= 12 ? 16 : x <= 24 ? 13 : 10;
        const pt = (r, rad) => { const a = -Math.PI / 2 + (2 * Math.PI * r) / x; return [C + rad * Math.cos(a), C + rad * Math.sin(a)]; };
        const done = new Set(), queued = new Set(tr.frames.length ? tr.starts : []);
        const edges = [];
        for (let i = 0; i < k; i++) {
          const fr = tr.frames[i];
          done.add(fr.r); queued.delete(fr.r);
          fr.kids.forEach((kid) => { if (kid.status !== "seen") { queued.add(kid.nr); edges.push([fr.r, kid.nr, kid.d, false]); } });
        }
        const cur = k > 0 ? tr.frames[k - 1] : null;
        if (cur) cur.kids.forEach((kid) => { if (kid.status === "seen") edges.push([cur.r, kid.nr, kid.d, true]); });
        const finished = k >= tr.frames.length && tr.answer !== null;
        const onPath = new Set(finished && !st.lenOnly ? tr.path : []);
        const seen = new Set([...done, ...queued]);
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
          return `<path class="${cls}-line" d="M${f(sx)},${f(sy)} Q${f(mx)},${f(my)} ${f(ex)},${f(ey)}" fill="none" stroke-width="${thick ? 3.5 : 2}"${dashed ? ' stroke-dasharray="4 3"' : ""}/>` +
                 (dashed ? "" : `<polygon class="${cls}-fill" points="${f(ex)},${f(ey)} ${f(hx + uy * 4)},${f(hy - ux * 4)} ${f(hx - uy * 4)},${f(hy + ux * 4)}"/>`);
        };
        // length only: no tree, just the layer number beside every remainder reached
        if (!st.lenOnly) edges.forEach(([a, b, d, pruned]) => {
          const thick = onPath.has(a) && onPath.has(b) && tr.parent[b] === a;
          s += arrow(a, b, clsOf(d), pruned, thick);
        });
        for (let r = 0; r < x; r++) {
          const [px, py] = pt(r, R);
          const cls = finished && r === 0 ? "st-ok" : cur && r === cur.r ? "st-stack is-cur" : queued.has(r) ? "st-stack" : done.has(r) ? "st-done" : "st-cell";
          s += `<g><circle class="${cls}${onPath.has(r) ? " is-path" : ""}" cx="${f(px)}" cy="${f(py)}" r="${NODE}"><title>שארית ${r}${seen.has(r) ? `, שכבה ${tr.depth[r]}` : ""}</title></circle>` +
               `<text class="st-text ${x <= 12 ? "st-sm" : "bf-xs"}" x="${f(px)}" y="${f(py + (x <= 12 ? 4 : 3.5))}" text-anchor="middle">${r}</text>`;
          if (st.lenOnly && seen.has(r)) { const [lx, ly] = pt(r, R + NODE + 9); s += `<text class="legend bf-layer" x="${f(lx)}" y="${f(ly + 4)}" text-anchor="middle">${tr.depth[r]}</text>`; }
          s += `</g>`;
        }
        return s + "</svg>";
      };
      // the hardware follow-up: what the reconstruction costs against a length-only search
      const memLine = () => {
        const bits = (x) => { const w = Math.max(1, Math.ceil(Math.log2(x + 1))), full = x * (w + 1), lean = 3 * x; return { w, full, lean }; };
        const kb = (b) => `${(b / 8192).toFixed(b < 8192 ? 2 : 0)} KB`;
        const here = bits(st.x), wide = bits(65535);
        return `זיכרון: עם שחזור, ${ltr(st.x)} הורים של ${ltr(here.w)} ביט ועוד ${ltr(st.x)} ספרות, ${ltr(here.full.toLocaleString("en-US"))} ביט; רק האורך, שלוש מפות ביטים של ${ltr(st.x)} ביט (נראה, החזית, החזית הבאה) ומונה שכבה, ${ltr(here.lean.toLocaleString("en-US"))} ביט. ` +
          `ל-${ltr("x")} של 16 ביט: ${ltr(wide.full.toLocaleString("en-US"))} ביט (${ltr(kb(wide.full))}) מול ${ltr(wide.lean.toLocaleString("en-US"))} ביט (${ltr(kb(wide.lean))}); התור של ההורים הוא FIFO של עד ${ltr("x")} כניסות של ${ltr(wide.w)} ביט.`;
      };
      const digitsText = () => st.digits.join("/");
      const draw = () => {
        $(".out-x").textContent = String(st.x);
        $(".bf-legend").innerHTML = legend();
        trace = bfs01Trace(st.x, st.digits);
        const tr = trace, total = tr.frames.length, none = tr.answer === null;
        st.k = Math.min(st.k, total);
        $(".bf-ring").innerHTML = ringSvg(tr, st.k);
        $(".ex-pos").textContent = `הוצאה ${st.k} מתוך ${total}`;
        const name = (r, n) => `${ltr(`r = ${r}`)} (המספר ${ltr(n)})`;
        const startNums = st.digits.filter((d) => d > 0);
        let step;
        if (st.k === 0) {
          step = total === 0 && !none
            ? `עבור ${ltr(`x = ${st.x}`)} המספר ${ltr(tr.answer)} כבר נותן שארית 0, ולכן התשובה היא ${ltr(tr.answer)} בלי צעדים.`
            : `מתחילים מ${startNums.length === 1 ? `המספר ${ltr(startNums[0])}, שארית ${ltr(tr.starts[0])}` : `המספרים ${ltr(startNums.join(", "))}, שאריות ${ltr(tr.starts.join(", "))}`}. התור: ${ltr(`[${tr.starts.join(", ")}]`)}.`;
        } else {
          const fr = tr.frames[st.k - 1];
          const kid = (kd) => {
            const n = fr.number + kd.d;
            return `${ltr(`+${kd.d}`)} → ${ltr(n)}, שארית ${ltr(kd.nr)}: ` +
              (kd.status === "new" ? "חדשה, נכנסת לתור" : kd.status === "seen" ? `כבר נראתה, נגזמת ✗` : `<b>0, מצאנו ✓</b>`);
          };
          step = `הוצאה ${ltr(st.k)}: מוציאים ${name(fr.r, fr.number)}. ${fr.kids.map(kid).join("; ")}.`;
        }
        $(".bf-step").innerHTML = step;
        const q = st.k === 0 ? tr.starts : tr.frames[st.k - 1].queue;
        $(".bf-queue").innerHTML = st.k > 0 ? `התור אחרי הצעד: ${ltr(`[${q.join(", ")}]`)}.` : "";
        const finished = st.k >= total;
        $(".bf-path").innerHTML = !finished ? ""
          : none ? `<span class="wv-bad">✗ התור התרוקן ושארית 0 לא נמצאה: לאף מספר מהספרות ${ltr(digitsText())} אין שארית 0 מודולו ${ltr(st.x)}, כלומר אין פתרון.</span>`
          : st.lenOnly ? `שארית 0 התגלתה בשכבה ${ltr(tr.depth[0])}: לכפולה הקטנה ביותר יש <b>${ltr(tr.depth[0])} ספרות</b>. בלי ההורים אי אפשר לומר איזו כפולה, רק כמה ספרות יש לה.`
          : `השחזור: ${ltr(tr.path.slice().reverse().map((r, i) => (i === 0 ? "0" : `← ${r}`)).join(" "))}, הספרות מהסוף להתחלה נותנות <b>${ltr(`y = ${tr.answer}`)}</b> (${ltr(`${tr.answer.length}`)} ספרות).`;
        const c = bfs01Counts(st.x, st.digits);
        $(".bf-sum").innerHTML = none
          ? `עבור ${ltr(`x = ${st.x}`)} והספרות ${ltr(digitsText())}: ה-BFS מוציא מהתור ${ltr(c.dequeues)} שאריות ונעצר בלי למצוא 0. ` +
            (st.digits.every((d) => d % 2) && st.x % 2 === 0 ? `כל הספרות אי-זוגיות, ולכן כל מספר שבנוי מהן אי-זוגי ואינו מתחלק ב-${ltr(st.x)}.` : `השאריות שהספרות האלה מגיעות אליהן אינן כוללות את 0.`)
          : `עבור ${ltr(`x = ${st.x}`)}${st.digits.join("") === "01" ? "" : ` והספרות ${ltr(digitsText())}`}: ה-BFS מוציא מהתור ${ltr(c.dequeues)} שאריות${c.dequeues < st.x ? ` (פחות מ-${ltr(st.x)})` : ""}. ` +
            `לשם השוואה, המעבר על המספרים מהספרות ${ltr(digitsText())} בודק ${ltr(big(c.enumerated))} מספרים, והמעבר על הכפולות של ${ltr(st.x)} בודק ${ltr(big(c.multiples))}.`;
        $(".bf-mem").innerHTML = st.lenOnly ? memLine() : "";
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => bfs01Trace(st.x, st.digits).frames.length;
      const setX = (x) => { stop(); st.x = x; st.k = 0; $(".ex-x").value = x; draw(); };
      $(".ex-x").addEventListener("input", () => setX(Number($(".ex-x").value)));
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => setX(Number(b.dataset.x))));
      // the digit set: up to three distinct digits, at least one of them non-zero
      const setDigits = (text) => {
        const ds = [...new Set((text.match(/[0-9]/g) || []).map(Number))].sort((a, b) => a - b);
        const err = ds.length === 0 || ds.length > 3 ? "בין ספרה אחת לשלוש" : ds.every((d) => d === 0) ? "לפחות ספרה אחת שאינה 0" : "";
        $(".bf-err").textContent = err;
        if (err) return;
        stop(); st.digits = ds; st.k = 0; $(".ex-digits").value = ds.join(" "); draw();
      };
      $(".ex-digits").addEventListener("change", () => setDigits($(".ex-digits").value));
      $(".ex-digits").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".ex-digits").blur(); });
      box.querySelectorAll(".ex-digitset").forEach((b) => b.addEventListener("click", () => setDigits(b.dataset.digits)));
      $(".ex-lenonly").addEventListener("change", () => { stop(); st.lenOnly = $(".ex-lenonly").checked; draw(); });
      const X0 = st.x;
      $(".ex-reset").addEventListener("click", () => { st.lenOnly = false; $(".ex-lenonly").checked = false; setDigits("0 1"); setX(X0); });
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
  // The 45 digit pairs a < b for one x (0005 follow-up): a triangle of cells, rows a = 0..8
  // and columns b = 1..9, each the length of the smallest multiple or ✗; a click shows the
  // answer, x = 2^s 5^t m and the rule of the theorem, and both functions are compared.
  const abmapView = () => ({
    mount(box) {
      const xmax = Number(box.dataset.xmax || 9999), X0 = Number(box.dataset.x || 28);
      const st = { x: X0, a: 1, b: 2 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏x</span><input type="number" class="ex-num ab-x" min="1" max="${xmax}" step="1" value="${st.x}" dir="ltr" inputmode="numeric" aria-label="המספר x, מ-1 עד ${xmax}"></label>` +
        `<span class="bf-presets">דוגמאות: ` + [7, 28, 40, 75, 125, 9999].filter((v) => v <= xmax).map((v) => `<button type="button" class="md-button ex-preset" data-x="${v}">${v}</button>`).join(" ") + `</span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err ab-err"></span></div>` +
        `<span class="viz-legend"><span><i class="ab-ok-key"></i>יש פתרון: מספר הספרות</span><span><i class="ab-no-key"></i>✗ אין פתרון</span></span>` +
        `<div class="ab-grid" dir="ltr" role="group" aria-label="45 זוגות הספרות: שורה לכל a, עמודה לכל b"></div>` +
        `<p class="ex-summary ab-sum"></p><p class="ab-detail" aria-live="polite"></p><p class="ex-note ab-rule"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const pow = (p, e) => (e === 0 ? "" : e === 1 ? `${p}` : `${p}<sup>${e}</sup>`);
      const factors = (e) => { const parts = [pow(2, e.s), pow(5, e.t), e.m > 1 ? String(e.m) : ""].filter(Boolean); return parts.length ? parts.join(" · ") : "1"; };
      const times = (h) => (h === 1 ? "חציה אחת" : `${h} חציות`);
      const reason = (e, a, b) => {
        const x = ltr(st.x);
        switch (e.rule) {
          case "zero": return `עם הספרה 0 תמיד יש פתרון` + (e.s || e.t ? `: ${ltr(b)} ואחריו אפסים מתחלק ב-${ltr(factors({ ...e, m: 1 }))}` : "") +
            (e.m > 1 ? `, וחזרות על הבלוק משלימות את ${ltr(e.m)}` : "") + ` (שלבים 3 ו-4 בהוכחה).`;
          case "coprime": return `${x} זר ל-10, ולכן לכל זוג ספרות יש פתרון (שלב 3 בהוכחה).`;
          case "ten": return `${x} מתחלק ב-10, ובלי הספרה 0 אף מספר לא מסתיים ב-0 (שלב 7 בהוכחה).`;
          case "no5": return `${x} מתחלק ב-5, ובלי 0 ו-5 אף מספר לא מסתיים ב-0 או ב-5 (שלב 6 בהוכחה).`;
          case "five": return `${x} מתחלק ב-5 פעם אחת בלבד, והספרה 5 בסוף המספר מספיקה (שלב 6 בהוכחה).`;
          case "twentyfive": return `${x} מתחלק ב-25, והסיומת ${ltr(a === 2 ? 25 : 75)} בנויה מהספרות (שלב 6 בהוכחה).`;
          case "no25": return `${x} מתחלק ב-25, והסיומות 25 ו-75 דורשות את הזוג ${ltr("{2, 5}")} או ${ltr("{5, 7}")} (שלב 6 בהוכחה).`;
          case "no125": return `${x} מתחלק ב-125, ולכל סיומת של 125 (${ltr("125, 375, 625, 875")}) יש שלוש ספרות שונות (שלב 6 בהוכחה).`;
          case "mixed": return `${e.halvings ? `אחרי ${times(e.halvings)} של הספרות נשארו ${ltr(e.a2)} ו-${ltr(e.b2)}: ` : ""}הספרות בזוגיות שונה, ולכן לכל חזקה של 2 יש כפולה (שלב 5 בהוכחה).`;
          case "halved": return `שתי הספרות זוגיות, ואחרי ${times(e.halvings)} של הספרות לא נשארת חזקה של 2 לטפל בה: ${ltr(factors({ ...e, t: 0, m: 1 }))} מטופל כולו (שלב 5 בהוכחה).`;
          default: return `${e.halvings ? `אחרי ${times(e.halvings)} של הספרות נשארו ${ltr(e.a2)} ו-${ltr(e.b2)}: ` : ""}שתי הספרות אי-זוגיות, ולכן כל מספר מהן אי-זוגי ולא מתחלק ב-${ltr(2 ** (e.s - e.halvings))} (שלב 5 בהוכחה).`;
        }
      };
      let cells = {};
      const draw = () => {
        cells = {};
        let html = `<span class="ab-head ab-corner">a \\ b</span>`;
        for (let b = 1; b <= 9; b++) html += `<span class="ab-head">${b}</span>`;
        let solved = 0, agree = 0, longest = null;
        for (let a = 0; a <= 8; a++) {
          html += `<span class="ab-head">${a}</span>`;
          for (let b = 1; b <= 9; b++) {
            if (b <= a) { html += `<span class="ab-void"></span>`; continue; }
            const r = abMultiple(st.x, a, b), e = abExists(st.x, a, b), ok = r.answer !== null;
            cells[`${a}${b}`] = { r, e };
            if (ok) { solved++; if (!longest || r.answer.length > longest.len) longest = { len: r.answer.length, a, b }; }
            if (ok === e.ok) agree++;
            const sel = a === st.a && b === st.b;
            html += `<button type="button" class="ab-cell ${ok ? "ab-ok" : "ab-no"}${sel ? " is-sel" : ""}" data-a="${a}" data-b="${b}" aria-pressed="${sel}" ` +
              `aria-label="${a} ו-${b}: ${ok ? `${r.answer.length} ספרות` : "אין פתרון"}">${ok ? r.answer.length : "✗"}</button>`;
          }
        }
        $(".ab-grid").innerHTML = html;
        box.querySelectorAll(".ab-cell").forEach((c) => c.addEventListener("click", () => { st.a = Number(c.dataset.a); st.b = Number(c.dataset.b); draw(); }));
        $(".ab-sum").innerHTML = `עבור ${ltr(`x = ${st.x}`)}: ל-${ltr(solved)} מתוך 45 הזוגות יש פתרון` +
          (longest ? `, והתשובה הארוכה ביותר היא בת ${ltr(longest.len)} ספרות (הספרות ${ltr(longest.a)} ו-${ltr(longest.b)}).` : ".") +
          (agree === 45 ? ` ה-BFS ובדיקת הקיום מסכימים בכל 45 התאים ✓.` : ` <span class="wv-bad">✗ ה-BFS ובדיקת הקיום חלוקים ב-${ltr(45 - agree)} תאים.</span>`);
        const { r, e } = cells[`${st.a}${st.b}`];
        const ans = r.answer;
        $(".ab-detail").innerHTML = `הספרות ${ltr(st.a)} ו-${ltr(st.b)}: ` + (ans !== null
          ? `הכפולה הקטנה ביותר של ${ltr(st.x)} היא <span class="ab-ans" dir="ltr">${ans}</span> ${ans.length > 1 ? `(${ltr(ans.length)} ספרות` : "(ספרה אחת"}, ה-BFS הוציא ${ltr(r.dequeues)} שאריות מהתור).`
          : `<b>אין כפולה.</b> ה-BFS הוציא ${ltr(r.dequeues)} שאריות מהתור, והתור התרוקן בלי שארית 0.`);
        $(".ab-rule").innerHTML = `הפירוק: ${ltr(`${st.x} = ${factors(e)}`)}, כלומר ${ltr(`s = ${e.s}, t = ${e.t}, m = ${e.m}`)}. ${reason(e, st.a, st.b)} ` +
          (e.ok === (ans !== null) ? "בדיקת הקיום מסכימה עם ה-BFS ✓." : `<span class="wv-bad">✗ בדיקת הקיום אומרת ${e.ok ? "שיש" : "שאין"} פתרון.</span>`);
      };
      const setX = (v) => {
        const x = Math.round(Number(v));
        const err = !Number.isFinite(x) || x < 1 || x > xmax ? `מספר שלם מ-1 עד ${xmax}` : "";
        $(".ab-err").textContent = err;
        if (err) return;
        st.x = x; $(".ab-x").value = x; draw();
      };
      $(".ab-x").addEventListener("change", () => setX($(".ab-x").value));
      $(".ab-x").addEventListener("keydown", (ev) => { if (ev.key === "Enter") setX($(".ab-x").value); });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => setX(b.dataset.x)));
      $(".ex-reset").addEventListener("click", () => { st.a = 1; st.b = 2; setX(X0); });
      draw();
    },
  });

  const bracketsView = () => ({
    mount(box) {
      const PRESETS = ["()", "()[]{}", "{[()]}", "([]{})", "(]", "([)]", "(((", "())", ")("];
      const st = { s: box.dataset.s || "{[()]}", k: 0 };
      const NAMES = { "(": "עגול", "[": "מרובע", "{": "מסולסל" };
      const esc = (c) => c.replace(/</g, "&lt;");
      box.innerHTML =
        `<div class="ex-controls"><label><span>המחרוזת</span><input type="text" class="ex-s" dir="ltr" spellcheck="false" maxlength="40" aria-label="מחרוזת של סוגריים"></label>` +
        `<span class="br-presets">דוגמאות: ` + PRESETS.map((p) => `<button type="button" class="md-button ex-preset" dir="ltr" data-s="${esc(p)}">${esc(p)}</button>`).join(" ") + `</span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
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
      const PAGE = st.s;
      $(".ex-reset").addEventListener("click", () => setS(PAGE));
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
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button>` +
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
      const seed = seedControls(box, $(".ex-reset"), (rng) => { st.board = tttRandom(st.wrap, rng).board; draw(); });
      $(".ex-random").addEventListener("click", seed.draw);
      $(".ex-clear").addEventListener("click", () => { st.board = new Array(9).fill("."); draw(); });
      const PAGE = st.board.slice();
      $(".ex-reset").addEventListener("click", () => { st.board = PAGE.slice(); draw(); });
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
      const seed = seedControls(box, $(".ex-heat"), (rng) => {
        stop(); st.heat = null;
        st.shapes = shapesRandom(st.N, st.M, st.max, st.squares, rng);
        $(".sh-step").innerHTML = `הגרלה שלמה כמו ${ltr("random_shapes")}: ${ltr(st.shapes.length)} ${st.shapes.length === 1 ? "צורה" : "צורות"} (מספר אחיד בין 1 ל-${ltr(st.max)}), כל אחת אחידה מבין המועמדים הפנויים אחרי קודמותיה.`;
        draw();
      });
      $(".ex-all").addEventListener("click", seed.draw);
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

      };
      const set = (x) => { if (Number.isInteger(x) && x >= 0 && x <= MAX) st.x = x; draw(); };
      input.addEventListener("change", () => set(Math.round(Number(input.value))));
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      const seed = seedControls(box, $(".kp-presets"), (rng) => set(Math.floor(rng() * (MAX + 1))));
      $(".ex-random").addEventListener("click", seed.draw);
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
        `<button type="button" class="md-button ex-prev">הקודמת</button><button type="button" class="md-button md-button--primary ex-next">ההכרזה הבאה</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(2200, 1300, 500) + `</div>` +
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
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: () => { st.k = Math.min(st.k + 1, Number(slider.max)); draw(); },
        done: () => st.k >= Number(slider.max),
        restart: () => { st.k = 0; draw(); },
      });
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, Number(slider.max)); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
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
      const newGame = (keepStats = true, rnd = Math.random) => {
        const cases = boxesCases().filter((c) => c.labels.join() === st.labels.join());
        st.content = cases[Math.floor(rnd() * cases.length)].content;
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
      const seed = seedControls(box, $(".ex-reveal"), (rng) => { newGame(true, rng); draw(); });
      $(".ex-new").addEventListener("click", seed.draw);
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
        `<button type="button" class="md-button ex-regular">מצולע משוכלל</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="tri-box"><svg class="figure tri-live" viewBox="0 0 320 320" role="group" aria-label="קודקודים על מעגל היחידה">` +
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
          return `<circle class="tri-pt" data-i="${i}" cx="${f(x)}" cy="${f(y)}" r="${n > 7 ? 7 : 9}" tabindex="0" role="slider" aria-valuemin="0" aria-valuemax="359" aria-valuenow="${d}" aria-label="P${i + 1}: ${d} מעלות, חיצים מזיזים"><title>P${i + 1}</title></circle>` +
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
        const p = polyProb(n), d = polyProbDiscrete(n);
        $(".tri-compare").innerHTML = `הנוסחה של סעיף ג לזוויות רציפות: ${ltr(`1 − ${n}/2^${n - 1} = ${fmt(p, 4)}`)}. ` +
          `בזוויות שלמות, כמו בספירה של סעיף ד: ${ltr(`1 − 360·C(180, ${n - 1}) / C(360, ${n}) = ${d.num}/${d.den} ≈ ${fmt(d.value, 4)}`)}, ` +
          `${ltr(fmt(Math.abs(d.value - p), 4))} ${d.value < p ? "פחות" : "יותר"} מהרציף. ` +
          (st.runs ? `מתוך ${ltr(num(st.runs))} מצולעים אקראיים (זוויות שלמות שונות), ${ltr(num(st.hits))} הכילו את המרכז: ${ltr(fmt(st.hits / st.runs, 4))}, מול ${ltr(fmt(d.value, 4))} הבדיד.` : `לחצו "1,000 הגרלות" כדי להשוות.`);
      };
      const setN = (n) => { st.n = n; st.angles = regular(n); st.runs = st.hits = 0; render(); };
      $(".ex-n").addEventListener("input", () => setN(Number($(".ex-n").value)));
      const seed = seedControls(box, $(".ex-random"), (rng) => { st.angles = polyRandom(st.n, rng); render(); });
      $(".ex-random").addEventListener("click", seed.draw);
      $(".ex-regular").addEventListener("click", () => { st.angles = regular(st.n); render(); });
      const N0 = st.n;
      $(".ex-reset").addEventListener("click", () => { $(".ex-n").value = N0; setN(N0); });
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
      // keyboard: a focused vertex moves one degree per arrow, ten with Shift; the
      // vertices are redrawn, so the focus is put back on the same one
      svg.addEventListener("keydown", (e) => {
        const t = e.target.closest(".tri-pt"), d = arrowStep(e);
        if (!t || !d) return;
        e.preventDefault(); e.stopPropagation();
        const i = Number(t.dataset.i), next = [...st.angles];
        next[i] = ((next[i] + d) % 360 + 360) % 360; st.angles = next; render();
        const g = svg.querySelector(`.tri-pt[data-i="${i}"]`); if (g) g.focus({ preventScroll: true });
      });
      void running;
      render();
    },
  });

  // A timing strip: rows over N slots (clock cycles, or half-cycles with `half`), the
  // names in a left column. Row kinds: "clock" (the square wave), "bit" (a level line,
  // shaded where high), "bus" (labelled boxes merged over equal values). A row's values
  // may stop early (frames not reached yet). `cells` on a row makes every slot a button
  // (data-k); `marks` on a row shades slots; `cursor` outlines one slot; `split` on a bus
  // row keeps equal neighbours apart (one box per slot, for a row of events).
  // The row names of a strip again as an HTML column that sticks to the left edge of the
  // scroll container, so a long strip scrolled to its end still says which row is which
  // (the names inside the svg stay for the enlarged copy).
  const stickyNames = (svg, names, L, T, RH) =>
    `<div class="wv-row"><div class="wv-names" aria-hidden="true" style="width:${L}px;margin-right:-${L}px;padding-top:${T}px">` +
    names.map((n) => `<div style="height:${RH}px;line-height:${RH - 2}px">${n}</div>`).join("") + `</div>${svg}</div>`;
  const waveStrip = (rows, N, opts = {}) => {
    const L = opts.labelW ?? 66, SW = opts.slotW ?? 36, RH = 30, T = opts.ticks ? 20 : 8;
    const W = L + N * SW + 6, H = T + rows.length * RH + 4;
    const x = (k) => L + k * SW;
    let s = `<svg class="wave-strip" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="${opts.role || "img"}" aria-label="${opts.label || ""}" data-wavedrom="${attr(waveDromText(waveDromOf(rows, N, opts)))}">`;
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
      } else if (row.kind === "flag") {
        for (let k = 0; k < len; k++) if (row.values[k]) s += `<g class="wv-fail"><circle cx="${x(k) + SW / 2}" cy="${ym}" r="9"/><text x="${x(k) + SW / 2}" y="${ym + 4}" text-anchor="middle">✗</text></g>`;
      } else if (row.kind === "bus") {
        let k = 0;
        while (k < len) {
          let j = k;
          while (!row.split && j + 1 < len && row.values[j + 1] === row.values[k]) j++;
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
    return stickyNames(s + "</svg>", rows.map((row) => row.name), L, T, RH);
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
      const cursorAfter = (p) => { st.cur = p === "clear" ? 1 : Math.max(1, st.sig.findIndex((v, i) => i > 0 && v !== st.sig[i - 1])); draw(); };
      const seed = seedControls(box, $(".wv-presets"), (rng) => { st.sig = Array.from({ length: N }, () => (rng() < 0.5 ? 1 : 0)); cursorAfter("random"); });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => {
        const p = b.dataset.p;
        if (p === "random") { seed.draw(); return; }
        if (p === "page") st.sig = PAGE.slice();
        else if (p === "short") st.sig = [0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1];
        else st.sig = new Array(N).fill(0);
        cursorAfter(p);
      }));
      draw();
    },
  });

  // The LFSR box (0036): a width of 3 to 8 bits, tick the taps (x^n and 1 are fixed), step
  // or play from 0…01 on a ring of the 2^n − 1 non-zero states (0 sits in the middle as the
  // fixed point; up to 6 bits), a timing strip of clk, the state, s[0] and the feedback bit
  // for every step so far, and the table of the polynomials with their periods: every one
  // up to 5 bits, the primitive ones from 6 bits on, with the count φ(2^n − 1) / n.
  const lfsrView = () => ({
    mount(box) {
      const SEED = 1, RING_MAX = 6, FULL_TABLE = 5;
      const st = { width: 4, mask: 0b0011, k: 0 };
      const bits = (v) => bitsOf(v, st.width);
      const states = () => (1 << st.width) - 1;
      const sup = (k) => (k === 1 ? "x" : `x<sup>${k}</sup>`);
      const polyHtml = (mask, width = st.width) => {
        const t = [`x<sup>${width}</sup>`];
        for (let k = width - 1; k >= 1; k--) if ((mask >> (width - k)) & 1) t.push(sup(k));
        return ltr(t.concat("1").join(" + "));
      };
      box.innerHTML =
        `<div class="ex-controls"><label>רוחב <select class="ex-width" aria-label="מספר הביטים">${[3, 4, 5, 6, 7, 8].map((w) => `<option value="${w}"${w === 4 ? " selected" : ""}>${w} ביטים</option>`).join("")}</select></label>` +
        `<span class="lf-taps" dir="ltr" role="group" aria-label="בחירת ה-taps"></span>` +
        `<span class="lf-presets">הפולינומים של השאלה: <button type="button" class="md-button ex-preset" data-mask="3">${ltr("x<sup>4</sup> + x<sup>3</sup> + 1")}</button> ` +
        `<button type="button" class="md-button ex-preset" data-mask="5">${ltr("x<sup>4</sup> + x<sup>2</sup> + 1")}</button></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">צעד</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1000">איטי</option><option value="500" selected>בינוני</option><option value="180">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד שהמצב חוזר</button><span class="ex-pos"></span></div>` +
        `<div class="lf-box"><div class="lf-ring"></div><div class="lf-panel">` +
        `<p class="lf-poly"></p><p class="lf-state"></p><p class="lf-fb"></p>` +
        `<p class="ex-summary lf-sum" aria-live="polite"></p></div></div>` +
        `<p class="ex-title">רצועת התזמון: המצב, הביט שיוצא (${code("s[0]")}) וביט ההיזון החוזר שנכנס, צעד אחרי צעד</p>` +
        `<div class="wv-wrap lf-strip" tabindex="0" role="group" aria-label="רצועת התזמון של ה-LFSR, גלילה אופקית"></div>` +
        `<p class="ex-title lf-table-title"></p><div class="lf-table" tabindex="0"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let timer = null;
      // the tap boxes follow the width: x^width and 1 fixed, a box per middle power
      const tapsHtml = () => {
        const ks = []; for (let k = st.width - 1; k >= 1; k--) ks.push(k);
        $(".lf-taps").innerHTML = `<span class="lf-fixed">${ltr(`x<sup>${st.width}</sup>`)} +</span> ` +
          ks.map((k) => `<label><input type="checkbox" class="ex-tap" data-k="${k}"> <span>${ltr(sup(k))} +</span></label>`).join(" ") + `<span class="lf-fixed">1</span>`;
        box.querySelectorAll(".ex-tap").forEach((c) => c.addEventListener("change", () => {
          const bit = 1 << (st.width - Number(c.dataset.k));
          st.mask = c.checked ? st.mask | bit : st.mask & ~bit;
          stop(); st.k = 0; draw();
        }));
      };
      const ring = (walk, shown) => {
        const n = states(), C = 150, R = st.width <= 4 ? 118 : 128;
        const rr = st.width <= 4 ? 17 : st.width === 5 ? 11 : 6, label = st.width <= 5;
        const pos = (v) => { const ang = -Math.PI / 2 + ((v - 1) / n) * 2 * Math.PI; return [C + R * Math.cos(ang), C + R * Math.sin(ang)]; };
        const visited = new Set(shown), cur = shown[shown.length - 1];
        let s = `<svg class="lf-live" viewBox="0 0 300 300" role="img" aria-label="טבעת של ${n} המצבים שאינם אפס, המצבים שבוקרו וחיצים ביניהם">` +
          `<defs><marker id="lf-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="${rr > 8 ? 7 : 5}" markerHeight="${rr > 8 ? 7 : 5}" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="lf-arrowhead"/></marker></defs>`;
        for (let i = 1; i < shown.length; i++) {
          const [x1, y1] = pos(shown[i - 1]), [x2, y2] = pos(shown[i]);
          const dx = x2 - x1, dy = y2 - y1, d = Math.hypot(dx, dy) || 1;
          s += `<line class="lf-edge${i === shown.length - 1 ? " is-cur" : ""}" x1="${f(x1 + (dx / d) * rr)}" y1="${f(y1 + (dy / d) * rr)}" x2="${f(x2 - (dx / d) * (rr + 2))}" y2="${f(y2 - (dy / d) * (rr + 2))}" marker-end="url(#lf-arrow)"/>`;
        }
        for (let v = 1; v <= n; v++) {
          const [x, y] = pos(v);
          s += `<g class="lf-node${visited.has(v) ? " is-seen" : ""}${v === cur ? " is-cur" : ""}${v === SEED ? " is-seed" : ""}"><circle cx="${f(x)}" cy="${f(y)}" r="${rr}"><title>${bits(v)}</title></circle>` +
               (label ? `<text x="${f(x)}" y="${f(y + (rr > 12 ? 4 : 3))}" text-anchor="middle"${rr > 12 ? "" : ' font-size="7"'}>${bits(v)}</text>` : "") + `</g>`;
        }
        const zr = Math.max(rr, 14);
        s += `<g class="lf-node lf-zero"><circle cx="${C}" cy="${C}" r="${zr}"/><text x="${C}" y="${C + 4}" text-anchor="middle"${st.width > 4 ? ' font-size="8"' : ""}>${bits(0)}</text></g>` +
             `<path class="lf-loop" d="M${C + 12},${C - zr + 4} a 11 11 0 1 1 -24 0" marker-end="url(#lf-arrow)"/></svg>`;
        return s;
      };
      // from 7 bits there is no ring: the strip below lists the states
      const noRing = () => `<p class="ex-note">‏${ltr(states())} מצבים שאינם אפס: יותר מדי לטבעת. רצועת התזמון שמתחת מראה את המצבים שבוקרו, בהקסה.</p>`;
      // the strip: every step so far, the bus in binary up to 6 bits and in hex beyond
      const stripHtml = () => {
        const sp = lfsrStrip(st.mask, st.width, st.k, SEED), hex = st.width > 6;
        const label = (v) => (hex ? `0x${v.toString(16).toUpperCase().padStart(2, "0")}` : bits(v));
        const SW = hex ? 40 : Math.max(36, Math.round(14 + 7.6 * st.width)), n = sp.states.length;
        return waveStrip([
          { name: "clk", kind: "clock" },
          { name: "state", kind: "bus", values: sp.states.map(label) },
          { name: "s[0]", kind: "bit", values: sp.out, cls: "wv-s2" },
          { name: "fb", kind: "bit", values: sp.fb, cls: "wv-s1" },
        ], n, { slotW: SW, cursor: n - 1, ticks: (k) => k, label: `רצועת התזמון של ה-LFSR: ${n} מצבים` });
      };
      const draw = () => {
        const walk = lfsrWalk(st.mask, st.width, SEED), total = walk.period, n = states();
        st.k = Math.min(st.k, total);
        box.querySelectorAll(".ex-tap").forEach((c) => { c.checked = ((st.mask >> (st.width - Number(c.dataset.k))) & 1) === 1; });
        const shown = walk.states.concat(walk.states[walk.back]).slice(0, st.k + 1);
        $(".lf-ring").innerHTML = st.width <= RING_MAX ? ring(walk, shown) : noRing();
        const cur = st.k < total ? walk.states[st.k] : walk.states[walk.back];
        const tapsIdx = [];
        for (let i = 0; i < st.width; i++) if ((st.mask >> i) & 1) tapsIdx.push(i);
        let fb = 0; tapsIdx.forEach((i) => { fb ^= (cur >> i) & 1; });
        const next = lfsrNext(cur, st.mask, st.width);
        $(".ex-pos").textContent = `צעד ${st.k} מתוך ${total}`;
        $(".ex-prev").disabled = st.k === 0;
        $(".lf-poly").innerHTML = `הפולינום ${polyHtml(st.mask)}, המסכה ${code(bits(st.mask))}: היזון חוזר מהביטים ${ltr(tapsIdx.map((i) => `s[${i}]`).join(", "))}.`;
        $(".lf-state").innerHTML = `המצב אחרי ${ltr(st.k)} צעדים: ${code(bits(cur))}` + (st.k === total ? ` — חזר למצב ההתחלה.` : ".");
        $(".lf-fb").innerHTML = `הצעד הבא: ${ltr(`${code("fb")} = ${code(tapsIdx.map((i) => `s[${i}]`).join(" ^ "))} = ${tapsIdx.map((i) => (cur >> i) & 1).join(" ^ ")} = ${fb}`)}, ` +
          `ואז ${ltr(`${code(`(${bits(cur)} >> 1) | (${fb} << ${st.width - 1})`)} = ${code(bits(next))}`)}.`;
        const wrap = $(".lf-strip");
        wrap.innerHTML = stripHtml();
        wrap.scrollLeft = wrap.scrollWidth;                // the current step in view
        const maximal = total === n;
        $(".lf-sum").innerHTML = st.k < total
          ? `בוקרו ${ltr(st.k + 1)} מצבים מתוך ${ltr(n)}. ` + (maximal ? `הפולינום פרימיטיבי: המחזור יהיה ${ltr(n)}.` : `המחזור של הפולינום הזה הוא ${ltr(total)}, ולכן ${ltr(n - total)} מצבים לא יבוקרו לעולם.`)
          : maximal ? `<span class="lf-ok">מחזור מקסימלי: ${ltr(n)} צעדים, כל מצב שאינו אפס פעם אחת ✓</span>`
          : `<span class="lf-bad">מחזור של ${ltr(total)} צעדים בלבד: ${ltr(n - total)} מצבים לא בוקרו.</span>`;
        // the table: every polynomial up to 5 bits, only the primitive ones from 6
        const all = lfsrTable(st.width), prim = lfsrPrimitiveCount(st.width), full = st.width <= FULL_TABLE;
        const rows = full ? all : all.filter((r) => r.period === n);
        $(".lf-table-title").innerHTML = (full
          ? `כל ${ltr(all.length)} הפולינומים ${ltr(`x<sup>${st.width}</sup> + … + 1`)} ואורך המחזור של כל אחד מ-${code(bits(SEED))}`
          : `${ltr(rows.length)} הפולינומים הפרימיטיביים מתוך ${ltr(all.length)} (מחזור ${ltr(n)} מ-${code(bits(SEED))})`) +
          `; לפי הנוסחה ${ltr(`φ(2<sup>${st.width}</sup> − 1) / ${st.width} = φ(${n}) / ${st.width} = ${prim}`)}`;
        $(".lf-table").innerHTML = `<table><thead><tr><th>הפולינום</th><th>המסכה</th><th>אורך המחזור</th></tr></thead><tbody>` +
          rows.map((r) => `<tr class="${r.mask === st.mask ? "is-cur" : ""}${r.period === n ? " is-max" : ""}"><td>${polyHtml(r.mask)}</td><td>${code(bits(r.mask))}</td><td>${ltr(r.period)}${r.period === n ? " ✓" : ""}</td></tr>`).join("") +
          `</tbody></table>`;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => lfsrWalk(st.mask, st.width, SEED).period;
      // a new width: the first primitive polynomial of the table, the question's one at 4
      const setWidth = (w) => {
        stop(); st.width = w; st.k = 0;
        st.mask = w === 4 ? 0b0011 : (lfsrTable(w).find((r) => r.period === states()) || lfsrTable(w)[0]).mask;
        $(".ex-width").value = String(w); tapsHtml(); draw();
      };
      $(".ex-width").addEventListener("change", () => setWidth(Number($(".ex-width").value)));
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { if (st.width !== 4) setWidth(4); stop(); st.mask = Number(b.dataset.mask); st.k = 0; draw(); }));
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
      tapsHtml();
      draw();
    },
  });

  // The divide-by-three box (0035): the page's half-cycle model one clock edge at a time
  // or played; the strip of clk, cnt, a, b and clk_out with the overlap of a and b shaded;
  // the duty measured from the trace; a wake-up in state 3 with the counter as in the
  // module (2 bits, wraps), without a wrap (the Python model) or guarded (>= 2).
  const div3View = () => ({
    mount(box) {
      const st = { k: 0, cnt0: 0, counter: "wrap", N: 3, total: 36 };
      const P = () => div3Params(st.N);
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>מחלק ב-N</span><input type="range" class="ex-n" min="2" max="10" step="1" value="3" dir="ltr" aria-label="המחלק N"><output class="out-n">3</output></label>` +
        `<label>אורך הרצועה <select class="ex-len" aria-label="אורך הרצועה במחזורים"><option value="36" selected>18 מחזורים</option><option value="60">30 מחזורים</option><option value="120">60 מחזורים</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">השפה הבאה</button>` +
        `<button type="button" class="md-button ex-prev">השפה הקודמת</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="900">איטי</option><option value="450" selected>בינוני</option><option value="150">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">איפוס</button>` +
        `<button type="button" class="md-button ex-wake">התעוררות במצב 3</button>` +
        `<label>המונה <select class="ex-counter" aria-label="גרסת המונה"><option value="wrap" class="opt-wrap">2 ביטים, כמו במודול</option><option value="wide">רחב יותר, בלי גלגול</option><option value="guard">מגן: cnt &gt;= 2</option></select></label>` +
        `<span class="ex-pos"></span></div>` +
        `<div class="wv-wrap" tabindex="0" role="group" aria-label="דיאגרמת תזמון של המחלק בשלוש, גלילה אופקית"></div>` +
        `<p class="wv-step" aria-live="polite"></p><p class="ex-summary wv-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let timer = null;
      const draw = () => {
        const { N, bits, from, wake, odd, high } = P(), TOTAL = st.total, wakeState = wake === null ? null : wake;
        const thr = high === 1 ? `${code("cnt")} == ${N - 1}` : `${code("cnt")} >= ${from}`;   // the a condition as text
        const rows = div3Trace(TOTAL, st.cnt0, st.counter, N), shown = rows.slice(0, st.k);
        $(".out-n").textContent = String(N);
        $(".ex-wake").textContent = wake === null ? `אין מצב לא נגיש (${bits} ביט ל-${N} מצבים)` : `התעוררות במצב ${wake}`;
        $(".ex-wake").disabled = wake === null;
        $(".opt-wrap").textContent = `${bits} ביט, כמו במודול`;
        const val = (key) => shown.map((r) => r[key]);
        const strip = [
          { name: "clk", kind: "clock" },
          { name: "cnt", kind: "bus", values: val("cnt") },
          { name: "a", kind: "bit", values: val("a"), cls: "wv-s1" },
          { name: "b", kind: "bit", values: val("b"), cls: "wv-s3" },
          { name: "clk_out", kind: "bit", values: val("out"), cls: "wv-s2", marks: shown.map((r) => r.a && r.b) },
        ];
        if (!odd) strip[4].marks = shown.map(() => 0);   // an even N: the output is a alone, no OR overlap
        $(".wv-wrap").innerHTML = waveStrip(strip, TOTAL, { half: true, label: "דיאגרמת תזמון בחצאי מחזורים", cursor: st.k ? st.k - 1 : null, ticks: (k) => (k % 2 === 0 ? k / 2 : "") });
        $(".ex-pos").textContent = `שפה ${st.k} מתוך ${TOTAL}`;
        $(".ex-prev").disabled = st.k === 0;
        let step;
        const woke = wake !== null && st.cnt0 === wake;
        if (!st.k) step = woke
          ? `המונה התעורר במצב ${wake}, שאינו נגיש אחרי איפוס: ${ltr(`${code("cnt")} = ${wake}`)}, ${ltr(`${code("a")} = 0`)}, ${ltr(`${code("b")} = 0`)}.`
          : `אחרי איפוס: ${ltr(`${code("cnt")} = 0`)}, ${ltr(`${code("a")} = 0`)}, ${ltr(`${code("b")} = 0`)}, והמוצא נמוך.` +
            (N === 3 ? "" : odd ? ` מחלק ב-${ltr(N)}: המונה סופר 0 עד ${ltr(N - 1)} ב-${ltr(bits)} ביט, ${code("a")} גבוה ${ltr(high)} מחזורים (${ltr(thr)}), ${code("b")} מוזז בחצי, והמוצא ${ltr("a | b")} גבוה ${ltr(`${N / 2}`)} מחזורים.`
              : ` מחלק ב-${ltr(N)}, זוגי: ${code("a")} גבוה ${ltr(high)} מתוך ${ltr(N)} מחזורים הוא כבר 50%, ולכן המוצא הוא ${code("a")} לבד; ${code("b")} מצויר אבל לא משתתף (${ltr("a | b")} היה נותן ${ltr(`${high + 0.5}`)} מחזורים).`);
        else {
          const r = rows[st.k - 1], cyc = Math.floor(r.edge / 2);
          if (r.rising) {
            step = `עליית השעון של מחזור ${ltr(cyc)}: ${ltr(`${code("a")} ← (${thr}) = ${r.a}`)}, ו-${ltr(`${code("cnt")} ← ${r.cnt}`)}` +
              (wake !== null && r.cntPrev === wake ? (st.counter === "wide" ? ` (‏${ltr(`${wake} + 1 = ${wake + 1}`)}: בלי גלגול המונה לא חוזר ל-0)` : st.counter === "guard" ? ` (‏${ltr(`${wake} >= ${N - 1}`)}, ולכן חזרה ל-0)` : ` (‏${ltr(`${wake} + 1`)} ב-${ltr(bits)} ביט מתגלגל ל-0)`) : "") + ".";
            if (r.aChanged && r.a) step += ` <span class="wv-ok">‏${code("a")} עלה: המוצא עולה עם עליית השעון.</span>`;
            else if (r.aChanged && !r.a) step += !odd ? ` ${code("a")} ירד: המוצא יורד איתו.` : r.b ? ` <span class="wv-ok">‏${code("a")} ירד, אבל ${code("b")} עדיין 1: ה-OR מחזיק את המוצא גבוה, בלי גליץ'.</span>` : ` ${code("a")} ירד ו-${code("b")} כבר 0: המוצא יורד.`;
          } else {
            step = `ירידת השעון באמצע מחזור ${ltr(cyc)}: ${ltr(`${code("b")} ← ${code("a")} = ${r.b}`)}.`;
            if (!odd) step += ` ‏${code("b")} לא משתתף במוצא כש-${ltr("N")} זוגי.`;
            else if (r.bChanged && r.b) step += ` ‏${code("b")} עלה כש-${code("a")} כבר 1: המוצא כבר גבוה, ואין שינוי בו.`;
            else if (r.bChanged && !r.b) step += ` <span class="wv-ok">‏${code("b")} ירד ו-${code("a")} כבר 0 מחצי מחזור: המוצא יורד בירידת השעון, אחרי ${ltr(`${N / 2}`)} מחזורים גבוה.</span>`;
          }
        }
        $(".wv-step").innerHTML = step;
        const duty = div3Duty(shown);
        let sum;
        if (duty.period === null) {
          const stuck = st.counter === "wide" && woke;
          sum = stuck && st.k >= 6 ? `<span class="wv-bad">המונה ממשיך לספור ${ltr(`${wake + 1}, ${wake + 2}, ${wake + 3}…`)} ולא חוזר ל-${ltr(N - 1)}: ${code("a")} לא עולה לעולם והמוצא תקוע נמוך. זה מה שמודל ה-Python של העמוד היה עושה ממצב ${ltr(wake)}.</span>`
            : `המוצא עוד לא השלים תקופה: ${code("a")} עולה רק אחרי שהמונה מגיע ל-${ltr(from)}.`;
        } else {
          sum = `מהעלייה הראשונה: תקופה של ${ltr(duty.period)} חצאי מחזורים = ${ltr(duty.period / 2)} מחזורים, גבוה ${ltr(duty.high)} מתוכם: duty ${ltr(Math.round((100 * duty.high) / duty.period))}%` +
            (duty.period === 2 * N && duty.high === N && duty.ok ? ` ✓ חלוקה ב-${ltr(N)} עם 50%.` : ".");
        }
        $(".wv-sum").innerHTML = sum;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, st.total); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; st.cnt0 = 0; draw(); });
      $(".ex-wake").addEventListener("click", () => { const w = P().wake; if (w === null) return; stop(); st.k = 0; st.cnt0 = w; draw(); });
      $(".ex-counter").addEventListener("change", () => { stop(); st.counter = $(".ex-counter").value; st.k = 0; draw(); });
      $(".ex-n").addEventListener("input", () => { stop(); st.N = Number($(".ex-n").value); st.k = 0; st.cnt0 = 0; draw(); });
      $(".ex-len").addEventListener("change", () => { stop(); st.total = Number($(".ex-len").value); st.k = Math.min(st.k, st.total); draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, { k: 0, cnt0: 0, counter: "wrap", N: 3, total: 36 }); $(".ex-n").value = 3; $(".ex-len").value = "36"; $(".ex-counter").value = "wrap"; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= st.total) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= st.total) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      draw();
    },
  });

  // The Gray pointer box (0034). data-mode="sync": a step b -> b + 1 of a 4-bit pointer
  // seen through a synchroniser, every changing bit tapped as arrived or not (or drawn
  // at random), in binary and in Gray side by side, for a pointer of 3 to 6 bits.
  // data-mode="flags": a FIFO of 8 to 64 entries with pointers one bit wider than the
  // address, write and read, the pointers in binary and Gray, empty and full by the
  // page's rules.
  const grayView = (box) => ({
    mount() {
      if (box.dataset.mode === "flags") { grayFlagsMount(box); return; }
      const st = { bits: 4, b: 7, arrBin: {}, arrGray: {} };
      let BITS = 4;
      box.innerHTML =
        `<div class="ex-controls"><label>רוחב <select class="ex-bits" aria-label="מספר הביטים של המצביע">${[3, 4, 5, 6].map((w) => `<option value="${w}"${w === 4 ? " selected" : ""}>${w} ביטים</option>`).join("")}</select></label>` +
        `<label><span>המצביע לפני הצעד</span><input type="range" class="ex-b" min="0" max="15" step="1" value="7" dir="ltr" aria-label="המצביע לפני הצעד"><output class="ex-bout"></output></label>` +
        `<button type="button" class="md-button ex-random">הגרלה: אילו ביטים הגיעו</button>` +
        `<button type="button" class="md-button ex-all">הכול הגיע</button>` +
        `<button type="button" class="md-button ex-none">כלום עוד לא הגיע</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
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
        BITS = st.bits;
        const r = graySample(st.b, BITS, st.arrBin, st.arrGray);
        $(".ex-b").max = String((1 << BITS) - 1); $(".ex-b").value = st.b; $(".ex-bout").textContent = String(st.b);
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
      const randomize = (rng) => {
        const r = graySample(st.b, BITS, {}, {});
        st.arrBin = {}; st.arrGray = {};
        r.changedBin.forEach((i) => { st.arrBin[i] = rng() < 0.5 ? 1 : 0; });
        r.changedGray.forEach((i) => { st.arrGray[i] = rng() < 0.5 ? 1 : 0; });
      };
      const setAll = (v) => { for (let i = 0; i < BITS; i++) { st.arrBin[i] = v; st.arrGray[i] = v; } };
      $(".ex-b").addEventListener("input", () => { st.b = Number($(".ex-b").value); draw(); });
      $(".ex-random").addEventListener("click", () => seed.draw());
      $(".ex-all").addEventListener("click", () => { setAll(1); draw(); });
      $(".ex-none").addEventListener("click", () => { setAll(0); draw(); });
      box.addEventListener("click", (e) => {
        const b = e.target.closest(".gr-btn");
        if (!b) return;
        const map = b.dataset.kind === "bin" ? st.arrBin : st.arrGray, i = Number(b.dataset.i);
        map[i] = map[i] ? 0 : 1;
        draw();
      });
      // the page's example: 4 bits, bits 3 and 0 arrived, 2 and 1 did not (1110); in Gray the old value
      const page = () => { st.bits = 4; $(".ex-bits").value = "4"; st.b = 7; st.arrBin = { 3: 1, 0: 1, 2: 0, 1: 0 }; st.arrGray = { 3: 0 }; draw(); };
      $(".ex-reset").addEventListener("click", page);
      // a new width: the step before the wrap (all bits change), nothing arrived yet
      $(".ex-bits").addEventListener("change", () => { st.bits = Number($(".ex-bits").value); st.b = (1 << (st.bits - 1)) - 1; st.arrBin = {}; st.arrGray = {}; draw(); });
      page();
      const seed = seedControls(box, $(".ex-reset"), (rng) => { randomize(rng); draw(); });
    },
  });
  const grayFlagsMount = (box) => {
    const st = { size: 16, w: 0, r: 0, hist: [], ops: [] };
    const KEEP = 64;                                       // columns kept on the strip
    const bitsN = () => Math.log2(st.size) + 1;          // one bit above the address
    box.innerHTML =
      `<div class="ex-controls"><label>עומק ה-FIFO <select class="ex-size" aria-label="מספר הכניסות">${[8, 16, 32, 64].map((v) => `<option value="${v}"${v === 16 ? " selected" : ""}>${v} כניסות</option>`).join("")}</select></label>` +
      `<button type="button" class="md-button md-button--primary ex-write">כתיבה</button>` +
      `<button type="button" class="md-button md-button--primary ex-read">קריאה</button>` +
      `<button type="button" class="md-button ex-write8"></button>` +
      `<button type="button" class="md-button ex-read8"></button>` +
      `<button type="button" class="md-button ex-prev">צעד אחורה</button>` +
      `<button type="button" class="md-button ex-start">איפוס</button></div>` +
      `<div class="gr-slots" dir="ltr" role="img"></div>` +
      `<div class="gr-ptrs"></div><p class="ex-summary gr-sum" aria-live="polite"></p>` +
      `<p class="ex-title">רצועת התזמון: עמודה לכל כתיבה או קריאה, המצביעים אחריה והדגלים</p>` +
      `<div class="wv-wrap gr-strip" tabindex="0" role="group" aria-label="רצועת התזמון של ה-FIFO, גלילה אופקית"></div>`;
    const $ = (sel) => box.querySelector(sel);
    const draw = () => {
      const BITS = bitsN(), SIZE = st.size, half = SIZE / 2, fl = grayFlags(st.w, st.r, BITS);
      $(".ex-write").disabled = fl.full; $(".ex-write8").disabled = fl.full;
      $(".ex-read").disabled = fl.empty; $(".ex-read8").disabled = fl.empty;
      $(".ex-write8").textContent = `${half} כתיבות`; $(".ex-read8").textContent = `${half} קריאות`;
      $(".ex-prev").disabled = !st.hist.length;
      const wa = st.w & (SIZE - 1), ra = st.r & (SIZE - 1);
      let cells = "";
      for (let i = 0; i < SIZE; i++) {
        const filled = ((i - ra) & (SIZE - 1)) < fl.occupancy;
        cells += `<span class="gr-slot${filled ? " is-full" : ""}"><span class="gr-w">${i === wa ? "W" : ""}</span><span class="gr-idx">${i}</span><span class="gr-r">${i === ra ? "R" : ""}</span></span>`;
      }
      const slots = $(".gr-slots");
      slots.innerHTML = cells;
      slots.style.setProperty("--gr-cols", String(Math.min(SIZE, 16)));
      slots.setAttribute("aria-label", `${SIZE} הכניסות של ה-FIFO, המלאות מודגשות, עם מצביעי הכתיבה והקריאה`);
      const split = (v, n) => { const s = bitsOf(v, BITS); return n === 1 ? `<span class="gr-top2">${s[0]}</span>${s.slice(1)}` : `<span class="gr-top">${s[0]}</span><span class="gr-top2">${s[1]}</span>${s.slice(2)}`; };
      $(".gr-ptrs").innerHTML = `<table><thead><tr><th>המצביע</th><th>בינארי (${ltr(BITS)} ביטים)</th><th>‏Gray</th><th>כתובת</th></tr></thead><tbody>` +
        `<tr><td>כתיבה ${code("wptr")}</td><td dir="ltr">${split(st.w, 1)}</td><td dir="ltr">${split(fl.wg, 2)}</td><td>${ltr(wa)}</td></tr>` +
        `<tr><td>קריאה ${code("rptr")}</td><td dir="ltr">${split(st.r, 1)}</td><td dir="ltr">${split(fl.rg, 2)}</td><td>${ltr(ra)}</td></tr></tbody></table>`;
      const wg = bitsOf(fl.wg, BITS), rg = bitsOf(fl.rg, BITS);
      const topFlip = wg.slice(0, 2) === rg.slice(0, 2).replace(/[01]/g, (c) => (c === "0" ? "1" : "0"));
      const low = BITS - 1, lowBits = bitsOf(wa, low);
      let sum = `תפוסה ${ltr(fl.occupancy)} מתוך ${ltr(SIZE)} (ההפרש בין המצביעים מודולו ${ltr(2 * SIZE)}). `;
      sum += fl.empty ? `<span class="gr-ok">ריק ✓</span>: שני ה-Gray שווים (${ltr(wg)} = ${ltr(rg)}). `
        : `ריק? לא: ${ltr(wg)} ≠ ${ltr(rg)}. `;
      sum += fl.full ? `<span class="gr-ok">מלא ✓</span>: שני הביטים העליונים הפוכים (${ltr(wg.slice(0, 2))} מול ${ltr(rg.slice(0, 2))}) ו-${ltr(BITS - 2)} הנמוכים שווים (${ltr(wg.slice(2))}).`
        : `מלא? לא: ` + (topFlip ? `העליונים הפוכים, אבל הנמוכים ${ltr(wg.slice(2))} מול ${ltr(rg.slice(2))}.` : `העליונים ${ltr(wg.slice(0, 2))} מול ${ltr(rg.slice(0, 2))} אינם הפוכים.`);
      if (fl.occupancy === 0 && st.w !== 0) sum += ` בלי הביט הנוסף המצביעים היו ${ltr(lowBits)} ו-${ltr(bitsOf(ra, low))}: שווים, בדיוק כמו במצב מלא.`;
      if (fl.full) sum += ` ${ltr(low)} הביטים הנמוכים של שני המצביעים שווים (${ltr(lowBits)}): בלי הביט הנוסף זה היה נראה ריק.`;
      $(".gr-sum").innerHTML = sum;
      // the strip: the last KEEP columns of the operations so far
      const all = grayFlagsOps(st.ops, SIZE), first = Math.max(0, all.length - KEEP), cols = all.slice(first);
      const SW = Math.round(16 + 7.6 * BITS), n = cols.length;
      const wrapEl = $(".gr-strip");
      wrapEl.innerHTML = waveStrip([
        { name: "wr", kind: "bit", values: cols.map((c) => (c.op === "w" ? 1 : 0)), cls: "wv-s2" },
        { name: "rd", kind: "bit", values: cols.map((c) => (c.op === "r" ? 1 : 0)), cls: "wv-s3" },
        { name: "wptr", kind: "bus", values: cols.map((c) => bitsOf(c.w, BITS)) },
        { name: "wptr Gray", kind: "bus", values: cols.map((c) => bitsOf(c.wg, BITS)) },
        { name: "rptr", kind: "bus", values: cols.map((c) => bitsOf(c.r, BITS)) },
        { name: "rptr Gray", kind: "bus", values: cols.map((c) => bitsOf(c.rg, BITS)) },
        { name: "full", kind: "bit", values: cols.map((c) => (c.full ? 1 : 0)), cls: "wv-s1" },
        { name: "empty", kind: "bit", values: cols.map((c) => (c.empty ? 1 : 0)), cls: "wv-s1" },
      ], n, { slotW: SW, labelW: 84, cursor: n - 1, ticks: (k) => first + k, label: `רצועת התזמון של ה-FIFO: ${n} עמודות` });
      wrapEl.scrollLeft = wrapEl.scrollWidth;
    };
    const step = (dw, dr) => {
      const BITS = bitsN(), wrap = 2 * st.size - 1;
      st.hist.push([st.w, st.r, st.ops.length]); if (st.hist.length > 200) st.hist.shift();
      for (let i = 0; i < dw; i++) if (!grayFlags(st.w, st.r, BITS).full) { st.w = (st.w + 1) & wrap; st.ops.push("w"); }
      for (let i = 0; i < dr; i++) if (!grayFlags(st.w, st.r, BITS).empty) { st.r = (st.r + 1) & wrap; st.ops.push("r"); }
      draw();
    };
    $(".ex-write").addEventListener("click", () => step(1, 0));
    $(".ex-read").addEventListener("click", () => step(0, 1));
    $(".ex-write8").addEventListener("click", () => step(st.size / 2, 0));
    $(".ex-read8").addEventListener("click", () => step(0, st.size / 2));
    $(".ex-prev").addEventListener("click", () => { const h = st.hist.pop(); if (h) { [st.w, st.r] = h; st.ops.length = h[2]; } draw(); });
    $(".ex-start").addEventListener("click", () => { st.w = 0; st.r = 0; st.hist = []; st.ops = []; draw(); });
    $(".ex-size").addEventListener("change", () => { st.size = Number($(".ex-size").value); st.w = 0; st.r = 0; st.hist = []; st.ops = []; draw(); });
    draw();
  };

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
        `<span class="wv-presets">מחירים: <button type="button" class="md-button ex-preset" data-p="page">דוגמת העמוד</button> ` +
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
          s += `<g class="st-pt${cur ? " is-cur" : ""}${i < st.k ? " is-seen" : ""}" data-i="${i}" tabindex="0" role="slider" aria-label="${dayName(i)}: מחיר ${p}, גרירה או חיצים משנים" aria-valuemin="1" aria-valuemax="${PMAX}" aria-valuenow="${p}"><circle cx="${f(X(i))}" cy="${f(Y(p))}" r="9"/><text x="${f(X(i))}" y="${f(Y(p) - 13)}" text-anchor="middle">${p}</text></g>`;
          s += `<text class="tick" x="${f(X(i))}" y="${Y1 + 18}" text-anchor="middle">${i}</text>`;
        });
        s += `<line class="axis" x1="${X0}" x2="${X1}" y1="${Y1}" y2="${Y1}"/></svg>`;
        chart.innerHTML = s;
        $(".ex-pos").textContent = `יום ${st.k} מתוך ${n}`;
        let step;
        if (!fr) step = `לפני היום הראשון: המינימום והמקסימום עד כה הם המחיר של יום 0, והעסקה הטובה ביותר היא 0.`;
        else {
          step = `${dayName(fr.i)}: המחיר ${ltr(fr.p)}. לונג שנסגר היום: ${ltr(`${fr.p} − ${fr.minP} = ${fr.longToday}`)} (קנייה ב${dayName(fr.minI)})` +
            (fr.impL ? ` <span class="wv-ok">✅ הלונג הטוב ביותר עד כה</span>` : fr.longToday <= 0 ? `, לא מרוויח` : `, לא עובר את ${ltr(fr.lb)}`) + `.`;
          if (st.both) step += ` שורט שנסגר היום: ${ltr(`${fr.maxP} − ${fr.p} = ${fr.shortToday}`)} (מכירה ב${dayName(fr.maxI)})` +
            (fr.impS ? ` <span class="wv-ok">✅ השורט הטוב ביותר עד כה</span>` : fr.shortToday <= 0 ? `, לא מרוויח` : `, לא עובר את ${ltr(fr.sb)}`) + `.`;
          const upd = [];
          if (fr.minAfter !== fr.minP) upd.push(`המינימום עד כה הופך ל-${ltr(fr.minAfter)}`);
          if (st.both && fr.maxAfter !== fr.maxP) upd.push(`המקסימום עד כה הופך ל-${ltr(fr.maxAfter)}`);
          step += upd.length ? ` אחרי היום: ${upd.join(", ")}.` : ` המינימום${st.both ? " והמקסימום" : ""} עד כה לא משתנ${st.both ? "ים" : "ה"}.`;
        }
        $(".wv-step").innerHTML = step;
        const L = fr ? { best: fr.lb, open: fr.lo, close: fr.lc } : sc.long, S = fr ? { best: fr.sb, open: fr.so, close: fr.sc } : sc.short;
        let sum = L.best > 0 ? `הלונג הטוב ביותר: רווח ${ltr(L.best)}, קנייה ביום ${ltr(L.open)} ומכירה ביום ${ltr(L.close)}.` : `אין לונג שמרוויח.`;
        if (st.both) {
          sum += S.best > 0 ? ` השורט הטוב ביותר: רווח ${ltr(S.best)}, מכירה ביום ${ltr(S.open)} וקנייה בחזרה ביום ${ltr(S.close)}.` : ` אין שורט שמרוויח.`;
          if (st.k >= n) sum += S.best > L.best ? ` <span class="wv-ok">התשובה: שורט ברווח ${ltr(S.best)}, ימים ${ltr(S.open)} ו-${ltr(S.close)}.</span>` : L.best > 0 ? ` <span class="wv-ok">התשובה: לונג ברווח ${ltr(L.best)}, ימים ${ltr(L.open)} ו-${ltr(L.close)}.</span>` : ` <span class="wv-ok">התשובה: רווח 0, בלי עסקה.</span>`;
        } else if (st.k >= n) sum += L.best > 0 ? ` <span class="wv-ok">התשובה: רווח ${ltr(L.best)}, ימים ${ltr(L.open)} ו-${ltr(L.close)}.</span>` : ` <span class="wv-ok">התשובה: רווח 0, בלי ימים.</span>`;
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

  // The handshake box (0038): draw req and ack cell by cell on a timing strip; the four
  // rules of the page's reference model are evaluated every cycle, a failure marked on
  // the row of its assertion at the cycle the SVA reports it; the page's traces as presets.
  const handshakeView = () => ({
    mount(box) {
      const N = 12, MAX_WAIT = 3;
      const RULES = [
        ["hold", "a_req_holds", "חוק 1, req מחזיק"],
        ["late", "a_ack_in_time", "חוק 2, ack בזמן"],
        ["orphan", "a_no_orphan_ack", "חוק 3, אין ack יתום"],
        ["drop", "a_req_drops", "חוק 4, req יורד אחרי ack"],
      ];
      const st = { req: hsWave(HS_PRESETS.ok[0], N), ack: hsWave(HS_PRESETS.ok[1], N), cur: 3 };
      box.innerHTML =
        `<div class="ex-controls"><span class="wv-presets">הדיאגרמות שבעמוד: ` +
        `<button type="button" class="md-button ex-preset" data-p="ok">עסקה תקינה</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="late">ack מאוחר</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="drop">req נופל</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="orphan">ack יתום</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="clear">ניקוי</button></span></div>` +
        `<p class="wv-hint">לחיצה על משבצת של ${code("req")} או ${code("ack")} הופכת את הערך שלה באותו מחזור. ✗ בשורה של assertion הוא המחזור שבו היא מדווחת על כישלון.</p>` +
        `<div class="wv-wrap" tabindex="0" role="group" aria-label="דיאגרמת תזמון של לחיצת הידיים וארבע שורות ה-assertions, גלילה אופקית"></div>` +
        `<p class="wv-step" aria-live="polite"></p><p class="ex-summary wv-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const draw = () => {
        const fails = hsCheck(st.req, st.ack, MAX_WAIT);
        const rows = [
          { name: "clk", kind: "clock" },
          { name: "req", kind: "bit", values: st.req, cls: "wv-s1", cells: (k) => `מחזור ${k}: req = ${st.req[k]}, לחיצה הופכת` },
          { name: "ack", kind: "bit", values: st.ack, cls: "wv-s3", cells: (k) => `מחזור ${k}: ack = ${st.ack[k]}, לחיצה הופכת` },
        ].concat(RULES.map(([key, name]) => ({ name, kind: "flag", values: st.req.map((_, k) => (fails[key].includes(k) ? 1 : 0)) })));
        $(".wv-wrap").innerHTML = waveStrip(rows, N, { role: "group", label: "דיאגרמת תזמון", labelW: 130, cursor: st.cur, ticks: (k) => k });
        const t = st.cur, req = st.req, ack = st.ack;
        const prevReq = t ? req[t - 1] : 0, prevAck = t ? ack[t - 1] : 0;
        const lines = [];
        if (t && prevReq && !prevAck) lines.push(`חוק 1: במחזור ${ltr(t - 1)} ‏${code("req")} היה גבוה בלי ${code("ack")}, ולכן ${code("req")} חייב להישאר גבוה עכשיו: ` + (req[t] ? `<span class="wv-ok">✓</span>` : `<span class="wv-bad">✗ ${code("req")} נפל לפני ${code("ack")}</span>`));
        if (req[t] && !prevReq) {
          const win = ack.slice(t + 1, t + 1 + MAX_WAIT);
          lines.push(`חוק 2: ${code("req")} עלה עכשיו (‏${code("$rose(req)")}), ולכן ${code("ack")} חייב להגיע במחזורים ${ltr(`${t + 1}..${t + MAX_WAIT}`)}: ` +
            (win.some((v) => v) ? `<span class="wv-ok">✓ מגיע במחזור ${ltr(t + 1 + win.findIndex((v) => v))}</span>` : win.length < MAX_WAIT ? `החלון עוד פתוח בסוף הרצף` : `<span class="wv-bad">✗ החלון נסגר בלי ack, הכישלון מדווח במחזור ${ltr(t + MAX_WAIT)}</span>`));
        }
        if (fails.late.includes(t)) lines.push(`חוק 2: כאן נסגר החלון של העלייה במחזור ${ltr(t - MAX_WAIT)} בלי ${code("ack")}: <span class="wv-bad">✗ ack מאוחר</span>`);
        if (ack[t]) lines.push(`חוק 3: ${code("ack")} גבוה, ולכן ${code("req")} חייב להיות גבוה באותה דגימה: ` + (req[t] ? `<span class="wv-ok">✓</span>` : `<span class="wv-bad">✗ ack יתום</span>`));
        if (t && prevAck) lines.push(`חוק 4: במחזור ${ltr(t - 1)} היה ${code("ack")}, ולכן ${code("req")} חייב להיות נמוך עכשיו: ` + (!req[t] ? `<span class="wv-ok">✓</span>` : `<span class="wv-bad">✗ req נשאר גבוה אחרי ack</span>`));
        $(".wv-step").innerHTML = `מחזור ${ltr(t)}: ${ltr(`req = ${req[t]}, ack = ${ack[t]}`)}. ` + (lines.length ? lines.join(" ") : `אף property לא נבדקת במחזור הזה (אין אנטצדנט).`);
        const total = RULES.reduce((a, [key]) => a + fails[key].length, 0);
        $(".wv-sum").innerHTML = total === 0
          ? `<span class="wv-ok">כל ארבע ה-properties מרוצות ✓</span>` + (req.some((v) => v) ? "" : ` (ובלי אף ${code("req")} הן מרוצות באופן ריק: vacuous pass)`)
          : `<span class="wv-bad">${ltr(total)} ${total === 1 ? "הפרה" : "הפרות"}:</span> ` + RULES.filter(([key]) => fails[key].length).map(([key, name, heb]) => `${heb} (${code(name)}) במחזור${fails[key].length > 1 ? "ים" : ""} ${ltr(fails[key].join(", "))}`).join("; ") + `.`;
      };
      const wrap = $(".wv-wrap");
      const tap = (c) => {
        const k = Number(c.dataset.k), row = c.getAttribute("aria-label").includes("req") ? st.req : st.ack;
        row[k] = row[k] ? 0 : 1; st.cur = k; draw();
      };
      wrap.addEventListener("click", (e) => { const c = e.target.closest(".wv-cell"); if (c) tap(c); });
      wrap.addEventListener("keydown", (e) => {
        const c = e.target.closest(".wv-cell");
        if (c && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); tap(c); }
      });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => {
        const p = b.dataset.p;
        if (p === "clear") { st.req = new Array(N).fill(0); st.ack = new Array(N).fill(0); st.cur = 0; }
        else { st.req = hsWave(HS_PRESETS[p][0], N); st.ack = hsWave(HS_PRESETS[p][1], N); const fl = hsCheck(st.req, st.ack, MAX_WAIT); const first = Object.values(fl).flat().sort((a, b) => a - b)[0]; st.cur = first === undefined ? 3 : first; }
        draw();
      }));
      draw();
    },
  });

  // The Ack/Nak box (0025): the RC and the EP side by side with the two link queues
  // between them; free event buttons (a new TLP, the head of each queue delivered,
  // corrupted or lost, the two timers) and the page's two examples as scripts stepped
  // through with the same engine.
  const acknakView = () => ({
    mount(box) {
      const st = { start: 4094, history: [], script: null, pos: 0, state: null, log: null, th: [], seed: newSeed(), unit: null, draws: 0, mode: "free" };
      // the EP's thresholds: the script's list first, then the seeded generator; the
      // history keeps the list and the draw count, so "previous" then "next" redraws the same
      const draw4 = () => { if (st.th.length) return st.th.shift(); st.draws += 1; return 1 + Math.floor(st.unit() * 4); };
      const rewind = (draws) => { st.unit = mulberry32(st.seed); st.draws = 0; while (st.draws < draws) draw4(); };
      const reset = (start, script) => {
        st.start = start; st.script = script || null; st.pos = 0; st.th = script ? [...script.thresholds] : [];
        rewind(0);
        st.state = anInit(start, draw4); st.history = []; st.dropped = 0; st.log = null; render();
      };
      // a step: the state before it (and the script position) go to the history, so
      // "previous" restores both; a free event leaves the script
      const apply = (ev, scripted) => {
        if (!scripted && st.script) { st.script = null; st.th = []; }
        st.history.push({ state: st.state, log: st.log, pos: st.pos, th: [...st.th], draws: st.draws });
        if (st.history.length > 300) { st.history.shift(); st.dropped = (st.dropped || 0) + 1; }
        if (scripted) st.pos += 1;
        const r = anApply(st.state, ev, draw4);
        st.state = r.state; st.log = r.log; render();
      };
      box.innerHTML =
        `<div class="ex-controls"><span class="wv-presets">הדוגמאות שבעמוד: ` +
        `<button type="button" class="md-button ex-preset" data-p="a">סעיף א</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="b">סעיף ב</button></span>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא בתסריט</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1000, 400) +
        `<button type="button" class="md-button ex-end">לסוף התסריט</button><span class="ex-pos"></span>` +
        `<label>מתחילים מ-<select class="ex-start" aria-label="המספר הראשון"><option value="4094" selected>4094 (לפני הגלישה)</option><option value="0">0</option></select></label>` +
        `<button type="button" class="md-button ex-reset">איפוס</button></div>` +
        `<div class="ex-controls an-free"><span class="ex-title">אירועים חופשיים:</span>` +
        `<button type="button" class="md-button ex-send">ה-RC שולח TLP</button>` +
        `<button type="button" class="md-button ex-flush">טיימר ה-Ack פג</button>` +
        `<button type="button" class="md-button ex-timeout">ה-REPLAY_TIMER פג</button></div>` +
        randomRow("שיעור התקלות", "תנועה אקראית (כמו ה-test של העמוד):") +
        `<div class="an-box"><div class="an-side an-rc"></div><div class="an-link"></div><div class="an-side an-ep"></div></div>` +
        `<p class="ex-title">ציר האירועים: עמודה לכל אירוע, המונים אחריו, ו-✗ כשאינווריאנט נופל</p><div class="wv-wrap an-strip" tabindex="0" role="group" aria-label="ציר האירועים, גלילה אופקית"></div>` +
        `<p class="wv-step an-log" aria-live="polite"></p><p class="ex-summary an-sum"></p><p class="ex-note an-rand"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const chips = (items, cls) => (items.length ? items.map((t) => `<span class="an-chip${t.cls ? " " + t.cls : ""}">${t.text}</span>`).join("") : `<span class="an-empty">ריק</span>`);
      const field = (name, value, changed) => `<div class="an-field${changed ? " is-changed" : ""}"><span class="an-name">${name}</span><span class="an-val">${value}</span></div>`;
      const render = () => {
        const s = st.state, prev = st.history.length ? st.history[st.history.length - 1].state : null;
        const ch = (key) => prev && JSON.stringify(prev[key]) !== JSON.stringify(s[key]);
        $(".an-rc").innerHTML = `<p class="an-title">ה-RC, המשדר</p>` +
          field("NEXT_TRANSMIT_SEQ", ltr(s.nts), ch("nts")) + field("ACKD_SEQ", ltr(s.ackd), ch("ackd")) +
          `<div class="an-field${ch("retry") ? " is-changed" : ""}"><span class="an-name">Retry Buffer</span><span class="an-chips" dir="ltr">${chips(s.retry.map((t) => ({ text: t.seq })))}</span></div>` +
          `<p class="an-counts">‏DLLPs פגומים: ${ltr(s.badDllp)}, שגיאות פרוטוקול: ${ltr(s.proto)}, ‏Replays: ${ltr(s.replays)}</p>`;
        $(".an-ep").innerHTML = `<p class="an-title">ה-EP, המקבל</p>` +
          field("NEXT_RCV_SEQ", ltr(s.nrs), ch("nrs")) + field("ממתינים / סף", ltr(`${s.pending} / ${s.threshold}`), ch("pending") || ch("threshold")) +
          field("NAK_SCHEDULED", s.nak ? "1" : "0", ch("nak")) +
          `<div class="an-field${ch("received") ? " is-changed" : ""}"><span class="an-name">נמסרו ל-TL</span><span class="an-chips" dir="ltr">${chips(s.received.slice(-8).map((q) => ({ text: q, cls: "is-done" })))}${s.received.length > 8 ? `<span class="an-empty">…</span>` : ""}</span></div>` +
          `<p class="an-counts">‏TLPs פגומים או מוקדמים: ${ltr(s.badTlp)}, כפולים: ${ltr(s.dups)}</p>`;
        const headBtns = (kind, empty) => `<span class="an-head-btns">` +
          `<button type="button" class="md-button an-act" data-q="${kind}" data-how="ok" ${empty ? "disabled" : ""}>מסור</button>` +
          `<button type="button" class="md-button an-act" data-q="${kind}" data-how="bad" ${empty ? "disabled" : ""}>מסור עם CRC שגוי</button>` +
          `<button type="button" class="md-button an-act" data-q="${kind}" data-how="lose" ${empty ? "disabled" : ""}>אבד</button></span>`;
        $(".an-link").innerHTML =
          `<div class="an-queue"><p class="an-qtitle">‏TLPs בדרך אל ה-EP ←</p><div class="an-chips" dir="ltr">${chips(s.link.map((t, i) => ({ text: `${t.seq}${t.replay ? " R" : ""}`, cls: (i === 0 ? "is-head" : "") + (t.replay ? " is-replay" : "") })))}</div>${headBtns("tlp", !s.link.length)}</div>` +
          `<div class="an-queue"><p class="an-qtitle">→ ‏DLLPs בדרך אל ה-RC</p><div class="an-chips" dir="ltr">${chips(s.dllps.map((d, i) => ({ text: `${d.kind === "ACK" ? "Ack" : "Nak"} ${d.seq}`, cls: (i === 0 ? "is-head" : "") + (d.kind === "NAK" ? " is-nak" : "") })))}</div>${headBtns("dllp", !s.dllps.length)}</div>`;
        const scripted = !!st.script, left = scripted ? st.script.steps.length - st.pos : 0;
        $(".ex-next").disabled = !scripted || left === 0;
        $(".ex-play").disabled = !scripted;
        $(".ex-prev").disabled = !st.history.length;
        $(".ex-pos").textContent = scripted ? `צעד ${st.pos} מתוך ${st.script.steps.length}` : "";
        $(".an-log").innerHTML = st.log ? logText(st.log) : `מצב התחלתי: ${ltr(`ACKD_SEQ = ${s.ackd}`)} הוא "לפני ${ltr(s.nts)}", ה-Retry Buffer ריק, וה-EP מצפה ל-${ltr(s.nrs)} עם סף Ack ${ltr(s.threshold)} שהגריל.`;
        const strip = $(".an-strip");
        strip.innerHTML = eventStrip(st, (S) => [
          { name: "NTS", kind: "bus", values: S.map((x) => x.nts) },
          { name: "ACKD_SEQ", kind: "bus", values: S.map((x) => x.ackd) },
          { name: "NRS", kind: "bus", values: S.map((x) => x.nrs) },
          { name: "retry", kind: "bus", values: S.map((x) => x.retry.length) },
          { name: "NAK_SCHED", kind: "bit", values: S.map((x) => (x.nak ? 1 : 0)), cls: "wv-s2" },
        ], anEventLabel, anInvariants);
        strip.scrollLeft = strip.scrollWidth;
        const bad = anInvariants(s);
        $(".an-sum").innerHTML = (!bad.includes("retry") ? `<span class="wv-ok">✓ ה-Retry Buffer מכיל בדיוק את ${ltr("ACKD_SEQ + 1")} עד ${ltr("NEXT_TRANSMIT_SEQ − 1")}.</span>` : `<span class="wv-bad">✗ ה-Retry Buffer אינו הרצף מ-ACKD_SEQ + 1.</span>`) +
          ` ` + (!bad.includes("order") ? `<span class="wv-ok">✓ ה-TLPs נמסרו בסדר, בלי חור ובלי כפילות.</span>` : `<span class="wv-bad">✗ המסירה אינה בסדר.</span>`);
        $(".ex-end").disabled = !scripted || left === 0;
        const rd = st.script && st.script.random;
        $(".an-rand").innerHTML = rd ? randNote(rd, st.seed, `ובהם ${ltr(rd.faults.lost)} פקטים שאבדו ו-${ltr(rd.faults.bad)} שהגיעו עם CRC שגוי`,
          { retry: "אינווריאנט ה-Retry Buffer", order: "סדר המסירה" }, "שני האינווריאנטים נבדקו אחרי כל אירוע.") : "";
      };
      const logText = (log) => {
        const seqs = (a) => ltr(a.join(", "));
        const parts = log.items.map((it) => {
          switch (it.out) {
            case "sent": return `‏TLP ${ltr(it.seq)} יצא לקישור ועותק שלו נשמר ב-Retry Buffer.`;
            case "accepted": return `‏TLP ${ltr(it.seq)}${it.replay ? " (Replay)" : ""} הוא הצפוי: נמסר ל-Transaction Layer, ו-NEXT_RCV_SEQ מתקדם.`;
            case "ack": return `<span class="wv-ok">הספירה הגיעה לסף, יוצא Ack ${ltr(it.seq)} (מצטבר) וסף חדש מוגרל.</span>`;
            case "nak": return `<span class="wv-bad">יוצא Nak ${ltr(it.seq)}: הכול עד ${ltr(it.seq)} התקבל, מה שאחריו לא. NAK_SCHEDULED נדלק.</span>`;
            case "nakHeld": return `‏Nak כבר נשלח על הפער הזה, ולכן לא יוצא עוד אחד (בלי סופת Nak-ים).`;
            case "badTlp": return `<span class="wv-bad">‏TLP ${ltr(it.seq)} הגיע עם LCRC שגוי: נזרק, המצב לא משתנה.</span>`;
            case "dup": return `‏TLP ${ltr(it.seq)} ישן (כבר נמסר): נזרק, ויוצא Ack חוזר כדי שהמשדר ינקה את ה-Retry Buffer.`;
            case "future": return `<span class="wv-bad">‏TLP ${ltr(it.seq)} הגיע לפני זמנו (מצפים ל-${ltr(it.expected)}): נזרק.</span>`;
            case "lost": return `${it.kind ? (it.kind === "ACK" ? "Ack" : "Nak") + " " + ltr(it.seq) : "‏TLP " + ltr(it.seq)} אבד על הקו: אף צד לא יודע על זה עדיין.`;
            case "badDllp": return `<span class="wv-bad">${it.kind === "ACK" ? "Ack" : "Nak"} ${ltr(it.seq)} הגיע עם CRC שגוי: לא סומכים לא על הסוג ולא על המספר, נזרק.</span>`;
            case "purged": return `<span class="wv-ok">${it.kind === "ACK" ? "Ack" : "Nak"} ${ltr(it.seq)} מצטבר: ${seqs(it.seqs)} נמחקים מה-Retry Buffer ו-ACKD_SEQ הופך ל-${ltr(it.seq)}.</span>`;
            case "noProgress": return `${it.kind === "ACK" ? "Ack" : "Nak"} ${ltr(it.seq)} שווה ל-ACKD_SEQ: אין התקדמות, המצב לא משתנה.`;
            case "protoErr": return `<span class="wv-bad">${it.kind === "ACK" ? "Ack" : "Nak"} ${ltr(it.seq)} לא ב-Retry Buffer ולא ACKD_SEQ: שגיאת פרוטוקול, נזרק ונספר.</span>`;
            case "replay": return `<span class="wv-ok">‏Replay: ${seqs(it.seqs)} יוצאים שוב לקישור מהעותקים השמורים, עם המספרים המקוריים.</span>`;
            case "nothingToReplay": return `אין מה לשדר מחדש: ה-Retry Buffer ריק.`;
            case "flushNak": return `הטיימר פג, אבל Nak תלוי ועומד: לא יוצא Ack.`;
            case "flushNothing": return `הטיימר פג ואין TLPs שממתינים ל-Ack.`;
            case "emptyLink": return `התור ריק.`;
            default: return "";
          }
        });
        return parts.join(" ");
      };
      const nextStep = () => { if (st.script && st.pos < st.script.steps.length) apply(st.script.steps[st.pos], true); };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: nextStep,
        done: () => !st.script || st.pos >= st.script.steps.length,
        restart: () => { if (st.script) reset(st.start, st.script); },
      });
      $(".ex-next").addEventListener("click", () => { stop(); nextStep(); });
      $(".ex-end").addEventListener("click", () => { stop(); while (st.script && st.pos < st.script.steps.length) nextStep(); });
      $(".ex-prev").addEventListener("click", () => { stop(); const h = st.history.pop(); if (h) { st.state = h.state; st.log = h.log; st.pos = h.pos; st.th = h.th; rewind(h.draws); render(); } });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { stop(); reset(AN_SCRIPTS[b.dataset.p].start, AN_SCRIPTS[b.dataset.p]); $(".ex-start").value = "4094"; }));
      $(".ex-reset").addEventListener("click", () => { st.mode = "free"; seed.draw(); });
      $(".ex-start").addEventListener("change", () => { stop(); reset(Number($(".ex-start").value), null); });
      // the random run: a script drawn from the seed, replayed with the script controls
      const runRandom = () => {
        stop();
        const script = anRandomScript(Number($(".ex-start").value), Number($(".ex-count").value), Number($(".ex-rate").value) / 100, mulberry32(st.seed));
        reset(script.start, script);
      };
      $(".ex-run").addEventListener("click", () => { st.mode = "run"; seed.draw(); });
      $(".ex-rate").addEventListener("input", () => { $(".out-rate").textContent = `${$(".ex-rate").value}%`; if (st.script && st.script.random) runRandom(); });
      $(".ex-count").addEventListener("change", () => { if (st.script && st.script.random) runRandom(); });
      $(".ex-send").addEventListener("click", () => { stop(); apply({ type: "send", n: 1 }); });
      $(".ex-flush").addEventListener("click", () => { stop(); apply({ type: "flush" }); });
      $(".ex-timeout").addEventListener("click", () => { stop(); apply({ type: "timeout" }); });
      box.addEventListener("click", (e) => { const b = e.target.closest(".an-act"); if (b) { stop(); apply({ type: b.dataset.q, how: b.dataset.how }); } });
      reset(4094, AN_SCRIPTS.a);
      const seed = seedControls(box, $(".ex-run"), (rng, n) => { stop(); st.seed = n; if (st.mode === "run") runRandom(); else reset(Number($(".ex-start").value), null); }, { seed: st.seed, state: {
        get: () => (st.script && st.script.random ? `r${$(".ex-count").value}.${$(".ex-rate").value}.${st.seed}` : null),
        set: (p) => {
          const m = RAND_HASH.exec(p);
          if (!m || Number(m[2]) > 50 || Number(m[2]) % 5 || Number(m[3]) < 1 || Number(m[3]) > SEED_MAX) return false;
          $(".ex-count").value = m[1]; $(".ex-rate").value = m[2]; $(".out-rate").textContent = `${m[2]}%`;
          st.seed = Number(m[3]); $(".ex-seed").value = st.seed; st.mode = "run"; runRandom(); return true;
        },
      } });
    },
  });

  // The credits box (0024): the four counters as hands on one modulo-256 circle (the
  // credits are the arc from PCC to PCL, the free slots the arc from PCR to PCA), the
  // dedicated buffer, the packets in flight, and the counters in a table; free events
  // and the page's two examples as scripts. A start near 250 shows the wrap.
  const creditsView = () => ({
    mount(box) {
      const st = { size: 5, base: 0, script: null, pos: 0, state: null, log: null, history: [], seed: newSeed() };
      const reset = (script) => { st.script = script || null; st.pos = 0; st.state = crInit(st.size, st.base); st.history = []; st.dropped = 0; st.log = null; render(); };
      const apply = (ev, scripted) => {
        if (!scripted && st.script) st.script = null;
        st.history.push({ state: st.state, log: st.log, pos: st.pos }); if (st.history.length > 300) { st.history.shift(); st.dropped = (st.dropped || 0) + 1; }
        if (scripted) st.pos += 1;
        const r = crApply(st.state, ev); st.state = r.state; st.log = r.log; render();
      };
      box.innerHTML =
        `<div class="ex-controls"><span class="wv-presets">הדוגמאות שבעמוד: ` +
        `<button type="button" class="md-button ex-preset" data-p="a">סעיף א</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="b">סעיף ב</button></span>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא בתסריט</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1000, 400) +
        `<button type="button" class="md-button ex-end">לסוף התסריט</button><span class="ex-pos"></span>` +
        `<label>גודל ה-buffer <select class="ex-size" aria-label="גודל ה-buffer">${[3, 4, 5, 6, 8].map((v) => `<option value="${v}"${v === 5 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<label><input type="checkbox" class="ex-wrap"> <span>להתחיל מ-250 (הגלישה)</span></label>` +
        `<button type="button" class="md-button ex-reset">איפוס</button></div>` +
        `<div class="ex-controls an-free"><span class="ex-title">אירועים חופשיים:</span>` +
        `<button type="button" class="md-button cr-act" data-ev="grant">Credit Grant</button>` +
        `<button type="button" class="md-button cr-act" data-ev="transmit">ה-Egress משדר פקטה</button>` +
        `<button type="button" class="md-button cr-act" data-ev="receive" data-how="ok">הפקטה הבאה התקבלה</button>` +
        `<button type="button" class="md-button cr-act" data-ev="receive" data-how="lose">הפקטה הבאה אבדה</button>` +
        `<button type="button" class="md-button cr-act" data-ev="dequeue">פקטה יוצאת מה-buffer</button>` +
        `<button type="button" class="md-button cr-act" data-ev="sync">Path Credit Sync</button></div>` +
        randomRow("שיעור האובדן", "תנועה אקראית (כמו ה-test של העמוד, אירועים חוקיים בלבד):") +
        `<div class="cr-box"><div class="cr-circle"></div><div class="cr-panel"><div class="cr-table"></div><p class="cr-buf"></p><p class="cr-link"></p></div></div>` +
        `<p class="ex-title">ציר האירועים: עמודה לכל אירוע, המונים אחריו, ו-✗ כשאינווריאנט נופל</p><div class="wv-wrap an-strip" tabindex="0" role="group" aria-label="ציר האירועים, גלילה אופקית"></div>` +
        `<p class="wv-step an-log" aria-live="polite"></p><p class="ex-summary an-sum"></p><p class="ex-note an-rand"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const circle = (s) => {
        const C = 150, R = 110, ang = (v) => -Math.PI / 2 + (v / CR_MOD) * 2 * Math.PI;
        const pt = (v, r) => [C + r * Math.cos(ang(v)), C + r * Math.sin(ang(v))];
        const arc = (a, b, r, cls) => {
          const d = crDist(a, b); if (d === 0) return "";
          const [x1, y1] = pt(a, r), [x2, y2] = pt(b, r);
          return `<path class="${cls}" d="M${f(x1)},${f(y1)} A${r},${r} 0 ${d > 128 ? 1 : 0} 1 ${f(x2)},${f(y2)}"/>`;
        };
        let g = `<svg class="cr-live" viewBox="0 0 300 300" role="img" aria-label="מעגל של 256 ערכים עם ארבעת המונים; הקשת מ-PCC ל-PCL היא הקרדיטים, הקשת מ-PCR ל-PCA היא התאים הפנויים לפי ה-Ingress">` +
          `<circle class="cr-ring" cx="${C}" cy="${C}" r="${R}"/>`;
        for (let v = 0; v < CR_MOD; v += 32) { const [x1, y1] = pt(v, R - 5), [x2, y2] = pt(v, R + 5); g += `<line class="cr-tick" x1="${f(x1)}" y1="${f(y1)}" x2="${f(x2)}" y2="${f(y2)}"/><text class="cr-ticktext" x="${f(pt(v, R + 17)[0])}" y="${f(pt(v, R + 17)[1] + 4)}" text-anchor="middle">${v}</text>`; }
        g += arc(s.pcc, s.pcl, R - 14, "cr-arc cr-arc-credits") + arc(s.pcr, s.pca, R - 28, "cr-arc cr-arc-free");
        // the labels sit at four different radii, so equal counters still read
        const hand = (v, r, cls, name, lr) => { const [x, y] = pt(v, r), [lx, ly] = pt(v, lr); return `<line class="cr-hand ${cls}" x1="${C}" y1="${C}" x2="${f(x)}" y2="${f(y)}"/><circle class="cr-dot ${cls}" cx="${f(x)}" cy="${f(y)}" r="5"/><text class="cr-label ${cls}" x="${f(lx)}" y="${f(ly + 4)}" text-anchor="middle">${name}</text>`; };
        g += hand(s.pcr, R - 28, "cr-pcr", "PCR", 24) + hand(s.pcc, R - 14, "cr-pcc", "PCC", 46) + hand(s.pcl, R - 14, "cr-pcl", "PCL", 68) + hand(s.pca, R - 28, "cr-pca", "PCA", 92);
        return g + `</svg><p class="cr-legend"><span class="cr-lg cr-lg-s1">‏PCC מלא, ‏PCL מקווקו: ה-Egress</span> <span class="cr-lg cr-lg-s2">‏PCR מלא, ‏PCA מקווקו: ה-Ingress</span></p>`;
      };
      const render = () => {
        const s = st.state, prev = st.history.length ? st.history[st.history.length - 1].state : null;
        const ch = (k) => prev && prev[k] !== s[k];
        $(".cr-circle").innerHTML = circle(s);
        const credits = crDist(s.pcc, s.pcl), free = crDist(s.pcr, s.pca);
        const row = (k, name, meaning) => `<div class="an-field${ch(k) ? " is-changed" : ""}"><span class="an-name">${name}</span><span class="an-val">${ltr(s[k])}</span><span class="cr-meaning">${meaning}</span></div>`;
        $(".cr-table").innerHTML = row("pcc", "PCC", "‏Egress: פקטות ששודרו") + row("pcl", "PCL", "‏Egress: ה-Grant האחרון") +
          row("pcr", "PCR", "‏Ingress: פקטות שנכנסו ל-buffer") + row("pca", "PCA", "‏Ingress: תאים שהוקצו מאז ההקמה") +
          `<p class="cr-derived">קרדיטים ${ltr(`= PCL − PCC = ${credits}`)}; תאים פנויים לפי ה-Ingress ${ltr(`= PCA − PCR = ${free}`)}.</p>`;
        let cells = ""; for (let i = 0; i < s.size; i++) cells += `<span class="cr-slot${i < s.occ ? " is-full" : ""}"></span>`;
        $(".cr-buf").innerHTML = `ה-buffer הייעודי (${ltr(s.size)} תאים, תפוסה ${ltr(s.occ)}): <span class="cr-slots" dir="ltr">${cells}</span>`;
        $(".cr-link").innerHTML = `פקטות בדרך אל ה-Ingress: <span class="an-chips" dir="ltr">${s.link.length ? s.link.map((id, i) => `<span class="an-chip${i === 0 ? " is-head" : ""}">${id}</span>`).join("") : `<span class="an-empty">אין</span>`}</span>`;
        box.querySelectorAll(".cr-act").forEach((b) => {
          const ev = b.dataset.ev;
          b.disabled = (ev === "receive" && !s.link.length) || (ev === "transmit" && !crCanTransmit(s)) || (ev === "dequeue" && !s.occ);
        });
        const scripted = !!st.script;
        $(".ex-next").disabled = !scripted || st.pos >= st.script.steps.length;
        $(".ex-end").disabled = !scripted || st.pos >= st.script.steps.length;
        $(".ex-play").disabled = !scripted;
        $(".ex-prev").disabled = !st.history.length;
        $(".ex-pos").textContent = scripted ? `צעד ${st.pos} מתוך ${st.script.steps.length}` : "";
        $(".an-log").innerHTML = st.log ? st.log.items.map(logText).join(" ") : `הקמת הנתיב: ${ltr(`PCA = ${s.pca}`)} הוא גודל ה-buffer${s.pca !== s.size ? " מעל נקודת ההתחלה" : ""}, ושאר המונים ב-${ltr(s.pcc)}. ‏PCL עדיין ${ltr(s.pcl)}, ולכן אין קרדיטים עד ה-Credit Grant הראשון.`;
        // the balance against the buffer: credits + in flight never exceed the free slots;
        // the gap is slots not yet granted plus packets lost and not yet synced
        const strip = $(".an-strip");
        strip.innerHTML = eventStrip(st, (S) => [
          { name: "PCC", kind: "bus", values: S.map((x) => x.pcc) },
          { name: "PCL", kind: "bus", values: S.map((x) => x.pcl) },
          { name: "PCR", kind: "bus", values: S.map((x) => x.pcr) },
          { name: "PCA", kind: "bus", values: S.map((x) => x.pca) },
          { name: "credits", kind: "bus", values: S.map((x) => crDist(x.pcc, x.pcl)) },
          { name: "occupancy", kind: "bus", values: S.map((x) => x.occ) },
        ], crEventLabel, crInvariants);
        strip.scrollLeft = strip.scrollWidth;
        const b = crBalance(s), bad = crInvariants(s);
        const gap = [];
        if (b.ungranted) gap.push(`${ltr(b.ungranted)} תאים שהתפנו ומחכים ל-Grant`);
        if (b.leak > 0) gap.push(`<b>דליפה</b>: ${ltr(b.leak)} פקטות אבדו ולא סונכרנו, ולכן ${ltr(b.leak)} תאים פנויים בלי קרדיט עד ה-Path Credit Sync הבא`);
        $(".an-sum").innerHTML = (crCanTransmit(s) ? `<span class="wv-ok">מותר לשדר: ${ltr(credits)} קרדיטים (מרחק 1 עד 127 קדימה מ-PCC ל-PCL).</span>` : `<span class="wv-bad">אסור לשדר: ${credits === 0 ? "הקרדיטים אזלו, PCL = PCC" : "PCL מאחורי PCC על המעגל (Grant ישן או מושחת)"}.</span>`) +
          ` ` + (bad.includes("overflow") ? `<span class="wv-bad">✗ ${s.occ > s.size ? "ה-buffer גלש" : `${ltr(s.errors)} הפרות של הסביבה (שידור בלי קרדיט, גלישה או הוצאה מ-buffer ריק)`}.</span> ` : "") +
          (bad.includes("credits")
            ? `<span class="wv-bad">✗ קרדיטים ועוד פקטות בדרך (${ltr(`${b.credits} + ${b.inFlight}`)}) עולים על ${ltr(b.free)} התאים הפנויים: Sync שנשלח כשפקטות היו בדרך ספר אותן כאבודות, וה-buffer עלול לגלוש.</span>`
            : `<span class="wv-ok">✓ קרדיטים ועוד פקטות בדרך (${ltr(`${b.credits} + ${b.inFlight}`)}) אינם עולים על ${ltr(b.free)} התאים הפנויים${gap.length ? `: ההפרש הוא ${gap.join(", ו")}` : ""}.</span>`);
        const rd = st.script && st.script.random;
        $(".an-rand").innerHTML = rd ? randNote(rd, st.seed, `ובהם ${ltr(rd.faults.lost)} פקטות שאבדו ו-${ltr(rd.faults.syncs)} סנכרונים`,
          { overflow: "אין גלישה", credits: "קרדיטים ועוד פקטות בדרך אינם עולים על התאים הפנויים" }, "שני האינווריאנטים נבדקו אחרי כל אירוע.") : "";
      };
      const logText = (it) => {
        switch (it.out) {
          case "grant": return `‏Credit Grant נושא ${ltr(`PCA = ${it.value}`)}; ה-Egress מחליף בו את PCL (לא מחבר), ועכשיו יש ${ltr(it.credits)} קרדיטים.`;
          case "transmitted": return `פקטה ${ltr(it.id)} שודרה: PCC עולה באחד והיא בדרך.`;
          case "noCredit": return `<span class="wv-bad">שידור בלי קרדיט (${ltr(`PCC = ${it.pcc}, PCL = ${it.pcl}`)}): המודל מדווח על הפרה ולא משנה דבר.</span>`;
          case "received": return `פקטה ${ltr(it.id)} התקבלה: PCR עולה באחד והיא תופסת תא.`;
          case "lost": return `<span class="wv-bad">פקטה ${ltr(it.id)} אבדה על הקו: ה-Egress ספר אותה ב-PCC, ה-Ingress לא יודע עליה, ואף מונה שלו לא זז.</span>`;
          case "overflow": return `<span class="wv-bad">ה-buffer מלא: גלישה, הפרה של הסביבה.</span>`;
          case "dequeued": return `פקטה יצאה מה-buffer: התא התפנה ו-PCA עולה ל-${ltr(it.pca)} (מצטבר).`;
          case "emptyBuffer": return `<span class="wv-bad">הוצאה מ-buffer ריק: הפרה.</span>`;
          case "sync": return `<span class="wv-ok">‏Path Credit Sync עם ${ltr(`PCC = ${it.pcc}`)}: ${ltr(`PCC − PCR = ${it.missing}`)} פקטות שודרו ולא התקבלו, הקרדיטים שלהן חוזרים (${ltr(`PCA = ${it.pca}`)}) ו-PCR מיושר ל-PCC.</span>`;
          case "emptyLink": return `אין פקטות בדרך.`;
          default: return "";
        }
      };
      const nextStep = () => { if (st.script && st.pos < st.script.steps.length) apply(st.script.steps[st.pos], true); };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: nextStep,
        done: () => !st.script || st.pos >= st.script.steps.length,
        restart: () => { if (st.script) reset(st.script); },
      });
      $(".ex-next").addEventListener("click", () => { stop(); nextStep(); });
      $(".ex-end").addEventListener("click", () => { stop(); while (st.script && st.pos < st.script.steps.length) nextStep(); });
      $(".ex-prev").addEventListener("click", () => { stop(); const h = st.history.pop(); if (h) { st.state = h.state; st.log = h.log; st.pos = h.pos; render(); } });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { stop(); st.size = CR_SCRIPTS[b.dataset.p].size; $(".ex-size").value = String(st.size); reset(CR_SCRIPTS[b.dataset.p]); }));
      $(".ex-size").addEventListener("change", () => { stop(); st.size = Number($(".ex-size").value); reset(null); });
      $(".ex-wrap").addEventListener("change", () => { stop(); st.base = $(".ex-wrap").checked ? 250 : 0; reset(null); });
      $(".ex-reset").addEventListener("click", () => { stop(); reset(null); });
      box.addEventListener("click", (e) => { const b = e.target.closest(".cr-act"); if (b) { stop(); apply({ type: b.dataset.ev, how: b.dataset.how }); } });
      // the random run: a script of legal events drawn from the seed
      const runRandom = () => {
        stop();
        reset(crRandomScript(st.size, st.base, Number($(".ex-count").value), Number($(".ex-rate").value) / 100, mulberry32(st.seed)));
      };
      $(".ex-run").addEventListener("click", () => seed.draw());
      $(".ex-rate").addEventListener("input", () => { $(".out-rate").textContent = `${$(".ex-rate").value}%`; if (st.script && st.script.random) runRandom(); });
      $(".ex-count").addEventListener("change", () => { if (st.script && st.script.random) runRandom(); });
      reset(CR_SCRIPTS.a);
      const seed = seedControls(box, $(".ex-run"), (rng, n) => { st.seed = n; runRandom(); }, { seed: st.seed, state: {
        get: () => (st.script && st.script.random ? `r${$(".ex-count").value}.${$(".ex-rate").value}.${st.seed}` : null),
        set: (p) => {
          const m = RAND_HASH.exec(p);
          if (!m || Number(m[2]) > 50 || Number(m[2]) % 5 || Number(m[3]) < 1 || Number(m[3]) > SEED_MAX) return false;
          $(".ex-count").value = m[1]; $(".ex-rate").value = m[2]; $(".out-rate").textContent = `${m[2]}%`;
          st.seed = Number(m[3]); $(".ex-seed").value = st.seed; runRandom(); return true;
        },
      } });
    },
  });

  // The endpoint box (0023): a request builder (a write paints bytes on the block map, a
  // read is cut at random RCB boundaries and parked), a cycle button that runs the
  // page's tick-then-completion loop with the reads interleaved, the completions table
  // with the falling Byte Count, and the page's two examples with their exact draws.
  const endpointView = () => ({
    mount(box) {
      const hex = (v, w = 0) => "0x" + v.toString(16).toUpperCase().padStart(w, "0");
      const st = { s: epInit(), values: [], seed: newSeed(), used: 0, rng: null, log: "", err: "", history: [] };
      // the generator: the script's draws first, then mulberry32 from the seed; `used` counts
      // the seeded draws so a snapshot can be restored and replayed
      const makeRng = () => {
        const unit = mulberry32(st.seed);
        for (let i = 0; i < st.used; i++) unit();
        st.rng = epValueRng(st.values, epUnitRng([], () => { st.used += 1; return unit(); }));
      };
      makeRng();
      const snap = () => { st.history.push({ s: JSON.parse(JSON.stringify(st.s)), values: [...st.values], used: st.used, log: st.log }); if (st.history.length > 200) st.history.shift(); };
      box.innerHTML =
        `<div class="ex-controls"><span class="wv-presets">הדוגמאות שבעמוד: ` +
        `<button type="button" class="md-button ex-preset" data-p="a">סעיף א (מיושר)</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="b">סעיף ב (לא מיושר)</button></span>` +
        `<button type="button" class="md-button ex-reset">איפוס</button></div>` +
        `<div class="ex-controls ep-form"><label>הבקשה <select class="ex-kind" aria-label="סוג הבקשה"><option value="write">MemWr (כתיבה)</option><option value="read" selected>MemRd (קריאה)</option></select></label>` +
        `<label>כתובת <input type="text" class="ex-addr" dir="ltr" value="0x10020" spellcheck="false" aria-label="כתובת בהקסה"></label>` +
        `<label>אורך בבתים <input type="number" class="ex-len" dir="ltr" min="1" max="256" value="256" aria-label="האורך בבתים"></label>` +
        `<button type="button" class="md-button md-button--primary ex-send">שלח בקשה</button><span class="ep-err"></span></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button md-button--primary ex-cycle">מחזור</button>` +
        `<button type="button" class="md-button ex-prev">צעד אחורה</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 600, 250) +
        `<button type="button" class="md-button ex-run">הרץ עד שכל ה-Completions יצאו</button><span class="ex-pos"></span></div>` +
        `<p class="ex-title">הזיכרון, בלוק אחרי בלוק (128 בתים): הכתיבות צבועות, הקריאות הפתוחות מסומנות בקו</p><div class="ep-mem"></div>` +
        `<p class="ex-title">קריאות פתוחות</p><div class="ep-pending"></div><div class="ep-gantt"></div>` +
        `<p class="ex-title">ציר המחזורים: ה-Completion שיצא בכל מחזור, ומתי כל קריאה מוכנה</p><div class="wv-wrap ep-strip" tabindex="0" role="group" aria-label="ציר המחזורים, גלילה אופקית"></div>` +
        `<p class="wv-step an-log" aria-live="polite"></p>` +
        `<p class="ex-title">ה-Completions שיצאו</p><div class="ep-table" tabindex="0"></div><p class="ex-summary an-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const colour = (id) => `ep-c${id % 4}`;
      const render = () => {
        const s = st.s;
        $(".ex-pos").textContent = `מחזור ${s.cycle}`;
        $(".ex-prev").disabled = !st.history.length;
        // the block map
        const keys = new Set(Object.keys(s.memory).map(Number));
        s.pending.forEach((p) => { for (let a = Math.floor(p.address / EP_RCB) * EP_RCB; a < p.address + p.length; a += EP_RCB) keys.add(a); });
        const blocks = [...keys].sort((a, b) => a - b);
        if (!blocks.length) $(".ep-mem").innerHTML = `<p class="an-empty">הזיכרון ריק: בית שלא נכתב נקרא כאפס.</p>`;
        else {
          const W = 520, L = 86, SW = (W - L - 8) / EP_RCB, RH = 26;
          let g = `<svg class="ep-live" viewBox="0 0 ${W} ${blocks.length * RH + 6}" role="img" aria-label="מפת הבלוקים: הבתים שנכתבו והקריאות הפתוחות">`;
          blocks.forEach((key, r) => {
            const y = 3 + r * RH;
            g += `<text class="wv-name" x="${L - 6}" y="${y + 16}" text-anchor="end">${hex(key)}</text><rect class="ep-block" x="${L}" y="${y}" width="${f(EP_RCB * SW)}" height="${RH - 6}"/>`;
            // written ranges: by the write that touched each byte (the latest wins)
            const owner = new Array(EP_RCB).fill(0);
            s.writes.forEach((w) => { for (let a = Math.max(w.address, key); a < Math.min(w.address + w.length, key + EP_RCB); a++) owner[a - key] = w.id; });
            let i = 0;
            while (i < EP_RCB) { let j = i; while (j + 1 < EP_RCB && owner[j + 1] === owner[i]) j++; if (owner[i]) g += `<rect class="ep-written ${colour(owner[i])}" x="${f(L + i * SW)}" y="${y}" width="${f((j - i + 1) * SW)}" height="${RH - 6}"><title>כתיבה ${owner[i]}: ${hex(key + i)} עד ${hex(key + j)}</title></rect>`; i = j + 1; }
            s.pending.forEach((p) => {
              const a = Math.max(p.address, key), b = Math.min(p.address + p.length, key + EP_RCB);
              if (a < b) g += `<rect class="ep-read ${colour(p.id)}" x="${f(L + (a - key) * SW)}" y="${y - 2}" width="${f((b - a) * SW)}" height="${RH - 2}"/>`;
            });
          });
          $(".ep-mem").innerHTML = g + `</svg>`;
        }
        $(".ep-pending").innerHTML = s.pending.length ? s.pending.map((p) => {
          const status = p.ready > s.cycle ? `מוכן ממחזור ${ltr(p.ready)}` : `<span class="wv-ok">מוכן</span>`;
          return `<p class="ep-pend ${colour(p.id)}"><span class="ep-swatch"></span>‏Tag ${ltr(hex(p.tag, 2))}, ${ltr(hex(p.address))}, ${ltr(p.length)} בתים: ` +
            `<span class="an-chips" dir="ltr">${p.cpls.map((c, i) => `<span class="an-chip${i === 0 ? " is-head" : ""}">${c.size} B · BC ${c.bc}</span>`).join("")}</span> ` +
            `${p.sent ? `יצאו ${ltr(p.sent)} מתוך ${ltr(p.total)}, ` : ""}${status}.</p>`;
        }).join("") : `<p class="an-empty">אין קריאות פתוחות.</p>`;
        // the timeline of every read: its random wait dashed, the time it is ready and
        // waiting its turn solid, a mark per completion, and a line at the current cycle
        const reads = s.reads;
        if (!reads.length) $(".ep-gantt").innerHTML = "";
        else {
          const W = 520, L = 86, RH = 22, last = Math.max(s.cycle, ...reads.flatMap((r) => r.waits.map((w) => w[1]))) + 1;
          const X = (c) => L + (c / last) * (W - L - 10), H = reads.length * RH + 22;
          const step = last > 60 ? 20 : last > 30 ? 10 : last > 12 ? 5 : 1;
          let g = `<svg class="ep-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="ציר המחזורים: לכל קריאה ההמתנות שלה וה-Completions שיצאו">`;
          for (let c = 0; c <= last; c += step) g += `<line class="grid" x1="${f(X(c))}" x2="${f(X(c))}" y1="2" y2="${H - 18}"/><text class="tick" x="${f(X(c))}" y="${H - 5}" text-anchor="middle">${c}</text>`;
          reads.forEach((r, i) => {
            const y = 2 + i * RH + RH / 2, outs = s.out.filter((c) => c.read === r.id);
            g += `<text class="wv-name" x="${L - 6}" y="${f(y + 4)}" text-anchor="end">Tag ${hex(r.tag, 2)}</text>`;
            r.waits.forEach(([from, ready], k) => {
              const until = outs[k] ? outs[k].cycle : s.cycle;
              g += `<line class="ep-wait ${colour(r.id)}" x1="${f(X(from))}" x2="${f(X(ready))}" y1="${y}" y2="${y}"><title>ממתינה ממחזור ${from} עד ${ready}</title></line>`;
              if (until > ready) g += `<line class="ep-ready ${colour(r.id)}" x1="${f(X(ready))}" x2="${f(X(until))}" y1="${y}" y2="${y}"><title>מוכנה ממחזור ${ready}, מחכה לתורה</title></line>`;
            });
            outs.forEach((c) => { g += `<circle class="ep-cpl ${colour(r.id)}" cx="${f(X(c.cycle))}" cy="${y}" r="5"><title>מחזור ${c.cycle}: ${c.size} בתים מ-${hex(c.address)}, Byte Count ${c.bc}</title></circle>`; });
          });
          g += `<line class="ep-now" x1="${f(X(s.cycle))}" x2="${f(X(s.cycle))}" y1="0" y2="${H - 16}"/>`;
          $(".ep-gantt").innerHTML = g + `</svg><p class="viz-legend ep-legend"><span><i class="ep-lg-wait"></i>ממתינה לזמן האקראי</span><span><i class="ep-lg-ready"></i>מוכנה, מחכה לתורה</span><span><i class="ep-lg-cpl"></i>‏Completion יצא</span><span><i class="ep-lg-now"></i>המחזור הנוכחי</span></p>`;
        }
        // the cycle axis: the last 64 cycles
        const es = epStrip(s), from = Math.max(0, es.n - 64), n = es.n - from;
        const cut = (a) => a.slice(from);
        const stripEl = $(".ep-strip");
        stripEl.innerHTML = waveStrip([
          { name: "Tag", kind: "bus", split: true, values: cut(es.cpl).map((c) => (c ? hex(c.tag, 2) : "—")) },
          { name: "size", kind: "bus", split: true, values: cut(es.cpl).map((c) => (c ? c.size : "—")) },
          { name: "BC", kind: "bus", split: true, values: cut(es.cpl).map((c) => (c ? c.bc : "—")) },
        ].concat(es.reads.map((r) => ({ name: `ready ${hex(r.tag, 2)}`, kind: "bit", values: cut(r.ready), cls: ["wv-s1", "wv-s2", "wv-s3"][r.id % 3] }))),
        n, { slotW: 46, labelW: 92, cursor: n - 1, ticks: (k) => from + k, label: `ציר המחזורים: ${n} מחזורים` });
        stripEl.scrollLeft = stripEl.scrollWidth;
        $(".an-log").innerHTML = (st.err ? `<span class="wv-bad">${st.err}</span> ` : "") + st.log;
        $(".ep-table").innerHTML = s.out.length ? `<table><thead><tr><th>מחזור</th><th>Requester ID</th><th>Tag</th><th>כתובת</th><th>גודל</th><th>Byte Count</th><th>הבית הראשון והאחרון</th></tr></thead><tbody>` +
          s.out.map((c) => `<tr class="${colour(c.read)}"><td>${ltr(c.cycle)}</td><td>${ltr(hex(c.rid, 4))}</td><td>${ltr(hex(c.tag, 2))}</td><td>${ltr(hex(c.address))}</td><td>${ltr(c.size)}</td><td>${ltr(c.bc)}</td><td>${ltr(`${hex(c.first, 2)} … ${hex(c.last, 2)}`)}</td></tr>`).join("") + `</tbody></table>` : `<p class="an-empty">עדיין לא יצא Completion.</p>`;
        // the rules, checked on what went out
        const perRead = new Map();
        s.out.forEach((c) => { if (!perRead.has(c.read)) perRead.set(c.read, []); perRead.get(c.read).push(c); });
        let ok = true, notes = [];
        perRead.forEach((list, id) => {
          const rd = s.reads.find((r) => r.id === id);
          const ascending = list.every((c, i) => i === 0 || c.address === list[i - 1].address + list[i - 1].size);
          const cuts = list.every((c, i) => i === 0 || c.address % EP_RCB === 0);
          const bc = list.every((c, i) => c.bc === rd.length - (c.address - rd.address));
          const mps = list.every((c) => c.size <= 256);
          if (!(ascending && cuts && bc && mps)) ok = false;
          const done = !s.pending.some((p) => p.id === id);
          if (done && list.reduce((a, c) => a + c.size, 0) !== rd.length) ok = false;
          notes.push(`Tag ${ltr(hex(rd.tag, 2))}: ${ltr(list.map((c) => c.size).join(" + "))}${done ? ` = ${ltr(rd.length)}` : " …"}`);
        });
        const perCycle = new Set(s.out.map((c) => c.cycle)).size === s.out.length;
        $(".an-sum").innerHTML = s.out.length
          ? (ok && perCycle ? `<span class="wv-ok">✓ בכל קריאה: סדר כתובות עולה, חיתוך רק על כפולות של 128, Byte Count יורד נכון, לכל היותר 256 בתים, ו-Completion אחד לכל היותר במחזור.</span> ` : `<span class="wv-bad">✗ כלל הופר.</span> `) + notes.join("; ") + "."
          : `שולחים כתיבה וקריאות, ואז מקדמים מחזורים: כל קריאה מחכה זמן אקראי, ובין קריאות מוכנות הבחירה אקראית, ומכאן השילוב.`;
      };
      const parseAddr = () => { const t = $(".ex-addr").value.trim(); const v = /^0x[0-9a-f]+$/i.test(t) ? parseInt(t, 16) : /^\d+$/.test(t) ? Number(t) : NaN; return v; };
      $(".ex-send").addEventListener("click", () => {
        stop();
        st.err = "";
        const address = parseAddr(), length = Number($(".ex-len").value);
        if (!Number.isFinite(address) || address < 0) st.err = "כתובת לא תקינה (הקסה, למשל 0x10020).";
        else if (!(length >= 1 && length <= EP_MRRS)) st.err = `האורך חייב להיות בין 1 ל-${EP_MRRS} (MRRS).`;
        else if (Math.floor(address / 4096) !== Math.floor((address + length - 1) / 4096)) st.err = "בקשה לא חוצה גבול של 4 KB.";
        if (st.err) { render(); return; }
        snap();
        if ($(".ex-kind").value === "write") {
          const w = st.s.writes.length + 1;
          epWrite(st.s, address, Array.from({ length }, (_, i) => (i + 0x10 * w) & 0xFF));
          st.log = `כתיבה ${ltr(w)}: ${ltr(length)} בתים מ-${ltr(hex(address))} (הבית ה-${ltr("i")} שווה ל-${ltr(`i + ${hex(0x10 * w)}`)}), posted: הבלוקים שנגעו בהם מתעדכנים, בלי Completion.`;
        } else {
          const tag = st.s.nextTag++, rid = 0x0200;
          const p = epRead(st.s, { address, length, rid, tag }, st.rng);
          st.log = `קריאה Tag ${ltr(hex(tag, 2))}: ${ltr(length)} בתים מ-${ltr(hex(address))}. ה-Completions נבנו עכשיו, בסדר כתובות: ${ltr(p.cpls.map((c) => c.size).join(" + "))} (חיתוך אקראי על גבולות 128), ויחכו עד מחזור ${ltr(p.ready)}.`;
        }
        render();
      });
      const cycle = () => {
        const c = epCycle(st.s, st.rng);
        st.err = "";
        st.log = c ? `מחזור ${ltr(st.s.cycle)}: יוצא Completion של Tag ${ltr(hex(c.tag, 2))} מ-${ltr(hex(c.address))}, ${ltr(c.size)} בתים, Byte Count ${ltr(c.bc)}` + (st.s.pending.some((p) => p.tag === c.tag) ? ` (הבא של אותה קריאה אחרי המתנה אקראית).` : ` (האחרון של הקריאה).`)
          : `מחזור ${ltr(st.s.cycle)}: אין קריאה מוכנה, לא יוצא דבר.`;
      };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: () => { snap(); cycle(); render(); },
        done: () => !st.s.pending.length,
        restart: () => {},
      });
      $(".ex-cycle").addEventListener("click", () => { stop(); snap(); cycle(); render(); });
      $(".ex-prev").addEventListener("click", () => {
        stop();
        const h = st.history.pop();
        if (!h) return;
        st.s = h.s; st.values = h.values; st.used = h.used; st.log = h.log; st.err = "";
        makeRng(); render();
      });
      $(".ex-run").addEventListener("click", () => { stop(); if (st.s.pending.length) snap(); let guard = 0; while (st.s.pending.length && guard++ < 400) cycle(); if (!guard) st.log = "אין קריאות פתוחות."; render(); });
      const load = (script) => {
        stop();
        st.s = epInit(); st.values = script ? [...script.draws] : []; st.used = 0; st.history = []; st.err = "";
        makeRng();
        if (script) {
          epWrite(st.s, 0x10000, Array.from({ length: 512 }, (_, i) => i & 0xFF));
          script.reads.forEach(([address, length, rid, tag]) => epRead(st.s, { address, length, rid, tag }, st.rng));
          st.s.nextTag = 0x30;
          st.log = `הדוגמה שבעמוד: כתיבה של 512 בתים מ-${ltr("0x10000")} (הבית ה-${ltr("i")} שווה ל-${ltr("i mod 256")}) ושתי קריאות עם הפיצול וההמתנות שבעמוד. "מחזור" או "הרץ" מוציאים את ה-Completions.`;
        } else st.log = "";
        render();
      };
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => load(EP_SCRIPTS[b.dataset.p])));
      $(".ex-reset").addEventListener("click", () => seed.draw());
      load(EP_SCRIPTS.b);
      const seed = seedControls(box, $(".ex-reset"), (rng, n) => { st.seed = n; load(null); }, { seed: st.seed });
    },
  });

  // The tracer box (0002, 0003): the Python code of the page on the left with the current
  // line lit, the state on the right. data-mode="swap": a version select, a and b, the
  // same-variable and 8-bit toggles, the symbolic expressions in a0 and b0.
  // data-mode="loop": a typed or random array, one comparison per step, a jump to the end
  // of the outer iteration with the invariant, the counters.
  const traceView = (box) => ({
    mount() {
      const mode = box.dataset.mode === "loop" ? "loop" : "swap";
      const playRow = (next, prev, extra = "") =>
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button md-button--primary ex-next">${next}</button>` +
        `<button type="button" class="md-button ex-prev">${prev}</button>${extra}` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1400">איטי</option><option value="800" selected>בינוני</option><option value="250">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button><button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>`;
      const codeHtml = (code, cur, swapLine) => `<pre class="tr-code" dir="ltr" tabindex="0" aria-label="הקוד">` +
        code.map((l, k) => `<span class="tr-line${k === cur ? " is-cur" : ""}${k === swapLine ? " is-swap" : ""}"><span class="tr-ln">${k + 1}</span>${l.replace(/</g, "&lt;")}</span>`).join("\n") + `</pre>`;
      const $ = (sel) => box.querySelector(sel);
      let timer = null;
      const stop = () => { if (timer) clearInterval(timer); timer = null; $(".ex-play").textContent = "הפעלה"; };
      if (mode === "swap") {
        const PAGE = { kind: "arith", a: 5, b: 3, c: 7, same: false, bits: 0, k: 0 };
        const st = { ...PAGE };
        box.innerHTML =
          `<div class="ex-controls"><label>הגרסה <select class="ex-kind" aria-label="גרסת ההחלפה"><option value="temp">עם משתנה עזר (סעיף א)</option><option value="arith" selected>אריתמטיקה (סעיף ב)</option><option value="xor">XOR (סעיף ג)</option><option value="rot">סיבוב של שלושה ב-XOR (שאלת המשך)</option></select></label>` +
          `<label><span>a</span> <input type="number" class="ex-a" dir="ltr" value="5" aria-label="הערך של a"></label>` +
          `<label><span>b</span> <input type="number" class="ex-b" dir="ltr" value="3" aria-label="הערך של b"></label>` +
          `<label class="tr-c" hidden><span>c</span> <input type="number" class="ex-c" dir="ltr" value="7" aria-label="הערך של c"></label>` +
          `<label><input type="checkbox" class="ex-same"> <span>‏a ו-b הם אותו משתנה (${code("swap(v, i, i)")})</span></label>` +
          `<label><input type="checkbox" class="ex-bits"> <span>‏int של 8 ביט (מודולו 256)</span></label>` +
          `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
          playRow("השורה הבאה", "השורה הקודמת") +
          `<div class="tr-box"><div class="tr-left"></div><div class="tr-right"></div></div>` +
          `<p class="wv-step tr-step" aria-live="polite"></p><p class="ex-summary tr-sum"></p>`;
        const bits8 = (v) => (st.bits ? ltr(v.toString(2).padStart(8, "0")) : "");
        const rot = () => st.kind === "rot";
        const traceOf = () => (rot() ? rotTrace(st.a, st.b, st.c, st.bits) : swapTrace(st.kind, st.a, st.b, st.same, st.bits));
        const draw = () => {
          const tr = traceOf(), total = tr.frames.length - 1;
          st.k = Math.min(st.k, total);
          const fr = tr.frames[st.k], prev = st.k ? tr.frames[st.k - 1] : null;
          $(".tr-left").innerHTML = codeHtml(tr.code, fr.line, -1);
          const row = (name, v, sym, changed) => `<tr class="${changed ? "is-changed" : ""}"><td>${ltr(name)}</td><td>${v === null ? "–" : ltr(v)}</td>${st.bits ? `<td>${v === null ? "" : bits8(v)}</td>` : ""}<td>${sym === null ? "–" : ltr(sym)}</td></tr>`;
          $(".tr-right").innerHTML = `<table class="tr-vars"><thead><tr><th>משתנה</th><th>ערך</th>${st.bits ? "<th>ביטים</th>" : ""}<th>סימבולית</th></tr></thead><tbody>` +
            row(rot() ? "a" : st.same ? "v[i] = v[j]" : "v[i] (a)", fr.a, fr.aSym, prev && prev.a !== fr.a) +
            (st.same ? "" : row(rot() ? "b" : "v[j] (b)", fr.b, fr.bSym, prev && prev.b !== fr.b)) +
            (rot() ? row("c", fr.c, fr.cSym, prev && prev.c !== fr.c) : "") +
            (st.kind === "temp" ? row("temp", fr.temp, fr.tempSym, prev && prev.temp !== fr.temp) : "") + `</tbody></table>`;
          $(".ex-pos").textContent = `שורה ${st.k} מתוך ${total}`;
          $(".tr-step").innerHTML = st.k === 0
            ? `לפני הריצה: ${ltr(`a = a0 = ${st.a}`)}${st.same ? ` ו-b הוא אותו תא` : `, ${ltr(`b = b0 = ${st.b}`)}`}${rot() ? `, ${ltr(`c = c0 = ${st.c}`)}` : ""}.`
            : `שורה ${ltr(st.k)}: ${ltr(code(tr.code[fr.line]))} ⇒ ${ltr(fr.text)}. סימבולית: ${ltr(`a = ${fr.aSym}`)}${st.same ? "" : `, ${ltr(`b = ${fr.bSym}`)}`}${rot() ? `, ${ltr(`c = ${fr.cSym}`)}` : ""}${fr.tempSym !== null && st.kind === "temp" ? `, ${ltr(`temp = ${fr.tempSym}`)}` : ""}.`;
          let sum = "";
          if (st.k === total) {
            if (rot()) sum = tr.ok
              ? `<span class="wv-ok">✓ סובבו: ${ltr(`a = b0 = ${fr.a}`)}, ${ltr(`b = c0 = ${fr.b}`)}, ${ltr(`c = a0 = ${fr.c}`)}.</span> שש פעולות XOR, כי סיבוב של שלושה הוא שתי החלפות: ${ltr("a ↔ b")} (שורות 1 עד 3) ואז ${ltr("b ↔ c")} (שורות 4 עד 6). אחרי ההחלפה הראשונה ${ltr("b = a0")}, וההחלפה השנייה מעבירה את ${ltr("a0")} ל-${ltr("c")}.`
              : `<span class="wv-bad">✗ הערכים לא סובבו.</span>`;
            else if (tr.ok) sum = `<span class="wv-ok">✓ הוחלפו: ${ltr(`a = b0 = ${fr.a}`)}, ${ltr(`b = a0 = ${fr.b}`)}.</span>`;
            else if (st.same) sum = st.kind === "temp" ? `<span class="wv-ok">✓ אותו משתנה: עם משתנה עזר הערך נשמר (${ltr(fr.a)}).</span>` : `<span class="wv-bad">✗ אותו משתנה: ${st.kind === "arith" ? "השורה הראשונה מכפילה והשנייה מאפסת" : "השורה הראשונה מחשבת a ^ a = 0"}, והערך ${ltr(st.a)} אבד. זו המלכודת של ${code("swap(v, i, i)")}.</span>`;
            else sum = `<span class="wv-bad">✗ הערכים לא הוחלפו.</span>`;
            if (st.bits && st.kind === "arith" && !st.same && st.a + st.b >= 256) sum += ` הסכום ${ltr(`${st.a} + ${st.b} = ${st.a + st.b}`)} גלש מעבר ל-255, ובכל זאת ההחלפה נכונה: החיסור מתבצע באותו מודולו, ו-${ltr("(a0 + b0) − b0 ≡ a0 (mod 256)")}.`;
          }
          $(".tr-sum").innerHTML = sum;
        };
        const total = () => traceOf().frames.length - 1;
        const readInputs = () => {
          const lim = st.bits ? 255 : 1e9;
          const clamp = (sel) => Math.max(st.bits ? 0 : -lim, Math.min(lim, Math.round(Number($(sel).value) || 0)));
          st.a = clamp(".ex-a"); st.b = clamp(".ex-b"); st.c = clamp(".ex-c");
          $(".ex-a").value = st.a; $(".ex-b").value = st.b; $(".ex-c").value = st.c;
        };
        // the rotation has three cells and no aliasing: the c field appears, "same" is off
        const setKind = (kind) => {
          st.kind = kind; $(".ex-kind").value = kind;
          $(".tr-c").hidden = !rot();
          if (rot()) { st.same = false; $(".ex-same").checked = false; $(".ex-b").disabled = false; }
          $(".ex-same").disabled = rot();
        };
        $(".ex-kind").addEventListener("change", () => { stop(); setKind($(".ex-kind").value); st.k = 0; draw(); });
        [".ex-a", ".ex-b", ".ex-c"].forEach((sel) => $(sel).addEventListener("change", () => { stop(); readInputs(); st.k = 0; draw(); }));
        $(".ex-same").addEventListener("change", () => { stop(); st.same = $(".ex-same").checked; $(".ex-b").disabled = st.same; st.k = 0; draw(); });
        $(".ex-bits").addEventListener("change", () => { stop(); st.bits = $(".ex-bits").checked ? 8 : 0; readInputs(); st.k = 0; draw(); });
        $(".ex-reset").addEventListener("click", () => {
          stop(); Object.assign(st, PAGE);
          setKind(PAGE.kind); $(".ex-a").value = PAGE.a; $(".ex-b").value = PAGE.b; $(".ex-c").value = PAGE.c; $(".ex-b").disabled = false; $(".ex-same").checked = false; $(".ex-bits").checked = false;
          draw();
        });
        $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
        $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
        $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
        $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
        $(".ex-play").addEventListener("click", () => {
          if (timer) { stop(); return; }
          if (st.k >= total()) st.k = 0;
          $(".ex-play").textContent = "עצירה";
          timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number($(".ex-speed").value));
        });
        $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); $(".ex-play").click(); } });
        draw();
        return;
      }
      const PAGE = [3, 1, 4, 2];
      const st = { A: PAGE.slice(), k: 0 };
      box.innerHTML =
        `<div class="ex-controls"><label><span>המערך</span><input type="text" class="ex-nums" dir="ltr" value="3, 1, 4, 2" spellcheck="false" aria-label="המערך, מספרים מופרדים בפסיקים"></label>` +
        `<button type="button" class="md-button ex-page">דוגמת העמוד</button><button type="button" class="md-button ex-random">אקראי</button><span class="fl-err"></span></div>` +
        playRow("ההשוואה הבאה", "הקודמת", `<button type="button" class="md-button ex-endi">עד סוף i</button>`) +
        `<div class="tr-box"><div class="tr-left"></div><div class="tr-right"></div></div>` +
        `<p class="wv-step tr-step" aria-live="polite"></p><p class="ex-summary tr-sum"></p>`;
      const draw = () => {
        const tr = loopTrace(st.A), total = tr.frames.length;
        st.k = Math.min(st.k, total);
        const fr = st.k ? tr.frames[st.k - 1] : null, n = st.A.length;
        $(".tr-left").innerHTML = codeHtml(tr.code, fr ? 3 : 0, fr && fr.swapped ? 4 : -1);
        const arr = fr ? fr.after : st.A, sortedTo = fr ? (fr.endOfI ? fr.i : fr.i - 1) : -1;
        $(".tr-right").innerHTML = `<div class="tr-arr" dir="ltr">` + arr.map((v, x) => {
          const cls = [x <= sortedTo ? "is-done" : "", fr && x === fr.i ? "is-i" : "", fr && x === fr.j ? "is-j" : "", fr && fr.swapped && (x === fr.i || x === fr.j) ? "is-swapped" : ""].join(" ").trim();
          return `<span class="${cls}"><span class="tr-idx">${x}</span>${v}</span>`;
        }).join("") + `</div><p class="tr-counts">${fr ? `${ltr("i")} = ${ltr(fr.i)}, ${ltr("j")} = ${ltr(fr.j)}. ` : ""}השוואות: ${ltr(fr ? fr.comparisons : 0)} מתוך ${ltr(n * n)}, החלפות: ${ltr(fr ? fr.swaps : 0)}.</p>` +
          `<p class="tr-legend"><span class="tr-lg-i">מסגרת כחולה: ${code("i")}</span> <span class="tr-lg-j">מסגרת כתומה מקווקוות: ${code("j")}</span> <span class="tr-lg-done">ירוק: ${code("A[0..i]")} ממוין</span></p>`;
        $(".ex-pos").textContent = `השוואה ${st.k} מתוך ${total}`;
        let step;
        if (!fr) step = n ? `לפני הריצה: ${ltr(`A = [${st.A.join(", ")}]`)}, ${ltr(`n = ${n}`)}. הלולאה הפנימית מתחילה מ-${ltr("j = 0")}, לא מ-${ltr("j = i + 1")}.` : `מערך ריק: אין השוואות.`;
        else {
          const ai = fr.before[fr.i], aj = fr.before[fr.j];
          step = `${ltr(`i = ${fr.i}, j = ${fr.j}`)}: ${ltr(`A[i] < A[j]`)} הוא ${ltr(`${ai} < ${aj}`)}, ` + (fr.swapped ? `<span class="wv-ok">כן ⇒ החלפה</span>: ${ltr(`A = [${fr.after.join(", ")}]`)}.` : `לא ⇒ בלי שינוי.`);
          if (fr.endOfI) step += ` <span class="wv-ok">סוף האיטרציה ${ltr(`i = ${fr.i}`)}: ${ltr(`A[0..${fr.i}]`)} ממוין בסדר עולה, והמקסימום של כל המערך (${ltr(Math.max(...fr.after))}) יושב במקום ${ltr(fr.i)}.</span>`;
          else if (fr.j < fr.i) step += ` ‏${ltr("j < i")}: החלפה כאן מזיזה את ${ltr("A[i]")} אחורה לתוך החלק הממוין.`;
        }
        $(".tr-step").innerHTML = step;
        $(".tr-sum").innerHTML = st.k >= total && n ? `<span class="wv-ok">✓ ${ltr(`n² = ${n * n}`)} השוואות, ${ltr(tr.swaps)} החלפות, בלי יציאה מוקדמת. המערך ממוין בסדר עולה: ${ltr(`[${tr.result.join(", ")}]`)}.</span>` : "";
      };
      const total = () => loopTrace(st.A).frames.length;
      const parse = () => {
        const parts = $(".ex-nums").value.split(/[,\s]+/).filter((t) => t.length);
        const nums = parts.map(Number);
        if (!nums.length || nums.some((v) => !Number.isInteger(v)) || nums.length > 8) { $(".fl-err").textContent = "3 עד 8 מספרים שלמים, מופרדים בפסיקים"; return; }
        if (nums.length < 3) { $(".fl-err").textContent = "לפחות 3 מספרים"; return; }
        $(".fl-err").textContent = ""; stop(); st.A = nums; st.k = 0; draw();
      };
      $(".ex-nums").addEventListener("change", parse);
      $(".ex-page").addEventListener("click", () => { $(".ex-nums").value = PAGE.join(", "); parse(); });
      const seed = seedControls(box, $(".ex-random"), (rng) => { const n = 3 + Math.floor(rng() * 6); $(".ex-nums").value = Array.from({ length: n }, () => Math.floor(rng() * 20)).join(", "); parse(); });
      $(".ex-random").addEventListener("click", seed.draw);
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-endi").addEventListener("click", () => { stop(); const n = st.A.length; if (st.k < total()) st.k = Math.min(total(), (Math.floor((st.k) / n) + 1) * n); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      $(".ex-play").addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= total()) st.k = 0;
        $(".ex-play").textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number($(".ex-speed").value));
      });
      $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); $(".ex-play").click(); } });
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
    abmap: abmapView,
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
    stock: stockView,
    handshake: handshakeView,
    acknak: acknakView,
    credits: creditsView,
    endpoint: endpointView,
    trace: traceView,
  };

  // --- the box -----------------------------------------------------------------------------

  // One line of help per kind: what the box shows and what its buttons do, behind the "?"
  // button of the box header; "איפוס הכול" beside it rebuilds the box from its data
  // attributes, so every control returns to its default.
  const HELP = {
    "cake-arith": "העוגה מחולקת לפי החוק החשבוני: a הוא החלק הראשון ו-d התוספת לכל אדם. הסליידרים ושדות המספר קובעים אותם, ״הבא״ ו״הפעלה״ עוברים אדם אחרי אדם, והטבלה והגרפים מראים מי מקבל הכי הרבה.",
    "cake-geo": "העוגה מחולקת לפי החוק ההנדסי: a הוא החלק הראשון ו-q היחס בין אדם לאדם. הסליידרים ושדות המספר קובעים אותם, ״הבא״ ו״הפעלה״ עוברים אדם אחרי אדם, והטבלה והגרפים מראים מי מקבל הכי הרבה.",
    motorcycle: "הציור מראה את הנוסעים על הדרך והגרף את מיקומם בזמן. הסליידרים קובעים את מהירויות ההליכה והרכיבה, בורר האסטרטגיה ומספר הרוכבים את התכנית, ״הפעלה״ מריץ אותה, ו״להשוואה עם״ מצייר תכנית שנייה מקווקוות.",
    josephus: "המעגל מראה את המשחק: N (ו-L) בסליידרים, ״הצעד הבא״ או ״הפעלה״ מוציאים אדם אחרי אדם, השורד מודגש מהתחלה, והגרף מראה את השורד לכל N. שדה המושב מחפש באילו מעגלים מושב שורד.",
    clock: "השעון מראה את מפגשי המחוגים: גוררים מחוג, מקלידים שעה או מפעילים, והקפיצות עוברות למפגש הבא או הקודם. המונים וציר הזמן סופרים את המפגשים מההתחלה.",
    strip: "גוררים את העכביש ואת הזבוב על הקירות: הרצועה המחזורית מראה את התמונות, את 48 הקווים ואת הקצר שבהם, והמסלול נפרש פנים אחרי פנים.",
    hourglass: "A, B (ו-C) הם שעוני החול ו-D הזמן למדידה. התכנית מצוירת על ציר הזמן, ״הצעד הבא״ ו״הפעלה״ עוברים אירוע אחרי אירוע, ובורר היעד בוחר בין היעד של העמוד למספר ההפיכות הקטן ביותר.",
    probability: "p ו-q הן ההסתברויות ו-C המספר: התיבה מחשבת את התשובה, מציירת את ריבוע שני הילדים ואת העקומה כנגד q.",
    bridge: "זמני החצייה בשדה, קיבולת הגשר ובורר התכנית: ״הבא״ ו״הפעלה״ מעבירים חצייה אחרי חצייה, והטבלה משווה את שלוש התכניות.",
    river: "מעבירים את הזאב, העז והכרוב בלחיצה, או נותנים לתכנית ה-BFS לרוץ; גרף המצבים מתעדכן עם כל מעבר.",
    pcie: "כתובת, אורך, MPS ו-RCB: התיבה חותכת את הבקשה לבלוקים, סופרת את הפיצולים בתכנות דינמי ובנוסחה סגורה, ומציירת את מפת הפיצולים כשהם מעטים. ה-presets טוענים את דוגמאות העמוד.",
    fifo: "ה-burst וקצבי הכתיבה והקריאה בסליידרים: הרצועה מראה את שני השעונים, הכתיבות, הקריאות (משבצת מדולגת מוצללת) ואת המילוי בזמן אמיתי, הסליידר שלה מזיז חלון של 40 מחזורי כתיבה, והגרף מראה את המילוי לאורך כל ה-burst ליד הנוסחה.",
    mtbf: "תדר השעון והנתונים, tau, T0 ו-overhead: התיבה מחשבת את ה-MTBF של פלופ אחד עד שלושה ביחידות קריאות, ומציירת אותו כנגד תדר השעון.",
    triangle: "שלוש נקודות על המעגל: גוררים, מקלידים זוויות או מזיזים בחיצים, וירוק אומר שהמרכז בפנים. ״הפעלה״ עובר על כל השלשות וסופר, ו״1,000 הגרלות״ מצייר היסטוגרמה של הקשת הגדולה.",
    polygon: "n קודקודים על המעגל: גוררים, מקלידים או מגרילים, וירוק אומר שהמרכז בפנים. ״1,000 הגרלות״ משווה לנוסחה הרציפה ולשבר הבדיד.",
    boxes: "N קופסאות במעגל עם המעגלים שלהן בצבעים: ״ערבוב״ מגריל סידור, בוחרים אדם ועוקבים אחרי הפתיחות שלו, ו״1,000 סיבובים״ משווה את האסטרטגיה לבחירה אקראית. ״העתקת קישור״ שומר את המצב.",
    floyd: "המערך כגרף של זנב ומעגל: ״הגרלה״ או הקלדה קובעים אותו, ו״הצעד הבא״ ו״הפעלה״ מזיזים את הצב ואת הארנב דרך שני השלבים עד הערך הכפול.",
    bfs01: "השאריות מודולו x על טבעת: ״הצעד הבא״ מוציא שארית מהתור ומצייר את עץ ה-BFS, ובסוף התשובה נקראת בחזרה. שדה הספרות ומצב ״רק האורך״ הם שאלות ההמשך.",
    abmap: "בוחרים x ורואים את כל 45 זוגות הספרות a < b: בתא ירוק אורך הכפולה הקטנה ביותר, ו-✗ כשאין. לחיצה על תא מציגה את התשובה, את הפירוק x = 2^s · 5^t · m ואת הכלל של המשפט, ושתי הפונקציות של העמוד מושוות בכל תא.",
    brackets: "מקלידים מחרוזת סוגריים: ״הצעד הבא״ ו״הפעלה״ קוראים תו אחרי תו, המחסנית וגרף העומק מתעדכנים, והכישלון הראשון מסומן עם הסיבה.",
    ttt: "לוחצים על משבצות הלוח: התיבה אומרת אם זה לוח סיום חוקי ולמה לא. ״הגרלה״ נותנת לוח חוקי, והבורר מפעיל את האלכסונים המתגלגלים של סעיף ב.",
    shapes: "״עוד צורה״ מגריל מועמד ומראה את הנדחים בגלל חפיפה, ״הגרלה שלמה״ מציירת את כולן, ו״500 הגרלות״ בונה מפת חום. N, M ומספר הצורות בסליידרים.",
    kaprekar: "מקלידים או מגרילים מספר: ״הצעד הבא״ ממיין ומחסר עד 495 או 6174, וההיסטוגרמה סופרת את אורכי השרשראות של כל המספרים.",
    eurovision: "״ההכרזה הבאה״ מוסיפה מדינה: הכוסות מתחת לסכום של ישראל כנגד הנקודות שנותרו. תיבת ה״מה אם״ משנה את הניקוד של ישראל.",
    boxes3: "שלוש קופסאות עם תוויות שגויות: לוחצים על קופסה כדי להוציא כדור, וההיסק נכתב שורה אחרי שורה. ״סידור אחר״ מגריל תכולה.",
    edge: "לוחצים על משבצות של sig ברצועת התזמון: sig_q ו-pulse עוקבים לפי בורר השפה. המתג מראה את מלכודת האיפוס, והכפתור טוען את הדיאגרמה של העמוד. ״העתקת WaveDrom״ מעתיקה את הרצועה כ-JSON.",
    lfsr: "מסמנים taps ובוחרים רוחב: ״צעד״ ו״הפעלה״ מריצים את המצב מ-0…01 על טבעת המצבים (עד 6 ביטים), רצועת התזמון מראה את המצב, הביט שיוצא וביט ההיזון בכל צעד, והטבלה נותנת את אורך המחזור של כל פולינום.",
    div3: "״השפה הבאה״ ו״הפעלה״ מריצים את מודל חצאי המחזור: cnt, a, b ו-clk_out על רצועה, וה-duty נמדד. ״התעוררות״ מתחילה ממצב לא נגיש לפי בורר המונה, והסליידר מחלק ב-N. ״העתקת WaveDrom״ מעתיקה את הרצועה כ-JSON.",
    gray: "בסנכרן בוחרים מצביע ורוחב, וכל ביט שמשתנה נדגם ישן או חדש (בלחיצה או ב״הגרלה״). ב-FIFO ״כתיבה״ ו״קריאה״ מזיזים את המצביעים, empty ו-full מחושבים לפי הכללים, ורצועת התזמון מוסיפה עמודה לכל פעולה.",
    stock: "גוררים מחירים או מגרילים: ״היום הבא״ ו״הפעלה״ מריצים את הסריקה יום אחרי יום עם המינימום והמקסימום עד כה והעסקה הטובה ביותר. הבורר עובר ללונג בלבד.",
    handshake: "לוחצים על משבצות של req ו-ack ברצועה: ארבעת הכללים נבדקים בכל מחזור, וכישלון מסומן בשורת ה-assertion שלו. ה-presets טוענים את ארבע הדוגמאות של העמוד. ״העתקת WaveDrom״ מעתיקה את הרצועה כ-JSON.",
    acknak: "ה-RC וה-EP עם שני תורי הקישור: ״הצעד הבא״ ו״הפעלה״ מריצים את תסריטי העמוד, האירועים החופשיים שולחים, מוסרים (גם עם CRC שגוי או אובדן) ומפעילים טיימרים, ו״הרצה אקראית״ מגרילה תנועה עם תקלות ובודקת את האינווריאנטים. ציר האירועים מוסיף עמודה לכל אירוע.",
    credits: "ארבעת המונים כמחוגים על מעגל: תסריטי העמוד ב״הצעד הבא״, אירועים חופשיים (Grant, שידור, קבלה או אובדן, הוצאה, Sync) ו״הרצה אקראית״ עם שיעור אובדן. שורת הסיכום מאזנת קרדיטים מול תאים פנויים, וציר האירועים מוסיף עמודה לכל אירוע.",
    endpoint: "בונים בקשות כתיבה וקריאה: ״מחזור״ ו״הרץ״ מוציאים Completions לפי המודל, ומפת הבלוקים, ציר ההמתנות, ציר המחזורים וטבלת ה-Completions מתעדכנים. ה-presets טוענים את דוגמאות העמוד.",
    trace: "הקוד של העמוד שורה אחרי שורה: ״הבא״ ו״הפעלה״ מריצים אותו עם הערכים והביטויים, הבורר מחליף בין הגרסאות, והשדות קובעים את הקלט.",
  };
  const header = (box, helpOpen) => {
    const bar = document.createElement("div");
    bar.className = "ex-bar";
    bar.innerHTML = `<button type="button" class="ex-help-btn" aria-expanded="false" aria-label="עזרה: מה התיבה מראה ומה הכפתורים עושים" title="עזרה">?</button>` +
      `<button type="button" class="ex-reset-all" title="כל הבקרות של התיבה חוזרות לברירת המחדל">איפוס הכול</button>` +
      `<p class="ex-help" hidden>${HELP[box.dataset.kind] || ""}</p>`;
    box.prepend(bar);
    const btn = bar.querySelector(".ex-help-btn"), help = bar.querySelector(".ex-help");
    const show = (open) => { help.hidden = !open; btn.setAttribute("aria-expanded", String(open)); };
    btn.addEventListener("click", () => show(help.hidden));
    if (helpOpen) show(true);
    bar.querySelector(".ex-reset-all").addEventListener("click", () => {
      const play = box.querySelector(".ex-play");
      if (play && play.textContent === "עצירה") play.click();        // stop a running loop first
      if (/^#(seed|state)-/.test(location.hash)) history.replaceState(null, "", `${location.pathname}${location.search}`);
      setup(box, !help.hidden);
    });
  };

  // Enlarge buttons (reading-tools.js) on every figure of a box, kept through redraws: a
  // view rebuilds its figures with innerHTML, so the buttons are added again after each
  // change (decorate skips figures that already have one).
  const LIVE_FIGURES = "svg.figure, svg.perf-chart, svg.lf-live, svg.cr-live, svg.ep-live, svg.wave-strip";
  // The WaveDrom row after every timing strip (any svg with data-wavedrom): copy the
  // source to the clipboard, or open it in the WaveDrom editor. The row sits after the
  // strip's scroll container, which the views redraw inside, and reads the current strip
  // when clicked.
  const WD_EDITOR = "https://wavedrom.com/editor.html?";
  const exportRows = (box) => {
    box.querySelectorAll("svg[data-wavedrom]").forEach((svg) => {
      if (svg.closest(".fig-lightbox")) return;
      const host = svg.closest(".wv-wrap") || svg.closest(".fig-wrap") || svg;
      if (host.nextElementSibling && host.nextElementSibling.classList.contains("wv-export")) return;
      const row = document.createElement("p");
      row.className = "wv-export";
      row.innerHTML = `<button type="button" class="md-button wv-copy" title="מעתיק את הרצועה כ-JSON של WaveDrom, כמו הבלוקים שבדפים">העתקת WaveDrom</button> ` +
        `<a class="wv-open" target="_blank" rel="noopener" href="${WD_EDITOR}">פתיחה בעורך WaveDrom</a>`;
      host.after(row);
      const source = () => { const s = host.querySelector("svg[data-wavedrom]") || (host.matches("svg[data-wavedrom]") ? host : null); return s ? s.getAttribute("data-wavedrom") : ""; };
      const link = row.querySelector(".wv-open");
      const refresh = () => { link.href = WD_EDITOR + encodeURIComponent(source()); };
      ["pointerdown", "focus", "click"].forEach((ev) => link.addEventListener(ev, refresh));
      const btn = row.querySelector(".wv-copy");
      btn.addEventListener("click", () => {
        const text = source();
        const done = () => { btn.textContent = "הועתק ✓"; setTimeout(() => { btn.textContent = "העתקת WaveDrom"; }, 1500); };
        const fallback = () => { window.prompt("‏JSON של WaveDrom:", text); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback); else fallback();
      });
    });
  };
  const decorateLive = (box) => {
    exportRows(box);
    if (!window.dvqDecorate) { if (!box.dvqObserved) { box.dvqObserved = true; new MutationObserver(() => exportRows(box)).observe(box, { childList: true, subtree: true }); } return; }
    const dec = () => { window.dvqDecorate(box, LIVE_FIGURES); exportRows(box); };
    dec();
    if (box.dvqObserved) return;                         // a rebuilt box keeps its observer
    box.dvqObserved = true;
    new MutationObserver(dec).observe(box, { childList: true, subtree: true });
  };

  // Keyboard stepping: with the box focused (it is in the tab order), → is the next step,
  // ← the previous, space plays or stops, Home and End jump to the ends. Keys typed in a
  // field, and space on a button, are left to the field or the button.
  const KEYS = [
    ["ArrowRight", "button.ex-next, button.ex-cycle"],
    ["ArrowLeft", "button.ex-prev"],
    [" ", "button.ex-play, button.ex-solve"],
    ["Home", "button.ex-start, button.ex-first"],
    ["End", "button.ex-end, button.ex-last"],
  ];
  const KEY_HINTS = [
    ["button.ex-next, button.ex-cycle, button.ex-prev", "חיצים ← → לצעד"],
    ["button.ex-play, button.ex-solve", "רווח להפעלה ולעצירה"],
    ["button.ex-start, button.ex-first, button.ex-end, button.ex-last", "‏Home ו-End להתחלה ולסוף"],
    ["[role=slider].tri-pt, [role=slider].st-pt", "‏Tab לנקודה וחיצים מזיזים אותה (עם Shift בקפיצות)"],
  ];
  const keyboard = (box) => {
    const hints = KEY_HINTS.filter(([sel]) => box.querySelector(sel)).map(([, text]) => text);
    if (!hints.length) return;
    box.tabIndex = 0;
    const hint = document.createElement("p");
    hint.className = "ex-keys";
    hint.textContent = `מקשים כשהתיבה ממוקדת: ${hints.join(", ")}.`;
    box.append(hint);
    if (box.dvqKeys) return;                             // a rebuilt box keeps its listener
    box.dvqKeys = true;
    box.addEventListener("keydown", (e) => {
      const t = e.target;
      if (t.matches("input, select, textarea") || t.getAttribute("role") === "slider" || (e.key === " " && t !== box && (t.matches("button") || t.getAttribute("role") === "button"))) return;
      const hit = KEYS.find(([key]) => key === e.key);
      if (!hit) return;
      const btn = box.querySelector(hit[1]);
      if (!btn || btn.disabled) return;
      e.preventDefault();
      btn.click();
    });
  };

  const setup = (box, helpOpen = false) => {
    const make = VIEWS[box.dataset.kind];
    if (!make) return;
    make(box).mount(box);
    header(box, helpOpen);
    keyboard(box);
    decorateLive(box);
  };

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".explorer").forEach(setup);
  });
})();
