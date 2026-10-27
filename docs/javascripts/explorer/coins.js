// kinds: coins
//   coins                  0052        a pattern of H and T (and a rival for a race): tosses by hand, at random or played, the matched part of each pattern, the games so far against the exact mean or chance; 1000 games by seed against the exact distribution
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { autoplay, code, f, frame, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Coin patterns (0052): Conway's correlation (the sum of 2^k over the k for which the
  // last k letters of a are the first k of b), the expected wait corr(p, p), the chance
  // that a comes before b, the automaton over H / T (the longest suffix that is a prefix)
  // and the exact distribution of the wait by dynamic programming on it.
  const coinCorr = (a, b) => {
    let v = 0;
    for (let k = 1; k <= Math.min(a.length, b.length); k++) if (a.slice(a.length - k) === b.slice(0, k)) v += Math.pow(2, k);
    return v;
  };
  const coinExpected = (p) => coinCorr(p, p);
  const coinFirst = (a, b) => { const wa = coinCorr(b, b) - coinCorr(b, a), wb = coinCorr(a, a) - coinCorr(a, b); return wa / (wa + wb); };
  const coinStep = (p, s, c) => {
    const seen = p.slice(0, s) + c;
    for (let k = Math.min(seen.length, p.length); k >= 0; k--) if (seen.endsWith(p.slice(0, k))) return k;
    return 0;
  };
  const coinTable = (p) => Array.from({ length: p.length + 1 }, (_, s) => ["H", "T"].map((c) => coinStep(p, s, c)));
  const coinDist = (p, tmax) => {
    const t = coinTable(p), L = p.length, out = [];
    let now = new Map([[0, 1]]);
    for (let i = 0; i < tmax; i++) {
      const nxt = new Map();
      let hit = 0;
      now.forEach((pr, s) => t[s].forEach((n) => { if (n === L) hit += pr / 2; else nxt.set(n, (nxt.get(n) || 0) + pr / 2); }));
      out.push(hit);
      now = nxt;
    }
    return out;
  };

  // The box (0052): pattern A and an optional rival B; tosses by the H and T buttons, a
  // random toss or play; each pattern as a row of letters with the part matched so far
  // lit; a game ends when a pattern appears and the next toss starts a new one; the games
  // so far against the exact mean (or, in a race, the share of wins against the exact
  // chance); "1000 games" by seed, with the histogram of the waits against the exact
  // distribution.
  const SIMS = 1000, TMAX = 30, KEEP = 40;
  const coinsView = () => ({
    mount(box) {
      const A0 = (box.dataset.a || "HH").toUpperCase(), B0 = (box.dataset.b || "").toUpperCase();
      const st = { a: A0, b: B0, tosses: [], games: [], sim: null };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>הרצף שלי</span><input type="text" class="ex-num cn-a" value="${A0}" dir="ltr" maxlength="6" aria-label="הרצף, 1 עד 6 אותיות H או T"></label>` +
        `<label><span>רצף יריב (למירוץ)</span><input type="text" class="ex-num cn-b" value="${B0}" dir="ltr" maxlength="6" aria-label="רצף היריב, ריק בלי מירוץ"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err cn-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<span class="cn-hand"><span class="ex-title">ההטלה הבאה :</span> ` +
        `<button type="button" class="md-button md-button--primary cn-toss" data-c="H">H</button> ` +
        `<button type="button" class="md-button md-button--primary cn-toss" data-c="T">T</button></span>` +
        `<button type="button" class="md-button ex-next">הטלה אקראית</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(700, 300, 80) +
        `<button type="button" class="md-button ex-start">ניקוי</button></div>` +
        `<div class="ex-controls cn-simrow"><button type="button" class="md-button md-button--primary cn-sim">${SIMS} משחקים</button><span class="cn-anchor"></span></div>` +
        `<p class="ex-summary cn-sum" aria-live="polite"></p>` +
        `<div class="cn-pats"></div>` +
        `<p class="cn-games"></p>` +
        `<div class="cn-chart"></div>` +
        `<p class="ex-title">ההטלות של המשחק הנוכחי</p><div class="cn-strip" dir="ltr"></div>`;
      const $ = (sel) => box.querySelector(sel);
      let stop = () => {};
      const race = () => st.b !== "";
      const state = (p) => st.tosses.reduce((s, c) => coinStep(p, s, c), 0);
      const over = () => st.tosses.length > 0 && (state(st.a) === st.a.length || (race() && state(st.b) === st.b.length));
      const patRow = (name, p, s, won) =>
        `<div class="cn-row${won ? " is-won" : ""}"><span class="cn-name">${name}</span><span class="cn-cells" dir="ltr">` +
        [...p].map((c, i) => `<span class="cn-cell${i < s ? " is-match" : ""}">${c}</span>`).join("") + `</span>` +
        `<span class="cn-state">${won ? "✓ הופיע" : s ? `${ltr(s)} מתוך ${ltr(p.length)}` : "עוד כלום"}</span></div>`;
      const chart = () => {
        if (!st.sim) return `<p class="ex-note">‏"${SIMS} משחקים" מריץ אלף משחקים ומשווה לחישוב המדויק.</p>`;
        const { waits, winsA } = st.sim, exact = coinDist(st.a, TMAX), counts = Array(TMAX + 1).fill(0);
        waits.forEach((w) => { counts[Math.min(w, TMAX + 1) - 1] = (counts[Math.min(w, TMAX + 1) - 1] || 0) + 1; });
        const share = counts.slice(0, TMAX).map((c) => c / waits.length);
        const top = Math.ceil(Math.max(0.05, ...share, ...exact) * 1.1 * 20) / 20, ticks = [0, top / 2, top];
        const fr = frame(`ההיסטוגרמה של מספר ההטלות ב-${SIMS} משחקים, מול ההתפלגות המדויקת`, TMAX, ticks[2], ticks, (v) => v.toFixed(2));
        let s = fr.s;
        const bw = (fr.cx(2) - fr.cx(1)) * 0.7;
        share.forEach((v, i) => { if (v > 0) s += `<rect class="bar by-multiples" x="${f(fr.cx(i + 1) - bw / 2)}" y="${f(fr.Y(v))}" width="${f(bw)}" height="${f(fr.Y(0) - fr.Y(v))}"><title>${i + 1}: ${v.toFixed(3)}</title></rect>`; });
        exact.forEach((v, i) => { s += `<circle class="s2-dot" cx="${f(fr.cx(i + 1))}" cy="${f(fr.Y(v))}" r="3.5"><title>${i + 1}: ${v.toFixed(4)}</title></circle>`; });
        [1, 5, 10, 15, 20, 25, 30].forEach((i) => { s += fr.xtick(i, String(i)); });
        const mean = waits.reduce((x, y) => x + y, 0) / waits.length;
        return `<p class="ex-title">${race() ? `ההמתנה בכל משחק עד שאחד הרצפים הופיע` : `מספר ההטלות עד ${code(st.a)} בכל משחק`} : עמודות מהסימולציה, נקודות מהחישוב המדויק${race() ? ` (של ${code(st.a)} לבד)` : ""}</p>` + s + fr.close() +
          `<span class="viz-legend"><span><i class="by-multiples"></i>שכיחות בסימולציה</span><span><i class="cn-key-exact"></i>ההסתברות המדויקת ל-${code(st.a)}</span></span>` +
          `<p class="cn-simsum">${ltr(SIMS)} משחקים : ממוצע ${ltr(mean.toFixed(2))} הטלות` + (race()
            ? `; ${code(st.a)} ניצח ב-${ltr(winsA)} (${ltr(`${(100 * winsA / SIMS).toFixed(1)}%`)}), והחישוב המדויק ${ltr(`${(100 * coinFirst(st.a, st.b)).toFixed(1)}%`)}.`
            : `, והתוחלת המדויקת ${ltr(coinExpected(st.a))}.`) + `</p>`;
      };
      const play1 = (rng) => {
        let sa = 0, sb = 0, n = 0;
        while (n < 100000) {
          const c = rng() < 0.5 ? "H" : "T";
          n++; sa = coinStep(st.a, sa, c);
          if (sa === st.a.length) return [n, 1];
          if (race()) { sb = coinStep(st.b, sb, c); if (sb === st.b.length) return [n, 0]; }
        }
        return [n, 0];
      };
      const draw = () => {
        const sa = state(st.a), sb = race() ? state(st.b) : 0, wonA = sa === st.a.length, wonB = race() && sb === st.b.length;
        $(".cn-pats").innerHTML = patRow("שלי", st.a, sa, wonA) + (race() ? patRow("יריב", st.b, sb, wonB && !wonA) : "");
        const head = race()
          ? `מירוץ ${code(st.a)} מול ${code(st.b)} : הסיכוי ש-${code(st.a)} מופיע קודם הוא ${ltr((coinFirst(st.a, st.b) * 100).toFixed(1) + "%")}, ` +
            `והתוחלות ${ltr(coinExpected(st.a))} ו-${ltr(coinExpected(st.b))} הטלות.`
          : `התוחלת של ${code(st.a)} : ${ltr(coinExpected(st.a))} הטלות, ${ltr([...Array(st.a.length).keys()].map((i) => i + 1).filter((k) => st.a.slice(-k) === st.a.slice(0, k)).map((k) => Math.pow(2, k)).join(" + ") + " = " + coinExpected(st.a))}.`;
        const now = st.tosses.length ? (over() ? ` המשחק הסתיים אחרי ${ltr(st.tosses.length)} הטלות${race() ? (wonA ? ` : ${code(st.a)} ניצח` : ` : ${code(st.b)} ניצח`) : ""}; ההטלה הבאה מתחילה משחק חדש.` : ` במשחק הנוכחי : ${ltr(st.tosses.length)} הטלות.`) : " עוד לא הוטל אף מטבע.";
        $(".cn-sum").innerHTML = head + now;
        const g = st.games, mean = g.length ? g.reduce((x, y) => x + y.n, 0) / g.length : 0, wins = g.filter((x) => x.a).length;
        $(".cn-games").innerHTML = g.length ? `משחקים שהסתיימו : ${ltr(g.length)}, ממוצע ${ltr(mean.toFixed(2))} הטלות` +
          (race() ? `, ${code(st.a)} ניצח ב-${ltr(wins)}.` : ` (התוחלת ${ltr(coinExpected(st.a))}).`) : "עוד לא הסתיים אף משחק.";
        $(".cn-chart").innerHTML = chart();
        const shown = st.tosses.slice(-KEEP), from = st.tosses.length - shown.length;
        $(".cn-strip").innerHTML = shown.length ? shown.map((c, i) => `<span class="cn-chip${over() && i >= shown.length - (wonA ? st.a.length : st.b.length) ? " is-hit" : ""}">${c}</span>`).join("") + (from ? `<span class="cn-more">+${from}</span>` : "")
          : `<span class="ex-note">אין הטלות עדיין.</span>`;
      };
      const toss = (c) => {
        if (over()) st.tosses = [];
        st.tosses.push(c);
        if (over()) st.games.push({ n: st.tosses.length, a: state(st.a) === st.a.length });
        draw();
      };
      const setPats = () => {
        const a = $(".cn-a").value.trim().toUpperCase(), b = $(".cn-b").value.trim().toUpperCase();
        const err = !/^[HT]{1,6}$/.test(a) ? "הרצף : 1 עד 6 אותיות H או T"
          : b && !/^[HT]{1,6}$/.test(b) ? "רצף היריב : ריק, או 1 עד 6 אותיות H או T"
          : b && (a.includes(b) || b.includes(a)) ? "במירוץ, אף רצף לא יכול להכיל את השני" : "";
        $(".cn-err").textContent = err;
        if (err) return;
        stop(); st.a = a; st.b = b; $(".cn-a").value = a; $(".cn-b").value = b; st.tosses = []; st.games = []; st.sim = null; draw();
      };
      [".cn-a", ".cn-b"].forEach((s) => { $(s).addEventListener("change", setPats); $(s).addEventListener("keydown", (e) => { if (e.key === "Enter") $(s).blur(); }); });
      box.querySelectorAll(".cn-toss").forEach((b) => b.addEventListener("click", () => { stop(); toss(b.dataset.c); }));
      $(".ex-next").addEventListener("click", () => { stop(); toss(Math.random() < 0.5 ? "H" : "T"); });
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
      $(".ex-reset").addEventListener("click", () => { $(".cn-a").value = A0; $(".cn-b").value = B0; setPats(); });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => toss(Math.random() < 0.5 ? "H" : "T"), done: () => st.games.length >= 200, restart: () => { st.tosses = []; st.games = []; draw(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { coins: coinsView },
    help: {
      coins: "מקלידים רצף של H ו-T, ואם רוצים רצף יריב למירוץ. הכפתורים H ו-T מטילים ביד, ״הטלה אקראית״ ו״הפעלה״ מגרילים. השורות מראות כמה מכל רצף כבר נבנה; כשרצף מופיע המשחק נגמר וההטלה הבאה מתחילה משחק חדש. ״1000 משחקים״ מריץ אלף משחקים לפי ערך האתחול, ומשווה את ההיסטוגרמה לחישוב המדויק.",
    },
    models: { coinCorr, coinExpected, coinFirst, coinTable, coinDist },
  });
})();
