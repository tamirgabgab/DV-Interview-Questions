// kinds: rainwater
//   rainwater              0047        part a (data-mode="row"): columns up to 24 with heights 0 to 9 (a tap on a cell sets the column's height, the arrows on a focused column raise or lower it, a random fill), the two pointers of the page's trap played a move at a time with left_max and right_max, the water of every column done so far, and a table of maxL, maxR and the water per column; part b (data-mode="map"): a height map up to 10 × 10 (a tap raises a cell, a digit sets it, a random fill), the page's trap_2d played a pop at a time: the boundary in the heap outlined, the popped cell framed, the neighbours it fills, the water by depth and the heap in order
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const ROW_MAX = 24, MAP_MAX = 10, H_MAX = 9;

  // Part a, the page's trap one move at a time: the lower side moves, its maximum is
  // updated and its column gets max - height. A step per move (n - 1 of them); the column
  // where the pointers meet is a highest one and holds no water.
  const rwRow = (h) => {
    const n = h.length, steps = [], water = Array(n).fill(0);
    let l = 0, r = n - 1, lm = 0, rm = 0, total = 0;
    while (l < r) {
      const left = h[l] < h[r], i = left ? l : r;
      if (left) lm = Math.max(lm, h[l]); else rm = Math.max(rm, h[r]);
      const w = (left ? lm : rm) - h[i];
      water[i] = w;
      total += w;
      steps.push({ left, i, l, r, lm, rm, w, total });
      if (left) l++; else r--;
    }
    const maxL = [], maxR = [];
    h.forEach((v, i) => { maxL.push(Math.max(v, i ? maxL[i - 1] : 0)); });
    for (let i = n - 1; i >= 0; i--) maxR[i] = Math.max(h[i], i < n - 1 ? maxR[i + 1] : 0);
    return { steps, water, total, maxL, maxR };
  };

  // Part b, the page's trap_2d one pop at a time. The heap is ordered by (level, row,
  // column), as Python's heapq orders the page's tuples, so the pops come in the page's
  // order. A step per pop, with the neighbours it reached (their height and water) and the
  // heap after it.
  const rwMap = (h) => {
    const m = h.length, n = m ? h[0].length : 0;
    const less = (a, b) => a[0] - b[0] || a[1] - b[1] || a[2] - b[2];
    const heap = [], push = (x) => {
      heap.push(x);
      for (let i = heap.length - 1; i > 0;) {
        const p = (i - 1) >> 1;
        if (less(heap[p], heap[i]) <= 0) break;
        [heap[p], heap[i]] = [heap[i], heap[p]];
        i = p;
      }
    };
    const pop = () => {
      const top = heap[0], last = heap.pop();
      if (heap.length) {
        heap[0] = last;
        for (let i = 0; ;) {
          let k = i;
          for (const c of [2 * i + 1, 2 * i + 2]) if (c < heap.length && less(heap[c], heap[k]) < 0) k = c;
          if (k === i) break;
          [heap[k], heap[i]] = [heap[i], heap[k]];
          i = k;
        }
      }
      return top;
    };
    const seen = h.map((row, i) => row.map((_, j) => i === 0 || i === m - 1 || j === 0 || j === n - 1));
    const water = h.map((row) => row.map(() => 0)), steps = [];
    for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) if (seen[i][j]) push([h[i][j], i, j]);
    let total = 0;
    while (heap.length) {
      const [level, r, c] = pop(), fills = [];
      for (const [a, b] of [[r + 1, c], [r - 1, c], [r, c + 1], [r, c - 1]]) {
        if (a < 0 || a >= m || b < 0 || b >= n || seen[a][b]) continue;
        seen[a][b] = true;
        const w = Math.max(0, level - h[a][b]);
        water[a][b] = w;
        total += w;
        fills.push({ r: a, c: b, h: h[a][b], w });
        push([Math.max(level, h[a][b]), a, b]);
      }
      steps.push({ r, c, level, fills, total, heap: heap.slice().sort(less) });
    }
    return { steps, water, total };
  };

  const rwParse = (text) => {
    if (!/^\d+(\.\d+)*$/.test(text)) return null;
    const rows = text.split(".");
    if (rows.length > MAP_MAX || rows[0].length > MAP_MAX || rows.some((r) => r.length !== rows[0].length)) return null;
    return rows.map((r) => [...r].map(Number));
  };
  const rwText = (h) => h.map((r) => r.join("")).join(".");
  const rowParse = (text) => {
    if (!/^\d(,\d)*$/.test(text)) return null;
    const h = text.split(",").map(Number);
    return h.length <= ROW_MAX ? h : null;
  };

  const P = (r, c) => ltr(`(${r}, ${c})`);
  const playRow = (n) =>
    `<div class="ex-controls"><button type="button" class="md-button ex-start">להתחלה</button><button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
    `<button type="button" class="md-button md-button--primary ex-play">הפעלה</button><button type="button" class="md-button ex-next">הצעד הבא</button>` +
    `<button type="button" class="md-button ex-end">עד הסוף</button>${speedSel(...n)}<span class="ex-pos" aria-live="off"></span></div>`;

  // Part a's box: the columns as stacks of cells, water in the columns done so far, the
  // two pointers under them, and the table of the two-arrays solution beside the run.
  const rowView = (box) => {
    const h0 = rowParse(box.dataset.heights || "") || [3, 0, 2, 0, 4];
    const st = { h: h0.slice(), k: 0, focus: 0 };
    box.innerHTML =
      `<div class="ex-controls"><label>עמודות <input type="number" class="ex-num rw-n" min="1" max="${ROW_MAX}" step="1" value="${h0.length}" dir="ltr" aria-label="מספר העמודות, עד ${ROW_MAX}"></label>` +
      `<button type="button" class="md-button md-button--primary rw-rand">מערך אקראי</button></div>` +
      playRow([700, 300, 80]) +
      `<p class="ex-summary rw-sum" aria-live="polite"></p>` +
      `<span class="viz-legend"><span><i class="rw-key-ground"></i>עמוד</span><span><i class="rw-key-water"></i>מים שחושבו</span><span><i class="rw-key-cur"></i>העמודה של הצעד</span></span>` +
      `<p class="rw-edit-hint">לחיצה על משבצת קובעת את גובה העמודה עד אליה (לחיצה על הראש מנמיכה ב-1). במקלדת${NB}: חיצים ימינה ושמאלה בין העמודות, למעלה ולמטה משנים גובה.</p>` +
      `<div class="rw-bars" dir="ltr"></div><div class="rw-ptrs" dir="ltr" aria-hidden="true"></div>` +
      `<div class="rw-table-wrap" dir="ltr" tabindex="0" role="region" aria-label="טבלת maxL, maxR והמים"><table class="rw-table"></table></div>` +
      `<p class="rw-step" aria-live="polite"></p><p class="rw-code"></p>`;
    const $ = (s) => box.querySelector(s);
    const play = $(".ex-play"), speed = $(".ex-speed");
    let trace = null;
    const retrace = () => { trace = rwRow(st.h); };
    const draw = () => {
      const n = st.h.length, T = trace.steps.length;
      st.k = Math.min(Math.max(0, st.k), T);
      const done = st.k === T, ev = st.k ? trace.steps[st.k - 1] : null;
      // the pointers after the step: the side that moved has moved
      const l = ev ? (ev.left ? ev.l + 1 : ev.l) : 0, r = ev ? (ev.left ? ev.r : ev.r - 1) : n - 1;
      const doneCol = (i) => done || i < l || i > r;
      const rows = Math.max(4, Math.min(H_MAX, Math.max(...st.h) + 1));
      let g = "";
      for (let i = 0; i < n; i++) {
        const wat = doneCol(i) ? trace.water[i] : 0, cur = ev && !done && ev.i === i;
        g += `<div class="rw-col${cur ? " is-cur" : ""}" data-i="${i}" tabindex="${st.focus === i ? 0 : -1}" role="slider" aria-orientation="vertical" ` +
          `aria-valuemin="0" aria-valuemax="${H_MAX}" aria-valuenow="${st.h[i]}" aria-label="עמודה ${i}, גובה ${st.h[i]}${wat ? `, מים ${wat}` : ""}">`;
        for (let y = rows; y >= 1; y--) {
          const cls = y <= st.h[i] ? " is-ground" : y <= st.h[i] + wat ? " is-water" : "";
          g += `<div class="rw-cell${cls}" data-y="${y}"></div>`;
        }
        g += `<div class="rw-idx">${i}</div></div>`;
      }
      const bars = $(".rw-bars");
      const had = box.contains(document.activeElement) && document.activeElement.classList.contains("rw-col");
      bars.style.setProperty("--n", n);
      bars.innerHTML = g;
      if (had) { const f = bars.querySelector('[tabindex="0"]'); if (f) f.focus({ preventScroll: true }); }
      const ptr = $(".rw-ptrs");
      ptr.style.setProperty("--n", n);
      ptr.innerHTML = done ? "" : Array.from({ length: n }, (_, i) => `<span>${i === l && i === r ? "l r" : i === l ? "l" : i === r ? "r" : ""}</span>`).join("");
      const tr = (name, vals, cls = () => "") => `<tr><th scope="row">${name}</th>${vals.map((v, i) => `<td class="${cls(i)}">${v}</td>`).join("")}</tr>`;
      const curCls = (i) => (ev && !done && ev.i === i ? "is-cur" : "");
      $(".rw-table").innerHTML = tr("i", st.h.map((_, i) => i)) + tr("height", st.h, curCls) + tr("maxL", trace.maxL, curCls) + tr("maxR", trace.maxR, curCls) +
        tr("water", st.h.map((_, i) => (doneCol(i) ? trace.water[i] : "")), (i) => `${curCls(i)}${doneCol(i) && trace.water[i] ? " is-water" : ""}`);
      let step = "", codeLine = "";
      if (!T) step = "בעמודה אחת אין מים, ואין צעדים.";
      else if (!ev) step = `לוחצים על "הצעד הבא" או "הפעלה"${NB}: ${ltr("l = 0")} ו-${ltr(`r = ${n - 1}`)}, ושני המקסימומים 0.`;
      else {
        const side = ev.left ? "l" : "r", mx = ev.left ? "left_max" : "right_max";
        step = `משווים ${ltr(`height[${ev.l}] = ${st.h[ev.l]} ${ev.left ? "&lt;" : "≥"} height[${ev.r}] = ${st.h[ev.r]}`)}, ולכן מזיזים את ${ltr(side)}${NB}: ` +
          `${ltr(`${mx} = ${ev.left ? ev.lm : ev.rm}`)}, ובעמודה ${ltr(ev.i)} נשארים ${ltr(`${ev.left ? ev.lm : ev.rm} − ${st.h[ev.i]} = ${ev.w}`)}.`;
        codeLine = `המשתנים אחרי הצעד${NB}: ${ltr(`l = ${l}, r = ${r}, left_max = ${ev.lm}, right_max = ${ev.rm}, water = ${ev.total}`)}` +
          (done ? `. המצביעים נפגשו בעמודה ${ltr(l)}, הגבוהה ביותר, ומעליה אין מים.` : "");
      }
      $(".rw-step").innerHTML = step;
      $(".rw-code").innerHTML = codeLine;
      $(".ex-pos").textContent = `צעד ${st.k} מתוך ${T}`;
      $(".rw-sum").innerHTML = `${ltr(n)} עמודות, הגבוהה בגובה ${ltr(Math.max(...st.h))}. צעד לכל הזזה של מצביע, ${ltr(T)} צעדים.`;
      answer(box, done ? `נשארות ${ltr(trace.total)} יחידות מים.` : null, ".rw-table tr:last-child td.is-water");
      $(".rw-n").value = n;
    };
    const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= trace.steps.length, restart: () => { st.k = 0; draw(); } });
    const edited = () => { stop(); st.k = 0; retrace(); draw(); };
    $(".rw-n").addEventListener("input", () => {
      const n = Math.min(ROW_MAX, Math.max(1, Math.round(Number($(".rw-n").value)) || 1));
      st.h = Array.from({ length: n }, (_, i) => st.h[i] || 0);
      st.focus = Math.min(st.focus, n - 1);
      edited();
    });
    const seed = seedControls(box, $(".rw-rand"), (rng) => { st.h = st.h.map(() => Math.floor(rng() * 7)); edited(); });
    $(".rw-rand").addEventListener("click", () => seed.draw());
    $(".ex-next").addEventListener("click", () => { stop(); st.k++; draw(); });
    $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
    $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
    $(".ex-end").addEventListener("click", () => { stop(); st.k = trace.steps.length; draw(); });
    const bars = $(".rw-bars");
    bars.addEventListener("click", (e) => {
      const cell = e.target.closest(".rw-cell"), col = e.target.closest(".rw-col");
      if (!col) return;
      const i = Number(col.dataset.i);
      st.focus = i;
      if (cell) { const y = Number(cell.dataset.y); st.h[i] = st.h[i] === y ? y - 1 : y; }
      edited();
    });
    bars.addEventListener("keydown", (e) => {
      const col = e.target.closest(".rw-col");
      if (!col) return;
      const i = Number(col.dataset.i), n = st.h.length;
      const move = { ArrowLeft: -1, ArrowRight: 1 }[e.key], up = { ArrowUp: 1, ArrowDown: -1 }[e.key];
      if (!move && !up) return;
      e.preventDefault();
      e.stopPropagation();                          // the box's own arrows step the run
      if (move) { st.focus = Math.min(n - 1, Math.max(0, i + move)); draw(); }
      else { st.h[i] = Math.min(H_MAX, Math.max(0, st.h[i] + up)); edited(); }
      const f = bars.querySelector('[tabindex="0"]');
      if (f) f.focus({ preventScroll: true });
    });
    // the link and the remembered state: the heights and the step, "3,0,2,0,4-2"
    box.dvqExtra = {
      get: () => `${st.h.join(",")}${st.k ? `-${st.k}` : ""}`,
      set: (text) => {
        const m = /^([\d,]+)(?:-(\d+))?$/.exec(text), h = m && rowParse(m[1]);
        if (!h) return false;
        stop();
        st.h = h;
        st.focus = 0;
        retrace();
        st.k = m[2] ? Number(m[2]) : 0;
        draw();
        return true;
      },
    };
    retrace();
    draw();
  };

  // Part b's box: the map as a grid of heights, shaded by height; water in blue by depth
  // with its depth; the heap's cells outlined, the popped cell framed and the cells it
  // filled marked; the heap in order beside the map.
  const mapView = (box) => {
    const h0 = rwParse(box.dataset.map || "") || [[3, 3, 3], [3, 0, 3], [3, 3, 3]];
    const st = { h: h0.map((r) => r.slice()), k: 0, focus: [0, 0] };
    box.innerHTML =
      `<div class="ex-controls"><label>שורות <input type="number" class="ex-num rw-m" min="1" max="${MAP_MAX}" step="1" value="${h0.length}" dir="ltr" aria-label="מספר השורות, עד ${MAP_MAX}"></label>` +
      `<label>עמודות <input type="number" class="ex-num rw-n" min="1" max="${MAP_MAX}" step="1" value="${h0[0].length}" dir="ltr" aria-label="מספר העמודות, עד ${MAP_MAX}"></label>` +
      `<button type="button" class="md-button md-button--primary rw-rand">מפה אקראית</button></div>` +
      playRow([900, 350, 100]) +
      `<p class="ex-summary rw-sum" aria-live="polite"></p>` +
      `<span class="viz-legend"><span><i class="rw-key-heap"></i>בערימה (הגבול)</span><span><i class="rw-key-cur"></i>יצא מהערימה</span><span><i class="rw-key-fill"></i>השכנים שהגיע אליהם</span><span><i class="rw-key-water"></i>מים</span></span>` +
      `<p class="rw-edit-hint">לחיצה על תא מעלה את הגובה שלו ב-1 (אחרי 9 חוזרים ל-0). במקלדת${NB}: חיצים בין התאים, ספרה קובעת גובה.</p>` +
      `<div class="rw-panels"><figure class="rw-panel"><figcaption>המפה${NB}: גובה, ו-${ltr("+")} מים</figcaption><div class="rw-map" role="grid" dir="ltr"></div></figure>` +
      `<figure class="rw-panel rw-heap-panel"><figcaption>הערימה, מהנמוך לגבוה</figcaption><ol class="rw-heap" dir="ltr"></ol></figure></div>` +
      `<p class="rw-step" aria-live="polite"></p><p class="rw-code"></p>`;
    const $ = (s) => box.querySelector(s);
    const play = $(".ex-play"), speed = $(".ex-speed");
    let trace = null;
    const retrace = () => { trace = rwMap(st.h); };
    const draw = () => {
      const m = st.h.length, n = st.h[0].length, T = trace.steps.length;
      st.k = Math.min(Math.max(0, st.k), T);
      const done = st.k === T, ev = st.k ? trace.steps[st.k - 1] : null, live = ev && !done ? ev : null;
      // the state after k pops: the water so far, the cells reached and the heap
      const wat = st.h.map((r) => r.map(() => null)), border = (i, j) => i === 0 || i === m - 1 || j === 0 || j === n - 1;
      for (let s = 0; s < st.k; s++) for (const f of trace.steps[s].fills) wat[f.r][f.c] = f.w;
      const heap = ev ? ev.heap : st.h.flatMap((r, i) => r.map((v, j) => [v, i, j])).filter(([, i, j]) => border(i, j)).sort((a, b) => a[0] - b[0] || a[1] - b[1] || a[2] - b[2]);
      const inHeap = new Set(heap.map(([, i, j]) => `${i},${j}`));
      const filled = new Set(live ? live.fills.map((f) => `${f.r},${f.c}`) : []);
      const had = box.contains(document.activeElement) && document.activeElement.classList.contains("rw-mcell");
      let g = "";
      for (let i = 0; i < m; i++) {
        g += `<div role="row" class="rw-r">`;
        for (let j = 0; j < n; j++) {
          const v = st.h[i][j], w = wat[i][j], f = st.focus[0] === i && st.focus[1] === j;
          const cls = `${!done && inHeap.has(`${i},${j}`) ? " is-heap" : ""}${live && live.r === i && live.c === j ? " is-cur" : ""}${filled.has(`${i},${j}`) ? " is-fill" : ""}${w ? " is-water" : ""}`;
          g += `<div role="gridcell" class="rw-mcell${cls}" style="--hgt:${v};--dep:${w || 0}" data-r="${i}" data-c="${j}" tabindex="${f ? 0 : -1}" ` +
            `aria-label="שורה ${i}, עמודה ${j}${NB}: גובה ${v}${w ? `, מים ${w}` : ""}"><span class="rw-h">${v}</span>${w ? `<span class="rw-w">+${w}</span>` : ""}</div>`;
        }
        g += `</div>`;
      }
      const map = $(".rw-map");
      map.style.setProperty("--n", n);
      map.innerHTML = g;
      if (had) { const f = map.querySelector('[tabindex="0"]'); if (f) f.focus({ preventScroll: true }); }
      const SHOW = 10;
      $(".rw-heap").innerHTML = done ? `<li class="rw-heap-empty">ריקה</li>` :
        heap.slice(0, SHOW).map(([lv, i, j], x) => `<li${x === 0 ? ' class="is-next"' : ""}>(${lv}, ${i}, ${j})</li>`).join("") + (heap.length > SHOW ? `<li class="rw-heap-more">ועוד ${heap.length - SHOW}</li>` : "");
      let step = "", codeLine = "";
      if (!ev) step = `לוחצים על "הצעד הבא" או "הפעלה"${NB}: תאי השפה בערימה, ${ltr(heap.length)} תאים, והראשון שייצא הוא ${heap.length ? P(heap[0][1], heap[0][2]) : ""}.`;
      else {
        const parts = ev.fills.map((f) => (f.w ? `${P(f.r, f.c)} בגובה ${ltr(f.h)} מתמלא ב-${ltr(f.w)} ונכנס בגובה ${ltr(ev.level)}` : `${P(f.r, f.c)} בגובה ${ltr(f.h)} לא מתמלא ונכנס בגובה ${ltr(f.h)}`));
        step = `יוצא מהערימה ${P(ev.r, ev.c)} בגובה ${ltr(ev.level)}. ` +
          (parts.length ? `${parts.length > 1 ? "השכנים החדשים" : "השכן החדש"}${NB}: ${parts.join("; ")}.` : "אין לו שכנים שעוד לא נבדקו.");
        codeLine = `עד עכשיו ${ltr(`water = ${ev.total}`)}, ובערימה ${ltr(ev.heap.length)} תאים.`;
      }
      $(".rw-step").innerHTML = step;
      $(".rw-code").innerHTML = codeLine;
      $(".ex-pos").textContent = `צעד ${st.k} מתוך ${T}`;
      $(".rw-sum").innerHTML = `מפה ${ltr(`${m} × ${n}`)}, גבהים עד ${ltr(Math.max(...st.h.flat()))}. צעד לכל הוצאה מהערימה, ${ltr(T)} צעדים.`;
      answer(box, done ? `נשארות ${ltr(trace.total)} יחידות מים.` : null);
    };
    const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= trace.steps.length, restart: () => { st.k = 0; draw(); } });
    const edited = () => { stop(); st.k = 0; retrace(); draw(); };
    const resize = () => {
      const m = Math.min(MAP_MAX, Math.max(1, Math.round(Number($(".rw-m").value)) || 1));
      const n = Math.min(MAP_MAX, Math.max(1, Math.round(Number($(".rw-n").value)) || 1));
      st.h = Array.from({ length: m }, (_, i) => Array.from({ length: n }, (_, j) => (st.h[i] && st.h[i][j]) || 0));
      st.focus = [Math.min(st.focus[0], m - 1), Math.min(st.focus[1], n - 1)];
      edited();
    };
    $(".rw-m").addEventListener("input", resize);
    $(".rw-n").addEventListener("input", resize);
    const seed = seedControls(box, $(".rw-rand"), (rng) => { st.h = st.h.map((r) => r.map(() => Math.floor(rng() * (H_MAX + 1)))); edited(); });
    $(".rw-rand").addEventListener("click", () => seed.draw());
    $(".ex-next").addEventListener("click", () => { stop(); st.k++; draw(); });
    $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
    $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
    $(".ex-end").addEventListener("click", () => { stop(); st.k = trace.steps.length; draw(); });
    const map = $(".rw-map");
    map.addEventListener("click", (e) => {
      const el = e.target.closest(".rw-mcell");
      if (!el) return;
      const r = Number(el.dataset.r), c = Number(el.dataset.c);
      st.focus = [r, c];
      st.h[r][c] = (st.h[r][c] + 1) % (H_MAX + 1);
      edited();
    });
    map.addEventListener("keydown", (e) => {
      const el = e.target.closest(".rw-mcell");
      if (!el) return;
      const m = st.h.length, n = st.h[0].length, r = Number(el.dataset.r), c = Number(el.dataset.c);
      const move = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[e.key];
      if (move) {
        e.preventDefault();
        e.stopPropagation();                        // the box's own arrows step the run
        st.focus = [Math.min(m - 1, Math.max(0, r + move[0])), Math.min(n - 1, Math.max(0, c + move[1]))];
        draw();
      } else if (/^\d$/.test(e.key)) {
        e.preventDefault();
        e.stopPropagation();
        st.h[r][c] = Number(e.key);
        edited();
      } else return;
      const f = map.querySelector('[tabindex="0"]');
      if (f) f.focus({ preventScroll: false });
    });
    // the link and the remembered state: the map and the step, "33333.31113-4"
    box.dvqExtra = {
      get: () => `${rwText(st.h)}${st.k ? `-${st.k}` : ""}`,
      set: (text) => {
        const m = /^([\d.]+)(?:-(\d+))?$/.exec(text), h = m && rwParse(m[1]);
        if (!h) return false;
        stop();
        st.h = h;
        st.focus = [0, 0];
        $(".rw-m").value = h.length;
        $(".rw-n").value = h[0].length;
        retrace();
        st.k = m[2] ? Number(m[2]) : 0;
        draw();
        return true;
      },
    };
    retrace();
    draw();
  };

  dvqExplorers.register({
    views: { rainwater: () => ({ mount: (box) => (box.dataset.mode === "map" ? mapView(box) : rowView(box)) }) },
    help: {
      rainwater: "בשורה : לוחצים על משבצת כדי לקבוע את גובה העמודה, ומריצים את שני המצביעים צעד אחרי צעד : הצד הנמוך זז, והמים של העמודה שלו נקבעים. הטבלה מראה את maxL, ‏maxR והמים של כל עמודה. במפה : לחיצה על תא מעלה את הגובה שלו, וכל צעד מוציא מהערימה את התא הנמוך בגבול וממלא את השכנים החדשים שלו עד הגובה שלו.",
    },
    models: { rwRow, rwMap, rwParse, rwText },
  });
})();
