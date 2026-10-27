// kinds: coins
//   coins                  0052        a pattern on a fair coin, a biased coin or a die (and a rival for a race): the state graph of the pattern, tosses by hand, at random or played, the games so far against the exact mean or chance; 1000 games by seed against the exact distribution
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { autoplay, code, f, frame, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Waiting for a pattern (0052), for any letter probabilities: the probabilities of a coin
  // with P(H) = q or of a die; Conway's correlation (1 / P(the first k letters of b) for
  // every k for which the last k letters of a are the first k of b); the expected wait
  // corr(p, p); a race of several patterns by Conway's equations (each pattern's chance
  // and the expected length); the automaton (the longest suffix that is a prefix) and the
  // exact distribution of the wait by dynamic programming on it.
  const coinProbs = (kind, q = 0.5) => (kind === "die" ? Object.fromEntries([1, 2, 3, 4, 5, 6].map((d) => [String(d), 1 / 6])) : { H: q, T: 1 - q });
  const probOf = (w, P) => [...w].reduce((r, c) => r * P[c], 1);
  const coinCorr = (a, b, P) => {
    let v = 0;
    for (let k = 1; k <= Math.min(a.length, b.length); k++) if (a.slice(a.length - k) === b.slice(0, k)) v += 1 / probOf(b.slice(0, k), P);
    return v;
  };
  const coinExpected = (p, P = coinProbs("coin")) => coinCorr(p, p, P);
  const coinRace = (pats, P = coinProbs("coin")) => {
    const m = pats.length, A = [];
    for (let j = 0; j < m; j++) A.push(pats.map((a) => coinCorr(a, pats[j], P)).concat([-1, 0]));
    A.push(Array(m).fill(1).concat([0, 1]));
    for (let c = 0; c <= m; c++) {
      let r = c;
      for (let i = c + 1; i <= m; i++) if (Math.abs(A[i][c]) > Math.abs(A[r][c])) r = i;
      [A[c], A[r]] = [A[r], A[c]];
      for (let i = 0; i <= m; i++) if (i !== c) { const k = A[i][c] / A[c][c]; for (let j = c; j <= m + 1; j++) A[i][j] -= k * A[c][j]; }
    }
    const x = A.map((row, i) => row[m + 1] / row[i]);
    return [x.slice(0, m), x[m]];
  };
  const coinStep = (p, s, c) => {
    const seen = p.slice(0, s) + c;
    for (let k = Math.min(seen.length, p.length); k >= 0; k--) if (seen.endsWith(p.slice(0, k))) return k;
    return 0;
  };
  const coinTable = (p, letters = ["H", "T"]) => Array.from({ length: p.length + 1 }, (_, s) => letters.map((c) => coinStep(p, s, c)));
  const coinDist = (p, tmax, P = coinProbs("coin")) => {
    const letters = Object.keys(P), t = coinTable(p, letters), L = p.length, out = [];
    let now = new Map([[0, 1]]);
    for (let i = 0; i < tmax; i++) {
      const nxt = new Map();
      let hit = 0;
      now.forEach((pr, s) => t[s].forEach((n, j) => { const w = pr * P[letters[j]]; if (n === L) hit += w; else nxt.set(n, (nxt.get(n) || 0) + w); }));
      out.push(hit);
      now = nxt;
    }
    return out;
  };

  // The box (0052): a fair coin, a coin with P(H) = q or a die; pattern A and an optional
  // rival B; the state graph of A (forward arrows, the fall-backs that keep a part of the
  // pattern, the current state and the arrow just taken); tosses by the letter buttons, a
  // random toss or play; each pattern as a row of letters with the part matched lit; a
  // game ends when a pattern appears and the next toss starts a new one; "1000 games" by
  // seed, with the histogram of the waits against the exact distribution.
  const SIMS = 1000, TMAX = 30, KEEP = 40;
  const DEFAULTS = { coin: ["HH", "HT"], die: ["66", "12"] };
  const coinsView = () => ({
    mount(box) {
      const A0 = (box.dataset.a || "HH").toUpperCase(), B0 = (box.dataset.b || "").toUpperCase();
      const st = { kind: "fair", q: 0.5, a: A0, b: B0, tosses: [], games: [], sim: null };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>ההטלה <select class="cn-kind" aria-label="מטבע הוגן, מטבע לא הוגן או קובייה"><option value="fair">מטבע הוגן</option><option value="q">מטבע עם q</option><option value="die">קובייה</option></select></label>` +
        `<label class="cn-qlab" hidden><span>‏P(H) = q</span><input type="range" class="cn-q" min="0.1" max="0.9" step="0.05" value="0.5" dir="ltr" aria-label="ההסתברות ל-H"><output class="out-q">0.50</output></label>` +
        `<label><span>הרצף שלי</span><input type="text" class="ex-num cn-a" value="${A0}" dir="ltr" maxlength="6" aria-label="הרצף, 1 עד 6 אותיות"></label>` +
        `<label><span>רצף יריב (למירוץ)</span><input type="text" class="ex-num cn-b" value="${B0}" dir="ltr" maxlength="6" aria-label="רצף היריב, ריק בלי מירוץ"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err cn-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<span class="cn-hand"></span>` +
        `<button type="button" class="md-button ex-next">הטלה אקראית</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(700, 300, 80) +
        `<button type="button" class="md-button ex-start">ניקוי</button></div>` +
        `<div class="ex-controls cn-simrow"><button type="button" class="md-button md-button--primary cn-sim">${SIMS} משחקים</button><span class="cn-anchor"></span></div>` +
        `<p class="ex-summary cn-sum" aria-live="polite"></p>` +
        `<div class="cn-graph"></div>` +
        `<div class="cn-pats"></div>` +
        `<p class="cn-games"></p>` +
        `<div class="cn-chart"></div>` +
        `<p class="ex-title">ההטלות של המשחק הנוכחי</p><div class="cn-strip" dir="ltr"></div>`;
      const $ = (sel) => box.querySelector(sel);
      let stop = () => {};
      const P = () => (st.kind === "die" ? coinProbs("die") : coinProbs("coin", st.kind === "q" ? st.q : 0.5));
      const letters = () => Object.keys(P());
      const race = () => st.b !== "";
      const state = (p) => st.tosses.reduce((s, c) => coinStep(p, s, c), 0);
      const over = () => st.tosses.length > 0 && (state(st.a) === st.a.length || (race() && state(st.b) === st.b.length));
      const pick = () => { const pr = P(), ls = letters(); let u = Math.random(); for (const c of ls) { u -= pr[c]; if (u < 0) return c; } return ls[ls.length - 1]; };
      const fmt = (v) => (Math.abs(v - Math.round(v)) < 1e-9 ? String(Math.round(v)) : v.toFixed(2));
      let toss = () => {};
      const hand = () => {
        $(".cn-hand").innerHTML = `<span class="ex-title">ההטלה הבאה :</span> ` + letters().map((c) => `<button type="button" class="md-button md-button--primary cn-toss" data-c="${c}">${c}</button>`).join(" ");
        box.querySelectorAll(".cn-toss").forEach((b) => b.addEventListener("click", () => { stop(); toss(b.dataset.c); }));
      };
      // the state graph of A: states 0..L in a row, the arrow forward with its letter, and
      // every fall-back that keeps part of the pattern (the rest go back to the start)
      const graph = () => {
        const p = st.a, L = p.length, ls = letters(), t = coinTable(p, ls), cur = state(st.a);
        const prev = st.tosses.length ? st.tosses.slice(0, -1).reduce((s, c) => coinStep(p, s, c), 0) : null;
        const lastC = st.tosses.length ? st.tosses[st.tosses.length - 1] : null;
        const W = 640, Y = 70, R = 22, H = 150, xs = Array.from({ length: L + 1 }, (_, k) => 46 + (k * (W - 92)) / L);
        let s = `<svg class="figure cn-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="גרף המצבים של ${p} : ${L + 1} מצבים, המצב הנוכחי מודגש">` +
          `<defs><marker id="cn-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>`;
        const labs = [];
        for (let k = 0; k < L; k++) {
          ls.forEach((c, j) => {
            const n = t[k][j], taken = prev === k && lastC === c;
            const cls = `fs-edge${n === L ? " is-found" : ""}${taken ? " is-taken" : ""}`;
            if (n === k + 1) { s += `<line class="${cls}" x1="${f(xs[k] + R)}" y1="${Y}" x2="${f(xs[n] - R - 2)}" y2="${Y}" marker-end="url(#cn-arrow)"/>`; labs.push([(xs[k] + xs[n]) / 2, Y - 7, c, n === L, taken]); }
            else if (n === k && k > 0) { s += `<path class="${cls}" d="M${f(xs[k] - 8)},${Y - R + 3} C${f(xs[k] - 28)},${Y - R - 34} ${f(xs[k] + 28)},${Y - R - 34} ${f(xs[k] + 8)},${Y - R + 2}" marker-end="url(#cn-arrow)"/>`; labs.push([xs[k], Y - R - 24, c, false, taken]); }
            else if (n > 0 && n < k) { const d = 22 + 12 * (k - n); s += `<path class="${cls}" d="M${f(xs[k])},${Y + R} Q${f((xs[k] + xs[n]) / 2)},${Y + R + d} ${f(xs[n])},${Y + R + 2}" marker-end="url(#cn-arrow)"/>`; labs.push([(xs[k] + xs[n]) / 2, Y + R + d / 2 + 12, c, false, taken]); }
            else if (taken && k > 0) s += `<path class="${cls}" d="M${f(xs[k])},${Y + R} Q${f((xs[k] + xs[0]) / 2)},${Y + R + 44} ${f(xs[0])},${Y + R + 2}" marker-end="url(#cn-arrow)"/>`;
          });
        }
        for (let k = 0; k <= L; k++) {
          s += `<g class="fs-node${k === cur ? " is-cur" : ""}${k === L ? " is-out" : ""}"><circle cx="${f(xs[k])}" cy="${Y}" r="${R}"/><text x="${f(xs[k])}" y="${Y + 4}" text-anchor="middle"${k === 0 ? ' style="font-size:10px"' : ""}>${k === 0 ? "start" : p.slice(0, k)}</text></g>`;
        }
        labs.forEach(([x, y, c, found, taken]) => { s += `<text class="fs-label halo${found ? " is-found" : ""}${taken ? " is-taken" : ""}" x="${f(x)}" y="${f(y)}" text-anchor="middle">${c}</text>`; });
        return s + "</svg>" + `<p class="cn-note">חץ לכל הטלה שמשאירה חלק מהרצף; כל הטלה אחרת מחזירה ל-start (החץ שנלקח מודגש).</p>`;
      };
      const patRow = (name, p, s, won) =>
        `<div class="cn-row${won ? " is-won" : ""}"><span class="cn-name">${name}</span><span class="cn-cells" dir="ltr">` +
        [...p].map((c, i) => `<span class="cn-cell${i < s ? " is-match" : ""}">${c}</span>`).join("") + `</span>` +
        `<span class="cn-state">${won ? "✓ הופיע" : s ? `${ltr(s)} מתוך ${ltr(p.length)}` : "עוד כלום"}</span></div>`;
      const chart = () => {
        if (!st.sim) return `<p class="ex-note">‏"${SIMS} משחקים" מריץ אלף משחקים ומשווה לחישוב המדויק.</p>`;
        const { waits, winsA } = st.sim, exact = coinDist(st.a, TMAX, P()), counts = Array(TMAX + 1).fill(0);
        waits.forEach((w) => { counts[Math.min(w, TMAX + 1) - 1]++; });
        const share = counts.slice(0, TMAX).map((c) => c / waits.length);
        const top = Math.ceil(Math.max(0.05, ...share, ...exact) * 1.1 * 20) / 20, ticks = [0, top / 2, top];
        const fr = frame(`ההיסטוגרמה של מספר ההטלות ב-${SIMS} משחקים, מול ההתפלגות המדויקת`, TMAX, ticks[2], ticks, (v) => v.toFixed(2));
        let s = fr.s;
        const bw = (fr.cx(2) - fr.cx(1)) * 0.7;
        share.forEach((v, i) => { if (v > 0) s += `<rect class="bar by-multiples" x="${f(fr.cx(i + 1) - bw / 2)}" y="${f(fr.Y(v))}" width="${f(bw)}" height="${f(fr.Y(0) - fr.Y(v))}"><title>${i + 1}: ${v.toFixed(3)}</title></rect>`; });
        exact.forEach((v, i) => { s += `<circle class="s2-dot" cx="${f(fr.cx(i + 1))}" cy="${f(fr.Y(v))}" r="3.5"><title>${i + 1}: ${v.toFixed(4)}</title></circle>`; });
        [1, 5, 10, 15, 20, 25, 30].forEach((i) => { s += fr.xtick(i, String(i)); });
        const mean = waits.reduce((x, y) => x + y, 0) / waits.length;
        const [wins, len] = race() ? coinRace([st.a, st.b], P()) : [null, null];
        return `<p class="ex-title">${race() ? `ההמתנה בכל משחק עד שאחד הרצפים הופיע` : `מספר ההטלות עד ${code(st.a)} בכל משחק`} : עמודות מהסימולציה, נקודות מהחישוב המדויק${race() ? ` (של ${code(st.a)} לבד)` : ""}</p>` + s + fr.close() +
          `<span class="viz-legend"><span><i class="by-multiples"></i>שכיחות בסימולציה</span><span><i class="cn-key-exact"></i>ההסתברות המדויקת ל-${code(st.a)}</span></span>` +
          `<p class="cn-simsum">${ltr(SIMS)} משחקים : ממוצע ${ltr(mean.toFixed(2))} הטלות` + (race()
            ? ` (המירוץ המדויק : ${ltr(len.toFixed(2))}); ${code(st.a)} ניצח ב-${ltr(winsA)} (${ltr(`${(100 * winsA / SIMS).toFixed(1)}%`)}), והחישוב המדויק ${ltr(`${(100 * wins[0]).toFixed(1)}%`)}.`
            : `, והתוחלת המדויקת ${ltr(fmt(coinExpected(st.a, P())))}.`) + `</p>`;
      };
      const play1 = (rng) => {
        const pr = P(), ls = letters();
        let sa = 0, sb = 0, n = 0;
        while (n < 100000) {
          let u = rng(), c = ls[ls.length - 1];
          for (const x of ls) { u -= pr[x]; if (u < 0) { c = x; break; } }
          n++; sa = coinStep(st.a, sa, c);
          if (sa === st.a.length) return [n, 1];
          if (race()) { sb = coinStep(st.b, sb, c); if (sb === st.b.length) return [n, 0]; }
        }
        return [n, 0];
      };
      const draw = () => {
        const sa = state(st.a), sb = race() ? state(st.b) : 0, wonA = sa === st.a.length, wonB = race() && sb === st.b.length, pr = P();
        $(".out-q").textContent = st.q.toFixed(2);
        $(".cn-qlab").hidden = st.kind !== "q";
        $(".cn-graph").innerHTML = graph();
        $(".cn-pats").innerHTML = patRow("שלי", st.a, sa, wonA) + (race() ? patRow("יריב", st.b, sb, wonB && !wonA) : "");
        const terms = [...Array(st.a.length).keys()].map((i) => i + 1).filter((k) => st.a.slice(-k) === st.a.slice(0, k)).map((k) => fmt(1 / probOf(st.a.slice(0, k), pr)));
        const what = st.kind === "die" ? "קובייה" : st.kind === "q" ? `מטבע עם ${ltr(`q = ${st.q.toFixed(2)}`)}` : "מטבע הוגן";
        let head;
        if (race()) {
          const [wins, len] = coinRace([st.a, st.b], pr);
          head = `${what}, מירוץ ${code(st.a)} מול ${code(st.b)} : הסיכוי ש-${code(st.a)} מופיע קודם ${ltr((wins[0] * 100).toFixed(1) + "%")}, המירוץ נמשך ${ltr(fmt(len))} הטלות בממוצע, ` +
            `והתוחלות לבד ${ltr(fmt(coinExpected(st.a, pr)))} ו-${ltr(fmt(coinExpected(st.b, pr)))}.`;
        } else head = `${what} : התוחלת של ${code(st.a)} היא ${ltr(`${terms.join(" + ")} = ${fmt(coinExpected(st.a, pr))}`)} הטלות.`;
        const now = st.tosses.length ? (over() ? ` המשחק הסתיים אחרי ${ltr(st.tosses.length)} הטלות${race() ? (wonA ? ` : ${code(st.a)} ניצח` : ` : ${code(st.b)} ניצח`) : ""}; ההטלה הבאה מתחילה משחק חדש.` : ` במשחק הנוכחי : ${ltr(st.tosses.length)} הטלות.`) : " עוד לא היתה אף הטלה.";
        $(".cn-sum").innerHTML = head + now;
        const g = st.games, mean = g.length ? g.reduce((x, y) => x + y.n, 0) / g.length : 0, wins = g.filter((x) => x.a).length;
        $(".cn-games").innerHTML = g.length ? `משחקים שהסתיימו : ${ltr(g.length)}, ממוצע ${ltr(mean.toFixed(2))} הטלות` +
          (race() ? `, ${code(st.a)} ניצח ב-${ltr(wins)}.` : ` (התוחלת ${ltr(fmt(coinExpected(st.a, pr)))}).`) : "עוד לא הסתיים אף משחק.";
        $(".cn-chart").innerHTML = chart();
        const shown = st.tosses.slice(-KEEP), from = st.tosses.length - shown.length;
        $(".cn-strip").innerHTML = shown.length ? shown.map((c, i) => `<span class="cn-chip${over() && i >= shown.length - (wonA ? st.a.length : st.b.length) ? " is-hit" : ""}">${c}</span>`).join("") + (from ? `<span class="cn-more">+${from}</span>` : "")
          : `<span class="ex-note">אין הטלות עדיין.</span>`;
      };
      toss = (c) => {
        if (over()) st.tosses = [];
        st.tosses.push(c);
        if (over()) st.games.push({ n: st.tosses.length, a: state(st.a) === st.a.length });
        draw();
      };
      const clean = () => { st.tosses = []; st.games = []; st.sim = null; };
      const setPats = () => {
        const ls = letters().join(""), re = new RegExp(`^[${ls}]{1,6}$`);
        const a = $(".cn-a").value.trim().toUpperCase(), b = $(".cn-b").value.trim().toUpperCase();
        const name = st.kind === "die" ? "הספרות 1 עד 6" : "האותיות H ו-T";
        const err = !re.test(a) ? `הרצף : 1 עד 6 מתוך ${name}`
          : b && !re.test(b) ? `רצף היריב : ריק, או 1 עד 6 מתוך ${name}`
          : b && (a === b || a.includes(b) || b.includes(a)) ? "במירוץ, הרצפים שונים ואף אחד לא בתוך השני" : "";
        $(".cn-err").textContent = err;
        if (err) return;
        stop(); st.a = a; st.b = b; $(".cn-a").value = a; $(".cn-b").value = b; clean(); draw();
      };
      $(".cn-kind").addEventListener("change", () => {
        stop();
        const was = st.kind === "die" ? "die" : "coin";
        st.kind = $(".cn-kind").value;
        const now = st.kind === "die" ? "die" : "coin";
        if (now !== was) { $(".cn-a").value = DEFAULTS[now][0]; $(".cn-b").value = DEFAULTS[now][1]; }
        hand(); clean(); setPats(); draw();
      });
      $(".cn-q").addEventListener("input", () => { st.q = Number($(".cn-q").value); st.sim = null; draw(); });
      [".cn-a", ".cn-b"].forEach((s) => { $(s).addEventListener("change", setPats); $(s).addEventListener("keydown", (e) => { if (e.key === "Enter") $(s).blur(); }); });
      $(".ex-next").addEventListener("click", () => { stop(); toss(pick()); });
      $(".ex-start").addEventListener("click", () => { stop(); st.tosses = []; st.games = []; draw(); });
      const seed = seedControls(box, $(".cn-anchor"), (rng) => {
        stop();
        const waits = [];
        let winsA = 0;
        for (let i = 0; i < SIMS; i++) { const [n, a] = play1(rng); waits.push(n); winsA += a; }
        st.sim = { waits, winsA };
        draw();
      });
      $(".cn-sim").addEventListener("click", () => seed.draw());
      $(".ex-reset").addEventListener("click", () => {
        st.kind = "fair"; st.q = 0.5; $(".cn-kind").value = "fair"; $(".cn-q").value = 0.5;
        $(".cn-a").value = A0; $(".cn-b").value = B0; hand(); setPats();
      });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => toss(pick()), done: () => st.games.length >= 200, restart: () => { st.tosses = []; st.games = []; draw(); } });
      hand();
      draw();
    },
  });

  dvqExplorers.register({
    views: { coins: coinsView },
    help: {
      coins: "בוחרים מטבע הוגן, מטבע עם q או קובייה, ומקלידים רצף, ואם רוצים רצף יריב למירוץ. הכפתורים מטילים ביד, ״הטלה אקראית״ ו״הפעלה״ מגרילים. גרף המצבים מראה כמה מהרצף כבר נבנה ואת החץ שנלקח; כשרצף מופיע המשחק נגמר וההטלה הבאה מתחילה משחק חדש. ״1000 משחקים״ מריץ אלף משחקים לפי ערך האתחול, ומשווה את ההיסטוגרמה לחישוב המדויק.",
    },
    models: { coinProbs, coinCorr, coinExpected, coinRace, coinTable, coinDist },
  });
})();
