// kinds: tagpool
//   tagpool                0062        transactions as bars over time (typed as "0-30 5-10", or "R0-10 W20-30" for reads and writes) and the sweep over their events step by step: the open count after each event as a step line under the bars, the maximum so far, and with two pools the counters of the reads, the writes and the shared pool
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, explain, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMAX = 12, TMAX = 99;
  // the solution's steps, as chips of the explanation panel, and a variable's change
  const STEPS = {
    one: ["שני אירועים לטרנזקציה", "מיון לפי זמן, תשובה לפני שליחה", "סריקה : המונה והשיא", "התשובה : השיא"],
    two: ["שני אירועים לטרנזקציה, עם הסוג", "מיון לפי זמן, תשובה לפני שליחה", "סריקה : מונה לכל סוג, והסכום", "התשובה : שלושת השיאים"],
  };
  const V = (name, before, after) => ltr(before === after ? `${name} = ${after}` : `${name} : ${before} → ${after}`);

  // The sorted events of the transactions (a response before a send at one time, then the
  // reads before the writes, then the list order) with the counters after each, as
  // tools/figures/q0062.py sweep(): the open reads, the open writes, their total and the
  // maxima so far. A transaction is [send, response, kind], the kind "R" or "W".
  const tpSweep = (txns) => {
    const ev = [];
    txns.forEach(([s, e, kind], i) => { ev.push({ t: s, d: 1, kind: kind || "R", i }); ev.push({ t: e, d: -1, kind: kind || "R", i }); });
    ev.sort((a, b) => a.t - b.t || a.d - b.d || (a.kind < b.kind ? -1 : a.kind > b.kind ? 1 : 0) || a.i - b.i);
    const open = { R: 0, W: 0 }, best = { R: 0, W: 0, all: 0 };
    return ev.map((x) => {
      open[x.kind] += x.d;
      best[x.kind] = Math.max(best[x.kind], open[x.kind]);
      best.all = Math.max(best.all, open.R + open.W);
      return { ...x, open: { ...open }, total: open.R + open.W, best: { ...best } };
    });
  };
  const tpPools = (txns) => { const r = tpSweep(txns); const b = r.length ? r[r.length - 1].best : { R: 0, W: 0, all: 0 }; return [b.R, b.W, b.all]; };

  const parse = (text) => {
    const toks = String(text).trim().toUpperCase().split(/[\s,;]+/).filter(Boolean);
    if (!toks.length || toks.length > NMAX) return null;
    const out = [];
    for (const tok of toks) {
      const m = /^([RW]?)(\d+)-(\d+)$/.exec(tok);
      if (!m) return null;
      const s = Number(m[2]), e = Number(m[3]);
      if (!(s < e) || e > TMAX) return null;
      out.push([s, e, m[1] || "R"]);
    }
    return out;
  };
  const text = (txns, two) => txns.map(([s, e, k]) => `${two ? k : ""}${s}-${e}`).join(" ");

  // The timeline: a bar per transaction (the list order, top to bottom), the time axis, and
  // under it the open count as a step line drawn up to the current event, the maximum so far
  // dashed, and a cursor at the event's time. The scale of the count comes from the final
  // peak, so the figure keeps its size through the steps.
  const svg = (txns, rows, s, two, peakRows) => {
    const T = Math.max(...txns.map((x) => x[1]));
    const L = 64, R = 16, W = 640, bar = 16, gap = 8, top = 14;
    const x = (t) => L + ((W - L - R) * t) / T;
    const peak = rows.length ? rows[rows.length - 1].best.all : 0;
    const yAxis = top + txns.length * (bar + gap) + 6, ch = 22 * Math.max(peak, 1), cy0 = yAxis + 42, H = cy0 + ch + 30;
    const yc = (c) => cy0 + ch - (ch * c) / Math.max(peak, 1);
    const cur = s ? rows[s - 1] : null;
    const openNow = new Set(), done = new Set();
    rows.slice(0, s).forEach((r) => { if (r.d > 0) openNow.add(r.i); else { openNow.delete(r.i); done.add(r.i); } });
    let out = `<svg class="figure tp-fig tp-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="ציר הזמן של ${txns.length} טרנזקציות, ומתחתיו כמה פתוחות בכל רגע">`;
    const step = T <= 40 ? 5 : T <= 100 ? 10 : 20;
    for (let t = 0; t <= T; t += step) out += `<line class="grid" x1="${x(t)}" x2="${x(t)}" y1="${top - 4}" y2="${cy0 + ch}"/><text class="tick" x="${x(t)}" y="${yAxis + 14}" text-anchor="middle">${t}</text>`;
    txns.forEach(([a, e, kind], i) => {
      const y = top + i * (bar + gap), name = two ? `${kind}${i + 1}` : `T${i + 1}`;
      const cls = `${two ? ` is-${kind.toLowerCase()}` : ""}${openNow.has(i) ? " is-open" : done.has(i) ? " is-done" : ""}${peakRows.has(i) ? " is-peak" : ""}${cur && cur.i === i ? " is-now" : ""}`;
      out += `<text class="tp-name" x="${L - 8}" y="${y + bar - 3}" text-anchor="end">${name}</text>` +
        `<rect class="tp-bar${cls}" x="${x(a)}" y="${y}" width="${x(e) - x(a)}" height="${bar}" rx="3"><title>${name}: ${a}–${e}</title></rect>`;
    });
    out += `<line class="axis" x1="${L}" x2="${W - R}" y1="${yAxis}" y2="${yAxis}"/>`;
    for (let c = 0; c <= peak; c++) out += `<text class="tick" x="${L - 8}" y="${yc(c) + 4}" text-anchor="end">${c}</text>`;
    const bestNow = cur ? cur.best.all : 0;
    if (cur) out += `<line class="tp-max" x1="${L}" x2="${W - R}" y1="${yc(bestNow)}" y2="${yc(bestNow)}"/><text class="legend" x="${W - R}" y="${yc(bestNow) - 7}" text-anchor="end">max = ${bestNow}</text>`;
    let d = `M${L},${yc(0)}`;
    rows.slice(0, s).forEach((r) => { d += ` H${x(r.t)} V${yc(r.total)}`; });
    if (cur) d += ` H${x(cur.t)}`;
    out += `<path class="tp-count" d="${d}"/>`;
    if (cur) out += `<line class="tp-cursor" x1="${x(cur.t)}" x2="${x(cur.t)}" y1="${top - 4}" y2="${cy0 + ch}"/>`;
    out += `<text class="tp-name" x="${L - 8}" y="${cy0 - 10}" text-anchor="end">open</text>`;
    return out + "</svg>";
  };

  const tagpoolView = () => ({
    mount(box) {
      const d0 = { two: box.dataset.mode === "two", txns: parse(box.dataset.txns || "0-30 5-10 15-20") || [[0, 30, "R"], [5, 10, "R"], [15, 20, "R"]] };
      const st = { two: d0.two, txns: d0.txns.map((t) => t.slice()), s: 0, n: 6 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המאגר <select class="tp-mode" aria-label="מאגר אחד, או מאגר לקריאות ומאגר לכתיבות"><option value="one">אחד לכולן (סעיף א)</option><option value="two">קריאות וכתיבות (סעיף ב)</option></select></label>` +
        `<label><span>הטרנזקציות</span><input type="text" class="ex-num tp-txns" dir="ltr" spellcheck="false" aria-label="הטרנזקציות, שליחה-תשובה מופרדות ברווח, עם R או W לפני כל אחת בשני מאגרים"></label>` +
        `<label>בהגרלה <select class="tp-n" aria-label="כמה טרנזקציות להגריל">${[4, 6, 8, 12].map((v) => `<option value="${v}"${v === 6 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button tp-rand">הגרלה</button><span class="tp-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err tp-err" role="status"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">האירוע הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">האירוע הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 700, 300) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary tp-sum" aria-live="polite"></p>` +
        `<div class="tp-wrap" data-fig-strip></div>` +
        `<span class="viz-legend"><span class="tp-one"><i class="tp-key-bar"></i>טרנזקציה</span><span class="tp-two"><i class="tp-key-r"></i>קריאה</span><span class="tp-two"><i class="tp-key-w"></i>כתיבה</span>` +
        `<span><i class="tp-key-open"></i>פתוחה עכשיו</span><span><i class="tp-key-count"></i>כמה פתוחות</span><span><i class="tp-key-max"></i>המקסימום עד עכשיו</span><span><i class="tp-key-cursor"></i>האירוע הנוכחי</span></span>` +
        `<p class="tp-note"></p>`;
      const show = explain(box, "הסבר : השלבים של הפתרון והקוד");
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const rows = () => tpSweep(st.txns);
      const draw = () => {
        const R = rows(), N = R.length, two = st.two;
        st.s = Math.min(Math.max(st.s, 0), N);
        const cur = st.s ? R[st.s - 1] : null, done = st.s === N, last = R[N - 1];
        $(".tp-mode").value = two ? "two" : "one"; $(".tp-txns").value = text(st.txns, two);
        box.classList.toggle("tp-is-two", two);
        $(".ex-pos").textContent = `אירוע ${st.s} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        // the transactions open at the first moment the shared count reaches its peak
        const peakRows = new Set();
        if (done) {
          const k = R.findIndex((r) => r.total === last.best.all), open = new Set();
          R.slice(0, k + 1).forEach((r) => { if (r.d > 0) open.add(r.i); else open.delete(r.i); });
          open.forEach((i) => peakRows.add(i));
        }
        $(".tp-wrap").innerHTML = svg(st.txns, R, st.s, two, peakRows);
        const nR = st.txns.filter((t) => t[2] === "R").length, nW = st.txns.length - nR;
        $(".tp-sum").innerHTML = `${ltr(st.txns.length)} טרנזקציות${two ? ` (${ltr(nR)} קריאות, ${ltr(nW)} כתיבות)` : ""}, ${ltr(N)} אירועים. ` +
          (cur ? `פתוחות עכשיו${NB}: <b>${ltr(cur.total)}</b>${two ? ` (קריאות ${ltr(cur.open.R)}, כתיבות ${ltr(cur.open.W)})` : ""}. המקסימום עד עכשיו${NB}: ${ltr(cur.best.all)}${two ? `, ולכל מאגר לבד ${ltr(cur.best.R)} ו-${ltr(cur.best.W)}` : ""}.`
            : `לוחצים על "האירוע הבא"${NB}: האירועים עוברים לפי הזמן, תשובה לפני שליחה באותו רגע.`);
        $(".tp-note").innerHTML = !cur ? "" :
          `${ltr(`t = ${cur.t}`)}${NB}: ${cur.d > 0 ? "שליחה" : "תשובה"} של ${ltr(`${two ? cur.kind : "T"}${cur.i + 1}`)} (${ltr(`${st.txns[cur.i][0]}–${st.txns[cur.i][1]}`)}), המונה ${cur.d > 0 ? "עולה" : "יורד"} ל-${ltr(cur.total)}.` +
          (cur.total === cur.best.all && cur.d > 0 && (st.s === 1 || R[st.s - 2].best.all < cur.best.all) ? ` <b>שיא חדש${NB}: ${ltr(cur.total)} ✓</b>` : "");
        // the explanation panel: the steps of the moment, the lines they ran, the variables
        const prev = st.s > 1 ? R[st.s - 2] : null;
        let lit, lines, vars;
        if (!cur) {
          lit = [1, 2];
          lines = two ? { py: [4, 5, 6], sv: [6, 7, 8, 9, 10, 11, 12] } : { py: [4, 5], sv: [4, 5, 6, 7, 8, 9] };
          vars = `${ltr(N)} אירועים ממוינים, ${ltr(two ? "open_r = open_w = 0" : "open_now = 0, best = 0")}`;
        } else {
          lit = [3, ...(done ? [4] : [])];
          lines = two ? { py: [7, 8, 9, 10, ...(done ? [11] : [])], sv: [13, 14, 15, 16, 17, 18] } : { py: [6, 7, 8, ...(done ? [9] : [])], sv: [10, 11, 12, ...(done ? [14] : [])] };
          const d = ltr(`d = ${cur.d > 0 ? "+1" : "−1"}`);
          vars = two ? [ltr(`t = ${cur.t}`), d, ltr(cur.kind === "R" ? "read" : "write"), V("open_r", prev ? prev.open.R : 0, cur.open.R), V("open_w", prev ? prev.open.W : 0, cur.open.W),
            ltr(`reads = ${cur.best.R}`), ltr(`writes = ${cur.best.W}`), V("shared", prev ? prev.best.all : 0, cur.best.all)].join(" · ")
            : [ltr(`t = ${cur.t}`), d, V("open_now", prev ? prev.total : 0, cur.total), V("best", prev ? prev.best.all : 0, cur.best.all)].join(" · ");
        }
        show({ code: two ? "pools" : "tags_needed", steps: STEPS[two ? "two" : "one"], lit, lines, vars });
        if (done) {
          const b = last.best;
          answer(box, two ? `קריאות לבד ${ltr(b.R)}, כתיבות לבד ${ltr(b.W)}, יחד ${ltr(b.R + b.W)} tags בשני מאגרים. מאגר משותף${NB}: ${ltr(b.all)} tags, ${b.R + b.W > b.all ? `חיסכון של ${ltr(b.R + b.W - b.all)}` : "בלי חיסכון, כי שני השיאים נופלים יחד"}.`
            : `צריך ${ltr(b.all)} tags${NB}: ברגע ${ltr(R[R.findIndex((r) => r.total === b.all)].t)} ${ltr(b.all)} טרנזקציות פתוחות יחד.`, ".tp-bar.is-peak");
        } else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= rows().length, restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; $(".tp-err").textContent = ""; draw(); };
      $(".tp-mode").addEventListener("change", () => { st.two = $(".tp-mode").value === "two"; restart(); });
      $(".tp-txns").addEventListener("change", () => {
        const v = parse($(".tp-txns").value);
        if (!v) { $(".tp-err").textContent = `הטרנזקציות${NB}: 1 עד ${NMAX} זוגות שליחה-תשובה, זמנים עד ${TMAX}, השליחה לפני התשובה`; return; }
        st.txns = v; restart();
      });
      $(".tp-txns").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".tp-txns").blur(); });
      $(".tp-n").addEventListener("change", () => { st.n = Number($(".tp-n").value); });
      const seed = seedControls(box, $(".tp-anchor"), (rng) => {
        st.txns = Array.from({ length: st.n }, () => { const s = Math.floor(rng() * 36); return [s, s + 3 + Math.floor(rng() * 12), st.two && rng() < 0.5 ? "W" : "R"]; });
        restart();
      }, { fresh: false });
      $(".tp-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = rows().length; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, { two: d0.two, txns: d0.txns.map((t) => t.slice()), n: 6 }); $(".tp-n").value = "6"; restart(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { tagpool: tagpoolView },
    help: {
      tagpool: "מקלידים טרנזקציות כזוגות שליחה-תשובה (למשל 0-30 5-10), ובשני מאגרים עם R או W לפני כל אחת, או מגרילים. כל צעד הוא אירוע אחד לפי הזמן, תשובה לפני שליחה באותו רגע : הקו שמתחת לטרנזקציות הוא כמה פתוחות, הקו המקווקו השיא עד עכשיו, והטרנזקציות הפתוחות מודגשות. בסוף התשובה היא השיא, ובשני מאגרים גם השיא של כל סוג לבד והחיסכון של מאגר משותף.",
    },
    models: { tpSweep, tpPools },
  });
})();
