// kinds: edgerace
//   edgerace               0115        the monitor race at the clock edge: the language, the driver's write, the monitor's sampling and the order of the processes as selects; the ten cycles stepped event by event, each edge taken apart into its scheduling regions with what every process reads and writes there, the values of in and out, and the scoreboard's verdict of every cycle
// Loaded after core.js on the page of question 0115 (hooks/questions.py adds the script
// tag); under Node tools/explorer_node.js loads every kind file and merges the models for
// the question tests (tests/0115/test_0115_box.py compares them with tools/figures/q0115.py).
(() => {
  const { autoplay, code, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";                                   // before a Hebrew colon

  // --- the model, as tools/figures/q0115.py ---------------------------------------------------

  // The page's stimulus, the edges the model runs and the cycles the box shows.
  const ER = { V: [1, 1, 1, 0, 0, 1, 1, 1, 0, 0], D: [5, 9, 9, 9, 9, 2, 6, 6, 6, 6], EDGES: 12, CYCLES: 10 };
  // The choices: the driver (= at the rising edge, <=, a clocking block's output #0, = at the
  // falling edge; in cocotb Immediate or a plain write), the monitor (at the rising edge or
  // right after RisingEdge, a clocking block's input #1step or #0, ReadOnly(), the falling
  // edge) and the order of the monitor (m), the driver (d) and the DUT's always_ff (x) in the
  // edge's Active region. Verilator runs the DUT last; the orders with the DUT first are what
  // another simulator may do.
  const ER_DRIVERS = { sv: ["blk", "nba", "cb", "neg"], py: ["imm", "dep"] };
  const ER_MONITORS = { sv: ["edge", "s1", "s0", "neg"], py: ["edge", "ro", "neg"] };
  const ER_ORDERS = { sv: ["mdx", "dmx", "xmd", "xdm"], py: ["mdx", "dmx"] };
  const ER_VERILATOR = ["mdx", "dmx"];

  // [the DUT takes the new row, the monitor reads the new input, the monitor reads the
  // output after the edge's update] (q0115.view_of)
  const erView = (lang, drv, mon, order) => {
    const at = (p) => order.indexOf(p);
    const active = drv === "blk" || drv === "imm";
    const dutNew = active && at("d") < at("x") ? 1 : 0;
    let monNew;
    if (mon === "edge") monNew = active && at("d") < at("m") ? 1 : 0;
    else if (mon === "s1") monNew = 0;
    else if (mon === "s0") monNew = drv === "blk" || drv === "nba" ? 1 : 0;
    else if (mon === "ro") monNew = 1;
    else monNew = drv !== "neg" || at("d") < at("m") ? 1 : 0;
    return [dutNew, monNew, ["s0", "ro", "neg"].includes(mon) ? 1 : 0];
  };
  const erRow = (i) => (i < 0 ? [0, 0] : [ER.V[Math.min(i, ER.V.length - 1)], ER.D[Math.min(i, ER.D.length - 1)]]);
  const plus1 = (r) => [r[0], (r[1] + 1) % 256];
  const erItem = (r) => (r[0] ? String(r[1]) : "none");
  // edge by edge (q0115.run): what the monitor read, what the DUT took, what the monitor
  // expected and got; out[k] is the output after edge k
  const erRun = ([dutNew, monNew, after]) => {
    const out = [[0, 0]];
    for (let k = 1; k <= ER.EDGES; k++) out.push(plus1(erRow(dutNew ? k - 1 : k - 2)));
    let exp = [0, 0];
    const edges = [], mismatches = [];
    for (let k = 1; k <= ER.EDGES; k++) {
      const read = erRow(monNew ? k - 1 : k - 2), got = after ? out[k] : out[k - 1];
      const bad = got[0] !== exp[0] || (exp[0] === 1 && got[1] !== exp[1]);
      edges.push({ k, read, took: erRow(dutNew ? k - 1 : k - 2), exp, got, bad });
      if (bad) mismatches.push([k, exp, got]);
      exp = plus1(read);
    }
    return { edges, mismatches, out };
  };

  // The regions of an edge, as the box shows them: SystemVerilog's, and cocotb's phases on
  // Verilator (the coroutines run right after RisingEdge, before the DUT's always_ff).
  const ER_REGIONS = {
    sv: ["Preponed", "Active", "NBA", "Observed", "Re-NBA", "negedge"],
    py: ["RisingEdge", "NBA", "ReadWrite", "ReadOnly", "FallingEdge"],
  };
  // The events of edge k, in the order they happen: { k, reg, who, act, val } with who m
  // (the monitor), d (the driver), x (the DUT) or c (the clocking block); act read (the
  // monitor samples: val the input, out the output, exp and bad its verdict), write (in
  // takes val), sched (the driver hands val on, to be written later), take (the DUT's
  // always_ff reads val) and update (out takes val).
  const erEvents = (lang, drv, mon, order, k, run) => {
    const [dutNew, monNew, after] = erView(lang, drv, mon, order);
    const e = run.edges[k - 1], nw = erRow(k - 1);
    const took = dutNew ? nw : erRow(k - 2);
    const read = (reg) => ({ k, reg, who: "m", act: "read", val: monNew ? nw : erRow(k - 2), out: after ? run.out[k] : run.out[k - 1], exp: e.exp, bad: e.bad });
    const ev = [];
    const procs = (reg, list) => [...order].forEach((p) => { const x = list[p]; if (x) ev.push({ k, reg, ...x }); });
    if (lang === "sv") {
      if (mon === "s1") ev.push(read(0));
      const d = drv === "blk" ? { who: "d", act: "write", val: nw } : drv === "nba" || drv === "cb" ? { who: "d", act: "sched", val: nw } : null;
      procs(1, { m: mon === "edge" ? read(1) : null, d, x: { who: "x", act: "take", val: took } });
      ev.push({ k, reg: 2, who: "x", act: "update", val: run.out[k] });
      if (drv === "nba") ev.push({ k, reg: 2, who: "d", act: "write", val: nw });
      if (mon === "s0") ev.push(read(3));
      if (drv === "cb") ev.push({ k, reg: 4, who: "c", act: "write", val: nw });
      procs(5, { m: mon === "neg" ? read(5) : null, d: drv === "neg" ? { who: "d", act: "write", val: nw } : null });
    } else {
      procs(0, { m: mon === "edge" ? read(0) : null, d: { who: "d", act: drv === "imm" ? "write" : "sched", val: nw } });
      ev.push({ k, reg: 0, who: "x", act: "take", val: took });
      ev.push({ k, reg: 1, who: "x", act: "update", val: run.out[k] });
      if (drv === "dep") ev.push({ k, reg: 2, who: "c", act: "write", val: nw });
      if (mon === "ro") ev.push(read(3));
      if (mon === "neg") ev.push(read(4));
    }
    return ev;
  };
  // every event of the cycles the box shows, and the values of in and out after each
  const erSteps = (lang, drv, mon, order) => {
    const run = erRun(erView(lang, drv, mon, order));
    const steps = [];
    let inp = [0, 0], out = [0, 0];
    for (let k = 1; k <= ER.CYCLES; k++) {
      for (const e of erEvents(lang, drv, mon, order, k, run)) {
        if (e.act === "write") inp = e.val;
        if (e.act === "update") out = e.val;
        steps.push({ ...e, in: inp, outNow: out });
      }
    }
    return { run, steps };
  };

  // --- the box ----------------------------------------------------------------------------

  const OPTS = {
    drv: {
      sv: [["blk", "חוסמת (=) בעלייה, כמו שנמצא"], ["nba", "לא חוסמת (<=) בעלייה"], ["cb", "דרך clocking block"], ["neg", "חוסמת (=) בירידה"]],
      py: [["imm", "ב-Immediate, כמו שנמצא"], ["dep", "כתיבה רגילה"]],
    },
    mon: {
      sv: [["edge", "בעלייה, כמו שנמצא"], ["s1", "דרך clocking block, ‏#1step"], ["s0", "דרך clocking block, ‏#0"], ["neg", "בירידה"]],
      py: [["edge", "אחרי RisingEdge, כמו שנמצא"], ["ro", "ב-ReadOnly, אחרי הקצה"], ["neg", "ב-FallingEdge"]],
    },
    ord: {
      sv: [["mdx", "‏monitor, driver, DUT"], ["dmx", "‏driver, monitor, DUT"], ["xmd", "‏DUT, monitor, driver"], ["xdm", "‏DUT, driver, monitor"]],
      py: [["mdx", "ה-monitor ראשון, כמו שנמצא"], ["dmx", "ה-driver ראשון"]],
    },
  };
  const WHAT = { drv: "ה-driver", mon: "ה-monitor", ord: "הסדר" };
  const ARIA = {
    drv: "איך ה-driver כותב את הכניסות",
    mon: "מתי ה-monitor דוגם",
    ord: "הסדר של התהליכים באזור ה-Active של הקצה",
  };
  const REG_NAME = { negedge: "ירידה" };
  const pair = (name, r) => code(`${name} = ${erItem(r)}`);

  // the event in words, and why
  const say = (e, st) => {
    const { lang, drv, mon } = st, v = erItem(e.val), view = erView(lang, drv, mon, st.order);
    const blocking = drv === "blk" || drv === "imm";
    if (e.act === "read") {
      const verdict = e.bad ? `<span class="wv-bad">✗ ציפה ל-${code(erItem(e.exp))}</span>` : `<span class="wv-ok">✓</span>`;
      let why;
      if (mon === "s1") why = "‏#1step דוגם את מה שהיה לפני הקצה";
      else if (mon === "s0") why = `‏#0 דוגם ב-Observed, אחרי ה-NBA${drv === "cb" ? ", לפני הדחיפה של drv_cb" : ""}`;
      else if (mon === "ro") why = "‏ReadOnly רואה הכול אחרי הקצה";
      else if (mon === "neg") why = drv === "neg" ? `בירידה, ${view[1] ? "אחרי" : "לפני"} שה-driver כותב בה` : "בירידה הכול כבר אחרי הקצה";
      else if (blocking) why = st.order.indexOf("d") < st.order.indexOf("m") ? "הוא רץ אחרי ה-driver ורואה את הכתיבה" : "הוא רץ לפני ה-driver ורואה את הישן";
      else why = "הכתיבה של הקצה עוד לא הגיעה";
      return `ה-monitor קורא ${pair("in", e.val)} ו-${pair("out", e.out)}, ${why}. מצפה ל-${code(erItem(e.exp))}${NB}: ${verdict}`;
    }
    if (e.act === "take") {
      const nw = view[0] === 1;
      return `ה-${code("always_ff")} של ה-DUT קורא ${pair("in", e.val)}${nw ? ", שה-driver כתב לפניו באותו קצה" : ", מה שהיה לפני הקצה"}.`;
    }
    if (e.act === "update") return `ה-NBA של ה-DUT${NB}: ${pair("out", e.val)}, מה שה-DUT לקח ועוד 1.`;
    if (e.act === "sched") {
      if (drv === "nba") return `ה-driver מתזמן ${code(`in <= ${v}`)}${NB}: הכתיבה תקרה ב-NBA.`;
      if (drv === "cb") return `ה-driver כותב ${code(v)} ל-${code("drv_cb")}${NB}: הדחיפה תקרה ב-Re-NBA.`;
      return `ה-driver כותב ${code(v)} בכתיבה רגילה${NB}: היא נכנסת לתור, עד ה-ReadWrite.`;
    }
    if (e.who === "c") return lang === "sv" ? `ה-clocking block דוחף ${pair("in", e.val)}, אחרי שכל הקוראים קראו.` : `‏cocotb מחיל את הכתיבה מהתור${NB}: ${pair("in", e.val)}.`;
    if (drv === "nba") return `ה-NBA של ה-driver${NB}: ${pair("in", e.val)}.`;
    if (drv === "neg") return `ה-driver כותב ${pair("in", e.val)} בירידה, חצי מחזור לפני העלייה הבאה.`;
    return `ה-driver כותב ${pair("in", e.val)}${drv === "imm" ? " ב-Immediate" : ""}, מיד, באמצע ${lang === "sv" ? "ה-Active" : "הקצה"}.`;
  };
  // the short text of an event on its chip
  const chip = (e, later) => {
    const who = { m: "monitor", d: "driver", x: "DUT", c: "" }[e.who];
    const v = erItem(e.val);
    const body = e.act === "read" ? `${code(`in ${v}`)} ${code(`out ${erItem(e.out)}`)} ${later ? "?" : e.bad ? "✗" : "✓"}`
      : e.act === "take" ? `קורא ${code(`in ${v}`)}`
      : e.act === "update" ? code(`out = ${v}`)
      : e.act === "sched" ? `מעביר ${code(v)}`
      : code(`in = ${v}`);
    const name = e.who === "c" ? (e.reg === 4 ? "drv_cb" : "התור") : who;
    return `<span class="er-who" dir="ltr">${name}</span> ${body}`;
  };

  const edgeraceView = () => ({
    mount(box) {
      const st = { lang: "sv", drv: { sv: "blk", py: "imm" }, mon: { sv: "edge", py: "edge" }, ord: { sv: "mdx", py: "mdx" }, s: 0 };
      const sel = (what, lang) => `<label class="er-${lang}"${lang === "py" ? " hidden" : ""}>${WHAT[what]} <select class="er-${what}-${lang}" aria-label="${ARIA[what]}">` +
        OPTS[what][lang].map(([v, t]) => `<option value="${v}">${t}</option>`).join("") + `</select></label>`;
      box.innerHTML =
        `<div class="ex-controls er-pick">` +
        `<label>הסביבה <select class="er-lang" aria-label="SystemVerilog או cocotb"><option value="sv">SystemVerilog</option><option value="py">cocotb</option></select></label>` +
        ["drv", "mon", "ord"].map((w) => sel(w, "sv") + sel(w, "py")).join("") + `</div>` +
        `<div class="ex-controls">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">האירוע הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<button type="button" class="md-button md-button--primary ex-next">האירוע הבא</button>` +
        `<button type="button" class="md-button ex-end">הסוף</button>` +
        `<button type="button" class="md-button er-tobad">לשגיאה הבאה</button>` +
        `<span class="ex-pos er-pos"></span></div>` +
        `<p class="ex-summary er-sum" aria-live="polite"></p>` +
        `<div class="er-cycles" role="group" aria-label="עשרת המחזורים והפסיקה של ה-monitor בכל אחד"></div>` +
        `<p class="er-now" aria-live="polite"></p>` +
        `<section class="er-edge" data-steady><p class="er-etitle"></p><ol class="er-regions"></ol></section>` +
        `<section class="er-vals"><p class="er-ctitle">האותות אחרי האירוע</p><table class="er-tab"><tbody></tbody></table>` +
        `<p class="er-ctitle">מה כל אחד ראה בקצה</p><p class="er-saw"></p></section>`;
      const $ = (q) => box.querySelector(q);
      let model = null;
      const cfg = () => ({ lang: st.lang, drv: st.drv[st.lang], mon: st.mon[st.lang], order: st.ord[st.lang] });
      const compute = () => { const c = cfg(); model = erSteps(c.lang, c.drv, c.mon, c.order); };
      const T = () => model.steps.length;
      const cycleOf = () => (st.s === 0 ? 1 : model.steps[st.s - 1].k);
      const summary = () => {
        const c = cfg(), bad = model.run.mismatches.filter(([k]) => k <= ER.CYCLES).map(([k]) => k);
        const ran = c.lang === "py" ? "כך גם בריצה של cocotb 2.1 על Verilator 5.053."
          : ER_VERILATOR.includes(c.order) ? "כך גם בריצה על Verilator 5.053 (הטסטים של השאלה)."
          : `סדר שהתקן מתיר ו-Verilator לא מריץ${NB}: לפי המודל.`;
        const n = bad.length;
        const head = n ? `<span class="wv-bad">${n === 1 ? "שגיאה אחת" : `${ltr(n)} שגיאות`}</span>, ${n === 1 ? "במחזור" : "במחזורים"} ${bad.length > 1 ? `${bad.slice(0, -1).join(", ")} ו-${bad[n - 1]}` : bad[0]}`
          : `<span class="wv-ok">0 שגיאות</span>`;
        return `בעשרת המחזורים${NB}: ${head}. ${ran}`;
      };
      const draw = () => {
        const c = cfg(), steps = model.steps, n = T(), s = st.s, k = cycleOf();
        box.querySelectorAll(".er-sv").forEach((el) => { el.hidden = c.lang !== "sv"; });
        box.querySelectorAll(".er-py").forEach((el) => { el.hidden = c.lang !== "py"; });
        $(".er-pos").textContent = `אירוע ${s} מתוך ${n}`;
        $(".ex-start").disabled = $(".ex-prev").disabled = s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = s === n;
        const nextBad = steps.findIndex((e, i) => i >= s && e.act === "read" && e.bad);
        $(".er-tobad").disabled = nextBad < 0;
        $(".er-sum").innerHTML = summary();
        // the cycles: the verdict of every cycle the monitor has compared by now
        $(".er-cycles").innerHTML = Array.from({ length: ER.CYCLES }, (_, i) => {
          const kk = i + 1, at = steps.findIndex((e) => e.k === kk && e.act === "read"), done = at >= 0 && at < s;
          const e = steps[at], mark = done ? (e.bad ? "✗" : "✓") : "";
          const label = `מחזור ${kk}${done ? (e.bad ? `${NB}: שגיאה, ציפה ל-${erItem(e.exp)} וקיבל ${erItem(e.out)}` : `${NB}: תקין`) : ""}`;
          return `<button type="button" class="er-cyc${done ? (e.bad ? " is-bad" : " is-ok") : ""}${kk === k ? " is-now" : ""}" data-k="${kk}" aria-label="${label}, לחיצה עוברת לקצה שלו"><b>${kk}</b><span>${mark || NB}</span></button>`;
        }).join("");
        const cur = s > 0 ? steps[s - 1] : null;
        $(".er-now").innerHTML = cur ? `<b>מחזור ${ltr(k)}, ${ER_REGIONS[c.lang][cur.reg] === "negedge" ? "הירידה" : code(ER_REGIONS[c.lang][cur.reg])}${NB}:</b> ${say(cur, c)}`
          : `לפני הקצה הראשון${NB}: ${code("in = none")} ו-${code("out = none")}. ״האירוע הבא״ מתחיל את הקצה של מחזור 1.`;
        // the edge of the cycle, region by region: the events before the current one, the current one, the ones still to come
        const mine = steps.map((e, i) => [e, i]).filter(([e]) => e.k === k);
        $(".er-etitle").innerHTML = `הקצה של מחזור ${ltr(k)}, לפי האזורים${c.lang === "py" ? " (cocotb על Verilator)" : ""}`;
        $(".er-regions").innerHTML = ER_REGIONS[c.lang].map((name, r) => {
          const evs = mine.filter(([e]) => e.reg === r);
          const chips = evs.length ? evs.map(([e, i]) => `<span class="er-chip${i === s - 1 ? " is-now" : i >= s ? " is-later" : ""}${e.act === "read" && e.bad ? " is-bad" : ""}">${chip(e, i >= s)}</span>`).join("")
            : `<span class="er-none">—</span>`;
          return `<li class="er-reg"><span class="er-rname">${REG_NAME[name] || `<span dir="ltr">${name}</span>`}</span><span class="er-evs">${chips}</span></li>`;
        }).join("");
        // the values after the event, and what each one saw in this edge so far
        const inNow = cur ? cur.in : [0, 0], outNow = cur ? cur.outNow : [0, 0];
        $(".er-tab tbody").innerHTML = [["in_valid", inNow[0]], ["in_data", inNow[1]], ["out_valid", outNow[0]], ["out_data", outNow[1]]]
          .map(([nm, v]) => `<tr><th scope="row" dir="ltr">${nm}</th><td dir="ltr">${v}</td></tr>`).join("");
        const seen = mine.filter(([, i]) => i < s).map(([e]) => e);
        const rd = seen.find((e) => e.act === "read"), tk = seen.find((e) => e.act === "take");
        $(".er-saw").innerHTML = `ה-monitor${NB}: ${rd ? `${pair("in", rd.val)}, ${pair("out", rd.out)}` : "עוד לא קרא"}.<br>ה-DUT${NB}: ${tk ? pair("in", tk.val) : "עוד לא קרא"}.`;
      };
      const go = (s) => { st.s = Math.max(0, Math.min(T(), s)); draw(); };
      let stop = () => {};
      const reload = () => {
        const old = model ? T() : 0;
        compute();
        if (old) st.s = Math.round((st.s * T()) / old);   // the same place on the timeline (core's keep does the same)
        go(st.s);
      };
      $(".er-lang").addEventListener("change", (e) => { stop(); st.lang = e.target.value; reload(); });
      for (const w of ["drv", "mon", "ord"]) {
        for (const lang of ["sv", "py"]) {
          $(`.er-${w}-${lang}`).addEventListener("change", (e) => { stop(); st[w][lang] = e.target.value; reload(); });
        }
      }
      $(".ex-start").addEventListener("click", () => { stop(); go(0); });
      $(".ex-prev").addEventListener("click", () => { stop(); go(st.s - 1); });
      $(".ex-next").addEventListener("click", () => { stop(); go(st.s + 1); });
      $(".ex-end").addEventListener("click", () => { stop(); go(T()); });
      $(".er-tobad").addEventListener("click", () => {
        stop();
        const i = model.steps.findIndex((e, j) => j >= st.s && e.act === "read" && e.bad);
        if (i >= 0) go(i + 1);
      });
      $(".er-cycles").addEventListener("click", (e) => {
        const b = e.target.closest(".er-cyc");
        if (!b) return;
        stop();
        go(model.steps.findIndex((x) => x.k === Number(b.dataset.k)));   // just before the edge's first event
      });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => go(st.s + 1), done: () => st.s >= T(), restart: () => go(0) });
      box.dvqExtra = {
        get: () => (st.s ? String(st.s) : ""),
        set: (text) => { const v = Number(text); if (!/^\d+$/.test(text) || v > T()) return false; go(v); return true; },
      };
      compute();
      draw();
    },
  });

  dvqExplorers.register({
    views: { edgerace: edgeraceView },
    help: {
      edgerace: `הבוררים הם הסביבה של השאלה${NB}: SystemVerilog או cocotb, איך ה-driver כותב, מתי ה-monitor דוגם, ובאיזה סדר רצים ה-monitor, ה-driver וה-${code("always_ff")} של ה-DUT באזור ה-Active של הקצה. ‏Verilator מריץ את ה-DUT אחרי שני התהליכים, בסדר שבו התחילו לחכות${NB}: הסדרים שבהם ה-DUT ראשון הם מה שסימולטור אחר רשאי לעשות. החצים, ״הפעלה״ או המקשים ← → עוברים על עשרת המחזורים אירוע אחרי אירוע. הרשימה מפרקת את הקצה של המחזור לאזורים${NB}: האירוע הנוכחי מסומן, והבאים בהירים. המשבצות של המחזורים מראות את הפסיקה של ה-monitor בכל מחזור שכבר נבדק, ולחיצה על משבצת עוברת לקצה שלו.`,
    },
    // the cycles, the event and the edge on the left; the values of the signals beside them
    cols: { edgerace: { side: ".er-vals", w: "minmax(0, 1.6fr)" } },
    models: { ER, ER_DRIVERS, ER_MONITORS, ER_ORDERS, ER_VERILATOR, ER_REGIONS, erView, erRow, erRun, erEvents, erSteps },
  });
})();
