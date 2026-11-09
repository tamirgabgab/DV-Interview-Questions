// kinds: rotatek
//   rotatek                0072        an array of n rotated left by k in place, stepped: the three reversals swap by swap (the reversed range framed), or the cycles of the rotation move by move (the cells tinted by their cycle, tmp beside the array); the swaps, the moves and the memory accesses counted
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const gcd = (x, y) => (y ? gcd(y, x % y) : x);

  // The cycles of the rotation: from every start s, s <- s + k <- s + 2k ... (mod n).
  const rkCycles = (n, k) => {
    k %= n;
    const seen = new Set(), out = [];
    for (let s = 0; s < n; s++) {
      if (seen.has(s)) continue;
      const cyc = [];
      let i = s;
      do { cyc.push(i); seen.add(i); i = (i + k) % n; } while (i !== s);
      out.push(cyc);
    }
    return out;
  };
  // The frames of the three reversals, as the page's code runs them: the array after every
  // swap, the two entries swapped and the range being reversed.
  const rkReversalSteps = (n, k) => {
    const arr = Array.from({ length: n }, (_, i) => i), frames = [{ arr: arr.slice(), swap: null, range: null, phase: 0 }];
    k %= n;
    if (k === 0) return frames;
    [[0, k], [k, n], [0, n]].forEach(([lo, hi], p) => {
      for (let a = lo, b = hi - 1; a < b; a++, b--) {
        [arr[a], arr[b]] = [arr[b], arr[a]];
        frames.push({ arr: arr.slice(), swap: [a, b], range: [lo, hi], phase: p + 1 });
      }
    });
    return frames;
  };
  // The frames of the cycles: save a[s] in tmp, pull a[i] <- a[i + k] along the cycle, and
  // close it with tmp; every frame is one assignment.
  const rkCycleSteps = (n, k) => {
    const arr = Array.from({ length: n }, (_, i) => i), frames = [{ arr: arr.slice(), tmp: null, act: null }];
    k %= n;
    if (k === 0) return frames;
    const g = gcd(n, k);
    for (let s = 0; s < g; s++) {
      let tmp = arr[s], i = s;
      frames.push({ arr: arr.slice(), tmp, act: "save", at: s, cyc: s });
      for (;;) {
        const j = i + k >= n ? i + k - n : i + k;
        if (j === s) break;
        arr[i] = arr[j];
        frames.push({ arr: arr.slice(), tmp, act: "pull", at: i, from: j, cyc: s });
        i = j;
      }
      arr[i] = tmp;
      frames.push({ arr: arr.slice(), tmp: null, act: "close", at: i, cyc: s });
    }
    return frames;
  };

  const METHODS = { rev: "שלושה היפוכים (סעיף א)", cyc: "מעגלים (סעיף ב)" };
  const PHASE = ["", "היפוך של A", "היפוך של B", "היפוך של הכול"];

  const rotatekView = () => ({
    mount(box) {
      const d0 = { method: METHODS[box.dataset.method] ? box.dataset.method : "rev", n: Number(box.dataset.n || 7), k: Number(box.dataset.k || 3) };
      const st = { ...d0, s: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>השיטה <select class="rk-method" aria-label="השיטה">${Object.entries(METHODS).map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<label><span>${ltr("n")}</span><input type="range" class="rk-n" min="2" max="16" step="1" dir="ltr" aria-label="אורך המערך"><output class="rk-no"></output></label>` +
        `<label><span>${ltr("k")}</span><input type="range" class="rk-k" min="0" max="15" step="1" dir="ltr" aria-label="בכמה מקומות מסובבים"><output class="rk-ko"></output></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">מההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary rk-sum" aria-live="polite"></p>` +
        `<div class="rk-fig" data-steady></div>` +
        `<span class="viz-legend rk-legend"></span>` +
        `<p class="rk-note"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const frames = () => (st.method === "rev" ? rkReversalSteps(st.n, st.k) : rkCycleSteps(st.n, st.k));
      const cycOf = () => { const m = new Map(); rkCycles(st.n, st.k).forEach((c, ci) => c.forEach((i) => m.set(i, ci))); return m; };
      const td = (text, cls) => `<td class="pm-c${cls ? ` ${cls}` : ""}">${text}</td>`;

      const draw = () => {
        const fr = frames(), T = fr.length - 1;
        st.s = Math.min(Math.max(st.s, 0), T);
        const f = fr[st.s], rev = st.method === "rev", k = st.k % st.n, g = k ? gcd(st.n, k) : st.n;
        $(".rk-method").value = st.method;
        $(".rk-n").value = String(st.n); $(".rk-no").textContent = String(st.n);
        $(".rk-k").max = String(st.n - 1); $(".rk-k").value = String(st.k); $(".rk-ko").textContent = String(st.k);
        $(".ex-pos").textContent = `צעד ${st.s} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.s === T;
        const cyc = cycOf();
        // the array: a cell per entry, the value its old index; tinted by the part it came from
        // (A or B) for the reversals and by its cycle for the cycles; the cells of the step framed
        const tint = (v) => (rev ? (v < k ? "c1" : "c2") : `c${(cyc.get(v) % 5) + 1}`);
        const hl = (i) => (rev ? f.swap && f.swap.includes(i) : f.act && (i === f.at || i === f.from));
        const inRange = (i) => rev && f.range && i >= f.range[0] && i < f.range[1];
        const want = Array.from({ length: st.n }, (_, i) => (i + k) % st.n);
        let t = `<div class="pm-scroll" tabindex="0" role="region" aria-label="המערך בצעד ${st.s}"><table class="pm-cells rk-cells" dir="ltr"><tbody>` +
          `<tr class="pm-head"><th></th>${f.arr.map((_, i) => `<td>${i}</td>`).join("")}${rev ? "" : "<td></td>"}</tr>` +
          `<tr><th>a</th>${f.arr.map((v, i) => td(v, `${tint(v)}${hl(i) ? " is-hl" : ""}${inRange(i) ? " is-in" : ""}`)).join("")}` +
          (rev ? "" : td(f.tmp === null ? "·" : f.tmp, `rk-tmp${f.tmp === null ? "" : ` ${tint(f.tmp)}`}`)) + `</tr>` +
          `<tr class="rk-want"><th>היעד</th>${want.map((v) => td(v, f.arr[want.indexOf(v)] === v ? "is-done" : "")).join("")}${rev ? "" : `<td class="rk-tmplab">tmp</td>`}</tr>` +
          `</tbody></table></div>`;
        $(".rk-fig").innerHTML = t;
        $(".rk-legend").innerHTML = rev
          ? `<span><i class="pm-key-c1"></i>${ltr("A")}, ‏${ltr("k")} הראשונים</span><span><i class="pm-key-c2"></i>${ltr("B")}, השאר</span><span><i class="pm-key-hl"></i>ההחלפה של הצעד</span>`
          : `${Array.from({ length: Math.min(g, 5) }, (_, c) => `<span><i class="pm-key-c${c + 1}"></i>מעגל ${c + 1}${g > 5 && c === 4 ? " ואילך" : ""}</span>`).join("")}<span><i class="pm-key-hl"></i>ההשמה של הצעד</span>`;
        // the counts: the swaps or the assignments so far, and the memory accesses
        const done = st.s === T;
        if (rev) {
          const swaps = st.s;
          $(".rk-sum").innerHTML = `${ltr(`n = ${st.n}, k = ${st.k}`)}${NB}: ${ltr(`⌊${k}/2⌋ + ⌊${st.n - k}/2⌋ + ⌊${st.n}/2⌋ = ${T}`)} החלפות. ` +
            `עד עכשיו ${ltr(swaps)} החלפות, ${ltr(4 * swaps)} גישות לזיכרון (שתי קריאות ושתי כתיבות לכל החלפה).`;
          $(".rk-note").innerHTML = !f.swap
            ? (k ? `הסיבוב הוא ${ltr("AB → BA")}. הופכים את ${ltr("A")}, את ${ltr("B")}, ואז את הכול.` : `${ltr("k mod n = 0")}${NB}: אין מה לסובב.`)
            : `${PHASE[f.phase]}${NB}: מחליפים את ${ltr(`a[${f.swap[0]}]`)} ו-${ltr(`a[${f.swap[1]}]`)}, מהקצוות פנימה.` + (done ? ` <b>המערך מסובב.</b>` : "");
        } else {
          const writes = fr.slice(1, st.s + 1).filter((x) => x.act !== "save").length;
          $(".rk-sum").innerHTML = `${ltr(`g = gcd(${st.n}, ${k}) = ${g}`)} מעגלים, כל אחד באורך ${ltr(st.n / g)}. ` +
            `עד עכשיו ${ltr(writes)} כתיבות ו-${ltr(writes)} קריאות${NB}: כל תא נקרא פעם אחת ונכתב פעם אחת, ${ltr(2 * st.n)} גישות בסוף.`;
          $(".rk-note").innerHTML = !f.act
            ? (k ? `האיבר שיגיע למקום ${ltr("i")} נמצא עכשיו ב-${ltr(`i + ${k}`)}. כל מעגל מתחיל במקום ${ltr("s < g")}.` : `${ltr("k mod n = 0")}${NB}: אין מה לסובב.`)
            : f.act === "save" ? `מעגל ${f.cyc + 1}${NB}: שומרים את ${ltr(`a[${f.at}]`)} ב-${ltr("tmp")}.`
            : f.act === "pull" ? `${ltr(`a[${f.at}] ← a[${f.from}]`)}${NB}: מושכים את הערך ממקום ${ltr(`${f.at} + ${k}`)}${f.at + k >= st.n ? ` (מודולו ${ltr(st.n)})` : ""}.`
            : `המקום הבא הוא שוב ${ltr(f.cyc)}, ולכן ${ltr(`a[${f.at}] ← tmp`)} סוגר את המעגל.` + (done ? ` <b>המערך מסובב.</b>` : "");
        }
        if (done && k) answer(box, `${ltr(`[${f.arr.join(", ")}]`)}${NB}: כל ערך ${ltr("v")} עבר למקום ${ltr(`v − ${k}`)} (מודולו ${ltr(st.n)}).`, ".rk-cells .is-hl");
        else answer(box, null);
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.s++; draw(); }, done: () => st.s >= frames().length - 1, restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; draw(); };
      $(".rk-method").addEventListener("change", () => { st.method = $(".rk-method").value; restart(); });
      $(".rk-n").addEventListener("input", () => { st.n = Number($(".rk-n").value); st.k = Math.min(st.k, st.n - 1); restart(); });
      $(".rk-k").addEventListener("input", () => { st.k = Number($(".rk-k").value); restart(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = frames().length - 1; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, d0); restart(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { rotatek: rotatekView },
    help: {
      rotatek: "בוחרים שיטה, אורך n ו-k. בשלושה היפוכים כל צעד הוא החלפה אחת, והקטע שמתהפך מסומן. במעגלים כל צעד הוא השמה אחת : שומרים ב-tmp, מושכים לאורך המעגל וסוגרים. השורה התחתונה היא המערך שצריך להגיע אליו, והתאים שכבר במקומם מסומנים.",
    },
    models: { rkCycles, rkReversalSteps, rkCycleSteps },
  });
})();
