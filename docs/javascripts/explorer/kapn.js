// kinds: kapn kapgraph
//   kapn                   0044        three digits in a base from 2 to 16 and n up to 1000: the gap D_k against k with the fixed point or the cycle, and a table of the digits after each step, the closed form of the page beside the direct computation
//   kapgraph               0044        three digits in a base from 2 to 20: the chain x -> y -> z as a state diagram (a snake of cards coloured by the gap d, the stage of the proof on each) closed by the fixed point's loop or the 2-cycle's back arrow, and the table of a_n, b_n, c_n, d_n
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { KB_DIGITS, f, ltr, seedControls } = dvqExplorers.lib;
  const NB = " ";

  // Kaprekar's routine on three digits in base B (0044): one step, the direct digits after
  // n steps, and the page's closed forms. d0 is the starting gap (largest digit minus
  // smallest, at least 1), m = |2 d0 − (B + 1)|.
  const kapnDigits = (x, B) => [Math.floor(x / (B * B)), Math.floor(x / B) % B, x % B];
  const kapnStep = (x, B) => {
    const s = kapnDigits(x, B).sort((p, q) => q - p);
    return (s[0] * B * B + s[1] * B + s[2]) - (s[2] * B * B + s[1] * B + s[0]);
  };
  const kapnRun = (x, B, n) => { let y = x; for (let i = 0; i < n; i++) y = kapnStep(y, B); return y; };
  // D_k for k >= 1 (D_0 = d0): the line (B + 1 − 2k + m) / 2 down to B / 2 (even base), or
  // down to h = (B − 1) / 2 and then h, h + 1, h, ... (odd base)
  const kapnGap = (d0, k, B) => {
    if (k === 0) return d0;
    const m = Math.abs(2 * d0 - (B + 1)), line = (B + 1 - 2 * k + m) / 2;
    if (B % 2 === 0) return Math.max(B / 2, line);
    const h = (B - 1) / 2, turn = (m + 2) / 2;          // the k where the line reaches h
    return k <= turn ? line : h + ((k - turn) % 2);
  };
  // The digits after n >= 1 steps by the page's cases, and which case gave them:
  // "first" (n = 1), "line", "fixed" (even base), "even" or "odd" (the parity of n − m/2).
  const kapnFormula = (d0, n, B) => {
    const m = Math.abs(2 * d0 - (B + 1)), b = B - 1;
    if (n === 1) return { a: d0 - 1, b, c: B - d0, m, row: "first" };
    if (B % 2 === 0) {
      if (n <= (3 + m) / 2) return { a: (B + 1 - 2 * n + m) / 2, b, c: (B - 3 + 2 * n - m) / 2, m, row: "line" };
      return { a: B / 2 - 1, b, c: B / 2, m, row: "fixed" };
    }
    if (n <= (m + 4) / 2) return { a: (B + 1 - 2 * n + m) / 2, b, c: (B - 3 + 2 * n - m) / 2, m, row: "line" };
    return (n - m / 2) % 2 === 0 ? { a: (B - 3) / 2, b, c: (B + 1) / 2, m, row: "even" } : { a: (B - 1) / 2, b, c: (B - 1) / 2, m, row: "odd" };
  };

  // The box (0044): a base (fixed on parts a and b), three digits typed or drawn, and n up
  // to 1000; the starting gap and m, a chart of D_k with the line and the fixed point or
  // the cycle, a table of the steps up to the end of the line part plus the chosen n with
  // the closed form beside the direct digits, and the number after n steps.
  const ROW_NAME = { first: "‏n = 1", line: "החלק הליניארי", fixed: "הקבוע", even: `המחזור, ${ltr("n − m/2")} זוגי`, odd: `המחזור, ${ltr("n − m/2")} אי-זוגי` };
  const kapnView = () => ({
    mount(box) {
      const ds = box.dataset, fixed = "fixed" in ds;
      const parse = (text, B) => {
        const t = String(text).trim().toUpperCase();
        if (!/^[0-9A-F]{3}$/.test(t)) return null;
        const v = [...t].map((ch) => KB_DIGITS.indexOf(ch));
        return v.some((d) => d >= B) ? null : v[0] * B * B + v[1] * B + v[2];
      };
      const D = { B: Math.min(16, Math.max(2, Number(ds.b || 10))), n: Math.min(1000, Math.max(1, Number(ds.n || 1000))) };
      D.x = parse(ds.x || "211", D.B) ?? 1;
      const st = { ...D };
      const text = (x) => kapnDigits(x, st.B).map((v) => KB_DIGITS[v]).join("");
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label${fixed ? " hidden" : ""}><span>הבסיס B</span><input type="range" class="kn-b" min="2" max="16" step="1" value="${D.B}" dir="ltr" aria-label="הבסיס, מ-2 עד 16"><output class="kn-out-b"></output></label>` +
        `<label><span>המספר, שלוש ספרות</span><input type="text" class="ex-num kn-x" maxlength="3" dir="ltr" spellcheck="false" aria-label="שלוש ספרות בבסיס, 0 עד 9 ו-A עד F"></label><span class="kn-dec"></span>` +
        `<button type="button" class="md-button ex-random">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err kn-err" aria-live="polite"></span></div>` +
        `<div class="ex-controls ex-play-row"><label><span>‏n, מספר הפעולות</span><input type="range" class="kn-n" min="1" max="1000" step="1" value="${D.n}" dir="ltr" aria-label="מספר הפעולות, עד 1000"><output class="kn-out-n"></output></label>` +
        `<button type="button" class="md-button ex-prev">‏n − 1</button><button type="button" class="md-button md-button--primary ex-next">‏n + 1</button></div>` +
        `<p class="ex-summary kn-start" aria-live="polite"></p>` +
        `<p class="ex-title">הפער ${ltr("D_k")} אחרי ${ltr("k")} פעולות</p><div class="kn-chart"></div>` +
        `<span class="viz-legend"><span><i class="s1"></i>הפער של המספר</span><span><i class="kn-key-line"></i>החלק הליניארי</span><span><i class="ink"></i>נקודת השבת או שני ערכי המחזור</span><span><i class="s2"></i>הצעד ${ltr("k = n − 1")}</span></span>` +
        `<div class="kn-table"></div><p class="ex-summary kn-sum" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const input = $(".kn-x");
      const gapOf = (x) => { const v = kapnDigits(x, st.B); return Math.max(...v) - Math.min(...v); };
      const chart = (d0, lineEnd) => {
        const B = st.B, K = Math.min(24, Math.max(8, lineEnd + 3)), W = 640, Hh = 230, X0 = 40, X1 = 624, Y0 = 14, Y1 = 196;
        const X = (k) => X0 + (k / K) * (X1 - X0), Y = (v) => Y1 - (v / B) * (Y1 - Y0);
        let s = `<svg class="perf-chart kn-svg" viewBox="0 0 ${W} ${Hh}" role="img" aria-label="הפער אחרי כל פעולה, בבסיס ${B}">`;
        const step = B > 10 ? 2 : 1;
        for (let v = 0; v <= B; v += step) s += `<line class="grid" x1="${X0}" x2="${X1}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 6}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        for (let k = 0; k <= K; k += K > 16 ? 2 : 1) s += `<text class="tick" x="${f(X(k))}" y="${Y1 + 17}" text-anchor="middle">${k}</text>`;
        const targets = B % 2 === 0 ? [B / 2] : [(B - 1) / 2, (B + 1) / 2];
        targets.forEach((v) => { s += `<line class="ink-line" x1="${X0}" x2="${X1}" y1="${f(Y(v))}" y2="${f(Y(v))}" stroke-width="1.2" stroke-dasharray="6 4"/>`; });
        // the line part: from k = 1 to its last k, shaded
        const lastK = lineEnd - 1;
        if (lastK > 1) s += `<rect class="kn-line" x="${f(X(1))}" y="${Y0}" width="${f(X(lastK) - X(1))}" height="${Y1 - Y0}"/>`;
        const pts = Array.from({ length: K + 1 }, (_, k) => `${f(X(k))},${f(Y(kapnGap(d0, k, B)))}`);
        s += `<polyline class="s1-line" points="${pts.join(" ")}" fill="none" stroke-width="2.5"/>`;
        for (let k = 0; k <= K; k++) {
          const g = kapnGap(d0, k, B), on = k === st.n - 1;
          s += `<circle class="${on ? "s2-dot" : "s1-dot"}" cx="${f(X(k))}" cy="${f(Y(g))}" r="${on ? 6.5 : 3.5}"><title>k = ${k}${NB}: D = ${g}</title></circle>`;
        }
        if (st.n - 1 > K) s += `<text class="legend halo" x="${X1 - 4}" y="${Y1 - 8}" text-anchor="end">k = ${st.n - 1} →</text>`;
        return s + `<line class="axis" x1="${X0}" x2="${X1}" y1="${Y1}" y2="${Y1}"/><text class="tick" x="${X1}" y="${Y1 + 30}" text-anchor="end">k</text></svg>`;
      };
      const draw = () => {
        const B = st.B, d0 = gapOf(st.x);
        $(".kn-b").value = B; $(".kn-out-b").textContent = String(B);
        $(".kn-n").value = st.n; $(".kn-out-n").textContent = String(st.n);
        if (document.activeElement !== input) input.value = text(st.x);
        $(".kn-dec").innerHTML = `= ${ltr(st.x)} בעשרוני`;
        $(".ex-prev").disabled = st.n <= 1; $(".ex-next").disabled = st.n >= 1000;
        if (d0 === 0) {
          $(".kn-start").innerHTML = `כל הספרות זהות, ולכן ${ltr("d0 = 0")}${NB}: אחרי פעולה אחת מקבלים ${ltr("000")}, ונשארים שם. השאלה מוציאה את המקרה הזה.`;
          $(".kn-chart").innerHTML = ""; $(".kn-table").innerHTML = ""; $(".kn-sum").textContent = "";
          return;
        }
        const m = Math.abs(2 * d0 - (B + 1)), even = B % 2 === 0, lineEnd = even ? (3 + m) / 2 : (m + 4) / 2;
        const sv = kapnDigits(st.x, B);
        $(".kn-start").innerHTML = `הפער ההתחלתי ${ltr(`d0 = ${KB_DIGITS[Math.max(...sv)]} − ${KB_DIGITS[Math.min(...sv)]} = ${d0}`)}, ולכן ${ltr(`m = |2·${d0} − ${B + 1}| = ${m}`)}. ` +
          (even ? `הבסיס זוגי, והחלק הליניארי נגמר ב-${ltr(`n = (3 + m)/2 = ${lineEnd}`)}${NB}: משם המספר קבוע.`
            : `הבסיס אי-זוגי, והחלק הליניארי נגמר ב-${ltr(`n = (m + 4)/2 = ${lineEnd}`)}${NB}: משם המספר מתחלף בין שני ערכים, לפי הזוגיות של ${ltr(`n − m/2 = n − ${m / 2}`)}.`);
        $(".kn-chart").innerHTML = chart(d0, lineEnd);
        const ns = [];
        for (let n = 1; n <= Math.max(2, lineEnd + 2); n++) ns.push(n);
        if (!ns.includes(st.n)) ns.push(st.n);
        let y = st.x, prev = 0, rows = "";
        ns.forEach((n) => {
          y = kapnRun(y, B, n - prev); prev = n;
          const r = kapnFormula(d0, n, B), dir = kapnDigits(y, B), ok = dir[0] === r.a && dir[1] === r.b && dir[2] === r.c;
          const dig = (v) => v.map((q) => KB_DIGITS[q]).join(", ");
          rows += `<tr${n === st.n ? ' class="is-now"' : ""}><td>${ltr(n)}</td><td>${ltr(kapnGap(d0, n - 1, B))}</td><td>${ROW_NAME[r.row]}</td><td>${ltr(`(${dig([r.a, r.b, r.c])})`)}</td><td>${ltr(`(${dig(dir)})`)} ${ok ? "✓" : "✗"}</td></tr>`;
        });
        $(".kn-table").innerHTML = `<div class="at-scroll"><table class="bridge-table kn-steps"><thead><tr><th>‏n</th><th>‏D<sub>n−1</sub></th><th>השורה בנוסחה</th><th>מהנוסחה</th><th>מהחישוב</th></tr></thead><tbody>${rows}</tbody></table></div>`;
        const r = kapnFormula(d0, st.n, B), val = (r.a * B + r.b) * B + r.c, g = kapnGap(d0, st.n - 1, B);
        $(".kn-sum").innerHTML = `אחרי ${ltr(st.n)} פעולות${NB}: ${ltr(`(${KB_DIGITS[r.a]}, ${KB_DIGITS[r.b]}, ${KB_DIGITS[r.c]})_${B} = ${val}`)}, כלומר ${ltr(`(B² − 1) · D = ${B * B - 1} · ${g}`)}. ` +
          (r.row === "fixed" ? `זה המספר הקבוע של הבסיס.` : r.row === "even" || r.row === "odd" ? `זה אחד משני המספרים של המחזור, והצעד הבא נותן את השני.` : `עוד לא הגענו לסוף החלק הליניארי.`);
      };
      const setX = (x) => { st.x = x; $(".kn-err").textContent = ""; draw(); };
      input.addEventListener("change", () => { const x = parse(input.value, st.B); if (x === null) $(".kn-err").textContent = `שלוש ספרות מ-0 עד ${KB_DIGITS[st.B - 1]}`; else setX(x); });
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      $(".kn-b").addEventListener("input", () => {
        const B = Number($(".kn-b").value), v = kapnDigits(st.x, st.B).map((d) => Math.min(d, B - 1));
        st.B = B; st.x = (v[0] * B + v[1]) * B + v[2]; draw();
      });
      $(".kn-n").addEventListener("input", () => { st.n = Number($(".kn-n").value); draw(); });
      $(".ex-next").addEventListener("click", () => { if (st.n < 1000) st.n++; draw(); });
      $(".ex-prev").addEventListener("click", () => { if (st.n > 1) st.n--; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, D); setX(D.x); });
      const seed = seedControls(box, $(".ex-random"), (rng) => {
        let x;
        do x = Math.floor(rng() * st.B ** 3); while (gapOf(x) === 0);
        setX(x);
      });
      $(".ex-random").addEventListener("click", () => seed.draw());
      draw();
    },
  });

  // The chain of one number (0044, the box at the top): x_0, x_1, ... until a value comes
  // back; the cycle it ends in (length 1, the fixed point or 000, or 2), and for every
  // node its digits, its gap d and its stage in the proof.
  const KG_DIGITS = "0123456789ABCDEFGHIJ";
  const kapgChain = (x, B) => {
    const nodes = [x], seen = new Map([[x, 0]]);
    for (;;) {
      const y = kapnStep(nodes[nodes.length - 1], B);
      if (seen.has(y)) return { nodes, cycleStart: seen.get(y), cycleLen: nodes.length - seen.get(y) };
      seen.set(y, nodes.length);
      nodes.push(y);
    }
  };
  // the stage of node n of a chain with starting gap d0: "start", "zero" (all digits equal),
  // "first" (n = 1), "line", "fixed" or "cycle", by the rows of the page's closed form
  const kapgStage = (d0, n, B) => {
    if (n === 0) return "start";
    if (d0 === 0) return "zero";
    const row = kapnFormula(d0, n, B).row;
    return row === "even" || row === "odd" ? "cycle" : row;
  };

  // The state diagram box (0044, after the statement): a base from 2 to 20 and three
  // digits; the chain as cards in a snake (right to left, then left to right; one column
  // on a narrow screen), each card with the number in the base, its decimal value, its
  // gap d (the card's shade) and its stage; the fixed point's loop or the 2-cycle's back
  // arrow; the table of a_n, b_n, c_n and d_n with the closed form checked, and a tap on a
  // card or a row picks that step.
  const STAGE_NAME = { start: "התחלה", zero: "הכול 0", first: "צעד ראשון", line: "חלק ליניארי", fixed: "נקודת שבת", cycle: "מחזור" };
  let kgUid = 0;
  const kapgraphView = () => ({
    mount(box) {
      const uid = ++kgUid;
      const parse = (text, B) => {
        const t = String(text).trim().toUpperCase();
        if (!/^[0-9A-J]{3}$/.test(t)) return null;
        const v = [...t].map((ch) => KG_DIGITS.indexOf(ch));
        return v.some((d) => d >= B) ? null : (v[0] * B + v[1]) * B + v[2];
      };
      const D = { B: Math.min(20, Math.max(2, Number(box.dataset.b || 10))) };
      D.x = parse(box.dataset.x || "211", D.B) ?? 1;
      const st = { ...D, sel: null };
      const txt = (x, B = st.B) => kapnDigits(x, B).map((v) => KG_DIGITS[v]).join("");
      const gapOf = (x) => { const v = kapnDigits(x, st.B); return Math.max(...v) - Math.min(...v); };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>הבסיס B</span><input type="range" class="kg-b" min="2" max="20" step="1" value="${D.B}" dir="ltr" aria-label="הבסיס, מ-2 עד 20"><output class="kg-out-b"></output></label>` +
        `<label><span>המספר, שלוש ספרות</span><input type="text" class="ex-num kg-x" maxlength="3" dir="ltr" spellcheck="false" aria-label="שלוש ספרות בבסיס, 0 עד 9 ו-A עד J"></label><span class="kg-dec"></span>` +
        `<button type="button" class="md-button ex-random">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err kg-err" aria-live="polite"></span></div>` +
        `<p class="ex-summary kg-sum" aria-live="polite"></p><div class="kg-graph"></div>` +
        `<span class="viz-legend"><span><i class="kg-key-lo"></i>פער d קטן</span><span><i class="kg-key-hi"></i>פער d גדול</span><span><i class="kg-key-end"></i>נקודת שבת או מחזור</span></span>` +
        `<p class="wv-step kg-step" aria-live="polite"></p><div class="kg-table"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const input = $(".kg-x");
      // the stage shown on a card and in the table: the cycle (or the fixed point) once the
      // chain is in it, the row of the closed form before that
      const labelOf = (ch, d0, i) => (i === 0 ? "start" : d0 === 0 ? "zero" : i >= ch.cycleStart ? (ch.cycleLen === 1 ? "fixed" : "cycle") : kapgStage(d0, i, st.B));
      const graph = (ch, d0) => {
        const B = st.B, n = ch.nodes.length, narrow = box.clientWidth > 0 && box.clientWidth < 520;
        const cols = narrow ? 1 : 4, CW = 108, CH = 64, GX = 44, TAG = 18, GY = 58, PAD = 18;
        // the slots: a 2-cycle keeps its two cards on one row
        const slots = [];
        let r = 0, c = 0;
        ch.nodes.forEach((_, i) => {
          if (cols > 1 && ch.cycleLen === 2 && i === ch.cycleStart && c === cols - 1) { r++; c = 0; }
          slots.push([r, c]);
          c++; if (c === cols) { r++; c = 0; }
        });
        const rows = slots[n - 1][0] + 1, W = 2 * PAD + cols * CW + (cols - 1) * GX + (cols === 1 ? 70 : 0);
        const H = PAD + rows * (TAG + CH + GY) + 6;
        const pos = slots.map(([rr, cc]) => {
          const slot = rr % 2 === 0 ? cols - 1 - cc : cc;           // right to left on even rows
          return { x: PAD + (cols === 1 ? 70 : 0) + slot * (CW + GX), y: PAD + rr * (TAG + CH + GY) + TAG, row: rr };
        });
        const head = `kg-ah-${uid}`;
        let s = `<svg class="figure kg-svg" viewBox="0 0 ${W} ${H}" style="max-width:${W}px" role="group" aria-label="דיאגרמת המצבים של המספר ${txt(st.x)} בבסיס ${B}">` +
          `<defs><marker id="${head}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="kg-head"/></marker>` +
          `<marker id="${head}-end" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="kg-head-end"/></marker></defs>`;
        const arrow = (d, cls = "") => `<path class="kg-arrow${cls}" d="${d}" marker-end="url(#${head}${cls ? "-end" : ""})"/>`;
        // the forward arrows
        for (let i = 0; i + 1 < n; i++) {
          const a = pos[i], b = pos[i + 1];
          if (a.row === b.row) {
            const left = b.x < a.x;
            s += arrow(`M${left ? a.x : a.x + CW},${a.y + CH / 2} L${left ? b.x + CW + 2 : b.x - 2},${b.y + CH / 2}`);
          } else {                                      // to the next row: down, across if needed, down
            const mid = a.y + CH + (GY - 4) / 2;
            s += arrow(`M${a.x + CW / 2},${a.y + CH} V${mid} H${b.x + CW / 2} V${b.y - TAG - 2}`);
          }
        }
        // closing the cycle: a loop under the fixed point, a back arrow for the 2-cycle
        const last = pos[n - 1];
        if (ch.cycleLen === 1) {
          s += arrow(`M${last.x + CW * 0.3},${last.y + CH} C${last.x + CW * 0.2},${last.y + CH + 40} ${last.x + CW * 0.8},${last.y + CH + 40} ${last.x + CW * 0.7},${last.y + CH + 2}`, " is-end");
        } else {
          const p = pos[ch.cycleStart];
          if (p.row === last.row) s += arrow(`M${last.x + CW / 2},${last.y + CH} C${last.x + CW / 2},${last.y + CH + 44} ${p.x + CW / 2},${p.y + CH + 44} ${p.x + CW / 2},${p.y + CH + 2}`, " is-end");
          else s += arrow(`M${last.x},${last.y + CH / 2} C${last.x - 60},${last.y + CH / 2} ${p.x - 60},${p.y + CH / 2} ${p.x - 2},${p.y + CH / 2}`, " is-end");
        }
        ch.nodes.forEach((x, i) => {
          const { x: px, y: py } = pos[i], d = gapOf(x), stage = labelOf(ch, d0, i), end = i >= ch.cycleStart;
          const shade = Math.round(8 + (52 * d) / Math.max(1, B - 1));
          s += `<g class="kg-node${end ? " is-end" : ""}${st.sel === i ? " is-sel" : ""}" data-i="${i}" tabindex="0" role="button" aria-label="צעד ${i}${NB}: ${txt(x)} בבסיס ${B}, ${x} בעשרוני, d = ${d}, ${STAGE_NAME[stage]}">` +
            `<text class="kg-tag" x="${px + CW / 2}" y="${py - 6}" text-anchor="middle" direction="rtl">${i === 0 ? "" : `n = ${i} · `}${STAGE_NAME[stage]}</text>` +
            `<rect class="kg-card" x="${px}" y="${py}" width="${CW}" height="${CH}" rx="9" style="--kg-t:${shade}%"/>` +
            `<text class="kg-num" x="${px + CW / 2}" y="${py + 29}" text-anchor="middle">${txt(x)}${B === 10 ? "" : `<tspan class="kg-base" dy="5">${B}</tspan>`}</text>` +
            `<text class="kg-sub" x="${px + CW / 2}" y="${py + 52}" text-anchor="middle">${B === 10 ? "" : `= ${x} · `}d = ${d}</text></g>`;
        });
        return s + "</svg>";
      };
      const draw = () => {
        const B = st.B, ch = kapgChain(st.x, B), d0 = gapOf(st.x), k = ch.cycleStart, n = ch.nodes.length;
        $(".kg-b").value = B; $(".kg-out-b").textContent = String(B);
        if (document.activeElement !== input) input.value = txt(st.x);
        $(".kg-dec").innerHTML = `= ${ltr(st.x)} בעשרוני`;
        const cyc = ch.nodes.slice(k).map((v) => txt(v));
        $(".kg-sum").innerHTML = d0 === 0 ? `כל הספרות זהות, ולכן ${ltr("d0 = 0")}${NB}: אחרי פעולה אחת מקבלים ${ltr("000")}, ונשארים שם.`
          : `הפער ההתחלתי ${ltr(`d0 = ${d0}`)}. ` + (ch.cycleLen === 1
            ? `בסיס ${ltr(B)} זוגי, והמספר מגיע לנקודת השבת <b>${ltr(cyc[0])}</b> (${ltr(ch.nodes[k])} בעשרוני, ${ltr(`d = ${B / 2}`)}) אחרי ${ltr(k)} ${k === 1 ? "צעד" : "צעדים"}.`
            : `בסיס ${ltr(B)} אי-זוגי, ואין נקודת שבת${NB}: אחרי ${ltr(k)} ${k === 1 ? "צעד" : "צעדים"} המספר נכנס למחזור <b>${ltr(`${cyc[0]} ↔ ${cyc[1]}`)}</b>, והפער מתחלף בין ${ltr((B - 1) / 2)} ל-${ltr((B + 1) / 2)}.`);
        $(".kg-graph").innerHTML = graph(ch, d0);
        // the table of the sequences
        let rows = "";
        const all = ch.nodes.concat([ch.nodes[k]]);
        all.forEach((x, i) => {
          const dg = kapnDigits(x, B), d = gapOf(x), stage = labelOf(ch, d0, Math.min(i, n - 1));
          let check = "—";
          if (i > 0 && d0 > 0) { const f = kapnFormula(d0, i, B); check = f.a === dg[0] && f.b === dg[1] && f.c === dg[2] && kapnGap(d0, i, B) === d ? "✓" : "✗"; }
          const cls = [st.sel === i ? "is-now" : "", i === n ? "kg-repeat" : ""].filter(Boolean).join(" ");
          rows += `<tr data-i="${i}"${cls ? ` class="${cls}"` : ""}><td>${ltr(i)}</td><td>${ltr(txt(x))}</td><td>${ltr(KG_DIGITS[dg[0]])}</td><td>${ltr(KG_DIGITS[dg[1]])}</td><td>${ltr(KG_DIGITS[dg[2]])}</td><td>${ltr(d)}</td><td>${i === n ? "חוזר" : STAGE_NAME[stage]}</td><td>${check}</td></tr>`;
        });
        $(".kg-table").innerHTML = `<div class="at-scroll"><table class="bridge-table kg-steps"><thead><tr><th>‏n</th><th>המספר</th><th>‏a<sub>n</sub></th><th>‏b<sub>n</sub></th><th>‏c<sub>n</sub></th><th>‏d<sub>n</sub></th><th>השלב</th><th>הנוסחה</th></tr></thead><tbody>${rows}</tbody></table></div>`;
        const i = st.sel;
        if (i === null || i >= all.length) $(".kg-step").innerHTML = d0 ? `לחיצה על כרטיס או על שורה מסבירה את הצעד. השורה האחרונה בטבלה היא הערך שחוזר, וממנו המעגל נסגר.` : "";
        else {
          const x = all[i], d = gapOf(x), stage = i === n ? labelOf(ch, d0, k) : labelOf(ch, d0, i), prevD = i ? gapOf(all[i - 1]) : null;
          $(".kg-step").innerHTML = i === 0 ? `המספר ההתחלתי ${ltr(txt(x))}, עם הפער ${ltr(`d0 = ${d}`)}.`
            : `צעד ${ltr(i)}${NB}: הפער הקודם היה ${ltr(prevD)}, ולכן ההפרש הוא ${ltr(`${prevD} · (B² − 1) = ${prevD} · ${B * B - 1} = ${x}`)}, עם הספרות ${ltr(`(d − 1, B − 1, B − d) = (${kapnDigits(x, B).map((v) => KG_DIGITS[v]).join(", ")})`)}. ` +
              `הפער החדש ${ltr(`max(${prevD} − 1, ${B} − ${prevD}) = ${d}`)}` + (stage === "line" ? `, אחד פחות מהקודם${NB}: החלק הליניארי.` : stage === "fixed" ? `${NB}: ${ltr(`d = B/2`)}, נקודת השבת.` : stage === "cycle" ? `${NB}: המחזור בין ${ltr((B - 1) / 2)} ל-${ltr((B + 1) / 2)}.` : stage === "first" ? `${NB}: אחרי צעד אחד הפער כבר לפחות ${ltr(`(B − 1)/2`)}.` : ".");
        }
      };
      const setX = (x) => { st.x = x; st.sel = null; $(".kg-err").textContent = ""; draw(); };
      const pick = (i) => { st.sel = st.sel === i ? null : i; draw(); };
      $(".kg-graph").addEventListener("click", (e) => { const g = e.target.closest(".kg-node"); if (g) pick(Number(g.dataset.i)); });
      $(".kg-graph").addEventListener("keydown", (e) => { const g = e.target.closest(".kg-node"); if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); pick(Number(g.dataset.i)); const again = box.querySelector(`.kg-node[data-i="${g.dataset.i}"]`); if (again) again.focus(); } });
      $(".kg-table").addEventListener("click", (e) => { const tr = e.target.closest("tr[data-i]"); if (tr) pick(Number(tr.dataset.i)); });
      input.addEventListener("change", () => { const x = parse(input.value, st.B); if (x === null) $(".kg-err").textContent = `שלוש ספרות מ-0 עד ${KG_DIGITS[st.B - 1]}`; else setX(x); });
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      $(".kg-b").addEventListener("input", () => {
        const B = Number($(".kg-b").value), v = kapnDigits(st.x, st.B).map((d) => Math.min(d, B - 1));
        st.B = B; setX((v[0] * B + v[1]) * B + v[2]);
      });
      $(".ex-reset").addEventListener("click", () => { st.B = D.B; setX(D.x); });
      const seed = seedControls(box, $(".ex-random"), (rng) => { let x; do x = Math.floor(rng() * st.B ** 3); while (gapOf(x) === 0); setX(x); });
      $(".ex-random").addEventListener("click", () => seed.draw());
      // one column below 520 px: redraw when the box crosses that width
      let wasNarrow = null;
      if (typeof ResizeObserver !== "undefined") new ResizeObserver(() => { const nw = box.clientWidth < 520; if (nw !== wasNarrow) { wasNarrow = nw; draw(); } }).observe(box);
      draw();
    },
  });

  dvqExplorers.register({
    views: { kapn: kapnView, kapgraph: kapgraphView },
    help: {
      kapn: "מקלידים שלוש ספרות או מגרילים, ובוחרים n עד 1000 (ובסעיף הבונוס גם בסיס) : הגרף מראה את הפער D_k אחרי כל פעולה, והטבלה משווה בכל צעד את הספרות מהנוסחה של העמוד לספרות מהחישוב הישיר, עם השורה בנוסחה שנתנה אותן.",
      kapgraph: "בוחרים בסיס מ-2 עד 20 ומקלידים שלוש ספרות : הדיאגרמה מראה את המספרים שהפעולה עוברת בהם, כל כרטיס בצבע לפי הפער d ועם השלב בהוכחה, עד הלולאה של נקודת השבת או החץ החוזר של המחזור. הטבלה מפרטת את a_n, b_n, c_n ו-d_n, ולחיצה על כרטיס או על שורה מסבירה את הצעד.",
    },
    models: { kapnDigits, kapnStep, kapnRun, kapnGap, kapnFormula, kapgChain, kapgStage },
  });
})();
