// kinds: handshake attempts
//   handshake              0038        req and ack drawn cell by cell; the four rules checked every cycle, a failure marked on its assertion's row
//   attempts               0038        part a: an attempt lane per property, where the antecedent matched, the window as a bracket, and pass, fail, still open or vacuous
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, ltr, stickyNames, waveStrip } = dvqExplorers.lib;
  const NB = "\u00a0";

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

  // The attempts of the page's four properties (part a): at every cycle each property
  // starts an attempt; when its antecedent does not match the attempt passes vacuously
  // at once, otherwise it runs over its window and ends in a pass, a fail, or is still
  // open when the trace ends (a window cut by the end, not reported, as on the page).
  //   hold   (req && !ack) |=> req        window t + 1
  //   late   $rose(req) |-> ##[1:w] ack   window t + 1 .. t + w, passes at the first ack
  //   orphan ack |-> req                  window t
  //   drop   ack |=> !req                 window t + 1
  // A fail ends at the cycle the SVA reports it, the cycle of hsCheck.
  const HS_PROPS = ["hold", "late", "orphan", "drop"];
  const hsAttempts = (req, ack, maxWait = 3) => {
    const n = req.length, out = { hold: [], late: [], orphan: [], drop: [] };
    const next = (key, t, ok) => out[key].push(t + 1 < n ? { t, end: t + 1, status: ok(t + 1) ? "pass" : "fail" } : { t, end: n - 1, status: "open" });
    for (let t = 0; t < n; t++) {
      const prevReq = t ? req[t - 1] : 0;
      if (req[t] && !ack[t]) next("hold", t, (u) => req[u]); else out.hold.push({ t, end: t, status: "vacuous" });
      if (req[t] && !prevReq) {
        let u = t + 1;
        while (u <= t + maxWait && u < n && !ack[u]) u++;
        out.late.push(u <= t + maxWait && u < n ? { t, end: u, status: "pass" } : u > t + maxWait ? { t, end: t + maxWait, status: "fail" } : { t, end: n - 1, status: "open" });
      } else out.late.push({ t, end: t, status: "vacuous" });
      out.orphan.push(ack[t] ? { t, end: t, status: req[t] ? "pass" : "fail" } : { t, end: t, status: "vacuous" });
      if (ack[t]) next("drop", t, (u) => !req[u]); else out.drop.push({ t, end: t, status: "vacuous" });
    }
    return out;
  };

  // The attempt box (0038 part a): the page's traces (or req and ack edited cell by
  // cell) on a strip, and under it one lane per property on the same columns: a dot
  // where the antecedent matched, the window as a bracket to the cycle the attempt ends,
  // ✓, ✗ or … at its end, and the vacuous cycles as small grey dots (a toggle); a cursor
  // cycle with the attempts that start or end there, and a count per property.
  const attemptsView = () => ({
    mount(box) {
      const N = 12, MAX_WAIT = 3, SW = 36, L = 130, RH = 34;
      const PROPS = [
        ["hold", "a_req_holds", "(req && !ack) |=> req", "חוק 1"],
        ["late", "a_ack_in_time", "$rose(req) |-> ##[1:3] ack", "חוק 2"],
        ["orphan", "a_no_orphan_ack", "ack |-> req", "חוק 3"],
        ["drop", "a_req_drops", "ack |=> !req", "חוק 4"],
      ];
      const P0 = HS_PRESETS[box.dataset.preset] ? box.dataset.preset : "late";
      const st = { req: hsWave(HS_PRESETS[P0][0], N), ack: hsWave(HS_PRESETS[P0][1], N), cur: 1, vac: true };
      box.innerHTML =
        `<div class="ex-controls"><span class="wv-presets">הדיאגרמות שבעמוד : ` +
        `<button type="button" class="md-button ex-preset" data-p="ok">עסקה תקינה</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="late">ack מאוחר</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="drop">req נופל</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="orphan">ack יתום</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="clear">ניקוי</button></span>` +
        `<label><input type="checkbox" class="at-vac" checked> להראות vacuous</label></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button ex-prev">המחזור הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">המחזור הבא</button><span class="ex-pos"></span></div>` +
        `<p class="wv-hint">לחיצה על משבצת של ${code("req")} או ${code("ack")} הופכת אותה. בכל מחזור כל property מתחילה ניסיון : נקודה היא אנטצדנט שהתאים, הסוגר הוא החלון, ובסופו ✓, ✗ או … (עוד פתוח).</p>` +
        `<div class="wv-wrap at-wrap" tabindex="0" role="group" aria-label="דיאגרמת התזמון ומסלול ניסיונות לכל property, גלילה אופקית"></div>` +
        `<span class="viz-legend"><span><i class="at-key-start"></i>האנטצדנט התאים</span><span><i class="at-key-pass"></i>עבר</span><span><i class="at-key-fail"></i>נכשל</span><span><i class="at-key-vac"></i>vacuous : האנטצדנט לא התאים</span></span>` +
        `<p class="wv-step at-step" aria-live="polite"></p><div class="at-table"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const X = (k) => L + k * SW + SW / 2;
      const lanes = (att) => {
        const T = 4, H = T + PROPS.length * RH + 4, W = L + N * SW + 6;
        let s = `<svg class="wave-strip at-lanes" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="מסלול ניסיונות לכל אחת מארבע ה-properties">`;
        for (let k = 0; k <= N; k++) s += `<line class="wv-grid" x1="${L + k * SW}" x2="${L + k * SW}" y1="${T}" y2="${H - 4}"/>`;
        s += `<rect class="wv-cursor" x="${L + st.cur * SW}" y="${T}" width="${SW}" height="${H - T - 4}"/>`;
        PROPS.forEach(([key, name], r) => {
          const y0 = T + r * RH;
          s += `<line class="at-sep" x1="${L}" x2="${W - 6}" y1="${y0 + RH}" y2="${y0 + RH}"/><text class="wv-name" x="${L - 8}" y="${y0 + RH / 2 + 4}" text-anchor="end">${name}</text>`;
          let lvl = 0;
          att[key].forEach((a) => {
            if (a.status === "vacuous") { if (st.vac) s += `<circle class="at-vac" cx="${X(a.t)}" cy="${y0 + RH / 2}" r="2.5"><title>מחזור ${a.t} : vacuous</title></circle>`; return; }
            const y = y0 + (lvl ? 23 : 11); lvl = 1 - lvl;
            const cls = a.status === "pass" ? "at-pass" : a.status === "fail" ? "at-fail" : "at-open";
            const xe = X(a.end) + (a.status === "open" ? SW / 2 - 2 : 0);
            s += `<g class="${cls}"><title>ניסיון שהתחיל במחזור ${a.t} : ${a.status === "pass" ? `עבר במחזור ${a.end}` : a.status === "fail" ? `נכשל במחזור ${a.end}` : "עוד פתוח בסוף הרצף"}</title>`;
            if (a.end > a.t || a.status === "open") s += `<path class="at-bracket" d="M${X(a.t)},${y - 4} V${y} H${f1(xe)} V${y - 4}"/>`;
            s += `<circle class="at-start" cx="${X(a.t)}" cy="${y}" r="3.5"/>`;
            const gx = a.end > a.t ? xe : X(a.t) + 10;
            s += `<text class="at-mark" x="${f1(gx)}" y="${y + 4}" text-anchor="middle">${a.status === "pass" ? "✓" : a.status === "fail" ? "✗" : "…"}</text></g>`;
          });
        });
        return stickyNames(s + "</svg>", PROPS.map((p) => p[1]), L, T, RH);
      };
      const f1 = (v) => Number(v).toFixed(1);
      const draw = () => {
        const att = hsAttempts(st.req, st.ack, MAX_WAIT);
        const rows = [
          { name: "clk", kind: "clock" },
          { name: "req", kind: "bit", values: st.req, cls: "wv-s1", cells: (k) => `מחזור ${k} : req = ${st.req[k]}, לחיצה הופכת` },
          { name: "ack", kind: "bit", values: st.ack, cls: "wv-s3", cells: (k) => `מחזור ${k} : ack = ${st.ack[k]}, לחיצה הופכת` },
        ];
        const wrap = $(".at-wrap"), left = wrap.scrollLeft;
        wrap.innerHTML = waveStrip(rows, N, { role: "group", label: "דיאגרמת תזמון", labelW: L, slotW: SW, cursor: st.cur, ticks: (k) => k }) + lanes(att);
        wrap.scrollLeft = left;
        $(".ex-pos").textContent = `מחזור ${st.cur}`;
        $(".ex-prev").disabled = st.cur === 0; $(".ex-next").disabled = st.cur >= N - 1;
        const t = st.cur, said = [];
        PROPS.forEach(([key, name, expr, rule]) => {
          att[key].forEach((a) => {
            if (a.status === "vacuous") return;
            const word = a.status === "pass" ? `<span class="wv-ok">עבר ✓</span>` : a.status === "fail" ? `<span class="wv-bad">נכשל ✗</span>` : "עדיין פתוח בסוף הרצף";
            if (a.t === t) said.push(`${rule}, ${code(expr)}${NB}: האנטצדנט התאים, ` + (a.end === t && a.status !== "open" ? `והקונסקוונט נבדק באותו מחזור${NB}: ${word}.`
              : a.status === "open" ? `והחלון מתחיל במחזור ${ltr(t + 1)}${NB}: ${word}.`
              : key === "late" ? `והחלון הוא המחזורים ${ltr(`${t + 1}..${t + MAX_WAIT}`)}${NB}: ${word} במחזור ${ltr(a.end)}.`
              : `והקונסקוונט נבדק במחזור ${ltr(a.end)}${NB}: ${word}.`));
            else if (a.end === t && a.status !== "open") said.push(`${rule}${NB}: הניסיון שהתחיל במחזור ${ltr(a.t)} ${a.status === "pass" ? "עבר" : "נכשל"} כאן ${a.status === "pass" ? "✓" : "✗"}.`);
          });
        });
        $(".at-step").innerHTML = `מחזור ${ltr(t)}${NB}: ${ltr(`req = ${st.req[t]}, ack = ${st.ack[t]}`)}. ` + (said.length ? said.join(" ") : `אף אנטצדנט לא התאים כאן, וכל ארבעת הניסיונות שהתחילו במחזור הזה עברו באופן ריק (vacuous).`);
        $(".at-table").innerHTML = `<div class="at-scroll" tabindex="0" role="region" aria-label="הספירה לכל חוק"><table class="bridge-table at-counts"><thead><tr><th>החוק</th><th title="האנטצדנט התאים">התאים</th><th>עבר</th><th>נכשל</th><th>פתוח</th><th>‏vacuous</th></tr></thead><tbody>` +
          PROPS.map(([key, name, expr, rule]) => { const c = (s) => att[key].filter((a) => a.status === s).length; return `<tr><td title="${name}">${rule}</td><td>${ltr(N - c("vacuous"))}</td><td>${ltr(c("pass"))}</td><td>${c("fail") ? `<span class="wv-bad">${ltr(c("fail"))}</span>` : ltr(0)}</td><td>${ltr(c("open"))}</td><td>${ltr(c("vacuous"))}</td></tr>`; }).join("") +
          `</tbody></table></div><p class="ex-note">רוב הניסיונות עוברים באופן ריק${NB}: assertion שרק עוברת vacuous לא בדקה כלום, ולכן כדאי לבדוק גם שהאנטצדנט התאים (cover).</p>`;
      };
      const wrap = $(".at-wrap");
      const tap = (c) => { const k = Number(c.dataset.k), row = c.getAttribute("aria-label").includes("req") ? st.req : st.ack; row[k] = row[k] ? 0 : 1; st.cur = k; draw(); };
      wrap.addEventListener("click", (e) => { const c = e.target.closest(".wv-cell"); if (c) tap(c); });
      wrap.addEventListener("keydown", (e) => { const c = e.target.closest(".wv-cell"); if (c && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); tap(c); } });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => {
        const p = b.dataset.p;
        if (p === "clear") { st.req = new Array(N).fill(0); st.ack = new Array(N).fill(0); }
        else { st.req = hsWave(HS_PRESETS[p][0], N); st.ack = hsWave(HS_PRESETS[p][1], N); }
        st.cur = 1; draw();
      }));
      $(".at-vac").addEventListener("change", () => { st.vac = $(".at-vac").checked; draw(); });
      $(".ex-next").addEventListener("click", () => { if (st.cur < N - 1) st.cur++; draw(); });
      $(".ex-prev").addEventListener("click", () => { if (st.cur > 0) st.cur--; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { handshake: handshakeView, attempts: attemptsView },
    help: {
      handshake: "לוחצים על משבצות של req ו-ack ברצועה : ארבעת הכללים נבדקים בכל מחזור, וכישלון מסומן בשורת ה-assertion שלו. ה-presets טוענים את ארבע הדוגמאות של העמוד. ״העתקת WaveDrom״ מעתיקה את הרצועה כ-JSON.",
      attempts: "מתחת לרצועה יש מסלול לכל property : בכל מחזור מתחיל ניסיון, נקודה מסמנת שהאנטצדנט התאים, הסוגר הוא החלון, ובסופו ✓ או ✗. נקודה אפורה היא ניסיון vacuous. ה-presets טוענים את הדיאגרמות של העמוד, לחיצה על משבצת הופכת אותה, ו״המחזור הבא״ מסביר מה קורה בכל מחזור.",
    },
    models: { hsCheck, HS_PRESETS, hsWave, hsAttempts, HS_PROPS },
  });
})();
