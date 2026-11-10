// kinds: probability
//   probability            0015        p, q and C: the answer, the two-children square and the curve against q
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { f, fmt, frame, hline, ltr } = dvqExplorers.lib;
  const NB = "\u00a0";

  // Probability (0015): P(all C children are boys | at least one is a boy with the trait).
  const probabilityAnswer = (C, p, q) => (Math.pow(p, C) * (1 - Math.pow(1 - q, C))) / (1 - Math.pow(1 - p * q, C));

  // The probability box (0015): p, q and the number of children move the answer; for two
  // children an area-proportional grid of the four kinds of child, and a curve of the
  // answer against q for the chosen p and C.
  const probabilityView = () => ({
    mount(box) {
      const QS = [["1", "בלי תכונה (q = 1)"], ["0.5", "הטלת מטבע (q = 1/2)"], ["0.14285714285714285", "יום בשבוע (q = 1/7)"],
                  ["0.08333333333333333", "חודש בשנה (q = 1/12)", ], ["0.0027397260273972603", "יום בשנה (q = 1/365)"]];
      const defaults = { p: Number(box.dataset.p || 0.5), q: QS[2][0], C: Number(box.dataset.c || 2) };
      const st = { ...defaults };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>ההסתברות לבן p</span><input type="range" class="ex-p" min="0.05" max="0.95" step="0.05" value="${st.p}" dir="ltr"><output class="out-p"></output></label>` +
        `<label>התכונה <select class="ex-q">${QS.map(([v, n]) => `<option value="${v}"${v === st.q ? " selected" : ""}>${n}</option>`).join("")}</select></label>` +
        `<label><span>מספר הילדים C</span><input type="range" class="ex-C" min="1" max="6" step="1" value="${st.C}" dir="ltr"><output class="out-C"></output></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p><div class="prob-box"><div class="prob-grid"></div><div class="prob-chart"></div></div>`;
      const $ = (sel) => box.querySelector(sel);
      // A trait band thinner than MIN px (a rare trait: 1/365 of 240 px is under a pixel) is
      // drawn MIN px wide, taken from the other band of the same sex, so the cross of the
      // condition stays visible; the title then says so. The boys' total width stays p · S.
      const MIN = 5;
      const KINDS = ["בן עם התכונה", "בן בלי התכונה", "בת עם התכונה", "בת בלי התכונה"];
      const bands = (p, q, S) => {
        const w = [p * q, p * (1 - q), (1 - p) * q, (1 - p) * (1 - q)], px = w.map((v) => v * S);
        let widened = false;
        [0, 2].forEach((i) => { if (px[i] > 0 && px[i] < MIN && px[i] + px[i + 1] >= 2 * MIN) { px[i + 1] -= MIN - px[i]; px[i] = MIN; widened = true; } });
        return { w, px, widened };
      };
      const gridSvg = (p, q) => {
        // child 1 along the rows, child 2 along the columns; four kinds each, with areas
        // proportional to their probabilities (but for a widened trait band)
        const S = 240, x0 = 96, y0 = 30, { w, px } = bands(p, q, S);
        const kinds = KINDS.map((n, i) => [n, w[i], px[i], i < 2, i % 2 === 0]);
        let s = `<svg class="figure prob-live" viewBox="0 0 ${x0 + S + 10} ${y0 + S + 10}" style="max-width:22rem" role="img" aria-label="ריבוע ההסתברות של שני ילדים${NB}: שטח כל משבצת הוא ההסתברות של הזוג">`;
        let cy = y0;
        kinds.forEach(([n1, w1, h1, boy1, tr1]) => {
          let cx = x0 + S;
          kinds.forEach(([n2, w2, cw, boy2, tr2]) => {
            cx -= cw;
            const cond = (boy1 && tr1) || (boy2 && tr2), hit = cond && boy1 && boy2;
            if (cw > 0.2 && h1 > 0.2) s += `<rect class="${hit ? "pg-hit" : cond ? "pg-cond" : "pg-out"}" x="${f(cx)}" y="${f(cy)}" width="${f(cw)}" height="${f(h1)}"><title>${n1} / ${n2}${NB}: ${fmt(w1 * w2, 4)}</title></rect>`;
          });
          if (h1 > 11) s += `<text class="pg-day" x="${x0 - 6}" y="${f(cy + h1 / 2 + 4)}" text-anchor="start" direction="rtl">${n1}</text>`;
          cy += h1;
        });
        let cx = x0 + S;
        kinds.forEach(([n2, , cw]) => { cx -= cw; if (cw > n2.length * 6 + 8) s += `<text class="pg-day" x="${f(cx + cw / 2)}" y="${y0 - 8}" text-anchor="middle" direction="rtl">${n2}</text>`; });
        s += `<rect class="pg-quad" x="${f(x0 + S - p * S)}" y="${y0}" width="${f(p * S)}" height="${f(p * S)}"/>`;
        return s + "</svg>";
      };
      // q on a logarithmic axis from 1/1000 to 1, so that 1/7, 1/12 and 1/365 lie apart
      const LOGQ = 3, SLOTS = 300;
      const curveSvg = (p, C, q) => {
        const fr = frame("התשובה כפונקציה של q, על ציר לוגריתמי", SLOTS, 1, [0, 0.25, 0.5, 0.75, 1]);
        const X = (qq) => fr.cx(0.5 + (SLOTS / LOGQ) * (Math.log10(qq) + LOGQ));
        let s = fr.s;
        const pts = [];
        for (let i = 0; i <= 150; i++) { const qq = Math.pow(10, -LOGQ + (LOGQ * i) / 150); pts.push(`${f(X(qq))},${f(fr.Y(probabilityAnswer(C, p, qq)))}`); }
        s += `<polyline class="s1-line" points="${pts.join(" ")}" fill="none" stroke-width="2.5"/>`;
        s += hline(fr, Math.pow(p, C - 1), `q → 0: p^(C−1) = ${fmt(Math.pow(p, C - 1))}`);
        s += `<circle class="s2-dot" cx="${f(X(q))}" cy="${f(fr.Y(probabilityAnswer(C, p, q)))}" r="6"/>`;
        [[0.001, "1/1000"], [1 / 365, "1/365"], [1 / 12, "1/12"], [1 / 7, "1/7"], [0.5, "1/2"], [1, "1"]].forEach(([v, t]) => {
          s += fr.xtick(0.5 + (SLOTS / LOGQ) * (Math.log10(v) + LOGQ), t);
        });
        return s + fr.close();
      };
      const draw = () => {
        const p = st.p, q = Number(st.q), C = st.C;
        $(".out-p").textContent = String(p); $(".out-C").textContent = String(C);
        const PT = 1 - Math.pow(1 - p * q, C), PAT = Math.pow(p, C) * (1 - Math.pow(1 - q, C)), ans = probabilityAnswer(C, p, q);
        $(".ex-summary").innerHTML = `עם ${ltr(`p = ${p}`)}, ‏${ltr(`q = ${fmt(q, 4)}`)} ו-${ltr(`C = ${C}`)} : ‏${ltr(`P(T) = ${fmt(PT, 4)}`)}, ‏${ltr(`P(A ∩ T) = ${fmt(PAT, 4)}`)}, ` +
          `ולכן ${ltr(`P(A | T) = ${fmt(ans, 4)}`)}. בלי התכונה (${ltr("q = 1")}) התשובה היא ${ltr(fmt(Math.pow(p, C) / (1 - Math.pow(1 - p, C)), 4))}, ` +
          `ועם תכונה נדירה מאוד היא שואפת ל-${ltr(`p^(C−1) = ${fmt(Math.pow(p, C - 1), 4)}`)}.`;
        const thin = bands(p, q, 240).widened ? ` <span class="prob-thin">רצועת התכונה צרה מכדי להיראות, והיא מצוירת רחבה יותר.</span>` : "";
        $(".prob-grid").innerHTML = C === 2 ? `<p class="ex-title">שני ילדים${NB}: שטח כל משבצת הוא ההסתברות של הזוג</p>${gridSvg(p, q)}` +
          `<span class="viz-legend"><span><i class="pg-hit"></i>מקיים את התנאי, ושני הילדים בנים</span><span><i class="pg-cond"></i>מקיים את התנאי, יש גם בת</span><span><i class="pg-out"></i>לא מקיים את התנאי</span>` +
          `<span><i class="pg-quad"></i>שני בנים</span><span>בכל מין, הרצועה הראשונה מלמעלה ומימין היא "עם התכונה".${thin}</span></span>`
          : `<p class="ex-title">הריבוע מצויר רק לשני ילדים; עם ${C} ילדים המספרים בשורה שלמעלה</p>`;
        $(".prob-chart").innerHTML = `<p class="ex-title">התשובה כפונקציה של q על ציר לוגריתמי, עם p ו-C הנבחרים; הנקודה היא q הנבחר</p>${curveSvg(p, C, q)}`;

      };
      $(".ex-p").addEventListener("input", () => { st.p = Number($(".ex-p").value); draw(); });
      $(".ex-C").addEventListener("input", () => { st.C = Number($(".ex-C").value); draw(); });
      $(".ex-q").addEventListener("change", () => { st.q = $(".ex-q").value; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, defaults); $(".ex-p").value = st.p; $(".ex-C").value = st.C; $(".ex-q").value = st.q; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { probability: probabilityView },
    help: {
      probability: "p ו-q הן ההסתברויות ו-C המספר : התיבה מחשבת את התשובה, מציירת את ריבוע שני הילדים ואת העקומה כנגד q.",
    },
    models: { probabilityAnswer },
  });
})();
