// kinds: rtlbug
//   rtlbug                 0110        the three RTL snippets of the page cycle by cycle, the code under review or its fix: a timing strip whose inputs are edited (the fields of the cycle under the cursor, or a cell of the strip), the outputs drawn up to that cycle against want, what the designer meant; beside it what each line of the code reads and writes in that cycle, and for the average the bits of the sum and the carry that the 8-bit context loses
// Loaded after core.js on the page of question 0110 (hooks/questions.py adds the script
// tag); under Node tools/explorer_node.js loads every kind file and merges the models for
// the question tests (tests/0110 compares them with tools/figures/q0110.py and the page).
(() => {
  const { answer, autoplay, bitsOf, code, ltr, speedSel, waveStrip } = dvqExplorers.lib;
  const NB = " ";                                   // before a Hebrew colon
  const N = 8;                                           // cycles 0 .. 7, as on the page
  const SW = 34, LW = 58;                                // the strip: a cycle's width, the names' width

  // The page's inputs, cycle by cycle (tools/figures/q0110.py D_A, EN_B, D_B, A_C, B_C).
  const rbPage = {
    dA: [0, 1, 1, 0, 1, 0, 0, 0],
    enB: [0, 1, 1, 0, 0, 1, 0, 0],
    dB: [3, 5, 9, 12, 7, 6, 10, 1],
    aC: [10, 100, 200, 127, 128, 255, 255, 60],
    bC: [20, 50, 100, 128, 128, 255, 1, 61],
  };

  // --- the models, as the page's Python (delay3, en_gate, avg8) ------------------------------

  // part a: [q1, q2, q3] during every cycle. At each edge the three lines run in order: with
  // = (blocking) each line reads what the line above has just written, with <= every
  // right-hand side is read before any register is written. Every variable starts at 0.
  const rbDelay = (d, blocking = false) => {
    let q1 = 0, q2 = 0, q3 = 0;
    const out = [];
    for (const x of d) {
      out.push([q1, q2, q3]);
      if (blocking) { q1 = x; q2 = q1; q3 = q2; } else [q1, q2, q3] = [x, q1, q2];
    }
    return out;
  };
  const rbDelayWant = (d) => d.map((_, k) => (k >= 3 ? d[k - 3] : 0));
  // the edge that opens cycle k >= 1: per line, [the right-hand side's value before the
  // edge, the value the line reads (and writes)]
  const rbEdge = (d, k, blocking = false) => {
    const [p1, p2] = rbDelay(d, blocking)[k - 1], x = d[k - 1];
    return blocking ? [[x, x], [p1, x], [p2, x]] : [[x, x], [p1, p1], [p2, p2]];
  };

  // part b: y during every cycle; without the default line a cycle with en low writes
  // nothing, and y keeps its value (a latch)
  const rbGate = (en, d, dflt = true) => {
    let y = 0;
    return en.map((e, k) => { if (dflt) y = 0; if (e) y = d[k]; return y; });
  };
  const rbGateWant = (en, d) => en.map((e, k) => (e ? d[k] : 0));
  // the cycle whose d the code under review shows in cycle k: k itself with en high, else
  // the last cycle before it with en high (-1: none, y is still the starting 0)
  const rbHeld = (en, k) => { let j = k; while (j >= 0 && !en[j]) j--; return j; };

  // part c: (a + b) >> 1 in a context of `width` bits, the result kept to 8 bits
  const rbAvg = (a, b, width = 9) => (((a + b) % (1 << width)) >> 1) % 256;
  const rbAvgWant = (a, b) => Math.floor((a + b) / 2);
  const rbSum = (a, b) => ({ sum: a + b, carry: (a + b) >> 8, sum8: (a + b) % 256, bug: rbAvg(a, b, 8), fix: rbAvg(a, b, 9) });

  // the traces of a part: the outputs of the chosen code and what the designer meant
  const rbTrace = (part, st, fix) => {
    if (part === "a") { const tr = rbDelay(st.dA, !fix); return { out: tr.map((r) => r[2]), want: rbDelayWant(st.dA), tr }; }
    if (part === "b") return { out: rbGate(st.enB, st.dB, fix), want: rbGateWant(st.enB, st.dB) };
    return { out: st.aC.map((a, k) => rbAvg(a, st.bC[k], fix ? 9 : 8)), want: st.aC.map((a, k) => rbAvgWant(a, st.bC[k])) };
  };

  // The inputs and the cursor as one text, for the link: "01101000_01100100_3.5.9…_10.100…_20.50…_3"
  const rbEncode = (st) => [st.dA.join(""), st.enB.join(""), st.dB.join("."), st.aC.join("."), st.bC.join("."), st.k].join("_");
  const rbDecode = (text) => {
    const m = /^([01]{8})_([01]{8})_([\d.]+)_([\d.]+)_([\d.]+)_(\d)$/.exec(String(text));
    if (!m) return null;
    const nums = (s, max) => { const v = s.split(".").map(Number); return v.length === N && v.every((x) => Number.isInteger(x) && x >= 0 && x <= max) ? v : null; };
    const dB = nums(m[3], 15), aC = nums(m[4], 255), bC = nums(m[5], 255), k = Number(m[6]);
    if (!dB || !aC || !bC || k >= N) return null;
    return { dA: [...m[1]].map(Number), enB: [...m[2]].map(Number), dB, aC, bC, k };
  };

  // --- the box --------------------------------------------------------------------------------

  const heList = (ks) => (ks.length === 1 ? `${ks[0]}` : `${ks.slice(0, -1).join(", ")} ו-${ks[ks.length - 1]}`);
  const PART_LABEL = { a: "קו ההשהיה", b: "המוצא עם האפשור", c: "הממוצע" };
  const OUT = { a: "q3", b: "y", c: "avg" };

  const rbView = () => ({
    mount(box) {
      const page = () => JSON.parse(JSON.stringify(rbPage));
      const st = { part: ["a", "b", "c"].includes(box.dataset.part) ? box.dataset.part : "c", fix: false, k: 0, note: "", ...page() };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הסעיף <select class="rb-part" aria-label="הסעיף שהתיבה מריצה"><option value="a">א, ${PART_LABEL.a}</option><option value="b">ב, ${PART_LABEL.b}</option><option value="c">ג, ${PART_LABEL.c}</option></select></label>` +
        `<label>הקוד <select class="rb-ver" aria-label="הקוד מהשאלה או התיקון"><option value="bug">מהשאלה</option><option value="fix">התיקון</option></select></label>` +
        `<button type="button" class="md-button rb-reset">הכניסות שבעמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">המחזור הראשון</button>` +
        `<button type="button" class="md-button ex-prev">המחזור הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1600, 900, 450) +
        `<button type="button" class="md-button md-button--primary ex-next">המחזור הבא</button>` +
        `<button type="button" class="md-button ex-end">המחזור האחרון</button><span class="ex-pos"></span></div>` +
        `<div class="ex-controls rb-inrow"></div>` +
        `<div class="wv-wrap rb-wave" tabindex="0" role="group" aria-label="צורת הגל, גלילה אופקית"></div>` +
        `<span class="viz-legend rb-legend"><span><i class="rb-key-now"></i>המחזור הנוכחי</span>` +
        `<span><i class="rb-key-want"></i>‏want${NB}: מה שהמתכנן רצה</span><span><i class="rb-key-bad"></i>המוצא שונה מ-want</span></span>` +
        `<p class="wv-sum rb-sum"></p>` +
        `<p class="wv-step rb-step" aria-live="polite"></p>` +
        `<div class="rb-panel" data-steady></div>`;
      answer(box, NB); answer(box, null);                // the answer line keeps its place from the first cycle
      const $ = (sel) => box.querySelector(sel);
      const partSel = $(".rb-part"), verSel = $(".rb-ver"), inrow = $(".rb-inrow");
      partSel.value = st.part;

      // the fields of the cycle under the cursor: they edit that cycle's inputs (their values
      // ride in the link as the box's own text, data-nolink)
      const FIELDS = {
        a: [["dA", "check", "d"]],
        b: [["enB", "check", "en"], ["dB", 15, "d"]],
        c: [["aC", 255, "a"], ["bC", 255, "b"]],
      };
      const buildInputs = () => {
        inrow.innerHTML = `<span class="rb-inhead">הכניסות של מחזור <b class="rb-k">0</b>${NB}:</span>` + FIELDS[st.part].map(([key, max, name]) => (max === "check"
          ? `<label class="rb-in"><input type="checkbox" class="rb-f" data-key="${key}" data-nolink aria-label="${name} במחזור הנוכחי"> ${code(`${name} = 1`)}</label>`
          : `<label class="rb-in">${code(name)} <input type="number" class="ex-num rb-f" data-key="${key}" data-max="${max}" min="0" max="${max}" step="1" dir="ltr" data-nolink aria-label="${name} במחזור הנוכחי, מספר מ-0 עד ${max}"></label>`)).join("");
      };

      const rows = (tr) => {
        const k = st.k, upto = (v) => v.slice(0, k + 1);
        const bad = upto(tr.out.map((v, i) => (v !== tr.want[i] ? 1 : 0)));
        const flag = { name: "≠ want", kind: "flag", values: bad };
        const clk = { name: "clk", kind: "clock" };
        if (st.part === "a") {
          return [clk,
            { name: "d", kind: "bit", values: st.dA, cls: "wv-s1", cells: (j) => `מחזור ${j}${NB}: d = ${st.dA[j]}, לחיצה הופכת` },
            { name: "q1", kind: "bit", values: upto(tr.tr.map((r) => r[0])), cls: "wv-s3" },
            { name: "q2", kind: "bit", values: upto(tr.tr.map((r) => r[1])), cls: "wv-s3" },
            { name: "q3", kind: "bit", values: upto(tr.out), cls: "wv-s2" },
            { name: "want", kind: "bit", values: tr.want, cls: "wv-dim" }, flag];
        }
        const ins = st.part === "b"
          ? [{ name: "en", kind: "bit", values: st.enB, cls: "wv-s1", cells: (j) => `מחזור ${j}${NB}: en = ${st.enB[j]}, לחיצה הופכת` },
            { name: "d", kind: "bus", values: st.dB, cells: (j) => `מחזור ${j}${NB}: d = ${st.dB[j]}, לחיצה עוברת למחזור הזה` }]
          : [{ name: "a", kind: "bus", values: st.aC, cells: (j) => `מחזור ${j}${NB}: a = ${st.aC[j]}, לחיצה עוברת למחזור הזה` },
            { name: "b", kind: "bus", values: st.bC, cells: (j) => `מחזור ${j}${NB}: b = ${st.bC[j]}, לחיצה עוברת למחזור הזה` }];
        return [clk, ...ins, { name: OUT[st.part], kind: "bus", values: upto(tr.out), cls: "rb-out" },
          { name: "want", kind: "bus", values: tr.want, cls: "rb-want" }, flag];
      };

      const verdict = (out, want) => (out === want
        ? ` עכשיו ${code(`${OUT[st.part]} = ${out}`)}, כמו שהמתכנן רצה <span class="wv-ok">✓</span>`
        : ` עכשיו ${code(`${OUT[st.part]} = ${out}`)}, והמתכנן רצה ${ltr(want)} <span class="wv-bad">✗</span>`);

      // part a: the edge that opened the cycle, line by line
      const stepA = (tr) => {
        const k = st.k;
        if (k === 0) return `מחזור 0${NB}: עוד לא הייתה עלייה של ${code("clk")}, ו-Verilator מתחיל את ${code("q1")}, ${code("q2")} ו-${code("q3")} ב-0.${verdict(tr.out[0], tr.want[0])}.`;
        const x = st.dA[k - 1], [p1, p2] = tr.tr[k - 1];
        const t = st.fix
          ? `העלייה שפתחה את מחזור ${k}${NB}: שלוש השורות קוראות קודם, ${code(`d = ${x}`)}, ${code(`q1 = ${p1}`)} ו-${code(`q2 = ${p2}`)}, ורק בסוף צעד הזמן כותבות. ${code("q2")} מקבל את ה-${code("q1")} הישן, ו-${code("q3")} את ה-${code("q2")} הישן.`
          : `העלייה שפתחה את מחזור ${k}${NB}: השורות רצות לפי הסדר, וכל אחת כותבת מיד. ${code("q1 = d")} כותבת ${x}, ${code("q2 = q1")} קוראת את ה-${x} שנכתב הרגע, וגם ${code("q3 = q2")}.`;
        return t + verdict(tr.out[k], tr.want[k]) + ".";
      };
      const panelA = (tr) => {
        const k = st.k, op = st.fix ? "<=" : "=", lines = [["q1", "d"], ["q2", "q1"], ["q3", "q2"]];
        const edge = k ? rbEdge(st.dA, k, !st.fix) : null;
        const body = lines.map(([l, r], i) => {
          const [old, got] = edge ? edge[i] : ["–", "–"], fresh = edge && got !== old;
          return `<tr${fresh ? ' class="is-new"' : ""}><td>${code(`${l} ${op} ${r};`)}</td><td>${old}</td><td>${got}${fresh ? ` <span class="rb-tag">חדש</span>` : ""}</td></tr>`;
        }).join("");
        return `<p class="rb-cap">${k ? `העלייה שפתחה את מחזור ${k}` : "מחזור 0, לפני העלייה הראשונה"}, שורה אחרי שורה${NB}:</p>` +
          `<table class="rb-tab"><thead><tr><th scope="col">השורה</th><th scope="col">הצד הימני לפני העלייה</th><th scope="col">השורה קוראת וכותבת</th></tr></thead><tbody>${body}</tbody></table>`;
      };

      // part b: the run of the block in the cycle
      const stepB = (tr) => {
        const k = st.k, e = st.enB[k], x = st.dB[k], y = tr.out[k];
        let t;
        if (st.fix) {
          t = e ? `מחזור ${k}${NB}: ${code("y = '0;")} כותבת 0, ${code("en")} גבוה, ולכן ${code("y = d;")} דורסת אותה${NB}: ${code(`y = ${x}`)}.`
            : `מחזור ${k}${NB}: ${code("y = '0;")} כותבת 0, ${code("en")} נמוך, וה-${code("if")} לא מתקיים${NB}: ${code("y")} נשאר 0.`;
        } else if (e) {
          t = `מחזור ${k}${NB}: ${code("en")} גבוה, ולכן ${code("y = d;")} כותבת ${code(`y = ${x}`)}.`;
        } else {
          const j = rbHeld(st.enB, k);
          t = `מחזור ${k}${NB}: ${code("en")} נמוך, ה-${code("if")} לא מתקיים, ואף שורה לא כותבת ל-${code("y")}. הוא שומר את ${ltr(y)} ` +
            (j >= 0 ? `ממחזור ${j}${NB}: זה ה-latch.` : `מההתחלה, כי Verilator מתחיל ב-0.`);
        }
        return t + verdict(y, tr.want[k]) + ".";
      };
      const panelB = (tr) => {
        const k = st.k, e = st.enB[k], x = st.dB[k], j = rbHeld(st.enB, k);
        const held = !st.fix && !e;
        const rowsB = [
          [code("y = '0;"), st.fix ? "כותבת 0" : "אין שורה כזו בקוד"],
          [code("if (en)"), e ? `${code("en = 1")}, נכנסים` : `${code("en = 0")}, מדלגים`],
          [code("y = d;"), e ? `כותבת ${ltr(x)}` : "לא רצה"],
          [`${code("y")} אחרי הריצה`, `<b>${tr.out[k]}</b>${held ? (j >= 0 ? `, נשמר ממחזור ${j}` : ", ערך ההתחלה") : ""}`],
        ];
        return `<p class="rb-cap">הריצה של ${code("always_comb")} במחזור ${k}, שורה אחרי שורה${NB}:</p>` +
          `<table class="rb-tab"><thead><tr><th scope="col">השורה</th><th scope="col">בריצה הזו</th></tr></thead><tbody>` +
          rowsB.map(([a, b], i) => `<tr${i === 3 && held ? ' class="is-held"' : ""}><td>${a}</td><td>${b}</td></tr>`).join("") + `</tbody></table>`;
      };

      // part c: the sum, the carry and the shift
      const stepC = (tr) => {
        const k = st.k, a = st.aC[k], b = st.bC[k], s = rbSum(a, b);
        const t = st.fix
          ? `מחזור ${k}${NB}: ב-9 ביטים ${code("a + b")} הוא ${ltr(s.sum)}${s.carry ? ", עם הנשא" : ""}, ו-${code(`${s.sum} >> 1`)} הוא ${ltr(s.fix)}.`
          : `מחזור ${k}${NB}: ${code("a + b")} הוא ${ltr(s.sum)}` + (s.carry
            ? `, אבל ב-8 ביטים נשאר ${ltr(s.sum8)}${NB}: הנשא, 256, נזרק. ${code(`${s.sum8} >> 1`)} הוא ${ltr(s.bug)}.`
            : `, הוא נכנס ב-8 ביטים, ו-${code(`${s.sum8} >> 1`)} הוא ${ltr(s.bug)}.`);
        return t + verdict(tr.out[k], tr.want[k]) + ".";
      };
      const panelC = () => {
        const k = st.k, a = st.aC[k], b = st.bC[k], s = rbSum(a, b);
        const cell = (v, cls = "") => `<td${cls ? ` class="${cls}"` : ""}>${v}</td>`;
        const bits = (v) => [...bitsOf(v, 8)].map((c) => cell(c)).join("");
        const row = (name, c9, v, val, cls = "") => `<tr${cls ? ` class="${cls}"` : ""}><th scope="row" dir="rtl">${name}</th>${c9}${bits(v)}${cell(val, "rb-val")}</tr>`;
        const on = (fix) => (st.fix === fix ? "is-on" : "");
        return `<p class="rb-cap">הביטים של מחזור ${k}${NB}: ${code(`a = ${a}`)}, ${code(`b = ${b}`)}</p>` +
          `<div class="rb-bitwrap" tabindex="0" role="region" aria-label="הביטים של הסכום והממוצע"><table class="rb-tab rb-bits" dir="ltr"><thead><tr><th scope="col" dir="rtl">ביט</th>` +
          [8, 7, 6, 5, 4, 3, 2, 1, 0].map((i) => `<th scope="col">${i}</th>`).join("") + `<th scope="col" dir="rtl">ערך</th></tr></thead><tbody>` +
          row(code("a"), cell(""), a, a) + row(code("b"), cell(""), b, b) +
          row(`${code("a + b")}, 9 ביטים`, cell(s.carry, s.carry ? "is-carry" : ""), s.sum8, s.sum, "rb-sumrow") +
          row("8 ביטים, מהשאלה", cell(s.carry ? "✗" : "", s.carry ? "is-lost" : ""), s.sum8, s.sum8, on(false)) +
          row(`${code("avg")}, מהשאלה`, cell(""), s.bug, s.bug, on(false)) +
          row(`${code("avg")}, התיקון`, cell(""), s.fix, s.fix, on(true)) +
          `</tbody></table></div>`;
      };

      const draw = () => {
        st.k = Math.max(0, Math.min(N - 1, st.k));
        const k = st.k, tr = rbTrace(st.part, st, st.fix);
        verSel.value = st.fix ? "fix" : "bug";
        $(".ex-pos").textContent = `מחזור ${k} מתוך ${N - 1}`;
        $(".ex-start").disabled = $(".ex-prev").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === N - 1;
        $(".rb-k").textContent = String(k);
        inrow.querySelectorAll(".rb-f").forEach((f) => {
          const v = st[f.dataset.key][k];
          if (f.type === "checkbox") f.checked = v === 1; else f.value = String(v);
        });
        $(".rb-wave").innerHTML = waveStrip(rows(tr), N, { role: "group", label: `צורת הגל של סעיף ${"אבג"["abc".indexOf(st.part)]}, ${st.fix ? "התיקון" : "הקוד מהשאלה"}, עד מחזור ${k}`, cursor: k, ticks: (j) => j, slotW: SW, labelW: LW });
        const wv = $(".rb-wave");   // on a phone the strip scrolls: keep the cycle under the cursor in view
        if (wv.scrollWidth > wv.clientWidth) wv.scrollLeft = Math.max(0, k * SW + SW / 2 - (wv.clientWidth - LW) / 2);
        const bad = tr.out.map((v, i) => (v !== tr.want[i] ? i : -1)).filter((i) => i >= 0);
        const seen = bad.filter((i) => i <= k);
        $(".rb-sum").innerHTML = st.note || (seen.length
          ? `עד מחזור ${k}${NB}: ${code(OUT[st.part])} שונה מ-${code("want")} ${seen.length === 1 ? `במחזור ${seen[0]}` : `במחזורים ${heList(seen)}`}.`
          : `עד מחזור ${k}${NB}: ${code(OUT[st.part])} שווה ל-${code("want")} בכל מחזור.`);
        $(".rb-step").innerHTML = st.part === "a" ? stepA(tr) : st.part === "b" ? stepB(tr) : stepC(tr);
        $(".rb-panel").innerHTML = st.part === "a" ? panelA(tr) : st.part === "b" ? panelB(tr) : panelC();
        if (k < N - 1) { answer(box, null); return; }
        const o = OUT[st.part], where = bad.length === 1 ? `במחזור ${bad[0]}` : `ב-${bad.length} מחזורים, ${heList(bad)}`;
        let text;
        if (!bad.length) {
          text = st.fix ? `${code(o)} שווה ל-${code("want")} בכל ${N} המחזורים${NB}: התיקון עושה מה שהמתכנן רצה.`
            : `בכניסות האלה ${code(o)} שווה ל-${code("want")} בכל ${N} המחזורים, אבל רק במקרה${NB}: ${st.part === "a" ? `${code("q3")} עדיין ${code("d")} מושהה במחזור אחד` : st.part === "b" ? "אין מחזור שבו ה-latch שומר ערך שאינו 0" : `אין זוג שבו ${code("a + b")} מגיע ל-256`}.`;
        } else if (st.part === "a") {
          text = `${code("q3")} שונה מ-${code("want")} ${where}${NB}: הוא ${code("d")} מושהה במחזור אחד, לא בשלושה.`;
        } else if (st.part === "b") {
          text = `${code("y")} שונה מ-${code("want")} ${where}${NB}: בכל אחד מהם ${code("en")} נמוך, ו-${code("y")} שומר ערך ישן.`;
        } else {
          text = `${code("avg")} שונה מ-${code("want")} ${where}, בכל אחד ב-128 בדיוק${NB}: שם ${code("a + b")} הוא 256 או יותר.`;
        }
        answer(box, text, box.querySelectorAll(".rb-wave .wv-fail"));
      };

      let stop = () => {};
      const edit = () => { stop(); st.note = ""; };
      partSel.addEventListener("change", () => { edit(); st.part = partSel.value; buildInputs(); draw(); });
      verSel.addEventListener("change", () => { edit(); st.fix = verSel.value === "fix"; draw(); });
      $(".rb-reset").addEventListener("click", () => { edit(); Object.assign(st, page()); draw(); });
      inrow.addEventListener("change", (e) => {
        const f = e.target.closest(".rb-f");
        if (!f) return;
        edit();
        const key = f.dataset.key;
        if (f.type === "checkbox") st[key][st.k] = f.checked ? 1 : 0;
        else {
          const v = Number(f.value), max = Number(f.dataset.max), name = key[0] === "e" ? "en" : key[0];
          if (f.value.trim() === "" || !Number.isInteger(v) || v < 0 || v > max) st.note = `הערך של ${code(name)} הוא מספר שלם מ-0 עד ${max}${NB}: נשאר ${st[key][st.k]}.`;
          else st[key][st.k] = v;
        }
        draw();
      });
      const wrap = $(".rb-wave");
      const tap = (c) => {
        const j = Number(c.dataset.k), row = c.getAttribute("aria-label") || "";
        edit();
        if (row.endsWith("לחיצה הופכת")) {                // a bit of the inputs: d (part a), en (part b)
          const key = st.part === "a" ? "dA" : "enB";
          st[key][j] = 1 - st[key][j];
        } else st.k = j;
        draw();
      };
      wrap.addEventListener("click", (e) => { const c = e.target.closest(".wv-cell"); if (c) tap(c); });
      wrap.addEventListener("keydown", (e) => {
        const c = e.target.closest(".wv-cell");
        if (c && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); tap(c); }
      });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { stop(); st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = N - 1; draw(); });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= N - 1, restart: () => { st.k = 0; draw(); } });
      box.dvqExtra = {
        get: () => rbEncode(st),
        set: (text) => {
          const v = rbDecode(text);
          if (!v) return false;
          Object.assign(st, v, { note: "" });
          draw();
          return true;
        },
      };
      buildInputs();
      draw();
    },
  });

  dvqExplorers.register({
    views: { rtlbug: rbView },
    help: {
      rtlbug: `הבוררים בוחרים סעיף ואת הקוד, זה שמהשאלה או התיקון. החצים, ״הפעלה״ או המקשים ← → מזיזים את השעון מחזור אחרי מחזור${NB}: המוצאים מצוירים עד המחזור הנוכחי, מול want, מה שהמתכנן רצה, ו-✗ מסמן מחזור שבו הם שונים. את הכניסות משנים בשדות של המחזור הנוכחי, או בלחיצה על משבצת ברצועה (ביט מתהפך, וערך מעביר את הסמן למחזור שלו). לצד הרצועה מה כל שורה של הקוד קוראת וכותבת במחזור הזה, ובסעיף ג הביטים של הסכום והנשא. ״הכניסות שבעמוד״ מחזיר את הכניסות של צורות הגל בעמוד.`,
    },
    // the strip, its key and the summary on the left; the step and the table of the lines beside them
    cols: { rtlbug: { side: ".rb-step, .rb-panel", w: "minmax(0, 1fr)" } },
    models: { rbPage, rbDelay, rbDelayWant, rbEdge, rbGate, rbGateWant, rbHeld, rbAvg, rbAvgWant, rbSum, rbTrace, rbEncode, rbDecode },
  });
})();
