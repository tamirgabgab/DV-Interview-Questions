// kinds: toposort
//   toposort               0102        tasks A.. on a circle with "b after a" arrows (data-n, data-edges "AB AC ...", data-dur "3.2.4..."), edited by clicking a task and then another (the arrow between them added or removed) or in a field of edges ("A>B, B>C"); ready graphs (the page's example, the example with a cycle, a diamond, a chain, no edges, a self loop); Kahn step by step (every pop and every lowered in-degree its own step) with the in-degrees, the queue and the order beside the graph, the cycle in red when the queue empties early; mode sched adds the durations and a Gantt chart: the earliest starts as Kahn pushes them, then the total, the slack and the critical path
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMIN = 2, NMAX = 8, EMAX = 24, DMAX = 99;
  const NAMES = "ABCDEFGH";
  const L = (v) => NAMES[v];

  // --- the model, as tools/figures/q0102.py ----------------------------------------------
  // find_cycle: each task left still waits for a task left; walk back from the smallest
  // one, always to the smallest predecessor left, until a task repeats; the walk between
  // the two visits, read forward, is a cycle, given from its smallest task
  const tsFindCycle = (n, edges, left) => {
    const rest = new Set(left), seen = new Map(), path = [];
    let cur = Math.min(...left);
    while (!seen.has(cur)) {
      seen.set(cur, path.length);
      path.push(cur);
      cur = Math.min(...edges.filter(([a, b]) => b === cur && rest.has(a)).map(([a]) => a));
    }
    const cyc = path.slice(seen.get(cur)).reverse();
    const k = cyc.indexOf(Math.min(...cyc));
    return cyc.slice(k).concat(cyc.slice(0, k));
  };
  // kahn_events: a pop takes the front of the queue, a lower takes one edge out of it (and
  // pushes the successor's earliest start), done names the tasks left and one cycle among
  // them, or the total, the latest finishes and the slack. Every event keeps the in-degrees,
  // the queue, the order and the earliest starts after it.
  const tsKahn = (n, edges, dur) => {
    dur = dur || Array(n).fill(1);
    const succ = Array.from({ length: n }, () => []), indeg = Array(n).fill(0);
    edges.forEach(([a, b], i) => { succ[a].push([b, i]); indeg[b]++; });
    const q = [], order = [], start = Array(n).fill(0), ev = [];
    for (let v = 0; v < n; v++) if (indeg[v] === 0) q.push(v);
    const rec = (e) => ev.push({ ...e, indeg: indeg.slice(), q: q.slice(), order: order.slice(), start: start.slice() });
    while (q.length) {
      const u = q.shift();
      order.push(u);
      rec({ kind: "pop", u });
      for (const [v, i] of succ[u]) {
        indeg[v]--;
        start[v] = Math.max(start[v], start[u] + dur[u]);
        const zero = indeg[v] === 0;
        if (zero) q.push(v);
        rec({ kind: "lower", u, v, i, zero });
      }
    }
    const left = [];
    for (let v = 0; v < n; v++) if (!order.includes(v)) left.push(v);
    const done = { kind: "done", left, cycle: left.length ? tsFindCycle(n, edges, left) : null, total: null, slack: null, late: null };
    if (!left.length) {
      let total = 0;
      for (let v = 0; v < n; v++) total = Math.max(total, start[v] + dur[v]);
      const late = Array(n).fill(total);
      for (const u of order.slice().reverse()) for (const [v] of succ[u]) late[u] = Math.min(late[u], late[v] - dur[v]);
      Object.assign(done, { total, late, slack: late.map((x, v) => x - dur[v] - start[v]) });
    }
    rec(done);
    return ev;
  };
  // one critical path: from a task that ends at the total, back through a predecessor with
  // no slack that ends exactly when it starts (the smallest such, at every step)
  const tsCritPath = (n, edges, dur, end) => {
    const { start, slack, total } = end;
    let v = -1;
    for (let t = 0; t < n && v < 0; t++) if (slack[t] === 0 && start[t] + dur[t] === total && !edges.some(([a, b]) => a === t && slack[b] === 0 && start[b] === start[t] + dur[t])) v = t;
    if (v < 0) return [];
    const path = [v];
    for (;;) {
      const cur = path[0];
      const ps = edges.filter(([a, b]) => b === cur && slack[a] === 0 && start[a] + dur[a] === start[cur]).map(([a]) => a);
      if (!ps.length) break;
      path.unshift(Math.min(...ps));
    }
    return path;
  };
  // "A>B, B>C>D": the edges, or the token that is not an edge of the first n letters
  const tsParse = (text, n) => {
    const out = [], toks = String(text || "").trim().split(/[\s,;]+/).filter(Boolean);
    for (const tok of toks) {
      const parts = tok.toUpperCase().split(/-?>/);
      if (parts.length < 2 || parts.some((p) => p.length !== 1 || NAMES.indexOf(p) < 0 || NAMES.indexOf(p) >= n)) return { err: tok };
      for (let k = 0; k + 1 < parts.length; k++) out.push([NAMES.indexOf(parts[k]), NAMES.indexOf(parts[k + 1])]);
    }
    return out.length > EMAX ? { err: null, many: true } : { edges: out };
  };
  const tsFormat = (edges) => edges.map(([a, b]) => `${L(a)}>${L(b)}`).join(", ");
  const tsParseDur = (text, n) => {
    const p = String(text || "").trim().split(/[\s,;]+/).filter(Boolean);
    if (p.length !== n || p.some((x) => !/^\d+$/.test(x) || Number(x) > DMAX)) return null;
    return p.map(Number);
  };
  const EX = [[0, 1], [0, 2], [4, 2], [1, 3], [2, 3], [3, 5], [5, 6]];
  const PRESETS = {
    example: { n: 7, edges: EX, dur: [3, 2, 4, 1, 5, 1, 4], name: "הדוגמה של העמוד" },
    cycle: { n: 7, edges: EX.concat([[3, 4]]), dur: [3, 2, 4, 1, 5, 1, 4], name: "הדוגמה עם מעגל" },
    diamond: { n: 4, edges: [[0, 1], [0, 2], [1, 3], [2, 3]], dur: [2, 3, 1, 2], name: "יהלום" },
    chain: { n: 5, edges: [[0, 1], [1, 2], [2, 3], [3, 4]], dur: [2, 1, 3, 1, 2], name: "שרשרת" },
    free: { n: 5, edges: [], dur: [3, 1, 4, 1, 5], name: "בלי תלויות" },
    loop: { n: 3, edges: [[0, 1], [1, 1], [1, 2]], dur: [2, 2, 2], name: "לולאה עצמית" },
    custom: { name: "משלכם" },
  };
  const tsPreset = (n, edges) => Object.keys(PRESETS).find((k) => PRESETS[k].n === n && tsFormat(PRESETS[k].edges) === tsFormat(edges)) || "custom";

  // --- drawing -------------------------------------------------------------------------
  // The layout: a column per rank, the rank of a task the longest chain of arrows into it
  // once the arrows that close a cycle are set aside (the back edges of a depth-first
  // search from A, B, ...; a self loop is one), so the example reads as its Kahn rounds and
  // the arrows of a cycle are the ones that run backwards. In a column the tasks are put
  // in the order of their predecessors' rows. The layout depends on the graph only, never
  // on the step.
  const tsLayout = (n, edges) => {
    const succ = Array.from({ length: n }, () => []);
    edges.forEach(([a, b], i) => succ[a].push([b, i]));
    const color = Array(n).fill(0), back = new Set();
    const visit = (u) => {
      color[u] = 1;
      for (const [v, i] of succ[u]) { if (color[v] === 1) back.add(i); else if (color[v] === 0) visit(v); }
      color[u] = 2;
    };
    for (let s = 0; s < n; s++) if (color[s] === 0) visit(s);
    const rank = Array(n).fill(0);
    for (let r = 0; r < n; r++) edges.forEach(([a, b], i) => { if (!back.has(i) && rank[a] + 1 > rank[b]) rank[b] = rank[a] + 1; });
    const cols = Array.from({ length: Math.max(...rank, 0) + 1 }, () => []);
    const row = Array(n).fill(0);
    for (let v = 0; v < n; v++) cols[rank[v]].push(v);
    cols.forEach((col) => {
      const key = (v) => {
        const ps = edges.filter(([a, b], i) => b === v && !back.has(i) && rank[a] < rank[v]).map(([a]) => row[a] / Math.max(1, cols[rank[a]].length - 1));
        return ps.length ? ps.reduce((x, y) => x + y, 0) / ps.length : -1;
      };
      col.sort((x, y) => key(x) - key(y) || x - y).forEach((v, i) => { row[v] = i; });
    });
    return { rank, row, cols, back: [...back].sort((x, y) => x - y) };
  };
  const W = 400, NR = 16, TOP = 31, SLOT = 34, SPACE = 40, ROWH = 30;
  const f1 = (x) => x.toFixed(1);
  const geometry = (n, edges) => {
    const lay = tsLayout(n, edges), C = lay.cols.length, kmax = Math.max(...lay.cols.map((c) => c.length));
    // a column of more than four tasks zigzags, two places apart, so it stays short
    const gap = kmax > 4 ? Math.min(40, 130 / (kmax - 1)) : kmax > 1 ? Math.min(56, 150 / (kmax - 1)) : 0;
    const P = Array.from({ length: n }, (_, v) => {
      const k = lay.cols[lay.rank[v]].length, zig = k > 4 ? (lay.row[v] % 2 ? 20 : -20) : 0;
      const x = (C === 1 ? W / 2 : 56 + lay.rank[v] * ((W - 112) / (C - 1))) + zig;
      return [x, TOP + (kmax - 1) * gap / 2 + (lay.row[v] - (k - 1) / 2) * gap, zig];
    });
    const backs = new Set(lay.back), loops = edges.some(([a, b]) => a === b);
    const bottom = TOP + (kmax - 1) * gap + NR + (edges.some(([a, b], i) => backs.has(i) && a !== b) ? 46 : loops ? 36 : 14);
    return { P, backs, bottom, H: bottom + 2 * ROWH + 10 };
  };
  const head = (tx, ty, ux, uy) => {
    const bx = tx - ux * 7, by = ty - uy * 7;
    return [`<path class="ts-head" d="M${f1(tx)},${f1(ty)} L${f1(bx - uy * 4.5)},${f1(by + ux * 4.5)} L${f1(bx + uy * 4.5)},${f1(by - ux * 4.5)} Z"/>`, bx, by];
  };
  // an arrow from p to q: straight, bent through a control point, or a loop under p
  const arrowPath = (p, q, ctrl) => {
    const [x1, y1] = p, [x2, y2] = q;
    if (p === q) {
      const a1 = 2.1, a2 = 1.05, ax = Math.cos(a1), ay = Math.sin(a1), bx0 = Math.cos(a2), by0 = Math.sin(a2);
      const tx = x1 + bx0 * NR, ty = y1 + by0 * NR, [hd, bx, by] = head(tx, ty, -bx0, -by0);
      return `<path d="M${f1(x1 + ax * NR)},${f1(y1 + ay * NR)} C${f1(x1 + ax * 44)},${f1(y1 + ay * 44)} ${f1(x1 + bx0 * 44)},${f1(y1 + by0 * 44)} ${f1(bx)},${f1(by)}" fill="none"/>` + hd;
    }
    if (!ctrl) {
      const d = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / d, uy = (y2 - y1) / d;
      const [hd, bx, by] = head(x2 - ux * NR, y2 - uy * NR, ux, uy);
      return `<line x1="${f1(x1 + ux * NR)}" y1="${f1(y1 + uy * NR)}" x2="${f1(bx)}" y2="${f1(by)}"/>` + hd;
    }
    const [cx, cy] = ctrl, s1 = Math.hypot(cx - x1, cy - y1), s2 = Math.hypot(x2 - cx, y2 - cy);
    const ex = (x2 - cx) / s2, ey = (y2 - cy) / s2;
    const [hd, bx, by] = head(x2 - ex * NR, y2 - ey * NR, ex, ey);
    return `<path d="M${f1(x1 + (cx - x1) / s1 * NR)},${f1(y1 + (cy - y1) / s1 * NR)} Q${f1(cx)},${f1(cy)} ${f1(bx)},${f1(by)}" fill="none"/>` + hd;
  };
  const control = (g, a, b, i, both) => {
    const [x1, y1] = g.P[a], [x2, y2] = g.P[b];
    if (a === b) return null;
    if (g.backs.has(i)) return [(x1 + x2) / 2, Math.max(y1, y2) + 44 + 0.08 * Math.abs(x2 - x1)];   // under the graph
    const span = Math.abs(x2 - x1), d = Math.hypot(x2 - x1, y2 - y1);
    const far = span > (W - 112) / 1.5 || [...g.P.keys()].some((v) => v !== a && v !== b && (() => {   // a task in the way
      const [x, y] = g.P[v], t = ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / (d * d);
      return t > 0.05 && t < 0.95 && Math.hypot(x1 + t * (x2 - x1) - x, y1 + t * (y2 - y1) - y) < NR + 4;
    })());
    if (!far && !both) return null;
    const off = far ? 30 : 16;
    return [(x1 + x2) / 2 + ((y2 - y1) / d) * off, (y1 + y2) / 2 - ((x2 - x1) / d) * off];
  };

  const graphSvg = (st, e, F) => {
    const { n, edges, mode } = st, sched = mode === "sched", done = e && e.kind === "done";
    const g = geometry(n, edges), P = g.P;
    const indeg = e ? e.indeg : Array.from({ length: n }, (_, v) => edges.filter(([, b]) => b === v).length);
    const q = e ? e.q : indeg.map((d, v) => (d === 0 ? v : -1)).filter((v) => v >= 0);
    const order = e ? e.order : [];
    const start = e ? e.start : Array(n).fill(0);
    const lowered = new Set(F.filter((x) => x.kind === "lower").map((x) => x.i));
    const cyc = done && e.cycle ? e.cycle : [];
    const onCyc = new Set(cyc.map((v, k) => `${v}>${cyc[(k + 1) % cyc.length]}`));
    const crit = done && !e.cycle && sched ? e.slack : null;
    const cur = e && e.kind !== "done" ? e.u : null;
    let s = `<svg class="figure ts-fig ts-live" viewBox="0 0 ${W} ${f1(g.H)}" style="max-width:${Math.round(W * 1.15)}px" role="group" ` +
      `aria-label="${n} משימות, חץ מכל משימה למשימה שרצה אחריה, ומתחתן התור והסדר${NB}: לחיצה על משימה ואחר כך על אחרת מוסיפה או מוחקת את החץ ביניהן">`;
    // the arrows, one per pair (a pair given twice is labelled ×2)
    const seen = new Map();
    edges.forEach(([a, b], i) => { const k = `${a}>${b}`; if (!seen.has(k)) seen.set(k, []); seen.get(k).push(i); });
    for (const [k, idx] of seen) {
      const [a, b] = k.split(">").map(Number);
      const now = e && e.kind === "lower" && idx.includes(e.i);
      const isCrit = crit && crit[a] === 0 && crit[b] === 0 && start[a] + st.dur[a] === start[b];
      const cls = now ? " is-now" : onCyc.has(k) ? " is-cycle" : isCrit ? " is-crit" : idx.every((i) => lowered.has(i)) ? " is-done" : "";
      const ctrl = control(g, a, b, idx[0], seen.has(`${b}>${a}`));
      s += `<g class="ts-edge${cls}"><title>${L(a)} → ${L(b)}: ${L(b)} after ${L(a)}${idx.length > 1 ? `, ${idx.length} times` : ""}</title>${arrowPath(P[a], a === b ? P[a] : P[b], ctrl)}`;
      if (idx.length > 1 && a !== b) {
        const [x1, y1] = P[a], [x2, y2] = P[b], [mx, my] = ctrl ? [(x1 + 2 * ctrl[0] + x2) / 4, (y1 + 2 * ctrl[1] + y2) / 4] : [(x1 + x2) / 2, (y1 + y2) / 2];
        s += `<text class="ts-mult" x="${f1(mx)}" y="${f1(my - 5)}" text-anchor="middle">×${idx.length}</text>`;
      }
      s += "</g>";
    }
    for (let v = 0; v < n; v++) {
      const [x, y] = P[v], out = order.includes(v);
      const state = done && e.cycle ? (cyc.includes(v) ? " is-cycle" : out ? " is-out" : " is-stuck")
        : crit && crit[v] === 0 ? " is-crit" : out ? " is-out" : q.includes(v) ? " is-ready" : "";
      const what = state === " is-cycle" ? "on the cycle" : state === " is-stuck" ? "stuck behind the cycle" : out ? "out of the queue" : q.includes(v) ? "in the queue" : `waits for ${indeg[v]}`;
      const label = st.sel === v ? `המשימה ${L(v)} נבחרה${NB}: לחצו על משימה אחרת כדי להוסיף או למחוק את החץ מ-${L(v)} אליה, או שוב עליה כדי לבטל`
        : `המשימה ${L(v)}, דרגת כניסה ${indeg[v]}${NB}: בחירה כדי להוסיף או למחוק חץ`;
      s += `<g class="ts-node${state}${v === cur ? " is-now" : ""}${st.sel === v ? " is-sel" : ""}" data-v="${v}" tabindex="0" role="button" aria-label="${label}"><title>task ${L(v)}: ${what}</title>` +
        `<circle cx="${f1(x)}" cy="${f1(y)}" r="${NR}"/><text x="${f1(x)}" y="${f1(y + 5)}" text-anchor="middle">${L(v)}</text></g>`;
      let txt, bc;
      if (!sched) { txt = String(indeg[v]); bc = indeg[v] === 0 ? " is-zero" : ""; }
      else { txt = String(start[v]); bc = crit && crit[v] === 0 ? " is-crit" : out ? " is-sched" : " is-tent"; }
      const bw = 12 + 7 * txt.length, left = P[v][2] < 0, bx = left ? x - 13 - bw / 2 + 6 : x + 13 + bw / 2 - 6, by = y - 21;
      s += `<g class="ts-badge${bc}"><title>${sched ? `earliest start of ${L(v)}${out ? "" : " so far"}: ${txt}` : `in-degree of ${L(v)}: ${txt}`}</title>` +
        `<rect x="${f1(bx - bw / 2)}" y="${f1(by - 9)}" width="${bw}" height="17" rx="5"/><text x="${f1(bx)}" y="${f1(by + 4)}" text-anchor="middle">${txt}</text></g>`;
    }
    // the queue and the order, a row of slots each, read from the left
    [["התור", q, "is-q"], ["הסדר", order, "is-o"]].forEach(([title, list, cls], c) => {
      const y = g.bottom + c * ROWH;
      s += `<text class="ts-lab" x="${W - 26}" y="${f1(y + 17)}" text-anchor="middle" direction="rtl">${title}</text>`;
      for (let r = 0; r < n; r++) {
        const it = list[r], x = 8 + r * SPACE;
        const isNew = it !== undefined && e && ((c === 0 && e.kind === "lower" && e.zero && it === e.v) || (c === 1 && e.kind === "pop" && it === e.u));
        const k = it === undefined ? " is-empty" : ` ${cls}${isNew ? " is-new" : ""}${c === 1 && crit && crit[it] === 0 ? " is-crit" : ""}`;
        s += `<g class="ts-qrow${k}"><rect x="${x}" y="${f1(y)}" width="${SLOT}" height="${ROWH - 6}" rx="4"/>` +
          `<text x="${x + SLOT / 2}" y="${f1(y + 17)}" text-anchor="middle">${it === undefined ? "" : L(it)}</text></g>`;
      }
    });
    return s + "</svg>";
  };

  // the schedule: a bar per task from its earliest start, drawn when it leaves the queue
  // (its start is then final); a mark at the start known so far for the others; at the end
  // the slack, the critical bars and the total. One scale for every step of a graph.
  const ganttSvg = (st, e, end) => {
    const { n, dur } = st, done = e && e.kind === "done";
    const T = end.cycle ? Math.max(1, dur.reduce((x, y) => x + y, 0)) : Math.max(1, end.total);
    const x0 = 30, x1 = W - 14, top = 6, RH = 19, base = top + n * RH + 3, Hh = base + 22;
    const X = (t) => x0 + (t / T) * (x1 - x0);
    const stepT = [1, 2, 5, 10, 20, 50, 100].find((k) => T / k <= 12) || 200;
    const start = e ? e.start : Array(n).fill(0), order = e ? e.order : [];
    let s = `<svg class="perf-chart ts-gantt" viewBox="0 0 ${W} ${Hh}" style="max-width:${Math.round(W * 1.15)}px" role="img" ` +
      `aria-label="לוח הזמנים${NB}: פס לכל משימה מההתחלה המוקדמת שלה, כשהיא יוצאת מהתור${done && !end.cycle ? `. הכול נגמר בזמן ${end.total}` : ""}">`;
    for (let t = 0; t <= T; t += stepT) s += `<line class="grid" x1="${f1(X(t))}" x2="${f1(X(t))}" y1="${top}" y2="${base}"/><text class="tick" x="${f1(X(t))}" y="${base + 16}" text-anchor="middle">${t}</text>`;
    for (let v = 0; v < n; v++) {
      const y = top + v * RH;
      s += `<text class="ts-glab" x="${x0 - 8}" y="${y + 13}" text-anchor="end">${L(v)}</text>`;
      if (order.includes(v)) {
        const crit = done && !end.cycle && end.slack[v] === 0;
        if (done && !end.cycle && end.slack[v] > 0) {
          s += `<rect class="ts-slack" x="${f1(X(start[v] + dur[v]))}" y="${y + 4}" width="${f1(X(end.late[v]) - X(start[v] + dur[v]))}" height="10" rx="3"><title>${L(v)}: slack ${end.slack[v]}</title></rect>`;
        }
        const w = Math.max(2, X(start[v] + dur[v]) - X(start[v]));
        s += `<g class="ts-bar${crit ? " is-crit" : ""}"><title>${L(v)}: ${dur[v]} minutes, from ${start[v]} to ${start[v] + dur[v]}</title>` +
          `<rect x="${f1(X(start[v]))}" y="${y + 1}" width="${f1(w)}" height="16" rx="3"/>` +
          (w >= 14 ? `<text x="${f1(X(start[v]) + w / 2)}" y="${y + 13}" text-anchor="middle">${dur[v]}</text>` : "") + "</g>";
      } else if (!(done && end.cycle)) {
        s += `<line class="ts-tent" x1="${f1(X(start[v]))}" x2="${f1(X(start[v]))}" y1="${y + 1}" y2="${y + 17}"><title>${L(v)}: starts at ${start[v]} or later</title></line>`;
      }
    }
    if (done && !end.cycle) s += `<line class="ts-total" x1="${f1(X(end.total))}" x2="${f1(X(end.total))}" y1="2" y2="${base}"/>`;
    if (done && end.cycle) s += `<text class="ts-gnone" x="${f1((x0 + x1) / 2)}" y="${f1(base - 10)}" text-anchor="middle" direction="rtl">אין לוח זמנים${NB}: יש מעגל</text>`;
    return s + `<line class="axis" x1="${x0}" x2="${x1}" y1="${base}" y2="${base}"/></svg>`;
  };

  const MODES = { kahn: "סדר, Kahn (סעיף א)", sched: "לוח זמנים (סעיף ג)" };
  const names = (vs) => vs.map(L).join(", ");
  const chain = (vs) => vs.map(L).join(" → ");

  const topoView = () => ({
    mount(box) {
      const mode0 = MODES[box.dataset.mode] ? box.dataset.mode : "kahn";
      const n0 = Math.min(NMAX, Math.max(NMIN, Number(box.dataset.n) || 7));
      const p0 = tsParse(String(box.dataset.edges || "").split(/\s+/).filter(Boolean).map((t) => t.split("").join(">")).join(", "), n0);
      const e0 = p0.edges || EX.map((x) => x.slice());
      const d0 = String(box.dataset.dur || "").split(".").map(Number);
      const dur0 = d0.length === n0 && d0.every((x) => Number.isInteger(x) && x >= 0 && x <= DMAX) ? d0 : Array(n0).fill(1);
      const init = { mode: mode0, n: n0, edges: e0, dur: dur0 };
      const st = { ...init, edges: e0.map((x) => x.slice()), dur: dur0.slice(), s: 0, sel: null, msg: "", err: "" };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המצב <select class="ts-mode" aria-label="איזה סעיף">${Object.entries(MODES).map(([v, w]) => `<option value="${v}">${w}</option>`).join("")}</select></label>` +
        `<label>הגרף <select class="ts-preset" aria-label="איזה גרף">${Object.entries(PRESETS).map(([v, p]) => `<option value="${v}">${p.name}</option>`).join("")}</select></label>` +
        `<label>משימות <select class="ts-n" aria-label="מספר המשימות">${Array.from({ length: NMAX - NMIN + 1 }, (_, i) => `<option value="${NMIN + i}">${NMIN + i}</option>`).join("")}</select></label>` +
        `<label>החצים <input type="text" class="ts-edges" dir="ltr" spellcheck="false" autocomplete="off" aria-label="החצים, למשל A>B, B>C : ‏B אחרי A"></label>` +
        `<label class="ts-sched-only">המשכים <input type="text" class="ts-dur" dir="ltr" spellcheck="false" autocomplete="off" aria-label="המשך של כל משימה בדקות, לפי הסדר A, B, C"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary ts-sum" aria-live="polite"></p>` +
        `<div class="ts-wrap ts-graph" data-edits></div>` +
        `<div class="ts-wrap ts-sched-only ts-gwrap"></div>` +
        `<p class="ts-note"></p>` +
        `<span class="viz-legend"><span class="ts-kahn-only"><i class="ts-key-badge"></i>דרגת הכניסה</span>` +
        `<span><i class="ts-key-ready"></i>בתור, מוכנה לרוץ</span><span><i class="ts-key-out"></i>יצאה מהתור</span>` +
        `<span><i class="ts-key-now"></i>המשימה של הצעד</span><span><i class="ts-key-lower"></i>החץ שמוריד דרגה</span>` +
        `<span class="ts-kahn-only"><i class="ts-key-cycle"></i>המעגל</span><span class="ts-kahn-only"><i class="ts-key-stuck"></i>תקועה</span>` +
        `<span class="ts-sched-only"><i class="ts-key-tent"></i>ההתחלה הידועה עד עכשיו</span><span class="ts-sched-only"><i class="ts-key-crit"></i>הנתיב הקריטי</span>` +
        `<span class="ts-sched-only"><i class="ts-key-slack"></i>המרווח</span><span><i class="ts-key-sel"></i>נבחרה לעריכה</span></span>` +
        `<p class="ts-succ"></p>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), wrap = $(".ts-graph");
      const frames = () => tsKahn(st.n, st.edges, st.dur);
      const syncFields = () => {
        $(".ts-mode").value = st.mode; $(".ts-n").value = String(st.n);
        $(".ts-preset").value = tsPreset(st.n, st.edges);
        $(".ts-edges").value = tsFormat(st.edges); $(".ts-dur").value = st.dur.join(", ");
      };
      const draw = () => {
        const F = frames(), T = F.length, m = st.mode, n = st.n, sched = m === "sched";
        st.s = Math.min(Math.max(st.s, 0), T);
        const e = st.s ? F[st.s - 1] : null, end = F[T - 1], done = st.s === T;
        box.classList.toggle("ts-is-sched", sched);
        $(".ex-pos").textContent = `צעד ${st.s} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        const had = wrap.contains(document.activeElement) ? Number(document.activeElement.dataset && document.activeElement.dataset.v) : null;
        wrap.innerHTML = graphSvg(st, e, F.slice(0, st.s));
        if (had !== null && Number.isInteger(had)) { const g = wrap.querySelector(`[data-v="${had}"]`); if (g) g.focus(); }
        $(".ts-gwrap").innerHTML = sched ? ganttSvg(st, e, end) : "";
        const succ = Array.from({ length: n }, () => []);
        st.edges.forEach(([a, b]) => succ[a].push(b));
        $(".ts-succ").innerHTML = `העוקבות, לפי הסדר של החצים${NB}: ` +
          (st.edges.length ? succ.map((l, v) => (l.length ? ltr(`${L(v)} → ${names(l)}`) : "")).filter(Boolean).join(" · ") : "אין חצים, כל המשימות בלתי תלויות.");
        const indeg0 = Array.from({ length: n }, (_, v) => st.edges.filter(([, b]) => b === v).length);
        let sum, note = "", ans = null, marks = [];
        const qOf = (x) => ltr(`[${names(x)}]`);
        if (!e) {
          const q0 = indeg0.map((d, v) => (d === 0 ? v : -1)).filter((v) => v >= 0);
          sum = `בגרף ${n} משימות ו-${st.edges.length} חצים. הדרגות${NB}: ${ltr(indeg0.map((d, v) => `${L(v)}${d}`).join(" "))}. התור מתחיל עם ${q0.length ? ltr(names(q0)) : "אף משימה"}.`;
          note = st.err ? `<span class="ts-err">${st.err}</span>` : st.msg ||
            (q0.length ? `כל משימה שדרגת הכניסה שלה 0 נכנסת לתור לפי הסדר. כל צעד הוא הוצאה מהתור, או הורדה של דרגה אחת בחץ אחד.`
              : `אין אף משימה עם דרגת כניסה 0${NB}: כל משימה מחכה לאחרת, והתור ריק כבר בהתחלה.`);
        } else {
          sum = e.kind === "done" ? (e.cycle ? `התור ריק, ו-${e.left.length} משימות לא יצאו.` : `התור ריק, וכל ${n} המשימות יצאו.`)
            : e.kind === "pop" ? `יוצאת מהתור${NB}: ${ltr(L(e.u))}.` : `החץ ${ltr(`${L(e.u)} → ${L(e.v)}`)}${NB}: הדרגה של ${ltr(L(e.v))} יורדת ל-${e.indeg[e.v]}.`;
          sum += ` התור${NB}: ${qOf(e.q)}. הסדר${NB}: ${qOf(e.order)}.`;
          if (e.kind === "pop") {
            const nx = succ[e.u];
            note = `המשימה ${ltr(L(e.u))} יוצאת מראש התור ונכנסת לסוף הסדר${sched ? `, ומתחילה בזמן ${e.start[e.u]}, הסיום של האחרונה מבין אלה שהיא חיכתה להן` : ""}. ` +
              (nx.length ? `עכשיו מורידים את הדרגה של כל עוקבת שלה${NB}: ${ltr(names(nx))}.` : "אין לה עוקבות.");
          } else if (e.kind === "lower") {
            const d = e.indeg[e.v];
            note = `החץ ${ltr(`${L(e.u)} → ${L(e.v)}`)}${NB}: ${ltr(L(e.u))} יצאה, ולכן ${ltr(L(e.v))} מחכה למשימה אחת פחות, ${ltr(`${d + 1} → ${d}`)}. ` +
              (e.zero ? `הדרגה הגיעה ל-0, ו-${ltr(L(e.v))} נכנסת לזנב התור.` : `היא עוד מחכה ל-${d === 1 ? "משימה אחת" : `${d} משימות`}.`) +
              (sched ? ` ההתחלה המוקדמת של ${ltr(L(e.v))} עד עכשיו${NB}: ${ltr(`max(…, ${e.start[e.u]} + ${st.dur[e.u]}) = ${e.start[e.v]}`)}.` : "");
          } else if (e.cycle) {
            const c = e.cycle, stuck = e.left.filter((v) => !c.includes(v));
            note = `התור התרוקן ונשארו ${ltr(names(e.left))}, כל אחת עם דרגה גדולה מ-0. הולכים אחורה מ-${ltr(L(c[0]))} דרך משימות שנשארו, עד שמשימה חוזרת${NB}: המעגל ${ltr(chain(c.concat([c[0]])))}.` +
              (stuck.length ? ` ${stuck.length === 1 ? "המשימה" : "המשימות"} ${ltr(names(stuck))} ${stuck.length === 1 ? "תקועה" : "תקועות"} בגללו, אבל לא עליו.` : "");
            ans = `${sched ? "אין לוח זמנים" : "אין סדר"}${NB}: המעגל ${ltr(chain(c.concat([c[0]])))}.`;
            marks = ".ts-graph .ts-node.is-cycle circle";
          } else if (!sched) {
            note = `התור ריק וכל ${n} המשימות יצאו, ולכן אין מעגל. הסדר ${ltr(names(e.order))}${NB}: כל חץ הולך ממשימה מוקדמת למאוחרת.`;
            ans = `הסדר ${ltr(names(e.order))}.`;
            marks = ".ts-graph .ts-qrow.is-o rect";
          } else {
            const path = tsCritPath(n, st.edges, st.dur, e), crit = e.slack.map((x, v) => (x === 0 ? v : -1)).filter((v) => v >= 0);
            const loose = e.slack.map((x, v) => (x > 0 ? `${L(v)} ${x}` : "")).filter(Boolean);
            const work = st.dur.reduce((x, y) => x + y, 0);
            note = `הכול נגמר בזמן ${e.total}, הסיום המאוחר ביותר. המעבר אחורה נותן לכל משימה את הסיום המאוחר שלא מעכב את הסוף, וההפרש הוא המרווח` +
              (loose.length ? `${NB}: ${ltr(loose.join(", "))}.` : `, 0 לכולן.`) + ` מריץ אחד היה צריך את סכום המשכים, ${work}.`;
            ans = `הכול נגמר בזמן ${e.total}. ${path.length > 1 ? `הנתיב הקריטי ${ltr(chain(path))}` : `המשימה הקריטית ${ltr(L(path[0] ?? crit[0]))}`}${crit.length > path.length ? `, וקריטיות גם ${ltr(names(crit.filter((v) => !path.includes(v))))}` : ""}.`;
            marks = ".ts-gwrap .ts-bar.is-crit rect";
          }
        }
        $(".ts-sum").innerHTML = sum;
        $(".ts-note").innerHTML = note;
        answer(box, done ? ans : null, marks);
      };
      const total = () => frames().length;
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= total(), restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; draw(); };
      const setGraph = (n, edges, msg = "") => {
        st.n = n; st.edges = edges; st.sel = null; st.err = ""; st.msg = msg;
        if (st.dur.length > n) st.dur = st.dur.slice(0, n);
        while (st.dur.length < n) st.dur.push(1);
        syncFields(); restart();
      };
      $(".ts-mode").addEventListener("change", () => { st.mode = MODES[$(".ts-mode").value] ? $(".ts-mode").value : "kahn"; st.msg = ""; restart(); });
      $(".ts-preset").addEventListener("change", () => {
        const p = PRESETS[$(".ts-preset").value];
        if (!p || !p.n) { $(".ts-preset").value = tsPreset(st.n, st.edges); return; }
        st.dur = p.dur.slice();
        setGraph(p.n, p.edges.map((x) => x.slice()));
      });
      $(".ts-n").addEventListener("change", () => {
        const n = Math.min(NMAX, Math.max(NMIN, Math.round(Number($(".ts-n").value)) || 7));
        setGraph(n, st.edges.filter(([a, b]) => a < n && b < n));
      });
      $(".ts-edges").addEventListener("change", () => {
        const p = tsParse($(".ts-edges").value, st.n);
        if (!p.edges) {
          st.err = p.many ? `עד ${EMAX} חצים.` : `לא הבנתי את ${ltr(p.err)}${NB}: כותבים חץ כמו ${ltr("A>B")} ("B אחרי A"), באותיות ${ltr(`A–${L(st.n - 1)}`)}, ומפרידים בפסיקים.`;
          st.msg = ""; stop(); st.s = 0; draw(); return;
        }
        setGraph(st.n, p.edges);
      });
      $(".ts-dur").addEventListener("change", () => {
        const d = tsParseDur($(".ts-dur").value, st.n);
        if (!d) {
          st.err = `צריך ${st.n} משכים, מספרים שלמים מ-0 עד ${DMAX}, אחד לכל משימה לפי הסדר ${ltr(names(Array.from({ length: st.n }, (_, v) => v)))}.`;
          st.msg = ""; stop(); st.s = 0; draw(); return;
        }
        st.dur = d; st.err = ""; st.msg = ""; syncFields(); restart();
      });
      // editing by clicking: a task, then another; the arrow from the first to the second
      // is added, or removed (every copy of it) when it is there
      const pick = (v) => {
        if (st.sel === null) { st.sel = v; st.msg = `נבחרה ${ltr(L(v))}. לחצו על משימה אחרת כדי להוסיף או למחוק את החץ מ-${ltr(L(v))} אליה, או שוב על ${ltr(L(v))} כדי לבטל.`; st.err = ""; draw(); return; }
        const a = st.sel;
        if (a === v) { st.sel = null; st.msg = ""; draw(); return; }
        const has = st.edges.some(([x, y]) => x === a && y === v);
        if (!has && st.edges.length >= EMAX) { st.sel = null; st.err = `עד ${EMAX} חצים.`; draw(); return; }
        const edges = has ? st.edges.filter(([x, y]) => !(x === a && y === v)) : st.edges.concat([[a, v]]);
        setGraph(st.n, edges, `${has ? "נמחק" : "נוסף"} החץ ${ltr(`${L(a)} → ${L(v)}`)}${has ? "" : `${NB}: ${ltr(L(v))} רצה אחרי ${ltr(L(a))}`}.`);
      };
      wrap.addEventListener("click", (ev) => { const g = ev.target.closest(".ts-node[data-v]"); if (g) { stop(); pick(Number(g.dataset.v)); } });
      wrap.addEventListener("keydown", (ev) => {
        const g = ev.target.closest(".ts-node[data-v]");
        if (!g) return;
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); stop(); pick(Number(g.dataset.v)); }
        else if (ev.key === "Escape" && st.sel !== null) { ev.preventDefault(); st.sel = null; st.msg = ""; draw(); }
      });
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => {
        Object.assign(st, { mode: init.mode, n: init.n, edges: init.edges.map((x) => x.slice()), dur: init.dur.slice(), sel: null, msg: "", err: "" });
        syncFields(); restart();
      });
      syncFields();
      draw();
    },
  });

  dvqExplorers.register({
    views: { toposort: topoView },
    help: {
      toposort: "בוחרים סעיף וגרף (הדוגמה של העמוד, הדוגמה עם מעגל, יהלום, שרשרת, בלי תלויות או לולאה עצמית) ומספר משימות. עורכים את הגרף בלחיצה על משימה ואחר כך על משימה אחרת : החץ מהראשונה לשנייה נוסף, או נמחק אם הוא כבר שם. אפשר גם לכתוב את החצים בשדה, כמו A>B, B>C (‏B אחרי A), ובסעיף ג את המשך של כל משימה. כל צעד הוא הוצאה אחת מהתור או הורדה של דרגה אחת : ליד כל משימה דרגת הכניסה שלה (בסעיף ג ההתחלה המוקדמת), וליד הגרף התור והסדר. כשהתור מתרוקן לפני שכל המשימות יצאו, המעגל מסומן באדום. בסעיף ג לוח הזמנים מתמלא כשמשימות יוצאות, ובסוף מסומנים המרווח והנתיב הקריטי. הפאנל 'הסבר' מדליק את שורות הקוד.",
    },
    cols: { toposort: { side: ".ts-note, .viz-legend, .ts-succ" } },   // the graph and the schedule beside the step's note, the legend and the successors
    models: { tsKahn, tsLayout, tsFindCycle, tsCritPath, tsParse, tsFormat, tsParseDur, tsPreset, tsPresets: () => PRESETS },
  });
})();
