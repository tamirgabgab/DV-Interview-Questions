// kinds: trace
//   trace                  0002, 0003  the page's Python one line (or one comparison) at a time: the swaps (and the three-variable XOR rotation) with a0 / b0 / c0 expressions, the double loop with its invariant
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, ltr, seedControls } = dvqExplorers.lib;

  // Code tracer (0002, 0003): the page's swap functions and the double loop replayed one
  // line (or one comparison) at a time, with the values and, for the swaps, the symbolic
  // expressions in a0 and b0.
  // swapTrace: `kind` is temp / arith / xor; `same` aliases the two cells (swap(v, i, i));
  // `bits` = 8 keeps the values modulo 256 (0 means unbounded integers).
  const SWAP_CODE = {
    temp: ["temp = v[i]", "v[i] = v[j]", "v[j] = temp"],
    arith: ["v[i] = v[i] + v[j]", "v[j] = v[i] - v[j]", "v[i] = v[i] - v[j]"],
    xor: ["v[i] = v[i] ^ v[j]", "v[j] = v[i] ^ v[j]", "v[i] = v[i] ^ v[j]"],
  };
  // A symbolic value is {p, q, r?}: p*a0 + q*b0 (+ r*c0) for arith (and temp), the xor
  // of the same terms for xor and the rotation.
  const symText = (sym, kind) => {
    const op = kind === "arith" || kind === "temp" ? " + " : " ^ ";
    const terms = [];
    const coef = (c, name) => (c === 1 ? name : `${c}·${name}`);
    if (sym.p) terms.push(coef(sym.p, "a0"));
    if (sym.q) terms.push(coef(sym.q, "b0"));
    if (sym.r) terms.push(coef(sym.r, "c0"));
    return terms.length ? terms.join(op) : "0";
  };
  const swapTrace = (kind, a, b, same = false, bits = 0) => {
    const wrap = (v) => (bits ? ((v % (1 << bits)) + (1 << bits)) % (1 << bits) : v);
    const cells = same ? [wrap(a)] : [wrap(a), wrap(b)];   // v[i] is cells[0], v[j] is cells[same ? 0 : 1]
    const syms = same ? [{ p: 1, q: 0 }] : [{ p: 1, q: 0 }, { p: 0, q: 1 }];
    const I = 0, J = same ? 0 : 1;
    let temp = null, tempSym = null;
    const combine = (x, y, op) => {
      if (kind === "xor") return { p: x.p ^ y.p, q: x.q ^ y.q };
      return op === "+" ? { p: x.p + y.p, q: x.q + y.q } : { p: x.p - y.p, q: x.q - y.q };
    };
    const snap = (line, text) => ({ line, text, a: cells[I], b: cells[J], temp, aSym: symText(syms[I], kind), bSym: symText(syms[J], kind), tempSym: tempSym === null ? null : symText(tempSym, kind) });
    const frames = [snap(-1, "")];
    if (kind === "temp") {
      temp = cells[I]; tempSym = syms[I]; frames.push(snap(0, `temp = ${cells[I]}`));
      cells[I] = cells[J]; syms[I] = syms[J]; frames.push(snap(1, `v[i] = ${cells[I]}`));
      cells[J] = temp; syms[J] = tempSym; frames.push(snap(2, `v[j] = ${cells[J]}`));
    } else {
      const op = kind === "xor" ? "^" : null;
      const apply = (line, target, x, y, o) => {
        const before = [cells[x], cells[y]];
        const raw = o === "^" ? cells[x] ^ cells[y] : o === "+" ? cells[x] + cells[y] : cells[x] - cells[y];
        cells[target] = wrap(raw); syms[target] = combine(syms[x], syms[y], o);
        frames.push(snap(line, `${before[0]} ${o} ${before[1]} = ${raw}${wrap(raw) !== raw ? ` → ${wrap(raw)} (mod ${1 << bits})` : ""}`));
      };
      apply(0, I, I, J, op || "+");
      apply(1, J, I, J, op || "-");
      apply(2, I, I, J, op || "-");
    }
    return { code: SWAP_CODE[kind], frames, ok: !same && cells[I] === wrap(b) && cells[J] === wrap(a), same };
  };
  // rotTrace: the follow-up rotation a <- b, b <- c, c <- a without a helper, as two XOR
  // swaps (a with b, then b with c): six lines, one frame each, with the values and the
  // symbolic expressions in a0, b0 and c0.
  const ROT_CODE = ["a = a ^ b", "b = a ^ b", "a = a ^ b", "b = b ^ c", "c = b ^ c", "b = b ^ c"];
  const ROT_STEPS = [["a", "b"], ["b", "a"], ["a", "b"], ["b", "c"], ["c", "b"], ["b", "c"]];   // target, other
  const rotTrace = (a, b, c, bits = 0) => {
    const wrap = (v) => (bits ? ((v % (1 << bits)) + (1 << bits)) % (1 << bits) : v);
    const v = { a, b, c }, sym = { a: { p: 1, q: 0, r: 0 }, b: { p: 0, q: 1, r: 0 }, c: { p: 0, q: 0, r: 1 } };
    const snap = (line, text) => ({ line, text, a: v.a, b: v.b, c: v.c, temp: null, aSym: symText(sym.a, "xor"), bSym: symText(sym.b, "xor"), cSym: symText(sym.c, "xor"), tempSym: null });
    const frames = [snap(-1, "")];
    ROT_STEPS.forEach(([t, o], line) => {
      const [x, y] = [t, o].sort(), before = [v[x], v[y]], raw = v[t] ^ v[o];   // printed in the order of the line
      v[t] = wrap(raw);
      sym[t] = { p: sym[t].p ^ sym[o].p, q: sym[t].q ^ sym[o].q, r: sym[t].r ^ sym[o].r };
      frames.push(snap(line, `${before[0]} ^ ${before[1]} = ${raw}`));
    });
    return { code: ROT_CODE, frames, ok: v.a === wrap(b) && v.b === wrap(c) && v.c === wrap(a) };
  };
  // loopTrace: the page's mystery(A), one comparison per frame; `endOfI` marks the last
  // comparison of an outer iteration, with the sorted prefix and the maximum noted.
  const LOOP_CODE = ["n = len(A)", "for i in range(n):", "    for j in range(n):", "        if A[i] < A[j]:", "            A[i], A[j] = A[j], A[i]"];
  const loopTrace = (A0) => {
    const A = [...A0], n = A.length, frames = [];
    let comparisons = 0, swaps = 0;
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        const before = [...A], swapped = A[i] < A[j];
        comparisons += 1;
        if (swapped) { const t = A[i]; A[i] = A[j]; A[j] = t; swaps += 1; }
        frames.push({ i, j, before, after: [...A], swapped, comparisons, swaps, endOfI: j === n - 1 });
      }
    }
    return { code: LOOP_CODE, frames, result: A, comparisons, swaps };
  };

  // The tracer box (0002, 0003): the Python code of the page on the left with the current
  // line lit, the state on the right. data-mode="swap": a version select, a and b, the
  // same-variable and 8-bit toggles, the symbolic expressions in a0 and b0; data-version
  // locks it on one version.
  // data-mode="loop": a typed or random array, one comparison per step, a jump to the end
  // of the outer iteration with the invariant, the counters.
  const traceView = (box) => ({
    mount() {
      const mode = box.dataset.mode === "loop" ? "loop" : "swap";
      const playRow = (next, prev, extra = "") =>
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button md-button--primary ex-next">${next}</button>` +
        `<button type="button" class="md-button ex-prev">${prev}</button>${extra}` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1400">איטי</option><option value="800" selected>בינוני</option><option value="250">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button><button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>`;
      const codeHtml = (code, cur, swapLine) => `<pre class="tr-code" dir="ltr" tabindex="0" aria-label="הקוד">` +
        code.map((l, k) => `<span class="tr-line${k === cur ? " is-cur" : ""}${k === swapLine ? " is-swap" : ""}"><span class="tr-ln">${k + 1}</span>${l.replace(/</g, "&lt;")}</span>`).join("\n") + `</pre>`;
      const $ = (sel) => box.querySelector(sel);
      let timer = null;
      const stop = () => { if (timer) clearInterval(timer); timer = null; $(".ex-play").textContent = "הפעלה"; };
      if (mode === "swap") {
        // data-version="temp" or "arith" locks the box on one part's version (0002 parts a, b)
        const lock = ["temp", "arith"].includes(box.dataset.version) ? box.dataset.version : null;
        const PAGE = { kind: lock || "arith", a: 5, b: 3, c: 7, same: false, bits: 0, k: 0 };
        const st = { ...PAGE };
        box.innerHTML =
          `<div class="ex-controls"><label>הגרסה <select class="ex-kind" aria-label="גרסת ההחלפה"><option value="temp">עם משתנה עזר (סעיף א)</option><option value="arith" selected>אריתמטיקה (סעיף ב)</option><option value="xor">XOR (סעיף ג)</option><option value="rot">סיבוב של שלושה ב-XOR (שאלת המשך)</option></select></label>` +
          `<label><span>a</span> <input type="number" class="ex-a" dir="ltr" value="5" aria-label="הערך של a"></label>` +
          `<label><span>b</span> <input type="number" class="ex-b" dir="ltr" value="3" aria-label="הערך של b"></label>` +
          `<label class="tr-c" hidden><span>c</span> <input type="number" class="ex-c" dir="ltr" value="7" aria-label="הערך של c"></label>` +
          `<label><input type="checkbox" class="ex-same"> <span>‏a ו-b הם אותו משתנה (${code("swap(v, i, i)")})</span></label>` +
          `<label><input type="checkbox" class="ex-bits"> <span>‏int של 8 ביט (מודולו 256)</span></label>` +
          `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
          playRow("השורה הבאה", "השורה הקודמת") +
          `<div class="tr-box"><div class="tr-left"></div><div class="tr-right"></div></div>` +
          `<p class="wv-step tr-step" aria-live="polite"></p><p class="ex-summary tr-sum"></p>`;
        const bits8 = (v) => (st.bits ? ltr(v.toString(2).padStart(8, "0")) : "");
        const rot = () => st.kind === "rot";
        const traceOf = () => (rot() ? rotTrace(st.a, st.b, st.c, st.bits) : swapTrace(st.kind, st.a, st.b, st.same, st.bits));
        const draw = () => {
          const tr = traceOf(), total = tr.frames.length - 1;
          st.k = Math.min(st.k, total);
          const fr = tr.frames[st.k], prev = st.k ? tr.frames[st.k - 1] : null;
          $(".tr-left").innerHTML = codeHtml(tr.code, fr.line, -1);
          const row = (name, v, sym, changed) => `<tr class="${changed ? "is-changed" : ""}"><td>${ltr(name)}</td><td>${v === null ? "–" : ltr(v)}</td>${st.bits ? `<td>${v === null ? "" : bits8(v)}</td>` : ""}<td>${sym === null ? "–" : ltr(sym)}</td></tr>`;
          $(".tr-right").innerHTML = `<table class="tr-vars"><thead><tr><th>משתנה</th><th>ערך</th>${st.bits ? "<th>ביטים</th>" : ""}<th>סימבולית</th></tr></thead><tbody>` +
            row(rot() ? "a" : st.same ? "v[i] = v[j]" : "v[i] (a)", fr.a, fr.aSym, prev && prev.a !== fr.a) +
            (st.same ? "" : row(rot() ? "b" : "v[j] (b)", fr.b, fr.bSym, prev && prev.b !== fr.b)) +
            (rot() ? row("c", fr.c, fr.cSym, prev && prev.c !== fr.c) : "") +
            (st.kind === "temp" ? row("temp", fr.temp, fr.tempSym, prev && prev.temp !== fr.temp) : "") + `</tbody></table>`;
          $(".ex-pos").textContent = `שורה ${st.k} מתוך ${total}`;
          $(".tr-step").innerHTML = st.k === 0
            ? `לפני הריצה : ${ltr(`a = a0 = ${st.a}`)}${st.same ? ` ו-b הוא אותו תא` : `, ${ltr(`b = b0 = ${st.b}`)}`}${rot() ? `, ${ltr(`c = c0 = ${st.c}`)}` : ""}.`
            : `שורה ${ltr(st.k)} : ${ltr(code(tr.code[fr.line]))} ⇒ ${ltr(fr.text)}. סימבולית : ${ltr(`a = ${fr.aSym}`)}${st.same ? "" : `, ${ltr(`b = ${fr.bSym}`)}`}${rot() ? `, ${ltr(`c = ${fr.cSym}`)}` : ""}${fr.tempSym !== null && st.kind === "temp" ? `, ${ltr(`temp = ${fr.tempSym}`)}` : ""}.`;
          let sum = "";
          if (st.k === total) {
            if (rot()) sum = tr.ok
              ? `<span class="wv-ok">✓ סובבו : ${ltr(`a = b0 = ${fr.a}`)}, ${ltr(`b = c0 = ${fr.b}`)}, ${ltr(`c = a0 = ${fr.c}`)}.</span> שש פעולות XOR, כי סיבוב של שלושה הוא שתי החלפות : ${ltr("a ↔ b")} (שורות 1 עד 3) ואז ${ltr("b ↔ c")} (שורות 4 עד 6). אחרי ההחלפה הראשונה ${ltr("b = a0")}, וההחלפה השנייה מעבירה את ${ltr("a0")} ל-${ltr("c")}.`
              : `<span class="wv-bad">✗ הערכים לא סובבו.</span>`;
            else if (tr.ok) sum = `<span class="wv-ok">✓ הוחלפו : ${ltr(`a = b0 = ${fr.a}`)}, ${ltr(`b = a0 = ${fr.b}`)}.</span>`;
            else if (st.same) sum = st.kind === "temp" ? `<span class="wv-ok">✓ אותו משתנה : עם משתנה עזר הערך נשמר (${ltr(fr.a)}).</span>` : `<span class="wv-bad">✗ אותו משתנה : ${st.kind === "arith" ? "השורה הראשונה מכפילה והשנייה מאפסת" : "השורה הראשונה מחשבת a ^ a = 0"}, והערך ${ltr(st.a)} אבד. זו המלכודת של ${code("swap(v, i, i)")}.</span>`;
            else sum = `<span class="wv-bad">✗ הערכים לא הוחלפו.</span>`;
            if (st.bits && st.kind === "arith" && !st.same && st.a + st.b >= 256) sum += ` הסכום ${ltr(`${st.a} + ${st.b} = ${st.a + st.b}`)} גלש מעבר ל-255, ובכל זאת ההחלפה נכונה : החיסור מתבצע באותו מודולו, ו-${ltr("(a0 + b0) − b0 ≡ a0 (mod 256)")}.`;
          }
          $(".tr-sum").innerHTML = sum;
        };
        const total = () => traceOf().frames.length - 1;
        const readInputs = () => {
          const lim = st.bits ? 255 : 1e9;
          const clamp = (sel) => Math.max(st.bits ? 0 : -lim, Math.min(lim, Math.round(Number($(sel).value) || 0)));
          st.a = clamp(".ex-a"); st.b = clamp(".ex-b"); st.c = clamp(".ex-c");
          $(".ex-a").value = st.a; $(".ex-b").value = st.b; $(".ex-c").value = st.c;
        };
        // the rotation has three cells and no aliasing: the c field appears, "same" is off
        const setKind = (kind) => {
          st.kind = kind; $(".ex-kind").value = kind;
          $(".tr-c").hidden = !rot();
          if (rot()) { st.same = false; $(".ex-same").checked = false; $(".ex-b").disabled = false; }
          $(".ex-same").disabled = rot();
        };
        $(".ex-kind").addEventListener("change", () => { stop(); setKind($(".ex-kind").value); st.k = 0; draw(); });
        [".ex-a", ".ex-b", ".ex-c"].forEach((sel) => $(sel).addEventListener("change", () => { stop(); readInputs(); st.k = 0; draw(); }));
        $(".ex-same").addEventListener("change", () => { stop(); st.same = $(".ex-same").checked; $(".ex-b").disabled = st.same; st.k = 0; draw(); });
        $(".ex-bits").addEventListener("change", () => { stop(); st.bits = $(".ex-bits").checked ? 8 : 0; readInputs(); st.k = 0; draw(); });
        $(".ex-reset").addEventListener("click", () => {
          stop(); Object.assign(st, PAGE);
          setKind(PAGE.kind); $(".ex-a").value = PAGE.a; $(".ex-b").value = PAGE.b; $(".ex-c").value = PAGE.c; $(".ex-b").disabled = false; $(".ex-same").checked = false; $(".ex-bits").checked = false;
          draw();
        });
        $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
        $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
        $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
        $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
        $(".ex-play").addEventListener("click", () => {
          if (timer) { stop(); return; }
          if (st.k >= total()) st.k = 0;
          $(".ex-play").textContent = "עצירה";
          timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number($(".ex-speed").value));
        });
        $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); $(".ex-play").click(); } });
        if (lock) {
          $(".ex-kind").closest("label").hidden = true;
          if (lock === "temp") $(".ex-bits").closest("label").hidden = true;   // overflow is part b's
          setKind(lock);
        }
        draw();
        return;
      }
      const PAGE = [3, 1, 4, 2];
      const st = { A: PAGE.slice(), k: 0 };
      box.innerHTML =
        `<div class="ex-controls"><label><span>המערך</span><input type="text" class="ex-nums" dir="ltr" value="3, 1, 4, 2" spellcheck="false" aria-label="המערך, מספרים מופרדים בפסיקים"></label>` +
        `<button type="button" class="md-button ex-page">דוגמת העמוד</button><button type="button" class="md-button ex-random">אקראי</button><span class="fl-err"></span></div>` +
        playRow("ההשוואה הבאה", "הקודמת", `<button type="button" class="md-button ex-endi">עד סוף i</button>`) +
        `<div class="tr-box"><div class="tr-left"></div><div class="tr-right"></div></div>` +
        `<p class="wv-step tr-step" aria-live="polite"></p><p class="ex-summary tr-sum"></p>`;
      const draw = () => {
        const tr = loopTrace(st.A), total = tr.frames.length;
        st.k = Math.min(st.k, total);
        const fr = st.k ? tr.frames[st.k - 1] : null, n = st.A.length;
        $(".tr-left").innerHTML = codeHtml(tr.code, fr ? 3 : 0, fr && fr.swapped ? 4 : -1);
        const arr = fr ? fr.after : st.A, sortedTo = fr ? (fr.endOfI ? fr.i : fr.i - 1) : -1;
        $(".tr-right").innerHTML = `<div class="tr-arr" dir="ltr">` + arr.map((v, x) => {
          const cls = [x <= sortedTo ? "is-done" : "", fr && x === fr.i ? "is-i" : "", fr && x === fr.j ? "is-j" : "", fr && fr.swapped && (x === fr.i || x === fr.j) ? "is-swapped" : ""].join(" ").trim();
          return `<span class="${cls}"><span class="tr-idx">${x}</span>${v}</span>`;
        }).join("") + `</div><p class="tr-counts">${fr ? `${ltr("i")} = ${ltr(fr.i)}, ${ltr("j")} = ${ltr(fr.j)}. ` : ""}השוואות : ${ltr(fr ? fr.comparisons : 0)} מתוך ${ltr(n * n)}, החלפות : ${ltr(fr ? fr.swaps : 0)}.</p>` +
          `<p class="tr-legend"><span class="tr-lg-i">מסגרת כחולה : ${code("i")}</span> <span class="tr-lg-j">מסגרת כתומה מקווקוות : ${code("j")}</span> <span class="tr-lg-done">ירוק : ${code("A[0..i]")} ממוין</span></p>`;
        $(".ex-pos").textContent = `השוואה ${st.k} מתוך ${total}`;
        let step;
        if (!fr) step = n ? `לפני הריצה : ${ltr(`A = [${st.A.join(", ")}]`)}, ${ltr(`n = ${n}`)}. הלולאה הפנימית מתחילה מ-${ltr("j = 0")}, לא מ-${ltr("j = i + 1")}.` : `מערך ריק : אין השוואות.`;
        else {
          const ai = fr.before[fr.i], aj = fr.before[fr.j];
          step = `${ltr(`i = ${fr.i}, j = ${fr.j}`)} : ${ltr(`A[i] < A[j]`)} הוא ${ltr(`${ai} < ${aj}`)}, ` + (fr.swapped ? `<span class="wv-ok">כן ⇒ החלפה</span> : ${ltr(`A = [${fr.after.join(", ")}]`)}.` : `לא ⇒ בלי שינוי.`);
          if (fr.endOfI) step += ` <span class="wv-ok">סוף האיטרציה ${ltr(`i = ${fr.i}`)} : ${ltr(`A[0..${fr.i}]`)} ממוין בסדר עולה, והמקסימום של כל המערך (${ltr(Math.max(...fr.after))}) יושב במקום ${ltr(fr.i)}.</span>`;
          else if (fr.j < fr.i) step += ` ‏${ltr("j < i")} : החלפה כאן מזיזה את ${ltr("A[i]")} אחורה לתוך החלק הממוין.`;
        }
        $(".tr-step").innerHTML = step;
        $(".tr-sum").innerHTML = st.k >= total && n ? `<span class="wv-ok">✓ ${ltr(`n² = ${n * n}`)} השוואות, ${ltr(tr.swaps)} החלפות, בלי יציאה מוקדמת. המערך ממוין בסדר עולה : ${ltr(`[${tr.result.join(", ")}]`)}.</span>` : "";
      };
      const total = () => loopTrace(st.A).frames.length;
      const parse = () => {
        const parts = $(".ex-nums").value.split(/[,\s]+/).filter((t) => t.length);
        const nums = parts.map(Number);
        if (!nums.length || nums.some((v) => !Number.isInteger(v)) || nums.length > 8) { $(".fl-err").textContent = "3 עד 8 מספרים שלמים, מופרדים בפסיקים"; return; }
        if (nums.length < 3) { $(".fl-err").textContent = "לפחות 3 מספרים"; return; }
        $(".fl-err").textContent = ""; stop(); st.A = nums; st.k = 0; draw();
      };
      $(".ex-nums").addEventListener("change", parse);
      $(".ex-page").addEventListener("click", () => { $(".ex-nums").value = PAGE.join(", "); parse(); });
      const seed = seedControls(box, $(".ex-random"), (rng) => { const n = 3 + Math.floor(rng() * 6); $(".ex-nums").value = Array.from({ length: n }, () => Math.floor(rng() * 20)).join(", "); parse(); });
      $(".ex-random").addEventListener("click", seed.draw);
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-endi").addEventListener("click", () => { stop(); const n = st.A.length; if (st.k < total()) st.k = Math.min(total(), (Math.floor((st.k) / n) + 1) * n); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      $(".ex-play").addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= total()) st.k = 0;
        $(".ex-play").textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number($(".ex-speed").value));
      });
      $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); $(".ex-play").click(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { trace: traceView },
    help: {
      trace: "הקוד של העמוד שורה אחרי שורה : ״הבא״ ו״הפעלה״ מריצים אותו עם הערכים והביטויים, הבורר מחליף בין הגרסאות, והשדות קובעים את הקלט.",
    },
    models: { SWAP_CODE, swapTrace, ROT_CODE, rotTrace, LOOP_CODE, loopTrace },
  });
})();
