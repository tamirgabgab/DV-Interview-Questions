// kinds: popnext
//   popnext                0059        the next number with as many ones: a width and a number, the rows of Gosper's formula (or of the previous one through the complement) step by step, and the next / previous / first / last buttons that walk the sorted list with the place in it
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, code, ltr, speedSel } = dvqExplorers.lib;

  // The next number with as many ones (0059), for widths up to 16 bits (plain JS numbers).
  // gsNext / gsPrev return 0 when there is none; gsRank counts the smaller numbers with as
  // many ones (the sum of C(p_i, i)); gsSteps gives the rows of Gosper's formula, each with
  // the bits the step is about (as in tools/figures/q0059.py).
  const ones = (v) => { let n = 0; for (; v; v >>>= 1) n += v & 1; return n; };
  const bitsOf = (v) => { const out = []; for (let p = 0; v; p++, v >>>= 1) if (v & 1) out.push(p); return out; };
  const range = (a, b) => Array.from({ length: Math.max(0, b - a) }, (_, i) => a + i);
  const binom = (n, k) => { if (k < 0 || k > n) return 0; let b = 1; for (let t = 1; t <= k; t++) b = (b * (n - k + t)) / t; return b; };
  const gsSteps = (x, w) => {
    if (!x) return { rows: [{ label: "x", v: 0, marks: [] }], next: 0, t: 0, m: 0 };
    const c = x & -x, r = x + c, t = Math.log2(c);
    let m = 0;
    while ((x >>> (t + m)) & 1) m++;
    const rows = [{ label: "x", v: x, marks: range(t, t + m) }, { label: "c = x & −x", v: c, marks: [t] }, { label: "r = x + c", v: r, marks: [t + m] }];
    if (r >= 2 ** w) return { rows, next: 0, t, m };
    const xr = x ^ r, s = (xr >>> 2) >>> t;      // the division by c = 2^t, floored as in Python
    rows.push({ label: "x ^ r", v: xr, marks: range(t, t + m + 1) }, { label: "(x ^ r) >> 2", v: xr >>> 2, marks: bitsOf(xr >>> 2) },
      { label: "s = … / c", v: s, marks: range(0, m - 1) }, { label: "r | s", v: r | s, marks: range(0, m - 1).concat([t + m]) });
    return { rows, next: r | s, t, m };
  };
  const gsNext = (x, w) => gsSteps(x, w).next;
  const gsPrev = (x, w) => { const mask = 2 ** w - 1, y = gsNext(~x & mask, w); return y ? ~y & mask : 0; };
  const gsRank = (x) => bitsOf(x).reduce((acc, p, i) => acc + binom(p, i + 1), 0);

  const WIDTHS = [4, 5, 6, 8, 10, 12, 16];
  const ROWS = 9;                      // the most rows (the previous one), so the table keeps its size
  const bin = (v, w) => v.toString(2).padStart(w, "0");

  // the rows the box shows: the next one, or the previous one as ~next(~x)
  const stepsOf = (x, w, dir) => {
    const mask = 2 ** w - 1;
    if (dir === "next") {
      const g = gsSteps(x, w);
      return { rows: g.rows, result: g.next, g };
    }
    const y = ~x & mask, g = gsSteps(y, w);
    const rows = [{ label: "x", v: x, marks: [] }, { label: "y = ~x", v: y, marks: [] }]
      .concat(g.rows.slice(1).map((r) => ({ ...r, label: r.label.replace(/x/g, "y") })));
    if (g.next) rows.push({ label: "~(r | s)", v: ~g.next & mask, marks: [] });
    return { rows, result: g.next ? ~g.next & mask : 0, g };
  };
  const NOTES = {
    next: (k, g, w, res) => [
      `בלוק האחדות הנמוך מסומן : ${ltr(g.m)} אחדות מהמקום ${ltr(g.t)}.`,
      `האחד הנמוך ביותר : ${ltr(`c = 2^${g.t} = ${2 ** g.t}`)}.`,
      res ? `ה-carry מכבה את הבלוק ומדליק את הביט ${ltr(g.t + g.m)} שמעליו.` : `החיבור גולש מעבר ל-${ltr(w)} ביטים : הבלוק היה בראש המילה, ואין מספר הבא.`,
      `הביטים שהשתנו : הבלוק והביט החדש, ${ltr(g.m + 1)} אחדות.`,
      `שתיים פחות : נשארות ${ltr(Math.max(0, g.m - 1))} אחדות, כמה שחסר.`,
      `החילוק ב-${ltr(2 ** g.t)} מזיז עוד ${ltr(g.t)} מקומות ימינה, לתחתית.`,
      `התשובה : החלק העליון מ-${code("r")} והאחדות שירדו מ-${code("s")}.`,
    ][k],
    prev: (k, g, w, res) => [
      `המספר. הקודם שלו הוא ההיפוך של המספר הבא אחרי ${code("~x")}.`,
      `ההיפוך ברוחב ${ltr(w)}. הסדר מתהפך, ועכשיו מחפשים את הבא.`,
      `האחד הנמוך ביותר של ${code("y")}.`,
      res ? `ה-carry מכבה את הבלוק הנמוך של ${code("y")} ומדליק את הביט שמעליו.` : `החיבור גולש : אין מספר אחרי ${code("y")}, ולכן אין קודם ל-${code("x")}.`,
      `הביטים שהשתנו.`,
      `שתיים פחות.`,
      `לתחתית.`,
      `המספר הבא אחרי ${code("y")}.`,
      `היפוך בחזרה : זה המספר הקודם ל-${code("x")}.`,
    ][k],
  };

  const popnextView = () => ({
    mount(box) {
      const d0 = { x: Number(box.dataset.x) || 92, w: Number(box.dataset.w) || 8 };
      const st = { x: d0.x, w: d0.w, dir: "next", k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הרוחב <select class="gs-w" aria-label="רוחב המילה בביטים">${WIDTHS.map((v) => `<option value="${v}"${v === d0.w ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<label><span>המספר</span><input type="number" class="ex-num gs-x" min="1" dir="ltr" aria-label="המספר x, בעשרוני"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err gs-err"></span></div>` +
        `<div class="ex-controls">` +
        `<span>ברשימה :</span>` +
        `<button type="button" class="md-button gs-first">הראשון</button>` +
        `<button type="button" class="md-button gs-prev">הקודם</button>` +
        `<button type="button" class="md-button md-button--primary gs-next">הבא</button>` +
        `<button type="button" class="md-button gs-last">האחרון</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<label>השלבים של <select class="gs-dir" aria-label="איזו נוסחה לפרק לשלבים"><option value="next" selected>הבא</option><option value="prev">הקודם</option></select></label>` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">השלב הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">השלב הבא</button>` +
        `<button type="button" class="md-button ex-end">כל השלבים</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 900, 450) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary gs-sum" aria-live="polite"></p>` +
        `<div class="gs-scroll"><table class="gs-bits" dir="ltr" aria-label="שלבי הנוסחה, ביט אחרי ביט"><tbody></tbody></table></div>` +
        `<span class="viz-legend"><span><i class="gs-key-one"></i>ביט דולק</span><span><i class="gs-key-mark"></i>הביטים שהשלב עוסק בהם</span></span>` +
        `<p class="gs-note"></p>` +
        `<p class="gs-note gs-rank"></p>`;
      const $ = (s) => box.querySelector(s);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const steps = () => stepsOf(st.x, st.w, st.dir);
      const draw = () => {
        const { x, w } = st, k = ones(x), mask = 2 ** w - 1;
        const S = steps(), N = S.rows.length - 1;
        st.k = Math.min(st.k, N);
        $(".gs-w").value = String(w); $(".gs-x").value = String(x); $(".gs-dir").value = st.dir;
        $(".gs-x").max = String(mask);
        const nx = gsNext(x, w), pv = gsPrev(x, w), first = 2 ** k - 1, last = first * 2 ** (w - k);
        $(".gs-next").disabled = $(".gs-last").disabled = !nx;
        $(".gs-prev").disabled = $(".gs-first").disabled = !pv;
        $(".ex-pos").textContent = `שלב ${st.k} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === N;
        const rank = gsRank(x), total = binom(w, k);
        $(".gs-sum").innerHTML = `${ltr(`x = ${x} = ${bin(x, w)}`)}, ${ltr(k)} אחדות ב-${ltr(w)} ביטים. ` +
          `במקום ${ltr(rank + 1)} מתוך ${ltr(total)} ברשימה של המספרים עם ${ltr(k)} אחדות` +
          `${first === x ? " (הראשון)" : ""}${last === x ? " (האחרון)" : ""}.`;
        let rows = "";
        for (let r = 0; r < ROWS; r++) {
          const row = S.rows[r] || { label: "·", v: 0, marks: [] }, off = r > st.k || !S.rows[r];
          let cells = "";
          for (let p = w - 1; p >= 0; p--) {
            const one = Math.floor(row.v / 2 ** p) % 2 === 1, mark = !off && row.marks.includes(p);
            cells += `<td class="gs-b${one ? " is-one" : ""}${mark ? " is-mark" : ""}">${one ? 1 : 0}</td>`;
          }
          rows += `<tr${off ? ` class="is-off" aria-hidden="true"` : ""}><th>${row.label.replace(/&/g, "&amp;").replace(/>/g, "&gt;")}</th>${cells}<td class="gs-val">${row.v}</td></tr>`;
        }
        $(".gs-bits tbody").innerHTML = rows;
        $(".gs-note").innerHTML = NOTES[st.dir](st.k, S.g, w, S.result);
        const terms = bitsOf(x).map((p, i) => [p, i + 1]);
        $(".gs-rank").innerHTML = `המקום : ${ltr(terms.map(([p, i]) => `C(${p},${i})`).join(" + "))} = ${ltr(terms.map(([p, i]) => binom(p, i)).join(" + "))} = ${ltr(rank)} מספרים קטנים מ-${ltr(x)} עם ${ltr(k)} אחדות.`;
        if (st.k === N) {
          const name = st.dir === "next" ? "הבא אחרי" : "הקודם ל-";
          answer(box, S.result ? `${name}${ltr(x)} עם ${ltr(k)} אחדות הוא ${ltr(`${S.result} = ${bin(S.result, w)}`)}.` :
            `אין מספר ${st.dir === "next" ? "הבא" : "קודם"} עם ${ltr(k)} אחדות ב-${ltr(w)} ביטים.`, box.querySelectorAll(`.gs-bits tr:nth-child(${N + 1}) td.gs-val`));
        } else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= steps().rows.length - 1, restart: () => { st.k = 0; draw(); } });
      const setX = (x) => { stop(); st.x = x; st.k = 0; $(".gs-err").textContent = ""; draw(); };
      $(".gs-x").addEventListener("change", () => {
        const v = Number($(".gs-x").value), mask = 2 ** st.w - 1;
        if (!Number.isInteger(v) || v < 1 || v > mask) { $(".gs-err").textContent = `המספר : שלם מ-1 עד ${mask}`; return; }
        setX(v);
      });
      $(".gs-x").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".gs-x").blur(); });
      $(".gs-w").addEventListener("change", () => {
        st.w = Number($(".gs-w").value);
        const mask = 2 ** st.w - 1;
        setX(st.x & mask || 2 ** Math.min(ones(st.x), st.w) - 1);
      });
      $(".gs-dir").addEventListener("change", () => { stop(); st.dir = $(".gs-dir").value; st.k = 0; draw(); });
      $(".gs-next").addEventListener("click", () => { const v = gsNext(st.x, st.w); if (v) setX(v); });
      $(".gs-prev").addEventListener("click", () => { const v = gsPrev(st.x, st.w); if (v) setX(v); });
      $(".gs-first").addEventListener("click", () => setX(2 ** ones(st.x) - 1));
      $(".gs-last").addEventListener("click", () => { const k = ones(st.x); setX((2 ** k - 1) * 2 ** (st.w - k)); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(0, st.k - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = steps().rows.length - 1; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, { x: d0.x, w: d0.w, dir: "next", k: 0 }); $(".gs-err").textContent = ""; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { popnext: popnextView },
    help: {
      popnext: "בוחרים רוחב ומספר. השלבים של הנוסחה נפתחים אחד אחרי השני, עם הביטים שכל שלב עוסק בהם, למספר הבא או למספר הקודם (דרך ההיפוך). הכפתורים הבא, הקודם, הראשון והאחרון עוברים ברשימה של כל המספרים עם אותו מספר של אחדות, ומתחת מופיע המקום ברשימה כסכום של מקדמי בינום.",
    },
    models: { gsNext, gsPrev, gsRank, gsSteps },
  });
})();
