// kinds: netdelay
//   netdelay               0067        a network of n nodes on a circle (data-n, data-edges "u-v-w ...", data-k) and three modes: a, the BFS of delay_bfs with the queue beside the graph, every pop and every link checked its own step; b, the Dijkstra of delay_dijkstra with the heap (sorted) beside the graph, the stale entries skipped; c, the same Dijkstra on one-directional links (arrows), the unreachable nodes marked at the end; ready graphs (the page's example, a line, a ring, a tree, a dense one), a random one from a seed, the source and the weights editable
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, explain, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMIN = 3, NMAX = 8, WMAX = 99;

  // --- the two searches, event by event, as tools/figures/q0067.py -------------------------
  // adj[u] = [[v, w, i], ...] in the order of the edge list (i its index); an undirected
  // link is entered from both ends, an unweighted one weighs 1.
  const ndAdj = (n, edges, directed, weighted) => {
    const adj = Array.from({ length: n + 1 }, () => []);
    edges.forEach((e, i) => {
      const w = weighted ? e[2] : 1;
      adj[e[0]].push([e[1], w, i]);
      if (!directed) adj[e[1]].push([e[0], w, i]);
    });
    return adj;
  };
  const answerOf = (t) => (t.some((x) => x === null) ? -1 : Math.max(...t));
  // Part a: a pop takes the front of the queue, a relax checks one link out of it (the
  // neighbour gets t[u] + 1 and enters the queue if it had no time yet), done gives the
  // answer. Every event keeps the times after it (null for none), the queue and the order.
  const ndBfs = (n, edges, k) => {
    const adj = ndAdj(n, edges, false, false), t = Array(n + 1).fill(null), q = [k], order = [], ev = [];
    t[k] = 0;
    const rec = (e) => ev.push({ ...e, t: t.slice(1), q: q.slice(), order: order.slice() });
    while (q.length) {
      const u = q.shift();
      order.push(u);
      rec({ kind: "pop", u, d: t[u] });
      adj[u].forEach(([v, , i]) => {
        const improved = t[v] === null;
        if (improved) { t[v] = t[u] + 1; q.push(v); }
        rec({ kind: "relax", u, v, w: 1, i, nd: t[u] + 1, improved });
      });
    }
    rec({ kind: "done", ans: answerOf(t.slice(1)) });
    return ev;
  };
  // Parts b and c: a pop takes the smallest (time, node) of the heap and settles the node,
  // a skip drops an entry of a node settled with a smaller time, a relax checks one link
  // out of the settled node, done gives the answer. The heap is kept sorted by (time, node),
  // which pops in the order of Python's heapq on the same pairs.
  const ndDijkstra = (n, edges, k, directed) => {
    const adj = ndAdj(n, edges, directed, true), t = Array(n + 1).fill(null), heap = [[0, k]], settled = [], ev = [];
    t[k] = 0;
    const rec = (e) => ev.push({ ...e, t: t.slice(1), heap: heap.map((x) => x.slice()), settled: settled.slice() });
    const push = (d, v) => {
      let pos = 0;
      while (pos < heap.length && (heap[pos][0] < d || (heap[pos][0] === d && heap[pos][1] < v))) pos++;
      heap.splice(pos, 0, [d, v]);
    };
    while (heap.length) {
      const [d, u] = heap.shift();
      if (d > t[u]) { rec({ kind: "skip", u, d }); continue; }
      settled.push(u);
      rec({ kind: "pop", u, d });
      adj[u].forEach(([v, w, i]) => {
        const nd = d + w, old = t[v], improved = old === null || nd < old;
        if (improved) { t[v] = nd; push(nd, v); }
        rec({ kind: "relax", u, v, w, i, nd, old, improved });
      });
    }
    rec({ kind: "done", ans: settled.length < n ? -1 : Math.max(...t.slice(1)) });
    return ev;
  };

  // --- the graphs ----------------------------------------------------------------------
  const EXAMPLE = { n: 6, k: 1, edges: [[1, 2, 1], [1, 3, 5], [3, 2, 1], [3, 4, 2], [2, 5, 6], [4, 5, 1], [6, 5, 1]] };
  const wOf = (u, v) => ((u * 3 + v * 5) % 9) + 1;
  const READY = {
    line: (n) => Array.from({ length: n - 1 }, (_, i) => [i + 1, i + 2, wOf(i + 1, i + 2)]),
    ring: (n) => Array.from({ length: n }, (_, i) => [i + 1, (i + 1) % n + 1, wOf(i + 1, (i + 1) % n + 1)]),
    tree: (n) => Array.from({ length: n - 1 }, (_, i) => [Math.floor((i + 2) / 2), i + 2, wOf(Math.floor((i + 2) / 2), i + 2)]),
    dense: (n) => { const E = []; for (let u = 1; u <= n; u++) for (let v = u + 1; v <= n; v++) E.push([u, v, wOf(u, v)]); return E; },
  };
  const GRAPHS = { example: "הדוגמה של העמוד", line: "קו", ring: "טבעת", tree: "עץ", dense: "צפוף", random: "אקראי" };
  // a random graph: between n − 1 and 2n − 2 distinct links in a random direction, weights
  // 1 to 9; not always connected, so −1 comes up
  const ndRandomGraph = (rng, n) => {
    const pairs = [];
    for (let u = 1; u <= n; u++) for (let v = u + 1; v <= n; v++) pairs.push([u, v]);
    for (let i = pairs.length - 1; i > 0; i--) { const j = Math.floor(rng() * (i + 1)); [pairs[i], pairs[j]] = [pairs[j], pairs[i]]; }
    const m = Math.min(pairs.length, n - 1 + Math.floor(rng() * n));
    return pairs.slice(0, m).map(([u, v]) => (rng() < 0.5 ? [u, v, 1 + Math.floor(rng() * 9)] : [v, u, 1 + Math.floor(rng() * 9)]));
  };
  const parseEdges = (text, n) => {
    const out = [];
    for (const tok of String(text || "").trim().split(/\s+/).filter(Boolean)) {
      const p = tok.split("-").map(Number);
      if (p.length < 2 || p.some((x) => !Number.isInteger(x)) || p[0] < 1 || p[1] < 1 || p[0] > n || p[1] > n) return null;
      out.push([p[0], p[1], p.length > 2 ? p[2] : 1]);
    }
    return out;
  };

  // --- drawing -------------------------------------------------------------------------
  const GW = 300, CX = 150, CY = 136, R = 82, NR = 16, PW = 104, ROW = 22, PTOP = 44;
  const pos = (i, n) => { const a = -Math.PI / 2 + (i - 1) * 2 * Math.PI / n; return [CX + R * Math.cos(a), CY + R * Math.sin(a), a]; };
  const f1 = (x) => x.toFixed(1);
  const num = (v) => (v === null || v === undefined ? "–" : String(v).replace("-", "−"));
  const pair = (d, v) => `(${d},${v})`;

  // the graph on the left: every link with its weight (an arrowhead when directed), the
  // links of the shortest-path tree so far thick, the link being checked lit; every node
  // by its state (source, settled, with a time, without), the one of the moment ringed,
  // its time in a badge outside the circle (light while it may still improve); and on
  // the right the queue or the heap, the entry taken out in the slot above it
  const svg = (st, e, F, rows) => {
    const { n, edges, k } = st, directed = st.mode === "c", weighted = st.mode !== "a";
    const H = Math.max(268, PTOP + (rows + 1) * ROW + 10), W = GW + PW;
    const t = e ? e.t : Array.from({ length: n }, (_, i) => (i + 1 === k ? 0 : null));
    const settled = new Set(e ? (st.mode === "a" ? e.order : e.settled) : []);
    const cur = e && e.kind !== "done" ? e.u : null;
    const tree = {};
    F.forEach((x) => { if (x.kind === "relax" && x.improved) tree[x.v] = x.i; });
    const mx = e && e.kind === "done" && e.ans >= 0 ? e.ans : null;
    let s = `<svg class="figure nd-fig nd-live" viewBox="0 0 ${W} ${H}" style="max-width:${Math.round(W * 1.15)}px" role="img" ` +
      `aria-label="הרשת על מעגל עם ${st.mode === "a" ? "התור" : "הערימה"} לידה : המקור ${k}, הזמנים בתוויות, הצומת של הצעד מוקף והקשת שנבדקת מודגשת">`;
    const P = {};
    for (let i = 1; i <= n; i++) P[i] = pos(i, n);
    edges.forEach(([u, v, w], i) => {
      const [x1, y1] = P[u], [x2, y2] = P[v];
      const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
      const ax = x1 + ux * NR, ay = y1 + uy * NR, cut = NR + (directed ? 7 : 0), bx = x2 - ux * cut, by = y2 - uy * cut;
      const isTree = Object.values(tree).includes(i), now = e && e.kind === "relax" && e.i === i;
      const cls = `nd-edge${isTree ? " is-tree" : ""}${now ? (e.improved ? " is-relax is-better" : " is-relax is-same") : ""}`;
      s += `<g class="${cls}"><title>link ${u} ${directed ? "→" : "–"} ${v}${weighted ? `, weight ${w}` : ""}</title><line x1="${f1(ax)}" y1="${f1(ay)}" x2="${f1(bx)}" y2="${f1(by)}"/>`;
      if (directed) s += `<path class="nd-head" d="M${f1(bx + ux * 7)},${f1(by + uy * 7)} L${f1(bx - uy * 4.5)},${f1(by + ux * 4.5)} L${f1(bx + uy * 4.5)},${f1(by - ux * 4.5)} Z"/>`;
      if (weighted) {
        const mxx = (x1 + x2) / 2 - uy * 9, myy = (y1 + y2) / 2 + ux * 9;
        s += `<rect class="nd-wbox" x="${f1(mxx - 8)}" y="${f1(myy - 8)}" width="16" height="16" rx="4"/><text class="nd-w" x="${f1(mxx)}" y="${f1(myy + 4)}" text-anchor="middle">${w}</text>`;
      }
      s += "</g>";
    });
    const done = e && e.kind === "done";
    for (let i = 1; i <= n; i++) {
      const [x, y, a] = P[i], ti = t[i - 1];
      const kind = i === k ? "is-src" : settled.has(i) ? "is-set" : ti !== null ? "is-open" : done ? "is-far" : "is-none";
      const what = i === k ? "the source" : settled.has(i) ? `settled, time ${ti}` : ti !== null ? `time ${ti} so far` : done ? "no path reaches it" : "no time yet";
      s += `<g class="nd-node ${kind}${i === cur ? " is-cur" : ""}"><title>node ${i}: ${what}</title><circle cx="${f1(x)}" cy="${f1(y)}" r="${NR}"/><text x="${f1(x)}" y="${f1(y + 5)}" text-anchor="middle">${i}</text></g>`;
      const bx = CX + (R + 34) * Math.cos(a), by = CY + (R + 34) * Math.sin(a);
      const tk = ti === null ? (done ? " is-far" : " is-empty") : settled.has(i) || st.mode === "a" ? "" : " is-tent";
      s += `<g class="nd-time${tk}${mx !== null && ti === mx ? " is-max" : ""}"><rect x="${f1(bx - 15)}" y="${f1(by - 9)}" width="30" height="18" rx="5"/>` +
        `<text x="${f1(bx)}" y="${f1(by + 4)}" text-anchor="middle">${ti === null ? (done ? "−1" : "") : ti}</text></g>`;
    }
    // the panel
    const px = GW + 10;
    s += `<text class="nd-lab" x="${px}" y="18">${st.mode === "a" ? "queue" : "heap (t, v)"}</text>`;
    const slotKind = !e ? "" : e.kind === "skip" ? " is-stale" : e.kind === "done" ? " is-off" : " is-now";
    const slotText = !e || e.kind === "done" ? "" : st.mode === "a" ? `out: ${e.u}` : `out: ${pair(e.kind === "relax" ? e.t[e.u - 1] : e.d, e.u)}`;
    s += `<g class="nd-slot${slotKind}"><rect x="${px}" y="26" width="${PW - 20}" height="18" rx="4"/><text x="${px + (PW - 20) / 2}" y="39" text-anchor="middle">${slotText}</text></g>`;
    if (e && e.kind === "skip") s += `<line class="nd-strike" x1="${px + 10}" y1="42" x2="${px + PW - 30}" y2="28"/>`;
    const list = !e ? (st.mode === "a" ? [k] : [[0, k]]) : st.mode === "a" ? e.q : e.heap;
    for (let r = 0; r < rows; r++) {
      const y = PTOP + 6 + r * ROW, it = list[r];
      const text = it === undefined ? "" : st.mode === "a" ? String(it) : pair(it[0], it[1]);
      const v = it === undefined ? null : st.mode === "a" ? it : it[1];
      const stale = v !== null && st.mode !== "a" && e && e.t[v - 1] < it[0];
      s += `<g class="nd-row${it === undefined ? " is-empty" : ""}${stale ? " is-old" : ""}"><title>${it === undefined ? "empty" : stale ? "a stale entry: the node already has a smaller time" : "waiting"}</title>` +
        `<rect x="${px}" y="${y}" width="${PW - 20}" height="${ROW - 4}" rx="4"/><text x="${px + (PW - 20) / 2}" y="${y + 14}" text-anchor="middle">${text}</text></g>`;
    }
    return s + "</svg>";
  };

  const MODES = { a: "בלי משקלים, BFS (סעיף א)", b: "עם משקלים, Dijkstra (סעיף ב)", c: "חד-כיווני, Dijkstra (סעיף ג)" };
  const STEPS = {
    a: ["בונים את רשימת השכנים", "מתחילים מ-k", "מוציאים מראש התור", "הסוף"],
    b: ["בונים את רשימת השכנים", "מתחילים מ-k", "מוציאים את הקטן מהערימה", "רשומה ישנה", "סוגרים ומשחררים", "הסוף"],
    c: ["בונים את רשימת השכנים", "אותו Dijkstra", "הסוף"],
  };
  const CODE = { a: "delay_bfs", b: "delay_dijkstra", c: "delay_dijkstra" };
  const tList = (t) => `[${t.map(num).join(", ")}]`;

  const netView = () => ({
    mount(box) {
      const mode0 = MODES[box.dataset.mode] ? box.dataset.mode : "a";
      const n0 = Math.min(NMAX, Math.max(NMIN, Number(box.dataset.n) || EXAMPLE.n));
      const e0 = parseEdges(box.dataset.edges, n0) || EXAMPLE.edges.map((e) => e.slice());
      const d0 = { mode: mode0, n: n0, k: Math.min(n0, Math.max(1, Number(box.dataset.k) || 1)), edges: e0 };
      const st = { mode: d0.mode, graph: "example", n: d0.n, k: d0.k, edges: d0.edges.map((e) => e.slice()), s: 0, lastSeed: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המצב <select class="nd-mode" aria-label="איזה סעיף">${Object.entries(MODES).map(([v, w]) => `<option value="${v}">${w}</option>`).join("")}</select></label>` +
        `<label>הגרף <select class="nd-graph" aria-label="איזה גרף">${Object.entries(GRAPHS).map(([v, w]) => `<option value="${v}">${w}</option>`).join("")}</select></label>` +
        `<label><span>n</span> <select class="nd-n" aria-label="מספר הצמתים">${Array.from({ length: NMAX - NMIN + 1 }, (_, i) => `<option value="${NMIN + i}">${NMIN + i}</option>`).join("")}</select></label>` +
        `<label><span>המקור k</span> <input type="number" class="ex-num nd-k" min="1" max="${NMAX}" step="1" dir="ltr" aria-label="הצומת שמשדר"></label>` +
        `<button type="button" class="md-button nd-rand">הגרלה</button><span class="nd-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary nd-sum" aria-live="polite"></p>` +
        `<div class="nd-wrap" data-fig-strip></div>` +
        `<span class="viz-legend"><span><i class="nd-key-src"></i>המקור</span><span><i class="nd-key-open"></i>יש לו זמן, עוד לא יצא</span>` +
        `<span><i class="nd-key-set"></i>יצא ונסגר</span><span><i class="nd-key-cur"></i>הצומת של הצעד</span>` +
        `<span><i class="nd-key-relax"></i>הקשת שנבדקת</span><span><i class="nd-key-tree"></i>הקשת שדרכה הגיע הזמן</span>` +
        `<span class="nd-not-a"><i class="nd-key-old"></i>רשומה ישנה</span><span><i class="nd-key-far"></i>לא מושג</span></span>` +
        `<p class="nd-note"></p><p class="nd-tally"></p>` +
        `<div class="ex-fold"><p class="ex-fold-title">הקשתות והמשקלים</p><div class="nd-etab-wrap"></div></div>`;
      const show = explain(box, "הסבר : השלבים של הפתרון והקוד");
      answer(box, NB); answer(box, null);           // the answer line keeps its place from the first step
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const frames = () => (st.mode === "a" ? ndBfs(st.n, st.edges, st.k) : ndDijkstra(st.n, st.edges, st.k, st.mode === "c"));
      // the table of the links, a weight field per row; rebuilt when the graph changes
      const table = () => {
        const arrow = st.mode === "c" ? "→" : "–";
        $(".nd-etab-wrap").innerHTML = st.edges.length ? `<table class="nd-etab"><thead><tr><th>#</th><th>מ</th><th></th><th>אל</th><th class="nd-wcol">המשקל</th></tr></thead><tbody>` +
          st.edges.map((e, i) => `<tr><td>${i + 1}</td><td>${e[0]}</td><td class="nd-arrow">${arrow}</td><td>${e[1]}</td>` +
            `<td class="nd-wcol"><input type="number" class="ex-num nd-w-in" data-i="${i}" min="0" max="${WMAX}" step="1" dir="ltr" value="${e[2]}" aria-label="המשקל של הקשת ${i + 1}"></td></tr>`).join("") +
          `</tbody></table>` : `<p class="nd-none">אין קשתות.</p>`;
        $(".nd-etab-wrap").querySelectorAll(".nd-w-in").forEach((inp) => inp.addEventListener("change", () => {
          const i = Number(inp.dataset.i), v = Math.round(Number(inp.value));
          if (!(v >= 0 && v <= WMAX)) { inp.value = String(st.edges[i][2]); return; }
          st.edges[i][2] = v; restart();
        }));
      };
      const draw = () => {
        const F = frames(), N = F.length, m = st.mode, n = st.n, k = st.k, directed = m === "c";
        st.s = Math.min(Math.max(st.s, 0), N);
        const e = st.s ? F[st.s - 1] : null, done = st.s === N;
        $(".nd-mode").value = m; $(".nd-graph").value = st.graph; $(".nd-n").value = String(n); $(".nd-k").value = String(k); $(".nd-k").max = String(n);
        box.classList.toggle("nd-is-a", m === "a");
        $(".nd-etab-wrap").querySelectorAll(".nd-arrow").forEach((td) => { td.textContent = directed ? "→" : "–"; });
        $(".ex-pos").textContent = `צעד ${st.s} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        const rows = Math.max(1, ...F.map((x) => (m === "a" ? x.q.length : x.heap.length)));
        $(".nd-wrap").innerHTML = svg(st, e, F.slice(0, st.s), rows);
        const E = st.edges.length, arrow = directed ? "→" : "–";
        let note = "", sum = "", lit = [], lines = { py: [], sv: [] }, vars = "", ans = null, marks = [];
        const pops = F.slice(0, st.s).filter((x) => x.kind === "pop").length, skips = F.slice(0, st.s).filter((x) => x.kind === "skip").length;
        const rel = F.slice(0, st.s).filter((x) => x.kind === "relax").length;
        if (m === "a") {
          sum = e ? `${e.kind === "done" ? "התור ריק." : `הצומת של הצעד${NB}: ${ltr(e.u)} (הזמן ${ltr(e.t[e.u - 1])}).`} התור${NB}: ${ltr(e.q.length ? `[${e.q.join(", ")}]` : "[]")}. הזמנים${NB}: ${ltr(tList(e.t))}.`
            : `${ltr(n)} צמתים, ${ltr(E)} קשתות, כל קשת יחידת זמן אחת. ${ltr(`t[${k}] = 0`)}, והתור מחזיק את ${ltr(k)}. כל צעד הוא הוצאה מהתור או בדיקה של קשת אחת.`;
          if (!e) { lines = { py: [7, 8, 9, 10, 11, 12, 13], sv: [4, 5, 6, 7, 8, 9, 10, 11, 12, 13] }; lit = [1, 2]; vars = [ltr(`k = ${k}`), ltr(`t = ${tList(Array.from({ length: n }, (_, i) => (i + 1 === k ? 0 : null)))}`), ltr(`q = [${k}]`)].join(" · "); }
          else if (e.kind === "pop") {
            const nb = ndAdj(n, st.edges, false, false)[e.u].map((x) => x[0]);
            note = `מוציאים מראש התור את ${ltr(e.u)}, שקיבל את האות בזמן ${ltr(e.d)}. עכשיו בודקים את כל השכנים שלו לפי הסדר ברשימת השכנים${NB}: ` +
              (nb.length ? ltr(nb.join(", ")) : "אין לו שכנים") + ".";
            lit = [3]; lines = { py: [14, 15], sv: [14, 15] };
          } else if (e.kind === "relax") {
            note = e.improved ? `הקשת ${ltr(`${e.u}${arrow}${e.v}`)}${NB}: ל-${ltr(e.v)} עוד אין זמן, ולכן ${ltr(`t[${e.v}] = t[${e.u}] + 1 = ${e.nd}`)}, ו-${ltr(e.v)} נכנס לזנב התור. זו הפעם הראשונה שמגיעים אליו, וכשכל הקשתות שוות היא גם הקצרה ביותר.`
              : `הקשת ${ltr(`${e.u}${arrow}${e.v}`)}${NB}: ל-${ltr(e.v)} כבר יש זמן ${ltr(`${e.t[e.v - 1]} ≤ ${e.nd}`)}, הוא קיבל את האות מוקדם יותר או באותו זמן. אין שינוי, והוא לא נכנס שוב לתור.`;
            lit = [3]; lines = e.improved ? { py: [16, 17, 18, 19], sv: [16, 17, 18, 19] } : { py: [16, 17], sv: [16, 17] };
          } else {
            const far = e.t.map((x, i) => (x === null ? i + 1 : null)).filter((x) => x !== null);
            note = far.length ? `התור ריק ו${far.length === 1 ? "הצומת" : "הצמתים"} ${ltr(far.join(", "))} נשאר${far.length === 1 ? "" : "ו"} בלי זמן${NB}: אין מסלול מ-${ltr(k)} אליו. התשובה ${ltr("−1")}.`
              : `התור ריק, ולכל צומת יש זמן. האחרון שקיבל את האות הוא ${ltr(e.t.map((x, i) => [x, i + 1]).filter(([x]) => x === e.ans).map(([, v]) => v).join(", "))} בזמן ${ltr(e.ans)}, וזו התשובה${NB}: המקסימום של הזמנים.`;
            lit = [4]; lines = far.length ? { py: [20, 21], sv: [23, 24] } : { py: [20, 22], sv: [23, 25, 27] };
          }
          if (e) vars = [ltr(`u = ${e.kind === "done" ? "–" : e.u}`), ltr(`t = ${tList(e.t)}`), ltr(`q = [${e.q.join(", ")}]`)].join(" · ");
          const tally = `הוצאות מהתור עד עכשיו${NB}: ${ltr(pops)} מתוך לכל היותר ${ltr(`V = ${n}`)}. בדיקות של קשתות${NB}: ${ltr(rel)} מתוך ${ltr(`2E = ${2 * E}`)}. לכן ${ltr("O(V + E)")}.`;
          $(".nd-tally").innerHTML = tally;
          if (done && e) { ans = e.ans < 0 ? `${ltr("−1")}${NB}: יש צומת שהאות לא מגיע אליו.` : `כל הצמתים קיבלו את האות בזמן ${ltr(e.ans)}.`; marks = e.ans < 0 ? ".nd-wrap .nd-node.is-far" : ".nd-wrap .nd-time.is-max"; }
        } else {
          sum = e ? `${e.kind === "done" ? "הערימה ריקה." : e.kind === "skip" ? `רשומה ישנה ${ltr(pair(e.d, e.u))}.` : `הצומת של הצעד${NB}: ${ltr(e.u)}, נסגר בזמן ${ltr(e.t[e.u - 1])}.`} הערימה${NB}: ${ltr(e.heap.length ? e.heap.map((x) => pair(x[0], x[1])).join(" ") : "ריקה")}. סגורים${NB}: ${ltr(e.settled.length ? e.settled.join(", ") : "–")}.`
            : `${ltr(n)} צמתים, ${ltr(E)} קשתות${directed ? " חד-כיווניות" : ""} עם משקלים. ${ltr(`t[${k}] = 0`)}, כל השאר ${ltr("∞")}, והערימה מחזיקה ${ltr(pair(0, k))}. כל צעד הוא הוצאה מהערימה או שחרור של קשת אחת.`;
          const initPy = m === "c" ? [8, 9, 10, 11, 13, 14, 15, 16, 17] : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17], initSv = m === "c" ? [7, 8, 9, 10, 11, 13, 14, 15, 16, 17] : [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17];
          const L = (chipsB, chipsC) => (m === "b" ? chipsB : chipsC);
          if (!e) { lines = { py: initPy, sv: initSv }; lit = L([1, 2], [1]); vars = [ltr(`k = ${k}`), ltr(`t = ${tList(Array.from({ length: n }, (_, i) => (i + 1 === k ? 0 : null)).map((x) => (x === null ? "∞" : x)))}`), ltr(`heap = [${pair(0, k)}]`), ltr("settled = 0")].join(" · "); }
          else if (e.kind === "pop") {
            note = `הזוג ${ltr(pair(e.d, e.u))} הוא הקטן בערימה, ו-${ltr(`${e.d} = t[${e.u}]`)}${NB}: הצומת ${ltr(e.u)} נסגר בזמן ${ltr(e.d)}, וזה הזמן הסופי שלו${NB}: כל מסלול אחר אליו עובר דרך צומת פתוח עם זמן ${ltr(`≥ ${e.d}`)}, והמשקלים אינם שליליים. עכשיו משחררים את הקשתות היוצאות ממנו.`;
            lit = L([3, 5], [2]); lines = { py: [18, 19, 20, 22], sv: [18, 19, 20, 21] };
          } else if (e.kind === "skip") {
            note = `הזוג ${ltr(pair(e.d, e.u))} יוצא, אבל ${ltr(e.u)} כבר נסגר בזמן ${ltr(`${e.t[e.u - 1]} < ${e.d}`)}${NB}: זו רשומה ישנה שנשארה בערימה כשהזמן של ${ltr(e.u)} השתפר. מדלגים עליה בבדיקה אחת, בלי לשחרר שוב את הקשתות.`;
            lit = L([3, 4], [2]); lines = { py: [19, 20, 21], sv: [19, 20] };
          } else if (e.kind === "relax") {
            const d = e.t[e.u - 1], old = e.old === null ? "∞" : String(e.old);
            note = e.improved ? `הקשת ${ltr(`${e.u}${arrow}${e.v}`)} במשקל ${ltr(e.w)}${NB}: ${ltr(`${d} + ${e.w} = ${e.nd} < ${old}`)}, ולכן ${ltr(`t[${e.v}] = ${e.nd}`)} ו-${ltr(pair(e.nd, e.v))} נדחף לערימה.` +
              (e.old !== null ? ` הרשומה הישנה ${ltr(pair(e.old, e.v))} נשארת בערימה, ותידחה כשתצא.` : "")
              : `הקשת ${ltr(`${e.u}${arrow}${e.v}`)} במשקל ${ltr(e.w)}${NB}: ${ltr(`${d} + ${e.w} = ${e.nd} ≥ ${old}`)}, לא משתפר. ${e.settled.includes(e.v) ? `הצומת ${ltr(e.v)} כבר סגור.` : "הזמן הידוע נשאר."}`;
            lit = L([5], [2]); lines = e.improved ? { py: [23, 24, 25, 26], sv: [22, 23, 24, 25, 26, 27, 28] } : { py: [23, 24], sv: [22, 23, 24] };
          } else {
            const far = e.t.map((x, i) => (x === null ? i + 1 : null)).filter((x) => x !== null);
            note = far.length ? `הערימה ריקה ונסגרו ${ltr(e.settled.length)} צמתים מתוך ${ltr(n)}${NB}: ${far.length === 1 ? "הצומת" : "הצמתים"} ${ltr(far.join(", "))} לא ${far.length === 1 ? "מושג" : "מושגים"} מ-${ltr(k)}${directed ? " (אף קשת לא נכנסת אליו ממקום שהאות הגיע אליו)" : ""}. התשובה ${ltr("−1")}.`
              : `הערימה ריקה וכל ${ltr(n)} הצמתים סגורים. הזמן הגדול ביותר הוא ${ltr(e.ans)}, של ${ltr(e.t.map((x, i) => [x, i + 1]).filter(([x]) => x === e.ans).map(([, v]) => v).join(", "))}${NB}: התשובה.`;
            lit = L([6], [3]); lines = far.length ? { py: [27, 28], sv: [32] } : { py: [27, 29], sv: [32, 33, 34] };
          }
          if (e) vars = [ltr(e.kind === "done" ? "heap = []" : `(d, u) = ${pair(e.kind === "relax" ? e.t[e.u - 1] : e.d, e.u)}`), ltr(`t = ${tList(e.t.map((x) => (x === null ? "∞" : x)))}`),
            ltr(`heap = [${e.heap.map((x) => pair(x[0], x[1])).join(", ")}]`), ltr(`settled = ${e.settled.length}`)].join(" · ");
          const Eeff = directed ? E : 2 * E;
          $(".nd-tally").innerHTML = `רשומות שיצאו מהערימה${NB}: ${ltr(pops + skips)} (מהן ${ltr(skips)} ישנות). שחרורים${NB}: ${ltr(rel)} מתוך ${ltr(Eeff)}. צמתים סגורים${NB}: ${ltr(pops)} מתוך ${ltr(n)}.`;
          if (done && e) { ans = e.ans < 0 ? `${ltr("−1")}${NB}: נסגרו ${ltr(e.settled.length)} צמתים מתוך ${ltr(n)}.` : `כל הצמתים קיבלו את האות בזמן ${ltr(e.ans)}.`; marks = e.ans < 0 ? ".nd-wrap .nd-node.is-far" : ".nd-wrap .nd-time.is-max"; }
        }
        $(".nd-sum").innerHTML = sum;
        $(".nd-note").innerHTML = note;
        show({ code: CODE[m], steps: STEPS[m], lit, lines, vars });
        answer(box, ans, marks);
      };
      const total = () => frames().length;
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= total(), restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; draw(); };
      const fitK = () => { st.k = Math.max(1, Math.min(st.k, st.n)); };
      const setGraph = (g) => {
        st.graph = g;
        if (g === "example") { st.n = EXAMPLE.n; st.edges = EXAMPLE.edges.map((e) => e.slice()); }
        else if (READY[g]) st.edges = READY[g](st.n);
        fitK(); table(); restart();
      };
      $(".nd-mode").addEventListener("change", () => { st.mode = MODES[$(".nd-mode").value] ? $(".nd-mode").value : "a"; restart(); });
      $(".nd-graph").addEventListener("change", () => {
        const g = GRAPHS[$(".nd-graph").value] ? $(".nd-graph").value : "example";
        if (g === "random") { if (st.lastSeed) seed.replay(st.lastSeed); else seed.draw(); return; }
        setGraph(g);
      });
      $(".nd-n").addEventListener("change", () => {
        st.n = Math.min(NMAX, Math.max(NMIN, Math.round(Number($(".nd-n").value)) || EXAMPLE.n));
        if (st.graph === "example") st.graph = "line";                 // the example has six nodes
        if (st.graph === "random" && st.lastSeed) { seed.replay(st.lastSeed); return; }
        setGraph(st.graph);
      });
      $(".nd-k").addEventListener("change", () => {
        const v = Math.round(Number($(".nd-k").value));
        if (!Number.isFinite(v)) { $(".nd-k").value = String(st.k); return; }
        st.k = Math.max(1, Math.min(v, st.n)); restart();
      });
      const seedBox = seedControls(box, $(".nd-anchor"), (rng, sd) => {
        st.graph = "random"; st.lastSeed = sd; st.edges = ndRandomGraph(rng, st.n);
        fitK(); table(); restart();
      }, { fresh: false });
      const seed = { draw: () => seedBox.draw(), replay: (sd) => box.dvqSeed.runSeed(sd) };
      $(".nd-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, { mode: d0.mode, graph: "example", n: d0.n, k: d0.k, edges: d0.edges.map((e) => e.slice()) }); table(); restart(); });
      table();
      draw();
    },
  });

  dvqExplorers.register({
    views: { netdelay: netView },
    help: {
      netdelay: "בוחרים סעיף וגרף (הדוגמה של העמוד, קו, טבעת, עץ, צפוף, או הגרלה מערך אתחול), את מספר הצמתים ואת המקור k, ובטבלה שמתחת לאיור את המשקל של כל קשת. הגרף מצויר על מעגל והתור (סעיף א) או הערימה (סעיפים ב ו-ג, ממוינת) לידו. כל צעד הוא הוצאה אחת מהתור או מהערימה, או בדיקה של קשת אחת : הצומת של הצעד מוקף, הקשת שנבדקת מודגשת, צומת שנסגר נצבע והזמן שלו נכתב בתווית שלידו, ורשומה ישנה בערימה נמחקת כשהיא יוצאת. בסוף התשובה : הזמן הגדול ביותר, או −1 עם הצמתים שלא מושגים. השורה שמתחת מסבירה כל צעד, והפאנל 'הסבר' מדליק את שורות הקוד.",
    },
    models: { ndBfs, ndDijkstra, ndRandomGraph, ndReady: (g, n) => (g === "example" ? EXAMPLE.edges : READY[g](n)) },
  });
})();
