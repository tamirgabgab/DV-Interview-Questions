// kinds: chameleons
//   chameleons             0086        red, green and blue chameleons (sliders for the three counts): meetings by hand (red and green, red and blue, green and blue, undo), or the shortest plan to the cheapest colour loaded and played meeting by meeting; the counts with their residues mod 3, why no single colour is possible when the residues differ, and the triangle of every state with the same sum: the reachable ones, the corners where all share a colour, the path so far
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the script
// tag); under Node tools/explorer_node.js loads every kind file and merges the models for the
// question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const RLM = "‏";
  const NAMES = ["אדומות", "ירוקות", "כחולות"];
  const ONE = ["אדומה", "ירוקה", "כחולה"];
  const PAIRS = [[0, 1], [0, 2], [1, 2]];

  // --- the model (tests/0086 compares it with the page's code and the generator) ------------

  // a chameleon of colour i meets one of colour j: both turn to the third colour
  const chMeet = (s, i, j) => { const t = s.slice(); t[i]--; t[j]--; t[3 - i - j] += 2; return t; };
  // the fewest meetings to every reachable state: { "r,g,b": d }
  const chDist = (start) => {
    const dist = { [start.join(",")]: 0 }, queue = [start];
    for (let h = 0; h < queue.length; h++) {
      const s = queue[h];
      for (const [i, j] of PAIRS) {
        if (!s[i] || !s[j]) continue;
        const t = chMeet(s, i, j), k = t.join(",");
        if (!(k in dist)) { dist[k] = dist[s.join(",")] + 1; queue.push(t); }
      }
    }
    return dist;
  };
  const mod3 = (v) => ((v % 3) + 3) % 3;
  // the closed form of the page: the fewest meetings until all are of colour c, or null
  const chTo = (s, c) => {
    const [x, y] = [0, 1, 2].filter((k) => k !== c).map((k) => s[k]);
    if (mod3(x - y)) return null;
    if (s[c] === 0 && Math.min(x, y) === 0 && Math.max(x, y) > 0) return null;
    return Math.max(x, y);
  };
  // [meetings, colour] for the cheapest colour (the first on a tie), or null
  const chMin = (s) => {
    let best = null;
    for (let c = 0; c < 3; c++) { const m = chTo(s, c); if (m !== null && (best === null || m < best[0])) best = [m, c]; }
    return best;
  };
  // the construction of part b: [[i, j], ...] with i < j
  const chPlan = (counts, c) => {
    const s = counts.slice(), plan = [];
    let [a, b] = [0, 1, 2].filter((k) => k !== c);
    if (s[a] < s[b]) [a, b] = [b, a];
    const go = (i, j) => { s[i]--; s[j]--; s[3 - i - j] += 2; plan.push([Math.min(i, j), Math.max(i, j)]); };
    while (s[b] > 0) go(a, b);
    while (s[a] > 0) { go(a, c); go(a, b); go(a, b); }
    return plan;
  };

  // --- the triangle --------------------------------------------------------------------------

  const SIDE = 280, LEFT = 30, TOP = 30, HT = (SIDE * Math.sqrt(3)) / 2;
  const TW = SIDE + 2 * LEFT, TH = Math.round(TOP + HT + 34);
  const corner = [[LEFT + SIDE / 2, TOP], [LEFT, TOP + HT], [LEFT + SIDE, TOP + HT]];
  const at = (s, n) => [0, 1].map((d) => (s[0] * corner[0][d] + s[1] * corner[1][d] + s[2] * corner[2][d]) / n);
  const triSvg = (n, dist, path, start, goalC) => {
    let out = `<svg class="figure ch-tri ch-live" viewBox="0 0 ${TW} ${TH}" role="img" aria-label="כל המצבים של ${n} זיקיות כנקודות במשולש : למעלה כולן אדומות, למטה משמאל כולן ירוקות, למטה מימין כולן כחולות. ${Object.keys(dist).length} מצבים נגישים, והדרך עד עכשיו">`;
    out += `<polygon class="ch-edge" points="${corner.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(" ")}"/>`;
    if (!n) return out + `</svg>`;
    const step = SIDE / n, rr = Math.min(4.2, step * 0.36).toFixed(2), rn = Math.min(2.6, step * 0.12).toFixed(2);
    if (path.length > 1) out += `<polyline class="ch-route" points="${path.map((s) => at(s, n).map((v) => v.toFixed(1)).join(",")).join(" ")}"/>`;
    for (let r = 0; r <= n; r++) {
      for (let g = 0; g + r <= n; g++) {
        const s = [r, g, n - r - g], [x, y] = at(s, n);
        out += s.join(",") in dist ? `<circle class="ch-reach" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${rr}"/>`
          : `<circle class="ch-never" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${rn}"/>`;
      }
    }
    corner.forEach(([x, y], c) => {
      const mono = [0, 1, 2].map((k) => (k === c ? n : 0)).join(",");
      const dy = c === 0 ? -14 : 18;
      out += `<circle class="ch-mono ch-c${c}" cx="${x.toFixed(1)}" cy="${(y + dy).toFixed(1)}" r="${mono in dist ? 8 : 5}"${c === goalC ? ' stroke-width="3"' : ""}/>`;
    });
    const [sx, sy] = at(start, n), now = path[path.length - 1], [cx, cy] = at(now, n);
    out += `<circle class="ch-start" cx="${sx.toFixed(1)}" cy="${sy.toFixed(1)}" r="8"/>`;
    return out + `<circle class="ch-cur" cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="6"/></svg>`;
  };

  // --- the box -------------------------------------------------------------------------------

  const encode = (p) => `${p[0]}${p[1]}`;
  const decode = (t) => { const r = /^([01])([12])$/.exec(t); return r && r[1] < r[2] ? [Number(r[1]), Number(r[2])] : null; };
  const counted = (s) => `${s[0]} ${NAMES[0]}, ${s[1]} ${NAMES[1]} ו-${s[2]} ${NAMES[2]}`;

  const view = () => ({
    mount(box) {
      const clamp = (v, d) => { const x = Math.floor(Number(v)); return Number.isFinite(x) ? Math.min(20, Math.max(0, x)) : d; };
      const D = { r: clamp(box.dataset.r, 13), g: clamp(box.dataset.g, 16), b: clamp(box.dataset.b, 17) };
      const st = { s0: [D.r, D.g, D.b], mine: [], track: "mine", k: 0 };
      let best = null, plan = [], dist = {};
      const compute = () => {
        best = chMin(st.s0);
        plan = best ? chPlan(st.s0, best[1]) : [];
        dist = st.s0.some((v) => v) ? chDist(st.s0) : {};
      };
      const slider = (cls, c) => `<label><span>${NAMES[c]}</span><input type="range" class="${cls}" min="0" max="20" step="1" dir="ltr" aria-label="כמה זיקיות ${NAMES[c]} בהתחלה"><output class="${cls}-o"></output></label>`;
      box.innerHTML =
        `<div class="ex-controls">` + slider("ch-r", 0) + slider("ch-g", 1) + slider("ch-b", 2) +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ch-moves" role="group" aria-label="הפגישות">` +
        PAIRS.map((p) => `<button type="button" class="md-button ch-mv" data-m="${encode(p)}">${ONE[p[0]]} ו${ONE[p[1]]}</button>`).join("") +
        `<button type="button" class="md-button ch-undo">ביטול</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ch-best">הדרך הקצרה</button>` +
        `<button type="button" class="md-button ex-start">התחלה</button>` +
        `<button type="button" class="md-button ex-prev">הפגישה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הפגישה הבאה</button>` +
        `<button type="button" class="md-button ex-end">סוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(900, 450, 150) +
        `<span class="ex-pos"></span></div>` +
        `<div class="ch-counts" data-steady></div>` +
        `<div class="ch-trimap"></div>` +
        `<span class="viz-legend"><span><i class="ch-key-reach"></i>מצב שמגיעים אליו</span><span><i class="ch-key-never"></i>מצב שלא מגיעים אליו</span>` +
        `<span><i class="ch-key-start"></i>ההתחלה</span><span><i class="ch-key-cur"></i>עכשיו</span><span><i class="ch-key-route"></i>הדרך עד עכשיו</span>` +
        `<span><i class="ch-key ch-c0"></i><i class="ch-key ch-c1"></i><i class="ch-key ch-c2"></i>פינה : כולן בצבע שלה, עיגול גדול אם מגיעים אליה</span></span>` +
        `<p class="ex-summary ch-sum" aria-live="polite"></p>` +
        `<p class="ch-note"></p>`;
      const $ = (q) => box.querySelector(q);
      const track = () => (st.track === "best" ? plan : st.mine);
      const statesOf = (moves) => { const out = [st.s0]; moves.forEach((p) => out.push(chMeet(out[out.length - 1], p[0], p[1]))); return out; };
      const draw = () => {
        const mv = track(), T = mv.length;
        st.k = Math.min(Math.max(st.k, 0), T);
        const k = st.k, states = statesOf(mv.slice(0, k)), s = states[k], p = k ? mv[k - 1] : null, n = s[0] + s[1] + s[2];
        ["ch-r", "ch-g", "ch-b"].forEach((c, i) => { $(`.${c}`).value = String(st.s0[i]); $(`.${c}-o`).textContent = st.s0[i]; });
        $(".ch-counts").innerHTML = s.map((v, c) => `<span class="ch-count ch-c${c}">` +
          `<span>${NAMES[c]}</span><b>${v}</b><span class="ch-mod">שארית ${mod3(v)}</span></span>`).join("");
        $(".ch-trimap").innerHTML = triSvg(n, dist, states, st.s0, best ? best[1] : -1);
        $(".ex-pos").textContent = `פגישה ${k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === T;
        $(".ch-undo").disabled = st.track !== "mine" || !st.mine.length;
        $(".ch-best").disabled = !best || !plan.length;
        box.querySelectorAll(".ch-mv").forEach((b) => { const q = decode(b.dataset.m); b.disabled = !(s[q[0]] && s[q[1]]); });
        $(".ch-sum").innerHTML = (k ? `פגישה ${ltr(k)}${NB}: ${ONE[p[0]]} ו${ONE[p[1]]} נפגשות, ושתיהן הופכות ל${ONE[3 - p[0] - p[1]]}. ` : "התחלה. ") +
          `עכשיו ${counted(s)}.` + (st.track === "best" ? ` <span class="ch-tag">הדרך הקצרה</span>` : "");
        const r0 = st.s0.map(mod3), same = PAIRS.filter(([i, j]) => r0[i] === r0[j]);
        let note;
        if (!n) note = "אין זיקיות. הזיזו אחד המחוונים.";
        else if (best && best[0] === 0) note = `כולן כבר ${NAMES[best[1]]}, בלי אף פגישה.`;
        else if (best) {
          const [i, j] = same.find(([a, b]) => 3 - a - b === best[1]) || same[0];
          note = `${RLM}${NAMES[i]} ו${NAMES[j]} שוות מודולו 3 (שארית ${r0[i]}), ולכן כולן יכולות להיות ${NAMES[best[1]]}, אחרי ${ltr(best[0])} פגישות לכל הפחות.` +
            (same.length === 3 ? ` כל השאריות שוות, אז גם שני הצבעים האחרים אפשריים, אבל ${NAMES[best[1]]} הכי זול.` : "") +
            ` ${ltr(Object.keys(dist).length)} מתוך ${ltr(((n + 1) * (n + 2)) / 2)} המצבים נגישים.`;
        }
        else note = `<strong>אי אפשר${NB}:</strong> השאריות מודולו 3 בהתחלה הן ${NAMES[0]} ${r0[0]}, ${NAMES[1]} ${r0[1]} ו${NAMES[2]} ${r0[2]}, שלוש שונות. כל פגישה מוסיפה 2 לכל אחת מהן, והן נשארות שונות, אבל כשכולן באותו צבע, שתי ספירות הן 0 ושוות.`;
        $(".ch-note").innerHTML = note;
        const done = n && s.filter((v) => v).length === 1 && k > 0;
        if (done) {
          const c = s.findIndex((v) => v), min = chTo(st.s0, c);
          answer(box, `כולן ${NAMES[c]} אחרי ${ltr(k)} פגישות. ${k === min ? "זה המינימום." : `המינימום${NB}: ${ltr(min)}.`}`, ".ch-sum");
        } else answer(box, null);
      };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= track().length, restart: () => { st.k = 0; draw(); } });
      const resetPlan = () => { st.mine = []; st.track = "mine"; st.k = 0; };
      box.querySelectorAll(".ch-mv").forEach((b) => b.addEventListener("click", () => {
        stop();
        const cur = track().slice(0, st.k);
        st.mine = cur.concat([decode(b.dataset.m)]); st.track = "mine"; st.k = st.mine.length;
        draw();
      }));
      $(".ch-undo").addEventListener("click", () => { stop(); st.mine = st.mine.slice(0, Math.max(0, st.k - 1)); st.k = st.mine.length; draw(); });
      $(".ch-best").addEventListener("click", () => { stop(); st.track = "best"; st.k = 0; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = track().length; draw(); });
      const onSlide = () => {
        stop();
        st.s0 = ["ch-r", "ch-g", "ch-b"].map((c, i) => clamp($(`.${c}`).value, st.s0[i]));
        resetPlan(); compute(); draw();
      };
      ["ch-r", "ch-g", "ch-b"].forEach((c) => $(`.${c}`).addEventListener("input", onSlide));
      $(".ex-reset").addEventListener("click", () => { stop(); st.s0 = [D.r, D.g, D.b]; resetPlan(); compute(); draw(); });
      // the meetings ride in the link: "m" (by hand) or "b" (the shortest), the meeting shown, the meetings
      box.dvqExtra = {
        get: () => (st.track === "best" ? `b.${st.k}` : st.mine.length ? `m.${st.k}.${st.mine.map(encode).join("-")}` : ""),
        set: (text) => {
          const r = /^(b)\.(\d+)$|^(m)\.(\d+)\.([012-]+)$/.exec(text);
          if (!r) return false;
          if (r[1]) {
            if (Number(r[2]) > plan.length) return false;
            st.track = "best"; st.k = Number(r[2]); draw(); return true;
          }
          const moves = r[5].split("-").map(decode);
          if (moves.length > 400 || !moves.every(Boolean) || Number(r[4]) > moves.length) return false;
          let s = st.s0;
          for (const q of moves) { if (!s[q[0]] || !s[q[1]]) return false; s = chMeet(s, q[0], q[1]); }
          st.track = "mine"; st.mine = moves; st.k = Number(r[4]); draw(); return true;
        },
      };
      compute();
      draw();
    },
  });

  dvqExplorers.register({
    views: { chameleons: view },
    help: {
      chameleons: "בוחרים כמה זיקיות מכל צבע, ומפגישים זוגות בכפתורים : שתי הזיקיות שנפגשו עוברות לצבע השלישי. מתחת לכל ספירה מוצגת השארית שלה מודולו 3, וכל פגישה מוסיפה 2 לכל השאריות. \"הדרך הקצרה\" טוענת את הבנייה לצבע הזול ביותר, והחיצים עוברים עליה פגישה אחרי פגישה. במשולש כל נקודה היא מצב : נקודה מלאה אם מגיעים אליו, עיגול ריק אם לא, והקו הוא הדרך עד עכשיו.",
    },
    models: { chMeet, chDist, chTo, chMin, chPlan },
  });
})();
