// kinds: handshake attempts
//   handshake              0038        part b, the mutation box: rst_n, req and ack drawn cell by cell; the four rules and one trap's variant of a property (MAX_WAIT 1 to 4) checked side by side, a failure marked on its assertion's row, and whether the trace tells the variant from the rule
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
        if (ack[t]) fails.late.push(t);                          // ack in the rise cycle: too early
        else if (window.length === maxWait && !window.some((v) => v)) fails.late.push(t + maxWait);
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

  // The mutation box (0038 part b): one property swapped for a trap's variant, checked
  // side by side with the page's four on the same trace. Every property, the page's and
  // the variants, as attempts with reset: an attempt that matched at t and ends at `end`
  // is disabled when rst_n is low at any cycle t..end (disable iff (!rst_n)), unless the
  // variant drops disable iff. With rst_n high throughout, the page's four give hsCheck.
  //   r4      ack |-> !req                    (trap 1: |-> where |=> was meant)
  //   r2req   req |-> ##[1:w] ack             (req instead of $rose(req))
  //   r2noack $rose(req) |-> ##[1:w] ack      (no !ack: an ack in the rise cycle passes)
  //   nodis   the page's four without disable iff (trap 2)
  const HS_MUTANTS = { r4: "drop", r2req: "late", r2noack: "late", nodis: null };
  const hsProp = (key, req, ack, rst, maxWait = 3, dis = true) => {
    const n = req.length, out = [];
    const win = (t, early) => {                     // ##[1:w] ack after t; early: !ack at t first
      if (early && ack[t]) return { t, end: t, status: "fail" };
      let u = t + 1;
      while (u <= t + maxWait && u < n && !ack[u]) u++;
      return u <= t + maxWait && u < n ? { t, end: u, status: "pass" } : u > t + maxWait ? { t, end: t + maxWait, status: "fail" } : { t, end: n - 1, status: "open" };
    };
    const next = (t, ok) => (t + 1 < n ? { t, end: t + 1, status: ok(t + 1) ? "pass" : "fail" } : { t, end: n - 1, status: "open" });
    for (let t = 0; t < n; t++) {
      const prevReq = t ? req[t - 1] : 0, rose = req[t] && !prevReq;
      let a = null;
      if (key === "hold" && req[t] && !ack[t]) a = next(t, (u) => req[u]);
      else if (key === "late" && rose) a = win(t, true);
      else if (key === "r2noack" && rose) a = win(t, false);
      else if (key === "r2req" && req[t]) a = win(t, false);
      else if (key === "orphan" && ack[t]) a = { t, end: t, status: req[t] ? "pass" : "fail" };
      else if (key === "r4" && ack[t]) a = { t, end: t, status: req[t] ? "fail" : "pass" };
      else if (key === "drop" && ack[t]) a = next(t, (u) => !req[u]);
      if (!a) { out.push({ t, end: t, status: "vacuous" }); continue; }
      if (dis && rst.slice(t, a.end + 1).some((v) => !v)) a = { t, end: a.end, status: "disabled" };
      out.push(a);
    }
    return out;
  };
  const hsFails = (att) => att.filter((a) => a.status === "fail").map((a) => a.end).sort((a, b) => a - b);
  // The page's four with reset (dis: disable iff), and the variant's failures.
  const hsCheckRst = (req, ack, rst, maxWait = 3, dis = true) =>
    Object.fromEntries(HS_PROPS.map((key) => [key, hsFails(hsProp(key, req, ack, rst, maxWait, dis))]));
  const hsMutant = (variant, req, ack, rst, maxWait = 3) => {
    if (variant === "nodis") return [...new Set(Object.values(hsCheckRst(req, ack, rst, maxWait, false)).flat())].sort((a, b) => a - b);
    return hsFails(hsProp(variant, req, ack, rst, maxWait, true));
  };
  // The trap of trap 2 as a preset: req rises at 1, reset at cycles 3 and 4 (req and ack
  // low under reset), so rule 1's attempt at 2 and rule 2's window 1..4 meet the reset.
  const HS_RESET = ["01.0....", "0.......", "111001.."];

  const handshakeView = () => ({
    mount(box) {
      const N = 12;
      const RULES = [
        ["hold", "a_req_holds", "חוק 1", "(req && !ack) |=> req"],
        ["late", "a_ack_in_time", "חוק 2", "$rose(req) |-> !ack ##[1:W] ack"],
        ["orphan", "a_no_orphan_ack", "חוק 3", "ack |-> req"],
        ["drop", "a_req_drops", "חוק 4", "ack |=> !req"],
      ];
      // variant: [the row's name, its expression, the select's text (code isolated LTR)]
      const iso = (t) => `\u2066${t}\u2069`;
      const MUT = {
        r4: [`מוטציה${NB}: חוק 4`, "ack |-> !req", `חוק 4 עם ${iso("|->")} במקום ${iso("|=>")}`],
        r2req: [`מוטציה${NB}: חוק 2`, "req |-> ##[1:W] ack", `חוק 2 עם ${iso("req")} במקום ${iso("$rose(req)")}`],
        r2noack: [`מוטציה${NB}: חוק 2`, "$rose(req) |-> ##[1:W] ack", `חוק 2 בלי ${iso("!ack")} במחזור העלייה`],
        nodis: ["בלי disable iff", "disable iff הוסר", `ארבעת החוקים בלי ${iso("disable iff")}`],
      };
      const d0 = { mut: MUT[box.dataset.mut] ? box.dataset.mut : "r4" };
      const st = { req: hsWave(HS_PRESETS.ok[0], N), ack: hsWave(HS_PRESETS.ok[1], N), rst: new Array(N).fill(1), cur: 3 };
      box.innerHTML =
        `<div class="ex-controls"><span class="wv-presets">הרצף${NB}: ` +
        `<button type="button" class="md-button ex-preset" data-p="ok">עסקה תקינה</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="late">ack מאוחר</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="drop">req נופל</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="orphan">ack יתום</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="reset">reset באמצע</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="clear">ניקוי</button></span></div>` +
        `<div class="ex-controls"><label>המוטציה <select class="hs-mut" aria-label="ה-property שמוחלפת בגרסה של מלכודת">` +
        Object.entries(MUT).map(([v, m]) => `<option value="${v}">${m[2]}</option>`).join("") + `</select></label>` +
        `<label>MAX_WAIT <select class="hs-wait" aria-label="MAX_WAIT, סוף החלון של חוק 2">${[1, 2, 3, 4].map((v) => `<option value="${v}">${v}</option>`).join("")}</select></label></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button ex-prev">המחזור הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">המחזור הבא</button><span class="ex-pos"></span></div>` +
        `<p class="wv-hint">לחיצה על משבצת של ${code("rst_n")}, ${code("req")} או ${code("ack")} הופכת אותה. ✗ בשורה הוא המחזור שבו ה-assertion מדווחת על כישלון; השורה האחרונה היא המוטציה.</p>` +
        `<div class="wv-wrap" tabindex="0" role="group" aria-label="דיאגרמת תזמון של לחיצת הידיים, ארבע שורות ה-assertions ושורת המוטציה, גלילה אופקית"></div>` +
        `<p class="wv-step" aria-live="polite"></p><p class="ex-summary wv-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      $(".hs-mut").value = d0.mut; $(".hs-wait").value = "3";
      const mut = () => $(".hs-mut").value, W = () => Number($(".hs-wait").value);
      const exprOf = (e) => e.replace("W]", `${W()}]`);
      const word = (a) => (a.status === "pass" ? `<span class="wv-ok">✓ במחזור ${ltr(a.end)}</span>` : a.status === "fail" ? `<span class="wv-bad">✗ במחזור ${ltr(a.end)}</span>`
        : a.status === "open" ? "עוד פתוח בסוף הרצף" : `מבוטל${NB}: ${code("rst_n")} נמוך בחלון`);
      const draw = () => {
        const w = W(), v = mut(), dis = v !== "nodis";
        const fails = hsCheckRst(st.req, st.ack, st.rst, w);
        const mf = hsMutant(v, st.req, st.ack, st.rst, w);
        const flag = (list) => st.req.map((_, k) => (list.includes(k) ? 1 : 0));
        const rows = [
          { name: "clk", kind: "clock" },
          { name: "rst_n", kind: "bit", values: st.rst, cells: (k) => `מחזור ${k} : rst_n = ${st.rst[k]}, לחיצה הופכת` },
          { name: "req", kind: "bit", values: st.req, cls: "wv-s1", cells: (k) => `מחזור ${k} : req = ${st.req[k]}, לחיצה הופכת` },
          { name: "ack", kind: "bit", values: st.ack, cls: "wv-s3", cells: (k) => `מחזור ${k} : ack = ${st.ack[k]}, לחיצה הופכת` },
        ].concat(RULES.map(([key, name]) => ({ name, kind: "flag", values: flag(fails[key]) })), [{ name: MUT[v][0], kind: "flag", values: flag(mf) }]);
        const wrap = $(".wv-wrap"), left = wrap.scrollLeft;
        wrap.innerHTML = waveStrip(rows, N, { role: "group", label: "דיאגרמת תזמון", labelW: 130, cursor: st.cur, ticks: (k) => k });
        wrap.scrollLeft = left;
        $(".ex-pos").textContent = `מחזור ${st.cur}`;
        $(".ex-prev").disabled = st.cur === 0; $(".ex-next").disabled = st.cur >= N - 1;
        // the cursor cycle: every attempt that starts here, or fails here after starting earlier
        const t = st.cur, said = [];
        const tell = (label, expr, att) => {
          const a = att[t];
          if (a.status !== "vacuous") said.push(`${label} (${code(expr.replace(/ /g, NB))})${NB}: ` + (a.end === t && (a.status === "pass" || a.status === "fail") ? `${a.status === "pass" ? `<span class="wv-ok">✓</span>` : `<span class="wv-bad">✗</span>`} באותו מחזור` : word(a)) + ".");
          att.filter((b) => b.t < t && b.end === t && b.status === "fail").forEach((b) => said.push(`${label}${NB}: הניסיון של מחזור ${ltr(b.t)} נכשל כאן <span class="wv-bad">✗</span>.`));
        };
        RULES.forEach(([key, , rule, expr]) => tell(rule, exprOf(expr), hsProp(key, st.req, st.ack, st.rst, w)));
        if (v !== "nodis") tell("המוטציה", exprOf(MUT[v][1]), hsProp(v, st.req, st.ack, st.rst, w));
        else RULES.forEach(([key, , rule]) => hsProp(key, st.req, st.ack, st.rst, w, false).filter((b) => b.end === t && b.status === "fail" && !fails[key].includes(t))
          .forEach((b) => said.push(`בלי ${code("disable iff")}, ${rule} נכשל כאן <span class="wv-bad">✗</span> (הניסיון של מחזור ${ltr(b.t)}).`)));
        $(".wv-step").innerHTML = `מחזור ${ltr(t)}${NB}: ${ltr(`rst_n = ${st.rst[t]}, req = ${st.req[t]}, ack = ${st.ack[t]}`)}. ` +
          (!st.rst[t] && dis ? `${code("rst_n")} נמוך${NB}: ‏${code("disable iff")} מבטל כל ניסיון שפתוח עכשיו. ` : "") +
          (said.length ? said.join(" ") : `אף אנטצדנט לא התאים כאן${NB}: כל הניסיונות שהתחילו במחזור הזה עברו באופן ריק.`);
        // the verdict: does this trace tell the variant from the rule it replaces?
        const orig = HS_MUTANTS[v] ? fails[HS_MUTANTS[v]] : [...new Set(Object.values(fails).flat())].sort((a, b) => a - b);
        const total = RULES.reduce((a, [key]) => a + fails[key].length, 0);
        const page = total === 0 ? `<span class="wv-ok">ארבעת החוקים עוברים ✓</span>`
          : `<span class="wv-bad">ארבעת החוקים${NB}: ${ltr(total)} ${total === 1 ? "הפרה" : "הפרות"}</span> (` + RULES.filter(([key]) => fails[key].length).map(([key, , rule]) => `${rule} במחזור${fails[key].length > 1 ? "ים" : ""} ${ltr(fails[key].join(", "))}`).join("; ") + `).`;
        const m = mf.length ? `המוטציה נכשלת במחזור${mf.length > 1 ? "ים" : ""} ${ltr(mf.join(", "))}` : "המוטציה עוברת";
        const same = JSON.stringify(orig) === JSON.stringify(mf);
        const extra = mf.some((k) => !orig.includes(k)), missed = orig.some((k) => !mf.includes(k));
        const kill = same ? `על הרצף הזה המוטציה והחוק המקורי מסכימים${NB}: הרצף לא מבדיל ביניהם.`
          : extra && missed ? `<span class="wv-bad">המוטציה והחוק נכשלים במחזורים שונים${NB}: הרצף מבדיל ביניהם.</span>`
          : extra ? `<span class="wv-bad">המוטציה מתריעה איפה שהחוק עבר${NB}: התרעת שווא.</span>`
          : `<span class="wv-bad">המוטציה שותקת איפה שהחוק נכשל${NB}: באג שהיה עובר.</span>`;
        $(".wv-sum").innerHTML = `${page} ${m}. ${kill}`;
      };
      const wrap = $(".wv-wrap");
      const tap = (c) => {
        const k = Number(c.dataset.k), label = c.getAttribute("aria-label");
        const row = label.includes("rst_n") ? st.rst : label.includes("req") ? st.req : st.ack;
        row[k] = row[k] ? 0 : 1; st.cur = k; draw();
      };
      wrap.addEventListener("click", (e) => { const c = e.target.closest(".wv-cell"); if (c) tap(c); });
      wrap.addEventListener("keydown", (e) => {
        const c = e.target.closest(".wv-cell");
        if (c && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); tap(c); }
      });
      const load = (p) => {
        st.rst = new Array(N).fill(1);
        if (p === "clear") { st.req = new Array(N).fill(0); st.ack = new Array(N).fill(0); st.cur = 0; return; }
        const [r, a, n] = p === "reset" ? HS_RESET : HS_PRESETS[p];
        st.req = hsWave(r, N); st.ack = hsWave(a, N); if (n) st.rst = hsWave(n, N);
        const first = Object.values(hsCheckRst(st.req, st.ack, st.rst, W())).flat().concat(hsMutant(mut(), st.req, st.ack, st.rst, W())).sort((x, y) => x - y)[0];
        st.cur = first === undefined ? 3 : first;
      };
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { load(b.dataset.p); draw(); }));
      $(".hs-mut").addEventListener("change", draw);
      $(".hs-wait").addEventListener("change", draw);
      $(".ex-next").addEventListener("click", () => { if (st.cur < N - 1) st.cur++; draw(); });
      $(".ex-prev").addEventListener("click", () => { if (st.cur > 0) st.cur--; draw(); });
      // the drawn rows ride in the link: "<rst_n>-<req>-<ack>", a bit per cycle
      box.dvqExtra = {
        get: () => [st.rst, st.req, st.ack].map((r) => r.join("")).join("-"),
        set: (text) => {
          const m = /^([01]{12})-([01]{12})-([01]{12})$/.exec(text);
          if (!m) return false;
          [st.rst, st.req, st.ack] = m.slice(1).map((s) => [...s].map(Number));
          draw(); return true;
        },
      };
      draw();
    },
  });

  // The attempts of the page's four properties (part a): at every cycle each property
  // starts an attempt; when its antecedent does not match the attempt passes vacuously
  // at once, otherwise it runs over its window and ends in a pass, a fail, or is still
  // open when the trace ends (a window cut by the end, not reported, as on the page).
  //   hold   (req && !ack) |=> req        window t + 1
  //   late   $rose(req) |-> !ack ##[1:w] ack   fails at t on an ack in the rise cycle,
  //          otherwise window t + 1 .. t + w, passes at the first ack
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
      if (req[t] && !prevReq && ack[t]) out.late.push({ t, end: t, status: "fail" });
      else if (req[t] && !prevReq) {
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
        ["late", "a_ack_in_time", "$rose(req) |-> !ack ##[1:3] ack", "חוק 2"],
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
      handshake: "בוחרים מוטציה, גרסה של אחת ה-properties מהמלכודות, והיא נבדקת לצד ארבעת החוקים של הדף על אותו רצף. לחיצה על משבצת של rst_n, req או ack הופכת אותה; הכפתורים טוענים את הדיאגרמות של הדף ורצף עם reset באמצע. בשורה האחרונה ה-✗ של המוטציה, ובסיכום אם הרצף מבדיל בינה לבין החוק המקורי : התרעת שווא, או באג שהיה עובר.",
      attempts: "מתחת לרצועה יש מסלול לכל property : בכל מחזור מתחיל ניסיון, נקודה מסמנת שהאנטצדנט התאים, הסוגר הוא החלון, ובסופו ✓ או ✗. נקודה אפורה היא ניסיון vacuous. ה-presets טוענים את הדיאגרמות של העמוד, לחיצה על משבצת הופכת אותה, ו״המחזור הבא״ מסביר מה קורה בכל מחזור.",
    },
    models: { hsCheck, HS_PRESETS, hsWave, hsAttempts, HS_PROPS, hsProp, hsCheckRst, hsMutant, HS_MUTANTS, HS_RESET },
  });
})();
