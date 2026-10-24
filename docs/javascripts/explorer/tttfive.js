// kinds: tttfive
//   tttfive                0011        part b's proof on the wrap-around board: up to five cells picked, the 12 lines in four directions of three parallel lines, how the cells split in each direction and the pairs on one line, the full line, and the cells that would complete one
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { ltr } = dvqExplorers.lib;
  const NB = " ";

  // The 12 lines of the wrap-around board in four directions, three parallel lines each:
  // every cell is on one line of each direction, and every pair of cells on exactly one line.
  const FIVE_DIRS = [
    { name: "שורות", lines: [[0, 1, 2], [3, 4, 5], [6, 7, 8]] },
    { name: "טורים", lines: [[0, 3, 6], [1, 4, 7], [2, 5, 8]] },
    { name: "אלכסונים ↘", lines: [[0, 4, 8], [1, 5, 6], [2, 3, 7]] },
    { name: "אלכסונים ↙", lines: [[2, 4, 6], [1, 3, 8], [0, 5, 7]] },
  ];
  const pairsOf = (c) => (c * (c - 1)) / 2;
  // For a set of cells: per direction how many fall on each line and the pairs that share
  // a line; the full lines; and the empty cells that would complete a line.
  const tttFive = (cells) => {
    const set = new Set(cells), m = set.size;
    const dirs = FIVE_DIRS.map((d) => {
      const counts = d.lines.map((l) => l.filter((c) => set.has(c)).length);
      return { name: d.name, lines: d.lines, counts, pairs: counts.reduce((t, c) => t + pairsOf(c), 0) };
    });
    const full = FIVE_DIRS.flatMap((d) => d.lines).filter((l) => l.every((c) => set.has(c)));
    const completers = [];
    for (let c = 0; c < 9; c++) if (!set.has(c) && FIVE_DIRS.some((d) => d.lines.some((l) => l.includes(c) && l.every((u) => u === c || set.has(u))))) completers.push(c);
    return { m, dirs, pairs: pairsOf(m), linePairs: dirs.reduce((t, d) => t + d.pairs, 0), full, completers };
  };

  // The five cells box (0011 part b): tap up to five cells (or type them); a table of the
  // four directions with the split over their three lines and the pairs on one line, the
  // full line drawn on the board, and with four cells and no line the empty cells that
  // would complete one (all of them).
  const tttfiveView = () => ({
    mount(box) {
      const P0 = (box.dataset.cells || "0 1 3 4").trim();
      const parse = (text) => {
        const parts = String(text).trim().split(/[\s,]+/).filter(Boolean);
        if (parts.some((p) => !/^[0-8]$/.test(p))) return null;
        const cells = [...new Set(parts.map(Number))];
        return cells.length <= 5 ? cells.sort((a, b) => a - b) : null;
      };
      let cells = parse(P0) || [];
      box.innerHTML =
        `<div class="ex-controls"><label><span>המשבצות</span><input type="text" class="ex-nums tf-cells" dir="ltr" spellcheck="false" aria-label="המשבצות שנבחרו, מספרים מ-0 עד 8"></label>` +
        `<button type="button" class="md-button ex-clear">ניקוי</button>` +
        `<button type="button" class="md-button ex-reset">הדוגמה מהדף</button><span class="fl-err tf-err" aria-live="polite"></span></div>` +
        `<div class="ttt-box"><div class="ttt-board tf-board"></div><div class="ttt-panel"><p class="tf-status" aria-live="polite"></p><div class="tf-table"></div><p class="ex-summary tf-sum"></p></div></div>`;
      const $ = (sel) => box.querySelector(sel);
      const S = 50, O = 6;
      const board = (r) => {
        const fullCells = new Set(r.full.flat()), star = r.full.length ? new Set() : new Set(r.m === 4 ? r.completers : []);
        let s = `<svg class="figure ttt-live tf-live" viewBox="0 0 ${3 * S + 2 * O} ${3 * S + 2 * O}" role="group" aria-label="לוח 3 על 3, לחיצה בוחרת משבצת">`;
        for (let c = 0; c < 9; c++) {
          const x = O + (c % 3) * S, y = O + Math.floor(c / 3) * S, on = cells.includes(c);
          s += `<g class="ttt-cell tf-cell${on ? " is-on" : ""}${fullCells.has(c) ? " is-full" : ""}" data-c="${c}" tabindex="0" role="button" aria-pressed="${on}" aria-label="משבצת ${c}${on ? ", נבחרה" : ""}${star.has(c) ? ", משלימה קו" : ""}">` +
               `<rect class="ttt-empty" x="${x}" y="${y}" width="${S}" height="${S}"/>` +
               (on ? `<circle class="tf-mark" cx="${x + S / 2}" cy="${y + S / 2}" r="15"/>` : star.has(c) ? `<text class="tf-star" x="${x + S / 2}" y="${y + S / 2 + 7}" text-anchor="middle">★</text>` : "") +
               `<text class="ttt-idx" x="${x + 5}" y="${y + 13}">${c}</text></g>`;
        }
        s += `<path class="ttt-grid" d="M${O + S},${O} V${O + 3 * S} M${O + 2 * S},${O} V${O + 3 * S} M${O},${O + S} H${O + 3 * S} M${O},${O + 2 * S} H${O + 3 * S}" fill="none"/>`;
        return s + "</svg>";
      };
      const draw = () => {
        const r = tttFive(cells);
        $(".tf-board").innerHTML = board(r);
        if (document.activeElement !== $(".tf-cells")) $(".tf-cells").value = cells.join(" ");
        $(".tf-table").innerHTML = `<table class="bridge-table tf-dirs"><thead><tr><th>הכיוון</th><th>שלושת הקווים</th><th>החלוקה</th><th>זוגות על קו</th></tr></thead><tbody>` +
          r.dirs.map((d) => `<tr${d.counts.includes(3) ? ' class="is-full"' : ""}><td>${d.name}</td><td>${ltr(d.lines.map((l) => l.join("")).join(" · "))}</td><td>${ltr(d.counts.join("-"))}</td><td>${d.pairs}</td></tr>`).join("") +
          `</tbody></table>`;
        const fullText = r.full.map((l) => ltr(`{${l.join(", ")}}`)).join(", ");
        $(".tf-status").innerHTML = !r.m ? "לחצו על משבצות, עד חמש."
          : r.full.length ? `<span class="b3-ok">${r.full.length === 1 ? "קו שלם" : "קווים שלמים"}${NB}: ${fullText}.</span>`
          : `<span class="b3-bad">${r.m === 1 ? "משבצת אחת" : `יש ${ltr(r.m)} משבצות`} בלי קו שלם.</span>` + (r.m === 4 ? ` הכוכבים${NB}: כל משבצת ריקה משלימה קו, ולכן המשבצת החמישית תמיד סוגרת אחד.` : "");
        $(".tf-sum").innerHTML = r.m < 2 ? "" :
          `כל זוג משבצות נמצא על קו אחד בדיוק, ולכן סכום העמודה האחרונה הוא ${ltr(`C(${r.m}, 2) = ${r.pairs}`)}${r.linePairs === r.pairs ? " ✓" : ""}. ` +
          (r.m === 5 ? `בלי קו שלם, בכל כיוון החלוקה הייתה ${ltr("2-2-1")}, ‏2 זוגות לכל כיוון, ‏${ltr("4 · 2 = 8")} זוגות בלבד, פחות מ-10. לכן חמש משבצות תמיד מכילות קו.`
            : `בלי קו שלם, כל קו מכיל לכל היותר 2 משבצות, ולכן בכל כיוון יש לכל היותר 2 זוגות.`);
      };
      const setCells = (next) => { cells = next.slice().sort((a, b) => a - b); $(".tf-err").textContent = ""; draw(); };
      const toggle = (c, keyboard) => {
        if (cells.includes(c)) setCells(cells.filter((v) => v !== c));
        else if (cells.length >= 5) $(".tf-err").textContent = "עד חמש משבצות";
        else setCells(cells.concat([c]));
        if (keyboard) { const again = box.querySelector(`.tf-cell[data-c="${c}"]`); if (again) again.focus(); }
      };
      $(".tf-board").addEventListener("click", (e) => { const g = e.target.closest(".tf-cell"); if (g) toggle(Number(g.dataset.c), false); });
      $(".tf-board").addEventListener("keydown", (e) => { const g = e.target.closest(".tf-cell"); if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); e.stopPropagation(); toggle(Number(g.dataset.c), true); } });
      $(".tf-cells").addEventListener("change", () => { const c = parse($(".tf-cells").value); if (c) setCells(c); else $(".tf-err").textContent = "עד חמש משבצות מ-0 עד 8"; });
      $(".tf-cells").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".tf-cells").blur(); });
      $(".ex-clear").addEventListener("click", () => setCells([]));
      $(".ex-reset").addEventListener("click", () => setCells(parse(P0) || []));
      draw();
    },
  });

  dvqExplorers.register({
    views: { tttfive: tttfiveView },
    help: {
      tttfive: "לוחצים על משבצות (עד חמש) או מקלידים אותן : הטבלה מראה לכל אחד מארבעת הכיוונים כמה משבצות על כל אחד משלושת הקווים המקבילים וכמה זוגות על קו, והלוח מסמן קו שלם. עם ארבע משבצות בלי קו, הכוכבים מסמנים משבצות שהיו משלימות קו.",
    },
    models: { FIVE_DIRS, tttFive },
  });
})();
