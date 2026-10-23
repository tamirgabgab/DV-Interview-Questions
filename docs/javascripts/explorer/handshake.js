// kinds: handshake
//   handshake              0038        req and ack drawn cell by cell; the four rules checked every cycle, a failure marked on its assertion's row
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, ltr, waveStrip } = dvqExplorers.lib;

  // Handshake (0038): the page's reference model on sampled values (index = cycle); the
  // cycle at which each rule fails is the cycle at which the SVA reports it.
  const hsCheck = (req, ack, maxWait = 3) => {
    const n = req.length, fails = { hold: [], late: [], orphan: [], drop: [] };
    for (let t = 0; t < n; t++) {
      const prevReq = t ? req[t - 1] : 0, prevAck = t ? ack[t - 1] : 0;
      if (t && prevReq && !prevAck && !req[t]) fails.hold.push(t);
      if (req[t] && !prevReq) {
        const window = ack.slice(t + 1, t + 1 + maxWait);
        if (window.length === maxWait && !window.some((v) => v)) fails.late.push(t + maxWait);
      }
      if (ack[t] && !req[t]) fails.orphan.push(t);
      if (t && prevAck && req[t]) fails.drop.push(t);
    }
    return fails;
  };
  // The page's four traces as WaveDrom strings; a wave string expanded to n cycles.
  const HS_PRESETS = {
    ok: ["01..0...", "0..10..."],
    late: ["01....0.", "0....10."],
    drop: ["01.0....", "0......."],
    orphan: ["0.......", "0.10...."],
  };
  const hsWave = (text, n) => {
    const out = [];
    for (let i = 0; i < n; i++) { const c = text[i]; out.push(c === undefined || c === "." ? (out.length ? out[out.length - 1] : 0) : Number(c)); }
    return out;
  };

  // The handshake box (0038): draw req and ack cell by cell on a timing strip; the four
  // rules of the page's reference model are evaluated every cycle, a failure marked on
  // the row of its assertion at the cycle the SVA reports it; the page's traces as presets.
  const handshakeView = () => ({
    mount(box) {
      const N = 12, MAX_WAIT = 3;
      const RULES = [
        ["hold", "a_req_holds", "חוק 1, req מחזיק"],
        ["late", "a_ack_in_time", "חוק 2, ack בזמן"],
        ["orphan", "a_no_orphan_ack", "חוק 3, אין ack יתום"],
        ["drop", "a_req_drops", "חוק 4, req יורד אחרי ack"],
      ];
      const st = { req: hsWave(HS_PRESETS.ok[0], N), ack: hsWave(HS_PRESETS.ok[1], N), cur: 3 };
      box.innerHTML =
        `<div class="ex-controls"><span class="wv-presets">הדיאגרמות שבעמוד : ` +
        `<button type="button" class="md-button ex-preset" data-p="ok">עסקה תקינה</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="late">ack מאוחר</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="drop">req נופל</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="orphan">ack יתום</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="clear">ניקוי</button></span></div>` +
        `<p class="wv-hint">לחיצה על משבצת של ${code("req")} או ${code("ack")} הופכת את הערך שלה באותו מחזור. ✗ בשורה של assertion הוא המחזור שבו היא מדווחת על כישלון.</p>` +
        `<div class="wv-wrap" tabindex="0" role="group" aria-label="דיאגרמת תזמון של לחיצת הידיים וארבע שורות ה-assertions, גלילה אופקית"></div>` +
        `<p class="wv-step" aria-live="polite"></p><p class="ex-summary wv-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const draw = () => {
        const fails = hsCheck(st.req, st.ack, MAX_WAIT);
        const rows = [
          { name: "clk", kind: "clock" },
          { name: "req", kind: "bit", values: st.req, cls: "wv-s1", cells: (k) => `מחזור ${k} : req = ${st.req[k]}, לחיצה הופכת` },
          { name: "ack", kind: "bit", values: st.ack, cls: "wv-s3", cells: (k) => `מחזור ${k} : ack = ${st.ack[k]}, לחיצה הופכת` },
        ].concat(RULES.map(([key, name]) => ({ name, kind: "flag", values: st.req.map((_, k) => (fails[key].includes(k) ? 1 : 0)) })));
        $(".wv-wrap").innerHTML = waveStrip(rows, N, { role: "group", label: "דיאגרמת תזמון", labelW: 130, cursor: st.cur, ticks: (k) => k });
        const t = st.cur, req = st.req, ack = st.ack;
        const prevReq = t ? req[t - 1] : 0, prevAck = t ? ack[t - 1] : 0;
        const lines = [];
        if (t && prevReq && !prevAck) lines.push(`חוק 1 : במחזור ${ltr(t - 1)} ‏${code("req")} היה גבוה בלי ${code("ack")}, ולכן ${code("req")} חייב להישאר גבוה עכשיו : ` + (req[t] ? `<span class="wv-ok">✓</span>` : `<span class="wv-bad">✗ ${code("req")} נפל לפני ${code("ack")}</span>`));
        if (req[t] && !prevReq) {
          const win = ack.slice(t + 1, t + 1 + MAX_WAIT);
          lines.push(`חוק 2 : ${code("req")} עלה עכשיו (‏${code("$rose(req)")}), ולכן ${code("ack")} חייב להגיע במחזורים ${ltr(`${t + 1}..${t + MAX_WAIT}`)} : ` +
            (win.some((v) => v) ? `<span class="wv-ok">✓ מגיע במחזור ${ltr(t + 1 + win.findIndex((v) => v))}</span>` : win.length < MAX_WAIT ? `החלון עוד פתוח בסוף הרצף` : `<span class="wv-bad">✗ החלון נסגר בלי ack, הכישלון מדווח במחזור ${ltr(t + MAX_WAIT)}</span>`));
        }
        if (fails.late.includes(t)) lines.push(`חוק 2 : כאן נסגר החלון של העלייה במחזור ${ltr(t - MAX_WAIT)} בלי ${code("ack")} : <span class="wv-bad">✗ ack מאוחר</span>`);
        if (ack[t]) lines.push(`חוק 3 : ${code("ack")} גבוה, ולכן ${code("req")} חייב להיות גבוה באותה דגימה : ` + (req[t] ? `<span class="wv-ok">✓</span>` : `<span class="wv-bad">✗ ack יתום</span>`));
        if (t && prevAck) lines.push(`חוק 4 : במחזור ${ltr(t - 1)} היה ${code("ack")}, ולכן ${code("req")} חייב להיות נמוך עכשיו : ` + (!req[t] ? `<span class="wv-ok">✓</span>` : `<span class="wv-bad">✗ req נשאר גבוה אחרי ack</span>`));
        $(".wv-step").innerHTML = `מחזור ${ltr(t)} : ${ltr(`req = ${req[t]}, ack = ${ack[t]}`)}. ` + (lines.length ? lines.join(" ") : `אף property לא נבדקת במחזור הזה (אין אנטצדנט).`);
        const total = RULES.reduce((a, [key]) => a + fails[key].length, 0);
        $(".wv-sum").innerHTML = total === 0
          ? `<span class="wv-ok">כל ארבע ה-properties מרוצות ✓</span>` + (req.some((v) => v) ? "" : ` (ובלי אף ${code("req")} הן מרוצות באופן ריק : vacuous pass)`)
          : `<span class="wv-bad">${ltr(total)} ${total === 1 ? "הפרה" : "הפרות"} :</span> ` + RULES.filter(([key]) => fails[key].length).map(([key, name, heb]) => `${heb} (${code(name)}) במחזור${fails[key].length > 1 ? "ים" : ""} ${ltr(fails[key].join(", "))}`).join("; ") + `.`;
      };
      const wrap = $(".wv-wrap");
      const tap = (c) => {
        const k = Number(c.dataset.k), row = c.getAttribute("aria-label").includes("req") ? st.req : st.ack;
        row[k] = row[k] ? 0 : 1; st.cur = k; draw();
      };
      wrap.addEventListener("click", (e) => { const c = e.target.closest(".wv-cell"); if (c) tap(c); });
      wrap.addEventListener("keydown", (e) => {
        const c = e.target.closest(".wv-cell");
        if (c && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); tap(c); }
      });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => {
        const p = b.dataset.p;
        if (p === "clear") { st.req = new Array(N).fill(0); st.ack = new Array(N).fill(0); st.cur = 0; }
        else { st.req = hsWave(HS_PRESETS[p][0], N); st.ack = hsWave(HS_PRESETS[p][1], N); const fl = hsCheck(st.req, st.ack, MAX_WAIT); const first = Object.values(fl).flat().sort((a, b) => a - b)[0]; st.cur = first === undefined ? 3 : first; }
        draw();
      }));
      draw();
    },
  });

  dvqExplorers.register({
    views: { handshake: handshakeView },
    help: {
      handshake: "לוחצים על משבצות של req ו-ack ברצועה : ארבעת הכללים נבדקים בכל מחזור, וכישלון מסומן בשורת ה-assertion שלו. ה-presets טוענים את ארבע הדוגמאות של העמוד. ״העתקת WaveDrom״ מעתיקה את הרצועה כ-JSON.",
    },
    models: { hsCheck, HS_PRESETS, hsWave },
  });
})();
