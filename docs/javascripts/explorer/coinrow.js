// kinds: coinrow
//   coinrow                0058        coins in a row, each player takes an end: a player per side (me by a click on an end, greedy, the parity trick, optimal), played move by move with the totals; the table of d[i][j] with the interval of the moment and the move it recommends
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, code, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Coins in a row (0058). d[i][j]: the lead of the player to move on coins i..j, both
  // playing their best (null below the diagonal). The strategies pick "L" or "R" on the
  // interval i..j: greedy the larger end (left on a tie); optimal the end with the larger
  // c - d of the rest (left on a tie); parity fixes, on the first even interval it sees, the
  // parity of the places that sum more and takes the end of that parity (on an odd interval
  // the two ends share a parity, and it plays greedy).
  const crDiff = (c) => {
    const n = c.length, d = Array.from({ length: n }, () => Array(n).fill(null));
    for (let i = 0; i < n; i++) d[i][i] = c[i];
    for (let len = 2; len <= n; len++) for (let i = 0; i + len - 1 < n; i++) {
      const j = i + len - 1;
      d[i][j] = Math.max(c[i] - d[i + 1][j], c[j] - d[i][j - 1]);
    }
    return d;
  };
  const STRATS = {
    greedy: (c, i, j) => (c[i] >= c[j] ? "L" : "R"),
    optimal: (c, i, j, st, d) => (i === j || c[i] - d[i + 1][j] >= c[j] - d[i][j - 1] ? "L" : "R"),
    parity: (c, i, j, st) => {
      if ((j - i + 1) % 2) return c[i] >= c[j] ? "L" : "R";
      if (st.want === undefined) {
        let s0 = 0, s1 = 0;
        for (let k = i; k <= j; k++) if (k % 2 === 0) s0 += c[k]; else s1 += c[k];
        st.want = s0 >= s1 ? 0 : 1;
      }
      return i % 2 === st.want ? "L" : "R";
    },
  };
  // run a game: the players' strategies, and the moves a human made ("L" / "R", in order)
  const crRun = (c, players, human = [], stop = Infinity) => {
    const d = crDiff(c), states = [{}, {}], moves = [], tot = [0, 0];
    let i = 0, j = c.length - 1, who = 0, h = 0;
    while (i <= j && moves.length < stop) {
      let side;
      if (players[who] === "me") { if (h >= human.length) break; side = human[h++]; }
      else side = STRATS[players[who]](c, i, j, states[who], d);
      const coin = side === "L" ? c[i] : c[j];
      moves.push([who, side, coin, side === "L" ? i : j]);
      tot[who] += coin;
      if (side === "L") i++; else j--;
      who ^= 1;
    }
    return { moves, tot, i, j, who, d };
  };
  const crPlay = (c, a, b) => { const r = crRun(c, [a, b]); return { moves: r.moves.map(([w, s, coin]) => [w, s, coin]), tot: r.tot }; };

  const NAMES = { me: "אני (בלחיצה)", greedy: "חמדן", parity: "הטריק של הזוגיות", optimal: "אופטימלי" };
  const NMAX = 12;
  const parse = (text) => {
    const v = String(text).split(/[\s,]+/).filter(Boolean).map(Number);
    return v.length >= 1 && v.length <= NMAX && v.every((x) => Number.isInteger(x) && x >= 1 && x <= 99) ? v : null;
  };

  const coinrowView = () => ({
    mount(box) {
      const d0 = { coins: parse(box.dataset.coins || "1,2,5,3") || [1, 2, 5, 3], a: box.dataset.first || "me", b: box.dataset.second || "optimal" };
      const st = { coins: [...d0.coins], players: [d0.a, d0.b], human: [], k: 0, n: 6 };
      const sel = (cls, v, label) => `<label>${label} <select class="${cls}" aria-label="${label}">${Object.entries(NAMES).map(([k, t]) => `<option value="${k}"${k === v ? " selected" : ""}>${t}</option>`).join("")}</select></label>`;
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>המטבעות</span><input type="text" class="ex-num cr-coins" dir="ltr" aria-label="ערכי המטבעות, מופרדים בפסיקים, עד ${NMAX}"></label>` +
        `<label>בהגרלה <select class="cr-n" aria-label="כמה מטבעות להגריל">${[4, 5, 6, 7, 8, 10, 12].map((v) => `<option value="${v}"${v === 6 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button cr-rand">הגרלה</button><span class="cr-anchor"></span>` +
        sel("cr-a", d0.a, "הראשון") + sel("cr-b", d0.b, "השני") +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err cr-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">המהלך הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">המהלך הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 700, 300) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary cr-sum" aria-live="polite"></p>` +
        `<div class="cr-row" role="group" aria-label="השורה : לוקחים מטבע מאחד הקצוות"></div>` +
        `<span class="viz-legend"><span><i class="cr-key-a"></i>של הראשון</span><span><i class="cr-key-b"></i>של השני</span><span><i class="cr-key-end"></i>קצה שאפשר לקחת</span></span>` +
        `<p class="cr-advice"></p>` +
        `<div class="cr-dp" data-steady></div>`;
      const $ = (sel2) => box.querySelector(sel2);
      const play = $(".ex-play"), speed = $(".ex-speed");
      // the whole game as far as it goes: the computer plays on until a human has to move
      const full = () => crRun(st.coins, st.players, st.human);
      const draw = () => {
        const c = st.coins, n = c.length, g = full(), T = g.moves.length;
        st.k = Math.min(st.k, T);
        const cur = crRun(c, st.players, st.human, st.k), done = cur.i > cur.j;
        const waiting = !done && st.k === T && st.players[cur.who] === "me";
        $(".cr-coins").value = c.join(", "); $(".cr-a").value = st.players[0]; $(".cr-b").value = st.players[1];
        $(".ex-pos").textContent = `מהלך ${st.k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === T;
        const owner = new Map(cur.moves.map(([w, , , idx], m) => [idx, [w, m + 1]]));
        $(".cr-row").innerHTML = c.map((v, idx) => {
          const o = owner.get(idx), end = !done && (idx === cur.i || idx === cur.j);
          const cls = o ? ` is-taken cr-by${o[0]}` : end ? " is-end" : "";
          const lab = o ? `<small>${o[0] === 0 ? "א" : "ב"}${o[1]}</small>` : "";
          return `<button type="button" class="cr-coin${cls}" data-idx="${idx}"${waiting && end ? "" : " disabled"} title="place ${idx + 1}">${v}${lab}</button>`;
        }).join("");
        const sum = c.reduce((a, b) => a + b, 0), left = sum - cur.tot[0] - cur.tot[1];
        $(".cr-sum").innerHTML = `${ltr(n)} מטבעות, סכום ${ltr(sum)}. ` +
          `הראשון (${NAMES[st.players[0]]}) : ${ltr(cur.tot[0])}, השני (${NAMES[st.players[1]]}) : ${ltr(cur.tot[1])}` +
          (done ? "." : `, ועוד ${ltr(left)} על השולחן. ${waiting ? "<b>תורך : לחצו על אחד הקצוות.</b>" : `התור של ${cur.who === 0 ? "הראשון" : "השני"}.`}`);
        // the advice of the table on the interval of the moment
        const d = cur.d;
        if (done) $(".cr-advice").innerHTML = "";
        else {
          const i = cur.i, j = cur.j;
          const l = i === j ? c[i] : c[i] - d[i + 1][j], r = i === j ? c[j] : c[j] - d[i][j - 1];
          $(".cr-advice").innerHTML = i === j ? `נשאר מטבע אחד, ${ltr(c[i])}.` :
            `הטבלה : לקחת ${ltr(c[i])} משמאל נותן יתרון ${ltr(`${c[i]} − ${d[i + 1][j]} = ${l}`)}, לקחת ${ltr(c[j])} מימין נותן ${ltr(`${c[j]} − ${d[i][j - 1]} = ${r}`)}. ` +
            `הכי טוב : <b>${l >= r ? "שמאל" : "ימין"}</b>, יתרון ${ltr(Math.max(l, r))} ל${cur.who === 0 ? "ראשון" : "שני"} מכאן והלאה.`;
        }
        // the table d[i][j], the interval of the moment and the two it compares
        const at = done ? null : [cur.i, cur.j];
        let t = `<table class="cr-table"><thead><tr><th>‏i \\ j</th>${c.map((v, j) => `<th>${j + 1}<br><small>${v}</small></th>`).join("")}</tr></thead><tbody>`;
        for (let i = 0; i < n; i++) {
          t += `<tr><th>${i + 1} <small>${c[i]}</small></th>`;
          for (let j = 0; j < n; j++) {
            const v = d[i][j];
            const cls = !at ? "" : i === at[0] && j === at[1] ? "is-now" : (i === at[0] + 1 && j === at[1]) || (i === at[0] && j === at[1] - 1) ? "is-opt" : "";
            t += `<td${cls ? ` class="${cls}"` : ""}>${v === null ? "" : v}</td>`;
          }
          t += "</tr>";
        }
        $(".cr-dp").innerHTML = `<p class="ex-title">‏${code("d[i][j]")} : היתרון של מי שתורו בקטע i..j (מסומן הקטע של הרגע, ובצבע אחר שני הקטעים שהוא בוחר ביניהם)</p>` + t + "</tbody></table>";
        if (done) {
          const best = (sum + d[0][n - 1]) / 2;
          answer(box, `הראשון קיבל ${ltr(cur.tot[0])} והשני ${ltr(cur.tot[1])}. במשחק הטוב ביותר של שניהם הראשון מקבל ${ltr(best)}.`, box.querySelectorAll(".cr-coin"));
        } else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= full().moves.length, restart: () => { st.k = 0; draw(); } });
      const newGame = () => { stop(); st.human = []; st.k = 0; draw(); };
      $(".cr-row").addEventListener("click", (e) => {
        const b = e.target.closest(".cr-coin");
        if (!b || b.disabled) return;
        const cur = crRun(st.coins, st.players, st.human, st.k);
        const idx = Number(b.dataset.idx);
        // a human move: keep the human moves made before this point, add this one
        const before = cur.moves.filter(([w]) => st.players[w] === "me").length;
        st.human = st.human.slice(0, before).concat([idx === cur.i ? "L" : "R"]);
        st.k = full().moves.length;                 // the reply of the computer, if any, comes at once
        draw();
      });
      $(".cr-coins").addEventListener("change", () => {
        const v = parse($(".cr-coins").value);
        $(".cr-err").textContent = v ? "" : `המטבעות : 1 עד ${NMAX} מספרים שלמים מ-1 עד 99`;
        if (v) { st.coins = v; newGame(); }
      });
      $(".cr-coins").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".cr-coins").blur(); });
      $(".cr-a").addEventListener("change", () => { st.players[0] = $(".cr-a").value; newGame(); });
      $(".cr-b").addEventListener("change", () => { st.players[1] = $(".cr-b").value; newGame(); });
      $(".cr-n").addEventListener("change", () => { st.n = Number($(".cr-n").value); });
      const seed = seedControls(box, $(".cr-anchor"), (rng) => {
        st.coins = Array.from({ length: st.n }, () => 1 + Math.floor(rng() * 20)); $(".cr-err").textContent = ""; newGame();
      }, { fresh: false });
      $(".cr-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(0, st.k - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = full().moves.length; draw(); });
      $(".ex-reset").addEventListener("click", () => {
        Object.assign(st, { coins: [...d0.coins], players: [d0.a, d0.b], n: 6 }); $(".cr-n").value = "6"; $(".cr-err").textContent = ""; newGame();
      });
      // the human moves ride in the link: "LRL"
      box.dvqExtra = {
        get: () => st.human.join(""),
        set: (text) => { if (!/^[LR]{1,12}$/.test(text)) return false; st.human = text.split(""); st.k = full().moves.length; draw(); return true; },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { coinrow: coinrowView },
    help: {
      coinrow: "בוחרים מי משחק בכל צד : אתם (לוחצים על אחד הקצוות כשמגיע תורכם), חמדן, הטריק של הזוגיות או משחק אופטימלי, ומריצים מהלך אחרי מהלך. מתחת לשורה הטבלה d[i][j] : היתרון של מי שתורו בכל קטע, הקטע של הרגע מסומן, ולצידה המהלך שהיא ממליצה עליו.",
    },
    models: { crDiff, crPlay },
  });
})();
