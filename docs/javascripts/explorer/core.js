// Interactive explorers, the shared core: a box `<div class="explorer" data-kind="..."
// data-...>` mounts the controls, a summary line and figures of its kind, redrawn on every
// change. This file holds what every kind uses (the seeded generator, the drawing helpers,
// the shared controls, the timing strip, the box header, keyboard stepping, lazy building)
// and the registry; each kind lives in explorer/<kind>.js, whose first line names the
// kinds it registers. hooks/questions.py adds this file and the files of the kinds on a
// page as script tags to that page only. Under Node, tools/explorer_node.js loads every
// file and returns the merged models, which the question tests (tests/0001 to 0043)
// compare with the Python reference.
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

  const bigComb = (n, k) => {
    if (k < 0 || k > n) return 0n;
    let r = 1n;
    for (let i = 1; i <= k; i++) r = (r * BigInt(n - k + i)) / BigInt(i);
    return r;
  };
  // Degrees on the unit circle (0007, the triangle and the polygon).
  const TRI_M = 360;
  const triNorm = (v) => ((Math.round(v) % TRI_M) + TRI_M) % TRI_M;
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

  // The digits of a base up to 16 (kapbase, kap4base); a value as a bit string (lfsr, gray).
  const KB_DIGITS = "0123456789ABCDEF";
  const bitsOf = (v, bits) => v.toString(2).padStart(bits, "0");
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

  // --- drawing helpers ---------------------------------------------------------------

  const f = (v, n = 1) => Number(v).toFixed(n);
  const attr = (s) => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  // math and numbers inside Hebrew text; a short one (a number, a coordinate, a short
  // formula) never breaks across lines, where its parts would read in the wrong order
  const LTR_KEEP = 24;
  const ltr = (x) => {
    const plain = String(x).replace(/<[^>]*>/g, "").replace(/&[a-z#0-9]+;/gi, "x");
    return `<bdi dir="ltr"${plain.length <= LTR_KEEP ? ' class="ex-nw"' : ""}>${x}</bdi>`;
  };
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

  const hline = (fr, v, label) =>
    `<line class="ink-line" x1="${X0}" x2="${W - RIGHT}" y1="${f(fr.Y(v))}" y2="${f(fr.Y(v))}" ` +
    `stroke-width="1.5" stroke-dasharray="6 4"/>` +
    (label ? `<text class="legend" x="${X0 + 6}" y="${f(fr.Y(v) - 6)}">${label}</text>` : "");

  // --- shared controls ---------------------------------------------------------------------

  // A speed select (milliseconds per step) and the play loop of a stepper: the play
  // button toggles a timer that calls step() every speed.value ms until done(); pressed
  // at the end, restart() rewinds first. Returns stop(), for the other controls.
  // The seed of a box's random draws: a seed field inserted after `after`; run(rng, seed)
  // redraws with a seeded generator. draw() picks a new seed and runs it, a typed seed
  // replays, and `#seed-<kind>-<n>` in the URL replays on load (the first box of that kind
  // on the page). opts.seed fills the field without running. opts.state = { get, set }:
  // get() returns the box's own state as a payload (or null to fall back to the controls),
  // the link button of the header then writes `#state-<kind>.<payload>`, and set() reopens
  // it on load (true when the payload was valid). The field and the codec are kept on the
  // box for the link and the remembered state (see "links" below), and draw() for "reset
  // everything", which draws a new example unless opts.fresh is false (a box whose draws
  // add up, as the Monte Carlo counts).
  const SEED_HASH = /^#seed-([a-z0-9-]+)-(\d+)$/;
  const STATE_HASH = /^#state-([a-z0-9-]+)\.(.+)$/;
  let tick = 0;                      // orders a box's last seeded draw against its last control change
  const seedControls = (box, after, run, opts = {}) => {
    const kind = box.dataset.kind;
    const label = document.createElement("label");
    label.className = "ex-seedlab";
    label.innerHTML = `<span>ערך אתחול</span> <input type="number" class="ex-seed" min="1" max="${SEED_MAX}" step="1" dir="ltr" inputmode="numeric" aria-label="ערך האתחול של ההגרלה, מספר לשחזור">`;
    after.after(label);
    const input = label.querySelector("input");
    if (opts.seed) input.value = opts.seed;
    const runSeed = (seed) => { input.value = seed; box.dvqSeedAt = ++tick; run(mulberry32(seed), seed); };
    const draw = () => runSeed(newSeed());
    box.dvqSeed = { input, runSeed, draw: opts.fresh === false ? null : draw };
    box.dvqState = opts.state || null;
    input.addEventListener("change", () => { const v = Math.round(Number(input.value)); if (v >= 1 && v <= SEED_MAX) runSeed(v); else input.value = ""; });
    input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
    const first = box === document.querySelector(`.explorer[data-kind="${kind}"]`);
    const m = SEED_HASH.exec(location.hash), sm = STATE_HASH.exec(location.hash);
    if (first && m && m[1] === kind) {
      runSeed(Number(m[2]));
      requestAnimationFrame(() => box.scrollIntoView({ block: "start" }));
    } else if (sm && sm[1] === stateName(box) && opts.state && opts.state.set(sm[2])) {
      requestAnimationFrame(() => box.scrollIntoView({ block: "start" }));
    }
    return { draw };
  };
  // The random traffic row of the two protocol boxes (0025, 0024): how many events and
  // the fault rate; the run button draws a new seed. The row folds under its title (closed
  // on a phone, see folds below). `randNote` is the line under the box once a random
  // script runs: the counts, and whether the invariants held.
  const randomRow = (label, title) =>
    `<div class="ex-fold"><p class="ex-fold-title">${title}</p><div class="ex-controls an-free an-random">` +
    `<label>אירועים <select class="ex-count" aria-label="מספר האירועים">${[20, 50, 200].map((v) => `<option value="${v}"${v === 50 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
    `<label>${label} <input type="range" class="ex-rate" min="0" max="50" step="5" value="20" dir="ltr" aria-label="${label} באחוזים"><output class="out-rate">20%</output></label>` +
    `<button type="button" class="md-button md-button--primary ex-run">הרצה אקראית</button></div></div>`;
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
    return waveStrip(rows, n, { slotW: 52, labelW: 92, cursor: n - 1, ticks: (k) => first + k, label: `ציר האירועים : ${n} עמודות` });
  };
  const randNote = (rd, seed, faults, names, checks) => {
    const v = rd.violation;
    return `תנועה אקראית מערך האתחול ${ltr(seed)} : ${ltr(rd.count)} אירועים בשיעור ${ltr(`${Math.round(rd.rate * 100)}%`)}, ${faults}. ${checks} ` +
      (v ? `<span class="wv-bad">✗ אחרי אירוע ${ltr(v.index)} הופר : ${v.names.map((n) => names[n]).join(", ")}; התסריט נעצר שם.</span>` : `<span class="wv-ok">✓ אף אחד מהם לא הופר לאורך כל התסריט.</span>`) +
      ` אותו ערך אתחול נותן את אותו תסריט; "הצעד הקודם" חוזר אחורה.`;
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

  // The answer lights up (E199): when a box reaches its result, answer(box, text, marks)
  // outlines the elements that are the answer (an array, a NodeList or a selector inside
  // the box) and names it in one line under the box's summary; answer(box, null) clears
  // both. A view calls it after every draw, so the marks follow the redrawn figure. A
  // cleared line keeps its place (invisible, its last text kept), so the figures under it do
  // not move when the answer comes back; steady() shows every step once at mount, so the
  // line is there before the reader reaches the answer.
  const answer = (box, text, marks = []) => {
    box.querySelectorAll(".ex-answer-mark").forEach((el) => el.classList.remove("ex-answer-mark"));
    let line = box.querySelector(":scope > .ex-answer");
    if (!text) {
      if (line) { line.classList.add("ex-answer--off"); line.setAttribute("aria-hidden", "true"); }
      return;
    }
    const off = !line || line.classList.contains("ex-answer--off");
    if (off && box.dvqArmed && !box.dvqPriming && !reduced()) {   // reached just now: one pulse (UI329)
      box.classList.add("ex-answer-new");
      setTimeout(() => box.classList.remove("ex-answer-new"), 1000);
    }
    if (!line) {
      line = document.createElement("p");
      line.className = "ex-answer";
      line.setAttribute("role", "status");
      const at = box.querySelector(":scope > .ex-summary") || box.querySelector(":scope > .ex-controls:last-of-type");
      if (at) at.after(line); else box.append(line);
    }
    line.classList.remove("ex-answer--off");
    line.removeAttribute("aria-hidden");
    line.innerHTML = `<span class="ex-answer__tag">התשובה</span> ${text}`;
    (typeof marks === "string" ? box.querySelectorAll(marks) : marks).forEach((el) => el && el.classList.add("ex-answer-mark"));
  };

  // An explanation panel (session 28): the solution's steps as chips, the ones of the
  // moment lit; the values of the code's variables; and the page's own code with the lines
  // the step ran lit, as the page lights its key lines. The code is read from the page (the
  // tabbed block whose title names the function, in the language of the open tab, which
  // follows the site's tab choice), so the box never holds a second copy of it.
  // explain(box, title) appends the panel (a fold, closed on a phone) and returns
  // show({ code, steps, lit, lines, vars }): code names the function, steps are the chip
  // texts, lit the chips to light (from 1), lines the line numbers per language
  // ({ py, sv }, from 1), and vars an HTML line of the variables.
  const CODE_LINE = /<a id="__codelineno-\d+-\d+"[^>]*><\/a>/;
  const codeSetOf = (name) => [...document.querySelectorAll(".tabbed-set")]
    .find((set) => [...set.querySelectorAll(".filename")].some((f) => f.textContent.trim().split(/\s+/).pop() === name));
  const PANELS = new Set();
  const explain = (box, title) => {
    const panel = document.createElement("section");
    panel.className = "ex-proof ex-explain";
    panel.innerHTML = `<p class="ex-proof-title">${title}</p><ol class="ex-stepchips"></ol><p class="ex-vars"></p>` +
      `<div class="highlight ex-codewrap"><pre class="ex-codeview"><code dir="ltr" tabindex="0" aria-label="הקוד של הפתרון, השורות של הצעד מודגשות"></code></pre></div>`;
    box.append(panel);
    let st = null;
    const render = () => {
      if (!st) return;
      panel.querySelector(".ex-stepchips").innerHTML = st.steps.map((s, i) => `<li${st.lit.includes(i + 1) ? ' class="is-lit"' : ""}>${s}</li>`).join("");
      panel.querySelector(".ex-vars").innerHTML = st.vars || "";
      const set = codeSetOf(st.code), code = panel.querySelector("code");
      if (!set) { code.innerHTML = ""; return; }
      const inputs = [...set.querySelectorAll(":scope > input")], labels = [...set.querySelectorAll(".tabbed-labels label")];
      const i = Math.max(0, inputs.findIndex((r) => r.checked));
      const lang = /python/i.test(labels[i] ? labels[i].textContent : "") ? "py" : "sv";
      const src = set.querySelectorAll(".tabbed-block")[i], el = src && src.querySelector("pre code");
      let lines = [];
      if (el) {                              // without the annotation markers the theme adds
        const clone = el.cloneNode(true);
        clone.querySelectorAll(".md-annotation").forEach((a) => a.remove());
        lines = clone.innerHTML.split(CODE_LINE).slice(1);
      }
      const lit = new Set(st.lines[lang] || []);
      code.innerHTML = lines.map((h, n) => {
        let t = h.replace(/\n$/, "");
        if (/^<span class="hll">/.test(t)) t = t.replace(/^<span class="hll">/, "").replace(/\n?<\/span>$/, "");   // the page's own key lines
        return `<span class="ex-line${lit.has(n + 1) ? " hll" : ""}" data-n="${n + 1}">${t}\n</span>`;
      }).join("");
    };
    PANELS.add(render);
    if (PANELS.size === 1) {                 // the language of every panel follows the tabs
      document.addEventListener("change", (e) => {
        if (e.target.closest && e.target.closest(".tabbed-set")) setTimeout(() => PANELS.forEach((r) => r()), 0);
      });
    }
    return (state) => { st = state; render(); };
  };

  // The box's header (UI328): a title, and help, "reset everything" and "copy link" as
  // icon buttons (the word stays in the button as its name and shows as a tooltip).
  // "Reset everything" builds the box again from its defaults and, in a box that draws
  // its examples, draws a new one; the box is at its first step. That draw is the box's
  // fresh state: it is not remembered, so a reload shows the page's example.
  const header = (box, helpOpen) => {
    const bar = document.createElement("div");
    bar.className = "ex-bar";
    const resetTip = box.dvqSeed && box.dvqSeed.draw ? "איפוס הכול : הבקרות חוזרות לברירת המחדל, עם דוגמה אקראית חדשה מההתחלה"
      : "איפוס הכול : כל הבקרות חוזרות לברירת המחדל";
    bar.innerHTML = `<span class="ex-bar-title"><i class="ui-ico ui-ico-gesture" aria-hidden="true"></i>נסו בעצמכם</span>` +
      `<button type="button" class="ex-help-btn ex-ibtn ui-ico-boxhelp" aria-expanded="false" aria-label="עזרה : מה התיבה מראה ומה הכפתורים עושים" data-tip="עזרה">עזרה</button>` +
      `<button type="button" class="ex-reset-all ex-ibtn ui-ico-reset" data-tip="${resetTip}">איפוס הכול</button>` +
      `<button type="button" class="ex-link ex-ibtn ui-ico-link" data-tip="העתקת קישור לתיבה עם אותן בחירות">העתקת קישור</button>` +
      `<p class="ex-help" hidden>${HELP[box.dataset.kind] || ""}</p>`;
    box.prepend(bar);
    const btn = bar.querySelector(".ex-help-btn"), help = bar.querySelector(".ex-help");
    const show = (open) => { help.hidden = !open; btn.setAttribute("aria-expanded", String(open)); };
    btn.addEventListener("click", () => show(help.hidden));
    if (helpOpen) show(true);
    bar.querySelector(".ex-reset-all").addEventListener("click", () => {
      const play = box.querySelector(".ex-play");
      if (play && play.textContent === "עצירה") play.click();        // stop a running loop first
      if (/^#(seed|state|ctl)-/.test(location.hash)) history.replaceState(null, "", `${location.pathname}${location.search}`);
      store.drop(storeKey(box));
      setup(box, !help.hidden);
      if (box.dvqSeed && box.dvqSeed.draw) {
        box.dvqSeed.draw();
        box.dvqFresh = JSON.stringify(stateOf(box));
      }
    });
    const link = bar.querySelector(".ex-link");
    link.addEventListener("click", () => {
      const url = `${location.origin}${location.pathname}${linkOf(box)}`;
      const done = () => {
        link.textContent = link.dataset.tip = "הועתק ✓";
        link.classList.add("is-done");
        setTimeout(() => { link.textContent = "העתקת קישור"; link.dataset.tip = "העתקת קישור לתיבה עם אותן בחירות"; link.classList.remove("is-done"); }, 1500);
      };
      const fallback = () => { window.prompt("הקישור :", url); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, fallback); else fallback();
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
        const fallback = () => { window.prompt("‏JSON של WaveDrom :" , text); };
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
    hint.textContent = `מקשים כשהתיבה ממוקדת : ${hints.join(", ")}.`;
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

  // --- links and the remembered state ---------------------------------------------------

  // The controls of a box are its inputs, selects and textareas in document order, the
  // seed field aside. Their values are the payload of the header's link,
  // `#ctl-<kind>-<n>.<head>~<v1>~<v2>…` (n counts the boxes of that kind on the page from
  // 1): the head is the seed, after "s" when the controls were changed after the last
  // seeded draw (the draw is replayed first) or after "S" when the draw came last (it is
  // replayed after the controls), and empty when nothing was drawn (a seed the view put in
  // the field when it was built is the page's own example, not a draw). A box with its own
  // codec (opts.state of seedControls) links with `#state-<kind>.<payload>` instead.
  // Applying a payload sets each control in turn and fires its input and change events,
  // so a control that adds others (the bins of 0041) is set before the ones it adds. A box
  // whose state goes beyond its controls (the cuts clicked in 0020, the shapes dragged in
  // 0014) sets box.dvqExtra = { get() → text or "", set(text) → ok }: its text rides as a
  // last part "!<text>" and is applied after the controls.
  const CTL_HASH = /^#ctl-([a-z0-9-]+)-(\d+)\.(.*)$/;
  // A field marked data-nolink (an editing aid whose result rides in dvqExtra) is no control.
  const controlsOf = (box) => [...box.querySelectorAll("input, select, textarea")].filter((el) => !el.classList.contains("ex-seed") && !el.classList.contains("ex-scrub") && !el.hasAttribute("data-nolink"));
  const valueOf = (el) => (el.type === "checkbox" || el.type === "radio" ? (el.checked ? "1" : "0") : el.value);
  const enc = (v) => encodeURIComponent(v).replace(/~/g, "%7E");
  const payloadOf = (box) => {
    const seed = box.dvqSeed && box.dvqSeedAt ? box.dvqSeed.input.value : "";   // a field filled at mount is no draw
    const head = seed ? `${(box.dvqSeedAt || 0) > (box.dvqCtlAt || 0) ? "S" : "s"}${seed}` : "";
    const extra = box.dvqExtra ? box.dvqExtra.get() : "";
    return [head, ...controlsOf(box).map((el) => enc(valueOf(el))), ...(extra ? [`!${enc(extra)}`] : [])].join("~");
  };
  const setValue = (el, v) => {
    if (el.disabled || valueOf(el) === v) return;
    if (el.tagName === "SELECT" && ![...el.options].some((o) => o.value === v)) return;
    if (el.type === "checkbox" || el.type === "radio") el.checked = v === "1"; else el.value = v;
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  };
  const applyPayload = (box, payload) => {
    let parts;
    try { parts = payload.split("~").map(decodeURIComponent); } catch (e) { return false; }
    const extra = parts.length > 1 && parts[parts.length - 1].startsWith("!") ? parts.pop().slice(1) : null;
    const m = /^([sS])(\d+)$/.exec(parts.shift());
    const seed = () => {
      const n = m ? Number(m[2]) : 0;
      if (box.dvqSeed && n >= 1 && n <= SEED_MAX) box.dvqSeed.runSeed(n);
    };
    if (m && m[1] === "s") seed();
    parts.forEach((v, i) => { const el = controlsOf(box)[i]; if (el) setValue(el, v); });
    if (m && m[1] === "S") seed();
    if (extra !== null && box.dvqExtra && !box.dvqExtra.set(extra)) return false;
    return true;
  };
  const indexOf = (box) => [...document.querySelectorAll(`.explorer[data-kind="${box.dataset.kind}"]`)].indexOf(box) + 1;
  // a codec link names its box: #state-<kind>.… for the first box of a kind on the page,
  // #state-<kind>-<n>.… for the n-th (0006 has two stock boxes)
  const stateName = (box) => { const n = indexOf(box); return n > 1 ? `${box.dataset.kind}-${n}` : box.dataset.kind; };
  const ownState = (box) => (box.dvqState ? box.dvqState.get() : null);
  const linkOf = (box) => {
    const own = ownState(box);
    return own ? `#state-${stateName(box)}.${own}` : `#ctl-${box.dataset.kind}-${indexOf(box)}.${payloadOf(box)}`;
  };

  // The remembered state: the box's payload (its own codec's when it has one) in
  // localStorage, per page and box, written a moment after every change and restored when
  // the box is next built, with a line that says so and offers to start over. "איפוס הכול"
  // drops it. The saved entry carries the box's page attributes and the shape of its
  // controls at their defaults, so a box that changed on the site starts from its
  // defaults. A box opened through a link shows the link and remembers nothing.
  const STORE = "dvq-box";
  const storeKey = (box) => `${STORE}:${location.pathname}:${box.dataset.kind}:${indexOf(box)}`;
  const store = {
    get(key) { try { return JSON.parse(localStorage.getItem(key)); } catch (e) { return null; } },
    set(key, v) { try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) { /* storage off */ } },
    drop(key) { try { localStorage.removeItem(key); } catch (e) { /* storage off */ } },
  };
  const stateOf = (box) => { const own = ownState(box); return own ? { own } : { ctl: payloadOf(box) }; };
  const signature = (box) => JSON.stringify([{ ...box.dataset }, controlsOf(box).map((el) => `${el.tagName}.${el.type}`)]);
  const save = (box) => {
    if (box.dvqLinked || !box.dvqDefault) return;
    const now = stateOf(box);
    if (JSON.stringify(now) === box.dvqDefault || JSON.stringify(now) === box.dvqFresh) store.drop(storeKey(box));
    else store.set(storeKey(box), { sig: box.dvqSig, ...now });
  };
  const restore = (box) => {
    const saved = store.get(storeKey(box));
    if (!saved) return;
    const ok = saved.sig === box.dvqSig
      && (saved.own ? Boolean(box.dvqState && box.dvqState.set(saved.own)) : applyPayload(box, saved.ctl || ""));
    if (!ok) { store.drop(storeKey(box)); return; }
    const note = document.createElement("p");
    note.className = "ex-restored";
    note.setAttribute("role", "status");
    note.innerHTML = `התיבה חזרה למצב שבו עצרת. <button type="button" class="ex-restart">להתחיל מחדש</button>`;
    box.querySelector(".ex-bar").after(note);
    note.querySelector(".ex-restart").addEventListener("click", () => box.querySelector(".ex-reset-all").click());
  };
  // Once per box: a change of a control (not the seed field) is timed against the seeded
  // draws, and any change is saved a moment later.
  const watch = (box) => {
    if (box.dvqWatched) return;
    box.dvqWatched = true;
    box.addEventListener("input", (e) => { if (!e.target.matches(".ex-seed, .ex-scrub")) box.dvqCtlAt = ++tick; }, true);
    let timer = null;
    // the steps steady() presses to measure the box are not the reader's changes
    const later = () => { if (box.dvqPriming) return; clearTimeout(timer); timer = setTimeout(() => save(box), 300); };
    ["input", "change", "click", "pointerup", "keyup"].forEach((ev) => box.addEventListener(ev, later));
  };

  // One layout for every box (E200), without touching the views: every child of a
  // controls row is tagged as an input (a label with a field), an action (a button that
  // draws or resets), playback (play, step, the speed select, the step counter) or other,
  // and the CSS shows them in that order with the same spacing and button size. The DOM
  // order stays, so the link payloads (the controls in document order) do not change.
  const PLAYBACK = "button.ex-play, button.ex-next, button.ex-prev, button.ex-start, button.ex-end, button.ex-first, " +
    "button.ex-last, button.ex-solve, button.ex-cycle, button.ex-step, .ex-pos";
  const layout = (box) => {
    box.querySelectorAll(".ex-controls").forEach((row) => {
      for (const el of row.children) {
        const kind = el.matches(PLAYBACK) || el.querySelector("select.ex-speed") ? "play"
          : el.matches("label") || el.querySelector("input, select, textarea") ? "input"
          : el.matches("button, .md-button") ? "action" : "other";
        el.classList.add(`ex-c-${kind}`);
      }
      // three or more action buttons in a row (examples, moves, amounts) go into one run
      // that scrolls sideways on a phone instead of wrapping into several lines (S418);
      // the order stays, and elsewhere the run lays out as if it were not there; a row a
      // view lays out as a grid (0024's events, one per cell) keeps its grid; the run is
      // not tagged as an action itself, so the button size and padding stay on its buttons
      if (!getComputedStyle(row).display.includes("flex")) return;
      let run = [];
      const close = () => {
        if (run.length >= 3) {
          const wrap = document.createElement("span");
          wrap.className = "ex-btnrun";
          run[0].before(wrap);
          wrap.append(...run);
        }
        run = [];
      };
      for (const el of [...row.children]) {
        if (el.matches("button.ex-c-action, .md-button.ex-c-action")) run.push(el); else close();
      }
      close();
    });
  };

  // Playback as one icon bar (UI327): in a controls row, the start, previous, play, next
  // and end buttons move (listeners and all) into a bar laid out left to right, as media
  // controls are, and show an icon; the word stays in the button as its name and shows as
  // a tooltip, and a play button whose word turns into "עצירה" shows the pause icon. The
  // usual slow / medium / fast select is kept (it is a control of the link) but hidden
  // behind three buttons beside the bar; a box with its own speed list keeps the select. A box with a "k מתוך T" counter gets a scrubber under the row: it
  // presses the box's own start / next buttons to reach a step, so every view keeps its
  // own stepping. The scrubber and the speed buttons are not controls of the link.
  // The same seek keeps the place on the timeline through an edit (see edits below).
  const TRANSPORT = [["button.ex-start, button.ex-first", "first"], ["button.ex-prev", "prev"], ["button.ex-play", "play"],
    ["button.ex-next", "next"], ["button.ex-end, button.ex-last", "last"]];
  const SPEED_NAMES = ["×1", "×2", "×4"], SPEED_WORDS = "איטי,בינוני,מהיר";   // other speed lists stay a select
  const SCRUB_MAX = 5000;
  const POS = /(\d+)\s*מתוך\s*(\d+)/;
  const transport = (box) => {
    box.querySelectorAll(".ex-controls").forEach((row) => {
      const own = (el) => el && el.closest(".ex-controls") === row;
      const found = TRANSPORT.map(([sel, icon]) => [[...row.querySelectorAll(sel)].find(own), icon]).filter(([b]) => b);
      if (!found.some(([, icon]) => icon === "play" || icon === "next")) return;
      const bar = document.createElement("span");
      bar.className = "ex-transport ex-c-play";
      bar.setAttribute("dir", "ltr");
      found[0][0].before(bar);
      found.forEach(([b, icon]) => {
        b.classList.add("ex-tbtn", `ui-ico-${icon}`);
        const sync = () => {
          const word = b.textContent.trim();
          b.dataset.tip = word;
          b.classList.toggle("is-playing", icon === "play" && word === "עצירה");
        };
        new MutationObserver(sync).observe(b, { childList: true, characterData: true, subtree: true });
        sync();
        bar.append(b);
      });
      const sel = [...row.querySelectorAll("select.ex-speed")].find(own);
      if (sel && [...sel.options].map((o) => o.text.trim()).join() === SPEED_WORDS) {
        const seg = document.createElement("span");
        seg.className = "ex-speedseg";
        seg.setAttribute("role", "group");
        seg.setAttribute("aria-label", "הקצב");
        const btns = [...sel.options].map((o, i) => {
          const b = document.createElement("button");
          b.type = "button";
          b.className = "ex-speedbtn";
          b.textContent = SPEED_NAMES[i] || o.text;
          b.dataset.tip = `קצב ${o.text}`;
          b.setAttribute("aria-label", `${b.textContent}, קצב ${o.text}`);   // the visible text first
          b.addEventListener("click", () => {
            sel.value = o.value;
            sel.dispatchEvent(new Event("input", { bubbles: true }));
            sel.dispatchEvent(new Event("change", { bubbles: true }));
          });
          seg.append(b);
          return [b, o];
        });
        const paint = () => btns.forEach(([b, o]) => b.setAttribute("aria-pressed", String(sel.value === o.value)));
        sel.addEventListener("change", paint);
        paint();
        (sel.closest("label") || sel).classList.add("ex-speed-kept");
        bar.append(seg);
      }
      const posOf = () => [...box.querySelectorAll(".ex-pos")].find(own) || null;   // views may redraw the counter
      const next = found.find(([, icon]) => icon === "next"), first = found.find(([, icon]) => icon === "first");
      const prev = found.find(([, icon]) => icon === "prev"), last = found.find(([, icon]) => icon === "last");
      const play = found.find(([, icon]) => icon === "play");
      if (!posOf() || !next) return;
      const wrap = document.createElement("div");
      wrap.className = "ex-scrubwrap";
      wrap.innerHTML = `<input type="range" class="ex-scrub" min="0" step="1" dir="ltr" aria-label="קפיצה לצעד">`;
      row.after(wrap);
      const scrub = wrap.querySelector("input");
      const read = () => { const pos = posOf(), m = pos && POS.exec(pos.textContent); return m ? [Number(m[1]), Number(m[2])] : null; };
      const show = () => {
        const kt = read();
        wrap.hidden = !kt || kt[1] < 1 || kt[1] > SCRUB_MAX;
        if (wrap.hidden) return;
        scrub.max = kt[1];
        if (document.activeElement !== scrub) scrub.value = kt[0];
        scrub.style.setProperty("--scrub", `${(100 * kt[0]) / kt[1]}%`);
        scrub.setAttribute("aria-valuetext", posOf().textContent.trim());
      };
      const seek = (goal) => {
        let kt = read();
        if (!kt) return;
        if (goal >= kt[1] && kt[0] < kt[1] && last) { last[0].click(); kt = read(); if (!kt) return; }
        if (goal < kt[0]) {
          if (first) first[0].click();
          else for (let i = kt[0] - goal; i > 0 && prev; i--) prev[0].click();
          kt = read();
        }
        for (let guard = 0; kt && kt[0] < goal && guard < SCRUB_MAX; guard++) {
          next[0].click();
          const now = read();
          if (!now || now[0] === kt[0]) break;            // the box stopped advancing
          kt = now;
        }
      };
      // After an edit (see edits), a counter that went back (the view started over) or kept
      // its step while the number of steps changed returns to the same step, or to the same
      // place relative to the new number of steps when it changed; the end stays the end. A
      // play the edit stopped goes on.
      let was = read();
      const keep = () => {
        const now = read(), old = was;
        if (!now) return;
        was = now;
        if (box.dvqSeeking || box.dvqCause !== "edit" || performance.now() - box.dvqCauseAt > EDIT_MS || !old) return;
        const restart = now[0] < old[0] || (now[1] !== old[1] && now[0] === old[0]);
        const goal = old[0] >= old[1] ? now[1] : now[1] === old[1] ? old[0] : Math.round((old[0] * now[1]) / old[1]);
        const resume = play && box.dvqPlaying && box.dvqPlaying.includes(play[0]);
        if ((!restart || goal === now[0] || old[1] < 1 || now[1] > SCRUB_MAX) && !resume) return;
        box.dvqSeeking = true;
        try {
          if (restart && old[1] >= 1 && now[1] <= SCRUB_MAX) seek(goal);
          was = read();
          if (resume && play[0].textContent.trim() !== "עצירה" && was && was[0] < was[1]) play[0].click();
        } finally { box.dvqSeeking = false; }
        if (resume) box.dvqPlaying = box.dvqPlaying.filter((b) => b !== play[0]);
      };
      let queued = false;
      new MutationObserver((records) => {
        if (queued || records.every((r) => wrap.contains(r.target))) return;
        queued = true;
        queueMicrotask(() => { queued = false; keep(); show(); });
      }).observe(box, { childList: true, characterData: true, subtree: true });
      show();
      scrub.addEventListener("input", () => { seek(Number(scrub.value)); show(); });
    });
  };

  // Edits and navigation, for the place on the timeline (transport above): an event on a
  // field, a button that is not playback, a slider point or a figure the view marks
  // data-edits (cells typed, clicked or dragged) is an edit; the transport, the scrubber,
  // the header, the keys of the box and a click elsewhere in a figure (which may pick a
  // step) are navigation. The play buttons running at an edit are noted, to go on after it.
  // An edit counts for EDIT_MS (the views redraw at once; a drag renews it), so a play
  // that goes on after it is never taken for one. Clicks of the seek itself do not count.
  const EDIT_MS = 600;
  const NAV = `.ex-transport, .ex-scrubwrap, .ex-bar, .ex-restored, .ex-guide, select.ex-speed, ${PLAYBACK}`;
  const causeOf = (e) => {
    const t = e.target instanceof Element ? e.target : null;
    if (!t || t.closest(NAV)) return "nav";
    if (t.matches("input, select, textarea") || t.closest("[data-edits], [role=slider]")) return "edit";
    return (e.type === "click" || e.type === "pointerdown") && t.closest("button, [role=button]") ? "edit" : "nav";
  };
  const edits = (box) => {
    if (box.dvqEdits) return;                           // a rebuilt box keeps its listeners
    box.dvqEdits = true;
    const note = (e) => {
      if (box.dvqSeeking) return;
      box.dvqCause = causeOf(e);
      box.dvqCauseAt = performance.now();
      if (box.dvqCause === "edit") box.dvqPlaying = [...box.querySelectorAll("button.ex-play")].filter((b) => b.textContent.trim() === "עצירה");
    };
    ["pointerdown", "click", "keydown", "input", "change"].forEach((ev) => box.addEventListener(ev, note, true));
    box.addEventListener("pointermove", (e) => { if (e.buttons && box.dvqCause === "edit") box.dvqCauseAt = performance.now(); }, true);
  };

  // Motion (UI329): once a person has touched the box (a trusted pointer or key event, so
  // a restored state and the page checks draw without it), every redraw is compared with
  // the one before. The values that changed (leaf elements of up to VALUE_MAX characters,
  // empty ones too: table and grid cells, labels) flash for a moment; in the kinds of TWEEN a
  // changed integer also counts to its new value, and a bar (an SVG rect with one edge
  // kept) grows from its old size or slides from its old place. A redraw that keeps few of
  // the places is a new picture and moves nothing; more than CHANGED_MAX changed values, or
  // a reshuffle of values already shown, flash nothing either. The flash is as
  // long as the time since the last redraw allows (a fast play keeps up), and none of it
  // runs under prefers-reduced-motion. Values are matched by their place in the box (the
  // path of child indices), so a redraw that adds an overlay still lines up. When a box
  // reaches its answer, the marks pulse once.
  const TWEEN = new Set(["maxones", "eggs", "eurovision", "coverage", "stages", "credits"]);
  const VALUE_MAX = 8, FLASH_MS = [160, 600], MOST = 0.4, CHANGED_MAX = 8;
  const STILL_PARTS = ".ex-bar, .ex-controls, .ex-scrubwrap, .ex-answer, .ex-help, .ex-keys, .ex-pos, .ex-guide, button, select, input, textarea, label, title, desc";
  const INT = /^-?\d+$/;
  const reduced = () => typeof matchMedia === "function" && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const textOf = (el) => (el.dvqTo !== undefined ? el.dvqTo : el.textContent).trim();
  // a value: an element with no child elements and a short text (an empty cell counts, so
  // a cell filled in by the step flashes), not a drawn shape, a paragraph or a word inside
  // a sentence
  const SHAPES = new Set(["rect", "path", "circle", "ellipse", "line", "polyline", "polygon", "use", "image", "stop", "i", "br", "hr", "img", "p"]);
  const valuesOf = (box) => [...box.querySelectorAll("*")].filter((el) => {
    if (el.firstElementChild || SHAPES.has(el.localName) || el.closest(STILL_PARTS)) return false;
    if ([...el.parentNode.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) return false;
    return textOf(el).length <= VALUE_MAX;
  });
  const rectsOf = (box) => [...box.querySelectorAll("svg rect")].filter((el) => !el.closest(STILL_PARTS));
  const pathOf = (box, el) => {                          // the element's place in the box
    const at = [];
    for (let e = el; e && e !== box; e = e.parentElement) at.push(Array.prototype.indexOf.call(e.parentElement.children, e));
    return at.join(".");
  };
  const geomOf = (el) => ["x", "y", "width", "height"].map((a) => Number(el.getAttribute(a)) || 0);
  const countTo = (el, from, to, ms) => {
    const t0 = performance.now(), text = String(to);
    el.dvqTo = text;
    const tick = (now) => {
      if (el.dvqTo !== text) return;                     // a newer count took over
      const u = Math.min(1, (now - t0) / ms), e = 1 - (1 - u) * (1 - u);
      el.textContent = u < 1 ? String(Math.round(from + (to - from) * e)) : text;
      if (u < 1) requestAnimationFrame(tick);
      else queueMicrotask(() => { if (el.dvqTo === text) delete el.dvqTo; });   // after the watch saw this last write
    };
    requestAnimationFrame(tick);
  };
  const moveRect = (el, [x0, y0, w0, h0], [x1, y1, w1, h1], ms) => {
    if (typeof el.animate !== "function" || !w1 || !h1) return;
    const near = (a, b) => Math.abs(a - b) < 0.05;
    let from = null, origin = "center";
    if (near(w0, w1) && near(h0, h1)) from = `translate(${x0 - x1}px, ${y0 - y1}px)`;
    else if (near(x0, x1) && near(w0, w1)) {
      if (near(y0 + h0, y1 + h1)) origin = "center bottom";
      else if (near(y0, y1)) origin = "center top";
      else return;
      from = `scale(1, ${h0 / h1})`;
    } else if (near(y0, y1) && near(h0, h1)) {
      if (near(x0, x1)) origin = "left center";
      else if (near(x0 + w0, x1 + w1)) origin = "right center";
      else return;
      from = `scale(${w0 / w1}, 1)`;
    } else return;
    el.style.transformBox = "fill-box";
    el.style.transformOrigin = origin;
    el.animate([{ transform: from }, { transform: "none" }], { duration: ms, easing: "ease-out" });
  };
  const motion = (box) => {
    box.dvqSnap = null;
    if (box.dvqMotion) return;                           // a box set up again keeps its watch
    box.dvqMotion = true;
    if (typeof MutationObserver === "undefined" || reduced()) return;
    let queued = false, last = 0;
    const arm = (e) => {
      if (!e.isTrusted || box.dvqArmed) return;
      box.dvqArmed = true;
      compare();                                         // the picture before the first change
    };
    box.addEventListener("pointerdown", arm, true);
    box.addEventListener("keydown", arm, true);
    const compare = () => {
      queued = false;
      if (!box.dvqArmed) return;
      const els = valuesOf(box), rects = TWEEN.has(box.dataset.kind) ? rectsOf(box) : [];
      const snap = {
        texts: new Map(els.map((el) => [pathOf(box, el), [el, textOf(el)]])),
        geoms: new Map(rects.map((el) => [pathOf(box, el), [el, geomOf(el)]])),
      };
      const before = box.dvqSnap;
      box.dvqSnap = snap;
      const now = performance.now(), gap = now - last;
      last = now;
      if (!before || reduced()) return;
      const ms = Math.round(Math.max(FLASH_MS[0], Math.min(FLASH_MS[1], gap * 0.8)));
      box.style.setProperty("--ex-flash", `${ms}ms`);
      // the same place in the drawing before and after; a new picture keeps few of them
      const pairs = (now_, then) => {
        const both = [...now_].filter(([k]) => then.has(k)).map(([k, [el, v]]) => [el, then.get(k)[1], v]);
        return both.length >= MOST * Math.max(now_.size, then.size) ? both : [];
      };
      // a value that was emptied does not flash; more than a few changes that only move
      // texts already shown (a list shifting, a circle renumbered) are a reshuffle
      const changed = pairs(snap.texts, before.texts).filter(([, a, b]) => a !== b && b !== "");
      const shown = new Set([...before.texts.values()].map(([, v]) => v));
      const shifted = changed.filter(([, , b]) => shown.has(b)).length;
      if (changed.length && changed.length <= CHANGED_MAX && (changed.length <= 3 || shifted < changed.length / 2)) {
        changed.forEach(([el, a, b]) => {
          if (el.dvqTo === undefined && TWEEN.has(box.dataset.kind) && INT.test(a) && INT.test(b) && Math.abs(Number(b) - Number(a)) > 1) {
            countTo(el, Number(a), Number(b), ms);
          }
          el.classList.remove("ex-changed");
          void el.getBoundingClientRect();               // restart the flash on a reused element
          el.classList.add("ex-changed");
          setTimeout(() => el.classList.remove("ex-changed"), ms + 50);
        });
      }
      const moved = pairs(snap.geoms, before.geoms).filter(([, g0, g1]) => g0.some((v, k) => Math.abs(v - g1[k]) >= 0.05));
      if (moved.length && moved.length <= Math.max(4, MOST * snap.geoms.size)) moved.forEach(([el, g0, g1]) => moveRect(el, g0, g1, ms));
    };
    new MutationObserver((records) => {
      if (queued || records.every((r) => (r.target.nodeType === 1 ? r.target : r.target.parentNode).dvqTo !== undefined)) return;
      queued = true;
      queueMicrotask(compare);
    }).observe(box, { childList: true, characterData: true, subtree: true });
  };

  // A first-visit guide (E201): on the page's first box with a playback bar, once per
  // browser, three short hints in turn point at the playback bar, the figure and the
  // summary line, each with "next" and "skip". They show when the box is mostly in view.
  // An automated browser (the page checks) sees none unless the address has ?guide.
  const GUIDE = "dvq-guide";
  const GUIDE_STEPS = [
    [".ex-transport", false, "כאן מריצים את התיבה : צעד קדימה או אחורה, הפעלה רציפה או קפיצה לסוף. הפס שמתחת קופץ ישר לכל צעד."],
    ["svg", true, "הציור מתעדכן בכל צעד, ומה שהצעד שינה מהבהב לרגע בכתום."],
    [".ex-summary", false, "כאן כתוב מה קרה בצעד, ובסוף מופיעה התשובה בירוק. בכפתור העזרה שבראש התיבה יש הסבר מלא."],
  ];
  const guideSeen = () => { try { return localStorage.getItem(GUIDE) === "1"; } catch (e) { return true; } };
  const guide = (box) => {
    const forced = /[?&]guide\b/.test(location.search);
    if (document.querySelector(".ex-guide") || (!forced && (guideSeen() || navigator.webdriver))) return;
    const first = [...document.querySelectorAll(".explorer")].find((b) => b.querySelector(".ex-transport"));
    if (first !== box || typeof IntersectionObserver === "undefined") return;
    const steps = GUIDE_STEPS.map(([sel, inside, text]) => {
      const area = (e) => { const r = e.getBoundingClientRect(); return r.width > 120 ? r.width * r.height : 0; };
      const all = [...box.querySelectorAll(sel)].filter((e) => sel === ".ex-transport" || !e.closest(".ex-bar, .ex-controls"));
      const el = inside ? all.filter(area).sort((a, b) => area(b) - area(a))[0] : all[0];   // the largest figure
      return el && el.getClientRects().length ? { el, inside, text } : null;
    }).filter(Boolean);
    if (!steps.length) return;
    const seen = new IntersectionObserver((entries) => {
      // mostly in view: 60% of the box, or half the screen for a tall box
      if (!entries.some((e) => e.intersectionRatio >= 0.6 || e.intersectionRect.height >= 0.5 * window.innerHeight) || !box.isConnected) return;
      seen.disconnect();
      try { localStorage.setItem(GUIDE, "1"); } catch (e) { /* private mode */ }
      let i = 0;
      const tip = document.createElement("div");
      tip.className = "ex-guide";
      tip.setAttribute("role", "note");
      tip.setAttribute("aria-live", "polite");
      box.classList.add("has-guide");
      box.append(tip);
      const place = () => {
        if (!tip.isConnected) return;
        const st = steps[i], br = box.getBoundingClientRect(), tr = st.el.getBoundingClientRect();
        const w = tip.offsetWidth, cx = tr.left + tr.width / 2 - br.left;
        const left = Math.max(8, Math.min(br.width - w - 8, cx - w / 2));
        tip.style.top = `${(st.inside ? tr.top + 12 : tr.bottom + 10) - br.top}px`;
        tip.style.left = `${left}px`;
        tip.style.setProperty("--ax", `${Math.round(cx - left)}px`);
        tip.classList.toggle("is-inside", st.inside);
      };
      const end = () => {
        steps.forEach((st) => st.el.classList.remove("ex-guide-target"));
        tip.remove();
        box.classList.remove("has-guide");
        window.removeEventListener("resize", place);
      };
      const show = () => {
        steps.forEach((st, k) => st.el.classList.toggle("ex-guide-target", k === i));
        tip.innerHTML = `<p class="exg-text"></p><div class="exg-foot"><span class="exg-pos">${i + 1} מתוך ${steps.length}</span>` +
          `<button type="button" class="exg-skip">דילוג</button><button type="button" class="exg-next">${i + 1 < steps.length ? "הבא" : "הבנתי"}</button></div>`;
        tip.querySelector(".exg-text").textContent = steps[i].text;
        tip.querySelector(".exg-skip").addEventListener("click", end);
        tip.querySelector(".exg-next").addEventListener("click", () => { if (++i < steps.length) show(); else end(); });
        place();
        if (typeof tip.scrollIntoView === "function") tip.scrollIntoView({ block: "nearest" });
      };
      tip.addEventListener("keydown", (e) => { if (e.key === "Escape") end(); });
      window.addEventListener("resize", place, { passive: true });
      show();
    }, { threshold: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6] });
    seen.observe(box);
  };

  // Steady heights: the text of a box changes at every step, and a line more or less moved
  // everything under it (the figure jumped up and down while playing). Every text paragraph
  // of the box (the summary, the captions, the step lines, the proof text) keeps the
  // tallest height it has shown: the height only grows, until a control changes a value,
  // "back to the question's values" is clicked, or the window changes width; then the
  // heights are released and measured again. A rebuilt box keeps its listeners, and a
  // paragraph that is hidden or empty (display: none) reserves nothing. A block of a view
  // that grows with the steps above a figure (a zoom window, a scrolling table) is marked
  // data-steady and kept the same way.
  //
  // The tallest heights are known before the reader steps: prime() runs every row that has
  // a step counter ("k מתוך T", or a bare count), a previous and a next button from its
  // first step to its last and back, measuring each step, at mount and whenever the
  // heights are released. It runs
  // synchronously, so the observers (the transport's keep, motion, steady itself) only see
  // the step it returns to; it skips a box that is playing, a row of more than PRIME_MAX
  // steps, and stops after PRIME_MS (the heights then still grow as before).
  const STEADY = "p, .ex-note, [aria-live], [data-steady]";
  const PRIME_MAX = 150, PRIME_MS = 250;
  const steady = (box) => {
    let queued = false;
    const fit = () => {
      queued = false;
      box.querySelectorAll(STEADY).forEach((el) => {
        if (el.hidden || el.closest(".ex-controls, .ex-bar, .fig-lightbox")) return;
        let h = el.getBoundingClientRect().height;
        if (!h) return;
        const cs = getComputedStyle(el);
        if (cs.boxSizing !== "border-box") {
          h -= parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom) + parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth);
        }
        if (h > (el.dvqSteady || 0) + 0.5) { el.dvqSteady = h; el.style.minHeight = `${h}px`; }
      });
    };
    const schedule = () => { if (!queued) { queued = true; requestAnimationFrame(fit); } };
    const prime = () => {
      if (box.dvqPriming || !box.isConnected || !box.getClientRects().length) return;
      if ([...box.querySelectorAll("button.ex-play")].some((b) => b.textContent.trim() === "עצירה")) return;
      const t0 = performance.now(), seeking = box.dvqSeeking;
      box.dvqPriming = box.dvqSeeking = true;
      try {
        box.querySelectorAll(".ex-controls").forEach((row) => {
          const own = (el) => el && el.closest(".ex-controls") === row;
          const find = (sel) => [...row.querySelectorAll(sel)].find(own);
          const read = () => {                             // "k מתוך T", or a bare count ("52 טסטים")
            const pos = [...box.querySelectorAll(".ex-pos")].find(own);
            const m = pos && (POS.exec(pos.textContent) || /(\d+)/.exec(pos.textContent));
            return m ? [Number(m[1]), m[2] === undefined ? Infinity : Number(m[2])] : null;
          };
          const step = (sel) => {                          // press, and say whether the counter moved
            const b = find(sel), was = read();
            if (!b || b.disabled || !was) return false;
            b.click();
            const now = read();
            return Boolean(now) && now[0] !== was[0];
          };
          // back with the previous button only: a start button may also clear a history
          const toFirst = () => { for (let i = 0; i < PRIME_MAX && step("button.ex-prev"); i++); };
          const start = read();
          // a timeline has both directions: a next without a previous draws something new
          // (a random test), and that is the reader's to press
          if (!start || (Number.isFinite(start[1]) && start[1] > PRIME_MAX) || !find("button.ex-next") || !find("button.ex-prev")) return;
          toFirst();
          fit();
          for (let i = 0; i < PRIME_MAX && performance.now() - t0 < PRIME_MS; i++) {
            const was = read();
            if (!step("button.ex-next") || read()[0] < was[0]) break;
            fit();
          }
          toFirst();
          for (let i = 0; i < PRIME_MAX && read() && read()[0] < start[0] && step("button.ex-next"); i++);
        });
      } finally {
        box.dvqPriming = false;
        box.dvqSeeking = seeking;
      }
    };
    const release = () => {
      box.querySelectorAll(STEADY).forEach((el) => {
        if (!el.dvqSteady) return;
        el.dvqSteady = 0;
        el.style.minHeight = "";
        if (!el.getAttribute("style")) el.removeAttribute("style");
      });
      schedule();
      setTimeout(prime, 0);                                // after the view and the transport settled
    };
    schedule();
    prime();
    if (box.dvqSteadyOn) return;
    box.dvqSteadyOn = true;
    new MutationObserver(schedule).observe(box, { childList: true, characterData: true, subtree: true });
    box.addEventListener("change", (e) => {
      const t = e.target;
      if (t.matches("input, select, textarea") && t.closest(".ex-controls") && !t.closest(".ex-play-row, .ex-scrub")) release();
    });
    box.addEventListener("click", (e) => { if (e.target.closest(".ex-reset")) release(); });
    box.addEventListener("dvq-fold", schedule);              // an opened fold shows text not measured yet
    let timer = 0;
    window.addEventListener("resize", () => { clearTimeout(timer); timer = setTimeout(release, 150); }, { passive: true });
  };

  // Folds (V3): a proof panel (.ex-proof, under its .ex-proof-title) or a group of
  // controls (.ex-fold, under its .ex-fold-title) opens and closes from its title, which
  // becomes a button. It starts closed on a phone and open on a wider screen. Folded, only
  // the title shows; the controls stay in the box in document order, so the link and the
  // remembered state are the same either way. data-fold="closed" starts closed everywhere.
  const FOLD_NARROW = "(max-width: 44.9375em)";
  const folds = (box) => {
    const closed = typeof matchMedia === "function" && matchMedia(FOLD_NARROW).matches;
    box.querySelectorAll(".ex-proof, .ex-fold").forEach((panel) => {
      const title = panel.querySelector(":scope > .ex-proof-title, :scope > .ex-fold-title");
      if (!title || title.querySelector(".ex-fold-btn")) return;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "ex-fold-btn";
      btn.append(...title.childNodes);
      title.append(btn);
      const set = (open) => {
        panel.classList.toggle("is-folded", !open);
        btn.setAttribute("aria-expanded", String(open));
        box.dispatchEvent(new Event("dvq-fold"));
      };
      btn.addEventListener("click", () => set(panel.classList.contains("is-folded")));
      set(!closed && panel.dataset.fold !== "closed");
    });
  };

  const setup = (box, helpOpen = false) => {
    const make = VIEWS[box.dataset.kind];
    if (!make) return;
    box.dvqSeedAt = box.dvqCtlAt = 0;                    // a rebuilt box has drawn nothing yet
    box.dvqFresh = null;
    box.dvqSeed = null;
    make(box).mount(box);
    folds(box);
    layout(box);
    transport(box);
    edits(box);
    header(box, helpOpen);
    keyboard(box);
    decorateLive(box);
    steady(box);
    watch(box);
    motion(box);
    guide(box);
    box.dvqSig = signature(box);
    box.dvqDefault = JSON.stringify(stateOf(box));
  };

  // --- lazy building -------------------------------------------------------------------------

  // A box is built when it comes within one screen of the viewport (a box inside a closed
  // block waits until the block opens), and then gets its remembered state back. The box a
  // link points at (`#seed-<kind>-…`, `#state-<kind>.…` or `#ctl-<kind>-<n>.…`) is built at
  // once, its closed blocks opened, and scrolled into view. ready() builds every box that
  // is still waiting, for the page checks (tools/check_phone.py, tools/check_explorers.py)
  // and for printing.
  const waiting = new Set();
  let observer = null;
  const build = (box) => {
    if (!waiting.delete(box)) return;
    if (observer) observer.unobserve(box);
    setup(box);
    if (!box.dvqLinked) restore(box);
  };
  const ready = () => { [...waiting].forEach(build); return Promise.resolve(); };
  const linked = (boxes) => {
    const c = CTL_HASH.exec(location.hash), m = c || SEED_HASH.exec(location.hash) || STATE_HASH.exec(location.hash);
    if (!m) return null;
    if (!c && !SEED_HASH.test(location.hash)) {   // a #state- link
      const box = boxes.find((b) => stateName(b) === m[1]);
      return box ? { box, payload: null } : null;
    }
    const box = boxes.filter((b) => b.dataset.kind === m[1])[c ? Number(c[2]) - 1 : 0];
    return box ? { box, payload: c ? c[3] : null } : null;
  };

  // --- the registry ----------------------------------------------------------------------------

  // Every kind file (explorer/<kind>.js) registers its views, its help line and the pure
  // functions the question tests compare with the Python reference. Under Node the
  // models of every file are merged (tools/explorer_node.js) and nothing is built.
  const VIEWS = {}, HELP = {};
  const models = { mulberry32, waveDromOf, waveDromText, floydTrace, floydParse, STATE_CODECS, bitsOf };
  const register = ({ views = {}, help = {}, models: own = {} }) => {
    Object.assign(VIEWS, views);
    Object.assign(HELP, help);
    Object.assign(models, own);
  };
  // Editing a grid of numbers (0046, 0047): the view select (every step, or straight to the
  // final result, which every later edit keeps), and the text of a grid: a row per line
  // (or Python's [[...], [...]]), the numbers split by commas or spaces, or digit by digit
  // when a line has neither and the values are single digits. parseGrid returns the grid
  // or a Hebrew reason it was not taken.
  const viewSel = () => `<label>תצוגה <select class="ex-view" aria-label="צעד אחרי צעד, או ישר לתוצאה הסופית"><option value="steps">צעד אחרי צעד</option><option value="final">התוצאה הסופית</option></select></label>`;
  const parseGrid = (text, { max, rows, cols, row = false }) => {
    let lines = text.trim();
    if (!lines) return "השדה ריק.";
    if (/^\[\s*\[/.test(lines)) lines = lines.replace(/\]\s*,?\s*\[/g, "\n");
    lines = lines.replace(/[\[\]]/g, "").split(/\n|;/).map((l) => l.trim()).filter(Boolean);
    if (row) lines = [lines.join(",")];
    const grid = lines.map((l) => (/[\s,]/.test(l) ? l.split(/[\s,]+/).filter(Boolean) : max <= 9 ? [...l] : [l]));
    if (grid.some((r) => r.some((v) => !/^\d+$/.test(v)))) return "יש בשדה משהו שהוא לא מספר שלם.";
    const g = grid.map((r) => r.map(Number));
    if (g.some((r) => r.some((v) => v > max))) return `הערכים הם 0 עד ${max}.`;
    if (g.some((r) => r.length !== g[0].length)) return "לכל השורות צריך להיות אותו אורך.";
    if (g.length > rows || g[0].length > cols) return row ? `עד ${cols} ערכים.` : `עד ${rows} שורות ועד ${cols} עמודות.`;
    return g;
  };
  const gridText = (grid, row = false) => (row ? grid[0].join(", ") : grid.map((r) => r.join(" ")).join("\n"));

  const lib = {
    BASE, EPS, H, KB_DIGITS, RAND_HASH, RIGHT, SEED_MAX, STATE_CODECS, TOP, TRI_M, W, X0,
    answer, arrowStep, attr, autoplay, bigComb, bitsOf, code, eventStrip, explain, f, floydParse, floydTrace, fmt, frame, hline,
    gridText, ltr, mulberry32, newSeed, parseGrid, randNote, randomRow, seedControls, speedSel, stickyNames, triNorm, viewSel,
    waveDromText, waveStrip,
  };
  globalThis.dvqExplorers = { lib, models, register, ready, linkOf };
  if (typeof document === "undefined") return;

  window.addEventListener("beforeprint", ready);
  document.addEventListener("DOMContentLoaded", () => {
    const boxes = [...document.querySelectorAll(".explorer")];
    boxes.forEach((box) => waiting.add(box));
    const link = linked(boxes);
    if (link) {
      const { box, payload } = link;
      for (let d = box.closest("details"); d; d = d.parentElement.closest("details")) d.open = true;
      box.dvqLinked = true;
      build(box);
      if (payload !== null) {
        applyPayload(box, payload);
        requestAnimationFrame(() => box.scrollIntoView({ block: "start" }));
      }
    }
    if (!("IntersectionObserver" in window)) { ready(); return; }
    observer = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) build(e.target); });
    }, { rootMargin: "100% 0px" });
    waiting.forEach((box) => observer.observe(box));
  });
})();
