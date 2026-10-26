// kinds: rainwater
//   rainwater              0047        part a (data-mode="row"): up to 24 columns with heights 0 to 20 (a tap on a cell sets the column's height, a drag selects columns for a value or ±1, digits typed on a column, a double tap edits it in place, the values as text, a random fill up to a chosen height), the two pointers of the page's trap played a move at a time with left_max and right_max, the water of every column done so far, and a table of maxL, maxR and the water per column; part b (data-mode="map"): a height map up to 10 × 10 with the same editing (a drag selects a rectangle), the page's trap_2d played a pop at a time: the boundary in the heap outlined, the popped cell framed, the neighbours it fills, the water by depth and the heap in order. Both can show the final result only, which every edit keeps.
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, gridText, ltr, parseGrid, seedControls, speedSel, viewSel } = dvqExplorers.lib;
  const NB = " ";
  const ROW_MAX = 24, MAP_MAX = 10, H_MAX = 20, TYPE_MS = 900;

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

  // the link's text: the map's rows split by ".", the heights by ","; a row is one such row
  const rwParse = (text) => {
    if (!/^\d+(,\d+)*(\.\d+(,\d+)*)*$/.test(text)) return null;
    const g = text.split(".").map((r) => r.split(",").map(Number));
    if (g.length > MAP_MAX || g[0].length > MAP_MAX || g.some((r) => r.length !== g[0].length || r.some((v) => v > H_MAX))) return null;
    return g;
  };
  const rwText = (h) => h.map((r) => r.join(",")).join(".");
  const rowParse = (text) => {
    if (!/^\d+(,\d+)*$/.test(text)) return null;
    const h = text.split(",").map(Number);
    return h.length <= ROW_MAX && h.every((v) => v <= H_MAX) ? h : null;
  };

  const P = (r, c) => ltr(`(${r}, ${c})`);
  const playRow = (n) =>
    `<div class="ex-controls rw-play"><button type="button" class="md-button ex-start">להתחלה</button><button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
    `<button type="button" class="md-button md-button--primary ex-play">הפעלה</button><button type="button" class="md-button ex-next">הצעד הבא</button>` +
    `<button type="button" class="md-button ex-end">עד הסוף</button>${speedSel(...n)}<span class="ex-pos" aria-live="off"></span></div>`;
  // the editing rows fold under one title (closed on a phone, see core.js); the view
  // select stays out, after them, so the link keeps its controls in the same order
  const editRows = (map, m) =>
    `<div class="ex-fold"><p class="ex-fold-title">עריכת ${map ? "המפה" : "המערך"}</p><div class="ex-controls"><label>${map ? "שורות" : "עמודות"} <input type="number" class="ex-num ${map ? "rw-m" : "rw-n"}" min="1" max="${map ? MAP_MAX : ROW_MAX}" step="1" dir="ltr" aria-label="מספר ה${map ? "שורות" : "עמודות"}, עד ${map ? MAP_MAX : ROW_MAX}"></label>` +
    (map ? `<label>עמודות <input type="number" class="ex-num rw-n" min="1" max="${MAP_MAX}" step="1" dir="ltr" aria-label="מספר העמודות, עד ${MAP_MAX}"></label>` : "") +
    `<label>גובה מרבי <input type="number" class="ex-num rw-top" min="1" max="${H_MAX}" step="1" value="9" dir="ltr" data-nolink aria-label="הגובה המרבי במילוי האקראי, עד ${H_MAX}"></label>` +
    `<button type="button" class="md-button md-button--primary rw-rand">${map ? "מפה אקראית" : "מערך אקראי"}</button></div>` +
    `<div class="ex-controls"><label>ערך <input type="number" class="ex-num rw-val" min="0" max="${H_MAX}" step="1" value="0" dir="ltr" data-nolink aria-label="ערך לכל הסימון, 0 עד ${H_MAX}"></label>` +
    `<button type="button" class="md-button rw-set" disabled>החלה על הסימון</button><button type="button" class="md-button rw-inc" disabled aria-label="הגדלה ב-1 של הסימון">+1</button>` +
    `<button type="button" class="md-button rw-dec" disabled aria-label="הקטנה ב-1 של הסימון">−1</button></div>` +
    `<div class="ex-controls rw-textrow"><label class="rw-textlab">הערכים ${map ? `<textarea class="rw-text" rows="${m}" dir="ltr" spellcheck="false" data-nolink aria-label="המפה כטקסט, שורה בכל שורה"></textarea>`
      : `<input type="text" class="rw-text" dir="ltr" spellcheck="false" data-nolink aria-label="הגבהים כטקסט, מופרדים בפסיקים">`}</label>` +
    `<button type="button" class="md-button rw-apply">עדכון מהטקסט</button><span class="rw-err" role="status"></span></div></div>` +
    `<div class="ex-controls">${viewSel()}</div>`;

  // What the two boxes share: the final-result switch, the selection and the value
  // buttons, the text field, digits typed on a cell (two digits within TYPE_MS make one
  // number) and the in-place editor. The view keeps st.h (a row is one row of a grid),
  // st.sel and st.focus, and st.cells(), the cells of the selection or the focus.
  const editing = (box, st, { row, retrace, draw, total, stop }) => {
    const $ = (s) => box.querySelector(s);
    const clamp = (v) => Math.min(H_MAX, Math.max(0, v));
    const grid = () => (row ? [st.h] : st.h);
    const edited = (fromText = false) => {
      stop();
      retrace();
      st.k = st.final ? total() : 0;
      if (!fromText) {
        const t = $(".rw-text");
        if (document.activeElement !== t) t.value = gridText(grid(), row);
        $(".rw-err").textContent = "";
      }
      if (!row) $(".rw-text").rows = st.h.length;
      draw();
    };
    const setCells = (f) => {
      for (const [r, c] of st.cells()) {
        if (row) st.h[c] = clamp(f(st.h[c])); else st.h[r][c] = clamp(f(st.h[r][c]));
      }
      edited();
    };
    $(".rw-set").addEventListener("click", () => { const v = clamp(Math.round(Number($(".rw-val").value)) || 0); setCells(() => v); });
    $(".rw-inc").addEventListener("click", () => setCells((v) => v + 1));
    $(".rw-dec").addEventListener("click", () => setCells((v) => v - 1));
    const apply = () => {
      const g = parseGrid($(".rw-text").value, { max: H_MAX, rows: row ? 1 : MAP_MAX, cols: row ? ROW_MAX : MAP_MAX, row });
      if (typeof g === "string") { $(".rw-err").textContent = g; return; }
      $(".rw-err").textContent = "";
      st.h = row ? g[0] : g;
      st.sel = null;
      st.focus = row ? Math.min(st.focus, st.h.length - 1) : [Math.min(st.focus[0], g.length - 1), Math.min(st.focus[1], g[0].length - 1)];
      edited(true);
    };
    $(".rw-apply").addEventListener("click", apply);
    $(".rw-text").addEventListener("change", apply);
    $(".rw-text").addEventListener("keydown", (e) => {
      e.stopPropagation();
      if (e.key === "Enter" && (row || e.ctrlKey || e.metaKey)) { e.preventDefault(); apply(); }
    });
    $(".ex-view").addEventListener("change", () => {
      st.final = $(".ex-view").value === "final";
      box.classList.toggle("ex-final", st.final);
      stop();
      if (st.final) st.k = total();
      draw();
    });
    let typed = { at: 0, v: 0 };
    const typeDigit = (d) => {
      const now = Date.now(), v = now - typed.at < TYPE_MS && typed.v * 10 + d <= H_MAX ? typed.v * 10 + d : d;
      typed = { at: now, v };
      setCells(() => v);
    };
    // the in-place editor: a number field over the cell (or under the column), committed
    // by Enter or by leaving it, dropped by Escape
    const inline = (host, value, commit) => {
      stop();
      const input = document.createElement("input");
      Object.assign(input, { type: "number", min: 0, max: H_MAX, step: 1, value, className: "rw-inline" });
      input.setAttribute("dir", "ltr");
      input.setAttribute("data-nolink", "");
      input.setAttribute("aria-label", `ערך חדש, 0 עד ${H_MAX}`);
      host.replaceChildren(input);
      input.focus();
      input.select();
      let done = false;
      const end = (ok) => {
        if (done) return;
        done = true;
        const v = Math.round(Number(input.value));
        if (ok && input.value !== "" && v >= 0 && v <= H_MAX) commit(v); else draw();
        const f = box.querySelector('.rw-col[tabindex="0"], .rw-mcell[tabindex="0"]');
        if (f) f.focus({ preventScroll: true });
      };
      input.addEventListener("keydown", (e) => {
        e.stopPropagation();
        if (e.key === "Enter") { e.preventDefault(); end(true); } else if (e.key === "Escape") { e.preventDefault(); end(false); }
      });
      input.addEventListener("blur", () => end(true));
      input.addEventListener("pointerdown", (e) => e.stopPropagation());
      input.addEventListener("click", (e) => e.stopPropagation());
      input.addEventListener("dblclick", (e) => e.stopPropagation());
    };
    const paintSel = () => { $(".rw-set").disabled = $(".rw-inc").disabled = $(".rw-dec").disabled = !st.sel; };
    // in the final view the steps stay at the end
    const guardStep = (f) => () => { if (!st.final) { stop(); f(); draw(); } };
    $(".ex-next").addEventListener("click", guardStep(() => { st.k++; }));
    $(".ex-prev").addEventListener("click", guardStep(() => { st.k--; }));
    $(".ex-start").addEventListener("click", guardStep(() => { st.k = 0; }));
    $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
    return { edited, typeDigit, inline, paintSel, clamp };
  };

  // Part a's box: the columns as stacks of cells, water in the columns done so far, the
  // two pointers under them, and the table of the two-arrays solution beside the run.
  const rowView = (box) => {
    const h0 = rowParse(box.dataset.heights || "") || [3, 0, 2, 0, 4];
    const st = { h: h0.slice(), k: 0, focus: 0, sel: null, final: false };
    st.cells = () => (st.sel ? Array.from({ length: Math.abs(st.sel[1] - st.sel[0]) + 1 }, (_, x) => [0, Math.min(...st.sel) + x]) : [[0, st.focus]]);
    box.innerHTML = editRows(false) + playRow([700, 300, 80]) +
      `<p class="ex-summary rw-sum" aria-live="polite"></p>` +
      `<span class="viz-legend"><span><i class="rw-key-ground"></i>עמוד</span><span><i class="rw-key-water"></i>מים שחושבו</span><span><i class="rw-key-cur"></i>העמודה של הצעד</span><span><i class="rw-key-sel"></i>מסומן</span></span>` +
      `<p class="rw-edit-hint">לחיצה על משבצת קובעת את גובה העמודה עד אליה, וגרירה מסמנת כמה עמודות. במקלדת${NB}: חיצים ימינה ושמאלה בין העמודות (עם Shift מסמנים), למעלה ולמטה משנים גובה, מספר קובע אותו, ו-Enter או לחיצה כפולה פותחים עריכה.</p>` +
      `<div class="rw-bars" dir="ltr" data-edits></div><div class="rw-ptrs" dir="ltr" aria-hidden="true"></div>` +
      `<div class="rw-table-wrap" dir="ltr" tabindex="0" role="region" aria-label="טבלת maxL, maxR והמים"><table class="rw-table"></table></div>` +
      `<p class="rw-step" aria-live="polite"></p><p class="rw-code"></p>`;
    const $ = (s) => box.querySelector(s);
    const play = $(".ex-play"), speed = $(".ex-speed");
    let trace = null;
    const retrace = () => { trace = rwRow(st.h); };
    const total = () => trace.steps.length;
    const draw = () => {
      const n = st.h.length, T = trace.steps.length;
      st.k = st.final ? T : Math.min(Math.max(0, st.k), T);
      const done = st.k === T, ev = st.k ? trace.steps[st.k - 1] : null;
      // the pointers after the step: the side that moved has moved
      const l = ev ? (ev.left ? ev.l + 1 : ev.l) : 0, r = ev ? (ev.left ? ev.r : ev.r - 1) : n - 1;
      const doneCol = (i) => done || i < l || i > r;
      const rows = Math.max(4, Math.min(H_MAX, Math.max(...st.h)) + 1);
      const inSel = (i) => st.sel && i >= Math.min(...st.sel) && i <= Math.max(...st.sel);
      let g = "";
      for (let i = 0; i < n; i++) {
        const wat = doneCol(i) ? trace.water[i] : 0, cur = ev && !done && ev.i === i;
        g += `<div class="rw-col${cur ? " is-cur" : ""}${inSel(i) ? " is-sel" : ""}" data-i="${i}" tabindex="${st.focus === i ? 0 : -1}" role="slider" aria-orientation="vertical" ` +
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
      bars.style.setProperty("--rows", rows);
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
      $(".rw-sum").innerHTML = `${ltr(n)} עמודות, הגבוהה בגובה ${ltr(Math.max(...st.h))}. ` +
        (st.final ? "מוצגת התוצאה הסופית, וכל עריכה מחשבת אותה מחדש." : `צעד לכל הזזה של מצביע, ${ltr(T)} צעדים.`);
      answer(box, done ? `נשארות ${ltr(trace.total)} יחידות מים.` : null, ".rw-table tr:last-child td.is-water");
      if (document.activeElement !== $(".rw-n")) $(".rw-n").value = n;
      ed.paintSel();
    };
    const stop = autoplay(play, speed, { step: () => { if (!st.final) st.k++; draw(); }, done: () => st.final || st.k >= total(), restart: () => { st.k = st.final ? total() : 0; draw(); } });
    const ed = editing(box, st, { row: true, retrace, draw, total, stop });
    $(".rw-n").addEventListener("input", () => {
      const n = Math.min(ROW_MAX, Math.max(1, Math.round(Number($(".rw-n").value)) || 1));
      st.h = Array.from({ length: n }, (_, i) => st.h[i] || 0);
      st.focus = Math.min(st.focus, n - 1);
      st.sel = null;
      ed.edited();
    });
    const seed = seedControls(box, $(".rw-rand"), (rng) => {
      const top = ed.clamp(Math.round(Number($(".rw-top").value)) || 9);
      st.h = st.h.map(() => Math.floor(rng() * (top + 1)));
      st.sel = null;
      ed.edited();
    });
    $(".rw-rand").addEventListener("click", () => seed.draw());
    // a tap sets the height up to the tapped cell (the top cell lowers by 1); a drag
    // across columns selects them
    const bars = $(".rw-bars");
    const colAt = (e) => { const el = document.elementFromPoint(e.clientX, e.clientY); return el && el.closest(".rw-bars .rw-col"); };
    let drag = null;
    bars.addEventListener("pointerdown", (e) => {
      const col = e.target.closest(".rw-col");
      if (!col || e.button > 0 || e.target.closest(".rw-inline")) return;
      e.preventDefault();
      const cell = e.target.closest(".rw-cell");
      drag = { i: Number(col.dataset.i), y: cell ? Number(cell.dataset.y) : null, moved: false };
      st.focus = drag.i;
      bars.setPointerCapture(e.pointerId);
    });
    bars.addEventListener("pointermove", (e) => {
      if (!drag) return;
      const col = colAt(e);
      if (!col) return;
      const i = Number(col.dataset.i);
      if (!drag.moved && i === drag.i) return;
      drag.moved = true;
      if (!st.sel || st.sel[1] !== i || st.sel[0] !== drag.i) { st.sel = [drag.i, i]; draw(); }
    });
    const endDrag = (e) => {
      if (!drag) return;
      const d = drag;
      drag = null;
      if (bars.hasPointerCapture(e.pointerId)) bars.releasePointerCapture(e.pointerId);
      if (d.moved || e.type !== "pointerup") return;
      st.sel = null;
      if (d.y !== null) st.h[d.i] = st.h[d.i] === d.y ? d.y - 1 : d.y;
      ed.edited();
    };
    bars.addEventListener("pointerup", endDrag);
    bars.addEventListener("pointercancel", endDrag);
    const editAt = (i) => {
      const idx = bars.querySelector(`.rw-col[data-i="${i}"] .rw-idx`);
      if (idx) ed.inline(idx, st.h[i], (v) => { st.h[i] = v; ed.edited(); });
    };
    // (the pointer capture of a tap makes the bars the double tap's target: find the column under it)
    bars.addEventListener("dblclick", (e) => { const col = e.target.closest(".rw-col") || colAt(e); if (col && !e.target.closest(".rw-inline")) editAt(Number(col.dataset.i)); });
    bars.addEventListener("keydown", (e) => {
      const col = e.target.closest(".rw-col");
      if (!col || e.target.closest(".rw-inline")) return;
      const i = Number(col.dataset.i), n = st.h.length;
      const move = { ArrowLeft: -1, ArrowRight: 1 }[e.key], up = { ArrowUp: 1, ArrowDown: -1 }[e.key];
      if (move) {
        const j = Math.min(n - 1, Math.max(0, i + move));
        st.sel = e.shiftKey ? [st.sel ? st.sel[0] : i, j] : null;
        st.focus = j;
        draw();
      } else if (up) { st.h[i] = ed.clamp(st.h[i] + up); ed.edited(); }
      else if (/^\d$/.test(e.key)) { if (st.sel && !st.cells().some(([, c]) => c === i)) st.sel = null; ed.typeDigit(Number(e.key)); }
      else if (e.key === "Enter") editAt(i);
      else if (e.key === "Escape" && st.sel) { st.sel = null; draw(); }
      else return;
      e.preventDefault();
      e.stopPropagation();                          // the box's own arrows step the run
      const f = bars.querySelector('[tabindex="0"]');
      if (f && e.key !== "Enter") f.focus({ preventScroll: true });
    });
    // the link and the remembered state: the heights and the step, "3,0,2,0,4-2"
    box.dvqExtra = {
      get: () => `${st.h.join(",")}${st.k ? `-${st.k}` : ""}`,
      set: (text) => {
        const mm = /^([\d,]+)(?:-(\d+))?$/.exec(text), h = mm && rowParse(mm[1]);
        if (!h) return false;
        st.h = h;
        st.focus = 0;
        st.sel = null;
        ed.edited();
        if (!st.final) st.k = mm[2] ? Number(mm[2]) : 0;
        draw();
        return true;
      },
    };
    retrace();
    ed.edited();
  };

  // Part b's box: the map as a grid of heights, shaded by height; water in blue by depth
  // with its depth; the heap's cells outlined, the popped cell framed and the cells it
  // filled marked; the heap in order beside the map.
  const mapView = (box) => {
    const h0 = rwParse(box.dataset.map || "") || [[3, 3, 3], [3, 0, 3], [3, 3, 3]];
    const st = { h: h0.map((r) => r.slice()), k: 0, focus: [0, 0], sel: null, final: false };
    st.cells = () => {
      if (!st.sel) return [st.focus];
      const [r0, c0, r1, c1] = st.sel, out = [];
      for (let r = Math.min(r0, r1); r <= Math.max(r0, r1); r++) for (let c = Math.min(c0, c1); c <= Math.max(c0, c1); c++) out.push([r, c]);
      return out;
    };
    box.innerHTML = editRows(true, h0.length) + playRow([900, 350, 100]) +
      `<p class="ex-summary rw-sum" aria-live="polite"></p>` +
      `<span class="viz-legend"><span><i class="rw-key-heap"></i>בערימה (הגבול)</span><span><i class="rw-key-cur"></i>יצא מהערימה</span><span><i class="rw-key-fill"></i>השכנים שהגיע אליהם</span><span><i class="rw-key-water"></i>מים</span><span><i class="rw-key-sel"></i>מסומן</span></span>` +
      `<p class="rw-edit-hint">לחיצה על תא מסמנת אותו, וגרירה מסמנת מלבן. מספר שמקלידים נכנס לכל התאים המסומנים, ו-Enter או לחיצה כפולה פותחים עריכה של תא. במקלדת${NB}: חיצים בין התאים, ו-Shift עם חץ מרחיב את הסימון.</p>` +
      `<div class="rw-panels"><figure class="rw-panel"><figcaption>המפה${NB}: גובה, ו-${ltr("+")} מים</figcaption><div class="rw-map" role="grid" dir="ltr" data-edits></div></figure>` +
      `<figure class="rw-panel rw-heap-panel"><figcaption>הערימה, מהנמוך לגבוה : ‏(גובה, שורה, עמודה)</figcaption><ol class="rw-heap" dir="ltr"></ol></figure></div>` +
      `<p class="rw-step" aria-live="polite"></p><p class="rw-code"></p>`;
    const $ = (s) => box.querySelector(s);
    const play = $(".ex-play"), speed = $(".ex-speed");
    let trace = null;
    const retrace = () => { trace = rwMap(st.h); };
    const total = () => trace.steps.length;
    const draw = () => {
      const m = st.h.length, n = st.h[0].length, T = trace.steps.length;
      st.k = st.final ? T : Math.min(Math.max(0, st.k), T);
      const done = st.k === T, ev = st.k ? trace.steps[st.k - 1] : null, live = ev && !done ? ev : null;
      // the state after k pops: the water so far, the cells reached and the heap
      const wat = st.h.map((r) => r.map(() => null)), border = (i, j) => i === 0 || i === m - 1 || j === 0 || j === n - 1;
      for (let s = 0; s < st.k; s++) for (const f of trace.steps[s].fills) wat[f.r][f.c] = f.w;
      const heap = ev ? ev.heap : st.h.flatMap((r, i) => r.map((v, j) => [v, i, j])).filter(([, i, j]) => border(i, j)).sort((a, b) => a[0] - b[0] || a[1] - b[1] || a[2] - b[2]);
      const inHeap = new Set(heap.map(([, i, j]) => `${i},${j}`));
      const filled = new Set(live ? live.fills.map((f) => `${f.r},${f.c}`) : []);
      const sel = new Set(st.sel ? st.cells().map(([r, c]) => `${r},${c}`) : []);
      const had = box.contains(document.activeElement) && document.activeElement.classList.contains("rw-mcell");
      let g = "";
      for (let i = 0; i < m; i++) {
        g += `<div role="row" class="rw-r">`;
        for (let j = 0; j < n; j++) {
          const v = st.h[i][j], w = wat[i][j], f = st.focus[0] === i && st.focus[1] === j, key = `${i},${j}`;
          const cls = `${!done && inHeap.has(key) ? " is-heap" : ""}${live && live.r === i && live.c === j ? " is-cur" : ""}${filled.has(key) ? " is-fill" : ""}${w ? " is-water" : ""}${sel.has(key) ? " is-sel" : ""}`;
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
      $(".rw-sum").innerHTML = `מפה ${ltr(`${m} × ${n}`)}, גבהים עד ${ltr(Math.max(...st.h.flat()))}. ` +
        (st.final ? "מוצגת התוצאה הסופית, וכל עריכה מחשבת אותה מחדש." : `צעד לכל הוצאה מהערימה, ${ltr(T)} צעדים.`);
      answer(box, done ? `נשארות ${ltr(trace.total)} יחידות מים.` : null);
      if (document.activeElement !== $(".rw-m")) $(".rw-m").value = m;
      if (document.activeElement !== $(".rw-n")) $(".rw-n").value = n;
      ed.paintSel();
    };
    const stop = autoplay(play, speed, { step: () => { if (!st.final) st.k++; draw(); }, done: () => st.final || st.k >= total(), restart: () => { st.k = st.final ? total() : 0; draw(); } });
    const ed = editing(box, st, { row: false, retrace, draw, total, stop });
    const resize = () => {
      const m = Math.min(MAP_MAX, Math.max(1, Math.round(Number($(".rw-m").value)) || 1));
      const n = Math.min(MAP_MAX, Math.max(1, Math.round(Number($(".rw-n").value)) || 1));
      st.h = Array.from({ length: m }, (_, i) => Array.from({ length: n }, (_, j) => (st.h[i] && st.h[i][j]) || 0));
      st.focus = [Math.min(st.focus[0], m - 1), Math.min(st.focus[1], n - 1)];
      st.sel = null;
      ed.edited();
    };
    $(".rw-m").addEventListener("input", resize);
    $(".rw-n").addEventListener("input", resize);
    const seed = seedControls(box, $(".rw-rand"), (rng) => {
      const top = ed.clamp(Math.round(Number($(".rw-top").value)) || 9);
      st.h = st.h.map((r) => r.map(() => Math.floor(rng() * (top + 1))));
      st.sel = null;
      ed.edited();
    });
    $(".rw-rand").addEventListener("click", () => seed.draw());
    // a tap selects a cell, a drag selects a rectangle; the selection is painted in place,
    // so the cell under the pointer stays the same element (a double tap needs that)
    const map = $(".rw-map");
    const paintSel = () => {
      const sel = new Set(st.sel ? st.cells().map(([r, c]) => `${r},${c}`) : []);
      map.querySelectorAll(".rw-mcell").forEach((el) => {
        el.classList.toggle("is-sel", sel.has(`${el.dataset.r},${el.dataset.c}`));
        el.tabIndex = Number(el.dataset.r) === st.focus[0] && Number(el.dataset.c) === st.focus[1] ? 0 : -1;
      });
      ed.paintSel();
    };
    const cellAt = (e) => { const el = document.elementFromPoint(e.clientX, e.clientY); return el && el.closest(".rw-map .rw-mcell"); };
    let drag = null;
    map.addEventListener("pointerdown", (e) => {
      const el = e.target.closest(".rw-mcell");
      if (!el || e.button > 0 || e.target.closest(".rw-inline")) return;
      e.preventDefault();
      const r = Number(el.dataset.r), c = Number(el.dataset.c);
      drag = { r, c };
      st.focus = [r, c];
      st.sel = [r, c, r, c];
      paintSel();
      el.focus({ preventScroll: true });
      map.setPointerCapture(e.pointerId);
    });
    map.addEventListener("pointermove", (e) => {
      if (!drag) return;
      const el = cellAt(e);
      if (!el) return;
      const r = Number(el.dataset.r), c = Number(el.dataset.c);
      if (st.sel[2] !== r || st.sel[3] !== c) { st.sel = [drag.r, drag.c, r, c]; paintSel(); }
    });
    const endDrag = (e) => {
      if (!drag) return;
      drag = null;
      if (map.hasPointerCapture(e.pointerId)) map.releasePointerCapture(e.pointerId);
    };
    map.addEventListener("pointerup", endDrag);
    map.addEventListener("pointercancel", endDrag);
    const editAt = (r, c) => {
      const el = map.querySelector(`.rw-mcell[data-r="${r}"][data-c="${c}"]`);
      if (el) ed.inline(el, st.h[r][c], (v) => { st.h[r][c] = v; ed.edited(); });
    };
    // (the pointer capture of a tap makes the map the double tap's target: find the cell under it)
    map.addEventListener("dblclick", (e) => { const el = e.target.closest(".rw-mcell") || cellAt(e); if (el && !e.target.closest(".rw-inline")) editAt(Number(el.dataset.r), Number(el.dataset.c)); });
    map.addEventListener("keydown", (e) => {
      const el = e.target.closest(".rw-mcell");
      if (!el || e.target.closest(".rw-inline")) return;
      const m = st.h.length, n = st.h[0].length, r = Number(el.dataset.r), c = Number(el.dataset.c);
      const move = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[e.key];
      if (move) {
        const nr = Math.min(m - 1, Math.max(0, r + move[0])), nc = Math.min(n - 1, Math.max(0, c + move[1]));
        st.sel = e.shiftKey ? [st.sel ? st.sel[0] : r, st.sel ? st.sel[1] : c, nr, nc] : null;
        st.focus = [nr, nc];
        draw();
      } else if (/^\d$/.test(e.key)) {
        if (st.sel && !st.cells().some(([a, b]) => a === r && b === c)) st.sel = null;
        ed.typeDigit(Number(e.key));
      } else if (e.key === "Enter") editAt(r, c);
      else if (e.key === "Escape" && st.sel) { st.sel = null; draw(); }
      else return;
      e.preventDefault();
      e.stopPropagation();                          // the box's own arrows step the run
      const f = map.querySelector('[tabindex="0"]');
      if (f && e.key !== "Enter") f.focus({ preventScroll: true });
    });
    // the link and the remembered state: the map and the step, "3,3,3.3,0,3.3,3,3-4"
    box.dvqExtra = {
      get: () => `${rwText(st.h)}${st.k ? `-${st.k}` : ""}`,
      set: (text) => {
        const mm = /^([\d.,]+)(?:-(\d+))?$/.exec(text), h = mm && rwParse(mm[1]);
        if (!h) return false;
        st.h = h;
        st.focus = [0, 0];
        st.sel = null;
        ed.edited();
        if (!st.final) st.k = mm[2] ? Number(mm[2]) : 0;
        draw();
        return true;
      },
    };
    retrace();
    ed.edited();
  };

  dvqExplorers.register({
    views: { rainwater: () => ({ mount: (box) => (box.dataset.mode === "map" ? mapView(box) : rowView(box)) }) },
    help: {
      rainwater: "עורכים את הגבהים : לחיצה, גרירה שמסמנת כמה ערכים יחד (ואז \"ערך\" או ‎+1 ו-‎−1, בקבוצה \"עריכת המערך\"), מספר שמקלידים, לחיצה כפולה לעריכה במקום, או שדה הטקסט שבאותה קבוצה, שאפשר להדביק לתוכו מערך. \"תצוגה\" בוחרת בין צעד אחרי צעד לבין התוצאה הסופית, שנשמרת גם אחרי כל עריכה ומילוי אקראי. בשורה רצים שני המצביעים, ובמפה כל צעד מוציא מהערימה את התא הנמוך בגבול וממלא את השכנים החדשים שלו.",
    },
    models: { rwRow, rwMap, rwParse, rwText },
  });
})();
