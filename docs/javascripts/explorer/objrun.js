// kinds: objrun
//   objrun                 0113        the run of the page's testbench over 0..160 ns: the test's objection, an output monitor that raises and never drops, the drain time; the waveform of what the monitors sample with the objection count, the drain and the run phase, a cursor with the pipeline's four stages, the objections held, the scoreboard's two lists and the end of the run (check_phase's lines, or the timeout)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, ltr, waveStrip } = dvqExplorers.lib;
  const NB = " ";

  // The timing model of tools/figures/q0113.py (0113), which tests/0113 checks against the
  // page's pyuvm code on Verilator: a 10 ns clock that starts low, reset for two rising
  // edges, one item per cycle, monitors at the falling edge, a 4-stage pipeline. Column j
  // of the box is the falling edge at 10j ns, where the monitors sample; the rising edge
  // in the middle of the column (10j + 5) is where the DUT takes an item and the test drops.
  const OR = { PERIOD: 10, LAT: 4, N: 8, RESET_EDGES: 2, LIMIT_US: 100, COLS: 17, DRAIN: 0, DRAIN_MAX: 60,
               SB: "uvm_test_top.env.sb", TEST: "uvm_test_top", HOLDER: "uvm_test_top.env.mon_out", TIMEOUT_SRC: "cocotb.pipe" };
  const orRise = (k) => OR.PERIOD / 2 + OR.PERIOD * k;
  const orTaken = (i) => orRise(OR.RESET_EDGES + i);
  const orSeenIn = (i) => orTaken(i) - OR.PERIOD / 2;
  const orSeenOut = (i) => orTaken(i) + (OR.LAT - 1) * OR.PERIOD + OR.PERIOD / 2;
  const orItems = (pred) => Array.from({ length: OR.N }, (_, i) => i).filter(pred);

  // One run: raise (the test raises around the sequence), hold (the output monitor raises
  // before its endless loop), drain (ns, after the drop). end is null for a run that never
  // ends; then check_phase never runs (passed is null) and the timeout stops it.
  const orRun = (raise, hold, drain) => {
    const drop = raise ? orTaken(OR.N - 1) : null;
    const end = hold ? null : raise ? drop + drain : 0;
    const before = (t) => end === null || t < end;
    const sent = orItems((i) => before(orSeenIn(i))), seen = orItems((i) => before(orSeenOut(i)));
    const cols = [];
    for (let j = 0; j < OR.COLS; j++) {
      const t = OR.PERIOD * j;
      const at = (f) => orItems((i) => f(i) === t)[0] ?? null;
      const holders = [];
      if (raise && t < drop) holders.push(OR.TEST);
      if (hold) holders.push(OR.HOLDER);
      cols.push({
        t,
        rst_n: t > orRise(OR.RESET_EDGES - 1) ? 1 : 0,
        in_item: at(orSeenIn),
        out_item: at(orSeenOut),
        stages: Array.from({ length: OR.LAT }, (_, s) => orItems((i) => orTaken(i) + OR.PERIOD * s <= t && t < orTaken(i) + OR.PERIOD * (s + 1))[0] ?? null),
        holders,
        drain: !hold && raise && drain > 0 && t > drop && t < end ? 1 : 0,
        running: before(t) ? 1 : 0,
        sent: sent.filter((i) => orSeenIn(i) <= t),
        seen: seen.filter((i) => orSeenOut(i) <= t),
      });
    }
    return {
      raise, hold, drain, drop, end, cols,
      sent: sent.length, compared: seen.length, missing: sent.length - seen.length,
      passed: end === null ? null : sent.length === seen.length,
      lost: orItems((i) => sent.includes(i) && !seen.includes(i)),
    };
  };
  // The lines the run ends with: the scoreboard's two in check_phase, or the timeout's
  // three (tools/figures/q0113.py: sb_lines, timeout_lines), as [level, who, message].
  const orLog = (r) => (r.end === null
    ? [["CRITICAL", OR.TIMEOUT_SRC, `timeout at ${OR.LIMIT_US * 1000} ns`], ["", "", "Active objections:"], ["", "", ` raised by ${OR.HOLDER}, description=""`]]
    : [["INFO", OR.SB, `${r.end} ns: ${r.compared} compared, 0 mismatches, ${r.missing} missing`],
       r.passed ? ["INFO", OR.SB, "TEST PASSED"] : ["ERROR", OR.SB, "TEST FAILED"]]);
  const orText = (r) => orLog(r).map(([lvl, who, msg]) => (lvl ? `${lvl.padEnd(8)} [${who}] ${msg}` : msg)).join("\n");
  // the column in which the run ends (its sample counts, the end is at the rising edge after it)
  const orEndCol = (r) => (r.end === null ? null : r.end === 0 ? -1 : Math.floor(r.end / OR.PERIOD));

  // The box (0113): the test's objection and the monitor's as switches, the drain as a
  // slider; the transport over the 17 falling edges; the verdict of the run; the waveform
  // of what the monitors sample, the objections, the drain and the run phase, the time after
  // the end shaded, the line of the edge under the cursor and the lines the run ends with;
  // beside them on a computer (under them on a phone), the cards of that edge.
  const objrunView = () => ({
    mount(box) {
      const st = { raise: 1, hold: 0, drain: OR.DRAIN, k: OR.COLS - 1 };
      box.innerHTML =
        `<div class="ex-controls or-switches">` +
        `<label><input type="checkbox" class="or-raise" checked> <span>ה-test מרים objection סביב ה-sequence</span></label>` +
        `<label><input type="checkbox" class="or-hold"> <span>‏mon_out מרים objection ולא מוריד</span></label>` +
        `<label class="or-drainlab"><span>‏drain</span><input type="range" class="or-drain" min="0" max="${OR.DRAIN_MAX}" step="10" value="${OR.DRAIN}" dir="ltr" aria-label="זמן ה-drain, 0 עד ${OR.DRAIN_MAX} ns"><output class="or-drain-o" dir="ltr"></output></label></div>` +
        `<div class="ex-controls">` +
        `<button type="button" class="md-button ex-start">הירידה הראשונה</button>` +
        `<button type="button" class="md-button ex-prev">הירידה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הירידה הבאה</button>` +
        `<button type="button" class="md-button ex-end">160 ns</button>` +
        `<button type="button" class="md-button or-toend">לסוף הריצה</button>` +
        `<span class="ex-pos or-pos"></span></div>` +
        `<p class="ex-summary or-sum" aria-live="polite"></p>` +
        `<div class="wv-wrap or-strip" tabindex="0" role="group" aria-label="דיאגרמת התזמון של הריצה, 0 עד 160 ns, גלילה אופקית"></div>` +
        `<span class="viz-legend or-legend"><span><i class="or-key-after"></i>אחרי סוף הריצה${NB}: ה-DUT עוד מוציא, ואף מוניטור לא דוגם</span><span><i class="or-key-now"></i>הירידה של הכרטיסים</span></span>` +
        `<p class="wv-step or-now" aria-live="polite"></p>` +
        `<div class="or-cards">` +
        `<section class="or-card"><p class="or-ctitle">הצינור, אחרי העלייה הקודמת</p><div class="or-pipe" dir="ltr"></div></section>` +
        `<section class="or-card"><p class="or-ctitle">ה-objections</p><p class="or-obj"></p></section>` +
        `<section class="or-card"><p class="or-ctitle">מה המוניטורים שלחו ל-scoreboard</p><p class="or-sb"></p></section>` +
        `</div>` +
        `<section class="or-card or-logcard"><p class="or-ctitle">השורות שהריצה נגמרת בהן</p><pre class="or-log" dir="ltr" tabindex="0" role="region" aria-label="השורות שהריצה נגמרת בהן"></pre></section>`;
      const $ = (sel) => box.querySelector(sel);
      const SW = 25, LW = 84, LAST = OR.COLS - 1;
      let run = null;
      const ns = (t) => ltr(`${t} ns`);
      const chips = (items, cls = () => "") => (items.length ? items.map((i) => `<span class="or-chip${cls(i)}">${i}</span>`).join("") : `<span class="or-empty">—</span>`);
      const verdict = () => {
        if (run.end === null) {
          return `<span class="wv-bad">הריצה לא נגמרת</span>${NB}: ה-objection של ${code("mon_out")} לא יורד, כי הלולאה שלפני ההורדה אינסופית. ה-timeout עוצר אותה ב-${ltr(`${OR.LIMIT_US} µs`)}, ו-${code("check_phase")} לא רץ.`;
        }
        if (run.end === 0) {
          return `הריצה נגמרת ב-${ns(0)}${NB}: אף אחד לא הרים objection. ‏${code("check_phase")} רץ על scoreboard ריק, ו<span class="wv-bad">${code("TEST PASSED")}</span> בלי שנבדק אף פריט.`;
        }
        const counts = `נבדקו ${ltr(run.compared)}, ${run.missing ? `<span class="wv-bad">חסרים ${ltr(run.missing)}</span>` : "אין חסרים"}`;
        return `הריצה נגמרת ב-${ns(run.end)}${run.drain ? ` (ההורדה ב-${ns(run.drop)} ועוד drain של ${ns(run.drain)})` : ""}${NB}: ${counts}. ` +
          (run.passed ? `<span class="wv-ok">TEST PASSED</span>` : `<span class="wv-bad">TEST FAILED</span>${NB}: ה-drain צריך להיות יותר מ-${ns(orSeenOut(OR.N - 1) - run.drop)}.`);
      };
      const describe = (k) => {
        const c = run.cols[k], endCol = orEndCol(run);
        if (!c.running) return `ירידת השעון ב-${ns(c.t)}${NB}: הריצה כבר נגמרה ב-${ns(run.end)}, והסימולציה עצרה. מה שמסומן כאן לא קרה.`;
        const parts = [];
        if (c.in_item !== null) parts.push(`‏${code("mon_in")} רואה את פריט ${ltr(c.in_item)}`);
        if (c.out_item !== null) parts.push(`‏${code("mon_out")} רואה את פריט ${ltr(c.out_item)}`);
        let s = `ירידת השעון ב-${ns(c.t)}${NB}: ${parts.length ? `${parts.join(", ")}.` : "אף מוניטור לא רואה פריט."}`;
        const rise = c.t + OR.PERIOD / 2, after = [];
        const takes = orItems((i) => orTaken(i) === rise)[0];
        if (takes !== undefined) after.push(`ה-DUT לוקח את פריט ${ltr(takes)}`);
        if (run.drop === rise) after.push(`‏${code("seq.start")} חוזרת וה-test מוריד את ה-objection שלו`);
        if (k === endCol) after.push(`<span class="wv-bad">הריצה נגמרת</span>`);
        if (after.length) s += ` ב-${ns(rise)}${NB}: ${after.join(", ")}.`;
        return s;
      };
      const draw = () => {
        const k = st.k, c = run.cols[k], endCol = orEndCol(run);
        $(".or-drain-o").textContent = `${st.drain} ns`;
        $(".or-drain").disabled = !st.raise || st.hold;
        $(".or-drainlab").classList.toggle("is-off", !st.raise || st.hold);
        $(".or-pos").innerHTML = `ירידה ${k} מתוך ${LAST}, ${ns(c.t)}`;
        $(".ex-start").disabled = $(".ex-prev").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === LAST;
        $(".or-toend").disabled = endCol === null || endCol < 0 || k === endCol;
        $(".or-sum").innerHTML = verdict();
        const C = run.cols, after = C.map((w) => !w.running);
        const v = (f) => C.map(f);
        const rows = [
          { name: "rst_n", kind: "bit", values: v((w) => w.rst_n), cls: "wv-dim", marks: after },
          { name: "mon_in", kind: "bus", values: v((w) => (w.in_item === null ? "–" : w.in_item)), cls: "wv-s1", marks: after },
          { name: "mon_out", kind: "bus", values: v((w) => (w.out_item === null ? "–" : w.out_item)), cls: "wv-s2", marks: after },
          { name: "objections", kind: "bus", values: v((w) => w.holders.length), marks: after },
          { name: "drain", kind: "bit", values: v((w) => w.drain), cls: "wv-s2", marks: after },
          { name: "run_phase", kind: "bit", values: v((w) => w.running), cls: "wv-s1", marks: after },
        ];
        const strip = $(".or-strip");
        strip.innerHTML = waveStrip(rows, OR.COLS, { slotW: SW, labelW: LW, cursor: k, ticks: (j) => (j % 2 ? "" : OR.PERIOD * j), label: `דיאגרמת התזמון של הריצה, הסמן ב-${c.t} ns` });
        const x = LW + k * SW;
        if (strip.clientWidth > LW + 5 * SW) {
          if (x < strip.scrollLeft + LW) strip.scrollLeft = Math.max(0, x - LW - 2 * SW);
          else if (x + SW > strip.scrollLeft + strip.clientWidth) strip.scrollLeft = x + 3 * SW - strip.clientWidth;
        }
        $(".or-now").innerHTML = describe(k);
        // the cards: the stages after the rising edge before the cursor, the objections, the lists
        $(".or-pipe").innerHTML = c.stages.map((i, s) => `<span class="or-stage${c.running ? "" : " is-after"}"><small>v[${s}]</small><b>${i === null ? "–" : i}</b></span>`).join("");
        const who = c.holders.map((h) => code(h)).join(", ");
        let obj;
        if (!c.running) obj = run.end === 0 ? "אף אחד לא הרים, והריצה נגמרה ב-0." : "הריצה נגמרה.";
        else if (!c.holders.length) obj = c.drain ? `המונה 0, ו-UVM מחכה את ה-drain${NB}: עד ${ns(run.end)}.` : "המונה 0, וה-run phase נגמר.";
        else obj = `מורמים ${ltr(c.holders.length)}${NB}: ${who}.` + (run.hold ? ` ה-objection של ${code("mon_out")} יורד רק אחרי הלולאה האינסופית שלו.` : "");
        $(".or-obj").innerHTML = obj;
        const lost = new Set(run.lost), done = endCol !== null && k >= Math.max(endCol, 0);
        $(".or-sb").innerHTML = `נכנסו${NB}: <span class="or-chips" dir="ltr">${chips(c.sent, (i) => (lost.has(i) && done ? " is-lost" : ""))}</span><br>` +
          `יצאו${NB}: <span class="or-chips" dir="ltr">${chips(c.seen)}</span>`;
        $(".or-log").textContent = done ? orText(run) : run.end === null && k === LAST ? `… ${OR.LIMIT_US} µs\n${orText(run)}` : "—";
      };
      const reload = () => { run = orRun(st.raise, st.hold, st.drain); draw(); };
      $(".or-raise").addEventListener("change", (e) => { st.raise = e.target.checked ? 1 : 0; reload(); });
      $(".or-hold").addEventListener("change", (e) => { st.hold = e.target.checked ? 1 : 0; reload(); });
      const dr = $(".or-drain");
      dr.addEventListener("input", () => { const n = Number(dr.value); if (n >= 0 && n <= OR.DRAIN_MAX) { st.drain = n; reload(); } });
      const go = (k) => { st.k = Math.max(0, Math.min(LAST, k)); draw(); };
      $(".ex-start").addEventListener("click", () => go(0));
      $(".ex-prev").addEventListener("click", () => go(st.k - 1));
      $(".ex-next").addEventListener("click", () => go(st.k + 1));
      $(".ex-end").addEventListener("click", () => go(LAST));
      $(".or-toend").addEventListener("click", () => { const e = orEndCol(run); if (e !== null && e >= 0) go(e); });
      // a click anywhere in a column of the strip moves the cursor there
      $(".or-strip").addEventListener("click", (e) => {
        const svg = e.target.closest("svg.wave-strip");
        if (!svg) return;
        const j = Math.floor((e.clientX - svg.getBoundingClientRect().left - LW) / SW);
        if (j >= 0 && j < OR.COLS) go(j);
      });
      // the link and the remembered state: the cursor rides after the controls
      box.dvqExtra = {
        get: () => (st.k === LAST ? "" : String(st.k)),
        set: (text) => { const n = Number(text); if (!/^\d+$/.test(text) || n > LAST) return false; go(n); return true; },
      };
      reload();
    },
  });

  dvqExplorers.register({
    views: { objrun: objrunView },
    help: {
      objrun: "שני המתגים קובעים מי מרים objection : ה-test סביב ה-sequence, ו-mon_out בתחילת הלולאה האינסופית שלו. ה-drain הוא הזמן ש-UVM מחכה אחרי שהמונה מגיע ל-0. כל עמודה היא ירידת שעון, שבה המוניטורים דוגמים : mon_in ו-mon_out מראים את מספר הפריט שראו, והשורות שמתחתן את מספר ה-objections, את ה-drain ואת ה-run phase. מה שאחרי סוף הריצה מוצלל : ה-DUT עוד מוציא פריטים, אבל הסימולציה כבר עצרה. הכרטיסים מראים את הירידה המסומנת : מה יש בכל שלב של הצינור, מי מחזיק objection, ומה כל מוניטור שלח ל-scoreboard עד אז.",
    },
    models: { OR, orRun, orLog, orEndCol },
    cols: { objrun: { main: ".or-strip, .or-legend, .or-now, .or-logcard", side: ".or-cards", w: "minmax(0, 1.9fr)" } },
  });
})();
