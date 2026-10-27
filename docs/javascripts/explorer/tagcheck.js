// kinds: tagcheck
//   tagcheck               0057        n tags sent, the responses back in a seeded order with tags dropped or doubled (a click on a tag, or a preset); the accumulators (XOR, XOR per bit, sum, sum of squares, the count out) updated response by response; at the end what each method finds and where it is wrong; a quiz that hides the fault
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, code, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Missing tags (0057): the accumulators of every tag sent and returned, and what each
  // method of the page reads from them: XOR (one missing), the split on the lowest bit of
  // x (two missing), the sums (one missing, one twice), the power sums with k = the count
  // still out (Newton's identities, the roots among 0..n-1).
  const tcAcc = (sent, ret, w) => {
    let x = 0, s = 0, q = 0;
    const part = Array(w).fill(0);
    for (const t of [...sent, ...ret]) {
      x ^= t;
      for (let j = 0; j < w; j++) if ((t >> j) & 1) part[j] ^= t;
    }
    sent.forEach((t) => { s += t; q += t * t; });
    ret.forEach((t) => { s -= t; q -= t * t; });
    return { x, part, s, q, out: sent.length - ret.length };
  };
  const tcK = (sent, ret, k, n) => {
    const p = [0];
    for (let i = 1; i <= k; i++) p.push(sent.reduce((a, t) => a + t ** i, 0) - ret.reduce((a, t) => a + t ** i, 0));
    const e = [1];
    for (let i = 1; i <= k; i++) {
      let v = 0;
      for (let j = 1; j <= i; j++) v += (j % 2 ? 1 : -1) * e[i - j] * p[j];
      e.push(Math.floor(v / i));
    }
    const out = [];
    for (let z = 0; z < n; z++) { let v = 0; for (let i = 0; i <= k; i++) v = v * z + (i % 2 ? -e[i] : e[i]); if (v === 0) out.push(z); }
    return out;
  };
  const tcDecode = (sent, ret, w, n) => {
    const a = tcAcc(sent, ret, w), r = { ...a, one: a.x, two: null, sums: null, k: null, bit: null };
    if (a.x) {
      const j = Math.log2(a.x & -a.x), m = a.part[j];
      r.bit = j; r.two = [m, a.x ^ m].sort((u, v) => u - v);
    }
    if (a.s) { const tot = Math.floor(a.q / a.s); r.sums = [Math.floor((tot + a.s) / 2), Math.floor((tot - a.s) / 2)]; }   // floor, as Python's //
    if (a.out > 0) r.k = tcK(sent, ret, a.out, n);
    return r;
  };

  const CASES = { none: "בלי תקלה", one: "אחד חסר", two: "שניים חסרים", dup: "חסר אחד וכפול אחד", three: "שלושה חסרים" };
  const preset = (c, n, rng) => {
    const f = Array(n).fill(0), pick = () => { let t; do t = Math.floor(rng() * n); while (f[t]); return t; };
    const miss = { one: 1, two: 2, dup: 1, three: 3 }[c] || 0;
    for (let i = 0; i < miss; i++) f[pick()] = 1;
    if (c === "dup") f[pick()] = 2;
    return f;
  };
  const PAGE = { two: [5, 12], one: [4], three: [1, 8, 14], dup: [7] };

  const tagcheckView = () => ({
    mount(box) {
      const d0 = { n: Number(box.dataset.n || 16), c: box.dataset.case || "two" };
      const st = { n: d0.n, c: d0.c, f: [], order: [], k: 0, quiz: false, solved: false, rng: null };
      const W = () => Math.log2(st.n);
      const pageFaults = () => {
        const f = Array(st.n).fill(0);
        (PAGE[st.c] || []).filter((t) => t < st.n).forEach((t) => { f[t] = 1; });
        if (st.c === "dup") f[3 % st.n] = 2;
        return f;
      };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>tags <select class="tc-n" aria-label="כמה tags">${[8, 16, 32].map((v) => `<option value="${v}">${v}</option>`).join("")}</select></label>` +
        `<label>התקלה <select class="tc-case" aria-label="התרחיש">${Object.entries(CASES).map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}<option value="custom">בחירה בלחיצה</option></select></label>` +
        `<button type="button" class="md-button tc-shuffle">סדר חדש</button><span class="tc-anchor"></span>` +
        `<label><input type="checkbox" class="tc-quiz"> חידה : התקלה מוסתרת</label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">לפני התשובות</button>` +
        `<button type="button" class="md-button ex-prev">התשובה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">התשובה הבאה</button>` +
        `<button type="button" class="md-button ex-end">כל התשובות</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(900, 400, 120) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary tc-sum" aria-live="polite"></p>` +
        `<div class="tc-tags" role="group" aria-label="ה-tags : לחיצה מסמנת tag שלא יחזור או שיחזור פעמיים"></div>` +
        `<span class="viz-legend"><span><i class="tc-key-out"></i>נשלח, עוד לא חזר</span><span><i class="tc-key-back"></i>חזר</span><span><i class="tc-key-twice"></i>חזר פעמיים</span><span><i class="tc-key-last"></i>התשובה האחרונה</span></span>` +
        `<div class="tc-acc"></div>` +
        `<div class="ex-controls tc-guessrow" hidden><label><span>החסרים</span><input type="text" class="ex-num tc-guess" data-nolink dir="ltr" placeholder="5, 12" aria-label="ה-tags החסרים, מופרדים בפסיקים"></label>` +
        `<label><span>הכפול</span><input type="text" class="ex-num tc-gdup" data-nolink dir="ltr" placeholder="—" aria-label="ה-tag שחזר פעמיים, אם יש"></label>` +
        `<button type="button" class="md-button md-button--primary tc-check">בדיקה</button><button type="button" class="md-button tc-show">הצגת התקלה</button></div>` +
        `<div class="tc-decode" data-steady></div>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const sent = () => Array.from({ length: st.n }, (_, t) => t);
      const returned = () => { const r = []; st.f.forEach((v, t) => { if (v !== 1) r.push(t); if (v === 2) r.push(t); }); return r; };
      const shuffle = (rng) => {
        const r = returned();
        for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(rng() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; }
        st.order = r;
      };
      const hidden = () => st.quiz && !st.solved;
      const bin = (v) => v.toString(2).padStart(W(), "0");

      const draw = () => {
        const n = st.n, w = W(), R = st.order.length;
        st.k = Math.min(st.k, R);
        $(".tc-n").value = String(n); $(".tc-case").value = st.c; $(".tc-quiz").checked = st.quiz;
        $(".tc-guessrow").hidden = !st.quiz;
        const back = st.order.slice(0, st.k), last = st.k ? st.order[st.k - 1] : null;
        const cnt = Array(n).fill(0); back.forEach((t) => { cnt[t]++; });
        $(".ex-pos").textContent = `תשובה ${st.k} מתוך ${R}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === R;
        const miss = st.f.map((v, t) => (v === 1 ? t : -1)).filter((t) => t >= 0), dups = st.f.map((v, t) => (v === 2 ? t : -1)).filter((t) => t >= 0);
        $(".tc-sum").innerHTML = `${ltr(n)} tags של ${ltr(w)} ביטים נשלחו, ${ltr(R)} תשובות בסדר אקראי. ` +
          (hidden() ? "התקלה מוסתרת : מצאו אותה מהמצברים." : `${miss.length ? `חסרים ${ltr(miss.join(", "))}` : "אף tag לא חסר"}${dups.length ? `, ‏${ltr(dups.join(", "))} חוזר פעמיים` : ""}.`);
        $(".tc-tags").innerHTML = Array.from({ length: n }, (_, t) => {
          const cls = cnt[t] >= 2 ? "is-twice" : cnt[t] === 1 ? "is-back" : "is-out";
          const mark = hidden() ? "" : st.f[t] === 1 ? `<span class="tc-f">✗</span>` : st.f[t] === 2 ? `<span class="tc-f">×2</span>` : "";
          return `<button type="button" class="tc-tag ${cls}${t === last ? " is-last" : ""}" data-t="${t}" title="tag ${t}"${hidden() ? " disabled" : ""}><b>${t}</b><small>${bin(t)}</small>${mark}</button>`;
        }).join("");
        const a = tcAcc(sent(), back, w);
        const hl = (j) => last !== null && ((last >> j) & 1);
        $(".tc-acc").innerHTML = `<table class="tc-table"><thead><tr><th>המצבר</th><th>בבינארי</th><th>ערך</th></tr></thead><tbody>` +
          `<tr${last !== null ? ' class="is-hit"' : ""}><td>${code("x")} : XOR של הכול</td><td dir="ltr"><code>${bin(a.x)}</code></td><td>${ltr(a.x)}</td></tr>` +
          a.part.map((v, j) => `<tr${hl(j) ? ' class="is-hit"' : ""}><td>${code(`part[${j}]`)} : ביט ${ltr(j)} דולק</td><td dir="ltr"><code>${bin(v)}</code></td><td>${ltr(v)}</td></tr>`).join("") +
          `<tr${last !== null ? ' class="is-hit"' : ""}><td>${code("s")} : סכום, נשלח פחות חזר</td><td></td><td>${ltr(a.s)}</td></tr>` +
          `<tr${last !== null ? ' class="is-hit"' : ""}><td>${code("q")} : סכום ריבועים</td><td></td><td>${ltr(a.q)}</td></tr>` +
          `<tr${last !== null ? ' class="is-hit"' : ""}><td>${code("out")} : מונה</td><td></td><td>${ltr(a.out)}</td></tr></tbody></table>` +
          `<p class="ex-note">${last === null ? "לפני התשובה הראשונה : המצברים מכילים את כל מה שנשלח." : `התשובה האחרונה ${code(String(last))} = ${code(bin(last))} : היא נכנסה ל-x, ל-s, ל-q, ולכל ${code("part[j]")} שהביט שלו דולק בה.`}</p>`;
        // the end: what each method reads, and whether it is right
        if (st.k < R) { $(".tc-decode").innerHTML = `<p class="ex-note">בסוף כל התשובות יופיע כאן מה כל שיטה מוצאת.</p>`; answer(box, null); return; }
        const d = tcDecode(sent(), st.order, w, n);
        const same = (u, v) => JSON.stringify([...u].sort((x, y) => x - y)) === JSON.stringify([...v].sort((x, y) => x - y));
        const verdict = (ok) => (hidden() ? "" : ok ? ` <span class="wv-ok">✓ נכון</span>` : ` <span class="wv-bad">✗ טועה</span>`);
        const lines = [];
        lines.push(`<p><b>XOR, חסר אחד :</b> ${d.out === 1 ? `‏${code("x")} = ${ltr(d.x)}, החסר ${ltr(d.one)}` : `המונה ${ltr(d.out)}, לא 1 : ${code("x")} = ${ltr(d.x)} לא אומר כלום לבד`}` +
          verdict(d.out === 1 && same([d.one], miss) && !dups.length) + `</p>`);
        if (d.two) {
          const g1 = sent().filter((t) => (t >> d.bit) & 1);
          lines.push(`<p><b>חלוקה לפי ביט :</b> הביט הנמוך שדולק ב-${code("x")} הוא ${ltr(d.bit)}. ‏${code(`part[${d.bit}]`)} = ${ltr(d.part[d.bit])}, ולכן "${ltr(d.two.join(", "))}"` +
            verdict(same(d.two, miss) && !dups.length) + `</p>` +
            `<p class="tc-groups">הקבוצה שהביט ${ltr(d.bit)} שלה 1 : <span dir="ltr">${g1.join(" ")}</span><br>הקבוצה שהביט ${ltr(d.bit)} שלה 0 : <span dir="ltr">${sent().filter((t) => !((t >> d.bit) & 1)).join(" ")}</span></p>`);
        } else lines.push(`<p><b>חלוקה לפי ביט :</b> ‏${code("x")} = 0, אין ביט להתחלק לפיו.${verdict(miss.length === 0 && !dups.length)}</p>`);
        lines.push(`<p><b>סכומים :</b> ${d.sums ? `‏${code("s")} = ${ltr(d.s)}, ‏${code("q")} = ${ltr(d.q)} : החסר ${ltr(d.sums[0])}, הכפול ${ltr(d.sums[1])}` : `‏${code("s")} = 0 : אין חסר וכפול`}` +
          verdict(d.sums ? same([d.sums[0]], miss) && same([d.sums[1]], dups) : !miss.length && !dups.length) + `</p>`);
        lines.push(`<p><b>סכומי חזקות, ‏k = המונה :</b> ${d.k ? `‏k = ${ltr(d.out)}, השורשים ${ltr(d.k.join(", ") || "—")}` : `המונה ${ltr(d.out)} : אין מה לחפש`}` +
          verdict(d.k ? same(d.k, miss) && !dups.length : !miss.length && !dups.length) + `</p>`);
        $(".tc-decode").innerHTML = `<p class="ex-title">מה כל שיטה מוצאת :</p>` + lines.join("");
        if (!hidden()) {
          const best = dups.length ? "רק הסכומים מוצאים חסר וכפול" : miss.length === 1 ? "כל השיטות מסכימות על חסר אחד" : miss.length === 2 ? "החלוקה לפי ביט וסכומי החזקות מוצאות את שניהם" : miss.length ? "רק סכומי החזקות מוצאים את כולם" : "הכול חזר : המונה 0 וכל המצברים 0";
          answer(box, `${best}.`);
        } else answer(box, null);
      };
      const stop = autoplay(play, speed, { step: () => { st.k = Math.min(st.order.length, st.k + 1); draw(); }, done: () => st.k >= st.order.length, restart: () => { st.k = 0; draw(); } });
      const seed = seedControls(box, $(".tc-anchor"), (rng) => {
        stop(); st.rng = rng;
        if (st.quiz) { st.c = ["one", "two", "dup", "three"][Math.floor(rng() * 4)]; st.f = preset(st.c, st.n, rng); st.solved = false; $(".tc-guess").value = ""; $(".tc-gdup").value = ""; }
        shuffle(rng); st.k = 0; draw();
      }, { fresh: false });
      const fresh = () => seed.draw();
      const setCase = () => { stop(); st.f = st.c === "custom" ? st.f : pageFaults(); shuffle(st.rng || dvqExplorers.lib.mulberry32(57)); st.k = 0; draw(); };
      $(".tc-n").addEventListener("change", () => { st.n = Number($(".tc-n").value); if (st.c === "custom") st.f = Array(st.n).fill(0); setCase(); });
      $(".tc-case").addEventListener("change", () => { st.c = $(".tc-case").value; if (st.c === "custom") st.f = Array(st.n).fill(0); setCase(); });
      $(".tc-tags").addEventListener("click", (e) => {
        const b = e.target.closest(".tc-tag");
        if (!b || hidden()) return;
        const t = Number(b.dataset.t);
        st.f[t] = (st.f[t] + 1) % 3;
        st.c = "custom"; stop(); shuffle(st.rng || dvqExplorers.lib.mulberry32(57)); st.k = 0; draw();
      });
      $(".tc-shuffle").addEventListener("click", fresh);
      $(".tc-quiz").addEventListener("change", () => { st.quiz = $(".tc-quiz").checked; st.solved = false; if (st.quiz) fresh(); else { st.c = d0.c; setCase(); } });
      const say = (cls, html) => { const p = document.createElement("p"); p.className = cls; p.innerHTML = html; $(".tc-decode").prepend(p); };
      $(".tc-check").addEventListener("click", () => {
        const list = (v) => v.split(/[\s,]+/).filter(Boolean).map(Number);
        const g = list($(".tc-guess").value), gd = list($(".tc-gdup").value);
        const miss = st.f.map((v, t) => (v === 1 ? t : -1)).filter((t) => t >= 0), dups = st.f.map((v, t) => (v === 2 ? t : -1)).filter((t) => t >= 0);
        const ok = JSON.stringify([...g].sort((a, b) => a - b)) === JSON.stringify(miss) && JSON.stringify([...gd].sort((a, b) => a - b)) === JSON.stringify(dups);
        if (st.k < st.order.length) { draw(); say("wv-bad", "קודם מריצים את כל התשובות : המצברים שלמים רק בסוף."); return; }
        if (ok) { st.solved = true; draw(); say("wv-ok", "✓ נכון."); return; }
        draw(); say("wv-bad", `✗ לא. רמז : המונה ${code("out")} אומר כמה חסרים נטו; כש-${code("out")} = 0 ו-${code("x")} ≠ 0, משהו חזר פעמיים.`);
      });
      $(".tc-show").addEventListener("click", () => { stop(); st.solved = true; st.k = st.order.length; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(0, st.k - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.k = Math.min(st.order.length, st.k + 1); draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = st.order.length; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, { n: d0.n, c: d0.c, quiz: false, solved: false, rng: null }); setCase(); });
      // the faults ride in the link when chosen by click: "m5.12-d3"
      box.dvqExtra = {
        get: () => (st.c !== "custom" ? "" : st.f.map((v, t) => (v === 1 ? `m${t}` : v === 2 ? `d${t}` : "")).filter(Boolean).join(".")),
        set: (text) => {
          const parts = text.split(".");
          if (!parts.every((p) => /^[md]\d{1,2}$/.test(p) && Number(p.slice(1)) < st.n)) return false;
          st.f = Array(st.n).fill(0); parts.forEach((p) => { st.f[Number(p.slice(1))] = p[0] === "m" ? 1 : 2; });
          st.c = "custom"; shuffle(st.rng || dvqExplorers.lib.mulberry32(57)); st.k = 0; draw(); return true;
        },
      };
      setCase();
    },
  });

  dvqExplorers.register({
    views: { tagcheck: tagcheckView },
    help: {
      tagcheck: "כל ה-tags נשלחים, והתשובות חוזרות אחת אחת בסדר אקראי. לחיצה על tag מסמנת שהוא לא יחזור (✗) או שיחזור פעמיים (×2), או שבוחרים תרחיש מוכן. המצברים מתעדכנים בכל תשובה, ובסוף רואים מה כל שיטה מוצאת ואם היא צודקת. במצב חידה התקלה מוסתרת : מריצים את כל התשובות וכותבים מה חסר ומה כפול.",
    },
    models: { tcAcc, tcK, tcDecode },
  });
})();
