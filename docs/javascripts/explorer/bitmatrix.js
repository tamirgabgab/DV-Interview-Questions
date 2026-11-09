// kinds: bitmatrix
//   bitmatrix              0075        an 8 x 8 bit matrix in a 64-bit word (row r = byte r), drawn by clicking cells or typing the word, taken through the three delta swaps of the transpose one stage per step: the mask bits and their partners tinted, the bits that moved framed, and the word, the mask, the shift and t written under the grid
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const STAGES = [
    { s: 7n, mask: 0x00AA00AA00AA00AAn, what: "בתוך כל בלוק 2×2" },
    { s: 14n, mask: 0x0000CCCC0000CCCCn, what: "בלוקים 2×2 בתוך כל 4×4" },
    { s: 28n, mask: 0x00000000F0F0F0F0n, what: "בלוקים 4×4" },
  ];
  const deltaSwap = (x, mask, s) => { const t = ((x >> s) ^ x) & mask; return x ^ t ^ (t << s); };
  // The word before and after each of the three stages.
  const bmStages = (x) => { const out = [x]; STAGES.forEach((g) => out.push(deltaSwap(out[out.length - 1], g.mask, g.s))); return out; };
  const bit = (x, p) => Number((x >> BigInt(p)) & 1n);
  const hex = (x) => `0x${x.toString(16).toUpperCase().padStart(16, "0")}`;
  const fromRows = (rows) => rows.reduce((x, row, r) => [...row].reduce((y, ch, c) => (ch === "#" ? y | (1n << BigInt(8 * r + c)) : y), x), 0n);
  const PATTERNS = {
    F: { label: "האות F", x: fromRows(["........", ".#####..", ".#......", ".####...", ".#......", ".#......", ".#......", "........"]) },
    row: { label: "השורה העליונה", x: 0xFFn },
    corner: { label: "הבלוק 4×4 הימני העליון", x: fromRows(["....####", "....####", "....####", "....####", "........", "........", "........", "........"]) },
    diag: { label: "האלכסון", x: 0x8040201008040201n },
  };
  const parseWord = (text) => {
    const m = /^\s*(?:0x)?([0-9a-f]{1,16})\s*$/i.exec(text);
    return m ? BigInt(`0x${m[1]}`) : null;
  };

  const bitmatrixView = () => ({
    mount(box) {
      const p0 = PATTERNS[box.dataset.pattern] ? box.dataset.pattern : "F";
      const st = { x: PATTERNS[p0].x, s: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>דוגמה <select class="bm-pat" aria-label="דוגמה">${Object.entries(PATTERNS).map(([v, p]) => `<option value="${v}">${p.label}</option>`).join("")}<option value="own">משלי</option></select></label>` +
        `<label>המילה <input type="text" class="bm-word" dir="ltr" spellcheck="false" size="20" aria-label="המילה של 64 ביט, בהקסדצימלי"></label>` +
        `<button type="button" class="md-button bm-rand">מילה אקראית</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לדוגמה של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">לפני השלב הראשון</button>` +
        `<button type="button" class="md-button ex-prev">השלב הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">השלב הבא</button>` +
        `<button type="button" class="md-button ex-end">כל השלבים</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1100, 600) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary bm-sum" aria-live="polite"></p>` +
        `<div class="bm-fig" data-steady></div>` +
        `<span class="viz-legend"><span><i class="bm-key-on"></i>ביט דולק</span><span><i class="pm-key-c1"></i>במסכה של השלב</span><span><i class="pm-key-c2"></i>בן הזוג, ב-${ltr("p + s")}</span><span><i class="pm-key-hl"></i>ביט שהשתנה</span></span>` +
        `<div class="bm-vals" data-steady></div>` +
        `<p class="bm-note"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const pat = () => Object.keys(PATTERNS).find((k) => PATTERNS[k].x === st.x) || "own";

      const draw = () => {
        st.s = Math.min(Math.max(st.s, 0), 3);
        const ws = bmStages(st.x), cur = ws[st.s], prev = st.s ? ws[st.s - 1] : null, g = st.s ? STAGES[st.s - 1] : null;
        $(".bm-pat").value = pat();
        if (document.activeElement !== $(".bm-word")) $(".bm-word").value = hex(st.x);
        $(".ex-pos").textContent = `שלב ${st.s} מתוך 3`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.s === 3;
        // the grid: row r = byte r, column c = bit c; the stage's mask bits and their partners
        // tinted, the bits that changed in this stage framed, the diagonal marked
        let rows = `<tr class="pm-head"><th></th>${Array.from({ length: 8 }, (_, c) => `<td>${c}</td>`).join("")}</tr>`;
        for (let r = 0; r < 8; r++) {
          rows += `<tr><th>בית ${r}</th>`;
          for (let c = 0; c < 8; c++) {
            const p = 8 * r + c, on = bit(cur, p);
            let cls = on ? "bm-on" : "";
            if (g && bit(g.mask, p)) cls += " c1";
            else if (g && p >= Number(g.s) && bit(g.mask, p - Number(g.s))) cls += " c2";
            if (prev !== null && bit(prev, p) !== on) cls += " is-hl";
            if (r === c) cls += " bm-diag";
            rows += `<td class="pm-c bm-cell ${cls}" data-p="${p}" title="(${r}, ${c}) : ביט ${p}">${on}</td>`;
          }
          rows += "</tr>";
        }
        $(".bm-fig").innerHTML = `<div class="pm-scroll" tabindex="0" role="region" aria-label="מטריצת הביטים אחרי ${st.s} שלבים"><table class="pm-cells bm-cells" dir="ltr"><tbody>${rows}</tbody></table></div>`;
        // the values: the word after every stage so far, and this stage's mask, shift and t
        const line = (name, v, now) => `<tr${now ? ' class="is-now"' : ""}><th>${name}</th><td><code>${hex(v)}</code></td></tr>`;
        let vals = line("x", ws[0], st.s === 0);
        for (let i = 1; i <= 3; i++) vals += i <= st.s ? line(`אחרי שלב ${i}`, ws[i], i === st.s) : `<tr class="is-later"><th>אחרי שלב ${i}</th><td><code>·</code></td></tr>`;
        if (g) {
          const t = ((prev >> g.s) ^ prev) & g.mask;
          vals += `<tr><th>המסכה, ${ltr(`s = ${g.s}`)}</th><td><code>${hex(g.mask)}</code></td></tr><tr><th>${ltr("t")}</th><td><code>${hex(t)}</code></td></tr>`;
        } else vals += `<tr class="is-later"><th>המסכה</th><td><code>·</code></td></tr><tr class="is-later"><th>${ltr("t")}</th><td><code>·</code></td></tr>`;
        $(".bm-vals").innerHTML = `<table class="bm-vtab" dir="ltr"><tbody>${vals}</tbody></table>`;
        const ones = [...Array(64).keys()].filter((p) => bit(st.x, p)).length;
        $(".bm-sum").innerHTML = `${ltr(ones)} ביטים דולקים. כל שלב הוא ${ltr("t = ((x >> s) ^ x) & mask, x ^= t ^ (t << s)")}${NB}: 16 זוגות מתחלפים בבת אחת, והאלכסון לא זז אף פעם.`;
        if (!g) $(".bm-note").innerHTML = `המטריצה לפני השחלוף. האיבר ${ltr("(r, c)")} הוא הביט ${ltr("8r + c")}, ובסוף הוא צריך להיות בביט ${ltr("8c + r")}.`;
        else {
          const t = ((prev >> g.s) ^ prev) & g.mask, changed = [...Array(64).keys()].filter((p) => bit(t, p)).length;
          $(".bm-note").innerHTML = `שלב ${st.s}, ${g.what}${NB}: הזזה ${ltr(g.s)}. ${changed ? `${ltr(changed)} מתוך 16 הזוגות היו שונים, והם התחלפו.` : "כל 16 הזוגות היו שווים, ולכן אף ביט לא השתנה."}`;
        }
        if (st.s === 3) answer(box, `${ltr(hex(cur))}${NB}: השחלוף. כל ביט ${ltr("8r + c")} עבר ל-${ltr("8c + r")}.`, ".bm-cells .is-hl");
        else answer(box, null);
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.s++; draw(); }, done: () => st.s >= 3, restart: () => { st.s = 0; draw(); } });
      const setWord = (x) => { stop(); st.x = BigInt.asUintN(64, x); st.s = 0; draw(); };
      $(".bm-pat").addEventListener("change", () => { const v = $(".bm-pat").value; if (PATTERNS[v]) setWord(PATTERNS[v].x); });
      $(".bm-word").addEventListener("change", () => {
        const x = parseWord($(".bm-word").value);
        if (x === null) { $(".bm-note").textContent = "צריך מילה בהקסדצימלי, עד 16 ספרות, למשל 0x8040201008040201."; return; }
        setWord(x);
      });
      $(".bm-rand").addEventListener("click", () => setWord(BigInt.asUintN(64, (BigInt(Math.floor(Math.random() * 2 ** 32)) << 32n) | BigInt(Math.floor(Math.random() * 2 ** 32)))));
      // a click on a cell toggles its bit in the word (before the stages; the text field is the
      // keyboard's way to the same word)
      $(".bm-fig").addEventListener("click", (e) => {
        const td = e.target.closest(".bm-cell");
        if (!td) return;
        const p = BigInt(td.dataset.p), shown = bmStages(st.x)[st.s];
        const back = { 0: (y) => y, 1: (y) => deltaSwap(y, STAGES[0].mask, STAGES[0].s), 2: (y) => deltaSwap(deltaSwap(y, STAGES[1].mask, STAGES[1].s), STAGES[0].mask, STAGES[0].s), 3: (y) => [2, 1, 0].reduce((z, i) => deltaSwap(z, STAGES[i].mask, STAGES[i].s), y) };
        const s = st.s;
        st.x = BigInt.asUintN(64, back[s](shown ^ (1n << p)));
        $(".bm-word").value = hex(st.x);
        $(".bm-word").dispatchEvent(new Event("change", { bubbles: true }));
        st.s = s; draw();
      });
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = 3; draw(); });
      $(".ex-reset").addEventListener("click", () => setWord(PATTERNS[p0].x));
      draw();
    },
  });

  dvqExplorers.register({
    views: { bitmatrix: bitmatrixView },
    help: {
      bitmatrix: "בוחרים דוגמה, מקלידים מילה בהקסדצימלי או לוחצים על תאים כדי להדליק ולכבות ביטים. ״השלב הבא״ מבצע delta swap אחד : הביטים של המסכה צבועים, בני הזוג שלהם בצבע אחר, והביטים שהשתנו ממוסגרים. מתחת לטבלה המילה אחרי כל שלב, המסכה, ההזזה ו-t.",
    },
    models: { bmStages },
    // on a computer: the matrix and its legend on the left, the words after each stage and
    // the stage's note on the right
    cols: { bitmatrix: { side: ".bm-vals, .bm-note" } },
  });
})();
