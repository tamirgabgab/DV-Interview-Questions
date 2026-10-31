// kinds: popnext
//   popnext                0060        the next number with as many ones (or zeros, without the leading ones): a bit, a width and a number, the rows of Gosper's formula (or of the previous one through the complement) step by step, with the jump to the next or previous length for zeros, and the next / previous buttons
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, code, ltr, speedSel } = dvqExplorers.lib;

  // The next number with as many ones (0060), for widths up to 16 bits (plain JS numbers).
  // gsNext / gsPrev return 0 when there is none; gsNext0 / gsPrev0 do the same for the zeros
  // below the top one (any length); gsSteps gives the rows of Gosper's formula, each with
  // the bits the step is about (as in tools/figures/q0060.py).
  const ones = (v) => { let n = 0; for (; v; v >>>= 1) n += v & 1; return n; };
  const bitsOf = (v) => { const out = []; for (let p = 0; v; p++, v >>>= 1) if (v & 1) out.push(p); return out; };
  const range = (a, b) => Array.from({ length: Math.max(0, b - a) }, (_, i) => a + i);
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
  const lenOf = (x) => (x ? Math.floor(Math.log2(x)) + 1 : 0);
  const gsNext0 = (x) => { const L = lenOf(x), z = L - ones(x), y = gsNext(x, L); return y || 2 ** L + 2 ** (L - z) - 1; };
  const gsPrev0 = (x) => {
    const L = lenOf(x), z = L - ones(x), y = gsPrev(x, L);
    if (y >= 2 ** (L - 1)) return y;
    return L - 1 - z >= 1 ? (2 ** (L - 1 - z) - 1) * 2 ** z : 0;
  };

  const WIDTHS = [4, 5, 6, 8, 10, 12, 16];
  const ROWS = 10;                     // the most rows (the previous one with zeros), so the table keeps its size
  const XMAX = 2 ** 16 - 1;
  const bin = (v) => v.toString(2);

  // the rows the box shows, each with its note: the next one or the previous one (as
  // ~next(~x)), counting ones in w bits or zeros in the length of x
  const stepsOf = (x, w, dir, bit) => {
    const L = bit ? w : lenOf(x), z = lenOf(x) - ones(x), mask = 2 ** L - 1;
    const g = gsSteps(dir === "next" ? x : ~x & mask, L);
    const N = (t) => `${ltr(t)}`;
    const gNotes = (name) => [
      `האחד הנמוך ביותר של ${code(name)} : ${N(`c = 2^${g.t}`)}.`,
      g.next ? `ה-carry מכבה את הבלוק הנמוך (${N(g.m)} אחדות) ומדליק את הביט ${N(g.t + g.m)} שמעליו.`
        : `החיבור גולש מעבר ל-${N(L)} ביטים : הבלוק היה בראש, ואין מספר הבא אחרי ${code(name)} ב-${N(L)} ביטים.`,
      `הביטים שהשתנו : הבלוק והביט החדש.`,
      `שתיים פחות : נשארות ${N(Math.max(0, g.m - 1))} אחדות.`,
      `החילוק ב-${code("c")} מזיז עוד ${N(g.t)} מקומות ימינה, לתחתית.`,
      `המספר הבא אחרי ${code(name)} עם אותן אחדות.`,
    ];
    const count = bit ? `${N(ones(x))} אחדות ב-${N(w)} ביטים` : `${N(z)} אפסים באורך ${N(L)}`;
    let rows, result;
    if (dir === "next") {
      rows = g.rows.map((r, i) => ({ ...r, note: i === 0 ? `${count}. בלוק האחדות הנמוך מסומן : ${N(g.m)} אחדות מהמקום ${N(g.t)}.` : gNotes("x")[i - 1] }));
      result = g.next;
      if (!bit && !g.next) {
        result = 2 ** L + 2 ** (L - z) - 1;
        rows.push({ label: "1 0…0 1…1", v: result, marks: [L].concat(range(0, L - z)), note: `האורך ${N(L)} נגמר. הקטן ביותר באורך ${N(L + 1)} עם ${N(z)} אפסים : אחד בראש, ${N(z)} אפסים, והאחדות בתחתית.` });
      }
    } else {
      rows = [{ label: "x", v: x, marks: [], note: `${count}. הקודם הוא ההיפוך של המספר הבא אחרי ${code("~x")}.` },
        { label: "y = ~x", v: ~x & mask, marks: [], note: `ההיפוך ב-${N(L)} ביטים. הסדר מתהפך, ועכשיו מחפשים את הבא.` }]
        .concat(g.rows.slice(1).map((r, i) => ({ ...r, label: r.label.replace(/x/g, "y"), note: gNotes("y")[i] })));
      result = 0;
      if (g.next) {
        result = ~g.next & mask;
        rows.push({ label: "~(r | s)", v: result, marks: [], note: bit || result >= 2 ** (L - 1) ? `היפוך בחזרה : זה המספר הקודם ל-${code("x")}.` : `היפוך בחזרה. הביט העליון כבוי : זה מספר קצר יותר, עם יותר אפסים.` });
      }
      if (!bit && result < 2 ** (L - 1)) {
        result = L - 1 - z >= 1 ? (2 ** (L - 1 - z) - 1) * 2 ** z : 0;
        if (result) rows.push({ label: "1…1 0…0", v: result, marks: range(z, L - 1), note: `אין קודם באורך ${N(L)}. הגדול ביותר באורך ${N(L - 1)} עם ${N(z)} אפסים : האחדות למעלה, האפסים למטה.` });
        else rows[rows.length - 1].note += ` ובאורך ${N(L - 1)} אין מקום לאחד ול-${N(z)} אפסים : אין מספר קודם.`;
      }
    }
    return { rows, result, width: bit ? w : Math.max(4, L + 1) };
  };

  const popnextView = () => ({
    mount(box) {
      const d0 = { x: Number(box.dataset.x) || 92, w: Number(box.dataset.w) || 8 };
      const st = { x: d0.x, w: d0.w, dir: "next", bit: 1, k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>סופרים <select class="gs-bit" aria-label="איזה ביט סופרים"><option value="1" selected>אחדות (ביט 1)</option><option value="0">אפסים (ביט 0)</option></select></label>` +
        `<label>הרוחב <select class="gs-w" aria-label="רוחב המילה בביטים">${WIDTHS.map((v) => `<option value="${v}"${v === d0.w ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<label><span>המספר</span><input type="number" class="ex-num gs-x" min="1" dir="ltr" aria-label="המספר x, בעשרוני"></label>` +
        `<button type="button" class="md-button gs-prev">הקודם</button>` +
        `<button type="button" class="md-button md-button--primary gs-next">הבא</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err gs-err"></span></div>` +
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
        `<span class="viz-legend"><span><i class="gs-key-one"></i>ביט דולק</span><span><i class="gs-key-mark"></i>הביטים שהשלב עוסק בהם</span><span><i class="gs-key-lead"></i>אפס מוביל, לא נספר</span></span>` +
        `<p class="gs-note"></p>`;
      const $ = (s) => box.querySelector(s);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const steps = () => stepsOf(st.x, st.w, st.dir, st.bit);
      const max = () => (st.bit ? 2 ** st.w - 1 : XMAX);
      const draw = () => {
        const { x, w, bit } = st;
        const S = steps(), N = S.rows.length - 1, D = S.width;
        st.k = Math.min(st.k, N);
        $(".gs-w").value = String(w); $(".gs-x").value = String(x); $(".gs-dir").value = st.dir; $(".gs-bit").value = String(bit);
        $(".gs-w").disabled = !bit;
        $(".gs-x").max = String(max());
        const nx = bit ? gsNext(x, w) : gsNext0(x), pv = bit ? gsPrev(x, w) : gsPrev0(x);
        $(".gs-next").disabled = !nx || nx > max();
        $(".gs-prev").disabled = !pv;
        $(".ex-pos").textContent = `שלב ${st.k} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === N;
        const L = lenOf(x);
        $(".gs-sum").innerHTML = `${ltr(`x = ${x} = ${bin(x)}`)} : ` + (bit ? `${ltr(ones(x))} אחדות, ברוחב ${ltr(w)} ביטים.` :
          `${ltr(L - ones(x))} אפסים מתחת לאחד העליון, באורך ${ltr(L)}. האורך יכול להשתנות.`);
        let rows = "";
        for (let r = 0; r < ROWS; r++) {
          const row = S.rows[r] || { label: "·", v: 0, marks: [] }, off = r > st.k || !S.rows[r];
          const lead = !bit && (r === 0 || r === N) ? lenOf(row.v) : -1;      // the leading zeros of x and of the answer
          let cells = "";
          for (let p = D - 1; p >= 0; p--) {
            const one = Math.floor(row.v / 2 ** p) % 2 === 1, mark = !off && row.marks.includes(p);
            cells += `<td class="gs-b${one ? " is-one" : ""}${mark ? " is-mark" : ""}${lead >= 0 && p >= lead ? " is-lead" : ""}">${one ? 1 : 0}</td>`;
          }
          rows += `<tr${off ? ` class="is-off" aria-hidden="true"` : ""}><th>${row.label.replace(/&/g, "&amp;").replace(/>/g, "&gt;")}</th>${cells}<td class="gs-val">${row.v}</td></tr>`;
        }
        $(".gs-bits tbody").innerHTML = rows;
        $(".gs-note").innerHTML = S.rows[st.k].note;
        if (st.k === N) {
          const what = bit ? `${ltr(ones(x))} אחדות` : `${ltr(L - ones(x))} אפסים`;
          const name = st.dir === "next" ? "הבא אחרי " : "הקודם ל-";
          answer(box, S.result ? `${name}${ltr(x)} עם ${what} הוא ${ltr(`${S.result} = ${bin(S.result)}`)}.` :
            `אין מספר ${st.dir === "next" ? "הבא" : "קודם"} עם ${what}${bit ? ` ב-${ltr(w)} ביטים` : ""}.`, box.querySelectorAll(`.gs-bits tr:nth-child(${N + 1}) td.gs-val`));
        } else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= steps().rows.length - 1, restart: () => { st.k = 0; draw(); } });
      const setX = (x) => { stop(); st.x = x; st.k = 0; $(".gs-err").textContent = ""; draw(); };
      $(".gs-x").addEventListener("change", () => {
        const v = Number($(".gs-x").value);
        if (!Number.isInteger(v) || v < 1 || v > max()) { $(".gs-err").textContent = `המספר : שלם מ-1 עד ${max()}`; return; }
        setX(v);
      });
      $(".gs-x").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".gs-x").blur(); });
      $(".gs-w").addEventListener("change", () => {
        st.w = Number($(".gs-w").value);
        setX(st.x & (2 ** st.w - 1) || 2 ** Math.min(ones(st.x), st.w) - 1);
      });
      $(".gs-bit").addEventListener("change", () => {
        st.bit = Number($(".gs-bit").value);
        setX(st.bit && st.x > 2 ** st.w - 1 ? st.x & (2 ** st.w - 1) || 1 : st.x);
      });
      $(".gs-dir").addEventListener("change", () => { stop(); st.dir = $(".gs-dir").value; st.k = 0; draw(); });
      $(".gs-next").addEventListener("click", () => { const v = st.bit ? gsNext(st.x, st.w) : gsNext0(st.x); if (v && v <= max()) setX(v); });
      $(".gs-prev").addEventListener("click", () => { const v = st.bit ? gsPrev(st.x, st.w) : gsPrev0(st.x); if (v) setX(v); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(0, st.k - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = steps().rows.length - 1; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, { x: d0.x, w: d0.w, dir: "next", bit: 1, k: 0 }); $(".gs-err").textContent = ""; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { popnext: popnextView },
    help: {
      popnext: "בוחרים מה סופרים (אחדות ברוחב קבוע, או אפסים מתחת לאחד העליון), רוחב ומספר. השלבים של הנוסחה נפתחים אחד אחרי השני, עם הביטים שכל שלב עוסק בהם, למספר הבא או למספר הקודם (דרך ההיפוך). עם אפסים, כשהאורך נגמר מופיע שלב של מעבר לאורך הבא או הקודם. הכפתורים הבא והקודם מחליפים את המספר בשכן שלו.",
    },
    models: { gsNext, gsPrev, gsNext0, gsPrev0, gsSteps },
  });
})();
