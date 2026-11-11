// kinds: soldiers
//   soldiers               0095        Conway's soldiers: a board with the line under row 1 (soldiers stand on y <= 0) and the target (0, n) of a chosen row 1 to 5; place soldiers below the line (row 5 opens placing; a fill button), jump by clicking a soldier and then the empty cell two away behind a neighbour, undo; a meter of the potential (σ to the power of the distance to the target, summed) against the target's 1; the stored plays of rows 1 to 4 stepped move by move
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, ltr, autoplay, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const SIGMA = (Math.sqrt(5) - 1) / 2;

  // --- the theory (tests/0095 compares these with the page's Python code) ----------------------
  // the plays of the page: the army below the line, then each move as [from, over, to]
  const SOLUTIONS = {
    1: [[[0, 0], [0, -1]],
      [[[0, -1], [0, 0], [0, 1]]]],
    2: [[[-2, 0], [-1, 0], [0, 0], [0, -1]],
      [[[0, -1], [0, 0], [0, 1]], [[-2, 0], [-1, 0], [0, 0]], [[0, 0], [0, 1], [0, 2]]]],
    3: [[[-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0], [0, -1], [1, -1], [2, -1]],
      [[[2, -1], [2, 0], [2, 1]], [[1, -1], [1, 0], [1, 1]], [[2, 1], [1, 1], [0, 1]],
        [[0, 0], [0, 1], [0, 2]], [[-2, 0], [-1, 0], [0, 0]], [[0, -1], [0, 0], [0, 1]],
        [[0, 1], [0, 2], [0, 3]]]],
    4: [[[-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0],
      [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1], [3, -1],
      [-2, -2], [-1, -2], [0, -2], [1, -2], [2, -2], [0, -3], [2, -3]],
    [[[0, -1], [0, 0], [0, 1]], [[0, -3], [0, -2], [0, -1]], [[-2, -2], [-1, -2], [0, -2]],
      [[1, -1], [1, 0], [1, 1]], [[3, -1], [2, -1], [1, -1]], [[2, -3], [2, -2], [2, -1]],
      [[2, -1], [2, 0], [2, 1]], [[4, 0], [3, 0], [2, 0]], [[1, -2], [1, -1], [1, 0]],
      [[0, -2], [0, -1], [0, 0]], [[-2, -1], [-2, 0], [-2, 1]], [[-1, -1], [-1, 0], [-1, 1]],
      [[2, 0], [2, 1], [2, 2]], [[1, 0], [1, 1], [1, 2]], [[2, 2], [1, 2], [0, 2]],
      [[0, 1], [0, 2], [0, 3]], [[-2, 1], [-1, 1], [0, 1]], [[0, 0], [0, 1], [0, 2]],
      [[0, 2], [0, 3], [0, 4]]]],
  };
  const key = (c) => `${c[0]},${c[1]}`;
  const unkey = (k) => k.split(",").map(Number);
  // a jump from src to dst (two cells away in a row or a column): the new army, or null
  // when it is not a jump (no soldier at src or between, or dst taken)
  const csJump = (army, src, dst) => {
    const dx = dst[0] - src[0], dy = dst[1] - src[1];
    if (!((Math.abs(dx) === 2 && dy === 0) || (Math.abs(dy) === 2 && dx === 0))) return null;
    const over = [src[0] + dx / 2, src[1] + dy / 2];
    const s = new Set(army.map(key));
    if (!s.has(key(src)) || !s.has(key(over)) || s.has(key(dst))) return null;
    s.delete(key(src)); s.delete(key(over)); s.add(key(dst));
    return [...s].map(unkey);
  };
  const sortArmy = (a) => a.slice().sort((p, q) => q[1] - p[1] || p[0] - q[0]);
  // every board of the stored play to row n, the start first
  const csBoards = (n) => {
    const [army, moves] = SOLUTIONS[n];
    const out = [sortArmy(army)];
    for (const [a, , c] of moves) out.push(sortArmy(csJump(out[out.length - 1], a, c)));
    return out;
  };
  const csDist = (c, n) => Math.abs(c[0]) + Math.abs(n - c[1]);
  const csPotential = (army, n) => army.reduce((s, c) => s + SIGMA ** csDist(c, n), 0);
  // the weight of the whole half plane y <= 0: σ^n · 1/(1 − σ) · (1 + 2σ/(1 − σ)) = σ^(n − 5)
  const csHalfPlane = (n) => SIGMA ** n / (1 - SIGMA) * (1 + 2 * SIGMA / (1 - SIGMA));

  // --- the view --------------------------------------------------------------------------------
  const XR = [-5, 5], YR = [-4, 5], S = 26, LM = 16, TOP = 26;
  const cellName = (c) => ltr(`(${c[0]}, ${c[1]})`);
  const plain = (c) => `(${c[0]}, ${c[1]})`;
  const view = () => ({
    mount(box) {
      const clamp = (v, lo, hi, d) => { const x = Math.floor(Number(v)); return Number.isFinite(x) ? Math.min(hi, Math.max(lo, x)) : d; };
      const n0 = clamp(box.dataset.row, 1, 5, 4);
      const st = { n: n0, army: [], hist: [], sel: null, place: n0 === 5, rep: n0 <= 4 ? { n: n0, k: 0 } : null, last: null, msg: "", focus: [0, 0] };
      const opts = [1, 2, 3, 4, 5].map((x) => `<option value="${x}"${x === n0 ? " selected" : ""}>${x}</option>`).join("");
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>השורה <select class="cy-row" aria-label="שורת היעד, מעל הקו">${opts}</select></label>` +
        `<button type="button" class="md-button cy-place" aria-pressed="false">הצבה</button>` +
        `<button type="button" class="md-button cy-fillall">מילוי</button>` +
        `<button type="button" class="md-button cy-clear">ניקוי</button>` +
        `<button type="button" class="md-button cy-undo">ביטול</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button cy-sol">הפתרון של השורה</button>` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">המהלך הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">המהלך הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(900, 500, 200) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary cy-sum" aria-live="polite"></p>` +
        `<div class="cy-meter"><span>הפוטנציאל</span><span class="cy-bar" role="img"><span class="cy-fill"></span><span class="cy-one"></span></span><span class="cy-val"></span></div>` +
        `<div class="cy-wrap"></div>` +
        `<span class="viz-legend"><span><i class="cy-key-man"></i>חייל</span><span><i class="cy-key-new"></i>החייל שקפץ</span>` +
        `<span><i class="cy-key-gone"></i>מה שהקפיצה פינתה</span><span><i class="cy-key-target"></i>היעד</span>` +
        `<span><i class="cy-key-sel"></i>החייל שנבחר</span><span><i class="cy-key-hint"></i>לאן הוא יכול לקפוץ</span></span>` +
        `<p class="cy-why"></p>`;
      const $ = (q) => box.querySelector(q);
      const wrap = $(".cy-wrap");
      const boardsOf = {};
      const boards = (n) => (boardsOf[n] = boardsOf[n] || csBoards(n));
      const total = () => (st.rep ? SOLUTIONS[st.rep.n][1].length : 0);
      const current = () => (st.rep ? boards(st.rep.n)[st.rep.k] : st.army);
      const lastMove = () => (st.rep ? (st.rep.k ? SOLUTIONS[st.rep.n][1][st.rep.k - 1] : null) : st.last);
      const has = (army, c) => army.some((p) => p[0] === c[0] && p[1] === c[1]);
      const targets = (army, c) => [[2, 0], [-2, 0], [0, 2], [0, -2]].map(([dx, dy]) => [c[0] + dx, c[1] + dy])
        .filter((d) => d[0] >= XR[0] && d[0] <= XR[1] && d[1] >= YR[0] && d[1] <= YR[1] && csJump(army, c, d));
      const draw = (focus = false) => {
        const army = current(), mv = lastMove();
        if (st.rep) st.n = st.rep.n;
        $(".cy-row").value = String(st.n);
        $(".cy-place").setAttribute("aria-pressed", String(st.place));
        $(".cy-undo").disabled = !!st.rep || !st.hist.length;
        $(".cy-sol").disabled = st.n > 4;
        $(".cy-sol").textContent = st.n > 4 ? "לשורה 5 אין פתרון" : `הפתרון של שורה ${st.n}`;
        const T = total(), k = st.rep ? st.rep.k : 0;
        $(".ex-pos").textContent = st.rep ? `מהלך ${k} מתוך ${T}` : "משחק חופשי";
        $(".ex-prev").disabled = $(".ex-start").disabled = !st.rep || k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = !st.rep || k === T;
        $(".ex-play").disabled = !st.rep;
        // the meter: the potential against the target's 1
        const pot = csPotential(army, st.n), top = Math.max(1.25, pot * 1.05);
        $(".cy-fill").style.transform = `scaleX(${(pot / top).toFixed(4)})`;
        $(".cy-one").style.left = `calc(${((1 / top) * 100).toFixed(2)}% - 1px)`;
        $(".cy-bar").setAttribute("aria-label", `הפוטנציאל ${pot.toFixed(4)}, היעד 1`);
        $(".cy-val").innerHTML = ltr(`${pot.toFixed(4)} ${pot >= 1 - 1e-9 ? "≥" : "<"} 1`);
        // the board
        const w = LM + (XR[1] - XR[0] + 1) * S + 4, ht = TOP + (YR[1] - YR[0] + 1) * S + 4;
        const px = (x, y) => [LM + (x - XR[0]) * S, TOP + (YR[1] - y) * S];
        const hints = st.sel && !st.rep ? targets(army, st.sel) : [];
        const r = S * 0.32;
        let s = `<svg class="figure cy-board" viewBox="0 0 ${w} ${ht}" style="max-width:${((w * 1.15) / 16).toFixed(1)}rem" role="group" ` +
          `aria-label="לוח החיילים, ${army.length} חיילים, היעד ${plain([0, st.n])}. לוחצים על משבצת, או עוברים בחיצים ולוחצים Enter">`;
        const [fx, fy] = st.focus;
        for (let y = YR[1]; y >= YR[0]; y--) {
          for (let x = XR[0]; x <= XR[1]; x++) {
            const [cx, cy] = px(x, y), c = [x, y], man = has(army, c);
            let inner = `<rect class="${y <= 0 ? "cy-ground" : "cy-sky"}" x="${cx + 0.5}" y="${cy + 0.5}" width="${S - 1}" height="${S - 1}"/>`;
            if (x === 0 && y === st.n) inner += `<rect class="cy-target" x="${cx + 1.5}" y="${cy + 1.5}" width="${S - 3}" height="${S - 3}" rx="2"/>`;
            if (mv && !man && ((mv[0][0] === x && mv[0][1] === y) || (mv[1][0] === x && mv[1][1] === y))) inner += `<circle class="cy-gone" cx="${cx + S / 2}" cy="${cy + S / 2}" r="${r}"/>`;
            if (man) inner += `<circle class="${mv && mv[2][0] === x && mv[2][1] === y ? "cy-new" : "cy-man"}" cx="${cx + S / 2}" cy="${cy + S / 2}" r="${r}"/>`;
            if (st.sel && !st.rep && st.sel[0] === x && st.sel[1] === y) inner += `<circle class="cy-sel" cx="${cx + S / 2}" cy="${cy + S / 2}" r="${r + 3}"/>`;
            if (hints.some((d) => d[0] === x && d[1] === y)) inner += `<rect class="cy-hint" x="${cx + 4}" y="${cy + 4}" width="${S - 8}" height="${S - 8}" rx="3"/>`;
            const name = `${plain(c)}${NB}: ${man ? "חייל" : "ריקה"}${x === 0 && y === st.n ? ", היעד" : ""}`;
            s += `<g class="cy-btn" role="button" tabindex="${x === fx && y === fy ? 0 : -1}" data-x="${x}" data-y="${y}" aria-label="${name}">${inner}` +
              `<rect class="cy-ring" x="${cx + 0.5}" y="${cy + 0.5}" width="${S - 1}" height="${S - 1}"/></g>`;
          }
          if (y > 0) { const [, cy] = px(XR[0], y); s += `<text class="cy-lab" x="${LM / 2}" y="${cy + S / 2 + 4}" text-anchor="middle">${y}</text>`; }
        }
        const [lx, ly] = px(XR[0], 0);
        s += `<line class="cy-line" x1="${lx - 2}" y1="${ly}" x2="${lx + (XR[1] - XR[0] + 1) * S + 2}" y2="${ly}"/>`;
        wrap.innerHTML = s + "</svg>";
        if (focus) { const el = wrap.querySelector(".cy-btn[tabindex='0']"); if (el) el.focus(); }
        // the summary and the reason
        const reached = has(army, [0, st.n]);
        let sum;
        if (st.rep) {
          sum = k === 0 ? `הפתרון של שורה ${ltr(st.rep.n)}${NB}: ${ltr(army.length)} חיילים מתחת לקו.`
            : `מהלך ${ltr(k)}${NB}: החייל ב-${cellName(mv[0])} קופץ מעל ${cellName(mv[1])} אל ${cellName(mv[2])}. נשארו ${ltr(army.length)} חיילים.`;
        } else if (st.place) sum = `<b>הצבה${NB}:</b> לחיצה על משבצת מתחת לקו מוסיפה חייל או מורידה אותו, ו"הצבה" שוב חוזרת לקפיצות. ${ltr(army.length)} חיילים.`;
        else if (st.sel) sum = `נבחר החייל ב-${cellName(st.sel)}. לוחצים על משבצת מסומנת כדי לקפוץ אליה, או על חייל אחר.`;
        else sum = `<b>קפיצה${NB}:</b> לוחצים על חייל, ואז על המשבצת הריקה שמעבר לשכן שלו. ${ltr(army.length)} חיילים.`;
        $(".cy-sum").innerHTML = sum;
        let why = st.msg;
        if (!why) {
          // what the last jump did to the sum (a placing leaves no last move)
          const d = mv && !reached ? csPotential(st.rep ? boards(st.rep.n)[k - 1] : (st.hist.length ? st.hist[st.hist.length - 1] : army), st.n) - pot : null;
          const moved = d === null ? "" : d > 1e-9 ? `המהלך האחרון הוריד את הסכום ב-${ltr(d.toFixed(4))}` : `המהלך האחרון לא שינה את הסכום${NB}: קפיצה ישר לכיוון היעד`;
          if (st.n === 5) why = moved ? `${moved}. בשורה 5 הסכום תמיד מתחת ל-1.` : `לשורה 5 כל חצי המישור שוקל בדיוק 1, ומספר סופי של חיילים שוקל פחות. המד לא יגיע ל-1, גם בלי לקפוץ.`;
          else if (pot < 1 - 1e-9) why = `${d > 1e-9 ? `${moved}, והוא` : "הסכום"} קטן מ-1${NB}: מהעמדה הזו כבר אי אפשר להגיע ל-${cellName([0, st.n])}, כי קפיצה אף פעם לא מגדילה אותו.`;
          else if (moved) why = d > 1e-9 ? `${moved}${NB}: הוא לא התקרב ליעד.` : `${moved}.`;
        }
        $(".cy-why").innerHTML = why;
        if (reached) answer(box, `חייל הגיע ל-${cellName([0, st.n])}, בשורה ${ltr(st.n)}.`, ".cy-sum");
        else answer(box, null);
      };
      const leaveReplay = () => {
        if (!st.rep) return;
        st.army = boards(st.rep.n)[st.rep.k].map((c) => c.slice());
        st.last = st.rep.k ? SOLUTIONS[st.rep.n][1][st.rep.k - 1] : null;
        st.hist = []; st.rep = null;
      };
      const act = (x, y) => {
        stop(); leaveReplay(); st.msg = "";
        const c = [x, y], army = st.army;
        if (st.place) {
          if (y > 0) { st.msg = `מציבים חיילים רק מתחת לקו, בשורה 0 ומטה.`; draw(true); return; }
          st.hist.push(army);
          st.army = has(army, c) ? army.filter((p) => p[0] !== x || p[1] !== y) : army.concat([c]);
          st.last = null; st.sel = null;
        } else if (has(army, c)) {
          st.sel = st.sel && st.sel[0] === x && st.sel[1] === y ? null : c;
          if (st.sel && !targets(army, c).length) st.msg = `לחייל ב-${cellName(c)} אין לאן לקפוץ${NB}: צריך שכן, ומעבר לו משבצת ריקה.`;
        } else if (!st.sel) {
          st.msg = `המשבצת ${cellName(c)} ריקה. כדי להציב חיילים לחצו "הצבה"; כדי לקפוץ, בחרו קודם חייל.`;
        } else {
          const next = csJump(army, st.sel, c);
          if (!next) st.msg = `מ-${cellName(st.sel)} אי אפשר לקפוץ אל ${cellName(c)}${NB}: קופצים שתי משבצות בשורה או בעמודה, מעל שכן.`;
          else {
            st.hist.push(army);
            st.last = [st.sel, [(st.sel[0] + x) / 2, (st.sel[1] + y) / 2], c];
            st.army = next; st.sel = null;
          }
        }
        st.focus = [x, y];
        draw(true);
      };
      wrap.addEventListener("click", (e) => { const b = e.target.closest(".cy-btn"); if (b) act(Number(b.dataset.x), Number(b.dataset.y)); });
      wrap.addEventListener("keydown", (e) => {
        const b = e.target.closest(".cy-btn");
        if (!b) return;
        const x = Number(b.dataset.x), y = Number(b.dataset.y);
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); e.stopPropagation(); act(x, y); return; }
        const dir = { ArrowUp: [0, 1], ArrowDown: [0, -1], ArrowLeft: [-1, 0], ArrowRight: [1, 0] }[e.key];
        if (!dir) return;
        e.preventDefault(); e.stopPropagation();
        const nx = x + dir[0], ny = y + dir[1];
        const t = wrap.querySelector(`.cy-btn[data-x="${nx}"][data-y="${ny}"]`);
        if (!t) return;
        wrap.querySelectorAll(".cy-btn").forEach((el) => el.setAttribute("tabindex", "-1"));
        t.setAttribute("tabindex", "0"); t.focus();
        st.focus = [nx, ny];
      });
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: () => { if (st.rep) st.rep.k++; draw(); },
        done: () => !st.rep || st.rep.k >= total(),
        restart: () => { if (st.rep) st.rep.k = 0; draw(); },
      });
      // row 5 has no play: an empty board in placing mode
      const loadSolution = (n) => { stop(); st.rep = n <= 4 ? { n, k: 0 } : null; st.sel = null; st.msg = ""; st.hist = []; st.last = null; if (!st.rep) { st.army = []; st.place = true; } st.n = n; draw(); };
      $(".cy-row").addEventListener("change", () => {
        const n = clamp($(".cy-row").value, 1, 5, n0);
        if (st.rep) loadSolution(n);
        else { st.n = n; st.msg = ""; draw(); }
      });
      $(".cy-place").addEventListener("click", () => { stop(); leaveReplay(); st.place = !st.place; st.sel = null; st.msg = ""; draw(); });
      // every cell of the board below the line (55 soldiers)
      $(".cy-fillall").addEventListener("click", () => {
        stop(); leaveReplay(); st.hist.push(st.army);
        st.army = [];
        for (let y = 0; y >= YR[0]; y--) for (let x = XR[0]; x <= XR[1]; x++) st.army.push([x, y]);
        st.sel = null; st.last = null; st.msg = ""; draw();
      });
      $(".cy-clear").addEventListener("click", () => { stop(); leaveReplay(); if (st.army.length) st.hist.push(st.army); st.army = []; st.sel = null; st.last = null; st.msg = ""; st.place = true; draw(); });
      $(".cy-undo").addEventListener("click", () => { if (!st.hist.length) return; st.army = st.hist.pop(); st.sel = null; st.last = null; st.msg = ""; draw(); });
      $(".cy-sol").addEventListener("click", () => loadSolution(st.n));
      $(".ex-start").addEventListener("click", () => { stop(); if (st.rep) st.rep.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.rep && st.rep.k) st.rep.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { if (st.rep && st.rep.k < total()) st.rep.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); if (st.rep) st.rep.k = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => { st.place = n0 === 5; st.focus = [0, 0]; loadSolution(n0); });
      // the state in the link: "4@7" (the play to row 4 at move 7) or "4|0.0,0.-1" (free play)
      box.dvqExtra = {
        get: () => (st.rep ? `${st.rep.n}@${st.rep.k}` : `${st.n}|${st.army.map((c) => `${c[0]}.${c[1]}`).join(",")}`),
        set: (text) => {
          let m = /^([1-4])@(\d{1,2})$/.exec(text);
          if (m) {
            const n = Number(m[1]), k = Number(m[2]);
            if (k > SOLUTIONS[n][1].length) return false;
            stop(); st.rep = { n, k }; st.n = n; st.sel = null; st.msg = ""; st.hist = []; draw(); return true;
          }
          m = /^([1-5])\|((-?\d\.-?\d)(,-?\d\.-?\d){0,109})?$/.exec(text);
          if (!m) return false;
          const army = m[2] ? m[2].split(",").map((p) => p.split(".").map(Number)) : [];
          if (army.some(([x, y]) => x < XR[0] || x > XR[1] || y < YR[0] || y > YR[1])) return false;
          if (new Set(army.map(key)).size !== army.length) return false;
          stop(); st.rep = null; st.n = Number(m[1]); st.army = army; st.hist = []; st.sel = null; st.last = null; st.msg = ""; draw(); return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { soldiers: view },
    help: {
      soldiers: `החיילים עומדים מתחת לקו, והיעד של השורה מסומן במסגרת. "הפתרון של שורה" מנגן את הפתרון השמור מהלך אחר מהלך. במשחק חופשי לוחצים על חייל, ואז על המשבצת הריקה שמעבר לשכן שלו. "הצבה" מוסיפה ומורידה חיילים בלחיצה, ו"מילוי" ממלא את כל המשבצות שמתחת לקו. המד${NB}: כל חייל שוקל σ בחזקת המרחק שלו מהיעד, וקפיצה אף פעם לא מגדילה את הסכום. מתחת ל-1 כבר אי אפשר להגיע.`,
    },
    cols: { soldiers: { main: ".cy-wrap", side: ".cy-meter, .cy-why, .viz-legend" } },   // the board beside the meter, the reason and the key
    models: { csSolutions: SOLUTIONS, csJump, csBoards, csPotential, csHalfPlane, csDist },
  });
})();
