// kinds: edge
//   edge                   0001        sig drawn cell by cell on a timing strip; sig_q and pulse follow, for a rising, falling or any edge; the reset trap; beside the strip the circuit of the chosen edge with the values of the cycle under the cursor (a wire at 1 lit, the flip-flop framed when it took a new value) and a table of every signal, a column per cycle; the transport moves the cursor
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, ltr, seedControls, waveStrip } = dvqExplorers.lib;

  // Edge detector (0001): sig per cycle, cycle 0 being the reset cycle (rst_n low, so
  // sig_q is 0 there); from cycle 1 sig_q is the previous cycle's sig. pulse follows the
  // page's AND for a rising edge, its mirror for a falling edge, XOR for both.
  const EDGE_MODES = {
    rise: (s, q) => (s && !q ? 1 : 0),
    fall: (s, q) => (!s && q ? 1 : 0),
    both: (s, q) => (s !== q ? 1 : 0),
  };
  const edgeTrace = (sig, mode = "rise") => {
    const fn = EDGE_MODES[mode] || EDGE_MODES.rise;
    const sigQ = sig.map((_, i) => (i === 0 ? 0 : sig[i - 1]));
    const pulse = sig.map((s, i) => fn(s, sigQ[i]));
    // the true edges of sig (between cycles i - 1 and i), independent of the circuit
    const edges = sig.map((s, i) => (i > 0 && fn(s, sig[i - 1]) ? 1 : 0));
    const pulses = [];
    pulse.forEach((p, i) => { if (p && !(i > 0 && pulse[i - 1])) pulses.push(i); });
    const widths = pulses.map((i) => { let w = 0; while (pulse[i + w]) w++; return w; });
    return { sigQ, pulse, edges, pulses, widths, phantom: pulse[0] === 1 };
  };

  // --- the circuit, as tools/figures/q0001.py figure(mode), with the values of a clock -----------

  const X_IN = 68, Y_SIG = 44, Y_D = 116, Y_CLK = 150, JX = 128, FX = 178, FY = 96, FW = 70, FH = 80;
  const NX = 318, AX = 408, AY = 58, AH = 44, OUT_X = 510, BEND = AX - 26;
  const hiCls = (on) => (on ? " is-hi" : "");
  const txt = (x, y, s, anchor = "middle", cls = "ff-text") => `<text class="${cls}" x="${x}" y="${y}" text-anchor="${anchor}">${s}</text>`;
  const wire = (pts, on) => `<polyline class="ff-wire${hiCls(on)}" points="${pts.map(([a, b]) => `${a},${b}`).join(" ")}"/>`;
  const inverter = (x, y) => `<path class="ff-gate" d="M${x},${y - 12} L${x + 22},${y} L${x},${y + 12} Z"/><circle class="ff-gate" cx="${x + 26}" cy="${y}" r="4"/>`;
  const andGate = (x, y, h, on) => `<path class="ff-gate${on ? " is-on" : ""}" d="M${x},${y - h / 2} H${x + h / 2} A${h / 2},${h / 2} 0 0 1 ${x + h / 2},${y + h / 2} H${x} Z"/>`;
  const xorGate = (x, y, h, on) => `<path class="ff-gate${on ? " is-on" : ""}" d="M${x - 4},${y - h / 2} Q${x + 10},${y} ${x - 4},${y + h / 2} Q${x + 26},${y + h / 2} ${x + h},${y} Q${x + 26},${y - h / 2} ${x - 4},${y - h / 2} Z"/>` +
    `<path class="ff-wire" d="M${x - 11},${y - h / 2} Q${x + 3},${y} ${x - 11},${y + h / 2}"/>`;
  // the circuit of a mode (rise: the page's module; fall and both: the follow-ups) with the
  // values of clock v = { rst, sig, q, pulse, cap } on its wires: a wire at 1 lit, the
  // flip-flop framed when it took a new value at this clock's edge; v = null draws it bare
  const edgeDiagram = (mode = "rise", v = null) => {
    const on = (net) => Boolean(v) && net === 1;
    const val = (x, y, n) => (v ? `<text class="ed-val${n ? " is-one" : ""}" x="${x}" y="${y}" text-anchor="middle">${n}</text>` : "");
    const sig = v ? v.sig : null, q = v ? v.q : null, rst = v ? v.rst : null;
    let s = `<svg class="ff-fig ed-live" viewBox="0 0 580 212" direction="ltr" role="img" aria-label="המעגל של ${mode === "rise" ? "עליית שפה" : mode === "fall" ? "ירידת שפה" : "שתי השפות"}${v ? " עם הערכים של המחזור הזה" : ""}">`;
    s += txt(X_IN - 6, Y_SIG + 6, "sig", "end") + txt(X_IN - 6, Y_CLK + 6, "clk", "end");
    const rx = FX + FW / 2, ry = FY + FH;
    s += txt(X_IN - 6, ry + 26, "rst_n", "end");
    const a2 = AY + 14;
    if (mode === "fall") s += wire([[X_IN, Y_SIG], [NX, Y_SIG]], on(sig)) + inverter(NX, Y_SIG) + wire([[NX + 30, Y_SIG], [AX, Y_SIG]], on(v && 1 - sig)) + val(375, 36, v && 1 - sig);
    else s += wire([[X_IN, Y_SIG], [AX, Y_SIG]], on(sig));
    s += wire([[JX, Y_SIG], [JX, Y_D], [FX, Y_D]], on(sig)) + `<circle class="ink-dot" cx="${JX}" cy="${Y_SIG}" r="4"/>` + val(98, 36, sig);
    s += `<rect class="ff-gate${v && v.cap ? " is-on" : ""}" x="${FX}" y="${FY}" width="${FW}" height="${FH}" rx="3"/>`;
    s += txt(FX + 8, Y_D + 6, "D", "start", "ff-pin") + txt(FX + FW - 8, Y_D + 6, "Q", "end", "ff-pin");
    s += wire([[X_IN, Y_CLK], [FX, Y_CLK]], false) + `<path class="ff-wire" d="M${FX},${Y_CLK - 7} L${FX + 10},${Y_CLK} L${FX},${Y_CLK + 7}"/>`;
    s += `<circle class="ff-gate" cx="${rx}" cy="${ry + 4}" r="4"/>` + wire([[rx, ry + 8], [rx, ry + 20], [X_IN, ry + 20]], on(rst)) + val(100, ry + 13, rst);
    s += txt((FX + FW + NX) / 2, Y_D - 10, "sig_q", "middle", "ff-small") + val((FX + FW + NX) / 2, Y_D + 22, q);
    if (mode === "rise") s += wire([[FX + FW, Y_D], [NX, Y_D]], on(q)) + inverter(NX, Y_D) + wire([[NX + 30, Y_D], [BEND, Y_D], [BEND, a2], [AX, a2]], on(v && 1 - q)) + val(365, Y_D + 22, v && 1 - q);
    else s += wire([[FX + FW, Y_D], [BEND, Y_D], [BEND, a2], [AX, a2]], on(q));
    s += mode === "both" ? xorGate(AX, AY, AH, on(v && v.pulse)) : andGate(AX, AY, AH, on(v && v.pulse));
    s += wire([[AX + AH, AY], [OUT_X, AY]], on(v && v.pulse)) + val(481, AY - 8, v && v.pulse);
    s += txt(OUT_X + 6, AY + 6, "pulse", "start");
    return s + "</svg>";
  };
  // the values of cycle k of a trace: rst_n is low in cycle 0 only, the flip-flop took a new
  // value when sig_q differs from the cycle before
  const edgeAt = (sig, tr, k) => ({ rst: k === 0 ? 0 : 1, sig: sig[k], q: tr.sigQ[k], pulse: tr.pulse[k], cap: k > 0 && tr.sigQ[k] !== tr.sigQ[k - 1] });

  // The edge detector box (0001): tap the cells of sig to draw it cycle by cycle (cycle 0
  // is the reset cycle); sig_q and pulse follow the page's circuit, for a rising edge, a
  // falling edge or both; the reset trap as a toggle; the page's own diagram as a preset.
  // Beside the strip, the circuit with the values of the cycle under the cursor and a table
  // of every signal, a column per cycle; the transport moves the cursor.
  const MID = { rise: ["~sig_q", (s, q) => 1 - q], fall: ["~sig", (s) => 1 - s], both: null };
  const edgeView = () => ({
    mount(box) {
      const N = 12;
      const PAGE = [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0];
      const FORMULA = { rise: "sig &amp; ~sig_q", fall: "~sig &amp; sig_q", both: "sig ^ sig_q" };
      const NAME = { rise: "עליית שפה", fall: "ירידת שפה", both: "שפה (עלייה או ירידה)" };
      const st = { sig: PAGE.slice(), mode: "rise", cur: 2 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>השפה שמזהים <select class="ex-mode" aria-label="איזו שפה מזהים"><option value="rise">עלייה</option><option value="fall">ירידה</option><option value="both">שתיהן</option></select></label>` +
        `<label><input type="checkbox" class="ex-hi"> <span>‏${code("sig")} כבר גבוה בזמן האיפוס</span></label>` +
        `<button type="button" class="md-button ex-start">המחזור הראשון</button>` +
        `<button type="button" class="md-button ex-prev">המחזור הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">המחזור הבא</button>` +
        `<button type="button" class="md-button ex-end">המחזור האחרון</button></div>` +
        `<div class="ex-controls"><span class="wv-presets">דוגמאות : <button type="button" class="md-button ex-preset" data-p="page">הדיאגרמה שבעמוד</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="short">פולסים קצרים</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="random">אקראי</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="clear">ניקוי</button></span></div>` +
        `<div class="wv-wrap" tabindex="0" role="group" aria-label="דיאגרמת תזמון של גלאי השפה, גלילה אופקית"></div>` +
        `<p class="wv-sum ed-sum"></p>` +
        `<span class="viz-legend ed-legend"><span><i class="ed-key-hi"></i>חוט ב-1</span><span><i class="ed-key-cap"></i>ערך חדש בפליפ-פלופ</span><span><i class="ed-key-now"></i>המחזור הנוכחי בטבלה</span></span>` +
        `<div class="ed-dpwrap"></div>` +
        `<div class="ed-tabwrap" dir="ltr" tabindex="0" role="region" aria-label="כל האותות, עמודה לכל מחזור"></div>` +
        `<p class="wv-step" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const table = (tr) => {
        const mid = MID[st.mode];
        const rows = [["rst_n", (k) => (k === 0 ? 0 : 1)], ["sig", (k) => st.sig[k]], ["sig_q", (k) => tr.sigQ[k]]];
        if (mid) rows.push([mid[0], (k) => mid[1](st.sig[k], tr.sigQ[k])]);
        rows.push(["pulse", (k) => tr.pulse[k]]);
        const now = (k) => (k === st.cur ? "is-now" : "");
        let t = `<table class="ed-tab"><thead><tr><th scope="col">מחזור</th>${st.sig.map((_, k) => `<th scope="col"${now(k) ? ` class="${now(k)}"` : ""}>${k}</th>`).join("")}</tr></thead><tbody>`;
        rows.forEach(([name, f]) => {
          t += `<tr><th scope="row">${name}</th>` + st.sig.map((_, k) => {
            const v = f(k), cls = [now(k), v ? "is-hi" : ""].filter(Boolean).join(" ");
            return `<td${cls ? ` class="${cls}"` : ""}>${v}</td>`;
          }).join("") + "</tr>";
        });
        return t + "</tbody></table>";
      };
      const draw = () => {
        const tr = edgeTrace(st.sig, st.mode);
        st.cur = Math.max(0, Math.min(N - 1, st.cur));
        $(".ex-hi").checked = st.sig[0] === 1;
        $(".ex-start").disabled = $(".ex-prev").disabled = st.cur === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.cur === N - 1;
        const rows = [
          { name: "rst_n", kind: "bit", values: st.sig.map((_, i) => (i === 0 ? 0 : 1)), cls: "wv-dim" },
          { name: "clk", kind: "clock" },
          { name: "sig", kind: "bit", values: st.sig, cls: "wv-s1", cells: (k) => `מחזור ${k} : sig = ${st.sig[k]}, לחיצה הופכת` },
          { name: "sig_q", kind: "bit", values: tr.sigQ, cls: "wv-s3" },
          { name: "pulse", kind: "bit", values: tr.pulse, cls: "wv-s2" },
        ];
        $(".wv-wrap").innerHTML = waveStrip(rows, N, { role: "group", label: "דיאגרמת תזמון", cursor: st.cur, ticks: (k) => k });
        $(".ed-dpwrap").innerHTML = edgeDiagram(st.mode, edgeAt(st.sig, tr, st.cur));
        const tw = $(".ed-tabwrap");
        tw.innerHTML = table(tr);
        const cur = tw.querySelector("th.is-now");
        if (cur && tw.scrollWidth > tw.clientWidth) tw.scrollLeft = Math.max(0, cur.offsetLeft - tw.clientWidth / 2);
        const k = st.cur, s = st.sig[k], q = tr.sigQ[k], p = tr.pulse[k];
        const out = ltr(`${code("pulse")} = ${code(FORMULA[st.mode])} = ${p}`);
        let step = k === 0
          ? `מחזור 0 הוא מחזור האיפוס : ${code("rst_n")} נמוך, ולכן ${ltr(`${code("sig_q")} = 0`)} בכוח. ${ltr(`${code("sig")} = ${s}`)} ⇒ ${out}.`
          : `מחזור ${ltr(k)} : ${ltr(`${code("sig")} = ${s}`)} עכשיו, ${ltr(`${code("sig_q")} = ${q}`)} (הערך של ${code("sig")} במחזור ${ltr(k - 1)}) ⇒ ${out}.`;
        if (k === 0 && p) step += ` <span class="wv-bad">פולס בלי שפה : ${code("sig")} היה גבוה כבר בזמן האיפוס, ו-${code("sig_q")} מתחיל מ-0. זו המלכודת מהערה 2 של הקוד.</span>`;
        else if (p) step += ` <span class="wv-ok">${NAME[st.mode]} בין מחזור ${ltr(k - 1)} למחזור ${ltr(k)} : הפולס גבוה במחזור הזה בלבד.</span>`;
        else if (k > 0 && s && q && st.mode === "rise") step += ` ${code("sig")} עדיין גבוה, אבל גם ${code("sig_q")} כבר 1 : ה-AND מאפס את המוצא, ולכן הפולס לא מתארך.`;
        $(".wv-step").innerHTML = step;
        const high = tr.pulse.reduce((a, b) => a + b, 0), edges = tr.edges.reduce((a, b) => a + b, 0);
        let sum = `‏${code("pulse")} גבוה ב-${ltr(high)} מחזורים`;
        sum += edges === 1 ? `, ויש ${NAME[st.mode]} אחת` : `, ויש ${ltr(edges)} שפות מהסוג שנבחר`;
        if (tr.phantom) sum += ` ועוד פולס אחד בלי שפה במחזור האיפוס`;
        sum += high === edges + (tr.phantom ? 1 : 0) ? ` : מחזור אחד בדיוק לכל שפה ✓` : ".";
        if (st.mode === "both" && tr.widths.some((w) => w > 1)) sum += ` שפות במחזורים עוקבים נותנות פולס רצוף : המוצא גבוה בכל מחזור שבו ${code("sig")} שונה מהמחזור הקודם.`;
        $(".wv-sum").innerHTML = sum;
      };
      const wrap = $(".wv-wrap");
      const tap = (k) => { st.sig[k] = st.sig[k] ? 0 : 1; st.cur = k; draw(); };
      wrap.addEventListener("click", (e) => { const c = e.target.closest(".wv-cell"); if (c) tap(Number(c.dataset.k)); });
      wrap.addEventListener("keydown", (e) => {
        const c = e.target.closest(".wv-cell");
        if (c && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); tap(Number(c.dataset.k)); }
      });
      $(".ex-mode").addEventListener("change", () => { st.mode = $(".ex-mode").value; draw(); });
      $(".ex-hi").addEventListener("change", () => { st.sig[0] = $(".ex-hi").checked ? 1 : 0; st.cur = 0; draw(); });
      $(".ex-start").addEventListener("click", () => { st.cur = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { st.cur--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.cur++; draw(); });
      $(".ex-end").addEventListener("click", () => { st.cur = N - 1; draw(); });
      const cursorAfter = (p) => { st.cur = p === "clear" ? 1 : Math.max(1, st.sig.findIndex((v, i) => i > 0 && v !== st.sig[i - 1])); draw(); };
      const seed = seedControls(box, $(".wv-presets"), (rng) => { st.sig = Array.from({ length: N }, () => (rng() < 0.5 ? 1 : 0)); cursorAfter("random"); });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => {
        const p = b.dataset.p;
        if (p === "random") { seed.draw(); return; }
        if (p === "page") st.sig = PAGE.slice();
        else if (p === "short") st.sig = [0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1];
        else st.sig = new Array(N).fill(0);
        cursorAfter(p);
      }));
      // the link and the remembered state: sig cycle by cycle and the cursor, "001111001100_2"
      box.dvqExtra = {
        get: () => `${st.sig.join("")}_${st.cur}`,
        set: (text) => {
          const m = /^([01]{12})_(\d+)$/.exec(text);
          if (!m) return false;
          Object.assign(st, { sig: [...m[1]].map(Number), cur: Number(m[2]) });
          draw();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { edge: edgeView },
    // the strip, the summary and the key on the left; the circuit, the table and the step beside them
    cols: { edge: { side: ".ed-dpwrap, .ed-tabwrap, .wv-step", w: "minmax(0, 1.45fr)" } },
    help: {
      edge: "לוחצים על משבצות של sig ברצועת התזמון : sig_q ו-pulse עוקבים לפי בורר השפה. המתג מראה את מלכודת האיפוס, והדוגמאות טוענות את הדיאגרמה של העמוד, פולסים קצרים, אות אקראי או אות ריק. לצד הרצועה המעגל עם הערכים של המחזור המסומן (חוט ב-1 מודגש) וטבלה של כל האותות, עמודה לכל מחזור. החצים, או המקשים ← →, מעבירים את המחזור. ״העתקת WaveDrom״ מעתיקה את הרצועה כ-JSON.",
    },
    models: { EDGE_MODES, edgeTrace, edgeDiagram, edgeAt },
  });
})();
