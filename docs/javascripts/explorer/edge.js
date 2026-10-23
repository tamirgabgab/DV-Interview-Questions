// kinds: edge
//   edge                   0001        sig drawn cell by cell on a timing strip; sig_q and pulse follow, for a rising, falling or any edge; the reset trap
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

  // The edge detector box (0001): tap the cells of sig to draw it cycle by cycle (cycle 0
  // is the reset cycle); sig_q and pulse follow the page's circuit, for a rising edge, a
  // falling edge or both; the reset trap as a toggle; the page's own diagram as a preset.
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
        `<span class="wv-presets">דוגמאות : <button type="button" class="md-button ex-preset" data-p="page">הדיאגרמה שבעמוד</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="short">פולסים קצרים</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="random">אקראי</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="clear">ניקוי</button></span></div>` +
        `<p class="wv-hint">לחיצה על משבצת בשורה של ${code("sig")} הופכת את הערך שלה באותו מחזור. מחזור 0 הוא מחזור האיפוס.</p>` +
        `<div class="wv-wrap" tabindex="0" role="group" aria-label="דיאגרמת תזמון של גלאי השפה, גלילה אופקית"></div>` +
        `<p class="wv-step" aria-live="polite"></p><p class="ex-summary wv-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const draw = () => {
        const tr = edgeTrace(st.sig, st.mode);
        $(".ex-hi").checked = st.sig[0] === 1;
        const rows = [
          { name: "rst_n", kind: "bit", values: st.sig.map((_, i) => (i === 0 ? 0 : 1)), cls: "wv-dim" },
          { name: "clk", kind: "clock" },
          { name: "sig", kind: "bit", values: st.sig, cls: "wv-s1", cells: (k) => `מחזור ${k} : sig = ${st.sig[k]}, לחיצה הופכת` },
          { name: "sig_q", kind: "bit", values: tr.sigQ, cls: "wv-s3" },
          { name: "pulse", kind: "bit", values: tr.pulse, cls: "wv-s2" },
        ];
        $(".wv-wrap").innerHTML = waveStrip(rows, N, { role: "group", label: "דיאגרמת תזמון", cursor: st.cur, ticks: (k) => k });
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
      draw();
    },
  });

  dvqExplorers.register({
    views: { edge: edgeView },
    help: {
      edge: "לוחצים על משבצות של sig ברצועת התזמון : sig_q ו-pulse עוקבים לפי בורר השפה. המתג מראה את מלכודת האיפוס, והכפתור טוען את הדיאגרמה של העמוד. ״העתקת WaveDrom״ מעתיקה את הרצועה כ-JSON.",
    },
    models: { EDGE_MODES, edgeTrace },
  });
})();
