// kinds: oddball
//   oddball                0045        N balls from 3 to 39: the minimum number of weighings, the fixed weighings as rows of balances, and the decision table from the outcomes to the odd ball; a row, or a typed ball and kind, lights the ball on the pans and tilts them
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, ltr } = dvqExplorers.lib;
  const NB = " ";

  // The fewest weighings for n balls: the smallest k with (3^k − 3) / 2 >= n.
  const obMinK = (n) => { let k = 2; while ((3 ** k - 3) / 2 < n) k++; return k; };

  // The codes of part b for 12 balls: +1 on the left pan, −1 on the right pan, 0 off the scale.
  const OB_CODES12 = [[1, 1, 0], [1, 0, 1], [1, -1, 0], [1, 1, -1], [-1, 0, 0], [-1, -1, -1],
                      [-1, 0, 1], [-1, 1, 1], [0, 1, 0], [0, -1, 1], [0, -1, -1], [0, 0, -1]];

  // The codes of part c (the page's find_odd_ball): the correct codes of length k whose
  // first digit is 1, in lexicographic order, each with its orbit c + 1, c + 2, c (first
  // digits +1, −1, 0); the last orbit trimmed when 3 does not divide n.
  const obDyson = (n) => {
    const k = obMinK(n), codes = [];
    const correct = (c) => {
      for (let i = 0; i + 1 < k; i++) if (c[i] !== c[i + 1]) return ((c[i + 1] - c[i]) % 3 + 3) % 3 === 1;
      return false;
    };
    const q = Math.ceil(n / 3), extra = (3 - (n % 3)) % 3;
    for (let v = 0; v < 3 ** (k - 1) && codes.length < 3 * q; v++) {
      const c = [1];
      for (let j = k - 1, m = v; j >= 1; j--, m = Math.floor(m / 3)) c[j] = m % 3;
      if (!correct(c)) continue;
      [1, 2, 0].forEach((s) => codes.push(c.map((d) => ((d + s) % 3) - 1)));
    }
    if (extra === 1) codes.pop();
    else if (extra === 2) codes.splice(codes.length - 3, 2);
    return codes;
  };

  // The box shows part b's table for 12 balls and part c's construction for every other n.
  const obCodes = (n) => (n === 12 ? { k: 3, codes: OB_CODES12, from: "b" } : { k: obMinK(n), codes: obDyson(n), from: "c" });

  // The pans of every weighing, as the page's code builds them: from weighing 2 on, a pan
  // that holds more balls loses a genuine ball, or the other pan gets one from outside
  // (genuine: on the scale when weighing 1 balanced, off it when weighing 1 tipped).
  // Balls are numbered from 1; moved lists the genuine balls taken off or put on.
  const obPans = (codes, k, out0) => {
    const pans = [];
    for (let j = 0; j < k; j++) {
      const L = [], R = [], moved = [];
      codes.forEach((c, b) => { if (c[j] === 1) L.push(b + 1); else if (c[j] === -1) R.push(b + 1); });
      if (j > 0) {
        codes.forEach((c, b) => {
          if (L.length === R.length || c[0] === out0 || c[0] === -out0) return;   // not known genuine
          const [big, small] = L.length > R.length ? [L, R] : [R, L], g = b + 1;
          if (big.includes(g)) { big.splice(big.indexOf(g), 1); moved.push({ ball: g, to: "off" }); }
          else if (!small.includes(g)) { small.push(g); moved.push({ ball: g, to: small === L ? "left" : "right" }); }
        });
      }
      pans.push({ L, R, moved });
    }
    return pans;
  };

  // A scenario: the odd ball (or none) and whether it is heavy, weighed on the pans above;
  // the outcome of each weighing is +1 (left heavier), −1 (right heavier) or 0.
  const obWeigh = (codes, k, ball, heavy) => {
    const w = (b) => (b === ball ? (heavy ? 11 : 9) : 10);
    const out = [], pans = [];
    for (let j = 0; j < k; j++) {
      const p = obPans(codes, k, j ? out[0] : 0)[j];
      const l = p.L.reduce((s, b) => s + w(b), 0), r = p.R.reduce((s, b) => s + w(b), 0);
      out.push(l > r ? 1 : r > l ? -1 : 0);
      pans.push(p);
    }
    return { out, pans };
  };

  // The decision: the ball whose code is the outcome (heavy) or its negation (light).
  const obDecode = (codes, out) => {
    for (let b = 0; b < codes.length; b++) {
      if (codes[b].every((v, j) => v === out[j])) return { ball: b + 1, heavy: true };
      if (codes[b].every((v, j) => v === -out[j])) return { ball: b + 1, heavy: false };
    }
    return null;
  };

  // Every outcome vector, sorted by weighing 1, then 2, … with L before = before R, and the
  // ball and kind it names (null for the vectors no ball gives).
  const OB_ORDER = [1, 0, -1];
  const obRows = (codes, k) => {
    const rows = [];
    for (let v = 0; v < 3 ** k; v++) {
      const out = [];
      for (let j = k - 1, m = v; j >= 0; j--, m = Math.floor(m / 3)) out[j] = OB_ORDER[m % 3];
      rows.push({ out, who: obDecode(codes, out) });
    }
    return rows;
  };

  const SIGN = { 1: "L", 0: "=", "-1": "R" };
  const WORD = { 1: "הכף השמאלית כבדה", 0: "מאוזן", "-1": "הכף הימנית כבדה" };

  // The box: n balls; the weighings as rows of balances (the pans of the chosen scenario,
  // tilted by its outcome, the odd ball red when heavy and blue when light, genuine balls
  // moved to even the pans dashed), and the decision table, a row per outcome vector; a
  // tap on a row or the ball and kind fields choose the scenario.
  const NMIN = 3, NMAX = 39;
  const oddballView = () => ({
    mount(box) {
      const fixed = "fixed" in box.dataset;
      const N0 = Math.min(NMAX, Math.max(NMIN, Number(box.dataset.n || 12)));
      const st = { n: N0, ball: Number(box.dataset.ball || (N0 === 12 ? 11 : 1)), heavy: box.dataset.heavy === "1", none: false };
      box.innerHTML =
        `<div class="ex-controls"><label${fixed ? " hidden" : ""}><span>מספר הכדורים ${ltr("N")}</span><input type="range" class="ob-n" min="${NMIN}" max="${NMAX}" step="1" value="${N0}" dir="ltr" aria-label="מספר הכדורים, מ-${NMIN} עד ${NMAX}"><output class="ob-out-n">${N0}</output></label>` +
        `<label>הכדור החריג <input type="number" class="ex-num ob-ball" min="1" max="${N0}" step="1" value="${st.ball}" dir="ltr" aria-label="מספר הכדור החריג"></label>` +
        `<label><select class="ob-kind" aria-label="כבד או קל"><option value="heavy">כבד</option><option value="light">קל</option></select></label>` +
        `<button type="button" class="md-button ob-none">בלי כדור חריג</button></div>` +
        `<p class="ex-summary ob-sum" aria-live="polite"></p>` +
        `<span class="viz-legend"><span><i class="ob-key-normal"></i>כדור רגיל</span><span><i class="ob-key-heavy"></i>החריג, כבד</span><span><i class="ob-key-light"></i>החריג, קל</span><span><i class="ob-key-helper"></i>כדור תקין שהועבר כדי לאזן</span></span>` +
        `<div class="ob-scales"></div>` +
        `<p class="ex-title ob-table-title"></p><div class="ob-table at-scroll" tabindex="0"></div>`;
      const $ = (sel) => box.querySelector(sel);
      $(".ob-kind").value = st.heavy ? "heavy" : "light";

      // one balance: the beam tilted by the outcome, the balls in rows on each pan, and the
      // balls off the scale in rows under it; a narrow box (a phone) gets a narrower drawing
      // with fewer balls per row, so the balls keep their size
      const R = 15, STEP = 33, BEAM = 104, TILT = 0.12;
      const geom = () => (box.clientWidth && box.clientWidth < 520
        ? { W: 400, per: 4, offPer: 10, left: 100, right: 300 }
        : { W: 640, per: 7, offPer: 13, left: 170, right: 470 });
      const ballSvg = (b, x, y, cls, title) =>
        `<g class="ob-ball ${cls}"><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${R}"><title>${title}</title></circle>` +
        `<text class="ob-num" x="${x.toFixed(1)}" y="${(y + 5).toFixed(1)}" text-anchor="middle">${b}</text></g>`;
      const balance = (j, p, out, scen) => {
        const g = geom(), PIVOT = g.W / 2, tilt = out * TILT;    // left heavier: the left end goes down
        const beamY = (x) => BEAM + (PIVOT - x) * tilt;
        const cls = (b) => (scen && b === scen.ball ? (scen.heavy ? "is-heavy" : "is-light") : "");
        const helper = new Set(p.moved.filter((m) => m.to !== "off").map((m) => m.ball));
        const removed = new Set(p.moved.filter((m) => m.to === "off").map((m) => m.ball));
        const off = [];
        for (let b = 1; b <= st.n; b++) if (!p.L.includes(b) && !p.R.includes(b)) off.push(b);
        const rows = Math.max(1, Math.ceil(p.L.length / g.per), Math.ceil(p.R.length / g.per));
        const top = 8 + (rows - 1) * STEP;
        const pan = (balls, cx) => balls.map((b, i) => {
          const row = Math.floor(i / g.per), inRow = Math.min(g.per, balls.length - row * g.per), x = cx + (i % g.per - (inRow - 1) / 2) * STEP;
          return ballSvg(b, x, beamY(x) - R - 3 - row * STEP, `${cls(b)}${helper.has(b) ? " is-helper" : ""}`,
            `כדור ${b}${helper.has(b) ? " : כדור תקין שנוסף כדי לאזן" : ""}`);
        }).join("");
        const offRows = Math.ceil(off.length / g.offPer);
        const offBall = (b, i) => {
          const row = Math.floor(i / g.offPer), inRow = Math.min(g.offPer, off.length - row * g.offPer);
          const x = PIVOT + (i % g.offPer - (inRow - 1) / 2) * STEP, y = BEAM + 72 + row * STEP;
          return ballSvg(b, x, y, `${cls(b)}${removed.has(b) ? " is-helper" : ""}`, `כדור ${b}, מחוץ למאזניים${removed.has(b) ? " : כדור תקין שהוצא כדי לאזן" : ""}`);
        };
        const H = top + BEAM + 72 + (Math.max(offRows, 1) - 1) * STEP + R + 8;
        const end = g.W - 70;
        return `<svg class="figure ob-svg" viewBox="0 0 ${g.W} ${H.toFixed(0)}" role="img" aria-label="שקילה ${j + 1} : ${p.L.join(", ") || "אף כדור"} מול ${p.R.join(", ") || "אף כדור"}, ${WORD[out]}">` +
          `<g transform="translate(0 ${top})">` +
          `<path class="ob-stand" d="M${PIVOT - 30},${BEAM + 40} L${PIVOT},${BEAM + 4} L${PIVOT + 30},${BEAM + 40} Z"/>` +
          `<line class="ob-beam" x1="70" y1="${beamY(70).toFixed(1)}" x2="${end}" y2="${beamY(end).toFixed(1)}"/>` +
          pan(p.L, g.left) + pan(p.R, g.right) +
          (off.length ? `<text class="ob-off-label" x="${g.W - 4}" y="${(BEAM + 50).toFixed(1)}" text-anchor="start" direction="rtl">בחוץ</text>` : "") +
          off.map(offBall).join("") +
          `</g></svg>`;
      };

      const draw = () => {
        const { k, codes, from } = obCodes(st.n);
        st.ball = Math.min(Math.max(1, st.ball), st.n);
        $(".ob-out-n").textContent = String(st.n);
        $(".ob-ball").max = st.n;
        if (document.activeElement !== $(".ob-ball")) $(".ob-ball").value = st.ball;
        $(".ob-kind").value = st.heavy ? "heavy" : "light";
        const scen = st.none ? null : { ball: st.ball, heavy: st.heavy };
        const { out, pans } = obWeigh(codes, k, scen ? scen.ball : 0, scen ? scen.heavy : true);
        const who = obDecode(codes, out);
        const lo = (3 ** (k - 1) - 3) / 2, hi = (3 ** k - 3) / 2;
        $(".ob-sum").innerHTML = `${ltr(`N = ${st.n}`)}${NB}: ‏<b>${k} שקילות</b>, המינימום${NB}: ${k - 1} שקילות מספיקות לכל היותר ל-${ltr(lo)} כדורים, ו-${k} ל-${ltr(hi)}. ` +
          `יש ${ltr(2 * st.n)} מצבים (כל כדור קל או כבד) ו-${ltr(3 ** k)} וקטורים של תוצאות; ${ltr(3 ** k - 2 * st.n)} מהם לא שייכים לאף כדור. ` +
          (from === "b" ? "החלוקה היא הטבלה של סעיף ב." : `החלוקה היא הבנייה של סעיף ג${st.n % 3 ? ", עם כדורים תקינים שמאזנים את הכפות מהשקילה השנייה" : ""}.`);
        $(".ob-scales").innerHTML = pans.map((p, j) =>
          `<div class="ob-row"><div class="ob-tag"><span>שקילה ${j + 1}</span><b dir="ltr">${SIGN[out[j]]}</b><small>${WORD[out[j]]}</small></div>${balance(j, p, out[j], scen)}</div>`).join("");
        // the decision table
        const rows = obRows(codes, k);
        const head = Array.from({ length: k }, (_, j) => `<th>ש${j + 1}</th>`).join("");
        const key = out.join(",");
        $(".ob-table-title").innerHTML = `טבלת ההחלטות${NB}: ${ltr(3 ** k)} וקטורים של תוצאות, ממוינים לפי שקילה 1, אחר כך 2${k > 2 ? " וכן הלאה" : ""}; לחיצה על שורה בוחרת אותה`;
        $(".ob-table").innerHTML = `<table class="ob-decide"><thead><tr>${head}<th>הכדור</th><th>המשקל</th></tr></thead><tbody>` +
          rows.map((r) => `<tr data-out="${r.out.join(",")}" class="${r.out.join(",") === key ? "is-now" : ""}${r.who ? "" : " is-none"}" tabindex="-1">` +
            r.out.map((v, j) => `<td class="ob-o ob-o${v < 0 ? "R" : v > 0 ? "L" : "E"}${j === 0 ? " ob-first" : ""}">${SIGN[v]}</td>`).join("") +
            (r.who ? `<td>${r.who.ball}</td><td class="${r.who.heavy ? "ob-h" : "ob-l"}">${r.who.heavy ? "כבד" : "קל"}</td>`
                   : `<td colspan="2" class="ob-x">אין חריג, או טעות</td>`) + `</tr>`).join("") + `</tbody></table>`;
        const now = $(".ob-table tr.is-now"), wrap = $(".ob-table");
        if (now) {
          const t = now.offsetTop - wrap.clientHeight / 2 + now.offsetHeight / 2;
          wrap.scrollTop = Math.max(0, t);
        }
        const vec = ltr(`(${out.map((v) => SIGN[v]).join(", ")})`);   // weighing 1 first, as a vector
        answer(box, who ? `התוצאות ${vec} : הכדור ${ltr(who.ball)}, ${who.heavy ? "כבד" : "קל"}.`
          : `התוצאות ${vec} : אף כדור לא נותן אותן, כלומר אין כדור חריג או שהייתה טעות בשקילה.`,
          []);                                            // the table row is lit already
      };

      $(".ob-n").addEventListener("input", () => { st.n = Number($(".ob-n").value); draw(); });
      $(".ob-ball").addEventListener("input", () => {
        const v = Number($(".ob-ball").value);
        if (Number.isInteger(v) && v >= 1 && v <= st.n) { st.ball = v; st.none = false; draw(); }
      });
      $(".ob-kind").addEventListener("change", () => { st.heavy = $(".ob-kind").value === "heavy"; st.none = false; draw(); });
      $(".ob-none").addEventListener("click", () => { st.none = true; draw(); });
      const pick = (tr) => {
        const { codes } = obCodes(st.n);
        const who = obDecode(codes, tr.dataset.out.split(",").map(Number));
        if (who) { st.ball = who.ball; st.heavy = who.heavy; st.none = false; }
        else st.none = true;
        draw();
      };
      $(".ob-table").addEventListener("click", (e) => { const tr = e.target.closest("tr[data-out]"); if (tr) pick(tr); });
      $(".ob-table").addEventListener("keydown", (e) => {
        if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
        const now = $(".ob-table tr.is-now") || $(".ob-table tbody tr");
        const next = e.key === "ArrowDown" ? now.nextElementSibling : now.previousElementSibling;
        if (next) { e.preventDefault(); pick(next); }
      });
      draw();
      if ("ResizeObserver" in window) {
        let wasNarrow = geom().W < 640;
        new ResizeObserver(() => { const now = geom().W < 640; if (now !== wasNarrow) { wasNarrow = now; draw(); } }).observe(box);
      }
    },
  });

  dvqExplorers.register({
    views: { oddball: oddballView },
    help: {
      oddball: "בוחרים מספר כדורים : התיבה מחשבת את מספר השקילות המינימלי ומציירת את השקילות הקבועות, שורה של מאזניים לכל שקילה. בוחרים כדור חריג וקל או כבד, או לוחצים על שורה בטבלה (או חיצים למעלה ולמטה כשהטבלה ממוקדת) : הכדור נצבע במאזניים, הכפות נוטות לפי התוצאה, והשורה המתאימה בטבלה מודגשת.",
    },
    models: { obMinK, obDyson, obCodes, obPans, obWeigh, obDecode, obRows, OB_CODES12 },
  });
})();
