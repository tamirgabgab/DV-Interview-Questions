// kinds: onesk
//   onesk                  0061        a vector of bits (or letters on a bus) and k: the sliding window step by step, the right end one cell per step, the zeros (or the cells that are not the most frequent value) counted, the left end moved one cell per step while they are more than k (a frame per left++), the total moves of the left end, the best window so far outlined and the answer at the end
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, explain, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMAX = 40;

  // Part a as the page's longest_ones plays it: a frame per right end, with the zeros in
  // the window, how far the left end moved, the best length so far and its window.
  const okTraceBits = (bits, k) => {
    const frames = [];
    let left = 0, zeros = 0, best = 0, win = null;
    bits.forEach((b, right) => {
      if (!b) zeros++;
      let moved = 0;
      while (zeros > k) { if (!bits[left]) zeros--; left++; moved++; }
      if (right - left + 1 > best) { best = right - left + 1; win = [left, right]; }
      frames.push({ right, left, zeros, moved, best, win });
    });
    return frames;
  };
  // Part b as the page's longest_same: a counter per value in the window, the most
  // frequent value (the first in the window on a tie) and the cells that are not it.
  const okTraceSame = (values, k) => {
    const frames = [], count = {};
    let left = 0, best = 0, win = null;
    const most = () => Math.max(0, ...Object.values(count));
    values.forEach((v, right) => {
      count[v] = (count[v] || 0) + 1;
      let moved = 0;
      while (right - left + 1 - most() > k) { count[values[left]]--; left++; moved++; }
      if (right - left + 1 > best) { best = right - left + 1; win = [left, right]; }
      const m = most(), top = values.slice(left, right + 1).find((c) => count[c] === m);
      frames.push({ right, left, count: { ...count }, most: m, top, moved, best, win });
    });
    return frames;
  };

  const parseBits = (text) => { const t = String(text).replace(/[\s,]+/g, ""); return new RegExp(`^[01]{1,${NMAX}}$`).test(t) ? [...t].map(Number) : null; };
  const parseVals = (text) => { const t = String(text).toUpperCase().replace(/[\s,]+/g, ""); return new RegExp(`^[A-Z]{1,${NMAX}}$`).test(t) ? [...t] : null; };

  // The box: the sequence as a strip of cells, left to right; a step moves the right end
  // one cell, or the left end one cell while the window is not valid (the cells it passed
  // in this right step struck out), the window is tinted, the cells to flip (or replace) in orange, the best
  // window so far outlined, and the right end underlined. Under it the step in words, and
  // with values the counters of the window.
  const MODES = { bits: "ביטים (סעיף א)", values: "ערכים על ה-bus (סעיף ב)" };
  // the solution's steps, as chips of the explanation panel, and a variable's change
  const STEPS = {
    bits: ["הקצה הימני מתקדם", "יותר מ-k אפסים : השמאלי מתקדם", "הטוב עד עכשיו", "הסוף : הטוב הוא התשובה"],
    values: ["הקצה הימני מתקדם, והמונה שלו גדל", "יותר מ-k להחלפה : השמאלי מתקדם", "הטוב עד עכשיו", "הסוף : הטוב הוא התשובה"],
  };
  const V = (name, before, after) => ltr(before === after ? `${name} = ${after}` : `${name} : ${before} → ${after}`);
  const onesView = () => ({
    mount(box) {
      const d0 = { mode: box.dataset.mode === "values" ? "values" : "bits", bits: box.dataset.bits || "11100011110", values: box.dataset.values || "AAABBCBABA", k: Number(box.dataset.k) || 2 };
      const seqOf = (mode) => (mode === "bits" ? parseBits(d0.bits) || [1, 0, 1] : parseVals(d0.values) || ["A", "B", "A"]);
      const st = { mode: d0.mode, seq: seqOf(d0.mode), k: d0.k, s: 0, n: 16 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הרצף <select class="ok-mode" aria-label="ביטים או ערכים">${Object.entries(MODES).map(([v, w]) => `<option value="${v}"${v === st.mode ? " selected" : ""}>${w}</option>`).join("")}</select></label>` +
        `<label><span>הערכים</span><input type="text" class="ex-num ok-seq" dir="ltr" spellcheck="false" aria-label="הרצף, עד ${NMAX} תאים : ספרות 0 ו-1, או אותיות"></label>` +
        `<label><span class="ok-klab">היפוכים (k)</span> <input type="number" class="ex-num ok-k" min="0" max="${NMAX}" step="1" dir="ltr" aria-label="כמה תאים מותר להפוך או להחליף"></label>` +
        `<label>בהגרלה <select class="ok-n" aria-label="כמה תאים להגריל">${[10, 16, 24, 40].map((v) => `<option value="${v}"${v === 16 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ok-rand">הגרלה</button><span class="ok-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err ok-err" role="status"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 700, 300) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary ok-sum" aria-live="polite"></p>` +
        `<div class="ok-strip" role="img"></div>` +
        `<span class="viz-legend"><span><i class="ok-key-in"></i>בחלון</span><span><i class="ok-key-flip"></i>תא שצריך להפוך או להחליף</span>` +
        `<span><i class="ok-key-best"></i>החלון הטוב עד עכשיו</span><span><i class="ok-key-cur"></i>הקצה הימני</span>` +
        `<span><i class="ok-key-gone"></i>יצא משמאל בצעד הזה</span></span>` +
        `<p class="ok-note"></p><p class="ok-tally"></p><p class="ok-counts"></p>`;
      const show = explain(box, "הסבר : השלבים של הפתרון והקוד");
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const bits = () => st.mode === "bits";
      const frames = () => (bits() ? okTraceBits(st.seq, st.k) : okTraceSame(st.seq, st.k));
      // the box steps through the model's frames split at every left++ of the shrink loop:
      // a sub-step { i, j } is frame i after j of its moves (j = 0: the right end just came in)
      const subs = () => { const F = frames(), S = []; F.forEach((f, i) => { for (let j = 0; j <= f.moved; j++) S.push({ i, j }); }); return { F, S }; };
      const total = () => subs().S.length;
      // the window [L, R] as it stands: its zeros, or its counters, the most frequent value
      // (the first in the window on a tie, as the model) and the cells to replace
      const windowAt = (seq, L, R) => {
        const w = seq.slice(L, R + 1), count = {};
        w.forEach((c) => { count[c] = (count[c] || 0) + 1; });
        const most = Math.max(0, ...Object.values(count)), top = w.find((c) => count[c] === most);
        return { count, most, top, zeros: w.filter((c) => c === 0).length, bad: bits() ? w.filter((c) => c === 0).length : w.length - most };
      };
      const draw = () => {
        const seq = st.seq, n = seq.length, { F, S } = subs(), N = S.length;
        st.s = Math.min(Math.max(st.s, 0), N);
        const cur = st.s ? S[st.s - 1] : null, fr = cur ? F[cur.i] : null, done = st.s === N;
        const prevF = cur && cur.i ? F[cur.i - 1] : null;
        const moved = fr ? fr.moved : 0, last = !!fr && cur.j === moved;        // last: the window is valid again
        const from = fr ? fr.left - moved : 0, L = from + (cur ? cur.j : 0), R = fr ? fr.right : -1;
        const W = fr ? windowAt(seq, L, R) : null;
        const best = last ? fr.best : prevF ? prevF.best : 0, bestWin = last ? fr.win : prevF ? prevF.win : null;
        $(".ok-seq").value = seq.join(bits() ? "" : " "); $(".ok-k").value = String(st.k); $(".ok-mode").value = st.mode;
        $(".ok-klab").textContent = bits() ? "היפוכים (k)" : "החלפות (k)";
        $(".ex-pos").textContent = `צעד ${st.s} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        const inWin = (p) => fr && p >= L && p <= R;
        const inBest = (p) => bestWin && p >= bestWin[0] && p <= bestWin[1];
        const flip = (p) => inWin(p) && (bits() ? seq[p] === 0 : seq[p] !== W.top);
        const gone = (p) => fr && p >= from && p < L;                             // the left end passed it in this step
        const strip = $(".ok-strip");
        strip.setAttribute("aria-label", `הרצף ${seq.join(" ")}${fr ? `, החלון ${L} עד ${R}` : ""}`);
        strip.innerHTML = seq.map((v, p) => `<div class="ok-c${inWin(p) ? " is-in" : ""}${flip(p) ? " is-flip" : ""}${inBest(p) ? " is-best" : ""}${gone(p) ? " is-gone" : ""}` +
          `${fr && p === R ? " is-cur" : ""}${p > R ? " is-wait" : ""}" title="place ${p}">${v}<small>${p}</small></div>`).join("");
        const len = fr ? R - L + 1 : 0, bad = W ? W.bad : 0;
        $(".ok-sum").innerHTML = `${ltr(n)} ${bits() ? "ביטים" : "ערכים"}, ${ltr(`k = ${st.k}`)}. ` +
          (fr ? `החלון ${ltr(`${L}..${R}`)} באורך ${ltr(len)}, עם ${ltr(bad)} ${bits() ? "אפסים" : "תאים להחלפה"}${bad > st.k ? `, יותר מ-${ltr("k")}` : ""}. הטוב עד עכשיו${NB}: <b>${ltr(best)}</b>.`
            : `לוחצים על "הצעד הבא"${NB}: הקצה הימני מתקדם תא אחד בכל צעד, והשמאלי תא אחד בכל צעד שבו החלון לא חוקי.`);
        let note = "", counts = "";
        if (fr) {
          const v = seq[R], K = ltr(`k = ${st.k}`), win = ltr(`${L}..${R}`);
          const fresh = last && fr.best === len && (cur.i === 0 || F[cur.i - 1].best < fr.best) ? ` <b>אורך חדש${NB}: ${ltr(len)} ✓</b>` : "";
          const path = moved ? ` בצעד הזה הקצה השמאלי עבר ${ltr(Array.from({ length: moved + 1 }, (_, j) => from + j).join(" → "))}.` : "";
          if (cur.j === 0) {
            const what = bits() ? (v ? `האפסים בחלון נשארים ${ltr(bad)}` : `האפסים בחלון עולים ל-${ltr(bad)}`)
              : `בחלון ${win} הנפוץ מופיע ${ltr(W.most)} פעמים, ולכן ${ltr(bad)} תאים להחלפה`;
            note = `נכנס ${ltr(v)} במקום ${ltr(R)}${NB}: ${what}` +
              (moved ? `, יותר מ-${K}. החלון ${win} לא חוקי, והקצה השמאלי מתחיל לזוז, תא אחד בכל צעד.` : `, לכל היותר ${K}, והחלון ${win} חוקי.`) + fresh;
          } else {
            const out = seq[L - 1];
            const what = bits() ? (out ? `יצא ${ltr(1)}, והאפסים בחלון נשארים ${ltr(bad)}` : `יצא אפס, והאפסים בחלון יורדים ל-${ltr(bad)}`)
              : `יצא ${ltr(out)}, ועכשיו ${ltr(bad)} תאים להחלפה`;
            note = `הקצה השמאלי זז מ-${ltr(L - 1)} ל-${ltr(L)}${NB}: ${what}` +
              (last ? `, לכל היותר ${K}. החלון ${win} חוקי שוב.${path}` : `, עדיין יותר מ-${K}.`) + fresh;
          }
          if (!bits()) {
            const keys = Object.keys(W.count).sort();
            counts = `המונים של החלון${NB}: ${keys.map((c) => ltr(`${c}: ${W.count[c]}`)).join(", ")}. הנפוץ${NB}: ${ltr(W.top)} (${ltr(W.most)}), להחלפה${NB}: ${ltr(`${len} − ${W.most} = ${bad}`)}.`;
          }
        }
        $(".ok-note").innerHTML = note;
        // the amortised bound: every left++ takes a cell out of the window for good
        $(".ok-tally").innerHTML = `הקצה השמאלי זז ${L === 1 ? "פעם אחת" : `${ltr(L)} פעמים`} בסך הכול, לכל היותר ${ltr(`n = ${n}`)}${NB}: הוא רק מתקדם, ולכן כל הצעדים יחד הם לכל היותר ${ltr("2n")}.`;
        $(".ok-counts").innerHTML = counts;
        // the explanation panel: the steps of the moment, the lines they ran, the variables
        let lit = [], lines, vars;
        if (!fr) {
          lines = bits() ? { py: [3], sv: [4] } : { py: [4, 5], sv: [5] };
          vars = ltr(bits() ? "best = 0, left = 0, zeros = 0" : "best = 0, left = 0, count = {}");
        } else {
          const enter = cur.j === 0, end = last ? (bits() ? { py: [9], sv: [11] } : { py: [11], sv: [16] }) : { py: [], sv: [] };
          const fin = done ? (bits() ? { py: [10], sv: [13] } : { py: [12], sv: [18] }) : { py: [], sv: [] };
          const body = bits() ? (enter ? { py: [5, 6], sv: [6, 7] } : { py: [6, 7, 8], sv: [7, 8, 9] })
            : (enter ? { py: [7, 8], sv: [7, 8, 9, 10] } : { py: [8, 9, 10], sv: [10, 11, 12, 13, 14] });
          lit = [...(enter ? [1] : [2]), ...(last ? [3] : []), ...(done ? [4] : [])];
          lines = { py: [...body.py, ...end.py, ...fin.py], sv: [...body.sv, ...end.sv, ...fin.sv] };
          const leftBefore = enter ? (prevF ? prevF.left : 0) : L - 1;
          const zerosBefore = enter ? (prevF ? prevF.zeros : 0) : bad + (seq[L - 1] === 0 ? 1 : 0);
          const bestBefore = prevF ? prevF.best : 0;
          vars = [ltr(`right = ${R}`), V("left", leftBefore, L),
            bits() ? V("zeros", zerosBefore, bad) : ltr(`most = ${W.most}`), V("best", bestBefore, best)].join(" · ");
        }
        show({ code: bits() ? "longest_ones" : "longest_same", steps: STEPS[st.mode], lit, lines, vars });
        if (done && fr) {
          answer(box, fr.best ? `${bits() ? "רצף האחדות הארוך ביותר" : "החלון הארוך ביותר של ערך אחד"} הוא באורך ${ltr(fr.best)}${NB}: המקומות ${ltr(fr.win[0])} עד ${ltr(fr.win[1])}.` : "הרצף ריק.", ".ok-strip .is-best");
        } else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= total(), restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; $(".ok-err").textContent = ""; draw(); };
      $(".ok-mode").addEventListener("change", () => { st.mode = MODES[$(".ok-mode").value] ? $(".ok-mode").value : "bits"; st.seq = seqOf(st.mode); restart(); });
      $(".ok-seq").addEventListener("change", () => {
        const v = bits() ? parseBits($(".ok-seq").value) : parseVals($(".ok-seq").value);
        if (!v) { $(".ok-err").textContent = bits() ? `הרצף${NB}: 1 עד ${NMAX} ספרות 0 או 1` : `הרצף${NB}: 1 עד ${NMAX} אותיות לטיניות`; return; }
        st.seq = v; restart();
      });
      $(".ok-seq").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".ok-seq").blur(); });
      $(".ok-k").addEventListener("change", () => {
        const v = Math.round(Number($(".ok-k").value));
        if (!(v >= 0 && v <= NMAX)) { $(".ok-k").value = String(st.k); return; }
        st.k = v; restart();
      });
      $(".ok-n").addEventListener("change", () => { st.n = Number($(".ok-n").value); });
      const seed = seedControls(box, $(".ok-anchor"), (rng) => {
        st.seq = bits() ? Array.from({ length: st.n }, () => (rng() < 0.7 ? 1 : 0))
          : Array.from({ length: st.n }, () => { const r = rng(); return r < 0.5 ? "A" : r < 0.8 ? "B" : "C"; });
        restart();
      }, { fresh: false });
      $(".ok-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, { mode: d0.mode, seq: seqOf(d0.mode), k: d0.k, n: 16 }); $(".ok-n").value = "16"; restart(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { onesk: onesView },
    help: {
      onesk: "מקלידים רצף (ספרות 0 ו-1, או אותיות בסעיף ב) ואת k, או מגרילים רצף. כל צעד מקדם את הקצה הימני בתא אחד : התאים שבחלון צבועים, התאים שצריך להפוך או להחליף בכתום, והחלון הטוב ביותר עד עכשיו מוקף. כשיש בחלון יותר מ-k תאים כאלה, הקצה השמאלי זז תא אחד בכל צעד, עד שהחלון חוקי שוב, והתאים שיצאו מסומנים בקו אלכסוני. השורה שמתחת סופרת כמה פעמים הקצה השמאלי זז בסך הכול. בסוף התשובה היא החלון המוקף.",
    },
    models: { okTraceBits, okTraceSame },
  });
})();
