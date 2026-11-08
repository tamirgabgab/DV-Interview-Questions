// kinds: divhw
//   divhw                  0055        the circuit of parts a and b clock by clock (data-bits, data-dir lsb / msb: where a new bit enters, data-start 00 / 11): the bits typed in their order of arrival, the start after reset (00) or without it (11, the trap); the block diagram of the page (next-state logic, the register of two D flip-flops, the output logic, the loop back) with this clock's values, the wires at 1 lit and the flip-flops that flip at the coming edge framed; a table of every signal, a column per clock, the clock of the moment marked, a div that disagrees with v mod 3 marked
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, code, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const MAXB = 16;

  // --- the model, as tools/figures/q0055.py hw_clocks ----------------------------------------
  // The minimal equations of the page (q0055.py equations): a new bit entering as the LSB is
  // part a, as the MSB part b, the same gates with the two flip-flops swapped.
  const NEXT = {
    lsb: (q1, q0, b) => [(q1 & b) | (q0 & (1 - b)), ((1 - q1) & (1 - q0) & b) | (q1 & (1 - b))],
    msb: (q1, q0, b) => [((1 - q1) & (1 - q0) & b) | (q0 & (1 - b)), (q1 & (1 - b)) | (q0 & b)],
  };
  // One record per clock, clock 0 the one after reset (or after power-up in start): the
  // flip-flops q1, q0 through the clock, the bit din presented in it and the next state d1, d0
  // (null after the last bit), div = !q1 & !q0, and v the number the bits before it spell.
  const dhTrace = (bits, enters = "lsb", start = [0, 0]) => {
    const out = [];
    let [q1, q0] = start;
    for (let t = 0; t <= bits.length; t++) {
      const din = t < bits.length ? bits[t] : null;
      const [d1, d0] = din === null ? [null, null] : NEXT[enters](q1, q0, din);
      const seen = bits.slice(0, t);
      const v = enters === "lsb" ? seen.reduce((a, b) => 2 * a + b, 0) : seen.reduce((a, b, i) => a + b * 2 ** i, 0);
      out.push({ clock: t, din, q1, q0, d1, d0, div: q1 || q0 ? 0 : 1, v });
      if (din !== null) [q1, q0] = [d1, d0];
    }
    return out;
  };

  // --- the block diagram, as tools/figures/q0055.py HW_BLOCKS, HW_FFS and HW_WIRES ------------
  const BLOCKS = [["ns", 40, 50, 130, 110, "stage", "next state"], ["reg", 220, 50, 110, 110, "reg", "register"], ["out", 380, 75, 90, 60, "out", "output"]];
  const FFS = [["ff1", 236, 82, 36, 36, "Q1"], ["ff0", 278, 82, 36, 36, "Q0"]];
  const WIRES = [
    ["din", [[6, 105], [40, 105]], "din", 8, 97, "start"],
    ["d", [[170, 105], [220, 105]], "D1 D0", 195, 97, "middle"],
    ["clk", [[252, 14], [252, 50]], "clk", 246, 26, "end"],
    ["rst", [[298, 14], [298, 50]], "rst_n", 304, 26, "start"],
    ["q", [[330, 105], [380, 105]], "Q1 Q0", 360, 97, "middle"],
    ["fb", [[346, 105], [346, 196], [105, 196], [105, 160]], "Q1 Q0", 225, 214, "middle"],
    ["div", [[470, 105], [496, 105]], "div", 483, 97, "middle"],
  ];
  // the wires at 1 (a pair of bits: not 00), and the value written under each
  const dhLit = (c) => {
    const on = new Set();
    if (!c) return on;
    if (c.din === 1) on.add("din");
    if (c.d1 || c.d0) on.add("d");
    if (c.q1 || c.q0) { on.add("q"); on.add("fb"); }
    if (c.div) on.add("div");
    return on;
  };
  const dhDiagram = (c, enters = "lsb") => {
    const lit = dhLit(c), pair = (a, b) => (a === null ? "–" : `${a}${b}`);
    const vals = c ? { din: [c.din ?? "–", 23, 121], d: [pair(c.d1, c.d0), 195, 121], fb: [pair(c.q1, c.q0), 225, 190], div: [c.div, 483, 121] } : {};
    const sub = c ? { ns: c.din === null ? "no bit" : `D = ${pair(c.d1, c.d0)}`, out: `div = ${c.div}` } : {};
    let g = `<svg class="dh-fig dh-dp dh-live-dp" viewBox="0 0 500 224" direction="ltr" role="img" aria-label="תרשים המלבנים של המכונה עם הערכים של השעון הזה${c ? `${NB}: Q1 Q0 = ${c.q1}${c.q0}, div = ${c.div}` : ""}">` +
      '<defs><marker id="dh-hd" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="dh-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>';
    BLOCKS.forEach(([id, x, y, w, h, cls, title]) => {
      const ty = id === "reg" ? y + 18 : y + h / 2 - 3;
      g += `<g class="dh-blk dh-${cls}" data-b="${id}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5"/>` +
        `<text x="${x + w / 2}" y="${ty}" text-anchor="middle">${title}</text>` +
        (sub[id] ? `<text class="dh-val" x="${x + w / 2}" y="${y + h / 2 + 13}" text-anchor="middle">${sub[id]}</text>` : "") + "</g>";
    });
    FFS.forEach(([id, x, y, w, h, name], i) => {
      const q = c ? (i ? c.q0 : c.q1) : null, d = c ? (i ? c.d0 : c.d1) : null, flip = c && d !== null && d !== q;
      g += `<g class="dh-ff${flip ? " is-flip" : ""}${q ? " is-one" : ""}" data-b="${id}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3"/>` +
        `<text x="${x + w / 2}" y="${y + h / 2 + 5}" text-anchor="middle">${c ? q : name}</text>` +
        (c ? `<text class="dh-sub" x="${x + w / 2}" y="${y + h + 16}" text-anchor="middle">${name}</text>` : "") + "</g>";
    });
    WIRES.forEach(([id, pts, lab, lx, ly, anchor]) => {
      g += `<path class="dh-wire${lit.has(id) ? " is-on" : ""}" d="M${pts.map(([a, b]) => `${a},${b}`).join(" L")}" marker-end="url(#dh-hd)"/>` +
        `<text class="dh-wlab" x="${lx}" y="${ly}" text-anchor="${anchor}">${lab}</text>`;
      if (vals[id]) g += `<text class="dh-wval" x="${vals[id][1]}" y="${vals[id][2]}" text-anchor="middle">${vals[id][0]}</text>`;
    });
    g += '<circle class="dh-dot" cx="346" cy="105" r="3.5"/>';
    return g + "</svg>";
  };

  // --- the box -----------------------------------------------------------------------------------

  const ok = (c) => (c.v % 3 === 0 ? 1 : 0);
  const ROWS = [["din", (c) => (c.din ?? "–")], ["Q1", (c) => c.q1], ["Q0", (c) => c.q0], ["D1", (c) => (c.d1 ?? "–")], ["D0", (c) => (c.d0 ?? "–")],
    ["div", (c) => c.div], ["v", (c) => c.v], ["v % 3", (c) => c.v % 3]];
  const FLAGS = new Set(["din", "Q1", "Q0", "D1", "D0", "div"]);
  const wave = (tr, k) => {
    let t = `<table class="dh-wave"><thead><tr><th scope="col">שעון</th>${tr.map((c) => `<th scope="col"${c.clock === k ? ' class="is-now"' : ""}>${c.clock}</th>`).join("")}</tr></thead><tbody>`;
    ROWS.forEach(([name, f]) => {
      t += `<tr><th scope="row">${name}</th>` + tr.map((c) => {
        const shown = c.clock <= k, v = shown ? f(c) : "";
        const cls = [c.clock === k ? "is-now" : "", shown ? "" : "is-fut", FLAGS.has(name) && v === 1 ? "is-hi" : "",
          shown && name === "div" && c.div !== ok(c) ? "is-bad" : ""].filter(Boolean).join(" ");
        return `<td${cls ? ` class="${cls}"` : ""}>${v}${shown && name === "div" && c.div !== ok(c) ? " ✗" : ""}</td>`;
      }).join("") + "</tr>";
    });
    return t + "</tbody></table>";
  };
  const parseBits = (text) => {
    const s = String(text).replace(/\s+/g, "");
    return /^[01]{1,16}$/.test(s) ? [...s].map(Number) : null;
  };

  const divhwView = () => ({
    mount(box) {
      const d0 = {
        bits: parseBits(box.dataset.bits || "") || [1, 1, 0, 1],
        dir: box.dataset.dir === "msb" ? "msb" : "lsb",
        start: box.dataset.start === "11" ? "11" : "00",
      };
      const st = { bits: d0.bits, dir: d0.dir, start: d0.start, k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>הביטים לפי סדר ההגעה</span><input type="text" class="ex-num dh-in" dir="ltr" maxlength="${MAXB + 8}" spellcheck="false" autocomplete="off" aria-label="הביטים לפי סדר ההגעה, ביט בכל שעון, עד ${MAXB}"></label>` +
        `<label>הכיוון <select class="dh-dir" aria-label="איפה הביט החדש נכנס"><option value="lsb">ביט חדש נכנס כ-LSB (סעיף א)</option><option value="msb">ביט חדש נכנס כ-MSB (סעיף ב)</option></select></label>` +
        `<label>ההתחלה <select class="dh-start" aria-label="המצב בשעון 0"><option value="00">מ-00, אחרי reset</option><option value="11">מ-11, בלי reset</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err dh-err" aria-live="polite"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">שעון 0</button>` +
        `<button type="button" class="md-button ex-prev">השעון הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">השעון הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 700, 300) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary dh-sum" aria-live="polite"></p>` +
        `<div class="dh-dpwrap"></div>` +
        `<div class="dh-wavewrap" dir="ltr" tabindex="0" role="region" aria-label="כל האותות, עמודה לכל שעון"></div>` +
        `<p class="dh-note" aria-live="polite"></p>` +
        `<span class="viz-legend dh-legend"><span><i class="dh-key-on"></i>חוט ב-1 (זוג ביטים שאינו 00)</span><span><i class="dh-key-flip"></i>פליפ-פלופ שמתהפך בקצה הבא</span>` +
        `<span><i class="dh-key-now"></i>השעון של הרגע</span><span><i class="dh-key-bad"></i>div שטועה</span></span>`;
      const $ = (sel) => box.querySelector(sel);
      const input = $(".dh-in");
      const trace = () => dhTrace(st.bits, st.dir, st.start === "11" ? [1, 1] : [0, 0]);

      const draw = () => {
        const tr = trace(), T = tr.length - 1;
        st.k = Math.max(0, Math.min(st.k, T));
        if (document.activeElement !== input) input.value = st.bits.join("");
        $(".dh-dir").value = st.dir; $(".dh-start").value = st.start;
        $(".ex-pos").textContent = `שעון ${st.k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === T;
        const c = tr[st.k], last = tr[T], name = st.dir === "lsb" ? "r" : "x", text = st.bits.join("");
        $(".dh-dpwrap").innerHTML = dhDiagram(c, st.dir);
        const wv = $(".dh-wavewrap");
        wv.innerHTML = wave(tr, st.k);
        const cur = wv.querySelector("th.is-now");
        if (cur) wv.scrollLeft = Math.max(0, cur.offsetLeft - wv.clientWidth / 2);
        $(".dh-sum").innerHTML = `${code(text)} נכנס ביט בכל שעון, ${st.dir === "lsb" ? "וכל ביט חדש נכנס כ-LSB (סעיף א)" : "וכל ביט חדש נכנס כ-MSB (סעיף ב)"}${NB}: ` +
          `אחרי ${ltr(T)} ביטים המספר ${ltr(last.v)}. ‏${ltr("div")} בשעון ${ltr("t")} עונה על הביטים שנכנסו בשעונים שלפניו.`;
        const q = `${c.q1}${c.q0}`, sname = q === "11" ? "קוד שלא בשימוש" : ltr(`${name} = ${2 * c.q1 + c.q0}`);
        const seen = st.k ? `המספר שנכנס עד עכשיו, ${code(st.dir === "lsb" ? text.slice(0, st.k) : [...text.slice(0, st.k)].reverse().join(""))} = ${ltr(c.v)}` : "עוד לא נכנס ביט, והמספר 0";
        let note = `שעון ${ltr(st.k)}${NB}: ‏${ltr(`Q1 Q0 = ${q}`)} (${sname}), ולכן ${ltr(`div = ${c.div}`)}. ${seen}, ${c.v % 3 === 0 ? "מתחלק" : "לא מתחלק"} ב-3` +
          (c.div !== ok(c) ? `${NB}: ‏${ltr("div")} טועה, כי המכונה התחילה מ-11 בלי reset.` : ".");
        if (c.din !== null) note += ` ‏${ltr(`din = ${c.din}`)}, והלוגיקה נותנת ${ltr(`D1 D0 = ${c.d1}${c.d0}`)}, שנכתב ל-${ltr("Q1 Q0")} בקצה שבסוף השעון.`;
        $(".dh-note").innerHTML = note;
        if (st.k === T) {
          const right = last.div === ok(last);
          answer(box, `${ltr(last.v)} ${ok(last) ? "מתחלק" : "לא מתחלק"} ב-3, ו-${ltr("div")} בשעון ${ltr(T)} הוא ${ltr(last.div)}` +
            (right ? "." : `${NB}: המכונה טועה, כי היא התחילה מ-11.`), ".dh-dpwrap [data-b=\"out\"] rect");
        } else answer(box, null);
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= st.bits.length, restart: () => { st.k = 0; draw(); } });
      input.addEventListener("change", () => {
        const bits = parseBits(input.value);
        if (!bits) { $(".dh-err").textContent = `הביטים${NB}: 1 עד ${MAXB} ספרות 0 או 1`; return; }
        $(".dh-err").textContent = "";
        stop(); st.bits = bits; st.k = 0; draw();
      });
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      $(".dh-dir").addEventListener("change", () => { stop(); st.dir = $(".dh-dir").value === "msb" ? "msb" : "lsb"; st.k = 0; draw(); });
      $(".dh-start").addEventListener("change", () => { stop(); st.start = $(".dh-start").value === "11" ? "11" : "00"; st.k = 0; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = st.bits.length; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, { bits: d0.bits, dir: d0.dir, start: d0.start, k: 0 }); $(".dh-err").textContent = ""; input.value = d0.bits.join(""); draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { divhw: divhwView },
    help: {
      divhw: "המעגל של סעיפים א ו-ב, שעון אחרי שעון. מקלידים את הביטים לפי סדר ההגעה ובוחרים איפה ביט חדש נכנס, ומתחילים מ-00 אחרי reset או מ-11 בלי reset. התרשים מראה את הערך של כל חוט ושל כל פליפ-פלופ בשעון הזה : חוט ב-1 מודגש, ופליפ-פלופ שיתהפך בקצה הבא ממוסגר. בטבלה כל האותות, עמודה לכל שעון, ו-div שלא מתאים ל-v mod 3 מסומן.".replace(/ :/g, `${NB}:`),
    },
    cols: { divhw: { main: ".dh-dpwrap", side: ".dh-wavewrap, .dh-note", w: "minmax(0, 1.6fr)" } },
    models: { dhTrace, dhDiagram, dhLit },
  });
})();
