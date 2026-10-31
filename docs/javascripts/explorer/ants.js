// kinds: ants
//   ants                   0057        ants on a pole of 100 cm: placed by a click (a click on an ant turns it, a second click removes it) or drawn from a seed; played half a second a step on the pole and on a space-time chart; a toggle between ants that turn and ghosts that walk through; the collisions so far and when each ant falls
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, code, f, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Ants on a pole (0057), the ants at distinct integer positions (ascending), dirs +1 / -1,
  // speed 1. The ghosts walk straight: ghost i is at p + d t until it is off (t >= p going
  // left, t >= len - p going right). The ants keep their order, so at time t the fl
  // leftmost ants have fallen left, the fr rightmost fallen right, and the k-th ant between
  // rides the k-th ghost still on the pole (at a meeting the ghost going left first). Time
  // is counted in half seconds (t2), when every meeting happens.
  const antsGhost = (p, d, len, t) => ({ x: p + d * t, gone: d < 0 ? (t >= p ? "L" : null) : t >= len - p ? "R" : null });
  const antsAt = (pos, dirs, len, t2) => {
    const t = t2 / 2, n = pos.length, gs = pos.map((p, i) => ({ i, d: dirs[i], ...antsGhost(p, dirs[i], len, t) }));
    const fl = gs.filter((g) => g.gone === "L").length, fr = gs.filter((g) => g.gone === "R").length;
    const on = gs.filter((g) => !g.gone).sort((a, b) => a.x - b.x || a.d - b.d);
    return Array.from({ length: n }, (_, k) => (k < fl ? { x: null, dir: -1, gone: "L", ghost: null }
      : k >= n - fr ? { x: null, dir: 1, gone: "R", ghost: null }
      : { x: on[k - fl].x, dir: on[k - fl].d, gone: null, ghost: on[k - fl].i }));
  };
  // when each ant (in order) falls and from which side: the leftmost ones as many as go left
  const antsFall = (pos, dirs, len) => {
    const left = pos.filter((_, i) => dirs[i] < 0).sort((a, b) => a - b);
    const right = pos.filter((_, i) => dirs[i] > 0).map((p) => len - p).sort((a, b) => b - a);
    return [...left.map((t) => [t, "L"]), ...right.map((t) => [t, "R"])];
  };
  const antsEnd = (pos, dirs, len) => Math.max(0, ...pos.map((p, i) => (dirs[i] < 0 ? p : len - p)));
  // the collisions by half second t2: a pair going toward each other meets after (b - a) / 2
  const antsHits = (pos, dirs, t2) => {
    let c = 0;
    pos.forEach((a, i) => pos.forEach((b, j) => { if (dirs[i] > 0 && dirs[j] < 0 && a < b && b - a <= t2) c++; }));
    return c;
  };

  const LEN = 100, NMAX = 12, X0 = 22, SX = 3.56, COLORS = 6;
  const parseCfg = (text) => {
    const m = String(text).split(".").map((s) => /^(\d{1,3})([RL])$/.exec(s));
    if (!m.length || m.some((x) => !x) || m.length > NMAX) return null;
    const ants = m.map((x) => [Number(x[1]), x[2] === "R" ? 1 : -1]).sort((a, b) => a[0] - b[0]);
    if (ants.some(([p], i) => p > LEN || (i && p === ants[i - 1][0]))) return null;
    return ants;
  };

  // The box (0057): the pole at the current half second, the space-time chart drawn up to
  // it, the collisions so far and the fall of every ant; ants or ghosts.
  const antsView = () => ({
    mount(box) {
      const ds = (box.dataset.dirs || "RLRLLR").split("");
      const d0 = (box.dataset.pos || "10,25,40,60,75,90").split(",").map((p, i) => [Number(p), ds[i] === "L" ? -1 : 1]);
      const st = { ants: d0.map((a) => [...a]), t2: 0, ghosts: false, n: 6 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><input type="checkbox" class="an-ghost"> רוחות : עוברות זו דרך זו במקום להסתובב</label>` +
        `<label>נמלים בהגרלה <select class="an-n" aria-label="כמה נמלים להגריל">${[2, 3, 4, 5, 6, 8, 10, 12].map((v) => `<option value="${v}"${v === 6 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button an-rand">הגרלה</button><span class="an-anchor"></span>` +
        `<button type="button" class="md-button an-clear">ניקוי המוט</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err an-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">חצי שנייה אחורה</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">חצי שנייה קדימה</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(400, 160, 60) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary an-sum" aria-live="polite"></p>` +
        `<div class="an-pole-wrap" data-fig-strip></div>` +
        `<p class="ex-note an-hint">לחיצה על המוט מוסיפה נמלה (פונה ימינה), לחיצה על נמלה הופכת אותה, ולחיצה שנייה מוחקת אותה. העריכה היא של מצב ההתחלה.</p>` +
        `<div class="an-st-wrap"></div>` +
        `<span class="viz-legend"><span><i class="an-key-path"></i>הקו של כל נמלה עד עכשיו : מקום מול זמן</span><span><i class="an-key-now"></i>הרגע הנוכחי</span></span>` +
        `<div class="an-falls" data-steady></div>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const pos = () => st.ants.map((a) => a[0]), dirs = () => st.ants.map((a) => a[1]);
      const T2 = () => 2 * antsEnd(pos(), dirs(), LEN);
      const X = (p) => X0 + p * SX;

      const poleSvg = (frame) => {
        const W = 400, H = 92, Y = 50;
        let s = `<svg class="figure an-live an-pole-svg" viewBox="0 0 ${W} ${H}" role="group" aria-label="המוט אחרי ${st.t2 / 2} שניות : ${frame.filter((a) => !a.gone).length} נמלים עליו">` +
          `<rect class="an-hit" x="${X0 - 8}" y="${Y - 26}" width="${LEN * SX + 16}" height="44"/>` +
          `<line class="an-pole" x1="${X0}" y1="${Y}" x2="${X(LEN)}" y2="${Y}"/>`;
        for (const v of [0, 25, 50, 75, 100]) s += `<text class="tick" x="${f(X(v))}" y="${Y + 30}" text-anchor="middle">${v}</text>`;
        frame.forEach((a, k) => {
          if (a.gone) return;
          const id = st.ghosts ? a.ghost : k, x = X(a.x), dx = a.dir * 16;
          s += `<g class="an-ant an-c${id % COLORS}" data-k="${k}" tabindex="0" role="button" aria-label="נמלה ${k + 1} במקום ${a.x}, ${a.dir > 0 ? "ימינה" : "שמאלה"}">` +
            `<title>${st.ghosts ? `ghost ${id + 1}` : `ant ${k + 1}`} at ${a.x} cm, going ${a.dir > 0 ? "right" : "left"}</title>` +
            `<path class="an-dir" d="M${f(x + dx)},${Y - 16} L${f(x + dx * 0.4)},${Y - 22} L${f(x + dx * 0.4)},${Y - 10} Z"/>` +
            `<circle cx="${f(x)}" cy="${Y - 16}" r="10"/><text x="${f(x)}" y="${Y - 11.5}" text-anchor="middle">${id + 1}</text></g>`;
        });
        return s + "</svg>";
      };
      const stSvg = (frames) => {
        const W = 400, top = 18, SY = 3.4, H = top + LEN * SY + 24, t = st.t2 / 2, end = T2();
        let s = `<svg class="figure an-live an-st" viewBox="0 0 ${W} ${f(H)}" role="img" aria-label="מקום מול זמן : ${st.ghosts ? "קווים ישרים של רוחות" : "הקווים השבורים של הנמלים"}">`;
        for (const v of [25, 50, 75, 100]) s += `<line class="an-grid" x1="${X0}" y1="${f(top + v * SY)}" x2="${f(X(LEN))}" y2="${f(top + v * SY)}"/><text class="tick" x="${X0 - 3}" y="${f(top + v * SY + 4)}" text-anchor="end">${v}</text>`;
        s += `<line class="an-pole" x1="${X0}" y1="${top}" x2="${f(X(LEN))}" y2="${top}"/>`;
        if (st.ghosts) {
          st.ants.forEach(([p, d], i) => {
            const g = antsGhost(p, d, LEN, t), stop = Math.min(t, d < 0 ? p : LEN - p), x1 = p + d * stop;
            if (stop > 0) s += `<line class="an-path an-c${i % COLORS}" x1="${f(X(p))}" y1="${top}" x2="${f(X(x1))}" y2="${f(top + stop * SY)}"/>`;
            if (!g.gone) s += `<circle class="an-start an-c${i % COLORS}" cx="${f(X(x1))}" cy="${f(top + stop * SY)}" r="3.5"/>`;
          });
        } else {
          st.ants.forEach((_, k) => {
            const pts = [];
            for (let u = 0; u <= st.t2 && u < frames.length; u++) {
              const a = frames[u][k];
              if (a.gone) { pts.push([a.gone === "L" ? 0 : LEN, u / 2]); break; }
              pts.push([a.x, u / 2]);
            }
            if (pts.length > 1) s += `<polyline class="an-path an-c${k % COLORS}" points="${pts.map(([x, u]) => `${f(X(x))},${f(top + u * SY)}`).join(" ")}"/>`;
            const a = frames[Math.min(st.t2, frames.length - 1)][k];
            if (!a.gone) s += `<circle class="an-start an-c${k % COLORS}" cx="${f(X(a.x))}" cy="${f(top + t * SY)}" r="3.5"/>`;
          });
        }
        s += `<line class="an-now" x1="${X0}" y1="${f(top + t * SY)}" x2="${f(X(LEN))}" y2="${f(top + t * SY)}"/>`;
        if (end) s += `<text class="legend" x="${W - 6}" y="${f(H - 6)}" text-anchor="end">t = ${t} s of ${end / 2} s</text>`;
        return s + "</svg>";
      };

      let frames = [];
      const draw = () => {
        const P = pos(), D = dirs(), n = P.length, end = T2();
        st.t2 = Math.min(st.t2, end);
        frames = Array.from({ length: end + 1 }, (_, u) => antsAt(P, D, LEN, u));
        const frame = n ? frames[st.t2] : [];
        $(".an-ghost").checked = st.ghosts;
        $(".ex-pos").textContent = `צעד ${st.t2} מתוך ${end}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.t2 === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.t2 === end;
        $(".an-pole-wrap").innerHTML = poleSvg(frame);
        $(".an-st-wrap").innerHTML = stSvg(frames);
        const hits = antsHits(P, D, st.t2), all = antsHits(P, D, Infinity);
        const fl = frame.filter((a) => a.gone === "L").length, fr = frame.filter((a) => a.gone === "R").length;
        $(".an-sum").innerHTML = !n ? "אין נמלים על המוט : לחצו על המוט כדי להוסיף." :
          `${ltr(n)} ${n === 1 ? "נמלה" : "נמלים"}, אחרי ${ltr(st.t2 / 2)} שניות : ${ltr(hits)} מתוך ${ltr(all)} התנגשויות, ` +
          `${ltr(fl)} נפלו משמאל ו-${ltr(fr)} מימין. ${st.ghosts ? "הרוחות עוברות זו דרך זו, וכל רוח בצבע שלה." : "כל נמלה בצבע שלה, והיא מסתובבת בכל מפגש."}`;
        const fall = antsFall(P, D, LEN);
        $(".an-falls").innerHTML = !n ? "" : `<p class="ex-title">מתי נופלת כל נמלה (משמאל לימין) :</p><div class="an-chips">` +
          fall.map(([tt, side], k) => `<span class="an-chip an-c${k % COLORS}${tt <= st.t2 / 2 ? " is-gone" : ""}"><b>${k + 1}</b> : ${side === "L" ? "משמאל" : "מימין"} ב-${ltr(tt)}</span>`).join("") + `</div>`;
        if (n && st.t2 === end) {
          const k = fall.reduce((b, [tt], i) => (tt >= fall[b][0] ? i : b), 0);
          answer(box, `המוט ריק אחרי ${ltr(end / 2)} שניות. האחרונה היא נמלה ${ltr(k + 1)} (התחילה ב-${ltr(P[k])}), והיא נופלת ${fall[k][1] === "L" ? "משמאל" : "מימין"}. היו ${ltr(all)} התנגשויות.`,
            box.querySelectorAll(`.an-chip:nth-child(${k + 1})`));
        } else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.t2 = Math.min(T2(), st.t2 + 1); draw(); }, done: () => st.t2 >= T2(), restart: () => { st.t2 = 0; draw(); } });
      const edit = (fn) => { stop(); if (st.t2 > 0) { st.t2 = 0; draw(); return; } $(".an-err").textContent = ""; fn(); st.ants.sort((a, b) => a[0] - b[0]); draw(); };
      const turn = (k) => edit(() => { const a = st.ants[k]; if (!a) return; if (a[1] > 0) a[1] = -1; else st.ants.splice(k, 1); });
      $(".an-pole-wrap").addEventListener("click", (e) => {
        const ant = e.target.closest(".an-ant");
        if (ant) { turn(Number(ant.dataset.k)); return; }
        const svg = $(".an-pole-svg");
        if (!svg || !e.target.closest(".an-hit, .an-pole")) return;
        const p0 = svg.createSVGPoint(); p0.x = e.clientX; p0.y = e.clientY;
        const q = p0.matrixTransform(svg.getScreenCTM().inverse());
        const p = Math.max(0, Math.min(LEN, Math.round((q.x - X0) / SX)));
        edit(() => {
          if (st.ants.some((a) => a[0] === p)) return;
          if (st.ants.length >= NMAX) { $(".an-err").textContent = `לכל היותר ${NMAX} נמלים`; return; }
          st.ants.push([p, 1]);
        });
      });
      $(".an-pole-wrap").addEventListener("keydown", (e) => {
        const ant = e.target.closest(".an-ant");
        if (ant && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); e.stopPropagation(); turn(Number(ant.dataset.k)); }
      });
      $(".an-ghost").addEventListener("change", () => { st.ghosts = $(".an-ghost").checked; draw(); });
      $(".an-n").addEventListener("change", () => { st.n = Number($(".an-n").value); });
      const seed = seedControls(box, $(".an-anchor"), (rng) => {
        stop();
        const spots = Array.from({ length: LEN - 1 }, (_, i) => i + 1);
        for (let i = spots.length - 1; i > 0; i--) { const j = Math.floor(rng() * (i + 1)); [spots[i], spots[j]] = [spots[j], spots[i]]; }
        st.ants = spots.slice(0, st.n).sort((a, b) => a - b).map((p) => [p, rng() < 0.5 ? 1 : -1]);
        st.t2 = 0; draw();
      }, { fresh: false });
      $(".an-rand").addEventListener("click", () => seed.draw());
      $(".an-clear").addEventListener("click", () => { stop(); st.ants = []; st.t2 = 0; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.t2 = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.t2 = Math.max(0, st.t2 - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.t2 = Math.min(T2(), st.t2 + 1); draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.t2 = T2(); draw(); });
      $(".ex-reset").addEventListener("click", () => {
        stop(); Object.assign(st, { ants: d0.map((a) => [...a]), t2: 0, ghosts: false, n: 6 });
        $(".an-n").value = "6"; $(".an-err").textContent = ""; draw();
      });
      // the ants ride in the copy link and the remembered state: "10R.25L..."
      const cfg = () => st.ants.map(([p, d]) => `${p}${d > 0 ? "R" : "L"}`).join(".");
      const CFG0 = cfg();
      box.dvqExtra = {
        get: () => (cfg() === CFG0 ? "" : cfg()),
        set: (text) => { const a = parseCfg(text); if (!a) return false; st.ants = a; st.t2 = 0; draw(); return true; },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { ants: antsView },
    help: {
      ants: "נמלים על מוט של 100 ס״מ, במהירות 1 ס״מ לשנייה. לוחצים על המוט כדי להוסיף נמלה, על נמלה כדי להפוך אותה, ושוב כדי למחוק; או מגרילים. ההפעלה מזיזה את הנמלים בחצאי שניות, ומתחת מצטייר הקו של כל נמלה, מקום מול זמן. המתג ״רוחות״ מראה את אותם מקומות כרוחות שעוברות זו דרך זו : הקווים זהים, רק הצבעים מתחלפים.",
    },
    models: { antsGhost, antsAt, antsFall, antsEnd, antsHits },
  });
})();
