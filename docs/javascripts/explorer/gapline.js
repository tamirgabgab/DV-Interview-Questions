// kinds: gapline
//   gapline                0029        part b's proof: the angle difference of two hands in turns against time, the integers as lines and each crossing a meeting; the interval [0, L] closed, open or half-open with the page's three counts
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { f, ltr } = dvqExplorers.lib;
  const NB = "\u00a0";

  const gcd = (a, b) => (b ? gcd(b, a % b) : Math.abs(a));
  // Two hands with periods ti < tj (whole seconds) and an interval of length L = Ln / Ld
  // that starts at a meeting: the gap between meetings T = ti tj / (tj − ti) and the ratio
  // r = L / T as reduced fractions, and the page's three counts (formula 3).
  const gapLine = (ti, tj, Ln, Ld = 1) => {
    const g = gcd(ti * tj, tj - ti), Tn = (ti * tj) / g, Td = (tj - ti) / g;
    let rn = Ln * Td, rd = Ld * Tn;
    const h = gcd(rn, rd);
    rn /= h; rd /= h;
    const floor = (rn - (rn % rd)) / rd, ceil = rn % rd ? floor + 1 : floor;
    return { Tn, Td, rn, rd, whole: rd === 1, closed: floor + 1, open: ceil - 1, half: ceil };
  };
  // Is meeting k (at k T) inside the interval, for r = L / T = rn / rd?
  const GAP_MODES = ["closed", "open", "half"];
  const gapIn = (k, rn, rd, mode) => {
    const atEnd = k * rd === rn, before = k * rd < rn;
    if (mode === "closed") return before || atEnd;
    if (mode === "open") return k > 0 && before;
    return before;
  };

  // The gap line box (0029 part b): a pair of the clock's hands (or two periods typed in),
  // the length L in quarters of T, and the kind of interval; the line θi − θj = t / T, the
  // integers as dashed lines, a dot at every crossing (filled when it is counted), the
  // ends of the interval as filled or hollow brackets, and the three counts of formula 3.
  const PAIRS = { sm: [60, 3600, "השניות והדקות"], sh: [60, 43200, "השניות והשעות"], mh: [3600, 43200, "הדקות והשעות"] };
  const MODE_NAME = { closed: "סגור", open: "פתוח", half: "חצי פתוח" };
  const MODE_SET = { closed: "[0, L]", open: "(0, L)", half: "[0, L)" };
  const MODE_FORMULA = { closed: "⌊L / T⌋ + 1", open: "⌈L / T⌉ − 1", half: "⌈L / T⌉" };
  const gaplineView = () => ({
    mount(box) {
      const D = { pair: box.dataset.pair || "mh", q: Math.round(4 * Number(box.dataset.r || 3)), mode: box.dataset.mode || "closed" };
      const st = { ...D, ti: 2, tj: 3 };
      box.innerHTML =
        `<div class="ex-controls"><label>הזוג <select class="gl-pair">${Object.entries(PAIRS).map(([k, v]) => `<option value="${k}">${v[2]}</option>`).join("")}<option value="any">שני מחוגים אחרים</option></select></label>` +
        `<label class="gl-own" hidden><span>‏t<sub>i</sub></span><input type="number" class="gl-ti" min="1" max="999" step="1" value="2" dir="ltr" aria-label="זמן הסיבוב של המחוג המהיר"></label>` +
        `<label class="gl-own" hidden><span>‏t<sub>j</sub></span><input type="number" class="gl-tj" min="2" max="1000" step="1" value="3" dir="ltr" aria-label="זמן הסיבוב של המחוג האיטי"></label>` +
        `<label><span>אורך הקטע L</span><input type="range" class="gl-q" min="1" max="24" step="1" value="${D.q}" dir="ltr" aria-label="אורך הקטע, ברבעים של T"><output class="gl-qout"></output></label>` +
        `<label>הקטע <select class="gl-mode">${GAP_MODES.map((m) => `<option value="${m}">${MODE_NAME[m]} \u2066${MODE_SET[m]}\u2069</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button><span class="fl-err gl-err" aria-live="polite"></span></div>` +
        `<p class="wv-step gl-T"></p><div class="gl-chart"></div>` +
        `<span class="viz-legend"><span><i class="gl-key-line"></i>ההפרש בסיבובים</span><span><i class="gl-key-in"></i>פגישה שנספרת</span><span><i class="gl-key-out"></i>פגישה מחוץ לקטע</span></span>` +
        `<div class="gl-table"></div><p class="ex-summary gl-sum" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const periods = () => (st.pair === "any" ? [st.ti, st.tj] : PAIRS[st.pair].slice(0, 2));
      const chart = (r) => {
        const W = 640, H = 270, X0 = 46, X1 = 620, Y0 = 14, Y1 = 226;
        const R = r.rn / r.rd, top = Math.max(1, Math.ceil(R + 0.35)), right = R * 1.1 + 0.15;
        const X = (u) => X0 + (u / right) * (X1 - X0), Y = (v) => Y1 - (v / top) * (Y1 - Y0);
        let s = `<svg class="perf-chart gl-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="ההפרש בין המחוגים בסיבובים מול הזמן, ${r.count} פגישות בקטע">`;
        for (let k = 0; k <= top; k++) s += `<line class="gl-int" x1="${X0}" x2="${X1}" y1="${f(Y(k))}" y2="${f(Y(k))}"/><text class="tick" x="${X0 - 6}" y="${f(Y(k) + 4)}" text-anchor="end">${k}</text>`;
        s += `<rect class="gl-span" x="${f(X(0))}" y="${Y0}" width="${f(X(R) - X(0))}" height="${Y1 - Y0}"/>`;
        s += `<line class="axis" x1="${X0}" x2="${X1}" y1="${Y1}" y2="${Y1}"/>`;
        for (let k = 0; k <= Math.floor(R * 1.1 + 0.15); k++) s += `<line class="gl-tickline" x1="${f(X(k))}" x2="${f(X(k))}" y1="${Y1}" y2="${Y1 + 5}"/><text class="tick" x="${f(X(k))}" y="${Y1 + 18}" text-anchor="middle">${k === 0 ? "0" : k === 1 ? "T" : `${k}T`}</text>`;
        s += `<line class="gl-line" x1="${f(X(0))}" y1="${f(Y(0))}" x2="${f(X(Math.min(right, top)))}" y2="${f(Y(Math.min(right, top)))}"/>`;
        // the ends of the interval on the time axis: a filled dot when the end is included
        const inc0 = st.mode !== "open", incL = st.mode === "closed";
        s += `<line class="gl-ends" x1="${f(X(0))}" x2="${f(X(R))}" y1="${Y1 + 30}" y2="${Y1 + 30}"/>` +
             `<circle class="${inc0 ? "gl-end-in" : "gl-end-out"}" cx="${f(X(0))}" cy="${Y1 + 30}" r="5.5"/>` +
             `<circle class="${incL ? "gl-end-in" : "gl-end-out"}" cx="${f(X(R))}" cy="${Y1 + 30}" r="5.5"/>` +
             `<text class="tick" x="${f(X(R) + 10)}" y="${Y1 + 34}">L</text>`;
        for (let k = 0; k <= Math.floor(right); k++) {
          const counted = gapIn(k, r.rn, r.rd, st.mode);
          s += `<circle class="${counted ? "gl-in" : "gl-out"}" cx="${f(X(k))}" cy="${f(Y(k))}" r="6"><title>פגישה ${k}, בזמן ${k === 0 ? "0" : k === 1 ? "T" : `${k}T`}${counted ? ", נספרת" : ", לא בקטע"}</title></circle>`;
        }
        return s + `<text class="tick" x="${X1}" y="${Y1 - 6}" text-anchor="end">t</text></svg>`;
      };
      const draw = () => {
        const [ti, tj] = periods();
        $(".gl-pair").value = st.pair; $(".gl-mode").value = st.mode; $(".gl-q").value = st.q;
        box.querySelectorAll(".gl-own").forEach((l) => { l.hidden = st.pair !== "any"; });
        // L = (q / 4) T, so L / T = q / 4 exactly
        const base = gapLine(ti, tj, 1), r = gapLine(ti, tj, st.q * base.Tn, 4 * base.Td);
        r.count = r[st.mode];
        const ratio = String(st.q / 4);
        $(".gl-qout").textContent = `${st.q === 4 ? "" : ratio}T`;
        const Tv = r.Tn / r.Td, Ts = r.Td === 1 ? r.Tn.toLocaleString("en-US") : `${r.Tn.toLocaleString("en-US")}/${r.Td} ≈ ${Tv.toLocaleString("en-US", { maximumFractionDigits: Tv < 100 ? 2 : 1 })}`;
        const n = (v) => v.toLocaleString("en-US");
        $(".gl-T").innerHTML = `המחוג המהיר מסיים סיבוב ב-${ltr(n(ti))} שניות והאיטי ב-${ltr(n(tj))}, ולכן הפער ביניהם גדל ב-${ltr(`1/${n(ti)} − 1/${n(tj)}`)} סיבוב לשנייה, ` +
          `ונפגשים כל ${ltr(`T = ${n(ti)}·${n(tj)} / (${n(tj)} − ${n(ti)}) = ${Ts}`)} שניות.`;
        $(".gl-chart").innerHTML = chart(r);
        $(".gl-table").innerHTML = `<table class="bridge-table gl-counts"><thead><tr><th>הקטע</th><th>הנוסחה</th><th>הפגישות</th></tr></thead><tbody>` +
          GAP_MODES.map((m) => `<tr${m === st.mode ? ' class="is-now"' : ""}><td>${MODE_NAME[m]} ${ltr(MODE_SET[m])}</td><td>${ltr(MODE_FORMULA[m])}</td><td>${ltr(r[m])}</td></tr>`).join("") + `</tbody></table>`;
        $(".gl-sum").innerHTML = `‏${ltr(`L / T = ${ratio}`)}${NB}: הקו עובר ${r.whole ? `בדיוק ב-${ltr(r.rn)} בקצה L` : `בין ${ltr(r.closed - 1)} ל-${ltr(r.closed)} בקצה L`}, וכל שלם שהוא חוצה הוא פגישה. ` +
          (r.whole ? `כאן הקצה L הוא בעצמו פגישה, ולכן שלוש הספירות שונות : ${ltr(r.closed)}, ${ltr(r.open)} ו-${ltr(r.half)}. הן נבדלות רק בשני הקצוות, 0 ו-L.`
            : `הקצה L אינו פגישה, ולכן רק הקצה 0 משנה : ${ltr(r.closed)} בקטע סגור או חצי פתוח, ${ltr(r.open)} בקטע פתוח.`);
      };
      const setOwn = () => {
        const ti = Number($(".gl-ti").value), tj = Number($(".gl-tj").value);
        if (!Number.isInteger(ti) || !Number.isInteger(tj) || ti < 1 || tj > 1000 || ti >= tj) { $(".gl-err").textContent = "שני שלמים עד 1000, הראשון קטן מהשני"; return; }
        $(".gl-err").textContent = ""; st.ti = ti; st.tj = tj; draw();
      };
      $(".gl-pair").addEventListener("change", () => { st.pair = $(".gl-pair").value; $(".gl-err").textContent = ""; draw(); });
      $(".gl-ti").addEventListener("change", setOwn);
      $(".gl-tj").addEventListener("change", setOwn);
      $(".gl-q").addEventListener("input", () => { st.q = Number($(".gl-q").value); draw(); });
      $(".gl-mode").addEventListener("change", () => { st.mode = $(".gl-mode").value; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, D); $(".gl-err").textContent = ""; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { gapline: gaplineView },
    help: {
      gapline: "בוחרים זוג מחוגים, אורך קטע L ברבעים של T וסוג קטע : הקו הוא ההפרש בין המחוגים בסיבובים, וכל חיתוך עם קו של מספר שלם הוא פגישה. נקודה מלאה נספרת, נקודה ריקה לא, והטבלה מראה את שלוש הספירות של נוסחה 3. כש-L הוא כפולה שלמה של T, הקצה L הוא פגישה, ושלוש הספירות שונות.",
    },
    models: { gapLine, gapIn, GAP_MODES },
  });
})();
