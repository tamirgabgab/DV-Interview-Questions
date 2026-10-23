// kinds: abmap
//   abmap                  0005        the 45 digit pairs a < b for one x: the length of the smallest multiple or ✗, the answer, x = 2^s 5^t m and the rule of the theorem
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { X0, ltr } = dvqExplorers.lib;

  // Two general digits a < b (0005 follow-up): the page's smallest_ab_multiple (the BFS
  // without frames, for every pair at once) and has_ab_solution with the rule of the
  // theorem that decided, for the map of the 45 pairs.
  const abMultiple = (x, a, b) => {
    const parent = new Int32Array(x).fill(-1), digit = new Int8Array(x), visited = new Uint8Array(x), queue = new Int32Array(x);
    let head = 0, tail = 0;
    for (const d of [a, b]) if (d > 0 && !visited[d % x]) { visited[d % x] = 1; digit[d % x] = d; queue[tail++] = d % x; }
    while (head < tail && !visited[0]) {
      const r = queue[head++];
      for (const d of [a, b]) {
        const nr = (r * 10 + d) % x;
        if (!visited[nr]) { visited[nr] = 1; parent[nr] = r; digit[nr] = d; queue[tail++] = nr; }
      }
    }
    if (!visited[0]) return { answer: null, dequeues: head };
    const out = [];
    for (let r = 0; r !== -1; r = parent[r]) out.push(digit[r]);
    return { answer: out.reverse().join(""), dequeues: head };
  };
  const abExists = (x, a, b) => {
    let m = x, s = 0, t = 0, halvings = 0;
    while (m % 2 === 0) { m /= 2; s++; }
    while (m % 5 === 0) { m /= 5; t++; }
    const out = (ok, rule) => ({ ok, rule, s, t, m, halvings, a2: a, b2: b });
    if (a === 0) return out(true, "zero");
    if (s > 0 && t > 0) return out(false, "ten");
    if (t > 0) {
      if (a !== 5 && b !== 5) return out(false, "no5");
      if (t === 1) return out(true, "five");
      if (t === 2) return (a === 2 && b === 5) || (a === 5 && b === 7) ? out(true, "twentyfive") : out(false, "no25");
      return out(false, "no125");
    }
    if (s === 0) return out(true, "coprime");
    let a2 = a, b2 = b, s2 = s;
    while (s2 > 0 && a2 % 2 === 0 && b2 % 2 === 0) { a2 /= 2; b2 /= 2; s2--; halvings++; }
    const res = s2 === 0 ? { ok: true, rule: "halved" } : a2 % 2 !== b2 % 2 ? { ok: true, rule: "mixed" } : { ok: false, rule: "odd" };
    return { ...res, s, t, m, halvings, a2, b2 };
  };

  // The brackets box (0010): a typed string of brackets (other characters are dropped),
  // the characters as cells with the one being read marked, the stack as a column that
  // grows and shrinks, the depth chart, and the first failure circled with its reason.
  // The 45 digit pairs a < b for one x (0005 follow-up): a triangle of cells, rows a = 0..8
  // and columns b = 1..9, each the length of the smallest multiple or ✗; a click shows the
  // answer, x = 2^s 5^t m and the rule of the theorem, and both functions are compared.
  const abmapView = () => ({
    mount(box) {
      const xmax = Number(box.dataset.xmax || 9999), X0 = Number(box.dataset.x || 28);
      const st = { x: X0, a: 1, b: 2 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>‏x</span><input type="number" class="ex-num ab-x" min="1" max="${xmax}" step="1" value="${st.x}" dir="ltr" inputmode="numeric" aria-label="המספר x, מ-1 עד ${xmax}"></label>` +
        `<span class="bf-presets">דוגמאות : ` + [7, 28, 40, 75, 125, 9999].filter((v) => v <= xmax).map((v) => `<button type="button" class="md-button ex-preset" data-x="${v}">${v}</button>`).join(" ") + `</span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err ab-err"></span></div>` +
        `<span class="viz-legend"><span><i class="ab-ok-key"></i>יש פתרון : מספר הספרות</span><span><i class="ab-no-key"></i>✗ אין פתרון</span></span>` +
        `<div class="ab-grid" dir="ltr" role="group" aria-label="45 זוגות הספרות : שורה לכל a, עמודה לכל b"></div>` +
        `<p class="ex-summary ab-sum"></p><p class="ab-detail" aria-live="polite"></p><p class="ex-note ab-rule"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const pow = (p, e) => (e === 0 ? "" : e === 1 ? `${p}` : `${p}<sup>${e}</sup>`);
      const factors = (e) => { const parts = [pow(2, e.s), pow(5, e.t), e.m > 1 ? String(e.m) : ""].filter(Boolean); return parts.length ? parts.join(" · ") : "1"; };
      const times = (h) => (h === 1 ? "חציה אחת" : `${h} חציות`);
      const reason = (e, a, b) => {
        const x = ltr(st.x);
        switch (e.rule) {
          case "zero": return `עם הספרה 0 תמיד יש פתרון` + (e.s || e.t ? ` : ${ltr(b)} ואחריו אפסים מתחלק ב-${ltr(factors({ ...e, m: 1 }))}` : "") +
            (e.m > 1 ? `, וחזרות על הבלוק משלימות את ${ltr(e.m)}` : "") + ` (שלבים 3 ו-4 בהוכחה).`;
          case "coprime": return `${x} זר ל-10, ולכן לכל זוג ספרות יש פתרון (שלב 3 בהוכחה).`;
          case "ten": return `${x} מתחלק ב-10, ובלי הספרה 0 אף מספר לא מסתיים ב-0 (שלב 7 בהוכחה).`;
          case "no5": return `${x} מתחלק ב-5, ובלי 0 ו-5 אף מספר לא מסתיים ב-0 או ב-5 (שלב 6 בהוכחה).`;
          case "five": return `${x} מתחלק ב-5 פעם אחת בלבד, והספרה 5 בסוף המספר מספיקה (שלב 6 בהוכחה).`;
          case "twentyfive": return `${x} מתחלק ב-25, והסיומת ${ltr(a === 2 ? 25 : 75)} בנויה מהספרות (שלב 6 בהוכחה).`;
          case "no25": return `${x} מתחלק ב-25, והסיומות 25 ו-75 דורשות את הזוג ${ltr("{2, 5}")} או ${ltr("{5, 7}")} (שלב 6 בהוכחה).`;
          case "no125": return `${x} מתחלק ב-125, ולכל סיומת של 125 (${ltr("125, 375, 625, 875")}) יש שלוש ספרות שונות (שלב 6 בהוכחה).`;
          case "mixed": return `${e.halvings ? `אחרי ${times(e.halvings)} של הספרות נשארו ${ltr(e.a2)} ו-${ltr(e.b2)} : ` : ""}הספרות בזוגיות שונה, ולכן לכל חזקה של 2 יש כפולה (שלב 5 בהוכחה).`;
          case "halved": return `שתי הספרות זוגיות, ואחרי ${times(e.halvings)} של הספרות לא נשארת חזקה של 2 לטפל בה : ${ltr(factors({ ...e, t: 0, m: 1 }))} מטופל כולו (שלב 5 בהוכחה).`;
          default: return `${e.halvings ? `אחרי ${times(e.halvings)} של הספרות נשארו ${ltr(e.a2)} ו-${ltr(e.b2)} : ` : ""}שתי הספרות אי-זוגיות, ולכן כל מספר מהן אי-זוגי ולא מתחלק ב-${ltr(2 ** (e.s - e.halvings))} (שלב 5 בהוכחה).`;
        }
      };
      let cells = {};
      const draw = () => {
        cells = {};
        let html = `<span class="ab-head ab-corner">a \\ b</span>`;
        for (let b = 1; b <= 9; b++) html += `<span class="ab-head">${b}</span>`;
        let solved = 0, agree = 0, longest = null;
        for (let a = 0; a <= 8; a++) {
          html += `<span class="ab-head">${a}</span>`;
          for (let b = 1; b <= 9; b++) {
            if (b <= a) { html += `<span class="ab-void"></span>`; continue; }
            const r = abMultiple(st.x, a, b), e = abExists(st.x, a, b), ok = r.answer !== null;
            cells[`${a}${b}`] = { r, e };
            if (ok) { solved++; if (!longest || r.answer.length > longest.len) longest = { len: r.answer.length, a, b }; }
            if (ok === e.ok) agree++;
            const sel = a === st.a && b === st.b;
            html += `<button type="button" class="ab-cell ${ok ? "ab-ok" : "ab-no"}${sel ? " is-sel" : ""}" data-a="${a}" data-b="${b}" aria-pressed="${sel}" ` +
              `aria-label="${a} ו-${b} : ${ok ? `${r.answer.length} ספרות` : "אין פתרון"}">${ok ? r.answer.length : "✗"}</button>`;
          }
        }
        $(".ab-grid").innerHTML = html;
        box.querySelectorAll(".ab-cell").forEach((c) => c.addEventListener("click", () => { st.a = Number(c.dataset.a); st.b = Number(c.dataset.b); draw(); }));
        $(".ab-sum").innerHTML = `עבור ${ltr(`x = ${st.x}`)} : ל-${ltr(solved)} מתוך 45 הזוגות יש פתרון` +
          (longest ? `, והתשובה הארוכה ביותר היא בת ${ltr(longest.len)} ספרות (הספרות ${ltr(longest.a)} ו-${ltr(longest.b)}).` : ".") +
          (agree === 45 ? ` ה-BFS ובדיקת הקיום מסכימים בכל 45 התאים ✓.` : ` <span class="wv-bad">✗ ה-BFS ובדיקת הקיום חלוקים ב-${ltr(45 - agree)} תאים.</span>`);
        const { r, e } = cells[`${st.a}${st.b}`];
        const ans = r.answer;
        $(".ab-detail").innerHTML = `הספרות ${ltr(st.a)} ו-${ltr(st.b)} : ` + (ans !== null
          ? `הכפולה הקטנה ביותר של ${ltr(st.x)} היא <span class="ab-ans" dir="ltr">${ans}</span> ${ans.length > 1 ? `(${ltr(ans.length)} ספרות` : "(ספרה אחת"}, ה-BFS הוציא ${ltr(r.dequeues)} שאריות מהתור).`
          : `<b>אין כפולה.</b> ה-BFS הוציא ${ltr(r.dequeues)} שאריות מהתור, והתור התרוקן בלי שארית 0.`);
        $(".ab-rule").innerHTML = `הפירוק : ${ltr(`${st.x} = ${factors(e)}`)}, כלומר ${ltr(`s = ${e.s}, t = ${e.t}, m = ${e.m}`)}. ${reason(e, st.a, st.b)} ` +
          (e.ok === (ans !== null) ? "בדיקת הקיום מסכימה עם ה-BFS ✓." : `<span class="wv-bad">✗ בדיקת הקיום אומרת ${e.ok ? "שיש" : "שאין"} פתרון.</span>`);
      };
      const setX = (v) => {
        const x = Math.round(Number(v));
        const err = !Number.isFinite(x) || x < 1 || x > xmax ? `מספר שלם מ-1 עד ${xmax}` : "";
        $(".ab-err").textContent = err;
        if (err) return;
        st.x = x; $(".ab-x").value = x; draw();
      };
      $(".ab-x").addEventListener("change", () => setX($(".ab-x").value));
      $(".ab-x").addEventListener("keydown", (ev) => { if (ev.key === "Enter") setX($(".ab-x").value); });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => setX(b.dataset.x)));
      $(".ex-reset").addEventListener("click", () => { st.a = 1; st.b = 2; setX(X0); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { abmap: abmapView },
    help: {
      abmap: "בוחרים x ורואים את כל 45 זוגות הספרות a < b : בתא ירוק אורך הכפולה הקטנה ביותר, ו-✗ כשאין. לחיצה על תא מציגה את התשובה, את הפירוק x = 2^s · 5^t · m ואת הכלל של המשפט, ושתי הפונקציות של העמוד מושוות בכל תא.",
    },
    models: { abMultiple, abExists },
  });
})();
