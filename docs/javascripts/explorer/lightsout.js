// kinds: lightsout
//   lightsout              0087        Lights Out on an n x n board (3 to 7), a press flips the light and its neighbours up, down, left and right (or the eight around it with the diagonals). Mode play: a click presses (or, in drawing, flips one light), a random start that can be solved, the presses against the fewest from the start, the solution shown as frames (the fewest presses), or why there is none (a quiet pattern that touches an odd number of lit lights). Mode chase: light chasing step by step, a press under every light still on, row by row, then the first row from the lights left on the bottom row, and chasing again
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tag); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests. Cell (r, c) is index r*n + c, row 0 on top and column 0
// on the left; a board is an array of 0 and 1.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMIN = 3, NMAX = 7;

  // --- the models ------------------------------------------------------------------------------

  // the cells a press on cell k flips
  const loFlips = (n, diag, k) => {
    const r = Math.floor(k / n), c = k % n, out = [];
    for (let dr = -1; dr <= 1; dr++) {
      for (let dc = -1; dc <= 1; dc++) {
        if (dr && dc && !diag) continue;
        const a = r + dr, b = c + dc;
        if (a >= 0 && a < n && b >= 0 && b < n) out.push(a * n + b);
      }
    }
    return out;
  };
  const loPress = (n, diag, lit, k) => { const out = lit.slice(); loFlips(n, diag, k).forEach((j) => { out[j] ^= 1; }); return out; };
  const loApply = (n, diag, lit, press) => {
    let out = lit.slice();
    press.forEach((p, k) => { if (p) out = loPress(n, diag, out, k); });
    return out;
  };
  const xorInto = (a, b) => { for (let i = 0; i < a.length; i++) a[i] ^= b[i]; };
  const dot = (a, b) => a.reduce((s, v, i) => s ^ (v & b[i]), 0);
  const weight = (v) => v.reduce((s, x) => s + x, 0);

  // the reduced row echelon form of the press matrix of a board (cached): the rows, the
  // pivot columns, and a basis of the kernel (the presses that change nothing)
  const CACHE = new Map();
  const loMatrix = (n, diag) => {
    const key = `${n}.${diag ? 1 : 0}`;
    if (CACHE.has(key)) return CACHE.get(key);
    const N = n * n, rows = [];
    for (let j = 0; j < N; j++) {
      const row = new Array(N).fill(0);
      loFlips(n, diag, j).forEach((i) => { row[i] = 1; });   // symmetric: press i flips j iff press j flips i
      rows.push(row);
    }
    const piv = [];
    const red = rows.map((r) => r.slice());
    for (let col = 0; col < N; col++) {
      const r = piv.length;
      let p = -1;
      for (let i = r; i < N; i++) if (red[i][col]) { p = i; break; }
      if (p < 0) continue;
      [red[r], red[p]] = [red[p], red[r]];
      for (let i = 0; i < N; i++) if (i !== r && red[i][col]) xorInto(red[i], red[r]);
      piv.push(col);
    }
    const kernel = [];
    for (let f = 0; f < N; f++) {
      if (piv.includes(f)) continue;
      const v = new Array(N).fill(0);
      v[f] = 1;
      piv.forEach((c, i) => { if (red[i][f]) v[c] = 1; });
      kernel.push(v);
    }
    const out = { N, rows, kernel };
    CACHE.set(key, out);
    return out;
  };
  // every combination of the kernel basis (at most 2^9 on these boards)
  const kernelAll = (kernel, N) => {
    let all = [new Array(N).fill(0)];
    kernel.forEach((b) => { all = all.concat(all.map((v) => { const w = v.slice(); xorInto(w, b); return w; })); });
    return all;
  };
  const key01 = (v) => v.join("");
  // the board lit: { press (the fewest presses, ties by the first cells), free, count (how
  // many press sets solve it), quiet (null, or a quiet pattern with an odd number of lit
  // lights in it, which shows there is none) }
  const loSolve = (n, diag, lit) => {
    const { N, rows, kernel } = loMatrix(n, diag);
    const eq = rows.map((r, j) => r.concat([lit[j]]));
    const piv = [];
    for (let col = 0; col < N; col++) {
      const r = piv.length;
      let p = -1;
      for (let i = r; i < N; i++) if (eq[i][col]) { p = i; break; }
      if (p < 0) continue;
      [eq[r], eq[p]] = [eq[p], eq[r]];
      for (let i = 0; i < N; i++) if (i !== r && eq[i][col]) xorInto(eq[i], eq[r]);
      piv.push(col);
    }
    const free = N - piv.length;
    if (eq.slice(piv.length).some((r) => r[N])) {
      const quiet = kernel.find((q) => dot(q, lit)) || null;
      return { press: null, free, count: 0, quiet };
    }
    const x = new Array(N).fill(0);
    piv.forEach((c, i) => { x[c] = eq[i][N]; });
    let best = null;
    kernelAll(kernel, N).forEach((k) => {
      const v = x.slice();
      xorInto(v, k);
      if (!best || weight(v) < weight(best) || (weight(v) === weight(best) && key01(v) > key01(best))) best = v;
    });
    return { press: best, free, count: 2 ** free, quiet: null };
  };

  // light chasing without diagonals: the bottom row (an array of n) left on after chasing
  // from lit with the presses first on row 0
  const chaseRest = (n, lit, first) => {
    let cur = lit.slice();
    first.forEach((f, c) => { if (f) cur = loPress(n, false, cur, c); });
    for (let r = 0; r < n - 1; r++) for (let c = 0; c < n; c++) if (cur[r * n + c]) cur = loPress(n, false, cur, (r + 1) * n + c);
    return cur.slice((n - 1) * n);
  };
  const bitsOfInt = (v, n) => Array.from({ length: n }, (_, c) => (v >> c) & 1);
  // the first rows that clear the bottom row rest, fewest presses first, then as the
  // bits read left to right (column 0 first)
  const loFirstRow = (n, rest) => {
    const zero = new Array(n * n).fill(0), out = [];
    for (let f = 0; f < 1 << n; f++) {
      const fb = bitsOfInt(f, n);
      if (key01(chaseRest(n, zero, fb)) === key01(rest)) out.push(fb);
    }
    out.sort((a, b) => weight(a) - weight(b) || (key01(a) < key01(b) ? -1 : 1));
    return out;
  };
  // the steps of light chasing from lit: { phase, k (the cell pressed, or -1), row (the row
  // it clears), lit, press (the presses so far, each cell's count mod 2), presses (how many
  // presses so far), rest, first }. Phases: chase1 (under the lights, row by row), rest
  // (the bottom row left on, and the first row that clears it, or null), fix (the first
  // row), chase2 (chasing again), done
  const loChaseSteps = (n, lit) => {
    const N = n * n, steps = [];
    let cur = lit.slice(), press = new Array(N).fill(0), presses = 0;
    const push = (phase, k, row, extra = {}) => steps.push({ phase, k, row, lit: cur.slice(), press: press.slice(), presses, ...extra });
    const doPress = (k) => { cur = loPress(n, false, cur, k); press[k] ^= 1; presses++; };
    const chase = (phase) => {
      for (let r = 0; r < n - 1; r++) for (let c = 0; c < n; c++) if (cur[r * n + c]) { doPress((r + 1) * n + c); push(phase, (r + 1) * n + c, r); }
    };
    chase("chase1");
    const rest = cur.slice((n - 1) * n);
    if (!rest.some((x) => x)) { push("done", -1, -1, { rest, first: new Array(n).fill(0) }); return steps; }
    const firsts = loFirstRow(n, rest), first = firsts.length ? firsts[0] : null;
    push("rest", -1, n - 1, { rest, first });
    if (!first) return steps;
    first.forEach((f, c) => { if (f) { doPress(c); push("fix", c, -1, { first }); } });
    chase("chase2");
    push("done", -1, -1, { rest, first });
    return steps;
  };

  // a board as hexadecimal (cell k is bit k), and back (null when it does not fit n*n cells)
  const loHex = (v) => {
    let s = "";
    for (let i = 0; i < v.length; i += 4) s = ((v[i] | 0) | (v[i + 1] | 0) << 1 | (v[i + 2] | 0) << 2 | (v[i + 3] | 0) << 3).toString(16) + s;
    return s.replace(/^0+(?=.)/, "") || "0";
  };
  const loUnhex = (s, N) => {
    if (!/^[0-9a-f]{1,13}$/i.test(String(s))) return null;
    const v = new Array(N).fill(0), t = String(s).toLowerCase();
    for (let i = 0; i < t.length; i++) {
      const d = parseInt(t[t.length - 1 - i], 16);
      for (let b = 0; b < 4; b++) {
        if (!((d >> b) & 1)) continue;
        const k = 4 * i + b;
        if (k >= N) return null;
        v[k] = 1;
      }
    }
    return v;
  };

  // --- the board -------------------------------------------------------------------------------

  const S = 40;
  // marks: k → classes of overlays (lo-press, lo-now, lo-quiet); band(r) → a row class
  const boardSvg = (n, lit, aria, { marks = () => [], band = () => "", buttons = false, focus = -1 } = {}) => {
    const w = n * S + 4;
    let s = `<svg class="figure lo-board" viewBox="0 0 ${w} ${w}" style="max-width:${Math.min(22, (w * 1.3) / 16).toFixed(1)}rem" role="${buttons ? "group" : "img"}" aria-label="${aria}">`;
    for (let k = 0; k < n * n; k++) {
      const r = Math.floor(k / n), c = k % n, x = 2 + c * S, y = 2 + r * S, b = band(r);
      let cell = `<rect class="lo-cell${b ? ` ${b}` : ""}" x="${x}" y="${y}" width="${S}" height="${S}"/>`;
      marks(k).forEach((m) => { cell += `<rect class="${m}" x="${x + 3}" y="${y + 3}" width="${S - 6}" height="${S - 6}" rx="4"/>`; });
      cell += `<circle class="${lit[k] ? "lo-on" : "lo-off"}" cx="${x + S / 2}" cy="${y + S / 2}" r="${(S * 0.27).toFixed(1)}"/>`;
      if (buttons) {
        const name = `שורה ${r}, עמודה ${c}${NB}: ${lit[k] ? "דולקת" : "כבויה"}`;
        cell = `<g class="lo-btn" role="button" tabindex="${k === focus ? 0 : -1}" data-k="${k}" aria-label="${name}">${cell}` +
          `<rect class="lo-ring" x="${x + 1}" y="${y + 1}" width="${S - 2}" height="${S - 2}"/></g>`;
      }
      s += cell;
    }
    return s + `<rect class="lo-frame" x="2" y="2" width="${n * S}" height="${n * S}"/></svg>`;
  };
  const cellName = (n, k) => `${ltr(`(${Math.floor(k / n)}, ${k % n})`)}`;
  const listCells = (n, v) => {
    const ks = v.map((x, k) => (x ? k : -1)).filter((k) => k >= 0);
    return ks.map((k) => cellName(n, k)).join(", ");
  };
  const clampN = (v, d) => { const x = Math.floor(Number(v)); return Number.isFinite(x) ? Math.min(NMAX, Math.max(NMIN, x)) : d; };
  const sizeSel = (n0) => `<label>הלוח <select class="lo-n" aria-label="גודל הלוח">` +
    Array.from({ length: NMAX - NMIN + 1 }, (_, i) => NMIN + i).map((v) => `<option value="${v}"${v === n0 ? " selected" : ""}>${v} × ${v}</option>`).join("") + `</select></label>`;
  const randomSolvable = (n, diag) => {
    const N = n * n;
    let lit = new Array(N).fill(0);
    for (let tries = 0; tries < 8 && !lit.some((x) => x); tries++) {
      for (let k = 0; k < N; k++) if (Math.random() < 0.5) lit = loPress(n, diag, lit, k);
    }
    return lit;
  };
  // the arrow keys move the focus between the cells of a board (column 0 on the left)
  const arrows = (wrap, n, setFocus, onKey) => {
    wrap.addEventListener("keydown", (e) => {
      const g = e.target.closest(".lo-btn");
      if (!g) return;
      const k = Number(g.dataset.k);
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); e.stopPropagation(); onKey(k); return; }
      const nn = n();
      let r = Math.floor(k / nn), c = k % nn;
      const moves = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] };
      if (e.key === "Home") c = 0; else if (e.key === "End") c = nn - 1; else if (moves[e.key]) {
        r = Math.min(nn - 1, Math.max(0, r + moves[e.key][0])); c = Math.min(nn - 1, Math.max(0, c + moves[e.key][1]));
      } else return;
      e.preventDefault(); e.stopPropagation();
      setFocus(r * nn + c);
      wrap.querySelectorAll(".lo-btn").forEach((el) => el.setAttribute("tabindex", "-1"));
      const t = wrap.querySelector(`.lo-btn[data-k="${r * nn + c}"]`);
      if (t) { t.setAttribute("tabindex", "0"); t.focus(); }
    });
  };

  // --- play ------------------------------------------------------------------------------------

  const playView = (box) => {
    const N0 = clampN(box.dataset.n, 3), D0 = box.dataset.diag === "1";
    const L0 = loUnhex(box.dataset.lit || "0", N0 * N0) || new Array(N0 * N0).fill(0);
    const st = { n: N0, diag: D0, start: L0.slice(), lit: L0.slice(), press: new Array(N0 * N0).fill(0), count: 0, show: false, focus: 0 };
    box.innerHTML =
      `<div class="ex-controls">` + sizeSel(N0) +
      `<label>השכנות <select class="lo-diag" aria-label="אילו שכנות לחיצה הופכת"><option value="0">למעלה, למטה, ימינה ושמאלה</option><option value="1">גם באלכסון</option></select></label>` +
      `<label>לחיצה על נורה <select class="lo-click" aria-label="מה עושה לחיצה על נורה"><option value="press">לוחצת</option><option value="draw">מדליקה או מכבה רק אותה</option></select></label></div>` +
      `<div class="ex-controls">` +
      `<button type="button" class="md-button md-button--primary lo-show" aria-pressed="false">הצגת פתרון</button>` +
      `<button type="button" class="md-button lo-rand">הגרלה</button>` +
      `<button type="button" class="md-button lo-clear">ניקוי הלוח</button>` +
      `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
      `<div class="lo-wrap"></div>` +
      `<span class="viz-legend"><span><i class="lo-key-on"></i>דולקת</span><span><i class="lo-key-off"></i>כבויה</span>` +
      `<span><i class="lo-key-press"></i>לחיצה בפתרון</span><span><i class="lo-key-quiet"></i>דפוס שקט</span></span>` +
      `<p class="ex-summary lo-sum" aria-live="polite"></p>` +
      `<p class="lo-note"></p>`;
    const $ = (s) => box.querySelector(s);
    const wrap = $(".lo-wrap");
    $(".lo-diag").value = D0 ? "1" : "0";
    const restart = (lit) => { const N = st.n * st.n; st.start = lit.slice(); st.lit = lit.slice(); st.press = new Array(N).fill(0); st.count = 0; };
    const draw = (focus = false) => {
      const n = st.n, N = n * n, sol = loSolve(n, st.diag, st.lit), from = loSolve(n, st.diag, st.start);
      st.focus = Math.min(st.focus, N - 1);
      $(".lo-n").value = String(n);
      $(".lo-show").setAttribute("aria-pressed", String(st.show));
      const on = weight(st.lit);
      wrap.innerHTML = boardSvg(n, st.lit, `לוח של ${n} על ${n}${NB}: ${on} נורות דולקות. לוחצים על נורה, או עוברים בחיצים ולוחצים Enter`, {
        buttons: true, focus: st.focus,
        marks: (k) => (st.show && on ? (sol.press ? (sol.press[k] ? ["lo-press"] : []) : sol.quiet && sol.quiet[k] ? ["lo-quiet"] : []) : []),
      });
      if (focus) { const g = wrap.querySelector(`.lo-btn[data-k="${st.focus}"]`); if (g) g.focus(); }
      let sum = `‏${ltr(on)} ${on === 1 ? "נורה דולקת" : "נורות דולקות"}, ${ltr(st.count)} ${st.count === 1 ? "לחיצה" : "לחיצות"} עד עכשיו. `;
      sum += from.press ? (weight(from.press) ? `מהמצב ההתחלתי אפשר לכבות הכול ב-${ltr(weight(from.press))} לחיצות לפחות.` : "המצב ההתחלתי כבוי.")
        : "את המצב ההתחלתי אי אפשר לכבות.";
      $(".lo-sum").innerHTML = sum;
      const kinds = st.diag ? "שמונה השכנות" : "ארבע השכנות";
      let note = `בלוח הזה ${ltr(N)} נעלמים ו-${ltr(sol.free)} ${sol.free === 1 ? "משתנה חופשי" : "משתנים חופשיים"}` +
        (sol.free ? `${NB}: רק ${ltr(`1/${2 ** sol.free}`)} מהמצבים אפשר לכבות, ולכל אחד מהם ${ltr(2 ** sol.free)} פתרונות.` : `${NB}: כל מצב אפשר לכבות, בדרך אחת בדיוק.`) +
        ` לחיצה הופכת נורה ואת ${kinds} שלה.`;
      if (st.show && on) {
        if (sol.press) {
          const w = weight(sol.press);
          note = `המסגרות הכחולות${NB}: ${ltr(w)} ${w === 1 ? "לחיצה שמכבה" : "לחיצות שמכבות"} את כל הנורות מהמצב הנוכחי` +
            (sol.free ? `, הכי מעט מבין ${ltr(sol.count)} הפתרונות.` : ", והפתרון היחיד.") + " הסדר לא משנה.";
        } else {
          const inq = sol.quiet ? st.lit.filter((x, k) => x && sol.quiet[k]).length : 0;
          note = `<strong>אי אפשר לכבות את המצב הזה.</strong> הדפוס המקווקו הוא לחיצות שלא משנות אף נורה, ובתוכו ${inq === 1 ? "נורה דולקת אחת" : `${ltr(inq)} נורות דולקות`}, מספר אי-זוגי. ` +
            `כל לחיצה הופכת בתוכו מספר זוגי של נורות, ולכן הזוגיות הזו לא משתנה ולא תגיע ל-${ltr(0)}.`;
        }
      }
      $(".lo-note").innerHTML = note;
      if (!on && st.count) answer(box, `כל הנורות כבויות אחרי ${ltr(st.count)} ${st.count === 1 ? "לחיצה" : "לחיצות"}. המינימום מהמצב ההתחלתי${NB}: ${ltr(from.press ? weight(from.press) : 0)}.`, ".lo-sum");
      else answer(box, null);
    };
    const act = (k) => {
      st.focus = k;
      if ($(".lo-click").value === "draw") { const lit = st.lit.slice(); lit[k] ^= 1; restart(lit); } else {
        st.lit = loPress(st.n, st.diag, st.lit, k); st.press[k] ^= 1; st.count++;
      }
      draw(true);
    };
    wrap.addEventListener("click", (e) => { const g = e.target.closest(".lo-btn"); if (g) act(Number(g.dataset.k)); });
    arrows(wrap, () => st.n, (k) => { st.focus = k; }, act);
    $(".lo-n").addEventListener("change", () => { st.n = clampN($(".lo-n").value, N0); restart(new Array(st.n * st.n).fill(0)); draw(); });
    $(".lo-diag").addEventListener("change", () => { st.diag = $(".lo-diag").value === "1"; restart(st.lit); draw(); });
    $(".lo-show").addEventListener("click", () => { st.show = !st.show; draw(); });
    $(".lo-rand").addEventListener("click", () => { restart(randomSolvable(st.n, st.diag)); draw(); });
    $(".lo-clear").addEventListener("click", () => { restart(new Array(st.n * st.n).fill(0)); draw(); });
    $(".ex-reset").addEventListener("click", () => {
      st.n = N0; st.diag = D0; $(".lo-diag").value = D0 ? "1" : "0"; $(".lo-click").value = "press"; st.show = false; st.focus = 0;
      restart(L0); draw();
    });
    // the start, the presses (each cell's count mod 2) and their number ride in the link
    box.dvqExtra = {
      get: () => `${loHex(st.start)}.${loHex(st.press)}.${st.count}`,
      set: (text) => {
        const m = /^([0-9a-f]+)\.([0-9a-f]+)\.(\d{1,4})$/i.exec(String(text));
        const N = st.n * st.n, start = m && loUnhex(m[1], N), press = m && loUnhex(m[2], N);
        if (!start || !press) return false;
        st.start = start; st.press = press; st.count = Math.max(Number(m[3]), weight(press));
        st.lit = loApply(st.n, st.diag, start, press);
        draw();
        return true;
      },
    };
    draw();
  };

  // --- light chasing ---------------------------------------------------------------------------

  const chaseView = (box) => {
    const N0 = clampN(box.dataset.n, 5);
    const L0 = loUnhex(box.dataset.lit || "0", N0 * N0) || new Array(N0 * N0).fill(0);
    const st = { n: N0, start: L0.slice(), k: 0, steps: loChaseSteps(N0, L0), focus: 0 };
    box.innerHTML =
      `<div class="ex-controls">` + sizeSel(N0) +
      `<button type="button" class="md-button lo-rand">הגרלה</button>` +
      `<button type="button" class="md-button lo-clear">ניקוי הלוח</button>` +
      `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
      `<div class="ex-controls ex-play-row">` +
      `<button type="button" class="md-button ex-start">ההתחלה</button>` +
      `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
      `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
      `<button type="button" class="md-button ex-end">עד הסוף</button>` +
      `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1300, 700, 300) +
      `<span class="ex-pos"></span></div>` +
      `<div class="lo-wrap"></div>` +
      `<span class="viz-legend"><span><i class="lo-key-on"></i>דולקת</span><span><i class="lo-key-now"></i>הלחיצה של הצעד, או הבאה בשורה העליונה</span>` +
      `<span><i class="lo-key-press"></i>נלחצה עד עכשיו</span><span><i class="lo-key-band"></i>השורה שמכבים</span><span><i class="lo-key-rest"></i>מה שנשאר בשורה התחתונה</span></span>` +
      `<p class="ex-summary lo-sum" aria-live="polite"></p>` +
      `<p class="lo-note"></p>`;
    const $ = (s) => box.querySelector(s);
    const wrap = $(".lo-wrap"), play = $(".ex-play"), speed = $(".ex-speed");
    const bitsText = (v) => ltr(v.join(""));
    const draw = (focus = false) => {
      const n = st.n, steps = st.steps, T = steps.length;
      st.k = Math.min(Math.max(st.k, 0), T);
      const k = st.k, s = k ? steps[k - 1] : null, lit = s ? s.lit : st.start, press = s ? s.press : new Array(n * n).fill(0);
      $(".lo-n").value = String(n);
      $(".ex-pos").textContent = `צעד ${k} מתוך ${T}`;
      $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
      $(".ex-next").disabled = $(".ex-end").disabled = k === T;
      const next = s && s.phase === "rest" && s.first ? s.first : null;
      wrap.innerHTML = boardSvg(n, lit, `לוח של ${n} על ${n} אחרי ${k} צעדים${NB}: ${weight(lit)} נורות דולקות. לפני הצעד הראשון לחיצה על נורה מדליקה או מכבה אותה`, {
        buttons: true, focus: st.focus,
        band: (r) => (s && (s.phase === "chase1" || s.phase === "chase2") && r === s.row ? "is-band" : s && s.phase === "rest" && r === n - 1 ? "is-rest" : ""),
        marks: (c) => {
          const m = [];
          if (press[c]) m.push("lo-press");
          if (s && c === s.k) m.push("lo-now");
          if (next && c < n && next[c]) m.push("lo-now");
          return m;
        },
      });
      if (focus) { const g = wrap.querySelector(`.lo-btn[data-k="${st.focus}"]`); if (g) g.focus(); }
      const on = weight(lit);
      let sum, note = "", ans = null;
      if (!s) {
        sum = `‏${ltr(on)} נורות דולקות. רדיפת אורות לוחצת מתחת לכל נורה דולקת, שורה אחרי שורה, וכך מכבה את כל השורות חוץ מהאחרונה.`;
        note = "לפני הצעד הראשון אפשר ללחוץ על נורות כדי לצייר מצב התחלתי.";
      } else {
        const r = Math.floor(s.k / n), c = s.k % n;
        sum = `צעד ${ltr(k)}${NB}: ${ltr(s.presses)} לחיצות עד עכשיו, ${ltr(on)} נורות דולקות.`;
        if (s.phase === "chase1" || s.phase === "chase2") {
          note = `הנורה ${cellName(n, s.row * n + c)} דולקת, ולכן לוחצים מתחתיה, על ${cellName(n, s.k)}. הלחיצה מכבה אותה ולא נוגעת בשורות שמעליה.` +
            (s.phase === "chase2" ? " זה המעבר השני, אחרי התיקון של השורה העליונה." : "");
        } else if (s.phase === "rest") {
          note = `השורות ${ltr(0)} עד ${ltr(n - 2)} כבויות, ובשורה התחתונה נשארו ${bitsText(s.rest)} (העמודה ${ltr(0)} משמאל). ` +
            (s.first ? `השורה התחתונה היא פונקציה לינארית של הלחיצות בשורה העליונה, ולכן פותרים ${ltr(n)} משוואות במקום ${ltr(n * n)}${NB}: לוחצים בשורה העליונה על ${bitsText(s.first)}, ורודפים שוב.`
              : `<strong>אין שורה עליונה שמנקה את זה</strong>${NB}: אף צירוף של לחיצות בשורה העליונה לא משאיר בתחתונה בדיוק ${bitsText(s.rest)}, ולכן את הלוח הזה אי אפשר לכבות.`);
          if (!s.first) ans = `אי אפשר לכבות את הלוח${NB}: אחרי הרדיפה נשאר ${bitsText(s.rest)} בשורה התחתונה, ושום שורה עליונה לא מנקה אותו.`;
        } else if (s.phase === "fix") {
          note = `מתקנים את השורה העליונה${NB}: לוחצים על ${cellName(n, s.k)}.`;
        } else {
          note = `כל הנורות כבויות. הלחיצות המסומנות הן הפתרון${NB}: ${listCells(n, s.press) || "אף אחת"}.`;
          ans = `כל הנורות כבויות${NB}: ${ltr(weight(s.press))} לחיצות בפתרון, ${ltr(s.presses)} לחיצות בדרך (לחיצה כפולה מבטלת את עצמה).`;
        }
      }
      $(".lo-sum").innerHTML = sum;
      $(".lo-note").innerHTML = note;
      answer(box, k === T ? ans : null, ".lo-sum");
    };
    const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= st.steps.length, restart: () => { st.k = 0; draw(); } });
    const setStart = (lit) => { stop(); st.start = lit.slice(); st.steps = loChaseSteps(st.n, st.start); st.k = 0; draw(); };
    const act = (k) => { st.focus = k; const lit = st.start.slice(); lit[k] ^= 1; stop(); st.start = lit; st.steps = loChaseSteps(st.n, lit); st.k = 0; draw(true); };
    wrap.addEventListener("click", (e) => { const g = e.target.closest(".lo-btn"); if (g) act(Number(g.dataset.k)); });
    arrows(wrap, () => st.n, (k) => { st.focus = k; }, act);
    $(".lo-n").addEventListener("change", () => { st.n = clampN($(".lo-n").value, N0); st.focus = 0; setStart(randomSolvable(st.n, false)); });
    $(".lo-rand").addEventListener("click", () => setStart(randomSolvable(st.n, false)));
    $(".lo-clear").addEventListener("click", () => setStart(new Array(st.n * st.n).fill(0)));
    $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
    $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
    $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
    $(".ex-end").addEventListener("click", () => { stop(); st.k = st.steps.length; draw(); });
    $(".ex-reset").addEventListener("click", () => { st.n = N0; st.focus = 0; setStart(L0); });
    // the start board rides in the link
    box.dvqExtra = {
      get: () => loHex(st.start),
      set: (text) => { const v = loUnhex(text, st.n * st.n); if (!v) return false; setStart(v); return true; },
    };
    draw();
  };

  const lightsoutView = () => ({
    mount(box) { (box.dataset.mode === "chase" ? chaseView : playView)(box); },
  });

  dvqExplorers.register({
    views: { lightsout: lightsoutView },
    help: {
      lightsout: "במצב משחק לוחצים על נורות (או עוברים בחיצים ולוחצים Enter) : כל לחיצה הופכת את הנורה ואת השכנות שלה. אפשר לבחור גודל לוח ושכנות, להגריל מצב שאפשר לכבות, או לבחור \"מדליקה או מכבה רק אותה\" ולצייר מצב. \"הצגת פתרון\" מסמנת את הלחיצות המעטות ביותר מהמצב הנוכחי, או דפוס שקט שמראה למה אין פתרון. בתיבה של רדיפת האורות כל צעד הוא לחיצה אחת : מתחת לכל נורה דולקת, שורה אחרי שורה, ואז התיקון של השורה העליונה לפי מה שנשאר בתחתונה, ורדיפה שנייה.",
    },
    models: { loFlips, loApply, loMatrix, loSolve, loFirstRow, loChaseSteps, loHex, loUnhex },
  });
})();
