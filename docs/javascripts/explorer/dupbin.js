// kinds: dupbin
//   dupbin                 0017        solution 3, binary search on the values: the count of numbers ≤ v for every v against the line y = v, lo and hi narrowing with the invariant, the counted cells of the array lit
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { autoplay, f, floydParse, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";

  // The page's find_duplicate_binary step by step: each frame holds lo, hi, mid, the count
  // of values <= mid and which half the duplicate is in; the answer is lo at the end.
  const dupBinarySearch = (nums) => {
    let lo = 1, hi = nums.length - 1;
    const frames = [];
    while (lo < hi) {
      const mid = Math.floor((lo + hi) / 2), count = nums.filter((v) => v <= mid).length, low = count > mid;
      frames.push({ lo, hi, mid, count, low });
      if (low) hi = mid; else lo = mid + 1;
    }
    return { frames, answer: lo };
  };
  // c(v): how many values are <= v, for v = 0..n
  const dupCounts = (nums) => Array.from({ length: nums.length }, (_, v) => nums.filter((u) => u <= v).length);
  // a random input like the page's test: 1..n, one value copied over another, shuffled
  const dupRandom = (n, rnd) => {
    const nums = Array.from({ length: n }, (_, i) => i + 1);
    const v = 1 + Math.floor(rnd() * n);
    nums[Math.floor(rnd() * n)] = v;
    nums.push(v);
    for (let i = nums.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [nums[i], nums[j]] = [nums[j], nums[i]]; }
    return nums;
  };

  // The binary search box (0017 solution 3): the array as a row of cells (those <= mid lit
  // at the current step), a chart of c(v) for v = 1..n against the line y = v with the
  // range lo..hi shaded and mid marked, and a line per step with the decision and the
  // invariant c(lo − 1) <= lo − 1, c(hi) > hi.
  const EXAMPLE = [3, 9, 5, 6, 7, 8, 1, 1, 2, 4];
  const dupbinView = () => ({
    mount(box) {
      const nmax = Number(box.dataset.nmax || 12);
      const st = { nums: EXAMPLE, k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏n</span><input type="range" class="ex-n" min="3" max="${nmax}" step="1" value="${EXAMPLE.length - 1}" dir="ltr" aria-label="n, מספר הערכים"><output class="out-n"></output></label>` +
        `<button type="button" class="md-button md-button--primary ex-shuffle">הגרלה</button>` +
        `<button type="button" class="md-button ex-example">הדוגמה מהדף</button>` +
        `<label class="fl-input"><span>המערך</span><input type="text" class="ex-nums" dir="ltr" spellcheck="false" aria-label="המערך, מספרים מופרדים בפסיקים"></label>` +
        `<button type="button" class="md-button ex-apply">החלה</button><span class="fl-err" aria-live="polite"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1000, 400) +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<div class="db-cells" dir="ltr"></div>` +
        `<p class="ex-title">כמה מספרים במערך הם לכל היותר v, לכל ערך v, מול הקו y = v</p><div class="db-chart"></div>` +
        `<span class="viz-legend"><span><i class="db-key-range"></i>הטווח lo עד hi</span><span><i class="db-key-mid"></i>‏mid והספירה שלו</span><span><i class="db-key-line"></i>הקו y = v</span></span>` +
        `<p class="wv-step db-step" aria-live="polite"></p><p class="ex-summary db-inv"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const numsIn = $(".ex-nums");
      const run = () => dupBinarySearch(st.nums);
      const state = () => {                     // lo, hi and the frame shown at step k
        const r = run(), fr = r.frames[st.k] || null;
        return fr ? { lo: fr.lo, hi: fr.hi, fr, r } : { lo: r.answer, hi: r.answer, fr: null, r };
      };
      const chart = (s) => {
        const n = st.nums.length - 1, c = dupCounts(st.nums);
        const W = 640, X0 = 44, X1 = 620, Y0 = 16, Y1 = 206, top = n + 1;
        const bw = (X1 - X0) / n, X = (v) => X0 + (v - 0.5) * bw, Y = (y) => Y1 - (y / top) * (Y1 - Y0);
        let g = `<svg class="perf-chart db-svg" viewBox="0 0 ${W} 236" role="img" aria-label="הספירה של כל ערך מול הקו y = v, הטווח מ-${s.lo} עד ${s.hi}">`;
        for (let y = 0; y <= top; y += top > 8 ? 2 : 1) g += `<line class="grid" x1="${X0}" x2="${X1}" y1="${f(Y(y))}" y2="${f(Y(y))}"/><text class="tick" x="${X0 - 6}" y="${f(Y(y) + 4)}" text-anchor="end">${y}</text>`;
        g += `<rect class="db-range" x="${f(X(s.lo) - bw / 2)}" y="${Y0}" width="${f(bw * (s.hi - s.lo + 1))}" height="${Y1 - Y0}"/>`;
        for (let v = 1; v <= n; v++) {
          const mid = s.fr && v === s.fr.mid, out = v < s.lo || v > s.hi, over = c[v] > v;
          g += `<rect class="db-bar${mid ? " is-mid" : ""}${out ? " is-out" : ""}" x="${f(X(v) - bw * 0.32)}" y="${f(Y(c[v]))}" width="${f(bw * 0.64)}" height="${f(Y1 - Y(c[v]))}"><title>${v} : ${c[v]} מספרים לכל היותר ${v}${over ? `, יותר מ-${v}` : ""}</title></rect>` +
               `<text class="tick" x="${f(X(v))}" y="${f(Y(c[v]) - 4)}" text-anchor="middle">${c[v]}</text>` +
               `<text class="tick" x="${f(X(v))}" y="${Y1 + 16}" text-anchor="middle">${v}</text>`;
        }
        g += `<line class="db-line" x1="${f(X(0.5))}" y1="${f(Y(0.5))}" x2="${f(X(n + 0.5))}" y2="${f(Y(n + 0.5))}"/>`;
        g += `<line class="axis" x1="${X0}" x2="${X1}" y1="${Y1}" y2="${Y1}"/>`;
        return g + `<text class="tick" x="${X1}" y="${Y1 + 30}" text-anchor="end">v</text></svg>`;
      };
      const draw = () => {
        const s = state(), { r, fr } = s, n = st.nums.length - 1, c = dupCounts(st.nums);
        st.k = Math.min(st.k, r.frames.length);
        $(".out-n").textContent = String(n);
        if (document.activeElement !== numsIn) numsIn.value = st.nums.join(", ");
        $(".db-cells").innerHTML = `<div class="box-grid fl-grid" style="grid-template-columns: repeat(${n + 1}, minmax(0, 1fr))">` +
          st.nums.map((v, i) => `<span class="${fr && v <= fr.mid ? "is-counted" : !fr && v === r.answer ? "hl" : ""}"><small>${i}</small><b>${v}</b></span>`).join("") + `</div>`;
        $(".db-chart").innerHTML = chart(s);
        $(".ex-pos").textContent = `צעד ${st.k} מתוך ${r.frames.length}`;
        $(".db-step").innerHTML = fr
          ? `הטווח ${ltr(`lo = ${fr.lo}`)} עד ${ltr(`hi = ${fr.hi}`)}, ולכן ${ltr(`mid = ${fr.mid}`)}. במערך ${ltr(fr.count)} מספרים הם לכל היותר ${ltr(fr.mid)} (המודגשים). ` +
            (fr.low ? `‏${ltr(`${fr.count} > ${fr.mid}`)}${NB}: יותר מספרים מערכים, ולפי שובך היונים יש כפול בין 1 ל-${ltr(fr.mid)}, ולכן ${ltr(`hi = ${fr.mid}`)}.`
                    : `‏${ltr(`${fr.count} ≤ ${fr.mid}`)}${NB}: אין עודף עד ${ltr(fr.mid)}, ולכן הכפול גדול ממנו, ו-${ltr(`lo = ${fr.mid + 1}`)}.`)
          : `‏${ltr(`lo = hi = ${r.answer}`)}${NB}: <b>הכפול הוא ${ltr(r.answer)}</b>, אחרי ${ltr(r.frames.length)} צעדים, וכל צעד ספר את כל ${ltr(n + 1)} המספרים.`;
        const lo1 = s.lo - 1;
        $(".db-inv").innerHTML = `השמורה${NB}: מתחת לטווח אין עודף, ${ltr(`c(${lo1}) = ${c[lo1]} ≤ ${lo1}`)} ✓; עד סוף הטווח יש עודף, ${ltr(`c(${s.hi}) = ${c[s.hi]} > ${s.hi}`)} ✓.` +
          (fr ? "" : ` לכן ${ltr(r.answer)} מופיע לפחות פעמיים.`);
        $(".ex-prev").disabled = st.k === 0;
        $(".ex-next").disabled = st.k >= r.frames.length;
      };
      const setNums = (nums) => { stop(); st.nums = nums; st.k = 0; $(".ex-n").value = nums.length - 1; $(".fl-err").textContent = ""; draw(); };
      let stop = () => {};
      const seed = seedControls(box, $(".ex-shuffle"), (rng) => setNums(dupRandom(Number($(".ex-n").value), rng)));
      $(".ex-shuffle").addEventListener("click", () => seed.draw());
      $(".ex-n").addEventListener("input", () => { $(".out-n").textContent = $(".ex-n").value; seed.draw(); });
      $(".ex-example").addEventListener("click", () => setNums(EXAMPLE));
      const apply = () => {
        const nums = floydParse(numsIn.value);
        if (!nums || nums.length - 1 > nmax) { $(".fl-err").textContent = `‏n + 1 מספרים מ-1 עד n, ‏n עד ${nmax}`; return; }
        setNums(nums);
      };
      $(".ex-apply").addEventListener("click", apply);
      numsIn.addEventListener("keydown", (e) => { if (e.key === "Enter") apply(); });
      $(".ex-next").addEventListener("click", () => { stop(); st.k++; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.k > 0) { st.k--; draw(); } });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = run().frames.length; draw(); });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= run().frames.length, restart: () => { st.k = 0; draw(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { dupbin: dupbinView },
    help: {
      dupbin: "״הצעד הבא״ ו״הפעלה״ מריצים את החיפוש הבינארי של פתרון 3 : בכל צעד מודגשים במערך המספרים שלכל היותר mid, העמודה של mid בתרשים מראה את הספירה מול הקו y = v, והטווח lo עד hi מצטמצם. ״הגרלה״, ‏n והשדה קובעים את המערך.",
    },
    models: { dupBinarySearch, dupCounts },
  });
})();
