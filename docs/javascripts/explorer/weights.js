// kinds: weights
//   weights                0064        a load n weighed with k weights: one pan (base 2), two pans (balanced base 3), or c copies of each weight on two pans (balanced base 2c + 1) or one pan (base c + 1); the conversion stepped digit by digit (n mod B, the digit, the carry) with the weights moving onto their pans, the digits and the bound of k weights against what they reach
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, explain, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const MINUS = "−";
  const num = (v) => (v < 0 ? `${MINUS}${-v}` : String(v));

  // The modes of the box: the pans and whether there are c copies of every weight.
  const MODES = {
    one: { two: false, copies: false, k0: 6, kmax: 7, code: "one_pan", label: "כף אחת (סעיף א)" },
    two: { two: true, copies: false, k0: 4, kmax: 5, code: "two_pans", label: "שתי כפות (סעיף ב)" },
    copies: { two: true, copies: true, k0: 3, kmax: 3, code: "balances", label: "c עותקים, שתי כפות (סעיף ג)" },
    copies1: { two: false, copies: true, k0: 3, kmax: 4, code: "balances", label: "c עותקים, כף אחת (סעיף ג)" },
  };
  const CMIN = 2, CMAX = 4;

  // The base is the number of states of one weight value: -c..c on two pans, 0..c on one.
  const wtBase = (c, two) => (two ? 2 * c + 1 : c + 1);
  // The bound of k values: every placement is a coefficient vector; on two pans the empty
  // one weighs 0 and a vector and its mirror weigh opposite loads.
  const wtBound = (k, c, two) => { const b = wtBase(c, two); return two ? (b ** k - 1) / 2 : b ** k - 1; };
  // The conversion step by step, as the page's code runs it: the remainder n mod B, the
  // digit (a remainder above c on two pans becomes r - B, with a carry of 1) and n after.
  const wtSteps = (n, k, c, two) => {
    const b = wtBase(c, two), rows = [];
    for (let i = 0; i < k; i++) {
      const r = n % b, d = two && r > c ? r - b : r, after = (n - d) / b;
      rows.push({ i, w: b ** i, before: n, r, d, carry: d < 0 ? 1 : 0, after });
      n = after;
    }
    return rows;
  };
  const wtDigits = (n, k, c, two) => { const rows = wtSteps(n, k, c, two); return rows.length && rows[rows.length - 1].after !== 0 ? null : rows.map((x) => x.d); };
  // What weights reach: the largest N with every load 1..N weighed by coefficients lo..hi,
  // found by trying every vector.
  const wtReach = (weights, lo, hi) => {
    let vals = new Set([0]);
    weights.forEach((w) => { const next = new Set(); vals.forEach((v) => { for (let e = lo; e <= hi; e++) next.add(v + e * w); }); vals = next; });
    let n = 0;
    while (vals.has(n + 1)) n++;
    return n;
  };

  // the solution's steps, as chips of the explanation panel, per mode
  const STEPS = {
    one: ["השארית n mod 2", "ביט 1 : המשקולת לכף השנייה", "חילוק ב-2", "הסוף : n = 0"],
    two: ["השארית n mod 3", "שארית 2 : הספרה <bdi dir=\"ltr\">−1</bdi> והעברה", "חילוק ב-3", "הסוף : n = 0"],
    copies: ["הבסיס B = 2c + 1", "השארית n mod B", "שארית מעל c : הספרה r − B והעברה", "חילוק ב-B", "הבדיקה"],
    copies1: ["הבסיס B = c + 1", "השארית n mod B", "שארית מעל c : הספרה r − B והעברה", "חילוק ב-B", "הבדיקה"],
  };
  // the lines of the page's code each part of a step runs, per mode and language
  const LINES = {
    one: { init: { py: [4], sv: [4] }, step: () => ({ py: [5, 6, 7], sv: [5, 6, 7] }), end: { py: [8], sv: [9] } },
    two: { init: { py: [4], sv: [4, 5] }, step: (neg) => ({ py: [5, 6, 7, ...(neg ? [8] : []), 9, 10], sv: [6, 7, 8, 9, 10] }), end: { py: [11], sv: [12] } },
    copies: { init: { py: [5, 6], sv: [4, 5] }, step: (neg) => ({ py: [7, 8, 9, ...(neg ? [10] : []), 11, 12], sv: [6, 7, 8, 9, 10] }), end: { py: [13, 19, 20, 21, 22, 23], sv: [12, 18, 19, 20, 21, 22, 24] } },
  };
  LINES.copies1 = LINES.copies;

  const weightsView = () => ({
    mount(box) {
      const m0 = MODES[box.dataset.mode] ? box.dataset.mode : "two";
      const d0 = { mode: m0, k: Number(box.dataset.k || MODES[m0].k0), c: MODES[m0].copies ? Number(box.dataset.c || 2) : 2, n: Number(box.dataset.n || 25) };
      const st = { ...d0, s: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הסעיף <select class="wt-mode" aria-label="כף אחת, שתי כפות, או c עותקים מכל משקולת">${Object.entries(MODES).map(([v, m]) => `<option value="${v}">${m.label}</option>`).join("")}</select></label>` +
        `<label class="wt-lab"><span>משקלים ${ltr("k")}</span><input type="range" class="wt-k" min="1" max="7" step="1" dir="ltr" aria-label="מספר המשקלים השונים"><output class="wt-ko"></output></label>` +
        `<label class="wt-lab wt-clab"><span>עותקים ${ltr("c")}</span><input type="range" class="wt-c" min="${CMIN}" max="${CMAX}" step="1" dir="ltr" aria-label="כמה עותקים מכל משקולת"><output class="wt-co"></output></label>` +
        `<label class="wt-lab"><span>המשא ${ltr("n")}</span><input type="range" class="wt-n" min="1" max="40" step="1" dir="ltr" aria-label="המשא"><output class="wt-no"></output></label>` +
        `<button type="button" class="md-button wt-rand">משא אקראי</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">לפני הספרה הראשונה</button>` +
        `<button type="button" class="md-button ex-prev">הספרה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הספרה הבאה</button>` +
        `<button type="button" class="md-button ex-end">כל הספרות</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1600, 1000, 450) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary wt-sum" aria-live="polite"></p>` +
        `<div class="wt-wrap" data-fig-strip></div>` +
        `<span class="viz-legend"><span><i class="wt-key-load"></i>המשא</span><span><i class="wt-key-other"></i>בכף השנייה</span><span class="wt-two"><i class="wt-key-beside"></i>ליד המשא</span>` +
        `<span><i class="wt-key-off"></i>בחוץ</span><span><i class="wt-key-wait"></i>עוד לא הוחלט</span><span><i class="wt-key-now"></i>הצעד הנוכחי</span></span>` +
        `<div class="wt-digits at-scroll" tabindex="0" aria-label="הספרות של המשא"></div>` +
        `<p class="wt-sums"></p><p class="wt-note"></p>` +
        `<p class="ex-title">ההמרה, ספרה אחר ספרה</p><div class="wt-conv at-scroll" tabindex="0" aria-label="טבלת ההמרה"></div>`;
      const show = explain(box, "הסבר : השלבים של הפתרון והקוד");
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const mode = () => MODES[st.mode];
      const cOf = () => (mode().copies ? st.c : 1);
      const reachOf = () => wtBound(st.k, cOf(), mode().two);

      // the balance, level and of one size through the steps: the load and k slots beside it
      // (two pans) on the left pan, k slots on the other pan, and under the beam a row of the
      // copies not on a pan; a slot holds the copies of one weight, the heaviest on the left
      const geom = () => (box.clientWidth && box.clientWidth < 520 ? { W: 320, LW: 38, S: 34, BH: 26 } : { W: 640, LW: 54, S: 46, BH: 24 });
      const svg = (rows) => {
        const g = geom(), m = mode(), c = cOf(), k = st.k, two = m.two, BH = g.BH, LH = 36;
        const half = g.W / 2 - (g.W < 640 ? 8 : 14);
        const S = Math.min(g.S, Math.floor((half - (two ? g.LW + 8 : 0)) / k));
        const SH = c * BH, top = 6, BY = top + Math.max(SH, LH), OY = BY + 40 + SH, H = OY + 8;
        const lc = g.W * 0.25, rc = g.W * 0.75;
        const xs = (center) => Array.from({ length: k }, (_, p) => center - (k * S) / 2 + p * S + S / 2);
        const right = xs(rc), off = xs(g.W / 2);
        let loadX, left = [];
        if (two) {
          const x0 = lc - (g.LW + 8 + k * S) / 2;
          loadX = x0 + g.LW / 2;
          left = Array.from({ length: k }, (_, p) => x0 + g.LW + 8 + p * S + S / 2);
        } else loadX = lc;
        const bhalf = Math.max(g.W / 2 - (loadX - g.LW / 2) + 8, right[k - 1] + S / 2 + 8 - g.W / 2);
        const block = (x, y, w, cls, title) =>
          `<g class="wt-w ${cls}"><title>${title}</title><rect x="${(x - S / 2 + 2).toFixed(1)}" y="${y}" width="${S - 4}" height="${BH - 3}" rx="3"/>` +
          `<text class="wt-num" x="${x.toFixed(1)}" y="${y + BH / 2 + 3}" text-anchor="middle">${w}</text></g>`;
        let s = `<svg class="figure wt-fig wt-live" viewBox="0 0 ${g.W} ${H}" role="img" aria-label="המאזניים : המשא ${st.n} והמשקולות שהוצבו עד עכשיו">` +
          `<path class="wt-stand" d="M${g.W / 2 - 22},${BY + 28} L${g.W / 2},${BY + 4} L${g.W / 2 + 22},${BY + 28} Z"/>` +
          `<line class="wt-beam" x1="${(g.W / 2 - bhalf).toFixed(1)}" y1="${BY + 3}" x2="${(g.W / 2 + bhalf).toFixed(1)}" y2="${BY + 3}"/>` +
          `<g class="wt-load"><title>the load: ${st.n}</title><rect x="${(loadX - g.LW / 2).toFixed(1)}" y="${BY - LH}" width="${g.LW}" height="${LH}" rx="5"/>` +
          `<text class="wt-num" x="${loadX.toFixed(1)}" y="${BY - LH / 2 + 5}" text-anchor="middle">${st.n}</text></g>`;
        rows.forEach((row, i) => {
          const p = k - 1 - i, decided = i < st.s, d = decided ? row.d : 0, now = i === st.s - 1 ? " is-now" : "";
          const where = d > 0 ? right : left;
          for (let j = 0; j < Math.abs(d); j++) s += block(where[p], BY - (j + 1) * BH, row.w, `${d > 0 ? "is-other" : "is-beside"}${now}`, `weight ${row.w}: ${d > 0 ? "the other pan" : "beside the load"}`);
          for (let j = 0; j < c - Math.abs(d); j++) s += block(off[p], OY - (j + 1) * BH, row.w, decided ? `is-off${now}` : "is-wait", `weight ${row.w}: ${decided ? "off the scale" : "not decided yet"}`);
        });
        s += `<line class="wt-off-line" x1="${(off[0] - S / 2).toFixed(1)}" y1="${OY}" x2="${(off[k - 1] + S / 2).toFixed(1)}" y2="${OY}"/>`;
        return s + "</svg>";
      };

      // the digits under the weights: a column per weight, the heaviest on the left as the
      // number is written, the digit -1 (any negative digit) marked, the current one framed
      const digitsTable = (rows) => {
        const cols = rows.slice().reverse();
        const cell = (row, html) => `<td class="${row.i < st.s && row.d < 0 ? "is-neg" : ""}${row.i === st.s - 1 ? " is-now" : ""}">${html}</td>`;
        const where = (d) => (d > 0 ? "מול" : d < 0 ? "ליד" : "בחוץ");
        const many = (d) => (Math.abs(d) > 1 ? `${Math.abs(d)} × ` : "");
        return `<table class="wt-dtab" dir="ltr"><tbody>` +
          `<tr>${cols.map((r) => `<td class="wt-wh">${r.w}</td>`).join("")}<th dir="rtl">המשקולת</th></tr>` +
          `<tr>${cols.map((r) => cell(r, r.i < st.s ? num(r.d) : "·")).join("")}<th dir="rtl">הספרה</th></tr>` +
          `<tr class="wt-where">${cols.map((r) => cell(r, r.i < st.s ? `<span dir="rtl">${many(r.d)}${where(r.d)}</span>` : "")).join("")}<th dir="rtl">מול המשא או לידו</th></tr>` +
          `</tbody></table>`;
      };

      // the conversion table: a row per digit, every row in place from the start (the rows
      // not reached yet are empty), so the table keeps its size through the steps
      const convTable = (rows, b, two) => {
        const head = ["הצעד", "המשקולת", "המספר", `השארית mod ${b}`, "הספרה", ...(two ? ["ההעברה"] : []), "המספר אחרי"];
        return `<table class="wt-ctab"><thead><tr>${head.map((h) => `<th>${h}</th>`).join("")}</tr></thead><tbody>` +
          rows.map((r) => {
            const on = r.i < st.s;
            const v = (x) => (on ? x : " ");
            return `<tr class="${r.i === st.s - 1 ? "is-now" : ""}${on ? "" : " is-later"}"><td>${r.i + 1}</td><td>${r.w}</td><td>${v(r.before)}</td><td>${v(r.r)}</td>` +
              `<td class="${on && r.d < 0 ? "is-neg" : ""}">${on ? `<bdi dir="ltr">${num(r.d)}</bdi>` : " "}</td>${two ? `<td>${v(r.carry)}</td>` : ""}<td>${v(r.after)}</td></tr>`;
          }).join("") + `</tbody></table>`;
      };

      const draw = () => {
        const m = mode(), c = cOf(), two = m.two, b = wtBase(c, two), k = st.k;
        const R = reachOf();
        st.n = Math.min(Math.max(1, st.n), R);
        st.s = Math.min(Math.max(st.s, 0), k);
        const rows = wtSteps(st.n, k, c, two), cur = st.s ? rows[st.s - 1] : null, done = st.s === k;
        box.classList.toggle("wt-is-two", two);
        box.classList.toggle("wt-is-copies", m.copies);
        $(".wt-mode").value = st.mode;
        $(".wt-k").max = String(m.kmax); $(".wt-k").value = String(k); $(".wt-ko").textContent = String(k);
        $(".wt-c").value = String(st.c); $(".wt-co").textContent = String(st.c);
        $(".wt-clab").hidden = !m.copies;
        $(".wt-n").max = String(R); $(".wt-n").value = String(st.n); $(".wt-no").textContent = String(st.n);
        $(".ex-pos").textContent = `ספרה ${st.s} מתוך ${k}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        // the bound of k values against what the weights b^i reach, found by trying every vector
        const weights = rows.map((r) => r.w), got = wtReach(weights, two ? -c : 0, c);
        const states = two ? (m.copies ? `מ-${ltr(`${MINUS}${c}`)} עד ${ltr(c)} עותקים נטו בכף השנייה` : "בכף השנייה, ליד המשא או בחוץ") : (m.copies ? `מ-0 עד ${ltr(c)} עותקים בכף` : "בכף או בחוץ");
        const formula = two ? `(${b}^${k} − 1) / 2` : `${b}^${k} − 1`;
        $(".wt-sum").innerHTML = `${m.copies ? `${ltr(`c = ${c}`)} עותקים מכל משקל, ` : ""}${ltr(`k = ${k}`)} ${m.copies ? "משקלים" : "משקולות"}${NB}: לכל ${m.copies ? "משקל" : "משקולת"} ${ltr(b)} מצבים (${states}), ולכן ${ltr(b ** k)} הצבות. ` +
          `<b>החסם${NB}: ${ltr(`${formula} = ${R}`)}</b>${two ? ", כי ההצבה הריקה שוקלת 0 והמראה של הצבה שוקלת את הנגדי" : ", בלי ההצבה הריקה"}. ` +
          `המשקולות ${ltr(weights.join(", "))}${m.copies ? `, ${ltr(c)} מכל אחת (${ltr(k * c)} משקולות),` : ""} שוקלות בפועל כל משא עד ${ltr(got)} ${got === R ? "✓" : "✗"} (בדיקה של כל ההצבות).`;
        $(".wt-wrap").innerHTML = svg(rows);
        $(".wt-digits").innerHTML = digitsTable(rows);
        $(".wt-conv").innerHTML = convTable(rows, b, two);
        // the two pans so far, and what is still to place: n = sum of the placed digits + B^s * rest
        const placed = rows.slice(0, st.s);
        const side = (sign) => placed.filter((r) => Math.sign(r.d) === sign).flatMap((r) => Array(Math.abs(r.d)).fill(r.w)).reverse();
        const bes = side(-1), oth = side(1), sum = (a) => a.reduce((x, y) => x + y, 0);
        const rest = cur ? cur.after : st.n, gap = st.n + sum(bes) - sum(oth);
        const loadSide = [st.n, ...bes].join(" + "), otherSide = oth.length ? oth.join(" + ") : "0";
        $(".wt-sums").innerHTML = `כף המשא${NB}: ${ltr(`${loadSide} = ${st.n + sum(bes)}`)} · הכף השנייה${NB}: ${ltr(`${otherSide}${oth.length > 1 ? ` = ${sum(oth)}` : ""}`)}` +
          (gap === 0 ? ` · <b>מאוזן ✓</b>` : ` · עוד חסר בכף השנייה${NB}: ${ltr(`${gap} = ${b}^${st.s} · ${rest}`)}, המספר שנשאר כפול המשקולת הבאה`);
        // the caption: what the step did and why
        let note;
        if (!cur) note = `המשא ${ltr(st.n)}, כל המשקולות בחוץ. בכל צעד מסתכלים על השארית ${ltr(`n mod ${b}`)}${NB}: היא הספרה הנמוכה של ${ltr("n")} בבסיס ${ltr(b)}, והיא אומרת כמה עותקים של המשקולת הקלה ביותר שנשארה צריך ובאיזו כף.`;
        else {
          const w = ltr(cur.w), cnt = Math.abs(cur.d) > 1 ? `${Math.abs(cur.d)} עותקים של ` : "";
          const head = `ספרה ${st.s}, המשקולת ${w}${NB}: ${ltr(`${cur.before} mod ${b} = ${cur.r}`)}. `;
          if (cur.d < 0) note = head + `השארית ${ltr(cur.r)} גדולה מ-${ltr(c)}, ואין ${ltr(cur.r)} עותקים, ולכן ${ltr(`${cur.r} = ${b} − ${b - cur.r}`)}${NB}: הספרה ${ltr(num(cur.d))}, ${cnt}${w} ליד המשא, ו-1 עובר הלאה. ${ltr(`(${cur.before} + ${-cur.d}) / ${b} = ${cur.after}`)}.`;
          else if (cur.d > 0) note = head + `הספרה ${ltr(cur.d)}${NB}: ${cnt}${w} בכף השנייה. ${ltr(`(${cur.before} − ${cur.d}) / ${b} = ${cur.after}`)}.`;
          else note = head + `הספרה 0${NB}: ${w} נשארת בחוץ. ${ltr(`${cur.before} / ${b} = ${cur.after}`)}.`;
          if (done) note += ` המספר הגיע ל-0${NB}: כל הספרות ידועות, והמאזניים מאוזנים.`;
          else if (cur.after === 0) note += ` המספר כבר 0${NB}: שאר המשקולות יישארו בחוץ.`;
        }
        $(".wt-note").innerHTML = note;
        // the explanation panel
        const L = LINES[st.mode], copies = m.copies;
        let lit, lines;
        if (!cur) { lit = copies ? [1] : []; lines = L.init; }
        else {
          const neg = cur.d < 0, mark = st.mode === "one" ? (cur.d ? [2] : []) : neg ? [copies ? 3 : 2] : [];
          lit = copies ? [2, ...mark, 4, ...(done ? [5] : [])] : [1, ...mark, 3, ...(done ? [4] : [])];
          const step = L.step(neg);
          lines = done ? { py: [...step.py, ...L.end.py], sv: [...step.sv, ...L.end.sv] } : step;
        }
        const ds = `[${placed.map((r) => num(r.d)).join(", ")}]`;
        const vars = cur ? [ltr(`n = ${cur.before}`), ltr(`r = ${cur.r}${cur.d !== cur.r ? ` → ${num(cur.d)}` : ""}`), ltr(`digits = ${ds}`), ltr(`n → ${cur.after}`)] : [ltr(`n = ${st.n}`), ltr(`base = ${b}`), ltr("digits = []")];
        if (copies) vars.splice(1, 0, ltr(`c = ${c}`));
        show({ code: m.code, steps: STEPS[st.mode], lit, lines, vars: vars.join(" · ") });
        if (done) {
          const parts = rows.filter((r) => r.d).reverse().map((r) => `${r.d > 0 ? "+" : MINUS} ${Math.abs(r.d) > 1 ? `${Math.abs(r.d)}·` : ""}${r.w}`).join(" ").replace(/^\+ /, "");
          answer(box, `${ltr(`${st.n} = ${parts}`)}${NB}: ${oth.length ? `${ltr(oth.join(", "))} בכף השנייה` : ""}${bes.length ? `, ${ltr(bes.join(", "))} ליד המשא` : ""}.`, ".wt-live .wt-w.is-other, .wt-live .wt-w.is-beside");
        } else answer(box, null);
      };

      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= st.k, restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; draw(); };
      $(".wt-mode").addEventListener("change", () => {
        st.mode = $(".wt-mode").value;
        st.k = MODES[st.mode].k0;
        restart();
      });
      $(".wt-k").addEventListener("input", () => { st.k = Number($(".wt-k").value); restart(); });
      $(".wt-c").addEventListener("input", () => { st.c = Number($(".wt-c").value); restart(); });
      $(".wt-n").addEventListener("input", () => { st.n = Number($(".wt-n").value); restart(); });
      $(".wt-rand").addEventListener("click", () => { st.n = 1 + Math.floor(Math.random() * reachOf()); restart(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = st.k; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, d0); restart(); });
      draw();
      if ("ResizeObserver" in window) {
        let wasNarrow = geom().W < 640;
        new ResizeObserver(() => { const now = geom().W < 640; if (now !== wasNarrow) { wasNarrow = now; draw(); } }).observe(box);
      }
    },
  });

  dvqExplorers.register({
    views: { weights: weightsView },
    help: {
      weights: "בוחרים סעיף (כף אחת, שתי כפות, או c עותקים מכל משקולת), מספר משקלים k ומשא n. כל צעד הוא ספרה אחת של n, מהנמוכה : השארית, הספרה (בשתי כפות שארית גדולה מ-c הופכת לספרה שלילית עם העברה), והמשקולת עוברת מהשורה שמתחת למאזניים לכף שלה. הטבלה מתחת למאזניים היא הספרות, הספרה השלילית מסומנת, ולמעלה החסם של k משקלים מול מה שהמשקולות שוקלות בפועל.",
    },
    models: { wtBase, wtBound, wtSteps, wtDigits, wtReach },
  });
})();
