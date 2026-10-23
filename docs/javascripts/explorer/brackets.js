// kinds: brackets
//   brackets               0010        a typed bracket string read character by character: the stack, the depth chart, the first failure
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, H, W, X0, f, ltr } = dvqExplorers.lib;

  // Valid parentheses (0010): the page's stack, one frame per character: push, pop, or
  // the first failure (a closer with an empty stack, or one that does not match the top);
  // openers left at the end are the third failure.
  const BRACKET_OF = { ")": "(", "]": "[", "}": "{" };
  const bracketsClean = (text) => [...String(text)].filter((c) => "()[]{}".includes(c)).join("");
  const bracketsTrace = (s) => {
    const frames = [], stack = [];
    let fail = null;
    for (let i = 0; i < s.length; i++) {
      const ch = s[i];
      if (ch in BRACKET_OF) {
        if (!stack.length) { fail = { i, kind: "unopened" }; frames.push({ i, ch, action: "unopened", stack: stack.join("") }); break; }
        const top = stack[stack.length - 1];
        if (top !== BRACKET_OF[ch]) { fail = { i, kind: "mismatch", top }; frames.push({ i, ch, action: "mismatch", stack: stack.join(""), top }); break; }
        stack.pop();
        frames.push({ i, ch, action: "pop", stack: stack.join("") });
      } else {
        stack.push(ch);
        frames.push({ i, ch, action: "push", stack: stack.join("") });
      }
    }
    if (!fail && stack.length) fail = { i: s.length, kind: "unclosed", left: stack.join("") };
    return { frames, valid: !fail, fail, odd: s.length % 2 === 1 };
  };

  const bracketsView = () => ({
    mount(box) {
      const PRESETS = ["()", "()[]{}", "{[()]}", "([]{})", "(]", "([)]", "(((", "())", ")("];
      const st = { s: box.dataset.s || "{[()]}", k: 0 };
      const NAMES = { "(": "עגול", "[": "מרובע", "{": "מסולסל" };
      const esc = (c) => c.replace(/</g, "&lt;");
      box.innerHTML =
        `<div class="ex-controls"><label><span>המחרוזת</span><input type="text" class="ex-s" dir="ltr" spellcheck="false" maxlength="40" aria-label="מחרוזת של סוגריים"></label>` +
        `<span class="br-presets">דוגמאות : ` + PRESETS.map((p) => `<button type="button" class="md-button ex-preset" dir="ltr" data-s="${esc(p)}">${esc(p)}</button>`).join(" ") + `</span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">התו הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">התו הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1200">איטי</option><option value="600" selected>בינוני</option><option value="200">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<div class="br-box"><div class="br-main"><div class="br-chars" dir="ltr"></div><div class="br-chart"></div></div>` +
        `<div class="br-stackwrap"><p class="ex-title">המחסנית</p><div class="br-stack" dir="ltr"></div></div></div>` +
        `<p class="br-step" aria-live="polite"></p><p class="ex-summary br-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), input = $(".ex-s");
      let timer = null;
      const draw = () => {
        const s = st.s, tr = bracketsTrace(s), total = tr.frames.length;
        st.k = Math.min(st.k, total);
        if (document.activeElement !== input) input.value = s;
        const fr = st.k ? tr.frames[st.k - 1] : null;
        const failAt = tr.fail && st.k >= total ? tr.fail.i : -1;
        $(".br-chars").innerHTML = s.length ? [...s].map((c, i) =>
          `<span class="${[i === st.k - 1 ? "is-cur" : "", i < st.k - 1 || (i === st.k - 1 && fr.action !== "mismatch" && fr.action !== "unopened") ? "is-done" : "", i === failAt ? "is-fail" : ""].join(" ").trim()}">${esc(c)}</span>`).join("") +
          (tr.fail && tr.fail.kind === "unclosed" && st.k >= total ? `<span class="is-fail is-end" aria-label="סוף המחרוזת">⏎</span>` : "")
          : `<span class="br-empty">(מחרוזת ריקה)</span>`;
        const stack = fr ? fr.stack : "";
        $(".br-stack").innerHTML = stack.length ? [...stack].map((c, i) =>
          `<span class="${i === stack.length - 1 ? "is-top" : ""}">${esc(c)}</span>`).join("") : `<span class="br-empty">ריקה</span>`;
        // the depth after each character read so far
        const depths = tr.frames.map((g) => g.stack.length);
        const n = Math.max(s.length, 1), W = 320, H = 90, X0 = 8, BASE = H - 18, dmax = Math.max(1, ...depths);
        const slot = (W - 2 * X0) / n, bw = Math.max(2, slot * 0.7);
        let c = `<svg class="perf-chart br-depth" viewBox="0 0 ${W} ${H}" role="img" aria-label="עומק המחסנית אחרי כל תו"><line class="axis" x1="${X0}" x2="${W - X0}" y1="${BASE}" y2="${BASE}"/>`;
        for (let d = 1; d <= dmax; d++) { const y = BASE - (d / dmax) * (BASE - 10); c += `<line class="grid" x1="${X0}" x2="${W - X0}" y1="${f(y)}" y2="${f(y)}"/><text class="tick" x="${W - X0 + 2}" y="${f(y + 3)}" font-size="8">${d}</text>`; }
        depths.slice(0, st.k).forEach((d, i) => {
          const h = (d / dmax) * (BASE - 10);
          const cls = i === failAt ? "by-enum" : "by-multiples";
          c += `<rect class="bar ${cls}" x="${f(X0 + i * slot + (slot - bw) / 2)}" y="${f(BASE - h)}" width="${f(bw)}" height="${f(h)}"><title>אחרי התו ${i + 1} : עומק ${d}</title></rect>`;
        });
        if (s.length <= 24) [...s].forEach((ch, i) => { c += `<text class="tick" x="${f(X0 + (i + 0.5) * slot)}" y="${BASE + 12}" text-anchor="middle" font-size="9">${esc(ch)}</text>`; });
        $(".br-chart").innerHTML = c + "</svg>";
        $(".ex-pos").textContent = `תו ${st.k} מתוך ${s.length}`;
        let step;
        if (!fr) step = s.length ? "לפני התו הראשון המחסנית ריקה." : "המחרוזת הריקה תקינה : אין מה לפתוח ואין מה לסגור.";
        else if (fr.action === "push") step = `התו ${ltr(esc(fr.ch))} פותח, ולכן נדחף למחסנית.`;
        else if (fr.action === "pop") step = `התו ${ltr(esc(fr.ch))} סוגר, בראש המחסנית ${ltr(esc(BRACKET_OF[fr.ch]))} מאותו סוג, ולכן מוציאים אותו.`;
        else if (fr.action === "mismatch") step = `<span class="br-bad">✗ התו ${ltr(esc(fr.ch))} סוגר ${NAMES[BRACKET_OF[fr.ch]]}, אבל בראש המחסנית ${ltr(esc(fr.top))} : הסוגר שנפתח אחרון עוד לא נסגר. סוג לא מתאים או סדר לא נכון.</span>`;
        else step = `<span class="br-bad">✗ התו ${ltr(esc(fr.ch))} סוגר, אבל המחסנית ריקה : אין לו סוגר פותח.</span>`;
        if (st.k >= total && tr.fail && tr.fail.kind === "unclosed") step += ` <span class="br-bad">✗ המחרוזת נגמרה והמחסנית לא ריקה : ${ltr(esc(tr.fail.left))} לא נסגרו.</span>`;
        if (st.k >= total && tr.valid && s.length) step += ` <span class="br-ok">✓ כל התווים נקראו והמחסנית ריקה : המחרוזת תקינה.</span>`;
        $(".br-step").innerHTML = step;
        $(".br-sum").innerHTML = (tr.valid ? `<span class="br-ok">תקינה ✓</span>` : `<span class="br-bad">לא תקינה ✗</span>`) +
          (tr.odd ? `, ואפשר לדעת את זה מיד : האורך ${ltr(s.length)} אי-זוגי, והקוד עוצר לפני המחסנית.` : ".") +
          ` העומק המרבי של המחסנית : ${ltr(Math.max(0, ...depths))}.`;
      };
      const total = () => bracketsTrace(st.s).frames.length;
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const setS = (s) => { stop(); st.s = bracketsClean(s).slice(0, 40); st.k = 0; draw(); };
      input.addEventListener("input", () => { const v = bracketsClean(input.value).slice(0, 40); if (v !== input.value) input.value = v; setS(v); });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { setS(b.dataset.s); st.k = total(); draw(); }));
      const PAGE = st.s;
      $(".ex-reset").addEventListener("click", () => setS(PAGE));
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= total()) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { brackets: bracketsView },
    help: {
      brackets: "מקלידים מחרוזת סוגריים : ״הצעד הבא״ ו״הפעלה״ קוראים תו אחרי תו, המחסנית וגרף העומק מתעדכנים, והכישלון הראשון מסומן עם הסיבה.",
    },
    models: { bracketsClean, bracketsTrace },
  });
})();
