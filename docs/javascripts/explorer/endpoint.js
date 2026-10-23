// kinds: endpoint
//   endpoint               0023        a request builder on the block map, reads cut at RCB boundaries and interleaved cycle by cycle, the completions table; a timeline of every read's waits and completions; a cycle axis of the completions and the ready reads
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { H, W, autoplay, f, ltr, mulberry32, newSeed, seedControls, speedSel, waveStrip } = dvqExplorers.lib;

  // PCIe endpoint (0023): the page's UnalignedEndpointModel. `rng` is {randint(a, b),
  // choice(n)}: the draws in the page's order (the cut coins of a read, then its delay;
  // the pick among the ready reads, then the gap), so they can be scripted (the page's
  // examples) or replayed by the tests.
  const EP_RCB = 128, EP_MRRS = 256, EP_MIN_DELAY = 1, EP_MAX_DELAY = 20, EP_MAX_GAP = 10;
  const epUnitRng = (units, rnd = Math.random) => {
    const next = () => (units.length ? units.shift() : rnd());
    return { randint: (a, b) => a + Math.floor(next() * (b - a + 1)), choice: (n) => Math.floor(next() * n) };
  };
  const epValueRng = (values, fallback) => ({
    randint: (a, b) => (values.length ? values.shift() : fallback.randint(a, b)),
    choice: (n) => (values.length ? values.shift() : fallback.choice(n)),
  });
  const epInit = () => ({ memory: {}, pending: [], cycle: 0, out: [], writes: [], reads: [], nextTag: 0x15, nextRead: 0 });
  const epWrite = (s, address, data) => {
    let done = 0;
    while (done < data.length) {
      const block = Math.floor((address + done) / EP_RCB), off = (address + done) % EP_RCB;
      const n = Math.min(EP_RCB - off, data.length - done), key = block * EP_RCB;
      if (!s.memory[key]) s.memory[key] = new Array(EP_RCB).fill(0);
      for (let i = 0; i < n; i++) s.memory[key][off + i] = data[done + i];
      done += n;
    }
    s.writes.push({ address, length: data.length, id: s.writes.length + 1 });
  };
  const epReadBytes = (s, address, length) => {
    const out = [];
    let done = 0;
    while (done < length) {
      const block = Math.floor((address + done) / EP_RCB), off = (address + done) % EP_RCB;
      const n = Math.min(EP_RCB - off, length - done), blk = s.memory[block * EP_RCB];
      for (let i = 0; i < n; i++) out.push(blk ? blk[off + i] : 0);
      done += n;
    }
    return out;
  };
  const epFragments = (address, length, rng) => {
    const end = address + length, sizes = [];
    let last = address, boundary = (Math.floor(address / EP_RCB) + 1) * EP_RCB;
    while (boundary < end) {
      if (rng.randint(0, 1)) { sizes.push(boundary - last); last = boundary; }
      boundary += EP_RCB;
    }
    sizes.push(end - last);
    return sizes;
  };
  const epRead = (s, req, rng) => {
    if (!(req.length > 0 && req.length <= EP_MRRS)) throw new Error("read exceeds MRRS");
    const data = epReadBytes(s, req.address, req.length);
    const p = { id: s.nextRead++, tag: req.tag, rid: req.rid, address: req.address, length: req.length, cpls: [], ready: 0, sent: 0 };
    let address = req.address, remaining = req.length;
    epFragments(req.address, req.length, rng).forEach((size) => {
      const off = address - req.address;
      p.cpls.push({ address, size, bc: remaining, data: data.slice(off, off + size) });
      address += size; remaining -= size;
    });
    p.total = p.cpls.length;
    p.ready = s.cycle + rng.randint(EP_MIN_DELAY, EP_MAX_DELAY);
    s.pending.push(p);
    // the read's record keeps its timeline: issued at, and every wait window [from, ready]
    s.reads.push({ id: p.id, tag: p.tag, rid: p.rid, address: p.address, length: p.length, sizes: p.cpls.map((c) => c.size), issued: s.cycle, waits: [[s.cycle, p.ready]] });
    return p;
  };
  const epNext = (s, rng) => {
    const ready = s.pending.filter((p) => p.ready <= s.cycle);
    if (!ready.length) return null;
    const pick = ready[rng.choice(ready.length)], cpl = pick.cpls.shift();
    pick.sent += 1;
    if (pick.cpls.length) { pick.ready = s.cycle + rng.randint(1, EP_MAX_GAP); s.reads.find((r) => r.id === pick.id).waits.push([s.cycle, pick.ready]); }
    else s.pending.splice(s.pending.indexOf(pick), 1);
    const rec = { cycle: s.cycle, read: pick.id, tag: pick.tag, rid: pick.rid, address: cpl.address, size: cpl.size, bc: cpl.bc, first: cpl.data[0], last: cpl.data[cpl.data.length - 1] };
    s.out.push(rec);
    return rec;
  };
  // One cycle as the page's run does it: tick, then one completion at most.
  const epCycle = (s, rng) => { s.cycle += 1; return epNext(s, rng); };
  // The page's two examples (tools/figures/q0023.py): a 512-byte write of i mod 256, two reads.
  const EP_SCRIPTS = {
    a: { reads: [[0x10000, 256, 0x0200, 0x15], [0x10100, 256, 0x0200, 0x16]], draws: [1, 5, 1, 3, 0, 3, 0, 1, 1, 0] },
    b: { reads: [[0x10000, 256, 0x0200, 0x15], [0x10020, 256, 0x0300, 0x22]], draws: [1, 4, 1, 1, 2, 0, 3, 0, 2, 0, 1, 0, 0] },
  };
  // The cycle axis of the endpoint box (X146): per cycle 0 .. now, the completion that
  // went out (or none), and for each of the last `keep` reads whether it was ready and
  // waiting its turn: from a wait window's ready cycle to the completion that ends it.
  const epStrip = (s, keep = 6) => {
    const n = s.cycle + 1, byCycle = new Map(s.out.map((c) => [c.cycle, c]));
    const cpl = Array.from({ length: n }, (_, c) => byCycle.get(c) || null);
    const reads = s.reads.slice(-keep).map((r) => {
      const outs = s.out.filter((c) => c.read === r.id).map((c) => c.cycle);
      const ready = Array.from({ length: n }, () => 0);
      r.waits.forEach(([, rdy], k) => { const end = k < outs.length ? outs[k] : s.cycle; for (let c = rdy; c <= end && c < n; c++) ready[c] = 1; });
      return { id: r.id, tag: r.tag, ready };
    });
    return { n, cpl, reads };
  };
  const epRunScript = (script) => {
    const s = epInit(), rng = epValueRng([...script.draws], epUnitRng([]));
    epWrite(s, 0x10000, Array.from({ length: 512 }, (_, i) => i & 0xFF));
    script.reads.forEach(([address, length, rid, tag]) => epRead(s, { address, length, rid, tag }, rng));
    let guard = 0;
    while (s.pending.length && guard++ < 400) epCycle(s, rng);
    return s;
  };

  // The endpoint box (0023): a request builder (a write paints bytes on the block map, a
  // read is cut at random RCB boundaries and parked), a cycle button that runs the
  // page's tick-then-completion loop with the reads interleaved, the completions table
  // with the falling Byte Count, and the page's two examples with their exact draws.
  const endpointView = () => ({
    mount(box) {
      const hex = (v, w = 0) => "0x" + v.toString(16).toUpperCase().padStart(w, "0");
      const st = { s: epInit(), values: [], seed: newSeed(), used: 0, rng: null, log: "", err: "", history: [] };
      // the generator: the script's draws first, then mulberry32 from the seed; `used` counts
      // the seeded draws so a snapshot can be restored and replayed
      const makeRng = () => {
        const unit = mulberry32(st.seed);
        for (let i = 0; i < st.used; i++) unit();
        st.rng = epValueRng(st.values, epUnitRng([], () => { st.used += 1; return unit(); }));
      };
      makeRng();
      const snap = () => { st.history.push({ s: JSON.parse(JSON.stringify(st.s)), values: [...st.values], used: st.used, log: st.log }); if (st.history.length > 200) st.history.shift(); };
      box.innerHTML =
        `<div class="ex-controls"><span class="wv-presets">הדוגמאות שבעמוד : ` +
        `<button type="button" class="md-button ex-preset" data-p="a">סעיף א (מיושר)</button> ` +
        `<button type="button" class="md-button ex-preset" data-p="b">סעיף ב (לא מיושר)</button></span>` +
        `<button type="button" class="md-button ex-reset">איפוס</button></div>` +
        `<div class="ex-controls ep-form"><label>הבקשה <select class="ex-kind" aria-label="סוג הבקשה"><option value="write">MemWr (כתיבה)</option><option value="read" selected>MemRd (קריאה)</option></select></label>` +
        `<label>כתובת <input type="text" class="ex-addr" dir="ltr" value="0x10020" spellcheck="false" aria-label="כתובת בהקסה"></label>` +
        `<label>אורך בבתים <input type="number" class="ex-len" dir="ltr" min="1" max="256" value="256" aria-label="האורך בבתים"></label>` +
        `<button type="button" class="md-button md-button--primary ex-send">שלח בקשה</button><span class="ep-err"></span></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button md-button--primary ex-cycle">מחזור</button>` +
        `<button type="button" class="md-button ex-prev">צעד אחורה</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 600, 250) +
        `<button type="button" class="md-button ex-run">הרץ עד שכל ה-Completions יצאו</button><span class="ex-pos"></span></div>` +
        `<p class="ex-title">הזיכרון, בלוק אחרי בלוק (128 בתים) : הכתיבות צבועות, הקריאות הפתוחות מסומנות בקו</p><div class="ep-mem"></div>` +
        `<p class="ex-title">קריאות פתוחות</p><div class="ep-pending"></div><div class="ep-gantt"></div>` +
        `<p class="ex-title">ציר המחזורים : ה-Completion שיצא בכל מחזור, ומתי כל קריאה מוכנה</p><div class="wv-wrap ep-strip" tabindex="0" role="group" aria-label="ציר המחזורים, גלילה אופקית"></div>` +
        `<p class="wv-step an-log" aria-live="polite"></p>` +
        `<p class="ex-title">ה-Completions שיצאו</p><div class="ep-table" tabindex="0"></div><p class="ex-summary an-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const colour = (id) => `ep-c${id % 4}`;
      const render = () => {
        const s = st.s;
        $(".ex-pos").textContent = `מחזור ${s.cycle}`;
        $(".ex-prev").disabled = !st.history.length;
        // the block map
        const keys = new Set(Object.keys(s.memory).map(Number));
        s.pending.forEach((p) => { for (let a = Math.floor(p.address / EP_RCB) * EP_RCB; a < p.address + p.length; a += EP_RCB) keys.add(a); });
        const blocks = [...keys].sort((a, b) => a - b);
        if (!blocks.length) $(".ep-mem").innerHTML = `<p class="an-empty">הזיכרון ריק : בית שלא נכתב נקרא כאפס.</p>`;
        else {
          const W = 520, L = 86, SW = (W - L - 8) / EP_RCB, RH = 26;
          let g = `<svg class="ep-live" viewBox="0 0 ${W} ${blocks.length * RH + 6}" role="img" aria-label="מפת הבלוקים : הבתים שנכתבו והקריאות הפתוחות">`;
          blocks.forEach((key, r) => {
            const y = 3 + r * RH;
            g += `<text class="wv-name" x="${L - 6}" y="${y + 16}" text-anchor="end">${hex(key)}</text><rect class="ep-block" x="${L}" y="${y}" width="${f(EP_RCB * SW)}" height="${RH - 6}"/>`;
            // written ranges: by the write that touched each byte (the latest wins)
            const owner = new Array(EP_RCB).fill(0);
            s.writes.forEach((w) => { for (let a = Math.max(w.address, key); a < Math.min(w.address + w.length, key + EP_RCB); a++) owner[a - key] = w.id; });
            let i = 0;
            while (i < EP_RCB) { let j = i; while (j + 1 < EP_RCB && owner[j + 1] === owner[i]) j++; if (owner[i]) g += `<rect class="ep-written ${colour(owner[i])}" x="${f(L + i * SW)}" y="${y}" width="${f((j - i + 1) * SW)}" height="${RH - 6}"><title>כתיבה ${owner[i]} : ${hex(key + i)} עד ${hex(key + j)}</title></rect>`; i = j + 1; }
            s.pending.forEach((p) => {
              const a = Math.max(p.address, key), b = Math.min(p.address + p.length, key + EP_RCB);
              if (a < b) g += `<rect class="ep-read ${colour(p.id)}" x="${f(L + (a - key) * SW)}" y="${y - 2}" width="${f((b - a) * SW)}" height="${RH - 2}"/>`;
            });
          });
          $(".ep-mem").innerHTML = g + `</svg>`;
        }
        $(".ep-pending").innerHTML = s.pending.length ? s.pending.map((p) => {
          const status = p.ready > s.cycle ? `מוכן ממחזור ${ltr(p.ready)}` : `<span class="wv-ok">מוכן</span>`;
          return `<p class="ep-pend ${colour(p.id)}"><span class="ep-swatch"></span>‏Tag ${ltr(hex(p.tag, 2))}, ${ltr(hex(p.address))}, ${ltr(p.length)} בתים : ` +
            `<span class="an-chips" dir="ltr">${p.cpls.map((c, i) => `<span class="an-chip${i === 0 ? " is-head" : ""}">${c.size} B · BC ${c.bc}</span>`).join("")}</span> ` +
            `${p.sent ? `יצאו ${ltr(p.sent)} מתוך ${ltr(p.total)}, ` : ""}${status}.</p>`;
        }).join("") : `<p class="an-empty">אין קריאות פתוחות.</p>`;
        // the timeline of every read: its random wait dashed, the time it is ready and
        // waiting its turn solid, a mark per completion, and a line at the current cycle
        const reads = s.reads;
        if (!reads.length) $(".ep-gantt").innerHTML = "";
        else {
          const W = 520, L = 86, RH = 22, last = Math.max(s.cycle, ...reads.flatMap((r) => r.waits.map((w) => w[1]))) + 1;
          const X = (c) => L + (c / last) * (W - L - 10), H = reads.length * RH + 22;
          const step = last > 60 ? 20 : last > 30 ? 10 : last > 12 ? 5 : 1;
          let g = `<svg class="ep-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="ציר המחזורים : לכל קריאה ההמתנות שלה וה-Completions שיצאו">`;
          for (let c = 0; c <= last; c += step) g += `<line class="grid" x1="${f(X(c))}" x2="${f(X(c))}" y1="2" y2="${H - 18}"/><text class="tick" x="${f(X(c))}" y="${H - 5}" text-anchor="middle">${c}</text>`;
          reads.forEach((r, i) => {
            const y = 2 + i * RH + RH / 2, outs = s.out.filter((c) => c.read === r.id);
            g += `<text class="wv-name" x="${L - 6}" y="${f(y + 4)}" text-anchor="end">Tag ${hex(r.tag, 2)}</text>`;
            r.waits.forEach(([from, ready], k) => {
              const until = outs[k] ? outs[k].cycle : s.cycle;
              g += `<line class="ep-wait ${colour(r.id)}" x1="${f(X(from))}" x2="${f(X(ready))}" y1="${y}" y2="${y}"><title>ממתינה ממחזור ${from} עד ${ready}</title></line>`;
              if (until > ready) g += `<line class="ep-ready ${colour(r.id)}" x1="${f(X(ready))}" x2="${f(X(until))}" y1="${y}" y2="${y}"><title>מוכנה ממחזור ${ready}, מחכה לתורה</title></line>`;
            });
            outs.forEach((c) => { g += `<circle class="ep-cpl ${colour(r.id)}" cx="${f(X(c.cycle))}" cy="${y}" r="5"><title>מחזור ${c.cycle} : ${c.size} בתים מ-${hex(c.address)}, Byte Count ${c.bc}</title></circle>`; });
          });
          g += `<line class="ep-now" x1="${f(X(s.cycle))}" x2="${f(X(s.cycle))}" y1="0" y2="${H - 16}"/>`;
          $(".ep-gantt").innerHTML = g + `</svg><p class="viz-legend ep-legend"><span><i class="ep-lg-wait"></i>ממתינה לזמן האקראי</span><span><i class="ep-lg-ready"></i>מוכנה, מחכה לתורה</span><span><i class="ep-lg-cpl"></i>‏Completion יצא</span><span><i class="ep-lg-now"></i>המחזור הנוכחי</span></p>`;
        }
        // the cycle axis: the last 64 cycles
        const es = epStrip(s), from = Math.max(0, es.n - 64), n = es.n - from;
        const cut = (a) => a.slice(from);
        const stripEl = $(".ep-strip");
        stripEl.innerHTML = waveStrip([
          { name: "Tag", kind: "bus", split: true, values: cut(es.cpl).map((c) => (c ? hex(c.tag, 2) : "—")) },
          { name: "size", kind: "bus", split: true, values: cut(es.cpl).map((c) => (c ? c.size : "—")) },
          { name: "BC", kind: "bus", split: true, values: cut(es.cpl).map((c) => (c ? c.bc : "—")) },
        ].concat(es.reads.map((r) => ({ name: `ready ${hex(r.tag, 2)}`, kind: "bit", values: cut(r.ready), cls: ["wv-s1", "wv-s2", "wv-s3"][r.id % 3] }))),
        n, { slotW: 46, labelW: 92, cursor: n - 1, ticks: (k) => from + k, label: `ציר המחזורים : ${n} מחזורים` });
        stripEl.scrollLeft = stripEl.scrollWidth;
        $(".an-log").innerHTML = (st.err ? `<span class="wv-bad">${st.err}</span> ` : "") + st.log;
        $(".ep-table").innerHTML = s.out.length ? `<table><thead><tr><th>מחזור</th><th>Requester ID</th><th>Tag</th><th>כתובת</th><th>גודל</th><th>Byte Count</th><th>הבית הראשון והאחרון</th></tr></thead><tbody>` +
          s.out.map((c) => `<tr class="${colour(c.read)}"><td>${ltr(c.cycle)}</td><td>${ltr(hex(c.rid, 4))}</td><td>${ltr(hex(c.tag, 2))}</td><td>${ltr(hex(c.address))}</td><td>${ltr(c.size)}</td><td>${ltr(c.bc)}</td><td>${ltr(`${hex(c.first, 2)} … ${hex(c.last, 2)}`)}</td></tr>`).join("") + `</tbody></table>` : `<p class="an-empty">עדיין לא יצא Completion.</p>`;
        // the rules, checked on what went out
        const perRead = new Map();
        s.out.forEach((c) => { if (!perRead.has(c.read)) perRead.set(c.read, []); perRead.get(c.read).push(c); });
        let ok = true, notes = [];
        perRead.forEach((list, id) => {
          const rd = s.reads.find((r) => r.id === id);
          const ascending = list.every((c, i) => i === 0 || c.address === list[i - 1].address + list[i - 1].size);
          const cuts = list.every((c, i) => i === 0 || c.address % EP_RCB === 0);
          const bc = list.every((c, i) => c.bc === rd.length - (c.address - rd.address));
          const mps = list.every((c) => c.size <= 256);
          if (!(ascending && cuts && bc && mps)) ok = false;
          const done = !s.pending.some((p) => p.id === id);
          if (done && list.reduce((a, c) => a + c.size, 0) !== rd.length) ok = false;
          notes.push(`Tag ${ltr(hex(rd.tag, 2))}: ${ltr(list.map((c) => c.size).join(" + "))}${done ? ` = ${ltr(rd.length)}` : " …"}`);
        });
        const perCycle = new Set(s.out.map((c) => c.cycle)).size === s.out.length;
        $(".an-sum").innerHTML = s.out.length
          ? (ok && perCycle ? `<span class="wv-ok">✓ בכל קריאה : סדר כתובות עולה, חיתוך רק על כפולות של 128, Byte Count יורד נכון, לכל היותר 256 בתים, ו-Completion אחד לכל היותר במחזור.</span> ` : `<span class="wv-bad">✗ כלל הופר.</span> `) + notes.join("; ") + "."
          : `שולחים כתיבה וקריאות, ואז מקדמים מחזורים : כל קריאה מחכה זמן אקראי, ובין קריאות מוכנות הבחירה אקראית, ומכאן השילוב.`;
      };
      const parseAddr = () => { const t = $(".ex-addr").value.trim(); const v = /^0x[0-9a-f]+$/i.test(t) ? parseInt(t, 16) : /^\d+$/.test(t) ? Number(t) : NaN; return v; };
      $(".ex-send").addEventListener("click", () => {
        stop();
        st.err = "";
        const address = parseAddr(), length = Number($(".ex-len").value);
        if (!Number.isFinite(address) || address < 0) st.err = "כתובת לא תקינה (הקסה, למשל 0x10020).";
        else if (!(length >= 1 && length <= EP_MRRS)) st.err = `האורך חייב להיות בין 1 ל-${EP_MRRS} (MRRS).`;
        else if (Math.floor(address / 4096) !== Math.floor((address + length - 1) / 4096)) st.err = "בקשה לא חוצה גבול של 4 KB.";
        if (st.err) { render(); return; }
        snap();
        if ($(".ex-kind").value === "write") {
          const w = st.s.writes.length + 1;
          epWrite(st.s, address, Array.from({ length }, (_, i) => (i + 0x10 * w) & 0xFF));
          st.log = `כתיבה ${ltr(w)} : ${ltr(length)} בתים מ-${ltr(hex(address))} (הבית ה-${ltr("i")} שווה ל-${ltr(`i + ${hex(0x10 * w)}`)}), posted : הבלוקים שנגעו בהם מתעדכנים, בלי Completion.`;
        } else {
          const tag = st.s.nextTag++, rid = 0x0200;
          const p = epRead(st.s, { address, length, rid, tag }, st.rng);
          st.log = `קריאה Tag ${ltr(hex(tag, 2))} : ${ltr(length)} בתים מ-${ltr(hex(address))}. ה-Completions נבנו עכשיו, בסדר כתובות : ${ltr(p.cpls.map((c) => c.size).join(" + "))} (חיתוך אקראי על גבולות 128), ויחכו עד מחזור ${ltr(p.ready)}.`;
        }
        render();
      });
      const cycle = () => {
        const c = epCycle(st.s, st.rng);
        st.err = "";
        st.log = c ? `מחזור ${ltr(st.s.cycle)} : יוצא Completion של Tag ${ltr(hex(c.tag, 2))} מ-${ltr(hex(c.address))}, ${ltr(c.size)} בתים, Byte Count ${ltr(c.bc)}` + (st.s.pending.some((p) => p.tag === c.tag) ? ` (הבא של אותה קריאה אחרי המתנה אקראית).` : ` (האחרון של הקריאה).`)
          : `מחזור ${ltr(st.s.cycle)} : אין קריאה מוכנה, לא יוצא דבר.`;
      };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: () => { snap(); cycle(); render(); },
        done: () => !st.s.pending.length,
        restart: () => {},
      });
      $(".ex-cycle").addEventListener("click", () => { stop(); snap(); cycle(); render(); });
      $(".ex-prev").addEventListener("click", () => {
        stop();
        const h = st.history.pop();
        if (!h) return;
        st.s = h.s; st.values = h.values; st.used = h.used; st.log = h.log; st.err = "";
        makeRng(); render();
      });
      $(".ex-run").addEventListener("click", () => { stop(); if (st.s.pending.length) snap(); let guard = 0; while (st.s.pending.length && guard++ < 400) cycle(); if (!guard) st.log = "אין קריאות פתוחות."; render(); });
      const load = (script) => {
        stop();
        st.s = epInit(); st.values = script ? [...script.draws] : []; st.used = 0; st.history = []; st.err = "";
        makeRng();
        if (script) {
          epWrite(st.s, 0x10000, Array.from({ length: 512 }, (_, i) => i & 0xFF));
          script.reads.forEach(([address, length, rid, tag]) => epRead(st.s, { address, length, rid, tag }, st.rng));
          st.s.nextTag = 0x30;
          st.log = `הדוגמה שבעמוד : כתיבה של 512 בתים מ-${ltr("0x10000")} (הבית ה-${ltr("i")} שווה ל-${ltr("i mod 256")}) ושתי קריאות עם הפיצול וההמתנות שבעמוד. "מחזור" או "הרץ" מוציאים את ה-Completions.`;
        } else st.log = "";
        render();
      };
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => load(EP_SCRIPTS[b.dataset.p])));
      $(".ex-reset").addEventListener("click", () => seed.draw());
      load(EP_SCRIPTS.b);
      const seed = seedControls(box, $(".ex-reset"), (rng, n) => { st.seed = n; load(null); }, { seed: st.seed });
    },
  });

  dvqExplorers.register({
    views: { endpoint: endpointView },
    help: {
      endpoint: "בונים בקשות כתיבה וקריאה : ״מחזור״ ו״הרץ״ מוציאים Completions לפי המודל, ומפת הבלוקים, ציר ההמתנות, ציר המחזורים וטבלת ה-Completions מתעדכנים. ה-presets טוענים את דוגמאות העמוד.",
    },
    models: { epStrip, EP_RCB, epUnitRng, epValueRng, epInit, epWrite, epReadBytes, epFragments, epRead, epNext, epCycle, EP_SCRIPTS, epRunScript },
  });
})();
