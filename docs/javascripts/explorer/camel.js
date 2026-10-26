// kinds: camel
//   camel                  0042        a, c, w and T (or the page's numbers with data-fixed): the passes played one at a time on a distance axis with the camel, the litres on it and the depots; the chart of the distance against the water with the logarithmic approximation; a toggle for the price list under the road
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, H, TOP, W, X0, autoplay, f, ltr, speedSel } = dvqExplorers.lib;

  // The camel and the water (0042): the levels of the water in motion (w, the multiples
  // of c between T and w, T), the segments at the price (2j - 1) a per km, the closed
  // form for T <= c, the logarithmic approximation of the bonus, and the passes played
  // one by one (full loads first, the partial load last).
  const camelLevels = (c, w, T) => { const k = Math.ceil(w / c), out = [w]; for (let j = k - 1; j >= 1; j--) if (j * c > T) out.push(j * c); out.push(T); return out; };
  const camelSegments = (a, c, w, T) => {
    const lv = camelLevels(c, w, T), out = [];
    let x = 0;
    for (let i = 0; i + 1 < lv.length; i++) {
      const j = Math.ceil(lv[i] / c), x1 = x + (lv[i] - lv[i + 1]) / ((2 * j - 1) * a);
      out.push({ x0: x, x1, loads: j, n0: lv[i], n1: lv[i + 1] });
      x = x1;
    }
    return out;
  };
  const camelDistance = (a, c, w, T) => { const k = Math.ceil(w / c); let s = 0; for (let j = 1; j < k; j++) s += 1 / (2 * j - 1); return (c * s + (w - (k - 1) * c) / (2 * k - 1) - T) / a; };
  const CAMEL_CONST = 2 * Math.log(2) + 0.5772156649015329;        // 2 ln 2 + gamma, the "1.96"
  const camelApprox = (a, c, w, T) => (c / (2 * a)) * (Math.log(w / c) + CAMEL_CONST) - T / a;
  const camelPasses = (a, c, w, T) => {
    const segs = camelSegments(a, c, w, T), depots = [w].concat(segs.map(() => 0)), out = [];
    segs.forEach((sg, s) => {
      const cost = a * (sg.x1 - sg.x0);
      for (let i = 0; i < sg.loads; i++) {
        const take = Math.min(c, depots[s]), keep = i === sg.loads - 1 ? 0 : cost;
        depots[s] -= take; depots[s + 1] += take - cost - keep;
        out.push({ seg: s, back: false, carry0: take, carry1: take - cost, drop: take - cost - keep, depots: depots.slice() });
        if (keep > 0) out.push({ seg: s, back: true, carry0: keep, carry1: 0, drop: 0, depots: depots.slice() });
      }
    });
    return out;
  };

  // The price list of the solution: how many times the camel has crossed each stretch
  // after `step` passes, out of 2j − 1 for a stretch with j loads (so a km there costs
  // (2j − 1) a litres).
  const camelCrossings = (segs, passes, step) => {
    const done = segs.map(() => 0);
    passes.slice(0, step).forEach((p) => { done[p.seg] += 1; });
    return segs.map((sg, i) => ({ done: done[i], total: 2 * sg.loads - 1 }));
  };

  // The camel box (0042): the page's numbers (data-fixed) or a, c, w and T to set; the
  // passes played one at a time on a distance axis with the camel, the litres on it and
  // the depots at the start, at every stop and at the end; the general box adds the
  // chart of the distance against the water with the logarithmic approximation.
  const camelView = () => ({
    mount(box) {
      const d = box.dataset, fixed = d.fixed === "1", LOADS = 10;
      const A0 = Number(d.a || 0.5), C0 = Number(d.c || 150), W0 = Number(d.w || 450), T0 = Number(d.t || 30);
      const st = { a: A0, c: C0, w: W0, T: T0, step: 0, segs: [], passes: [], d: 0 };
      const lit = (v) => (Math.abs(v - Math.round(v)) < 1e-9 ? String(Math.round(v)) : f(v, 1));
      box.innerHTML =
        (fixed ? "" :
          `<div class="ex-controls">` +
          `<label><span>צריכה a (ליטר לק"מ)</span><input type="range" class="cm-a" min="0.2" max="1" step="0.1" value="${st.a}" dir="ltr" aria-label="הצריכה בליטר לקילומטר"><output class="out-a">${st.a}</output></label>` +
          `<label><span>קיבולת c (ליטר)</span><input type="range" class="cm-c" min="100" max="300" step="10" value="${st.c}" dir="ltr" aria-label="הקיבולת בליטר"><output class="out-c">${st.c}</output></label>` +
          `<label><span>מים בהתחלה w</span><input type="number" class="ex-num cm-w" min="0" max="${LOADS * 300}" step="10" value="${st.w}" dir="ltr" inputmode="numeric" aria-label="המים בהתחלה בליטר, יותר מהיעד ועד עשרה מטענים"></label>` +
          `<label><span>ליעד T</span><input type="number" class="ex-num cm-t" min="0" max="300" step="10" value="${st.T}" dir="ltr" inputmode="numeric" aria-label="המים שצריכים להגיע, עד מטען אחד"></label>` +
          `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err cm-err"></span></div>`) +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">המעבר הבא</button>` +
        `<button type="button" class="md-button ex-prev">המעבר הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1600, 900, 350) +
        `<button type="button" class="md-button ex-start">מההתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button><span class="ex-pos"></span>` +
        `<label><input type="checkbox" class="cm-price" checked> המחירון על הדרך</label></div>` +
        `<p class="ex-summary cm-sum" aria-live="polite"></p><p class="cm-step"></p><p class="ex-note cm-price-text"></p>` +
        `<span class="viz-legend"><span><i class="cm-key-depot"></i>מחסן : הליטרים שבו מעל הציר</span><span><i class="cm-key-camel"></i>הגמל והליטרים שעליו</span><span><i class="cm-key-pass"></i>המעבר האחרון : ליטרים ביציאה ← בהגעה</span><span><i class="cm-key-next"></i>המעבר הבא</span></span>` +
        `<div class="cm-road"></div>` +
        (fixed ? "" : `<p class="ex-title">המרחק המקסימלי לפי כמות המים בהתחלה, עם הקירוב הלוגריתמי מקווקו</p><div class="cm-chart"></div>`);
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const compute = () => {
        st.segs = camelSegments(st.a, st.c, st.w, st.T);
        st.passes = camelPasses(st.a, st.c, st.w, st.T);
        st.d = st.segs.length ? st.segs[st.segs.length - 1].x1 : 0;
        st.step = Math.min(st.step, st.passes.length);
      };
      // the state after `step` passes: where the camel is, what it carries, the depots
      const after = (step) => {
        if (step === 0) return { pos: 0, carry: 0, depots: [st.w].concat(st.segs.map(() => 0)), last: null };
        const p = st.passes[step - 1], sg = st.segs[p.seg];
        return { pos: p.back ? sg.x0 : sg.x1, carry: p.back ? 0 : p.carry1 - p.drop, depots: p.depots, last: p };
      };
      const road = (s) => {
        const price = $(".cm-price").checked;
        const W = 480, H = price ? 236 : 200, X0 = 28, X1 = 452, YA = 110, BAR = 76, dmax = Math.max(st.d, 1e-9);   // 480 wide: readable at phone width
        const X = (x) => X0 + (x / dmax) * (X1 - X0);
        const pts = [0].concat(st.segs.map((sg) => sg.x1));
        let h = `<svg class="figure cm-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="ציר הדרך מ-0 עד ${lit(st.d)} ק״מ : המחסנים עם הליטרים שבהם, הגמל במקומו ומה שעליו, והמעבר האחרון">` +
          `<line class="cm-axis" x1="${X0}" x2="${X1}" y1="${YA}" y2="${YA}"/>`;
        let lastLabel = -1e9, lastLitres = -1e9, lift = 0;
        const camelX = X(s.pos);                                       // no km label under the camel
        pts.forEach((x, i) => {
          const v = s.depots[i], hb = st.w > 0 ? (Math.max(0, v) / st.w) * BAR : 0, xx = X(x);
          h += `<line class="cm-stop" x1="${f(xx)}" x2="${f(xx)}" y1="${YA - 6}" y2="${YA + 6}"/>`;
          if (v > 1e-9) {
            lift = xx - lastLitres < 34 ? (lift + 1) % 3 : 0;            // crowded depots: the litres stacked in three rows
            lastLitres = xx;
            h += `<rect class="cm-depot" x="${f(xx - 6)}" y="${f(YA - hb)}" width="12" height="${f(hb)}" rx="2"><title>מחסן ב-${lit(x)} ק״מ : ${lit(v)} ליטר</title></rect>` +
              `<text class="cm-litres" x="${f(xx)}" y="${f(YA - hb - 5 - 12 * lift)}" text-anchor="middle">${lit(v)}</text>`;
          }
          if ((xx - lastLabel >= 28 || i === pts.length - 1) && Math.abs(xx - camelX) >= 14) { h += `<text class="cm-km" x="${f(xx)}" y="${YA + 19}" text-anchor="middle">${lit(x)}</text>`; lastLabel = xx; }
        });
        const arrow = (p, cls, y) => {
          const sg = st.segs[p.seg], xa = X(p.back ? sg.x1 : sg.x0), xb = X(p.back ? sg.x0 : sg.x1), dir = xb >= xa ? 1 : -1;
          const tip = Math.abs(xb - xa) > 8 ? xb - dir * 8 : xa;
          return `<line class="cm-pass ${cls}" x1="${f(xa)}" x2="${f(tip)}" y1="${y}" y2="${y}"/>` +
            `<path class="cm-pass-head ${cls}" d="M ${f(xb)} ${y} l ${-dir * 9} -5 v 10 z"/>` +
            `<text class="cm-pass-lbl ${cls}" x="${f((xa + xb) / 2)}" y="${y + 15}" text-anchor="middle">${lit(p.carry0)} → ${lit(p.carry1)}</text>`;
        };
        if (s.last) h += arrow(s.last, "is-last", YA + 44);
        if (st.step < st.passes.length) h += arrow(st.passes[st.step], "is-next", YA + 70);
        if (price) {
          // under the road: every stretch with its crossings so far out of 2j − 1, and the price per km
          const cross = camelCrossings(st.segs, st.passes, st.step), y = H - 24;
          st.segs.forEach((sg, i) => {
            const xa = X(sg.x0), xb = X(sg.x1), cx = (xa + xb) / 2, c = cross[i], full = c.done === c.total;
            h += `<line class="cm-band${full ? " is-full" : ""}" x1="${f(xa + 2)}" x2="${f(xb - 2)}" y1="${y}" y2="${y}"><title>קטע ${i + 1} : ${c.done} מתוך ${c.total} מעברים, ${lit(c.total * st.a)} ליטר לק״מ</title></line>`;
            // a phone shows the price per km only; the crossings so far are in the title and the line under the box
            const narrow = box.clientWidth > 0 && box.clientWidth < 520;
            const lbl = narrow ? (xb - xa >= 44 ? `${lit(c.total * st.a)}/km` : "") : xb - xa >= 30 ? `${c.done}/${c.total}${xb - xa >= 62 ? ` · ${lit(c.total * st.a)}/km` : ""}` : "";
            if (lbl) h += `<text class="cm-price-lbl" x="${f(cx)}" y="${y + 15}" text-anchor="middle">${lbl}</text>`;
          });
        }
        const xc = X(s.pos);
        h += `<text class="cm-camel" x="${f(xc)}" y="${YA + 36}" text-anchor="middle">🐪</text>` +
          `<text class="cm-carry" x="${f(xc + (xc > X0 + 60 ? -36 : 36))}" y="${YA + 34}" text-anchor="middle">💧${lit(s.carry)}</text>`;
        return h + "</svg>";
      };
      const chart = () => {
        const W = 640, H = 210, X0 = 46, R = 12, TOP = 14, BASE = 180, wmax = LOADS * st.c, wmin = st.T;
        const ws = [];
        for (let i = 0; i <= 160; i++) ws.push(wmin + ((wmax - wmin) * i) / 160);
        for (let j = 1; j <= LOADS; j++) if (j * st.c > wmin) ws.push(j * st.c);
        ws.sort((u, v) => u - v);
        const dm = camelDistance(st.a, st.c, wmax, st.T), ymax = dm * 1.08;
        const X = (w) => X0 + ((w - wmin) / (wmax - wmin)) * (W - X0 - R), Y = (v) => BASE - (v / ymax) * (BASE - TOP);
        let h = `<svg class="perf-chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="המרחק המקסימלי לפי המים בהתחלה, מ-${lit(wmin)} עד ${wmax} ליטר, עם הקירוב הלוגריתמי">`;
        const ystep = ymax > 1500 ? 500 : ymax > 600 ? 200 : ymax > 300 ? 100 : 50;
        for (let v = 0; v <= ymax; v += ystep) h += `<line class="grid" x1="${X0}" x2="${W - R}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        [2, 4, 6, 8, 10].forEach((j) => { const w = j * st.c; if (w > wmin) h += `<line class="grid" x1="${f(X(w))}" x2="${f(X(w))}" y1="${TOP}" y2="${BASE}" stroke-dasharray="4 4"/><text class="tick" x="${f(X(w))}" y="${BASE + 16}" text-anchor="middle">${w}</text>`; });
        const ap = ws.filter((w) => w >= st.c).map((w) => `${f(X(w))},${f(Y(Math.max(0, camelApprox(st.a, st.c, w, st.T))))}`).join(" ");
        h += `<polyline class="s1-line" points="${ws.map((w) => `${f(X(w))},${f(Y(camelDistance(st.a, st.c, w, st.T)))}`).join(" ")}" fill="none" stroke-width="2.5"/>`;
        if (ap) h += `<polyline class="ink-line" points="${ap}" fill="none" stroke-width="1.5" stroke-dasharray="6 4"/>`;
        h += `<circle class="s2-dot" cx="${f(X(st.w))}" cy="${f(Y(st.d))}" r="5"><title>${lit(st.w)} ליטר : ${lit(st.d)} ק״מ</title></circle>`;
        return h + `<line class="axis" x1="${X0}" x2="${W - R}" y1="${BASE}" y2="${BASE}"/></svg>`;
      };
      const draw = () => {
        const s = after(st.step), done = st.step === st.passes.length, k = Math.ceil(st.w / st.c), r = st.w - (k - 1) * st.c;
        if (!fixed) { $(".out-a").textContent = String(st.a); $(".out-c").textContent = String(st.c); $(".cm-w").value = st.w; $(".cm-t").value = st.T; $(".cm-t").max = st.c; $(".cm-w").max = LOADS * st.c; }
        $(".cm-road").innerHTML = road(s);
        if (!fixed) $(".cm-chart").innerHTML = chart();
        $(".ex-pos").textContent = `מעבר ${st.step} מתוך ${st.passes.length}`;
        $(".ex-prev").disabled = st.step === 0; $(".ex-next").disabled = done; $(".ex-end").disabled = done;
        const stops = st.segs.slice(0, -1).map((sg) => lit(sg.x1));
        $(".cm-sum").innerHTML = `צריכה ${ltr(st.a)} ליטר לק"מ, קיבולת ${ltr(st.c)}, ${ltr(st.w)} ליטר בהתחלה ו-${ltr(st.T)} ליעד : ${ltr(k)} ${k === 1 ? "מטען" : "מטענים"}` +
          (k > 1 ? ` (העליון ${ltr(lit(r))})` : "") + `, המרחק המקסימלי <b>${ltr(lit(st.d))} ק"מ</b>, ` +
          (stops.length ? `עצירות ב-${ltr(stops.join(", "))}` : "בלי עצירות") + `, ${ltr(st.passes.length)} מעברים. ` +
          `בדיקה : נשרפו ${ltr(lit(st.w - st.T))} והגיעו ${ltr(lit(st.T))}, ביחד ${ltr(lit(st.w))} ✓` +
          (!fixed && st.w >= st.c ? ` הקירוב הלוגריתמי נותן ${ltr(lit(camelApprox(st.a, st.c, st.w, st.T)))}; פי ${ltr("e")} מים (${ltr(lit(Math.E * st.w))} ליטר) היו מוסיפים ${ltr(lit(st.c / (2 * st.a)))} ק"מ.` : "");
        let step;
        if (st.step === 0) step = `לפני המעבר הראשון : ${ltr(lit(st.w))} ליטר במחסן של נקודת ההתחלה, והגמל ריק.` +
          (st.passes.length ? ` המעבר הראשון : לוקח ${ltr(lit(st.passes[0].carry0))} ליטר ל-${ltr(lit(st.segs[0].x1))} ק"מ.` : " אין מה להזיז.");
        else {
          const p = s.last, sg = st.segs[p.seg], L = sg.x1 - sg.x0, cost = st.a * L;
          step = `מעבר ${ltr(st.step)} (קטע ${ltr(p.seg + 1)}, ${p.back ? "חזור" : "הלוך"})  : ` +
            (p.back ? `חוזר מ-${ltr(lit(sg.x1))} ל-${ltr(lit(sg.x0))} עם ${ltr(lit(p.carry0))} ליטר, בדיוק מה ש-${ltr(lit(L))} ק"מ שורפים, ומגיע ריק.`
              : `יוצא מ-${ltr(lit(sg.x0))} עם ${ltr(lit(p.carry0))} ליטר, שורף ${ltr(lit(cost))} ב-${ltr(lit(L))} ק"מ ומגיע ל-${ltr(lit(sg.x1))} עם ${ltr(lit(p.carry1))}; ` +
                (p.carry1 - p.drop > 1e-9 ? `משאיר ${ltr(lit(p.drop))} במחסן ושומר ${ltr(lit(p.carry1 - p.drop))} לדרך חזרה.` : `משאיר הכול (${ltr(lit(p.drop))}).`)) +
            (done ? ` <b>הגיע ליעד</b> ב-${ltr(lit(st.d))} ק"מ עם ${ltr(lit(st.T))} ליטר ✓` : ` במחסנים : ${ltr(s.depots.map((v, i) => `${lit(i === 0 ? 0 : st.segs[i - 1].x1)} → ${lit(v)}`).filter((t) => !t.endsWith("→ 0")).join(", ") || "0 → 0")}.`);
        }
        // the price list in one line: each stretch, its crossings so far out of 2j − 1, and the price
        const priceOn = $(".cm-price").checked && st.segs.length, cross = priceOn ? camelCrossings(st.segs, st.passes, st.step) : [];
        $(".cm-price-text").innerHTML = priceOn
          ? `המחירון : ` + st.segs.map((sg, i) => `קטע ${ltr(i + 1)} נחצה ${ltr(cross[i].total)} ${cross[i].total === 1 ? "פעם" : "פעמים"}, ${ltr(lit(cross[i].total * st.a))} ליטר לק"מ (עד עכשיו ${ltr(cross[i].done)})`).join("; ") +
            `. בקטע האחרון הקילומטר הכי זול, ולכן מטען מים שלם מגיע בו הכי רחוק.`
          : "";
        $(".cm-step").innerHTML = step;
      };
      let stop = () => {};
      const setParams = (a, c, w, T, typed) => {
        if (!typed) { T = Math.min(T, c); w = Math.max(Math.min(w, LOADS * c), T + 10); }
        const err = !(w > T) ? "המים בהתחלה צריכים להיות יותר מהיעד" : w > LOADS * c ? `לכל היותר ${LOADS} מטענים (${LOADS * c} ליטר)` : T < 0 || T > c ? `היעד בין 0 ל-${c} (מטען אחד)` : "";
        if (!fixed) $(".cm-err").textContent = err;
        if (err) return;
        stop(); st.a = a; st.c = c; st.w = w; st.T = T; st.step = 0; compute(); draw();
      };
      if (!fixed) {
        $(".cm-a").addEventListener("input", () => setParams(Number($(".cm-a").value), st.c, st.w, st.T, false));
        $(".cm-c").addEventListener("input", () => setParams(st.a, Number($(".cm-c").value), st.w, st.T, false));
        [".cm-w", ".cm-t"].forEach((sel) => {
          $(sel).addEventListener("change", () => { const w = Number($(".cm-w").value), T = Number($(".cm-t").value); if (Number.isFinite(w) && Number.isFinite(T)) setParams(st.a, st.c, w, T, true); });
          $(sel).addEventListener("keydown", (e) => { if (e.key === "Enter") $(sel).blur(); });
        });
        $(".ex-reset").addEventListener("click", () => { $(".cm-a").value = A0; $(".cm-c").value = C0; setParams(A0, C0, W0, T0, true); });
      }
      $(".cm-price").addEventListener("change", draw);
      $(".ex-next").addEventListener("click", () => { stop(); if (st.step < st.passes.length) { st.step++; draw(); } });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.step > 0) { st.step--; draw(); } });
      $(".ex-start").addEventListener("click", () => { stop(); st.step = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.step = st.passes.length; draw(); });
      stop = autoplay(play, speed, { step: () => { st.step++; draw(); }, done: () => st.step >= st.passes.length, restart: () => { st.step = 0; draw(); } });
      compute();
      draw();
    },
  });

  dvqExplorers.register({
    views: { camel: camelView },
    help: {
      camel: "״המעבר הבא״ ו״הפעלה״ מזיזים את הגמל מעבר אחרי מעבר על ציר הדרך : הליטרים שעליו מסומנים לידו, כל מחסן מראה כמה ליטר יש בו, והשורה מתחת מסבירה מה הוא עשה. בתיבה הכללית הסליידרים והשדות קובעים את הצריכה, הקיבולת, המים והיעד, והגרף מראה את המרחק המקסימלי לכל כמות מים עם הקירוב הלוגריתמי. המתג ״המחירון על הדרך״ מראה מתחת לכל קטע כמה פעמים הגמל עבר בו ומה עולה בו ק״מ.",
    },
    models: { camelLevels, camelSegments, camelDistance, camelApprox, camelPasses, camelCrossings },
  });
})();
