// kinds: overtakes
//   overtakes              0069        the response times of n requests (data-done) and three modes: a, passed[i] by a Fenwick tree over the ranks walked from the last request (a query step and an update step per request); b, overtook[i] walked from the first request; c, the stream: the responses in arrival order, the tree over the send indices, the live report of every arrival, the running total and the disorder. The requests and their responses with the crossing lines above, the tree with the ranges its cells cover under it, the query path and the update path lit, the counts under the requests
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, explain, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMAX = 16, VMAX = 99;

  const lowbit = (i) => i & -i;
  const ovRanks = (done) => {
    const rk = {};
    [...new Set(done)].sort((a, b) => a - b).forEach((v, r) => { rk[v] = r + 1; });
    return rk;
  };
  const ovOrder = (done) => done.map((v, i) => i).sort((a, b) => done[a] - done[b] || a - b);
  // A Fenwick tree over 1..n that remembers the cells of its last walk, as Fen in
  // tools/figures/q0069.py.
  const fen = (n) => {
    const tree = Array(n + 1).fill(0);
    return {
      tree,
      add(i) { const path = []; while (i <= n) { tree[i]++; path.push(i); i += lowbit(i); } return path; },
      prefix(i) { let s = 0; const path = []; while (i > 0) { s += tree[i]; path.push(i); i -= lowbit(i); } return [s, path]; },
    };
  };
  // The walk of a mode, a row per request, as walk_passed(), walk_overtook() and
  // walk_live() of the generator: the request i, its time v, its rank (the send index + 1
  // in mode c), how many are in the tree, the query's argument, result and path, the
  // update's path, the count, the running total and the tree after the update.
  const ovWalk = (done, mode) => {
    const n = done.length, rows = [], pairs = n * (n - 1) / 2;
    const rk = mode === "c" ? null : ovRanks(done);
    const ft = fen(mode === "c" ? n : Object.keys(rk).length);
    const seq = mode === "a" ? done.map((_, i) => n - 1 - i) : mode === "b" ? done.map((_, i) => i) : ovOrder(done);
    let total = 0;
    seq.forEach((i, k) => {
      const r = mode === "c" ? i + 1 : rk[done[i]], arg = mode === "a" ? r - 1 : r;
      const [q, qpath] = ft.prefix(arg);
      const upath = ft.add(r);
      const count = mode === "a" ? q : k - q;
      total += count;
      rows.push({ k, i, v: done[i], rank: r, inserted: k, arg, q, qpath, upath, count, total, disorder: pairs ? total / pairs : 0, tree: ft.tree.slice(1) });
    });
    return rows;
  };

  const parse = (text) => {
    const toks = String(text).trim().split(/[\s,;]+/).filter(Boolean);
    if (!toks.length || toks.length > NMAX || !toks.every((t) => /^\d+$/.test(t))) return null;
    const v = toks.map(Number);
    return v.every((x) => x <= VMAX) ? v : null;
  };

  const MODES = { a: "כמה עקפו כל בקשה (סעיף א)", b: "כמה כל בקשה עקפה (סעיף ב)", c: "הזרם, בזמן אמת (סעיף ג)" };
  const NAME = { a: "passed", b: "overtook", c: "passed" };
  const CODE = { a: "passed", b: "overtook", c: "live_overtakes" };
  const STEPS = {
    a: ["דרגות", "עץ ריק", "מהסוף להתחלה", `שאילתה${NB}: prefix(r − 1)`, `עדכון${NB}: add(r)`],
    b: ["דרגות ועץ ריק", "מההתחלה לסוף", `שאילתה${NB}: prefix(r)`, `ההשלמה${NB}: i − prefix(r)`, `עדכון${NB}: add(r)`],
    c: ["סך העקיפות", "אי-הסדר", `הזרם${NB}: לפי סדר ההגעה`, `דיווח${NB}: k − prefix(i + 1)`, `עדכון${NB}: add(i + 1)`],
  };
  const LINES = {
    a: { start: { py: [29, 30, 31], sv: [38, 39, 40, 41, 42] }, q: { py: [32, 33, 14, 15, 16, 17, 18, 19], sv: [43, 44, 17, 18, 19, 20, 21, 22, 23, 24] }, u: { py: [34, 9, 10, 11, 12], sv: [45, 11, 12, 13, 14, 15, 16] }, end: { py: [35], sv: [] } },
    b: { start: { py: [3, 4, 5], sv: [3, 4, 5, 6, 7] }, q: { py: [6, 7], sv: [8, 9] }, u: { py: [8], sv: [10] }, end: { py: [9], sv: [] } },
    c: { start: { py: [27, 28], sv: [30, 31, 32] }, q: { py: [29, 30], sv: [33, 34] }, u: { py: [31], sv: [35] }, end: { py: [32], sv: [] } },
  };
  const LIT = { a: { start: [1, 2], q: [3, 4], u: [5] }, b: { start: [1], q: [2, 3, 4], u: [5] }, c: { start: [3], q: [3, 4], u: [5, 1, 2] } };
  const cells = (path) => path.map((i) => `tree[${i}]`).join(" → ");
  const list = (a) => `[${a.join(", ")}]`;

  // --- drawing ------------------------------------------------------------------------
  const CELL = 40, LW = 64;
  const open = (W, H, cls, label) => `<svg class="figure ov-fig ov-live ${cls}" viewBox="0 0 ${W} ${H}" style="min-width:${Math.round(W * 0.72)}px;max-width:${Math.round(W * 1.15)}px" role="img" aria-label="${label}">`;
  const cx = (p) => LW + p * CELL + CELL / 2;

  // the requests in send order with their times, the responses in arrival order, a line
  // from each request to its response; the current request, the lines it crosses that the
  // step counts, and the counts found so far under the requests
  const svgCross = (done, mode, rows, step) => {
    const n = done.length, order = ovOrder(done), pos = {}, W = LW + n * CELL + 8, H = 190;
    order.forEach((i, p) => { pos[i] = p; });
    const row = step ? rows[Math.ceil(step / 2) - 1] : null, cur = row ? row.i : -1;
    const found = {};
    rows.slice(0, Math.ceil(step / 2)).forEach((r) => { found[r.i] = r.count; });
    const counted = (j) => row && (mode === "b" ? j < cur && done[j] > done[cur] : j > cur && done[j] < done[cur]);
    const seen = (j) => (mode === "a" ? j > cur : mode === "b" ? j < cur : pos[j] < pos[cur]);
    let s = open(W, H, "ov-cross", `הבקשות לפי סדר השליחה עם זמני התשובה, התשובות לפי סדר ההגעה, קו מכל בקשה לתשובה שלה, ו-${NAME[mode]} של כל בקשה`);
    s += `<text class="tick" x="${LW - 8}" y="12" text-anchor="end">i</text><text class="ov-lab" x="${LW - 8}" y="39" text-anchor="end">done</text>` +
      `<text class="ov-lab" x="${LW - 8}" y="111" text-anchor="end">arrive</text><text class="tick" x="${LW - 8}" y="138" text-anchor="end">time</text>` +
      `<text class="ov-lab" x="${LW - 8}" y="171" text-anchor="end">${NAME[mode]}</text>`;
    for (let i = 0; i < n; i++) s += `<text class="tick" x="${cx(i)}" y="12" text-anchor="middle">${i}</text>`;
    for (let i = 0; i < n; i++) {
      const cls = i === cur ? " is-cur" : counted(i) ? " is-counted" : row && !seen(i) ? " is-later" : "";
      s += `<line class="ov-line${cls}" x1="${cx(i)}" y1="48" x2="${cx(pos[i])}" y2="94"><title>request ${i}: answered at ${done[i]}, slot ${pos[i]} of the answers</title></line>`;
    }
    done.forEach((v, i) => {
      const cls = i === cur ? " is-cur" : counted(i) ? " is-counted" : row && !seen(i) ? " is-later" : "";
      s += `<g class="ov-cell is-req${cls}"><title>request ${i}, answered at time ${v}</title><rect x="${LW + i * CELL + 4}" y="20" width="${CELL - 8}" height="28" rx="4"/><text x="${cx(i)}" y="39" text-anchor="middle">${v}</text></g>`;
    });
    order.forEach((i, p) => {
      const cls = i === cur ? " is-cur" : counted(i) ? " is-counted" : row && !seen(i) ? " is-later" : "";
      s += `<g class="ov-cell is-rsp${cls}"><title>answer slot ${p}: request ${i}, time ${done[i]}</title><rect x="${LW + p * CELL + 4}" y="94" width="${CELL - 8}" height="28" rx="4"/><text x="${cx(p)}" y="113" text-anchor="middle">${i}</text></g>` +
        `<text class="tick" x="${cx(p)}" y="138" text-anchor="middle">${done[i]}</text>`;
    });
    for (let i = 0; i < n; i++) {
      const has = i in found, c = has ? found[i] : "";
      const cls = !has ? " is-empty" : c === 0 ? " is-zero" : "";
      s += `<g class="ov-cnt${cls}${i === cur ? " is-cur" : ""}"><title>${NAME[mode]}[${i}]${has ? ` = ${c}` : ": not counted yet"}</title><rect x="${LW + i * CELL + 4}" y="152" width="${CELL - 8}" height="28" rx="4"/><text x="${cx(i)}" y="171" text-anchor="middle">${c}</text></g>`;
    }
    return s + "</svg>";
  };

  // the Fenwick array: a bar over the range each cell covers, the values, the index and its
  // binary, and under them what the index stands for (a time, or a request); the cells the
  // query read (is-q) and the update raised (is-u)
  const svgTree = (m, tree, qpath, upath, under) => {
    const levels = m.toString(2).length, BAR = 14, LVL = 16, top = 8 + levels * LVL, H = top + 30 + 54, W = LW + m * CELL + 8;
    const tx = (i) => LW + (i - 1) * CELL + CELL / 2;
    let s = open(W, H, "ov-fw", "מערך Fenwick : מעל כל תא הטווח שהוא מכסה, בתא הערך, ומתחתיו האינדקס, הבינארי שלו ומה הוא מייצג");
    s += `<text class="ov-lab" x="${LW - 8}" y="${top + 19}" text-anchor="end">tree[i]</text><text class="tick" x="${LW - 8}" y="${top + 44}" text-anchor="end">i</text>` +
      `<text class="tick" x="${LW - 8}" y="${top + 57}" text-anchor="end">binary</text><text class="tick" x="${LW - 8}" y="${top + 71}" text-anchor="end">${under[0]}</text>`;
    for (let i = 1; i <= m; i++) {
      const lb = lowbit(i), lvl = lb.toString(2).length - 1, y = top - 4 - (lvl + 1) * LVL + (LVL - BAR), x0 = LW + (i - lb) * CELL + 3;
      const cls = qpath.includes(i) ? " is-q" : upath.includes(i) ? " is-u" : "";
      s += `<g class="ov-bar${cls}"><title>tree[${i}] covers ${i - lb + 1}..${i}</title><rect x="${x0}" y="${y}" width="${lb * CELL - 6}" height="${BAR}" rx="3"/>` +
        `<text x="${x0 + (lb * CELL - 6) / 2}" y="${y + 11}" text-anchor="middle">${lb > 1 ? `${i - lb + 1}..${i}` : i}</text></g>`;
      s += `<g class="ov-tc${cls}"><title>tree[${i}] = ${tree[i - 1]}</title><rect x="${LW + (i - 1) * CELL + 4}" y="${top}" width="${CELL - 8}" height="28" rx="4"/><text x="${tx(i)}" y="${top + 19}" text-anchor="middle">${tree[i - 1]}</text></g>`;
      s += `<text class="tick${cls}" x="${tx(i)}" y="${top + 44}" text-anchor="middle">${i}</text><text class="ov-bin" x="${tx(i)}" y="${top + 57}" text-anchor="middle">${i.toString(2).padStart(levels, "0")}</text>` +
        `<text class="tick" x="${tx(i)}" y="${top + 71}" text-anchor="middle">${under[1][i - 1]}</text>`;
    }
    return s + "</svg>";
  };

  const view = () => ({
    mount(box) {
      const mode0 = MODES[box.dataset.mode] ? box.dataset.mode : "a";
      const d0 = { mode: mode0, done: parse(box.dataset.done || "5 2 6 1") || [5, 2, 6, 1] };
      const st = { mode: d0.mode, done: d0.done.slice(), s: 0, n: 8 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המצב <select class="ov-mode" aria-label="איזה סעיף">${Object.entries(MODES).map(([v, w]) => `<option value="${v}">${w}</option>`).join("")}</select></label>` +
        `<label><span>זמני התשובה</span><input type="text" class="ex-num ov-done" dir="ltr" spellcheck="false" aria-label="זמני התשובה : עד ${NMAX} מספרים שלמים בין 0 ל-${VMAX}, מופרדים ברווח"></label>` +
        `<label>בהגרלה <select class="ov-n" aria-label="כמה בקשות להגריל">${[6, 8, 12, 16].map((v) => `<option value="${v}"${v === 8 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ov-rand">הגרלה</button><span class="ov-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err ov-err" role="status"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary ov-sum" aria-live="polite"></p>` +
        `<div class="ov-wrap" data-fig-strip></div>` +
        `<span class="viz-legend"><span><i class="ov-key-cur"></i>הבקשה של הצעד</span><span><i class="ov-key-counted"></i>העקיפות שהצעד סופר</span>` +
        `<span><i class="ov-key-later"></i>עוד לא בעץ</span><span><i class="ov-key-cnt"></i>הספירה שנמצאה</span>` +
        `<span><i class="ov-key-q"></i>תאים שהשאילתה קוראת</span><span><i class="ov-key-u"></i>תאים שהעדכון מגדיל</span></span>` +
        `<div class="ov-wrap ov-treewrap"></div>` +
        `<p class="ov-note"></p><p class="ov-tally"></p>`;
      const show = explain(box, `הסבר${NB}: השלבים של הפתרון והקוד`);
      answer(box, NB); answer(box, null);           // the answer line keeps its place from the first step
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const rows = () => ovWalk(st.done, st.mode);
      const draw = () => {
        const R = rows(), done = st.done, n = done.length, m = st.mode, N = 2 * n;
        st.s = Math.min(Math.max(st.s, 0), N);
        const k = Math.ceil(st.s / 2) - 1, row = st.s ? R[k] : null, ph = st.s ? (st.s % 2 ? "q" : "u") : "start", fin = st.s === N;
        $(".ov-mode").value = m; $(".ov-done").value = done.join(" ");
        $(".ex-pos").textContent = `צעד ${st.s} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = fin;
        const rk = m === "c" ? null : ovRanks(done), vals = m === "c" ? null : Object.keys(rk).map(Number).sort((a, b) => a - b);
        const M = m === "c" ? n : vals.length, pairs = n * (n - 1) / 2;
        const under = m === "c" ? ["request", done.map((_, i) => i)] : ["time", vals];
        const tree = row ? (ph === "q" ? (k ? R[k - 1].tree : Array(M).fill(0)) : row.tree) : Array(M).fill(0);
        $(".ov-wrap:not(.ov-treewrap)").innerHTML = svgCross(done, m, R, st.s);
        $(".ov-treewrap").innerHTML = svgTree(M, tree, row && ph === "q" ? row.qpath : [], row && ph === "u" ? row.upath : [], under);
        const soFar = R.slice(0, k + (ph === "u" ? 1 : 0));
        const sum = soFar.reduce((a, r) => a + r.count, 0), mx = soFar.reduce((a, r) => Math.max(a, r.count), 0);
        let summ, note = "", tally, vars, ans = null;
        const who = (m === "a" || m === "c") ? "מאוחרות ממנה נענו לפניה" : "מוקדמות ממנה נענו אחריה";
        if (!row) {
          summ = m === "c" ? `${ltr(n)} בקשות, התשובות מגיעות בסדר ${ltr(ovOrder(done).join(" "))}. העץ על אינדקסי השליחה, ${ltr(n)} תאים.`
            : `${ltr(n)} בקשות, הזמנים ${ltr(done.join(" "))}. ${m === "a" ? "מהאחרונה לראשונה" : "מהראשונה לאחרונה"}, שני צעדים לבקשה${NB}: שאילתה ועדכון.`;
          if (m !== "c") note = `דחיסה לדרגות${NB}: הערכים השונים ממוינים הם ${ltr(vals.join(" "))}, ולכן הדרגות הן ${ltr(done.map((v) => rk[v]).join(" "))}. העץ מכסה ${ltr(`1..${M}`)}, וכולו אפסים.`;
          else note = `אין דחיסה${NB}: הדרגה של בקשה ${ltr("i")} היא ${ltr("i + 1")}, כי אינדקסי השליחה כבר רצופים. העץ ריק, ואף תשובה עוד לא הגיעה.`;
          vars = m === "c" ? ltr(`n = ${n}, tree = ${list(Array(M).fill(0))}, k = 0`) : ltr(`ranks = {${vals.map((v) => `${v}: ${rk[v]}`).join(", ")}}, tree = ${list(Array(M).fill(0))}`);
        } else {
          const { i, v, rank: r, q, count } = row, kk = row.inserted;
          summ = m === "c" ? `התשובה ה-${ltr(kk)}, של בקשה ${ltr(i)} (זמן ${ltr(v)})${NB}: ${ph === "q" ? "השאילתה" : "העדכון"}. הסכום הרץ${NB}: <b>${ltr(ph === "u" ? row.total : (k ? R[k - 1].total : 0))}</b>.`
            : `בקשה ${ltr(i)} (זמן ${ltr(v)}, דרגה ${ltr(r)})${NB}: ${ph === "q" ? "השאילתה" : "העדכון"}. ${ltr(`${NAME[m]}[${i}] = ${count}`)}.`;
          if (ph === "q") {
            const read = row.qpath.length ? `קוראת את ${ltr(cells(row.qpath))}` : "לא קוראת אף תא";
            if (m === "a") note = `בעץ כבר ${ltr(kk)} דרגות, של הבקשות המאוחרות מ-${ltr(i)}. ${ltr(`prefix(${row.arg})`)} סופרת דרגות קטנות ממש מ-${ltr(r)}${NB}: ${read}, ומקבלת <b>${ltr(q)}</b>. ` +
              `${q ? `${ltr(q)} בקשות ${who}, ולכן` : `אף בקשה מאוחרת לא נענתה לפניה${NB}:`} ${ltr(`passed[${i}] = ${q}`)}. (כל קפיצה מורידה את הביט הנמוך${NB}: ${ltr(row.qpath.length ? row.qpath.concat(0).join(" → ") : "0")}.)`;
            else if (m === "b") note = `בעץ ${ltr(kk)} דרגות, של הבקשות ${ltr(`0..${i - 1}`)}. ${ltr(`prefix(${r})`)} סופרת דרגות עד ${ltr(r)} ועד בכלל${NB}: ${read}, ומקבלת ${ltr(q)}${NB}: ` +
              `כל כך הרבה בקשות מוקדמות נענו לא אחריה. השאר, ${ltr(`${kk} − ${q} = ${count}`)}, ${count ? `${who}${NB}: אותן היא עקפה` : "אין, היא לא עקפה אף אחת"}. ${ltr(`overtook[${i}] = ${count}`)}.`;
            else note = `כבר ענו ${ltr(kk)} בקשות (בעץ). ${ltr(`prefix(${i + 1})`)} סופרת מהן את אלה שנשלחו עד ${ltr(i)} ועד בכלל${NB}: ${read}, ומקבלת ${ltr(q)}. השאר, ${ltr(`${kk} − ${q} = ${count}`)}, נשלחו אחרי ${ltr(i)} ונענו לפניה${NB}: ` +
              `${ltr(`passed[${i}] = ${count}`)}, ידוע ברגע שהתשובה הגיעה.`;
            vars = [ltr(m === "c" ? `k = ${kk}` : `i = ${i}`), ltr(m === "c" ? `i = ${i}` : `r = ${r}`), ltr(`prefix(${row.arg}) = ${q}`), ltr(`${NAME[m]}[${i}] = ${count}`), ltr(`tree = ${list(tree)}`)].join(" · ");
          } else {
            note = `${ltr(`add(${r})`)} מגדילה ב-1 את ${ltr(cells(row.upath))}${NB}: כל התאים שהבלוק שלהם מכיל את ${ltr(r)}, מ-${ltr(r)} והלאה ב-${ltr("i += i & −i")} (${ltr(row.upath.concat(row.upath[row.upath.length - 1] + lowbit(row.upath[row.upath.length - 1])).join(" → "))}, עד מעבר ל-${ltr(M)}). ` +
              (m === "a" ? `מעכשיו בקשה ${ltr(i)} נספרת בשאילתות של הבקשות שלפניה.` : m === "b" ? `מעכשיו בקשה ${ltr(i)} נספרת בשאילתות של הבקשות שאחריה.` : `הסכום הרץ${NB}: ${ltr(`${row.total - count} + ${count} = ${row.total}`)}, ואי-הסדר ${ltr(`${row.total}/${pairs} ≈ ${row.disorder.toFixed(2)}`)}.`);
            vars = [ltr(m === "c" ? `k = ${kk}` : `i = ${i}`), ltr(`add(${r})`), ltr(`tree = ${list(row.tree)}`), ...(m === "c" ? [ltr(`total = ${row.total}`)] : [])].join(" · ");
          }
        }
        if (m === "c") {
          const tot = soFar.length ? soFar[soFar.length - 1].total : 0;
          tally = `סך העקיפות עד עכשיו${NB}: ${ltr(tot)} מתוך ${ltr(`n(n − 1)/2 = ${pairs}`)} זוגות, אי-סדר ${ltr(pairs ? (tot / pairs).toFixed(2) : "0")}. ‏0 הוא סדר מלא, 1 סדר הפוך לגמרי.`;
        } else {
          tally = `עד עכשיו${NB}: הסכום ${ltr(sum)} והמקסימום ${ltr(mx)} של ${ltr(NAME[m])}. ${m === "a" ? "המקסימום הוא עומק הסידור מחדש, והסכום הוא סך העקיפות." : "הסכום שווה לסכום של passed, כי שניהם סופרים את אותם זוגות."}`;
        }
        const lines = LINES[m][ph], lit = LIT[m][ph];
        if (fin && row) {
          const arr = R.slice().sort((a, b) => a.i - b.i).map((r) => r.count);
          ans = m === "c" ? `סך העקיפות ${ltr(row.total)}, אי-סדר ${ltr(`${row.total}/${pairs} ≈ ${row.disorder.toFixed(2)}`)}; ‏${ltr(`passed = ${list(arr)}`)}, מדווח תשובה אחרי תשובה.`
            : `${ltr(`${NAME[m]} = ${list(arr)}`)}, הסכום ${ltr(sum)}${m === "a" ? `, המקסימום ${ltr(mx)}` : ""}.`;
        }
        $(".ov-sum").innerHTML = summ;
        $(".ov-note").innerHTML = note;
        $(".ov-tally").innerHTML = tally;
        show({ code: CODE[m], steps: STEPS[m], lit, lines: fin ? { py: lines.py.concat(LINES[m].end.py), sv: lines.sv.concat(LINES[m].end.sv) } : lines, vars });
        answer(box, ans, ".ov-cross .ov-cnt");
      };
      const total = () => 2 * st.done.length;
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= total(), restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; $(".ov-err").textContent = ""; draw(); };
      $(".ov-mode").addEventListener("change", () => { st.mode = MODES[$(".ov-mode").value] ? $(".ov-mode").value : "a"; restart(); });
      $(".ov-done").addEventListener("change", () => {
        const v = parse($(".ov-done").value);
        if (!v) { $(".ov-err").textContent = `זמני התשובה${NB}: 1 עד ${NMAX} מספרים שלמים בין 0 ל-${VMAX}`; return; }
        st.done = v; restart();
      });
      $(".ov-done").addEventListener("keydown", (ev) => { if (ev.key === "Enter") $(".ov-done").blur(); });
      $(".ov-n").addEventListener("change", () => { st.n = Number($(".ov-n").value); });
      const seed = seedControls(box, $(".ov-anchor"), (rng) => {
        // a random arrival order with a few equal times: n times out of 1..2n
        st.done = Array.from({ length: st.n }, () => 1 + Math.floor(rng() * 2 * st.n));
        restart();
      }, { fresh: false });
      $(".ov-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, { mode: d0.mode, done: d0.done.slice(), n: 8 }); $(".ov-n").value = "8"; restart(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { overtakes: view },
    help: {
      overtakes: `מקלידים את זמני התשובה של הבקשות (או מגרילים) ובוחרים סעיף. למעלה הבקשות לפי סדר השליחה והתשובות לפי סדר ההגעה, עם קו מכל בקשה לתשובה שלה${NB}: קווים שחוצים זה את זה הם עקיפות. למטה עץ Fenwick עם הטווח שכל תא מכסה. לכל בקשה שני צעדים${NB}: שאילתה (התאים שנקראים כחולים) ועדכון (התאים שגדלים כתומים), והספירה נכתבת מתחת לבקשה. בסעיף א הולכים מהבקשה האחרונה לראשונה, בסעיף ב מהראשונה לאחרונה, ובסעיף ג לפי סדר ההגעה של התשובות, עם הסכום הרץ ואי-הסדר. השורה שמתחת מסבירה כל צעד, והפאנל 'הסבר' מדליק את שורות הקוד.`,
    },
    models: { ovWalk, ovRanks, ovOrder },
  });
})();
