// kinds: kapn
//   kapn                   0044        three digits in a base from 2 to 16 and n up to 1000: the gap D_k against k with the fixed point or the cycle, and a table of the digits after each step, the closed form of the page beside the direct computation
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

  dvqExplorers.register({
    views: { kapn: kapnView },
    help: {
      kapn: "מקלידים שלוש ספרות או מגרילים, ובוחרים n עד 1000 (ובסעיף הבונוס גם בסיס) : הגרף מראה את הפער D_k אחרי כל פעולה, והטבלה משווה בכל צעד את הספרות מהנוסחה של העמוד לספרות מהחישוב הישיר, עם השורה בנוסחה שנתנה אותן.",
    },
    models: { kapnDigits, kapnStep, kapnRun, kapnGap, kapnFormula },
  });
})();
