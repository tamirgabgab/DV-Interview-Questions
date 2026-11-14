// kinds: ibanhw
//   ibanhw                 0099        the hardware checker of part b (data-iban): the IBAN as it arrives, a digit a clock (every letter as two digits, the first 6 the head), then the tail of six zeros, stepped clock by clock (step / play); the answer of the whole IBAN shown from the first clock; the block diagram of the page with the values on its wires and blocks this clock (head and tail, the two multiplexers, 10x + e, mod 97, last from the input, what is written where, y + h at the end), the path the clock takes lit; the flip-flops h, r and n bit by bit; a table of every signal, a column per clock, the clock of the moment marked
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const HEAD = 6, TAIL = 6;
  const IL = "IL620108000000099999999";

  // --- the models, as tools/figures/q0099.py trace_rows and run_final ------------------------

  // the IBAN without spaces: two letters, two digits, then letters and digits, 5 to 34
  // characters; null otherwise
  const ihParse = (text) => {
    const s = String(text).replace(/\s+/g, "").toUpperCase();
    return /^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$/.test(s) ? s : null;
  };
  // the digits as they arrive: the IBAN as written, every letter as two digits
  const ihStream = (s) => [...s].flatMap((c) => [...String(parseInt(c, 36))].map(Number));
  const ihStep = (x, e) => (10 * x + e) % 97;          // the two blocks: 10x + e, then mod 97
  // every clock of the checker, as the SystemVerilog of the page: the registers before
  // (hb, rb, nb) and after (h, r, n), the control head = rb >= 97 and tail = nb > 0, the
  // multiplexers x and e, s = 10x + e, y = s mod 97, and done / ok in the clock with n = 6
  const ihTrace = (digits) => {
    const out = [];
    let h = 0, r = 97, n = 0;
    const clock = (d, last) => {
      const head = r >= 97, tail = n > 0;
      const x = head ? h : r, e = tail ? 0 : d, s = 10 * x + e, y = s % 97;
      const rec = { d: tail ? null : d, last: !tail && last, hb: h, rb: r, nb: n, head, tail, x, e, s, y, done: false, ok: false };
      if (tail) { r = y; rec.done = n === TAIL; rec.ok = rec.done && (y + h === 1 || y + h === 98); n = n === TAIL ? 0 : n + 1; }
      else if (head) { h = y; r = r === 97 + HEAD - 1 ? 0 : r + 1; }
      else { r = y; n = last ? 1 : 0; }
      Object.assign(rec, { h, r, n });
      out.push(rec);
    };
    digits.forEach((d, k) => clock(d, k === digits.length - 1));
    while (n > 0) clock(0, false);
    return out;
  };

  // --- the box ---------------------------------------------------------------------------------

  const bits = (v, w) => [...Array(w)].map((_, i) => (v >> (w - 1 - i)) & 1);
  // the block diagram of the page (tools/figures/q0099.py datapath_svg) with this clock's values
  const diagram = (c) => {
    const on = (yes) => (yes ? " is-on" : "");
    const blk = (x, y, w, h, title, value, cls, lit) =>
      `<g class="ih-blk ${cls}${on(lit)}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5"/>` +
      `<text x="${x + w / 2}" y="${y + h / 2 - 3}" text-anchor="middle">${title}</text>` +
      `<text class="ih-val" x="${x + w / 2}" y="${y + h / 2 + 13}" text-anchor="middle">${value}</text></g>`;
    const wire = (pts, lit, arrow = true) => `<path class="ih-wire${on(lit)}" d="M${pts.map(([a, b]) => `${a},${b}`).join(" L")}"${arrow ? ' marker-end="url(#ih-hd)"' : ""}/>`;
    const any = Boolean(c), head = any && c.head, tail = any && c.tail, rest = any && !c.head && !c.tail;
    const val = (f) => (any ? f() : "");
    const wrote = !any ? "" : head ? `h ← ${c.y}, r ← ${c.r}` : tail ? `r ← ${c.y}, n ← ${c.n}` : `r ← ${c.y}${c.n ? ", n ← 1" : ""}`;
    let g = `<svg class="ih-fig ih-live-dp" viewBox="0 0 400 500" direction="ltr" role="img" aria-label="תרשים המלבנים של הבודק עם הערכים של השעון הזה">` +
      '<defs><marker id="ih-hd" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="ih-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>';
    g += blk(20, 14, 104, 48, "h", val(() => c.hb), "ih-reg", head || (any && c.done));
    g += blk(148, 14, 104, 48, "r", val(() => c.rb), "ih-reg", any && !head);
    g += blk(276, 14, 104, 48, "n", val(() => c.nb), "ih-reg", tail);
    g += blk(148, 86, 104, 40, "r ≥ 97 ?", val(() => `head = ${head ? 1 : 0}`), "ih-ctl", head);
    g += blk(276, 86, 104, 40, "n > 0 ?", val(() => `tail = ${tail ? 1 : 0}`), "ih-ctl", tail);
    g += wire([[200, 62], [200, 86]], any) + wire([[328, 62], [328, 86]], any);
    g += blk(40, 154, 150, 44, "x = head ? h : r", val(() => `x = ${c.x}`), "ih-mux", any);
    g += blk(220, 154, 150, 44, "e = tail ? 0 : d", val(() => `e = ${c.e}`), "ih-mux", any);
    g += wire([[72, 62], [72, 154]], head) + wire([[170, 62], [170, 72], [134, 72], [134, 154]], any && !head);
    g += wire([[148, 126], [148, 140], [115, 140], [115, 154]], head, false) + wire([[330, 126], [330, 140], [295, 140], [295, 154]], tail, false);
    g += `<text class="ih-wlab" x="352" y="144" text-anchor="start">d = ${any && c.d != null ? c.d : "–"}</text>` + wire([[350, 148], [350, 154]], rest || head);
    g += blk(90, 222, 220, 44, "s = 10x + e", val(() => `s = ${c.s}`), "ih-add", any);
    g += wire([[115, 198], [115, 222]], any) + wire([[295, 198], [295, 222]], any);
    g += blk(90, 290, 220, 44, "y = s mod 97", val(() => `y = ${c.y}`), "ih-stage", any);
    g += wire([[200, 266], [200, 290]], any);
    g += blk(40, 358, 320, 44, "write back", wrote, "ih-mux", any);
    g += wire([[200, 334], [200, 358]], any);
    // last, from the input with the last digit: it loads n = 1, the start of the tail
    g += `<text class="ih-wlab" x="50" y="347" text-anchor="start">last = ${any && c.last ? 1 : 0}</text>` + wire([[46, 340], [46, 358]], any && c.last);
    g += wire([[40, 380], [8, 380], [8, 38], [20, 38]], head);
    g += wire([[360, 380], [392, 380], [392, 6], [200, 6], [200, 14]], any && !head ? true : head) + wire([[328, 6], [328, 14]], any && c.n !== c.nb);
    const done = any && c.done;
    g += blk(40, 430, 140, 44, "y + h", done ? `${c.y} + ${c.hb} = ${c.y + c.hb}` : "", "ih-add", done);
    g += blk(220, 430, 140, 44, "= 1 or 98 ?", done ? `done = 1, ok = ${c.ok ? 1 : 0}` : "done = 0", "ih-out", done);
    g += wire([[110, 402], [110, 430]], done) + wire([[180, 452], [220, 452]], done);
    return g + "</svg>";
  };
  // every signal, a row each, a column per clock; the clock of the moment marked
  const ROWS = [["d", (c) => (c.d == null ? "" : c.d)], ["last", (c) => +c.last], ["head", (c) => +c.head], ["tail", (c) => +c.tail], ["x", (c) => c.x], ["e", (c) => c.e],
    ["s", (c) => c.s], ["y", (c) => c.y], ["h", (c) => c.h], ["r", (c) => c.r], ["n", (c) => c.n], ["done", (c) => +c.done], ["ok", (c) => +c.ok]];
  const FLAGS = new Set(["last", "head", "tail", "done", "ok"]);
  const wave = (tr, k) => {
    let t = `<table class="ih-wave"><thead><tr><th scope="col">שעון</th>${tr.map((_, i) => `<th scope="col"${i === k - 1 ? ' class="is-now"' : ""}>${i + 1}</th>`).join("")}</tr></thead><tbody>`;
    ROWS.forEach(([name, f]) => {
      t += `<tr><th scope="row">${name}</th>` + tr.map((c, i) => {
        const shown = i < k, v = shown ? f(c) : "";
        const cls = [i === k - 1 ? "is-now" : "", shown ? "" : "is-fut", FLAGS.has(name) && v === 1 ? "is-hi" : ""].filter(Boolean).join(" ");
        return `<td${cls ? ` class="${cls}"` : ""}>${v}</td>`;
      }).join("") + "</tr>";
    });
    return t + "</tbody></table>";
  };

  const ibanhwView = () => ({
    mount(box) {
      const s0 = ihParse(box.dataset.iban || "") || IL;
      const st = { s: s0, k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label class="ih-lab-in"><span>ה-IBAN</span><input type="text" class="ex-num ih-in" data-nolink dir="ltr" spellcheck="false" autocomplete="off" aria-label="ה-IBAN, אותיות וספרות"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה ל-IBAN של העמוד</button><span class="fl-err ih-err" aria-live="polite"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">השעון הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">השעון הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1100, 600, 200) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary ih-sum" aria-live="polite"></p>` +
        `<div class="ih-grid">` +
        `<div class="ih-strip" dir="ltr" tabindex="0" role="region" aria-label="הספרות כפי שהן מגיעות, ספרה בכל שעון, ואחריהן הזנב"></div>` +
        `<div class="ih-dpwrap"></div>` +
        `<div class="ih-regs" dir="ltr" role="group" aria-label="הפליפ-פלופים אחרי השעון, ביט אחרי ביט"></div>` +
        `<div class="ih-wavewrap" dir="ltr" tabindex="0" role="region" aria-label="כל האותות, עמודה לכל שעון"></div></div>` +
        `<span class="viz-legend"><span><i class="ih-key-head"></i>ספרות הראש</span><span><i class="ih-key-tail"></i>ספרות 0 של הזנב</span>` +
        `<span><i class="ih-key-now"></i>השעון של הרגע</span><span><i class="ih-key-on"></i>הנתיב של השעון הזה</span><span><i class="ih-key-flip"></i>פליפ-פלופ שהשתנה</span></span>` +
        `<p class="ih-note" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const trace = () => ihTrace(ihStream(st.s));

      const draw = () => {
        const tr = trace(), digits = ihStream(st.s), T = tr.length;
        st.k = Math.max(0, Math.min(st.k, T));
        $(".ih-in").value = st.s.replace(/(.{4})/g, "$1 ").trim();
        $(".ex-pos").textContent = `שעון ${st.k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === T;
        const c = st.k ? tr[st.k - 1] : null;
        const cells = digits.map((d, i) => [d, i < HEAD ? " ih-head" : ""]).concat(T > digits.length ? Array(T - digits.length).fill([0, " ih-tail"]) : []);
        $(".ih-strip").innerHTML = cells.map(([d, cls], i) => `<span class="ih-c${cls}${i === st.k - 1 ? " is-now" : ""}${i < st.k - 1 ? " is-past" : ""}">${d}</span>`).join("");
        $(".ih-dpwrap").innerHTML = diagram(c);
        // the flip-flops after this clock, the bits that changed marked
        const now = c ? { h: c.h, r: c.r, n: c.n } : { h: 0, r: 97, n: 0 }, was = c ? { h: c.hb, r: c.rb, n: c.nb } : now;
        $(".ih-regs").innerHTML = [["h", 7], ["r", 7], ["n", 3]].map(([name, w]) => {
          const old = bits(was[name], w);
          return `<span class="ih-reg"><span class="ih-rname">${name}</span><span class="ih-bits">` +
            bits(now[name], w).map((b, i) => `<i class="ih-b${c && b !== old[i] ? " is-flip" : ""}">${b}</i>`).join("") + `</span><span class="ih-rval">${now[name]}</span></span>`;
        }).join("");
        const wv = $(".ih-wavewrap");
        wv.innerHTML = wave(tr, st.k);
        const cur = wv.querySelector("th.is-now");
        if (cur) wv.scrollLeft = Math.max(0, cur.offsetLeft - wv.clientWidth / 2);
        $(".ih-sum").innerHTML = `בסך הכול ${ltr(T)} שעונים${NB}: ${ltr(digits.length)} ספרות, ${ltr(HEAD)} מהן בראש, ו-${ltr(T - digits.length)} אפסים של זנב. ‏${ltr(17)} פליפ-פלופים.`;
        let note;
        if (!c) note = `לפני השעון הראשון${NB}: ${ltr("h = 0")}, ${ltr("r = 97")} (ספרה 0 של הראש) ו-${ltr("n = 0")}. ‏"השעון הבא" מכניס ספרה.`;
        else if (c.head) note = `שעון ${ltr(st.k)}, הראש${NB}: ${ltr("r ≥ 97")}, ולכן ${ltr(`x = h = ${c.x}`)}. ‏${ltr(`(10·${c.x} + ${c.e}) mod 97 = ${c.y}`)} נכתב ל-${ltr("h")}, ו-${ltr("r")} סופר${NB}: ${ltr(`r = ${c.r}`)}${c.r === 0 ? ", הראש נגמר" : ""}.`;
        else if (c.tail) note = `שעון ${ltr(st.k)}, הזנב, ${ltr(`n = ${c.nb}`)}${NB}: ${ltr("e = 0")}, כלומר ${ltr("r")} כפול 10${NB}: ${ltr(`(10·${c.x}) mod 97 = ${c.y}`)}.` +
          (c.done ? ` זה השעון השישי, ולכן ${ltr("done = 1")}${NB}: ${ltr(`y + h = ${c.y} + ${c.hb} = ${c.y + c.hb}`)}.` : ` המונה עולה ל-${ltr(c.n)}.`);
        else note = `שעון ${ltr(st.k)}${NB}: ${ltr(`x = r = ${c.x}`)}, ‏${ltr(`(10·${c.x} + ${c.e}) mod 97 = ${c.y}`)} נכתב ל-${ltr("r")}.` + (c.n ? ` זו הספרה האחרונה, ו-${ltr("last")} טוען ${ltr("n = 1")}${NB}: מתחיל הזנב.` : "");
        $(".ih-note").innerHTML = note;
        // the answer of the whole IBAN, from the first clock (it comes out at the last one)
        const e = tr[T - 1];
        if (e && e.done) answer(box, (e.ok ? `תקין${NB}: ` : `לא תקין${NB}: `) + `בשעון ${ltr(T)}, ${ltr(`y + h = ${e.y} + ${e.hb} = ${e.y + e.hb}`)}${e.ok ? "" : ", לא 1 ולא 98"}.`, st.k === T ? ".ih-dpwrap .ih-out rect" : []);
        else answer(box, `לא תקין${NB}: ה-IBAN קצר מהראש.`, []);
      };

      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= trace().length, restart: () => { st.k = 0; draw(); } });
      $(".ih-in").addEventListener("change", () => {
        const s = ihParse($(".ih-in").value);
        $(".ih-err").textContent = s ? "" : `ה-IBAN${NB}: שתי אותיות, שתי ספרות, ואחריהן אותיות וספרות, עד 34 תווים`;
        if (s) { stop(); st.s = s; st.k = 0; draw(); }
      });
      $(".ih-in").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".ih-in").blur(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = trace().length; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, { s: s0, k: 0 }); $(".ih-err").textContent = ""; draw(); });
      // the link and the remembered state: "IL62..._7"
      box.dvqExtra = {
        get: () => `${st.s}_${st.k}`,
        set: (text) => {
          const m = /^([A-Z0-9]{5,34})_(\d+)$/.exec(text);
          if (!m || !ihParse(m[1])) return false;
          stop();
          Object.assign(st, { s: m[1], k: Number(m[2]) });
          draw();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { ibanhw: ibanhwView },
    help: {
      ibanhw: "ה-IBAN נכנס לבודק ספרה אחת בכל שעון, כל אות כשתי ספרות, ו-6 הספרות הראשונות הן הראש. אחרי הספרה האחרונה באים 6 שעונים של זנב, עם הספרה 0. \"השעון הבא\" מתקדם בשעון אחד : התרשים מראה את הערך בכל חוט ובכל בלוק בשעון הזה, והנתיב שהשעון עובר בו מודגש. מתחתיו הפליפ-פלופים ביט אחרי ביט, וטבלה של כל האותות, עמודה לכל שעון. התשובה של כל ה-IBAN מופיעה מההתחלה.".replace(/ :/g, " :"),
    },
    models: { ihParse, ihStream, ihTrace },
  });
})();
