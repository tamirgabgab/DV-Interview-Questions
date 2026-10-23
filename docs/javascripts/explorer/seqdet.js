// kinds: seqdet
//   seqdet                 0040        a pattern of up to 8 bits, Mealy or Moore: the KMP automaton drawn as a row of states, bits fed by hand, at random or played, the strip of din / state / found; a toggle for the pattern slid under the input, the build of both edges
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { H, W, autoplay, code, f, ltr, seedControls, speedSel, waveStrip } = dvqExplorers.lib;

  // Sequence detector (0040): the KMP automaton of a pattern (states 0..L, nxt[s][b]),
  // the Mealy state the full match collapses to (the state with the same transitions),
  // and a run over bits: the state before each bit and the output (Mealy on the bit that
  // completes the pattern, Moore one cycle later).
  const seqTable = (pattern) => {
    const L = pattern.length, nxt = Array.from({ length: L + 1 }, () => [0, 0]);
    nxt[0][pattern[0]] = 1;
    let fail = 0;
    for (let s = 1; s <= L; s++) {
      for (let b = 0; b < 2; b++) nxt[s][b] = s < L && pattern[s] === b ? s + 1 : nxt[fail][b];
      if (s < L) fail = nxt[fail][pattern[s]];
    }
    let rest = 0;
    for (let s = 0; s < L; s++) if (nxt[s][0] === nxt[L][0] && nxt[s][1] === nxt[L][1]) { rest = s; break; }
    return { nxt, rest, L };
  };
  // How an edge is built: in state s the last s bits are the pattern's first s; a bit b
  // makes the text pattern[0..s) + b, and the next state is the longest prefix of the
  // pattern that this text ends with (the pattern slid under it by `shift`).
  const seqFallback = (pattern, s, b) => {
    const text = pattern.slice(0, s).concat([b]), L = pattern.length;
    for (let k = Math.min(text.length, L); k >= 0; k--) {
      const tail = text.slice(text.length - k);
      if (tail.every((v, i) => v === pattern[i])) return { text, shift: text.length - k, target: k };
    }
    return { text, shift: text.length, target: 0 };
  };
  const seqRun = (pattern, bits, moore = false) => {
    const { nxt, rest, L } = seqTable(pattern);
    let state = 0;
    const states = [], out = [];
    bits.forEach((b) => {
      states.push(state);
      const n = nxt[state][b];
      out.push(moore ? (state === L ? 1 : 0) : (n === L ? 1 : 0));
      state = moore || n < L ? n : rest;
    });
    return { states, out, next: state };
  };

  // The sequence detector box (0040): a pattern of up to 8 bits and a Mealy / Moore
  // select; bits fed one at a time by the 0 and 1 buttons, by a random bit at the chosen
  // probability of 1, or played; the automaton drawn as a row of states with the taken
  // transition lit; a strip of clk, din, the state and found; the summary names where
  // 0 and 1 lead next.
  const seqdetView = () => ({
    mount(box) {
      const P0 = (box.dataset.pattern || "1011").replace(/[^01]/g, "").slice(0, 8) || "1011";
      const KEEP = 24;
      const st = { pattern: [...P0].map(Number), moore: false, p1: 0.5, bits: [] };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>התבנית</span><input type="text" class="ex-num sq-pat" value="${P0}" dir="ltr" maxlength="8" pattern="[01]{1,8}" inputmode="numeric" aria-label="התבנית, 1 עד 8 ביטים"></label>` +
        `<label>המכונה <select class="sq-kind" aria-label="Mealy או Moore"><option value="mealy">Mealy</option><option value="moore">Moore</option></select></label>` +
        `<label><span>הסתברות ל-1</span><input type="range" class="sq-p" min="0" max="100" step="5" value="50" dir="ltr" aria-label="ההסתברות שביט אקראי הוא 1, באחוזים"><output class="out-p">50%</output></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err sq-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<span class="ex-title">הביט הבא :</span>` +
        `<button type="button" class="md-button md-button--primary sq-bit" data-b="0">0</button>` +
        `<button type="button" class="md-button md-button--primary sq-bit" data-b="1">1</button>` +
        `<button type="button" class="md-button ex-next">ביט אקראי</button>` +
        `<button type="button" class="md-button ex-prev">ביטול הביט האחרון</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 600, 250) +
        `<button type="button" class="md-button ex-start">ניקוי</button>` +
        `<span class="wv-presets">דוגמאות : <button type="button" class="md-button ex-preset" data-s="1011011">1011011</button> <button type="button" class="md-button ex-preset" data-s="10101011">10101011</button></span></div>` +
        `<p class="ex-summary sq-sum" aria-live="polite"></p><p class="sq-next"></p>` +
        `<div class="sq-graph"></div>` +
        `<label class="sq-build-toggle"><input type="checkbox" class="sq-build" checked> איך נבנה המעבר מהמצב הנוכחי</label><div class="sq-slide"></div>` +
        `<span class="viz-legend"><span><i class="fs-key"></i>מעבר</span><span><i class="fs-key-found"></i>המעבר שמזהה (Mealy) או המצב שמוציא 1 (Moore)</span><span><i class="sq-key-cur"></i>המצב הנוכחי</span></span>` +
        `<div class="wv-wrap sq-strip" tabindex="0" role="group" aria-label="רצועת התזמון של הגלאי, גלילה אופקית"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let stop = () => {};
      const graph = (t, run) => {
        const L = t.L, N = st.moore ? L + 1 : L;
        const W = 640, Y = 90, R = N > 6 ? 18 : 24, H = 200;
        const xs = Array.from({ length: N }, (_, k) => (N === 1 ? W / 2 : 50 + (k * (W - 100)) / (N - 1)));
        const cur = run.next, last = st.bits.length ? st.bits[st.bits.length - 1] : null, before = st.bits.length ? run.states[run.states.length - 1] : null;
        const target = (s, b) => { const n = t.nxt[s][b]; return st.moore || n < L ? n : t.rest; };
        let h = `<svg class="figure sq-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="גרף המצבים : ${N} מצבים, המצב הנוכחי מודגש">` +
          `<defs><marker id="sq-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>`;
        const labels = [];
        for (let s = 0; s < N; s++) for (let b = 0; b < 2; b++) {
          const n = t.nxt[s][b], found = !st.moore && n === L, tg = target(s, b);
          const taken = before === s && last === b;
          const cls = `fs-edge${found ? " is-found" : ""}${taken ? " is-taken" : ""}`;
          const x0 = xs[s], x1 = xs[tg], lab = found ? `${b} / 1` : String(b);
          if (tg === s + 1) { h += `<line class="${cls}" x1="${f(x0 + R)}" y1="${Y}" x2="${f(x1 - R - 2)}" y2="${Y}" marker-end="url(#sq-arrow)"/>`; labels.push([(x0 + x1) / 2, Y - 7, lab, found, taken]); }
          else if (tg === s) { h += `<path class="${cls}" d="M${f(x0 - 9)},${Y - R + 3} C${f(x0 - 30)},${Y - R - 40} ${f(x0 + 30)},${Y - R - 40} ${f(x0 + 9)},${Y - R + 2}" marker-end="url(#sq-arrow)"/>`; labels.push([x0, Y - R - 29, lab, found, taken]); }
          else { const depth = 26 + 14 * Math.abs(s - tg); h += `<path class="${cls}" d="M${f(x0)},${Y + R} Q${f((x0 + x1) / 2)},${Y + R + depth} ${f(x1)},${Y + R + 2}" marker-end="url(#sq-arrow)"/>`; labels.push([(x0 + x1) / 2, Y + R + depth / 2 + 14, lab, found, taken]); }
        }
        for (let s = 0; s < N; s++) {
          const out = st.moore && s === L;
          h += `<g class="fs-node${s === cur ? " is-cur" : ""}${out ? " is-out" : ""}"><circle cx="${f(xs[s])}" cy="${Y}" r="${R}"/><text x="${f(xs[s])}" y="${Y + 4}" text-anchor="middle">S${s}</text></g>` +
               `<text class="fs-meaning" x="${f(xs[s])}" y="${Y + R + 14}" text-anchor="middle">${s === 0 ? "start" : st.pattern.slice(0, s).join("")}</text>`;
        }
        labels.forEach(([x, y, lab, found, taken]) => { h += `<text class="fs-label halo${found ? " is-found" : ""}${taken ? " is-taken" : ""}" x="${f(x)}" y="${f(y)}" text-anchor="middle">${lab}</text>`; });
        return h + "</svg>";
      };
      const draw = () => {
        const t = seqTable(st.pattern), run = seqRun(st.pattern, st.bits, st.moore), L = t.L;
        $(".sq-kind").value = st.moore ? "moore" : "mealy"; $(".out-p").textContent = `${Math.round(st.p1 * 100)}%`;
        $(".sq-graph").innerHTML = graph(t, run);
        // the build of the two edges out of the current state: the text so far plus each
        // bit, with the pattern slid under it to the longest prefix that the text ends with
        if ($(".sq-build").checked) {
          const cur = run.next, rows = [0, 1].map((b) => {
            const fb = seqFallback(st.pattern, cur, b), n = fb.text.length, cell = (v, cls) => `<span class="sq-c ${cls}">${v}</span>`;
            const textRow = fb.text.map((v, i) => cell(v, i === n - 1 ? "is-bit" : "")).join("");
            const patRow = cell("", "is-pad").repeat(fb.shift) + st.pattern.map((v, i) => cell(v, i < fb.target ? "is-match" : "is-rest")).join("");
            const tg = st.moore || fb.target < L ? fb.target : t.rest;
            const what = fb.shift === 0 && fb.target === n ? `ממשיך קדימה` : fb.target === 0 ? `אף התחלה של התבנית לא נשארת` : `התבנית הוזזה ב-${ltr(fb.shift)}, ו-${ltr(fb.target)} ${fb.target === 1 ? "ביט מתאים" : "ביטים מתאימים"}`;
            return `<div class="sq-slide-case"><p>מ-${code(`S${cur}`)} עם ${code(String(b))} : ${what}, ולכן המעבר ל-${code(`S${tg}`)}${!st.moore && fb.target === L ? " (זיהוי, ומשם ממשיכים כמו מ-" + code(`S${t.rest}`) + ")" : ""}.</p>` +
              `<div class="sq-grid" dir="ltr"><span class="sq-lab">input</span>${textRow}<br><span class="sq-lab">pattern</span>${patRow}</div></div>`;
          });
          $(".sq-slide").innerHTML = `<p class="ex-title">במצב ${code(`S${cur}`)} ידוע ש${cur ? `-${ltr(cur)} הביטים האחרונים הם ${code(st.pattern.slice(0, cur).join(""))}` : "שום ביט מהתבנית עוד לא הופיע"}. לכל ביט הבא, התבנית מוזזת מתחת לקלט עד ההתאמה הארוכה ביותר :</p>` + rows.join("");
        } else $(".sq-slide").innerHTML = "";
        const from = Math.max(0, st.bits.length - KEEP), bits = st.bits.slice(from), states = run.states.slice(from), out = run.out.slice(from);
        const n = bits.length;
        $(".sq-strip").innerHTML = n ? waveStrip([
          { name: "clk", kind: "clock" },
          { name: "din", kind: "bit", values: bits, cls: "wv-s1" },
          { name: "state", kind: "bus", values: states.map((s) => `S${s}`), split: true },
          { name: "found", kind: "bit", values: out, cls: "wv-s2" },
        ], n, { cursor: n - 1, ticks: (k) => from + k + 1, label: `רצועת התזמון : ${n} מחזורים` }) : `<p class="ex-note">עוד לא הוזן אף ביט.</p>`;
        $(".sq-strip").scrollLeft = $(".sq-strip").scrollWidth;
        $(".ex-prev").disabled = st.bits.length === 0;
        const hits = run.out.reduce((a, b) => a + b, 0), pat = st.pattern.join("");
        $(".sq-sum").innerHTML = `התבנית ${code(pat)}, ${st.moore ? "Moore" : "Mealy"} עם ${ltr(st.moore ? L + 1 : L)} מצבים : ` +
          (st.bits.length ? `${ltr(st.bits.length)} ביטים הוזנו, ${hits === 1 ? "זיהוי אחד" : `${ltr(hits)} זיהויים`}` : "עוד לא הוזן אף ביט") +
          (st.bits.length && run.out[run.out.length - 1] ? ` <span class="wv-ok">✓ המוצא גבוה עכשיו</span>` : "") + `. המצב הנוכחי ${code(`S${run.next}`)}` +
          (run.next === 0 ? " (כלום מהתבנית)." : run.next === L ? " (התבנית הסתיימה, המוצא 1)." : ` (הביטים האחרונים ${code(st.pattern.slice(0, run.next).join(""))}).`);
        const where = (b) => { const nx = t.nxt[run.next][b], det = nx === L; const s = st.moore || !det ? nx : t.rest; return `${code(String(b))} → ${code(`S${s}`)}${det ? (st.moore ? " (יוציא 1 במחזור הבא)" : " ופלט 1") : ""}`; };
        $(".sq-next").innerHTML = `הביט הבא : ${where(0)}; ${where(1)}.` + (st.moore && run.next === L ? ` המצב ${code(`S${L}`)} מוציא 1 עכשיו, מחזור אחרי הביט האחרון.` : "");
      };
      const feed = (b) => { st.bits.push(b); draw(); };
      const setPattern = (text) => {
        const clean = String(text).replace(/\s/g, "");
        const err = /^[01]{1,8}$/.test(clean) ? "" : "תבנית של 1 עד 8 ביטים, רק 0 ו-1";
        $(".sq-err").textContent = err;
        if (err) return;
        stop(); st.pattern = [...clean].map(Number); $(".sq-pat").value = clean; draw();
      };
      $(".sq-pat").addEventListener("change", () => setPattern($(".sq-pat").value));
      $(".sq-pat").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".sq-pat").blur(); });
      $(".sq-build").addEventListener("change", draw);
      $(".sq-kind").addEventListener("change", () => { stop(); st.moore = $(".sq-kind").value === "moore"; draw(); });
      $(".sq-p").addEventListener("input", () => { st.p1 = Number($(".sq-p").value) / 100; draw(); });
      box.querySelectorAll(".sq-bit").forEach((btn) => btn.addEventListener("click", () => { stop(); feed(Number(btn.dataset.b)); }));
      const seed = seedControls(box, $(".wv-presets"), (rng) => { stop(); st.bits = Array.from({ length: 12 }, () => (rng() < st.p1 ? 1 : 0)); draw(); });
      $(".ex-next").addEventListener("click", () => { stop(); feed(Math.random() < st.p1 ? 1 : 0); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.bits.pop(); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.bits = []; draw(); });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { stop(); st.bits = [...b.dataset.s].map(Number); draw(); }));
      $(".ex-reset").addEventListener("click", () => { stop(); st.moore = false; st.p1 = 0.5; $(".sq-p").value = 50; st.bits = []; setPattern(P0); });
      stop = autoplay(play, speed, { step: () => feed(Math.random() < st.p1 ? 1 : 0), done: () => st.bits.length >= 400, restart: () => { st.bits = []; draw(); } });
      void seed;
      draw();
    },
  });

  dvqExplorers.register({
    views: { seqdet: seqdetView },
    help: {
      seqdet: "מקלידים תבנית ובוחרים Mealy או Moore : הכפתורים 0 ו-1 מזינים ביט, ״ביט אקראי״ ו״הפעלה״ מגרילים לפי ההסתברות שבסליידר. הגרף מדגיש את המצב ואת המעבר שנלקח, הרצועה מראה din, state ו-found, והשורה מתחת אומרת לאן 0 ו-1 יובילו. המתג ״איך נבנה המעבר״ מראה את התבנית מוזזת מתחת לקלט עד ההתאמה הארוכה ביותר, וזה המצב הבא.",
    },
    models: { seqTable, seqFallback, seqRun },
  });
})();
