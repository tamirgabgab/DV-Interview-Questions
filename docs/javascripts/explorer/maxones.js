// kinds: maxones
//   maxones                0046        a binary grid up to 16 × 16 (typed size, a random fill at a chosen probability of 1, a tap toggles a cell, a dragged rectangle set to 1 or 0); the largest all-ones square by the dp of part a, the largest rectangle by the histograms and the stack of part b, or the largest right triangle with equal legs by the four passes of part c, played step by step beside the dp or heights matrix, the best so far outlined and the answer green at the end
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, gridText, ltr, parseGrid, seedControls, speedSel, viewSel } = dvqExplorers.lib;
  const NB = " ";
  const MAX = 16;

  // Part a, the page's largest_square one cell at a time: dp[i][j] is the side of the
  // largest all-ones square whose bottom-right corner is (i, j), the min of the three
  // neighbours plus 1 on a 1. A frame per cell, with the neighbours it read and the best
  // side so far (a larger side only replaces it, as in the page's code).
  const moSquare = (grid) => {
    const m = grid.length, n = m ? grid[0].length : 0;
    const dp = grid.map((r) => r.map(() => 0)), frames = [];
    let side = 0, end = null;
    for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) {
      const top = i ? dp[i - 1][j] : 0, left = j ? dp[i][j - 1] : 0, diag = i && j ? dp[i - 1][j - 1] : 0;
      const v = grid[i][j] ? Math.min(top, left, diag) + 1 : 0;
      dp[i][j] = v;
      const better = v > side;
      if (better) { side = v; end = [i, j]; }
      frames.push({ i, j, v, top, left, diag, better, side, end });
    }
    const result = side ? { area: side * side, tl: [end[0] - side + 1, end[1] - side + 1], br: end } : { area: 0, tl: null, br: null };
    return { dp, frames, result };
  };

  // Part b, the page's largest_rectangle one event at a time: a row event (the heights
  // updated), a pop (a column leaves the stack, its rectangle checked) and a push. The
  // zero pushed at j = n only ends the row and is no event. Every event carries the stack
  // after it and the best rectangle so far.
  const moRect = (grid) => {
    const m = grid.length, n = m ? grid[0].length : 0;
    const H = [], events = [], heights = Array(n).fill(0);
    let best = { area: 0, tl: null, br: null };
    for (let i = 0; i < m; i++) {
      for (let j = 0; j < n; j++) heights[j] = grid[i][j] ? heights[j] + 1 : 0;
      H.push(heights.slice());
      const stack = [];
      events.push({ t: "row", i, stack: [], best });
      for (let j = 0; j <= n; j++) {
        const h = j < n ? heights[j] : 0;
        while (stack.length && heights[stack[stack.length - 1]] >= h) {
          const col = stack.pop(), height = heights[col], left = stack.length ? stack[stack.length - 1] + 1 : 0;
          const cand = { area: height * (j - left), tl: [i - height + 1, left], br: [i, j - 1] };
          const better = cand.area > best.area;
          if (better) best = cand;
          events.push({ t: "pop", i, j, h, col, height, left, cand, better, stack: stack.slice(), best });
        }
        stack.push(j);
        if (j < n) events.push({ t: "push", i, j, h, stack: stack.slice(), best });
      }
    }
    return { H, events, result: best };
  };

  // Part c, the page's largest_triangle one cell at a time: a pass per direction of the
  // legs, in the page's order, each scanning from the side the legs point to; dp is the leg
  // of the largest triangle whose right angle is the cell, the min of the two neighbours
  // along the legs plus 1 on a 1. A frame per cell of every pass, with the neighbours read
  // and the best leg so far. The ties: a leg of 1 is any 1 (one cell, every direction), and
  // a longer leg fixes the corner and the direction, so they are the cells holding it.
  const MO_DIRS = [[-1, -1], [-1, 1], [1, -1], [1, 1]];
  const moTriShape = (k, corner, p) => {
    const [dv, dh] = MO_DIRS[p];
    return { area: (k * (k + 1)) / 2, k, p, dv, dh, corner, legCol: [corner[0] + dv * (k - 1), corner[1]], legRow: [corner[0], corner[1] + dh * (k - 1)] };
  };
  const moTri = (grid) => {
    const m = grid.length, n = m ? grid[0].length : 0;
    const dps = [], frames = [];
    let side = 0, at = null, pass = 0;
    MO_DIRS.forEach(([dv, dh], p) => {
      const dp = grid.map((r) => r.map(() => 0));
      for (let s = 0; s < m; s++) {
        const i = dv < 0 ? s : m - 1 - s;
        for (let t = 0; t < n; t++) {
          const j = dh < 0 ? t : n - 1 - t;
          const vert = i + dv >= 0 && i + dv < m ? dp[i + dv][j] : 0, horiz = j + dh >= 0 && j + dh < n ? dp[i][j + dh] : 0;
          const v = grid[i][j] ? Math.min(vert, horiz) + 1 : 0;
          dp[i][j] = v;
          const better = v > side;
          if (better) { side = v; at = [i, j]; pass = p; }
          frames.push({ p, i, j, v, vert, horiz, better, side, at, pass });
        }
      }
      dps.push(dp);
    });
    const result = side ? moTriShape(side, at, pass) : { area: 0, corner: null, legCol: null, legRow: null };
    const ties = !side ? 0 : side === 1 ? grid.flat().filter(Boolean).length : dps.reduce((a, dp) => a + dp.flat().filter((v) => v === side).length, 0);
    return { dps, frames, result, ties };
  };

  // How many all-ones squares (or rectangles of any shape) have the given area: the page's
  // code returns the first one it meets, and the others are the ties.
  const moCount = (grid, area, square) => {
    const m = grid.length, n = m ? grid[0].length : 0;
    if (!area) return 0;
    const P = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
    for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) P[i + 1][j + 1] = grid[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j];
    let count = 0;
    for (let h = 1; h <= m; h++) {
      if (area % h) continue;
      const w = area / h;
      if (w > n || (square && w !== h)) continue;
      for (let r = 0; r + h <= m; r++) for (let c = 0; c + w <= n; c++)
        if (P[r + h][c + w] - P[r][c + w] - P[r + h][c] + P[r][c] === area) count++;
    }
    return count;
  };

  const moParse = (text) => {
    if (!/^[01]+(\.[01]+)*$/.test(text)) return null;
    const rows = text.split(".");
    if (rows.length > MAX || rows[0].length > MAX || rows.some((r) => r.length !== rows[0].length)) return null;
    return rows.map((r) => [...r].map(Number));
  };
  const moText = (grid) => grid.map((r) => r.join("")).join(".");

  // The box: the grid to edit on the left of the figure and the dp (or heights) matrix
  // beside it, both drawn left to right as matrices are; a step plays one cell (a square,
  // a triangle) or one event (a rectangle). During the run the current cell is framed, the
  // best shape so far outlined in orange and the rectangle being checked dashed; at the end
  // the answer's cells turn green. A triangle's outline is a staircase drawn in an SVG over
  // its bounding square, and its dp panel shows the pass being played.
  const DIR_WORDS = ["למעלה ושמאלה", "למעלה וימינה", "למטה ושמאלה", "למטה וימינה"];
  const MODES = { square: "ריבוע", rect: "מלבן", tri: "משולש" };
  const maxonesView = () => ({
    mount(box) {
      const mode0 = MODES[box.dataset.mode] ? box.dataset.mode : "square";
      const grid0 = moParse(box.dataset.grid || "") || [[1, 1], [1, 0]];
      const st = { grid: grid0.map((r) => r.slice()), mode: mode0, p: 70, k: 0, sel: null, focus: [0, 0], final: false };
      box.innerHTML =
        `<div class="ex-controls"><label>שורות <input type="number" class="ex-num mo-m" min="1" max="${MAX}" step="1" value="${grid0.length}" dir="ltr" aria-label="מספר השורות, עד ${MAX}"></label>` +
        `<label>עמודות <input type="number" class="ex-num mo-n" min="1" max="${MAX}" step="1" value="${grid0[0].length}" dir="ltr" aria-label="מספר העמודות, עד ${MAX}"></label>` +
        `<label>הסיכוי ל-1 <input type="range" class="mo-p" min="0" max="100" step="5" value="70" dir="ltr" aria-label="הסיכוי של תא להיות 1 במערך אקראי, באחוזים"><output class="mo-out-p">70%</output></label>` +
        `<button type="button" class="md-button md-button--primary mo-rand">מערך אקראי</button></div>` +
        `<div class="ex-controls"><label>מחפשים <select class="mo-mode" aria-label="ריבוע, מלבן או משולש">${Object.entries(MODES).map(([v, w]) => `<option value="${v}">${w}</option>`).join("")}</select></label>${viewSel()}` +
        `<button type="button" class="md-button mo-set1" disabled>הסימון ל-1</button><button type="button" class="md-button mo-set0" disabled>הסימון ל-0</button></div>` +
        `<div class="ex-controls mo-textrow"><label class="mo-textlab">הערכים <textarea class="mo-text" rows="${grid0.length}" dir="ltr" spellcheck="false" data-nolink aria-label="המערך כטקסט, שורה בכל שורה"></textarea></label>` +
        `<button type="button" class="md-button mo-apply">עדכון מהטקסט</button><span class="mo-err" role="status"></span></div>` +
        `<div class="ex-controls mo-play"><button type="button" class="md-button ex-start">להתחלה</button><button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-play">הפעלה</button><button type="button" class="md-button ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-step mo-nextrow">השורה הבאה</button><button type="button" class="md-button ex-step mo-nextdir" hidden>הכיוון הבא</button><button type="button" class="md-button ex-end">עד הסוף</button>` +
        `${speedSel(600, 220, 50)}<span class="ex-pos" aria-live="off"></span></div>` +
        `<p class="ex-summary mo-sum" aria-live="polite"></p>` +
        `<span class="viz-legend"><span><i class="mo-key-one"></i>תא 1</span><span><i class="mo-key-cur"></i>התא הנוכחי</span><span class="mo-key-nb-wrap"><i class="mo-key-nb"></i>השכנים שנקראו</span>` +
        `<span class="mo-key-cand-wrap"><i class="mo-key-cand"></i>המלבן שנבדק</span><span><i class="mo-key-best"></i>הטוב עד עכשיו</span><span><i class="mo-key-win"></i>התשובה</span></span>` +
        `<p class="mo-edit-hint">לחיצה על תא הופכת אותו. גרירה מסמנת מלבן, ואז "הסימון ל-1" או "הסימון ל-0". במקלדת${NB}: חיצים בין התאים, רווח הופך תא, 0 או 1 קובעים אותו (או את כל הסימון), ו-Shift עם חץ מסמן. בשדה "הערכים" אפשר להדביק מערך שלם.</p>` +
        `<div class="mo-panels"><figure class="mo-panel"><figcaption class="mo-cap-in"></figcaption><div class="mo-grid mo-in" role="grid" dir="ltr" data-edits></div></figure>` +
        `<figure class="mo-panel"><figcaption class="mo-cap-dp"></figcaption><div class="mo-grid mo-dp" role="table" dir="ltr"></div></figure></div>` +
        `<p class="mo-step" aria-live="polite"></p><p class="mo-code"></p>`;
      const $ = (sel) => box.querySelector(sel);
      $(".mo-mode").value = st.mode;
      const play = $(".ex-play"), speed = $(".ex-speed");
      let trace = null;
      const retrace = () => { trace = st.mode === "square" ? moSquare(st.grid) : st.mode === "rect" ? moRect(st.grid) : moTri(st.grid); };
      const total = () => (st.mode === "rect" ? trace.events.length : trace.frames.length);

      const area = (s, cls) => (s && s.area ? `<div class="mo-box ${cls}" style="grid-area:${s.tl[0] + 1} / ${s.tl[1] + 1} / ${s.br[0] + 2} / ${s.br[1] + 2}"></div>` : "");
      const sqShape = (side, end) => (side ? { area: side * side, tl: [end[0] - side + 1, end[1] - side + 1], br: end } : null);
      const inside = (s, r, c) => {
        if (!s || !s.area) return false;
        if (!s.k) return r >= s.tl[0] && r <= s.br[0] && c >= s.tl[1] && c <= s.br[1];
        const a = (r - s.corner[0]) * s.dv, b = (c - s.corner[1]) * s.dh;
        return a >= 0 && b >= 0 && a + b < s.k;
      };
      // a triangle's staircase: drawn with the right angle at the bottom left (the legs up
      // and right, row y holding y + 1 cells) and mirrored into its direction
      const triLine = (s, cls) => {
        if (!s || !s.area) return "";
        const k = s.k, pts = [[0, 0]];
        for (let y = 0; y < k; y++) pts.push([y + 1, y], [y + 1, y + 1]);
        pts.push([0, k]);
        const xy = pts.map(([x, y]) => `${s.dh < 0 ? k - x : x},${s.dv > 0 ? k - y : y}`).join(" ");
        const r0 = Math.min(s.corner[0], s.legCol[0]), c0 = Math.min(s.corner[1], s.legRow[1]);
        return `<svg class="mo-tri ${cls}" style="grid-area:${r0 + 1} / ${c0 + 1} / ${r0 + k + 1} / ${c0 + k + 1}" viewBox="0 0 ${k} ${k}" preserveAspectRatio="none" aria-hidden="true">` +
          `<polygon points="${xy}" vector-effect="non-scaling-stroke"/></svg>`;
      };
      const outline = (s, cls) => (s && s.k ? triLine(s, `mo-tri--${cls}`) : area(s, `mo-box--${cls}`));

      const draw = () => {
        const m = st.grid.length, n = st.grid[0].length, T = total();
        const sq = st.mode === "square", rect = st.mode === "rect", tri = st.mode === "tri";
        st.k = st.final ? T : Math.min(Math.max(0, st.k), T);
        const done = st.k === T, ev = st.k ? (rect ? trace.events[st.k - 1] : trace.frames[st.k - 1]) : null;
        const res = trace.result, win = done ? res : null;
        const best = !ev ? null : sq ? sqShape(ev.side, ev.end) : tri ? (ev.side ? moTriShape(ev.side, ev.at, ev.pass) : null) : ev.best;
        const cand = ev && ev.t === "pop" && ev.cand.area ? ev.cand : null;
        // the marks of the current step go once the run is over, and the answer stays
        const live = ev && !done ? ev : null;
        const cur = live ? (!rect ? [ev.i, ev.j] : ev.t !== "row" && ev.j < n ? [ev.i, ev.j] : null) : null;
        const row = live ? live.i : -1;
        // a triangle's dp panel shows the pass being played, or at the end the answer's pass
        const pass = !tri ? 0 : live ? live.p : done && res.area ? res.p : done ? 3 : 0;
        const [dv, dh] = MO_DIRS[pass];
        box.classList.toggle("mo-is-rect", rect);
        box.classList.toggle("mo-is-tri", tri);
        // the grid to edit
        const isCur = (r, c) => cur && cur[0] === r && cur[1] === c;
        const dense = n > 10 ? " mo-dense" : "";
        const had = box.contains(document.activeElement) && document.activeElement.classList.contains("mo-cell");
        let g = "";
        for (let r = 0; r < m; r++) {
          g += `<div role="row" class="mo-r">`;
          for (let c = 0; c < n; c++) {
            const v = st.grid[r][c], f = st.focus[0] === r && st.focus[1] === c;
            g += `<div role="gridcell" class="mo-cell${v ? " is-1" : ""}${isCur(r, c) ? " is-cur" : ""}${inside(win, r, c) ? " is-win" : ""}${rect && r === row ? " is-row" : ""}" ` +
              `style="grid-area:${r + 1} / ${c + 1}" data-r="${r}" data-c="${c}" tabindex="${f ? 0 : -1}" aria-label="שורה ${r}, עמודה ${c}${NB}: ${v}">${v}</div>`;
          }
          g += `</div>`;
        }
        if (st.sel) g += area({ area: 1, tl: [Math.min(st.sel[0], st.sel[2]), Math.min(st.sel[1], st.sel[3])], br: [Math.max(st.sel[0], st.sel[2]), Math.max(st.sel[1], st.sel[3])] }, "mo-box--sel");
        g += done ? outline(win, "win") : outline(best, "best") + area(cand, "mo-box--cand");
        const gin = $(".mo-in");
        gin.className = `mo-grid mo-in${dense}`;
        gin.style.setProperty("--n", n);
        gin.innerHTML = g;
        if (had) { const f = gin.querySelector('[tabindex="0"]'); if (f) f.focus({ preventScroll: true }); }
        // the dp matrix of part a or c, or the heights of part b; cells not reached yet are empty
        const nb = live && !rect && st.grid[ev.i][ev.j] ? (sq ? [[ev.i - 1, ev.j], [ev.i, ev.j - 1], [ev.i - 1, ev.j - 1]] : [[ev.i + dv, ev.j], [ev.i, ev.j + dh]]) : [];
        const order = (r, c) => (dv < 0 ? r : m - 1 - r) * n + (dh < 0 ? c : n - 1 - c);   // a cell's place in its pass
        let d = "";
        for (let r = 0; r < m; r++) {
          d += `<div role="row" class="mo-r">`;
          for (let c = 0; c < n; c++) {
            const reached = sq ? r * n + c < st.k : tri ? done || order(r, c) < st.k - pass * m * n : done || r <= row;
            const v = !reached ? "" : sq ? trace.dp[r][c] : tri ? trace.dps[pass][r][c] : trace.H[r][c];
            const onStack = rect && live && r === row && ev.stack.includes(c);
            const lit = nb.some(([a, b]) => a === r && b === c);
            const popped = live && ev.t === "pop" && r === row && c === ev.col;
            d += `<div role="cell" class="mo-cell mo-val${reached ? "" : " is-wait"}${v ? " is-pos" : ""}${isCur(r, c) ? " is-cur" : ""}${lit ? " is-nb" : ""}` +
              `${onStack ? " is-stack" : ""}${popped ? " is-pop" : ""}${rect && r === row ? " is-row" : ""}${inside(win, r, c) ? " is-win" : ""}" style="grid-area:${r + 1} / ${c + 1}">${v}</div>`;
          }
          d += `</div>`;
        }
        d += done ? outline(win, "win") : area(cand, "mo-box--cand") + (sq || (tri && best && best.p === pass) ? outline(best, "best") : "");
        const gdp = $(".mo-dp");
        gdp.className = `mo-grid mo-dp${dense}`;
        gdp.style.setProperty("--n", n);
        gdp.innerHTML = d;
        $(".mo-cap-in").innerHTML = `המערך ${ltr("grid")}, ${ltr(`${m} × ${n}`)}`;
        $(".mo-cap-dp").innerHTML = sq ? `${ltr("dp[i][j]")}${NB}: הצלע של הריבוע הגדול שנגמר בתא`
          : tri ? `${ltr("dp[i][j]")}${NB}: הניצב של המשולש הגדול שהזווית הישרה שלו בתא, ניצבים ${DIR_WORDS[pass]}`
            : `${ltr("heights")}${NB}: ה-1 הרצופים שנגמרים בשורה, שורה אחרי שורה`;
        // the step in words, and the code's own state
        const P = (r, c) => ltr(`(${r}, ${c})`);
        let step = "", codeLine = "";
        if (!ev) {
          step = !T ? "" : `לוחצים על "הצעד הבא" או "הפעלה"${NB}: ` + (sq ? `התא הראשון הוא ${P(0, 0)}.`
            : tri ? `הכיוון הראשון הוא ניצבים ${DIR_WORDS[0]}, והתא הראשון הוא ${P(0, 0)}.` : "הצעד הראשון מעדכן את הגבהים של שורה 0.");
        } else if (sq) {
          step = st.grid[ev.i][ev.j]
            ? `תא ${P(ev.i, ev.j)} הוא 1, ולכן ${ltr(`dp = min(${ev.top}, ${ev.left}, ${ev.diag}) + 1 = ${ev.v}`)} (למעלה, משמאל ובאלכסון).` +
              (ev.better ? ` <b>ריבוע חדש בצלע ${ltr(ev.v)}, הגדול עד עכשיו ✓</b>` : "")
            : `תא ${P(ev.i, ev.j)} הוא 0, ולכן ${ltr("dp = 0")}.`;
          const arr = [0];
          for (let c = 0; c < n; c++) arr.push(c <= ev.j ? trace.dp[ev.i][c] : ev.i ? trace.dp[ev.i - 1][c] : 0);
          codeLine = `בקוד נשמרת רק שורה אחת${NB}: ${ltr(`dp = [${arr.join(", ")}]`)} ו-${ltr(`diag = ${ev.top}`)}, הערך מלמעלה שישמש כאלכסון לתא הבא.`;
        } else if (tri && done) {
          step = res.area ? `ארבעת הכיוונים נבדקו. לצד המערך מוצג ${ltr("dp")} של הכיוון שבו נמצא המשולש${NB}: ניצבים ${DIR_WORDS[res.p]}.` : "ארבעת הכיוונים נבדקו.";
        } else if (tri) {
          const [edv, edh] = MO_DIRS[ev.p];
          step = st.grid[ev.i][ev.j]
            ? `תא ${P(ev.i, ev.j)} הוא 1, ולכן ${ltr(`dp = min(${ev.vert}, ${ev.horiz}) + 1 = ${ev.v}`)} (השכנים ${edv < 0 ? "מלמעלה" : "מלמטה"} ו${edh < 0 ? "משמאל" : "מימין"}).` +
              (ev.better ? ` <b>משולש חדש בניצב ${ltr(ev.v)}, בשטח ${ltr((ev.v * (ev.v + 1)) / 2)}, הגדול עד עכשיו ✓</b>` : "")
            : `תא ${P(ev.i, ev.j)} הוא 0, ולכן ${ltr("dp = 0")}.`;
          // the page's one row: the cells of this row done so far, the row before it in the pass elsewhere
          const dp = trace.dps[ev.p], before = ev.i + edv, now = (c) => (edh < 0 ? c <= ev.j : c >= ev.j);
          const arr = [];
          for (let c = 0; c < n; c++) arr.push(now(c) ? dp[ev.i][c] : before >= 0 && before < m ? dp[before][c] : 0);
          codeLine = `כיוון ${ltr(ev.p + 1)} מתוך 4, ניצבים ${DIR_WORDS[ev.p]}. בקוד נשמרת רק שורה אחת${NB}: ${ltr(`dp = [${arr.join(", ")}]`)} ו-${ltr(`prev = ${ev.v}`)}, השכן לאורך השורה של התא הבא.`;
        } else {
          const hs = trace.H[ev.i];
          if (ev.t === "row") step = `שורה ${ltr(ev.i)}${NB}: ${ltr(`heights = [${hs.join(", ")}]`)}. מעל כל 1 הגובה גדל ב-1, ובכל 0 הוא מתאפס. המחסנית מתחילה ריקה.`;
          else if (ev.t === "push") step = `עמודה ${ltr(`j = ${ev.j}`)}, גובה ${ltr(ev.h)}${NB}: דוחפים את ${ltr(ev.j)} למחסנית.`;
          else {
            const w = ev.j - ev.left;
            step = `עמודה ${ltr(`j = ${ev.j}`)}, גובה ${ltr(ev.h)}${ev.j === n ? " (העמודה הדמיונית בסוף)" : ""}${NB}: מוציאים את ${ltr(ev.col)}, שגובהה ${ltr(ev.height)} ${ltr("≥")} ${ltr(ev.h)}. ` +
              (ev.height ? `הגבול השמאלי הוא ${ltr(ev.left)}, ולכן המלבן הוא עמודות ${ltr(`${ev.left}-${ev.j - 1}`)} בגובה ${ltr(ev.height)}, שטח ${ltr(`${ev.height} × ${w} = ${ev.cand.area}`)}.` +
                (ev.better ? ` <b>הגדול עד עכשיו ✓</b>` : "")
                : "גובה 0, אין מלבן.");
          }
          codeLine = `המחסנית${NB}: ${ltr(`[${ev.stack.join(", ")}]`)}${ev.stack.length ? `, בגבהים ${ltr(`[${ev.stack.map((c) => hs[c]).join(", ")}]`)}, עולים מלמטה למעלה` : ", ריקה"}.` +
            (ev.best.area ? ` הטוב עד עכשיו${NB}: שטח ${ltr(ev.best.area)}.` : "");
        }
        $(".mo-step").innerHTML = step;
        $(".mo-code").innerHTML = codeLine;
        $(".ex-pos").textContent = `צעד ${st.k} מתוך ${T}`;
        const ones = st.grid.reduce((s, r) => s + r.reduce((a, b) => a + b, 0), 0);
        const ties = !done || !res.area ? 0 : tri ? trace.ties : moCount(st.grid, res.area, sq);
        $(".mo-sum").innerHTML = `מערך ${ltr(`${m} × ${n}`)} עם ${ltr(ones)} תאים של 1. ` +
          (sq ? `ריבוע${NB}: צעד לכל תא, ${ltr(T)} צעדים.` : tri ? `משולש${NB}: ארבעה כיוונים וצעד לכל תא בכל כיוון, ${ltr(T)} צעדים.`
            : `מלבן${NB}: צעד לכל עדכון של שורה, לכל דחיפה ולכל הוצאה מהמחסנית, ${ltr(T)} צעדים.`) +
          (ties > 1 ? ` יש ${ltr(ties)} ${sq ? "ריבועים" : tri ? "משולשים" : "מלבנים"} בשטח ${ltr(res.area)}, והקוד מחזיר את הראשון שהוא פוגש.` : "");
        const text = !res.area ? `אין אף 1 במערך, ולכן התשובה היא ${ltr(tri ? "(0, None, None, None)" : "(0, None, None)")}.`
          : tri ? `השטח המקסימלי הוא ${ltr(res.area)}${NB}: משולש בניצב ${ltr(res.k)}, הזווית הישרה ב-${P(...res.corner)}, והניצבים עד ${P(...res.legCol)} ועד ${P(...res.legRow)}.`
            : `השטח המקסימלי הוא ${ltr(res.area)}${NB}: ${sq ? "ריבוע" : "מלבן"} ${ltr(`${res.br[0] - res.tl[0] + 1} × ${res.br[1] - res.tl[1] + 1}`)}, מ-${P(...res.tl)} עד ${P(...res.br)}.`;
        answer(box, done ? text : null, tri ? ".mo-in .mo-tri--win polygon" : ".mo-in .mo-box--win");
        $(".mo-set1").disabled = $(".mo-set0").disabled = !st.sel;
        $(".mo-nextdir").hidden = !tri;
        $(".mo-out-p").textContent = `${st.p}%`;
      };

      // every edit starts the run over
      // (in the final view every edit shows the end, and the steps stay there)
      const stop = autoplay(play, speed, {
        step: () => { if (!st.final) st.k++; draw(); },
        done: () => st.final || st.k >= total(),
        restart: () => { st.k = st.final ? total() : 0; draw(); },
      });
      const edited = (fromText = false) => {
        stop();
        retrace();
        st.k = st.final ? total() : 0;
        if (!fromText) {
          if (document.activeElement !== $(".mo-text")) $(".mo-text").value = gridText(st.grid);
          $(".mo-err").textContent = "";
        }
        $(".mo-text").rows = st.grid.length;
        draw();
      };
      const applyText = () => {
        const g = parseGrid($(".mo-text").value, { max: 1, rows: MAX, cols: MAX });
        if (typeof g === "string") { $(".mo-err").textContent = g; return; }
        $(".mo-err").textContent = "";
        st.grid = g;
        st.sel = null;
        st.focus = [Math.min(st.focus[0], g.length - 1), Math.min(st.focus[1], g[0].length - 1)];
        $(".mo-m").value = g.length;
        $(".mo-n").value = g[0].length;
        edited(true);
      };
      $(".mo-apply").addEventListener("click", applyText);
      $(".mo-text").addEventListener("change", applyText);
      $(".mo-text").addEventListener("keydown", (e) => {
        e.stopPropagation();
        if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); applyText(); }
      });
      $(".ex-view").addEventListener("change", () => {
        st.final = $(".ex-view").value === "final";
        box.classList.toggle("ex-final", st.final);
        stop();
        if (st.final) st.k = total();
        draw();
      });
      const resize = () => {
        const m = Math.min(MAX, Math.max(1, Math.round(Number($(".mo-m").value)) || 1));
        const n = Math.min(MAX, Math.max(1, Math.round(Number($(".mo-n").value)) || 1));
        st.grid = Array.from({ length: m }, (_, r) => Array.from({ length: n }, (_, c) => (st.grid[r] && st.grid[r][c]) || 0));
        st.sel = null;
        st.focus = [Math.min(st.focus[0], m - 1), Math.min(st.focus[1], n - 1)];
        edited();
      };
      $(".mo-m").addEventListener("input", resize);
      $(".mo-n").addEventListener("input", resize);
      $(".mo-p").addEventListener("input", () => { st.p = Number($(".mo-p").value); draw(); });
      const seed = seedControls(box, $(".mo-rand"), (rng) => {
        const m = st.grid.length, n = st.grid[0].length;
        st.grid = Array.from({ length: m }, () => Array.from({ length: n }, () => (rng() < st.p / 100 ? 1 : 0)));
        st.sel = null;
        edited();
      });
      $(".mo-rand").addEventListener("click", () => seed.draw());
      $(".mo-mode").addEventListener("change", () => { st.mode = MODES[$(".mo-mode").value] ? $(".mo-mode").value : "square"; edited(); });
      const fill = (v) => {
        if (!st.sel) return;
        const [r0, c0, r1, c1] = st.sel;
        for (let r = Math.min(r0, r1); r <= Math.max(r0, r1); r++) for (let c = Math.min(c0, c1); c <= Math.max(c0, c1); c++) st.grid[r][c] = v;
        st.sel = null;
        edited();
      };
      $(".mo-set1").addEventListener("click", () => fill(1));
      $(".mo-set0").addEventListener("click", () => fill(0));
      const guard = (f) => () => { if (!st.final) f(); };
      $(".ex-next").addEventListener("click", guard(() => { stop(); st.k++; draw(); }));
      $(".ex-prev").addEventListener("click", guard(() => { stop(); st.k--; draw(); }));
      $(".ex-start").addEventListener("click", guard(() => { stop(); st.k = 0; draw(); }));
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      $(".mo-nextrow").addEventListener("click", guard(() => {
        stop();
        const n = st.grid[0].length, T = total();
        if (st.mode !== "rect") st.k = Math.min(T, (Math.floor(st.k / n) + 1) * n);
        else {
          let k = st.k + 1;
          while (k < T && trace.events[k].t !== "row") k++;
          st.k = k;
        }
        draw();
      }));

      $(".mo-nextdir").addEventListener("click", guard(() => {
        stop();
        const mn = st.grid.length * st.grid[0].length;
        st.k = Math.min(total(), (Math.floor(st.k / mn) + 1) * mn);
        draw();
      }));

      // the grid: a tap toggles a cell, a drag selects a rectangle; the arrow keys move
      // between the cells (Shift extends the selection), space or Enter toggles
      const gin = $(".mo-in");
      const cellAt = (e) => { const el = document.elementFromPoint(e.clientX, e.clientY); return el && el.closest(".mo-in .mo-cell"); };
      let drag = null;
      gin.addEventListener("pointerdown", (e) => {
        const el = e.target.closest(".mo-cell");
        if (!el || e.button > 0) return;
        e.preventDefault();
        const r = Number(el.dataset.r), c = Number(el.dataset.c);
        drag = { r, c, moved: false };
        st.focus = [r, c];
        gin.setPointerCapture(e.pointerId);
      });
      gin.addEventListener("pointermove", (e) => {
        if (!drag) return;
        const el = cellAt(e);
        if (!el) return;
        const r = Number(el.dataset.r), c = Number(el.dataset.c);
        if (!drag.moved && r === drag.r && c === drag.c) return;
        drag.moved = true;
        const next = [drag.r, drag.c, r, c];
        if (!st.sel || next.some((v, i) => v !== st.sel[i])) { st.sel = next; draw(); }
      });
      const endDrag = (e) => {
        if (!drag) return;
        const d = drag;
        drag = null;
        if (gin.hasPointerCapture(e.pointerId)) gin.releasePointerCapture(e.pointerId);
        if (!d.moved && e.type === "pointerup") { st.grid[d.r][d.c] ^= 1; st.sel = null; edited(); }
      };
      gin.addEventListener("pointerup", endDrag);
      gin.addEventListener("pointercancel", endDrag);
      gin.addEventListener("keydown", (e) => {
        const el = e.target.closest(".mo-cell");
        if (!el) return;
        const m = st.grid.length, n = st.grid[0].length;
        const r = Number(el.dataset.r), c = Number(el.dataset.c);
        const move = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[e.key];
        if (move) {
          e.preventDefault();
          e.stopPropagation();                    // the box's own arrows step the run
          const nr = Math.min(m - 1, Math.max(0, r + move[0])), nc = Math.min(n - 1, Math.max(0, c + move[1]));
          if (e.shiftKey) st.sel = st.sel ? [st.sel[0], st.sel[1], nr, nc] : [r, c, nr, nc];
          st.focus = [nr, nc];
          draw();
          const f = gin.querySelector('[tabindex="0"]');
          if (f) f.focus({ preventScroll: false });
        } else if (e.key === " " || e.key === "Enter") {
          e.preventDefault();
          e.stopPropagation();
          st.grid[r][c] ^= 1;
          st.sel = null;
          edited();
        } else if (e.key === "0" || e.key === "1") {
          e.preventDefault();
          e.stopPropagation();
          const v = Number(e.key);
          if (st.sel && r >= Math.min(st.sel[0], st.sel[2]) && r <= Math.max(st.sel[0], st.sel[2]) && c >= Math.min(st.sel[1], st.sel[3]) && c <= Math.max(st.sel[1], st.sel[3])) fill(v);
          else { st.grid[r][c] = v; st.sel = null; edited(); }
        } else if (e.key === "Escape" && st.sel) {
          st.sel = null;
          draw();
        }
      });

      // the link and the remembered state carry the grid and the step: "10111.11111-12"
      box.dvqExtra = {
        get: () => `${moText(st.grid)}${st.k ? `-${st.k}` : ""}`,
        set: (text) => {
          const m = /^([01.]+)(?:-(\d+))?$/.exec(text), grid = m && moParse(m[1]);
          if (!grid) return false;
          stop();
          st.grid = grid;
          st.sel = null;
          $(".mo-m").value = grid.length;
          $(".mo-n").value = grid[0].length;
          edited();
          if (!st.final) st.k = m[2] ? Number(m[2]) : 0;
          draw();
          return true;
        },
      };
      retrace();
      edited();
    },
  });

  dvqExplorers.register({
    views: { maxones: maxonesView },
    help: {
      maxones: "עורכים את המערך : לחיצה על תא הופכת אותו, גרירה מסמנת מלבן שאפשר להפוך כולו ל-1 או ל-0, ו\"מערך אקראי\" ממלא לפי הסיכוי ל-1. בוחרים ריבוע, מלבן או משולש ומריצים צעד אחרי צעד, שורה אחרי שורה, כיוון אחרי כיוון (במשולש) או עד הסוף : לצד המערך מתמלא dp (בריבוע ובמשולש, בכל כיוון בנפרד) או heights (במלבן, עם המחסנית), הטוב עד עכשיו מוקף בכתום, ובסוף התשובה נצבעת בירוק.",
    },
    models: { moSquare, moRect, moTri, moCount, moParse, moText },
  });
})();
