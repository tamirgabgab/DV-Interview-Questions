// kinds: kflip kflip2
//   kflip                  0108        the fewest flips of k consecutive bits that make a row of bits all ones (data-bits "00010110", data-k 3): a typed or clicked row of up to 20 bits or a ready one (the page's example, 010 with k = 1, 110 with k = 2 that has no solution, a long one and the same with its last bit flipped), scanned bit by bit: the bits as given and as they are now, the windows chosen so far in lanes under the row (open over the bit, closed, the one just opened), each bit's decision (a window, none, a check where no window can start), the queue of open windows with its parity and the flips, why the decision is forced, and the answer or why there is none
//   kflip2                 0108        the same on a grid of up to 8 x 8 cells with k x k squares (data-grid "10011.10101.00010.00100", data-k 2): a typed or clicked grid, a ready one or a random one that can be fixed, scanned cell by cell row by row: the cells now with the squares chosen so far and the square just opened, the band of the last k − 1 rows and columns where no square starts (only checked), and the page's difference array d (three corners of every square) beside the prefix XOR p of the scanned cells
// Loaded after core.js on the pages that have these kinds (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests. Bit 0 is on the left; cell (r, c) is row r from the top
// and column c from the left.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMAX = 20, KMAX = 8, GMAX = 8, K2MAX = 5;

  // --- the models, as tools/figures/q0108.py ------------------------------------------------
  // "00010110", "0001 0110" or "0,0,0,1": 1 to NMAX bits, else null
  const kfParse = (text) => {
    const t = String(text || "").replace(/[\s,;.]+/g, "");
    if (!t || t.length > NMAX || !/^[01]+$/.test(t)) return null;
    return [...t].map(Number);
  };
  // the forced scan: a row per bit until it stops, as q0108.events
  const kfScan = (a, k) => {
    const n = a.length, chosen = [], rows = [];
    for (let i = 0; i < n; i++) {
      const open = chosen.filter((p) => p > i - k), par = open.length % 2, now = a[i] ^ par;
      const act = i <= n - k ? (now === 0 ? "start" : "skip") : (now === 1 ? "check" : "fail");
      rows.push({ i, a: a[i], open, par, now, act });
      if (act === "start") chosen.push(i);
      if (act === "fail") break;
    }
    return rows;
  };
  // "10011.10101" or "10011 10101" or "10011/10101": 1 to GMAX rows of the same 1 to GMAX bits, else null
  const kf2Parse = (text) => {
    const rows = String(text || "").trim().split(/[\s,;./|]+/).filter(Boolean);
    if (!rows.length || rows.length > GMAX || rows.some((r) => !/^[01]+$/.test(r) || r.length > GMAX || r.length !== rows[0].length)) return null;
    return rows.map((r) => [...r].map(Number));
  };
  // the forced scan of a grid, row by row: a row per cell until it stops, as q0108.events2
  const kf2Scan = (g, k) => {
    const R = g.length, C = g[0].length, chosen = [], rows = [];
    for (let r = 0; r < R; r++) {
      for (let c = 0; c < C; c++) {
        const par = chosen.filter(([pr, pc]) => pr <= r && r < pr + k && pc <= c && c < pc + k).length % 2, now = g[r][c] ^ par;
        const act = r + k <= R && c + k <= C ? (now === 0 ? "start" : "skip") : (now === 1 ? "check" : "fail");
        rows.push({ r, c, par, now, act });
        if (act === "start") chosen.push([r, c]);
        if (act === "fail") return rows;
      }
    }
    return rows;
  };
  // the page's d (three corners of every square chosen) and p (the parity of the scanned cells,
  // null for the others) after the first `steps` cells, as q0108.dp_after
  const kf2State = (g, k, steps) => {
    const R = g.length, C = g[0].length, ev = kf2Scan(g, k).slice(0, steps);
    const chosen = ev.filter((e) => e.act === "start").map((e) => [e.r, e.c]);
    const d = Array.from({ length: R + 1 }, () => new Array(C + 1).fill(0));
    chosen.forEach(([r, c]) => { d[r][c + k] ^= 1; d[r + k][c] ^= 1; d[r + k][c + k] ^= 1; });
    const p = Array.from({ length: R }, () => new Array(C).fill(null));
    ev.forEach(({ r, c }) => { p[r][c] = chosen.filter(([pr, pc]) => pr <= r && r < pr + k && pc <= c && c < pc + k).length % 2; });
    return { d, p, chosen };
  };
  const bits = (s) => [...s].map(Number);
  const kfPresets = [
    ["הדוגמה", bits("00010110"), 3],
    ["‏010, k = 1", bits("010"), 1],
    ["‏110, k = 2 : אין פתרון", bits("110"), 2],
    ["ארוך, k = 4", bits("00011110000101101000"), 4],
    ["ארוך, הביט האחרון הפוך", bits("00011110000101101001"), 4],
  ];
  const grid = (s) => s.split(".").map(bits);
  const kf2Presets = [
    ["הדוגמה", grid("10011.10101.00010.00100"), 2],
    ["הפינה הפוכה : אין פתרון", grid("10011.10101.00010.00101"), 2],
    ["‏6 על 6, k = 3", grid("001001.001110.010010.011011.011100.000000"), 3],
    ["‏8 על 8, k = 2", grid("00000101.11000011.10110001.11001111.01000100.00100100.01001000.10010000"), 2],
  ];

  // --- shared helpers ----------------------------------------------------------------------------
  const plural = (v, one, many) => (v === 1 ? one : `${ltr(v)} ${many}`);
  const listOf = (xs) => ltr(`[${xs.join(", ")}]`);
  const clampK = (v, hi, d) => { const x = Math.floor(Number(v)); return Number.isFinite(x) && x >= 1 && x <= hi ? x : d; };
  // the arrow keys move the focus between the cells of a row or a grid (roving tabindex)
  const roving = (wrap, sel, move) => {
    wrap.addEventListener("keydown", (e) => {
      const el = e.target.closest(sel);
      if (!el) return;
      const to = move(el, e.key);
      if (to === null) return;
      e.preventDefault(); e.stopPropagation();
      wrap.querySelectorAll(sel).forEach((b) => b.setAttribute("tabindex", "-1"));
      const t = wrap.querySelector(`${sel}[data-at="${to}"]`);
      if (t) { t.setAttribute("tabindex", "0"); t.focus(); }
    });
  };
  const playRow = () =>
    `<div class="ex-controls ex-play-row">` +
    `<button type="button" class="md-button ex-start">ההתחלה</button>` +
    `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
    `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
    `<button type="button" class="md-button ex-end">עד הסוף</button>` +
    `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1300, 750, 300) +
    `<span class="ex-pos"></span></div>`;

  // --- the row ---------------------------------------------------------------------------------

  const rowView = () => ({
    mount(box) {
      const a0 = kfParse(box.dataset.bits) || kfPresets[0][1].slice();
      const k0 = clampK(box.dataset.k, KMAX, 3);
      const st = { a: a0.slice(), k: k0, s: 0, focus: 0, err: "" };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המערך <select class="kf-preset" aria-label="איזה מערך">${kfPresets.map(([name], i) => `<option value="${i}">${name}</option>`).join("")}<option value="custom">משלכם</option></select></label>` +
        `<label>הביטים <input type="text" class="kf-bits" dir="ltr" spellcheck="false" autocomplete="off" aria-label="הביטים, ביט 0 משמאל, עד ${NMAX} ביטים"></label>` +
        `<label>‏k <input type="number" class="kf-k" min="1" max="${KMAX}" step="1" dir="ltr" inputmode="numeric" aria-label="k, אורך החלון"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        playRow() +
        `<p class="ex-summary kf-sum" aria-live="polite"></p>` +
        `<div class="kf-rowwrap" tabindex="0" role="region" aria-label="הביטים, החלונות שנבחרו וההחלטה על כל ביט"></div>` +
        `<p class="kf-state"></p>` +
        `<p class="kf-note"></p>` +
        `<span class="viz-legend kf-legend"><span><i class="kf-key-one"></i>ביט 1</span><span><i class="kf-key-cur"></i>הביט של הצעד</span>` +
        `<span><i class="kf-key-open"></i>חלון פתוח מעל הביט</span><span><i class="kf-key-new"></i>החלון שהצעד פתח</span>` +
        `<span><i class="kf-key-closed"></i>חלון שנסגר</span><span><i class="kf-key-nostart"></i>שום חלון לא מתחיל כאן</span></span>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const wrap = $(".kf-rowwrap"), play = $(".ex-play"), speed = $(".ex-speed");
      const sync = () => {
        const i = kfPresets.findIndex(([, a, k]) => a.join("") === st.a.join("") && k === st.k);
        $(".kf-preset").value = i < 0 ? "custom" : String(i);
        $(".kf-bits").value = st.a.join("");
        $(".kf-k").value = String(st.k);
      };
      const table = (ev, s) => {
        const { a, k } = st, n = a.length, m = n - k;            // windows start at 0 .. m
        const done = ev.slice(0, s), last = s ? done[s - 1] : null;
        const chosen = done.filter((e) => e.act === "start").map((e) => e.i);
        const now = a.slice();
        chosen.forEach((p) => { for (let j = p; j < p + k; j++) now[j] ^= 1; });
        const cur = last ? last.i : -1;
        const col = (j) => (j === cur ? " is-cur" : "") + (j > m ? " is-nostart" : "");
        let h = `<table class="kf-tab" dir="ltr"><thead><tr><th scope="col"><span class="kf-sr">השורה</span></th>`;
        for (let j = 0; j < n; j++) h += `<th scope="col" class="kf-ix${col(j)}">${j}</th>`;
        h += `</tr></thead><tbody><tr><th scope="row">a</th>`;
        for (let j = 0; j < n; j++) {
          h += `<td class="kf-c${col(j)}"><button type="button" class="kf-bit${a[j] ? " kf-one" : ""}" data-at="${j}" tabindex="${j === st.focus ? 0 : -1}" ` +
            `aria-label="ביט ${j}${NB}: ${a[j]}. לחיצה הופכת אותו">${a[j]}</button></td>`;
        }
        h += `</tr><tr><th scope="row">עכשיו</th>`;
        for (let j = 0; j < n; j++) {
          const bad = last && last.act === "fail" && j === cur;
          h += `<td class="kf-c${col(j)}"><span class="kf-b${now[j] ? " kf-one" : ""}${bad ? " is-bad" : ""}">${now[j]}</span></td>`;
        }
        h += `</tr>`;
        const lanes = m >= 0 ? Math.min(k, m + 1) : 0;
        for (let L = 0; L < lanes; L++) {
          h += `<tr class="kf-lane"><th scope="row"><span class="kf-sr">חלונות</span></th>`;
          for (let j = 0; j < n;) {
            if (j % k === L && chosen.includes(j)) {
              const isNew = last && last.act === "start" && last.i === j, open = j + k > cur;
              h += `<td colspan="${k}" class="kf-wcell"><span class="kf-win${isNew ? " is-new" : open ? " is-open" : " is-closed"}" title="window ${j} .. ${j + k - 1}">${j}</span></td>`;
              j += k;
            } else { h += `<td class="kf-c${col(j)}"></td>`; j++; }
          }
          h += `</tr>`;
        }
        h += `<tr><th scope="row">חלון</th>`;
        for (let j = 0; j < n; j++) {
          const e = j < s ? done[j] : null;
          const txt = !e ? (j > m ? "–" : "·") : e.act === "start" ? "1" : e.act === "skip" ? "0" : e.act === "check" ? "✓" : "✗";
          const cls = !e ? "" : e.act === "start" ? " is-start" : e.act === "fail" ? " is-bad" : e.act === "check" ? " is-ok" : "";
          h += `<td class="kf-c${col(j)}"><span class="kf-x${cls}">${txt}</span></td>`;
        }
        return h + `</tr></tbody></table>`;
      };
      const draw = (focus = false) => {
        const { a, k } = st, n = a.length, m = n - k, ev = kfScan(a, k), T = ev.length;
        st.s = Math.min(Math.max(st.s, 0), T);
        const s = st.s, last = s ? ev[s - 1] : null, done = s === T;
        $(".ex-pos").textContent = `צעד ${s} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        const sl = wrap.scrollLeft;
        wrap.innerHTML = table(ev, s);
        wrap.scrollLeft = sl;
        if (focus) { const b = wrap.querySelector(`.kf-bit[data-at="${st.focus}"]`); if (b) b.focus(); }
        const flips = ev.slice(0, s).filter((e) => e.act === "start").length;
        const starts = ev.slice(0, s).filter((e) => e.act === "start").map((e) => e.i);
        const where = m >= 0 ? `חלון יכול להתחיל בביטים 0 עד ${ltr(m)}` : `${ltr(`k > n`)}${NB}: שום חלון לא נכנס במערך`;
        let sum, note, state;
        if (!last) {
          sum = `${ltr(n)} ביטים, ${ltr(`k = ${k}`)}. ${where}.`;
          note = st.err ? `<span class="kf-err">${st.err}</span>` :
            `הסריקה עוברת משמאל לימין. בכל ביט הערך שלו עכשיו הוא ${ltr("a[i]")} XOR הזוגיות של החלונות הפתוחים מעליו, וממנו ההחלטה אם לפתוח בו חלון.`;
          state = `התור${NB}: ריק · הזוגיות${NB}: 0 · היפוכים${NB}: 0`;
        } else {
          const { i, par, now } = last, open = last.open, more = last.act === "start" ? open.concat([i]) : open;
          const openTxt = open.length ? `${plural(open.length, "חלון פתוח", "חלונות פתוחים")} מעליו, ${listOf(open)}` : "אין מעליו חלון פתוח";
          sum = `צעד ${s}${NB}: ביט ${ltr(i)}, ${ltr(`a = ${last.a}`)}. ${openTxt}, הזוגיות ${par}, ולכן הוא ${now} עכשיו.`;
          if (last.act === "start") note = `ביט ${ltr(i)} הוא 0 עכשיו. כל החלונות שמכסים אותו, מ-${ltr(Math.max(0, i - k + 1))} עד ${ltr(i)}, כבר הוחלטו חוץ מזה שמתחיל ב-${ltr(i)}${NB}: <strong>חייבים לפתוח אותו</strong>.`;
          else if (last.act === "skip") note = `ביט ${ltr(i)} כבר 1. חלון ב-${ltr(i)} היה הופך אותו ל-0, ואף חלון שעוד לא הוחלט לא מכסה אותו${NB}: <strong>אסור לפתוח חלון כאן</strong>.`;
          else if (last.act === "check") note = `ביט ${ltr(i)} אחרי ${ltr(`n − k = ${m}`)}${NB}: שום חלון לא מתחיל בו, וכל החלונות שמכסים אותו כבר הוחלטו. הוא רק נבדק, והוא 1.`;
          else note = `<strong>אין פתרון.</strong> ביט ${ltr(i)} אחרי ${ltr(`n − k = ${m}`)} נשאר 0, וכל החלונות שמכסים אותו כבר הוחלטו${NB}: אין חלון שיתקן אותו.`;
          state = `התור אחרי ביט ${ltr(i)}${NB}: ${more.length ? listOf(more) : "ריק"} · הזוגיות${NB}: ${more.length % 2} · היפוכים${NB}: ${ltr(flips)}`;
        }
        $(".kf-sum").innerHTML = sum;
        $(".kf-note").innerHTML = note;
        $(".kf-state").innerHTML = state;
        if (done && T) {
          const fail = ev[T - 1].act === "fail";
          answer(box, fail ? `${ltr("−1")}${NB}: ביט ${ltr(ev[T - 1].i)} נשאר 0, ואין חלון שיכול לתקן אותו.`
            : flips ? `${plural(flips, "היפוך אחד", "היפוכים")}, בחלונות שמתחילים ב-${listOf(starts)}. זה הפתרון היחיד, ולכן גם הקצר ביותר.`
              : `כל הביטים כבר 1${NB}: אפס היפוכים.`,
          fail ? ".kf-x.is-bad" : ".kf-x.is-start");
        } else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= kfScan(st.a, st.k).length, restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; draw(); };
      const set = (a, k) => { st.a = a; st.k = k; st.err = ""; st.focus = Math.min(st.focus, a.length - 1); sync(); restart(); };
      $(".kf-preset").addEventListener("change", () => {
        const pr = kfPresets[Number($(".kf-preset").value)];
        if (!pr || $(".kf-preset").value === "custom") { sync(); return; }
        set(pr[1].slice(), pr[2]);
      });
      $(".kf-bits").addEventListener("change", () => {
        const v = kfParse($(".kf-bits").value);
        if (!v) { st.err = `צריך בין 1 ל-${NMAX} ביטים, רק 0 ו-1.`; stop(); st.s = 0; draw(); return; }
        set(v, st.k);
      });
      $(".kf-k").addEventListener("change", () => {
        const v = clampK($(".kf-k").value, KMAX, null);
        if (v === null) { st.err = `‏k הוא מספר שלם מ-1 עד ${KMAX}.`; $(".kf-k").value = String(st.k); stop(); st.s = 0; draw(); return; }
        set(st.a, v);
      });
      wrap.addEventListener("click", (e) => {
        const b = e.target.closest(".kf-bit");
        if (!b) return;
        const j = Number(b.dataset.at), a = st.a.slice();
        a[j] ^= 1; st.focus = j;
        st.a = a; st.err = ""; sync(); stop(); st.s = 0; draw(true);
      });
      roving(wrap, ".kf-bit", (el, key) => {
        const j = Number(el.dataset.at), n = st.a.length;
        const to = key === "ArrowRight" ? j + 1 : key === "ArrowLeft" ? j - 1 : key === "Home" ? 0 : key === "End" ? n - 1 : null;
        if (to === null) return null;
        st.focus = Math.min(n - 1, Math.max(0, to));
        return st.focus;
      });
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = kfScan(st.a, st.k).length; draw(); });
      $(".ex-reset").addEventListener("click", () => { st.focus = 0; set(a0.slice(), k0); });
      box.dvqExtra = {
        get: () => (st.s ? String(st.s) : ""),
        set: (t) => { if (!/^\d{1,3}$/.test(String(t))) return false; st.s = Number(t); draw(); return true; },
      };
      sync();
      draw();
    },
  });

  // --- the grid --------------------------------------------------------------------------------

  const gridView = () => ({
    mount(box) {
      const g0 = kf2Parse(box.dataset.grid) || kf2Presets[0][1].map((r) => r.slice());
      const k0 = clampK(box.dataset.k, K2MAX, 2);
      const st = { g: g0.map((r) => r.slice()), k: k0, s: 0, focus: 0, err: "" };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הלוח <select class="kf2-preset" aria-label="איזה לוח">${kf2Presets.map(([name], i) => `<option value="${i}">${name}</option>`).join("")}<option value="custom">משלכם</option></select></label>` +
        `<label>השורות <input type="text" class="kf2-grid" dir="ltr" spellcheck="false" autocomplete="off" aria-label="השורות של הלוח, מופרדות בנקודות, עד ${GMAX} שורות של עד ${GMAX} ביטים"></label>` +
        `<label>‏k <input type="number" class="kf2-k" min="1" max="${K2MAX}" step="1" dir="ltr" inputmode="numeric" aria-label="k, הצלע של הריבוע"></label>` +
        `<button type="button" class="md-button kf2-rand">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        playRow() +
        `<p class="ex-summary kf2-sum" aria-live="polite"></p>` +
        `<div class="kf2-boardwrap"></div>` +
        `<span class="viz-legend kf2-legend"><span><i class="kf-key-one"></i>תא 1</span><span><i class="kf-key-cur"></i>התא של הצעד</span>` +
        `<span><i class="kf-key-new"></i>הריבוע שהצעד פתח</span><span><i class="kf-key-sq"></i>ריבוע שנבחר קודם</span>` +
        `<span><i class="kf-key-band"></i>שום ריבוע לא מתחיל כאן${NB}: רק בדיקה</span></span>` +
        `<div class="kf2-side"></div>` +
        `<p class="kf2-note"></p>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const wrap = $(".kf2-boardwrap"), play = $(".ex-play"), speed = $(".ex-speed");
      const sync = () => {
        const i = kf2Presets.findIndex(([, g, k]) => g.map((r) => r.join("")).join(".") === st.g.map((r) => r.join("")).join(".") && k === st.k);
        $(".kf2-preset").value = i < 0 ? "custom" : String(i);
        $(".kf2-grid").value = st.g.map((r) => r.join("")).join(".");
        $(".kf2-k").value = String(st.k);
      };
      const small = (cls, label, rows, cellOf) => {
        let h = `<figure class="kf2-mini ${cls}"><figcaption>${label}</figcaption><div class="kf2-mgrid" dir="ltr" style="--kf-cols:${rows[0].length}" role="img" aria-label="${label}">`;
        rows.forEach((row, r) => row.forEach((v, c) => { h += cellOf(v, r, c); }));
        return h + `</div></figure>`;
      };
      const draw = (focus = false) => {
        const { g, k } = st, R = g.length, C = g[0].length, ev = kf2Scan(g, k), T = ev.length;
        st.s = Math.min(Math.max(st.s, 0), T);
        const s = st.s, last = s ? ev[s - 1] : null, done = s === T;
        const { d, p, chosen } = kf2State(g, k, s);
        $(".ex-pos").textContent = `צעד ${s} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        const now = g.map((row) => row.slice());
        chosen.forEach(([r0, c0]) => { for (let r = r0; r < r0 + k; r++) for (let c = c0; c < c0 + k; c++) now[r][c] ^= 1; });
        const band = (r, c) => r + k > R || c + k > C;
        const seen = new Map(ev.slice(0, s).map((e) => [e.r * C + e.c, e]));
        let h = `<div class="kf2-board" dir="ltr" role="group" style="--kf-cols:${C}" aria-label="לוח של ${R} על ${C}${NB}: התאים עכשיו. לחיצה על תא הופכת אותו בלוח ההתחלתי">`;
        for (let r = 0; r < R; r++) {
          for (let c = 0; c < C; c++) {
            const at = r * C + c, e = seen.get(at), isCur = last && last.r === r && last.c === c;
            const cls = `kf2-cell${now[r][c] ? " kf-one" : ""}${band(r, c) ? " is-band" : ""}${isCur ? " is-cur" : ""}` +
              `${e && e.act === "fail" ? " is-bad" : ""}${e && e.act === "check" ? " is-ok" : ""}`;
            h += `<button type="button" class="${cls}" data-at="${at}" tabindex="${at === st.focus ? 0 : -1}" style="grid-row:${r + 1};grid-column:${c + 1}" ` +
              `aria-label="תא ${r}, ${c}${NB}: ${now[r][c]} עכשיו, ${g[r][c]} בהתחלה. לחיצה הופכת אותו">${now[r][c]}</button>`;
          }
        }
        chosen.forEach(([r, c]) => {
          const isNew = last && last.act === "start" && last.r === r && last.c === c;
          h += `<span class="kf2-sq${isNew ? " is-new" : ""}" style="grid-row:${r + 1} / span ${k};grid-column:${c + 1} / span ${k}" aria-hidden="true"><i></i></span>`;
        });
        h += `</div>`;
        wrap.innerHTML = h;
        if (focus) { const b = wrap.querySelector(`.kf2-cell[data-at="${st.focus}"]`); if (b) b.focus(); }
        const lastNew = last && last.act === "start" ? [[last.r, last.c + k], [last.r + k, last.c], [last.r + k, last.c + k]] : [];
        $(".kf2-side").innerHTML =
          small("kf2-d", `‏d${NB}: הפינות`, d, (v, r, c) => `<span class="kf2-m${v ? " is-corner" : ""}${r === R || c === C ? " is-out" : ""}${lastNew.some(([a, b]) => a === r && b === c) ? " is-new" : ""}">${v}</span>`) +
          small("kf2-p", `‏p${NB}: הזוגיות`, p, (v, r, c) => `<span class="kf2-m${v ? " kf-one" : ""}${last && last.r === r && last.c === c ? " is-cur" : ""}">${v === null ? "·" : v}</span>`);
        const flips = chosen.length;
        let sum, note;
        if (!last) {
          sum = `לוח של ${ltr(`${R} × ${C}`)}, ריבועים של ${ltr(`${k} × ${k}`)}. ריבוע יכול להתחיל בשורות 0 עד ${ltr(R - k)} ובעמודות 0 עד ${ltr(C - k)}.`;
          if (R < k || C < k) sum = `לוח של ${ltr(`${R} × ${C}`)}, ריבועים של ${ltr(`${k} × ${k}`)}${NB}: שום ריבוע לא נכנס בלוח.`;
          note = st.err ? `<span class="kf-err">${st.err}</span>` :
            `הסריקה עוברת שורה אחרי שורה. בכל תא הזוגיות ${ltr("p")} באה מ-${ltr("d")} ומשלושה שכנים שכבר חושבו, והתא עכשיו הוא ${ltr("g XOR p")}.`;
        } else {
          const { r, c, par, now: v } = last, cell = ltr(`(${r}, ${c})`);
          sum = `צעד ${s}${NB}: התא ${cell}, ${ltr(`g = ${g[r][c]}`)}, הזוגיות של הריבועים מעליו ${par}, ולכן הוא ${v} עכשיו. עד עכשיו ${plural(flips, "ריבוע אחד", "ריבועים")}.`;
          if (last.act === "start") note = `כל ריבוע אחר שמכסה את ${cell} מתחיל בתא שהסריקה כבר עברה${NB}: <strong>חייבים לפתוח ריבוע כאן</strong>. שלוש פינות שלו מתהפכות ב-${ltr("d")}, והרביעית היא התא עצמו, ולכן מתהפך ה-${ltr("p")} שלו.`;
          else if (last.act === "skip") note = `התא כבר 1, וריבוע שמתחיל בו היה הופך אותו ל-0${NB}: <strong>אסור לפתוח ריבוע כאן</strong>.`;
          else if (last.act === "check") note = `ריבוע שמתחיל ב-${cell} היה יוצא מהלוח. כל הריבועים שמכסים את התא כבר הוחלטו, והוא רק נבדק${NB}: 1.`;
          else note = `<strong>אין פתרון.</strong> התא ${cell} נשאר 0, ריבוע לא יכול להתחיל בו, וכל הריבועים שמכסים אותו כבר הוחלטו.`;
        }
        $(".kf2-sum").innerHTML = sum;
        $(".kf2-note").innerHTML = note;
        if (done && T) {
          const e = ev[T - 1];
          if (e.act === "fail") answer(box, `${ltr("−1")}${NB}: התא ${ltr(`(${e.r}, ${e.c})`)} נשאר 0, ואין ריבוע שיכול לתקן אותו.`, ".kf2-cell.is-bad");
          else answer(box, flips ? `${plural(flips, "ריבוע אחד", "ריבועים")}, מהפינות ${ltr(chosen.map(([r, c]) => `(${r}, ${c})`).join(" "))}. הפתרון היחיד.` : `כל התאים כבר 1${NB}: אפס היפוכים.`, ".kf2-sq");
        } else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= kf2Scan(st.g, st.k).length, restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; draw(); };
      const set = (g, k) => { st.g = g; st.k = k; st.err = ""; st.focus = Math.min(st.focus, g.length * g[0].length - 1); sync(); restart(); };
      $(".kf2-preset").addEventListener("change", () => {
        const pr = kf2Presets[Number($(".kf2-preset").value)];
        if (!pr || $(".kf2-preset").value === "custom") { sync(); return; }
        set(pr[1].map((r) => r.slice()), pr[2]);
      });
      $(".kf2-grid").addEventListener("change", () => {
        const v = kf2Parse($(".kf2-grid").value);
        if (!v) { st.err = `צריך עד ${GMAX} שורות באותו אורך, עד ${GMAX} ביטים בכל אחת, מופרדות בנקודות.`; stop(); st.s = 0; draw(); return; }
        set(v, st.k);
      });
      $(".kf2-k").addEventListener("change", () => {
        const v = clampK($(".kf2-k").value, K2MAX, null);
        if (v === null) { st.err = `‏k הוא מספר שלם מ-1 עד ${K2MAX}.`; $(".kf2-k").value = String(st.k); stop(); st.s = 0; draw(); return; }
        set(st.g, v);
      });
      // a random grid that can be fixed: a random set of squares on a board of ones
      $(".kf2-rand").addEventListener("click", () => {
        const R = st.g.length, C = st.g[0].length, k = st.k;
        const g = Array.from({ length: R }, () => new Array(C).fill(1));
        for (let r = 0; r + k <= R; r++) for (let c = 0; c + k <= C; c++) {
          if (Math.random() < 0.35) for (let i = r; i < r + k; i++) for (let j = c; j < c + k; j++) g[i][j] ^= 1;
        }
        set(g, k);
      });
      wrap.addEventListener("click", (e) => {
        const b = e.target.closest(".kf2-cell");
        if (!b) return;
        const at = Number(b.dataset.at), C = st.g[0].length, g = st.g.map((r) => r.slice());
        g[Math.floor(at / C)][at % C] ^= 1; st.focus = at;
        st.g = g; st.err = ""; sync(); stop(); st.s = 0; draw(true);
      });
      roving(wrap, ".kf2-cell", (el, key) => {
        const at = Number(el.dataset.at), R = st.g.length, C = st.g[0].length;
        let r = Math.floor(at / C), c = at % C;
        const moves = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] };
        if (key === "Home") c = 0; else if (key === "End") c = C - 1; else if (moves[key]) {
          r = Math.min(R - 1, Math.max(0, r + moves[key][0])); c = Math.min(C - 1, Math.max(0, c + moves[key][1]));
        } else return null;
        st.focus = r * C + c;
        return st.focus;
      });
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = kf2Scan(st.g, st.k).length; draw(); });
      $(".ex-reset").addEventListener("click", () => { st.focus = 0; set(g0.map((r) => r.slice()), k0); });
      box.dvqExtra = {
        get: () => (st.s ? String(st.s) : ""),
        set: (t) => { if (!/^\d{1,3}$/.test(String(t))) return false; st.s = Number(t); draw(); return true; },
      };
      sync();
      draw();
    },
  });

  dvqExplorers.register({
    views: { kflip: rowView, kflip2: gridView },
    help: {
      kflip: "בוחרים מערך, כותבים עד 20 ביטים או לוחצים על ביט כדי להפוך אותו, ובוחרים k. כל צעד מחליט על ביט אחד, משמאל לימין : הערך שלו עכשיו הוא הביט XOR הזוגיות של החלונות הפתוחים מעליו, ואם הוא 0 חייבים לפתוח בו חלון. מתחת לביטים החלונות שנבחרו, ובשורה האחרונה ההחלטה על כל ביט. בביטים שאחרי n − k שום חלון לא מתחיל, והם רק נבדקים.",
      kflip2: "בוחרים לוח, כותבים את השורות מופרדות בנקודות, לוחצים על תא כדי להפוך אותו או מגרילים לוח שאפשר לתקן. כל צעד מחליט על תא אחד, שורה אחרי שורה : אם הוא 0 עכשיו חייבים לפתוח בו ריבוע. בתאים המוצללים שום ריבוע לא מתחיל, והם רק נבדקים. בצד מערך ההפרשים d של העמוד והזוגיות p של כל תא שנסרק.",
    },
    cols: { kflip2: { main: ".kf2-boardwrap", side: ".kf2-legend, .kf2-side, .kf2-note", w: "min-content" } },   // the board (as wide as it needs) beside the legend, d and p
    models: { kfParse, kfScan, kf2Parse, kf2Scan, kf2State, kfPresets, kf2Presets },
  });
})();
