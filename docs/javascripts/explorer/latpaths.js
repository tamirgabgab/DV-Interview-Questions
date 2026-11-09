// kinds: latpaths
//   latpaths               0022        the paths from the top-left cell to the bottom-right one (data-grid, rows of 0 and 1 joined by dots, 1 an obstacle; data-dirs "rd" right and down, "rud" right, up and down without a cell twice): every open cell shows the number of paths that end at it, on a tint that grows with it (log scale); a tap or a drag puts or removes obstacles (not on S and T), the rows and the columns from 2 to 10, the directions, a clear board; "a random path" draws one path with every path equally likely (backwards through the counts), and the summary gives the count, the closed form when the board is empty, and the count of the other directions
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, bigComb, ltr } = dvqExplorers.lib;
  const NB = "\u00a0";
  const MINS = 2, MAXS = 10;
  const ARROW = { "0,1": "→", "1,0": "↓", "-1,0": "↑", "0,-1": "←" };

  // --- the models, as tools/figures/q0022.py counts() --------------------------------------

  // "0000010.0100000" -> the rows, or null: 2 to 10 rows of 2 to 10 cells, all the same
  // length, of 0 and 1, with S and T open
  const lpParse = (text) => {
    const rows = String(text).trim().split(".");
    if (rows.length < MINS || rows.length > MAXS) return null;
    const n = rows[0].length;
    if (n < MINS || n > MAXS || rows.some((r) => r.length !== n || !/^[01]+$/.test(r))) return null;
    if (rows[0][0] === "1" || rows[rows.length - 1][n - 1] === "1") return null;
    return rows;
  };
  const blocked = (grid, r, c) => grid[r][c] === "1";
  // what enters column c at each row: the start at row 0 of column 0, else the paths that end
  // at the cell on the left; 0 at an obstacle
  const enterCol = (grid, f, c) => grid.map((row, r) => (blocked(grid, r, c) ? 0n : c === 0 ? (r === 0 ? 1n : 0n) : f[r][c - 1]));
  // the runs of open cells of column c, as [first, last]
  const runsOf = (grid, c) => {
    const out = [];
    for (let r = 0; r < grid.length; r++) {
      if (blocked(grid, r, c)) continue;
      const s = r;
      while (r + 1 < grid.length && !blocked(grid, r + 1, c)) r++;
      out.push([s, r]);
    }
    return out;
  };
  // the number of paths from (0, 0) that end at every cell, as BigInt
  const lpCounts = (grid, up) => {
    const m = grid.length, n = grid[0].length;
    const f = grid.map(() => Array(n).fill(0n));
    for (let c = 0; c < n; c++) {
      const enter = enterCol(grid, f, c);
      if (!up) {
        for (let r = 0; r < m; r++) if (!blocked(grid, r, c)) f[r][c] = enter[r] + (r ? f[r - 1][c] : 0n);
        continue;
      }
      runsOf(grid, c).forEach(([s, e]) => {
        let total = 0n;
        for (let r = s; r <= e; r++) total += enter[r];
        for (let r = s; r <= e; r++) f[r][c] = total;
      });
    }
    return f;
  };
  const lpCount = (grid, up) => { const f = lpCounts(grid, up); return f[f.length - 1][f[0].length - 1]; };
  // the closed forms of an empty board: C(m + n - 2, m - 1) and m^(n - 1)
  const lpFormula = (m, n, up) => (up ? BigInt(m) ** BigInt(n - 1) : bigComb(m + n - 2, m - 1));
  // a path with every path equally likely, backwards from T through the counts; rnd() in [0, 1)
  const pick = (weights, rnd) => {
    const total = weights.reduce((a, w) => a + Number(w), 0);
    let x = rnd() * total;
    for (let i = 0; i < weights.length; i++) {
      x -= Number(weights[i]);
      if (x < 0 && weights[i] > 0n) return i;
    }
    return weights.findLastIndex((w) => w > 0n);
  };
  const lpSample = (grid, up, rnd) => {
    const m = grid.length, n = grid[0].length, f = lpCounts(grid, up);
    if (f[m - 1][n - 1] === 0n) return null;
    const back = [];
    let r = m - 1, c = n - 1;
    if (!up) {
      back.push([r, c]);
      while (r || c) {
        const left = c ? f[r][c - 1] : 0n, above = r ? f[r - 1][c] : 0n;
        if (pick([left, above], rnd) === 0) c--; else r--;
        back.push([r, c]);
      }
      return back.reverse();
    }
    // with up: in column c the path ends at row r; it entered at a row a of the same run,
    // chosen in proportion to what entered there, and walked from a to r
    for (; c >= 0; c--) {
      const [s, e] = runsOf(grid, c).find(([a, b]) => a <= r && r <= b);
      const enter = enterCol(grid, f, c);
      const a = s + pick(enter.slice(s, e + 1), rnd);
      const step = a <= r ? -1 : 1;
      for (let k = r; k !== a + step; k += step) back.push([k, c]);
      r = a;
    }
    return back.reverse();
  };
  const lpArrows = (path) => path.slice(1).map(([r, c], i) => ARROW[`${r - path[i][0]},${c - path[i][1]}`]).join("");
  // a count in a cell: up to 4 digits as they are, else two digits and the power of ten
  const lpShort = (v) => {
    const s = v.toString();
    return s.length <= 4 ? s : `${s[0]}.${s[1]}e${s.length - 1}`;
  };
  const group = (v) => v.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  const heat = (v, top) => {
    if (v <= 0n) return 0;
    if (top <= 1n) return 1;
    return 1 + Math.min(3, Math.floor((3.999 * Math.log(Number(v))) / Math.log(Number(top))));
  };

  // --- the box ---------------------------------------------------------------------------------

  const latpathsView = () => ({
    mount(box) {
      const grid0 = lpParse(box.dataset.grid || "") || ["000", "000", "000"];
      const up0 = box.dataset.dirs === "rud";
      const st = { grid: grid0.slice(), up: up0, path: null, focus: [0, 0] };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>כיוונים <select class="lp-dirs" data-nolink aria-label="הצעדים המותרים"><option value="rd">ימינה ולמטה</option><option value="rud">ימינה, למעלה ולמטה</option></select></label>` +
        `<label>שורות <input type="number" class="ex-num lp-rows" data-nolink min="${MINS}" max="${MAXS}" step="1" dir="ltr" inputmode="numeric" aria-label="מספר השורות, ${MINS} עד ${MAXS}"></label>` +
        `<label>עמודות <input type="number" class="ex-num lp-cols" data-nolink min="${MINS}" max="${MAXS}" step="1" dir="ltr" inputmode="numeric" aria-label="מספר העמודות, ${MINS} עד ${MAXS}"></label>` +
        `<button type="button" class="md-button lp-clear">ניקוי</button>` +
        `<button type="button" class="md-button ex-reset">חזרה ללוח של העמוד</button></div>` +
        `<div class="ex-controls">` +
        `<button type="button" class="md-button md-button--primary lp-rand">מסלול אקראי</button>` +
        `<button type="button" class="md-button lp-unpath">בלי מסלול</button></div>` +
        `<p class="ex-summary lp-sum" aria-live="polite"></p>` +
        `<p class="gp-edit-hint">לחיצה או גרירה על תאים שמה מכשולים או מורידה אותם, חוץ מ-S ו-T. במקלדת${NB}: חיצים בין התאים, ורווח או Enter.</p>` +
        `<figure class="gp-panel"><div class="gp-wrap"><div class="gp-grid" role="grid" dir="ltr" data-edits aria-label="הלוח${NB}: לחיצה על תא שמה בו מכשול או מורידה אותו"></div>` +
        `<svg class="gp-over" aria-hidden="true" preserveAspectRatio="none"><polyline class="gp-line" points=""/></svg></div></figure>` +
        `<span class="viz-legend"><span><i class="gx-key-s"></i>S ההתחלה, T היעד</span><span><i class="lp-key-lo"></i>מעט מסלולים</span>` +
        `<span><i class="lp-key-hi"></i>הרבה מסלולים</span><span><i class="gx-key is-wall"></i>מכשול</span><span><i class="gx-key-path"></i>המסלול האקראי</span></span>` +
        `<p class="lp-note"></p>`;
      answer(box, NB); answer(box, null);                 // the answer line keeps its place
      const $ = (sel) => box.querySelector(sel);
      const gin = $(".gp-grid"), line = $(".gp-line"), over = $(".gp-over");
      const isS = (r, c) => r === 0 && c === 0;
      const isT = (r, c) => r === st.grid.length - 1 && c === st.grid[0].length - 1;

      const draw = () => {
        const m = st.grid.length, n = st.grid[0].length;
        const f = lpCounts(st.grid, st.up), total = f[m - 1][n - 1];
        const other = lpCount(st.grid, !st.up);
        let top = 0n;
        f.forEach((row) => row.forEach((v) => { if (v > top) top = v; }));
        $(".lp-dirs").value = st.up ? "rud" : "rd";
        $(".lp-rows").value = String(m);
        $(".lp-cols").value = String(n);
        $(".lp-unpath").disabled = !st.path;
        const had = box.contains(document.activeElement) && document.activeElement.classList.contains("gp-cell");
        const onPath = new Set((st.path || []).map((x) => x.join(",")));
        let g = "";
        for (let r = 0; r < m; r++) {
          g += `<div role="row" class="gp-r">`;
          for (let c = 0; c < n; c++) {
            const wall = blocked(st.grid, r, c), v = f[r][c], tg = isS(r, c) ? "S" : isT(r, c) ? "T" : "";
            const shown = wall ? "" : lpShort(v);
            let cls = wall ? " is-wall" : ` is-open lp-h${heat(v, top)}`;
            if (onPath.has(`${r},${c}`)) cls += " is-path";
            const what = (wall ? "מכשול" : `${group(v)} מסלולים נגמרים בתא`) + (tg === "S" ? ", ההתחלה" : tg === "T" ? ", היעד" : "");
            const fo = st.focus[0] === r && st.focus[1] === c;
            const long = shown.length >= 6 ? " lp-long2" : shown.length >= 4 ? " lp-long" : "";
            g += `<div role="gridcell" class="gp-cell${cls}" data-r="${r}" data-c="${c}"${tg ? ` data-tag="${tg}"` : ""} tabindex="${fo ? 0 : -1}"${wall ? "" : ` title="${group(v)}"`}>` +
              `<span class="gp-sr">שורה ${r}, עמודה ${c}${NB}: ${what}</span>` +
              (tg ? `<span class="gp-tag" aria-hidden="true">${tg}</span>` : "") +
              `<span class="gp-v${long}" aria-hidden="true">${shown}</span></div>`;
          }
          g += `</div>`;
        }
        gin.style.setProperty("--n", n);
        $(".gp-wrap").style.setProperty("--n", n);
        gin.innerHTML = g;
        if (had) { const el = gin.querySelector('[tabindex="0"]'); if (el) el.focus({ preventScroll: true }); }
        over.setAttribute("viewBox", `0 0 ${n} ${m}`);
        line.setAttribute("points", st.path ? st.path.map(([r, c]) => `${c + 0.5},${r + 0.5}`).join(" ") : "");
        // the summary: the count, the closed form of an empty board, the other directions
        const dirs = st.up ? "ימינה, למעלה ולמטה" : "ימינה ולמטה", otherDirs = st.up ? "ימינה ולמטה בלבד" : "עם צעד למעלה";
        const empty = st.grid.every((row) => !row.includes("1"));
        const form = st.up ? `${m}^${n - 1}` : `C(${m + n - 2}, ${m - 1})`;
        let sum = `לוח ${ltr(`${m} × ${n}`)}, ${dirs}${NB}: <strong class="lp-big">${ltr(group(total))}</strong> מסלולים.`;
        if (empty) sum += ` בלוח ריק זה ${ltr(`${form} = ${group(lpFormula(m, n, st.up))}`)}.`;
        else if (total === 0n) sum += ` המכשולים חוסמים כל מסלול${st.up ? "" : other > 0n ? ", אבל עם צעד למעלה יש" : ""}.`;
        sum += ` ${otherDirs}${NB}: ${ltr(group(other))}.`;
        $(".lp-sum").innerHTML = sum;
        $(".lp-note").innerHTML = st.path
          ? `המסלול האקראי, ${ltr(st.path.length - 1)} צעדים${NB}: ${ltr(lpArrows(st.path))}. לכל אחד מ-${ltr(group(total))} המסלולים יש אותו סיכוי.`
          : st.up ? "בכל עמודה, כל תא של קטע פנוי מקבל את סכום הכניסות לקטע." : "כל תא פנוי הוא סכום של התא משמאלו והתא מעליו.";
        answer(box, total > 0n ? `${ltr(group(total))} מסלולים מ-S ל-T.` : `אין מסלול מ-S ל-T${NB}: ${ltr(0)}.`, '.gp-grid .gp-cell[data-tag="T"]');
      };

      const edited = () => { st.path = null; draw(); };
      $(".lp-dirs").addEventListener("change", () => { st.up = $(".lp-dirs").value === "rud"; edited(); });
      // the size: cells kept where they were, new ones open, S and T open
      const resize = () => {
        const clamp = (el, was) => { const v = Math.round(Number(el.value)); return Number.isFinite(v) && v > 0 ? Math.min(MAXS, Math.max(MINS, v)) : was; };
        const m = clamp($(".lp-rows"), st.grid.length), n = clamp($(".lp-cols"), st.grid[0].length);
        st.grid = Array.from({ length: m }, (_, r) => Array.from({ length: n }, (_, c) => (st.grid[r] && st.grid[r][c]) || "0").join(""));
        st.grid[m - 1] = st.grid[m - 1].slice(0, n - 1) + "0";
        st.focus = [Math.min(st.focus[0], m - 1), Math.min(st.focus[1], n - 1)];
        edited();
      };
      $(".lp-rows").addEventListener("change", resize);
      $(".lp-cols").addEventListener("change", resize);
      $(".lp-clear").addEventListener("click", () => { st.grid = st.grid.map((row) => "0".repeat(row.length)); edited(); });
      $(".ex-reset").addEventListener("click", () => { st.grid = grid0.slice(); st.up = up0; st.focus = [0, 0]; edited(); });
      $(".lp-rand").addEventListener("click", () => { st.path = lpSample(st.grid, st.up, Math.random); draw(); });
      $(".lp-unpath").addEventListener("click", () => { st.path = null; draw(); });
      // editing: a press paints the pressed cell's opposite, a drag goes on painting
      const setCell = (r, c, ch) => {
        if (isS(r, c) || isT(r, c) || st.grid[r][c] === ch) return false;
        st.grid[r] = st.grid[r].slice(0, c) + ch + st.grid[r].slice(c + 1);
        return true;
      };
      let drag = null;
      const cellAt = (ev) => {
        const el = document.elementFromPoint(ev.clientX, ev.clientY);
        const cell = el && el.closest && el.closest(".gp-cell");
        return cell && gin.contains(cell) ? [Number(cell.dataset.r), Number(cell.dataset.c)] : null;
      };
      gin.addEventListener("pointerdown", (ev) => {
        const at = cellAt(ev);
        if (!at || (ev.pointerType === "mouse" && ev.button !== 0)) return;
        ev.preventDefault();
        const [r, c] = at;
        st.focus = [r, c];
        drag = { paint: st.grid[r][c] === "1" ? "0" : "1", id: ev.pointerId };
        try { gin.setPointerCapture(ev.pointerId); } catch (err) { /* a synthetic event */ }
        if (setCell(r, c, drag.paint)) edited(); else draw();
      });
      gin.addEventListener("pointermove", (ev) => {
        if (!drag || ev.pointerId !== drag.id) return;
        const at = cellAt(ev);
        if (at && setCell(at[0], at[1], drag.paint)) edited();
      });
      const end = () => { drag = null; };
      gin.addEventListener("pointerup", end);
      gin.addEventListener("pointercancel", end);
      gin.addEventListener("lostpointercapture", end);
      gin.addEventListener("keydown", (ev) => {
        const el = ev.target.closest(".gp-cell");
        if (!el) return;
        const m = st.grid.length, n = st.grid[0].length, r = Number(el.dataset.r), c = Number(el.dataset.c);
        const mv = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[ev.key];
        if (mv) {
          st.focus = [Math.min(m - 1, Math.max(0, r + mv[0])), Math.min(n - 1, Math.max(0, c + mv[1]))];
          draw();
          const fo = gin.querySelector('[tabindex="0"]');
          if (fo) fo.focus({ preventScroll: false });
        } else if (ev.key === " " || ev.key === "Enter") {
          if (setCell(r, c, st.grid[r][c] === "1" ? "0" : "1")) edited();
        } else return;
        ev.preventDefault();
        ev.stopPropagation();
      });
      // the link and the remembered state carry the directions and the board: "rud_0100.0000"
      box.dvqExtra = {
        get: () => `${st.up ? "rud" : "rd"}_${st.grid.join(".")}`,
        set: (text) => {
          const mm = /^(rd|rud)_([01.]+)$/.exec(text), grid = mm && lpParse(mm[2]);
          if (!grid) return false;
          st.up = mm[1] === "rud";
          st.grid = grid;
          st.focus = [0, 0];
          edited();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { latpaths: latpathsView },
    help: {
      latpaths: "בכל תא פנוי מופיע מספר המסלולים מ-S שנגמרים בו, והצבע מתחזק כשהמספר גדל. לחיצה או גרירה על תאים שמה מכשולים או מורידה אותם, ובוחרים את גודל הלוח ואת הכיוונים : ימינה ולמטה, או ימינה, למעלה ולמטה בלי לעבור באותו תא פעמיים. \"מסלול אקראי\" מצייר מסלול אחד מ-S ל-T, כשלכל המסלולים יש אותו סיכוי. השורה שמעל הלוח נותנת את המספר, את הנוסחה כשהלוח ריק, ואת המספר של הכיוונים האחרים.".replace(/ :/g, " :"),
    },
    models: { lpParse, lpCounts, lpCount, lpFormula, lpSample, lpArrows, lpShort },
  });
})();
