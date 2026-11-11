// kinds: sicherman
//   sicherman              0101        two n-sided dice with any faces (data-n 4, 6 or 8, data-a / data-b "1.2.2.3.3.4"): the faces of both dice in number fields (0 to 20), the n x n table of the sums tinted by the sum (a cell whose sum comes a different number of times than with standard dice framed), the histogram of the sum against the triangle of two standard dice (a bar that differs orange), whether each die alone is a standard die, a select of n and buttons for the known pairs of that n (scPairs: the standard pair and the other pairs of q0101.factor_pairs, for n = 6 also part b's shifts with a face 0 and a failed try with face 1 twice)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, ltr } = dvqExplorers.lib;
  const NB = " ";
  const NS = [4, 6, 8], NMAX = 8, FMAX = 20;

  // --- the models, as tools/figures/q0101.py --------------------------------------------------

  const scStd = (n) => Array.from({ length: n }, (_, i) => i + 1);
  // counts[s]: how many of the n * n rolls of the dice a and b give the sum s
  const scSums = (a, b) => {
    const c = Array(Math.max(...a) + Math.max(...b) + 1).fill(0);
    a.forEach((x) => b.forEach((y) => { c[x + y] += 1; }));
    return c;
  };
  // the sums whose count differs from that of two standard dice of as many faces
  const scDiff = (a, b) => {
    const n = a.length, want = scSums(scStd(n), scStd(n)), got = scSums(a, b), out = [];
    for (let s = 0; s < Math.max(want.length, got.length); s++) if ((want[s] || 0) !== (got[s] || 0)) out.push(s);
    return out;
  };
  // the tint of a sum: how often two standard dice give it, from 1 to 6 (0: never), and its hue
  // (below the middle sum, the middle, above it), as level() and hue() of q0101.py
  const scLevel = (s, n) => { const f = n - Math.abs(s - (n + 1)); return f <= 0 ? 0 : Math.ceil((6 * f) / n); };
  const scHue = (s, n) => (s < n + 1 ? "sc-lo" : s === n + 1 ? "sc-mid" : "sc-hi");
  const sameDie = (a) => [...a].sort((x, y) => x - y).every((f, i) => f === i + 1);
  // the known pairs of each n: [name, die A, die B]; for 6 also the shifts of part b and a try
  // that fails (face 1 twice)
  const scPairs = {
    4: [["רגילות", [1, 2, 3, 4], [1, 2, 3, 4]], ["הזוג האחר", [1, 2, 2, 3], [1, 3, 3, 5]]],
    6: [
      ["רגילות", [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]],
      ["‏Sicherman", [1, 2, 2, 3, 3, 4], [1, 3, 4, 5, 6, 8]],
      ["הזזה של הרגילות", [0, 1, 2, 3, 4, 5], [2, 3, 4, 5, 6, 7]],
      ["הזזה 1 של Sicherman", [0, 1, 1, 2, 2, 3], [2, 4, 5, 6, 7, 9]],
      ["הזזה 2 של Sicherman", [2, 3, 3, 4, 4, 5], [0, 2, 3, 4, 5, 7]],
    ],
    8: [
      ["רגילות", [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8]],
      ["זוג 1", [1, 2, 2, 3, 3, 4, 4, 5], [1, 3, 5, 5, 7, 7, 9, 11]],
      ["זוג 2", [1, 2, 2, 3, 5, 6, 6, 7], [1, 3, 3, 5, 5, 7, 7, 9]],
      ["זוג 3", [1, 2, 3, 3, 4, 4, 5, 6], [1, 2, 5, 5, 6, 6, 9, 10]],
    ],
  };
  const scTries = { 6: [[`ניסיון${NB}: 1 פעמיים`, [1, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]]] };
  // "1.2.2.3.3.4" -> the n faces, each a whole number from 0 to FMAX; null otherwise
  const scParse = (text, n) => {
    const v = String(text || "").split(".").filter((x) => x !== "");
    if (v.length !== n || v.some((x) => !/^\d{1,2}$/.test(x) || Number(x) > FMAX)) return null;
    return v.map(Number);
  };

  // --- the box ---------------------------------------------------------------------------------

  const hist = (a, b, n, bad) => {
    const got = scSums(a, b), want = scSums(scStd(n), scStd(n));
    const lo = Math.min(2, Math.min(...a) + Math.min(...b)), hi = Math.max(2 * n, got.length - 1);
    const slots = hi - lo + 1, ymax = Math.max(n, ...got);
    const W = 400, H = 190, X0 = 30, R = 6, TOP = 16, BASE = 160;
    const slot = (W - X0 - R) / slots, bw = slot * 0.7;
    const X = (s) => X0 + (s - lo + 0.5) * slot, Y = (v) => BASE - (v / ymax) * (BASE - TOP);
    const every = slots > 24 ? 4 : slots > 14 ? 2 : 1;
    let s = `<svg class="perf-chart sc-hist" viewBox="0 0 ${W} ${H}" role="img" aria-label="התפלגות הסכום מול המשולש של שתי קוביות רגילות${bad.length ? `${NB}: ${bad.length} סכומים שונים` : `${NB}: זהה`}">`;
    [0, Math.round(ymax / 2), ymax].forEach((v) => {
      s += `<line class="grid" x1="${X0}" x2="${W - R}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}"/>` +
        `<text class="tick" x="${X0 - 6}" y="${(Y(v) + 4).toFixed(1)}" text-anchor="end">${v}</text>`;
    });
    for (let k = lo; k <= hi; k++) {
      const g = got[k] || 0, w = want[k] || 0, off = bad.includes(k);
      const tip = `סכום ${k}${NB}: ${g} הטלות, ברגילות ${w}`;
      if (g) s += `<rect class="sc-bar${off ? " is-bad" : ""}" x="${(X(k) - bw / 2).toFixed(1)}" y="${Y(g).toFixed(1)}" width="${bw.toFixed(1)}" height="${(BASE - Y(g)).toFixed(1)}" rx="1.5"><title>${tip}</title></rect>`;
      if (w) s += `<line class="sc-want" x1="${(X(k) - slot / 2 + 1).toFixed(1)}" x2="${(X(k) + slot / 2 - 1).toFixed(1)}" y1="${Y(w).toFixed(1)}" y2="${Y(w).toFixed(1)}"><title>${tip}</title></line>`;
      if ((k - lo) % every === 0) s += `<text class="tick" x="${X(k).toFixed(1)}" y="${BASE + 17}" text-anchor="middle">${k}</text>`;
    }
    return `${s}<line class="axis" x1="${X0}" x2="${W - R}" y1="${BASE}" y2="${BASE}"/></svg>`;
  };
  const table = (a, b, n, bad) => {
    let h = `<table class="sc-tab" dir="ltr" aria-label="טבלת הסכומים${NB}: שורה לכל פאה של A, עמודה לכל פאה של B"><thead><tr><th scope="col" class="sc-corner">+</th>`;
    b.forEach((f) => { h += `<th scope="col">${f}</th>`; });
    h += "</tr></thead><tbody>";
    a.forEach((e) => {
      h += `<tr><th scope="row">${e}</th>`;
      b.forEach((f) => {
        const s = e + f, lv = scLevel(s, n);
        h += `<td class="sc-c ${lv ? `${scHue(s, n)} sc-f${lv}` : "sc-out"}${bad.includes(s) ? " is-off" : ""}" title="${e} + ${f} = ${s}">${s}</td>`;
      });
      h += "</tr>";
    });
    return `${h}</tbody></table>`;
  };

  const sichermanView = () => ({
    mount(box) {
      const n0 = NS.includes(Number(box.dataset.n)) ? Number(box.dataset.n) : 6;
      const a0 = scParse(box.dataset.a, n0) || scStd(n0), b0 = scParse(box.dataset.b, n0) || scStd(n0);
      const st = { n: n0, a: a0.slice(), b: b0.slice() };
      const fields = (name) => `<div class="sc-die" role="group" aria-label="הפאות של קובייה ${name}"><span class="sc-lab" aria-hidden="true">${name}</span>` +
        Array.from({ length: NMAX }, (_, i) => `<input type="number" class="ex-num sc-face" data-die="${name}" data-i="${i}" min="0" max="${FMAX}" step="1" dir="ltr" inputmode="numeric" aria-label="קובייה ${name}, פאה ${i + 1}">`).join("") + `</div>`;
      const presets = NS.map((n) => [...scPairs[n], ...(scTries[n] || [])].map(([name, a, b], k) =>
        `<button type="button" class="md-button ex-preset sc-pick" data-n="${n}" data-k="${k}" title="A = ${a.join(", ")}${NB}; B = ${b.join(", ")}">${name}</button>`).join("")).join("");
      box.innerHTML =
        `<div class="ex-controls"><label>פאות לכל קובייה <select class="sc-n" aria-label="מספר הפאות של כל קובייה">${NS.map((n) => `<option value="${n}">${n}</option>`).join("")}</select></label></div>` +
        `<div class="ex-controls sc-dice" dir="ltr">${fields("A")}${fields("B")}</div>` +
        `<div class="ex-controls sc-presets">${presets}</div>` +
        `<p class="ex-summary sc-sum" aria-live="polite"></p>` +
        `<div class="sc-tablewrap" tabindex="0" role="region" aria-label="טבלת הסכומים"></div>` +
        `<div class="sc-histwrap"></div>` +
        `<span class="viz-legend sc-legend"><span><i class="sc-key-ok"></i>סכום שמתקבל כמו ברגילות</span><span><i class="sc-key-bad"></i>סכום שמתקבל מספר אחר של פעמים</span>` +
        `<span><i class="sc-key-want"></i>המשולש של שתי קוביות רגילות</span></span>` +
        `<p class="sc-alone" aria-live="polite"></p>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const inputs = (die) => [...box.querySelectorAll(`.sc-face[data-die="${die}"]`)];

      const draw = () => {
        const { n, a, b } = st;
        $(".sc-n").value = String(n);
        ["A", "B"].forEach((die) => inputs(die).forEach((el, i) => {
          el.hidden = i >= n;
          el.value = i < n ? String((die === "A" ? a : b)[i]) : String(i + 1);
        }));
        box.querySelectorAll(".sc-pick").forEach((btn) => { btn.hidden = Number(btn.dataset.n) !== n; });
        const bad = scDiff(a, b);
        $(".sc-tablewrap").innerHTML = table(a, b, n, bad);
        $(".sc-histwrap").innerHTML = hist(a, b, n, bad);
        const sa = sameDie(a), sb = sameDie(b);
        let sum = `קוביות של ${n} פאות${NB}: `;
        if (!bad.length) sum += "כל סכום מתקבל באותו מספר הטלות כמו בשתי קוביות רגילות.";
        else {
          const shown = bad.slice(0, 6).join(", ") + (bad.length > 6 ? ", ..." : "");
          sum += `${bad.length === 1 ? "סכום אחד מתקבל" : `${bad.length} סכומים מתקבלים`} מספר אחר של פעמים מאשר בקוביות רגילות${NB}: ${ltr(shown)}.`;
        }
        $(".sc-sum").innerHTML = sum;
        const word = (ok, name) => `${name} ${ok ? "רגילה" : "לא רגילה"}`;
        $(".sc-alone").innerHTML = !bad.length && !(sa && sb)
          ? `בדיקה של הסכום לא מבדילה בין הזוג הזה לרגילות. בדיקה של כל קובייה לבד כן${NB}: ${word(sa, "A")}, ${word(sb, "B")}.`
          : `כל קובייה לבד${NB}: ${word(sa, "A")}, ${word(sb, "B")}.`;
        answer(box, bad.length ? null : sa && sb ? "אותה התפלגות של הסכום. אלה הקוביות הרגילות." : "אותה התפלגות של הסכום, עם קוביות אחרות.", ".sc-hist");
      };

      $(".sc-n").addEventListener("change", () => {
        const n = Number($(".sc-n").value);
        if (!NS.includes(n) || n === st.n) return;
        Object.assign(st, { n, a: scStd(n), b: scStd(n) });
        draw();
      });
      box.querySelectorAll(".sc-face").forEach((el) => el.addEventListener("change", () => {
        const i = Number(el.dataset.i), faces = el.dataset.die === "A" ? st.a : st.b;
        if (i >= st.n) return;
        const v = Math.round(Number(el.value));
        if (el.value.trim() !== "" && Number.isFinite(v)) faces[i] = Math.min(FMAX, Math.max(0, v));
        draw();
      }));
      box.querySelectorAll(".sc-pick").forEach((btn) => btn.addEventListener("click", () => {
        const n = Number(btn.dataset.n), [, a, b] = [...scPairs[n], ...(scTries[n] || [])][Number(btn.dataset.k)];
        Object.assign(st, { n, a: a.slice(), b: b.slice() });
        draw();
      }));
      draw();
    },
  });

  dvqExplorers.register({
    views: { sicherman: sichermanView },
    help: {
      sicherman: "כותבים מספר על כל פאה של שתי הקוביות, 0 עד 20. הטבלה מראה את כל ההטלות, שורה לכל פאה של A ועמודה לכל פאה של B, ובכל תא את הסכום. הצבע הוא של הסכום : כחול מתחת לסכום האמצעי, ירוק לאמצעי וסגול מעליו, עמוק יותר ככל שבקוביות רגילות הוא נפוץ יותר. ההיסטוגרמה סופרת כל סכום, והקווים הם המשולש של שתי קוביות רגילות. סכום שמתקבל מספר אחר של פעמים כתום בהיסטוגרמה וממוסגר בטבלה. הבחירה של מספר הפאות והכפתורים טוענים את הזוגות שבעמוד.",
    },
    cols: { sicherman: { main: ".sc-tablewrap", side: ".sc-histwrap, .sc-legend, .sc-alone", w: "minmax(0, 1fr)" } },   // the table of the sums beside the histogram
    models: { scStd, scSums, scDiff, scLevel, scHue, scPairs, scTries, scParse },
  });
})();
