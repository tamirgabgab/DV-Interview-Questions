// kinds: bfs01
//   bfs01                  0005        the remainders modulo x on a ring, the BFS tree one dequeue at a time, the answer read back; a digit set and a length-only mode
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { W, X0, f, ltr } = dvqExplorers.lib;

  // Smallest 0/1 multiple (0005): the page's BFS over the remainders modulo x, one frame
  // per dequeue: the remainder taken out, its children (the smaller digit first) with
  // their fate, and the queue after the step. Numbers are strings of digits (they outgrow
  // 2^53). `digits` is the allowed set (the page's [0, 1]; the follow-up's [3, 7]): the
  // BFS starts from every non-zero digit, and when the queue empties before the
  // remainder 0 there is no multiple (answer null). `depth` is the BFS layer of every
  // remainder reached (the length of its number), for the length-only mode.
  const bfs01Trace = (x, digits = [0, 1]) => {
    const parent = new Array(x).fill(-1), digit = new Array(x).fill(""), visited = new Array(x).fill(false), depth = new Array(x).fill(0);
    const starts = [], queue = [];
    digits.filter((d) => d > 0).forEach((d) => {
      const r = d % x;
      if (visited[r]) return;
      visited[r] = true; digit[r] = String(d); depth[r] = 1; starts.push(r); queue.push(r);
    });
    const number = (r) => { let s = ""; for (let q = r; q !== -1; q = parent[q]) s = digit[q] + s; return s; };
    const frames = [];
    while (!visited[0] && queue.length) {
      const r = queue.shift(), kids = [];
      for (const d of digits) {
        const nr = (r * 10 + d) % x;
        if (!visited[nr]) { visited[nr] = true; parent[nr] = r; digit[nr] = String(d); depth[nr] = depth[r] + 1; queue.push(nr); kids.push({ d, nr, status: nr === 0 ? "found" : "new" }); }
        else kids.push({ d, nr, status: "seen" });
      }
      frames.push({ r, number: number(r), kids, queue: [...queue] });
    }
    const found = visited[0];
    const path = [];                                 // remainders from the start to 0
    if (found) for (let q = 0; q !== -1; q = parent[q]) path.unshift(q);
    return { frames, answer: found ? number(0) : null, path, parent, digit, depth, start: starts[0], starts, dequeues: frames.length, digits };
  };
  // the counts of the page's chart: multiples of x scanned, numbers over the digit set
  // enumerated in increasing order up to the answer, dequeues
  const bfs01Counts = (x, digits = [0, 1]) => {
    const t = bfs01Trace(x, digits);
    if (t.answer === null) return { multiples: null, enumerated: null, dequeues: t.dequeues, answer: null };
    const y = BigInt(t.answer), k = BigInt(digits.length), nz = digits.filter((d) => d > 0), L = t.answer.length;
    let enumerated = 0n, pow = 1n;                   // numbers shorter than the answer
    for (let len = 1; len < L; len++) { enumerated += BigInt(nz.length) * pow; pow *= k; }
    let rank = 0n;                                   // the answer's place among the numbers of its length
    for (let i = 0; i < L; i++) {
      const d = Number(t.answer[i]);
      rank = rank * k + BigInt(i === 0 ? nz.indexOf(d) : digits.indexOf(d));
    }
    enumerated += rank + 1n;
    return { multiples: (y / BigInt(x)).toString(), enumerated: enumerated.toString(), dequeues: t.dequeues, answer: t.answer };
  };

  // The remainders box (0005): the x remainders on a ring, the BFS tree growing one
  // dequeue at a time with +0 edges blue and +1 edges orange, the queue beside it, and at
  // the end the path back from 0 that spells the answer, with the step counts of the
  // three methods.
  const bfs01View = () => ({
    mount(box) {
      const xmax = Number(box.dataset.xmax || 40);
      const st = { x: Number(box.dataset.x || 7), k: 0, digits: [0, 1], lenOnly: false };
      const big = (s) => { const b = BigInt(s); return b < 10n ** 12n ? Number(b).toLocaleString("en-US") : `${(Number(b / 10n ** BigInt(s.length - 3)) / 100).toFixed(2)}·10^${s.length - 1}`; };
      const DIGIT_CLS = ["s1", "s2", "s3"];          // one colour per allowed digit, in order
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏x</span><input type="range" class="ex-x" min="1" max="${xmax}" step="1" value="${st.x}" dir="ltr"><output class="out-x"></output></label>` +
        `<span class="bf-presets">דוגמאות : ` + [7, 9, 11, 13, 37].filter((v) => v <= xmax).map((v) => `<button type="button" class="md-button ex-preset" data-x="${v}">${v}</button>`).join(" ") + `</span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls">` +
        `<label>הספרות המותרות <input type="text" class="ex-digits" value="0 1" size="7" dir="ltr" inputmode="numeric" aria-label="הספרות המותרות, עד שלוש"></label>` +
        `<span class="bf-presets"><button type="button" class="md-button ex-digitset" data-digits="0 1">0 ו-1 (השאלה)</button> <button type="button" class="md-button ex-digitset" data-digits="3 7">3 ו-7 (שאלת ההמשך)</button></span>` +
        `<label><input type="checkbox" class="ex-lenonly"> <span>רק האורך, בלי שחזור ההורים</span></label><span class="fl-err bf-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1500">איטי</option><option value="700" selected>בינוני</option><option value="250">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<span class="viz-legend bf-legend"></span>` +
        `<div class="bf-box"><div class="bf-ring"></div><div class="bf-panel"><p class="bf-step" aria-live="polite"></p><p class="bf-queue"></p><p class="bf-path"></p></div></div>` +
        `<p class="ex-summary bf-sum"></p><p class="ex-note bf-mem"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let timer = null, trace = null;
      const clsOf = (d) => DIGIT_CLS[st.digits.indexOf(d)] || "ink";
      const legend = () => st.digits.map((d) => `<span><i class="${clsOf(d)}"></i>הוספת ${d}</span>`).join("") +
        `<span><i class="st-stack"></i>בתור</span><span><i class="st-done"></i>טופל</span><span><i class="st-ok"></i>שארית 0</span>`;
      const ringSvg = (tr, k) => {
        const x = st.x, W = 360, C = 180, R = x <= 12 ? 120 : 140, NODE = x <= 12 ? 16 : x <= 24 ? 13 : 10;
        const pt = (r, rad) => { const a = -Math.PI / 2 + (2 * Math.PI * r) / x; return [C + rad * Math.cos(a), C + rad * Math.sin(a)]; };
        const done = new Set(), queued = new Set(tr.frames.length ? tr.starts : []);
        const edges = [];
        for (let i = 0; i < k; i++) {
          const fr = tr.frames[i];
          done.add(fr.r); queued.delete(fr.r);
          fr.kids.forEach((kid) => { if (kid.status !== "seen") { queued.add(kid.nr); edges.push([fr.r, kid.nr, kid.d, false]); } });
        }
        const cur = k > 0 ? tr.frames[k - 1] : null;
        if (cur) cur.kids.forEach((kid) => { if (kid.status === "seen") edges.push([cur.r, kid.nr, kid.d, true]); });
        const finished = k >= tr.frames.length && tr.answer !== null;
        const onPath = new Set(finished && !st.lenOnly ? tr.path : []);
        const seen = new Set([...done, ...queued]);
        let s = `<svg class="figure bf-live" viewBox="0 0 ${W} ${W}" role="img" aria-label="${x} השאריות מודולו ${x} במעגל, ועץ ה-BFS">`;
        const arrow = (a, b, cls, dashed, thick) => {
          const [x0, y0] = pt(a, R), [x1, y1] = pt(b, R);
          if (a === b) {
            const [ox, oy] = pt(a, R + NODE + 10);
            return `<circle class="${cls}" cx="${f(ox)}" cy="${f(oy)}" r="8" fill="none" stroke-width="${thick ? 3.5 : 2}"${dashed ? ' stroke-dasharray="4 3"' : ""}/>`;
          }
          const dx = x1 - x0, dy = y1 - y0, len = Math.hypot(dx, dy);
          const mx = (x0 + x1) / 2 + (-dy / len) * len * 0.2, my = (y0 + y1) / 2 + (dx / len) * len * 0.2;
          const d1 = Math.hypot(x1 - mx, y1 - my), ux = (x1 - mx) / d1, uy = (y1 - my) / d1;
          const d0 = Math.hypot(mx - x0, my - y0), vx = (mx - x0) / d0, vy = (my - y0) / d0;
          const sx = x0 + vx * (NODE + 1), sy = y0 + vy * (NODE + 1), ex = x1 - ux * (NODE + 2), ey = y1 - uy * (NODE + 2);
          const hx = ex - ux * 8, hy = ey - uy * 8;
          return `<path class="${cls}-line" d="M${f(sx)},${f(sy)} Q${f(mx)},${f(my)} ${f(ex)},${f(ey)}" fill="none" stroke-width="${thick ? 3.5 : 2}"${dashed ? ' stroke-dasharray="4 3"' : ""}/>` +
                 (dashed ? "" : `<polygon class="${cls}-fill" points="${f(ex)},${f(ey)} ${f(hx + uy * 4)},${f(hy - ux * 4)} ${f(hx - uy * 4)},${f(hy + ux * 4)}"/>`);
        };
        // length only: no tree, just the layer number beside every remainder reached
        if (!st.lenOnly) edges.forEach(([a, b, d, pruned]) => {
          const thick = onPath.has(a) && onPath.has(b) && tr.parent[b] === a;
          s += arrow(a, b, clsOf(d), pruned, thick);
        });
        for (let r = 0; r < x; r++) {
          const [px, py] = pt(r, R);
          const cls = finished && r === 0 ? "st-ok" : cur && r === cur.r ? "st-stack is-cur" : queued.has(r) ? "st-stack" : done.has(r) ? "st-done" : "st-cell";
          s += `<g><circle class="${cls}${onPath.has(r) ? " is-path" : ""}" cx="${f(px)}" cy="${f(py)}" r="${NODE}"><title>שארית ${r}${seen.has(r) ? `, שכבה ${tr.depth[r]}` : ""}</title></circle>` +
               `<text class="st-text ${x <= 12 ? "st-sm" : "bf-xs"}" x="${f(px)}" y="${f(py + (x <= 12 ? 4 : 3.5))}" text-anchor="middle">${r}</text>`;
          if (st.lenOnly && seen.has(r)) { const [lx, ly] = pt(r, R + NODE + 9); s += `<text class="legend bf-layer" x="${f(lx)}" y="${f(ly + 4)}" text-anchor="middle">${tr.depth[r]}</text>`; }
          s += `</g>`;
        }
        return s + "</svg>";
      };
      // the hardware follow-up: what the reconstruction costs against a length-only search
      const memLine = () => {
        const bits = (x) => { const w = Math.max(1, Math.ceil(Math.log2(x + 1))), full = x * (w + 1), lean = 3 * x; return { w, full, lean }; };
        const kb = (b) => `${(b / 8192).toFixed(b < 8192 ? 2 : 0)} KB`;
        const here = bits(st.x), wide = bits(65535);
        return `זיכרון : עם שחזור, ${ltr(st.x)} הורים של ${ltr(here.w)} ביט ועוד ${ltr(st.x)} ספרות, ${ltr(here.full.toLocaleString("en-US"))} ביט; רק האורך, שלוש מפות ביטים של ${ltr(st.x)} ביט (נראה, החזית, החזית הבאה) ומונה שכבה, ${ltr(here.lean.toLocaleString("en-US"))} ביט. ` +
          `ל-${ltr("x")} של 16 ביט : ${ltr(wide.full.toLocaleString("en-US"))} ביט (${ltr(kb(wide.full))}) מול ${ltr(wide.lean.toLocaleString("en-US"))} ביט (${ltr(kb(wide.lean))}); התור של ההורים הוא FIFO של עד ${ltr("x")} כניסות של ${ltr(wide.w)} ביט.`;
      };
      const digitsText = () => st.digits.join("/");
      const draw = () => {
        $(".out-x").textContent = String(st.x);
        $(".bf-legend").innerHTML = legend();
        trace = bfs01Trace(st.x, st.digits);
        const tr = trace, total = tr.frames.length, none = tr.answer === null;
        st.k = Math.min(st.k, total);
        $(".bf-ring").innerHTML = ringSvg(tr, st.k);
        $(".ex-pos").textContent = `הוצאה ${st.k} מתוך ${total}`;
        const name = (r, n) => `${ltr(`r = ${r}`)} (המספר ${ltr(n)})`;
        const startNums = st.digits.filter((d) => d > 0);
        let step;
        if (st.k === 0) {
          step = total === 0 && !none
            ? `עבור ${ltr(`x = ${st.x}`)} המספר ${ltr(tr.answer)} כבר נותן שארית 0, ולכן התשובה היא ${ltr(tr.answer)} בלי צעדים.`
            : `מתחילים מ${startNums.length === 1 ? `המספר ${ltr(startNums[0])}, שארית ${ltr(tr.starts[0])}` : `המספרים ${ltr(startNums.join(", "))}, שאריות ${ltr(tr.starts.join(", "))}`}. התור : ${ltr(`[${tr.starts.join(", ")}]`)}.`;
        } else {
          const fr = tr.frames[st.k - 1];
          const kid = (kd) => {
            const n = fr.number + kd.d;
            return `${ltr(`+${kd.d}`)} → ${ltr(n)}, שארית ${ltr(kd.nr)} : ` +
              (kd.status === "new" ? "חדשה, נכנסת לתור" : kd.status === "seen" ? `כבר נראתה, נגזמת ✗` : `<b>0, מצאנו ✓</b>`);
          };
          step = `הוצאה ${ltr(st.k)} : מוציאים ${name(fr.r, fr.number)}. ${fr.kids.map(kid).join("; ")}.`;
        }
        $(".bf-step").innerHTML = step;
        const q = st.k === 0 ? tr.starts : tr.frames[st.k - 1].queue;
        $(".bf-queue").innerHTML = st.k > 0 ? `התור אחרי הצעד : ${ltr(`[${q.join(", ")}]`)}.` : "";
        const finished = st.k >= total;
        $(".bf-path").innerHTML = !finished ? ""
          : none ? `<span class="wv-bad">✗ התור התרוקן ושארית 0 לא נמצאה : לאף מספר מהספרות ${ltr(digitsText())} אין שארית 0 מודולו ${ltr(st.x)}, כלומר אין פתרון.</span>`
          : st.lenOnly ? `שארית 0 התגלתה בשכבה ${ltr(tr.depth[0])} : לכפולה הקטנה ביותר יש <b>${ltr(tr.depth[0])} ספרות</b>. בלי ההורים אי אפשר לומר איזו כפולה, רק כמה ספרות יש לה.`
          : `השחזור : ${ltr(tr.path.slice().reverse().map((r, i) => (i === 0 ? "0" : `← ${r}`)).join(" "))}, הספרות מהסוף להתחלה נותנות <b>${ltr(`y = ${tr.answer}`)}</b> (${ltr(`${tr.answer.length}`)} ספרות).`;
        const c = bfs01Counts(st.x, st.digits);
        $(".bf-sum").innerHTML = none
          ? `עבור ${ltr(`x = ${st.x}`)} והספרות ${ltr(digitsText())} : ה-BFS מוציא מהתור ${ltr(c.dequeues)} שאריות ונעצר בלי למצוא 0. ` +
            (st.digits.every((d) => d % 2) && st.x % 2 === 0 ? `כל הספרות אי-זוגיות, ולכן כל מספר שבנוי מהן אי-זוגי ואינו מתחלק ב-${ltr(st.x)}.` : `השאריות שהספרות האלה מגיעות אליהן אינן כוללות את 0.`)
          : `עבור ${ltr(`x = ${st.x}`)}${st.digits.join("") === "01" ? "" : ` והספרות ${ltr(digitsText())}`} : ה-BFS מוציא מהתור ${ltr(c.dequeues)} שאריות${c.dequeues < st.x ? ` (פחות מ-${ltr(st.x)})` : ""}. ` +
            `לשם השוואה, המעבר על המספרים מהספרות ${ltr(digitsText())} בודק ${ltr(big(c.enumerated))} מספרים, והמעבר על הכפולות של ${ltr(st.x)} בודק ${ltr(big(c.multiples))}.`;
        $(".bf-mem").innerHTML = st.lenOnly ? memLine() : "";
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => bfs01Trace(st.x, st.digits).frames.length;
      const setX = (x) => { stop(); st.x = x; st.k = 0; $(".ex-x").value = x; draw(); };
      $(".ex-x").addEventListener("input", () => setX(Number($(".ex-x").value)));
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => setX(Number(b.dataset.x))));
      // the digit set: up to three distinct digits, at least one of them non-zero
      const setDigits = (text) => {
        const ds = [...new Set((text.match(/[0-9]/g) || []).map(Number))].sort((a, b) => a - b);
        const err = ds.length === 0 || ds.length > 3 ? "בין ספרה אחת לשלוש" : ds.every((d) => d === 0) ? "לפחות ספרה אחת שאינה 0" : "";
        $(".bf-err").textContent = err;
        if (err) return;
        stop(); st.digits = ds; st.k = 0; $(".ex-digits").value = ds.join(" "); draw();
      };
      $(".ex-digits").addEventListener("change", () => setDigits($(".ex-digits").value));
      $(".ex-digits").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".ex-digits").blur(); });
      box.querySelectorAll(".ex-digitset").forEach((b) => b.addEventListener("click", () => setDigits(b.dataset.digits)));
      $(".ex-lenonly").addEventListener("change", () => { stop(); st.lenOnly = $(".ex-lenonly").checked; draw(); });
      const X0 = st.x;
      $(".ex-reset").addEventListener("click", () => { st.lenOnly = false; $(".ex-lenonly").checked = false; setDigits("0 1"); setX(X0); });
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
      draw();
    },
  });

  dvqExplorers.register({
    views: { bfs01: bfs01View },
    help: {
      bfs01: "השאריות מודולו x על טבעת : ״הצעד הבא״ מוציא שארית מהתור ומצייר את עץ ה-BFS, ובסוף התשובה נקראת בחזרה. שדה הספרות ומצב ״רק האורך״ הם שאלות ההמשך.",
    },
    models: { bfs01Trace, bfs01Counts },
  });
})();
