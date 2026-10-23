// kinds: div3
//   div3                   0035        the half-cycle model one clock edge at a time: cnt, a, b and clk_out on a strip, the duty measured; a wake-up in an unreachable state; a divide by N (2 to 10) and a strip length
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, ltr, waveStrip } = dvqExplorers.lib;

  // Divide by three (0035): the page's half-cycle model, edge by edge, from any counter
  // state. `counter`: "wrap" is the module (cnt is 2 bits, so 3 + 1 wraps to 0), "wide"
  // is a counter with no wrap (the page's Python model: 3 + 1 = 4 and a never rises),
  // "guard" compares with >= 2. Returns the values after each edge.
  // The follow-up generalises to a divide by N: the counter is modulo N in
  // ceil(log2 N) bits, a is high for the last floor(N / 2) counts (one for N = 3, two
  // for N = 5 and for N = 4), b is a half a cycle later, and the output is a | b for an
  // odd N (high N / 2 cycles) and a alone for an even N (already 50%; the OR would add
  // half a cycle). The highest state of the counter, 2^bits - 1, is unreachable when it
  // is >= N.
  const div3Params = (N) => {
    const bits = Math.max(1, Math.ceil(Math.log2(N) - 1e-9)), top = (1 << bits) - 1;
    const high = Math.floor(N / 2);
    return { N, bits, mask: top, high, from: N - high, wake: top >= N ? top : null, odd: N % 2 === 1 };
  };
  const div3Trace = (halfCycles, cnt0 = 0, counter = "wrap", N = 3) => {
    const P = div3Params(N);
    let cnt = cnt0, a = 0, b = 0;
    const rows = [];
    for (let edge = 0; edge < halfCycles; edge++) {
      const rising = edge % 2 === 0;
      const pa = a, pb = b, pc = cnt;
      if (rising) {
        a = cnt >= P.from && cnt <= N - 1 ? 1 : 0;
        if (counter === "guard") cnt = cnt >= N - 1 ? 0 : cnt + 1;
        else if (counter === "wide") cnt = cnt === N - 1 ? 0 : cnt + 1;
        else cnt = cnt === N - 1 ? 0 : (cnt + 1) & P.mask;
      } else b = a;
      rows.push({ edge, rising, cnt, a, b, out: P.odd ? a | b : a, aChanged: a !== pa, bChanged: b !== pb, cntPrev: pc });
    }
    return rows;
  };
  // The period and the high count of the output from the first rise, and whether it
  // settled into 3 high / 3 low.
  const div3Duty = (rows) => {
    const out = rows.map((r) => r.out);
    const rises = [];
    out.forEach((v, i) => { if (v && !(i > 0 && out[i - 1])) rises.push(i); });
    if (rises.length < 2) return { rises, period: null, high: null };
    const period = rises[1] - rises[0];
    let high = 0;
    for (let i = rises[0]; i < rises[1]; i++) high += out[i];
    const ok = rises.every((r, k) => k === 0 || r - rises[k - 1] === period);
    return { rises, period, high, ok };
  };

  // The divide-by-three box (0035): the page's half-cycle model one clock edge at a time
  // or played; the strip of clk, cnt, a, b and clk_out with the overlap of a and b shaded;
  // the duty measured from the trace; a wake-up in state 3 with the counter as in the
  // module (2 bits, wraps), without a wrap (the Python model) or guarded (>= 2).
  const div3View = () => ({
    mount(box) {
      const st = { k: 0, cnt0: 0, counter: "wrap", N: 3, total: 36 };
      const P = () => div3Params(st.N);
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>מחלק ב-N</span><input type="range" class="ex-n" min="2" max="10" step="1" value="3" dir="ltr" aria-label="המחלק N"><output class="out-n">3</output></label>` +
        `<label>אורך הרצועה <select class="ex-len" aria-label="אורך הרצועה במחזורים"><option value="36" selected>18 מחזורים</option><option value="60">30 מחזורים</option><option value="120">60 מחזורים</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">השפה הבאה</button>` +
        `<button type="button" class="md-button ex-prev">השפה הקודמת</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="900">איטי</option><option value="450" selected>בינוני</option><option value="150">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">איפוס</button>` +
        `<button type="button" class="md-button ex-wake">התעוררות במצב 3</button>` +
        `<label>המונה <select class="ex-counter" aria-label="גרסת המונה"><option value="wrap" class="opt-wrap">2 ביטים, כמו במודול</option><option value="wide">רחב יותר, בלי גלגול</option><option value="guard">מגן : cnt &gt;= 2</option></select></label>` +
        `<span class="ex-pos"></span></div>` +
        `<div class="wv-wrap" tabindex="0" role="group" aria-label="דיאגרמת תזמון של המחלק בשלוש, גלילה אופקית"></div>` +
        `<p class="wv-step" aria-live="polite"></p><p class="ex-summary wv-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let timer = null;
      const draw = () => {
        const { N, bits, from, wake, odd, high } = P(), TOTAL = st.total, wakeState = wake === null ? null : wake;
        const thr = high === 1 ? `${code("cnt")} == ${N - 1}` : `${code("cnt")} >= ${from}`;   // the a condition as text
        const rows = div3Trace(TOTAL, st.cnt0, st.counter, N), shown = rows.slice(0, st.k);
        $(".out-n").textContent = String(N);
        $(".ex-wake").textContent = wake === null ? `אין מצב לא נגיש (${bits} ביט ל-${N} מצבים)` : `התעוררות במצב ${wake}`;
        $(".ex-wake").disabled = wake === null;
        $(".opt-wrap").textContent = `${bits} ביט, כמו במודול`;
        const val = (key) => shown.map((r) => r[key]);
        const strip = [
          { name: "clk", kind: "clock" },
          { name: "cnt", kind: "bus", values: val("cnt") },
          { name: "a", kind: "bit", values: val("a"), cls: "wv-s1" },
          { name: "b", kind: "bit", values: val("b"), cls: "wv-s3" },
          { name: "clk_out", kind: "bit", values: val("out"), cls: "wv-s2", marks: shown.map((r) => r.a && r.b) },
        ];
        if (!odd) strip[4].marks = shown.map(() => 0);   // an even N: the output is a alone, no OR overlap
        $(".wv-wrap").innerHTML = waveStrip(strip, TOTAL, { half: true, label: "דיאגרמת תזמון בחצאי מחזורים", cursor: st.k ? st.k - 1 : null, ticks: (k) => (k % 2 === 0 ? k / 2 : "") });
        $(".ex-pos").textContent = `שפה ${st.k} מתוך ${TOTAL}`;
        $(".ex-prev").disabled = st.k === 0;
        let step;
        const woke = wake !== null && st.cnt0 === wake;
        if (!st.k) step = woke
          ? `המונה התעורר במצב ${wake}, שאינו נגיש אחרי איפוס : ${ltr(`${code("cnt")} = ${wake}`)}, ${ltr(`${code("a")} = 0`)}, ${ltr(`${code("b")} = 0`)}.`
          : `אחרי איפוס : ${ltr(`${code("cnt")} = 0`)}, ${ltr(`${code("a")} = 0`)}, ${ltr(`${code("b")} = 0`)}, והמוצא נמוך.` +
            (N === 3 ? "" : odd ? ` מחלק ב-${ltr(N)} : המונה סופר 0 עד ${ltr(N - 1)} ב-${ltr(bits)} ביט, ${code("a")} גבוה ${ltr(high)} מחזורים (${ltr(thr)}), ${code("b")} מוזז בחצי, והמוצא ${ltr("a | b")} גבוה ${ltr(`${N / 2}`)} מחזורים.`
              : ` מחלק ב-${ltr(N)}, זוגי : ${code("a")} גבוה ${ltr(high)} מתוך ${ltr(N)} מחזורים הוא כבר 50%, ולכן המוצא הוא ${code("a")} לבד; ${code("b")} מצויר אבל לא משתתף (${ltr("a | b")} היה נותן ${ltr(`${high + 0.5}`)} מחזורים).`);
        else {
          const r = rows[st.k - 1], cyc = Math.floor(r.edge / 2);
          if (r.rising) {
            step = `עליית השעון של מחזור ${ltr(cyc)} : ${ltr(`${code("a")} ← (${thr}) = ${r.a}`)}, ו-${ltr(`${code("cnt")} ← ${r.cnt}`)}` +
              (wake !== null && r.cntPrev === wake ? (st.counter === "wide" ? ` (‏${ltr(`${wake} + 1 = ${wake + 1}`)} : בלי גלגול המונה לא חוזר ל-0)` : st.counter === "guard" ? ` (‏${ltr(`${wake} >= ${N - 1}`)}, ולכן חזרה ל-0)` : ` (‏${ltr(`${wake} + 1`)} ב-${ltr(bits)} ביט מתגלגל ל-0)`) : "") + ".";
            if (r.aChanged && r.a) step += ` <span class="wv-ok">‏${code("a")} עלה : המוצא עולה עם עליית השעון.</span>`;
            else if (r.aChanged && !r.a) step += !odd ? ` ${code("a")} ירד : המוצא יורד איתו.` : r.b ? ` <span class="wv-ok">‏${code("a")} ירד, אבל ${code("b")} עדיין 1 : ה-OR מחזיק את המוצא גבוה, בלי גליץ'.</span>` : ` ${code("a")} ירד ו-${code("b")} כבר 0 : המוצא יורד.`;
          } else {
            step = `ירידת השעון באמצע מחזור ${ltr(cyc)} : ${ltr(`${code("b")} ← ${code("a")} = ${r.b}`)}.`;
            if (!odd) step += ` ‏${code("b")} לא משתתף במוצא כש-${ltr("N")} זוגי.`;
            else if (r.bChanged && r.b) step += ` ‏${code("b")} עלה כש-${code("a")} כבר 1 : המוצא כבר גבוה, ואין שינוי בו.`;
            else if (r.bChanged && !r.b) step += ` <span class="wv-ok">‏${code("b")} ירד ו-${code("a")} כבר 0 מחצי מחזור : המוצא יורד בירידת השעון, אחרי ${ltr(`${N / 2}`)} מחזורים גבוה.</span>`;
          }
        }
        $(".wv-step").innerHTML = step;
        const duty = div3Duty(shown);
        let sum;
        if (duty.period === null) {
          const stuck = st.counter === "wide" && woke;
          sum = stuck && st.k >= 6 ? `<span class="wv-bad">המונה ממשיך לספור ${ltr(`${wake + 1}, ${wake + 2}, ${wake + 3}…`)} ולא חוזר ל-${ltr(N - 1)} : ${code("a")} לא עולה לעולם והמוצא תקוע נמוך. זה מה שמודל ה-Python של העמוד היה עושה ממצב ${ltr(wake)}.</span>`
            : `המוצא עוד לא השלים תקופה : ${code("a")} עולה רק אחרי שהמונה מגיע ל-${ltr(from)}.`;
        } else {
          sum = `מהעלייה הראשונה : תקופה של ${ltr(duty.period)} חצאי מחזורים = ${ltr(duty.period / 2)} מחזורים, גבוה ${ltr(duty.high)} מתוכם : duty ${ltr(Math.round((100 * duty.high) / duty.period))}%` +
            (duty.period === 2 * N && duty.high === N && duty.ok ? ` ✓ חלוקה ב-${ltr(N)} עם 50%.` : ".");
        }
        $(".wv-sum").innerHTML = sum;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, st.total); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; st.cnt0 = 0; draw(); });
      $(".ex-wake").addEventListener("click", () => { const w = P().wake; if (w === null) return; stop(); st.k = 0; st.cnt0 = w; draw(); });
      $(".ex-counter").addEventListener("change", () => { stop(); st.counter = $(".ex-counter").value; st.k = 0; draw(); });
      $(".ex-n").addEventListener("input", () => { stop(); st.N = Number($(".ex-n").value); st.k = 0; st.cnt0 = 0; draw(); });
      $(".ex-len").addEventListener("change", () => { stop(); st.total = Number($(".ex-len").value); st.k = Math.min(st.k, st.total); draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, { k: 0, cnt0: 0, counter: "wrap", N: 3, total: 36 }); $(".ex-n").value = 3; $(".ex-len").value = "36"; $(".ex-counter").value = "wrap"; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= st.total) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= st.total) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { div3: div3View },
    help: {
      div3: "״השפה הבאה״ ו״הפעלה״ מריצים את מודל חצאי המחזור : cnt, a, b ו-clk_out על רצועה, וה-duty נמדד. ״התעוררות״ מתחילה ממצב לא נגיש לפי בורר המונה, והסליידר מחלק ב-N. ״העתקת WaveDrom״ מעתיקה את הרצועה כ-JSON.",
    },
    models: { div3Params, div3Trace, div3Duty },
  });
})();
