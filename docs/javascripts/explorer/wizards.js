// kinds: wizards
//   wizards                0071        the three-wizard duel with the cat rule: two rivals, my place and the rivals' order, my wand; the four chances (me, each rival, the cats), the best choice over the six orders and every wand, the table of the six orders, the chart of my chance against my wand, and the game's Markov chain for the current choice
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, RIGHT, TOP, W, X0, f, ltr } = dvqExplorers.lib;
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

  // The chart: my chance against my wand, broken where it jumps; the current wand and the best.
  const H = 230;
  const chart = (me, rivals, own, best) => {
    const X = (x) => X0 + x * (W - X0 - RIGHT), Y = (v) => BASE - v * (BASE - TOP);
    let s = `<svg class="perf-chart wz-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="הסיכוי שלי לנצח כפונקציה של השרביט">`;
    [0, 0.2, 0.4, 0.6, 0.8, 1].forEach((v) => {
      s += `<line class="grid" x1="${X0}" x2="${W - RIGHT}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v * 100}%</text>`;
      s += `<text class="tick" x="${f(X(v))}" y="${BASE + 18}" text-anchor="middle">${v}</text>`;
    });
    rivals.forEach((r) => { s += `<line class="grid" x1="${f(X(r))}" x2="${f(X(r))}" y1="${TOP}" y2="${BASE}" stroke-dasharray="4 4"/>`; });
    let pts = [], prev = null;
    const flush = () => { if (pts.length > 1) s += `<polyline class="s1-line" points="${pts.join(" ")}" fill="none" stroke-width="2.5"/>`; pts = []; };
    for (let k = 1; k <= 200; k++) {
      const x = k / 200 - 1e-7, v = wzChance(me, x, rivals);
      if (prev !== null && Math.abs(v - prev) > 0.04) flush();
      pts.push(`${f(X(x))},${f(Y(v))}`);
      prev = v;
    }
    flush();
    const now = wzChance(me, own, rivals);
    s += `<circle class="s3-dot" cx="${f(X(best.wand))}" cy="${f(Y(best.chance))}" r="6"><title>${pct(best.chance)}</title></circle>`;
    s += `<circle class="s2-dot" cx="${f(X(own))}" cy="${f(Y(now))}" r="6"><title>${pct(now)}</title></circle>`;
    return s + `<line class="axis" x1="${X0}" x2="${W - RIGHT}" y1="${BASE}" y2="${BASE}"/></svg>`;
  };

  // The Markov chain of the current choice: the same drawing as tools/figures/q0071.py's
  // chain_svg (the states, the chosen edges with their chances, the absorbing chances).
  const CP = {
    R1: [62, 46], R2: [180, 46], R3: [298, 46], CATS: [420, 46],
    "1,2,1": [44, 214], "1,2,2": [122, 214], "1,3,1": [200, 214], "1,3,3": [278, 214], "2,3,2": [356, 214], "2,3,3": [434, 214],
    W1: [90, 372], W2: [240, 372], W3: [390, 372],
  };
  const LABEL_AT = { 12: [0.55, 0], 13: [0.45, -10], 23: [0.25, 10], 21: [0.35, 8], 31: [0.6, 12], 32: [0.42, -12] };
  const duelOf = (killer, victim) => { const [i, j] = [1, 2, 3].filter((k) => k !== victim); return `${i},${j},${6 - killer - victim}`; };
  const isDuel = (k) => k.includes(",");
  const chainBox = (key, lines, cls, w, me) => {
    const [x, y] = CP[key];
    let s = `<rect class="${cls}${me ? " mk-me" : ""}" x="${x - w / 2}" y="${y - 20}" width="${w}" height="40" rx="7"/>`;
    if (lines.length === 1) s += `<text class="mk-text" x="${x}" y="${y + 5}" text-anchor="middle" direction="rtl">${lines[0]}</text>`;
    else s += `<text class="mk-text" x="${x}" y="${y - 3}" text-anchor="middle" direction="rtl">${lines[0]}</text><text class="mk-text mk-sub" x="${x}" y="${y + 13}" text-anchor="middle" direction="rtl">${lines[1]}</text>`;
    return s;
  };
  const chainEdge = (a, b, cls, label, t = 0.5, dx = 0, bend = 0) => {
    let [x1, y1] = CP[a], [x2, y2] = CP[b], line, lx, ly;
    if (y1 === y2) {
      const s = x2 > x1 ? 1 : -1;
      if (bend) {
        const sx = x1 + s * 10, ex = x2 - s * 10, sy = y1 + bend * 20, cx = (sx + ex) / 2, cy = sy + bend * 14;
        line = `<path class="${cls}" d="M${sx},${sy} Q${cx},${cy} ${ex},${sy}" fill="none" marker-end="url(#wz-arrow)"/>`;
        lx = cx; ly = sy + bend * 12 + (bend > 0 ? 12 : -4);
      } else {
        const sx = x1 + s * (isDuel(a) ? 32 : 42), ex = x2 - s * (isDuel(b) ? 32 : 42);
        line = `<line class="${cls}" x1="${sx}" y1="${y1}" x2="${ex}" y2="${y2}" marker-end="url(#wz-arrow)"/>`;
        lx = (sx + ex) / 2; ly = y1 - 7;
      }
    } else {
      const sy = y1 + 20, ey = y2 - 21, sx = x1 + (x2 - x1) * 0.12, ex = x2 - (x2 - x1) * 0.04;
      line = `<line class="${cls}" x1="${f(sx, 0)}" y1="${sy}" x2="${f(ex, 0)}" y2="${ey}" marker-end="url(#wz-arrow)"/>`;
      lx = sx + (ex - sx) * t; ly = sy + (ey - sy) * t + 4;
    }
    return [line, label ? `<text class="mk-lab" x="${f(lx + dx, 0)}" y="${f(ly, 0)}" text-anchor="middle">${label}</text>` : ""];
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
      if (air) labels.push(`<text class="mk-lab" x="${(CP[key][0] + CP[nxt][0]) / 2}" y="${CP[key][1] + 34}" text-anchor="middle" direction="rtl">באוויר</text>`);
    }
    Object.keys(CP).filter(isDuel).forEach((d) => {
      if (!used.has(d)) return;
      const [i, j, k] = d.split(",").map(Number), other = `${i},${j},${k === i ? j : i}`;
      used.add(other);
      let [e, l] = chainEdge(d, `W${k}`, "mk-hit", short(p[k - 1]), 0.4, CP[`W${k}`][0] > CP[d][0] ? 14 : -14);
      edges.push(e); labels.push(l); used.add(`W${k}`);
      [e, l] = chainEdge(d, other, "mk-miss", short(1 - p[k - 1]), 0.5, 0, k === i ? -1 : 1);
      edges.push(e); labels.push(l);
    });
    const boxes = [];
    [1, 2, 3].forEach((w) => boxes.push([`R${w}`, chainBox(`R${w}`, ["כולם חיים", `תור ${w}`], "mk-node", 84, w === me)]));
    boxes.push(["CATS", chainBox("CATS", ["חתולים", pct(res.cats)], "mk-cat", 84, false)]);
    Object.keys(CP).filter(isDuel).forEach((d) => { const [i, j, k] = d.split(",").map(Number); boxes.push([d, chainBox(d, [`${i} מול ${j}`, `תור ${k}`], "mk-node", 64, k === me)]); });
    [1, 2, 3].forEach((k) => boxes.push([`W${k}`, chainBox(`W${k}`, [`${k} מנצח`, pct(res.win[k - 1])], "mk-win", 96, k === me)]));
    let s = `<svg class="figure mk-chain" viewBox="0 0 480 418" role="img" aria-label="שרשרת מרקוב של הבחירה הנוכחית : הסיכויים הסופיים ${res.win.map(pct).join(", ")}, חתולים ${pct(res.cats)}">` +
      `<defs><marker id="wz-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="mk-head"/></marker></defs>`;
    s += edges.join("");
    boxes.forEach(([key, b]) => { s += used.has(key) ? b : `<g class="st-faded">${b}</g>`; });
    return s + labels.join("") + "</svg>";
  };

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
        `<p class="ex-title">ששת הסדרים מול היריבים האלה, כל אחד עם השרביט הטוב ביותר שלו; לחיצה על שורה בוחרת אותה</p>` +
        `<div class="wz-tablewrap" tabindex="0" role="region" aria-label="ששת הסדרים"></div>` +
        `<p class="ex-title">הסיכוי שלי לנצח לכל שרביט, בתור ובסדר שבחרתי; הקווים המקווקווים הם היריבים</p><div class="wz-chart"></div>` +
        `<span class="viz-legend"><span><i class="s1"></i>הסיכוי שלי</span><span><i class="s2"></i>השרביט שבחרתי</span><span><i class="s3"></i>השרביט הטוב ביותר בתור הזה</span></span>` +
        `<p class="ex-title">שרשרת מרקוב של הבחירה${NB}: על החצים ההסתברויות, ובמצבים הסופיים הסיכוי להגיע אליהם</p><div class="wz-chain"></div>` +
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
        let t = `<table class="wz-table"><thead><tr><th>ראשון</th><th>שני</th><th>שלישי</th><th>השרביט</th><th>אני</th><th>יריב א</th><th>יריב ב</th><th>חתולים</th><th></th></tr></thead><tbody>`;
        rows.forEach((o, i) => {
          const pp = wzPlace(o.me, o.wand, o.rivals), seq = o.order === "ab" ? ["א", "ב"] : ["ב", "א"];
          let q = 0;
          const cells = [0, 1, 2].map((k) => (k === o.me - 1 ? `<td class="wz-me">אני</td>` : `<td>${seq[q++]} ${ltr(pp[k])}</td>`));
          const ia = [0, 1, 2].filter((k) => k !== o.me - 1)[o.order === "ab" ? 0 : 1], ib = [0, 1, 2].filter((k) => k !== o.me - 1)[o.order === "ab" ? 1 : 0];
          const now = o.me === st.me && o.order === st.order, isBest = Math.abs(o.win[o.me - 1] - top) < 1e-12;
          t += `<tr data-i="${i}" class="${[now ? "is-now" : "", isBest ? "is-best" : ""].join(" ").trim()}">${cells.join("")}<td>${ltr(wandText(o.wand))}</td><td>${ltr(pct(o.win[o.me - 1]))}</td><td>${ltr(pct(o.win[ia]))}</td><td>${ltr(pct(o.win[ib]))}</td><td>${ltr(pct(o.cats))}</td>` +
            `<td><button type="button" class="md-button wz-pick" data-i="${i}">לבחור</button></td></tr>`;
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
      $(".wz-tablewrap").addEventListener("click", (e) => {
        const tr = e.target.closest("tr[data-i]");
        if (tr) pick(wzOrders(st.a, st.b)[Number(tr.dataset.i)]);
      });
      sync();
      draw();
    },
  });

  dvqExplorers.register({
    views: { wizards: wizardsView },
    help: {
      wizards: "בוחרים את שני היריבים, את התור שלי, את הסדר שלהם ואת השרביט : מתחת לכפתורים הסיכויים של כולם ושל החתולים. ״הבחירה הטובה ביותר״ עוברת על ששת הסדרים ועל כל השרביטים. הטבלה מראה את ששת הסדרים, הגרף את הסיכוי שלי לכל שרביט, ושרשרת מרקוב את המשחק עם הבחירות של כולם.",
    },
    models: { wzDuel, wzRound, wzChance, wzBest, wzOrders },
  });
})();
