// kinds: acknak
//   acknak                 0025        the RC and the EP with the two link queues: send, deliver / corrupt / lose, the timers; the page's examples as scripts; random traffic at a fault rate with the invariants checked; an event axis of the counters
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { RAND_HASH, SEED_MAX, autoplay, eventStrip, ltr, mulberry32, newSeed, randNote, randomRow, seedControls, speedSel } = dvqExplorers.lib;

  // Ack/Nak (0025): the page's TransmitterWithReplay and ReceiverWithNak as one state
  // object with the two link queues between them (TLPs towards the EP, DLLPs towards
  // the RC). `anApply` is pure: it returns the next state and a log of what happened.
  // `rnd()` draws the EP's next Ack threshold (1..4), as the page's rng.randint(1, 4).
  const AN_MOD = 4096;
  const anInit = (startSeq, rnd) => ({
    nts: startSeq % AN_MOD, ackd: (startSeq - 1 + AN_MOD) % AN_MOD, retry: [], link: [], dllps: [],
    badDllp: 0, proto: 0, replays: 0,
    nrs: startSeq % AN_MOD, nak: false, pending: 0, threshold: rnd(), received: [], badTlp: 0, dups: 0,
    payload: 0xA0,
  });
  const anClone = (s) => ({ ...s, retry: s.retry.map((t) => ({ ...t })), link: s.link.map((t) => ({ ...t })), dllps: s.dllps.map((d) => ({ ...d })), received: [...s.received] });
  const anApply = (state, ev, rnd) => {
    const s = anClone(state), log = { type: ev.type, how: ev.how, items: [] };
    const lastAccepted = () => (s.nrs - 1 + AN_MOD) % AN_MOD;
    const sendAck = () => { s.dllps.push({ kind: "ACK", seq: lastAccepted(), crcOk: true }); s.pending = 0; s.threshold = rnd(); log.items.push({ out: "ack", seq: lastAccepted() }); };
    const scheduleNak = () => { if (s.nak) { log.items.push({ out: "nakHeld" }); return; } s.dllps.push({ kind: "NAK", seq: lastAccepted(), crcOk: true }); s.nak = true; s.pending = 0; log.items.push({ out: "nak", seq: lastAccepted() }); };
    const accept = (t) => { s.received.push(t.seq); s.nrs = (s.nrs + 1) % AN_MOD; s.nak = false; s.pending += 1; log.items.push({ out: "accepted", seq: t.seq, replay: t.replay }); if (s.pending >= s.threshold) sendAck(); };
    const isDup = (seq) => { const behind = (s.nrs - seq + AN_MOD) % AN_MOD; return behind > 0 && behind <= AN_MOD / 2; };
    const replay = () => { if (!s.retry.length) { log.items.push({ out: "nothingToReplay" }); return; } s.retry.forEach((t) => s.link.push({ ...t, crcOk: true, replay: true })); s.replays += 1; log.items.push({ out: "replay", seqs: s.retry.map((t) => t.seq) }); };
    if (ev.type === "send") {
      for (let i = 0; i < (ev.n || 1); i++) {
        const t = { seq: s.nts, payload: s.payload, crcOk: true, replay: false };
        s.retry.push({ seq: t.seq, payload: t.payload }); s.link.push(t);
        log.items.push({ out: "sent", seq: t.seq });
        s.nts = (s.nts + 1) % AN_MOD; s.payload += 1;
      }
    } else if (ev.type === "tlp") {
      for (let i = 0; i < (ev.count || 1); i++) {
        const t = s.link.shift();
        if (!t) { log.items.push({ out: "emptyLink" }); break; }
        if (ev.how === "lose") { log.items.push({ out: "lost", seq: t.seq }); continue; }
        if (ev.how === "bad" && i === 0) t.crcOk = false;
        if (!t.crcOk) { s.badTlp += 1; log.items.push({ out: "badTlp", seq: t.seq }); scheduleNak(); }
        else if (t.seq === s.nrs) accept(t);
        else if (isDup(t.seq)) { s.dups += 1; log.items.push({ out: "dup", seq: t.seq }); sendAck(); }
        else { s.badTlp += 1; log.items.push({ out: "future", seq: t.seq, expected: s.nrs }); scheduleNak(); }
      }
    } else if (ev.type === "dllp") {
      const d = s.dllps.shift();
      if (!d) log.items.push({ out: "emptyLink" });
      else if (ev.how === "lose") log.items.push({ out: "lost", kind: d.kind, seq: d.seq });
      else {
        if (ev.how === "bad") d.crcOk = false;
        if (ev.tamper !== undefined) d.seq = ev.tamper;
        log.kind = d.kind; log.seq = d.seq;
        if (!d.crcOk) { s.badDllp += 1; log.items.push({ out: "badDllp", kind: d.kind, seq: d.seq }); }
        else {
          const idx = s.retry.findIndex((t) => t.seq === d.seq);
          if (idx >= 0) { const purged = s.retry.slice(0, idx + 1).map((t) => t.seq); s.retry.splice(0, idx + 1); s.ackd = d.seq; log.items.push({ out: "purged", kind: d.kind, seq: d.seq, seqs: purged }); if (d.kind === "NAK") replay(); }
          else if (d.seq !== s.ackd) { s.proto += 1; log.items.push({ out: "protoErr", kind: d.kind, seq: d.seq }); }
          else { log.items.push({ out: "noProgress", kind: d.kind, seq: d.seq }); if (d.kind === "NAK") replay(); }
        }
      }
    } else if (ev.type === "flush") {
      if (s.pending && !s.nak) sendAck(); else log.items.push({ out: s.nak ? "flushNak" : "flushNothing" });
    } else if (ev.type === "timeout") {
      replay();
    }
    return { state: s, log };
  };
  // The page's two examples (tools/figures/q0025.py): start at 4094, scripted thresholds.
  const AN_SCRIPTS = {
    a: { start: 4094, thresholds: [2, 3, 1], steps: [
      { type: "send", n: 2 }, { type: "tlp", how: "ok" }, { type: "tlp", how: "ok" }, { type: "dllp", how: "ok" },
      { type: "send", n: 3 }, { type: "tlp", how: "ok" }, { type: "tlp", how: "ok" }, { type: "tlp", how: "ok" }, { type: "dllp", how: "ok" }] },
    b: { start: 4094, thresholds: [3, 1, 1, 1, 1], steps: [
      { type: "send", n: 4 }, { type: "tlp", how: "ok" }, { type: "tlp", how: "bad" }, { type: "tlp", how: "ok" }, { type: "tlp", how: "ok" },
      { type: "dllp", how: "ok" }, { type: "tlp", how: "ok" }, { type: "tlp", how: "ok", count: 2 }, { type: "dllp", how: "bad" },
      { type: "timeout" }, { type: "tlp", how: "ok", count: 3 }, { type: "dllp", how: "ok" }, { type: "dllp", how: "ok" }, { type: "dllp", how: "ok", tamper: 9 }] },
  };
  const anRun = (script, rnd) => {
    const th = [...script.thresholds];
    const draw = () => (th.length ? th.shift() : rnd());
    let s = anInit(script.start, draw);
    const states = [s];
    script.steps.forEach((ev) => { s = anApply(s, ev, draw).state; states.push(s); });
    return states;
  };
  // The two invariants the box checks, as the names of those that fail: "retry" (the
  // Retry Buffer holds exactly ACKD_SEQ + 1 .. NEXT_TRANSMIT_SEQ − 1) and "order" (the
  // TLPs were delivered once, in order).
  const anInvariants = (s) => {
    const expect = [];
    for (let q = (s.ackd + 1) % AN_MOD; q !== s.nts && expect.length <= AN_MOD; q = (q + 1) % AN_MOD) expect.push(q);
    const bad = [];
    if (expect.length !== s.retry.length || expect.some((q, i) => q !== s.retry[i].seq)) bad.push("retry");
    if (s.received.some((q, i) => i > 0 && q !== (s.received[i - 1] + 1) % AN_MOD)) bad.push("order");
    return bad;
  };
  // Random traffic, the way the page's test drives the link: `count` events drawn from
  // rnd (sends of 1 or 2 TLPs while fewer than 12 wait for an Ack, the head of a queue
  // delivered, the Ack timer, the replay timer once the link is drained), a delivery
  // corrupted or lost with probability `rate` (half each). The Ack thresholds are drawn
  // first and kept in the script, so the box replays it exactly. The invariants are
  // checked after every event and the first violation ends the script there (the
  // page's model never reaches one; the test corrupts a state to see the check fire).
  const anRandomScript = (start, count, rate, rnd) => {
    const thresholds = Array.from({ length: count + 2 }, () => 1 + Math.floor(rnd() * 4));
    const th = [...thresholds], draw = () => (th.length ? th.shift() : 1 + Math.floor(rnd() * 4));
    let s = anInit(start, draw);
    const steps = [], faults = { lost: 0, bad: 0 };
    let violation = null;
    const how = () => (rnd() < rate ? (rnd() < 0.5 ? "lose" : "bad") : "ok");
    while (steps.length < count) {
      const r = rnd();
      let ev;
      if (r < 0.15) { if (s.retry.length >= 12) continue; ev = { type: "send", n: 1 + Math.floor(rnd() * 2) }; }
      else if (r < 0.6) { if (!s.link.length) continue; ev = { type: "tlp", how: how() }; }
      else if (r < 0.85) { if (!s.dllps.length) continue; ev = { type: "dllp", how: how() }; }
      else if (r < 0.93) ev = { type: "flush" };
      else { if (s.link.length || !s.retry.length) continue; ev = { type: "timeout" }; }
      if (ev.how === "lose") faults.lost += 1; else if (ev.how === "bad") faults.bad += 1;
      steps.push(ev);
      s = anApply(s, ev, draw).state;
      const bad = anInvariants(s);
      if (bad.length) { violation = { index: steps.length, names: bad }; break; }
    }
    return { start, thresholds, steps, random: { count, rate, faults, violation } };
  };

  // The event axis of the box (X146): a short label per event, from its log.
  const anEventLabel = (log) => {
    if (!log) return "start";
    const mark = log.how === "bad" ? "!" : log.how === "lose" ? "×" : "";
    if (log.type === "send") return `TX${log.items.length > 1 ? log.items.length : ""}`;
    if (log.type === "tlp") return `TLP${mark}`;
    if (log.type === "dllp") { const it = log.items.find((x) => x.kind); const k = log.kind || (it && it.kind); return `${k === "NAK" ? "Nak" : k === "ACK" ? "Ack" : "DLLP"}${mark}`; }
    return log.type === "flush" ? "flush" : log.type === "timeout" ? "replay" : log.type;
  };
  // The Ack/Nak box (0025): the RC and the EP side by side with the two link queues
  // between them; free event buttons (a new TLP, the head of each queue delivered,
  // corrupted or lost, the two timers) and the page's two examples as scripts stepped
  // through with the same engine.
  const acknakView = () => ({
    mount(box) {
      const st = { start: 4094, history: [], script: null, pos: 0, state: null, log: null, th: [], seed: newSeed(), unit: null, draws: 0, mode: "free" };
      // the EP's thresholds: the script's list first, then the seeded generator; the
      // history keeps the list and the draw count, so "previous" then "next" redraws the same
      const draw4 = () => { if (st.th.length) return st.th.shift(); st.draws += 1; return 1 + Math.floor(st.unit() * 4); };
      const rewind = (draws) => { st.unit = mulberry32(st.seed); st.draws = 0; while (st.draws < draws) draw4(); };
      const reset = (start, script) => {
        st.start = start; st.script = script || null; st.pos = 0; st.th = script ? [...script.thresholds] : [];
        rewind(0);
        st.state = anInit(start, draw4); st.history = []; st.dropped = 0; st.log = null; render();
      };
      // a step: the state before it (and the script position) go to the history, so
      // "previous" restores both; a free event leaves the script
      const apply = (ev, scripted) => {
        if (!scripted && st.script) { st.script = null; st.th = []; }
        st.history.push({ state: st.state, log: st.log, pos: st.pos, th: [...st.th], draws: st.draws });
        if (st.history.length > 300) { st.history.shift(); st.dropped = (st.dropped || 0) + 1; }
        if (scripted) st.pos += 1;
        const r = anApply(st.state, ev, draw4);
        st.state = r.state; st.log = r.log; render();
      };
      box.innerHTML =
        `<div class="ex-controls"><span class="wv-presets">הדוגמאות שבעמוד : ` +
        `<button type="button" class="md-button ex-preset" data-p="a">סעיף א</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="b">סעיף ב</button></span>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא בתסריט</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1000, 400) +
        `<button type="button" class="md-button ex-end">לסוף התסריט</button><span class="ex-pos"></span>` +
        `<label>מתחילים מ-<select class="ex-start" aria-label="המספר הראשון"><option value="4094" selected>4094 (לפני הגלישה)</option><option value="0">0</option></select></label>` +
        `<button type="button" class="md-button ex-reset">איפוס</button></div>` +
        `<div class="ex-controls an-free"><span class="ex-title">אירועים חופשיים :</span> ` +
        `<button type="button" class="md-button ex-send">ה-RC שולח TLP</button>` +
        `<button type="button" class="md-button ex-flush">טיימר ה-Ack פג</button>` +
        `<button type="button" class="md-button ex-timeout">ה-REPLAY_TIMER פג</button></div>` +
        randomRow("שיעור התקלות", "תנועה אקראית (כמו ה-test של העמוד) :") +
        `<div class="an-box"><div class="an-side an-rc"></div><div class="an-link"></div><div class="an-side an-ep"></div></div>` +
        `<p class="ex-title">ציר האירועים : עמודה לכל אירוע, המונים אחריו, ו-✗ כשאינווריאנט נופל</p><div class="wv-wrap an-strip" tabindex="0" role="group" aria-label="ציר האירועים, גלילה אופקית"></div>` +
        `<p class="wv-step an-log" aria-live="polite"></p><p class="ex-summary an-sum"></p><p class="ex-note an-rand"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const chips = (items, cls) => (items.length ? items.map((t) => `<span class="an-chip${t.cls ? " " + t.cls : ""}">${t.text}</span>`).join("") : `<span class="an-empty">ריק</span>`);
      const field = (name, value, changed) => `<div class="an-field${changed ? " is-changed" : ""}"><span class="an-name">${name}</span><span class="an-val">${value}</span></div>`;
      const render = () => {
        const s = st.state, prev = st.history.length ? st.history[st.history.length - 1].state : null;
        const ch = (key) => prev && JSON.stringify(prev[key]) !== JSON.stringify(s[key]);
        $(".an-rc").innerHTML = `<p class="an-title">ה-RC, המשדר</p>` +
          field("NEXT_TRANSMIT_SEQ", ltr(s.nts), ch("nts")) + field("ACKD_SEQ", ltr(s.ackd), ch("ackd")) +
          `<div class="an-field${ch("retry") ? " is-changed" : ""}"><span class="an-name">Retry Buffer</span><span class="an-chips" dir="ltr">${chips(s.retry.map((t) => ({ text: t.seq })))}</span></div>` +
          `<p class="an-counts">‏DLLPs פגומים : ${ltr(s.badDllp)}, שגיאות פרוטוקול : ${ltr(s.proto)}, ‏Replays : ${ltr(s.replays)}</p>`;
        $(".an-ep").innerHTML = `<p class="an-title">ה-EP, המקבל</p>` +
          field("NEXT_RCV_SEQ", ltr(s.nrs), ch("nrs")) + field("ממתינים / סף", ltr(`${s.pending} / ${s.threshold}`), ch("pending") || ch("threshold")) +
          field("NAK_SCHEDULED", s.nak ? "1" : "0", ch("nak")) +
          `<div class="an-field${ch("received") ? " is-changed" : ""}"><span class="an-name">נמסרו ל-TL</span><span class="an-chips" dir="ltr">${chips(s.received.slice(-8).map((q) => ({ text: q, cls: "is-done" })))}${s.received.length > 8 ? `<span class="an-empty">…</span>` : ""}</span></div>` +
          `<p class="an-counts">‏TLPs פגומים או מוקדמים : ${ltr(s.badTlp)}, כפולים : ${ltr(s.dups)}</p>`;
        const headBtns = (kind, empty) => `<span class="an-head-btns">` +
          `<button type="button" class="md-button an-act" data-q="${kind}" data-how="ok" ${empty ? "disabled" : ""}>מסור</button>` +
          `<button type="button" class="md-button an-act" data-q="${kind}" data-how="bad" ${empty ? "disabled" : ""}>מסור עם CRC שגוי</button>` +
          `<button type="button" class="md-button an-act" data-q="${kind}" data-how="lose" ${empty ? "disabled" : ""}>אבד</button></span>`;
        $(".an-link").innerHTML =
          `<div class="an-queue"><p class="an-qtitle">‏TLPs בדרך אל ה-EP ←</p><div class="an-chips" dir="ltr">${chips(s.link.map((t, i) => ({ text: `${t.seq}${t.replay ? " R" : ""}`, cls: (i === 0 ? "is-head" : "") + (t.replay ? " is-replay" : "") })))}</div>${headBtns("tlp", !s.link.length)}</div>` +
          `<div class="an-queue"><p class="an-qtitle">→ ‏DLLPs בדרך אל ה-RC</p><div class="an-chips" dir="ltr">${chips(s.dllps.map((d, i) => ({ text: `${d.kind === "ACK" ? "Ack" : "Nak"} ${d.seq}`, cls: (i === 0 ? "is-head" : "") + (d.kind === "NAK" ? " is-nak" : "") })))}</div>${headBtns("dllp", !s.dllps.length)}</div>`;
        const scripted = !!st.script, left = scripted ? st.script.steps.length - st.pos : 0;
        $(".ex-next").disabled = !scripted || left === 0;
        $(".ex-play").disabled = !scripted;
        $(".ex-prev").disabled = !st.history.length;
        $(".ex-pos").textContent = scripted ? `צעד ${st.pos} מתוך ${st.script.steps.length}` : "";
        $(".an-log").innerHTML = st.log ? logText(st.log) : `מצב התחלתי : ${ltr(`ACKD_SEQ = ${s.ackd}`)} הוא "לפני ${ltr(s.nts)}", ה-Retry Buffer ריק, וה-EP מצפה ל-${ltr(s.nrs)} עם סף Ack ${ltr(s.threshold)} שהגריל.`;
        const strip = $(".an-strip");
        strip.innerHTML = eventStrip(st, (S) => [
          { name: "NTS", kind: "bus", values: S.map((x) => x.nts) },
          { name: "ACKD_SEQ", kind: "bus", values: S.map((x) => x.ackd) },
          { name: "NRS", kind: "bus", values: S.map((x) => x.nrs) },
          { name: "retry", kind: "bus", values: S.map((x) => x.retry.length) },
          { name: "NAK_SCHED", kind: "bit", values: S.map((x) => (x.nak ? 1 : 0)), cls: "wv-s2" },
        ], anEventLabel, anInvariants);
        strip.scrollLeft = strip.scrollWidth;
        const bad = anInvariants(s);
        $(".an-sum").innerHTML = (!bad.includes("retry") ? `<span class="wv-ok">✓ ה-Retry Buffer מכיל בדיוק את ${ltr("ACKD_SEQ + 1")} עד ${ltr("NEXT_TRANSMIT_SEQ − 1")}.</span>` : `<span class="wv-bad">✗ ה-Retry Buffer אינו הרצף מ-ACKD_SEQ + 1.</span>`) +
          ` ` + (!bad.includes("order") ? `<span class="wv-ok">✓ ה-TLPs נמסרו בסדר, בלי חור ובלי כפילות.</span>` : `<span class="wv-bad">✗ המסירה אינה בסדר.</span>`);
        $(".ex-end").disabled = !scripted || left === 0;
        const rd = st.script && st.script.random;
        $(".an-rand").innerHTML = rd ? randNote(rd, st.seed, `ובהם ${ltr(rd.faults.lost)} פקטים שאבדו ו-${ltr(rd.faults.bad)} שהגיעו עם CRC שגוי`,
          { retry: "אינווריאנט ה-Retry Buffer", order: "סדר המסירה" }, "שני האינווריאנטים נבדקו אחרי כל אירוע.") : "";
      };
      const logText = (log) => {
        const seqs = (a) => ltr(a.join(", "));
        const parts = log.items.map((it) => {
          switch (it.out) {
            case "sent": return `‏TLP ${ltr(it.seq)} יצא לקישור ועותק שלו נשמר ב-Retry Buffer.`;
            case "accepted": return `‏TLP ${ltr(it.seq)}${it.replay ? " (Replay)" : ""} הוא הצפוי : נמסר ל-Transaction Layer, ו-NEXT_RCV_SEQ מתקדם.`;
            case "ack": return `<span class="wv-ok">הספירה הגיעה לסף, יוצא Ack ${ltr(it.seq)} (מצטבר) וסף חדש מוגרל.</span>`;
            case "nak": return `<span class="wv-bad">יוצא Nak ${ltr(it.seq)} : הכול עד ${ltr(it.seq)} התקבל, מה שאחריו לא. NAK_SCHEDULED נדלק.</span>`;
            case "nakHeld": return `‏Nak כבר נשלח על הפער הזה, ולכן לא יוצא עוד אחד (בלי סופת Nak-ים).`;
            case "badTlp": return `<span class="wv-bad">‏TLP ${ltr(it.seq)} הגיע עם LCRC שגוי : נזרק, המצב לא משתנה.</span>`;
            case "dup": return `‏TLP ${ltr(it.seq)} ישן (כבר נמסר) : נזרק, ויוצא Ack חוזר כדי שהמשדר ינקה את ה-Retry Buffer.`;
            case "future": return `<span class="wv-bad">‏TLP ${ltr(it.seq)} הגיע לפני זמנו (מצפים ל-${ltr(it.expected)})  : נזרק.</span>`;
            case "lost": return `${it.kind ? (it.kind === "ACK" ? "Ack" : "Nak") + " " + ltr(it.seq) : "‏TLP " + ltr(it.seq)} אבד על הקו : אף צד לא יודע על זה עדיין.`;
            case "badDllp": return `<span class="wv-bad">${it.kind === "ACK" ? "Ack" : "Nak"} ${ltr(it.seq)} הגיע עם CRC שגוי : לא סומכים לא על הסוג ולא על המספר, נזרק.</span>`;
            case "purged": return `<span class="wv-ok">${it.kind === "ACK" ? "Ack" : "Nak"} ${ltr(it.seq)} מצטבר : ${seqs(it.seqs)} נמחקים מה-Retry Buffer ו-ACKD_SEQ הופך ל-${ltr(it.seq)}.</span>`;
            case "noProgress": return `${it.kind === "ACK" ? "Ack" : "Nak"} ${ltr(it.seq)} שווה ל-ACKD_SEQ : אין התקדמות, המצב לא משתנה.`;
            case "protoErr": return `<span class="wv-bad">${it.kind === "ACK" ? "Ack" : "Nak"} ${ltr(it.seq)} לא ב-Retry Buffer ולא ACKD_SEQ : שגיאת פרוטוקול, נזרק ונספר.</span>`;
            case "replay": return `<span class="wv-ok">‏Replay : ${seqs(it.seqs)} יוצאים שוב לקישור מהעותקים השמורים, עם המספרים המקוריים.</span>`;
            case "nothingToReplay": return `אין מה לשדר מחדש : ה-Retry Buffer ריק.`;
            case "flushNak": return `הטיימר פג, אבל Nak תלוי ועומד : לא יוצא Ack.`;
            case "flushNothing": return `הטיימר פג ואין TLPs שממתינים ל-Ack.`;
            case "emptyLink": return `התור ריק.`;
            default: return "";
          }
        });
        return parts.join(" ");
      };
      const nextStep = () => { if (st.script && st.pos < st.script.steps.length) apply(st.script.steps[st.pos], true); };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: nextStep,
        done: () => !st.script || st.pos >= st.script.steps.length,
        restart: () => { if (st.script) reset(st.start, st.script); },
      });
      $(".ex-next").addEventListener("click", () => { stop(); nextStep(); });
      $(".ex-end").addEventListener("click", () => { stop(); while (st.script && st.pos < st.script.steps.length) nextStep(); });
      $(".ex-prev").addEventListener("click", () => { stop(); const h = st.history.pop(); if (h) { st.state = h.state; st.log = h.log; st.pos = h.pos; st.th = h.th; rewind(h.draws); render(); } });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { stop(); reset(AN_SCRIPTS[b.dataset.p].start, AN_SCRIPTS[b.dataset.p]); $(".ex-start").value = "4094"; }));
      $(".ex-reset").addEventListener("click", () => { st.mode = "free"; seed.draw(); });
      $(".ex-start").addEventListener("change", () => { stop(); reset(Number($(".ex-start").value), null); });
      // the random run: a script drawn from the seed, replayed with the script controls
      const runRandom = () => {
        stop();
        const script = anRandomScript(Number($(".ex-start").value), Number($(".ex-count").value), Number($(".ex-rate").value) / 100, mulberry32(st.seed));
        reset(script.start, script);
      };
      $(".ex-run").addEventListener("click", () => { st.mode = "run"; seed.draw(); });
      $(".ex-rate").addEventListener("input", () => { $(".out-rate").textContent = `${$(".ex-rate").value}%`; if (st.script && st.script.random) runRandom(); });
      $(".ex-count").addEventListener("change", () => { if (st.script && st.script.random) runRandom(); });
      $(".ex-send").addEventListener("click", () => { stop(); apply({ type: "send", n: 1 }); });
      $(".ex-flush").addEventListener("click", () => { stop(); apply({ type: "flush" }); });
      $(".ex-timeout").addEventListener("click", () => { stop(); apply({ type: "timeout" }); });
      box.addEventListener("click", (e) => { const b = e.target.closest(".an-act"); if (b) { stop(); apply({ type: b.dataset.q, how: b.dataset.how }); } });
      reset(4094, AN_SCRIPTS.a);
      const seed = seedControls(box, $(".ex-run"), (rng, n) => { stop(); st.seed = n; if (st.mode === "run") runRandom(); else reset(Number($(".ex-start").value), null); }, { seed: st.seed, state: {
        get: () => (st.script && st.script.random ? `r${$(".ex-count").value}.${$(".ex-rate").value}.${st.seed}` : null),
        set: (p) => {
          const m = RAND_HASH.exec(p);
          if (!m || Number(m[2]) > 50 || Number(m[2]) % 5 || Number(m[3]) < 1 || Number(m[3]) > SEED_MAX) return false;
          $(".ex-count").value = m[1]; $(".ex-rate").value = m[2]; $(".out-rate").textContent = `${m[2]}%`;
          st.seed = Number(m[3]); $(".ex-seed").value = st.seed; st.mode = "run"; runRandom(); return true;
        },
      } });
    },
  });

  dvqExplorers.register({
    views: { acknak: acknakView },
    help: {
      acknak: "ה-RC וה-EP עם שני תורי הקישור : ״הצעד הבא״ ו״הפעלה״ מריצים את תסריטי העמוד, האירועים החופשיים שולחים, מוסרים (גם עם CRC שגוי או אובדן) ומפעילים טיימרים, ו״הרצה אקראית״ מגרילה תנועה עם תקלות ובודקת את האינווריאנטים. ציר האירועים מוסיף עמודה לכל אירוע.",
    },
    models: { AN_MOD, anInit, anApply, AN_SCRIPTS, anRun, anInvariants, anRandomScript, anEventLabel },
  });
})();
