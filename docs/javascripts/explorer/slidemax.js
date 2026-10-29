// kinds: slidemax
//   slidemax               0063        an array of numbers (data-nums) and three modes: a, the monotonic deque of window_max with every pop its own step (the window, the deque under its indices, the outputs filling in); b, longest_within with the two deques hi and lo, the left and right ends and the best window; c, the module win_max cycle by cycle (the stream, the K entries with their ages, the comparisons with x, the keep mask, the slot of x, the entry that ages out, max_out), two steps a cycle
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, explain, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMAX = 24, VMAX = 99, KMAX_HW = 8;
  const num = (v) => String(v).replace("-", "−");

  // Part a event by event, as tools/figures/q0063.py trace_max(): the front index that left
  // the window, every index popped from the back, and the push with the output.
  const smTraceMax = (nums, k) => {
    const ev = [], out = [];
    let q = [];
    nums.forEach((x, i) => {
      if (q.length && q[0] === i - k) { ev.push({ kind: "front", i, idx: q[0], q: q.slice(1), out: out.slice() }); q = q.slice(1); }
      while (q.length && nums[q[q.length - 1]] <= x) { ev.push({ kind: "pop", i, idx: q[q.length - 1], q: q.slice(0, -1), out: out.slice() }); q = q.slice(0, -1); }
      q = [...q, i];
      if (i >= k - 1) out.push(nums[q[0]]);
      ev.push({ kind: "push", i, idx: i, q: q.slice(), out: out.slice() });
    });
    return ev;
  };
  // Part b event by event, as trace_limit(): the pops from the backs of hi and lo, the push
  // into both, every step of the left end; the event that ends a right end's turn is measured.
  const smTraceLimit = (nums, limit) => {
    const ev = [], hi = [], lo = [];
    let left = 0, best = 0, win = null;
    const rec = (kind, right, idx, measured = false, gone = []) =>
      ev.push({ kind, right, idx, hi: hi.slice(), lo: lo.slice(), left, best, win: win ? win.slice() : null, measured, gone });
    nums.forEach((x, right) => {
      while (hi.length && nums[hi[hi.length - 1]] <= x) rec("hipop", right, hi.pop());
      while (lo.length && nums[lo[lo.length - 1]] >= x) rec("lopop", right, lo.pop());
      hi.push(right); lo.push(right);
      if (nums[hi[0]] - nums[lo[0]] <= limit) {
        if (right - left + 1 > best) { best = right - left + 1; win = [left, right]; }
        rec("enter", right, right, true);
        return;
      }
      rec("enter", right, right);
      while (nums[hi[0]] - nums[lo[0]] > limit) {
        const gone = [];
        if (hi[0] === left) { gone.push("hi"); hi.shift(); }
        if (lo[0] === left) { gone.push("lo"); lo.shift(); }
        left++;
        const ok = nums[hi[0]] - nums[lo[0]] <= limit;
        if (ok && right - left + 1 > best) { best = right - left + 1; win = [left, right]; }
        rec("left", right, left - 1, ok, gone);
      }
    });
    return ev;
  };
  // Part c cycle by cycle, as hw_trace(): the mask keep[j] = valid and val[j] > x, the slot p
  // of x (its first zero), the front that ages out, the entries before and after the edge.
  const smTraceHw = (stream, k) => {
    let val = Array(k).fill(0), age = Array(k).fill(0), vld = Array(k).fill(false);
    return stream.map((x, t) => {
      const keep = val.map((v, j) => vld[j] && v > x);
      const p = keep.indexOf(false) < 0 ? k : keep.indexOf(false);
      let nval = [], nage = [];
      for (let j = 0; j <= p; j++) { nval.push(j < p ? val[j] : x); nage.push(j < p ? age[j] + 1 : 0); }
      const drop = nage[0] === k;
      if (drop) { nval = nval.slice(1); nage = nage.slice(1); }
      const before = val.map((v, j) => [v, age[j]]).filter((_, j) => vld[j]);
      val = nval.concat(Array(k - nval.length).fill(0));
      age = nage.concat(Array(k - nage.length).fill(0));
      vld = val.map((_, j) => j < nval.length);
      return { t, x, before, keep, p, drop, dropped: drop ? before[0] : null, after: val.map((v, j) => [v, age[j]]).filter((_, j) => vld[j]), out: val[0] };
    });
  };

  const parse = (text) => {
    const toks = String(text).trim().replace(/−/g, "-").split(/[\s,;]+/).filter(Boolean);
    if (!toks.length || toks.length > NMAX || !toks.every((t) => /^-?\d+$/.test(t))) return null;
    const v = toks.map(Number);
    return v.every((x) => Math.abs(x) <= VMAX) ? v : null;
  };

  const MODES = { a: "המקסימום של כל חלון (סעיף א)", b: "max − min ≤ limit (סעיף ב)", c: "המודול, מחזור אחרי מחזור (סעיף ג)" };
  const STEPS = {
    a: ["הראש יצא מהחלון", "מנקים את הזנב", "מכניסים", "הפלט"],
    b: ["הקצה הימני מתקדם", "החלון לא חוקי : השמאלי מתקדם", "הטוב עד עכשיו", "הסוף : הטוב הוא התשובה"],
    c: ["השוואה", "המקום של x", "המצב הבא", "יציאה לפי גיל", "המוצא"],
  };
  const CODE = { a: "window_max", b: "longest_within", c: "win_max" };
  const V = (name, before, after) => ltr(before === after ? `${name} = ${after}` : `${name} : ${before} → ${after}`);
  const list = (nums, idx) => `[${idx.map((j) => num(nums[j])).join(", ")}]`;

  // --- drawing ------------------------------------------------------------------------
  const CELL = 36, LW = 80;
  const open = (W, H, label) => `<svg class="figure sm-fig sm-live" viewBox="0 0 ${W} ${H}" style="min-width:${Math.round(W * 0.72)}px;max-width:${Math.round(W * 1.15)}px" role="img" aria-label="${label}">`;
  const cx = (p) => LW + p * CELL + CELL / 2;
  const cell = (p, y, h, v, cls, title) => `<g class="sm-cell ${cls}"><title>${title}</title><rect x="${LW + p * CELL + 3}" y="${y}" width="${CELL - 6}" height="${h}" rx="4"/>` +
    `<text x="${cx(p)}" y="${y + h / 2 + 5}" text-anchor="middle">${num(v)}</text></g>`;
  const strike = (p, y, h) => `<line class="sm-strike" x1="${LW + p * CELL + 6}" y1="${y + h - 3}" x2="${LW + p * CELL + CELL - 6}" y2="${y + 3}"/>`;
  const label = (y, text) => `<text class="sm-lab" x="${LW - 8}" y="${y}" text-anchor="end">${text}</text>`;
  const ticks = (n, y) => Array.from({ length: n }, (_, p) => `<text class="tick" x="${cx(p)}" y="${y}" text-anchor="middle">${p}</text>`).join("");
  const frame = (a, b, y, h, cls) => `<rect class="${cls}" x="${LW + a * CELL + 1}" y="${y}" width="${(b - a + 1) * CELL - 2}" height="${h}" rx="5"/>`;

  // mode a: the array with the window, the deque under its indices, the outputs under the
  // index that closes each window
  const svgA = (nums, k, e) => {
    const n = nums.length, W = LW + n * CELL + 8, H = 166;
    let s = open(W, H, `המערך, החלון של ${k} הערכים האחרונים, ה-deque מתחת למקומות שלו והמקסימום של כל חלון`);
    s += ticks(n, 14) + label(42, "nums") + label(92, "deque") + label(146, "max");
    const i = e ? e.i : -1;
    if (e) s += frame(Math.max(0, i - k + 1), i, 21, 34, "sm-win");
    nums.forEach((v, p) => { s += cell(p, 24, 28, v, p === i ? "is-cur" : p > i ? "is-wait" : "is-off", `place ${p}, value ${v}`); });
    if (e) {
      e.q.forEach((p, m) => { s += cell(p, 74, 28, nums[p], m === 0 ? "is-front" : "is-in", `in the deque: place ${p}, value ${nums[p]}`); });
      if (e.kind !== "push") s += cell(e.idx, 74, 28, nums[e.idx], "is-pop", `left the deque: place ${e.idx}`) + strike(e.idx, 74, 28);
      if (e.q.length) s += `<text class="tick" x="${cx(e.q[0])}" y="116" text-anchor="middle">front</text>`;
      if (e.q.length > 1) s += `<text class="tick" x="${cx(e.q[e.q.length - 1])}" y="116" text-anchor="middle">back</text>`;
      e.out.forEach((v, j) => {
        const p = j + k - 1, now = e.kind === "push" && p === i;
        s += `<text class="sm-out is-val${now ? " is-now" : ""}" x="${cx(p)}" y="146" text-anchor="middle">${num(v)}</text>`;
      });
    }
    return s + "</svg>";
  };

  // mode b: the array with the window [left, right] and the best window, hi and lo under
  // their indices, the two ends as markers
  const svgB = (nums, e) => {
    const n = nums.length, W = LW + n * CELL + 8, H = 196;
    let s = open(W, H, "המערך עם החלון בין הקצה השמאלי לימני, החלון הטוב ביותר, ושני ה-deques : hi למקסימום ו-lo למינימום");
    s += ticks(n, 14) + label(42, "nums") + label(92, "hi (max)") + label(136, "lo (min)") + label(178, "ends");
    const R = e ? e.right : -1, L = e ? e.left : 0;
    if (e && e.win) s += frame(e.win[0], e.win[1], 18, 40, "sm-best");
    if (e) s += frame(L, R, 21, 34, "sm-win");
    nums.forEach((v, p) => { s += cell(p, 24, 28, v, p === R ? "is-cur" : p > R ? "is-wait" : p < L ? "is-gone" : "is-off", `place ${p}, value ${v}`); });
    if (e) {
      const row = (q, y, name) => q.map((p, m) => cell(p, y, 28, nums[p], m === 0 ? "is-front" : "is-in", `${name}: place ${p}, value ${nums[p]}`)).join("");
      s += row(e.hi, 74, "hi") + row(e.lo, 118, "lo");
      if (e.kind === "hipop") s += cell(e.idx, 74, 28, nums[e.idx], "is-pop", `left hi: place ${e.idx}`) + strike(e.idx, 74, 28);
      if (e.kind === "lopop") s += cell(e.idx, 118, 28, nums[e.idx], "is-pop", `left lo: place ${e.idx}`) + strike(e.idx, 118, 28);
      if (e.kind === "left") {
        if (e.gone.includes("hi")) s += cell(e.idx, 74, 28, nums[e.idx], "is-pop", `left hi from the front: place ${e.idx}`) + strike(e.idx, 74, 28);
        if (e.gone.includes("lo")) s += cell(e.idx, 118, 28, nums[e.idx], "is-pop", `left lo from the front: place ${e.idx}`) + strike(e.idx, 118, 28);
      }
      const mark = (p, t, dy) => `<path class="sm-ptr" d="M${cx(p) - 6},${168 + dy} L${cx(p) + 6},${168 + dy} L${cx(p)},${160 + dy} Z"/><text class="sm-lab" x="${cx(p)}" y="${184 + dy}" text-anchor="middle">${t}</text>`;
      s += L === R ? mark(L, "L R", 0) : mark(L, "L", 0) + mark(R, "R", 0);
    }
    return s + "</svg>";
  };

  // mode c: the stream with the window of the last K samples, the K entries (and the spare
  // slot when x goes there), the comparisons with x, the mask, the slot of x and max_out
  const svgC = (stream, k, row, phase) => {
    const n = stream.length, SL = 66, sx = (j) => LW + j * SL + SL / 2;
    const W = Math.max(LW + n * CELL, LW + (k + 1) * SL) + 8, H = 256;
    let s = open(W, H, `הזרם עם K = ${k} הדגימות האחרונות, ${k} הכניסות עם הגילים, ההשוואות עם x, המסכה keep והמוצא`);
    s += ticks(n, 14) + label(42, "x(t)") + label(104, "entries") + label(160, "val > x") + label(196, "keep") + label(244, "max_out");
    const t = row ? row.t : -1;
    if (row) s += frame(Math.max(0, t - k + 1), t, 21, 34, "sm-win");
    stream.forEach((v, p) => { s += cell(p, 24, 28, v, p === t ? "is-cur" : p > t ? "is-wait" : "is-off", `cycle ${p}, sample ${v}`); });
    const ents = !row ? [] : phase === "cmp" ? row.before : row.after;
    const slot = (j, cls, v, a, title) => `<g class="sm-slot ${cls}"><title>${title}</title><rect x="${LW + j * SL + 4}" y="78" width="${SL - 8}" height="44" rx="5"/>` +
      (v === null ? "" : `<text class="sm-sv" x="${sx(j)}" y="100" text-anchor="middle">${num(v)}</text><text class="tick" x="${sx(j)}" y="116" text-anchor="middle">age ${a}</text>`) + "</g>";
    for (let j = 0; j < k; j++) {
      const e = ents[j];
      const cls = !e ? "is-empty" : phase === "cmp" && row.keep[j] === false && j >= row.p ? "is-cut" : phase === "clk" && j === 0 ? "is-front" : "is-in";
      s += slot(j, cls + (phase === "cmp" && row.drop && j === 0 ? " is-age" : ""), e ? e[0] : null, e ? e[1] : 0, e ? `entry ${j}: value ${e[0]}, age ${e[1]}` : `entry ${j}: not valid`);
      if (e && cls === "is-cut") s += `<line class="sm-strike" x1="${LW + j * SL + 10}" y1="118" x2="${LW + j * SL + SL - 10}" y2="82"/>`;
    }
    if (row && phase === "cmp") {
      if (row.p === k) s += slot(k, "is-spare", row.x, 0, `the spare slot: x = ${row.x}`);
      for (let j = 0; j < k; j++) {
        const e = row.before[j];
        s += `<text class="sm-cmp${e ? "" : " is-dim"}" x="${sx(j)}" y="164" text-anchor="middle">${e ? `${num(e[0])} &gt; ${num(row.x)}` : "invalid"}</text>`;
        s += `<g class="sm-bit ${row.keep[j] ? "is-one" : "is-zero"}${j === row.p ? " is-edge" : ""}"><rect x="${sx(j) - 13}" y="178" width="26" height="26" rx="4"/><text x="${sx(j)}" y="196" text-anchor="middle">${row.keep[j] ? 1 : 0}</text></g>`;
      }
      s += `<text class="sm-lab sm-xto" x="${sx(row.p)}" y="222" text-anchor="middle">x = ${num(row.x)} → slot ${row.p}</text>`;
      if (row.drop) s += `<text class="sm-lab sm-ageout" x="${sx(0)}" y="72" text-anchor="middle">age → ${k}: out</text>`;
    }
    if (row && phase === "clk") s += `<text class="sm-out is-val is-now" x="${LW + 8}" y="244">${num(row.out)}</text>`;
    return s + "</svg>";
  };

  const slideView = () => ({
    mount(box) {
      const mode0 = MODES[box.dataset.mode] ? box.dataset.mode : "a";
      const d0 = { mode: mode0, nums: parse(box.dataset.nums || "1 3 -1 -3 5 3 6 7") || [1, 3, -1, -3, 5, 3, 6, 7], k: Number(box.dataset.k) || 3, limit: Number(box.dataset.limit) || 0 };
      const st = { mode: d0.mode, nums: d0.nums.slice(), k: d0.k, limit: d0.limit, s: 0, n: 8 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המצב <select class="sm-mode" aria-label="איזה סעיף">${Object.entries(MODES).map(([v, w]) => `<option value="${v}">${w}</option>`).join("")}</select></label>` +
        `<label><span>המערך</span><input type="text" class="ex-num sm-nums" dir="ltr" spellcheck="false" aria-label="המערך : עד ${NMAX} מספרים שלמים, מופרדים ברווח"></label>` +
        `<label class="sm-klab"><span class="sm-kname">k</span> <input type="number" class="ex-num sm-k" min="1" max="${NMAX}" step="1" dir="ltr" aria-label="גודל החלון"></label>` +
        `<label class="sm-llab"><span>limit</span> <input type="number" class="ex-num sm-limit" min="0" max="${2 * VMAX}" step="1" dir="ltr" aria-label="ההפרש המותר בין המקסימום למינימום"></label>` +
        `<label>בהגרלה <select class="sm-n" aria-label="כמה מספרים להגריל">${[8, 12, 16, 24].map((v) => `<option value="${v}"${v === 8 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button sm-rand">הגרלה</button><span class="sm-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err sm-err" role="status"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary sm-sum" aria-live="polite"></p>` +
        `<div class="sm-wrap" data-fig-strip></div>` +
        `<span class="viz-legend"><span><i class="sm-key-win"></i>החלון</span><span class="sm-only-b"><i class="sm-key-best"></i>החלון הטוב ביותר עד עכשיו</span>` +
        `<span class="sm-not-c"><i class="sm-key-in"></i>ב-deque</span><span class="sm-only-c"><i class="sm-key-in"></i>כניסה בשימוש</span><span><i class="sm-key-front"></i>הראש, המקסימום</span>` +
        `<span><i class="sm-key-pop"></i>יוצא בצעד הזה</span><span><i class="sm-key-cur"></i>הערך החדש</span></span>` +
        `<p class="sm-note"></p><p class="sm-tally"></p>`;
      const show = explain(box, "הסבר : השלבים של הפתרון והקוד");
      answer(box, NB); answer(box, null);           // the answer line keeps its place from the first step
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      // the frames of the mode: the events of a and b, two frames per cycle in c
      const frames = () => {
        if (st.mode === "a") return smTraceMax(st.nums, st.k);
        if (st.mode === "b") return smTraceLimit(st.nums, st.limit);
        const F = [];
        smTraceHw(st.nums, st.k).forEach((r) => { F.push({ row: r, phase: "cmp" }); F.push({ row: r, phase: "clk" }); });
        return F;
      };
      const draw = () => {
        const F = frames(), N = F.length, nums = st.nums, n = nums.length, m = st.mode;
        st.s = Math.min(Math.max(st.s, 0), N);
        const e = st.s ? F[st.s - 1] : null, done = st.s === N, prev = st.s > 1 ? F[st.s - 2] : null;
        $(".sm-mode").value = m; $(".sm-nums").value = nums.join(" "); $(".sm-k").value = String(st.k); $(".sm-limit").value = String(st.limit);
        $(".sm-kname").textContent = m === "c" ? "K" : "k";
        $(".sm-klab").hidden = m === "b"; $(".sm-llab").hidden = m !== "b";
        box.classList.toggle("sm-is-b", m === "b"); box.classList.toggle("sm-is-c", m === "c");
        $(".ex-pos").textContent = `צעד ${st.s} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        let note = "", tally = "", sum = "", lit = [], lines = { py: [], sv: [] }, vars = "", ans = null, marks = [];
        if (m === "a") {
          $(".sm-wrap").innerHTML = svgA(nums, st.k, e);
          const pops = F.slice(0, st.s).filter((x) => x.kind !== "push").length, pushes = st.s - pops;
          sum = e ? `הצעד של ${ltr(`i = ${e.i}`)} (הערך ${ltr(num(nums[e.i]))}). ה-deque${NB}: ${ltr(list(nums, e.q))}.`
            : `${ltr(n)} ערכים, ${ltr(`k = ${st.k}`)}, ${ltr(n - st.k + 1)} חלונות. כל צעד הוא פעולה אחת על ה-deque.`;
          if (e) {
            const x = nums[e.i], v = nums[e.idx];
            if (e.kind === "front") note = `המקום ${ltr(e.idx)} בראש, וזה ${ltr(`${e.i} − ${st.k}`)}${NB}: החלון שנגמר ב-${ltr(e.i)} מתחיל ב-${ltr(e.i - st.k + 1)}, ולכן המקום ${ltr(e.idx)} (הערך ${ltr(num(v))}) כבר בחוץ ויוצא מהראש.`;
            else if (e.kind === "pop") note = `נכנס ${ltr(num(x))} במקום ${ltr(e.i)}. בזנב המקום ${ltr(e.idx)} עם ${ltr(`${num(v)} ≤ ${num(x)}`)}${NB}: מעכשיו כל חלון שמכיל אותו מכיל גם את ${ltr(num(x))}, ולכן הוא לא יהיה מקסימום יותר. יוצא מהזנב.`;
            else {
              const tail = e.q.length > 1 ? e.q[e.q.length - 2] : null;
              note = `${tail === null ? "ה-deque ריק" : `בזנב ${ltr(`${num(nums[tail])} > ${num(x)}`)}`}, ולכן הניקוי נעצר, ו-${ltr(e.i)} נכנס לזנב. ` +
                (e.i >= st.k - 1 ? `החלון ${ltr(`${e.i - st.k + 1}..${e.i}`)} מלא, והראש, הערך <b>${ltr(num(nums[e.q[0]]))}</b>, הוא המקסימום שלו.` : `החלון עוד לא מלא (צריך ${ltr(st.k)} ערכים), ואין פלט.`);
            }
          }
          tally = `פעולות על ה-deque עד עכשיו${NB}: ${ltr(pushes)} הכנסות ו-${ltr(pops)} הוצאות. בכל הריצה לכל היותר ${ltr(`2n = ${2 * n}`)}, כי כל מקום נכנס פעם אחת ויוצא לכל היותר פעם אחת.`;
          if (!e) { lines = { py: [7, 8], sv: [4, 5] }; vars = ltr("q = [], out = []"); }
          else {
            lit = e.kind === "front" ? [1] : e.kind === "pop" ? [2] : [3, ...(e.i >= st.k - 1 ? [4] : [])];
            lines = e.kind === "front" ? { py: [10, 11], sv: [7] } : e.kind === "pop" ? { py: [12, 13], sv: [8] }
              : { py: [14, 15, ...(e.i >= st.k - 1 ? [16] : []), ...(done ? [17] : [])], sv: [9, 10] };
            const qb = prev ? prev.q : [];                                   // the deque before this event
            vars = [ltr(`i = ${e.i}`), ltr(`x = ${num(nums[e.i])}`), V("q", `[${qb.join(", ")}]`, `[${e.q.join(", ")}]`), ltr(`out = [${e.out.map(num).join(", ")}]`)].join(" · ");
          }
          if (done && e) { ans = `המקסימום של כל חלון${NB}: ${ltr(e.out.map(num).join(" "))}.`; marks = ".sm-wrap .sm-out"; }
        } else if (m === "b") {
          $(".sm-wrap").innerHTML = svgB(nums, e);
          const lim = st.limit;
          sum = e ? `החלון ${ltr(`${e.left}..${e.right}`)}, המקסימום ${ltr(num(nums[e.hi[0]]))} והמינימום ${ltr(num(nums[e.lo[0]]))}. הטוב עד עכשיו${NB}: <b>${ltr(e.best)}</b>.`
            : `${ltr(n)} ערכים, ${ltr(`limit = ${lim}`)}. כל צעד הוא פעולה אחת על deque או על הקצה השמאלי.`;
          if (e) {
            const x = nums[e.right], v = e.idx === null ? 0 : nums[e.idx], mx = nums[e.hi[0]], mn = nums[e.lo[0]], d = mx - mn, len = e.right - e.left + 1;
            const fresh = e.measured && e.best === len && (!prev || prev.best < e.best) ? ` <b>אורך חדש${NB}: ${ltr(len)} ✓</b>` : "";
            if (e.kind === "hipop") note = `נכנס ${ltr(num(x))} במקום ${ltr(e.right)}. ב-${ltr("hi")} הזנב הוא המקום ${ltr(e.idx)} עם ${ltr(`${num(v)} ≤ ${num(x)}`)}${NB}: הוא לא יהיה מקסימום יותר, ויוצא.`;
            else if (e.kind === "lopop") note = `ב-${ltr("lo")} הזנב הוא המקום ${ltr(e.idx)} עם ${ltr(`${num(v)} ≥ ${num(x)}`)}${NB}: הוא לא יהיה מינימום יותר, ויוצא.`;
            else if (e.kind === "enter") note = `${ltr(e.right)} נכנס לזנב של ${ltr("hi")} ושל ${ltr("lo")}. המקסימום פחות המינימום${NB}: ${ltr(`${num(mx)} − ${num(mn)} = ${d}`)}` +
              (d > lim ? `, יותר מ-${ltr(`limit = ${lim}`)}. החלון ${ltr(`${e.left}..${e.right}`)} לא חוקי, והקצה השמאלי מתחיל לזוז.` : `, לכל היותר ${ltr(lim)}. החלון ${ltr(`${e.left}..${e.right}`)} חוקי, באורך ${ltr(len)}.${fresh}`);
            else note = `הקצה השמאלי זז מ-${ltr(e.idx)} ל-${ltr(e.left)}` + (e.gone.length ? `, והמקום ${ltr(e.idx)} יוצא מהראש של ${e.gone.map((g) => ltr(g)).join(" ושל ")}` : `, והמקום ${ltr(e.idx)} לא בראש של אף deque`) +
              `. עכשיו ${ltr(`${num(mx)} − ${num(mn)} = ${d}`)}` + (e.measured ? `, והחלון ${ltr(`${e.left}..${e.right}`)} חוקי, באורך ${ltr(len)}.${fresh}` : `, עדיין יותר מ-${ltr(lim)}.`);
          }
          const moves = e ? e.left : 0;
          tally = `הקצה השמאלי זז ${moves === 1 ? "פעם אחת" : `${ltr(moves)} פעמים`} בסך הכול, לכל היותר ${ltr(`n = ${n}`)}${NB}: הוא רק מתקדם, כי חלון לא חוקי נשאר לא חוקי כשמאריכים אותו.`;
          if (!e) { lines = { py: [7, 8, 9], sv: [4] }; vars = ltr("hi = [], lo = [], left = 0, best = 0"); }
          else {
            const meas = e.measured ? { py: [23], sv: [15] } : { py: [], sv: [] }, fin = done ? { py: [24], sv: [17] } : { py: [], sv: [] };
            const body = { hipop: { py: [11, 12], sv: [6] }, lopop: { py: [13, 14], sv: [7] }, enter: { py: [15, 16, 17], sv: [8, 9, 10] }, left: { py: [17, 18, 19, 20, 21, 22], sv: [10, 11, 12, 13] } }[e.kind];
            lit = [...(e.kind === "left" ? [2] : [1]), ...(e.measured ? [3] : []), ...(done ? [4] : [])];
            lines = { py: [...body.py, ...meas.py, ...fin.py], sv: [...body.sv, ...meas.sv, ...fin.sv] };
            vars = [ltr(`right = ${e.right}`), V("left", prev ? prev.left : 0, e.left), ltr(`hi = [${e.hi.join(", ")}]`), ltr(`lo = [${e.lo.join(", ")}]`), V("best", prev ? prev.best : 0, e.best)].join(" · ");
          }
          if (done && e) { ans = e.best ? `הקטע הארוך ביותר עם ${ltr(`max − min ≤ ${lim}`)} הוא באורך ${ltr(e.best)}${NB}: המקומות ${ltr(e.win[0])} עד ${ltr(e.win[1])}.` : "המערך ריק."; marks = ".sm-wrap .sm-best"; }
        } else {
          const K = st.k, row = e ? e.row : null, ph = e ? e.phase : null;
          $(".sm-wrap").innerHTML = svgC(nums, K, row, ph);
          sum = row ? `מחזור ${ltr(row.t)}, ${ltr(`x = ${num(row.x)}`)}${NB}: ${ph === "clk" ? `עליית השעון, ${ltr(`max_out = ${num(row.out)}`)}` : "ההשוואות"}.`
            : `${ltr(n)} דגימות, ${ltr(`K = ${K}`)}. בכל מחזור שני צעדים${NB}: ההשוואות, ואז עליית השעון.`;
          if (row) {
            const cut = row.before.slice(row.p).map((x) => num(x[0]));
            if (ph === "cmp") {
              const bits = row.keep.map((b) => (b ? 1 : 0)).join("");
              note = `מחזור ${ltr(row.t)}, הדגימה ${ltr(num(row.x))} נכנסת. ${ltr(K)} המשווים בבת אחת נותנים ${ltr(`keep = ${bits}`)}${NB}: ` +
                (row.p === 0 ? "אף כניסה לא גדולה מ-x" : `${row.p === 1 ? "הכניסה 0 גדולה" : `הכניסות ${ltr(`0..${row.p - 1}`)} גדולות`} מ-x`) +
                (row.p < K ? `, והאפס הראשון במקום ${ltr(row.p)}. לשם נכתבת x` : `, כולן. x נכתבת למקום הנוסף ${ltr(K)}`) +
                (cut.length ? `, והכניסות שאחריה מתבטלות (${ltr(cut.join(", "))}), כמו ההוצאות מהזנב בסעיף א.` : ".") +
                (row.drop ? ` הראש, ${ltr(num(row.dropped[0]))}, מגיע לגיל ${ltr(K)}${NB}: הוא כבר מחוץ לחלון, ויוצא, וכל הכניסות זזות מקום אחד לראש.` : "");
            } else {
              note = `עליית השעון${NB}: הכניסות עכשיו ${ltr(row.after.map(([v, a]) => `${num(v)}(${a})`).join(" "))}, ערך עם הגיל שלו. ` +
                `${ltr(`max_out = val[0] = ${num(row.out)}`)}, המקסימום של ${ltr(nums.slice(Math.max(0, row.t - K + 1), row.t + 1).map(num).join(" "))}.`;
            }
          }
          const done2 = F.slice(0, st.s).filter((x) => x.phase === "clk").length;
          tally = `בכל מחזור אותה עבודה${NB}: ${ltr(K)} השוואות, מקודד עדיפות ומרבבים, בלי קשר לכמה כניסות מתבטלות. מחזורים שהסתיימו${NB}: ${ltr(done2)}.`;
          if (!row) { lines = { py: [5, 6, 7], sv: [38, 39, 40] }; vars = ltr(`slots = ${K} × (0, 0, False)`); }
          else if (ph === "cmp") {
            lit = [1, 2, 3, ...(row.drop ? [4] : [])];
            lines = { py: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], sv: [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35] };
            vars = [ltr(`x = ${num(row.x)}`), ltr(`keep = ${row.keep.map((b) => (b ? 1 : 0)).join("")}`), ltr(`p = ${row.p}`), ltr(`drop = ${row.drop ? 1 : 0}`)].join(" · ");
          } else {
            lit = [...(row.drop ? [4] : []), 5];
            lines = { py: [23, 24], sv: [42, 43, 44, 45, 48] };
            vars = [ltr(`x = ${num(row.x)}`), ltr(`val = [${row.after.map((x) => num(x[0])).join(", ")}]`), ltr(`age = [${row.after.map((x) => x[1]).join(", ")}]`), ltr(`max_out = ${num(row.out)}`)].join(" · ");
          }
          if (done && row) { ans = `${ltr("max_out")} בכל מחזור${NB}: ${ltr(smTraceHw(nums, K).map((r) => num(r.out)).join(" "))}.`; marks = ".sm-wrap .sm-out"; }
        }
        $(".sm-sum").innerHTML = sum;
        $(".sm-note").innerHTML = note;
        $(".sm-tally").innerHTML = tally;
        show({ code: CODE[m], steps: STEPS[m], lit, lines, vars });
        answer(box, ans, marks);
      };
      const total = () => frames().length;
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= total(), restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; $(".sm-err").textContent = ""; draw(); };
      const fitK = () => { st.k = Math.max(1, Math.min(st.k, st.mode === "c" ? KMAX_HW : st.nums.length)); };
      $(".sm-mode").addEventListener("change", () => { st.mode = MODES[$(".sm-mode").value] ? $(".sm-mode").value : "a"; fitK(); restart(); });
      $(".sm-nums").addEventListener("change", () => {
        const v = parse($(".sm-nums").value);
        if (!v) { $(".sm-err").textContent = `המערך${NB}: 1 עד ${NMAX} מספרים שלמים בין ${VMAX} − ל-${VMAX}`; return; }
        st.nums = v; fitK(); restart();
      });
      $(".sm-nums").addEventListener("keydown", (ev) => { if (ev.key === "Enter") $(".sm-nums").blur(); });
      $(".sm-k").addEventListener("change", () => {
        const v = Math.round(Number($(".sm-k").value)), top = st.mode === "c" ? KMAX_HW : st.nums.length;
        if (!Number.isFinite(v)) { $(".sm-k").value = String(st.k); return; }
        st.k = Math.max(1, Math.min(v, top)); restart();                    // k fits the array (K up to 8 in the module)
      });
      $(".sm-limit").addEventListener("change", () => {
        const v = Math.round(Number($(".sm-limit").value));
        if (!(v >= 0 && v <= 2 * VMAX)) { $(".sm-limit").value = String(st.limit); return; }
        st.limit = v; restart();
      });
      $(".sm-n").addEventListener("change", () => { st.n = Number($(".sm-n").value); });
      const seed = seedControls(box, $(".sm-anchor"), (rng) => {
        st.nums = Array.from({ length: st.n }, () => (st.mode === "c" ? Math.floor(rng() * 16) : Math.floor(rng() * 19) - 9));
        fitK(); restart();
      }, { fresh: false });
      $(".sm-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, { mode: d0.mode, nums: d0.nums.slice(), k: d0.k, limit: d0.limit, n: 8 }); $(".sm-n").value = "8"; restart(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { slidemax: slideView },
    help: {
      slidemax: "מקלידים מערך של מספרים שלמים (או מגרילים) ובוחרים מצב. בסעיף א כל צעד הוא פעולה אחת על ה-deque : הוצאה מהראש כשהמקום יצא מהחלון, הוצאה מהזנב של ערך שאינו גדול מהחדש, או הכנסה עם הפלט. ה-deque מצויר מתחת למקומות שלו, הראש מודגש והיוצא מחוק. בסעיף ב שני deques, hi למקסימום ו-lo למינימום, והקצוות L ו-R : השמאלי מתקדם כל עוד ההפרש גדול מ-limit. בסעיף ג המודול, שני צעדים בכל מחזור : ההשוואות של הכניסות עם x, המסכה keep והמקום של x, ואז עליית השעון עם הכניסות החדשות ו-max_out. השורה שמתחת מסבירה כל צעד, והפאנל 'הסבר' מדליק את שורות הקוד.",
    },
    models: { smTraceMax, smTraceLimit, smTraceHw },
  });
})();
