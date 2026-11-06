// kinds: chomp
//   chomp                  0091        Chomp, the poisoned chocolate bar (a1 at the bottom left; eating a square eats it and everything above it and to its right): mode play, a game against the computer on m rows x n columns with perfect play, who starts, the winning and losing squares marked on request; mode mirror, a square board where the computer opens with b2 and answers every move with its mirror in the other arm of the L (a random move for the opponent on request); undo and a log of the moves
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, ltr } = dvqExplorers.lib;
  const NB = " ";
  const COLS = "abcdefgh";

  // --- the theory (tests/0091 compares these with the page's Python code) ----------------------
  // a position: the column heights, column a first, never rising to the right
  const eat = (h, c, r) => h.map((x, i) => (i >= c ? Math.min(x, r) : x));
  const size = (h) => h.reduce((a, b) => a + b, 0);
  const poisonOnly = (h) => h[0] === 1 && h.every((x, i) => i === 0 || x === 0);
  const memo = new Map();
  // the player to move wins from h (the poison is never a move: with a1 alone, the player loses)
  const wins = (h) => {
    const k = h.join(",");
    if (memo.has(k)) return memo.get(k);
    let w = false;
    for (let c = 0; c < h.length && !w; c++) for (let r = 0; r < h[c] && !w; r++) if ((c || r) && !wins(eat(h, c, r))) w = true;
    memo.set(k, w);
    return w;
  };
  // every winning move [column, row], column by column, as the page's winning_moves
  const winningMoves = (h) => {
    const out = [];
    for (let c = 0; c < h.length; c++) for (let r = 0; r < h[c]; r++) if ((c || r) && !wins(eat(h, c, r))) out.push([c, r]);
    return out;
  };
  // the computer: the first winning move; in a lost position the move that eats the fewest
  // squares (the rightmost, then the highest, of those); with a1 alone, a1
  const computerMove = (h) => {
    if (poisonOnly(h)) return [0, 0];
    const w = winningMoves(h);
    if (w.length) return w[0];
    let best = null, bestEaten = Infinity;
    for (let c = 0; c < h.length; c++) for (let r = 0; r < h[c]; r++) {
      if (!c && !r) continue;
      const e = size(h) - size(eat(h, c, r));
      if (e < bestEaten || (e === bestEaten && (c > best[0] || (c === best[0] && r > best[1])))) { best = [c, r]; bestEaten = e; }
    }
    return best;
  };
  // the mirror strategy on a square board: b2 first, then keep the two arms of the L equal
  const mirrorMove = (h) => {
    if (h.length > 1 && h[1] > 1) return [1, 1];
    const up = h[0] - 1, right = h.filter((x) => x > 0).length - 1;
    if (up > right) return [0, right + 1];
    if (right > up) return [up + 1, 0];
    return null;
  };
  const legal = (h, c, r) => Number.isInteger(c) && Number.isInteger(r) && c >= 0 && c < h.length && r >= 0 && r < h[c];
  // the game: the computer plays at once on its turns, the human moves are taken in order
  // while they are legal; who = 0 the human, 1 the computer. Eating a1 ends the game, and
  // so does a1 left alone (the player to move has to eat it).
  const chompPlay = (mode, m, n, first, human) => {
    let h = new Array(n).fill(m);
    const moves = [];
    let who = mode === "mirror" || first === "pc" ? 1 : 0, k = 0, bad = false, loser = null;
    for (;;) {
      if (poisonOnly(h)) { loser = who; break; }
      let mv;
      if (who === 1) mv = mode === "mirror" ? (mirrorMove(h) || computerMove(h)) : computerMove(h);
      else if (k < human.length) {
        mv = human[k];
        if (!legal(h, mv[0], mv[1])) { bad = true; break; }
        k++;
      } else break;
      const before = h;
      h = eat(h, mv[0], mv[1]);
      moves.push({ who, c: mv[0], r: mv[1], eaten: size(before) - size(h), before });
      if (!mv[0] && !mv[1]) { loser = who; break; }
      who ^= 1;
    }
    return { h, moves, who, over: loser !== null, loser, used: k, bad };
  };
  const sq = (c, r) => `${COLS[c]}${r + 1}`;

  // --- the view --------------------------------------------------------------------------------
  const S = 34, LM = 18, BM = 18, TOP = 26;   // TOP: room for the enlarge button over the board
  const chompView = () => ({
    mount(box) {
      const mode = box.dataset.mode === "mirror" ? "mirror" : "play";
      const clamp = (v, lo, hi, d) => { const x = Math.floor(Number(v)); return Number.isFinite(x) ? Math.min(hi, Math.max(lo, x)) : d; };
      const n0 = clamp(box.dataset.n, mode === "mirror" ? 2 : 1, 8, 4), m0 = mode === "mirror" ? n0 : clamp(box.dataset.m, 1, 8, 4);
      const st = { m: m0, n: n0, first: "me", human: [], hint: false, focus: [0, 0] };
      const opts = (lo, hi, v, f) => Array.from({ length: hi - lo + 1 }, (_, i) => lo + i).map((x) => `<option value="${x}"${x === v ? " selected" : ""}>${f(x)}</option>`).join("");
      box.innerHTML =
        `<div class="ex-controls">` +
        (mode === "mirror"
          ? `<label>הלוח <select class="cp-size" aria-label="גודל הלוח הריבועי">${opts(2, 8, n0, (x) => `${x} × ${x}`)}</select></label>`
          : `<label>שורות <select class="cp-m" aria-label="מספר השורות">${opts(1, 8, m0, String)}</select></label>` +
            `<label>עמודות <select class="cp-n" aria-label="מספר העמודות">${opts(1, 8, n0, String)}</select></label>` +
            `<label>מתחיל <select class="cp-first" aria-label="מי מתחיל"><option value="me">אני</option><option value="pc">המחשב</option></select></label>`) +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls">` +
        `<button type="button" class="md-button md-button--primary cp-new">משחק חדש</button>` +
        `<button type="button" class="md-button cp-undo">ביטול המהלך שלי</button>` +
        (mode === "mirror"
          ? `<button type="button" class="md-button cp-rand">מהלך אקראי של היריב</button>`
          : `<button type="button" class="md-button cp-hint" aria-pressed="false">סימון המהלכים</button>`) +
        `</div>` +
        `<div class="cp-wrap"></div>` +
        `<span class="viz-legend"><span><i class="cp-key-sq"></i>שוקולד</span><span><i class="cp-key-poison"></i>a1 המורעלת</span>` +
        `<span><i class="cp-key-pick"></i>המהלך האחרון</span><span><i class="cp-key-gone"></i>מה שהוא אכל</span>` +
        (mode === "play" ? `<span><i class="cp-key-win"></i>מהלך מנצח</span><span><i class="cp-key-lose"></i>מהלך מפסיד</span>` : "") + `</span>` +
        `<p class="ex-summary cp-sum" aria-live="polite"></p>` +
        `<p class="cp-why"></p>` +
        `<ol class="cp-log" data-steady></ol>`;
      const $ = (s) => box.querySelector(s);
      const wrap = $(".cp-wrap");
      const game = () => chompPlay(mode, st.m, st.n, st.first, st.human);
      const draw = (focus = false) => {
        const g = game(), h = g.h, m = st.m, n = st.n;
        const myTurn = !g.over && g.who === 0;
        const last = g.moves.length ? g.moves[g.moves.length - 1] : null;
        const marks = mode === "play" && st.hint && myTurn;
        if (mode === "mirror") $(".cp-size").value = String(n);
        else { $(".cp-m").value = String(m); $(".cp-n").value = String(n); $(".cp-first").value = st.first; $(".cp-hint").setAttribute("aria-pressed", String(st.hint)); }
        $(".cp-undo").disabled = !st.human.length;
        if ($(".cp-rand")) $(".cp-rand").disabled = !myTurn;
        // keep the focus on a square that is left
        let [fc, fr] = st.focus;
        if (!(fr < h[fc])) { fc = 0; fr = 0; }
        st.focus = [fc, fr];
        const w = LM + n * S + 4, ht = TOP + m * S + BM + 4;
        let s = `<svg class="figure cp-board" viewBox="0 0 ${w} ${ht}" style="max-width:${Math.min(24, (w * 1.2) / 16).toFixed(1)}rem" ` +
          `role="${myTurn ? "group" : "img"}" aria-label="טבלה של ${m} שורות ו-${n} עמודות, נשארו ${size(h)} משבצות${myTurn ? ". לוחצים על משבצת, או עוברים בחיצים ולוחצים Enter" : ""}">`;
        for (let c = 0; c < n; c++) for (let r = 0; r < m; r++) {
          const x = LM + c * S + 2, y = TOP + (m - 1 - r) * S;
          let cell;
          if (r < h[c]) {
            const poison = !c && !r;
            cell = `<rect class="${poison ? "cp-poison" : "cp-sq"}" x="${x + 1}" y="${y + 1}" width="${S - 2}" height="${S - 2}" rx="4"/>`;
            if (poison) {
              const d = S * 0.26, cx = x + S / 2, cy = y + S / 2;
              cell += `<path class="cp-cross" d="M${cx - d},${cy - d} L${cx + d},${cy + d} M${cx - d},${cy + d} L${cx + d},${cy - d}"/>`;
            }
            if (marks) {
              const win = (c || r) && !wins(eat(h, c, r));
              cell += `<rect class="${win ? "cp-win" : "cp-lose"}" x="${x + 4}" y="${y + 4}" width="${S - 8}" height="${S - 8}" rx="3"/>`;
            }
            if (myTurn) {
              const e = size(h) - size(eat(h, c, r));
              const name = poison ? `${sq(c, r)}${NB}: המשבצת המורעלת, מי שאוכל אותה מפסיד` : `${sq(c, r)}${NB}: אוכלים ${e === 1 ? "משבצת אחת" : `${e} משבצות`}`;
              const tab = c === fc && r === fr ? 0 : -1;
              cell = `<g class="cp-btn" role="button" tabindex="${tab}" data-c="${c}" data-r="${r}" aria-label="${name}">${cell}` +
                `<rect class="cp-ring" x="${x + 1}" y="${y + 1}" width="${S - 2}" height="${S - 2}" rx="4"/></g>`;
            }
          } else if (last && r < last.before[c]) {
            cell = `<rect class="cp-gone" x="${x + 3}" y="${y + 3}" width="${S - 6}" height="${S - 6}" rx="4"/>`;
          } else {
            cell = `<rect class="cp-empty" x="${x + 1}" y="${y + 1}" width="${S - 2}" height="${S - 2}" rx="4"/>`;
          }
          s += cell;
        }
        if (last) {
          const x = LM + last.c * S + 2, y = TOP + (m - 1 - last.r) * S;
          s += `<rect class="cp-pick" x="${x + 1}" y="${y + 1}" width="${S - 2}" height="${S - 2}" rx="4"/>`;
        }
        for (let c = 0; c < n; c++) s += `<text class="cp-lab" x="${LM + c * S + 2 + S / 2}" y="${TOP + m * S + 14}" text-anchor="middle">${COLS[c]}</text>`;
        for (let r = 0; r < m; r++) s += `<text class="cp-lab" x="${LM / 2}" y="${TOP + (m - 1 - r) * S + S / 2 + 4}" text-anchor="middle">${r + 1}</text>`;
        wrap.innerHTML = s + `</svg>`;
        if (focus) { const el = wrap.querySelector(".cp-btn[tabindex='0']"); if (el) el.focus(); }
        // the summary, the reason and the log
        const who = (x) => (x === 0 ? "אתם" : "המחשב");
        let sum;
        if (g.over) sum = g.moves.length && last.c === 0 && last.r === 0 ? `${g.loser === 0 ? "אכלתם" : "המחשב אכל"} את a1 המורעלת.` : `נשארה רק a1, והתור ${g.loser === 0 ? "שלכם" : "של המחשב"}.`;
        else if (myTurn) sum = `<b>תורכם${NB}:</b> לוחצים על משבצת, והיא וכל מה שמעליה ומימינה נאכלים. נשארו ${ltr(size(h))} משבצות.`;
        else sum = "התור של המחשב.";
        $(".cp-sum").innerHTML = sum;
        let why = "";
        if (!g.over) {
          if (mode === "mirror") {
            const up = h[0] - 1, right = h.filter((x) => x > 0).length - 1;
            const mv = last && last.who === 1 ? last : null;
            why = mv && mv.c === 1 && mv.r === 1
              ? `המחשב פתח ב-b2${NB}: נשארו שתי זרועות, ${ltr(up)} משבצות למעלה ו-${ltr(right)} ימינה. מעכשיו הוא עונה על כל מהלך במהלך המקביל בזרוע השנייה.`
              : mv ? `המחשב ענה ב-${sq(mv.c, mv.r)}${NB}: שתי הזרועות שוות שוב, ${ltr(up)} משבצות בכל אחת.` : "";
          } else if (st.hint && myTurn) {
            const wm = winningMoves(h);
            why = wm.length ? `${wm.length === 1 ? "המהלך המנצח" : "המהלכים המנצחים"}${NB}: ${wm.map(([c, r]) => sq(c, r)).join(", ")}. כל מהלך אחר משאיר למחשב מצב מנצח.`
              : `אין מהלך מנצח${NB}: כל מהלך משאיר למחשב מצב מנצח, ונשאר לקוות שהוא יטעה.`;
          } else if (myTurn) {
            why = wins(h) ? "מי שתורו כאן מנצח, אם ימצא את המהלך." : "מי שתורו כאן מפסיד, אם היריב לא טועה.";
          }
        }
        $(".cp-why").innerHTML = why;
        const ate = (x) => (x === 0 ? "אכלתם" : "המחשב אכל");
        $(".cp-log").innerHTML = g.moves.map((mv) => `<li>${ate(mv.who)} ${mv.c || mv.r ? `${mv.eaten === 1 ? "משבצת אחת" : `${ltr(mv.eaten)} משבצות`} ב-${sq(mv.c, mv.r)}` : "את a1 המורעלת"}</li>`).join("");
        if (g.over) answer(box, g.loser === 1 ? `ניצחתם, אחרי ${ltr(g.moves.length)} מהלכים.` : `המחשב ניצח, אחרי ${ltr(g.moves.length)} מהלכים.`);
        else answer(box, null);
      };
      const act = (c, r) => {
        const g = game();
        if (g.over || g.who !== 0 || !legal(g.h, c, r)) return;
        st.human = st.human.slice(0, g.used).concat([[c, r]]);
        st.focus = [0, 0];
        draw(true);
      };
      const newGame = () => { st.human = []; draw(); };
      wrap.addEventListener("click", (e) => { const b = e.target.closest(".cp-btn"); if (b) act(Number(b.dataset.c), Number(b.dataset.r)); });
      // the arrow keys move between the squares that are left (a1 at the bottom left)
      wrap.addEventListener("keydown", (e) => {
        const b = e.target.closest(".cp-btn");
        if (!b) return;
        const c = Number(b.dataset.c), r = Number(b.dataset.r);
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); e.stopPropagation(); act(c, r); return; }
        const dir = { ArrowUp: [0, 1], ArrowDown: [0, -1], ArrowLeft: [-1, 0], ArrowRight: [1, 0] }[e.key];
        if (!dir) return;
        e.preventDefault(); e.stopPropagation();
        const nc = c + dir[0], nr = r + dir[1];
        const t = wrap.querySelector(`.cp-btn[data-c="${nc}"][data-r="${nr}"]`);
        if (!t) return;
        wrap.querySelectorAll(".cp-btn").forEach((el) => el.setAttribute("tabindex", "-1"));
        t.setAttribute("tabindex", "0"); t.focus();
        st.focus = [nc, nr];
      });
      if (mode === "mirror") {
        $(".cp-size").addEventListener("change", () => { st.m = st.n = clamp($(".cp-size").value, 2, 8, n0); newGame(); });
        $(".cp-rand").addEventListener("click", () => {
          const g = game();
          if (g.over || g.who !== 0) return;
          const opts2 = [];
          g.h.forEach((height, c) => { for (let r = 0; r < height; r++) if (c || r) opts2.push([c, r]); });
          if (opts2.length) act(...opts2[Math.floor(Math.random() * opts2.length)]);
        });
      } else {
        $(".cp-m").addEventListener("change", () => { st.m = clamp($(".cp-m").value, 1, 8, m0); newGame(); });
        $(".cp-n").addEventListener("change", () => { st.n = clamp($(".cp-n").value, 1, 8, n0); newGame(); });
        $(".cp-first").addEventListener("change", () => { st.first = $(".cp-first").value; newGame(); });
        $(".cp-hint").addEventListener("click", () => { st.hint = !st.hint; draw(); });
      }
      $(".cp-new").addEventListener("click", newGame);
      $(".cp-undo").addEventListener("click", () => { st.human.pop(); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, { m: m0, n: n0, first: "me", human: [], hint: false, focus: [0, 0] }); draw(); });
      // my moves ride in the link: "column.row" pairs, "1.1,0.3"
      box.dvqExtra = {
        get: () => st.human.map(([c, r]) => `${c}.${r}`).join(","),
        set: (text) => {
          if (!/^\d\.\d(,\d\.\d){0,63}$/.test(text)) return false;
          const human = text.split(",").map((p) => p.split(".").map(Number));
          const g = chompPlay(mode, st.m, st.n, st.first, human);
          if (g.bad || g.used !== human.length) return false;
          st.human = human; draw(); return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { chomp: chompView },
    help: {
      chomp: "טבלת שוקולד, והמשבצת a1 בפינה השמאלית התחתונה מורעלת. לחיצה על משבצת אוכלת אותה ואת כל מה שמעליה ומימינה, ומי שאוכל את a1 מפסיד. במשחק נגד המחשב בוחרים גודל ומי מתחיל, ו\"סימון המהלכים\" מסמן בירוק מהלך מנצח ובאפור מקווקו מהלך מפסיד. במשחק המראה המחשב פותח ב-b2 ועונה על כל מהלך במהלך המקביל בזרוע השנייה.",
    },
    models: { chompEat: eat, chompWins: wins, chompWinningMoves: winningMoves, chompComputerMove: computerMove, chompMirrorMove: mirrorMove, chompPlay },
  });
})();
