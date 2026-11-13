// kinds: hll
//   hll                    0105        part c, HyperLogLog: a stream of 20,000 transactions (data-stream rand: distinct addresses, dup: 2,000 addresses that repeat, seq: one line after the other), a hash (data-hash mix: mix64, ident: the address itself, same: mix64 with the rank counted over the register's bits too) and m (data-m 16, 64, 256 or 1024); stepped to 21 checkpoints from 10 to 20,000 transactions: the registers as a heat grid (the ones changed in the step outlined) and a chart of the relative error of the estimate and of the single register of part b against the transactions, with the band of 1.04/sqrt(m); the models give the registers of tools/figures/q0105.py bit for bit
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = "\u00a0";

  // --- the models (tests/0105/test_0105.py checks them against tools/figures/q0105.py) ----

  const MASK = (1n << 64n) - 1n;
  const GOLD = 2654435761, LINES = 67108864, N = 20000, DUP_SET = 2000, SEQ_BASE = 0x80000000;
  const CHECKPOINTS = [10, 15, 20, 30, 50, 70, 100, 150, 200, 300, 500, 700, 1000, 1500, 2000, 3000, 5000, 7000, 10000, 15000, 20000];
  // mix64 of the page: splitmix64's finalizer, in BigInt
  const hllMix = (a) => {
    let x = (BigInt(a) + 0x9E3779B97F4A7C15n) & MASK;
    x = ((x ^ (x >> 30n)) * 0xBF58476D1CE4E5B9n) & MASK;
    x = ((x ^ (x >> 27n)) * 0x94D049BB133111EBn) & MASK;
    return x ^ (x >> 31n);
  };
  const hllHash = (a, kind) => (kind === "ident" ? (BigInt(a) << 32n) & MASK : hllMix(a));
  const distinctAddr = (t) => 64 * ((t * GOLD) % LINES);
  // the three streams of the box, as stream() of q0105.py (addresses below 2^33, exact in a Number)
  const hllStream = (name, n = N) => Array.from({ length: n }, (_, i) => {
    const t = i + 1;
    if (name === "dup") return distinctAddr(1 + ((t * GOLD) % LINES) % DUP_SET);
    if (name === "seq") return SEQ_BASE + 64 * t;
    return distinctAddr(t);
  });
  // the hash as two 32-bit halves; the leading zeros of all 64 bits (64 for 0)
  const halves = (h) => [Number(h >> 32n), Number(h & 0xFFFFFFFFn)];
  const clz64 = (hi, lo) => (hi ? Math.clz32(hi) : 32 + Math.clz32(lo));
  // the register (the top p bits) and the rank of the other 64 - p bits; kind "same" counts
  // the rank over the whole hash, the register's bits too (the trap)
  const splitHalves = (hi, lo, p, kind) => {
    const j = p ? hi >>> (32 - p) : 0;
    if (kind === "same") return [j, clz64(hi, lo) + 1];
    const hm = p ? (hi & (0xFFFFFFFF >>> p)) >>> 0 : hi;
    const lz = hm ? Math.clz32(hm) - p : lo ? 32 - p + Math.clz32(lo) : 64 - p;
    return [j, lz + 1];
  };
  const hllSplit = (h, p, kind = "mix") => splitHalves(...halves(h), p, kind);
  const hllAlpha = (m) => 0.7213 / (1 + 1.079 / m);
  const hllEstimate = (regs) => {
    const m = regs.length;
    let sum = 0, zeros = 0;
    for (const r of regs) { sum += 2 ** -r; if (r === 0) zeros++; }
    const raw = hllAlpha(m) * m * m / sum, linear = raw <= 2.5 * m && zeros > 0;
    return { raw, zeros, linear, est: linear ? m * Math.log(m / zeros) : raw };
  };
  // the tint of a register: 0 empty, then 1 to 6 by its share of the largest value
  const hllLevel = (v, vmax) => (v === 0 ? 0 : Math.min(6, Math.max(1, Math.ceil((6 * v) / Math.max(vmax, 1)))));
  const hashCache = new Map();
  const hashed = (name, kind) => {
    const key = `${name}.${kind === "ident" ? "ident" : "mix"}`;
    if (!hashCache.has(key)) {
      const addrs = hllStream(name), hi = new Array(N), lo = new Array(N);
      addrs.forEach((a, i) => { [hi[i], lo[i]] = halves(hllHash(a, kind)); });
      hashCache.set(key, { addrs, hi, lo });
    }
    return hashCache.get(key);
  };
  // the box at every checkpoint: transactions, distinct addresses so far, the estimate, the
  // single register's rank (of the whole hash), the registers and the ones the step changed
  const seriesCache = new Map();
  const hllSeries = (name, kind, p) => {
    const key = `${name}.${kind}.${p}`;
    if (seriesCache.has(key)) return seriesCache.get(key);
    const { addrs, hi, lo } = hashed(name, kind), regs = new Array(1 << p).fill(0), seen = new Set(), out = [];
    let t = 0, single = 0;
    for (const c of CHECKPOINTS) {
      const changed = new Set();
      for (; t < c; t++) {
        seen.add(addrs[t]);
        const [j, r] = splitHalves(hi[t], lo[t], p, kind);
        if (r > regs[j]) { regs[j] = r; changed.add(j); }
        single = Math.max(single, clz64(hi[t], lo[t]) + 1);
      }
      out.push({ t: c, distinct: seen.size, ...hllEstimate(regs), single, regs: regs.slice(), changed: [...changed].sort((a, b) => a - b) });
    }
    seriesCache.set(key, out);
    return out;
  };

  // --- the box ---------------------------------------------------------------------------------

  const n0 = (v) => Math.round(v).toLocaleString("en-US");
  const pct = (e) => `${e >= 0 ? "+" : "−"}${Math.abs(e * 100).toFixed(1)}%`;
  const STREAMS = { rand: "כתובות שונות", dup: "2,000 כתובות שחוזרות", seq: "כתובות רציפות" };
  const HASHES = { mix: "mix64", ident: "הכתובת עצמה", same: "אותם ביטים" };

  // the relative error of the estimates against the transactions (a log axis), the band of
  // one standard error, the points up to the step; a point past +100% sits on the edge
  const chart = (series, k, p) => {
    const W = 400, H = 232, X0 = 46, XR = 14, TOP = 12, BASE = 200;
    const L0 = 1, L1 = Math.log10(CHECKPOINTS[CHECKPOINTS.length - 1]);
    const X = (t) => X0 + ((Math.log10(t) - L0) / (L1 - L0)) * (W - X0 - XR);
    const Y = (e) => TOP + ((1 - Math.max(-1, Math.min(1, e))) / 2) * (BASE - TOP);
    const sd = 1.04 / Math.sqrt(1 << p), f1 = (v) => v.toFixed(1);
    const shown = series.slice(0, k);
    let s = `<svg class="perf-chart hll-chart" viewBox="0 0 ${W} ${H}" direction="ltr" role="img" aria-label="${`השגיאה של האומדן מול מספר הטרנזקציות, ${k ? `עד ${n0(series[k - 1].t)}` : "לפני הטרנזקציה הראשונה"}`}">`;
    s += `<rect class="hll-band" x="${f1(X(10))}" y="${f1(Y(sd))}" width="${f1(X(20000) - X(10))}" height="${f1(Y(-sd) - Y(sd))}"><title>${ltr(`±1.04/√m = ±${(sd * 100).toFixed(2)}%`)}</title></rect>`;
    [[-1, "−100%"], [-0.5, "−50%"], [0, "0"], [0.5, "+50%"], [1, "+100%"]].forEach(([e, t]) => {
      s += `<line class="${e === 0 ? "axis" : "grid"}" x1="${X0}" x2="${W - XR}" y1="${f1(Y(e))}" y2="${f1(Y(e))}"/>` +
        `<text class="tick" x="${X0 - 5}" y="${f1(Y(e) + 4)}" text-anchor="end">${t}</text>`;
    });
    [[10, "10"], [100, "100"], [1000, "1,000"], [10000, "10,000"]].forEach(([t, lab]) => {
      s += `<line class="grid" x1="${f1(X(t))}" x2="${f1(X(t))}" y1="${TOP}" y2="${BASE}"/>` +
        `<text class="tick" x="${f1(X(t))}" y="${BASE + 18}" text-anchor="middle">${lab}</text>`;
    });
    if (k) s += `<line class="hll-cursor" x1="${f1(X(series[k - 1].t))}" x2="${f1(X(series[k - 1].t))}" y1="${TOP - 4}" y2="${BASE}"/>`;
    const pts = (val) => shown.map((x) => [X(x.t), val(x) / x.distinct - 1]);
    const line = (cls, ps) => (ps.length > 1 ? `<polyline class="${cls}" points="${ps.map(([x, e]) => `${f1(x)},${f1(Y(e))}`).join(" ")}"/>` : "");
    const one = pts((x) => 2 ** x.single), est = pts((x) => x.est);
    s += line("hll-line-one", one) + line("hll-line-est", est);
    one.forEach(([x, e], i) => {
      const tip = `${n0(shown[i].t)} טרנזקציות${NB}: רגיסטר אחד R = ${shown[i].single}, ${n0(2 ** shown[i].single)}, ${pct(e)}`;
      s += e > 1 ? `<path class="hll-dot-one is-clip" d="M${f1(x)},${f1(Y(1) - 2)} l-5,8 h10 z"><title>${tip}</title></path>`
        : `<rect class="hll-dot-one" x="${f1(x - 3.5)}" y="${f1(Y(e) - 3.5)}" width="7" height="7"><title>${tip}</title></rect>`;
    });
    est.forEach(([x, e], i) => {
      s += `<circle class="hll-dot-est" cx="${f1(x)}" cy="${f1(Y(e))}" r="4"><title>${n0(shown[i].t)} טרנזקציות${NB}: האומדן ${n0(shown[i].est)} מול ${n0(shown[i].distinct)}, ${pct(e)}</title></circle>`;
    });
    return `${s}</svg>`;
  };

  // the registers as a square grid, tinted by value; the ones the step changed outlined
  const grid = (regs, changed, vmax) => {
    const m = regs.length, side = Math.round(Math.sqrt(m)), C = 256 / side, txt = m <= 64;
    const isNew = new Set(changed);
    let s = `<svg class="figure hll-grid" viewBox="-2 -2 260 260" direction="ltr" role="img" aria-label="${`${m} הרגיסטרים, ${regs.filter((v) => v === 0).length} ריקים, הגבוה ${Math.max(...regs)}`}">`;
    regs.forEach((v, j) => {
      const x = (j % side) * C, y = Math.floor(j / side) * C;
      s += `<g class="hll-reg hll-c${hllLevel(v, vmax)}${isNew.has(j) ? " is-new" : ""}"><rect x="${x + 1}" y="${y + 1}" width="${C - 2}" height="${C - 2}" rx="${m <= 64 ? 3 : 1}"/>` +
        (txt && v ? `<text x="${x + C / 2}" y="${y + C / 2 + (m <= 16 ? 8 : 5)}" text-anchor="middle" class="${m <= 16 ? "is-big" : ""}">${v}</text>` : "") +
        (txt ? `<title>רגיסטר ${j}${NB}: ${v || "ריק"}</title>` : "") + "</g>";
    });
    return `${s}</svg>`;
  };

  const hllView = () => ({
    mount(box) {
      const ds = box.dataset, st = { k: 0 };
      const pOf = { 16: 4, 64: 6, 256: 8, 1024: 10 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הזרם <select class="hll-stream">${Object.entries(STREAMS).map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<label>ה-hash <select class="hll-hash">${Object.entries(HASHES).map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<label>רגיסטרים <select class="hll-m">${[16, 64, 256, 1024].map((m) => `<option value="${pOf[m]}">${m.toLocaleString("en-US")}</option>`).join("")}</select></label></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<p class="wv-step hll-step" aria-live="polite"></p>` +
        `<div class="hll-chartwrap"></div>` +
        `<span class="viz-legend hll-legend1"><span><i class="hll-key-est"></i>HyperLogLog</span><span><i class="hll-key-single"></i>רגיסטר אחד, ${ltr("2<sup>R</sup>")}</span>` +
        `<span><i class="hll-key-band"></i>${ltr("±1.04/√m")}</span><span>אופקי${NB}: טרנזקציות, אנכי${NB}: השגיאה</span></span>` +
        `<div class="hll-gridwrap" data-fig-strip></div>` +
        `<span class="viz-legend hll-legend2"></span>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const streamIn = $(".hll-stream"), hashIn = $(".hll-hash"), mIn = $(".hll-m");
      if (STREAMS[ds.stream]) streamIn.value = ds.stream;
      if (HASHES[ds.hash]) hashIn.value = ds.hash;
      if (pOf[ds.m]) mIn.value = String(pOf[ds.m]);
      const T = CHECKPOINTS.length;
      const series = () => hllSeries(streamIn.value, hashIn.value, Number(mIn.value));
      const draw = () => {
        const sr = series(), p = Number(mIn.value), m = 1 << p, k = Math.min(Math.max(st.k, 0), T);
        st.k = k;
        const last = sr[T - 1], vmax = Math.max(1, ...last.regs);
        const cur = k ? sr[k - 1] : null, regs = cur ? cur.regs : new Array(m).fill(0);
        $(".hll-chartwrap").innerHTML = chart(sr, k, p);
        $(".hll-gridwrap").innerHTML = grid(regs, cur ? cur.changed : [], vmax);
        $(".hll-legend2").innerHTML = `<span><i class="hll-key-c0"></i>ריק</span><span class="hll-scale">1 ${[1, 2, 3, 4, 5, 6].map((l) => `<i class="hll-key-c${l}"></i>`).join("")} ${vmax}</span>` +
          `<span><i class="hll-key-new"></i>השתנה בצעד</span>`;
        const used = regs.filter((v) => v > 0).length;
        let text;
        if (!cur) text = `ההתחלה${NB}: עוד לא עברה אף טרנזקציה, וכל ${n0(m)} הרגיסטרים ריקים. כל צעד מעביר טרנזקציות עד העצירה הבאה, 10, 15, 20, 30 ועד 20,000.`;
        else {
          const e = cur.est / cur.distinct - 1;
          text = `אחרי ${n0(cur.t)} טרנזקציות${NB}: ${n0(cur.distinct)} כתובות שונות, ${n0(used)} מתוך ${n0(m)} רגיסטרים בשימוש. ` +
            `האומדן ${n0(cur.est)}, ${ltr(pct(e))}, ` + (cur.linear ? `בספירה ליניארית, כי ${n0(cur.zeros)} רגיסטרים ריקים. ` : "מהנוסחה ההרמונית. ") +
            `רגיסטר אחד${NB}: ${ltr(`R = ${cur.single}`)}, כלומר ${n0(2 ** cur.single)}. בצעד הזה השתנו ${cur.changed.length === 1 ? "רגיסטר אחד" : `${n0(cur.changed.length)} רגיסטרים`}.`;
        }
        $(".hll-step").innerHTML = text;
        $(".ex-pos").textContent = `צעד ${k} מתוך ${T}`;
        $(".ex-prev").disabled = k === 0;
        $(".ex-next").disabled = k >= T;
        if (k < T) { answer(box, null); return; }
        const e = last.est / last.distinct - 1, sd = 1.04 / Math.sqrt(m);
        answer(box, `${n0(last.distinct)} כתובות שונות ב-20,000 טרנזקציות. ${n0(m)} רגיסטרים, ${n0((m * 6) / 8)} בתים, אומדים ${n0(last.est)}, ${ltr(pct(e))}, ` +
          `${Math.abs(e) <= 2 * sd ? "בתוך" : "מחוץ ל"}שתי שגיאות תקניות של ${ltr(`${(sd * 100).toFixed(1)}%`)}. רגיסטר אחד${NB}: ${n0(2 ** last.single)}.`, ".hll-dot-est:last-of-type");
      };
      let stop = () => {};
      const changed = () => { stop(); draw(); };
      [streamIn, hashIn, mIn].forEach((el) => el.addEventListener("change", changed));
      $(".ex-next").addEventListener("click", () => { stop(); if (st.k < T) { st.k++; draw(); } });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.k > 0) { st.k--; draw(); } });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = T; draw(); });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= T, restart: () => { st.k = 0; draw(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { hll: hllView },
    help: {
      hll: `״הצעד הבא״ ו״הפעלה״ מעבירים את הזרם עד העצירה הבאה, מ-10 טרנזקציות עד 20,000. הגרף מראה את השגיאה של האומדן, (האומדן פחות האמת) חלקי האמת, בכל עצירה${NB}: עיגולים ל-HyperLogLog וריבועים לרגיסטר האחד של סעיף ב, ומשולש בקצה כשהשגיאה מעל 100%. הפס האפור הוא שגיאה תקנית אחת, 1.04/√m. הרשת היא הרגיסטרים, כהים יותר ככל שהערך גבוה, עם מסגרת לאלה שהשתנו בצעד. הזרם, ה-hash ומספר הרגיסטרים בוחרים את הדוגמה.`,
    },
    models: { hllMix, hllHash, hllStream, hllSplit, hllAlpha, hllEstimate, hllLevel, hllSeries, hllCheckpoints: CHECKPOINTS },
    cols: { hll: { main: ".hll-chartwrap, .hll-legend1", side: ".hll-gridwrap, .hll-legend2", w: "minmax(0, 1.3fr)" } },
  });
})();
