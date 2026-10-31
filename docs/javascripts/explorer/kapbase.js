// kinds: kapbase
//   kapbase                0012        three digits in a base from 2 to 16: the chain to the fixed point (even base) or the 2-cycle (odd), each step explained by d = max − min, how many numbers share each d (and so the difference), the map d → max(b − d, d − 1) with the path, the histogram of chain lengths over all b³ numbers
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, H, KB_DIGITS, W, X0, answer, autoplay, f, frame, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Sort the digits and subtract in base b (0012 part c): one step on three digits, the
  // attractor (the fixed point of an even base, the two values of the cycle of an odd
  // one), the chain until the value is in the attractor or 0, and the chain lengths over
  // every number of the base.
  const kbDigits = (x, b) => [Math.floor(x / (b * b)), Math.floor(x / b) % b, x % b];
  const kbText = (x, b) => kbDigits(x, b).map((v) => KB_DIGITS[v]).join("");
  const kbParse = (text, b) => {                     // three digits of the base, or null
    const t = String(text).trim().toUpperCase();
    if (!/^[0-9A-F]{3}$/.test(t)) return null;
    const vals = [...t].map((ch) => KB_DIGITS.indexOf(ch));
    return vals.some((v) => v >= b) ? null : vals[0] * b * b + vals[1] * b + vals[2];
  };
  const kbStep = (x, b) => {
    const sorted = kbDigits(x, b).sort((u, v) => u - v), [lo, mid, hi] = sorted;
    const largest = hi * b * b + mid * b + lo, smallest = lo * b * b + mid * b + hi, diff = largest - smallest, d = hi - lo;
    return { x, largest, smallest, diff, d, dNext: d ? Math.max(b - d, d - 1) : 0, digits: d ? [d - 1, b - 1, b - d] : [0, 0, 0] };
  };
  const kbAttractor = (b) => { const k = Math.floor(b / 2); return b % 2 === 0 ? [k * (b * b - 1)] : [k * (b * b - 1), (k + 1) * (b * b - 1)]; };
  const kbChain = (x, b) => {
    const att = kbAttractor(b), values = [x];
    while (values[values.length - 1] !== 0 && !att.includes(values[values.length - 1]) && values.length < 40) values.push(kbStep(values[values.length - 1], b).diff);
    return values;
  };
  const kbHistogram = (b) => {
    const hist = [];
    let zeros = 0;
    for (let x = 0; x < b * b * b; x++) { const c = kbChain(x, b); const n = c.length - 1; hist[n] = (hist[n] || 0) + 1; if (c[c.length - 1] === 0) zeros++; }
    for (let i = 0; i < hist.length; i++) hist[i] = hist[i] || 0;
    return { hist, zeros };
  };
  // How many of the b³ numbers have each d: F(X) depends only on d, so they all give the
  // same difference (6d(b − d) of them for d ≥ 1, the b numbers with equal digits for d = 0)
  const kbSpreadCounts = (b) => {
    const n = Array(b).fill(0);
    for (let x = 0; x < b * b * b; x++) n[kbStep(x, b).d]++;
    return n;
  };

  // The base-b Kaprekar box (0012 part c): a base from 2 to 16 and three digits typed in
  // that base; the chain played step by step in a table (the sort, the subtraction, the
  // difference in the base and in decimal, d), a line that explains the step by the
  // digits (d − 1, b − 1, b − d) and the move d → max(b − d, d − 1), the map of d with
  // the path of the number, and the histogram of chain lengths over every b³ number.
  const kapbaseView = () => ({
    mount(box) {
      const d0 = box.dataset, B0 = Math.min(16, Math.max(2, Number(d0.b || 7)));
      const X0 = kbParse(d0.x || "610", B0) ?? 0;
      const st = { b: B0, x: X0, step: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>הבסיס b</span><input type="range" class="kb-b" min="2" max="16" step="1" value="${st.b}" dir="ltr" aria-label="הבסיס, מ-2 עד 16"><output class="out-b">${st.b}</output></label>` +
        `<label><span>שלוש ספרות בבסיס</span><input type="text" class="ex-num kb-x" maxlength="3" value="${kbText(st.x, st.b)}" dir="ltr" spellcheck="false" aria-label="שלוש ספרות בבסיס שנבחר, 0 עד 9 ו-A עד F"></label>` +
        `<span class="kb-dec"></span>` +
        `<button type="button" class="md-button ex-random">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err kb-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1000, 400) +
        `<button type="button" class="md-button ex-start">מההתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button><span class="ex-pos"></span></div>` +
        `<p class="ex-summary kb-sum" aria-live="polite"></p><p class="kb-step"></p>` +
        `<p class="ex-title">המפה של d : מכל d חץ ל-max(b − d, d − 1), והמסלול של המספר מודגש</p><div class="kb-map"></div>` +
        `<span class="viz-legend"><span><i class="kb-key-arrow"></i>חץ מ-d ל-d'</span><span><i class="kb-key-fixed"></i>היעד : נקודת שבת או מחזור</span><span><i class="kb-key-path"></i>המסלול של המספר</span></span>` +
        `<p class="ex-title kb-hist-title"></p><div class="kb-chart"></div>` +
        `<div class="kp-table kb-table"></div>`;     // last: the table grows a row a step
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), input = $(".kb-x");
      let H = null, Hb = 0, Nd = null;
      const chainOf = () => kbChain(st.x, st.b);
      const draw = () => {
        const b = st.b, chain = chainOf(), att = kbAttractor(b), total = chain.length - 1;
        if (Hb !== b) { H = kbHistogram(b); Nd = kbSpreadCounts(b); Hb = b; }
        // the key fact: every number with this d gives this same difference
        const same = (sp) => ` כל ${ltr(Nd[sp.d])} המספרים עם ${ltr(`d = ${sp.d}`)} נותנים אותו הפרש ${ltr(sp.diff)}.`;
        st.step = Math.min(st.step, total);
        const done = st.step === total;
        $(".out-b").textContent = String(b);
        if (document.activeElement !== input) input.value = kbText(st.x, b);
        $(".kb-dec").innerHTML = `= ${ltr(st.x)} בעשרוני`;
        $(".ex-pos").textContent = `צעד ${st.step} מתוך ${total}`;
        $(".ex-prev").disabled = st.step === 0; $(".ex-next").disabled = done; $(".ex-end").disabled = done;
        const attText = att.map((v) => kbText(v, b));
        $(".kb-sum").innerHTML = `בסיס ${ltr(b)} : ` + (b % 2 === 0
          ? `נקודת שבת יחידה <b>${ltr(attText[0])}</b> (‏${ltr(att[0])} בעשרוני, d = ${ltr(b / 2)}).`
          : `אין נקודת שבת; המחזור <b>${ltr(attText[0])} ↔ ${ltr(attText[1])}</b> (‏${ltr(att[0])} ↔ ${ltr(att[1])} בעשרוני, d = ${ltr(Math.floor(b / 2))} ↔ ${ltr(Math.floor(b / 2) + 1)}).`) +
          ` המספר ${ltr(kbText(st.x, b))} ` + (total === 0 ? (st.x === 0 || att.includes(st.x) ? `כבר ביעד.` : "") : `מגיע ליעד אחרי ${ltr(total)} ${total === 1 ? "צעד" : "צעדים"} : ${ltr(chain.map((v) => kbText(v, b)).join(" → "))}.`);
        // the table of the steps so far
        let rows = "";
        for (let i = 0; i < Math.max(st.step, 0); i++) {
          const sp = kbStep(chain[i], b);
          rows += `<tr${i === st.step - 1 ? ' class="is-last"' : ""}><td>${ltr(i + 1)}</td><td>${ltr(kbText(sp.x, b))} (${ltr(sp.x)})</td><td>${ltr(kbText(sp.largest, b))}</td><td>${ltr(kbText(sp.smallest, b))}</td><td class="kb-diff">${ltr(`${sp.largest} − ${sp.smallest} = ${sp.diff} = <b>${kbText(sp.diff, b)}</b>`)}</td><td>${ltr(sp.d)}</td><td>${ltr(sp.dNext)}</td></tr>`;
        }
        $(".kb-table").innerHTML = st.step ? `<table tabindex="0" aria-label="צעדי המיון והחיסור בבסיס"><thead><tr><th>צעד</th><th>X</th><th>מהגדול לקטן</th><th>מהקטן לגדול</th><th>ההפרש</th><th>d</th><th>d הבא</th></tr></thead><tbody>${rows}</tbody></table>` : `<p class="ex-note">עוד לא נעשה צעד. ״הצעד הבא״ ממיין ומחסר.</p>`;
        let text;
        if (st.step === 0) {
          const sp = kbStep(st.x, b);
          text = (sp.d === 0 ? `כל הספרות שוות, ולכן d = 0 וההפרש יהיה 0.` : `הספרה הגדולה פחות הקטנה : d = ${ltr(sp.d)}. ההפרש יהיה ${ltr(`d · (b² − 1) = ${sp.d} · ${b * b - 1} = ${sp.diff}`)}, עם הספרות ${ltr(`(d − 1, b − 1, b − d) = (${sp.digits.map((v) => KB_DIGITS[v]).join(", ")})`)}.`) + same(sp);
        } else {
          const sp = kbStep(chain[st.step - 1], b);
          text = `צעד ${ltr(st.step)} : ‏d = ${ltr(sp.d)}, ולכן ${ltr(`F(X) = ${sp.d} · ${b * b - 1} = ${sp.diff}`)} = ${ltr(kbText(sp.diff, b))}, הספרות ${ltr(`(d − 1, b − 1, b − d) = (${sp.digits.map((v) => KB_DIGITS[v]).join(", ")})`)};${same(sp).slice(0, -1)}; ` +
            (sp.d === 0 ? `ההפרש 0 ושם זה נגמר.` : `ה-d הבא הוא ${ltr(`max(b − d, d − 1) = max(${b - sp.d}, ${sp.d - 1}) = ${sp.dNext}`)}.`) +
            (done ? (att.includes(sp.diff) ? ` <b>${ltr(kbText(sp.diff, b))} ${b % 2 === 0 ? "היא נקודת השבת" : "במחזור"}</b>${b % 2 === 0 ? " : הצעד הבא מחזיר אותה לעצמה ✓" : ` : הצעד הבא נותן ${ltr(kbText(kbStep(sp.diff, b).diff, b))}, ואז שוב ${ltr(kbText(sp.diff, b))} ✓`}` : "") : "");
        }
        $(".kb-step").innerHTML = text;
        const end = chain[total];
        answer(box, done && total > 0 ? `${ltr(kbText(st.x, b))} מגיע אחרי ${ltr(total)} ${total === 1 ? "צעד" : "צעדים"} ל-<b>${ltr(kbText(end, b))}</b>` +
          (end === 0 ? " (כל הספרות שוות)." : b % 2 === 0 ? ", נקודת השבת של בסיס " + ltr(b) + "." : `, שבמחזור ${ltr(attText[0])} ↔ ${ltr(attText[1])}.`) : null,
          ".kb-table tr.is-last");
        // the map of d with the path so far
        const W = 420, Hh = 150, X0 = 22, X1 = 398, YA = 90, X = (d) =>   // 420 wide: readable at phone width
           (b > 2 ? X0 + ((d - 1) * (X1 - X0)) / (b - 2) : (X0 + X1) / 2);
        const attD = att.map((v) => Math.floor(v / (b * b - 1)));
        const path = new Set();
        for (let i = 0; i < st.step; i++) { const sp = kbStep(chain[i], b); if (sp.d) path.add(`${sp.d}>${sp.dNext}`); }
        let m = `<svg class="figure kb-map kb-live" viewBox="0 0 ${W} ${Hh}" role="img" aria-label="המפה של d בבסיס ${b} עם המסלול של המספר"><line class="kb-axis" x1="${X0}" x2="${X1}" y1="${YA}" y2="${YA}"/>`;
        for (let d = 1; d < b; d++) {
          const nd = Math.max(b - d, d - 1);
          m += `<text class="kb-tick" x="${f(X(d))}" y="${YA + 18}" text-anchor="middle">${d}</text>`;
          if (nd === d) continue;
          const up = nd > d, xa = X(d), xb = X(nd), bulge = up ? YA - 12 - 7 * Math.abs(nd - d) : YA + 26 + 7 * Math.abs(nd - d), y = up ? YA - 4 : YA + 4;
          const cls = "kb-arrow" + (path.has(`${d}>${nd}`) ? " is-path" : "") + (attD.includes(d) && attD.includes(nd) ? " is-cycle" : "");
          m += `<path class="${cls}" d="M ${f(xa)} ${y} Q ${f((xa + xb) / 2)} ${f(bulge)} ${f(xb)} ${y}"/><circle class="${cls}" cx="${f(xb)}" cy="${y}" r="2.6"/>`;
        }
        attD.forEach((d) => { m += `<circle class="kb-fixed" cx="${f(X(d))}" cy="${YA}" r="7"><title>d = ${d}</title></circle>`; });
        const cur = kbStep(chain[st.step], b).d;
        if (cur) m += `<circle class="kb-cur" cx="${f(X(cur))}" cy="${YA}" r="10"><title>d של המספר הנוכחי = ${cur}</title></circle>`;
        $(".kb-map").innerHTML = m + "</svg>";
        // the histogram of chain lengths over every number of the base
        const n = H.hist.length, ymax = Math.max(...H.hist), stepT = ymax > 2000 ? 500 : ymax > 400 ? 100 : ymax > 80 ? 20 : 5, ticks = [];
        for (let v = 0; v <= ymax + stepT - 1; v += stepT) ticks.push(v);
        const fr = frame("התפלגות מספר הצעדים עד היעד", n, ticks[ticks.length - 1], ticks, (v) => String(v));
        let sv = fr.s;
        H.hist.forEach((v, k) => {
          const bw = Math.max(fr.slot * 0.6, 1), cls = k === total ? "by-enum" : "by-multiples";
          sv += `<rect class="bar ${cls}" x="${f(fr.cx(k + 1) - bw / 2)}" y="${f(fr.Y(v))}" width="${f(bw)}" height="${f(BASE - fr.Y(v))}"><title>${k} צעדים : ${v} מספרים</title></rect>` +
            `<text class="tick" x="${f(fr.cx(k + 1))}" y="${f(fr.Y(v) - 4)}" text-anchor="middle" font-size="10">${v}</text>` + fr.xtick(k + 1, k);
        });
        $(".kb-chart").innerHTML = sv + fr.close();
        $(".kb-hist-title").textContent = `מספר הצעדים עד היעד על כל ${b * b * b} המספרים של בסיס ${b}; הארוך ביותר ${n - 1}, ו-${H.zeros} מספרים עם ספרות שוות נופלים ל-0`;
      };
      let stop = () => {};
      const setX = (x) => { stop(); st.x = x; st.step = 0; draw(); };
      $(".kb-b").addEventListener("input", () => {
        stop(); const b = Number($(".kb-b").value);
        const vals = kbDigits(st.x, st.b).map((v) => Math.min(v, b - 1));            // the same digits, clipped to the new base
        st.b = b; st.x = vals[0] * b * b + vals[1] * b + vals[2]; st.step = 0; $(".kb-err").textContent = ""; draw();
      });
      input.addEventListener("change", () => { const x = kbParse(input.value, st.b); $(".kb-err").textContent = x === null ? `שלוש ספרות מ-0 עד ${KB_DIGITS[st.b - 1]}` : ""; if (x !== null) setX(x); else input.value = kbText(st.x, st.b); });
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      const seed = seedControls(box, $(".ex-random"), (rng) => setX(Math.floor(rng() * st.b * st.b * st.b)));
      $(".ex-random").addEventListener("click", () => seed.draw());
      if (d0.fixed !== undefined) $(".kb-b").closest("label").hidden = true;   // data-fixed: the base stays b (0012 part b)
      $(".ex-reset").addEventListener("click", () => { stop(); st.b = B0; st.x = X0; st.step = 0; $(".kb-b").value = B0; $(".kb-err").textContent = ""; draw(); });
      $(".ex-next").addEventListener("click", () => { stop(); if (st.step < chainOf().length - 1) { st.step++; draw(); } });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.step > 0) { st.step--; draw(); } });
      $(".ex-start").addEventListener("click", () => { stop(); st.step = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.step = chainOf().length - 1; draw(); });
      stop = autoplay(play, speed, { step: () => { st.step++; draw(); }, done: () => st.step >= chainOf().length - 1, restart: () => { st.step = 0; draw(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { kapbase: kapbaseView },
    help: {
      kapbase: "בוחרים בסיס ומקלידים שלוש ספרות בו : ״הצעד הבא״ ו״הפעלה״ ממיינים ומחסרים צעד אחרי צעד, הטבלה מראה את ההפרש בבסיס ובעשרוני, השורה מתחת מסבירה את הספרות (d − 1, b − 1, b − d), כמה מספרים חולקים את אותו d ולכן את אותו הפרש, ואת המעבר d → max(b − d, d − 1), המפה מראה את המסלול, וההיסטוגרמה סופרת את הצעדים של כל מספרי הבסיס.",
    },
    models: { kbDigits, kbText, kbParse, kbStep, kbAttractor, kbChain, kbHistogram, kbSpreadCounts },
  });
})();
