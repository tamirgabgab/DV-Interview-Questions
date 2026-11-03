// kinds: bitrev
//   bitrev                 0077        f(1) = 1, f(3) = 3, f(2n) = f(n), f(4n+1) = 2f(2n+1) − f(n), f(4n+3) = 3f(2n+1) − 2f(n): n typed, stepped by one or sent to the next palindrome; the bits of n moving one by one, from the lowest, to the top of f(n) (f(2m + c) = f(m) + c·2^ℓ(m)), and the table of every value the rules need on the way to f(n)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const MAX = 4095;                   // 12 bits: at most 21 rows in the table of the rules

  const bin = (n) => n.toString(2);
  const len = (n) => bin(n).length;
  // f by the five rules of the question, nothing else (0077)
  const brValue = (n, memo = new Map()) => {
    if (n === 1 || n === 3) return n;
    if (memo.has(n)) return memo.get(n);
    let v;
    if (n % 2 === 0) v = brValue(n / 2, memo);
    else {
      const m = Math.floor(n / 4), a = brValue(2 * m + 1, memo), b = brValue(m, memo);
      v = n % 4 === 1 ? 2 * a - b : 3 * a - 2 * b;
    }
    memo.set(n, v);
    return v;
  };
  // the binary digits of n in the opposite order (part b)
  const brReverse = (n) => parseInt([...bin(n)].reverse().join(""), 2);
  const brIsPal = (n) => brReverse(n) === n;
  const brNextPal = (n) => { for (let k = n + 1; k <= MAX; k++) if (brIsPal(k)) return k; return 0; };
  // every value the rules need on the way to f(n), smallest first, with its rule (part a)
  const brRules = (n) => {
    const seen = new Set(), memo = new Map();
    const walk = (k) => {
      if (seen.has(k)) return;
      seen.add(k);
      if (k === 1 || k === 3) return;
      if (k % 2 === 0) walk(k / 2);
      else { walk(2 * Math.floor(k / 4) + 1); walk(Math.floor(k / 4)); }
    };
    walk(n);
    return [...seen].sort((x, y) => x - y).map((k) => {
      const value = brValue(k, memo);
      if (k === 1 || k === 3) return { n: k, rule: "base", m: 0, value };
      if (k % 2 === 0) return { n: k, rule: "even", m: k / 2, value };
      const m = Math.floor(k / 4);
      return { n: k, rule: k % 4 === 1 ? "4m+1" : "4m+3", m, a: brValue(2 * m + 1, memo), b: brValue(m, memo), value };
    });
  };
  // the unrolling of part b: f(n) = acc + f(m) with m = n >> j, the bits b_0 .. b_(j-1)
  // already at the top of f(n); the last step replaces f(1) by 1 (L + 1 steps in all)
  const brSteps = (n) => {
    const L = len(n), out = [];
    let acc = 0;
    for (let j = 0; j < L; j++) {
      out.push({ j, m: Math.floor(n / 2 ** j), acc });
      acc += (Math.floor(n / 2 ** j) % 2) * 2 ** (L - 1 - j);
    }
    out.push({ j: L, m: 0, acc });
    return out;
  };

  const sup = (k) => `2<sup>${k}</sup>`;
  const bitrevView = () => ({
    mount(box) {
      const N0 = Math.min(MAX, Math.max(1, Math.floor(Number(box.dataset.n || 2027)) || 2027));
      const st = { n: N0, k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>n</span><input type="number" class="ex-num br-n" min="1" max="${MAX}" step="1" value="${N0}" dir="ltr" inputmode="numeric" aria-label="n, מספר טבעי"></label>` +
        `<button type="button" class="md-button br-dec">n − 1</button>` +
        `<button type="button" class="md-button br-inc">n + 1</button>` +
        `<button type="button" class="md-button md-button--primary br-pal">הפלינדרום הבא</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערך של העמוד</button><span class="fl-err br-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">כל הצעדים</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 900, 450) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary br-sum" aria-live="polite"></p>` +
        `<p class="ex-title">הביטים של n עוברים לראש של f(n), אחד בכל צעד</p>` +
        `<div class="gs-scroll br-bitswrap"><table class="gs-bits br-bits" dir="ltr" aria-label="הביטים של n ושל f(n) בצעד הזה"><tbody></tbody></table></div>` +
        `<span class="viz-legend"><span><i class="gs-key-one"></i>ביט 1</span><span><i class="gs-key-mark"></i>הביט שעבר בצעד הזה</span><span><i class="gs-key-lead"></i>ביט שכבר עבר, או מקום שעוד לא נקבע</span></span>` +
        `<p class="br-now"></p><p class="br-note"></p>` +
        `<p class="ex-title br-rules-title"></p>` +
        `<div class="gs-scroll br-rules" tabindex="0" role="region" aria-label="הטבלה של הכללים"></div>`;
      const $ = (s) => box.querySelector(s);
      const input = $(".br-n"), play = $(".ex-play"), speed = $(".ex-speed");
      const cell = (bit, cls) => `<td class="gs-b${bit === "1" ? " is-one" : ""}${cls}">${bit}</td>`;
      const rulesTable = (n) => {
        const rows = brRules(n);
        let t = `<table aria-label="הכללים בדרך ל-f(n)"><thead><tr><th>n</th><th>בבינארי</th><th>הכלל</th><th>החישוב</th><th>f(n)</th></tr></thead><tbody>`;
        rows.forEach((r) => {
          let rule, calc;
          if (r.rule === "base") { rule = "נתון"; calc = ltr(`f(${r.n}) = ${r.n}`); }
          else if (r.rule === "even") { rule = ltr(`2 · ${r.m}`); calc = ltr(`f(${r.m}) = ${r.value}`); }
          else if (r.rule === "4m+1") { rule = ltr(`4 · ${r.m} + 1`); calc = ltr(`2 · ${r.a} − ${r.b} = ${r.value}`); }
          else { rule = ltr(`4 · ${r.m} + 3`); calc = ltr(`3 · ${r.a} − 2 · ${r.b} = ${r.value}`); }
          t += `<tr${r.n === n ? ' class="br-top"' : ""}><td>${ltr(r.n)}</td><td>${ltr(bin(r.n))}</td><td>${rule}</td><td>${calc}</td><td><strong>${ltr(r.value)}</strong></td></tr>`;
        });
        return t + `</tbody></table>`;
      };
      const note = (n, s, L) => {
        if (s.j === 0) {
          return `מתחילים מ-${ltr(`m = n = ${n}`)}. בכל צעד הביט האחרון של ${ltr("m")} עובר לראש של ${ltr("f(n)")}${NB}: ` +
            `${ltr(`f(2m + c) = f(m) + c · ${sup("ℓ(m)")}`)}, כש-${ltr("ℓ(m)")} הוא מספר הביטים של ${ltr("m")}.`;
        }
        if (s.j === L) {
          return `נשאר ${ltr("m = 1")}, ו-${ltr("f(1) = 1")}${NB}: הביט העליון של ${ltr(n)} הוא הביט הנמוך של ${ltr("f(n)")}. ` +
            `כל ${ltr(L)} הביטים עברו, ו-${ltr(`f(${n}) = ${s.acc}`)}.`;
        }
        const prev = Math.floor(n / 2 ** (s.j - 1)), c = prev % 2, ell = L - s.j;
        return `מורידים את הביט האחרון${NB}: ${ltr(`${prev} = 2 · ${s.m} + ${c}`)}, ולכן ${ltr(`f(${prev}) = f(${s.m}) + ${c} · ${sup(ell)}`)}. ` +
          (c ? `הביט 1 עובר למקום ${ltr(sup(ell))} של ${ltr("f(n)")}.` : `הביט 0 לא מוסיף כלום, ותופס את המקום ${ltr(sup(ell))}.`);
      };
      const draw = () => {
        const n = st.n, L = len(n), S = brSteps(n), N = S.length - 1;
        st.k = Math.min(st.k, N);
        const s = S[st.k], R = brReverse(n), nb = bin(n);
        if (document.activeElement !== input) input.value = String(n);
        $(".ex-pos").textContent = `צעד ${st.k} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === N;
        $(".br-dec").disabled = n <= 1;
        $(".br-inc").disabled = n >= MAX;
        $(".br-pal").disabled = !brNextPal(n);
        $(".br-sum").innerHTML = `המספר ${ltr(`n = ${n}`)}, ובבינארי ${ltr(nb)}${NB}: ${ltr(L)} ביטים.`;
        // the row of n: the bits already moved dashed; the row of f(n): the places filled so far
        let top = "", low = "";
        for (let c = 0; c < L; c++) {
          const p = L - 1 - c;                      // the bit of n in column c is b_p
          top += cell(nb[c], p < s.j ? " is-lead" : "");
          const filled = s.j === L ? true : c < s.j, fresh = s.j === L ? c === L - 1 : c === s.j - 1;
          const bit = filled ? nb[L - 1 - c] : "·";
          low += cell(bit, (filled ? "" : " is-lead") + (fresh ? (bit === "1" ? " is-mark" : " br-mark") : ""));
        }
        $(".gs-bits tbody").innerHTML = `<tr><th>n</th>${top}</tr><tr><th>f(n)</th>${low}</tr>`;
        $(".br-now").innerHTML = s.j === L ? `עכשיו${NB}: ${ltr(`f(${n}) = ${s.acc}`)}, וכל הביטים במקומם.` :
          `עכשיו${NB}: ${ltr(`f(${n}) = ${s.acc} + f(${s.m})`)}, עם ${ltr(`m = ${s.m} = ${bin(s.m)}`)} שעוד לא עבר.`;
        $(".br-note").innerHTML = note(n, s, L);
        $(".br-rules-title").innerHTML = `הכללים בדרך ל-${ltr(`f(${n})`)}, מהקטן לגדול${NB}: ${ltr(brRules(n).length)} ערכים`;
        if (box.dvqRulesOf !== n) { $(".br-rules").innerHTML = rulesTable(n); box.dvqRulesOf = n; }
        if (st.k === N) {
          answer(box, `התוצאה${NB}: ${ltr(`f(${n}) = ${R}`)}, ובבינארי ${ltr(bin(R))}. ` + (R === n ? `זה פלינדרום, ולכן ${ltr(`f(n) = n`)}.` : `זה לא פלינדרום, ולכן ${ltr(`f(n) ≠ n`)}.`));
        } else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= len(st.n), restart: () => { st.k = 0; draw(); } });
      const set = (x) => { stop(); st.n = x; st.k = 0; $(".br-err").textContent = ""; input.value = String(x); draw(); };
      input.addEventListener("change", () => {
        const x = Number(input.value);
        if (!Number.isInteger(x) || x < 1 || x > MAX) { $(".br-err").textContent = `מספר שלם מ-1 עד ${MAX}`; input.value = String(st.n); return; }
        set(x);
      });
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      // a button moves n through the field, so the link and the remembered state follow it
      const move = (x) => { input.value = String(x); input.dispatchEvent(new Event("input", { bubbles: true })); input.dispatchEvent(new Event("change", { bubbles: true })); };
      $(".br-dec").addEventListener("click", () => { if (st.n > 1) move(st.n - 1); });
      $(".br-inc").addEventListener("click", () => { if (st.n < MAX) move(st.n + 1); });
      $(".br-pal").addEventListener("click", () => { const v = brNextPal(st.n); if (v) move(v); });
      $(".ex-reset").addEventListener("click", () => move(N0));
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(0, st.k - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = len(st.n); draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { bitrev: bitrevView },
    help: {
      bitrev: "מקלידים n, מזיזים אותו ב-1 או קופצים לפלינדרום הבא. הצעדים מעבירים את הביטים של n, מהנמוך, לראש של f(n), כמו בפיתוח של סעיף ב, והטבלה מתחת מראה את כל הערכים שהכללים צריכים בדרך ל-f(n), כמו בסעיף א.",
    },
    models: { brValue, brReverse, brIsPal, brNextPal, brRules, brSteps },
  });
})();
