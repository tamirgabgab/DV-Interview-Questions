// kinds: intervals
//   intervals              0066        intervals typed as "s-e" (or "s-e-h" with a height) drawn as bars over an axis, and three modes: a, merge() interval by interval in sorted order with the merged result growing on the row under the axis; b, skyline() position by position with the heights as stacked blocks and the total-height line built left to right, the running sum shown; c, above() and peak() piece by piece over the skyline, the threshold T on a slider, the ranges at or above it and the peak marked
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, explain, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMAX = 10, TMAX = 60, HMAX = 9;

  // Part a interval by interval, as tools/figures/q0066.py trace_merge(): the merged list
  // before and after, and the decision (new, extend, inside).
  const ivMerge = (intervals) => {
    const sorted = intervals.map(([s, e]) => [s, e]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const ev = [], out = [];
    sorted.forEach(([s, e], i) => {
      const before = out.map((x) => x.slice());
      let kind;
      if (out.length && s <= out[out.length - 1][1]) {
        kind = e > out[out.length - 1][1] ? "extend" : "inside";
        out[out.length - 1][1] = Math.max(out[out.length - 1][1], e);
      } else { kind = "new"; out.push([s, e]); }
      ev.push({ i, s, e, kind, prev_end: before.length ? before[before.length - 1][1] : null, before, after: out.map((x) => x.slice()) });
    });
    return ev;
  };
  // Part b position by position, as trace_skyline(): the events at the position (−h before
  // +h, then by the interval's index), the total before and after them, the piece emitted
  // for the gap since the previous position and whether it joined the previous piece.
  const ivSkyline = (triples) => {
    const events = [];
    triples.forEach(([s, e, h], i) => { events.push([s, h, i]); events.push([e, -h, i]); });
    events.sort((a, b) => a[0] - b[0] || a[1] - b[1] || a[2] - b[2]);
    const ev = [], out = [];
    let total = 0, prev = null, k = 0;
    while (k < events.length) {
      const p = events[k][0], mine = [];
      while (k < events.length && events[k][0] === p) { mine.push({ i: events[k][2], d: events[k][1] }); k++; }
      let piece = null, joined = false;
      if (prev !== null && total !== 0) {
        if (out.length && out[out.length - 1][1] === prev && out[out.length - 1][2] === total) { out[out.length - 1][1] = p; joined = true; }
        else out.push([prev, p, total]);
        piece = [prev, p, total];
      }
      const before = total;
      total += mine.reduce((a, m) => a + m.d, 0);
      ev.push({ p, events: mine, before, after: total, prev, piece, joined, pieces: out.map((x) => x.slice()) });
      prev = p;
    }
    return ev;
  };
  const ivPieces = (triples) => { const ev = ivSkyline(triples); return ev.length ? ev[ev.length - 1].pieces : []; };
  // Part c piece by piece, as trace_above(): whether the piece reaches t and joined the last
  // range, the ranges so far, the peak so far and where it holds.
  const ivAbove = (pieces, t) => {
    const ev = [], ranges = [];
    let peak = 0, where = [];
    pieces.forEach(([s, e, h], j) => {
      const ok = h >= t;
      let joined = false;
      if (ok) {
        if (ranges.length && ranges[ranges.length - 1][1] === s) { ranges[ranges.length - 1][1] = e; joined = true; }
        else ranges.push([s, e]);
      }
      if (h > peak) { peak = h; where = [[s, e]]; }
      else if (h === peak) {
        if (where.length && where[where.length - 1][1] === s) where[where.length - 1][1] = e; else where.push([s, e]);
      }
      ev.push({ j, s, e, h, ok, joined, ranges: ranges.map((r) => r.slice()), peak, where: where.map((w) => w.slice()) });
    });
    return ev;
  };

  // "s-e" or "s-e-h" per interval; a pair gets the height 1
  const parse = (text) => {
    const toks = String(text).trim().split(/[\s,;]+/).filter(Boolean);
    if (!toks.length || toks.length > NMAX) return null;
    const out = [];
    for (const tok of toks) {
      const m = /^(\d+)-(\d+)(?:-(\d+))?$/.exec(tok);
      if (!m) return null;
      const s = Number(m[1]), e = Number(m[2]), h = m[3] === undefined ? 1 : Number(m[3]);
      if (!(s < e) || e > TMAX || h < 1 || h > HMAX) return null;
      out.push([s, e, h]);
    }
    return out;
  };
  const text = (ivs, withH) => ivs.map(([s, e, h]) => (withH ? `${s}-${e}-${h}` : `${s}-${e}`)).join(" ");
  const span = (a, b, closed) => (closed ? `[${a}, ${b}]` : `[${a}, ${b})`);
  const spans = (list, closed) => list.map(([a, b]) => span(a, b, closed)).join(" ");
  // a list in Hebrew text: every interval its own short LTR run, so a long list wraps between them
  const spansH = (list, closed) => list.map(([a, b]) => ltr(span(a, b, closed))).join(" ");

  const MODES = { a: "מיזוג קטעים (סעיף א)", b: "הגובה הכולל (סעיף ב)", c: "השיא והסף (סעיף ג)" };
  const STEPS = {
    a: ["מיון לפי ההתחלה", "מתחיל עד הסוף : מאריכים", "מתחיל אחרי הסוף : קטע חדש", "התשובה : הרשימה הממוזגת"],
    b: ["שני אירועים לקטע, +h ו-−h", "מיון לפי מיקום", "לפני האירועים : פולטים חתיכה", "מעדכנים את הסכום"],
    c: ["החתיכות של סעיף ב", "הסף : מצטרפת לטווח או פותחת חדש", "השיא : הגובה הגדול ביותר"],
  };
  const CODE = { a: "merge", b: "skyline", c: "above" };
  const V = (name, before, after) => ltr(before === after ? `${name} = ${after}` : `${name} : ${before} → ${after}`);

  // --- drawing ------------------------------------------------------------------------
  const L = 64, R = 44, W = 640, BAR = 16, GAP = 8, TOP = 14;
  const open = (H, label) => `<svg class="figure iv-fig iv-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="${label}">`;
  const axis = (lo, T, bottom) => {
    const spanT = Math.max(T - lo, 1), x = (t) => L + ((W - L - R) * (t - lo)) / spanT;
    const step = spanT <= 12 ? 1 : spanT <= 24 ? 2 : 5;
    let s = "";
    for (let t = lo; t <= T; t += step) s += `<line class="grid" x1="${x(t)}" x2="${x(t)}" y1="${TOP - 4}" y2="${bottom}"/><text class="tick" x="${x(t)}" y="${bottom + 14}" text-anchor="middle">${t}</text>`;
    return { s, x };
  };
  // a label beside a cursor, on the side that has room
  const label = (X, y, txt) => (X > (L + W - R) / 2 ? `<text class="legend" x="${X - 4}" y="${y}" text-anchor="end">${txt}</text>` : `<text class="legend" x="${X + 4}" y="${y}">${txt}</text>`);
  const bars = (ivs, x, cls, withH) => ivs.map(([a, b, h], i) => {
    const y = TOP + i * (BAR + GAP);
    return `<text class="iv-name" x="${L - 8}" y="${y + BAR - 3}" text-anchor="end">${i + 1}</text>` +
      `<rect class="iv-bar${withH ? ` iv-c${i % 4}` : ""}${cls(i)}" x="${x(a)}" y="${y}" width="${x(b) - x(a)}" height="${BAR}" rx="3"><title>${withH ? `[${a}, ${b}) height ${h}` : `[${a}, ${b}]`}</title></rect>` +
      (withH ? `<text class="iv-h" x="${x(b) + 6}" y="${y + BAR - 3}">h = ${h}</text>` : "");
  }).join("");

  // mode a: the sorted intervals, a row each, the merged result on the row under the axis,
  // the end of the last merged interval as a cursor while a step decides
  const svgA = (ivs, e) => {
    const sorted = ivs.map(([s, t]) => [s, t]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const lo = Math.min(0, ...sorted.map((v) => v[0])), T = Math.max(...sorted.map((v) => v[1]));
    const yAxis = TOP + sorted.length * (BAR + GAP) + 6, yRes = yAxis + 44, H = yRes + BAR + 10;
    const { s: g, x } = axis(lo, T, yAxis);
    let s = open(H, `הקטעים ממוינים לפי ההתחלה, ומתחת לציר הקטעים הממוזגים עד הצעד הזה`) + g;
    const i = e ? e.i : -1;
    s += bars(sorted, x, (j) => (j === i ? " is-cur" : j < i ? " is-done" : " is-wait"), false);
    s += `<line class="axis" x1="${L}" x2="${W - R}" y1="${yAxis}" y2="${yAxis}"/>`;
    s += `<text class="iv-name" x="${L - 8}" y="${yRes + BAR - 3}" text-anchor="end">merged</text>`;
    if (e) {
      e.after.forEach(([a, b], m) => {
        s += `<rect class="iv-merged${m === e.after.length - 1 ? " is-now" : ""}" x="${x(a)}" y="${yRes}" width="${x(b) - x(a)}" height="${BAR}" rx="3"><title>merged: [${a}, ${b}]</title></rect>`;
      });
      if (e.prev_end !== null) s += `<line class="iv-cursor" x1="${x(e.prev_end)}" x2="${x(e.prev_end)}" y1="${TOP - 4}" y2="${yRes + BAR}"/>` + label(x(e.prev_end), yRes - 6, `end = ${e.prev_end}`);
    }
    return s + "</svg>";
  };

  // the gaps between consecutive event positions with the intervals covering each
  const stacks = (triples) => {
    const pos = [...new Set(triples.flatMap(([s, e]) => [s, e]))].sort((a, b) => a - b);
    return pos.slice(1).map((b, k) => { const a = pos[k]; return [a, b, triples.map((v, i) => (v[0] <= a && b <= v[1] ? i : -1)).filter((i) => i >= 0)]; });
  };
  const chart = (triples) => {
    const lo = Math.min(0, ...triples.map((v) => v[0])), T = Math.max(...triples.map((v) => v[1]));
    const peak = Math.max(0, ...stacks(triples).map(([, , idx]) => idx.reduce((a, i) => a + triples[i][2], 0)));
    const yAxis = TOP + triples.length * (BAR + GAP) + 6;
    const unit = Math.max(10, Math.min(22, Math.floor(120 / Math.max(peak, 1))));
    const ch = unit * Math.max(peak, 1), cy0 = yAxis + 42;
    const { s, x } = axis(lo, T, yAxis);
    const yc = (c) => cy0 + ch - (ch * c) / Math.max(peak, 1);
    const tick = peak <= 8 ? 1 : peak <= 16 ? 2 : 5;
    let g = s;
    for (let c = 0; c <= peak; c += tick) g += `<text class="tick" x="${L - 8}" y="${yc(c) + 4}" text-anchor="end">${c}</text>`;
    return { lo, T, peak, yAxis, cy0, ch, x, yc, g };
  };

  // mode b: the bars with their heights, the stacked blocks up to the current position, the
  // total-height line so far, the piece just emitted outlined, a cursor at the position
  const svgB = (triples, e) => {
    const c = chart(triples), H = c.cy0 + c.ch + 10;
    const at = e ? new Set(e.events.map((m) => m.i)) : new Set();
    let s = open(H, "הקטעים עם הגבהים שלהם, ומתחת לציר הגובה הכולל כבלוקים, עד המיקום של הצעד") + c.g;
    s += bars(triples, c.x, (i) => (at.has(i) ? " is-cur" : ""), true);
    s += `<line class="axis" x1="${L}" x2="${W - R}" y1="${c.yAxis}" y2="${c.yAxis}"/>`;
    s += `<text class="iv-name" x="${L - 8}" y="${c.cy0 - 8}" text-anchor="end">total</text>`;
    const upto = e ? e.p : null;
    let d = `M${c.x(c.lo)},${c.yc(0)}`;
    stacks(triples).forEach(([a, b, idx]) => {
      if (upto === null || a >= upto) return;
      let level = 0;
      idx.forEach((i) => {
        const h = triples[i][2];
        s += `<rect class="iv-blk iv-c${i % 4}" x="${c.x(a)}" y="${c.yc(level + h)}" width="${c.x(b) - c.x(a)}" height="${c.yc(level) - c.yc(level + h)}"><title>[${a}, ${b}): interval ${i + 1} adds ${h}</title></rect>`;
        level += h;
      });
      d += ` H${c.x(a)} V${c.yc(level)} H${c.x(b)}`;
    });
    if (e) d += ` H${c.x(e.p)} V${c.yc(e.after)}`;
    s += `<path class="iv-line" d="${d}"/>`;
    if (e) {
      e.pieces.forEach(([a, b, t], m) => {
        const now = e.piece && e.piece[1] === b && e.piece[2] === t;
        s += `<rect class="iv-piece${now ? " is-now" : ""}" x="${c.x(a)}" y="${c.yc(t)}" width="${c.x(b) - c.x(a)}" height="${c.yc(0) - c.yc(t)}"><title>piece ${m + 1}: [${a}, ${b}) total ${t}</title></rect>`;
      });
      s += `<line class="iv-cursor" x1="${c.x(e.p)}" x2="${c.x(e.p)}" y1="${TOP - 4}" y2="${c.cy0 + c.ch}"/>`;
      s += label(c.x(e.p), c.cy0 - 8, `total = ${e.after}`);
    }
    return s + "</svg>";
  };

  // mode c: the whole skyline as a line, the pieces read so far filled (tinted when they
  // reach T), the current one outlined, the threshold line, the peak so far dashed, and the
  // ranges found on a row under the chart
  const svgC = (triples, pieces, e, t) => {
    const c = chart(triples), yRng = c.cy0 + c.ch + 22, H = yRng + BAR + 10;
    let s = open(H, `הגובה הכולל כקו, הסף T = ${t}, השיא, והטווחים בגובה לפחות T עד הצעד הזה`) + c.g;
    s += bars(triples, c.x, () => " is-done", true);
    s += `<line class="axis" x1="${L}" x2="${W - R}" y1="${c.yAxis}" y2="${c.yAxis}"/>`;
    s += `<text class="iv-name" x="${L - 8}" y="${c.cy0 - 8}" text-anchor="end">total</text>`;
    const j = e ? e.j : -1;
    pieces.forEach(([a, b, h], m) => {
      if (m > j) return;
      s += `<rect class="iv-piece${h >= t ? " is-ok" : ""}${m === j ? " is-now" : ""}" x="${c.x(a)}" y="${c.yc(h)}" width="${c.x(b) - c.x(a)}" height="${c.yc(0) - c.yc(h)}"><title>piece ${m + 1}: [${a}, ${b}) total ${h}</title></rect>`;
    });
    let d = `M${c.x(c.lo)},${c.yc(0)}`;
    stacks(triples).forEach(([a, b, idx]) => { d += ` H${c.x(a)} V${c.yc(idx.reduce((q, i) => q + triples[i][2], 0))} H${c.x(b)}`; });
    d += ` V${c.yc(0)}`;
    s += `<path class="iv-line" d="${d}"/>`;
    const tt = Math.min(t, c.peak);
    s += `<line class="iv-thr" x1="${L}" x2="${W - R}" y1="${c.yc(tt)}" y2="${c.yc(tt)}"/><text class="legend" x="${W - R + 4}" y="${c.yc(tt) + 4}">T = ${t}</text>`;
    if (e) s += `<line class="iv-peak" x1="${L}" x2="${W - R}" y1="${c.yc(e.peak)}" y2="${c.yc(e.peak)}"/>`;
    s += `<text class="iv-name" x="${L - 8}" y="${yRng + BAR - 3}" text-anchor="end">≥ T</text>`;
    if (e) {
      e.ranges.forEach(([a, b], m) => { s += `<rect class="iv-range${m === e.ranges.length - 1 && e.ok ? " is-now" : ""}" x="${c.x(a)}" y="${yRng}" width="${c.x(b) - c.x(a)}" height="${BAR}" rx="3"><title>total at least ${t} on [${a}, ${b})</title></rect>`; });
      e.where.forEach(([a, b]) => { s += `<rect class="iv-top" x="${c.x(a)}" y="${c.yc(e.peak) - 3}" width="${c.x(b) - c.x(a)}" height="6"><title>the peak ${e.peak} on [${a}, ${b})</title></rect>`; });
    }
    return s + "</svg>";
  };

  const intervalsView = () => ({
    mount(box) {
      const mode0 = MODES[box.dataset.mode] ? box.dataset.mode : "a";
      const d0 = { mode: mode0, ivs: parse(box.dataset.ivs || "1-3 2-6 8-10 15-18") || [[1, 3, 1], [2, 6, 1], [8, 10, 1], [15, 18, 1]], t: Math.max(1, Number(box.dataset.t) || 1) };
      const st = { mode: d0.mode, ivs: d0.ivs.map((v) => v.slice()), t: d0.t, s: 0, n: 6 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המצב <select class="iv-mode" aria-label="איזה סעיף">${Object.entries(MODES).map(([v, w]) => `<option value="${v}">${w}</option>`).join("")}</select></label>` +
        `<label><span>הקטעים</span><input type="text" class="ex-num iv-ivs" dir="ltr" spellcheck="false" aria-label="הקטעים : התחלה-סוף, או התחלה-סוף-גובה, מופרדים ברווח"></label>` +
        `<label class="iv-tlab"><span>T</span> <input type="range" class="iv-t" min="1" max="9" step="1" dir="ltr" aria-label="הסף T"><output class="iv-tout"></output></label>` +
        `<label>בהגרלה <select class="iv-n" aria-label="כמה קטעים להגריל">${[4, 6, 8, 10].map((v) => `<option value="${v}"${v === 6 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button iv-rand">הגרלה</button><span class="iv-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err iv-err" role="status"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary iv-sum" aria-live="polite"></p>` +
        `<div class="iv-wrap" data-fig-strip></div>` +
        `<span class="viz-legend"><span class="iv-only-a"><i class="iv-key-bar"></i>קטע מהקלט</span><span class="iv-only-a"><i class="iv-key-merged"></i>קטע ממוזג</span>` +
        `<span class="iv-not-a"><i class="iv-key-blk"></i>הגובה של קטע אחד</span><span class="iv-not-a"><i class="iv-key-line"></i>הגובה הכולל</span><span class="iv-only-b"><i class="iv-key-piece"></i>חתיכה שנפלטה</span>` +
        `<span class="iv-only-c"><i class="iv-key-thr"></i>הסף T</span><span class="iv-only-c"><i class="iv-key-peak"></i>השיא עד עכשיו</span><span class="iv-only-c"><i class="iv-key-range"></i>טווח בגובה לפחות T</span>` +
        `<span><i class="iv-key-cur"></i>הקטע או החתיכה של הצעד</span></span>` +
        `<p class="iv-note"></p>`;
      const show = explain(box, "הסבר : השלבים של הפתרון והקוד");
      answer(box, NB); answer(box, null);           // the answer line keeps its place from the first step
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const pieces = () => ivPieces(st.ivs);
      const peakOf = () => Math.max(1, ...pieces().map((p) => p[2]));
      const frames = () => (st.mode === "a" ? ivMerge(st.ivs) : st.mode === "b" ? ivSkyline(st.ivs) : ivAbove(pieces(), st.t));
      const draw = () => {
        const F = frames(), N = F.length, m = st.mode, n = st.ivs.length;
        st.s = Math.min(Math.max(st.s, 0), N);
        const e = st.s ? F[st.s - 1] : null, done = st.s === N, prev = st.s > 1 ? F[st.s - 2] : null;
        $(".iv-mode").value = m; $(".iv-ivs").value = text(st.ivs, m !== "a");
        $(".iv-t").max = String(peakOf()); $(".iv-t").value = String(st.t); $(".iv-tout").textContent = String(st.t);
        $(".iv-tlab").hidden = m !== "c";
        box.classList.toggle("iv-is-a", m === "a"); box.classList.toggle("iv-is-b", m === "b"); box.classList.toggle("iv-is-c", m === "c");
        $(".ex-pos").textContent = `צעד ${st.s} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        let sum = "", note = "", lit = [], lines = { py: [], sv: [] }, vars = "", ans = null, marks = [];
        if (m === "a") {
          $(".iv-wrap").innerHTML = svgA(st.ivs, e);
          sum = e ? `הקטע ${ltr(e.i + 1)} מתוך ${ltr(n)} (ממוין)${NB}: ${ltr(span(e.s, e.e, true))}. הפלט${NB}: ${spansH(e.after, true)}.`
            : `${ltr(n)} קטעים, ממוינים לפי ההתחלה. כל צעד הוא קטע אחד, שנבדק מול הסוף של הקטע הממוזג האחרון.`;
          if (e) {
            if (e.prev_end === null) note = `הפלט ריק, ולכן ${ltr(span(e.s, e.e, true))} נפתח כקטע הראשון.`;
            else if (e.kind === "new") note = `${ltr(`${e.s} > ${e.prev_end}`)}${NB}: הקטע מתחיל אחרי הסוף של הקטע הממוזג האחרון, ולכן אינו חופף לו, וגם לא לקטעים שלפניו, שנגמרים עוד קודם. הוא נוסף לפלט כקטע חדש, והקודם לא ישתנה יותר.`;
            else if (e.kind === "extend") note = `${ltr(`${e.s} ≤ ${e.prev_end}`)}${NB}: הקטע חופף לקטע הממוזג האחרון, והסוף של האחרון גדל מ-${ltr(e.prev_end)} ל-${ltr(e.e)}.`;
            else note = `${ltr(`${e.s} ≤ ${e.prev_end}`)} וגם ${ltr(`${e.e} ≤ ${e.prev_end}`)}${NB}: הקטע כולו בתוך הקטע הממוזג האחרון, ודבר לא משתנה.`;
          }
          if (!e) { lines = { py: [4, 5], sv: [6, 7, 8, 9] }; vars = ltr("out = []"); }
          else {
            lit = e.kind === "new" ? [3] : [2];
            if (done) lit.push(4);
            lines = e.kind === "new" ? { py: [5, 6, 8, 9, ...(done ? [10] : [])], sv: [10, 11, 13, ...(done ? [15] : [])] } : { py: [5, 6, 7, ...(done ? [10] : [])], sv: [10, 11, 12, ...(done ? [15] : [])] };
            const endAfter = e.after[e.after.length - 1][1];
            vars = [ltr(`i = ${e.i}`), ltr(`s = ${e.s}`), ltr(`e = ${e.e}`), V("end", e.prev_end === null ? "—" : e.prev_end, endAfter), ltr(`out = ${spans(e.after, true)}`)].join(" · ");
          }
          if (done && e) { ans = `הקטעים הממוזגים${NB}: ${spansH(e.after, true)}.`; marks = ".iv-wrap .iv-merged"; }
        } else if (m === "b") {
          $(".iv-wrap").innerHTML = svgB(st.ivs, e);
          const evs = (x) => x.events.map((q) => ltr(`${q.d > 0 ? "+" : "−"}${Math.abs(q.d)}`) + ` (קטע ${ltr(q.i + 1)})`).join(", ");
          sum = e ? `המיקום ${ltr(e.p)}${NB}: האירועים ${evs(e)}. הסכום ${ltr(`${e.before} → ${e.after}`)}. חתיכות עד עכשיו${NB}: <b>${ltr(e.pieces.length)}</b>.`
            : `${ltr(n)} קטעים, ${ltr(2 * n)} אירועים ב-${ltr(N)} מיקומים. כל צעד הוא מיקום אחד${NB}: קודם החתיכה עד אליו, ואז האירועים שבו.`;
          if (e) {
            note = e.piece ? `בין ${ltr(e.prev)} ל-${ltr(e.p)} הסכום היה ${ltr(e.before)}, ולכן נפלטת החתיכה ${ltr(span(e.prev, e.p, false))} בגובה <b>${ltr(e.before)}</b>` +
              (e.joined ? `, והיא מאריכה את החתיכה הקודמת, שנגמרת ב-${ltr(e.prev)} באותו גובה.` : ".")
              : e.prev === null ? "זה המיקום הראשון, ואין עדיין חתיכה לפלוט." : `בין ${ltr(e.prev)} ל-${ltr(e.p)} הסכום היה 0${NB}: רווח, ולא נפלט.`;
            note += ` אז ${e.events.length === 1 ? "האירוע" : `${ltr(e.events.length)} האירועים`} של המיקום${NB}: ${evs(e)}, והסכום הופך ל-${ltr(e.after)}.`;
          }
          if (!e) { lit = [1, 2]; lines = { py: [5, 6, 7], sv: [8, 9, 10, 11, 12, 13, 14, 15, 16] }; vars = ltr(`${2 * n} events, total = 0, prev = None`); }
          else {
            lit = [...(e.piece ? [3] : []), 4];
            const emit = e.piece ? (e.joined ? { py: [9, 10, 11], sv: [18, 19] } : { py: [9, 10, 12, 13], sv: [18, 20] }) : { py: [9], sv: [18] };
            lines = { py: [8, ...emit.py, 14, 15, ...(done ? [16] : [])], sv: [17, ...emit.sv, 22, 23] };
            vars = [ltr(`p = ${e.p}`), ltr(`d = ${e.events.map((q) => (q.d > 0 ? `+${q.d}` : `−${-q.d}`)).join(", ")}`), V("total", e.before, e.after), V("prev", e.prev === null ? "None" : e.prev, e.p), ltr(`out = ${e.pieces.length} pieces`)].join(" · ");
          }
          if (done && e) { ans = `החתיכות${NB}: ${e.pieces.map(([a, b, t]) => ltr(`(${a}, ${b}, ${t})`)).join(" ")}.`; marks = ".iv-wrap .iv-piece"; }
        } else {
          const P = pieces();
          $(".iv-wrap").innerHTML = svgC(st.ivs, P, e, st.t);
          sum = e ? `החתיכה ${ltr(e.j + 1)} מתוך ${ltr(P.length)}${NB}: ${ltr(span(e.s, e.e, false))} בגובה ${ltr(e.h)}, הסף ${ltr(`T = ${st.t}`)}. טווחים עד עכשיו${NB}: ${e.ranges.length ? spansH(e.ranges, false) : "אין"}. השיא עד עכשיו${NB}: <b>${ltr(e.peak)}</b>.`
            : `${ltr(P.length)} חתיכות מסעיף ב, הסף ${ltr(`T = ${st.t}`)}. כל צעד הוא חתיכה אחת${NB}: מעל הסף או לא, מצטרפת לטווח או פותחת חדש.`;
          if (e) {
            note = e.ok ? (e.joined ? `${ltr(`${e.h} ≥ ${st.t}`)}, והטווח האחרון נגמר בדיוק ב-${ltr(e.s)}${NB}: החתיכה מצטרפת אליו, והוא עכשיו ${ltr(span(e.ranges[e.ranges.length - 1][0], e.e, false))}.`
              : `${ltr(`${e.h} ≥ ${st.t}`)}, ו${e.ranges.length > 1 ? `הטווח האחרון נגמר לפני ${ltr(e.s)}` : "אין עדיין טווח"}${NB}: טווח חדש ${ltr(span(e.s, e.e, false))}.`)
              : `${ltr(`${e.h} < ${st.t}`)}${NB}: מתחת לסף, החתיכה מדולגת, והטווח הבא יתחיל מחדש.`;
            const pk = prev ? prev.peak : 0;
            note += e.h > pk ? ` <b>שיא חדש${NB}: ${ltr(e.h)} ב-${ltr(span(e.s, e.e, false))} ✓</b>` : e.h === pk ? ` הגובה שווה לשיא, ולכן גם ${ltr(span(e.s, e.e, false))} בשיא.` : ` השיא נשאר ${ltr(e.peak)}.`;
          }
          if (!e) { lit = [1]; lines = { py: [3], sv: [4] }; vars = ltr(`t = ${st.t}, out = [], top = 0`); }
          else {
            lit = [2, ...(done ? [3] : [])];
            const body = e.ok ? (e.joined ? { py: [4, 5, 6, 7], sv: [5, 6, 7] } : { py: [4, 5, 6, 8, 9], sv: [5, 6, 8] }) : { py: [4, 5], sv: [5, 6] };
            lines = { py: [...body.py, ...(done ? [10, 17, 18] : [])], sv: [...body.sv, ...(done ? [15, 16, 17] : [])] };
            vars = [ltr(`j = ${e.j}`), ltr(`piece = (${e.s}, ${e.e}, ${e.h})`), ltr(`t = ${st.t}`), ltr(`out = ${e.ranges.length ? spans(e.ranges, false) : "[]"}`), V("top", prev ? prev.peak : 0, e.peak)].join(" · ");
          }
          if (done && e) { ans = `השיא ${ltr(e.peak)} ב-${spansH(e.where, false)}. בגובה לפחות ${ltr(st.t)}${NB}: ${e.ranges.length ? spansH(e.ranges, false) : "אף טווח"}.`; marks = ".iv-wrap .iv-range, .iv-wrap .iv-top"; }
        }
        $(".iv-sum").innerHTML = sum;
        $(".iv-note").innerHTML = note;
        show({ code: CODE[m], steps: STEPS[m], lit, lines, vars });
        answer(box, ans, marks);
      };
      const total = () => frames().length;
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= total(), restart: () => { st.s = 0; draw(); } });
      const fitT = () => { st.t = Math.max(1, Math.min(st.t, peakOf())); };
      const restart = () => { stop(); st.s = 0; $(".iv-err").textContent = ""; fitT(); draw(); };
      $(".iv-mode").addEventListener("change", () => { st.mode = MODES[$(".iv-mode").value] ? $(".iv-mode").value : "a"; restart(); });
      $(".iv-ivs").addEventListener("change", () => {
        const v = parse($(".iv-ivs").value);
        if (!v) { $(".iv-err").textContent = `הקטעים${NB}: 1 עד ${NMAX} קטעים, התחלה-סוף או התחלה-סוף-גובה, ההתחלה לפני הסוף, מיקומים עד ${TMAX} וגובה 1 עד ${HMAX}`; return; }
        st.ivs = v; restart();
      });
      $(".iv-ivs").addEventListener("keydown", (ev) => { if (ev.key === "Enter") $(".iv-ivs").blur(); });
      $(".iv-t").addEventListener("input", () => { st.t = Math.round(Number($(".iv-t").value)) || 1; restart(); });
      $(".iv-n").addEventListener("change", () => { st.n = Number($(".iv-n").value); });
      const seed = seedControls(box, $(".iv-anchor"), (rng) => {
        st.ivs = Array.from({ length: st.n }, () => { const s = Math.floor(rng() * 30); return [s, s + 1 + Math.floor(rng() * 8), st.mode === "a" ? 1 : 1 + Math.floor(rng() * 5)]; });
        restart();
      }, { fresh: false });
      $(".iv-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, { mode: d0.mode, ivs: d0.ivs.map((v) => v.slice()), t: d0.t, n: 6 }); $(".iv-n").value = "6"; restart(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { intervals: intervalsView },
    help: {
      intervals: "מקלידים קטעים כזוגות התחלה-סוף (למשל 1-3 2-6), ובסעיפים ב ו-ג עם גובה, התחלה-סוף-גובה (למשל 1-7-7), או מגרילים. בסעיף א כל צעד הוא קטע אחד בסדר הממוין : מאריך את הקטע הממוזג האחרון או פותח חדש, והפלט על השורה שמתחת לציר. בסעיף ב כל צעד הוא מיקום אחד של אירועים : החתיכה עד אליו נפלטת בגובה הסכום הרץ, הבלוקים הם הגובה של כל קטע והקו הוא הסכום. בסעיף ג כל צעד הוא חתיכה אחת מול הסף T שבסליידר : מצטרפת לטווח או פותחת חדש, והשיא מקווקו. השורה שמתחת מסבירה כל צעד, והפאנל 'הסבר' מדליק את שורות הקוד.",
    },
    models: { ivMerge, ivSkyline, ivPieces, ivAbove },
  });
})();
