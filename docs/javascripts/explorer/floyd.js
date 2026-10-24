// kinds: floyd
//   floyd                  0017        the array as the graph i -> nums[i], the tortoise and the hare through both phases; the copy link carries the array and the step
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { H, STATE_CODECS, W, answer, f, floydParse, floydTrace, ltr, seedControls } = dvqExplorers.lib;

  // Find the duplicate (0017): nums has n + 1 values in 1..n. The walk i -> nums[i] from
  // 0 is a tail and a cycle (the rho); the entry of the cycle is a duplicate value.
  const floydRho = (nums) => {
    const seen = new Map();                          // node -> position in the walk
    const walk = [];
    let x = 0;
    while (!seen.has(x)) { seen.set(x, walk.length); walk.push(x); x = nums[x]; }
    const mu = seen.get(x), tail = walk.slice(0, mu), cycle = walk.slice(mu);
    const reached = new Set(walk);
    const others = nums.map((_, i) => i).filter((i) => !reached.has(i));
    return { tail, cycle, entry: x, mu, lambda: cycle.length, others };
  };
  // a random input like the page's test: 1..n, one value copied over another, shuffled
  const floydRandom = (n, rnd = Math.random) => {
    const nums = Array.from({ length: n }, (_, i) => i + 1);
    const v = 1 + Math.floor(rnd() * n);
    nums[Math.floor(rnd() * n)] = v;
    nums.push(v);
    for (let i = nums.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [nums[i], nums[j]] = [nums[j], nums[i]]; }
    return nums;
  };
  // The Floyd box (0017): the array as a row of cells and as the graph i -> nums[i] laid
  // out as a rho (the tail in a line, the cycle as a circle, unreached indices below);
  // the tortoise and the hare step through the two phases, played or one step at a time.
  const floydView = () => ({
    mount(box) {
      const EXAMPLE = [3, 9, 5, 6, 7, 8, 1, 1, 2, 4];
      const nmax = Number(box.dataset.nmax || 12), NODE = 16;
      const st = { nums: EXAMPLE, k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏n</span><input type="range" class="ex-n" min="3" max="${nmax}" step="1" value="${EXAMPLE.length - 1}" dir="ltr"><output class="out-n"></output></label>` +
        `<button type="button" class="md-button md-button--primary ex-shuffle">הגרלה</button>` +
        `<button type="button" class="md-button ex-example">הדוגמה מהדף</button>` +
        `<label class="fl-input"><span>המערך</span><input type="text" class="ex-nums" dir="ltr" spellcheck="false" aria-label="המערך, מספרים מופרדים בפסיקים"></label>` +
        `<button type="button" class="md-button ex-apply">החלה</button><span class="fl-err" aria-live="polite"></span></div>` +
        `<div class="fl-cells" dir="ltr"></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1500">איטי</option><option value="700" selected>בינוני</option><option value="250">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<div class="fl-graph"></div><p class="fl-step" aria-live="polite"></p><p class="ex-summary fl-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), numsIn = $(".ex-nums");
      let timer = null;
      const graphSvg = (rho, fr, done) => {
        const { tail, cycle, entry, others } = rho;
        const pos = new Map();
        const GAP = 60;
        tail.forEach((v, i) => pos.set(v, [30 + GAP * i, 0]));
        const r = Math.max(48, (cycle.length * 44) / (2 * Math.PI));
        const cx = (tail.length ? 30 + GAP * (tail.length - 1) : -30) + GAP + r;
        cycle.forEach((v, i) => {
          const a = Math.PI - (2 * Math.PI * i) / cycle.length;     // the entry on the left
          pos.set(v, [cx + r * Math.cos(a), -r * Math.sin(a)]);
        });
        const top = r + 30, rowY = r + 70;
        others.forEach((v, i) => pos.set(v, [30 + 50 * i, rowY]));
        const W = Math.max(cx + r + 30, others.length ? 30 + 50 * (others.length - 1) + 30 : 0);
        const H = top + (others.length ? rowY : r) + 30;
        const P = (v) => { const [x, y] = pos.get(v); return [x, y + top]; };
        const dupEdges = done ? new Set(st.nums.map((v, i) => (v === entry ? i : -1)).filter((i) => i >= 0)) : new Set();
        let s = `<svg class="figure fl-live" viewBox="0 0 ${f(W, 0)} ${f(H, 0)}" role="img" aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו">`;
        st.nums.forEach((v, i) => {
          const [x0, y0] = P(i), [x1, y1] = P(v);
          const faded = others.includes(i) ? " st-faded" : "";
          const hot = dupEdges.has(i);
          if (i === v) {                                           // nums[i] = i: a loop
            s += `<circle class="${hot ? "s2-line" : "ink-line"}${faded}" cx="${f(x0)}" cy="${f(y0 - NODE - 9)}" r="9" fill="none" stroke-width="2.2"/>`;
            return;
          }
          // edges of unreached indices bend upward, so a row of them stays readable
          const bend = faded ? 0.3 : 0;
          const d = Math.hypot(x1 - x0, y1 - y0);
          const mx = (x0 + x1) / 2 - ((y1 - y0) / d) * d * bend, my = (y0 + y1) / 2 + ((x1 - x0) / d) * d * bend - (faded ? 2 : 0);
          const d0 = Math.hypot(mx - x0, my - y0), d1 = Math.hypot(x1 - mx, y1 - my);
          const u0x = (mx - x0) / d0, u0y = (my - y0) / d0, ux = (x1 - mx) / d1, uy = (y1 - my) / d1;
          const ax = x0 + u0x * (NODE + 2), ay = y0 + u0y * (NODE + 2), bx = x1 - ux * (NODE + 3), by = y1 - uy * (NODE + 3);
          const hx = bx - ux * 9, hy = by - uy * 9;
          s += `<g class="fl-edge${faded}"><path class="${hot ? "s2-line" : "ink-line"}" d="M${f(ax)},${f(ay)} Q${f(mx)},${f(my)} ${f(bx)},${f(by)}" fill="none" stroke-width="${hot ? 3 : 2.2}"><title>nums[${i}] = ${v}</title></path>` +
               `<polygon class="${hot ? "s2-fill" : "ink-fill"}" points="${f(bx)},${f(by)} ${f(hx + uy * 4.5)},${f(hy - ux * 4.5)} ${f(hx - uy * 4.5)},${f(hy + ux * 4.5)}"/></g>`;
        });
        st.nums.forEach((_, v) => {
          const [x, y] = P(v);
          const cls = done && v === entry ? "st-ok" : "st-cell";
          s += `<g${others.includes(v) ? ' class="st-faded"' : ""}><circle class="${cls}" cx="${f(x)}" cy="${f(y)}" r="${NODE}"/>` +
               `<text class="st-text st-sm" x="${f(x)}" y="${f(y + 4)}" text-anchor="middle">${v}</text></g>`;
        });
        if (fr) {
          const [sx, sy] = P(fr.slow), [fx, fy] = P(fr.fast);
          s += `<circle class="fl-slow" cx="${f(sx)}" cy="${f(sy)}" r="${NODE + 5}"/><circle class="fl-fast" cx="${f(fx)}" cy="${f(fy)}" r="${NODE + 10}"/>`;
        }
        return s + "</svg>";
      };
      const draw = () => {
        const nums = st.nums, n = nums.length - 1;
        $(".out-n").textContent = String(n);
        if (document.activeElement !== numsIn) numsIn.value = nums.join(", ");
        const rho = floydRho(nums), tr = floydTrace(nums);
        st.k = Math.min(st.k, tr.frames.length - 1);
        const fr = tr.frames[st.k], last = st.k === tr.frames.length - 1;
        $(".fl-cells").innerHTML = `<div class="box-grid fl-grid" style="grid-template-columns: repeat(${n + 1}, minmax(0, 1fr))">` +
          nums.map((v, i) => `<span class="${[i === fr.slow ? "is-slow" : "", i === fr.fast ? "is-fast" : "", last && v === rho.entry ? "hl" : ""].join(" ").trim()}"><small>${i}</small><b>${v}</b></span>`).join("") + `</div>`;
        $(".fl-graph").innerHTML = graphSvg(rho, fr, last);
        $(".ex-pos").textContent = `צעד ${st.k} מתוך ${tr.frames.length - 1}`;
        let text;
        if (fr.phase === 1 && fr.step === 0) text = "שלב 1 : הצב והארנב מתחילים באינדקס 0, שאף ערך לא מצביע עליו.";
        else if (fr.phase === 1 && fr.slow !== fr.fast) text = `שלב 1, איטרציה ${ltr(fr.step)} : הצב מתקדם צעד אחד ל-${ltr(fr.slow)}, והארנב שני צעדים ל-${ltr(fr.fast)}.`;
        else if (fr.phase === 1) text = `שלב 1, איטרציה ${ltr(fr.step)} : שניהם ב-${ltr(fr.slow)}. נפגשו בתוך המעגל, ומספר האיטרציות ${ltr(fr.step)} הוא כפולה של אורך המעגל ${ltr(rho.lambda)}.`;
        else if (fr.step === 0) text = `שלב 2 : מחזירים את הצב ל-0. הארנב נשאר בנקודת המפגש ${ltr(tr.meet)}, ומעכשיו שניהם צועדים צעד אחד.`;
        else if (fr.slow !== fr.fast) text = `שלב 2, איטרציה ${ltr(fr.step)} : הצב ב-${ltr(fr.slow)}, הארנב ב-${ltr(fr.fast)}.`;
        else {
          const into = nums.map((v, i) => (v === rho.entry ? i : -1)).filter((i) => i >= 0);
          text = `שלב 2, איטרציה ${ltr(fr.step)} : שניהם ב-${ltr(fr.slow)}, הכניסה למעגל. ${into.length === 2 ? "שני חצים נכנסים" : `${ltr(into.length)} חצים נכנסים`} אליה, מהאינדקסים ${ltr(into.join(", "))}, ולכן <b>${ltr(fr.slow)}</b> הוא הערך הכפול.`;
        }
        $(".fl-step").innerHTML = text;
        $(".fl-sum").innerHTML = `הזנב : ${rho.mu === 0 ? "ריק" : ltr(rho.tail.join(" → "))} (${ltr(`μ = ${rho.mu}`)}), המעגל : ${ltr(rho.cycle.join(" → "))} (${ltr(`λ = ${rho.lambda}`)}). ` +
          `המפגש אחרי ${ltr(tr.frames.findIndex((g) => g.phase === 2) - 1)} איטרציות, ושלב 2 לוקח ${ltr(rho.mu)}. התשובה : ${ltr(tr.answer)}.` +
          (rho.others.length ? ` האינדקסים ${ltr(rho.others.join(", "))} לא נגישים מ-0 ולא משנים כלום.` : "");
        answer(box, last ? `הערך הכפול הוא ${ltr(tr.answer)} : הכניסה למעגל, שהצב והארנב נפגשים בה בשלב 2.` : null, ".fl-cells .hl");
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const setNums = (nums) => { stop(); st.nums = nums; st.k = 0; $(".ex-n").value = nums.length - 1; $(".fl-err").textContent = ""; draw(); };
      const total = () => floydTrace(st.nums).frames.length - 1;
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= total()) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      $(".ex-n").addEventListener("input", () => setNums(floydRandom(Number($(".ex-n").value))));
      const seed = seedControls(box, $(".ex-example"), (rng) => setNums(floydRandom(st.nums.length - 1, rng)), { state: {
        get: () => STATE_CODECS.floyd.enc({ nums: st.nums, k: st.k }),
        set: (p) => { const d = STATE_CODECS.floyd.dec(p, nmax); if (!d) return false; setNums(d.nums); st.k = d.k; draw(); return true; },
      } });
      $(".ex-shuffle").addEventListener("click", seed.draw);
      $(".ex-example").addEventListener("click", () => setNums(EXAMPLE));
      const apply = () => {
        const nums = floydParse(numsIn.value);
        if (nums && nums.length - 1 <= nmax) setNums(nums);
        else $(".fl-err").textContent = `צריך n + 1 מספרים בין 1 ל-n, עם n עד ${nmax}.`;
      };
      $(".ex-apply").addEventListener("click", apply);
      numsIn.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); apply(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { floyd: floydView },
    help: {
      floyd: "המערך כגרף של זנב ומעגל : ״הגרלה״ או הקלדה קובעים אותו, ו״הצעד הבא״ ו״הפעלה״ מזיזים את הצב ואת הארנב דרך שני השלבים עד הערך הכפול.",
    },
    models: { floydRho, floydRandom },
  });
})();
