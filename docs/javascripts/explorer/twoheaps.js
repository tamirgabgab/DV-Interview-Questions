// kinds: twoheaps
//   twoheaps               0068        a stream of numbers (data-nums) and three modes: a, the median with two heaps, three steps a value (the push into low, low's top through to high, the balance with the median); b, the p-quantile by the nearest rank with a slider for p (data-p, percent), the target size ceil(p n) and at most one move back; c, the quantile over the last W values (data-w) with lazy deletion: the window on the stream, the values that left it greyed and struck inside the heaps until they are thrown away from a top, the live sizes and the rebuild. high is drawn above the line with its top at the bottom, low below it with its top at the top, so the two tops meet on the answer's line; the trees are drawn for the deepest heap of the run, so the figure keeps its size.
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, explain, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMAX = 15, VMAX = 99, WMAX = 7;
  const num = (v) => String(v).replace("-", "−");

  // A binary heap of [value, id] items, the smallest on top (or the largest with isMax),
  // ties by the smaller id: the same sift algorithm as tools/figures/q0068.py Heap, so the
  // array layouts (the drawn trees) are the same.
  const mkHeap = (isMax) => ({
    a: [], isMax,
    before(x, y) { return x[0] !== y[0] ? (this.isMax ? x[0] > y[0] : x[0] < y[0]) : x[1] < y[1]; },
    push(x) {
      const a = this.a;
      a.push(x);
      let i = a.length - 1;
      while (i > 0 && this.before(a[i], a[(i - 1) >> 1])) { const p = (i - 1) >> 1; [a[i], a[p]] = [a[p], a[i]]; i = p; }
    },
    pop() {
      const a = this.a, top = a[0], last = a.pop();
      if (a.length) {
        a[0] = last;
        let i = 0;
        for (;;) {
          let k = i;
          for (const c of [2 * i + 1, 2 * i + 2]) if (c < a.length && this.before(a[c], a[k])) k = c;
          if (k === i) break;
          [a[i], a[k]] = [a[k], a[i]];
          i = k;
        }
      }
      return top;
    },
    top() { return this.a[0]; },
    size() { return this.a.length; },
  });
  // the nearest rank of the p-quantile, p = num / den: ceil(p n) in integers, at least 1
  const thRank = (n, nu, de) => Math.max(1, Math.floor((nu * n + de - 1) / de));
  // the depth of a heap of n items
  const thLevels = (n) => { let d = 1; while ((1 << d) - 1 < Math.max(n, 1)) d++; return d; };
  const snap = (low, high, more) => ({ low: low.a.map((x) => x.slice()), high: high.a.map((x) => x.slice()), ...more });

  // Part a frame by frame, as trace_median(): push, through, balance (with the median).
  const thTraceMedian = (nums) => {
    const low = mkHeap(true), high = mkHeap(false), F = [];
    nums.forEach((x, i) => {
      low.push([x, i]);
      F.push(snap(low, high, { kind: "push", i, x }));
      const t = low.pop();
      high.push(t);
      F.push(snap(low, high, { kind: "through", i, x, moved: t.slice() }));
      let back = null;
      if (high.size() > low.size()) { back = high.pop(); low.push(back); }
      const ans = low.size() > high.size() ? low.top()[0] : (low.top()[0] + high.top()[0]) / 2;
      F.push(snap(low, high, { kind: "balance", i, x, moved: back ? back.slice() : null, ans }));
    });
    return F;
  };
  // Part b, as trace_quantile(): push, through, target (the move back when ceil(p n) grew).
  const thTraceQuantile = (nums, nu, de) => {
    const low = mkHeap(true), high = mkHeap(false), F = [];
    nums.forEach((x, i) => {
      const t0 = i ? thRank(i, nu, de) : 0;
      low.push([x, i]);
      F.push(snap(low, high, { kind: "push", i, x, t: t0 }));
      const t = low.pop();
      high.push(t);
      F.push(snap(low, high, { kind: "through", i, x, moved: t.slice(), t: t0 }));
      const target = thRank(i + 1, nu, de);
      let back = null;
      if (low.size() < target) { back = high.pop(); low.push(back); }
      F.push(snap(low, high, { kind: "target", i, x, moved: back ? back.slice() : null, t: target, ans: low.top()[0] }));
    });
    return F;
  };
  // Part c, as trace_window(): leave (the oldest value dies), push, through, target; the
  // dead tops pruned and the rebuilds recorded on the frame they happened in.
  const thTraceWindow = (nums, w, nu, de) => {
    const heaps = { low: mkHeap(true), high: mkHeap(false) }, F = [];
    const side = new Map(), live = { low: 0, high: 0 };
    let pruned = [], rebuilt = [];
    const prune = (s) => { const h = heaps[s]; while (h.size() && !side.has(h.top()[1])) pruned.push([s, h.pop().slice()]); };
    const move = (src, dst) => {
      prune(src);
      const x = heaps[src].pop();
      heaps[dst].push(x);
      side.set(x[1], dst); live[src]--; live[dst]++;
      return x.slice();
    };
    const rebuild = () => {
      for (const s of ["low", "high"]) {
        const h = heaps[s];
        if (h.size() > 2 * live[s]) { const keep = h.a.filter((x) => side.has(x[1])); h.a = []; keep.forEach((x) => h.push(x)); rebuilt.push(s); }
      }
    };
    const frame = (kind, i, x, more) => {
      const dead = [...heaps.low.a, ...heaps.high.a].map((e) => e[1]).filter((id) => !side.has(id)).sort((p, q) => p - q);
      F.push(snap(heaps.low, heaps.high, { kind, i, x, left: Math.max(0, i - w + 1), live: { ...live }, dead, pruned, rebuilt, ...more }));
      pruned = []; rebuilt = [];
    };
    nums.forEach((x, i) => {
      if (i >= w) {
        const gone = side.get(i - w);
        side.delete(i - w);
        live[gone]--;
        frame("leave", i, x, { gone: [nums[i - w], i - w], gone_side: gone, t: thRank(w, nu, de) });
      }
      heaps.low.push([x, i]);
      side.set(i, "low");
      live.low++;
      const t0 = i ? thRank(Math.min(i, w), nu, de) : 0;
      frame("push", i, x, { t: t0 });
      const moved = move("low", "high");
      frame("through", i, x, { moved, t: t0 });
      const target = thRank(Math.min(i + 1, w), nu, de);
      let back = null;
      if (live.low < target) back = move("high", "low");
      else if (live.low > target) back = move("low", "high");
      prune("low");
      rebuild();
      frame("target", i, x, { moved: back, t: target, ans: heaps.low.top()[0] });
    });
    return F;
  };

  const parse = (text) => {
    const toks = String(text).trim().replace(/−/g, "-").split(/[\s,;]+/).filter(Boolean);
    if (!toks.length || toks.length > NMAX || !toks.every((t) => /^-?\d+$/.test(t))) return null;
    const v = toks.map(Number);
    return v.every((x) => Math.abs(x) <= VMAX) ? v : null;
  };
  const fmt = (v) => num(Number.isInteger(v) ? v : v.toFixed(1));
  const pct = (p) => (p / 100).toFixed(2).replace(/\.?0+$/, "") || "0";

  const MODES = { a: "החציון (סעיף א)", b: "אחוזון p (סעיף ב)", c: "חלון של W הערכים האחרונים (סעיף ג)" };
  const STEPS = {
    a: ["דוחפים ל-low", "הראש של low עובר ל-high", "איזון : high גדולה יותר?", "החציון"],
    b: ["דוחפים דרך low", "היעד ⌈p · n⌉", "השלמה : חסר ל-low?", "האחוזון"],
    c: ["הערך הישן יוצא", "דוחפים דרך low", "היעד על החיים", "בנייה מחדש", "האחוזון"],
  };
  const CODE = { a: "StreamMedian", b: "StreamQuantile", c: "WindowQuantile" };
  const V = (name, before, after) => ltr(before === after ? `${name} = ${after}` : `${name} : ${before} → ${after}`);
  const vals = (a, isMax) => `[${a.slice().sort((p, q) => (isMax ? q[0] - p[0] : p[0] - q[0]) || p[1] - q[1]).map((x) => num(x[0])).join(", ")}]`;

  // --- drawing ------------------------------------------------------------------------
  // the stream as a row of cells: the values read so far, the current one framed, in
  // mode c the window outlined and the values that left it dimmed
  const svgStream = (nums, i, left, w) => {
    const n = nums.length, C = 30, W = n * C + 8, H = 50;
    let s = `<svg class="figure th-fig th-stream th-live" viewBox="0 0 ${W} ${H}" style="max-width:${Math.round(W * 1.25)}px" role="img" aria-label="הזרם : ${n} ערכים, הערך הנוכחי מסומן">`;
    nums.forEach((_, p) => { s += `<text class="tick" x="${4 + p * C + C / 2}" y="12" text-anchor="middle">${p}</text>`; });
    if (i >= 0 && w) s += `<rect class="th-win" x="${4 + left * C + 1}" y="17" width="${(i - left + 1) * C - 2}" height="30" rx="5"/>`;
    nums.forEach((v, p) => {
      const cls = p === i ? "is-cur" : p > i ? "is-wait" : w && p < left ? "is-gone" : "is-off";
      s += `<g class="th-cell ${cls}"><title>arrival ${p}: value ${v}</title><rect x="${4 + p * C + 3}" y="20" width="${C - 6}" height="24" rx="4"/><text x="${4 + p * C + C / 2}" y="37" text-anchor="middle">${num(v)}</text></g>`;
    });
    return s + "</svg>";
  };
  // the two heaps facing each other, as q0068.heaps_svg(): high above with its top at
  // the bottom, low below with its top at the top, the answer on the line between them
  const svgTwo = (low, high, L, o) => {
    const W = 320, LH = 40, R = 14, MID = 44, H = 2 * L * LH + MID + 16, ymid = 8 + L * LH + MID / 2;
    let s = `<svg class="figure th-fig th-two th-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="${o.label}">`;
    const dead = new Set(o.dead || []);
    const tree = (a, up, name) => {
      const pos = a.map((_, k) => {
        const d = thLevels(k + 1) - 1, j = k + 1 - (1 << d), slot = Math.min(64, (W - 16) / (1 << d));
        return [W / 2 + (j + 0.5 - (1 << d) / 2) * slot, up ? ymid - MID / 2 - 8 - R - d * LH : ymid + MID / 2 + 8 + R + d * LH];
      });
      for (let k = 1; k < a.length; k++) { const [x1, y1] = pos[(k - 1) >> 1], [x2, y2] = pos[k]; s += `<line class="th-edge" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"/>`; }
      a.forEach(([v, i], k) => {
        const [x, y] = pos[k], isDead = dead.has(i);
        let cls = isDead ? " is-dead" : "";
        if (k === 0 && !isDead) cls += " is-top";
        if (o.now === i) cls += " is-new";
        if (o.moved === i) cls += " is-moved";
        const what = isDead ? "left the window, not thrown away yet" : k === 0 ? "the top" : "in the heap";
        s += `<g class="th-node${cls}"><title>${name}[${k}]: value ${v}, arrival ${i}, ${what}</title><circle cx="${x}" cy="${y}" r="${R}"/><text x="${x}" y="${y + 4}" text-anchor="middle">${num(v)}</text></g>`;
        if (isDead) s += `<line class="th-strike" x1="${x - 9}" y1="${y + 9}" x2="${x + 9}" y2="${y - 9}"/>`;
      });
    };
    tree(high, true, "high");
    tree(low, false, "low");
    s += `<line class="th-mid" x1="8" y1="${ymid}" x2="${W - 8}" y2="${ymid}"/>`;
    s += `<text class="th-lab" x="10" y="${ymid - 8}">high ↑ ${o.nh}</text><text class="th-lab" x="10" y="${ymid + 16}">low ↓ ${o.nl}</text>`;
    if (o.target !== undefined) s += `<text class="th-lab th-target" x="${W - 10}" y="${ymid + 16}" text-anchor="end">target ${o.target}</text>`;
    if (o.line) s += `<rect class="th-ans-bg" x="${W / 2 - 60}" y="${ymid - 11}" width="120" height="22" rx="11"/><text class="th-ans${o.hot ? " is-now" : ""}" x="${W / 2}" y="${ymid + 5}" text-anchor="middle">${o.line}</text>`;
    return s + "</svg>";
  };

  const twoView = () => ({
    mount(box) {
      const mode0 = MODES[box.dataset.mode] ? box.dataset.mode : "a";
      const d0 = { mode: mode0, nums: parse(box.dataset.nums || "5 15 1 3 8 7 9 10 20 2") || [5, 15, 1, 3, 8, 7, 9, 10, 20, 2], p: Math.min(100, Math.max(0, Number(box.dataset.p) || 50)), w: Math.min(WMAX, Math.max(1, Number(box.dataset.w) || 4)) };
      const st = { mode: d0.mode, nums: d0.nums.slice(), p: d0.p, w: d0.w, s: 0, n: 10 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המצב <select class="th-mode" aria-label="איזה סעיף">${Object.entries(MODES).map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<label><span>הזרם</span><input type="text" class="ex-num th-nums" dir="ltr" spellcheck="false" aria-label="הזרם : עד ${NMAX} מספרים שלמים, מופרדים ברווח"></label>` +
        `<label class="th-plab"><span>p</span><input type="range" class="th-p" min="0" max="100" step="1" dir="ltr" aria-label="האחוזון p באחוזים"><output class="th-po"></output></label>` +
        `<label class="th-wlab"><span>W</span> <input type="number" class="ex-num th-w" min="1" max="${WMAX}" step="1" dir="ltr" aria-label="גודל החלון"></label>` +
        `<label>בהגרלה <select class="th-n" aria-label="כמה מספרים להגריל">${[8, 10, 12, 15].map((v) => `<option value="${v}"${v === 10 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button th-rand">הגרלה</button><span class="th-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err th-err" role="status"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary th-sum" aria-live="polite"></p>` +
        `<div class="th-wrap" data-fig-strip><div class="th-streamwrap"></div><div class="th-twowrap"></div></div>` +
        `<span class="viz-legend"><span><i class="th-key-in"></i>בערימה</span><span><i class="th-key-top"></i>הראש</span><span><i class="th-key-new"></i>הערך החדש</span>` +
        `<span><i class="th-key-moved"></i>עבר בצעד הזה</span><span class="th-only-c"><i class="th-key-dead"></i>יצא מהחלון, עוד בערימה</span><span class="th-only-c"><i class="th-key-win"></i>החלון</span></span>` +
        `<p class="th-note"></p><p class="th-tally"></p>`;
      const show = explain(box, "הסבר : השלבים של הפתרון והקוד");
      answer(box, NB); answer(box, null);           // the answer line keeps its place from the first step
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const frames = () => (st.mode === "a" ? thTraceMedian(st.nums) : st.mode === "b" ? thTraceQuantile(st.nums, st.p, 100) : thTraceWindow(st.nums, st.w, st.p, 100));
      const draw = () => {
        const F = frames(), N = F.length, nums = st.nums, n = nums.length, m = st.mode;
        st.s = Math.min(Math.max(st.s, 0), N);
        const e = st.s ? F[st.s - 1] : null, done = st.s === N, prev = st.s > 1 ? F[st.s - 2] : null;
        $(".th-mode").value = m; $(".th-nums").value = nums.join(" "); $(".th-p").value = String(st.p); $(".th-po").textContent = pct(st.p); $(".th-w").value = String(st.w);
        $(".th-plab").hidden = m === "a"; $(".th-wlab").hidden = m !== "c";
        box.classList.toggle("th-is-c", m === "c");
        $(".ex-pos").textContent = `צעד ${st.s} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        // the trees are drawn for the deepest heap of the whole run, so the figure keeps its size
        const L = Math.max(2, thLevels(Math.max(1, ...F.map((f) => Math.max(f.low.length, f.high.length)))));
        const i = e ? e.i : -1, left = e ? (m === "c" ? e.left : 0) : 0;
        $(".th-streamwrap").innerHTML = svgStream(nums, i, left, m === "c" ? st.w : 0);
        const pTxt = ltr(`p = ${pct(st.p)}`), name = m === "a" ? "median" : "quantile";
        const ansOf = (f) => (m === "a" ? fmt(f.ans) : num(f.ans));
        const last = F.slice(0, st.s).reverse().find((f) => f.ans !== undefined);   // the answer of the moment, or the last one
        const lineTxt = last ? `${name} = ${ansOf(last)}` : "";
        const o = { label: `שתי הערימות : high למעלה עם הראש למטה, low למטה עם הראש למעלה, ו${m === "a" ? "החציון" : "האחוזון"} על הקו ביניהן`,
          now: e && e.kind !== "leave" ? e.i : undefined, moved: e && e.moved ? e.moved[1] : undefined, dead: e ? e.dead : [],
          nh: e ? (m === "c" ? e.live.high : e.high.length) : 0, nl: e ? (m === "c" ? e.live.low : e.low.length) : 0,
          target: m !== "a" && e ? e.t : undefined, line: lineTxt, hot: e && e.ans !== undefined };
        $(".th-twowrap").innerHTML = e ? svgTwo(e.low, e.high, L, o) : svgTwo([], [], L, o);
        let note = "", tally = "", sum = "", lit = [], lines = { py: [], sv: [] }, vars = "", ans = null;
        const ops = F.slice(0, st.s).reduce((c, f) => c + (f.kind === "push" ? 1 : f.kind === "through" ? 2 : f.moved ? 2 : 0) + (f.pruned ? f.pruned.length : 0), 0);
        if (!e) {
          sum = m === "a" ? `${ltr(n)} ערכים. כל ערך הוא שלושה צעדים${NB}: הדחיפה ל-${ltr("low")}, המעבר ל-${ltr("high")}, והאיזון עם החציון.`
            : m === "b" ? `${ltr(n)} ערכים, ${pTxt}. כל ערך הוא שלושה צעדים${NB}: הדחיפה ל-${ltr("low")}, המעבר ל-${ltr("high")}, וההשלמה ליעד ${ltr("⌈p · n⌉")} עם האחוזון.`
              : `${ltr(n)} ערכים, ${ltr(`W = ${st.w}`)}, ${pTxt}. מהערך ה-${ltr(st.w + 1)} כל ערך הוא ארבעה צעדים${NB}: הישן יוצא, הדחיפה, המעבר, וההשלמה ליעד על החיים.`;
          lines = m === "a" ? { py: [10, 11], sv: [38, 39] } : m === "b" ? { py: [6, 7, 8], sv: [2, 3] } : { py: [10, 11, 12, 13], sv: [2, 3, 4, 5] };
          vars = ltr(m === "c" ? "low = [], high = [], live = {0, 0}" : "low = [], high = []");
        } else {
          const x = e.x, lowS = vals(e.low, true), highS = vals(e.high, false);
          const pv = prev || { low: [], high: [], live: { low: 0, high: 0 } };
          const nl = m === "c" ? e.live.low : e.low.length, nh = m === "c" ? e.live.high : e.high.length;
          const pnl = m === "c" ? pv.live.low : pv.low.length, pnh = m === "c" ? pv.live.high : pv.high.length;
          sum = `הערך ה-${ltr(e.i + 1)}, ${ltr(`x = ${num(x)}`)}. ${ltr("low")}${NB}: ${ltr(lowS)}, ${ltr("high")}${NB}: ${ltr(highS)}` + (m === "c" ? ` (חיים${NB}: ${ltr(`${nl}, ${nh}`)})` : "") + ".";
          const pr = e.pruned && e.pruned.length ? ` קודם נזרק${e.pruned.length > 1 ? "ו" : ""} מהראש ${e.pruned.map(([s2, [v2]]) => `${ltr(num(v2))} מ-${ltr(s2)}`).join(" ו-")}, ${e.pruned.length > 1 ? "שיצאו" : "שיצא"} מהחלון ולא ${e.pruned.length > 1 ? "נספרו" : "נספר"} ממילא.` : "";
          const rb = e.rebuilt && e.rebuilt.length ? ` ב-${e.rebuilt.map(ltr).join(" וב-")} היו יותר מתים מחיים, ולכן ${e.rebuilt.length > 1 ? "הן נבנו" : "היא נבנתה"} מחדש מהחיים בלבד.` : "";
          if (e.kind === "leave") {
            note = `הערך ${ltr(num(e.gone[0]))} (ההגעה ${ltr(e.gone[1])}) יוצא מהחלון. הוא חי ב-${ltr(e.gone_side)}, ולכן החיים שלה יורדים ל-${ltr(e.live[e.gone_side])}. הוא נשאר בערימה, מחוק, עד שיגיע לראש.`;
            lit = [1]; lines = { py: [38, 39], sv: [31] };
          } else if (e.kind === "push") {
            note = `${ltr(num(x))} נדחף ל-${ltr("low")}, ערימת המקסימום${m !== "c" ? " (ב-Python נדחף " + ltr(num(-x)) + ")" : ""}. הערימה מעלה אותו למקומו${e.low[0][1] === e.i ? ", והוא עכשיו הראש שלה" : ""}. הגדלים לא מאוזנים עדיין${NB}: ${ltr(`${nl}, ${nh}`)}.`;
            lit = m === "c" ? [2] : [1]; lines = m === "a" ? { py: [14], sv: [41] } : m === "b" ? { py: [11], sv: [7] } : { py: [35, 36], sv: [29] };
          } else if (e.kind === "through") {
            const stayed = e.moved[1] !== e.i;
            note = `הראש של ${ltr("low")}, ${ltr(num(e.moved[0]))}, עובר ל-${ltr("high")}. ${stayed ? `זה לא ${ltr(num(x))}${NB}: הערך החדש קטן מהראש הישן, ולכן הוא נשאר ב-${ltr("low")} והראש הישן הוא שעובר` : `זה הערך החדש עצמו${NB}: הוא גדול מהראש הישן של ${ltr("low")}, ולכן הוא עלה לראש ועובר הלאה`}. מה שעבר גדול מכל מה שנשאר ב-${ltr("low")}, ולכן הסדר נשמר בלי השוואה בקוד.${pr}`;
            lit = m === "b" ? [1] : [2]; lines = m === "a" ? { py: [15], sv: [42] } : m === "b" ? { py: [12], sv: [8] } : { py: [37, ...(e.pruned.length ? [18, 19] : []), 23, 24, 25, 26, 27, 28, 29, 30], sv: [30, ...(e.pruned.length ? [10] : []), 14, 15, 16, 17] };
          } else if (m === "a") {
            note = e.moved ? `${ltr("high")} גדולה יותר (${ltr(`${pnh} > ${pnl}`)}), ולכן הראש שלה, ${ltr(num(e.moved[0]))}, חוזר ל-${ltr("low")}. ` : `${ltr("high")} לא גדולה מ-${ltr("low")} (${ltr(`${nh} ≤ ${nl}`)}), ושום דבר לא זז. `;
            note += nl > nh ? `מספר אי-זוגי של ערכים, והראש של ${ltr("low")} הוא החציון${NB}: <b>${ltr(fmt(e.ans))}</b>.` : `מספר זוגי של ערכים, והחציון הוא הממוצע של שני הראשים${NB}: ${ltr(`(${num(e.low[0][0])} + ${num(e.high[0][0])}) / 2`)} = <b>${ltr(fmt(e.ans))}</b>.`;
            lit = [3, 4]; lines = { py: [16, ...(e.moved ? [17] : []), 20, ...(nl > nh ? [21] : [22])], sv: [43, ...(nl > nh ? [47] : [48])] };
          } else if (m === "b") {
            const t0 = prev.t;
            note = `${ltr(`n = ${e.i + 1}`)}, והיעד ${ltr(`⌈${pct(st.p)} · ${e.i + 1}⌉ = ${e.t}`)}${e.t === t0 ? ` לא השתנה` : ` עלה ב-1`}. ` +
              (e.moved ? `ל-${ltr("low")} חסר ערך (${ltr(`${pnl} < ${e.t}`)}), ולכן הראש של ${ltr("high")}, ${ltr(num(e.moved[0]))}, חוזר. ` : `ל-${ltr("low")} יש בדיוק ${ltr(e.t)}, ושום דבר לא זז. `) +
              `האחוזון הוא הראש של ${ltr("low")}${NB}: <b>${ltr(num(e.ans))}</b>, הערך במקום ${ltr(e.t)} מבין ${ltr(e.i + 1)}.`;
            lit = [2, 3, 4]; lines = { py: [13, 14, 15, ...(e.moved ? [16] : []), 19], sv: [9, 10, 11, 12, 14] };
          } else {
            const mm = Math.min(e.i + 1, st.w);
            note = `${ltr(`m = ${mm}`)} חיים, והיעד ${ltr(`⌈${pct(st.p)} · ${mm}⌉ = ${e.t}`)}. ` +
              (e.moved ? (pnl < e.t ? `ל-${ltr("low")} חסר חי (${ltr(`${pnl} < ${e.t}`)}), ולכן הראש החי של ${ltr("high")}, ${ltr(num(e.moved[0]))}, עובר אליה. ` : `ל-${ltr("low")} יש חי אחד יותר מדי (${ltr(`${pnl} > ${e.t}`)}), ולכן הראש שלה, ${ltr(num(e.moved[0]))}, עובר ל-${ltr("high")}. `) : `ל-${ltr("low")} יש בדיוק ${ltr(e.t)} חיים, ושום דבר לא זז. `) +
              pr + rb + ` האחוזון הוא הראש החי של ${ltr("low")}${NB}: <b>${ltr(num(e.ans))}</b>, מבין ${ltr(nums.slice(e.left, e.i + 1).map(num).join(" "))}.`;
            lit = [3, ...(e.rebuilt.length ? [4] : []), 5];
            lines = { py: [40, 41, 42, ...(e.moved ? (pnl < e.t ? [43] : [44, 45]) : []), ...(e.rebuilt.length ? [46, 47, 48, 49] : []), 52, 53], sv: [33, 34, 35, 36, ...(e.moved && pnl >= e.t ? [37] : []), ...(e.rebuilt.length ? [19, 22, 23, 24, 25] : []), 40] };
          }
          const sz = m === "c" ? ltr(`live = {${nl}, ${nh}}`) : V("|low|, |high|", `${pnl}, ${pnh}`, `${nl}, ${nh}`);
          vars = [ltr(`x = ${num(x)}`), ltr(`low = ${lowS}`), ltr(`high = ${highS}`), sz, ...(m !== "a" ? [ltr(`target = ${e.t}`)] : [])].join(" · ");
        }
        tally = `פעולות ערימה עד עכשיו${NB}: ${ltr(ops)}, לכל היותר חמש לערך${m === "c" ? " ועוד זריקה אחת לכל ערך שמת" : ""}, כל אחת ${ltr(`O(log ${m === "c" ? "W" : "n"})`)}.` +
          (m === "b" ? ` היעד זז ב-0 או ב-1 בכל ערך, ולכן לכל היותר מעבר אחד חזרה.` : m === "c" ? ` ערימה מחזיקה לכל היותר ${ltr("2 · live + 1")} איברים, כי יותר מתים מחיים גוררים בנייה מחדש.` : "");
        $(".th-sum").innerHTML = sum;
        $(".th-note").innerHTML = note;
        $(".th-tally").innerHTML = tally;
        show({ code: CODE[m], steps: STEPS[m], lit, lines, vars });
        if (done && e) ans = `${m === "a" ? "החציון" : "האחוזון"} ${m === "c" ? "של החלון האחרון" : "של כל הזרם"}${NB}: <b>${ltr(ansOf(e))}</b>.`;
        answer(box, ans, ".th-twowrap .th-ans");
      };
      const total = () => frames().length;
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= total(), restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; $(".th-err").textContent = ""; draw(); };
      $(".th-mode").addEventListener("change", () => { st.mode = MODES[$(".th-mode").value] ? $(".th-mode").value : "a"; restart(); });
      $(".th-nums").addEventListener("change", () => {
        const v = parse($(".th-nums").value);
        if (!v) { $(".th-err").textContent = `הזרם${NB}: 1 עד ${NMAX} מספרים שלמים בין ${VMAX} − ל-${VMAX}`; return; }
        st.nums = v; restart();
      });
      $(".th-nums").addEventListener("keydown", (ev) => { if (ev.key === "Enter") $(".th-nums").blur(); });
      $(".th-p").addEventListener("input", () => { st.p = Number($(".th-p").value); restart(); });
      $(".th-w").addEventListener("change", () => {
        const v = Math.round(Number($(".th-w").value));
        if (!Number.isFinite(v)) { $(".th-w").value = String(st.w); return; }
        st.w = Math.max(1, Math.min(v, WMAX)); restart();
      });
      $(".th-n").addEventListener("change", () => { st.n = Number($(".th-n").value); });
      const seed = seedControls(box, $(".th-anchor"), (rng) => {
        st.nums = Array.from({ length: st.n }, () => Math.floor(rng() * 30) + 1);
        restart();
      }, { fresh: false });
      $(".th-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, { mode: d0.mode, nums: d0.nums.slice(), p: d0.p, w: d0.w, n: 10 }); $(".th-n").value = "10"; restart(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { twoheaps: twoView },
    help: {
      twoheaps: "מקלידים זרם של מספרים שלמים (או מגרילים) ובוחרים מצב. שתי הערימות מצוירות זו מול זו : high למעלה עם הראש שלה למטה, low למטה עם הראש שלה למעלה, והקו ביניהן הוא התשובה. בסעיף א כל ערך הוא שלושה צעדים : הדחיפה ל-low, המעבר של הראש ל-high, והאיזון עם החציון. בסעיף ב מחוון ל-p, והצעד השלישי משלים את low ליעד ⌈p · n⌉. בסעיף ג חלון של W הערכים האחרונים : ערך שיצא מהחלון נשאר בערימה מחוק ואפור עד שהוא נזרק מהראש, והגדלים שמוצגים הם החיים. השורה שמתחת מסבירה כל צעד, והפאנל 'הסבר' מדליק את שורות הקוד.",
    },
    models: { thTraceMedian, thTraceQuantile, thTraceWindow, thRank, thLevels },
  });
})();
