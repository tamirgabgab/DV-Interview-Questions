// kinds: gridpath
//   gridpath               0070        a grid of open cells and walls (data-grid, rows joined by dots; in mode c every cell a cost 1..9 or # for a wall) with a start and a target (data-s, data-t "r,c") and three modes: a, the BFS of shortest_path; b, the BFS over (cell, breaks left) of shortest_with_breaks with k from 0 to 5 (data-k); c, the Dijkstra of cheapest_path. Four or eight directions (data-diag), the rows and the columns from 4 to 14, a tap or a drag paints walls (a, b) or the brush's cost (c), S and T dragged, a random grid from a seed and a clear one; every step one pop: the cell out of the queue framed, its neighbours marked, the frontier tinted, every visited cell with its distance (b: and the most breaks left, c: its cost), the path drawn at the end; a caption per step, the queue or the heap under the grid and the explain panel with the code lines of the step
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, explain, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = "\u00a0";
  const MINS = 4, MAXS = 14, KMAX = 5, LIST_MAX = 14;
  const DIRS = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]];
  const DIR_HEB = ["למעלה", "למטה", "שמאלה", "ימינה", "למעלה-שמאלה", "למעלה-ימינה", "למטה-שמאלה", "למטה-ימינה"];

  // --- the three searches, pop by pop, as tools/figures/q0070.py trace() ------------------
  // The moves out of (r, c) in the order of the table, as [a, b, k, squeezed]: a diagonal
  // between two walls is squeezed, not a move (the page's rule).
  const gpMoves = (grid, r, c, diag, wall) => {
    const m = grid.length, n = grid[0].length, out = [];
    (diag ? DIRS : DIRS.slice(0, 4)).forEach(([dr, dc], k) => {
      const a = r + dr, b = c + dc;
      if (a < 0 || a >= m || b < 0 || b >= n) return;
      out.push([a, b, k, Boolean(dr && dc && grid[r][b] === wall && grid[a][c] === wall)]);
    });
    return out;
  };
  // A frame per pop: kind "pop", "goal" (t popped: the end, with the path) or "skip" (a stale
  // heap entry), and a last "none" frame when the queue empties without t. Every frame has
  // the popped cell and its value (d; left in mode b), the moves checked as [a, b, why,
  // value], the frontier after it (cells in a, [r, c, left, d] in b, [d, r, c] sorted in c)
  // and the values of every cell (a: the distance, b: the most breaks left and in dst the
  // steps of that state, c: the cost; -1 for none).
  const gpTrace = (mode, grid, s, t, diag, k) => {
    const m = grid.length, n = grid[0].length, wall = mode === "c" ? "#" : "1";
    const val = grid.map((row) => [...row].map(() => -1)), dst = grid.map((row) => [...row].map(() => -1));
    const par = new Map(), frames = [];
    const key = (x) => x.join(",");
    const snap = (kind, cell, d, nb, front, left = null, path = null) => frames.push({
      kind, cell, d, left, nb, front, val: val.map((row) => row.slice()), dst: mode === "b" ? dst.map((row) => row.slice()) : null, path,
    });
    const walk = (x, cellOf) => {
      const out = [];
      for (let y = x; y !== null; y = par.get(key(y))) out.push(cellOf(y));
      return out.reverse();
    };
    const isT = (r, c) => r === t[0] && c === t[1];
    if (mode === "a") {
      val[s[0]][s[1]] = 0;
      par.set(key(s), null);
      const q = [[s[0], s[1]]];
      while (q.length) {
        const [r, c] = q.shift();
        if (isT(r, c)) { snap("goal", [r, c], val[r][c], [], q.map((x) => x.slice()), null, walk([r, c], (y) => y.slice())); return frames; }
        const nb = [];
        gpMoves(grid, r, c, diag, wall).forEach(([a, b, , sq]) => {
          if (sq) nb.push([a, b, "squeeze", null]);
          else if (grid[a][b] !== "0") nb.push([a, b, "wall", null]);
          else if (val[a][b] >= 0) nb.push([a, b, "seen", val[a][b]]);
          else { val[a][b] = val[r][c] + 1; par.set(key([a, b]), [r, c]); q.push([a, b]); nb.push([a, b, "push", val[a][b]]); }
        });
        snap("pop", [r, c], val[r][c], nb, q.map((x) => x.slice()));
      }
    } else if (mode === "b") {
      val[s[0]][s[1]] = k;
      dst[s[0]][s[1]] = 0;
      par.set(key([s[0], s[1], k]), null);
      const q = [[s[0], s[1], k, 0]];
      while (q.length) {
        const [r, c, left, d] = q.shift();
        if (isT(r, c)) { snap("goal", [r, c], d, [], q.map((x) => x.slice()), left, walk([r, c, left], (y) => y.slice(0, 2))); return frames; }
        const nb = [];
        gpMoves(grid, r, c, diag, wall).forEach(([a, b, , sq]) => {
          const rest = left - (grid[a][b] === "1" ? 1 : 0);
          if (sq) nb.push([a, b, "squeeze", null]);
          else if (rest < 0) nb.push([a, b, "nobreak", rest]);
          else if (rest <= val[a][b]) nb.push([a, b, "worse", rest]);
          else {
            val[a][b] = rest;
            dst[a][b] = d + 1;
            par.set(key([a, b, rest]), [r, c, left]);
            q.push([a, b, rest, d + 1]);
            nb.push([a, b, "push", rest]);
          }
        });
        snap("pop", [r, c], d, nb, q.map((x) => x.slice()), left);
      }
    } else {
      val[s[0]][s[1]] = 0;
      par.set(key(s), null);
      const heap = [[0, s[0], s[1]]];
      const less = (x, y) => x[0] < y[0] || (x[0] === y[0] && (x[1] < y[1] || (x[1] === y[1] && x[2] < y[2])));
      const push = (e) => { let i = 0; while (i < heap.length && less(heap[i], e)) i++; heap.splice(i, 0, e); };
      while (heap.length) {
        const [d, r, c] = heap.shift();
        if (d > val[r][c]) { snap("skip", [r, c], d, [], heap.map((x) => x.slice())); continue; }
        if (isT(r, c)) { snap("goal", [r, c], d, [], heap.map((x) => x.slice()), null, walk([r, c], (y) => y.slice())); return frames; }
        const nb = [];
        gpMoves(grid, r, c, diag, wall).forEach(([a, b, , sq]) => {
          if (sq) { nb.push([a, b, "squeeze", null]); return; }
          if (grid[a][b] === "#") { nb.push([a, b, "wall", null]); return; }
          const nd = d + Number(grid[a][b]);
          if (val[a][b] < 0 || nd < val[a][b]) { val[a][b] = nd; par.set(key([a, b]), [r, c]); push([nd, a, b]); nb.push([a, b, "push", nd]); }
          else nb.push([a, b, "noimp", nd]);
        });
        snap("pop", [r, c], d, nb, heap.map((x) => x.slice()));
      }
    }
    snap("none", null, -1, [], []);
    return frames;
  };
  const gpAnswer = (frames) => (frames[frames.length - 1].kind === "goal" ? frames[frames.length - 1].d : -1);
  // A random grid from the seeded generator: walls at about 30% (a, b), or terrain (c):
  // road half of the time, mud, mountain and a few walls; S and T stay open.
  const gpRandom = (rng, mode, m, n, s, t) => Array.from({ length: m }, (_, r) => Array.from({ length: n }, (_, c) => {
    const x = rng();
    const keep = (r === s[0] && c === s[1]) || (r === t[0] && c === t[1]);
    if (mode !== "c") return x < 0.3 && !keep ? "1" : "0";
    if (x < 0.06 && !keep) return "#";
    if (x < 0.55) return "1";
    if (x < 0.8) return String(4 + Math.floor(rng() * 3));
    return String(7 + Math.floor(rng() * 3));
  }).join(""));
  const gpParse = (text, mode) => {
    const ok = mode === "c" ? /^[1-9#]+(\.[1-9#]+)*$/ : /^[01]+(\.[01]+)*$/;
    if (!ok.test(text)) return null;
    const rows = text.split(".");
    if (rows.length < MINS || rows.length > MAXS || rows[0].length < MINS || rows[0].length > MAXS || rows.some((r) => r.length !== rows[0].length)) return null;
    return rows;
  };
  const cellOf = (text) => { const m = /^(\d+),(\d+)$/.exec(text || ""); return m ? [Number(m[1]), Number(m[2])] : null; };

  // --- the box ----------------------------------------------------------------------------------
  const MODES = {
    a: { code: "shortest_path", wall: "1", open: "0", queue: "התור" },
    b: { code: "shortest_with_breaks", wall: "1", open: "0", queue: "התור" },
    c: { code: "cheapest_path", wall: "#", open: "1", queue: "הערימה" },
  };
  const STEPS = {
    a: ["מתחילים מ-S", "מוציאים מראש התור", `השכנים${NB}: מרחק + 1, הורה, לתור`, `תור ריק${NB}: −1`, "המסלול מההורים"],
    b: [`מתחילים${NB}: (S, k, 0)`, "מוציאים מראש התור", `השכנים${NB}: ℓ′`, "רק מצב טוב יותר נכנס", `תור ריק${NB}: −1`],
    c: [`מתחילים${NB}: cost[S] = 0`, "מוציאים את הקטן", "היעד", "משחררים", `ערימה ריקה${NB}: −1`],
  };
  const R = (a, b) => Array.from({ length: b - a + 1 }, (_, i) => a + i);
  // the lines of the page's code for every kind of frame, per mode
  const LINES = {
    a: {
      init: { py: R(23, 27), sv: R(22, 32) }, pop: { py: [28, 29, 30, 32, 33], sv: R(33, 39) }, push: { py: R(34, 36), sv: R(40, 42) },
      goal: { py: [29, 30, 31, 37, ...R(39, 43)], sv: [34, 35, ...R(46, 54)] }, none: { py: [37, 38], sv: [46, 47] },
    },
    b: {
      init: { py: R(5, 8), sv: R(7, 16) }, pop: { py: [9, 10, 11, 13, 14, 15], sv: R(17, 23) }, push: { py: [16, 17], sv: [24, 25] },
      goal: { py: [10, 11, 12], sv: [18, 19] }, none: { py: [18], sv: [29] },
    },
    c: {
      init: { py: R(7, 11), sv: R(6, 15) }, pop: { py: [12, 13, 14, 16, 18, 19], sv: R(16, 25) }, push: { py: [20, 21], sv: R(26, 29) },
      skip: { py: [13, 14, 15], sv: [17, 18] }, goal: { py: [13, 14, 16, 17], sv: [17, 18, 19] }, none: { py: [22], sv: [33] },
    },
  };
  const LIT = {
    a: { init: [1], pop: [2, 3], goal: [2, 5], none: [4] },
    b: { init: [1], pop: [2, 3, 4], goal: [2], none: [5] },
    c: { init: [1], pop: [2, 4], skip: [2], goal: [2, 3], none: [5] },
  };
  const P = (r, c) => ltr(`(${r}, ${c})`);
  const walls = (n) => (n === 1 ? "קיר אחד" : `${ltr(n)} קירות`);

  const gridpathView = () => ({
    mount(box) {
      const mode = MODES[box.dataset.mode] ? box.dataset.mode : "a", M = MODES[mode];
      const grid0 = gpParse(box.dataset.grid || "", mode) || Array.from({ length: 6 }, () => M.open.repeat(6));
      const fit = (x, g, dflt) => (x && x[0] < g.length && x[1] < g[0].length && g[x[0]][x[1]] !== M.wall ? x : dflt);
      const s0 = fit(cellOf(box.dataset.s), grid0, [0, 0]);
      const t0 = fit(cellOf(box.dataset.t), grid0, [grid0.length - 1, grid0[0].length - 1]);
      const k0 = Math.min(KMAX, Math.max(0, Number(box.dataset.k) || 0)), diag0 = box.dataset.diag === "1";
      const st = { grid: grid0.slice(), s: s0.slice(), t: t0.slice(), k: k0, diag: diag0, brush: "#", s_: 0, focus: [0, 0] };
      const still = typeof navigator !== "undefined" && navigator.webdriver === true;
      box.classList.add(`gp-is-${mode}`);
      if (still) box.classList.add("gp-still");
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>כיוונים <select class="gp-dirs" aria-label="ארבעה או שמונה כיוונים"><option value="4">ארבעה</option><option value="8">שמונה</option></select></label>` +
        (mode === "b" ? `<label><span>k</span> <input type="number" class="ex-num gp-k" min="0" max="${KMAX}" step="1" dir="ltr" aria-label="מספר הקירות שמותר לשבור, 0 עד ${KMAX}"></label>` : "") +
        `<label>שורות <input type="number" class="ex-num gp-rows" min="${MINS}" max="${MAXS}" step="1" dir="ltr" aria-label="מספר השורות, ${MINS} עד ${MAXS}"></label>` +
        `<label>עמודות <input type="number" class="ex-num gp-cols" min="${MINS}" max="${MAXS}" step="1" dir="ltr" aria-label="מספר העמודות, ${MINS} עד ${MAXS}"></label>` +
        (mode === "c" ? `<label>מברשת <select class="gp-brush" data-nolink aria-label="מה לחיצה על תא צובעת">` +
          `<option value="#">קיר</option>${R(1, 9).map((v) => `<option value="${v}">${v}${v === 1 ? " כביש" : v === 5 ? " בוץ" : v === 9 ? " הר" : ""}</option>`).join("")}</select></label>` : "") +
        `<button type="button" class="md-button gp-rand">אקראי</button><span class="gp-anchor"></span>` +
        `<button type="button" class="md-button gp-clear">ניקוי</button>` +
        `<button type="button" class="md-button ex-reset">חזרה ללוח של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(600, 250, 80) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary gp-sum" aria-live="polite"></p>` +
        `<p class="gp-edit-hint">${mode === "c" ? "לחיצה או גרירה על תאים צובעת אותם במברשת" : "לחיצה או גרירה על תאים מציירת קירות או מוחקת אותם"}, ו-S ו-T נגררים למקום אחר. במקלדת${NB}: חיצים בין התאים, רווח צובע, S או T מעבירים לשם את ההתחלה או את היעד.</p>` +
        `<figure class="gp-panel"><div class="gp-wrap"><div class="gp-grid" role="grid" dir="ltr" data-edits aria-label="הלוח${NB}: לחיצה או גרירה צובעת תאים"></div>` +
        `<svg class="gp-over" aria-hidden="true" preserveAspectRatio="none"><polyline class="gp-line" points=""/></svg></div></figure>` +
        `<span class="viz-legend"><span><i class="gx-key-s"></i>S ההתחלה, T היעד</span>` +
        (mode === "c" ? `<span><i class="gx-key gx-t1"></i>כביש</span><span><i class="gx-key gx-t2"></i>בוץ</span><span><i class="gx-key gx-t3"></i>הר</span>` : "") +
        `<span><i class="gx-key is-wall"></i>קיר</span>${mode === "b" ? `<span><i class="gx-key is-broken"></i>קיר שנכנסו אליו (נשבר)</span>` : ""}` +
        `<span><i class="gp-key-front"></i>ב${M.queue}</span><span><i class="gp-key-done"></i>יצא מ${M.queue}</span>` +
        `<span><i class="gp-key-cur"></i>יוצא עכשיו</span><span><i class="gp-key-new"></i>נכנס בצעד הזה</span><span><i class="gx-key-path"></i>המסלול</span></span>` +
        `<p class="gp-note"></p><p class="gp-front"></p>`;
      const show = explain(box, "הסבר : השלבים של הפתרון והקוד".replace(" :", `${NB}:`));
      answer(box, NB); answer(box, null);                 // the answer line keeps its place from the first step
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), gin = $(".gp-grid"), line = $(".gp-line"), over = $(".gp-over");
      let F = [];
      const retrace = () => { F = gpTrace(mode, st.grid, st.s, st.t, st.diag, st.k); };
      const isS = (r, c) => st.s[0] === r && st.s[1] === c, isT = (r, c) => st.t[0] === r && st.t[1] === c;
      const tag = (r, c) => (isS(r, c) ? "S" : isT(r, c) ? "T" : "");

      const draw = () => {
        const m = st.grid.length, n = st.grid[0].length, N = F.length;
        st.s_ = Math.min(Math.max(st.s_, 0), N);
        const e = st.s_ ? F[st.s_ - 1] : null, done = st.s_ === N;
        $(".gp-dirs").value = st.diag ? "8" : "4";
        if ($(".gp-k")) $(".gp-k").value = String(st.k);
        $(".gp-rows").value = String(m); $(".gp-cols").value = String(n);
        if ($(".gp-brush")) $(".gp-brush").value = st.brush;
        $(".ex-pos").textContent = `צעד ${st.s_} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s_ === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        // the cells: popped so far, the frontier, the current one and its moves
        const val = e ? e.val : st.grid.map((row, r) => [...row].map((_, c) => (isS(r, c) ? (mode === "b" ? st.k : 0) : -1)));
        const dstM = e ? e.dst : null;
        const popped = new Set();
        for (let i = 0; i < st.s_; i++) if (F[i].cell && F[i].kind !== "skip") popped.add(F[i].cell.join(","));
        const front = new Set((e ? e.front : [mode === "c" ? [0, ...st.s] : st.s.slice()]).map((x) => (mode === "c" ? `${x[1]},${x[2]}` : `${x[0]},${x[1]}`)));
        const moved = new Map((e ? e.nb : []).map(([a, b, why]) => [`${a},${b}`, why]));
        const cur = e && e.cell ? e.cell.join(",") : "";
        const onPath = new Set(done && e && e.path ? e.path.map((x) => x.join(",")) : []);
        const had = box.contains(document.activeElement) && document.activeElement.classList.contains("gp-cell");
        let g = "";
        for (let r = 0; r < m; r++) {
          g += `<div role="row" class="gp-r">`;
          for (let c = 0; c < n; c++) {
            const ch = st.grid[r][c], key = `${r},${c}`, isWall = ch === M.wall, v = val[r][c], tg = tag(r, c);
            let cls = isWall ? (mode === "b" && v >= 0 ? " is-broken" : " is-wall") : " is-open";
            if (mode === "c" && !isWall) cls += ` gx-t${Math.floor((Number(ch) - 1) / 3) + 1}`;
            if (popped.has(key)) cls += " is-done";
            else if (front.has(key)) cls += " is-front";
            if (key === cur) cls += " is-cur";
            const why = moved.get(key);
            if (why === "push") cls += " is-new";
            else if (why) cls += " is-chk";
            if (onPath.has(key)) cls += " is-path";
            const shown = v < 0 ? "" : mode === "b" ? dstM ? dstM[r][c] : 0 : v;
            const corner = mode === "c" && !isWall ? ch : mode === "b" && v >= 0 ? v : "";
            const what = (isWall ? (mode === "b" && v >= 0 ? "קיר שנשבר" : "קיר") : mode === "c" ? `עלות כניסה ${ch}` : "פתוח") +
              (tg === "S" ? ", ההתחלה" : tg === "T" ? ", היעד" : "") +
              (v >= 0 ? (mode === "c" ? `, העלות עד כאן ${v}` : mode === "b" ? `, ${shown} צעדים, נשארו ${v} שבירות` : `, מרחק ${v}`) : "");
            const f = st.focus[0] === r && st.focus[1] === c;
            g += `<div role="gridcell" class="gp-cell${cls}" data-r="${r}" data-c="${c}"${tg ? ` data-tag="${tg}"` : ""} tabindex="${f ? 0 : -1}"><span class="gp-sr">שורה ${r}, עמודה ${c}${NB}: ${what}</span>` +
              (tg ? `<span class="gp-tag" aria-hidden="true">${tg}</span>` : "") + (corner !== "" ? `<span class="gp-corner" aria-hidden="true">${corner}</span>` : "") +
              `<span class="gp-v" aria-hidden="true">${shown}</span></div>`;
          }
          g += `</div>`;
        }
        gin.style.setProperty("--n", n);
        $(".gp-wrap").style.setProperty("--n", n);
        gin.innerHTML = g;
        if (had) { const fo = gin.querySelector('[tabindex="0"]'); if (fo) fo.focus({ preventScroll: true }); }
        over.setAttribute("viewBox", `0 0 ${n} ${m}`);
        line.setAttribute("points", onPath.size ? e.path.map(([r, c]) => `${c + 0.5},${r + 0.5}`).join(" ") : "");
        // the summary, the caption of the step, the queue or the heap
        const dirs = st.diag ? "שמונה כיוונים" : "ארבעה כיוונים", Q = M.queue;
        let sum, note, kind = e ? e.kind : "init", vars, ans = null;
        const lines = { py: [], sv: [] };
        const add = (part) => { lines.py.push(...part.py); lines.sv.push(...part.sv); };
        add(LINES[mode][kind]);
        if (!e) {
          sum = `לוח ${ltr(`${m} × ${n}`)}, ${dirs}${mode === "b" ? `, ${ltr(`k = ${st.k}`)}` : ""}. כל צעד מוציא ${mode === "c" ? "רשומה אחת מהערימה" : "מצב אחד מהתור"}.`;
          note = `${Q} מחזיק${mode === "c" ? "ה" : ""} את ההתחלה ${P(...st.s)}${mode === "b" ? ` עם ${ltr(st.k)} שבירות` : ""}, ${mode === "c" ? "בעלות 0 : העלות של S לא משולמת" : "במרחק 0"}. "הצעד הבא" מוציא אותה ובודק את השכנים.`.replace(" :", `${NB}:`);
          vars = mode === "a" ? [ltr(`dist[S] = 0`), ltr(`q = [(${st.s})]`)] : mode === "b" ? [ltr(`best[S] = ${st.k}`), ltr(`q = [(${st.s},${st.k},0)]`)] : [ltr("cost[S] = 0"), ltr(`heap = [(0,${st.s})]`)];
        } else if (kind === "none") {
          sum = `${Q} התרוקן${mode === "c" ? "ה" : ""} לפני ש-T יצא${NB}: אין מסלול.`;
          note = `אף תא שעוד לא יצא אינו מגיע ל-T${mode === "b" ? ` גם עם ${ltr(st.k)} שבירות` : ""}${mode === "c" ? " בלי לעבור בקיר" : ""}. התשובה ${ltr("−1")}.`;
          vars = [ltr(mode === "c" ? "heap = []" : "q = []")];
          ans = `אין מסלול${NB}: ${ltr("−1")}.`;
        } else {
          const [r, c] = e.cell, word = mode === "c" ? "בעלות" : "במרחק";
          const stateTxt = mode === "b" ? ltr(`(${r},${c},${e.left},${e.d})`) : mode === "c" ? ltr(`(${e.d}, ${r}, ${c})`) : P(r, c);
          if (kind === "goal") {
            const steps = e.path.length - 1, broken = mode === "b" ? e.path.filter(([a, b]) => st.grid[a][b] === "1").length : 0;
            sum = `T יצא מ${Q} ${word} ${ltr(e.d)}${NB}: ${mode === "c" ? `העלות הקטנה ביותר, במסלול של ${ltr(steps)} צעדים` : `המסלול הקצר הוא ${ltr(e.d)} צעדים`}.`;
            note = `${stateTxt} יוצא מ${Q} והוא היעד, ולכן ${mode === "c" ? "העלות" : "המרחק"} שלו סופי${mode === "c" ? "ת" : ""}. המסלול נבנה מההורים${NB}: מ-T אחורה עד S, ${ltr(e.path.length)} תאים.` +
              (mode === "b" ? ` ${broken ? `הוא שובר ${walls(broken)}${NB}: ${e.path.filter(([a, b]) => st.grid[a][b] === "1").map(([a, b]) => P(a, b)).join(", ")}` : "הוא לא שובר אף קיר"}, ונשארו ${ltr(e.left)} שבירות.` : "");
            ans = mode === "c" ? `עלות ${ltr(e.d)}, במסלול של ${ltr(steps)} צעדים.` :
              mode === "b" ? `${ltr(e.d)} צעדים, ${broken ? `שוברים ${walls(broken)}` : "בלי לשבור קיר"}.` : `${ltr(e.d)} צעדים מ-S ל-T.`;
            vars = [stateTxt, ltr(`${mode === "c" ? "cost" : mode === "b" ? "d" : "dist"}[T] = ${e.d}`), ltr(`path: ${e.path.length} cells`)];
          } else if (kind === "skip") {
            sum = `צעד ${ltr(st.s_)}${NB}: רשומה ישנה של ${P(r, c)}, מדלגים.`;
            note = `${stateTxt} יוצאת מהערימה, אבל ${P(r, c)} כבר יצא בעלות ${ltr(e.val[r][c])}, קטנה יותר. מדלגים.`;
            vars = [stateTxt, ltr(`cost = ${e.val[r][c]}`)];
          } else {
            const pushed = e.nb.filter((x) => x[2] === "push");
            if (pushed.length) add(LINES[mode].push);
            sum = `צעד ${ltr(st.s_)}${NB}: ${P(r, c)} יוצא מ${Q} ${word} ${ltr(e.d)}${mode === "b" ? `, נשארו ${ltr(e.left)} שבירות` : ""}. נכנסו ${ltr(pushed.length)}.`;
            const say = ([a, b, why, v]) => {
              const k = DIRS.findIndex(([dr, dc]) => r + dr === a && c + dc === b);
              const what = {
                squeeze: "אלכסון בין שני קירות, אסור",
                wall: "קיר",
                seen: `כבר יש לו מרחק ${ltr(v)}`,
                push: mode === "a" ? `<b>מרחק ${ltr(v)}, נכנס לתור</b>` : mode === "b" ? `<b>נכנס עם ${ltr(v)} שבירות</b>` : `<b>עלות ${ltr(v)}, נכנס לערימה</b>`,
                nobreak: "קיר, ואין שבירות",
                worse: `${ltr(v)} שבירות, לא יותר מ-${ltr(e.val[a][b])} שכבר נראו`,
                noimp: `${ltr(`${e.d} + ${st.grid[a][b]} = ${v}`)}, לא פחות מ-${ltr(e.val[a][b])}`,
              }[why];
              return `${DIR_HEB[k]} ${P(a, b)}${NB}: ${what}`;
            };
            note = `${stateTxt} יוצא מראש ${Q}. ${e.nb.length ? e.nb.map(say).join("; ") : "אין לו שכנים בתוך הלוח"}.` +
              (e.front.length ? "" : ` ${Q} ריק${mode === "c" ? "ה" : ""} עכשיו.`);
            vars = mode === "a" ? [ltr(`(r, c) = (${r}, ${c})`), ltr(`dist = ${e.d}`), ltr(`len(q) = ${e.front.length}`)]
              : mode === "b" ? [ltr(`(r, c, left, d) = (${r}, ${c}, ${e.left}, ${e.d})`), ltr(`len(q) = ${e.front.length}`)]
                : [ltr(`(d, r, c) = (${e.d}, ${r}, ${c})`), ltr(`len(heap) = ${e.front.length}`)];
          }
        }
        $(".gp-sum").innerHTML = sum;
        $(".gp-note").innerHTML = note;
        const items = e ? e.front : [mode === "c" ? [0, ...st.s] : mode === "b" ? [...st.s, st.k, 0] : st.s.slice()];
        const fmt = (x) => (mode === "c" ? `(${x[1]},${x[2]})=${x[0]}` : mode === "b" ? `(${x.join(",")})` : `(${x.join(",")})`);
        $(".gp-front").innerHTML = `${Q}${mode === "c" ? ", הקטן משמאל" : ", הראש משמאל"}${NB}: ` + (items.length
          ? ltr(items.slice(0, LIST_MAX).map(fmt).join(" ")) + (items.length > LIST_MAX ? ` ועוד ${ltr(items.length - LIST_MAX)}` : "")
          : "ריק") + ` · יצאו עד עכשיו${NB}: ${ltr(popped.size)} תאים.`;
        show({ code: M.code, steps: STEPS[mode], lit: LIT[mode][kind], lines, vars: vars.join(" · ") });
        answer(box, ans, '.gp-grid .gp-cell[data-tag="T"].is-path');
      };

      const total = () => F.length;
      const stop = autoplay(play, speed, { step: () => { st.s_++; draw(); }, done: () => st.s_ >= total(), restart: () => { st.s_ = 0; draw(); } });
      const edited = () => { stop(); retrace(); st.s_ = 0; draw(); };
      $(".gp-dirs").addEventListener("change", () => { st.diag = $(".gp-dirs").value === "8"; edited(); });
      if ($(".gp-k")) $(".gp-k").addEventListener("change", () => {
        const v = Math.round(Number($(".gp-k").value));
        st.k = Number.isFinite(v) ? Math.min(KMAX, Math.max(0, v)) : st.k;
        edited();
      });
      if ($(".gp-brush")) $(".gp-brush").addEventListener("change", () => { st.brush = $(".gp-brush").value; });
      // the size: cells kept where they were, new ones open; S and T kept inside, apart
      const place = (x, other) => {
        const m = st.grid.length, n = st.grid[0].length;
        let [r, c] = [Math.min(x[0], m - 1), Math.min(x[1], n - 1)];
        if (r === other[0] && c === other[1]) c = c > 0 ? c - 1 : c + 1;
        const row = st.grid[r];
        if (row[c] === M.wall) st.grid[r] = row.slice(0, c) + M.open + row.slice(c + 1);
        return [r, c];
      };
      const resize = () => {
        const clamp = (el, was) => { const v = Math.round(Number(el.value)); return Number.isFinite(v) && v > 0 ? Math.min(MAXS, Math.max(MINS, v)) : was; };
        const m = clamp($(".gp-rows"), st.grid.length), n = clamp($(".gp-cols"), st.grid[0].length);
        st.grid = Array.from({ length: m }, (_, r) => Array.from({ length: n }, (_, c) => (st.grid[r] && st.grid[r][c]) || M.open).join(""));
        st.t = place(st.t, [-1, -1]);
        st.s = place(st.s, st.t);
        st.focus = [Math.min(st.focus[0], m - 1), Math.min(st.focus[1], n - 1)];
        edited();
      };
      $(".gp-rows").addEventListener("change", resize);
      $(".gp-cols").addEventListener("change", resize);
      const seed = seedControls(box, $(".gp-anchor"), (rng) => {
        st.grid = gpRandom(rng, mode, st.grid.length, st.grid[0].length, st.s, st.t);
        edited();
      });
      $(".gp-rand").addEventListener("click", () => seed.draw());
      $(".gp-clear").addEventListener("click", () => { st.grid = st.grid.map((row) => M.open.repeat(row.length)); edited(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.s_ = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s_--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s_++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s_ = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => {
        st.grid = grid0.slice(); st.s = s0.slice(); st.t = t0.slice(); st.k = k0; st.diag = diag0; st.focus = [0, 0];
        edited();
      });
      // editing the grid: a press on S or T drags it, a press elsewhere paints (a, b: the
      // pressed cell's opposite, c: the brush) and a drag goes on painting; one redraw per cell
      const setCell = (r, c, ch) => {
        if (tag(r, c) || st.grid[r][c] === ch) return false;
        st.grid[r] = st.grid[r].slice(0, c) + ch + st.grid[r].slice(c + 1);
        return true;
      };
      const paintOf = (r, c) => (mode === "c" ? st.brush : st.grid[r][c] === M.wall ? M.open : M.wall);
      let drag = null;
      const cellAt = (ev) => {
        const el = document.elementFromPoint(ev.clientX, ev.clientY);
        const cell = el && el.closest && el.closest(".gp-cell");
        return cell && gin.contains(cell) ? [Number(cell.dataset.r), Number(cell.dataset.c)] : null;
      };
      const apply = (r, c) => {
        if (!drag) return;
        if (drag.move) {
          const other = drag.move === "s" ? st.t : st.s, here = drag.move === "s" ? st.s : st.t;
          if ((r === here[0] && c === here[1]) || (r === other[0] && c === other[1]) || st.grid[r][c] === M.wall) return;
          if (drag.move === "s") st.s = [r, c]; else st.t = [r, c];
          edited();
        } else if (setCell(r, c, drag.paint)) edited();
      };
      gin.addEventListener("pointerdown", (ev) => {
        const at = cellAt(ev);
        if (!at || (ev.pointerType === "mouse" && ev.button !== 0)) return;
        ev.preventDefault();
        const [r, c] = at, tg = tag(r, c);
        st.focus = [r, c];
        drag = tg ? { move: tg.toLowerCase(), id: ev.pointerId } : { paint: paintOf(r, c), id: ev.pointerId };
        try { gin.setPointerCapture(ev.pointerId); } catch (err) { /* a synthetic event */ }
        if (!tg) apply(r, c); else draw();
      });
      gin.addEventListener("pointermove", (ev) => {
        if (!drag || ev.pointerId !== drag.id) return;
        const at = cellAt(ev);
        if (at) apply(...at);
      });
      const end = () => { drag = null; };
      gin.addEventListener("pointerup", end);
      gin.addEventListener("pointercancel", end);
      gin.addEventListener("lostpointercapture", end);
      // the keyboard: the arrows move between the cells, space or Enter paints, S and T move
      // the start or the target (the box's own arrows step the run, so the keys stop here)
      gin.addEventListener("keydown", (ev) => {
        const el = ev.target.closest(".gp-cell");
        if (!el) return;
        const m = st.grid.length, n = st.grid[0].length, r = Number(el.dataset.r), c = Number(el.dataset.c);
        const mv = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[ev.key];
        const key = ev.key.toLowerCase();
        if (mv) {
          st.focus = [Math.min(m - 1, Math.max(0, r + mv[0])), Math.min(n - 1, Math.max(0, c + mv[1]))];
          draw();
          const fo = gin.querySelector('[tabindex="0"]');
          if (fo) fo.focus({ preventScroll: false });
        } else if (ev.key === " " || ev.key === "Enter") {
          if (setCell(r, c, paintOf(r, c))) edited();
        } else if ((key === "s" || key === "t") && st.grid[r][c] !== M.wall && !tag(r, c)) {
          if (key === "s") st.s = [r, c]; else st.t = [r, c];
          edited();
        } else return;
        ev.preventDefault();
        ev.stopPropagation();
      });
      // the link and the remembered state carry the grid, S, T and the step: "rows_3-0_3-8_12"
      box.dvqExtra = {
        get: () => `${st.grid.join(".")}_${st.s.join("-")}_${st.t.join("-")}${st.s_ ? `_${st.s_}` : ""}`,
        set: (text) => {
          const mm = /^([0-9#.]+)_(\d+)-(\d+)_(\d+)-(\d+)(?:_(\d+))?$/.exec(text), grid = mm && gpParse(mm[1], mode);
          if (!grid) return false;
          const s = [Number(mm[2]), Number(mm[3])], t = [Number(mm[4]), Number(mm[5])];
          const okCell = (x) => x[0] < grid.length && x[1] < grid[0].length && grid[x[0]][x[1]] !== M.wall;
          if (!okCell(s) || !okCell(t) || (s[0] === t[0] && s[1] === t[1])) return false;
          st.grid = grid; st.s = s; st.t = t; st.focus = [0, 0];
          edited();
          st.s_ = mm[6] ? Number(mm[6]) : 0;
          draw();
          return true;
        },
      };
      retrace();
      draw();
    },
  });

  dvqExplorers.register({
    views: { gridpath: gridpathView },
    help: {
      gridpath: "לחיצה או גרירה על תאים מציירת קירות (בסעיף ג : צובעת בעלות של המברשת), ואת S ו-T גוררים למקום אחר; \"אקראי\" מגריל לוח, \"ניקוי\" מנקה אותו, ובוחרים ארבעה או שמונה כיוונים (ובסעיף ב את k). כל צעד מוציא תא אחד מהתור (בסעיף ג מהערימה) : הוא מוקף, השכנים שנבדקו מסומנים, מה שבתור צבוע, ובכל תא שכבר הגיעו אליו כתוב המרחק שלו (בסעיף ב גם השבירות שנשארו, בפינה; בסעיף ג העלות). בסוף המסלול מצויר כקו. השורה שמתחת ללוח מסבירה כל צעד, והפאנל 'הסבר' מדליק את שורות הקוד.".replace(/ :/g, "\u00a0:"),
    },
    models: { gpMoves, gpTrace, gpAnswer, gpRandom, gpParse },
  });
})();
