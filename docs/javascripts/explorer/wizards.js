// kinds: wizards
//   wizards                0071        the three-wizard duel with the cat rule: two rivals, my place and the rivals' order, my wand; the four chances (me, each rival, the cats), the best choice over the six orders and every wand, the table of the six orders, the chart of my chance against my wand, and the game's Markov chain for the current choice
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { f, ltr } = dvqExplorers.lib;
  const NB = " ";

  // The model (0071): p in turn order. A duel to the end, the opener first; after a kill
  // in the first round the survivor is next in turn, so it opens against the killer. The
  // first round backward: each wizard keeps the air unless a target is better by more
  // than 1e-12 (the page's rule), targets in order 1, 2, 3.
  const wzDuel = (x, y) => x / (x + y - x * y);
  const wzRound = (p) => {
    let after = [0, 0, 0];
    const trace = [];
    for (const w of [2, 1, 0]) {
      const opts = { air: after };
      let best = "air";
      for (let t = 0; t < 3; t++) {
        if (t === w) continue;
        const o = 3 - w - t, hit = [0, 0, 0];
        hit[o] = wzDuel(p[o], p[w]);
        hit[w] = 1 - hit[o];
        opts[t + 1] = hit.map((h, k) => p[w] * h + (1 - p[w]) * after[k]);
        if (opts[t + 1][w] > opts[best][w] + 1e-12) best = String(t + 1);
      }
      trace.push({ w: w + 1, opts: Object.fromEntries(Object.entries(opts).map(([k, v]) => [k, v[w]])), choice: best });
      after = opts[best];
    }
    // the cats: nobody hit in the first round (a wizard in the air cannot hit)
    const choice = Object.fromEntries(trace.map((t) => [t.w, t.choice]));
    let cats = 1;
    for (let w = 1; w <= 3; w++) if (choice[w] !== "air") cats *= 1 - p[w - 1];
    return { win: after, trace, cats };
  };
  const wzPlace = (me, own, rivals) => { const p = rivals.slice(); p.splice(me - 1, 0, own); return p; };
  const wzChance = (me, own, rivals) => wzRound(wzPlace(me, own, rivals)).win[me - 1];
  // the best wand at a place: every 0.001 and the points just under the rivals and 0.5 (a
  // wand exactly equal to a rival is left out: there the tie rule decides, as on the page)
  const wzBest = (me, rivals) => {
    const qs = [];
    for (let k = 1; k <= 1000; k++) if (!rivals.some((r) => Math.abs(r - k / 1000) < 1e-12)) qs.push(k / 1000);
    rivals.forEach((r) => qs.push(r - 1e-9));
    qs.push(0.5 - 1e-9);
    let best = { chance: -1, wand: 0 };
    qs.forEach((q) => { const v = wzChance(me, q, rivals); if (v > best.chance || (v === best.chance && q > best.wand)) best = { chance: v, wand: q }; });
    return best;
  };
  // the six orders against rivals a and b: my place 1..3, then a before b, then b before a
  const wzOrders = (a, b) => {
    const rows = [];
    for (const me of [1, 2, 3]) {
      for (const order of ["ab", "ba"]) {
        const rivals = order === "ab" ? [a, b] : [b, a], best = wzBest(me, rivals), res = wzRound(wzPlace(me, best.wand, rivals));
        rows.push({ me, order, rivals, wand: best.wand, win: res.win, cats: res.cats });
      }
    }
    return rows;
  };

  const POS = ["ראשון", "שני", "שלישי"];
  const pct = (v) => `${(v * 100).toFixed(1)}%`;
  const short = (v) => { const s = Number(v).toFixed(3).replace(/0+$/, "").replace(/\.$/, ""); return s || "0"; };
  const wandText = (q) => { const r = Math.round(q * 1000) / 1000; return Math.abs(q - r) > 1e-12 && q < r ? `${r}⁻` : String(r); };

  // The chart: my chance against my wand, broken where it jumps; the current wand and the
  // best. Its own small frame, so that it can sit beside the table; the hover group (a line,
  // a dot and the values) is moved by the pointer, a click sets the wand.
  const CWD = 360, CHT = 230, CX0 = 44, CRT = 12, CTP = 14, CBS = 196;
  const cX = (x) => CX0 + x * (CWD - CX0 - CRT), cY = (v) => CBS - v * (CBS - CTP);
  const chart = (me, rivals, own, best) => {
    let s = `<svg class="perf-chart wz-live" viewBox="0 0 ${CWD} ${CHT}" role="img" aria-label="הסיכוי שלי לנצח כפונקציה של השרביט">`;
    [0, 0.2, 0.4, 0.6, 0.8, 1].forEach((v) => {
      s += `<line class="grid" x1="${CX0}" x2="${CWD - CRT}" y1="${f(cY(v))}" y2="${f(cY(v))}"/><text class="tick" x="${CX0 - 6}" y="${f(cY(v) + 4)}" text-anchor="end">${v * 100}%</text>`;
      s += `<text class="tick" x="${f(cX(v))}" y="${CBS + 18}" text-anchor="middle">${v}</text>`;
    });
    rivals.forEach((r) => { s += `<line class="grid" x1="${f(cX(r))}" x2="${f(cX(r))}" y1="${CTP}" y2="${CBS}" stroke-dasharray="4 4"/>`; });
    let pts = [], prev = null;
    const flush = () => { if (pts.length > 1) s += `<polyline class="s1-line" points="${pts.join(" ")}" fill="none" stroke-width="2.5"/>`; pts = []; };
    for (let k = 1; k <= 200; k++) {
      const x = k / 200 - 1e-7, v = wzChance(me, x, rivals);
      if (prev !== null && Math.abs(v - prev) > 0.04) flush();
      pts.push(`${f(cX(x))},${f(cY(v))}`);
      prev = v;
    }
    flush();
    const now = wzChance(me, own, rivals);
    s += `<circle class="s3-dot" cx="${f(cX(best.wand))}" cy="${f(cY(best.chance))}" r="6"><title>${pct(best.chance)}</title></circle>`;
    s += `<circle class="s2-dot" cx="${f(cX(own))}" cy="${f(cY(now))}" r="6"><title>${pct(now)}</title></circle>`;
    s += `<line class="axis" x1="${CX0}" x2="${CWD - CRT}" y1="${CBS}" y2="${CBS}"/>`;
    s += `<g class="wz-hover" visibility="hidden"><line class="wz-hline" y1="${CTP}" y2="${CBS}"/><circle class="wz-hdot" r="5"/><rect class="wz-hbg" rx="4" height="22"/><text class="wz-htext" dy="0.32em"></text></g>`;
    return s + `<rect class="wz-hit" x="${CX0}" y="${CTP}" width="${CWD - CX0 - CRT}" height="${CBS - CTP}" fill="transparent"/></svg>`;
  };

  // The Markov chain of the current choice: the same drawing as tools/figures/q0071.py's
  // chain_svg (the states, the chosen edges with their chances, the absorbing chances). Each
  // edge carries its two ends (data-a, data-b) and each state its key (data-s).
  const CP = {
    R1: [70, 40], R2: [180, 40], R3: [290, 40], CATS: [400, 40],
    "1,2,1": [44, 176], "1,2,2": [122, 176], "1,3,1": [200, 176], "1,3,3": [278, 176], "2,3,2": [356, 176], "2,3,3": [434, 176],
    W1: [100, 300], W2: [240, 300], W3: [380, 300],
  };
  const LABEL_AT = { 12: [0.55, 0], 13: [0.45, -10], 23: [0.25, 10], 21: [0.35, 8], 31: [0.6, 12], 32: [0.42, -12] };
  const duelOf = (killer, victim) => { const [i, j] = [1, 2, 3].filter((k) => k !== victim); return `${i},${j},${6 - killer - victim}`; };
  const isDuel = (k) => k.includes(",");
  const chainBox = (key, lines, cls, w, me, faded) => {
    const [x, y] = CP[key];
    let s = `<g class="mk-state${faded ? " st-faded" : ""}" data-s="${key}" tabindex="0" role="button">` +
      `<rect class="${cls}${me ? " mk-me" : ""}" x="${x - w / 2}" y="${y - 20}" width="${w}" height="40" rx="7"/>`;
    if (lines.length === 1) s += `<text class="mk-text" x="${x}" y="${y + 5}" text-anchor="middle" direction="rtl">${lines[0]}</text>`;
    else s += `<text class="mk-text" x="${x}" y="${y - 3}" text-anchor="middle" direction="rtl">${lines[0]}</text><text class="mk-text mk-sub" x="${x}" y="${y + 13}" text-anchor="middle" direction="rtl">${lines[1]}</text>`;
    return s + "</g>";
  };
  const chainEdge = (a, b, cls, label, t = 0.5, dx = 0, bend = 0) => {
    let [x1, y1] = CP[a], [x2, y2] = CP[b], line, lx, ly;
    const ends = `data-a="${a}" data-b="${b}"`;
    if (y1 === y2) {
      const s = x2 > x1 ? 1 : -1;
      if (bend) {
        const sx = x1 + s * 10, ex = x2 - s * 10, sy = y1 + bend * 20, cx = (sx + ex) / 2, cy = sy + bend * 14;
        line = `<path class="${cls}" ${ends} d="M${sx},${sy} Q${cx},${cy} ${ex},${sy}" fill="none" marker-end="url(#wz-arrow)"/>`;
        lx = cx; ly = sy + bend * 12 + (bend > 0 ? 12 : -4);
      } else {
        const sx = x1 + s * (isDuel(a) ? 32 : 42), ex = x2 - s * (isDuel(b) ? 32 : 42);
        line = `<line class="${cls}" ${ends} x1="${sx}" y1="${y1}" x2="${ex}" y2="${y2}" marker-end="url(#wz-arrow)"/>`;
        lx = (sx + ex) / 2; ly = y1 - 7;
      }
    } else {
      const sy = y1 + 20, ey = y2 - 21, sx = x1 + (x2 - x1) * 0.12, ex = x2 - (x2 - x1) * 0.04;
      line = `<line class="${cls}" ${ends} x1="${f(sx, 0)}" y1="${sy}" x2="${f(ex, 0)}" y2="${ey}" marker-end="url(#wz-arrow)"/>`;
      lx = sx + (ex - sx) * t; ly = sy + (ey - sy) * t + 4;
    }
    return [line, label ? `<text class="mk-lab" ${ends} x="${f(lx + dx, 0)}" y="${f(ly, 0)}" text-anchor="middle">${label}</text>` : ""];
  };
  const chainSvg = (p, me) => {
    const res = wzRound(p), choice = Object.fromEntries(res.trace.map((t) => [t.w, t.choice]));
    const edges = [], labels = [], used = new Set(["R1"]);
    const steps = [[1, "R2"], [2, "R3"], [3, "CATS"]];
    for (const [w, nxt] of steps) {
      const key = `R${w}`;
      if (!used.has(key)) break;
      if (choice[w] !== "air") {
        const t = Number(choice[w]), d = duelOf(w, t), [at, dx] = LABEL_AT[`${w}${t}`];
        const [e, l] = chainEdge(key, d, "mk-hit", short(p[w - 1]), at, dx);
        edges.push(e); labels.push(l); used.add(d);
      }
      const air = choice[w] === "air";
      const [e, l] = chainEdge(key, nxt, "mk-miss", air ? "1" : short(1 - p[w - 1]));
      edges.push(e); labels.push(l); used.add(nxt);
      if (air) labels.push(`<text class="mk-lab" data-a="${key}" data-b="${nxt}" x="${(CP[key][0] + CP[nxt][0]) / 2}" y="${CP[key][1] + 34}" text-anchor="middle" direction="rtl">באוויר</text>`);
    }
    Object.keys(CP).filter(isDuel).forEach((d) => {
      if (!used.has(d)) return;
      const [i, j, k] = d.split(",").map(Number), other = `${i},${j},${k === i ? j : i}`;
      used.add(other);
      let [e, l] = chainEdge(d, `W${k}`, "mk-hit", short(p[k - 1]), CP[`W${k}`][0] > CP[d][0] ? 0.62 : 0.45, CP[`W${k}`][0] > CP[d][0] ? 16 : -16);
      edges.push(e); labels.push(l); used.add(`W${k}`);
      [e, l] = chainEdge(d, other, "mk-miss", short(1 - p[k - 1]), 0.5, 0, k === i ? -1 : 1);
      edges.push(e); labels.push(l);
    });
    const boxes = [];
    [1, 2, 3].forEach((w) => boxes.push(chainBox(`R${w}`, ["כולם חיים", `תור ${w}`], "mk-node", 84, w === me, !used.has(`R${w}`))));
    boxes.push(chainBox("CATS", ["חתולים", pct(res.cats)], "mk-cat", 84, false, !used.has("CATS")));
    Object.keys(CP).filter(isDuel).forEach((d) => { const [i, j, k] = d.split(",").map(Number); boxes.push(chainBox(d, [`${i} מול ${j}`, `תור ${k}`], "mk-node", 64, k === me, !used.has(d))); });
    [1, 2, 3].forEach((k) => boxes.push(chainBox(`W${k}`, [`${k} מנצח`, pct(res.win[k - 1])], "mk-win", 96, k === me, !used.has(`W${k}`))));
    return `<svg class="figure mk-chain" viewBox="0 0 480 340" role="group" data-p="${p.join(",")}" data-me="${me}" aria-label="שרשרת מרקוב של הבחירה הנוכחית : הסיכויים הסופיים ${res.win.map(pct).join(", ")}, חתולים ${pct(res.cats)}">` +
      `<defs><marker id="wz-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="mk-head"/></marker></defs>` +
      edges.join("") + boxes.join("") + labels.join("") + "</svg>";
  };

  // How the number of each state comes about (q0071.chain_states): the chance to ever reach
  // it; for a duel state, the chance that the wizard to shoot wins the duel from there; for
  // a win, its terms: the chance to enter a duel at a state times the winner's chance there.
  const wzStates = (p) => {
    const res = wzRound(p), choice = Object.fromEntries(res.trace.map((t) => [t.w, t.choice]));
    const out = { R1: { reach: 1 } }, direct = {};
    let r = 1;
    [[1, "R2"], [2, "R3"], [3, "CATS"]].forEach(([w, nxt]) => {
      const c = choice[w], keep = c === "air" ? 1 : 1 - p[w - 1];
      out[`R${w}`].choice = c;
      if (c !== "air") { const d = duelOf(w, Number(c)); direct[d] = (direct[d] || 0) + r * p[w - 1]; out[`R${w}`].hit = { d, x: p[w - 1] }; }
      out[nxt] = { reach: r * keep, prev: r, keep, w };
      r *= keep;
    });
    Object.keys(CP).filter(isDuel).forEach((d) => {
      const [i, j, k] = d.split(",").map(Number), o = k === i ? j : i, partner = `${i},${j},${o}`;
      out[d] = { reach: (direct[d] || 0) + (direct[partner] || 0) * (1 - p[o - 1]), direct: direct[d] || 0, fromPartner: (direct[partner] || 0), k, o, duel: wzDuel(p[k - 1], p[o - 1]) };
    });
    [1, 2, 3].forEach((k) => {
      const terms = [];
      Object.entries(direct).forEach(([d, rr]) => {
        const [i, j, s] = d.split(",").map(Number);
        if ((k !== i && k !== j) || !rr) return;
        const other = k === i ? j : i;
        terms.push({ d, r: rr, v: s === k ? wzDuel(p[k - 1], p[other - 1]) : 1 - wzDuel(p[s - 1], p[k - 1]) });
      });
      out[`W${k}`] = { reach: terms.reduce((a, t) => a + t.r * t.v, 0), terms };
    });
    return out;
  };

  // The line under a chain: how the state's number came about, in one or two lines.
  const n3 = (v) => { const s = Number(v).toFixed(3).replace(/0+$/, "").replace(/\.$/, ""); return s || "0"; };
  // Each formula is a block of its own, left to right, so that a long one wraps in order.
  const M = (x) => `<span class="mk-math" dir="ltr">${x}</span>`;
  const explainState = (key, p, me) => {
    const st = wzStates(p), e = st[key], P = (k) => (k === me ? wandText(p[k - 1]) : short(p[k - 1]));
    const who = (c, w) => (c === "air" ? `קוסם ${w} מכשף באוויר.` : `קוסם ${w} מכשף על קוסם ${c}${c === String(me) ? " (עליי)" : ""}.`);
    if (key === "R1") return `<b>כולם חיים, תור 1${NB}:</b> ההתחלה, מגיעים לכאן בהסתברות ${ltr(1)}. ${who(e.choice, 1)}`;
    if (key === "R2" || key === "R3") {
      const w = e.w, keepText = e.keep === 1 ? "1" : `(1 − ${P(w)})`, head = `<b>כולם חיים, תור ${w + 1}${NB}:</b> `;
      if (!e.reach) return `${head}קוסם ${w} פוגע תמיד, ולכן אף מסלול לא מגיע לכאן.`;
      return `${head}${e.keep === 1 ? `קוסם ${w} כישף באוויר` : `קוסם ${w} החטיא`}, ולכן מגיעים לכאן בהסתברות${NB}: ` +
        M(`${n3(e.prev)} · ${keepText} = ${n3(e.reach)}`) + who(st[key].choice, w + 1);
    }
    if (key === "CATS") {
      const f3 = [1, 2, 3].map((w) => (st[`R${w}`].choice === "air" ? "1" : `(1 − ${P(w)})`));
      return `<b>חתולים${NB}:</b> אף אחד לא פגע בסבב הראשון${NB}: ` + M(`${f3.join(" · ")} = ${n3(e.reach)}`);
    }
    if (isDuel(key)) {
      const [i, j] = key.split(",").map(Number), { k, o } = e, head = `<b>דו-קרב ${i} מול ${j}, תור ${k}${NB}:</b> `;
      if (!e.reach) return `${head}בבחירות האלה אף מסלול לא מגיע לכאן.`;
      const parts = [];
      [1, 2, 3].forEach((w) => { const h = st[`R${w}`].hit; if (h && h.d === key) parts.push(`${n3(st[`R${w}`].reach)} · ${P(w)}`); });
      if (e.fromPartner) parts.push(`${n3(e.fromPartner)} · (1 − ${P(o)})`);
      return `${head}ההסתברות להגיע לכאן, ואז הסיכוי של קוסם ${k} לנצח את הדו-קרב${NB}: ` +
        M(`${parts.join(" + ")} = ${n3(e.reach)}`) +
        M(`V(${P(k)}, ${P(o)}) = ${P(k)} / (${P(k)} + ${P(o)} − ${P(k)}·${P(o)}) = ${n3(e.duel)}`);
    }
    const k = Number(key.slice(1)), head = `<b>קוסם ${k} מנצח${NB}:</b> `;
    if (!e.terms.length) return `${head}אף מסלול לא מגיע לכאן.`;
    return `${head}לכל חץ שנכנס, ההסתברות להגיע לדו-קרב כפול הסיכוי של קוסם ${k} לנצח בו, ומחברים${NB}: ` +
      M(`${e.terms.map((t) => `${n3(t.r)} · ${n3(t.v)}`).join(" + ")} = ${n3(e.reach)}`);
  };

  // Light a state's edges and neighbours, dim the rest, and explain the state; `root` holds
  // the chain (re-drawn by the box, or a page figure), `line` is the explanation's line.
  const wireChain = (root, line) => {
    const svgOf = () => root.matches("svg") ? root : root.querySelector("svg.mk-chain");
    const clear = () => { const svg = svgOf(); if (!svg) return; svg.classList.remove("mk-focus"); svg.querySelectorAll(".is-on").forEach((x) => x.classList.remove("is-on")); };
    const show = (g) => {
      const svg = svgOf();
      if (!svg || !g) return;
      clear();
      const key = g.dataset.s, p = svg.dataset.p.split(",").map(Number), me = Number(svg.dataset.me);
      svg.classList.add("mk-focus");
      g.classList.add("is-on");
      svg.querySelectorAll("[data-a]").forEach((x) => {
        if (x.dataset.a === key || x.dataset.b === key) {
          x.classList.add("is-on");
          const other = x.dataset.a === key ? x.dataset.b : x.dataset.a, n = svg.querySelector(`[data-s="${other}"]`);
          if (n) n.classList.add("is-on");
        }
      });
      if (line) line.innerHTML = explainState(key, p, me);
    };
    const at = (e) => e.target.closest && e.target.closest("[data-s]");
    root.addEventListener("pointerover", (e) => { const g = at(e); if (g) show(g); });
    root.addEventListener("pointerdown", (e) => { const g = at(e); if (g) show(g); });
    root.addEventListener("focusin", (e) => { const g = at(e); if (g) show(g); });
    root.addEventListener("pointerleave", clear);
    root.addEventListener("focusout", (e) => { if (!root.contains(e.relatedTarget)) clear(); });
  };
  // The page's own chain (part a): the figure from q0071.py carries data-p, data-me and the
  // id of its explanation line.
  if (typeof document !== "undefined") {
    const wireStatic = () => document.querySelectorAll("svg.mk-chain[data-p][data-explain]").forEach((svg) => {
      if (svg.dataset.wired) return;
      svg.dataset.wired = "1";
      wireChain(svg, document.getElementById(svg.dataset.explain));
    });
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", wireStatic); else wireStatic();
  }

  const wizardsView = () => ({
    mount(box) {
      const num = (v, d) => (Number.isFinite(Number(v)) && v !== undefined ? Number(v) : d);
      const st = { a: num(box.dataset.r1, 0.6), b: num(box.dataset.r2, 0.8), me: num(box.dataset.me, 1), order: box.dataset.order === "ba" ? "ba" : "ab", wand: num(box.dataset.wand, 0.599) };
      box.innerHTML =
        `<div class="ex-controls"><label><span>יריב א</span><input type="range" class="wz-r1" min="0.05" max="1" step="0.05" dir="ltr" aria-label="ההסתברות של יריב א לפגוע"><output class="wz-o1"></output></label>` +
        `<label><span>יריב ב</span><input type="range" class="wz-r2" min="0.05" max="1" step="0.05" dir="ltr" aria-label="ההסתברות של יריב ב לפגוע"><output class="wz-o2"></output></label></div>` +
        `<div class="ex-controls"><label>אני <select class="wz-me" aria-label="התור שלי">${POS.map((n, i) => `<option value="${i + 1}">${n}</option>`).join("")}</select></label>` +
        `<label>הסדר <select class="wz-order" aria-label="הסדר של היריבים"><option value="ab">א לפני ב</option><option value="ba">ב לפני א</option></select></label>` +
        `<label><span>השרביט שלי</span><input type="range" class="wz-wand" min="0.001" max="1" step="0.001" dir="ltr" aria-label="ההסתברות שלי לפגוע"><output class="wz-ow"></output></label></div>` +
        `<div class="ex-controls"><button type="button" class="md-button wz-weak">ממש מתחת ליריב החלש</button>` +
        `<button type="button" class="md-button wz-sniper">צלף (1)</button>` +
        `<button type="button" class="md-button md-button--primary wz-best">הבחירה הטובה ביותר</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p><div class="wz-out"></div>` +
        `<div class="wz-duo"><div class="wz-col"><p class="ex-title">ששת הסדרים, כל אחד עם השרביט הטוב ביותר שלו; לחיצה על שורה בוחרת אותה</p>` +
        `<div class="wz-tablewrap" role="region" aria-label="ששת הסדרים"></div></div>` +
        `<div class="wz-col"><p class="ex-title">הסיכוי שלי לכל שרביט; לחיצה על הגרף קובעת שרביט</p><div class="wz-chart"></div>` +
        `<span class="viz-legend"><span><i class="s1"></i>הסיכוי שלי</span><span><i class="s2"></i>השרביט שלי</span><span><i class="s3"></i>הטוב ביותר בתור הזה</span></span></div></div>` +
        `<p class="ex-title">שרשרת מרקוב של הבחירה${NB}: על החצים ההסתברויות, ובמצבים הסופיים הסיכוי להגיע אליהם</p><div class="wz-chain"></div>` +
        `<p class="mk-explain wz-explain" aria-live="polite">מעבירים את העכבר מעל מצב, או נוגעים בו, ורואים את החצים שלו ואיך התקבל המספר שלו.</p>` +
        `<span class="viz-legend"><span><i class="mk-key-hit"></i>פגיעה</span><span><i class="mk-key-miss"></i>החטאה או באוויר</span><span><i class="mk-key-win"></i>ניצחון</span><span><i class="mk-key-cat"></i>חתולים</span><span><i class="mk-key-me"></i>המצבים שלי</span></span>`;
      const $ = (sel) => box.querySelector(sel);
      const rivals = () => (st.order === "ab" ? [st.a, st.b] : [st.b, st.a]);
      const sliderWand = (q) => Math.min(1, Math.max(0.001, Math.round(q * 1000) / 1000 - (q < Math.round(q * 1000) / 1000 - 1e-7 ? 0.001 : 0)));
      const sync = () => {
        $(".wz-r1").value = st.a; $(".wz-r2").value = st.b; $(".wz-me").value = String(st.me); $(".wz-order").value = st.order;
        $(".wz-wand").value = sliderWand(st.wand);
      };
      const draw = () => {
        $(".wz-o1").textContent = String(st.a); $(".wz-o2").textContent = String(st.b); $(".wz-ow").textContent = wandText(st.wand);
        const rv = rivals(), p = wzPlace(st.me, st.wand, rv), res = wzRound(p), best = wzBest(st.me, rv), mine = res.win[st.me - 1];
        const names = [0, 1, 2].map((k) => (k === st.me - 1 ? "אני" : null));
        const order = st.order === "ab" ? ["א", "ב"] : ["ב", "א"];
        let r = 0;
        for (let k = 0; k < 3; k++) if (names[k] === null) names[k] = `יריב ${order[r++]}`;
        $(".ex-summary").innerHTML = `התורות${NB}: ${names.map((n, k) => `${POS[k]} ${n} (${ltr(k === st.me - 1 ? wandText(st.wand) : p[k])})`).join(", ")}. ` +
          `הסיכוי שלי לנצח ${ltr(pct(mine))}; עם השרביט הטוב ביותר בתור ובסדר האלה, ${ltr(wandText(best.wand))}, הוא ${ltr(pct(best.chance))}.`;
        const outs = names.map((n, k) => `<span${k === st.me - 1 ? ' class="is-me"' : ""}>${n}${NB}: ${ltr(pct(res.win[k]))}</span>`);
        $(".wz-out").innerHTML = outs.join("") + `<span>חתולים${NB}: ${ltr(pct(res.cats))}</span>`;
        const rows = wzOrders(st.a, st.b), top = Math.max(...rows.map((o) => o.win[o.me - 1]));
        let t = `<table class="wz-table"><thead><tr><th>הסדר</th><th>השרביט</th><th>אני</th><th>יריב א</th><th>יריב ב</th><th>חתולים</th></tr></thead><tbody>`;
        rows.forEach((o, i) => {
          const pp = wzPlace(o.me, o.wand, o.rivals);
          const seq = [0, 1, 2].map((k) => (k === o.me - 1 ? "אני" : ltr(short(pp[k])))).join(" ← ");
          const ia = [0, 1, 2].filter((k) => k !== o.me - 1)[o.order === "ab" ? 0 : 1], ib = [0, 1, 2].filter((k) => k !== o.me - 1)[o.order === "ab" ? 1 : 0];
          const now = o.me === st.me && o.order === st.order, isBest = Math.abs(o.win[o.me - 1] - top) < 1e-12;
          const name = `לבחור את הסדר ${[0, 1, 2].map((k) => (k === o.me - 1 ? "אני" : short(pp[k]))).join(", ")}, השרביט ${wandText(o.wand)}, הסיכוי שלי ${pct(o.win[o.me - 1])}`;
          t += `<tr data-i="${i}" tabindex="0" aria-label="${name}" class="${[now ? "is-now" : "", isBest ? "is-best" : ""].join(" ").trim()}"><td class="wz-seq">${seq}</td><td>${ltr(wandText(o.wand))}</td><td>${ltr(pct(o.win[o.me - 1]))}</td><td>${ltr(pct(o.win[ia]))}</td><td>${ltr(pct(o.win[ib]))}</td><td>${ltr(pct(o.cats))}</td></tr>`;
        });
        $(".wz-tablewrap").innerHTML = t + "</tbody></table>";
        $(".wz-chart").innerHTML = chart(st.me, rv, st.wand, best);
        $(".wz-chain").innerHTML = chainSvg(p, st.me);
      };
      const pick = (o) => { st.me = o.me; st.order = o.order; st.wand = o.wand; sync(); draw(); };
      const read = () => { st.a = Number($(".wz-r1").value); st.b = Number($(".wz-r2").value); st.me = Number($(".wz-me").value); st.order = $(".wz-order").value; draw(); };
      ["wz-r1", "wz-r2", "wz-me", "wz-order"].forEach((c) => $(`.${c}`).addEventListener(c === "wz-me" || c === "wz-order" ? "change" : "input", read));
      $(".wz-wand").addEventListener("input", () => { st.wand = Number($(".wz-wand").value); draw(); });
      const setWand = (q) => { st.wand = q; $(".wz-wand").value = sliderWand(q); draw(); };
      $(".wz-weak").addEventListener("click", () => setWand(Math.max(0.001, Math.min(st.a, st.b) - 1e-9)));
      $(".wz-sniper").addEventListener("click", () => setWand(1));
      $(".wz-best").addEventListener("click", () => {
        const rows = wzOrders(st.a, st.b);
        pick(rows.reduce((m, o) => (o.win[o.me - 1] > m.win[m.me - 1] + 1e-12 ? o : m)));
      });
      const pickRow = (tr) => {
        const i = tr.dataset.i, focused = document.activeElement === tr;
        pick(wzOrders(st.a, st.b)[Number(i)]);
        if (focused) { const again = $(`.wz-tablewrap tr[data-i="${i}"]`); if (again) again.focus(); }
      };
      $(".wz-tablewrap").addEventListener("click", (e) => { const tr = e.target.closest("tr[data-i]"); if (tr) pickRow(tr); });
      $(".wz-tablewrap").addEventListener("keydown", (e) => {
        const tr = e.target.closest("tr[data-i]");
        if (tr && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); pickRow(tr); }
      });
      // the chart: a line and a dot follow the pointer with the wand and my chance; a click
      // (or a tap) sets the wand there
      const wandAt = (e) => {
        const svg = $(".wz-chart svg");
        if (!svg || !svg.getScreenCTM()) return null;
        const pt = svg.createSVGPoint();
        pt.x = e.clientX; pt.y = e.clientY;
        const x = pt.matrixTransform(svg.getScreenCTM().inverse()).x;
        return Math.min(1, Math.max(0.001, Math.round(((x - CX0) / (CWD - CX0 - CRT)) * 1000) / 1000));
      };
      const hover = (e) => {
        const q = wandAt(e), g = $(".wz-chart .wz-hover");
        if (q === null || !g) return;
        const v = wzChance(st.me, q, rivals()), x = cX(q), y = cY(v), txt = `${q} → ${pct(v)}`;
        g.setAttribute("visibility", "visible");
        g.querySelector(".wz-hline").setAttribute("x1", f(x)); g.querySelector(".wz-hline").setAttribute("x2", f(x));
        g.querySelector(".wz-hdot").setAttribute("cx", f(x)); g.querySelector(".wz-hdot").setAttribute("cy", f(y));
        const t = g.querySelector(".wz-htext"), w = txt.length * 7.6 + 12, left = x + w + 10 > CWD - CRT;
        const tx = left ? x - 8 - w : x + 8, ty = Math.min(Math.max(y - 18, CTP + 11), CBS - 11);
        t.textContent = txt; t.setAttribute("x", f(tx + 6)); t.setAttribute("y", f(ty));
        const bg = g.querySelector(".wz-hbg");
        bg.setAttribute("x", f(tx)); bg.setAttribute("y", f(ty - 11)); bg.setAttribute("width", f(w));
      };
      $(".wz-chart").addEventListener("pointermove", hover);
      $(".wz-chart").addEventListener("pointerdown", hover);
      $(".wz-chart").addEventListener("pointerleave", () => { const g = $(".wz-chart .wz-hover"); if (g) g.setAttribute("visibility", "hidden"); });
      $(".wz-chart").addEventListener("click", (e) => { const q = wandAt(e); if (q !== null) { setWand(q); hover(e); } });
      wireChain($(".wz-chain"), $(".wz-explain"));
      sync();
      draw();
    },
  });

  dvqExplorers.register({
    views: { wizards: wizardsView },
    help: {
      wizards: "בוחרים את שני היריבים, את התור שלי, את הסדר שלהם ואת השרביט : מתחת לכפתורים הסיכויים של כולם ושל החתולים. ״הבחירה הטובה ביותר״ עוברת על ששת הסדרים ועל כל השרביטים. הטבלה מראה את ששת הסדרים, הגרף את הסיכוי שלי לכל שרביט, ושרשרת מרקוב את המשחק עם הבחירות של כולם.",
    },
    cols: { wizards: { main: ".wz-duo", side: ".ex-title, .wz-chain, .wz-explain, .viz-legend", w: "minmax(0, 0.75fr)" } },   // the six orders and the chart (stacked) beside the chain; the outcome chips stay full width
    models: { wzDuel, wzRound, wzChance, wzBest, wzOrders, wzStates, explainState },
  });
})();
