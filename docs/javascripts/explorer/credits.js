// kinds: credits
//   credits                0024        the four counters as hands on a modulo-256 circle, the buffer, packets in flight; grant, transmit, lose, dequeue, sync; random legal traffic at a loss rate with the invariants checked; an event axis of the counters
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { RAND_HASH, SEED_MAX, autoplay, eventStrip, f, ltr, mulberry32, newSeed, randNote, randomRow, seedControls, speedSel } = dvqExplorers.lib;

  // USB4 path credits (0024): the page's EgressSyncModel and IngressSyncModel as one
  // state with the packets in flight between them. Errors the page raises (a transmission
  // without a credit, a buffer overflow, a dequeue from an empty buffer) are counted and
  // leave the counters as they were.
  const CR_MOD = 256;
  const crDist = (a, b) => (b - a + CR_MOD) % CR_MOD;
  const crInit = (size, base = 0) => ({
    size, pcc: base % CR_MOD, pcl: base % CR_MOD, pcr: base % CR_MOD, pca: (base + size) % CR_MOD,
    occ: 0, link: [], nextId: 1, errors: 0,
  });
  const crCanTransmit = (s) => { const ahead = crDist(s.pcc, s.pcl); return ahead > 0 && ahead < 128; };
  const crApply = (state, ev) => {
    const s = { ...state, link: [...state.link] }, log = { type: ev.type, how: ev.how, items: [] };
    const transmit = () => {
      if (!crCanTransmit(s)) { s.errors += 1; log.items.push({ out: "noCredit", pcc: s.pcc, pcl: s.pcl }); return false; }
      s.pcc = (s.pcc + 1) % CR_MOD; s.link.push(s.nextId); log.items.push({ out: "transmitted", id: s.nextId }); s.nextId += 1; return true;
    };
    const receive = (how) => {
      const id = s.link.shift();
      if (id === undefined) { log.items.push({ out: "emptyLink" }); return; }
      if (how === "lose") { log.items.push({ out: "lost", id }); return; }
      if (s.occ >= s.size) { s.errors += 1; log.items.push({ out: "overflow", id }); return; }
      s.pcr = (s.pcr + 1) % CR_MOD; s.occ += 1; log.items.push({ out: "received", id });
    };
    if (ev.type === "grant") { s.pcl = s.pca; log.items.push({ out: "grant", value: s.pca, credits: crDist(s.pcc, s.pcl) }); }
    else if (ev.type === "transmit") transmit();
    else if (ev.type === "receive") receive(ev.how);
    else if (ev.type === "packet") { if (transmit()) receive(ev.how); }
    else if (ev.type === "dequeue") {
      if (s.occ === 0) { s.errors += 1; log.items.push({ out: "emptyBuffer" }); }
      else { s.occ -= 1; s.pca = (s.pca + 1) % CR_MOD; log.items.push({ out: "dequeued", pca: s.pca }); }
    } else if (ev.type === "sync") {
      const missing = crDist(s.pcr, s.pcc);
      s.pca = (s.pca + missing) % CR_MOD; log.items.push({ out: "sync", pcc: s.pcc, pcrBefore: s.pcr, missing, pca: s.pca }); s.pcr = s.pcc;
    }
    return { state: s, log };
  };
  // The page's two examples (tools/figures/q0024.py): a buffer of 5.
  const CR_SCRIPTS = {
    a: { size: 5, steps: [{ type: "grant" }, { type: "packet", how: "ok" }, { type: "packet", how: "ok" }, { type: "packet", how: "ok" }, { type: "dequeue" }, { type: "dequeue" }, { type: "grant" },
      { type: "packet", how: "ok" }, { type: "packet", how: "ok" }, { type: "packet", how: "ok" }, { type: "packet", how: "ok" }] },
    b: { size: 5, steps: [{ type: "grant" }, { type: "packet", how: "ok" }, { type: "packet", how: "lose" }, { type: "packet", how: "ok" }, { type: "dequeue" }, { type: "dequeue" }, { type: "grant" }, { type: "sync" }, { type: "grant" }] },
  };
  const crRun = (script, base = 0) => {
    let s = crInit(script.size, base);
    const states = [s];
    script.steps.forEach((ev) => { s = crApply(s, ev).state; states.push(s); });
    return states;
  };
  // What the credits add up to against the buffer: the credits the Egress holds plus the
  // packets in flight can never exceed the free slots; the gap is slots freed but not yet
  // granted (PCA − PCL) plus packets lost and not yet synced (the leak). A negative leak
  // means a Sync counted a packet in flight as lost, and the gap turns into an overflow
  // risk. crInvariants names what fails: "overflow" (an error of the page's models, or
  // more packets than slots) and "credits" (credits + in flight > free slots).
  const crBalance = (s) => {
    const credits = crDist(s.pcc, s.pcl), free = s.size - s.occ, ungranted = crDist(s.pcl, s.pca);
    return { credits, inFlight: s.link.length, free, ungranted, leak: free - credits - s.link.length - ungranted };
  };
  const crInvariants = (s) => {
    const b = crBalance(s), bad = [];
    if (s.errors || s.occ > s.size) bad.push("overflow");
    if (b.credits + b.inFlight > b.free) bad.push("credits");
    return bad;
  };
  // Random traffic as the page's test drives it: only legal events (a transmission with a
  // credit, a dequeue from a non-empty buffer, a Sync when nothing is in flight, since on
  // the in-order link it arrives after the packets ahead of it), a received packet lost
  // with probability `rate`. The invariants are checked after every event; the first
  // violation ends the script there.
  const crRandomScript = (size, base, count, rate, rnd) => {
    let s = crInit(size, base);
    const steps = [], faults = { lost: 0, syncs: 0 };
    let violation = null;
    while (steps.length < count) {
      const r = rnd();
      let ev;
      if (r < 0.3) { if (!crCanTransmit(s)) continue; ev = { type: "transmit" }; }
      else if (r < 0.65) { if (!s.link.length) continue; ev = { type: "receive", how: rnd() < rate ? "lose" : "ok" }; }
      else if (r < 0.8) { if (!s.occ) continue; ev = { type: "dequeue" }; }
      else if (r < 0.93) ev = { type: "grant" };
      else { if (s.link.length) continue; ev = { type: "sync" }; }
      if (ev.how === "lose") faults.lost += 1; else if (ev.type === "sync") faults.syncs += 1;
      steps.push(ev);
      s = crApply(s, ev).state;
      const bad = crInvariants(s);
      if (bad.length) { violation = { index: steps.length, names: bad }; break; }
    }
    return { size, steps, random: { count, rate, faults, violation } };
  };

  const crEventLabel = (log) => {
    if (!log) return "start";
    const mark = log.how === "lose" ? "×" : "";
    return { grant: "Grant", transmit: "TX", receive: `RX${mark}`, packet: `pkt${mark}`, dequeue: "deq", sync: "Sync" }[log.type] || log.type;
  };
  // The credits box (0024): the four counters as hands on one modulo-256 circle (the
  // credits are the arc from PCC to PCL, the free slots the arc from PCR to PCA), the
  // dedicated buffer, the packets in flight, and the counters in a table; free events
  // and the page's two examples as scripts. A start near 250 shows the wrap.
  const creditsView = () => ({
    mount(box) {
      const st = { size: 5, base: 0, script: null, pos: 0, state: null, log: null, history: [], seed: newSeed() };
      const reset = (script) => { st.script = script || null; st.pos = 0; st.state = crInit(st.size, st.base); st.history = []; st.dropped = 0; st.log = null; render(); };
      const apply = (ev, scripted) => {
        if (!scripted && st.script) st.script = null;
        st.history.push({ state: st.state, log: st.log, pos: st.pos }); if (st.history.length > 300) { st.history.shift(); st.dropped = (st.dropped || 0) + 1; }
        if (scripted) st.pos += 1;
        const r = crApply(st.state, ev); st.state = r.state; st.log = r.log; render();
      };
      box.innerHTML =
        `<div class="ex-controls"><span class="wv-presets">הדוגמאות שבעמוד : ` +
        `<button type="button" class="md-button ex-preset" data-p="a">סעיף א</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="b">סעיף ב</button></span>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא בתסריט</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1000, 400) +
        `<button type="button" class="md-button ex-end">לסוף התסריט</button><span class="ex-pos"></span>` +
        `<label>גודל ה-buffer <select class="ex-size" aria-label="גודל ה-buffer">${[3, 4, 5, 6, 8].map((v) => `<option value="${v}"${v === 5 ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<label><input type="checkbox" class="ex-wrap"> <span>להתחיל מ-250 (הגלישה)</span></label>` +
        `<button type="button" class="md-button ex-reset">איפוס</button></div>` +
        `<div class="ex-controls an-free"><span class="ex-title">אירועים חופשיים :</span> ` +
        `<button type="button" class="md-button cr-act" data-ev="grant">Credit Grant</button>` +
        `<button type="button" class="md-button cr-act" data-ev="transmit">ה-Egress משדר פקטה</button>` +
        `<button type="button" class="md-button cr-act" data-ev="receive" data-how="ok">הפקטה הבאה התקבלה</button>` +
        `<button type="button" class="md-button cr-act" data-ev="receive" data-how="lose">הפקטה הבאה אבדה</button>` +
        `<button type="button" class="md-button cr-act" data-ev="dequeue">פקטה יוצאת מה-buffer</button>` +
        `<button type="button" class="md-button cr-act" data-ev="sync">Path Credit Sync</button></div>` +
        randomRow("שיעור האובדן", "תנועה אקראית (כמו ה-test של העמוד, אירועים חוקיים בלבד) :") +
        `<div class="cr-box"><div class="cr-circle"></div><div class="cr-panel"><div class="cr-table"></div><p class="cr-buf"></p><p class="cr-link"></p></div></div>` +
        `<p class="ex-title">ציר האירועים : עמודה לכל אירוע, המונים אחריו, ו-✗ כשאינווריאנט נופל</p><div class="wv-wrap an-strip" tabindex="0" role="group" aria-label="ציר האירועים, גלילה אופקית"></div>` +
        `<p class="wv-step an-log" aria-live="polite"></p><p class="ex-summary an-sum"></p><p class="ex-note an-rand"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const circle = (s) => {
        const C = 150, R = 110, ang = (v) => -Math.PI / 2 + (v / CR_MOD) * 2 * Math.PI;
        const pt = (v, r) => [C + r * Math.cos(ang(v)), C + r * Math.sin(ang(v))];
        const arc = (a, b, r, cls) => {
          const d = crDist(a, b); if (d === 0) return "";
          const [x1, y1] = pt(a, r), [x2, y2] = pt(b, r);
          return `<path class="${cls}" d="M${f(x1)},${f(y1)} A${r},${r} 0 ${d > 128 ? 1 : 0} 1 ${f(x2)},${f(y2)}"/>`;
        };
        let g = `<svg class="cr-live" viewBox="0 0 300 300" role="img" aria-label="מעגל של 256 ערכים עם ארבעת המונים; הקשת מ-PCC ל-PCL היא הקרדיטים, הקשת מ-PCR ל-PCA היא התאים הפנויים לפי ה-Ingress">` +
          `<circle class="cr-ring" cx="${C}" cy="${C}" r="${R}"/>`;
        for (let v = 0; v < CR_MOD; v += 32) { const [x1, y1] = pt(v, R - 5), [x2, y2] = pt(v, R + 5); g += `<line class="cr-tick" x1="${f(x1)}" y1="${f(y1)}" x2="${f(x2)}" y2="${f(y2)}"/><text class="cr-ticktext" x="${f(pt(v, R + 17)[0])}" y="${f(pt(v, R + 17)[1] + 4)}" text-anchor="middle">${v}</text>`; }
        g += arc(s.pcc, s.pcl, R - 14, "cr-arc cr-arc-credits") + arc(s.pcr, s.pca, R - 28, "cr-arc cr-arc-free");
        // the labels sit at four different radii, so equal counters still read
        const hand = (v, r, cls, name, lr) => { const [x, y] = pt(v, r), [lx, ly] = pt(v, lr); return `<line class="cr-hand ${cls}" x1="${C}" y1="${C}" x2="${f(x)}" y2="${f(y)}"/><circle class="cr-dot ${cls}" cx="${f(x)}" cy="${f(y)}" r="5"/><text class="cr-label ${cls}" x="${f(lx)}" y="${f(ly + 4)}" text-anchor="middle">${name}</text>`; };
        g += hand(s.pcr, R - 28, "cr-pcr", "PCR", 24) + hand(s.pcc, R - 14, "cr-pcc", "PCC", 46) + hand(s.pcl, R - 14, "cr-pcl", "PCL", 68) + hand(s.pca, R - 28, "cr-pca", "PCA", 92);
        return g + `</svg><p class="cr-legend"><span class="cr-lg cr-lg-s1">‏PCC מלא, ‏PCL מקווקו : ה-Egress</span> <span class="cr-lg cr-lg-s2">‏PCR מלא, ‏PCA מקווקו : ה-Ingress</span></p>`;
      };
      const render = () => {
        const s = st.state, prev = st.history.length ? st.history[st.history.length - 1].state : null;
        const ch = (k) => prev && prev[k] !== s[k];
        $(".cr-circle").innerHTML = circle(s);
        const credits = crDist(s.pcc, s.pcl), free = crDist(s.pcr, s.pca);
        const row = (k, name, meaning) => `<div class="an-field${ch(k) ? " is-changed" : ""}"><span class="an-name">${name}</span><span class="an-val">${ltr(s[k])}</span><span class="cr-meaning">${meaning}</span></div>`;
        $(".cr-table").innerHTML = row("pcc", "PCC", "‏Egress : פקטות ששודרו") + row("pcl", "PCL", "‏Egress : ה-Grant האחרון") +
          row("pcr", "PCR", "‏Ingress : פקטות שנכנסו ל-buffer") + row("pca", "PCA", "‏Ingress : תאים שהוקצו מאז ההקמה") +
          `<p class="cr-derived">קרדיטים ${ltr(`= PCL − PCC = ${credits}`)}; תאים פנויים לפי ה-Ingress ${ltr(`= PCA − PCR = ${free}`)}.</p>`;
        let cells = ""; for (let i = 0; i < s.size; i++) cells += `<span class="cr-slot${i < s.occ ? " is-full" : ""}"></span>`;
        $(".cr-buf").innerHTML = `ה-buffer הייעודי (${ltr(s.size)} תאים, תפוסה ${ltr(s.occ)})  : <span class="cr-slots" dir="ltr">${cells}</span>`;
        $(".cr-link").innerHTML = `פקטות בדרך אל ה-Ingress : <span class="an-chips" dir="ltr">${s.link.length ? s.link.map((id, i) => `<span class="an-chip${i === 0 ? " is-head" : ""}">${id}</span>`).join("") : `<span class="an-empty">אין</span>`}</span>`;
        box.querySelectorAll(".cr-act").forEach((b) => {
          const ev = b.dataset.ev;
          b.disabled = (ev === "receive" && !s.link.length) || (ev === "transmit" && !crCanTransmit(s)) || (ev === "dequeue" && !s.occ);
        });
        const scripted = !!st.script;
        $(".ex-next").disabled = !scripted || st.pos >= st.script.steps.length;
        $(".ex-end").disabled = !scripted || st.pos >= st.script.steps.length;
        $(".ex-play").disabled = !scripted;
        $(".ex-prev").disabled = !st.history.length;
        $(".ex-pos").textContent = scripted ? `צעד ${st.pos} מתוך ${st.script.steps.length}` : "";
        $(".an-log").innerHTML = st.log ? st.log.items.map(logText).join(" ") : `הקמת הנתיב : ${ltr(`PCA = ${s.pca}`)} הוא גודל ה-buffer${s.pca !== s.size ? " מעל נקודת ההתחלה" : ""}, ושאר המונים ב-${ltr(s.pcc)}. ‏PCL עדיין ${ltr(s.pcl)}, ולכן אין קרדיטים עד ה-Credit Grant הראשון.`;
        // the balance against the buffer: credits + in flight never exceed the free slots;
        // the gap is slots not yet granted plus packets lost and not yet synced
        const strip = $(".an-strip");
        strip.innerHTML = eventStrip(st, (S) => [
          { name: "PCC", kind: "bus", values: S.map((x) => x.pcc) },
          { name: "PCL", kind: "bus", values: S.map((x) => x.pcl) },
          { name: "PCR", kind: "bus", values: S.map((x) => x.pcr) },
          { name: "PCA", kind: "bus", values: S.map((x) => x.pca) },
          { name: "credits", kind: "bus", values: S.map((x) => crDist(x.pcc, x.pcl)) },
          { name: "occupancy", kind: "bus", values: S.map((x) => x.occ) },
        ], crEventLabel, crInvariants);
        strip.scrollLeft = strip.scrollWidth;
        const b = crBalance(s), bad = crInvariants(s);
        const gap = [];
        if (b.ungranted) gap.push(`${ltr(b.ungranted)} תאים שהתפנו ומחכים ל-Grant`);
        if (b.leak > 0) gap.push(`<b>דליפה</b> : ${ltr(b.leak)} פקטות אבדו ולא סונכרנו, ולכן ${ltr(b.leak)} תאים פנויים בלי קרדיט עד ה-Path Credit Sync הבא`);
        $(".an-sum").innerHTML = (crCanTransmit(s) ? `<span class="wv-ok">מותר לשדר : ${ltr(credits)} קרדיטים (מרחק 1 עד 127 קדימה מ-PCC ל-PCL).</span>` : `<span class="wv-bad">אסור לשדר : ${credits === 0 ? "הקרדיטים אזלו, PCL = PCC" : "PCL מאחורי PCC על המעגל (Grant ישן או מושחת)"}.</span>`) +
          ` ` + (bad.includes("overflow") ? `<span class="wv-bad">✗ ${s.occ > s.size ? "ה-buffer גלש" : `${ltr(s.errors)} הפרות של הסביבה (שידור בלי קרדיט, גלישה או הוצאה מ-buffer ריק)`}.</span> ` : "") +
          (bad.includes("credits")
            ? `<span class="wv-bad">✗ קרדיטים ועוד פקטות בדרך (${ltr(`${b.credits} + ${b.inFlight}`)}) עולים על ${ltr(b.free)} התאים הפנויים : Sync שנשלח כשפקטות היו בדרך ספר אותן כאבודות, וה-buffer עלול לגלוש.</span>`
            : `<span class="wv-ok">✓ קרדיטים ועוד פקטות בדרך (${ltr(`${b.credits} + ${b.inFlight}`)}) אינם עולים על ${ltr(b.free)} התאים הפנויים${gap.length ? ` : ההפרש הוא ${gap.join(", ו")}` : ""}.</span>`);
        const rd = st.script && st.script.random;
        $(".an-rand").innerHTML = rd ? randNote(rd, st.seed, `ובהם ${ltr(rd.faults.lost)} פקטות שאבדו ו-${ltr(rd.faults.syncs)} סנכרונים`,
          { overflow: "אין גלישה", credits: "קרדיטים ועוד פקטות בדרך אינם עולים על התאים הפנויים" }, "שני האינווריאנטים נבדקו אחרי כל אירוע.") : "";
      };
      const logText = (it) => {
        switch (it.out) {
          case "grant": return `‏Credit Grant נושא ${ltr(`PCA = ${it.value}`)}; ה-Egress מחליף בו את PCL (לא מחבר), ועכשיו יש ${ltr(it.credits)} קרדיטים.`;
          case "transmitted": return `פקטה ${ltr(it.id)} שודרה : PCC עולה באחד והיא בדרך.`;
          case "noCredit": return `<span class="wv-bad">שידור בלי קרדיט (${ltr(`PCC = ${it.pcc}, PCL = ${it.pcl}`)})  : המודל מדווח על הפרה ולא משנה דבר.</span>`;
          case "received": return `פקטה ${ltr(it.id)} התקבלה : PCR עולה באחד והיא תופסת תא.`;
          case "lost": return `<span class="wv-bad">פקטה ${ltr(it.id)} אבדה על הקו : ה-Egress ספר אותה ב-PCC, ה-Ingress לא יודע עליה, ואף מונה שלו לא זז.</span>`;
          case "overflow": return `<span class="wv-bad">ה-buffer מלא : גלישה, הפרה של הסביבה.</span>`;
          case "dequeued": return `פקטה יצאה מה-buffer : התא התפנה ו-PCA עולה ל-${ltr(it.pca)} (מצטבר).`;
          case "emptyBuffer": return `<span class="wv-bad">הוצאה מ-buffer ריק : הפרה.</span>`;
          case "sync": return `<span class="wv-ok">‏Path Credit Sync עם ${ltr(`PCC = ${it.pcc}`)} : ${ltr(`PCC − PCR = ${it.missing}`)} פקטות שודרו ולא התקבלו, הקרדיטים שלהן חוזרים (${ltr(`PCA = ${it.pca}`)}) ו-PCR מיושר ל-PCC.</span>`;
          case "emptyLink": return `אין פקטות בדרך.`;
          default: return "";
        }
      };
      const nextStep = () => { if (st.script && st.pos < st.script.steps.length) apply(st.script.steps[st.pos], true); };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: nextStep,
        done: () => !st.script || st.pos >= st.script.steps.length,
        restart: () => { if (st.script) reset(st.script); },
      });
      $(".ex-next").addEventListener("click", () => { stop(); nextStep(); });
      $(".ex-end").addEventListener("click", () => { stop(); while (st.script && st.pos < st.script.steps.length) nextStep(); });
      $(".ex-prev").addEventListener("click", () => { stop(); const h = st.history.pop(); if (h) { st.state = h.state; st.log = h.log; st.pos = h.pos; render(); } });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { stop(); st.size = CR_SCRIPTS[b.dataset.p].size; $(".ex-size").value = String(st.size); reset(CR_SCRIPTS[b.dataset.p]); }));
      $(".ex-size").addEventListener("change", () => { stop(); st.size = Number($(".ex-size").value); reset(null); });
      $(".ex-wrap").addEventListener("change", () => { stop(); st.base = $(".ex-wrap").checked ? 250 : 0; reset(null); });
      $(".ex-reset").addEventListener("click", () => { stop(); reset(null); });
      box.addEventListener("click", (e) => { const b = e.target.closest(".cr-act"); if (b) { stop(); apply({ type: b.dataset.ev, how: b.dataset.how }); } });
      // the random run: a script of legal events drawn from the seed
      const runRandom = () => {
        stop();
        reset(crRandomScript(st.size, st.base, Number($(".ex-count").value), Number($(".ex-rate").value) / 100, mulberry32(st.seed)));
      };
      $(".ex-run").addEventListener("click", () => seed.draw());
      $(".ex-rate").addEventListener("input", () => { $(".out-rate").textContent = `${$(".ex-rate").value}%`; if (st.script && st.script.random) runRandom(); });
      $(".ex-count").addEventListener("change", () => { if (st.script && st.script.random) runRandom(); });
      reset(CR_SCRIPTS.a);
      const seed = seedControls(box, $(".ex-run"), (rng, n) => { st.seed = n; runRandom(); }, { seed: st.seed, state: {
        get: () => (st.script && st.script.random ? `r${$(".ex-count").value}.${$(".ex-rate").value}.${st.seed}` : null),
        set: (p) => {
          const m = RAND_HASH.exec(p);
          if (!m || Number(m[2]) > 50 || Number(m[2]) % 5 || Number(m[3]) < 1 || Number(m[3]) > SEED_MAX) return false;
          $(".ex-count").value = m[1]; $(".ex-rate").value = m[2]; $(".out-rate").textContent = `${m[2]}%`;
          st.seed = Number(m[3]); $(".ex-seed").value = st.seed; runRandom(); return true;
        },
      } });
    },
  });

  dvqExplorers.register({
    views: { credits: creditsView },
    help: {
      credits: "ארבעת המונים כמחוגים על מעגל : תסריטי העמוד ב״הצעד הבא״, אירועים חופשיים (Grant, שידור, קבלה או אובדן, הוצאה, Sync) ו״הרצה אקראית״ עם שיעור אובדן. שורת הסיכום מאזנת קרדיטים מול תאים פנויים, וציר האירועים מוסיף עמודה לכל אירוע.",
    },
    models: { crEventLabel, CR_MOD, crDist, crInit, crCanTransmit, crApply, CR_SCRIPTS, crRun, crBalance, crInvariants, crRandomScript },
  });
})();
