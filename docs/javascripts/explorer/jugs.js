// kinds: jugs jugs3
//   jugs                   0083        two jugs a and b with a tap and a sink (sliders a, b and the target T): the steps by hand (fill, empty, pour each way, undo), or the shortest plan of the BFS loaded and played step by step; the jugs with their water, the steps against the minimum, why T cannot be measured (more than the bigger jug, or not a multiple of gcd), and the grid of the pairs (x, y): the reachable ones, the ones never reached, the path so far
//   jugs3                  0083        three jugs without a tap (8, 5 and 3, the 8 full): the six pours by hand or the shortest plan to two halves of 4 played pour by pour, the jugs and the grid of the 5 and the 3 (the 8 holds the rest)
// Loaded after core.js on the pages that have these kinds (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const RLM = "‏";

  // --- the model (tests/0083 compares it with the page's code and the generator) ------------

  // a step is ["fill", i], ["empty", i] or ["pour", i, j]; the order of the page's code:
  // the fills, the empties, then every pour i into j by i, then j
  const jugApply = (caps, s, m) => {
    const n = s.slice();
    if (m[0] === "fill") n[m[1]] = caps[m[1]];
    else if (m[0] === "empty") n[m[1]] = 0;
    else { const d = Math.min(s[m[1]], caps[m[2]] - s[m[2]]); n[m[1]] -= d; n[m[2]] += d; }
    return n;
  };
  const jugSteps = (caps, tap) => {
    const out = [];
    if (tap) {
      caps.forEach((_, i) => out.push(["fill", i]));
      caps.forEach((_, i) => out.push(["empty", i]));
    }
    caps.forEach((_, i) => caps.forEach((__, j) => { if (i !== j) out.push(["pour", i, j]); }));
    return out;
  };
  const same = (a, b) => a.length === b.length && a.every((v, i) => v === b[i]);
  // the states one step away, as [step, state]; a step that changes nothing is left out
  const jugMoves = (caps, s, tap) => jugSteps(caps, tap).map((m) => [m, jugApply(caps, s, m)]).filter(([, n]) => !same(n, s));
  const hits = (target) => (Array.isArray(target) ? (s) => same(s, target) : (s) => s.includes(target));
  // the fewest steps from start to a state with `target` (a number: in one of the jugs; an
  // array: that exact state): [[step, state], ...], or null
  const jugBfs = (caps, start, target, tap) => {
    const goal = hits(target), key = (s) => s.join(","), parent = new Map([[key(start), null]]);
    const queue = [start];
    for (let h = 0; h < queue.length; h++) {
      let s = queue[h];
      if (goal(s)) {
        const path = [];
        while (parent.get(key(s))) { const [s0, m] = parent.get(key(s)); path.push([m, s]); s = s0; }
        return path.reverse();
      }
      for (const [m, n] of jugMoves(caps, s, tap)) {
        if (!parent.has(key(n))) { parent.set(key(n), [s, m]); queue.push(n); }
      }
    }
    return null;
  };
  // the fewest steps to every reachable state: { "x,y": d }
  const jugDist = (caps, start, tap) => {
    const dist = { [start.join(",")]: 0 }, queue = [start];
    for (let h = 0; h < queue.length; h++) {
      const s = queue[h];
      for (const [, n] of jugMoves(caps, s, tap)) {
        const k = n.join(",");
        if (!(k in dist)) { dist[k] = dist[s.join(",")] + 1; queue.push(n); }
      }
    }
    return dist;
  };
  const gcd = (a, b) => (b ? gcd(b, a % b) : a);
  const jugCan = (a, b, t) => t >= 0 && t <= Math.max(a, b) && t % gcd(a, b) === 0;

  // --- drawings ------------------------------------------------------------------------------

  const UNIT = { 2: 18, 3: 13 };
  // the jugs side by side, the first on the left: the water, the amount, the name and the
  // capacity under each; the jugs that changed framed, an arrow over a pour
  const jugsSvg = (caps, s, names, m, aria) => {
    const n = caps.length, unit = Math.min(UNIT[n] || 13, Math.floor(150 / Math.max(...caps))), jw = 58, gap = 40, top = 30;
    const H = top + Math.max(...caps) * unit + 44, W = n * jw + (n - 1) * gap + 24, base = top + Math.max(...caps) * unit;
    const xs = caps.map((_, k) => 12 + k * (jw + gap));
    let out = `<svg class="figure wj-fig wj-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="${aria}">`;
    caps.forEach((c, k) => {
      const x = xs[k], hk = c * unit, wh = s[k] * unit;
      if (wh) out += `<rect class="wj-water" x="${x + 3}" y="${base - wh}" width="${jw - 6}" height="${wh}"/>`;
      for (let lev = 1; lev < c; lev++) out += `<line class="wj-lev" x1="${x}" x2="${x + 7}" y1="${base - lev * unit}" y2="${base - lev * unit}"/>`;
      const chg = m && (m[1] === k || (m[0] === "pour" && m[2] === k));
      out += `<path class="wj-jug${chg ? " wj-chg" : ""}" d="M${x},${base - hk} L${x},${base} L${x + jw},${base} L${x + jw},${base - hk}"/>`;
      const ty = wh ? base - Math.max(wh, unit * 0.9) / 2 + 5 : base - 9;
      out += `<text class="wj-num" x="${x + jw / 2}" y="${ty}" text-anchor="middle">${s[k]}</text>`;
      out += `<text class="wj-name" x="${x + jw / 2}" y="${base + 18}" text-anchor="middle">${names[k]}</text>`;
      out += `<text class="wj-cap" x="${x + jw / 2}" y="${base + 36}" text-anchor="middle" direction="rtl">${c} ליטר</text>`;
    });
    if (m && m[0] === "pour") {
      const [, i, j] = m, x1 = xs[i] + jw / 2, x2 = xs[j] + jw / 2, d = x2 > x1 ? 1 : -1;
      const tx = x2 - d * 8, ty = base - caps[j] * unit - 9;
      out += `<path class="wj-arrow" d="M${x1},${base - caps[i] * unit - 4} Q${(x1 + x2) / 2},4 ${tx},${ty}"/>`;
      out += `<polygon class="wj-head" points="${tx - 5},${ty - 7} ${tx + 5},${ty - 7} ${tx},${ty + 2}"/>`;
    }
    return out + `</svg>`;
  };
  // the states as a grid: jug i0 across, jug i1 up; a dot for every reachable state, a ring
  // for the ones never reached, the goal in green, the path so far and the state now
  const gridSvg = (caps, dist, i0, i1, total, path, now, goal, names) => {
    const ca = caps[i0], cb = caps[i1], cell = Math.min(34, Math.floor(260 / Math.max(ca + 1, cb + 1)));
    const L = 40, T = 12, W = L + cell * (ca + 1) + 12, H = T + cell * (cb + 1) + 34;
    const X = (x) => L + cell * (x + 0.5), Y = (y) => T + cell * (cb - y + 0.5);
    const at = (s) => [s[i0], s[i1]];
    const seen = new Set(Object.keys(dist).map((k) => at(k.split(",").map(Number)).join(",")));
    let out = `<svg class="figure wj-grid" viewBox="0 0 ${W} ${H}" role="img" aria-label="מרחב המצבים : ${names[0]} לרוחב, ${names[1]} לגובה. ${seen.size} מצבים נגישים, והמסלול עד עכשיו">`;
    for (let x = 0; x <= ca; x++) out += `<line class="grid" x1="${X(x)}" x2="${X(x)}" y1="${T}" y2="${T + cell * (cb + 1)}"/><text class="tick" x="${X(x)}" y="${H - 16}" text-anchor="middle">${x}</text>`;
    for (let y = 0; y <= cb; y++) out += `<line class="grid" x1="${L}" x2="${W - 12}" y1="${Y(y)}" y2="${Y(y)}"/><text class="tick" x="${L - 8}" y="${Y(y) + 4}" text-anchor="end">${y}</text>`;
    out += `<text class="tick" x="${W - 12}" y="${H - 2}" text-anchor="end">${names[0]}</text><text class="tick" x="${L - 26}" y="${T + 10}" text-anchor="end">${names[1]}</text>`;
    if (path.length > 1) out += `<polyline class="wj-route" points="${path.map((s) => `${X(s[i0])},${Y(s[i1])}`).join(" ")}" fill="none" stroke-width="3"/>`;
    for (let x = 0; x <= ca; x++) {
      for (let y = 0; y <= cb; y++) {
        if (total !== null) { const rest = total - x - y; if (rest < 0 || rest > caps[3 - i0 - i1]) continue; }
        if (seen.has(`${x},${y}`)) out += `<circle class="${goal(x, y) ? "wj-goal" : "wj-reach"}" cx="${X(x)}" cy="${Y(y)}" r="${(cell * 0.19).toFixed(1)}"/>`;
        else out += `<circle class="wj-never" cx="${X(x)}" cy="${Y(y)}" r="${(cell * 0.13).toFixed(1)}"/>`;
      }
    }
    const [nx, ny] = at(now);
    return out + `<circle class="wj-cur" cx="${X(nx)}" cy="${Y(ny)}" r="${(cell * 0.34).toFixed(1)}"/></svg>`;
  };

  // --- the box -------------------------------------------------------------------------------

  // what a step does, in words: two jugs by name, three by capacity
  const words = (m, caps, names) => {
    const nm = (i) => (names ? names[i] : `הכד של ${caps[i]}`);
    if (m[0] === "fill") return `ממלאים את ${nm(m[1])}`;
    if (m[0] === "empty") return `מרוקנים את ${nm(m[1])}`;
    return names ? `מוזגים מ-${names[m[1]]} ל-${names[m[2]]}` : `מוזגים מהכד של ${caps[m[1]]} לכד של ${caps[m[2]]}`;
  };
  const CODE = { fill: "f", empty: "e", pour: "p" };
  const encode = (m) => CODE[m[0]] + m.slice(1).join("");
  const decode = (t) => {
    const r = /^([fep])(\d)(\d)?$/.exec(t);
    if (!r) return null;
    const kind = { f: "fill", e: "empty", p: "pour" }[r[1]];
    return kind === "pour" ? (r[3] === undefined ? null : [kind, Number(r[2]), Number(r[3])]) : (r[3] === undefined ? [kind, Number(r[2])] : null);
  };

  // the shared view: opts.tap (two jugs with sliders) or not (three jugs from the page)
  const jugsView = (three) => () => ({
    mount(box) {
      const clamp = (v, lo, hi, d) => { const x = Math.floor(Number(v)); return Number.isFinite(x) ? Math.min(hi, Math.max(lo, x)) : d; };
      const D = three
        ? { caps: (box.dataset.caps || "8,5,3").split(",").map(Number), goal: (box.dataset.goal || "4,4,0").split(",").map(Number) }
        : { a: clamp(box.dataset.a, 1, 9, 3), b: clamp(box.dataset.b, 1, 12, 5), t: clamp(box.dataset.t, 0, 12, 4) };
      const st = three ? { mine: [], track: "mine", k: 0 } : { a: D.a, b: D.b, t: D.t, mine: [], track: "mine", k: 0 };
      const caps = () => (three ? D.caps : [st.a, st.b]);
      const names = three ? null : ["A", "B"];
      const start = () => (three ? [D.caps[0], 0, 0] : [0, 0]);
      const target = () => (three ? D.goal : st.t);
      let best = null, dist = null;
      const compute = () => {
        best = jugBfs(caps(), start(), target(), !three);
        dist = jugDist(caps(), start(), !three);
      };
      const slider = (cls, label, aria, lo, hi) => `<label><span>${label}</span><input type="range" class="${cls}" min="${lo}" max="${hi}" step="1" dir="ltr" aria-label="${aria}"><output class="${cls}-o"></output></label>`;
      const stepsOf = jugSteps(three ? D.caps : [1, 1], !three);
      const btnName = (m) => (three ? `מ-${D.caps[m[1]]} ל-${D.caps[m[2]]}` : m[0] === "fill" ? `מילוי ${names[m[1]]}` : m[0] === "empty" ? `ריקון ${names[m[1]]}` : `מזיגה מ-${names[m[1]]} ל-${names[m[2]]}`);
      box.innerHTML =
        (three ? "" : `<div class="ex-controls">` + slider("wj-a", RLM + "a", "הקיבולת של כד A בליטרים", 1, 9) + slider("wj-b", RLM + "b", "הקיבולת של כד B בליטרים", 1, 12) +
          slider("wj-t", RLM + "T", "כמה ליטר צריך למדוד, T", 0, 12) + `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>`) +
        `<div class="ex-controls wj-moves" role="group" aria-label="${three ? "המזיגות" : "הצעדים"}">` +
        stepsOf.map((m) => `<button type="button" class="md-button wj-mv" data-m="${encode(m)}">${btnName(m)}</button>`).join("") +
        `<button type="button" class="md-button wj-undo">ביטול</button>` + (three ? `<button type="button" class="md-button ex-reset">חזרה להתחלה</button>` : "") + `</div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button wj-best">הדרך הקצרה</button>` +
        `<button type="button" class="md-button ex-start">התחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">סוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 700, 300) +
        `<span class="ex-pos"></span></div>` +
        `<div class="wj-figs"><div class="wj-jugs"></div><div class="wj-gridwrap"></div></div>` +
        `<span class="viz-legend"><span><i class="wj-key-water"></i>מים</span><span><i class="wj-key-chg"></i>הכד שהצעד שינה</span>` +
        `<span><i class="wj-key-reach"></i>מצב נגיש</span><span><i class="wj-key-goal"></i>${three ? "החלוקה" : "מצב עם T"}</span>` +
        `<span><i class="wj-key-never"></i>לא מגיעים אליו</span><span><i class="wj-key-best"></i>המסלול עד עכשיו</span></span>` +
        `<p class="ex-summary wj-sum" aria-live="polite"></p>` +
        `<p class="wj-note"></p>`;
      const $ = (s) => box.querySelector(s);
      const track = () => (st.track === "best" ? (best || []).map(([m]) => m) : st.mine);
      const statesOf = (moves) => { const out = [start()]; moves.forEach((m) => out.push(jugApply(caps(), out[out.length - 1], m))); return out; };
      const draw = () => {
        const mv = track(), T = mv.length;
        st.k = Math.min(Math.max(st.k, 0), T);
        const k = st.k, states = statesOf(mv.slice(0, k)), s = states[k], m = k ? mv[k - 1] : null;
        if (!three) {
          $(".wj-a").value = String(st.a); $(".wj-b").value = String(st.b); $(".wj-t").value = String(st.t);
          $(".wj-a-o").textContent = st.a; $(".wj-b-o").textContent = st.b; $(".wj-t-o").textContent = st.t;
        }
        const nm = three ? D.caps.map(String) : names;
        const aria = (three ? `שלושת הכדים : ` : `שני הכדים : `) + s.map((v, i) => (three ? `בכד של ${D.caps[i]} ${v}` : `ב-${names[i]} ${v}`)).join(", ");
        $(".wj-jugs").innerHTML = jugsSvg(caps(), s, three ? nm.map((c) => "") : names, m, aria);
        const goal = three ? (y, z) => same([D.caps[0] - y - z, y, z], D.goal) : (x, y) => x === st.t || y === st.t;
        $(".wj-gridwrap").innerHTML = gridSvg(caps(), dist, three ? 1 : 0, three ? 2 : 1, three ? D.caps[0] : null, states, s,
          goal, three ? [`${D.caps[1]}`, `${D.caps[2]}`] : names);
        $(".ex-pos").textContent = `צעד ${k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === T;
        $(".wj-undo").disabled = st.track !== "mine" || !st.mine.length;
        $(".wj-best").disabled = !best;
        box.querySelectorAll(".wj-mv").forEach((b) => { b.disabled = same(jugApply(caps(), s, decode(b.dataset.m)), s); });
        const now = three ? `בכדים של ${D.caps.slice(0, -1).join(", ")} ו-${D.caps[2]}${NB}: ${s.slice(0, -1).join(", ")} ו-${s[2]}`
          : `ב-A יש ${s[0]}, וב-B יש ${s[1]}`;
        const kind = three ? "מזיגה" : "צעד";
        $(".wj-sum").innerHTML = (k ? `${kind} ${ltr(k)}${NB}: ${words(m, caps(), names)}. ` : `התחלה. `) + now + "." +
          (st.track === "best" ? ` <span class="wj-tag">הדרך הקצרה</span>` : "");
        const min = best ? best.length : null;
        let note;
        if (three) note = `הדרך הקצרה ביותר${NB}: ${ltr(min)} מזיגות. ${ltr(Object.keys(dist).length)} מתוך ${ltr((D.caps[1] + 1) * (D.caps[2] + 1))} המצבים נגישים.`;
        else if (best) note = `${RLM}${ltr(st.t)} ליטר ${st.t > Math.min(st.a, st.b) ? "בכד הגדול" : "באחד הכדים"}${NB}: ${min ? `לפחות ${ltr(min)} צעדים` : "כבר שם, בלי צעדים"}. ${ltr(`gcd(${st.a}, ${st.b}) = ${gcd(st.a, st.b)}`)}, ו-${ltr(Object.keys(dist).length)} מתוך ${ltr((st.a + 1) * (st.b + 1))} הזוגות נגישים.`;
        else if (st.t > Math.max(st.a, st.b)) note = `<strong>אי אפשר${NB}:</strong> ${ltr(st.t)} ליטר לא נכנסים לאף כד, הגדול מחזיק ${ltr(Math.max(st.a, st.b))}.`;
        else note = `<strong>אי אפשר${NB}:</strong> ${ltr(`gcd(${st.a}, ${st.b}) = ${gcd(st.a, st.b)}`)}, וכל צעד משאיר בכל כד כפולה של ${ltr(gcd(st.a, st.b))}. ${ltr(st.t)} לא כפולה של ${ltr(gcd(st.a, st.b))}.`;
        $(".wj-note").innerHTML = note;
        const done = three ? same(s, D.goal) : s.includes(st.t);
        if (done && (k || !three) && best) {
          const where = three ? "" : ` בכד ${names[s.indexOf(st.t)]}`;
          const head = three ? `שני חצאים של ${ltr(D.goal[0])} אחרי ${ltr(k)} מזיגות` : `יש ${ltr(st.t)} ליטר${where} אחרי ${ltr(k)} צעדים`;
          answer(box, `${head}. ${k === min ? "זה המינימום." : `המינימום${NB}: ${ltr(min)}.`}`, ".wj-sum");
        } else answer(box, null);
      };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= track().length, restart: () => { st.k = 0; draw(); } });
      const resetPlan = () => { st.mine = []; st.track = "mine"; st.k = 0; };
      box.querySelectorAll(".wj-mv").forEach((b) => b.addEventListener("click", () => {
        stop();
        const cur = track().slice(0, st.k);
        st.mine = cur.concat([decode(b.dataset.m)]); st.track = "mine"; st.k = st.mine.length;
        draw();
      }));
      $(".wj-undo").addEventListener("click", () => { stop(); st.mine = st.mine.slice(0, Math.max(0, st.k - 1)); st.k = st.mine.length; draw(); });
      $(".wj-best").addEventListener("click", () => { stop(); st.track = "best"; st.k = 0; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = track().length; draw(); });
      if (!three) {
        const onSlide = () => {
          stop();
          st.a = clamp($(".wj-a").value, 1, 9, D.a); st.b = clamp($(".wj-b").value, 1, 12, D.b); st.t = clamp($(".wj-t").value, 0, 12, D.t);
          resetPlan(); compute(); draw();
        };
        ["wj-a", "wj-b", "wj-t"].forEach((c) => $(`.${c}`).addEventListener("input", onSlide));
      }
      box.querySelectorAll(".ex-reset").forEach((b) => b.addEventListener("click", () => {
        stop();
        if (!three) Object.assign(st, { a: D.a, b: D.b, t: D.t });
        resetPlan(); compute(); draw();
      }));
      // the steps ride in the link: "m" (by hand) or "b" (the shortest), the step shown, the steps
      box.dvqExtra = {
        get: () => (st.track === "best" ? `b.${st.k}` : st.mine.length ? `m.${st.k}.${st.mine.map(encode).join("-")}` : ""),
        set: (text) => {
          const r = /^(b)\.(\d+)$|^(m)\.(\d+)\.([fep\d-]+)$/.exec(text);
          if (!r) return false;
          if (r[1]) {
            if (!best || Number(r[2]) > best.length) return false;
            st.track = "best"; st.k = Number(r[2]); draw(); return true;
          }
          const moves = r[5].split("-").map(decode);
          const ok = moves.length <= 200 && moves.every((m) => m && m.slice(1).every((i) => i < caps().length) && (m[0] === "pour" ? m[1] !== m[2] : !three));
          if (!ok || Number(r[4]) > moves.length) return false;
          st.track = "mine"; st.mine = moves; st.k = Number(r[4]); draw(); return true;
        },
      };
      compute();
      draw();
    },
  });

  dvqExplorers.register({
    views: { jugs: jugsView(false), jugs3: jugsView(true) },
    help: {
      jugs: "בוחרים את הקיבולות a ו-b ואת הכמות T. הכפתורים ממלאים, מרוקנים ומוזגים, והדף סופר צעדים ומשווה למינימום. \"הדרך הקצרה\" טוענת את התוכנית של BFS, והחיצים עוברים עליה צעד אחרי צעד. ברשת, כל עיגול הוא זוג (x, y) : מלא אם מגיעים אליו, טבעת אם לא, והקו הוא המסלול עד עכשיו.",
      jugs3: "מוזגים בין שלושת הכדים בכפתורים, או טוענים את \"הדרך הקצרה\" ועוברים עליה מזיגה אחרי מזיגה. הרשת מראה את הכד של 5 לרוחב ואת הכד של 3 לגובה, והכד של 8 מחזיק את השאר.",
    },
    models: { jugApply, jugMoves, jugBfs, jugDist, jugCan },
  });
})();
