// kinds: eggs
//   eggs                   0039        k eggs and n floors: the building with the unknown range, a zoom of its floors to pick the threshold, the plan played drop by drop, drops per threshold under the worst case; a toggle for the recurrence's two bands at the next drop
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, H, TOP, W, X0, autoplay, f, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Egg drop (0039): F[e][t] is how many floors e eggs settle in t drops, capped at n
  // (the cap keeps the numbers small and changes no decision); the worst case is the
  // first t with F[k][t] >= n; the plan drops from low + F[eggs - 1][t - 1] + 1 and
  // plays against a threshold T (the egg breaks from floor T + 1).
  const eggsTable = (k, n) => {
    const F = Array.from({ length: k + 1 }, () => new Int32Array(n + 1));
    for (let e = 1; e <= k; e++) for (let t = 1; t <= n; t++) F[e][t] = Math.min(n, F[e - 1][t - 1] + 1 + F[e][t - 1]);
    return F;
  };
  const eggsDropsOf = (F, k, n) => { for (let t = 0; t <= n; t++) if (F[k][t] >= n) return t; return n; };
  const eggsDrops = (k, n) => eggsDropsOf(eggsTable(k, n), k, n);
  const eggsRunOf = (F, k, n, T) => {
    let t = eggsDropsOf(F, k, n), low = 0, high = n + 1, eggs = k;
    const drops = [];
    while (high - low > 1) {
      const fl = Math.min(low + F[eggs - 1][t - 1] + 1, high - 1), broke = fl > T;
      drops.push([fl, broke]);
      t--;
      if (broke) { high = fl; eggs--; } else low = fl;
    }
    return drops;
  };
  // The recurrence at a drop: with `eggs` eggs and `left` drops on the unknown floors
  // low + 1 .. high − 1, the plan drops from low + f(eggs − 1, left − 1) + 1. The floors
  // below are what the eggs left after a break settle in the drops left, the floors above
  // at most what all the eggs settle in them: f(e, t) = f(e − 1, t − 1) + 1 + f(e, t − 1).
  const eggsSplitAt = (F, low, high, eggs, left) => {
    const floor = Math.min(low + F[eggs - 1][left - 1] + 1, high - 1);
    return { floor, below: floor - low - 1, above: high - floor - 1, fBelow: F[eggs - 1][left - 1], fAbove: F[eggs][left - 1], f: F[eggs][left] };
  };
  const eggsRun = (k, n, T) => eggsRunOf(eggsTable(k, n), k, n, T);
  const eggsFirst = (k, n) => eggsRun(k, n, n).map((d) => d[0]);
  const eggsPerThreshold = (k, n) => { const F = eggsTable(k, n); return Array.from({ length: n + 1 }, (_, T) => eggsRunOf(F, k, n, T).length); };

  // The egg drop box (0039): k eggs and n floors, a threshold picked on the building or
  // in the zoom of the unknown floors, and the plan played drop by drop; the whole
  // building keeps the known-safe and known-breaking floors tinted, the zoom shows a
  // window of the floors still unknown one by one, and the chart counts the drops the
  // plan needs for every threshold under the worst-case line.
  const eggsView = () => ({
    mount(box) {
      const d = box.dataset;
      const KMAX = Number(d.kmax || 10), NMAX = Number(d.nmax || 1000), ZW = 30;
      const K0 = Math.min(KMAX, Number(d.k || 3)), N0 = Math.min(NMAX, Number(d.n || 100)), T0 = Math.min(N0, Number(d.t || 36));
      const st = { k: K0, n: N0, T: T0, step: 0, win: null, F: null, drops: [], worst: 0, used: [] };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>ביצים k</span><input type="range" class="ex-k" min="1" max="${KMAX}" step="1" value="${st.k}" dir="ltr" aria-label="מספר הביצים"><output class="out-k">${st.k}</output></label>` +
        `<label><span>קומות n</span><input type="number" class="ex-num eg-n" min="1" max="${NMAX}" step="1" value="${st.n}" dir="ltr" inputmode="numeric" aria-label="מספר הקומות, מ-1 עד ${NMAX}"></label>` +
        `<label><span>הסף T</span><input type="number" class="ex-num eg-t" min="0" max="${st.n}" step="1" value="${st.T}" dir="ltr" inputmode="numeric" aria-label="קומת הסף, מ-0 עד n"></label>` +
        `<button type="button" class="md-button ex-random">הגרלת סף</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err eg-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">ההטלה הבאה</button>` +
        `<button type="button" class="md-button ex-prev">ההטלה הקודמת</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 300) +
        `<button type="button" class="md-button ex-start">מההתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button><span class="ex-pos"></span>` +
        `<label><input type="checkbox" class="eg-rec" checked> הנוסחה על הבניין</label></div>` +
        `<p class="ex-summary eg-sum" aria-live="polite"></p><p class="eg-step"></p><p class="eg-rec-text"></p>` +
        `<span class="viz-legend"><span><i class="eg-key-safe"></i>ידוע שלא נשברת</span><span><i class="eg-key-broke"></i>ידוע שנשברת</span><span><i class="eg-key-unknown"></i>עוד לא ידוע</span><span><i class="eg-key-thr"></i>הסף שבחרתם</span><span><i class="eg-key-next"></i>ההטלה הבאה</span></span>` +
        `<div class="eg-box"><div class="eg-building"></div><div class="eg-zoomwrap"><p class="ex-title eg-zoomtitle"></p><div class="eg-zoom"></div>` +
        `<label class="eg-winlab"><span>חלון התקריב</span><input type="range" class="eg-win" min="1" max="1" step="1" value="1" dir="ltr" aria-label="הקומה הראשונה בחלון התקריב"></label></div></div>` +
        `<p class="ex-title">מספר ההטלות של התוכנית לכל סף אפשרי</p><div class="eg-chart"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const compute = () => {
        st.F = eggsTable(st.k, st.n);
        st.worst = eggsDropsOf(st.F, st.k, st.n);
        st.drops = eggsRunOf(st.F, st.k, st.n, st.T);
        st.used = Array.from({ length: st.n + 1 }, (_, T) => eggsRunOf(st.F, st.k, st.n, T).length);
        st.step = Math.min(st.step, st.drops.length);
      };
      // the state after `step` drops: the known range, the eggs and drops left
      const after = (step) => {
        let low = 0, high = st.n + 1, eggs = st.k;
        for (let i = 0; i < step; i++) { const [fl, broke] = st.drops[i]; if (broke) { high = fl; eggs--; } else low = fl; }
        return { low, high, eggs, left: st.worst - step };
      };
      const clampWin = (s) => { const { low, high } = after(st.step); const len = Math.min(ZW, high - low - 1); return Math.max(low + 1, Math.min(s, high - len)); };
      const building = (s) => {
        const W = 150, H = 380, X0 = 44, X1 = 112, TOP = 18, BOT = 362, n = st.n;
        const pitch = (BOT - TOP) / n, y = (fl) => BOT - fl * pitch;
        const next = st.step < st.drops.length ? st.drops[st.step][0] : null;
        const len = Math.min(ZW, s.high - s.low - 1), w0 = st.win, w1 = st.win + len - 1;
        let h = `<svg class="figure eg-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="הבניין : ${n} קומות, הקומות הידועות צבועות והטווח הלא ידוע ביניהן">` +
          `<rect class="eg-wall" x="${X0}" y="${TOP}" width="${X1 - X0}" height="${BOT - TOP}" rx="3"/>` +
          `<rect class="eg-safe" x="${X0 + 1}" y="${f(y(s.low))}" width="${X1 - X0 - 2}" height="${f(BOT - y(s.low))}"/>` +
          `<rect class="eg-broke" x="${X0 + 1}" y="${TOP + 1}" width="${X1 - X0 - 2}" height="${f(Math.max(0, y(s.high - 1) - TOP - 1))}"/>`;
        if (s.high - s.low > 1) h += `<rect class="eg-win" x="${X0 - 3}" y="${f(y(w1))}" width="${X1 - X0 + 6}" height="${f(y(w0 - 1) - y(w1))}"/>`;
        const every = n <= 20 ? 1 : n <= 100 ? 10 : n <= 400 ? 50 : 100;
        for (let fl = every; fl < n; fl += every) h += `<line class="eg-floor" x1="${X0}" x2="${X1}" y1="${f(y(fl))}" y2="${f(y(fl))}"/><text class="eg-tick" x="${X0 - 4}" y="${f(y(fl) + 3)}" text-anchor="end">${fl}</text>`;
        h += `<text class="eg-tick" x="${X0 - 4}" y="${BOT + 3}" text-anchor="end">0</text><text class="eg-tick" x="${X0 - 4}" y="${TOP + 3}" text-anchor="end">${n}</text>`;
        h += `<line class="eg-thr" x1="${X0 - 2}" x2="${X1 + 2}" y1="${f(y(st.T))}" y2="${f(y(st.T))}"/>`;
        st.drops.slice(0, st.step).forEach(([fl, broke], i) => {
          h += `<g class="eg-drop ${broke ? "is-broke" : "is-safe"}"><circle cx="${X1 + 16}" cy="${f(y(fl))}" r="7"/><text x="${X1 + 16}" y="${f(y(fl) + 3)}" text-anchor="middle">${i + 1}</text><title>הטלה ${i + 1} מקומה ${fl} : ${broke ? "נשברה" : "לא נשברה"}</title></g>`;
        });
        if (next !== null) h += `<line class="eg-next" x1="${X0}" x2="${X1 + 8}" y1="${f(y(next))}" y2="${f(y(next))}"/><text class="eg-nextlbl" x="${X1 + 28}" y="${f(y(next) + 3)}">${next}</text>`;
        if (next !== null && $(".eg-rec").checked) {
          // the next drop's split: the band below it (what the eggs left after a break
          // settle) and the band above (what all of them settle), beside the building
          const sp = eggsSplitAt(st.F, s.low, s.high, s.eggs, s.left), bx = X0 - 34;
          if (sp.below > 0) h += `<rect class="eg-band-below" x="${bx}" y="${f(y(sp.floor - 1))}" width="7" height="${f(y(s.low) - y(sp.floor - 1))}"><title>מתחת להטלה : ${sp.below} קומות</title></rect>`;
          if (sp.above > 0) h += `<rect class="eg-band-above" x="${bx}" y="${f(y(s.high - 1))}" width="7" height="${f(y(sp.floor) - y(s.high - 1))}"><title>מעל ההטלה : ${sp.above} קומות</title></rect>`;
          h += `<line class="eg-next" x1="${bx}" x2="${X0}" y1="${f(y(sp.floor))}" y2="${f(y(sp.floor))}"/>`;
        }
        h += `<rect class="eg-hit" x="${X0}" y="${TOP}" width="${X1 - X0}" height="${BOT - TOP}"/></svg>`;
        return h;
      };
      const zoom = (s) => {
        const unknown = s.high - s.low - 1;
        if (unknown <= 0) return `<p class="ex-note">אין קומות לא ידועות : הסף נמצא.</p>`;
        const len = Math.min(ZW, unknown), w0 = st.win, w1 = w0 + len - 1, RH = 16, W = 250, H = len * RH + 8;
        const next = st.step < st.drops.length ? st.drops[st.step][0] : null;
        let h = `<svg class="figure eg-zoomsvg" viewBox="0 0 ${W} ${H}" role="group" aria-label="תקריב : הקומות ${w0} עד ${w1}, לחיצה על קומה קובעת את הסף">`;
        for (let i = 0; i < len; i++) {
          const fl = w1 - i, y0 = 4 + i * RH;
          const cls = (fl === st.T ? " is-thr" : "") + (fl === next ? " is-next" : "");
          h += `<g class="eg-row${cls}" data-fl="${fl}" tabindex="0" role="button">` +
               `<rect x="40" y="${y0}" width="${W - 44}" height="${RH - 2}" rx="2"/><text class="eg-rownum" x="34" y="${y0 + RH - 5}" text-anchor="end">${fl}</text>` +
               (fl === next ? `<text class="eg-rowtxt" x="${W - 10}" y="${y0 + RH - 5}" text-anchor="end">ההטלה הבאה</text>` : fl === st.T ? `<text class="eg-rowtxt" x="${W - 10}" y="${y0 + RH - 5}" text-anchor="end">הסף</text>` : "") + `</g>`;
        }
        return h + "</svg>";
      };
      const chart = () => {
        const n = st.n, t = st.worst, W = 640, H = 200, X0 = 40, R = 12, TOP = 14, BASE = 170;
        const X = (v) => X0 + (v / (n + 1)) * (W - X0 - R), Y = (v) => BASE - (v / (t + 1)) * (BASE - TOP);
        let h = `<svg class="perf-chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="מספר ההטלות לכל סף, מתחת לקו של ${t}">`;
        const ystep = t > 20 ? 10 : t > 8 ? 4 : t > 3 ? 2 : 1;
        for (let v = 0; v <= t + 1; v += ystep) h += `<line class="grid" x1="${X0}" x2="${W - R}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        const xs = n <= 10 ? Array.from({ length: n + 1 }, (_, i) => i) : [0, Math.round(n / 4), Math.round(n / 2), Math.round(3 * n / 4), n];
        xs.forEach((v) => { h += `<text class="tick" x="${f(X(v + 0.5))}" y="${BASE + 16}" text-anchor="middle">${v}</text>`; });
        h += `<line class="ink-line" x1="${X0}" x2="${W - R}" y1="${f(Y(t))}" y2="${f(Y(t))}" stroke-width="1.5" stroke-dasharray="6 4"/><text class="legend" x="${W - R - 4}" y="${f(Y(t) - 6)}" text-anchor="end">המקרה הגרוע : ${t}</text>`;
        let path = "";
        st.used.forEach((v, T) => { path += `${f(X(T))},${f(Y(v))} ${f(X(T + 1))},${f(Y(v))} `; });
        h += `<polyline class="s1-line" points="${path.trim()}" fill="none" stroke-width="2"/>`;
        h += `<rect class="eg-chart-thr" x="${f(X(st.T))}" y="${TOP}" width="${f(Math.max(2, X(1) - X(0)))}" height="${BASE - TOP}"/>`;
        h += `<circle class="s2-dot" cx="${f(X(st.T + 0.5))}" cy="${f(Y(st.used[st.T]))}" r="5"><title>הסף ${st.T} : ${st.used[st.T]} הטלות</title></circle>`;
        return h + `<line class="axis" x1="${X0}" x2="${W - R}" y1="${BASE}" y2="${BASE}"/></svg>`;
      };
      const draw = () => {
        const s = after(st.step), done = st.step === st.drops.length;
        st.win = clampWin(st.win === null ? st.T - Math.floor(ZW / 2) : st.win);
        $(".out-k").textContent = String(st.k); $(".eg-n").value = st.n; $(".eg-t").value = st.T; $(".eg-t").max = st.n;
        const win = $(".eg-win"), len = Math.min(ZW, s.high - s.low - 1);
        win.min = s.low + 1; win.max = Math.max(s.low + 1, s.high - len); win.value = st.win; win.disabled = s.high - s.low - 1 <= ZW;
        $(".eg-building").innerHTML = building(s);
        $(".eg-zoom").innerHTML = zoom(s);
        $(".eg-zoomtitle").textContent = s.high - s.low > 1 ? `תקריב : קומות ${st.win} עד ${st.win + len - 1} מתוך ${s.high - s.low - 1} הלא ידועות (${s.low + 1} עד ${s.high - 1})` : "תקריב";
        $(".eg-chart").innerHTML = chart();
        $(".ex-pos").textContent = `הטלה ${st.step} מתוך ${st.drops.length}`;
        $(".ex-prev").disabled = st.step === 0; $(".ex-next").disabled = done; $(".ex-end").disabled = done;
        const worstCount = st.used.filter((v) => v === st.worst).length;
        $(".eg-sum").innerHTML = `${ltr(st.k)} ${st.k === 1 ? "ביצה" : "ביצים"} ו-${ltr(st.n)} קומות : המקרה הגרוע הוא ${ltr(st.worst)} הטלות, ` +
          `והסף ${ltr(st.T)} דורש ${ltr(st.drops.length)}. ${worstCount === st.n + 1 ? "כל" : ltr(worstCount)} ${worstCount === 1 ? "סף אחד מגיע" : "ספים מגיעים"} למקרה הגרוע, ואף סף לא עובר אותו ✓`;
        let step;
        if (st.step === 0) step = `לפני ההטלה הראשונה : ${ltr(st.n)} קומות לא ידועות, ${ltr(st.k)} ביצים ו-${ltr(st.worst)} הטלות. ` +
          (st.drops.length ? `ההטלה הראשונה מקומה ${ltr(st.drops[0][0])} : מתחתיה ${ltr(st.drops[0][0] - 1)} קומות, בדיוק מה ש-${ltr(st.k - 1)} ${st.k - 1 === 1 ? "ביצה מספיקה לה" : "ביצים מספיקות להן"} ב-${ltr(st.worst - 1)} הטלות.` : "אין מה להטיל.");
        else {
          const [fl, broke] = st.drops[st.step - 1];
          step = `הטלה ${ltr(st.step)} מקומה ${ltr(fl)} : ` + (broke ? `<span class="wv-bad">נשברה</span>, הסף מתחת ל-${ltr(fl)}, נשארו ${ltr(s.eggs)} ${s.eggs === 1 ? "ביצה" : "ביצים"}.` : `<span class="wv-ok">לא נשברה</span>, הסף הוא ${ltr(fl)} או מעליו.`) +
            (done ? ` <b>הסתיים אחרי ${ltr(st.step)} הטלות</b> : קומה ${ltr(s.low)} בטוחה ו-${ltr(s.high)} שוברת, ולכן הסף הוא ${ltr(s.low)} ✓` :
              ` נשארו ${ltr(s.high - s.low - 1)} קומות לא ידועות (${ltr(s.low + 1)} עד ${ltr(s.high - 1)}), ${ltr(s.eggs)} ${s.eggs === 1 ? "ביצה" : "ביצים"} ו-${ltr(s.left)} הטלות; הבאה מקומה ${ltr(st.drops[st.step][0])}` +
              (s.eggs === 1 ? ` (ביצה אחרונה : קומה אחר קומה).` : `.`));
        }
        $(".eg-step").innerHTML = step;
        // the recurrence for the next drop, in words, next to the bands on the building
        if ($(".eg-rec").checked && !done) {
          const sp = eggsSplitAt(st.F, s.low, s.high, s.eggs, s.left), e = s.eggs, t = s.left;
          $(".eg-rec-text").innerHTML = `הנוסחה על הבניין : ההטלה הבאה מקומה ${ltr(sp.floor)}. מתחתיה <span class="eg-below-txt">${ltr(sp.below)} קומות</span>, ` +
            (e === 1 ? `ואין עוד ביצה אחרי שבירה, ולכן עולים קומה אחר קומה. ` :
              sp.below === sp.fBelow
                ? `בדיוק ${ltr(`f(${e - 1}, ${t - 1}) = ${sp.fBelow}`)} : מה ש-${ltr(e - 1)} ${e - 1 === 1 ? "ביצה שנשארת" : "ביצים שנשארות"} אחרי שבירה מכריעות ב-${ltr(t - 1)} ההטלות שנשארו. `
                : `פחות מ-${ltr(`f(${e - 1}, ${t - 1}) = ${sp.fBelow}`)}, כי ההטלה לא עולה מעל הקומה האחרונה שעוד לא ידועה. ${ltr(e - 1)} ${e - 1 === 1 ? "ביצה שנשארת" : "ביצים שנשארות"} אחרי שבירה מכריעות ב-${ltr(t - 1)} ההטלות שנשארו עד ${ltr(sp.fBelow)} קומות, ולכן גם ${ltr(sp.below)} האלה. `) +
            `מעליה <span class="eg-above-txt">${ltr(sp.above)} קומות</span>, ו-${ltr(`f(${e}, ${t - 1}) = ${sp.fAbove}`)} ${sp.above === sp.fAbove ? "מכריעות בדיוק אותן" : "מכריעות עד כמה שצריך"} אם היא לא נשברת. ` +
            `ביחד ${ltr(`f(${e}, ${t}) = f(${e - 1}, ${t - 1}) + 1 + f(${e}, ${t - 1}) = ${sp.fBelow} + 1 + ${sp.fAbove}`)}${sp.fBelow + 1 + sp.fAbove > st.n ? `, יותר מ-${ltr(st.n)} הקומות` : ""}, והטווח הלא ידוע הוא ${ltr(s.high - s.low - 1)} קומות.`;
        } else $(".eg-rec-text").innerHTML = "";
        // the clickable floors
        box.querySelectorAll(".eg-row").forEach((r) => {
          const pick = () => { setT(Number(r.dataset.fl), false); };
          r.addEventListener("click", pick);
          r.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); } });
        });
        const hit = $(".eg-hit");
        if (hit) hit.addEventListener("click", (e) => {
          const svg = hit.ownerSVGElement, r = svg.getBoundingClientRect();
          const yv = 18 + ((e.clientY - r.top) / r.height) * 380;
          const fl = Math.round(st.n - ((yv - 18) / (362 - 18)) * st.n);
          setT(Math.max(0, Math.min(st.n, fl)), true);
        });
      };
      let stop = () => {};
      const setT = (T, recentre) => { stop(); st.T = T; st.step = 0; if (recentre) st.win = null; compute(); draw(); };
      const setKN = (k, n) => {
        const err = !Number.isInteger(n) || n < 1 || n > NMAX ? `מספר קומות שלם מ-1 עד ${NMAX}` : "";
        $(".eg-err").textContent = err;
        if (err) return;
        stop(); st.k = k; st.n = n; st.T = Math.min(st.T, n); st.step = 0; st.win = null; compute(); draw();
      };
      $(".ex-k").addEventListener("input", () => setKN(Number($(".ex-k").value), st.n));
      $(".eg-n").addEventListener("change", () => setKN(st.k, Math.round(Number($(".eg-n").value))));
      $(".eg-n").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".eg-n").blur(); });
      const readT = () => { const v = Math.round(Number($(".eg-t").value)); if (v >= 0 && v <= st.n) setT(v, true); else $(".eg-t").value = st.T; };
      $(".eg-t").addEventListener("change", readT);
      $(".eg-t").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".eg-t").blur(); });
      $(".eg-rec").addEventListener("change", draw);
      $(".eg-win").addEventListener("input", () => { st.win = clampWin(Number($(".eg-win").value)); draw(); });
      const seed = seedControls(box, $(".ex-random"), (rng) => { setT(Math.floor(rng() * (st.n + 1)), true); });
      $(".ex-random").addEventListener("click", () => seed.draw());
      $(".ex-reset").addEventListener("click", () => { $(".ex-k").value = K0; st.T = T0; setKN(K0, N0); });
      $(".ex-next").addEventListener("click", () => { stop(); if (st.step < st.drops.length) { st.step++; st.win = null; draw(); } });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.step > 0) { st.step--; st.win = null; draw(); } });
      $(".ex-start").addEventListener("click", () => { stop(); st.step = 0; st.win = null; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.step = st.drops.length; st.win = null; draw(); });
      stop = autoplay(play, speed, { step: () => { st.step++; st.win = null; draw(); }, done: () => st.step >= st.drops.length, restart: () => { st.step = 0; st.win = null; draw(); } });
      compute();
      draw();
    },
  });

  dvqExplorers.register({
    views: { eggs: eggsView },
    help: {
      eggs: "k ביצים ו-n קומות בבקרות, והסף נבחר בלחיצה על הבניין, על קומה בתקריב או בשדה. ״ההטלה הבאה״ ו״הפעלה״ מריצים את התוכנית : הבניין צובע את הקומות הידועות, התקריב מראה את הקומות הלא ידועות אחת-אחת, והגרף סופר את ההטלות לכל סף מתחת לקו של המקרה הגרוע. המתג ״הנוסחה על הבניין״ מסמן ליד הבניין את שני החלקים של ההטלה הבאה, f(k − 1, t − 1) מתחתיה ו-f(k, t − 1) מעליה.",
    },
    models: { eggsTable, eggsSplitAt, eggsDrops, eggsRun, eggsFirst, eggsPerThreshold },
  });
})();
