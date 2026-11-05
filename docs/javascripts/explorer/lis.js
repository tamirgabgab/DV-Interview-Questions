// kinds: lis
//   lis                    0084        the longest increasing subsequence of an array (data-nums, a text field, presets and a random draw) in two modes: dp (data-mode="dp"), every comparison of a[j] with a[i] its own step, the rows len and cnt under the array and the prev arcs above it, the LIS and how many there are at the end; tails, every comparison of the binary search (lo, hi, mid) and every insertion into tails its own step, the parent arcs above the array, the LIS reconstructed at the end
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = "\u00a0";
  const NMAX = 12, VMIN = -99, VMAX = 999;
  const MODES = { dp: "DP, סעיפים א ו-ג", tails: "מערך tails, סעיף ב" };
  const PRESETS = [
    ["הדוגמה של הדף", "10 9 2 5 3 7 101 18"],
    ["שתי סדרות", "1 3 5 4 7"],
    ["tails שאינו LIS", "3 4 5 1"],
    ["ערכים שווים", "2 2 2 2 2"],
    ["יורד", "5 4 3 2 1"],
  ];

  // --- the models ------------------------------------------------------------------------------

  // the array from the text field: 1 to NMAX integers between VMIN and VMAX, separated by
  // spaces or commas; null otherwise
  const lisParse = (text) => {
    const parts = String(text).trim().split(/[\s,]+/).filter(Boolean);
    if (!parts.length || parts.length > NMAX) return null;
    const out = [];
    for (const p of parts) {
      if (!/^-?\d+$/.test(p)) return null;
      const v = Number(p);
      if (v < VMIN || v > VMAX) return null;
      out.push(v);
    }
    return out;
  };
  // part a and c: one step per comparison of a[j] with a[i] (j < i), and one "init" step when
  // i starts; kind: init, longer (dp[i] grows, cnt[i] = cnt[j]), tie (cnt[i] += cnt[j]),
  // shorter (a[j] < a[i] but no gain) or skip (a[j] >= a[i]); len, cnt and prev after the step
  const lisDpSteps = (a) => {
    const n = a.length, len = new Array(n).fill(0), cnt = new Array(n).fill(0), prev = new Array(n).fill(-1), out = [];
    const snap = (i, j, kind) => out.push({ i, j, kind, len: len.slice(), cnt: cnt.slice(), prev: prev.slice() });
    for (let i = 0; i < n; i++) {
      len[i] = 1; cnt[i] = 1;
      snap(i, -1, "init");
      for (let j = 0; j < i; j++) {
        let kind = "skip";
        if (a[j] < a[i]) {
          if (len[j] + 1 > len[i]) { len[i] = len[j] + 1; cnt[i] = cnt[j]; prev[i] = j; kind = "longer"; }
          else if (len[j] + 1 === len[i]) { cnt[i] += cnt[j]; kind = "tie"; }
          else kind = "shorter";
        }
        snap(i, j, kind);
      }
    }
    return out;
  };
  // the result of part a and c: { best, count, seq (the indices of one LIS: from the first
  // index with the largest len, back along prev) }
  const lisDpResult = (a) => {
    const s = lisDpSteps(a), last = s.length ? s[s.length - 1] : { len: [], cnt: [], prev: [] };
    const best = Math.max(0, ...last.len);
    const count = last.len.reduce((t, l, i) => t + (l === best ? last.cnt[i] : 0), 0);
    const seq = [];
    for (let i = last.len.indexOf(best); i >= 0 && best > 0; i = last.prev[i]) seq.unshift(i);
    return { best, count, seq };
  };
  // part b: one step per comparison of the binary search (kind "probe": lo, hi, mid and
  // whether tails[mid] < x, before lo or hi moves) and one per insertion (kind "append" or
  // "replace" at k, with old the value replaced); tails, at (tail_at) and parent after it
  const lisTailsSteps = (a) => {
    const tails = [], at = [], parent = new Array(a.length).fill(-1), out = [];
    a.forEach((x, i) => {
      let lo = 0, hi = tails.length;
      while (lo < hi) {
        const mid = (lo + hi) >> 1, less = tails[mid] < x;
        out.push({ i, x, kind: "probe", lo, hi, mid, less, tails: tails.slice(), at: at.slice(), parent: parent.slice() });
        if (less) lo = mid + 1; else hi = mid;
      }
      const append = lo === tails.length, old = append ? null : tails[lo];
      if (append) { tails.push(x); at.push(i); } else { tails[lo] = x; at[lo] = i; }
      parent[i] = lo ? at[lo - 1] : -1;
      out.push({ i, x, kind: append ? "append" : "replace", k: lo, old, tails: tails.slice(), at: at.slice(), parent: parent.slice() });
    });
    return out;
  };
  // the indices of the LIS of part b: from the end of tails back along parent
  const lisTailsSeq = (a) => {
    const s = lisTailsSteps(a);
    if (!s.length) return [];
    const last = s[s.length - 1], seq = [];
    for (let i = last.at[last.at.length - 1]; i >= 0; i = last.parent[i]) seq.unshift(i);
    return seq;
  };

  // --- the drawing -------------------------------------------------------------------------------

  const C = 36, G = 6, LW = 52, CY = 52;
  const cx = (i) => LW + i * (C + G) + C / 2;
  const arc = (p, i, cls) => {
    const h = Math.min(30, 6 + 6 * (i - p)), x1 = cx(p), x2 = cx(i);
    return `<path class="${cls}" d="M${x1},${CY - 2} Q${(x1 + x2) / 2},${CY - 2 - 2 * h} ${x2},${CY - 2}"/>`;
  };
  const label = (y, t) => `<text class="lis-lab" x="${LW - 10}" y="${y}" text-anchor="end">${t}</text>`;
  // the array row: cell classes per index (cls(i) → extra classes)
  const arrayRow = (a, cls) => {
    let s = label(CY + C / 2 + 5, "a");
    a.forEach((v, i) => {
      const x = LW + i * (C + G);
      s += `<text class="lis-idx" x="${cx(i)}" y="14" text-anchor="middle">${i}</text>` +
        `<rect class="lis-cell${cls(i)}" x="${x}" y="${CY}" width="${C}" height="${C}" rx="3"/>` +
        `<text class="lis-v" x="${cx(i)}" y="${CY + C / 2 + 6}" text-anchor="middle">${v}</text>`;
    });
    return s;
  };
  const valRow = (n, y, name, val, cls) => {
    let s = label(y + 20, name);
    for (let i = 0; i < n; i++) {
      const v = val(i), x = LW + i * (C + G);
      s += `<rect class="lis-val${cls(i)}" x="${x}" y="${y}" width="${C}" height="28" rx="3"/>` +
        `<text class="lis-num" x="${cx(i)}" y="${y + 19}" text-anchor="middle">${v === null ? "" : v}</text>`;
    }
    return s;
  };
  const svgOf = (w, h, aria, body) =>
    `<svg class="figure lis-live" viewBox="0 0 ${w} ${h}" style="max-width:${(w / 16).toFixed(1)}rem" role="img" aria-label="${aria}">${body}</svg>`;
  const width = (n) => LW + n * (C + G) - G + 8;

  // the dp mode: the array, len and cnt under it, the prev arcs of the finished indices
  const dpSvg = (a, step, seq) => {
    const n = a.length, i = step ? step.i : -1, j = step ? step.j : -1;
    const lit = new Set(seq || []);
    let s = "";
    if (step) {
      for (let k = 1; k <= i; k++) {
        const p = step.prev[k];
        if (p >= 0 && !(lit.has(k) && lit.has(p))) s += arc(p, k, `lis-link${k === i && !seq ? " is-now" : ""}`);
      }
      seq && seq.slice(1).forEach((k, m) => { s += arc(seq[m], k, "lis-link is-chain"); });
    }
    const live = step && !seq;                        // the step's marks, gone once the answer is shown
    s += arrayRow(a, (k) => (lit.has(k) ? " is-lis" : "") + (live && k === i ? " is-cur" : "") + (live && k === j ? (step.kind === "skip" ? " is-no" : " is-cmp") : ""));
    const shown = (k) => step && k <= i;
    s += valRow(n, 100, "len", (k) => (shown(k) ? step.len[k] : null), (k) => (shown(k) ? "" : " is-off") + (live && k === i ? " is-cur" : "") + (lit.has(k) ? " is-lis" : ""));
    s += valRow(n, 136, "cnt", (k) => (shown(k) ? step.cnt[k] : null), (k) => (shown(k) ? "" : " is-off") + (live && k === i ? " is-cur" : ""));
    const aria = step ? `המערך ${a.join(" ")}. i = ${i}${j >= 0 ? `, j = ${j}` : ""}. len עד i : ${step.len.slice(0, i + 1).join(" ")}; cnt : ${step.cnt.slice(0, i + 1).join(" ")}` : `המערך ${a.join(" ")}, לפני הצעד הראשון`;
    return svgOf(width(n), 172, aria, s);
  };
  // the tails mode: the parent arcs over the array, tails under it with tail_at, and the
  // range [lo, hi) of the search with mid
  const tailsSvg = (a, step, seq) => {
    const n = a.length, i = step ? step.i : -1, lit = new Set(seq || []);
    let s = "";
    if (step) {
      for (let k = 1; k <= i; k++) {
        const p = step.parent[k];
        if (p >= 0 && !(lit.has(k) && lit.has(p))) s += arc(p, k, `lis-link${k === i && step.kind !== "probe" && !seq ? " is-now" : ""}`);
      }
      seq && seq.slice(1).forEach((k, m) => { s += arc(seq[m], k, "lis-link is-chain"); });
    }
    const live = step && !seq;
    s += arrayRow(a, (k) => (lit.has(k) ? " is-lis" : "") + (live && k === i ? " is-cur" : "") + (!step || k > i ? " is-todo" : ""));
    const T = 110, tails = step ? step.tails : [], at = step ? step.at : [];
    s += label(T + 23, "tails");
    for (let k = 0; k < n; k++) {
      const x = LW + k * (C + G), has = k < tails.length;
      let cls = has ? "" : " is-off";
      if (step && step.kind === "probe") {
        if (k >= step.lo && k < step.hi) cls += " is-range";
        if (k === step.mid) cls += " is-mid";
      } else if (live && k === step.k) cls += step.kind === "append" ? " is-new" : " is-rep";
      s += `<rect class="lis-val lis-tail${cls}" x="${x}" y="${T}" width="${C}" height="32" rx="3"/>` +
        `<text class="lis-num" x="${cx(k)}" y="${T + 21}" text-anchor="middle">${has ? tails[k] : ""}</text>` +
        (has ? `<text class="lis-at" x="${cx(k)}" y="${T + 48}" text-anchor="middle">a[${at[k]}]</text>` : "");
    }
    s += label(T + 48, "at");
    if (step && step.kind === "probe") {
      const mark = (k, y, t) => `<text class="lis-mark" x="${k < n ? cx(k) : cx(n - 1) + C / 2 + 4}" y="${y}" text-anchor="${k < n ? "middle" : "start"}">${t}</text>`;
      s += mark(step.lo, T + 68, "lo") + mark(step.hi, T + 86, "hi");
    } else if (live) {
      s += `<text class="lis-mark" x="${cx(step.k)}" y="${T + 68}" text-anchor="middle">k</text>`;
    }
    const aria = step ? `המערך ${a.join(" ")}. x = ${step.x} (i = ${i}). tails : ${tails.join(" ") || "ריק"}` : `המערך ${a.join(" ")}, tails ריק`;
    return svgOf(width(n), T + 94, aria, s);
  };

  // --- the box -------------------------------------------------------------------------------------

  const lisView = () => ({
    mount(box) {
      const mode0 = MODES[box.dataset.mode] ? box.dataset.mode : "dp";
      const nums0 = lisParse(box.dataset.nums || "") || [10, 9, 2, 5, 3, 7, 101, 18];
      const st = { mode: mode0, a: nums0.slice(), k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המצב <select class="lis-mode" aria-label="איזה פתרון">${Object.entries(MODES).map(([v, w]) => `<option value="${v}">${w}</option>`).join("")}</select></label>` +
        `<label><span>המערך</span><input type="text" class="ex-num lis-nums" dir="ltr" spellcheck="false" aria-label="המערך${NB}: עד ${NMAX} מספרים שלמים, מופרדים ברווח"></label>` +
        `<button type="button" class="md-button lis-rand">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err lis-err" role="status"></span></div>` +
        `<div class="ex-controls lis-presets"><span>דוגמאות${NB}:</span>` +
        PRESETS.map(([t, v]) => `<button type="button" class="md-button ex-preset" data-nums="${v}">${t}</button>`).join("") + `</div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1300, 700, 300) +
        `<span class="ex-pos"></span></div>` +
        `<div class="lis-wrap"></div>` +
        `<span class="viz-legend lis-legend"></span>` +
        `<p class="ex-summary lis-sum" aria-live="polite"></p>` +
        `<p class="lis-note"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const steps = () => (st.mode === "dp" ? lisDpSteps(st.a) : lisTailsSteps(st.a));
      const key = (cls, text) => `<span><i class="${cls}"></i><span>${text}</span></span>`;
      const legend = () => (st.mode === "dp"
        ? key("lis-key-cur", ltr("a[i]")) + key("lis-key-cmp", ltr("a[j] < a[i]")) + key("lis-key-no", ltr("a[j] ≥ a[i]")) +
          key("lis-key-chain", `קשת ${ltr("prev")}`) + key("lis-key-lis", ltr("LIS"))
        : key("lis-key-cur", ltr("x = a[i]")) + key("lis-key-range", `הטווח ${ltr("[lo, hi)")}`) + key("lis-key-mid", ltr("mid")) +
          key("lis-key-new", "מאריך") + key("fc-key-chg", "מחליף") + key("lis-key-chain", `קשת ${ltr("parent")}`) + key("lis-key-lis", ltr("LIS")));
      const draw = () => {
        const S = steps(), T = S.length, a = st.a, n = a.length;
        st.k = Math.min(Math.max(st.k, 0), T);
        const k = st.k, step = k ? S[k - 1] : null, done = k === T;
        $(".lis-mode").value = st.mode;
        if (document.activeElement !== $(".lis-nums")) $(".lis-nums").value = a.join(" ");
        $(".ex-pos").textContent = `צעד ${k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        $(".lis-legend").innerHTML = legend();
        let sum = "", note = "", ans = null;
        if (st.mode === "dp") {
          const res = done ? lisDpResult(a) : null;
          $(".lis-wrap").innerHTML = dpSvg(a, step, res ? res.seq : null);
          if (!step) {
            sum = `במערך ${ltr(n)} איברים. כל צעד משווה ${ltr("a[j]")} ל-${ltr("a[i]")}, ובסך הכול ${ltr(n * (n - 1) / 2)} השוואות.`;
          } else {
            const { i, j } = step;
            sum = (j >= 0 ? `משווים את ${ltr(`a[${j}] = ${a[j]}`)} ל-${ltr(`a[${i}] = ${a[i]}`)}. ` : `האיבר ${ltr(`a[${i}] = ${a[i]}`)} מתחיל. `) +
              `עכשיו ${ltr(`len[${i}] = ${step.len[i]}`)} ו-${ltr(`cnt[${i}] = ${step.cnt[i]}`)}.`;
            const lj = j >= 0 ? step.len[j] : 0;
            note = {
              init: `האיבר ${ltr(a[i])} לבדו הוא תת-סדרה עולה${NB}: ${ltr("len = 1")}, ${ltr("cnt = 1")}.` + (i ? ` עכשיו משווים אותו לכל אחד מ-${ltr(i)} האיברים שלפניו.` : " אין איברים לפניו."),
              skip: `הערך ${ltr(a[j])} לא קטן מ-${ltr(a[i])}${NB}: אי אפשר לשים את ${ltr(a[i])} אחריו בסדרה עולה ממש.`,
              longer: `הערך ${ltr(a[j])} קטן מ-${ltr(a[i])}, ו-${ltr(`len[${j}] + 1 = ${lj + 1}`)} ארוך יותר${NB}: אורך חדש, ${ltr(`prev[${i}] = ${j}`)}, וה-${ltr("cnt")} מתחיל מחדש מ-${ltr(`cnt[${j}] = ${step.cnt[j]}`)}.`,
              tie: `הערך ${ltr(a[j])} קטן מ-${ltr(a[i])}, ו-${ltr(`len[${j}] + 1 = ${lj + 1}`)} הוא אותו אורך${NB}: עוד ${ltr(step.cnt[j])} ${step.cnt[j] === 1 ? "סדרה" : "סדרות"}, ${ltr(`cnt[${i}] = ${step.cnt[i]}`)}. המצביע ${ltr("prev")} לא משתנה.`,
              shorter: `הערך ${ltr(a[j])} קטן מ-${ltr(a[i])}, אבל ${ltr(`len[${j}] + 1 = ${lj + 1}`)} קצר מ-${ltr(step.len[i])}${NB}: אין שינוי.`,
            }[step.kind];
          }
          if (done && res) {
            ans = n ? `האורך ${ltr(res.best)}, ${res.count === 1 ? "ויש תת-סדרה אחת כזו" : `ויש ${ltr(res.count)} תתי-סדרות כאלה`}. אחת מהן${NB}: ${ltr(res.seq.map((x) => a[x]).join(", "))}.` : null;
          }
        } else {
          const seq = done ? lisTailsSeq(a) : null;
          $(".lis-wrap").innerHTML = tailsSvg(a, step, seq);
          if (!step) {
            sum = `במערך ${ltr(n)} איברים. כל צעד הוא השוואה אחת של החיפוש הבינארי, או הכנסה של ${ltr("x")} ל-${ltr("tails")}.`;
          } else {
            const t = step.tails;
            sum = `האיבר ${ltr(`x = a[${step.i}] = ${step.x}`)}, ו-${ltr(`tails = [${t.join(", ")}]`)}.`;
            if (step.kind === "probe") {
              note = `מחפשים את ה-${ltr("k")} הראשון עם ${ltr(`tails[k] ≥ ${step.x}`)} בטווח ${ltr(`[${step.lo}, ${step.hi})`)}. ${ltr(`mid = ${step.mid}`)}, ${ltr(`tails[${step.mid}] = ${t[step.mid]}`)}` +
                (step.less ? `, קטן מ-${ltr(step.x)}${NB}: ה-${ltr("k")} מימין ל-mid, ${ltr(`lo = ${step.mid + 1}`)}.` : `, לא קטן מ-${ltr(step.x)}${NB}: ה-${ltr("k")} הוא ${ltr("mid")} או משמאל לו, ${ltr(`hi = ${step.mid}`)}.`);
            } else if (step.kind === "append") {
              note = `${step.k ? `כל הערכים ב-${ltr("tails")} קטנים מ-${ltr(step.x)}` : `המערך ${ltr("tails")} היה ריק`}${NB}: ${ltr(step.x)} מאריך אותו, ${ltr(`k = ${step.k}`)}. יש עכשיו תת-סדרה עולה באורך ${ltr(step.k + 1)}. ` +
                (step.k ? `האיבר שלפניו${NB}: ${ltr(`parent[${step.i}] = ${step.parent[step.i]}`)}, הסוף של סדרה באורך ${ltr(step.k)}.` : `אין איבר לפניו, ${ltr(`parent[${step.i}] = -1`)}.`);
            } else {
              note = `הערך ${ltr(`tails[${step.k}] = ${step.old}`)} הוא הראשון שאינו קטן מ-${ltr(step.x)}${NB}: ${ltr(step.x)} מחליף אותו, וסדרה באורך ${ltr(step.k + 1)} נגמרת עכשיו בערך קטן יותר או שווה. ` +
                (step.k ? `האיבר שלפניו${NB}: ${ltr(`parent[${step.i}] = ${step.parent[step.i]}`)}.` : `אין איבר לפניו, ${ltr(`parent[${step.i}] = -1`)}.`);
            }
          }
          if (done && seq && n) {
            const t = step.tails, same = seq.every((x, m) => a[x] === t[m]);
            ans = `האורך ${ltr(t.length)}, והשחזור לפי ${ltr("parent")}${NB}: ${ltr(seq.map((x) => a[x]).join(", "))}.` +
              (same ? "" : ` שימו לב${NB}: ${ltr(`tails = [${t.join(", ")}]`)} אינו תת-סדרה.`);
          }
        }
        $(".lis-sum").innerHTML = sum;
        $(".lis-note").innerHTML = note;
        answer(box, ans, ".lis-wrap .is-lis");
      };
      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= steps().length, restart: () => { st.k = 0; draw(); } });
      const setArray = (v) => { stop(); st.a = v; st.k = 0; $(".lis-err").textContent = ""; $(".lis-nums").value = v.join(" "); draw(); };
      $(".lis-mode").addEventListener("change", () => { stop(); st.mode = MODES[$(".lis-mode").value] ? $(".lis-mode").value : "dp"; st.k = 0; draw(); });
      $(".lis-nums").addEventListener("change", () => {
        const v = lisParse($(".lis-nums").value);
        if (!v) { $(".lis-err").textContent = `המערך${NB}: 1 עד ${NMAX} מספרים שלמים בין ${VMIN} ל-${VMAX}`; return; }
        setArray(v);
      });
      $(".lis-rand").addEventListener("click", () => {
        const n = 8 + Math.floor(Math.random() * 5);
        setArray(Array.from({ length: n }, () => 1 + Math.floor(Math.random() * 30)));
      });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => setArray(lisParse(b.dataset.nums))));
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = steps().length; draw(); });
      $(".ex-reset").addEventListener("click", () => { st.mode = mode0; setArray(nums0.slice()); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { lis: lisView },
    help: {
      lis: "בוחרים מצב ומערך (מקלידים מספרים מופרדים ברווח, בוחרים דוגמה או מגרילים). במצב DP כל צעד משווה את a[j] ל-a[i]\u00a0: מתחת למערך האורך len והמספר cnt של הסדרות הארוכות ביותר שנגמרות בכל איבר, ומעליו הקשת מ-prev. במצב tails כל צעד הוא השוואה של החיפוש הבינארי (הטווח מ-lo עד hi ו-mid מסומנים) או הכנסה ל-tails, ומעל המערך הקשתות של parent. בסוף ה-LIS מודגש.",
    },
    models: { lisParse, lisDpSteps, lisDpResult, lisTailsSteps, lisTailsSeq },
  });
})();
