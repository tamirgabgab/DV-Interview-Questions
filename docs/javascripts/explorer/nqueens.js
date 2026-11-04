// kinds: nqueens nqplace
//   nqueens                0081        N queens by backtracking with three bit masks: N chosen (4..10); a step is one queen the search places (the lowest free bit of its row first); the board with the queens so far, the cells of the next row attacked or free, the masks cols, left, right and free of that row in binary (bit c under column c, column 0 on the right), the solutions found so far, a jump to the next solution
//   nqplace                0081        N queens placed by hand: N chosen; a click (or Enter on a focused cell, the arrows move between cells) puts or takes a queen; the attacked cells, the queens that attack each other, and whether the queens can be completed to a solution (how many ways, one shown as faint queens, and a button that places it)
// Loaded after core.js on the pages that have these kinds (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMIN = 4, NMAX = 10;

  // --- the models ------------------------------------------------------------------------------

  // the queens the search places, in order: { row, col, count } (count: the solutions found
  // once this queen is down); the lowest free bit of a row first, as the page's code
  const nqSteps = (n) => {
    const full = (1 << n) - 1, out = [];
    let count = 0;
    const place = (row, cols, left, right) => {
      let free = full & ~(cols | left | right);
      while (free) {
        const bit = free & -free;
        free ^= bit;
        const col = 31 - Math.clz32(bit);
        if (row === n - 1) count++;
        out.push({ row, col, count });
        if (row < n - 1) place(row + 1, cols | bit, ((left | bit) << 1) & full, (right | bit) >> 1);
      }
    };
    place(0, 0, 0, 0);
    return out;
  };
  // the queens on the board after k steps (k = 0: none): a column per row from row 0
  const nqQueens = (steps, k) => {
    const qs = [];
    for (let i = 0; i < k; i++) { qs.length = steps[i].row; qs.push(steps[i].col); }
    return qs;
  };
  // the masks of the row after the queens qs: cols, left, right and the free bits
  const nqMasks = (n, qs) => {
    const full = (1 << n) - 1;
    let cols = 0, left = 0, right = 0;
    qs.forEach((c) => { const bit = 1 << c; cols |= bit; left = ((left | bit) << 1) & full; right = (right | bit) >> 1; });
    return { cols, left, right, free: full & ~(cols | left | right) };
  };
  // two queens [r, c] attack each other: the same row, column or diagonal
  const nqHits = (a, b) => a[0] === b[0] || a[1] === b[1] || Math.abs(a[0] - b[0]) === Math.abs(a[1] - b[1]);
  // the pairs of queens (indices into qs, a list of [r, c]) that attack each other
  const nqConflicts = (qs) => {
    const out = [];
    for (let i = 0; i < qs.length; i++) for (let j = i + 1; j < qs.length; j++) if (nqHits(qs[i], qs[j])) out.push([i, j]);
    return out;
  };
  // the cells attacked by the queens qs (a set of "r,c"), the queens' own cells left out
  const nqAttacked = (n, qs) => {
    const own = new Set(qs.map(([r, c]) => `${r},${c}`)), out = new Set();
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
      if (!own.has(`${r},${c}`) && qs.some((q) => nqHits(q, [r, c]))) out.add(`${r},${c}`);
    }
    return out;
  };
  // the completions of the queens qs (a list of [r, c], at most one per row, none attacking):
  // { count, first }, first a column per row (null when there is none)
  const nqComplete = (n, qs) => {
    const fixed = new Array(n).fill(-1);
    qs.forEach(([r, c]) => { fixed[r] = c; });
    let count = 0, first = null;
    const cols = [];
    const ok = (r, c) => cols.every((c2, r2) => c2 !== c && Math.abs(c2 - c) !== r - r2)
      && qs.every(([r2, c2]) => r2 <= r || (c2 !== c && Math.abs(c2 - c) !== r2 - r));
    const go = (r) => {
      if (r === n) { count++; if (!first) first = cols.slice(); return; }
      const cands = fixed[r] >= 0 ? [fixed[r]] : Array.from({ length: n }, (_, c) => c);
      cands.forEach((c) => { if (ok(r, c)) { cols.push(c); go(r + 1); cols.pop(); } });
    };
    go(0);
    return { count, first };
  };

  // --- the board -------------------------------------------------------------------------------

  const S = 40, PAD = 24;
  // a queen centred at (x, y) in a cell of side s: a crown on a base
  const queen = (x, y, s, cls) => {
    const k = s / 100, pts = [[-30, 18], [-36, -22], [-15, 0], [0, -32], [15, 0], [36, -22], [30, 18]];
    return `<g class="nq-q${cls ? ` ${cls}` : ""}"><polygon points="${pts.map(([a, b]) => `${(x + a * k).toFixed(1)},${(y + b * k).toFixed(1)}`).join(" ")}"/>` +
      `<rect x="${(x - 30 * k).toFixed(1)}" y="${(y + 20 * k).toFixed(1)}" width="${(60 * k).toFixed(1)}" height="${(11 * k).toFixed(1)}" rx="${(3 * k).toFixed(1)}"/></g>`;
  };
  // the board: column 0 on the right; cell(r, c) → { cls, queen (a class or null), attrs (of
  // the cell's group, when it is a button) }
  const boardSvg = (n, label, cell, cls = "") => {
    const w = n * S + PAD + 2, x0 = 1, y0 = PAD;
    let s = `<svg class="figure nq-board${cls ? ` ${cls}` : ""}" viewBox="0 0 ${w} ${w}" role="${cls.includes("nq-live-place") ? "group" : "img"}" aria-label="${label}">`;
    for (let c = 0; c < n; c++) s += `<text class="nq-lab" x="${x0 + (n - 1 - c) * S + S / 2}" y="${y0 - 7}" text-anchor="middle">${c}</text>`;
    for (let r = 0; r < n; r++) s += `<text class="nq-lab" x="${x0 + n * S + 5}" y="${y0 + r * S + S / 2 + 5}">${r}</text>`;
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const x = x0 + (n - 1 - c) * S, y = y0 + r * S, d = cell(r, c);
        const sq = `<rect class="nq-sq${(r + c) % 2 ? " is-dark" : ""}${d.cls ? ` ${d.cls}` : ""}" x="${x}" y="${y}" width="${S}" height="${S}"/>`;
        const q = d.queen !== null && d.queen !== undefined ? queen(x + S / 2, y + S / 2, S, d.queen) : "";
        s += d.attrs ? `<g class="nq-cell" ${d.attrs}>${sq}${q}<rect class="nq-ring" x="${x + 2}" y="${y + 2}" width="${S - 4}" height="${S - 4}"/></g>` : sq + q;
      }
    }
    return s + `<rect class="nq-frame" x="${x0}" y="${y0}" width="${n * S}" height="${n * S}"/></svg>`;
  };
  const bitsRow = (name, v, n, cls) => {
    let t = `<tr><th>${name}</th>`;
    for (let c = n - 1; c >= 0; c--) { const b = (v >> c) & 1; t += `<td class="gs-b${b ? " is-one" : ""}${b && cls ? ` ${cls}` : ""}">${b}</td>`; }
    return `${t}<td class="gs-val">= ${v}</td></tr>`;
  };
  const clampN = (v, d) => { const x = Math.floor(Number(v)); return Number.isFinite(x) ? Math.min(NMAX, Math.max(NMIN, x)) : d; };
  const nSelect = (n0, aria) => `<label><span>${ltr("N")}</span><select class="nq-n" aria-label="${aria}">` +
    Array.from({ length: NMAX - NMIN + 1 }, (_, i) => NMIN + i).map((v) => `<option value="${v}"${v === n0 ? " selected" : ""}>${v}</option>`).join("") + `</select></label>`;

  // --- the search, step by step ------------------------------------------------------------------

  const nqueensView = () => ({
    mount(box) {
      const N0 = clampN(box.dataset.n, 8);
      const lastSol = (steps, n) => { for (let i = steps.length - 1; i >= 0; i--) if (steps[i].row === n - 1) return i; return -1; };
      const st = { n: N0, k: 0, steps: nqSteps(N0) };
      st.last = lastSol(st.steps, N0);
      box.innerHTML =
        `<div class="ex-controls">` + nSelect(N0, "N, גודל הלוח ומספר המלכות") +
        `<button type="button" class="md-button nq-nextsol">לפתרון הבא</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערך של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">לוח ריק</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">כל הצעדים</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(900, 400, 120) +
        `<span class="ex-pos"></span></div>` +
        `<div class="nq-wrap"></div>` +
        `<span class="viz-legend"><span><i class="nq-key-new"></i>המלכה של הצעד</span><span><i class="nq-key-hit"></i>מאוימת בשורה הבאה</span>` +
        `<span><i class="nq-key-free"></i>פנויה בשורה הבאה</span><span><i class="nq-key-sol"></i>פתרון</span></span>` +
        `<p class="ex-title nq-mtitle"></p>` +
        `<div class="gs-scroll" tabindex="0" role="region" aria-label="המסכות של השורה הבאה"><table class="gs-bits nq-masks" dir="ltr" aria-label="המסכות של השורה הבאה, הביט הגבוה משמאל"><tbody></tbody></table></div>` +
        `<p class="ex-summary nq-sum" aria-live="polite"></p>` +
        `<p class="nq-now"></p>`;
      const $ = (s) => box.querySelector(s);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const draw = () => {
        const n = st.n, steps = st.steps, T = steps.length;
        st.k = Math.min(Math.max(st.k, 0), T);
        const k = st.k, qs = nqQueens(steps, k), row = qs.length, m = nqMasks(n, qs), cur = k ? steps[k - 1] : null;
        const sol = row === n, count = cur ? cur.count : 0, total = steps.length ? steps[T - 1].count : 0;
        $(".nq-n").value = String(n);
        $(".ex-pos").textContent = `צעד ${k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === T;
        $(".nq-nextsol").disabled = st.last < k;
        const label = `לוח של ${n} על ${n} אחרי ${k} צעדים${NB}: ${row} מלכות` + (row ? `, בשורות 0 עד ${row - 1}` : "") + (sol ? ", פתרון" : row < n ? `. בשורה ${row} ${m.free ? "יש משבצות פנויות" : "אין משבצת פנויה"}` : "");
        $(".nq-wrap").innerHTML = boardSvg(n, label, (r, c) => {
          let cls = "";
          if (r === row && row < n) cls = (m.free >> c) & 1 ? "is-free" : "is-hit";
          const qn = qs[r] === c ? (sol ? "is-sol" : r === row - 1 && cur ? "is-new" : "") : null;
          return { cls, queen: qn };
        }, "nq-live");
        $(".nq-mtitle").innerHTML = row < n ? `המסכות של שורה ${ltr(row)}, הביט ${ltr("c")} מתחת לעמודה ${ltr("c")}` : `כל השורות מלאות${NB}: ${ltr("cols")} הוא ${ltr(n)} אחדות`;
        $(".nq-masks tbody").innerHTML = `<tr class="nq-bitno"><th>bit</th>${Array.from({ length: n }, (_, i) => `<th>${n - 1 - i}</th>`).join("")}<td></td></tr>` +
          bitsRow("cols", m.cols, n) + bitsRow("left", row < n ? m.left : 0, n) + bitsRow("right", row < n ? m.right : 0, n) + bitsRow("free", row < n ? m.free : 0, n, "is-free");
        $(".nq-sum").innerHTML = cur
          ? `צעד ${ltr(k)}${NB}: מלכה בשורה ${ltr(cur.row)}, עמודה ${ltr(cur.col)}. פתרונות עד כאן${NB}: ${ltr(count)}.`
          : `לוח ריק. בשורה ${ltr(0)} כל ${ltr(n)} העמודות פנויות, והחיפוש מתחיל מהביט הנמוך, העמודה ${ltr(0)} מימין.`;
        let now = "";
        if (cur) {
          const prev = k > 1 ? steps[k - 2] : null;
          if (prev && cur.row <= prev.row) {
            const after = prev.row === n - 1 ? "אחרי הפתרון החיפוש ממשיך" : "בשורות שמתחת לא נשארה עמודה לנסות";
            now = cur.row < prev.row
              ? `${after}, ולכן חוזרים לשורה ${ltr(cur.row)} ומנסים בה את הביט הפנוי הבא${NB}: העמודה ${ltr(cur.col)}.`
              : `${prev.row === n - 1 ? "אחרי הפתרון החיפוש ממשיך" : `העמודה ${ltr(prev.col)} לא הובילה להמשך`}, ולכן מנסים בשורה ${ltr(cur.row)} את הביט הפנוי הבא${NB}: העמודה ${ltr(cur.col)}.`;
          } else now = `הביט הנמוך של ${ltr("free")} בשורה ${ltr(cur.row)} הוא העמודה ${ltr(cur.col)}${NB}: ${ltr(`free & −free = ${1 << cur.col}`)}.`;
          if (sol) now += ` <strong>פתרון מספר ${ltr(count)}.</strong>`;
          else if (!m.free) now += ` בשורה ${ltr(row)} אין משבצת פנויה (${ltr("free = 0")}), ולכן הצעד הבא חוזר אחורה.`;
        }
        $(".nq-now").innerHTML = now;
        if (k === T) answer(box, `החיפוש הציב ${ltr(T)} מלכות ומצא ${ltr(total)} פתרונות של ${ltr(n)} מלכות.`, ".nq-sum");
        else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= st.steps.length, restart: () => { st.k = 0; draw(); } });
      const setN = (n) => { stop(); st.n = n; st.steps = nqSteps(n); st.last = lastSol(st.steps, n); st.k = 0; draw(); };
      $(".nq-n").addEventListener("change", () => setN(clampN($(".nq-n").value, N0)));
      $(".nq-nextsol").addEventListener("click", () => {
        stop();
        const i = st.steps.findIndex((s, j) => j >= st.k && s.row === st.n - 1);
        if (i >= 0) { st.k = i + 1; draw(); }
      });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = st.steps.length; draw(); });
      $(".ex-reset").addEventListener("click", () => setN(N0));
      draw();
    },
  });

  // --- queens placed by hand ---------------------------------------------------------------------

  const nqplaceView = () => ({
    mount(box) {
      const N0 = clampN(box.dataset.n, 8);
      const parse = (text, n) => {
        if (!text) return [];
        const out = [];
        for (const part of String(text).split("_")) {
          const m = /^(\d+)\.(\d+)$/.exec(part);
          if (!m) return null;
          const r = Number(m[1]), c = Number(m[2]);
          if (r >= n || c >= n || out.some(([a, b]) => a === r && b === c)) return null;
          out.push([r, c]);
        }
        return out;
      };
      const Q0 = parse(box.dataset.queens || "", N0) || [];
      const st = { n: N0, qs: Q0.map((q) => q.slice()), fr: 0, fc: 0 };
      box.innerHTML =
        `<div class="ex-controls">` + nSelect(N0, "N, גודל הלוח") +
        `<button type="button" class="md-button md-button--primary nq-fill">השלמה</button>` +
        `<button type="button" class="md-button nq-clear">ניקוי הלוח</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לדוגמה של העמוד</button></div>` +
        `<div class="nq-wrap"></div>` +
        `<span class="viz-legend"><span><i class="nq-key-new"></i>מלכה</span><span><i class="nq-key-bad"></i>מלכה מאוימת</span>` +
        `<span><i class="nq-key-hit"></i>משבצת מאוימת</span><span><i class="nq-key-ghost"></i>השלמה אפשרית</span></span>` +
        `<p class="ex-summary nq-psum" aria-live="polite"></p>` +
        `<p class="nq-pnow"></p>`;
      const $ = (s) => box.querySelector(s);
      const wrap = $(".nq-wrap");
      const has = (r, c) => st.qs.findIndex(([a, b]) => a === r && b === c);
      const state = () => {
        const n = st.n, conf = nqConflicts(st.qs), bad = new Set(conf.flat());
        const done = !conf.length ? nqComplete(n, st.qs) : { count: 0, first: null };
        return { n, conf, bad, done };
      };
      const draw = (focus = false) => {
        const { n, conf, bad, done } = state(), hit = nqAttacked(n, st.qs);
        st.fr = Math.min(st.fr, n - 1); st.fc = Math.min(st.fc, n - 1);
        $(".nq-n").value = String(n);
        $(".nq-fill").disabled = !done.first || st.qs.length === n;
        $(".nq-clear").disabled = !st.qs.length;
        const ghost = done.first && st.qs.length < n ? done.first : null;
        wrap.innerHTML = boardSvg(n, `לוח של ${n} על ${n}, העמודה 0 מימין${NB}: לוחצים על משבצת כדי לשים מלכה או להוריד אותה`, (r, c) => {
          const i = has(r, c), name = i >= 0 ? (bad.has(i) ? "מלכה מאוימת" : "מלכה") : hit.has(`${r},${c}`) ? "ריקה, מאוימת" : ghost && ghost[r] === c ? "ריקה, בהשלמה" : "ריקה";
          return {
            cls: i < 0 && hit.has(`${r},${c}`) ? "is-hit" : "",
            queen: i >= 0 ? (bad.has(i) ? "is-bad" : "is-new") : ghost && ghost[r] === c ? "is-ghost" : null,
            attrs: `role="button" tabindex="${r === st.fr && c === st.fc ? 0 : -1}" data-r="${r}" data-c="${c}" aria-pressed="${i >= 0}" aria-label="שורה ${r}, עמודה ${c}${NB}: ${name}"`,
          };
        }, "nq-live-place");
        if (focus) { const g = wrap.querySelector(`.nq-cell[data-r="${st.fr}"][data-c="${st.fc}"]`); if (g) g.focus(); }
        const k = st.qs.length;
        let sum = `‏${ltr(k)} ${k === 1 ? "מלכה" : "מלכות"} על הלוח. `;
        if (conf.length) {
          const [i, j] = conf[0], a = st.qs[i], b = st.qs[j];
          const why = a[0] === b[0] ? "באותה שורה" : a[1] === b[1] ? "באותה עמודה" : "באותו אלכסון";
          sum += `המלכות ב-${ltr(`(${a[0]}, ${a[1]})`)} וב-${ltr(`(${b[0]}, ${b[1]})`)} ${why}${conf.length > 1 ? `, ועוד ${ltr(conf.length - 1)} ${conf.length > 2 ? "זוגות" : "זוג"}` : ""}.`;
        } else sum += k ? "אין שתי מלכות שמאיימות זו על זו." : "לוחצים על משבצת כדי לשים מלכה.";
        $(".nq-psum").innerHTML = sum;
        let now;
        if (conf.length) now = "אי אפשר להשלים לפתרון, כי כבר יש מלכות שמאיימות זו על זו.";
        else if (k === n) now = `<strong>זה פתרון של ${ltr(n)} מלכות.</strong>`;
        else if (done.count) now = `אפשר להשלים${NB}: ${done.count === 1 ? "בדרך אחת" : `ב-${ltr(done.count)} דרכים`}. ${done.count === 1 ? "היא מסומנת" : "אחת מהן מסומנת"} במלכות שקופות, ו"השלמה" מציבה אותה.`;
        else now = `אי אפשר להשלים${NB}: אין אף פתרון של ${ltr(n)} מלכות שמכיל את ${k === 1 ? "המלכה הזו" : "המלכות האלה"}.` + (k ? "" : " (ל-2 ול-3 אין פתרון בכלל, אבל כאן N לפחות 4.)");
        $(".nq-pnow").innerHTML = now;
        if (k === n && !conf.length) answer(box, `זה פתרון${NB}: ${ltr(n)} מלכות, ואף שתיים לא באותה שורה, עמודה או אלכסון.`, ".nq-psum");
        else answer(box, null);
      };
      const toggle = (r, c) => {
        const i = has(r, c);
        if (i >= 0) st.qs.splice(i, 1); else st.qs.push([r, c]);
        st.fr = r; st.fc = c;
      };
      wrap.addEventListener("click", (e) => {
        const g = e.target.closest(".nq-cell");
        if (!g) return;
        toggle(Number(g.dataset.r), Number(g.dataset.c));
        draw(true);
      });
      wrap.addEventListener("keydown", (e) => {
        const g = e.target.closest(".nq-cell");
        if (!g) return;
        const n = st.n;
        let r = Number(g.dataset.r), c = Number(g.dataset.c);
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); e.stopPropagation(); toggle(r, c); draw(true); return; }
        // column 0 is on the right: the left arrow goes to a higher column
        const moves = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, 1], ArrowRight: [0, -1] };
        if (e.key === "Home") { c = n - 1; } else if (e.key === "End") { c = 0; } else if (moves[e.key]) {
          r = Math.min(n - 1, Math.max(0, r + moves[e.key][0])); c = Math.min(n - 1, Math.max(0, c + moves[e.key][1]));
        } else return;
        e.preventDefault(); e.stopPropagation();
        st.fr = r; st.fc = c;
        wrap.querySelectorAll(".nq-cell").forEach((el) => el.setAttribute("tabindex", "-1"));
        const t = wrap.querySelector(`.nq-cell[data-r="${r}"][data-c="${c}"]`);
        if (t) { t.setAttribute("tabindex", "0"); t.focus(); }
      });
      $(".nq-n").addEventListener("change", () => {
        st.n = clampN($(".nq-n").value, N0);
        st.qs = st.qs.filter(([r, c]) => r < st.n && c < st.n);
        draw();
      });
      $(".nq-fill").addEventListener("click", () => {
        const { done } = state();
        if (!done.first) return;
        st.qs = done.first.map((c, r) => [r, c]);
        draw();
      });
      $(".nq-clear").addEventListener("click", () => { st.qs = []; draw(); });
      $(".ex-reset").addEventListener("click", () => { st.n = N0; st.qs = Q0.map((q) => q.slice()); st.fr = st.fc = 0; draw(); });
      // the queens ride in the link and the remembered state after the controls
      box.dvqExtra = {
        get: () => st.qs.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]).map(([r, c]) => `${r}.${c}`).join("_"),
        set: (text) => { const qs = parse(text, st.n); if (!qs) return false; st.qs = qs; draw(); return true; },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { nqueens: nqueensView, nqplace: nqplaceView },
    help: {
      nqueens: "בוחרים N. כל צעד הוא מלכה אחת שהחיפוש מציב, שורה אחרי שורה, ובכל שורה העמודה של הביט הנמוך הפנוי קודם. על הלוח המלכות עד עכשיו, ובשורה הבאה המשבצות המאוימות והפנויות. מתחת המסכות של השורה הבאה בבינארי, כל ביט מתחת לעמודה שלו (העמודה 0 מימין). כשאין משבצת פנויה החיפוש חוזר אחורה. \"לפתרון הבא\" קופץ לצעד שמשלים את הפתרון הבא.",
      nqplace: "בוחרים N ולוחצים על משבצות כדי לשים מלכות או להוריד אותן (או עוברים בחיצים ולוחצים Enter). המשבצות שהמלכות מאיימות עליהן צבועות, ומלכות שמאיימות זו על זו מסומנות. מתחת ללוח כתוב אם אפשר להשלים את המלכות לפתרון ובכמה דרכים. השלמה אחת מסומנת במלכות שקופות, ו\"השלמה\" מציבה אותה.",
    },
    models: { nqSteps, nqQueens, nqMasks, nqConflicts, nqAttacked, nqComplete },
  });
})();
