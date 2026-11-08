// kinds: grayhw
//   grayhw                 0034        the pointer paths of an asynchronous FIFO of 16 entries (5-bit pointers), edge by edge in time order (wclk every 20 ticks, rclk every 30): the block diagram of the page with every register's value after the edge, the domain that ticked lit, a bit caught metastable marked; a table of every signal, a column per edge; buttons for the trap cases (a metastable bit that settles old, the binary pointer through the synchronizer, a Gray computed by XORs, the writer up to full)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";

  // --- the model, as tools/figures/q0034.py hw_trace -------------------------------------------
  const BITS = 5, SIZE = 32, ENTRIES = 16, FULL_FLIP = 3 << (BITS - 2), PW = 20, PR = 30;
  const DELAY = [9, 7, 5, 3, 1];             // bit i reaches the other domain DELAY[i] ticks after its edge
  const range = (a, b) => Array.from({ length: b - a }, (_, i) => a + i);
  const SCEN = {
    page: { mode: "gray", p0: 0, r0: 29, writes: [1, 2, 3], read_from: 1, reads: null, settle: "new", end: 230 },
    old: { mode: "gray", p0: 0, r0: 29, writes: [1, 2, 3], read_from: 1, reads: null, settle: "old", end: 230 },
    bin: { mode: "bin", p0: 7, r0: 24, writes: [1], read_from: 1, reads: null, settle: "new", end: 170 },
    comb: { mode: "comb", p0: 7, r0: 24, writes: [1], read_from: 1, reads: null, settle: "new", end: 170 },
    full: { mode: "gray", p0: 0, r0: 29, writes: range(1, 23), read_from: 11, reads: 1, settle: "new", end: 450 },
  };
  const gray = (b) => b ^ (b >> 1);
  const gray2bin = (g) => { let b = 0, acc = 0; for (let i = BITS - 1; i >= 0; i--) { acc ^= (g >> i) & 1; b |= acc << i; } return b; };
  const mod = (v) => ((v % SIZE) + SIZE) % SIZE;
  // the bits of a register as the other domain sees them: each bit's changes, in time
  const wire = (value) => {
    const hist = range(0, BITS).map((i) => [[-1e9, (value >> i) & 1]]);
    return {
      change(t, a, b) { for (let i = 0; i < BITS; i++) if (((a ^ b) >> i) & 1) hist[i].push([t + DELAY[i], (b >> i) & 1]); },
      at(t, inclusive) {
        let v = 0;
        hist.forEach((h, i) => { const ok = h.filter(([c]) => (inclusive ? c <= t : c < t)); v |= ok[ok.length - 1][1] << i; });
        return v;
      },
    };
  };
  // the first flop at edge t: the value it takes and the bits it caught metastable
  const sample = (w, mode, t, settle) => {
    let after = w.at(t, true), before = w.at(t, false);
    if (mode === "comb") { after = gray(after); before = gray(before); }
    return [settle === "new" ? after : before, after ^ before];
  };
  const edgesOf = (sc) => {
    const out = [];
    for (let k = 1; k <= Math.floor(sc.end / PW); k++) out.push([PW * k, "w", k]);
    for (let k = 0; k <= Math.floor((sc.end - sc.r0) / PR); k++) out.push([PR * k + sc.r0, "r", k + 1]);
    return out.sort((a, b) => a[0] - b[0]);
  };
  const ghTrace = (name = "page") => {
    const sc = SCEN[name], { mode, settle, p0 } = sc;
    const far = mode === "bin" ? (b) => b : gray, asBin = mode === "bin" ? (v) => v : gray2bin;
    const s = { wbin: p0, wgray: gray(p0), wfull: 0, wq1: far(p0), wq2: far(p0), rbin: p0, rgray: gray(p0), rempty: 1, rq1: far(p0), rq2: far(p0) };
    const ww = wire(mode === "gray" ? s.wgray : p0), rw = wire(mode === "gray" ? s.rgray : p0);
    let reads = 0;
    const out = [];
    edgesOf(sc).forEach(([t, clk, k]) => {
      const rec = { clk, t, k };
      if (clk === "w") {
        const want = sc.writes.includes(k), inc = want && !s.wfull ? 1 : 0;
        const wbin = (s.wbin + inc) % SIZE, wg = gray(wbin);
        const cmp = mode === "bin" ? wbin : wg, farR = s.wq2 ^ (mode === "bin" ? ENTRIES : FULL_FLIP);
        const [q1, meta] = sample(rw, mode, t, settle);
        ww.change(t, mode === "gray" ? s.wgray : s.wbin, mode === "gray" ? wg : wbin);
        Object.assign(s, { wbin, wgray: wg, wfull: cmp === farR ? 1 : 0, wq2: s.wq1, wq1: q1 });
        Object.assign(rec, { want: want ? 1 : 0, inc, meta, cmp: farR, seen: mod(s.wbin - asBin(s.wq2)), true: mod(s.wbin - s.rbin) });
      } else {
        const inc = !s.rempty && k >= sc.read_from && (sc.reads == null || reads < sc.reads) ? 1 : 0;
        reads += inc;
        const rbin = (s.rbin + inc) % SIZE, rg = gray(rbin);
        const cmp = mode === "bin" ? rbin : rg;
        const [q1, meta] = sample(ww, mode, t, settle);
        rw.change(t, mode === "gray" ? s.rgray : s.rbin, mode === "gray" ? rg : rbin);
        const farW = s.rq2;
        Object.assign(s, { rbin, rgray: rg, rempty: cmp === farW ? 1 : 0, rq2: s.rq1, rq1: q1 });
        Object.assign(rec, { want: 0, inc, meta, cmp: farW, seen: mod(asBin(s.rq2) - s.rbin), true: mod(s.wbin - s.rbin) });
      }
      Object.assign(rec, s);
      out.push(rec);
    });
    return out;
  };

  // --- the block diagram, as tools/figures/q0034.py DP_BLOCKS and DP_WIRES -----------------------
  const BW = 76, BH = 44;
  const BLOCKS = [
    ["wbin", 20, 30, "reg", "wbin", "w"], ["wb2g", 122, 30, "mux", "bin2gray", "w"], ["wgray", 224, 30, "reg", "wgray", "w"],
    ["wq1", 20, 110, "sync", "wq1_rgray", "w"], ["wq2", 122, 110, "sync", "wq2_rgray", "w"], ["full", 224, 110, "stage", "full ?", "w"],
    ["wfull", 326, 110, "out", "wfull", "w"], ["rempty", 20, 206, "out", "rempty", "r"], ["empty", 122, 206, "stage", "empty ?", "r"],
    ["rq2", 224, 206, "sync", "rq2_wgray", "r"], ["rq1", 326, 206, "sync", "rq1_wgray", "r"], ["rgray", 20, 286, "reg", "rgray", "r"],
    ["rb2g", 122, 286, "mux", "bin2gray", "r"], ["rbin", 224, 286, "reg", "rbin", "r"],
  ];
  const WIRES = [
    ["winc", [[58, 8], [58, 30]], "winc", 64, 18, "start", "w"],
    ["wnext", [[96, 52], [122, 52]], "", 0, 0, "", "w"],
    ["wgnext", [[198, 52], [224, 52]], "", 0, 0, "", "w"],
    ["wgfull", [[160, 74], [160, 92], [262, 92], [262, 110]], "wgray_next", 211, 88, "middle", "w"],
    ["wcross", [[300, 52], [412, 52], [412, 228], [402, 228]], "wgray", 406, 96, "end", "r"],
    ["wq12", [[96, 132], [122, 132]], "", 0, 0, "", "w"],
    ["wq2full", [[198, 132], [224, 132]], "", 0, 0, "", "w"],
    ["fullreg", [[300, 132], [326, 132]], "", 0, 0, "", "w"],
    ["rq12", [[326, 228], [300, 228]], "", 0, 0, "", "r"],
    ["rq2empty", [[224, 228], [198, 228]], "", 0, 0, "", "r"],
    ["emptyreg", [[122, 228], [96, 228]], "", 0, 0, "", "r"],
    ["rcross", [[20, 308], [8, 308], [8, 132], [20, 132]], "rgray", 14, 270, "start", "w"],
    ["rnext", [[224, 308], [198, 308]], "", 0, 0, "", "r"],
    ["rgnext", [[122, 308], [96, 308]], "", 0, 0, "", "r"],
    ["rgempty", [[160, 286], [160, 250]], "rgray_next", 166, 272, "start", "r"],
    ["rinc", [[262, 348], [262, 330]], "rinc", 268, 344, "start", "r"],
  ];
  const REGS = ["wbin", "wgray", "wq1", "wq2", "wfull", "rbin", "rgray", "rq1", "rq2", "rempty"];
  const bin5 = (v) => v.toString(2).padStart(BITS, "0");
  // a 5-bit value with the bits caught metastable in their own tspan
  const bitsMarked = (v, meta) => [...bin5(v)].map((b, j) => ((meta >> (BITS - 1 - j)) & 1 ? `<tspan class="gh-xbit">${b}</tspan>` : b)).join("");
  // the names the trap modes give the synchronizers: the binary crosses in mode bin, the XORs' output in mode comb
  const titles = (mode) => (mode === "bin"
    ? { wq1: "wq1_rbin", wq2: "wq2_rbin", rq1: "rq1_wbin", rq2: "rq2_wbin", wcross: "wbin", rcross: "rbin" }
    : mode === "comb" ? { wcross: "gray(wbin)", rcross: "gray(rbin)" } : {});
  // the second line of each block after edge c (its predecessor p for what changed)
  const values = (c, mode) => {
    if (!c) return {};
    const w = c.clk === "w", r = !w;
    const far = (v, m) => (mode === "bin" ? `${v}` : bitsMarked(v, m));
    return {
      wbin: `${bin5(c.wbin)} = ${c.wbin}`, wb2g: w ? `→ ${bin5(gray(c.wbin))}` : "", wgray: bin5(c.wgray),
      wq1: far(c.wq1, w ? c.meta : 0), wq2: far(c.wq2, 0), full: w ? `= ${c.wfull}` : "", wfull: `${c.wfull}`,
      rbin: `${bin5(c.rbin)} = ${c.rbin}`, rb2g: r ? `→ ${bin5(gray(c.rbin))}` : "", rgray: bin5(c.rgray),
      rq1: far(c.rq1, r ? c.meta : 0), rq2: far(c.rq2, 0), empty: r ? `= ${c.rempty}` : "", rempty: `${c.rempty}`,
    };
  };
  // the diagram after edge c (null: before the first edge, the page's names); p the record before
  const ghDiagram = (c, p = null, mode = "gray") => {
    const val = values(c, mode), tl = titles(mode);
    const dom = c ? c.clk : null;
    let g = `<svg class="gh-fig gh-dp gh-live-dp" viewBox="0 0 420 352" direction="ltr" role="img" aria-label="תרשים המלבנים של מצביעי ה-FIFO עם הערכים אחרי השפה הזאת">` +
      '<defs><marker id="gh-hd" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="gh-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>' +
      '<path class="gh-cdc" d="M0,180 L420,180"/>' +
      `<text class="gh-dom${dom === "w" ? " is-on" : ""}" x="210" y="173" text-anchor="middle">wclk domain</text>` +
      `<text class="gh-dom${dom === "r" ? " is-on" : ""}" x="210" y="196" text-anchor="middle">rclk domain</text>`;
    BLOCKS.forEach(([id, x, y, cls, title, d]) => {
      const lit = dom === d, chg = c && p && REGS.includes(id) && c[id] !== p[id];
      const meta = c && c.meta && ((id === "rq1" && dom === "r") || (id === "wq1" && dom === "w"));
      g += `<g class="gh-blk gh-${cls}${lit ? " is-on" : ""}${chg ? " is-chg" : ""}${meta ? " is-meta" : ""}" data-b="${id}"><rect x="${x}" y="${y}" width="${BW}" height="${BH}" rx="5"/>` +
        `<text x="${x + BW / 2}" y="${y + BH / 2 - 3}" text-anchor="middle">${tl[id] || title}</text>` +
        `<text class="gh-val" x="${x + BW / 2}" y="${y + BH / 2 + 13}" text-anchor="middle">${val[id] ?? ""}</text></g>`;
    });
    WIRES.forEach(([id, pts, lab, lx, ly, anchor, d]) => {
      g += `<path class="gh-wire${dom === d ? " is-on" : ""}" d="M${pts.map(([a, b]) => `${a},${b}`).join(" L")}" marker-end="url(#gh-hd)"/>`;
      if (lab) g += `<text class="gh-wlab" x="${lx}" y="${ly}" text-anchor="${anchor}">${id === "winc" && c ? `winc = ${c.clk === "w" ? c.inc : 0}` : id === "rinc" && c ? `rinc = ${c.clk === "r" ? c.inc : 0}` : tl[id] || lab}</text>`;
    });
    return g + "</svg>";
  };

  // --- the box -----------------------------------------------------------------------------------

  const counts = (c, mode) => {
    const asBin = mode === "bin" ? (v) => v : gray2bin;
    return { r: mod(asBin(c.rq2) - c.rbin), w: mod(c.wbin - asBin(c.wq2)), t: mod(c.wbin - c.rbin) };
  };
  const ROWS = [
    ["clk", (c) => c.clk + "clk"], ["t", (c) => c.t],
    ["winc", (c) => (c.clk === "w" ? c.inc : "")], ["wbin", (c) => c.wbin], ["wgray", (c) => bin5(c.wgray)],
    ["wq1", (c, m) => (m === "bin" ? c.wq1 : bin5(c.wq1))], ["wq2", (c, m) => (m === "bin" ? c.wq2 : bin5(c.wq2))], ["wfull", (c) => c.wfull],
    ["rinc", (c) => (c.clk === "r" ? c.inc : "")], ["rbin", (c) => c.rbin], ["rgray", (c) => bin5(c.rgray)],
    ["rq1", (c, m) => (m === "bin" ? c.rq1 : bin5(c.rq1))], ["rq2", (c, m) => (m === "bin" ? c.rq2 : bin5(c.rq2))], ["rempty", (c) => c.rempty],
    ["words", (c, m) => counts(c, m).t], ["r sees", (c, m) => counts(c, m).r], ["w sees", (c, m) => counts(c, m).w],
  ];
  const FLAGS = new Set(["winc", "wfull", "rinc", "rempty"]);
  const bad = (name, c, m) => {
    if (name !== "r sees" && name !== "w sees") return false;
    const n = counts(c, m);
    return name === "r sees" ? n.r > n.t : n.w < n.t || n.w > ENTRIES;
  };
  const table = (tr, k, mode) => {
    let t = `<table class="gh-wave"><thead><tr><th scope="col">שפה</th>${tr.map((_, i) => `<th scope="col"${i === k - 1 ? ' class="is-now"' : ""}>${i + 1}</th>`).join("")}</tr></thead><tbody>`;
    ROWS.forEach(([name, f]) => {
      t += `<tr><th scope="row">${name}</th>` + tr.map((c, i) => {
        const shown = i < k, v = shown ? f(c, mode) : "";
        const meta = shown && c.meta && ((name === "rq1" && c.clk === "r") || (name === "wq1" && c.clk === "w"));
        const cls = [i === k - 1 ? "is-now" : "", shown ? "" : "is-fut", FLAGS.has(name) && v === 1 ? "is-hi" : "",
          shown && bad(name, c, mode) ? "is-bad" : "", meta ? "is-meta" : "", shown && name === "clk" ? `gh-${c.clk}` : ""].filter(Boolean).join(" ");
        return `<td${cls ? ` class="${cls}"` : ""}>${v}</td>`;
      }).join("") + "</tr>";
    });
    return t + "</tbody></table>";
  };

  const TRAPS = [["old", "הביט נרגע לישן"], ["bin", "מצביע בינארי בסנכרן"], ["comb", "Gray צירופי"], ["full", "כתיבה עד full"]];
  const MODE_TEXT = {
    gray: `הסנכרנים מעבירים את ${ltr("wgray")} ואת ${ltr("rgray")}, שני רגיסטרים`,
    bin: `מלכודת${NB}: הסנכרנים מעבירים את המצביעים הבינאריים ${ltr("wbin")} ו-${ltr("rbin")}`,
    comb: `מלכודת${NB}: הסנכרנים מעבירים את ה-Gray שה-XOR מחשב מ-${ltr("wbin")} ומ-${ltr("rbin")}, בלי רגיסטר`,
  };
  const bitList = (m) => range(0, BITS).filter((i) => (m >> i) & 1);

  const grayhwView = () => ({
    mount(box) {
      const st = { name: "page", k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<button type="button" class="md-button ex-reset">חזרה לדוגמה של העמוד</button>` +
        TRAPS.map(([n, t]) => `<button type="button" class="md-button ex-preset gh-trap" data-s="${n}">מקרה מלכודת${NB}: ${t}</button>`).join("") + `</div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">השפה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">השפה הבאה</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 300) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary gh-sum" aria-live="polite"></p>` +
        `<div class="gh-dpwrap"></div>` +
        `<div class="gh-wavewrap" dir="ltr" tabindex="0" role="region" aria-label="כל האותות, עמודה לכל שפה"></div>` +
        `<p class="gh-note" aria-live="polite"></p>` +
        `<span class="viz-legend"><span><i class="gh-key-on"></i>הדומיין של השפה הזאת</span><span><i class="gh-key-chg"></i>רגיסטר שהשתנה</span>` +
        `<span><i class="gh-key-meta"></i>ביט שנתפס מטא-יציב</span><span><i class="gh-key-bad"></i>ספירה שגויה</span></span>`;
      const $ = (sel) => box.querySelector(sel);
      const trace = () => ghTrace(st.name);

      const draw = () => {
        const sc = SCEN[st.name], tr = trace(), T = tr.length;
        st.k = Math.max(0, Math.min(st.k, T));
        $(".ex-pos").textContent = `שפה ${st.k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === T;
        box.querySelectorAll(".gh-trap").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.s === st.name)));
        const c = st.k ? tr[st.k - 1] : null, p = st.k > 1 ? tr[st.k - 2] : null;
        $(".gh-dpwrap").innerHTML = ghDiagram(c, p || (c ? { ...c, ...initial(sc) } : null), sc.mode);
        const wv = $(".gh-wavewrap");
        wv.innerHTML = table(tr, st.k, sc.mode);
        const cur = wv.querySelector("th.is-now");
        if (cur) wv.scrollLeft = Math.max(0, cur.offsetLeft - wv.clientWidth / 2);
        $(".gh-sum").innerHTML = `${MODE_TEXT[sc.mode]}. ‏${ltr("wclk")} כל ${ltr(PW)} טיקים, ‏${ltr("rclk")} כל ${ltr(PR)}, ` +
          `וכל ביט מגיע לצד השני ${ltr("9, 7, 5, 3, 1")} טיקים אחרי השפה (ביט 0 עד ביט 4).`;
        $(".gh-note").innerHTML = note(c, p || (c ? { ...c, ...initial(sc) } : null), sc);
        const res = result(tr, sc);
        if (res && st.k >= res.at) answer(box, res.text, `.gh-dpwrap [data-b="${res.block}"] rect`);
        else answer(box, null);
      };
      const initial = (sc) => {
        const far = sc.mode === "bin" ? sc.p0 : gray(sc.p0);
        return { wbin: sc.p0, wgray: gray(sc.p0), wfull: 0, wq1: far, wq2: far, rbin: sc.p0, rgray: gray(sc.p0), rempty: 1, rq1: far, rq2: far };
      };
      const fmt = (v, mode) => (mode === "bin" ? String(v) : bin5(v));
      const note = (c, p, sc) => {
        if (!c) return `לפני השפה הראשונה${NB}: ה-FIFO ריק, ושני המצביעים ${ltr(sc.p0)}. ‏"השפה הבאה" מתקדמת לשפה הבאה בזמן, של ${ltr("wclk")} או של ${ltr("rclk")}.`;
        const T = ltr(`t = ${c.t}`), m = sc.mode, n = counts(c, m);
        const metaTxt = c.meta ? ` ביט ${ltr(bitList(c.meta).join(", "))} השתנה בדיוק בשפה ונתפס מטא-יציב, ונרגע ל${sc.settle === "new" ? "חדש" : "ישן"}.` : "";
        if (c.clk === "w") {
          let s = `שפה של ${ltr("wclk")} ב-${T}${NB}: `;
          if (c.inc) {
            const ch = bitList(gray(c.wbin) ^ gray(p.wbin)).map((i) => `ביט ${ltr(i)} מגיע לצד השני ב-${ltr(`t = ${c.t + DELAY[i]}`)}`);
            s += `‏${ltr("winc = 1")}, ‏${ltr(`wbin ${p.wbin} → ${c.wbin}`)} ו-${ltr(`wgray ${bin5(p.wgray)} → ${bin5(c.wgray)}`)}${m === "gray" ? ` (${ch.join(", ")})` : ""}.`;
          } else s += c.want ? `הכותב רוצה לכתוב, אבל ${ltr("wfull = 1")}, והכתיבה מחכה.` : "אין כתיבה.";
          s += ` ‏${ltr(`${titles(m).wq1 || "wq1_rgray"} ← ${fmt(c.wq1, m)}`)}.${metaTxt}`;
          if (c.wfull !== p.wfull) s += ` ‏${ltr(`wfull ← ${c.wfull}`)}${c.wfull ? `, ובפנים ${ltr(n.t)} מילים` : `${NB}: הקריאה הגיעה לכותב`}.`;
          if (n.w < n.t || n.w > ENTRIES) s += ` הכותב רואה ${ltr(n.w)} מילים, ובפנים ${ltr(n.t)} ✗`;
          return s;
        }
        let s = `שפה של ${ltr("rclk")} ב-${T}${NB}: `;
        s += c.inc ? `‏${ltr("rinc = 1")}, קריאת מילה, ‏${ltr(`rbin ${p.rbin} → ${c.rbin}`)}.` : p.rempty ? `‏${ltr("rempty = 1")}, אין קריאה.` : "אין קריאה.";
        s += ` ‏${ltr(`${titles(m).rq1 || "rq1_wgray"} ← ${fmt(c.rq1, m)}`)} ו-${ltr(`${titles(m).rq2 || "rq2_wgray"} ← ${fmt(c.rq2, m)}`)}.${metaTxt}`;
        if (c.rempty !== p.rempty) s += ` ‏${ltr(`rempty ← ${c.rempty}`)}${c.rempty ? "" : `${NB}: הכתיבה הגיעה לקורא`}.`;
        if (n.r > n.t) s += ` הקורא רואה ${ltr(n.r)} מילים, ובפנים ${ltr(n.t)} ✗`;
        return s;
      };
      // the scenario's point, once its edge is reached: the latency, the wrong count, full and back
      const result = (tr, sc) => {
        if (sc.mode !== "gray") {
          const i = tr.findIndex((c) => c.clk === "r" && counts(c, sc.mode).r > counts(c, sc.mode).t);
          if (i < 0) return null;
          const c = tr[i], n = counts(c, sc.mode);
          return { at: i + 1, block: "rq2", text: `בשפה ${ltr(i + 1)} ‏${ltr(`${titles(sc.mode).rq2 || "rq2_wgray"} = ${sc.mode === "bin" ? c.rq2 : `${bin5(c.rq2)} = ${gray2bin(c.rq2)}`}`)}${NB}: הקורא רואה ${ltr(n.r)} מילים, ובפנים ${ltr(n.t)} ✗` };
        }
        if (sc.reads != null) {
          const up = tr.findIndex((c) => c.clk === "w" && c.wfull);
          const down = tr.findIndex((c, j) => j > up && c.clk === "w" && !c.wfull);
          const rd = tr.find((c) => c.clk === "r" && c.inc);
          if (up < 0 || down < 0 || !rd) return null;
          const arrive = rd.t + DELAY[0];
          return { at: down + 1, block: "wfull", text: `‏${ltr("wfull")} עולה ב-${ltr(`t = ${tr[up].t}`)} ויורד ב-${ltr(`t = ${tr[down].t}`)}, ‏${ltr(((tr[down].t - arrive) / PW).toFixed(1))} מחזורי ${ltr("wclk")} אחרי שהקריאה הגיעה לצד הכותב.` };
        }
        const w = tr.find((c) => c.clk === "w" && c.inc), arrive = w.t + DELAY[0];
        const i = tr.findIndex((c) => c.clk === "r" && !c.rempty);
        return { at: i + 1, block: "rempty", text: `‏${ltr("rempty")} יורד ב-${ltr(`t = ${tr[i].t}`)}, ‏${ltr((tr[i].t - arrive) / PR)} מחזורי ${ltr("rclk")} אחרי שהביט של המילה הראשונה הגיע (${ltr(`t = ${arrive}`)}).` };
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= trace().length, restart: () => { st.k = 0; draw(); } });
      const set = (name) => { stop(); Object.assign(st, { name, k: 0 }); draw(); };
      box.querySelectorAll(".gh-trap").forEach((b) => b.addEventListener("click", () => set(b.dataset.s)));
      $(".ex-reset").addEventListener("click", () => set("page"));
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = trace().length; draw(); });
      // the link and the remembered state: "page_7", the scenario and the edge
      box.dvqExtra = {
        get: () => `${st.name}_${st.k}`,
        set: (text) => {
          const m = /^([a-z]+)_(\d{1,3})$/.exec(text);
          if (!m || !SCEN[m[1]]) return false;
          stop();
          Object.assign(st, { name: m[1], k: Number(m[2]) });
          draw();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { grayhw: grayhwView },
    help: {
      grayhw: "ה-FIFO של 16 כניסות, שפה אחרי שפה לפי הזמן: wclk כל 20 טיקים ו-rclk כל 30. התרשים מראה את הערך של כל רגיסטר אחרי השפה, והדומיין שתקתק מודגש. ביט שמשתנה בדיוק בשפה נתפס מטא-יציב ומסומן. בטבלה כל האותות, עמודה לכל שפה, וגם כמה מילים כל צד חושב שיש. כפתורי המלכודת טוענים את הטעויות: מצביע בינארי בסנכרן, Gray צירופי, וכתיבה עד full.".replace(/:/g, `${NB}:`),
    },
    cols: { grayhw: { main: ".gh-dpwrap", side: ".gh-wavewrap, .gh-note", w: "minmax(0, 1.2fr)" } },
    models: { ghTrace, ghDiagram },
  });
})();
