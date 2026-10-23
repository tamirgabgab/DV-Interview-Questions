// kinds: ttt
//   ttt                    0011        tap cells on a 3 x 3 board: is it a legal final board and why not; random legal boards; wrap diagonals
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { ltr, seedControls } = dvqExplorers.lib;

  // Tic-tac-toe final boards (0011): the page's four conditions on a board of "X", "O"
  // and "." (cells 0..8 row by row), with the reason a board fails; every legal final
  // board counted once per line set; a draw of the page's randomize().
  const TTT_LINES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
  const TTT_WRAP = TTT_LINES.concat([[1, 5, 6], [2, 3, 7], [0, 5, 7], [1, 3, 8]]);
  const tttCheck = (board, wrap = false) => {
    const lines = wrap ? TTT_WRAP : TTT_LINES;
    const nX = board.filter((c) => c === "X").length, nO = board.filter((c) => c === "O").length;
    const won = (p) => lines.map((l, i) => (l.every((c) => board[c] === p) ? i : -1)).filter((i) => i >= 0);
    const xLines = won("X"), oLines = won("O");
    let result = null, reason = null;
    if (nX !== nO && nX !== nO + 1) reason = "count";
    else if (xLines.length && oLines.length) reason = "both";
    else if (xLines.length) { if (nX === nO + 1) result = "X"; else reason = "o_after"; }
    else if (oLines.length) { if (nX === nO) result = "O"; else reason = "x_after"; }
    else if (nX + nO === 9) result = "draw";
    else reason = "unfinished";
    return { nX, nO, xLines, oLines, result, reason, lines };
  };
  let tttGroupsCache = {};
  const tttFinalBoards = (wrap = false) => {
    const key = wrap ? "wrap" : "plain";
    if (tttGroupsCache[key]) return tttGroupsCache[key];
    const groups = { X: [], O: [], draw: [] };
    const board = new Array(9).fill(".");
    for (let n = 0; n < 19683; n++) {
      let m = n;
      for (let i = 0; i < 9; i++) { board[i] = ".XO"[m % 3]; m = Math.floor(m / 3); }
      const r = tttCheck(board, wrap).result;
      if (r) groups[r].push(board.join(""));
    }
    tttGroupsCache[key] = groups;
    return groups;
  };
  const tttRandom = (wrap = false, rnd = Math.random) => {
    const groups = tttFinalBoards(wrap);
    const results = Object.keys(groups).filter((r) => groups[r].length);
    const result = results[Math.floor(rnd() * results.length)];
    const boards = groups[result];
    return { result, board: boards[Math.floor(rnd() * boards.length)].split("") };
  };

  // The tic-tac-toe box (0011): tap a cell to cycle empty, X, O; the page's conditions
  // decide live whether the board is a legal final board and say why not; a random
  // legal board as the page's randomize() draws it; the wrap-around diagonals of part b
  // as a toggle, with the counts of final boards per line set.
  const tttView = () => ({
    mount(box) {
      const st = { board: (box.dataset.board || "XXXOXOOOX").split(""), wrap: false };
      const num = (v) => Number(v).toLocaleString("en-US");
      const REASON = {
        count: "מספר ה-X חייב להיות שווה למספר ה-O או גדול ממנו ב-1 : X מתחיל ומשחקים לסירוגין.",
        both: "לשני השחקנים יש שלישייה. המשחק נעצר ברגע שהראשון השלים אחת.",
        o_after: "ל-X יש שלישייה אבל מספר ה-X שווה למספר ה-O : O שיחק אחרי שהמשחק נגמר.",
        x_after: "ל-O יש שלישייה אבל ל-X יש סימן אחד יותר : X שיחק אחרי שהמשחק נגמר.",
        unfinished: "אין שלישייה והלוח לא מלא : המשחק עוד לא נגמר.",
      };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<button type="button" class="md-button md-button--primary ex-random">לוח חוקי אקראי</button>` +
        `<button type="button" class="md-button ex-clear">ניקוי</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button>` +
        `<label><input type="checkbox" class="ex-wrap"> אלכסונים מסביב (סעיף ב)</label></div>` +
        `<div class="ttt-box"><div class="ttt-board" role="group" aria-label="לוח 3 על 3, לחיצה על משבצת מחליפה ריק, X ו-O"></div>` +
        `<div class="ttt-panel"><p class="ttt-counts"></p><p class="ttt-verdict" aria-live="polite"></p><p class="ttt-why"></p></div></div>` +
        `<p class="ex-summary ttt-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const boardEl = $(".ttt-board");
      const draw = () => {
        const chk = tttCheck(st.board, st.wrap);
        const lit = new Set();
        chk.xLines.concat(chk.oLines).forEach((i) => chk.lines[i].forEach((c) => lit.add(c)));
        const tint = chk.result === "X" || (chk.xLines.length && !chk.oLines.length) ? "cell-s2" : "cell-s1";
        let s = `<svg class="figure ttt-live" viewBox="0 0 114 114">`;
        st.board.forEach((v, i) => {
          const x = 6 + (i % 3) * 34, y = 6 + Math.floor(i / 3) * 34;
          const inX = chk.xLines.some((l) => chk.lines[l].includes(i));
          s += `<g class="ttt-cell" data-i="${i}" tabindex="0" role="button" aria-label="${v === "." ? `${i} : משבצת ריקה` : `${v} במשבצת ${i}`}">` +
               `<rect class="${lit.has(i) ? (inX ? "cell-s2" : "cell-s1") : "ttt-empty"}" x="${x}" y="${y}" width="34" height="34"/>`;
          if (v === "X") s += `<path class="mark" d="M${x + 9},${y + 9} L${x + 25},${y + 25} M${x + 25},${y + 9} L${x + 9},${y + 25}"/>`;
          else if (v === "O") s += `<circle class="mark" cx="${x + 17}" cy="${y + 17}" r="9"/>`;
          else s += `<text class="ttt-idx" x="${x + 17}" y="${y + 21}" text-anchor="middle">${i}</text>`;
          s += `</g>`;
        });
        s += `<line class="ttt-grid" x1="40" x2="40" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="40" y2="40"/>` +
             `<line class="ttt-grid" x1="74" x2="74" y1="6" y2="108"/><line class="ttt-grid" x1="6" x2="108" y1="74" y2="74"/></svg>`;
        boardEl.innerHTML = s;
        void tint;
        const names = (ls) => ls.map((i) => ltr(`{${chk.lines[i].join(", ")}}`)).join(", ");
        $(".ttt-counts").innerHTML = `${ltr(`n_X = ${chk.nX}`)}, ${ltr(`n_O = ${chk.nO}`)}. שלישיות של X : ${chk.xLines.length ? names(chk.xLines) : "אין"}; של O : ${chk.oLines.length ? names(chk.oLines) : "אין"}.`;
        const verdict = chk.result
          ? `<span class="ttt-ok">✓ לוח סיום חוקי : ${chk.result === "draw" ? "תיקו" : `${chk.result} ניצח`}.</span>`
          : `<span class="ttt-bad">✗ לא לוח סיום.</span>`;
        $(".ttt-verdict").innerHTML = verdict;
        $(".ttt-why").innerHTML = chk.result
          ? (chk.result === "draw" ? "הלוח מלא ולאף אחד אין שלישייה." : chk.result === "X"
            ? `ל-X ${chk.xLines.length === 2 ? "שתי שלישיות שנחתכות" : "שלישייה"}, ל-O אין, ו-${ltr("n_X = n_O + 1")} : X שיחק אחרון.`
            : `ל-O שלישייה, ל-X אין, ו-${ltr("n_X = n_O")} : O שיחק אחרון.`)
          : REASON[chk.reason];
        const g = tttFinalBoards(st.wrap), total = g.X.length + g.O.length + g.draw.length;
        $(".ttt-sum").innerHTML = `עם ${st.wrap ? "12" : "8"} הקווים יש ${ltr(num(total))} לוחות סיום מתוך ${ltr("3^9 = 19,683")} מילויים : ` +
          `${ltr(num(g.X.length))} ניצחונות של X, ${ltr(num(g.O.length))} של O ו-${ltr(num(g.draw.length))} תיקו` +
          (st.wrap ? ". תיקו בלתי אפשרי : כל 5 משבצות מכילות קו שלם." : ".") +
          ` "לוח חוקי אקראי" בוחר תוצאה בהסתברות שווה ואז לוח אחיד מבין הלוחות שלה, כמו ${ltr("solve result before board")}.`;
      };
      const cycle = (i) => { st.board[i] = { ".": "X", X: "O", O: "." }[st.board[i]]; draw(); };
      boardEl.addEventListener("click", (e) => { const g = e.target.closest(".ttt-cell"); if (g) cycle(Number(g.dataset.i)); });
      boardEl.addEventListener("keydown", (e) => {
        const g = e.target.closest(".ttt-cell");
        if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); cycle(Number(g.dataset.i)); }
      });
      const seed = seedControls(box, $(".ex-reset"), (rng) => { st.board = tttRandom(st.wrap, rng).board; draw(); });
      $(".ex-random").addEventListener("click", seed.draw);
      $(".ex-clear").addEventListener("click", () => { st.board = new Array(9).fill("."); draw(); });
      const PAGE = st.board.slice();
      $(".ex-reset").addEventListener("click", () => { st.board = PAGE.slice(); draw(); });
      $(".ex-wrap").addEventListener("change", () => { st.wrap = $(".ex-wrap").checked; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { ttt: tttView },
    help: {
      ttt: "לוחצים על משבצות הלוח : התיבה אומרת אם זה לוח סיום חוקי ולמה לא. ״הגרלה״ נותנת לוח חוקי, והבורר מפעיל את האלכסונים המתגלגלים של סעיף ב.",
    },
    models: { TTT_LINES, TTT_WRAP, tttCheck, tttFinalBoards, tttRandom },
  });
})();
