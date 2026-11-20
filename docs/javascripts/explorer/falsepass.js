// kinds: falsepass
//   falsepass              0111        the register slice and its testbench over 40 cycles: the three testbench fixes and the DUT fix as switches, the LFSR seed; the waveform with the overwritten items and every error marked, a cycle cursor with the scoreboard's list and the checkers' counts at that cycle, the log so far and the verdict
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, ltr, waveStrip } = dvqExplorers.lib;
  const NB = " ";

  // The page's run_bench (0111), line for line: one run of slice_tb, the four fixes as
  // flags (0 or 1). rows[t] are the values the edge that ends cycle t samples; errors are
  // [cycle, checker, item] in the order the bench prints them (a_hold before the
  // scoreboard in one edge, as Verilator runs them). snaps[t] (not in the Python) is what
  // the checkers hold after that edge, for the cursor.
  const FP = { CYCLES: 40, RESET: 2, DRAIN: 6, MAX_WAIT: 10, SEED: 187 };
  const fpLfsr = (s) => ((s << 1) | (((s >> 15) ^ (s >> 13) ^ (s >> 12) ^ (s >> 10)) & 1)) & 0xffff;
  const fpRun = (seed, bp, sva, sb, fx) => {
    let lfsr = seed, inValid = 0, inData = 0, took = 0, full = 0, data = 0, rq = 0;
    let stalls = 0, holds = 0, checked = 0, nIn = 0, nOut = 0, prev = null;
    const expected = [], errors = [], rows = [], snaps = [];
    for (let t = 0; t < FP.CYCLES; t++) {
      if (took) inValid = 0;                                   // the driver, between two edges
      const rstN = t >= FP.RESET ? 1 : 0;
      let outReady = 1;
      if (rstN && t < FP.CYCLES - FP.DRAIN) {
        for (let i = 0; i < 4; i++) lfsr = fpLfsr(lfsr);
        if (!inValid && (lfsr & 3)) { inValid = 1; inData += 1; }
        if (bp) outReady = ((lfsr >> 2) & 3) !== 0 ? 1 : 0;
      }
      const inReady = !full || (fx ? outReady : rq) ? 1 : 0;
      const row = { t, rst_n: rstN, in_valid: inValid, in_ready: inReady, in_data: inData,
                    out_valid: full, out_ready: outReady, out_data: data, full_q: full, out_ready_q: rq };
      rows.push(row);
      if (rstN) {                                              // the checkers, at the edge
        if (sva && prev && prev.rst_n && prev.out_valid && !prev.out_ready) {
          checked++;
          if (!(full && data === prev.out_data)) errors.push([t, "a_hold", prev.out_data]);
        }
        if (full && outReady) {
          nOut++;
          const at = expected.findIndex(([d]) => d === data);
          if (at < 0) errors.push([t, "unexpected", data]); else expected.splice(at, 1);
        }
        if (inValid && inReady) { nIn++; expected.push([inData, t]); }
        if (sb) expected.forEach(([d, t0]) => { if (t - t0 === FP.MAX_WAIT) errors.push([t, "wait", d]); });
        if (full && !outReady) { stalls += bp; holds += sva; }
      }
      snaps.push({ expected: expected.map((e) => e.slice()), n_in: nIn, n_out: nOut, stalls, holds, checked });
      took = inValid && inReady ? 1 : 0;                       // the edge
      if (!rstN) { full = 0; data = 0; rq = 0; } else {
        if (inValid && inReady) { full = 1; data = inData; } else if (outReady) full = 0;
        rq = outReady;
      }
      prev = row;
    }
    if (bp && stalls === 0) errors.push([FP.CYCLES, "c_stall", 0]);   // the end of the test
    if (sva && holds === 0) errors.push([FP.CYCLES, "c_hold", 0]);
    if (sb) expected.forEach(([d]) => errors.push([FP.CYCLES, "missing", d]));
    return { rows, errors, n_in: nIn, n_out: nOut, left: expected.map(([d]) => d), stalls, holds, checked, snaps };
  };
  // The bench's error texts and its log (tools/figures/q0111.py prints the same lines).
  const FP_MSG = {
    a_hold: () => "a_hold: out_data changed while out_ready was low",
    unexpected: (d) => `scoreboard: unexpected item ${d}`,
    wait: (d) => `scoreboard: item ${d} still waiting after ${FP.MAX_WAIT} cycles`,
    missing: (d) => `scoreboard: item ${d} never came out`,
    c_stall: () => "c_stall: no cycle with out_valid && !out_ready",
    c_hold: () => "c_hold: a_hold never checked anything",
  };
  const fpLog = (r) => {
    const lines = r.errors.map(([t, who, d]) => `ERROR at cycle ${t}: ${FP_MSG[who](d)}`);
    const n = r.errors.length;
    lines.push(`TEST ${n ? "FAILED" : "PASSED"}: ${r.n_in} in, ${r.n_out} out, ${n} errors`);
    if (n) { const [t, who, d] = r.errors[0]; lines.push(`first error: cycle ${t}: ${FP_MSG[who](d)}`); }
    return lines;
  };
  // The cycles where the broken slice takes a new item over the one that waits, and that item.
  const fpLost = (r) => r.rows.filter((w) => w.rst_n && w.out_valid && !w.out_ready && w.in_valid && w.in_ready).map((w) => [w.t, w.out_data]);
  const checker = (who) => (who === "wait" || who === "missing" || who === "unexpected" ? "scoreboard" : who);

  const SWITCHES = [
    ["fp-bp", "א\u00a0: עצירות ויעד"],
    ["fp-sva", "ב\u00a0: ה-assertion"],
    ["fp-sb", "ג\u00a0: ה-scoreboard"],
    ["fp-fx", "ד\u00a0: ה-DUT"],
  ];

  // The box (0111): the switches and the seed; the transport over cycles 0..40 (40 is the
  // end of the test); the verdict of the run; the waveform with the cursor, the overwritten
  // items shaded on out_data and an ✗ where the bench reports an error; a line on the
  // cycle; cards for the scoreboard's list, the assertion with the two covers, and the log so far.
  const falsepassView = () => ({
    mount(box) {
      const st = { flags: [0, 0, 0, 0], seed: FP.SEED, k: FP.CYCLES };
      box.innerHTML =
        `<div class="ex-controls fp-switches">` +
        SWITCHES.map(([cls, text]) => `<label><input type="checkbox" class="${cls}"> <span>${text}</span></label>`).join("") +
        `<label>ערך האתחול <input type="number" class="fp-seed" min="1" max="65535" step="1" dir="ltr" inputmode="numeric" value="${FP.SEED}" aria-label="ערך האתחול של ה-LFSR, 1 עד 65535"></label></div>` +
        `<div class="ex-controls">` +
        `<button type="button" class="md-button ex-start">המחזור הראשון</button>` +
        `<button type="button" class="md-button ex-prev">המחזור הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">המחזור הבא</button>` +
        `<button type="button" class="md-button ex-end">סוף הטסט</button>` +
        `<button type="button" class="md-button fp-tolost">לפריט שנדרס</button>` +
        `<button type="button" class="md-button fp-tofail">לשגיאה הראשונה</button>` +
        `<span class="ex-pos fp-pos"></span></div>` +
        `<p class="ex-summary fp-sum" aria-live="polite"></p>` +
        `<div class="wv-wrap fp-strip" tabindex="0" role="group" aria-label="דיאגרמת התזמון של הריצה, 40 מחזורים ועמודת סוף הטסט, גלילה אופקית"></div>` +
        `<span class="viz-legend fp-legend"><span><i class="fp-key-lost"></i>פריט שנדרס ביציאה</span><span><i class="fp-key-fail"></i>שגיאה שהסביבה מדפיסה</span><span><i class="fp-key-now"></i>המחזור של הכרטיסים</span></span>` +
        `<p class="wv-step fp-now" aria-live="polite"></p>` +
        `<div class="fp-cards">` +
        `<section class="fp-card fp-sbcard"><p class="fp-ctitle">הרשימה של ה-scoreboard</p><div class="fp-list" dir="ltr"></div><p class="fp-cnt"></p></section>` +
        `<section class="fp-card"><p class="fp-ctitle">ה-assertion וה-covers</p><p class="fp-assert"></p><p class="fp-stall"></p></section>` +
        `<section class="fp-card fp-logcard"><p class="fp-ctitle">הלוג עד המחזור</p><pre class="fp-log" dir="ltr" tabindex="0" role="region" aria-label="הלוג של הסביבה עד המחזור המסומן"></pre></section>` +
        `</div>`;
      const $ = (sel) => box.querySelector(sel);
      const boxes = SWITCHES.map(([cls]) => $(`.${cls}`));
      const N = FP.CYCLES + 1;                                  // the cycles and the end of the test
      let run = null;
      const compute = () => { run = fpRun(st.seed, ...st.flags); };
      const verdict = () => {
        const [bp, sva, sb, fx] = st.flags, lost = fpLost(run), n = run.errors.length;
        const counts = ltr(`${run.n_in} in, ${run.n_out} out`);
        if (!n) {
          let s = `<span class="wv-ok">TEST PASSED</span>${NB}: ${counts}`;
          if (lost.length) s += `, <span class="wv-bad">אבל ${lost.length === 1 ? "פריט אחד נדרס" : `${ltr(lost.length)} פריטים נדרסו`} (${ltr(lost.map(([, d]) => d).join(", "))}), ואף בודק לא דיווח.</span>`;
          else if (fx) s += ". ה-DUT באמת תקין, וכל פריט שנכנס יצא.";
          else if (!bp) s += `. ‏${code("out_ready")} תמיד 1, ולכן ה-DUT השבור מתנהג כמו המתוקן.`;
          else s += ". אף עצירה לא פגשה פריט חדש בכניסה, ולכן הבאג לא קרה בריצה הזו.";
          return s;
        }
        const [t, who] = run.errors[0];
        let s = `<span class="wv-bad">TEST FAILED</span>${NB}: הראשון לדווח הוא ${code(checker(who))}, במחזור ${ltr(t)}${n > 1 ? `, ובסך הכול ${ltr(n)} שגיאות` : ""}.`;
        if (who === "c_hold") s += ` ה-assertion לא בדק אף מחזור, כי אף פריט לא חיכה ביציאה.`;
        else if (who === "c_stall") s += ` הגירוי של ערך האתחול הזה לא עצר אף פריט${NB}: זו לא שגיאה של ה-DUT, אלא של הגירוי.`;
        return s;
      };
      // the errors of the end of the test: the cover goals by name, the items that never came out counted
      const endErrors = (end) => {
        const missing = end.filter(([, who]) => who === "missing").map(([, , d]) => d);
        const parts = end.filter(([, who]) => who !== "missing").map(([, who]) => code(who));
        if (missing.length) parts.push(`${code("scoreboard")}, ${missing.length === 1 ? `פריט ${ltr(missing[0])} לא יצא` : `${ltr(missing.length)} פריטים לא יצאו`}`);
        return parts.join("; ");
      };
      const describe = (k) => {
        if (k === FP.CYCLES) {
          const end = run.errors.filter(([t]) => t === FP.CYCLES);
          return `סוף הטסט (האירוע ${code("eot")}, אחרי ${ltr(FP.DRAIN)} מחזורי הניקוז)${NB}: ` +
            (end.length ? `<span class="wv-bad">${endErrors(end)}</span>.` : "בדיקות הסוף לא מצאו כלום.");
        }
        const w = run.rows[k];
        if (!w.rst_n) return `מחזור ${ltr(k)}${NB}: איפוס (${code("rst_n")} נמוך).${st.flags[1] ? "" : ` ‏${code("disable iff (rst_n)")} פעיל רק כאן, וכאן ${code("out_valid")} נמוך.`}`;
        const parts = [];
        const lostNow = w.out_valid && !w.out_ready && w.in_valid && w.in_ready;
        if (lostNow) parts.push(`<span class="wv-bad">פריט ${ltr(w.in_data)} נכנס ודורס את פריט ${ltr(w.out_data)}, שמחכה ביציאה</span>`);
        else {
          if (w.out_valid && w.out_ready) parts.push(`פריט ${ltr(w.out_data)} יוצא`);
          if (w.out_valid && !w.out_ready) parts.push(`פריט ${ltr(w.out_data)} מחכה ביציאה`);
          if (w.in_valid && w.in_ready) parts.push(`פריט ${ltr(w.in_data)} נכנס`);
          if (w.in_valid && !w.in_ready) parts.push(`פריט ${ltr(w.in_data)} מחכה בכניסה`);
        }
        const errs = run.errors.filter(([t]) => t === k);
        let s = `מחזור ${ltr(k)}${NB}: ${parts.length ? parts.join(", ") : "אין העברה"}.`;
        if (errs.length) s += ` <span class="wv-bad">✗ ${errs.map(([, who, d]) => `${code(checker(who))}${who === "a_hold" ? "" : ` (פריט ${ltr(d)})`}`).join(", ")}</span>`;
        return s;
      };
      const draw = () => {
        const k = st.k, [bp, sva, sb, fx] = st.flags, R = run.rows, lost = fpLost(run);
        const lostAt = new Set(lost.map(([t]) => t));
        $(".fp-pos").textContent = `מחזור ${k} מתוך ${FP.CYCLES}`;
        $(".ex-start").disabled = $(".ex-prev").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === FP.CYCLES;
        $(".fp-tolost").disabled = !lost.length;
        $(".fp-tofail").disabled = !run.errors.length;
        $(".fp-sum").innerHTML = verdict();
        const bit = (name) => R.map((w) => w[name]);
        const fails = Array.from({ length: N }, (_, t) => (run.errors.some(([c]) => c === t) ? 1 : 0));
        const rows = [
          { name: "rst_n", kind: "bit", values: bit("rst_n"), cls: "wv-dim" },
          { name: "in_valid", kind: "bit", values: bit("in_valid"), cls: "wv-s1" },
          { name: "in_ready", kind: "bit", values: bit("in_ready"), cls: "wv-s1" },
          { name: "in_data", kind: "bus", values: bit("in_data") },
          { name: "out_valid", kind: "bit", values: bit("out_valid"), cls: "wv-s2" },
          { name: "out_ready", kind: "bit", values: bit("out_ready"), cls: "wv-s2" },
          { name: "out_data", kind: "bus", values: bit("out_data"), marks: R.map((w) => lostAt.has(w.t)) },
          { name: "out_ready_q", kind: "bit", values: fx ? [] : bit("out_ready_q"), cls: "wv-dim" },
          { name: "errors", kind: "flag", values: fails },
        ];
        const strip = $(".fp-strip");
        strip.innerHTML = waveStrip(rows, N, { slotW: 22, labelW: 92, cursor: k, ticks: (t) => t, label: `דיאגרמת התזמון, ערך האתחול ${st.seed}` });
        // a strip wider than the box scrolls: keep the cursor's column in view, beside the
        // row names that stick to the left edge (92 px), with two columns of context
        const x = 92 + k * 22;
        if (strip.clientWidth > 92 + 5 * 22) {
          if (x < strip.scrollLeft + 92) strip.scrollLeft = Math.max(0, x - 92 - 2 * 22);
          else if (x + 22 > strip.scrollLeft + strip.clientWidth) strip.scrollLeft = x + 3 * 22 - strip.clientWidth;
        }
        $(".fp-now").innerHTML = describe(k);
        // the cards: what the checkers hold after the edge of cycle k (at 40, after the end checks)
        const snap = run.snaps[Math.min(k, FP.CYCLES - 1)];
        const gone = new Set(lost.filter(([t]) => t <= k).map(([, d]) => d));
        $(".fp-list").innerHTML = snap.expected.length
          ? snap.expected.map(([d, t0]) => `<span class="fp-item${gone.has(d) ? " is-lost" : ""}${sb && k - t0 >= FP.MAX_WAIT ? " is-late" : ""}"><b>${d}</b><small>${t0}</small></span>`).join("")
          : `<span class="fp-empty">empty</span>`;
        let cnt = `נכנסו ${ltr(snap.n_in)}, יצאו ${ltr(snap.n_out)}`;
        cnt += gone.size ? `, <span class="wv-bad">${gone.size === 1 ? `ופריט ${ltr([...gone][0])} נדרס` : `ו-${ltr(gone.size)} נדרסו`}.</span> ` : ". ";
        if (k === FP.CYCLES) cnt += sb ? "בסוף הטסט כל פריט ברשימה הוא שגיאה." : "בסוף הטסט אף אחד לא בודק את הרשימה.";
        else cnt += `מתחת לכל פריט${NB}: המחזור שבו נכנס${sb ? `, ואחרי ${ltr(FP.MAX_WAIT)} מחזורים הוא שגיאה.` : ", ואין גבול להמתנה."}`;
        $(".fp-cnt").innerHTML = cnt;
        const fA = run.errors.filter(([t, who]) => who === "a_hold" && t <= k).length;
        const goal = (n) => (k === FP.CYCLES ? (n ? " ✓" : ` <span class="wv-bad">✗ היעד הוא לפחות 1</span>`) : "");
        $(".fp-assert").innerHTML = sva
          ? `‏${code("a_hold")} עם ${code("disable iff (!rst_n)")}${NB}: בדק ${ltr(snap.checked)} מחזורים, נכשל ב-${ltr(fA)}. ‏${code("c_hold")}${NB}: ${ltr(snap.holds)} פגיעות${goal(snap.holds)}.`
          : `‏${code("a_hold")} עם ${code("disable iff (rst_n)")}${NB}: מנוטרל כל עוד ${code("rst_n")} גבוה, ולא בדק אף מחזור.`;
        $(".fp-stall").innerHTML = bp
          ? `‏${code("c_stall")}${NB}: ${ltr(snap.stalls)} מחזורים שבהם פריט חיכה ביציאה${goal(snap.stalls)}.`
          : `‏${code("BACKPRESSURE = 0")}${NB}: ${code("out_ready")} תמיד 1, ואף פריט לא חיכה ביציאה.`;
        const lines = fpLog(run).filter((line) => line.startsWith("ERROR") ? Number(/cycle (\d+)/.exec(line)[1]) <= k : k === FP.CYCLES);
        $(".fp-log").textContent = lines.length ? lines.join("\n") : "—";
      };
      const reload = () => { compute(); draw(); };
      boxes.forEach((el, i) => el.addEventListener("change", () => { st.flags[i] = el.checked ? 1 : 0; reload(); }));
      const seedIn = $(".fp-seed");
      seedIn.addEventListener("change", () => {
        const v = Math.round(Number(seedIn.value));
        if (v >= 1 && v <= 65535) { st.seed = v; reload(); } else seedIn.value = String(st.seed);
      });
      const go = (k) => { st.k = Math.max(0, Math.min(FP.CYCLES, k)); draw(); };
      $(".ex-start").addEventListener("click", () => go(0));
      $(".ex-prev").addEventListener("click", () => go(st.k - 1));
      $(".ex-next").addEventListener("click", () => go(st.k + 1));
      $(".ex-end").addEventListener("click", () => go(FP.CYCLES));
      $(".fp-tolost").addEventListener("click", () => { const l = fpLost(run); if (l.length) go(l[0][0]); });
      $(".fp-tofail").addEventListener("click", () => { if (run.errors.length) go(run.errors[0][0]); });
      // a click anywhere in a column of the strip moves the cursor there
      $(".fp-strip").addEventListener("click", (e) => {
        const svg = e.target.closest("svg.wave-strip");
        if (!svg) return;
        const x = e.clientX - svg.getBoundingClientRect().left;
        const t = Math.floor((x - 92) / 22);
        if (t >= 0 && t < N) go(t);
      });
      // the link and the remembered state: the cursor rides after the controls
      box.dvqExtra = {
        get: () => (st.k === FP.CYCLES ? "" : String(st.k)),
        set: (text) => { const v = Number(text); if (!/^\d+$/.test(text) || v > FP.CYCLES) return false; go(v); return true; },
      };
      reload();
    },
  });

  dvqExplorers.register({
    views: { falsepass: falsepassView },
    help: {
      falsepass: "ארבעת המתגים הם ארבעת התיקונים של השאלה\u00a0: שלושה בסביבת הבדיקה ואחד ב-DUT. ערך האתחול בוחר את הגירוי של ה-LFSR, כמו הפרמטר SEED. הסביבה רצה 40 מחזורים, והשורה העליונה אומרת מה היא מדפיסה בסוף. המחזור המסומן (לחיצה על עמודה, או הכפתורים) קובע מה הכרטיסים מראים\u00a0: הרשימה של ה-scoreboard אחרי הקצה, הספירות של ה-assertion ושל ה-covers, והלוג עד אותו מחזור. העמודה 40 היא סוף הטסט.",
    },
    models: { FP, fpRun, fpLog, fpLost },
  });
})();
