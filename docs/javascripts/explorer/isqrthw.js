// kinds: isqrthw
//   isqrthw                0097        the sequential module of part c (data-n): isqrt_seq on a 16-bit n, stepped cycle by cycle from the start cycle (step / play); the block diagram of the page with this cycle's values on its blocks and wires (the registers k, root and rem, the trial shifter, the 17-bit subtractor and its borrow, fits = !borrow, the decoder of root[k], the multiplexer into rem, the control) and the path the cycle takes lit; a table of every signal, a column per cycle, the cycle of the moment marked; buttons for the trap inputs
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = "\u00a0";
  const MAX = 65535, CYCLES = 11;

  // --- the model, as tools/figures/q0097.py hw_cycles ---------------------------------------
  // One record per cycle (rising edge to rising edge), cycle 0 the one with start high: the
  // registers through the cycle (null before the load), the combinational trial, diff, borrow
  // and fits while busy, load = start & !busy, the bit the decoder sets, and the registers the
  // edge at the end of the cycle writes (nk, nroot, nrem, nbusy, ndone).
  const isqhwTrace = (n, cycles = CYCLES) => {
    const out = [];
    let k = null, root = null, rem = null, busy = 0, done = 0;
    for (let c = 0; c < cycles; c++) {
      const start = c === 0 ? 1 : 0, load = start && !busy ? 1 : 0;
      const rec = { cycle: c, start, load, k, root, rem, busy, done, trial: null, diff: null, borrow: null, fits: null, set: null };
      let nk = k, nroot = root, nrem = rem, nbusy = busy, ndone = 0;
      if (load) { nk = 7; nroot = 0; nrem = n; nbusy = 1; }
      else if (busy) {
        const trial = root * 2 ** (k + 1) + 2 ** (2 * k), borrow = trial > rem ? 1 : 0;   // the two never share a bit: OR = +
        Object.assign(rec, { trial, diff: rem - trial, borrow, fits: 1 - borrow });
        if (!borrow) { nrem = rem - trial; nroot = root + 2 ** k; rec.set = k; }
        if (k === 0) { nbusy = 0; ndone = 1; } else nk = k - 1;
      }
      Object.assign(rec, { nk, nroot, nrem, nbusy, ndone });
      out.push(rec);
      [k, root, rem, busy, done] = [nk, nroot, nrem, nbusy, ndone];
    }
    return out;
  };

  // --- the block diagram, as tools/figures/q0097.py DP_BLOCKS and DP_WIRES ----------------------
  const BLOCKS = [
    ["k", 10, 14, 70, 44, "reg", "k"], ["root", 118, 14, 130, 44, "reg", "root"], ["rem", 284, 14, 108, 44, "reg", "rem"],
    ["shift", 118, 92, 126, 44, "mux", "trial"], ["sub", 284, 92, 108, 44, "stage", "rem − trial"],
    ["dec", 118, 166, 124, 44, "mux", "decoder"], ["fits", 278, 166, 92, 40, "ctl", "fits"],
    ["ctl", 10, 246, 238, 44, "ctl", "control"], ["mux", 284, 246, 108, 44, "mux", "rem mux"],
  ];
  const WIRES = [
    ["k_ctl", [[28, 58], [28, 246]], "k", 32, 232, "start"],
    ["ctl_k", [[62, 246], [62, 58]], "k − 1", 66, 232, "start"],
    ["k_dec", [[80, 36], [92, 36], [92, 180], [118, 180]]],
    ["k_sh", [[146, 74], [146, 92]], "k", 152, 84, "start"],
    ["root_sh", [[183, 58], [183, 92]]],
    ["sh_sub", [[244, 114], [284, 114]], "trial", 264, 105, "middle"],
    ["rem_sub", [[338, 58], [338, 92]]],
    ["borrow", [[304, 136], [304, 166]], "borrow", 299, 155, "end"],
    ["fits_dec", [[278, 194], [242, 194]], "fits", 260, 188, "middle"],
    ["fits_mux", [[316, 206], [316, 246]], "fits", 312, 232, "end"],
    ["diff", [[382, 136], [382, 246]], "diff", 378, 232, "end"],
    ["mux_rem", [[392, 268], [401, 268], [401, 36], [392, 36]]],
    ["dec_root", [[146, 166], [146, 150], [104, 150], [104, 66], [128, 66], [128, 58]]],
    ["ctl_dec", [[183, 246], [183, 210]], "load, busy", 187, 232, "start"],
    ["ctl_mux", [[248, 268], [284, 268]]],
    ["start", [[56, 318], [56, 290]], "start", 56, 332, "middle"],
    ["out", [[170, 290], [170, 318]], "busy, done", 170, 332, "middle"],
    ["n", [[338, 318], [338, 290]], "n", 338, 332, "middle"],
  ];
  const bin8 = (v) => v.toString(2).padStart(8, "0");
  const dash = (v) => (v == null ? "–" : String(v));
  // the blocks and wires this cycle uses: the load, a step (with or without the fit), the done cycle
  const isqhwLit = (c) => {
    const b = new Set(), w = new Set();
    if (!c) return { blocks: b, wires: w };
    if (c.load) {
      ["ctl", "k", "root", "rem", "mux", "dec"].forEach((x) => b.add(x));
      ["start", "ctl_k", "ctl_dec", "ctl_mux", "n", "mux_rem", "dec_root"].forEach((x) => w.add(x));
    } else if (c.busy) {
      ["k", "root", "rem", "shift", "sub", "fits", "ctl"].forEach((x) => b.add(x));
      ["k_sh", "root_sh", "sh_sub", "rem_sub", "borrow", "fits_dec", "fits_mux", "k_ctl", "ctl_k", "ctl_dec", "ctl_mux"].forEach((x) => w.add(x));
      if (c.fits) {
        ["dec", "mux"].forEach((x) => b.add(x));
        ["k_dec", "dec_root", "diff", "mux_rem"].forEach((x) => w.add(x));
      }
      if (c.ndone) w.add("out");
    } else if (c.done) { b.add("ctl"); w.add("out"); }
    return { blocks: b, wires: w };
  };
  // the second line of each block and the text of each labelled wire, this cycle
  const values = (c) => {
    if (!c) return { blocks: {}, wires: {} };
    const busy = c.busy && !c.load;
    const ctl = c.load ? "load: k ← 7, busy ← 1" : busy ? (c.ndone ? "k = 0: busy ← 0, done ← 1" : `busy = 1, k ← ${c.nk}`)
      : c.done ? "done = 1" : c.start ? "" : "idle";
    return {
      blocks: {
        k: dash(c.k), root: c.root == null ? "–" : `${bin8(c.root)} = ${c.root}`, rem: dash(c.rem),
        shift: busy ? `= ${c.trial}` : "–",
        sub: busy ? (c.borrow ? "diff < 0" : `diff = ${c.diff}`) : "–",
        fits: busy ? `= ${c.fits}` : "–",
        dec: c.load ? "root ← 0" : busy && c.fits ? `root[${c.k}] ← 1` : "–",
        mux: c.load ? `rem ← ${c.nrem}` : busy ? (c.fits ? `rem ← ${c.nrem}` : "rem ← rem") : "–",
        ctl,
      },
      wires: {
        borrow: busy ? `borrow = ${c.borrow}` : "borrow", start: `start = ${c.start}`,
        out: `busy, done = ${c.busy}, ${c.done}`,
      },
    };
  };
  // the diagram with this cycle's values (null: the page's names)
  const isqhwDiagram = (c, n = null) => {
    const lit = isqhwLit(c), val = values(c);
    let g = `<svg class="isq-fig isq-dp isq-live-dp" viewBox="0 0 410 346" direction="ltr" role="img" aria-label="תרשים המלבנים של isqrt_seq עם הערכים של המחזור הזה">` +
      '<defs><marker id="isq-hd" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="isq-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>';
    BLOCKS.forEach(([id, x, y, w, h, cls, title]) => {
      g += `<g class="isq-blk isq-${cls}${lit.blocks.has(id) ? " is-on" : ""}" data-b="${id}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5"/>` +
        `<text x="${x + w / 2}" y="${y + h / 2 - 3}" text-anchor="middle">${title}</text>` +
        `<text class="isq-val" x="${x + w / 2}" y="${y + h / 2 + 13}" text-anchor="middle">${val.blocks[id] ?? ""}</text></g>`;
    });
    WIRES.forEach(([id, pts, lab, lx, ly, anchor]) => {
      g += `<path class="isq-wire${lit.wires.has(id) ? " is-on" : ""}" d="M${pts.map(([a, b]) => `${a},${b}`).join(" L")}" marker-end="url(#isq-hd)"/>`;
      if (lab) {
        const text = id === "n" && n != null ? `n = ${n}` : val.wires[id] ?? lab;
        g += `<text class="isq-wlab" x="${lx}" y="${ly}" text-anchor="${anchor}">${text}</text>`;
      }
    });
    return g + "</svg>";
  };

  // --- the box -----------------------------------------------------------------------------------

  const ROWS = [["start", (c) => c.start], ["busy", (c) => c.busy], ["k", (c) => dash(c.k)], ["trial", (c) => dash(c.trial)],
    ["borrow", (c) => dash(c.borrow)], ["fits", (c) => dash(c.fits)], ["root", (c) => dash(c.root)], ["rem", (c) => dash(c.rem)], ["done", (c) => c.done]];
  const FLAGS = new Set(["start", "busy", "fits", "done"]);
  const wave = (tr, t) => {
    let s = `<table class="isq-wave"><thead><tr><th scope="col">מחזור</th>${tr.map((c) => `<th scope="col"${c.cycle === t ? ' class="is-now"' : ""}>${c.cycle}</th>`).join("")}</tr></thead><tbody>`;
    ROWS.forEach(([name, f]) => {
      s += `<tr><th scope="row">${name}</th>` + tr.map((c) => {
        const shown = c.cycle <= t, v = shown ? f(c) : "";
        const cls = [c.cycle === t ? "is-now" : "", shown ? "" : "is-fut", FLAGS.has(name) && v === 1 ? "is-hi" : ""].filter(Boolean).join(" ");
        return `<td${cls ? ` class="${cls}"` : ""}>${v}</td>`;
      }).join("") + "</tr>";
    });
    return s + "</tbody></table>";
  };
  // the trap inputs: the largest, a trial equal to the remainder, one before a square, zero
  const TRAPS = [[65535, "65535, הגדול ביותר"], [4096, ltr("4096 = 64²")], [4095, ltr("4095 = 64² − 1")], [0, "0"]];

  const isqrthwView = () => ({
    mount(box) {
      const N0 = Math.min(MAX, Math.max(0, Math.floor(Number(box.dataset.n ?? 1000)) || 0));
      const st = { n: N0, t: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>${ltr("n")}</span><input type="number" class="ex-num isqh-n" data-nolink min="0" max="${MAX}" step="1" value="${N0}" dir="ltr" inputmode="numeric" aria-label="n, מספר של 16 ביטים"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה ל-${ltr(N0)} של העמוד</button>` +
        TRAPS.map(([v, t]) => `<button type="button" class="md-button ex-preset isqh-trap" data-v="${v}">מקרה מלכודת${NB}: ${t}</button>`).join("") +
        `<span class="fl-err isqh-err" aria-live="polite"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">המחזור הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">המחזור הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 300) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary isqh-sum" aria-live="polite"></p>` +
        `<div class="isqh-dpwrap"></div>` +
        `<div class="isqh-wavewrap" dir="ltr" tabindex="0" role="region" aria-label="כל האותות, עמודה לכל מחזור"></div>` +
        `<p class="isqh-note" aria-live="polite"></p>` +
        `<span class="viz-legend"><span><i class="isq-key-on"></i>הנתיב של המחזור הזה</span><span><i class="isq-key-now"></i>המחזור של הרגע</span>` +
        `<span><i class="isq-key-hi"></i>אות דולק</span></span>`;
      const $ = (sel) => box.querySelector(sel);
      const input = $(".isqh-n");
      const trace = () => isqhwTrace(st.n);

      const draw = () => {
        const tr = trace(), T = tr.length - 1;
        st.t = Math.max(0, Math.min(st.t, T));
        if (document.activeElement !== input) input.value = String(st.n);
        $(".ex-pos").textContent = `מחזור ${st.t} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.t === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.t === T;
        const c = tr[st.t];
        $(".isqh-dpwrap").innerHTML = isqhwDiagram(c, st.n);
        const wv = $(".isqh-wavewrap");
        wv.innerHTML = wave(tr, st.t);
        const cur = wv.querySelector("th.is-now");
        if (cur) wv.scrollLeft = Math.max(0, cur.offsetLeft - wv.clientWidth / 2);
        const end = tr.find((x) => x.done);
        $(".isqh-sum").innerHTML = `${ltr(`n = ${st.n}`)}${NB}: ‏${ltr("busy")} במחזורים 1 עד 8, ביט אחד של השורש בכל מחזור, ו-${ltr("done")} במחזור ${ltr(end.cycle)}.`;
        let note;
        const K = ltr(`k = ${c.k}`);
        if (c.load) note = `מחזור 0${NB}: ‏${ltr("start")} עולה ו-${ltr("busy")} עוד 0, ולכן ${ltr("load = 1")}. בסוף המחזור${NB}: ${ltr(`rem ← ${st.n}`)}, ${ltr("root ← 0")}, ${ltr("k ← 7")} ו-${ltr("busy ← 1")}.`;
        else if (c.busy && c.fits) note = `מחזור ${ltr(c.cycle)}, ${K}${NB}: הניסיון ${ltr(`(${c.root} ≪ ${c.k + 1}) | (1 ≪ ${2 * c.k}) = ${c.trial}`)}. ‏${ltr(`${c.rem} − ${c.trial} = ${c.diff}`)} בלי ${ltr("borrow")}, ולכן ${ltr("fits = 1")}. בסוף המחזור${NB}: ${ltr(`rem ← ${c.nrem}`)} ו-${ltr(`root[${c.k}] ← 1`)}, כלומר ${ltr(`root = ${c.nroot}`)}` +
          (c.ndone ? `, ו-${ltr("k = 0")}${NB}: ‏${ltr("busy ← 0")} ו-${ltr("done ← 1")}.` : `, ו-${ltr(`k ← ${c.nk}`)}.`);
        else if (c.busy) note = `מחזור ${ltr(c.cycle)}, ${K}${NB}: הניסיון ${ltr(c.trial)} גדול מ-${ltr(`rem = ${c.rem}`)}, והמחסר לווה${NB}: ${ltr("borrow = 1")}, ולכן ${ltr("fits = 0")}. ‏${ltr("root")} ו-${ltr("rem")} לא זזים` +
          (c.ndone ? `, ו-${ltr("k = 0")}${NB}: ‏${ltr("busy ← 0")} ו-${ltr("done ← 1")}.` : `, ו-${ltr(`k ← ${c.nk}`)}.`);
        else if (c.done) note = `מחזור ${ltr(c.cycle)}${NB}: ‏${ltr("done = 1")} למחזור אחד, ו-${ltr(`root = ${c.root}`)} ו-${ltr(`rem = ${c.rem}`)} מוכנים${NB}: ${ltr(`${c.root}² + ${c.rem} = ${c.root * c.root + c.rem}`)}.`;
        else note = `מחזור ${ltr(c.cycle)}${NB}: ‏${ltr("done")} ירד, ו-${ltr("root")} ו-${ltr("rem")} נשארים עד ה-${ltr("start")} הבא.`;
        $(".isqh-note").innerHTML = note;
        if (st.t >= end.cycle) answer(box, `${ltr(`⌊√${st.n}⌋ = ${end.root}`)}, והשארית ${ltr(`rem = ${end.rem}`)}, במחזור ${ltr(end.cycle)}.`, ".isqh-dpwrap [data-b=\"root\"] rect");
        else answer(box, null);
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.t++; draw(); }, done: () => st.t >= CYCLES - 1, restart: () => { st.t = 0; draw(); } });
      const set = (n) => { stop(); st.n = n; st.t = 0; $(".isqh-err").textContent = ""; input.value = String(n); draw(); };
      input.addEventListener("change", () => {
        const x = Number(input.value);
        if (input.value.trim() === "" || !Number.isInteger(x) || x < 0 || x > MAX) { $(".isqh-err").textContent = `מספר שלם מ-0 עד ${MAX}`; input.value = String(st.n); return; }
        set(x);
      });
      box.querySelectorAll(".isqh-trap").forEach((b) => b.addEventListener("click", () => set(Number(b.dataset.v))));
      $(".ex-start").addEventListener("click", () => { stop(); st.t = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.t--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.t++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.t = CYCLES - 1; draw(); });
      $(".ex-reset").addEventListener("click", () => set(N0));
      // the link and the remembered state: "1000_5", n and the cycle
      box.dvqExtra = {
        get: () => `${st.n}_${st.t}`,
        set: (text) => {
          const m = /^(\d{1,5})_(\d{1,2})$/.exec(text);
          if (!m || Number(m[1]) > MAX) return false;
          stop();
          Object.assign(st, { n: Number(m[1]), t: Number(m[2]) });
          draw();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { isqrthw: isqrthwView },
    help: {
      isqrthw: "המודול isqrt_seq על n של 16 ביטים, מחזור אחרי מחזור: במחזור 0 start טוען את n, במחזורים 1 עד 8 נקבע ביט אחד של השורש בכל מחזור, ובמחזור 9 done עולה. התרשים מראה את הערך בכל מלבן ובכל חוט במחזור הזה, והנתיב של המחזור מודגש. בטבלה כל האותות, עמודה לכל מחזור. כפתורי המלכודת טוענים קלטים שבהם קל לטעות.".replace(/:/g, `${NB}:`),
    },
    cols: { isqrthw: { main: ".isqh-dpwrap", side: ".isqh-wavewrap, .isqh-note", w: "minmax(0, 0.8fr)" } },
    models: { isqhwTrace, isqhwDiagram, isqhwLit },
  });
})();
