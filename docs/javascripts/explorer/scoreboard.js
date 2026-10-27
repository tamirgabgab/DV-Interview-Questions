// kinds: scoreboard
//   scoreboard             0050        the scenarios of part b or a random stream with one injected bug, stepped event by event: the queue of every ID, and the verdicts of three checkers (a queue per ID, one queue, a search in the ID's queue)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { autoplay, code, ltr, mulberry32, seedControls, speedSel } = dvqExplorers.lib;

  // Out-of-order scoreboard (0050): three checkers over events { t, op, id, data } (op is
  // req, rsp, reset or end), each with the same timeout and end checks: "per_id" compares
  // a response with the oldest pending request of its ID, "fifo" with the oldest pending
  // request of all, "any" with a pending request of its ID with the same data (else the
  // oldest of its ID). The errors are [kind, id] in order; trace[k] is after event k.
  const sbCheck = (events, kind, timeout) => {
    const pend = [], errors = [], trace = [];
    events.forEach(({ t, op, id, data }) => {
      const before = errors.length;
      pend.forEach((p) => { if (!p.late && t - p.t > timeout) { p.late = true; errors.push(["timeout", p.id]); } });
      if (op === "req") pend.push({ t, id, data, late: false });
      else if (op === "reset") pend.length = 0;
      else if (op === "end") pend.forEach((p) => errors.push(["missing", p.id]));
      else if (op === "rsp") {
        let cand = null;
        if (kind === "fifo") {
          cand = pend[0] || null;
          if (cand && cand.id !== id) { errors.push(["mismatch", id]); pend.shift(); cand = undefined; }
        } else if (kind === "per_id") cand = pend.find((p) => p.id === id) || null;
        else cand = pend.find((p) => p.id === id && p.data === data) || pend.find((p) => p.id === id) || null;
        if (cand === null) errors.push(["unexpected", id]);
        else if (cand) { pend.splice(pend.indexOf(cand), 1); if (cand.data !== data) errors.push(["mismatch", id]); }
      }
      trace.push({ pend: pend.map((p) => ({ ...p })), added: errors.slice(before) });
    });
    return { errors, trace };
  };
  // A random stream: requests and responses interleaved, every ID answered in its own
  // order; then one bug: two responses of one ID swapped, a wrong data, a dropped or a
  // duplicated response, or everything from one response on delayed past the timeout.
  const SB_TIMEOUT = 8;
  const sbTraffic = (seed, bug, n = 16, ids = 3) => {
    const rng = mulberry32(seed), pick = (a) => a[Math.floor(rng() * a.length)];
    // at most four requests wait at a time, and the oldest is answered before its timeout
    const ev = [], pend = Array.from({ length: ids }, () => []);
    let t = 0, nxt = 100, sent = 0;
    while (sent < n || pend.some((q) => q.length)) {
      const busy = pend.map((q, i) => (q.length ? i : -1)).filter((i) => i >= 0);
      const waiting = pend.reduce((a, q) => a + q.length, 0);
      const oldest = busy.length ? busy.reduce((a, i) => (pend[i][0].t < pend[a][0].t ? i : a), busy[0]) : -1;
      const urgent = oldest >= 0 && t - pend[oldest][0].t >= SB_TIMEOUT - 3;
      if (!urgent && sent < n && waiting < 4 && (!busy.length || rng() < 0.55)) {
        const i = Math.floor(rng() * ids); ev.push({ t, op: "req", id: i, data: nxt }); pend[i].push({ data: nxt, t }); nxt++; sent++;
      } else {
        const i = urgent ? oldest : pick(busy); ev.push({ t, op: "rsp", id: i, data: pend[i].shift().data });
      }
      t++;
    }
    const rsp = ev.map((e, k) => (e.op === "rsp" ? k : -1)).filter((k) => k >= 0);
    let out = ev;
    if (bug === "swap") {
      const pairs = [];
      rsp.forEach((a) => rsp.forEach((b) => { if (a < b && ev[a].id === ev[b].id) pairs.push([a, b]); }));
      if (pairs.length) { const [a, b] = pick(pairs); const da = ev[a].data; out = ev.map((e) => ({ ...e })); out[a].data = ev[b].data; out[b].data = da; }
      else bug = "data";
    }
    if (bug === "data") { const k = pick(rsp); out = ev.map((e, j) => (j === k ? { ...e, data: e.data + 1000 } : e)); }
    else if (bug === "drop") { const k = pick(rsp); out = ev.filter((_, j) => j !== k); }
    else if (bug === "dup") { const k = pick(rsp); out = ev.slice(0, k + 1).concat([{ ...ev[k] }], ev.slice(k + 1)); }
    else if (bug === "late") { const k = pick(rsp); out = ev.map((e, j) => (j >= k ? { ...e, t: e.t + 3 * SB_TIMEOUT } : e)); }
    const end = out.length ? out[out.length - 1].t + 1 : 0;
    return out.concat([{ t: end, op: "end", id: 0, data: 0 }]);
  };

  const E = (t, op, id = 0, data = 0) => ({ t, op, id, data });
  const SCEN = [
    ["ערבוב חוקי בין IDs", true, [E(0, "req", 0, 10), E(1, "req", 1, 20), E(2, "req", 0, 11), E(3, "rsp", 1, 20), E(4, "rsp", 0, 10), E(5, "rsp", 0, 11), E(6, "end")]],
    ["החלפת סדר בתוך ID", false, [E(0, "req", 0, 10), E(1, "req", 0, 11), E(2, "rsp", 0, 11), E(3, "rsp", 0, 10), E(4, "end")]],
    ["נתון שגוי", false, [E(0, "req", 0, 10), E(1, "req", 1, 20), E(2, "rsp", 1, 21), E(3, "rsp", 0, 10), E(4, "end")]],
    ["תשובה חסרה", false, [E(0, "req", 0, 10), E(1, "req", 1, 20), E(2, "rsp", 1, 20), E(3, "end")]],
    ["תשובה כפולה", false, [E(0, "req", 0, 10), E(1, "rsp", 0, 10), E(2, "rsp", 0, 10), E(3, "end")]],
    ["תשובה מאוחרת", false, [E(0, "req", 0, 10), E(12, "rsp", 0, 10), E(13, "end")]],
    ["איפוס, ותשובה חדשה אחריו", true, [E(0, "req", 0, 10), E(1, "req", 1, 20), E(2, "reset"), E(3, "req", 1, 21), E(4, "rsp", 1, 21), E(5, "end")]],
    ["תשובה ישנה אחרי איפוס", false, [E(0, "req", 0, 10), E(1, "reset"), E(2, "rsp", 0, 10), E(3, "end")]],
  ];
  const BUGS = [["none", "בלי באג (חוקי)"], ["swap", "החלפה בתוך ID"], ["data", "נתון שגוי"], ["drop", "תשובה חסרה"], ["dup", "תשובה כפולה"], ["late", "עיכוב מעבר ל-timeout"]];
  const KINDS = [["per_id", "תור לכל ID"], ["fifo", "תור אחד לכולם"], ["any", "חיפוש בתור של ה-ID"]];
  const WORD = { timeout: "timeout", missing: "חסרה", unexpected: "לא צפויה", mismatch: "אי-התאמה" };
  const label = (e) => (e.op === "req" ? `req ${e.id}:${e.data}` : e.op === "rsp" ? `rsp ${e.id}:${e.data}` : e.op);

  // The box (0050): a scenario or a random stream with a bug; the events as a row of
  // chips (the current one framed, its time under it), the pending queue of every ID
  // under the per-ID checker (the head on the right), and a card per checker with its
  // errors so far and, at the end, whether it was right.
  const scoreboardView = () => ({
    mount(box) {
      const S0 = Number(box.dataset.scenario || 0);
      const st = { scen: S0, bug: "swap", seed: 1, k: 0, events: SCEN[S0][2], legal: SCEN[S0][1] };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>התרחיש <select class="sb-scen" aria-label="התרחיש">${SCEN.map(([n], i) => `<option value="${i}"${i === S0 ? " selected" : ""}>${n}</option>`).join("")}<option value="rand">זרם אקראי עם באג</option></select></label>` +
        `<label class="sb-buglab" hidden>הבאג <select class="sb-bug" aria-label="הבאג המוזרק">${BUGS.map(([v, n]) => `<option value="${v}"${v === "swap" ? " selected" : ""}>${n}</option>`).join("")}</select></label>` +
        `<span class="sb-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">התחלה</button>` +
        `<button type="button" class="md-button ex-prev">האירוע הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 600, 250) +
        `<button type="button" class="md-button md-button--primary ex-next">האירוע הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button><span class="ex-pos"></span></div>` +
        `<p class="ex-summary sb-sum" aria-live="polite"></p>` +
        `<div class="sb-events" dir="ltr"></div>` +
        `<p class="ex-title">התורים של הבודק "תור לכל ID" : הראש מימין, התשובה הבאה של ה-ID</p><div class="sb-queues" dir="ltr"></div>` +
        `<div class="sb-cards"></div>`;
      const $ = (sel) => box.querySelector(sel);
      let stop = () => {};
      const run = () => KINDS.map(([k]) => sbCheck(st.events, k, SB_TIMEOUT));
      const draw = () => {
        const N = st.events.length, k = st.k, runs = run(), cur = k ? st.events[k - 1] : null;
        $(".ex-pos").textContent = `אירוע ${k} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === N;
        $(".sb-buglab").hidden = st.scen !== "rand";
        const name = st.scen === "rand" ? `זרם אקראי, ${BUGS.find(([v]) => v === st.bug)[1]}` : SCEN[st.scen][0];
        $(".sb-sum").innerHTML = `${name} : ה-DUT ${st.legal ? "תקין" : "מכיל באג"}, timeout של ${ltr(SB_TIMEOUT)} מחזורים. ` +
          (cur ? `האירוע האחרון : ${code(label(cur))} בזמן ${ltr(cur.t)}.` : "עוד לא עבר אף אירוע.");
        $(".sb-events").innerHTML = st.events.map((e, j) => `<span class="sb-ev sb-${e.op}${j === k - 1 ? " is-now" : ""}${j >= k ? " is-later" : ""}"><b>${label(e)}</b><small>t=${e.t}</small></span>`).join("");
        const strip = $(".sb-events"), now = strip.querySelector(".is-now");   // a phone scrolls the row to the current event
        if (strip.scrollWidth > strip.clientWidth) strip.scrollLeft = now ? now.offsetLeft - strip.offsetLeft - strip.clientWidth / 2 + now.offsetWidth / 2 : 0;
        const ids = [...new Set(st.events.filter((e) => e.op === "req" || e.op === "rsp").map((e) => e.id))].sort((a, b) => a - b);
        const pend = k ? runs[0].trace[k - 1].pend : [];
        $(".sb-queues").innerHTML = ids.map((id) => {
          const q = pend.filter((p) => p.id === id);
          return `<div class="sb-q"><span class="sb-qname">ID ${id}</span><span class="sb-qitems">${q.length ? q.map((p, j) => `<span class="sb-qi${j === 0 ? " is-head" : ""}${p.late ? " is-late" : ""}">${p.data}</span>`).reverse().join("") : `<span class="sb-qempty">empty</span>`}</span></div>`;
        }).join("");
        $(".sb-cards").innerHTML = KINDS.map(([kk, title], i) => {
          const errs = k ? runs[i].trace.slice(0, k).flatMap((s) => s.added) : [];
          const done = k === N, total = runs[i].errors.length;
          const right = st.legal ? total === 0 : total > 0;
          const verdict = !done ? "" : right ? `<p class="wv-ok">✓ ${st.legal ? "עבר, ובצדק" : "תפס את הבאג"}</p>` : `<p class="wv-bad">✗ ${st.legal ? "אזעקת שווא" : "פספס את הבאג"}</p>`;
          const now = k && runs[i].trace[k - 1].added.length;
          return `<div class="sb-card${done ? (right ? " is-right" : " is-wrong") : ""}"><p class="sb-ctitle">${title}</p>` +
            `<p class="sb-cnow">${!k ? "—" : now ? `<span class="wv-bad">${runs[i].trace[k - 1].added.map(([w, id]) => `${WORD[w]} ב-ID ${id}`).join(", ")}</span>` : "בסדר"}</p>` +
            `<p class="sb-ccount">שגיאות עד עכשיו : ${ltr(errs.length)}</p>${verdict}</div>`;
        }).join("");
      };
      const load = () => {
        if (st.scen === "rand") { st.events = sbTraffic(st.seed, st.bug); st.legal = st.bug === "none"; }
        else { st.events = SCEN[st.scen][2]; st.legal = SCEN[st.scen][1]; }
        st.k = 0; draw();
      };
      const seed = seedControls(box, $(".sb-anchor"), (rng, s) => { stop(); st.seed = s; if (st.scen !== "rand") { st.scen = "rand"; $(".sb-scen").value = "rand"; } load(); }, { seed: 1, fresh: false });
      $(".sb-scen").addEventListener("change", () => { stop(); const v = $(".sb-scen").value; st.scen = v === "rand" ? "rand" : Number(v); load(); });
      $(".sb-bug").addEventListener("change", () => { stop(); st.bug = $(".sb-bug").value; load(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(0, st.k - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.k = Math.min(st.events.length, st.k + 1); draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = st.events.length; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); st.scen = S0; st.bug = "swap"; st.seed = 1; $(".sb-scen").value = String(S0); $(".sb-bug").value = "swap"; load(); });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k = Math.min(st.events.length, st.k + 1); draw(); }, done: () => st.k >= st.events.length, restart: () => { st.k = 0; draw(); } });
      void seed;
      draw();
    },
  });

  dvqExplorers.register({
    views: { scoreboard: scoreboardView },
    help: {
      scoreboard: "בוחרים תרחיש, או ״זרם אקראי עם באג״ ובאג להזרקה (ערך האתחול משחזר את אותו זרם), ועוברים אירוע אחרי אירוע. התורים מראים מה מחכה לתשובה בכל ID, והכרטיסים מראים מה כל אחד משלושת הבודקים מדווח. בסוף כל כרטיס אומר אם הבודק צדק.",
    },
    models: { sbCheck, sbTraffic },
  });
})();
