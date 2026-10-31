// kinds: islands
//   islands                0065        a grid of land and water (data-grid, rows of 0 and 1 joined by dots) edited by a tap on a cell or drawn from a seed; the flood fill of the page's code stepped one cell at a time: a new island when the scan meets land not marked yet, a cell leaving the queue with its neighbours checked and the land ones pushed; four or eight neighbours by a select; every island in its own colour with its number (modes a and b) or its running size (mode c, with the sorted list under the grid); the queue drawn beside the grid, a caption per step and the explain panel with the code lines of the step
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, explain, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const MAXR = 8, MAXC = 10;
  const DIRS4 = [[-1, 0], [1, 0], [0, -1], [0, 1]];
  const DIRS8 = [...DIRS4, [-1, -1], [-1, 1], [1, -1], [1, 1]];
  const DIR_HEB = ["למעלה", "למטה", "שמאלה", "ימינה", "למעלה-שמאלה", "למעלה-ימינה", "למטה-שמאלה", "למטה-ימינה"];

  // The flood fill frame by frame, as tools/figures/q0065.py trace(): a "start" frame when
  // the scan meets a land cell not marked yet (a new island, the cell pushed), a "pop" frame
  // for every cell that leaves the queue (its neighbours checked in the order of the
  // directions, the land cells not marked yet pushed and marked), and an "end" frame when
  // the scan is over. Every frame carries the queue after it, the island label of every cell
  // (0 for water or not reached yet), the count and the sizes so far (the running island last).
  const ilTrace = (grid, diag) => {
    const m = grid.length, n = m ? grid[0].length : 0, dirs = diag ? DIRS8 : DIRS4;
    const labels = grid.map((row) => row.map(() => 0));
    const frames = [], sizes = [];
    let skipped = 0, count = 0;
    const snap = (kind, more) => frames.push({ kind, count, sizes: sizes.slice(), labels: labels.map((row) => row.slice()), ...more });
    for (let r = 0; r < m; r++) {
      for (let c = 0; c < n; c++) {
        if (!grid[r][c] || labels[r][c]) { skipped++; continue; }
        count++;
        labels[r][c] = count;
        sizes.push(0);
        const q = [[r, c]];
        snap("start", { cell: [r, c], isle: count, skipped, q: [[r, c]], pushed: [[r, c]], nb: [] });
        skipped = 0;
        while (q.length) {
          const [i, j] = q.shift();
          sizes[sizes.length - 1]++;
          const nb = [], pushed = [];
          dirs.forEach(([di, dj], k) => {
            const a = i + di, b = j + dj;
            let why;
            if (!(a >= 0 && a < m && b >= 0 && b < n)) why = "out";
            else if (!grid[a][b]) why = "water";
            else if (labels[a][b]) why = "seen";
            else { why = "push"; labels[a][b] = count; q.push([a, b]); pushed.push([a, b]); }
            nb.push([a, b, why, k]);
          });
          snap("pop", { cell: [i, j], isle: count, q: q.map((x) => x.slice()), pushed, nb, skipped: 0 });
        }
      }
    }
    snap("end", { cell: null, isle: count, skipped, q: [], pushed: [], nb: [] });
    return frames;
  };
  const ilSizes = (grid, diag) => ilTrace(grid, diag)[ilTrace(grid, diag).length - 1].sizes.slice().sort((a, b) => b - a);
  const ilParse = (text) => {
    if (!/^[01]+(\.[01]+)*$/.test(text)) return null;
    const rows = text.split(".");
    if (rows.length > MAXR || rows[0].length > MAXC || rows.some((r) => r.length !== rows[0].length)) return null;
    return rows.map((r) => [...r].map(Number));
  };
  const ilText = (grid) => grid.map((r) => r.join("")).join(".");

  const MODES = {
    a: { label: "כמה איים, ארבעה כיוונים (סעיף א)", code: "count_islands", diag: false },
    b: { label: "כמה איים, שמונה כיוונים (סעיף ב)", code: "count_islands8", diag: true },
    c: { label: "הגודל של כל אי (סעיף ג)", code: "island_sizes", diag: false },
  };
  const STEPS = {
    a: ["הסריקה : תא אחרי תא", "אי חדש : המונה גדל, התא לתור", "ההצפה : תא יוצא, שכנים נכנסים", "האי נגמר : התור ריק", "הסוף : count"],
    c: ["הסריקה : תא אחרי תא", "אי חדש : הצפה", "ההצפה סופרת : size גדל", "הגודל לרשימה", "המיון בסוף"],
  };
  STEPS.b = STEPS.a;
  // the lines of the page's code: the scan of each mode's function, and the flood of part a
  const SCAN = {
    a: { init: { py: [27, 28, 29], sv: [29, 30, 31, 32] }, start: { py: [30, 31, 32, 33, 34, 10, 11], sv: [33, 34, 35, 36, 37, 10, 11] }, end: { py: [35], sv: [39] } },
    b: { init: { py: [7, 8, 9], sv: [7, 8, 9, 10] }, start: { py: [10, 11, 12, 13, 14], sv: [11, 12, 13, 14, 15] }, end: { py: [15], sv: [17] } },
    c: { init: { py: [4, 5, 6, 7], sv: [4, 5, 6, 7, 8] }, start: { py: [8, 9, 10, 11], sv: [9, 10, 11, 12] }, end: { py: [12], sv: [13] } },
  };
  const FLOOD = (pushed, empty) => ({
    py: [13, 14, 15, 16, 17, 18, ...(pushed ? [19, 20] : []), ...(empty ? [21] : [])],
    sv: [12, 13, 14, 15, 16, 17, ...(pushed ? [18, 19] : []), ...(empty ? [23] : [])],
  });
  const P = (r, c) => ltr(`(${r}, ${c})`);
  const list = (cells) => (cells.length ? ltr(`[${cells.map(([r, c]) => `(${r},${c})`).join(" ")}]`) : "ריק");

  const islandsView = () => ({
    mount(box) {
      const mode0 = MODES[box.dataset.mode] ? box.dataset.mode : "a";
      const grid0 = ilParse(box.dataset.grid || "") || [[1, 1, 0], [0, 0, 1], [1, 0, 1]];
      const st = { mode: mode0, diag: MODES[mode0].diag, grid: grid0.map((r) => r.slice()), p: 50, s: 0, focus: [0, 0] };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המצב <select class="il-mode" aria-label="איזה סעיף">${Object.entries(MODES).map(([v, m]) => `<option value="${v}">${m.label}</option>`).join("")}</select></label>` +
        `<label>שכנים <select class="il-dirs" aria-label="ארבעה או שמונה כיוונים"><option value="4">ארבעה כיוונים</option><option value="8">שמונה כיוונים</option></select></label>` +
        `<label>שורות <input type="number" class="ex-num il-m" min="1" max="${MAXR}" step="1" dir="ltr" aria-label="מספר השורות, עד ${MAXR}"></label>` +
        `<label>עמודות <input type="number" class="ex-num il-n" min="1" max="${MAXC}" step="1" dir="ltr" aria-label="מספר העמודות, עד ${MAXC}"></label>` +
        `<label>הסיכוי ליבשה <input type="range" class="il-p" min="10" max="90" step="10" value="50" dir="ltr" aria-label="הסיכוי של תא להיות יבשה בלוח אקראי, באחוזים"><output class="il-po">50%</output></label>` +
        `<button type="button" class="md-button il-rand">לוח אקראי</button><span class="il-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה ללוח של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary il-sum" aria-live="polite"></p>` +
        `<p class="il-edit-hint">לחיצה על תא הופכת אותו ממים ליבשה ובחזרה, ומתחילה את ההצפה מחדש. במקלדת${NB}: חיצים בין התאים, רווח או Enter הופכים תא.</p>` +
        `<div class="il-panels"><figure class="il-panel"><figcaption class="il-cap"></figcaption><div class="il-grid" role="grid" dir="ltr" data-edits aria-label="הלוח : לחיצה על תא הופכת אותו"></div></figure>` +
        `<figure class="il-panel il-qpanel" data-steady><figcaption>התור, הראש משמאל</figcaption><div class="il-queue"></div></figure></div>` +
        `<span class="viz-legend"><span><i class="il-key is-water"></i>מים</span><span><i class="il-key is-land"></i>יבשה שעוד לא הוצפה</span><span><i class="il-key il-i1"></i>אי (צבע ומספר לכל אי)</span>` +
        `<span><i class="il-key-q"></i>בתור</span><span><i class="il-key-cur"></i>התא שיצא מהתור</span><span><i class="il-key-new"></i>נכנס לתור בצעד הזה</span></span>` +
        `<p class="il-note"></p><p class="il-sizes"></p>`;
      const show = explain(box, "הסבר : השלבים של הפתרון והקוד");
      answer(box, NB); answer(box, null);           // the answer line keeps its place from the first step
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), gin = $(".il-grid");
      let F = [];
      const retrace = () => { F = ilTrace(st.grid, st.diag); };

      const draw = () => {
        const m = st.grid.length, n = st.grid[0].length, N = F.length, mo = st.mode, sizesMode = mo === "c";
        st.s = Math.min(Math.max(st.s, 0), N);
        const e = st.s ? F[st.s - 1] : null, done = st.s === N;
        const labels = e ? e.labels : st.grid.map((r) => r.map(() => 0));
        const land = st.grid.reduce((s, r) => s + r.reduce((a, b) => a + b, 0), 0);
        $(".il-mode").value = mo; $(".il-dirs").value = st.diag ? "8" : "4";
        $(".il-m").value = String(m); $(".il-n").value = String(n); $(".il-po").textContent = `${st.p}%`;
        $(".ex-pos").textContent = `צעד ${st.s} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        box.classList.toggle("il-is-c", sizesMode);
        // the grid: every cell by its island, the queue, the current cell and the pushed ones
        const inQ = new Set(e ? e.q.map(([r, c]) => `${r},${c}`) : []);
        const pushed = new Set(e && e.kind !== "end" ? e.pushed.map(([r, c]) => `${r},${c}`) : []);
        const cur = e && e.cell ? e.cell : null;
        const sizeOf = (k) => (e && k >= 1 && k <= e.sizes.length ? e.sizes[k - 1] : 0);
        const had = box.contains(document.activeElement) && document.activeElement.classList.contains("il-cell");
        let g = "";
        for (let r = 0; r < m; r++) {
          g += `<div role="row" class="il-r">`;
          for (let c = 0; c < n; c++) {
            const v = st.grid[r][c], k = labels[r][c], f = st.focus[0] === r && st.focus[1] === c, key = `${r},${c}`;
            const cls = !v ? "" : k ? ` il-i${(k - 1) % 5 + 1} is-isle` : " is-land";
            const txt = !k ? "" : sizesMode ? sizeOf(k) : k;
            const what = !v ? "מים" : k ? `יבשה, אי ${k}${sizesMode ? `, גודל ${sizeOf(k)}` : ""}` : "יבשה שעוד לא הוצפה";
            g += `<div role="gridcell" class="il-cell${cls}${inQ.has(key) ? " is-q" : ""}${pushed.has(key) ? " is-new" : ""}${cur && cur[0] === r && cur[1] === c ? " is-cur" : ""}" ` +
              `style="grid-area:${r + 1} / ${c + 1}" data-r="${r}" data-c="${c}" tabindex="${f ? 0 : -1}" aria-label="שורה ${r}, עמודה ${c}${NB}: ${what}">${txt}</div>`;
          }
          g += `</div>`;
        }
        gin.style.setProperty("--n", n);
        gin.innerHTML = g;
        if (had) { const fo = gin.querySelector('[tabindex="0"]'); if (fo) fo.focus({ preventScroll: true }); }
        $(".il-cap").innerHTML = `הלוח ${ltr(`${m} × ${n}`)}, ${ltr(land)} תאי יבשה`;
        $(".il-queue").innerHTML = e && e.q.length
          ? e.q.map(([r, c], i) => `<span class="il-q${i === 0 ? " is-head" : ""}${pushed.has(`${r},${c}`) ? " is-new" : ""}">(${r},${c})</span>`).join("")
          : `<span class="il-q is-empty">ריק</span>`;
        // the summary, the caption of the step, the sizes line
        const dirsWord = st.diag ? "שמונה כיוונים" : "ארבעה כיוונים";
        let sum, note = "", lit, lines, code = MODES[mo].code, vars, ans = null;
        if (!e) {
          sum = `לוח ${ltr(`${m} × ${n}`)} עם ${ltr(land)} תאי יבשה, ${dirsWord}. כל צעד הוא תא אחד${NB}: אי חדש שנכנס לתור, או תא שיוצא ממנו.`;
          note = land ? `הסריקה מתחילה מ-${P(0, 0)}, שורה אחרי שורה ומשמאל לימין. ${ltr("seen")} ריק, ${ltr("count = 0")}.` : "אין אף תא יבשה, ולכן הסריקה לא תמצא אי.";
          lit = [1]; lines = SCAN[mo].init;
          vars = [ltr("count = 0"), ltr(sizesMode ? "sizes = []" : "q = []")].join(" · ");
        } else if (e.kind === "start") {
          const [r, c] = e.cell;
          sum = `צעד ${ltr(st.s)}${NB}: אי חדש ${ltr(e.isle)} מתחיל ב-${P(r, c)}. איים עד עכשיו${NB}: <b>${ltr(e.count)}</b>.`;
          note = `הסריקה ${e.skipped ? `עברה ${ltr(e.skipped)} תאים (מים, או יבשה שכבר סומנה) ו` : ""}פגשה ב-${P(r, c)} יבשה שלא סומנה${NB}: אף הצפה לא הגיעה לשם, ולכן זה אי חדש. ` +
            (sizesMode ? `מתחילים הצפה ממנו, והגודל שהיא תחזיר ייכנס לרשימה.` : `${ltr(`count ← ${e.count}`)}, התא מסומן ב-${ltr("seen")} ונכנס לתור.`);
          lit = [1, 2]; lines = SCAN[mo].start;
          vars = [ltr(`r = ${r}`), ltr(`c = ${c}`), ltr(`count = ${e.count}`), ltr(`q = [(${r},${c})]`)].join(" · ");
        } else if (e.kind === "pop") {
          const [i, j] = e.cell, size = e.sizes[e.sizes.length - 1], empty = e.q.length === 0;
          sum = `צעד ${ltr(st.s)}${NB}: ${P(i, j)} יוצא מהתור, אי ${ltr(e.isle)}, הגודל עד עכשיו ${ltr(size)}. איים עד עכשיו${NB}: <b>${ltr(e.count)}</b>.`;
          const parts = e.nb.map(([a, b, why, k]) => `${DIR_HEB[k]}${why === "out" ? " מחוץ ללוח" : ` ${P(a, b)} ${{ water: "מים", seen: "כבר סומן", push: "<b>יבשה שלא סומנה : מסומן ונכנס לתור</b>" }[why]}`}`);
          note = `${P(i, j)} יוצא מראש התור, ${ltr(`size ← ${size}`)}. ${e.nb.length} השכנים${NB}: ${parts.join("; ")}.` +
            (empty ? ` התור ריק${NB}: האי ${ltr(e.isle)} שלם, ${ltr(size)} תאים${sizesMode ? `, והגודל נכנס לרשימה` : ""}. הסריקה ממשיכה מהמקום שבו עצרה.` : "");
          lit = [3, ...(empty ? [4] : [])]; lines = FLOOD(e.pushed.length > 0, empty); code = "count_islands";
          vars = [ltr(`(i, j) = (${i}, ${j})`), ltr(`size = ${size}`), `${ltr("q")} = ${list(e.q)}`, ltr(`count = ${e.count}`)].join(" · ");
        } else {
          sum = `הסריקה נגמרה${NB}: <b>${ltr(e.count)}</b> איים, ${dirsWord}.`;
          note = `הסריקה עברה את ${ltr(e.skipped)} התאים האחרונים (מים, או יבשה שכבר סומנה) בלי למצוא אי חדש, ונגמרה. ` +
            (sizesMode ? `הרשימה ממוינת בסדר יורד${NB}: ${ltr(`[${e.sizes.slice().sort((x, y) => y - x).join(", ")}]`)}.` : `${ltr(`count = ${e.count}`)} הוא מספר האיים.`);
          lit = [5]; lines = SCAN[mo].end;
          vars = [ltr(`count = ${e.count}`), ltr(sizesMode ? `sizes = [${e.sizes.join(", ")}]` : "q = []")].join(" · ");
        }
        if (sizesMode) {
          const sz = e ? e.sizes : [], running = e && e.kind !== "end" ? sz.length - 1 : -1;
          const found = sz.map((v, k) => (k === running ? `<b class="is-run">${v}</b>` : String(v))).join(", ");
          const sorted = sz.slice().sort((x, y) => y - x);
          $(".il-sizes").innerHTML = `הגדלים לפי סדר המציאה${NB}: ${ltr(`[${found}]`)}${running >= 0 ? " (האי שמוצף עכשיו מודגש)" : ""} · ממוינים מהגדול לקטן${NB}: ${ltr(`[${sorted.join(", ")}]`)} · סכום${NB}: ${ltr(sorted.reduce((x, y) => x + y, 0))} מתוך ${ltr(land)} תאי יבשה.`;
        } else {
          const marked = labels.reduce((s, r) => s + r.filter(Boolean).length, 0);
          $(".il-sizes").innerHTML = `תאי יבשה שסומנו${NB}: ${ltr(marked)} מתוך ${ltr(land)}. כל תא יבשה נכנס לתור פעם אחת בדיוק, ולכן גם מספר ההכנסות הוא ${ltr(marked)}.`;
        }
        $(".il-sum").innerHTML = sum;
        $(".il-note").innerHTML = note;
        show({ code, steps: STEPS[mo], lit, lines, vars });
        if (done && e) {
          const sorted = e.sizes.slice().sort((x, y) => y - x);
          ans = sizesMode ? `הגדלים מהגדול לקטן${NB}: ${ltr(`[${sorted.join(", ")}]`)}${NB}: ${ltr(e.count)} איים, ${ltr(land)} תאי יבשה.` : `מספר האיים עם ${dirsWord}${NB}: ${ltr(e.count)}.`;
        }
        answer(box, ans, ".il-grid .il-cell.is-isle");
      };

      const total = () => F.length;
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= total(), restart: () => { st.s = 0; draw(); } });
      const edited = () => { stop(); retrace(); st.s = 0; draw(); };
      $(".il-mode").addEventListener("change", () => { st.mode = MODES[$(".il-mode").value] ? $(".il-mode").value : "a"; st.diag = MODES[st.mode].diag; edited(); });
      $(".il-dirs").addEventListener("change", () => { st.diag = $(".il-dirs").value === "8"; edited(); });
      const resize = () => {
        const m = Math.min(MAXR, Math.max(1, Math.round(Number($(".il-m").value)) || 1));
        const n = Math.min(MAXC, Math.max(1, Math.round(Number($(".il-n").value)) || 1));
        st.grid = Array.from({ length: m }, (_, r) => Array.from({ length: n }, (_, c) => (st.grid[r] && st.grid[r][c]) || 0));
        st.focus = [Math.min(st.focus[0], m - 1), Math.min(st.focus[1], n - 1)];
        edited();
      };
      $(".il-m").addEventListener("change", resize);
      $(".il-n").addEventListener("change", resize);
      $(".il-p").addEventListener("input", () => { st.p = Number($(".il-p").value); $(".il-po").textContent = `${st.p}%`; });
      const seed = seedControls(box, $(".il-anchor"), (rng) => {
        const m = st.grid.length, n = st.grid[0].length;
        st.grid = Array.from({ length: m }, () => Array.from({ length: n }, () => (rng() < st.p / 100 ? 1 : 0)));
        edited();
      });
      $(".il-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => { st.grid = grid0.map((r) => r.slice()); st.mode = mode0; st.diag = MODES[mode0].diag; st.p = 50; $(".il-p").value = "50"; st.focus = [0, 0]; edited(); });
      // the grid: a tap toggles a cell; the arrow keys move between the cells, space or
      // Enter toggles (the box's own arrows step the run, so the keys stop here)
      gin.addEventListener("click", (ev) => {
        const el = ev.target.closest(".il-cell");
        if (!el) return;
        const r = Number(el.dataset.r), c = Number(el.dataset.c);
        st.grid[r][c] ^= 1;
        st.focus = [r, c];
        edited();
      });
      gin.addEventListener("keydown", (ev) => {
        const el = ev.target.closest(".il-cell");
        if (!el) return;
        const m = st.grid.length, n = st.grid[0].length, r = Number(el.dataset.r), c = Number(el.dataset.c);
        const move = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[ev.key];
        if (move) {
          ev.preventDefault();
          ev.stopPropagation();
          st.focus = [Math.min(m - 1, Math.max(0, r + move[0])), Math.min(n - 1, Math.max(0, c + move[1]))];
          draw();
          const fo = gin.querySelector('[tabindex="0"]');
          if (fo) fo.focus({ preventScroll: false });
        } else if (ev.key === " " || ev.key === "Enter") {
          ev.preventDefault();
          ev.stopPropagation();
          st.grid[r][c] ^= 1;
          edited();
        }
      });
      // the link and the remembered state carry the grid and the step: "110000.110011-12"
      box.dvqExtra = {
        get: () => `${ilText(st.grid)}${st.s ? `-${st.s}` : ""}`,
        set: (text) => {
          const mm = /^([01.]+)(?:-(\d+))?$/.exec(text), grid = mm && ilParse(mm[1]);
          if (!grid) return false;
          st.grid = grid;
          st.focus = [0, 0];
          edited();
          st.s = mm[2] ? Number(mm[2]) : 0;
          draw();
          return true;
        },
      };
      retrace();
      draw();
    },
  });

  dvqExplorers.register({
    views: { islands: islandsView },
    help: {
      islands: "לחיצה על תא הופכת אותו ממים ליבשה ובחזרה, \"לוח אקראי\" מגריל לוח לפי הסיכוי ליבשה, ובוחרים ארבעה או שמונה כיוונים. כל צעד הוא תא אחד של מילוי בהצפה : הסריקה פוגשת יבשה שלא סומנה ומתחילה אי חדש, או תא יוצא מהתור ושכניו נבדקים. התור מצויר ליד הלוח, התא שיצא מוקף, התאים שנכנסו מסומנים בכתום, וכל אי מקבל צבע עם המספר שלו (בסעיף ג : הגודל שלו, והרשימה הממוינת מתחת). השורה שמתחת מסבירה כל צעד, והפאנל 'הסבר' מדליק את שורות הקוד.",
    },
    models: { ilTrace, ilSizes, ilParse, ilText },
  });
})();
