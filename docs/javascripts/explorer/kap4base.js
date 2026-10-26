// kinds: kap4base
//   kap4base               0013        four digits in a base from 2 to 16: the orbit until a value repeats (a fixed point or a cycle), each step explained by p, q and the digits of F, the map of the pairs (p, q) with the path, where all B⁴ numbers end
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { H, KB_DIGITS, W, X0, autoplay, f, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Sort four digits and subtract in base B (0013 bonus): one step, the pair (p, q) of a
  // number, the value p(B³ − 1) + q(B² − B) of a pair and its digits by the formula, the
  // fixed points of the theorem, the orbit until a value repeats, and every attractor of
  // the base with the number of values that end in it (by the pairs: a number ends where
  // the value of its pair ends).
  const k4Digits = (x, B) => [Math.floor(x / (B * B * B)), Math.floor(x / (B * B)) % B, Math.floor(x / B) % B, x % B];
  const k4Text = (x, B) => k4Digits(x, B).map((v) => KB_DIGITS[v]).join("");
  const k4Parse = (text, B) => {                     // four digits of the base, or null
    const t = String(text).trim().toUpperCase();
    if (!/^[0-9A-F]{4}$/.test(t)) return null;
    const vals = [...t].map((ch) => KB_DIGITS.indexOf(ch));
    return vals.some((v) => v >= B) ? null : ((vals[0] * B + vals[1]) * B + vals[2]) * B + vals[3];
  };
  const k4Pair = (x, B) => { const [a, b, c, d] = k4Digits(x, B).sort((u, v) => v - u); return [a - d, b - c]; };
  const k4Value = (p, q, B) => p * (B * B * B - 1) + q * (B * B - B);
  const k4FormulaDigits = (p, q, B) => (p === 0 ? [0, 0, 0, 0] : q === 0 ? [p - 1, B - 1, B - 1, B - p] : [p, q - 1, B - q - 1, B - p]);
  const k4Step = (x, B) => {
    const s = k4Digits(x, B).sort((u, v) => v - u), [a, b, c, d] = s;
    const largest = ((a * B + b) * B + c) * B + d, smallest = ((d * B + c) * B + b) * B + a, diff = largest - smallest;
    const [p, q] = [a - d, b - c], [pn, qn] = k4Pair(diff, B);
    return { x, sorted: s, largest, smallest, diff, p, q, digitsF: k4FormulaDigits(p, q, B), pNext: pn, qNext: qn };
  };
  const k4Fixed = (B) => { const out = B === 2 ? [7, 9] : B === 4 ? [201] : []; if (B % 5 === 0) out.push((B * (B - 1) * (3 * B * B + 4 * B + 3)) / 5); return out; };
  const k4Orbit = (x, B) => {
    const values = [x];
    for (;;) { const y = k4Step(values[values.length - 1], B).diff, i = values.indexOf(y); if (i >= 0) return { values, start: i }; values.push(y); }
  };
  const k4Attractors = (B) => {
    const count = new Map();
    for (let x = 0; x < B * B * B * B; x++) { const [p, q] = k4Pair(x, B), key = p * B + q; count.set(key, (count.get(key) || 0) + 1); }
    const att = new Map();
    for (const [key, n] of count) {
      const p = Math.floor(key / B), q = key % B, o = k4Orbit(k4Value(p, q, B), B), cyc = o.values.slice(o.start), id = Math.min(...cyc);
      if (!att.has(id)) { const c = [id]; let v = k4Step(id, B).diff; while (v !== id) { c.push(v); v = k4Step(v, B).diff; } att.set(id, { cycle: c, count: 0 }); }
      att.get(id).count += n;
    }
    return [...att.values()].sort((u, v) => v.count - u.count || u.cycle[0] - v.cycle[0]);
  };

  // The base-B four-digit box (0013 bonus): a base from 2 to 16 and four digits typed in
  // that base; the orbit played step by step until a value repeats, a table of the steps,
  // a line that explains each step by p, q and the digits of F and names the fixed point or
  // the cycle when it closes, the map of the pairs (p, q) coloured by where each pair's
  // value ends with the path so far, and the table of where all B⁴ numbers end.
  const kap4baseView = () => ({
    mount(box) {
      const d0 = box.dataset, B0 = Math.min(16, Math.max(2, Number(d0.b || 15)));
      const X0 = k4Parse(d0.x || "1234", B0) ?? 0;
      const st = { B: B0, x: X0, step: 0 };
      const NB = " ";
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>הבסיס B</span><input type="range" class="k4-b" min="2" max="16" step="1" value="${st.B}" dir="ltr" aria-label="הבסיס, מ-2 עד 16"><output class="out-b">${st.B}</output></label>` +
        `<label><span>ארבע ספרות בבסיס</span><input type="text" class="ex-num k4-x" maxlength="4" value="${k4Text(st.x, st.B)}" dir="ltr" spellcheck="false" aria-label="ארבע ספרות בבסיס שנבחר, 0 עד 9 ו-A עד F"></label>` +
        `<span class="kb-dec k4-dec"></span>` +
        `<button type="button" class="md-button ex-random">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err k4-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1000, 400) +
        `<button type="button" class="md-button ex-start">מההתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button><span class="ex-pos"></span></div>` +
        `<p class="ex-summary k4-sum" aria-live="polite"></p><p class="kb-step k4-step"></p>` +
        `<p class="ex-title">המפה של הזוגות (p, q)${NB}: כל משבצת צבועה לפי היעד של הערך שלה, והמסלול של המספר מודגש</p><div class="k4-map"></div>` +
        `<span class="viz-legend"><span><i class="kq-key-fixed"></i>נקודת שבת</span><span><i class="kq-key-cycle"></i>על מחזור</span><span><i class="kq-key-tofixed"></i>מגיעים לנקודת שבת</span><span><i class="kq-key-tocycle"></i>נכנסים למחזור</span><span><i class="kq-key-path"></i>המסלול</span></span>` +
        `<div class="kp-table k4-table"></div>` +       // under the map: the table grows a row a step
        `<p class="ex-title k4-att-title"></p><div class="kp-table k4-att"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), input = $(".k4-x");
      let A = null, Ab = 0, kinds = null;
      const orbit = () => k4Orbit(st.x, st.B);
      const fmtDigits = (ds) => ds.map((v) => KB_DIGITS[v]).join(", ");
      const pairKinds = (B) => {                       // for every pair: fixed, on a cycle, reaching a fixed point, reaching a cycle
        const fixed = new Set(k4Fixed(B)), out = new Map();
        for (let p = 1; p < B; p++) for (let q = 0; q <= p; q++) {
          const v = k4Value(p, q, B), o = k4Orbit(v, B), cyc = o.values.slice(o.start);
          const onCycle = cyc.some((y) => { const [pp, qq] = k4Pair(y, B); return pp === p && qq === q; });
          out.set(p * B + q, fixed.has(v) && onCycle ? "is-fixed" : onCycle ? "is-cycle" : cyc.length === 1 ? "to-fixed" : "to-cycle");
        }
        return out;
      };
      const draw = () => {
        const B = st.B, o = orbit(), total = o.values.length;
        st.step = Math.min(st.step, total);
        const done = st.step === total, cycLen = total - o.start;
        $(".out-b").textContent = String(B);
        if (document.activeElement !== input) input.value = k4Text(st.x, B);
        $(".k4-dec").innerHTML = `= ${ltr(st.x)} בעשרוני`;
        $(".ex-pos").textContent = `צעד ${st.step} מתוך ${total}`;
        $(".ex-prev").disabled = st.step === 0; $(".ex-next").disabled = done; $(".ex-end").disabled = done;
        const fx = k4Fixed(B);
        const ends = o.values[o.start];
        $(".k4-sum").innerHTML = `בסיס ${ltr(B)}${NB}: ` + (fx.length ? `${fx.length === 1 ? "נקודת שבת" : "נקודות שבת"} ${ltr(fx.map((v) => k4Text(v, B)).join(", "))}${B % 5 === 0 ? ` (‏${ltr(`B = 5 · ${B / 5}`)})` : ""}.` : `אין נקודת שבת (‏${ltr(B)} לא מתחלק ב-5, ואינו 2 או 4).`) +
          ` המספר ${ltr(k4Text(st.x, B))} ` + (ends === 0 ? `מגיע ל-0 (כל הספרות שוות).` : cycLen === 1 ? `מגיע לנקודת השבת ${ltr(k4Text(ends, B))} ${o.start === 0 ? "מיד : הוא עצמו נקודת השבת" : o.start === 1 ? "אחרי צעד אחד" : `אחרי ${ltr(o.start)} צעדים`}.` : `נכנס למחזור באורך ${ltr(cycLen)}${NB}: ${ltr(o.values.slice(o.start).map((v) => k4Text(v, B)).join(" → "))} → ${ltr(k4Text(ends, B))}.`);
        let rows = "";
        for (let i = 0; i < st.step; i++) {
          const sp = k4Step(o.values[i], B);
          rows += `<tr${i === st.step - 1 ? ' class="is-last"' : ""}><td>${ltr(i + 1)}</td><td>${ltr(k4Text(sp.x, B))}</td><td>${ltr(k4Text(sp.largest, B))}</td><td>${ltr(k4Text(sp.smallest, B))}</td><td>${ltr(`(${sp.p}, ${sp.q})`)}</td><td class="kb-diff">${ltr(`<b>${k4Text(sp.diff, B)}</b> = ${sp.diff}`)}</td></tr>`;
        }
        $(".k4-table").innerHTML = st.step ? `<table tabindex="0" aria-label="צעדי המיון והחיסור בבסיס"><thead><tr><th>צעד</th><th>X</th><th>מהגדול לקטן</th><th>מהקטן לגדול</th><th>(p, q)</th><th>ההפרש</th></tr></thead><tbody>${rows}</tbody></table>` : `<p class="ex-note">עוד לא נעשה צעד. ״הצעד הבא״ ממיין ומחסר.</p>`;
        let text;
        if (st.step === 0) {
          const sp = k4Step(st.x, B);
          text = sp.p === 0 ? `כל הספרות שוות, ולכן p = 0 וההפרש יהיה 0.` : `הספרות הממוינות ${ltr(fmtDigits(sp.sorted))}${NB}: ‏p = a − d = ${ltr(sp.p)} ו-q = b − c = ${ltr(sp.q)}. ההפרש יהיה ${ltr(`p(B³ − 1) + q(B² − B) = ${sp.diff}`)}.`;
        } else {
          const sp = k4Step(o.values[st.step - 1], B);
          text = `צעד ${ltr(st.step)}${NB}: ‏(p, q) = ${ltr(`(${sp.p}, ${sp.q})`)}, ולכן ${ltr(`F = ${sp.p} · ${B * B * B - 1} + ${sp.q} · ${B * B - B} = ${sp.diff}`)} = ${ltr(k4Text(sp.diff, B))}` +
            (sp.p === 0 ? `.` : `, והספרות לפי הנוסחה ${sp.q === 0 ? ltr("(p − 1, B − 1, B − 1, B − p)") : ltr("(p, q − 1, B − q − 1, B − p)")} = ${ltr(`(${fmtDigits(sp.digitsF)})`)}; הזוג הבא ${ltr(`(${sp.pNext}, ${sp.qNext})`)}.`) +
            (done ? (ends === 0 ? ` <b>ההפרש 0</b>.` : cycLen === 1 ? ` <b>${ltr(k4Text(ends, B))} היא נקודת שבת</b>${NB}: הזוג שלה הוא הזוג שיצר אותה ✓` : ` <b>${ltr(k4Text(sp.diff, B))} כבר הופיע בצעד ${ltr(o.start + 1)}</b>${NB}: מחזור באורך ${ltr(cycLen)}, ולא נגיע לנקודת שבת.`) : "");
        }
        $(".k4-step").innerHTML = text;
        // the map of the pairs with the path so far
        if (Ab !== B) { A = k4Attractors(B); kinds = pairKinds(B); Ab = B; }
        const CW = 24, CH = 20, MX = 40, MY = 24, W = MX + B * CW + 8, H = MY + (B - 1) * CH + 8;
        const cx = (q) => MX + q * CW + CW / 2, cy = (pp) => MY + (pp - 1) * CH + CH / 2;
        let m = `<svg class="figure kq-map k4-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="המפה של הזוגות (p, q) בבסיס ${B} עם המסלול של המספר">`;
        for (let q = 0; q < B; q++) m += `<text class="kq-tick" x="${cx(q)}" y="${MY - 8}" text-anchor="middle">${q}</text>`;
        for (let pp = 1; pp < B; pp++) {
          m += `<text class="kq-tick" x="${MX - 6}" y="${cy(pp) + 4}" text-anchor="end">${pp}</text>`;
          for (let q = 0; q <= pp; q++) m += `<rect class="kq-cell ${kinds.get(pp * B + q)}" x="${MX + q * CW + 1}" y="${MY + (pp - 1) * CH + 1}" width="${CW - 2}" height="${CH - 2}" rx="3"><title>(p, q) = (${pp}, ${q})${NB}: ${k4Text(k4Value(pp, q, B), B)}</title></rect>`;
        }
        const pairs = o.values.slice(0, st.step + 1).map((v) => k4Pair(v, B));
        if (st.step === total) pairs.push(k4Pair(k4Step(o.values[total - 1], B).diff, B));
        for (let i = 0; i + 1 < pairs.length; i++) {
          const [p1, q1] = pairs[i], [p2, q2] = pairs[i + 1];
          if (p1 === 0 || p2 === 0) continue;
          m += `<line class="kq-path" x1="${f(cx(q1))}" y1="${f(cy(p1))}" x2="${f(cx(q2))}" y2="${f(cy(p2))}"/><circle class="kq-head" cx="${f(cx(q2))}" cy="${f(cy(p2))}" r="3.5"/>`;
        }
        if (pairs[0][0] > 0) m += `<circle class="kq-start" cx="${f(cx(pairs[0][1]))}" cy="${f(cy(pairs[0][0]))}" r="7"/>`;
        $(".k4-map").innerHTML = m + "</svg>";
        // where every number of the base ends
        const mine = ends === 0 ? 0 : Math.min(...o.values.slice(o.start));
        $(".k4-att-title").textContent = `לאן מגיעים כל ${(B ** 4).toLocaleString("en-US")} המספרים של בסיס ${B}`;
        $(".k4-att").innerHTML = `<table tabindex="0" aria-label="היעדים של הבסיס"><thead><tr><th>היעד</th><th>סוג</th><th>מספרים</th></tr></thead><tbody>` +
          A.map((a) => `<tr${a.cycle[0] === mine ? ' class="is-last"' : ""}><td>${ltr(a.cycle.map((v) => k4Text(v, B)).join(" → "))}</td><td>${a.cycle[0] === 0 ? "0 (ספרות שוות)" : a.cycle.length === 1 ? "נקודת שבת" : `מחזור באורך ${a.cycle.length}`}</td><td>${ltr(a.count.toLocaleString("en-US"))}</td></tr>`).join("") + `</tbody></table>`;
      };
      let stop = () => {};
      const setX = (x) => { stop(); st.x = x; st.step = 0; draw(); };
      $(".k4-b").addEventListener("input", () => {
        stop(); const B = Number($(".k4-b").value);
        const vals = k4Digits(st.x, st.B).map((v) => Math.min(v, B - 1));           // the same digits, clipped to the new base
        st.B = B; st.x = ((vals[0] * B + vals[1]) * B + vals[2]) * B + vals[3]; st.step = 0; $(".k4-err").textContent = ""; draw();
      });
      input.addEventListener("change", () => { const x = k4Parse(input.value, st.B); $(".k4-err").textContent = x === null ? `ארבע ספרות מ-0 עד ${KB_DIGITS[st.B - 1]}` : ""; if (x !== null) setX(x); else input.value = k4Text(st.x, st.B); });
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      const seed = seedControls(box, $(".ex-random"), (rng) => setX(Math.floor(rng() * st.B ** 4)));
      $(".ex-random").addEventListener("click", () => seed.draw());
      $(".ex-reset").addEventListener("click", () => { stop(); st.B = B0; st.x = X0; st.step = 0; $(".k4-b").value = B0; $(".k4-err").textContent = ""; draw(); });
      $(".ex-next").addEventListener("click", () => { stop(); if (st.step < orbit().values.length) { st.step++; draw(); } });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.step > 0) { st.step--; draw(); } });
      $(".ex-start").addEventListener("click", () => { stop(); st.step = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.step = orbit().values.length; draw(); });
      stop = autoplay(play, speed, { step: () => { st.step++; draw(); }, done: () => st.step >= orbit().values.length, restart: () => { st.step = 0; draw(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { kap4base: kap4baseView },
    help: {
      kap4base: "בוחרים בסיס ומקלידים ארבע ספרות בו : ״הצעד הבא״ ו״הפעלה״ ממיינים ומחסרים צעד אחרי צעד עד שערך חוזר, השורה מתחת מסבירה את p, q ואת הספרות של F ומודיעה על נקודת שבת או מחזור, המפה מראה את המסלול על הזוגות (p, q), והטבלה האחרונה אומרת לאן מגיעים כל מספרי הבסיס.",
    },
    models: { k4Digits, k4Text, k4Parse, k4Pair, k4Value, k4FormulaDigits, k4Step, k4Fixed, k4Orbit, k4Attractors },
  });
})();
