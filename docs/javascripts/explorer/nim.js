// kinds: nim
//   nim                    0082        a game of Nim against the computer: the heaps typed, the rule (the last to take wins, the last to take loses, or a move takes only 1, 3 or 4), who starts; a token clicked takes it and every token after it in its heap, and the computer answers with its best move; the heaps in binary with the XOR row (the Grundy numbers in the subtraction game), the winning move marked on request, undo and a log of the moves
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, ltr } = dvqExplorers.lib;
  const NB = " ";

  // --- the theory (tests/0082 compares these with the page's Python code) --------------------
  const SUB = [1, 3, 4];
  const nimXor = (h) => h.reduce((a, b) => a ^ b, 0);
  // normal Nim: a winning move [heap, new size], or null when the player to move loses
  const nimMove = (h) => {
    const x = nimXor(h);
    if (!x) return null;
    for (let i = 0; i < h.length; i++) if ((h[i] ^ x) < h[i]) return [i, h[i] ^ x];
    return null;
  };
  // misère Nim (the last to take loses), at least one token on the table
  const misereMove = (h) => {
    const big = [], ones = h.filter((v) => v === 1).length;
    h.forEach((v, i) => { if (v > 1) big.push(i); });
    if (big.length === 1) return [big[0], ones % 2 === 0 ? 1 : 0];
    if (!big.length) return ones && ones % 2 === 0 ? [h.indexOf(1), 0] : null;
    return nimMove(h);
  };
  // the Grundy numbers g[0..n] of one heap when a move takes one of `moves`
  const grundy = (n, moves = SUB) => {
    const g = [0];
    for (let k = 1; k <= n; k++) {
      const seen = new Set(moves.filter((m) => m <= k).map((m) => g[k - m]));
      let v = 0;
      while (seen.has(v)) v++;
      g.push(v);
    }
    return g;
  };
  // the sum of subtraction games: a winning move, or null
  const subMove = (h, moves = SUB) => {
    const g = grundy(Math.max(0, ...h), moves), x = h.reduce((a, v) => a ^ g[v], 0);
    if (!x) return null;
    for (let i = 0; i < h.length; i++) for (const m of moves) if (m <= h[i] && g[h[i] - m] === (g[h[i]] ^ x)) return [i, h[i] - m];
    return null;
  };
  const RULES = { normal: nimMove, misere: misereMove, sub: subMove };
  const legal = (rule, h, i, nw) => Number.isInteger(i) && i >= 0 && i < h.length && Number.isInteger(nw) && nw >= 0 && nw < h[i] &&
    (rule !== "sub" || SUB.includes(h[i] - nw));
  // the computer: the winning move, and in a lost position one token from the largest heap
  const computerMove = (rule, h) => {
    const m = RULES[rule](h);
    if (m) return m;
    let i = 0;
    h.forEach((v, k) => { if (v > h[i]) i = k; });
    return [i, h[i] - 1];
  };
  // the game from `start`: the computer plays at once on its turns, the human moves are
  // taken in order while they are legal; who = 0 me, 1 the computer
  const nimPlay = (rule, start, first, human) => {
    const h = [...start], moves = [];
    let who = first === "pc" ? 1 : 0, k = 0, bad = false;
    while (h.some((v) => v > 0)) {
      let m;
      if (who === 1) m = computerMove(rule, h);
      else if (k < human.length) {
        m = human[k];
        if (!legal(rule, h, m[0], m[1])) { bad = true; break; }
        k++;
      } else break;
      moves.push([who, m[0], h[m[0]], m[1]]);
      h[m[0]] = m[1];
      who ^= 1;
    }
    const over = !h.some((v) => v > 0);
    // the last mover: wins, or loses when the last to take loses
    const last = moves.length ? moves[moves.length - 1][0] : null;
    const winner = !over || last === null ? null : rule === "misere" ? last ^ 1 : last;
    return { heaps: h, moves, who, over, winner, used: k, bad };
  };

  const NMAX = 6, HMAX = 20;
  const parse = (text) => {
    const v = String(text).split(/[\s,]+/).filter(Boolean).map(Number);
    return v.length >= 1 && v.length <= NMAX && v.every((x) => Number.isInteger(x) && x >= 1 && x <= HMAX) ? v : null;
  };
  const NAMES = { normal: "האחרון שלוקח מנצח", misere: "האחרון שלוקח מפסיד", sub: "לוקחים רק 1, 3 או 4" };

  const nimView = () => ({
    mount(box) {
      const d0 = { heaps: parse(box.dataset.heaps || "3,4,5") || [3, 4, 5], rule: RULES[box.dataset.rule] ? box.dataset.rule : "normal", first: "me" };
      const st = { heaps: [...d0.heaps], rule: d0.rule, first: d0.first, human: [] };
      const opt = (o, v) => Object.entries(o).map(([k, t]) => `<option value="${k}"${k === v ? " selected" : ""}>${t}</option>`).join("");
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>הערימות</span><input type="text" class="ex-num nim-heaps" dir="ltr" aria-label="גדלי הערימות, מופרדים בפסיקים : עד ${NMAX} ערימות, כל אחת 1 עד ${HMAX}"></label>` +
        `<label>החוק <select class="nim-rule" aria-label="חוק המשחק">${opt(NAMES, st.rule)}</select></label>` +
        `<label>מתחיל <select class="nim-first" aria-label="מי מתחיל">${opt({ me: "אני", pc: "המחשב" }, st.first)}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err nim-err"></span></div>` +
        `<div class="ex-controls">` +
        `<button type="button" class="md-button nim-new">משחק חדש</button>` +
        `<button type="button" class="md-button nim-undo">ביטול המהלך שלי</button>` +
        `<label class="nim-hintlab"><input type="checkbox" class="nim-hint"> הצגת המהלך המנצח</label></div>` +
        `<p class="ex-summary nim-sum" aria-live="polite"></p>` +
        `<div class="nim-board" role="group" aria-label="הערימות : לחיצה על אסימון לוקחת אותו ואת כל האסימונים שאחריו בערימה"></div>` +
        `<span class="viz-legend"><span><i class="nim-key-tok"></i>אסימון שאפשר לקחת</span><span><i class="nim-key-hint"></i>המהלך המנצח</span><span><i class="nim-key-gone"></i>נלקח</span></span>` +
        `<p class="ex-title nim-bintitle"></p>` +
        `<div class="gs-scroll" data-steady><table class="gs-bits nim-bin" dir="ltr" aria-label="הערימות בבינארי ושורת ה-XOR"><tbody></tbody></table></div>` +
        `<p class="nim-why"></p>` +
        `<ol class="nim-log" data-steady></ol>`;
      const $ = (s) => box.querySelector(s);
      const game = () => nimPlay(st.rule, st.heaps, st.first, st.human);
      const draw = () => {
        const g = game(), h = g.heaps, rule = st.rule;
        $(".nim-err").textContent = ""; $(".nim-heaps").value = st.heaps.join(", "); $(".nim-rule").value = rule; $(".nim-first").value = st.first;
        const myTurn = !g.over && g.who === 0;
        const best = g.over ? null : RULES[rule](h);
        const hint = $(".nim-hint").checked && myTurn && best;
        $(".nim-undo").disabled = !st.human.length;
        // the board: every token of the start, the taken ones hollow, so the board keeps its size
        $(".nim-board").innerHTML = st.heaps.map((size, i) => {
          let row = `<div class="nim-heap"><span class="nim-lab">ערימה ${i + 1}${NB}: <b>${ltr(h[i])}</b></span><span class="nim-toks">`;
          for (let j = 0; j < size; j++) {
            if (j >= h[i]) { row += `<span class="nim-tok is-gone" aria-hidden="true"></span>`; continue; }
            const take = h[i] - j, ok = myTurn && legal(rule, h, i, j);
            const cls = hint && best[0] === i && j >= best[1] ? " is-hint" : "";
            row += `<button type="button" class="nim-tok${cls}" data-i="${i}" data-j="${j}"${ok ? "" : " disabled"} ` +
              `aria-label="לקחת ${take} מערימה ${i + 1}" title="לקחת ${take}"></button>`;
          }
          return row + `</span></div>`;
        }).join("");
        // the table: the sizes (or the Grundy numbers) in binary, and their XOR
        const gr = grundy(Math.max(...st.heaps));
        const vals = rule === "sub" ? h.map((v) => gr[v]) : h;
        const x = vals.reduce((a, b) => a ^ b, 0), W = 5;
        const top = x ? 31 - Math.clz32(x) : -1;
        $(".nim-bintitle").textContent = rule === "sub" ? "מספרי גרנדי של הערימות בבינארי, וה-XOR שלהם" : "הערימות בבינארי, וה-XOR שלהן";
        const bitRow = (label, v, isX) => {
          let r = `<tr><th>${label}</th>`;
          for (let b = W - 1; b >= 0; b--) {
            const on = (v >> b) & 1;
            const cls = isX ? (x ? (on ? " is-one" : "") + (b === top ? " nim-top" : "") : " nim-zero") : (on ? " is-one" : "") + (b === top && on ? " nim-top" : "");
            r += `<td class="gs-b${cls}">${on}</td>`;
          }
          return r + `<td class="gs-val">= ${v}</td></tr>`;
        };
        $(".nim-bin tbody").innerHTML = vals.map((v, i) => bitRow(rule === "sub" ? `g(${h[i]})` : `ערימה ${i + 1}`, v)).join("") + bitRow("XOR", x, true);
        // the summary and the reason
        const who = (w) => (w === 0 ? "אתם" : "המחשב");
        $(".nim-sum").innerHTML = `${NAMES[rule]}. ` + (g.over ? `המשחק נגמר.` :
          myTurn ? `<b>תורכם${NB}:</b> לוחצים על אסימון, והוא וכל האסימונים שאחריו בערימה נלקחים.` : `התור של המחשב.`);
        let why;
        if (g.over) why = "";
        else if (rule === "misere" && !h.some((v) => v > 1)) {
          const ones = h.filter((v) => v === 1).length;
          why = `כל הערימות 1 או 0${NB}: יש ${ltr(ones)} ערימות של 1, ומי שתורו כשהמספר אי-זוגי מפסיד. ` + (ones % 2 ? `כאן הוא אי-זוגי, ולכן מי שתורו מפסיד.` : `כאן הוא זוגי, ולכן מי שתורו מנצח.`);
        } else if (rule === "misere" && h.filter((v) => v > 1).length === 1) {
          why = `נשארה ערימה אחת גדולה מ-1${NB}: מי שתורו מנצח. מורידים אותה ל-0 או ל-1 כך שיישאר מספר אי-זוגי של ערימות של 1.`;
        } else {
          why = x ? `${ltr(`XOR = ${x}`)}${NB}: מי שתורו מנצח.` : `${ltr("XOR = 0")}${NB}: מי שתורו מפסיד, אם היריב לא טועה.`;
        }
        if (!g.over && $(".nim-hint").checked) {
          why += best ? ` המהלך המנצח${NB}: מערימה ${ltr(best[0] + 1)} לוקחים ${ltr(h[best[0]] - best[1])}, ונשארים בה ${ltr(best[1])}.` : ` אין מהלך מנצח${NB}: כל מהלך משאיר ליריב מצב מנצח.`;
        }
        $(".nim-why").innerHTML = why;
        $(".nim-log").innerHTML = g.moves.map(([w, i, from, to]) => `<li>${who(w)}${NB}: מערימה ${ltr(i + 1)} לקחו ${ltr(from - to)}, ${ltr(`${from} → ${to}`)}</li>`).join("");
        if (g.over) answer(box, g.winner === 0 ? `ניצחתם, אחרי ${ltr(g.moves.length)} מהלכים.` : `המחשב ניצח, אחרי ${ltr(g.moves.length)} מהלכים.`);
        else answer(box, null);
      };
      const newGame = () => { st.human = []; draw(); };
      $(".nim-board").addEventListener("click", (e) => {
        const b = e.target.closest(".nim-tok");
        if (!b || b.disabled || b.tagName !== "BUTTON") return;
        st.human = st.human.slice(0, game().used).concat([[Number(b.dataset.i), Number(b.dataset.j)]]);
        draw();
        const next = box.querySelector(".nim-tok:not([disabled])");
        if (next && document.activeElement === document.body) next.focus();
      });
      $(".nim-heaps").addEventListener("change", () => {
        const v = parse($(".nim-heaps").value);
        $(".nim-err").textContent = v ? "" : `הערימות${NB}: 1 עד ${NMAX} מספרים שלמים, כל אחד 1 עד ${HMAX}`;
        if (v) { st.heaps = v; newGame(); }
      });
      $(".nim-heaps").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".nim-heaps").blur(); });
      $(".nim-rule").addEventListener("change", () => { st.rule = $(".nim-rule").value; newGame(); });
      $(".nim-first").addEventListener("change", () => { st.first = $(".nim-first").value; newGame(); });
      $(".nim-hint").addEventListener("change", draw);
      $(".nim-new").addEventListener("click", newGame);
      $(".nim-undo").addEventListener("click", () => { st.human.pop(); draw(); });
      $(".ex-reset").addEventListener("click", () => {
        Object.assign(st, { heaps: [...d0.heaps], rule: d0.rule, first: d0.first, human: [] });
        $(".nim-hint").checked = false; $(".nim-err").textContent = ""; draw();
      });
      // my moves ride in the link: "heap.new" pairs, "0.1,2.3"
      box.dvqExtra = {
        get: () => st.human.map(([i, j]) => `${i}.${j}`).join(","),
        set: (text) => {
          if (!/^\d+\.\d+(,\d+\.\d+){0,59}$/.test(text)) return false;
          const human = text.split(",").map((p) => p.split(".").map(Number));
          const g = nimPlay(st.rule, st.heaps, st.first, human);
          if (g.bad || g.used !== human.length) return false;
          st.human = human; draw(); return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { nim: nimView },
    help: {
      nim: "מקלידים את הערימות, בוחרים חוק ומי מתחיל, ומשחקים נגד המחשב : לחיצה על אסימון לוקחת אותו ואת כל האסימונים שאחריו בערימה, והמחשב עונה במהלך הטוב ביותר. מתחת ללוח הערימות בבינארי (או מספרי גרנדי שלהן) ושורת ה-XOR, ו\"הצגת המהלך המנצח\" מסמנת את האסימונים שכדאי לקחת.",
    },
    models: { nimXor, nimMove, misereMove, grundy, subMove, computerMove, nimPlay, nimLegal: legal },
  });
})();
