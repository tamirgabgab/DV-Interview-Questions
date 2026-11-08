// kinds: seqhw
//   seqhw                  0040        part a's circuit clock by clock (data-bits): the stimulus typed (1 to 24 bits of din), Mealy or Moore; the block diagram of the page (next-state logic, the state register, the output logic, din -> found in Mealy) with this clock's value on every wire and block and the path of the clock lit; the state register's flip-flops and their inputs bit by bit, the bits that flip at the edge marked; a table of every signal, a column per clock, the clock of the moment marked
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { autoplay, code, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const PAGE_BITS = "1011011";
  const MAX = 24;

  // --- the model, as the page's detect_1011 (Mealy) and run_fsm(moore=True) ------------------

  // the transition table of 1011 (states 0..4, 4 = the full match), as the page's tables;
  // Mealy has no state 4: the edge into it goes to S1 (REST) and outputs 1
  const NXT = [[0, 1], [2, 1], [0, 3], [2, 4], [2, 1]];
  const FULL = 4, REST = 1;
  // the stimulus: 1 to 24 bits of 0 and 1, spaces ignored; null otherwise
  const shParse = (text) => {
    const s = String(text).replace(/\s+/g, "");
    return /^[01]{1,24}$/.test(s) ? s : null;
  };
  // every clock of the module: din on the line, the state the flip-flops hold (q), the next
  // state at their inputs (d, loaded at the rising edge that ends the clock), and found.
  // Mealy: found = (state == S3) & din, a clock per bit. Moore: found = (state == S4), and one
  // more clock after the last bit, with no bit (din null, next null), whose found comes from
  // the state alone.
  const shTrace = (bits, moore = false) => {
    const width = moore ? 3 : 2, clocks = [];
    const bitsOf = (v) => (v == null ? null : [...Array(width)].map((_, i) => (v >> (width - 1 - i)) & 1));
    let s = 0;
    bits.forEach((b) => {
      const n = NXT[s][b];
      const found = moore ? +(s === FULL) : +(n === FULL);
      const next = moore || n < FULL ? n : REST;
      clocks.push({ din: b, state: s, next, found, q: bitsOf(s), d: bitsOf(next) });
      s = next;
    });
    if (moore) clocks.push({ din: null, state: s, next: null, found: +(s === FULL), q: bitsOf(s), d: null });
    return { width, clocks };
  };

  // --- the box ---------------------------------------------------------------------------------

  const S = (v) => (v == null ? "–" : `S${v}`);
  const B = (bits) => (bits ? bits.join("") : "–");
  // the block diagram of the page (tools/figures/q0040.py circuit_svg) with this clock's values
  const diagram = (c, moore, width) => {
    const on = (yes) => (yes ? " is-on" : "");
    const any = Boolean(c), decides = any && !moore && c.state === 3;
    const blk = (x, y, w, h, title, value, cls, lit) =>
      `<g class="shw-blk ${cls}${on(lit)}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5"/>` +
      `<text x="${x + w / 2}" y="${y + h / 2 - 3}" text-anchor="middle">${title}</text>` +
      `<text class="shw-val" x="${x + w / 2}" y="${y + h / 2 + 14}" text-anchor="middle">${value}</text></g>`;
    const wire = (pts, lit, cls = "") => `<path class="shw-wire${cls}${on(lit)}" d="M${pts.map(([a, b]) => `${a},${b}`).join(" L")}" marker-end="url(#shw-hd)"/>`;
    const lab = (x, y, t, anchor = "start", cls = "") => `<text class="shw-wlab${cls}" x="${x}" y="${y}" text-anchor="${anchor}">${t}</text>`;
    const din = any ? (c.din == null ? "–" : c.din) : "";
    let g = `<svg class="shw-fig shw-live-dp" viewBox="0 0 440 356" direction="ltr" role="img" aria-label="תרשים המלבנים של הגלאי עם הערכים של השעון הזה">` +
      '<defs><marker id="shw-hd" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="shw-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>';
    g += lab(200, 14, any ? `din = ${din}` : "din", "middle");
    g += wire([[200, 20], [200, 58]], any && c.din != null);
    if (!moore) {
      g += wire([[200, 38], [410, 38], [410, 285], [322, 285]], decides, " shw-mealy");
      g += `<circle class="shw-dot" cx="200" cy="38" r="3"/>` + lab(404, 160, "Mealy", "end", " shw-mlab");
    }
    g += blk(80, 60, 240, 50, "next-state logic", any ? (c.next == null ? "no bit: –" : `${S(c.state)}, din = ${c.din} → ${S(c.next)}`) : "next = f(state, din)", "shw-logic", any && c.next != null);
    g += wire([[200, 110], [200, 158]], any && c.next != null) + lab(208, 140, any ? `next = ${B(c.d)}` : `next[${width - 1}:0]`);
    g += blk(110, 160, 180, 50, "state register", any ? `${S(c.state)} = ${B(c.q)}` : `${width} D flip-flops`, "shw-reg", any);
    g += wire([[370, 185], [292, 185]], any) + lab(298, 178, "clk, rst_n");
    g += wire([[200, 210], [200, 258]], any) + `<circle class="shw-dot" cx="200" cy="235" r="3"/>`;
    g += wire([[200, 235], [40, 235], [40, 85], [78, 85]], any && c.next != null);
    g += lab(208, 250, any ? `state = ${B(c.q)}` : `state[${width - 1}:0]`);
    const outv = !any ? (moore ? "found = (state == S4)" : "found = (state == S3) &amp; din")
      : moore ? `(${S(c.state)} == S4) = ${c.found}` : `(${S(c.state)} == S3) &amp; ${c.din} = ${c.found}`;
    g += blk(80, 260, 240, 50, "output logic", outv, "shw-out", any && (c.found === 1 || decides));
    g += wire([[200, 310], [200, 343]], any && c.found === 1) + lab(208, 338, any ? `found = ${c.found}` : "found");
    return g + "</svg>";
  };
  // every signal, a row each, a column per clock; the clock of the moment marked
  const ROWS = [["din", (c) => (c.din == null ? "–" : c.din)], ["state", (c) => S(c.state)], ["state[]", (c) => B(c.q)],
    ["next", (c) => S(c.next)], ["next[]", (c) => B(c.d)], ["found", (c) => c.found]];
  const wave = (tr, k, width) => {
    const name = (n) => n.replace("[]", `[${width - 1}:0]`);
    let t = `<table class="shw-wave"><thead><tr><th scope="col">שעון</th>${tr.map((_, i) => `<th scope="col"${i === k - 1 ? ' class="is-now"' : ""}>${i + 1}</th>`).join("")}</tr></thead><tbody>`;
    ROWS.forEach(([n, f]) => {
      t += `<tr><th scope="row">${name(n)}</th>` + tr.map((c, i) => {
        const shown = i < k, v = shown ? f(c) : "";
        const cls = [i === k - 1 ? "is-now" : "", shown ? "" : "is-fut", n === "found" && v === 1 ? "is-hi" : ""].filter(Boolean).join(" ");
        return `<td${cls ? ` class="${cls}"` : ""}>${v}</td>`;
      }).join("") + "</tr>";
    });
    return t + "</tbody></table>";
  };

  const seqhwView = () => ({
    mount(box) {
      const b0 = shParse(box.dataset.bits || "") || PAGE_BITS;
      const st = { s: b0, moore: false, k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label class="shw-lab-in"><span>הביטים של din</span><input type="text" class="ex-num shw-in" value="${b0}" dir="ltr" maxlength="40" inputmode="numeric" spellcheck="false" autocomplete="off" aria-label="הביטים של din, אחד בכל שעון, 1 עד 24"></label>` +
        `<label>המכונה <select class="shw-kind" aria-label="Mealy או Moore"><option value="mealy">Mealy</option><option value="moore">Moore</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לביטים של העמוד</button><span class="fl-err shw-err" aria-live="polite"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">השעון הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">השעון הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1100, 600, 250) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary shw-sum" aria-live="polite"></p>` +
        `<div class="shw-grid">` +
        `<div class="shw-strip" dir="ltr" role="group" aria-label="הביטים של din, אחד בכל שעון"></div>` +
        `<div class="shw-dpwrap"></div>` +
        `<div class="shw-regs" dir="ltr" role="group" aria-label="הפליפ-פלופים של המצב והכניסות שלהם, ביט אחרי ביט"></div>` +
        `<div class="shw-wavewrap" dir="ltr" tabindex="0" role="region" aria-label="כל האותות, עמודה לכל שעון"></div></div>` +
        `<span class="viz-legend"><span><i class="shw-key-now"></i>השעון של הרגע</span><span><i class="shw-key-on"></i>הנתיב של השעון הזה</span>` +
        `<span><i class="shw-key-mealy"></i>‏din → found ב-Mealy</span><span><i class="shw-key-flip"></i>ביט שמתהפך בעליית השעון</span></span>` +
        `<p class="shw-note" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const trace = () => shTrace([...st.s].map(Number), st.moore);

      const draw = () => {
        const { width, clocks: tr } = trace(), T = tr.length;
        st.k = Math.max(0, Math.min(st.k, T));
        $(".shw-kind").value = st.moore ? "moore" : "mealy";
        $(".ex-pos").textContent = `שעון ${st.k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === T;
        const c = st.k ? tr[st.k - 1] : null;
        $(".shw-strip").innerHTML = tr.map((x, i) => `<span class="shw-c${x.din == null ? " shw-none" : ""}${i === st.k - 1 ? " is-now" : ""}${i < st.k - 1 ? " is-past" : ""}">${x.din == null ? "–" : x.din}</span>`).join("");
        $(".shw-dpwrap").innerHTML = diagram(c, st.moore, width);
        // the flip-flops now (q) and at their inputs (d); a bit that differs flips at the edge
        const q = c ? c.q : Array(width).fill(0), d = c ? c.d : null;
        const reg = (name, bits, val, other) => `<span class="shw-reg"><span class="shw-rname">${name}</span><span class="shw-bits">` +
          (bits ? bits.map((b, i) => `<i class="shw-b${other && b !== other[i] ? " is-flip" : ""}">${b}</i>`).join("") : Array(width).fill('<i class="shw-b shw-none">–</i>').join("")) +
          `</span><span class="shw-rval">${val}</span></span>`;
        $(".shw-regs").innerHTML = reg(`state[${width - 1}:0]`, q, c ? S(c.state) : "S0", d) + reg(`next[${width - 1}:0]`, d, c ? S(c.next) : "–", d ? q : null);
        const wv = $(".shw-wavewrap");
        wv.innerHTML = wave(tr, st.k, width);
        const cur = wv.querySelector("th.is-now");
        if (cur) wv.scrollLeft = Math.max(0, cur.offsetLeft - wv.clientWidth / 2);
        const hits = tr.map((x, i) => (x.found ? i + 1 : 0)).filter(Boolean);
        $(".shw-sum").innerHTML = `המכונה ${st.moore ? "Moore" : "Mealy"}, ${ltr(width)} פליפ-פלופים, ${ltr(T)} שעונים${st.moore ? " (האחרון בלי ביט)" : ""}${NB}: ` +
          (hits.length ? `‏${code("found")} עולה ${hits.length === 1 ? "בשעון" : "בשעונים"} ${ltr(hits.join(", "))}.` : `‏${code("found")} לא עולה אף פעם.`);
        let note;
        if (!c) note = `לפני השעון הראשון${NB}: האיפוס שם את המצב ב-${code("S0")}, ‏${ltr(`state = ${"0".repeat(width)}`)}. ‏"השעון הבא" מכניס את הביט הראשון.`;
        else if (c.din == null) note = `שעון ${ltr(st.k)}${NB}: אין ביט חדש. ב-Moore ‏${code("found")} יוצא מהמצב בלבד${NB}: המצב ${code(S(c.state))}, ולכן ${ltr(`found = ${c.found}`)}` +
          (c.found ? `, שעון אחד אחרי הביט שסגר את התבנית.` : ".");
        else {
          note = `שעון ${ltr(st.k)}${NB}: המצב ${code(S(c.state))} ‏(${ltr(B(c.q))}) ו-${ltr(`din = ${c.din}`)}. לוגיקת המצב הבא בוחרת ${code(S(c.next))} ‏(${ltr(B(c.d))}), שנכנס לפליפ-פלופים בעליית השעון.`;
          if (st.moore) note += c.found ? ` המצב ${code("S4")}, ולכן ${ltr("found = 1")}, בלי קשר ל-${code("din")}.` : ` ‏${ltr("found = 0")}, כי המצב אינו ${code("S4")}.`;
          else if (c.state === 3) note += ` המצב ${code("S3")}, ולכן ${ltr(`found = din = ${c.found}`)} באותו שעון${NB}: המסלול הצירופי מ-${code("din")} ל-${code("found")}.`;
          else note += ` ‏${ltr("found = 0")}, כי המצב אינו ${code("S3")}.`;
        }
        $(".shw-note").innerHTML = note;
      };

      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= trace().clocks.length, restart: () => { st.k = 0; draw(); } });
      $(".shw-in").addEventListener("change", () => {
        const s = shParse($(".shw-in").value);
        $(".shw-err").textContent = s ? "" : `הביטים${NB}: 1 עד ${MAX} ביטים, רק 0 ו-1`;
        if (s) { stop(); st.s = s; st.k = 0; $(".shw-in").value = s; draw(); }
      });
      $(".shw-in").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".shw-in").blur(); });
      $(".shw-kind").addEventListener("change", () => { stop(); st.moore = $(".shw-kind").value === "moore"; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = trace().clocks.length; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, { s: b0, moore: false, k: 0 }); $(".shw-in").value = b0; $(".shw-err").textContent = ""; draw(); });
      // the link and the remembered state: the field and the select are controls; the clock rides here
      box.dvqExtra = {
        get: () => (st.k ? String(st.k) : ""),
        set: (text) => {
          if (!/^\d+$/.test(text)) return false;
          stop();
          st.k = Number(text);
          draw();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { seqhw: seqhwView },
    help: {
      seqhw: "המעגל של סעיף א, שעון אחרי שעון. מקלידים את הביטים של din ובוחרים Mealy או Moore. \"השעון הבא\" מתקדם בשעון אחד : התרשים מראה את הערך בכל חוט ובכל בלוק בשעון הזה, והנתיב שלו מודגש. מתחתיו הפליפ-פלופים של המצב והכניסות שלהם ביט אחרי ביט (ביט שמתהפך בעליית השעון ממוסגר), וטבלה של כל האותות, עמודה לכל שעון. ב-Moore יש שעון אחד נוסף בלי ביט, שבו found יוצא מהמצב בלבד.".replace(/ :/g, " :"),
    },
    models: { shParse, shTrace },
  });
})();
